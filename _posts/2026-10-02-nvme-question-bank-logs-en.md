---
layout: post
title: "NVMe Self-Study Bank: Get Log Page and data consistency"
date: 2026-10-02 00:00:00 +0800
categories: [nvme]
permalink: /nvme/question-bank/logs/en/
lang: en
nvme_quickref: true
nvme_qa: true
---

<div class="nvme-quickref nvme-qa">
<nav class="qr-top" aria-label="Bank and editions"><a href="#content">Skip to content</a><a href="/nvme/question-bank/en/">Question index</a><a href="/nvme/question-bank/logs/zh-tw/">繁體中文</a><a href="/DOCS/nvme-question-bank/logs.html">Chinese tutorial HTML</a></nav>
<main id="content"><p class="qr-eyebrow">BASE 2.4 / NVM 1.3 / PCIe 1.4 · Q1–320</p>
<header><p class="qa-range">Q69–Q81</p><h1>Get Log Page and data consistency</h1><p class="qr-intro">Logs expose state, history or capability, with different lifetimes and read effects. Choose the view and scope before length, pagination, acknowledgment and consistency.</p><p>Practice first, then reveal 17 answer items per question. All numerical examples are hypothetical. Status is written SCT/SC; h indicates hexadecimal.</p></header>
<aside class="qa-glossary"><h2>Terms used in this volume</h2><dl><dt>Controller / namespace</dt><dd>A controller receives commands and manages access. A namespace is a logical storage space that commands can address. An NVM subsystem contains controllers and nonvolatile storage resources.</dd><dt>SQ / CQ / SQE / CQE</dt><dd>Submission and Completion Queues carry command entries (SQEs) and completion entries (CQEs). QID identifies a queue, CID distinguishes outstanding commands in one SQ, and NSID identifies a namespace.</dd><dt>Register / Identify / Feature / Log</dt><dd>A register exposes control or state. Identify queries capabilities and attributes; features query or configure operation; log pages report specific state or records. FID, LID, CNS and CSI select features, logs, Identify structures and command sets.</dd><dt>index / offset / zero-based</dt><dd>An index selects an entry, usually starting at 0; an offset measures distance from an origin in specified units. A zero-based count encodes count−1, but not every zero-valued field is a count. A Dword is 4 bytes; a byte is 8 bits.</dd><dt>Scope / reset / retention</dt><dd>Scope names the affected objects; retention means preserving state. Controller Reset (clearing CC.EN) is one form of Controller Level Reset, or CLR. Different CLR triggers can retain different registers.</dd></dl></aside>
<section id="overview" class="qa-overview"><h2>Four separate questions when reading logs</h2><p class="qa-takeaway">Choose the evidence first; a successful read does not complete the operation being observed.</p>
<div class="qr-table" tabindex="0" role="region" aria-label="Horizontally scrollable comparison table"><table><thead><tr><th scope="col">Evidence needed</th><th scope="col">View</th><th scope="col">Limitation</th></tr></thead><tbody><tr><td>Supported logs</td><td>LID 00h</td><td>Support does not imply a current event</td></tr><tr><td>Current health</td><td>SMART LID 02h</td><td>Current warnings and lifetime counters differ</td></tr><tr><td>Command error details</td><td>Error LID 01h</td><td>Correlate identity; old entries can disappear</td></tr><tr><td>Persistent event history</td><td>PEL LID 0Dh</td><td>Capacity and supported-event limits remain</td></tr></tbody></table></div>
<p><strong>Worked interpretation: </strong>A 4096-byte read encodes NUMD1023. The next byte offset is 4096, but index-offset logs require their own entry progression.</p>
<p class="qa-citations">Sources: <a href="#ref-getlog">Base 2.4 §5.2.13–5.2.13.1.1</a> · <a href="#ref-smart">Base 2.4 §5.2.13.1.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-pelcontext">Base 2.4 §5.2.13.1.14–5.2.13.1.14.2.5 (exclude PCIe link/packet decoding)</a></p>
</section>
<div class="qa-controls" hidden><label>Search this page <input type="search" id="qa-search" placeholder="Question number, field or keyword"></label><button type="button" data-expand="true">Expand all answers</button><button type="button" data-expand="false">Collapse all answers</button><output id="qa-count" aria-live="polite"></output></div>
<section id="question-index"><h2>Questions in this volume</h2><ol class="qa-index">
<li><a href="#q-069">Q69 · What does Supported Log Pages provide, and how should support be checked before reading another log?</a></li>
<li><a href="#q-070">Q70 · What do Error Information and SMART/Health Information record?</a></li>
<li><a href="#q-071">Q71 · What do Firmware Slot, Changed Namespace and Commands Supported and Effects logs establish?</a></li>
<li><a href="#q-072">Q72 · When should Device Self-test, Persistent Event and Sanitize Status logs be used?</a></li>
<li><a href="#q-073">Q73 · What do Endurance Group, Predictable Latency, Lockdown, Boot Partition and Media Unit Status logs contain?</a></li>
<li><a href="#q-074">Q74 · How should NSID and other selectors follow a log’s scope?</a></li>
<li><a href="#q-075">Q75 · How are large logs read in chunks, including offsets, lengths, overlaps and gaps?</a></li>
<li><a href="#q-076">Q76 · What are LSI, UUID Index and Retain Asynchronous Event used for?</a></li>
<li><a href="#q-077">Q77 · How can a host detect inconsistent log chunks when content changes?</a></li>
<li><a href="#q-078">Q78 · How are old records handled when Error Information or PEL reaches capacity?</a></li>
<li><a href="#q-079">Q79 · Which log data survives controller reset, subsystem reset or power cycling?</a></li>
<li><a href="#q-080">Q80 · How should advertised log/command support be checked against actual behavior?</a></li>
<li><a href="#q-081">Q81 · How does Commands Supported and Effects describe opcode support and impact?</a></li>
</ol></section>
<article class="qa-question" id="q-069" data-question="69"><h2><a class="qa-qid" href="#q-069">Q69</a> What does Supported Log Pages provide, and how should support be checked before reading another log?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-069-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-069-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Supported Log Pages is a directory of LIDs and index-offset support on the current interface. It distinguishes lack of support from zero-valued data. Reading it is a discovery method, not a mandatory command before every log request.</p>
</li>
<li id="q-069-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Results describe the receiving interface and controller. Interfaces can differ; with CC.CSS=110b, CSI and the enabled command-set profile also affect support. Another interface’s directory is not interchangeable.</p>
</li>
<li id="q-069-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Use Get Log Page LID=00h. Identify.LPA.SPEDS controls extended offset/length support; each LID entry supplies LSUPP and IOS for support and index-offset capability.</p>
</li>
<li id="q-069-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>There are 256 four-byte entries. LID n is at byte 4n; bit 0 is LSUPP, bit 1 IOS, and LIDSP is log-specific. The host should ignore other fields when LSUPP=0.</p>
</li>
<li id="q-069-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Select the controller and command set, read 00h, and inspect the target entry. Then apply that log’s scope, length and parameters. Rediscover capability after relevant firmware or configuration changes.</p>
</li>
<li id="q-069-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Success returns a capability directory, not the logs themselves. LSUPP=1 for 81h establishes Sanitize Status availability, not that sanitization has run or completed.</p>
</li>
<li id="q-069-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>An unsupported LID normally returns Invalid Log Page (1/09h). Using unsupported OT=1 returns Invalid Field (0/02h), even when the LID is supported. These are different failures.</p>
</li>
<li id="q-069-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-069-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Reading a log does not itself require a new event. <a class="qa-rule-link" href="#common-log_query-9">Full rule in this volume</a></p>
</li>
<li id="q-069-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Get Log Page returns the selected data. <a class="qa-rule-link" href="#common-log_query-10">Full rule in this volume</a></p>
</li>
<li id="q-069-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>Get Log Page is not a per-read PEL audit trail. <a class="qa-rule-link" href="#common-log_query-11">Full rule in this volume</a></p>
</li>
<li id="q-069-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Controller Reset stops outstanding queries, which are reissued after Admin Queue recovery. <a class="qa-rule-link" href="#common-log_query-12">Full rule in this volume</a></p>
</li>
<li id="q-069-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>After subsystem reset, recover query access on affected controllers and re-read the logs. <a class="qa-rule-link" href="#common-log_query-13">Full rule in this volume</a></p>
</li>
<li id="q-069-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Reissue the query after a power cycle. <a class="qa-rule-link" href="#common-log_query-14">Full rule in this volume</a></p>
</li>
<li id="q-069-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Queries do not write namespace user data, but some reads acknowledge events or clear reported lists. <a class="qa-rule-link" href="#common-log_query-15">Full rule in this volume</a></p>
</li>
<li id="q-069-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Compare LSUPP, IOS and LPA against a valid request. Supported logs need not support index offsets; an invalid request does not by itself contradict LSUPP.</p>
</li>
<li id="q-069-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First establish the same interface, CSI and configuration period, then verify four-byte entry addressing.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-getlog">Base 2.4 §5.2.13–5.2.13.1.1</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-profile">Base 2.4 §5.2.30.1.18</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-070" data-question="70"><h2><a class="qa-qid" href="#q-070">Q70</a> What do Error Information and SMART/Health Information record?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-070-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-070-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Error Information explains individual errors; SMART/Health describes current warnings and lifetime usage. They answer different questions and are not substitutes.</p>
</li>
<li id="q-070-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>LID 01h is controller-scoped. LID 02h may accept namespace requests, but Base 2.4 defines no namespace-specific SMART information, so controller and namespace reports contain identical information rather than independent usage totals.</p>
</li>
<li id="q-070-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>ELPE+1 gives the maximum Error Information entry count. The LPA SMART bit determines whether per-namespace requests are accepted; establish support before interpreting the data.</p>
</li>
<li id="q-070-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>Each 01h entry is 64 bytes, with ECNT, SQID, CID, status, parameter location and NSID. The 512-byte 02h page contains warnings, temperature, spare, endurance estimate and cumulative usage/error counters.</p>
</li>
<li id="q-070-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Preserve the CQE, correlate 01h to the command, then sample 02h for health context. Record times to avoid pairing an old error with an unrelated current warning.</p>
</li>
<li id="q-070-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>A successful read does not mean an error-free device. ECNT=0 marks an invalid entry; Percentage Used=100 describes estimated endurance consumption, not necessarily device failure.</p>
</li>
<li id="q-070-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>A specific-NSID SMART request without support returns Invalid Field (0/02h). Historical status in the log is distinct from the status of the current Get Log Page command.</p>
</li>
<li id="q-070-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-070-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Reading a log does not itself require a new event. <a class="qa-rule-link" href="#common-log_query-9">Full rule in this volume</a></p>
</li>
<li id="q-070-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Get Log Page returns the selected data. <a class="qa-rule-link" href="#common-log_query-10">Full rule in this volume</a></p>
</li>
<li id="q-070-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>Get Log Page is not a per-read PEL audit trail. <a class="qa-rule-link" href="#common-log_query-11">Full rule in this volume</a></p>
</li>
<li id="q-070-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Controller Reset stops outstanding queries, which are reissued after Admin Queue recovery. <a class="qa-rule-link" href="#common-log_query-12">Full rule in this volume</a></p>
</li>
<li id="q-070-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>After subsystem reset, recover query access on affected controllers and re-read the logs. <a class="qa-rule-link" href="#common-log_query-13">Full rule in this volume</a></p>
</li>
<li id="q-070-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Reissue the query after a power cycle. <a class="qa-rule-link" href="#common-log_query-14">Full rule in this volume</a></p>
</li>
<li id="q-070-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Queries do not write namespace user data, but some reads acknowledge events or clear reported lists. <a class="qa-rule-link" href="#common-log_query-15">Full rule in this volume</a></p>
</li>
<li id="q-070-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>The SMART Error Log Entries total is not the number of entries currently visible in 01h. Finite capacity and reset clearing can make the lifetime total larger.</p>
</li>
<li id="q-070-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First identify whether the comparison concerns error history, current warning state or a cumulative count, then check validity and timing.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-getlog">Base 2.4 §5.2.13–5.2.13.1.1</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-smart">Base 2.4 §5.2.13.1.3</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-071" data-question="71"><h2><a class="qa-qid" href="#q-071">Q71</a> What do Firmware Slot, Changed Namespace and Commands Supported and Effects logs establish?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-071-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-071-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>These logs identify the running firmware slot, namespaces with reported changes, and command support/effects. None is a universal operation history.</p>
</li>
<li id="q-071-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>03h is domain or subsystem scoped; 04h describes attached-namespace changes for this controller; 05h describes its commands for the selected command set.</p>
</li>
<li id="q-071-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Check 00h and relevant Identify capabilities. Slot count and read-only restrictions come from FRMW, not merely the number of nonzero strings in 03h.</p>
</li>
<li id="q-071-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>Read CAFS, NAFS and FRS1–7 in 03h; NSIDs and the leading FFFFFFFFh overflow marker in 04h; and CSUPP, effects, CSE/CSER and CSP in 05h.</p>
</li>
<li id="q-071-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Choose by purpose: compare 03h with Identify.FR after activation; read 04h and rediscover namespaces after notification; use 05h before a management operation and refresh affected capabilities afterward.</p>
</li>
<li id="q-071-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>NAFS=2 identifies a slot awaiting an applicable CLR, not the currently running slot. NSID 7 in 04h signals change without specifying whether it was formatted or deleted.</p>
</li>
<li id="q-071-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Separate retrieval errors from reported state. Unsupported LIDs return 1/09h; invalid defined parameters follow 0/02h rules. Empty slots or empty change lists are not themselves retrieval failures.</p>
</li>
<li id="q-071-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-071-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Reading a log does not itself require a new event. <a class="qa-rule-link" href="#common-log_query-9">Full rule in this volume</a></p>
</li>
<li id="q-071-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Get Log Page returns the selected data. <a class="qa-rule-link" href="#common-log_query-10">Full rule in this volume</a></p>
</li>
<li id="q-071-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>Get Log Page is not a per-read PEL audit trail. <a class="qa-rule-link" href="#common-log_query-11">Full rule in this volume</a></p>
</li>
<li id="q-071-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Controller Reset stops outstanding queries, which are reissued after Admin Queue recovery. <a class="qa-rule-link" href="#common-log_query-12">Full rule in this volume</a></p>
</li>
<li id="q-071-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>After subsystem reset, recover query access on affected controllers and re-read the logs. <a class="qa-rule-link" href="#common-log_query-13">Full rule in this volume</a></p>
</li>
<li id="q-071-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Reissue the query after a power cycle. <a class="qa-rule-link" href="#common-log_query-14">Full rule in this volume</a></p>
</li>
<li id="q-071-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Queries do not write namespace user data, but some reads acknowledge events or clear reported lists. <a class="qa-rule-link" href="#common-log_query-15">Full rule in this volume</a></p>
</li>
<li id="q-071-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Correlate the active slot with FR, changed IDs with fresh Identify, and CSUPP with valid command behavior. The three logs need not contain matching values.</p>
</li>
<li id="q-071-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First check for confusing NAFS with CAFS or a changed list with the complete active namespace inventory.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-fwlog">Base 2.4 §5.2.13.1.4</a> · <a href="#ref-changedlog">Base 2.4 §5.2.13.1.5</a> · <a href="#ref-commandseffects">Base 2.4 §5.2.13.1.6</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-072" data-question="72"><h2><a class="qa-qid" href="#q-072">Q72</a> When should Device Self-test, Persistent Event and Sanitize Status logs be used?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-072-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-072-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Self-test logs show progress and recent results; PEL provides supported historical events; Sanitize Status reports sanitization state and outcome. Choose the right evidence before equating acceptance with completion.</p>
</li>
<li id="q-072-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Self-test scope depends on capabilities such as DSTO.SDSO. PEL is subsystem-scoped; 81h uses NSID to distinguish subsystem and namespace targets. The querying controller is not necessarily the full affected scope.</p>
</li>
<li id="q-072-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Check self-test OACS, PEL LPA and subsystem/namespace sanitize capabilities, then the relevant LIDs. A readable status log does not establish every operation method.</p>
</li>
<li id="q-072-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>For 06h read DSTOS before progress and validity-qualified results. For 0Dh establish or obtain a reporting context and traverse lengths. For 81h inspect SSTAT before SPROG and outcome fields.</p>
</li>
<li id="q-072-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Poll 81h after sanitize acceptance for background completion; inspect the newest valid 06h result after self-test; use PEL for supported historical reset or management events.</p>
</li>
<li id="q-072-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Successful Get establishes retrieval, not a passed test or successful sanitize. Missing PEL events require checking event support, logging conditions and retained history.</p>
</li>
<li id="q-072-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Unsupported LIDs return 1/09h; invalid PEL context sequencing can return 0/0Ch. Operation failures in returned data do not turn a successful retrieval CQE into failure.</p>
</li>
<li id="q-072-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-072-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Reading a log does not itself require a new event. <a class="qa-rule-link" href="#common-log_query-9">Full rule in this volume</a></p>
</li>
<li id="q-072-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Get Log Page returns the selected data. <a class="qa-rule-link" href="#common-log_query-10">Full rule in this volume</a></p>
</li>
<li id="q-072-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>Get Log Page is not a per-read PEL audit trail. <a class="qa-rule-link" href="#common-log_query-11">Full rule in this volume</a></p>
</li>
<li id="q-072-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Controller Reset stops outstanding queries, which are reissued after Admin Queue recovery. <a class="qa-rule-link" href="#common-log_query-12">Full rule in this volume</a></p>
</li>
<li id="q-072-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>After subsystem reset, recover query access on affected controllers and re-read the logs. <a class="qa-rule-link" href="#common-log_query-13">Full rule in this volume</a></p>
</li>
<li id="q-072-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Reissue the query after a power cycle. <a class="qa-rule-link" href="#common-log_query-14">Full rule in this volume</a></p>
</li>
<li id="q-072-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Queries do not write namespace user data, but some reads acknowledge events or clear reported lists. <a class="qa-rule-link" href="#common-log_query-15">Full rule in this volume</a></p>
</li>
<li id="q-072-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Correlate target, time and latest results. An old test result or previous sanitize success is not proof of success for the current operation.</p>
</li>
<li id="q-072-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First match the queried target and operation before interpreting progress or history.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-dstlog">Base 2.4 §5.2.13.1.7</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-getlog">Base 2.4 §5.2.13–5.2.13.1.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-073" data-question="73"><h2><a class="qa-qid" href="#q-073">Q73</a> What do Endurance Group, Predictable Latency, Lockdown, Boot Partition and Media Unit Status logs contain?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-073-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-073-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>These logs describe group endurance, predictable-latency state, prohibited operations, boot partitions and media-unit resources. They are not interchangeable health reports.</p>
</li>
<li id="q-073-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Establish the management object: endurance group, NVM set, lockdown selection/scope, controller-accessed boot partitions, or domain/subsystem media units.</p>
</li>
<li id="q-073-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Check 00h and relevant Identify capabilities. The main LIDs are 09h, 0Ah/0Bh, 14h, 15h and 10h. LSI can mean different things for different logs.</p>
</li>
<li id="q-073-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>Inspect group warnings/spare/endurance in 09h, set latency state/events in 0Ah/0Bh, prohibited opcodes/FIDs in 14h, partition identity/protection in 15h, and media-unit identity/association/state in 10h.</p>
</li>
<li id="q-073-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Choose the LID by question, map resource IDs through Identify, then apply the log’s selectors and structure. Group-3 health requires ENDGID=3, not an arbitrary NSID substituted into LSI.</p>
</li>
<li id="q-073-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Results describe the selected object. One group warning does not establish identical media faults in every namespace; lockdown entries are prohibitions, not execution history.</p>
</li>
<li id="q-073-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Distinguish unsupported LIDs (1/09h) from invalid resource selectors governed by each log’s defined fields and specific status. Do not classify all selector failures as Invalid Namespace.</p>
</li>
<li id="q-073-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-073-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Reading a log does not itself require a new event. <a class="qa-rule-link" href="#common-log_query-9">Full rule in this volume</a></p>
</li>
<li id="q-073-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Get Log Page returns the selected data. <a class="qa-rule-link" href="#common-log_query-10">Full rule in this volume</a></p>
</li>
<li id="q-073-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>Get Log Page is not a per-read PEL audit trail. <a class="qa-rule-link" href="#common-log_query-11">Full rule in this volume</a></p>
</li>
<li id="q-073-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Controller Reset stops outstanding queries, which are reissued after Admin Queue recovery. <a class="qa-rule-link" href="#common-log_query-12">Full rule in this volume</a></p>
</li>
<li id="q-073-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>After subsystem reset, recover query access on affected controllers and re-read the logs. <a class="qa-rule-link" href="#common-log_query-13">Full rule in this volume</a></p>
</li>
<li id="q-073-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Reissue the query after a power cycle. <a class="qa-rule-link" href="#common-log_query-14">Full rule in this volume</a></p>
</li>
<li id="q-073-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Queries do not write namespace user data, but some reads acknowledge events or clear reported lists. <a class="qa-rule-link" href="#common-log_query-15">Full rule in this volume</a></p>
</li>
<li id="q-073-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Correlate resource association, reported state and behavior. Prohibited FIDs should match lockdown policy; media-unit state must be related to namespace dependencies.</p>
</li>
<li id="q-073-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First check whether different resource identifier types were confused.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-getlog">Base 2.4 §5.2.13–5.2.13.1.1</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-074" data-question="74"><h2><a class="qa-qid" href="#q-074">Q74</a> How should NSID and other selectors follow a log’s scope?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-074-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-074-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Scope identifies the kind of object described; selectors identify its instance. A common NSID field does not make every log per-namespace.</p>
</li>
<li id="q-074-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Figure 209 lists scopes, while individual fields may define more specific ones. Read both the directory and the selected LID’s exceptions.</p>
</li>
<li id="q-074-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Check LSUPP, LPA, multi-domain support and whether CSI/UUID selection applies. Together they determine valid query combinations.</p>
</li>
<li id="q-074-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>Controller/subsystem logs normally use NSID=0 or FFFFFFFFh. LSI, LSP, CSI and UIDX are separate selectors, not extensions of NSID.</p>
</li>
<li id="q-074-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Name the target object first, then map it to the specified fields. Fill unused fields according to reserved-field rules.</p>
</li>
<li id="q-074-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>A valid request returns the selected scope. Aggregate SMART and group endurance are different views; copying an aggregate does not create independent namespace statistics.</p>
</li>
<li id="q-074-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Under the common rule, controller/subsystem logs with another NSID return Invalid Field (0/02h). Other scopes use their LID-specific and NSID rules.</p>
</li>
<li id="q-074-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-074-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Reading a log does not itself require a new event. <a class="qa-rule-link" href="#common-log_query-9">Full rule in this volume</a></p>
</li>
<li id="q-074-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Get Log Page returns the selected data. <a class="qa-rule-link" href="#common-log_query-10">Full rule in this volume</a></p>
</li>
<li id="q-074-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>Get Log Page is not a per-read PEL audit trail. <a class="qa-rule-link" href="#common-log_query-11">Full rule in this volume</a></p>
</li>
<li id="q-074-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Controller Reset stops outstanding queries, which are reissued after Admin Queue recovery. <a class="qa-rule-link" href="#common-log_query-12">Full rule in this volume</a></p>
</li>
<li id="q-074-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>After subsystem reset, recover query access on affected controllers and re-read the logs. <a class="qa-rule-link" href="#common-log_query-13">Full rule in this volume</a></p>
</li>
<li id="q-074-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Reissue the query after a power cycle. <a class="qa-rule-link" href="#common-log_query-14">Full rule in this volume</a></p>
</li>
<li id="q-074-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Queries do not write namespace user data, but some reads acknowledge events or clear reported lists. <a class="qa-rule-link" href="#common-log_query-15">Full rule in this volume</a></p>
</li>
<li id="q-074-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Retain command selectors, Identify associations and returned data so comparisons refer to the same object.</p>
</li>
<li id="q-074-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>Check the LID’s scope first; a nonzero NSID alone does not establish namespace-specific information.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-getlog">Base 2.4 §5.2.13–5.2.13.1.1</a> · <a href="#ref-smart">Base 2.4 §5.2.13.1.3</a> · <a href="#ref-uuid">Base 2.4 §8.1.31.1–8.1.31.2</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-075" data-question="75"><h2><a class="qa-qid" href="#q-075">Q75</a> How are large logs read in chunks, including offsets, lengths, overlaps and gaps?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-075-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-075-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Chunking reads a large log with bounded buffers. Both coverage and consistency matter; individually successful reads do not establish a complete coherent file.</p>
</li>
<li id="q-075-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Offsets locate data within the log, not host memory. OT=0 uses bytes; OT=1 uses log-defined entry indices. Do not mix their units.</p>
</li>
<li id="q-075-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Check LPA.SPEDS and per-LID IOS, then size transfers using MDTS and log-specific length rules.</p>
</li>
<li id="q-075-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>NUMD=(NUMDU&lt;&lt;16)|NUMDL normally encodes bytes/4−1. LPOU/LPOL form the 64-bit offset; byte offsets require Dword alignment, with further log-specific constraints.</p>
</li>
<li id="q-075-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>An 8192-byte log can use two 4096-byte reads at offsets 0 and 4096, each NUMD=1023. Check coverage; overlaps can be compared, but changing content prevents arbitrary merging.</p>
</li>
<li id="q-075-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Success covers the requested valid range. Unless otherwise specified, bytes beyond the log end are undefined and are not additional log content.</p>
</li>
<li id="q-075-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>An offset beyond the log or OT=1 without IOS returns 0/02h. For nonzero low two byte-offset bits, the controller may reject or operate as if those bits were zero; neither outcome is universally mandatory.</p>
</li>
<li id="q-075-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-075-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Reading a log does not itself require a new event. <a class="qa-rule-link" href="#common-log_query-9">Full rule in this volume</a></p>
</li>
<li id="q-075-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Get Log Page returns the selected data. <a class="qa-rule-link" href="#common-log_query-10">Full rule in this volume</a></p>
</li>
<li id="q-075-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>Get Log Page is not a per-read PEL audit trail. <a class="qa-rule-link" href="#common-log_query-11">Full rule in this volume</a></p>
</li>
<li id="q-075-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Controller Reset stops outstanding queries, which are reissued after Admin Queue recovery. <a class="qa-rule-link" href="#common-log_query-12">Full rule in this volume</a></p>
</li>
<li id="q-075-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>After subsystem reset, recover query access on affected controllers and re-read the logs. <a class="qa-rule-link" href="#common-log_query-13">Full rule in this volume</a></p>
</li>
<li id="q-075-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Reissue the query after a power cycle. <a class="qa-rule-link" href="#common-log_query-14">Full rule in this volume</a></p>
</li>
<li id="q-075-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Queries do not write namespace user data, but some reads acknowledge events or clear reported lists. <a class="qa-rule-link" href="#common-log_query-15">Full rule in this volume</a></p>
</li>
<li id="q-075-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Verify total length, offsets/NUMD and generation or reporting context. Complete coverage and one coherent snapshot are separate requirements.</p>
</li>
<li id="q-075-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First check offset units and NUMD’s +1 conversion, then look for mixed generations.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-getlog">Base 2.4 §5.2.13–5.2.13.1.1</a> · <a href="#ref-telemetrylog">Base 2.4 §5.2.13.1.8–5.2.13.1.9</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-076" data-question="76"><h2><a class="qa-qid" href="#q-076">Q76</a> What are LSI, UUID Index and Retain Asynchronous Event used for?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-076-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-076-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>These fields select a resource, a data-definition context, and event retention. Their roles are independent.</p>
</li>
<li id="q-076-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>LSI is LID-specific; UIDX selects a UUID-list definition; RAE controls the associated event. Not every log uses all three.</p>
</li>
<li id="q-076-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Check whether LSI is defined and UUID selection supported. RAE behavior depends on the event’s acknowledgment rules.</p>
</li>
<li id="q-076-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>LSI is CDW11[31:16], UIDX CDW14[6:0] with zero meaning no UUID selection, and RAE CDW10[15]. UIDX is an index, not the UUID itself.</p>
</li>
<li id="q-076-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Fix the target and UUID definition, then decide whether the event should remain pending. Record RAE for each chunk and follow the selected log’s acknowledgment procedure.</p>
</li>
<li id="q-076-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Successful RAE=1 reads retain the event; successful RAE=0 reads clear it as defined. Failed reads must retain it; an attempted read is not acknowledgment.</p>
</li>
<li id="q-076-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Invalid UUID selection follows 0/02h rules in §8.1.31; invalid LSI follows the LID definition. Changing RAE does not fix the selected resource.</p>
</li>
<li id="q-076-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-076-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Reading a log does not itself require a new event. <a class="qa-rule-link" href="#common-log_query-9">Full rule in this volume</a></p>
</li>
<li id="q-076-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Get Log Page returns the selected data. <a class="qa-rule-link" href="#common-log_query-10">Full rule in this volume</a></p>
</li>
<li id="q-076-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>Get Log Page is not a per-read PEL audit trail. <a class="qa-rule-link" href="#common-log_query-11">Full rule in this volume</a></p>
</li>
<li id="q-076-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Controller Reset stops outstanding queries, which are reissued after Admin Queue recovery. <a class="qa-rule-link" href="#common-log_query-12">Full rule in this volume</a></p>
</li>
<li id="q-076-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>After subsystem reset, recover query access on affected controllers and re-read the logs. <a class="qa-rule-link" href="#common-log_query-13">Full rule in this volume</a></p>
</li>
<li id="q-076-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Reissue the query after a power cycle. <a class="qa-rule-link" href="#common-log_query-14">Full rule in this volume</a></p>
</li>
<li id="q-076-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Queries do not write namespace user data, but some reads acknowledge events or clear reported lists. <a class="qa-rule-link" href="#common-log_query-15">Full rule in this volume</a></p>
</li>
<li id="q-076-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Compare the target, UUID mapping and pending-event state. Identical returned bytes with different RAE can produce different subsequent notification behavior.</p>
</li>
<li id="q-076-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First look for another successful RAE=0 read that already acknowledged the event.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-getlog">Base 2.4 §5.2.13–5.2.13.1.1</a> · <a href="#ref-uuid">Base 2.4 §8.1.31.1–8.1.31.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-077" data-question="77"><h2><a class="qa-qid" href="#q-077">Q77</a> How can a host detect inconsistent log chunks when content changes?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-077-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-077-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>This prevents combining different times into an apparently complete report. Correct length and coverage do not establish a single capture.</p>
</li>
<li id="q-077-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Consistency is log-specific: Telemetry has generations, PEL reporting contexts. Other dynamic logs do not gain cross-command atomic snapshots by assumption.</p>
</li>
<li id="q-077-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Check the supported log structure/version and its generation, total length, availability or context action. Common command fields alone are insufficient.</p>
</li>
<li id="q-077-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>Retain Telemetry generation and area boundaries, or PEL context/TLL/event lengths and versions, together with each chunk’s offset, length and acquisition time.</p>
</li>
<li id="q-077-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Read the header, use the same capture/context and recheck the header where applicable. A changed generation requires reacquisition or an explicit consistency limitation, not just replacement of the header.</p>
</li>
<li id="q-077-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Initial TCDGN=10 and final=11 leave intervening chunks unproven even when all Gets succeed. Retain consistency evidence with the resulting report.</p>
</li>
<li id="q-077-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Content changes need not produce an error CQE. Invalid PEL context operations can produce 0/0Ch, which is distinct from a legitimate generation change.</p>
</li>
<li id="q-077-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-077-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Reading a log does not itself require a new event. <a class="qa-rule-link" href="#common-log_query-9">Full rule in this volume</a></p>
</li>
<li id="q-077-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Get Log Page returns the selected data. <a class="qa-rule-link" href="#common-log_query-10">Full rule in this volume</a></p>
</li>
<li id="q-077-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>Get Log Page is not a per-read PEL audit trail. <a class="qa-rule-link" href="#common-log_query-11">Full rule in this volume</a></p>
</li>
<li id="q-077-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Controller Reset stops outstanding queries, which are reissued after Admin Queue recovery. <a class="qa-rule-link" href="#common-log_query-12">Full rule in this volume</a></p>
</li>
<li id="q-077-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>After subsystem reset, recover query access on affected controllers and re-read the logs. <a class="qa-rule-link" href="#common-log_query-13">Full rule in this volume</a></p>
</li>
<li id="q-077-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Reissue the query after a power cycle. <a class="qa-rule-link" href="#common-log_query-14">Full rule in this volume</a></p>
</li>
<li id="q-077-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Queries do not write namespace user data, but some reads acknowledge events or clear reported lists. <a class="qa-rule-link" href="#common-log_query-15">Full rule in this volume</a></p>
</li>
<li id="q-077-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Treat headers, chunks and query order as one evidence set. The last capability or generation value cannot retroactively validate every earlier chunk.</p>
</li>
<li id="q-077-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>Check generation/context continuity before blaming the parser.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-getlog">Base 2.4 §5.2.13–5.2.13.1.1</a> · <a href="#ref-telemetrylog">Base 2.4 §5.2.13.1.8–5.2.13.1.9</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-078" data-question="78"><h2><a class="qa-qid" href="#q-078">Q78</a> How are old records handled when Error Information or PEL reaches capacity?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-078-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-078-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Finite logs cannot preserve unlimited history. Distinguish cumulative counts from currently readable records; a missing old entry does not prove the event never occurred.</p>
</li>
<li id="q-078-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Error Information is controller-scoped; PEL contains supported subsystem events accessed through reporting contexts. Capacity and read lifecycles differ.</p>
</li>
<li id="q-078-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>ELPE+1 sets Error Information capacity. For PEL inspect support, report length/event count and maximum capacity; SMART totals do not size the current buffer.</p>
</li>
<li id="q-078-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>Error entries are newest first with ECNT identity. PEL traversal uses EHL, EL, ET and ETR; events are not fixed 64-byte error entries.</p>
</li>
<li id="q-078-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Record valid entries and boundary identities, then correlate overlapping samples. Mark lost history explicitly rather than inventing missing records or their order.</p>
</li>
<li id="q-078-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>When Error Information is full, the specification recommends inserting the new entry and discarding the oldest. A complete finite PEL report is not the device’s entire lifetime history.</p>
</li>
<li id="q-078-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Full storage does not automatically make a valid Get fail. Inspect retention behavior; invalid parameters or contexts are separate command errors.</p>
</li>
<li id="q-078-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-078-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Reading a log does not itself require a new event. <a class="qa-rule-link" href="#common-log_query-9">Full rule in this volume</a></p>
</li>
<li id="q-078-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Get Log Page returns the selected data. <a class="qa-rule-link" href="#common-log_query-10">Full rule in this volume</a></p>
</li>
<li id="q-078-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>Get Log Page is not a per-read PEL audit trail. <a class="qa-rule-link" href="#common-log_query-11">Full rule in this volume</a></p>
</li>
<li id="q-078-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Controller Reset stops outstanding queries, which are reissued after Admin Queue recovery. <a class="qa-rule-link" href="#common-log_query-12">Full rule in this volume</a></p>
</li>
<li id="q-078-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>After subsystem reset, recover query access on affected controllers and re-read the logs. <a class="qa-rule-link" href="#common-log_query-13">Full rule in this volume</a></p>
</li>
<li id="q-078-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Reissue the query after a power cycle. <a class="qa-rule-link" href="#common-log_query-14">Full rule in this volume</a></p>
</li>
<li id="q-078-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Queries do not write namespace user data, but some reads acknowledge events or clear reported lists. <a class="qa-rule-link" href="#common-log_query-15">Full rule in this volume</a></p>
</li>
<li id="q-078-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>ECNT/SMART totals may diverge from visible entry counts. Explain the difference using capacity and retention, not an expectation of unlimited historical preservation.</p>
</li>
<li id="q-078-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First check whether the request asked for only the newest few entries before concluding that older records were evicted.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-079" data-question="79"><h2><a class="qa-qid" href="#q-079">Q79</a> Which log data survives controller reset, subsystem reset or power cycling?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-079-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-079-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Separate the query command, temporary reporting state and retained history. An aborted Get does not imply erasure of all underlying data.</p>
</li>
<li id="q-079-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Retention may apply to a whole log or individual fields. Establish reset coverage in multi-controller and multi-domain configurations.</p>
</li>
<li id="q-079-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Use log-specific retention text and reset rules. Figure 209’s Restore to Default Content concerns manufacturing defaults, not clearing on every reset.</p>
</li>
<li id="q-079-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>Compare error entries, their ECNT, SMART totals, current temperature, PEL events and PEL context separately. Proximity does not imply identical retention.</p>
</li>
<li id="q-079-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Capture the same target before reset, perform the specified event, recover and read again. Record concurrent activation, format or manufacturing-default restoration as separate causes.</p>
</li>
<li id="q-079-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Error entries should clear on CLR/power cycle while ECNT persists. SMART lifetime data persists across power cycles unless a field says otherwise. Persistent PEL events do not make reporting contexts persistent.</p>
</li>
<li id="q-079-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Comparing values creates no status. A failed post-reset Get first requires checking readiness, selectors and context; it is not evidence of cleared data.</p>
</li>
<li id="q-079-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-079-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Reading a log does not itself require a new event. <a class="qa-rule-link" href="#common-log_query-9">Full rule in this volume</a></p>
</li>
<li id="q-079-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Get Log Page returns the selected data. <a class="qa-rule-link" href="#common-log_query-10">Full rule in this volume</a></p>
</li>
<li id="q-079-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>Get Log Page is not a per-read PEL audit trail. <a class="qa-rule-link" href="#common-log_query-11">Full rule in this volume</a></p>
</li>
<li id="q-079-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Controller Reset stops outstanding queries, which are reissued after Admin Queue recovery. <a class="qa-rule-link" href="#common-log_query-12">Full rule in this volume</a></p>
</li>
<li id="q-079-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>After subsystem reset, recover query access on affected controllers and re-read the logs. <a class="qa-rule-link" href="#common-log_query-13">Full rule in this volume</a></p>
</li>
<li id="q-079-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Reissue the query after a power cycle. <a class="qa-rule-link" href="#common-log_query-14">Full rule in this volume</a></p>
</li>
<li id="q-079-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Queries do not write namespace user data, but some reads acknowledge events or clear reported lists. <a class="qa-rule-link" href="#common-log_query-15">Full rule in this volume</a></p>
</li>
<li id="q-079-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Compare field semantics and validity rather than requiring byte-identical buffers. Persistent counters can coexist with newly sampled current state.</p>
</li>
<li id="q-079-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First determine whether the discrepancy concerns stored content, an invalidated context or an interrupted query.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-getlog">Base 2.4 §5.2.13–5.2.13.1.1</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-smart">Base 2.4 §5.2.13.1.3</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-080" data-question="80"><h2><a class="qa-qid" href="#q-080">Q80</a> How should advertised log/command support be checked against actual behavior?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-080-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-080-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Build a reproducible support-consistency check. Support establishes valid uses, not success for every parameter combination.</p>
</li>
<li id="q-080-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Fix interface, controller, CSI, UUID selection and configuration time. With CC.CSS=110b, a command set not enabled by the profile is treated as unsupported.</p>
</li>
<li id="q-080-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Preserve LSUPP/IOS, CSUPP, Identify capability bits and FID 19h. Log support and opcode support are different declarations.</p>
</li>
<li id="q-080-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>Retain all relevant selectors, length and data pointers, then decode CQE SCT/SC rather than only a tool’s error string.</p>
</li>
<li id="q-080-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Construct a request meeting capability, scope and state requirements, execute, then exclude invalid fields, lockdown, namespace readiness and intervening changes before declaring a contradiction.</p>
</li>
<li id="q-080-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>In a stable context, unsupported status for a valid advertised operation is a contradiction to investigate. A legitimate restrictive status is not equivalent to lack of support.</p>
</li>
<li id="q-080-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Unsupported LID uses 1/09h; unsupported opcode uses 0/01h; 0/02h calls for parameter review. Preserve specific exceptions and allowed choices for multiple errors.</p>
</li>
<li id="q-080-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-080-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Reading a log does not itself require a new event. <a class="qa-rule-link" href="#common-log_query-9">Full rule in this volume</a></p>
</li>
<li id="q-080-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Get Log Page returns the selected data. <a class="qa-rule-link" href="#common-log_query-10">Full rule in this volume</a></p>
</li>
<li id="q-080-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>Get Log Page is not a per-read PEL audit trail. <a class="qa-rule-link" href="#common-log_query-11">Full rule in this volume</a></p>
</li>
<li id="q-080-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Controller Reset stops outstanding queries, which are reissued after Admin Queue recovery. <a class="qa-rule-link" href="#common-log_query-12">Full rule in this volume</a></p>
</li>
<li id="q-080-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>After subsystem reset, recover query access on affected controllers and re-read the logs. <a class="qa-rule-link" href="#common-log_query-13">Full rule in this volume</a></p>
</li>
<li id="q-080-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Reissue the query after a power cycle. <a class="qa-rule-link" href="#common-log_query-14">Full rule in this volume</a></p>
</li>
<li id="q-080-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Queries do not write namespace user data, but some reads acknowledge events or clear reported lists. <a class="qa-rule-link" href="#common-log_query-15">Full rule in this volume</a></p>
</li>
<li id="q-080-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Compare declarations, behavior and timing. After activation, rediscover support instead of imposing an old table on new firmware.</p>
</li>
<li id="q-080-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First verify the same interface and command-set configuration on both sides of the comparison.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-getlog">Base 2.4 §5.2.13–5.2.13.1.1</a> · <a href="#ref-commandseffects">Base 2.4 §5.2.13.1.6</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-profile">Base 2.4 §5.2.30.1.18</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-081" data-question="81"><h2><a class="qa-qid" href="#q-081">Q81</a> How does Commands Supported and Effects describe opcode support and impact?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-081-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-081-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>The table describes support and possible effects on data, namespaces and controller capability. It reports overall possible effects, not effects guaranteed on every invocation.</p>
</li>
<li id="q-081-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Admin and I/O opcodes occupy separate regions; the I/O region also requires the correct command set. CSP can name several possible scopes because parameters affect actual impact.</p>
</li>
<li id="q-081-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Check LPA.CELP, LID 05h and command-set selection. CSP=0 means no scope is reported, not no affected object.</p>
</li>
<li id="q-081-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>Admin entry offset is 4×opcode; I/O offset is 1024+4×opcode. Decode support, effects, submission recommendations, UUID selection and scope rather than only bit 0.</p>
</li>
<li id="q-081-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Select the entry and coordinate work under CSE/CSER recommendations. Use a supported nonzero CSER relaxation; otherwise use CSE. Rediscover potentially changed capabilities or inventory afterward.</p>
</li>
<li id="q-081-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>NIC=1 permits inventory or multi-namespace capability changes; it does not guarantee one new namespace per call. CSUPP=0 requires all other entry fields to be zero.</p>
</li>
<li id="q-081-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Retrieval errors follow Get Log Page; operation errors follow the command. Submission recommendations do not authorize inventing a mandatory status for every violation.</p>
</li>
<li id="q-081-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-081-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Reading a log does not itself require a new event. <a class="qa-rule-link" href="#common-log_query-9">Full rule in this volume</a></p>
</li>
<li id="q-081-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Get Log Page returns the selected data. <a class="qa-rule-link" href="#common-log_query-10">Full rule in this volume</a></p>
</li>
<li id="q-081-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>Get Log Page is not a per-read PEL audit trail. <a class="qa-rule-link" href="#common-log_query-11">Full rule in this volume</a></p>
</li>
<li id="q-081-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Controller Reset stops outstanding queries, which are reissued after Admin Queue recovery. <a class="qa-rule-link" href="#common-log_query-12">Full rule in this volume</a></p>
</li>
<li id="q-081-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>After subsystem reset, recover query access on affected controllers and re-read the logs. <a class="qa-rule-link" href="#common-log_query-13">Full rule in this volume</a></p>
</li>
<li id="q-081-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Reissue the query after a power cycle. <a class="qa-rule-link" href="#common-log_query-14">Full rule in this volume</a></p>
</li>
<li id="q-081-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Queries do not write namespace user data, but some reads acknowledge events or clear reported lists. <a class="qa-rule-link" href="#common-log_query-15">Full rule in this volume</a></p>
</li>
<li id="q-081-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Correlate effects with before/after Identify, inventory and data. Support declarations should agree; actual effects depend on this invocation’s parameters.</p>
</li>
<li id="q-081-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First check the I/O region’s 1024-byte base, then CSI and the interpretation of CSP=0.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-commandseffects">Base 2.4 §5.2.13.1.6</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-profile">Base 2.4 §5.2.30.1.18</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<section id="common-rules" class="qa-common"><h2>Shared rules linked from the answers</h2><p>Each shared mechanism is explained in full once in this volume. Use browser Back to return to the question; explicit command or feature exceptions take precedence.</p>
<article id="common-command-8"><h3>Command completion, events and records · How are DNR and More set?</h3><p>For a CQE, DNR=1 means the identical command is expected to fail if resubmitted to any controller in this subsystem; DNR=0 means it may succeed. Do not assign DNR=1 solely from an error name unless that condition mandates it. More=1 identifies additional information for this command in the Error Information Log. DNR should be zero when SCT=SC=0.</p></article>
<article id="common-log_query-9"><h3>Shared conditions for this topic · Is an asynchronous event generated?</h3><p>Reading a log does not itself require a new event. A successful RAE=0 read may acknowledge its event; RAE=1 and unsuccessful reads retain it. Immediate and One-Shot events have separate clearing rules.</p></article>
<article id="common-log_query-10"><h3>Shared conditions for this topic · Are Error Information or other logs updated?</h3><p>Get Log Page returns the selected data. Reads can clear reported changes or acknowledge events, depending on the log and RAE, so preserve comparison evidence first. A successful read does not require an error entry; failed reads follow CQE and error-log rules.</p></article>
<article id="common-log_query-11"><h3>Shared conditions for this topic · Is it recorded in the Persistent Event Log?</h3><p>Get Log Page is not a per-read PEL audit trail. Reading PEL does not create another such event; separately occurring events follow their supported logging conditions.</p></article>
<article id="common-log_query-12"><h3>Shared conditions for this topic · What survives or continues after Controller Reset?</h3><p>Controller Reset stops outstanding queries, which are reissued after Admin Queue recovery. Content retention is separate: Error Information entries should clear but Error Count persists; SMART cumulative information and PEL follow their field-specific persistence rules.</p></article>
<article id="common-log_query-13"><h3>Shared conditions for this topic · What survives or continues after NVM Subsystem Reset?</h3><p>After subsystem reset, recover query access on affected controllers and re-read the logs. This is not restoration of manufacturing defaults; Figure 209’s Restore to Default Content column is not an ordinary reset-retention table.</p></article>
<article id="common-log_query-14"><h3>Shared conditions for this topic · What survives or continues after a power cycle?</h3><p>Reissue the query after a power cycle. SMART lifetime information and PEL have persistent content; Error Information entries should clear while the cumulative Error Count persists. Reassess current temperature, active operations and reporting contexts under their own rules rather than expecting every byte to remain fixed.</p></article>
<article id="common-log_query-15"><h3>Shared conditions for this topic · Are other controllers or namespaces affected?</h3><p>Queries do not write namespace user data, but some reads acknowledge events or clear reported lists. Logs have controller, namespace, domain or subsystem scopes; track readers and acknowledgment times when several hosts share the view.</p></article>
</section>
<section id="source-index"><h2>Source locations and existing figure guides</h2><p>Base printed page = PDF page−26; the other two use identical numbers. Locations follow the supplied PDF body and retain figure numbers. Shared pages contribute only the relevant definitions, excluding Fabrics and PCIe link/packet content.</p><ul class="qa-references">
<li id="ref-reset"><strong>Base 2.4 · §3.7.1–3.7.4</strong><br>Printed pages 120–124 · PDF 146–150</li>
<li id="ref-status"><strong>Base 2.4 · §4.2.3</strong><br>Printed pages 145–155 · PDF 171–181 · Figure 101–105</li>
<li id="ref-aer"><strong>Base 2.4 · §5.2.2</strong><br>Printed pages 183–190 · PDF 209–216 · Figure 150–156</li>
<li id="ref-getlog"><strong>Base 2.4 · §5.2.13–5.2.13.1.1</strong><br>Printed pages 212–218 · PDF 238–244 · Figure 203–211</li>
<li id="ref-error"><strong>Base 2.4 · §5.2.13.1.2</strong><br>Printed pages 218–220 · PDF 244–246 · Figure 212</li>
<li id="ref-smart"><strong>Base 2.4 · §5.2.13.1.3</strong><br>Printed pages 220–225 · PDF 246–251 · Figure 213–214</li>
<li id="ref-fwlog"><strong>Base 2.4 · §5.2.13.1.4</strong><br>Printed pages 225–226 · PDF 251–252 · Figure 215</li>
<li id="ref-changedlog"><strong>Base 2.4 · §5.2.13.1.5</strong><br>Printed pages 226 · PDF 252</li>
<li id="ref-commandseffects"><strong>Base 2.4 · §5.2.13.1.6</strong><br>Printed pages 226–229 · PDF 252–255 · Figure 216–217</li>
<li id="ref-dstlog"><strong>Base 2.4 · §5.2.13.1.7</strong><br>Printed pages 229–232 · PDF 255–258 · Figure 218–219</li>
<li id="ref-telemetrylog"><strong>Base 2.4 · §5.2.13.1.8–5.2.13.1.9</strong><br>Printed pages 232–237 · PDF 258–263 · Figure 220–223</li>
<li id="ref-pel"><strong>Base 2.4 · §5.2.13.1.14 (header, reset, hardware, Set Feature events)</strong><br>Printed pages 244–256, 258, 262–264 · PDF 270–282, 284, 288–290 · Figure 232–244, 246, 252–253</li>
<li id="ref-pelcontext"><strong>Base 2.4 · §5.2.13.1.14–5.2.13.1.14.2.5 (exclude PCIe link/packet decoding)</strong><br>Printed pages 244–256, 258 · PDF 270–282, 284 · Figure 232–244, 246</li>
<li id="ref-idctrl"><strong>Base 2.4 · §5.2.14.2.1</strong><br>Printed pages 340–387 · PDF 366–413 · Figure 338–341</li>
<li id="ref-profile"><strong>Base 2.4 · §5.2.30.1.18</strong><br>Printed pages 478–479 · PDF 504–505 · Figure 494–495</li>
<li id="ref-uuid"><strong>Base 2.4 · §8.1.31.1–8.1.31.2</strong><br>Printed pages 737–738 · PDF 763–764 · Figure 782</li>
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
<nav class="qr-top" aria-label="Bank and editions"><a href="#content">Skip to content</a><a href="/nvme/question-bank/en/">Question index</a><a href="/nvme/question-bank/logs/zh-tw/">繁體中文</a><a href="/DOCS/nvme-question-bank/logs.html">Chinese tutorial HTML</a></nav>
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
