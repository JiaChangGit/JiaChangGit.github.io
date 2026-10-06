---
layout: post
title: "NVMe Self-Study Bank: PRP and SGL"
date: 2026-10-02 00:00:00 +0800
categories: [nvme]
permalink: /nvme/question-bank/pointers/en/
lang: en
nvme_quickref: true
nvme_qa: true
---

<div class="nvme-quickref nvme-qa">
<nav class="qr-top" aria-label="Bank and editions"><a href="#content">Skip to content</a><a href="/nvme/question-bank/en/">Question index</a><a href="/nvme/question-bank/pointers/zh-tw/">繁體中文</a><a href="/DOCS/nvme-question-bank/pointers.html">Chinese tutorial HTML</a></nav>
<main id="content"><p class="qr-eyebrow">BASE 2.4 / NVM 1.3 / PCIe 1.4 · Q1–328</p>
<header><p class="qa-range">Q276–Q285</p><h1>PRP and SGL</h1><p class="qr-intro">Learn memory layout through PRP boundary calculations, SGL descriptor relationships and distinct error classes.</p><p>Practice first, then reveal the explanation. Each question uses the prose, field interpretation, comparison or flow that suits it. All numerical examples are hypothetical. Status is written SCT/SC; h indicates hexadecimal.</p></header>
<aside class="qa-glossary"><h2>Terms used in this volume</h2><dl><dt>Controller / namespace</dt><dd>A controller receives commands and manages access. A namespace is a logical storage space that commands can address. An NVM subsystem contains controllers and nonvolatile storage resources.</dd><dt>SQ / CQ / SQE / CQE</dt><dd>Submission and Completion Queues carry command entries (SQEs) and completion entries (CQEs). QID identifies a queue, CID distinguishes outstanding commands in one SQ, and NSID identifies a namespace.</dd><dt>Register / Identify / Feature / Log</dt><dd>A register exposes control or state. Identify queries capabilities and attributes; features query or configure operation; log pages report specific state or records. FID, LID, CNS and CSI select features, logs, Identify structures and command sets.</dd><dt>index / offset / zero-based</dt><dd>An index selects an entry, usually starting at 0; an offset measures distance from an origin in specified units. A zero-based count encodes count−1, but not every zero-valued field is a count. A Dword is 4 bytes; a byte is 8 bits.</dd><dt>Scope / reset / retention</dt><dd>Scope names the affected objects; retention means preserving state. Controller Reset (clearing CC.EN) is one form of Controller Level Reset, or CLR. Different CLR triggers can retain different registers.</dd></dl></aside>
<section id="overview" class="qa-overview"><h2>A 4 KiB page with first offset 1024</h2><p class="qa-takeaway">Boundary crossings, including the first offset, determine PRP2.</p>
<div class="qr-table" tabindex="0" role="region" aria-label="Horizontally scrollable comparison table"><table><thead><tr><th scope="col">Transfer length</th><th scope="col">Remaining after first page</th><th scope="col">PRP2 role</th></tr></thead><tbody><tr><td>2048 bytes</td><td>0</td><td>Reserved</td></tr><tr><td>4096 bytes</td><td>1024 bytes</td><td>Direct second-page pointer</td></tr><tr><td>8192 bytes</td><td>5120 bytes</td><td>PRP-list pointer</td></tr></tbody></table></div>
<p><strong>Worked interpretation: </strong>A 32-byte last segment contains two descriptors; their data lengths determine payload size.</p>
<p class="qa-citations">Sources: <a href="#ref-pointers">Base 2.4 §4.2.1, 4.3.1–4.3.2 (PCIe-applicable layouts)</a> · <a href="#ref-sgls">Base 2.4 §5.2.14.2.1 (SGLS)</a> · <a href="#ref-retirement">PCIe Transport 1.4 §3.4 (Command Related Resource Retirement)</a></p>
</section>
<div class="qa-controls" hidden><label>Search this page <input type="search" id="qa-search" placeholder="Question number, field or keyword"></label><button type="button" data-expand="true">Expand all answers</button><button type="button" data-expand="false">Collapse all answers</button><output id="qa-count" aria-live="polite"></output></div>
<section id="question-index"><h2>Questions in this volume</h2><ol class="qa-index">
<li><a href="#q-276">Q276 · How does PRP1 describe the first data page?</a></li>
<li><a href="#q-277">Q277 · When is PRP2 a second-page address or a list pointer?</a></li>
<li><a href="#q-278">Q278 · How are multiple PRP-list pages chained?</a></li>
<li><a href="#q-279">Q279 · What alignment rules apply to PRPs and lists?</a></li>
<li><a href="#q-280">Q280 · Do zero, invalid or broken-chain PRPs have one universal error?</a></li>
<li><a href="#q-281">Q281 · How do SGL data, segment and last-segment descriptors work?</a></li>
<li><a href="#q-282">Q282 · How are SGL address, length, count and type errors distinguished?</a></li>
<li><a href="#q-283">Q283 · How do Identify SGL capabilities constrain usage?</a></li>
<li><a href="#q-284">Q284 · How do pointer-format errors differ from Data Transfer Error?</a></li>
<li><a href="#q-285">Q285 · How are pointer errors correlated with completion and Error Information?</a></li>
</ol></section>
<article class="qa-question" id="q-276" data-question="276" data-answer-kind="fields"><h2><a class="qa-qid" href="#q-276">Q276</a> How does PRP1 describe the first data page?</h2>
<p class="qa-prompt">Explain the units and encoding, then work through one set of values.</p>
<details class="qa-answer" id="q-276-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-276-a-01">PRPs map a command’s data stream onto memory pages, including the start within the first page.</p><div class="qa-sections">
<section class="qa-section" id="q-276-s-01" data-answer-section="1"><h3><span>1.</span> Establish the source and scope</h3>
<span class="qa-anchor" id="q-276-a-02"></span><p>These are CC.MPS memory pages, not NAND pages or namespace LBAs.</p>
<span class="qa-anchor" id="q-276-a-03"></span><p>Check supported and selected MPS; page size is 2^(12+MPS) bytes.</p>
</section>
<section class="qa-section" id="q-276-s-02" data-answer-section="2"><h3><span>2.</span> Fields, units and worked interpretation</h3>
<span class="qa-anchor" id="q-276-a-04"></span><p>Ordinary PRP1 contains a page base and Dword-aligned offset; special commands can instead define a list pointer.</p>
<span class="qa-anchor" id="q-276-a-05"></span><p>Calculate P−offset before deciding whether more pages are required.</p>
<span class="qa-anchor" id="q-276-a-06"></span><p>With page 4096, offset 1024 and length 2048, the 3072-byte remainder suffices and PRP2 is reserved.</p>
</section>
<section class="qa-section" id="q-276-s-03" data-answer-section="3"><h3><span>3.</span> Conditions that change the interpretation</h3>
<span class="qa-anchor" id="q-276-a-07"></span><p>Create Queue requires page-aligned PRP1 and does not inherit ordinary first-data-page offset freedom.</p>
<span class="qa-anchor" id="q-276-a-16"></span><p>Verify length with offset and page size; a sub-page transfer can still cross a boundary.</p>
</section>
</div>
<span class="qa-anchor" id="q-276-a-17"></span><span class="qa-anchor" id="q-276-a-08"></span><span class="qa-anchor" id="q-276-a-09"></span><span class="qa-anchor" id="q-276-a-10"></span><span class="qa-anchor" id="q-276-a-11"></span><span class="qa-anchor" id="q-276-a-12"></span><span class="qa-anchor" id="q-276-a-13"></span><span class="qa-anchor" id="q-276-a-14"></span><span class="qa-anchor" id="q-276-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-pointers">Base 2.4 §4.2.1, 4.3.1–4.3.2 (PCIe-applicable layouts)</a> · <a href="#ref-sgls">Base 2.4 §5.2.14.2.1 (SGLS)</a> · <a href="#ref-retirement">PCIe Transport 1.4 §3.4 (Command Related Resource Retirement)</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-create">Base 2.4 §5.3.1–5.3.2</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-277" data-question="277" data-answer-kind="concept"><h2><a class="qa-qid" href="#q-277">Q277</a> When is PRP2 a second-page address or a list pointer?</h2>
<p class="qa-prompt">Explain the mechanism in your own words and identify a common misconception.</p>
<details class="qa-answer" id="q-277-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-277-a-01">Boundary crossings determine PRP2 meaning without a separate list flag.</p><div class="qa-sections">
<section class="qa-section" id="q-277-s-01" data-answer-section="1"><h3><span>1.</span> Mechanism and scope</h3>
<span class="qa-anchor" id="q-277-a-02"></span><p>This applies to ordinary PRP data layouts, subject to command-specific definitions.</p>
</section>
<section class="qa-section" id="q-277-s-02" data-answer-section="2"><h3><span>2.</span> Understand it through actions and results</h3>
<span class="qa-anchor" id="q-277-a-03"></span><p>Derive the required pages from MPS, first offset and total length.</p>
<span class="qa-anchor" id="q-277-a-04"></span>
<span class="qa-anchor" id="q-277-a-05"></span>
<span class="qa-anchor" id="q-277-a-06"></span>
<span class="qa-anchor" id="q-277-a-17"></span>
<figure class="qa-flow" id="q-277-flow"><figcaption>Determine PRP2 from the remaining length</figcaption>
<p>First-page capacity is page size P minus PRP1’s page offset. Let R be the transfer length remaining after that first-page data.</p><ol class="qa-flow-steps">
<li class="qa-flow-branch"><strong>R=0: only the first page is needed</strong><p>PRP2 is reserved; no additional data page is needed.</p></li>
<li class="qa-flow-branch"><strong>0&lt;R≤P: one more page is enough</strong><p>PRP2 points directly to the second data page.</p></li>
<li class="qa-flow-branch"><strong>R&gt;P: at least two more data pages are needed</strong><p>PRP2 points to a PRP List containing the subsequent data-page addresses.</p></li>
</ol><p class="qa-flow-conclusion">These are mutually exclusive branches. With P=4096 and offset=1024, the first page holds 3072 bytes: a 4096-byte transfer leaves R=1024 (data-page pointer); an 8192-byte transfer leaves R=5120 (list pointer). PRP2 has no independent type flag; a nonzero value alone does not identify its meaning.</p></figure>
</section>
<section class="qa-section" id="q-277-s-03" data-answer-section="3"><h3><span>3.</span> Avoid a misleading conclusion</h3>
<span class="qa-anchor" id="q-277-a-07"></span><p>A wrong interpretation can turn data into addresses; detection before any transfer is not guaranteed.</p>
<span class="qa-anchor" id="q-277-a-16"></span><p>Verify the pointed content matches the derived role, not merely a nonzero address.</p>
</section>
</div>
<span class="qa-anchor" id="q-277-a-08"></span><span class="qa-anchor" id="q-277-a-09"></span><span class="qa-anchor" id="q-277-a-10"></span><span class="qa-anchor" id="q-277-a-11"></span><span class="qa-anchor" id="q-277-a-12"></span><span class="qa-anchor" id="q-277-a-13"></span><span class="qa-anchor" id="q-277-a-14"></span><span class="qa-anchor" id="q-277-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-pointers">Base 2.4 §4.2.1, 4.3.1–4.3.2 (PCIe-applicable layouts)</a> · <a href="#ref-sgls">Base 2.4 §5.2.14.2.1 (SGLS)</a> · <a href="#ref-retirement">PCIe Transport 1.4 §3.4 (Command Related Resource Retirement)</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-create">Base 2.4 §5.3.1–5.3.2</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-278" data-question="278" data-answer-kind="fields"><h2><a class="qa-qid" href="#q-278">Q278</a> How are multiple PRP-list pages chained?</h2>
<p class="qa-prompt">Explain the units and encoding, then work through one set of values.</p>
<details class="qa-answer" id="q-278-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-278-a-01">List pages store data-page addresses; additional list pages are chained when necessary.</p><div class="qa-sections">
<section class="qa-section" id="q-278-s-01" data-answer-section="1"><h3><span>1.</span> Establish the source and scope</h3>
<span class="qa-anchor" id="q-278-a-02"></span><p>The list covers data not already described by in-command PRPs.</p>
<span class="qa-anchor" id="q-278-a-03"></span><p>Use page size and eight-byte entries to calculate capacity.</p>
</section>
<section class="qa-section" id="q-278-s-02" data-answer-section="2"><h3><span>2.</span> Fields, units and worked interpretation</h3>
<span class="qa-anchor" id="q-278-a-04"></span><p>A nonfinal list page uses its last entry as a page-aligned link to the next list page.</p>
<span class="qa-anchor" id="q-278-a-05"></span><p>Pack only required entries and use a chain only when additional coverage is necessary.</p>
<span class="qa-anchor" id="q-278-a-06"></span><p>A page-aligned 4 KiB list has 512 slots:511 data pointers plus a link when nonfinal, or up to 512 data pointers when final.</p>
</section>
<section class="qa-section" id="q-278-s-03" data-answer-section="3"><h3><span>3.</span> Conditions that change the interpretation</h3>
<span class="qa-anchor" id="q-278-a-07"></span><p>Remaining transfer length determines whether the final slot is data or linkage.</p>
<span class="qa-anchor" id="q-278-a-16"></span><p>Retain command lists until completion, but queue lists until successful deletion or reset.</p>
</section>
</div>
<span class="qa-anchor" id="q-278-a-17"></span><span class="qa-anchor" id="q-278-a-08"></span><span class="qa-anchor" id="q-278-a-09"></span><span class="qa-anchor" id="q-278-a-10"></span><span class="qa-anchor" id="q-278-a-11"></span><span class="qa-anchor" id="q-278-a-12"></span><span class="qa-anchor" id="q-278-a-13"></span><span class="qa-anchor" id="q-278-a-14"></span><span class="qa-anchor" id="q-278-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-pointers">Base 2.4 §4.2.1, 4.3.1–4.3.2 (PCIe-applicable layouts)</a> · <a href="#ref-sgls">Base 2.4 §5.2.14.2.1 (SGLS)</a> · <a href="#ref-retirement">PCIe Transport 1.4 §3.4 (Command Related Resource Retirement)</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-create">Base 2.4 §5.3.1–5.3.2</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-279" data-question="279" data-answer-kind="fields"><h2><a class="qa-qid" href="#q-279">Q279</a> What alignment rules apply to PRPs and lists?</h2>
<p class="qa-prompt">Explain the units and encoding, then work through one set of values.</p>
<details class="qa-answer" id="q-279-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-279-a-01">Data and list starts have different alignment rules; not every pointer must be 4 KiB aligned.</p><div class="qa-sections">
<section class="qa-section" id="q-279-s-01" data-answer-section="1"><h3><span>1.</span> Establish the source and scope</h3>
<span class="qa-anchor" id="q-279-a-02"></span><p>Apply selected MPS and pointer role, not an assumed OS page size.</p>
<span class="qa-anchor" id="q-279-a-03"></span><p>Identify first data, first list pointer, list data entry or chained-list pointer.</p>
</section>
<section class="qa-section" id="q-279-s-02" data-answer-section="2"><h3><span>2.</span> Fields, units and worked interpretation</h3>
<span class="qa-anchor" id="q-279-a-04"></span><p>Ordinary first data is Dword aligned; the first list pointer is Qword aligned with possible page offset; later data and list pages are page aligned.</p>
<span class="qa-anchor" id="q-279-a-05"></span><p>Check alignment and remaining capacity of the first list page.</p>
<span class="qa-anchor" id="q-279-a-06"></span><p>A first list starting at 4080 within a 4 KiB page has two slots, with the last used for linkage if needed.</p>
</section>
<section class="qa-section" id="q-279-s-03" data-answer-section="3"><h3><span>3.</span> Conditions that change the interpretation</h3>
<span class="qa-anchor" id="q-279-a-07"></span><p>Low-two-bit violations may produce PRP Offset Invalid or must be treated as cleared; nonzero later-page offsets should produce that error.</p>
<span class="qa-anchor" id="q-279-a-16"></span><p>Permitted controller tolerance does not remove host alignment obligations.</p>
</section>
</div>
<span class="qa-anchor" id="q-279-a-17"></span><span class="qa-anchor" id="q-279-a-08"></span><span class="qa-anchor" id="q-279-a-09"></span><span class="qa-anchor" id="q-279-a-10"></span><span class="qa-anchor" id="q-279-a-11"></span><span class="qa-anchor" id="q-279-a-12"></span><span class="qa-anchor" id="q-279-a-13"></span><span class="qa-anchor" id="q-279-a-14"></span><span class="qa-anchor" id="q-279-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-pointers">Base 2.4 §4.2.1, 4.3.1–4.3.2 (PCIe-applicable layouts)</a> · <a href="#ref-sgls">Base 2.4 §5.2.14.2.1 (SGLS)</a> · <a href="#ref-retirement">PCIe Transport 1.4 §3.4 (Command Related Resource Retirement)</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-create">Base 2.4 §5.3.1–5.3.2</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-280" data-question="280" data-answer-kind="error"><h2><a class="qa-qid" href="#q-280">Q280</a> Do zero, invalid or broken-chain PRPs have one universal error?</h2>
<p class="qa-prompt">Distinguish failure conditions before deciding whether a particular response is required.</p>
<details class="qa-answer" id="q-280-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-280-a-01">Zero is an address value, not a universal NVMe null pointer; accessibility depends on memory mapping.</p><div class="qa-sections">
<section class="qa-section" id="q-280-s-01" data-answer-section="1"><h3><span>1.</span> Distinguish the failure conditions</h3>
<span class="qa-anchor" id="q-280-a-02"></span><p>Separate format, coverage and actual transfer failures.</p>
<span class="qa-anchor" id="q-280-a-04"></span><p>Invalid offsets differ from transfer failures; address zero alone does not establish either result.</p>
<span class="qa-anchor" id="q-280-a-07"></span><p>No unique CQE is defined for every malformed chain or inaccessible address, especially if communication fails.</p>
</section>
<section class="qa-section" id="q-280-s-02" data-answer-section="2"><h3><span>2.</span> Establish the cause from evidence</h3>
<span class="qa-anchor" id="q-280-a-03"></span><p>Check MPS, pointer roles, required pages and accessible memory ranges.</p>
<span class="qa-anchor" id="q-280-a-05"></span><p>Isolate one change from a valid baseline and inspect the complete required address coverage.</p>
</section>
<section class="qa-section" id="q-280-s-03" data-answer-section="3"><h3><span>3.</span> Outcome and follow-up checks</h3>
<span class="qa-anchor" id="q-280-a-06"></span><p>A valid accessible layout can succeed, and reserved PRP2 zero is not a missing page.</p>
<span class="qa-anchor" id="q-280-a-16"></span><p>Preserve SQE, list contents and mapping before host changes obscure evidence.</p>
<span class="qa-anchor" id="q-280-a-17"></span><p>First establish that the command actually uses the pointer.</p>
</section>
</div>
<span class="qa-anchor" id="q-280-a-08"></span><span class="qa-anchor" id="q-280-a-09"></span><span class="qa-anchor" id="q-280-a-10"></span><span class="qa-anchor" id="q-280-a-11"></span><span class="qa-anchor" id="q-280-a-12"></span><span class="qa-anchor" id="q-280-a-13"></span><span class="qa-anchor" id="q-280-a-14"></span><span class="qa-anchor" id="q-280-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-pointers">Base 2.4 §4.2.1, 4.3.1–4.3.2 (PCIe-applicable layouts)</a> · <a href="#ref-sgls">Base 2.4 §5.2.14.2.1 (SGLS)</a> · <a href="#ref-retirement">PCIe Transport 1.4 §3.4 (Command Related Resource Retirement)</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-create">Base 2.4 §5.3.1–5.3.2</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-281" data-question="281" data-answer-kind="compare"><h2><a class="qa-qid" href="#q-281">Q281</a> How do SGL data, segment and last-segment descriptors work?</h2>
<p class="qa-prompt">Identify the key difference and one case where the alternatives are not interchangeable.</p>
<details class="qa-answer" id="q-281-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-281-a-01">Data blocks describe payload; segment descriptors describe another descriptor array.</p><div class="qa-sections">
<section class="qa-section" id="q-281-s-01" data-answer-section="1"><h3><span>1.</span> What differs</h3>
<span class="qa-anchor" id="q-281-a-02"></span><p>SGLs apply to supported PCIe I/O commands, not PCIe Admin commands.</p>
<span class="qa-anchor" id="q-281-a-04"></span><p>Descriptors are 16 bytes; types 0h/2h/3h distinguish data, segment and last segment, whose length describes descriptor bytes.</p>
</section>
<section class="qa-section" id="q-281-s-02" data-answer-section="2"><h3><span>2.</span> How to choose and verify</h3>
<span class="qa-anchor" id="q-281-a-03"></span><p>Establish SGL support and PSDT data/metadata layout.</p>
<span class="qa-anchor" id="q-281-a-05"></span><p>One block fits directly in SGL1; multiple blocks use a pointed descriptor array.</p>
<span class="qa-anchor" id="q-281-a-06"></span><p>Last Segment length 32 means two descriptors, not 32 payload bytes; payload length comes from those entries.</p>
</section>
<section class="qa-section" id="q-281-s-03" data-answer-section="3"><h3><span>3.</span> Where the comparison stops</h3>
<span class="qa-anchor" id="q-281-a-07"></span><p>Link descriptors must be last in their segment, and a last segment cannot contain another link.</p>
<span class="qa-anchor" id="q-281-a-16"></span><p>Account descriptor and payload bytes separately.</p>
</section>
</div>
<span class="qa-anchor" id="q-281-a-17"></span><span class="qa-anchor" id="q-281-a-08"></span><span class="qa-anchor" id="q-281-a-09"></span><span class="qa-anchor" id="q-281-a-10"></span><span class="qa-anchor" id="q-281-a-11"></span><span class="qa-anchor" id="q-281-a-12"></span><span class="qa-anchor" id="q-281-a-13"></span><span class="qa-anchor" id="q-281-a-14"></span><span class="qa-anchor" id="q-281-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-pointers">Base 2.4 §4.2.1, 4.3.1–4.3.2 (PCIe-applicable layouts)</a> · <a href="#ref-sgls">Base 2.4 §5.2.14.2.1 (SGLS)</a> · <a href="#ref-retirement">PCIe Transport 1.4 §3.4 (Command Related Resource Retirement)</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-create">Base 2.4 §5.3.1–5.3.2</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-282" data-question="282" data-answer-kind="error"><h2><a class="qa-qid" href="#q-282">Q282</a> How are SGL address, length, count and type errors distinguished?</h2>
<p class="qa-prompt">Distinguish failure conditions before deciding whether a particular response is required.</p>
<details class="qa-answer" id="q-282-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-282-a-01">Specific SGL errors identify different malformed structures rather than one generic invalid field.</p><div class="qa-sections">
<section class="qa-section" id="q-282-s-01" data-answer-section="1"><h3><span>1.</span> Distinguish the failure conditions</h3>
<span class="qa-anchor" id="q-282-a-02"></span><p>Data and metadata SGL length errors have distinct statuses.</p>
<span class="qa-anchor" id="q-282-a-04"></span><p>Segment addresses are Qword aligned with nonzero 16-byte-multiple lengths; zero-length data blocks are valid.</p>
<span class="qa-anchor" id="q-282-a-07"></span><p>Misplaced links require 0/0Eh; links inside a last segment 0/0Dh; unsupported types 0/11h; short data/metadata 0/0Fh or 0/10h.</p>
</section>
<section class="qa-section" id="q-282-s-02" data-answer-section="2"><h3><span>2.</span> Establish the cause from evidence</h3>
<span class="qa-anchor" id="q-282-a-03"></span><p>Check alignment, longer-length support, descriptor types and requested transfer length.</p>
<span class="qa-anchor" id="q-282-a-05"></span><p>Traverse boundaries, link position, type/subtype and aggregate data coverage.</p>
</section>
<section class="qa-section" id="q-282-s-03" data-answer-section="3"><h3><span>3.</span> Outcome and follow-up checks</h3>
<span class="qa-anchor" id="q-282-a-06"></span><p>The SGL must cover the request; LLDTS1 permits excess capacity without enlarging the transfer.</p>
<span class="qa-anchor" id="q-282-a-16"></span><p>Excess length with LLDTS0 should not cause abort; if it does, the corresponding length status is recommended. Alignment rules retain their may/should strengths.</p>
<span class="qa-anchor" id="q-282-a-17"></span><p>First establish a concrete structural violation rather than infer one from bad data.</p>
</section>
</div>
<span class="qa-anchor" id="q-282-a-08"></span><span class="qa-anchor" id="q-282-a-09"></span><span class="qa-anchor" id="q-282-a-10"></span><span class="qa-anchor" id="q-282-a-11"></span><span class="qa-anchor" id="q-282-a-12"></span><span class="qa-anchor" id="q-282-a-13"></span><span class="qa-anchor" id="q-282-a-14"></span><span class="qa-anchor" id="q-282-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-pointers">Base 2.4 §4.2.1, 4.3.1–4.3.2 (PCIe-applicable layouts)</a> · <a href="#ref-sgls">Base 2.4 §5.2.14.2.1 (SGLS)</a> · <a href="#ref-retirement">PCIe Transport 1.4 §3.4 (Command Related Resource Retirement)</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-create">Base 2.4 §5.3.1–5.3.2</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-283" data-question="283" data-answer-kind="lookup"><h2><a class="qa-qid" href="#q-283">Q283</a> How do Identify SGL capabilities constrain usage?</h2>
<p class="qa-prompt">Choose the interface and target, then identify the returned field that supports your conclusion.</p>
<details class="qa-answer" id="q-283-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-283-a-01">SGL capability includes alignment, optional types, metadata and excess-length support.</p><div class="qa-sections">
<section class="qa-section" id="q-283-s-01" data-answer-section="1"><h3><span>1.</span> Select the target and information</h3>
<span class="qa-anchor" id="q-283-a-02"></span><p>Capabilities remain constrained by transport and command type.</p>
<span class="qa-anchor" id="q-283-a-03"></span><p>SGLS low bits encode unsupported, unrestricted data-block alignment, or Dword alignment/granularity.</p>
<span class="qa-anchor" id="q-283-a-04"></span><p>LLDTS, SBBDS, MSDS/MBA and SDT respectively cover excess length, bit buckets, metadata and recommended count.</p>
</section>
<section class="qa-section" id="q-283-s-02" data-answer-section="2"><h3><span>2.</span> Query sequence and interpretation</h3>
<span class="qa-anchor" id="q-283-a-05"></span><p>Select valid PSDT and supported PCIe types/subtypes; do not import another transport’s offset format.</p>
<span class="qa-anchor" id="q-283-a-06"></span><p>Dword granularity requires four-byte address/length multiples, not page alignment.</p>
</section>
<section class="qa-section" id="q-283-s-03" data-answer-section="3"><h3><span>3.</span> Handle missing or inconsistent evidence</h3>
<span class="qa-anchor" id="q-283-a-07"></span><p>Exceeding SDT may reduce performance; it is not a universal rejection limit, and capsule-only limits do not define PCIe list limits.</p>
<span class="qa-anchor" id="q-283-a-16"></span><p>Legal behavior must match capabilities while retaining the Admin SGL prohibition.</p>
<span class="qa-anchor" id="q-283-a-17"></span><p>First decode individual SGLS fields instead of testing nonzero.</p>
</section>
</div>
<span class="qa-anchor" id="q-283-a-08"></span><span class="qa-anchor" id="q-283-a-09"></span><span class="qa-anchor" id="q-283-a-10"></span><span class="qa-anchor" id="q-283-a-11"></span><span class="qa-anchor" id="q-283-a-12"></span><span class="qa-anchor" id="q-283-a-13"></span><span class="qa-anchor" id="q-283-a-14"></span><span class="qa-anchor" id="q-283-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-pointers">Base 2.4 §4.2.1, 4.3.1–4.3.2 (PCIe-applicable layouts)</a> · <a href="#ref-sgls">Base 2.4 §5.2.14.2.1 (SGLS)</a> · <a href="#ref-retirement">PCIe Transport 1.4 §3.4 (Command Related Resource Retirement)</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-create">Base 2.4 §5.3.1–5.3.2</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-284" data-question="284" data-answer-kind="compare"><h2><a class="qa-qid" href="#q-284">Q284</a> How do pointer-format errors differ from Data Transfer Error?</h2>
<p class="qa-prompt">Identify the key difference and one case where the alternatives are not interchangeable.</p>
<details class="qa-answer" id="q-284-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-284-a-01">Pointer errors concern description validity; transfer errors concern moving data or metadata.</p><div class="qa-sections">
<section class="qa-section" id="q-284-s-01" data-answer-section="1"><h3><span>1.</span> What differs</h3>
<span class="qa-anchor" id="q-284-a-02"></span><p>Detection can occur during descriptor validation or memory access.</p>
<span class="qa-anchor" id="q-284-a-04"></span><p>Preserve layout and completion fields; Error Information PEL means Parameter Error Location, not Persistent Event Log.</p>
</section>
<section class="qa-section" id="q-284-s-02" data-answer-section="2"><h3><span>2.</span> How to choose and verify</h3>
<span class="qa-anchor" id="q-284-a-03"></span><p>Validate layout/coverage and memory lifetime at the time of access.</p>
<span class="qa-anchor" id="q-284-a-05"></span><p>Exclude premature buffer reclamation before diagnosing access to a valid address.</p>
<span class="qa-anchor" id="q-284-a-06"></span><p>Valid pointers and successful transfer do not alone prove the requested media operation succeeded.</p>
</section>
<section class="qa-section" id="q-284-s-03" data-answer-section="3"><h3><span>3.</span> Where the comparison stops</h3>
<span class="qa-anchor" id="q-284-a-07"></span><p>Data Transfer Error is 0/04h, distinct from pointer-format statuses; not every transfer failure is a host formatting error.</p>
<span class="qa-anchor" id="q-284-a-16"></span><p>Valid SGL portions may transfer before another descriptor fails; an error CQE does not prove an untouched buffer.</p>
</section>
</div>
<span class="qa-anchor" id="q-284-a-17"></span><span class="qa-anchor" id="q-284-a-08"></span><span class="qa-anchor" id="q-284-a-09"></span><span class="qa-anchor" id="q-284-a-10"></span><span class="qa-anchor" id="q-284-a-11"></span><span class="qa-anchor" id="q-284-a-12"></span><span class="qa-anchor" id="q-284-a-13"></span><span class="qa-anchor" id="q-284-a-14"></span><span class="qa-anchor" id="q-284-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-pointers">Base 2.4 §4.2.1, 4.3.1–4.3.2 (PCIe-applicable layouts)</a> · <a href="#ref-sgls">Base 2.4 §5.2.14.2.1 (SGLS)</a> · <a href="#ref-retirement">PCIe Transport 1.4 §3.4 (Command Related Resource Retirement)</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-create">Base 2.4 §5.3.1–5.3.2</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-285" data-question="285" data-answer-kind="diagnose"><h2><a class="qa-qid" href="#q-285">Q285</a> How are pointer errors correlated with completion and Error Information?</h2>
<p class="qa-prompt">Separate available evidence from missing information before judging conformance.</p>
<details class="qa-answer" id="q-285-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-285-a-01">Correlation identifies the original pointer or range requiring correction.</p><div class="qa-sections">
<section class="qa-section" id="q-285-s-01" data-answer-section="1"><h3><span>1.</span> Preserve the evidence first</h3>
<span class="qa-anchor" id="q-285-a-02"></span><p>Match controller, queue lifetime and SQID/CID; reusable identifiers alone are insufficient.</p>
<span class="qa-anchor" id="q-285-a-03"></span><p>Preserve status and auxiliary bits before reading applicable error information.</p>
<span class="qa-anchor" id="q-285-a-04"></span><p>Error count, command identity, status and parameter location help correlation, including invalid/unspecified location encodings.</p>
</section>
<section class="qa-section" id="q-285-s-02" data-answer-section="2"><h3><span>2.</span> Work through the possible causes</h3>
<span class="qa-anchor" id="q-285-a-17"></span><p>First preserve the original command/list before retry overwrites them.</p>
<span class="qa-anchor" id="q-285-a-05"></span><p>Correlate identity/status before byte/bit locations; list-memory errors need not identify a unique SQE bit.</p>
</section>
<section class="qa-section" id="q-285-s-03" data-answer-section="3"><h3><span>3.</span> Decide what the evidence supports</h3>
<span class="qa-anchor" id="q-285-a-06"></span><p>A matched record connects original fields, violated conditions and returned status.</p>
<span class="qa-anchor" id="q-285-a-07"></span><p>More 0 does not prohibit an entry, not every error requires one, and DNR0 does not justify reusing a malformed list.</p>
<span class="qa-anchor" id="q-285-a-16"></span><p>Overwritten or reset-cleared history limits evidence rather than proving validity.</p>
</section>
<section class="qa-section" id="q-285-s-04" data-answer-section="4"><h3><span>4.</span> Correlate error completions and records</h3>
<span class="qa-anchor" id="q-285-a-08"></span><p>For a CQE, DNR=1 means the identical command is expected to fail if resubmitted to any controller in this subsystem; DNR=0 means it may succeed. <a class="qa-rule-link" href="#common-command-8">Read the complete conditions in this volume</a></p>
<span class="qa-anchor" id="q-285-a-10"></span><p>A successful CQE does not require a new Error Information entry. <a class="qa-rule-link" href="#common-command-10">Read the complete conditions in this volume</a></p>
</section>
</div>
<span class="qa-anchor" id="q-285-a-09"></span><span class="qa-anchor" id="q-285-a-11"></span><span class="qa-anchor" id="q-285-a-12"></span><span class="qa-anchor" id="q-285-a-13"></span><span class="qa-anchor" id="q-285-a-14"></span><span class="qa-anchor" id="q-285-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-pointers">Base 2.4 §4.2.1, 4.3.1–4.3.2 (PCIe-applicable layouts)</a> · <a href="#ref-sgls">Base 2.4 §5.2.14.2.1 (SGLS)</a> · <a href="#ref-retirement">PCIe Transport 1.4 §3.4 (Command Related Resource Retirement)</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-create">Base 2.4 §5.3.1–5.3.2</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<section id="common-rules" class="qa-common"><h2>Shared rules linked from the answers</h2><p>Each shared mechanism is explained in full once in this volume. Use browser Back to return to the question; explicit command or feature exceptions take precedence.</p>
<article id="common-command-8"><h3>Command completion, events and records · How are DNR and More set?</h3><p>For a CQE, DNR=1 means the identical command is expected to fail if resubmitted to any controller in this subsystem; DNR=0 means it may succeed. Do not assign DNR=1 solely from an error name unless that condition mandates it. More=1 identifies additional information for this command in the Error Information Log. DNR should be zero when SCT=SC=0.</p></article>
<article id="common-command-10"><h3>Command completion, events and records · Are Error Information or other logs updated?</h3><p>A successful CQE does not require a new Error Information entry. For an error with More=1, read LID 01h and correlate SQID, CID and Error Count; not every unsuccessful CQE requires a new entry. Re-read the interfaces named in this question for the state the operation changes.</p></article>
</section>
<section id="source-index"><h2>Source locations and existing figure guides</h2><p>Base printed page = PDF page−26; the other two use identical numbers. Locations follow the supplied PDF body and retain figure numbers. Shared pages contribute only the relevant definitions, excluding Fabrics and PCIe link/packet content.</p><ul class="qa-references">
<li id="ref-reset"><strong>Base 2.4 · §3.7.1–3.7.4</strong><br>Printed pages 120–124 · PDF 146–150</li>
<li id="ref-pointers"><strong>Base 2.4 · §4.2.1, 4.3.1–4.3.2 (PCIe-applicable layouts)</strong><br>Printed pages 140–142, 158–164 · PDF 166–168, 184–190 · Figure 93, 110–122</li>
<li id="ref-status"><strong>Base 2.4 · §4.2.3</strong><br>Printed pages 145–155 · PDF 171–181 · Figure 101–105</li>
<li id="ref-aer"><strong>Base 2.4 · §5.2.2</strong><br>Printed pages 183–190 · PDF 209–216 · Figure 150–156</li>
<li id="ref-error"><strong>Base 2.4 · §5.2.13.1.2</strong><br>Printed pages 218–220 · PDF 244–246 · Figure 212</li>
<li id="ref-pel"><strong>Base 2.4 · §5.2.13.1.14 (header, reset, hardware, Set Feature events)</strong><br>Printed pages 244–256, 258, 262–264 · PDF 270–282, 284, 288–290 · Figure 232–244, 246, 252–253</li>
<li id="ref-sgls"><strong>Base 2.4 · §5.2.14.2.1 (SGLS)</strong><br>Printed pages 377–378 · PDF 403–404 · Figure 338</li>
<li id="ref-create"><strong>Base 2.4 · §5.3.1–5.3.2</strong><br>Printed pages 527–531 · PDF 553–557 · Figure 571–579</li>
<li id="ref-retirement"><strong>PCIe Transport 1.4 · §3.4 (Command Related Resource Retirement)</strong><br>Printed pages 13 · PDF 13</li>
</ul><h3>When you need a field guide</h3><p>Existing figure explanations have canonical locations; use these links instead of duplicating the same guide.</p><ul>
<li><a href="/nvme/figure-reference/command/en/#figure-b101">Base 2.4 Figure 101 · Completion Queue Entry: Status Field</a></li>
<li><a href="/nvme/figure-reference/command/en/#figure-b104">Base 2.4 Figure 104 · Status Code – Command Specific Status Values</a></li>
<li><a href="/nvme/figure-reference/identify/en/#figure-b338">Base 2.4 Figure 338 · Identify – Identify Controller Data Structure, I/O Command Set Independent</a></li>
<li><a href="/nvme/figure-reference/command/en/#figure-b93">Base 2.4 Figure 93 · Common Command Format</a></li>
</ul><details><summary>Original documents used</summary><ul class="qr-sources">
<li>NVM Express Base Specification · Revision 2.4 · 2026-07-31<br><code>NVM-Express-Base-Specification-Revision-2.4-Ratified-2026.07.31.pdf</code></li>
<li>NVM Express NVM Command Set Specification · Revision 1.3 · 2026-07-31<br><code>NVM-Express-NVM-Command-Set-Specification-Revision-1.3-Ratified-2026.07.31.pdf</code></li>
<li>NVM Express NVMe over PCIe Transport Specification · Revision 1.4 · 2026-07-31<br><code>NVM-Express-NVMe-over-PCIe-Transport-Specification-Revision-1.4-Ratified-2026.07.31.pdf</code></li>
</ul></details></section>
</main>
<nav class="qr-top" aria-label="Bank and editions"><a href="#content">Skip to content</a><a href="/nvme/question-bank/en/">Question index</a><a href="/nvme/question-bank/pointers/zh-tw/">繁體中文</a><a href="/DOCS/nvme-question-bank/pointers.html">Chinese tutorial HTML</a></nav>
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
