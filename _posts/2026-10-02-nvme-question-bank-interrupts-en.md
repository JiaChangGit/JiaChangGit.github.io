---
layout: post
title: "NVMe Self-Study Bank: Interrupt configuration and completion delivery"
date: 2026-10-02 00:00:00 +0800
categories: [nvme]
permalink: /nvme/question-bank/interrupts/en/
lang: en
nvme_quickref: true
nvme_qa: true
---

<div class="nvme-quickref nvme-qa">
<nav class="qr-top" aria-label="Bank and editions"><a href="#content">Skip to content</a><a href="/nvme/question-bank/en/">Question index</a><a href="/nvme/question-bank/interrupts/zh-tw/">繁體中文</a><a href="/DOCS/nvme-question-bank/interrupts.html">Chinese tutorial HTML</a></nav>
<main id="content"><p class="qr-eyebrow">BASE 2.4 / NVM 1.3 / PCIe 1.4 · Q1–320</p>
<header><p class="qa-range">Q286–Q296</p><h1>Interrupt configuration and completion delivery</h1><p class="qr-intro">Establish CQE posting before diagnosing routing, aggregation, masks and host consumption.</p><p>Practice first, then reveal 17 answer items per question. All numerical examples are hypothetical. Status is written SCT/SC; h indicates hexadecimal.</p></header>
<aside class="qa-glossary"><h2>Terms used in this volume</h2><dl><dt>Controller / namespace</dt><dd>A controller receives commands and manages access. A namespace is a logical storage space that commands can address. An NVM subsystem contains controllers and nonvolatile storage resources.</dd><dt>SQ / CQ / SQE / CQE</dt><dd>Submission and Completion Queues carry command entries (SQEs) and completion entries (CQEs). QID identifies a queue, CID distinguishes outstanding commands in one SQ, and NSID identifies a namespace.</dd><dt>Register / Identify / Feature / Log</dt><dd>A register exposes control or state. Identify queries capabilities and attributes; features query or configure operation; log pages report specific state or records. FID, LID, CNS and CSI select features, logs, Identify structures and command sets.</dd><dt>index / offset / zero-based</dt><dd>An index selects an entry, usually starting at 0; an offset measures distance from an origin in specified units. A zero-based count encodes count−1, but not every zero-valued field is a count. A Dword is 4 bytes; a byte is 8 bits.</dd><dt>Scope / reset / retention</dt><dd>Scope names the affected objects; retention means preserving state. Controller Reset (clearing CC.EN) is one form of Controller Level Reset, or CLR. Different CLR triggers can retain different registers.</dd></dl></aside>
<section id="overview" class="qa-overview"><h2>Four controls answer different questions</h2><p class="qa-takeaway">FID 09h.CD disables coalescing, not interrupts.</p>
<div class="qr-table" tabindex="0" role="region" aria-label="Horizontally scrollable comparison table"><table><thead><tr><th scope="col">Control</th><th scope="col">Interface</th><th scope="col">Meaning</th></tr></thead><tbody><tr><td>CQ routing</td><td>IV/IEN</td><td>Vector and notification enable</td></tr><tr><td>Aggregation</td><td>TIME/THR</td><td>Recommended delay/count</td></tr><tr><td>Per-vector override</td><td>CD</td><td>Disable aggregation for this vector</td></tr><tr><td>Masking</td><td>Mode-specific masks</td><td>Allow delivery</td></tr></tbody></table></div>
<p><strong>Worked interpretation: </strong>Shared masked CQs can accumulate entries; one later interrupt can cover many completions.</p>
<p class="qa-citations">Sources: <a href="#ref-interruptfeature">Base 2.4 §5.2.30.2.1–5.2.30.2.2</a> · <a href="#ref-interruptmask">Base 2.4 §3.1.4 (INTMS, INTMC)</a> · <a href="#ref-interruptfull">PCIe Transport 1.4 §3.5–3.5.2 (interrupt delivery and masks), 3.8.4</a> · <a href="#ref-create">Base 2.4 §5.3.1–5.3.2</a></p>
</section>
<div class="qa-controls" hidden><label>Search this page <input type="search" id="qa-search" placeholder="Question number, field or keyword"></label><button type="button" data-expand="true">Expand all answers</button><button type="button" data-expand="false">Collapse all answers</button><output id="qa-count" aria-live="polite"></output></div>
<section id="question-index"><h2>Questions in this volume</h2><ol class="qa-index">
<li><a href="#q-286">Q286 · How does a CQ select an interrupt vector?</a></li>
<li><a href="#q-287">Q287 · How do shared and dedicated CQ vectors differ?</a></li>
<li><a href="#q-288">Q288 · How do coalescing threshold and time work?</a></li>
<li><a href="#q-289">Q289 · How is interrupt coalescing disabled?</a></li>
<li><a href="#q-290">Q290 · Does FID 09h mask interrupts, and where are actual masks configured?</a></li>
<li><a href="#q-291">Q291 · Can completions be posted while a vector is masked?</a></li>
<li><a href="#q-292">Q292 · How are accumulated completions handled after unmasking?</a></li>
<li><a href="#q-293">Q293 · Can an in-use vector be reconfigured?</a></li>
<li><a href="#q-294">Q294 · How are interrupts restored after reset?</a></li>
<li><a href="#q-295">Q295 · How are interrupt resources reclaimed after queue deletion?</a></li>
<li><a href="#q-296">Q296 · How are interrupt settings, CQ state and completions cross-checked?</a></li>
</ol></section>
<article class="qa-question" id="q-286" data-question="286"><h2><a class="qa-qid" href="#q-286">Q286</a> How does a CQ select an interrupt vector?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-286-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-286-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>CQ identity selects completion storage, while IV selects notification; the numbers need not match.</p>
</li>
<li id="q-286-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>I/O CQs own vector associations; SQs use them through CQID.</p>
</li>
<li id="q-286-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Establish interrupt mode and allocated vectors before CQ creation.</p>
</li>
<li id="q-286-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>IV selects the vector, IEN enables CQ interrupts and PC selects memory contiguity.</p>
</li>
<li id="q-286-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Allocate vectors, create CQ and SQ, then verify with I/O.</p>
</li>
<li id="q-286-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>CQ5 can use IV2; an SQ7 completion goes to CQ5 and is identified by SQID/CID after IV2 notification.</p>
</li>
<li id="q-286-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Invalid vector selection maps to 1/08h, independently of QID validity.</p>
</li>
<li id="q-286-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-286-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Completion interrupts and Asynchronous Event Requests are different mechanisms; an AER completion also uses a CQE, but an ordinary I/O interrupt is not an NVMe asynchronous event. <a class="qa-rule-link" href="#common-interrupt_op-9">Full rule in this volume</a></p>
</li>
<li id="q-286-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Normal configuration/delivery does not require an error entry. <a class="qa-rule-link" href="#common-interrupt_op-10">Full rule in this volume</a></p>
</li>
<li id="q-286-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>Interrupts are not individually recorded in PEL. <a class="qa-rule-link" href="#common-interrupt_op-11">Full rule in this volume</a></p>
</li>
<li id="q-286-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>CLR invalidates I/O queues and their vector associations. <a class="qa-rule-link" href="#common-interrupt_op-12">Full rule in this volume</a></p>
</li>
<li id="q-286-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Rebuild affected queues, vector associations and settings after subsystem reset; a reused vector number does not preserve the old CQ lifetime. <a class="qa-rule-link" href="#common-interrupt_op-13">Full rule in this volume</a></p>
</li>
<li id="q-286-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Configure interrupt mode, queues and features after power cycle; mode changes also need not retain coalescing and reconfiguration is recommended. <a class="qa-rule-link" href="#common-interrupt_op-14">Full rule in this volume</a></p>
</li>
<li id="q-286-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>A shared vector’s mask/coalescing affects notifications for all associated CQs; equal vector numbers on different controllers do not identify one NVMe setting. <a class="qa-rule-link" href="#common-interrupt_op-15">Full rule in this volume</a></p>
</li>
<li id="q-286-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Correlate successful creation, IV/IEN and the host handler’s CQ list.</p>
</li>
<li id="q-286-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First identify which CQ the host checks for that vector.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-interruptfull">PCIe Transport 1.4 §3.5–3.5.2 (interrupt delivery and masks), 3.8.4</a> · <a href="#ref-interruptmask">Base 2.4 §3.1.4 (INTMS, INTMC)</a> · <a href="#ref-interruptfeature">Base 2.4 §5.2.30.2.1–5.2.30.2.2</a> · <a href="#ref-create">Base 2.4 §5.3.1–5.3.2</a> · <a href="#ref-delete">Base 2.4 §5.3.3–5.3.4</a> · <a href="#ref-cqe">Base 2.4 §4.2.1, 4.2.3–4.2.4</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-287" data-question="287"><h2><a class="qa-qid" href="#q-287">Q287</a> How do shared and dedicated CQ vectors differ?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-287-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-287-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Sharing saves vectors but requires scanning more CQs; dedicated vectors simplify distribution.</p>
</li>
<li id="q-287-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Aggregation thresholds apply per vector and may cover several CQs.</p>
</li>
<li id="q-287-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Inspect available vectors and CQ IV/IEN associations.</p>
</li>
<li id="q-287-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>CQEs retain command identity; the interrupt does not enumerate completed commands.</p>
</li>
<li id="q-287-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Maintain vector-to-CQ membership, consume valid entries and acknowledge each CQ.</p>
</li>
<li id="q-287-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>One IV3 interrupt can cover multiple completions in two CQs.</p>
</li>
<li id="q-287-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Interrupt and CQE counts need not match under sharing and aggregation.</p>
</li>
<li id="q-287-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-287-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Completion interrupts and Asynchronous Event Requests are different mechanisms; an AER completion also uses a CQE, but an ordinary I/O interrupt is not an NVMe asynchronous event. <a class="qa-rule-link" href="#common-interrupt_op-9">Full rule in this volume</a></p>
</li>
<li id="q-287-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Normal configuration/delivery does not require an error entry. <a class="qa-rule-link" href="#common-interrupt_op-10">Full rule in this volume</a></p>
</li>
<li id="q-287-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>Interrupts are not individually recorded in PEL. <a class="qa-rule-link" href="#common-interrupt_op-11">Full rule in this volume</a></p>
</li>
<li id="q-287-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>CLR invalidates I/O queues and their vector associations. <a class="qa-rule-link" href="#common-interrupt_op-12">Full rule in this volume</a></p>
</li>
<li id="q-287-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Rebuild affected queues, vector associations and settings after subsystem reset; a reused vector number does not preserve the old CQ lifetime. <a class="qa-rule-link" href="#common-interrupt_op-13">Full rule in this volume</a></p>
</li>
<li id="q-287-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Configure interrupt mode, queues and features after power cycle; mode changes also need not retain coalescing and reconfiguration is recommended. <a class="qa-rule-link" href="#common-interrupt_op-14">Full rule in this volume</a></p>
</li>
<li id="q-287-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>A shared vector’s mask/coalescing affects notifications for all associated CQs; equal vector numbers on different controllers do not identify one NVMe setting. <a class="qa-rule-link" href="#common-interrupt_op-15">Full rule in this volume</a></p>
</li>
<li id="q-287-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Measure per-CQ posting and consumption, not only shared-vector counts.</p>
</li>
<li id="q-287-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First check whether the handler misses a CQ sharing the vector.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-interruptfull">PCIe Transport 1.4 §3.5–3.5.2 (interrupt delivery and masks), 3.8.4</a> · <a href="#ref-interruptmask">Base 2.4 §3.1.4 (INTMS, INTMC)</a> · <a href="#ref-interruptfeature">Base 2.4 §5.2.30.2.1–5.2.30.2.2</a> · <a href="#ref-create">Base 2.4 §5.3.1–5.3.2</a> · <a href="#ref-delete">Base 2.4 §5.3.3–5.3.4</a> · <a href="#ref-cqe">Base 2.4 §4.2.1, 4.2.3–4.2.4</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-288" data-question="288"><h2><a class="qa-qid" href="#q-288">Q288</a> How do coalescing threshold and time work?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-288-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-288-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Aggregation reduces host overhead at possible notification-latency cost without requiring delayed CQE posting.</p>
</li>
<li id="q-288-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>FID 08h applies to I/O queues, not Admin CQ.</p>
</li>
<li id="q-288-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Read/configure TIME/THR and check each vector’s coalescing-disable bit.</p>
</li>
<li id="q-288-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>TIME is in 100 µs units and THR is a zero-based recommended completion count.</p>
</li>
<li id="q-288-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Establish nonzero settings and CD0 before comparing notification timing under a fixed workload.</p>
</li>
<li id="q-288-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>TIME5/THR7 recommends 500 µs and 8 completions, not waiting for both exact values.</p>
</li>
<li id="q-288-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>PCIe permits implementation-specific aggregation, including none; deviation from recommended timing alone is not a violation.</p>
</li>
<li id="q-288-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-288-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Completion interrupts and Asynchronous Event Requests are different mechanisms; an AER completion also uses a CQE, but an ordinary I/O interrupt is not an NVMe asynchronous event. <a class="qa-rule-link" href="#common-interrupt_op-9">Full rule in this volume</a></p>
</li>
<li id="q-288-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Normal configuration/delivery does not require an error entry. <a class="qa-rule-link" href="#common-interrupt_op-10">Full rule in this volume</a></p>
</li>
<li id="q-288-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>Interrupts are not individually recorded in PEL. <a class="qa-rule-link" href="#common-interrupt_op-11">Full rule in this volume</a></p>
</li>
<li id="q-288-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>CLR invalidates I/O queues and their vector associations. <a class="qa-rule-link" href="#common-interrupt_op-12">Full rule in this volume</a></p>
</li>
<li id="q-288-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Rebuild affected queues, vector associations and settings after subsystem reset; a reused vector number does not preserve the old CQ lifetime. <a class="qa-rule-link" href="#common-interrupt_op-13">Full rule in this volume</a></p>
</li>
<li id="q-288-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Configure interrupt mode, queues and features after power cycle; mode changes also need not retain coalescing and reconfiguration is recommended. <a class="qa-rule-link" href="#common-interrupt_op-14">Full rule in this volume</a></p>
</li>
<li id="q-288-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>A shared vector’s mask/coalescing affects notifications for all associated CQs; equal vector numbers on different controllers do not identify one NVMe setting. <a class="qa-rule-link" href="#common-interrupt_op-15">Full rule in this volume</a></p>
</li>
<li id="q-288-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>CQ-head updates may restart aggregation and ongoing servicing can continually postpone another notification.</p>
</li>
<li id="q-288-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First distinguish completion posting from interrupt delay.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-interruptfull">PCIe Transport 1.4 §3.5–3.5.2 (interrupt delivery and masks), 3.8.4</a> · <a href="#ref-interruptmask">Base 2.4 §3.1.4 (INTMS, INTMC)</a> · <a href="#ref-interruptfeature">Base 2.4 §5.2.30.2.1–5.2.30.2.2</a> · <a href="#ref-create">Base 2.4 §5.3.1–5.3.2</a> · <a href="#ref-delete">Base 2.4 §5.3.3–5.3.4</a> · <a href="#ref-cqe">Base 2.4 §4.2.1, 4.2.3–4.2.4</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-289" data-question="289"><h2><a class="qa-qid" href="#q-289">Q289</a> How is interrupt coalescing disabled?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-289-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-289-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Disabling aggregation removes coalescing, not interrupts.</p>
</li>
<li id="q-289-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>FID 08h controls I/O aggregation globally, while FID 09h.CD disables it per vector.</p>
</li>
<li id="q-289-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Read aggregation settings, vector overrides and CQ interrupt enable.</p>
</li>
<li id="q-289-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>Either zero TIME or zero THR implicitly disables aggregation; CD1 prevents aggregation on that vector.</p>
</li>
<li id="q-289-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Use FID 08h globally, or associate an I/O CQ before setting a per-vector override.</p>
</li>
<li id="q-289-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Verify readback and apply delivery/mask rules rather than the previous aggregation threshold.</p>
</li>
<li id="q-289-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>THR0 has an explicit disable meaning despite ordinary zero-based count interpretation.</p>
</li>
<li id="q-289-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-289-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Completion interrupts and Asynchronous Event Requests are different mechanisms; an AER completion also uses a CQE, but an ordinary I/O interrupt is not an NVMe asynchronous event. <a class="qa-rule-link" href="#common-interrupt_op-9">Full rule in this volume</a></p>
</li>
<li id="q-289-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Normal configuration/delivery does not require an error entry. <a class="qa-rule-link" href="#common-interrupt_op-10">Full rule in this volume</a></p>
</li>
<li id="q-289-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>Interrupts are not individually recorded in PEL. <a class="qa-rule-link" href="#common-interrupt_op-11">Full rule in this volume</a></p>
</li>
<li id="q-289-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>CLR invalidates I/O queues and their vector associations. <a class="qa-rule-link" href="#common-interrupt_op-12">Full rule in this volume</a></p>
</li>
<li id="q-289-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Rebuild affected queues, vector associations and settings after subsystem reset; a reused vector number does not preserve the old CQ lifetime. <a class="qa-rule-link" href="#common-interrupt_op-13">Full rule in this volume</a></p>
</li>
<li id="q-289-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Configure interrupt mode, queues and features after power cycle; mode changes also need not retain coalescing and reconfiguration is recommended. <a class="qa-rule-link" href="#common-interrupt_op-14">Full rule in this volume</a></p>
</li>
<li id="q-289-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>A shared vector’s mask/coalescing affects notifications for all associated CQs; equal vector numbers on different controllers do not identify one NVMe setting. <a class="qa-rule-link" href="#common-interrupt_op-15">Full rule in this volume</a></p>
</li>
<li id="q-289-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>No aggregation does not require one separate interrupt per CQE.</p>
</li>
<li id="q-289-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First check whether CD1 was mistaken for masking.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-interruptfull">PCIe Transport 1.4 §3.5–3.5.2 (interrupt delivery and masks), 3.8.4</a> · <a href="#ref-interruptmask">Base 2.4 §3.1.4 (INTMS, INTMC)</a> · <a href="#ref-interruptfeature">Base 2.4 §5.2.30.2.1–5.2.30.2.2</a> · <a href="#ref-create">Base 2.4 §5.3.1–5.3.2</a> · <a href="#ref-delete">Base 2.4 §5.3.3–5.3.4</a> · <a href="#ref-cqe">Base 2.4 §4.2.1, 4.2.3–4.2.4</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-290" data-question="290"><h2><a class="qa-qid" href="#q-290">Q290</a> Does FID 09h mask interrupts, and where are actual masks configured?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-290-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-290-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>The original premise confuses FID 09h coalescing control with interrupt masking.</p>
</li>
<li id="q-290-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>A mask blocks delivery for all CQs sharing that vector.</p>
</li>
<li id="q-290-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Select the masking interface after establishing the active interrupt mode.</p>
</li>
<li id="q-290-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>INTMS write-one sets and INTMC write-one clears pin/MSI masks; MSI-X uses function and table-vector masks.</p>
</li>
<li id="q-290-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Preserve state, mask, service/acknowledge CQs, unmask and check remaining work.</p>
</li>
<li id="q-290-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>INTMC requires writing one to clear a mask; zero has no effect.</p>
</li>
<li id="q-290-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>INTMS/INTMC access is prohibited and undefined under MSI-X, not a guaranteed NVMe status.</p>
</li>
<li id="q-290-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Mask register accesses have no NVMe CQE; only separate Get/Set Feature commands carry DNR/More.</p>
</li>
<li id="q-290-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Completion interrupts and Asynchronous Event Requests are different mechanisms; an AER completion also uses a CQE, but an ordinary I/O interrupt is not an NVMe asynchronous event. <a class="qa-rule-link" href="#common-interrupt_op-9">Full rule in this volume</a></p>
</li>
<li id="q-290-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Normal configuration/delivery does not require an error entry. <a class="qa-rule-link" href="#common-interrupt_op-10">Full rule in this volume</a></p>
</li>
<li id="q-290-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>Interrupts are not individually recorded in PEL. <a class="qa-rule-link" href="#common-interrupt_op-11">Full rule in this volume</a></p>
</li>
<li id="q-290-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>CLR invalidates I/O queues and their vector associations. <a class="qa-rule-link" href="#common-interrupt_op-12">Full rule in this volume</a></p>
</li>
<li id="q-290-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Rebuild affected queues, vector associations and settings after subsystem reset; a reused vector number does not preserve the old CQ lifetime. <a class="qa-rule-link" href="#common-interrupt_op-13">Full rule in this volume</a></p>
</li>
<li id="q-290-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Configure interrupt mode, queues and features after power cycle; mode changes also need not retain coalescing and reconfiguration is recommended. <a class="qa-rule-link" href="#common-interrupt_op-14">Full rule in this volume</a></p>
</li>
<li id="q-290-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>A shared vector’s mask/coalescing affects notifications for all associated CQs; equal vector numbers on different controllers do not identify one NVMe setting. <a class="qa-rule-link" href="#common-interrupt_op-15">Full rule in this volume</a></p>
</li>
<li id="q-290-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>FID 09h readback does not establish MSI-X mask state.</p>
</li>
<li id="q-290-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First inspect actual mode and mask bits.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-interruptfull">PCIe Transport 1.4 §3.5–3.5.2 (interrupt delivery and masks), 3.8.4</a> · <a href="#ref-interruptmask">Base 2.4 §3.1.4 (INTMS, INTMC)</a> · <a href="#ref-interruptfeature">Base 2.4 §5.2.30.2.1–5.2.30.2.2</a> · <a href="#ref-create">Base 2.4 §5.3.1–5.3.2</a> · <a href="#ref-delete">Base 2.4 §5.3.3–5.3.4</a> · <a href="#ref-cqe">Base 2.4 §4.2.1, 4.2.3–4.2.4</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-291" data-question="291"><h2><a class="qa-qid" href="#q-291">Q291</a> Can completions be posted while a vector is masked?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-291-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-291-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Masking controls notification rather than command execution or CQ posting.</p>
</li>
<li id="q-291-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Associated CQs can accumulate completions until their capacity limits intervene.</p>
</li>
<li id="q-291-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Inspect masks, IEN, CQ position/phase and applicable MSI-X pending bits.</p>
</li>
<li id="q-291-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>Normal CQE posting continues; MSI-X masks cause pending-interrupt indication.</p>
</li>
<li id="q-291-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Poll and consume valid CQEs, then update head to release space.</p>
</li>
<li id="q-291-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>A new valid CQE without an interrupt can be normal while masked.</p>
</li>
<li id="q-291-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>CQ fullness is a capacity consequence of nonconsumption, not a direct masking rule.</p>
</li>
<li id="q-291-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-291-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Completion interrupts and Asynchronous Event Requests are different mechanisms; an AER completion also uses a CQE, but an ordinary I/O interrupt is not an NVMe asynchronous event. <a class="qa-rule-link" href="#common-interrupt_op-9">Full rule in this volume</a></p>
</li>
<li id="q-291-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Normal configuration/delivery does not require an error entry. <a class="qa-rule-link" href="#common-interrupt_op-10">Full rule in this volume</a></p>
</li>
<li id="q-291-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>Interrupts are not individually recorded in PEL. <a class="qa-rule-link" href="#common-interrupt_op-11">Full rule in this volume</a></p>
</li>
<li id="q-291-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>CLR invalidates I/O queues and their vector associations. <a class="qa-rule-link" href="#common-interrupt_op-12">Full rule in this volume</a></p>
</li>
<li id="q-291-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Rebuild affected queues, vector associations and settings after subsystem reset; a reused vector number does not preserve the old CQ lifetime. <a class="qa-rule-link" href="#common-interrupt_op-13">Full rule in this volume</a></p>
</li>
<li id="q-291-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Configure interrupt mode, queues and features after power cycle; mode changes also need not retain coalescing and reconfiguration is recommended. <a class="qa-rule-link" href="#common-interrupt_op-14">Full rule in this volume</a></p>
</li>
<li id="q-291-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>A shared vector’s mask/coalescing affects notifications for all associated CQs; equal vector numbers on different controllers do not identify one NVMe setting. <a class="qa-rule-link" href="#common-interrupt_op-15">Full rule in this volume</a></p>
</li>
<li id="q-291-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Absence of an interrupt does not establish absence of completion.</p>
</li>
<li id="q-291-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First check valid CQ phase before notification configuration.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-interruptfull">PCIe Transport 1.4 §3.5–3.5.2 (interrupt delivery and masks), 3.8.4</a> · <a href="#ref-interruptmask">Base 2.4 §3.1.4 (INTMS, INTMC)</a> · <a href="#ref-interruptfeature">Base 2.4 §5.2.30.2.1–5.2.30.2.2</a> · <a href="#ref-create">Base 2.4 §5.3.1–5.3.2</a> · <a href="#ref-delete">Base 2.4 §5.3.3–5.3.4</a> · <a href="#ref-cqe">Base 2.4 §4.2.1, 4.2.3–4.2.4</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-292" data-question="292"><h2><a class="qa-qid" href="#q-292">Q292</a> How are accumulated completions handled after unmasking?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-292-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-292-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>One pending interrupt can represent many completions whose results remain in CQs.</p>
</li>
<li id="q-292-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Service all relevant CQs sharing the vector.</p>
</li>
<li id="q-292-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Check mode-specific masks/pending state and associated queues.</p>
</li>
<li id="q-292-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>Pending MSI-X delivery requires both mask layers clear.</p>
</li>
<li id="q-292-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Unmask, process valid CQEs and acknowledge heads while handling arrival races.</p>
</li>
<li id="q-292-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Ten accumulated completions need not cause ten replayed interrupts.</p>
</li>
<li id="q-292-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>INTM masking suppresses MSI pending assertion; MSI-X PBA semantics cannot be copied to it.</p>
</li>
<li id="q-292-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-292-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Completion interrupts and Asynchronous Event Requests are different mechanisms; an AER completion also uses a CQE, but an ordinary I/O interrupt is not an NVMe asynchronous event. <a class="qa-rule-link" href="#common-interrupt_op-9">Full rule in this volume</a></p>
</li>
<li id="q-292-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Normal configuration/delivery does not require an error entry. <a class="qa-rule-link" href="#common-interrupt_op-10">Full rule in this volume</a></p>
</li>
<li id="q-292-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>Interrupts are not individually recorded in PEL. <a class="qa-rule-link" href="#common-interrupt_op-11">Full rule in this volume</a></p>
</li>
<li id="q-292-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>CLR invalidates I/O queues and their vector associations. <a class="qa-rule-link" href="#common-interrupt_op-12">Full rule in this volume</a></p>
</li>
<li id="q-292-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Rebuild affected queues, vector associations and settings after subsystem reset; a reused vector number does not preserve the old CQ lifetime. <a class="qa-rule-link" href="#common-interrupt_op-13">Full rule in this volume</a></p>
</li>
<li id="q-292-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Configure interrupt mode, queues and features after power cycle; mode changes also need not retain coalescing and reconfiguration is recommended. <a class="qa-rule-link" href="#common-interrupt_op-14">Full rule in this volume</a></p>
</li>
<li id="q-292-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>A shared vector’s mask/coalescing affects notifications for all associated CQs; equal vector numbers on different controllers do not identify one NVMe setting. <a class="qa-rule-link" href="#common-interrupt_op-15">Full rule in this volume</a></p>
</li>
<li id="q-292-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Judge consumption completeness, not equality of interrupt and command counts.</p>
</li>
<li id="q-292-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First check another mask layer or omitted shared CQ.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-interruptfull">PCIe Transport 1.4 §3.5–3.5.2 (interrupt delivery and masks), 3.8.4</a> · <a href="#ref-interruptmask">Base 2.4 §3.1.4 (INTMS, INTMC)</a> · <a href="#ref-interruptfeature">Base 2.4 §5.2.30.2.1–5.2.30.2.2</a> · <a href="#ref-create">Base 2.4 §5.3.1–5.3.2</a> · <a href="#ref-delete">Base 2.4 §5.3.3–5.3.4</a> · <a href="#ref-cqe">Base 2.4 §4.2.1, 4.2.3–4.2.4</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-293" data-question="293"><h2><a class="qa-qid" href="#q-293">Q293</a> Can an in-use vector be reconfigured?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-293-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-293-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Distinguish coalescing changes, masking and reassignment of CQ association.</p>
</li>
<li id="q-293-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>FID 09h changes aggregation for the selected vector and its associated CQs.</p>
</li>
<li id="q-293-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>FID 09h requires prior association with an existing I/O CQ.</p>
</li>
<li id="q-293-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>CD selects aggregation behavior, not reassignment of Create CQ.IV.</p>
</li>
<li id="q-293-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Change/read back vector settings; recreate the queue association when a different IV is needed.</p>
</li>
<li id="q-293-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>An existing CQ is the feature’s prerequisite, not a prohibition on change.</p>
</li>
<li id="q-293-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Invalid/unassociated IV should produce Invalid Field, preserving the recommendation strength.</p>
</li>
<li id="q-293-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-293-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Completion interrupts and Asynchronous Event Requests are different mechanisms; an AER completion also uses a CQE, but an ordinary I/O interrupt is not an NVMe asynchronous event. <a class="qa-rule-link" href="#common-interrupt_op-9">Full rule in this volume</a></p>
</li>
<li id="q-293-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Normal configuration/delivery does not require an error entry. <a class="qa-rule-link" href="#common-interrupt_op-10">Full rule in this volume</a></p>
</li>
<li id="q-293-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>Interrupts are not individually recorded in PEL. <a class="qa-rule-link" href="#common-interrupt_op-11">Full rule in this volume</a></p>
</li>
<li id="q-293-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>CLR invalidates I/O queues and their vector associations. <a class="qa-rule-link" href="#common-interrupt_op-12">Full rule in this volume</a></p>
</li>
<li id="q-293-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Rebuild affected queues, vector associations and settings after subsystem reset; a reused vector number does not preserve the old CQ lifetime. <a class="qa-rule-link" href="#common-interrupt_op-13">Full rule in this volume</a></p>
</li>
<li id="q-293-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Configure interrupt mode, queues and features after power cycle; mode changes also need not retain coalescing and reconfiguration is recommended. <a class="qa-rule-link" href="#common-interrupt_op-14">Full rule in this volume</a></p>
</li>
<li id="q-293-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>A shared vector’s mask/coalescing affects notifications for all associated CQs; equal vector numbers on different controllers do not identify one NVMe setting. <a class="qa-rule-link" href="#common-interrupt_op-15">Full rule in this volume</a></p>
</li>
<li id="q-293-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Preserve shared-CQ and mask state to isolate feature effects.</p>
</li>
<li id="q-293-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First identify which of CD, mask or CQ.IV is intended to change.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-interruptfull">PCIe Transport 1.4 §3.5–3.5.2 (interrupt delivery and masks), 3.8.4</a> · <a href="#ref-interruptmask">Base 2.4 §3.1.4 (INTMS, INTMC)</a> · <a href="#ref-interruptfeature">Base 2.4 §5.2.30.2.1–5.2.30.2.2</a> · <a href="#ref-create">Base 2.4 §5.3.1–5.3.2</a> · <a href="#ref-delete">Base 2.4 §5.3.3–5.3.4</a> · <a href="#ref-cqe">Base 2.4 §4.2.1, 4.2.3–4.2.4</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-294" data-question="294"><h2><a class="qa-qid" href="#q-294">Q294</a> How are interrupts restored after reset?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-294-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-294-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Queue associations end with queue lifetime; PCIe mode/mask retention depends on the reset source.</p>
</li>
<li id="q-294-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>One-controller reset differs from broader reset and does not justify reconfiguring unaffected controllers.</p>
</li>
<li id="q-294-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Inspect controller state, interrupt mode and feature current values.</p>
</li>
<li id="q-294-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>FID 08h resets to zero; default per-vector coalescing permission does not enable a disabled global aggregation policy.</p>
</li>
<li id="q-294-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Recover Admin access, vectors and queues before configuring per-vector/global aggregation.</p>
</li>
<li id="q-294-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>New completions are consumed through the rebuilt path without importing stale CQEs.</p>
</li>
<li id="q-294-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Setting FID 09h before rebuilding its CQ can violate the association prerequisite.</p>
</li>
<li id="q-294-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-294-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Completion interrupts and Asynchronous Event Requests are different mechanisms; an AER completion also uses a CQE, but an ordinary I/O interrupt is not an NVMe asynchronous event. <a class="qa-rule-link" href="#common-interrupt_op-9">Full rule in this volume</a></p>
</li>
<li id="q-294-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Normal configuration/delivery does not require an error entry. <a class="qa-rule-link" href="#common-interrupt_op-10">Full rule in this volume</a></p>
</li>
<li id="q-294-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>Interrupts are not individually recorded in PEL. <a class="qa-rule-link" href="#common-interrupt_op-11">Full rule in this volume</a></p>
</li>
<li id="q-294-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>CLR invalidates I/O queues and their vector associations. <a class="qa-rule-link" href="#common-interrupt_op-12">Full rule in this volume</a></p>
</li>
<li id="q-294-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Rebuild affected queues, vector associations and settings after subsystem reset; a reused vector number does not preserve the old CQ lifetime. <a class="qa-rule-link" href="#common-interrupt_op-13">Full rule in this volume</a></p>
</li>
<li id="q-294-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Configure interrupt mode, queues and features after power cycle; mode changes also need not retain coalescing and reconfiguration is recommended. <a class="qa-rule-link" href="#common-interrupt_op-14">Full rule in this volume</a></p>
</li>
<li id="q-294-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>A shared vector’s mask/coalescing affects notifications for all associated CQs; equal vector numbers on different controllers do not identify one NVMe setting. <a class="qa-rule-link" href="#common-interrupt_op-15">Full rule in this volume</a></p>
</li>
<li id="q-294-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Mode changes may lose aggregation settings; CC.EN testing does not establish power-cycle behavior.</p>
</li>
<li id="q-294-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First check reset type and successful new-CQ creation time.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-interruptfull">PCIe Transport 1.4 §3.5–3.5.2 (interrupt delivery and masks), 3.8.4</a> · <a href="#ref-interruptmask">Base 2.4 §3.1.4 (INTMS, INTMC)</a> · <a href="#ref-interruptfeature">Base 2.4 §5.2.30.2.1–5.2.30.2.2</a> · <a href="#ref-create">Base 2.4 §5.3.1–5.3.2</a> · <a href="#ref-delete">Base 2.4 §5.3.3–5.3.4</a> · <a href="#ref-cqe">Base 2.4 §4.2.1, 4.2.3–4.2.4</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-295" data-question="295"><h2><a class="qa-qid" href="#q-295">Q295</a> How are interrupt resources reclaimed after queue deletion?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-295-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-295-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>CQ deletion removes one completion destination, not the host-allocated PCIe vector itself.</p>
</li>
<li id="q-295-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Other CQs may still use the vector, requiring association-aware reclamation.</p>
</li>
<li id="q-295-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Preserve SQ-to-CQ-to-IV dependencies and outstanding commands.</p>
</li>
<li id="q-295-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>Delete dependent SQs and wait, then delete CQ and retire its host handling state.</p>
</li>
<li id="q-295-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Release the handler/vector only after checking remaining CQ users.</p>
</li>
<li id="q-295-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Deleting CQ1 leaves IV3 serving CQ2 when both shared it.</p>
</li>
<li id="q-295-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Referenced CQs cannot be deleted successfully, nor their memory reclaimed early.</p>
</li>
<li id="q-295-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-295-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Completion interrupts and Asynchronous Event Requests are different mechanisms; an AER completion also uses a CQE, but an ordinary I/O interrupt is not an NVMe asynchronous event. <a class="qa-rule-link" href="#common-interrupt_op-9">Full rule in this volume</a></p>
</li>
<li id="q-295-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Normal configuration/delivery does not require an error entry. <a class="qa-rule-link" href="#common-interrupt_op-10">Full rule in this volume</a></p>
</li>
<li id="q-295-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>Interrupts are not individually recorded in PEL. <a class="qa-rule-link" href="#common-interrupt_op-11">Full rule in this volume</a></p>
</li>
<li id="q-295-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>CLR invalidates I/O queues and their vector associations. <a class="qa-rule-link" href="#common-interrupt_op-12">Full rule in this volume</a></p>
</li>
<li id="q-295-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Rebuild affected queues, vector associations and settings after subsystem reset; a reused vector number does not preserve the old CQ lifetime. <a class="qa-rule-link" href="#common-interrupt_op-13">Full rule in this volume</a></p>
</li>
<li id="q-295-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Configure interrupt mode, queues and features after power cycle; mode changes also need not retain coalescing and reconfiguration is recommended. <a class="qa-rule-link" href="#common-interrupt_op-14">Full rule in this volume</a></p>
</li>
<li id="q-295-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>A shared vector’s mask/coalescing affects notifications for all associated CQs; equal vector numbers on different controllers do not identify one NVMe setting. <a class="qa-rule-link" href="#common-interrupt_op-15">Full rule in this volume</a></p>
</li>
<li id="q-295-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Correlate deletion completion, host membership and remaining notification paths.</p>
</li>
<li id="q-295-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First establish whether the vector is dedicated or shared.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-interruptfull">PCIe Transport 1.4 §3.5–3.5.2 (interrupt delivery and masks), 3.8.4</a> · <a href="#ref-interruptmask">Base 2.4 §3.1.4 (INTMS, INTMC)</a> · <a href="#ref-interruptfeature">Base 2.4 §5.2.30.2.1–5.2.30.2.2</a> · <a href="#ref-create">Base 2.4 §5.3.1–5.3.2</a> · <a href="#ref-delete">Base 2.4 §5.3.3–5.3.4</a> · <a href="#ref-cqe">Base 2.4 §4.2.1, 4.2.3–4.2.4</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-296" data-question="296"><h2><a class="qa-qid" href="#q-296">Q296</a> How are interrupt settings, CQ state and completions cross-checked?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-296-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-296-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Separating completion from notification distinguishes execution failures from delivery/consumption failures.</p>
</li>
<li id="q-296-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Follow a complete SQ-command-to-CQ-to-vector-to-handler path.</p>
</li>
<li id="q-296-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Inspect routing, aggregation, masks and phase.</p>
</li>
<li id="q-296-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>Preserve submission, CQE posting, notification and head-update times separately.</p>
</li>
<li id="q-296-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Establish a valid CQE, assess notification, then verify consumption and reclamation.</p>
</li>
<li id="q-296-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>A posted CQE consumed by polling while masked can be valid normal behavior.</p>
</li>
<li id="q-296-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Resolve wrong phase/CQ or missing head updates before diagnosing a lost command from absent interrupts.</p>
</li>
<li id="q-296-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-296-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Completion interrupts and Asynchronous Event Requests are different mechanisms; an AER completion also uses a CQE, but an ordinary I/O interrupt is not an NVMe asynchronous event. <a class="qa-rule-link" href="#common-interrupt_op-9">Full rule in this volume</a></p>
</li>
<li id="q-296-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Normal configuration/delivery does not require an error entry. <a class="qa-rule-link" href="#common-interrupt_op-10">Full rule in this volume</a></p>
</li>
<li id="q-296-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>Interrupts are not individually recorded in PEL. <a class="qa-rule-link" href="#common-interrupt_op-11">Full rule in this volume</a></p>
</li>
<li id="q-296-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>CLR invalidates I/O queues and their vector associations. <a class="qa-rule-link" href="#common-interrupt_op-12">Full rule in this volume</a></p>
</li>
<li id="q-296-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Rebuild affected queues, vector associations and settings after subsystem reset; a reused vector number does not preserve the old CQ lifetime. <a class="qa-rule-link" href="#common-interrupt_op-13">Full rule in this volume</a></p>
</li>
<li id="q-296-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Configure interrupt mode, queues and features after power cycle; mode changes also need not retain coalescing and reconfiguration is recommended. <a class="qa-rule-link" href="#common-interrupt_op-14">Full rule in this volume</a></p>
</li>
<li id="q-296-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>A shared vector’s mask/coalescing affects notifications for all associated CQs; equal vector numbers on different controllers do not identify one NVMe setting. <a class="qa-rule-link" href="#common-interrupt_op-15">Full rule in this volume</a></p>
</li>
<li id="q-296-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Correlate settings and observations from the same test interval.</p>
</li>
<li id="q-296-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First inspect the command’s CQ position and phase.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-interruptfull">PCIe Transport 1.4 §3.5–3.5.2 (interrupt delivery and masks), 3.8.4</a> · <a href="#ref-interruptmask">Base 2.4 §3.1.4 (INTMS, INTMC)</a> · <a href="#ref-interruptfeature">Base 2.4 §5.2.30.2.1–5.2.30.2.2</a> · <a href="#ref-create">Base 2.4 §5.3.1–5.3.2</a> · <a href="#ref-delete">Base 2.4 §5.3.3–5.3.4</a> · <a href="#ref-cqe">Base 2.4 §4.2.1, 4.2.3–4.2.4</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<section id="common-rules" class="qa-common"><h2>Shared rules linked from the answers</h2><p>Each shared mechanism is explained in full once in this volume. Use browser Back to return to the question; explicit command or feature exceptions take precedence.</p>
<article id="common-command-8"><h3>Command completion, events and records · How are DNR and More set?</h3><p>For a CQE, DNR=1 means the identical command is expected to fail if resubmitted to any controller in this subsystem; DNR=0 means it may succeed. Do not assign DNR=1 solely from an error name unless that condition mandates it. More=1 identifies additional information for this command in the Error Information Log. DNR should be zero when SCT=SC=0.</p></article>
<article id="common-interrupt_op-9"><h3>Shared conditions for this topic · Is an asynchronous event generated?</h3><p>Completion interrupts and Asynchronous Event Requests are different mechanisms; an AER completion also uses a CQE, but an ordinary I/O interrupt is not an NVMe asynchronous event.</p></article>
<article id="common-interrupt_op-10"><h3>Shared conditions for this topic · Are Error Information or other logs updated?</h3><p>Normal configuration/delivery does not require an error entry. Failed commands follow error rules; an unconsumed CQE does not automatically create a controller error entry.</p></article>
<article id="common-interrupt_op-11"><h3>Shared conditions for this topic · Is it recorded in the Persistent Event Log?</h3><p>Interrupts are not individually recorded in PEL. Feature changes follow FID-specific event rules, so PEL is not an interrupt counter.</p></article>
<article id="common-interrupt_op-12"><h3>Shared conditions for this topic · What survives or continues after Controller Reset?</h3><p>CLR invalidates I/O queues and their vector associations. FID 08h resets to zero and FID 09h defaults to coalescing allowed; PCIe masks/modes require reset-source-specific treatment.</p></article>
<article id="common-interrupt_op-13"><h3>Shared conditions for this topic · What survives or continues after NVM Subsystem Reset?</h3><p>Rebuild affected queues, vector associations and settings after subsystem reset; a reused vector number does not preserve the old CQ lifetime.</p></article>
<article id="common-interrupt_op-14"><h3>Shared conditions for this topic · What survives or continues after a power cycle?</h3><p>Configure interrupt mode, queues and features after power cycle; mode changes also need not retain coalescing and reconfiguration is recommended.</p></article>
<article id="common-interrupt_op-15"><h3>Shared conditions for this topic · Are other controllers or namespaces affected?</h3><p>A shared vector’s mask/coalescing affects notifications for all associated CQs; equal vector numbers on different controllers do not identify one NVMe setting.</p></article>
</section>
<section id="source-index"><h2>Source locations and existing figure guides</h2><p>Base printed page = PDF page−26; the other two use identical numbers. Locations follow the supplied PDF body and retain figure numbers. Shared pages contribute only the relevant definitions, excluding Fabrics and PCIe link/packet content.</p><ul class="qa-references">
<li id="ref-interruptmask"><strong>Base 2.4 · §3.1.4 (INTMS, INTMC)</strong><br>Printed pages 59 · PDF 85 · Figure 39–40</li>
<li id="ref-reset"><strong>Base 2.4 · §3.7.1–3.7.4</strong><br>Printed pages 120–124 · PDF 146–150</li>
<li id="ref-cqe"><strong>Base 2.4 · §4.2.1, 4.2.3–4.2.4</strong><br>Printed pages 144–157 · PDF 170–183 · Figure 97–105, 109</li>
<li id="ref-status"><strong>Base 2.4 · §4.2.3</strong><br>Printed pages 145–155 · PDF 171–181 · Figure 101–105</li>
<li id="ref-feature"><strong>Base 2.4 · §4.4</strong><br>Printed pages 166–169 · PDF 192–195 · Figure 126–127</li>
<li id="ref-aer"><strong>Base 2.4 · §5.2.2</strong><br>Printed pages 183–190 · PDF 209–216 · Figure 150–156</li>
<li id="ref-error"><strong>Base 2.4 · §5.2.13.1.2</strong><br>Printed pages 218–220 · PDF 244–246 · Figure 212</li>
<li id="ref-pel"><strong>Base 2.4 · §5.2.13.1.14 (header, reset, hardware, Set Feature events)</strong><br>Printed pages 244–256, 258, 262–264 · PDF 270–282, 284, 288–290 · Figure 232–244, 246, 252–253</li>
<li id="ref-setfeat"><strong>Base 2.4 · §5.2.30.1 (common fields, scope and persistence)</strong><br>Printed pages 456–460 · PDF 482–486 · Figure 463–466</li>
<li id="ref-interruptfeature"><strong>Base 2.4 · §5.2.30.2.1–5.2.30.2.2</strong><br>Printed pages 514–515 · PDF 540–541 · Figure 543–544</li>
<li id="ref-create"><strong>Base 2.4 · §5.3.1–5.3.2</strong><br>Printed pages 527–531 · PDF 553–557 · Figure 571–579</li>
<li id="ref-delete"><strong>Base 2.4 · §5.3.3–5.3.4</strong><br>Printed pages 531–532 · PDF 557–558 · Figure 580–583</li>
<li id="ref-interruptfull"><strong>PCIe Transport 1.4 · §3.5–3.5.2 (interrupt delivery and masks), 3.8.4</strong><br>Printed pages 13–16, 24–26 · PDF 13–16, 24–26 · Figure 9, 42–48</li>
</ul><h3>When you need a field guide</h3><p>Existing figure explanations have canonical locations; use these links instead of duplicating the same guide.</p><ul>
<li><a href="/nvme/figure-reference/command/en/#figure-b101">Base 2.4 Figure 101 · Completion Queue Entry: Status Field</a></li>
<li><a href="/nvme/figure-reference/command/en/#figure-b104">Base 2.4 Figure 104 · Status Code – Command Specific Status Values</a></li>
<li><a href="/nvme/figure-reference/features/en/#figure-b543">Base 2.4 Figure 543 · Interrupt Coalescing – Command Dword 11</a></li>
<li><a href="/nvme/figure-reference/command/en/#figure-b97">Base 2.4 Figure 97 · Common Completion Queue Entry Layout – Admin and All I/O Command Sets</a></li>
</ul><details><summary>Original documents used</summary><ul class="qr-sources">
<li>NVM Express Base Specification · Revision 2.4 · 2026-07-31<br><code>NVM-Express-Base-Specification-Revision-2.4-Ratified-2026.07.31.pdf</code></li>
<li>NVM Express NVM Command Set Specification · Revision 1.3 · 2026-07-31<br><code>NVM-Express-NVM-Command-Set-Specification-Revision-1.3-Ratified-2026.07.31.pdf</code></li>
<li>NVM Express NVMe over PCIe Transport Specification · Revision 1.4 · 2026-07-31<br><code>NVM-Express-NVMe-over-PCIe-Transport-Specification-Revision-1.4-Ratified-2026.07.31.pdf</code></li>
</ul></details></section>
</main>
<nav class="qr-top" aria-label="Bank and editions"><a href="#content">Skip to content</a><a href="/nvme/question-bank/en/">Question index</a><a href="/nvme/question-bank/interrupts/zh-tw/">繁體中文</a><a href="/DOCS/nvme-question-bank/interrupts.html">Chinese tutorial HTML</a></nav>
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
