---
layout: post
title: "NVMe Self-Study Bank: Multi-controller and virtualization"
date: 2026-10-02 00:00:00 +0800
categories: [nvme]
permalink: /nvme/question-bank/virtualization/en/
lang: en
nvme_quickref: true
nvme_qa: true
---

<div class="nvme-quickref nvme-qa">
<nav class="qr-top" aria-label="Bank and editions"><a href="#content">Skip to content</a><a href="/nvme/question-bank/en/">Question index</a><a href="/nvme/question-bank/virtualization/zh-tw/">繁體中文</a><a href="/DOCS/nvme-question-bank/virtualization.html">Chinese tutorial HTML</a></nav>
<main id="content"><p class="qr-eyebrow">BASE 2.4 / NVM 1.3 / PCIe 1.4 · Q1–328</p>
<header><p class="qa-range">Q246–Q255</p><h1>Multi-controller and virtualization</h1><p class="qr-intro">Separate multipath, shared storage and virtualization before combining topology, attachment, ANA and resources.</p><p>Practice first, then reveal 17 answer items per question. All numerical examples are hypothetical. Status is written SCT/SC; h indicates hexadecimal.</p></header>
<aside class="qa-glossary"><h2>Terms used in this volume</h2><dl><dt>Controller / namespace</dt><dd>A controller receives commands and manages access. A namespace is a logical storage space that commands can address. An NVM subsystem contains controllers and nonvolatile storage resources.</dd><dt>SQ / CQ / SQE / CQE</dt><dd>Submission and Completion Queues carry command entries (SQEs) and completion entries (CQEs). QID identifies a queue, CID distinguishes outstanding commands in one SQ, and NSID identifies a namespace.</dd><dt>Register / Identify / Feature / Log</dt><dd>A register exposes control or state. Identify queries capabilities and attributes; features query or configure operation; log pages report specific state or records. FID, LID, CNS and CSI select features, logs, Identify structures and command sets.</dd><dt>index / offset / zero-based</dt><dd>An index selects an entry, usually starting at 0; an offset measures distance from an origin in specified units. A zero-based count encodes count−1, but not every zero-valued field is a count. A Dword is 4 bytes; a byte is 8 bits.</dd><dt>Scope / reset / retention</dt><dd>Scope names the affected objects; retention means preserving state. Controller Reset (clearing CC.EN) is one form of Controller Level Reset, or CLR. Different CLR triggers can retain different registers.</dd></dl></aside>
<section id="overview" class="qa-overview"><h2>Three state dimensions on one topology</h2><p class="qa-takeaway">Online, enabled and namespace-accessible are different.</p>
<div class="qr-table" tabindex="0" role="region" aria-label="Horizontally scrollable comparison table"><table><thead><tr><th scope="col">State</th><th scope="col">Discovery</th><th scope="col">Interpretation</th></tr></thead><tbody><tr><td>Role</td><td>Primary/secondary structures</td><td>Resource-management authority</td></tr><tr><td>Online status</td><td>State and resource counts</td><td>Online prerequisites</td></tr><tr><td>Interface</td><td>CC/CSTS</td><td>Enabled/readiness</td></tr><tr><td>Namespace path</td><td>Active inventory and ANA</td><td>Current path availability</td></tr></tbody></table></div>
<p><strong>Worked interpretation: </strong>Online does not set RDY1; host initialization and enable remain necessary.</p>
<p class="qa-citations">Sources: <a href="#ref-multipath">Base 2.4 §2.4.1–2.4.2 (PCIe topology)</a> · <a href="#ref-virtual">Base 2.4 §8.2.7</a> · <a href="#ref-virtualcmd">Base 2.4 §5.3.6</a> · <a href="#ref-virtualid">Base 2.4 §5.2.14.3.1–5.2.14.3.2 (Primary Capabilities, Secondary List)</a> · <a href="#ref-ana">Base 2.4 §2.4.2, 8.1.1 (PCIe namespace access)</a> · <a href="#ref-analog">Base 2.4 §5.2.13.1.13</a></p>
</section>
<div class="qa-controls" hidden><label>Search this page <input type="search" id="qa-search" placeholder="Question number, field or keyword"></label><button type="button" data-expand="true">Expand all answers</button><button type="button" data-expand="false">Collapse all answers</button><output id="qa-count" aria-live="polite"></output></div>
<section id="question-index"><h2>Questions in this volume</h2><ol class="qa-index">
<li><a href="#q-246">Q246 · How are subsystems, primary and secondary controllers related?</a></li>
<li><a href="#q-247">Q247 · How are private and shared namespaces attached?</a></li>
<li><a href="#q-248">Q248 · How is a namespace’s attached-controller list retrieved?</a></li>
<li><a href="#q-249">Q249 · Can other paths continue during one controller’s reset?</a></li>
<li><a href="#q-250">Q250 · Which controllers are affected by subsystem reset?</a></li>
<li><a href="#q-251">Q251 · How are namespace changes reported through other controllers?</a></li>
<li><a href="#q-252">Q252 · How do asymmetric behavior and ANA guide path selection?</a></li>
<li><a href="#q-253">Q253 · How does a secondary transition Online or Offline?</a></li>
<li><a href="#q-254">Q254 · How are virtualization resources assigned and released?</a></li>
<li><a href="#q-255">Q255 · How are virtualization resources restored after reset and power cycle?</a></li>
</ol></section>
<article class="qa-question" id="q-246" data-question="246"><h2><a class="qa-qid" href="#q-246">Q246</a> How are subsystems, primary and secondary controllers related?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-246-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-246-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Controllers are command endpoints, namespaces storage objects; virtualization lets a primary allocate queue/interrupt resources.</p>
</li>
<li id="q-246-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>A subsystem can contain multiple primary groups, with each secondary in its primary’s domain.</p>
</li>
<li id="q-246-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Discover VMS and the primary/secondary structures rather than inferring parentage from function numbers.</p>
</li>
<li id="q-246-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>VQ manages an SQ/CQ pair, VI a vector; private resources are fixed and flexible resources reallocatable.</p>
</li>
<li id="q-246-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Map parentage, resources and attachment before creating queues.</p>
</li>
<li id="q-246-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>An enabled Online secondary remains a compliant NVMe controller.</p>
</li>
<li id="q-246-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Resource management requires support and the associated primary endpoint.</p>
</li>
<li id="q-246-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-246-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Resource allocation and Online/Offline do not define a universal success AER; qualifying namespace or ANA changes follow their own rules. <a class="qa-rule-link" href="#common-virtual_op-9">Full rule in this volume</a></p>
</li>
<li id="q-246-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Verify resource state through capability/list structures and path state through namespace/ANA data; allocation changes are not themselves error entries. <a class="qa-rule-link" href="#common-virtual_op-10">Full rule in this volume</a></p>
</li>
<li id="q-246-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>Virtualization Management has no dedicated PEL event; actual resets or qualifying namespace operations follow their events, not every Assign. <a class="qa-rule-link" href="#common-virtual_op-11">Full rule in this volume</a></p>
</li>
<li id="q-246-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Primary disable/CLR/shutdown takes secondaries Offline, removing their flexible resources on the transition. <a class="qa-rule-link" href="#common-virtual_op-12">Full rule in this volume</a></p>
</li>
<li id="q-246-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Rebuild affected primary/secondary operation after subsystem reset; persistent primary allocation does not preserve Online state or queues. <a class="qa-rule-link" href="#common-virtual_op-13">Full rule in this volume</a></p>
</li>
<li id="q-246-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Primary flexible allocation persists across power cycles; rediscover/reconfigure secondary resources and state. <a class="qa-rule-link" href="#common-virtual_op-14">Full rule in this volume</a></p>
</li>
<li id="q-246-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>A primary manages its own secondaries/pool; one resource cannot belong to two controllers simultaneously. <a class="qa-rule-link" href="#common-virtual_op-15">Full rule in this volume</a></p>
</li>
<li id="q-246-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>PF/VF map to primary/secondary when both are supported; not all multi-controller devices implement SR-IOV.</p>
</li>
<li id="q-246-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First establish topology and capability before management authority.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-multipath">Base 2.4 §2.4.1–2.4.2 (PCIe topology)</a> · <a href="#ref-virtual">Base 2.4 §8.2.7</a> · <a href="#ref-virtualcmd">Base 2.4 §5.3.6</a> · <a href="#ref-virtualid">Base 2.4 §5.2.14.3.1–5.2.14.3.2 (Primary Capabilities, Secondary List)</a> · <a href="#ref-nsattach">Base 2.4 §5.2.24–5.2.25, 8.1.17–8.1.17.2</a> · <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-247" data-question="247"><h2><a class="qa-qid" href="#q-247">Q247</a> How are private and shared namespaces attached?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-247-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-247-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Attachment creates access paths, not copies; private/shared determines simultaneous attachments.</p>
</li>
<li id="q-247-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Private permits one attached controller at a time; shared permits several subject to constraints.</p>
</li>
<li id="q-247-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Inspect NMIC, controller capabilities and attachment list.</p>
</li>
<li id="q-247-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>Attachment uses target NSID, Attach/Detach selector and controller-ID list.</p>
</li>
<li id="q-247-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Confirm allocation/sharing, attach and verify active lists per controller.</p>
</li>
<li id="q-247-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Shared paths see the same data; a private namespace cannot acquire a second simultaneous attachment.</p>
</li>
<li id="q-247-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>A private namespace attached elsewhere differs from an already-attached target.</p>
</li>
<li id="q-247-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-247-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Create/delete affect allocated inventory; attach/detach affect controller active lists. <a class="qa-rule-link" href="#common-namespace_op-9">Full rule in this volume</a></p>
</li>
<li id="q-247-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Identify lists establish current allocation/attachment; changed lists 04h/1Ch identify changes rather than complete state. <a class="qa-rule-link" href="#common-namespace_op-10">Full rule in this volume</a></p>
</li>
<li id="q-247-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>Supported Change Namespace 06h records defined management changes; do not treat attachment as creation/deletion. <a class="qa-rule-link" href="#common-namespace_op-11">Full rule in this volume</a></p>
</li>
<li id="q-247-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Completed configuration/attachment survives reset; command channels reset without deleting namespaces. <a class="qa-rule-link" href="#common-namespace_op-12">Full rule in this volume</a></p>
</li>
<li id="q-247-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Subsystem reset is not Restore Default Namespace Configuration. <a class="qa-rule-link" href="#common-namespace_op-13">Full rule in this volume</a></p>
</li>
<li id="q-247-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Completed namespace configuration/attachments persist. <a class="qa-rule-link" href="#common-namespace_op-14">Full rule in this volume</a></p>
</li>
<li id="q-247-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Creation/deletion changes inventory and attachment lists select affected controllers. <a class="qa-rule-link" href="#common-namespace_op-15">Full rule in this volume</a></p>
</li>
<li id="q-247-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Cross-check per-controller active lists against the namespace controller list.</p>
</li>
<li id="q-247-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First distinguish existence from attachment.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-multipath">Base 2.4 §2.4.1–2.4.2 (PCIe topology)</a> · <a href="#ref-virtual">Base 2.4 §8.2.7</a> · <a href="#ref-virtualcmd">Base 2.4 §5.3.6</a> · <a href="#ref-virtualid">Base 2.4 §5.2.14.3.1–5.2.14.3.2 (Primary Capabilities, Secondary List)</a> · <a href="#ref-nsattach">Base 2.4 §5.2.24–5.2.25, 8.1.17–8.1.17.2</a> · <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-248" data-question="248"><h2><a class="qa-qid" href="#q-248">Q248</a> How is a namespace’s attached-controller list retrieved?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-248-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-248-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>It lists attachment endpoints, not every controller in the subsystem.</p>
</li>
<li id="q-248-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Scope is the selected namespace; unattached controllers are not access paths.</p>
</li>
<li id="q-248-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Select Attached Controller List with the proper CNS, NSID and starting controller identifier.</p>
</li>
<li id="q-248-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>Parse count/IDs and obey the inclusive starting-controller rule, not a different namespace-list pagination rule.</p>
</li>
<li id="q-248-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Read successive pages using the next ID after the last entry, considering concurrent changes.</p>
</li>
<li id="q-248-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Attachment discovery precedes Online/Ready/ANA availability checks.</p>
</li>
<li id="q-248-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Invalid selectors follow Identify rules; an empty attachment list does not prove deletion.</p>
</li>
<li id="q-248-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-248-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Resource allocation and Online/Offline do not define a universal success AER; qualifying namespace or ANA changes follow their own rules. <a class="qa-rule-link" href="#common-virtual_op-9">Full rule in this volume</a></p>
</li>
<li id="q-248-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Verify resource state through capability/list structures and path state through namespace/ANA data; allocation changes are not themselves error entries. <a class="qa-rule-link" href="#common-virtual_op-10">Full rule in this volume</a></p>
</li>
<li id="q-248-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>Virtualization Management has no dedicated PEL event; actual resets or qualifying namespace operations follow their events, not every Assign. <a class="qa-rule-link" href="#common-virtual_op-11">Full rule in this volume</a></p>
</li>
<li id="q-248-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Repeat an interrupted query and distinguish identity, configuration and dynamic fields. <a class="qa-rule-link" href="#common-identify-12">Full rule in this volume</a></p>
</li>
<li id="q-248-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Rediscover affected objects; reset alone does not mean namespace deletion or factory configuration. <a class="qa-rule-link" href="#common-identify-13">Full rule in this volume</a></p>
</li>
<li id="q-248-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Re-read and compare, separating firmware activation or management changes from power cycling alone. <a class="qa-rule-link" href="#common-identify-14">Full rule in this volume</a></p>
</li>
<li id="q-248-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Identify is read-only; active lists may differ by controller, so compare matching query targets. <a class="qa-rule-link" href="#common-identify-15">Full rule in this volume</a></p>
</li>
<li id="q-248-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Cross-check per-controller active lists at consistent times.</p>
</li>
<li id="q-248-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First check which controller-list selection was used.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-multipath">Base 2.4 §2.4.1–2.4.2 (PCIe topology)</a> · <a href="#ref-virtual">Base 2.4 §8.2.7</a> · <a href="#ref-virtualcmd">Base 2.4 §5.3.6</a> · <a href="#ref-virtualid">Base 2.4 §5.2.14.3.1–5.2.14.3.2 (Primary Capabilities, Secondary List)</a> · <a href="#ref-nsattach">Base 2.4 §5.2.24–5.2.25, 8.1.17–8.1.17.2</a> · <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-249" data-question="249"><h2><a class="qa-qid" href="#q-249">Q249</a> Can other paths continue during one controller’s reset?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-249-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-249-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Shared namespaces provide paths, not immunity to every shared failure.</p>
</li>
<li id="q-249-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>CLR usually targets one controller, but primary resets offline secondaries and shared media/domain faults can broaden impact.</p>
</li>
<li id="q-249-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Check parentage, domain, attachment, ANA and readiness of alternate paths.</p>
</li>
<li id="q-249-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>Independent queues can remain valid while namespace/ANA/access restrictions still govern I/O.</p>
</li>
<li id="q-249-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Quiesce the failed path, establish an alternative and resolve old/new command dependencies.</p>
</li>
<li id="q-249-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>A healthy alternative can access the same data without creating another namespace.</p>
</li>
<li id="q-249-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Successful failover does not prove old Writes unexecuted; retries may overlap effects.</p>
</li>
<li id="q-249-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-249-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Create/delete affect allocated inventory; attach/detach affect controller active lists. <a class="qa-rule-link" href="#common-namespace_op-9">Full rule in this volume</a></p>
</li>
<li id="q-249-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Identify lists establish current allocation/attachment; changed lists 04h/1Ch identify changes rather than complete state. <a class="qa-rule-link" href="#common-namespace_op-10">Full rule in this volume</a></p>
</li>
<li id="q-249-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>Supported Change Namespace 06h records defined management changes; do not treat attachment as creation/deletion. <a class="qa-rule-link" href="#common-namespace_op-11">Full rule in this volume</a></p>
</li>
<li id="q-249-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Completed configuration/attachment survives reset; command channels reset without deleting namespaces. <a class="qa-rule-link" href="#common-namespace_op-12">Full rule in this volume</a></p>
</li>
<li id="q-249-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Subsystem reset is not Restore Default Namespace Configuration. <a class="qa-rule-link" href="#common-namespace_op-13">Full rule in this volume</a></p>
</li>
<li id="q-249-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Completed namespace configuration/attachments persist. <a class="qa-rule-link" href="#common-namespace_op-14">Full rule in this volume</a></p>
</li>
<li id="q-249-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Creation/deletion changes inventory and attachment lists select affected controllers. <a class="qa-rule-link" href="#common-namespace_op-15">Full rule in this volume</a></p>
</li>
<li id="q-249-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Use topology and outcomes rather than assuming universal reset isolation.</p>
</li>
<li id="q-249-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First check whether the reset controller is the alternate path’s parent.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-ana">Base 2.4 §2.4.2, 8.1.1 (PCIe namespace access)</a> · <a href="#ref-multipath">Base 2.4 §2.4.1–2.4.2 (PCIe topology)</a> · <a href="#ref-virtual">Base 2.4 §8.2.7</a> · <a href="#ref-virtualcmd">Base 2.4 §5.3.6</a> · <a href="#ref-virtualid">Base 2.4 §5.2.14.3.1–5.2.14.3.2 (Primary Capabilities, Secondary List)</a> · <a href="#ref-nsattach">Base 2.4 §5.2.24–5.2.25, 8.1.17–8.1.17.2</a> · <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-250" data-question="250"><h2><a class="qa-qid" href="#q-250">Q250</a> Which controllers are affected by subsystem reset?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-250-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-250-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Multi-domain implementations may reset one domain despite the subsystem-reset name.</p>
</li>
<li id="q-250-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Single-domain scope is all; multi-domain scope is one or all domains as implemented.</p>
</li>
<li id="q-250-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Inspect topology, host-reset capability and NSSRO evidence.</p>
</li>
<li id="q-250-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>Supported NSSR triggers reset; affected controllers undergo CLR and their PMRs are disabled.</p>
</li>
<li id="q-250-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Quiesce the intended scope, reset and restore each affected path.</p>
</li>
<li id="q-250-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Rebuild affected queues; outside paths depend on their own/shared-resource health.</p>
</li>
<li id="q-250-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Register-triggered reset has no CQE or DNR/More.</p>
</li>
<li id="q-250-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>NSSR writes have no CQE/DNR/More; post-recovery query CQEs belong to those queries.</p>
</li>
<li id="q-250-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Resource allocation and Online/Offline do not define a universal success AER; qualifying namespace or ANA changes follow their own rules. <a class="qa-rule-link" href="#common-virtual_op-9">Full rule in this volume</a></p>
</li>
<li id="q-250-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Verify resource state through capability/list structures and path state through namespace/ANA data; allocation changes are not themselves error entries. <a class="qa-rule-link" href="#common-virtual_op-10">Full rule in this volume</a></p>
</li>
<li id="q-250-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>Virtualization Management has no dedicated PEL event; actual resets or qualifying namespace operations follow their events, not every Assign. <a class="qa-rule-link" href="#common-virtual_op-11">Full rule in this volume</a></p>
</li>
<li id="q-250-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Primary disable/CLR/shutdown takes secondaries Offline, removing their flexible resources on the transition. <a class="qa-rule-link" href="#common-virtual_op-12">Full rule in this volume</a></p>
</li>
<li id="q-250-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Rebuild affected primary/secondary operation after subsystem reset; persistent primary allocation does not preserve Online state or queues. <a class="qa-rule-link" href="#common-virtual_op-13">Full rule in this volume</a></p>
</li>
<li id="q-250-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Primary flexible allocation persists across power cycles; rediscover/reconfigure secondary resources and state. <a class="qa-rule-link" href="#common-virtual_op-14">Full rule in this volume</a></p>
</li>
<li id="q-250-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>A primary manages its own secondaries/pool; one resource cannot belong to two controllers simultaneously. <a class="qa-rule-link" href="#common-virtual_op-15">Full rule in this volume</a></p>
</li>
<li id="q-250-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Compare all affected controllers with domain configuration.</p>
</li>
<li id="q-250-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First establish actual domain reset scope.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-multipath">Base 2.4 §2.4.1–2.4.2 (PCIe topology)</a> · <a href="#ref-virtual">Base 2.4 §8.2.7</a> · <a href="#ref-virtualcmd">Base 2.4 §5.3.6</a> · <a href="#ref-virtualid">Base 2.4 §5.2.14.3.1–5.2.14.3.2 (Primary Capabilities, Secondary List)</a> · <a href="#ref-nsattach">Base 2.4 §5.2.24–5.2.25, 8.1.17–8.1.17.2</a> · <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-251" data-question="251"><h2><a class="qa-qid" href="#q-251">Q251</a> How are namespace changes reported through other controllers?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-251-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-251-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Management on one path can require rediscovery by hosts using other paths.</p>
</li>
<li id="q-251-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Notification follows affected attachment/views rather than unconditional broadcast.</p>
</li>
<li id="q-251-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Check NAN, AERs, changed/active lists and separate ANA notice configuration.</p>
</li>
<li id="q-251-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>The notice prompts rediscovery; changed IDs narrow it, while FFFFFFFFh requires broad rediscovery.</p>
</li>
<li id="q-251-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Process notice, read changes and refresh Identify with acknowledgment/masking accounted for.</p>
</li>
<li id="q-251-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Affected views converge with configuration without requiring unlimited one-event-per-change history.</p>
</li>
<li id="q-251-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>The processing controller has a specific Admin Delete notice exclusion.</p>
</li>
<li id="q-251-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-251-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Create/delete affect allocated inventory; attach/detach affect controller active lists. <a class="qa-rule-link" href="#common-namespace_op-9">Full rule in this volume</a></p>
</li>
<li id="q-251-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Identify lists establish current allocation/attachment; changed lists 04h/1Ch identify changes rather than complete state. <a class="qa-rule-link" href="#common-namespace_op-10">Full rule in this volume</a></p>
</li>
<li id="q-251-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>Supported Change Namespace 06h records defined management changes; do not treat attachment as creation/deletion. <a class="qa-rule-link" href="#common-namespace_op-11">Full rule in this volume</a></p>
</li>
<li id="q-251-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Completed configuration/attachment survives reset; command channels reset without deleting namespaces. <a class="qa-rule-link" href="#common-namespace_op-12">Full rule in this volume</a></p>
</li>
<li id="q-251-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Subsystem reset is not Restore Default Namespace Configuration. <a class="qa-rule-link" href="#common-namespace_op-13">Full rule in this volume</a></p>
</li>
<li id="q-251-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Completed namespace configuration/attachments persist. <a class="qa-rule-link" href="#common-namespace_op-14">Full rule in this volume</a></p>
</li>
<li id="q-251-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Creation/deletion changes inventory and attachment lists select affected controllers. <a class="qa-rule-link" href="#common-namespace_op-15">Full rule in this volume</a></p>
</li>
<li id="q-251-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Namespace and ANA notices describe different changes and logs.</p>
</li>
<li id="q-251-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First check applicability and existing event masking.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-changedlog">Base 2.4 §5.2.13.1.5</a> · <a href="#ref-aerfull">Base 2.4 §5.2.2 (PCIe-applicable events)</a> · <a href="#ref-analog">Base 2.4 §5.2.13.1.13</a> · <a href="#ref-multipath">Base 2.4 §2.4.1–2.4.2 (PCIe topology)</a> · <a href="#ref-virtual">Base 2.4 §8.2.7</a> · <a href="#ref-virtualcmd">Base 2.4 §5.3.6</a> · <a href="#ref-virtualid">Base 2.4 §5.2.14.3.1–5.2.14.3.2 (Primary Capabilities, Secondary List)</a> · <a href="#ref-nsattach">Base 2.4 §5.2.24–5.2.25, 8.1.17–8.1.17.2</a> · <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-252" data-question="252"><h2><a class="qa-qid" href="#q-252">Q252</a> How do asymmetric behavior and ANA guide path selection?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-252-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-252-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Access characteristics can differ across controllers, including PCIe paths.</p>
</li>
<li id="q-252-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>ANA state describes a controller-to-group relationship, not one global namespace state.</p>
</li>
<li id="q-252-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Inspect ANA capability, transition time, group membership and LID 0Ch.</p>
</li>
<li id="q-252-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>Optimized/non-optimized support normal commands; inaccessible, persistent loss and change impose distinct restrictions.</p>
</li>
<li id="q-252-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Select accessible paths, prefer optimized access and refresh after notices.</p>
</li>
<li id="q-252-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Non-optimized is usable, and another path may report a different state for the same group.</p>
</li>
<li id="q-252-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Restricted states use their corresponding asymmetric-access status for nonexempt commands, not every Admin command.</p>
</li>
<li id="q-252-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-252-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Resource allocation and Online/Offline do not define a universal success AER; qualifying namespace or ANA changes follow their own rules. <a class="qa-rule-link" href="#common-virtual_op-9">Full rule in this volume</a></p>
</li>
<li id="q-252-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Verify resource state through capability/list structures and path state through namespace/ANA data; allocation changes are not themselves error entries. <a class="qa-rule-link" href="#common-virtual_op-10">Full rule in this volume</a></p>
</li>
<li id="q-252-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>Virtualization Management has no dedicated PEL event; actual resets or qualifying namespace operations follow their events, not every Assign. <a class="qa-rule-link" href="#common-virtual_op-11">Full rule in this volume</a></p>
</li>
<li id="q-252-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Repeat an interrupted query and distinguish identity, configuration and dynamic fields. <a class="qa-rule-link" href="#common-identify-12">Full rule in this volume</a></p>
</li>
<li id="q-252-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Rediscover affected objects; reset alone does not mean namespace deletion or factory configuration. <a class="qa-rule-link" href="#common-identify-13">Full rule in this volume</a></p>
</li>
<li id="q-252-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Re-read and compare, separating firmware activation or management changes from power cycling alone. <a class="qa-rule-link" href="#common-identify-14">Full rule in this volume</a></p>
</li>
<li id="q-252-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Identify is read-only; active lists may differ by controller, so compare matching query targets. <a class="qa-rule-link" href="#common-identify-15">Full rule in this volume</a></p>
</li>
<li id="q-252-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Different performance does not prove ANA reporting support; check capability first.</p>
</li>
<li id="q-252-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First match group state to the actual controller path.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-ana">Base 2.4 §2.4.2, 8.1.1 (PCIe namespace access)</a> · <a href="#ref-analog">Base 2.4 §5.2.13.1.13</a> · <a href="#ref-multipath">Base 2.4 §2.4.1–2.4.2 (PCIe topology)</a> · <a href="#ref-virtual">Base 2.4 §8.2.7</a> · <a href="#ref-virtualcmd">Base 2.4 §5.3.6</a> · <a href="#ref-virtualid">Base 2.4 §5.2.14.3.1–5.2.14.3.2 (Primary Capabilities, Secondary List)</a> · <a href="#ref-nsattach">Base 2.4 §5.2.24–5.2.25, 8.1.17–8.1.17.2</a> · <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-253" data-question="253"><h2><a class="qa-qid" href="#q-253">Q253</a> How does a secondary transition Online or Offline?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-253-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-253-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Online permits use but is not the same as enabled/ready.</p>
</li>
<li id="q-253-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>The associated primary manages it; Offline sets CFS and leaves other properties undefined.</p>
</li>
<li id="q-253-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Inspect secondary state/resource counts and primary enablement.</p>
</li>
<li id="q-253-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>ACT7 offlines,8 assigns and 9 onlines; offlining removes flexible resources.</p>
</li>
<li id="q-253-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Recommended sequence: Offline, assign, CLR (prefer VF FLR for a VF), Online, then enable and initialize queues.</p>
</li>
<li id="q-253-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>With flexible VQ support, at least two resources are needed; with VI support, vector 0 must be assigned.</p>
</li>
<li id="q-253-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Wrong state or insufficient Online prerequisites cause Invalid Secondary Controller State; repeated same-state requests are allowed.</p>
</li>
<li id="q-253-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-253-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Resource allocation and Online/Offline do not define a universal success AER; qualifying namespace or ANA changes follow their own rules. <a class="qa-rule-link" href="#common-virtual_op-9">Full rule in this volume</a></p>
</li>
<li id="q-253-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Verify resource state through capability/list structures and path state through namespace/ANA data; allocation changes are not themselves error entries. <a class="qa-rule-link" href="#common-virtual_op-10">Full rule in this volume</a></p>
</li>
<li id="q-253-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>Virtualization Management has no dedicated PEL event; actual resets or qualifying namespace operations follow their events, not every Assign. <a class="qa-rule-link" href="#common-virtual_op-11">Full rule in this volume</a></p>
</li>
<li id="q-253-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Primary disable/CLR/shutdown takes secondaries Offline, removing their flexible resources on the transition. <a class="qa-rule-link" href="#common-virtual_op-12">Full rule in this volume</a></p>
</li>
<li id="q-253-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Rebuild affected primary/secondary operation after subsystem reset; persistent primary allocation does not preserve Online state or queues. <a class="qa-rule-link" href="#common-virtual_op-13">Full rule in this volume</a></p>
</li>
<li id="q-253-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Primary flexible allocation persists across power cycles; rediscover/reconfigure secondary resources and state. <a class="qa-rule-link" href="#common-virtual_op-14">Full rule in this volume</a></p>
</li>
<li id="q-253-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>A primary manages its own secondaries/pool; one resource cannot belong to two controllers simultaneously. <a class="qa-rule-link" href="#common-virtual_op-15">Full rule in this volume</a></p>
</li>
<li id="q-253-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Validate Online and Enable separately; expected Offline CFS is not unexplained hardware failure.</p>
</li>
<li id="q-253-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First establish prerequisites before diagnosing enable timeout.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-multipath">Base 2.4 §2.4.1–2.4.2 (PCIe topology)</a> · <a href="#ref-virtual">Base 2.4 §8.2.7</a> · <a href="#ref-virtualcmd">Base 2.4 §5.3.6</a> · <a href="#ref-virtualid">Base 2.4 §5.2.14.3.1–5.2.14.3.2 (Primary Capabilities, Secondary List)</a> · <a href="#ref-nsattach">Base 2.4 §5.2.24–5.2.25, 8.1.17–8.1.17.2</a> · <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-254" data-question="254"><h2><a class="qa-qid" href="#q-254">Q254</a> How are virtualization resources assigned and released?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-254-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-254-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Flexible allocation redistributes a finite pool rather than creating resources.</p>
</li>
<li id="q-254-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>VQ and VI are separate pools; private resources cannot be reassigned.</p>
</li>
<li id="q-254-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Read resource types, totals, assignments, per-secondary maxima and granularity.</p>
</li>
<li id="q-254-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>CNTLID/RT/ACT select target/type/action, NR requests a count and NRM reports the modified count.</p>
</li>
<li id="q-254-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Assign only while Offline; offlining removes secondary resources. Primary allocation changes need the specified later reset.</p>
</li>
<li id="q-254-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>NRM may be smaller or larger than NR; verify actual allocation.</p>
</li>
<li id="q-254-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Invalid total/per-controller count differs from invalid/private/in-use resource ranges.</p>
</li>
<li id="q-254-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-254-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Resource allocation and Online/Offline do not define a universal success AER; qualifying namespace or ANA changes follow their own rules. <a class="qa-rule-link" href="#common-virtual_op-9">Full rule in this volume</a></p>
</li>
<li id="q-254-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Verify resource state through capability/list structures and path state through namespace/ANA data; allocation changes are not themselves error entries. <a class="qa-rule-link" href="#common-virtual_op-10">Full rule in this volume</a></p>
</li>
<li id="q-254-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>Virtualization Management has no dedicated PEL event; actual resets or qualifying namespace operations follow their events, not every Assign. <a class="qa-rule-link" href="#common-virtual_op-11">Full rule in this volume</a></p>
</li>
<li id="q-254-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Primary disable/CLR/shutdown takes secondaries Offline, removing their flexible resources on the transition. <a class="qa-rule-link" href="#common-virtual_op-12">Full rule in this volume</a></p>
</li>
<li id="q-254-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Rebuild affected primary/secondary operation after subsystem reset; persistent primary allocation does not preserve Online state or queues. <a class="qa-rule-link" href="#common-virtual_op-13">Full rule in this volume</a></p>
</li>
<li id="q-254-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Primary flexible allocation persists across power cycles; rediscover/reconfigure secondary resources and state. <a class="qa-rule-link" href="#common-virtual_op-14">Full rule in this volume</a></p>
</li>
<li id="q-254-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>A primary manages its own secondaries/pool; one resource cannot belong to two controllers simultaneously. <a class="qa-rule-link" href="#common-virtual_op-15">Full rule in this volume</a></p>
</li>
<li id="q-254-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Reconcile pool ownership and distinguish preferred granularity from mandatory rejection.</p>
</li>
<li id="q-254-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First check NRM and readback rather than requested NR.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-multipath">Base 2.4 §2.4.1–2.4.2 (PCIe topology)</a> · <a href="#ref-virtual">Base 2.4 §8.2.7</a> · <a href="#ref-virtualcmd">Base 2.4 §5.3.6</a> · <a href="#ref-virtualid">Base 2.4 §5.2.14.3.1–5.2.14.3.2 (Primary Capabilities, Secondary List)</a> · <a href="#ref-nsattach">Base 2.4 §5.2.24–5.2.25, 8.1.17–8.1.17.2</a> · <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-255" data-question="255"><h2><a class="qa-qid" href="#q-255">Q255</a> How are virtualization resources restored after reset and power cycle?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-255-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-255-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Primary persistent allocation and secondary live assignment have different lifetimes.</p>
</li>
<li id="q-255-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Include dependent secondaries, not only the reset controller.</p>
</li>
<li id="q-255-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Snapshot capabilities, secondary list, reset source and function relationships.</p>
</li>
<li id="q-255-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>Primary allocation is persistent and new values take effect after CLR other than CC.EN Controller Reset.</p>
</li>
<li id="q-255-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>After primary recovery, rediscover and rebuild secondary operation through the required sequence.</p>
</li>
<li id="q-255-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Persistent allocation and freshly established secondary resources/queues are validated separately.</p>
</li>
<li id="q-255-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Retained primary allocation does not preserve secondary queues or Online state.</p>
</li>
<li id="q-255-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-255-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Resource allocation and Online/Offline do not define a universal success AER; qualifying namespace or ANA changes follow their own rules. <a class="qa-rule-link" href="#common-virtual_op-9">Full rule in this volume</a></p>
</li>
<li id="q-255-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Verify resource state through capability/list structures and path state through namespace/ANA data; allocation changes are not themselves error entries. <a class="qa-rule-link" href="#common-virtual_op-10">Full rule in this volume</a></p>
</li>
<li id="q-255-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>Virtualization Management has no dedicated PEL event; actual resets or qualifying namespace operations follow their events, not every Assign. <a class="qa-rule-link" href="#common-virtual_op-11">Full rule in this volume</a></p>
</li>
<li id="q-255-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Primary disable/CLR/shutdown takes secondaries Offline, removing their flexible resources on the transition. <a class="qa-rule-link" href="#common-virtual_op-12">Full rule in this volume</a></p>
</li>
<li id="q-255-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Rebuild affected primary/secondary operation after subsystem reset; persistent primary allocation does not preserve Online state or queues. <a class="qa-rule-link" href="#common-virtual_op-13">Full rule in this volume</a></p>
</li>
<li id="q-255-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Primary flexible allocation persists across power cycles; rediscover/reconfigure secondary resources and state. <a class="qa-rule-link" href="#common-virtual_op-14">Full rule in this volume</a></p>
</li>
<li id="q-255-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>A primary manages its own secondaries/pool; one resource cannot belong to two controllers simultaneously. <a class="qa-rule-link" href="#common-virtual_op-15">Full rule in this volume</a></p>
</li>
<li id="q-255-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Persistent attachment can remain while secondary is Offline; do not recreate the namespace merely for that reason.</p>
</li>
<li id="q-255-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First check the primary-reset cascade into secondary Offline/resource removal.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-multipath">Base 2.4 §2.4.1–2.4.2 (PCIe topology)</a> · <a href="#ref-virtual">Base 2.4 §8.2.7</a> · <a href="#ref-virtualcmd">Base 2.4 §5.3.6</a> · <a href="#ref-virtualid">Base 2.4 §5.2.14.3.1–5.2.14.3.2 (Primary Capabilities, Secondary List)</a> · <a href="#ref-nsattach">Base 2.4 §5.2.24–5.2.25, 8.1.17–8.1.17.2</a> · <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<section id="common-rules" class="qa-common"><h2>Shared rules linked from the answers</h2><p>Each shared mechanism is explained in full once in this volume. Use browser Back to return to the question; explicit command or feature exceptions take precedence.</p>
<article id="common-command-8"><h3>Command completion, events and records · How are DNR and More set?</h3><p>For a CQE, DNR=1 means the identical command is expected to fail if resubmitted to any controller in this subsystem; DNR=0 means it may succeed. Do not assign DNR=1 solely from an error name unless that condition mandates it. More=1 identifies additional information for this command in the Error Information Log. DNR should be zero when SCT=SC=0.</p></article>
<article id="common-identify-12"><h3>Query reset and scope · What survives or continues after Controller Reset?</h3><p>Controller Reset stops an outstanding query; a missing response is not an all-zero result. Re-read after recovery, distinguishing identity, configuration and dynamic state by field. Reset alone does not mean the namespace was deleted.</p></article>
<article id="common-identify-13"><h3>Query reset and scope · What survives or continues after NVM Subsystem Reset?</h3><p>Rediscover affected controllers and namespaces after reset. An NVM Subsystem Reset does not by itself imply that all storage configuration returns to manufacturing defaults. Verify changes caused by any separate management operation.</p></article>
<article id="common-identify-14"><h3>Query reset and scope · What survives or continues after a power cycle?</h3><p>After a power cycle, re-read version, capabilities, current format and attachment lists. Stable identity and persistent configuration are not ordinary volatile feature values. Firmware activation or configuration changes require before/after snapshots and event timing.</p></article>
<article id="common-identify-15"><h3>Query reset and scope · Are other controllers or namespaces affected?</h3><p>Identify reads data; it does not create, format or attach a namespace. CNS and selectors determine the view. Active lists may differ across controllers, so different lists do not alone establish corruption.</p></article>
<article id="common-namespace_op-9"><h3>Shared conditions for this topic · Is an asynchronous event generated?</h3><p>Create/delete affect allocated inventory; attach/detach affect controller active lists. Apply per-controller support/AEC. The Admin Delete recipient does not report its own deletion notice; other eligible controllers do.</p></article>
<article id="common-namespace_op-10"><h3>Shared conditions for this topic · Are Error Information or other logs updated?</h3><p>Identify lists establish current allocation/attachment; changed lists 04h/1Ch identify changes rather than complete state. Errors use More and applicable Error Information fields.</p></article>
<article id="common-namespace_op-11"><h3>Shared conditions for this topic · Is it recorded in the Persistent Event Log?</h3><p>Supported Change Namespace 06h records defined management changes; do not treat attachment as creation/deletion. Write protection follows supported Set Feature-event rules.</p></article>
<article id="common-namespace_op-12"><h3>Shared conditions for this topic · What survives or continues after Controller Reset?</h3><p>Completed configuration/attachment survives reset; command channels reset without deleting namespaces. For interrupted commands, inspect lists rather than assuming rollback.</p></article>
<article id="common-namespace_op-13"><h3>Shared conditions for this topic · What survives or continues after NVM Subsystem Reset?</h3><p>Subsystem reset is not Restore Default Namespace Configuration. Rediscover persisted namespaces/attachments and rebuild queues, accounting for domain scope.</p></article>
<article id="common-namespace_op-14"><h3>Shared conditions for this topic · What survives or continues after a power cycle?</h3><p>Completed namespace configuration/attachments persist. Ordinary/permanent write protection persist; until-power-cycle protection clears on a real power cycle, not all configuration.</p></article>
<article id="common-namespace_op-15"><h3>Shared conditions for this topic · Are other controllers or namespaces affected?</h3><p>Creation/deletion changes inventory and attachment lists select affected controllers. Shared namespace protection applies through all attached controllers.</p></article>
<article id="common-virtual_op-9"><h3>Shared conditions for this topic · Is an asynchronous event generated?</h3><p>Resource allocation and Online/Offline do not define a universal success AER; qualifying namespace or ANA changes follow their own rules.</p></article>
<article id="common-virtual_op-10"><h3>Shared conditions for this topic · Are Error Information or other logs updated?</h3><p>Verify resource state through capability/list structures and path state through namespace/ANA data; allocation changes are not themselves error entries.</p></article>
<article id="common-virtual_op-11"><h3>Shared conditions for this topic · Is it recorded in the Persistent Event Log?</h3><p>Virtualization Management has no dedicated PEL event; actual resets or qualifying namespace operations follow their events, not every Assign.</p></article>
<article id="common-virtual_op-12"><h3>Shared conditions for this topic · What survives or continues after Controller Reset?</h3><p>Primary disable/CLR/shutdown takes secondaries Offline, removing their flexible resources on the transition. Primary allocation is persistent but a new value takes effect after a CLR other than CC.EN Controller Reset.</p></article>
<article id="common-virtual_op-13"><h3>Shared conditions for this topic · What survives or continues after NVM Subsystem Reset?</h3><p>Rebuild affected primary/secondary operation after subsystem reset; persistent primary allocation does not preserve Online state or queues.</p></article>
<article id="common-virtual_op-14"><h3>Shared conditions for this topic · What survives or continues after a power cycle?</h3><p>Primary flexible allocation persists across power cycles; rediscover/reconfigure secondary resources and state. Offline does not delete persistent namespace/attachment configuration.</p></article>
<article id="common-virtual_op-15"><h3>Shared conditions for this topic · Are other controllers or namespaces affected?</h3><p>A primary manages its own secondaries/pool; one resource cannot belong to two controllers simultaneously. Shared namespaces expose the same data and require host write coordination.</p></article>
</section>
<section id="source-index"><h2>Source locations and existing figure guides</h2><p>Base printed page = PDF page−26; the other two use identical numbers. Locations follow the supplied PDF body and retain figure numbers. Shared pages contribute only the relevant definitions, excluding Fabrics and PCIe link/packet content.</p><ul class="qa-references">
<li id="ref-multipath"><strong>Base 2.4 · §2.4.1–2.4.2 (PCIe topology)</strong><br>Printed pages 34–37 · PDF 60–63 · Figure 19–22</li>
<li id="ref-ana"><strong>Base 2.4 · §2.4.2, 8.1.1 (PCIe namespace access)</strong><br>Printed pages 37, 578–584 · PDF 63, 604–610 · Figure 675–678</li>
<li id="ref-reset"><strong>Base 2.4 · §3.7.1–3.7.4</strong><br>Printed pages 120–124 · PDF 146–150</li>
<li id="ref-status"><strong>Base 2.4 · §4.2.3</strong><br>Printed pages 145–155 · PDF 171–181 · Figure 101–105</li>
<li id="ref-aer"><strong>Base 2.4 · §5.2.2</strong><br>Printed pages 183–190 · PDF 209–216 · Figure 150–156</li>
<li id="ref-aerfull"><strong>Base 2.4 · §5.2.2 (PCIe-applicable events)</strong><br>Printed pages 183–191 · PDF 209–217 · Figure 150–160</li>
<li id="ref-error"><strong>Base 2.4 · §5.2.13.1.2</strong><br>Printed pages 218–220 · PDF 244–246 · Figure 212</li>
<li id="ref-changedlog"><strong>Base 2.4 · §5.2.13.1.5</strong><br>Printed pages 226 · PDF 252</li>
<li id="ref-analog"><strong>Base 2.4 · §5.2.13.1.13</strong><br>Printed pages 241–244 · PDF 267–270 · Figure 229–231</li>
<li id="ref-pel"><strong>Base 2.4 · §5.2.13.1.14 (header, reset, hardware, Set Feature events)</strong><br>Printed pages 244–256, 258, 262–264 · PDF 270–282, 284, 288–290 · Figure 232–244, 246, 252–253</li>
<li id="ref-idlist"><strong>Base 2.4 · §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</strong><br>Printed pages 387–399, 402–404 · PDF 413–425, 428–430 · Figure 342–355, 360–362</li>
<li id="ref-virtualid"><strong>Base 2.4 · §5.2.14.3.1–5.2.14.3.2 (Primary Capabilities, Secondary List)</strong><br>Printed pages 402–404 · PDF 428–430 · Figure 360–362</li>
<li id="ref-nsattach"><strong>Base 2.4 · §5.2.24–5.2.25, 8.1.17–8.1.17.2</strong><br>Printed pages 444–448, 660–663 · PDF 470–474, 686–689 · Figure 442–450</li>
<li id="ref-virtualcmd"><strong>Base 2.4 · §5.3.6</strong><br>Printed pages 533–535 · PDF 559–561 · Figure 587–590</li>
<li id="ref-virtual"><strong>Base 2.4 · §8.2.7</strong><br>Printed pages 754–758 · PDF 780–784 · Figure 796</li>
</ul><h3>When you need a field guide</h3><p>Existing figure explanations have canonical locations; use these links instead of duplicating the same guide.</p><ul>
<li><a href="/nvme/figure-reference/command/en/#figure-b101">Base 2.4 Figure 101 · Completion Queue Entry: Status Field</a></li>
<li><a href="/nvme/figure-reference/command/en/#figure-b104">Base 2.4 Figure 104 · Status Code – Command Specific Status Values</a></li>
</ul><details><summary>Original documents used</summary><ul class="qr-sources">
<li>NVM Express Base Specification · Revision 2.4 · 2026-07-31<br><code>NVM-Express-Base-Specification-Revision-2.4-Ratified-2026.07.31.pdf</code></li>
<li>NVM Express NVM Command Set Specification · Revision 1.3 · 2026-07-31<br><code>NVM-Express-NVM-Command-Set-Specification-Revision-1.3-Ratified-2026.07.31.pdf</code></li>
<li>NVM Express NVMe over PCIe Transport Specification · Revision 1.4 · 2026-07-31<br><code>NVM-Express-NVMe-over-PCIe-Transport-Specification-Revision-1.4-Ratified-2026.07.31.pdf</code></li>
</ul></details></section>
</main>
<nav class="qr-top" aria-label="Bank and editions"><a href="#content">Skip to content</a><a href="/nvme/question-bank/en/">Question index</a><a href="/nvme/question-bank/virtualization/zh-tw/">繁體中文</a><a href="/DOCS/nvme-question-bank/virtualization.html">Chinese tutorial HTML</a></nav>
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
