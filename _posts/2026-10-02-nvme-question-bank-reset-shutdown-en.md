---
layout: post
title: "NVMe Self-Study Bank: Reset and shutdown"
date: 2026-10-02 00:00:00 +0800
categories: [nvme]
permalink: /nvme/question-bank/reset-shutdown/en/
lang: en
nvme_quickref: true
nvme_qa: true
---

<div class="nvme-quickref nvme-qa">
<nav class="qr-top" aria-label="Bank and editions"><a href="#content">Skip to content</a><a href="/nvme/question-bank/en/">Question index</a><a href="/nvme/question-bank/reset-shutdown/zh-tw/">繁體中文</a><a href="/DOCS/nvme-question-bank/reset-shutdown.html">Chinese tutorial HTML</a></nav>
<main id="content"><p class="qr-eyebrow">BASE 2.4 / NVM 1.3 / PCIe 1.4 · Q1–328</p>
<header><p class="qa-range">Q174–Q187</p><h1>Reset and shutdown</h1><p class="qr-intro">Reset rebuilds an operating context while shutdown prepares stopping; compare scope, completion and retained operations.</p><p>Practice first, then reveal 17 answer items per question. All numerical examples are hypothetical. Status is written SCT/SC; h indicates hexadecimal.</p></header>
<aside class="qa-glossary"><h2>Terms used in this volume</h2><dl><dt>Controller / namespace</dt><dd>A controller receives commands and manages access. A namespace is a logical storage space that commands can address. An NVM subsystem contains controllers and nonvolatile storage resources.</dd><dt>SQ / CQ / SQE / CQE</dt><dd>Submission and Completion Queues carry command entries (SQEs) and completion entries (CQEs). QID identifies a queue, CID distinguishes outstanding commands in one SQ, and NSID identifies a namespace.</dd><dt>Register / Identify / Feature / Log</dt><dd>A register exposes control or state. Identify queries capabilities and attributes; features query or configure operation; log pages report specific state or records. FID, LID, CNS and CSI select features, logs, Identify structures and command sets.</dd><dt>index / offset / zero-based</dt><dd>An index selects an entry, usually starting at 0; an offset measures distance from an origin in specified units. A zero-based count encodes count−1, but not every zero-valued field is a count. A Dword is 4 bytes; a byte is 8 bits.</dd><dt>Scope / reset / retention</dt><dd>Scope names the affected objects; retention means preserving state. Controller Reset (clearing CC.EN) is one form of Controller Level Reset, or CLR. Different CLR triggers can retain different registers.</dd></dl></aside>
<section id="overview" class="qa-overview"><h2>Requested stop versus completed stop</h2><p class="qa-takeaway">A host request is not device completion; inspect reported state.</p>
<div class="qr-table" tabindex="0" role="region" aria-label="Horizontally scrollable comparison table"><table><thead><tr><th scope="col">Action</th><th scope="col">Request</th><th scope="col">Follow-up</th></tr></thead><tbody><tr><td>Controller reset</td><td>CC.EN→0</td><td>Wait RDY0 and rebuild queues</td></tr><tr><td>Subsystem reset</td><td>Applicable reset interface</td><td>Recover affected controllers</td></tr><tr><td>Normal shutdown</td><td>CC.SHN=01b</td><td>Wait SHST10b and power-off scope</td></tr><tr><td>Abrupt shutdown</td><td>CC.SHN=10b</td><td>Still observe completion</td></tr></tbody></table></div>
<p><strong>Worked interpretation: </strong>Incomplete normal shutdown can qualify for UPL; completed abrupt shutdown need not. State at power loss matters.</p>
<p class="qa-citations">Sources: <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-shutdownfull">Base 2.4 §3.6–3.6.1 (memory-based scope and shutdown)</a> · <a href="#ref-pciereset">PCIe Transport 1.4 §3.3</a> · <a href="#ref-smart">Base 2.4 §5.2.13.1.3</a></p>
</section>
<div class="qa-controls" hidden><label>Search this page <input type="search" id="qa-search" placeholder="Question number, field or keyword"></label><button type="button" data-expand="true">Expand all answers</button><button type="button" data-expand="false">Collapse all answers</button><output id="qa-count" aria-live="polite"></output></div>
<section id="question-index"><h2>Questions in this volume</h2><ol class="qa-index">
<li><a href="#q-174">Q174 · How do controller, subsystem and queue resets differ?</a></li>
<li><a href="#q-175">Q175 · How do PCIe reset types affect NVMe?</a></li>
<li><a href="#q-176">Q176 · How do reset outcomes depend on ongoing activity?</a></li>
<li><a href="#q-177">Q177 · How does RDY behave during reset?</a></li>
<li><a href="#q-178">Q178 · What needs rebuilding after reset?</a></li>
<li><a href="#q-179">Q179 · How are old outstanding commands handled after reset?</a></li>
<li><a href="#q-180">Q180 · How is state revalidated after reset?</a></li>
<li><a href="#q-181">Q181 · What if reset times out or CFS remains?</a></li>
<li><a href="#q-182">Q182 · How is normal shutdown requested?</a></li>
<li><a href="#q-183">Q183 · When is power removal appropriate?</a></li>
<li><a href="#q-184">Q184 · How do normal, abrupt and unannounced loss differ?</a></li>
<li><a href="#q-185">Q185 · What may remain outstanding during shutdown?</a></li>
<li><a href="#q-186">Q186 · How do shutdown modes affect the former Unsafe Shutdowns counter?</a></li>
<li><a href="#q-187">Q187 · Why inspect health, errors and persistent events after loss?</a></li>
</ol></section>
<article class="qa-question" id="q-174" data-question="174"><h2><a class="qa-qid" href="#q-174">Q174</a> How do controller, subsystem and queue resets differ?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-174-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-174-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Choose recovery scope with known impact on ongoing work.</p>
</li>
<li id="q-174-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Queue reset recreates selected I/O queues; CLR resets a controller; subsystem reset covers its defined domains.</p>
</li>
<li id="q-174-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Check NSSRS, domain topology and queue dependencies.</p>
</li>
<li id="q-174-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>Use Delete/Create, clear CC.EN or write 4E564D65h to supported NSSR respectively.</p>
</li>
<li id="q-174-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Quiesce, reset/rebuild and resume, respecting SQ/CQ dependencies.</p>
</li>
<li id="q-174-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Recovered resources begin a new valid lifetime.</p>
</li>
<li id="q-174-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Register reset has no CQE; queue-management commands do.</p>
</li>
<li id="q-174-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Queue-reset Delete/Create commands have CQEs; CC.EN/NSSR register accesses do not. DNR/More therefore apply only to the command completions.</p>
</li>
<li id="q-174-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Register access has no success event; separate hardware errors use their event conditions. <a class="qa-rule-link" href="#common-register-9">Full rule in this volume</a></p>
</li>
<li id="q-174-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Register accesses are not logged individually; preserve registers and timing before obtaining available diagnostics. <a class="qa-rule-link" href="#common-register-10">Full rule in this volume</a></p>
</li>
<li id="q-174-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>Ordinary register access is not a PEL event; completed resets and supported hardware errors are assessed separately. <a class="qa-rule-link" href="#common-register-11">Full rule in this volume</a></p>
</li>
<li id="q-174-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Clearing CC.EN invalidates I/O queues and resets Admin pointers; retained base addresses do not validate old completions. <a class="qa-rule-link" href="#common-queue-12">Full rule in this volume</a></p>
</li>
<li id="q-174-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Rebuild affected-controller queues; do not assume CC.EN-reset register-retention exceptions. <a class="qa-rule-link" href="#common-queue-13">Full rule in this volume</a></p>
</li>
<li id="q-174-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Initialize queues and host tracking again; residual memory is not valid command state for a new lifetime. <a class="qa-rule-link" href="#common-queue-14">Full rule in this volume</a></p>
</li>
<li id="q-174-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Controller Reset targets one controller; subsystem reset covers one/all domains as defined for the implementation. <a class="qa-rule-link" href="#common-reset_review-15">Full rule in this volume</a></p>
</li>
<li id="q-174-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Verify affected resources rather than host function names.</p>
</li>
<li id="q-174-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First identify the actual reset mechanism.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-cc">Base 2.4 §3.1.4 (CC, CSTS, NSSR)</a> · <a href="#ref-shutdownfull">Base 2.4 §3.6–3.6.1 (memory-based scope and shutdown)</a> · <a href="#ref-pciereset">PCIe Transport 1.4 §3.3</a> · <a href="#ref-smart">Base 2.4 §5.2.13.1.3</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-175" data-question="175"><h2><a class="qa-qid" href="#q-175">Q175</a> How do PCIe reset types affect NVMe?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-175-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-175-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Focus on NVMe-visible effects; reset source changes retention and activation.</p>
</li>
<li id="q-175-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>FLR is function-level; Conventional Reset includes Hot/Fundamental forms, with topology determining affected controllers.</p>
</li>
<li id="q-175-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Check reset support, CAP and pending firmware requirements.</p>
</li>
<li id="q-175-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>Conventional/FLR initiate CLR; CC.EN reset does not reset PCI configuration space.</p>
</li>
<li id="q-175-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Record source, restore applicable PCI configuration and initialize NVMe.</p>
</li>
<li id="q-175-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Rebuild affected queues; FLR does not preserve I/O queues.</p>
</li>
<li id="q-175-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>FLR/CC.EN do not satisfy a required Conventional Reset.</p>
</li>
<li id="q-175-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>This MMIO access has no NVMe CQE, so DNR/More do not apply. <a class="qa-rule-link" href="#common-register-8">Full rule in this volume</a></p>
</li>
<li id="q-175-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Register access has no success event; separate hardware errors use their event conditions. <a class="qa-rule-link" href="#common-register-9">Full rule in this volume</a></p>
</li>
<li id="q-175-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Register accesses are not logged individually; preserve registers and timing before obtaining available diagnostics. <a class="qa-rule-link" href="#common-register-10">Full rule in this volume</a></p>
</li>
<li id="q-175-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>Ordinary register access is not a PEL event; completed resets and supported hardware errors are assessed separately. <a class="qa-rule-link" href="#common-register-11">Full rule in this volume</a></p>
</li>
<li id="q-175-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Clearing CC.EN invalidates I/O queues and resets Admin pointers; retained base addresses do not validate old completions. <a class="qa-rule-link" href="#common-queue-12">Full rule in this volume</a></p>
</li>
<li id="q-175-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Rebuild affected-controller queues; do not assume CC.EN-reset register-retention exceptions. <a class="qa-rule-link" href="#common-queue-13">Full rule in this volume</a></p>
</li>
<li id="q-175-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Initialize queues and host tracking again; residual memory is not valid command state for a new lifetime. <a class="qa-rule-link" href="#common-queue-14">Full rule in this volume</a></p>
</li>
<li id="q-175-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Controller Reset targets one controller; subsystem reset covers one/all domains as defined for the implementation. <a class="qa-rule-link" href="#common-reset_review-15">Full rule in this volume</a></p>
</li>
<li id="q-175-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Respect exceptions such as CMBMSC retention under FLR.</p>
</li>
<li id="q-175-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First identify the actual reset source.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-cc">Base 2.4 §3.1.4 (CC, CSTS, NSSR)</a> · <a href="#ref-shutdownfull">Base 2.4 §3.6–3.6.1 (memory-based scope and shutdown)</a> · <a href="#ref-pciereset">PCIe Transport 1.4 §3.3</a> · <a href="#ref-smart">Base 2.4 §5.2.13.1.3</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-176" data-question="176"><h2><a class="qa-qid" href="#q-176">Q176</a> How do reset outcomes depend on ongoing activity?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-176-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-176-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Channels and background operations can have different reset behavior.</p>
</li>
<li id="q-176-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Queues end while data/management state follow specific rules.</p>
</li>
<li id="q-176-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Snapshot outstanding work, logs and reset source.</p>
</li>
<li id="q-176-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>Sanitize continues, short tests abort, extended tests resume and uncommitted staging is discarded.</p>
</li>
<li id="q-176-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Record stage and reread state instead of stale CQE bytes.</p>
</li>
<li id="q-176-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Classify each operation as complete, stopped, continuing or unresolved.</p>
</li>
<li id="q-176-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Missing CQE does not prove no execution or rollback.</p>
</li>
<li id="q-176-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>This MMIO access has no NVMe CQE, so DNR/More do not apply. <a class="qa-rule-link" href="#common-register-8">Full rule in this volume</a></p>
</li>
<li id="q-176-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Register access has no success event; separate hardware errors use their event conditions. <a class="qa-rule-link" href="#common-register-9">Full rule in this volume</a></p>
</li>
<li id="q-176-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Register accesses are not logged individually; preserve registers and timing before obtaining available diagnostics. <a class="qa-rule-link" href="#common-register-10">Full rule in this volume</a></p>
</li>
<li id="q-176-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>Ordinary register access is not a PEL event; completed resets and supported hardware errors are assessed separately. <a class="qa-rule-link" href="#common-register-11">Full rule in this volume</a></p>
</li>
<li id="q-176-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Clearing CC.EN invalidates I/O queues and resets Admin pointers; retained base addresses do not validate old completions. <a class="qa-rule-link" href="#common-queue-12">Full rule in this volume</a></p>
</li>
<li id="q-176-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Rebuild affected-controller queues; do not assume CC.EN-reset register-retention exceptions. <a class="qa-rule-link" href="#common-queue-13">Full rule in this volume</a></p>
</li>
<li id="q-176-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Initialize queues and host tracking again; residual memory is not valid command state for a new lifetime. <a class="qa-rule-link" href="#common-queue-14">Full rule in this volume</a></p>
</li>
<li id="q-176-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Controller Reset targets one controller; subsystem reset covers one/all domains as defined for the implementation. <a class="qa-rule-link" href="#common-reset_review-15">Full rule in this volume</a></p>
</li>
<li id="q-176-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Apply per-function persistence.</p>
</li>
<li id="q-176-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First distinguish the command from its background work.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-sanitizecmd">Base 2.4 §5.2.26–5.2.27</a> · <a href="#ref-selftest">Base 2.4 §5.2.6, 8.1.8</a> · <a href="#ref-firmware">Base 2.4 §3.11–3.11.1, 5.2.9–5.2.10</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-cc">Base 2.4 §3.1.4 (CC, CSTS, NSSR)</a> · <a href="#ref-shutdownfull">Base 2.4 §3.6–3.6.1 (memory-based scope and shutdown)</a> · <a href="#ref-pciereset">PCIe Transport 1.4 §3.3</a> · <a href="#ref-smart">Base 2.4 §5.2.13.1.3</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-177" data-question="177"><h2><a class="qa-qid" href="#q-177">Q177</a> How does RDY behave during reset?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-177-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-177-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>RDY confirms disable/readiness, not just EN writes.</p>
</li>
<li id="q-177-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>RDY is controller state, not universal namespace readiness.</p>
</li>
<li id="q-177-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Read CAP.TO and ready-mode/CRTO capabilities.</p>
</li>
<li id="q-177-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>Wait RDY0 after disable and RDY1 after enable with proper deadlines.</p>
</li>
<li id="q-177-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Complete disable/configuration before re-enabling.</p>
</li>
<li id="q-177-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Transitions and media restrictions follow the selected mode.</p>
</li>
<li id="q-177-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>An inaccessible register is not RDY0 evidence.</p>
</li>
<li id="q-177-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>This MMIO access has no NVMe CQE, so DNR/More do not apply. <a class="qa-rule-link" href="#common-register-8">Full rule in this volume</a></p>
</li>
<li id="q-177-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Register access has no success event; separate hardware errors use their event conditions. <a class="qa-rule-link" href="#common-register-9">Full rule in this volume</a></p>
</li>
<li id="q-177-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Register accesses are not logged individually; preserve registers and timing before obtaining available diagnostics. <a class="qa-rule-link" href="#common-register-10">Full rule in this volume</a></p>
</li>
<li id="q-177-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>Ordinary register access is not a PEL event; completed resets and supported hardware errors are assessed separately. <a class="qa-rule-link" href="#common-register-11">Full rule in this volume</a></p>
</li>
<li id="q-177-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Clearing CC.EN invalidates I/O queues and resets Admin pointers; retained base addresses do not validate old completions. <a class="qa-rule-link" href="#common-queue-12">Full rule in this volume</a></p>
</li>
<li id="q-177-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Rebuild affected-controller queues; do not assume CC.EN-reset register-retention exceptions. <a class="qa-rule-link" href="#common-queue-13">Full rule in this volume</a></p>
</li>
<li id="q-177-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Initialize queues and host tracking again; residual memory is not valid command state for a new lifetime. <a class="qa-rule-link" href="#common-queue-14">Full rule in this volume</a></p>
</li>
<li id="q-177-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Controller Reset targets one controller; subsystem reset covers one/all domains as defined for the implementation. <a class="qa-rule-link" href="#common-reset_review-15">Full rule in this volume</a></p>
</li>
<li id="q-177-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Correlate request and acknowledgment with timing.</p>
</li>
<li id="q-177-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First exclude failed-access fill values.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-cap">Base 2.4 §3.1.4 (CAP, VS)</a> · <a href="#ref-crto">Base 2.4 §3.1.4 (CRTO)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-cc">Base 2.4 §3.1.4 (CC, CSTS, NSSR)</a> · <a href="#ref-shutdownfull">Base 2.4 §3.6–3.6.1 (memory-based scope and shutdown)</a> · <a href="#ref-pciereset">PCIe Transport 1.4 §3.3</a> · <a href="#ref-smart">Base 2.4 §5.2.13.1.3</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-178" data-question="178"><h2><a class="qa-qid" href="#q-178">Q178</a> What needs rebuilding after reset?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-178-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-178-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Rebuild by reset source and feature rules.</p>
</li>
<li id="q-178-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Queues/pointers reset separately from persistent configuration.</p>
</li>
<li id="q-178-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Check retention exceptions, features and queue allocation.</p>
</li>
<li id="q-178-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>CC.EN reset preserves specified registers, not queue pointers.</p>
</li>
<li id="q-178-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Restore transport/registers, initialize phase, enable/wait, configure and recreate queues.</p>
</li>
<li id="q-178-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>New queues work and features restore correctly.</p>
</li>
<li id="q-178-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Retained addresses do not validate CQEs; non-saveable is not necessarily zero.</p>
</li>
<li id="q-178-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>This MMIO access has no NVMe CQE, so DNR/More do not apply. <a class="qa-rule-link" href="#common-register-8">Full rule in this volume</a></p>
</li>
<li id="q-178-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Register access has no success event; separate hardware errors use their event conditions. <a class="qa-rule-link" href="#common-register-9">Full rule in this volume</a></p>
</li>
<li id="q-178-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Register accesses are not logged individually; preserve registers and timing before obtaining available diagnostics. <a class="qa-rule-link" href="#common-register-10">Full rule in this volume</a></p>
</li>
<li id="q-178-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>Ordinary register access is not a PEL event; completed resets and supported hardware errors are assessed separately. <a class="qa-rule-link" href="#common-register-11">Full rule in this volume</a></p>
</li>
<li id="q-178-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Clearing CC.EN invalidates I/O queues and resets Admin pointers; retained base addresses do not validate old completions. <a class="qa-rule-link" href="#common-queue-12">Full rule in this volume</a></p>
</li>
<li id="q-178-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Rebuild affected-controller queues; do not assume CC.EN-reset register-retention exceptions. <a class="qa-rule-link" href="#common-queue-13">Full rule in this volume</a></p>
</li>
<li id="q-178-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Initialize queues and host tracking again; residual memory is not valid command state for a new lifetime. <a class="qa-rule-link" href="#common-queue-14">Full rule in this volume</a></p>
</li>
<li id="q-178-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Controller Reset targets one controller; subsystem reset covers one/all domains as defined for the implementation. <a class="qa-rule-link" href="#common-reset_review-15">Full rule in this volume</a></p>
</li>
<li id="q-178-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Compare values and exceptions rather than blanket zeroing.</p>
</li>
<li id="q-178-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>Establish reset source first.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-adminreg">Base 2.4 §3.1.4 (AQA, ASQ, ACQ, CMBLOC)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-cc">Base 2.4 §3.1.4 (CC, CSTS, NSSR)</a> · <a href="#ref-shutdownfull">Base 2.4 §3.6–3.6.1 (memory-based scope and shutdown)</a> · <a href="#ref-pciereset">PCIe Transport 1.4 §3.3</a> · <a href="#ref-smart">Base 2.4 §5.2.13.1.3</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-179" data-question="179"><h2><a class="qa-qid" href="#q-179">Q179</a> How are old outstanding commands handled after reset?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-179-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-179-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Prevent stale-CID confusion and late effects.</p>
</li>
<li id="q-179-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Separate lifetimes, including cross-controller recovery.</p>
</li>
<li id="q-179-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Preserve reset and old-command evidence.</p>
</li>
<li id="q-179-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>Reinitialize phase/pointers, ignoring old-generation CQEs.</p>
</li>
<li id="q-179-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Establish termination before reclamation or mutating retries.</p>
</li>
<li id="q-179-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>New commands use new results; assess prior data effects separately.</p>
</li>
<li id="q-179-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Lost communication precludes a universal abort-CQE requirement.</p>
</li>
<li id="q-179-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>This MMIO access has no NVMe CQE, so DNR/More do not apply. <a class="qa-rule-link" href="#common-register-8">Full rule in this volume</a></p>
</li>
<li id="q-179-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Register access has no success event; separate hardware errors use their event conditions. <a class="qa-rule-link" href="#common-register-9">Full rule in this volume</a></p>
</li>
<li id="q-179-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Register accesses are not logged individually; preserve registers and timing before obtaining available diagnostics. <a class="qa-rule-link" href="#common-register-10">Full rule in this volume</a></p>
</li>
<li id="q-179-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>Ordinary register access is not a PEL event; completed resets and supported hardware errors are assessed separately. <a class="qa-rule-link" href="#common-register-11">Full rule in this volume</a></p>
</li>
<li id="q-179-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Clearing CC.EN invalidates I/O queues and resets Admin pointers; retained base addresses do not validate old completions. <a class="qa-rule-link" href="#common-queue-12">Full rule in this volume</a></p>
</li>
<li id="q-179-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Rebuild affected-controller queues; do not assume CC.EN-reset register-retention exceptions. <a class="qa-rule-link" href="#common-queue-13">Full rule in this volume</a></p>
</li>
<li id="q-179-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Initialize queues and host tracking again; residual memory is not valid command state for a new lifetime. <a class="qa-rule-link" href="#common-queue-14">Full rule in this volume</a></p>
</li>
<li id="q-179-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Controller Reset targets one controller; subsystem reset covers one/all domains as defined for the implementation. <a class="qa-rule-link" href="#common-reset_review-15">Full rule in this volume</a></p>
</li>
<li id="q-179-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Distinguish fresh writes from residual bytes.</p>
</li>
<li id="q-179-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>Inspect phase and CID reuse first.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-commrecovery">Base 2.4 §9.1–9.6.2.1 (PCIe-applicable rules; stop before 9.6.2.2)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-cc">Base 2.4 §3.1.4 (CC, CSTS, NSSR)</a> · <a href="#ref-shutdownfull">Base 2.4 §3.6–3.6.1 (memory-based scope and shutdown)</a> · <a href="#ref-pciereset">PCIe Transport 1.4 §3.3</a> · <a href="#ref-smart">Base 2.4 §5.2.13.1.3</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-180" data-question="180"><h2><a class="qa-qid" href="#q-180">Q180</a> How is state revalidated after reset?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-180-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-180-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>RDY1 alone does not establish restored settings or background state.</p>
</li>
<li id="q-180-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Query each defined scope.</p>
</li>
<li id="q-180-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Use supported discovery interfaces.</p>
</li>
<li id="q-180-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>Inspect feature values, namespace lists, firmware and operation logs.</p>
</li>
<li id="q-180-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Discover state before resuming correctly configured I/O.</p>
</li>
<li id="q-180-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Explain differences such as continued sanitization with invalidated AERs.</p>
</li>
<li id="q-180-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Cleared entries and retained counters can both conform.</p>
</li>
<li id="q-180-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>This MMIO access has no NVMe CQE, so DNR/More do not apply. <a class="qa-rule-link" href="#common-register-8">Full rule in this volume</a></p>
</li>
<li id="q-180-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Register access has no success event; separate hardware errors use their event conditions. <a class="qa-rule-link" href="#common-register-9">Full rule in this volume</a></p>
</li>
<li id="q-180-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Register accesses are not logged individually; preserve registers and timing before obtaining available diagnostics. <a class="qa-rule-link" href="#common-register-10">Full rule in this volume</a></p>
</li>
<li id="q-180-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>Ordinary register access is not a PEL event; completed resets and supported hardware errors are assessed separately. <a class="qa-rule-link" href="#common-register-11">Full rule in this volume</a></p>
</li>
<li id="q-180-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Clearing CC.EN invalidates I/O queues and resets Admin pointers; retained base addresses do not validate old completions. <a class="qa-rule-link" href="#common-queue-12">Full rule in this volume</a></p>
</li>
<li id="q-180-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Rebuild affected-controller queues; do not assume CC.EN-reset register-retention exceptions. <a class="qa-rule-link" href="#common-queue-13">Full rule in this volume</a></p>
</li>
<li id="q-180-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Initialize queues and host tracking again; residual memory is not valid command state for a new lifetime. <a class="qa-rule-link" href="#common-queue-14">Full rule in this volume</a></p>
</li>
<li id="q-180-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Controller Reset targets one controller; subsystem reset covers one/all domains as defined for the implementation. <a class="qa-rule-link" href="#common-reset_review-15">Full rule in this volume</a></p>
</li>
<li id="q-180-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Compare persistent, restored and live fields appropriately.</p>
</li>
<li id="q-180-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>Avoid generalizing one empty log to all history.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-firmware">Base 2.4 §3.11–3.11.1, 5.2.9–5.2.10</a> · <a href="#ref-sanitizelog">Base 2.4 §5.2.13.1.38</a> · <a href="#ref-dstlog">Base 2.4 §5.2.13.1.7</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-cc">Base 2.4 §3.1.4 (CC, CSTS, NSSR)</a> · <a href="#ref-shutdownfull">Base 2.4 §3.6–3.6.1 (memory-based scope and shutdown)</a> · <a href="#ref-pciereset">PCIe Transport 1.4 §3.3</a> · <a href="#ref-smart">Base 2.4 §5.2.13.1.3</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-181" data-question="181"><h2><a class="qa-qid" href="#q-181">Q181</a> What if reset times out or CFS remains?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-181-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-181-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Distinguish a wrong deadline from persistent failure.</p>
</li>
<li id="q-181-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Start locally and assess broader impact.</p>
</li>
<li id="q-181-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Preserve capability/state/source/timing.</p>
</li>
<li id="q-181-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>Apply the correct deadlines and fatal-recovery rules.</p>
</li>
<li id="q-181-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Validate readings, reset controller and consider subsystem reset if appropriate.</p>
</li>
<li id="q-181-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Recovery includes usable channels, not only cleared CFS.</p>
</li>
<li id="q-181-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Avoid unjustified short deadlines or unsuitable subsystem resets.</p>
</li>
<li id="q-181-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>This MMIO access has no NVMe CQE, so DNR/More do not apply. <a class="qa-rule-link" href="#common-register-8">Full rule in this volume</a></p>
</li>
<li id="q-181-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Register access has no success event; separate hardware errors use their event conditions. <a class="qa-rule-link" href="#common-register-9">Full rule in this volume</a></p>
</li>
<li id="q-181-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Register accesses are not logged individually; preserve registers and timing before obtaining available diagnostics. <a class="qa-rule-link" href="#common-register-10">Full rule in this volume</a></p>
</li>
<li id="q-181-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>Ordinary register access is not a PEL event; completed resets and supported hardware errors are assessed separately. <a class="qa-rule-link" href="#common-register-11">Full rule in this volume</a></p>
</li>
<li id="q-181-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Clearing CC.EN invalidates I/O queues and resets Admin pointers; retained base addresses do not validate old completions. <a class="qa-rule-link" href="#common-queue-12">Full rule in this volume</a></p>
</li>
<li id="q-181-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Rebuild affected-controller queues; do not assume CC.EN-reset register-retention exceptions. <a class="qa-rule-link" href="#common-queue-13">Full rule in this volume</a></p>
</li>
<li id="q-181-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Initialize queues and host tracking again; residual memory is not valid command state for a new lifetime. <a class="qa-rule-link" href="#common-queue-14">Full rule in this volume</a></p>
</li>
<li id="q-181-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Controller Reset targets one controller; subsystem reset covers one/all domains as defined for the implementation. <a class="qa-rule-link" href="#common-reset_review-15">Full rule in this volume</a></p>
</li>
<li id="q-181-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Exclude expected Offline-secondary CFS.</p>
</li>
<li id="q-181-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>Verify deadline and role first.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-fatal">Base 2.4 §9.1–9.6.1</a> · <a href="#ref-cap">Base 2.4 §3.1.4 (CAP, VS)</a> · <a href="#ref-crto">Base 2.4 §3.1.4 (CRTO)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-cc">Base 2.4 §3.1.4 (CC, CSTS, NSSR)</a> · <a href="#ref-shutdownfull">Base 2.4 §3.6–3.6.1 (memory-based scope and shutdown)</a> · <a href="#ref-pciereset">PCIe Transport 1.4 §3.3</a> · <a href="#ref-smart">Base 2.4 §5.2.13.1.3</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-182" data-question="182"><h2><a class="qa-qid" href="#q-182">Q182</a> How is normal shutdown requested?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-182-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-182-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Normal shutdown prepares media, unlike disable.</p>
</li>
<li id="q-182-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Coordinate controllers in CAP.CPS power scope.</p>
</li>
<li id="q-182-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Read power scope, latency and shutdown status.</p>
</li>
<li id="q-182-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>SHN01b requests normal shutdown; SHST10b/ST0 confirms it.</p>
</li>
<li id="q-182-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Quiesce/drain, delete SQs then CQs, request shutdown and wait.</p>
</li>
<li id="q-182-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Readiness persists until a defined state-changing event.</p>
</li>
<li id="q-182-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>SHN has no CQE; commands may be aborted for power-loss notification.</p>
</li>
<li id="q-182-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>This MMIO access has no NVMe CQE, so DNR/More do not apply. <a class="qa-rule-link" href="#common-register-8">Full rule in this volume</a></p>
</li>
<li id="q-182-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Register access has no success event; separate hardware errors use their event conditions. <a class="qa-rule-link" href="#common-register-9">Full rule in this volume</a></p>
</li>
<li id="q-182-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Register accesses are not logged individually; preserve registers and timing before obtaining available diagnostics. <a class="qa-rule-link" href="#common-register-10">Full rule in this volume</a></p>
</li>
<li id="q-182-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>Ordinary register access is not a PEL event; completed resets and supported hardware errors are assessed separately. <a class="qa-rule-link" href="#common-register-11">Full rule in this volume</a></p>
</li>
<li id="q-182-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Clearing CC.EN invalidates I/O queues and resets Admin pointers; retained base addresses do not validate old completions. <a class="qa-rule-link" href="#common-queue-12">Full rule in this volume</a></p>
</li>
<li id="q-182-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Rebuild affected-controller queues; do not assume CC.EN-reset register-retention exceptions. <a class="qa-rule-link" href="#common-queue-13">Full rule in this volume</a></p>
</li>
<li id="q-182-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Initialize queues and host tracking again; residual memory is not valid command state for a new lifetime. <a class="qa-rule-link" href="#common-queue-14">Full rule in this volume</a></p>
</li>
<li id="q-182-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Controller Reset targets one controller; subsystem reset covers one/all domains as defined for the implementation. <a class="qa-rule-link" href="#common-reset_review-15">Full rule in this volume</a></p>
</li>
<li id="q-182-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Verify acknowledgment rather than request alone.</p>
</li>
<li id="q-182-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>Exclude disable-as-shutdown first.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-cc">Base 2.4 §3.1.4 (CC, CSTS, NSSR)</a> · <a href="#ref-shutdownfull">Base 2.4 §3.6–3.6.1 (memory-based scope and shutdown)</a> · <a href="#ref-pciereset">PCIe Transport 1.4 §3.3</a> · <a href="#ref-smart">Base 2.4 §5.2.13.1.3</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-183" data-question="183"><h2><a class="qa-qid" href="#q-183">Q183</a> When is power removal appropriate?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-183-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-183-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Notification is not completed preparation.</p>
</li>
<li id="q-183-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>All controllers in the power scope must be ready.</p>
</li>
<li id="q-183-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Inspect status, scope and latency guidance.</p>
</li>
<li id="q-183-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>SHST01b/10b mean processing/complete with ST0 for controller shutdown.</p>
</li>
<li id="q-183-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Poll completion; the one-second guidance for RTD3E0 is not unconditional removal permission.</p>
</li>
<li id="q-183-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Establish readiness across the required scope.</p>
</li>
<li id="q-183-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Later reset/media access can invalidate readiness.</p>
</li>
<li id="q-183-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>This MMIO access has no NVMe CQE, so DNR/More do not apply. <a class="qa-rule-link" href="#common-register-8">Full rule in this volume</a></p>
</li>
<li id="q-183-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Register access has no success event; separate hardware errors use their event conditions. <a class="qa-rule-link" href="#common-register-9">Full rule in this volume</a></p>
</li>
<li id="q-183-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Register accesses are not logged individually; preserve registers and timing before obtaining available diagnostics. <a class="qa-rule-link" href="#common-register-10">Full rule in this volume</a></p>
</li>
<li id="q-183-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>Ordinary register access is not a PEL event; completed resets and supported hardware errors are assessed separately. <a class="qa-rule-link" href="#common-register-11">Full rule in this volume</a></p>
</li>
<li id="q-183-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Clearing CC.EN invalidates I/O queues and resets Admin pointers; retained base addresses do not validate old completions. <a class="qa-rule-link" href="#common-queue-12">Full rule in this volume</a></p>
</li>
<li id="q-183-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Rebuild affected-controller queues; do not assume CC.EN-reset register-retention exceptions. <a class="qa-rule-link" href="#common-queue-13">Full rule in this volume</a></p>
</li>
<li id="q-183-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Initialize queues and host tracking again; residual memory is not valid command state for a new lifetime. <a class="qa-rule-link" href="#common-queue-14">Full rule in this volume</a></p>
</li>
<li id="q-183-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Controller Reset targets one controller; subsystem reset covers one/all domains as defined for the implementation. <a class="qa-rule-link" href="#common-reset_review-15">Full rule in this volume</a></p>
</li>
<li id="q-183-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Correlate latest state with actual loss.</p>
</li>
<li id="q-183-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>Check multi-controller power scope first.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-cap">Base 2.4 §3.1.4 (CAP, VS)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-cc">Base 2.4 §3.1.4 (CC, CSTS, NSSR)</a> · <a href="#ref-shutdownfull">Base 2.4 §3.6–3.6.1 (memory-based scope and shutdown)</a> · <a href="#ref-pciereset">PCIe Transport 1.4 §3.3</a> · <a href="#ref-smart">Base 2.4 §5.2.13.1.3</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-184" data-question="184"><h2><a class="qa-qid" href="#q-184">Q184</a> How do normal, abrupt and unannounced loss differ?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-184-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-184-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Both shutdown types notify; unannounced loss may not.</p>
</li>
<li id="q-184-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Work/persistence opportunities differ within the required power scope.</p>
</li>
<li id="q-184-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Preserve shutdown, power and counter evidence.</p>
</li>
<li id="q-184-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>Both modes report completion through SHST10b.</p>
</li>
<li id="q-184-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Normal drains/deletes; abrupt stops new I/O/notifies; sudden loss cannot wait.</p>
</li>
<li id="q-184-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Ready abrupt shutdown does not increment UPL merely by name.</p>
</li>
<li id="q-184-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Procedure names do not guarantee outstanding-write persistence.</p>
</li>
<li id="q-184-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>This MMIO access has no NVMe CQE, so DNR/More do not apply. <a class="qa-rule-link" href="#common-register-8">Full rule in this volume</a></p>
</li>
<li id="q-184-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Register access has no success event; separate hardware errors use their event conditions. <a class="qa-rule-link" href="#common-register-9">Full rule in this volume</a></p>
</li>
<li id="q-184-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Register accesses are not logged individually; preserve registers and timing before obtaining available diagnostics. <a class="qa-rule-link" href="#common-register-10">Full rule in this volume</a></p>
</li>
<li id="q-184-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>Ordinary register access is not a PEL event; completed resets and supported hardware errors are assessed separately. <a class="qa-rule-link" href="#common-register-11">Full rule in this volume</a></p>
</li>
<li id="q-184-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Clearing CC.EN invalidates I/O queues and resets Admin pointers; retained base addresses do not validate old completions. <a class="qa-rule-link" href="#common-queue-12">Full rule in this volume</a></p>
</li>
<li id="q-184-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Rebuild affected-controller queues; do not assume CC.EN-reset register-retention exceptions. <a class="qa-rule-link" href="#common-queue-13">Full rule in this volume</a></p>
</li>
<li id="q-184-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Initialize queues and host tracking again; residual memory is not valid command state for a new lifetime. <a class="qa-rule-link" href="#common-queue-14">Full rule in this volume</a></p>
</li>
<li id="q-184-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Controller Reset targets one controller; subsystem reset covers one/all domains as defined for the implementation. <a class="qa-rule-link" href="#common-reset_review-15">Full rule in this volume</a></p>
</li>
<li id="q-184-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Observe request, completion and actual loss.</p>
</li>
<li id="q-184-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>Inspect state at loss first.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-cc">Base 2.4 §3.1.4 (CC, CSTS, NSSR)</a> · <a href="#ref-shutdownfull">Base 2.4 §3.6–3.6.1 (memory-based scope and shutdown)</a> · <a href="#ref-pciereset">PCIe Transport 1.4 §3.3</a> · <a href="#ref-smart">Base 2.4 §5.2.13.1.3</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-185" data-question="185"><h2><a class="qa-qid" href="#q-185">Q185</a> What may remain outstanding during shutdown?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-185-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-185-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Continued I/O obstructs orderly shutdown.</p>
</li>
<li id="q-185-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Pending AERs are not pending data writes.</p>
</li>
<li id="q-185-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Inspect command tracking and shutdown state.</p>
</li>
<li id="q-185-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>Drain I/O; Admin abortion is host policy, with only AERs recommended outstanding at completion.</p>
</li>
<li id="q-185-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Quiesce/process results, request shutdown and avoid disrupting it with EN clearing.</p>
</li>
<li id="q-185-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Complete shutdown can coexist with pending AERs.</p>
</li>
<li id="q-185-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Late commands may be aborted for power-loss notification.</p>
</li>
<li id="q-185-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>This MMIO access has no NVMe CQE, so DNR/More do not apply. <a class="qa-rule-link" href="#common-register-8">Full rule in this volume</a></p>
</li>
<li id="q-185-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Register access has no success event; separate hardware errors use their event conditions. <a class="qa-rule-link" href="#common-register-9">Full rule in this volume</a></p>
</li>
<li id="q-185-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Register accesses are not logged individually; preserve registers and timing before obtaining available diagnostics. <a class="qa-rule-link" href="#common-register-10">Full rule in this volume</a></p>
</li>
<li id="q-185-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>Ordinary register access is not a PEL event; completed resets and supported hardware errors are assessed separately. <a class="qa-rule-link" href="#common-register-11">Full rule in this volume</a></p>
</li>
<li id="q-185-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Clearing CC.EN invalidates I/O queues and resets Admin pointers; retained base addresses do not validate old completions. <a class="qa-rule-link" href="#common-queue-12">Full rule in this volume</a></p>
</li>
<li id="q-185-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Rebuild affected-controller queues; do not assume CC.EN-reset register-retention exceptions. <a class="qa-rule-link" href="#common-queue-13">Full rule in this volume</a></p>
</li>
<li id="q-185-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Initialize queues and host tracking again; residual memory is not valid command state for a new lifetime. <a class="qa-rule-link" href="#common-queue-14">Full rule in this volume</a></p>
</li>
<li id="q-185-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Controller Reset targets one controller; subsystem reset covers one/all domains as defined for the implementation. <a class="qa-rule-link" href="#common-reset_review-15">Full rule in this volume</a></p>
</li>
<li id="q-185-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Exclude AERs from data-drain expectations.</p>
</li>
<li id="q-185-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>Identify the pending command type first.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-cc">Base 2.4 §3.1.4 (CC, CSTS, NSSR)</a> · <a href="#ref-shutdownfull">Base 2.4 §3.6–3.6.1 (memory-based scope and shutdown)</a> · <a href="#ref-pciereset">PCIe Transport 1.4 §3.3</a> · <a href="#ref-smart">Base 2.4 §5.2.13.1.3</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-186" data-question="186"><h2><a class="qa-qid" href="#q-186">Q186</a> How do shutdown modes affect the former Unsafe Shutdowns counter?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-186-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-186-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Base 2.4 calls it UPL and counts actual loss conditions.</p>
</li>
<li id="q-186-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>UPL is lifetime information, not per-shutdown status.</p>
</li>
<li id="q-186-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Read bytes 144–159 and preserve pre-loss state.</p>
</li>
<li id="q-186-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>Increment with SHST≠10b at loss or the defined Ignore Shutdown/media exception.</p>
</li>
<li id="q-186-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Baseline, request/wait, remove power and compare, recording intervening activity.</p>
</li>
<li id="q-186-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Ready normal/abrupt shutdown does not increment by name; premature loss does.</p>
</li>
<li id="q-186-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Reset alone is not a power-loss count.</p>
</li>
<li id="q-186-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>This MMIO access has no NVMe CQE, so DNR/More do not apply. <a class="qa-rule-link" href="#common-register-8">Full rule in this volume</a></p>
</li>
<li id="q-186-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Register access has no success event; separate hardware errors use their event conditions. <a class="qa-rule-link" href="#common-register-9">Full rule in this volume</a></p>
</li>
<li id="q-186-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Register accesses are not logged individually; preserve registers and timing before obtaining available diagnostics. <a class="qa-rule-link" href="#common-register-10">Full rule in this volume</a></p>
</li>
<li id="q-186-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>Ordinary register access is not a PEL event; completed resets and supported hardware errors are assessed separately. <a class="qa-rule-link" href="#common-register-11">Full rule in this volume</a></p>
</li>
<li id="q-186-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Clearing CC.EN invalidates I/O queues and resets Admin pointers; retained base addresses do not validate old completions. <a class="qa-rule-link" href="#common-queue-12">Full rule in this volume</a></p>
</li>
<li id="q-186-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Rebuild affected-controller queues; do not assume CC.EN-reset register-retention exceptions. <a class="qa-rule-link" href="#common-queue-13">Full rule in this volume</a></p>
</li>
<li id="q-186-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Initialize queues and host tracking again; residual memory is not valid command state for a new lifetime. <a class="qa-rule-link" href="#common-queue-14">Full rule in this volume</a></p>
</li>
<li id="q-186-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Controller Reset targets one controller; subsystem reset covers one/all domains as defined for the implementation. <a class="qa-rule-link" href="#common-reset_review-15">Full rule in this volume</a></p>
</li>
<li id="q-186-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Apply exact conditions, excluding extra losses and wrong samples.</p>
</li>
<li id="q-186-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>Check readiness at actual loss.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-cc">Base 2.4 §3.1.4 (CC, CSTS, NSSR)</a> · <a href="#ref-shutdownfull">Base 2.4 §3.6–3.6.1 (memory-based scope and shutdown)</a> · <a href="#ref-pciereset">PCIe Transport 1.4 §3.3</a> · <a href="#ref-smart">Base 2.4 §5.2.13.1.3</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-187" data-question="187"><h2><a class="qa-qid" href="#q-187">Q187</a> Why inspect health, errors and persistent events after loss?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-187-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-187-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Counters/errors/history help reconstruct the missing-completion interval.</p>
</li>
<li id="q-187-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Match identity and cumulative/live state.</p>
</li>
<li id="q-187-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Check supported events and correct log selection.</p>
</li>
<li id="q-187-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>Inspect power/error counters and reset/operation events.</p>
</li>
<li id="q-187-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Preserve logs before generating additional history.</p>
</li>
<li id="q-187-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Absence of an error entry does not establish data safety.</p>
</li>
<li id="q-187-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Cleared entries can conform while counters persist.</p>
</li>
<li id="q-187-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>This MMIO access has no NVMe CQE, so DNR/More do not apply. <a class="qa-rule-link" href="#common-register-8">Full rule in this volume</a></p>
</li>
<li id="q-187-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Register access has no success event; separate hardware errors use their event conditions. <a class="qa-rule-link" href="#common-register-9">Full rule in this volume</a></p>
</li>
<li id="q-187-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Register accesses are not logged individually; preserve registers and timing before obtaining available diagnostics. <a class="qa-rule-link" href="#common-register-10">Full rule in this volume</a></p>
</li>
<li id="q-187-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>Ordinary register access is not a PEL event; completed resets and supported hardware errors are assessed separately. <a class="qa-rule-link" href="#common-register-11">Full rule in this volume</a></p>
</li>
<li id="q-187-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Clearing CC.EN invalidates I/O queues and resets Admin pointers; retained base addresses do not validate old completions. <a class="qa-rule-link" href="#common-queue-12">Full rule in this volume</a></p>
</li>
<li id="q-187-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Rebuild affected-controller queues; do not assume CC.EN-reset register-retention exceptions. <a class="qa-rule-link" href="#common-queue-13">Full rule in this volume</a></p>
</li>
<li id="q-187-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Initialize queues and host tracking again; residual memory is not valid command state for a new lifetime. <a class="qa-rule-link" href="#common-queue-14">Full rule in this volume</a></p>
</li>
<li id="q-187-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Controller Reset targets one controller; subsystem reset covers one/all domains as defined for the implementation. <a class="qa-rule-link" href="#common-reset_review-15">Full rule in this volume</a></p>
</li>
<li id="q-187-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Correlate timelines without one-to-one record assumptions.</p>
</li>
<li id="q-187-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>Preserve the first recovered snapshot.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-cc">Base 2.4 §3.1.4 (CC, CSTS, NSSR)</a> · <a href="#ref-shutdownfull">Base 2.4 §3.6–3.6.1 (memory-based scope and shutdown)</a> · <a href="#ref-pciereset">PCIe Transport 1.4 §3.3</a> · <a href="#ref-smart">Base 2.4 §5.2.13.1.3</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<section id="common-rules" class="qa-common"><h2>Shared rules linked from the answers</h2><p>Each shared mechanism is explained in full once in this volume. Use browser Back to return to the question; explicit command or feature exceptions take precedence.</p>
<article id="common-queue-12"><h3>Queue reset and scope · What survives or continues after Controller Reset?</h3><p>Clearing CC.EN initiates a Controller Level Reset: I/O queues are deleted and Admin Queue pointers reset. Retention of AQA/ASQ/ACQ for this reset does not validate old CQEs. Reinitialize Admin CQ phases, enable, then configure and recreate I/O queues.</p></article>
<article id="common-queue-13"><h3>Queue reset and scope · What survives or continues after NVM Subsystem Reset?</h3><p>Affected controllers undergo Controller Level Reset during an NVM Subsystem Reset; old queues cannot be reused. Re-establish transport and register state and the Admin/I/O environment. Do not apply the AQA retention exception of a CC.EN reset to this different reset source.</p></article>
<article id="common-queue-14"><h3>Queue reset and scope · What survives or continues after a power cycle?</h3><p>After a power cycle, initialize and create queues again. Residual SQE/CQE bytes in host memory are not valid commands or completions for the new queue lifetime; rebuild host pointers, phases and outstanding-command tracking.</p></article>
<article id="common-register-8"><h3>Register access · How are DNR and More set?</h3><p>Not applicable to this register access: it has no NVMe CQE and therefore no DNR or More to set. Decode those bits only for a subsequent Admin or I/O command that actually returns a CQE.</p></article>
<article id="common-register-9"><h3>Register access · Is an asynchronous event generated?</h3><p>This register access does not define a success notification. A separate defined event, such as an Internal Error, follows its own rules. When the Admin Queue is unavailable, waiting for an event cannot replace initialization-state checks.</p></article>
<article id="common-register-10"><h3>Register access · Are Error Information or other logs updated?</h3><p>Every register read or write does not require an Error Information entry. Preserve CAP, CC, CSTS, CRTO and timestamps first; logs provide additional evidence if the controller subsequently permits access.</p></article>
<article id="common-register-11"><h3>Register access · Is it recorded in the Persistent Event Log?</h3><p>An ordinary register access is not a separate persistent event. Reset, power or hardware conditions are recorded when PEL support and the corresponding event requirements apply; each CC write is not automatically a Power-on or Reset event.</p></article>
<article id="common-reset_review-15"><h3>Shared conditions for this topic · Are other controllers or namespaces affected?</h3><p>Controller Reset targets one controller; subsystem reset covers one/all domains as defined for the implementation. Power-off readiness also depends on CAP.CPS; shared paths are not independent data copies.</p></article>
</section>
<section id="source-index"><h2>Source locations and existing figure guides</h2><p>Base printed page = PDF page−26; the other two use identical numbers. Locations follow the supplied PDF body and retain figure numbers. Shared pages contribute only the relevant definitions, excluding Fabrics and PCIe link/packet content.</p><ul class="qa-references">
<li id="ref-cap"><strong>Base 2.4 · §3.1.4 (CAP, VS)</strong><br>Printed pages 54–59 · PDF 80–85 · Figure 36–37</li>
<li id="ref-cc"><strong>Base 2.4 · §3.1.4 (CC, CSTS, NSSR)</strong><br>Printed pages 60–66 · PDF 86–92 · Figure 41–43</li>
<li id="ref-adminreg"><strong>Base 2.4 · §3.1.4 (AQA, ASQ, ACQ, CMBLOC)</strong><br>Printed pages 66–68 · PDF 92–94 · Figure 44–47</li>
<li id="ref-crto"><strong>Base 2.4 · §3.1.4 (CRTO)</strong><br>Printed pages 72–73 · PDF 98–99 · Figure 57</li>
<li id="ref-shutdownfull"><strong>Base 2.4 · §3.6–3.6.1 (memory-based scope and shutdown)</strong><br>Printed pages 113–115 · PDF 139–141 · Figure 85</li>
<li id="ref-reset"><strong>Base 2.4 · §3.7.1–3.7.4</strong><br>Printed pages 120–124 · PDF 146–150</li>
<li id="ref-firmware"><strong>Base 2.4 · §3.11–3.11.1, 5.2.9–5.2.10</strong><br>Printed pages 135–138, 202–206 · PDF 161–164, 228–232 · Figure 187–193</li>
<li id="ref-status"><strong>Base 2.4 · §4.2.3</strong><br>Printed pages 145–155 · PDF 171–181 · Figure 101–105</li>
<li id="ref-feature"><strong>Base 2.4 · §4.4</strong><br>Printed pages 166–169 · PDF 192–195 · Figure 126–127</li>
<li id="ref-aer"><strong>Base 2.4 · §5.2.2</strong><br>Printed pages 183–190 · PDF 209–216 · Figure 150–156</li>
<li id="ref-selftest"><strong>Base 2.4 · §5.2.6, 8.1.8</strong><br>Printed pages 199–201, 614–616 · PDF 225–227, 640–642 · Figure 176–180, 700–701</li>
<li id="ref-error"><strong>Base 2.4 · §5.2.13.1.2</strong><br>Printed pages 218–220 · PDF 244–246 · Figure 212</li>
<li id="ref-smart"><strong>Base 2.4 · §5.2.13.1.3</strong><br>Printed pages 220–225 · PDF 246–251 · Figure 213–214</li>
<li id="ref-dstlog"><strong>Base 2.4 · §5.2.13.1.7</strong><br>Printed pages 229–232 · PDF 255–258 · Figure 218–219</li>
<li id="ref-pel"><strong>Base 2.4 · §5.2.13.1.14 (header, reset, hardware, Set Feature events)</strong><br>Printed pages 244–256, 258, 262–264 · PDF 270–282, 284, 288–290 · Figure 232–244, 246, 252–253</li>
<li id="ref-sanitizelog"><strong>Base 2.4 · §5.2.13.1.38</strong><br>Printed pages 313–320 · PDF 339–346 · Figure 312</li>
<li id="ref-sanitizecmd"><strong>Base 2.4 · §5.2.26–5.2.27</strong><br>Printed pages 448–454 · PDF 474–480 · Figure 451–455</li>
<li id="ref-commrecovery"><strong>Base 2.4 · §9.1–9.6.2.1 (PCIe-applicable rules; stop before 9.6.2.2)</strong><br>Printed pages 825–828 · PDF 851–854</li>
<li id="ref-fatal"><strong>Base 2.4 · §9.1–9.6.1</strong><br>Printed pages 825–826 · PDF 851–852</li>
<li id="ref-pciereset"><strong>PCIe Transport 1.4 · §3.3</strong><br>Printed pages 11–12 · PDF 11–12</li>
</ul><h3>When you need a field guide</h3><p>Existing figure explanations have canonical locations; use these links instead of duplicating the same guide.</p><ul>
<li><a href="/nvme/figure-reference/command/en/#figure-b101">Base 2.4 Figure 101 · Completion Queue Entry: Status Field</a></li>
<li><a href="/nvme/figure-reference/command/en/#figure-b104">Base 2.4 Figure 104 · Status Code – Command Specific Status Values</a></li>
<li><a href="/nvme/figure-reference/init/en/#figure-b36">Base 2.4 Figure 36 · Offset 0h: CAP – Controller Capabilities</a></li>
<li><a href="/nvme/figure-reference/init/en/#figure-b41">Base 2.4 Figure 41 · Offset 14h: CC – Controller Configuration</a></li>
<li><a href="/nvme/figure-reference/init/en/#figure-b42">Base 2.4 Figure 42 · Offset 1Ch: CSTS – Controller Status</a></li>
<li><a href="/nvme/figure-reference/init/en/#figure-b44">Base 2.4 Figure 44 · Offset 24h: AQA – Admin Queue Attributes</a></li>
<li><a href="/nvme/figure-reference/init/en/#figure-b45">Base 2.4 Figure 45 · Offset 28h: ASQ – Admin Submission Queue Base Address</a></li>
<li><a href="/nvme/figure-reference/init/en/#figure-b46">Base 2.4 Figure 46 · Offset 30h: ACQ – Admin Completion Queue Base Address</a></li>
</ul><details><summary>Original documents used</summary><ul class="qr-sources">
<li>NVM Express Base Specification · Revision 2.4 · 2026-07-31<br><code>NVM-Express-Base-Specification-Revision-2.4-Ratified-2026.07.31.pdf</code></li>
<li>NVM Express NVM Command Set Specification · Revision 1.3 · 2026-07-31<br><code>NVM-Express-NVM-Command-Set-Specification-Revision-1.3-Ratified-2026.07.31.pdf</code></li>
<li>NVM Express NVMe over PCIe Transport Specification · Revision 1.4 · 2026-07-31<br><code>NVM-Express-NVMe-over-PCIe-Transport-Specification-Revision-1.4-Ratified-2026.07.31.pdf</code></li>
</ul></details></section>
</main>
<nav class="qr-top" aria-label="Bank and editions"><a href="#content">Skip to content</a><a href="/nvme/question-bank/en/">Question index</a><a href="/nvme/question-bank/reset-shutdown/zh-tw/">繁體中文</a><a href="/DOCS/nvme-question-bank/reset-shutdown.html">Chinese tutorial HTML</a></nav>
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
