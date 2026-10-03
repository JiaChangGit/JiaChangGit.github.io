---
layout: post
title: "NVMe Self-Study Bank: Persistent Event Log and Timestamp"
date: 2026-10-02 00:00:00 +0800
categories: [nvme]
permalink: /nvme/question-bank/persistent-events/en/
lang: en
nvme_quickref: true
nvme_qa: true
---

<div class="nvme-quickref nvme-qa">
<nav class="qr-top" aria-label="Bank and editions"><a href="#content">Skip to content</a><a href="/nvme/question-bank/en/">Question index</a><a href="/nvme/question-bank/persistent-events/zh-tw/">繁體中文</a><a href="/DOCS/nvme-question-bank/persistent-events.html">Chinese tutorial HTML</a></nav>
<main id="content"><p class="qr-eyebrow">BASE 2.4 / NVM 1.3 / PCIe 1.4 · Q1–320</p>
<header><p class="qa-range">Q205–Q216</p><h1>Persistent Event Log and Timestamp</h1><p class="qr-intro">Retrieve a consistent PEL before interpreting variable lengths, event types and changing time bases.</p><p>Practice first, then reveal 17 answer items per question. All numerical examples are hypothetical. Status is written SCT/SC; h indicates hexadecimal.</p></header>
<aside class="qa-glossary"><h2>Terms used in this volume</h2><dl><dt>Controller / namespace</dt><dd>A controller receives commands and manages access. A namespace is a logical storage space that commands can address. An NVM subsystem contains controllers and nonvolatile storage resources.</dd><dt>SQ / CQ / SQE / CQE</dt><dd>Submission and Completion Queues carry command entries (SQEs) and completion entries (CQEs). QID identifies a queue, CID distinguishes outstanding commands in one SQ, and NSID identifies a namespace.</dd><dt>Register / Identify / Feature / Log</dt><dd>A register exposes control or state. Identify queries capabilities and attributes; features query or configure operation; log pages report specific state or records. FID, LID, CNS and CSI select features, logs, Identify structures and command sets.</dd><dt>index / offset / zero-based</dt><dd>An index selects an entry, usually starting at 0; an offset measures distance from an origin in specified units. A zero-based count encodes count−1, but not every zero-valued field is a count. A Dword is 4 bytes; a byte is 8 bits.</dd><dt>Scope / reset / retention</dt><dd>Scope names the affected objects; retention means preserving state. Controller Reset (clearing CC.EN) is one form of Controller Level Reset, or CLR. Different CLR triggers can retain different registers.</dd></dl></aside>
<section id="overview" class="qa-overview"><h2>Reporting context differs from persistent history</h2><p class="qa-takeaway">Persistent events do not guarantee a reusable context after reset.</p>
<div class="qr-table" tabindex="0" role="region" aria-label="Horizontally scrollable comparison table"><table><thead><tr><th scope="col">Retrieval step</th><th scope="col">Fields</th><th scope="col">Constraint</th></tr></thead><tbody><tr><td>Establish view</td><td>Action and context status</td><td>ACT3 RCE0 can mean newly established</td></tr><tr><td>Traverse</td><td>Header length, total length, event count</td><td>Events have variable lengths</td></tr><tr><td>Parse event</td><td>Header, event and vendor lengths</td><td>Total=EHL+3+EL</td></tr><tr><td>Interpret time</td><td>Clock attributes and change event</td><td>Timestamps need not be monotonic</td></tr></tbody></table></div>
<p><strong>Worked interpretation: </strong>With EHL21/EL20/VSIL4, total length is 44 bytes and event data 16 bytes; adding VSIL again misaligns the next event.</p>
<p class="qa-citations">Sources: <a href="#ref-pelcontext">Base 2.4 §5.2.13.1.14–5.2.13.1.14.2.5 (exclude PCIe link/packet decoding)</a> · <a href="#ref-nvmpel">NVM Command Set 1.3 §4.1.4.4</a> · <a href="#ref-timestamp">Base 2.4 §5.2.30.1.8</a></p>
</section>
<div class="qa-controls" hidden><label>Search this page <input type="search" id="qa-search" placeholder="Question number, field or keyword"></label><button type="button" data-expand="true">Expand all answers</button><button type="button" data-expand="false">Collapse all answers</button><output id="qa-count" aria-live="polite"></output></div>
<section id="question-index"><h2>Questions in this volume</h2><ol class="qa-index">
<li><a href="#q-205">Q205 · How is PEL and individual event support established?</a></li>
<li><a href="#q-206">Q206 · How is a PEL context established, read and released?</a></li>
<li><a href="#q-207">Q207 · What happens for absent or duplicate PEL contexts?</a></li>
<li><a href="#q-208">Q208 · How are key PEL event classes recorded?</a></li>
<li><a href="#q-209">Q209 · Which persistent events describe namespace, format and sanitize operations?</a></li>
<li><a href="#q-210">Q210 · How are events removed when PEL reaches its limits?</a></li>
<li><a href="#q-211">Q211 · Does a new PEL event require an asynchronous notification?</a></li>
<li><a href="#q-212">Q212 · What persists in PEL across resets and power cycles?</a></li>
<li><a href="#q-213">Q213 · How are PEL headers, lengths and ordering validated?</a></li>
<li><a href="#q-214">Q214 · How is Timestamp set and verified?</a></li>
<li><a href="#q-215">Q215 · How do Timestamp counting, wrap-around, Origin and SYNC work?</a></li>
<li><a href="#q-216">Q216 · How are Timestamp changes and reset outcomes interpreted?</a></li>
</ol></section>
<article class="qa-question" id="q-205" data-question="205"><h2><a class="qa-qid" href="#q-205">Q205</a> How is PEL and individual event support established?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-205-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-205-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Establish log support and then event support; PEL support does not require every optional event.</p>
</li>
<li id="q-205-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>PEL is subsystem-global despite controller identifiers in its entries.</p>
</li>
<li id="q-205-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Check LPA, PELS and LID 0Dh support, then the header’s Supported Events Bitmap.</p>
</li>
<li id="q-205-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>PELS uses 64 KiB units. ECRH supports ACT=3 and GNUM and is required for PEL implementations conforming to Base 2.0 or later.</p>
</li>
<li id="q-205-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Read the header and map mandatory/conditional events before testing.</p>
</li>
<li id="q-205-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Obtain an event support matrix rather than one yes/no log result.</p>
</li>
<li id="q-205-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Unsupported logs follow Invalid Log Page handling; an unadvertised optional event does not invalidate the log.</p>
</li>
<li id="q-205-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-205-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Base 2.4 does not define a generic PEL Changed AER for every appended entry. <a class="qa-rule-link" href="#common-pel_query-9">Full rule in this volume</a></p>
</li>
<li id="q-205-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>A context fixes the reported event set. <a class="qa-rule-link" href="#common-pel_query-10">Full rule in this volume</a></p>
</li>
<li id="q-205-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>PEL retrieval is not itself a PEL read event. <a class="qa-rule-link" href="#common-pel_query-11">Full rule in this volume</a></p>
</li>
<li id="q-205-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Event content survives CLR; the reporting context need not. <a class="qa-rule-link" href="#common-pel_query-12">Full rule in this volume</a></p>
</li>
<li id="q-205-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Subsystem reset preserves events and may add the supported Power-on or Reset event at completion; establish a fresh consistent reporting context. <a class="qa-rule-link" href="#common-pel_query-13">Full rule in this volume</a></p>
</li>
<li id="q-205-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Events persist across power cycles, with minimal power-failure loss recommended. <a class="qa-rule-link" href="#common-pel_query-14">Full rule in this volume</a></p>
</li>
<li id="q-205-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>PEL is subsystem-global. <a class="qa-rule-link" href="#common-pel_query-15">Full rule in this volume</a></p>
</li>
<li id="q-205-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Figure 233 reserves bits 221:16 while Figure 236 defines ET10h. Preserve this source inconsistency rather than inventing a reconciled bitmap.</p>
</li>
<li id="q-205-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First classify the expected event’s support requirement.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-getlog">Base 2.4 §5.2.13–5.2.13.1.1</a> · <a href="#ref-pelcontext">Base 2.4 §5.2.13.1.14–5.2.13.1.14.2.5 (exclude PCIe link/packet decoding)</a> · <a href="#ref-timestamp">Base 2.4 §5.2.30.1.8</a> · <a href="#ref-nvmpel">NVM Command Set 1.3 §4.1.4.4</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-206" data-question="206"><h2><a class="qa-qid" href="#q-206">Q206</a> How is a PEL context established, read and released?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-206-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-206-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>A context stabilizes an event set while a large log is read in segments.</p>
</li>
<li id="q-206-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>It is a reporting view, not suspension of event recording.</p>
</li>
<li id="q-206-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Check LID 0Dh, ECRH and TLL/LHL/GNUM/RCI.</p>
</li>
<li id="q-206-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>ACT1 establishes/reads, ACT0 reads, ACT2 releases and ACT3 establishes/reuses with a fixed 512-byte header.</p>
</li>
<li id="q-206-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Read the header with ACT3, retain GNUM, fetch segments with ACT0/LPO, recheck GNUM and release with ACT2.</p>
</li>
<li id="q-206-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Segments share a context; newly logged events appear in a later context. Allocate at least 512 bytes for ACT3.</p>
</li>
<li id="q-206-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>ACT0 without a context or ACT1 with one requires Command Sequence Error; ACT2 without one is not an error.</p>
</li>
<li id="q-206-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-206-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Base 2.4 does not define a generic PEL Changed AER for every appended entry. <a class="qa-rule-link" href="#common-pel_query-9">Full rule in this volume</a></p>
</li>
<li id="q-206-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>A context fixes the reported event set. <a class="qa-rule-link" href="#common-pel_query-10">Full rule in this volume</a></p>
</li>
<li id="q-206-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>PEL retrieval is not itself a PEL read event. <a class="qa-rule-link" href="#common-pel_query-11">Full rule in this volume</a></p>
</li>
<li id="q-206-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Event content survives CLR; the reporting context need not. <a class="qa-rule-link" href="#common-pel_query-12">Full rule in this volume</a></p>
</li>
<li id="q-206-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Subsystem reset preserves events and may add the supported Power-on or Reset event at completion; establish a fresh consistent reporting context. <a class="qa-rule-link" href="#common-pel_query-13">Full rule in this volume</a></p>
</li>
<li id="q-206-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Events persist across power cycles, with minimal power-failure loss recommended. <a class="qa-rule-link" href="#common-pel_query-14">Full rule in this volume</a></p>
</li>
<li id="q-206-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>PEL is subsystem-global. <a class="qa-rule-link" href="#common-pel_query-15">Full rule in this volume</a></p>
</li>
<li id="q-206-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>A changed GNUM means the assembled data may be invalid and should be reread.</p>
</li>
<li id="q-206-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First compare ACT, offsets and generation across segments.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-getlog">Base 2.4 §5.2.13–5.2.13.1.1</a> · <a href="#ref-pelcontext">Base 2.4 §5.2.13.1.14–5.2.13.1.14.2.5 (exclude PCIe link/packet decoding)</a> · <a href="#ref-timestamp">Base 2.4 §5.2.30.1.8</a> · <a href="#ref-nvmpel">NVM Command Set 1.3 §4.1.4.4</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-207" data-question="207"><h2><a class="qa-qid" href="#q-207">Q207</a> What happens for absent or duplicate PEL contexts?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-207-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-207-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Replace the presumed context-count limit with ACT/existing-context rules; this interface does not create an arbitrary list of host-selected context IDs.</p>
</li>
<li id="q-207-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Evaluate context existence when the command is processed.</p>
</li>
<li id="q-207-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Use ACT3 RCE and reporting-port information to inspect an existing context.</p>
</li>
<li id="q-207-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>RCE=0 means none existed before processing; ACT3 still successfully establishes one.</p>
</li>
<li id="q-207-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Read with ACT0; coordinate readers before release/re-establishment for a fresh set.</p>
</li>
<li id="q-207-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>ACT3 returns a header in either case, with RCE distinguishing prior state; repeated ACT2 release is allowed.</p>
</li>
<li id="q-207-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Duplicate ACT1 and absent-context ACT0 require Command Sequence Error, not an invented resource-count status.</p>
</li>
<li id="q-207-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-207-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Base 2.4 does not define a generic PEL Changed AER for every appended entry. <a class="qa-rule-link" href="#common-pel_query-9">Full rule in this volume</a></p>
</li>
<li id="q-207-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>A context fixes the reported event set. <a class="qa-rule-link" href="#common-pel_query-10">Full rule in this volume</a></p>
</li>
<li id="q-207-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>PEL retrieval is not itself a PEL read event. <a class="qa-rule-link" href="#common-pel_query-11">Full rule in this volume</a></p>
</li>
<li id="q-207-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Event content survives CLR; the reporting context need not. <a class="qa-rule-link" href="#common-pel_query-12">Full rule in this volume</a></p>
</li>
<li id="q-207-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Subsystem reset preserves events and may add the supported Power-on or Reset event at completion; establish a fresh consistent reporting context. <a class="qa-rule-link" href="#common-pel_query-13">Full rule in this volume</a></p>
</li>
<li id="q-207-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Events persist across power cycles, with minimal power-failure loss recommended. <a class="qa-rule-link" href="#common-pel_query-14">Full rule in this volume</a></p>
</li>
<li id="q-207-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>PEL is subsystem-global. <a class="qa-rule-link" href="#common-pel_query-15">Full rule in this volume</a></p>
</li>
<li id="q-207-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Successful CQE and RCE describing prior state are compatible.</p>
</li>
<li id="q-207-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First check whether RCE was mistaken for a post-command existence flag.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-pelcontext">Base 2.4 §5.2.13.1.14–5.2.13.1.14.2.5 (exclude PCIe link/packet decoding)</a> · <a href="#ref-timestamp">Base 2.4 §5.2.30.1.8</a> · <a href="#ref-nvmpel">NVM Command Set 1.3 §4.1.4.4</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-208" data-question="208"><h2><a class="qa-qid" href="#q-208">Q208</a> How are key PEL event classes recorded?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-208-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-208-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Each event has its own trigger and payload; decode type before interpreting fields.</p>
</li>
<li id="q-208-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>CNTLID identifies the recorder; shared events should be recorded once and may describe several controllers.</p>
</li>
<li id="q-208-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Establish event support; SMART snapshots are required for PCIe implementations supporting PEL.</p>
</li>
<li id="q-208-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>ET01 carries SMART; 02 commit action/slot/status/requested revision; 03 previous time; 04 reset descriptors; 05 code-selected hardware data.</p>
</li>
<li id="q-208-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Decode ET/ETR/length first. SMART snapshots occur at least once per 24 power-on hours; reset events are logged on completion.</p>
</li>
<li id="q-208-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Firmware NFR is the requested revision, not proof of activation; reset FA supplies activation outcome.</p>
</li>
<li id="q-208-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Supported qualifying hardware errors are logged subject to suppression; an Invalid Field command error need not be a hardware event.</p>
</li>
<li id="q-208-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-208-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Base 2.4 does not define a generic PEL Changed AER for every appended entry. <a class="qa-rule-link" href="#common-pel_query-9">Full rule in this volume</a></p>
</li>
<li id="q-208-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>A context fixes the reported event set. <a class="qa-rule-link" href="#common-pel_query-10">Full rule in this volume</a></p>
</li>
<li id="q-208-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>PEL retrieval is not itself a PEL read event. <a class="qa-rule-link" href="#common-pel_query-11">Full rule in this volume</a></p>
</li>
<li id="q-208-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Event content survives CLR; the reporting context need not. <a class="qa-rule-link" href="#common-pel_query-12">Full rule in this volume</a></p>
</li>
<li id="q-208-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Subsystem reset preserves events and may add the supported Power-on or Reset event at completion; establish a fresh consistent reporting context. <a class="qa-rule-link" href="#common-pel_query-13">Full rule in this volume</a></p>
</li>
<li id="q-208-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Events persist across power cycles, with minimal power-failure loss recommended. <a class="qa-rule-link" href="#common-pel_query-14">Full rule in this volume</a></p>
</li>
<li id="q-208-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>PEL is subsystem-global. <a class="qa-rule-link" href="#common-pel_query-15">Full rule in this volume</a></p>
</li>
<li id="q-208-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Correlate CQEs, FR, SMART and payload rather than event names alone.</p>
</li>
<li id="q-208-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First check event revision and distinguish requested action from completed effect.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-fwpel">Base 2.4 §5.2.13.1.14.2.2, 5.2.13.1.14.2.4</a> · <a href="#ref-smart">Base 2.4 §5.2.13.1.3</a> · <a href="#ref-pelcontext">Base 2.4 §5.2.13.1.14–5.2.13.1.14.2.5 (exclude PCIe link/packet decoding)</a> · <a href="#ref-timestamp">Base 2.4 §5.2.30.1.8</a> · <a href="#ref-nvmpel">NVM Command Set 1.3 §4.1.4.4</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-209" data-question="209"><h2><a class="qa-qid" href="#q-209">Q209</a> Which persistent events describe namespace, format and sanitize operations?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-209-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-209-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Long management operations need distinct start and completion evidence.</p>
</li>
<li id="q-209-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Identify NSID and command-specific namespace or wider scope.</p>
</li>
<li id="q-209-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Check command capability and conditionally mandatory PEL event support.</p>
</li>
<li id="q-209-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>ET06 records namespace create/delete; 07/08 format start/completion; 09/0A sanitize start/completion. NVM defines FLBAS/DPS interpretation.</p>
</li>
<li id="q-209-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Pair target/action and start/end data; Attach/Detach are not ET06 create/delete operations.</p>
</li>
<li id="q-209-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Interpret Format with FNVMS/INFO; entering Sanitize Media Verification is not final completion.</p>
</li>
<li id="q-209-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>If reset prevented a Format CQE, absent/zero status evidence is not proof of success.</p>
</li>
<li id="q-209-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-209-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Base 2.4 does not define a generic PEL Changed AER for every appended entry. <a class="qa-rule-link" href="#common-pel_query-9">Full rule in this volume</a></p>
</li>
<li id="q-209-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>A context fixes the reported event set. <a class="qa-rule-link" href="#common-pel_query-10">Full rule in this volume</a></p>
</li>
<li id="q-209-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>PEL retrieval is not itself a PEL read event. <a class="qa-rule-link" href="#common-pel_query-11">Full rule in this volume</a></p>
</li>
<li id="q-209-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Event content survives CLR; the reporting context need not. <a class="qa-rule-link" href="#common-pel_query-12">Full rule in this volume</a></p>
</li>
<li id="q-209-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Subsystem reset preserves events and may add the supported Power-on or Reset event at completion; establish a fresh consistent reporting context. <a class="qa-rule-link" href="#common-pel_query-13">Full rule in this volume</a></p>
</li>
<li id="q-209-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Events persist across power cycles, with minimal power-failure loss recommended. <a class="qa-rule-link" href="#common-pel_query-14">Full rule in this volume</a></p>
</li>
<li id="q-209-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>PEL is subsystem-global. <a class="qa-rule-link" href="#common-pel_query-15">Full rule in this volume</a></p>
</li>
<li id="q-209-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>FLBAS/DPS are reserved for delete-all; single deletion describes the former format, not an object still available to Identify.</p>
</li>
<li id="q-209-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First distinguish start from completion and validate outcome fields.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-nspelevent">Base 2.4 §5.2.13.1.14.2.6</a> · <a href="#ref-formatpel">Base 2.4 §5.2.13.1.14.2.7–5.2.13.1.14.2.8</a> · <a href="#ref-sanitizepel">Base 2.4 §5.2.13.1.14.2.9–5.2.13.1.14.2.10</a> · <a href="#ref-pelcontext">Base 2.4 §5.2.13.1.14–5.2.13.1.14.2.5 (exclude PCIe link/packet decoding)</a> · <a href="#ref-timestamp">Base 2.4 §5.2.30.1.8</a> · <a href="#ref-nvmpel">NVM Command Set 1.3 §4.1.4.4</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-210" data-question="210"><h2><a class="qa-qid" href="#q-210">Q210</a> How are events removed when PEL reaches its limits?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-210-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-210-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>PEL is bounded; not every event is retained forever.</p>
</li>
<li id="q-210-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Limits may be total bytes, event count or per-category capacity.</p>
</li>
<li id="q-210-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Check PELS, TLL/TNEV and vendor policy; current count is not lifetime occurrence count.</p>
</li>
<li id="q-210-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>Eviction is vendor-specific and may retain older important events rather than strict FIFO order.</p>
</li>
<li id="q-210-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Compare complete contexts and account for eviction, frequency suppression and Sanitize.</p>
</li>
<li id="q-210-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>A valid retained set need not have a monotonically growing count.</p>
</li>
<li id="q-210-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Lifetime-sized capacity is a should, not a prohibition on all eviction.</p>
</li>
<li id="q-210-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-210-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Base 2.4 does not define a generic PEL Changed AER for every appended entry. <a class="qa-rule-link" href="#common-pel_query-9">Full rule in this volume</a></p>
</li>
<li id="q-210-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>A context fixes the reported event set. <a class="qa-rule-link" href="#common-pel_query-10">Full rule in this volume</a></p>
</li>
<li id="q-210-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>PEL retrieval is not itself a PEL read event. <a class="qa-rule-link" href="#common-pel_query-11">Full rule in this volume</a></p>
</li>
<li id="q-210-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Event content survives CLR; the reporting context need not. <a class="qa-rule-link" href="#common-pel_query-12">Full rule in this volume</a></p>
</li>
<li id="q-210-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Subsystem reset preserves events and may add the supported Power-on or Reset event at completion; establish a fresh consistent reporting context. <a class="qa-rule-link" href="#common-pel_query-13">Full rule in this volume</a></p>
</li>
<li id="q-210-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Events persist across power cycles, with minimal power-failure loss recommended. <a class="qa-rule-link" href="#common-pel_query-14">Full rule in this volume</a></p>
</li>
<li id="q-210-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>PEL is subsystem-global. <a class="qa-rule-link" href="#common-pel_query-15">Full rule in this volume</a></p>
</li>
<li id="q-210-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>GNUM tracks changed content at context establishment, not total event occurrences.</p>
</li>
<li id="q-210-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First consider all limits, not only whether TLL equals PELS.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-pelcontext">Base 2.4 §5.2.13.1.14–5.2.13.1.14.2.5 (exclude PCIe link/packet decoding)</a> · <a href="#ref-timestamp">Base 2.4 §5.2.30.1.8</a> · <a href="#ref-nvmpel">NVM Command Set 1.3 §4.1.4.4</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-211" data-question="211"><h2><a class="qa-qid" href="#q-211">Q211</a> Does a new PEL event require an asynchronous notification?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-211-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-211-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Correct the assumption that persistent recording always implies immediate notification.</p>
</li>
<li id="q-211-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>PEL provides persistent history while AER reports eligible asynchronous conditions.</p>
</li>
<li id="q-211-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Check PEL support separately from AER/AEC; the event bitmap is not an AER mask.</p>
</li>
<li id="q-211-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>A critical warning may qualify for both mechanisms; Timestamp Change does not create a generic PEL Changed notification.</p>
</li>
<li id="q-211-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Identify the underlying event and then its separate AER type, enablement, masking and request requirements.</p>
</li>
<li id="q-211-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>PEL-only or dual reporting may be correct depending on the underlying event.</p>
</li>
<li id="q-211-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Do not invent a notification or command error where none is defined.</p>
</li>
<li id="q-211-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-211-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Base 2.4 does not define a generic PEL Changed AER for every appended entry. <a class="qa-rule-link" href="#common-pel_query-9">Full rule in this volume</a></p>
</li>
<li id="q-211-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>A context fixes the reported event set. <a class="qa-rule-link" href="#common-pel_query-10">Full rule in this volume</a></p>
</li>
<li id="q-211-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>PEL retrieval is not itself a PEL read event. <a class="qa-rule-link" href="#common-pel_query-11">Full rule in this volume</a></p>
</li>
<li id="q-211-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Event content survives CLR; the reporting context need not. <a class="qa-rule-link" href="#common-pel_query-12">Full rule in this volume</a></p>
</li>
<li id="q-211-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Subsystem reset preserves events and may add the supported Power-on or Reset event at completion; establish a fresh consistent reporting context. <a class="qa-rule-link" href="#common-pel_query-13">Full rule in this volume</a></p>
</li>
<li id="q-211-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Events persist across power cycles, with minimal power-failure loss recommended. <a class="qa-rule-link" href="#common-pel_query-14">Full rule in this volume</a></p>
</li>
<li id="q-211-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>PEL is subsystem-global. <a class="qa-rule-link" href="#common-pel_query-15">Full rule in this volume</a></p>
</li>
<li id="q-211-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Record separate expectations for logging and notification.</p>
</li>
<li id="q-211-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First check whether the test assumes a nonexistent generic PEL Changed AER.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-aerfull">Base 2.4 §5.2.2 (PCIe-applicable events)</a> · <a href="#ref-aec">Base 2.4 §5.2.30.1.6</a> · <a href="#ref-pelcontext">Base 2.4 §5.2.13.1.14–5.2.13.1.14.2.5 (exclude PCIe link/packet decoding)</a> · <a href="#ref-timestamp">Base 2.4 §5.2.30.1.8</a> · <a href="#ref-nvmpel">NVM Command Set 1.3 §4.1.4.4</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-212" data-question="212"><h2><a class="qa-qid" href="#q-212">Q212</a> What persists in PEL across resets and power cycles?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-212-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-212-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Persistent events and temporary reporting contexts have different lifetimes.</p>
</li>
<li id="q-212-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Persistence protects subsystem history; a context serves one consistent retrieval.</p>
</li>
<li id="q-212-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Save a complete pre-reset view and establish a new context afterward.</p>
</li>
<li id="q-212-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>Header time, generation, count and offsets may change, including from a new reset event.</p>
</li>
<li id="q-212-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Correlate event identity/content rather than demanding fixed offsets.</p>
</li>
<li id="q-212-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Persisted events remain subject to retention rules; an expired context requires a fresh read.</p>
</li>
<li id="q-212-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>A stale-context sequence error does not prove erased history; assess eviction, suppression and Sanitize separately.</p>
</li>
<li id="q-212-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-212-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Base 2.4 does not define a generic PEL Changed AER for every appended entry. <a class="qa-rule-link" href="#common-pel_query-9">Full rule in this volume</a></p>
</li>
<li id="q-212-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>A context fixes the reported event set. <a class="qa-rule-link" href="#common-pel_query-10">Full rule in this volume</a></p>
</li>
<li id="q-212-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>PEL retrieval is not itself a PEL read event. <a class="qa-rule-link" href="#common-pel_query-11">Full rule in this volume</a></p>
</li>
<li id="q-212-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Event content survives CLR; the reporting context need not. <a class="qa-rule-link" href="#common-pel_query-12">Full rule in this volume</a></p>
</li>
<li id="q-212-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Subsystem reset preserves events and may add the supported Power-on or Reset event at completion; establish a fresh consistent reporting context. <a class="qa-rule-link" href="#common-pel_query-13">Full rule in this volume</a></p>
</li>
<li id="q-212-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Events persist across power cycles, with minimal power-failure loss recommended. <a class="qa-rule-link" href="#common-pel_query-14">Full rule in this volume</a></p>
</li>
<li id="q-212-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>PEL is subsystem-global. <a class="qa-rule-link" href="#common-pel_query-15">Full rule in this volume</a></p>
</li>
<li id="q-212-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Validate the complete fresh view rather than only the first entry.</p>
</li>
<li id="q-212-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First distinguish missing history from missing context.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-pelcontext">Base 2.4 §5.2.13.1.14–5.2.13.1.14.2.5 (exclude PCIe link/packet decoding)</a> · <a href="#ref-timestamp">Base 2.4 §5.2.30.1.8</a> · <a href="#ref-nvmpel">NVM Command Set 1.3 §4.1.4.4</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-213" data-question="213"><h2><a class="qa-qid" href="#q-213">Q213</a> How are PEL headers, lengths and ordering validated?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-213-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-213-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>One length error can misalign every subsequent variable-length event.</p>
</li>
<li id="q-213-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Distinguish the whole log from individual events. Log Revision (LREV) identifies the overall log format, while each Event Type Revision (ETR) identifies the format of that event type. Validate both rather than treating them as one version.</p>
</li>
<li id="q-213-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Confirm PEL support through Identify Controller.LPA, then read the log header. Total Log Length (TLL) counts log bytes and Total Number of Events (TNEV) counts entries. Log Header Length (LHL) locates the first event, while Generation Number (GNUM) helps detect updates. Establish these bounds before parsing individual events.</p>
</li>
<li id="q-213-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>LHL starts counting at log byte 20, so the full log header occupies LHL+20 bytes. Event Header Length (EHL) similarly excludes the first three event bytes. Event Length (EL) covers data after the event header and already includes the vendor information counted by Vendor Specific Information Length (VSIL). Total event length is EHL+3+EL; event data excluding vendor information is EL−VSIL.</p>
</li>
<li id="q-213-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Advance by validated lengths. With hypothetical EHL=21, EL=20 and VSIL=4, the event is 44 bytes with 16 bytes of event data.</p>
</li>
<li id="q-213-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Walk the reported events within bounds; individual events are not guaranteed four-byte aligned.</p>
</li>
<li id="q-213-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>VSIL&gt;EL or an event beyond TLL is inconsistent; transfer alignment does not make events fixed-size.</p>
</li>
<li id="q-213-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-213-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Base 2.4 does not define a generic PEL Changed AER for every appended entry. <a class="qa-rule-link" href="#common-pel_query-9">Full rule in this volume</a></p>
</li>
<li id="q-213-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>A context fixes the reported event set. <a class="qa-rule-link" href="#common-pel_query-10">Full rule in this volume</a></p>
</li>
<li id="q-213-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>PEL retrieval is not itself a PEL read event. <a class="qa-rule-link" href="#common-pel_query-11">Full rule in this volume</a></p>
</li>
<li id="q-213-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Event content survives CLR; the reporting context need not. <a class="qa-rule-link" href="#common-pel_query-12">Full rule in this volume</a></p>
</li>
<li id="q-213-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Subsystem reset preserves events and may add the supported Power-on or Reset event at completion; establish a fresh consistent reporting context. <a class="qa-rule-link" href="#common-pel_query-13">Full rule in this volume</a></p>
</li>
<li id="q-213-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Events persist across power cycles, with minimal power-failure loss recommended. <a class="qa-rule-link" href="#common-pel_query-14">Full rule in this volume</a></p>
</li>
<li id="q-213-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>PEL is subsystem-global. <a class="qa-rule-link" href="#common-pel_query-15">Full rule in this volume</a></p>
</li>
<li id="q-213-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Newer-first ordering is recommended with vendor-defined occurrence ordering; timestamp changes prevent simplistic numeric sorting.</p>
</li>
<li id="q-213-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First check double-counted VSIL and the EHL+3 rule.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-pelcontext">Base 2.4 §5.2.13.1.14–5.2.13.1.14.2.5 (exclude PCIe link/packet decoding)</a> · <a href="#ref-timestamp">Base 2.4 §5.2.30.1.8</a> · <a href="#ref-nvmpel">NVM Command Set 1.3 §4.1.4.4</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-214" data-question="214"><h2><a class="qa-qid" href="#q-214">Q214</a> How is Timestamp set and verified?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-214-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-214-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Timestamp supplies a host time basis for correlation, not a security clock or automatically shared clock.</p>
</li>
<li id="q-214-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>It targets a controller; cross-controller correlation needs offsets and reset evidence.</p>
</li>
<li id="q-214-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Check ONCS Timestamp support and FID 0Eh saveability.</p>
</li>
<li id="q-214-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>Set uses an eight-byte buffer with a 48-bit UTC-epoch millisecond value; Get adds Origin and SYNC.</p>
</li>
<li id="q-214-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Record host time, await successful Set, then Get Current with elapsed time accounted for.</p>
</li>
<li id="q-214-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Origin=001b marks Set Features initialization; value includes counted elapsed time.</p>
</li>
<li id="q-214-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Unsupported/invalid/save failures follow feature status rules; a failed Set does not establish an update.</p>
</li>
<li id="q-214-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-214-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Set Timestamp defines no generic success AER or PEL Changed notice. <a class="qa-rule-link" href="#common-timestamp_op-9">Full rule in this volume</a></p>
</li>
<li id="q-214-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Get Current reflects a successful new time basis; error records follow command-error rules. <a class="qa-rule-link" href="#common-timestamp_op-10">Full rule in this volume</a></p>
</li>
<li id="q-214-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>Timestamp uses its dedicated Change event and shall not be recorded as a generic Set Feature event. <a class="qa-rule-link" href="#common-timestamp_op-11">Full rule in this volume</a></p>
</li>
<li id="q-214-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>A CLR method that maintains the running timestamp shall preserve Origin; otherwise apply its initialization/saved-value rules. <a class="qa-rule-link" href="#common-timestamp_op-12">Full rule in this volume</a></p>
</li>
<li id="q-214-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Check continued counting and Origin per affected controller, not assumed equality across the subsystem. <a class="qa-rule-link" href="#common-timestamp_op-13">Full rule in this volume</a></p>
</li>
<li id="q-214-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Restoring a saved value can move time backward; uninterrupted counting through power loss is not guaranteed. <a class="qa-rule-link" href="#common-timestamp_op-14">Full rule in this volume</a></p>
</li>
<li id="q-214-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Setting one controller does not synchronize every controller. <a class="qa-rule-link" href="#common-timestamp_op-15">Full rule in this volume</a></p>
</li>
<li id="q-214-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Compare setting, Origin, SYNC and read timing together.</p>
</li>
<li id="q-214-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First check milliseconds versus seconds and the 48-bit encoding.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-getfeat">Base 2.4 §5.2.12</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-pelcontext">Base 2.4 §5.2.13.1.14–5.2.13.1.14.2.5 (exclude PCIe link/packet decoding)</a> · <a href="#ref-timestamp">Base 2.4 §5.2.30.1.8</a> · <a href="#ref-nvmpel">NVM Command Set 1.3 §4.1.4.4</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-215" data-question="215"><h2><a class="qa-qid" href="#q-215">Q215</a> How do Timestamp counting, wrap-around, Origin and SYNC work?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-215-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-215-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>The same number can represent host-set epoch time or time since reset; interpret attributes first.</p>
</li>
<li id="q-215-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>The 48-bit value belongs to that controller’s time basis.</p>
</li>
<li id="q-215-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Read Current Timestamp/TSTMPS and historical changes from PEL.</p>
</li>
<li id="q-215-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>Origin 000 means reset initialization and 001 host initialization. SYNC0 means continuous millisecond counting; SYNC1 permits omitted intervals.</p>
</li>
<li id="q-215-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Establish Origin, then elapsed time; overflow should be reduced modulo 2^48.</p>
</li>
<li id="q-215-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Modular differences work within the same basis; SYNC1 prevents demanding wall-clock equality.</p>
</li>
<li id="q-215-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>A smaller value may reflect wrap, reset, saved restoration or a new Set rather than corruption.</p>
</li>
<li id="q-215-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-215-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Set Timestamp defines no generic success AER or PEL Changed notice. <a class="qa-rule-link" href="#common-timestamp_op-9">Full rule in this volume</a></p>
</li>
<li id="q-215-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Get Current reflects a successful new time basis; error records follow command-error rules. <a class="qa-rule-link" href="#common-timestamp_op-10">Full rule in this volume</a></p>
</li>
<li id="q-215-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>Timestamp uses its dedicated Change event and shall not be recorded as a generic Set Feature event. <a class="qa-rule-link" href="#common-timestamp_op-11">Full rule in this volume</a></p>
</li>
<li id="q-215-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>A CLR method that maintains the running timestamp shall preserve Origin; otherwise apply its initialization/saved-value rules. <a class="qa-rule-link" href="#common-timestamp_op-12">Full rule in this volume</a></p>
</li>
<li id="q-215-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Check continued counting and Origin per affected controller, not assumed equality across the subsystem. <a class="qa-rule-link" href="#common-timestamp_op-13">Full rule in this volume</a></p>
</li>
<li id="q-215-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Restoring a saved value can move time backward; uninterrupted counting through power loss is not guaranteed. <a class="qa-rule-link" href="#common-timestamp_op-14">Full rule in this volume</a></p>
</li>
<li id="q-215-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Setting one controller does not synchronize every controller. <a class="qa-rule-link" href="#common-timestamp_op-15">Full rule in this volume</a></p>
</li>
<li id="q-215-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Use attributes and change/reset events before ordering timestamps.</p>
</li>
<li id="q-215-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First establish that both values share one time basis.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-pelcontext">Base 2.4 §5.2.13.1.14–5.2.13.1.14.2.5 (exclude PCIe link/packet decoding)</a> · <a href="#ref-timestamp">Base 2.4 §5.2.30.1.8</a> · <a href="#ref-nvmpel">NVM Command Set 1.3 §4.1.4.4</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-216" data-question="216"><h2><a class="qa-qid" href="#q-216">Q216</a> How are Timestamp changes and reset outcomes interpreted?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-216-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-216-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Timestamp Change connects discontinuous old and new time bases.</p>
</li>
<li id="q-216-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Interpret changes and resets per controller rather than assuming a subsystem clock.</p>
</li>
<li id="q-216-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Check support and preserve current attributes, saved value and reset source.</p>
</li>
<li id="q-216-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>ET03 header uses the new time; PTSTP records the prior value and MSR the time since CLR.</p>
</li>
<li id="q-216-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Relate old/new values, then use MSR and reset descriptors for correlation.</p>
</li>
<li id="q-216-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>A CLR retaining the running clock preserves Origin; otherwise account for initialization and any saved restoration.</p>
</li>
<li id="q-216-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>A backward clock adjustment does not prove event-order violation; Timestamp shall not use generic ET0Bh Set Feature logging.</p>
</li>
<li id="q-216-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-216-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Set Timestamp defines no generic success AER or PEL Changed notice. <a class="qa-rule-link" href="#common-timestamp_op-9">Full rule in this volume</a></p>
</li>
<li id="q-216-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Get Current reflects a successful new time basis; error records follow command-error rules. <a class="qa-rule-link" href="#common-timestamp_op-10">Full rule in this volume</a></p>
</li>
<li id="q-216-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>Timestamp uses its dedicated Change event and shall not be recorded as a generic Set Feature event. <a class="qa-rule-link" href="#common-timestamp_op-11">Full rule in this volume</a></p>
</li>
<li id="q-216-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>A CLR method that maintains the running timestamp shall preserve Origin; otherwise apply its initialization/saved-value rules. <a class="qa-rule-link" href="#common-timestamp_op-12">Full rule in this volume</a></p>
</li>
<li id="q-216-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Check continued counting and Origin per affected controller, not assumed equality across the subsystem. <a class="qa-rule-link" href="#common-timestamp_op-13">Full rule in this volume</a></p>
</li>
<li id="q-216-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Restoring a saved value can move time backward; uninterrupted counting through power loss is not guaranteed. <a class="qa-rule-link" href="#common-timestamp_op-14">Full rule in this volume</a></p>
</li>
<li id="q-216-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Setting one controller does not synchronize every controller. <a class="qa-rule-link" href="#common-timestamp_op-15">Full rule in this volume</a></p>
</li>
<li id="q-216-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Get and change/reset events should support a coherent explanation without assuming all timestamps monotonically increase.</p>
</li>
<li id="q-216-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First check clock updates or saved restoration before event ordering.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-pelcontext">Base 2.4 §5.2.13.1.14–5.2.13.1.14.2.5 (exclude PCIe link/packet decoding)</a> · <a href="#ref-timestamp">Base 2.4 §5.2.30.1.8</a> · <a href="#ref-nvmpel">NVM Command Set 1.3 §4.1.4.4</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<section id="common-rules" class="qa-common"><h2>Shared rules linked from the answers</h2><p>Each shared mechanism is explained in full once in this volume. Use browser Back to return to the question; explicit command or feature exceptions take precedence.</p>
<article id="common-command-8"><h3>Command completion, events and records · How are DNR and More set?</h3><p>For a CQE, DNR=1 means the identical command is expected to fail if resubmitted to any controller in this subsystem; DNR=0 means it may succeed. Do not assign DNR=1 solely from an error name unless that condition mandates it. More=1 identifies additional information for this command in the Error Information Log. DNR should be zero when SCT=SC=0.</p></article>
<article id="common-pel_query-9"><h3>Shared conditions for this topic · Is an asynchronous event generated?</h3><p>Base 2.4 does not define a generic PEL Changed AER for every appended entry. The underlying condition may have its own SMART, Sanitize or other notification rules.</p></article>
<article id="common-pel_query-10"><h3>Shared conditions for this topic · Are Error Information or other logs updated?</h3><p>A context fixes the reported event set. New events remain logged but shall not enter that context. Reading/releasing a context does not erase PEL; failed reads use ordinary error-log rules.</p></article>
<article id="common-pel_query-11"><h3>Shared conditions for this topic · Is it recorded in the Persistent Event Log?</h3><p>PEL retrieval is not itself a PEL read event. Supported underlying events follow their triggers, with permitted vendor-threshold suppression of frequent repeated events.</p></article>
<article id="common-pel_query-12"><h3>Shared conditions for this topic · What survives or continues after Controller Reset?</h3><p>Event content survives CLR; the reporting context need not. Re-establish it after recovery instead of joining partial data across contexts.</p></article>
<article id="common-pel_query-13"><h3>Shared conditions for this topic · What survives or continues after NVM Subsystem Reset?</h3><p>Subsystem reset preserves events and may add the supported Power-on or Reset event at completion; establish a fresh consistent reporting context.</p></article>
<article id="common-pel_query-14"><h3>Shared conditions for this topic · What survives or continues after a power cycle?</h3><p>Events persist across power cycles, with minimal power-failure loss recommended. Capacity eviction, repeated-event suppression and Sanitize-related privacy removal are distinct from ordinary power-cycle clearing.</p></article>
<article id="common-pel_query-15"><h3>Shared conditions for this topic · Are other controllers or namespaces affected?</h3><p>PEL is subsystem-global. CNTLID identifies the recording controller; multi-controller events should be logged once. Coordinate readers so one does not release a context still used by another.</p></article>
<article id="common-timestamp_op-9"><h3>Shared conditions for this topic · Is an asynchronous event generated?</h3><p>Set Timestamp defines no generic success AER or PEL Changed notice.</p></article>
<article id="common-timestamp_op-10"><h3>Shared conditions for this topic · Are Error Information or other logs updated?</h3><p>Get Current reflects a successful new time basis; error records follow command-error rules.</p></article>
<article id="common-timestamp_op-11"><h3>Shared conditions for this topic · Is it recorded in the Persistent Event Log?</h3><p>Timestamp uses its dedicated Change event and shall not be recorded as a generic Set Feature event.</p></article>
<article id="common-timestamp_op-12"><h3>Shared conditions for this topic · What survives or continues after Controller Reset?</h3><p>A CLR method that maintains the running timestamp shall preserve Origin; otherwise apply its initialization/saved-value rules.</p></article>
<article id="common-timestamp_op-13"><h3>Shared conditions for this topic · What survives or continues after NVM Subsystem Reset?</h3><p>Check continued counting and Origin per affected controller, not assumed equality across the subsystem.</p></article>
<article id="common-timestamp_op-14"><h3>Shared conditions for this topic · What survives or continues after a power cycle?</h3><p>Restoring a saved value can move time backward; uninterrupted counting through power loss is not guaranteed.</p></article>
<article id="common-timestamp_op-15"><h3>Shared conditions for this topic · Are other controllers or namespaces affected?</h3><p>Setting one controller does not synchronize every controller.</p></article>
</section>
<section id="source-index"><h2>Source locations and existing figure guides</h2><p>Base printed page = PDF page−26; the other two use identical numbers. Locations follow the supplied PDF body and retain figure numbers. Shared pages contribute only the relevant definitions, excluding Fabrics and PCIe link/packet content.</p><ul class="qa-references">
<li id="ref-reset"><strong>Base 2.4 · §3.7.1–3.7.4</strong><br>Printed pages 120–124 · PDF 146–150</li>
<li id="ref-status"><strong>Base 2.4 · §4.2.3</strong><br>Printed pages 145–155 · PDF 171–181 · Figure 101–105</li>
<li id="ref-feature"><strong>Base 2.4 · §4.4</strong><br>Printed pages 166–169 · PDF 192–195 · Figure 126–127</li>
<li id="ref-aer"><strong>Base 2.4 · §5.2.2</strong><br>Printed pages 183–190 · PDF 209–216 · Figure 150–156</li>
<li id="ref-aerfull"><strong>Base 2.4 · §5.2.2 (PCIe-applicable events)</strong><br>Printed pages 183–191 · PDF 209–217 · Figure 150–160</li>
<li id="ref-getfeat"><strong>Base 2.4 · §5.2.12</strong><br>Printed pages 209–212 · PDF 235–238 · Figure 197–202</li>
<li id="ref-getlog"><strong>Base 2.4 · §5.2.13–5.2.13.1.1</strong><br>Printed pages 212–218 · PDF 238–244 · Figure 203–211</li>
<li id="ref-error"><strong>Base 2.4 · §5.2.13.1.2</strong><br>Printed pages 218–220 · PDF 244–246 · Figure 212</li>
<li id="ref-smart"><strong>Base 2.4 · §5.2.13.1.3</strong><br>Printed pages 220–225 · PDF 246–251 · Figure 213–214</li>
<li id="ref-pel"><strong>Base 2.4 · §5.2.13.1.14 (header, reset, hardware, Set Feature events)</strong><br>Printed pages 244–256, 258, 262–264 · PDF 270–282, 284, 288–290 · Figure 232–244, 246, 252–253</li>
<li id="ref-pelcontext"><strong>Base 2.4 · §5.2.13.1.14–5.2.13.1.14.2.5 (exclude PCIe link/packet decoding)</strong><br>Printed pages 244–256, 258 · PDF 270–282, 284 · Figure 232–244, 246</li>
<li id="ref-fwpel"><strong>Base 2.4 · §5.2.13.1.14.2.2, 5.2.13.1.14.2.4</strong><br>Printed pages 252–255 · PDF 278–281 · Figure 238, 240–241</li>
<li id="ref-nspelevent"><strong>Base 2.4 · §5.2.13.1.14.2.6</strong><br>Printed pages 258–259 · PDF 284–285 · Figure 247</li>
<li id="ref-formatpel"><strong>Base 2.4 · §5.2.13.1.14.2.7–5.2.13.1.14.2.8</strong><br>Printed pages 259–261 · PDF 285–287 · Figure 248–249</li>
<li id="ref-sanitizepel"><strong>Base 2.4 · §5.2.13.1.14.2.9–5.2.13.1.14.2.10</strong><br>Printed pages 261–262 · PDF 287–288 · Figure 250–251</li>
<li id="ref-idctrl"><strong>Base 2.4 · §5.2.14.2.1</strong><br>Printed pages 340–387 · PDF 366–413 · Figure 338–341</li>
<li id="ref-setfeat"><strong>Base 2.4 · §5.2.30.1 (common fields, scope and persistence)</strong><br>Printed pages 456–460 · PDF 482–486 · Figure 463–466</li>
<li id="ref-aec"><strong>Base 2.4 · §5.2.30.1.6</strong><br>Printed pages 466–468 · PDF 492–494 · Figure 474</li>
<li id="ref-timestamp"><strong>Base 2.4 · §5.2.30.1.8</strong><br>Printed pages 469–471 · PDF 495–497 · Figure 479–480</li>
<li id="ref-nvmpel"><strong>NVM Command Set 1.3 · §4.1.4.4</strong><br>Printed pages 76–77 · PDF 76–77 · Figure 112</li>
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
<nav class="qr-top" aria-label="Bank and editions"><a href="#content">Skip to content</a><a href="/nvme/question-bank/en/">Question index</a><a href="/nvme/question-bank/persistent-events/zh-tw/">繁體中文</a><a href="/DOCS/nvme-question-bank/persistent-events.html">Chinese tutorial HTML</a></nav>
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
