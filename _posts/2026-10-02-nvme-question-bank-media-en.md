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
<main id="content"><p class="qr-eyebrow">BASE 2.4 / NVM 1.3 / PCIe 1.4 · Q1–320</p>
<header><p class="qa-range">Q268–Q275</p><h1>Domains, reclaim groups and media units</h1><p class="qr-intro">Distinguish ownership from FDP placement, then follow identifiers to an RU and interpret media-report limits.</p><p>Practice first, then reveal 17 answer items per question. All numerical examples are hypothetical. Status is written SCT/SC; h indicates hexadecimal.</p></header>
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
<article class="qa-question" id="q-268" data-question="268"><h2><a class="qa-qid" href="#q-268">Q268</a> Do domains, sets, groups, media units and namespaces form one hierarchy?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-268-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-268-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>These names represent management, endurance, capacity, logical addressing and data-placement views.</p>
</li>
<li id="q-268-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>With sets, namespace→set→endurance group→domain is ownership; a reclaim group is not another namespace container inserted into that chain.</p>
</li>
<li id="q-268-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Read capabilities, inventories, namespace membership and FDP configurations.</p>
</li>
<li id="q-268-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>A media unit is a reported media-information entity; an FDP reclaim unit is a reclamation entity, not necessarily the same object.</p>
</li>
<li id="q-268-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Draw ownership separately from placement-handle selection; they answer membership and placement respectively.</p>
</li>
<li id="q-268-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Explain both ownership and placement without inventing one-to-one mappings.</p>
</li>
<li id="q-268-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>A media unit is not guaranteed to be a die, nor is channel membership universally one-to-one.</p>
</li>
<li id="q-268-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-268-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Reading a log does not itself require a new event. <a class="qa-rule-link" href="#common-log_query-9">Full rule in this volume</a></p>
</li>
<li id="q-268-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Get Log Page returns the selected data. <a class="qa-rule-link" href="#common-log_query-10">Full rule in this volume</a></p>
</li>
<li id="q-268-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>Get Log Page is not a per-read PEL audit trail. <a class="qa-rule-link" href="#common-log_query-11">Full rule in this volume</a></p>
</li>
<li id="q-268-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Controller Reset stops outstanding queries, which are reissued after Admin Queue recovery. <a class="qa-rule-link" href="#common-log_query-12">Full rule in this volume</a></p>
</li>
<li id="q-268-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>After subsystem reset, recover query access on affected controllers and re-read the logs. <a class="qa-rule-link" href="#common-log_query-13">Full rule in this volume</a></p>
</li>
<li id="q-268-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Reissue the query after a power cycle. <a class="qa-rule-link" href="#common-log_query-14">Full rule in this volume</a></p>
</li>
<li id="q-268-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Queries do not write namespace user data, but some reads acknowledge events or clear reported lists. <a class="qa-rule-link" href="#common-log_query-15">Full rule in this volume</a></p>
</li>
<li id="q-268-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Compare identifier definitions, scopes and observation times rather than numeric equality.</p>
</li>
<li id="q-268-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First label every edge as containment, ownership or a dynamic reference.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-capacitymodel">Base 2.4 §3.2.2–3.2.3, 3.8</a> · <a href="#ref-mediaunit">Base 2.4 §5.2.13.1.16</a> · <a href="#ref-fdpmodel">Base 2.4 §3.2.4, 8.1.12</a> · <a href="#ref-fdpcontrol">Base 2.4 §5.2.13.1.29–5.2.13.1.32, 5.2.30.1.21–5.2.30.1.22, 7.3–7.4</a> · <a href="#ref-fdpnvm">NVM Command Set 1.3 §3.2, 4.1.4.6–4.1.4.7</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-idns">NVM Command Set 1.3 §4.1.5.1–4.1.5.4</a> · <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-ana">Base 2.4 §2.4.2, 8.1.1 (PCIe namespace access)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-269" data-question="269"><h2><a class="qa-qid" href="#q-269">Q269</a> How are domains and resource ownership discovered?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-269-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-269-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Establish the observation domain before interpreting resource and capacity inventories.</p>
</li>
<li id="q-269-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>A domain can contain no controller or no endurance group; visible controllers do not enumerate all domains.</p>
</li>
<li id="q-269-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Read MDS, controller domain information and domain/group/set inventories.</p>
</li>
<li id="q-269-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>Namespace membership and media-unit DID/group/set fields provide complementary ownership views.</p>
</li>
<li id="q-269-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Enumerate valid domains and resources, preserving controller and DID with each observation.</p>
</li>
<li id="q-269-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>A joined view identifies the namespace’s group and the domain owning the reported capacity.</p>
</li>
<li id="q-269-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>LID 10h DID0 selects the controller’s domain; an invalid nonzero DID requires Invalid Field.</p>
</li>
<li id="q-269-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-269-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Reading a log does not itself require a new event. <a class="qa-rule-link" href="#common-log_query-9">Full rule in this volume</a></p>
</li>
<li id="q-269-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Get Log Page returns the selected data. <a class="qa-rule-link" href="#common-log_query-10">Full rule in this volume</a></p>
</li>
<li id="q-269-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>Get Log Page is not a per-read PEL audit trail. <a class="qa-rule-link" href="#common-log_query-11">Full rule in this volume</a></p>
</li>
<li id="q-269-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Controller Reset stops outstanding queries, which are reissued after Admin Queue recovery. <a class="qa-rule-link" href="#common-log_query-12">Full rule in this volume</a></p>
</li>
<li id="q-269-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>After subsystem reset, recover query access on affected controllers and re-read the logs. <a class="qa-rule-link" href="#common-log_query-13">Full rule in this volume</a></p>
</li>
<li id="q-269-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Reissue the query after a power cycle. <a class="qa-rule-link" href="#common-log_query-14">Full rule in this volume</a></p>
</li>
<li id="q-269-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Queries do not write namespace user data, but some reads acknowledge events or clear reported lists. <a class="qa-rule-link" href="#common-log_query-15">Full rule in this volume</a></p>
</li>
<li id="q-269-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Interpret zero with MDS and distinguish unavailable cross-domain information from absent resources.</p>
</li>
<li id="q-269-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First check the endpoint and domain selector.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-capacitymodel">Base 2.4 §3.2.2–3.2.3, 3.8</a> · <a href="#ref-mediaunit">Base 2.4 §5.2.13.1.16</a> · <a href="#ref-fdpmodel">Base 2.4 §3.2.4, 8.1.12</a> · <a href="#ref-fdpcontrol">Base 2.4 §5.2.13.1.29–5.2.13.1.32, 5.2.30.1.21–5.2.30.1.22, 7.3–7.4</a> · <a href="#ref-fdpnvm">NVM Command Set 1.3 §3.2, 4.1.4.6–4.1.4.7</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-idns">NVM Command Set 1.3 §4.1.5.1–4.1.5.4</a> · <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-ana">Base 2.4 §2.4.2, 8.1.1 (PCIe namespace access)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-270" data-question="270"><h2><a class="qa-qid" href="#q-270">Q270</a> What are a reclaim group, reclaim unit and reclaim-unit handle?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-270-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-270-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>FDP conveys placement intent while the controller manages reclamation and active-RU replacement.</p>
</li>
<li id="q-270-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>FDP configuration is endurance-group scoped; RG/RUH identifiers belong to that configuration.</p>
</li>
<li id="q-270-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Read configuration counts/descriptors and the enabled configuration through FID 1Dh.</p>
</li>
<li id="q-270-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>An RG contains RUs; each RUH references one RU in every RG, while an RU has at most one current RUH reference.</p>
</li>
<li id="q-270-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Select RG and placement handle, map to RUH, and let the controller replace a full RU within that RG.</p>
</li>
<li id="q-270-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Example: RUH2 references one RU in RG0 and another in RG1; RUH2 alone does not select between them.</p>
</li>
<li id="q-270-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Initially and persistently isolated handles have different reclamation mixing requirements.</p>
</li>
<li id="q-270-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-270-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Reading a log does not itself require a new event. <a class="qa-rule-link" href="#common-log_query-9">Full rule in this volume</a></p>
</li>
<li id="q-270-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Get Log Page returns the selected data. <a class="qa-rule-link" href="#common-log_query-10">Full rule in this volume</a></p>
</li>
<li id="q-270-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>Get Log Page is not a per-read PEL audit trail. <a class="qa-rule-link" href="#common-log_query-11">Full rule in this volume</a></p>
</li>
<li id="q-270-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Controller Reset stops outstanding queries, which are reissued after Admin Queue recovery. <a class="qa-rule-link" href="#common-log_query-12">Full rule in this volume</a></p>
</li>
<li id="q-270-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>After subsystem reset, recover query access on affected controllers and re-read the logs. <a class="qa-rule-link" href="#common-log_query-13">Full rule in this volume</a></p>
</li>
<li id="q-270-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Reissue the query after a power cycle. <a class="qa-rule-link" href="#common-log_query-14">Full rule in this volume</a></p>
</li>
<li id="q-270-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Queries do not write namespace user data, but some reads acknowledge events or clear reported lists. <a class="qa-rule-link" href="#common-log_query-15">Full rule in this volume</a></p>
</li>
<li id="q-270-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Correlate configuration, RG, handle type and state; a stable RUH ID does not imply a fixed RU reference.</p>
</li>
<li id="q-270-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First check whether a handle was mistaken for a physical RU address.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-capacitymodel">Base 2.4 §3.2.2–3.2.3, 3.8</a> · <a href="#ref-mediaunit">Base 2.4 §5.2.13.1.16</a> · <a href="#ref-fdpmodel">Base 2.4 §3.2.4, 8.1.12</a> · <a href="#ref-fdpcontrol">Base 2.4 §5.2.13.1.29–5.2.13.1.32, 5.2.30.1.21–5.2.30.1.22, 7.3–7.4</a> · <a href="#ref-fdpnvm">NVM Command Set 1.3 §3.2, 4.1.4.6–4.1.4.7</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-idns">NVM Command Set 1.3 §4.1.5.1–4.1.5.4</a> · <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-ana">Base 2.4 §2.4.2, 8.1.1 (PCIe namespace access)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-271" data-question="271"><h2><a class="qa-qid" href="#q-271">Q271</a> How does a namespace select an RU through a placement handle?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-271-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-271-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>A namespace’s placement-handle list maps write placement intent to group-level RUHs.</p>
</li>
<li id="q-271-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>The same PH can map differently across namespaces, while sharing RUHs is possible under configuration constraints.</p>
</li>
<li id="q-271-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Read namespace handle mapping, configuration and RUH status.</p>
</li>
<li id="q-271-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>FDP writes use DTYPE02h and a DSPEC PID encoding RGID plus PH, not a raw RUH ID.</p>
</li>
<li id="q-271-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Decode PID, map PH to RUH and select that handle’s current RU in the chosen RG.</p>
</li>
<li id="q-271-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>If NS1 PH0 maps to RUH2 and PID selects RG1, placement uses RUH2&#x27;s current RU in RG1.</p>
</li>
<li id="q-271-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Invalid write PID requires fallback placement and enabled-event handling; invalid RUH Update selectors do not use that fallback rule.</p>
</li>
<li id="q-271-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-271-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Reading a log does not itself require a new event. <a class="qa-rule-link" href="#common-log_query-9">Full rule in this volume</a></p>
</li>
<li id="q-271-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Get Log Page returns the selected data. <a class="qa-rule-link" href="#common-log_query-10">Full rule in this volume</a></p>
</li>
<li id="q-271-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>Get Log Page is not a per-read PEL audit trail. <a class="qa-rule-link" href="#common-log_query-11">Full rule in this volume</a></p>
</li>
<li id="q-271-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Controller Reset stops outstanding queries, which are reissued after Admin Queue recovery. <a class="qa-rule-link" href="#common-log_query-12">Full rule in this volume</a></p>
</li>
<li id="q-271-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>After subsystem reset, recover query access on affected controllers and re-read the logs. <a class="qa-rule-link" href="#common-log_query-13">Full rule in this volume</a></p>
</li>
<li id="q-271-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Reissue the query after a power cycle. <a class="qa-rule-link" href="#common-log_query-14">Full rule in this volume</a></p>
</li>
<li id="q-271-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Queries do not write namespace user data, but some reads acknowledge events or clear reported lists. <a class="qa-rule-link" href="#common-log_query-15">Full rule in this volume</a></p>
</li>
<li id="q-271-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Writes without the directive use PH0 and a controller-selected RG, not a bypass of FDP configuration.</p>
</li>
<li id="q-271-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First verify PID decoding and the namespace-specific PH-to-RUH mapping.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-capacitymodel">Base 2.4 §3.2.2–3.2.3, 3.8</a> · <a href="#ref-mediaunit">Base 2.4 §5.2.13.1.16</a> · <a href="#ref-fdpmodel">Base 2.4 §3.2.4, 8.1.12</a> · <a href="#ref-fdpcontrol">Base 2.4 §5.2.13.1.29–5.2.13.1.32, 5.2.30.1.21–5.2.30.1.22, 7.3–7.4</a> · <a href="#ref-fdpnvm">NVM Command Set 1.3 §3.2, 4.1.4.6–4.1.4.7</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-idns">NVM Command Set 1.3 §4.1.5.1–4.1.5.4</a> · <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-ana">Base 2.4 §2.4.2, 8.1.1 (PCIe namespace access)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-272" data-question="272"><h2><a class="qa-qid" href="#q-272">Q272</a> What does Media Unit Status report and how are descriptors traversed?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-272-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-272-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>This log reports domain media ownership, adjustment and wear, not per-I/O completion.</p>
</li>
<li id="q-272-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>LID 10h selects a domain; media-unit and channel identifiers are domain-local.</p>
</li>
<li id="q-272-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Check log/domain support and header counts/configuration.</p>
</li>
<li id="q-272-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>Descriptors provide identity, ownership, adjustment, spare/wear and channel-list location/count.</p>
</li>
<li id="q-272-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Locate the channel list at CIO and read MUCS two-byte IDs; applicable descriptor length is CIO plus list length, not a universal fixed stride.</p>
</li>
<li id="q-272-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Parse ordered IDs; CCHANS0 means the common-channel count is unreported, not no channels exist.</p>
</li>
<li id="q-272-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Cleared capacity configuration has specified zero fields and is not an ordinary populated configuration.</p>
</li>
<li id="q-272-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-272-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Reading a log does not itself require a new event. <a class="qa-rule-link" href="#common-log_query-9">Full rule in this volume</a></p>
</li>
<li id="q-272-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Get Log Page returns the selected data. <a class="qa-rule-link" href="#common-log_query-10">Full rule in this volume</a></p>
</li>
<li id="q-272-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>Get Log Page is not a per-read PEL audit trail. <a class="qa-rule-link" href="#common-log_query-11">Full rule in this volume</a></p>
</li>
<li id="q-272-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Controller Reset stops outstanding queries, which are reissued after Admin Queue recovery. <a class="qa-rule-link" href="#common-log_query-12">Full rule in this volume</a></p>
</li>
<li id="q-272-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>After subsystem reset, recover query access on affected controllers and re-read the logs. <a class="qa-rule-link" href="#common-log_query-13">Full rule in this volume</a></p>
</li>
<li id="q-272-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Reissue the query after a power cycle. <a class="qa-rule-link" href="#common-log_query-14">Full rule in this volume</a></p>
</li>
<li id="q-272-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Queries do not write namespace user data, but some reads acknowledge events or clear reported lists. <a class="qa-rule-link" href="#common-log_query-15">Full rule in this volume</a></p>
</li>
<li id="q-272-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>The specification does not define group health as a simple average of media-unit values.</p>
</li>
<li id="q-272-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First check domain selection and descriptor boundaries.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-capacitymodel">Base 2.4 §3.2.2–3.2.3, 3.8</a> · <a href="#ref-mediaunit">Base 2.4 §5.2.13.1.16</a> · <a href="#ref-fdpmodel">Base 2.4 §3.2.4, 8.1.12</a> · <a href="#ref-fdpcontrol">Base 2.4 §5.2.13.1.29–5.2.13.1.32, 5.2.30.1.21–5.2.30.1.22, 7.3–7.4</a> · <a href="#ref-fdpnvm">NVM Command Set 1.3 §3.2, 4.1.4.6–4.1.4.7</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-idns">NVM Command Set 1.3 §4.1.5.1–4.1.5.4</a> · <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-ana">Base 2.4 §2.4.2, 8.1.1 (PCIe namespace access)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-273" data-question="273"><h2><a class="qa-qid" href="#q-273">Q273</a> Can Media Unit Status directly establish namespace unavailability?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-273-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-273-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>The original premise assumes a universal media-unavailable-to-namespace-ready mapping that LID 10h does not provide.</p>
</li>
<li id="q-273-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Media wear, namespace accessibility and controller-path availability are distinct observations.</p>
</li>
<li id="q-273-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Combine membership, controller readiness, applicable ANA and command results, using media-unit data as context.</p>
</li>
<li id="q-273-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>Percentage used estimates endurance consumption and spare reports reserve; neither directly encodes Namespace Not Ready.</p>
</li>
<li id="q-273-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Establish attachment/path access, inspect a valid command’s failure and then correlate media ownership.</p>
</li>
<li id="q-273-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Percentage used above 100 does not require all I/O to fail.</p>
</li>
<li id="q-273-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Namespace Not Ready, ANA Inaccessible and media errors have different conditions and statuses.</p>
</li>
<li id="q-273-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-273-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Reading a log does not itself require a new event. <a class="qa-rule-link" href="#common-log_query-9">Full rule in this volume</a></p>
</li>
<li id="q-273-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Get Log Page returns the selected data. <a class="qa-rule-link" href="#common-log_query-10">Full rule in this volume</a></p>
</li>
<li id="q-273-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>Get Log Page is not a per-read PEL audit trail. <a class="qa-rule-link" href="#common-log_query-11">Full rule in this volume</a></p>
</li>
<li id="q-273-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Controller Reset stops outstanding queries, which are reissued after Admin Queue recovery. <a class="qa-rule-link" href="#common-log_query-12">Full rule in this volume</a></p>
</li>
<li id="q-273-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>After subsystem reset, recover query access on affected controllers and re-read the logs. <a class="qa-rule-link" href="#common-log_query-13">Full rule in this volume</a></p>
</li>
<li id="q-273-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Reissue the query after a power cycle. <a class="qa-rule-link" href="#common-log_query-14">Full rule in this volume</a></p>
</li>
<li id="q-273-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Queries do not write namespace user data, but some reads acknowledge events or clear reported lists. <a class="qa-rule-link" href="#common-log_query-15">Full rule in this volume</a></p>
</li>
<li id="q-273-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Correlate shared resources for simultaneous failures without treating coincidence as proof.</p>
</li>
<li id="q-273-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First preserve completion status and namespace-path state.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-capacitymodel">Base 2.4 §3.2.2–3.2.3, 3.8</a> · <a href="#ref-mediaunit">Base 2.4 §5.2.13.1.16</a> · <a href="#ref-fdpmodel">Base 2.4 §3.2.4, 8.1.12</a> · <a href="#ref-fdpcontrol">Base 2.4 §5.2.13.1.29–5.2.13.1.32, 5.2.30.1.21–5.2.30.1.22, 7.3–7.4</a> · <a href="#ref-fdpnvm">NVM Command Set 1.3 §3.2, 4.1.4.6–4.1.4.7</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-idns">NVM Command Set 1.3 §4.1.5.1–4.1.5.4</a> · <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-ana">Base 2.4 §2.4.2, 8.1.1 (PCIe namespace access)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-274" data-question="274"><h2><a class="qa-qid" href="#q-274">Q274</a> Which notices and records can accompany media changes?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-274-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-274-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>There is no generic AER for every media-unit field change; classify health, ANA, namespace or FDP changes first.</p>
</li>
<li id="q-274-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Warnings can be group, subsystem or controller-path scoped and are not interchangeable.</p>
</li>
<li id="q-274-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Read AEC, group-health and FDP-event enables with capability bits.</p>
</li>
<li id="q-274-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>Health logs report warnings, ANA reports paths and FDP logs enabled placement events.</p>
</li>
<li id="q-274-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Preserve AER type/information/LID, then read the matching log with RAE1 when retention is needed.</p>
</li>
<li id="q-274-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>A group spare warning calls for EGCW and configured aggregate notice, not an invented Media Unit Lost event.</p>
</li>
<li id="q-274-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Before declaring a missing event, check enables, pending AERs, prior acknowledgments and qualifying conditions.</p>
</li>
<li id="q-274-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-274-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Reading a log does not itself require a new event. <a class="qa-rule-link" href="#common-log_query-9">Full rule in this volume</a></p>
</li>
<li id="q-274-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Get Log Page returns the selected data. <a class="qa-rule-link" href="#common-log_query-10">Full rule in this volume</a></p>
</li>
<li id="q-274-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>Get Log Page is not a per-read PEL audit trail. <a class="qa-rule-link" href="#common-log_query-11">Full rule in this volume</a></p>
</li>
<li id="q-274-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Controller Reset stops outstanding queries, which are reissued after Admin Queue recovery. <a class="qa-rule-link" href="#common-log_query-12">Full rule in this volume</a></p>
</li>
<li id="q-274-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>After subsystem reset, recover query access on affected controllers and re-read the logs. <a class="qa-rule-link" href="#common-log_query-13">Full rule in this volume</a></p>
</li>
<li id="q-274-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Reissue the query after a power cycle. <a class="qa-rule-link" href="#common-log_query-14">Full rule in this volume</a></p>
</li>
<li id="q-274-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Queries do not write namespace user data, but some reads acknowledge events or clear reported lists. <a class="qa-rule-link" href="#common-log_query-15">Full rule in this volume</a></p>
</li>
<li id="q-274-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>PEL records supported qualifying events, not every percentage-used update.</p>
</li>
<li id="q-274-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First specify the actual field transition before selecting an event rule.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-capacitymodel">Base 2.4 §3.2.2–3.2.3, 3.8</a> · <a href="#ref-mediaunit">Base 2.4 §5.2.13.1.16</a> · <a href="#ref-fdpmodel">Base 2.4 §3.2.4, 8.1.12</a> · <a href="#ref-fdpcontrol">Base 2.4 §5.2.13.1.29–5.2.13.1.32, 5.2.30.1.21–5.2.30.1.22, 7.3–7.4</a> · <a href="#ref-fdpnvm">NVM Command Set 1.3 §3.2, 4.1.4.6–4.1.4.7</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-idns">NVM Command Set 1.3 §4.1.5.1–4.1.5.4</a> · <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-ana">Base 2.4 §2.4.2, 8.1.1 (PCIe namespace access)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-275" data-question="275"><h2><a class="qa-qid" href="#q-275">Q275</a> How are entity scopes distinguished without confusing identifiers?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-275-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-275-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>The same number can identify a namespace, domain, group or reclaim group; field type and enclosing scope are essential.</p>
</li>
<li id="q-275-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Command endpoint, configuration scope and data ownership can differ.</p>
</li>
<li id="q-275-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Establish command/feature scope before resolving identifiers through inventories.</p>
</li>
<li id="q-275-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>Record applicable endpoint, domain, group, namespace and selectors without inventing zero IDs for inapplicable fields.</p>
</li>
<li id="q-275-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Ask who receives it, who is targeted and who shares the effects before cross-controller comparison.</p>
</li>
<li id="q-275-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>FID 1Dh is group-scoped while namespaces retain distinct placement-handle mappings.</p>
</li>
<li id="q-275-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Absent IDs, unsupported functionality and inaccessible cross-domain information are distinct conditions.</p>
</li>
<li id="q-275-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-275-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Reading a log does not itself require a new event. <a class="qa-rule-link" href="#common-log_query-9">Full rule in this volume</a></p>
</li>
<li id="q-275-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Get Log Page returns the selected data. <a class="qa-rule-link" href="#common-log_query-10">Full rule in this volume</a></p>
</li>
<li id="q-275-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>Get Log Page is not a per-read PEL audit trail. <a class="qa-rule-link" href="#common-log_query-11">Full rule in this volume</a></p>
</li>
<li id="q-275-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Controller Reset stops outstanding queries, which are reissued after Admin Queue recovery. <a class="qa-rule-link" href="#common-log_query-12">Full rule in this volume</a></p>
</li>
<li id="q-275-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>After subsystem reset, recover query access on affected controllers and re-read the logs. <a class="qa-rule-link" href="#common-log_query-13">Full rule in this volume</a></p>
</li>
<li id="q-275-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Reissue the query after a power cycle. <a class="qa-rule-link" href="#common-log_query-14">Full rule in this volume</a></p>
</li>
<li id="q-275-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Queries do not write namespace user data, but some reads acknowledge events or clear reported lists. <a class="qa-rule-link" href="#common-log_query-15">Full rule in this volume</a></p>
</li>
<li id="q-275-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Compare matching selectors/times and rediscover after ownership changes.</p>
</li>
<li id="q-275-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First qualify every bare number with its field and enclosing scope.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-capacitymodel">Base 2.4 §3.2.2–3.2.3, 3.8</a> · <a href="#ref-mediaunit">Base 2.4 §5.2.13.1.16</a> · <a href="#ref-fdpmodel">Base 2.4 §3.2.4, 8.1.12</a> · <a href="#ref-fdpcontrol">Base 2.4 §5.2.13.1.29–5.2.13.1.32, 5.2.30.1.21–5.2.30.1.22, 7.3–7.4</a> · <a href="#ref-fdpnvm">NVM Command Set 1.3 §3.2, 4.1.4.6–4.1.4.7</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-idns">NVM Command Set 1.3 §4.1.5.1–4.1.5.4</a> · <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-ana">Base 2.4 §2.4.2, 8.1.1 (PCIe namespace access)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<section id="common-rules" class="qa-common"><h2>Shared rules linked from the answers</h2><p>Each shared mechanism is explained in full once in this volume. Use browser Back to return to the question; explicit command or feature exceptions take precedence.</p>
<article id="common-command-8"><h3>Command completion, events and records · How are DNR and More set?</h3><p>For a CQE, DNR=1 means the identical command is expected to fail if resubmitted to any controller in this subsystem; DNR=0 means it may succeed. Do not assign DNR=1 solely from an error name unless that condition mandates it. More=1 identifies additional information for this command in the Error Information Log. DNR should be zero when SCT=SC=0.</p></article>
<article id="common-log_query-9"><h3>Shared conditions for this topic · Is an asynchronous event generated?</h3><p>Reading a log does not itself require a new event. A successful RAE=0 read may acknowledge its event; RAE=1 and unsuccessful reads retain it. Immediate and One-Shot events have separate clearing rules.</p></article>
<article id="common-log_query-10"><h3>Shared conditions for this topic · Are Error Information or other logs updated?</h3><p>Get Log Page returns the selected data. Reads can clear reported changes or acknowledge events, depending on the log and RAE, so preserve comparison evidence first. A successful read does not require an error entry; failed reads follow CQE and error-log rules.</p></article>
<article id="common-log_query-11"><h3>Shared conditions for this topic · Is it recorded in the Persistent Event Log?</h3><p>Get Log Page is not a per-read PEL audit trail. Reading PEL does not create another such event; separately occurring events follow their supported logging conditions.</p></article>
<article id="common-log_query-12"><h3>Shared conditions for this topic · What survives or continues after Controller Reset?</h3><p>Controller Reset stops outstanding queries, which are reissued after Admin Queue recovery. Content retention is separate: Error Information entries should clear but Error Count persists; SMART cumulative information and PEL follow their field-specific persistence rules.</p></article>
<article id="common-log_query-13"><h3>Shared conditions for this topic · What survives or continues after NVM Subsystem Reset?</h3><p>After subsystem reset, recover query access on affected controllers and re-read the logs. This is not restoration of manufacturing defaults; Figure 209’s Restore to Default Content column is not an ordinary reset-retention table.</p></article>
<article id="common-log_query-14"><h3>Shared conditions for this topic · What survives or continues after a power cycle?</h3><p>Reissue the query after a power cycle. SMART lifetime information and PEL have persistent content; Error Information entries should clear while the cumulative Error Count persists. Reassess current temperature, active operations and reporting contexts under their own rules rather than expecting every byte to remain fixed.</p></article>
<article id="common-log_query-15"><h3>Shared conditions for this topic · Are other controllers or namespaces affected?</h3><p>Queries do not write namespace user data, but some reads acknowledge events or clear reported lists. Logs have controller, namespace, domain or subsystem scopes; track readers and acknowledgment times when several hosts share the view.</p></article>
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
