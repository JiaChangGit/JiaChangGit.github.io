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
<main id="content"><p class="qr-eyebrow">BASE 2.4 / NVM 1.3 / PCIe 1.4 · Q1–68</p>
<header><p class="qa-range">Q54–Q68</p><h1>Get Features and Set Features</h1><p class="qr-intro">Establish scope, changeability and saveability before Set. Completion, Current readback, actual behavior and restoration after reset are separate observations; a successful CQE does not replace them.</p><p>Practice first, then reveal 17 answer items per question. All numerical examples are hypothetical. Status is written SCT/SC; h indicates hexadecimal.</p></header>
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
<article class="qa-question" id="q-054" data-question="54"><h2><a class="qa-qid" href="#q-054">Q54</a> What do Current, Default, Saved and Supported Capabilities mean?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-054-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-054-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Separate the active value, manufacturing default, saved value and change/save capabilities; these are not four identical settings.</p>
</li>
<li id="q-054-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Compare the same FID, scope and selectors; Current can differ across namespaces.</p>
</li>
<li id="q-054-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>ONCS.SSFS advertises Save/Select support. Under that mechanism, Get Features.SEL=3 returns CHANG/NSSPEC/SVBL for the FID.</p>
</li>
<li id="q-054-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>SEL 0/1/2/3 select Current/Default/Saved/Supported Capabilities. With SEL 3, DW0 bits 2/1/0 are CHANG/NSSPEC/SVBL, not operational values.</p>
</li>
<li id="q-054-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Read capabilities and Current first, then Saved/Default for reset analysis. If unsaveable or never saved, SEL 2 returns Default, subject to features that define no Default.</p>
</li>
<li id="q-054-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>SEL 3 result 5 means changeable, saveable and NSSPEC=0, not Current=5. NSSPEC=0 alone does not establish controller scope.</p>
</li>
<li id="q-054-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Unsupported FID uses Invalid Field (0/02h); SEL 4–7 are reserved. Without Select support, do not treat a response as valid CHANG/SVBL discovery.</p>
</li>
<li id="q-054-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-054-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Normal completion here does not guarantee an AER; a separate defined event requires support, configuration and a pending request. <a class="qa-rule-link" href="#common-command-9">Full rule in this volume</a></p>
</li>
<li id="q-054-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Correlate the completion with error records under the shared entry-creation rules; do not infer entry count directly from the number of failures. <a class="qa-rule-link" href="#common-command-10">Full rule in this volume</a></p>
</li>
<li id="q-054-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>Get does not itself produce a Set Feature event; Set requires FID logging support, successful completion and a check for a changed setting. <a class="qa-rule-link" href="#common-feature_events-11">Full rule in this volume</a></p>
</li>
<li id="q-054-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Use scope, saveability and reset coverage; whole-subsystem and partial resets differ. <a class="qa-rule-link" href="#common-feature-12">Full rule in this volume</a></p>
</li>
<li id="q-054-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Establish whole or partial subsystem coverage; non-saveable persistent values do not thereby become zero. <a class="qa-rule-link" href="#common-feature-13">Full rule in this volume</a></p>
</li>
<li id="q-054-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Saveable values restore Saved; non-saveable values require their persistence and feature-specific rules. <a class="qa-rule-link" href="#common-feature-14">Full rule in this volume</a></p>
</li>
<li id="q-054-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Feature scope determines whether other controllers or namespaces share the setting. <a class="qa-rule-link" href="#common-feature-15">Full rule in this volume</a></p>
</li>
<li id="q-054-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Preserve FID and SEL with the returned DW0 to distinguish a value from a capability bitmap.</p>
</li>
<li id="q-054-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First check SEL before concluding that Set failed to take effect.</p>
</li>
</ol><details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-getfeat">Base 2.4 §5.2.12</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-featureeffects">Base 2.4 §5.2.13.1.18</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-055" data-question="55"><h2><a class="qa-qid" href="#q-055">Q55</a> How does Set Features.Save affect values after reset and power cycling?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-055-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-055-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Let the host change only the active value or also the persistent value used on restoration.</p>
</li>
<li id="q-055-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Saving follows feature scope; namespace-scoped and controller-scoped settings are not one global value.</p>
</li>
<li id="q-055-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Check ONCS.SSFS and the FID&#x27;s SVBL. Controller Save support does not make every feature saveable.</p>
</li>
<li id="q-055-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>SV=0 changes Current without updating Saved; successful SV=1 updates both. Default does not become the host&#x27;s chosen value.</p>
</li>
<li id="q-055-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Discover support, Set and await completion, then read Current/Saved separately. After the chosen reset, verify Current under scope and exception rules.</p>
</li>
<li id="q-055-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>With Saved=A and an SV=0 change to B, Current becomes B; a reset that restores Saved returns it to A, not B.</p>
</li>
<li id="q-055-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>SV=1 for an unsaveable feature shall return Feature Identifier Not Saveable (1/0Dh), not silently succeed and lose the saved setting.</p>
</li>
<li id="q-055-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-055-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Normal completion here does not guarantee an AER; a separate defined event requires support, configuration and a pending request. <a class="qa-rule-link" href="#common-command-9">Full rule in this volume</a></p>
</li>
<li id="q-055-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Correlate the completion with error records under the shared entry-creation rules; do not infer entry count directly from the number of failures. <a class="qa-rule-link" href="#common-command-10">Full rule in this volume</a></p>
</li>
<li id="q-055-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>Get does not itself produce a Set Feature event; Set requires FID logging support, successful completion and a check for a changed setting. <a class="qa-rule-link" href="#common-feature_events-11">Full rule in this volume</a></p>
</li>
<li id="q-055-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Use scope, saveability and reset coverage; whole-subsystem and partial resets differ. <a class="qa-rule-link" href="#common-feature-12">Full rule in this volume</a></p>
</li>
<li id="q-055-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Establish whole or partial subsystem coverage; non-saveable persistent values do not thereby become zero. <a class="qa-rule-link" href="#common-feature-13">Full rule in this volume</a></p>
</li>
<li id="q-055-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Saveable values restore Saved; non-saveable values require their persistence and feature-specific rules. <a class="qa-rule-link" href="#common-feature-14">Full rule in this volume</a></p>
</li>
<li id="q-055-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Feature scope determines whether other controllers or namespaces share the setting. <a class="qa-rule-link" href="#common-feature-15">Full rule in this volume</a></p>
</li>
<li id="q-055-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Save success, active application and restoration are three separate checks. Current=B does not establish Saved=B.</p>
</li>
<li id="q-055-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First inspect original SV/SVBL, then reset type and coverage.</p>
</li>
</ol><details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-getfeat">Base 2.4 §5.2.12</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-featureeffects">Base 2.4 §5.2.13.1.18</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-056" data-question="56"><h2><a class="qa-qid" href="#q-056">Q56</a> Which errors apply to unsupported features, invalid values and unsupported Save?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-056-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-056-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Distinguish unsupported function, unchangeability, unsaveability and invalid value; their causes and corrections differ.</p>
</li>
<li id="q-056-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Evaluate the FID, target scope, current state and this Get/Set operation, not merely the controller model.</p>
</li>
<li id="q-056-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>SEL 3 capabilities require SSFS. CHANG=1 means some values are changeable, not that a current permanent state can be reversed.</p>
</li>
<li id="q-056-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>Check FID, SV, NSID, CDW11 and payload. Some features require selectors beyond a single value.</p>
</li>
<li id="q-056-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Establish a valid baseline, then separately test unsupported FID, bad values, SV=1 and wrong scope.</p>
</li>
<li id="q-056-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Successful Set establishes completion. Setting an unchangeable feature to its existing value may succeed or return Feature Not Changeable; both are permitted.</p>
</li>
<li id="q-056-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Unsupported FID/invalid defined value:0/02h; unsaveable:1/0Dh; unchangeable:1/0Eh; controller-scoped Set with a valid NSID:1/0Fh. Specific FID ordering/state errors take precedence.</p>
</li>
<li id="q-056-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-056-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Normal completion here does not guarantee an AER; a separate defined event requires support, configuration and a pending request. <a class="qa-rule-link" href="#common-command-9">Full rule in this volume</a></p>
</li>
<li id="q-056-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Correlate the completion with error records under the shared entry-creation rules; do not infer entry count directly from the number of failures. <a class="qa-rule-link" href="#common-command-10">Full rule in this volume</a></p>
</li>
<li id="q-056-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>Get does not itself produce a Set Feature event; Set requires FID logging support, successful completion and a check for a changed setting. <a class="qa-rule-link" href="#common-feature_events-11">Full rule in this volume</a></p>
</li>
<li id="q-056-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Use scope, saveability and reset coverage; whole-subsystem and partial resets differ. <a class="qa-rule-link" href="#common-feature-12">Full rule in this volume</a></p>
</li>
<li id="q-056-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Establish whole or partial subsystem coverage; non-saveable persistent values do not thereby become zero. <a class="qa-rule-link" href="#common-feature-13">Full rule in this volume</a></p>
</li>
<li id="q-056-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Saveable values restore Saved; non-saveable values require their persistence and feature-specific rules. <a class="qa-rule-link" href="#common-feature-14">Full rule in this volume</a></p>
</li>
<li id="q-056-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Feature scope determines whether other controllers or namespaces share the setting. <a class="qa-rule-link" href="#common-feature-15">Full rule in this volume</a></p>
</li>
<li id="q-056-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Re-read after failure according to the feature&#x27;s error rules; an error is not a universal proof of no side effects.</p>
</li>
<li id="q-056-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First exclude multiple simultaneous faults that allow different valid error choices.</p>
</li>
</ol><details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-getfeat">Base 2.4 §5.2.12</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-featureeffects">Base 2.4 §5.2.13.1.18</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-057" data-question="57"><h2><a class="qa-qid" href="#q-057">Q57</a> How does the host determine whether a feature requires NSID?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-057-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-057-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Select the correct target before changing configuration.</p>
</li>
<li id="q-057-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Feature scope can be controller, namespace, subsystem, set, group or another management entity, not just two categories.</p>
</li>
<li id="q-057-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>SEL 3.NSSPEC=1 indicates namespace scope. With zero, inspect the feature-effects scope and Figure 466/NVM Figure 92.</p>
</li>
<li id="q-057-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>Controller-scoped Get/Set accepts NSID 0 or FFFFFFFFh. A valid namespace ID on Get can return the controller value, whereas Set must report the scope error.</p>
</li>
<li id="q-057-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Determine scope, then NSID and other selectors. Namespace scope normally uses an active NSID; broadcast Get/Set differ and multi-domain restrictions apply.</p>
</li>
<li id="q-057-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>FID 05h Error Recovery is namespace-scoped and FID 01h Arbitration controller-scoped; numeric CDW11 values do not make their NSID rules interchangeable.</p>
</li>
<li id="q-057-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Controller-scoped Set with a valid NSID returns 1/0Fh. Namespace-scoped Get with FFFFFFFFh generally returns 0/0Bh, subject to specific exceptions.</p>
</li>
<li id="q-057-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-057-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Normal completion here does not guarantee an AER; a separate defined event requires support, configuration and a pending request. <a class="qa-rule-link" href="#common-command-9">Full rule in this volume</a></p>
</li>
<li id="q-057-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Correlate the completion with error records under the shared entry-creation rules; do not infer entry count directly from the number of failures. <a class="qa-rule-link" href="#common-command-10">Full rule in this volume</a></p>
</li>
<li id="q-057-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>Get does not itself produce a Set Feature event; Set requires FID logging support, successful completion and a check for a changed setting. <a class="qa-rule-link" href="#common-feature_events-11">Full rule in this volume</a></p>
</li>
<li id="q-057-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Use scope, saveability and reset coverage; whole-subsystem and partial resets differ. <a class="qa-rule-link" href="#common-feature-12">Full rule in this volume</a></p>
</li>
<li id="q-057-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Establish whole or partial subsystem coverage; non-saveable persistent values do not thereby become zero. <a class="qa-rule-link" href="#common-feature-13">Full rule in this volume</a></p>
</li>
<li id="q-057-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Saveable values restore Saved; non-saveable values require their persistence and feature-specific rules. <a class="qa-rule-link" href="#common-feature-14">Full rule in this volume</a></p>
</li>
<li id="q-057-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Feature scope determines whether other controllers or namespaces share the setting. <a class="qa-rule-link" href="#common-feature-15">Full rule in this volume</a></p>
</li>
<li id="q-057-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>NSSPEC=0 can coexist with subsystem/set scope; it does not universally mean one controller value for all namespaces.</p>
</li>
<li id="q-057-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First read the scope definition and original NSID before suspecting namespace failure.</p>
</li>
</ol><details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-getfeat">Base 2.4 §5.2.12</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-nvmfeat">NVM Command Set 1.3 §4.1.3.1–4.1.3.7</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-featureeffects">Base 2.4 §5.2.13.1.18</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-058" data-question="58"><h2><a class="qa-qid" href="#q-058">Q58</a> How are Arbitration, Number of Queues and I/O Command Set Profile configured and checked?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-058-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-058-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>These control scheduling parameters, queue allocations and allowed command-set combinations at different initialization stages.</p>
</li>
<li id="q-058-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>All three target controller configuration, while Profile affects namespace/command-set usability.</p>
</li>
<li id="q-058-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Arbitration uses CAP.AMS/CC.AMS; queue allocation uses successful Set results; Profile requires CAP.CSS.IOCSS and CNS 1Ch vectors.</p>
</li>
<li id="q-058-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>FID 01h uses AB/HPW/MPW/LPW; FID 07h maps requested to allocated SQ/CQ counts; FID 19h.IOCSCI is a combination index.</p>
</li>
<li id="q-058-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Select the profile and discover namespaces, allocate queues and create CQs/SQs; verify arbitration parameters together with CC.AMS/QPRIO.</p>
</li>
<li id="q-058-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Read back the same FID/selectors. With CC.CSS other than 110b, Set FID 19h succeeds without effect; with 110b, the selected combination applies. Profile index 0 selects combination 0, not no command sets. FID 07h allocation is not instantiated queue count.</p>
</li>
<li id="q-058-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Setting FID 07h after queue creation returns 0/0Ch. With CC.CSS=110b, FID 19h shall return Combination Rejected if IOCSCI selects a zero-valued combination or an attached namespace uses an I/O command set absent from that combination. The supplied spec conflicts: Figure 104 lists Combination Rejected as 1/2Bh, Figure 554 as 1/15h. Preserve that discrepancy rather than declaring noncompliance from either table alone.</p>
</li>
<li id="q-058-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-058-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Normal completion here does not guarantee an AER; a separate defined event requires support, configuration and a pending request. <a class="qa-rule-link" href="#common-command-9">Full rule in this volume</a></p>
</li>
<li id="q-058-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Correlate the completion with error records under the shared entry-creation rules; do not infer entry count directly from the number of failures. <a class="qa-rule-link" href="#common-command-10">Full rule in this volume</a></p>
</li>
<li id="q-058-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>Get does not itself produce a Set Feature event; Set requires FID logging support, successful completion and a check for a changed setting. <a class="qa-rule-link" href="#common-feature_events-11">Full rule in this volume</a></p>
</li>
<li id="q-058-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Use scope, saveability and reset coverage; whole-subsystem and partial resets differ. <a class="qa-rule-link" href="#common-feature-12">Full rule in this volume</a></p>
</li>
<li id="q-058-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Establish whole or partial subsystem coverage; non-saveable persistent values do not thereby become zero. <a class="qa-rule-link" href="#common-feature-13">Full rule in this volume</a></p>
</li>
<li id="q-058-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Saveable values restore Saved; non-saveable values require their persistence and feature-specific rules. <a class="qa-rule-link" href="#common-feature-14">Full rule in this volume</a></p>
</li>
<li id="q-058-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Feature scope determines whether other controllers or namespaces share the setting. <a class="qa-rule-link" href="#common-feature-15">Full rule in this volume</a></p>
</li>
<li id="q-058-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Verify settings, creatable queue ranges and usable command sets independently.</p>
</li>
<li id="q-058-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First check whether queue allocation was attempted after I/O queue creation.</p>
</li>
</ol><details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-arbit">Base 2.4 §5.2.30.1.1</a> · <a href="#ref-number">Base 2.4 §5.2.30.1.5</a> · <a href="#ref-profile">Base 2.4 §5.2.30.1.18</a> · <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-setcomplete">Base 2.4 §5.2.30 (Command Completion)</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-featureeffects">Base 2.4 §5.2.13.1.18</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-059" data-question="59"><h2><a class="qa-qid" href="#q-059">Q59</a> How are interrupt coalescing and vector configuration set and verified?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-059-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-059-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Trade notification latency against interrupt overhead; posting a completion and generating an IRQ are different events.</p>
</li>
<li id="q-059-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>FID 08h controls I/O interrupt coalescing; FID 09h selects its application per vector. Admin CQ does not support coalescing.</p>
</li>
<li id="q-059-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Check CQ.IEN/IV, PCIe interrupt mode and masks. Feature support is required, while aggregation algorithms remain implementation-specific.</p>
</li>
<li id="q-059-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>FID 08h TIME uses 100 μs units and THR is zero-based; either zero implicitly disables coalescing. FID 09h uses IV/CD; CD=1 disables coalescing, not interrupts.</p>
</li>
<li id="q-059-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Associate a valid vector with a CQ before Set FID 09h. Set/read FID 08h and observe CQE timing alongside interrupts.</p>
</li>
<li id="q-059-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Settings can complete successfully without defining exact IRQ timing for every workload. PCIe makes parameter use implementation-specific and permits no coalescing implementation.</p>
</li>
<li id="q-059-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Invalid or unassociated IV in FID 09h should return Invalid Field (0/02h), unlike Create CQ&#x27;s Invalid Interrupt Vector (1/08h).</p>
</li>
<li id="q-059-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-059-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Normal completion here does not guarantee an AER; a separate defined event requires support, configuration and a pending request. <a class="qa-rule-link" href="#common-command-9">Full rule in this volume</a></p>
</li>
<li id="q-059-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Correlate the completion with error records under the shared entry-creation rules; do not infer entry count directly from the number of failures. <a class="qa-rule-link" href="#common-command-10">Full rule in this volume</a></p>
</li>
<li id="q-059-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>Get does not itself produce a Set Feature event; Set requires FID logging support, successful completion and a check for a changed setting. <a class="qa-rule-link" href="#common-feature_events-11">Full rule in this volume</a></p>
</li>
<li id="q-059-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Use scope, saveability and reset coverage; whole-subsystem and partial resets differ. <a class="qa-rule-link" href="#common-feature-12">Full rule in this volume</a></p>
</li>
<li id="q-059-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Establish whole or partial subsystem coverage; non-saveable persistent values do not thereby become zero. <a class="qa-rule-link" href="#common-feature-13">Full rule in this volume</a></p>
</li>
<li id="q-059-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Saveable values restore Saved; non-saveable values require their persistence and feature-specific rules. <a class="qa-rule-link" href="#common-feature-14">Full rule in this volume</a></p>
</li>
<li id="q-059-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Feature scope determines whether other controllers or namespaces share the setting. <a class="qa-rule-link" href="#common-feature-15">Full rule in this volume</a></p>
</li>
<li id="q-059-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Check readback, CQ mapping, masks and notification behavior. CD=1 does not override an MSI-X mask.</p>
</li>
<li id="q-059-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First distinguish disabling coalescing from masking interrupts.</p>
</li>
</ol><details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-irqfeat">Base 2.4 §5.2.30.2.1–5.2.30.2.2</a> · <a href="#ref-irq">PCIe Transport 1.4 §3.5</a> · <a href="#ref-create">Base 2.4 §5.3.1–5.3.2</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-featureeffects">Base 2.4 §5.2.13.1.18</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-060" data-question="60"><h2><a class="qa-qid" href="#q-060">Q60</a> What do Volatile Write Cache and Write Atomicity Normal control?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-060-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-060-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Separate persistence from atomicity: reaching nonvolatile storage is different from updating logical blocks as a defined unit.</p>
</li>
<li id="q-060-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>FID 06h controls controller volatile caching; FID 0Ah controls normal atomicity requirements, not the advertised namespace atomic units.</p>
</li>
<li id="q-060-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>VWC advertises cache presence; AWUN/AWUPF, namespace overrides and boundaries describe atomicity.</p>
</li>
<li id="q-060-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>With FID 06h.WCE=0, written user data must be persistent. FID 0Ah.DN=1 removes AWUN/NAWUN requirements while retaining AWUPF/NAWUPF.</p>
</li>
<li id="q-060-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Read capabilities/format, Set/Get, then compare allowed outcomes for Writes respecting units/boundaries. Drain first for a clean setting transition.</p>
</li>
<li id="q-060-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>WCE=0 does not make arbitrary-size writes atomic; DN=1 does not make completion persistent. The controls are not substitutes.</p>
</li>
<li id="q-060-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Get/Set FID 06h without volatile cache shall return Invalid Field (0/02h). Other conditions follow applicable command/namespace/atomicity rules.</p>
</li>
<li id="q-060-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-060-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Normal completion here does not guarantee an AER; a separate defined event requires support, configuration and a pending request. <a class="qa-rule-link" href="#common-command-9">Full rule in this volume</a></p>
</li>
<li id="q-060-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Correlate the completion with error records under the shared entry-creation rules; do not infer entry count directly from the number of failures. <a class="qa-rule-link" href="#common-command-10">Full rule in this volume</a></p>
</li>
<li id="q-060-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>Get does not itself produce a Set Feature event; Set requires FID logging support, successful completion and a check for a changed setting. <a class="qa-rule-link" href="#common-feature_events-11">Full rule in this volume</a></p>
</li>
<li id="q-060-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Use scope, saveability and reset coverage; whole-subsystem and partial resets differ. <a class="qa-rule-link" href="#common-feature-12">Full rule in this volume</a></p>
</li>
<li id="q-060-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Establish whole or partial subsystem coverage; non-saveable persistent values do not thereby become zero. <a class="qa-rule-link" href="#common-feature-13">Full rule in this volume</a></p>
</li>
<li id="q-060-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Saveable values restore Saved; non-saveable values require their persistence and feature-specific rules. <a class="qa-rule-link" href="#common-feature-14">Full rule in this volume</a></p>
</li>
<li id="q-060-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Feature scope determines whether other controllers or namespaces share the setting. <a class="qa-rule-link" href="#common-feature-15">Full rule in this volume</a></p>
</li>
<li id="q-060-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Correlate Current.WCE/DN with the effective atomic units. FUA requests persistence for a command without enlarging its atomic unit.</p>
</li>
<li id="q-060-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First identify whether the requirement is no torn update or survival of power loss.</p>
</li>
</ol><details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-vwc">Base 2.4 §5.2.30.1.4</a> · <a href="#ref-nvmfeat">NVM Command Set 1.3 §4.1.3.1–4.1.3.7</a> · <a href="#ref-nvmatomic">NVM Command Set 1.3 §2.1.2–2.1.4</a> · <a href="#ref-idns">NVM Command Set 1.3 §4.1.5.1–4.1.5.4</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-featureeffects">Base 2.4 §5.2.13.1.18</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-061" data-question="61"><h2><a class="qa-qid" href="#q-061">Q61</a> How does Asynchronous Event Configuration select reported events?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-061-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-061-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Select desired change notifications; configuration does not submit an event request on the host&#x27;s behalf.</p>
</li>
<li id="q-061-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>FID 0Bh configures controller notifications about state with various scopes.</p>
</li>
<li id="q-061-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>OAES advertises optional event support, with applicable health capabilities and NVM-specific bit definitions.</p>
</li>
<li id="q-061-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>CDW11 enable bits select notifications. AER completion AET/AEI/LID describes the event; it is not the same bitmap.</p>
</li>
<li id="q-061-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Discover support, Set the mask, post AER, observe a condition, read the event/log, acknowledge under its rules and replenish requests.</p>
</li>
<li id="q-061-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>A condition already true when enabled is also reported under this feature&#x27;s rules; reporting is not limited to later state changes.</p>
</li>
<li id="q-061-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Enabling an unsupported event shall return Invalid Field (0/02h). No outstanding AER can delay notification without being a Set Features error.</p>
</li>
<li id="q-061-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-061-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>This feature configures notifications, with event-specific conditions and clearing rules. FID 0Bh is not a universal switch for every Error event, and Get Features does not replenish AERs.</p>
</li>
<li id="q-061-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Correlate the completion with error records under the shared entry-creation rules; do not infer entry count directly from the number of failures. <a class="qa-rule-link" href="#common-command-10">Full rule in this volume</a></p>
</li>
<li id="q-061-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>Get does not itself produce a Set Feature event; Set requires FID logging support, successful completion and a check for a changed setting. <a class="qa-rule-link" href="#common-feature_events-11">Full rule in this volume</a></p>
</li>
<li id="q-061-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Use scope, saveability and reset coverage; whole-subsystem and partial resets differ. <a class="qa-rule-link" href="#common-feature-12">Full rule in this volume</a></p>
</li>
<li id="q-061-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Establish whole or partial subsystem coverage; non-saveable persistent values do not thereby become zero. <a class="qa-rule-link" href="#common-feature-13">Full rule in this volume</a></p>
</li>
<li id="q-061-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Saveable values restore Saved; non-saveable values require their persistence and feature-specific rules. <a class="qa-rule-link" href="#common-feature-14">Full rule in this volume</a></p>
</li>
<li id="q-061-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Feature scope determines whether other controllers or namespaces share the setting. <a class="qa-rule-link" href="#common-feature-15">Full rule in this volume</a></p>
</li>
<li id="q-061-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Correlate OAES, Current mask, pending requests and event masking. An enabled bit alone does not guarantee immediate delivery.</p>
</li>
<li id="q-061-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First check outstanding AERs and acknowledgement of prior events.</p>
</li>
</ol><details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-aec">Base 2.4 §5.2.30.1.6</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-nvmfeat">NVM Command Set 1.3 §4.1.3.1–4.1.3.7</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-featureeffects">Base 2.4 §5.2.13.1.18</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-062" data-question="62"><h2><a class="qa-qid" href="#q-062">Q62</a> How do Power Management, APST and Host Controlled Thermal Management differ?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-062-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-062-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Separate explicit host power-state selection, idle-driven automatic transitions and temperature-driven power/performance management.</p>
</li>
<li id="q-062-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Configuration targets a controller, while shared-domain controllers can interact in power behavior.</p>
</li>
<li id="q-062-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Read NPSS/power-state descriptors, APSTA, HCTMA and MNTMT/MXTMT.</p>
</li>
<li id="q-062-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>FID 02h selects PS and related limits. FID 0Ch.APSTE enables a 32-entry table with ITPT idle milliseconds in that state and ITPS targeting a nonoperational state. FID 10h TMT1/TMT2 use kelvins.</p>
</li>
<li id="q-062-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Discover states/latencies, select explicit PS or an APST table and separately set legal TMT1&lt;TMT2 when both are nonzero. Each new state uses its own idle-transition condition.</p>
</li>
<li id="q-062-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Successful FID 02h Set establishes the requested PS, but enabled APST may transition again. HCTM activity is not another host Power Management command.</p>
</li>
<li id="q-062-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Unsupported states, invalid APST targets and illegal thermal ranges/order follow the relevant Invalid Field (0/02h) requirements.</p>
</li>
<li id="q-062-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-062-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Normal completion here does not guarantee an AER; a separate defined event requires support, configuration and a pending request. <a class="qa-rule-link" href="#common-command-9">Full rule in this volume</a></p>
</li>
<li id="q-062-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Correlate the completion with error records under the shared entry-creation rules; do not infer entry count directly from the number of failures. <a class="qa-rule-link" href="#common-command-10">Full rule in this volume</a></p>
</li>
<li id="q-062-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>Power Management Set Feature logging is Not Recommended; APST/HCTM logging is Optional and, when supported, follows successful-change rules. Actual temperature excursions use Thermal Excursion event conditions; setting a threshold is not a temperature excursion.</p>
</li>
<li id="q-062-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Non-saveable Power Management/APST follows Figure 466 defaults; non-saveable HCTM is persistent. Saveable configurations use Saved rules, with coordination among controllers sharing a domain.</p>
</li>
<li id="q-062-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Establish whole or partial subsystem coverage; non-saveable persistent values do not thereby become zero. <a class="qa-rule-link" href="#common-feature-13">Full rule in this volume</a></p>
</li>
<li id="q-062-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Do not classify all three as volatile: non-saveable HCTM persists, whereas Power Management/APST do not; saveable features restore Saved.</p>
</li>
<li id="q-062-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Feature scope determines whether other controllers or namespaces share the setting. <a class="qa-rule-link" href="#common-feature-15">Full rule in this volume</a></p>
</li>
<li id="q-062-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Compare configuration, operational state, SMART temperature and HCTM counters separately. Lower power alone does not identify APST as the cause.</p>
</li>
<li id="q-062-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First identify whether the trigger was host Set, idle timing or temperature.</p>
</li>
</ol><details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-power">Base 2.4 §5.2.30.1.2, 5.2.30.1.7</a> · <a href="#ref-thermal">Base 2.4 §5.2.30.1.10</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-featureeffects">Base 2.4 §5.2.13.1.18</a> · <a href="#ref-powerstates">Base 2.4 §8.1.19</a> · <a href="#ref-thermalpel">Base 2.4 §5.2.13.1.14.2.13</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-063" data-question="63"><h2><a class="qa-qid" href="#q-063">Q63</a> How are Timestamp, Keep Alive Timer and Host Memory Buffer configured and verified?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-063-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-063-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>These provide event time, communication-liveness monitoring and dedicated host memory, requiring different validation methods.</p>
</li>
<li id="q-063-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Timestamp/Keep Alive are controller time state; HMB also controls ownership/lifetime of host memory.</p>
</li>
<li id="q-063-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Check ONCS for Timestamp, KAS/CTRATT.TBKAS for Keep Alive, and HMPRE/HMMIN/HMMINDS/HMMAXD for HMB.</p>
</li>
<li id="q-063-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>FID 0Eh sets a 48-bit millisecond Timestamp in an 8-byte buffer. FID 0Fh sets KATO milliseconds rounded up to KAS×100 ms. FID 0Dh configures EHM/MR, HSIZE and descriptor address/count.</p>
</li>
<li id="q-063-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Timestamp Get should reflect elapsed time; KATO Get returns the rounded value. Allocate valid HMB pages before enabling and reclaim only after successful disable. MR=1 requires unchanged contents and descriptors as well as layout.</p>
</li>
<li id="q-063-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>KAS=10 rounds requested KATO1500 ms to 2000 ms. HMB Get returns CQE state and an attributes buffer, not only an enable bit.</p>
</li>
<li id="q-063-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Re-enabling enabled HMB returns 0/0Ch; HMDLEC=0 returns 0/02h. PCIe allows KATO=0 to disable; do not import another transport&#x27;s mandatory-enablement rule.</p>
</li>
<li id="q-063-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-063-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Normal completion here does not guarantee an AER; a separate defined event requires support, configuration and a pending request. <a class="qa-rule-link" href="#common-command-9">Full rule in this volume</a></p>
</li>
<li id="q-063-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Correlate the completion with error records under the shared entry-creation rules; do not infer entry count directly from the number of failures. <a class="qa-rule-link" href="#common-command-10">Full rule in this volume</a></p>
</li>
<li id="q-063-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>Timestamp shall not be logged as a Set Feature event; with PEL, use Timestamp Change (03h) and its before/after values. KATO/HMB Set Feature logging is Optional; when supported, successful changes require recording. Gets are not universally logged.</p>
</li>
<li id="q-063-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>HMB enable configuration is not retained and must be restored; MR=1 requires fully retained memory/content. A Timestamp maintained across that CLR must retain Origin; otherwise CLR clears the timestamp to zero; also account for a restored Saved value and read back Origin. Recheck Keep Alive under its save/default rules.</p>
</li>
<li id="q-063-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Reconfigure HMB on affected controllers, do not assume identical Timestamp continuity for all CLR methods, and rebuild host Keep Alive timing from restored Current.</p>
</li>
<li id="q-063-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>HMB is not nonvolatile storage; equal addresses do not justify MR=1. Restoring Saved Timestamp may move time backward. PCIe Keep Alive defaults to KATO=0 unless restoration rules provide otherwise.</p>
</li>
<li id="q-063-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Feature scope determines whether other controllers or namespaces share the setting. <a class="qa-rule-link" href="#common-feature-15">Full rule in this volume</a></p>
</li>
<li id="q-063-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Check Timestamp Origin/Synch rather than assuming a perfect wall clock, rounded KATO Current and HMB support/configuration/EHM/memory retention.</p>
</li>
<li id="q-063-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First locate the result in CQE versus data buffer and verify time/size units.</p>
</li>
</ol><details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-timestamp">Base 2.4 §5.2.30.1.8</a> · <a href="#ref-keepalive">Base 2.4 §3.9 (common and PCIe rules), 5.2.30.1.9</a> · <a href="#ref-hmb">Base 2.4 §5.2.30.2.3, 8.2.4</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-featureeffects">Base 2.4 §5.2.13.1.18</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-064" data-question="64"><h2><a class="qa-qid" href="#q-064">Q64</a> What do Host Behavior Support, Error Recovery and Read Recovery Level do?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-064-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-064-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Advertise host understanding of extensions, configure namespace error recovery and choose a read-recovery strategy.</p>
</li>
<li id="q-064-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>FID 16h is controller-scoped, FID 05h namespace-scoped, and FID 12h set/subsystem-scoped according to NVM Set support.</p>
</li>
<li id="q-064-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Pair ACRE with relevant capabilities, check NSFEAT.DAE before DULBE and RRLS before selecting a recovery level.</p>
</li>
<li id="q-064-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>FID 16h payload includes ACRE/LBAFEE. FID 05h TLER uses 100 ms and DULBE bit 16. FID 12h RRL is a level code, not the RRLS bitmap.</p>
</li>
<li id="q-064-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Discover support before Set. TLER starts when error recovery begins, not at command submission as a universal timeout. Set/read an advertised RRL for the correct target.</p>
</li>
<li id="q-064-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>ACRE enables applicable advanced retry behavior; DULBE changes unwritten/deallocated-block responses. Fast Fail does not promise fixed latency or zero internal attempts.</p>
</li>
<li id="q-064-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Unsupported levels/invalid settings follow 0/02h and applicable rules. Command Interrupted 0/21h requires ACRE=1 and DNR=0.</p>
</li>
<li id="q-064-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-064-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Normal completion here does not guarantee an AER; a separate defined event requires support, configuration and a pending request. <a class="qa-rule-link" href="#common-command-9">Full rule in this volume</a></p>
</li>
<li id="q-064-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Correlate the completion with error records under the shared entry-creation rules; do not infer entry count directly from the number of failures. <a class="qa-rule-link" href="#common-command-10">Full rule in this volume</a></p>
</li>
<li id="q-064-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>Get does not itself produce a Set Feature event; Set requires FID logging support, successful completion and a check for a changed setting. <a class="qa-rule-link" href="#common-feature_events-11">Full rule in this volume</a></p>
</li>
<li id="q-064-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Non-saveable Host Behavior Support and Error Recovery are nonpersistent, while Read Recovery Level persists. Saveable cases follow Saved and scope-dependent reset rules.</p>
</li>
<li id="q-064-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Establish whole or partial subsystem coverage; non-saveable persistent values do not thereby become zero. <a class="qa-rule-link" href="#common-feature-13">Full rule in this volume</a></p>
</li>
<li id="q-064-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Re-read Current after a power cycle. Non-saveable RRL still persists; absence of Saved does not mean it must return zero. Host Behavior Support/Error Recovery use their separate restoration rules.</p>
</li>
<li id="q-064-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Feature scope determines whether other controllers or namespaces share the setting. <a class="qa-rule-link" href="#common-feature-15">Full rule in this volume</a></p>
</li>
<li id="q-064-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>LBAFEE affects exposure/use of extended formats; interpret capability, host declaration and namespace format together.</p>
</li>
<li id="q-064-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First check whether TLER was treated as whole-command timeout or RRLS was confused with an RRL code.</p>
</li>
</ol><details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-behavior">Base 2.4 §5.2.30.1.15</a> · <a href="#ref-nvmfeat">NVM Command Set 1.3 §4.1.3.1–4.1.3.7</a> · <a href="#ref-rrl">Base 2.4 §5.2.30.1.12, 8.1.23</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-featureeffects">Base 2.4 §5.2.13.1.18</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-065" data-question="65"><h2><a class="qa-qid" href="#q-065">Q65</a> How is namespace write protection configured, and which modes survive reset or power cycling?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-065-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-065-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Prevent namespace modification with reversible, until-power-cycle and permanent protection lifetimes.</p>
</li>
<li id="q-065-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Protection belongs to the namespace and applies through other controllers accessing it, not just one queue&#x27;s software flag.</p>
</li>
<li id="q-065-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>NWPC advertises capability, WPC.WPUPCC/PWPC permits entering specific modes and Get FID 84h.WPS reports current state.</p>
</li>
<li id="q-065-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>WPS0/1/2/3 means none/basic/until-power-cycle/permanent. This feature is unsaveable and has no Default; SV=1 does not create persistence.</p>
</li>
<li id="q-065-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Check support/entry permission, Set WPS for NSID and read Current. Entering protection commits that namespace&#x27;s volatile data/metadata to nonvolatile media.</p>
</li>
<li id="q-065-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>After success, prohibited operations must obey protection rules while ordinary reads remain governed by readable state. Verify behavior in addition to Set success.</p>
</li>
<li id="q-065-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Changing WPS2/3, missing entry permission or prohibited multi-domain WPS2 transition uses 1/0Eh; Get Default uses 0/02h; prohibited commands may return Namespace is Write Protected 0/20h.</p>
</li>
<li id="q-065-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-065-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Normal completion here does not guarantee an AER; a separate defined event requires support, configuration and a pending request. <a class="qa-rule-link" href="#common-command-9">Full rule in this volume</a></p>
</li>
<li id="q-065-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Correlate the completion with error records under the shared entry-creation rules; do not infer entry count directly from the number of failures. <a class="qa-rule-link" href="#common-command-10">Full rule in this volume</a></p>
</li>
<li id="q-065-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>Get does not itself produce a Set Feature event; Set requires FID logging support, successful completion and a check for a changed setting. <a class="qa-rule-link" href="#common-feature_events-11">Full rule in this volume</a></p>
</li>
<li id="q-065-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Controller Reset preserves existing WPS, including Until Power Cycle; unsaveability does not remove protection.</p>
</li>
<li id="q-065-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>NVM Subsystem Reset is not a power cycle; WPS follows its state machine. NSSR is not a method to remove Until Power Cycle protection.</p>
</li>
<li id="q-065-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>An actual power cycle returns WPS2 to No Write Protect; basic WPS1 and permanent WPS3 persist. Ordinary Set/reset cannot remove permanent protection.</p>
</li>
<li id="q-065-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Feature scope determines whether other controllers or namespaces share the setting. <a class="qa-rule-link" href="#common-feature-15">Full rule in this volume</a></p>
</li>
<li id="q-065-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>CHANG=1 does not promise reversal of permanent protection. Reset of WPC permission bits differs from the namespace&#x27;s existing WPS state.</p>
</li>
<li id="q-065-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First read Current.WPS and WPC to separate missing support, denied entry and an already unchangeable state.</p>
</li>
</ol><details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-nwp">Base 2.4 §5.2.30.1.38, 8.1.18</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-featureeffects">Base 2.4 §5.2.13.1.18</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-066" data-question="66"><h2><a class="qa-qid" href="#q-066">Q66</a> Why read Get Features after a successful Set Features?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-066-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-066-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Verify transformations between the requested and effective value rather than relying only on success status.</p>
</li>
<li id="q-066-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Compare identical FID/scope/selectors and time; Supported Capabilities is not Current.</p>
</li>
<li id="q-066-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Know the response format and support; values may be in CQE, a payload or both.</p>
</li>
<li id="q-066-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>Preserve original SV/parameters and Set results, read Current with SEL 0 and Saved with SEL 2 when needed.</p>
</li>
<li id="q-066-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Await successful Set before Get and coordinate concurrent shared-scope writers. Compare dynamic values such as Timestamp with elapsed time rather than byte equality.</p>
</li>
<li id="q-066-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Successful Set completion cannot precede completion of attribute setting. Rounded KATO and allocated queue counts may validly differ from requests.</p>
</li>
<li id="q-066-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>A later Get failure has its own status and does not replace the Set result. Check selectors, scope and intervening reset.</p>
</li>
<li id="q-066-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-066-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Normal completion here does not guarantee an AER; a separate defined event requires support, configuration and a pending request. <a class="qa-rule-link" href="#common-command-9">Full rule in this volume</a></p>
</li>
<li id="q-066-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Correlate the completion with error records under the shared entry-creation rules; do not infer entry count directly from the number of failures. <a class="qa-rule-link" href="#common-command-10">Full rule in this volume</a></p>
</li>
<li id="q-066-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>Get does not itself produce a Set Feature event; Set requires FID logging support, successful completion and a check for a changed setting. <a class="qa-rule-link" href="#common-feature_events-11">Full rule in this volume</a></p>
</li>
<li id="q-066-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Use scope, saveability and reset coverage; whole-subsystem and partial resets differ. <a class="qa-rule-link" href="#common-feature-12">Full rule in this volume</a></p>
</li>
<li id="q-066-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Establish whole or partial subsystem coverage; non-saveable persistent values do not thereby become zero. <a class="qa-rule-link" href="#common-feature-13">Full rule in this volume</a></p>
</li>
<li id="q-066-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Saveable values restore Saved; non-saveable values require their persistence and feature-specific rules. <a class="qa-rule-link" href="#common-feature-14">Full rule in this volume</a></p>
</li>
<li id="q-066-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Feature scope determines whether other controllers or namespaces share the setting. <a class="qa-rule-link" href="#common-feature-15">Full rule in this volume</a></p>
</li>
<li id="q-066-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Readback establishes reported configuration; behavioral checks establish its use. Both are needed, without duplicating the same comparison as separate tests.</p>
</li>
<li id="q-066-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First confirm SEL=Current and no intervening reset or other Set.</p>
</li>
</ol><details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-getfeat">Base 2.4 §5.2.12</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-setcomplete">Base 2.4 §5.2.30 (Command Completion)</a> · <a href="#ref-keepalive">Base 2.4 §3.9 (common and PCIe rules), 5.2.30.1.9</a> · <a href="#ref-number">Base 2.4 §5.2.30.1.5</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-featureeffects">Base 2.4 §5.2.13.1.18</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-067" data-question="67"><h2><a class="qa-qid" href="#q-067">Q67</a> How should features change after activation, namespace deletion, reset and power cycling?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-067-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-067-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Establish persistence expectations per event and feature instead of assuming universal clearing or retention.</p>
</li>
<li id="q-067-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Separate controller, namespace and shared-object scope, then Current/Saved/Default.</p>
</li>
<li id="q-067-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Check SVBL, Figure 466/NVM Figure 92 and feature-specific exceptions. Unsaveable and nonpersistent are not synonyms.</p>
</li>
<li id="q-067-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>Record actual CLR occurrence and coverage. Namespace deletion removes an object; a new namespace reusing its number is not automatically the same configured object.</p>
</li>
<li id="q-067-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Snapshot, perform the defined event, restore management access, reread values/capabilities and verify behavior. For activation, identify its actual activation/reset path.</p>
</li>
<li id="q-067-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>An SV=0 change to a saveable feature can revert to older Saved after reset; HMB needs reconfiguration; WPS2 survives Controller Reset but ends at a power cycle.</p>
</li>
<li id="q-067-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Access after object deletion follows that FID&#x27;s NSID rules; failure to read a deleted namespace is not evidence of failed saving.</p>
</li>
<li id="q-067-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-067-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Normal completion here does not guarantee an AER; a separate defined event requires support, configuration and a pending request. <a class="qa-rule-link" href="#common-command-9">Full rule in this volume</a></p>
</li>
<li id="q-067-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Correlate the completion with error records under the shared entry-creation rules; do not infer entry count directly from the number of failures. <a class="qa-rule-link" href="#common-command-10">Full rule in this volume</a></p>
</li>
<li id="q-067-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>Get does not itself produce a Set Feature event; Set requires FID logging support, successful completion and a check for a changed setting. <a class="qa-rule-link" href="#common-feature_events-11">Full rule in this volume</a></p>
</li>
<li id="q-067-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Use scope, saveability and reset coverage; whole-subsystem and partial resets differ. <a class="qa-rule-link" href="#common-feature-12">Full rule in this volume</a></p>
</li>
<li id="q-067-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Establish whole or partial subsystem coverage; non-saveable persistent values do not thereby become zero. <a class="qa-rule-link" href="#common-feature-13">Full rule in this volume</a></p>
</li>
<li id="q-067-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Saveable values restore Saved; non-saveable values require their persistence and feature-specific rules. <a class="qa-rule-link" href="#common-feature-14">Full rule in this volume</a></p>
</li>
<li id="q-067-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Feature scope determines whether other controllers or namespaces share the setting. <a class="qa-rule-link" href="#common-feature-15">Full rule in this volume</a></p>
</li>
<li id="q-067-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Preserve object identity, SV, scope, reset cause and timing, not merely a changed-value flag.</p>
</li>
<li id="q-067-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First confirm the same object and the actual reset coverage.</p>
</li>
</ol><details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-timestamp">Base 2.4 §5.2.30.1.8</a> · <a href="#ref-hmb">Base 2.4 §5.2.30.2.3, 8.2.4</a> · <a href="#ref-nwp">Base 2.4 §5.2.30.1.38, 8.1.18</a> · <a href="#ref-nsmanage">Base 2.4 §5.2.24–5.2.25, 8.1.17</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-featureeffects">Base 2.4 §5.2.13.1.18</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-068" data-question="68"><h2><a class="qa-qid" href="#q-068">Q68</a> How should supported-feature claims be checked when Get, Set and behavior appear inconsistent?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-068-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-068-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Isolate whether the contradiction lies in capability, configuration, observation or firmware behavior under reproducible conditions.</p>
</li>
<li id="q-068-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Fix controller, FID, NSID/other selectors and configuration interval to avoid mixing scopes.</p>
</li>
<li id="q-068-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Compare Identify, feature-effects information and SEL 3. NSSPEC=0 is not necessarily controller scope; CHANG=1 is not unconditional changeability.</p>
</li>
<li id="q-068-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>Preserve FID/SEL/SV/CDW11/payloads and CQEs, and identify commands already outstanding before behavioral checks.</p>
</li>
<li id="q-068-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Discover, legally Set, await completion, Get Current and submit new affected work; test saving/reset separately, changing one factor at a time.</p>
</li>
<li id="q-068-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Consistency means conformance to allowed outcomes. Rounded KATO, dynamic Timestamp and implementation-specific coalescing cannot be rejected simply for differing from a request.</p>
</li>
<li id="q-068-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>First distinguish unsupported FID 0/02h, unsaveable 1/0Dh, unchangeable 1/0Eh and wrong-scope 1/0Fh; retain allowed status choices for multiple faults.</p>
</li>
<li id="q-068-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-068-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Normal completion here does not guarantee an AER; a separate defined event requires support, configuration and a pending request. <a class="qa-rule-link" href="#common-command-9">Full rule in this volume</a></p>
</li>
<li id="q-068-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Correlate the completion with error records under the shared entry-creation rules; do not infer entry count directly from the number of failures. <a class="qa-rule-link" href="#common-command-10">Full rule in this volume</a></p>
</li>
<li id="q-068-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>Get does not itself produce a Set Feature event; Set requires FID logging support, successful completion and a check for a changed setting. <a class="qa-rule-link" href="#common-feature_events-11">Full rule in this volume</a></p>
</li>
<li id="q-068-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Use scope, saveability and reset coverage; whole-subsystem and partial resets differ. <a class="qa-rule-link" href="#common-feature-12">Full rule in this volume</a></p>
</li>
<li id="q-068-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Establish whole or partial subsystem coverage; non-saveable persistent values do not thereby become zero. <a class="qa-rule-link" href="#common-feature-13">Full rule in this volume</a></p>
</li>
<li id="q-068-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Saveable values restore Saved; non-saveable values require their persistence and feature-specific rules. <a class="qa-rule-link" href="#common-feature-14">Full rule in this volume</a></p>
</li>
<li id="q-068-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Feature scope determines whether other controllers or namespaces share the setting. <a class="qa-rule-link" href="#common-feature-15">Full rule in this volume</a></p>
</li>
<li id="q-068-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>A noncompliance finding should include the explicit requirement, established prerequisites, raw request/response and evidence excluding selector/timing misuse.</p>
</li>
<li id="q-068-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First check wrong SEL/NSID or behavioral test commands submitted before Set completed.</p>
</li>
</ol><details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-getfeat">Base 2.4 §5.2.12</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-setcomplete">Base 2.4 §5.2.30 (Command Completion)</a> · <a href="#ref-irqfeat">Base 2.4 §5.2.30.2.1–5.2.30.2.2</a> · <a href="#ref-effects">Base 2.4 §5.2.13.1.5</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-featureeffects">Base 2.4 §5.2.13.1.18</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<section id="common-rules" class="qa-common"><h2>Shared rules linked from the answers</h2><p>Each shared mechanism is explained in full once in this volume. Use browser Back to return to the question; explicit command or feature exceptions take precedence.</p>
<article id="common-command-8"><h3>Command completion, events and records · How are DNR and More set?</h3><p>For a CQE, DNR=1 means the identical command is expected to fail if resubmitted to any controller in this subsystem; DNR=0 means it may succeed. Do not assign DNR=1 solely from an error name unless that condition mandates it. More=1 identifies additional information for this command in the Error Information Log. DNR should be zero when SCT=SC=0.</p></article>
<article id="common-command-9"><h3>Command completion, events and records · Is an asynchronous event generated?</h3><p>Command completion and asynchronous notification are separate. Success here does not itself guarantee an event. For a defined resulting event, check support, applicable notification configuration, masking and an outstanding Asynchronous Event Request.</p></article>
<article id="common-command-10"><h3>Command completion, events and records · Are Error Information or other logs updated?</h3><p>A successful CQE does not require a new Error Information entry. For an error with More=1, read LID 01h and correlate SQID, CID and Error Count; not every unsuccessful CQE requires a new entry. Re-read the interfaces named in this question for the state the operation changes.</p></article>
<article id="common-feature-12"><h3>Feature reset and scope · What survives or continues after Controller Reset?</h3><p>Separate scope from saveability. For a reset covering the subsystem, a saveable Current value is restored from Saved, or Default if no Saved value exists; a non-saveable, nonpersistent value returns to Default. A partial reset uses Figure 127 for shared scopes. The specific feature exceptions in this question take precedence.</p></article>
<article id="common-feature-13"><h3>Feature reset and scope · What survives or continues after NVM Subsystem Reset?</h3><p>Determine reset coverage, not only its name. Figure 126 applies to the whole subsystem; Figure 127 applies to a partial multi-domain reset. A non-saveable feature specified as persistent remains persistent; non-saveable does not mean reset to zero.</p></article>
<article id="common-feature-14"><h3>Feature reset and scope · What survives or continues after a power cycle?</h3><p>A successfully saved SV=1 setting is restored from Saved across a power cycle; SV=0 does not update Saved. For non-saveable features use Figure 466 persistence and feature-specific exceptions. Verify Current and behavior rather than assuming an existing Saved value is already active.</p></article>
<article id="common-feature-15"><h3>Feature reset and scope · Are other controllers or namespaces affected?</h3><p>Feature scope determines impact. Controller-scoped settings target that controller; namespace, NVM Set and subsystem settings may be shared across controllers. Coordinate changes across hosts and do not treat NSID=FFFFFFFFh as a universal feature broadcast.</p></article>
<article id="common-feature_events-11"><h3>Set Feature event recording · Is it recorded in the Persistent Event Log?</h3><p>With supported PEL Set Feature logging, Figure 252 must also permit and support this FID: successful changes shall be recorded; successfully reapplying the same value may be recorded. This is not universal across FIDs. Timestamp is prohibited from Set Feature logging and uses its separate Timestamp Change event rules.</p></article>
</section>
<section id="source-index"><h2>Source locations and existing figure guides</h2><p>Base printed page = PDF page−26; the other two use identical numbers. Locations follow the supplied PDF body and retain figure numbers. Shared pages contribute only the relevant definitions, excluding Fabrics and PCIe link/packet content.</p><ul class="qa-references">
<li id="ref-reset"><strong>Base 2.4 · §3.7.1–3.7.4</strong><br>Printed pages 120–124 · PDF 146–150</li>
<li id="ref-keepalive"><strong>Base 2.4 · §3.9 (common and PCIe rules), 5.2.30.1.9</strong><br>Printed pages 129–135, 471 · PDF 155–161, 497 · Figure 481</li>
<li id="ref-status"><strong>Base 2.4 · §4.2.3</strong><br>Printed pages 145–155 · PDF 171–181 · Figure 101–105</li>
<li id="ref-feature"><strong>Base 2.4 · §4.4</strong><br>Printed pages 166–169 · PDF 192–195 · Figure 126–127</li>
<li id="ref-aer"><strong>Base 2.4 · §5.2.2</strong><br>Printed pages 183–190 · PDF 209–216 · Figure 150–156</li>
<li id="ref-getfeat"><strong>Base 2.4 · §5.2.12</strong><br>Printed pages 209–212 · PDF 235–238 · Figure 197–202</li>
<li id="ref-error"><strong>Base 2.4 · §5.2.13.1.2</strong><br>Printed pages 218–220 · PDF 244–246 · Figure 212</li>
<li id="ref-effects"><strong>Base 2.4 · §5.2.13.1.5</strong><br>Printed pages 226–230 · PDF 252–256 · Figure 216–218</li>
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
