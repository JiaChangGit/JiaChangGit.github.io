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
<main id="content"><p class="qr-eyebrow">BASE 2.4 / NVM 1.3 / PCIe 1.4 · Q1–320</p>
<header><p class="qa-range">Q256–Q267</p><h1>NVM sets, endurance groups and capacity</h1><p class="qr-intro">Establish ownership before interpreting layer-specific capacity and group-scoped health.</p><p>Practice first, then reveal 17 answer items per question. All numerical examples are hypothetical. Status is written SCT/SC; h indicates hexadecimal.</p></header>
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
<article class="qa-question" id="q-256" data-question="256"><h2><a class="qa-qid" href="#q-256">Q256</a> How are NVM sets, endurance groups and namespaces related?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-256-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-256-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>They organize capacity, endurance and logical access rather than rename one object.</p>
</li>
<li id="q-256-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>With set support, a formatted namespace resides in one set, each set in one group and each group in one domain.</p>
</li>
<li id="q-256-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Read support and lists, then namespace membership identifiers.</p>
</li>
<li id="q-256-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>Set lists, group logs and namespace Identify provide distinct capacity, health and membership views.</p>
</li>
<li id="q-256-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Draw supported layers and actual IDs; absence of set support does not create a fictional Set 0 layer.</p>
</li>
<li id="q-256-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Example EG1 contains Set 2/3 and their namespaces, with endurance managed across those sets.</p>
</li>
<li id="q-256-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Set support requires groups; group support does not require sets.</p>
</li>
<li id="q-256-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-256-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Capacity completion has no generic AER; cascaded namespace deletion follows explicit list/notice rules. <a class="qa-rule-link" href="#common-capacity_op-9">Full rule in this volume</a></p>
</li>
<li id="q-256-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Verify lists, layer-specific capacity and supported media ownership. <a class="qa-rule-link" href="#common-capacity_op-10">Full rule in this volume</a></p>
</li>
<li id="q-256-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>There is no universal dedicated Capacity Management PEL completion event; separately qualifying namespace or hardware events use their own conditions. <a class="qa-rule-link" href="#common-capacity_op-11">Full rule in this volume</a></p>
</li>
<li id="q-256-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Completed storage configuration is not volatile queue state and is not deleted by ordinary CLR. <a class="qa-rule-link" href="#common-capacity_op-12">Full rule in this volume</a></p>
</li>
<li id="q-256-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Subsystem reset is distinct from restoring default capacity configuration; rediscover retained storage configuration unless a separate management action changed it. <a class="qa-rule-link" href="#common-capacity_op-13">Full rule in this volume</a></p>
</li>
<li id="q-256-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Completed configuration persists across power cycles; requery interrupted operations because missing CQE does not prove no effect. <a class="qa-rule-link" href="#common-capacity_op-14">Full rule in this volume</a></p>
</li>
<li id="q-256-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Deleting a group cascades through sets/namespaces; deleting a set removes its namespaces across all paths. <a class="qa-rule-link" href="#common-capacity_op-15">Full rule in this volume</a></p>
</li>
<li id="q-256-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Cross-check membership through all supported layers.</p>
</li>
<li id="q-256-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First establish supported layers before interpreting zero IDs.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-capacitymodel">Base 2.4 §3.2.2–3.2.3, 3.8</a> · <a href="#ref-capacitycmd">Base 2.4 §5.2.3</a> · <a href="#ref-capacityop">Base 2.4 §8.1.4</a> · <a href="#ref-eghealth">Base 2.4 §5.2.13.1.10</a> · <a href="#ref-egevents">Base 2.4 §3.2.3.1, 5.2.13.1.15, 5.2.30.1.17</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-nvmcreate">NVM Command Set 1.3 §4.1.5.8, 4.1.6, 5.8</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-257" data-question="257"><h2><a class="qa-qid" href="#q-257">Q257</a> How are sets and groups discovered through Identify?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-257-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-257-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Capability, inventory and maximum identifier answer different questions.</p>
</li>
<li id="q-257-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Discovery reflects information accessible through the queried controller.</p>
</li>
<li id="q-257-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Read support/maxima and the respective inventories.</p>
</li>
<li id="q-257-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>Set attributes include capacities/membership; detailed group data comes from LID 09h.</p>
</li>
<li id="q-257-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Enumerate actual IDs before reading details; do not assume every possible ID exists.</p>
</li>
<li id="q-257-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Discover inventory and distinguish absent allocation from unsupported capability.</p>
</li>
<li id="q-257-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Required zero output for unsupported functionality does not create valid entity 0.</p>
</li>
<li id="q-257-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-257-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Capacity completion has no generic AER; cascaded namespace deletion follows explicit list/notice rules. <a class="qa-rule-link" href="#common-capacity_op-9">Full rule in this volume</a></p>
</li>
<li id="q-257-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Verify lists, layer-specific capacity and supported media ownership. <a class="qa-rule-link" href="#common-capacity_op-10">Full rule in this volume</a></p>
</li>
<li id="q-257-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>There is no universal dedicated Capacity Management PEL completion event; separately qualifying namespace or hardware events use their own conditions. <a class="qa-rule-link" href="#common-capacity_op-11">Full rule in this volume</a></p>
</li>
<li id="q-257-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Completed storage configuration is not volatile queue state and is not deleted by ordinary CLR. <a class="qa-rule-link" href="#common-capacity_op-12">Full rule in this volume</a></p>
</li>
<li id="q-257-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Subsystem reset is distinct from restoring default capacity configuration; rediscover retained storage configuration unless a separate management action changed it. <a class="qa-rule-link" href="#common-capacity_op-13">Full rule in this volume</a></p>
</li>
<li id="q-257-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Completed configuration persists across power cycles; requery interrupted operations because missing CQE does not prove no effect. <a class="qa-rule-link" href="#common-capacity_op-14">Full rule in this volume</a></p>
</li>
<li id="q-257-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Deleting a group cascades through sets/namespaces; deleting a set removes its namespaces across all paths. <a class="qa-rule-link" href="#common-capacity_op-15">Full rule in this volume</a></p>
</li>
<li id="q-257-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Reconcile advertisement, inventories, maxima and membership.</p>
</li>
<li id="q-257-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First check confusion between maximum ID and current count.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-capacitymodel">Base 2.4 §3.2.2–3.2.3, 3.8</a> · <a href="#ref-capacitycmd">Base 2.4 §5.2.3</a> · <a href="#ref-capacityop">Base 2.4 §8.1.4</a> · <a href="#ref-eghealth">Base 2.4 §5.2.13.1.10</a> · <a href="#ref-egevents">Base 2.4 §3.2.3.1, 5.2.13.1.15, 5.2.30.1.17</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-nvmcreate">NVM Command Set 1.3 §4.1.5.8, 4.1.6, 5.8</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-258" data-question="258"><h2><a class="qa-qid" href="#q-258">Q258</a> How is a namespace created in a selected set or group?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-258-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-258-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Select a resource pool while encoding logical capacity in blocks of the chosen format.</p>
</li>
<li id="q-258-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Creation selects placement for a new object rather than moving an existing namespace.</p>
</li>
<li id="q-258-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Check inventory, capacity and LBA format before selecting membership.</p>
</li>
<li id="q-258-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>Create fields combine logical size/capacity, format/protection and membership.</p>
</li>
<li id="q-258-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Both zero delegate selection; group-only selects within it; a specified set requires its correct nonzero group.</p>
</li>
<li id="q-258-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Success returns NSID; verify allocated Identify and attach separately.</p>
</li>
<li id="q-258-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Nonexistent/mismatched explicit membership is not automatic selection.</p>
</li>
<li id="q-258-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-258-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Capacity completion has no generic AER; cascaded namespace deletion follows explicit list/notice rules. <a class="qa-rule-link" href="#common-capacity_op-9">Full rule in this volume</a></p>
</li>
<li id="q-258-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Verify lists, layer-specific capacity and supported media ownership. <a class="qa-rule-link" href="#common-capacity_op-10">Full rule in this volume</a></p>
</li>
<li id="q-258-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>There is no universal dedicated Capacity Management PEL completion event; separately qualifying namespace or hardware events use their own conditions. <a class="qa-rule-link" href="#common-capacity_op-11">Full rule in this volume</a></p>
</li>
<li id="q-258-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Completed storage configuration is not volatile queue state and is not deleted by ordinary CLR. <a class="qa-rule-link" href="#common-capacity_op-12">Full rule in this volume</a></p>
</li>
<li id="q-258-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Subsystem reset is distinct from restoring default capacity configuration; rediscover retained storage configuration unless a separate management action changed it. <a class="qa-rule-link" href="#common-capacity_op-13">Full rule in this volume</a></p>
</li>
<li id="q-258-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Completed configuration persists across power cycles; requery interrupted operations because missing CQE does not prove no effect. <a class="qa-rule-link" href="#common-capacity_op-14">Full rule in this volume</a></p>
</li>
<li id="q-258-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Deleting a group cascades through sets/namespaces; deleting a set removes its namespaces across all paths. <a class="qa-rule-link" href="#common-capacity_op-15">Full rule in this volume</a></p>
</li>
<li id="q-258-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Verify returned membership and the correct allocation layer.</p>
</li>
<li id="q-258-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First verify membership, not merely existence of both IDs.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-capacitymodel">Base 2.4 §3.2.2–3.2.3, 3.8</a> · <a href="#ref-capacitycmd">Base 2.4 §5.2.3</a> · <a href="#ref-capacityop">Base 2.4 §8.1.4</a> · <a href="#ref-eghealth">Base 2.4 §5.2.13.1.10</a> · <a href="#ref-egevents">Base 2.4 §3.2.3.1, 5.2.13.1.15, 5.2.30.1.17</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-nvmcreate">NVM Command Set 1.3 §4.1.5.8, 4.1.6, 5.8</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-259" data-question="259"><h2><a class="qa-qid" href="#q-259">Q259</a> What happens when a set or group identifier does not exist?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-259-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-259-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Zero and nonexistent nonzero identifiers differ, with zero semantics varying by command.</p>
</li>
<li id="q-259-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Identify whether the operation is namespace/capacity management, logging or a feature.</p>
</li>
<li id="q-259-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Check current inventory and command-specific special values.</p>
</li>
<li id="q-259-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>For example, zero ELID auto-selects a domain for group creation but is invalid for group deletion.</p>
</li>
<li id="q-259-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Start from a valid request and isolate one nonexistent identifier.</p>
</li>
<li id="q-259-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Valid automatic selection returns the selected ID; invalid explicit IDs must not silently target another object.</p>
</li>
<li id="q-259-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Invalid capacity entity selectors and nonexistent FID 18h groups require Invalid Field.</p>
</li>
<li id="q-259-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-259-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Capacity completion has no generic AER; cascaded namespace deletion follows explicit list/notice rules. <a class="qa-rule-link" href="#common-capacity_op-9">Full rule in this volume</a></p>
</li>
<li id="q-259-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Verify lists, layer-specific capacity and supported media ownership. <a class="qa-rule-link" href="#common-capacity_op-10">Full rule in this volume</a></p>
</li>
<li id="q-259-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>There is no universal dedicated Capacity Management PEL completion event; separately qualifying namespace or hardware events use their own conditions. <a class="qa-rule-link" href="#common-capacity_op-11">Full rule in this volume</a></p>
</li>
<li id="q-259-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Completed storage configuration is not volatile queue state and is not deleted by ordinary CLR. <a class="qa-rule-link" href="#common-capacity_op-12">Full rule in this volume</a></p>
</li>
<li id="q-259-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Subsystem reset is distinct from restoring default capacity configuration; rediscover retained storage configuration unless a separate management action changed it. <a class="qa-rule-link" href="#common-capacity_op-13">Full rule in this volume</a></p>
</li>
<li id="q-259-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Completed configuration persists across power cycles; requery interrupted operations because missing CQE does not prove no effect. <a class="qa-rule-link" href="#common-capacity_op-14">Full rule in this volume</a></p>
</li>
<li id="q-259-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Deleting a group cascades through sets/namespaces; deleting a set removes its namespaces across all paths. <a class="qa-rule-link" href="#common-capacity_op-15">Full rule in this volume</a></p>
</li>
<li id="q-259-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Base has ENDGID-ignore rules when groups are unsupported; distinguish absence of capability from invalid IDs under support.</p>
</li>
<li id="q-259-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First read zero semantics for that specific command.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-capacitymodel">Base 2.4 §3.2.2–3.2.3, 3.8</a> · <a href="#ref-capacitycmd">Base 2.4 §5.2.3</a> · <a href="#ref-capacityop">Base 2.4 §8.1.4</a> · <a href="#ref-eghealth">Base 2.4 §5.2.13.1.10</a> · <a href="#ref-egevents">Base 2.4 §3.2.3.1, 5.2.13.1.15, 5.2.30.1.17</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-nvmcreate">NVM Command Set 1.3 §4.1.5.8, 4.1.6, 5.8</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-260" data-question="260"><h2><a class="qa-qid" href="#q-260">Q260</a> What does the Endurance Group Information Log report?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-260-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-260-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>This log provides group-scoped health/workload rather than only aggregate SMART.</p>
</li>
<li id="q-260-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>LID 09h selects ENDGID and describes the group’s lifetime.</p>
</li>
<li id="q-260-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Establish support and existence before reading the 512-byte structure.</p>
</li>
<li id="q-260-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>Health, host/media data volume, command/error counts and byte capacities occupy distinct field groups.</p>
</li>
<li id="q-260-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Inspect health and difference snapshots; these data counters use rounded billions of bytes, not SMART’s 512000-byte units.</p>
</li>
<li id="q-260-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>MUW includes internal writes unlike DUW; account for quantization and unreported zero values.</p>
</li>
<li id="q-260-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Unreported zero is not zero consumption and cannot support a meaningful amplification ratio.</p>
</li>
<li id="q-260-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-260-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Capacity completion has no generic AER; cascaded namespace deletion follows explicit list/notice rules. <a class="qa-rule-link" href="#common-capacity_op-9">Full rule in this volume</a></p>
</li>
<li id="q-260-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Verify lists, layer-specific capacity and supported media ownership. <a class="qa-rule-link" href="#common-capacity_op-10">Full rule in this volume</a></p>
</li>
<li id="q-260-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>There is no universal dedicated Capacity Management PEL completion event; separately qualifying namespace or hardware events use their own conditions. <a class="qa-rule-link" href="#common-capacity_op-11">Full rule in this volume</a></p>
</li>
<li id="q-260-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Group lifetime health is not restarted by a querying controller reset; reassess current warnings and reissue interrupted reads.</p>
</li>
<li id="q-260-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Subsystem reset does not delete the group; compare cumulative values, current state and acknowledgment state separately.</p>
</li>
<li id="q-260-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>A retained group’s lifetime information persists; feature/event configuration restoration remains a separate rule.</p>
</li>
<li id="q-260-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Group health can be shared across readers; record acknowledgments and reader timing.</p>
</li>
<li id="q-260-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Correlate group membership and aggregate warning semantics, not bytewise equality with SMART.</p>
</li>
<li id="q-260-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First check same-name counters with different units.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-capacitymodel">Base 2.4 §3.2.2–3.2.3, 3.8</a> · <a href="#ref-capacitycmd">Base 2.4 §5.2.3</a> · <a href="#ref-capacityop">Base 2.4 §8.1.4</a> · <a href="#ref-eghealth">Base 2.4 §5.2.13.1.10</a> · <a href="#ref-egevents">Base 2.4 §3.2.3.1, 5.2.13.1.15, 5.2.30.1.17</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-nvmcreate">NVM Command Set 1.3 §4.1.5.8, 4.1.6, 5.8</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-261" data-question="261"><h2><a class="qa-qid" href="#q-261">Q261</a> How are group health warnings and events updated?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-261-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-261-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Live health, pending-group entries and host notices form separate stages.</p>
</li>
<li id="q-261-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>FID 18h is per-group, while AEC enables aggregate-log notices.</p>
</li>
<li id="q-261-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Inspect live health, per-group event mask and AEC notice enablement.</p>
</li>
<li id="q-261-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>Group warning bits 0/2/3 indicate spare/reliability/read-only; namespace write protection must not set EGRO. Bit 1 is reserved, unlike SMART temperature.</p>
</li>
<li id="q-261-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Pending groups enter 0Fh; read it, then each 09h. Successful 09h RAE0 acknowledges/removes that group’s pending entry.</p>
</li>
<li id="q-261-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Aggregate acknowledgment is not acknowledgment of every group; current warning may already have cleared.</p>
</li>
<li id="q-261-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Reserved warning bits or nonexistent groups in FID 18h require Invalid Field.</p>
</li>
<li id="q-261-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-261-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>FID 18h selects group warnings for the aggregate; AEC and AER conditions govern host notice of additions.</p>
</li>
<li id="q-261-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>LID 0Fh lists pending group IDs;09h reports current group health and successful RAE0 reads acknowledge that group.</p>
</li>
<li id="q-261-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>There is no universal dedicated Capacity Management PEL completion event; separately qualifying namespace or hardware events use their own conditions. <a class="qa-rule-link" href="#common-capacity_op-11">Full rule in this volume</a></p>
</li>
<li id="q-261-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Group lifetime health is not restarted by a querying controller reset; reassess current warnings and reissue interrupted reads.</p>
</li>
<li id="q-261-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Subsystem reset does not delete the group; compare cumulative values, current state and acknowledgment state separately.</p>
</li>
<li id="q-261-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>A retained group’s lifetime information persists; feature/event configuration restoration remains a separate rule.</p>
</li>
<li id="q-261-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Group health can be shared across readers; record acknowledgments and reader timing.</p>
</li>
<li id="q-261-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>The specified aggregate SMART rule applies when all groups assert the bit, not merely one group.</p>
</li>
<li id="q-261-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First check confusion between aggregate and per-group acknowledgment.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-capacitymodel">Base 2.4 §3.2.2–3.2.3, 3.8</a> · <a href="#ref-capacitycmd">Base 2.4 §5.2.3</a> · <a href="#ref-capacityop">Base 2.4 §8.1.4</a> · <a href="#ref-eghealth">Base 2.4 §5.2.13.1.10</a> · <a href="#ref-egevents">Base 2.4 §3.2.3.1, 5.2.13.1.15, 5.2.30.1.17</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-nvmcreate">NVM Command Set 1.3 §4.1.5.8, 4.1.6, 5.8</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-262" data-question="262"><h2><a class="qa-qid" href="#q-262">Q262</a> How are total and unallocated capacities determined?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-262-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-262-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Unallocated means unallocated to a particular next layer, not universally free for any operation.</p>
</li>
<li id="q-262-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Capacity pools exist at subsystem, domain, group or set scope.</p>
</li>
<li id="q-262-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Read controller/domain capacities, group capacities and set attributes.</p>
</li>
<li id="q-262-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>Physical-capacity fields use bytes; namespace sizes use formatted blocks.</p>
</li>
<li id="q-262-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Select the operation’s capacity source under Figure 89, including granularity and adjustment factor.</p>
</li>
<li id="q-262-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Creating a set allocates from UEGCAP without requiring another decrease in subsystem UNVMCAP.</p>
</li>
<li id="q-262-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Zero may mean unreported under field-specific rules rather than no capacity.</p>
</li>
<li id="q-262-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-262-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Capacity completion has no generic AER; cascaded namespace deletion follows explicit list/notice rules. <a class="qa-rule-link" href="#common-capacity_op-9">Full rule in this volume</a></p>
</li>
<li id="q-262-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Verify lists, layer-specific capacity and supported media ownership. <a class="qa-rule-link" href="#common-capacity_op-10">Full rule in this volume</a></p>
</li>
<li id="q-262-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>There is no universal dedicated Capacity Management PEL completion event; separately qualifying namespace or hardware events use their own conditions. <a class="qa-rule-link" href="#common-capacity_op-11">Full rule in this volume</a></p>
</li>
<li id="q-262-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Completed storage configuration is not volatile queue state and is not deleted by ordinary CLR. <a class="qa-rule-link" href="#common-capacity_op-12">Full rule in this volume</a></p>
</li>
<li id="q-262-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Subsystem reset is distinct from restoring default capacity configuration; rediscover retained storage configuration unless a separate management action changed it. <a class="qa-rule-link" href="#common-capacity_op-13">Full rule in this volume</a></p>
</li>
<li id="q-262-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Completed configuration persists across power cycles; requery interrupted operations because missing CQE does not prove no effect. <a class="qa-rule-link" href="#common-capacity_op-14">Full rule in this volume</a></p>
</li>
<li id="q-262-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Deleting a group cascades through sets/namespaces; deleting a set removes its namespaces across all paths. <a class="qa-rule-link" href="#common-capacity_op-15">Full rule in this volume</a></p>
</li>
<li id="q-262-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Compare within one layer to avoid double counting.</p>
</li>
<li id="q-262-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First identify which entity is being created.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-capacitymodel">Base 2.4 §3.2.2–3.2.3, 3.8</a> · <a href="#ref-capacitycmd">Base 2.4 §5.2.3</a> · <a href="#ref-capacityop">Base 2.4 §8.1.4</a> · <a href="#ref-eghealth">Base 2.4 §5.2.13.1.10</a> · <a href="#ref-egevents">Base 2.4 §3.2.3.1, 5.2.13.1.15, 5.2.30.1.17</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-nvmcreate">NVM Command Set 1.3 §4.1.5.8, 4.1.6, 5.8</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-263" data-question="263"><h2><a class="qa-qid" href="#q-263">Q263</a> How do namespace creation and deletion affect free capacity?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-263-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-263-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Namespace allocation consumes its containing pool, not always controller UNVMCAP.</p>
</li>
<li id="q-263-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Use the supported containing layer: set, group or domain/subsystem.</p>
</li>
<li id="q-263-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Preserve membership, format, actual NVMCAP and pool snapshots.</p>
</li>
<li id="q-263-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>Logical size/capacity and physical consumption differ because of allocation granularity.</p>
</li>
<li id="q-263-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>After creation/deletion verify inventory and the corresponding pool.</p>
</li>
<li id="q-263-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Capacity follows allocation rules; Detach alone does not return namespace capacity.</p>
</li>
<li id="q-263-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Capacity exhaustion differs from identifier/count exhaustion.</p>
</li>
<li id="q-263-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-263-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Capacity completion has no generic AER; cascaded namespace deletion follows explicit list/notice rules. <a class="qa-rule-link" href="#common-capacity_op-9">Full rule in this volume</a></p>
</li>
<li id="q-263-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Verify lists, layer-specific capacity and supported media ownership. <a class="qa-rule-link" href="#common-capacity_op-10">Full rule in this volume</a></p>
</li>
<li id="q-263-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>There is no universal dedicated Capacity Management PEL completion event; separately qualifying namespace or hardware events use their own conditions. <a class="qa-rule-link" href="#common-capacity_op-11">Full rule in this volume</a></p>
</li>
<li id="q-263-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Completed storage configuration is not volatile queue state and is not deleted by ordinary CLR. <a class="qa-rule-link" href="#common-capacity_op-12">Full rule in this volume</a></p>
</li>
<li id="q-263-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Subsystem reset is distinct from restoring default capacity configuration; rediscover retained storage configuration unless a separate management action changed it. <a class="qa-rule-link" href="#common-capacity_op-13">Full rule in this volume</a></p>
</li>
<li id="q-263-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Completed configuration persists across power cycles; requery interrupted operations because missing CQE does not prove no effect. <a class="qa-rule-link" href="#common-capacity_op-14">Full rule in this volume</a></p>
</li>
<li id="q-263-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Deleting a group cascades through sets/namespaces; deleting a set removes its namespaces across all paths. <a class="qa-rule-link" href="#common-capacity_op-15">Full rule in this volume</a></p>
</li>
<li id="q-263-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Verify allocation separately from data sanitization; deletion is not proof of purge.</p>
</li>
<li id="q-263-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First check the accounting layer and whether the operation was only Detach.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-capacitymodel">Base 2.4 §3.2.2–3.2.3, 3.8</a> · <a href="#ref-capacitycmd">Base 2.4 §5.2.3</a> · <a href="#ref-capacityop">Base 2.4 §8.1.4</a> · <a href="#ref-eghealth">Base 2.4 §5.2.13.1.10</a> · <a href="#ref-egevents">Base 2.4 §3.2.3.1, 5.2.13.1.15, 5.2.30.1.17</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-nvmcreate">NVM Command Set 1.3 §4.1.5.8, 4.1.6, 5.8</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-264" data-question="264"><h2><a class="qa-qid" href="#q-264">Q264</a> How does Capacity Management allocate and release groups and sets?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-264-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-264-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Fixed selects supported layouts; Variable creates entities by requested capacity.</p>
</li>
<li id="q-264-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Changes can cascade to contained namespaces and all paths.</p>
</li>
<li id="q-264-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Check management/deletion support and supported fixed configurations.</p>
</li>
<li id="q-264-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>OPER selects layout/create/delete/restore; ELID meaning varies and CAPU:CAPL encodes create bytes.</p>
</li>
<li id="q-264-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Variable allocation proceeds group→set→namespace; fixed reconfiguration follows clearing/selection prerequisites.</p>
</li>
<li id="q-264-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Creation returns CELID; other operations do not universally return a valid created ID.</p>
</li>
<li id="q-264-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Deletion cascades; default restoration with remaining groups/sets requires Command Sequence Error.</p>
</li>
<li id="q-264-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-264-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Capacity completion has no generic AER; cascaded namespace deletion follows explicit list/notice rules. <a class="qa-rule-link" href="#common-capacity_op-9">Full rule in this volume</a></p>
</li>
<li id="q-264-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Verify lists, layer-specific capacity and supported media ownership. <a class="qa-rule-link" href="#common-capacity_op-10">Full rule in this volume</a></p>
</li>
<li id="q-264-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>There is no universal dedicated Capacity Management PEL completion event; separately qualifying namespace or hardware events use their own conditions. <a class="qa-rule-link" href="#common-capacity_op-11">Full rule in this volume</a></p>
</li>
<li id="q-264-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Completed storage configuration is not volatile queue state and is not deleted by ordinary CLR. <a class="qa-rule-link" href="#common-capacity_op-12">Full rule in this volume</a></p>
</li>
<li id="q-264-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Subsystem reset is distinct from restoring default capacity configuration; rediscover retained storage configuration unless a separate management action changed it. <a class="qa-rule-link" href="#common-capacity_op-13">Full rule in this volume</a></p>
</li>
<li id="q-264-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Completed configuration persists across power cycles; requery interrupted operations because missing CQE does not prove no effect. <a class="qa-rule-link" href="#common-capacity_op-14">Full rule in this volume</a></p>
</li>
<li id="q-264-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Deleting a group cascades through sets/namespaces; deleting a set removes its namespaces across all paths. <a class="qa-rule-link" href="#common-capacity_op-15">Full rule in this volume</a></p>
</li>
<li id="q-264-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Requery final lists/ownership/capacity; intermediate accesses may be indeterminate.</p>
</li>
<li id="q-264-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First check operation and its zero-identifier semantics.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-capacitymodel">Base 2.4 §3.2.2–3.2.3, 3.8</a> · <a href="#ref-capacitycmd">Base 2.4 §5.2.3</a> · <a href="#ref-capacityop">Base 2.4 §8.1.4</a> · <a href="#ref-eghealth">Base 2.4 §5.2.13.1.10</a> · <a href="#ref-egevents">Base 2.4 §3.2.3.1, 5.2.13.1.15, 5.2.30.1.17</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-nvmcreate">NVM Command Set 1.3 §4.1.5.8, 4.1.6, 5.8</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-265" data-question="265"><h2><a class="qa-qid" href="#q-265">Q265</a> What happens when capacity or identifiers are exhausted?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-265-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-265-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Capacity exhaustion and identifier exhaustion are distinct limits.</p>
</li>
<li id="q-265-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Group creation checks relevant pool/max size; set creation checks UEGCAP.</p>
</li>
<li id="q-265-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Inspect capacity limits and inventory.</p>
</li>
<li id="q-265-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>Interpret requested bytes with adjustment and allocation granularity.</p>
</li>
<li id="q-265-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Isolate capacity and identifier exhaustion in separate scenarios.</p>
</li>
<li id="q-265-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Adequate resources create an entity and return CELID; failure must not fabricate one.</p>
</li>
<li id="q-265-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Capacity shortage returns 1/26h; identifier exhaustion returns 1/2Dh.</p>
</li>
<li id="q-265-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-265-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Capacity completion has no generic AER; cascaded namespace deletion follows explicit list/notice rules. <a class="qa-rule-link" href="#common-capacity_op-9">Full rule in this volume</a></p>
</li>
<li id="q-265-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Insufficient-capacity creation requires the stated CSINFO detail when Error Log is supported; preserve the prose/Figure 165 semantic conflict.</p>
</li>
<li id="q-265-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>There is no universal dedicated Capacity Management PEL completion event; separately qualifying namespace or hardware events use their own conditions. <a class="qa-rule-link" href="#common-capacity_op-11">Full rule in this volume</a></p>
</li>
<li id="q-265-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Completed storage configuration is not volatile queue state and is not deleted by ordinary CLR. <a class="qa-rule-link" href="#common-capacity_op-12">Full rule in this volume</a></p>
</li>
<li id="q-265-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Subsystem reset is distinct from restoring default capacity configuration; rediscover retained storage configuration unless a separate management action changed it. <a class="qa-rule-link" href="#common-capacity_op-13">Full rule in this volume</a></p>
</li>
<li id="q-265-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Completed configuration persists across power cycles; requery interrupted operations because missing CQE does not prove no effect. <a class="qa-rule-link" href="#common-capacity_op-14">Full rule in this volume</a></p>
</li>
<li id="q-265-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Deleting a group cascades through sets/namespaces; deleting a set removes its namespaces across all paths. <a class="qa-rule-link" href="#common-capacity_op-15">Full rule in this volume</a></p>
</li>
<li id="q-265-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Prose specifies largest creatable capacity in CSINFO, while Figure 165 describes required capacity. Preserve this conflict rather than using one interpretation as an unconditional conformance oracle.</p>
</li>
<li id="q-265-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First identify the exhausted resource, then the CSINFO source ambiguity.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-capacitymodel">Base 2.4 §3.2.2–3.2.3, 3.8</a> · <a href="#ref-capacitycmd">Base 2.4 §5.2.3</a> · <a href="#ref-capacityop">Base 2.4 §8.1.4</a> · <a href="#ref-eghealth">Base 2.4 §5.2.13.1.10</a> · <a href="#ref-egevents">Base 2.4 §3.2.3.1, 5.2.13.1.15, 5.2.30.1.17</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-nvmcreate">NVM Command Set 1.3 §4.1.5.8, 4.1.6, 5.8</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-266" data-question="266"><h2><a class="qa-qid" href="#q-266">Q266</a> Which views change after capacity reconfiguration?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-266-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-266-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Validate coherent views, not just successful CQE.</p>
</li>
<li id="q-266-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Inspect affected group/set/namespace/domain/media relationships.</p>
</li>
<li id="q-266-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Preserve inventory, capacity and ownership snapshots.</p>
</li>
<li id="q-266-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>Group creation changes parent capacity; set creation changes set inventory/UEGCAP but not UNVMCAP; deletion follows its cascade.</p>
</li>
<li id="q-266-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Read after completion and account for concurrent management.</p>
</li>
<li id="q-266-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Deleting a set removes its namespaces, clears applicable media ownership and returns group capacity.</p>
</li>
<li id="q-266-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Ordered intermediate updates are not universally atomic byte-for-byte to all readers.</p>
</li>
<li id="q-266-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-266-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Capacity completion has no generic AER; cascaded namespace deletion follows explicit list/notice rules. <a class="qa-rule-link" href="#common-capacity_op-9">Full rule in this volume</a></p>
</li>
<li id="q-266-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Verify lists, layer-specific capacity and supported media ownership. <a class="qa-rule-link" href="#common-capacity_op-10">Full rule in this volume</a></p>
</li>
<li id="q-266-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>There is no universal dedicated Capacity Management PEL completion event; separately qualifying namespace or hardware events use their own conditions. <a class="qa-rule-link" href="#common-capacity_op-11">Full rule in this volume</a></p>
</li>
<li id="q-266-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Completed storage configuration is not volatile queue state and is not deleted by ordinary CLR. <a class="qa-rule-link" href="#common-capacity_op-12">Full rule in this volume</a></p>
</li>
<li id="q-266-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Subsystem reset is distinct from restoring default capacity configuration; rediscover retained storage configuration unless a separate management action changed it. <a class="qa-rule-link" href="#common-capacity_op-13">Full rule in this volume</a></p>
</li>
<li id="q-266-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Completed configuration persists across power cycles; requery interrupted operations because missing CQE does not prove no effect. <a class="qa-rule-link" href="#common-capacity_op-14">Full rule in this volume</a></p>
</li>
<li id="q-266-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Deleting a group cascades through sets/namespaces; deleting a set removes its namespaces across all paths. <a class="qa-rule-link" href="#common-capacity_op-15">Full rule in this volume</a></p>
</li>
<li id="q-266-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Verify the full chain of inventory, child removal, accounting and rediscovery notices.</p>
</li>
<li id="q-266-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First check completion and concurrent-operation timing.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-capacitymodel">Base 2.4 §3.2.2–3.2.3, 3.8</a> · <a href="#ref-capacitycmd">Base 2.4 §5.2.3</a> · <a href="#ref-capacityop">Base 2.4 §8.1.4</a> · <a href="#ref-eghealth">Base 2.4 §5.2.13.1.10</a> · <a href="#ref-egevents">Base 2.4 §3.2.3.1, 5.2.13.1.15, 5.2.30.1.17</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-nvmcreate">NVM Command Set 1.3 §4.1.5.8, 4.1.6, 5.8</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-267" data-question="267"><h2><a class="qa-qid" href="#q-267">Q267</a> How does storage configuration persist across reset and power cycle?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-267-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-267-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Storage organization is distinct from transient I/O queues; reset is not configuration deletion.</p>
</li>
<li id="q-267-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Compare completed entity membership and capacity accounting.</p>
</li>
<li id="q-267-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Snapshot configuration, identity, capacities and outstanding management.</p>
</li>
<li id="q-267-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>OPER5 default restoration is separate and has inventory prerequisites.</p>
</li>
<li id="q-267-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Rediscover after channel recovery; interrupted operations require outcome discovery rather than assumed rollback.</p>
</li>
<li id="q-267-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Completed configuration remains identifiable; explain differences through actual management/state changes.</p>
</li>
<li id="q-267-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Missing completion establishes uncertainty, not an unchanged configuration.</p>
</li>
<li id="q-267-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-267-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Capacity completion has no generic AER; cascaded namespace deletion follows explicit list/notice rules. <a class="qa-rule-link" href="#common-capacity_op-9">Full rule in this volume</a></p>
</li>
<li id="q-267-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Verify lists, layer-specific capacity and supported media ownership. <a class="qa-rule-link" href="#common-capacity_op-10">Full rule in this volume</a></p>
</li>
<li id="q-267-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>There is no universal dedicated Capacity Management PEL completion event; separately qualifying namespace or hardware events use their own conditions. <a class="qa-rule-link" href="#common-capacity_op-11">Full rule in this volume</a></p>
</li>
<li id="q-267-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Completed storage configuration is not volatile queue state and is not deleted by ordinary CLR. <a class="qa-rule-link" href="#common-capacity_op-12">Full rule in this volume</a></p>
</li>
<li id="q-267-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Subsystem reset is distinct from restoring default capacity configuration; rediscover retained storage configuration unless a separate management action changed it. <a class="qa-rule-link" href="#common-capacity_op-13">Full rule in this volume</a></p>
</li>
<li id="q-267-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Completed configuration persists across power cycles; requery interrupted operations because missing CQE does not prove no effect. <a class="qa-rule-link" href="#common-capacity_op-14">Full rule in this volume</a></p>
</li>
<li id="q-267-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Deleting a group cascades through sets/namespaces; deleting a set removes its namespaces across all paths. <a class="qa-rule-link" href="#common-capacity_op-15">Full rule in this volume</a></p>
</li>
<li id="q-267-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Distinguish temporary query unavailability from missing persistent configuration.</p>
</li>
<li id="q-267-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First check for separate restore/delete/reconfiguration activity.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-capacitymodel">Base 2.4 §3.2.2–3.2.3, 3.8</a> · <a href="#ref-capacitycmd">Base 2.4 §5.2.3</a> · <a href="#ref-capacityop">Base 2.4 §8.1.4</a> · <a href="#ref-eghealth">Base 2.4 §5.2.13.1.10</a> · <a href="#ref-egevents">Base 2.4 §3.2.3.1, 5.2.13.1.15, 5.2.30.1.17</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-nvmcreate">NVM Command Set 1.3 §4.1.5.8, 4.1.6, 5.8</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<section id="common-rules" class="qa-common"><h2>Shared rules linked from the answers</h2><p>Each shared mechanism is explained in full once in this volume. Use browser Back to return to the question; explicit command or feature exceptions take precedence.</p>
<article id="common-capacity_op-9"><h3>Shared conditions for this topic · Is an asynchronous event generated?</h3><p>Capacity completion has no generic AER; cascaded namespace deletion follows explicit list/notice rules. Health events use separate FID 18h/AEC settings.</p></article>
<article id="common-capacity_op-10"><h3>Shared conditions for this topic · Are Error Information or other logs updated?</h3><p>Verify lists, layer-specific capacity and supported media ownership. Insufficient-capacity creation has explicit error-log detail requirements beyond the CQE.</p></article>
<article id="common-capacity_op-11"><h3>Shared conditions for this topic · Is it recorded in the Persistent Event Log?</h3><p>There is no universal dedicated Capacity Management PEL completion event; separately qualifying namespace or hardware events use their own conditions.</p></article>
<article id="common-capacity_op-12"><h3>Shared conditions for this topic · What survives or continues after Controller Reset?</h3><p>Completed storage configuration is not volatile queue state and is not deleted by ordinary CLR. Requery interrupted operations rather than assume rollback.</p></article>
<article id="common-capacity_op-13"><h3>Shared conditions for this topic · What survives or continues after NVM Subsystem Reset?</h3><p>Subsystem reset is distinct from restoring default capacity configuration; rediscover retained storage configuration unless a separate management action changed it.</p></article>
<article id="common-capacity_op-14"><h3>Shared conditions for this topic · What survives or continues after a power cycle?</h3><p>Completed configuration persists across power cycles; requery interrupted operations because missing CQE does not prove no effect.</p></article>
<article id="common-capacity_op-15"><h3>Shared conditions for this topic · Are other controllers or namespaces affected?</h3><p>Deleting a group cascades through sets/namespaces; deleting a set removes its namespaces across all paths. Account namespace allocation in its containing resource layer.</p></article>
<article id="common-command-8"><h3>Command completion, events and records · How are DNR and More set?</h3><p>For a CQE, DNR=1 means the identical command is expected to fail if resubmitted to any controller in this subsystem; DNR=0 means it may succeed. Do not assign DNR=1 solely from an error name unless that condition mandates it. More=1 identifies additional information for this command in the Error Information Log. DNR should be zero when SCT=SC=0.</p></article>
</section>
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
