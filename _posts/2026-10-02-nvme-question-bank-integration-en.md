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
<main id="content"><p class="qr-eyebrow">BASE 2.4 / NVM 1.3 / PCIe 1.4 · Q1–320</p>
<header><p class="qa-range">Q297–Q320</p><h1>Integrated validation and evidence correlation</h1><p class="qr-intro">Apply prior mechanisms to apparent contradictions, matching identity and time before judging evidence.</p><p>Practice first, then reveal 17 answer items per question. All numerical examples are hypothetical. Status is written SCT/SC; h indicates hexadecimal.</p></header>
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
<article class="qa-question" id="q-297" data-question="297"><h2><a class="qa-qid" href="#q-297">Q297</a> Where do you start when an advertised command fails?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-297-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-297-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Distinguish command support from legality and executability of this request.</p>
</li>
<li id="q-297-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Match controller, command set, namespace and time before comparing support.</p>
</li>
<li id="q-297-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Preserve Identify support, CSUPP and CSI/UUID selectors.</p>
</li>
<li id="q-297-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>If supported Format returns Invalid Format, compare its LBAF with the namespace’s formats.</p>
</li>
<li id="q-297-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Decode the CQE, then validate selectors, namespace state, protection and active-operation restrictions.</p>
</li>
<li id="q-297-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Rejecting an unsupported LBA format can be consistent with supporting Format.</p>
</li>
<li id="q-297-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Invalid Opcode with all prerequisites met warrants support-consistency investigation, not an automatic conclusion from any failure.</p>
</li>
<li id="q-297-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-297-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Normal completion here does not guarantee an AER; a separate defined event requires support, configuration and a pending request. <a class="qa-rule-link" href="#common-command-9">Full rule in this volume</a></p>
</li>
<li id="q-297-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Correlate the completion with error records under the shared entry-creation rules; do not infer entry count directly from the number of failures. <a class="qa-rule-link" href="#common-command-10">Full rule in this volume</a></p>
</li>
<li id="q-297-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>PEL is not a per-command trace; supported defined events are logged under their recording conditions. <a class="qa-rule-link" href="#common-command-11">Full rule in this volume</a></p>
</li>
<li id="q-297-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Controller Level Reset aborts outstanding commands and resets queues; do not wait for old CQEs. <a class="qa-rule-link" href="#common-error_review-12">Full rule in this volume</a></p>
</li>
<li id="q-297-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>A subsystem reset applies Controller Level Reset to affected controllers. <a class="qa-rule-link" href="#common-error_review-13">Full rule in this volume</a></p>
</li>
<li id="q-297-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>After a power cycle, rebuild queues and command tracking before checking actual data and operation state. <a class="qa-rule-link" href="#common-error_review-14">Full rule in this volume</a></p>
</li>
<li id="q-297-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>One command failure does not establish failure of other commands, namespaces or controllers. <a class="qa-rule-link" href="#common-error_review-15">Full rule in this volume</a></p>
</li>
<li id="q-297-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Use a contemporaneous valid control differing in one relevant condition.</p>
</li>
<li id="q-297-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First inspect SCT/SC rather than an application’s generic failure label.</p>
</li>
</ol>
<p class="qa-related">Related mechanisms: <a href="/nvme/question-bank/identify/en/#q-050">Q50</a> · <a href="/nvme/question-bank/logs/en/#q-081">Q81</a> · <a href="/nvme/question-bank/errors/en/#q-093">Q93</a></p>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-commandseffects">Base 2.4 §5.2.13.1.6</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-298" data-question="298"><h2><a class="qa-qid" href="#q-298">Q298</a> Does success of an unadvertised command prove compliance?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-298-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-298-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Success does not correct an inaccurate capability declaration.</p>
</li>
<li id="q-298-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Establish applicability to controller type, command set and query revision.</p>
</li>
<li id="q-298-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Compare the relevant discovery interface rather than unrelated capability bits.</p>
</li>
<li id="q-298-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>CSUPP0 and successful effective execution of that opcode under the same CSI require investigation.</p>
</li>
<li id="q-298-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Exclude stale snapshots, activation, opcode-category confusion and reserved-field misinterpretation.</p>
</li>
<li id="q-298-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Capability, completion and observable effects must agree.</p>
</li>
<li id="q-298-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Require rejection only where the specification defines unsupported behavior; inapplicable zero fields do not universally prohibit commands.</p>
</li>
<li id="q-298-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-298-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Normal completion here does not guarantee an AER; a separate defined event requires support, configuration and a pending request. <a class="qa-rule-link" href="#common-command-9">Full rule in this volume</a></p>
</li>
<li id="q-298-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Correlate the completion with error records under the shared entry-creation rules; do not infer entry count directly from the number of failures. <a class="qa-rule-link" href="#common-command-10">Full rule in this volume</a></p>
</li>
<li id="q-298-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>PEL is not a per-command trace; supported defined events are logged under their recording conditions. <a class="qa-rule-link" href="#common-command-11">Full rule in this volume</a></p>
</li>
<li id="q-298-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Controller Level Reset aborts outstanding commands and resets queues; do not wait for old CQEs. <a class="qa-rule-link" href="#common-error_review-12">Full rule in this volume</a></p>
</li>
<li id="q-298-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>A subsystem reset applies Controller Level Reset to affected controllers. <a class="qa-rule-link" href="#common-error_review-13">Full rule in this volume</a></p>
</li>
<li id="q-298-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>After a power cycle, rebuild queues and command tracking before checking actual data and operation state. <a class="qa-rule-link" href="#common-error_review-14">Full rule in this volume</a></p>
</li>
<li id="q-298-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>One command failure does not establish failure of other commands, namespaces or controllers. <a class="qa-rule-link" href="#common-error_review-15">Full rule in this volume</a></p>
</li>
<li id="q-298-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Preserve contradictory evidence and cite the exact declaration rule.</p>
</li>
<li id="q-298-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First compare discovery and execution selectors.</p>
</li>
</ol>
<p class="qa-related">Related mechanisms: <a href="/nvme/question-bank/identify/en/#q-048">Q48</a> · <a href="/nvme/question-bank/identify/en/#q-050">Q50</a> · <a href="/nvme/question-bank/logs/en/#q-080">Q80</a></p>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-commandseffects">Base 2.4 §5.2.13.1.6</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-299" data-question="299"><h2><a class="qa-qid" href="#q-299">Q299</a> How is a successful Set with different readback or behavior investigated?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-299-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-299-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Separate acceptance, current value, saved value and actual effect.</p>
</li>
<li id="q-299-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Feature scope determines the target that Get must match.</p>
</li>
<li id="q-299-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Check supported capabilities and whether the feature may adjust requested values.</p>
</li>
<li id="q-299-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>KATO may round up to KAS granularity, so a larger readback is not necessarily wrong.</p>
</li>
<li id="q-299-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Preserve Set selectors/data, read Current and separately test Saved/restoration.</p>
</li>
<li id="q-299-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Valid adjusted readback with matching behavior can be a passing result.</p>
</li>
<li id="q-299-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Correct selector mistakes before diagnosing unexplained same-target inconsistency.</p>
</li>
<li id="q-299-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-299-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Normal completion here does not guarantee an AER; a separate defined event requires support, configuration and a pending request. <a class="qa-rule-link" href="#common-command-9">Full rule in this volume</a></p>
</li>
<li id="q-299-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Correlate the completion with error records under the shared entry-creation rules; do not infer entry count directly from the number of failures. <a class="qa-rule-link" href="#common-command-10">Full rule in this volume</a></p>
</li>
<li id="q-299-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>Get does not itself produce a Set Feature event; Set requires FID logging support, successful completion and a check for a changed setting. <a class="qa-rule-link" href="#common-feature_events-11">Full rule in this volume</a></p>
</li>
<li id="q-299-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Use scope, saveability and reset coverage; whole-subsystem and partial resets differ. <a class="qa-rule-link" href="#common-feature-12">Full rule in this volume</a></p>
</li>
<li id="q-299-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Establish whole or partial subsystem coverage; non-saveable persistent values do not thereby become zero. <a class="qa-rule-link" href="#common-feature-13">Full rule in this volume</a></p>
</li>
<li id="q-299-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Saveable values restore Saved; non-saveable values require their persistence and feature-specific rules. <a class="qa-rule-link" href="#common-feature-14">Full rule in this volume</a></p>
</li>
<li id="q-299-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Feature scope determines whether other controllers or namespaces share the setting. <a class="qa-rule-link" href="#common-feature-15">Full rule in this volume</a></p>
</li>
<li id="q-299-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Track intervening configuration, resets and mode changes.</p>
</li>
<li id="q-299-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First check Current selection and feature scope.</p>
</li>
</ol>
<p class="qa-related">Related mechanisms: <a href="/nvme/question-bank/features/en/#q-054">Q54</a> · <a href="/nvme/question-bank/features/en/#q-055">Q55</a> · <a href="/nvme/question-bank/features/en/#q-066">Q66</a> · <a href="/nvme/question-bank/features/en/#q-068">Q68</a></p>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-featureeffects">Base 2.4 §5.2.13.1.18</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-300" data-question="300"><h2><a class="qa-qid" href="#q-300">Q300</a> Why might an AER completion have no matching visible log information?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-300-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-300-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>A notice identifies a qualifying event, while the log may expose current state rather than a historical snapshot.</p>
</li>
<li id="q-300-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Match log scope to the event’s endpoint and entity.</p>
</li>
<li id="q-300-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Preserve event type, information, LID and required selectors.</p>
</li>
<li id="q-300-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>A temperature warning may clear before a later SMART read without invalidating the earlier event.</p>
</li>
<li id="q-300-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Read the matching log and check intervening acknowledgments and state changes.</p>
</li>
<li id="q-300-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>A coherent timeline can explain cleared current state after a valid event.</p>
</li>
<li id="q-300-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Immediate, One-Shot and ordinary events have distinct clearing rules.</p>
</li>
<li id="q-300-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-300-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>AER reports an event by completing a request. <a class="qa-rule-link" href="#common-aer_request-9">Full rule in this volume</a></p>
</li>
<li id="q-300-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Use AET, AEI and LID to select the associated log. <a class="qa-rule-link" href="#common-aer_request-10">Full rule in this volume</a></p>
</li>
<li id="q-300-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>PEL logging depends on the underlying event, not on AER completion. <a class="qa-rule-link" href="#common-aer_request-11">Full rule in this volume</a></p>
</li>
<li id="q-300-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Controller Reset aborts outstanding AERs without CQEs. <a class="qa-rule-link" href="#common-aer_request-12">Full rule in this volume</a></p>
</li>
<li id="q-300-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>After subsystem reset, reestablish Admin Queues and AERs on affected controllers. <a class="qa-rule-link" href="#common-aer_request-13">Full rule in this volume</a></p>
</li>
<li id="q-300-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Old AERs are invalid after a power cycle. <a class="qa-rule-link" href="#common-aer_request-14">Full rule in this volume</a></p>
</li>
<li id="q-300-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Requests and completions belong to a controller, while event scope may be a namespace, domain or subsystem. <a class="qa-rule-link" href="#common-aer_request-15">Full rule in this volume</a></p>
</li>
<li id="q-300-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Preserve the first read and all acknowledgments before investigating persistent inconsistency.</p>
</li>
<li id="q-300-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First check LID, scope and observation delay.</p>
</li>
</ol>
<p class="qa-related">Related mechanisms: <a href="/nvme/question-bank/asynchronous-events/en/#q-083">Q83</a> · <a href="/nvme/question-bank/asynchronous-events/en/#q-084">Q84</a> · <a href="/nvme/question-bank/asynchronous-events/en/#q-090">Q90</a> · <a href="/nvme/question-bank/asynchronous-events/en/#q-092">Q92</a></p>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-aerfull">Base 2.4 §5.2.2 (PCIe-applicable events)</a> · <a href="#ref-getlog">Base 2.4 §5.2.13–5.2.13.1.1</a> · <a href="#ref-smart">Base 2.4 §5.2.13.1.3</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-301" data-question="301"><h2><a class="qa-qid" href="#q-301">Q301</a> Does every failed CQE require a new error entry?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-301-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-301-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Error Information is not a mandatory one-entry copy of every failed CQE.</p>
</li>
<li id="q-301-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Match controller and error counts, considering overwrite by concurrent failures.</p>
</li>
<li id="q-301-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Inspect More and command-specific logging requirements.</p>
</li>
<li id="q-301-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>More 1 indicates additional status information, while More 0 does not prohibit logging.</p>
</li>
<li id="q-301-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Compare before/after counts and correlate valid entries by command identity and status.</p>
</li>
<li id="q-301-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Absence can be compliant where no applicable mandatory logging requirement exists.</p>
</li>
<li id="q-301-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Explicit mandatory details, such as specified capacity failures, override general optionality.</p>
</li>
<li id="q-301-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-301-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Normal completion here does not guarantee an AER; a separate defined event requires support, configuration and a pending request. <a class="qa-rule-link" href="#common-command-9">Full rule in this volume</a></p>
</li>
<li id="q-301-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Correlate the completion with error records under the shared entry-creation rules; do not infer entry count directly from the number of failures. <a class="qa-rule-link" href="#common-command-10">Full rule in this volume</a></p>
</li>
<li id="q-301-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>PEL is not a per-command trace; supported defined events are logged under their recording conditions. <a class="qa-rule-link" href="#common-command-11">Full rule in this volume</a></p>
</li>
<li id="q-301-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Controller Level Reset aborts outstanding commands and resets queues; do not wait for old CQEs. <a class="qa-rule-link" href="#common-error_review-12">Full rule in this volume</a></p>
</li>
<li id="q-301-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>A subsystem reset applies Controller Level Reset to affected controllers. <a class="qa-rule-link" href="#common-error_review-13">Full rule in this volume</a></p>
</li>
<li id="q-301-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>After a power cycle, rebuild queues and command tracking before checking actual data and operation state. <a class="qa-rule-link" href="#common-error_review-14">Full rule in this volume</a></p>
</li>
<li id="q-301-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>One command failure does not establish failure of other commands, namespaces or controllers. <a class="qa-rule-link" href="#common-error_review-15">Full rule in this volume</a></p>
</li>
<li id="q-301-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Exclude overwrite, reset clearing and incomplete reads before declaring a missing record.</p>
</li>
<li id="q-301-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First establish this error’s exact logging requirement strength.</p>
</li>
</ol>
<p class="qa-related">Related mechanisms: <a href="/nvme/question-bank/errors/en/#q-099">Q99</a> · <a href="/nvme/question-bank/errors/en/#q-103">Q103</a></p>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-302" data-question="302"><h2><a class="qa-qid" href="#q-302">Q302</a> When do differing CQE, Error Information and PEL records conflict?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-302-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-302-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>The three records have different purposes and timing, not bytewise equivalence.</p>
</li>
<li id="q-302-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>CQEs describe commands, error entries add failure details and PEL describes persistent events.</p>
</li>
<li id="q-302-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Verify event support, More and command identity before correlating.</p>
</li>
<li id="q-302-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>Matching error status bits 15:1 match CQE status; phase follows its separate rule.</p>
</li>
<li id="q-302-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Correlate identity/time before parsing event-specific outcome fields.</p>
</li>
<li id="q-302-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Successful sanitize acceptance and later operation failure can both be correct.</p>
</li>
<li id="q-302-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Reused CIDs and requested-versus-completed values can create false contradictions.</p>
</li>
<li id="q-302-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-302-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Normal completion here does not guarantee an AER; a separate defined event requires support, configuration and a pending request. <a class="qa-rule-link" href="#common-command-9">Full rule in this volume</a></p>
</li>
<li id="q-302-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Correlate the completion with error records under the shared entry-creation rules; do not infer entry count directly from the number of failures. <a class="qa-rule-link" href="#common-command-10">Full rule in this volume</a></p>
</li>
<li id="q-302-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>PEL is not a per-command trace; supported defined events are logged under their recording conditions. <a class="qa-rule-link" href="#common-command-11">Full rule in this volume</a></p>
</li>
<li id="q-302-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Controller Level Reset aborts outstanding commands and resets queues; do not wait for old CQEs. <a class="qa-rule-link" href="#common-error_review-12">Full rule in this volume</a></p>
</li>
<li id="q-302-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>A subsystem reset applies Controller Level Reset to affected controllers. <a class="qa-rule-link" href="#common-error_review-13">Full rule in this volume</a></p>
</li>
<li id="q-302-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>After a power cycle, rebuild queues and command tracking before checking actual data and operation state. <a class="qa-rule-link" href="#common-error_review-14">Full rule in this volume</a></p>
</li>
<li id="q-302-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>One command failure does not establish failure of other commands, namespaces or controllers. <a class="qa-rule-link" href="#common-error_review-15">Full rule in this volume</a></p>
</li>
<li id="q-302-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Build an acceptance/start/operation-completion/query timeline.</p>
</li>
<li id="q-302-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First establish what each record actually proves.</p>
</li>
</ol>
<p class="qa-related">Related mechanisms: <a href="/nvme/question-bank/errors/en/#q-100">Q100</a> · <a href="/nvme/question-bank/errors/en/#q-101">Q101</a> · <a href="/nvme/question-bank/errors/en/#q-106">Q106</a> · <a href="/nvme/question-bank/persistent-events/en/#q-213">Q213</a></p>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-pelcontext">Base 2.4 §5.2.13.1.14–5.2.13.1.14.2.5 (exclude PCIe link/packet decoding)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-303" data-question="303"><h2><a class="qa-qid" href="#q-303">Q303</a> How are unexpected feature retention or lost saved values assessed?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-303-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-303-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Non-saveable does not mean nonpersistent, and unsaved current values need not survive power loss.</p>
</li>
<li id="q-303-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Compare feature scope with actual reset coverage.</p>
</li>
<li id="q-303-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Preserve capabilities, value classes and the last successful Set’s save bit.</p>
</li>
<li id="q-303-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>Namespace write protection has explicit retention despite being non-saveable.</p>
</li>
<li id="q-303-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Establish known saved state, apply a specific reset and requery the same target.</p>
</li>
<li id="q-303-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Pass criteria follow restoration rules and explicit exceptions, not universal zeroing.</p>
</li>
<li id="q-303-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Failed saves or intervening changes invalidate a simple lost-save diagnosis.</p>
</li>
<li id="q-303-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-303-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Normal completion here does not guarantee an AER; a separate defined event requires support, configuration and a pending request. <a class="qa-rule-link" href="#common-command-9">Full rule in this volume</a></p>
</li>
<li id="q-303-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Correlate the completion with error records under the shared entry-creation rules; do not infer entry count directly from the number of failures. <a class="qa-rule-link" href="#common-command-10">Full rule in this volume</a></p>
</li>
<li id="q-303-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>Get does not itself produce a Set Feature event; Set requires FID logging support, successful completion and a check for a changed setting. <a class="qa-rule-link" href="#common-feature_events-11">Full rule in this volume</a></p>
</li>
<li id="q-303-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Use scope, saveability and reset coverage; whole-subsystem and partial resets differ. <a class="qa-rule-link" href="#common-feature-12">Full rule in this volume</a></p>
</li>
<li id="q-303-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Establish whole or partial subsystem coverage; non-saveable persistent values do not thereby become zero. <a class="qa-rule-link" href="#common-feature-13">Full rule in this volume</a></p>
</li>
<li id="q-303-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Saveable values restore Saved; non-saveable values require their persistence and feature-specific rules. <a class="qa-rule-link" href="#common-feature-14">Full rule in this volume</a></p>
</li>
<li id="q-303-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Feature scope determines whether other controllers or namespaces share the setting. <a class="qa-rule-link" href="#common-feature-15">Full rule in this volume</a></p>
</li>
<li id="q-303-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Record saveability, persistence, reset source and coverage separately.</p>
</li>
<li id="q-303-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First check the successful save and feature-specific exceptions.</p>
</li>
</ol>
<p class="qa-related">Related mechanisms: <a href="/nvme/question-bank/features/en/#q-055">Q55</a> · <a href="/nvme/question-bank/features/en/#q-067">Q67</a> · <a href="/nvme/question-bank/integration/en/#q-318">Q318</a></p>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-304" data-question="304"><h2><a class="qa-qid" href="#q-304">Q304</a> How are namespace changes reconciled across Identify, lists and AER?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-304-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-304-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Identify exposes current configuration, the changed list identifies changes and AER prompts rediscovery.</p>
</li>
<li id="q-304-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Controllers can observe different changes according to attachment and notification rules.</p>
</li>
<li id="q-304-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Record support/enables, pending requests and before/after inventories.</p>
</li>
<li id="q-304-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>Attachment changes active inventory while creation changes allocated inventory.</p>
</li>
<li id="q-304-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Perform one operation, observe completion/notice and rediscover current state.</p>
</li>
<li id="q-304-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>A changed NSID need not still exist because deletion also requires rediscovery.</p>
</li>
<li id="q-304-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Overflow uses FFFFFFFFh and requires full rediscovery, not treating it as a real namespace.</p>
</li>
<li id="q-304-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-304-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Create/delete affect allocated inventory; attach/detach affect controller active lists. <a class="qa-rule-link" href="#common-namespace_op-9">Full rule in this volume</a></p>
</li>
<li id="q-304-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Identify lists establish current allocation/attachment; changed lists 04h/1Ch identify changes rather than complete state. <a class="qa-rule-link" href="#common-namespace_op-10">Full rule in this volume</a></p>
</li>
<li id="q-304-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>Supported Change Namespace 06h records defined management changes; do not treat attachment as creation/deletion. <a class="qa-rule-link" href="#common-namespace_op-11">Full rule in this volume</a></p>
</li>
<li id="q-304-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Completed configuration/attachment survives reset; command channels reset without deleting namespaces. <a class="qa-rule-link" href="#common-namespace_op-12">Full rule in this volume</a></p>
</li>
<li id="q-304-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Subsystem reset is not Restore Default Namespace Configuration. <a class="qa-rule-link" href="#common-namespace_op-13">Full rule in this volume</a></p>
</li>
<li id="q-304-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Completed namespace configuration/attachments persist. <a class="qa-rule-link" href="#common-namespace_op-14">Full rule in this volume</a></p>
</li>
<li id="q-304-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Creation/deletion changes inventory and attachment lists select affected controllers. <a class="qa-rule-link" href="#common-namespace_op-15">Full rule in this volume</a></p>
</li>
<li id="q-304-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Preserve the first list and distinguish the initiating endpoint from notified peers.</p>
</li>
<li id="q-304-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First identify the management operation class.</p>
</li>
</ol>
<p class="qa-related">Related mechanisms: <a href="/nvme/question-bank/namespace-management/en/#q-160">Q160</a> · <a href="/nvme/question-bank/namespace-management/en/#q-162">Q162</a> · <a href="/nvme/question-bank/namespace-management/en/#q-167">Q167</a> · <a href="/nvme/question-bank/namespace-management/en/#q-168">Q168</a></p>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-nsattach">Base 2.4 §5.2.24–5.2.25, 8.1.17–8.1.17.2</a> · <a href="#ref-changedlog">Base 2.4 §5.2.13.1.5</a> · <a href="#ref-aerfull">Base 2.4 §5.2.2 (PCIe-applicable events)</a> · <a href="#ref-nspelevent">Base 2.4 §5.2.13.1.14.2.6</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-305" data-question="305"><h2><a class="qa-qid" href="#q-305">Q305</a> How are unchanged firmware revision or slot fields assessed after activation?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-305-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-305-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Download, slot commit, scheduled activation and actual activation are distinct stages.</p>
</li>
<li id="q-305-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Slot/activation state may be shared within a domain.</p>
</li>
<li id="q-305-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Inspect capability, current/next active slots, slot revisions and current firmware revision.</p>
</li>
<li id="q-305-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>Preserve action/slot/status and execute the specifically required activation reset.</p>
</li>
<li id="q-305-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Verify commit, perform activation and rediscover current state.</p>
</li>
<li id="q-305-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Equal version strings do not alone prove activation failure.</p>
</li>
<li id="q-305-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Fallback and requested PEL revision are not proof of active new firmware.</p>
</li>
<li id="q-305-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-305-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Starting reset-free activation triggers Firmware Activation Starting on affected controllers when notices are enabled. <a class="qa-rule-link" href="#common-firmware_op-9">Full rule in this volume</a></p>
</li>
<li id="q-305-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Distinguish active and next-reset slots with Firmware Slot Information and confirm running revision through Identify.FR. <a class="qa-rule-link" href="#common-firmware_op-10">Full rule in this volume</a></p>
</li>
<li id="q-305-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>PEL Commit 02h records old/requested revisions, action, slot and status. <a class="qa-rule-link" href="#common-firmware_op-11">Full rule in this volume</a></p>
</li>
<li id="q-305-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>A CLR between download and completed Commit discards staged portions. <a class="qa-rule-link" href="#common-firmware_op-12">Full rule in this volume</a></p>
</li>
<li id="q-305-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Subsystem reset affects its covered controllers and satisfies a required subsystem-reset activation. <a class="qa-rule-link" href="#common-firmware_op-13">Full rule in this volume</a></p>
</li>
<li id="q-305-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Entering D3cold during activation Commit can resume with the old or newly activated image; verify it. <a class="qa-rule-link" href="#common-firmware_op-14">Full rule in this volume</a></p>
</li>
<li id="q-305-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Controllers in one domain share slots/image, covering the subsystem in a single-domain system. <a class="qa-rule-link" href="#common-firmware_op-15">Full rule in this volume</a></p>
</li>
<li id="q-305-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Reconcile pending/active slot, current revision and commit/reset events separately.</p>
</li>
<li id="q-305-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First verify action and activation mechanism.</p>
</li>
</ol>
<p class="qa-related">Related mechanisms: <a href="/nvme/question-bank/firmware-boot/en/#q-139">Q139</a> · <a href="/nvme/question-bank/firmware-boot/en/#q-140">Q140</a> · <a href="/nvme/question-bank/firmware-boot/en/#q-144">Q144</a></p>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-firmware">Base 2.4 §3.11–3.11.1, 5.2.9–5.2.10</a> · <a href="#ref-fwlog">Base 2.4 §5.2.13.1.4</a> · <a href="#ref-fwpel">Base 2.4 §5.2.13.1.14.2.2, 5.2.13.1.14.2.4</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-306" data-question="306"><h2><a class="qa-qid" href="#q-306">Q306</a> Is an in-progress log after sanitize command success an error?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-306-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-306-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Sanitize command completion acknowledges initiation, while media sanitization can continue in the background.</p>
</li>
<li id="q-306-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Match subsystem or namespace scope and result selection.</p>
</li>
<li id="q-306-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Inspect capabilities, command scope, status and supported completion events.</p>
</li>
<li id="q-306-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>Interpret progress with operation and verification state, not FFFFh alone.</p>
</li>
<li id="q-306-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Preserve initiation completion and poll state, then correlate final result with any completion event.</p>
</li>
<li id="q-306-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>In-progress after initiation is normal; final state must follow actual operation completion.</p>
</li>
<li id="q-306-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Exclude a newer operation, wrong scope and stale data before diagnosing a stuck status.</p>
</li>
<li id="q-306-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-306-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>State transitions report completed, unexpected-deallocation completion or media-verification entry with LID 81h. <a class="qa-rule-link" href="#common-sanitize_op-9">Full rule in this volume</a></p>
</li>
<li id="q-306-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Sanitize Status updates before the initiating CQE and on transitions, persisting across resets/power. <a class="qa-rule-link" href="#common-sanitize_op-10">Full rule in this volume</a></p>
</li>
<li id="q-306-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>Supported PEL logging records Start 09h on entering processing and Completion 0Ah on entering Idle or either failure state. <a class="qa-rule-link" href="#common-sanitize_op-11">Full rule in this volume</a></p>
</li>
<li id="q-306-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Background sanitization continues through Controller Level Reset. <a class="qa-rule-link" href="#common-sanitize_op-12">Full rule in this volume</a></p>
</li>
<li id="q-306-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Subsystem reset does not abort sanitization. <a class="qa-rule-link" href="#common-sanitize_op-13">Full rule in this volume</a></p>
</li>
<li id="q-306-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Processing cannot occur without power, but sanitization continues from retained state after power returns. <a class="qa-rule-link" href="#common-sanitize_op-14">Full rule in this volume</a></p>
</li>
<li id="q-306-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Subsystem sanitization restricts subsystem access; namespace sanitization targets one namespace across its controllers. <a class="qa-rule-link" href="#common-sanitize_op-15">Full rule in this volume</a></p>
</li>
<li id="q-306-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Correlate one operation across command, log, AER and PEL.</p>
</li>
<li id="q-306-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First identify what the claimed completion actually establishes.</p>
</li>
</ol>
<p class="qa-related">Related mechanisms: <a href="/nvme/question-bank/format-sanitize/en/#q-128">Q128</a> · <a href="/nvme/question-bank/format-sanitize/en/#q-130">Q130</a> · <a href="/nvme/question-bank/format-sanitize/en/#q-131">Q131</a> · <a href="/nvme/question-bank/format-sanitize/en/#q-133">Q133</a></p>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-sanitizecmd">Base 2.4 §5.2.26–5.2.27</a> · <a href="#ref-sanitizelog">Base 2.4 §5.2.13.1.38</a> · <a href="#ref-sanitizestate">Base 2.4 §8.1.27.1–8.1.27.5</a> · <a href="#ref-sanitizepel">Base 2.4 §5.2.13.1.14.2.9–5.2.13.1.14.2.10</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-307" data-question="307"><h2><a class="qa-qid" href="#q-307">Q307</a> How is a missing result after self-test investigated?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-307-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-307-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Start-command success is not test success; current operation and result history establish the outcome.</p>
</li>
<li id="q-307-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Match controller/shared-test scope and read the complete log correctly.</p>
</li>
<li id="q-307-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Inspect support/options/time and LID 06h&#x27;s 20 newest-first result slots.</p>
</li>
<li id="q-307-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>Current state, progress, result code, test code and validity bits have distinct roles.</p>
</li>
<li id="q-307-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Capture history, run one test and compare the newest result after completion.</p>
</li>
<li id="q-307-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Result update and return to idle follow the specified ordering for a test that produces a result.</p>
</li>
<li id="q-307-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>An Abort while idle can succeed without creating a test result.</p>
</li>
<li id="q-307-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-307-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>There is no generic Device Self-test Completed AER. <a class="qa-rule-link" href="#common-selftest_op-9">Full rule in this volume</a></p>
</li>
<li id="q-307-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Short/extended completion or cancellation creates the newest result before returning current operation to idle. <a class="qa-rule-link" href="#common-selftest_op-10">Full rule in this volume</a></p>
</li>
<li id="q-307-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>PEL has no generic per-self-test result event; use LID 06h. <a class="qa-rule-link" href="#common-selftest_op-11">Full rule in this volume</a></p>
</li>
<li id="q-307-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>CLR aborts a short test but an extended test must persist and resume after reset. <a class="qa-rule-link" href="#common-selftest_op-12">Full rule in this volume</a></p>
</li>
<li id="q-307-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Subsystem reset causes CLR on covered controllers: short tests abort and extended tests resume. <a class="qa-rule-link" href="#common-selftest_op-13">Full rule in this volume</a></p>
</li>
<li id="q-307-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Extended testing must resume after power restoration; short testing has no such continuation requirement. <a class="qa-rule-link" href="#common-selftest_op-14">Full rule in this volume</a></p>
</li>
<li id="q-307-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>The receiving controller runs the test and NSID selects coverage. <a class="qa-rule-link" href="#common-selftest_op-15">Full rule in this volume</a></p>
</li>
<li id="q-307-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Interpret reset effects using the distinct short/extended-test rules.</p>
</li>
<li id="q-307-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First establish that a test actually started.</p>
</li>
</ol>
<p class="qa-related">Related mechanisms: <a href="/nvme/question-bank/self-test/en/#q-152">Q152</a> · <a href="/nvme/question-bank/self-test/en/#q-153">Q153</a> · <a href="/nvme/question-bank/self-test/en/#q-155">Q155</a> · <a href="/nvme/question-bank/self-test/en/#q-156">Q156</a></p>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-selftest">Base 2.4 §5.2.6, 8.1.8</a> · <a href="#ref-dstlog">Base 2.4 §5.2.13.1.7</a> · <a href="#ref-nvmselftest">NVM Command Set 1.3 §4.1.4.3</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-308" data-question="308"><h2><a class="qa-qid" href="#q-308">Q308</a> How are unexpected unsafe-shutdown counts assessed?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-308-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-308-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Count behavior depends on state at main-power loss, not only the requested shutdown type.</p>
</li>
<li id="q-308-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Base 2.4 UPL counts qualifying power losses, not host shutdown calls.</p>
</li>
<li id="q-308-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Preserve count, request, status and actual power-loss time.</p>
</li>
<li id="q-308-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>Ordinary qualification concerns main-power loss before SHST10b, with a separate applicable out-of-band ignore-shutdown case.</p>
</li>
<li id="q-308-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Read baseline, request shutdown, observe status and compare after controlled power cycling.</p>
</li>
<li id="q-308-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Abrupt shutdown can complete before power loss and need not increment UPL each time.</p>
</li>
<li id="q-308-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Incomplete normal shutdown may qualify, while controller reset without power loss does not automatically count.</p>
</li>
<li id="q-308-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>This MMIO access has no NVMe CQE, so DNR/More do not apply. <a class="qa-rule-link" href="#common-register-8">Full rule in this volume</a></p>
</li>
<li id="q-308-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Register access has no success event; separate hardware errors use their event conditions. <a class="qa-rule-link" href="#common-register-9">Full rule in this volume</a></p>
</li>
<li id="q-308-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Register accesses are not logged individually; preserve registers and timing before obtaining available diagnostics. <a class="qa-rule-link" href="#common-register-10">Full rule in this volume</a></p>
</li>
<li id="q-308-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>Ordinary register access is not a PEL event; completed resets and supported hardware errors are assessed separately. <a class="qa-rule-link" href="#common-register-11">Full rule in this volume</a></p>
</li>
<li id="q-308-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Clearing CC.EN invalidates I/O queues and resets Admin pointers; retained base addresses do not validate old completions. <a class="qa-rule-link" href="#common-queue-12">Full rule in this volume</a></p>
</li>
<li id="q-308-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Rebuild affected-controller queues; do not assume CC.EN-reset register-retention exceptions. <a class="qa-rule-link" href="#common-queue-13">Full rule in this volume</a></p>
</li>
<li id="q-308-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Initialize queues and host tracking again; residual memory is not valid command state for a new lifetime. <a class="qa-rule-link" href="#common-queue-14">Full rule in this volume</a></p>
</li>
<li id="q-308-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Controller Reset targets one controller; subsystem reset covers one/all domains as defined for the implementation. <a class="qa-rule-link" href="#common-reset_review-15">Full rule in this volume</a></p>
</li>
<li id="q-308-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Use pre-loss state rather than post-restart SHST.</p>
</li>
<li id="q-308-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First establish actual main-power loss and SHST at that moment.</p>
</li>
</ol>
<p class="qa-related">Related mechanisms: <a href="/nvme/question-bank/reset-shutdown/en/#q-183">Q183</a> · <a href="/nvme/question-bank/reset-shutdown/en/#q-184">Q184</a> · <a href="/nvme/question-bank/reset-shutdown/en/#q-186">Q186</a> · <a href="/nvme/question-bank/health/en/#q-199">Q199</a></p>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-smart">Base 2.4 §5.2.13.1.3</a> · <a href="#ref-shutdownfull">Base 2.4 §3.6–3.6.1 (memory-based scope and shutdown)</a> · <a href="#ref-pciereset">PCIe Transport 1.4 §3.3</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-309" data-question="309"><h2><a class="qa-qid" href="#q-309">Q309</a> Which settings explain a warning change without an AER?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-309-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-309-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>State transitions and event conditions differ; clearing a warning need not mirror assertion.</p>
</li>
<li id="q-309-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Aggregate and group-specific warnings use different scopes/settings.</p>
</li>
<li id="q-309-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Check support/enables, pending AERs and unacknowledged prior events.</p>
</li>
<li id="q-309-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>Preserve warning bits, measured values and thresholds rather than only UI labels.</p>
</li>
<li id="q-309-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Verify qualifying conditions, competing/coalesced events and acknowledgment reads.</p>
</li>
<li id="q-309-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Qualifying enabled events follow their queuing rules, not one AER per sampled fluctuation.</p>
</li>
<li id="q-309-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>No pending request means no immediate CQE; unconsumed completions are not missing notifications.</p>
</li>
<li id="q-309-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-309-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>AER reports an event by completing a request. <a class="qa-rule-link" href="#common-aer_request-9">Full rule in this volume</a></p>
</li>
<li id="q-309-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Use AET, AEI and LID to select the associated log. <a class="qa-rule-link" href="#common-aer_request-10">Full rule in this volume</a></p>
</li>
<li id="q-309-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>PEL logging depends on the underlying event, not on AER completion. <a class="qa-rule-link" href="#common-aer_request-11">Full rule in this volume</a></p>
</li>
<li id="q-309-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Controller Reset aborts outstanding AERs without CQEs. <a class="qa-rule-link" href="#common-aer_request-12">Full rule in this volume</a></p>
</li>
<li id="q-309-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>After subsystem reset, reestablish Admin Queues and AERs on affected controllers. <a class="qa-rule-link" href="#common-aer_request-13">Full rule in this volume</a></p>
</li>
<li id="q-309-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Old AERs are invalid after a power cycle. <a class="qa-rule-link" href="#common-aer_request-14">Full rule in this volume</a></p>
</li>
<li id="q-309-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Requests and completions belong to a controller, while event scope may be a namespace, domain or subsystem. <a class="qa-rule-link" href="#common-aer_request-15">Full rule in this volume</a></p>
</li>
<li id="q-309-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Correlate warning, configuration, requests and acknowledgments.</p>
</li>
<li id="q-309-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First verify AEC at event time.</p>
</li>
</ol>
<p class="qa-related">Related mechanisms: <a href="/nvme/question-bank/features/en/#q-061">Q61</a> · <a href="/nvme/question-bank/asynchronous-events/en/#q-088">Q88</a> · <a href="/nvme/question-bank/health/en/#q-196">Q196</a> · <a href="/nvme/question-bank/health/en/#q-202">Q202</a></p>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-smart">Base 2.4 §5.2.13.1.3</a> · <a href="#ref-aerfull">Base 2.4 §5.2.2 (PCIe-applicable events)</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-310" data-question="310"><h2><a class="qa-qid" href="#q-310">Q310</a> How is apparent PEL event-order mismatch investigated?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-310-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-310-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Log order, event timestamp and real operation order are distinct.</p>
</li>
<li id="q-310-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Subsystem PEL can interleave controllers and permits defined vendor ordering.</p>
</li>
<li id="q-310-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Inspect reporting context, generation and clock origin/synchronization.</p>
</li>
<li id="q-310-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>Host changes and restoration can move timestamps, so they are not universal monotonic sequence numbers.</p>
</li>
<li id="q-310-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Read one consistent context, parse lengths and account for clock-change/reset events.</p>
</li>
<li id="q-310-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Newest-first is recommended with vendor-defined ordering allowed, not an unconditional mandate.</p>
</li>
<li id="q-310-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Mixed contexts and incorrect event-length accounting can create false disorder.</p>
</li>
<li id="q-310-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-310-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Base 2.4 does not define a generic PEL Changed AER for every appended entry. <a class="qa-rule-link" href="#common-pel_query-9">Full rule in this volume</a></p>
</li>
<li id="q-310-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>A context fixes the reported event set. <a class="qa-rule-link" href="#common-pel_query-10">Full rule in this volume</a></p>
</li>
<li id="q-310-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>PEL retrieval is not itself a PEL read event. <a class="qa-rule-link" href="#common-pel_query-11">Full rule in this volume</a></p>
</li>
<li id="q-310-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Event content survives CLR; the reporting context need not. <a class="qa-rule-link" href="#common-pel_query-12">Full rule in this volume</a></p>
</li>
<li id="q-310-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Subsystem reset preserves events and may add the supported Power-on or Reset event at completion; establish a fresh consistent reporting context. <a class="qa-rule-link" href="#common-pel_query-13">Full rule in this volume</a></p>
</li>
<li id="q-310-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Events persist across power cycles, with minimal power-failure loss recommended. <a class="qa-rule-link" href="#common-pel_query-14">Full rule in this volume</a></p>
</li>
<li id="q-310-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>PEL is subsystem-global. <a class="qa-rule-link" href="#common-pel_query-15">Full rule in this volume</a></p>
</li>
<li id="q-310-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Use a host monotonic timeline as evidence without equating unsynchronized clocks.</p>
</li>
<li id="q-310-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First verify context and event boundaries.</p>
</li>
</ol>
<p class="qa-related">Related mechanisms: <a href="/nvme/question-bank/persistent-events/en/#q-213">Q213</a> · <a href="/nvme/question-bank/persistent-events/en/#q-214">Q214</a> · <a href="/nvme/question-bank/persistent-events/en/#q-215">Q215</a> · <a href="/nvme/question-bank/persistent-events/en/#q-216">Q216</a></p>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-pelcontext">Base 2.4 §5.2.13.1.14–5.2.13.1.14.2.5 (exclude PCIe link/packet decoding)</a> · <a href="#ref-nvmpel">NVM Command Set 1.3 §4.1.4.4</a> · <a href="#ref-timestamp">Base 2.4 §5.2.30.1.8</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-311" data-question="311"><h2><a class="qa-qid" href="#q-311">Q311</a> What evidence remains when CFS is set with little diagnostic information?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-311-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-311-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Fatal conditions may break diagnostics; absent logs do not invalidate CFS or justify unlimited further commands.</p>
</li>
<li id="q-311-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Distinguish fatal failure from a secondary controller’s Offline state.</p>
</li>
<li id="q-311-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Preserve accessible controller state, capabilities and recent management history.</p>
</li>
<li id="q-311-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>Obtain available diagnostics without assuming every CFS cause has a readable dedicated record.</p>
</li>
<li id="q-311-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Preserve evidence before reset/recovery, then query surviving records.</p>
</li>
<li id="q-311-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Reinitialize and verify recovery while retaining uncertainty about interrupted commands.</p>
</li>
<li id="q-311-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Unreliable/all-ones reads are not automatically valid NVMe state.</p>
</li>
<li id="q-311-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>This MMIO access has no NVMe CQE, so DNR/More do not apply. <a class="qa-rule-link" href="#common-register-8">Full rule in this volume</a></p>
</li>
<li id="q-311-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Register access has no success event; separate hardware errors use their event conditions. <a class="qa-rule-link" href="#common-register-9">Full rule in this volume</a></p>
</li>
<li id="q-311-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Register accesses are not logged individually; preserve registers and timing before obtaining available diagnostics. <a class="qa-rule-link" href="#common-register-10">Full rule in this volume</a></p>
</li>
<li id="q-311-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>Ordinary register access is not a PEL event; completed resets and supported hardware errors are assessed separately. <a class="qa-rule-link" href="#common-register-11">Full rule in this volume</a></p>
</li>
<li id="q-311-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Clearing CC.EN invalidates I/O queues and resets Admin pointers; retained base addresses do not validate old completions. <a class="qa-rule-link" href="#common-queue-12">Full rule in this volume</a></p>
</li>
<li id="q-311-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Rebuild affected-controller queues; do not assume CC.EN-reset register-retention exceptions. <a class="qa-rule-link" href="#common-queue-13">Full rule in this volume</a></p>
</li>
<li id="q-311-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Initialize queues and host tracking again; residual memory is not valid command state for a new lifetime. <a class="qa-rule-link" href="#common-queue-14">Full rule in this volume</a></p>
</li>
<li id="q-311-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Controller Reset targets one controller; subsystem reset covers one/all domains as defined for the implementation. <a class="qa-rule-link" href="#common-reset_review-15">Full rule in this volume</a></p>
</li>
<li id="q-311-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Separate device status, host timeout and communication-failure evidence.</p>
</li>
<li id="q-311-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First establish role and register-read validity.</p>
</li>
</ol>
<p class="qa-related">Related mechanisms: <a href="/nvme/question-bank/initialization/en/#q-006">Q6</a> · <a href="/nvme/question-bank/errors/en/#q-105">Q105</a> · <a href="/nvme/question-bank/recovery/en/#q-117">Q117</a></p>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-cc">Base 2.4 §3.1.4 (CC, CSTS, NSSR)</a> · <a href="#ref-ready">Base 2.4 §3.5.3–3.5.4</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-smart">Base 2.4 §5.2.13.1.3</a> · <a href="#ref-pelcontext">Base 2.4 §5.2.13.1.14–5.2.13.1.14.2.5 (exclude PCIe link/packet decoding)</a> · <a href="#ref-virtual">Base 2.4 §8.2.7</a> · <a href="#ref-commrecovery">Base 2.4 §9.1–9.6.2.1 (PCIe-applicable rules; stop before 9.6.2.2)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-312" data-question="312"><h2><a class="qa-qid" href="#q-312">Q312</a> How are two observed completions after Abort classified?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-312-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-312-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Abort and its target each complete; two total CQEs can be normal, unlike duplicate target completion.</p>
</li>
<li id="q-312-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Identify commands by endpoint, SQID/CID and queue lifetime.</p>
</li>
<li id="q-312-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Record target identity, Abort’s own identity and IANP.</p>
</li>
<li id="q-312-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>IANP semantics do not erase the target’s completion, and IANP1 permits later normal completion.</p>
</li>
<li id="q-312-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Separate Abort and target CQEs, then exclude host double-consumption.</p>
</li>
<li id="q-312-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Handle one completion for each command without assuming the target had no effects.</p>
</li>
<li id="q-312-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Two genuine completions for the same target in one lifetime violate single-completion tracking.</p>
</li>
<li id="q-312-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-312-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Normal completion here does not guarantee an AER; a separate defined event requires support, configuration and a pending request. <a class="qa-rule-link" href="#common-command-9">Full rule in this volume</a></p>
</li>
<li id="q-312-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Correlate the completion with error records under the shared entry-creation rules; do not infer entry count directly from the number of failures. <a class="qa-rule-link" href="#common-command-10">Full rule in this volume</a></p>
</li>
<li id="q-312-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>PEL is not a per-command trace; supported defined events are logged under their recording conditions. <a class="qa-rule-link" href="#common-command-11">Full rule in this volume</a></p>
</li>
<li id="q-312-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Clearing CC.EN invalidates I/O queues and resets Admin pointers; retained base addresses do not validate old completions. <a class="qa-rule-link" href="#common-queue-12">Full rule in this volume</a></p>
</li>
<li id="q-312-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Rebuild affected-controller queues; do not assume CC.EN-reset register-retention exceptions. <a class="qa-rule-link" href="#common-queue-13">Full rule in this volume</a></p>
</li>
<li id="q-312-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Initialize queues and host tracking again; residual memory is not valid command state for a new lifetime. <a class="qa-rule-link" href="#common-queue-14">Full rule in this volume</a></p>
</li>
<li id="q-312-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Queues belong to a controller; CQ capacity and lifetime affect all SQs sharing it. <a class="qa-rule-link" href="#common-queue-15">Full rule in this volume</a></p>
</li>
<li id="q-312-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Exclude CID reuse and CQ wrap before declaring duplicates.</p>
</li>
<li id="q-312-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First identify which completion belongs to Abort itself.</p>
</li>
</ol>
<p class="qa-related">Related mechanisms: <a href="/nvme/question-bank/recovery/en/#q-107">Q107</a> · <a href="/nvme/question-bank/recovery/en/#q-110">Q110</a> · <a href="/nvme/question-bank/recovery/en/#q-112">Q112</a></p>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-abort">Base 2.4 §5.2.1</a> · <a href="#ref-cqe">Base 2.4 §4.2.1, 4.2.3–4.2.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-313" data-question="313"><h2><a class="qa-qid" href="#q-313">Q313</a> What is wrong with queue-memory access after completed deletion?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-313-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-313-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Access after the queue lifetime can corrupt memory already reused elsewhere.</p>
</li>
<li id="q-313-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Distinguish deleted queue memory from buffers belonging to other live commands.</p>
</li>
<li id="q-313-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Preserve target QID, successful deletion completion and memory range.</p>
</li>
<li id="q-313-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>Submission is not successful deletion, and SQ/CQ dependencies differ.</p>
</li>
<li id="q-313-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Check accesses after success and exclude legitimate address reuse by another queue.</p>
</li>
<li id="q-313-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>After retirement, the controller must not continue using it as the deleted queue.</p>
</li>
<li id="q-313-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Such access can corrupt host data or produce invalid command/completion behavior.</p>
</li>
<li id="q-313-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-313-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Normal completion here does not guarantee an AER; a separate defined event requires support, configuration and a pending request. <a class="qa-rule-link" href="#common-command-9">Full rule in this volume</a></p>
</li>
<li id="q-313-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Correlate the completion with error records under the shared entry-creation rules; do not infer entry count directly from the number of failures. <a class="qa-rule-link" href="#common-command-10">Full rule in this volume</a></p>
</li>
<li id="q-313-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>PEL is not a per-command trace; supported defined events are logged under their recording conditions. <a class="qa-rule-link" href="#common-command-11">Full rule in this volume</a></p>
</li>
<li id="q-313-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Clearing CC.EN invalidates I/O queues and resets Admin pointers; retained base addresses do not validate old completions. <a class="qa-rule-link" href="#common-queue-12">Full rule in this volume</a></p>
</li>
<li id="q-313-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Rebuild affected-controller queues; do not assume CC.EN-reset register-retention exceptions. <a class="qa-rule-link" href="#common-queue-13">Full rule in this volume</a></p>
</li>
<li id="q-313-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Initialize queues and host tracking again; residual memory is not valid command state for a new lifetime. <a class="qa-rule-link" href="#common-queue-14">Full rule in this volume</a></p>
</li>
<li id="q-313-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Queues belong to a controller; CQ capacity and lifetime affect all SQs sharing it. <a class="qa-rule-link" href="#common-queue-15">Full rule in this volume</a></p>
</li>
<li id="q-313-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Preserve reuse timing and queue identities; address equality alone is insufficient.</p>
</li>
<li id="q-313-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First establish successful deletion completion.</p>
</li>
</ol>
<p class="qa-related">Related mechanisms: <a href="/nvme/question-bank/queues/en/#q-019">Q19</a> · <a href="/nvme/question-bank/memory/en/#q-227">Q227</a> · <a href="/nvme/question-bank/interrupts/en/#q-295">Q295</a></p>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-delete">Base 2.4 §5.3.3–5.3.4</a> · <a href="#ref-create">Base 2.4 §5.3.1–5.3.2</a> · <a href="#ref-retirement">PCIe Transport 1.4 §3.4 (Command Related Resource Retirement)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-314" data-question="314"><h2><a class="qa-qid" href="#q-314">Q314</a> How should a CQE from before reset be handled?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-314-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-314-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Residual memory differs from a newly posted stale completion after reset.</p>
</li>
<li id="q-314-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Reset ends old queue lifetimes even when addresses and identifiers are reused.</p>
</li>
<li id="q-314-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Inspect reset source, readiness transitions, CQ initialization and expected phase.</p>
</li>
<li id="q-314-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>Rebuild command tracking without associating an old CID with a new request.</p>
</li>
<li id="q-314-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Finish reset and initialize memory before accepting valid new-lifetime completions.</p>
</li>
<li id="q-314-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Ignore stale completions while separately resolving possible prior media effects.</p>
</li>
<li id="q-314-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>New writes to a retired queue require investigation, unlike passive residual bytes.</p>
</li>
<li id="q-314-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-314-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Normal completion here does not guarantee an AER; a separate defined event requires support, configuration and a pending request. <a class="qa-rule-link" href="#common-command-9">Full rule in this volume</a></p>
</li>
<li id="q-314-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Correlate the completion with error records under the shared entry-creation rules; do not infer entry count directly from the number of failures. <a class="qa-rule-link" href="#common-command-10">Full rule in this volume</a></p>
</li>
<li id="q-314-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>PEL is not a per-command trace; supported defined events are logged under their recording conditions. <a class="qa-rule-link" href="#common-command-11">Full rule in this volume</a></p>
</li>
<li id="q-314-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Clearing CC.EN invalidates I/O queues and resets Admin pointers; retained base addresses do not validate old completions. <a class="qa-rule-link" href="#common-queue-12">Full rule in this volume</a></p>
</li>
<li id="q-314-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Rebuild affected-controller queues; do not assume CC.EN-reset register-retention exceptions. <a class="qa-rule-link" href="#common-queue-13">Full rule in this volume</a></p>
</li>
<li id="q-314-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Initialize queues and host tracking again; residual memory is not valid command state for a new lifetime. <a class="qa-rule-link" href="#common-queue-14">Full rule in this volume</a></p>
</li>
<li id="q-314-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Queues belong to a controller; CQ capacity and lifetime affect all SQs sharing it. <a class="qa-rule-link" href="#common-queue-15">Full rule in this volume</a></p>
</li>
<li id="q-314-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Correlate initialization and write timing to distinguish stale storage from late access.</p>
</li>
<li id="q-314-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First verify phase and command-tracking initialization.</p>
</li>
</ol>
<p class="qa-related">Related mechanisms: <a href="/nvme/question-bank/initialization/en/#q-009">Q9</a> · <a href="/nvme/question-bank/queues/en/#q-021">Q21</a> · <a href="/nvme/question-bank/recovery/en/#q-115">Q115</a> · <a href="/nvme/question-bank/reset-shutdown/en/#q-179">Q179</a></p>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-cqe">Base 2.4 §4.2.1, 4.2.3–4.2.4</a> · <a href="#ref-pciereset">PCIe Transport 1.4 §3.3</a> · <a href="#ref-commrecovery">Base 2.4 §9.1–9.6.2.1 (PCIe-applicable rules; stop before 9.6.2.2)</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-315" data-question="315"><h2><a class="qa-qid" href="#q-315">Q315</a> When can command success after detach be reasonable?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-315-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-315-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Submission acceptance is not successful execution, and some queries can address allocated inactive namespaces.</p>
</li>
<li id="q-315-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Detach affects selected endpoints, not every attached path.</p>
</li>
<li id="q-315-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Verify completed detach through both views.</p>
</li>
<li id="q-315-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>Distinguish ordinary I/O from allocated-namespace queries and special management commands.</p>
</li>
<li id="q-315-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Submit a new command after successful detach on the detached endpoint.</p>
</li>
<li id="q-315-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Success on another attached path or an allowed allocated query can be normal.</p>
</li>
<li id="q-315-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Applicable inactive-namespace commands require Invalid Field absent an exception, distinct from invalid-NSID status.</p>
</li>
<li id="q-315-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-315-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Create/delete affect allocated inventory; attach/detach affect controller active lists. <a class="qa-rule-link" href="#common-namespace_op-9">Full rule in this volume</a></p>
</li>
<li id="q-315-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Identify lists establish current allocation/attachment; changed lists 04h/1Ch identify changes rather than complete state. <a class="qa-rule-link" href="#common-namespace_op-10">Full rule in this volume</a></p>
</li>
<li id="q-315-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>Supported Change Namespace 06h records defined management changes; do not treat attachment as creation/deletion. <a class="qa-rule-link" href="#common-namespace_op-11">Full rule in this volume</a></p>
</li>
<li id="q-315-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Completed configuration/attachment survives reset; command channels reset without deleting namespaces. <a class="qa-rule-link" href="#common-namespace_op-12">Full rule in this volume</a></p>
</li>
<li id="q-315-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Subsystem reset is not Restore Default Namespace Configuration. <a class="qa-rule-link" href="#common-namespace_op-13">Full rule in this volume</a></p>
</li>
<li id="q-315-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Completed namespace configuration/attachments persist. <a class="qa-rule-link" href="#common-namespace_op-14">Full rule in this volume</a></p>
</li>
<li id="q-315-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Creation/deletion changes inventory and attachment lists select affected controllers. <a class="qa-rule-link" href="#common-namespace_op-15">Full rule in this volume</a></p>
</li>
<li id="q-315-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Separate outstanding and newly submitted commands when assessing detach effects.</p>
</li>
<li id="q-315-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First check endpoint and active-namespace requirement.</p>
</li>
</ol>
<p class="qa-related">Related mechanisms: <a href="/nvme/question-bank/namespace-management/en/#q-164">Q164</a> · <a href="/nvme/question-bank/namespace-management/en/#q-165">Q165</a></p>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-nsattach">Base 2.4 §5.2.24–5.2.25, 8.1.17–8.1.17.2</a> · <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-316" data-question="316"><h2><a class="qa-qid" href="#q-316">Q316</a> How is apparent Lockdown bypass investigated?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-316-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-316-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>A prohibition matches interface, controller scope and command/feature target together.</p>
</li>
<li id="q-316-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Scope selectors jointly define the target, not opcode alone.</p>
</li>
<li id="q-316-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Read supported/current prohibitions under matching selectors.</p>
</li>
<li id="q-316-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>Feature scope prohibits Set, not automatically Get; enhanced aggregate ACNTL0 is not no prohibition.</p>
</li>
<li id="q-316-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Test an exact matching target plus an allowed control after successful Lockdown.</p>
</li>
<li id="q-316-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>A prohibited matching Admin command requires 0/23h.</p>
</li>
<li id="q-316-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Exclude expiry, later allowance, mismatched interfaces and explicit personality exceptions.</p>
</li>
<li id="q-316-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-316-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Lockdown success defines no generic configuration-complete AER. <a class="qa-rule-link" href="#common-lockdown_op-9">Full rule in this volume</a></p>
</li>
<li id="q-316-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Current prohibitions should reflect success under matching interface/scope/controller/UUID selectors; denied commands use ordinary error-log correlation. <a class="qa-rule-link" href="#common-lockdown_op-10">Full rule in this volume</a></p>
</li>
<li id="q-316-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>Lockdown itself has no dedicated standard PEL event. <a class="qa-rule-link" href="#common-lockdown_op-11">Full rule in this volume</a></p>
</li>
<li id="q-316-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Ordinary CLR does not remove a successful prohibition; removal requires an allowed subsequent Lockdown or its specified power-cycle condition. <a class="qa-rule-link" href="#common-lockdown_op-12">Full rule in this volume</a></p>
</li>
<li id="q-316-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Subsystem reset is not power cycle and does not automatically remove prohibitions; preserve scope-specific state and explicit personality exceptions. <a class="qa-rule-link" href="#common-lockdown_op-13">Full rule in this volume</a></p>
</li>
<li id="q-316-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>CSEL0 persists across power cycles only with LDPE1; otherwise power cycle removes it. <a class="qa-rule-link" href="#common-lockdown_op-14">Full rule in this volume</a></p>
</li>
<li id="q-316-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>CSEL selects controllers and IFC the receiving interface. <a class="qa-rule-link" href="#common-lockdown_op-15">Full rule in this volume</a></p>
</li>
<li id="q-316-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Correlate configuration, inventory and behavior under identical selectors.</p>
</li>
<li id="q-316-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First inspect interface, controller scope and command-versus-feature selection.</p>
</li>
</ol>
<p class="qa-related">Related mechanisms: <a href="/nvme/question-bank/security/en/#q-242">Q242</a> · <a href="/nvme/question-bank/security/en/#q-243">Q243</a> · <a href="/nvme/question-bank/security/en/#q-244">Q244</a> · <a href="/nvme/question-bank/security/en/#q-245">Q245</a></p>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-lockdown">Base 2.4 §5.2.16, 8.1.5</a> · <a href="#ref-locklog">Base 2.4 §5.2.13.1.20</a> · <a href="#ref-lockpersist">Base 2.4 §5.2.30.1.25.4–5.2.30.1.25.4.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-317" data-question="317"><h2><a class="qa-qid" href="#q-317">Q317</a> How is excessive power-state recovery latency measured correctly?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-317-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-317-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Command latency includes exit, possible entry and execution, not only EXLAT.</p>
</li>
<li id="q-317-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Establish source/target states and concurrent thermal constraints.</p>
</li>
<li id="q-317-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Read state types, entry/exit latencies and selected policies.</p>
</li>
<li id="q-317-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>ITPT is idle time in milliseconds; entry/exit latencies are in microseconds.</p>
</li>
<li id="q-317-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Separate idle, transition trigger, recovery and command execution timing.</p>
</li>
<li id="q-317-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Assess relevant transitions rather than equating full read latency with EXLAT.</p>
</li>
<li id="q-317-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>CQE timing alone may not isolate an exit-latency violation.</p>
</li>
<li id="q-317-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-317-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>A power-state transition or throttling action does not itself define an AER. <a class="qa-rule-link" href="#common-power_config-9">Full rule in this volume</a></p>
</li>
<li id="q-317-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>SMART thermal transition counts and accumulated times help verify HCTM. <a class="qa-rule-link" href="#common-power_config-10">Full rule in this volume</a></p>
</li>
<li id="q-317-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>For supported PEL Set Feature events, verify that the FID permits and supports logging. <a class="qa-rule-link" href="#common-power_config-11">Full rule in this volume</a></p>
</li>
<li id="q-317-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Use scope, saveability and reset coverage; whole-subsystem and partial resets differ. <a class="qa-rule-link" href="#common-feature-12">Full rule in this volume</a></p>
</li>
<li id="q-317-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Establish whole or partial subsystem coverage; non-saveable persistent values do not thereby become zero. <a class="qa-rule-link" href="#common-feature-13">Full rule in this volume</a></p>
</li>
<li id="q-317-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Saveable values restore Saved; non-saveable values require their persistence and feature-specific rules. <a class="qa-rule-link" href="#common-feature-14">Full rule in this volume</a></p>
</li>
<li id="q-317-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Feature scope determines whether other controllers or namespaces share the setting. <a class="qa-rule-link" href="#common-feature-15">Full rule in this volume</a></p>
</li>
<li id="q-317-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Compare an operational baseline with matching workload, temperature and settings.</p>
</li>
<li id="q-317-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First verify units and timing origin.</p>
</li>
</ol>
<p class="qa-related">Related mechanisms: <a href="/nvme/question-bank/health/en/#q-188">Q188</a> · <a href="/nvme/question-bank/health/en/#q-190">Q190</a> · <a href="/nvme/question-bank/health/en/#q-192">Q192</a> · <a href="/nvme/question-bank/health/en/#q-194">Q194</a></p>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-powerdetail">Base 2.4 §8.1.19.1–8.1.19.5</a> · <a href="#ref-psd">Base 2.4 §5.2.14.2.1 (Power State Descriptor)</a> · <a href="#ref-power">Base 2.4 §5.2.30.1.2, 5.2.30.1.7</a> · <a href="#ref-smart">Base 2.4 §5.2.13.1.3</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-318" data-question="318"><h2><a class="qa-qid" href="#q-318">Q318</a> How are three reset types compared for one feature?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-318-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-318-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Compare matched initial states under distinct reset mechanisms.</p>
</li>
<li id="q-318-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Reset coverage and persistence conditions differ across the three cases.</p>
</li>
<li id="q-318-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Select one function and capture support, state and affected endpoints.</p>
</li>
<li id="q-318-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>Track registers, queues, settings, ongoing operation and stored data separately.</p>
</li>
<li id="q-318-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Reset from matched baselines and restore query access before comparison.</p>
</li>
<li id="q-318-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Extended self-test persistence and I/O queue invalidation can coexist under CLR.</p>
</li>
<li id="q-318-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>CC.EN-specific register exceptions do not cover all CLR, and subsystem reset is not factory restoration.</p>
</li>
<li id="q-318-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>This MMIO access has no NVMe CQE, so DNR/More do not apply. <a class="qa-rule-link" href="#common-register-8">Full rule in this volume</a></p>
</li>
<li id="q-318-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Register access has no success event; separate hardware errors use their event conditions. <a class="qa-rule-link" href="#common-register-9">Full rule in this volume</a></p>
</li>
<li id="q-318-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Register accesses are not logged individually; preserve registers and timing before obtaining available diagnostics. <a class="qa-rule-link" href="#common-register-10">Full rule in this volume</a></p>
</li>
<li id="q-318-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>Ordinary register access is not a PEL event; completed resets and supported hardware errors are assessed separately. <a class="qa-rule-link" href="#common-register-11">Full rule in this volume</a></p>
</li>
<li id="q-318-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Clearing CC.EN invalidates I/O queues and resets Admin pointers; retained base addresses do not validate old completions. <a class="qa-rule-link" href="#common-queue-12">Full rule in this volume</a></p>
</li>
<li id="q-318-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Rebuild affected-controller queues; do not assume CC.EN-reset register-retention exceptions. <a class="qa-rule-link" href="#common-queue-13">Full rule in this volume</a></p>
</li>
<li id="q-318-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Initialize queues and host tracking again; residual memory is not valid command state for a new lifetime. <a class="qa-rule-link" href="#common-queue-14">Full rule in this volume</a></p>
</li>
<li id="q-318-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Controller Reset targets one controller; subsystem reset covers one/all domains as defined for the implementation. <a class="qa-rule-link" href="#common-reset_review-15">Full rule in this volume</a></p>
</li>
<li id="q-318-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Tie differences to explicit rules and retain limits where behavior is unspecified.</p>
</li>
<li id="q-318-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First identify the actual reset trigger.</p>
</li>
</ol>
<p class="qa-related">Related mechanisms: <a href="/nvme/question-bank/reset-shutdown/en/#q-174">Q174</a> · <a href="/nvme/question-bank/reset-shutdown/en/#q-178">Q178</a> · <a href="/nvme/question-bank/reset-shutdown/en/#q-180">Q180</a></p>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-pciereset">PCIe Transport 1.4 §3.3</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-shutdownfull">Base 2.4 §3.6–3.6.1 (memory-based scope and shutdown)</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-319" data-question="319"><h2><a class="qa-qid" href="#q-319">Q319</a> How is an operation’s real scope established?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-319-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-319-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Submission through one Admin Queue does not limit effects to that controller.</p>
</li>
<li id="q-319-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Commands and selectors determine namespace, controller, group, domain or subsystem effects.</p>
</li>
<li id="q-319-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Inspect command selectors, feature scope, capabilities and command effects.</p>
</li>
<li id="q-319-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>Broadcast semantics are command-specific and effects metadata does not replace explicit scope definitions.</p>
</li>
<li id="q-319-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Identify endpoint, targets and shared resources, then observe inside/outside controls.</p>
</li>
<li id="q-319-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Detaching one endpoint does not duplicate or delete shared namespace data.</p>
</li>
<li id="q-319-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Exclude shared-resource and concurrent-operation causes before alleging out-of-scope effects.</p>
</li>
<li id="q-319-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-319-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Normal completion here does not guarantee an AER; a separate defined event requires support, configuration and a pending request. <a class="qa-rule-link" href="#common-command-9">Full rule in this volume</a></p>
</li>
<li id="q-319-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Correlate the completion with error records under the shared entry-creation rules; do not infer entry count directly from the number of failures. <a class="qa-rule-link" href="#common-command-10">Full rule in this volume</a></p>
</li>
<li id="q-319-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>PEL is not a per-command trace; supported defined events are logged under their recording conditions. <a class="qa-rule-link" href="#common-command-11">Full rule in this volume</a></p>
</li>
<li id="q-319-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Controller Level Reset aborts outstanding commands and resets queues; do not wait for old CQEs. <a class="qa-rule-link" href="#common-error_review-12">Full rule in this volume</a></p>
</li>
<li id="q-319-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>A subsystem reset applies Controller Level Reset to affected controllers. <a class="qa-rule-link" href="#common-error_review-13">Full rule in this volume</a></p>
</li>
<li id="q-319-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>After a power cycle, rebuild queues and command tracking before checking actual data and operation state. <a class="qa-rule-link" href="#common-error_review-14">Full rule in this volume</a></p>
</li>
<li id="q-319-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>One command failure does not establish failure of other commands, namespaces or controllers. <a class="qa-rule-link" href="#common-error_review-15">Full rule in this volume</a></p>
</li>
<li id="q-319-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Compare matching entities and times; active inventories can legitimately differ by endpoint.</p>
</li>
<li id="q-319-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First read special selector values for that specific command.</p>
</li>
</ol>
<p class="qa-related">Related mechanisms: <a href="/nvme/question-bank/initialization/en/#q-002">Q2</a> · <a href="/nvme/question-bank/identify/en/#q-047">Q47</a> · <a href="/nvme/question-bank/logs/en/#q-081">Q81</a> · <a href="/nvme/question-bank/media/en/#q-275">Q275</a></p>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-commandseffects">Base 2.4 §5.2.13.1.6</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-capacitymodel">Base 2.4 §3.2.2–3.2.3, 3.8</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-320" data-question="320"><h2><a class="qa-qid" href="#q-320">Q320</a> How are the interfaces combined into one conformance investigation?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-320-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-320-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Build traceable evidence across advertisement, prerequisites, operation, result, notice, record and persistence.</p>
</li>
<li id="q-320-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Define one function and its scope before testing multiple interacting mechanisms.</p>
</li>
<li id="q-320-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Capture discovery, effects and relevant configuration as the baseline.</p>
</li>
<li id="q-320-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>Record request, completion and applicable logs/events, explaining inapplicable or unsupported interfaces.</p>
</li>
<li id="q-320-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Run a valid case, isolate invalid conditions and then test persistence from matched baselines.</p>
</li>
<li id="q-320-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Conclusions identify supported requirements and remaining evidence limitations.</p>
</li>
<li id="q-320-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Do not turn permissions into mandates, invent statuses for undefined behavior or equate acceptance with background completion.</p>
</li>
<li id="q-320-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-320-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Normal completion here does not guarantee an AER; a separate defined event requires support, configuration and a pending request. <a class="qa-rule-link" href="#common-command-9">Full rule in this volume</a></p>
</li>
<li id="q-320-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Correlate the completion with error records under the shared entry-creation rules; do not infer entry count directly from the number of failures. <a class="qa-rule-link" href="#common-command-10">Full rule in this volume</a></p>
</li>
<li id="q-320-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>PEL is not a per-command trace; supported defined events are logged under their recording conditions. <a class="qa-rule-link" href="#common-command-11">Full rule in this volume</a></p>
</li>
<li id="q-320-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Controller Level Reset aborts outstanding commands and resets queues; do not wait for old CQEs. <a class="qa-rule-link" href="#common-error_review-12">Full rule in this volume</a></p>
</li>
<li id="q-320-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>A subsystem reset applies Controller Level Reset to affected controllers. <a class="qa-rule-link" href="#common-error_review-13">Full rule in this volume</a></p>
</li>
<li id="q-320-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>After a power cycle, rebuild queues and command tracking before checking actual data and operation state. <a class="qa-rule-link" href="#common-error_review-14">Full rule in this volume</a></p>
</li>
<li id="q-320-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>One command failure does not establish failure of other commands, namespaces or controllers. <a class="qa-rule-link" href="#common-error_review-15">Full rule in this volume</a></p>
</li>
<li id="q-320-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Link raw evidence on a timeline with source sections, figures and PDF pages.</p>
</li>
<li id="q-320-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First state one precise requirement and then select the evidence needed to test it.</p>
</li>
</ol>
<p class="qa-related">Related mechanisms: <a href="/nvme/question-bank/integration/en/#q-297">Q297</a> · <a href="/nvme/question-bank/integration/en/#q-299">Q299</a> · <a href="/nvme/question-bank/integration/en/#q-300">Q300</a> · <a href="/nvme/question-bank/integration/en/#q-301">Q301</a> · <a href="/nvme/question-bank/integration/en/#q-302">Q302</a> · <a href="/nvme/question-bank/integration/en/#q-318">Q318</a> · <a href="/nvme/question-bank/integration/en/#q-319">Q319</a></p>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-commandseffects">Base 2.4 §5.2.13.1.6</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-getlog">Base 2.4 §5.2.13–5.2.13.1.1</a> · <a href="#ref-aerfull">Base 2.4 §5.2.2 (PCIe-applicable events)</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-pelcontext">Base 2.4 §5.2.13.1.14–5.2.13.1.14.2.5 (exclude PCIe link/packet decoding)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<section id="common-rules" class="qa-common"><h2>Shared rules linked from the answers</h2><p>Each shared mechanism is explained in full once in this volume. Use browser Back to return to the question; explicit command or feature exceptions take precedence.</p>
<article id="common-aer_request-9"><h3>Shared conditions for this topic · Is an asynchronous event generated?</h3><p>AER reports an event by completing a request. Distinguish the event condition, enablement, masking and available requests; submitting AER does not enable every optional event.</p></article>
<article id="common-aer_request-10"><h3>Shared conditions for this topic · Are Error Information or other logs updated?</h3><p>Use AET, AEI and LID to select the associated log. Error events point to Error Information and SMART events to SMART/Health. A successful AER does not itself require an error entry; current state may have changed since the event, so record both times.</p></article>
<article id="common-aer_request-11"><h3>Shared conditions for this topic · Is it recorded in the Persistent Event Log?</h3><p>PEL logging depends on the underlying event, not on AER completion. Check supported event conditions rather than requiring an entry for every request or acknowledgment.</p></article>
<article id="common-aer_request-12"><h3>Shared conditions for this topic · What survives or continues after Controller Reset?</h3><p>Controller Reset aborts outstanding AERs without CQEs. Controller Level Reset also clears pending notifications. After recovery submit fresh requests and read retained state under each log’s rules.</p></article>
<article id="common-aer_request-13"><h3>Shared conditions for this topic · What survives or continues after NVM Subsystem Reset?</h3><p>After subsystem reset, reestablish Admin Queues and AERs on affected controllers. Do not wait for old requests; determine other controllers’ involvement from actual reset coverage.</p></article>
<article id="common-aer_request-14"><h3>Shared conditions for this topic · What survives or continues after a power cycle?</h3><p>Old AERs are invalid after a power cycle. Reinitialize, check the restored asynchronous-event configuration and post new requests. Persistent log history does not imply replay of every old notification.</p></article>
<article id="common-aer_request-15"><h3>Shared conditions for this topic · Are other controllers or namespaces affected?</h3><p>Requests and completions belong to a controller, while event scope may be a namespace, domain or subsystem. Several controllers can report one shared condition; notification count is not independent-failure count.</p></article>
<article id="common-command-8"><h3>Command completion, events and records · How are DNR and More set?</h3><p>For a CQE, DNR=1 means the identical command is expected to fail if resubmitted to any controller in this subsystem; DNR=0 means it may succeed. Do not assign DNR=1 solely from an error name unless that condition mandates it. More=1 identifies additional information for this command in the Error Information Log. DNR should be zero when SCT=SC=0.</p></article>
<article id="common-command-9"><h3>Command completion, events and records · Is an asynchronous event generated?</h3><p>Command completion and asynchronous notification are separate. Success here does not itself guarantee an event. For a defined resulting event, check support, applicable notification configuration, masking and an outstanding Asynchronous Event Request.</p></article>
<article id="common-command-10"><h3>Command completion, events and records · Are Error Information or other logs updated?</h3><p>A successful CQE does not require a new Error Information entry. For an error with More=1, read LID 01h and correlate SQID, CID and Error Count; not every unsuccessful CQE requires a new entry. Re-read the interfaces named in this question for the state the operation changes.</p></article>
<article id="common-command-11"><h3>Command completion, events and records · Is it recorded in the Persistent Event Log?</h3><p>The optional Persistent Event Log is an event history, not a trace of every command. Check LPA support and the Supported Events Bitmap, then the logging condition for the particular event. Command success or failure alone does not require an entry.</p></article>
<article id="common-error_review-12"><h3>Shared conditions for this topic · What survives or continues after Controller Reset?</h3><p>Controller Level Reset aborts outstanding commands and resets queues; do not wait for old CQEs. It does not roll back prior changes or universally stop background operations. Preserve available evidence, then inspect operation-specific state after recovery. Error Information entries should clear while Error Count persists, so an absent post-reset entry does not disprove an earlier error.</p></article>
<article id="common-error_review-13"><h3>Shared conditions for this topic · What survives or continues after NVM Subsystem Reset?</h3><p>A subsystem reset applies Controller Level Reset to affected controllers. Restore query access before inspection; it is neither factory restoration nor proof that the fault is resolved. Verify operation results, current settings, retained logs and the reset coverage of controllers sharing resources.</p></article>
<article id="common-error_review-14"><h3>Shared conditions for this topic · What survives or continues after a power cycle?</h3><p>After a power cycle, rebuild queues and command tracking before checking actual data and operation state. SMART/PEL persistence does not establish command success. Error entries should clear but Error Count persists, so correlate pre-power-loss requests, completions and logs with fresh observations.</p></article>
<article id="common-error_review-15"><h3>Shared conditions for this topic · Are other controllers or namespaces affected?</h3><p>One command failure does not establish failure of other commands, namespaces or controllers. Distinguish parameter, queue and controller failures, broadening recovery when shared resources or state are affected.</p></article>
<article id="common-feature-12"><h3>Feature reset and scope · What survives or continues after Controller Reset?</h3><p>Separate scope from saveability. For a reset covering the subsystem, a saveable Current value is restored from Saved, or Default if no Saved value exists; a non-saveable, nonpersistent value returns to Default. A partial reset uses Figure 127 for shared scopes. The specific feature exceptions in this question take precedence.</p></article>
<article id="common-feature-13"><h3>Feature reset and scope · What survives or continues after NVM Subsystem Reset?</h3><p>Determine reset coverage, not only its name. Figure 126 applies to the whole subsystem; Figure 127 applies to a partial multi-domain reset. A non-saveable feature specified as persistent remains persistent; non-saveable does not mean reset to zero.</p></article>
<article id="common-feature-14"><h3>Feature reset and scope · What survives or continues after a power cycle?</h3><p>A successfully saved SV=1 setting is restored from Saved across a power cycle; SV=0 does not update Saved. For non-saveable features use Figure 466 persistence and feature-specific exceptions. Verify Current and behavior rather than assuming an existing Saved value is already active.</p></article>
<article id="common-feature-15"><h3>Feature reset and scope · Are other controllers or namespaces affected?</h3><p>Feature scope determines impact. Controller-scoped settings target that controller; namespace, NVM Set and subsystem settings may be shared across controllers. Coordinate changes across hosts and do not treat NSID=FFFFFFFFh as a universal feature broadcast.</p></article>
<article id="common-feature_events-11"><h3>Set Feature event recording · Is it recorded in the Persistent Event Log?</h3><p>With supported PEL Set Feature logging, Figure 252 must also permit and support this FID: successful changes shall be recorded; successfully reapplying the same value may be recorded. This is not universal across FIDs. Timestamp is prohibited from Set Feature logging and uses its separate Timestamp Change event rules.</p></article>
<article id="common-firmware_op-9"><h3>Shared conditions for this topic · Is an asynchronous event generated?</h3><p>Starting reset-free activation triggers Firmware Activation Starting on affected controllers when notices are enabled. Load failure has a separate error event; each successful download segment does not trigger activation.</p></article>
<article id="common-firmware_op-10"><h3>Shared conditions for this topic · Are Error Information or other logs updated?</h3><p>Distinguish active and next-reset slots with Firmware Slot Information and confirm running revision through Identify.FR. Use More for error details; stored does not mean executing.</p></article>
<article id="common-firmware_op-11"><h3>Shared conditions for this topic · Is it recorded in the Persistent Event Log?</h3><p>PEL Commit 02h records old/requested revisions, action, slot and status. Requested NFR is not proof of activation; Reset-event FA/FREV provide outcome evidence.</p></article>
<article id="common-firmware_op-12"><h3>Shared conditions for this topic · What survives or continues after Controller Reset?</h3><p>A CLR between download and completed Commit discards staged portions. Committed slots/pending activation follow CA and required reset type; not every reset activates the image.</p></article>
<article id="common-firmware_op-13"><h3>Shared conditions for this topic · What survives or continues after NVM Subsystem Reset?</h3><p>Subsystem reset affects its covered controllers and satisfies a required subsystem-reset activation. Recheck revision, slots and capabilities; uncommitted staging cannot be reused.</p></article>
<article id="common-firmware_op-14"><h3>Shared conditions for this topic · What survives or continues after a power cycle?</h3><p>Entering D3cold during activation Commit can resume with the old or newly activated image; verify it. Uncommitted downloaded portions are not a persistent slot.</p></article>
<article id="common-firmware_op-15"><h3>Shared conditions for this topic · Are other controllers or namespaces affected?</h3><p>Controllers in one domain share slots/image, covering the subsystem in a single-domain system. Coordinate affected accessors and avoid overlapping update sequences.</p></article>
<article id="common-lockdown_op-9"><h3>Shared conditions for this topic · Is an asynchronous event generated?</h3><p>Lockdown success defines no generic configuration-complete AER. Verify the log and target command behavior; separate events follow their own rules.</p></article>
<article id="common-lockdown_op-10"><h3>Shared conditions for this topic · Are Error Information or other logs updated?</h3><p>Current prohibitions should reflect success under matching interface/scope/controller/UUID selectors; denied commands use ordinary error-log correlation.</p></article>
<article id="common-lockdown_op-11"><h3>Shared conditions for this topic · Is it recorded in the Persistent Event Log?</h3><p>Lockdown itself has no dedicated standard PEL event. A separate persistence-personality change follows its supported event rules.</p></article>
<article id="common-lockdown_op-12"><h3>Shared conditions for this topic · What survives or continues after Controller Reset?</h3><p>Ordinary CLR does not remove a successful prohibition; removal requires an allowed subsequent Lockdown or its specified power-cycle condition.</p></article>
<article id="common-lockdown_op-13"><h3>Shared conditions for this topic · What survives or continues after NVM Subsystem Reset?</h3><p>Subsystem reset is not power cycle and does not automatically remove prohibitions; preserve scope-specific state and explicit personality exceptions.</p></article>
<article id="common-lockdown_op-14"><h3>Shared conditions for this topic · What survives or continues after a power cycle?</h3><p>CSEL0 persists across power cycles only with LDPE1; otherwise power cycle removes it. CSEL1/2 end at power cycle regardless of LDPE.</p></article>
<article id="common-lockdown_op-15"><h3>Shared conditions for this topic · Are other controllers or namespaces affected?</h3><p>CSEL selects controllers and IFC the receiving interface. One interface’s prohibition does not cover others; FID scope targets Set Features, not automatic Get prohibition.</p></article>
<article id="common-namespace_op-9"><h3>Shared conditions for this topic · Is an asynchronous event generated?</h3><p>Create/delete affect allocated inventory; attach/detach affect controller active lists. Apply per-controller support/AEC. The Admin Delete recipient does not report its own deletion notice; other eligible controllers do.</p></article>
<article id="common-namespace_op-10"><h3>Shared conditions for this topic · Are Error Information or other logs updated?</h3><p>Identify lists establish current allocation/attachment; changed lists 04h/1Ch identify changes rather than complete state. Errors use More and applicable Error Information fields.</p></article>
<article id="common-namespace_op-11"><h3>Shared conditions for this topic · Is it recorded in the Persistent Event Log?</h3><p>Supported Change Namespace 06h records defined management changes; do not treat attachment as creation/deletion. Write protection follows supported Set Feature-event rules.</p></article>
<article id="common-namespace_op-12"><h3>Shared conditions for this topic · What survives or continues after Controller Reset?</h3><p>Completed configuration/attachment survives reset; command channels reset without deleting namespaces. For interrupted commands, inspect lists rather than assuming rollback.</p></article>
<article id="common-namespace_op-13"><h3>Shared conditions for this topic · What survives or continues after NVM Subsystem Reset?</h3><p>Subsystem reset is not Restore Default Namespace Configuration. Rediscover persisted namespaces/attachments and rebuild queues, accounting for domain scope.</p></article>
<article id="common-namespace_op-14"><h3>Shared conditions for this topic · What survives or continues after a power cycle?</h3><p>Completed namespace configuration/attachments persist. Ordinary/permanent write protection persist; until-power-cycle protection clears on a real power cycle, not all configuration.</p></article>
<article id="common-namespace_op-15"><h3>Shared conditions for this topic · Are other controllers or namespaces affected?</h3><p>Creation/deletion changes inventory and attachment lists select affected controllers. Shared namespace protection applies through all attached controllers.</p></article>
<article id="common-pel_query-9"><h3>Shared conditions for this topic · Is an asynchronous event generated?</h3><p>Base 2.4 does not define a generic PEL Changed AER for every appended entry. The underlying condition may have its own SMART, Sanitize or other notification rules.</p></article>
<article id="common-pel_query-10"><h3>Shared conditions for this topic · Are Error Information or other logs updated?</h3><p>A context fixes the reported event set. New events remain logged but shall not enter that context. Reading/releasing a context does not erase PEL; failed reads use ordinary error-log rules.</p></article>
<article id="common-pel_query-11"><h3>Shared conditions for this topic · Is it recorded in the Persistent Event Log?</h3><p>PEL retrieval is not itself a PEL read event. Supported underlying events follow their triggers, with permitted vendor-threshold suppression of frequent repeated events.</p></article>
<article id="common-pel_query-12"><h3>Shared conditions for this topic · What survives or continues after Controller Reset?</h3><p>Event content survives CLR; the reporting context need not. Re-establish it after recovery instead of joining partial data across contexts.</p></article>
<article id="common-pel_query-13"><h3>Shared conditions for this topic · What survives or continues after NVM Subsystem Reset?</h3><p>Subsystem reset preserves events and may add the supported Power-on or Reset event at completion; establish a fresh consistent reporting context.</p></article>
<article id="common-pel_query-14"><h3>Shared conditions for this topic · What survives or continues after a power cycle?</h3><p>Events persist across power cycles, with minimal power-failure loss recommended. Capacity eviction, repeated-event suppression and Sanitize-related privacy removal are distinct from ordinary power-cycle clearing.</p></article>
<article id="common-pel_query-15"><h3>Shared conditions for this topic · Are other controllers or namespaces affected?</h3><p>PEL is subsystem-global. CNTLID identifies the recording controller; multi-controller events should be logged once. Coordinate readers so one does not release a context still used by another.</p></article>
<article id="common-power_config-9"><h3>Shared conditions for this topic · Is an asynchronous event generated?</h3><p>A power-state transition or throttling action does not itself define an AER. Temperature warnings use SMART/Health event conditions and configuration; HCTM TMT1/TMT2 are distinct from Temperature Threshold feature limits.</p></article>
<article id="common-power_config-10"><h3>Shared conditions for this topic · Are Error Information or other logs updated?</h3><p>SMART thermal transition counts and accumulated times help verify HCTM. There is no generic per-transition power-state log. Successful configuration requires no error entry; failures follow CQE and logging rules.</p></article>
<article id="common-power_config-11"><h3>Shared conditions for this topic · Is it recorded in the Persistent Event Log?</h3><p>For supported PEL Set Feature events, verify that the FID permits and supports logging. Eligible setting changes are recorded; automatic state transitions and throttling are not additional Set Features commands.</p></article>
<article id="common-queue-12"><h3>Queue reset and scope · What survives or continues after Controller Reset?</h3><p>Clearing CC.EN initiates a Controller Level Reset: I/O queues are deleted and Admin Queue pointers reset. Retention of AQA/ASQ/ACQ for this reset does not validate old CQEs. Reinitialize Admin CQ phases, enable, then configure and recreate I/O queues.</p></article>
<article id="common-queue-13"><h3>Queue reset and scope · What survives or continues after NVM Subsystem Reset?</h3><p>Affected controllers undergo Controller Level Reset during an NVM Subsystem Reset; old queues cannot be reused. Re-establish transport and register state and the Admin/I/O environment. Do not apply the AQA retention exception of a CC.EN reset to this different reset source.</p></article>
<article id="common-queue-14"><h3>Queue reset and scope · What survives or continues after a power cycle?</h3><p>After a power cycle, initialize and create queues again. Residual SQE/CQE bytes in host memory are not valid commands or completions for the new queue lifetime; rebuild host pointers, phases and outstanding-command tracking.</p></article>
<article id="common-queue-15"><h3>Queue reset and scope · Are other controllers or namespaces affected?</h3><p>Queues belong to their controller; equal QIDs on different controllers do not identify the same queue. SQs sharing a CQ are directly coupled through CQ capacity and deletion ordering. Queue reset neither deletes a namespace nor reverses completed writes.</p></article>
<article id="common-register-8"><h3>Register access · How are DNR and More set?</h3><p>Not applicable to this register access: it has no NVMe CQE and therefore no DNR or More to set. Decode those bits only for a subsequent Admin or I/O command that actually returns a CQE.</p></article>
<article id="common-register-9"><h3>Register access · Is an asynchronous event generated?</h3><p>This register access does not define a success notification. A separate defined event, such as an Internal Error, follows its own rules. When the Admin Queue is unavailable, waiting for an event cannot replace initialization-state checks.</p></article>
<article id="common-register-10"><h3>Register access · Are Error Information or other logs updated?</h3><p>Every register read or write does not require an Error Information entry. Preserve CAP, CC, CSTS, CRTO and timestamps first; logs provide additional evidence if the controller subsequently permits access.</p></article>
<article id="common-register-11"><h3>Register access · Is it recorded in the Persistent Event Log?</h3><p>An ordinary register access is not a separate persistent event. Reset, power or hardware conditions are recorded when PEL support and the corresponding event requirements apply; each CC write is not automatically a Power-on or Reset event.</p></article>
<article id="common-reset_review-15"><h3>Shared conditions for this topic · Are other controllers or namespaces affected?</h3><p>Controller Reset targets one controller; subsystem reset covers one/all domains as defined for the implementation. Power-off readiness also depends on CAP.CPS; shared paths are not independent data copies.</p></article>
<article id="common-sanitize_op-9"><h3>Shared conditions for this topic · Is an asynchronous event generated?</h3><p>State transitions report completed, unexpected-deallocation completion or media-verification entry with LID 81h. For Admin-SQ initiation, only the initiating controller reports the event; inspect the log for actual outcome.</p></article>
<article id="common-sanitize_op-10"><h3>Shared conditions for this topic · Are Error Information or other logs updated?</h3><p>Sanitize Status updates before the initiating CQE and on transitions, persisting across resets/power. Match target, SOS, SANS, SPROG, SCDW10 and GDE/NDE; background failure does not require a second initiation CQE.</p></article>
<article id="common-sanitize_op-11"><h3>Shared conditions for this topic · Is it recorded in the Persistent Event Log?</h3><p>Supported PEL logging records Start 09h on entering processing and Completion 0Ah on entering Idle or either failure state. Completion includes failures; NSID distinguishes subsystem and namespace targets.</p></article>
<article id="common-sanitize_op-12"><h3>Shared conditions for this topic · What survives or continues after Controller Reset?</h3><p>Background sanitization continues through Controller Level Reset. Re-read target LID 81h after recovery. Some reset sources cancel media verification and set MVCNCLD without cancelling the entire sanitize operation.</p></article>
<article id="common-sanitize_op-13"><h3>Shared conditions for this topic · What survives or continues after NVM Subsystem Reset?</h3><p>Subsystem reset does not abort sanitization. Preserve operation/log state and check MVCNCLD and post-verification deallocation when verification was requested.</p></article>
<article id="common-sanitize_op-14"><h3>Shared conditions for this topic · What survives or continues after a power cycle?</h3><p>Processing cannot occur without power, but sanitization continues from retained state after power returns. Inspect SOS/SANS and progress; SPROG=FFFFh alone is not success.</p></article>
<article id="common-sanitize_op-15"><h3>Shared conditions for this topic · Are other controllers or namespaces affected?</h3><p>Subsystem sanitization restricts subsystem access; namespace sanitization targets one namespace across its controllers. Shared operations such as firmware update have additional restrictions even when other namespace data is not erased.</p></article>
<article id="common-selftest_op-9"><h3>Shared conditions for this topic · Is an asynchronous event generated?</h3><p>There is no generic Device Self-test Completed AER. Read LID 06h for normal completion; diagnostic failures separately follow Diagnostic Failure error-event conditions.</p></article>
<article id="common-selftest_op-10"><h3>Shared conditions for this topic · Are Error Information or other logs updated?</h3><p>Short/extended completion or cancellation creates the newest result before returning current operation to idle. Check diagnostic valid bits before NSID/LBA/SCT/SC.</p></article>
<article id="common-selftest_op-11"><h3>Shared conditions for this topic · Is it recorded in the Persistent Event Log?</h3><p>PEL has no generic per-self-test result event; use LID 06h. Separately qualifying hardware/reset events do not replace the self-test result.</p></article>
<article id="common-selftest_op-12"><h3>Shared conditions for this topic · What survives or continues after Controller Reset?</h3><p>CLR aborts a short test but an extended test must persist and resume after reset. The resume segment is vendor-specific; implementations should only need to repeat the interrupted last segment.</p></article>
<article id="common-selftest_op-13"><h3>Shared conditions for this topic · What survives or continues after NVM Subsystem Reset?</h3><p>Subsystem reset causes CLR on covered controllers: short tests abort and extended tests resume. Rebuilding Admin Queues is not restarting the entire extended test.</p></article>
<article id="common-selftest_op-14"><h3>Shared conditions for this topic · What survives or continues after a power cycle?</h3><p>Extended testing must resume after power restoration; short testing has no such continuation requirement. Read operation/progress/results rather than requiring reset-aborted results for both.</p></article>
<article id="common-selftest_op-15"><h3>Shared conditions for this topic · Are other controllers or namespaces affected?</h3><p>The receiving controller runs the test and NSID selects coverage. DSTO.SDSO determines controller/subsystem concurrency scope; shared resources may slow unrelated work.</p></article>
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
