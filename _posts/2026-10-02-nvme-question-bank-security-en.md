---
layout: post
title: "NVMe Self-Study Bank: Security and Lockdown"
date: 2026-10-02 00:00:00 +0800
categories: [nvme]
permalink: /nvme/question-bank/security/en/
lang: en
nvme_quickref: true
nvme_qa: true
---

<div class="nvme-quickref nvme-qa">
<nav class="qr-top" aria-label="Bank and editions"><a href="#content">Skip to content</a><a href="/nvme/question-bank/en/">Question index</a><a href="/nvme/question-bank/security/zh-tw/">繁體中文</a><a href="/DOCS/nvme-question-bank/security.html">Chinese tutorial HTML</a></nav>
<main id="content"><p class="qr-eyebrow">BASE 2.4 / NVM 1.3 / PCIe 1.4 · Q1–328</p>
<header><p class="qa-range">Q237–Q245</p><h1>Security and Lockdown</h1><p class="qr-intro">Security commands transport protocol data; Lockdown prohibits selected operations. Separate protocol results, prohibition scope and persistence.</p><p>Practice first, then reveal the explanation. Each question uses the prose, field interpretation, comparison or flow that suits it. All numerical examples are hypothetical. Status is written SCT/SC; h indicates hexadecimal.</p></header>
<aside class="qa-glossary"><h2>Terms used in this volume</h2><dl><dt>Controller / namespace</dt><dd>A controller receives commands and manages access. A namespace is a logical storage space that commands can address. An NVM subsystem contains controllers and nonvolatile storage resources.</dd><dt>SQ / CQ / SQE / CQE</dt><dd>Submission and Completion Queues carry command entries (SQEs) and completion entries (CQEs). QID identifies a queue, CID distinguishes outstanding commands in one SQ, and NSID identifies a namespace.</dd><dt>Register / Identify / Feature / Log</dt><dd>A register exposes control or state. Identify queries capabilities and attributes; features query or configure operation; log pages report specific state or records. FID, LID, CNS and CSI select features, logs, Identify structures and command sets.</dd><dt>index / offset / zero-based</dt><dd>An index selects an entry, usually starting at 0; an offset measures distance from an origin in specified units. A zero-based count encodes count−1, but not every zero-valued field is a count. A Dword is 4 bytes; a byte is 8 bits.</dd><dt>Scope / reset / retention</dt><dd>Scope names the affected objects; retention means preserving state. Controller Reset (clearing CC.EN) is one form of Controller Level Reset, or CLR. Different CLR triggers can retain different registers.</dd></dl></aside>
<section id="overview" class="qa-overview"><h2>Transport, protocol and permission are distinct</h2><p class="qa-takeaway">NVMe success is not authentication success, and prohibiting Set does not automatically prohibit Get.</p>
<div class="qr-table" tabindex="0" role="region" aria-label="Horizontally scrollable comparison table"><table><thead><tr><th scope="col">Question</th><th scope="col">Evidence</th><th scope="col">Where the answer resides</th></tr></thead><tbody><tr><td>Was data exchanged?</td><td>Security CQE</td><td>NVMe completion</td></tr><tr><td>Did authentication succeed?</td><td>Protocol selectors/payload</td><td>Selected protocol</td></tr><tr><td>Is it prohibited?</td><td>Interface/scope/list</td><td>Prohibition and target completion</td></tr><tr><td>Does it survive power loss?</td><td>CSEL and LDPE</td><td>Scope-specific persistence</td></tr></tbody></table></div>
<p><strong>Worked interpretation: </strong>CSEL0 with LDPE1 persists, while CSEL1/2 do not gain that persistence from LDPE.</p>
<p class="qa-citations">Sources: <a href="#ref-security">Base 2.4 §5.2.28–5.2.29</a> · <a href="#ref-lockdown">Base 2.4 §5.2.16, 8.1.5</a> · <a href="#ref-locklog">Base 2.4 §5.2.13.1.20</a> · <a href="#ref-lockpersist">Base 2.4 §5.2.30.1.25.4–5.2.30.1.25.4.1</a></p>
</section>
<div class="qa-controls" hidden><label>Search this page <input type="search" id="qa-search" placeholder="Question number, field or keyword"></label><button type="button" data-expand="true">Expand all answers</button><button type="button" data-expand="false">Collapse all answers</button><output id="qa-count" aria-live="polite"></output></div>
<section id="question-index"><h2>Questions in this volume</h2><ol class="qa-index">
<li><a href="#q-237">Q237 · How are Security Send/Receive and protocols discovered?</a></li>
<li><a href="#q-238">Q238 · How are invalid security selectors or lengths handled?</a></li>
<li><a href="#q-239">Q239 · How are security transfer and protocol failures distinguished?</a></li>
<li><a href="#q-240">Q240 · How can security state affect other Admin commands?</a></li>
<li><a href="#q-241">Q241 · Does security state survive reset or power cycle?</a></li>
<li><a href="#q-242">Q242 · How does Lockdown restrict commands or features?</a></li>
<li><a href="#q-243">Q243 · What response is required for a prohibited command or feature?</a></li>
<li><a href="#q-244">Q244 · How are normal and enhanced Lockdown logs interpreted?</a></li>
<li><a href="#q-245">Q245 · Does Lockdown survive resets and power cycles?</a></li>
</ol></section>
<article class="qa-question" id="q-237" data-question="237" data-answer-kind="lookup"><h2><a class="qa-qid" href="#q-237">Q237</a> How are Security Send/Receive and protocols discovered?</h2>
<p class="qa-prompt">Choose the interface and target, then identify the returned field that supports your conclusion.</p>
<details class="qa-answer" id="q-237-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-237-a-01">NVMe command support and security-protocol support are separate capability layers.</p><div class="qa-sections">
<section class="qa-section" id="q-237-s-01" data-answer-section="1"><h3><span>1.</span> Select the target and information</h3>
<span class="qa-anchor" id="q-237-a-02"></span><p>OACS describes commands; discovery identifies supported SECP values.</p>
<span class="qa-anchor" id="q-237-a-03"></span><p>Check the OACS support bit and Commands Supported and Effects.</p>
<span class="qa-anchor" id="q-237-a-04"></span><p>Security Receive SECP00h discovers protocols without a prior Security Send.</p>
</section>
<section class="qa-section" id="q-237-s-02" data-answer-section="2"><h3><span>2.</span> Query sequence and interpretation</h3>
<span class="qa-anchor" id="q-237-a-05"></span><p>Discover first, then encode selectors/lengths and protocol-specific exchange ordering.</p>
<span class="qa-anchor" id="q-237-a-06"></span><p>Successful discovery identifies protocols, not authentication success.</p>
</section>
<section class="qa-section" id="q-237-s-03" data-answer-section="3"><h3><span>3.</span> Handle missing or inconsistent evidence</h3>
<span class="qa-anchor" id="q-237-a-07"></span><p>Unsupported Receive SECP requires Invalid Field; unsupported Opcode is a different layer.</p>
<span class="qa-anchor" id="q-237-a-16"></span><p>Command support does not promise every SECP.</p>
<span class="qa-anchor" id="q-237-a-17"></span><p>First locate failure at command or protocol selection level.</p>
</section>
</div>
<span class="qa-anchor" id="q-237-a-08"></span><span class="qa-anchor" id="q-237-a-09"></span><span class="qa-anchor" id="q-237-a-10"></span><span class="qa-anchor" id="q-237-a-11"></span><span class="qa-anchor" id="q-237-a-12"></span><span class="qa-anchor" id="q-237-a-13"></span><span class="qa-anchor" id="q-237-a-14"></span><span class="qa-anchor" id="q-237-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-security">Base 2.4 §5.2.28–5.2.29</a> · <a href="#ref-lockdown">Base 2.4 §5.2.16, 8.1.5</a> · <a href="#ref-locklog">Base 2.4 §5.2.13.1.20</a> · <a href="#ref-lockpersist">Base 2.4 §5.2.30.1.25.4–5.2.30.1.25.4.1</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-238" data-question="238" data-answer-kind="error"><h2><a class="qa-qid" href="#q-238">Q238</a> How are invalid security selectors or lengths handled?</h2>
<p class="qa-prompt">Distinguish failure conditions before deciding whether a particular response is required.</p>
<details class="qa-answer" id="q-238-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-238-a-01">Separate outer NVMe fields from inner protocol data to predict the right response.</p><div class="qa-sections">
<section class="qa-section" id="q-238-s-01" data-answer-section="1"><h3><span>1.</span> Distinguish the failure conditions</h3>
<span class="qa-anchor" id="q-238-a-02"></span><p>Selectors, pointers and lengths matter; protocol definitions govern payload validity.</p>
<span class="qa-anchor" id="q-238-a-04"></span><p>AL/TL follow Security Protocol In/Out with INC_512=0, not generic zero-based Dword counts.</p>
<span class="qa-anchor" id="q-238-a-07"></span><p>Unsupported Receive/reserved Send SECP requires Invalid Field; inner authentication failure may be a protocol result rather than those CQE statuses.</p>
</section>
<section class="qa-section" id="q-238-s-02" data-answer-section="2"><h3><span>2.</span> Establish the cause from evidence</h3>
<span class="qa-anchor" id="q-238-a-03"></span><p>Establish supported commands and protocols before forming a request.</p>
<span class="qa-anchor" id="q-238-a-05"></span><p>Validate outer fields/buffer before payload; NSSF is defined for specified EAh uses.</p>
</section>
<section class="qa-section" id="q-238-s-03" data-answer-section="3"><h3><span>3.</span> Outcome and follow-up checks</h3>
<span class="qa-anchor" id="q-238-a-06"></span><p>Valid transport returns protocol results that separately establish security success.</p>
<span class="qa-anchor" id="q-238-a-16"></span><p>Preserve both outer CQE and inner result.</p>
<span class="qa-anchor" id="q-238-a-17"></span><p>First check lengths and buffer capacity before diagnosing credentials.</p>
</section>
</div>
<span class="qa-anchor" id="q-238-a-08"></span><span class="qa-anchor" id="q-238-a-09"></span><span class="qa-anchor" id="q-238-a-10"></span><span class="qa-anchor" id="q-238-a-11"></span><span class="qa-anchor" id="q-238-a-12"></span><span class="qa-anchor" id="q-238-a-13"></span><span class="qa-anchor" id="q-238-a-14"></span><span class="qa-anchor" id="q-238-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-security">Base 2.4 §5.2.28–5.2.29</a> · <a href="#ref-lockdown">Base 2.4 §5.2.16, 8.1.5</a> · <a href="#ref-locklog">Base 2.4 §5.2.13.1.20</a> · <a href="#ref-lockpersist">Base 2.4 §5.2.30.1.25.4–5.2.30.1.25.4.1</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-239" data-question="239" data-answer-kind="error"><h2><a class="qa-qid" href="#q-239">Q239</a> How are security transfer and protocol failures distinguished?</h2>
<p class="qa-prompt">Distinguish failure conditions before deciding whether a particular response is required.</p>
<details class="qa-answer" id="q-239-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-239-a-01">Failed transport differs from a protocol rejecting successfully delivered data.</p><div class="qa-sections">
<section class="qa-section" id="q-239-s-01" data-answer-section="1"><h3><span>1.</span> Distinguish the failure conditions</h3>
<span class="qa-anchor" id="q-239-a-02"></span><p>Analyze command transport before the multi-command protocol exchange.</p>
<span class="qa-anchor" id="q-239-a-04"></span><p>Data Transfer Error concerns data movement; security outcomes may be encoded separately in protocol fields.</p>
<span class="qa-anchor" id="q-239-a-07"></span><p>Unsupported fields, transfer failures, internal errors and authentication rejection have distinct premises.</p>
</section>
<section class="qa-section" id="q-239-s-02" data-answer-section="2"><h3><span>2.</span> Establish the cause from evidence</h3>
<span class="qa-anchor" id="q-239-a-03"></span><p>Preserve SQE, pointers, length, CQE and valid receive payload.</p>
<span class="qa-anchor" id="q-239-a-05"></span><p>Establish valid returned data before decoding; stale buffers after transfer failure are not new results.</p>
</section>
<section class="qa-section" id="q-239-s-03" data-answer-section="3"><h3><span>3.</span> Outcome and follow-up checks</h3>
<span class="qa-anchor" id="q-239-a-06"></span><p>A successful CQE still requires protocol-result interpretation.</p>
<span class="qa-anchor" id="q-239-a-16"></span><p>Correlate both layers and sequence to the intended exchange.</p>
<span class="qa-anchor" id="q-239-a-17"></span><p>First distinguish protocol rejection from DMA failure.</p>
</section>
</div>
<span class="qa-anchor" id="q-239-a-08"></span><span class="qa-anchor" id="q-239-a-09"></span><span class="qa-anchor" id="q-239-a-10"></span><span class="qa-anchor" id="q-239-a-11"></span><span class="qa-anchor" id="q-239-a-12"></span><span class="qa-anchor" id="q-239-a-13"></span><span class="qa-anchor" id="q-239-a-14"></span><span class="qa-anchor" id="q-239-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-security">Base 2.4 §5.2.28–5.2.29</a> · <a href="#ref-lockdown">Base 2.4 §5.2.16, 8.1.5</a> · <a href="#ref-locklog">Base 2.4 §5.2.13.1.20</a> · <a href="#ref-lockpersist">Base 2.4 §5.2.30.1.25.4–5.2.30.1.25.4.1</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-240" data-question="240" data-answer-kind="concept"><h2><a class="qa-qid" href="#q-240">Q240</a> How can security state affect other Admin commands?</h2>
<p class="qa-prompt">Explain the mechanism in your own words and identify a common misconception.</p>
<details class="qa-answer" id="q-240-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-240-a-01">Security policy may restrict operations, but an unspecified Locked state does not prohibit every Admin command.</p><div class="qa-sections">
<section class="qa-section" id="q-240-s-01" data-answer-section="1"><h3><span>1.</span> Mechanism and scope</h3>
<span class="qa-anchor" id="q-240-a-02"></span><p>Protocol, protected objects and explicit NVMe interactions determine scope.</p>
<span class="qa-anchor" id="q-240-a-04"></span><p>Security transport, Lockdown and Namespace Write Protection are distinct mechanisms.</p>
</section>
<section class="qa-section" id="q-240-s-02" data-answer-section="2"><h3><span>2.</span> Understand it through actions and results</h3>
<span class="qa-anchor" id="q-240-a-03"></span><p>Identify the actual protocol/state, Lockdown log and applicable personality settings.</p>
<span class="qa-anchor" id="q-240-a-05"></span><p>Identify command/scope, the denying mechanism and its specified response.</p>
<span class="qa-anchor" id="q-240-a-06"></span><p>Permitted queries may continue, and removing one restriction need not remove others.</p>
</section>
<section class="qa-section" id="q-240-s-03" data-answer-section="3"><h3><span>3.</span> Avoid a misleading conclusion</h3>
<span class="qa-anchor" id="q-240-a-07"></span><p>Generic SC 23h applies to Lockdown, not every security denial.</p>
<span class="qa-anchor" id="q-240-a-16"></span><p>Correlate each mechanism separately with observed behavior.</p>
</section>
</div>
<span class="qa-anchor" id="q-240-a-17"></span><span class="qa-anchor" id="q-240-a-08"></span><span class="qa-anchor" id="q-240-a-09"></span><span class="qa-anchor" id="q-240-a-10"></span><span class="qa-anchor" id="q-240-a-11"></span><span class="qa-anchor" id="q-240-a-12"></span><span class="qa-anchor" id="q-240-a-13"></span><span class="qa-anchor" id="q-240-a-14"></span><span class="qa-anchor" id="q-240-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-security">Base 2.4 §5.2.28–5.2.29</a> · <a href="#ref-lockdown">Base 2.4 §5.2.16, 8.1.5</a> · <a href="#ref-locklog">Base 2.4 §5.2.13.1.20</a> · <a href="#ref-lockpersist">Base 2.4 §5.2.30.1.25.4–5.2.30.1.25.4.1</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-241" data-question="241" data-answer-kind="lifecycle"><h2><a class="qa-qid" href="#q-241">Q241</a> Does security state survive reset or power cycle?</h2>
<p class="qa-prompt">Name the reset or interruption, then assess settings, ongoing operations and data separately.</p>
<details class="qa-answer" id="q-241-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-241-a-01">A testable answer requires a particular protocol and state.</p><div class="qa-sections">
<section class="qa-section" id="q-241-s-01" data-answer-section="1"><h3><span>1.</span> Identify the trigger and affected objects</h3>
<span class="qa-anchor" id="q-241-a-02"></span><p>Keys, persistent policy, sessions and pending receive data have different lifetimes.</p>
<span class="qa-anchor" id="q-241-a-03"></span><p>Record protocol/revision/state and reset source; the three NVMe specs define only their stated transport behavior.</p>
</section>
<section class="qa-section" id="q-241-s-02" data-answer-section="2"><h3><span>2.</span> State changes and recovery</h3>
<span class="qa-anchor" id="q-241-a-04"></span><p>Base permits loss of receive results after communication loss/CLR, not automatic erasure of persistent security settings.</p>
<span class="qa-anchor" id="q-241-a-05"></span><p>Recover communication, query state and reauthenticate if the selected protocol requires it.</p>
<span class="qa-anchor" id="q-241-a-06"></span><p>Correctness follows selected protocol retention, not universal keep/clear behavior.</p>
</section>
<section class="qa-section" id="q-241-s-03" data-answer-section="3"><h3><span>3.</span> Checks across reset or power loss</h3>
<span class="qa-anchor" id="q-241-a-12"></span>
<span class="qa-anchor" id="q-241-a-13"></span>
<span class="qa-anchor" id="q-241-a-14"></span>
<div class="qr-table" tabindex="0" role="region" aria-label="Horizontally scrollable comparison table"><table><thead><tr><th scope="col">Trigger</th><th scope="col">Effect on this operation or state</th></tr></thead><tbody><tr><td>What survives or continues after Controller Reset?</td><td>Pending Security Receive data may not survive CLR. Lock/session/key persistence is protocol-specific; lost transport results do not establish unlock or key erasure.</td></tr><tr><td>What survives or continues after NVM Subsystem Reset?</td><td>Rediscover communication and protocol state after subsystem reset. Base supplies no universal authentication/lock retention rule for every security protocol.</td></tr><tr><td>What survives or continues after a power cycle?</td><td>Recreated queues do not prove an unlocked security state after power cycle. Apply the selected protocol’s persistent/session rules; absent that choice these NVMe sources do not define one answer.</td></tr></tbody></table></div>
</section>
<section class="qa-section" id="q-241-s-04" data-answer-section="4"><h3><span>4.</span> Verify retention and recovery</h3>
<span class="qa-anchor" id="q-241-a-07"></span><p>Without a protocol, do not invent statuses, unlock results or key handling; state the specification boundary.</p>
<span class="qa-anchor" id="q-241-a-16"></span><p>Verify transport, session and persistent state separately.</p>
<span class="qa-anchor" id="q-241-a-17"></span><p>First identify the exact field or protocol object meant by security state.</p>
</section>
</div>
<span class="qa-anchor" id="q-241-a-08"></span><span class="qa-anchor" id="q-241-a-09"></span><span class="qa-anchor" id="q-241-a-10"></span><span class="qa-anchor" id="q-241-a-11"></span><span class="qa-anchor" id="q-241-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-security">Base 2.4 §5.2.28–5.2.29</a> · <a href="#ref-lockdown">Base 2.4 §5.2.16, 8.1.5</a> · <a href="#ref-locklog">Base 2.4 §5.2.13.1.20</a> · <a href="#ref-lockpersist">Base 2.4 §5.2.30.1.25.4–5.2.30.1.25.4.1</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-242" data-question="242" data-answer-kind="process"><h2><a class="qa-qid" href="#q-242">Q242</a> How does Lockdown restrict commands or features?</h2>
<p class="qa-prompt">Order the actions and identify which completion must precede the next action.</p>
<details class="qa-answer" id="q-242-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-242-a-01">Lockdown controls execution at selected interfaces/controllers, not encryption or namespace write protection.</p><div class="qa-sections">
<section class="qa-section" id="q-242-s-01" data-answer-section="1"><h3><span>1.</span> Prepare the operation</h3>
<span class="qa-anchor" id="q-242-a-02"></span><p>CSEL selects subsystem, controller or a primary’s secondaries; IFC selects the receiving interface.</p>
<span class="qa-anchor" id="q-242-a-03"></span><p>Check CFLS/CCFLS and the prohibitable list, which is implementation-defined.</p>
<span class="qa-anchor" id="q-242-a-04"></span><p>SCP/OFI select opcode or FID, PRHBT controls prohibition, and CSS/UIDX select target controller/definition.</p>
</section>
<section class="qa-section" id="q-242-s-02" data-answer-section="2"><h3><span>2.</span> Sequence and completion conditions</h3>
<span class="qa-anchor" id="q-242-a-05"></span><p>Discover, apply, await success, read current prohibition and test the matching interface.</p>
<span class="qa-anchor" id="q-242-a-06"></span><p>Successful scope enforcement is idempotent for repeat prohibit/allow operations.</p>
</section>
<section class="qa-section" id="q-242-s-03" data-answer-section="3"><h3><span>3.</span> Handle unmet conditions</h3>
<span class="qa-anchor" id="q-242-a-07"></span><p>Nonprohibitable targets require the command-specific prohibition-not-supported status; unsupported nonzero CSEL requires Invalid Field.</p>
<span class="qa-anchor" id="q-242-a-16"></span><p>Prohibiting one FID targets Set, not Get or necessarily the entire Set Features opcode.</p>
</section>
</div>
<span class="qa-anchor" id="q-242-a-17"></span><span class="qa-anchor" id="q-242-a-08"></span><span class="qa-anchor" id="q-242-a-09"></span><span class="qa-anchor" id="q-242-a-10"></span><span class="qa-anchor" id="q-242-a-11"></span><span class="qa-anchor" id="q-242-a-12"></span><span class="qa-anchor" id="q-242-a-13"></span><span class="qa-anchor" id="q-242-a-14"></span><span class="qa-anchor" id="q-242-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-security">Base 2.4 §5.2.28–5.2.29</a> · <a href="#ref-lockdown">Base 2.4 §5.2.16, 8.1.5</a> · <a href="#ref-locklog">Base 2.4 §5.2.13.1.20</a> · <a href="#ref-lockpersist">Base 2.4 §5.2.30.1.25.4–5.2.30.1.25.4.1</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-243" data-question="243" data-answer-kind="error"><h2><a class="qa-qid" href="#q-243">Q243</a> What response is required for a prohibited command or feature?</h2>
<p class="qa-prompt">Distinguish failure conditions before deciding whether a particular response is required.</p>
<details class="qa-answer" id="q-243-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-243-a-01">Verify actual enforcement after successful configuration.</p><div class="qa-sections">
<section class="qa-section" id="q-243-s-01" data-answer-section="1"><h3><span>1.</span> Distinguish the failure conditions</h3>
<span class="qa-anchor" id="q-243-a-02"></span><p>Match controller, receiving interface, opcode/FID and applicable UUID.</p>
<span class="qa-anchor" id="q-243-a-04"></span><p>A prohibited command received on the Admin SQ shall abort with SCT 0/SC 23h.</p>
<span class="qa-anchor" id="q-243-a-07"></span><p>Configuration failures differ from target denial; preserve explicit CDP Authentication exceptions.</p>
</section>
<section class="qa-section" id="q-243-s-02" data-answer-section="2"><h3><span>2.</span> Establish the cause from evidence</h3>
<span class="qa-anchor" id="q-243-a-03"></span><p>Read current prohibitions and confirm the successful setting/scope.</p>
<span class="qa-anchor" id="q-243-a-05"></span><p>Apply the restriction, submit an otherwise-valid target command and verify denial/no execution.</p>
</section>
<section class="qa-section" id="q-243-s-03" data-answer-section="3"><h3><span>3.</span> Outcome and follow-up checks</h3>
<span class="qa-anchor" id="q-243-a-06"></span><p>Test success means enforcement, not successful execution of the denied command.</p>
<span class="qa-anchor" id="q-243-a-16"></span><p>With enabled persistence and the required authenticated-unfreeze support, CDP Authentication Send/Receive remains allowed despite prior prohibition.</p>
<span class="qa-anchor" id="q-243-a-17"></span><p>First check target/interface and explicit exceptions.</p>
</section>
</div>
<span class="qa-anchor" id="q-243-a-08"></span><span class="qa-anchor" id="q-243-a-09"></span><span class="qa-anchor" id="q-243-a-10"></span><span class="qa-anchor" id="q-243-a-11"></span><span class="qa-anchor" id="q-243-a-12"></span><span class="qa-anchor" id="q-243-a-13"></span><span class="qa-anchor" id="q-243-a-14"></span><span class="qa-anchor" id="q-243-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-security">Base 2.4 §5.2.28–5.2.29</a> · <a href="#ref-lockdown">Base 2.4 §5.2.16, 8.1.5</a> · <a href="#ref-locklog">Base 2.4 §5.2.13.1.20</a> · <a href="#ref-lockpersist">Base 2.4 §5.2.30.1.25.4–5.2.30.1.25.4.1</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-244" data-question="244" data-answer-kind="fields"><h2><a class="qa-qid" href="#q-244">Q244</a> How are normal and enhanced Lockdown logs interpreted?</h2>
<p class="qa-prompt">Explain the units and encoding, then work through one set of values.</p>
<details class="qa-answer" id="q-244-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-244-a-01">The log distinguishes prohibitable capability from current prohibitions.</p><div class="qa-sections">
<section class="qa-section" id="q-244-s-01" data-answer-section="1"><h3><span>1.</span> Establish the source and scope</h3>
<span class="qa-anchor" id="q-244-a-02"></span><p>Normal lists can describe all controllers; enhanced lists can select one or aggregate entries reported by at least one.</p>
<span class="qa-anchor" id="q-244-a-03"></span><p>Enhanced ELPF1 requires CCFLS; LSI.CNTLID is used only there.</p>
</section>
<section class="qa-section" id="q-244-s-02" data-answer-section="2"><h3><span>2.</span> Fields, units and worked interpretation</h3>
<span class="qa-anchor" id="q-244-a-04"></span><p>CNTTS chooses capability/Admin/OOB prohibition; SCP selects identifiers. Normal LNGTH counts bytes; enhanced sizes/counts govern descriptors.</p>
<span class="qa-anchor" id="q-244-a-05"></span><p>Match returned selectors; in the enhanced aggregate, ACNTL1 means all and 0 some but not all.</p>
<span class="qa-anchor" id="q-244-a-06"></span><p>If only controller 1 prohibits FID 12h, an aggregate entry with ACNTL0 means partial coverage, not no prohibition.</p>
</section>
<section class="qa-section" id="q-244-s-03" data-answer-section="3"><h3><span>3.</span> Conditions that change the interpretation</h3>
<span class="qa-anchor" id="q-244-a-07"></span><p>Unsupported enhanced format requires Invalid Field; enhanced log length is not universally 512 bytes.</p>
<span class="qa-anchor" id="q-244-a-16"></span><p>Compare per-controller results and behavior to distinguish union from intersection.</p>
</section>
</div>
<span class="qa-anchor" id="q-244-a-17"></span><span class="qa-anchor" id="q-244-a-08"></span><span class="qa-anchor" id="q-244-a-09"></span><span class="qa-anchor" id="q-244-a-10"></span><span class="qa-anchor" id="q-244-a-11"></span><span class="qa-anchor" id="q-244-a-12"></span><span class="qa-anchor" id="q-244-a-13"></span><span class="qa-anchor" id="q-244-a-14"></span><span class="qa-anchor" id="q-244-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-security">Base 2.4 §5.2.28–5.2.29</a> · <a href="#ref-lockdown">Base 2.4 §5.2.16, 8.1.5</a> · <a href="#ref-locklog">Base 2.4 §5.2.13.1.20</a> · <a href="#ref-lockpersist">Base 2.4 §5.2.30.1.25.4–5.2.30.1.25.4.1</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-245" data-question="245" data-answer-kind="lifecycle"><h2><a class="qa-qid" href="#q-245">Q245</a> Does Lockdown survive resets and power cycles?</h2>
<p class="qa-prompt">Name the reset or interruption, then assess settings, ongoing operations and data separately.</p>
<details class="qa-answer" id="q-245-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-245-a-01">Retention depends on CSEL and persistence settings, not one Lockdown-enabled flag.</p><div class="qa-sections">
<section class="qa-section" id="q-245-s-01" data-answer-section="1"><h3><span>1.</span> Identify the trigger and affected objects</h3>
<span class="qa-anchor" id="q-245-a-02"></span><p>Separate subsystem prohibitions from selected-controller/group prohibitions.</p>
<span class="qa-anchor" id="q-245-a-03"></span><p>Preserve original selectors and read actual personality LDPS.</p>
</section>
<section class="qa-section" id="q-245-s-02" data-answer-section="2"><h3><span>2.</span> State changes and recovery</h3>
<span class="qa-anchor" id="q-245-a-04"></span><p>LDPE is requested input and LDPS returned state; submission does not establish success.</p>
<span class="qa-anchor" id="q-245-a-05"></span><p>Snapshot, perform the specified reset/power cycle and repeat the same query/behavior checks.</p>
<span class="qa-anchor" id="q-245-a-06"></span><p>Ordinary reset retains restrictions; power-cycle behavior depends on scope and persistence, with no CSEL1/2 persistence extension.</p>
</section>
<section class="qa-section" id="q-245-s-03" data-answer-section="3"><h3><span>3.</span> Checks across reset or power loss</h3>
<span class="qa-anchor" id="q-245-a-12"></span>
<span class="qa-anchor" id="q-245-a-13"></span>
<span class="qa-anchor" id="q-245-a-14"></span>
<div class="qr-table" tabindex="0" role="region" aria-label="Horizontally scrollable comparison table"><table><thead><tr><th scope="col">Trigger</th><th scope="col">Effect on this operation or state</th></tr></thead><tbody><tr><td>What survives or continues after Controller Reset?</td><td>Ordinary CLR does not remove a successful prohibition; removal requires an allowed subsequent Lockdown or its specified power-cycle condition.</td></tr><tr><td>What survives or continues after NVM Subsystem Reset?</td><td>Subsystem reset is not power cycle and does not automatically remove prohibitions; preserve scope-specific state and explicit personality exceptions.</td></tr><tr><td>What survives or continues after a power cycle?</td><td>CSEL0 persists across power cycles only with LDPE1; otherwise power cycle removes it. CSEL1/2 end at power cycle regardless of LDPE.</td></tr></tbody></table></div>
</section>
<section class="qa-section" id="q-245-s-04" data-answer-section="4"><h3><span>4.</span> Verify retention and recovery</h3>
<span class="qa-anchor" id="q-245-a-07"></span><p>Neither retention after subsystem reset nor loss of controller-scoped restrictions after power cycle is automatically a failure.</p>
<span class="qa-anchor" id="q-245-a-16"></span><p>Scope, actual personality state and reset type jointly determine the expectation.</p>
<span class="qa-anchor" id="q-245-a-17"></span><p>First distinguish the three actual reset/power actions.</p>
</section>
</div>
<span class="qa-anchor" id="q-245-a-08"></span><span class="qa-anchor" id="q-245-a-09"></span><span class="qa-anchor" id="q-245-a-10"></span><span class="qa-anchor" id="q-245-a-11"></span><span class="qa-anchor" id="q-245-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-security">Base 2.4 §5.2.28–5.2.29</a> · <a href="#ref-lockdown">Base 2.4 §5.2.16, 8.1.5</a> · <a href="#ref-locklog">Base 2.4 §5.2.13.1.20</a> · <a href="#ref-lockpersist">Base 2.4 §5.2.30.1.25.4–5.2.30.1.25.4.1</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>

<section id="source-index"><h2>Source locations and existing figure guides</h2><p>Base printed page = PDF page−26; the other two use identical numbers. Locations follow the supplied PDF body and retain figure numbers. Shared pages contribute only the relevant definitions, excluding Fabrics and PCIe link/packet content.</p><ul class="qa-references">
<li id="ref-reset"><strong>Base 2.4 · §3.7.1–3.7.4</strong><br>Printed pages 120–124 · PDF 146–150</li>
<li id="ref-status"><strong>Base 2.4 · §4.2.3</strong><br>Printed pages 145–155 · PDF 171–181 · Figure 101–105</li>
<li id="ref-aer"><strong>Base 2.4 · §5.2.2</strong><br>Printed pages 183–190 · PDF 209–216 · Figure 150–156</li>
<li id="ref-error"><strong>Base 2.4 · §5.2.13.1.2</strong><br>Printed pages 218–220 · PDF 244–246 · Figure 212</li>
<li id="ref-pel"><strong>Base 2.4 · §5.2.13.1.14 (header, reset, hardware, Set Feature events)</strong><br>Printed pages 244–256, 258, 262–264 · PDF 270–282, 284, 288–290 · Figure 232–244, 246, 252–253</li>
<li id="ref-locklog"><strong>Base 2.4 · §5.2.13.1.20</strong><br>Printed pages 279–283 · PDF 305–309 · Figure 274–278</li>
<li id="ref-idctrl"><strong>Base 2.4 · §5.2.14.2.1</strong><br>Printed pages 340–387 · PDF 366–413 · Figure 338–341</li>
<li id="ref-lockdown"><strong>Base 2.4 · §5.2.16, 8.1.5</strong><br>Printed pages 405–408, 597–599 · PDF 431–434, 623–625 · Figure 365–367</li>
<li id="ref-security"><strong>Base 2.4 · §5.2.28–5.2.29</strong><br>Printed pages 454–456 · PDF 480–482 · Figure 456–462</li>
<li id="ref-lockpersist"><strong>Base 2.4 · §5.2.30.1.25.4–5.2.30.1.25.4.1</strong><br>Printed pages 493–494 · PDF 519–520 · Figure 518–519</li>
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
<nav class="qr-top" aria-label="Bank and editions"><a href="#content">Skip to content</a><a href="/nvme/question-bank/en/">Question index</a><a href="/nvme/question-bank/security/zh-tw/">繁體中文</a><a href="/DOCS/nvme-question-bank/security.html">Chinese tutorial HTML</a></nav>
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
