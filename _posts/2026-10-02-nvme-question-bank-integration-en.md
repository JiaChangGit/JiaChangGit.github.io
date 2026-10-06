---
layout: post
title: "NVMe Self-Study Bank: Integrated validation and evidence correlation"
date: 2026-10-02 00:00:00 +0800
categories: [nvme]
permalink: /nvme/question-bank/integration/en/
lang: en
nvme_quickref: true
nvme_qa: true
---

<div class="nvme-quickref nvme-qa">
<nav class="qr-top" aria-label="Bank and editions"><a href="#content">Skip to content</a><a href="/nvme/question-bank/en/">Question index</a><a href="/nvme/question-bank/integration/zh-tw/">繁體中文</a><a href="/DOCS/nvme-question-bank/integration.html">Chinese tutorial HTML</a></nav>
<main id="content"><p class="qr-eyebrow">BASE 2.4 / NVM 1.3 / PCIe 1.4 · Q1–328</p>
<header><p class="qa-range">Q297–Q320</p><h1>Integrated validation and evidence correlation</h1><p class="qr-intro">Apply prior mechanisms to apparent contradictions, matching identity and time before judging evidence.</p><p>Practice first, then reveal the explanation. Each question uses the prose, field interpretation, comparison or flow that suits it. All numerical examples are hypothetical. Status is written SCT/SC; h indicates hexadecimal.</p></header>
<aside class="qa-glossary"><h2>Terms used in this volume</h2><dl><dt>Controller / namespace</dt><dd>A controller receives commands and manages access. A namespace is a logical storage space that commands can address. An NVM subsystem contains controllers and nonvolatile storage resources.</dd><dt>SQ / CQ / SQE / CQE</dt><dd>Submission and Completion Queues carry command entries (SQEs) and completion entries (CQEs). QID identifies a queue, CID distinguishes outstanding commands in one SQ, and NSID identifies a namespace.</dd><dt>Register / Identify / Feature / Log</dt><dd>A register exposes control or state. Identify queries capabilities and attributes; features query or configure operation; log pages report specific state or records. FID, LID, CNS and CSI select features, logs, Identify structures and command sets.</dd><dt>index / offset / zero-based</dt><dd>An index selects an entry, usually starting at 0; an offset measures distance from an origin in specified units. A zero-based count encodes count−1, but not every zero-valued field is a count. A Dword is 4 bytes; a byte is 8 bits.</dd><dt>Scope / reset / retention</dt><dd>Scope names the affected objects; retention means preserving state. Controller Reset (clearing CC.EN) is one form of Controller Level Reset, or CLR. Different CLR triggers can retain different registers.</dd></dl></aside>
<section id="overview" class="qa-overview"><h2>A reproducible evidence path</h2><p class="qa-takeaway">State the requirement before collecting evidence; volume is not completeness.</p>
<div class="qr-table" tabindex="0" role="region" aria-label="Horizontally scrollable comparison table"><table><thead><tr><th scope="col">Stage</th><th scope="col">Preserve</th><th scope="col">Avoid</th></tr></thead><tbody><tr><td>Preconditions</td><td>Support, scope, configuration, state</td><td>Support means all requests are legal</td></tr><tr><td>Operation</td><td>Request, selectors, time</td><td>Reconstructed rather than original evidence</td></tr><tr><td>Results</td><td>Completion, logs, events</td><td>Acceptance equals operation completion</td></tr><tr><td>Persistence</td><td>Reset type and state changes</td><td>All resets have identical effects</td></tr></tbody></table></div>
<p><strong>Worked interpretation: </strong>Successful initiation with progress is normal; confirmed final completion with persistent same-scope in-progress data needs investigation.</p>
<p class="qa-citations">Sources: <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-commandseffects">Base 2.4 §5.2.13.1.6</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-getlog">Base 2.4 §5.2.13–5.2.13.1.1</a> · <a href="#ref-aerfull">Base 2.4 §5.2.2 (PCIe-applicable events)</a> · <a href="#ref-pelcontext">Base 2.4 §5.2.13.1.14–5.2.13.1.14.2.5 (exclude PCIe link/packet decoding)</a></p>
</section>
<div class="qa-controls" hidden><label>Search this page <input type="search" id="qa-search" placeholder="Question number, field or keyword"></label><button type="button" data-expand="true">Expand all answers</button><button type="button" data-expand="false">Collapse all answers</button><output id="qa-count" aria-live="polite"></output></div>
<section id="question-index"><h2>Questions in this volume</h2><ol class="qa-index">
<li><a href="#q-297">Q297 · Where do you start when an advertised command fails?</a></li>
<li><a href="#q-298">Q298 · Does success of an unadvertised command prove compliance?</a></li>
<li><a href="#q-299">Q299 · How is a successful Set with different readback or behavior investigated?</a></li>
<li><a href="#q-300">Q300 · Why might an AER completion have no matching visible log information?</a></li>
<li><a href="#q-301">Q301 · Does every failed CQE require a new error entry?</a></li>
<li><a href="#q-302">Q302 · When do differing CQE, Error Information and PEL records conflict?</a></li>
<li><a href="#q-303">Q303 · How are unexpected feature retention or lost saved values assessed?</a></li>
<li><a href="#q-304">Q304 · How are namespace changes reconciled across Identify, lists and AER?</a></li>
<li><a href="#q-305">Q305 · How are unchanged firmware revision or slot fields assessed after activation?</a></li>
<li><a href="#q-306">Q306 · Is an in-progress log after sanitize command success an error?</a></li>
<li><a href="#q-307">Q307 · How is a missing result after self-test investigated?</a></li>
<li><a href="#q-308">Q308 · How are unexpected unsafe-shutdown counts assessed?</a></li>
<li><a href="#q-309">Q309 · Which settings explain a warning change without an AER?</a></li>
<li><a href="#q-310">Q310 · How is apparent PEL event-order mismatch investigated?</a></li>
<li><a href="#q-311">Q311 · What evidence remains when CFS is set with little diagnostic information?</a></li>
<li><a href="#q-312">Q312 · How are two observed completions after Abort classified?</a></li>
<li><a href="#q-313">Q313 · What is wrong with queue-memory access after completed deletion?</a></li>
<li><a href="#q-314">Q314 · How should a CQE from before reset be handled?</a></li>
<li><a href="#q-315">Q315 · When can command success after detach be reasonable?</a></li>
<li><a href="#q-316">Q316 · How is apparent Lockdown bypass investigated?</a></li>
<li><a href="#q-317">Q317 · How is excessive power-state recovery latency measured correctly?</a></li>
<li><a href="#q-318">Q318 · How are three reset types compared for one feature?</a></li>
<li><a href="#q-319">Q319 · How is an operation’s real scope established?</a></li>
<li><a href="#q-320">Q320 · How are the interfaces combined into one conformance investigation?</a></li>
</ol></section>
<article class="qa-question" id="q-297" data-question="297" data-answer-kind="diagnose"><h2><a class="qa-qid" href="#q-297">Q297</a> Where do you start when an advertised command fails?</h2>
<p class="qa-prompt">Separate available evidence from missing information before judging conformance.</p>
<details class="qa-answer" id="q-297-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-297-a-01">Distinguish command support from legality and executability of this request.</p><div class="qa-sections">
<section class="qa-section" id="q-297-s-01" data-answer-section="1"><h3><span>1.</span> Preserve the evidence first</h3>
<span class="qa-anchor" id="q-297-a-02"></span><p>Match controller, command set, namespace and time before comparing support.</p>
<span class="qa-anchor" id="q-297-a-03"></span><p>Preserve Identify support, CSUPP and CSI/UUID selectors.</p>
<span class="qa-anchor" id="q-297-a-04"></span><p>If supported Format returns Invalid Format, compare its LBAF with the namespace’s formats.</p>
</section>
<section class="qa-section" id="q-297-s-02" data-answer-section="2"><h3><span>2.</span> Work through the possible causes</h3>
<span class="qa-anchor" id="q-297-a-17"></span><p>First inspect SCT/SC rather than an application’s generic failure label.</p>
<span class="qa-anchor" id="q-297-a-05"></span><p>Decode the CQE, then validate selectors, namespace state, protection and active-operation restrictions.</p>
</section>
<section class="qa-section" id="q-297-s-03" data-answer-section="3"><h3><span>3.</span> Decide what the evidence supports</h3>
<span class="qa-anchor" id="q-297-a-06"></span><p>Rejecting an unsupported LBA format can be consistent with supporting Format.</p>
<span class="qa-anchor" id="q-297-a-07"></span><p>Invalid Opcode with all prerequisites met warrants support-consistency investigation, not an automatic conclusion from any failure.</p>
<span class="qa-anchor" id="q-297-a-16"></span><p>Use a contemporaneous valid control differing in one relevant condition.</p>
</section>
</div>
<span class="qa-anchor" id="q-297-a-08"></span><span class="qa-anchor" id="q-297-a-09"></span><span class="qa-anchor" id="q-297-a-10"></span><span class="qa-anchor" id="q-297-a-11"></span><span class="qa-anchor" id="q-297-a-12"></span><span class="qa-anchor" id="q-297-a-13"></span><span class="qa-anchor" id="q-297-a-14"></span><span class="qa-anchor" id="q-297-a-15"></span>
<p class="qa-related">Related mechanisms: <a href="/nvme/question-bank/identify/en/#q-050">Q50</a> · <a href="/nvme/question-bank/logs/en/#q-081">Q81</a> · <a href="/nvme/question-bank/errors/en/#q-093">Q93</a></p>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-commandseffects">Base 2.4 §5.2.13.1.6</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-298" data-question="298" data-answer-kind="diagnose"><h2><a class="qa-qid" href="#q-298">Q298</a> Does success of an unadvertised command prove compliance?</h2>
<p class="qa-prompt">Separate available evidence from missing information before judging conformance.</p>
<details class="qa-answer" id="q-298-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-298-a-01">Success does not correct an inaccurate capability declaration.</p><div class="qa-sections">
<section class="qa-section" id="q-298-s-01" data-answer-section="1"><h3><span>1.</span> Preserve the evidence first</h3>
<span class="qa-anchor" id="q-298-a-02"></span><p>Establish applicability to controller type, command set and query revision.</p>
<span class="qa-anchor" id="q-298-a-03"></span><p>Compare the relevant discovery interface rather than unrelated capability bits.</p>
<span class="qa-anchor" id="q-298-a-04"></span><p>CSUPP0 and successful effective execution of that opcode under the same CSI require investigation.</p>
</section>
<section class="qa-section" id="q-298-s-02" data-answer-section="2"><h3><span>2.</span> Work through the possible causes</h3>
<span class="qa-anchor" id="q-298-a-17"></span><p>First compare discovery and execution selectors.</p>
<span class="qa-anchor" id="q-298-a-05"></span><p>Exclude stale snapshots, activation, opcode-category confusion and reserved-field misinterpretation.</p>
</section>
<section class="qa-section" id="q-298-s-03" data-answer-section="3"><h3><span>3.</span> Decide what the evidence supports</h3>
<span class="qa-anchor" id="q-298-a-06"></span><p>Capability, completion and observable effects must agree.</p>
<span class="qa-anchor" id="q-298-a-07"></span><p>Require rejection only where the specification defines unsupported behavior; inapplicable zero fields do not universally prohibit commands.</p>
<span class="qa-anchor" id="q-298-a-16"></span><p>Preserve contradictory evidence and cite the exact declaration rule.</p>
</section>
</div>
<span class="qa-anchor" id="q-298-a-08"></span><span class="qa-anchor" id="q-298-a-09"></span><span class="qa-anchor" id="q-298-a-10"></span><span class="qa-anchor" id="q-298-a-11"></span><span class="qa-anchor" id="q-298-a-12"></span><span class="qa-anchor" id="q-298-a-13"></span><span class="qa-anchor" id="q-298-a-14"></span><span class="qa-anchor" id="q-298-a-15"></span>
<p class="qa-related">Related mechanisms: <a href="/nvme/question-bank/identify/en/#q-048">Q48</a> · <a href="/nvme/question-bank/identify/en/#q-050">Q50</a> · <a href="/nvme/question-bank/logs/en/#q-080">Q80</a></p>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-commandseffects">Base 2.4 §5.2.13.1.6</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-299" data-question="299" data-answer-kind="diagnose"><h2><a class="qa-qid" href="#q-299">Q299</a> How is a successful Set with different readback or behavior investigated?</h2>
<p class="qa-prompt">Separate available evidence from missing information before judging conformance.</p>
<details class="qa-answer" id="q-299-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-299-a-01">Separate acceptance, current value, saved value and actual effect.</p><div class="qa-sections">
<section class="qa-section" id="q-299-s-01" data-answer-section="1"><h3><span>1.</span> Preserve the evidence first</h3>
<span class="qa-anchor" id="q-299-a-02"></span><p>Feature scope determines the target that Get must match.</p>
<span class="qa-anchor" id="q-299-a-03"></span><p>Check supported capabilities and whether the feature may adjust requested values.</p>
<span class="qa-anchor" id="q-299-a-04"></span><p>KATO may round up to KAS granularity, so a larger readback is not necessarily wrong.</p>
</section>
<section class="qa-section" id="q-299-s-02" data-answer-section="2"><h3><span>2.</span> Work through the possible causes</h3>
<span class="qa-anchor" id="q-299-a-05"></span>
<span class="qa-anchor" id="q-299-a-06"></span>
<span class="qa-anchor" id="q-299-a-17"></span>
<figure class="qa-flow" id="q-299-flow"><figcaption>Align query conditions before comparing Set and Get</figcaption>
<p>First rule out reading a different kind of value before concluding that the controller failed to apply a setting.</p><ol class="qa-flow-steps">
<li class="qa-flow-step"><strong>Preserve the Set request and successful completion</strong><p>Record FID, SV, NSID, other selectors and the payload.</p></li>
<li class="qa-flow-step"><span class="qa-flow-arrow" aria-hidden="true">↓</span><strong>Read Current with SEL=0 on the same target</strong><p>Default, Saved or another namespace’s value does not directly verify this current setting.</p></li>
<li class="qa-flow-step"><span class="qa-flow-arrow" aria-hidden="true">↓</span><strong>Check allowed adjustment, then observe behavior</strong><p>A permitted adjusted value with matching behavior can be a valid successful result.</p></li>
<li class="qa-flow-branch"><strong>To test saving, separately inspect Saved and the specified reset</strong><p>Persistence is a separate test objective; do not collapse current-value and reset-recovery checks into one numeric comparison.</p></li>
</ol><p class="qa-flow-conclusion">Investigate implementation inconsistency only after ruling out different selectors, permitted adjustment, another Set and intervening reset.</p></figure>
</section>
<section class="qa-section" id="q-299-s-03" data-answer-section="3"><h3><span>3.</span> Decide what the evidence supports</h3>
<span class="qa-anchor" id="q-299-a-07"></span><p>Correct selector mistakes before diagnosing unexplained same-target inconsistency.</p>
<span class="qa-anchor" id="q-299-a-16"></span><p>Track intervening configuration, resets and mode changes.</p>
</section>
</div>
<span class="qa-anchor" id="q-299-a-08"></span><span class="qa-anchor" id="q-299-a-09"></span><span class="qa-anchor" id="q-299-a-10"></span><span class="qa-anchor" id="q-299-a-11"></span><span class="qa-anchor" id="q-299-a-12"></span><span class="qa-anchor" id="q-299-a-13"></span><span class="qa-anchor" id="q-299-a-14"></span><span class="qa-anchor" id="q-299-a-15"></span>
<p class="qa-related">Related mechanisms: <a href="/nvme/question-bank/features/en/#q-054">Q54</a> · <a href="/nvme/question-bank/features/en/#q-055">Q55</a> · <a href="/nvme/question-bank/features/en/#q-066">Q66</a> · <a href="/nvme/question-bank/features/en/#q-068">Q68</a></p>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-featureeffects">Base 2.4 §5.2.13.1.18</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-300" data-question="300" data-answer-kind="diagnose"><h2><a class="qa-qid" href="#q-300">Q300</a> Why might an AER completion have no matching visible log information?</h2>
<p class="qa-prompt">Separate available evidence from missing information before judging conformance.</p>
<details class="qa-answer" id="q-300-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-300-a-01">A notice identifies a qualifying event, while the log may expose current state rather than a historical snapshot.</p><div class="qa-sections">
<section class="qa-section" id="q-300-s-01" data-answer-section="1"><h3><span>1.</span> Preserve the evidence first</h3>
<span class="qa-anchor" id="q-300-a-02"></span><p>Match log scope to the event’s endpoint and entity.</p>
<span class="qa-anchor" id="q-300-a-03"></span><p>Preserve event type, information, LID and required selectors.</p>
<span class="qa-anchor" id="q-300-a-04"></span><p>A temperature warning may clear before a later SMART read without invalidating the earlier event.</p>
</section>
<section class="qa-section" id="q-300-s-02" data-answer-section="2"><h3><span>2.</span> Work through the possible causes</h3>
<span class="qa-anchor" id="q-300-a-17"></span><p>First check LID, scope and observation delay.</p>
<span class="qa-anchor" id="q-300-a-05"></span><p>Read the matching log and check intervening acknowledgments and state changes.</p>
</section>
<section class="qa-section" id="q-300-s-03" data-answer-section="3"><h3><span>3.</span> Decide what the evidence supports</h3>
<span class="qa-anchor" id="q-300-a-06"></span><p>A coherent timeline can explain cleared current state after a valid event.</p>
<span class="qa-anchor" id="q-300-a-07"></span><p>Immediate, One-Shot and ordinary events have distinct clearing rules.</p>
<span class="qa-anchor" id="q-300-a-16"></span><p>Preserve the first read and all acknowledgments before investigating persistent inconsistency.</p>
</section>
</div>
<span class="qa-anchor" id="q-300-a-08"></span><span class="qa-anchor" id="q-300-a-09"></span><span class="qa-anchor" id="q-300-a-10"></span><span class="qa-anchor" id="q-300-a-11"></span><span class="qa-anchor" id="q-300-a-12"></span><span class="qa-anchor" id="q-300-a-13"></span><span class="qa-anchor" id="q-300-a-14"></span><span class="qa-anchor" id="q-300-a-15"></span>
<p class="qa-related">Related mechanisms: <a href="/nvme/question-bank/asynchronous-events/en/#q-083">Q83</a> · <a href="/nvme/question-bank/asynchronous-events/en/#q-084">Q84</a> · <a href="/nvme/question-bank/asynchronous-events/en/#q-090">Q90</a> · <a href="/nvme/question-bank/asynchronous-events/en/#q-092">Q92</a></p>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-aerfull">Base 2.4 §5.2.2 (PCIe-applicable events)</a> · <a href="#ref-getlog">Base 2.4 §5.2.13–5.2.13.1.1</a> · <a href="#ref-smart">Base 2.4 §5.2.13.1.3</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-301" data-question="301" data-answer-kind="diagnose"><h2><a class="qa-qid" href="#q-301">Q301</a> Does every failed CQE require a new error entry?</h2>
<p class="qa-prompt">Separate available evidence from missing information before judging conformance.</p>
<details class="qa-answer" id="q-301-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-301-a-01">Error Information is not a mandatory one-entry copy of every failed CQE.</p><div class="qa-sections">
<section class="qa-section" id="q-301-s-01" data-answer-section="1"><h3><span>1.</span> Preserve the evidence first</h3>
<span class="qa-anchor" id="q-301-a-02"></span><p>Match controller and error counts, considering overwrite by concurrent failures.</p>
<span class="qa-anchor" id="q-301-a-03"></span><p>Inspect More and command-specific logging requirements.</p>
<span class="qa-anchor" id="q-301-a-04"></span><p>More 1 indicates additional status information, while More 0 does not prohibit logging.</p>
</section>
<section class="qa-section" id="q-301-s-02" data-answer-section="2"><h3><span>2.</span> Work through the possible causes</h3>
<span class="qa-anchor" id="q-301-a-17"></span><p>First establish this error’s exact logging requirement strength.</p>
<span class="qa-anchor" id="q-301-a-05"></span><p>Compare before/after counts and correlate valid entries by command identity and status.</p>
</section>
<section class="qa-section" id="q-301-s-03" data-answer-section="3"><h3><span>3.</span> Decide what the evidence supports</h3>
<span class="qa-anchor" id="q-301-a-06"></span><p>Absence can be compliant where no applicable mandatory logging requirement exists.</p>
<span class="qa-anchor" id="q-301-a-07"></span><p>Explicit mandatory details, such as specified capacity failures, override general optionality.</p>
<span class="qa-anchor" id="q-301-a-16"></span><p>Exclude overwrite, reset clearing and incomplete reads before declaring a missing record.</p>
</section>
<section class="qa-section" id="q-301-s-04" data-answer-section="4"><h3><span>4.</span> Evidence supplied by the log</h3>
<span class="qa-anchor" id="q-301-a-10"></span><p>A successful CQE does not require a new Error Information entry. <a class="qa-rule-link" href="#common-command-10">Read the complete conditions in this volume</a></p>
</section>
</div>
<span class="qa-anchor" id="q-301-a-08"></span><span class="qa-anchor" id="q-301-a-09"></span><span class="qa-anchor" id="q-301-a-11"></span><span class="qa-anchor" id="q-301-a-12"></span><span class="qa-anchor" id="q-301-a-13"></span><span class="qa-anchor" id="q-301-a-14"></span><span class="qa-anchor" id="q-301-a-15"></span>
<p class="qa-related">Related mechanisms: <a href="/nvme/question-bank/errors/en/#q-099">Q99</a> · <a href="/nvme/question-bank/errors/en/#q-103">Q103</a></p>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-302" data-question="302" data-answer-kind="diagnose"><h2><a class="qa-qid" href="#q-302">Q302</a> When do differing CQE, Error Information and PEL records conflict?</h2>
<p class="qa-prompt">Separate available evidence from missing information before judging conformance.</p>
<details class="qa-answer" id="q-302-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-302-a-01">The three records have different purposes and timing, not bytewise equivalence.</p><div class="qa-sections">
<section class="qa-section" id="q-302-s-01" data-answer-section="1"><h3><span>1.</span> Preserve the evidence first</h3>
<span class="qa-anchor" id="q-302-a-02"></span><p>CQEs describe commands, error entries add failure details and PEL describes persistent events.</p>
<span class="qa-anchor" id="q-302-a-03"></span><p>Verify event support, More and command identity before correlating.</p>
<span class="qa-anchor" id="q-302-a-04"></span><p>Matching error status bits 15:1 match CQE status; phase follows its separate rule.</p>
</section>
<section class="qa-section" id="q-302-s-02" data-answer-section="2"><h3><span>2.</span> Work through the possible causes</h3>
<span class="qa-anchor" id="q-302-a-17"></span><p>First establish what each record actually proves.</p>
<span class="qa-anchor" id="q-302-a-05"></span><p>Correlate identity/time before parsing event-specific outcome fields.</p>
</section>
<section class="qa-section" id="q-302-s-03" data-answer-section="3"><h3><span>3.</span> Decide what the evidence supports</h3>
<span class="qa-anchor" id="q-302-a-06"></span><p>Successful sanitize acceptance and later operation failure can both be correct.</p>
<span class="qa-anchor" id="q-302-a-07"></span><p>Reused CIDs and requested-versus-completed values can create false contradictions.</p>
<span class="qa-anchor" id="q-302-a-16"></span><p>Build an acceptance/start/operation-completion/query timeline.</p>
</section>
</div>
<span class="qa-anchor" id="q-302-a-08"></span><span class="qa-anchor" id="q-302-a-09"></span><span class="qa-anchor" id="q-302-a-10"></span><span class="qa-anchor" id="q-302-a-11"></span><span class="qa-anchor" id="q-302-a-12"></span><span class="qa-anchor" id="q-302-a-13"></span><span class="qa-anchor" id="q-302-a-14"></span><span class="qa-anchor" id="q-302-a-15"></span>
<p class="qa-related">Related mechanisms: <a href="/nvme/question-bank/errors/en/#q-100">Q100</a> · <a href="/nvme/question-bank/errors/en/#q-101">Q101</a> · <a href="/nvme/question-bank/errors/en/#q-106">Q106</a> · <a href="/nvme/question-bank/persistent-events/en/#q-213">Q213</a></p>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-pelcontext">Base 2.4 §5.2.13.1.14–5.2.13.1.14.2.5 (exclude PCIe link/packet decoding)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-303" data-question="303" data-answer-kind="lifecycle"><h2><a class="qa-qid" href="#q-303">Q303</a> How are unexpected feature retention or lost saved values assessed?</h2>
<p class="qa-prompt">Name the reset or interruption, then assess settings, ongoing operations and data separately.</p>
<details class="qa-answer" id="q-303-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-303-a-01">Non-saveable does not mean nonpersistent, and unsaved current values need not survive power loss.</p><div class="qa-sections">
<section class="qa-section" id="q-303-s-01" data-answer-section="1"><h3><span>1.</span> Identify the trigger and affected objects</h3>
<span class="qa-anchor" id="q-303-a-02"></span><p>Compare feature scope with actual reset coverage.</p>
<span class="qa-anchor" id="q-303-a-03"></span><p>Preserve capabilities, value classes and the last successful Set’s save bit.</p>
</section>
<section class="qa-section" id="q-303-s-02" data-answer-section="2"><h3><span>2.</span> State changes and recovery</h3>
<span class="qa-anchor" id="q-303-a-04"></span><p>Namespace write protection has explicit retention despite being non-saveable.</p>
<span class="qa-anchor" id="q-303-a-05"></span><p>Establish known saved state, apply a specific reset and requery the same target.</p>
<span class="qa-anchor" id="q-303-a-06"></span><p>Pass criteria follow restoration rules and explicit exceptions, not universal zeroing.</p>
</section>
<section class="qa-section" id="q-303-s-03" data-answer-section="3"><h3><span>3.</span> Verify retention and recovery</h3>
<span class="qa-anchor" id="q-303-a-07"></span><p>Failed saves or intervening changes invalidate a simple lost-save diagnosis.</p>
<span class="qa-anchor" id="q-303-a-16"></span><p>Record saveability, persistence, reset source and coverage separately.</p>
<span class="qa-anchor" id="q-303-a-17"></span><p>First check the successful save and feature-specific exceptions.</p>
</section>
</div>
<span class="qa-anchor" id="q-303-a-08"></span><span class="qa-anchor" id="q-303-a-09"></span><span class="qa-anchor" id="q-303-a-10"></span><span class="qa-anchor" id="q-303-a-11"></span><span class="qa-anchor" id="q-303-a-12"></span><span class="qa-anchor" id="q-303-a-13"></span><span class="qa-anchor" id="q-303-a-14"></span><span class="qa-anchor" id="q-303-a-15"></span>
<p class="qa-related">Related mechanisms: <a href="/nvme/question-bank/features/en/#q-055">Q55</a> · <a href="/nvme/question-bank/features/en/#q-067">Q67</a> · <a href="/nvme/question-bank/integration/en/#q-318">Q318</a></p>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-304" data-question="304" data-answer-kind="diagnose"><h2><a class="qa-qid" href="#q-304">Q304</a> How are namespace changes reconciled across Identify, lists and AER?</h2>
<p class="qa-prompt">Separate available evidence from missing information before judging conformance.</p>
<details class="qa-answer" id="q-304-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-304-a-01">Identify exposes current configuration, the changed list identifies changes and AER prompts rediscovery.</p><div class="qa-sections">
<section class="qa-section" id="q-304-s-01" data-answer-section="1"><h3><span>1.</span> Preserve the evidence first</h3>
<span class="qa-anchor" id="q-304-a-02"></span><p>Controllers can observe different changes according to attachment and notification rules.</p>
<span class="qa-anchor" id="q-304-a-03"></span><p>Record support/enables, pending requests and before/after inventories.</p>
<span class="qa-anchor" id="q-304-a-04"></span><p>Attachment changes active inventory while creation changes allocated inventory.</p>
</section>
<section class="qa-section" id="q-304-s-02" data-answer-section="2"><h3><span>2.</span> Work through the possible causes</h3>
<span class="qa-anchor" id="q-304-a-17"></span><p>First identify the management operation class.</p>
<span class="qa-anchor" id="q-304-a-05"></span><p>Perform one operation, observe completion/notice and rediscover current state.</p>
</section>
<section class="qa-section" id="q-304-s-03" data-answer-section="3"><h3><span>3.</span> Decide what the evidence supports</h3>
<span class="qa-anchor" id="q-304-a-06"></span><p>A changed NSID need not still exist because deletion also requires rediscovery.</p>
<span class="qa-anchor" id="q-304-a-07"></span><p>Overflow uses FFFFFFFFh and requires full rediscovery, not treating it as a real namespace.</p>
<span class="qa-anchor" id="q-304-a-16"></span><p>Preserve the first list and distinguish the initiating endpoint from notified peers.</p>
</section>
</div>
<span class="qa-anchor" id="q-304-a-08"></span><span class="qa-anchor" id="q-304-a-09"></span><span class="qa-anchor" id="q-304-a-10"></span><span class="qa-anchor" id="q-304-a-11"></span><span class="qa-anchor" id="q-304-a-12"></span><span class="qa-anchor" id="q-304-a-13"></span><span class="qa-anchor" id="q-304-a-14"></span><span class="qa-anchor" id="q-304-a-15"></span>
<p class="qa-related">Related mechanisms: <a href="/nvme/question-bank/namespace-management/en/#q-160">Q160</a> · <a href="/nvme/question-bank/namespace-management/en/#q-162">Q162</a> · <a href="/nvme/question-bank/namespace-management/en/#q-167">Q167</a> · <a href="/nvme/question-bank/namespace-management/en/#q-168">Q168</a></p>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-nsattach">Base 2.4 §5.2.24–5.2.25, 8.1.17–8.1.17.2</a> · <a href="#ref-changedlog">Base 2.4 §5.2.13.1.5</a> · <a href="#ref-aerfull">Base 2.4 §5.2.2 (PCIe-applicable events)</a> · <a href="#ref-nspelevent">Base 2.4 §5.2.13.1.14.2.6</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-305" data-question="305" data-answer-kind="diagnose"><h2><a class="qa-qid" href="#q-305">Q305</a> How are unchanged firmware revision or slot fields assessed after activation?</h2>
<p class="qa-prompt">Separate available evidence from missing information before judging conformance.</p>
<details class="qa-answer" id="q-305-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-305-a-01">Download, slot commit, scheduled activation and actual activation are distinct stages.</p><div class="qa-sections">
<section class="qa-section" id="q-305-s-01" data-answer-section="1"><h3><span>1.</span> Preserve the evidence first</h3>
<span class="qa-anchor" id="q-305-a-02"></span><p>Slot/activation state may be shared within a domain.</p>
<span class="qa-anchor" id="q-305-a-03"></span><p>Inspect capability, current/next active slots, slot revisions and current firmware revision.</p>
<span class="qa-anchor" id="q-305-a-04"></span><p>Preserve action/slot/status and execute the specifically required activation reset.</p>
</section>
<section class="qa-section" id="q-305-s-02" data-answer-section="2"><h3><span>2.</span> Work through the possible causes</h3>
<span class="qa-anchor" id="q-305-a-17"></span><p>First verify action and activation mechanism.</p>
<span class="qa-anchor" id="q-305-a-05"></span><p>Verify commit, perform activation and rediscover current state.</p>
</section>
<section class="qa-section" id="q-305-s-03" data-answer-section="3"><h3><span>3.</span> Decide what the evidence supports</h3>
<span class="qa-anchor" id="q-305-a-06"></span><p>Equal version strings do not alone prove activation failure.</p>
<span class="qa-anchor" id="q-305-a-07"></span><p>Fallback and requested PEL revision are not proof of active new firmware.</p>
<span class="qa-anchor" id="q-305-a-16"></span><p>Reconcile pending/active slot, current revision and commit/reset events separately.</p>
</section>
</div>
<span class="qa-anchor" id="q-305-a-08"></span><span class="qa-anchor" id="q-305-a-09"></span><span class="qa-anchor" id="q-305-a-10"></span><span class="qa-anchor" id="q-305-a-11"></span><span class="qa-anchor" id="q-305-a-12"></span><span class="qa-anchor" id="q-305-a-13"></span><span class="qa-anchor" id="q-305-a-14"></span><span class="qa-anchor" id="q-305-a-15"></span>
<p class="qa-related">Related mechanisms: <a href="/nvme/question-bank/firmware-boot/en/#q-139">Q139</a> · <a href="/nvme/question-bank/firmware-boot/en/#q-140">Q140</a> · <a href="/nvme/question-bank/firmware-boot/en/#q-144">Q144</a></p>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-firmware">Base 2.4 §3.11–3.11.1, 5.2.9–5.2.10</a> · <a href="#ref-fwlog">Base 2.4 §5.2.13.1.4</a> · <a href="#ref-fwpel">Base 2.4 §5.2.13.1.14.2.2, 5.2.13.1.14.2.4</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-306" data-question="306" data-answer-kind="diagnose"><h2><a class="qa-qid" href="#q-306">Q306</a> Is an in-progress log after sanitize command success an error?</h2>
<p class="qa-prompt">Separate available evidence from missing information before judging conformance.</p>
<details class="qa-answer" id="q-306-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-306-a-01">Sanitize command completion acknowledges initiation, while media sanitization can continue in the background.</p><div class="qa-sections">
<section class="qa-section" id="q-306-s-01" data-answer-section="1"><h3><span>1.</span> Preserve the evidence first</h3>
<span class="qa-anchor" id="q-306-a-02"></span><p>Match subsystem or namespace scope and result selection.</p>
<span class="qa-anchor" id="q-306-a-03"></span><p>Inspect capabilities, command scope, status and supported completion events.</p>
<span class="qa-anchor" id="q-306-a-04"></span><p>Interpret progress with operation and verification state, not FFFFh alone.</p>
</section>
<section class="qa-section" id="q-306-s-02" data-answer-section="2"><h3><span>2.</span> Work through the possible causes</h3>
<span class="qa-anchor" id="q-306-a-17"></span><p>First identify what the claimed completion actually establishes.</p>
<span class="qa-anchor" id="q-306-a-05"></span><p>Preserve initiation completion and poll state, then correlate final result with any completion event.</p>
</section>
<section class="qa-section" id="q-306-s-03" data-answer-section="3"><h3><span>3.</span> Decide what the evidence supports</h3>
<span class="qa-anchor" id="q-306-a-06"></span><p>In-progress after initiation is normal; final state must follow actual operation completion.</p>
<span class="qa-anchor" id="q-306-a-07"></span><p>Exclude a newer operation, wrong scope and stale data before diagnosing a stuck status.</p>
<span class="qa-anchor" id="q-306-a-16"></span><p>Correlate one operation across command, log, AER and PEL.</p>
</section>
</div>
<span class="qa-anchor" id="q-306-a-08"></span><span class="qa-anchor" id="q-306-a-09"></span><span class="qa-anchor" id="q-306-a-10"></span><span class="qa-anchor" id="q-306-a-11"></span><span class="qa-anchor" id="q-306-a-12"></span><span class="qa-anchor" id="q-306-a-13"></span><span class="qa-anchor" id="q-306-a-14"></span><span class="qa-anchor" id="q-306-a-15"></span>
<p class="qa-related">Related mechanisms: <a href="/nvme/question-bank/format-sanitize/en/#q-128">Q128</a> · <a href="/nvme/question-bank/format-sanitize/en/#q-130">Q130</a> · <a href="/nvme/question-bank/format-sanitize/en/#q-131">Q131</a> · <a href="/nvme/question-bank/format-sanitize/en/#q-133">Q133</a></p>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-sanitizecmd">Base 2.4 §5.2.26–5.2.27</a> · <a href="#ref-sanitizelog">Base 2.4 §5.2.13.1.38</a> · <a href="#ref-sanitizestate">Base 2.4 §8.1.27.1–8.1.27.5</a> · <a href="#ref-sanitizepel">Base 2.4 §5.2.13.1.14.2.9–5.2.13.1.14.2.10</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-307" data-question="307" data-answer-kind="diagnose"><h2><a class="qa-qid" href="#q-307">Q307</a> How is a missing result after self-test investigated?</h2>
<p class="qa-prompt">Separate available evidence from missing information before judging conformance.</p>
<details class="qa-answer" id="q-307-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-307-a-01">Start-command success is not test success; current operation and result history establish the outcome.</p><div class="qa-sections">
<section class="qa-section" id="q-307-s-01" data-answer-section="1"><h3><span>1.</span> Preserve the evidence first</h3>
<span class="qa-anchor" id="q-307-a-02"></span><p>Match controller/shared-test scope and read the complete log correctly.</p>
<span class="qa-anchor" id="q-307-a-03"></span><p>Inspect support/options/time and LID 06h&#x27;s 20 newest-first result slots.</p>
<span class="qa-anchor" id="q-307-a-04"></span><p>Current state, progress, result code, test code and validity bits have distinct roles.</p>
</section>
<section class="qa-section" id="q-307-s-02" data-answer-section="2"><h3><span>2.</span> Work through the possible causes</h3>
<span class="qa-anchor" id="q-307-a-17"></span><p>First establish that a test actually started.</p>
<span class="qa-anchor" id="q-307-a-05"></span><p>Capture history, run one test and compare the newest result after completion.</p>
</section>
<section class="qa-section" id="q-307-s-03" data-answer-section="3"><h3><span>3.</span> Decide what the evidence supports</h3>
<span class="qa-anchor" id="q-307-a-06"></span><p>Result update and return to idle follow the specified ordering for a test that produces a result.</p>
<span class="qa-anchor" id="q-307-a-07"></span><p>An Abort while idle can succeed without creating a test result.</p>
<span class="qa-anchor" id="q-307-a-16"></span><p>Interpret reset effects using the distinct short/extended-test rules.</p>
</section>
</div>
<span class="qa-anchor" id="q-307-a-08"></span><span class="qa-anchor" id="q-307-a-09"></span><span class="qa-anchor" id="q-307-a-10"></span><span class="qa-anchor" id="q-307-a-11"></span><span class="qa-anchor" id="q-307-a-12"></span><span class="qa-anchor" id="q-307-a-13"></span><span class="qa-anchor" id="q-307-a-14"></span><span class="qa-anchor" id="q-307-a-15"></span>
<p class="qa-related">Related mechanisms: <a href="/nvme/question-bank/self-test/en/#q-152">Q152</a> · <a href="/nvme/question-bank/self-test/en/#q-153">Q153</a> · <a href="/nvme/question-bank/self-test/en/#q-155">Q155</a> · <a href="/nvme/question-bank/self-test/en/#q-156">Q156</a></p>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-selftest">Base 2.4 §5.2.6, 8.1.8</a> · <a href="#ref-dstlog">Base 2.4 §5.2.13.1.7</a> · <a href="#ref-nvmselftest">NVM Command Set 1.3 §4.1.4.3</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-308" data-question="308" data-answer-kind="diagnose"><h2><a class="qa-qid" href="#q-308">Q308</a> How are unexpected unsafe-shutdown counts assessed?</h2>
<p class="qa-prompt">Separate available evidence from missing information before judging conformance.</p>
<details class="qa-answer" id="q-308-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-308-a-01">Count behavior depends on state at main-power loss, not only the requested shutdown type.</p><div class="qa-sections">
<section class="qa-section" id="q-308-s-01" data-answer-section="1"><h3><span>1.</span> Preserve the evidence first</h3>
<span class="qa-anchor" id="q-308-a-02"></span><p>Base 2.4 UPL counts qualifying power losses, not host shutdown calls.</p>
<span class="qa-anchor" id="q-308-a-03"></span><p>Preserve count, request, status and actual power-loss time.</p>
<span class="qa-anchor" id="q-308-a-04"></span><p>Ordinary qualification concerns main-power loss before SHST10b, with a separate applicable out-of-band ignore-shutdown case.</p>
</section>
<section class="qa-section" id="q-308-s-02" data-answer-section="2"><h3><span>2.</span> Work through the possible causes</h3>
<span class="qa-anchor" id="q-308-a-17"></span><p>First establish actual main-power loss and SHST at that moment.</p>
<span class="qa-anchor" id="q-308-a-05"></span><p>Read baseline, request shutdown, observe status and compare after controlled power cycling.</p>
</section>
<section class="qa-section" id="q-308-s-03" data-answer-section="3"><h3><span>3.</span> Decide what the evidence supports</h3>
<span class="qa-anchor" id="q-308-a-06"></span><p>Abrupt shutdown can complete before power loss and need not increment UPL each time.</p>
<span class="qa-anchor" id="q-308-a-07"></span><p>Incomplete normal shutdown may qualify, while controller reset without power loss does not automatically count.</p>
<span class="qa-anchor" id="q-308-a-16"></span><p>Use pre-loss state rather than post-restart SHST.</p>
</section>
</div>
<span class="qa-anchor" id="q-308-a-08"></span><span class="qa-anchor" id="q-308-a-09"></span><span class="qa-anchor" id="q-308-a-10"></span><span class="qa-anchor" id="q-308-a-11"></span><span class="qa-anchor" id="q-308-a-12"></span><span class="qa-anchor" id="q-308-a-13"></span><span class="qa-anchor" id="q-308-a-14"></span><span class="qa-anchor" id="q-308-a-15"></span>
<p class="qa-related">Related mechanisms: <a href="/nvme/question-bank/reset-shutdown/en/#q-183">Q183</a> · <a href="/nvme/question-bank/reset-shutdown/en/#q-184">Q184</a> · <a href="/nvme/question-bank/reset-shutdown/en/#q-186">Q186</a> · <a href="/nvme/question-bank/health/en/#q-199">Q199</a></p>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-smart">Base 2.4 §5.2.13.1.3</a> · <a href="#ref-shutdownfull">Base 2.4 §3.6–3.6.1 (memory-based scope and shutdown)</a> · <a href="#ref-pciereset">PCIe Transport 1.4 §3.3</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-309" data-question="309" data-answer-kind="diagnose"><h2><a class="qa-qid" href="#q-309">Q309</a> Which settings explain a warning change without an AER?</h2>
<p class="qa-prompt">Separate available evidence from missing information before judging conformance.</p>
<details class="qa-answer" id="q-309-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-309-a-01">State transitions and event conditions differ; clearing a warning need not mirror assertion.</p><div class="qa-sections">
<section class="qa-section" id="q-309-s-01" data-answer-section="1"><h3><span>1.</span> Preserve the evidence first</h3>
<span class="qa-anchor" id="q-309-a-02"></span><p>Aggregate and group-specific warnings use different scopes/settings.</p>
<span class="qa-anchor" id="q-309-a-03"></span><p>Check support/enables, pending AERs and unacknowledged prior events.</p>
<span class="qa-anchor" id="q-309-a-04"></span><p>Preserve warning bits, measured values and thresholds rather than only UI labels.</p>
</section>
<section class="qa-section" id="q-309-s-02" data-answer-section="2"><h3><span>2.</span> Work through the possible causes</h3>
<span class="qa-anchor" id="q-309-a-17"></span><p>First verify AEC at event time.</p>
<span class="qa-anchor" id="q-309-a-05"></span><p>Verify qualifying conditions, competing/coalesced events and acknowledgment reads.</p>
</section>
<section class="qa-section" id="q-309-s-03" data-answer-section="3"><h3><span>3.</span> Decide what the evidence supports</h3>
<span class="qa-anchor" id="q-309-a-06"></span><p>Qualifying enabled events follow their queuing rules, not one AER per sampled fluctuation.</p>
<span class="qa-anchor" id="q-309-a-07"></span><p>No pending request means no immediate CQE; unconsumed completions are not missing notifications.</p>
<span class="qa-anchor" id="q-309-a-16"></span><p>Correlate warning, configuration, requests and acknowledgments.</p>
</section>
</div>
<span class="qa-anchor" id="q-309-a-08"></span><span class="qa-anchor" id="q-309-a-09"></span><span class="qa-anchor" id="q-309-a-10"></span><span class="qa-anchor" id="q-309-a-11"></span><span class="qa-anchor" id="q-309-a-12"></span><span class="qa-anchor" id="q-309-a-13"></span><span class="qa-anchor" id="q-309-a-14"></span><span class="qa-anchor" id="q-309-a-15"></span>
<p class="qa-related">Related mechanisms: <a href="/nvme/question-bank/features/en/#q-061">Q61</a> · <a href="/nvme/question-bank/asynchronous-events/en/#q-088">Q88</a> · <a href="/nvme/question-bank/health/en/#q-196">Q196</a> · <a href="/nvme/question-bank/health/en/#q-202">Q202</a></p>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-smart">Base 2.4 §5.2.13.1.3</a> · <a href="#ref-aerfull">Base 2.4 §5.2.2 (PCIe-applicable events)</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-310" data-question="310" data-answer-kind="diagnose"><h2><a class="qa-qid" href="#q-310">Q310</a> How is apparent PEL event-order mismatch investigated?</h2>
<p class="qa-prompt">Separate available evidence from missing information before judging conformance.</p>
<details class="qa-answer" id="q-310-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-310-a-01">Log order, event timestamp and real operation order are distinct.</p><div class="qa-sections">
<section class="qa-section" id="q-310-s-01" data-answer-section="1"><h3><span>1.</span> Preserve the evidence first</h3>
<span class="qa-anchor" id="q-310-a-02"></span><p>Subsystem PEL can interleave controllers and permits defined vendor ordering.</p>
<span class="qa-anchor" id="q-310-a-03"></span><p>Inspect reporting context, generation and clock origin/synchronization.</p>
<span class="qa-anchor" id="q-310-a-04"></span><p>Host changes and restoration can move timestamps, so they are not universal monotonic sequence numbers.</p>
</section>
<section class="qa-section" id="q-310-s-02" data-answer-section="2"><h3><span>2.</span> Work through the possible causes</h3>
<span class="qa-anchor" id="q-310-a-17"></span><p>First verify context and event boundaries.</p>
<span class="qa-anchor" id="q-310-a-05"></span><p>Read one consistent context, parse lengths and account for clock-change/reset events.</p>
</section>
<section class="qa-section" id="q-310-s-03" data-answer-section="3"><h3><span>3.</span> Decide what the evidence supports</h3>
<span class="qa-anchor" id="q-310-a-06"></span><p>Newest-first is recommended with vendor-defined ordering allowed, not an unconditional mandate.</p>
<span class="qa-anchor" id="q-310-a-07"></span><p>Mixed contexts and incorrect event-length accounting can create false disorder.</p>
<span class="qa-anchor" id="q-310-a-16"></span><p>Use a host monotonic timeline as evidence without equating unsynchronized clocks.</p>
</section>
</div>
<span class="qa-anchor" id="q-310-a-08"></span><span class="qa-anchor" id="q-310-a-09"></span><span class="qa-anchor" id="q-310-a-10"></span><span class="qa-anchor" id="q-310-a-11"></span><span class="qa-anchor" id="q-310-a-12"></span><span class="qa-anchor" id="q-310-a-13"></span><span class="qa-anchor" id="q-310-a-14"></span><span class="qa-anchor" id="q-310-a-15"></span>
<p class="qa-related">Related mechanisms: <a href="/nvme/question-bank/persistent-events/en/#q-213">Q213</a> · <a href="/nvme/question-bank/persistent-events/en/#q-214">Q214</a> · <a href="/nvme/question-bank/persistent-events/en/#q-215">Q215</a> · <a href="/nvme/question-bank/persistent-events/en/#q-216">Q216</a></p>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-pelcontext">Base 2.4 §5.2.13.1.14–5.2.13.1.14.2.5 (exclude PCIe link/packet decoding)</a> · <a href="#ref-nvmpel">NVM Command Set 1.3 §4.1.4.4</a> · <a href="#ref-timestamp">Base 2.4 §5.2.30.1.8</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-311" data-question="311" data-answer-kind="diagnose"><h2><a class="qa-qid" href="#q-311">Q311</a> What evidence remains when CFS is set with little diagnostic information?</h2>
<p class="qa-prompt">Separate available evidence from missing information before judging conformance.</p>
<details class="qa-answer" id="q-311-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-311-a-01">Fatal conditions may break diagnostics; absent logs do not invalidate CFS or justify unlimited further commands.</p><div class="qa-sections">
<section class="qa-section" id="q-311-s-01" data-answer-section="1"><h3><span>1.</span> Preserve the evidence first</h3>
<span class="qa-anchor" id="q-311-a-02"></span><p>Distinguish fatal failure from a secondary controller’s Offline state.</p>
<span class="qa-anchor" id="q-311-a-03"></span><p>Preserve accessible controller state, capabilities and recent management history.</p>
<span class="qa-anchor" id="q-311-a-04"></span><p>Obtain available diagnostics without assuming every CFS cause has a readable dedicated record.</p>
</section>
<section class="qa-section" id="q-311-s-02" data-answer-section="2"><h3><span>2.</span> Work through the possible causes</h3>
<span class="qa-anchor" id="q-311-a-17"></span><p>First establish role and register-read validity.</p>
<span class="qa-anchor" id="q-311-a-05"></span><p>Preserve evidence before reset/recovery, then query surviving records.</p>
</section>
<section class="qa-section" id="q-311-s-03" data-answer-section="3"><h3><span>3.</span> Decide what the evidence supports</h3>
<span class="qa-anchor" id="q-311-a-06"></span><p>Reinitialize and verify recovery while retaining uncertainty about interrupted commands.</p>
<span class="qa-anchor" id="q-311-a-07"></span><p>Unreliable/all-ones reads are not automatically valid NVMe state.</p>
<span class="qa-anchor" id="q-311-a-16"></span><p>Separate device status, host timeout and communication-failure evidence.</p>
</section>
</div>
<span class="qa-anchor" id="q-311-a-08"></span><span class="qa-anchor" id="q-311-a-09"></span><span class="qa-anchor" id="q-311-a-10"></span><span class="qa-anchor" id="q-311-a-11"></span><span class="qa-anchor" id="q-311-a-12"></span><span class="qa-anchor" id="q-311-a-13"></span><span class="qa-anchor" id="q-311-a-14"></span><span class="qa-anchor" id="q-311-a-15"></span>
<p class="qa-related">Related mechanisms: <a href="/nvme/question-bank/initialization/en/#q-006">Q6</a> · <a href="/nvme/question-bank/errors/en/#q-105">Q105</a> · <a href="/nvme/question-bank/recovery/en/#q-117">Q117</a></p>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-cc">Base 2.4 §3.1.4 (CC, CSTS, NSSR)</a> · <a href="#ref-ready">Base 2.4 §3.5.3–3.5.4</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-smart">Base 2.4 §5.2.13.1.3</a> · <a href="#ref-pelcontext">Base 2.4 §5.2.13.1.14–5.2.13.1.14.2.5 (exclude PCIe link/packet decoding)</a> · <a href="#ref-virtual">Base 2.4 §8.2.7</a> · <a href="#ref-commrecovery">Base 2.4 §9.1–9.6.2.1 (PCIe-applicable rules; stop before 9.6.2.2)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-312" data-question="312" data-answer-kind="diagnose"><h2><a class="qa-qid" href="#q-312">Q312</a> How are two observed completions after Abort classified?</h2>
<p class="qa-prompt">Separate available evidence from missing information before judging conformance.</p>
<details class="qa-answer" id="q-312-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-312-a-01">Abort and its target each complete; two total CQEs can be normal, unlike duplicate target completion.</p><div class="qa-sections">
<section class="qa-section" id="q-312-s-01" data-answer-section="1"><h3><span>1.</span> Preserve the evidence first</h3>
<span class="qa-anchor" id="q-312-a-02"></span><p>Identify commands by endpoint, SQID/CID and queue lifetime.</p>
<span class="qa-anchor" id="q-312-a-03"></span><p>Record target identity, Abort’s own identity and IANP.</p>
<span class="qa-anchor" id="q-312-a-04"></span><p>IANP semantics do not erase the target’s completion, and IANP1 permits later normal completion.</p>
</section>
<section class="qa-section" id="q-312-s-02" data-answer-section="2"><h3><span>2.</span> Work through the possible causes</h3>
<span class="qa-anchor" id="q-312-a-17"></span><p>First identify which completion belongs to Abort itself.</p>
<span class="qa-anchor" id="q-312-a-05"></span><p>Separate Abort and target CQEs, then exclude host double-consumption.</p>
</section>
<section class="qa-section" id="q-312-s-03" data-answer-section="3"><h3><span>3.</span> Decide what the evidence supports</h3>
<span class="qa-anchor" id="q-312-a-06"></span><p>Handle one completion for each command without assuming the target had no effects.</p>
<span class="qa-anchor" id="q-312-a-07"></span><p>Two genuine completions for the same target in one lifetime violate single-completion tracking.</p>
<span class="qa-anchor" id="q-312-a-16"></span><p>Exclude CID reuse and CQ wrap before declaring duplicates.</p>
</section>
</div>
<span class="qa-anchor" id="q-312-a-08"></span><span class="qa-anchor" id="q-312-a-09"></span><span class="qa-anchor" id="q-312-a-10"></span><span class="qa-anchor" id="q-312-a-11"></span><span class="qa-anchor" id="q-312-a-12"></span><span class="qa-anchor" id="q-312-a-13"></span><span class="qa-anchor" id="q-312-a-14"></span><span class="qa-anchor" id="q-312-a-15"></span>
<p class="qa-related">Related mechanisms: <a href="/nvme/question-bank/recovery/en/#q-107">Q107</a> · <a href="/nvme/question-bank/recovery/en/#q-110">Q110</a> · <a href="/nvme/question-bank/recovery/en/#q-112">Q112</a></p>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-abort">Base 2.4 §5.2.1</a> · <a href="#ref-cqe">Base 2.4 §4.2.1, 4.2.3–4.2.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-313" data-question="313" data-answer-kind="diagnose"><h2><a class="qa-qid" href="#q-313">Q313</a> What is wrong with queue-memory access after completed deletion?</h2>
<p class="qa-prompt">Separate available evidence from missing information before judging conformance.</p>
<details class="qa-answer" id="q-313-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-313-a-01">Access after the queue lifetime can corrupt memory already reused elsewhere.</p><div class="qa-sections">
<section class="qa-section" id="q-313-s-01" data-answer-section="1"><h3><span>1.</span> Preserve the evidence first</h3>
<span class="qa-anchor" id="q-313-a-02"></span><p>Distinguish deleted queue memory from buffers belonging to other live commands.</p>
<span class="qa-anchor" id="q-313-a-03"></span><p>Preserve target QID, successful deletion completion and memory range.</p>
<span class="qa-anchor" id="q-313-a-04"></span><p>Submission is not successful deletion, and SQ/CQ dependencies differ.</p>
</section>
<section class="qa-section" id="q-313-s-02" data-answer-section="2"><h3><span>2.</span> Work through the possible causes</h3>
<span class="qa-anchor" id="q-313-a-17"></span><p>First establish successful deletion completion.</p>
<span class="qa-anchor" id="q-313-a-05"></span><p>Check accesses after success and exclude legitimate address reuse by another queue.</p>
</section>
<section class="qa-section" id="q-313-s-03" data-answer-section="3"><h3><span>3.</span> Decide what the evidence supports</h3>
<span class="qa-anchor" id="q-313-a-06"></span><p>After retirement, the controller must not continue using it as the deleted queue.</p>
<span class="qa-anchor" id="q-313-a-07"></span><p>Such access can corrupt host data or produce invalid command/completion behavior.</p>
<span class="qa-anchor" id="q-313-a-16"></span><p>Preserve reuse timing and queue identities; address equality alone is insufficient.</p>
</section>
</div>
<span class="qa-anchor" id="q-313-a-08"></span><span class="qa-anchor" id="q-313-a-09"></span><span class="qa-anchor" id="q-313-a-10"></span><span class="qa-anchor" id="q-313-a-11"></span><span class="qa-anchor" id="q-313-a-12"></span><span class="qa-anchor" id="q-313-a-13"></span><span class="qa-anchor" id="q-313-a-14"></span><span class="qa-anchor" id="q-313-a-15"></span>
<p class="qa-related">Related mechanisms: <a href="/nvme/question-bank/queues/en/#q-019">Q19</a> · <a href="/nvme/question-bank/memory/en/#q-227">Q227</a> · <a href="/nvme/question-bank/interrupts/en/#q-295">Q295</a></p>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-delete">Base 2.4 §5.3.3–5.3.4</a> · <a href="#ref-create">Base 2.4 §5.3.1–5.3.2</a> · <a href="#ref-retirement">PCIe Transport 1.4 §3.4 (Command Related Resource Retirement)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-314" data-question="314" data-answer-kind="diagnose"><h2><a class="qa-qid" href="#q-314">Q314</a> How should a CQE from before reset be handled?</h2>
<p class="qa-prompt">Separate available evidence from missing information before judging conformance.</p>
<details class="qa-answer" id="q-314-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-314-a-01">Residual memory differs from a newly posted stale completion after reset.</p><div class="qa-sections">
<section class="qa-section" id="q-314-s-01" data-answer-section="1"><h3><span>1.</span> Preserve the evidence first</h3>
<span class="qa-anchor" id="q-314-a-02"></span><p>Reset ends old queue lifetimes even when addresses and identifiers are reused.</p>
<span class="qa-anchor" id="q-314-a-03"></span><p>Inspect reset source, readiness transitions, CQ initialization and expected phase.</p>
<span class="qa-anchor" id="q-314-a-04"></span><p>Rebuild command tracking without associating an old CID with a new request.</p>
</section>
<section class="qa-section" id="q-314-s-02" data-answer-section="2"><h3><span>2.</span> Work through the possible causes</h3>
<span class="qa-anchor" id="q-314-a-17"></span><p>First verify phase and command-tracking initialization.</p>
<span class="qa-anchor" id="q-314-a-05"></span><p>Finish reset and initialize memory before accepting valid new-lifetime completions.</p>
</section>
<section class="qa-section" id="q-314-s-03" data-answer-section="3"><h3><span>3.</span> Decide what the evidence supports</h3>
<span class="qa-anchor" id="q-314-a-06"></span><p>Ignore stale completions while separately resolving possible prior media effects.</p>
<span class="qa-anchor" id="q-314-a-07"></span><p>New writes to a retired queue require investigation, unlike passive residual bytes.</p>
<span class="qa-anchor" id="q-314-a-16"></span><p>Correlate initialization and write timing to distinguish stale storage from late access.</p>
</section>
</div>
<span class="qa-anchor" id="q-314-a-08"></span><span class="qa-anchor" id="q-314-a-09"></span><span class="qa-anchor" id="q-314-a-10"></span><span class="qa-anchor" id="q-314-a-11"></span><span class="qa-anchor" id="q-314-a-12"></span><span class="qa-anchor" id="q-314-a-13"></span><span class="qa-anchor" id="q-314-a-14"></span><span class="qa-anchor" id="q-314-a-15"></span>
<p class="qa-related">Related mechanisms: <a href="/nvme/question-bank/initialization/en/#q-009">Q9</a> · <a href="/nvme/question-bank/queues/en/#q-021">Q21</a> · <a href="/nvme/question-bank/recovery/en/#q-115">Q115</a> · <a href="/nvme/question-bank/reset-shutdown/en/#q-179">Q179</a></p>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-cqe">Base 2.4 §4.2.1, 4.2.3–4.2.4</a> · <a href="#ref-pciereset">PCIe Transport 1.4 §3.3</a> · <a href="#ref-commrecovery">Base 2.4 §9.1–9.6.2.1 (PCIe-applicable rules; stop before 9.6.2.2)</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-315" data-question="315" data-answer-kind="diagnose"><h2><a class="qa-qid" href="#q-315">Q315</a> When can command success after detach be reasonable?</h2>
<p class="qa-prompt">Separate available evidence from missing information before judging conformance.</p>
<details class="qa-answer" id="q-315-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-315-a-01">Submission acceptance is not successful execution, and some queries can address allocated inactive namespaces.</p><div class="qa-sections">
<section class="qa-section" id="q-315-s-01" data-answer-section="1"><h3><span>1.</span> Preserve the evidence first</h3>
<span class="qa-anchor" id="q-315-a-02"></span><p>Detach affects selected endpoints, not every attached path.</p>
<span class="qa-anchor" id="q-315-a-03"></span><p>Verify completed detach through both views.</p>
<span class="qa-anchor" id="q-315-a-04"></span><p>Distinguish ordinary I/O from allocated-namespace queries and special management commands.</p>
</section>
<section class="qa-section" id="q-315-s-02" data-answer-section="2"><h3><span>2.</span> Work through the possible causes</h3>
<span class="qa-anchor" id="q-315-a-17"></span><p>First check endpoint and active-namespace requirement.</p>
<span class="qa-anchor" id="q-315-a-05"></span><p>Submit a new command after successful detach on the detached endpoint.</p>
</section>
<section class="qa-section" id="q-315-s-03" data-answer-section="3"><h3><span>3.</span> Decide what the evidence supports</h3>
<span class="qa-anchor" id="q-315-a-06"></span><p>Success on another attached path or an allowed allocated query can be normal.</p>
<span class="qa-anchor" id="q-315-a-07"></span><p>Applicable inactive-namespace commands require Invalid Field absent an exception, distinct from invalid-NSID status.</p>
<span class="qa-anchor" id="q-315-a-16"></span><p>Separate outstanding and newly submitted commands when assessing detach effects.</p>
</section>
</div>
<span class="qa-anchor" id="q-315-a-08"></span><span class="qa-anchor" id="q-315-a-09"></span><span class="qa-anchor" id="q-315-a-10"></span><span class="qa-anchor" id="q-315-a-11"></span><span class="qa-anchor" id="q-315-a-12"></span><span class="qa-anchor" id="q-315-a-13"></span><span class="qa-anchor" id="q-315-a-14"></span><span class="qa-anchor" id="q-315-a-15"></span>
<p class="qa-related">Related mechanisms: <a href="/nvme/question-bank/namespace-management/en/#q-164">Q164</a> · <a href="/nvme/question-bank/namespace-management/en/#q-165">Q165</a></p>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-nsattach">Base 2.4 §5.2.24–5.2.25, 8.1.17–8.1.17.2</a> · <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-316" data-question="316" data-answer-kind="diagnose"><h2><a class="qa-qid" href="#q-316">Q316</a> How is apparent Lockdown bypass investigated?</h2>
<p class="qa-prompt">Separate available evidence from missing information before judging conformance.</p>
<details class="qa-answer" id="q-316-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-316-a-01">A prohibition matches interface, controller scope and command/feature target together.</p><div class="qa-sections">
<section class="qa-section" id="q-316-s-01" data-answer-section="1"><h3><span>1.</span> Preserve the evidence first</h3>
<span class="qa-anchor" id="q-316-a-02"></span><p>Scope selectors jointly define the target, not opcode alone.</p>
<span class="qa-anchor" id="q-316-a-03"></span><p>Read supported/current prohibitions under matching selectors.</p>
<span class="qa-anchor" id="q-316-a-04"></span><p>Feature scope prohibits Set, not automatically Get; enhanced aggregate ACNTL0 is not no prohibition.</p>
</section>
<section class="qa-section" id="q-316-s-02" data-answer-section="2"><h3><span>2.</span> Work through the possible causes</h3>
<span class="qa-anchor" id="q-316-a-17"></span><p>First inspect interface, controller scope and command-versus-feature selection.</p>
<span class="qa-anchor" id="q-316-a-05"></span><p>Test an exact matching target plus an allowed control after successful Lockdown.</p>
</section>
<section class="qa-section" id="q-316-s-03" data-answer-section="3"><h3><span>3.</span> Decide what the evidence supports</h3>
<span class="qa-anchor" id="q-316-a-06"></span><p>A prohibited matching Admin command requires 0/23h.</p>
<span class="qa-anchor" id="q-316-a-07"></span><p>Exclude expiry, later allowance, mismatched interfaces and explicit personality exceptions.</p>
<span class="qa-anchor" id="q-316-a-16"></span><p>Correlate configuration, inventory and behavior under identical selectors.</p>
</section>
</div>
<span class="qa-anchor" id="q-316-a-08"></span><span class="qa-anchor" id="q-316-a-09"></span><span class="qa-anchor" id="q-316-a-10"></span><span class="qa-anchor" id="q-316-a-11"></span><span class="qa-anchor" id="q-316-a-12"></span><span class="qa-anchor" id="q-316-a-13"></span><span class="qa-anchor" id="q-316-a-14"></span><span class="qa-anchor" id="q-316-a-15"></span>
<p class="qa-related">Related mechanisms: <a href="/nvme/question-bank/security/en/#q-242">Q242</a> · <a href="/nvme/question-bank/security/en/#q-243">Q243</a> · <a href="/nvme/question-bank/security/en/#q-244">Q244</a> · <a href="/nvme/question-bank/security/en/#q-245">Q245</a></p>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-lockdown">Base 2.4 §5.2.16, 8.1.5</a> · <a href="#ref-locklog">Base 2.4 §5.2.13.1.20</a> · <a href="#ref-lockpersist">Base 2.4 §5.2.30.1.25.4–5.2.30.1.25.4.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-317" data-question="317" data-answer-kind="diagnose"><h2><a class="qa-qid" href="#q-317">Q317</a> How is excessive power-state recovery latency measured correctly?</h2>
<p class="qa-prompt">Separate available evidence from missing information before judging conformance.</p>
<details class="qa-answer" id="q-317-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-317-a-01">Command latency includes exit, possible entry and execution, not only EXLAT.</p><div class="qa-sections">
<section class="qa-section" id="q-317-s-01" data-answer-section="1"><h3><span>1.</span> Preserve the evidence first</h3>
<span class="qa-anchor" id="q-317-a-02"></span><p>Establish source/target states and concurrent thermal constraints.</p>
<span class="qa-anchor" id="q-317-a-03"></span><p>Read state types, entry/exit latencies and selected policies.</p>
<span class="qa-anchor" id="q-317-a-04"></span><p>ITPT is idle time in milliseconds; entry/exit latencies are in microseconds.</p>
</section>
<section class="qa-section" id="q-317-s-02" data-answer-section="2"><h3><span>2.</span> Work through the possible causes</h3>
<span class="qa-anchor" id="q-317-a-17"></span><p>First verify units and timing origin.</p>
<span class="qa-anchor" id="q-317-a-05"></span><p>Separate idle, transition trigger, recovery and command execution timing.</p>
</section>
<section class="qa-section" id="q-317-s-03" data-answer-section="3"><h3><span>3.</span> Decide what the evidence supports</h3>
<span class="qa-anchor" id="q-317-a-06"></span><p>Assess relevant transitions rather than equating full read latency with EXLAT.</p>
<span class="qa-anchor" id="q-317-a-07"></span><p>CQE timing alone may not isolate an exit-latency violation.</p>
<span class="qa-anchor" id="q-317-a-16"></span><p>Compare an operational baseline with matching workload, temperature and settings.</p>
</section>
</div>
<span class="qa-anchor" id="q-317-a-08"></span><span class="qa-anchor" id="q-317-a-09"></span><span class="qa-anchor" id="q-317-a-10"></span><span class="qa-anchor" id="q-317-a-11"></span><span class="qa-anchor" id="q-317-a-12"></span><span class="qa-anchor" id="q-317-a-13"></span><span class="qa-anchor" id="q-317-a-14"></span><span class="qa-anchor" id="q-317-a-15"></span>
<p class="qa-related">Related mechanisms: <a href="/nvme/question-bank/health/en/#q-188">Q188</a> · <a href="/nvme/question-bank/health/en/#q-190">Q190</a> · <a href="/nvme/question-bank/health/en/#q-192">Q192</a> · <a href="/nvme/question-bank/health/en/#q-194">Q194</a></p>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-powerdetail">Base 2.4 §8.1.19.1–8.1.19.5</a> · <a href="#ref-psd">Base 2.4 §5.2.14.2.1 (Power State Descriptor)</a> · <a href="#ref-power">Base 2.4 §5.2.30.1.2, 5.2.30.1.7</a> · <a href="#ref-smart">Base 2.4 §5.2.13.1.3</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-318" data-question="318" data-answer-kind="lifecycle"><h2><a class="qa-qid" href="#q-318">Q318</a> How are three reset types compared for one feature?</h2>
<p class="qa-prompt">Name the reset or interruption, then assess settings, ongoing operations and data separately.</p>
<details class="qa-answer" id="q-318-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-318-a-01">Compare matched initial states under distinct reset mechanisms.</p><div class="qa-sections">
<section class="qa-section" id="q-318-s-01" data-answer-section="1"><h3><span>1.</span> Identify the trigger and affected objects</h3>
<span class="qa-anchor" id="q-318-a-02"></span><p>Reset coverage and persistence conditions differ across the three cases.</p>
<span class="qa-anchor" id="q-318-a-03"></span><p>Select one function and capture support, state and affected endpoints.</p>
</section>
<section class="qa-section" id="q-318-s-02" data-answer-section="2"><h3><span>2.</span> State changes and recovery</h3>
<span class="qa-anchor" id="q-318-a-04"></span><p>Track registers, queues, settings, ongoing operation and stored data separately.</p>
<span class="qa-anchor" id="q-318-a-05"></span><p>Reset from matched baselines and restore query access before comparison.</p>
<span class="qa-anchor" id="q-318-a-06"></span><p>Extended self-test persistence and I/O queue invalidation can coexist under CLR.</p>
</section>
<section class="qa-section" id="q-318-s-03" data-answer-section="3"><h3><span>3.</span> Verify retention and recovery</h3>
<span class="qa-anchor" id="q-318-a-07"></span><p>CC.EN-specific register exceptions do not cover all CLR, and subsystem reset is not factory restoration.</p>
<span class="qa-anchor" id="q-318-a-16"></span><p>Tie differences to explicit rules and retain limits where behavior is unspecified.</p>
<span class="qa-anchor" id="q-318-a-17"></span><p>First identify the actual reset trigger.</p>
</section>
</div>
<span class="qa-anchor" id="q-318-a-08"></span><span class="qa-anchor" id="q-318-a-09"></span><span class="qa-anchor" id="q-318-a-10"></span><span class="qa-anchor" id="q-318-a-11"></span><span class="qa-anchor" id="q-318-a-12"></span><span class="qa-anchor" id="q-318-a-13"></span><span class="qa-anchor" id="q-318-a-14"></span><span class="qa-anchor" id="q-318-a-15"></span>
<p class="qa-related">Related mechanisms: <a href="/nvme/question-bank/reset-shutdown/en/#q-174">Q174</a> · <a href="/nvme/question-bank/reset-shutdown/en/#q-178">Q178</a> · <a href="/nvme/question-bank/reset-shutdown/en/#q-180">Q180</a></p>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-pciereset">PCIe Transport 1.4 §3.3</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-shutdownfull">Base 2.4 §3.6–3.6.1 (memory-based scope and shutdown)</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-319" data-question="319" data-answer-kind="diagnose"><h2><a class="qa-qid" href="#q-319">Q319</a> How is an operation’s real scope established?</h2>
<p class="qa-prompt">Separate available evidence from missing information before judging conformance.</p>
<details class="qa-answer" id="q-319-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-319-a-01">Submission through one Admin Queue does not limit effects to that controller.</p><div class="qa-sections">
<section class="qa-section" id="q-319-s-01" data-answer-section="1"><h3><span>1.</span> Preserve the evidence first</h3>
<span class="qa-anchor" id="q-319-a-02"></span><p>Commands and selectors determine namespace, controller, group, domain or subsystem effects.</p>
<span class="qa-anchor" id="q-319-a-03"></span><p>Inspect command selectors, feature scope, capabilities and command effects.</p>
<span class="qa-anchor" id="q-319-a-04"></span><p>Broadcast semantics are command-specific and effects metadata does not replace explicit scope definitions.</p>
</section>
<section class="qa-section" id="q-319-s-02" data-answer-section="2"><h3><span>2.</span> Work through the possible causes</h3>
<span class="qa-anchor" id="q-319-a-17"></span><p>First read special selector values for that specific command.</p>
<span class="qa-anchor" id="q-319-a-05"></span><p>Identify endpoint, targets and shared resources, then observe inside/outside controls.</p>
</section>
<section class="qa-section" id="q-319-s-03" data-answer-section="3"><h3><span>3.</span> Decide what the evidence supports</h3>
<span class="qa-anchor" id="q-319-a-06"></span><p>Detaching one endpoint does not duplicate or delete shared namespace data.</p>
<span class="qa-anchor" id="q-319-a-07"></span><p>Exclude shared-resource and concurrent-operation causes before alleging out-of-scope effects.</p>
<span class="qa-anchor" id="q-319-a-16"></span><p>Compare matching entities and times; active inventories can legitimately differ by endpoint.</p>
</section>
</div>
<span class="qa-anchor" id="q-319-a-08"></span><span class="qa-anchor" id="q-319-a-09"></span><span class="qa-anchor" id="q-319-a-10"></span><span class="qa-anchor" id="q-319-a-11"></span><span class="qa-anchor" id="q-319-a-12"></span><span class="qa-anchor" id="q-319-a-13"></span><span class="qa-anchor" id="q-319-a-14"></span><span class="qa-anchor" id="q-319-a-15"></span>
<p class="qa-related">Related mechanisms: <a href="/nvme/question-bank/initialization/en/#q-002">Q2</a> · <a href="/nvme/question-bank/identify/en/#q-047">Q47</a> · <a href="/nvme/question-bank/logs/en/#q-081">Q81</a> · <a href="/nvme/question-bank/media/en/#q-275">Q275</a></p>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-commandseffects">Base 2.4 §5.2.13.1.6</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-capacitymodel">Base 2.4 §3.2.2–3.2.3, 3.8</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-320" data-question="320" data-answer-kind="diagnose"><h2><a class="qa-qid" href="#q-320">Q320</a> How are the interfaces combined into one conformance investigation?</h2>
<p class="qa-prompt">Separate available evidence from missing information before judging conformance.</p>
<details class="qa-answer" id="q-320-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-320-a-01">Build traceable evidence across advertisement, prerequisites, operation, result, notice, record and persistence.</p><div class="qa-sections">
<section class="qa-section" id="q-320-s-01" data-answer-section="1"><h3><span>1.</span> Preserve the evidence first</h3>
<span class="qa-anchor" id="q-320-a-02"></span><p>Define one function and its scope before testing multiple interacting mechanisms.</p>
<span class="qa-anchor" id="q-320-a-03"></span><p>Capture discovery, effects and relevant configuration as the baseline.</p>
<span class="qa-anchor" id="q-320-a-04"></span><p>Record request, completion and applicable logs/events, explaining inapplicable or unsupported interfaces.</p>
</section>
<section class="qa-section" id="q-320-s-02" data-answer-section="2"><h3><span>2.</span> Work through the possible causes</h3>
<span class="qa-anchor" id="q-320-a-17"></span><p>First state one precise requirement and then select the evidence needed to test it.</p>
<span class="qa-anchor" id="q-320-a-05"></span><p>Run a valid case, isolate invalid conditions and then test persistence from matched baselines.</p>
</section>
<section class="qa-section" id="q-320-s-03" data-answer-section="3"><h3><span>3.</span> Decide what the evidence supports</h3>
<span class="qa-anchor" id="q-320-a-06"></span><p>Conclusions identify supported requirements and remaining evidence limitations.</p>
<span class="qa-anchor" id="q-320-a-07"></span><p>Do not turn permissions into mandates, invent statuses for undefined behavior or equate acceptance with background completion.</p>
<span class="qa-anchor" id="q-320-a-16"></span><p>Link raw evidence on a timeline with source sections, figures and PDF pages.</p>
</section>
</div>
<span class="qa-anchor" id="q-320-a-08"></span><span class="qa-anchor" id="q-320-a-09"></span><span class="qa-anchor" id="q-320-a-10"></span><span class="qa-anchor" id="q-320-a-11"></span><span class="qa-anchor" id="q-320-a-12"></span><span class="qa-anchor" id="q-320-a-13"></span><span class="qa-anchor" id="q-320-a-14"></span><span class="qa-anchor" id="q-320-a-15"></span>
<p class="qa-related">Related mechanisms: <a href="/nvme/question-bank/integration/en/#q-297">Q297</a> · <a href="/nvme/question-bank/integration/en/#q-299">Q299</a> · <a href="/nvme/question-bank/integration/en/#q-300">Q300</a> · <a href="/nvme/question-bank/integration/en/#q-301">Q301</a> · <a href="/nvme/question-bank/integration/en/#q-302">Q302</a> · <a href="/nvme/question-bank/integration/en/#q-318">Q318</a> · <a href="/nvme/question-bank/integration/en/#q-319">Q319</a></p>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-commandseffects">Base 2.4 §5.2.13.1.6</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-getlog">Base 2.4 §5.2.13–5.2.13.1.1</a> · <a href="#ref-aerfull">Base 2.4 §5.2.2 (PCIe-applicable events)</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-pelcontext">Base 2.4 §5.2.13.1.14–5.2.13.1.14.2.5 (exclude PCIe link/packet decoding)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<section id="common-rules" class="qa-common"><h2>Shared rules linked from the answers</h2><p>Each shared mechanism is explained in full once in this volume. Use browser Back to return to the question; explicit command or feature exceptions take precedence.</p>
<article id="common-command-10"><h3>Command completion, events and records · Are Error Information or other logs updated?</h3><p>A successful CQE does not require a new Error Information entry. For an error with More=1, read LID 01h and correlate SQID, CID and Error Count; not every unsuccessful CQE requires a new entry. Re-read the interfaces named in this question for the state the operation changes.</p></article>
</section>
<section id="source-index"><h2>Source locations and existing figure guides</h2><p>Base printed page = PDF page−26; the other two use identical numbers. Locations follow the supplied PDF body and retain figure numbers. Shared pages contribute only the relevant definitions, excluding Fabrics and PCIe link/packet content.</p><ul class="qa-references">
<li id="ref-cc"><strong>Base 2.4 · §3.1.4 (CC, CSTS, NSSR)</strong><br>Printed pages 60–66 · PDF 86–92 · Figure 41–43</li>
<li id="ref-capacitymodel"><strong>Base 2.4 · §3.2.2–3.2.3, 3.8</strong><br>Printed pages 80–84, 125–129 · PDF 106–110, 151–155 · Figure 67–69, 86–89</li>
<li id="ref-ready"><strong>Base 2.4 · §3.5.3–3.5.4</strong><br>Printed pages 109–113 · PDF 135–139 · Figure 84–85</li>
<li id="ref-shutdownfull"><strong>Base 2.4 · §3.6–3.6.1 (memory-based scope and shutdown)</strong><br>Printed pages 113–115 · PDF 139–141 · Figure 85</li>
<li id="ref-reset"><strong>Base 2.4 · §3.7.1–3.7.4</strong><br>Printed pages 120–124 · PDF 146–150</li>
<li id="ref-firmware"><strong>Base 2.4 · §3.11–3.11.1, 5.2.9–5.2.10</strong><br>Printed pages 135–138, 202–206 · PDF 161–164, 228–232 · Figure 187–193</li>
<li id="ref-cqe"><strong>Base 2.4 · §4.2.1, 4.2.3–4.2.4</strong><br>Printed pages 144–157 · PDF 170–183 · Figure 97–105, 109</li>
<li id="ref-status"><strong>Base 2.4 · §4.2.3</strong><br>Printed pages 145–155 · PDF 171–181 · Figure 101–105</li>
<li id="ref-feature"><strong>Base 2.4 · §4.4</strong><br>Printed pages 166–169 · PDF 192–195 · Figure 126–127</li>
<li id="ref-abort"><strong>Base 2.4 · §5.2.1</strong><br>Printed pages 181–182 · PDF 207–208 · Figure 147–149</li>
<li id="ref-aer"><strong>Base 2.4 · §5.2.2</strong><br>Printed pages 183–190 · PDF 209–216 · Figure 150–156</li>
<li id="ref-aerfull"><strong>Base 2.4 · §5.2.2 (PCIe-applicable events)</strong><br>Printed pages 183–191 · PDF 209–217 · Figure 150–160</li>
<li id="ref-selftest"><strong>Base 2.4 · §5.2.6, 8.1.8</strong><br>Printed pages 199–201, 614–616 · PDF 225–227, 640–642 · Figure 176–180, 700–701</li>
<li id="ref-getlog"><strong>Base 2.4 · §5.2.13–5.2.13.1.1</strong><br>Printed pages 212–218 · PDF 238–244 · Figure 203–211</li>
<li id="ref-error"><strong>Base 2.4 · §5.2.13.1.2</strong><br>Printed pages 218–220 · PDF 244–246 · Figure 212</li>
<li id="ref-smart"><strong>Base 2.4 · §5.2.13.1.3</strong><br>Printed pages 220–225 · PDF 246–251 · Figure 213–214</li>
<li id="ref-fwlog"><strong>Base 2.4 · §5.2.13.1.4</strong><br>Printed pages 225–226 · PDF 251–252 · Figure 215</li>
<li id="ref-changedlog"><strong>Base 2.4 · §5.2.13.1.5</strong><br>Printed pages 226 · PDF 252</li>
<li id="ref-commandseffects"><strong>Base 2.4 · §5.2.13.1.6</strong><br>Printed pages 226–229 · PDF 252–255 · Figure 216–217</li>
<li id="ref-dstlog"><strong>Base 2.4 · §5.2.13.1.7</strong><br>Printed pages 229–232 · PDF 255–258 · Figure 218–219</li>
<li id="ref-pel"><strong>Base 2.4 · §5.2.13.1.14 (header, reset, hardware, Set Feature events)</strong><br>Printed pages 244–256, 258, 262–264 · PDF 270–282, 284, 288–290 · Figure 232–244, 246, 252–253</li>
<li id="ref-pelcontext"><strong>Base 2.4 · §5.2.13.1.14–5.2.13.1.14.2.5 (exclude PCIe link/packet decoding)</strong><br>Printed pages 244–256, 258 · PDF 270–282, 284 · Figure 232–244, 246</li>
<li id="ref-fwpel"><strong>Base 2.4 · §5.2.13.1.14.2.2, 5.2.13.1.14.2.4</strong><br>Printed pages 252–255 · PDF 278–281 · Figure 238, 240–241</li>
<li id="ref-nspelevent"><strong>Base 2.4 · §5.2.13.1.14.2.6</strong><br>Printed pages 258–259 · PDF 284–285 · Figure 247</li>
<li id="ref-sanitizepel"><strong>Base 2.4 · §5.2.13.1.14.2.9–5.2.13.1.14.2.10</strong><br>Printed pages 261–262 · PDF 287–288 · Figure 250–251</li>
<li id="ref-featureeffects"><strong>Base 2.4 · §5.2.13.1.18</strong><br>Printed pages 276–278 · PDF 302–304 · Figure 270–271</li>
<li id="ref-locklog"><strong>Base 2.4 · §5.2.13.1.20</strong><br>Printed pages 279–283 · PDF 305–309 · Figure 274–278</li>
<li id="ref-sanitizelog"><strong>Base 2.4 · §5.2.13.1.38</strong><br>Printed pages 313–320 · PDF 339–346 · Figure 312</li>
<li id="ref-idctrl"><strong>Base 2.4 · §5.2.14.2.1</strong><br>Printed pages 340–387 · PDF 366–413 · Figure 338–341</li>
<li id="ref-psd"><strong>Base 2.4 · §5.2.14.2.1 (Power State Descriptor)</strong><br>Printed pages 384–387 · PDF 410–413 · Figure 340–341</li>
<li id="ref-idlist"><strong>Base 2.4 · §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</strong><br>Printed pages 387–399, 402–404 · PDF 413–425, 428–430 · Figure 342–355, 360–362</li>
<li id="ref-lockdown"><strong>Base 2.4 · §5.2.16, 8.1.5</strong><br>Printed pages 405–408, 597–599 · PDF 431–434, 623–625 · Figure 365–367</li>
<li id="ref-nsattach"><strong>Base 2.4 · §5.2.24–5.2.25, 8.1.17–8.1.17.2</strong><br>Printed pages 444–448, 660–663 · PDF 470–474, 686–689 · Figure 442–450</li>
<li id="ref-sanitizecmd"><strong>Base 2.4 · §5.2.26–5.2.27</strong><br>Printed pages 448–454 · PDF 474–480 · Figure 451–455</li>
<li id="ref-setfeat"><strong>Base 2.4 · §5.2.30.1 (common fields, scope and persistence)</strong><br>Printed pages 456–460 · PDF 482–486 · Figure 463–466</li>
<li id="ref-power"><strong>Base 2.4 · §5.2.30.1.2, 5.2.30.1.7</strong><br>Printed pages 460–462, 468–469 · PDF 486–488, 494–495 · Figure 468–469, 475–478</li>
<li id="ref-timestamp"><strong>Base 2.4 · §5.2.30.1.8</strong><br>Printed pages 469–471 · PDF 495–497 · Figure 479–480</li>
<li id="ref-lockpersist"><strong>Base 2.4 · §5.2.30.1.25.4–5.2.30.1.25.4.1</strong><br>Printed pages 493–494 · PDF 519–520 · Figure 518–519</li>
<li id="ref-create"><strong>Base 2.4 · §5.3.1–5.3.2</strong><br>Printed pages 527–531 · PDF 553–557 · Figure 571–579</li>
<li id="ref-delete"><strong>Base 2.4 · §5.3.3–5.3.4</strong><br>Printed pages 531–532 · PDF 557–558 · Figure 580–583</li>
<li id="ref-powerdetail"><strong>Base 2.4 · §8.1.19.1–8.1.19.5</strong><br>Printed pages 666–671 · PDF 692–697 · Figure 738–741</li>
<li id="ref-sanitizestate"><strong>Base 2.4 · §8.1.27.1–8.1.27.5</strong><br>Printed pages 711–732 · PDF 737–758 · Figure 770–779</li>
<li id="ref-virtual"><strong>Base 2.4 · §8.2.7</strong><br>Printed pages 754–758 · PDF 780–784 · Figure 796</li>
<li id="ref-commrecovery"><strong>Base 2.4 · §9.1–9.6.2.1 (PCIe-applicable rules; stop before 9.6.2.2)</strong><br>Printed pages 825–828 · PDF 851–854</li>
<li id="ref-nvmselftest"><strong>NVM Command Set 1.3 · §4.1.4.3</strong><br>Printed pages 75–76 · PDF 75–76 · Figure 111</li>
<li id="ref-nvmpel"><strong>NVM Command Set 1.3 · §4.1.4.4</strong><br>Printed pages 76–77 · PDF 76–77 · Figure 112</li>
<li id="ref-pciereset"><strong>PCIe Transport 1.4 · §3.3</strong><br>Printed pages 11–12 · PDF 11–12</li>
<li id="ref-retirement"><strong>PCIe Transport 1.4 · §3.4 (Command Related Resource Retirement)</strong><br>Printed pages 13 · PDF 13</li>
</ul><h3>When you need a field guide</h3><p>Existing figure explanations have canonical locations; use these links instead of duplicating the same guide.</p><ul>
<li><a href="/nvme/figure-reference/command/en/#figure-b101">Base 2.4 Figure 101 · Completion Queue Entry: Status Field</a></li>
<li><a href="/nvme/figure-reference/command/en/#figure-b104">Base 2.4 Figure 104 · Status Code – Command Specific Status Values</a></li>
<li><a href="/nvme/figure-reference/identify/en/#figure-b338">Base 2.4 Figure 338 · Identify – Identify Controller Data Structure, I/O Command Set Independent</a></li>
<li><a href="/nvme/figure-reference/init/en/#figure-b41">Base 2.4 Figure 41 · Offset 14h: CC – Controller Configuration</a></li>
<li><a href="/nvme/figure-reference/init/en/#figure-b42">Base 2.4 Figure 42 · Offset 1Ch: CSTS – Controller Status</a></li>
<li><a href="/nvme/figure-reference/command/en/#figure-b97">Base 2.4 Figure 97 · Common Completion Queue Entry Layout – Admin and All I/O Command Sets</a></li>
</ul><details><summary>Original documents used</summary><ul class="qr-sources">
<li>NVM Express Base Specification · Revision 2.4 · 2026-07-31<br><code>NVM-Express-Base-Specification-Revision-2.4-Ratified-2026.07.31.pdf</code></li>
<li>NVM Express NVM Command Set Specification · Revision 1.3 · 2026-07-31<br><code>NVM-Express-NVM-Command-Set-Specification-Revision-1.3-Ratified-2026.07.31.pdf</code></li>
<li>NVM Express NVMe over PCIe Transport Specification · Revision 1.4 · 2026-07-31<br><code>NVM-Express-NVMe-over-PCIe-Transport-Specification-Revision-1.4-Ratified-2026.07.31.pdf</code></li>
</ul></details></section>
</main>
<nav class="qr-top" aria-label="Bank and editions"><a href="#content">Skip to content</a><a href="/nvme/question-bank/en/">Question index</a><a href="/nvme/question-bank/integration/zh-tw/">繁體中文</a><a href="/DOCS/nvme-question-bank/integration.html">Chinese tutorial HTML</a></nav>
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
