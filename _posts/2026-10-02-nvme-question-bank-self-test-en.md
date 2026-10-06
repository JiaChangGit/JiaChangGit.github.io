---
layout: post
title: "NVMe Self-Study Bank: Device self-test"
date: 2026-10-02 00:00:00 +0800
categories: [nvme]
permalink: /nvme/question-bank/self-test/en/
lang: en
nvme_quickref: true
nvme_qa: true
---

<div class="nvme-quickref nvme-qa">
<nav class="qr-top" aria-label="Bank and editions"><a href="#content">Skip to content</a><a href="/nvme/question-bank/en/">Question index</a><a href="/nvme/question-bank/self-test/zh-tw/">繁體中文</a><a href="/DOCS/nvme-question-bank/self-test.html">Chinese tutorial HTML</a></nav>
<main id="content"><p class="qr-eyebrow">BASE 2.4 / NVM 1.3 / PCIe 1.4 · Q1–328</p>
<header><p class="qa-range">Q149–Q156</p><h1>Device self-test</h1><p class="qr-intro">Establish supported tests, then distinguish progress, final results and valid failure details.</p><p>Practice first, then reveal the explanation. Each question uses the prose, field interpretation, comparison or flow that suits it. All numerical examples are hypothetical. Status is written SCT/SC; h indicates hexadecimal.</p></header>
<aside class="qa-glossary"><h2>Terms used in this volume</h2><dl><dt>Controller / namespace</dt><dd>A controller receives commands and manages access. A namespace is a logical storage space that commands can address. An NVM subsystem contains controllers and nonvolatile storage resources.</dd><dt>SQ / CQ / SQE / CQE</dt><dd>Submission and Completion Queues carry command entries (SQEs) and completion entries (CQEs). QID identifies a queue, CID distinguishes outstanding commands in one SQ, and NSID identifies a namespace.</dd><dt>Register / Identify / Feature / Log</dt><dd>A register exposes control or state. Identify queries capabilities and attributes; features query or configure operation; log pages report specific state or records. FID, LID, CNS and CSI select features, logs, Identify structures and command sets.</dd><dt>index / offset / zero-based</dt><dd>An index selects an entry, usually starting at 0; an offset measures distance from an origin in specified units. A zero-based count encodes count−1, but not every zero-valued field is a count. A Dword is 4 bytes; a byte is 8 bits.</dd><dt>Scope / reset / retention</dt><dd>Scope names the affected objects; retention means preserving state. Controller Reset (clearing CC.EN) is one form of Controller Level Reset, or CLR. Different CLR triggers can retain different registers.</dd></dl></aside>
<section id="overview" class="qa-overview"><h2>Start, progress and result are distinct</h2><p class="qa-takeaway">Successful initiation does not mean a passed test.</p>
<div class="qr-table" tabindex="0" role="region" aria-label="Horizontally scrollable comparison table"><table><thead><tr><th scope="col">Observation</th><th scope="col">Interface</th><th scope="col">Use</th></tr></thead><tbody><tr><td>Capability</td><td>OACS, DSTO</td><td>Support and concurrency</td></tr><tr><td>Progress</td><td>Current operation and percentage</td><td>Track current work</td></tr><tr><td>Result</td><td>Newest test/result codes</td><td>Pass, failure or abort</td></tr><tr><td>Failure detail</td><td>Validity, segment and LBA</td><td>Use only valid fields</td></tr></tbody></table></div>
<p><strong>Worked interpretation: </strong>Short and extended tests have different reset/power continuity rules.</p>
<p class="qa-citations">Sources: <a href="#ref-selftest">Base 2.4 §5.2.6, 8.1.8</a> · <a href="#ref-dstlog">Base 2.4 §5.2.13.1.7</a> · <a href="#ref-nvmselftest">NVM Command Set 1.3 §4.1.4.3</a></p>
</section>
<div class="qa-controls" hidden><label>Search this page <input type="search" id="qa-search" placeholder="Question number, field or keyword"></label><button type="button" data-expand="true">Expand all answers</button><button type="button" data-expand="false">Collapse all answers</button><output id="qa-count" aria-live="polite"></output></div>
<section id="question-index"><h2>Questions in this volume</h2><ol class="qa-index">
<li><a href="#q-149">Q149 · How are self-test support and coverage established?</a></li>
<li><a href="#q-150">Q150 · How do short and extended self-tests differ?</a></li>
<li><a href="#q-151">Q151 · What happens when self-test is restarted or cancelled?</a></li>
<li><a href="#q-152">Q152 · How are current operation and completion percentage interpreted?</a></li>
<li><a href="#q-153">Q153 · How are self-test outcomes and interruption effects interpreted?</a></li>
<li><a href="#q-154">Q154 · Does every self-test completion generate an AER?</a></li>
<li><a href="#q-155">Q155 · When are segment, diagnostic and failing-LBA fields valid?</a></li>
<li><a href="#q-156">Q156 · How are the 20 self-test results ordered and replaced?</a></li>
</ol></section>
<article class="qa-question" id="q-149" data-question="149" data-answer-kind="lookup"><h2><a class="qa-qid" href="#q-149">Q149</a> How are self-test support and coverage established?</h2>
<p class="qa-prompt">Choose the interface and target, then identify the returned field that supports your conclusion.</p>
<details class="qa-answer" id="q-149-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-149-a-01">Self-test diagnoses controller and selected media internally; it does not replace complete host data validation.</p><div class="qa-sections">
<section class="qa-section" id="q-149-s-01" data-answer-section="1"><h3><span>1.</span> Select the target and information</h3>
<span class="qa-anchor" id="q-149-a-02"></span><p>NSID 0 tests the controller, an active ID includes that namespace andFFFFFFFFh includes namespaces accessible through that controller at start.</p>
<span class="qa-anchor" id="q-149-a-03"></span><p>OACS establishes support, DSTO.SDSO concurrency scope and EDSTT extended-test duration.</p>
<span class="qa-anchor" id="q-149-a-04"></span><p>STC selects the test action and LID 06h reports current operation and 20 results.</p>
</section>
<section class="qa-section" id="q-149-s-02" data-answer-section="2"><h3><span>2.</span> Query sequence and interpretation</h3>
<span class="qa-anchor" id="q-149-a-05"></span><p>Establish support/state, preserve the old log, then start and monitor the selected test.</p>
<span class="qa-anchor" id="q-149-a-06"></span><p>Initiation success starts background testing; passing requires a new result with DSTR0.</p>
</section>
<section class="qa-section" id="q-149-s-03" data-answer-section="3"><h3><span>3.</span> Handle missing or inconsistent evidence</h3>
<span class="qa-anchor" id="q-149-a-07"></span><p>Invalid NSID uses Invalid Namespace/Format; an inactive NSID uses Invalid Field. Keep the cases distinct.</p>
<span class="qa-anchor" id="q-149-a-16"></span><p>Match OACS, STC, target and logged test code.</p>
<span class="qa-anchor" id="q-149-a-17"></span><p>First distinguish an invalid ID from an existing inactive namespace.</p>
</section>
</div>
<span class="qa-anchor" id="q-149-a-08"></span><span class="qa-anchor" id="q-149-a-09"></span><span class="qa-anchor" id="q-149-a-10"></span><span class="qa-anchor" id="q-149-a-11"></span><span class="qa-anchor" id="q-149-a-12"></span><span class="qa-anchor" id="q-149-a-13"></span><span class="qa-anchor" id="q-149-a-14"></span><span class="qa-anchor" id="q-149-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-selftest">Base 2.4 §5.2.6, 8.1.8</a> · <a href="#ref-dstlog">Base 2.4 §5.2.13.1.7</a> · <a href="#ref-nvmselftest">NVM Command Set 1.3 §4.1.4.3</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-aerfull">Base 2.4 §5.2.2 (PCIe-applicable events)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-150" data-question="150" data-answer-kind="compare"><h2><a class="qa-qid" href="#q-150">Q150</a> How do short and extended self-tests differ?</h2>
<p class="qa-prompt">Identify the key difference and one case where the alternatives are not interchangeable.</p>
<details class="qa-answer" id="q-150-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-150-a-01">They offer different diagnostic duration/depth; segment contents are vendor-defined and the illustrated RAM/media checks are informative examples.</p><div class="qa-sections">
<section class="qa-section" id="q-150-s-01" data-answer-section="1"><h3><span>1.</span> What differs</h3>
<span class="qa-anchor" id="q-150-a-02"></span><p>Both use NSID coverage and can affect other work through shared resources.</p>
<span class="qa-anchor" id="q-150-a-04"></span><p>STC1/2 selects short/extended; DSTOS identifies the current test and DSTCS its percentage.</p>
</section>
<section class="qa-section" id="q-150-s-02" data-answer-section="2"><h3><span>2.</span> How to choose and verify</h3>
<span class="qa-anchor" id="q-150-a-03"></span><p>EDSTT reports extended duration; short tests should finish within two minutes. Preserve the strength of these recommendations.</p>
<span class="qa-anchor" id="q-150-a-05"></span><p>Select depth/impact, record start and monitor; commands requiring suspension run between test suspension and resumption.</p>
<span class="qa-anchor" id="q-150-a-06"></span><p>Results determine pass/failure; a short pass does not guarantee an extended pass.</p>
</section>
<section class="qa-section" id="q-150-s-03" data-answer-section="3"><h3><span>3.</span> Where the comparison stops</h3>
<span class="qa-anchor" id="q-150-a-07"></span><p>Reset is a crucial difference: CLR aborts short tests, while extended tests persist across CLR and resume after restored power.</p>
<span class="qa-anchor" id="q-150-a-16"></span><p>Account for other work/suspension when reviewing timing and apply the distinct reset rules.</p>
</section>
</div>
<span class="qa-anchor" id="q-150-a-17"></span><span class="qa-anchor" id="q-150-a-08"></span><span class="qa-anchor" id="q-150-a-09"></span><span class="qa-anchor" id="q-150-a-10"></span><span class="qa-anchor" id="q-150-a-11"></span><span class="qa-anchor" id="q-150-a-12"></span><span class="qa-anchor" id="q-150-a-13"></span><span class="qa-anchor" id="q-150-a-14"></span><span class="qa-anchor" id="q-150-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-selftest">Base 2.4 §5.2.6, 8.1.8</a> · <a href="#ref-dstlog">Base 2.4 §5.2.13.1.7</a> · <a href="#ref-nvmselftest">NVM Command Set 1.3 §4.1.4.3</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-aerfull">Base 2.4 §5.2.2 (PCIe-applicable events)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-151" data-question="151" data-answer-kind="error"><h2><a class="qa-qid" href="#q-151">Q151</a> What happens when self-test is restarted or cancelled?</h2>
<p class="qa-prompt">Distinguish failure conditions before deciding whether a particular response is required.</p>
<details class="qa-answer" id="q-151-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-151-a-01">Concurrency is limited and STCFh explicitly cancels the background self-test operation.</p><div class="qa-sections">
<section class="qa-section" id="q-151-s-01" data-answer-section="1"><h3><span>1.</span> Distinguish the failure conditions</h3>
<span class="qa-anchor" id="q-151-a-02"></span><p>SDSO0 checks controller-level concurrency andSDSO1 subsystem-level concurrency.</p>
<span class="qa-anchor" id="q-151-a-04"></span><p>STC1/2/3 start operations, Fh cancels andEh has vendor-specific interactions.</p>
<span class="qa-anchor" id="q-151-a-07"></span><p>Starting 1/2/3 while a test is active returns 1/1Dh rather than silently restarting it.</p>
</section>
<section class="qa-section" id="q-151-s-02" data-answer-section="2"><h3><span>2.</span> Establish the cause from evidence</h3>
<span class="qa-anchor" id="q-151-a-03"></span><p>Read DSTO and LID 06h; local host command tracking cannot rule out an already running background test.</p>
<span class="qa-anchor" id="q-151-a-05"></span><p>With an active test, cancellation precedes a new result, idle state and command completion.</p>
</section>
<section class="qa-section" id="q-151-s-03" data-answer-section="3"><h3><span>3.</span> Outcome and follow-up checks</h3>
<span class="qa-anchor" id="q-151-a-06"></span><p>Cancelling with no test succeeds without changing the log.</p>
<span class="qa-anchor" id="q-151-a-16"></span><p>Verify log update ordering and DSTR1 rather than idle alone.</p>
<span class="qa-anchor" id="q-151-a-17"></span><p>First distinguish STCFh from Abort targeting an already completed initiation command.</p>
</section>
</div>
<span class="qa-anchor" id="q-151-a-08"></span><span class="qa-anchor" id="q-151-a-09"></span><span class="qa-anchor" id="q-151-a-10"></span><span class="qa-anchor" id="q-151-a-11"></span><span class="qa-anchor" id="q-151-a-12"></span><span class="qa-anchor" id="q-151-a-13"></span><span class="qa-anchor" id="q-151-a-14"></span><span class="qa-anchor" id="q-151-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-selftest">Base 2.4 §5.2.6, 8.1.8</a> · <a href="#ref-dstlog">Base 2.4 §5.2.13.1.7</a> · <a href="#ref-nvmselftest">NVM Command Set 1.3 §4.1.4.3</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-aerfull">Base 2.4 §5.2.2 (PCIe-applicable events)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-152" data-question="152" data-answer-kind="fields"><h2><a class="qa-qid" href="#q-152">Q152</a> How are current operation and completion percentage interpreted?</h2>
<p class="qa-prompt">Explain the units and encoding, then work through one set of values.</p>
<details class="qa-answer" id="q-152-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-152-a-01">The header describes current work while the result list describes finished tests; old results do not replace current progress.</p><div class="qa-sections">
<section class="qa-section" id="q-152-s-01" data-answer-section="1"><h3><span>1.</span> Establish the source and scope</h3>
<span class="qa-anchor" id="q-152-a-02"></span><p>Query the appropriate test scope and retain sampling time.</p>
<span class="qa-anchor" id="q-152-a-03"></span><p>Use LID 06h CDSTO/CDSTC/RDS1 after checking support.</p>
</section>
<section class="qa-section" id="q-152-s-02" data-answer-section="2"><h3><span>2.</span> Fields, units and worked interpretation</h3>
<span class="qa-anchor" id="q-152-a-04"></span><p>DSTOS0 is idle,1 short,2 extended,3 refresh; DSTCS25 means 25%, not 26%.</p>
<span class="qa-anchor" id="q-152-a-05"></span><p>Read operation before percentage; ignore percentage when idle and inspect the latest result.</p>
<span class="qa-anchor" id="q-152-a-06"></span><p>A short/extended result must be created before clearing DSTOS; idle plus new result establishes outcome.</p>
</section>
<section class="qa-section" id="q-152-s-03" data-answer-section="3"><h3><span>3.</span> Conditions that change the interpretation</h3>
<span class="qa-anchor" id="q-152-a-07"></span><p>A stationary percentage need not prove failure; segment work or suspension may explain it. Percentage does not replace outcome.</p>
<span class="qa-anchor" id="q-152-a-16"></span><p>Compare operation, progress and result across snapshots rather than diagnosing a stall from one number.</p>
</section>
</div>
<span class="qa-anchor" id="q-152-a-17"></span><span class="qa-anchor" id="q-152-a-08"></span><span class="qa-anchor" id="q-152-a-09"></span><span class="qa-anchor" id="q-152-a-10"></span><span class="qa-anchor" id="q-152-a-11"></span><span class="qa-anchor" id="q-152-a-12"></span><span class="qa-anchor" id="q-152-a-13"></span><span class="qa-anchor" id="q-152-a-14"></span><span class="qa-anchor" id="q-152-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-selftest">Base 2.4 §5.2.6, 8.1.8</a> · <a href="#ref-dstlog">Base 2.4 §5.2.13.1.7</a> · <a href="#ref-nvmselftest">NVM Command Set 1.3 §4.1.4.3</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-aerfull">Base 2.4 §5.2.2 (PCIe-applicable events)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-153" data-question="153" data-answer-kind="lifecycle"><h2><a class="qa-qid" href="#q-153">Q153</a> How are self-test outcomes and interruption effects interpreted?</h2>
<p class="qa-prompt">Name the reset or interruption, then assess settings, ongoing operations and data separately.</p>
<details class="qa-answer" id="q-153-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-153-a-01">Outcome codes distinguish diagnostic failure from host cancellation; resumed extended testing must not be mislabeled as failed due to reset alone.</p><div class="qa-sections">
<section class="qa-section" id="q-153-s-01" data-answer-section="1"><h3><span>1.</span> Identify the trigger and affected objects</h3>
<span class="qa-anchor" id="q-153-a-02"></span><p>Results describe test instances and their code/time, not initiation-command status.</p>
<span class="qa-anchor" id="q-153-a-03"></span><p>Read DSTR, DSTC, POH and valid diagnostic fields in LID 06h.</p>
</section>
<section class="qa-section" id="q-153-s-02" data-answer-section="2"><h3><span>2.</span> State changes and recovery</h3>
<span class="qa-anchor" id="q-153-a-04"></span><p>DSTR0 success;1 command cancellation;2 CLR;3 namespace removal;4 Format;5 fatal/unknown test error;6/7 segment failure;8 unknown abort;9 Sanitize.</p>
<span class="qa-anchor" id="q-153-a-05"></span><p>Identify test type before matching interruption: CLR ends short testing but extended testing resumes and produces its final result later.</p>
<span class="qa-anchor" id="q-153-a-06"></span><p>DSTR0 passes;7 provides a known failing segment. No new result can mean extended testing is still resuming.</p>
</section>
<section class="qa-section" id="q-153-s-03" data-answer-section="3"><h3><span>3.</span> Checks across reset or power loss</h3>
<span class="qa-anchor" id="q-153-a-12"></span>
<span class="qa-anchor" id="q-153-a-13"></span>
<span class="qa-anchor" id="q-153-a-14"></span>
<div class="qr-table" tabindex="0" role="region" aria-label="Horizontally scrollable comparison table"><table><thead><tr><th scope="col">Trigger</th><th scope="col">Effect on this operation or state</th></tr></thead><tbody><tr><td>What survives or continues after Controller Reset?</td><td>CLR aborts a short test but an extended test must persist and resume after reset. The resume segment is vendor-specific; implementations should only need to repeat the interrupted last segment.</td></tr><tr><td>What survives or continues after NVM Subsystem Reset?</td><td>Subsystem reset causes CLR on covered controllers: short tests abort and extended tests resume. Rebuilding Admin Queues is not restarting the entire extended test.</td></tr><tr><td>What survives or continues after a power cycle?</td><td>Extended testing must resume after power restoration; short testing has no such continuation requirement. Read operation/progress/results rather than requiring reset-aborted results for both.</td></tr></tbody></table></div>
</section>
<section class="qa-section" id="q-153-s-04" data-answer-section="4"><h3><span>4.</span> Verify retention and recovery</h3>
<span class="qa-anchor" id="q-153-a-07"></span><p>There is no separate power-loss DSTR code; Format cancellation also depends on Figure 701 scope combinations.</p>
<span class="qa-anchor" id="q-153-a-16"></span><p>Correlate external operations, test type and log cause.</p>
<span class="qa-anchor" id="q-153-a-17"></span><p>First check extended-test continuation before expecting a reset-aborted entry.</p>
</section>
</div>
<span class="qa-anchor" id="q-153-a-08"></span><span class="qa-anchor" id="q-153-a-09"></span><span class="qa-anchor" id="q-153-a-10"></span><span class="qa-anchor" id="q-153-a-11"></span><span class="qa-anchor" id="q-153-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-selftest">Base 2.4 §5.2.6, 8.1.8</a> · <a href="#ref-dstlog">Base 2.4 §5.2.13.1.7</a> · <a href="#ref-nvmselftest">NVM Command Set 1.3 §4.1.4.3</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-aerfull">Base 2.4 §5.2.2 (PCIe-applicable events)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-154" data-question="154" data-answer-kind="events"><h2><a class="qa-qid" href="#q-154">Q154</a> Does every self-test completion generate an AER?</h2>
<p class="qa-prompt">Establish the event condition, then distinguish notification, acknowledgment and recording.</p>
<details class="qa-answer" id="q-154-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-154-a-01">Determine normal self-test completion from the Device Self-test Log. There is no generic Self-test Completed notice, so receiving an AER is not a completion requirement.</p><div class="qa-sections">
<section class="qa-section" id="q-154-s-01" data-answer-section="1"><h3><span>1.</span> Where normal test completion is reported</h3>
<span class="qa-anchor" id="q-154-a-02"></span><p>Initiation completion and later background completion are distinct and do not automatically create an AER.</p>
<span class="qa-anchor" id="q-154-a-05"></span><p>Monitor operation/new result; correlate any diagnostic-error event and additional error information.</p>
<span class="qa-anchor" id="q-154-a-06"></span><p>Normal completion without AER can conform; an error event still does not replace detailed results.</p>
</section>
<section class="qa-section" id="q-154-s-02" data-answer-section="2"><h3><span>2.</span> Diagnostic Failure is a distinct notification</h3>
<span class="qa-anchor" id="q-154-a-03"></span><p>Check self-test/LID 06h support and the separate Diagnostic Failure error event.</p>
<span class="qa-anchor" id="q-154-a-04"></span><p>Diagnostic Failure uses AET0/AEI02h and is distinct from DSTR.</p>
<span class="qa-anchor" id="q-154-a-16"></span><p>Validate defined events rather than transplanting Sanitize completion semantics.</p>
</section>
</div>
<span class="qa-anchor" id="q-154-a-07"></span><span class="qa-anchor" id="q-154-a-17"></span><span class="qa-anchor" id="q-154-a-08"></span><span class="qa-anchor" id="q-154-a-09"></span><span class="qa-anchor" id="q-154-a-10"></span><span class="qa-anchor" id="q-154-a-11"></span><span class="qa-anchor" id="q-154-a-12"></span><span class="qa-anchor" id="q-154-a-13"></span><span class="qa-anchor" id="q-154-a-14"></span><span class="qa-anchor" id="q-154-a-15"></span>
<p class="qa-related">Related mechanisms: <a href="/nvme/question-bank/format-sanitize/en/#q-133">Q133</a></p>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-selftest">Base 2.4 §5.2.6, 8.1.8</a> · <a href="#ref-dstlog">Base 2.4 §5.2.13.1.7</a> · <a href="#ref-nvmselftest">NVM Command Set 1.3 §4.1.4.3</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-aerfull">Base 2.4 §5.2.2 (PCIe-applicable events)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-155" data-question="155" data-answer-kind="fields"><h2><a class="qa-qid" href="#q-155">Q155</a> When are segment, diagnostic and failing-LBA fields valid?</h2>
<p class="qa-prompt">Explain the units and encoding, then work through one set of values.</p>
<details class="qa-answer" id="q-155-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-155-a-01">Nonzero fields need not be valid; validity bits prevent false precision.</p><div class="qa-sections">
<section class="qa-section" id="q-155-s-01" data-answer-section="1"><h3><span>1.</span> Establish the source and scope</h3>
<span class="qa-anchor" id="q-155-a-02"></span><p>SEGN identifies an internal test segment and FLBA a logical block; they are not interchangeable.</p>
<span class="qa-anchor" id="q-155-a-03"></span><p>Read DSTR and VDINFO validity bits before the corresponding fields.</p>
</section>
<section class="qa-section" id="q-155-s-02" data-answer-section="2"><h3><span>2.</span> Fields, units and worked interpretation</h3>
<span class="qa-anchor" id="q-155-a-04"></span><p>SEGN is the first known failed segment only for DSTR7; FVLD validates one failing LBA under NVM semantics.</p>
<span class="qa-anchor" id="q-155-a-05"></span><p>Check nonempty result and valid bits before mapping namespace/LBA; do not invent namespace association.</p>
<span class="qa-anchor" id="q-155-a-06"></span><p>Reporting one of several failing LBAs is valid; completeness or lowest-LBA ordering is not guaranteed.</p>
</section>
<section class="qa-section" id="q-155-s-03" data-answer-section="3"><h3><span>3.</span> Conditions that change the interpretation</h3>
<span class="qa-anchor" id="q-155-a-07"></span><p>Ignore invalid fields rather than validating their range, while valid contradictory data remains significant.</p>
<span class="qa-anchor" id="q-155-a-16"></span><p>Distinguish unknown location from an inconsistent valid location using validity and format.</p>
</section>
</div>
<span class="qa-anchor" id="q-155-a-17"></span><span class="qa-anchor" id="q-155-a-08"></span><span class="qa-anchor" id="q-155-a-09"></span><span class="qa-anchor" id="q-155-a-10"></span><span class="qa-anchor" id="q-155-a-11"></span><span class="qa-anchor" id="q-155-a-12"></span><span class="qa-anchor" id="q-155-a-13"></span><span class="qa-anchor" id="q-155-a-14"></span><span class="qa-anchor" id="q-155-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-selftest">Base 2.4 §5.2.6, 8.1.8</a> · <a href="#ref-dstlog">Base 2.4 §5.2.13.1.7</a> · <a href="#ref-nvmselftest">NVM Command Set 1.3 §4.1.4.3</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-aerfull">Base 2.4 §5.2.2 (PCIe-applicable events)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-156" data-question="156" data-answer-kind="concept"><h2><a class="qa-qid" href="#q-156">Q156</a> How are the 20 self-test results ordered and replaced?</h2>
<p class="qa-prompt">Explain the mechanism in your own words and identify a common misconception.</p>
<details class="qa-answer" id="q-156-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-156-a-01">Fixed history supports recent diagnosis rather than a complete lifetime audit.</p><div class="qa-sections">
<section class="qa-section" id="q-156-s-01" data-answer-section="1"><h3><span>1.</span> Mechanism and scope</h3>
<span class="qa-anchor" id="q-156-a-02"></span><p>LID 06h has 20 results of 28 bytes after a 4-byte current-status header.</p>
<span class="qa-anchor" id="q-156-a-04"></span><p>RDS1 is newest through RDS20 oldest; unused entries have DSTRFh/DSTC0 and other fields ignored.</p>
</section>
<section class="qa-section" id="q-156-s-02" data-answer-section="2"><h3><span>2.</span> Understand it through actions and results</h3>
<span class="qa-anchor" id="q-156-a-03"></span><p>Use structural and empty-entry rules, not an all-zero test.</p>
<span class="qa-anchor" id="q-156-a-05"></span><p>Snapshot RDS1, then verify insertion and older-result displacement; history beyond 20 is no longer included.</p>
<span class="qa-anchor" id="q-156-a-06"></span><p>After the 21st result,20 structures still represent the recent history.</p>
</section>
<section class="qa-section" id="q-156-s-03" data-answer-section="3"><h3><span>3.</span> Avoid a misleading conclusion</h3>
<span class="qa-anchor" id="q-156-a-07"></span><p>STCFh with no active test leaves the log unchanged rather than inserting a synthetic cancellation result.</p>
<span class="qa-anchor" id="q-156-a-16"></span><p>Compare code, outcome, hours and diagnostics rather than treating potentially repeated timestamps as unique IDs.</p>
</section>
</div>
<span class="qa-anchor" id="q-156-a-17"></span><span class="qa-anchor" id="q-156-a-08"></span><span class="qa-anchor" id="q-156-a-09"></span><span class="qa-anchor" id="q-156-a-10"></span><span class="qa-anchor" id="q-156-a-11"></span><span class="qa-anchor" id="q-156-a-12"></span><span class="qa-anchor" id="q-156-a-13"></span><span class="qa-anchor" id="q-156-a-14"></span><span class="qa-anchor" id="q-156-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-selftest">Base 2.4 §5.2.6, 8.1.8</a> · <a href="#ref-dstlog">Base 2.4 §5.2.13.1.7</a> · <a href="#ref-nvmselftest">NVM Command Set 1.3 §4.1.4.3</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-aerfull">Base 2.4 §5.2.2 (PCIe-applicable events)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>

<section id="source-index"><h2>Source locations and existing figure guides</h2><p>Base printed page = PDF page−26; the other two use identical numbers. Locations follow the supplied PDF body and retain figure numbers. Shared pages contribute only the relevant definitions, excluding Fabrics and PCIe link/packet content.</p><ul class="qa-references">
<li id="ref-reset"><strong>Base 2.4 · §3.7.1–3.7.4</strong><br>Printed pages 120–124 · PDF 146–150</li>
<li id="ref-status"><strong>Base 2.4 · §4.2.3</strong><br>Printed pages 145–155 · PDF 171–181 · Figure 101–105</li>
<li id="ref-aer"><strong>Base 2.4 · §5.2.2</strong><br>Printed pages 183–190 · PDF 209–216 · Figure 150–156</li>
<li id="ref-aerfull"><strong>Base 2.4 · §5.2.2 (PCIe-applicable events)</strong><br>Printed pages 183–191 · PDF 209–217 · Figure 150–160</li>
<li id="ref-selftest"><strong>Base 2.4 · §5.2.6, 8.1.8</strong><br>Printed pages 199–201, 614–616 · PDF 225–227, 640–642 · Figure 176–180, 700–701</li>
<li id="ref-error"><strong>Base 2.4 · §5.2.13.1.2</strong><br>Printed pages 218–220 · PDF 244–246 · Figure 212</li>
<li id="ref-dstlog"><strong>Base 2.4 · §5.2.13.1.7</strong><br>Printed pages 229–232 · PDF 255–258 · Figure 218–219</li>
<li id="ref-pel"><strong>Base 2.4 · §5.2.13.1.14 (header, reset, hardware, Set Feature events)</strong><br>Printed pages 244–256, 258, 262–264 · PDF 270–282, 284, 288–290 · Figure 232–244, 246, 252–253</li>
<li id="ref-idctrl"><strong>Base 2.4 · §5.2.14.2.1</strong><br>Printed pages 340–387 · PDF 366–413 · Figure 338–341</li>
<li id="ref-nvmselftest"><strong>NVM Command Set 1.3 · §4.1.4.3</strong><br>Printed pages 75–76 · PDF 75–76 · Figure 111</li>
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
<nav class="qr-top" aria-label="Bank and editions"><a href="#content">Skip to content</a><a href="/nvme/question-bank/en/">Question index</a><a href="/nvme/question-bank/self-test/zh-tw/">繁體中文</a><a href="/DOCS/nvme-question-bank/self-test.html">Chinese tutorial HTML</a></nav>
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
