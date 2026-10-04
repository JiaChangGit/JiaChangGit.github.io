---
layout: post
title: "NVMe Self-Study Bank: Format and sanitize"
date: 2026-10-02 00:00:00 +0800
categories: [nvme]
permalink: /nvme/question-bank/format-sanitize/en/
lang: en
nvme_quickref: true
nvme_qa: true
---

<div class="nvme-quickref nvme-qa">
<nav class="qr-top" aria-label="Bank and editions"><a href="#content">Skip to content</a><a href="/nvme/question-bank/en/">Question index</a><a href="/nvme/question-bank/format-sanitize/zh-tw/">繁體中文</a><a href="/DOCS/nvme-question-bank/format-sanitize.html">Chinese tutorial HTML</a></nav>
<main id="content"><p class="qr-eyebrow">BASE 2.4 / NVM 1.3 / PCIe 1.4 · Q1–328</p>
<header><p class="qa-range">Q118–Q135</p><h1>Format and sanitize</h1><p class="qr-intro">Format changes namespace format; sanitize removes data. Compare scope, completion and reset behavior across the operation lifecycle.</p><p>Practice first, then reveal 17 answer items per question. All numerical examples are hypothetical. Status is written SCT/SC; h indicates hexadecimal.</p></header>
<aside class="qa-glossary"><h2>Terms used in this volume</h2><dl><dt>Controller / namespace</dt><dd>A controller receives commands and manages access. A namespace is a logical storage space that commands can address. An NVM subsystem contains controllers and nonvolatile storage resources.</dd><dt>SQ / CQ / SQE / CQE</dt><dd>Submission and Completion Queues carry command entries (SQEs) and completion entries (CQEs). QID identifies a queue, CID distinguishes outstanding commands in one SQ, and NSID identifies a namespace.</dd><dt>Register / Identify / Feature / Log</dt><dd>A register exposes control or state. Identify queries capabilities and attributes; features query or configure operation; log pages report specific state or records. FID, LID, CNS and CSI select features, logs, Identify structures and command sets.</dd><dt>index / offset / zero-based</dt><dd>An index selects an entry, usually starting at 0; an offset measures distance from an origin in specified units. A zero-based count encodes count−1, but not every zero-valued field is a count. A Dword is 4 bytes; a byte is 8 bits.</dd><dt>Scope / reset / retention</dt><dd>Scope names the affected objects; retention means preserving state. Controller Reset (clearing CC.EN) is one form of Controller Level Reset, or CLR. Different CLR triggers can retain different registers.</dd></dl></aside>
<section id="overview" class="qa-overview"><h2>Three distinct operation paths</h2><p class="qa-takeaway">Subsystem overwrite support does not enable namespace overwrite.</p>
<div class="qr-table" tabindex="0" role="region" aria-label="Horizontally scrollable comparison table"><table><thead><tr><th scope="col">Operation</th><th scope="col">Main selectors</th><th scope="col">Completion evidence</th></tr></thead><tbody><tr><td>Format NVM</td><td>Format, metadata, PI and SES</td><td>Format CQE and resulting format</td></tr><tr><td>Subsystem sanitize</td><td>Action and options</td><td>Initiation CQE followed by status</td></tr><tr><td>Namespace sanitize</td><td>NSID and crypto erase</td><td>Target namespace status</td></tr></tbody></table></div>
<p><strong>Worked interpretation: </strong>OWS1 advertises subsystem overwrite. Base 2.4 namespace sanitize permits crypto erase, not copied SANACT3 overwrite.</p>
<p class="qa-citations">Sources: <a href="#ref-format">Base 2.4 §5.1.1, 5.2.11</a> · <a href="#ref-nvmformat">NVM Command Set 1.3 §4.1.2</a> · <a href="#ref-sanitizecmd">Base 2.4 §5.2.26–5.2.27</a> · <a href="#ref-sanitizelog">Base 2.4 §5.2.13.1.38</a> · <a href="#ref-sanitizestate">Base 2.4 §8.1.27.1–8.1.27.5</a></p>
</section>
<div class="qa-controls" hidden><label>Search this page <input type="search" id="qa-search" placeholder="Question number, field or keyword"></label><button type="button" data-expand="true">Expand all answers</button><button type="button" data-expand="false">Collapse all answers</button><output id="qa-count" aria-live="polite"></output></div>
<section id="question-index"><h2>Questions in this volume</h2><ol class="qa-index">
<li><a href="#q-118">Q118 · How is support for Format, Sanitize and Sanitize Namespace discovered?</a></li>
<li><a href="#q-119">Q119 · How do Format, secure erase and the two sanitize targets differ?</a></li>
<li><a href="#q-120">Q120 · How are Format data format, metadata, PI and SES selected?</a></li>
<li><a href="#q-121">Q121 · How are invalid Format parameters and states reported?</a></li>
<li><a href="#q-122">Q122 · Which Admin operations can continue during Format?</a></li>
<li><a href="#q-123">Q123 · How is interrupted Format assessed after reset or power loss?</a></li>
<li><a href="#q-124">Q124 · Which namespace data must be refreshed after Format?</a></li>
<li><a href="#q-125">Q125 · How are Format failures checked using CQE, Error Log and PEL?</a></li>
<li><a href="#q-126">Q126 · How does SANICAP advertise sanitize methods?</a></li>
<li><a href="#q-127">Q127 · How do NDAS, overwrite pattern, passes and inversion work?</a></li>
<li><a href="#q-128">Q128 · How are progress, status, state and erased-data flags interpreted together?</a></li>
<li><a href="#q-129">Q129 · Which commands are permitted during subsystem sanitization?</a></li>
<li><a href="#q-130">Q130 · Does sanitization continue across reset or power loss?</a></li>
<li><a href="#q-131">Q131 · How do success, failure and failure mode differ in the log?</a></li>
<li><a href="#q-132">Q132 · What does Exit Failure Mode accomplish?</a></li>
<li><a href="#q-133">Q133 · When are sanitize AERs and persistent events generated?</a></li>
<li><a href="#q-134">Q134 · How is namespace sanitization targeted and isolated?</a></li>
<li><a href="#q-135">Q135 · How are invalid or unsupported namespace sanitize requests handled?</a></li>
</ol></section>
<article class="qa-question" id="q-118" data-question="118"><h2><a class="qa-qid" href="#q-118">Q118</a> How is support for Format, Sanitize and Sanitize Namespace discovered?</h2>
<p class="qa-prompt">Task: determine Sanitize Namespace support using queries only. Identify the opcode, log, entry and support bit before revealing the answer.</p>
<details class="qa-answer" id="q-118-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-118-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Opcode support, supported action and current permission are distinct; Sanitize support does not enable every erasure method.</p>
</li>
<li id="q-118-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Format scope depends on FNA, SES and NSID; subsystem and namespace sanitization use distinct commands and targets.</p>
</li>
<li id="q-118-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Use OACS/FNA for Format and SANICAP CES/BES/OWS for Sanitize. For the Sanitize Namespace command itself, find Admin opcode 8Ch in Figure 28, then decode bit 0 (CSUPP) of its Admin entry in LID 05h using Figure 217. CSUPP declares command support; CES and NVERS separately describe the method and namespace media-verification capability.</p>
<section class="qa-lookup" id="q-118-lookup"><h4>Worked lookup: from Sanitize Namespace to CSUPP</h4>
<p>All values below are hypothetical. Use one PCIe I/O controller, CC.CSS=000b and UUID Index 0; decode buffers only after successful queries. Figure 28 is the specification’s command catalog, not the device’s measured capability list.</p>
<div class="qr-table" tabindex="0" role="region" aria-label="Horizontally scrollable comparison table"><table><thead><tr><th scope="col">Step and source location</th><th scope="col">Information to retrieve</th><th scope="col">What this establishes</th></tr></thead><tbody><tr><td>1 · Figure 28, printed 46/PDF 72</td><td>Sanitize Namespace → Admin opcode 8Ch; O means optional.</td><td>Identifies the command and encoding. Optional does not establish this controller’s support.</td></tr><tr><td>2 · Identify Controller, Figure 338, printed 355,361–362/PDF 381,387–388</td><td>CNS 01h; assume LPA.CSES=1, SANICAP.CES=1 and NVERS=0. CSES is LPA bit 1.</td><td>Effects log and Crypto Erase are supported; namespace media verification is not. CES alone does not replace 8Ch support discovery.</td></tr><tr><td>3 · Get Log Page, Figures 204–208, printed 213–215/PDF 239–241</td><td>Opcode 02h, LID 05h, NSID 0, NUMDL=03FFh, NUMDU=0, LPO=0, OT=0 and RAE=0 retrieve 4096 bytes.</td><td>NUMD encodes count−1: (03FFh+1)×4=4096 bytes. This reads a directory without submitting opcode 8Ch.</td></tr><tr><td>4 · Figure 216, printed 227/PDF 253</td><td>Admin entries begin at byte 0 and occupy 4 bytes each. 8Ch=140, so offset 4×140=560=230h selects bytes 560–563.</td><td>This Admin entry does not use the I/O region’s 1024-byte base. For a partial read, subtract that segment’s starting byte offset to find the buffer-relative position.</td></tr><tr><td>5 · Figure 217, printed 228–229/PDF 254–255</td><td>Hypothetical bytes 03h,00h,01h,00h form little-endian 00010003h; bit 0=1.</td><td>CSUPP=1 advertises 8Ch. LBCC=1 and CSE=001b additionally describe possible data change and same-namespace coordination recommendations, not an operation result.</td></tr><tr><td>6 · §5.2.27/Figure 454, printed 452–453/PDF 478–479</td><td>Namespace initiation uses SANACT100b (Crypto Erase);010b/011b are reserved. Check active NSID, protection and concurrency before execution.</td><td>Command support does not establish namespace Overwrite or current eligibility of every target. NVERS=0 also does not provide entry to Media Verification.</td></tr></tbody></table></div>
<p>A valid entry with CSUPP=0 reports no command support and requires its other fields to be zero. CSES=0 or a failed log query instead leaves this route without valid support evidence; neither is an observed CSUPP=0.</p>
<p class="qa-citations">Sources: <a href="#ref-adminsupport">Base 2.4 §3.1.3.4 (Figure 28 PCIe I/O-controller rows and O/M/P note only)</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-idcmd">Base 2.4 §5.2.14.1</a> · <a href="#ref-getlog">Base 2.4 §5.2.13–5.2.13.1.1</a> · <a href="#ref-commandseffects">Base 2.4 §5.2.13.1.6</a> · <a href="#ref-sanitizecmd">Base 2.4 §5.2.26–5.2.27</a></p>
</section>
</li>
<li id="q-118-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>Format, Sanitize and Sanitize Namespace have Admin opcodes 80h,84h and 8Ch. Discovery submits Identify (06h) and Get Log Page (02h), with LID 05h selecting the command table. Do not put 8Ch in LID or treat support for Get Log Page itself as support for every log or management command.</p>
</li>
<li id="q-118-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Establish query access and log support, read the correct entry, then check method, parameters and target state when CSUPP=1. Discovery requires no sanitize initiation. Before actual execution, additionally check active NSID, protection, sanitize state, concurrency and pending-firmware restrictions.</p>
</li>
<li id="q-118-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Successful Identify/Get Log Page provides capability evidence. CSUPP=1 for 8Ch establishes advertised Sanitize Namespace support, not current eligibility of NSID 7 or completed erasure.</p>
</li>
<li id="q-118-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>An unsupported LID 05h generally causes Invalid Log Page (1/09h), leaving no valid CSUPP result; it is not CSUPP=0. An unsupported submitted opcode and an invalid SANACT in a supported command are separate conditions using 0/01h and 0/02h respectively.</p>
</li>
<li id="q-118-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-118-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Reading Identify and capability logs does not initiate sanitization or generate its start/completion notices. Unrelated concurrent events retain their own rules.</p>
</li>
<li id="q-118-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Successful capability discovery neither starts the Sanitize Status state machine nor erases target data. Diagnose a failed query from its own CQE/error information, separately from background sanitize outcomes.</p>
</li>
<li id="q-118-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>Read-only discovery does not create Sanitize Start or Completion persistent events. Support does not imply a history of performing the operation.</p>
</li>
<li id="q-118-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Repeat an interrupted query and distinguish identity, configuration and dynamic fields. <a class="qa-rule-link" href="#common-identify-12">Full rule in this volume</a></p>
</li>
<li id="q-118-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Rediscover affected objects; reset alone does not mean namespace deletion or factory configuration. <a class="qa-rule-link" href="#common-identify-13">Full rule in this volume</a></p>
</li>
<li id="q-118-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Re-read and compare, separating firmware activation or management changes from power cycling alone. <a class="qa-rule-link" href="#common-identify-14">Full rule in this volume</a></p>
</li>
<li id="q-118-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Identify is read-only; active lists may differ by controller, so compare matching query targets. <a class="qa-rule-link" href="#common-identify-15">Full rule in this volume</a></p>
</li>
<li id="q-118-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Compare the same controller, command-set context and configuration period. With CSUPP=1, exclude invalid parameters/state before alleging inconsistency. CSUPP=0 with valid successful execution needs investigation. OWS=1 does not legalize namespace Overwrite.</p>
</li>
<li id="q-118-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First confirm a successful LID 05h read and the Admin entry for 8Ch. Selecting 84h, using the wrong offset units or decoding a buffer from a failed query invalidates the support conclusion.</p>
</li>
</ol>
<p class="qa-related">Related mechanisms: <a href="/nvme/question-bank/logs/en/#q-081">Q81</a> · <a href="/nvme/question-bank/format-sanitize/en/#q-126">Q126</a> · <a href="/nvme/question-bank/format-sanitize/en/#q-134">Q134</a> · <a href="/nvme/question-bank/format-sanitize/en/#q-135">Q135</a></p>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-commandseffects">Base 2.4 §5.2.13.1.6</a> · <a href="#ref-sanitizecmd">Base 2.4 §5.2.26–5.2.27</a> · <a href="#ref-format">Base 2.4 §5.1.1, 5.2.11</a> · <a href="#ref-nvmformat">NVM Command Set 1.3 §4.1.2</a> · <a href="#ref-formatpel">Base 2.4 §5.2.13.1.14.2.7–5.2.13.1.14.2.8</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-adminsupport">Base 2.4 §3.1.3.4 (Figure 28 PCIe I/O-controller rows and O/M/P note only)</a> · <a href="#ref-getlog">Base 2.4 §5.2.13–5.2.13.1.1</a> · <a href="#ref-idcmd">Base 2.4 §5.2.14.1</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-119" data-question="119"><h2><a class="qa-qid" href="#q-119">Q119</a> How do Format, secure erase and the two sanitize targets differ?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-119-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-119-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Format changes media format and can request secure erase; Sanitize removes target user data rather than serving as an ordinary format change.</p>
</li>
<li id="q-119-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Format scope is selected by FNA/SES/NSID; subsystem sanitize covers its defined user-data locations and namespace sanitize its selected target.</p>
</li>
<li id="q-119-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Check OACS, FNA, SANICAP, namespace state and formats; the shared name Crypto Erase does not imply identical command scope.</p>
</li>
<li id="q-119-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>Format SES0 omits secure erase,1 requests user-data erase and 2 cryptographic erase. Sanitize uses SANACT; namespace sanitization only supports Crypto Erase.</p>
</li>
<li id="q-119-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Choose based on format change, target and required method. Sanitizing each namespace is not equivalent to covering every subsystem user-data location.</p>
</li>
<li id="q-119-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Format completion follows media formatting; successful Sanitize initiation still requires LID 81h monitoring.</p>
</li>
<li id="q-119-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Invalid formats and unsupported SANACT use their separate statuses, Invalid Format and Invalid Field.</p>
</li>
<li id="q-119-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-119-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>This comparison distinguishes Format: Format attribute changes follow namespace-change support/configuration and changed-list rules. Relevant FPI notifications concern zero/nonzero transitions, not every percentage update. Sanitize: State transitions report completed, unexpected-deallocation completion or media-verification entry with LID 81h. For Admin-SQ initiation, only the initiating controller reports the event; inspect the log for actual outcome.</p>
</li>
<li id="q-119-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>This comparison distinguishes Format: Re-read namespace format/capacity and changed lists after success. For errors use CQE.More and Error Information; a successful Get Log does not substitute for Format completion. Sanitize: Sanitize Status updates before the initiating CQE and on transitions, persisting across resets/power. Match target, SOS, SANS, SPROG, SCDW10 and GDE/NDE; background failure does not require a second initiation CQE.</p>
</li>
<li id="q-119-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>This comparison distinguishes Format: With supported PEL events, Format Start 07h records the request and Completion 08h the outcome. Read FNVMS with INFO; INFO can be zero when no Format CQE was reported and does not alone prove success. Sanitize: Supported PEL logging records Start 09h on entering processing and Completion 0Ah on entering Idle or either failure state. Completion includes failures; NSID distinguishes subsystem and namespace targets.</p>
</li>
<li id="q-119-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>This comparison distinguishes Format: Controller Reset ends the old command channel. Re-read format, FPI and available Format Completion events after recovery; reset proves neither format success nor rollback. Sanitize: Background sanitization continues through Controller Level Reset. Re-read target LID 81h after recovery. Some reset sources cancel media verification and set MVCNCLD without cancelling the entire sanitize operation.</p>
</li>
<li id="q-119-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>This comparison distinguishes Format: After subsystem reset, recover access and inspect namespaces in the original format scope; one controller’s recovery does not establish all namespace outcomes. Sanitize: Subsystem reset does not abort sanitization. Preserve operation/log state and check MVCNCLD and post-verification deallocation when verification was requested.</p>
</li>
<li id="q-119-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>This comparison distinguishes Format: Without trustworthy successful completion before power interruption, reassess format and usability and, if needed, perform a valid new Format. Missing success does not imply old data survived. Sanitize: Processing cannot occur without power, but sanitization continues from retained state after power returns. Inspect SOS/SANS and progress; SPROG=FFFFh alone is not success.</p>
</li>
<li id="q-119-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>This comparison distinguishes Format: Select FNA.FNS or SENS using SES, then combine it with NSID. Coordinate other access paths to shared namespaces; submission to one controller does not imply controller-local data impact. Sanitize: Subsystem sanitization restricts subsystem access; namespace sanitization targets one namespace across its controllers. Shared operations such as firmware update have additional restrictions even when other namespace data is not erased.</p>
</li>
<li id="q-119-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Use Format to select 4 KiB LBAs; erasing one namespace and observing NDE does not establish subsystem GDE.</p>
</li>
<li id="q-119-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First clarify whether the erasure target is one namespace or the full subsystem scope.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-sanitizecmd">Base 2.4 §5.2.26–5.2.27</a> · <a href="#ref-sanitizestate">Base 2.4 §8.1.27.1–8.1.27.5</a> · <a href="#ref-nvmsanitize">NVM Command Set 1.3 §4.1.7, 5.12</a> · <a href="#ref-format">Base 2.4 §5.1.1, 5.2.11</a> · <a href="#ref-nvmformat">NVM Command Set 1.3 §4.1.2</a> · <a href="#ref-formatpel">Base 2.4 §5.2.13.1.14.2.7–5.2.13.1.14.2.8</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-120" data-question="120"><h2><a class="qa-qid" href="#q-120">Q120</a> How are Format data format, metadata, PI and SES selected?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-120-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-120-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Format selection determines I/O data and metadata layout; mismatches invalidate subsequent buffers and protection information.</p>
</li>
<li id="q-120-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>The selection configures namespaces in the format scope rather than only this command’s transfer.</p>
</li>
<li id="q-120-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Read LBAF/FLBAS, MC, DPC, DPS and applicable NVM format extensions, plus LBAFEE.</p>
</li>
<li id="q-120-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>LBAFL plus enabled LBAFU select format; MSET selects extended or separate metadata, PI selects 0–3, and current NVM PIL must be 0. SES independently selects secure erase.</p>
</li>
<li id="q-120-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Select an advertised format and verify metadata/PI compatibility. For hypothetical LBAF2 with 4096+16 bytes, MSET=1 gives 4112 bytes per extended LBA.</p>
</li>
<li id="q-120-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>On success FLBAS/DPS reflect the selection; changed logical-block size can alter NSZE/NCAP, requiring fresh reads.</p>
</li>
<li id="q-120-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Unsupported formats use Invalid Format; formats disabled by missing LBAFEE use Invalid Namespace or Format. Shared FDP RUHs impose matching-format constraints.</p>
</li>
<li id="q-120-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-120-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Format attribute changes follow namespace-change support/configuration and changed-list rules. <a class="qa-rule-link" href="#common-format_op-9">Full rule in this volume</a></p>
</li>
<li id="q-120-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Re-read namespace format/capacity and changed lists after success. <a class="qa-rule-link" href="#common-format_op-10">Full rule in this volume</a></p>
</li>
<li id="q-120-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>With supported PEL events, Format Start 07h records the request and Completion 08h the outcome. <a class="qa-rule-link" href="#common-format_op-11">Full rule in this volume</a></p>
</li>
<li id="q-120-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Controller Reset ends the old command channel. <a class="qa-rule-link" href="#common-format_op-12">Full rule in this volume</a></p>
</li>
<li id="q-120-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>After subsystem reset, recover access and inspect namespaces in the original format scope; one controller’s recovery does not establish all namespace outcomes. <a class="qa-rule-link" href="#common-format_op-13">Full rule in this volume</a></p>
</li>
<li id="q-120-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Without trustworthy successful completion before power interruption, reassess format and usability and, if needed, perform a valid new Format. <a class="qa-rule-link" href="#common-format_op-14">Full rule in this volume</a></p>
</li>
<li id="q-120-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Select FNA.FNS or SENS using SES, then combine it with NSID. <a class="qa-rule-link" href="#common-format_op-15">Full rule in this volume</a></p>
</li>
<li id="q-120-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Recalculate I/O data/metadata lengths rather than retaining the pre-format layout.</p>
</li>
<li id="q-120-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First check index upper/lower bits and LBAFEE, then MSET/PI compatibility.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-idns">NVM Command Set 1.3 §4.1.5.1–4.1.5.4</a> · <a href="#ref-behavior">Base 2.4 §5.2.30.1.15</a> · <a href="#ref-format">Base 2.4 §5.1.1, 5.2.11</a> · <a href="#ref-nvmformat">NVM Command Set 1.3 §4.1.2</a> · <a href="#ref-formatpel">Base 2.4 §5.2.13.1.14.2.7–5.2.13.1.14.2.8</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-121" data-question="121"><h2><a class="qa-qid" href="#q-121">Q121</a> How are invalid Format parameters and states reported?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-121-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-121-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Rejection can result from unsupported/disabled formats, protection or conflicting operations, requiring different fixes.</p>
</li>
<li id="q-121-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Compute full format scope before checking protection across all affected namespaces.</p>
</li>
<li id="q-121-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Establish preconditions through LBAF, LBAFEE, FNA, protection and concurrent operations.</p>
</li>
<li id="q-121-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>Relevant codes are 1/0Ah,0/0Bh,0/20h,0/0Ch and 0/84h respectively.</p>
</li>
<li id="q-121-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Isolate one defect per negative test, keeping NSID, protection and concurrency valid for an unsupported-LBAF test.</p>
</li>
<li id="q-121-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Rejection does not establish a format change; re-read configuration rather than treating failure as successful execution.</p>
</li>
<li id="q-121-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>With I/O being processed for an affected namespace, Format may be aborted, using Command Sequence Error if aborted for that reason; rejection is not universally mandatory.</p>
</li>
<li id="q-121-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-121-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Format attribute changes follow namespace-change support/configuration and changed-list rules. <a class="qa-rule-link" href="#common-format_op-9">Full rule in this volume</a></p>
</li>
<li id="q-121-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Re-read namespace format/capacity and changed lists after success. <a class="qa-rule-link" href="#common-format_op-10">Full rule in this volume</a></p>
</li>
<li id="q-121-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>With supported PEL events, Format Start 07h records the request and Completion 08h the outcome. <a class="qa-rule-link" href="#common-format_op-11">Full rule in this volume</a></p>
</li>
<li id="q-121-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Controller Reset ends the old command channel. <a class="qa-rule-link" href="#common-format_op-12">Full rule in this volume</a></p>
</li>
<li id="q-121-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>After subsystem reset, recover access and inspect namespaces in the original format scope; one controller’s recovery does not establish all namespace outcomes. <a class="qa-rule-link" href="#common-format_op-13">Full rule in this volume</a></p>
</li>
<li id="q-121-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Without trustworthy successful completion before power interruption, reassess format and usability and, if needed, perform a valid new Format. <a class="qa-rule-link" href="#common-format_op-14">Full rule in this volume</a></p>
</li>
<li id="q-121-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Select FNA.FNS or SENS using SES, then combine it with NSID. <a class="qa-rule-link" href="#common-format_op-15">Full rule in this volume</a></p>
</li>
<li id="q-121-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Tests must distinguish shall/should/may and permitted selection among simultaneous errors.</p>
</li>
<li id="q-121-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First check whether multiple defects make an exact-status assertion ambiguous.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-nwp">Base 2.4 §5.2.30.1.38, 8.1.18</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-format">Base 2.4 §5.1.1, 5.2.11</a> · <a href="#ref-nvmformat">NVM Command Set 1.3 §4.1.2</a> · <a href="#ref-formatpel">Base 2.4 §5.2.13.1.14.2.7–5.2.13.1.14.2.8</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-122" data-question="122"><h2><a class="qa-qid" href="#q-122">Q122</a> Which Admin operations can continue during Format?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-122-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-122-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Hosts still need status, notifications and queue management; Format does not universally block all Admin commands.</p>
</li>
<li id="q-122-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Restrictions depend on affected namespaces and Figure 144 command/log conditions.</p>
</li>
<li id="q-122-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Establish support first; the allowed-during-Format list does not enable unsupported optional commands.</p>
</li>
<li id="q-122-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>Examples include Abort, AER, queue management, Identify, Get Features, selected logs and Keep Alive; Namespace Write Protection Config is excluded from allowed Set Features.</p>
</li>
<li id="q-122-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Apply Figure 144 per entry: error-log LBA returns zero and only Controller DST should be allowed. Get Log permission does not extend to every LID.</p>
</li>
<li id="q-122-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Permitted queries return state without establishing Format completion.</p>
</li>
<li id="q-122-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Unlisted Admin commands affecting the target may be aborted and should use Format In Progress for that reason; preexisting conflicting Admin work can instead cause Format sequence error.</p>
</li>
<li id="q-122-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-122-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Format attribute changes follow namespace-change support/configuration and changed-list rules. <a class="qa-rule-link" href="#common-format_op-9">Full rule in this volume</a></p>
</li>
<li id="q-122-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Re-read namespace format/capacity and changed lists after success. <a class="qa-rule-link" href="#common-format_op-10">Full rule in this volume</a></p>
</li>
<li id="q-122-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>With supported PEL events, Format Start 07h records the request and Completion 08h the outcome. <a class="qa-rule-link" href="#common-format_op-11">Full rule in this volume</a></p>
</li>
<li id="q-122-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Controller Reset ends the old command channel. <a class="qa-rule-link" href="#common-format_op-12">Full rule in this volume</a></p>
</li>
<li id="q-122-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>After subsystem reset, recover access and inspect namespaces in the original format scope; one controller’s recovery does not establish all namespace outcomes. <a class="qa-rule-link" href="#common-format_op-13">Full rule in this volume</a></p>
</li>
<li id="q-122-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Without trustworthy successful completion before power interruption, reassess format and usability and, if needed, perform a valid new Format. <a class="qa-rule-link" href="#common-format_op-14">Full rule in this volume</a></p>
</li>
<li id="q-122-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Select FNA.FNS or SENS using SES, then combine it with NSID. <a class="qa-rule-link" href="#common-format_op-15">Full rule in this volume</a></p>
</li>
<li id="q-122-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Verify command permission, LID restrictions and returned fields separately.</p>
</li>
<li id="q-122-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First inspect Figure 144&#x27;s additional restrictions for the specific LID.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-sanitizerestrict">Base 2.4 §5.1.1–5.1.2 (PCIe commands)</a> · <a href="#ref-format">Base 2.4 §5.1.1, 5.2.11</a> · <a href="#ref-nvmformat">NVM Command Set 1.3 §4.1.2</a> · <a href="#ref-formatpel">Base 2.4 §5.2.13.1.14.2.7–5.2.13.1.14.2.8</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-123" data-question="123"><h2><a class="qa-qid" href="#q-123">Q123</a> How is interrupted Format assessed after reset or power loss?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-123-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-123-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Lost completion means unknown outcome, not guaranteed non-execution or success; reconstruct it from current state and events.</p>
</li>
<li id="q-123-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Inspect all originally affected namespaces and their access through other controllers.</p>
</li>
<li id="q-123-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Read FLBAS, DPS, NSZE/NCAP, supported FPI and PEL Format Completion.</p>
</li>
<li id="q-123-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>FNVMS describes formatting outcome while INFO records a reported status; INFO=0 without a CQE is not proof of success.</p>
</li>
<li id="q-123-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Recover access, preserve events and re-read format/usability before resuming I/O; do not assume the old format when completion remains uncertain.</p>
</li>
<li id="q-123-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Configure buffers/PI after establishing current format and completion; any new Format must use current capability and scope.</p>
</li>
<li id="q-123-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Reset/power cycle do not roll back Format or guarantee old-data survival.</p>
</li>
<li id="q-123-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-123-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Format attribute changes follow namespace-change support/configuration and changed-list rules. <a class="qa-rule-link" href="#common-format_op-9">Full rule in this volume</a></p>
</li>
<li id="q-123-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Re-read namespace format/capacity and changed lists after success. <a class="qa-rule-link" href="#common-format_op-10">Full rule in this volume</a></p>
</li>
<li id="q-123-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>With supported PEL events, Format Start 07h records the request and Completion 08h the outcome. <a class="qa-rule-link" href="#common-format_op-11">Full rule in this volume</a></p>
</li>
<li id="q-123-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Controller Reset ends the old command channel. <a class="qa-rule-link" href="#common-format_op-12">Full rule in this volume</a></p>
</li>
<li id="q-123-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>After subsystem reset, recover access and inspect namespaces in the original format scope; one controller’s recovery does not establish all namespace outcomes. <a class="qa-rule-link" href="#common-format_op-13">Full rule in this volume</a></p>
</li>
<li id="q-123-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Without trustworthy successful completion before power interruption, reassess format and usability and, if needed, perform a valid new Format. <a class="qa-rule-link" href="#common-format_op-14">Full rule in this volume</a></p>
</li>
<li id="q-123-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Select FNA.FNS or SENS using SES, then combine it with NSID. <a class="qa-rule-link" href="#common-format_op-15">Full rule in this volume</a></p>
</li>
<li id="q-123-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Link the last trustworthy pre-reset evidence to the first recovered snapshot and mark the observation gap.</p>
</li>
<li id="q-123-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First establish whether a trustworthy Format success CQE exists; do not infer it solely from INFO=0.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-idns">NVM Command Set 1.3 §4.1.5.1–4.1.5.4</a> · <a href="#ref-format">Base 2.4 §5.1.1, 5.2.11</a> · <a href="#ref-nvmformat">NVM Command Set 1.3 §4.1.2</a> · <a href="#ref-formatpel">Base 2.4 §5.2.13.1.14.2.7–5.2.13.1.14.2.8</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-124" data-question="124"><h2><a class="qa-qid" href="#q-124">Q124</a> Which namespace data must be refreshed after Format?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-124-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-124-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Format changes I/O interpretation, requiring refreshed namespace caches rather than old block/PI settings.</p>
</li>
<li id="q-124-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Refresh format and capacity for affected namespaces; Format is not namespace creation/deletion and does not inherently assign a new NSID.</p>
</li>
<li id="q-124-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Query namespace and NVM-specific structures for FLBAS, DPS, LBAF, NSZE, NCAP and FPI.</p>
</li>
<li id="q-124-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>FLBAS reports active format/metadata transfer, DPS protection settings and NSZE/NCAP counts in new logical blocks.</p>
</li>
<li id="q-124-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Wait for Format success, refresh Identify and recalculate address/buffer layout, coordinating other accessors.</p>
</li>
<li id="q-124-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Readback must reflect the request; block-size changes can change counts, so identical counts are not a valid universal capacity test.</p>
</li>
<li id="q-124-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>For old-format readback after success, exclude wrong namespace, stale caching and mistaken scope.</p>
</li>
<li id="q-124-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-124-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Format attribute changes follow namespace-change support/configuration and changed-list rules. <a class="qa-rule-link" href="#common-format_op-9">Full rule in this volume</a></p>
</li>
<li id="q-124-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Re-read namespace format/capacity and changed lists after success. <a class="qa-rule-link" href="#common-format_op-10">Full rule in this volume</a></p>
</li>
<li id="q-124-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>With supported PEL events, Format Start 07h records the request and Completion 08h the outcome. <a class="qa-rule-link" href="#common-format_op-11">Full rule in this volume</a></p>
</li>
<li id="q-124-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Controller Reset ends the old command channel. <a class="qa-rule-link" href="#common-format_op-12">Full rule in this volume</a></p>
</li>
<li id="q-124-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>After subsystem reset, recover access and inspect namespaces in the original format scope; one controller’s recovery does not establish all namespace outcomes. <a class="qa-rule-link" href="#common-format_op-13">Full rule in this volume</a></p>
</li>
<li id="q-124-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Without trustworthy successful completion before power interruption, reassess format and usability and, if needed, perform a valid new Format. <a class="qa-rule-link" href="#common-format_op-14">Full rule in this volume</a></p>
</li>
<li id="q-124-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Select FNA.FNS or SENS using SES, then combine it with NSID. <a class="qa-rule-link" href="#common-format_op-15">Full rule in this volume</a></p>
</li>
<li id="q-124-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>When changing 512-byte to 4096-byte LBAs, compare byte capacity under allowed behavior rather than block counts alone.</p>
</li>
<li id="q-124-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First confirm a fresh Identify was issued instead of reading a pre-format buffer.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-idns">NVM Command Set 1.3 §4.1.5.1–4.1.5.4</a> · <a href="#ref-nvmformat">NVM Command Set 1.3 §4.1.2</a> · <a href="#ref-changedlog">Base 2.4 §5.2.13.1.5</a> · <a href="#ref-format">Base 2.4 §5.1.1, 5.2.11</a> · <a href="#ref-formatpel">Base 2.4 §5.2.13.1.14.2.7–5.2.13.1.14.2.8</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-125" data-question="125"><h2><a class="qa-qid" href="#q-125">Q125</a> How are Format failures checked using CQE, Error Log and PEL?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-125-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-125-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Distinguish validation rejection from failure after formatting began, which may already have changed data.</p>
</li>
<li id="q-125-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Evidence must match the same Format and scope, not a neighboring namespace operation.</p>
</li>
<li id="q-125-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Preserve SCT/SC/M/DNR and PEL support/validity.</p>
</li>
<li id="q-125-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>Correlate Error Log by IDs/count; Format Start preserves parameters and Completion carries FNVMS/INFO.</p>
</li>
<li id="q-125-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Read the CQE, additional information indicated by M, then PEL/current Identify; do not force one-to-one entries across all sources.</p>
</li>
<li id="q-125-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>A diagnosis establishes failure cause and current usability; retain uncertainty rather than assuming rollback.</p>
</li>
<li id="q-125-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Simultaneous faults may permit different statuses; INFO=0 can mean no CQE, requiring FNVMS interpretation.</p>
</li>
<li id="q-125-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-125-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Format attribute changes follow namespace-change support/configuration and changed-list rules. <a class="qa-rule-link" href="#common-format_op-9">Full rule in this volume</a></p>
</li>
<li id="q-125-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Re-read namespace format/capacity and changed lists after success. <a class="qa-rule-link" href="#common-format_op-10">Full rule in this volume</a></p>
</li>
<li id="q-125-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>With supported PEL events, Format Start 07h records the request and Completion 08h the outcome. <a class="qa-rule-link" href="#common-format_op-11">Full rule in this volume</a></p>
</li>
<li id="q-125-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Controller Reset ends the old command channel. <a class="qa-rule-link" href="#common-format_op-12">Full rule in this volume</a></p>
</li>
<li id="q-125-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>After subsystem reset, recover access and inspect namespaces in the original format scope; one controller’s recovery does not establish all namespace outcomes. <a class="qa-rule-link" href="#common-format_op-13">Full rule in this volume</a></p>
</li>
<li id="q-125-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Without trustworthy successful completion before power interruption, reassess format and usability and, if needed, perform a valid new Format. <a class="qa-rule-link" href="#common-format_op-14">Full rule in this volume</a></p>
</li>
<li id="q-125-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Select FNA.FNS or SENS using SES, then combine it with NSID. <a class="qa-rule-link" href="#common-format_op-15">Full rule in this volume</a></p>
</li>
<li id="q-125-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Compare parameters, result and current format to detect inconsistent controller or host interpretation.</p>
</li>
<li id="q-125-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First establish whether execution began and whether corresponding Start/Completion events exist.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-format">Base 2.4 §5.1.1, 5.2.11</a> · <a href="#ref-nvmformat">NVM Command Set 1.3 §4.1.2</a> · <a href="#ref-formatpel">Base 2.4 §5.2.13.1.14.2.7–5.2.13.1.14.2.8</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-126" data-question="126"><h2><a class="qa-qid" href="#q-126">Q126</a> How does SANICAP advertise sanitize methods?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-126-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-126-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>SANICAP advertises individual methods and extensions, not a Boolean enabling every sanitize action.</p>
</li>
<li id="q-126-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>CES/BES/OWS advertise subsystem methods; namespace sanitization has separate support and only Crypto Erase in this revision.</p>
</li>
<li id="q-126-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Read SANICAP and cross-check opcodes 84h/8Ch and LID 81h support.</p>
</li>
<li id="q-126-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>CES/BES/OWS select method support; no-deallocate attributes govern NDAS and VERS/NVERS govern verification for the two target types.</p>
</li>
<li id="q-126-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Match the required method to its bit before SANACT selection; BES alone does not authorize Overwrite.</p>
</li>
<li id="q-126-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Valid initiation succeeds with status updated; supported capability does not guarantee every background operation succeeds.</p>
</li>
<li id="q-126-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>A supported command with unsupported SANACT must return Invalid Field.</p>
</li>
<li id="q-126-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-126-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>State transitions report completed, unexpected-deallocation completion or media-verification entry with LID 81h. <a class="qa-rule-link" href="#common-sanitize_op-9">Full rule in this volume</a></p>
</li>
<li id="q-126-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Sanitize Status updates before the initiating CQE and on transitions, persisting across resets/power. <a class="qa-rule-link" href="#common-sanitize_op-10">Full rule in this volume</a></p>
</li>
<li id="q-126-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>Supported PEL logging records Start 09h on entering processing and Completion 0Ah on entering Idle or either failure state. <a class="qa-rule-link" href="#common-sanitize_op-11">Full rule in this volume</a></p>
</li>
<li id="q-126-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Background sanitization continues through Controller Level Reset. <a class="qa-rule-link" href="#common-sanitize_op-12">Full rule in this volume</a></p>
</li>
<li id="q-126-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Subsystem reset does not abort sanitization. <a class="qa-rule-link" href="#common-sanitize_op-13">Full rule in this volume</a></p>
</li>
<li id="q-126-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Processing cannot occur without power, but sanitization continues from retained state after power returns. <a class="qa-rule-link" href="#common-sanitize_op-14">Full rule in this volume</a></p>
</li>
<li id="q-126-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Subsystem sanitization restricts subsystem access; namespace sanitization targets one namespace across its controllers. <a class="qa-rule-link" href="#common-sanitize_op-15">Full rule in this volume</a></p>
</li>
<li id="q-126-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Controllers in the same subsystem must advertise consistent supported sanitize types for the corresponding command.</p>
</li>
<li id="q-126-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First inspect the method-specific bit rather than SANICAP being nonzero.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-sanitizecmd">Base 2.4 §5.2.26–5.2.27</a> · <a href="#ref-sanitizelog">Base 2.4 §5.2.13.1.38</a> · <a href="#ref-sanitizestate">Base 2.4 §8.1.27.1–8.1.27.5</a> · <a href="#ref-sanitizepel">Base 2.4 §5.2.13.1.14.2.9–5.2.13.1.14.2.10</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-127" data-question="127"><h2><a class="qa-qid" href="#q-127">Q127</a> How do NDAS, overwrite pattern, passes and inversion work?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-127-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-127-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Overwrite fields select pattern/passes while NDAS controls allocation release; erasure and deallocation are distinct.</p>
</li>
<li id="q-127-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>These overwrite/NDAS fields belong to subsystem Sanitize, not the namespace command layout.</p>
</li>
<li id="q-127-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Check OWS, no-deallocate inhibition/media-modification attributes and FID 17h.NODRM.</p>
</li>
<li id="q-127-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>SANACT3 selects Overwrite; OVRPAT is 32-bit, OWPASS0 means 16 passes and 1–15 their literal count; OIPBP1 inverts between passes.</p>
</li>
<li id="q-127-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>With patternAAAAAAAAh, two passes and inversion, the patterns areAAAAAAAAh then 55555555h; choose NDAS separately.</p>
</li>
<li id="q-127-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>After completion inspect SOS, completed passes and GDE; deallocated reads follow deallocation rules rather than guaranteeing the final pattern.</p>
</li>
<li id="q-127-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>With inhibited NDAS, NODRM0 rejects with Invalid Field; warning mode permits processing with unexpected-deallocation reporting. Non-overwrite actions ignore overwrite fields as defined.</p>
</li>
<li id="q-127-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-127-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>State transitions report completed, unexpected-deallocation completion or media-verification entry with LID 81h. <a class="qa-rule-link" href="#common-sanitize_op-9">Full rule in this volume</a></p>
</li>
<li id="q-127-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Sanitize Status updates before the initiating CQE and on transitions, persisting across resets/power. <a class="qa-rule-link" href="#common-sanitize_op-10">Full rule in this volume</a></p>
</li>
<li id="q-127-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>Supported PEL logging records Start 09h on entering processing and Completion 0Ah on entering Idle or either failure state. <a class="qa-rule-link" href="#common-sanitize_op-11">Full rule in this volume</a></p>
</li>
<li id="q-127-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Background sanitization continues through Controller Level Reset. <a class="qa-rule-link" href="#common-sanitize_op-12">Full rule in this volume</a></p>
</li>
<li id="q-127-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Subsystem reset does not abort sanitization. <a class="qa-rule-link" href="#common-sanitize_op-13">Full rule in this volume</a></p>
</li>
<li id="q-127-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Processing cannot occur without power, but sanitization continues from retained state after power returns. <a class="qa-rule-link" href="#common-sanitize_op-14">Full rule in this volume</a></p>
</li>
<li id="q-127-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Subsystem sanitization restricts subsystem access; namespace sanitization targets one namespace across its controllers. <a class="qa-rule-link" href="#common-sanitize_op-15">Full rule in this volume</a></p>
</li>
<li id="q-127-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Compare request fields and logged SCDW10/outcome; OWPASS0 does not mean zero work.</p>
</li>
<li id="q-127-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First check zero-pass encoding and NDAS validity before interpreting readback.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-sanitizeconfig">Base 2.4 §5.2.30.1.16</a> · <a href="#ref-nvmsanitize">NVM Command Set 1.3 §4.1.7, 5.12</a> · <a href="#ref-sanitizecmd">Base 2.4 §5.2.26–5.2.27</a> · <a href="#ref-sanitizelog">Base 2.4 §5.2.13.1.38</a> · <a href="#ref-sanitizestate">Base 2.4 §8.1.27.1–8.1.27.5</a> · <a href="#ref-sanitizepel">Base 2.4 §5.2.13.1.14.2.9–5.2.13.1.14.2.10</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-128" data-question="128"><h2><a class="qa-qid" href="#q-128">Q128</a> How are progress, status, state and erased-data flags interpreted together?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-128-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-128-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Progress, outcome, state and continued erased-data condition answer different questions; neitherFFFFh nor GDE1 alone proves full completion.</p>
</li>
<li id="q-128-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>LID 81h selects subsystem or namespace using NSID; NDE does not substitute for subsystem GDE.</p>
</li>
<li id="q-128-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Check sanitize/verification support and read a consistent snapshot for the same target.</p>
</li>
<li id="q-128-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>SPROG/65536 gives applicable-phase progress, SOS outcome/progress category, SANS state, and GDE/NDE the erased condition affected by later writes.</p>
</li>
<li id="q-128-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Read SOS, identify the active SANS phase, then interpret SPROG.</p>
</li>
<li id="q-128-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>SPROG8000h indicates 50% in an applicable processing phase; FFFFh also appears outside processing or during verification and is not standalone success.</p>
</li>
<li id="q-128-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Invalid targets and namespace queries during subsystem sanitization have distinct Invalid Namespace/Format and Sanitize In Progress conditions.</p>
</li>
<li id="q-128-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-128-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>State transitions report completed, unexpected-deallocation completion or media-verification entry with LID 81h. <a class="qa-rule-link" href="#common-sanitize_op-9">Full rule in this volume</a></p>
</li>
<li id="q-128-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Sanitize Status updates before the initiating CQE and on transitions, persisting across resets/power. <a class="qa-rule-link" href="#common-sanitize_op-10">Full rule in this volume</a></p>
</li>
<li id="q-128-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>Supported PEL logging records Start 09h on entering processing and Completion 0Ah on entering Idle or either failure state. <a class="qa-rule-link" href="#common-sanitize_op-11">Full rule in this volume</a></p>
</li>
<li id="q-128-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Background sanitization continues through Controller Level Reset. <a class="qa-rule-link" href="#common-sanitize_op-12">Full rule in this volume</a></p>
</li>
<li id="q-128-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Subsystem reset does not abort sanitization. <a class="qa-rule-link" href="#common-sanitize_op-13">Full rule in this volume</a></p>
</li>
<li id="q-128-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Processing cannot occur without power, but sanitization continues from retained state after power returns. <a class="qa-rule-link" href="#common-sanitize_op-14">Full rule in this volume</a></p>
</li>
<li id="q-128-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Subsystem sanitization restricts subsystem access; namespace sanitization targets one namespace across its controllers. <a class="qa-rule-link" href="#common-sanitize_op-15">Full rule in this volume</a></p>
</li>
<li id="q-128-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Match SCDW10 to the request and consider subsequent writes clearing GDE/NDE rather than mistaking an old result for the current operation.</p>
</li>
<li id="q-128-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First read SOS/SANS, then assess the progress value.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-nvmsanitize">NVM Command Set 1.3 §4.1.7, 5.12</a> · <a href="#ref-sanitizecmd">Base 2.4 §5.2.26–5.2.27</a> · <a href="#ref-sanitizelog">Base 2.4 §5.2.13.1.38</a> · <a href="#ref-sanitizestate">Base 2.4 §8.1.27.1–8.1.27.5</a> · <a href="#ref-sanitizepel">Base 2.4 §5.2.13.1.14.2.9–5.2.13.1.14.2.10</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-129" data-question="129"><h2><a class="qa-qid" href="#q-129">Q129</a> Which commands are permitted during subsystem sanitization?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-129-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-129-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Sanitization restricts user-data access while preserving essential management; permissions apply to commands, options and logs.</p>
</li>
<li id="q-129-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Restrictions apply across subsystem controllers; another controller is not a bypass.</p>
</li>
<li id="q-129-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Use Figure 144, the sanitize state machine and NVM Figures 200/201.</p>
</li>
<li id="q-129-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>Identify, AER, Get Features, queue management and selected logs remain available. PEL/vendor logs and self-test are prohibited; Error Log LBA returns zero.</p>
</li>
<li id="q-129-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Apply state, command and LID restrictions; Flush and media-verification reads have explicit exceptions to ordinary I/O blocking.</p>
</li>
<li id="q-129-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Allowed commands complete while prohibited commands are rejected and sanitization continues; avoid excessively frequent polling.</p>
</li>
<li id="q-129-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>In-progress rejection generally uses Sanitize In Progress; failure-state processing follows its command-specific rules.</p>
</li>
<li id="q-129-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-129-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>State transitions report completed, unexpected-deallocation completion or media-verification entry with LID 81h. <a class="qa-rule-link" href="#common-sanitize_op-9">Full rule in this volume</a></p>
</li>
<li id="q-129-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Sanitize Status updates before the initiating CQE and on transitions, persisting across resets/power. <a class="qa-rule-link" href="#common-sanitize_op-10">Full rule in this volume</a></p>
</li>
<li id="q-129-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>Supported PEL logging records Start 09h on entering processing and Completion 0Ah on entering Idle or either failure state. <a class="qa-rule-link" href="#common-sanitize_op-11">Full rule in this volume</a></p>
</li>
<li id="q-129-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Background sanitization continues through Controller Level Reset. <a class="qa-rule-link" href="#common-sanitize_op-12">Full rule in this volume</a></p>
</li>
<li id="q-129-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Subsystem reset does not abort sanitization. <a class="qa-rule-link" href="#common-sanitize_op-13">Full rule in this volume</a></p>
</li>
<li id="q-129-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Processing cannot occur without power, but sanitization continues from retained state after power returns. <a class="qa-rule-link" href="#common-sanitize_op-14">Full rule in this volume</a></p>
</li>
<li id="q-129-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Subsystem sanitization restricts subsystem access; namespace sanitization targets one namespace across its controllers. <a class="qa-rule-link" href="#common-sanitize_op-15">Full rule in this volume</a></p>
</li>
<li id="q-129-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Verify restrictions across controllers and permitted logs&#x27; sanitization of user-data fields.</p>
</li>
<li id="q-129-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First check the specific LID, not merely Get Log Page opcode permission.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-sanitizerestrict">Base 2.4 §5.1.1–5.1.2 (PCIe commands)</a> · <a href="#ref-nvmsanitize">NVM Command Set 1.3 §4.1.7, 5.12</a> · <a href="#ref-sanitizecmd">Base 2.4 §5.2.26–5.2.27</a> · <a href="#ref-sanitizelog">Base 2.4 §5.2.13.1.38</a> · <a href="#ref-sanitizestate">Base 2.4 §8.1.27.1–8.1.27.5</a> · <a href="#ref-sanitizepel">Base 2.4 §5.2.13.1.14.2.9–5.2.13.1.14.2.10</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-130" data-question="130"><h2><a class="qa-qid" href="#q-130">Q130</a> Does sanitization continue across reset or power loss?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-130-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-130-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Reset or power cycling must not provide an escape from sanitization; background processing continues across them.</p>
</li>
<li id="q-130-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>What persists is the target operation/state machine, not old Admin Queues or AER requests.</p>
</li>
<li id="q-130-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>After recovering access, inspect target NSID, SOS, SANS, SCDW10 and MVCNCLD.</p>
</li>
<li id="q-130-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>MVCNCLD reports cancelled media verification under specified transport/subsystem-reset conditions, not cancelled sanitization.</p>
</li>
<li id="q-130-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Preserve pre-reset state, re-read the same target and identify processing/deallocation/completion before attempting another operation.</p>
</li>
<li id="q-130-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Continuing or completed operation can be correct; no progress while unpowered is expected, but forgetting the operation is not.</p>
</li>
<li id="q-130-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>A new initiation during processing can be rejected as Sanitize In Progress without implying reset damage.</p>
</li>
<li id="q-130-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-130-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>State transitions report completed, unexpected-deallocation completion or media-verification entry with LID 81h. <a class="qa-rule-link" href="#common-sanitize_op-9">Full rule in this volume</a></p>
</li>
<li id="q-130-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Sanitize Status updates before the initiating CQE and on transitions, persisting across resets/power. <a class="qa-rule-link" href="#common-sanitize_op-10">Full rule in this volume</a></p>
</li>
<li id="q-130-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>Supported PEL logging records Start 09h on entering processing and Completion 0Ah on entering Idle or either failure state. <a class="qa-rule-link" href="#common-sanitize_op-11">Full rule in this volume</a></p>
</li>
<li id="q-130-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Background sanitization continues through Controller Level Reset. <a class="qa-rule-link" href="#common-sanitize_op-12">Full rule in this volume</a></p>
</li>
<li id="q-130-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Subsystem reset does not abort sanitization. <a class="qa-rule-link" href="#common-sanitize_op-13">Full rule in this volume</a></p>
</li>
<li id="q-130-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Processing cannot occur without power, but sanitization continues from retained state after power returns. <a class="qa-rule-link" href="#common-sanitize_op-14">Full rule in this volume</a></p>
</li>
<li id="q-130-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Subsystem sanitization restricts subsystem access; namespace sanitization targets one namespace across its controllers. <a class="qa-rule-link" href="#common-sanitize_op-15">Full rule in this volume</a></p>
</li>
<li id="q-130-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Verify parameter/target/state continuity separately from renewed AER and query setup.</p>
</li>
<li id="q-130-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First ensure the post-reset query addresses the original target.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-sanitizecmd">Base 2.4 §5.2.26–5.2.27</a> · <a href="#ref-sanitizelog">Base 2.4 §5.2.13.1.38</a> · <a href="#ref-sanitizestate">Base 2.4 §8.1.27.1–8.1.27.5</a> · <a href="#ref-sanitizepel">Base 2.4 §5.2.13.1.14.2.9–5.2.13.1.14.2.10</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-131" data-question="131"><h2><a class="qa-qid" href="#q-131">Q131</a> How do success, failure and failure mode differ in the log?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-131-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-131-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Outcome and current state differ: leaving failure mode can return to Idle while the latest sanitize outcome remains failed.</p>
</li>
<li id="q-131-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Use SOS/SANS for one target; namespace failure is not the subsystem’s last-operation result.</p>
</li>
<li id="q-131-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Read LID 81h and applicable FAILS/MVCNCLD to establish the failure stage.</p>
</li>
<li id="q-131-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>SOS001b means sanitized,010b sanitizing,011b failed and 100b sanitized with unexpected deallocation; SANS identifies the actual state.</p>
</li>
<li id="q-131-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Inspect outcome and current restrictions; Idle with failed SOS can follow valid Exit Failure Mode.</p>
</li>
<li id="q-131-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Neither progress alone nor the initiation CQE establishes the final background outcome.</p>
</li>
<li id="q-131-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Restricted and Unrestricted Failure allow different recovery actions despite both reporting failure.</p>
</li>
<li id="q-131-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-131-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>State transitions report completed, unexpected-deallocation completion or media-verification entry with LID 81h. <a class="qa-rule-link" href="#common-sanitize_op-9">Full rule in this volume</a></p>
</li>
<li id="q-131-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Sanitize Status updates before the initiating CQE and on transitions, persisting across resets/power. <a class="qa-rule-link" href="#common-sanitize_op-10">Full rule in this volume</a></p>
</li>
<li id="q-131-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>Supported PEL logging records Start 09h on entering processing and Completion 0Ah on entering Idle or either failure state. <a class="qa-rule-link" href="#common-sanitize_op-11">Full rule in this volume</a></p>
</li>
<li id="q-131-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Background sanitization continues through Controller Level Reset. <a class="qa-rule-link" href="#common-sanitize_op-12">Full rule in this volume</a></p>
</li>
<li id="q-131-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Subsystem reset does not abort sanitization. <a class="qa-rule-link" href="#common-sanitize_op-13">Full rule in this volume</a></p>
</li>
<li id="q-131-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Processing cannot occur without power, but sanitization continues from retained state after power returns. <a class="qa-rule-link" href="#common-sanitize_op-14">Full rule in this volume</a></p>
</li>
<li id="q-131-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Subsystem sanitization restricts subsystem access; namespace sanitization targets one namespace across its controllers. <a class="qa-rule-link" href="#common-sanitize_op-15">Full rule in this volume</a></p>
</li>
<li id="q-131-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Correlate SOS, SANS, original AUSE and recovery requests to identify invalid transitions.</p>
</li>
<li id="q-131-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First inspect SANS to distinguish current failure mode from historical failure outcome.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-sanitizecmd">Base 2.4 §5.2.26–5.2.27</a> · <a href="#ref-sanitizelog">Base 2.4 §5.2.13.1.38</a> · <a href="#ref-sanitizestate">Base 2.4 §8.1.27.1–8.1.27.5</a> · <a href="#ref-sanitizepel">Base 2.4 §5.2.13.1.14.2.9–5.2.13.1.14.2.10</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-132" data-question="132"><h2><a class="qa-qid" href="#q-132">Q132</a> What does Exit Failure Mode accomplish?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-132-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-132-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Where permitted, Exit Failure Mode releases failure-state restrictions; it neither finishes erasure nor converts failure into success.</p>
</li>
<li id="q-132-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>The action applies to the selected subsystem or namespace target.</p>
</li>
<li id="q-132-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Read SANS and original AUSE, which selects restricted versus unrestricted processing.</p>
</li>
<li id="q-132-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>SANACT001b requests Exit Failure Mode, not a new erasure operation.</p>
</li>
<li id="q-132-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Unrestricted Failure can transition to Idle; Restricted Failure requires a permitted new sanitize operation. The action in Idle is not an error.</p>
</li>
<li id="q-132-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Valid exit restores permitted access while SOS can retain failure; exit alone cannot establish GDE/NDE erasure.</p>
</li>
<li id="q-132-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Exit is rejected under restricted-failure rules; repeated requests or reset do not bypass them.</p>
</li>
<li id="q-132-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-132-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>State transitions report completed, unexpected-deallocation completion or media-verification entry with LID 81h. <a class="qa-rule-link" href="#common-sanitize_op-9">Full rule in this volume</a></p>
</li>
<li id="q-132-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Sanitize Status updates before the initiating CQE and on transitions, persisting across resets/power. <a class="qa-rule-link" href="#common-sanitize_op-10">Full rule in this volume</a></p>
</li>
<li id="q-132-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>Supported PEL logging records Start 09h on entering processing and Completion 0Ah on entering Idle or either failure state. <a class="qa-rule-link" href="#common-sanitize_op-11">Full rule in this volume</a></p>
</li>
<li id="q-132-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Background sanitization continues through Controller Level Reset. <a class="qa-rule-link" href="#common-sanitize_op-12">Full rule in this volume</a></p>
</li>
<li id="q-132-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Subsystem reset does not abort sanitization. <a class="qa-rule-link" href="#common-sanitize_op-13">Full rule in this volume</a></p>
</li>
<li id="q-132-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Processing cannot occur without power, but sanitization continues from retained state after power returns. <a class="qa-rule-link" href="#common-sanitize_op-14">Full rule in this volume</a></p>
</li>
<li id="q-132-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Subsystem sanitization restricts subsystem access; namespace sanitization targets one namespace across its controllers. <a class="qa-rule-link" href="#common-sanitize_op-15">Full rule in this volume</a></p>
</li>
<li id="q-132-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Verify both restored state and retained failure history rather than demanding all-zero logs.</p>
</li>
<li id="q-132-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First establish AUSE and SANS to determine whether exit is permitted.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-sanitizecmd">Base 2.4 §5.2.26–5.2.27</a> · <a href="#ref-sanitizelog">Base 2.4 §5.2.13.1.38</a> · <a href="#ref-sanitizestate">Base 2.4 §8.1.27.1–8.1.27.5</a> · <a href="#ref-sanitizepel">Base 2.4 §5.2.13.1.14.2.9–5.2.13.1.14.2.10</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-133" data-question="133"><h2><a class="qa-qid" href="#q-133">Q133</a> When are sanitize AERs and persistent events generated?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-133-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-133-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Notifications announce transitions and PEL retains history; neither is a second completion of the initiating command.</p>
</li>
<li id="q-133-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>The initiating controller reports the AER; event parameters and PEL.NSID identify the target.</p>
</li>
<li id="q-133-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Establish event/configuration support, outstanding AERs and PEL support.</p>
</li>
<li id="q-133-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>AET6/LID 81h use AEI01h for completion,02h unexpected deallocation and 03h verification entry; DW1 carries defined target information.</p>
</li>
<li id="q-133-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Record start at initiation, notify verification entry separately and record completion at Idle/failure transitions; read the same target after notification.</p>
</li>
<li id="q-133-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Completed notifications and PEL completion can describe failure; inspect SOS/SANS/SSTAT.</p>
</li>
<li id="q-133-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Without an AER request no immediate CQE is expected; normal retention/masking rules apply. Do not require PEL reads while prohibited during sanitization.</p>
</li>
<li id="q-133-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-133-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>State transitions report completed, unexpected-deallocation completion or media-verification entry with LID 81h. <a class="qa-rule-link" href="#common-sanitize_op-9">Full rule in this volume</a></p>
</li>
<li id="q-133-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Sanitize Status updates before the initiating CQE and on transitions, persisting across resets/power. <a class="qa-rule-link" href="#common-sanitize_op-10">Full rule in this volume</a></p>
</li>
<li id="q-133-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>Supported PEL logging records Start 09h on entering processing and Completion 0Ah on entering Idle or either failure state. <a class="qa-rule-link" href="#common-sanitize_op-11">Full rule in this volume</a></p>
</li>
<li id="q-133-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Background sanitization continues through Controller Level Reset. <a class="qa-rule-link" href="#common-sanitize_op-12">Full rule in this volume</a></p>
</li>
<li id="q-133-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Subsystem reset does not abort sanitization. <a class="qa-rule-link" href="#common-sanitize_op-13">Full rule in this volume</a></p>
</li>
<li id="q-133-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Processing cannot occur without power, but sanitization continues from retained state after power returns. <a class="qa-rule-link" href="#common-sanitize_op-14">Full rule in this volume</a></p>
</li>
<li id="q-133-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Subsystem sanitization restricts subsystem access; namespace sanitization targets one namespace across its controllers. <a class="qa-rule-link" href="#common-sanitize_op-15">Full rule in this volume</a></p>
</li>
<li id="q-133-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Correlate event target, initiating command and log state to distinguish notification loss from unfinished processing.</p>
</li>
<li id="q-133-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First check AEC, available requests and reporting controller before declaring a missing event.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-aerfull">Base 2.4 §5.2.2 (PCIe-applicable events)</a> · <a href="#ref-aec">Base 2.4 §5.2.30.1.6</a> · <a href="#ref-sanitizecmd">Base 2.4 §5.2.26–5.2.27</a> · <a href="#ref-sanitizelog">Base 2.4 §5.2.13.1.38</a> · <a href="#ref-sanitizestate">Base 2.4 §8.1.27.1–8.1.27.5</a> · <a href="#ref-sanitizepel">Base 2.4 §5.2.13.1.14.2.9–5.2.13.1.14.2.10</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-134" data-question="134"><h2><a class="qa-qid" href="#q-134">Q134</a> How is namespace sanitization targeted and isolated?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-134-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-134-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Namespace Sanitize provides a narrower Crypto Erase target while shared management restrictions remain separate from data isolation.</p>
</li>
<li id="q-134-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>NSID selects one active namespace, with restrictions applying across all controllers accessing it.</p>
</li>
<li id="q-134-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Check Admin opcode 8Ch CSUPP in LID 05h, then CES and any required NVERS/SPRRS capability; Q118 gives the lookup. Separately establish active namespace, protection and MNSOIP limits before claiming current eligibility.</p>
</li>
<li id="q-134-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>Use opcode 8Ch/SANACT100b; PREQ is CDW10 bit 4 rather than subsystem bit 11. Query that NSID’s LID 81h/NDE.</p>
</li>
<li id="q-134-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Snapshot target and non-target baselines, initiate and monitor the target, then verify erasure and preservation of non-target data.</p>
</li>
<li id="q-134-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Target NDE may become 1; sanitizing all namespaces still does not establish GDE because subsystem scope includes other locations.</p>
</li>
<li id="q-134-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Zero, broadcast, inactive or deleting namespaces use Invalid Namespace/Format; protection uses Namespace is Write Protected.</p>
</li>
<li id="q-134-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-134-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>State transitions report completed, unexpected-deallocation completion or media-verification entry with LID 81h. <a class="qa-rule-link" href="#common-sanitize_op-9">Full rule in this volume</a></p>
</li>
<li id="q-134-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Sanitize Status updates before the initiating CQE and on transitions, persisting across resets/power. <a class="qa-rule-link" href="#common-sanitize_op-10">Full rule in this volume</a></p>
</li>
<li id="q-134-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>Supported PEL logging records Start 09h on entering processing and Completion 0Ah on entering Idle or either failure state. <a class="qa-rule-link" href="#common-sanitize_op-11">Full rule in this volume</a></p>
</li>
<li id="q-134-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Background sanitization continues through Controller Level Reset. <a class="qa-rule-link" href="#common-sanitize_op-12">Full rule in this volume</a></p>
</li>
<li id="q-134-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Subsystem reset does not abort sanitization. <a class="qa-rule-link" href="#common-sanitize_op-13">Full rule in this volume</a></p>
</li>
<li id="q-134-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Processing cannot occur without power, but sanitization continues from retained state after power returns. <a class="qa-rule-link" href="#common-sanitize_op-14">Full rule in this volume</a></p>
</li>
<li id="q-134-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Subsystem sanitization restricts subsystem access; namespace sanitization targets one namespace across its controllers. <a class="qa-rule-link" href="#common-sanitize_op-15">Full rule in this volume</a></p>
</li>
<li id="q-134-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Validate non-target data, target I/O restrictions and shared firmware restrictions separately.</p>
</li>
<li id="q-134-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First verify opcode 8Ch and the intended NSID rather than subsystem opcode 84h.</p>
</li>
</ol>
<p class="qa-related">Related mechanisms: <a href="/nvme/question-bank/format-sanitize/en/#q-118">Q118</a></p>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-sanitizerestrict">Base 2.4 §5.1.1–5.1.2 (PCIe commands)</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-nsid">Base 2.4 §3.2.1</a> · <a href="#ref-sanitizecmd">Base 2.4 §5.2.26–5.2.27</a> · <a href="#ref-sanitizelog">Base 2.4 §5.2.13.1.38</a> · <a href="#ref-sanitizestate">Base 2.4 §8.1.27.1–8.1.27.5</a> · <a href="#ref-sanitizepel">Base 2.4 §5.2.13.1.14.2.9–5.2.13.1.14.2.10</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-commandseffects">Base 2.4 §5.2.13.1.6</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-135" data-question="135"><h2><a class="qa-qid" href="#q-135">Q135</a> How are invalid or unsupported namespace sanitize requests handled?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-135-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-135-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Unsupported command, invalid target/action and exhausted concurrency are distinct failure causes.</p>
</li>
<li id="q-135-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Check target and subsystem sanitize state; subsystem failure can block a new namespace operation.</p>
</li>
<li id="q-135-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>First use 8Ch CSUPP in LID 05h for command support, then SANICAP, namespace lists, protection and MNSOIP for method, target and concurrency conditions. These are distinct prerequisites.</p>
</li>
<li id="q-135-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>Namespace SANACT supports Crypto Erase and defined state-management actions;010b/011b are reserved.</p>
</li>
<li id="q-135-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Establish valid support, then isolate target, protection, action and concurrency negative tests with state snapshots.</p>
</li>
<li id="q-135-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>An unsuccessful initiation must not start sanitization, alter target Sanitize Status or alter user data for that command.</p>
</li>
<li id="q-135-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Invalid targets use Invalid Namespace/Format, actions Invalid Field and over-limit requests their named concurrency status. Figure 104 lists 3Ch while Figure 455 lists 12h: the source conflict prevents treating either as an undisputed sole acceptance value.</p>
</li>
<li id="q-135-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-135-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>State transitions report completed, unexpected-deallocation completion or media-verification entry with LID 81h. <a class="qa-rule-link" href="#common-sanitize_op-9">Full rule in this volume</a></p>
</li>
<li id="q-135-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Sanitize Status updates before the initiating CQE and on transitions, persisting across resets/power. <a class="qa-rule-link" href="#common-sanitize_op-10">Full rule in this volume</a></p>
</li>
<li id="q-135-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>Supported PEL logging records Start 09h on entering processing and Completion 0Ah on entering Idle or either failure state. <a class="qa-rule-link" href="#common-sanitize_op-11">Full rule in this volume</a></p>
</li>
<li id="q-135-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Background sanitization continues through Controller Level Reset. <a class="qa-rule-link" href="#common-sanitize_op-12">Full rule in this volume</a></p>
</li>
<li id="q-135-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Subsystem reset does not abort sanitization. <a class="qa-rule-link" href="#common-sanitize_op-13">Full rule in this volume</a></p>
</li>
<li id="q-135-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Processing cannot occur without power, but sanitization continues from retained state after power returns. <a class="qa-rule-link" href="#common-sanitize_op-14">Full rule in this volume</a></p>
</li>
<li id="q-135-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Subsystem sanitization restricts subsystem access; namespace sanitization targets one namespace across its controllers. <a class="qa-rule-link" href="#common-sanitize_op-15">Full rule in this volume</a></p>
</li>
<li id="q-135-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Verify both status and absence of operation/data changes for rejected requests.</p>
</li>
<li id="q-135-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First isolate the failed condition; preserve both source locations for the conflicting concurrency code.</p>
</li>
</ol>
<p class="qa-related">Related mechanisms: <a href="/nvme/question-bank/format-sanitize/en/#q-118">Q118</a></p>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-nsid">Base 2.4 §3.2.1</a> · <a href="#ref-nwp">Base 2.4 §5.2.30.1.38, 8.1.18</a> · <a href="#ref-sanitizecmd">Base 2.4 §5.2.26–5.2.27</a> · <a href="#ref-sanitizelog">Base 2.4 §5.2.13.1.38</a> · <a href="#ref-sanitizestate">Base 2.4 §8.1.27.1–8.1.27.5</a> · <a href="#ref-sanitizepel">Base 2.4 §5.2.13.1.14.2.9–5.2.13.1.14.2.10</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-commandseffects">Base 2.4 §5.2.13.1.6</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<section id="common-rules" class="qa-common"><h2>Shared rules linked from the answers</h2><p>Each shared mechanism is explained in full once in this volume. Use browser Back to return to the question; explicit command or feature exceptions take precedence.</p>
<article id="common-command-8"><h3>Command completion, events and records · How are DNR and More set?</h3><p>For a CQE, DNR=1 means the identical command is expected to fail if resubmitted to any controller in this subsystem; DNR=0 means it may succeed. Do not assign DNR=1 solely from an error name unless that condition mandates it. More=1 identifies additional information for this command in the Error Information Log. DNR should be zero when SCT=SC=0.</p></article>
<article id="common-format_op-9"><h3>Shared conditions for this topic · Is an asynchronous event generated?</h3><p>Format attribute changes follow namespace-change support/configuration and changed-list rules. Relevant FPI notifications concern zero/nonzero transitions, not every percentage update.</p></article>
<article id="common-format_op-10"><h3>Shared conditions for this topic · Are Error Information or other logs updated?</h3><p>Re-read namespace format/capacity and changed lists after success. For errors use CQE.More and Error Information; a successful Get Log does not substitute for Format completion.</p></article>
<article id="common-format_op-11"><h3>Shared conditions for this topic · Is it recorded in the Persistent Event Log?</h3><p>With supported PEL events, Format Start 07h records the request and Completion 08h the outcome. Read FNVMS with INFO; INFO can be zero when no Format CQE was reported and does not alone prove success.</p></article>
<article id="common-format_op-12"><h3>Shared conditions for this topic · What survives or continues after Controller Reset?</h3><p>Controller Reset ends the old command channel. Re-read format, FPI and available Format Completion events after recovery; reset proves neither format success nor rollback.</p></article>
<article id="common-format_op-13"><h3>Shared conditions for this topic · What survives or continues after NVM Subsystem Reset?</h3><p>After subsystem reset, recover access and inspect namespaces in the original format scope; one controller’s recovery does not establish all namespace outcomes.</p></article>
<article id="common-format_op-14"><h3>Shared conditions for this topic · What survives or continues after a power cycle?</h3><p>Without trustworthy successful completion before power interruption, reassess format and usability and, if needed, perform a valid new Format. Missing success does not imply old data survived.</p></article>
<article id="common-format_op-15"><h3>Shared conditions for this topic · Are other controllers or namespaces affected?</h3><p>Select FNA.FNS or SENS using SES, then combine it with NSID. Coordinate other access paths to shared namespaces; submission to one controller does not imply controller-local data impact.</p></article>
<article id="common-identify-12"><h3>Query reset and scope · What survives or continues after Controller Reset?</h3><p>Controller Reset stops an outstanding query; a missing response is not an all-zero result. Re-read after recovery, distinguishing identity, configuration and dynamic state by field. Reset alone does not mean the namespace was deleted.</p></article>
<article id="common-identify-13"><h3>Query reset and scope · What survives or continues after NVM Subsystem Reset?</h3><p>Rediscover affected controllers and namespaces after reset. An NVM Subsystem Reset does not by itself imply that all storage configuration returns to manufacturing defaults. Verify changes caused by any separate management operation.</p></article>
<article id="common-identify-14"><h3>Query reset and scope · What survives or continues after a power cycle?</h3><p>After a power cycle, re-read version, capabilities, current format and attachment lists. Stable identity and persistent configuration are not ordinary volatile feature values. Firmware activation or configuration changes require before/after snapshots and event timing.</p></article>
<article id="common-identify-15"><h3>Query reset and scope · Are other controllers or namespaces affected?</h3><p>Identify reads data; it does not create, format or attach a namespace. CNS and selectors determine the view. Active lists may differ across controllers, so different lists do not alone establish corruption.</p></article>
<article id="common-sanitize_op-9"><h3>Shared conditions for this topic · Is an asynchronous event generated?</h3><p>State transitions report completed, unexpected-deallocation completion or media-verification entry with LID 81h. For Admin-SQ initiation, only the initiating controller reports the event; inspect the log for actual outcome.</p></article>
<article id="common-sanitize_op-10"><h3>Shared conditions for this topic · Are Error Information or other logs updated?</h3><p>Sanitize Status updates before the initiating CQE and on transitions, persisting across resets/power. Match target, SOS, SANS, SPROG, SCDW10 and GDE/NDE; background failure does not require a second initiation CQE.</p></article>
<article id="common-sanitize_op-11"><h3>Shared conditions for this topic · Is it recorded in the Persistent Event Log?</h3><p>Supported PEL logging records Start 09h on entering processing and Completion 0Ah on entering Idle or either failure state. Completion includes failures; NSID distinguishes subsystem and namespace targets.</p></article>
<article id="common-sanitize_op-12"><h3>Shared conditions for this topic · What survives or continues after Controller Reset?</h3><p>Background sanitization continues through Controller Level Reset. Re-read target LID 81h after recovery. Some reset sources cancel media verification and set MVCNCLD without cancelling the entire sanitize operation.</p></article>
<article id="common-sanitize_op-13"><h3>Shared conditions for this topic · What survives or continues after NVM Subsystem Reset?</h3><p>Subsystem reset does not abort sanitization. Preserve operation/log state and check MVCNCLD and post-verification deallocation when verification was requested.</p></article>
<article id="common-sanitize_op-14"><h3>Shared conditions for this topic · What survives or continues after a power cycle?</h3><p>Processing cannot occur without power, but sanitization continues from retained state after power returns. Inspect SOS/SANS and progress; SPROG=FFFFh alone is not success.</p></article>
<article id="common-sanitize_op-15"><h3>Shared conditions for this topic · Are other controllers or namespaces affected?</h3><p>Subsystem sanitization restricts subsystem access; namespace sanitization targets one namespace across its controllers. Shared operations such as firmware update have additional restrictions even when other namespace data is not erased.</p></article>
</section>
<section id="source-index"><h2>Source locations and existing figure guides</h2><p>Base printed page = PDF page−26; the other two use identical numbers. Locations follow the supplied PDF body and retain figure numbers. Shared pages contribute only the relevant definitions, excluding Fabrics and PCIe link/packet content.</p><ul class="qa-references">
<li id="ref-adminsupport"><strong>Base 2.4 · §3.1.3.4 (Figure 28 PCIe I/O-controller rows and O/M/P note only)</strong><br>Printed pages 45–47 · PDF 71–73 · Figure 28</li>
<li id="ref-nsid"><strong>Base 2.4 · §3.2.1</strong><br>Printed pages 78–81 · PDF 104–107</li>
<li id="ref-reset"><strong>Base 2.4 · §3.7.1–3.7.4</strong><br>Printed pages 120–124 · PDF 146–150</li>
<li id="ref-status"><strong>Base 2.4 · §4.2.3</strong><br>Printed pages 145–155 · PDF 171–181 · Figure 101–105</li>
<li id="ref-format"><strong>Base 2.4 · §5.1.1, 5.2.11</strong><br>Printed pages 178–179, 206–209 · PDF 204–205, 232–235 · Figure 144, 194–196</li>
<li id="ref-sanitizerestrict"><strong>Base 2.4 · §5.1.1–5.1.2 (PCIe commands)</strong><br>Printed pages 178–181 · PDF 204–207 · Figure 144–146</li>
<li id="ref-aer"><strong>Base 2.4 · §5.2.2</strong><br>Printed pages 183–190 · PDF 209–216 · Figure 150–156</li>
<li id="ref-aerfull"><strong>Base 2.4 · §5.2.2 (PCIe-applicable events)</strong><br>Printed pages 183–191 · PDF 209–217 · Figure 150–160</li>
<li id="ref-getlog"><strong>Base 2.4 · §5.2.13–5.2.13.1.1</strong><br>Printed pages 212–218 · PDF 238–244 · Figure 203–211</li>
<li id="ref-error"><strong>Base 2.4 · §5.2.13.1.2</strong><br>Printed pages 218–220 · PDF 244–246 · Figure 212</li>
<li id="ref-changedlog"><strong>Base 2.4 · §5.2.13.1.5</strong><br>Printed pages 226 · PDF 252</li>
<li id="ref-commandseffects"><strong>Base 2.4 · §5.2.13.1.6</strong><br>Printed pages 226–229 · PDF 252–255 · Figure 216–217</li>
<li id="ref-pel"><strong>Base 2.4 · §5.2.13.1.14 (header, reset, hardware, Set Feature events)</strong><br>Printed pages 244–256, 258, 262–264 · PDF 270–282, 284, 288–290 · Figure 232–244, 246, 252–253</li>
<li id="ref-formatpel"><strong>Base 2.4 · §5.2.13.1.14.2.7–5.2.13.1.14.2.8</strong><br>Printed pages 259–261 · PDF 285–287 · Figure 248–249</li>
<li id="ref-sanitizepel"><strong>Base 2.4 · §5.2.13.1.14.2.9–5.2.13.1.14.2.10</strong><br>Printed pages 261–262 · PDF 287–288 · Figure 250–251</li>
<li id="ref-sanitizelog"><strong>Base 2.4 · §5.2.13.1.38</strong><br>Printed pages 313–320 · PDF 339–346 · Figure 312</li>
<li id="ref-idcmd"><strong>Base 2.4 · §5.2.14.1</strong><br>Printed pages 336–340 · PDF 362–366 · Figure 332–337</li>
<li id="ref-idctrl"><strong>Base 2.4 · §5.2.14.2.1</strong><br>Printed pages 340–387 · PDF 366–413 · Figure 338–341</li>
<li id="ref-sanitizecmd"><strong>Base 2.4 · §5.2.26–5.2.27</strong><br>Printed pages 448–454 · PDF 474–480 · Figure 451–455</li>
<li id="ref-aec"><strong>Base 2.4 · §5.2.30.1.6</strong><br>Printed pages 466–468 · PDF 492–494 · Figure 474</li>
<li id="ref-behavior"><strong>Base 2.4 · §5.2.30.1.15</strong><br>Printed pages 475–477 · PDF 501–503 · Figure 491</li>
<li id="ref-sanitizeconfig"><strong>Base 2.4 · §5.2.30.1.16</strong><br>Printed pages 477–478 · PDF 503–504 · Figure 492</li>
<li id="ref-nwp"><strong>Base 2.4 · §5.2.30.1.38, 8.1.18</strong><br>Printed pages 512, 664–666 · PDF 538, 690–692 · Figure 541, 735–737</li>
<li id="ref-sanitizestate"><strong>Base 2.4 · §8.1.27.1–8.1.27.5</strong><br>Printed pages 711–732 · PDF 737–758 · Figure 770–779</li>
<li id="ref-nvmformat"><strong>NVM Command Set 1.3 · §4.1.2</strong><br>Printed pages 62–63 · PDF 62–63 · Figure 91</li>
<li id="ref-idns"><strong>NVM Command Set 1.3 · §4.1.5.1–4.1.5.4</strong><br>Printed pages 84–107 · PDF 84–107 · Figure 123–130</li>
<li id="ref-nvmsanitize"><strong>NVM Command Set 1.3 · §4.1.7, 5.12</strong><br>Printed pages 113, 173–175 · PDF 113, 173–175 · Figure 200–201</li>
</ul><h3>When you need a field guide</h3><p>Existing figure explanations have canonical locations; use these links instead of duplicating the same guide.</p><ul>
<li><a href="/nvme/figure-reference/command/en/#figure-b101">Base 2.4 Figure 101 · Completion Queue Entry: Status Field</a></li>
<li><a href="/nvme/figure-reference/command/en/#figure-b104">Base 2.4 Figure 104 · Status Code – Command Specific Status Values</a></li>
<li><a href="/nvme/figure-reference/logs/en/#figure-b217">Base 2.4 Figure 217 · Commands Supported and Effects Data Structure</a></li>
<li><a href="/nvme/figure-reference/identify/en/#figure-b338">Base 2.4 Figure 338 · Identify – Identify Controller Data Structure, I/O Command Set Independent</a></li>
<li><a href="/nvme/figure-reference/identify/en/#figure-n123">NVM Command Set 1.3 Figure 123 · Identify – Identify Namespace Data Structure, NVM Command Set</a></li>
</ul><details><summary>Original documents used</summary><ul class="qr-sources">
<li>NVM Express Base Specification · Revision 2.4 · 2026-07-31<br><code>NVM-Express-Base-Specification-Revision-2.4-Ratified-2026.07.31.pdf</code></li>
<li>NVM Express NVM Command Set Specification · Revision 1.3 · 2026-07-31<br><code>NVM-Express-NVM-Command-Set-Specification-Revision-1.3-Ratified-2026.07.31.pdf</code></li>
<li>NVM Express NVMe over PCIe Transport Specification · Revision 1.4 · 2026-07-31<br><code>NVM-Express-NVMe-over-PCIe-Transport-Specification-Revision-1.4-Ratified-2026.07.31.pdf</code></li>
</ul></details></section>
</main>
<nav class="qr-top" aria-label="Bank and editions"><a href="#content">Skip to content</a><a href="/nvme/question-bank/en/">Question index</a><a href="/nvme/question-bank/format-sanitize/zh-tw/">繁體中文</a><a href="/DOCS/nvme-question-bank/format-sanitize.html">Chinese tutorial HTML</a></nav>
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
