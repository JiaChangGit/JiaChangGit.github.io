---
layout: post
title: "NVMe Self-Study Bank: Asynchronous Event Request"
date: 2026-10-02 00:00:00 +0800
categories: [nvme]
permalink: /nvme/question-bank/asynchronous-events/en/
lang: en
nvme_quickref: true
nvme_qa: true
---

<div class="nvme-quickref nvme-qa">
<nav class="qr-top" aria-label="Bank and editions"><a href="#content">Skip to content</a><a href="/nvme/question-bank/en/">Question index</a><a href="/nvme/question-bank/asynchronous-events/zh-tw/">繁體中文</a><a href="/DOCS/nvme-question-bank/asynchronous-events.html">Chinese tutorial HTML</a></nav>
<main id="content"><p class="qr-eyebrow">BASE 2.4 / NVM 1.3 / PCIe 1.4 · Q1–320</p>
<header><p class="qa-range">Q82–Q92</p><h1>Asynchronous Event Request</h1><p class="qr-intro">AER preposts requests that complete on events. Connect requests, events, logs and acknowledgment before concurrency and rearming.</p><p>Practice first, then reveal 17 answer items per question. All numerical examples are hypothetical. Status is written SCT/SC; h indicates hexadecimal.</p></header>
<aside class="qa-glossary"><h2>Terms used in this volume</h2><dl><dt>Controller / namespace</dt><dd>A controller receives commands and manages access. A namespace is a logical storage space that commands can address. An NVM subsystem contains controllers and nonvolatile storage resources.</dd><dt>SQ / CQ / SQE / CQE</dt><dd>Submission and Completion Queues carry command entries (SQEs) and completion entries (CQEs). QID identifies a queue, CID distinguishes outstanding commands in one SQ, and NSID identifies a namespace.</dd><dt>Register / Identify / Feature / Log</dt><dd>A register exposes control or state. Identify queries capabilities and attributes; features query or configure operation; log pages report specific state or records. FID, LID, CNS and CSI select features, logs, Identify structures and command sets.</dd><dt>index / offset / zero-based</dt><dd>An index selects an entry, usually starting at 0; an offset measures distance from an origin in specified units. A zero-based count encodes count−1, but not every zero-valued field is a count. A Dword is 4 bytes; a byte is 8 bits.</dd><dt>Scope / reset / retention</dt><dd>Scope names the affected objects; retention means preserving state. Controller Reset (clearing CC.EN) is one form of Controller Level Reset, or CLR. Different CLR triggers can retain different registers.</dd></dl></aside>
<section id="overview" class="qa-overview"><h2>Notification completion is not the end</h2><p class="qa-takeaway">An AER supplies event identity; logs provide detail and current state.</p>
<div class="qr-table" tabindex="0" role="region" aria-label="Horizontally scrollable comparison table"><table><thead><tr><th scope="col">Stage</th><th scope="col">Action</th><th scope="col">Evidence</th></tr></thead><tbody><tr><td>Before event</td><td>Host submits AER</td><td>Request identity and AERL+1 limit</td></tr><tr><td>Event occurs</td><td>Controller completes a request</td><td>Type, information, LID</td></tr><tr><td>Inspect</td><td>Host reads matching log</td><td>Selectors, RAE and raw data</td></tr><tr><td>Continue</td><td>Host posts another AER</td><td>New outstanding request</td></tr></tbody></table></div>
<p><strong>Worked interpretation: </strong>AERL3 allows four requests. Replace a completed request; a completed unrearmed request cannot receive another event.</p>
<p class="qa-citations">Sources: <a href="#ref-aerfull">Base 2.4 §5.2.2 (PCIe-applicable events)</a> · <a href="#ref-getlog">Base 2.4 §5.2.13–5.2.13.1.1</a> · <a href="#ref-aec">Base 2.4 §5.2.30.1.6</a></p>
</section>
<div class="qa-controls" hidden><label>Search this page <input type="search" id="qa-search" placeholder="Question number, field or keyword"></label><button type="button" data-expand="true">Expand all answers</button><button type="button" data-expand="false">Collapse all answers</button><output id="qa-count" aria-live="polite"></output></div>
<section id="question-index"><h2>Questions in this volume</h2><ol class="qa-index">
<li><a href="#q-082">Q82 · Why post Asynchronous Event Requests before events, and why do they remain outstanding?</a></li>
<li><a href="#q-083">Q83 · How does AER completion identify the event and its log?</a></li>
<li><a href="#q-084">Q84 · Why read the associated log and post another AER after an event?</a></li>
<li><a href="#q-085">Q85 · What happens when outstanding AERs exceed the controller limit?</a></li>
<li><a href="#q-086">Q86 · How are events handled when no AER is outstanding?</a></li>
<li><a href="#q-087">Q87 · How can concurrent identical or different events be combined and reported?</a></li>
<li><a href="#q-088">Q88 · How does Asynchronous Event Configuration enable or disable notifications?</a></li>
<li><a href="#q-089">Q89 · What notification conditions apply to SMART, namespaces, firmware, telemetry, sanitize, self-test and PEL?</a></li>
<li><a href="#q-090">Q90 · How does reading a log clear or retain an event?</a></li>
<li><a href="#q-091">Q91 · Can AER be aborted, and what happens to pending requests during reset?</a></li>
<li><a href="#q-092">Q92 · How should an AER be investigated when the associated log lacks expected information?</a></li>
</ol></section>
<article class="qa-question" id="q-082" data-question="82"><h2><a class="qa-qid" href="#q-082">Q82</a> Why post Asynchronous Event Requests before events, and why do they remain outstanding?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-082-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-082-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>AER provides a request the controller can complete to report an event. It is not an unsolicited ordinary completion without a corresponding request, so the host posts requests in advance.</p>
</li>
<li id="q-082-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Each AER belongs to its controller and Admin Queue. It waits for an event rather than reading or writing a namespace.</p>
</li>
<li id="q-082-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Identify.AERL+1 limits outstanding requests. OAES and FID 0Bh govern optional notifications; AERL is not an event-type count.</p>
</li>
<li id="q-082-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>Command-specific fields are reserved; allocate a unique outstanding Admin CID. Event completion supplies AET/AEI/LID in DW0 and event-specific DW1 where defined.</p>
</li>
<li id="q-082-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>After initialization and notification setup, post requests within the limit. Preserve a returned event, handle and acknowledge it, then replenish the request pool.</p>
</li>
<li id="q-082-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Remaining outstanding without events is normal; the host should not assign an ordinary timeout. AER does not need periodic success completions as a liveness signal.</p>
</li>
<li id="q-082-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Exceeding the outstanding limit can produce Asynchronous Event Request Limit Exceeded (1/05h). Waiting without an event is not a specified timeout error.</p>
</li>
<li id="q-082-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-082-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>AER reports an event by completing a request. <a class="qa-rule-link" href="#common-aer_request-9">Full rule in this volume</a></p>
</li>
<li id="q-082-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Use AET, AEI and LID to select the associated log. <a class="qa-rule-link" href="#common-aer_request-10">Full rule in this volume</a></p>
</li>
<li id="q-082-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>PEL logging depends on the underlying event, not on AER completion. <a class="qa-rule-link" href="#common-aer_request-11">Full rule in this volume</a></p>
</li>
<li id="q-082-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Controller Reset aborts outstanding AERs without CQEs. <a class="qa-rule-link" href="#common-aer_request-12">Full rule in this volume</a></p>
</li>
<li id="q-082-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>After subsystem reset, reestablish Admin Queues and AERs on affected controllers. <a class="qa-rule-link" href="#common-aer_request-13">Full rule in this volume</a></p>
</li>
<li id="q-082-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Old AERs are invalid after a power cycle. <a class="qa-rule-link" href="#common-aer_request-14">Full rule in this volume</a></p>
</li>
<li id="q-082-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Requests and completions belong to a controller, while event scope may be a namespace, domain or subsystem. <a class="qa-rule-link" href="#common-aer_request-15">Full rule in this volume</a></p>
</li>
<li id="q-082-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Compare outstanding request count, AERL, notification configuration and event conditions rather than elapsed seconds alone.</p>
</li>
<li id="q-082-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First establish that a request was actually submitted and remains outstanding.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-aerfull">Base 2.4 §5.2.2 (PCIe-applicable events)</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-aec">Base 2.4 §5.2.30.1.6</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-083" data-question="83"><h2><a class="qa-qid" href="#q-083">Q83</a> How does AER completion identify the event and its log?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-083-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-083-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>A successful status completes the AER; the actual event is in its command-specific result. Decode that result to select the next log.</p>
</li>
<li id="q-083-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Match the request by SQID/CID before decoding the controller’s event; another Admin command’s DW0 need not use the AER format.</p>
</li>
<li id="q-083-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Capabilities and event tables define the supported events. Decode AET first to select the AEI table.</p>
</li>
<li id="q-083-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>DW0[2:0] is AET, [15:8] AEI and [23:16] LID. DW1 is event-specific; do not assume it is NSID without a definition.</p>
</li>
<li id="q-083-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Validate phase and identity, then SCT/SC. For normal event completions, decode the event and follow its associated read or handling rule.</p>
</li>
<li id="q-083-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Firmware Activation Starting is a Notice pointing to Firmware Slot Information; it signals starting, not completion. Sanitize events additionally use their defined DW1 target.</p>
</li>
<li id="q-083-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Do not decode arbitrary DW0 as an event when the AER itself failed. Identical AEI values can mean different things under different AETs.</p>
</li>
<li id="q-083-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-083-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>AER reports an event by completing a request. <a class="qa-rule-link" href="#common-aer_request-9">Full rule in this volume</a></p>
</li>
<li id="q-083-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Use AET, AEI and LID to select the associated log. <a class="qa-rule-link" href="#common-aer_request-10">Full rule in this volume</a></p>
</li>
<li id="q-083-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>PEL logging depends on the underlying event, not on AER completion. <a class="qa-rule-link" href="#common-aer_request-11">Full rule in this volume</a></p>
</li>
<li id="q-083-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Controller Reset aborts outstanding AERs without CQEs. <a class="qa-rule-link" href="#common-aer_request-12">Full rule in this volume</a></p>
</li>
<li id="q-083-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>After subsystem reset, reestablish Admin Queues and AERs on affected controllers. <a class="qa-rule-link" href="#common-aer_request-13">Full rule in this volume</a></p>
</li>
<li id="q-083-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Old AERs are invalid after a power cycle. <a class="qa-rule-link" href="#common-aer_request-14">Full rule in this volume</a></p>
</li>
<li id="q-083-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Requests and completions belong to a controller, while event scope may be a namespace, domain or subsystem. <a class="qa-rule-link" href="#common-aer_request-15">Full rule in this volume</a></p>
</li>
<li id="q-083-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Preserve raw CQE and subsequent log, checking LID and target instead of retaining only a translated message.</p>
</li>
<li id="q-083-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First check the AET-selected decoding table, then LID and DW1.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-aerfull">Base 2.4 §5.2.2 (PCIe-applicable events)</a> · <a href="#ref-cqe">Base 2.4 §4.2.1, 4.2.3–4.2.4</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-084" data-question="84"><h2><a class="qa-qid" href="#q-084">Q84</a> Why read the associated log and post another AER after an event?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-084-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-084-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Reading the log obtains and acknowledges event information; posting AER supplies the next response opportunity. Missing either can stall future notification.</p>
</li>
<li id="q-084-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Ordinary reported event types are automatically masked until acknowledged. Immediate and One-Shot events have separate clearing behavior.</p>
</li>
<li id="q-084-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Check the event’s LID, RAE rule and enablement. AERL limits outstanding requests; it does not unmask events.</p>
</li>
<li id="q-084-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>Ordinary acknowledgment uses Get Log Page with RAE=0; RAE=1 retains the event. The replacement AER is another Admin command with a valid CID.</p>
</li>
<li id="q-084-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Preserve the notification, read and process evidence, acknowledge as defined and maintain request availability. For persistent conditions, consider threshold or mask changes before acknowledgment to avoid repeated reports.</p>
</li>
<li id="q-084-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Acknowledgment permits further reporting, but a continuing condition can be reported again. Posting another AER alone does not clear the original event.</p>
</li>
<li id="q-084-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Failed reads retain the event; an attempted RAE=0 request is not success. One-Shot events clear on reporting and follow their specific handling.</p>
</li>
<li id="q-084-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-084-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>AER reports an event by completing a request. <a class="qa-rule-link" href="#common-aer_request-9">Full rule in this volume</a></p>
</li>
<li id="q-084-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Use AET, AEI and LID to select the associated log. <a class="qa-rule-link" href="#common-aer_request-10">Full rule in this volume</a></p>
</li>
<li id="q-084-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>PEL logging depends on the underlying event, not on AER completion. <a class="qa-rule-link" href="#common-aer_request-11">Full rule in this volume</a></p>
</li>
<li id="q-084-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Controller Reset aborts outstanding AERs without CQEs. <a class="qa-rule-link" href="#common-aer_request-12">Full rule in this volume</a></p>
</li>
<li id="q-084-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>After subsystem reset, reestablish Admin Queues and AERs on affected controllers. <a class="qa-rule-link" href="#common-aer_request-13">Full rule in this volume</a></p>
</li>
<li id="q-084-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Old AERs are invalid after a power cycle. <a class="qa-rule-link" href="#common-aer_request-14">Full rule in this volume</a></p>
</li>
<li id="q-084-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Requests and completions belong to a controller, while event scope may be a namespace, domain or subsystem. <a class="qa-rule-link" href="#common-aer_request-15">Full rule in this volume</a></p>
</li>
<li id="q-084-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Verify evidence preservation, successful acknowledgment and an available AER separately; one status does not prove all three.</p>
</li>
<li id="q-084-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First distinguish a missing acknowledgment from a missing replacement request.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-aerfull">Base 2.4 §5.2.2 (PCIe-applicable events)</a> · <a href="#ref-getlog">Base 2.4 §5.2.13–5.2.13.1.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-085" data-question="85"><h2><a class="qa-qid" href="#q-085">Q85</a> What happens when outstanding AERs exceed the controller limit?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-085-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-085-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>The limit bounds waiting request resources, not the number of possible events.</p>
</li>
<li id="q-085-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>It applies to concurrent outstanding AERs on this controller, not lifetime submissions across the subsystem.</p>
</li>
<li id="q-085-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>AERL is zero-based: AERL=3 permits four outstanding requests.</p>
</li>
<li id="q-085-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>Track CID and submission/completion times. Completed requests no longer consume the limit; update tracking before replenishing.</p>
</li>
<li id="q-085-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Read AERL and post within the limit. For an excess-request test, add one while controlling concurrent event completions that could free a slot.</p>
</li>
<li id="q-085-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Within the limit, requests wait normally. A concurrent completion can make a later request valid; total submission count is insufficient.</p>
</li>
<li id="q-085-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Excess AERs use Asynchronous Event Request Limit Exceeded (1/05h), not Abort Command Limit Exceeded (1/03h).</p>
</li>
<li id="q-085-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-085-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>AER reports an event by completing a request. <a class="qa-rule-link" href="#common-aer_request-9">Full rule in this volume</a></p>
</li>
<li id="q-085-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Use AET, AEI and LID to select the associated log. <a class="qa-rule-link" href="#common-aer_request-10">Full rule in this volume</a></p>
</li>
<li id="q-085-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>PEL logging depends on the underlying event, not on AER completion. <a class="qa-rule-link" href="#common-aer_request-11">Full rule in this volume</a></p>
</li>
<li id="q-085-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Controller Reset aborts outstanding AERs without CQEs. <a class="qa-rule-link" href="#common-aer_request-12">Full rule in this volume</a></p>
</li>
<li id="q-085-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>After subsystem reset, reestablish Admin Queues and AERs on affected controllers. <a class="qa-rule-link" href="#common-aer_request-13">Full rule in this volume</a></p>
</li>
<li id="q-085-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Old AERs are invalid after a power cycle. <a class="qa-rule-link" href="#common-aer_request-14">Full rule in this volume</a></p>
</li>
<li id="q-085-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Requests and completions belong to a controller, while event scope may be a namespace, domain or subsystem. <a class="qa-rule-link" href="#common-aer_request-15">Full rule in this volume</a></p>
</li>
<li id="q-085-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Compare AERL+1 against concurrent outstanding counts and account for slots freed by event completions.</p>
</li>
<li id="q-085-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First check the +1 conversion and removal of completed requests from the outstanding set.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-aerfull">Base 2.4 §5.2.2 (PCIe-applicable events)</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-086" data-question="86"><h2><a class="qa-qid" href="#q-086">Q86</a> How are events handled when no AER is outstanding?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-086-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-086-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Distinguish occurrence from delivery. No request does not imply no event, but not every event must wait indefinitely.</p>
</li>
<li id="q-086-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Ordinary, Immediate and One-Shot events differ; establish enablement and masking first.</p>
</li>
<li id="q-086-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Check OAES, FID 0Bh, event type and request history. Log support alone does not enable every related event.</p>
</li>
<li id="q-086-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>Ordinary pending information can supply a later AER. Immediate events require an outstanding request at occurrence and must not be reported otherwise.</p>
</li>
<li id="q-086-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Trigger an enabled ordinary event without a request, then post AER. A clearing log read or CLR in between removes the basis for expecting the old notification.</p>
</li>
<li id="q-086-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>For enabled ordinary events, the specification recommends retaining information for the next request. This is should, not unconditional permanent retention for all event classes.</p>
</li>
<li id="q-086-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Absence of a request does not create an error CQE. Omitting an Immediate event under these conditions is required, not a firmware notification-loss defect.</p>
</li>
<li id="q-086-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-086-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>AER reports an event by completing a request. <a class="qa-rule-link" href="#common-aer_request-9">Full rule in this volume</a></p>
</li>
<li id="q-086-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Use AET, AEI and LID to select the associated log. <a class="qa-rule-link" href="#common-aer_request-10">Full rule in this volume</a></p>
</li>
<li id="q-086-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>PEL logging depends on the underlying event, not on AER completion. <a class="qa-rule-link" href="#common-aer_request-11">Full rule in this volume</a></p>
</li>
<li id="q-086-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Controller Reset aborts outstanding AERs without CQEs. <a class="qa-rule-link" href="#common-aer_request-12">Full rule in this volume</a></p>
</li>
<li id="q-086-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>After subsystem reset, reestablish Admin Queues and AERs on affected controllers. <a class="qa-rule-link" href="#common-aer_request-13">Full rule in this volume</a></p>
</li>
<li id="q-086-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Old AERs are invalid after a power cycle. <a class="qa-rule-link" href="#common-aer_request-14">Full rule in this volume</a></p>
</li>
<li id="q-086-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Requests and completions belong to a controller, while event scope may be a namespace, domain or subsystem. <a class="qa-rule-link" href="#common-aer_request-15">Full rule in this volume</a></p>
</li>
<li id="q-086-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Correlate occurrence, request, acknowledgment and CLR times to determine whether a notification should remain pending.</p>
</li>
<li id="q-086-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>Identify the event class before applying ordinary pending-event retention.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-aerfull">Base 2.4 §5.2.2 (PCIe-applicable events)</a> · <a href="#ref-getlog">Base 2.4 §5.2.13–5.2.13.1.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-087" data-question="87"><h2><a class="qa-qid" href="#q-087">Q87</a> How can concurrent identical or different events be combined and reported?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-087-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-087-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Notification can consolidate conditions while preserving actionable information. Occurrences, log entries and AER completions need not correspond one-to-one.</p>
</li>
<li id="q-087-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Events of the same type with identical responses may be combined. Different types or responses have a queuing recommendation; automatic masking also affects reporting.</p>
</li>
<li id="q-087-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Establish support/enablement and available request count. One request cannot simultaneously yield several independent completions.</p>
</li>
<li id="q-087-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>Compare AET, AEI, LID and event-specific parameters, not AEI alone.</p>
</li>
<li id="q-087-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Trigger known conditions, preserve responses and process logs/replenish requests. Check acknowledgment before expecting further notifications of a masked type.</p>
</li>
<li id="q-087-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Combining identical responses is permitted; queuing differing responses is recommended. AER order does not thereby provide a precise timeline of every internal occurrence.</p>
</li>
<li id="q-087-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Legitimate consolidation is not a missing-completion error. Excess requests separately invoke 1/05h handling.</p>
</li>
<li id="q-087-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-087-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>AER reports an event by completing a request. <a class="qa-rule-link" href="#common-aer_request-9">Full rule in this volume</a></p>
</li>
<li id="q-087-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Use AET, AEI and LID to select the associated log. <a class="qa-rule-link" href="#common-aer_request-10">Full rule in this volume</a></p>
</li>
<li id="q-087-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>PEL logging depends on the underlying event, not on AER completion. <a class="qa-rule-link" href="#common-aer_request-11">Full rule in this volume</a></p>
</li>
<li id="q-087-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Controller Reset aborts outstanding AERs without CQEs. <a class="qa-rule-link" href="#common-aer_request-12">Full rule in this volume</a></p>
</li>
<li id="q-087-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>After subsystem reset, reestablish Admin Queues and AERs on affected controllers. <a class="qa-rule-link" href="#common-aer_request-13">Full rule in this volume</a></p>
</li>
<li id="q-087-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Old AERs are invalid after a power cycle. <a class="qa-rule-link" href="#common-aer_request-14">Full rule in this volume</a></p>
</li>
<li id="q-087-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Requests and completions belong to a controller, while event scope may be a namespace, domain or subsystem. <a class="qa-rule-link" href="#common-aer_request-15">Full rule in this volume</a></p>
</li>
<li id="q-087-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Use log records or generations to supplement notifications rather than treating AER count as fault count.</p>
</li>
<li id="q-087-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First check identical responses and whether the previous notification remains masked.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-aerfull">Base 2.4 §5.2.2 (PCIe-applicable events)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-088" data-question="88"><h2><a class="qa-qid" href="#q-088">Q88</a> How does Asynchronous Event Configuration enable or disable notifications?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-088-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-088-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>FID 0Bh selects applicable notifications. It neither removes the underlying condition nor submits AERs automatically.</p>
</li>
<li id="q-088-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>It configures specified SMART and optional notifications on a controller, not a universal switch for all Error events.</p>
</li>
<li id="q-088-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Check OAES and applicable support, then Current FID 0Bh. Configuration enablement and automatic pending-event masking are separate states.</p>
</li>
<li id="q-088-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>Set CDW11 enables notification bits; Get returns Current. The bitmap is not the AET/AEI encoding of an AER completion.</p>
</li>
<li id="q-088-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Set valid bits, await success, read Current, ensure a pending AER and establish the condition. Conditions already true at enablement follow the feature’s rules as well.</p>
</li>
<li id="q-088-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Success establishes configuration; delivery still depends on condition, masking and requests. Disabling notification does not necessarily clear the warning itself.</p>
</li>
<li id="q-088-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Enabling unsupported events returns Invalid Field (0/02h). Lack of an available AER is not a Set Features failure status.</p>
</li>
<li id="q-088-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-088-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>AER reports an event by completing a request. <a class="qa-rule-link" href="#common-aer_request-9">Full rule in this volume</a></p>
</li>
<li id="q-088-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Use AET, AEI and LID to select the associated log. <a class="qa-rule-link" href="#common-aer_request-10">Full rule in this volume</a></p>
</li>
<li id="q-088-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>PEL logging depends on the underlying event, not on AER completion. <a class="qa-rule-link" href="#common-aer_request-11">Full rule in this volume</a></p>
</li>
<li id="q-088-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Controller Reset aborts outstanding AERs without CQEs. <a class="qa-rule-link" href="#common-aer_request-12">Full rule in this volume</a></p>
</li>
<li id="q-088-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>After subsystem reset, reestablish Admin Queues and AERs on affected controllers. <a class="qa-rule-link" href="#common-aer_request-13">Full rule in this volume</a></p>
</li>
<li id="q-088-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Old AERs are invalid after a power cycle. <a class="qa-rule-link" href="#common-aer_request-14">Full rule in this volume</a></p>
</li>
<li id="q-088-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Requests and completions belong to a controller, while event scope may be a namespace, domain or subsystem. <a class="qa-rule-link" href="#common-aer_request-15">Full rule in this volume</a></p>
</li>
<li id="q-088-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Correlate support, current mask, actual condition and AER availability. Set success alone does not validate the whole notification path.</p>
</li>
<li id="q-088-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First distinguish disabled notification from automatic masking after a previous report.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-aec">Base 2.4 §5.2.30.1.6</a> · <a href="#ref-aerfull">Base 2.4 §5.2.2 (PCIe-applicable events)</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-089" data-question="89"><h2><a class="qa-qid" href="#q-089">Q89</a> What notification conditions apply to SMART, namespaces, firmware, telemetry, sanitize, self-test and PEL?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-089-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-089-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Correct the assumption that every function has a completion AER. Events require an actual specification definition; having a log is insufficient.</p>
</li>
<li id="q-089-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Events can describe controller health, namespace changes, activation or sanitization targets. Match the affected scope, not only the receiving controller.</p>
</li>
<li id="q-089-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Use OAES, FID 0Bh and event tables. Self-test or PEL support does not automatically define a generic Self-test Completed or PEL Changed AER.</p>
</li>
<li id="q-089-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>SMART uses 02h; attached/allocated namespace changes use 04h/1Ch; activation starting uses 03h; telemetry changes use 08h; sanitize events use 81h.</p>
</li>
<li id="q-089-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Identify the event condition before selecting its log. Normal self-test completion is established from 06h; a separately applicable Diagnostic Failure uses the Error event rules.</p>
</li>
<li id="q-089-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Sanitize distinguishes completion, unexpected deallocation and entry into Media Verification. Activation Starting likewise does not establish final activation success.</p>
</li>
<li id="q-089-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Absence of an undefined completion event is not an error. A missing-event claim must establish the defined event, support, enablement and request conditions.</p>
</li>
<li id="q-089-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-089-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>AER reports an event by completing a request. <a class="qa-rule-link" href="#common-aer_request-9">Full rule in this volume</a></p>
</li>
<li id="q-089-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Use AET, AEI and LID to select the associated log. <a class="qa-rule-link" href="#common-aer_request-10">Full rule in this volume</a></p>
</li>
<li id="q-089-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>PEL logging depends on the underlying event, not on AER completion. <a class="qa-rule-link" href="#common-aer_request-11">Full rule in this volume</a></p>
</li>
<li id="q-089-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Controller Reset aborts outstanding AERs without CQEs. <a class="qa-rule-link" href="#common-aer_request-12">Full rule in this volume</a></p>
</li>
<li id="q-089-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>After subsystem reset, reestablish Admin Queues and AERs on affected controllers. <a class="qa-rule-link" href="#common-aer_request-13">Full rule in this volume</a></p>
</li>
<li id="q-089-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Old AERs are invalid after a power cycle. <a class="qa-rule-link" href="#common-aer_request-14">Full rule in this volume</a></p>
</li>
<li id="q-089-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Requests and completions belong to a controller, while event scope may be a namespace, domain or subsystem. <a class="qa-rule-link" href="#common-aer_request-15">Full rule in this volume</a></p>
</li>
<li id="q-089-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Compare operation results, dedicated logs and AER conditions separately, then supplement with supported PEL events; they need not map one-to-one.</p>
</li>
<li id="q-089-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First verify that the expected event is actually defined in this revision.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-aerfull">Base 2.4 §5.2.2 (PCIe-applicable events)</a> · <a href="#ref-smart">Base 2.4 §5.2.13.1.3</a> · <a href="#ref-dstlog">Base 2.4 §5.2.13.1.7</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-090" data-question="90"><h2><a class="qa-qid" href="#q-090">Q90</a> How does reading a log clear or retain an event?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-090-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-090-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Acknowledgment controls further reporting; it does not erase all history or repair the cause. The underlying warning may remain.</p>
</li>
<li id="q-090-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Use the event’s specified log and target. Reading another log or target need not acknowledge it.</p>
</li>
<li id="q-090-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Establish ordinary log-based acknowledgment versus Immediate/One-Shot behavior before applying RAE.</p>
</li>
<li id="q-090-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>RAE=0 clears the associated event on success; RAE=1 retains it. LID, NSID and other selectors still must identify the correct log view.</p>
</li>
<li id="q-090-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Preserve notification and state, retain where needed with RAE=1, and acknowledge via the applicable successful RAE=0 read. Do not invent a universal partial-read acknowledgment rule.</p>
</li>
<li id="q-090-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Successful acknowledgment unmasks as defined; a continuing condition can recur. RAE retains the event, not necessarily a frozen data snapshot.</p>
</li>
<li id="q-090-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Failed Gets must retain the event regardless of the requested RAE=0.</p>
</li>
<li id="q-090-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-090-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>AER reports an event by completing a request. <a class="qa-rule-link" href="#common-aer_request-9">Full rule in this volume</a></p>
</li>
<li id="q-090-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Use AET, AEI and LID to select the associated log. <a class="qa-rule-link" href="#common-aer_request-10">Full rule in this volume</a></p>
</li>
<li id="q-090-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>PEL logging depends on the underlying event, not on AER completion. <a class="qa-rule-link" href="#common-aer_request-11">Full rule in this volume</a></p>
</li>
<li id="q-090-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Controller Reset aborts outstanding AERs without CQEs. <a class="qa-rule-link" href="#common-aer_request-12">Full rule in this volume</a></p>
</li>
<li id="q-090-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>After subsystem reset, reestablish Admin Queues and AERs on affected controllers. <a class="qa-rule-link" href="#common-aer_request-13">Full rule in this volume</a></p>
</li>
<li id="q-090-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Old AERs are invalid after a power cycle. <a class="qa-rule-link" href="#common-aer_request-14">Full rule in this volume</a></p>
</li>
<li id="q-090-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Requests and completions belong to a controller, while event scope may be a namespace, domain or subsystem. <a class="qa-rule-link" href="#common-aer_request-15">Full rule in this volume</a></p>
</li>
<li id="q-090-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Correlate successful completion time, RAE, mask state and later notifications. Current state can differ from event-time state without invalidating acknowledgment.</p>
</li>
<li id="q-090-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First establish that acknowledgment completed successfully rather than merely being submitted.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-aerfull">Base 2.4 §5.2.2 (PCIe-applicable events)</a> · <a href="#ref-getlog">Base 2.4 §5.2.13–5.2.13.1.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-091" data-question="91"><h2><a class="qa-qid" href="#q-091">Q91</a> Can AER be aborted, and what happens to pending requests during reset?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-091-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-091-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>AER has an Admin CID despite not having an ordinary timeout. Distinguish a targeted Abort from resetting the whole controller.</p>
</li>
<li id="q-091-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Target the AER with SQID=0 and its CID; controller reset affects all its outstanding AERs.</p>
</li>
<li id="q-091-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>ACL+1 limits concurrent Aborts, independently of AERL+1. Aborting AER has no universal success guarantee beyond Abort semantics.</p>
</li>
<li id="q-091-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>Track the Abort CID, target CID and IANP. IANP=0 identifies immediate abort; IANP=1 does not rule out a later deferred abort.</p>
</li>
<li id="q-091-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Process Abort and target results separately. If resetting instead, terminate old tracking under reset rules and post new AERs after recovery without waiting for reset-aborted CQEs.</p>
</li>
<li id="q-091-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>An event can win the race and complete normally. An aborted target reports Command Abort Requested; a controller-reset-aborted AER must not return a CQE. These outcomes differ.</p>
</li>
<li id="q-091-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Excess Abort commands may return 1/03h. A missing/already-completed target does not universally make Abort fail; inspect IANP and target completion history.</p>
</li>
<li id="q-091-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-091-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>AER reports an event by completing a request. <a class="qa-rule-link" href="#common-aer_request-9">Full rule in this volume</a></p>
</li>
<li id="q-091-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Use AET, AEI and LID to select the associated log. <a class="qa-rule-link" href="#common-aer_request-10">Full rule in this volume</a></p>
</li>
<li id="q-091-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>PEL logging depends on the underlying event, not on AER completion. <a class="qa-rule-link" href="#common-aer_request-11">Full rule in this volume</a></p>
</li>
<li id="q-091-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Controller Reset aborts outstanding AERs without CQEs. <a class="qa-rule-link" href="#common-aer_request-12">Full rule in this volume</a></p>
</li>
<li id="q-091-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>After subsystem reset, reestablish Admin Queues and AERs on affected controllers. <a class="qa-rule-link" href="#common-aer_request-13">Full rule in this volume</a></p>
</li>
<li id="q-091-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Old AERs are invalid after a power cycle. <a class="qa-rule-link" href="#common-aer_request-14">Full rule in this volume</a></p>
</li>
<li id="q-091-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Requests and completions belong to a controller, while event scope may be a namespace, domain or subsystem. <a class="qa-rule-link" href="#common-aer_request-15">Full rule in this volume</a></p>
</li>
<li id="q-091-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Correlate CIDs within one Admin Queue lifetime so reused post-reset CIDs are not mistaken for old targets.</p>
</li>
<li id="q-091-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First identify event completion, Abort or reset termination before deciding whether a CQE is expected.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-aerfull">Base 2.4 §5.2.2 (PCIe-applicable events)</a> · <a href="#ref-abort">Base 2.4 §5.2.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-092" data-question="92"><h2><a class="qa-qid" href="#q-092">Q92</a> How should an AER be investigated when the associated log lacks expected information?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-092-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-092-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Notifications describe an occurrence; logs may show current state or bounded history rather than a same-time copy. Identify the data model before claiming inconsistency.</p>
</li>
<li id="q-092-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Fix controller, target and interface. Another host may have read or acknowledged shared state outside the local trace.</p>
</li>
<li id="q-092-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Check the event definition/LID and the log’s update, clearing and retention rules. Not every event creates an entry.</p>
</li>
<li id="q-092-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>Preserve CQE, selectors, RAE, time and valid fields. SMART Critical Warning reflects Get processing time and may differ from event-time state.</p>
</li>
<li id="q-092-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Exclude wrong log/target, intervening reads/reset, generation changes and recovered transient conditions before testing a specific retention requirement.</p>
</li>
<li id="q-092-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Temperature can trigger an event and fall before SMART is read. Conversely, a More=1 command error calls for correlatable supplemental information under its own rules.</p>
</li>
<li id="q-092-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Missing expected data does not rewrite the successful AER status. Preserve a subsequent Get failure separately.</p>
</li>
<li id="q-092-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-092-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>AER reports an event by completing a request. <a class="qa-rule-link" href="#common-aer_request-9">Full rule in this volume</a></p>
</li>
<li id="q-092-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Use AET, AEI and LID to select the associated log. <a class="qa-rule-link" href="#common-aer_request-10">Full rule in this volume</a></p>
</li>
<li id="q-092-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>PEL logging depends on the underlying event, not on AER completion. <a class="qa-rule-link" href="#common-aer_request-11">Full rule in this volume</a></p>
</li>
<li id="q-092-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Controller Reset aborts outstanding AERs without CQEs. <a class="qa-rule-link" href="#common-aer_request-12">Full rule in this volume</a></p>
</li>
<li id="q-092-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>After subsystem reset, reestablish Admin Queues and AERs on affected controllers. <a class="qa-rule-link" href="#common-aer_request-13">Full rule in this volume</a></p>
</li>
<li id="q-092-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Old AERs are invalid after a power cycle. <a class="qa-rule-link" href="#common-aer_request-14">Full rule in this volume</a></p>
</li>
<li id="q-092-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Requests and completions belong to a controller, while event scope may be a namespace, domain or subsystem. <a class="qa-rule-link" href="#common-aer_request-15">Full rule in this volume</a></p>
</li>
<li id="q-092-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Establish the event condition, log time model and intervening actions. A contradiction requires the relevant retention preconditions to hold.</p>
</li>
<li id="q-092-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First distinguish current-state logs from event history; that determines whether event-time values must remain visible.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-aerfull">Base 2.4 §5.2.2 (PCIe-applicable events)</a> · <a href="#ref-getlog">Base 2.4 §5.2.13–5.2.13.1.1</a> · <a href="#ref-smart">Base 2.4 §5.2.13.1.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
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
</section>
<section id="source-index"><h2>Source locations and existing figure guides</h2><p>Base printed page = PDF page−26; the other two use identical numbers. Locations follow the supplied PDF body and retain figure numbers. Shared pages contribute only the relevant definitions, excluding Fabrics and PCIe link/packet content.</p><ul class="qa-references">
<li id="ref-reset"><strong>Base 2.4 · §3.7.1–3.7.4</strong><br>Printed pages 120–124 · PDF 146–150</li>
<li id="ref-cqe"><strong>Base 2.4 · §4.2.1, 4.2.3–4.2.4</strong><br>Printed pages 144–157 · PDF 170–183 · Figure 97–105, 109</li>
<li id="ref-status"><strong>Base 2.4 · §4.2.3</strong><br>Printed pages 145–155 · PDF 171–181 · Figure 101–105</li>
<li id="ref-abort"><strong>Base 2.4 · §5.2.1</strong><br>Printed pages 181–182 · PDF 207–208 · Figure 147–149</li>
<li id="ref-aer"><strong>Base 2.4 · §5.2.2</strong><br>Printed pages 183–190 · PDF 209–216 · Figure 150–156</li>
<li id="ref-aerfull"><strong>Base 2.4 · §5.2.2 (PCIe-applicable events)</strong><br>Printed pages 183–191 · PDF 209–217 · Figure 150–160</li>
<li id="ref-getlog"><strong>Base 2.4 · §5.2.13–5.2.13.1.1</strong><br>Printed pages 212–218 · PDF 238–244 · Figure 203–211</li>
<li id="ref-error"><strong>Base 2.4 · §5.2.13.1.2</strong><br>Printed pages 218–220 · PDF 244–246 · Figure 212</li>
<li id="ref-smart"><strong>Base 2.4 · §5.2.13.1.3</strong><br>Printed pages 220–225 · PDF 246–251 · Figure 213–214</li>
<li id="ref-dstlog"><strong>Base 2.4 · §5.2.13.1.7</strong><br>Printed pages 229–232 · PDF 255–258 · Figure 218–219</li>
<li id="ref-pel"><strong>Base 2.4 · §5.2.13.1.14 (header, reset, hardware, Set Feature events)</strong><br>Printed pages 244–256, 258, 262–264 · PDF 270–282, 284, 288–290 · Figure 232–244, 246, 252–253</li>
<li id="ref-idctrl"><strong>Base 2.4 · §5.2.14.2.1</strong><br>Printed pages 340–387 · PDF 366–413 · Figure 338–341</li>
<li id="ref-aec"><strong>Base 2.4 · §5.2.30.1.6</strong><br>Printed pages 466–468 · PDF 492–494 · Figure 474</li>
</ul><h3>When you need a field guide</h3><p>Existing figure explanations have canonical locations; use these links instead of duplicating the same guide.</p><ul>
<li><a href="/nvme/figure-reference/command/en/#figure-b101">Base 2.4 Figure 101 · Completion Queue Entry: Status Field</a></li>
<li><a href="/nvme/figure-reference/command/en/#figure-b104">Base 2.4 Figure 104 · Status Code – Command Specific Status Values</a></li>
<li><a href="/nvme/figure-reference/identify/en/#figure-b338">Base 2.4 Figure 338 · Identify – Identify Controller Data Structure, I/O Command Set Independent</a></li>
<li><a href="/nvme/figure-reference/command/en/#figure-b97">Base 2.4 Figure 97 · Common Completion Queue Entry Layout – Admin and All I/O Command Sets</a></li>
</ul><details><summary>Original documents used</summary><ul class="qr-sources">
<li>NVM Express Base Specification · Revision 2.4 · 2026-07-31<br><code>NVM-Express-Base-Specification-Revision-2.4-Ratified-2026.07.31.pdf</code></li>
<li>NVM Express NVM Command Set Specification · Revision 1.3 · 2026-07-31<br><code>NVM-Express-NVM-Command-Set-Specification-Revision-1.3-Ratified-2026.07.31.pdf</code></li>
<li>NVM Express NVMe over PCIe Transport Specification · Revision 1.4 · 2026-07-31<br><code>NVM-Express-NVMe-over-PCIe-Transport-Specification-Revision-1.4-Ratified-2026.07.31.pdf</code></li>
</ul></details></section>
</main>
<nav class="qr-top" aria-label="Bank and editions"><a href="#content">Skip to content</a><a href="/nvme/question-bank/en/">Question index</a><a href="/nvme/question-bank/asynchronous-events/zh-tw/">繁體中文</a><a href="/DOCS/nvme-question-bank/asynchronous-events.html">Chinese tutorial HTML</a></nav>
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
