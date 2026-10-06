---
layout: post
title: "NVMe Self-Study Bank: Domains, reclaim groups and media units"
date: 2026-10-02 00:00:00 +0800
categories: [nvme]
permalink: /nvme/question-bank/media/en/
lang: en
nvme_quickref: true
nvme_qa: true
---

<div class="nvme-quickref nvme-qa">
<nav class="qr-top" aria-label="Bank and editions"><a href="#content">Skip to content</a><a href="/nvme/question-bank/en/">Question index</a><a href="/nvme/question-bank/media/zh-tw/">繁體中文</a><a href="/DOCS/nvme-question-bank/media.html">Chinese tutorial HTML</a></nav>
<main id="content"><p class="qr-eyebrow">BASE 2.4 / NVM 1.3 / PCIe 1.4 · Q1–328</p>
<header><p class="qa-range">Q268–Q275</p><h1>Domains, reclaim groups and media units</h1><p class="qr-intro">Distinguish ownership from FDP placement, then follow identifiers to an RU and interpret media-report limits.</p><p>Practice first, then reveal the explanation. Each question uses the prose, field interpretation, comparison or flow that suits it. All numerical examples are hypothetical. Status is written SCT/SC; h indicates hexadecimal.</p></header>
<aside class="qa-glossary"><h2>Terms used in this volume</h2><dl><dt>Controller / namespace</dt><dd>A controller receives commands and manages access. A namespace is a logical storage space that commands can address. An NVM subsystem contains controllers and nonvolatile storage resources.</dd><dt>SQ / CQ / SQE / CQE</dt><dd>Submission and Completion Queues carry command entries (SQEs) and completion entries (CQEs). QID identifies a queue, CID distinguishes outstanding commands in one SQ, and NSID identifies a namespace.</dd><dt>Register / Identify / Feature / Log</dt><dd>A register exposes control or state. Identify queries capabilities and attributes; features query or configure operation; log pages report specific state or records. FID, LID, CNS and CSI select features, logs, Identify structures and command sets.</dd><dt>index / offset / zero-based</dt><dd>An index selects an entry, usually starting at 0; an offset measures distance from an origin in specified units. A zero-based count encodes count−1, but not every zero-valued field is a count. A Dword is 4 bytes; a byte is 8 bits.</dd><dt>Scope / reset / retention</dt><dd>Scope names the affected objects; retention means preserving state. Controller Reset (clearing CC.EN) is one form of Controller Level Reset, or CLR. Different CLR triggers can retain different registers.</dd></dl></aside>
<section id="overview" class="qa-overview"><h2>Follow a write PID to the current RU</h2><p class="qa-takeaway">A PID placement handle is not the RUH identifier; apply namespace mapping.</p>
<div class="qr-table" tabindex="0" role="region" aria-label="Horizontally scrollable comparison table"><table><thead><tr><th scope="col">Step</th><th scope="col">Hypothetical value</th><th scope="col">Selection</th></tr></thead><tbody><tr><td>Decode PID</td><td>RGID1, PH0</td><td>RG1 and namespace PH0</td></tr><tr><td>Map handle</td><td>NS1 PH0 maps to RUH2</td><td>RUH2</td></tr><tr><td>Current reference</td><td>RUH2 references RU B in RG1</td><td>Current placement RU</td></tr><tr><td>After filling</td><td>Controller replaces active RU</td><td>Stable PH, different RU</td></tr></tbody></table></div>
<p><strong>Worked interpretation: </strong>Equal PID values in two namespaces can map to different RUHs; preserve NSID and configuration.</p>
<p class="qa-citations">Sources: <a href="#ref-fdpmodel">Base 2.4 §3.2.4, 8.1.12</a> · <a href="#ref-fdpcontrol">Base 2.4 §5.2.13.1.29–5.2.13.1.32, 5.2.30.1.21–5.2.30.1.22, 7.3–7.4</a> · <a href="#ref-fdpnvm">NVM Command Set 1.3 §3.2, 4.1.4.6–4.1.4.7</a> · <a href="#ref-mediaunit">Base 2.4 §5.2.13.1.16</a></p>
</section>
<div class="qa-controls" hidden><label>Search this page <input type="search" id="qa-search" placeholder="Question number, field or keyword"></label><button type="button" data-expand="true">Expand all answers</button><button type="button" data-expand="false">Collapse all answers</button><output id="qa-count" aria-live="polite"></output></div>
<section id="question-index"><h2>Questions in this volume</h2><ol class="qa-index">
<li><a href="#q-268">Q268 · Do domains, sets, groups, media units and namespaces form one hierarchy?</a></li>
<li><a href="#q-269">Q269 · How are domains and resource ownership discovered?</a></li>
<li><a href="#q-270">Q270 · What are a reclaim group, reclaim unit and reclaim-unit handle?</a></li>
<li><a href="#q-271">Q271 · How does a namespace select an RU through a placement handle?</a></li>
<li><a href="#q-272">Q272 · What does Media Unit Status report and how are descriptors traversed?</a></li>
<li><a href="#q-273">Q273 · Can Media Unit Status directly establish namespace unavailability?</a></li>
<li><a href="#q-274">Q274 · Which notices and records can accompany media changes?</a></li>
<li><a href="#q-275">Q275 · How are entity scopes distinguished without confusing identifiers?</a></li>
</ol></section>
<article class="qa-question" id="q-268" data-question="268" data-answer-kind="compare"><h2><a class="qa-qid" href="#q-268">Q268</a> Do domains, sets, groups, media units and namespaces form one hierarchy?</h2>
<p class="qa-prompt">Identify the key difference and one case where the alternatives are not interchangeable.</p>
<details class="qa-answer" id="q-268-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-268-a-01">These names represent management, endurance, capacity, logical addressing and data-placement views.</p><div class="qa-sections">
<section class="qa-section" id="q-268-s-01" data-answer-section="1"><h3><span>1.</span> What differs</h3>
<span class="qa-anchor" id="q-268-a-02"></span><p>With sets, namespace→set→endurance group→domain is ownership; a reclaim group is not another namespace container inserted into that chain.</p>
<span class="qa-anchor" id="q-268-a-04"></span><p>A media unit is a reported media-information entity; an FDP reclaim unit is a reclamation entity, not necessarily the same object.</p>
</section>
<section class="qa-section" id="q-268-s-02" data-answer-section="2"><h3><span>2.</span> How to choose and verify</h3>
<span class="qa-anchor" id="q-268-a-03"></span><p>Read capabilities, inventories, namespace membership and FDP configurations.</p>
<span class="qa-anchor" id="q-268-a-05"></span><p>Draw ownership separately from placement-handle selection; they answer membership and placement respectively.</p>
<span class="qa-anchor" id="q-268-a-06"></span><p>Explain both ownership and placement without inventing one-to-one mappings.</p>
</section>
<section class="qa-section" id="q-268-s-03" data-answer-section="3"><h3><span>3.</span> Where the comparison stops</h3>
<span class="qa-anchor" id="q-268-a-07"></span><p>A media unit is not guaranteed to be a die, nor is channel membership universally one-to-one.</p>
<span class="qa-anchor" id="q-268-a-16"></span><p>Compare identifier definitions, scopes and observation times rather than numeric equality.</p>
</section>
</div>
<span class="qa-anchor" id="q-268-a-17"></span><span class="qa-anchor" id="q-268-a-08"></span><span class="qa-anchor" id="q-268-a-09"></span><span class="qa-anchor" id="q-268-a-10"></span><span class="qa-anchor" id="q-268-a-11"></span><span class="qa-anchor" id="q-268-a-12"></span><span class="qa-anchor" id="q-268-a-13"></span><span class="qa-anchor" id="q-268-a-14"></span><span class="qa-anchor" id="q-268-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-capacitymodel">Base 2.4 §3.2.2–3.2.3, 3.8</a> · <a href="#ref-mediaunit">Base 2.4 §5.2.13.1.16</a> · <a href="#ref-fdpmodel">Base 2.4 §3.2.4, 8.1.12</a> · <a href="#ref-fdpcontrol">Base 2.4 §5.2.13.1.29–5.2.13.1.32, 5.2.30.1.21–5.2.30.1.22, 7.3–7.4</a> · <a href="#ref-fdpnvm">NVM Command Set 1.3 §3.2, 4.1.4.6–4.1.4.7</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-idns">NVM Command Set 1.3 §4.1.5.1–4.1.5.4</a> · <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-ana">Base 2.4 §2.4.2, 8.1.1 (PCIe namespace access)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-269" data-question="269" data-answer-kind="lookup"><h2><a class="qa-qid" href="#q-269">Q269</a> How are domains and resource ownership discovered?</h2>
<p class="qa-prompt">Choose the interface and target, then identify the returned field that supports your conclusion.</p>
<details class="qa-answer" id="q-269-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-269-a-01">Establish the observation domain before interpreting resource and capacity inventories.</p><div class="qa-sections">
<section class="qa-section" id="q-269-s-01" data-answer-section="1"><h3><span>1.</span> Select the target and information</h3>
<span class="qa-anchor" id="q-269-a-02"></span><p>A domain can contain no controller or no endurance group; visible controllers do not enumerate all domains.</p>
<span class="qa-anchor" id="q-269-a-03"></span><p>Read MDS, controller domain information and domain/group/set inventories.</p>
<span class="qa-anchor" id="q-269-a-04"></span><p>Namespace membership and media-unit DID/group/set fields provide complementary ownership views.</p>
</section>
<section class="qa-section" id="q-269-s-02" data-answer-section="2"><h3><span>2.</span> Query sequence and interpretation</h3>
<span class="qa-anchor" id="q-269-a-05"></span><p>Enumerate valid domains and resources, preserving controller and DID with each observation.</p>
<span class="qa-anchor" id="q-269-a-06"></span><p>A joined view identifies the namespace’s group and the domain owning the reported capacity.</p>
</section>
<section class="qa-section" id="q-269-s-03" data-answer-section="3"><h3><span>3.</span> Handle missing or inconsistent evidence</h3>
<span class="qa-anchor" id="q-269-a-07"></span><p>LID 10h DID0 selects the controller’s domain; an invalid nonzero DID requires Invalid Field.</p>
<span class="qa-anchor" id="q-269-a-16"></span><p>Interpret zero with MDS and distinguish unavailable cross-domain information from absent resources.</p>
<span class="qa-anchor" id="q-269-a-17"></span><p>First check the endpoint and domain selector.</p>
</section>
</div>
<span class="qa-anchor" id="q-269-a-08"></span><span class="qa-anchor" id="q-269-a-09"></span><span class="qa-anchor" id="q-269-a-10"></span><span class="qa-anchor" id="q-269-a-11"></span><span class="qa-anchor" id="q-269-a-12"></span><span class="qa-anchor" id="q-269-a-13"></span><span class="qa-anchor" id="q-269-a-14"></span><span class="qa-anchor" id="q-269-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-capacitymodel">Base 2.4 §3.2.2–3.2.3, 3.8</a> · <a href="#ref-mediaunit">Base 2.4 §5.2.13.1.16</a> · <a href="#ref-fdpmodel">Base 2.4 §3.2.4, 8.1.12</a> · <a href="#ref-fdpcontrol">Base 2.4 §5.2.13.1.29–5.2.13.1.32, 5.2.30.1.21–5.2.30.1.22, 7.3–7.4</a> · <a href="#ref-fdpnvm">NVM Command Set 1.3 §3.2, 4.1.4.6–4.1.4.7</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-idns">NVM Command Set 1.3 §4.1.5.1–4.1.5.4</a> · <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-ana">Base 2.4 §2.4.2, 8.1.1 (PCIe namespace access)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-270" data-question="270" data-answer-kind="compare"><h2><a class="qa-qid" href="#q-270">Q270</a> What are a reclaim group, reclaim unit and reclaim-unit handle?</h2>
<p class="qa-prompt">Identify the key difference and one case where the alternatives are not interchangeable.</p>
<details class="qa-answer" id="q-270-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-270-a-01">FDP conveys placement intent while the controller manages reclamation and active-RU replacement.</p><div class="qa-sections">
<section class="qa-section" id="q-270-s-01" data-answer-section="1"><h3><span>1.</span> What differs</h3>
<span class="qa-anchor" id="q-270-a-02"></span><p>FDP configuration is endurance-group scoped; RG/RUH identifiers belong to that configuration.</p>
<span class="qa-anchor" id="q-270-a-04"></span><p>An RG contains RUs; each RUH references one RU in every RG, while an RU has at most one current RUH reference.</p>
</section>
<section class="qa-section" id="q-270-s-02" data-answer-section="2"><h3><span>2.</span> How to choose and verify</h3>
<span class="qa-anchor" id="q-270-a-03"></span><p>Read configuration counts/descriptors and the enabled configuration through FID 1Dh.</p>
<span class="qa-anchor" id="q-270-a-05"></span><p>Select RG and placement handle, map to RUH, and let the controller replace a full RU within that RG.</p>
<span class="qa-anchor" id="q-270-a-06"></span><p>Example: RUH2 references one RU in RG0 and another in RG1; RUH2 alone does not select between them.</p>
</section>
<section class="qa-section" id="q-270-s-03" data-answer-section="3"><h3><span>3.</span> Where the comparison stops</h3>
<span class="qa-anchor" id="q-270-a-07"></span><p>Initially and persistently isolated handles have different reclamation mixing requirements.</p>
<span class="qa-anchor" id="q-270-a-16"></span><p>Correlate configuration, RG, handle type and state; a stable RUH ID does not imply a fixed RU reference.</p>
</section>
</div>
<span class="qa-anchor" id="q-270-a-17"></span><span class="qa-anchor" id="q-270-a-08"></span><span class="qa-anchor" id="q-270-a-09"></span><span class="qa-anchor" id="q-270-a-10"></span><span class="qa-anchor" id="q-270-a-11"></span><span class="qa-anchor" id="q-270-a-12"></span><span class="qa-anchor" id="q-270-a-13"></span><span class="qa-anchor" id="q-270-a-14"></span><span class="qa-anchor" id="q-270-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-capacitymodel">Base 2.4 §3.2.2–3.2.3, 3.8</a> · <a href="#ref-mediaunit">Base 2.4 §5.2.13.1.16</a> · <a href="#ref-fdpmodel">Base 2.4 §3.2.4, 8.1.12</a> · <a href="#ref-fdpcontrol">Base 2.4 §5.2.13.1.29–5.2.13.1.32, 5.2.30.1.21–5.2.30.1.22, 7.3–7.4</a> · <a href="#ref-fdpnvm">NVM Command Set 1.3 §3.2, 4.1.4.6–4.1.4.7</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-idns">NVM Command Set 1.3 §4.1.5.1–4.1.5.4</a> · <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-ana">Base 2.4 §2.4.2, 8.1.1 (PCIe namespace access)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-271" data-question="271" data-answer-kind="process"><h2><a class="qa-qid" href="#q-271">Q271</a> How does a namespace select an RU through a placement handle?</h2>
<p class="qa-prompt">Order the actions and identify which completion must precede the next action.</p>
<details class="qa-answer" id="q-271-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-271-a-01">A namespace’s placement-handle list maps write placement intent to group-level RUHs.</p><div class="qa-sections">
<section class="qa-section" id="q-271-s-01" data-answer-section="1"><h3><span>1.</span> Prepare the operation</h3>
<span class="qa-anchor" id="q-271-a-02"></span><p>The same PH can map differently across namespaces, while sharing RUHs is possible under configuration constraints.</p>
<span class="qa-anchor" id="q-271-a-03"></span><p>Read namespace handle mapping, configuration and RUH status.</p>
<span class="qa-anchor" id="q-271-a-04"></span><p>FDP writes use DTYPE02h and a DSPEC PID encoding RGID plus PH, not a raw RUH ID.</p>
</section>
<section class="qa-section" id="q-271-s-02" data-answer-section="2"><h3><span>2.</span> Sequence and completion conditions</h3>
<span class="qa-anchor" id="q-271-a-05"></span><p>Decode PID, map PH to RUH and select that handle’s current RU in the chosen RG.</p>
<span class="qa-anchor" id="q-271-a-06"></span><p>If NS1 PH0 maps to RUH2 and PID selects RG1, placement uses RUH2&#x27;s current RU in RG1.</p>
</section>
<section class="qa-section" id="q-271-s-03" data-answer-section="3"><h3><span>3.</span> Handle unmet conditions</h3>
<span class="qa-anchor" id="q-271-a-07"></span><p>Invalid write PID requires fallback placement and enabled-event handling; invalid RUH Update selectors do not use that fallback rule.</p>
<span class="qa-anchor" id="q-271-a-16"></span><p>Writes without the directive use PH0 and a controller-selected RG, not a bypass of FDP configuration.</p>
</section>
</div>
<span class="qa-anchor" id="q-271-a-17"></span><span class="qa-anchor" id="q-271-a-08"></span><span class="qa-anchor" id="q-271-a-09"></span><span class="qa-anchor" id="q-271-a-10"></span><span class="qa-anchor" id="q-271-a-11"></span><span class="qa-anchor" id="q-271-a-12"></span><span class="qa-anchor" id="q-271-a-13"></span><span class="qa-anchor" id="q-271-a-14"></span><span class="qa-anchor" id="q-271-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-capacitymodel">Base 2.4 §3.2.2–3.2.3, 3.8</a> · <a href="#ref-mediaunit">Base 2.4 §5.2.13.1.16</a> · <a href="#ref-fdpmodel">Base 2.4 §3.2.4, 8.1.12</a> · <a href="#ref-fdpcontrol">Base 2.4 §5.2.13.1.29–5.2.13.1.32, 5.2.30.1.21–5.2.30.1.22, 7.3–7.4</a> · <a href="#ref-fdpnvm">NVM Command Set 1.3 §3.2, 4.1.4.6–4.1.4.7</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-idns">NVM Command Set 1.3 §4.1.5.1–4.1.5.4</a> · <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-ana">Base 2.4 §2.4.2, 8.1.1 (PCIe namespace access)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-272" data-question="272" data-answer-kind="fields"><h2><a class="qa-qid" href="#q-272">Q272</a> What does Media Unit Status report and how are descriptors traversed?</h2>
<p class="qa-prompt">Explain the units and encoding, then work through one set of values.</p>
<details class="qa-answer" id="q-272-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-272-a-01">This log reports domain media ownership, adjustment and wear, not per-I/O completion.</p><div class="qa-sections">
<section class="qa-section" id="q-272-s-01" data-answer-section="1"><h3><span>1.</span> Establish the source and scope</h3>
<span class="qa-anchor" id="q-272-a-02"></span><p>LID 10h selects a domain; media-unit and channel identifiers are domain-local.</p>
<span class="qa-anchor" id="q-272-a-03"></span><p>Check log/domain support and header counts/configuration.</p>
</section>
<section class="qa-section" id="q-272-s-02" data-answer-section="2"><h3><span>2.</span> Fields, units and worked interpretation</h3>
<span class="qa-anchor" id="q-272-a-04"></span><p>Descriptors provide identity, ownership, adjustment, spare/wear and channel-list location/count.</p>
<span class="qa-anchor" id="q-272-a-05"></span><p>Locate the channel list at CIO and read MUCS two-byte IDs; applicable descriptor length is CIO plus list length, not a universal fixed stride.</p>
<span class="qa-anchor" id="q-272-a-06"></span><p>Parse ordered IDs; CCHANS0 means the common-channel count is unreported, not no channels exist.</p>
</section>
<section class="qa-section" id="q-272-s-03" data-answer-section="3"><h3><span>3.</span> Conditions that change the interpretation</h3>
<span class="qa-anchor" id="q-272-a-07"></span><p>Cleared capacity configuration has specified zero fields and is not an ordinary populated configuration.</p>
<span class="qa-anchor" id="q-272-a-16"></span><p>The specification does not define group health as a simple average of media-unit values.</p>
</section>
</div>
<span class="qa-anchor" id="q-272-a-17"></span><span class="qa-anchor" id="q-272-a-08"></span><span class="qa-anchor" id="q-272-a-09"></span><span class="qa-anchor" id="q-272-a-10"></span><span class="qa-anchor" id="q-272-a-11"></span><span class="qa-anchor" id="q-272-a-12"></span><span class="qa-anchor" id="q-272-a-13"></span><span class="qa-anchor" id="q-272-a-14"></span><span class="qa-anchor" id="q-272-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-capacitymodel">Base 2.4 §3.2.2–3.2.3, 3.8</a> · <a href="#ref-mediaunit">Base 2.4 §5.2.13.1.16</a> · <a href="#ref-fdpmodel">Base 2.4 §3.2.4, 8.1.12</a> · <a href="#ref-fdpcontrol">Base 2.4 §5.2.13.1.29–5.2.13.1.32, 5.2.30.1.21–5.2.30.1.22, 7.3–7.4</a> · <a href="#ref-fdpnvm">NVM Command Set 1.3 §3.2, 4.1.4.6–4.1.4.7</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-idns">NVM Command Set 1.3 §4.1.5.1–4.1.5.4</a> · <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-ana">Base 2.4 §2.4.2, 8.1.1 (PCIe namespace access)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-273" data-question="273" data-answer-kind="concept"><h2><a class="qa-qid" href="#q-273">Q273</a> Can Media Unit Status directly establish namespace unavailability?</h2>
<p class="qa-prompt">Explain the mechanism in your own words and identify a common misconception.</p>
<details class="qa-answer" id="q-273-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-273-a-01">Not directly. Media Unit Status Log (LID 10h) has no generic state that translates into Namespace Ready; inspect namespace and access-path evidence separately.</p><div class="qa-sections">
<section class="qa-section" id="q-273-s-01" data-answer-section="1"><h3><span>1.</span> Wear values are not readiness state</h3>
<span class="qa-anchor" id="q-273-a-02"></span><p>Media wear, namespace accessibility and controller-path availability are distinct observations.</p>
<span class="qa-anchor" id="q-273-a-04"></span><p>Percentage used estimates endurance consumption and spare reports reserve; neither directly encodes Namespace Not Ready.</p>
<span class="qa-anchor" id="q-273-a-06"></span><p>Percentage used above 100 does not require all I/O to fail.</p>
</section>
<section class="qa-section" id="q-273-s-02" data-answer-section="2"><h3><span>2.</span> Evidence to examine after access fails</h3>
<span class="qa-anchor" id="q-273-a-03"></span><p>Combine membership, controller readiness, applicable ANA and command results, using media-unit data as context.</p>
<span class="qa-anchor" id="q-273-a-05"></span><p>Establish attachment/path access, inspect a valid command’s failure and then correlate media ownership.</p>
<span class="qa-anchor" id="q-273-a-07"></span><p>Namespace Not Ready, ANA Inaccessible and media errors have different conditions and statuses.</p>
<span class="qa-anchor" id="q-273-a-16"></span><p>Correlate shared resources for simultaneous failures without treating coincidence as proof.</p>
</section>
</div>
<span class="qa-anchor" id="q-273-a-17"></span><span class="qa-anchor" id="q-273-a-08"></span><span class="qa-anchor" id="q-273-a-09"></span><span class="qa-anchor" id="q-273-a-10"></span><span class="qa-anchor" id="q-273-a-11"></span><span class="qa-anchor" id="q-273-a-12"></span><span class="qa-anchor" id="q-273-a-13"></span><span class="qa-anchor" id="q-273-a-14"></span><span class="qa-anchor" id="q-273-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-capacitymodel">Base 2.4 §3.2.2–3.2.3, 3.8</a> · <a href="#ref-mediaunit">Base 2.4 §5.2.13.1.16</a> · <a href="#ref-fdpmodel">Base 2.4 §3.2.4, 8.1.12</a> · <a href="#ref-fdpcontrol">Base 2.4 §5.2.13.1.29–5.2.13.1.32, 5.2.30.1.21–5.2.30.1.22, 7.3–7.4</a> · <a href="#ref-fdpnvm">NVM Command Set 1.3 §3.2, 4.1.4.6–4.1.4.7</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-idns">NVM Command Set 1.3 §4.1.5.1–4.1.5.4</a> · <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-ana">Base 2.4 §2.4.2, 8.1.1 (PCIe namespace access)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-274" data-question="274" data-answer-kind="events"><h2><a class="qa-qid" href="#q-274">Q274</a> Which notices and records can accompany media changes?</h2>
<p class="qa-prompt">Establish the event condition, then distinguish notification, acknowledgment and recording.</p>
<details class="qa-answer" id="q-274-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-274-a-01">There is no generic AER for every media-unit field change; classify health, ANA, namespace or FDP changes first.</p><div class="qa-sections">
<section class="qa-section" id="q-274-s-01" data-answer-section="1"><h3><span>1.</span> When the event exists and who observes it</h3>
<span class="qa-anchor" id="q-274-a-02"></span><p>Warnings can be group, subsystem or controller-path scoped and are not interchangeable.</p>
<span class="qa-anchor" id="q-274-a-03"></span><p>Read AEC, group-health and FDP-event enables with capability bits.</p>
<span class="qa-anchor" id="q-274-a-04"></span><p>Health logs report warnings, ANA reports paths and FDP logs enabled placement events.</p>
</section>
<section class="qa-section" id="q-274-s-02" data-answer-section="2"><h3><span>2.</span> Notification, reading and acknowledgment</h3>
<span class="qa-anchor" id="q-274-a-05"></span><p>Preserve AER type/information/LID, then read the matching log with RAE1 when retention is needed.</p>
<span class="qa-anchor" id="q-274-a-06"></span><p>A group spare warning calls for EGCW and configured aggregate notice, not an invented Media Unit Lost event.</p>
</section>
<section class="qa-section" id="q-274-s-03" data-answer-section="3"><h3><span>3.</span> Evaluate missing notifications or records</h3>
<span class="qa-anchor" id="q-274-a-07"></span><p>Before declaring a missing event, check enables, pending AERs, prior acknowledgments and qualifying conditions.</p>
<span class="qa-anchor" id="q-274-a-16"></span><p>PEL records supported qualifying events, not every percentage-used update.</p>
<span class="qa-anchor" id="q-274-a-17"></span><p>First specify the actual field transition before selecting an event rule.</p>
</section>
<section class="qa-section" id="q-274-s-04" data-answer-section="4"><h3><span>4.</span> Check notifications and log records separately</h3>
<span class="qa-anchor" id="q-274-a-09"></span><p>Reading a log does not itself require a new event. <a class="qa-rule-link" href="#common-log_query-9">Read the complete conditions in this volume</a></p>
<span class="qa-anchor" id="q-274-a-10"></span><p>Get Log Page returns the selected data. <a class="qa-rule-link" href="#common-log_query-10">Read the complete conditions in this volume</a></p>
<span class="qa-anchor" id="q-274-a-11"></span><p>Get Log Page is not a per-read PEL audit trail. <a class="qa-rule-link" href="#common-log_query-11">Read the complete conditions in this volume</a></p>
</section>
</div>
<span class="qa-anchor" id="q-274-a-08"></span><span class="qa-anchor" id="q-274-a-12"></span><span class="qa-anchor" id="q-274-a-13"></span><span class="qa-anchor" id="q-274-a-14"></span><span class="qa-anchor" id="q-274-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-capacitymodel">Base 2.4 §3.2.2–3.2.3, 3.8</a> · <a href="#ref-mediaunit">Base 2.4 §5.2.13.1.16</a> · <a href="#ref-fdpmodel">Base 2.4 §3.2.4, 8.1.12</a> · <a href="#ref-fdpcontrol">Base 2.4 §5.2.13.1.29–5.2.13.1.32, 5.2.30.1.21–5.2.30.1.22, 7.3–7.4</a> · <a href="#ref-fdpnvm">NVM Command Set 1.3 §3.2, 4.1.4.6–4.1.4.7</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-idns">NVM Command Set 1.3 §4.1.5.1–4.1.5.4</a> · <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-ana">Base 2.4 §2.4.2, 8.1.1 (PCIe namespace access)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-275" data-question="275" data-answer-kind="concept"><h2><a class="qa-qid" href="#q-275">Q275</a> How are entity scopes distinguished without confusing identifiers?</h2>
<p class="qa-prompt">Explain the mechanism in your own words and identify a common misconception.</p>
<details class="qa-answer" id="q-275-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-275-a-01">The same number can identify a namespace, domain, group or reclaim group; field type and enclosing scope are essential.</p><div class="qa-sections">
<section class="qa-section" id="q-275-s-01" data-answer-section="1"><h3><span>1.</span> Mechanism and scope</h3>
<span class="qa-anchor" id="q-275-a-02"></span><p>Command endpoint, configuration scope and data ownership can differ.</p>
<span class="qa-anchor" id="q-275-a-04"></span><p>Record applicable endpoint, domain, group, namespace and selectors without inventing zero IDs for inapplicable fields.</p>
</section>
<section class="qa-section" id="q-275-s-02" data-answer-section="2"><h3><span>2.</span> Understand it through actions and results</h3>
<span class="qa-anchor" id="q-275-a-03"></span><p>Establish command/feature scope before resolving identifiers through inventories.</p>
<span class="qa-anchor" id="q-275-a-05"></span><p>Ask who receives it, who is targeted and who shares the effects before cross-controller comparison.</p>
<span class="qa-anchor" id="q-275-a-06"></span><p>FID 1Dh is group-scoped while namespaces retain distinct placement-handle mappings.</p>
</section>
<section class="qa-section" id="q-275-s-03" data-answer-section="3"><h3><span>3.</span> Avoid a misleading conclusion</h3>
<span class="qa-anchor" id="q-275-a-07"></span><p>Absent IDs, unsupported functionality and inaccessible cross-domain information are distinct conditions.</p>
<span class="qa-anchor" id="q-275-a-16"></span><p>Compare matching selectors/times and rediscover after ownership changes.</p>
</section>
</div>
<span class="qa-anchor" id="q-275-a-17"></span><span class="qa-anchor" id="q-275-a-08"></span><span class="qa-anchor" id="q-275-a-09"></span><span class="qa-anchor" id="q-275-a-10"></span><span class="qa-anchor" id="q-275-a-11"></span><span class="qa-anchor" id="q-275-a-12"></span><span class="qa-anchor" id="q-275-a-13"></span><span class="qa-anchor" id="q-275-a-14"></span><span class="qa-anchor" id="q-275-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-capacitymodel">Base 2.4 §3.2.2–3.2.3, 3.8</a> · <a href="#ref-mediaunit">Base 2.4 §5.2.13.1.16</a> · <a href="#ref-fdpmodel">Base 2.4 §3.2.4, 8.1.12</a> · <a href="#ref-fdpcontrol">Base 2.4 §5.2.13.1.29–5.2.13.1.32, 5.2.30.1.21–5.2.30.1.22, 7.3–7.4</a> · <a href="#ref-fdpnvm">NVM Command Set 1.3 §3.2, 4.1.4.6–4.1.4.7</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-idns">NVM Command Set 1.3 §4.1.5.1–4.1.5.4</a> · <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-ana">Base 2.4 §2.4.2, 8.1.1 (PCIe namespace access)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<section id="common-rules" class="qa-common"><h2>Shared rules linked from the answers</h2><p>Each shared mechanism is explained in full once in this volume. Use browser Back to return to the question; explicit command or feature exceptions take precedence.</p>
<article id="common-log_query-9"><h3>Shared conditions for this topic · Is an asynchronous event generated?</h3><p>Reading a log does not itself require a new event. A successful RAE=0 read may acknowledge its event; RAE=1 and unsuccessful reads retain it. Immediate and One-Shot events have separate clearing rules.</p></article>
<article id="common-log_query-10"><h3>Shared conditions for this topic · Are Error Information or other logs updated?</h3><p>Get Log Page returns the selected data. Reads can clear reported changes or acknowledge events, depending on the log and RAE, so preserve comparison evidence first. A successful read does not require an error entry; failed reads follow CQE and error-log rules.</p></article>
<article id="common-log_query-11"><h3>Shared conditions for this topic · Is it recorded in the Persistent Event Log?</h3><p>Get Log Page is not a per-read PEL audit trail. Reading PEL does not create another such event; separately occurring events follow their supported logging conditions.</p></article>
</section>
<section id="source-index"><h2>Source locations and existing figure guides</h2><p>Base printed page = PDF page−26; the other two use identical numbers. Locations follow the supplied PDF body and retain figure numbers. Shared pages contribute only the relevant definitions, excluding Fabrics and PCIe link/packet content.</p><ul class="qa-references">
<li id="ref-ana"><strong>Base 2.4 · §2.4.2, 8.1.1 (PCIe namespace access)</strong><br>Printed pages 37, 578–584 · PDF 63, 604–610 · Figure 675–678</li>
<li id="ref-capacitymodel"><strong>Base 2.4 · §3.2.2–3.2.3, 3.8</strong><br>Printed pages 80–84, 125–129 · PDF 106–110, 151–155 · Figure 67–69, 86–89</li>
<li id="ref-fdpmodel"><strong>Base 2.4 · §3.2.4, 8.1.12</strong><br>Printed pages 84–87, 648–652 · PDF 110–113, 674–678 · Figure 70–72, 730–732</li>
<li id="ref-reset"><strong>Base 2.4 · §3.7.1–3.7.4</strong><br>Printed pages 120–124 · PDF 146–150</li>
<li id="ref-status"><strong>Base 2.4 · §4.2.3</strong><br>Printed pages 145–155 · PDF 171–181 · Figure 101–105</li>
<li id="ref-aer"><strong>Base 2.4 · §5.2.2</strong><br>Printed pages 183–190 · PDF 209–216 · Figure 150–156</li>
<li id="ref-error"><strong>Base 2.4 · §5.2.13.1.2</strong><br>Printed pages 218–220 · PDF 244–246 · Figure 212</li>
<li id="ref-pel"><strong>Base 2.4 · §5.2.13.1.14 (header, reset, hardware, Set Feature events)</strong><br>Printed pages 244–256, 258, 262–264 · PDF 270–282, 284, 288–290 · Figure 232–244, 246, 252–253</li>
<li id="ref-mediaunit"><strong>Base 2.4 · §5.2.13.1.16</strong><br>Printed pages 270–272 · PDF 296–298 · Figure 262–264</li>
<li id="ref-fdpcontrol"><strong>Base 2.4 · §5.2.13.1.29–5.2.13.1.32, 5.2.30.1.21–5.2.30.1.22, 7.3–7.4</strong><br>Printed pages 293–301, 480–483, 568–571 · PDF 319–327, 506–509, 594–597 · Figure 293–303, 499–506, 650–657</li>
<li id="ref-idctrl"><strong>Base 2.4 · §5.2.14.2.1</strong><br>Printed pages 340–387 · PDF 366–413 · Figure 338–341</li>
<li id="ref-idlist"><strong>Base 2.4 · §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</strong><br>Printed pages 387–399, 402–404 · PDF 413–425, 428–430 · Figure 342–355, 360–362</li>
<li id="ref-fdpnvm"><strong>NVM Command Set 1.3 · §3.2, 4.1.4.6–4.1.4.7</strong><br>Printed pages 26, 79 · PDF 26, 79 · Figure 21, 116</li>
<li id="ref-idns"><strong>NVM Command Set 1.3 · §4.1.5.1–4.1.5.4</strong><br>Printed pages 84–107 · PDF 84–107 · Figure 123–130</li>
</ul><h3>When you need a field guide</h3><p>Existing figure explanations have canonical locations; use these links instead of duplicating the same guide.</p><ul>
<li><a href="/nvme/figure-reference/command/en/#figure-b101">Base 2.4 Figure 101 · Completion Queue Entry: Status Field</a></li>
<li><a href="/nvme/figure-reference/command/en/#figure-b104">Base 2.4 Figure 104 · Status Code – Command Specific Status Values</a></li>
<li><a href="/nvme/figure-reference/identify/en/#figure-b338">Base 2.4 Figure 338 · Identify – Identify Controller Data Structure, I/O Command Set Independent</a></li>
<li><a href="/nvme/figure-reference/identify/en/#figure-n123">NVM Command Set 1.3 Figure 123 · Identify – Identify Namespace Data Structure, NVM Command Set</a></li>
</ul><details><summary>Original documents used</summary><ul class="qr-sources">
<li>NVM Express Base Specification · Revision 2.4 · 2026-07-31<br><code>NVM-Express-Base-Specification-Revision-2.4-Ratified-2026.07.31.pdf</code></li>
<li>NVM Express NVM Command Set Specification · Revision 1.3 · 2026-07-31<br><code>NVM-Express-NVM-Command-Set-Specification-Revision-1.3-Ratified-2026.07.31.pdf</code></li>
<li>NVM Express NVMe over PCIe Transport Specification · Revision 1.4 · 2026-07-31<br><code>NVM-Express-NVMe-over-PCIe-Transport-Specification-Revision-1.4-Ratified-2026.07.31.pdf</code></li>
</ul></details></section>
</main>
<nav class="qr-top" aria-label="Bank and editions"><a href="#content">Skip to content</a><a href="/nvme/question-bank/en/">Question index</a><a href="/nvme/question-bank/media/zh-tw/">繁體中文</a><a href="/DOCS/nvme-question-bank/media.html">Chinese tutorial HTML</a></nav>
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
