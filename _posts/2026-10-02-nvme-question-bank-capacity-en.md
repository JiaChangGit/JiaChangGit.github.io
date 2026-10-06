---
layout: post
title: "NVMe Self-Study Bank: NVM sets, endurance groups and capacity"
date: 2026-10-02 00:00:00 +0800
categories: [nvme]
permalink: /nvme/question-bank/capacity/en/
lang: en
nvme_quickref: true
nvme_qa: true
---

<div class="nvme-quickref nvme-qa">
<nav class="qr-top" aria-label="Bank and editions"><a href="#content">Skip to content</a><a href="/nvme/question-bank/en/">Question index</a><a href="/nvme/question-bank/capacity/zh-tw/">繁體中文</a><a href="/DOCS/nvme-question-bank/capacity.html">Chinese tutorial HTML</a></nav>
<main id="content"><p class="qr-eyebrow">BASE 2.4 / NVM 1.3 / PCIe 1.4 · Q1–328</p>
<header><p class="qa-range">Q256–Q267</p><h1>NVM sets, endurance groups and capacity</h1><p class="qr-intro">Establish ownership before interpreting layer-specific capacity and group-scoped health.</p><p>Practice first, then reveal the explanation. Each question uses the prose, field interpretation, comparison or flow that suits it. All numerical examples are hypothetical. Status is written SCT/SC; h indicates hexadecimal.</p></header>
<aside class="qa-glossary"><h2>Terms used in this volume</h2><dl><dt>Controller / namespace</dt><dd>A controller receives commands and manages access. A namespace is a logical storage space that commands can address. An NVM subsystem contains controllers and nonvolatile storage resources.</dd><dt>SQ / CQ / SQE / CQE</dt><dd>Submission and Completion Queues carry command entries (SQEs) and completion entries (CQEs). QID identifies a queue, CID distinguishes outstanding commands in one SQ, and NSID identifies a namespace.</dd><dt>Register / Identify / Feature / Log</dt><dd>A register exposes control or state. Identify queries capabilities and attributes; features query or configure operation; log pages report specific state or records. FID, LID, CNS and CSI select features, logs, Identify structures and command sets.</dd><dt>index / offset / zero-based</dt><dd>An index selects an entry, usually starting at 0; an offset measures distance from an origin in specified units. A zero-based count encodes count−1, but not every zero-valued field is a count. A Dword is 4 bytes; a byte is 8 bits.</dd><dt>Scope / reset / retention</dt><dd>Scope names the affected objects; retention means preserving state. Controller Reset (clearing CC.EN) is one form of Controller Level Reset, or CLR. Different CLR triggers can retain different registers.</dd></dl></aside>
<section id="overview" class="qa-overview"><h2>Capacity has multiple accounting layers</h2><p class="qa-takeaway">Namespace blocks, group bytes and adjusted physical consumption differ.</p>
<div class="qr-table" tabindex="0" role="region" aria-label="Horizontally scrollable comparison table"><table><thead><tr><th scope="col">Layer</th><th scope="col">Observation</th><th scope="col">Common mistake</th></tr></thead><tbody><tr><td>Namespace</td><td>Logical size/capacity and format</td><td>Treating blocks as bytes</td></tr><tr><td>Set/group</td><td>Total/unallocated capacity</td><td>Double-counting resource pools</td></tr><tr><td>Physical allocation</td><td>Adjustment and granularity</td><td>Equating logical size and physical cost</td></tr><tr><td>Health</td><td>Group log/warnings</td><td>Using SMART counter units</td></tr></tbody></table></div>
<p><strong>Worked interpretation: </strong>CAF200 can make 5 GiB consume 10 GiB before granularity effects; it does not double LBA size.</p>
<p class="qa-citations">Sources: <a href="#ref-capacitymodel">Base 2.4 §3.2.2–3.2.3, 3.8</a> · <a href="#ref-capacitycmd">Base 2.4 §5.2.3</a> · <a href="#ref-capacityop">Base 2.4 §8.1.4</a> · <a href="#ref-eghealth">Base 2.4 §5.2.13.1.10</a> · <a href="#ref-egevents">Base 2.4 §3.2.3.1, 5.2.13.1.15, 5.2.30.1.17</a></p>
</section>
<div class="qa-controls" hidden><label>Search this page <input type="search" id="qa-search" placeholder="Question number, field or keyword"></label><button type="button" data-expand="true">Expand all answers</button><button type="button" data-expand="false">Collapse all answers</button><output id="qa-count" aria-live="polite"></output></div>
<section id="question-index"><h2>Questions in this volume</h2><ol class="qa-index">
<li><a href="#q-256">Q256 · How are NVM sets, endurance groups and namespaces related?</a></li>
<li><a href="#q-257">Q257 · How are sets and groups discovered through Identify?</a></li>
<li><a href="#q-258">Q258 · How is a namespace created in a selected set or group?</a></li>
<li><a href="#q-259">Q259 · What happens when a set or group identifier does not exist?</a></li>
<li><a href="#q-260">Q260 · What does the Endurance Group Information Log report?</a></li>
<li><a href="#q-261">Q261 · How are group health warnings and events updated?</a></li>
<li><a href="#q-262">Q262 · How are total and unallocated capacities determined?</a></li>
<li><a href="#q-263">Q263 · How do namespace creation and deletion affect free capacity?</a></li>
<li><a href="#q-264">Q264 · How does Capacity Management allocate and release groups and sets?</a></li>
<li><a href="#q-265">Q265 · What happens when capacity or identifiers are exhausted?</a></li>
<li><a href="#q-266">Q266 · Which views change after capacity reconfiguration?</a></li>
<li><a href="#q-267">Q267 · How does storage configuration persist across reset and power cycle?</a></li>
</ol></section>
<article class="qa-question" id="q-256" data-question="256" data-answer-kind="compare"><h2><a class="qa-qid" href="#q-256">Q256</a> How are NVM sets, endurance groups and namespaces related?</h2>
<p class="qa-prompt">Identify the key difference and one case where the alternatives are not interchangeable.</p>
<details class="qa-answer" id="q-256-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-256-a-01">They organize capacity, endurance and logical access rather than rename one object.</p><div class="qa-sections">
<section class="qa-section" id="q-256-s-01" data-answer-section="1"><h3><span>1.</span> What differs</h3>
<span class="qa-anchor" id="q-256-a-02"></span><p>With set support, a formatted namespace resides in one set, each set in one group and each group in one domain.</p>
<span class="qa-anchor" id="q-256-a-04"></span><p>Set lists, group logs and namespace Identify provide distinct capacity, health and membership views.</p>
</section>
<section class="qa-section" id="q-256-s-02" data-answer-section="2"><h3><span>2.</span> How to choose and verify</h3>
<span class="qa-anchor" id="q-256-a-03"></span><p>Read support and lists, then namespace membership identifiers.</p>
<span class="qa-anchor" id="q-256-a-05"></span><p>Draw supported layers and actual IDs; absence of set support does not create a fictional Set 0 layer.</p>
<span class="qa-anchor" id="q-256-a-06"></span><p>Example EG1 contains Set 2/3 and their namespaces, with endurance managed across those sets.</p>
</section>
<section class="qa-section" id="q-256-s-03" data-answer-section="3"><h3><span>3.</span> Where the comparison stops</h3>
<span class="qa-anchor" id="q-256-a-07"></span><p>Set support requires groups; group support does not require sets.</p>
<span class="qa-anchor" id="q-256-a-16"></span><p>Cross-check membership through all supported layers.</p>
</section>
</div>
<span class="qa-anchor" id="q-256-a-17"></span><span class="qa-anchor" id="q-256-a-08"></span><span class="qa-anchor" id="q-256-a-09"></span><span class="qa-anchor" id="q-256-a-10"></span><span class="qa-anchor" id="q-256-a-11"></span><span class="qa-anchor" id="q-256-a-12"></span><span class="qa-anchor" id="q-256-a-13"></span><span class="qa-anchor" id="q-256-a-14"></span><span class="qa-anchor" id="q-256-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-capacitymodel">Base 2.4 §3.2.2–3.2.3, 3.8</a> · <a href="#ref-capacitycmd">Base 2.4 §5.2.3</a> · <a href="#ref-capacityop">Base 2.4 §8.1.4</a> · <a href="#ref-eghealth">Base 2.4 §5.2.13.1.10</a> · <a href="#ref-egevents">Base 2.4 §3.2.3.1, 5.2.13.1.15, 5.2.30.1.17</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-nvmcreate">NVM Command Set 1.3 §4.1.5.8, 4.1.6, 5.8</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-257" data-question="257" data-answer-kind="lookup"><h2><a class="qa-qid" href="#q-257">Q257</a> How are sets and groups discovered through Identify?</h2>
<p class="qa-prompt">Choose the interface and target, then identify the returned field that supports your conclusion.</p>
<details class="qa-answer" id="q-257-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-257-a-01">Capability, inventory and maximum identifier answer different questions.</p><div class="qa-sections">
<section class="qa-section" id="q-257-s-01" data-answer-section="1"><h3><span>1.</span> Select the target and information</h3>
<span class="qa-anchor" id="q-257-a-02"></span><p>Discovery reflects information accessible through the queried controller.</p>
<span class="qa-anchor" id="q-257-a-03"></span><p>Read support/maxima and the respective inventories.</p>
<span class="qa-anchor" id="q-257-a-04"></span><p>Set attributes include capacities/membership; detailed group data comes from LID 09h.</p>
</section>
<section class="qa-section" id="q-257-s-02" data-answer-section="2"><h3><span>2.</span> Query sequence and interpretation</h3>
<span class="qa-anchor" id="q-257-a-05"></span><p>Enumerate actual IDs before reading details; do not assume every possible ID exists.</p>
<span class="qa-anchor" id="q-257-a-06"></span><p>Discover inventory and distinguish absent allocation from unsupported capability.</p>
</section>
<section class="qa-section" id="q-257-s-03" data-answer-section="3"><h3><span>3.</span> Handle missing or inconsistent evidence</h3>
<span class="qa-anchor" id="q-257-a-07"></span><p>Required zero output for unsupported functionality does not create valid entity 0.</p>
<span class="qa-anchor" id="q-257-a-16"></span><p>Reconcile advertisement, inventories, maxima and membership.</p>
<span class="qa-anchor" id="q-257-a-17"></span><p>First check confusion between maximum ID and current count.</p>
</section>
</div>
<span class="qa-anchor" id="q-257-a-08"></span><span class="qa-anchor" id="q-257-a-09"></span><span class="qa-anchor" id="q-257-a-10"></span><span class="qa-anchor" id="q-257-a-11"></span><span class="qa-anchor" id="q-257-a-12"></span><span class="qa-anchor" id="q-257-a-13"></span><span class="qa-anchor" id="q-257-a-14"></span><span class="qa-anchor" id="q-257-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-capacitymodel">Base 2.4 §3.2.2–3.2.3, 3.8</a> · <a href="#ref-capacitycmd">Base 2.4 §5.2.3</a> · <a href="#ref-capacityop">Base 2.4 §8.1.4</a> · <a href="#ref-eghealth">Base 2.4 §5.2.13.1.10</a> · <a href="#ref-egevents">Base 2.4 §3.2.3.1, 5.2.13.1.15, 5.2.30.1.17</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-nvmcreate">NVM Command Set 1.3 §4.1.5.8, 4.1.6, 5.8</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-258" data-question="258" data-answer-kind="process"><h2><a class="qa-qid" href="#q-258">Q258</a> How is a namespace created in a selected set or group?</h2>
<p class="qa-prompt">Order the actions and identify which completion must precede the next action.</p>
<details class="qa-answer" id="q-258-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-258-a-01">Select a resource pool while encoding logical capacity in blocks of the chosen format.</p><div class="qa-sections">
<section class="qa-section" id="q-258-s-01" data-answer-section="1"><h3><span>1.</span> Prepare the operation</h3>
<span class="qa-anchor" id="q-258-a-02"></span><p>Creation selects placement for a new object rather than moving an existing namespace.</p>
<span class="qa-anchor" id="q-258-a-03"></span><p>Check inventory, capacity and LBA format before selecting membership.</p>
<span class="qa-anchor" id="q-258-a-04"></span><p>Create fields combine logical size/capacity, format/protection and membership.</p>
</section>
<section class="qa-section" id="q-258-s-02" data-answer-section="2"><h3><span>2.</span> Sequence and completion conditions</h3>
<span class="qa-anchor" id="q-258-a-05"></span><p>Both zero delegate selection; group-only selects within it; a specified set requires its correct nonzero group.</p>
<span class="qa-anchor" id="q-258-a-06"></span><p>Success returns NSID; verify allocated Identify and attach separately.</p>
</section>
<section class="qa-section" id="q-258-s-03" data-answer-section="3"><h3><span>3.</span> Handle unmet conditions</h3>
<span class="qa-anchor" id="q-258-a-07"></span><p>Nonexistent/mismatched explicit membership is not automatic selection.</p>
<span class="qa-anchor" id="q-258-a-16"></span><p>Verify returned membership and the correct allocation layer.</p>
</section>
</div>
<span class="qa-anchor" id="q-258-a-17"></span><span class="qa-anchor" id="q-258-a-08"></span><span class="qa-anchor" id="q-258-a-09"></span><span class="qa-anchor" id="q-258-a-10"></span><span class="qa-anchor" id="q-258-a-11"></span><span class="qa-anchor" id="q-258-a-12"></span><span class="qa-anchor" id="q-258-a-13"></span><span class="qa-anchor" id="q-258-a-14"></span><span class="qa-anchor" id="q-258-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-capacitymodel">Base 2.4 §3.2.2–3.2.3, 3.8</a> · <a href="#ref-capacitycmd">Base 2.4 §5.2.3</a> · <a href="#ref-capacityop">Base 2.4 §8.1.4</a> · <a href="#ref-eghealth">Base 2.4 §5.2.13.1.10</a> · <a href="#ref-egevents">Base 2.4 §3.2.3.1, 5.2.13.1.15, 5.2.30.1.17</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-nvmcreate">NVM Command Set 1.3 §4.1.5.8, 4.1.6, 5.8</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-259" data-question="259" data-answer-kind="error"><h2><a class="qa-qid" href="#q-259">Q259</a> What happens when a set or group identifier does not exist?</h2>
<p class="qa-prompt">Distinguish failure conditions before deciding whether a particular response is required.</p>
<details class="qa-answer" id="q-259-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-259-a-01">Zero and nonexistent nonzero identifiers differ, with zero semantics varying by command.</p><div class="qa-sections">
<section class="qa-section" id="q-259-s-01" data-answer-section="1"><h3><span>1.</span> Distinguish the failure conditions</h3>
<span class="qa-anchor" id="q-259-a-02"></span><p>Identify whether the operation is namespace/capacity management, logging or a feature.</p>
<span class="qa-anchor" id="q-259-a-04"></span><p>For example, zero ELID auto-selects a domain for group creation but is invalid for group deletion.</p>
<span class="qa-anchor" id="q-259-a-07"></span><p>Invalid capacity entity selectors and nonexistent FID 18h groups require Invalid Field.</p>
</section>
<section class="qa-section" id="q-259-s-02" data-answer-section="2"><h3><span>2.</span> Establish the cause from evidence</h3>
<span class="qa-anchor" id="q-259-a-03"></span><p>Check current inventory and command-specific special values.</p>
<span class="qa-anchor" id="q-259-a-05"></span><p>Start from a valid request and isolate one nonexistent identifier.</p>
</section>
<section class="qa-section" id="q-259-s-03" data-answer-section="3"><h3><span>3.</span> Outcome and follow-up checks</h3>
<span class="qa-anchor" id="q-259-a-06"></span><p>Valid automatic selection returns the selected ID; invalid explicit IDs must not silently target another object.</p>
<span class="qa-anchor" id="q-259-a-16"></span><p>Base has ENDGID-ignore rules when groups are unsupported; distinguish absence of capability from invalid IDs under support.</p>
<span class="qa-anchor" id="q-259-a-17"></span><p>First read zero semantics for that specific command.</p>
</section>
</div>
<span class="qa-anchor" id="q-259-a-08"></span><span class="qa-anchor" id="q-259-a-09"></span><span class="qa-anchor" id="q-259-a-10"></span><span class="qa-anchor" id="q-259-a-11"></span><span class="qa-anchor" id="q-259-a-12"></span><span class="qa-anchor" id="q-259-a-13"></span><span class="qa-anchor" id="q-259-a-14"></span><span class="qa-anchor" id="q-259-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-capacitymodel">Base 2.4 §3.2.2–3.2.3, 3.8</a> · <a href="#ref-capacitycmd">Base 2.4 §5.2.3</a> · <a href="#ref-capacityop">Base 2.4 §8.1.4</a> · <a href="#ref-eghealth">Base 2.4 §5.2.13.1.10</a> · <a href="#ref-egevents">Base 2.4 §3.2.3.1, 5.2.13.1.15, 5.2.30.1.17</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-nvmcreate">NVM Command Set 1.3 §4.1.5.8, 4.1.6, 5.8</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-260" data-question="260" data-answer-kind="fields"><h2><a class="qa-qid" href="#q-260">Q260</a> What does the Endurance Group Information Log report?</h2>
<p class="qa-prompt">Explain the units and encoding, then work through one set of values.</p>
<details class="qa-answer" id="q-260-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-260-a-01">This log provides group-scoped health/workload rather than only aggregate SMART.</p><div class="qa-sections">
<section class="qa-section" id="q-260-s-01" data-answer-section="1"><h3><span>1.</span> Establish the source and scope</h3>
<span class="qa-anchor" id="q-260-a-02"></span><p>LID 09h selects ENDGID and describes the group’s lifetime.</p>
<span class="qa-anchor" id="q-260-a-03"></span><p>Establish support and existence before reading the 512-byte structure.</p>
</section>
<section class="qa-section" id="q-260-s-02" data-answer-section="2"><h3><span>2.</span> Fields, units and worked interpretation</h3>
<span class="qa-anchor" id="q-260-a-04"></span><p>Health, host/media data volume, command/error counts and byte capacities occupy distinct field groups.</p>
<span class="qa-anchor" id="q-260-a-05"></span><p>Inspect health and difference snapshots; these data counters use rounded billions of bytes, not SMART’s 512000-byte units.</p>
<span class="qa-anchor" id="q-260-a-06"></span><p>MUW includes internal writes unlike DUW; account for quantization and unreported zero values.</p>
</section>
<section class="qa-section" id="q-260-s-03" data-answer-section="3"><h3><span>3.</span> Checks across reset or power loss</h3>
<span class="qa-anchor" id="q-260-a-14"></span>
<div class="qr-table" tabindex="0" role="region" aria-label="Horizontally scrollable comparison table"><table><thead><tr><th scope="col">Trigger</th><th scope="col">Effect on this operation or state</th></tr></thead><tbody><tr><td>What survives or continues after a power cycle?</td><td>A retained group’s lifetime information persists; feature/event configuration restoration remains a separate rule.</td></tr></tbody></table></div>
</section>
<section class="qa-section" id="q-260-s-04" data-answer-section="4"><h3><span>4.</span> Conditions that change the interpretation</h3>
<span class="qa-anchor" id="q-260-a-07"></span><p>Unreported zero is not zero consumption and cannot support a meaningful amplification ratio.</p>
<span class="qa-anchor" id="q-260-a-16"></span><p>Correlate group membership and aggregate warning semantics, not bytewise equality with SMART.</p>
</section>
<section class="qa-section" id="q-260-s-05" data-answer-section="5"><h3><span>5.</span> Reporting and shared objects</h3>
<span class="qa-anchor" id="q-260-a-15"></span><p>Group health can be shared across readers; record acknowledgments and reader timing.</p>
</section>
</div>
<span class="qa-anchor" id="q-260-a-17"></span><span class="qa-anchor" id="q-260-a-08"></span><span class="qa-anchor" id="q-260-a-09"></span><span class="qa-anchor" id="q-260-a-10"></span><span class="qa-anchor" id="q-260-a-11"></span><span class="qa-anchor" id="q-260-a-12"></span><span class="qa-anchor" id="q-260-a-13"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-capacitymodel">Base 2.4 §3.2.2–3.2.3, 3.8</a> · <a href="#ref-capacitycmd">Base 2.4 §5.2.3</a> · <a href="#ref-capacityop">Base 2.4 §8.1.4</a> · <a href="#ref-eghealth">Base 2.4 §5.2.13.1.10</a> · <a href="#ref-egevents">Base 2.4 §3.2.3.1, 5.2.13.1.15, 5.2.30.1.17</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-nvmcreate">NVM Command Set 1.3 §4.1.5.8, 4.1.6, 5.8</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-261" data-question="261" data-answer-kind="events"><h2><a class="qa-qid" href="#q-261">Q261</a> How are group health warnings and events updated?</h2>
<p class="qa-prompt">Establish the event condition, then distinguish notification, acknowledgment and recording.</p>
<details class="qa-answer" id="q-261-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-261-a-01">Live health, pending-group entries and host notices form separate stages.</p><div class="qa-sections">
<section class="qa-section" id="q-261-s-01" data-answer-section="1"><h3><span>1.</span> When the event exists and who observes it</h3>
<span class="qa-anchor" id="q-261-a-02"></span><p>FID 18h is per-group, while AEC enables aggregate-log notices.</p>
<span class="qa-anchor" id="q-261-a-03"></span><p>Inspect live health, per-group event mask and AEC notice enablement.</p>
<span class="qa-anchor" id="q-261-a-04"></span><p>Group warning bits 0/2/3 indicate spare/reliability/read-only; namespace write protection must not set EGRO. Bit 1 is reserved, unlike SMART temperature.</p>
</section>
<section class="qa-section" id="q-261-s-02" data-answer-section="2"><h3><span>2.</span> Notification, reading and acknowledgment</h3>
<span class="qa-anchor" id="q-261-a-05"></span><p>Pending groups enter 0Fh; read it, then each 09h. Successful 09h RAE0 acknowledges/removes that group’s pending entry.</p>
<span class="qa-anchor" id="q-261-a-06"></span><p>Aggregate acknowledgment is not acknowledgment of every group; current warning may already have cleared.</p>
</section>
<section class="qa-section" id="q-261-s-03" data-answer-section="3"><h3><span>3.</span> Evaluate missing notifications or records</h3>
<span class="qa-anchor" id="q-261-a-07"></span><p>Reserved warning bits or nonexistent groups in FID 18h require Invalid Field.</p>
<span class="qa-anchor" id="q-261-a-16"></span><p>The specified aggregate SMART rule applies when all groups assert the bit, not merely one group.</p>
<span class="qa-anchor" id="q-261-a-17"></span><p>First check confusion between aggregate and per-group acknowledgment.</p>
</section>
<section class="qa-section" id="q-261-s-04" data-answer-section="4"><h3><span>4.</span> Reporting and shared objects</h3>
<span class="qa-anchor" id="q-261-a-09"></span><p>FID 18h selects group warnings for the aggregate; AEC and AER conditions govern host notice of additions.</p>
<span class="qa-anchor" id="q-261-a-10"></span><p>LID 0Fh lists pending group IDs;09h reports current group health and successful RAE0 reads acknowledge that group.</p>
<span class="qa-anchor" id="q-261-a-15"></span><p>Group health can be shared across readers; record acknowledgments and reader timing.</p>
</section>
</div>
<span class="qa-anchor" id="q-261-a-08"></span><span class="qa-anchor" id="q-261-a-11"></span><span class="qa-anchor" id="q-261-a-12"></span><span class="qa-anchor" id="q-261-a-13"></span><span class="qa-anchor" id="q-261-a-14"></span>
<p class="qa-related">Related mechanisms: <a href="/nvme/question-bank/capacity/en/#q-260">Q260</a></p>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-capacitymodel">Base 2.4 §3.2.2–3.2.3, 3.8</a> · <a href="#ref-capacitycmd">Base 2.4 §5.2.3</a> · <a href="#ref-capacityop">Base 2.4 §8.1.4</a> · <a href="#ref-eghealth">Base 2.4 §5.2.13.1.10</a> · <a href="#ref-egevents">Base 2.4 §3.2.3.1, 5.2.13.1.15, 5.2.30.1.17</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-nvmcreate">NVM Command Set 1.3 §4.1.5.8, 4.1.6, 5.8</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-262" data-question="262" data-answer-kind="lookup"><h2><a class="qa-qid" href="#q-262">Q262</a> How are total and unallocated capacities determined?</h2>
<p class="qa-prompt">Choose the interface and target, then identify the returned field that supports your conclusion.</p>
<details class="qa-answer" id="q-262-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-262-a-01">Unallocated means unallocated to a particular next layer, not universally free for any operation.</p><div class="qa-sections">
<section class="qa-section" id="q-262-s-01" data-answer-section="1"><h3><span>1.</span> Select the target and information</h3>
<span class="qa-anchor" id="q-262-a-02"></span><p>Capacity pools exist at subsystem, domain, group or set scope.</p>
<span class="qa-anchor" id="q-262-a-03"></span><p>Read controller/domain capacities, group capacities and set attributes.</p>
<span class="qa-anchor" id="q-262-a-04"></span><p>Physical-capacity fields use bytes; namespace sizes use formatted blocks.</p>
</section>
<section class="qa-section" id="q-262-s-02" data-answer-section="2"><h3><span>2.</span> Query sequence and interpretation</h3>
<span class="qa-anchor" id="q-262-a-05"></span><p>Select the operation’s capacity source under Figure 89, including granularity and adjustment factor.</p>
<span class="qa-anchor" id="q-262-a-06"></span><p>Creating a set allocates from UEGCAP without requiring another decrease in subsystem UNVMCAP.</p>
</section>
<section class="qa-section" id="q-262-s-03" data-answer-section="3"><h3><span>3.</span> Handle missing or inconsistent evidence</h3>
<span class="qa-anchor" id="q-262-a-07"></span><p>Zero may mean unreported under field-specific rules rather than no capacity.</p>
<span class="qa-anchor" id="q-262-a-16"></span><p>Compare within one layer to avoid double counting.</p>
<span class="qa-anchor" id="q-262-a-17"></span><p>First identify which entity is being created.</p>
</section>
</div>
<span class="qa-anchor" id="q-262-a-08"></span><span class="qa-anchor" id="q-262-a-09"></span><span class="qa-anchor" id="q-262-a-10"></span><span class="qa-anchor" id="q-262-a-11"></span><span class="qa-anchor" id="q-262-a-12"></span><span class="qa-anchor" id="q-262-a-13"></span><span class="qa-anchor" id="q-262-a-14"></span><span class="qa-anchor" id="q-262-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-capacitymodel">Base 2.4 §3.2.2–3.2.3, 3.8</a> · <a href="#ref-capacitycmd">Base 2.4 §5.2.3</a> · <a href="#ref-capacityop">Base 2.4 §8.1.4</a> · <a href="#ref-eghealth">Base 2.4 §5.2.13.1.10</a> · <a href="#ref-egevents">Base 2.4 §3.2.3.1, 5.2.13.1.15, 5.2.30.1.17</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-nvmcreate">NVM Command Set 1.3 §4.1.5.8, 4.1.6, 5.8</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-263" data-question="263" data-answer-kind="concept"><h2><a class="qa-qid" href="#q-263">Q263</a> How do namespace creation and deletion affect free capacity?</h2>
<p class="qa-prompt">Explain the mechanism in your own words and identify a common misconception.</p>
<details class="qa-answer" id="q-263-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-263-a-01">Namespace allocation consumes its containing pool, not always controller UNVMCAP.</p><div class="qa-sections">
<section class="qa-section" id="q-263-s-01" data-answer-section="1"><h3><span>1.</span> Mechanism and scope</h3>
<span class="qa-anchor" id="q-263-a-02"></span><p>Use the supported containing layer: set, group or domain/subsystem.</p>
<span class="qa-anchor" id="q-263-a-04"></span><p>Logical size/capacity and physical consumption differ because of allocation granularity.</p>
</section>
<section class="qa-section" id="q-263-s-02" data-answer-section="2"><h3><span>2.</span> Understand it through actions and results</h3>
<span class="qa-anchor" id="q-263-a-03"></span><p>Preserve membership, format, actual NVMCAP and pool snapshots.</p>
<span class="qa-anchor" id="q-263-a-05"></span><p>After creation/deletion verify inventory and the corresponding pool.</p>
<span class="qa-anchor" id="q-263-a-06"></span><p>Capacity follows allocation rules; Detach alone does not return namespace capacity.</p>
</section>
<section class="qa-section" id="q-263-s-03" data-answer-section="3"><h3><span>3.</span> Avoid a misleading conclusion</h3>
<span class="qa-anchor" id="q-263-a-07"></span><p>Capacity exhaustion differs from identifier/count exhaustion.</p>
<span class="qa-anchor" id="q-263-a-16"></span><p>Verify allocation separately from data sanitization; deletion is not proof of purge.</p>
</section>
</div>
<span class="qa-anchor" id="q-263-a-17"></span><span class="qa-anchor" id="q-263-a-08"></span><span class="qa-anchor" id="q-263-a-09"></span><span class="qa-anchor" id="q-263-a-10"></span><span class="qa-anchor" id="q-263-a-11"></span><span class="qa-anchor" id="q-263-a-12"></span><span class="qa-anchor" id="q-263-a-13"></span><span class="qa-anchor" id="q-263-a-14"></span><span class="qa-anchor" id="q-263-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-capacitymodel">Base 2.4 §3.2.2–3.2.3, 3.8</a> · <a href="#ref-capacitycmd">Base 2.4 §5.2.3</a> · <a href="#ref-capacityop">Base 2.4 §8.1.4</a> · <a href="#ref-eghealth">Base 2.4 §5.2.13.1.10</a> · <a href="#ref-egevents">Base 2.4 §3.2.3.1, 5.2.13.1.15, 5.2.30.1.17</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-nvmcreate">NVM Command Set 1.3 §4.1.5.8, 4.1.6, 5.8</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-264" data-question="264" data-answer-kind="process"><h2><a class="qa-qid" href="#q-264">Q264</a> How does Capacity Management allocate and release groups and sets?</h2>
<p class="qa-prompt">Order the actions and identify which completion must precede the next action.</p>
<details class="qa-answer" id="q-264-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-264-a-01">Fixed selects supported layouts; Variable creates entities by requested capacity.</p><div class="qa-sections">
<section class="qa-section" id="q-264-s-01" data-answer-section="1"><h3><span>1.</span> Prepare the operation</h3>
<span class="qa-anchor" id="q-264-a-02"></span><p>Changes can cascade to contained namespaces and all paths.</p>
<span class="qa-anchor" id="q-264-a-03"></span><p>Check management/deletion support and supported fixed configurations.</p>
<span class="qa-anchor" id="q-264-a-04"></span><p>OPER selects layout/create/delete/restore; ELID meaning varies and CAPU:CAPL encodes create bytes.</p>
</section>
<section class="qa-section" id="q-264-s-02" data-answer-section="2"><h3><span>2.</span> Sequence and completion conditions</h3>
<span class="qa-anchor" id="q-264-a-05"></span><p>Variable allocation proceeds group→set→namespace; fixed reconfiguration follows clearing/selection prerequisites.</p>
<span class="qa-anchor" id="q-264-a-06"></span><p>Creation returns CELID; other operations do not universally return a valid created ID.</p>
</section>
<section class="qa-section" id="q-264-s-03" data-answer-section="3"><h3><span>3.</span> Handle unmet conditions</h3>
<span class="qa-anchor" id="q-264-a-07"></span><p>Deletion cascades; default restoration with remaining groups/sets requires Command Sequence Error.</p>
<span class="qa-anchor" id="q-264-a-16"></span><p>Requery final lists/ownership/capacity; intermediate accesses may be indeterminate.</p>
</section>
</div>
<span class="qa-anchor" id="q-264-a-17"></span><span class="qa-anchor" id="q-264-a-08"></span><span class="qa-anchor" id="q-264-a-09"></span><span class="qa-anchor" id="q-264-a-10"></span><span class="qa-anchor" id="q-264-a-11"></span><span class="qa-anchor" id="q-264-a-12"></span><span class="qa-anchor" id="q-264-a-13"></span><span class="qa-anchor" id="q-264-a-14"></span><span class="qa-anchor" id="q-264-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-capacitymodel">Base 2.4 §3.2.2–3.2.3, 3.8</a> · <a href="#ref-capacitycmd">Base 2.4 §5.2.3</a> · <a href="#ref-capacityop">Base 2.4 §8.1.4</a> · <a href="#ref-eghealth">Base 2.4 §5.2.13.1.10</a> · <a href="#ref-egevents">Base 2.4 §3.2.3.1, 5.2.13.1.15, 5.2.30.1.17</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-nvmcreate">NVM Command Set 1.3 §4.1.5.8, 4.1.6, 5.8</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-265" data-question="265" data-answer-kind="error"><h2><a class="qa-qid" href="#q-265">Q265</a> What happens when capacity or identifiers are exhausted?</h2>
<p class="qa-prompt">Distinguish failure conditions before deciding whether a particular response is required.</p>
<details class="qa-answer" id="q-265-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-265-a-01">Capacity exhaustion and identifier exhaustion are distinct limits.</p><div class="qa-sections">
<section class="qa-section" id="q-265-s-01" data-answer-section="1"><h3><span>1.</span> Distinguish the failure conditions</h3>
<span class="qa-anchor" id="q-265-a-02"></span><p>Group creation checks relevant pool/max size; set creation checks UEGCAP.</p>
<span class="qa-anchor" id="q-265-a-04"></span><p>Interpret requested bytes with adjustment and allocation granularity.</p>
<span class="qa-anchor" id="q-265-a-07"></span><p>Capacity shortage returns 1/26h; identifier exhaustion returns 1/2Dh.</p>
</section>
<section class="qa-section" id="q-265-s-02" data-answer-section="2"><h3><span>2.</span> Establish the cause from evidence</h3>
<span class="qa-anchor" id="q-265-a-03"></span><p>Inspect capacity limits and inventory.</p>
<span class="qa-anchor" id="q-265-a-05"></span><p>Isolate capacity and identifier exhaustion in separate scenarios.</p>
</section>
<section class="qa-section" id="q-265-s-03" data-answer-section="3"><h3><span>3.</span> Outcome and follow-up checks</h3>
<span class="qa-anchor" id="q-265-a-06"></span><p>Adequate resources create an entity and return CELID; failure must not fabricate one.</p>
<span class="qa-anchor" id="q-265-a-16"></span><p>Prose specifies largest creatable capacity in CSINFO, while Figure 165 describes required capacity. Preserve this conflict rather than using one interpretation as an unconditional conformance oracle.</p>
<span class="qa-anchor" id="q-265-a-17"></span><p>First identify the exhausted resource, then the CSINFO source ambiguity.</p>
</section>
<section class="qa-section" id="q-265-s-04" data-answer-section="4"><h3><span>4.</span> Evidence supplied by the log</h3>
<span class="qa-anchor" id="q-265-a-10"></span><p>Insufficient-capacity creation requires the stated CSINFO detail when Error Log is supported; preserve the prose/Figure 165 semantic conflict.</p>
</section>
</div>
<span class="qa-anchor" id="q-265-a-08"></span><span class="qa-anchor" id="q-265-a-09"></span><span class="qa-anchor" id="q-265-a-11"></span><span class="qa-anchor" id="q-265-a-12"></span><span class="qa-anchor" id="q-265-a-13"></span><span class="qa-anchor" id="q-265-a-14"></span><span class="qa-anchor" id="q-265-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-capacitymodel">Base 2.4 §3.2.2–3.2.3, 3.8</a> · <a href="#ref-capacitycmd">Base 2.4 §5.2.3</a> · <a href="#ref-capacityop">Base 2.4 §8.1.4</a> · <a href="#ref-eghealth">Base 2.4 §5.2.13.1.10</a> · <a href="#ref-egevents">Base 2.4 §3.2.3.1, 5.2.13.1.15, 5.2.30.1.17</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-nvmcreate">NVM Command Set 1.3 §4.1.5.8, 4.1.6, 5.8</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-266" data-question="266" data-answer-kind="process"><h2><a class="qa-qid" href="#q-266">Q266</a> Which views change after capacity reconfiguration?</h2>
<p class="qa-prompt">Order the actions and identify which completion must precede the next action.</p>
<details class="qa-answer" id="q-266-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-266-a-01">Validate coherent views, not just successful CQE.</p><div class="qa-sections">
<section class="qa-section" id="q-266-s-01" data-answer-section="1"><h3><span>1.</span> Prepare the operation</h3>
<span class="qa-anchor" id="q-266-a-02"></span><p>Inspect affected group/set/namespace/domain/media relationships.</p>
<span class="qa-anchor" id="q-266-a-03"></span><p>Preserve inventory, capacity and ownership snapshots.</p>
<span class="qa-anchor" id="q-266-a-04"></span><p>Group creation changes parent capacity; set creation changes set inventory/UEGCAP but not UNVMCAP; deletion follows its cascade.</p>
</section>
<section class="qa-section" id="q-266-s-02" data-answer-section="2"><h3><span>2.</span> Sequence and completion conditions</h3>
<span class="qa-anchor" id="q-266-a-05"></span><p>Read after completion and account for concurrent management.</p>
<span class="qa-anchor" id="q-266-a-06"></span><p>Deleting a set removes its namespaces, clears applicable media ownership and returns group capacity.</p>
</section>
<section class="qa-section" id="q-266-s-03" data-answer-section="3"><h3><span>3.</span> Handle unmet conditions</h3>
<span class="qa-anchor" id="q-266-a-07"></span><p>Ordered intermediate updates are not universally atomic byte-for-byte to all readers.</p>
<span class="qa-anchor" id="q-266-a-16"></span><p>Verify the full chain of inventory, child removal, accounting and rediscovery notices.</p>
</section>
</div>
<span class="qa-anchor" id="q-266-a-17"></span><span class="qa-anchor" id="q-266-a-08"></span><span class="qa-anchor" id="q-266-a-09"></span><span class="qa-anchor" id="q-266-a-10"></span><span class="qa-anchor" id="q-266-a-11"></span><span class="qa-anchor" id="q-266-a-12"></span><span class="qa-anchor" id="q-266-a-13"></span><span class="qa-anchor" id="q-266-a-14"></span><span class="qa-anchor" id="q-266-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-capacitymodel">Base 2.4 §3.2.2–3.2.3, 3.8</a> · <a href="#ref-capacitycmd">Base 2.4 §5.2.3</a> · <a href="#ref-capacityop">Base 2.4 §8.1.4</a> · <a href="#ref-eghealth">Base 2.4 §5.2.13.1.10</a> · <a href="#ref-egevents">Base 2.4 §3.2.3.1, 5.2.13.1.15, 5.2.30.1.17</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-nvmcreate">NVM Command Set 1.3 §4.1.5.8, 4.1.6, 5.8</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-267" data-question="267" data-answer-kind="lifecycle"><h2><a class="qa-qid" href="#q-267">Q267</a> How does storage configuration persist across reset and power cycle?</h2>
<p class="qa-prompt">Name the reset or interruption, then assess settings, ongoing operations and data separately.</p>
<details class="qa-answer" id="q-267-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-267-a-01">Storage organization is distinct from transient I/O queues; reset is not configuration deletion.</p><div class="qa-sections">
<section class="qa-section" id="q-267-s-01" data-answer-section="1"><h3><span>1.</span> Identify the trigger and affected objects</h3>
<span class="qa-anchor" id="q-267-a-02"></span><p>Compare completed entity membership and capacity accounting.</p>
<span class="qa-anchor" id="q-267-a-03"></span><p>Snapshot configuration, identity, capacities and outstanding management.</p>
</section>
<section class="qa-section" id="q-267-s-02" data-answer-section="2"><h3><span>2.</span> State changes and recovery</h3>
<span class="qa-anchor" id="q-267-a-04"></span><p>OPER5 default restoration is separate and has inventory prerequisites.</p>
<span class="qa-anchor" id="q-267-a-05"></span><p>Rediscover after channel recovery; interrupted operations require outcome discovery rather than assumed rollback.</p>
<span class="qa-anchor" id="q-267-a-06"></span><p>Completed configuration remains identifiable; explain differences through actual management/state changes.</p>
</section>
<section class="qa-section" id="q-267-s-03" data-answer-section="3"><h3><span>3.</span> Checks across reset or power loss</h3>
<span class="qa-anchor" id="q-267-a-12"></span>
<span class="qa-anchor" id="q-267-a-13"></span>
<span class="qa-anchor" id="q-267-a-14"></span>
<div class="qr-table" tabindex="0" role="region" aria-label="Horizontally scrollable comparison table"><table><thead><tr><th scope="col">Trigger</th><th scope="col">Effect on this operation or state</th></tr></thead><tbody><tr><td>What survives or continues after Controller Reset?</td><td>Completed storage configuration is not volatile queue state and is not deleted by ordinary CLR. Requery interrupted operations rather than assume rollback.</td></tr><tr><td>What survives or continues after NVM Subsystem Reset?</td><td>Subsystem reset is distinct from restoring default capacity configuration; rediscover retained storage configuration unless a separate management action changed it.</td></tr><tr><td>What survives or continues after a power cycle?</td><td>Completed configuration persists across power cycles; requery interrupted operations because missing CQE does not prove no effect.</td></tr></tbody></table></div>
</section>
<section class="qa-section" id="q-267-s-04" data-answer-section="4"><h3><span>4.</span> Verify retention and recovery</h3>
<span class="qa-anchor" id="q-267-a-07"></span><p>Missing completion establishes uncertainty, not an unchanged configuration.</p>
<span class="qa-anchor" id="q-267-a-16"></span><p>Distinguish temporary query unavailability from missing persistent configuration.</p>
<span class="qa-anchor" id="q-267-a-17"></span><p>First check for separate restore/delete/reconfiguration activity.</p>
</section>
</div>
<span class="qa-anchor" id="q-267-a-08"></span><span class="qa-anchor" id="q-267-a-09"></span><span class="qa-anchor" id="q-267-a-10"></span><span class="qa-anchor" id="q-267-a-11"></span><span class="qa-anchor" id="q-267-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-capacitymodel">Base 2.4 §3.2.2–3.2.3, 3.8</a> · <a href="#ref-capacitycmd">Base 2.4 §5.2.3</a> · <a href="#ref-capacityop">Base 2.4 §8.1.4</a> · <a href="#ref-eghealth">Base 2.4 §5.2.13.1.10</a> · <a href="#ref-egevents">Base 2.4 §3.2.3.1, 5.2.13.1.15, 5.2.30.1.17</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-nvmcreate">NVM Command Set 1.3 §4.1.5.8, 4.1.6, 5.8</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>

<section id="source-index"><h2>Source locations and existing figure guides</h2><p>Base printed page = PDF page−26; the other two use identical numbers. Locations follow the supplied PDF body and retain figure numbers. Shared pages contribute only the relevant definitions, excluding Fabrics and PCIe link/packet content.</p><ul class="qa-references">
<li id="ref-capacitymodel"><strong>Base 2.4 · §3.2.2–3.2.3, 3.8</strong><br>Printed pages 80–84, 125–129 · PDF 106–110, 151–155 · Figure 67–69, 86–89</li>
<li id="ref-egevents"><strong>Base 2.4 · §3.2.3.1, 5.2.13.1.15, 5.2.30.1.17</strong><br>Printed pages 84, 270, 478 · PDF 110, 296, 504 · Figure 261, 493</li>
<li id="ref-reset"><strong>Base 2.4 · §3.7.1–3.7.4</strong><br>Printed pages 120–124 · PDF 146–150</li>
<li id="ref-status"><strong>Base 2.4 · §4.2.3</strong><br>Printed pages 145–155 · PDF 171–181 · Figure 101–105</li>
<li id="ref-aer"><strong>Base 2.4 · §5.2.2</strong><br>Printed pages 183–190 · PDF 209–216 · Figure 150–156</li>
<li id="ref-capacitycmd"><strong>Base 2.4 · §5.2.3</strong><br>Printed pages 191–195 · PDF 217–221 · Figure 162–166</li>
<li id="ref-error"><strong>Base 2.4 · §5.2.13.1.2</strong><br>Printed pages 218–220 · PDF 244–246 · Figure 212</li>
<li id="ref-eghealth"><strong>Base 2.4 · §5.2.13.1.10</strong><br>Printed pages 237–239 · PDF 263–265 · Figure 224–225</li>
<li id="ref-pel"><strong>Base 2.4 · §5.2.13.1.14 (header, reset, hardware, Set Feature events)</strong><br>Printed pages 244–256, 258, 262–264 · PDF 270–282, 284, 288–290 · Figure 232–244, 246, 252–253</li>
<li id="ref-idctrl"><strong>Base 2.4 · §5.2.14.2.1</strong><br>Printed pages 340–387 · PDF 366–413 · Figure 338–341</li>
<li id="ref-idlist"><strong>Base 2.4 · §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</strong><br>Printed pages 387–399, 402–404 · PDF 413–425, 428–430 · Figure 342–355, 360–362</li>
<li id="ref-capacityop"><strong>Base 2.4 · §8.1.4</strong><br>Printed pages 594–597 · PDF 620–623</li>
<li id="ref-nvmcreate"><strong>NVM Command Set 1.3 · §4.1.5.8, 4.1.6, 5.8</strong><br>Printed pages 108, 110–113, 162–163 · PDF 108, 110–113, 162–163 · Figure 132–134</li>
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
<nav class="qr-top" aria-label="Bank and editions"><a href="#content">Skip to content</a><a href="/nvme/question-bank/en/">Question index</a><a href="/nvme/question-bank/capacity/zh-tw/">繁體中文</a><a href="/DOCS/nvme-question-bank/capacity.html">Chinese tutorial HTML</a></nav>
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
