---
layout: post
title: "NVMe Self-Study Bank: Keep Alive"
date: 2026-10-02 00:00:00 +0800
categories: [nvme]
permalink: /nvme/question-bank/keep-alive/en/
lang: en
nvme_quickref: true
nvme_qa: true
---

<div class="nvme-quickref nvme-qa">
<nav class="qr-top" aria-label="Bank and editions"><a href="#content">Skip to content</a><a href="/nvme/question-bank/en/">Question index</a><a href="/nvme/question-bank/keep-alive/zh-tw/">繁體中文</a><a href="/DOCS/nvme-question-bank/keep-alive.html">Chinese tutorial HTML</a></nav>
<main id="content"><p class="qr-eyebrow">BASE 2.4 / NVM 1.3 / PCIe 1.4 · Q1–328</p>
<header><p class="qa-range">Q217–Q222</p><h1>Keep Alive</h1><p class="qr-intro">Optional PCIe Keep Alive detects host liveness through command-based or traffic-based timing.</p><p>Practice first, then reveal 17 answer items per question. All numerical examples are hypothetical. Status is written SCT/SC; h indicates hexadecimal.</p></header>
<aside class="qa-glossary"><h2>Terms used in this volume</h2><dl><dt>Controller / namespace</dt><dd>A controller receives commands and manages access. A namespace is a logical storage space that commands can address. An NVM subsystem contains controllers and nonvolatile storage resources.</dd><dt>SQ / CQ / SQE / CQE</dt><dd>Submission and Completion Queues carry command entries (SQEs) and completion entries (CQEs). QID identifies a queue, CID distinguishes outstanding commands in one SQ, and NSID identifies a namespace.</dd><dt>Register / Identify / Feature / Log</dt><dd>A register exposes control or state. Identify queries capabilities and attributes; features query or configure operation; log pages report specific state or records. FID, LID, CNS and CSI select features, logs, Identify structures and command sets.</dd><dt>index / offset / zero-based</dt><dd>An index selects an entry, usually starting at 0; an offset measures distance from an origin in specified units. A zero-based count encodes count−1, but not every zero-valued field is a count. A Dword is 4 bytes; a byte is 8 bits.</dd><dt>Scope / reset / retention</dt><dd>Scope names the affected objects; retention means preserving state. Controller Reset (clearing CC.EN) is one form of Controller Level Reset, or CLR. Different CLR triggers can retain different registers.</dd></dl></aside>
<section id="overview" class="qa-overview"><h2>Two modes with different renewal evidence</h2><p class="qa-takeaway">One long-outstanding command does not establish activity in every interval.</p>
<div class="qr-table" tabindex="0" role="region" aria-label="Horizontally scrollable comparison table"><table><thead><tr><th scope="col">Condition</th><th scope="col">Evidence/action</th><th scope="col">Interpretation</th></tr></thead><tbody><tr><td>Support/granularity</td><td>KAS, TBKAS</td><td>KAS uses 100 ms units; mode is separate</td></tr><tr><td>Timeout</td><td>FID 0Fh.KATO</td><td>Value may be rounded up</td></tr><tr><td>Command mode</td><td>Successful Keep Alive/KATO Set</td><td>Restart on qualifying success</td></tr><tr><td>Traffic mode</td><td>Command fetches in interval</td><td>Outstanding alone is insufficient</td></tr></tbody></table></div>
<p><strong>Worked interpretation: </strong>KAS2 means 200 ms granularity; a 250 ms request is rounded upward. Schedule using actual readback.</p>
<p class="qa-citations">Sources: <a href="#ref-keepalive">Base 2.4 §3.9 (common and PCIe rules), 5.2.30.1.9</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-feature">Base 2.4 §4.4</a></p>
</section>
<div class="qa-controls" hidden><label>Search this page <input type="search" id="qa-search" placeholder="Question number, field or keyword"></label><button type="button" data-expand="true">Expand all answers</button><button type="button" data-expand="false">Collapse all answers</button><output id="qa-count" aria-live="polite"></output></div>
<section id="question-index"><h2>Questions in this volume</h2><ol class="qa-index">
<li><a href="#q-217">Q217 · How does a PCIe host discover Keep Alive support?</a></li>
<li><a href="#q-218">Q218 · How is the timer configured, adjusted and disabled?</a></li>
<li><a href="#q-219">Q219 · How does the host maintain liveness before expiry?</a></li>
<li><a href="#q-220">Q220 · What cleanup is required after Keep Alive Timeout?</a></li>
<li><a href="#q-221">Q221 · Must Keep Alive be reconfigured after reset?</a></li>
<li><a href="#q-222">Q222 · How do command-based and traffic-based Keep Alive differ?</a></li>
</ol></section>
<article class="qa-question" id="q-217" data-question="217"><h2><a class="qa-qid" href="#q-217">Q217</a> How does a PCIe host discover Keep Alive support?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-217-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-217-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Keep Alive monitors communication liveness, not each I/O’s execution deadline; PCIe does not require every SSD to enable it.</p>
</li>
<li id="q-217-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Each controller has its own timer; activity on another controller does not substitute.</p>
</li>
<li id="q-217-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Nonzero KAS advertises support and 100 ms granularity units; CTRATT.TBKAS identifies Traffic Based mode.</p>
</li>
<li id="q-217-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>Timer support requires the Keep Alive command; FID 0Fh KATO configures milliseconds.</p>
</li>
<li id="q-217-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Read KAS, determine mode, configure and read back the actual timeout.</p>
</li>
<li id="q-217-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>PCIe defaults to disabled KATO=0; support and active use are distinct.</p>
</li>
<li id="q-217-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>KAS=0 does not promise command/feature acceptance; apply the relevant unsupported-command/feature rules.</p>
</li>
<li id="q-217-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-217-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>A successful Keep Alive defines no separate success AER. <a class="qa-rule-link" href="#common-keepalive_op-9">Full rule in this volume</a></p>
</li>
<li id="q-217-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Keep Alive Timeout requires an Error Information entry with Keep Alive Timeout Expired within CQT cleanup time; this is an explicit requirement distinct from ordinary command-error logging. <a class="qa-rule-link" href="#common-keepalive_op-10">Full rule in this volume</a></p>
</li>
<li id="q-217-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>Supported PEL Controller Fatal Status hardware events follow the resulting CFS condition; individual Keep Alive commands are not a PEL trace. <a class="qa-rule-link" href="#common-keepalive_op-11">Full rule in this volume</a></p>
</li>
<li id="q-217-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Use scope, saveability and reset coverage; whole-subsystem and partial resets differ. <a class="qa-rule-link" href="#common-feature-12">Full rule in this volume</a></p>
</li>
<li id="q-217-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Establish whole or partial subsystem coverage; non-saveable persistent values do not thereby become zero. <a class="qa-rule-link" href="#common-feature-13">Full rule in this volume</a></p>
</li>
<li id="q-217-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Saveable values restore Saved; non-saveable values require their persistence and feature-specific rules. <a class="qa-rule-link" href="#common-feature-14">Full rule in this volume</a></p>
</li>
<li id="q-217-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>The timer targets a controller. <a class="qa-rule-link" href="#common-keepalive_op-15">Full rule in this volume</a></p>
</li>
<li id="q-217-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>KAS, TBKAS, command support/effects and feature behavior must agree.</p>
</li>
<li id="q-217-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First check whether an optional PCIe capability was incorrectly assumed mandatory.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-keepalive">Base 2.4 §3.9 (common and PCIe rules), 5.2.30.1.9</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-commrecovery">Base 2.4 §9.1–9.6.2.1 (PCIe-applicable rules; stop before 9.6.2.2)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-218" data-question="218"><h2><a class="qa-qid" href="#q-218">Q218</a> How is the timer configured, adjusted and disabled?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-218-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-218-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>The host chooses a communication interval and the controller applies supported granularity.</p>
</li>
<li id="q-218-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>It is controller-scoped, not a subsystem-wide I/O timeout.</p>
</li>
<li id="q-218-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Read KAS, current KATO and feature saveability.</p>
</li>
<li id="q-218-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>KATO is milliseconds; round upward to KAS granularity and apply an implementation minimum when needed.</p>
</li>
<li id="q-218-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Read the effective timeout after success and update host scheduling; PCIe allows KATO=0 to disable.</p>
</li>
<li id="q-218-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>With hypothetical KAS=10, 1500 ms rounds to 2000 ms unless a larger minimum applies.</p>
</li>
<li id="q-218-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>An applicable transport maximum violation returns Keep Alive Timeout Invalid without changing the setting; do not invent a fixed PCIe maximum.</p>
</li>
<li id="q-218-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-218-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>A successful Keep Alive defines no separate success AER. <a class="qa-rule-link" href="#common-keepalive_op-9">Full rule in this volume</a></p>
</li>
<li id="q-218-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Keep Alive Timeout requires an Error Information entry with Keep Alive Timeout Expired within CQT cleanup time; this is an explicit requirement distinct from ordinary command-error logging. <a class="qa-rule-link" href="#common-keepalive_op-10">Full rule in this volume</a></p>
</li>
<li id="q-218-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>Supported PEL Controller Fatal Status hardware events follow the resulting CFS condition; individual Keep Alive commands are not a PEL trace. <a class="qa-rule-link" href="#common-keepalive_op-11">Full rule in this volume</a></p>
</li>
<li id="q-218-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Use scope, saveability and reset coverage; whole-subsystem and partial resets differ. <a class="qa-rule-link" href="#common-feature-12">Full rule in this volume</a></p>
</li>
<li id="q-218-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Establish whole or partial subsystem coverage; non-saveable persistent values do not thereby become zero. <a class="qa-rule-link" href="#common-feature-13">Full rule in this volume</a></p>
</li>
<li id="q-218-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Saveable values restore Saved; non-saveable values require their persistence and feature-specific rules. <a class="qa-rule-link" href="#common-feature-14">Full rule in this volume</a></p>
</li>
<li id="q-218-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>The timer targets a controller. <a class="qa-rule-link" href="#common-keepalive_op-15">Full rule in this volume</a></p>
</li>
<li id="q-218-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>A larger readback can be valid because of rounding/minimums.</p>
</li>
<li id="q-218-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First check whether host scheduling uses the requested or effective timeout.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-keepalive">Base 2.4 §3.9 (common and PCIe rules), 5.2.30.1.9</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-commrecovery">Base 2.4 §9.1–9.6.2.1 (PCIe-applicable rules; stop before 9.6.2.2)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-219" data-question="219"><h2><a class="qa-qid" href="#q-219">Q219</a> How does the host maintain liveness before expiry?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-219-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-219-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Margin accommodates scheduling and processing delay; last-moment submission does not prove timely controller processing.</p>
</li>
<li id="q-219-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>The timer is active only with EN=RDY=1, SHN=SHST=00b and nonzero KATO.</p>
</li>
<li id="q-219-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Read effective KATO and determine the active mode.</p>
</li>
<li id="q-219-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>Command Based restarts on successful Keep Alive or nonzero KATO Set, not ordinary Reads.</p>
</li>
<li id="q-219-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>The host should send at KATT/2 and keep Admin SQ space available, adjusting scheduling after successful KATO changes.</p>
</li>
<li id="q-219-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Successful completions demonstrate communication, not completion of every media operation.</p>
</li>
<li id="q-219-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Missing Keep Alive completion is assessed against KATT and recovery rules rather than hidden by endless submissions.</p>
</li>
<li id="q-219-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-219-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>A successful Keep Alive defines no separate success AER. <a class="qa-rule-link" href="#common-keepalive_op-9">Full rule in this volume</a></p>
</li>
<li id="q-219-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Keep Alive Timeout requires an Error Information entry with Keep Alive Timeout Expired within CQT cleanup time; this is an explicit requirement distinct from ordinary command-error logging. <a class="qa-rule-link" href="#common-keepalive_op-10">Full rule in this volume</a></p>
</li>
<li id="q-219-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>Supported PEL Controller Fatal Status hardware events follow the resulting CFS condition; individual Keep Alive commands are not a PEL trace. <a class="qa-rule-link" href="#common-keepalive_op-11">Full rule in this volume</a></p>
</li>
<li id="q-219-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Use scope, saveability and reset coverage; whole-subsystem and partial resets differ. <a class="qa-rule-link" href="#common-feature-12">Full rule in this volume</a></p>
</li>
<li id="q-219-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Establish whole or partial subsystem coverage; non-saveable persistent values do not thereby become zero. <a class="qa-rule-link" href="#common-feature-13">Full rule in this volume</a></p>
</li>
<li id="q-219-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Saveable values restore Saved; non-saveable values require their persistence and feature-specific rules. <a class="qa-rule-link" href="#common-feature-14">Full rule in this volume</a></p>
</li>
<li id="q-219-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>The timer targets a controller. <a class="qa-rule-link" href="#common-keepalive_op-15">Full rule in this volume</a></p>
</li>
<li id="q-219-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Separate submission, controller completion and host receipt timestamps.</p>
</li>
<li id="q-219-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First check whether Admin SQ congestion prevented actual submission.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-keepalive">Base 2.4 §3.9 (common and PCIe rules), 5.2.30.1.9</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-commrecovery">Base 2.4 §9.1–9.6.2.1 (PCIe-applicable rules; stop before 9.6.2.2)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-220" data-question="220"><h2><a class="qa-qid" href="#q-220">Q220</a> What cleanup is required after Keep Alive Timeout?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-220-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-220-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Cleanup stops processing on a failed communication path before host recovery introduces new work.</p>
</li>
<li id="q-220-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>PCIe cleanup neither deletes namespaces, sanitizes data nor rolls back writes.</p>
</li>
<li id="q-220-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Check CQT, CFS and Error Information with outstanding-command records.</p>
</li>
<li id="q-220-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>Within CQT, log Keep Alive Timeout Expired, stop processing and set CFS.</p>
</li>
<li id="q-220-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Stop submissions, preserve available evidence and recover/reinitialize the path.</p>
</li>
<li id="q-220-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Cleanup establishes stopped processing, not a CQE for every outstanding command.</p>
</li>
<li id="q-220-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Timeout does not prove old Writes unexecuted or safely retryable unchanged.</p>
</li>
<li id="q-220-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-220-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>A successful Keep Alive defines no separate success AER. <a class="qa-rule-link" href="#common-keepalive_op-9">Full rule in this volume</a></p>
</li>
<li id="q-220-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Keep Alive Timeout requires an Error Information entry with Keep Alive Timeout Expired within CQT cleanup time; this is an explicit requirement distinct from ordinary command-error logging. <a class="qa-rule-link" href="#common-keepalive_op-10">Full rule in this volume</a></p>
</li>
<li id="q-220-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>Supported PEL Controller Fatal Status hardware events follow the resulting CFS condition; individual Keep Alive commands are not a PEL trace. <a class="qa-rule-link" href="#common-keepalive_op-11">Full rule in this volume</a></p>
</li>
<li id="q-220-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Use scope, saveability and reset coverage; whole-subsystem and partial resets differ. <a class="qa-rule-link" href="#common-feature-12">Full rule in this volume</a></p>
</li>
<li id="q-220-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Establish whole or partial subsystem coverage; non-saveable persistent values do not thereby become zero. <a class="qa-rule-link" href="#common-feature-13">Full rule in this volume</a></p>
</li>
<li id="q-220-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Saveable values restore Saved; non-saveable values require their persistence and feature-specific rules. <a class="qa-rule-link" href="#common-feature-14">Full rule in this volume</a></p>
</li>
<li id="q-220-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>The timer targets a controller. <a class="qa-rule-link" href="#common-keepalive_op-15">Full rule in this volume</a></p>
</li>
<li id="q-220-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Correlate fatal state, error record and cleanup timing separately from data effects.</p>
</li>
<li id="q-220-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First distinguish host-detected timeout from controller-detected/completed cleanup.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-keepalive">Base 2.4 §3.9 (common and PCIe rules), 5.2.30.1.9</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-commrecovery">Base 2.4 §9.1–9.6.2.1 (PCIe-applicable rules; stop before 9.6.2.2)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-221" data-question="221"><h2><a class="qa-qid" href="#q-221">Q221</a> Must Keep Alive be reconfigured after reset?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-221-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-221-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Reset ends the old command environment; restored timer configuration follows feature persistence rather than host memory of old KATO.</p>
</li>
<li id="q-221-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Reassess the affected controller’s configuration and activation conditions.</p>
</li>
<li id="q-221-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Read restored Current KATO and applicable Saved/Default behavior.</p>
</li>
<li id="q-221-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>Invalid activation conditions make the timer inactive; activation initializes it to effective KATO.</p>
</li>
<li id="q-221-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Initialize, read KATO, enable/read back if needed and restart host maintenance scheduling.</p>
</li>
<li id="q-221-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Host scheduling matches the actual value, mode and new controller lifetime.</p>
</li>
<li id="q-221-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Pre-reset commands or stale CQE bytes do not establish post-reset liveness.</p>
</li>
<li id="q-221-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-221-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>A successful Keep Alive defines no separate success AER. <a class="qa-rule-link" href="#common-keepalive_op-9">Full rule in this volume</a></p>
</li>
<li id="q-221-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Keep Alive Timeout requires an Error Information entry with Keep Alive Timeout Expired within CQT cleanup time; this is an explicit requirement distinct from ordinary command-error logging. <a class="qa-rule-link" href="#common-keepalive_op-10">Full rule in this volume</a></p>
</li>
<li id="q-221-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>Supported PEL Controller Fatal Status hardware events follow the resulting CFS condition; individual Keep Alive commands are not a PEL trace. <a class="qa-rule-link" href="#common-keepalive_op-11">Full rule in this volume</a></p>
</li>
<li id="q-221-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Use scope, saveability and reset coverage; whole-subsystem and partial resets differ. <a class="qa-rule-link" href="#common-feature-12">Full rule in this volume</a></p>
</li>
<li id="q-221-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Establish whole or partial subsystem coverage; non-saveable persistent values do not thereby become zero. <a class="qa-rule-link" href="#common-feature-13">Full rule in this volume</a></p>
</li>
<li id="q-221-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Saveable values restore Saved; non-saveable values require their persistence and feature-specific rules. <a class="qa-rule-link" href="#common-feature-14">Full rule in this volume</a></p>
</li>
<li id="q-221-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>The timer targets a controller. <a class="qa-rule-link" href="#common-keepalive_op-15">Full rule in this volume</a></p>
</li>
<li id="q-221-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Validate restored configuration, not continuation of the old countdown to the millisecond.</p>
</li>
<li id="q-221-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>Read Current before deciding whether to reconfigure; rediscovery is not universally rewriting one value.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-keepalive">Base 2.4 §3.9 (common and PCIe rules), 5.2.30.1.9</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-commrecovery">Base 2.4 §9.1–9.6.2.1 (PCIe-applicable rules; stop before 9.6.2.2)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-222" data-question="222"><h2><a class="qa-qid" href="#q-222">Q222</a> How do command-based and traffic-based Keep Alive differ?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-222-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-222-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>One mode relies on explicit Keep Alive commands; the other can use normal command traffic.</p>
</li>
<li id="q-222-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Controller TBKAS determines support; the host cannot unilaterally assume traffic-based operation.</p>
</li>
<li id="q-222-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Check nonzero KAS and TBKAS; zero selects command-based behavior.</p>
</li>
<li id="q-222-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>Traffic-based controller checks for fetched commands per KATT interval; the host uses submitted-and-completed activity to decide whether to skip Keep Alive.</p>
</li>
<li id="q-222-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>In traffic-based mode the host should check every KATT/4 and send Keep Alive when qualifying traffic is absent.</p>
</li>
<li id="q-222-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>A fetch in an interval permits the next interval, so detection can take nearly 2×KATT after the last fetch.</p>
</li>
<li id="q-222-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Do not require expiry exactly KATT after the last fetch or treat one long outstanding command as new traffic in every interval.</p>
</li>
<li id="q-222-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-222-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>A successful Keep Alive defines no separate success AER. <a class="qa-rule-link" href="#common-keepalive_op-9">Full rule in this volume</a></p>
</li>
<li id="q-222-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Keep Alive Timeout requires an Error Information entry with Keep Alive Timeout Expired within CQT cleanup time; this is an explicit requirement distinct from ordinary command-error logging. <a class="qa-rule-link" href="#common-keepalive_op-10">Full rule in this volume</a></p>
</li>
<li id="q-222-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>Supported PEL Controller Fatal Status hardware events follow the resulting CFS condition; individual Keep Alive commands are not a PEL trace. <a class="qa-rule-link" href="#common-keepalive_op-11">Full rule in this volume</a></p>
</li>
<li id="q-222-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Use scope, saveability and reset coverage; whole-subsystem and partial resets differ. <a class="qa-rule-link" href="#common-feature-12">Full rule in this volume</a></p>
</li>
<li id="q-222-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Establish whole or partial subsystem coverage; non-saveable persistent values do not thereby become zero. <a class="qa-rule-link" href="#common-feature-13">Full rule in this volume</a></p>
</li>
<li id="q-222-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Saveable values restore Saved; non-saveable values require their persistence and feature-specific rules. <a class="qa-rule-link" href="#common-feature-14">Full rule in this volume</a></p>
</li>
<li id="q-222-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>The timer targets a controller. <a class="qa-rule-link" href="#common-keepalive_op-15">Full rule in this volume</a></p>
</li>
<li id="q-222-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Compare fetch/completion evidence and interval boundaries, not merely a prepared SQE.</p>
</li>
<li id="q-222-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First check mode agreement with TBKAS.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-keepalive">Base 2.4 §3.9 (common and PCIe rules), 5.2.30.1.9</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-commrecovery">Base 2.4 §9.1–9.6.2.1 (PCIe-applicable rules; stop before 9.6.2.2)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<section id="common-rules" class="qa-common"><h2>Shared rules linked from the answers</h2><p>Each shared mechanism is explained in full once in this volume. Use browser Back to return to the question; explicit command or feature exceptions take precedence.</p>
<article id="common-command-8"><h3>Command completion, events and records · How are DNR and More set?</h3><p>For a CQE, DNR=1 means the identical command is expected to fail if resubmitted to any controller in this subsystem; DNR=0 means it may succeed. Do not assign DNR=1 solely from an error name unless that condition mandates it. More=1 identifies additional information for this command in the Error Information Log. DNR should be zero when SCT=SC=0.</p></article>
<article id="common-feature-12"><h3>Feature reset and scope · What survives or continues after Controller Reset?</h3><p>Separate scope from saveability. For a reset covering the subsystem, a saveable Current value is restored from Saved, or Default if no Saved value exists; a non-saveable, nonpersistent value returns to Default. A partial reset uses Figure 127 for shared scopes. The specific feature exceptions in this question take precedence.</p></article>
<article id="common-feature-13"><h3>Feature reset and scope · What survives or continues after NVM Subsystem Reset?</h3><p>Determine reset coverage, not only its name. Figure 126 applies to the whole subsystem; Figure 127 applies to a partial multi-domain reset. A non-saveable feature specified as persistent remains persistent; non-saveable does not mean reset to zero.</p></article>
<article id="common-feature-14"><h3>Feature reset and scope · What survives or continues after a power cycle?</h3><p>A successfully saved SV=1 setting is restored from Saved across a power cycle; SV=0 does not update Saved. For non-saveable features use Figure 466 persistence and feature-specific exceptions. Verify Current and behavior rather than assuming an existing Saved value is already active.</p></article>
<article id="common-keepalive_op-9"><h3>Shared conditions for this topic · Is an asynchronous event generated?</h3><p>A successful Keep Alive defines no separate success AER. Timeout stops command processing and sets CFS, so the host cannot rely on continued AER delivery.</p></article>
<article id="common-keepalive_op-10"><h3>Shared conditions for this topic · Are Error Information or other logs updated?</h3><p>Keep Alive Timeout requires an Error Information entry with Keep Alive Timeout Expired within CQT cleanup time; this is an explicit requirement distinct from ordinary command-error logging.</p></article>
<article id="common-keepalive_op-11"><h3>Shared conditions for this topic · Is it recorded in the Persistent Event Log?</h3><p>Supported PEL Controller Fatal Status hardware events follow the resulting CFS condition; individual Keep Alive commands are not a PEL trace.</p></article>
<article id="common-keepalive_op-15"><h3>Shared conditions for this topic · Are other controllers or namespaces affected?</h3><p>The timer targets a controller. Cleanup stops its processing, not namespace or user-data deletion. Failover must still account for unresolved work on the failed path.</p></article>
</section>
<section id="source-index"><h2>Source locations and existing figure guides</h2><p>Base printed page = PDF page−26; the other two use identical numbers. Locations follow the supplied PDF body and retain figure numbers. Shared pages contribute only the relevant definitions, excluding Fabrics and PCIe link/packet content.</p><ul class="qa-references">
<li id="ref-reset"><strong>Base 2.4 · §3.7.1–3.7.4</strong><br>Printed pages 120–124 · PDF 146–150</li>
<li id="ref-keepalive"><strong>Base 2.4 · §3.9 (common and PCIe rules), 5.2.30.1.9</strong><br>Printed pages 129–135, 471 · PDF 155–161, 497 · Figure 481</li>
<li id="ref-status"><strong>Base 2.4 · §4.2.3</strong><br>Printed pages 145–155 · PDF 171–181 · Figure 101–105</li>
<li id="ref-feature"><strong>Base 2.4 · §4.4</strong><br>Printed pages 166–169 · PDF 192–195 · Figure 126–127</li>
<li id="ref-aer"><strong>Base 2.4 · §5.2.2</strong><br>Printed pages 183–190 · PDF 209–216 · Figure 150–156</li>
<li id="ref-error"><strong>Base 2.4 · §5.2.13.1.2</strong><br>Printed pages 218–220 · PDF 244–246 · Figure 212</li>
<li id="ref-pel"><strong>Base 2.4 · §5.2.13.1.14 (header, reset, hardware, Set Feature events)</strong><br>Printed pages 244–256, 258, 262–264 · PDF 270–282, 284, 288–290 · Figure 232–244, 246, 252–253</li>
<li id="ref-idctrl"><strong>Base 2.4 · §5.2.14.2.1</strong><br>Printed pages 340–387 · PDF 366–413 · Figure 338–341</li>
<li id="ref-setfeat"><strong>Base 2.4 · §5.2.30.1 (common fields, scope and persistence)</strong><br>Printed pages 456–460 · PDF 482–486 · Figure 463–466</li>
<li id="ref-commrecovery"><strong>Base 2.4 · §9.1–9.6.2.1 (PCIe-applicable rules; stop before 9.6.2.2)</strong><br>Printed pages 825–828 · PDF 851–854</li>
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
<nav class="qr-top" aria-label="Bank and editions"><a href="#content">Skip to content</a><a href="/nvme/question-bank/en/">Question index</a><a href="/nvme/question-bank/keep-alive/zh-tw/">繁體中文</a><a href="/DOCS/nvme-question-bank/keep-alive.html">Chinese tutorial HTML</a></nav>
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
