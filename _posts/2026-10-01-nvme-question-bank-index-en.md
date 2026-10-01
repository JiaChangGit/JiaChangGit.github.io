---
layout: post
title: "NVMe Self-Study Bank: Index · Q1–68"
date: 2026-10-01 00:00:00 +0800
categories: [nvme]
permalink: /nvme/question-bank/en/
lang: en
nvme_quickref: true
nvme_qa: true
---

<div class="nvme-quickref nvme-qa">
<nav class="qr-top" aria-label="Bank and editions"><a href="#content">Skip to content</a><a href="/nvme/question-bank/en/">Question index</a><a href="/nvme/question-bank/zh-tw/">繁體中文</a><a href="/DOCS/nvme-question-bank/index.html">Chinese tutorial HTML</a></nav>
<main id="content"><p class="qr-eyebrow">BASE 2.4 / NVM 1.3 / PCIe 1.4 · Q1–68</p>
<h1>NVMe Base 2.4 Self-Study Question Bank</h1><p class="qr-intro">Questions 1–68 in six volumes: from controller enable, queues and commands to capability discovery and configuration. Learn both the mechanisms and how to judge observations against the specification.</p><div class="qr-series">
<article><h2><a href="/nvme/question-bank/initialization/en/">Controller initialization and disable</a></h2><p class="qr-tags">Q1–Q9</p><p>Understand controller state transitions before commands. Discovering capabilities is not enabling; setting EN is not readiness; RDY=1 need not establish readiness of every media operation. This volume connects timing, state and permitted actions.</p></article>
<article><h2><a href="/nvme/question-bank/queues/en/">Admin and I/O queues</a></h2><p class="qr-tags">Q10–Q21</p><p>Queue memory, allocated queue counts and successfully created queues are distinct. Learn SQ/CQ dependencies before size, identifiers, deletion and reset so memory can be reclaimed at the right time.</p></article>
<article><h2><a href="/nvme/question-bank/doorbells/en/">Doorbells, full queues and wrap-around</a></h2><p class="qr-tags">Q22–Q30</p><p>Doorbells communicate pointer positions; phase tells the host whether a CQ slot belongs to the next completion generation. Together they distinguish wrap-around from an invalid movement and new completions from stale ones.</p></article>
<article><h2><a href="/nvme/question-bank/commands/en/">Commands, completions and processing order</a></h2><p class="qr-tags">Q31–Q43</p><p>Follow submission, consumption, processing, completion and host reclamation to learn what each field proves. Ordering, arbitration, fairness and interrupts answer different questions; completion order alone cannot establish them all.</p></article>
<article><h2><a href="/nvme/question-bank/identify/en/">Identify and capability discovery</a></h2><p class="qr-tags">Q44–Q53</p><p>Treat Identify as several distinct query interfaces. Choose the object and structure before CNS, CSI, NSID and other selectors. Separate capability, current configuration and changing lists to find real contradictions.</p></article>
<article><h2><a href="/nvme/question-bank/features/en/">Get Features and Set Features</a></h2><p class="qr-tags">Q54–Q68</p><p>Establish scope, changeability and saveability before Set. Completion, Current readback, actual behavior and restoration after reset are separate observations; a successful CQE does not replace them.</p></article>
</div><section><h2>How to use this bank</h2><ol><li>Explain purpose, affected objects and sequence before selecting query fields.</li><li>Reveal the answer and separately compare success, errors, events, logs and three reset cases. Items without an MMIO CQE explicitly state non-applicability.</li><li>Establish preconditions before judging firmware. Shall is a requirement, should a recommendation, may permission. Undefined behavior does not supply a fixed expected status.</li></ol><p>All numerical examples are hypothetical, not hardware measurements. The scope is the three specifications as used by PCIe SSDs, excluding NVMe over Fabrics and PCIe link/packet details while retaining necessary PCIe configuration, interrupts, registers and doorbells.</p></section>
<div class="qa-controls" hidden><label>Search this page <input type="search" id="qa-search" placeholder="Question number, field or keyword"></label><output id="qa-count" aria-live="polite"></output></div>
<section id="question-index"><h2>All questions</h2><ol class="qa-index">
<li class="qa-search-item"><a href="/nvme/question-bank/initialization/en/#q-001">Q01 · How does a host discover version, queue limits, timeouts, doorbell stride, page sizes and command sets from CAP and VS?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/initialization/en/#q-002">Q02 · In what order are AQA, ASQ, ACQ and CC programmed, and what happens if they are wrong?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/initialization/en/#q-003">Q03 · How does a host judge enable completion using CC.EN, CSTS.RDY and the timeout fields?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/initialization/en/#q-004">Q04 · How is disable completion detected, and may the host re-enable before it completes?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/initialization/en/#q-005">Q05 · May a host submit commands or update doorbells while CSTS.RDY is zero?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/initialization/en/#q-006">Q06 · What does CSTS.CFS mean, and how should the host recover from initialization failure or a fatal state?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/initialization/en/#q-007">Q07 · Which ready modes exist, and how should the host handle limited readiness?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/initialization/en/#q-008">Q08 · How do Enable, Disable, Controller Reset, NVM Subsystem Reset and Shutdown differ?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/initialization/en/#q-009">Q09 · What must be reinitialized after Controller Reset?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/queues/en/#q-010">Q10 · How are the Admin Submission and Completion Queues established through AQA, ASQ and ACQ?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/queues/en/#q-011">Q11 · What are the size, base-address and page-alignment requirements for Admin and I/O queues?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/queues/en/#q-012">Q12 · How are I/O CQs and SQs created, and why must the CQ be created first?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/queues/en/#q-013">Q13 · How does sharing a CQ differ from giving every SQ its own CQ?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/queues/en/#q-014">Q14 · How does the host determine supported queue memory layouts?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/queues/en/#q-015">Q15 · Which statuses apply to duplicate/zero QIDs, missing CQIDs, oversized queues and invalid vectors?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/queues/en/#q-016">Q16 · How do Number of Queues results relate to queues that can actually be created?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/queues/en/#q-017">Q17 · Why must associated SQs be deleted before their CQ?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/queues/en/#q-018">Q18 · What happens when deleting a missing queue, a referenced CQ or an SQ with outstanding commands?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/queues/en/#q-019">Q19 · May the controller access deleted queue memory or post completions for its old commands?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/queues/en/#q-020">Q20 · What is the scope of Queue Level Reset, and how is outstanding work handled?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/queues/en/#q-021">Q21 · Are old I/O queues valid after Controller Reset, and what must the host do again?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/doorbells/en/#q-022">Q22 · When should the host update SQ Tail and CQ Head doorbells?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/doorbells/en/#q-023">Q23 · What happens with repeated, apparently backward, out-of-range or wrong-QID doorbells?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/doorbells/en/#q-024">Q24 · How are SQ/CQ doorbell addresses calculated from CAP.DSTRD?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/doorbells/en/#q-025">Q25 · May the host access doorbells of uncreated/deleted queues or a disabled controller?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/doorbells/en/#q-026">Q26 · How should SQ Tail and CQ Head wrap around?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/doorbells/en/#q-027">Q27 · How does the CQ phase change across wrap, and how does the host identify a new completion?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/doorbells/en/#q-028">Q28 · How does CQ Full arise, and may related SQ processing continue?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/doorbells/en/#q-029">Q29 · How does processing resume when the host releases CQ space?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/doorbells/en/#q-030">Q30 · How does the host identify completions from SQs sharing a CQ?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/commands/en/#q-031">Q31 · What do Opcode, CID, NSID, Data Pointer and command dwords mean?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/commands/en/#q-032">Q32 · How are nonzero reserved fields, illegal field combinations and unsupported opcodes handled?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/commands/en/#q-033">Q33 · Which statuses apply to invalid, inactive, unused and improperly broadcast NSIDs?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/commands/en/#q-034">Q34 · What are SQHD, SQID, CID, phase and status used for in a CQE?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/commands/en/#q-035">Q35 · How should Status Code Type and Status Code be decoded?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/commands/en/#q-036">Q36 · What do More and DNR mean, and does DNR=0 guarantee an immediate safe retry?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/commands/en/#q-037">Q37 · Why might a posted completion remain unprocessed by the host?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/commands/en/#q-038">Q38 · Must outstanding commands complete in submission order?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/commands/en/#q-039">Q39 · Which commands have ordering dependencies, and why is universal ordered completion unsafe to assume?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/commands/en/#q-040">Q40 · How do outstanding limits and CQ Full constrain further command handling?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/commands/en/#q-041">Q41 · How do Round Robin and Weighted Round Robin arbitration differ?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/commands/en/#q-042">Q42 · When do Urgent, High, Medium and Low queue priorities take effect?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/commands/en/#q-043">Q43 · How can arbitration be evaluated when multiple queues compete?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/identify/en/#q-044">Q44 · What important information is provided by Identify Controller and Identify Namespace?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/identify/en/#q-045">Q45 · How do active, allocated and namespace descriptor lists differ?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/identify/en/#q-046">Q46 · What are Controller Lists, the UUID List and I/O Command Set Identify data used for?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/identify/en/#q-047">Q47 · Which Identify structures describe NVM Sets, Endurance Groups, Domains and Secondary Controllers?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/identify/en/#q-048">Q48 · How should unsupported or invalid CNS, CSI, NSID and UUID Index values be handled?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/identify/en/#q-049">Q49 · How are SN, MN, FR, MDTS and optional Admin capability fields interpreted?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/identify/en/#q-050">Q50 · How can advertised Identify support be cross-checked against commands and the Commands Supported and Effects Log?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/identify/en/#q-051">Q51 · Which Identify data and lists change after namespace creation, deletion, attachment, detachment or format?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/identify/en/#q-052">Q52 · Which Identify data may change after firmware activation, reset or power cycling?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/identify/en/#q-053">Q53 · How should inconsistencies among Identify, features, logs and command behavior be investigated?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/features/en/#q-054">Q54 · What do Current, Default, Saved and Supported Capabilities mean?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/features/en/#q-055">Q55 · How does Set Features.Save affect values after reset and power cycling?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/features/en/#q-056">Q56 · Which errors apply to unsupported features, invalid values and unsupported Save?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/features/en/#q-057">Q57 · How does the host determine whether a feature requires NSID?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/features/en/#q-058">Q58 · How are Arbitration, Number of Queues and I/O Command Set Profile configured and checked?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/features/en/#q-059">Q59 · How are interrupt coalescing and vector configuration set and verified?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/features/en/#q-060">Q60 · What do Volatile Write Cache and Write Atomicity Normal control?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/features/en/#q-061">Q61 · How does Asynchronous Event Configuration select reported events?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/features/en/#q-062">Q62 · How do Power Management, APST and Host Controlled Thermal Management differ?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/features/en/#q-063">Q63 · How are Timestamp, Keep Alive Timer and Host Memory Buffer configured and verified?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/features/en/#q-064">Q64 · What do Host Behavior Support, Error Recovery and Read Recovery Level do?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/features/en/#q-065">Q65 · How is namespace write protection configured, and which modes survive reset or power cycling?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/features/en/#q-066">Q66 · Why read Get Features after a successful Set Features?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/features/en/#q-067">Q67 · How should features change after activation, namespace deletion, reset and power cycling?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/features/en/#q-068">Q68 · How should supported-feature claims be checked when Get, Set and behavior appear inconsistent?</a></li>
</ol></section>
</main>
<nav class="qr-top" aria-label="Bank and editions"><a href="#content">Skip to content</a><a href="/nvme/question-bank/en/">Question index</a><a href="/nvme/question-bank/zh-tw/">繁體中文</a><a href="/DOCS/nvme-question-bank/index.html">Chinese tutorial HTML</a></nav>
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
