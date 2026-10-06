---
layout: post
title: "NVMe Self-Study Bank: Namespace management, attachment and protection"
date: 2026-10-02 00:00:00 +0800
categories: [nvme]
permalink: /nvme/question-bank/namespace-management/en/
lang: en
nvme_quickref: true
nvme_qa: true
---

<div class="nvme-quickref nvme-qa">
<nav class="qr-top" aria-label="Bank and editions"><a href="#content">Skip to content</a><a href="/nvme/question-bank/en/">Question index</a><a href="/nvme/question-bank/namespace-management/zh-tw/">繁體中文</a><a href="/DOCS/nvme-question-bank/namespace-management.html">Chinese tutorial HTML</a></nav>
<main id="content"><p class="qr-eyebrow">BASE 2.4 / NVM 1.3 / PCIe 1.4 · Q1–328</p>
<header><p class="qa-range">Q157–Q173</p><h1>Namespace management, attachment and protection</h1><p class="qr-intro">Creation, attachment and write protection are separate states connected through a namespace lifecycle.</p><p>Practice first, then reveal the explanation. Each question uses the prose, field interpretation, comparison or flow that suits it. All numerical examples are hypothetical. Status is written SCT/SC; h indicates hexadecimal.</p></header>
<aside class="qa-glossary"><h2>Terms used in this volume</h2><dl><dt>Controller / namespace</dt><dd>A controller receives commands and manages access. A namespace is a logical storage space that commands can address. An NVM subsystem contains controllers and nonvolatile storage resources.</dd><dt>SQ / CQ / SQE / CQE</dt><dd>Submission and Completion Queues carry command entries (SQEs) and completion entries (CQEs). QID identifies a queue, CID distinguishes outstanding commands in one SQ, and NSID identifies a namespace.</dd><dt>Register / Identify / Feature / Log</dt><dd>A register exposes control or state. Identify queries capabilities and attributes; features query or configure operation; log pages report specific state or records. FID, LID, CNS and CSI select features, logs, Identify structures and command sets.</dd><dt>index / offset / zero-based</dt><dd>An index selects an entry, usually starting at 0; an offset measures distance from an origin in specified units. A zero-based count encodes count−1, but not every zero-valued field is a count. A Dword is 4 bytes; a byte is 8 bits.</dd><dt>Scope / reset / retention</dt><dd>Scope names the affected objects; retention means preserving state. Controller Reset (clearing CC.EN) is one form of Controller Level Reset, or CLR. Different CLR triggers can retain different registers.</dd></dl></aside>
<section id="overview" class="qa-overview"><h2>Check existence, access and writability separately</h2><p class="qa-takeaway">Creation does not automatically attach a namespace.</p>
<div class="qr-table" tabindex="0" role="region" aria-label="Horizontally scrollable comparison table"><table><thead><tr><th scope="col">Question</th><th scope="col">Evidence</th><th scope="col">Next step</th></tr></thead><tbody><tr><td>Does it exist?</td><td>Allocated inventory and returned NSID</td><td>Check format/capacity</td></tr><tr><td>Is it attached here?</td><td>Active and attachment lists</td><td>Check readiness/path</td></tr><tr><td>Is writing allowed?</td><td>Capability, control and state</td><td>Apply command restrictions</td></tr></tbody></table></div>
<p><strong>Worked interpretation: </strong>Namespace 2 absent from A’s active list may still exist and be attached to B.</p>
<p class="qa-citations">Sources: <a href="#ref-nsattach">Base 2.4 §5.2.24–5.2.25, 8.1.17–8.1.17.2</a> · <a href="#ref-nvmcreate">NVM Command Set 1.3 §4.1.5.8, 4.1.6, 5.8</a> · <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-nwp">Base 2.4 §5.2.30.1.38, 8.1.18</a></p>
</section>
<div class="qa-controls" hidden><label>Search this page <input type="search" id="qa-search" placeholder="Question number, field or keyword"></label><button type="button" data-expand="true">Expand all answers</button><button type="button" data-expand="false">Collapse all answers</button><output id="qa-count" aria-live="polite"></output></div>
<section id="question-index"><h2>Questions in this volume</h2><ol class="qa-index">
<li><a href="#q-157">Q157 · How are namespace management and attachment supported?</a></li>
<li><a href="#q-158">Q158 · How are size, capacity, format and thin provisioning selected?</a></li>
<li><a href="#q-159">Q159 · How are namespace-creation resource and parameter errors reported?</a></li>
<li><a href="#q-160">Q160 · How does creation change the allocated namespace list?</a></li>
<li><a href="#q-161">Q161 · How are controllers selected for attachment changes?</a></li>
<li><a href="#q-162">Q162 · How are active and controller lists cross-checked?</a></li>
<li><a href="#q-163">Q163 · How are attachment relationship errors reported?</a></li>
<li><a href="#q-164">Q164 · What happens to outstanding commands during detach?</a></li>
<li><a href="#q-165">Q165 · How are commands handled after namespace detach?</a></li>
<li><a href="#q-166">Q166 · How are nonexistent or attached namespace deletions handled?</a></li>
<li><a href="#q-167">Q167 · Which events and logs follow namespace changes?</a></li>
<li><a href="#q-168">Q168 · How does changed-namespace overflow work?</a></li>
<li><a href="#q-169">Q169 · Do namespace configuration and attachment survive resets?</a></li>
<li><a href="#q-170">Q170 · How do private and shared namespaces differ?</a></li>
<li><a href="#q-171">Q171 · How do write-protection modes and entry controls differ?</a></li>
<li><a href="#q-172">Q172 · How does write protection persist across reset and power?</a></li>
<li><a href="#q-173">Q173 · How does protection affect format, sanitize and namespace management?</a></li>
</ol></section>
<article class="qa-question" id="q-157" data-question="157" data-answer-kind="lookup"><h2><a class="qa-qid" href="#q-157">Q157</a> How are namespace management and attachment supported?</h2>
<p class="qa-prompt">Choose the interface and target, then identify the returned field that supports your conclusion.</p>
<details class="qa-answer" id="q-157-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-157-a-01">Management creates/deletes namespaces; attachment controls controller access. The capabilities are related but not equivalent.</p><div class="qa-sections">
<section class="qa-section" id="q-157-s-01" data-answer-section="1"><h3><span>1.</span> Select the target and information</h3>
<span class="qa-anchor" id="q-157-a-02"></span><p>Allocation is subsystem inventory; active access is controller-specific.</p>
<span class="qa-anchor" id="q-157-a-03"></span><p>NMS1 requires both commands; NMS0 can still support attachment alone, discoverable through Command Effects.</p>
<span class="qa-anchor" id="q-157-a-04"></span><p>Opcodes 0Dh and 15h have different SEL action definitions.</p>
</section>
<section class="qa-section" id="q-157-s-02" data-answer-section="2"><h3><span>2.</span> Query sequence and interpretation</h3>
<span class="qa-anchor" id="q-157-a-05"></span><p>Establish command support, enumerate objects and construct the intended operation.</p>
<span class="qa-anchor" id="q-157-a-06"></span><p>NMS entails both command capabilities; attachment-only support does not authorize creation.</p>
</section>
<section class="qa-section" id="q-157-s-03" data-answer-section="3"><h3><span>3.</span> Handle missing or inconsistent evidence</h3>
<span class="qa-anchor" id="q-157-a-07"></span><p>Distinguish unsupported opcode from unsupported Restore Default action, which uses Invalid Field.</p>
<span class="qa-anchor" id="q-157-a-16"></span><p>Cross-check OACS, CSUPP and valid behavior.</p>
<span class="qa-anchor" id="q-157-a-17"></span><p>First check the mistaken implication that NMS0 forbids attachment.</p>
</section>
</div>
<span class="qa-anchor" id="q-157-a-08"></span><span class="qa-anchor" id="q-157-a-09"></span><span class="qa-anchor" id="q-157-a-10"></span><span class="qa-anchor" id="q-157-a-11"></span><span class="qa-anchor" id="q-157-a-12"></span><span class="qa-anchor" id="q-157-a-13"></span><span class="qa-anchor" id="q-157-a-14"></span><span class="qa-anchor" id="q-157-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-commandseffects">Base 2.4 §5.2.13.1.6</a> · <a href="#ref-nsattach">Base 2.4 §5.2.24–5.2.25, 8.1.17–8.1.17.2</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-nspelevent">Base 2.4 §5.2.13.1.14.2.6</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-158" data-question="158" data-answer-kind="fields"><h2><a class="qa-qid" href="#q-158">Q158</a> How are size, capacity, format and thin provisioning selected?</h2>
<p class="qa-prompt">Explain the units and encoding, then work through one set of values.</p>
<details class="qa-answer" id="q-158-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-158-a-01">NSZE defines address range and NCAP allocatable logical blocks, both in the selected format’s units.</p><div class="qa-sections">
<section class="qa-section" id="q-158-s-01" data-answer-section="1"><h3><span>1.</span> Establish the source and scope</h3>
<span class="qa-anchor" id="q-158-a-02"></span><p>Creation consumes selected resources without attaching the new namespace.</p>
<span class="qa-anchor" id="q-158-a-03"></span><p>Inspect common capabilities, format list, thin provisioning, unallocated capacity and reported granularity.</p>
</section>
<section class="qa-section" id="q-158-s-02" data-answer-section="2"><h3><span>2.</span> Fields, units and worked interpretation</h3>
<span class="qa-anchor" id="q-158-a-04"></span><p>Set NSZE/NCAP/FLBAS/DPS/NMIC and resource IDs. NCAP cannot exceed NSZE; smaller capacity requires thin-provisioning support.</p>
<span class="qa-anchor" id="q-158-a-05"></span><p>Select format before conversion:1000×4 KiB=4000 KiB user capacity, while physical allocation can be larger.</p>
<span class="qa-anchor" id="q-158-a-06"></span><p>Successful creation returns NSID in DW0 and formats the namespace; verify before attachment.</p>
</section>
<section class="qa-section" id="q-158-s-03" data-answer-section="3"><h3><span>3.</span> Conditions that change the interpretation</h3>
<span class="qa-anchor" id="q-158-a-07"></span><p>Invalid format, unsupported thin provisioning, capacity shortage and ID exhaustion are distinct.</p>
<span class="qa-anchor" id="q-158-a-16"></span><p>Compare requested block counts/format with NSZE/NCAP/NVMCAP using their distinct units.</p>
</section>
</div>
<span class="qa-anchor" id="q-158-a-17"></span><span class="qa-anchor" id="q-158-a-08"></span><span class="qa-anchor" id="q-158-a-09"></span><span class="qa-anchor" id="q-158-a-10"></span><span class="qa-anchor" id="q-158-a-11"></span><span class="qa-anchor" id="q-158-a-12"></span><span class="qa-anchor" id="q-158-a-13"></span><span class="qa-anchor" id="q-158-a-14"></span><span class="qa-anchor" id="q-158-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-nvmcreate">NVM Command Set 1.3 §4.1.5.8, 4.1.6, 5.8</a> · <a href="#ref-idns">NVM Command Set 1.3 §4.1.5.1–4.1.5.4</a> · <a href="#ref-nsattach">Base 2.4 §5.2.24–5.2.25, 8.1.17–8.1.17.2</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-nspelevent">Base 2.4 §5.2.13.1.14.2.6</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-159" data-question="159" data-answer-kind="error"><h2><a class="qa-qid" href="#q-159">Q159</a> How are namespace-creation resource and parameter errors reported?</h2>
<p class="qa-prompt">Distinguish failure conditions before deciding whether a particular response is required.</p>
<details class="qa-answer" id="q-159-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-159-a-01">Distinguish capacity, identifier count, format and resource mapping before choosing a remedy.</p><div class="qa-sections">
<section class="qa-section" id="q-159-s-01" data-answer-section="1"><h3><span>1.</span> Distinguish the failure conditions</h3>
<span class="qa-anchor" id="q-159-a-02"></span><p>Capacity is evaluated in the selected resource pool, not unrelated groups.</p>
<span class="qa-anchor" id="q-159-a-04"></span><p>Distinct codes are capacity 1/15h, identifier 1/16h, format 1/0Ah and thin provisioning 1/1Bh.</p>
<span class="qa-anchor" id="q-159-a-07"></span><p>Missing preferred granularity can waste allocation but must not alone reject an otherwise valid create.</p>
</section>
<section class="qa-section" id="q-159-s-02" data-answer-section="2"><h3><span>2.</span> Establish the cause from evidence</h3>
<span class="qa-anchor" id="q-159-a-03"></span><p>Inspect capacity, applicable namespace limits, formats/granularity and resource lists.</p>
<span class="qa-anchor" id="q-159-a-05"></span><p>Isolate parameters; for insufficient capacity inspect CSINFO’s required unallocated bytes.</p>
</section>
<section class="qa-section" id="q-159-s-03" data-answer-section="3"><h3><span>3.</span> Outcome and follow-up checks</h3>
<span class="qa-anchor" id="q-159-a-06"></span><p>Only successful Create DW0 contains the created NSID.</p>
<span class="qa-anchor" id="q-159-a-16"></span><p>Distinguish invalid format from insufficient allocation using consistent quantities.</p>
<span class="qa-anchor" id="q-159-a-17"></span><p>First decode SCT/SC before choosing the resource to inspect.</p>
</section>
</div>
<span class="qa-anchor" id="q-159-a-08"></span><span class="qa-anchor" id="q-159-a-09"></span><span class="qa-anchor" id="q-159-a-10"></span><span class="qa-anchor" id="q-159-a-11"></span><span class="qa-anchor" id="q-159-a-12"></span><span class="qa-anchor" id="q-159-a-13"></span><span class="qa-anchor" id="q-159-a-14"></span><span class="qa-anchor" id="q-159-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-nvmcreate">NVM Command Set 1.3 §4.1.5.8, 4.1.6, 5.8</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-nsattach">Base 2.4 §5.2.24–5.2.25, 8.1.17–8.1.17.2</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-nspelevent">Base 2.4 §5.2.13.1.14.2.6</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-160" data-question="160" data-answer-kind="process"><h2><a class="qa-qid" href="#q-160">Q160</a> How does creation change the allocated namespace list?</h2>
<p class="qa-prompt">Order the actions and identify which completion must precede the next action.</p>
<details class="qa-answer" id="q-160-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-160-a-01">Allocated means existence; active means access through a controller. Creation establishes allocation first.</p><div class="qa-sections">
<section class="qa-section" id="q-160-s-01" data-answer-section="1"><h3><span>1.</span> Prepare the operation</h3>
<span class="qa-anchor" id="q-160-a-02"></span><p>Allocated inventory and controller-specific active lists are distinct.</p>
<span class="qa-anchor" id="q-160-a-03"></span><p>Query CNS 10h and the new namespace; CNS 02h verifies later attachment.</p>
<span class="qa-anchor" id="q-160-a-04"></span><p>Create returns a controller-selected ID, not a guaranteed host-predicted sequence.</p>
</section>
<section class="qa-section" id="q-160-s-02" data-answer-section="2"><h3><span>2.</span> Sequence and completion conditions</h3>
<span class="qa-anchor" id="q-160-a-05"></span><p>Snapshot inventory, await success and enumerate again to identify the new object.</p>
<span class="qa-anchor" id="q-160-a-06"></span><p>The new ID is allocated but creation does not automatically attach it.</p>
</section>
<section class="qa-section" id="q-160-s-03" data-answer-section="3"><h3><span>3.</span> Handle unmet conditions</h3>
<span class="qa-anchor" id="q-160-a-07"></span><p>Continue enumeration when lists are longer than one response.</p>
<span class="qa-anchor" id="q-160-a-16"></span><p>Correlate returned ID, inventory and attributes rather than count alone.</p>
</section>
</div>
<span class="qa-anchor" id="q-160-a-17"></span><span class="qa-anchor" id="q-160-a-08"></span><span class="qa-anchor" id="q-160-a-09"></span><span class="qa-anchor" id="q-160-a-10"></span><span class="qa-anchor" id="q-160-a-11"></span><span class="qa-anchor" id="q-160-a-12"></span><span class="qa-anchor" id="q-160-a-13"></span><span class="qa-anchor" id="q-160-a-14"></span><span class="qa-anchor" id="q-160-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-nsid">Base 2.4 §3.2.1</a> · <a href="#ref-nsattach">Base 2.4 §5.2.24–5.2.25, 8.1.17–8.1.17.2</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-nspelevent">Base 2.4 §5.2.13.1.14.2.6</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-161" data-question="161" data-answer-kind="process"><h2><a class="qa-qid" href="#q-161">Q161</a> How are controllers selected for attachment changes?</h2>
<p class="qa-prompt">Order the actions and identify which completion must precede the next action.</p>
<details class="qa-answer" id="q-161-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-161-a-01">Attachment changes access relationships without creating/deleting or reformatting the namespace.</p><div class="qa-sections">
<section class="qa-section" id="q-161-s-01" data-answer-section="1"><h3><span>1.</span> Prepare the operation</h3>
<span class="qa-anchor" id="q-161-a-02"></span><p>NSID selects the namespace and the payload Controller List selects controllers.</p>
<span class="qa-anchor" id="q-161-a-03"></span><p>Check allocation, sharing, controller IDs, command-set support and attachment limits.</p>
<span class="qa-anchor" id="q-161-a-04"></span><p>SEL 0 attaches and 1 detaches using a 4096-byte list of controller IDs, not namespace IDs.</p>
</section>
<section class="qa-section" id="q-161-s-02" data-answer-section="2"><h3><span>2.</span> Sequence and completion conditions</h3>
<span class="qa-anchor" id="q-161-a-05"></span><p>Submit a valid list and verify each targeted controller and namespace relationship afterward.</p>
<span class="qa-anchor" id="q-161-a-06"></span><p>Successful attachment change preserves namespace allocation.</p>
</section>
<section class="qa-section" id="q-161-s-03" data-answer-section="3"><h3><span>3.</span> Handle unmet conditions</h3>
<span class="qa-anchor" id="q-161-a-07"></span><p>Invalid/admin-controller list entries and unsupported/disabled command sets have separate statuses.</p>
<span class="qa-anchor" id="q-161-a-16"></span><p>CSINFO identifies the first failing entry offset; processing stops there, without a universal all-or-nothing rollback guarantee.</p>
</section>
</div>
<span class="qa-anchor" id="q-161-a-17"></span><span class="qa-anchor" id="q-161-a-08"></span><span class="qa-anchor" id="q-161-a-09"></span><span class="qa-anchor" id="q-161-a-10"></span><span class="qa-anchor" id="q-161-a-11"></span><span class="qa-anchor" id="q-161-a-12"></span><span class="qa-anchor" id="q-161-a-13"></span><span class="qa-anchor" id="q-161-a-14"></span><span class="qa-anchor" id="q-161-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-nsattach">Base 2.4 §5.2.24–5.2.25, 8.1.17–8.1.17.2</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-nspelevent">Base 2.4 §5.2.13.1.14.2.6</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-162" data-question="162" data-answer-kind="process"><h2><a class="qa-qid" href="#q-162">Q162</a> How are active and controller lists cross-checked?</h2>
<p class="qa-prompt">Order the actions and identify which completion must precede the next action.</p>
<details class="qa-answer" id="q-162-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-162-a-01">View the relationship from both controller and namespace to detect one-sided updates.</p><div class="qa-sections">
<section class="qa-section" id="q-162-s-01" data-answer-section="1"><h3><span>1.</span> Prepare the operation</h3>
<span class="qa-anchor" id="q-162-a-02"></span><p>An active list belongs to one controller, not the full subsystem.</p>
<span class="qa-anchor" id="q-162-a-03"></span><p>Use applicable active/controller-list queries such as CNS 02h/12h with verified identity.</p>
<span class="qa-anchor" id="q-162-a-04"></span><p>Preserve IDs and pagination markers to avoid missing the target.</p>
</section>
<section class="qa-section" id="q-162-s-02" data-answer-section="2"><h3><span>2.</span> Sequence and completion conditions</h3>
<span class="qa-anchor" id="q-162-a-05"></span><p>Successful attach appears in both views; detach removes it from both.</p>
<span class="qa-anchor" id="q-162-a-06"></span><p>If namespace 7 attaches toA thenB, B’s active list contains 7 and the namespace’s controller list containsA/B.</p>
</section>
<section class="qa-section" id="q-162-s-03" data-answer-section="3"><h3><span>3.</span> Handle unmet conditions</h3>
<span class="qa-anchor" id="q-162-a-07"></span><p>Concurrent management can make snapshots temporally inconsistent; stabilize before diagnosing contradiction.</p>
<span class="qa-anchor" id="q-162-a-16"></span><p>Allocation persists across attachment-only changes.</p>
</section>
</div>
<span class="qa-anchor" id="q-162-a-17"></span><span class="qa-anchor" id="q-162-a-08"></span><span class="qa-anchor" id="q-162-a-09"></span><span class="qa-anchor" id="q-162-a-10"></span><span class="qa-anchor" id="q-162-a-11"></span><span class="qa-anchor" id="q-162-a-12"></span><span class="qa-anchor" id="q-162-a-13"></span><span class="qa-anchor" id="q-162-a-14"></span><span class="qa-anchor" id="q-162-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-nsattach">Base 2.4 §5.2.24–5.2.25, 8.1.17–8.1.17.2</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-nspelevent">Base 2.4 §5.2.13.1.14.2.6</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-163" data-question="163" data-answer-kind="error"><h2><a class="qa-qid" href="#q-163">Q163</a> How are attachment relationship errors reported?</h2>
<p class="qa-prompt">Distinguish failure conditions before deciding whether a particular response is required.</p>
<details class="qa-answer" id="q-163-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-163-a-01">Relationship/list errors do not imply namespace-data damage.</p><div class="qa-sections">
<section class="qa-section" id="q-163-s-01" data-answer-section="1"><h3><span>1.</span> Distinguish the failure conditions</h3>
<span class="qa-anchor" id="q-163-a-02"></span><p>Evaluate each list entry against its state; earlier entries may have been processed before failure.</p>
<span class="qa-anchor" id="q-163-a-04"></span><p>Codes distinguish already-attached 1/18h, private 1/19h, not-attached 1/1Ah and invalid-list 1/1Ch.</p>
<span class="qa-anchor" id="q-163-a-07"></span><p>A second attachment of an already attached private namespace is rejected for privacy, not capacity.</p>
</section>
<section class="qa-section" id="q-163-s-02" data-answer-section="2"><h3><span>2.</span> Establish the cause from evidence</h3>
<span class="qa-anchor" id="q-163-a-03"></span><p>Inspect current attachment, sharing and target capabilities.</p>
<span class="qa-anchor" id="q-163-a-05"></span><p>Isolate the error and reread affected relationships and first-failure position.</p>
</section>
<section class="qa-section" id="q-163-s-03" data-answer-section="3"><h3><span>3.</span> Outcome and follow-up checks</h3>
<span class="qa-anchor" id="q-163-a-06"></span><p>Valid operations change relationships; errors stop processing further list entries.</p>
<span class="qa-anchor" id="q-163-a-16"></span><p>Correlate status/offset and pre/post lists instead of assuming global rollback.</p>
<span class="qa-anchor" id="q-163-a-17"></span><p>First check sharing mode and existing attachment.</p>
</section>
</div>
<span class="qa-anchor" id="q-163-a-08"></span><span class="qa-anchor" id="q-163-a-09"></span><span class="qa-anchor" id="q-163-a-10"></span><span class="qa-anchor" id="q-163-a-11"></span><span class="qa-anchor" id="q-163-a-12"></span><span class="qa-anchor" id="q-163-a-13"></span><span class="qa-anchor" id="q-163-a-14"></span><span class="qa-anchor" id="q-163-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-nsattach">Base 2.4 §5.2.24–5.2.25, 8.1.17–8.1.17.2</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-nspelevent">Base 2.4 §5.2.13.1.14.2.6</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-164" data-question="164" data-answer-kind="concept"><h2><a class="qa-qid" href="#q-164">Q164</a> What happens to outstanding commands during detach?</h2>
<p class="qa-prompt">Explain the mechanism in your own words and identify a common misconception.</p>
<details class="qa-answer" id="q-164-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-164-a-01">Detach invalidates controller access; quiescing first helps hosts, but outstanding-command behavior remains specified.</p><div class="qa-sections">
<section class="qa-section" id="q-164-s-01" data-answer-section="1"><h3><span>1.</span> Mechanism and scope</h3>
<span class="qa-anchor" id="q-164-a-02"></span><p>Only specified relationships change; other attached controllers remain attached.</p>
<span class="qa-anchor" id="q-164-a-04"></span><p>Base 8.1.17 applies inactive-NSID rules to outstanding and later commands, subject to command exceptions.</p>
</section>
<section class="qa-section" id="q-164-s-02" data-answer-section="2"><h3><span>2.</span> Understand it through actions and results</h3>
<span class="qa-anchor" id="q-164-a-03"></span><p>Preserve outstanding IDs, namespace and detach completion timing.</p>
<span class="qa-anchor" id="q-164-a-05"></span><p>Quiesce, synchronize and drain where possible before detach; race tests must retain precise ordering.</p>
<span class="qa-anchor" id="q-164-a-06"></span><p>Detach removes the relationship without duplicate completions; outstanding work follows inactive rules.</p>
</section>
<section class="qa-section" id="q-164-s-03" data-answer-section="3"><h3><span>3.</span> Avoid a misleading conclusion</h3>
<span class="qa-anchor" id="q-164-a-07"></span><p>Generic inactive handling uses Invalid Field, with explicit command exceptions.</p>
<span class="qa-anchor" id="q-164-a-16"></span><p>Check timing classification and premature buffer reclamation.</p>
</section>
</div>
<span class="qa-anchor" id="q-164-a-17"></span><span class="qa-anchor" id="q-164-a-08"></span><span class="qa-anchor" id="q-164-a-09"></span><span class="qa-anchor" id="q-164-a-10"></span><span class="qa-anchor" id="q-164-a-11"></span><span class="qa-anchor" id="q-164-a-12"></span><span class="qa-anchor" id="q-164-a-13"></span><span class="qa-anchor" id="q-164-a-14"></span><span class="qa-anchor" id="q-164-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-sqe">Base 2.4 §4.1.1</a> · <a href="#ref-nsid">Base 2.4 §3.2.1</a> · <a href="#ref-nsattach">Base 2.4 §5.2.24–5.2.25, 8.1.17–8.1.17.2</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-nspelevent">Base 2.4 §5.2.13.1.14.2.6</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-165" data-question="165" data-answer-kind="error"><h2><a class="qa-qid" href="#q-165">Q165</a> How are commands handled after namespace detach?</h2>
<p class="qa-prompt">Distinguish failure conditions before deciding whether a particular response is required.</p>
<details class="qa-answer" id="q-165-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-165-a-01">Detach makes an ID inactive on that controller without deleting it from the subsystem.</p><div class="qa-sections">
<section class="qa-section" id="q-165-s-01" data-answer-section="1"><h3><span>1.</span> Distinguish the failure conditions</h3>
<span class="qa-anchor" id="q-165-a-02"></span><p>The same namespace can remain active through another controller.</p>
<span class="qa-anchor" id="q-165-a-04"></span><p>Figure 93 uses Invalid Field for inactive IDs by default; Identify and other management selectors have their own rules.</p>
<span class="qa-anchor" id="q-165-a-07"></span><p>Successful allocated-object Identify does not disprove detach; inactive and invalid IDs differ.</p>
</section>
<section class="qa-section" id="q-165-s-02" data-answer-section="2"><h3><span>2.</span> Establish the cause from evidence</h3>
<span class="qa-anchor" id="q-165-a-03"></span><p>Inspect controller-active, allocated and namespace-controller lists.</p>
<span class="qa-anchor" id="q-165-a-05"></span><p>After completion, compare the detached and still-attached paths with other conditions fixed.</p>
</section>
<section class="qa-section" id="q-165-s-03" data-answer-section="3"><h3><span>3.</span> Outcome and follow-up checks</h3>
<span class="qa-anchor" id="q-165-a-06"></span><p>Allocation does not authorize normal active data access, while allocated-object management queries can remain valid.</p>
<span class="qa-anchor" id="q-165-a-16"></span><p>Apply the specific opcode/CNS rule, not NSID alone.</p>
<span class="qa-anchor" id="q-165-a-17"></span><p>First distinguish ordinary I/O from permitted inactive-object queries.</p>
</section>
</div>
<span class="qa-anchor" id="q-165-a-08"></span><span class="qa-anchor" id="q-165-a-09"></span><span class="qa-anchor" id="q-165-a-10"></span><span class="qa-anchor" id="q-165-a-11"></span><span class="qa-anchor" id="q-165-a-12"></span><span class="qa-anchor" id="q-165-a-13"></span><span class="qa-anchor" id="q-165-a-14"></span><span class="qa-anchor" id="q-165-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-sqe">Base 2.4 §4.1.1</a> · <a href="#ref-nsid">Base 2.4 §3.2.1</a> · <a href="#ref-nsattach">Base 2.4 §5.2.24–5.2.25, 8.1.17–8.1.17.2</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-nspelevent">Base 2.4 §5.2.13.1.14.2.6</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-166" data-question="166" data-answer-kind="error"><h2><a class="qa-qid" href="#q-166">Q166</a> How are nonexistent or attached namespace deletions handled?</h2>
<p class="qa-prompt">Distinguish failure conditions before deciding whether a particular response is required.</p>
<details class="qa-answer" id="q-166-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-166-a-01">Correct the premise that attached namespaces cannot be deleted: prior detach is recommended, and deletion itself removes all attachments.</p><div class="qa-sections">
<section class="qa-section" id="q-166-s-01" data-answer-section="1"><h3><span>1.</span> Distinguish the failure conditions</h3>
<span class="qa-anchor" id="q-166-a-02"></span><p>Deletion removes the object, not merely one access path.</p>
<span class="qa-anchor" id="q-166-a-04"></span><p>SEL 1 deletes; NSID selects an existing namespace andFFFFFFFFh all. Delete-all with no valid namespaces succeeds.</p>
<span class="qa-anchor" id="q-166-a-07"></span><p>Specific nonexistent targets follow NSID/command errors, unlike empty delete-all; protection/sanitization impose additional restrictions.</p>
</section>
<section class="qa-section" id="q-166-s-02" data-answer-section="2"><h3><span>2.</span> Establish the cause from evidence</h3>
<span class="qa-anchor" id="q-166-a-03"></span><p>Check allocation, protection, background work and scope before individual/all deletion.</p>
<span class="qa-anchor" id="q-166-a-05"></span><p>Quiesce, preferably detach all accessors, delete and refresh inventory/active lists.</p>
</section>
<section class="qa-section" id="q-166-s-03" data-answer-section="3"><h3><span>3.</span> Outcome and follow-up checks</h3>
<span class="qa-anchor" id="q-166-a-06"></span><p>Success removes object and attachment; the numeric NSID may later be reused.</p>
<span class="qa-anchor" id="q-166-a-16"></span><p>Verify actual inventory removal rather than only detachment.</p>
<span class="qa-anchor" id="q-166-a-17"></span><p>First inspect broadcast NSID before judging empty-inventory behavior.</p>
</section>
</div>
<span class="qa-anchor" id="q-166-a-08"></span><span class="qa-anchor" id="q-166-a-09"></span><span class="qa-anchor" id="q-166-a-10"></span><span class="qa-anchor" id="q-166-a-11"></span><span class="qa-anchor" id="q-166-a-12"></span><span class="qa-anchor" id="q-166-a-13"></span><span class="qa-anchor" id="q-166-a-14"></span><span class="qa-anchor" id="q-166-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-sqe">Base 2.4 §4.1.1</a> · <a href="#ref-nsid">Base 2.4 §3.2.1</a> · <a href="#ref-nwp">Base 2.4 §5.2.30.1.38, 8.1.18</a> · <a href="#ref-nsattach">Base 2.4 §5.2.24–5.2.25, 8.1.17–8.1.17.2</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-nspelevent">Base 2.4 §5.2.13.1.14.2.6</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-167" data-question="167" data-answer-kind="events"><h2><a class="qa-qid" href="#q-167">Q167</a> Which events and logs follow namespace changes?</h2>
<p class="qa-prompt">Establish the event condition, then distinguish notification, acknowledgment and recording.</p>
<details class="qa-answer" id="q-167-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-167-a-01">Notifications invalidate host caches, changed lists identify changes and Identify describes current configuration.</p><div class="qa-sections">
<section class="qa-section" id="q-167-s-01" data-answer-section="1"><h3><span>1.</span> When the event exists and who observes it</h3>
<span class="qa-anchor" id="q-167-a-02"></span><p>Create/delete change inventory; attach/detach change controller-active membership.</p>
<span class="qa-anchor" id="q-167-a-03"></span><p>Check attached/allocated notice support, enablement and available requests.</p>
<span class="qa-anchor" id="q-167-a-04"></span><p>LID 04h/1Ch identify attached/allocated changes; Identify and defined PEL management events serve different purposes.</p>
</section>
<section class="qa-section" id="q-167-s-02" data-answer-section="2"><h3><span>2.</span> Notification, reading and acknowledgment</h3>
<span class="qa-anchor" id="q-167-a-05"></span><p>Process affected-controller notices, preserve lists and refresh Identify after management completion.</p>
<span class="qa-anchor" id="q-167-a-06"></span><p>The Admin Delete recipient omits its own deletion notice while other eligible controllers report; equal counts are not required.</p>
</section>
<section class="qa-section" id="q-167-s-03" data-answer-section="3"><h3><span>3.</span> Evaluate missing notifications or records</h3>
<span class="qa-anchor" id="q-167-a-07"></span><p>Disabled/masked/acknowledged events change observable AERs; command success alone does not prove a missing event defect.</p>
<span class="qa-anchor" id="q-167-a-16"></span><p>Correlate origin, affected lists and per-controller AEC on a timeline.</p>
<span class="qa-anchor" id="q-167-a-17"></span><p>First check whether the observer is the Admin Delete recipient.</p>
</section>
<section class="qa-section" id="q-167-s-04" data-answer-section="4"><h3><span>4.</span> Check notifications and log records separately</h3>
<span class="qa-anchor" id="q-167-a-09"></span><p>Create/delete affect allocated inventory; attach/detach affect controller active lists. <a class="qa-rule-link" href="#common-namespace_op-9">Read the complete conditions in this volume</a></p>
<span class="qa-anchor" id="q-167-a-10"></span><p>Identify lists establish current allocation/attachment; changed lists 04h/1Ch identify changes rather than complete state. <a class="qa-rule-link" href="#common-namespace_op-10">Read the complete conditions in this volume</a></p>
<span class="qa-anchor" id="q-167-a-11"></span><p>Supported Change Namespace 06h records defined management changes; do not treat attachment as creation/deletion. <a class="qa-rule-link" href="#common-namespace_op-11">Read the complete conditions in this volume</a></p>
</section>
</div>
<span class="qa-anchor" id="q-167-a-08"></span><span class="qa-anchor" id="q-167-a-12"></span><span class="qa-anchor" id="q-167-a-13"></span><span class="qa-anchor" id="q-167-a-14"></span><span class="qa-anchor" id="q-167-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-aerfull">Base 2.4 §5.2.2 (PCIe-applicable events)</a> · <a href="#ref-aec">Base 2.4 §5.2.30.1.6</a> · <a href="#ref-changedlog">Base 2.4 §5.2.13.1.5</a> · <a href="#ref-nspelevent">Base 2.4 §5.2.13.1.14.2.6</a> · <a href="#ref-nsattach">Base 2.4 §5.2.24–5.2.25, 8.1.17–8.1.17.2</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-168" data-question="168" data-answer-kind="fields"><h2><a class="qa-qid" href="#q-168">Q168</a> How does changed-namespace overflow work?</h2>
<p class="qa-prompt">Explain the units and encoding, then work through one set of values.</p>
<details class="qa-answer" id="q-168-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-168-a-01">Overflow requests a full relevant rescan instead of trusting an incomplete list.</p><div class="qa-sections">
<section class="qa-section" id="q-168-s-01" data-answer-section="1"><h3><span>1.</span> Establish the source and scope</h3>
<span class="qa-anchor" id="q-168-a-02"></span><p>LID 04h concerns attached changes for that controller, not universal subsystem history.</p>
<span class="qa-anchor" id="q-168-a-03"></span><p>Apply the fixed 1024-entry layout and read/clear rules.</p>
</section>
<section class="qa-section" id="q-168-s-02" data-answer-section="2"><h3><span>2.</span> Fields, units and worked interpretation</h3>
<span class="qa-anchor" id="q-168-a-04"></span><p>More than 1024 changed namespaces yieldsFFFFFFFFh first and zeros in remaining entries.</p>
<span class="qa-anchor" id="q-168-a-05"></span><p>Detect the marker, enumerate and refresh properties rather than treating it as an object ID.</p>
<span class="qa-anchor" id="q-168-a-06"></span><p>Full rescan restores current state; repeated 04h reads are not historical pagination.</p>
</section>
<section class="qa-section" id="q-168-s-03" data-answer-section="3"><h3><span>3.</span> Conditions that change the interpretation</h3>
<span class="qa-anchor" id="q-168-a-07"></span><p>A short transfer is distinct from log overflow.</p>
<span class="qa-anchor" id="q-168-a-16"></span><p>Validate rescan cache against current Identify state.</p>
</section>
</div>
<span class="qa-anchor" id="q-168-a-17"></span><span class="qa-anchor" id="q-168-a-08"></span><span class="qa-anchor" id="q-168-a-09"></span><span class="qa-anchor" id="q-168-a-10"></span><span class="qa-anchor" id="q-168-a-11"></span><span class="qa-anchor" id="q-168-a-12"></span><span class="qa-anchor" id="q-168-a-13"></span><span class="qa-anchor" id="q-168-a-14"></span><span class="qa-anchor" id="q-168-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-changedlog">Base 2.4 §5.2.13.1.5</a> · <a href="#ref-getlog">Base 2.4 §5.2.13–5.2.13.1.1</a> · <a href="#ref-nsattach">Base 2.4 §5.2.24–5.2.25, 8.1.17–8.1.17.2</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-nspelevent">Base 2.4 §5.2.13.1.14.2.6</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-169" data-question="169" data-answer-kind="lifecycle"><h2><a class="qa-qid" href="#q-169">Q169</a> Do namespace configuration and attachment survive resets?</h2>
<p class="qa-prompt">Name the reset or interruption, then assess settings, ongoing operations and data separately.</p>
<details class="qa-answer" id="q-169-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-169-a-01">Namespaces are persistent configuration, separate from recreated queues.</p><div class="qa-sections">
<section class="qa-section" id="q-169-s-01" data-answer-section="1"><h3><span>1.</span> Identify the trigger and affected objects</h3>
<span class="qa-anchor" id="q-169-a-02"></span><p>Completed configuration persists; interrupted commands require state discovery.</p>
<span class="qa-anchor" id="q-169-a-03"></span><p>Preserve global identity, NSID, format and attachment for comparison.</p>
</section>
<section class="qa-section" id="q-169-s-02" data-answer-section="2"><h3><span>2.</span> State changes and recovery</h3>
<span class="qa-anchor" id="q-169-a-04"></span><p>Resets/power cycle are not the explicit Restore Default Namespace Configuration operation.</p>
<span class="qa-anchor" id="q-169-a-05"></span><p>Recover Admin access, enumerate existing namespaces/attachments, then build queues rather than recreating objects.</p>
<span class="qa-anchor" id="q-169-a-06"></span><p>Existing configuration becomes accessible again; secondary-controller Offline does not erase attachment.</p>
</section>
<section class="qa-section" id="q-169-s-03" data-answer-section="3"><h3><span>3.</span> Checks across reset or power loss</h3>
<span class="qa-anchor" id="q-169-a-12"></span>
<span class="qa-anchor" id="q-169-a-13"></span>
<span class="qa-anchor" id="q-169-a-14"></span>
<div class="qr-table" tabindex="0" role="region" aria-label="Horizontally scrollable comparison table"><table><thead><tr><th scope="col">Trigger</th><th scope="col">Effect on this operation or state</th></tr></thead><tbody><tr><td>What survives or continues after Controller Reset?</td><td>Completed configuration/attachment survives reset; command channels reset without deleting namespaces. For interrupted commands, inspect lists rather than assuming rollback.</td></tr><tr><td>What survives or continues after NVM Subsystem Reset?</td><td>Subsystem reset is not Restore Default Namespace Configuration. Rediscover persisted namespaces/attachments and rebuild queues, accounting for domain scope.</td></tr><tr><td>What survives or continues after a power cycle?</td><td>Completed namespace configuration/attachments persist. Ordinary/permanent write protection persist; until-power-cycle protection clears on a real power cycle, not all configuration.</td></tr></tbody></table></div>
</section>
<section class="qa-section" id="q-169-s-04" data-answer-section="4"><h3><span>4.</span> Verify retention and recovery</h3>
<span class="qa-anchor" id="q-169-a-07"></span><p>Post-reset lists may reflect an operation whose CQE was lost; absence of completion does not prove non-execution.</p>
<span class="qa-anchor" id="q-169-a-16"></span><p>Match persistent identity/properties to avoid NSID-reuse mistakes.</p>
<span class="qa-anchor" id="q-169-a-17"></span><p>First check whether host recovery itself restored defaults or deleted objects.</p>
</section>
</div>
<span class="qa-anchor" id="q-169-a-08"></span><span class="qa-anchor" id="q-169-a-09"></span><span class="qa-anchor" id="q-169-a-10"></span><span class="qa-anchor" id="q-169-a-11"></span><span class="qa-anchor" id="q-169-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-nsid">Base 2.4 §3.2.1</a> · <a href="#ref-nsattach">Base 2.4 §5.2.24–5.2.25, 8.1.17–8.1.17.2</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-nspelevent">Base 2.4 §5.2.13.1.14.2.6</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-170" data-question="170" data-answer-kind="compare"><h2><a class="qa-qid" href="#q-170">Q170</a> How do private and shared namespaces differ?</h2>
<p class="qa-prompt">Identify the key difference and one case where the alternatives are not interchangeable.</p>
<details class="qa-answer" id="q-170-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-170-a-01">Private limits attachment to one controller; shared allows multiple. These describe access topology, not encryption or access permissions.</p><div class="qa-sections">
<section class="qa-section" id="q-170-s-01" data-answer-section="1"><h3><span>1.</span> What differs</h3>
<span class="qa-anchor" id="q-170-a-02"></span><p>Multiple paths can address one data object, not separate copies.</p>
<span class="qa-anchor" id="q-170-a-04"></span><p>NMIC is selected at creation; attachment changes relationships within supported limits.</p>
</section>
<section class="qa-section" id="q-170-s-02" data-answer-section="2"><h3><span>2.</span> How to choose and verify</h3>
<span class="qa-anchor" id="q-170-a-03"></span><p>Inspect NMIC and actual attachments.</p>
<span class="qa-anchor" id="q-170-a-05"></span><p>Configure sharing, attach controllers and verify each active list.</p>
<span class="qa-anchor" id="q-170-a-06"></span><p>Shared permits multiple accessors; private can move fromA toB through detachment but not attach to both simultaneously.</p>
</section>
<section class="qa-section" id="q-170-s-03" data-answer-section="3"><h3><span>3.</span> Where the comparison stops</h3>
<span class="qa-anchor" id="q-170-a-07"></span><p>Additional attachment of an already attached private namespace uses Namespace Is Private.</p>
<span class="qa-anchor" id="q-170-a-16"></span><p>Compare identity/data/attachments rather than counting paths as additional capacity.</p>
</section>
</div>
<span class="qa-anchor" id="q-170-a-17"></span><span class="qa-anchor" id="q-170-a-08"></span><span class="qa-anchor" id="q-170-a-09"></span><span class="qa-anchor" id="q-170-a-10"></span><span class="qa-anchor" id="q-170-a-11"></span><span class="qa-anchor" id="q-170-a-12"></span><span class="qa-anchor" id="q-170-a-13"></span><span class="qa-anchor" id="q-170-a-14"></span><span class="qa-anchor" id="q-170-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-idns">NVM Command Set 1.3 §4.1.5.1–4.1.5.4</a> · <a href="#ref-nsattach">Base 2.4 §5.2.24–5.2.25, 8.1.17–8.1.17.2</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-nspelevent">Base 2.4 §5.2.13.1.14.2.6</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-171" data-question="171" data-answer-kind="compare"><h2><a class="qa-qid" href="#q-171">Q171</a> How do write-protection modes and entry controls differ?</h2>
<p class="qa-prompt">Identify the key difference and one case where the alternatives are not interchangeable.</p>
<details class="qa-answer" id="q-171-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-171-a-01">Protection modes differ in reversibility; permanent protection is not an ordinary reversible toggle.</p><div class="qa-sections">
<section class="qa-section" id="q-171-s-01" data-answer-section="1"><h3><span>1.</span> What differs</h3>
<span class="qa-anchor" id="q-171-a-02"></span><p>WPS is namespace state enforced across attached controllers.</p>
<span class="qa-anchor" id="q-171-a-04"></span><p>WPS0/1/2/3 select unprotected/ordinary/until-cycle/permanent; only ordinary protection is normally reversible by Set.</p>
</section>
<section class="qa-section" id="q-171-s-02" data-answer-section="2"><h3><span>2.</span> How to choose and verify</h3>
<span class="qa-anchor" id="q-171-a-03"></span><p>NWPC advertises modes, RPMB WPC gates entry and FID 84h reports actual WPS.</p>
<span class="qa-anchor" id="q-171-a-05"></span><p>Check support/entry permission, Set and Get; entering protection commits associated volatile cached data/metadata.</p>
<span class="qa-anchor" id="q-171-a-06"></span><p>State and write prohibition agree while reads remain subject to normal conditions.</p>
</section>
<section class="qa-section" id="q-171-s-03" data-answer-section="3"><h3><span>3.</span> Where the comparison stops</h3>
<span class="qa-anchor" id="q-171-a-07"></span><p>Disallowed entry or changing locked modes uses Feature Not Changeable; until-cycle mode is prohibited in multi-domain systems.</p>
<span class="qa-anchor" id="q-171-a-16"></span><p>WPC is entry permission, not state; clearing it does not remove existing protection.</p>
</section>
</div>
<span class="qa-anchor" id="q-171-a-17"></span><span class="qa-anchor" id="q-171-a-08"></span><span class="qa-anchor" id="q-171-a-09"></span><span class="qa-anchor" id="q-171-a-10"></span><span class="qa-anchor" id="q-171-a-11"></span><span class="qa-anchor" id="q-171-a-12"></span><span class="qa-anchor" id="q-171-a-13"></span><span class="qa-anchor" id="q-171-a-14"></span><span class="qa-anchor" id="q-171-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-nwp">Base 2.4 §5.2.30.1.38, 8.1.18</a> · <a href="#ref-nsattach">Base 2.4 §5.2.24–5.2.25, 8.1.17–8.1.17.2</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-nspelevent">Base 2.4 §5.2.13.1.14.2.6</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-172" data-question="172" data-answer-kind="lifecycle"><h2><a class="qa-qid" href="#q-172">Q172</a> How does write protection persist across reset and power?</h2>
<p class="qa-prompt">Name the reset or interruption, then assess settings, ongoing operations and data separately.</p>
<details class="qa-answer" id="q-172-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-172-a-01">FID 84h is non-saveable but has explicit persistent state; generic saved-feature assumptions do not apply.</p><div class="qa-sections">
<section class="qa-section" id="q-172-s-01" data-answer-section="1"><h3><span>1.</span> Identify the trigger and affected objects</h3>
<span class="qa-anchor" id="q-172-a-02"></span><p>Persistence follows the namespace, not one access controller.</p>
<span class="qa-anchor" id="q-172-a-03"></span><p>Read current WPS and record the actual reset/power event.</p>
</section>
<section class="qa-section" id="q-172-s-02" data-answer-section="2"><h3><span>2.</span> State changes and recovery</h3>
<span class="qa-anchor" id="q-172-a-04"></span><p>WPS1/3 persist across reset/power; WPS2 survives non-power CLR and clears to 0 on power cycle.</p>
<span class="qa-anchor" id="q-172-a-05"></span><p>Set baseline, perform the selected event and verify state/behavior; clearingCC.EN is not power cycling.</p>
<span class="qa-anchor" id="q-172-a-06"></span><p>WPS2 remaining protected after controller reset is correct; actual power cycling releases it.</p>
</section>
<section class="qa-section" id="q-172-s-03" data-answer-section="3"><h3><span>3.</span> Verify retention and recovery</h3>
<span class="qa-anchor" id="q-172-a-07"></span><p>No default value exists; Get Default returns Invalid Field, not a fabricated restoration value.</p>
<span class="qa-anchor" id="q-172-a-16"></span><p>Compare WPS and actual write/format restrictions.</p>
<span class="qa-anchor" id="q-172-a-17"></span><p>First establish whether a real power cycle occurred.</p>
</section>
</div>
<span class="qa-anchor" id="q-172-a-08"></span><span class="qa-anchor" id="q-172-a-09"></span><span class="qa-anchor" id="q-172-a-10"></span><span class="qa-anchor" id="q-172-a-11"></span><span class="qa-anchor" id="q-172-a-12"></span><span class="qa-anchor" id="q-172-a-13"></span><span class="qa-anchor" id="q-172-a-14"></span><span class="qa-anchor" id="q-172-a-15"></span>
<p class="qa-related">Related mechanisms: <a href="/nvme/question-bank/features/en/#q-065">Q65</a></p>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-nwp">Base 2.4 §5.2.30.1.38, 8.1.18</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-nsattach">Base 2.4 §5.2.24–5.2.25, 8.1.17–8.1.17.2</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-nspelevent">Base 2.4 §5.2.13.1.14.2.6</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-173" data-question="173" data-answer-kind="concept"><h2><a class="qa-qid" href="#q-173">Q173</a> How does protection affect format, sanitize and namespace management?</h2>
<p class="qa-prompt">Explain the mechanism in your own words and identify a common misconception.</p>
<details class="qa-answer" id="q-173-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-173-a-01">Protection covers operations modifying the namespace, including broad commands not naming it directly.</p><div class="qa-sections">
<section class="qa-section" id="q-173-s-01" data-answer-section="1"><h3><span>1.</span> Mechanism and scope</h3>
<span class="qa-anchor" id="q-173-a-02"></span><p>All attached paths enforce protection, including covering Format/subsystem-sanitize scopes.</p>
<span class="qa-anchor" id="q-173-a-04"></span><p>Reads/Compare/Verify generally remain allowed; Flush succeeds without effect after cache commitment. Attachment is allowed, while modifying deletion/format/sanitize is restricted.</p>
</section>
<section class="qa-section" id="q-173-s-02" data-answer-section="2"><h3><span>2.</span> Understand it through actions and results</h3>
<span class="qa-anchor" id="q-173-a-03"></span><p>Check WPS, scope and Figure 737 permitted actions.</p>
<span class="qa-anchor" id="q-173-a-05"></span><p>Compute full impact before checking each namespace’s protection and command exceptions.</p>
<span class="qa-anchor" id="q-173-a-06"></span><p>Allowed queries succeed while prohibited changes are rejected across paths.</p>
</section>
<section class="qa-section" id="q-173-s-03" data-answer-section="3"><h3><span>3.</span> Avoid a misleading conclusion</h3>
<span class="qa-anchor" id="q-173-a-07"></span><p>Prohibited modifications use Namespace is Write Protected; ignoring SMART critical warnings for sanitize does not bypass namespace protection.</p>
<span class="qa-anchor" id="q-173-a-16"></span><p>Cross-check direct writes and broader operations against the same protection scope.</p>
</section>
</div>
<span class="qa-anchor" id="q-173-a-17"></span><span class="qa-anchor" id="q-173-a-08"></span><span class="qa-anchor" id="q-173-a-09"></span><span class="qa-anchor" id="q-173-a-10"></span><span class="qa-anchor" id="q-173-a-11"></span><span class="qa-anchor" id="q-173-a-12"></span><span class="qa-anchor" id="q-173-a-13"></span><span class="qa-anchor" id="q-173-a-14"></span><span class="qa-anchor" id="q-173-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-nwp">Base 2.4 §5.2.30.1.38, 8.1.18</a> · <a href="#ref-format">Base 2.4 §5.1.1, 5.2.11</a> · <a href="#ref-sanitizecmd">Base 2.4 §5.2.26–5.2.27</a> · <a href="#ref-nsattach">Base 2.4 §5.2.24–5.2.25, 8.1.17–8.1.17.2</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-nspelevent">Base 2.4 §5.2.13.1.14.2.6</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<section id="common-rules" class="qa-common"><h2>Shared rules linked from the answers</h2><p>Each shared mechanism is explained in full once in this volume. Use browser Back to return to the question; explicit command or feature exceptions take precedence.</p>
<article id="common-namespace_op-9"><h3>Shared conditions for this topic · Is an asynchronous event generated?</h3><p>Create/delete affect allocated inventory; attach/detach affect controller active lists. Apply per-controller support/AEC. The Admin Delete recipient does not report its own deletion notice; other eligible controllers do.</p></article>
<article id="common-namespace_op-10"><h3>Shared conditions for this topic · Are Error Information or other logs updated?</h3><p>Identify lists establish current allocation/attachment; changed lists 04h/1Ch identify changes rather than complete state. Errors use More and applicable Error Information fields.</p></article>
<article id="common-namespace_op-11"><h3>Shared conditions for this topic · Is it recorded in the Persistent Event Log?</h3><p>Supported Change Namespace 06h records defined management changes; do not treat attachment as creation/deletion. Write protection follows supported Set Feature-event rules.</p></article>
</section>
<section id="source-index"><h2>Source locations and existing figure guides</h2><p>Base printed page = PDF page−26; the other two use identical numbers. Locations follow the supplied PDF body and retain figure numbers. Shared pages contribute only the relevant definitions, excluding Fabrics and PCIe link/packet content.</p><ul class="qa-references">
<li id="ref-nsid"><strong>Base 2.4 · §3.2.1</strong><br>Printed pages 78–81 · PDF 104–107</li>
<li id="ref-reset"><strong>Base 2.4 · §3.7.1–3.7.4</strong><br>Printed pages 120–124 · PDF 146–150</li>
<li id="ref-sqe"><strong>Base 2.4 · §4.1.1</strong><br>Printed pages 139–142 · PDF 165–168 · Figure 92–93</li>
<li id="ref-status"><strong>Base 2.4 · §4.2.3</strong><br>Printed pages 145–155 · PDF 171–181 · Figure 101–105</li>
<li id="ref-feature"><strong>Base 2.4 · §4.4</strong><br>Printed pages 166–169 · PDF 192–195 · Figure 126–127</li>
<li id="ref-format"><strong>Base 2.4 · §5.1.1, 5.2.11</strong><br>Printed pages 178–179, 206–209 · PDF 204–205, 232–235 · Figure 144, 194–196</li>
<li id="ref-aer"><strong>Base 2.4 · §5.2.2</strong><br>Printed pages 183–190 · PDF 209–216 · Figure 150–156</li>
<li id="ref-aerfull"><strong>Base 2.4 · §5.2.2 (PCIe-applicable events)</strong><br>Printed pages 183–191 · PDF 209–217 · Figure 150–160</li>
<li id="ref-getlog"><strong>Base 2.4 · §5.2.13–5.2.13.1.1</strong><br>Printed pages 212–218 · PDF 238–244 · Figure 203–211</li>
<li id="ref-error"><strong>Base 2.4 · §5.2.13.1.2</strong><br>Printed pages 218–220 · PDF 244–246 · Figure 212</li>
<li id="ref-changedlog"><strong>Base 2.4 · §5.2.13.1.5</strong><br>Printed pages 226 · PDF 252</li>
<li id="ref-commandseffects"><strong>Base 2.4 · §5.2.13.1.6</strong><br>Printed pages 226–229 · PDF 252–255 · Figure 216–217</li>
<li id="ref-pel"><strong>Base 2.4 · §5.2.13.1.14 (header, reset, hardware, Set Feature events)</strong><br>Printed pages 244–256, 258, 262–264 · PDF 270–282, 284, 288–290 · Figure 232–244, 246, 252–253</li>
<li id="ref-nspelevent"><strong>Base 2.4 · §5.2.13.1.14.2.6</strong><br>Printed pages 258–259 · PDF 284–285 · Figure 247</li>
<li id="ref-idctrl"><strong>Base 2.4 · §5.2.14.2.1</strong><br>Printed pages 340–387 · PDF 366–413 · Figure 338–341</li>
<li id="ref-idlist"><strong>Base 2.4 · §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</strong><br>Printed pages 387–399, 402–404 · PDF 413–425, 428–430 · Figure 342–355, 360–362</li>
<li id="ref-nsattach"><strong>Base 2.4 · §5.2.24–5.2.25, 8.1.17–8.1.17.2</strong><br>Printed pages 444–448, 660–663 · PDF 470–474, 686–689 · Figure 442–450</li>
<li id="ref-sanitizecmd"><strong>Base 2.4 · §5.2.26–5.2.27</strong><br>Printed pages 448–454 · PDF 474–480 · Figure 451–455</li>
<li id="ref-aec"><strong>Base 2.4 · §5.2.30.1.6</strong><br>Printed pages 466–468 · PDF 492–494 · Figure 474</li>
<li id="ref-nwp"><strong>Base 2.4 · §5.2.30.1.38, 8.1.18</strong><br>Printed pages 512, 664–666 · PDF 538, 690–692 · Figure 541, 735–737</li>
<li id="ref-idns"><strong>NVM Command Set 1.3 · §4.1.5.1–4.1.5.4</strong><br>Printed pages 84–107 · PDF 84–107 · Figure 123–130</li>
<li id="ref-nvmcreate"><strong>NVM Command Set 1.3 · §4.1.5.8, 4.1.6, 5.8</strong><br>Printed pages 108, 110–113, 162–163 · PDF 108, 110–113, 162–163 · Figure 132–134</li>
</ul><h3>When you need a field guide</h3><p>Existing figure explanations have canonical locations; use these links instead of duplicating the same guide.</p><ul>
<li><a href="/nvme/figure-reference/command/en/#figure-b101">Base 2.4 Figure 101 · Completion Queue Entry: Status Field</a></li>
<li><a href="/nvme/figure-reference/command/en/#figure-b104">Base 2.4 Figure 104 · Status Code – Command Specific Status Values</a></li>
<li><a href="/nvme/figure-reference/identify/en/#figure-b338">Base 2.4 Figure 338 · Identify – Identify Controller Data Structure, I/O Command Set Independent</a></li>
<li><a href="/nvme/figure-reference/command/en/#figure-b93">Base 2.4 Figure 93 · Common Command Format</a></li>
<li><a href="/nvme/figure-reference/identify/en/#figure-n123">NVM Command Set 1.3 Figure 123 · Identify – Identify Namespace Data Structure, NVM Command Set</a></li>
</ul><details><summary>Original documents used</summary><ul class="qr-sources">
<li>NVM Express Base Specification · Revision 2.4 · 2026-07-31<br><code>NVM-Express-Base-Specification-Revision-2.4-Ratified-2026.07.31.pdf</code></li>
<li>NVM Express NVM Command Set Specification · Revision 1.3 · 2026-07-31<br><code>NVM-Express-NVM-Command-Set-Specification-Revision-1.3-Ratified-2026.07.31.pdf</code></li>
<li>NVM Express NVMe over PCIe Transport Specification · Revision 1.4 · 2026-07-31<br><code>NVM-Express-NVMe-over-PCIe-Transport-Specification-Revision-1.4-Ratified-2026.07.31.pdf</code></li>
</ul></details></section>
</main>
<nav class="qr-top" aria-label="Bank and editions"><a href="#content">Skip to content</a><a href="/nvme/question-bank/en/">Question index</a><a href="/nvme/question-bank/namespace-management/zh-tw/">繁體中文</a><a href="/DOCS/nvme-question-bank/namespace-management.html">Chinese tutorial HTML</a></nav>
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
