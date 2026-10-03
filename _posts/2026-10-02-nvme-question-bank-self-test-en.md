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
<header><p class="qa-range">Q149–Q156</p><h1>Device self-test</h1><p class="qr-intro">Establish supported tests, then distinguish progress, final results and valid failure details.</p><p>Practice first, then reveal 17 answer items per question. All numerical examples are hypothetical. Status is written SCT/SC; h indicates hexadecimal.</p></header>
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
<article class="qa-question" id="q-149" data-question="149"><h2><a class="qa-qid" href="#q-149">Q149</a> How are self-test support and coverage established?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-149-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-149-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Self-test diagnoses controller and selected media internally; it does not replace complete host data validation.</p>
</li>
<li id="q-149-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>NSID 0 tests the controller, an active ID includes that namespace andFFFFFFFFh includes namespaces accessible through that controller at start.</p>
</li>
<li id="q-149-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>OACS establishes support, DSTO.SDSO concurrency scope and EDSTT extended-test duration.</p>
</li>
<li id="q-149-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>STC selects the test action and LID 06h reports current operation and 20 results.</p>
</li>
<li id="q-149-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Establish support/state, preserve the old log, then start and monitor the selected test.</p>
</li>
<li id="q-149-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Initiation success starts background testing; passing requires a new result with DSTR0.</p>
</li>
<li id="q-149-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Invalid NSID uses Invalid Namespace/Format; an inactive NSID uses Invalid Field. Keep the cases distinct.</p>
</li>
<li id="q-149-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-149-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>There is no generic Device Self-test Completed AER. <a class="qa-rule-link" href="#common-selftest_op-9">Full rule in this volume</a></p>
</li>
<li id="q-149-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Short/extended completion or cancellation creates the newest result before returning current operation to idle. <a class="qa-rule-link" href="#common-selftest_op-10">Full rule in this volume</a></p>
</li>
<li id="q-149-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>PEL has no generic per-self-test result event; use LID 06h. <a class="qa-rule-link" href="#common-selftest_op-11">Full rule in this volume</a></p>
</li>
<li id="q-149-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>CLR aborts a short test but an extended test must persist and resume after reset. <a class="qa-rule-link" href="#common-selftest_op-12">Full rule in this volume</a></p>
</li>
<li id="q-149-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Subsystem reset causes CLR on covered controllers: short tests abort and extended tests resume. <a class="qa-rule-link" href="#common-selftest_op-13">Full rule in this volume</a></p>
</li>
<li id="q-149-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Extended testing must resume after power restoration; short testing has no such continuation requirement. <a class="qa-rule-link" href="#common-selftest_op-14">Full rule in this volume</a></p>
</li>
<li id="q-149-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>The receiving controller runs the test and NSID selects coverage. <a class="qa-rule-link" href="#common-selftest_op-15">Full rule in this volume</a></p>
</li>
<li id="q-149-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Match OACS, STC, target and logged test code.</p>
</li>
<li id="q-149-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First distinguish an invalid ID from an existing inactive namespace.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-selftest">Base 2.4 §5.2.6, 8.1.8</a> · <a href="#ref-dstlog">Base 2.4 §5.2.13.1.7</a> · <a href="#ref-nvmselftest">NVM Command Set 1.3 §4.1.4.3</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-aerfull">Base 2.4 §5.2.2 (PCIe-applicable events)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-150" data-question="150"><h2><a class="qa-qid" href="#q-150">Q150</a> How do short and extended self-tests differ?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-150-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-150-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>They offer different diagnostic duration/depth; segment contents are vendor-defined and the illustrated RAM/media checks are informative examples.</p>
</li>
<li id="q-150-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Both use NSID coverage and can affect other work through shared resources.</p>
</li>
<li id="q-150-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>EDSTT reports extended duration; short tests should finish within two minutes. Preserve the strength of these recommendations.</p>
</li>
<li id="q-150-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>STC1/2 selects short/extended; DSTOS identifies the current test and DSTCS its percentage.</p>
</li>
<li id="q-150-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Select depth/impact, record start and monitor; commands requiring suspension run between test suspension and resumption.</p>
</li>
<li id="q-150-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Results determine pass/failure; a short pass does not guarantee an extended pass.</p>
</li>
<li id="q-150-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Reset is a crucial difference: CLR aborts short tests, while extended tests persist across CLR and resume after restored power.</p>
</li>
<li id="q-150-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-150-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>There is no generic Device Self-test Completed AER. <a class="qa-rule-link" href="#common-selftest_op-9">Full rule in this volume</a></p>
</li>
<li id="q-150-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Short/extended completion or cancellation creates the newest result before returning current operation to idle. <a class="qa-rule-link" href="#common-selftest_op-10">Full rule in this volume</a></p>
</li>
<li id="q-150-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>PEL has no generic per-self-test result event; use LID 06h. <a class="qa-rule-link" href="#common-selftest_op-11">Full rule in this volume</a></p>
</li>
<li id="q-150-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>CLR aborts a short test but an extended test must persist and resume after reset. <a class="qa-rule-link" href="#common-selftest_op-12">Full rule in this volume</a></p>
</li>
<li id="q-150-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Subsystem reset causes CLR on covered controllers: short tests abort and extended tests resume. <a class="qa-rule-link" href="#common-selftest_op-13">Full rule in this volume</a></p>
</li>
<li id="q-150-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Extended testing must resume after power restoration; short testing has no such continuation requirement. <a class="qa-rule-link" href="#common-selftest_op-14">Full rule in this volume</a></p>
</li>
<li id="q-150-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>The receiving controller runs the test and NSID selects coverage. <a class="qa-rule-link" href="#common-selftest_op-15">Full rule in this volume</a></p>
</li>
<li id="q-150-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Account for other work/suspension when reviewing timing and apply the distinct reset rules.</p>
</li>
<li id="q-150-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First inspect STC before applying reset persistence.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-selftest">Base 2.4 §5.2.6, 8.1.8</a> · <a href="#ref-dstlog">Base 2.4 §5.2.13.1.7</a> · <a href="#ref-nvmselftest">NVM Command Set 1.3 §4.1.4.3</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-aerfull">Base 2.4 §5.2.2 (PCIe-applicable events)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-151" data-question="151"><h2><a class="qa-qid" href="#q-151">Q151</a> What happens when self-test is restarted or cancelled?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-151-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-151-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Concurrency is limited and STCFh explicitly cancels the background self-test operation.</p>
</li>
<li id="q-151-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>SDSO0 checks controller-level concurrency andSDSO1 subsystem-level concurrency.</p>
</li>
<li id="q-151-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Read DSTO and LID 06h; local host command tracking cannot rule out an already running background test.</p>
</li>
<li id="q-151-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>STC1/2/3 start operations, Fh cancels andEh has vendor-specific interactions.</p>
</li>
<li id="q-151-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>With an active test, cancellation precedes a new result, idle state and command completion.</p>
</li>
<li id="q-151-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Cancelling with no test succeeds without changing the log.</p>
</li>
<li id="q-151-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Starting 1/2/3 while a test is active returns 1/1Dh rather than silently restarting it.</p>
</li>
<li id="q-151-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-151-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>There is no generic Device Self-test Completed AER. <a class="qa-rule-link" href="#common-selftest_op-9">Full rule in this volume</a></p>
</li>
<li id="q-151-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Short/extended completion or cancellation creates the newest result before returning current operation to idle. <a class="qa-rule-link" href="#common-selftest_op-10">Full rule in this volume</a></p>
</li>
<li id="q-151-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>PEL has no generic per-self-test result event; use LID 06h. <a class="qa-rule-link" href="#common-selftest_op-11">Full rule in this volume</a></p>
</li>
<li id="q-151-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>CLR aborts a short test but an extended test must persist and resume after reset. <a class="qa-rule-link" href="#common-selftest_op-12">Full rule in this volume</a></p>
</li>
<li id="q-151-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Subsystem reset causes CLR on covered controllers: short tests abort and extended tests resume. <a class="qa-rule-link" href="#common-selftest_op-13">Full rule in this volume</a></p>
</li>
<li id="q-151-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Extended testing must resume after power restoration; short testing has no such continuation requirement. <a class="qa-rule-link" href="#common-selftest_op-14">Full rule in this volume</a></p>
</li>
<li id="q-151-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>The receiving controller runs the test and NSID selects coverage. <a class="qa-rule-link" href="#common-selftest_op-15">Full rule in this volume</a></p>
</li>
<li id="q-151-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Verify log update ordering and DSTR1 rather than idle alone.</p>
</li>
<li id="q-151-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First distinguish STCFh from Abort targeting an already completed initiation command.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-selftest">Base 2.4 §5.2.6, 8.1.8</a> · <a href="#ref-dstlog">Base 2.4 §5.2.13.1.7</a> · <a href="#ref-nvmselftest">NVM Command Set 1.3 §4.1.4.3</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-aerfull">Base 2.4 §5.2.2 (PCIe-applicable events)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-152" data-question="152"><h2><a class="qa-qid" href="#q-152">Q152</a> How are current operation and completion percentage interpreted?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-152-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-152-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>The header describes current work while the result list describes finished tests; old results do not replace current progress.</p>
</li>
<li id="q-152-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Query the appropriate test scope and retain sampling time.</p>
</li>
<li id="q-152-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Use LID 06h CDSTO/CDSTC/RDS1 after checking support.</p>
</li>
<li id="q-152-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>DSTOS0 is idle,1 short,2 extended,3 refresh; DSTCS25 means 25%, not 26%.</p>
</li>
<li id="q-152-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Read operation before percentage; ignore percentage when idle and inspect the latest result.</p>
</li>
<li id="q-152-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>A short/extended result must be created before clearing DSTOS; idle plus new result establishes outcome.</p>
</li>
<li id="q-152-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>A stationary percentage need not prove failure; segment work or suspension may explain it. Percentage does not replace outcome.</p>
</li>
<li id="q-152-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-152-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>There is no generic Device Self-test Completed AER. <a class="qa-rule-link" href="#common-selftest_op-9">Full rule in this volume</a></p>
</li>
<li id="q-152-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Short/extended completion or cancellation creates the newest result before returning current operation to idle. <a class="qa-rule-link" href="#common-selftest_op-10">Full rule in this volume</a></p>
</li>
<li id="q-152-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>PEL has no generic per-self-test result event; use LID 06h. <a class="qa-rule-link" href="#common-selftest_op-11">Full rule in this volume</a></p>
</li>
<li id="q-152-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>CLR aborts a short test but an extended test must persist and resume after reset. <a class="qa-rule-link" href="#common-selftest_op-12">Full rule in this volume</a></p>
</li>
<li id="q-152-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Subsystem reset causes CLR on covered controllers: short tests abort and extended tests resume. <a class="qa-rule-link" href="#common-selftest_op-13">Full rule in this volume</a></p>
</li>
<li id="q-152-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Extended testing must resume after power restoration; short testing has no such continuation requirement. <a class="qa-rule-link" href="#common-selftest_op-14">Full rule in this volume</a></p>
</li>
<li id="q-152-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>The receiving controller runs the test and NSID selects coverage. <a class="qa-rule-link" href="#common-selftest_op-15">Full rule in this volume</a></p>
</li>
<li id="q-152-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Compare operation, progress and result across snapshots rather than diagnosing a stall from one number.</p>
</li>
<li id="q-152-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First check idle before interpreting a leftover percentage.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-selftest">Base 2.4 §5.2.6, 8.1.8</a> · <a href="#ref-dstlog">Base 2.4 §5.2.13.1.7</a> · <a href="#ref-nvmselftest">NVM Command Set 1.3 §4.1.4.3</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-aerfull">Base 2.4 §5.2.2 (PCIe-applicable events)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-153" data-question="153"><h2><a class="qa-qid" href="#q-153">Q153</a> How are self-test outcomes and interruption effects interpreted?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-153-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-153-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Outcome codes distinguish diagnostic failure from host cancellation; resumed extended testing must not be mislabeled as failed due to reset alone.</p>
</li>
<li id="q-153-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Results describe test instances and their code/time, not initiation-command status.</p>
</li>
<li id="q-153-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Read DSTR, DSTC, POH and valid diagnostic fields in LID 06h.</p>
</li>
<li id="q-153-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>DSTR0 success;1 command cancellation;2 CLR;3 namespace removal;4 Format;5 fatal/unknown test error;6/7 segment failure;8 unknown abort;9 Sanitize.</p>
</li>
<li id="q-153-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Identify test type before matching interruption: CLR ends short testing but extended testing resumes and produces its final result later.</p>
</li>
<li id="q-153-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>DSTR0 passes;7 provides a known failing segment. No new result can mean extended testing is still resuming.</p>
</li>
<li id="q-153-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>There is no separate power-loss DSTR code; Format cancellation also depends on Figure 701 scope combinations.</p>
</li>
<li id="q-153-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-153-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>There is no generic Device Self-test Completed AER. <a class="qa-rule-link" href="#common-selftest_op-9">Full rule in this volume</a></p>
</li>
<li id="q-153-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Short/extended completion or cancellation creates the newest result before returning current operation to idle. <a class="qa-rule-link" href="#common-selftest_op-10">Full rule in this volume</a></p>
</li>
<li id="q-153-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>PEL has no generic per-self-test result event; use LID 06h. <a class="qa-rule-link" href="#common-selftest_op-11">Full rule in this volume</a></p>
</li>
<li id="q-153-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>CLR aborts a short test but an extended test must persist and resume after reset. <a class="qa-rule-link" href="#common-selftest_op-12">Full rule in this volume</a></p>
</li>
<li id="q-153-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Subsystem reset causes CLR on covered controllers: short tests abort and extended tests resume. <a class="qa-rule-link" href="#common-selftest_op-13">Full rule in this volume</a></p>
</li>
<li id="q-153-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Extended testing must resume after power restoration; short testing has no such continuation requirement. <a class="qa-rule-link" href="#common-selftest_op-14">Full rule in this volume</a></p>
</li>
<li id="q-153-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>The receiving controller runs the test and NSID selects coverage. <a class="qa-rule-link" href="#common-selftest_op-15">Full rule in this volume</a></p>
</li>
<li id="q-153-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Correlate external operations, test type and log cause.</p>
</li>
<li id="q-153-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First check extended-test continuation before expecting a reset-aborted entry.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-selftest">Base 2.4 §5.2.6, 8.1.8</a> · <a href="#ref-dstlog">Base 2.4 §5.2.13.1.7</a> · <a href="#ref-nvmselftest">NVM Command Set 1.3 §4.1.4.3</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-aerfull">Base 2.4 §5.2.2 (PCIe-applicable events)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-154" data-question="154"><h2><a class="qa-qid" href="#q-154">Q154</a> Does every self-test completion generate an AER?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-154-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-154-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Correct the implied premise: normal completion is established by the log, not a nonexistent generic completion event.</p>
</li>
<li id="q-154-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Initiation completion and later background completion are distinct and do not automatically create an AER.</p>
</li>
<li id="q-154-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Check self-test/LID 06h support and the separate Diagnostic Failure error event.</p>
</li>
<li id="q-154-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>Diagnostic Failure uses AET0/AEI02h and is distinct from DSTR.</p>
</li>
<li id="q-154-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Monitor operation/new result; correlate any diagnostic-error event and additional error information.</p>
</li>
<li id="q-154-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Normal completion without AER can conform; an error event still does not replace detailed results.</p>
</li>
<li id="q-154-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Do not fail compliance solely for absent generic completion AER or interpret any AER as success.</p>
</li>
<li id="q-154-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-154-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>There is no generic Device Self-test Completed AER. <a class="qa-rule-link" href="#common-selftest_op-9">Full rule in this volume</a></p>
</li>
<li id="q-154-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Short/extended completion or cancellation creates the newest result before returning current operation to idle. <a class="qa-rule-link" href="#common-selftest_op-10">Full rule in this volume</a></p>
</li>
<li id="q-154-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>PEL has no generic per-self-test result event; use LID 06h. <a class="qa-rule-link" href="#common-selftest_op-11">Full rule in this volume</a></p>
</li>
<li id="q-154-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>CLR aborts a short test but an extended test must persist and resume after reset. <a class="qa-rule-link" href="#common-selftest_op-12">Full rule in this volume</a></p>
</li>
<li id="q-154-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Subsystem reset causes CLR on covered controllers: short tests abort and extended tests resume. <a class="qa-rule-link" href="#common-selftest_op-13">Full rule in this volume</a></p>
</li>
<li id="q-154-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Extended testing must resume after power restoration; short testing has no such continuation requirement. <a class="qa-rule-link" href="#common-selftest_op-14">Full rule in this volume</a></p>
</li>
<li id="q-154-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>The receiving controller runs the test and NSID selects coverage. <a class="qa-rule-link" href="#common-selftest_op-15">Full rule in this volume</a></p>
</li>
<li id="q-154-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Validate defined events rather than transplanting Sanitize completion semantics.</p>
</li>
<li id="q-154-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First inspect whether the test expects an undefined event.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-selftest">Base 2.4 §5.2.6, 8.1.8</a> · <a href="#ref-dstlog">Base 2.4 §5.2.13.1.7</a> · <a href="#ref-nvmselftest">NVM Command Set 1.3 §4.1.4.3</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-aerfull">Base 2.4 §5.2.2 (PCIe-applicable events)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-155" data-question="155"><h2><a class="qa-qid" href="#q-155">Q155</a> When are segment, diagnostic and failing-LBA fields valid?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-155-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-155-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Nonzero fields need not be valid; validity bits prevent false precision.</p>
</li>
<li id="q-155-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>SEGN identifies an internal test segment and FLBA a logical block; they are not interchangeable.</p>
</li>
<li id="q-155-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Read DSTR and VDINFO validity bits before the corresponding fields.</p>
</li>
<li id="q-155-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>SEGN is the first known failed segment only for DSTR7; FVLD validates one failing LBA under NVM semantics.</p>
</li>
<li id="q-155-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Check nonempty result and valid bits before mapping namespace/LBA; do not invent namespace association.</p>
</li>
<li id="q-155-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Reporting one of several failing LBAs is valid; completeness or lowest-LBA ordering is not guaranteed.</p>
</li>
<li id="q-155-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Ignore invalid fields rather than validating their range, while valid contradictory data remains significant.</p>
</li>
<li id="q-155-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-155-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>There is no generic Device Self-test Completed AER. <a class="qa-rule-link" href="#common-selftest_op-9">Full rule in this volume</a></p>
</li>
<li id="q-155-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Short/extended completion or cancellation creates the newest result before returning current operation to idle. <a class="qa-rule-link" href="#common-selftest_op-10">Full rule in this volume</a></p>
</li>
<li id="q-155-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>PEL has no generic per-self-test result event; use LID 06h. <a class="qa-rule-link" href="#common-selftest_op-11">Full rule in this volume</a></p>
</li>
<li id="q-155-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>CLR aborts a short test but an extended test must persist and resume after reset. <a class="qa-rule-link" href="#common-selftest_op-12">Full rule in this volume</a></p>
</li>
<li id="q-155-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Subsystem reset causes CLR on covered controllers: short tests abort and extended tests resume. <a class="qa-rule-link" href="#common-selftest_op-13">Full rule in this volume</a></p>
</li>
<li id="q-155-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Extended testing must resume after power restoration; short testing has no such continuation requirement. <a class="qa-rule-link" href="#common-selftest_op-14">Full rule in this volume</a></p>
</li>
<li id="q-155-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>The receiving controller runs the test and NSID selects coverage. <a class="qa-rule-link" href="#common-selftest_op-15">Full rule in this volume</a></p>
</li>
<li id="q-155-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Distinguish unknown location from an inconsistent valid location using validity and format.</p>
</li>
<li id="q-155-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First inspect FVLD before diagnosing LBA0 from a zero value.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-selftest">Base 2.4 §5.2.6, 8.1.8</a> · <a href="#ref-dstlog">Base 2.4 §5.2.13.1.7</a> · <a href="#ref-nvmselftest">NVM Command Set 1.3 §4.1.4.3</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-aerfull">Base 2.4 §5.2.2 (PCIe-applicable events)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-156" data-question="156"><h2><a class="qa-qid" href="#q-156">Q156</a> How are the 20 self-test results ordered and replaced?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-156-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-156-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Fixed history supports recent diagnosis rather than a complete lifetime audit.</p>
</li>
<li id="q-156-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>LID 06h has 20 results of 28 bytes after a 4-byte current-status header.</p>
</li>
<li id="q-156-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Use structural and empty-entry rules, not an all-zero test.</p>
</li>
<li id="q-156-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>RDS1 is newest through RDS20 oldest; unused entries have DSTRFh/DSTC0 and other fields ignored.</p>
</li>
<li id="q-156-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Snapshot RDS1, then verify insertion and older-result displacement; history beyond 20 is no longer included.</p>
</li>
<li id="q-156-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>After the 21st result,20 structures still represent the recent history.</p>
</li>
<li id="q-156-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>STCFh with no active test leaves the log unchanged rather than inserting a synthetic cancellation result.</p>
</li>
<li id="q-156-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-156-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>There is no generic Device Self-test Completed AER. <a class="qa-rule-link" href="#common-selftest_op-9">Full rule in this volume</a></p>
</li>
<li id="q-156-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Short/extended completion or cancellation creates the newest result before returning current operation to idle. <a class="qa-rule-link" href="#common-selftest_op-10">Full rule in this volume</a></p>
</li>
<li id="q-156-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>PEL has no generic per-self-test result event; use LID 06h. <a class="qa-rule-link" href="#common-selftest_op-11">Full rule in this volume</a></p>
</li>
<li id="q-156-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>CLR aborts a short test but an extended test must persist and resume after reset. <a class="qa-rule-link" href="#common-selftest_op-12">Full rule in this volume</a></p>
</li>
<li id="q-156-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Subsystem reset causes CLR on covered controllers: short tests abort and extended tests resume. <a class="qa-rule-link" href="#common-selftest_op-13">Full rule in this volume</a></p>
</li>
<li id="q-156-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Extended testing must resume after power restoration; short testing has no such continuation requirement. <a class="qa-rule-link" href="#common-selftest_op-14">Full rule in this volume</a></p>
</li>
<li id="q-156-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>The receiving controller runs the test and NSID selects coverage. <a class="qa-rule-link" href="#common-selftest_op-15">Full rule in this volume</a></p>
</li>
<li id="q-156-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Compare code, outcome, hours and diagnostics rather than treating potentially repeated timestamps as unique IDs.</p>
</li>
<li id="q-156-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First ensure the transfer covers the full 564-byte structure rather than a truncated result list.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-selftest">Base 2.4 §5.2.6, 8.1.8</a> · <a href="#ref-dstlog">Base 2.4 §5.2.13.1.7</a> · <a href="#ref-nvmselftest">NVM Command Set 1.3 §4.1.4.3</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-aerfull">Base 2.4 §5.2.2 (PCIe-applicable events)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<section id="common-rules" class="qa-common"><h2>Shared rules linked from the answers</h2><p>Each shared mechanism is explained in full once in this volume. Use browser Back to return to the question; explicit command or feature exceptions take precedence.</p>
<article id="common-command-8"><h3>Command completion, events and records · How are DNR and More set?</h3><p>For a CQE, DNR=1 means the identical command is expected to fail if resubmitted to any controller in this subsystem; DNR=0 means it may succeed. Do not assign DNR=1 solely from an error name unless that condition mandates it. More=1 identifies additional information for this command in the Error Information Log. DNR should be zero when SCT=SC=0.</p></article>
<article id="common-selftest_op-9"><h3>Shared conditions for this topic · Is an asynchronous event generated?</h3><p>There is no generic Device Self-test Completed AER. Read LID 06h for normal completion; diagnostic failures separately follow Diagnostic Failure error-event conditions.</p></article>
<article id="common-selftest_op-10"><h3>Shared conditions for this topic · Are Error Information or other logs updated?</h3><p>Short/extended completion or cancellation creates the newest result before returning current operation to idle. Check diagnostic valid bits before NSID/LBA/SCT/SC.</p></article>
<article id="common-selftest_op-11"><h3>Shared conditions for this topic · Is it recorded in the Persistent Event Log?</h3><p>PEL has no generic per-self-test result event; use LID 06h. Separately qualifying hardware/reset events do not replace the self-test result.</p></article>
<article id="common-selftest_op-12"><h3>Shared conditions for this topic · What survives or continues after Controller Reset?</h3><p>CLR aborts a short test but an extended test must persist and resume after reset. The resume segment is vendor-specific; implementations should only need to repeat the interrupted last segment.</p></article>
<article id="common-selftest_op-13"><h3>Shared conditions for this topic · What survives or continues after NVM Subsystem Reset?</h3><p>Subsystem reset causes CLR on covered controllers: short tests abort and extended tests resume. Rebuilding Admin Queues is not restarting the entire extended test.</p></article>
<article id="common-selftest_op-14"><h3>Shared conditions for this topic · What survives or continues after a power cycle?</h3><p>Extended testing must resume after power restoration; short testing has no such continuation requirement. Read operation/progress/results rather than requiring reset-aborted results for both.</p></article>
<article id="common-selftest_op-15"><h3>Shared conditions for this topic · Are other controllers or namespaces affected?</h3><p>The receiving controller runs the test and NSID selects coverage. DSTO.SDSO determines controller/subsystem concurrency scope; shared resources may slow unrelated work.</p></article>
</section>
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
