---
layout: post
title: "NVMe Self-Study Bank: Data I/O: size, persistence and integrity"
date: 2026-10-03 00:00:00 +0800
categories: [nvme]
permalink: /nvme/question-bank/data-io/en/
lang: en
nvme_quickref: true
nvme_qa: true
---

<div class="nvme-quickref nvme-qa">
<nav class="qr-top" aria-label="Bank and editions"><a href="#content">Skip to content</a><a href="/nvme/question-bank/en/">Question index</a><a href="/nvme/question-bank/data-io/zh-tw/">繁體中文</a><a href="/DOCS/nvme-question-bank/data-io.html">Chinese tutorial HTML</a></nav>
<main id="content"><p class="qr-eyebrow">BASE 2.4 / NVM 1.3 / PCIe 1.4 · Q1–328</p>
<header><p class="qa-range">Q321–Q328</p><h1>Data I/O: size, persistence and integrity</h1><p class="qr-intro">This supplement develops data-I/O reasoning not previously covered in depth: request validity, completion guarantees, content verification and partial failure effects. Derive answers from concrete field values while linking back to existing feature, queue and pointer lessons.</p><p>Practice first, then reveal the explanation. Each question uses the prose, field interpretation, comparison or flow that suits it. All numerical examples are hypothetical. Status is written SCT/SC; h indicates hexadecimal.</p></header>
<aside class="qa-glossary"><h2>Terms used in this volume</h2><dl><dt>Controller / namespace</dt><dd>A controller receives commands and manages access. A namespace is a logical storage space that commands can address. An NVM subsystem contains controllers and nonvolatile storage resources.</dd><dt>SQ / CQ / SQE / CQE</dt><dd>Submission and Completion Queues carry command entries (SQEs) and completion entries (CQEs). QID identifies a queue, CID distinguishes outstanding commands in one SQ, and NSID identifies a namespace.</dd><dt>Register / Identify / Feature / Log</dt><dd>A register exposes control or state. Identify queries capabilities and attributes; features query or configure operation; log pages report specific state or records. FID, LID, CNS and CSI select features, logs, Identify structures and command sets.</dd><dt>index / offset / zero-based</dt><dd>An index selects an entry, usually starting at 0; an offset measures distance from an origin in specified units. A zero-based count encodes count−1, but not every zero-valued field is a count. A Dword is 4 bytes; a byte is 8 bits.</dd><dt>Scope / reset / retention</dt><dd>Scope names the affected objects; retention means preserving state. Controller Reset (clearing CC.EN) is one form of Controller Level Reset, or CLR. Different CLR triggers can retain different registers.</dd></dl></aside>
<section id="overview" class="qa-overview"><h2>Choose the claim before choosing the command</h2><p class="qa-takeaway">Request validity, content correctness, persistence and atomicity are separate claims; one success cannot prove all four.</p>
<div class="qr-table" tabindex="0" role="region" aria-label="Horizontally scrollable comparison table"><table><thead><tr><th scope="col">Question to establish</th><th scope="col">Evidence to combine</th><th scope="col">Easily missed condition</th></tr></thead><tbody><tr><td>Is the request range valid?</td><td>MDTS, MPSMIN, NLB, NSZE, transferred format</td><td>NLB+1 and metadata accounting</td></tr><tr><td>Is completed data persistent?</td><td>WCE, FUA, Flush scope and timing</td><td>Whether the Write completed before Flush submission</td></tr><tr><td>Can interruption leave a partial update?</td><td>Effective atomic units, MAM, boundaries and LBAs</td><td>Normal and power-fail atomicity differ</td></tr><tr><td>Does readable mean correct?</td><td>Read, Compare, Verify and PI conditions</td><td>Verify does not compare application expectations</td></tr><tr><td>What changed before failure?</td><td>Copy DW0, destination readback, source snapshot</td><td>DW0=0 does not prove an untouched destination</td></tr></tbody></table></div>
<p><strong>Worked interpretation: </strong>In the example, Write A succeeds before Flush is submitted for the same namespace. Successful Flush then supplies the covered persistence guarantee. Submitting both concurrently does not let an earlier Flush success cover an unfinished A; timing, not success-counting, is decisive.</p>
<p class="qa-citations">Sources: <a href="#ref-flushdata">Base 2.4 §7.2–7.2.1</a> · <a href="#ref-iofields">NVM Command Set 1.3 §3.3.4, 3.3.6 (data pointers, SLBA, NLB, FUA and completion)</a> · <a href="#ref-atomicdata">NVM Command Set 1.3 §2.1.4–2.1.4.6</a> · <a href="#ref-verifydata">NVM Command Set 1.3 §3.3.5–3.3.5.1</a> · <a href="#ref-copydata">NVM Command Set 1.3 §3.3.2–3.3.2.3, 3.3.2.5 (Formats 0h/1h; cross-namespace formats only for contrast)</a></p>
</section>
<div class="qa-controls" hidden><label>Search this page <input type="search" id="qa-search" placeholder="Question number, field or keyword"></label><button type="button" data-expand="true">Expand all answers</button><button type="button" data-expand="false">Collapse all answers</button><output id="qa-count" aria-live="polite"></output></div>
<section id="question-index"><h2>Questions in this volume</h2><ol class="qa-index">
<li><a href="#q-321">Q321 · Is a Read/Write length valid across MDTS, NLB and namespace bounds?</a></li>
<li><a href="#q-322">Q322 · Does successful Write imply power-loss persistence, and what do Flush and FUA guarantee?</a></li>
<li><a href="#q-323">Q323 · Why can a small Write lose whole-command atomicity when it crosses a boundary?</a></li>
<li><a href="#q-324">Q324 · What do successful Read, Compare and Verify actually prove?</a></li>
<li><a href="#q-325">Q325 · Must reads return zero after Write Zeroes or Deallocate?</a></li>
<li><a href="#q-326">Q326 · Why did PI checking miss an error? A Type 1, 16-bit Guard example</a></li>
<li><a href="#q-327">Q327 · What does CQE.DW0 establish after a Copy failure?</a></li>
<li><a href="#q-328">Q328 · Does a read failure after Write Uncorrectable prove damaged media?</a></li>
</ol></section>
<article class="qa-question" id="q-321" data-question="321" data-answer-kind="fields"><h2><a class="qa-qid" href="#q-321">Q321</a> Is a Read/Write length valid across MDTS, NLB and namespace bounds?</h2>
<p class="qa-prompt">Explain the units and encoding, then work through one set of values.</p>
<details class="qa-answer" id="q-321-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-321-a-01">Validate block count, host-transfer bytes and the final namespace LBA separately. A PRP list capable of describing the buffer does not establish a legal transfer size.</p><div class="qa-sections">
<section class="qa-section" id="q-321-s-01" data-answer-section="1"><h3><span>1.</span> Establish the source and scope</h3>
<span class="qa-anchor" id="q-321-a-02"></span><p>Consider ordinary Read/Write without other command extensions. NSID selects the namespace; MDTS limits host/controller transfer size while NSZE bounds LBA addresses.</p>
<span class="qa-anchor" id="q-321-a-03"></span><p>Read MDTS, CTRATT.MEM, CAP.MPSMIN, NSZE and the selected LBA format, including LBADS/MS and metadata layout. A nonzero MDTS gives 2^MDTS × 2^(12+MPSMIN) bytes, not a limit based on current CC.MPS.</p>
</section>
<section class="qa-section" id="q-321-s-02" data-answer-section="2"><h3><span>2.</span> Fields, units and worked interpretation</h3>
<span class="qa-anchor" id="q-321-a-04"></span><p>SLBA is the starting address, NLB+1 is the block count, and SLBA+NLB is the final LBA. Each data block has 2^LBADS bytes. Interleaved metadata counts toward MDTS when MEM=0 and is excluded when MEM=1.</p>
<span class="qa-anchor" id="q-321-a-05"></span><p>Fix the namespace format, validate the LBA range, calculate transfer bytes, then construct pointers. With hypothetical MPSMIN=0, MDTS=5, 4096-byte data, 8-byte interleaved metadata without PI and MEM=0, NLB=31 requires 131328 bytes rather than 131072; ignoring metadata misses 256 bytes.</p>
<span class="qa-anchor" id="q-321-a-06"></span><p>Under that example, 31 blocks require 127224 bytes and encode NLB=30. This satisfies MDTS only; namespace access, pointers and any PI must also be valid for successful completion.</p>
</section>
<section class="qa-section" id="q-321-s-03" data-answer-section="3"><h3><span>3.</span> Conditions that change the interpretation</h3>
<span class="qa-anchor" id="q-321-a-07"></span><p>Exceeding MDTS requires Invalid Field (0/02h); exceeding namespace bounds uses LBA Out of Range (0/80h). NSZE=1024, SLBA=1000 and NLB=31 end at LBA1031 beyond 1023. Isolate one invalid condition when testing an exact status.</p>
<span class="qa-anchor" id="q-321-a-16"></span><p>MDTS=0 removes this particular limit, not NLB encoding, namespace bounds or command-specific limits. Do not apply MDTS directly to Verify, Write Zeroes or Write Uncorrectable, which do not transfer host payload data.</p>
</section>
</div>
<span class="qa-anchor" id="q-321-a-17"></span><span class="qa-anchor" id="q-321-a-08"></span><span class="qa-anchor" id="q-321-a-09"></span><span class="qa-anchor" id="q-321-a-10"></span><span class="qa-anchor" id="q-321-a-11"></span><span class="qa-anchor" id="q-321-a-12"></span><span class="qa-anchor" id="q-321-a-13"></span><span class="qa-anchor" id="q-321-a-14"></span><span class="qa-anchor" id="q-321-a-15"></span>
<p class="qa-related">Related mechanisms: <a href="/nvme/question-bank/identify/en/#q-049">Q49</a> · <a href="/nvme/question-bank/pointers/en/#q-276">Q276</a> · <a href="/nvme/question-bank/pointers/en/#q-279">Q279</a> · <a href="/nvme/question-bank/data-io/en/#q-326">Q326</a></p>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-cap">Base 2.4 §3.1.4 (CAP, VS)</a> · <a href="#ref-pointers">Base 2.4 §4.2.1, 4.3.1–4.3.2 (PCIe-applicable layouts)</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-idns">NVM Command Set 1.3 §4.1.5.1–4.1.5.4</a> · <a href="#ref-iofields">NVM Command Set 1.3 §3.3.4, 3.3.6 (data pointers, SLBA, NLB, FUA and completion)</a> · <a href="#ref-mediaerrors">Base 2.4 §4.2.3 (Media and Data Integrity Errors only)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-322" data-question="322" data-answer-kind="process"><h2><a class="qa-qid" href="#q-322">Q322</a> Does successful Write imply power-loss persistence, and what do Flush and FUA guarantee?</h2>
<p class="qa-prompt">Order the actions and identify which completion must precede the next action.</p>
<details class="qa-answer" id="q-322-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-322-a-01">Write success completes the command, but enabled volatile caching may retain the data. Persistence requires the applicable nonvolatile-storage guarantee; ordinary successful readback or a CQE alone is insufficient.</p><div class="qa-sections">
<section class="qa-section" id="q-322-s-01" data-answer-section="1"><h3><span>1.</span> Prepare the operation</h3>
<span class="qa-anchor" id="q-322-a-02"></span><p>Write FUA applies to that command’s data and metadata. Flush covers commands for its namespace completed by the controller before Flush submission; it does not automatically order all still-running commands.</p>
<span class="qa-anchor" id="q-322-a-03"></span><p>Check VWC.VWCP, current FID 06h.WCE, VWC.FB broadcast support and applicable namespace VWCNP. Controller-wide cache presence does not imply a cache for every namespace.</p>
<span class="qa-anchor" id="q-322-a-04"></span><p>Write FUA=1 commits its data and metadata before completion; FUA=0 adds no requirement. Flush selects scope with NSID and has reserved command-specific fields. FB=11b permits broadcast Flush over namespaces attached to the submitting controller.</p>
</section>
<section class="qa-section" id="q-322-s-02" data-answer-section="2"><h3><span>2.</span> Sequence and completion conditions</h3>
<span class="qa-anchor" id="q-322-a-05"></span><p>For a batch, wait for the target Writes to succeed, submit Flush for the correct NSID and wait for its success. Concurrently submitting Write A and Flush does not establish that an earlier Flush completion covers A. Alternatively, use FUA=1 on each Write and await each success.</p>
<span class="qa-anchor" id="q-322-a-06"></span><p>Successful Flush makes covered data persistent. Without a present/enabled volatile cache it has no effect and must succeed when no Sanitize is in progress; this is not an unsupported-Flush error.</p>
</section>
<section class="qa-section" id="q-322-s-03" data-answer-section="3"><h3><span>3.</span> Handle unmet conditions</h3>
<span class="qa-anchor" id="q-322-a-07"></span><p>Broadcast Flush with FB=10b requires Invalid Namespace or Format (0/0Bh). Base 2.4 controllers cannot use the old FB=00b undefined broadcast behavior. Sanitize in progress has separate command rules.</p>
<span class="qa-anchor" id="q-322-a-16"></span><p>FUA/Flush do not enlarge atomic write units. Atomicity constrains interrupted or concurrent data combinations; persistence constrains post-success loss of committed data. Correlate timing, WCE, FUA and Flush coverage.</p>
</section>
</div>
<span class="qa-anchor" id="q-322-a-17"></span><span class="qa-anchor" id="q-322-a-08"></span><span class="qa-anchor" id="q-322-a-09"></span><span class="qa-anchor" id="q-322-a-10"></span><span class="qa-anchor" id="q-322-a-11"></span><span class="qa-anchor" id="q-322-a-12"></span><span class="qa-anchor" id="q-322-a-13"></span><span class="qa-anchor" id="q-322-a-14"></span><span class="qa-anchor" id="q-322-a-15"></span>
<p class="qa-related">Related mechanisms: <a href="/nvme/question-bank/commands/en/#q-038">Q38</a> · <a href="/nvme/question-bank/commands/en/#q-039">Q39</a> · <a href="/nvme/question-bank/features/en/#q-060">Q60</a> · <a href="/nvme/question-bank/reset-shutdown/en/#q-182">Q182</a></p>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-flushdata">Base 2.4 §7.2–7.2.1</a> · <a href="#ref-vwc">Base 2.4 §5.2.30.1.4</a> · <a href="#ref-atomicdata">NVM Command Set 1.3 §2.1.4–2.1.4.6</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-idns">NVM Command Set 1.3 §4.1.5.1–4.1.5.4</a> · <a href="#ref-iofields">NVM Command Set 1.3 §3.3.4, 3.3.6 (data pointers, SLBA, NLB, FUA and completion)</a> · <a href="#ref-mediaerrors">Base 2.4 §4.2.3 (Media and Data Integrity Errors only)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-323" data-question="323" data-answer-kind="fields"><h2><a class="qa-qid" href="#q-323">Q323</a> Why can a small Write lose whole-command atomicity when it crosses a boundary?</h2>
<p class="qa-prompt">Explain the units and encoding, then work through one set of values.</p>
<details class="qa-answer" id="q-323-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-323-a-01">Atomicity depends on effective size, namespace atomicity mode and boundary alignment. Equal-length Writes with different starting LBAs can have different guarantees.</p><div class="qa-sections">
<section class="qa-section" id="q-323-s-01" data-answer-section="1"><h3><span>1.</span> Establish the source and scope</h3>
<span class="qa-anchor" id="q-323-a-02"></span><p>Normal atomicity constrains inter-command results; power-fail atomicity constrains old/new data after interruption by power failure or error. Neither is a substitute for post-success persistence.</p>
<span class="qa-anchor" id="q-323-a-03"></span><p>Check NSABP, MAM and FID 0Ah.DN. When namespace units are supported, a zero NAWUN/NAWUPF falls back to AWUN/AWUPF; nonzero values encode count−1. MAM distinguishes Single from Multiple Atomicity Mode, and DN can remove normal-atomicity requirements.</p>
</section>
<section class="qa-section" id="q-323-s-02" data-answer-section="2"><h3><span>2.</span> Fields, units and worked interpretation</h3>
<span class="qa-anchor" id="q-323-a-04"></span><p>NABSN/NABSPF define normal/power-fail boundary sizes: zero means no boundary, while nonzero encodings decode by adding one. NABO is an LBA offset, not a count. Decoded boundaries occur at NABO+y×size for nonnegative integer y.</p>
<span class="qa-anchor" id="q-323-a-05"></span><p>Assume NSABP=1, MAM=0, DN=0, baseline AWUN=AWUPF=0, NAWUN=7, NAWUPF=1, boundary encodings 15 and offset 0. The effective units are 8 and 2 blocks, with 16-block boundaries. LBAs 14–15 stay within one boundary region;15–16 cross LBA16.</p>
<span class="qa-anchor" id="q-323-a-06"></span><p>A normally completed Write reports Success; interruption atomicity additionally requires readback evidence. An interrupted 2-block Write at 14–15 must yield all old or all new data under the stated power-fail conditions. At 15–16 it lacks that whole 2-block guarantee. A valid Multiple Atomicity configuration instead makes each boundary-delimited subrange atomic, not the whole crossing command.</p>
</section>
<section class="qa-section" id="q-323-s-03" data-answer-section="3"><h3><span>3.</span> Conditions that change the interpretation</h3>
<span class="qa-anchor" id="q-323-a-07"></span><p>Exceeding an atomic unit or crossing a boundary does not universally require rejection of an ordinary Write. It can succeed with different guarantees; fused-operation Atomic Write Unit Exceeded rules are not universal Write rules.</p>
<span class="qa-anchor" id="q-323-a-16"></span><p>Rediscover namespace atomic fields after Format and use the new LBA size. Capture concurrency when testing normal atomicity. One intact readback does not establish a larger guarantee than advertised.</p>
</section>
</div>
<span class="qa-anchor" id="q-323-a-17"></span><span class="qa-anchor" id="q-323-a-08"></span><span class="qa-anchor" id="q-323-a-09"></span><span class="qa-anchor" id="q-323-a-10"></span><span class="qa-anchor" id="q-323-a-11"></span><span class="qa-anchor" id="q-323-a-12"></span><span class="qa-anchor" id="q-323-a-13"></span><span class="qa-anchor" id="q-323-a-14"></span><span class="qa-anchor" id="q-323-a-15"></span>
<p class="qa-related">Related mechanisms: <a href="/nvme/question-bank/features/en/#q-060">Q60</a> · <a href="/nvme/question-bank/data-io/en/#q-322">Q322</a></p>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-atomicdata">NVM Command Set 1.3 §2.1.4–2.1.4.6</a> · <a href="#ref-nvmfeat">NVM Command Set 1.3 §4.1.3.1–4.1.3.7</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-idns">NVM Command Set 1.3 §4.1.5.1–4.1.5.4</a> · <a href="#ref-iofields">NVM Command Set 1.3 §3.3.4, 3.3.6 (data pointers, SLBA, NLB, FUA and completion)</a> · <a href="#ref-mediaerrors">Base 2.4 §4.2.3 (Media and Data Integrity Errors only)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-324" data-question="324" data-answer-kind="compare"><h2><a class="qa-qid" href="#q-324">Q324</a> What do successful Read, Compare and Verify actually prove?</h2>
<p class="qa-prompt">Identify the key difference and one case where the alternatives are not interchangeable.</p>
<details class="qa-answer" id="q-324-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-324-a-01">Read returns data, Compare tests a host-supplied expected buffer, and Verify checks stored-information integrity without returning payload. Verify success does not establish equality with an application’s expected value.</p><div class="qa-sections">
<section class="qa-section" id="q-324-s-01" data-answer-section="1"><h3><span>1.</span> What differs</h3>
<span class="qa-anchor" id="q-324-a-02"></span><p>All select a namespace/range, but Compare consumes host data, Read fills a host buffer and Verify transfers no host payload. They therefore do not produce identical buffer evidence.</p>
<span class="qa-anchor" id="q-324-a-04"></span><p>SLBA/NLB select the range and PRCHK selects PI checks. Compare includes non-PI metadata in equality checks. Verify requires PRACT=0; FUA=1 commits associated cached data before verifying nonvolatile contents, without ordering other commands.</p>
</section>
<section class="qa-section" id="q-324-s-02" data-answer-section="2"><h3><span>2.</span> How to choose and verify</h3>
<span class="qa-anchor" id="q-324-a-03"></span><p>Discover opcode support/effects and Verify’s VSL/NVMVFYS rules. A nonzero VSL can be a recommended maximum under the advertised variant, not universally a rejection threshold. MDTS does not directly limit payload-free Verify.</p>
<span class="qa-anchor" id="q-324-a-05"></span><p>With valid data A at LBA100, wait for the Write, read back A, then compare against A and against different B. The latter should report Compare Failure. Verify may still succeed even if the application intended B, because it checks stored integrity rather than that expectation.</p>
<span class="qa-anchor" id="q-324-a-06"></span><p>Read success plus returned bytes establishes readback; Compare success establishes equality with its supplied data; Verify success establishes the requested integrity verification. Concurrent writes can invalidate comparisons across separate observations.</p>
</section>
<section class="qa-section" id="q-324-s-03" data-answer-section="3"><h3><span>3.</span> Where the comparison stops</h3>
<span class="qa-anchor" id="q-324-a-07"></span><p>Mismatch uses Compare Failure (2/85h), not Unrecovered Read Error (2/81h). Verify with nonzero PRACT requires Invalid Field (0/02h); detected PI failures have their own integrity statuses. Verify and Read need not report the same error for the same media problem.</p>
<span class="qa-anchor" id="q-324-a-16"></span><p>Data read or integrity-checked by Verify must contribute to SMART Data Units Read despite no host payload transfer. The counter represents defined work, not necessarily delivered bytes; account for units and rounding.</p>
</section>
<section class="qa-section" id="q-324-s-04" data-answer-section="4"><h3><span>4.</span> Evidence supplied by the log</h3>
<span class="qa-anchor" id="q-324-a-10"></span><p>Verify reads/integrity checks contribute to Data Units Read even without host payload transfer. Correlate failures through More/error-log rules; normal verification does not require an error entry.</p>
</section>
</div>
<span class="qa-anchor" id="q-324-a-17"></span><span class="qa-anchor" id="q-324-a-08"></span><span class="qa-anchor" id="q-324-a-09"></span><span class="qa-anchor" id="q-324-a-11"></span><span class="qa-anchor" id="q-324-a-12"></span><span class="qa-anchor" id="q-324-a-13"></span><span class="qa-anchor" id="q-324-a-14"></span><span class="qa-anchor" id="q-324-a-15"></span>
<p class="qa-related">Related mechanisms: <a href="/nvme/question-bank/identify/en/#q-050">Q50</a> · <a href="/nvme/question-bank/health/en/#q-198">Q198</a> · <a href="/nvme/question-bank/data-io/en/#q-326">Q326</a></p>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-comparedata">NVM Command Set 1.3 §3.3.1–3.3.1.1</a> · <a href="#ref-verifydata">NVM Command Set 1.3 §3.3.5–3.3.5.1</a> · <a href="#ref-smart">Base 2.4 §5.2.13.1.3</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-idns">NVM Command Set 1.3 §4.1.5.1–4.1.5.4</a> · <a href="#ref-iofields">NVM Command Set 1.3 §3.3.4, 3.3.6 (data pointers, SLBA, NLB, FUA and completion)</a> · <a href="#ref-mediaerrors">Base 2.4 §4.2.3 (Media and Data Integrity Errors only)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-325" data-question="325" data-answer-kind="compare"><h2><a class="qa-qid" href="#q-325">Q325</a> Must reads return zero after Write Zeroes or Deallocate?</h2>
<p class="qa-prompt">Identify the key difference and one case where the alternatives are not interchangeable.</p>
<details class="qa-answer" id="q-325-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-325-a-01">Write Zeroes requires zero-valued successful readback; Dataset Management Deallocate supplies a no-longer-needed-data attribute that the controller may choose not to act on. Neither success is proof of irreversible data sanitization.</p><div class="qa-sections">
<section class="qa-section" id="q-325-s-01" data-answer-section="1"><h3><span>1.</span> What differs</h3>
<span class="qa-anchor" id="q-325-a-02"></span><p>Compare range operations in one namespace, initially using ordinary Write Zeroes with NSZ=0. Whole-namespace NSZ=1 has extra requirements and is not implied by range-operation success.</p>
<span class="qa-anchor" id="q-325-a-04"></span><p>Write Zeroes NLB and Dataset Management NR are zero-based; each Dataset Management range length is a one-based count. DEAC requests deallocation. Decode each field according to its own definition.</p>
</section>
<section class="qa-section" id="q-325-s-02" data-answer-section="2"><h3><span>2.</span> How to choose and verify</h3>
<span class="qa-anchor" id="q-325-a-03"></span><p>Check command support, DLFEAT.DRB, NSFEAT.DAE and current FID 05h.DULBE. DRB defines deallocated read values, DAE advertises the error capability, and DULBE enables that error.</p>
<span class="qa-anchor" id="q-325-a-05"></span><p>Assume DRB=001b and DAE=1. After valid Write Zeroes, deallocated blocks with DULBE=1 produce Deallocated or Unwritten Logical Block. With DULBE=0, successful readback is zero. DEAC=0 does not prohibit deallocation when the required zero-read behavior is preserved.</p>
<span class="qa-anchor" id="q-325-a-06"></span><p>A DULBE error after Write Zeroes is not by itself a zeroing failure. Dataset Management success likewise does not prove every range was deallocated; distinguish processing rules from actual effects.</p>
</section>
<section class="qa-section" id="q-325-s-03" data-answer-section="3"><h3><span>3.</span> Where the comparison stops</h3>
<span class="qa-anchor" id="q-325-a-07"></span><p>Supported/enabled DULBE requires 2/87h for applicable reads of deallocated/unwritten blocks. Write Zeroes with NSZ=1 but DEAC=0, or without zero-valued deallocated reads, requires Invalid Field (0/02h).</p>
<span class="qa-anchor" id="q-325-a-16"></span><p>With DULBE disabled, genuinely deallocated blocks return all 00h or allFFh according to DRB. DRB=000b permits either, but a block’s returned value must remain deterministic until a write. Read/Verify do not allocate it.</p>
</section>
</div>
<span class="qa-anchor" id="q-325-a-17"></span><span class="qa-anchor" id="q-325-a-08"></span><span class="qa-anchor" id="q-325-a-09"></span><span class="qa-anchor" id="q-325-a-10"></span><span class="qa-anchor" id="q-325-a-11"></span><span class="qa-anchor" id="q-325-a-12"></span><span class="qa-anchor" id="q-325-a-13"></span><span class="qa-anchor" id="q-325-a-14"></span><span class="qa-anchor" id="q-325-a-15"></span>
<p class="qa-related">Related mechanisms: <a href="/nvme/question-bank/features/en/#q-064">Q64</a> · <a href="/nvme/question-bank/format-sanitize/en/#q-127">Q127</a></p>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-deallocateddata">NVM Command Set 1.3 §3.3.3–3.3.3.3, 3.3.8–3.3.8.2</a> · <a href="#ref-nvmfeat">NVM Command Set 1.3 §4.1.3.1–4.1.3.7</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-idns">NVM Command Set 1.3 §4.1.5.1–4.1.5.4</a> · <a href="#ref-iofields">NVM Command Set 1.3 §3.3.4, 3.3.6 (data pointers, SLBA, NLB, FUA and completion)</a> · <a href="#ref-mediaerrors">Base 2.4 §4.2.3 (Media and Data Integrity Errors only)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-326" data-question="326" data-answer-kind="fields"><h2><a class="qa-qid" href="#q-326">Q326</a> Why did PI checking miss an error? A Type 1, 16-bit Guard example</h2>
<p class="qa-prompt">Explain the units and encoding, then work through one set of values.</p>
<details class="qa-answer" id="q-326-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-326-a-01">PI protects integrity and block association, but formatting a namespace with PI does not enable every check on every command. Format, PRACT, PRCHK and special tag values determine actual processing.</p><div class="qa-sections">
<section class="qa-section" id="q-326-s-01" data-answer-section="1"><h3><span>1.</span> Establish the source and scope</h3>
<span class="qa-anchor" id="q-326-a-02"></span><p>Limit the example to Type 1,16-bit Guard, STS=0 and 8-byte PI, not 32/64-bit Guard layouts. Guard, Application Tag and Reference Tag occupy 2,2 and 4 metadata bytes respectively.</p>
<span class="qa-anchor" id="q-326-a-03"></span><p>DPC advertises protection capabilities, DPS selects the current protection type, and MS gives metadata size. Also establish the active PI format and STS; capabilities alone do not identify the current layout.</p>
</section>
<section class="qa-section" id="q-326-s-02" data-answer-section="2"><h3><span>2.</span> Fields, units and worked interpretation</h3>
<span class="qa-anchor" id="q-326-a-04"></span><p>PRCHK bits 2/1/0 select Guard/Application/Reference checks; PRACT controls passing, generation or removal. With reference-tag checking enabled, Type 1 ILBRT/EILBRT must match the relevant low SLBA bits. Application-tag mask bits set to 1 are compared; zero masks them.</p>
<span class="qa-anchor" id="q-326-a-05"></span><p>With hypothetical 4096-byte data, MS=8, PRACT=0 and PRCHK=111b, first use valid PI and avoid the FFFFh application-tag escape. Establish a valid baseline, then corrupt one Guard/Application/Reference field at a time while preserving other inputs.</p>
<span class="qa-anchor" id="q-326-a-06"></span><p>The valid baseline should complete successfully; PRACT determines which data/metadata Read returns. With MS equal to the 8-byte PI size, Write.PRACT=1 generates/appends PI without those host bytes and ignores PRCHK; Read.PRACT=1 checks as applicable, then strips PI before returning data. If MS exceeds PI size, the full metadata does not simply disappear from the host buffer.</p>
</section>
<section class="qa-section" id="q-326-s-03" data-answer-section="3"><h3><span>3.</span> Conditions that change the interpretation</h3>
<span class="qa-anchor" id="q-326-a-07"></span><p>Enabled, non-escaped check failures use Guard 2/82h, Application 2/83h or Reference 2/84h. With that check enabled, a Type 1 command ILBRT/EILBRT inconsistent with SLBA instead requires Invalid Protection Information (1/81h), distinct from bad stored tags.</p>
<span class="qa-anchor" id="q-326-a-16"></span><p>Type 1/Type 2 Application Tag=FFFFh disables PI checks despite PRCHK. An intentionally bad Guard can therefore succeed because PRACT regenerates PI or a special tag suppresses checking, rather than because the controller omitted a required check.</p>
</section>
</div>
<span class="qa-anchor" id="q-326-a-17"></span><span class="qa-anchor" id="q-326-a-08"></span><span class="qa-anchor" id="q-326-a-09"></span><span class="qa-anchor" id="q-326-a-10"></span><span class="qa-anchor" id="q-326-a-11"></span><span class="qa-anchor" id="q-326-a-12"></span><span class="qa-anchor" id="q-326-a-13"></span><span class="qa-anchor" id="q-326-a-14"></span><span class="qa-anchor" id="q-326-a-15"></span>
<p class="qa-related">Related mechanisms: <a href="/nvme/question-bank/format-sanitize/en/#q-120">Q120</a> · <a href="/nvme/question-bank/pointers/en/#q-279">Q279</a> · <a href="/nvme/question-bank/pointers/en/#q-284">Q284</a></p>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-pidata">NVM Command Set 1.3 §2.1.5, 5.3.1.1 (STS=0), 5.3.2.1–5.3.2.2, 5.3.3</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-idns">NVM Command Set 1.3 §4.1.5.1–4.1.5.4</a> · <a href="#ref-iofields">NVM Command Set 1.3 §3.3.4, 3.3.6 (data pointers, SLBA, NLB, FUA and completion)</a> · <a href="#ref-mediaerrors">Base 2.4 §4.2.3 (Media and Data Integrity Errors only)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-327" data-question="327" data-answer-kind="fields"><h2><a class="qa-qid" href="#q-327">Q327</a> What does CQE.DW0 establish after a Copy failure?</h2>
<p class="qa-prompt">Explain the units and encoding, then work through one set of values.</p>
<details class="qa-answer" id="q-327-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-327-a-01">Copy assembles multiple source ranges into a consecutive destination without routing payload through the host. Failure may leave partial effects; its CQE does not provide transactional rollback.</p><div class="qa-sections">
<section class="qa-section" id="q-327-s-01" data-answer-section="1"><h3><span>1.</span> Establish the source and scope</h3>
<span class="qa-anchor" id="q-327-a-02"></span><p>Use a same-namespace Format 0h example. NSID selects the destination namespace and SDLBA its start; descriptor order determines destination placement. Cross-namespace Formats 2h/3h add rules beyond merely changing NSID.</p>
<span class="qa-anchor" id="q-327-a-03"></span><p>Discover Copy/descriptor support, MSRC, MSSRL and MCL. MSRC is a zero-based source-range count; MSSRL and MCL bound per-range and total block counts. Destination atomicity remains a separate constraint.</p>
</section>
<section class="qa-section" id="q-327-s-02" data-answer-section="2"><h3><span>2.</span> Fields, units and worked interpretation</h3>
<span class="qa-anchor" id="q-327-a-04"></span><p>Decode zero-based NR and source NLB before summing. NR=1 with source NLB values 3 and 1 describes 4+2 blocks. SDLBA=1000 places them at 1000–1003 and 1004–1005, not both at 1000.</p>
<span class="qa-anchor" id="q-327-a-05"></span><p>Validate ranges, nonoverlap and all three Copy limits, preserving source and old-destination data. On failure, DW0 identifies the lowest-numbered source entry not successfully copied, not a successful-block count or a guaranteed execution cursor.</p>
<span class="qa-anchor" id="q-327-a-06"></span><p>Successful Copy places all source content consecutively in descriptor order. Failure does not imply no changes: if ranges 0,1 and 3 succeed but 2 does not, DW0=2. It does not prove range 3 was untouched or range 2 had no partial effects. No destination writes requires DW0=0, but DW0=0 does not prove no writes.</p>
</section>
<section class="qa-section" id="q-327-s-03" data-answer-section="3"><h3><span>3.</span> Conditions that change the interpretation</h3>
<span class="qa-anchor" id="q-327-a-07"></span><p>Source-length/total-copy limit violations use 1/83h. Hosts should avoid overlap for Formats 0h/1h, but cannot universally demand Overlapping I/O Range there; Formats 2h/3h explicitly prohibit relevant overlap and require 1/87h. Fix descriptor format before testing status.</p>
<span class="qa-anchor" id="q-327-a-16"></span><p>Applicable NVM1.3 NVMCSA rules treat the destination write as one Write for atomicity, not as an unlimited atomic transaction. Before retrying, inspect destination effects, atomic subranges and source changes rather than treating DW0 as a safe resume cursor.</p>
</section>
</div>
<span class="qa-anchor" id="q-327-a-17"></span><span class="qa-anchor" id="q-327-a-08"></span><span class="qa-anchor" id="q-327-a-09"></span><span class="qa-anchor" id="q-327-a-10"></span><span class="qa-anchor" id="q-327-a-11"></span><span class="qa-anchor" id="q-327-a-12"></span><span class="qa-anchor" id="q-327-a-13"></span><span class="qa-anchor" id="q-327-a-14"></span><span class="qa-anchor" id="q-327-a-15"></span>
<p class="qa-related">Related mechanisms: <a href="/nvme/question-bank/recovery/en/#q-112">Q112</a> · <a href="/nvme/question-bank/data-io/en/#q-323">Q323</a></p>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-copydata">NVM Command Set 1.3 §3.3.2–3.3.2.3, 3.3.2.5 (Formats 0h/1h; cross-namespace formats only for contrast)</a> · <a href="#ref-atomicdata">NVM Command Set 1.3 §2.1.4–2.1.4.6</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-idns">NVM Command Set 1.3 §4.1.5.1–4.1.5.4</a> · <a href="#ref-iofields">NVM Command Set 1.3 §3.3.4, 3.3.6 (data pointers, SLBA, NLB, FUA and completion)</a> · <a href="#ref-mediaerrors">Base 2.4 §4.2.3 (Media and Data Integrity Errors only)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-328" data-question="328" data-answer-kind="concept"><h2><a class="qa-qid" href="#q-328">Q328</a> Does a read failure after Write Uncorrectable prove damaged media?</h2>
<p class="qa-prompt">Explain the mechanism in your own words and identify a common misconception.</p>
<details class="qa-answer" id="q-328-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-328-a-01">Write Uncorrectable deliberately marks logical blocks invalid so later reads fail. This is a requested logical state change; the resulting Unrecovered Read Error alone does not prove physical NAND damage.</p><div class="qa-sections">
<section class="qa-section" id="q-328-s-01" data-answer-section="1"><h3><span>1.</span> Mechanism and scope</h3>
<span class="qa-anchor" id="q-328-a-02"></span><p>The operation targets an LBA range rather than disabling the whole namespace. Other attached controllers can observe the invalid state, so account for concurrent writes.</p>
<span class="qa-anchor" id="q-328-a-04"></span><p>SLBA selects the start and zero-based NLB selects count. SLBA200/NLB1 targets blocks 200 and 201. No host Read/Write payload buffer carries an invalid marker; the command requests the state change.</p>
</section>
<section class="qa-section" id="q-328-s-02" data-answer-section="2"><h3><span>2.</span> Understand it through actions and results</h3>
<span class="qa-anchor" id="q-328-a-03"></span><p>Check command support, WUSL and NVMWUSV. With nonzero WUSL, variant 1 makes it a recommended maximum; variant 0 makes exceeding it a rejection condition. The command has no host payload, so MDTS is not its direct limit.</p>
<span class="qa-anchor" id="q-328-a-05"></span><p>Establish valid data, complete Write Uncorrectable, then read the marked range and an unmarked control range. A subsequent valid Write clears the invalid-block status; do not substitute Reset for that write.</p>
<span class="qa-anchor" id="q-328-a-06"></span><p>The marking command can succeed while subsequent reads require Unrecovered Read Error. A new write clears invalid status, permitting new-data readback absent other errors. Verify all three stages together.</p>
</section>
<section class="qa-section" id="q-328-s-03" data-answer-section="3"><h3><span>3.</span> Avoid a misleading conclusion</h3>
<span class="qa-anchor" id="q-328-a-07"></span><p>Subsequent read failure is 2/81h; the marking command need not fail. Exceeding effective WUSL with NVMWUSV=0 requires Invalid Field (0/02h), unlike variant 1’s advisory size.</p>
<span class="qa-anchor" id="q-328-a-16"></span><p>Correlate marking success, read failure and rewritten data with applicable logs/counters. Even when a read error contributes to relevant statistics, a known host-requested invalid mark is not by itself evidence of physical degradation.</p>
</section>
</div>
<span class="qa-anchor" id="q-328-a-17"></span><span class="qa-anchor" id="q-328-a-08"></span><span class="qa-anchor" id="q-328-a-09"></span><span class="qa-anchor" id="q-328-a-10"></span><span class="qa-anchor" id="q-328-a-11"></span><span class="qa-anchor" id="q-328-a-12"></span><span class="qa-anchor" id="q-328-a-13"></span><span class="qa-anchor" id="q-328-a-14"></span><span class="qa-anchor" id="q-328-a-15"></span>
<p class="qa-related">Related mechanisms: <a href="/nvme/question-bank/errors/en/#q-096">Q96</a> · <a href="/nvme/question-bank/health/en/#q-199">Q199</a></p>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-uncorrectabledata">NVM Command Set 1.3 §3.3.7–3.3.7.1</a> · <a href="#ref-atomicdata">NVM Command Set 1.3 §2.1.4–2.1.4.6</a> · <a href="#ref-smart">Base 2.4 §5.2.13.1.3</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-idns">NVM Command Set 1.3 §4.1.5.1–4.1.5.4</a> · <a href="#ref-iofields">NVM Command Set 1.3 §3.3.4, 3.3.6 (data pointers, SLBA, NLB, FUA and completion)</a> · <a href="#ref-mediaerrors">Base 2.4 §4.2.3 (Media and Data Integrity Errors only)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>

<section id="source-index"><h2>Source locations and existing figure guides</h2><p>Base printed page = PDF page−26; the other two use identical numbers. Locations follow the supplied PDF body and retain figure numbers. Shared pages contribute only the relevant definitions, excluding Fabrics and PCIe link/packet content.</p><ul class="qa-references">
<li id="ref-cap"><strong>Base 2.4 · §3.1.4 (CAP, VS)</strong><br>Printed pages 54–59 · PDF 80–85 · Figure 36–37</li>
<li id="ref-reset"><strong>Base 2.4 · §3.7.1–3.7.4</strong><br>Printed pages 120–124 · PDF 146–150</li>
<li id="ref-pointers"><strong>Base 2.4 · §4.2.1, 4.3.1–4.3.2 (PCIe-applicable layouts)</strong><br>Printed pages 140–142, 158–164 · PDF 166–168, 184–190 · Figure 93, 110–122</li>
<li id="ref-status"><strong>Base 2.4 · §4.2.3</strong><br>Printed pages 145–155 · PDF 171–181 · Figure 101–105</li>
<li id="ref-mediaerrors"><strong>Base 2.4 · §4.2.3 (Media and Data Integrity Errors only)</strong><br>Printed pages 154–155 · PDF 180–181 · Figure 107</li>
<li id="ref-aer"><strong>Base 2.4 · §5.2.2</strong><br>Printed pages 183–190 · PDF 209–216 · Figure 150–156</li>
<li id="ref-error"><strong>Base 2.4 · §5.2.13.1.2</strong><br>Printed pages 218–220 · PDF 244–246 · Figure 212</li>
<li id="ref-smart"><strong>Base 2.4 · §5.2.13.1.3</strong><br>Printed pages 220–225 · PDF 246–251 · Figure 213–214</li>
<li id="ref-pel"><strong>Base 2.4 · §5.2.13.1.14 (header, reset, hardware, Set Feature events)</strong><br>Printed pages 244–256, 258, 262–264 · PDF 270–282, 284, 288–290 · Figure 232–244, 246, 252–253</li>
<li id="ref-idctrl"><strong>Base 2.4 · §5.2.14.2.1</strong><br>Printed pages 340–387 · PDF 366–413 · Figure 338–341</li>
<li id="ref-vwc"><strong>Base 2.4 · §5.2.30.1.4</strong><br>Printed pages 464–465 · PDF 490–491 · Figure 471</li>
<li id="ref-flushdata"><strong>Base 2.4 · §7.2–7.2.1</strong><br>Printed pages 567 · PDF 593</li>
<li id="ref-atomicdata"><strong>NVM Command Set 1.3 · §2.1.4–2.1.4.6</strong><br>Printed pages 15–21 · PDF 15–21 · Figure 4–10</li>
<li id="ref-pidata"><strong>NVM Command Set 1.3 · §2.1.5, 5.3.1.1 (STS=0), 5.3.2.1–5.3.2.2, 5.3.3</strong><br>Printed pages 21–22, 131, 141–145, 151–152 · PDF 21–22, 131, 141–145, 151–152 · Figure 11–12, 155, 174–175</li>
<li id="ref-comparedata"><strong>NVM Command Set 1.3 · §3.3.1–3.3.1.1</strong><br>Printed pages 27–30 · PDF 27–30 · Figure 24, 26–27, 31</li>
<li id="ref-copydata"><strong>NVM Command Set 1.3 · §3.3.2–3.3.2.3, 3.3.2.5 (Formats 0h/1h; cross-namespace formats only for contrast)</strong><br>Printed pages 30–40, 43–44 · PDF 30–40, 43–44 · Figure 34–35, 39–40, 42–43</li>
<li id="ref-deallocateddata"><strong>NVM Command Set 1.3 · §3.3.3–3.3.3.3, 3.3.8–3.3.8.2</strong><br>Printed pages 44–48, 57–61 · PDF 44–48, 57–61 · Figure 45–47, 49, 83, 88–89</li>
<li id="ref-iofields"><strong>NVM Command Set 1.3 · §3.3.4, 3.3.6 (data pointers, SLBA, NLB, FUA and completion)</strong><br>Printed pages 48–51, 53–56 · PDF 48–51, 53–56 · Figure 53–54, 59, 68, 70–71, 76</li>
<li id="ref-verifydata"><strong>NVM Command Set 1.3 · §3.3.5–3.3.5.1</strong><br>Printed pages 51–53 · PDF 51–53 · Figure 61–62, 66</li>
<li id="ref-uncorrectabledata"><strong>NVM Command Set 1.3 · §3.3.7–3.3.7.1</strong><br>Printed pages 56–57 · PDF 56–57 · Figure 77–80</li>
<li id="ref-nvmfeat"><strong>NVM Command Set 1.3 · §4.1.3.1–4.1.3.7</strong><br>Printed pages 64–69 · PDF 64–69 · Figure 92–101</li>
<li id="ref-idns"><strong>NVM Command Set 1.3 · §4.1.5.1–4.1.5.4</strong><br>Printed pages 84–107 · PDF 84–107 · Figure 123–130</li>
</ul><h3>When you need a field guide</h3><p>Existing figure explanations have canonical locations; use these links instead of duplicating the same guide.</p><ul>
<li><a href="/nvme/figure-reference/command/en/#figure-b101">Base 2.4 Figure 101 · Completion Queue Entry: Status Field</a></li>
<li><a href="/nvme/figure-reference/command/en/#figure-b104">Base 2.4 Figure 104 · Status Code – Command Specific Status Values</a></li>
<li><a href="/nvme/figure-reference/identify/en/#figure-b338">Base 2.4 Figure 338 · Identify – Identify Controller Data Structure, I/O Command Set Independent</a></li>
<li><a href="/nvme/figure-reference/init/en/#figure-b36">Base 2.4 Figure 36 · Offset 0h: CAP – Controller Capabilities</a></li>
<li><a href="/nvme/figure-reference/command/en/#figure-b93">Base 2.4 Figure 93 · Common Command Format</a></li>
<li><a href="/nvme/figure-reference/identify/en/#figure-n123">NVM Command Set 1.3 Figure 123 · Identify – Identify Namespace Data Structure, NVM Command Set</a></li>
<li><a href="/nvme/figure-reference/io/en/#figure-n155">NVM Command Set 1.3 Figure 155 · 16b Guard Protection Information Format when STS field is cleared to 0h</a></li>
<li><a href="/nvme/figure-reference/io/en/#figure-n174">NVM Command Set 1.3 Figure 174 · Write Command 16b Guard Protection Information Processing</a></li>
<li><a href="/nvme/figure-reference/io/en/#figure-n175">NVM Command Set 1.3 Figure 175 · Read 16b Guard Command Protection Information Processing</a></li>
<li><a href="/nvme/figure-reference/io/en/#figure-n39">NVM Command Set 1.3 Figure 39 · Copy – Copy Descriptor Formats</a></li>
<li><a href="/nvme/figure-reference/io/en/#figure-n4">NVM Command Set 1.3 Figure 4 · Atomicity Parameters for Single Atomicity Mode</a></li>
<li><a href="/nvme/figure-reference/io/en/#figure-n47">NVM Command Set 1.3 Figure 47 · Dataset Management – Range Definition</a></li>
<li><a href="/nvme/figure-reference/io/en/#figure-n53">NVM Command Set 1.3 Figure 53 · Read – Command Dword 10 and Command Dword 11</a></li>
<li><a href="/nvme/figure-reference/io/en/#figure-n54">NVM Command Set 1.3 Figure 54 · Read – Command Dword 12</a></li>
<li><a href="/nvme/figure-reference/io/en/#figure-n70">NVM Command Set 1.3 Figure 70 · Write – Command Dword 10 and Command Dword 11</a></li>
<li><a href="/nvme/figure-reference/io/en/#figure-n71">NVM Command Set 1.3 Figure 71 · Write – Command Dword 12</a></li>
<li><a href="/nvme/figure-reference/io/en/#figure-n8">NVM Command Set 1.3 Figure 8 · Atomic Boundaries Example</a></li>
<li><a href="/nvme/figure-reference/io/en/#figure-n83">NVM Command Set 1.3 Figure 83 · Write Zeroes – Command Dword 12</a></li>
</ul><details><summary>Original documents used</summary><ul class="qr-sources">
<li>NVM Express Base Specification · Revision 2.4 · 2026-07-31<br><code>NVM-Express-Base-Specification-Revision-2.4-Ratified-2026.07.31.pdf</code></li>
<li>NVM Express NVM Command Set Specification · Revision 1.3 · 2026-07-31<br><code>NVM-Express-NVM-Command-Set-Specification-Revision-1.3-Ratified-2026.07.31.pdf</code></li>
<li>NVM Express NVMe over PCIe Transport Specification · Revision 1.4 · 2026-07-31<br><code>NVM-Express-NVMe-over-PCIe-Transport-Specification-Revision-1.4-Ratified-2026.07.31.pdf</code></li>
</ul></details></section>
</main>
<nav class="qr-top" aria-label="Bank and editions"><a href="#content">Skip to content</a><a href="/nvme/question-bank/en/">Question index</a><a href="/nvme/question-bank/data-io/zh-tw/">繁體中文</a><a href="/DOCS/nvme-question-bank/data-io.html">Chinese tutorial HTML</a></nav>
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
