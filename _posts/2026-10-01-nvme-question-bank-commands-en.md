---
layout: post
title: "NVMe Self-Study Bank: Commands, completions and processing order"
date: 2026-10-01 00:00:00 +0800
categories: [nvme]
permalink: /nvme/question-bank/commands/en/
lang: en
nvme_quickref: true
nvme_qa: true
---

<div class="nvme-quickref nvme-qa">
<nav class="qr-top" aria-label="Bank and editions"><a href="#content">Skip to content</a><a href="/nvme/question-bank/en/">Question index</a><a href="/nvme/question-bank/commands/zh-tw/">繁體中文</a><a href="/DOCS/nvme-question-bank/commands.html">Chinese tutorial HTML</a></nav>
<main id="content"><p class="qr-eyebrow">BASE 2.4 / NVM 1.3 / PCIe 1.4 · Q1–328</p>
<header><p class="qa-range">Q31–Q43</p><h1>Commands, completions and processing order</h1><p class="qr-intro">Follow submission, consumption, processing, completion and host reclamation to learn what each field proves. Ordering, arbitration, fairness and interrupts answer different questions; completion order alone cannot establish them all.</p><p>Practice first, then reveal the explanation. Each question uses the prose, field interpretation, comparison or flow that suits it. All numerical examples are hypothetical. Status is written SCT/SC; h indicates hexadecimal.</p></header>
<aside class="qa-glossary"><h2>Terms used in this volume</h2><dl><dt>Controller / namespace</dt><dd>A controller receives commands and manages access. A namespace is a logical storage space that commands can address. An NVM subsystem contains controllers and nonvolatile storage resources.</dd><dt>SQ / CQ / SQE / CQE</dt><dd>Submission and Completion Queues carry command entries (SQEs) and completion entries (CQEs). QID identifies a queue, CID distinguishes outstanding commands in one SQ, and NSID identifies a namespace.</dd><dt>Register / Identify / Feature / Log</dt><dd>A register exposes control or state. Identify queries capabilities and attributes; features query or configure operation; log pages report specific state or records. FID, LID, CNS and CSI select features, logs, Identify structures and command sets.</dd><dt>index / offset / zero-based</dt><dd>An index selects an entry, usually starting at 0; an offset measures distance from an origin in specified units. A zero-based count encodes count−1, but not every zero-valued field is a count. A Dword is 4 bytes; a byte is 8 bits.</dd><dt>Scope / reset / retention</dt><dd>Scope names the affected objects; retention means preserving state. Controller Reset (clearing CC.EN) is one form of Controller Level Reset, or CLR. Different CLR triggers can retain different registers.</dd></dl></aside>
<section id="overview" class="qa-overview"><h2>Five observations during one command lifetime</h2><p class="qa-takeaway">Evidence of progress is not evidence of success; identify the stage you actually observed.</p>
<div class="qr-table" tabindex="0" role="region" aria-label="Horizontally scrollable comparison table"><table><thead><tr><th scope="col">Stage</th><th scope="col">What is established</th><th scope="col">What is not yet established</th></tr></thead><tbody><tr><td>SQE prepared</td><td>Host filled opcode, CID, NSID and data pointers</td><td>Controller visibility</td></tr><tr><td>SQ tail updated</td><td>Submission, with separately ensured memory visibility</td><td>Consumption or completion</td></tr><tr><td>A CQE reports an advanced SQHD</td><td>Consumption reached the reported position</td><td>Completion of all commands from those slots</td></tr><tr><td>Target CQE has valid phase</td><td>Correlate SQID+CID and inspect SCT/SC</td><td>Interrupt delivery or unconditional persistence</td></tr><tr><td>Host advances CQ head</td><td>Host consumed completions and released CQ space</td><td>Completion of other SQs or CIDs</td></tr></tbody></table></div>
<p><strong>Worked interpretation: </strong>SQ1/CID 7 and SQ2/CID 7 can coexist. In a shared CQ, CID 7 alone is insufficient: read SQID. Write persistence additionally requires WCE, FUA or Flush completion conditions, not only success status.</p>
<p class="qa-citations">Sources: <a href="#ref-sqe">Base 2.4 §4.1.1</a> · <a href="#ref-cqe">Base 2.4 §4.2.1, 4.2.3–4.2.4</a> · <a href="#ref-order">Base 2.4 §3.4.1–3.4.5</a> · <a href="#ref-vwc">Base 2.4 §5.2.30.1.4</a> · <a href="#ref-nvmatomic">NVM Command Set 1.3 §2.1.2–2.1.4</a></p>
</section>
<div class="qa-controls" hidden><label>Search this page <input type="search" id="qa-search" placeholder="Question number, field or keyword"></label><button type="button" data-expand="true">Expand all answers</button><button type="button" data-expand="false">Collapse all answers</button><output id="qa-count" aria-live="polite"></output></div>
<section id="question-index"><h2>Questions in this volume</h2><ol class="qa-index">
<li><a href="#q-031">Q31 · What do Opcode, CID, NSID, Data Pointer and command dwords mean?</a></li>
<li><a href="#q-032">Q32 · How are nonzero reserved fields, illegal field combinations and unsupported opcodes handled?</a></li>
<li><a href="#q-033">Q33 · Which statuses apply to invalid, inactive, unused and improperly broadcast NSIDs?</a></li>
<li><a href="#q-034">Q34 · What are SQHD, SQID, CID, phase and status used for in a CQE?</a></li>
<li><a href="#q-035">Q35 · How should Status Code Type and Status Code be decoded?</a></li>
<li><a href="#q-036">Q36 · What do More and DNR mean, and does DNR=0 guarantee an immediate safe retry?</a></li>
<li><a href="#q-037">Q37 · Why might a posted completion remain unprocessed by the host?</a></li>
<li><a href="#q-038">Q38 · Must outstanding commands complete in submission order?</a></li>
<li><a href="#q-039">Q39 · Which commands have ordering dependencies, and why is universal ordered completion unsafe to assume?</a></li>
<li><a href="#q-040">Q40 · How do outstanding limits and CQ Full constrain further command handling?</a></li>
<li><a href="#q-041">Q41 · How do Round Robin and Weighted Round Robin arbitration differ?</a></li>
<li><a href="#q-042">Q42 · When do Urgent, High, Medium and Low queue priorities take effect?</a></li>
<li><a href="#q-043">Q43 · How can arbitration be evaluated when multiple queues compete?</a></li>
</ol></section>
<article class="qa-question" id="q-031" data-question="31" data-answer-kind="fields"><h2><a class="qa-qid" href="#q-031">Q31</a> What do Opcode, CID, NSID, Data Pointer and command dwords mean?</h2>
<p class="qa-prompt">Explain the units and encoding, then work through one set of values.</p>
<details class="qa-answer" id="q-031-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-031-a-01">Encode the operation, target, data location and parameters into a command the controller can read.</p><div class="qa-sections">
<section class="qa-section" id="q-031-s-01" data-answer-section="1"><h3><span>1.</span> Establish the source and scope</h3>
<span class="qa-anchor" id="q-031-a-02"></span><p>Opcode interpretation depends on the Admin/I/O command set; equal numeric values need not mean the same operation across sets.</p>
<span class="qa-anchor" id="q-031-a-03"></span><p>Check capabilities such as OACS, ONCS and SGLS and the namespace CSI. Not every command uses every common field.</p>
</section>
<section class="qa-section" id="q-031-s-02" data-answer-section="2"><h3><span>2.</span> Fields, units and worked interpretation</h3>
<span class="qa-anchor" id="q-031-a-04"></span><p>CDW0 contains OPC, FUSE, PSDT and CID. NSID selects the target, MPTR/DPTR describe data, and CDW10–15 are command-specific. The common command is 64 bytes.</p>
<span class="qa-anchor" id="q-031-a-05"></span><p>Select command set, opcode/support, legal NSID/parameters, data/pointers and a unique outstanding CID, then submit. PCIe Admin commands use PRPs, not arbitrary SGLs.</p>
<span class="qa-anchor" id="q-031-a-06"></span><p>Match completion by SQID+CID. Results may reside in the host buffer or CQE DW0/1, not solely Status.</p>
</section>
<section class="qa-section" id="q-031-s-03" data-answer-section="3"><h3><span>3.</span> Conditions that change the interpretation</h3>
<span class="qa-anchor" id="q-031-a-07"></span><p>Unsupported opcode uses Invalid Command Opcode (0/01h). Invalid defined fields generally use Invalid Field (0/02h), subject to specific error definitions.</p>
<span class="qa-anchor" id="q-031-a-16"></span><p>Cross-check command-set context, support and payload size. A valid DPTR address does not prove sufficient described data length.</p>
</section>
</div>
<span class="qa-anchor" id="q-031-a-17"></span><span class="qa-anchor" id="q-031-a-08"></span><span class="qa-anchor" id="q-031-a-09"></span><span class="qa-anchor" id="q-031-a-10"></span><span class="qa-anchor" id="q-031-a-11"></span><span class="qa-anchor" id="q-031-a-12"></span><span class="qa-anchor" id="q-031-a-13"></span><span class="qa-anchor" id="q-031-a-14"></span><span class="qa-anchor" id="q-031-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-sqe">Base 2.4 §4.1.1</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-032" data-question="32" data-answer-kind="error"><h2><a class="qa-qid" href="#q-032">Q32</a> How are nonzero reserved fields, illegal field combinations and unsupported opcodes handled?</h2>
<p class="qa-prompt">Distinguish failure conditions before deciding whether a particular response is required.</p>
<details class="qa-answer" id="q-032-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-032-a-01">Distinguish reserved bits from reserved coded values in defined fields; not every reserved bit requires receiver validation.</p><div class="qa-sections">
<section class="qa-section" id="q-032-s-01" data-answer-section="1"><h3><span>1.</span> Distinguish the failure conditions</h3>
<span class="qa-anchor" id="q-032-a-02"></span><p>Host construction requirements and controller validation requirements are separate.</p>
<span class="qa-anchor" id="q-032-a-04"></span><p>The host shall zero reserved fields; the recipient need not check reserved bits/bytes/fields. A reserved coded value in a defined command field shall be reported as an error.</p>
<span class="qa-anchor" id="q-032-a-07"></span><p>Unsupported/reserved opcode: 0/01h. Illegal defined field: generally 0/02h unless a specific status applies. Multiple faults usually permit choosing one; nonzero reserved bits do not universally mandate 0/02h.</p>
</section>
<section class="qa-section" id="q-032-s-02" data-answer-section="2"><h3><span>2.</span> Establish the cause from evidence</h3>
<span class="qa-anchor" id="q-032-a-03"></span><p>Use Base §1.4.1 reserved semantics, opcode support and the individual command&#x27;s field restrictions.</p>
<span class="qa-anchor" id="q-032-a-05"></span><p>Start from a zeroed SQE and populate used fields. Change one item per error exercise and record whether the requirement says shall or should.</p>
</section>
<section class="qa-section" id="q-032-s-03" data-answer-section="3"><h3><span>3.</span> Outcome and follow-up checks</h3>
<span class="qa-anchor" id="q-032-a-06"></span><p>A legal combination follows normal completion. Lack of reserved-bit checking does not make a nonzero host value legal.</p>
<span class="qa-anchor" id="q-032-a-16"></span><p>Record both host violation and controller detection obligations to avoid labeling permitted nonchecking as a firmware bug.</p>
<span class="qa-anchor" id="q-032-a-17"></span><p>First ask whether the modified item is a reserved bit or a reserved encoding within a defined field.</p>
</section>
</div>
<span class="qa-anchor" id="q-032-a-08"></span><span class="qa-anchor" id="q-032-a-09"></span><span class="qa-anchor" id="q-032-a-10"></span><span class="qa-anchor" id="q-032-a-11"></span><span class="qa-anchor" id="q-032-a-12"></span><span class="qa-anchor" id="q-032-a-13"></span><span class="qa-anchor" id="q-032-a-14"></span><span class="qa-anchor" id="q-032-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-conventions">Base 2.4 §1.4.1</a> · <a href="#ref-sqe">Base 2.4 §4.1.1</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-033" data-question="33" data-answer-kind="error"><h2><a class="qa-qid" href="#q-033">Q33</a> Which statuses apply to invalid, inactive, unused and improperly broadcast NSIDs?</h2>
<p class="qa-prompt">Distinguish failure conditions before deciding whether a particular response is required.</p>
<details class="qa-answer" id="q-033-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-033-a-01">Separate invalid identity, inactive namespace and a command that does not use NSID.</p><div class="qa-sections">
<section class="qa-section" id="q-033-s-01" data-answer-section="1"><h3><span>1.</span> Distinguish the failure conditions</h3>
<span class="qa-anchor" id="q-033-a-02"></span><p>Active state is controller-relative. Accessibility through another path does not establish activity on this controller.</p>
<span class="qa-anchor" id="q-033-a-04"></span><p>Distinguish zero, valid allocated, inactive and FFFFFFFFh identifiers. Each command defines the scope of FFFFFFFFh.</p>
<span class="qa-anchor" id="q-033-a-07"></span><p>Figure 93 defaults: inactive on an NSID-using command returns 0/02h, invalid returns 0/0Bh. Unsupported broadcast or nonzero NSID on an unused field returns 0/02h. Command-specific exceptions take precedence.</p>
</section>
<section class="qa-section" id="q-033-s-02" data-answer-section="2"><h3><span>2.</span> Establish the cause from evidence</h3>
<span class="qa-anchor" id="q-033-a-03"></span><p>Use active/allocated lists and the command&#x27;s NSID rules, then check command-specific exceptions.</p>
<span class="qa-anchor" id="q-033-a-05"></span><p>Determine whether NSID is used, then permitted namespace state and broadcast support. Some Identify CNS values intentionally query allocated/inactive namespaces.</p>
</section>
<section class="qa-section" id="q-033-s-03" data-answer-section="3"><h3><span>3.</span> Outcome and follow-up checks</h3>
<span class="qa-anchor" id="q-033-a-06"></span><p>Legal targets follow the command&#x27;s completion rules. Some queries define special replies for absent/inactive objects that override the generic rule.</p>
<span class="qa-anchor" id="q-033-a-16"></span><p>Correlate the original NSID, the list at that time and CNS/FID/opcode rules. A current list alone may not explain a past request.</p>
<span class="qa-anchor" id="q-033-a-17"></span><p>First check whether the command uses the generic rule or defines an explicit exception.</p>
</section>
</div>
<span class="qa-anchor" id="q-033-a-08"></span><span class="qa-anchor" id="q-033-a-09"></span><span class="qa-anchor" id="q-033-a-10"></span><span class="qa-anchor" id="q-033-a-11"></span><span class="qa-anchor" id="q-033-a-12"></span><span class="qa-anchor" id="q-033-a-13"></span><span class="qa-anchor" id="q-033-a-14"></span><span class="qa-anchor" id="q-033-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-sqe">Base 2.4 §4.1.1</a> · <a href="#ref-nsid">Base 2.4 §3.2.1</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-034" data-question="34" data-answer-kind="fields"><h2><a class="qa-qid" href="#q-034">Q34</a> What are SQHD, SQID, CID, phase and status used for in a CQE?</h2>
<p class="qa-prompt">Explain the units and encoding, then work through one set of values.</p>
<details class="qa-answer" id="q-034-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-034-a-01">A CQE carries command result, identity and queue progress; these fields are not interchangeable.</p><div class="qa-sections">
<section class="qa-section" id="q-034-s-01" data-answer-section="1"><h3><span>1.</span> Establish the source and scope</h3>
<span class="qa-anchor" id="q-034-a-02"></span><p>SQHD describes the identified SQ, P the CQ slot, and Status the command identified by SQID+CID.</p>
<span class="qa-anchor" id="q-034-a-03"></span><p>Interpret using current queue configuration and the common CQE layout, not a feature-selected meaning of SQHD.</p>
</section>
<section class="qa-section" id="q-034-s-02" data-answer-section="2"><h3><span>2.</span> Fields, units and worked interpretation</h3>
<span class="qa-anchor" id="q-034-a-04"></span><p>DW2 contains SQHD/SQID; DW3 contains CID/P/Status; DW0/1 carry command-specific results. SQHD reports consumption when that CQE was constructed.</p>
<span class="qa-anchor" id="q-034-a-05"></span><p>Validate P, match SQID+CID, decode status/results, update SQ slot availability and finally release the CQ slot.</p>
<span class="qa-anchor" id="q-034-a-06"></span><p>SQHD=8 reports head advancement to eight; it does not establish execution completion of every command from slots zero through seven.</p>
</section>
<section class="qa-section" id="q-034-s-03" data-answer-section="3"><h3><span>3.</span> Conditions that change the interpretation</h3>
<span class="qa-anchor" id="q-034-a-07"></span><p>Decode SCT and SC together; P is not an error code. Malformed CQEs or unknown CIDs require checking memory/lifetimes, not inventing a new NVMe status.</p>
<span class="qa-anchor" id="q-034-a-16"></span><p>Distinguish SQ consumption, command completion and data-buffer reclamation. Reusable SQ slots do not permit early release of command data.</p>
</section>
</div>
<span class="qa-anchor" id="q-034-a-17"></span><span class="qa-anchor" id="q-034-a-08"></span><span class="qa-anchor" id="q-034-a-09"></span><span class="qa-anchor" id="q-034-a-10"></span><span class="qa-anchor" id="q-034-a-11"></span><span class="qa-anchor" id="q-034-a-12"></span><span class="qa-anchor" id="q-034-a-13"></span><span class="qa-anchor" id="q-034-a-14"></span><span class="qa-anchor" id="q-034-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-cqe">Base 2.4 §4.2.1, 4.2.3–4.2.4</a> · <a href="#ref-queue">Base 2.4 §3.3.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-035" data-question="35" data-answer-kind="fields"><h2><a class="qa-qid" href="#q-035">Q35</a> How should Status Code Type and Status Code be decoded?</h2>
<p class="qa-prompt">Explain the units and encoding, then work through one set of values.</p>
<details class="qa-answer" id="q-035-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-035-a-01">The same SC can mean different things under different SCTs; decode the pair.</p><div class="qa-sections">
<section class="qa-section" id="q-035-s-01" data-answer-section="1"><h3><span>1.</span> Establish the source and scope</h3>
<span class="qa-anchor" id="q-035-a-02"></span><p>Status belongs to this completion and must be interpreted with opcode, command set and failure conditions.</p>
<span class="qa-anchor" id="q-035-a-03"></span><p>Base defines common SCT/SC values; use NVM definitions for its specific codes, not another command set&#x27;s table.</p>
</section>
<section class="qa-section" id="q-035-s-02" data-answer-section="2"><h3><span>2.</span> Fields, units and worked interpretation</h3>
<span class="qa-anchor" id="q-035-a-04"></span><p>In CQE DW3, SCT is bits 27:25, SC bits 24:17 and P bit 16. In the final 16-bit word, SCT occupies bits 11:9 and SC bits 8:1.</p>
<span class="qa-anchor" id="q-035-a-05"></span><p>Confirm data width/endianness, extract SCT/SC, select the correct table, then inspect DNR, More, CRD and command-specific results.</p>
<span class="qa-anchor" id="q-035-a-06"></span><p>SCT=0, SC=00h means Successful Completion, but matching and phase still matter; zero low bits alone do not establish a new valid success.</p>
</section>
<section class="qa-section" id="q-035-s-03" data-answer-section="3"><h3><span>3.</span> Conditions that change the interpretation</h3>
<span class="qa-anchor" id="q-035-a-07"></span><p>For example, 0/01h is Invalid Command Opcode and 1/01h Invalid Queue Identifier. SCT 2 is Media/Data Integrity, SCT 3 Path Related and SCT 7 Vendor Specific.</p>
<span class="qa-anchor" id="q-035-a-16"></span><p>Preserve raw CQE bytes and decoded values. Tools that remove P or repack status cannot have their integers compared blindly.</p>
</section>
</div>
<span class="qa-anchor" id="q-035-a-17"></span><span class="qa-anchor" id="q-035-a-08"></span><span class="qa-anchor" id="q-035-a-09"></span><span class="qa-anchor" id="q-035-a-10"></span><span class="qa-anchor" id="q-035-a-11"></span><span class="qa-anchor" id="q-035-a-12"></span><span class="qa-anchor" id="q-035-a-13"></span><span class="qa-anchor" id="q-035-a-14"></span><span class="qa-anchor" id="q-035-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-cqe">Base 2.4 §4.2.1, 4.2.3–4.2.4</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-036" data-question="36" data-answer-kind="concept"><h2><a class="qa-qid" href="#q-036">Q36</a> What do More and DNR mean, and does DNR=0 guarantee an immediate safe retry?</h2>
<p class="qa-prompt">Explain the mechanism in your own words and identify a common misconception.</p>
<details class="qa-answer" id="q-036-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-036-a-01">Separate potential retry success, additional error information and retry safety.</p><div class="qa-sections">
<section class="qa-section" id="q-036-s-01" data-answer-section="1"><h3><span>1.</span> Mechanism and scope</h3>
<span class="qa-anchor" id="q-036-a-02"></span><p>Decode the same CQE; DNR&#x27;s identical-command retry semantics cover any controller in the same subsystem.</p>
<span class="qa-anchor" id="q-036-a-04"></span><p>DNR does not establish that data was unchanged. More=1 points to additional status in LID 01h, not another completion.</p>
</section>
<section class="qa-section" id="q-036-s-02" data-answer-section="2"><h3><span>2.</span> Understand it through actions and results</h3>
<span class="qa-anchor" id="q-036-a-03"></span><p>The common bits always exist; CRD use additionally depends on Host Behavior Support.ACRE and Identify.CRDT1–3.</p>
<span class="qa-anchor" id="q-036-a-05"></span><p>Decode the cause; with DNR=0, address transient conditions, respect valid CRD guidance and assess retry safety. For non-idempotent work, determine whether the earlier operation took effect.</p>
<span class="qa-anchor" id="q-036-a-06"></span><p>Only the new CQE establishes retry success. DNR=0 means may succeed, not immediate or duplicate-free success.</p>
</section>
<section class="qa-section" id="q-036-s-03" data-answer-section="3"><h3><span>3.</span> Avoid a misleading conclusion</h3>
<span class="qa-anchor" id="q-036-a-07"></span><p>Repeating unchanged invalid parameters is not useful. Apply explicit DNR rules: Command Interrupted (0/21h) requires DNR=0 and may be returned only with ACRE enabled.</p>
<span class="qa-anchor" id="q-036-a-16"></span><p>More=1 must correspond to associated additional Error Information. Interpret CRD only when DNR/ACRE make it applicable.</p>
</section>
</div>
<span class="qa-anchor" id="q-036-a-17"></span><span class="qa-anchor" id="q-036-a-08"></span><span class="qa-anchor" id="q-036-a-09"></span><span class="qa-anchor" id="q-036-a-10"></span><span class="qa-anchor" id="q-036-a-11"></span><span class="qa-anchor" id="q-036-a-12"></span><span class="qa-anchor" id="q-036-a-13"></span><span class="qa-anchor" id="q-036-a-14"></span><span class="qa-anchor" id="q-036-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-behavior">Base 2.4 §5.2.30.1.15</a> · <a href="#ref-fatal">Base 2.4 §9.1–9.6.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-037" data-question="37" data-answer-kind="diagnose"><h2><a class="qa-qid" href="#q-037">Q37</a> Why might a posted completion remain unprocessed by the host?</h2>
<p class="qa-prompt">Separate available evidence from missing information before judging conformance.</p>
<details class="qa-answer" id="q-037-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-037-a-01">Separate completion posting, notification delivery and host consumption.</p><div class="qa-sections">
<section class="qa-section" id="q-037-s-01" data-answer-section="1"><h3><span>1.</span> Preserve the evidence first</h3>
<span class="qa-anchor" id="q-037-a-02"></span><p>This involves CQ memory, host Head/expected phase and interrupt routing, not necessarily execution failure.</p>
<span class="qa-anchor" id="q-037-a-03"></span><p>Check Create CQ.IEN/IV, the selected MSI/MSI-X mode, masks and interrupt features.</p>
<span class="qa-anchor" id="q-037-a-04"></span><p>For MSI-X inspect Function Mask, vector mask and PBA; ordinary MSI uses different INTMS/INTMC rules. CQE validity still depends on location and phase.</p>
</section>
<section class="qa-section" id="q-037-s-02" data-answer-section="2"><h3><span>2.</span> Work through the possible causes</h3>
<span class="qa-anchor" id="q-037-a-17"></span><p>First check CQ/slot selection and expected phase before assuming interrupt loss.</p>
<span class="qa-anchor" id="q-037-a-05"></span><p>Inspect the correct CQ Head and phase first. Process valid CQEs; investigate missing interrupts through IEN, IV, masks, coalescing and the host handler.</p>
</section>
<section class="qa-section" id="q-037-s-03" data-answer-section="3"><h3><span>3.</span> Decide what the evidence supports</h3>
<span class="qa-anchor" id="q-037-a-06"></span><p>Polling can consume a valid completion without a one-to-one interrupt. Interrupt count need not equal completion count.</p>
<span class="qa-anchor" id="q-037-a-07"></span><p>Missing an interrupt does not itself carry an NVMe error status; the CQE may be successful. Do not invent Internal Error for it.</p>
<span class="qa-anchor" id="q-037-a-16"></span><p>Compare posting, masking, interrupt delivery and Head-update times. An IRQ is notification, not the completion payload itself.</p>
</section>
</div>
<span class="qa-anchor" id="q-037-a-08"></span><span class="qa-anchor" id="q-037-a-09"></span><span class="qa-anchor" id="q-037-a-10"></span><span class="qa-anchor" id="q-037-a-11"></span><span class="qa-anchor" id="q-037-a-12"></span><span class="qa-anchor" id="q-037-a-13"></span><span class="qa-anchor" id="q-037-a-14"></span><span class="qa-anchor" id="q-037-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-cqe">Base 2.4 §4.2.1, 4.2.3–4.2.4</a> · <a href="#ref-pcie">PCIe Transport 1.4 §3.1–3.4</a> · <a href="#ref-irq">PCIe Transport 1.4 §3.5</a> · <a href="#ref-irqfeat">Base 2.4 §5.2.30.2.1–5.2.30.2.2</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-038" data-question="38" data-answer-kind="concept"><h2><a class="qa-qid" href="#q-038">Q38</a> Must outstanding commands complete in submission order?</h2>
<p class="qa-prompt">Explain the mechanism in your own words and identify a common misconception.</p>
<details class="qa-answer" id="q-038-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-038-a-01">Understand that queued submission order is not a universal execution/completion-order guarantee.</p><div class="qa-sections">
<section class="qa-section" id="q-038-s-01" data-answer-section="1"><h3><span>1.</span> Which stages are ordered</h3>
<span class="qa-anchor" id="q-038-a-02"></span><p>Independent commands need not complete FIFO even within one SQ; nearby submission times across SQs do not establish dependency.</p>
<span class="qa-anchor" id="q-038-a-03"></span><p>Check for a fused operation or command-specific ordering rule; FUSES advertises fused support.</p>
<span class="qa-anchor" id="q-038-a-04"></span><p>Distinguish submitted, consumed, processing and completed stages. SQHD only reports consumption.</p>
</section>
<section class="qa-section" id="q-038-s-02" data-answer-section="2"><h3><span>2.</span> How the host handles dependencies</h3>
<span class="qa-anchor" id="q-038-a-05"></span><p>If B depends on A, wait for A&#x27;s successful completion before submitting B. Apply Flush/FUA separately for persistence.</p>
<span class="qa-anchor" id="q-038-a-06"></span><p>Independent Read B may legally complete before Read A; match by SQID/CID rather than submission-array order.</p>
<span class="qa-anchor" id="q-038-a-07"></span><p>Out-of-order completion alone has no error status. Violations of defined multicommand sequences follow their own errors.</p>
<span class="qa-anchor" id="q-038-a-16"></span><p>Test required causal relations rather than treating apparent reordering alone as noncompliance.</p>
</section>
</div>
<span class="qa-anchor" id="q-038-a-17"></span><span class="qa-anchor" id="q-038-a-08"></span><span class="qa-anchor" id="q-038-a-09"></span><span class="qa-anchor" id="q-038-a-10"></span><span class="qa-anchor" id="q-038-a-11"></span><span class="qa-anchor" id="q-038-a-12"></span><span class="qa-anchor" id="q-038-a-13"></span><span class="qa-anchor" id="q-038-a-14"></span><span class="qa-anchor" id="q-038-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-order">Base 2.4 §3.4.1–3.4.5</a> · <a href="#ref-nvmatomic">NVM Command Set 1.3 §2.1.2–2.1.4</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-039" data-question="39" data-answer-kind="concept"><h2><a class="qa-qid" href="#q-039">Q39</a> Which commands have ordering dependencies, and why is universal ordered completion unsafe to assume?</h2>
<p class="qa-prompt">Explain the mechanism in your own words and identify a common misconception.</p>
<details class="qa-answer" id="q-039-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-039-a-01">Explicitly establish real dependencies instead of treating queuing as a transaction mechanism.</p><div class="qa-sections">
<section class="qa-section" id="q-039-s-01" data-answer-section="1"><h3><span>1.</span> Mechanism and scope</h3>
<span class="qa-anchor" id="q-039-a-02"></span><p>Examples include CQ-before-SQ creation, SQ-before-CQ deletion, successful Set Features before affected new commands, and supported fused pairs.</p>
<span class="qa-anchor" id="q-039-a-04"></span><p>FUSE=01b/10b marks the first/second command. In PCIe they must be adjacent in one SQ and submitted by one Tail update.</p>
</section>
<section class="qa-section" id="q-039-s-02" data-answer-section="2"><h3><span>2.</span> Understand it through actions and results</h3>
<span class="qa-anchor" id="q-039-a-03"></span><p>Check FUSES and individual feature/command rules; no global ordered-mode bit resolves every case.</p>
<span class="qa-anchor" id="q-039-a-05"></span><p>Establish ordinary dependencies by waiting for completion; submit fused pairs under their special rules with separate CQEs. Do not assume the controller orders arbitrary concurrent requests for the host.</p>
<span class="qa-anchor" id="q-039-a-06"></span><p>Commands submitted after successful Set Features use the new value; previously submitted ones may use old or new settings. Drain first when testing a clean transition.</p>
</section>
<section class="qa-section" id="q-039-s-03" data-answer-section="3"><h3><span>3.</span> Avoid a misleading conclusion</h3>
<span class="qa-anchor" id="q-039-a-07"></span><p>A missing adjacent fused partner uses 0/0Ah. Queue dependency errors use Create/Delete-specific statuses, not universally 0/0Ch.</p>
<span class="qa-anchor" id="q-039-a-16"></span><p>Trace completion-to-submission boundaries. FUA controls persistence, not these dependencies.</p>
</section>
</div>
<span class="qa-anchor" id="q-039-a-17"></span><span class="qa-anchor" id="q-039-a-08"></span><span class="qa-anchor" id="q-039-a-09"></span><span class="qa-anchor" id="q-039-a-10"></span><span class="qa-anchor" id="q-039-a-11"></span><span class="qa-anchor" id="q-039-a-12"></span><span class="qa-anchor" id="q-039-a-13"></span><span class="qa-anchor" id="q-039-a-14"></span><span class="qa-anchor" id="q-039-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-order">Base 2.4 §3.4.1–3.4.5</a> · <a href="#ref-create">Base 2.4 §5.3.1–5.3.2</a> · <a href="#ref-delete">Base 2.4 §5.3.3–5.3.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-nvmatomic">NVM Command Set 1.3 §2.1.2–2.1.4</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-040" data-question="40" data-answer-kind="concept"><h2><a class="qa-qid" href="#q-040">Q40</a> How do outstanding limits and CQ Full constrain further command handling?</h2>
<p class="qa-prompt">Explain the mechanism in your own words and identify a common misconception.</p>
<details class="qa-answer" id="q-040-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-040-a-01">Separate host submission capacity, internal execution resources and completion capacity instead of using one queue-depth value to explain every stall.</p><div class="qa-sections">
<section class="qa-section" id="q-040-s-01" data-answer-section="1"><h3><span>1.</span> Mechanism and scope</h3>
<span class="qa-anchor" id="q-040-a-02"></span><p>Limits may affect an SQ, shared CQ or internal resources; not every limit is controller-wide failure.</p>
<span class="qa-anchor" id="q-040-a-04"></span><p>Fetching submitted SQEs uses a vendor-specific algorithm; arbitration selects where candidate processing starts. Fetch and execution start are distinct.</p>
</section>
<section class="qa-section" id="q-040-s-02" data-answer-section="2"><h3><span>2.</span> Understand it through actions and results</h3>
<span class="qa-anchor" id="q-040-a-03"></span><p>The host uses queue size/SQHD and unique CIDs. Do not import another transport&#x27;s MAXCMD flow-control assumptions into PCIe.</p>
<span class="qa-anchor" id="q-040-a-05"></span><p>The host must not overwrite unconsumed SQEs; the controller must not post into a full CQ and may pause related further processing while independent SQs continue.</p>
<span class="qa-anchor" id="q-040-a-06"></span><p>Progress resumes as capacity becomes available. A freed SQ slot can belong to a still-outstanding command because consumption is not completion.</p>
</section>
<section class="qa-section" id="q-040-s-03" data-answer-section="3"><h3><span>3.</span> Avoid a misleading conclusion</h3>
<span class="qa-anchor" id="q-040-a-07"></span><p>Normal resource limits do not automatically require error CQEs; pointer misuse, CID reuse and command-specific limits have separate rules.</p>
<span class="qa-anchor" id="q-040-a-16"></span><p>Use evidence for each stage; submitted count does not establish simultaneous execution of every command.</p>
</section>
</div>
<span class="qa-anchor" id="q-040-a-17"></span><span class="qa-anchor" id="q-040-a-08"></span><span class="qa-anchor" id="q-040-a-09"></span><span class="qa-anchor" id="q-040-a-10"></span><span class="qa-anchor" id="q-040-a-11"></span><span class="qa-anchor" id="q-040-a-12"></span><span class="qa-anchor" id="q-040-a-13"></span><span class="qa-anchor" id="q-040-a-14"></span><span class="qa-anchor" id="q-040-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-queue">Base 2.4 §3.3.1</a> · <a href="#ref-order">Base 2.4 §3.4.1–3.4.5</a> · <a href="#ref-cqe">Base 2.4 §4.2.1, 4.2.3–4.2.4</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-041" data-question="41" data-answer-kind="compare"><h2><a class="qa-qid" href="#q-041">Q41</a> How do Round Robin and Weighted Round Robin arbitration differ?</h2>
<p class="qa-prompt">Identify the key difference and one case where the alternatives are not interchangeable.</p>
<details class="qa-answer" id="q-041-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-041-a-01">Select which SQ starts the next batch when several contain eligible work, allowing host service priorities.</p><div class="qa-sections">
<section class="qa-section" id="q-041-s-01" data-answer-section="1"><h3><span>1.</span> What differs</h3>
<span class="qa-anchor" id="q-041-a-02"></span><p>Arbitration governs candidate processing starts, not completion order or a fixed IOPS ratio.</p>
<span class="qa-anchor" id="q-041-a-04"></span><p>FID 01h provides AB and HPW/MPW/LPW; QPRIO applies in WRR. AB=7 means unlimited burst, otherwise 2^AB; weights encode value+1.</p>
</section>
<section class="qa-section" id="q-041-s-02" data-answer-section="2"><h3><span>2.</span> How to choose and verify</h3>
<span class="qa-anchor" id="q-041-a-03"></span><p>All controllers support Round Robin. Discover optional WRR via CAP.AMS and select it with CC.AMS.</p>
<span class="qa-anchor" id="q-041-a-05"></span><p>Select CC.AMS while disabled, set FID 01h after enabling, create SQ priorities and observe under continuously eligible workloads.</p>
<span class="qa-anchor" id="q-041-a-06"></span><p>RR gives all SQs, including Admin, equal round-robin priority. WRR prioritizes Admin, then Urgent, then weighted High/Medium/Low service with within-class rules.</p>
</section>
<section class="qa-section" id="q-041-s-03" data-answer-section="3"><h3><span>3.</span> Where the comparison stops</h3>
<span class="qa-anchor" id="q-041-a-07"></span><p>Unsupported CC.AMS programming is undefined, not a Set Features Invalid Field completion. Invalid defined FID 01h parameters follow command rules.</p>
<span class="qa-anchor" id="q-041-a-16"></span><p>Get FID 01h verifies configuration only. Service time, media contention and CQ pressure affect throughput, so IOPS ratios alone cannot validate WRR.</p>
</section>
</div>
<span class="qa-anchor" id="q-041-a-17"></span><span class="qa-anchor" id="q-041-a-08"></span><span class="qa-anchor" id="q-041-a-09"></span><span class="qa-anchor" id="q-041-a-10"></span><span class="qa-anchor" id="q-041-a-11"></span><span class="qa-anchor" id="q-041-a-12"></span><span class="qa-anchor" id="q-041-a-13"></span><span class="qa-anchor" id="q-041-a-14"></span><span class="qa-anchor" id="q-041-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-order">Base 2.4 §3.4.1–3.4.5</a> · <a href="#ref-arbit">Base 2.4 §5.2.30.1.1</a> · <a href="#ref-cap">Base 2.4 §3.1.4 (CAP, VS)</a> · <a href="#ref-create">Base 2.4 §5.3.1–5.3.2</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-featureeffects">Base 2.4 §5.2.13.1.18</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-042" data-question="42" data-answer-kind="concept"><h2><a class="qa-qid" href="#q-042">Q42</a> When do Urgent, High, Medium and Low queue priorities take effect?</h2>
<p class="qa-prompt">Explain the mechanism in your own words and identify a common misconception.</p>
<details class="qa-answer" id="q-042-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-042-a-01">Give SQs different service opportunities only under the applicable arbitration mechanism.</p><div class="qa-sections">
<section class="qa-section" id="q-042-s-01" data-answer-section="1"><h3><span>1.</span> Mechanism and scope</h3>
<span class="qa-anchor" id="q-042-a-02"></span><p>QPRIO is an SQ-level setting, not a per-Read/Write priority field.</p>
<span class="qa-anchor" id="q-042-a-04"></span><p>Create SQ CDW11.QPRIO encodes Urgent 00b, High 01b, Medium 10b and Low 11b; FID 01h weights the latter three.</p>
</section>
<section class="qa-section" id="q-042-s-02" data-answer-section="2"><h3><span>2.</span> Understand it through actions and results</h3>
<span class="qa-anchor" id="q-042-a-03"></span><p>QPRIO is used only when WRR is supported and selected through CC.AMS; otherwise it shall be ignored.</p>
<span class="qa-anchor" id="q-042-a-05"></span><p>Create SQs with suitable QPRIO. Change an existing queue through reconstruction, not by editing an old Create SQE in host memory.</p>
<span class="qa-anchor" id="q-042-a-06"></span><p>Urgent outranks weighted service but remains below Admin. Persistent Urgent work may starve lower classes; High has no universal fixed minimum bandwidth.</p>
</section>
<section class="qa-section" id="q-042-s-03" data-answer-section="3"><h3><span>3.</span> Avoid a misleading conclusion</h3>
<span class="qa-anchor" id="q-042-a-07"></span><p>Ignoring QPRIO under RR is correct, not a failed priority feature. Invalid queue parameters still follow Create statuses.</p>
<span class="qa-anchor" id="q-042-a-16"></span><p>Preserve each SQ&#x27;s QPRIO, CC.AMS and FID 01h together; none alone explains priority behavior.</p>
</section>
</div>
<span class="qa-anchor" id="q-042-a-17"></span><span class="qa-anchor" id="q-042-a-08"></span><span class="qa-anchor" id="q-042-a-09"></span><span class="qa-anchor" id="q-042-a-10"></span><span class="qa-anchor" id="q-042-a-11"></span><span class="qa-anchor" id="q-042-a-12"></span><span class="qa-anchor" id="q-042-a-13"></span><span class="qa-anchor" id="q-042-a-14"></span><span class="qa-anchor" id="q-042-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-order">Base 2.4 §3.4.1–3.4.5</a> · <a href="#ref-create">Base 2.4 §5.3.1–5.3.2</a> · <a href="#ref-arbit">Base 2.4 §5.2.30.1.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-featureeffects">Base 2.4 §5.2.13.1.18</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-043" data-question="43" data-answer-kind="diagnose"><h2><a class="qa-qid" href="#q-043">Q43</a> How can arbitration be evaluated when multiple queues compete?</h2>
<p class="qa-prompt">Separate available evidence from missing information before judging conformance.</p>
<details class="qa-answer" id="q-043-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-043-a-01">Translate candidate-selection requirements into evidence rather than equating latency or throughput differences with arbitration violations.</p><div class="qa-sections">
<section class="qa-section" id="q-043-s-01" data-answer-section="1"><h3><span>1.</span> Preserve the evidence first</h3>
<span class="qa-anchor" id="q-043-a-02"></span><p>Observe competing SQs on one controller after excluding CQ Full, dependencies, unequal service costs and insufficient offered work.</p>
<span class="qa-anchor" id="q-043-a-03"></span><p>Record CAP.AMS, CC.AMS, FID 01h AB/weights and each SQ&#x27;s QPRIO.</p>
<span class="qa-anchor" id="q-043-a-04"></span><p>In WRR, processing starts per round are limited by remaining credits and AB. Ready candidates matter, not merely a nonempty SQ.</p>
</section>
<section class="qa-section" id="q-043-s-02" data-answer-section="2"><h3><span>2.</span> Work through the possible causes</h3>
<span class="qa-anchor" id="q-043-a-17"></span><p>First verify continuously eligible high-priority candidates and available CQ space.</p>
<span class="qa-anchor" id="q-043-a-05"></span><p>Use comparable commands, sustained supply and nonblocking CQs. Compare processing-start/scheduler evidence where available; CQEs alone cannot reconstruct all internal choices.</p>
</section>
<section class="qa-section" id="q-043-s-03" data-answer-section="3"><h3><span>3.</span> Decide what the evidence supports</h3>
<span class="qa-anchor" id="q-043-a-06"></span><p>High/Low weights of 4:1 describe service credits, not an exact completion ratio in every short interval.</p>
<span class="qa-anchor" id="q-043-a-07"></span><p>Measurement itself has no error CQE. Verify configuration success and distinguish shall/may requirements; unsuitable workload conditions do not establish noncompliance.</p>
<span class="qa-anchor" id="q-043-a-16"></span><p>A noncompliance claim needs a contradiction between a defined selection rule and evidence, not merely slower high-priority work.</p>
</section>
</div>
<span class="qa-anchor" id="q-043-a-08"></span><span class="qa-anchor" id="q-043-a-09"></span><span class="qa-anchor" id="q-043-a-10"></span><span class="qa-anchor" id="q-043-a-11"></span><span class="qa-anchor" id="q-043-a-12"></span><span class="qa-anchor" id="q-043-a-13"></span><span class="qa-anchor" id="q-043-a-14"></span><span class="qa-anchor" id="q-043-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-order">Base 2.4 §3.4.1–3.4.5</a> · <a href="#ref-arbit">Base 2.4 §5.2.30.1.1</a> · <a href="#ref-create">Base 2.4 §5.3.1–5.3.2</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-featureeffects">Base 2.4 §5.2.13.1.18</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>

<section id="source-index"><h2>Source locations and existing figure guides</h2><p>Base printed page = PDF page−26; the other two use identical numbers. Locations follow the supplied PDF body and retain figure numbers. Shared pages contribute only the relevant definitions, excluding Fabrics and PCIe link/packet content.</p><ul class="qa-references">
<li id="ref-conventions"><strong>Base 2.4 · §1.4.1</strong><br>Printed pages 2–3 · PDF 28–29</li>
<li id="ref-cap"><strong>Base 2.4 · §3.1.4 (CAP, VS)</strong><br>Printed pages 54–59 · PDF 80–85 · Figure 36–37</li>
<li id="ref-nsid"><strong>Base 2.4 · §3.2.1</strong><br>Printed pages 78–81 · PDF 104–107</li>
<li id="ref-queue"><strong>Base 2.4 · §3.3.1</strong><br>Printed pages 88–91 · PDF 114–117 · Figure 73–74</li>
<li id="ref-order"><strong>Base 2.4 · §3.4.1–3.4.5</strong><br>Printed pages 101–105 · PDF 127–131 · Figure 80–81</li>
<li id="ref-reset"><strong>Base 2.4 · §3.7.1–3.7.4</strong><br>Printed pages 120–124 · PDF 146–150</li>
<li id="ref-sqe"><strong>Base 2.4 · §4.1.1</strong><br>Printed pages 139–142 · PDF 165–168 · Figure 92–93</li>
<li id="ref-cqe"><strong>Base 2.4 · §4.2.1, 4.2.3–4.2.4</strong><br>Printed pages 144–157 · PDF 170–183 · Figure 97–105, 109</li>
<li id="ref-status"><strong>Base 2.4 · §4.2.3</strong><br>Printed pages 145–155 · PDF 171–181 · Figure 101–105</li>
<li id="ref-feature"><strong>Base 2.4 · §4.4</strong><br>Printed pages 166–169 · PDF 192–195 · Figure 126–127</li>
<li id="ref-aer"><strong>Base 2.4 · §5.2.2</strong><br>Printed pages 183–190 · PDF 209–216 · Figure 150–156</li>
<li id="ref-error"><strong>Base 2.4 · §5.2.13.1.2</strong><br>Printed pages 218–220 · PDF 244–246 · Figure 212</li>
<li id="ref-pel"><strong>Base 2.4 · §5.2.13.1.14 (header, reset, hardware, Set Feature events)</strong><br>Printed pages 244–256, 258, 262–264 · PDF 270–282, 284, 288–290 · Figure 232–244, 246, 252–253</li>
<li id="ref-featureeffects"><strong>Base 2.4 · §5.2.13.1.18</strong><br>Printed pages 276–278 · PDF 302–304 · Figure 270–271</li>
<li id="ref-idctrl"><strong>Base 2.4 · §5.2.14.2.1</strong><br>Printed pages 340–387 · PDF 366–413 · Figure 338–341</li>
<li id="ref-setfeat"><strong>Base 2.4 · §5.2.30.1 (common fields, scope and persistence)</strong><br>Printed pages 456–460 · PDF 482–486 · Figure 463–466</li>
<li id="ref-arbit"><strong>Base 2.4 · §5.2.30.1.1</strong><br>Printed pages 460 · PDF 486 · Figure 467</li>
<li id="ref-vwc"><strong>Base 2.4 · §5.2.30.1.4</strong><br>Printed pages 464–465 · PDF 490–491 · Figure 471</li>
<li id="ref-behavior"><strong>Base 2.4 · §5.2.30.1.15</strong><br>Printed pages 475–477 · PDF 501–503 · Figure 491</li>
<li id="ref-irqfeat"><strong>Base 2.4 · §5.2.30.2.1–5.2.30.2.2</strong><br>Printed pages 514–515 · PDF 540–541 · Figure 543–544</li>
<li id="ref-create"><strong>Base 2.4 · §5.3.1–5.3.2</strong><br>Printed pages 527–531 · PDF 553–557 · Figure 571–579</li>
<li id="ref-delete"><strong>Base 2.4 · §5.3.3–5.3.4</strong><br>Printed pages 531–532 · PDF 557–558 · Figure 580–583</li>
<li id="ref-fatal"><strong>Base 2.4 · §9.1–9.6.1</strong><br>Printed pages 825–826 · PDF 851–852</li>
<li id="ref-nvmatomic"><strong>NVM Command Set 1.3 · §2.1.2–2.1.4</strong><br>Printed pages 14–20 · PDF 14–20 · Figure 3–9</li>
<li id="ref-pcie"><strong>PCIe Transport 1.4 · §3.1–3.4</strong><br>Printed pages 9–13 · PDF 9–13 · Figure 3–8</li>
<li id="ref-irq"><strong>PCIe Transport 1.4 · §3.5</strong><br>Printed pages 13–16 · PDF 13–16 · Figure 9</li>
</ul><h3>When you need a field guide</h3><p>Existing figure explanations have canonical locations; use these links instead of duplicating the same guide.</p><ul>
<li><a href="/nvme/figure-reference/command/en/#figure-b101">Base 2.4 Figure 101 · Completion Queue Entry: Status Field</a></li>
<li><a href="/nvme/figure-reference/command/en/#figure-b104">Base 2.4 Figure 104 · Status Code – Command Specific Status Values</a></li>
<li><a href="/nvme/figure-reference/identify/en/#figure-b338">Base 2.4 Figure 338 · Identify – Identify Controller Data Structure, I/O Command Set Independent</a></li>
<li><a href="/nvme/figure-reference/init/en/#figure-b36">Base 2.4 Figure 36 · Offset 0h: CAP – Controller Capabilities</a></li>
<li><a href="/nvme/figure-reference/features/en/#figure-b543">Base 2.4 Figure 543 · Interrupt Coalescing – Command Dword 11</a></li>
<li><a href="/nvme/figure-reference/command/en/#figure-b93">Base 2.4 Figure 93 · Common Command Format</a></li>
<li><a href="/nvme/figure-reference/command/en/#figure-b97">Base 2.4 Figure 97 · Common Completion Queue Entry Layout – Admin and All I/O Command Sets</a></li>
</ul><details><summary>Original documents used</summary><ul class="qr-sources">
<li>NVM Express Base Specification · Revision 2.4 · 2026-07-31<br><code>NVM-Express-Base-Specification-Revision-2.4-Ratified-2026.07.31.pdf</code></li>
<li>NVM Express NVM Command Set Specification · Revision 1.3 · 2026-07-31<br><code>NVM-Express-NVM-Command-Set-Specification-Revision-1.3-Ratified-2026.07.31.pdf</code></li>
<li>NVM Express NVMe over PCIe Transport Specification · Revision 1.4 · 2026-07-31<br><code>NVM-Express-NVMe-over-PCIe-Transport-Specification-Revision-1.4-Ratified-2026.07.31.pdf</code></li>
</ul></details></section>
</main>
<nav class="qr-top" aria-label="Bank and editions"><a href="#content">Skip to content</a><a href="/nvme/question-bank/en/">Question index</a><a href="/nvme/question-bank/commands/zh-tw/">繁體中文</a><a href="/DOCS/nvme-question-bank/commands.html">Chinese tutorial HTML</a></nav>
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
