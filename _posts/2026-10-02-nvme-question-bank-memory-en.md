---
layout: post
title: "NVMe Self-Study Bank: HMB, CMB and PMR"
date: 2026-10-02 00:00:00 +0800
categories: [nvme]
permalink: /nvme/question-bank/memory/en/
lang: en
nvme_quickref: true
nvme_qa: true
---

<div class="nvme-quickref nvme-qa">
<nav class="qr-top" aria-label="Bank and editions"><a href="#content">Skip to content</a><a href="/nvme/question-bank/en/">Question index</a><a href="/nvme/question-bank/memory/zh-tw/">繁體中文</a><a href="/DOCS/nvme-question-bank/memory.html">Chinese tutorial HTML</a></nav>
<main id="content"><p class="qr-eyebrow">BASE 2.4 / NVM 1.3 / PCIe 1.4 · Q1–320</p>
<header><p class="qa-range">Q223–Q236</p><h1>HMB, CMB and PMR</h1><p class="qr-intro">Compare location, ownership, lifetime and persistence rather than treating all memory facilities alike.</p><p>Practice first, then reveal 17 answer items per question. All numerical examples are hypothetical. Status is written SCT/SC; h indicates hexadecimal.</p></header>
<aside class="qa-glossary"><h2>Terms used in this volume</h2><dl><dt>Controller / namespace</dt><dd>A controller receives commands and manages access. A namespace is a logical storage space that commands can address. An NVM subsystem contains controllers and nonvolatile storage resources.</dd><dt>SQ / CQ / SQE / CQE</dt><dd>Submission and Completion Queues carry command entries (SQEs) and completion entries (CQEs). QID identifies a queue, CID distinguishes outstanding commands in one SQ, and NSID identifies a namespace.</dd><dt>Register / Identify / Feature / Log</dt><dd>A register exposes control or state. Identify queries capabilities and attributes; features query or configure operation; log pages report specific state or records. FID, LID, CNS and CSI select features, logs, Identify structures and command sets.</dd><dt>index / offset / zero-based</dt><dd>An index selects an entry, usually starting at 0; an offset measures distance from an origin in specified units. A zero-based count encodes count−1, but not every zero-valued field is a count. A Dword is 4 bytes; a byte is 8 bits.</dd><dt>Scope / reset / retention</dt><dd>Scope names the affected objects; retention means preserving state. Controller Reset (clearing CC.EN) is one form of Controller Level Reset, or CLR. Different CLR triggers can retain different registers.</dd></dl></aside>
<section id="overview" class="qa-overview"><h2>Location, ownership and persistence</h2><p class="qa-takeaway">Retained addressing is not retained content; CQE success alone does not establish PMR persistence.</p>
<div class="qr-table" tabindex="0" role="region" aria-label="Horizontally scrollable comparison table"><table><thead><tr><th scope="col">Facility</th><th scope="col">Location/use</th><th scope="col">Lifetime/evidence</th></tr></thead><tbody><tr><td>HMB</td><td>Host-provided controller buffer</td><td>Reclaim after successful disable</td></tr><tr><td>CMB</td><td>Controller memory with advertised uses</td><td>Reinitialize under reset/CMSE rules</td></tr><tr><td>PMR</td><td>Function-provided persistent region</td><td>Check readiness, health and write barriers</td></tr></tbody></table></div>
<p><strong>Worked interpretation: </strong>HMB cannot be reused before disable; retained CMB addressing can still require content reinitialization; PMR has distinct persistence/health rules.</p>
<p class="qa-citations">Sources: <a href="#ref-hmb">Base 2.4 §5.2.30.2.3, 8.2.4</a> · <a href="#ref-cmb">Base 2.4 §8.2.1 (memory placement and lifetime)</a> · <a href="#ref-cmbreg">Base 2.4 §3.1.4 (CMBLOC, CMBSZ, CMBMSC, CMBSTS)</a> · <a href="#ref-pmr">Base 2.4 §8.2.5 (memory behavior; exclude PCIe packet detail)</a> · <a href="#ref-pmrreg">Base 2.4 §3.1.4 (PMR properties)</a></p>
</section>
<div class="qa-controls" hidden><label>Search this page <input type="search" id="qa-search" placeholder="Question number, field or keyword"></label><button type="button" data-expand="true">Expand all answers</button><button type="button" data-expand="false">Collapse all answers</button><output id="qa-count" aria-live="polite"></output></div>
<section id="question-index"><h2>Questions in this volume</h2><ol class="qa-index">
<li><a href="#q-223">Q223 · What problems do HMB, CMB and PMR solve?</a></li>
<li><a href="#q-224">Q224 · How are HMB size and descriptor lists configured?</a></li>
<li><a href="#q-225">Q225 · How are malformed HMB allocations handled?</a></li>
<li><a href="#q-226">Q226 · How is HMB enabled, disabled and returned after reset?</a></li>
<li><a href="#q-227">Q227 · What happens if the host prematurely reclaims HMB?</a></li>
<li><a href="#q-228">Q228 · How are CMB location, size and uses discovered?</a></li>
<li><a href="#q-229">Q229 · Which queues, buffers and lists may reside in CMB?</a></li>
<li><a href="#q-230">Q230 · How are out-of-range or unsupported CMB uses handled?</a></li>
<li><a href="#q-231">Q231 · Do CMB configuration and contents survive reset?</a></li>
<li><a href="#q-232">Q232 · How is PMR discovered, enabled and made ready?</a></li>
<li><a href="#q-233">Q233 · What happens for not-ready or unhealthy PMR accesses?</a></li>
<li><a href="#q-234">Q234 · How is PMR safely disabled?</a></li>
<li><a href="#q-235">Q235 · How do resets and power cycles affect PMR state and data?</a></li>
<li><a href="#q-236">Q236 · How do host memory, HMB, CMB and PMR lifetimes compare?</a></li>
</ol></section>
<article class="qa-question" id="q-223" data-question="223"><h2><a class="qa-qid" href="#q-223">Q223</a> What problems do HMB, CMB and PMR solve?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-223-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-223-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Their memory location, user and persistence guarantees differ; identify those before placement.</p>
</li>
<li id="q-223-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>HMB is host memory dedicated to the controller; CMB is controller memory for supported uses; PMR is directly accessible persistent memory.</p>
</li>
<li id="q-223-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Discover HMB through HMPRE, CMB through CAP/CMBSZ and PMR through CAP/PMRCAP.</p>
</li>
<li id="q-223-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>HMB uses FID 0Dh descriptors; CMB uses address/control registers; PMR uses enable/readiness/health registers.</p>
</li>
<li id="q-223-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Match the need: firmware host RAM, supported CMB SQ placement or persistent PMR data with barriers and health checks.</p>
</li>
<li id="q-223-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Success means supported use within its constraints, not universal placement freedom.</p>
</li>
<li id="q-223-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Queue/list use in PMR is outside scope and may return Invalid Field; writable PMR is not interchangeable with CMB.</p>
</li>
<li id="q-223-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>HMB Set Features has a CQE; direct CMB/PMR register accesses do not. <a class="qa-rule-link" href="#common-memory_compare-8">Full rule in this volume</a></p>
</li>
<li id="q-223-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>No generic success AER accompanies memory configuration; qualifying PMR health warnings use their specific SMART/event rules.</p>
</li>
<li id="q-223-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Verify HMB lifetime, CMB placement/use and PMR readiness/error/health; these observations are not per-access error-log mandates.</p>
</li>
<li id="q-223-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>Ordinary memory access is not a PEL event; supported HMB feature changes and PMR health/hardware events follow separate conditions.</p>
</li>
<li id="q-223-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>CLR invalidates HMB allocation; CMB mappings may persist while contents become undefined; persistent PMR data remains. <a class="qa-rule-link" href="#common-memory_compare-12">Full rule in this volume</a></p>
</li>
<li id="q-223-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>After subsystem reset, separately restore HMB allocation, initialize CMB and check PMR health. <a class="qa-rule-link" href="#common-memory_compare-13">Full rule in this volume</a></p>
</li>
<li id="q-223-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>HMB/CMB lack PMR persistence guarantees; PMR still requires supported barriers and health checks. <a class="qa-rule-link" href="#common-memory_compare-14">Full rule in this volume</a></p>
</li>
<li id="q-223-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Identify physical location, ownership and address space; identical numeric addresses do not prove identical buffers across mappings. <a class="qa-rule-link" href="#common-memory_compare-15">Full rule in this volume</a></p>
</li>
<li id="q-223-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Compare support, configuration, access method and restored contents, not only readable bytes.</p>
</li>
<li id="q-223-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First check memory type and the mistaken assumption that device-local means persistent.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-hmb">Base 2.4 §5.2.30.2.3, 8.2.4</a> · <a href="#ref-cmb">Base 2.4 §8.2.1 (memory placement and lifetime)</a> · <a href="#ref-cmbreg">Base 2.4 §3.1.4 (CMBLOC, CMBSZ, CMBMSC, CMBSTS)</a> · <a href="#ref-pmr">Base 2.4 §8.2.5 (memory behavior; exclude PCIe packet detail)</a> · <a href="#ref-pmrreg">Base 2.4 §3.1.4 (PMR properties)</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-224" data-question="224"><h2><a class="qa-qid" href="#q-224">Q224</a> How are HMB size and descriptor lists configured?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-224-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-224-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Multiple contiguous ranges form HMB; the descriptor list itself must be physically contiguous.</p>
</li>
<li id="q-224-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>The allocation is exclusive to one controller and unavailable for ordinary host writes while enabled.</p>
</li>
<li id="q-224-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Read preferred/minimum size, minimum descriptor size and maximum descriptors; size capability fields use 4 KiB units.</p>
</li>
<li id="q-224-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>HSIZE/BSIZE use CC.MPS pages; HMDLEC is a literal count, list address is 16-byte aligned and BADD page-aligned.</p>
</li>
<li id="q-224-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Pin memory, construct descriptors, reconcile sizes and enable with EHM=1, awaiting success.</p>
</li>
<li id="q-224-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Get verifies allocation; with hypothetical 8 KiB pages, HSIZE256 means 2 MiB.</p>
</li>
<li id="q-224-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Zero HMDLEC requires Invalid Field; exceeding usable descriptor limits may reduce utilization rather than force rejection.</p>
</li>
<li id="q-224-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-224-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>HMB enable/disable has no separate success AER; independently defined hardware faults follow their own event rules. <a class="qa-rule-link" href="#common-hmb_op-9">Full rule in this volume</a></p>
</li>
<li id="q-224-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Get reports HMB state and allocation, not a backup of buffer contents. <a class="qa-rule-link" href="#common-hmb_op-10">Full rule in this volume</a></p>
</li>
<li id="q-224-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>Supported, permitted Set Feature logging follows successful-change rules; ordinary HMB accesses are not individual persistent events. <a class="qa-rule-link" href="#common-hmb_op-11">Full rule in this volume</a></p>
</li>
<li id="q-224-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>HMB allocation does not persist across CLR. <a class="qa-rule-link" href="#common-hmb_op-12">Full rule in this volume</a></p>
</li>
<li id="q-224-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Subsystem reset invalidates affected HMB allocations. <a class="qa-rule-link" href="#common-hmb_op-13">Full rule in this volume</a></p>
</li>
<li id="q-224-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>HMB is not persistent storage. <a class="qa-rule-link" href="#common-hmb_op-14">Full rule in this volume</a></p>
</li>
<li id="q-224-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>HMB is host memory exclusively allocated to this controller; the host shall not modify its list/buffers while enabled or repurpose them. <a class="qa-rule-link" href="#common-hmb_op-15">Full rule in this volume</a></p>
</li>
<li id="q-224-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Convert capability units before encoding HSIZE and verify readback.</p>
</li>
<li id="q-224-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First check page units and literal descriptor count.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-hmb">Base 2.4 §5.2.30.2.3, 8.2.4</a> · <a href="#ref-cmb">Base 2.4 §8.2.1 (memory placement and lifetime)</a> · <a href="#ref-cmbreg">Base 2.4 §3.1.4 (CMBLOC, CMBSZ, CMBMSC, CMBSTS)</a> · <a href="#ref-pmr">Base 2.4 §8.2.5 (memory behavior; exclude PCIe packet detail)</a> · <a href="#ref-pmrreg">Base 2.4 §3.1.4 (PMR properties)</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-225" data-question="225"><h2><a class="qa-qid" href="#q-225">Q225</a> How are malformed HMB allocations handled?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-225-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-225-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Different fields have different rules; isolate one malformed condition at a time.</p>
</li>
<li id="q-225-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Check list structure, ranges and current enable state.</p>
</li>
<li id="q-225-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Check limits, HMBR, current EHM and submitted fields.</p>
</li>
<li id="q-225-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>Zero entry count is Invalid Field; zero-size descriptors are ignored. The list address low four bits are treated as zero without a required check.</p>
</li>
<li id="q-225-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Separate specified format errors from inaccessible-memory transfer failures.</p>
</li>
<li id="q-225-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Valid allocation succeeds; out-of-limit allocation may be only partly used.</p>
</li>
<li id="q-225-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Re-enabling active HMB requires Command Sequence Error; unsupported HMNARE requires Invalid Field. Do not demand one status for every alignment defect.</p>
</li>
<li id="q-225-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-225-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>HMB enable/disable has no separate success AER; independently defined hardware faults follow their own event rules. <a class="qa-rule-link" href="#common-hmb_op-9">Full rule in this volume</a></p>
</li>
<li id="q-225-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Get reports HMB state and allocation, not a backup of buffer contents. <a class="qa-rule-link" href="#common-hmb_op-10">Full rule in this volume</a></p>
</li>
<li id="q-225-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>Supported, permitted Set Feature logging follows successful-change rules; ordinary HMB accesses are not individual persistent events. <a class="qa-rule-link" href="#common-hmb_op-11">Full rule in this volume</a></p>
</li>
<li id="q-225-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>HMB allocation does not persist across CLR. <a class="qa-rule-link" href="#common-hmb_op-12">Full rule in this volume</a></p>
</li>
<li id="q-225-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Subsystem reset invalidates affected HMB allocations. <a class="qa-rule-link" href="#common-hmb_op-13">Full rule in this volume</a></p>
</li>
<li id="q-225-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>HMB is not persistent storage. <a class="qa-rule-link" href="#common-hmb_op-14">Full rule in this volume</a></p>
</li>
<li id="q-225-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>HMB is host memory exclusively allocated to this controller; the host shall not modify its list/buffers while enabled or repurpose them. <a class="qa-rule-link" href="#common-hmb_op-15">Full rule in this volume</a></p>
</li>
<li id="q-225-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Match each condition to its rule, preserving ignore versus reject semantics.</p>
</li>
<li id="q-225-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First check whether multiple faults prevent a unique expected status.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-hmb">Base 2.4 §5.2.30.2.3, 8.2.4</a> · <a href="#ref-cmb">Base 2.4 §8.2.1 (memory placement and lifetime)</a> · <a href="#ref-cmbreg">Base 2.4 §3.1.4 (CMBLOC, CMBSZ, CMBMSC, CMBSTS)</a> · <a href="#ref-pmr">Base 2.4 §8.2.5 (memory behavior; exclude PCIe packet detail)</a> · <a href="#ref-pmrreg">Base 2.4 §3.1.4 (PMR properties)</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-226" data-question="226"><h2><a class="qa-qid" href="#q-226">Q226</a> How is HMB enabled, disabled and returned after reset?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-226-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-226-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Explicit ownership transitions establish when memory may be reclaimed.</p>
</li>
<li id="q-226-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>EHM controls use; MR describes whether returned contents are unchanged.</p>
</li>
<li id="q-226-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Read EHM/allocation rather than assuming pre-reset enablement persists.</p>
</li>
<li id="q-226-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>EHM0 ignores CDW12–15; MR1 requires identical size, list address/content and buffer contents.</p>
</li>
<li id="q-226-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Enable, then disable and await success before host modification; reprovide retained or new allocation after reset.</p>
</li>
<li id="q-226-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>After successful disable no HMB access is allowed until re-enabled; disabling an already disabled HMB succeeds without action.</p>
</li>
<li id="q-226-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Re-enable while enabled is a sequence error; claiming MR1 after modification violates the return premise.</p>
</li>
<li id="q-226-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-226-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>HMB enable/disable has no separate success AER; independently defined hardware faults follow their own event rules. <a class="qa-rule-link" href="#common-hmb_op-9">Full rule in this volume</a></p>
</li>
<li id="q-226-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Get reports HMB state and allocation, not a backup of buffer contents. <a class="qa-rule-link" href="#common-hmb_op-10">Full rule in this volume</a></p>
</li>
<li id="q-226-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>Supported, permitted Set Feature logging follows successful-change rules; ordinary HMB accesses are not individual persistent events. <a class="qa-rule-link" href="#common-hmb_op-11">Full rule in this volume</a></p>
</li>
<li id="q-226-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>HMB allocation does not persist across CLR. <a class="qa-rule-link" href="#common-hmb_op-12">Full rule in this volume</a></p>
</li>
<li id="q-226-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Subsystem reset invalidates affected HMB allocations. <a class="qa-rule-link" href="#common-hmb_op-13">Full rule in this volume</a></p>
</li>
<li id="q-226-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>HMB is not persistent storage. <a class="qa-rule-link" href="#common-hmb_op-14">Full rule in this volume</a></p>
</li>
<li id="q-226-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>HMB is host memory exclusively allocated to this controller; the host shall not modify its list/buffers while enabled or repurpose them. <a class="qa-rule-link" href="#common-hmb_op-15">Full rule in this volume</a></p>
</li>
<li id="q-226-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Use successful disable completion, not submission, as the ownership handoff.</p>
</li>
<li id="q-226-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First compare reclamation timing with disable completion.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-hmb">Base 2.4 §5.2.30.2.3, 8.2.4</a> · <a href="#ref-cmb">Base 2.4 §8.2.1 (memory placement and lifetime)</a> · <a href="#ref-cmbreg">Base 2.4 §3.1.4 (CMBLOC, CMBSZ, CMBMSC, CMBSTS)</a> · <a href="#ref-pmr">Base 2.4 §8.2.5 (memory behavior; exclude PCIe packet detail)</a> · <a href="#ref-pmrreg">Base 2.4 §3.1.4 (PMR properties)</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-227" data-question="227"><h2><a class="qa-qid" href="#q-227">Q227</a> What happens if the host prematurely reclaims HMB?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-227-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-227-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>It violates exclusive ownership and can expose or corrupt memory reassigned to another use.</p>
</li>
<li id="q-227-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Damage may reach unrelated host data in reassigned physical pages.</p>
</li>
<li id="q-227-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Check EHM, disable completion and allocation/mapping lifetime.</p>
</li>
<li id="q-227-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>Both descriptors and described ranges must remain intact; retaining only the list is insufficient.</p>
</li>
<li id="q-227-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Disable and await success before unmapping; failure recovery must end old accesses before reclamation.</p>
</li>
<li id="q-227-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>After a valid handoff the old allocation is no longer accessed.</p>
</li>
<li id="q-227-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Host misuse has no guaranteed detection or fixed status and may corrupt data; error logging is not protection.</p>
</li>
<li id="q-227-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-227-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>HMB enable/disable has no separate success AER; independently defined hardware faults follow their own event rules. <a class="qa-rule-link" href="#common-hmb_op-9">Full rule in this volume</a></p>
</li>
<li id="q-227-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Get reports HMB state and allocation, not a backup of buffer contents. <a class="qa-rule-link" href="#common-hmb_op-10">Full rule in this volume</a></p>
</li>
<li id="q-227-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>Supported, permitted Set Feature logging follows successful-change rules; ordinary HMB accesses are not individual persistent events. <a class="qa-rule-link" href="#common-hmb_op-11">Full rule in this volume</a></p>
</li>
<li id="q-227-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>HMB allocation does not persist across CLR. <a class="qa-rule-link" href="#common-hmb_op-12">Full rule in this volume</a></p>
</li>
<li id="q-227-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Subsystem reset invalidates affected HMB allocations. <a class="qa-rule-link" href="#common-hmb_op-13">Full rule in this volume</a></p>
</li>
<li id="q-227-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>HMB is not persistent storage. <a class="qa-rule-link" href="#common-hmb_op-14">Full rule in this volume</a></p>
</li>
<li id="q-227-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>HMB is host memory exclusively allocated to this controller; the host shall not modify its list/buffers while enabled or repurpose them. <a class="qa-rule-link" href="#common-hmb_op-15">Full rule in this volume</a></p>
</li>
<li id="q-227-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Distinguish premature host reclamation from controller accesses after successful disable.</p>
</li>
<li id="q-227-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First align ownership end and memory reuse timing.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-hmb">Base 2.4 §5.2.30.2.3, 8.2.4</a> · <a href="#ref-cmb">Base 2.4 §8.2.1 (memory placement and lifetime)</a> · <a href="#ref-cmbreg">Base 2.4 §3.1.4 (CMBLOC, CMBSZ, CMBMSC, CMBSTS)</a> · <a href="#ref-pmr">Base 2.4 §8.2.5 (memory behavior; exclude PCIe packet detail)</a> · <a href="#ref-pmrreg">Base 2.4 §3.1.4 (PMR properties)</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-228" data-question="228"><h2><a class="qa-qid" href="#q-228">Q228</a> How are CMB location, size and uses discovered?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-228-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-228-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Discover both host access and controller interpretation of command addresses.</p>
</li>
<li id="q-228-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Its PCIe and controller address ranges may have different bases but matching offsets.</p>
</li>
<li id="q-228-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Check CAP.CMBS, enable CRE and read location/size; zero values with CRE0 do not prove absence.</p>
</li>
<li id="q-228-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>BIR selects BAR, OFST locates the region and SZ×SZU determines size within BAR limits; support bits distinguish uses.</p>
</li>
<li id="q-228-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Configure a nonconflicting CBA, enable CMSE, check CBAI and initialize contents.</p>
</li>
<li id="q-228-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Both address views reach the same contents at matching offsets.</p>
</li>
<li id="q-228-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Invalid CBA sets CBAI and prevents memory-space enablement; it is register state, not an Admin CQE.</p>
</li>
<li id="q-228-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>CMB register/memory accesses have no CQE. <a class="qa-rule-link" href="#common-cmb_op-8">Full rule in this volume</a></p>
</li>
<li id="q-228-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Register access has no success event; separate hardware errors use their event conditions. <a class="qa-rule-link" href="#common-register-9">Full rule in this volume</a></p>
</li>
<li id="q-228-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Register accesses are not logged individually; preserve registers and timing before obtaining available diagnostics. <a class="qa-rule-link" href="#common-register-10">Full rule in this volume</a></p>
</li>
<li id="q-228-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>Ordinary register access is not a PEL event; completed resets and supported hardware errors are assessed separately. <a class="qa-rule-link" href="#common-register-11">Full rule in this volume</a></p>
</li>
<li id="q-228-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>CC.EN reset and FLR retain CMBMSC but make CMB contents undefined. <a class="qa-rule-link" href="#common-cmb_op-12">Full rule in this volume</a></p>
</li>
<li id="q-228-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Rediscover mappings and rebuild queues after subsystem reset; do not extend specific CC.EN/FLR retention to every reset source. <a class="qa-rule-link" href="#common-cmb_op-13">Full rule in this volume</a></p>
</li>
<li id="q-228-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>CMB has no PMR-style power-cycle persistence guarantee; reconfigure and initialize it. <a class="qa-rule-link" href="#common-cmb_op-14">Full rule in this volume</a></p>
</li>
<li id="q-228-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Host and controller CMB address ranges may differ; map equal offsets correctly and avoid DMA/PMR conflicts. <a class="qa-rule-link" href="#common-cmb_op-15">Full rule in this volume</a></p>
</li>
<li id="q-228-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Cross-check address bounds, units and use flags, not just capability presence.</p>
</li>
<li id="q-228-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First check confusion between BAR and configured controller addresses.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-hmb">Base 2.4 §5.2.30.2.3, 8.2.4</a> · <a href="#ref-cmb">Base 2.4 §8.2.1 (memory placement and lifetime)</a> · <a href="#ref-cmbreg">Base 2.4 §3.1.4 (CMBLOC, CMBSZ, CMBMSC, CMBSTS)</a> · <a href="#ref-pmr">Base 2.4 §8.2.5 (memory behavior; exclude PCIe packet detail)</a> · <a href="#ref-pmrreg">Base 2.4 §3.1.4 (PMR properties)</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-229" data-question="229"><h2><a class="qa-qid" href="#q-229">Q229</a> Which queues, buffers and lists may reside in CMB?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-229-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-229-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Independent capability bits govern placement; SQ support does not imply CQ/data support.</p>
</li>
<li id="q-229-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Restrictions apply to an entire queue, a command’s list or its data/metadata set.</p>
</li>
<li id="q-229-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Inspect use flags and mixed-memory/discontiguous-list capabilities.</p>
</li>
<li id="q-229-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>CQMMS0 prohibits mixed queue placement; CQPDS0 requires contiguous queues. LISTS and related bits govern pointer-list placement and dependencies.</p>
</li>
<li id="q-229-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Select the object capability, then validate its combined placement constraints before allocating.</p>
</li>
<li id="q-229-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>With hypothetical SQS1/CQS0, an SQ may use CMB while its CQ remains in host memory.</p>
</li>
<li id="q-229-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>General misuse requires Invalid Use of CMB; placing lists with LISTS0 is explicitly undefined, not a fixed-status case.</p>
</li>
<li id="q-229-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>CMB register/memory accesses have no CQE. <a class="qa-rule-link" href="#common-cmb_op-8">Full rule in this volume</a></p>
</li>
<li id="q-229-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Register access has no success event; separate hardware errors use their event conditions. <a class="qa-rule-link" href="#common-register-9">Full rule in this volume</a></p>
</li>
<li id="q-229-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Register accesses are not logged individually; preserve registers and timing before obtaining available diagnostics. <a class="qa-rule-link" href="#common-register-10">Full rule in this volume</a></p>
</li>
<li id="q-229-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>Ordinary register access is not a PEL event; completed resets and supported hardware errors are assessed separately. <a class="qa-rule-link" href="#common-register-11">Full rule in this volume</a></p>
</li>
<li id="q-229-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>CC.EN reset and FLR retain CMBMSC but make CMB contents undefined. <a class="qa-rule-link" href="#common-cmb_op-12">Full rule in this volume</a></p>
</li>
<li id="q-229-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Rediscover mappings and rebuild queues after subsystem reset; do not extend specific CC.EN/FLR retention to every reset source. <a class="qa-rule-link" href="#common-cmb_op-13">Full rule in this volume</a></p>
</li>
<li id="q-229-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>CMB has no PMR-style power-cycle persistence guarantee; reconfigure and initialize it. <a class="qa-rule-link" href="#common-cmb_op-14">Full rule in this volume</a></p>
</li>
<li id="q-229-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Host and controller CMB address ranges may differ; map equal offsets correctly and avoid DMA/PMR conflicts. <a class="qa-rule-link" href="#common-cmb_op-15">Full rule in this volume</a></p>
</li>
<li id="q-229-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Interpret RDS/WDS by command transfer direction.</p>
</li>
<li id="q-229-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First check the specific use flag rather than mere CMB presence.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-hmb">Base 2.4 §5.2.30.2.3, 8.2.4</a> · <a href="#ref-cmb">Base 2.4 §8.2.1 (memory placement and lifetime)</a> · <a href="#ref-cmbreg">Base 2.4 §3.1.4 (CMBLOC, CMBSZ, CMBMSC, CMBSTS)</a> · <a href="#ref-pmr">Base 2.4 §8.2.5 (memory behavior; exclude PCIe packet detail)</a> · <a href="#ref-pmrreg">Base 2.4 §3.1.4 (PMR properties)</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-230" data-question="230"><h2><a class="qa-qid" href="#q-230">Q230</a> How are out-of-range or unsupported CMB uses handled?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-230-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-230-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Distinguish invalid mapping, misuse within a mapped CMB and addresses interpreted elsewhere.</p>
</li>
<li id="q-230-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>CBA/size define the controller range; disabled CMSE routes addresses elsewhere.</p>
</li>
<li id="q-230-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Preserve mapping/status/capabilities and the full command range.</p>
</li>
<li id="q-230-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>CBA must not overflow the 64-bit address space or overlap enabled PMR space.</p>
</li>
<li id="q-230-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Calculate both range endpoints, resolve address spaces and check use/mixing rules.</p>
</li>
<li id="q-230-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Valid ranges and uses follow ordinary command processing.</p>
</li>
<li id="q-230-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Mapping failure uses CBAI; misuse uses its specified status. Out-of-range addresses may resolve elsewhere and have no universal CMB-overrun status.</p>
</li>
<li id="q-230-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>CMB register/memory accesses have no CQE. <a class="qa-rule-link" href="#common-cmb_op-8">Full rule in this volume</a></p>
</li>
<li id="q-230-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Register access has no success event; separate hardware errors use their event conditions. <a class="qa-rule-link" href="#common-register-9">Full rule in this volume</a></p>
</li>
<li id="q-230-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Register accesses are not logged individually; preserve registers and timing before obtaining available diagnostics. <a class="qa-rule-link" href="#common-register-10">Full rule in this volume</a></p>
</li>
<li id="q-230-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>Ordinary register access is not a PEL event; completed resets and supported hardware errors are assessed separately. <a class="qa-rule-link" href="#common-register-11">Full rule in this volume</a></p>
</li>
<li id="q-230-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>CC.EN reset and FLR retain CMBMSC but make CMB contents undefined. <a class="qa-rule-link" href="#common-cmb_op-12">Full rule in this volume</a></p>
</li>
<li id="q-230-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Rediscover mappings and rebuild queues after subsystem reset; do not extend specific CC.EN/FLR retention to every reset source. <a class="qa-rule-link" href="#common-cmb_op-13">Full rule in this volume</a></p>
</li>
<li id="q-230-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>CMB has no PMR-style power-cycle persistence guarantee; reconfigure and initialize it. <a class="qa-rule-link" href="#common-cmb_op-14">Full rule in this volume</a></p>
</li>
<li id="q-230-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Host and controller CMB address ranges may differ; map equal offsets correctly and avoid DMA/PMR conflicts. <a class="qa-rule-link" href="#common-cmb_op-15">Full rule in this volume</a></p>
</li>
<li id="q-230-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Command outcomes and register status are separate evidence.</p>
</li>
<li id="q-230-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First check arithmetic overflow and which address space was used.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-hmb">Base 2.4 §5.2.30.2.3, 8.2.4</a> · <a href="#ref-cmb">Base 2.4 §8.2.1 (memory placement and lifetime)</a> · <a href="#ref-cmbreg">Base 2.4 §3.1.4 (CMBLOC, CMBSZ, CMBMSC, CMBSTS)</a> · <a href="#ref-pmr">Base 2.4 §8.2.5 (memory behavior; exclude PCIe packet detail)</a> · <a href="#ref-pmrreg">Base 2.4 §3.1.4 (PMR properties)</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-231" data-question="231"><h2><a class="qa-qid" href="#q-231">Q231</a> Do CMB configuration and contents survive reset?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-231-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-231-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Mapping retention and data retention are distinct.</p>
</li>
<li id="q-231-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>CC.EN reset and FLR explicitly retain CMBMSC; other sources use their own register rules.</p>
</li>
<li id="q-231-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Snapshot source and registers, then reread after recovery.</p>
</li>
<li id="q-231-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>CMSE0→1, Controller Reset and FLR make CMB contents undefined.</p>
</li>
<li id="q-231-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Restore mapping, initialize memory and rebuild queues, especially CQ phase bits.</p>
</li>
<li id="q-231-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>A new lifetime uses initialized contents, not old queue state.</p>
</li>
<li id="q-231-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Identical residual bytes do not turn undefined retention into a guarantee.</p>
</li>
<li id="q-231-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>CMB register/memory accesses have no CQE. <a class="qa-rule-link" href="#common-cmb_op-8">Full rule in this volume</a></p>
</li>
<li id="q-231-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Register access has no success event; separate hardware errors use their event conditions. <a class="qa-rule-link" href="#common-register-9">Full rule in this volume</a></p>
</li>
<li id="q-231-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Register accesses are not logged individually; preserve registers and timing before obtaining available diagnostics. <a class="qa-rule-link" href="#common-register-10">Full rule in this volume</a></p>
</li>
<li id="q-231-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>Ordinary register access is not a PEL event; completed resets and supported hardware errors are assessed separately. <a class="qa-rule-link" href="#common-register-11">Full rule in this volume</a></p>
</li>
<li id="q-231-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>CC.EN reset and FLR retain CMBMSC but make CMB contents undefined. <a class="qa-rule-link" href="#common-cmb_op-12">Full rule in this volume</a></p>
</li>
<li id="q-231-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Rediscover mappings and rebuild queues after subsystem reset; do not extend specific CC.EN/FLR retention to every reset source. <a class="qa-rule-link" href="#common-cmb_op-13">Full rule in this volume</a></p>
</li>
<li id="q-231-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>CMB has no PMR-style power-cycle persistence guarantee; reconfigure and initialize it. <a class="qa-rule-link" href="#common-cmb_op-14">Full rule in this volume</a></p>
</li>
<li id="q-231-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Host and controller CMB address ranges may differ; map equal offsets correctly and avoid DMA/PMR conflicts. <a class="qa-rule-link" href="#common-cmb_op-15">Full rule in this volume</a></p>
</li>
<li id="q-231-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Validate mappings and content/queue initialization separately.</p>
</li>
<li id="q-231-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First check whether unchanged CMBMSC incorrectly caused initialization to be skipped.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-hmb">Base 2.4 §5.2.30.2.3, 8.2.4</a> · <a href="#ref-cmb">Base 2.4 §8.2.1 (memory placement and lifetime)</a> · <a href="#ref-cmbreg">Base 2.4 §3.1.4 (CMBLOC, CMBSZ, CMBMSC, CMBSTS)</a> · <a href="#ref-pmr">Base 2.4 §8.2.5 (memory behavior; exclude PCIe packet detail)</a> · <a href="#ref-pmrreg">Base 2.4 §3.1.4 (PMR properties)</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-232" data-question="232"><h2><a class="qa-qid" href="#q-232">Q232</a> How is PMR discovered, enabled and made ready?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-232-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-232-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>PMR enablement is independent of the command controller and has its own readiness state.</p>
</li>
<li id="q-232-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>PMR occupies the selected BAR region, with separately configurable controller addressing.</p>
</li>
<li id="q-232-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Check support, location, command access, barrier mechanisms and timeout units.</p>
</li>
<li id="q-232-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>EN1 plus NRDY0 establishes readiness, with health/error checks still required.</p>
</li>
<li id="q-232-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Configure addressing, set EN and wait for NRDY0, allowing at least the declared timeout interval.</p>
</li>
<li id="q-232-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Use supported accesses when ready and healthy; CC.EN need not be enabled first.</p>
</li>
<li id="q-232-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>PMRTO is a transition wait allowance, not a per-command timeout; invalid addressing is reported by CBAI.</p>
</li>
<li id="q-232-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Direct PMR/register access has no CQE. <a class="qa-rule-link" href="#common-pmr_op-8">Full rule in this volume</a></p>
</li>
<li id="q-232-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Read-only/unreliable PMR sets the SMART warning and may trigger configured AER. <a class="qa-rule-link" href="#common-pmr_op-9">Full rule in this volume</a></p>
</li>
<li id="q-232-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>NRDY/HSTS/ERR are primary evidence, with SMART PMR warnings. <a class="qa-rule-link" href="#common-pmr_op-10">Full rule in this volume</a></p>
</li>
<li id="q-232-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>A PMR warning may qualify for a supported PEL critical-warning event; each read/write or EN change is not independently logged. <a class="qa-rule-link" href="#common-pmr_op-11">Full rule in this volume</a></p>
</li>
<li id="q-232-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Ready-state persistent data survives CLR. <a class="qa-rule-link" href="#common-pmr_op-12">Full rule in this volume</a></p>
</li>
<li id="q-232-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Recheck enable/readiness and HSTS after subsystem reset. <a class="qa-rule-link" href="#common-pmr_op-13">Full rule in this volume</a></p>
</li>
<li id="q-232-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Confirmed persistent writes survive power cycles, subject to restored health checks. <a class="qa-rule-link" href="#common-pmr_op-14">Full rule in this volume</a></p>
</li>
<li id="q-232-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>PMR belongs to its PCIe function; consumers must check that PMR’s health. <a class="qa-rule-link" href="#common-pmr_op-15">Full rule in this volume</a></p>
</li>
<li id="q-232-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Combine capability, enablement, readiness, health and mapping evidence.</p>
</li>
<li id="q-232-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First check inverted readiness and timeout units.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-hmb">Base 2.4 §5.2.30.2.3, 8.2.4</a> · <a href="#ref-cmb">Base 2.4 §8.2.1 (memory placement and lifetime)</a> · <a href="#ref-cmbreg">Base 2.4 §3.1.4 (CMBLOC, CMBSZ, CMBMSC, CMBSTS)</a> · <a href="#ref-pmr">Base 2.4 §8.2.5 (memory behavior; exclude PCIe packet detail)</a> · <a href="#ref-pmrreg">Base 2.4 §3.1.4 (PMR properties)</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-233" data-question="233"><h2><a class="qa-qid" href="#q-233">Q233</a> What happens for not-ready or unhealthy PMR accesses?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-233-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-233-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Completion of an access does not establish valid contents without PMR status.</p>
</li>
<li id="q-233-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Direct accesses and commands using PMR buffers expose errors differently.</p>
</li>
<li id="q-233-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Inspect EN/NRDY/HSTS/ERR; HSTS clears when not ready, so zero alone does not prove usable health.</p>
</li>
<li id="q-233-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>Not-ready reads can succeed with undefined data and writes can succeed without updating memory; health distinguishes restore failure, read-only and unreliable states.</p>
</li>
<li id="q-233-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Establish readiness, access, then verify barriers/status and reconsider accesses since the last normal health observation.</p>
</li>
<li id="q-233-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>A successful NVMe command targeting PMR does not alone prove the PMR write succeeded.</p>
</li>
<li id="q-233-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Detected failure writing an associated PMR should produce Data Transfer Error for the command; direct accesses have no NVMe CQE.</p>
</li>
<li id="q-233-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Direct PMR/register access has no CQE. <a class="qa-rule-link" href="#common-pmr_op-8">Full rule in this volume</a></p>
</li>
<li id="q-233-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Read-only/unreliable PMR sets the SMART warning and may trigger configured AER. <a class="qa-rule-link" href="#common-pmr_op-9">Full rule in this volume</a></p>
</li>
<li id="q-233-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>NRDY/HSTS/ERR are primary evidence, with SMART PMR warnings. <a class="qa-rule-link" href="#common-pmr_op-10">Full rule in this volume</a></p>
</li>
<li id="q-233-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>A PMR warning may qualify for a supported PEL critical-warning event; each read/write or EN change is not independently logged. <a class="qa-rule-link" href="#common-pmr_op-11">Full rule in this volume</a></p>
</li>
<li id="q-233-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Ready-state persistent data survives CLR. <a class="qa-rule-link" href="#common-pmr_op-12">Full rule in this volume</a></p>
</li>
<li id="q-233-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Recheck enable/readiness and HSTS after subsystem reset. <a class="qa-rule-link" href="#common-pmr_op-13">Full rule in this volume</a></p>
</li>
<li id="q-233-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Confirmed persistent writes survive power cycles, subject to restored health checks. <a class="qa-rule-link" href="#common-pmr_op-14">Full rule in this volume</a></p>
</li>
<li id="q-233-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>PMR belongs to its PCIe function; consumers must check that PMR’s health. <a class="qa-rule-link" href="#common-pmr_op-15">Full rule in this volume</a></p>
</li>
<li id="q-233-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Validate command success and PMR health separately.</p>
</li>
<li id="q-233-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First inspect readiness at access time, not merely after later recovery.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-hmb">Base 2.4 §5.2.30.2.3, 8.2.4</a> · <a href="#ref-cmb">Base 2.4 §8.2.1 (memory placement and lifetime)</a> · <a href="#ref-cmbreg">Base 2.4 §3.1.4 (CMBLOC, CMBSZ, CMBMSC, CMBSTS)</a> · <a href="#ref-pmr">Base 2.4 §8.2.5 (memory behavior; exclude PCIe packet detail)</a> · <a href="#ref-pmrreg">Base 2.4 §3.1.4 (PMR properties)</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-234" data-question="234"><h2><a class="qa-qid" href="#q-234">Q234</a> How is PMR safely disabled?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-234-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-234-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Establish completion and persistence before disabling rather than assuming in-flight writes are safe.</p>
</li>
<li id="q-234-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Coordinate direct users and commands still using PMR buffers.</p>
</li>
<li id="q-234-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Check supported barriers, health and transition wait units.</p>
</li>
<li id="q-234-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>Use the advertised PMR-read or PMRSTS-read barrier, not an arbitrary register read.</p>
</li>
<li id="q-234-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Stop accesses, drain users, perform the supported barrier/health check, clear EN and wait for NRDY1.</p>
</li>
<li id="q-234-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>NRDY1 indicates disabled readiness for re-enable; valid persistent content is not made undefined as CMB would be.</p>
</li>
<li id="q-234-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Successful disable cannot prove earlier data valid when error/health state says otherwise.</p>
</li>
<li id="q-234-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Direct PMR/register access has no CQE. <a class="qa-rule-link" href="#common-pmr_op-8">Full rule in this volume</a></p>
</li>
<li id="q-234-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Read-only/unreliable PMR sets the SMART warning and may trigger configured AER. <a class="qa-rule-link" href="#common-pmr_op-9">Full rule in this volume</a></p>
</li>
<li id="q-234-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>NRDY/HSTS/ERR are primary evidence, with SMART PMR warnings. <a class="qa-rule-link" href="#common-pmr_op-10">Full rule in this volume</a></p>
</li>
<li id="q-234-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>A PMR warning may qualify for a supported PEL critical-warning event; each read/write or EN change is not independently logged. <a class="qa-rule-link" href="#common-pmr_op-11">Full rule in this volume</a></p>
</li>
<li id="q-234-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Ready-state persistent data survives CLR. <a class="qa-rule-link" href="#common-pmr_op-12">Full rule in this volume</a></p>
</li>
<li id="q-234-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Recheck enable/readiness and HSTS after subsystem reset. <a class="qa-rule-link" href="#common-pmr_op-13">Full rule in this volume</a></p>
</li>
<li id="q-234-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Confirmed persistent writes survive power cycles, subject to restored health checks. <a class="qa-rule-link" href="#common-pmr_op-14">Full rule in this volume</a></p>
</li>
<li id="q-234-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>PMR belongs to its PCIe function; consumers must check that PMR’s health. <a class="qa-rule-link" href="#common-pmr_op-15">Full rule in this volume</a></p>
</li>
<li id="q-234-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Verify barrier/health and enable-state ordering, not only final EN0.</p>
</li>
<li id="q-234-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First verify quiesced users and the actual supported barrier.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-hmb">Base 2.4 §5.2.30.2.3, 8.2.4</a> · <a href="#ref-cmb">Base 2.4 §8.2.1 (memory placement and lifetime)</a> · <a href="#ref-cmbreg">Base 2.4 §3.1.4 (CMBLOC, CMBSZ, CMBMSC, CMBSTS)</a> · <a href="#ref-pmr">Base 2.4 §8.2.5 (memory behavior; exclude PCIe packet detail)</a> · <a href="#ref-pmrreg">Base 2.4 §3.1.4 (PMR properties)</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-235" data-question="235"><h2><a class="qa-qid" href="#q-235">Q235</a> How do resets and power cycles affect PMR state and data?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-235-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-235-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Persistence and current accessibility differ; restoration can leave retained data temporarily unavailable.</p>
</li>
<li id="q-235-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Retention applies to completed persistent writes, not unverified in-flight writes.</p>
</li>
<li id="q-235-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Preserve barrier evidence and inspect enable/readiness/health/mapping after recovery.</p>
</li>
<li id="q-235-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>Restore Error means current normal persistent operation with possibly incorrect restored content, unlike ongoing Unreliable status.</p>
</li>
<li id="q-235-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Restore readiness, inspect health and verify content, accounting separately for Sanitize.</p>
</li>
<li id="q-235-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Qualified persistent data survives CLR, disable and power cycle; register retention remains source-specific.</p>
</li>
<li id="q-235-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Nonzero ERR persists until PCI Function reset; clearing CC.EN does not necessarily clear it.</p>
</li>
<li id="q-235-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Direct PMR/register access has no CQE. <a class="qa-rule-link" href="#common-pmr_op-8">Full rule in this volume</a></p>
</li>
<li id="q-235-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Read-only/unreliable PMR sets the SMART warning and may trigger configured AER. <a class="qa-rule-link" href="#common-pmr_op-9">Full rule in this volume</a></p>
</li>
<li id="q-235-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>NRDY/HSTS/ERR are primary evidence, with SMART PMR warnings. <a class="qa-rule-link" href="#common-pmr_op-10">Full rule in this volume</a></p>
</li>
<li id="q-235-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>A PMR warning may qualify for a supported PEL critical-warning event; each read/write or EN change is not independently logged. <a class="qa-rule-link" href="#common-pmr_op-11">Full rule in this volume</a></p>
</li>
<li id="q-235-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Ready-state persistent data survives CLR. <a class="qa-rule-link" href="#common-pmr_op-12">Full rule in this volume</a></p>
</li>
<li id="q-235-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Recheck enable/readiness and HSTS after subsystem reset. <a class="qa-rule-link" href="#common-pmr_op-13">Full rule in this volume</a></p>
</li>
<li id="q-235-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Confirmed persistent writes survive power cycles, subject to restored health checks. <a class="qa-rule-link" href="#common-pmr_op-14">Full rule in this volume</a></p>
</li>
<li id="q-235-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>PMR belongs to its PCIe function; consumers must check that PMR’s health. <a class="qa-rule-link" href="#common-pmr_op-15">Full rule in this volume</a></p>
</li>
<li id="q-235-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Verify data, registers and errors as separate requirements.</p>
</li>
<li id="q-235-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First distinguish persistent-data loss from incomplete writes or premature reads.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-hmb">Base 2.4 §5.2.30.2.3, 8.2.4</a> · <a href="#ref-cmb">Base 2.4 §8.2.1 (memory placement and lifetime)</a> · <a href="#ref-cmbreg">Base 2.4 §3.1.4 (CMBLOC, CMBSZ, CMBMSC, CMBSTS)</a> · <a href="#ref-pmr">Base 2.4 §8.2.5 (memory behavior; exclude PCIe packet detail)</a> · <a href="#ref-pmrreg">Base 2.4 §3.1.4 (PMR properties)</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-236" data-question="236"><h2><a class="qa-qid" href="#q-236">Q236</a> How do host memory, HMB, CMB and PMR lifetimes compare?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-236-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-236-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Equal-looking data addresses can have different owners, initialization duties and reclamation conditions.</p>
</li>
<li id="q-236-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Ordinary host buffers are command-scoped; HMB is controller-exclusive; CMB is device-local; PMR adds persistence mechanisms.</p>
</li>
<li id="q-236-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Use capabilities and command pointers to identify the actual space.</p>
</li>
<li id="q-236-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>Reclaim ordinary buffers by command/queue lifetime, HMB after disable, initialize CMB after reset and verify PMR barriers/health.</p>
</li>
<li id="q-236-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Map host/controller addresses to physical memory and mark access/reclamation boundaries.</p>
</li>
<li id="q-236-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>A Write completion can end source-buffer use without releasing HMB or performing a PMR barrier.</p>
</li>
<li id="q-236-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Error outcomes depend on the violated interface, not one universal memory-error status.</p>
</li>
<li id="q-236-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>HMB Set Features has a CQE; direct CMB/PMR register accesses do not. <a class="qa-rule-link" href="#common-memory_compare-8">Full rule in this volume</a></p>
</li>
<li id="q-236-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>No generic success AER accompanies memory configuration; qualifying PMR health warnings use their specific SMART/event rules.</p>
</li>
<li id="q-236-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Verify HMB lifetime, CMB placement/use and PMR readiness/error/health; these observations are not per-access error-log mandates.</p>
</li>
<li id="q-236-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>Ordinary memory access is not a PEL event; supported HMB feature changes and PMR health/hardware events follow separate conditions.</p>
</li>
<li id="q-236-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>CLR invalidates HMB allocation; CMB mappings may persist while contents become undefined; persistent PMR data remains. <a class="qa-rule-link" href="#common-memory_compare-12">Full rule in this volume</a></p>
</li>
<li id="q-236-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>After subsystem reset, separately restore HMB allocation, initialize CMB and check PMR health. <a class="qa-rule-link" href="#common-memory_compare-13">Full rule in this volume</a></p>
</li>
<li id="q-236-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>HMB/CMB lack PMR persistence guarantees; PMR still requires supported barriers and health checks. <a class="qa-rule-link" href="#common-memory_compare-14">Full rule in this volume</a></p>
</li>
<li id="q-236-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Identify physical location, ownership and address space; identical numeric addresses do not prove identical buffers across mappings. <a class="qa-rule-link" href="#common-memory_compare-15">Full rule in this volume</a></p>
</li>
<li id="q-236-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Verify ownership, mapping, completion and persistence rather than merely readable contents.</p>
</li>
<li id="q-236-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First identify whether the lifetime is a command, HMB allocation, CMB mapping or persistent PMR data.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-hmb">Base 2.4 §5.2.30.2.3, 8.2.4</a> · <a href="#ref-cmb">Base 2.4 §8.2.1 (memory placement and lifetime)</a> · <a href="#ref-cmbreg">Base 2.4 §3.1.4 (CMBLOC, CMBSZ, CMBMSC, CMBSTS)</a> · <a href="#ref-pmr">Base 2.4 §8.2.5 (memory behavior; exclude PCIe packet detail)</a> · <a href="#ref-pmrreg">Base 2.4 §3.1.4 (PMR properties)</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<section id="common-rules" class="qa-common"><h2>Shared rules linked from the answers</h2><p>Each shared mechanism is explained in full once in this volume. Use browser Back to return to the question; explicit command or feature exceptions take precedence.</p>
<article id="common-cmb_op-8"><h3>Shared conditions for this topic · How are DNR and More set?</h3><p>CMB register/memory accesses have no CQE. Decode DNR/More only for an Admin/I/O command using CMB, not for MMIO itself.</p></article>
<article id="common-cmb_op-12"><h3>Shared conditions for this topic · What survives or continues after Controller Reset?</h3><p>CC.EN reset and FLR retain CMBMSC but make CMB contents undefined. Reinitialize memory, especially CQ phases; retained addressing does not preserve valid queues/data.</p></article>
<article id="common-cmb_op-13"><h3>Shared conditions for this topic · What survives or continues after NVM Subsystem Reset?</h3><p>Rediscover mappings and rebuild queues after subsystem reset; do not extend specific CC.EN/FLR retention to every reset source.</p></article>
<article id="common-cmb_op-14"><h3>Shared conditions for this topic · What survives or continues after a power cycle?</h3><p>CMB has no PMR-style power-cycle persistence guarantee; reconfigure and initialize it.</p></article>
<article id="common-cmb_op-15"><h3>Shared conditions for this topic · Are other controllers or namespaces affected?</h3><p>Host and controller CMB address ranges may differ; map equal offsets correctly and avoid DMA/PMR conflicts.</p></article>
<article id="common-command-8"><h3>Command completion, events and records · How are DNR and More set?</h3><p>For a CQE, DNR=1 means the identical command is expected to fail if resubmitted to any controller in this subsystem; DNR=0 means it may succeed. Do not assign DNR=1 solely from an error name unless that condition mandates it. More=1 identifies additional information for this command in the Error Information Log. DNR should be zero when SCT=SC=0.</p></article>
<article id="common-hmb_op-9"><h3>Shared conditions for this topic · Is an asynchronous event generated?</h3><p>HMB enable/disable has no separate success AER; independently defined hardware faults follow their own event rules.</p></article>
<article id="common-hmb_op-10"><h3>Shared conditions for this topic · Are Error Information or other logs updated?</h3><p>Get reports HMB state and allocation, not a backup of buffer contents. Successful operations require no error entry; failures use CQE/logging rules.</p></article>
<article id="common-hmb_op-11"><h3>Shared conditions for this topic · Is it recorded in the Persistent Event Log?</h3><p>Supported, permitted Set Feature logging follows successful-change rules; ordinary HMB accesses are not individual persistent events.</p></article>
<article id="common-hmb_op-12"><h3>Shared conditions for this topic · What survives or continues after Controller Reset?</h3><p>HMB allocation does not persist across CLR. Reprovide it after reset; MR=1 requires unchanged size, descriptor address/content and buffer content.</p></article>
<article id="common-hmb_op-13"><h3>Shared conditions for this topic · What survives or continues after NVM Subsystem Reset?</h3><p>Subsystem reset invalidates affected HMB allocations. Reconfigure after recovery; residual RAM bytes do not establish an active allocation.</p></article>
<article id="common-hmb_op-14"><h3>Shared conditions for this topic · What survives or continues after a power cycle?</h3><p>HMB is not persistent storage. Use MR=0 if content was lost; the controller must prevent data loss/corruption from surprise removal while using HMB.</p></article>
<article id="common-hmb_op-15"><h3>Shared conditions for this topic · Are other controllers or namespaces affected?</h3><p>HMB is host memory exclusively allocated to this controller; the host shall not modify its list/buffers while enabled or repurpose them.</p></article>
<article id="common-memory_compare-8"><h3>Shared conditions for this topic · How are DNR and More set?</h3><p>HMB Set Features has a CQE; direct CMB/PMR register accesses do not. Commands using buffers carry their own DNR/More, not one fixed memory-type value.</p></article>
<article id="common-memory_compare-12"><h3>Shared conditions for this topic · What survives or continues after Controller Reset?</h3><p>CLR invalidates HMB allocation; CMB mappings may persist while contents become undefined; persistent PMR data remains. Recheck readiness separately.</p></article>
<article id="common-memory_compare-13"><h3>Shared conditions for this topic · What survives or continues after NVM Subsystem Reset?</h3><p>After subsystem reset, separately restore HMB allocation, initialize CMB and check PMR health.</p></article>
<article id="common-memory_compare-14"><h3>Shared conditions for this topic · What survives or continues after a power cycle?</h3><p>HMB/CMB lack PMR persistence guarantees; PMR still requires supported barriers and health checks. External host-memory persistence is a separate property.</p></article>
<article id="common-memory_compare-15"><h3>Shared conditions for this topic · Are other controllers or namespaces affected?</h3><p>Identify physical location, ownership and address space; identical numeric addresses do not prove identical buffers across mappings.</p></article>
<article id="common-pmr_op-8"><h3>Shared conditions for this topic · How are DNR and More set?</h3><p>Direct PMR/register access has no CQE. Commands using a PMR buffer do, but successful CQE does not replace health/persistence verification.</p></article>
<article id="common-pmr_op-9"><h3>Shared conditions for this topic · Is an asynchronous event generated?</h3><p>Read-only/unreliable PMR sets the SMART warning and may trigger configured AER. Delivery may lag, so assess operations since the last normal HSTS observation.</p></article>
<article id="common-pmr_op-10"><h3>Shared conditions for this topic · Are Error Information or other logs updated?</h3><p>NRDY/HSTS/ERR are primary evidence, with SMART PMR warnings. Register accesses are not individually error-logged; command failures follow CQE rules.</p></article>
<article id="common-pmr_op-11"><h3>Shared conditions for this topic · Is it recorded in the Persistent Event Log?</h3><p>A PMR warning may qualify for a supported PEL critical-warning event; each read/write or EN change is not independently logged.</p></article>
<article id="common-pmr_op-12"><h3>Shared conditions for this topic · What survives or continues after Controller Reset?</h3><p>Ready-state persistent data survives CLR. CC.EN reset also retains PMR control/status registers; inspect health and Restore Error nonetheless.</p></article>
<article id="common-pmr_op-13"><h3>Shared conditions for this topic · What survives or continues after NVM Subsystem Reset?</h3><p>Recheck enable/readiness and HSTS after subsystem reset. Data persistence differs from register restoration; Restore Error questions restored contents.</p></article>
<article id="common-pmr_op-14"><h3>Shared conditions for this topic · What survives or continues after a power cycle?</h3><p>Confirmed persistent writes survive power cycles, subject to restored health checks. Sanitize can purge PMR and is distinct from ordinary power-loss behavior.</p></article>
<article id="common-pmr_op-15"><h3>Shared conditions for this topic · Are other controllers or namespaces affected?</h3><p>PMR belongs to its PCIe function; consumers must check that PMR’s health. A command’s data and metadata must be entirely inside or outside PMR.</p></article>
<article id="common-register-9"><h3>Register access · Is an asynchronous event generated?</h3><p>This register access does not define a success notification. A separate defined event, such as an Internal Error, follows its own rules. When the Admin Queue is unavailable, waiting for an event cannot replace initialization-state checks.</p></article>
<article id="common-register-10"><h3>Register access · Are Error Information or other logs updated?</h3><p>Every register read or write does not require an Error Information entry. Preserve CAP, CC, CSTS, CRTO and timestamps first; logs provide additional evidence if the controller subsequently permits access.</p></article>
<article id="common-register-11"><h3>Register access · Is it recorded in the Persistent Event Log?</h3><p>An ordinary register access is not a separate persistent event. Reset, power or hardware conditions are recorded when PEL support and the corresponding event requirements apply; each CC write is not automatically a Power-on or Reset event.</p></article>
</section>
<section id="source-index"><h2>Source locations and existing figure guides</h2><p>Base printed page = PDF page−26; the other two use identical numbers. Locations follow the supplied PDF body and retain figure numbers. Shared pages contribute only the relevant definitions, excluding Fabrics and PCIe link/packet content.</p><ul class="qa-references">
<li id="ref-cmbreg"><strong>Base 2.4 · §3.1.4 (CMBLOC, CMBSZ, CMBMSC, CMBSTS)</strong><br>Printed pages 67–69, 70–72 · PDF 93–95, 96–98 · Figure 47–48, 52–55</li>
<li id="ref-pmrreg"><strong>Base 2.4 · §3.1.4 (PMR properties)</strong><br>Printed pages 73–77 · PDF 99–103 · Figure 58–64</li>
<li id="ref-reset"><strong>Base 2.4 · §3.7.1–3.7.4</strong><br>Printed pages 120–124 · PDF 146–150</li>
<li id="ref-status"><strong>Base 2.4 · §4.2.3</strong><br>Printed pages 145–155 · PDF 171–181 · Figure 101–105</li>
<li id="ref-aer"><strong>Base 2.4 · §5.2.2</strong><br>Printed pages 183–190 · PDF 209–216 · Figure 150–156</li>
<li id="ref-error"><strong>Base 2.4 · §5.2.13.1.2</strong><br>Printed pages 218–220 · PDF 244–246 · Figure 212</li>
<li id="ref-pel"><strong>Base 2.4 · §5.2.13.1.14 (header, reset, hardware, Set Feature events)</strong><br>Printed pages 244–256, 258, 262–264 · PDF 270–282, 284, 288–290 · Figure 232–244, 246, 252–253</li>
<li id="ref-idctrl"><strong>Base 2.4 · §5.2.14.2.1</strong><br>Printed pages 340–387 · PDF 366–413 · Figure 338–341</li>
<li id="ref-hmb"><strong>Base 2.4 · §5.2.30.2.3, 8.2.4</strong><br>Printed pages 515–519, 744 · PDF 541–545, 770 · Figure 545–553</li>
<li id="ref-cmb"><strong>Base 2.4 · §8.2.1 (memory placement and lifetime)</strong><br>Printed pages 742–744 · PDF 768–770</li>
<li id="ref-pmr"><strong>Base 2.4 · §8.2.5 (memory behavior; exclude PCIe packet detail)</strong><br>Printed pages 745–746 · PDF 771–772</li>
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
<nav class="qr-top" aria-label="Bank and editions"><a href="#content">Skip to content</a><a href="/nvme/question-bank/en/">Question index</a><a href="/nvme/question-bank/memory/zh-tw/">繁體中文</a><a href="/DOCS/nvme-question-bank/memory.html">Chinese tutorial HTML</a></nav>
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
