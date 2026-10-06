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
<header><p class="qa-range">Q44–Q53</p><h1>Identify and capability discovery</h1><p class="qr-intro">Treat Identify as several distinct query interfaces. Choose the object and structure before CNS, CSI, NSID and other selectors. Separate capability, current configuration and changing lists to find real contradictions.</p><p>Practice first, then reveal the explanation. Each question uses the prose, field interpretation, comparison or flow that suits it. All numerical examples are hypothetical. Status is written SCT/SC; h indicates hexadecimal.</p></header>
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
<article class="qa-question" id="q-044" data-question="44" data-answer-kind="compare"><h2><a class="qa-qid" href="#q-044">Q44</a> What important information is provided by Identify Controller and Identify Namespace?</h2>
<p class="qa-prompt">Identify the key difference and one case where the alternatives are not interchangeable.</p>
<details class="qa-answer" id="q-044-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-044-a-01">Separate controller capability from a particular namespace&#x27;s capacity, format and protection configuration.</p><div class="qa-sections">
<section class="qa-section" id="q-044-s-01" data-answer-section="1"><h3><span>1.</span> What differs</h3>
<span class="qa-anchor" id="q-044-a-02"></span><p>Controller data describes the receiving controller&#x27;s view; NSID/CNS/CSI select namespace information.</p>
<span class="qa-anchor" id="q-044-a-04"></span><p>Controller fields include SN/MN/FR, MDTS, OACS/ONCS, LPA and SQES/CQES. NVM Namespace includes NSZE/NCAP/NUSE, FLBAS/LBAF, MC/DPC/DPS, atomicity and group identifiers.</p>
</section>
<section class="qa-section" id="q-044-s-02" data-answer-section="2"><h3><span>2.</span> How to choose and verify</h3>
<span class="qa-anchor" id="q-044-a-03"></span><p>Main entry points are CNS 01h Controller and CNS 00h NVM Namespace; CNS 05h/06h are command-set specific, while CNS 08h is command-set independent Namespace data.</p>
<span class="qa-anchor" id="q-044-a-05"></span><p>Read Controller and the active list, then the applicable structures for each namespace. Convert block counts using the currently selected LBA format.</p>
<span class="qa-anchor" id="q-044-a-06"></span><p>Identify returns a 4096-byte structure and successful CQE. NSZE=8192 and LBADS=12 describe 32 MiB of logical address space.</p>
</section>
<section class="qa-section" id="q-044-s-03" data-answer-section="3"><h3><span>3.</span> Where the comparison stops</h3>
<span class="qa-anchor" id="q-044-a-07"></span><p>Unsupported CNS uses Invalid Field (0/02h); an incompatible namespace command set uses Invalid I/O Command Set (1/2Ch). Apply CNS-specific NSID rules.</p>
<span class="qa-anchor" id="q-044-a-16"></span><p>Controller opcode support does not make every namespace format or current state suitable; both levels must permit the operation.</p>
</section>
</div>
<span class="qa-anchor" id="q-044-a-17"></span><span class="qa-anchor" id="q-044-a-08"></span><span class="qa-anchor" id="q-044-a-09"></span><span class="qa-anchor" id="q-044-a-10"></span><span class="qa-anchor" id="q-044-a-11"></span><span class="qa-anchor" id="q-044-a-12"></span><span class="qa-anchor" id="q-044-a-13"></span><span class="qa-anchor" id="q-044-a-14"></span><span class="qa-anchor" id="q-044-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-idcmd">Base 2.4 §5.2.14.1</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-idns">NVM Command Set 1.3 §4.1.5.1–4.1.5.4</a> · <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-045" data-question="45" data-answer-kind="compare"><h2><a class="qa-qid" href="#q-045">Q45</a> How do active, allocated and namespace descriptor lists differ?</h2>
<p class="qa-prompt">Identify the key difference and one case where the alternatives are not interchangeable.</p>
<details class="qa-answer" id="q-045-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-045-a-01">Separate accessibility through this controller, allocation/existence and the identity of one namespace.</p><div class="qa-sections">
<section class="qa-section" id="q-045-s-01" data-answer-section="1"><h3><span>1.</span> What differs</h3>
<span class="qa-anchor" id="q-045-a-02"></span><p>The active list is controller-relative; the allocated list can include unattached namespaces; descriptors describe one NSID.</p>
<span class="qa-anchor" id="q-045-a-04"></span><p>List NSID is a pagination cursor returning greater IDs. Descriptors contain NIDT/NIDL/NID for identifiers such as EUI64, NGUID, UUID and CSI.</p>
</section>
<section class="qa-section" id="q-045-s-02" data-answer-section="2"><h3><span>2.</span> How to choose and verify</h3>
<span class="qa-anchor" id="q-045-a-03"></span><p>CNS 02h queries active IDs, CNS 10h allocated IDs and CNS 03h namespace identification descriptors. Allocation queries depend on Namespace Management support.</p>
<span class="qa-anchor" id="q-045-a-05"></span><p>Start list enumeration at NSID=0 and continue from returned IDs; for a descriptor query NSID selects the target, not a cursor.</p>
<span class="qa-anchor" id="q-045-a-06"></span><p>Allocated={1,3,8} and Active={1,8} mean namespace 3 is allocated but not active here, not necessarily damaged.</p>
</section>
<section class="qa-section" id="q-045-s-03" data-answer-section="3"><h3><span>3.</span> Where the comparison stops</h3>
<span class="qa-anchor" id="q-045-a-07"></span><p>CNS 02h/10h cursors FFFFFFFEh or FFFFFFFFh shall return Invalid Namespace or Format (0/0Bh); unsupported CNS uses 0/02h.</p>
<span class="qa-anchor" id="q-045-a-16"></span><p>Correlate stable descriptor identifiers rather than assuming NSIDs never change. Restart enumeration when configuration changes compromise a consistent view.</p>
</section>
</div>
<span class="qa-anchor" id="q-045-a-17"></span><span class="qa-anchor" id="q-045-a-08"></span><span class="qa-anchor" id="q-045-a-09"></span><span class="qa-anchor" id="q-045-a-10"></span><span class="qa-anchor" id="q-045-a-11"></span><span class="qa-anchor" id="q-045-a-12"></span><span class="qa-anchor" id="q-045-a-13"></span><span class="qa-anchor" id="q-045-a-14"></span><span class="qa-anchor" id="q-045-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-nsid">Base 2.4 §3.2.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-046" data-question="46" data-answer-kind="compare"><h2><a class="qa-qid" href="#q-046">Q46</a> What are Controller Lists, the UUID List and I/O Command Set Identify data used for?</h2>
<p class="qa-prompt">Identify the key difference and one case where the alternatives are not interchangeable.</p>
<details class="qa-answer" id="q-046-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-046-a-01">Answer three different questions: which controllers can access, which vendor definition to use and which command sets can operate together.</p><div class="qa-sections">
<section class="qa-section" id="q-046-s-01" data-answer-section="1"><h3><span>1.</span> What differs</h3>
<span class="qa-anchor" id="q-046-a-02"></span><p>Controller Lists describe relationships. The UUID List selects vendor-specific information and is not the namespace UUID descriptor.</p>
<span class="qa-anchor" id="q-046-a-04"></span><p>CNTID is a list cursor or CNS-specific target; UIDX=0 selects no UUID. Each CNS 1Ch vector describes a simultaneously supported set combination.</p>
</section>
<section class="qa-section" id="q-046-s-02" data-answer-section="2"><h3><span>2.</span> How to choose and verify</h3>
<span class="qa-anchor" id="q-046-a-03"></span><p>CNS 12h lists controllers attached to a namespace, 13h subsystem I/O controllers, 17h the UUID List and 1Ch command-set combinations.</p>
<span class="qa-anchor" id="q-046-a-05"></span><p>Select CNS and selectors for the question. After CNS 1Ch discovery, FID 19h.IOCSCI selects the combination index, not the CSI bitmap itself.</p>
<span class="qa-anchor" id="q-046-a-06"></span><p>Lists return identities/counts or UUID entries; command-set vectors advertise available combinations without automatically enabling them.</p>
</section>
<section class="qa-section" id="q-046-s-03" data-answer-section="3"><h3><span>3.</span> Where the comparison stops</h3>
<span class="qa-anchor" id="q-046-a-07"></span><p>Unsupported CNS and CNS 12h NSID=FFFFFFFFh use 0/02h. Illegal UUID selection follows §8.1.31, not namespace-absence rules.</p>
<span class="qa-anchor" id="q-046-a-16"></span><p>Keep CNTID and NSID roles separate and verify that FID 19h Current selects the intended vector.</p>
</section>
</div>
<span class="qa-anchor" id="q-046-a-17"></span><span class="qa-anchor" id="q-046-a-08"></span><span class="qa-anchor" id="q-046-a-09"></span><span class="qa-anchor" id="q-046-a-10"></span><span class="qa-anchor" id="q-046-a-11"></span><span class="qa-anchor" id="q-046-a-12"></span><span class="qa-anchor" id="q-046-a-13"></span><span class="qa-anchor" id="q-046-a-14"></span><span class="qa-anchor" id="q-046-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-idcmd">Base 2.4 §5.2.14.1</a> · <a href="#ref-uuid">Base 2.4 §8.1.31.1–8.1.31.2</a> · <a href="#ref-profile">Base 2.4 §5.2.30.1.18</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-047" data-question="47" data-answer-kind="lookup"><h2><a class="qa-qid" href="#q-047">Q47</a> Which Identify structures describe NVM Sets, Endurance Groups, Domains and Secondary Controllers?</h2>
<p class="qa-prompt">Choose the interface and target, then identify the returned field that supports your conclusion.</p>
<details class="qa-answer" id="q-047-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-047-a-01">Establish resource membership instead of treating sets, groups, domains and controllers as interchangeable objects.</p><div class="qa-sections">
<section class="qa-section" id="q-047-s-01" data-answer-section="1"><h3><span>1.</span> Select the target and information</h3>
<span class="qa-anchor" id="q-047-a-02"></span><p>Each list has its own IDs and capacity/resource fields. This question discovers information rather than changing capacity or virtualization state.</p>
<span class="qa-anchor" id="q-047-a-03"></span><p>Check relevant CTRATT capabilities and OACS.VMS. CNS 04h,19h,18h and 14h/15h describe sets, endurance groups, domains and primary/secondary controllers respectively.</p>
<span class="qa-anchor" id="q-047-a-04"></span><p>Set attributes include ENDGID; namespace data includes NVMSETID/ENDGID; domain entries include DID/TDC/UDC; secondary entries include SCID/PCID, state and VQ/VI counts.</p>
</section>
<section class="qa-section" id="q-047-s-02" data-answer-section="2"><h3><span>2.</span> Query sequence and interpretation</h3>
<span class="qa-anchor" id="q-047-a-05"></span><p>Trace namespace membership through sets/groups, domain capacity and primary/secondary resource information for allocated queues and interrupts.</p>
<span class="qa-anchor" id="q-047-a-06"></span><p>Results provide related IDs/attributes. A zero field is not always a zero resource count; first establish support and field validity.</p>
</section>
<section class="qa-section" id="q-047-s-03" data-answer-section="3"><h3><span>3.</span> Handle missing or inconsistent evidence</h3>
<span class="qa-anchor" id="q-047-a-07"></span><p>Unsupported CNS uses 0/02h; cursors beyond existing IDs may return empty lists rather than errors.</p>
<span class="qa-anchor" id="q-047-a-16"></span><p>Compare resources with queue allocations, valid QIDs and vectors. Primary capacity and secondary allocations are different quantities.</p>
<span class="qa-anchor" id="q-047-a-17"></span><p>First check the selected primary controller and pagination starting point.</p>
</section>
</div>
<span class="qa-anchor" id="q-047-a-08"></span><span class="qa-anchor" id="q-047-a-09"></span><span class="qa-anchor" id="q-047-a-10"></span><span class="qa-anchor" id="q-047-a-11"></span><span class="qa-anchor" id="q-047-a-12"></span><span class="qa-anchor" id="q-047-a-13"></span><span class="qa-anchor" id="q-047-a-14"></span><span class="qa-anchor" id="q-047-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-virtual">Base 2.4 §8.2.7</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-idns">NVM Command Set 1.3 §4.1.5.1–4.1.5.4</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-048" data-question="48" data-answer-kind="error"><h2><a class="qa-qid" href="#q-048">Q48</a> How should unsupported or invalid CNS, CSI, NSID and UUID Index values be handled?</h2>
<p class="qa-prompt">Distinguish failure conditions before deciding whether a particular response is required.</p>
<details class="qa-answer" id="q-048-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-048-a-01">Judge selectors by their actual roles rather than calling every Identify failure an invalid namespace.</p><div class="qa-sections">
<section class="qa-section" id="q-048-s-01" data-answer-section="1"><h3><span>1.</span> Distinguish the failure conditions</h3>
<span class="qa-anchor" id="q-048-a-02"></span><p>The same NSID/CSI can be legal for one CNS and illegal for another; fix the CNS and prerequisites in each test.</p>
<span class="qa-anchor" id="q-048-a-04"></span><p>For unused CNTID, the host clears it and the controller ignores it. For unused CSI, the host should clear it; the controller should ignore it but may return Invalid Field if nonzero.</p>
<span class="qa-anchor" id="q-048-a-07"></span><p>Unsupported CNS:0/02h; incompatible namespace command set:1/2Ch; prohibited terminal cursors for CNS 02h/10h:0/0Bh. For UUID selection, an unsupported UUID for the requested information, an all-zero UUID or the NVMe Invalid UUID shall return 0/02h. CSI handling depends on whether the CNS uses CSI and on the namespace command set.</p>
</section>
<section class="qa-section" id="q-048-s-02" data-answer-section="2"><h3><span>2.</span> Establish the cause from evidence</h3>
<span class="qa-anchor" id="q-048-a-03"></span><p>Figure 336 specifies use of NSID/CNTID/CSI per CNS; UUID-selection capability controls UIDX use.</p>
<span class="qa-anchor" id="q-048-a-05"></span><p>Hold other selectors constant, vary the target field and apply CNS-specific rules before generic defaults.</p>
</section>
<section class="qa-section" id="q-048-s-03" data-answer-section="3"><h3><span>3.</span> Outcome and follow-up checks</h3>
<span class="qa-anchor" id="q-048-a-06"></span><p>Valid queries return 4096 bytes. CNS 11h can return zero-filled data for a defined unallocated NSID, distinct from an invalid-NSID error.</p>
<span class="qa-anchor" id="q-048-a-16"></span><p>Preserve CQE with CDW10/11/14; different selectors can produce the same 0/02h.</p>
<span class="qa-anchor" id="q-048-a-17"></span><p>First check whether the CNS uses that selector. Ignoring an unused field is not automatically a validation omission.</p>
</section>
</div>
<span class="qa-anchor" id="q-048-a-08"></span><span class="qa-anchor" id="q-048-a-09"></span><span class="qa-anchor" id="q-048-a-10"></span><span class="qa-anchor" id="q-048-a-11"></span><span class="qa-anchor" id="q-048-a-12"></span><span class="qa-anchor" id="q-048-a-13"></span><span class="qa-anchor" id="q-048-a-14"></span><span class="qa-anchor" id="q-048-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-idcmd">Base 2.4 §5.2.14.1</a> · <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-uuid">Base 2.4 §8.1.31.1–8.1.31.2</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-idns">NVM Command Set 1.3 §4.1.5.1–4.1.5.4</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-049" data-question="49" data-answer-kind="fields"><h2><a class="qa-qid" href="#q-049">Q49</a> How are SN, MN, FR, MDTS and optional Admin capability fields interpreted?</h2>
<p class="qa-prompt">Explain the units and encoding, then work through one set of values.</p>
<details class="qa-answer" id="q-049-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-049-a-01">One large Identify structure combines identity strings, transfer limits and capability bitmaps, requiring different interpretation methods.</p><div class="qa-sections">
<section class="qa-section" id="q-049-s-01" data-answer-section="1"><h3><span>1.</span> Establish the source and scope</h3>
<span class="qa-anchor" id="q-049-a-02"></span><p>SN/MN identify the subsystem, FR the active firmware, MDTS a transfer limit and OACS optional Admin capabilities.</p>
<span class="qa-anchor" id="q-049-a-03"></span><p>In CNS 01h: SN bytes 23:4, MN63:24, FR71:64, MDTS byte 77 and OACS bytes 257:256.</p>
</section>
<section class="qa-section" id="q-049-s-02" data-answer-section="2"><h3><span>2.</span> Fields, units and worked interpretation</h3>
<span class="qa-anchor" id="q-049-a-04"></span><p>Decode ASCII strings and space padding. Nonzero MDTS limits bytes to 2^MDTS×2^(12+CAP.MPSMIN), not CC.MPS. MDTS=0 removes this limit, not all command-specific limits.</p>
<span class="qa-anchor" id="q-049-a-05"></span><p>Confirm layout/offsets, then decode strings, bits and exponents separately. Check CTRATT.MEM when accounting for metadata in transfer length.</p>
<span class="qa-anchor" id="q-049-a-06"></span><p>MPSMIN=0 and MDTS=5 give 128 KiB. With MEM=0, 32 blocks of 4096-byte data plus 16-byte metadata per block exceed it.</p>
</section>
<section class="qa-section" id="q-049-s-03" data-answer-section="3"><h3><span>3.</span> Conditions that change the interpretation</h3>
<span class="qa-anchor" id="q-049-a-07"></span><p>Exceeding MDTS returns Invalid Field (0/02h). Unsupported optional opcodes generally use 0/01h; a recent revision does not require all options.</p>
<span class="qa-anchor" id="q-049-a-16"></span><p>Compare FR with the currently active firmware slot, not a pending slot; cross-check OACS with corresponding command-support entries.</p>
</section>
</div>
<span class="qa-anchor" id="q-049-a-17"></span><span class="qa-anchor" id="q-049-a-08"></span><span class="qa-anchor" id="q-049-a-09"></span><span class="qa-anchor" id="q-049-a-10"></span><span class="qa-anchor" id="q-049-a-11"></span><span class="qa-anchor" id="q-049-a-12"></span><span class="qa-anchor" id="q-049-a-13"></span><span class="qa-anchor" id="q-049-a-14"></span><span class="qa-anchor" id="q-049-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-cap">Base 2.4 §3.1.4 (CAP, VS)</a> · <a href="#ref-conventions">Base 2.4 §1.4.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-050" data-question="50" data-answer-kind="lookup"><h2><a class="qa-qid" href="#q-050">Q50</a> How can advertised Identify support be cross-checked against commands and the Commands Supported and Effects Log?</h2>
<p class="qa-prompt">Choose the interface and target, then identify the returned field that supports your conclusion.</p>
<details class="qa-answer" id="q-050-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-050-a-01">Connect an advertised bit to a legal operation instead of validating the bit alone.</p><div class="qa-sections">
<section class="qa-section" id="q-050-s-01" data-answer-section="1"><h3><span>1.</span> Select the target and information</h3>
<span class="qa-anchor" id="q-050-a-02"></span><p>Compare the same controller, command set, namespace configuration and time.</p>
<span class="qa-anchor" id="q-050-a-03"></span><p>Check Identify support, LPA.CSES and the correct Admin/I/O opcode&#x27;s CSUPP and effects in LID 05h.</p>
<span class="qa-anchor" id="q-050-a-04"></span><p>Read CSUPP together with LBCC, NCC, NIC, CCC and CSE to understand data/capability/list changes and execution restrictions.</p>
</section>
<section class="qa-section" id="q-050-s-02" data-answer-section="2"><h3><span>2.</span> Query sequence and interpretation</h3>
<span class="qa-anchor" id="q-050-a-05"></span><p>Establish legal prerequisites, discover support, prepare valid parameters/resources, execute, verify result and rediscover information affected by the command.</p>
<span class="qa-anchor" id="q-050-a-06"></span><p>Support means a legal supported operation exists, not that every parameter/state succeeds. Completion must also match the command&#x27;s defined effect.</p>
</section>
<section class="qa-section" id="q-050-s-03" data-answer-section="3"><h3><span>3.</span> Handle missing or inconsistent evidence</h3>
<span class="qa-anchor" id="q-050-a-07"></span><p>0/01h may contradict opcode support, but Invalid Field, Namespace Not Ready or Lockdown first require checking parameters and state.</p>
<span class="qa-anchor" id="q-050-a-16"></span><p>Commands Supported and Effects describes capability/effects, not recent execution history.</p>
<span class="qa-anchor" id="q-050-a-17"></span><p>First check Admin versus I/O entry selection and CSI.</p>
</section>
</div>
<span class="qa-anchor" id="q-050-a-08"></span><span class="qa-anchor" id="q-050-a-09"></span><span class="qa-anchor" id="q-050-a-10"></span><span class="qa-anchor" id="q-050-a-11"></span><span class="qa-anchor" id="q-050-a-12"></span><span class="qa-anchor" id="q-050-a-13"></span><span class="qa-anchor" id="q-050-a-14"></span><span class="qa-anchor" id="q-050-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-effects">Base 2.4 §5.2.13.1.6</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-idcmd">Base 2.4 §5.2.14.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-051" data-question="51" data-answer-kind="process"><h2><a class="qa-qid" href="#q-051">Q51</a> Which Identify data and lists change after namespace creation, deletion, attachment, detachment or format?</h2>
<p class="qa-prompt">Order the actions and identify which completion must precede the next action.</p>
<details class="qa-answer" id="q-051-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-051-a-01">Connect configuration changes to rediscovery instead of continuing with stale capacity, format or attachment data.</p><div class="qa-sections">
<section class="qa-section" id="q-051-s-01" data-answer-section="1"><h3><span>1.</span> Prepare the operation</h3>
<span class="qa-anchor" id="q-051-a-02"></span><p>Create/Delete change existence, Attach/Detach controller accessibility, and Format the data format within its defined scope.</p>
<span class="qa-anchor" id="q-051-a-03"></span><p>OACS.NMS advertises namespace management; Format also uses OACS/FNA and NVM format support.</p>
<span class="qa-anchor" id="q-051-a-04"></span><p>Separately inspect allocated/active lists, CNS 12h attached controllers and namespace format/capacity fields such as FLBAS/DPS/NSZE/NCAP.</p>
</section>
<section class="qa-section" id="q-051-s-02" data-answer-section="2"><h3><span>2.</span> Sequence and completion conditions</h3>
<span class="qa-anchor" id="q-051-a-05"></span><p>Capture before-state, wait for management completion, then reread affected lists/namespace data. Successful Create does not automatically attach the namespace.</p>
<span class="qa-anchor" id="q-051-a-06"></span><p>Create adds to Allocated; Attach adds to the target Active list; Detach removes from that Active list without necessarily deallocating; Format updates the selected format rather than necessarily changing NSID.</p>
</section>
<section class="qa-section" id="q-051-s-03" data-answer-section="3"><h3><span>3.</span> Handle unmet conditions</h3>
<span class="qa-anchor" id="q-051-a-07"></span><p>A failed management command does not universally imply either every change occurred or none occurred; examine its failure/partial-operation rules and rediscover.</p>
<span class="qa-anchor" id="q-051-a-16"></span><p>Correlate management results, lists, namespace data and applicable Changed Namespace notification. The event is not a full replacement for Identify configuration data.</p>
</section>
<section class="qa-section" id="q-051-s-04" data-answer-section="4"><h3><span>4.</span> Evidence supplied by the log</h3>
<span class="qa-anchor" id="q-051-a-10"></span><p>Check Changed Namespace List (LID 04h) alongside fresh Identify data. The list identifies changed NSIDs, not current configuration. RAE affects acknowledgement; preserve the event and list before subsequent queries.</p>
</section>
</div>
<span class="qa-anchor" id="q-051-a-17"></span><span class="qa-anchor" id="q-051-a-08"></span><span class="qa-anchor" id="q-051-a-09"></span><span class="qa-anchor" id="q-051-a-11"></span><span class="qa-anchor" id="q-051-a-12"></span><span class="qa-anchor" id="q-051-a-13"></span><span class="qa-anchor" id="q-051-a-14"></span><span class="qa-anchor" id="q-051-a-15"></span>
<p class="qa-related">Related mechanisms: <a href="/nvme/question-bank/namespace-management/en/#q-167">Q167</a></p>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-idns">NVM Command Set 1.3 §4.1.5.1–4.1.5.4</a> · <a href="#ref-nsmanage">Base 2.4 §5.2.24–5.2.25, 8.1.17</a> · <a href="#ref-effects">Base 2.4 §5.2.13.1.6</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-nschange">Base 2.4 §5.2.13.1.5, 5.2.13.1.14.2.6–5.2.13.1.14.2.8</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-052" data-question="52" data-answer-kind="lifecycle"><h2><a class="qa-qid" href="#q-052">Q52</a> Which Identify data may change after firmware activation, reset or power cycling?</h2>
<p class="qa-prompt">Name the reset or interruption, then assess settings, ongoing operations and data separately.</p>
<details class="qa-answer" id="q-052-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-052-a-01">Judge change by field semantics instead of requiring the whole 4096-byte buffer to remain identical.</p><div class="qa-sections">
<section class="qa-section" id="q-052-s-01" data-answer-section="1"><h3><span>1.</span> Identify the trigger and affected objects</h3>
<span class="qa-anchor" id="q-052-a-02"></span><p>Separate stable identity, firmware-advertised capability, persistent configuration and dynamic state.</p>
<span class="qa-anchor" id="q-052-a-03"></span><p>Preserve identity, namespace stable identifiers, FR, capabilities, capacity/format/attachments and dynamic fields as separate comparison groups.</p>
</section>
<section class="qa-section" id="q-052-s-02" data-answer-section="2"><h3><span>2.</span> State changes and recovery</h3>
<span class="qa-anchor" id="q-052-a-04"></span><p>FR describes active firmware. Rediscover MDTS/capabilities after an update; dynamic fields such as NUSE are not fixed identities.</p>
<span class="qa-anchor" id="q-052-a-05"></span><p>Record whether reset/power cycling also activated firmware or changed configuration. Reread with identical selectors and compare by field definition.</p>
<span class="qa-anchor" id="q-052-a-06"></span><p>Ordinary reset is not a rename, namespace deletion or format operation. Concurrent firmware activation can change FR and legitimately change advertised capabilities.</p>
</section>
<section class="qa-section" id="q-052-s-03" data-answer-section="3"><h3><span>3.</span> Verify retention and recovery</h3>
<span class="qa-anchor" id="q-052-a-07"></span><p>Comparison has no new status. For failed post-reset Identify distinguish incomplete initialization, invalid NSID and wrong CNS before attributing every difference to firmware.</p>
<span class="qa-anchor" id="q-052-a-16"></span><p>Confirm object identity with stable IDs. Preserve raw bytes while separating padding, reserved/dynamic fields and meaningful changes.</p>
<span class="qa-anchor" id="q-052-a-17"></span><p>First check concurrent pending firmware activation and accidental selection of another controller/namespace.</p>
</section>
</div>
<span class="qa-anchor" id="q-052-a-08"></span><span class="qa-anchor" id="q-052-a-09"></span><span class="qa-anchor" id="q-052-a-10"></span><span class="qa-anchor" id="q-052-a-11"></span><span class="qa-anchor" id="q-052-a-12"></span><span class="qa-anchor" id="q-052-a-13"></span><span class="qa-anchor" id="q-052-a-14"></span><span class="qa-anchor" id="q-052-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-identity">Base 2.4 §4.7.1</a> · <a href="#ref-idns">NVM Command Set 1.3 §4.1.5.1–4.1.5.4</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-effects">Base 2.4 §5.2.13.1.6</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-053" data-question="53" data-answer-kind="diagnose"><h2><a class="qa-qid" href="#q-053">Q53</a> How should inconsistencies among Identify, features, logs and command behavior be investigated?</h2>
<p class="qa-prompt">Separate available evidence from missing information before judging conformance.</p>
<details class="qa-answer" id="q-053-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-053-a-01">Build a complete evidence chain instead of letting one advertised capability override current conditions.</p><div class="qa-sections">
<section class="qa-section" id="q-053-s-01" data-answer-section="1"><h3><span>1.</span> Preserve the evidence first</h3>
<span class="qa-anchor" id="q-053-a-02"></span><p>Hold controller, NSID, CSI, time and configuration constant; different views/times need not describe the same state.</p>
<span class="qa-anchor" id="q-053-a-03"></span><p>Identify discovers capability, Get Features configuration, and logs state/events or effect declarations. Their roles differ.</p>
<span class="qa-anchor" id="q-053-a-04"></span><p>Preserve SQE/CQE, raw Identify, Feature SEL and log selectors. Distinguish Current from Supported Capabilities.</p>
</section>
<section class="qa-section" id="q-053-s-02" data-answer-section="2"><h3><span>2.</span> Work through the possible causes</h3>
<span class="qa-anchor" id="q-053-a-17"></span><p>First verify that all evidence describes the same controller/namespace, configuration interval and selectors.</p>
<span class="qa-anchor" id="q-053-a-05"></span><p>Check revision/decoding, scope/selectors, legal parameters, current state/order and result; isolate one variable when reproducing.</p>
</section>
<section class="qa-section" id="q-053-s-03" data-answer-section="3"><h3><span>3.</span> Decide what the evidence supports</h3>
<span class="qa-anchor" id="q-053-a-06"></span><p>Consistency means the specified relationships hold, not equal numeric values. CHANG=1 and Current=0 can both be correct.</p>
<span class="qa-anchor" id="q-053-a-07"></span><p>Use original SCT/SC for next steps and associated Error Information when More=1. A host timeout without status first requires locating the submission/completion stage.</p>
<span class="qa-anchor" id="q-053-a-16"></span><p>A defensible noncompliance conclusion requires fixed prerequisites, object and timing, plus a remaining contradiction with an explicit requirement.</p>
</section>
</div>
<span class="qa-anchor" id="q-053-a-08"></span><span class="qa-anchor" id="q-053-a-09"></span><span class="qa-anchor" id="q-053-a-10"></span><span class="qa-anchor" id="q-053-a-11"></span><span class="qa-anchor" id="q-053-a-12"></span><span class="qa-anchor" id="q-053-a-13"></span><span class="qa-anchor" id="q-053-a-14"></span><span class="qa-anchor" id="q-053-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-idcmd">Base 2.4 §5.2.14.1</a> · <a href="#ref-effects">Base 2.4 §5.2.13.1.6</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-getfeat">Base 2.4 §5.2.12</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>

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
