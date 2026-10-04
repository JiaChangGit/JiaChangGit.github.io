---
layout: post
title: "NVMe Self-Study Bank: Identify and capability discovery"
date: 2026-10-01 00:00:00 +0800
categories: [nvme]
permalink: /nvme/question-bank/identify/en/
lang: en
nvme_quickref: true
nvme_qa: true
---

<div class="nvme-quickref nvme-qa">
<nav class="qr-top" aria-label="Bank and editions"><a href="#content">Skip to content</a><a href="/nvme/question-bank/en/">Question index</a><a href="/nvme/question-bank/identify/zh-tw/">繁體中文</a><a href="/DOCS/nvme-question-bank/identify.html">Chinese tutorial HTML</a></nav>
<main id="content"><p class="qr-eyebrow">BASE 2.4 / NVM 1.3 / PCIe 1.4 · Q1–328</p>
<header><p class="qa-range">Q44–Q53</p><h1>Identify and capability discovery</h1><p class="qr-intro">Treat Identify as several distinct query interfaces. Choose the object and structure before CNS, CSI, NSID and other selectors. Separate capability, current configuration and changing lists to find real contradictions.</p><p>Practice first, then reveal 17 answer items per question. All numerical examples are hypothetical. Status is written SCT/SC; h indicates hexadecimal.</p></header>
<aside class="qa-glossary"><h2>Terms used in this volume</h2><dl><dt>Controller / namespace</dt><dd>A controller receives commands and manages access. A namespace is a logical storage space that commands can address. An NVM subsystem contains controllers and nonvolatile storage resources.</dd><dt>SQ / CQ / SQE / CQE</dt><dd>Submission and Completion Queues carry command entries (SQEs) and completion entries (CQEs). QID identifies a queue, CID distinguishes outstanding commands in one SQ, and NSID identifies a namespace.</dd><dt>Register / Identify / Feature / Log</dt><dd>A register exposes control or state. Identify queries capabilities and attributes; features query or configure operation; log pages report specific state or records. FID, LID, CNS and CSI select features, logs, Identify structures and command sets.</dd><dt>index / offset / zero-based</dt><dd>An index selects an entry, usually starting at 0; an offset measures distance from an origin in specified units. A zero-based count encodes count−1, but not every zero-valued field is a count. A Dword is 4 bytes; a byte is 8 bits.</dd><dt>Scope / reset / retention</dt><dd>Scope names the affected objects; retention means preserving state. Controller Reset (clearing CC.EN) is one form of Controller Level Reset, or CLR. Different CLR triggers can retain different registers.</dd></dl></aside>
<section id="overview" class="qa-overview"><h2>Choose the question before the Identify structure</h2><p class="qa-takeaway">Different CNS values answer different questions; allocated does not automatically mean accessible through this controller.</p>
<div class="qr-table" tabindex="0" role="region" aria-label="Horizontally scrollable comparison table"><table><thead><tr><th scope="col">Question</th><th scope="col">Query</th><th scope="col">How to use the response</th></tr></thead><tbody><tr><td>Advertised controller capability</td><td>CNS=01h</td><td>Read OACS, ONCS, MDTS and their field conditions</td></tr><tr><td>Currently active namespaces</td><td>CNS=02h</td><td>Active list, not all allocated capacity</td></tr><tr><td>Allocated namespaces</td><td>CNS=10h with Namespace Management support</td><td>May include namespaces not attached to this controller</td></tr><tr><td>Format of one NVM namespace</td><td>CNS=00h; additionally CNS=05h, CSI=00h when applicable</td><td>Interpret NSZE/NCAP, FLBAS, LBAF and PI together</td></tr><tr><td>Command-set-independent namespace properties</td><td>CNS=08h</td><td>Keep separate from the NVM-specific LBA format structure</td></tr></tbody></table></div>
<p><strong>Worked interpretation: </strong>If Allocated={1,2} and this controller’s Active={1}, namespace 2 is absent from this active list; that does not establish deletion. Check attachment and relevant state, preserving controller identity and query time.</p>
<p class="qa-citations">Sources: <a href="#ref-idcmd">Base 2.4 §5.2.14.1</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-idns">NVM Command Set 1.3 §4.1.5.1–4.1.5.4</a> · <a href="#ref-nsmanage">Base 2.4 §5.2.24–5.2.25, 8.1.17</a></p>
</section>
<div class="qa-controls" hidden><label>Search this page <input type="search" id="qa-search" placeholder="Question number, field or keyword"></label><button type="button" data-expand="true">Expand all answers</button><button type="button" data-expand="false">Collapse all answers</button><output id="qa-count" aria-live="polite"></output></div>
<section id="question-index"><h2>Questions in this volume</h2><ol class="qa-index">
<li><a href="#q-044">Q44 · What important information is provided by Identify Controller and Identify Namespace?</a></li>
<li><a href="#q-045">Q45 · How do active, allocated and namespace descriptor lists differ?</a></li>
<li><a href="#q-046">Q46 · What are Controller Lists, the UUID List and I/O Command Set Identify data used for?</a></li>
<li><a href="#q-047">Q47 · Which Identify structures describe NVM Sets, Endurance Groups, Domains and Secondary Controllers?</a></li>
<li><a href="#q-048">Q48 · How should unsupported or invalid CNS, CSI, NSID and UUID Index values be handled?</a></li>
<li><a href="#q-049">Q49 · How are SN, MN, FR, MDTS and optional Admin capability fields interpreted?</a></li>
<li><a href="#q-050">Q50 · How can advertised Identify support be cross-checked against commands and the Commands Supported and Effects Log?</a></li>
<li><a href="#q-051">Q51 · Which Identify data and lists change after namespace creation, deletion, attachment, detachment or format?</a></li>
<li><a href="#q-052">Q52 · Which Identify data may change after firmware activation, reset or power cycling?</a></li>
<li><a href="#q-053">Q53 · How should inconsistencies among Identify, features, logs and command behavior be investigated?</a></li>
</ol></section>
<article class="qa-question" id="q-044" data-question="44"><h2><a class="qa-qid" href="#q-044">Q44</a> What important information is provided by Identify Controller and Identify Namespace?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-044-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-044-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Separate controller capability from a particular namespace&#x27;s capacity, format and protection configuration.</p>
</li>
<li id="q-044-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Controller data describes the receiving controller&#x27;s view; NSID/CNS/CSI select namespace information.</p>
</li>
<li id="q-044-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Main entry points are CNS 01h Controller and CNS 00h NVM Namespace; CNS 05h/06h are command-set specific, while CNS 08h is command-set independent Namespace data.</p>
</li>
<li id="q-044-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>Controller fields include SN/MN/FR, MDTS, OACS/ONCS, LPA and SQES/CQES. NVM Namespace includes NSZE/NCAP/NUSE, FLBAS/LBAF, MC/DPC/DPS, atomicity and group identifiers.</p>
</li>
<li id="q-044-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Read Controller and the active list, then the applicable structures for each namespace. Convert block counts using the currently selected LBA format.</p>
</li>
<li id="q-044-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Identify returns a 4096-byte structure and successful CQE. NSZE=8192 and LBADS=12 describe 32 MiB of logical address space.</p>
</li>
<li id="q-044-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Unsupported CNS uses Invalid Field (0/02h); an incompatible namespace command set uses Invalid I/O Command Set (1/2Ch). Apply CNS-specific NSID rules.</p>
</li>
<li id="q-044-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-044-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Normal completion here does not guarantee an AER; a separate defined event requires support, configuration and a pending request. <a class="qa-rule-link" href="#common-command-9">Full rule in this volume</a></p>
</li>
<li id="q-044-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Correlate the completion with error records under the shared entry-creation rules; do not infer entry count directly from the number of failures. <a class="qa-rule-link" href="#common-command-10">Full rule in this volume</a></p>
</li>
<li id="q-044-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>PEL is not a per-command trace; supported defined events are logged under their recording conditions. <a class="qa-rule-link" href="#common-command-11">Full rule in this volume</a></p>
</li>
<li id="q-044-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Repeat an interrupted query and distinguish identity, configuration and dynamic fields. <a class="qa-rule-link" href="#common-identify-12">Full rule in this volume</a></p>
</li>
<li id="q-044-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Rediscover affected objects; reset alone does not mean namespace deletion or factory configuration. <a class="qa-rule-link" href="#common-identify-13">Full rule in this volume</a></p>
</li>
<li id="q-044-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Re-read and compare, separating firmware activation or management changes from power cycling alone. <a class="qa-rule-link" href="#common-identify-14">Full rule in this volume</a></p>
</li>
<li id="q-044-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Identify is read-only; active lists may differ by controller, so compare matching query targets. <a class="qa-rule-link" href="#common-identify-15">Full rule in this volume</a></p>
</li>
<li id="q-044-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Controller opcode support does not make every namespace format or current state suitable; both levels must permit the operation.</p>
</li>
<li id="q-044-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First identify the returned CNS structure; do not decode CNS 08h with the CNS 00h layout.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-idcmd">Base 2.4 §5.2.14.1</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-idns">NVM Command Set 1.3 §4.1.5.1–4.1.5.4</a> · <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-045" data-question="45"><h2><a class="qa-qid" href="#q-045">Q45</a> How do active, allocated and namespace descriptor lists differ?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-045-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-045-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Separate accessibility through this controller, allocation/existence and the identity of one namespace.</p>
</li>
<li id="q-045-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>The active list is controller-relative; the allocated list can include unattached namespaces; descriptors describe one NSID.</p>
</li>
<li id="q-045-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>CNS 02h queries active IDs, CNS 10h allocated IDs and CNS 03h namespace identification descriptors. Allocation queries depend on Namespace Management support.</p>
</li>
<li id="q-045-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>List NSID is a pagination cursor returning greater IDs. Descriptors contain NIDT/NIDL/NID for identifiers such as EUI64, NGUID, UUID and CSI.</p>
</li>
<li id="q-045-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Start list enumeration at NSID=0 and continue from returned IDs; for a descriptor query NSID selects the target, not a cursor.</p>
</li>
<li id="q-045-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Allocated={1,3,8} and Active={1,8} mean namespace 3 is allocated but not active here, not necessarily damaged.</p>
</li>
<li id="q-045-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>CNS 02h/10h cursors FFFFFFFEh or FFFFFFFFh shall return Invalid Namespace or Format (0/0Bh); unsupported CNS uses 0/02h.</p>
</li>
<li id="q-045-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-045-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Normal completion here does not guarantee an AER; a separate defined event requires support, configuration and a pending request. <a class="qa-rule-link" href="#common-command-9">Full rule in this volume</a></p>
</li>
<li id="q-045-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Correlate the completion with error records under the shared entry-creation rules; do not infer entry count directly from the number of failures. <a class="qa-rule-link" href="#common-command-10">Full rule in this volume</a></p>
</li>
<li id="q-045-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>PEL is not a per-command trace; supported defined events are logged under their recording conditions. <a class="qa-rule-link" href="#common-command-11">Full rule in this volume</a></p>
</li>
<li id="q-045-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Repeat an interrupted query and distinguish identity, configuration and dynamic fields. <a class="qa-rule-link" href="#common-identify-12">Full rule in this volume</a></p>
</li>
<li id="q-045-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Rediscover affected objects; reset alone does not mean namespace deletion or factory configuration. <a class="qa-rule-link" href="#common-identify-13">Full rule in this volume</a></p>
</li>
<li id="q-045-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Re-read and compare, separating firmware activation or management changes from power cycling alone. <a class="qa-rule-link" href="#common-identify-14">Full rule in this volume</a></p>
</li>
<li id="q-045-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Identify is read-only; active lists may differ by controller, so compare matching query targets. <a class="qa-rule-link" href="#common-identify-15">Full rule in this volume</a></p>
</li>
<li id="q-045-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Correlate stable descriptor identifiers rather than assuming NSIDs never change. Restart enumeration when configuration changes compromise a consistent view.</p>
</li>
<li id="q-045-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First determine whether NSID is a target or a start-after cursor.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-nsid">Base 2.4 §3.2.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-046" data-question="46"><h2><a class="qa-qid" href="#q-046">Q46</a> What are Controller Lists, the UUID List and I/O Command Set Identify data used for?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-046-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-046-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Answer three different questions: which controllers can access, which vendor definition to use and which command sets can operate together.</p>
</li>
<li id="q-046-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Controller Lists describe relationships. The UUID List selects vendor-specific information and is not the namespace UUID descriptor.</p>
</li>
<li id="q-046-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>CNS 12h lists controllers attached to a namespace, 13h subsystem I/O controllers, 17h the UUID List and 1Ch command-set combinations.</p>
</li>
<li id="q-046-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>CNTID is a list cursor or CNS-specific target; UIDX=0 selects no UUID. Each CNS 1Ch vector describes a simultaneously supported set combination.</p>
</li>
<li id="q-046-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Select CNS and selectors for the question. After CNS 1Ch discovery, FID 19h.IOCSCI selects the combination index, not the CSI bitmap itself.</p>
</li>
<li id="q-046-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Lists return identities/counts or UUID entries; command-set vectors advertise available combinations without automatically enabling them.</p>
</li>
<li id="q-046-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Unsupported CNS and CNS 12h NSID=FFFFFFFFh use 0/02h. Illegal UUID selection follows §8.1.31, not namespace-absence rules.</p>
</li>
<li id="q-046-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-046-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Normal completion here does not guarantee an AER; a separate defined event requires support, configuration and a pending request. <a class="qa-rule-link" href="#common-command-9">Full rule in this volume</a></p>
</li>
<li id="q-046-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Correlate the completion with error records under the shared entry-creation rules; do not infer entry count directly from the number of failures. <a class="qa-rule-link" href="#common-command-10">Full rule in this volume</a></p>
</li>
<li id="q-046-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>PEL is not a per-command trace; supported defined events are logged under their recording conditions. <a class="qa-rule-link" href="#common-command-11">Full rule in this volume</a></p>
</li>
<li id="q-046-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Repeat an interrupted query and distinguish identity, configuration and dynamic fields. <a class="qa-rule-link" href="#common-identify-12">Full rule in this volume</a></p>
</li>
<li id="q-046-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Rediscover affected objects; reset alone does not mean namespace deletion or factory configuration. <a class="qa-rule-link" href="#common-identify-13">Full rule in this volume</a></p>
</li>
<li id="q-046-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Re-read and compare, separating firmware activation or management changes from power cycling alone. <a class="qa-rule-link" href="#common-identify-14">Full rule in this volume</a></p>
</li>
<li id="q-046-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Identify is read-only; active lists may differ by controller, so compare matching query targets. <a class="qa-rule-link" href="#common-identify-15">Full rule in this volume</a></p>
</li>
<li id="q-046-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Keep CNTID and NSID roles separate and verify that FID 19h Current selects the intended vector.</p>
</li>
<li id="q-046-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First confirm that UIDX is a UUID List index, not the UUID value or an NSID.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-idcmd">Base 2.4 §5.2.14.1</a> · <a href="#ref-uuid">Base 2.4 §8.1.31.1–8.1.31.2</a> · <a href="#ref-profile">Base 2.4 §5.2.30.1.18</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-047" data-question="47"><h2><a class="qa-qid" href="#q-047">Q47</a> Which Identify structures describe NVM Sets, Endurance Groups, Domains and Secondary Controllers?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-047-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-047-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Establish resource membership instead of treating sets, groups, domains and controllers as interchangeable objects.</p>
</li>
<li id="q-047-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Each list has its own IDs and capacity/resource fields. This question discovers information rather than changing capacity or virtualization state.</p>
</li>
<li id="q-047-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Check relevant CTRATT capabilities and OACS.VMS. CNS 04h,19h,18h and 14h/15h describe sets, endurance groups, domains and primary/secondary controllers respectively.</p>
</li>
<li id="q-047-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>Set attributes include ENDGID; namespace data includes NVMSETID/ENDGID; domain entries include DID/TDC/UDC; secondary entries include SCID/PCID, state and VQ/VI counts.</p>
</li>
<li id="q-047-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Trace namespace membership through sets/groups, domain capacity and primary/secondary resource information for allocated queues and interrupts.</p>
</li>
<li id="q-047-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Results provide related IDs/attributes. A zero field is not always a zero resource count; first establish support and field validity.</p>
</li>
<li id="q-047-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Unsupported CNS uses 0/02h; cursors beyond existing IDs may return empty lists rather than errors.</p>
</li>
<li id="q-047-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-047-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Normal completion here does not guarantee an AER; a separate defined event requires support, configuration and a pending request. <a class="qa-rule-link" href="#common-command-9">Full rule in this volume</a></p>
</li>
<li id="q-047-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Correlate the completion with error records under the shared entry-creation rules; do not infer entry count directly from the number of failures. <a class="qa-rule-link" href="#common-command-10">Full rule in this volume</a></p>
</li>
<li id="q-047-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>PEL is not a per-command trace; supported defined events are logged under their recording conditions. <a class="qa-rule-link" href="#common-command-11">Full rule in this volume</a></p>
</li>
<li id="q-047-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Repeat an interrupted query and distinguish identity, configuration and dynamic fields. <a class="qa-rule-link" href="#common-identify-12">Full rule in this volume</a></p>
</li>
<li id="q-047-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Rediscover affected objects; reset alone does not mean namespace deletion or factory configuration. <a class="qa-rule-link" href="#common-identify-13">Full rule in this volume</a></p>
</li>
<li id="q-047-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Re-read and compare, separating firmware activation or management changes from power cycling alone. <a class="qa-rule-link" href="#common-identify-14">Full rule in this volume</a></p>
</li>
<li id="q-047-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Identify is read-only; active lists may differ by controller, so compare matching query targets. <a class="qa-rule-link" href="#common-identify-15">Full rule in this volume</a></p>
</li>
<li id="q-047-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Compare resources with queue allocations, valid QIDs and vectors. Primary capacity and secondary allocations are different quantities.</p>
</li>
<li id="q-047-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First check the selected primary controller and pagination starting point.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-virtual">Base 2.4 §8.2.7</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-idns">NVM Command Set 1.3 §4.1.5.1–4.1.5.4</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-048" data-question="48"><h2><a class="qa-qid" href="#q-048">Q48</a> How should unsupported or invalid CNS, CSI, NSID and UUID Index values be handled?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-048-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-048-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Judge selectors by their actual roles rather than calling every Identify failure an invalid namespace.</p>
</li>
<li id="q-048-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>The same NSID/CSI can be legal for one CNS and illegal for another; fix the CNS and prerequisites in each test.</p>
</li>
<li id="q-048-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Figure 336 specifies use of NSID/CNTID/CSI per CNS; UUID-selection capability controls UIDX use.</p>
</li>
<li id="q-048-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>For unused CNTID, the host clears it and the controller ignores it. For unused CSI, the host should clear it; the controller should ignore it but may return Invalid Field if nonzero.</p>
</li>
<li id="q-048-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Hold other selectors constant, vary the target field and apply CNS-specific rules before generic defaults.</p>
</li>
<li id="q-048-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Valid queries return 4096 bytes. CNS 11h can return zero-filled data for a defined unallocated NSID, distinct from an invalid-NSID error.</p>
</li>
<li id="q-048-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Unsupported CNS:0/02h; incompatible namespace command set:1/2Ch; prohibited terminal cursors for CNS 02h/10h:0/0Bh. For UUID selection, an unsupported UUID for the requested information, an all-zero UUID or the NVMe Invalid UUID shall return 0/02h. CSI handling depends on whether the CNS uses CSI and on the namespace command set.</p>
</li>
<li id="q-048-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-048-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Normal completion here does not guarantee an AER; a separate defined event requires support, configuration and a pending request. <a class="qa-rule-link" href="#common-command-9">Full rule in this volume</a></p>
</li>
<li id="q-048-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Correlate the completion with error records under the shared entry-creation rules; do not infer entry count directly from the number of failures. <a class="qa-rule-link" href="#common-command-10">Full rule in this volume</a></p>
</li>
<li id="q-048-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>PEL is not a per-command trace; supported defined events are logged under their recording conditions. <a class="qa-rule-link" href="#common-command-11">Full rule in this volume</a></p>
</li>
<li id="q-048-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Repeat an interrupted query and distinguish identity, configuration and dynamic fields. <a class="qa-rule-link" href="#common-identify-12">Full rule in this volume</a></p>
</li>
<li id="q-048-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Rediscover affected objects; reset alone does not mean namespace deletion or factory configuration. <a class="qa-rule-link" href="#common-identify-13">Full rule in this volume</a></p>
</li>
<li id="q-048-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Re-read and compare, separating firmware activation or management changes from power cycling alone. <a class="qa-rule-link" href="#common-identify-14">Full rule in this volume</a></p>
</li>
<li id="q-048-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Identify is read-only; active lists may differ by controller, so compare matching query targets. <a class="qa-rule-link" href="#common-identify-15">Full rule in this volume</a></p>
</li>
<li id="q-048-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Preserve CQE with CDW10/11/14; different selectors can produce the same 0/02h.</p>
</li>
<li id="q-048-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First check whether the CNS uses that selector. Ignoring an unused field is not automatically a validation omission.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-idcmd">Base 2.4 §5.2.14.1</a> · <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-uuid">Base 2.4 §8.1.31.1–8.1.31.2</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-idns">NVM Command Set 1.3 §4.1.5.1–4.1.5.4</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-049" data-question="49"><h2><a class="qa-qid" href="#q-049">Q49</a> How are SN, MN, FR, MDTS and optional Admin capability fields interpreted?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-049-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-049-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>One large Identify structure combines identity strings, transfer limits and capability bitmaps, requiring different interpretation methods.</p>
</li>
<li id="q-049-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>SN/MN identify the subsystem, FR the active firmware, MDTS a transfer limit and OACS optional Admin capabilities.</p>
</li>
<li id="q-049-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>In CNS 01h: SN bytes 23:4, MN63:24, FR71:64, MDTS byte 77 and OACS bytes 257:256.</p>
</li>
<li id="q-049-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>Decode ASCII strings and space padding. Nonzero MDTS limits bytes to 2^MDTS×2^(12+CAP.MPSMIN), not CC.MPS. MDTS=0 removes this limit, not all command-specific limits.</p>
</li>
<li id="q-049-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Confirm layout/offsets, then decode strings, bits and exponents separately. Check CTRATT.MEM when accounting for metadata in transfer length.</p>
</li>
<li id="q-049-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>MPSMIN=0 and MDTS=5 give 128 KiB. With MEM=0, 32 blocks of 4096-byte data plus 16-byte metadata per block exceed it.</p>
</li>
<li id="q-049-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Exceeding MDTS returns Invalid Field (0/02h). Unsupported optional opcodes generally use 0/01h; a recent revision does not require all options.</p>
</li>
<li id="q-049-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-049-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Normal completion here does not guarantee an AER; a separate defined event requires support, configuration and a pending request. <a class="qa-rule-link" href="#common-command-9">Full rule in this volume</a></p>
</li>
<li id="q-049-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Correlate the completion with error records under the shared entry-creation rules; do not infer entry count directly from the number of failures. <a class="qa-rule-link" href="#common-command-10">Full rule in this volume</a></p>
</li>
<li id="q-049-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>PEL is not a per-command trace; supported defined events are logged under their recording conditions. <a class="qa-rule-link" href="#common-command-11">Full rule in this volume</a></p>
</li>
<li id="q-049-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Repeat an interrupted query and distinguish identity, configuration and dynamic fields. <a class="qa-rule-link" href="#common-identify-12">Full rule in this volume</a></p>
</li>
<li id="q-049-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Rediscover affected objects; reset alone does not mean namespace deletion or factory configuration. <a class="qa-rule-link" href="#common-identify-13">Full rule in this volume</a></p>
</li>
<li id="q-049-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Re-read and compare, separating firmware activation or management changes from power cycling alone. <a class="qa-rule-link" href="#common-identify-14">Full rule in this volume</a></p>
</li>
<li id="q-049-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Identify is read-only; active lists may differ by controller, so compare matching query targets. <a class="qa-rule-link" href="#common-identify-15">Full rule in this volume</a></p>
</li>
<li id="q-049-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Compare FR with the currently active firmware slot, not a pending slot; cross-check OACS with corresponding command-support entries.</p>
</li>
<li id="q-049-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First check whether MDTS was treated as a byte count or multiplied by the wrong page size.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-cap">Base 2.4 §3.1.4 (CAP, VS)</a> · <a href="#ref-conventions">Base 2.4 §1.4.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-050" data-question="50"><h2><a class="qa-qid" href="#q-050">Q50</a> How can advertised Identify support be cross-checked against commands and the Commands Supported and Effects Log?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-050-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-050-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Connect an advertised bit to a legal operation instead of validating the bit alone.</p>
</li>
<li id="q-050-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Compare the same controller, command set, namespace configuration and time.</p>
</li>
<li id="q-050-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Check Identify support, LPA.CSES and the correct Admin/I/O opcode&#x27;s CSUPP and effects in LID 05h.</p>
</li>
<li id="q-050-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>Read CSUPP together with LBCC, NCC, NIC, CCC and CSE to understand data/capability/list changes and execution restrictions.</p>
</li>
<li id="q-050-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Establish legal prerequisites, discover support, prepare valid parameters/resources, execute, verify result and rediscover information affected by the command.</p>
</li>
<li id="q-050-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Support means a legal supported operation exists, not that every parameter/state succeeds. Completion must also match the command&#x27;s defined effect.</p>
</li>
<li id="q-050-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>0/01h may contradict opcode support, but Invalid Field, Namespace Not Ready or Lockdown first require checking parameters and state.</p>
</li>
<li id="q-050-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-050-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Normal completion here does not guarantee an AER; a separate defined event requires support, configuration and a pending request. <a class="qa-rule-link" href="#common-command-9">Full rule in this volume</a></p>
</li>
<li id="q-050-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Correlate the completion with error records under the shared entry-creation rules; do not infer entry count directly from the number of failures. <a class="qa-rule-link" href="#common-command-10">Full rule in this volume</a></p>
</li>
<li id="q-050-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>PEL is not a per-command trace; supported defined events are logged under their recording conditions. <a class="qa-rule-link" href="#common-command-11">Full rule in this volume</a></p>
</li>
<li id="q-050-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Repeat an interrupted query and distinguish identity, configuration and dynamic fields. <a class="qa-rule-link" href="#common-identify-12">Full rule in this volume</a></p>
</li>
<li id="q-050-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Rediscover affected objects; reset alone does not mean namespace deletion or factory configuration. <a class="qa-rule-link" href="#common-identify-13">Full rule in this volume</a></p>
</li>
<li id="q-050-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Re-read and compare, separating firmware activation or management changes from power cycling alone. <a class="qa-rule-link" href="#common-identify-14">Full rule in this volume</a></p>
</li>
<li id="q-050-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Identify is read-only; active lists may differ by controller, so compare matching query targets. <a class="qa-rule-link" href="#common-identify-15">Full rule in this volume</a></p>
</li>
<li id="q-050-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Commands Supported and Effects describes capability/effects, not recent execution history.</p>
</li>
<li id="q-050-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First check Admin versus I/O entry selection and CSI.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-effects">Base 2.4 §5.2.13.1.6</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-idcmd">Base 2.4 §5.2.14.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-051" data-question="51"><h2><a class="qa-qid" href="#q-051">Q51</a> Which Identify data and lists change after namespace creation, deletion, attachment, detachment or format?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-051-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-051-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Connect configuration changes to rediscovery instead of continuing with stale capacity, format or attachment data.</p>
</li>
<li id="q-051-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Create/Delete change existence, Attach/Detach controller accessibility, and Format the data format within its defined scope.</p>
</li>
<li id="q-051-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>OACS.NMS advertises namespace management; Format also uses OACS/FNA and NVM format support.</p>
</li>
<li id="q-051-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>Separately inspect allocated/active lists, CNS 12h attached controllers and namespace format/capacity fields such as FLBAS/DPS/NSZE/NCAP.</p>
</li>
<li id="q-051-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Capture before-state, wait for management completion, then reread affected lists/namespace data. Successful Create does not automatically attach the namespace.</p>
</li>
<li id="q-051-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Create adds to Allocated; Attach adds to the target Active list; Detach removes from that Active list without necessarily deallocating; Format updates the selected format rather than necessarily changing NSID.</p>
</li>
<li id="q-051-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>A failed management command does not universally imply either every change occurred or none occurred; examine its failure/partial-operation rules and rediscover.</p>
</li>
<li id="q-051-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-051-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Identify queries do not generate change events. Namespace attribute changes from Create, Delete, Attach, Detach or Format follow the affected-controller, support and AEC conditions for Namespace Attribute Changed; controllers need not observe identical changes.</p>
</li>
<li id="q-051-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Check Changed Namespace List (LID 04h) alongside fresh Identify data. The list identifies changed NSIDs, not current configuration. RAE affects acknowledgement; preserve the event and list before subsequent queries.</p>
</li>
<li id="q-051-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>With PEL support, Change Namespace events for Create/Delete differ from Format Start/Completion events. Attach/Detach are not Create/Delete records; Identify itself does not require these events.</p>
</li>
<li id="q-051-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Repeat an interrupted query and distinguish identity, configuration and dynamic fields. <a class="qa-rule-link" href="#common-identify-12">Full rule in this volume</a></p>
</li>
<li id="q-051-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Rediscover affected objects; reset alone does not mean namespace deletion or factory configuration. <a class="qa-rule-link" href="#common-identify-13">Full rule in this volume</a></p>
</li>
<li id="q-051-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Re-read and compare, separating firmware activation or management changes from power cycling alone. <a class="qa-rule-link" href="#common-identify-14">Full rule in this volume</a></p>
</li>
<li id="q-051-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Identify is read-only; active lists may differ by controller, so compare matching query targets. <a class="qa-rule-link" href="#common-identify-15">Full rule in this volume</a></p>
</li>
<li id="q-051-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Correlate management results, lists, namespace data and applicable Changed Namespace notification. The event is not a full replacement for Identify configuration data.</p>
</li>
<li id="q-051-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First verify the affected controller and completion of the preceding management command.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-idns">NVM Command Set 1.3 §4.1.5.1–4.1.5.4</a> · <a href="#ref-nsmanage">Base 2.4 §5.2.24–5.2.25, 8.1.17</a> · <a href="#ref-effects">Base 2.4 §5.2.13.1.6</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-nschange">Base 2.4 §5.2.13.1.5, 5.2.13.1.14.2.6–5.2.13.1.14.2.8</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-052" data-question="52"><h2><a class="qa-qid" href="#q-052">Q52</a> Which Identify data may change after firmware activation, reset or power cycling?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-052-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-052-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Judge change by field semantics instead of requiring the whole 4096-byte buffer to remain identical.</p>
</li>
<li id="q-052-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Separate stable identity, firmware-advertised capability, persistent configuration and dynamic state.</p>
</li>
<li id="q-052-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Preserve identity, namespace stable identifiers, FR, capabilities, capacity/format/attachments and dynamic fields as separate comparison groups.</p>
</li>
<li id="q-052-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>FR describes active firmware. Rediscover MDTS/capabilities after an update; dynamic fields such as NUSE are not fixed identities.</p>
</li>
<li id="q-052-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Record whether reset/power cycling also activated firmware or changed configuration. Reread with identical selectors and compare by field definition.</p>
</li>
<li id="q-052-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Ordinary reset is not a rename, namespace deletion or format operation. Concurrent firmware activation can change FR and legitimately change advertised capabilities.</p>
</li>
<li id="q-052-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Comparison has no new status. For failed post-reset Identify distinguish incomplete initialization, invalid NSID and wrong CNS before attributing every difference to firmware.</p>
</li>
<li id="q-052-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-052-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Normal completion here does not guarantee an AER; a separate defined event requires support, configuration and a pending request. <a class="qa-rule-link" href="#common-command-9">Full rule in this volume</a></p>
</li>
<li id="q-052-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Correlate the completion with error records under the shared entry-creation rules; do not infer entry count directly from the number of failures. <a class="qa-rule-link" href="#common-command-10">Full rule in this volume</a></p>
</li>
<li id="q-052-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>PEL is not a per-command trace; supported defined events are logged under their recording conditions. <a class="qa-rule-link" href="#common-command-11">Full rule in this volume</a></p>
</li>
<li id="q-052-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Repeat an interrupted query and distinguish identity, configuration and dynamic fields. <a class="qa-rule-link" href="#common-identify-12">Full rule in this volume</a></p>
</li>
<li id="q-052-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Rediscover affected objects; reset alone does not mean namespace deletion or factory configuration. <a class="qa-rule-link" href="#common-identify-13">Full rule in this volume</a></p>
</li>
<li id="q-052-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Re-read and compare, separating firmware activation or management changes from power cycling alone. <a class="qa-rule-link" href="#common-identify-14">Full rule in this volume</a></p>
</li>
<li id="q-052-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Identify is read-only; active lists may differ by controller, so compare matching query targets. <a class="qa-rule-link" href="#common-identify-15">Full rule in this volume</a></p>
</li>
<li id="q-052-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Confirm object identity with stable IDs. Preserve raw bytes while separating padding, reserved/dynamic fields and meaningful changes.</p>
</li>
<li id="q-052-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First check concurrent pending firmware activation and accidental selection of another controller/namespace.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-identity">Base 2.4 §4.7.1</a> · <a href="#ref-idns">NVM Command Set 1.3 §4.1.5.1–4.1.5.4</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-effects">Base 2.4 §5.2.13.1.6</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-053" data-question="53"><h2><a class="qa-qid" href="#q-053">Q53</a> How should inconsistencies among Identify, features, logs and command behavior be investigated?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-053-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-053-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Build a complete evidence chain instead of letting one advertised capability override current conditions.</p>
</li>
<li id="q-053-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Hold controller, NSID, CSI, time and configuration constant; different views/times need not describe the same state.</p>
</li>
<li id="q-053-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Identify discovers capability, Get Features configuration, and logs state/events or effect declarations. Their roles differ.</p>
</li>
<li id="q-053-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>Preserve SQE/CQE, raw Identify, Feature SEL and log selectors. Distinguish Current from Supported Capabilities.</p>
</li>
<li id="q-053-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Check revision/decoding, scope/selectors, legal parameters, current state/order and result; isolate one variable when reproducing.</p>
</li>
<li id="q-053-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Consistency means the specified relationships hold, not equal numeric values. CHANG=1 and Current=0 can both be correct.</p>
</li>
<li id="q-053-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Use original SCT/SC for next steps and associated Error Information when More=1. A host timeout without status first requires locating the submission/completion stage.</p>
</li>
<li id="q-053-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-053-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Normal completion here does not guarantee an AER; a separate defined event requires support, configuration and a pending request. <a class="qa-rule-link" href="#common-command-9">Full rule in this volume</a></p>
</li>
<li id="q-053-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Correlate the completion with error records under the shared entry-creation rules; do not infer entry count directly from the number of failures. <a class="qa-rule-link" href="#common-command-10">Full rule in this volume</a></p>
</li>
<li id="q-053-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>PEL is not a per-command trace; supported defined events are logged under their recording conditions. <a class="qa-rule-link" href="#common-command-11">Full rule in this volume</a></p>
</li>
<li id="q-053-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Repeat an interrupted query and distinguish identity, configuration and dynamic fields. <a class="qa-rule-link" href="#common-identify-12">Full rule in this volume</a></p>
</li>
<li id="q-053-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Rediscover affected objects; reset alone does not mean namespace deletion or factory configuration. <a class="qa-rule-link" href="#common-identify-13">Full rule in this volume</a></p>
</li>
<li id="q-053-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Re-read and compare, separating firmware activation or management changes from power cycling alone. <a class="qa-rule-link" href="#common-identify-14">Full rule in this volume</a></p>
</li>
<li id="q-053-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Identify is read-only; active lists may differ by controller, so compare matching query targets. <a class="qa-rule-link" href="#common-identify-15">Full rule in this volume</a></p>
</li>
<li id="q-053-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>A defensible noncompliance conclusion requires fixed prerequisites, object and timing, plus a remaining contradiction with an explicit requirement.</p>
</li>
<li id="q-053-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First verify that all evidence describes the same controller/namespace, configuration interval and selectors.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-idcmd">Base 2.4 §5.2.14.1</a> · <a href="#ref-effects">Base 2.4 §5.2.13.1.6</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-getfeat">Base 2.4 §5.2.12</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<section id="common-rules" class="qa-common"><h2>Shared rules linked from the answers</h2><p>Each shared mechanism is explained in full once in this volume. Use browser Back to return to the question; explicit command or feature exceptions take precedence.</p>
<article id="common-command-8"><h3>Command completion, events and records · How are DNR and More set?</h3><p>For a CQE, DNR=1 means the identical command is expected to fail if resubmitted to any controller in this subsystem; DNR=0 means it may succeed. Do not assign DNR=1 solely from an error name unless that condition mandates it. More=1 identifies additional information for this command in the Error Information Log. DNR should be zero when SCT=SC=0.</p></article>
<article id="common-command-9"><h3>Command completion, events and records · Is an asynchronous event generated?</h3><p>Command completion and asynchronous notification are separate. Success here does not itself guarantee an event. For a defined resulting event, check support, applicable notification configuration, masking and an outstanding Asynchronous Event Request.</p></article>
<article id="common-command-10"><h3>Command completion, events and records · Are Error Information or other logs updated?</h3><p>A successful CQE does not require a new Error Information entry. For an error with More=1, read LID 01h and correlate SQID, CID and Error Count; not every unsuccessful CQE requires a new entry. Re-read the interfaces named in this question for the state the operation changes.</p></article>
<article id="common-command-11"><h3>Command completion, events and records · Is it recorded in the Persistent Event Log?</h3><p>The optional Persistent Event Log is an event history, not a trace of every command. Check LPA support and the Supported Events Bitmap, then the logging condition for the particular event. Command success or failure alone does not require an entry.</p></article>
<article id="common-identify-12"><h3>Query reset and scope · What survives or continues after Controller Reset?</h3><p>Controller Reset stops an outstanding query; a missing response is not an all-zero result. Re-read after recovery, distinguishing identity, configuration and dynamic state by field. Reset alone does not mean the namespace was deleted.</p></article>
<article id="common-identify-13"><h3>Query reset and scope · What survives or continues after NVM Subsystem Reset?</h3><p>Rediscover affected controllers and namespaces after reset. An NVM Subsystem Reset does not by itself imply that all storage configuration returns to manufacturing defaults. Verify changes caused by any separate management operation.</p></article>
<article id="common-identify-14"><h3>Query reset and scope · What survives or continues after a power cycle?</h3><p>After a power cycle, re-read version, capabilities, current format and attachment lists. Stable identity and persistent configuration are not ordinary volatile feature values. Firmware activation or configuration changes require before/after snapshots and event timing.</p></article>
<article id="common-identify-15"><h3>Query reset and scope · Are other controllers or namespaces affected?</h3><p>Identify reads data; it does not create, format or attach a namespace. CNS and selectors determine the view. Active lists may differ across controllers, so different lists do not alone establish corruption.</p></article>
</section>
<section id="source-index"><h2>Source locations and existing figure guides</h2><p>Base printed page = PDF page−26; the other two use identical numbers. Locations follow the supplied PDF body and retain figure numbers. Shared pages contribute only the relevant definitions, excluding Fabrics and PCIe link/packet content.</p><ul class="qa-references">
<li id="ref-conventions"><strong>Base 2.4 · §1.4.1</strong><br>Printed pages 2–3 · PDF 28–29</li>
<li id="ref-cap"><strong>Base 2.4 · §3.1.4 (CAP, VS)</strong><br>Printed pages 54–59 · PDF 80–85 · Figure 36–37</li>
<li id="ref-nsid"><strong>Base 2.4 · §3.2.1</strong><br>Printed pages 78–81 · PDF 104–107</li>
<li id="ref-reset"><strong>Base 2.4 · §3.7.1–3.7.4</strong><br>Printed pages 120–124 · PDF 146–150</li>
<li id="ref-status"><strong>Base 2.4 · §4.2.3</strong><br>Printed pages 145–155 · PDF 171–181 · Figure 101–105</li>
<li id="ref-feature"><strong>Base 2.4 · §4.4</strong><br>Printed pages 166–169 · PDF 192–195 · Figure 126–127</li>
<li id="ref-identity"><strong>Base 2.4 · §4.7.1</strong><br>Printed pages 173–175 · PDF 199–201</li>
<li id="ref-aer"><strong>Base 2.4 · §5.2.2</strong><br>Printed pages 183–190 · PDF 209–216 · Figure 150–156</li>
<li id="ref-getfeat"><strong>Base 2.4 · §5.2.12</strong><br>Printed pages 209–212 · PDF 235–238 · Figure 197–202</li>
<li id="ref-error"><strong>Base 2.4 · §5.2.13.1.2</strong><br>Printed pages 218–220 · PDF 244–246 · Figure 212</li>
<li id="ref-effects"><strong>Base 2.4 · §5.2.13.1.6</strong><br>Printed pages 226–229 · PDF 252–255 · Figure 216–217</li>
<li id="ref-nschange"><strong>Base 2.4 · §5.2.13.1.5, 5.2.13.1.14.2.6–5.2.13.1.14.2.8</strong><br>Printed pages 226, 258–261 · PDF 252, 284–287 · Figure 247–249</li>
<li id="ref-pel"><strong>Base 2.4 · §5.2.13.1.14 (header, reset, hardware, Set Feature events)</strong><br>Printed pages 244–256, 258, 262–264 · PDF 270–282, 284, 288–290 · Figure 232–244, 246, 252–253</li>
<li id="ref-idcmd"><strong>Base 2.4 · §5.2.14.1</strong><br>Printed pages 336–340 · PDF 362–366 · Figure 332–337</li>
<li id="ref-idctrl"><strong>Base 2.4 · §5.2.14.2.1</strong><br>Printed pages 340–387 · PDF 366–413 · Figure 338–341</li>
<li id="ref-idlist"><strong>Base 2.4 · §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</strong><br>Printed pages 387–399, 402–404 · PDF 413–425, 428–430 · Figure 342–355, 360–362</li>
<li id="ref-nsmanage"><strong>Base 2.4 · §5.2.24–5.2.25, 8.1.17</strong><br>Printed pages 442–448, 660–664 · PDF 468–474, 686–690 · Figure 442–450</li>
<li id="ref-profile"><strong>Base 2.4 · §5.2.30.1.18</strong><br>Printed pages 478–479 · PDF 504–505 · Figure 494–495</li>
<li id="ref-uuid"><strong>Base 2.4 · §8.1.31.1–8.1.31.2</strong><br>Printed pages 737–738 · PDF 763–764 · Figure 782</li>
<li id="ref-virtual"><strong>Base 2.4 · §8.2.7</strong><br>Printed pages 754–758 · PDF 780–784 · Figure 796</li>
<li id="ref-idns"><strong>NVM Command Set 1.3 · §4.1.5.1–4.1.5.4</strong><br>Printed pages 84–107 · PDF 84–107 · Figure 123–130</li>
</ul><h3>When you need a field guide</h3><p>Existing figure explanations have canonical locations; use these links instead of duplicating the same guide.</p><ul>
<li><a href="/nvme/figure-reference/command/en/#figure-b101">Base 2.4 Figure 101 · Completion Queue Entry: Status Field</a></li>
<li><a href="/nvme/figure-reference/command/en/#figure-b104">Base 2.4 Figure 104 · Status Code – Command Specific Status Values</a></li>
<li><a href="/nvme/figure-reference/identify/en/#figure-b338">Base 2.4 Figure 338 · Identify – Identify Controller Data Structure, I/O Command Set Independent</a></li>
<li><a href="/nvme/figure-reference/init/en/#figure-b36">Base 2.4 Figure 36 · Offset 0h: CAP – Controller Capabilities</a></li>
<li><a href="/nvme/figure-reference/identify/en/#figure-n123">NVM Command Set 1.3 Figure 123 · Identify – Identify Namespace Data Structure, NVM Command Set</a></li>
</ul><details><summary>Original documents used</summary><ul class="qr-sources">
<li>NVM Express Base Specification · Revision 2.4 · 2026-07-31<br><code>NVM-Express-Base-Specification-Revision-2.4-Ratified-2026.07.31.pdf</code></li>
<li>NVM Express NVM Command Set Specification · Revision 1.3 · 2026-07-31<br><code>NVM-Express-NVM-Command-Set-Specification-Revision-1.3-Ratified-2026.07.31.pdf</code></li>
<li>NVM Express NVMe over PCIe Transport Specification · Revision 1.4 · 2026-07-31<br><code>NVM-Express-NVMe-over-PCIe-Transport-Specification-Revision-1.4-Ratified-2026.07.31.pdf</code></li>
</ul></details></section>
</main>
<nav class="qr-top" aria-label="Bank and editions"><a href="#content">Skip to content</a><a href="/nvme/question-bank/en/">Question index</a><a href="/nvme/question-bank/identify/zh-tw/">繁體中文</a><a href="/DOCS/nvme-question-bank/identify.html">Chinese tutorial HTML</a></nav>
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
