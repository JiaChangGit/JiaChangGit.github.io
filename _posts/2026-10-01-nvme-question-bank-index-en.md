---
layout: post
title: "NVMe Self-Study Bank: Index · Q1–328"
date: 2026-10-01 00:00:00 +0800
categories: [nvme]
permalink: /nvme/question-bank/en/
lang: en
nvme_quickref: true
nvme_qa: true
---

<div class="nvme-quickref nvme-qa">
<nav class="qr-top" aria-label="Bank and editions"><a href="#content">Skip to content</a><a href="/nvme/question-bank/en/">Question index</a><a href="/nvme/question-bank/zh-tw/">繁體中文</a><a href="/DOCS/nvme-question-bank/index.html">Chinese tutorial HTML</a></nav>
<main id="content"><p class="qr-eyebrow">BASE 2.4 / NVM 1.3 / PCIe 1.4 · Q1–328</p>
<h1>NVMe Base 2.4 Self-Study Question Bank</h1><p class="qr-intro">Questions 1–328 in 27 volumes: from controller enable, queues and commands to capability discovery and configuration. Learn both the mechanisms and how to judge observations against the specification.</p><div class="qr-series">
<article><h2><a href="/nvme/question-bank/initialization/en/">Controller initialization and disable</a></h2><p class="qr-tags">Q1–Q9</p><p>Understand controller state transitions before commands. Discovering capabilities is not enabling; setting EN is not readiness; RDY=1 need not establish readiness of every media operation. This volume connects timing, state and permitted actions.</p></article>
<article><h2><a href="/nvme/question-bank/queues/en/">Admin and I/O queues</a></h2><p class="qr-tags">Q10–Q21</p><p>Queue memory, allocated queue counts and successfully created queues are distinct. Learn SQ/CQ dependencies before size, identifiers, deletion and reset so memory can be reclaimed at the right time.</p></article>
<article><h2><a href="/nvme/question-bank/doorbells/en/">Doorbells, full queues and wrap-around</a></h2><p class="qr-tags">Q22–Q30</p><p>Doorbells communicate pointer positions; phase tells the host whether a CQ slot belongs to the next completion generation. Together they distinguish wrap-around from an invalid movement and new completions from stale ones.</p></article>
<article><h2><a href="/nvme/question-bank/commands/en/">Commands, completions and processing order</a></h2><p class="qr-tags">Q31–Q43</p><p>Follow submission, consumption, processing, completion and host reclamation to learn what each field proves. Ordering, arbitration, fairness and interrupts answer different questions; completion order alone cannot establish them all.</p></article>
<article><h2><a href="/nvme/question-bank/identify/en/">Identify and capability discovery</a></h2><p class="qr-tags">Q44–Q53</p><p>Treat Identify as several distinct query interfaces. Choose the object and structure before CNS, CSI, NSID and other selectors. Separate capability, current configuration and changing lists to find real contradictions.</p></article>
<article><h2><a href="/nvme/question-bank/features/en/">Get Features and Set Features</a></h2><p class="qr-tags">Q54–Q68</p><p>Establish scope, changeability and saveability before Set. Completion, Current readback, actual behavior and restoration after reset are separate observations; a successful CQE does not replace them.</p></article>
<article><h2><a href="/nvme/question-bank/logs/en/">Get Log Page and data consistency</a></h2><p class="qr-tags">Q69–Q81</p><p>Logs expose state, history or capability, with different lifetimes and read effects. Choose the view and scope before length, pagination, acknowledgment and consistency.</p></article>
<article><h2><a href="/nvme/question-bank/asynchronous-events/en/">Asynchronous Event Request</a></h2><p class="qr-tags">Q82–Q92</p><p>AER preposts requests that complete on events. Connect requests, events, logs and acknowledgment before concurrency and rearming.</p></article>
<article><h2><a href="/nvme/question-bank/errors/en/">Error status and Error Information</a></h2><p class="qr-tags">Q93–Q106</p><p>Start with one failed command, classify it and correlate completion with supplemental records and recovery evidence.</p></article>
<article><h2><a href="/nvme/question-bank/recovery/en/">Abort, timeout and recovery</a></h2><p class="qr-tags">Q107–Q117</p><p>A timeout is an observation, not a location. Follow submission through consumption before choosing abort or reset.</p></article>
<article><h2><a href="/nvme/question-bank/format-sanitize/en/">Format and sanitize</a></h2><p class="qr-tags">Q118–Q135</p><p>Format changes namespace format; sanitize removes data. Compare scope, completion and reset behavior across the operation lifecycle.</p></article>
<article><h2><a href="/nvme/question-bank/firmware-boot/en/">Firmware update and boot partitions</a></h2><p class="qr-tags">Q136–Q148</p><p>Separate download, commit and activation, then compare boot-image access and selection.</p></article>
<article><h2><a href="/nvme/question-bank/self-test/en/">Device self-test</a></h2><p class="qr-tags">Q149–Q156</p><p>Establish supported tests, then distinguish progress, final results and valid failure details.</p></article>
<article><h2><a href="/nvme/question-bank/namespace-management/en/">Namespace management, attachment and protection</a></h2><p class="qr-tags">Q157–Q173</p><p>Creation, attachment and write protection are separate states connected through a namespace lifecycle.</p></article>
<article><h2><a href="/nvme/question-bank/reset-shutdown/en/">Reset and shutdown</a></h2><p class="qr-tags">Q174–Q187</p><p>Reset rebuilds an operating context while shutdown prepares stopping; compare scope, completion and retained operations.</p></article>
<article><h2><a href="/nvme/question-bank/health/en/">Power, thermal and health monitoring</a></h2><p class="qr-tags">Q188–Q204</p><p>Power states, thermal control and health counters are related but answer different questions. Learn state and timing before warnings and workload.</p></article>
<article><h2><a href="/nvme/question-bank/persistent-events/en/">Persistent Event Log and Timestamp</a></h2><p class="qr-tags">Q205–Q216</p><p>Retrieve a consistent PEL before interpreting variable lengths, event types and changing time bases.</p></article>
<article><h2><a href="/nvme/question-bank/keep-alive/en/">Keep Alive</a></h2><p class="qr-tags">Q217–Q222</p><p>Optional PCIe Keep Alive detects host liveness through command-based or traffic-based timing.</p></article>
<article><h2><a href="/nvme/question-bank/memory/en/">HMB, CMB and PMR</a></h2><p class="qr-tags">Q223–Q236</p><p>Compare location, ownership, lifetime and persistence rather than treating all memory facilities alike.</p></article>
<article><h2><a href="/nvme/question-bank/security/en/">Security and Lockdown</a></h2><p class="qr-tags">Q237–Q245</p><p>Security commands transport protocol data; Lockdown prohibits selected operations. Separate protocol results, prohibition scope and persistence.</p></article>
<article><h2><a href="/nvme/question-bank/virtualization/en/">Multi-controller and virtualization</a></h2><p class="qr-tags">Q246–Q255</p><p>Separate multipath, shared storage and virtualization before combining topology, attachment, ANA and resources.</p></article>
<article><h2><a href="/nvme/question-bank/capacity/en/">NVM sets, endurance groups and capacity</a></h2><p class="qr-tags">Q256–Q267</p><p>Establish ownership before interpreting layer-specific capacity and group-scoped health.</p></article>
<article><h2><a href="/nvme/question-bank/media/en/">Domains, reclaim groups and media units</a></h2><p class="qr-tags">Q268–Q275</p><p>Distinguish ownership from FDP placement, then follow identifiers to an RU and interpret media-report limits.</p></article>
<article><h2><a href="/nvme/question-bank/pointers/en/">PRP and SGL</a></h2><p class="qr-tags">Q276–Q285</p><p>Learn memory layout through PRP boundary calculations, SGL descriptor relationships and distinct error classes.</p></article>
<article><h2><a href="/nvme/question-bank/interrupts/en/">Interrupt configuration and completion delivery</a></h2><p class="qr-tags">Q286–Q296</p><p>Establish CQE posting before diagnosing routing, aggregation, masks and host consumption.</p></article>
<article><h2><a href="/nvme/question-bank/integration/en/">Integrated validation and evidence correlation</a></h2><p class="qr-tags">Q297–Q320</p><p>Apply prior mechanisms to apparent contradictions, matching identity and time before judging evidence.</p></article>
<article><h2><a href="/nvme/question-bank/data-io/en/">Data I/O: size, persistence and integrity</a></h2><p class="qr-tags">Q321–Q328</p><p>This supplement develops data-I/O reasoning not previously covered in depth: request validity, completion guarantees, content verification and partial failure effects. Derive answers from concrete field values while linking back to existing feature, queue and pointer lessons.</p></article>
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
<li class="qa-search-item"><a href="/nvme/question-bank/logs/en/#q-069">Q69 · What does Supported Log Pages provide, and how should support be checked before reading another log?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/logs/en/#q-070">Q70 · What do Error Information and SMART/Health Information record?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/logs/en/#q-071">Q71 · What do Firmware Slot, Changed Namespace and Commands Supported and Effects logs establish?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/logs/en/#q-072">Q72 · When should Device Self-test, Persistent Event and Sanitize Status logs be used?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/logs/en/#q-073">Q73 · What do Endurance Group, Predictable Latency, Lockdown, Boot Partition and Media Unit Status logs contain?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/logs/en/#q-074">Q74 · How should NSID and other selectors follow a log’s scope?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/logs/en/#q-075">Q75 · How are large logs read in chunks, including offsets, lengths, overlaps and gaps?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/logs/en/#q-076">Q76 · What are LSI, UUID Index and Retain Asynchronous Event used for?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/logs/en/#q-077">Q77 · How can a host detect inconsistent log chunks when content changes?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/logs/en/#q-078">Q78 · How are old records handled when Error Information or PEL reaches capacity?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/logs/en/#q-079">Q79 · Which log data survives controller reset, subsystem reset or power cycling?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/logs/en/#q-080">Q80 · How should advertised log/command support be checked against actual behavior?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/logs/en/#q-081">Q81 · How does Commands Supported and Effects describe opcode support and impact?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/asynchronous-events/en/#q-082">Q82 · Why post Asynchronous Event Requests before events, and why do they remain outstanding?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/asynchronous-events/en/#q-083">Q83 · How does AER completion identify the event and its log?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/asynchronous-events/en/#q-084">Q84 · Why read the associated log and post another AER after an event?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/asynchronous-events/en/#q-085">Q85 · What happens when outstanding AERs exceed the controller limit?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/asynchronous-events/en/#q-086">Q86 · How are events handled when no AER is outstanding?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/asynchronous-events/en/#q-087">Q87 · How can concurrent identical or different events be combined and reported?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/asynchronous-events/en/#q-088">Q88 · How does Asynchronous Event Configuration enable or disable notifications?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/asynchronous-events/en/#q-089">Q89 · What notification conditions apply to SMART, namespaces, firmware, telemetry, sanitize, self-test and PEL?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/asynchronous-events/en/#q-090">Q90 · How does reading a log clear or retain an event?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/asynchronous-events/en/#q-091">Q91 · Can AER be aborted, and what happens to pending requests during reset?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/asynchronous-events/en/#q-092">Q92 · How should an AER be investigated when the associated log lacks expected information?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/errors/en/#q-093">Q93 · How do opcode, field, CID and sequence errors differ?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/errors/en/#q-094">Q94 · How are namespace, log, queue, size and vector errors located?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/errors/en/#q-095">Q95 · Why must firmware, format and capacity errors be tied to their commands?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/errors/en/#q-096">Q96 · How do transfer, internal and namespace-readiness errors differ?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/errors/en/#q-097">Q97 · How do power loss, abort, SQ deletion and fused failures appear?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/errors/en/#q-098">Q98 · How do status, More, DNR and CRD guide recovery?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/errors/en/#q-099">Q99 · Which errors require Error Information?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/errors/en/#q-100">Q100 · How is an error entry correlated with its command and parameter?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/errors/en/#q-101">Q101 · Must an error entry match every CQE status bit?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/errors/en/#q-102">Q102 · How do concurrent errors, log capacity and Error Count interact?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/errors/en/#q-103">Q103 · Is a non-success CQE without a new error entry always nonconforming?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/errors/en/#q-104">Q104 · Can other commands continue after an ordinary command error?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/errors/en/#q-105">Q105 · When may serious failures set CFS, and how should the host interpret it?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/errors/en/#q-106">Q106 · How are CQEs, Error Information and persistent events correlated?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/recovery/en/#q-107">Q107 · How does Abort identify its target with SQID and CID?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/recovery/en/#q-108">Q108 · What happens when Abort targets a completed or missing command?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/recovery/en/#q-109">Q109 · How does ACL apply to repeated and concurrent Abort commands?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/recovery/en/#q-110">Q110 · Does successful Abort prove that the target never executed?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/recovery/en/#q-111">Q111 · Can a target complete normally if Abort did not immediately cancel it?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/recovery/en/#q-112">Q112 · How does the host handle racing Abort and target completions?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/recovery/en/#q-113">Q113 · Must every timeout follow Abort, queue reset, then controller reset?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/recovery/en/#q-114">Q114 · How should the host recover when Abort itself times out?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/recovery/en/#q-115">Q115 · How are old commands, completions and queues handled after reset?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/recovery/en/#q-116">Q116 · How do command, ready and long-operation timeouts differ?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/recovery/en/#q-117">Q117 · How is a timeout located along submission, execution and completion?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/format-sanitize/en/#q-118">Q118 · How are Format and Sanitize capabilities established?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/format-sanitize/en/#q-119">Q119 · How do Format, secure erase and the two sanitize targets differ?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/format-sanitize/en/#q-120">Q120 · How are Format data format, metadata, PI and SES selected?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/format-sanitize/en/#q-121">Q121 · How are invalid Format parameters and states reported?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/format-sanitize/en/#q-122">Q122 · Which Admin operations can continue during Format?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/format-sanitize/en/#q-123">Q123 · How is interrupted Format assessed after reset or power loss?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/format-sanitize/en/#q-124">Q124 · Which namespace data must be refreshed after Format?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/format-sanitize/en/#q-125">Q125 · How are Format failures checked using CQE, Error Log and PEL?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/format-sanitize/en/#q-126">Q126 · How does SANICAP advertise sanitize methods?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/format-sanitize/en/#q-127">Q127 · How do NDAS, overwrite pattern, passes and inversion work?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/format-sanitize/en/#q-128">Q128 · How are progress, status, state and erased-data flags interpreted together?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/format-sanitize/en/#q-129">Q129 · Which commands are permitted during subsystem sanitization?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/format-sanitize/en/#q-130">Q130 · Does sanitization continue across reset or power loss?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/format-sanitize/en/#q-131">Q131 · How do success, failure and failure mode differ in the log?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/format-sanitize/en/#q-132">Q132 · What does Exit Failure Mode accomplish?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/format-sanitize/en/#q-133">Q133 · When are sanitize AERs and persistent events generated?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/format-sanitize/en/#q-134">Q134 · How is namespace sanitization targeted and isolated?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/format-sanitize/en/#q-135">Q135 · How are invalid or unsupported namespace sanitize requests handled?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/firmware-boot/en/#q-136">Q136 · Where are firmware slot count, protection and usage reported?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/firmware-boot/en/#q-137">Q137 · How do OFST and NUMD describe firmware download pieces?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/firmware-boot/en/#q-138">Q138 · How are overlap, gaps, order and invalid images handled?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/firmware-boot/en/#q-139">Q139 · How are Firmware Commit slot and action selected?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/firmware-boot/en/#q-140">Q140 · How do immediate and reset-triggered activation differ?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/firmware-boot/en/#q-141">Q141 · When is Firmware Activation Starting reported?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/firmware-boot/en/#q-142">Q142 · How are firmware-update interruptions recovered?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/firmware-boot/en/#q-143">Q143 · How does firmware-load failure recovery work?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/firmware-boot/en/#q-144">Q144 · How is completed activation verified?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/firmware-boot/en/#q-145">Q145 · What should persist or be rediscovered after activation?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/firmware-boot/en/#q-146">Q146 · How are boot partition support, state and active ID discovered?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/firmware-boot/en/#q-147">Q147 · How are boot images downloaded, committed and selected?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/firmware-boot/en/#q-148">Q148 · How do boot and controller-firmware updates differ?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/self-test/en/#q-149">Q149 · How are self-test support and coverage established?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/self-test/en/#q-150">Q150 · How do short and extended self-tests differ?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/self-test/en/#q-151">Q151 · What happens when self-test is restarted or cancelled?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/self-test/en/#q-152">Q152 · How are current operation and completion percentage interpreted?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/self-test/en/#q-153">Q153 · How are self-test outcomes and interruption effects interpreted?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/self-test/en/#q-154">Q154 · Does every self-test completion generate an AER?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/self-test/en/#q-155">Q155 · When are segment, diagnostic and failing-LBA fields valid?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/self-test/en/#q-156">Q156 · How are the 20 self-test results ordered and replaced?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/namespace-management/en/#q-157">Q157 · How are namespace management and attachment supported?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/namespace-management/en/#q-158">Q158 · How are size, capacity, format and thin provisioning selected?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/namespace-management/en/#q-159">Q159 · How are namespace-creation resource and parameter errors reported?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/namespace-management/en/#q-160">Q160 · How does creation change the allocated namespace list?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/namespace-management/en/#q-161">Q161 · How are controllers selected for attachment changes?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/namespace-management/en/#q-162">Q162 · How are active and controller lists cross-checked?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/namespace-management/en/#q-163">Q163 · How are attachment relationship errors reported?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/namespace-management/en/#q-164">Q164 · What happens to outstanding commands during detach?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/namespace-management/en/#q-165">Q165 · How are commands handled after namespace detach?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/namespace-management/en/#q-166">Q166 · How are nonexistent or attached namespace deletions handled?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/namespace-management/en/#q-167">Q167 · Which events and logs follow namespace changes?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/namespace-management/en/#q-168">Q168 · How does changed-namespace overflow work?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/namespace-management/en/#q-169">Q169 · Do namespace configuration and attachment survive resets?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/namespace-management/en/#q-170">Q170 · How do private and shared namespaces differ?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/namespace-management/en/#q-171">Q171 · How do write-protection modes and entry controls differ?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/namespace-management/en/#q-172">Q172 · How does write protection persist across reset and power?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/namespace-management/en/#q-173">Q173 · How does protection affect format, sanitize and namespace management?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/reset-shutdown/en/#q-174">Q174 · How do controller, subsystem and queue resets differ?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/reset-shutdown/en/#q-175">Q175 · How do PCIe reset types affect NVMe?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/reset-shutdown/en/#q-176">Q176 · How do reset outcomes depend on ongoing activity?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/reset-shutdown/en/#q-177">Q177 · How does RDY behave during reset?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/reset-shutdown/en/#q-178">Q178 · What needs rebuilding after reset?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/reset-shutdown/en/#q-179">Q179 · How are old outstanding commands handled after reset?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/reset-shutdown/en/#q-180">Q180 · How is state revalidated after reset?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/reset-shutdown/en/#q-181">Q181 · What if reset times out or CFS remains?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/reset-shutdown/en/#q-182">Q182 · How is normal shutdown requested?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/reset-shutdown/en/#q-183">Q183 · When is power removal appropriate?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/reset-shutdown/en/#q-184">Q184 · How do normal, abrupt and unannounced loss differ?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/reset-shutdown/en/#q-185">Q185 · What may remain outstanding during shutdown?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/reset-shutdown/en/#q-186">Q186 · How do shutdown modes affect the former Unsafe Shutdowns counter?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/reset-shutdown/en/#q-187">Q187 · Why inspect health, errors and persistent events after loss?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/health/en/#q-188">Q188 · What does a Power State Descriptor tell the host?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/health/en/#q-189">Q189 · How do operational and non-operational power states differ?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/health/en/#q-190">Q190 · How do entry and exit latency affect command waits?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/health/en/#q-191">Q191 · How is APST configured, triggered and disabled?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/health/en/#q-192">Q192 · How should an apparent EXLAT violation be evaluated?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/health/en/#q-193">Q193 · How should HCTM TMT1 and TMT2 be configured?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/health/en/#q-194">Q194 · When does thermal management start and stop?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/health/en/#q-195">Q195 · How are power and thermal settings restored?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/health/en/#q-196">Q196 · What do SMART Critical Warning bits mean?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/health/en/#q-197">Q197 · How are spare capacity and percentage used interpreted?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/health/en/#q-198">Q198 · How do SMART workload and uptime counters accumulate?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/health/en/#q-199">Q199 · How do unexpected power-loss and error counters accumulate?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/health/en/#q-200">Q200 · How are warning and critical temperature times counted?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/health/en/#q-201">Q201 · How do sensor temperatures relate to Composite Temperature?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/health/en/#q-202">Q202 · Which health changes generate asynchronous events?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/health/en/#q-203">Q203 · How is SMART data scope determined?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/health/en/#q-204">Q204 · How are SMART, operations, errors and PEL cross-checked?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/persistent-events/en/#q-205">Q205 · How is PEL and individual event support established?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/persistent-events/en/#q-206">Q206 · How is a PEL context established, read and released?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/persistent-events/en/#q-207">Q207 · What happens for absent or duplicate PEL contexts?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/persistent-events/en/#q-208">Q208 · How are key PEL event classes recorded?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/persistent-events/en/#q-209">Q209 · Which persistent events describe namespace, format and sanitize operations?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/persistent-events/en/#q-210">Q210 · How are events removed when PEL reaches its limits?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/persistent-events/en/#q-211">Q211 · Does a new PEL event require an asynchronous notification?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/persistent-events/en/#q-212">Q212 · What persists in PEL across resets and power cycles?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/persistent-events/en/#q-213">Q213 · How are PEL headers, lengths and ordering validated?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/persistent-events/en/#q-214">Q214 · How is Timestamp set and verified?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/persistent-events/en/#q-215">Q215 · How do Timestamp counting, wrap-around, Origin and SYNC work?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/persistent-events/en/#q-216">Q216 · How are Timestamp changes and reset outcomes interpreted?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/keep-alive/en/#q-217">Q217 · How does a PCIe host discover Keep Alive support?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/keep-alive/en/#q-218">Q218 · How is the timer configured, adjusted and disabled?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/keep-alive/en/#q-219">Q219 · How does the host maintain liveness before expiry?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/keep-alive/en/#q-220">Q220 · What cleanup is required after Keep Alive Timeout?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/keep-alive/en/#q-221">Q221 · Must Keep Alive be reconfigured after reset?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/keep-alive/en/#q-222">Q222 · How do command-based and traffic-based Keep Alive differ?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/memory/en/#q-223">Q223 · What problems do HMB, CMB and PMR solve?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/memory/en/#q-224">Q224 · How are HMB size and descriptor lists configured?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/memory/en/#q-225">Q225 · How are malformed HMB allocations handled?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/memory/en/#q-226">Q226 · How is HMB enabled, disabled and returned after reset?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/memory/en/#q-227">Q227 · What happens if the host prematurely reclaims HMB?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/memory/en/#q-228">Q228 · How are CMB location, size and uses discovered?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/memory/en/#q-229">Q229 · Which queues, buffers and lists may reside in CMB?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/memory/en/#q-230">Q230 · How are out-of-range or unsupported CMB uses handled?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/memory/en/#q-231">Q231 · Do CMB configuration and contents survive reset?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/memory/en/#q-232">Q232 · How is PMR discovered, enabled and made ready?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/memory/en/#q-233">Q233 · What happens for not-ready or unhealthy PMR accesses?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/memory/en/#q-234">Q234 · How is PMR safely disabled?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/memory/en/#q-235">Q235 · How do resets and power cycles affect PMR state and data?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/memory/en/#q-236">Q236 · How do host memory, HMB, CMB and PMR lifetimes compare?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/security/en/#q-237">Q237 · How are Security Send/Receive and protocols discovered?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/security/en/#q-238">Q238 · How are invalid security selectors or lengths handled?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/security/en/#q-239">Q239 · How are security transfer and protocol failures distinguished?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/security/en/#q-240">Q240 · How can security state affect other Admin commands?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/security/en/#q-241">Q241 · Does security state survive reset or power cycle?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/security/en/#q-242">Q242 · How does Lockdown restrict commands or features?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/security/en/#q-243">Q243 · What response is required for a prohibited command or feature?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/security/en/#q-244">Q244 · How are normal and enhanced Lockdown logs interpreted?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/security/en/#q-245">Q245 · Does Lockdown survive resets and power cycles?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/virtualization/en/#q-246">Q246 · How are subsystems, primary and secondary controllers related?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/virtualization/en/#q-247">Q247 · How are private and shared namespaces attached?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/virtualization/en/#q-248">Q248 · How is a namespace’s attached-controller list retrieved?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/virtualization/en/#q-249">Q249 · Can other paths continue during one controller’s reset?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/virtualization/en/#q-250">Q250 · Which controllers are affected by subsystem reset?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/virtualization/en/#q-251">Q251 · How are namespace changes reported through other controllers?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/virtualization/en/#q-252">Q252 · How do asymmetric behavior and ANA guide path selection?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/virtualization/en/#q-253">Q253 · How does a secondary transition Online or Offline?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/virtualization/en/#q-254">Q254 · How are virtualization resources assigned and released?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/virtualization/en/#q-255">Q255 · How are virtualization resources restored after reset and power cycle?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/capacity/en/#q-256">Q256 · How are NVM sets, endurance groups and namespaces related?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/capacity/en/#q-257">Q257 · How are sets and groups discovered through Identify?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/capacity/en/#q-258">Q258 · How is a namespace created in a selected set or group?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/capacity/en/#q-259">Q259 · What happens when a set or group identifier does not exist?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/capacity/en/#q-260">Q260 · What does the Endurance Group Information Log report?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/capacity/en/#q-261">Q261 · How are group health warnings and events updated?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/capacity/en/#q-262">Q262 · How are total and unallocated capacities determined?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/capacity/en/#q-263">Q263 · How do namespace creation and deletion affect free capacity?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/capacity/en/#q-264">Q264 · How does Capacity Management allocate and release groups and sets?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/capacity/en/#q-265">Q265 · What happens when capacity or identifiers are exhausted?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/capacity/en/#q-266">Q266 · Which views change after capacity reconfiguration?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/capacity/en/#q-267">Q267 · How does storage configuration persist across reset and power cycle?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/media/en/#q-268">Q268 · Do domains, sets, groups, media units and namespaces form one hierarchy?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/media/en/#q-269">Q269 · How are domains and resource ownership discovered?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/media/en/#q-270">Q270 · What are a reclaim group, reclaim unit and reclaim-unit handle?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/media/en/#q-271">Q271 · How does a namespace select an RU through a placement handle?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/media/en/#q-272">Q272 · What does Media Unit Status report and how are descriptors traversed?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/media/en/#q-273">Q273 · Can Media Unit Status directly establish namespace unavailability?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/media/en/#q-274">Q274 · Which notices and records can accompany media changes?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/media/en/#q-275">Q275 · How are entity scopes distinguished without confusing identifiers?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/pointers/en/#q-276">Q276 · How does PRP1 describe the first data page?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/pointers/en/#q-277">Q277 · When is PRP2 a second-page address or a list pointer?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/pointers/en/#q-278">Q278 · How are multiple PRP-list pages chained?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/pointers/en/#q-279">Q279 · What alignment rules apply to PRPs and lists?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/pointers/en/#q-280">Q280 · Do zero, invalid or broken-chain PRPs have one universal error?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/pointers/en/#q-281">Q281 · How do SGL data, segment and last-segment descriptors work?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/pointers/en/#q-282">Q282 · How are SGL address, length, count and type errors distinguished?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/pointers/en/#q-283">Q283 · How do Identify SGL capabilities constrain usage?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/pointers/en/#q-284">Q284 · How do pointer-format errors differ from Data Transfer Error?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/pointers/en/#q-285">Q285 · How are pointer errors correlated with completion and Error Information?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/interrupts/en/#q-286">Q286 · How does a CQ select an interrupt vector?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/interrupts/en/#q-287">Q287 · How do shared and dedicated CQ vectors differ?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/interrupts/en/#q-288">Q288 · How do coalescing threshold and time work?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/interrupts/en/#q-289">Q289 · How is interrupt coalescing disabled?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/interrupts/en/#q-290">Q290 · Does FID 09h mask interrupts, and where are actual masks configured?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/interrupts/en/#q-291">Q291 · Can completions be posted while a vector is masked?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/interrupts/en/#q-292">Q292 · How are accumulated completions handled after unmasking?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/interrupts/en/#q-293">Q293 · Can an in-use vector be reconfigured?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/interrupts/en/#q-294">Q294 · How are interrupts restored after reset?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/interrupts/en/#q-295">Q295 · How are interrupt resources reclaimed after queue deletion?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/interrupts/en/#q-296">Q296 · How are interrupt settings, CQ state and completions cross-checked?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/integration/en/#q-297">Q297 · Where do you start when an advertised command fails?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/integration/en/#q-298">Q298 · Does success of an unadvertised command prove compliance?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/integration/en/#q-299">Q299 · How is a successful Set with different readback or behavior investigated?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/integration/en/#q-300">Q300 · Why might an AER completion have no matching visible log information?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/integration/en/#q-301">Q301 · Does every failed CQE require a new error entry?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/integration/en/#q-302">Q302 · When do differing CQE, Error Information and PEL records conflict?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/integration/en/#q-303">Q303 · How are unexpected feature retention or lost saved values assessed?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/integration/en/#q-304">Q304 · How are namespace changes reconciled across Identify, lists and AER?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/integration/en/#q-305">Q305 · How are unchanged firmware revision or slot fields assessed after activation?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/integration/en/#q-306">Q306 · Is an in-progress log after sanitize command success an error?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/integration/en/#q-307">Q307 · How is a missing result after self-test investigated?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/integration/en/#q-308">Q308 · How are unexpected unsafe-shutdown counts assessed?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/integration/en/#q-309">Q309 · Which settings explain a warning change without an AER?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/integration/en/#q-310">Q310 · How is apparent PEL event-order mismatch investigated?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/integration/en/#q-311">Q311 · What evidence remains when CFS is set with little diagnostic information?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/integration/en/#q-312">Q312 · How are two observed completions after Abort classified?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/integration/en/#q-313">Q313 · What is wrong with queue-memory access after completed deletion?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/integration/en/#q-314">Q314 · How should a CQE from before reset be handled?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/integration/en/#q-315">Q315 · When can command success after detach be reasonable?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/integration/en/#q-316">Q316 · How is apparent Lockdown bypass investigated?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/integration/en/#q-317">Q317 · How is excessive power-state recovery latency measured correctly?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/integration/en/#q-318">Q318 · How are three reset types compared for one feature?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/integration/en/#q-319">Q319 · How is an operation’s real scope established?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/integration/en/#q-320">Q320 · How are the interfaces combined into one conformance investigation?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/data-io/en/#q-321">Q321 · Is a Read/Write length valid across MDTS, NLB and namespace bounds?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/data-io/en/#q-322">Q322 · Does successful Write imply power-loss persistence, and what do Flush and FUA guarantee?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/data-io/en/#q-323">Q323 · Why can a small Write lose whole-command atomicity when it crosses a boundary?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/data-io/en/#q-324">Q324 · What do successful Read, Compare and Verify actually prove?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/data-io/en/#q-325">Q325 · Must reads return zero after Write Zeroes or Deallocate?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/data-io/en/#q-326">Q326 · Why did PI checking miss an error? A Type 1, 16-bit Guard example</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/data-io/en/#q-327">Q327 · What does CQE.DW0 establish after a Copy failure?</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/data-io/en/#q-328">Q328 · Does a read failure after Write Uncorrectable prove damaged media?</a></li>
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
