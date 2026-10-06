---
layout: post
title: "NVMe Self-Study Bank: Get Features and Set Features"
date: 2026-10-01 00:00:00 +0800
categories: [nvme]
permalink: /nvme/question-bank/features/en/
lang: en
nvme_quickref: true
nvme_qa: true
---

<div class="nvme-quickref nvme-qa">
<nav class="qr-top" aria-label="Bank and editions"><a href="#content">Skip to content</a><a href="/nvme/question-bank/en/">Question index</a><a href="/nvme/question-bank/features/zh-tw/">繁體中文</a><a href="/DOCS/nvme-question-bank/features.html">Chinese tutorial HTML</a></nav>
<main id="content"><p class="qr-eyebrow">BASE 2.4 / NVM 1.3 / PCIe 1.4 · Q1–328</p>
<header><p class="qa-range">Q54–Q68</p><h1>Get Features and Set Features</h1><p class="qr-intro">Establish scope, changeability and saveability before Set. Completion, Current readback, actual behavior and restoration after reset are separate observations; a successful CQE does not replace them.</p><p>Practice first, then reveal the explanation. Each question uses the prose, field interpretation, comparison or flow that suits it. All numerical examples are hypothetical. Status is written SCT/SC; h indicates hexadecimal.</p></header>
<aside class="qa-glossary"><h2>Terms used in this volume</h2><dl><dt>Controller / namespace</dt><dd>A controller receives commands and manages access. A namespace is a logical storage space that commands can address. An NVM subsystem contains controllers and nonvolatile storage resources.</dd><dt>SQ / CQ / SQE / CQE</dt><dd>Submission and Completion Queues carry command entries (SQEs) and completion entries (CQEs). QID identifies a queue, CID distinguishes outstanding commands in one SQ, and NSID identifies a namespace.</dd><dt>Register / Identify / Feature / Log</dt><dd>A register exposes control or state. Identify queries capabilities and attributes; features query or configure operation; log pages report specific state or records. FID, LID, CNS and CSI select features, logs, Identify structures and command sets.</dd><dt>index / offset / zero-based</dt><dd>An index selects an entry, usually starting at 0; an offset measures distance from an origin in specified units. A zero-based count encodes count−1, but not every zero-valued field is a count. A Dword is 4 bytes; a byte is 8 bits.</dd><dt>Scope / reset / retention</dt><dd>Scope names the affected objects; retention means preserving state. Controller Reset (clearing CC.EN) is one form of Controller Level Reset, or CLR. Different CLR triggers can retain different registers.</dd></dl></aside>
<section id="overview" class="qa-overview"><h2>Current and Saved follow different update paths</h2><p class="qa-takeaway">SV=0 changes the present value; SV=1 requests saving. Restoration additionally depends on scope, saveability and feature exceptions.</p>
<div class="qr-table" tabindex="0" role="region" aria-label="Horizontally scrollable comparison table"><table><thead><tr><th scope="col">Action</th><th scope="col">Current</th><th scope="col">Saved / subsequent restoration</th></tr></thead><tbody><tr><td>Start with a saveable feature</td><td>A</td><td>Saved=A</td></tr><tr><td>Successful Set B, SV=0</td><td>B</td><td>Remains A</td></tr><tr><td>A reset restoring Saved</td><td>Returns to A</td><td>A</td></tr><tr><td>Successful Set C, SV=1</td><td>C</td><td>Updates to C</td></tr><tr><td>Same reset again</td><td>Returns to C</td><td>C</td></tr></tbody></table></div>
<p><strong>Worked interpretation: </strong>This table assumes a saveable feature and a reset that restores Saved. It is not universal: FID 84h is unsaveable with no Default, yet basic WPS1 survives power cycling and WPS2 clears on a power cycle.</p>
<p class="qa-citations">Sources: <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-getfeat">Base 2.4 §5.2.12</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-nwp">Base 2.4 §5.2.30.1.38, 8.1.18</a></p>
</section>
<div class="qa-controls" hidden><label>Search this page <input type="search" id="qa-search" placeholder="Question number, field or keyword"></label><button type="button" data-expand="true">Expand all answers</button><button type="button" data-expand="false">Collapse all answers</button><output id="qa-count" aria-live="polite"></output></div>
<section id="question-index"><h2>Questions in this volume</h2><ol class="qa-index">
<li><a href="#q-054">Q54 · What do Current, Default, Saved and Supported Capabilities mean?</a></li>
<li><a href="#q-055">Q55 · How does Set Features.Save affect values after reset and power cycling?</a></li>
<li><a href="#q-056">Q56 · Which errors apply to unsupported features, invalid values and unsupported Save?</a></li>
<li><a href="#q-057">Q57 · How does the host determine whether a feature requires NSID?</a></li>
<li><a href="#q-058">Q58 · How are Arbitration, Number of Queues and I/O Command Set Profile configured and checked?</a></li>
<li><a href="#q-059">Q59 · How are interrupt coalescing and vector configuration set and verified?</a></li>
<li><a href="#q-060">Q60 · What do Volatile Write Cache and Write Atomicity Normal control?</a></li>
<li><a href="#q-061">Q61 · How does Asynchronous Event Configuration select reported events?</a></li>
<li><a href="#q-062">Q62 · How do Power Management, APST and Host Controlled Thermal Management differ?</a></li>
<li><a href="#q-063">Q63 · How are Timestamp, Keep Alive Timer and Host Memory Buffer configured and verified?</a></li>
<li><a href="#q-064">Q64 · What do Host Behavior Support, Error Recovery and Read Recovery Level do?</a></li>
<li><a href="#q-065">Q65 · How is namespace write protection configured, and which modes survive reset or power cycling?</a></li>
<li><a href="#q-066">Q66 · Why read Get Features after a successful Set Features?</a></li>
<li><a href="#q-067">Q67 · How should features change after activation, namespace deletion, reset and power cycling?</a></li>
<li><a href="#q-068">Q68 · How should supported-feature claims be checked when Get, Set and behavior appear inconsistent?</a></li>
</ol></section>
<article class="qa-question" id="q-054" data-question="54" data-answer-kind="compare"><h2><a class="qa-qid" href="#q-054">Q54</a> What do Current, Default, Saved and Supported Capabilities mean?</h2>
<p class="qa-prompt">Task: establish Volatile Write Cache feature availability, saveability and current enable state. Identify the separate responses before revealing the answer.</p>
<details class="qa-answer" id="q-054-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-054-a-01">Separate the active value, manufacturing default, saved value and change/save capabilities; these are not four identical settings.</p><div class="qa-sections">
<section class="qa-section" id="q-054-s-01" data-answer-section="1"><h3><span>1.</span> What differs</h3>
<span class="qa-anchor" id="q-054-a-02"></span><p>Compare the same FID, scope and selectors; Current can differ across namespaces.</p>
<span class="qa-anchor" id="q-054-a-04"></span><p>SEL 0/1/2/3 select Current/Default/Saved/Supported Capabilities. With SEL 3, DW0 bits 2/1/0 are CHANG/NSSPEC/SVBL, not operational values.</p>
</section>
<section class="qa-section" id="q-054-s-02" data-answer-section="2"><h3><span>2.</span> How to choose and verify</h3>
<span class="qa-anchor" id="q-054-a-03"></span><p>Separate FID availability from its settings capabilities. LID 12h FSUPP reports availability; Identify.ONCS.SSFS advertises Save/Select, under which Get Features.SEL 3 returns CHANG/NSSPEC/SVBL. SEL 3 DW0 bit 0 is SVBL, not FSUPP.</p>
<section class="qa-lookup" id="q-054-lookup"><h4>Worked lookup: FSUPP, SVBL and Current.WCE</h4>
<p>Assume CC.CSS=000b, UUID Index 0, MLPS=1, SSFS=1 and VWC.VWCP=1. The example performs queries only and does not change the cache.</p>
<div class="qr-table" tabindex="0" role="region" aria-label="Horizontally scrollable comparison table"><table><thead><tr><th scope="col">Step and source location</th><th scope="col">Information to retrieve</th><th scope="col">What this establishes</th></tr></thead><tbody><tr><td>1 · Figure 200, printed 211/PDF 237</td><td>Volatile Write Cache uses FID 06h; MLPS=1 also guarantees LID 12h.</td><td>Identifies the feature and discovery log. Cache presence does not establish current enablement.</td></tr><tr><td>2 · Figures 270–271, printed 276–278/PDF 302–304</td><td>Read 1024 bytes of LID 12h (NUMD=255); FID 06h is at byte 4×6=24=18h. Assume its FSUPP bit 0 is 1.</td><td>FID 06h is advertised; saveability and current WCE are still unknown.</td></tr><tr><td>3 · Figures 198/201, printed 210,212/PDF 236,238</td><td>Get Features opcode 0Ah, FID 06h, SEL 3 and NSID 0 returns successful CQE DW0=00000005h.</td><td>Bits 2/1/0 give CHANG=1/NSSPEC=0/SVBL=1: changeable and saveable. Five is a capability bitmap, not the cache setting.</td></tr><tr><td>4 · Figure 471, printed 464–465/PDF 490–491</td><td>Query the same FID with SEL 0. Assume DW0=0; the VWC format decodes bit 0 as WCE=0.</td><td>The feature is supported and saveable while caching is currently disabled. Current 0 is not lack of support and need not equal the SEL 3 bitmap 5.</td></tr></tbody></table></div>
<p>Three different bit 0 definitions are involved: FSUPP in LID 12h, SVBL in SEL 3 CQE and WCE in this FID’s SEL 0 CQE. Preserve LID/FID, SEL and response format with the numeric value.</p>
<p class="qa-citations">Sources: <a href="#ref-featureeffects">Base 2.4 §5.2.13.1.18</a> · <a href="#ref-getfeat">Base 2.4 §5.2.12</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-vwc">Base 2.4 §5.2.30.1.4</a></p>
</section>
<span class="qa-anchor" id="q-054-a-05"></span><p>Read capabilities and Current first, then Saved/Default for reset analysis. If unsaveable or never saved, SEL 2 returns Default, subject to features that define no Default.</p>
<span class="qa-anchor" id="q-054-a-06"></span><p>SEL 3 DW0=5 reports CHANG=1, SVBL=1 and NSSPEC=0: changeable and saveable. NSSPEC=0 does not indicate scope; consult FSP or the FID definition rather than assuming controller scope. Five is not the Current operating value.</p>
</section>
<section class="qa-section" id="q-054-s-03" data-answer-section="3"><h3><span>3.</span> Where the comparison stops</h3>
<span class="qa-anchor" id="q-054-a-07"></span><p>Unsupported FID uses Invalid Field (0/02h); SEL 4–7 are reserved. Without Select support, do not treat a response as valid CHANG/SVBL discovery.</p>
<span class="qa-anchor" id="q-054-a-16"></span><p>Preserve FID and SEL with the returned DW0 to distinguish a value from a capability bitmap.</p>
</section>
</div>
<span class="qa-anchor" id="q-054-a-17"></span><span class="qa-anchor" id="q-054-a-08"></span><span class="qa-anchor" id="q-054-a-09"></span><span class="qa-anchor" id="q-054-a-10"></span><span class="qa-anchor" id="q-054-a-11"></span><span class="qa-anchor" id="q-054-a-12"></span><span class="qa-anchor" id="q-054-a-13"></span><span class="qa-anchor" id="q-054-a-14"></span><span class="qa-anchor" id="q-054-a-15"></span>
<p class="qa-related">Related mechanisms: <a href="/nvme/question-bank/logs/en/#q-069">Q69</a> · <a href="/nvme/question-bank/logs/en/#q-081">Q81</a> · <a href="/nvme/question-bank/features/en/#q-055">Q55</a> · <a href="/nvme/question-bank/features/en/#q-060">Q60</a></p>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-getfeat">Base 2.4 §5.2.12</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-featureeffects">Base 2.4 §5.2.13.1.18</a> · <a href="#ref-vwc">Base 2.4 §5.2.30.1.4</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-055" data-question="55" data-answer-kind="lifecycle"><h2><a class="qa-qid" href="#q-055">Q55</a> How does Set Features.Save affect values after reset and power cycling?</h2>
<p class="qa-prompt">Name the reset or interruption, then assess settings, ongoing operations and data separately.</p>
<details class="qa-answer" id="q-055-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-055-a-01">Let the host change only the active value or also the persistent value used on restoration.</p><div class="qa-sections">
<section class="qa-section" id="q-055-s-01" data-answer-section="1"><h3><span>1.</span> Identify the trigger and affected objects</h3>
<span class="qa-anchor" id="q-055-a-02"></span><p>Saving follows feature scope; namespace-scoped and controller-scoped settings are not one global value.</p>
<span class="qa-anchor" id="q-055-a-03"></span><p>Check ONCS.SSFS and the FID&#x27;s SVBL. Controller Save support does not make every feature saveable.</p>
</section>
<section class="qa-section" id="q-055-s-02" data-answer-section="2"><h3><span>2.</span> State changes and recovery</h3>
<span class="qa-anchor" id="q-055-a-04"></span><p>SV=0 changes Current without updating Saved; successful SV=1 updates both. Default does not become the host&#x27;s chosen value.</p>
<span class="qa-anchor" id="q-055-a-05"></span><p>Discover support, Set and await completion, then read Current/Saved separately. After the chosen reset, verify Current under scope and exception rules.</p>
<span class="qa-anchor" id="q-055-a-06"></span><p>With Saved=A and an SV=0 change to B, Current becomes B; a reset that restores Saved returns it to A, not B.</p>
</section>
<section class="qa-section" id="q-055-s-03" data-answer-section="3"><h3><span>3.</span> Verify retention and recovery</h3>
<span class="qa-anchor" id="q-055-a-07"></span><p>SV=1 for an unsaveable feature shall return Feature Identifier Not Saveable (1/0Dh), not silently succeed and lose the saved setting.</p>
<span class="qa-anchor" id="q-055-a-16"></span><p>Save success, active application and restoration are three separate checks. Current=B does not establish Saved=B.</p>
<span class="qa-anchor" id="q-055-a-17"></span><p>First inspect original SV/SVBL, then reset type and coverage.</p>
</section>
</div>
<span class="qa-anchor" id="q-055-a-08"></span><span class="qa-anchor" id="q-055-a-09"></span><span class="qa-anchor" id="q-055-a-10"></span><span class="qa-anchor" id="q-055-a-11"></span><span class="qa-anchor" id="q-055-a-12"></span><span class="qa-anchor" id="q-055-a-13"></span><span class="qa-anchor" id="q-055-a-14"></span><span class="qa-anchor" id="q-055-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-getfeat">Base 2.4 §5.2.12</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-featureeffects">Base 2.4 §5.2.13.1.18</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-056" data-question="56" data-answer-kind="error"><h2><a class="qa-qid" href="#q-056">Q56</a> Which errors apply to unsupported features, invalid values and unsupported Save?</h2>
<p class="qa-prompt">Distinguish failure conditions before deciding whether a particular response is required.</p>
<details class="qa-answer" id="q-056-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-056-a-01">Distinguish unsupported function, unchangeability, unsaveability and invalid value; their causes and corrections differ.</p><div class="qa-sections">
<section class="qa-section" id="q-056-s-01" data-answer-section="1"><h3><span>1.</span> Distinguish the failure conditions</h3>
<span class="qa-anchor" id="q-056-a-02"></span><p>Evaluate the FID, target scope, current state and this Get/Set operation, not merely the controller model.</p>
<span class="qa-anchor" id="q-056-a-04"></span><p>Check FID, SV, NSID, CDW11 and payload. Some features require selectors beyond a single value.</p>
<span class="qa-anchor" id="q-056-a-07"></span><p>Unsupported FID/invalid defined value:0/02h; unsaveable:1/0Dh; unchangeable:1/0Eh; controller-scoped Set with a valid NSID:1/0Fh. Specific FID ordering/state errors take precedence.</p>
</section>
<section class="qa-section" id="q-056-s-02" data-answer-section="2"><h3><span>2.</span> Establish the cause from evidence</h3>
<span class="qa-anchor" id="q-056-a-03"></span><p>SEL 3 capabilities require SSFS. CHANG=1 means some values are changeable, not that a current permanent state can be reversed.</p>
<span class="qa-anchor" id="q-056-a-05"></span><p>Establish a valid baseline, then separately test unsupported FID, bad values, SV=1 and wrong scope.</p>
</section>
<section class="qa-section" id="q-056-s-03" data-answer-section="3"><h3><span>3.</span> Outcome and follow-up checks</h3>
<span class="qa-anchor" id="q-056-a-06"></span><p>Successful Set establishes completion. Setting an unchangeable feature to its existing value may succeed or return Feature Not Changeable; both are permitted.</p>
<span class="qa-anchor" id="q-056-a-16"></span><p>Re-read after failure according to the feature&#x27;s error rules; an error is not a universal proof of no side effects.</p>
<span class="qa-anchor" id="q-056-a-17"></span><p>First exclude multiple simultaneous faults that allow different valid error choices.</p>
</section>
</div>
<span class="qa-anchor" id="q-056-a-08"></span><span class="qa-anchor" id="q-056-a-09"></span><span class="qa-anchor" id="q-056-a-10"></span><span class="qa-anchor" id="q-056-a-11"></span><span class="qa-anchor" id="q-056-a-12"></span><span class="qa-anchor" id="q-056-a-13"></span><span class="qa-anchor" id="q-056-a-14"></span><span class="qa-anchor" id="q-056-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-getfeat">Base 2.4 §5.2.12</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-featureeffects">Base 2.4 §5.2.13.1.18</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-057" data-question="57" data-answer-kind="lookup"><h2><a class="qa-qid" href="#q-057">Q57</a> How does the host determine whether a feature requires NSID?</h2>
<p class="qa-prompt">Choose the interface and target, then identify the returned field that supports your conclusion.</p>
<details class="qa-answer" id="q-057-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-057-a-01">Select the correct target before changing configuration.</p><div class="qa-sections">
<section class="qa-section" id="q-057-s-01" data-answer-section="1"><h3><span>1.</span> Select the target and information</h3>
<span class="qa-anchor" id="q-057-a-02"></span><p>Feature scope can be controller, namespace, subsystem, set, group or another management entity, not just two categories.</p>
<span class="qa-anchor" id="q-057-a-03"></span><p>SEL 3.NSSPEC=1 indicates namespace scope. With zero, inspect the feature-effects scope and Figure 466/NVM Figure 92.</p>
<span class="qa-anchor" id="q-057-a-04"></span><p>Controller-scoped Get/Set accepts NSID 0 or FFFFFFFFh. A valid namespace ID on Get can return the controller value, whereas Set must report the scope error.</p>
</section>
<section class="qa-section" id="q-057-s-02" data-answer-section="2"><h3><span>2.</span> Query sequence and interpretation</h3>
<span class="qa-anchor" id="q-057-a-05"></span><p>Determine scope, then NSID and other selectors. Namespace scope normally uses an active NSID; broadcast Get/Set differ and multi-domain restrictions apply.</p>
<span class="qa-anchor" id="q-057-a-06"></span><p>FID 05h Error Recovery is namespace-scoped and FID 01h Arbitration controller-scoped; numeric CDW11 values do not make their NSID rules interchangeable.</p>
</section>
<section class="qa-section" id="q-057-s-03" data-answer-section="3"><h3><span>3.</span> Handle missing or inconsistent evidence</h3>
<span class="qa-anchor" id="q-057-a-07"></span><p>Controller-scoped Set with a valid NSID returns 1/0Fh. Namespace-scoped Get with FFFFFFFFh generally returns 0/0Bh, subject to specific exceptions.</p>
<span class="qa-anchor" id="q-057-a-16"></span><p>NSSPEC=0 can coexist with subsystem/set scope; it does not universally mean one controller value for all namespaces.</p>
<span class="qa-anchor" id="q-057-a-17"></span><p>First read the scope definition and original NSID before suspecting namespace failure.</p>
</section>
</div>
<span class="qa-anchor" id="q-057-a-08"></span><span class="qa-anchor" id="q-057-a-09"></span><span class="qa-anchor" id="q-057-a-10"></span><span class="qa-anchor" id="q-057-a-11"></span><span class="qa-anchor" id="q-057-a-12"></span><span class="qa-anchor" id="q-057-a-13"></span><span class="qa-anchor" id="q-057-a-14"></span><span class="qa-anchor" id="q-057-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-getfeat">Base 2.4 §5.2.12</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-nvmfeat">NVM Command Set 1.3 §4.1.3.1–4.1.3.7</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-featureeffects">Base 2.4 §5.2.13.1.18</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-058" data-question="58" data-answer-kind="process"><h2><a class="qa-qid" href="#q-058">Q58</a> How are Arbitration, Number of Queues and I/O Command Set Profile configured and checked?</h2>
<p class="qa-prompt">Order the actions and identify which completion must precede the next action.</p>
<details class="qa-answer" id="q-058-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-058-a-01">These control scheduling parameters, queue allocations and allowed command-set combinations at different initialization stages.</p><div class="qa-sections">
<section class="qa-section" id="q-058-s-01" data-answer-section="1"><h3><span>1.</span> Prepare the operation</h3>
<span class="qa-anchor" id="q-058-a-02"></span><p>All three target controller configuration, while Profile affects namespace/command-set usability.</p>
<span class="qa-anchor" id="q-058-a-03"></span><p>Arbitration uses CAP.AMS/CC.AMS; queue allocation uses successful Set results; Profile requires CAP.CSS.IOCSS and CNS 1Ch vectors.</p>
<span class="qa-anchor" id="q-058-a-04"></span><p>FID 01h uses AB/HPW/MPW/LPW; FID 07h maps requested to allocated SQ/CQ counts; FID 19h.IOCSCI is a combination index.</p>
</section>
<section class="qa-section" id="q-058-s-02" data-answer-section="2"><h3><span>2.</span> Sequence and completion conditions</h3>
<span class="qa-anchor" id="q-058-a-05"></span><p>Select the profile and discover namespaces, allocate queues and create CQs/SQs; verify arbitration parameters together with CC.AMS/QPRIO.</p>
<span class="qa-anchor" id="q-058-a-06"></span><p>Read back the same FID/selectors. With CC.CSS other than 110b, Set FID 19h succeeds without effect; with 110b, the selected combination applies. Profile index 0 selects combination 0, not no command sets. FID 07h allocation is not instantiated queue count.</p>
</section>
<section class="qa-section" id="q-058-s-03" data-answer-section="3"><h3><span>3.</span> Handle unmet conditions</h3>
<span class="qa-anchor" id="q-058-a-07"></span><p>Setting FID 07h after queue creation returns 0/0Ch. With CC.CSS=110b, FID 19h shall return Combination Rejected if IOCSCI selects a zero-valued combination or an attached namespace uses an I/O command set absent from that combination. The supplied spec conflicts: Figure 104 lists Combination Rejected as 1/2Bh, Figure 554 as 1/15h. Preserve that discrepancy rather than declaring noncompliance from either table alone.</p>
<span class="qa-anchor" id="q-058-a-16"></span><p>Verify settings, creatable queue ranges and usable command sets independently.</p>
</section>
</div>
<span class="qa-anchor" id="q-058-a-17"></span><span class="qa-anchor" id="q-058-a-08"></span><span class="qa-anchor" id="q-058-a-09"></span><span class="qa-anchor" id="q-058-a-10"></span><span class="qa-anchor" id="q-058-a-11"></span><span class="qa-anchor" id="q-058-a-12"></span><span class="qa-anchor" id="q-058-a-13"></span><span class="qa-anchor" id="q-058-a-14"></span><span class="qa-anchor" id="q-058-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-arbit">Base 2.4 §5.2.30.1.1</a> · <a href="#ref-number">Base 2.4 §5.2.30.1.5</a> · <a href="#ref-profile">Base 2.4 §5.2.30.1.18</a> · <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-setcomplete">Base 2.4 §5.2.30 (Command Completion)</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-featureeffects">Base 2.4 §5.2.13.1.18</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-059" data-question="59" data-answer-kind="process"><h2><a class="qa-qid" href="#q-059">Q59</a> How are interrupt coalescing and vector configuration set and verified?</h2>
<p class="qa-prompt">Order the actions and identify which completion must precede the next action.</p>
<details class="qa-answer" id="q-059-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-059-a-01">Trade notification latency against interrupt overhead; posting a completion and generating an IRQ are different events.</p><div class="qa-sections">
<section class="qa-section" id="q-059-s-01" data-answer-section="1"><h3><span>1.</span> Prepare the operation</h3>
<span class="qa-anchor" id="q-059-a-02"></span><p>FID 08h controls I/O interrupt coalescing; FID 09h selects its application per vector. Admin CQ does not support coalescing.</p>
<span class="qa-anchor" id="q-059-a-03"></span><p>Check CQ.IEN/IV, PCIe interrupt mode and masks. Feature support is required, while aggregation algorithms remain implementation-specific.</p>
<span class="qa-anchor" id="q-059-a-04"></span><p>FID 08h TIME uses 100 μs units and THR is zero-based; either zero implicitly disables coalescing. FID 09h uses IV/CD; CD=1 disables coalescing, not interrupts.</p>
</section>
<section class="qa-section" id="q-059-s-02" data-answer-section="2"><h3><span>2.</span> Sequence and completion conditions</h3>
<span class="qa-anchor" id="q-059-a-05"></span><p>Associate a valid vector with a CQ before Set FID 09h. Set/read FID 08h and observe CQE timing alongside interrupts.</p>
<span class="qa-anchor" id="q-059-a-06"></span><p>Settings can complete successfully without defining exact IRQ timing for every workload. PCIe makes parameter use implementation-specific and permits no coalescing implementation.</p>
</section>
<section class="qa-section" id="q-059-s-03" data-answer-section="3"><h3><span>3.</span> Handle unmet conditions</h3>
<span class="qa-anchor" id="q-059-a-07"></span><p>Invalid or unassociated IV in FID 09h should return Invalid Field (0/02h), unlike Create CQ&#x27;s Invalid Interrupt Vector (1/08h).</p>
<span class="qa-anchor" id="q-059-a-16"></span><p>Check readback, CQ mapping, masks and notification behavior. CD=1 does not override an MSI-X mask.</p>
</section>
</div>
<span class="qa-anchor" id="q-059-a-17"></span><span class="qa-anchor" id="q-059-a-08"></span><span class="qa-anchor" id="q-059-a-09"></span><span class="qa-anchor" id="q-059-a-10"></span><span class="qa-anchor" id="q-059-a-11"></span><span class="qa-anchor" id="q-059-a-12"></span><span class="qa-anchor" id="q-059-a-13"></span><span class="qa-anchor" id="q-059-a-14"></span><span class="qa-anchor" id="q-059-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-irqfeat">Base 2.4 §5.2.30.2.1–5.2.30.2.2</a> · <a href="#ref-irq">PCIe Transport 1.4 §3.5</a> · <a href="#ref-create">Base 2.4 §5.3.1–5.3.2</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-featureeffects">Base 2.4 §5.2.13.1.18</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-060" data-question="60" data-answer-kind="compare"><h2><a class="qa-qid" href="#q-060">Q60</a> What do Volatile Write Cache and Write Atomicity Normal control?</h2>
<p class="qa-prompt">Identify the key difference and one case where the alternatives are not interchangeable.</p>
<details class="qa-answer" id="q-060-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-060-a-01">Separate persistence from atomicity: reaching nonvolatile storage is different from updating logical blocks as a defined unit.</p><div class="qa-sections">
<section class="qa-section" id="q-060-s-01" data-answer-section="1"><h3><span>1.</span> What differs</h3>
<span class="qa-anchor" id="q-060-a-02"></span><p>FID 06h controls controller volatile caching; FID 0Ah controls normal atomicity requirements, not the advertised namespace atomic units.</p>
<span class="qa-anchor" id="q-060-a-04"></span><p>With FID 06h.WCE=0, written user data must be persistent. FID 0Ah.DN=1 removes AWUN/NAWUN requirements while retaining AWUPF/NAWUPF.</p>
</section>
<section class="qa-section" id="q-060-s-02" data-answer-section="2"><h3><span>2.</span> How to choose and verify</h3>
<span class="qa-anchor" id="q-060-a-03"></span><p>VWC advertises cache presence; AWUN/AWUPF, namespace overrides and boundaries describe atomicity.</p>
<span class="qa-anchor" id="q-060-a-05"></span><p>Read capabilities/format, Set/Get, then compare allowed outcomes for Writes respecting units/boundaries. Drain first for a clean setting transition.</p>
<span class="qa-anchor" id="q-060-a-06"></span><p>WCE=0 does not make arbitrary-size writes atomic; DN=1 does not make completion persistent. The controls are not substitutes.</p>
</section>
<section class="qa-section" id="q-060-s-03" data-answer-section="3"><h3><span>3.</span> Where the comparison stops</h3>
<span class="qa-anchor" id="q-060-a-07"></span><p>Get/Set FID 06h without volatile cache shall return Invalid Field (0/02h). Other conditions follow applicable command/namespace/atomicity rules.</p>
<span class="qa-anchor" id="q-060-a-16"></span><p>Correlate Current.WCE/DN with the effective atomic units. FUA requests persistence for a command without enlarging its atomic unit.</p>
</section>
</div>
<span class="qa-anchor" id="q-060-a-17"></span><span class="qa-anchor" id="q-060-a-08"></span><span class="qa-anchor" id="q-060-a-09"></span><span class="qa-anchor" id="q-060-a-10"></span><span class="qa-anchor" id="q-060-a-11"></span><span class="qa-anchor" id="q-060-a-12"></span><span class="qa-anchor" id="q-060-a-13"></span><span class="qa-anchor" id="q-060-a-14"></span><span class="qa-anchor" id="q-060-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-vwc">Base 2.4 §5.2.30.1.4</a> · <a href="#ref-nvmfeat">NVM Command Set 1.3 §4.1.3.1–4.1.3.7</a> · <a href="#ref-nvmatomic">NVM Command Set 1.3 §2.1.2–2.1.4</a> · <a href="#ref-idns">NVM Command Set 1.3 §4.1.5.1–4.1.5.4</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-featureeffects">Base 2.4 §5.2.13.1.18</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-061" data-question="61" data-answer-kind="process"><h2><a class="qa-qid" href="#q-061">Q61</a> How does Asynchronous Event Configuration select reported events?</h2>
<p class="qa-prompt">Order the actions and identify which completion must precede the next action.</p>
<details class="qa-answer" id="q-061-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-061-a-01">Select desired change notifications; configuration does not submit an event request on the host&#x27;s behalf.</p><div class="qa-sections">
<section class="qa-section" id="q-061-s-01" data-answer-section="1"><h3><span>1.</span> Prepare the operation</h3>
<span class="qa-anchor" id="q-061-a-02"></span><p>FID 0Bh configures controller notifications about state with various scopes.</p>
<span class="qa-anchor" id="q-061-a-03"></span><p>OAES advertises optional event support, with applicable health capabilities and NVM-specific bit definitions.</p>
<span class="qa-anchor" id="q-061-a-04"></span><p>CDW11 enable bits select notifications. AER completion AET/AEI/LID describes the event; it is not the same bitmap.</p>
</section>
<section class="qa-section" id="q-061-s-02" data-answer-section="2"><h3><span>2.</span> Sequence and completion conditions</h3>
<span class="qa-anchor" id="q-061-a-05"></span><p>Discover support, Set the mask, post AER, observe a condition, read the event/log, acknowledge under its rules and replenish requests.</p>
<span class="qa-anchor" id="q-061-a-06"></span><p>A condition already true when enabled is also reported under this feature&#x27;s rules; reporting is not limited to later state changes.</p>
</section>
<section class="qa-section" id="q-061-s-03" data-answer-section="3"><h3><span>3.</span> Handle unmet conditions</h3>
<span class="qa-anchor" id="q-061-a-07"></span><p>Enabling an unsupported event shall return Invalid Field (0/02h). No outstanding AER can delay notification without being a Set Features error.</p>
<span class="qa-anchor" id="q-061-a-16"></span><p>Correlate OAES, Current mask, pending requests and event masking. An enabled bit alone does not guarantee immediate delivery.</p>
</section>
<section class="qa-section" id="q-061-s-04" data-answer-section="4"><h3><span>4.</span> Asynchronous Event notification conditions</h3>
<span class="qa-anchor" id="q-061-a-09"></span><p>This feature configures notifications, with event-specific conditions and clearing rules. FID 0Bh is not a universal switch for every Error event, and Get Features does not replenish AERs.</p>
</section>
</div>
<span class="qa-anchor" id="q-061-a-17"></span><span class="qa-anchor" id="q-061-a-08"></span><span class="qa-anchor" id="q-061-a-10"></span><span class="qa-anchor" id="q-061-a-11"></span><span class="qa-anchor" id="q-061-a-12"></span><span class="qa-anchor" id="q-061-a-13"></span><span class="qa-anchor" id="q-061-a-14"></span><span class="qa-anchor" id="q-061-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-aec">Base 2.4 §5.2.30.1.6</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-nvmfeat">NVM Command Set 1.3 §4.1.3.1–4.1.3.7</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-featureeffects">Base 2.4 §5.2.13.1.18</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-062" data-question="62" data-answer-kind="compare"><h2><a class="qa-qid" href="#q-062">Q62</a> How do Power Management, APST and Host Controlled Thermal Management differ?</h2>
<p class="qa-prompt">Identify the key difference and one case where the alternatives are not interchangeable.</p>
<details class="qa-answer" id="q-062-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-062-a-01">Separate explicit host power-state selection, idle-driven automatic transitions and temperature-driven power/performance management.</p><div class="qa-sections">
<section class="qa-section" id="q-062-s-01" data-answer-section="1"><h3><span>1.</span> What differs</h3>
<span class="qa-anchor" id="q-062-a-02"></span><p>Configuration targets a controller, while shared-domain controllers can interact in power behavior.</p>
<span class="qa-anchor" id="q-062-a-04"></span><p>FID 02h selects PS and related limits. FID 0Ch.APSTE enables a 32-entry table with ITPT idle milliseconds in that state and ITPS targeting a nonoperational state. FID 10h TMT1/TMT2 use kelvins.</p>
</section>
<section class="qa-section" id="q-062-s-02" data-answer-section="2"><h3><span>2.</span> How to choose and verify</h3>
<span class="qa-anchor" id="q-062-a-03"></span><p>Read NPSS/power-state descriptors, APSTA, HCTMA and MNTMT/MXTMT.</p>
<span class="qa-anchor" id="q-062-a-05"></span><p>Discover states/latencies, select explicit PS or an APST table and separately set legal TMT1&lt;TMT2 when both are nonzero. Each new state uses its own idle-transition condition.</p>
<span class="qa-anchor" id="q-062-a-06"></span><p>Successful FID 02h Set establishes the requested PS, but enabled APST may transition again. HCTM activity is not another host Power Management command.</p>
</section>
<section class="qa-section" id="q-062-s-03" data-answer-section="3"><h3><span>3.</span> Checks across reset or power loss</h3>
<span class="qa-anchor" id="q-062-a-12"></span>
<span class="qa-anchor" id="q-062-a-14"></span>
<div class="qr-table" tabindex="0" role="region" aria-label="Horizontally scrollable comparison table"><table><thead><tr><th scope="col">Trigger</th><th scope="col">Effect on this operation or state</th></tr></thead><tbody><tr><td>What survives or continues after Controller Reset?</td><td>Non-saveable Power Management/APST follows Figure 466 defaults; non-saveable HCTM is persistent. Saveable configurations use Saved rules, with coordination among controllers sharing a domain.</td></tr><tr><td>What survives or continues after a power cycle?</td><td>Do not classify all three as volatile: non-saveable HCTM persists, whereas Power Management/APST do not; saveable features restore Saved.</td></tr></tbody></table></div>
</section>
<section class="qa-section" id="q-062-s-04" data-answer-section="4"><h3><span>4.</span> Where the comparison stops</h3>
<span class="qa-anchor" id="q-062-a-07"></span><p>Unsupported states, invalid APST targets and illegal thermal ranges/order follow the relevant Invalid Field (0/02h) requirements.</p>
<span class="qa-anchor" id="q-062-a-16"></span><p>Compare configuration, operational state, SMART temperature and HCTM counters separately. Lower power alone does not identify APST as the cause.</p>
</section>
</div>
<span class="qa-anchor" id="q-062-a-17"></span><span class="qa-anchor" id="q-062-a-08"></span><span class="qa-anchor" id="q-062-a-09"></span><span class="qa-anchor" id="q-062-a-10"></span><span class="qa-anchor" id="q-062-a-11"></span><span class="qa-anchor" id="q-062-a-13"></span><span class="qa-anchor" id="q-062-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-power">Base 2.4 §5.2.30.1.2, 5.2.30.1.7</a> · <a href="#ref-thermal">Base 2.4 §5.2.30.1.10</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-featureeffects">Base 2.4 §5.2.13.1.18</a> · <a href="#ref-powerstates">Base 2.4 §8.1.19</a> · <a href="#ref-thermalpel">Base 2.4 §5.2.13.1.14.2.13</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-063" data-question="63" data-answer-kind="process"><h2><a class="qa-qid" href="#q-063">Q63</a> How are Timestamp, Keep Alive Timer and Host Memory Buffer configured and verified?</h2>
<p class="qa-prompt">Order the actions and identify which completion must precede the next action.</p>
<details class="qa-answer" id="q-063-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-063-a-01">These provide event time, communication-liveness monitoring and dedicated host memory, requiring different validation methods.</p><div class="qa-sections">
<section class="qa-section" id="q-063-s-01" data-answer-section="1"><h3><span>1.</span> Prepare the operation</h3>
<span class="qa-anchor" id="q-063-a-02"></span><p>Timestamp/Keep Alive are controller time state; HMB also controls ownership/lifetime of host memory.</p>
<span class="qa-anchor" id="q-063-a-03"></span><p>Check ONCS for Timestamp, KAS/CTRATT.TBKAS for Keep Alive, and HMPRE/HMMIN/HMMINDS/HMMAXD for HMB.</p>
<span class="qa-anchor" id="q-063-a-04"></span><p>FID 0Eh sets a 48-bit millisecond Timestamp in an 8-byte buffer. FID 0Fh sets KATO milliseconds rounded up to KAS×100 ms. FID 0Dh configures EHM/MR, HSIZE and descriptor address/count.</p>
</section>
<section class="qa-section" id="q-063-s-02" data-answer-section="2"><h3><span>2.</span> Sequence and completion conditions</h3>
<span class="qa-anchor" id="q-063-a-05"></span><p>Timestamp Get should reflect elapsed time; KATO Get returns the rounded value. Allocate valid HMB pages before enabling and reclaim only after successful disable. MR=1 requires unchanged contents and descriptors as well as layout.</p>
<span class="qa-anchor" id="q-063-a-06"></span><p>KAS=10 rounds requested KATO1500 ms to 2000 ms. HMB Get returns CQE state and an attributes buffer, not only an enable bit.</p>
</section>
<section class="qa-section" id="q-063-s-03" data-answer-section="3"><h3><span>3.</span> Handle unmet conditions</h3>
<span class="qa-anchor" id="q-063-a-07"></span><p>Re-enabling enabled HMB returns 0/0Ch; HMDLEC=0 returns 0/02h. PCIe allows KATO=0 to disable; do not import another transport&#x27;s mandatory-enablement rule.</p>
<span class="qa-anchor" id="q-063-a-16"></span><p>Check Timestamp Origin/Synch rather than assuming a perfect wall clock, rounded KATO Current and HMB support/configuration/EHM/memory retention.</p>
</section>
</div>
<span class="qa-anchor" id="q-063-a-17"></span><span class="qa-anchor" id="q-063-a-08"></span><span class="qa-anchor" id="q-063-a-09"></span><span class="qa-anchor" id="q-063-a-10"></span><span class="qa-anchor" id="q-063-a-11"></span><span class="qa-anchor" id="q-063-a-12"></span><span class="qa-anchor" id="q-063-a-13"></span><span class="qa-anchor" id="q-063-a-14"></span><span class="qa-anchor" id="q-063-a-15"></span>
<p class="qa-related">Related mechanisms: <a href="/nvme/question-bank/persistent-events/en/#q-216">Q216</a> · <a href="/nvme/question-bank/keep-alive/en/#q-221">Q221</a> · <a href="/nvme/question-bank/memory/en/#q-226">Q226</a></p>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-timestamp">Base 2.4 §5.2.30.1.8</a> · <a href="#ref-keepalive">Base 2.4 §3.9 (common and PCIe rules), 5.2.30.1.9</a> · <a href="#ref-hmb">Base 2.4 §5.2.30.2.3, 8.2.4</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-featureeffects">Base 2.4 §5.2.13.1.18</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-064" data-question="64" data-answer-kind="compare"><h2><a class="qa-qid" href="#q-064">Q64</a> What do Host Behavior Support, Error Recovery and Read Recovery Level do?</h2>
<p class="qa-prompt">Identify the key difference and one case where the alternatives are not interchangeable.</p>
<details class="qa-answer" id="q-064-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-064-a-01">Advertise host understanding of extensions, configure namespace error recovery and choose a read-recovery strategy.</p><div class="qa-sections">
<section class="qa-section" id="q-064-s-01" data-answer-section="1"><h3><span>1.</span> What differs</h3>
<span class="qa-anchor" id="q-064-a-02"></span><p>FID 16h is controller-scoped, FID 05h namespace-scoped, and FID 12h set/subsystem-scoped according to NVM Set support.</p>
<span class="qa-anchor" id="q-064-a-04"></span><p>FID 16h payload includes ACRE/LBAFEE. FID 05h TLER uses 100 ms and DULBE bit 16. FID 12h RRL is a level code, not the RRLS bitmap.</p>
</section>
<section class="qa-section" id="q-064-s-02" data-answer-section="2"><h3><span>2.</span> How to choose and verify</h3>
<span class="qa-anchor" id="q-064-a-03"></span><p>Pair ACRE with relevant capabilities, check NSFEAT.DAE before DULBE and RRLS before selecting a recovery level.</p>
<span class="qa-anchor" id="q-064-a-05"></span><p>Discover support before Set. TLER starts when error recovery begins, not at command submission as a universal timeout. Set/read an advertised RRL for the correct target.</p>
<span class="qa-anchor" id="q-064-a-06"></span><p>ACRE enables applicable advanced retry behavior; DULBE changes unwritten/deallocated-block responses. Fast Fail does not promise fixed latency or zero internal attempts.</p>
</section>
<section class="qa-section" id="q-064-s-03" data-answer-section="3"><h3><span>3.</span> Checks across reset or power loss</h3>
<span class="qa-anchor" id="q-064-a-12"></span>
<span class="qa-anchor" id="q-064-a-14"></span>
<div class="qr-table" tabindex="0" role="region" aria-label="Horizontally scrollable comparison table"><table><thead><tr><th scope="col">Trigger</th><th scope="col">Effect on this operation or state</th></tr></thead><tbody><tr><td>What survives or continues after Controller Reset?</td><td>Non-saveable Host Behavior Support and Error Recovery are nonpersistent, while Read Recovery Level persists. Saveable cases follow Saved and scope-dependent reset rules.</td></tr><tr><td>What survives or continues after a power cycle?</td><td>Re-read Current after a power cycle. Non-saveable RRL still persists; absence of Saved does not mean it must return zero. Host Behavior Support/Error Recovery use their separate restoration rules.</td></tr></tbody></table></div>
</section>
<section class="qa-section" id="q-064-s-04" data-answer-section="4"><h3><span>4.</span> Where the comparison stops</h3>
<span class="qa-anchor" id="q-064-a-07"></span><p>Unsupported levels/invalid settings follow 0/02h and applicable rules. Command Interrupted 0/21h requires ACRE=1 and DNR=0.</p>
<span class="qa-anchor" id="q-064-a-16"></span><p>LBAFEE affects exposure/use of extended formats; interpret capability, host declaration and namespace format together.</p>
</section>
</div>
<span class="qa-anchor" id="q-064-a-17"></span><span class="qa-anchor" id="q-064-a-08"></span><span class="qa-anchor" id="q-064-a-09"></span><span class="qa-anchor" id="q-064-a-10"></span><span class="qa-anchor" id="q-064-a-11"></span><span class="qa-anchor" id="q-064-a-13"></span><span class="qa-anchor" id="q-064-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-behavior">Base 2.4 §5.2.30.1.15</a> · <a href="#ref-nvmfeat">NVM Command Set 1.3 §4.1.3.1–4.1.3.7</a> · <a href="#ref-rrl">Base 2.4 §5.2.30.1.12, 8.1.23</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-featureeffects">Base 2.4 §5.2.13.1.18</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-065" data-question="65" data-answer-kind="process"><h2><a class="qa-qid" href="#q-065">Q65</a> How is namespace write protection configured, and which modes survive reset or power cycling?</h2>
<p class="qa-prompt">Order the actions and identify which completion must precede the next action.</p>
<details class="qa-answer" id="q-065-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-065-a-01">Prevent namespace modification with reversible, until-power-cycle and permanent protection lifetimes.</p><div class="qa-sections">
<section class="qa-section" id="q-065-s-01" data-answer-section="1"><h3><span>1.</span> Prepare the operation</h3>
<span class="qa-anchor" id="q-065-a-02"></span><p>Protection belongs to the namespace and applies through other controllers accessing it, not just one queue&#x27;s software flag.</p>
<span class="qa-anchor" id="q-065-a-03"></span><p>NWPC advertises capability, WPC.WPUPCC/PWPC permits entering specific modes and Get FID 84h.WPS reports current state.</p>
<span class="qa-anchor" id="q-065-a-04"></span><p>WPS0/1/2/3 means none/basic/until-power-cycle/permanent. This feature is unsaveable and has no Default; SV=1 does not create persistence.</p>
</section>
<section class="qa-section" id="q-065-s-02" data-answer-section="2"><h3><span>2.</span> Sequence and completion conditions</h3>
<span class="qa-anchor" id="q-065-a-05"></span><p>Check support/entry permission, Set WPS for NSID and read Current. Entering protection commits that namespace&#x27;s volatile data/metadata to nonvolatile media.</p>
<span class="qa-anchor" id="q-065-a-06"></span><p>After success, prohibited operations must obey protection rules while ordinary reads remain governed by readable state. Verify behavior in addition to Set success.</p>
</section>
<section class="qa-section" id="q-065-s-03" data-answer-section="3"><h3><span>3.</span> Checks across reset or power loss</h3>
<span class="qa-anchor" id="q-065-a-12"></span>
<span class="qa-anchor" id="q-065-a-13"></span>
<span class="qa-anchor" id="q-065-a-14"></span>
<div class="qr-table" tabindex="0" role="region" aria-label="Horizontally scrollable comparison table"><table><thead><tr><th scope="col">Trigger</th><th scope="col">Effect on this operation or state</th></tr></thead><tbody><tr><td>What survives or continues after Controller Reset?</td><td>Controller Reset preserves existing WPS, including Until Power Cycle; unsaveability does not remove protection.</td></tr><tr><td>What survives or continues after NVM Subsystem Reset?</td><td>NVM Subsystem Reset is not a power cycle; WPS follows its state machine. NSSR is not a method to remove Until Power Cycle protection.</td></tr><tr><td>What survives or continues after a power cycle?</td><td>An actual power cycle returns WPS2 to No Write Protect; basic WPS1 and permanent WPS3 persist. Ordinary Set/reset cannot remove permanent protection.</td></tr></tbody></table></div>
</section>
<section class="qa-section" id="q-065-s-04" data-answer-section="4"><h3><span>4.</span> Handle unmet conditions</h3>
<span class="qa-anchor" id="q-065-a-07"></span><p>Changing WPS2/3, missing entry permission or prohibited multi-domain WPS2 transition uses 1/0Eh; Get Default uses 0/02h; prohibited commands may return Namespace is Write Protected 0/20h.</p>
<span class="qa-anchor" id="q-065-a-16"></span><p>CHANG=1 does not promise reversal of permanent protection. Reset of WPC permission bits differs from the namespace&#x27;s existing WPS state.</p>
</section>
</div>
<span class="qa-anchor" id="q-065-a-17"></span><span class="qa-anchor" id="q-065-a-08"></span><span class="qa-anchor" id="q-065-a-09"></span><span class="qa-anchor" id="q-065-a-10"></span><span class="qa-anchor" id="q-065-a-11"></span><span class="qa-anchor" id="q-065-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-nwp">Base 2.4 §5.2.30.1.38, 8.1.18</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-featureeffects">Base 2.4 §5.2.13.1.18</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-066" data-question="66" data-answer-kind="process"><h2><a class="qa-qid" href="#q-066">Q66</a> Why read Get Features after a successful Set Features?</h2>
<p class="qa-prompt">Order the actions and identify which completion must precede the next action.</p>
<details class="qa-answer" id="q-066-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-066-a-01">Verify transformations between the requested and effective value rather than relying only on success status.</p><div class="qa-sections">
<section class="qa-section" id="q-066-s-01" data-answer-section="1"><h3><span>1.</span> Prepare the operation</h3>
<span class="qa-anchor" id="q-066-a-02"></span><p>Compare identical FID/scope/selectors and time; Supported Capabilities is not Current.</p>
<span class="qa-anchor" id="q-066-a-03"></span><p>Know the response format and support; values may be in CQE, a payload or both.</p>
<span class="qa-anchor" id="q-066-a-04"></span><p>Preserve original SV/parameters and Set results, read Current with SEL 0 and Saved with SEL 2 when needed.</p>
</section>
<section class="qa-section" id="q-066-s-02" data-answer-section="2"><h3><span>2.</span> Sequence and completion conditions</h3>
<span class="qa-anchor" id="q-066-a-05"></span><p>Await successful Set before Get and coordinate concurrent shared-scope writers. Compare dynamic values such as Timestamp with elapsed time rather than byte equality.</p>
<span class="qa-anchor" id="q-066-a-06"></span><p>Successful Set completion cannot precede completion of attribute setting. Rounded KATO and allocated queue counts may validly differ from requests.</p>
</section>
<section class="qa-section" id="q-066-s-03" data-answer-section="3"><h3><span>3.</span> Handle unmet conditions</h3>
<span class="qa-anchor" id="q-066-a-07"></span><p>A later Get failure has its own status and does not replace the Set result. Check selectors, scope and intervening reset.</p>
<span class="qa-anchor" id="q-066-a-16"></span><p>Readback establishes reported configuration; behavioral checks establish its use. Both are needed, without duplicating the same comparison as separate tests.</p>
</section>
</div>
<span class="qa-anchor" id="q-066-a-17"></span><span class="qa-anchor" id="q-066-a-08"></span><span class="qa-anchor" id="q-066-a-09"></span><span class="qa-anchor" id="q-066-a-10"></span><span class="qa-anchor" id="q-066-a-11"></span><span class="qa-anchor" id="q-066-a-12"></span><span class="qa-anchor" id="q-066-a-13"></span><span class="qa-anchor" id="q-066-a-14"></span><span class="qa-anchor" id="q-066-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-getfeat">Base 2.4 §5.2.12</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-setcomplete">Base 2.4 §5.2.30 (Command Completion)</a> · <a href="#ref-keepalive">Base 2.4 §3.9 (common and PCIe rules), 5.2.30.1.9</a> · <a href="#ref-number">Base 2.4 §5.2.30.1.5</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-featureeffects">Base 2.4 §5.2.13.1.18</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-067" data-question="67" data-answer-kind="lifecycle"><h2><a class="qa-qid" href="#q-067">Q67</a> How should features change after activation, namespace deletion, reset and power cycling?</h2>
<p class="qa-prompt">Name the reset or interruption, then assess settings, ongoing operations and data separately.</p>
<details class="qa-answer" id="q-067-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-067-a-01">Establish persistence expectations per event and feature instead of assuming universal clearing or retention.</p><div class="qa-sections">
<section class="qa-section" id="q-067-s-01" data-answer-section="1"><h3><span>1.</span> Identify the trigger and affected objects</h3>
<span class="qa-anchor" id="q-067-a-02"></span><p>Separate controller, namespace and shared-object scope, then Current/Saved/Default.</p>
<span class="qa-anchor" id="q-067-a-03"></span><p>Check SVBL, Figure 466/NVM Figure 92 and feature-specific exceptions. Unsaveable and nonpersistent are not synonyms.</p>
</section>
<section class="qa-section" id="q-067-s-02" data-answer-section="2"><h3><span>2.</span> State changes and recovery</h3>
<span class="qa-anchor" id="q-067-a-04"></span><p>Record actual CLR occurrence and coverage. Namespace deletion removes an object; a new namespace reusing its number is not automatically the same configured object.</p>
<span class="qa-anchor" id="q-067-a-05"></span><p>Snapshot, perform the defined event, restore management access, reread values/capabilities and verify behavior. For activation, identify its actual activation/reset path.</p>
<span class="qa-anchor" id="q-067-a-06"></span><p>An SV=0 change to a saveable feature can revert to older Saved after reset; HMB needs reconfiguration; WPS2 survives Controller Reset but ends at a power cycle.</p>
</section>
<section class="qa-section" id="q-067-s-03" data-answer-section="3"><h3><span>3.</span> Verify retention and recovery</h3>
<span class="qa-anchor" id="q-067-a-07"></span><p>Access after object deletion follows that FID&#x27;s NSID rules; failure to read a deleted namespace is not evidence of failed saving.</p>
<span class="qa-anchor" id="q-067-a-16"></span><p>Preserve object identity, SV, scope, reset cause and timing, not merely a changed-value flag.</p>
<span class="qa-anchor" id="q-067-a-17"></span><p>First confirm the same object and the actual reset coverage.</p>
</section>
</div>
<span class="qa-anchor" id="q-067-a-08"></span><span class="qa-anchor" id="q-067-a-09"></span><span class="qa-anchor" id="q-067-a-10"></span><span class="qa-anchor" id="q-067-a-11"></span><span class="qa-anchor" id="q-067-a-12"></span><span class="qa-anchor" id="q-067-a-13"></span><span class="qa-anchor" id="q-067-a-14"></span><span class="qa-anchor" id="q-067-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-timestamp">Base 2.4 §5.2.30.1.8</a> · <a href="#ref-hmb">Base 2.4 §5.2.30.2.3, 8.2.4</a> · <a href="#ref-nwp">Base 2.4 §5.2.30.1.38, 8.1.18</a> · <a href="#ref-nsmanage">Base 2.4 §5.2.24–5.2.25, 8.1.17</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-featureeffects">Base 2.4 §5.2.13.1.18</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-068" data-question="68" data-answer-kind="diagnose"><h2><a class="qa-qid" href="#q-068">Q68</a> How should supported-feature claims be checked when Get, Set and behavior appear inconsistent?</h2>
<p class="qa-prompt">Separate available evidence from missing information before judging conformance.</p>
<details class="qa-answer" id="q-068-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-068-a-01">Isolate whether the contradiction lies in capability, configuration, observation or firmware behavior under reproducible conditions.</p><div class="qa-sections">
<section class="qa-section" id="q-068-s-01" data-answer-section="1"><h3><span>1.</span> Preserve the evidence first</h3>
<span class="qa-anchor" id="q-068-a-02"></span><p>Fix controller, FID, NSID/other selectors and configuration interval to avoid mixing scopes.</p>
<span class="qa-anchor" id="q-068-a-03"></span><p>Compare Identify, feature-effects information and SEL 3. NSSPEC=0 is not necessarily controller scope; CHANG=1 is not unconditional changeability.</p>
<span class="qa-anchor" id="q-068-a-04"></span><p>Preserve FID/SEL/SV/CDW11/payloads and CQEs, and identify commands already outstanding before behavioral checks.</p>
</section>
<section class="qa-section" id="q-068-s-02" data-answer-section="2"><h3><span>2.</span> Work through the possible causes</h3>
<span class="qa-anchor" id="q-068-a-17"></span><p>First check wrong SEL/NSID or behavioral test commands submitted before Set completed.</p>
<span class="qa-anchor" id="q-068-a-05"></span><p>Discover, legally Set, await completion, Get Current and submit new affected work; test saving/reset separately, changing one factor at a time.</p>
</section>
<section class="qa-section" id="q-068-s-03" data-answer-section="3"><h3><span>3.</span> Decide what the evidence supports</h3>
<span class="qa-anchor" id="q-068-a-06"></span><p>Consistency means conformance to allowed outcomes. Rounded KATO, dynamic Timestamp and implementation-specific coalescing cannot be rejected simply for differing from a request.</p>
<span class="qa-anchor" id="q-068-a-07"></span><p>First distinguish unsupported FID 0/02h, unsaveable 1/0Dh, unchangeable 1/0Eh and wrong-scope 1/0Fh; retain allowed status choices for multiple faults.</p>
<span class="qa-anchor" id="q-068-a-16"></span><p>A noncompliance finding should include the explicit requirement, established prerequisites, raw request/response and evidence excluding selector/timing misuse.</p>
</section>
</div>
<span class="qa-anchor" id="q-068-a-08"></span><span class="qa-anchor" id="q-068-a-09"></span><span class="qa-anchor" id="q-068-a-10"></span><span class="qa-anchor" id="q-068-a-11"></span><span class="qa-anchor" id="q-068-a-12"></span><span class="qa-anchor" id="q-068-a-13"></span><span class="qa-anchor" id="q-068-a-14"></span><span class="qa-anchor" id="q-068-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-getfeat">Base 2.4 §5.2.12</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-setcomplete">Base 2.4 §5.2.30 (Command Completion)</a> · <a href="#ref-irqfeat">Base 2.4 §5.2.30.2.1–5.2.30.2.2</a> · <a href="#ref-effects">Base 2.4 §5.2.13.1.6</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-featureeffects">Base 2.4 §5.2.13.1.18</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>

<section id="source-index"><h2>Source locations and existing figure guides</h2><p>Base printed page = PDF page−26; the other two use identical numbers. Locations follow the supplied PDF body and retain figure numbers. Shared pages contribute only the relevant definitions, excluding Fabrics and PCIe link/packet content.</p><ul class="qa-references">
<li id="ref-reset"><strong>Base 2.4 · §3.7.1–3.7.4</strong><br>Printed pages 120–124 · PDF 146–150</li>
<li id="ref-keepalive"><strong>Base 2.4 · §3.9 (common and PCIe rules), 5.2.30.1.9</strong><br>Printed pages 129–135, 471 · PDF 155–161, 497 · Figure 481</li>
<li id="ref-status"><strong>Base 2.4 · §4.2.3</strong><br>Printed pages 145–155 · PDF 171–181 · Figure 101–105</li>
<li id="ref-feature"><strong>Base 2.4 · §4.4</strong><br>Printed pages 166–169 · PDF 192–195 · Figure 126–127</li>
<li id="ref-aer"><strong>Base 2.4 · §5.2.2</strong><br>Printed pages 183–190 · PDF 209–216 · Figure 150–156</li>
<li id="ref-getfeat"><strong>Base 2.4 · §5.2.12</strong><br>Printed pages 209–212 · PDF 235–238 · Figure 197–202</li>
<li id="ref-error"><strong>Base 2.4 · §5.2.13.1.2</strong><br>Printed pages 218–220 · PDF 244–246 · Figure 212</li>
<li id="ref-effects"><strong>Base 2.4 · §5.2.13.1.6</strong><br>Printed pages 226–229 · PDF 252–255 · Figure 216–217</li>
<li id="ref-pel"><strong>Base 2.4 · §5.2.13.1.14 (header, reset, hardware, Set Feature events)</strong><br>Printed pages 244–256, 258, 262–264 · PDF 270–282, 284, 288–290 · Figure 232–244, 246, 252–253</li>
<li id="ref-thermalpel"><strong>Base 2.4 · §5.2.13.1.14.2.13</strong><br>Printed pages 265–266 · PDF 291–292 · Figure 255</li>
<li id="ref-featureeffects"><strong>Base 2.4 · §5.2.13.1.18</strong><br>Printed pages 276–278 · PDF 302–304 · Figure 270–271</li>
<li id="ref-idctrl"><strong>Base 2.4 · §5.2.14.2.1</strong><br>Printed pages 340–387 · PDF 366–413 · Figure 338–341</li>
<li id="ref-idlist"><strong>Base 2.4 · §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</strong><br>Printed pages 387–399, 402–404 · PDF 413–425, 428–430 · Figure 342–355, 360–362</li>
<li id="ref-nsmanage"><strong>Base 2.4 · §5.2.24–5.2.25, 8.1.17</strong><br>Printed pages 442–448, 660–664 · PDF 468–474, 686–690 · Figure 442–450</li>
<li id="ref-setfeat"><strong>Base 2.4 · §5.2.30.1 (common fields, scope and persistence)</strong><br>Printed pages 456–460 · PDF 482–486 · Figure 463–466</li>
<li id="ref-arbit"><strong>Base 2.4 · §5.2.30.1.1</strong><br>Printed pages 460 · PDF 486 · Figure 467</li>
<li id="ref-power"><strong>Base 2.4 · §5.2.30.1.2, 5.2.30.1.7</strong><br>Printed pages 460–462, 468–469 · PDF 486–488, 494–495 · Figure 468–469, 475–478</li>
<li id="ref-vwc"><strong>Base 2.4 · §5.2.30.1.4</strong><br>Printed pages 464–465 · PDF 490–491 · Figure 471</li>
<li id="ref-number"><strong>Base 2.4 · §5.2.30.1.5</strong><br>Printed pages 465–466 · PDF 491–492 · Figure 472–473</li>
<li id="ref-aec"><strong>Base 2.4 · §5.2.30.1.6</strong><br>Printed pages 466–468 · PDF 492–494 · Figure 474</li>
<li id="ref-timestamp"><strong>Base 2.4 · §5.2.30.1.8</strong><br>Printed pages 469–471 · PDF 495–497 · Figure 479–480</li>
<li id="ref-thermal"><strong>Base 2.4 · §5.2.30.1.10</strong><br>Printed pages 471–472 · PDF 497–498 · Figure 482</li>
<li id="ref-rrl"><strong>Base 2.4 · §5.2.30.1.12, 8.1.23</strong><br>Printed pages 473, 689–690 · PDF 499, 715–716 · Figure 484–485, 755</li>
<li id="ref-behavior"><strong>Base 2.4 · §5.2.30.1.15</strong><br>Printed pages 475–477 · PDF 501–503 · Figure 491</li>
<li id="ref-profile"><strong>Base 2.4 · §5.2.30.1.18</strong><br>Printed pages 478–479 · PDF 504–505 · Figure 494–495</li>
<li id="ref-nwp"><strong>Base 2.4 · §5.2.30.1.38, 8.1.18</strong><br>Printed pages 512, 664–666 · PDF 538, 690–692 · Figure 541, 735–737</li>
<li id="ref-irqfeat"><strong>Base 2.4 · §5.2.30.2.1–5.2.30.2.2</strong><br>Printed pages 514–515 · PDF 540–541 · Figure 543–544</li>
<li id="ref-hmb"><strong>Base 2.4 · §5.2.30.2.3, 8.2.4</strong><br>Printed pages 515–519, 744 · PDF 541–545, 770 · Figure 545–553</li>
<li id="ref-setcomplete"><strong>Base 2.4 · §5.2.30 (Command Completion)</strong><br>Printed pages 519 · PDF 545 · Figure 554</li>
<li id="ref-create"><strong>Base 2.4 · §5.3.1–5.3.2</strong><br>Printed pages 527–531 · PDF 553–557 · Figure 571–579</li>
<li id="ref-powerstates"><strong>Base 2.4 · §8.1.19</strong><br>Printed pages 666–672 · PDF 692–698 · Figure 738–740</li>
<li id="ref-nvmatomic"><strong>NVM Command Set 1.3 · §2.1.2–2.1.4</strong><br>Printed pages 14–20 · PDF 14–20 · Figure 3–9</li>
<li id="ref-nvmfeat"><strong>NVM Command Set 1.3 · §4.1.3.1–4.1.3.7</strong><br>Printed pages 64–69 · PDF 64–69 · Figure 92–101</li>
<li id="ref-idns"><strong>NVM Command Set 1.3 · §4.1.5.1–4.1.5.4</strong><br>Printed pages 84–107 · PDF 84–107 · Figure 123–130</li>
<li id="ref-irq"><strong>PCIe Transport 1.4 · §3.5</strong><br>Printed pages 13–16 · PDF 13–16 · Figure 9</li>
</ul><h3>When you need a field guide</h3><p>Existing figure explanations have canonical locations; use these links instead of duplicating the same guide.</p><ul>
<li><a href="/nvme/figure-reference/command/en/#figure-b101">Base 2.4 Figure 101 · Completion Queue Entry: Status Field</a></li>
<li><a href="/nvme/figure-reference/command/en/#figure-b104">Base 2.4 Figure 104 · Status Code – Command Specific Status Values</a></li>
<li><a href="/nvme/figure-reference/identify/en/#figure-b338">Base 2.4 Figure 338 · Identify – Identify Controller Data Structure, I/O Command Set Independent</a></li>
<li><a href="/nvme/figure-reference/features/en/#figure-b473">Base 2.4 Figure 473 · Number of Queues – Completion Queue Entry Dword 0</a></li>
<li><a href="/nvme/figure-reference/features/en/#figure-b543">Base 2.4 Figure 543 · Interrupt Coalescing – Command Dword 11</a></li>
<li><a href="/nvme/figure-reference/identify/en/#figure-n123">NVM Command Set 1.3 Figure 123 · Identify – Identify Namespace Data Structure, NVM Command Set</a></li>
</ul><details><summary>Original documents used</summary><ul class="qr-sources">
<li>NVM Express Base Specification · Revision 2.4 · 2026-07-31<br><code>NVM-Express-Base-Specification-Revision-2.4-Ratified-2026.07.31.pdf</code></li>
<li>NVM Express NVM Command Set Specification · Revision 1.3 · 2026-07-31<br><code>NVM-Express-NVM-Command-Set-Specification-Revision-1.3-Ratified-2026.07.31.pdf</code></li>
<li>NVM Express NVMe over PCIe Transport Specification · Revision 1.4 · 2026-07-31<br><code>NVM-Express-NVMe-over-PCIe-Transport-Specification-Revision-1.4-Ratified-2026.07.31.pdf</code></li>
</ul></details></section>
</main>
<nav class="qr-top" aria-label="Bank and editions"><a href="#content">Skip to content</a><a href="/nvme/question-bank/en/">Question index</a><a href="/nvme/question-bank/features/zh-tw/">繁體中文</a><a href="/DOCS/nvme-question-bank/features.html">Chinese tutorial HTML</a></nav>
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
