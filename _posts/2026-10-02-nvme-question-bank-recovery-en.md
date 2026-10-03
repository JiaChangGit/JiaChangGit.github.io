---
layout: post
title: "NVMe Self-Study Bank: Abort, timeout and recovery"
date: 2026-10-02 00:00:00 +0800
categories: [nvme]
permalink: /nvme/question-bank/recovery/en/
lang: en
nvme_quickref: true
nvme_qa: true
---

<div class="nvme-quickref nvme-qa">
<nav class="qr-top" aria-label="Bank and editions"><a href="#content">Skip to content</a><a href="/nvme/question-bank/en/">Question index</a><a href="/nvme/question-bank/recovery/zh-tw/">繁體中文</a><a href="/DOCS/nvme-question-bank/recovery.html">Chinese tutorial HTML</a></nav>
<main id="content"><p class="qr-eyebrow">BASE 2.4 / NVM 1.3 / PCIe 1.4 · Q1–328</p>
<header><p class="qa-range">Q107–Q117</p><h1>Abort, timeout and recovery</h1><p class="qr-intro">A timeout is an observation, not a location. Follow submission through consumption before choosing abort or reset.</p><p>Practice first, then reveal 17 answer items per question. All numerical examples are hypothetical. Status is written SCT/SC; h indicates hexadecimal.</p></header>
<aside class="qa-glossary"><h2>Terms used in this volume</h2><dl><dt>Controller / namespace</dt><dd>A controller receives commands and manages access. A namespace is a logical storage space that commands can address. An NVM subsystem contains controllers and nonvolatile storage resources.</dd><dt>SQ / CQ / SQE / CQE</dt><dd>Submission and Completion Queues carry command entries (SQEs) and completion entries (CQEs). QID identifies a queue, CID distinguishes outstanding commands in one SQ, and NSID identifies a namespace.</dd><dt>Register / Identify / Feature / Log</dt><dd>A register exposes control or state. Identify queries capabilities and attributes; features query or configure operation; log pages report specific state or records. FID, LID, CNS and CSI select features, logs, Identify structures and command sets.</dd><dt>index / offset / zero-based</dt><dd>An index selects an entry, usually starting at 0; an offset measures distance from an origin in specified units. A zero-based count encodes count−1, but not every zero-valued field is a count. A Dword is 4 bytes; a byte is 8 bits.</dd><dt>Scope / reset / retention</dt><dd>Scope names the affected objects; retention means preserving state. Controller Reset (clearing CC.EN) is one form of Controller Level Reset, or CLR. Different CLR triggers can retain different registers.</dd></dl></aside>
<section id="overview" class="qa-overview"><h2>Find the command stage first</h2><p class="qa-takeaway">Missing completion proves neither nonexecution nor unchanged media.</p>
<div class="qr-table" tabindex="0" role="region" aria-label="Horizontally scrollable comparison table"><table><thead><tr><th scope="col">Stage</th><th scope="col">Evidence</th><th scope="col">Next question</th></tr></thead><tbody><tr><td>Submitted</td><td>SQE and tail</td><td>Was it consumed?</td></tr><tr><td>Consumed</td><td>SQHD and tracking</td><td>Is it a long operation?</td></tr><tr><td>Completed</td><td>CQE and phase</td><td>Did the host miss it?</td></tr><tr><td>Recovering</td><td>Abort/reset state</td><td>Are prior effects uncertain?</td></tr></tbody></table></div>
<p><strong>Worked interpretation: </strong>Abort targeting SQ5/CID 9 has its own Admin completion. One CQE for each is normal; duplicate target completion is different.</p>
<p class="qa-citations">Sources: <a href="#ref-abort">Base 2.4 §5.2.1</a> · <a href="#ref-commrecovery">Base 2.4 §9.1–9.6.2.1 (PCIe-applicable rules; stop before 9.6.2.2)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-cqe">Base 2.4 §4.2.1, 4.2.3–4.2.4</a></p>
</section>
<div class="qa-controls" hidden><label>Search this page <input type="search" id="qa-search" placeholder="Question number, field or keyword"></label><button type="button" data-expand="true">Expand all answers</button><button type="button" data-expand="false">Collapse all answers</button><output id="qa-count" aria-live="polite"></output></div>
<section id="question-index"><h2>Questions in this volume</h2><ol class="qa-index">
<li><a href="#q-107">Q107 · How does Abort identify its target with SQID and CID?</a></li>
<li><a href="#q-108">Q108 · What happens when Abort targets a completed or missing command?</a></li>
<li><a href="#q-109">Q109 · How does ACL apply to repeated and concurrent Abort commands?</a></li>
<li><a href="#q-110">Q110 · Does successful Abort prove that the target never executed?</a></li>
<li><a href="#q-111">Q111 · Can a target complete normally if Abort did not immediately cancel it?</a></li>
<li><a href="#q-112">Q112 · How does the host handle racing Abort and target completions?</a></li>
<li><a href="#q-113">Q113 · Must every timeout follow Abort, queue reset, then controller reset?</a></li>
<li><a href="#q-114">Q114 · How should the host recover when Abort itself times out?</a></li>
<li><a href="#q-115">Q115 · How are old commands, completions and queues handled after reset?</a></li>
<li><a href="#q-116">Q116 · How do command, ready and long-operation timeouts differ?</a></li>
<li><a href="#q-117">Q117 · How is a timeout located along submission, execution and completion?</a></li>
</ol></section>
<article class="qa-question" id="q-107" data-question="107"><h2><a class="qa-qid" href="#q-107">Q107</a> How does Abort identify its target with SQID and CID?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-107-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-107-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Abort requests cancellation of a previously submitted command without necessarily resetting the controller; it does not prove the target was never executed.</p>
</li>
<li id="q-107-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>The target can be in the Admin SQ or an I/O SQ. Abort is itself an Admin command with its own CID and completion.</p>
</li>
<li id="q-107-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Identify.ACL is the zero-based concurrent Abort limit; queue depth does not replace it.</p>
</li>
<li id="q-107-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>Abort CDW10 bits 31:16 select target CID and bits 15:0 target SQID; CDW0.CID identifies the Abort command itself.</p>
</li>
<li id="q-107-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Locate the target in outstanding tracking, retain its buffers, submit Abort with a distinct Admin CID and track both completions.</p>
</li>
<li id="q-107-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>On successful Abort, DW0.IANP=0 reports immediate abort; IANP=1 reports no immediate abort but allows deferred abort. Inspect the target CQE too.</p>
</li>
<li id="q-107-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Excess outstanding Aborts may receive 1/03h. A missing target can be represented by successful Abort with IANP=1, not a universal Invalid Queue Identifier requirement.</p>
</li>
<li id="q-107-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-107-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Normal completion here does not guarantee an AER; a separate defined event requires support, configuration and a pending request. <a class="qa-rule-link" href="#common-command-9">Full rule in this volume</a></p>
</li>
<li id="q-107-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Correlate the completion with error records under the shared entry-creation rules; do not infer entry count directly from the number of failures. <a class="qa-rule-link" href="#common-command-10">Full rule in this volume</a></p>
</li>
<li id="q-107-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>PEL is not a per-command trace; supported defined events are logged under their recording conditions. <a class="qa-rule-link" href="#common-command-11">Full rule in this volume</a></p>
</li>
<li id="q-107-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Clearing CC.EN invalidates I/O queues and resets Admin pointers; retained base addresses do not validate old completions. <a class="qa-rule-link" href="#common-queue-12">Full rule in this volume</a></p>
</li>
<li id="q-107-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Rebuild affected-controller queues; do not assume CC.EN-reset register-retention exceptions. <a class="qa-rule-link" href="#common-queue-13">Full rule in this volume</a></p>
</li>
<li id="q-107-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Initialize queues and host tracking again; residual memory is not valid command state for a new lifetime. <a class="qa-rule-link" href="#common-queue-14">Full rule in this volume</a></p>
</li>
<li id="q-107-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Queues belong to a controller; CQ capacity and lifetime affect all SQs sharing it. <a class="qa-rule-link" href="#common-queue-15">Full rule in this volume</a></p>
</li>
<li id="q-107-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>If SQ3/CID 7 and SQ4/CID 7 coexist, CDW10=(7&lt;&lt;16)|3 targets only the former; this detects swapped fields.</p>
</li>
<li id="q-107-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First check that target CID was not confused with the Abort command’s own CID.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-abort">Base 2.4 §5.2.1</a> · <a href="#ref-sqe">Base 2.4 §4.1.1</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-108" data-question="108"><h2><a class="qa-qid" href="#q-108">Q108</a> What happens when Abort targets a completed or missing command?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-108-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-108-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>A target may finish between the host deciding to abort and the controller processing Abort; absence is a normal race to handle.</p>
</li>
<li id="q-108-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>The target is the command at the specified IDs at that time, not every historic use of those numbers.</p>
</li>
<li id="q-108-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Preserve queue-lifetime and CID-allocation records so a delayed Abort is not misdirected to a later reuse.</p>
</li>
<li id="q-108-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>Read Abort status and IANP and check for a target CQE. IANP=1 can mean absence or inability to abort immediately.</p>
</li>
<li id="q-108-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Process an already received target completion; if it remains outstanding with IANP=1, continue tracking and retain its buffers.</p>
</li>
<li id="q-108-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>A valid Abort can succeed with IANP=1 without cancelling the target; this reports request processing, not target success or rollback.</p>
</li>
<li id="q-108-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Do not assign a universal error status to every missing SQID/CID target; separate any independent invalid encoding in Abort itself.</p>
</li>
<li id="q-108-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-108-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Normal completion here does not guarantee an AER; a separate defined event requires support, configuration and a pending request. <a class="qa-rule-link" href="#common-command-9">Full rule in this volume</a></p>
</li>
<li id="q-108-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Correlate the completion with error records under the shared entry-creation rules; do not infer entry count directly from the number of failures. <a class="qa-rule-link" href="#common-command-10">Full rule in this volume</a></p>
</li>
<li id="q-108-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>PEL is not a per-command trace; supported defined events are logged under their recording conditions. <a class="qa-rule-link" href="#common-command-11">Full rule in this volume</a></p>
</li>
<li id="q-108-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Clearing CC.EN invalidates I/O queues and resets Admin pointers; retained base addresses do not validate old completions. <a class="qa-rule-link" href="#common-queue-12">Full rule in this volume</a></p>
</li>
<li id="q-108-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Rebuild affected-controller queues; do not assume CC.EN-reset register-retention exceptions. <a class="qa-rule-link" href="#common-queue-13">Full rule in this volume</a></p>
</li>
<li id="q-108-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Initialize queues and host tracking again; residual memory is not valid command state for a new lifetime. <a class="qa-rule-link" href="#common-queue-14">Full rule in this volume</a></p>
</li>
<li id="q-108-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Queues belong to a controller; CQ capacity and lifetime affect all SQs sharing it. <a class="qa-rule-link" href="#common-queue-15">Full rule in this volume</a></p>
</li>
<li id="q-108-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Replace a test requiring Abort failure for a completed target with checks of IANP and the existing target result.</p>
</li>
<li id="q-108-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First check whether the target already completed but its CQE has not been consumed.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-abort">Base 2.4 §5.2.1</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-109" data-question="109"><h2><a class="qa-qid" href="#q-109">Q109</a> How does ACL apply to repeated and concurrent Abort commands?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-109-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-109-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>ACL limits concurrent Abort requests, not cancellations per second or namespace count.</p>
</li>
<li id="q-109-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Each outstanding Abort consumes concurrent capacity, including several targeting the same command.</p>
</li>
<li id="q-109-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>ACL=0 permits one outstanding Abort and ACL=3 four; release host accounting on completion.</p>
</li>
<li id="q-109-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>Track each Abort CID, target IDs and result separately. Bulk cancellation can use supported Cancel or I/O SQ deletion/recreation.</p>
</li>
<li id="q-109-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Check capacity before submission and wait at the limit. Repeated targets still have separate Abort CQEs but only one target completion.</p>
</li>
<li id="q-109-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>With ACL=1, two outstanding Aborts fit the limit; submitting another after one completes avoids host overrun.</p>
</li>
<li id="q-109-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>The controller may complete excess requests with 1/03h; the specification does not mandate observing that code on every over-limit test.</p>
</li>
<li id="q-109-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-109-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Normal completion here does not guarantee an AER; a separate defined event requires support, configuration and a pending request. <a class="qa-rule-link" href="#common-command-9">Full rule in this volume</a></p>
</li>
<li id="q-109-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Correlate the completion with error records under the shared entry-creation rules; do not infer entry count directly from the number of failures. <a class="qa-rule-link" href="#common-command-10">Full rule in this volume</a></p>
</li>
<li id="q-109-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>PEL is not a per-command trace; supported defined events are logged under their recording conditions. <a class="qa-rule-link" href="#common-command-11">Full rule in this volume</a></p>
</li>
<li id="q-109-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Clearing CC.EN invalidates I/O queues and resets Admin pointers; retained base addresses do not validate old completions. <a class="qa-rule-link" href="#common-queue-12">Full rule in this volume</a></p>
</li>
<li id="q-109-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Rebuild affected-controller queues; do not assume CC.EN-reset register-retention exceptions. <a class="qa-rule-link" href="#common-queue-13">Full rule in this volume</a></p>
</li>
<li id="q-109-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Initialize queues and host tracking again; residual memory is not valid command state for a new lifetime. <a class="qa-rule-link" href="#common-queue-14">Full rule in this volume</a></p>
</li>
<li id="q-109-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Queues belong to a controller; CQ capacity and lifetime affect all SQs sharing it. <a class="qa-rule-link" href="#common-queue-15">Full rule in this volume</a></p>
</li>
<li id="q-109-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Count submissions not yet completed rather than cumulative Abort operations.</p>
</li>
<li id="q-109-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First check zero-based ACL interpretation and removal of completed requests from the count.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-abort">Base 2.4 §5.2.1</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-110" data-question="110"><h2><a class="qa-qid" href="#q-110">Q110</a> Does successful Abort prove that the target never executed?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-110-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-110-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>No. Abort can stop further processing but is not transaction rollback; data transfer or state changes may already have occurred.</p>
</li>
<li id="q-110-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Separate Abort completion, immediate-abort guarantees and effects already produced by the target.</p>
</li>
<li id="q-110-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>The Base 2.4 evidence is IANP in a successful Abort, not success status alone.</p>
</li>
<li id="q-110-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>IANP=0 prohibits subsequent target effects after the Abort CQE, including host-memory access and media/management changes, except posting the target CQE.</p>
</li>
<li id="q-110-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Record Abort completion and IANP, handle target completion and assess data under command semantics before retrying a possibly partially executed write.</p>
</li>
<li id="q-110-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Immediate abort yields target Command Abort Requested. The target CQE may precede or, under the no-subsequent-effects guarantee, follow the Abort CQE.</p>
</li>
<li id="q-110-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>IANP=1 gives no no-subsequent-effects guarantee. An initiated but incomplete transfer without a posted target CQE precludes immediate abort.</p>
</li>
<li id="q-110-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-110-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Normal completion here does not guarantee an AER; a separate defined event requires support, configuration and a pending request. <a class="qa-rule-link" href="#common-command-9">Full rule in this volume</a></p>
</li>
<li id="q-110-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Correlate the completion with error records under the shared entry-creation rules; do not infer entry count directly from the number of failures. <a class="qa-rule-link" href="#common-command-10">Full rule in this volume</a></p>
</li>
<li id="q-110-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>PEL is not a per-command trace; supported defined events are logged under their recording conditions. <a class="qa-rule-link" href="#common-command-11">Full rule in this volume</a></p>
</li>
<li id="q-110-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Clearing CC.EN invalidates I/O queues and resets Admin pointers; retained base addresses do not validate old completions. <a class="qa-rule-link" href="#common-queue-12">Full rule in this volume</a></p>
</li>
<li id="q-110-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Rebuild affected-controller queues; do not assume CC.EN-reset register-retention exceptions. <a class="qa-rule-link" href="#common-queue-13">Full rule in this volume</a></p>
</li>
<li id="q-110-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Initialize queues and host tracking again; residual memory is not valid command state for a new lifetime. <a class="qa-rule-link" href="#common-queue-14">Full rule in this volume</a></p>
</li>
<li id="q-110-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Queues belong to a controller; CQ capacity and lifetime affect all SQs sharing it. <a class="qa-rule-link" href="#common-queue-15">Full rule in this volume</a></p>
</li>
<li id="q-110-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Test prohibited effects after Abort completion rather than requiring that the target never performed any work.</p>
</li>
<li id="q-110-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First check whether the conclusion is based on IANP=0 or merely Abort success.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-abort">Base 2.4 §5.2.1</a> · <a href="#ref-order">Base 2.4 §3.4.1–3.4.5</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-111" data-question="111"><h2><a class="qa-qid" href="#q-111">Q111</a> Can a target complete normally if Abort did not immediately cancel it?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-111-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-111-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Yes. IANP=1 allows either deferred cancellation or normal target completion.</p>
</li>
<li id="q-111-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Abort and target outcomes are separate; failed or non-immediate Abort does not automatically fail the target.</p>
</li>
<li id="q-111-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Inspect IANP on successful Abort and the target CQE. Do not interpret reserved/undefined DW0 from a failed Abort as a valid IANP result.</p>
</li>
<li id="q-111-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>A deferred-aborted target must report Command Abort Requested; otherwise it reports its actual execution result.</p>
</li>
<li id="q-111-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>After IANP=1, track the target under host recovery time limits; escalating to reset requires proper queue-lifetime and resource handling.</p>
</li>
<li id="q-111-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Either target success or Command Abort Requested can be valid, without a second target completion.</p>
</li>
<li id="q-111-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>IANP=1 means neither that cancellation will never occur nor that it definitely will occur later.</p>
</li>
<li id="q-111-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-111-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Normal completion here does not guarantee an AER; a separate defined event requires support, configuration and a pending request. <a class="qa-rule-link" href="#common-command-9">Full rule in this volume</a></p>
</li>
<li id="q-111-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Correlate the completion with error records under the shared entry-creation rules; do not infer entry count directly from the number of failures. <a class="qa-rule-link" href="#common-command-10">Full rule in this volume</a></p>
</li>
<li id="q-111-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>PEL is not a per-command trace; supported defined events are logged under their recording conditions. <a class="qa-rule-link" href="#common-command-11">Full rule in this volume</a></p>
</li>
<li id="q-111-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Clearing CC.EN invalidates I/O queues and resets Admin pointers; retained base addresses do not validate old completions. <a class="qa-rule-link" href="#common-queue-12">Full rule in this volume</a></p>
</li>
<li id="q-111-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Rebuild affected-controller queues; do not assume CC.EN-reset register-retention exceptions. <a class="qa-rule-link" href="#common-queue-13">Full rule in this volume</a></p>
</li>
<li id="q-111-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Initialize queues and host tracking again; residual memory is not valid command state for a new lifetime. <a class="qa-rule-link" href="#common-queue-14">Full rule in this volume</a></p>
</li>
<li id="q-111-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Queues belong to a controller; CQ capacity and lifetime affect all SQs sharing it. <a class="qa-rule-link" href="#common-queue-15">Full rule in this volume</a></p>
</li>
<li id="q-111-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Validate the target’s actual result rather than deriving it from Abort status.</p>
</li>
<li id="q-111-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First inspect the target CQE; without it, leave the outcome unresolved.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-abort">Base 2.4 §5.2.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-112" data-question="112"><h2><a class="qa-qid" href="#q-112">Q112</a> How does the host handle racing Abort and target completions?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-112-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-112-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Timeout and normal completion paths can race over host tracking. Synchronize host state rather than demanding a universal completion order.</p>
</li>
<li id="q-112-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Abort and target have separate lifetimes; their CQEs are distinct even though they refer to one target.</p>
</li>
<li id="q-112-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Identify completions by SQID+CID, phase and queue lifetime; CID alone is insufficient across queues.</p>
</li>
<li id="q-112-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>Track target and Abort completion independently; only the target result completes the target to higher software layers.</p>
</li>
<li id="q-112-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Update the appropriate state atomically. A later Abort CQE closes Abort only; an earlier Abort CQE requires IANP and target-state handling.</p>
</li>
<li id="q-112-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Each command completes once and resources are reclaimed once. Two CQEs for two different commands are not duplicate target completion.</p>
</li>
<li id="q-112-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Do not universally require target CQE first; Base 2.4 permits either posting order when immediate-abort no-subsequent-effects conditions are met.</p>
</li>
<li id="q-112-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-112-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Normal completion here does not guarantee an AER; a separate defined event requires support, configuration and a pending request. <a class="qa-rule-link" href="#common-command-9">Full rule in this volume</a></p>
</li>
<li id="q-112-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Correlate the completion with error records under the shared entry-creation rules; do not infer entry count directly from the number of failures. <a class="qa-rule-link" href="#common-command-10">Full rule in this volume</a></p>
</li>
<li id="q-112-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>PEL is not a per-command trace; supported defined events are logged under their recording conditions. <a class="qa-rule-link" href="#common-command-11">Full rule in this volume</a></p>
</li>
<li id="q-112-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Clearing CC.EN invalidates I/O queues and resets Admin pointers; retained base addresses do not validate old completions. <a class="qa-rule-link" href="#common-queue-12">Full rule in this volume</a></p>
</li>
<li id="q-112-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Rebuild affected-controller queues; do not assume CC.EN-reset register-retention exceptions. <a class="qa-rule-link" href="#common-queue-13">Full rule in this volume</a></p>
</li>
<li id="q-112-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Initialize queues and host tracking again; residual memory is not valid command state for a new lifetime. <a class="qa-rule-link" href="#common-queue-14">Full rule in this volume</a></p>
</li>
<li id="q-112-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Queues belong to a controller; CQ capacity and lifetime affect all SQs sharing it. <a class="qa-rule-link" href="#common-queue-15">Full rule in this volume</a></p>
</li>
<li id="q-112-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Verify single upper-layer completion and prevent old Abort results from affecting a reused CID lifetime.</p>
</li>
<li id="q-112-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First determine whether the two CQEs actually belong to Abort and target separately.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-abort">Base 2.4 §5.2.1</a> · <a href="#ref-cqe">Base 2.4 §4.2.1, 4.2.3–4.2.4</a> · <a href="#ref-queue">Base 2.4 §3.3.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-113" data-question="113"><h2><a class="qa-qid" href="#q-113">Q113</a> Must every timeout follow Abort, queue reset, then controller reset?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-113-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-113-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>There is no universal three-step sequence. Diagnose a slow command, failed queue or lost controller communication before selecting recovery scope.</p>
</li>
<li id="q-113-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Abort targets a command; queue deletion/recreation targets queues; controller reset affects all its queues and outstanding commands.</p>
</li>
<li id="q-113-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Preserve CQ position/phase, interrupts, CSTS and other-command progress. CAP.TO is not a per-I/O timeout.</p>
</li>
<li id="q-113-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>Available actions include Abort, queue deletion/recreation and reset via CC.EN, each with its own preconditions and completion checks.</p>
</li>
<li id="q-113-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>First exclude missed CQEs. With a working Admin path, consider Abort; recover damaged queues; serious Admin errors or uncompleted deletion call for controller reset.</p>
</li>
<li id="q-113-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Recovery establishes usable new channels, resolves old-command access risks and rechecks any continuing background operations.</p>
</li>
<li id="q-113-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>A host timeout is not an NVMe completion status. Do not fabricate a timeout CQE or require Abort when the Admin path cannot complete it.</p>
</li>
<li id="q-113-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-113-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Normal completion here does not guarantee an AER; a separate defined event requires support, configuration and a pending request. <a class="qa-rule-link" href="#common-command-9">Full rule in this volume</a></p>
</li>
<li id="q-113-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Correlate the completion with error records under the shared entry-creation rules; do not infer entry count directly from the number of failures. <a class="qa-rule-link" href="#common-command-10">Full rule in this volume</a></p>
</li>
<li id="q-113-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>PEL is not a per-command trace; supported defined events are logged under their recording conditions. <a class="qa-rule-link" href="#common-command-11">Full rule in this volume</a></p>
</li>
<li id="q-113-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Clearing CC.EN invalidates I/O queues and resets Admin pointers; retained base addresses do not validate old completions. <a class="qa-rule-link" href="#common-queue-12">Full rule in this volume</a></p>
</li>
<li id="q-113-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Rebuild affected-controller queues; do not assume CC.EN-reset register-retention exceptions. <a class="qa-rule-link" href="#common-queue-13">Full rule in this volume</a></p>
</li>
<li id="q-113-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Initialize queues and host tracking again; residual memory is not valid command state for a new lifetime. <a class="qa-rule-link" href="#common-queue-14">Full rule in this volume</a></p>
</li>
<li id="q-113-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Queues belong to a controller; CQ capacity and lifetime affect all SQs sharing it. <a class="qa-rule-link" href="#common-queue-15">Full rule in this volume</a></p>
</li>
<li id="q-113-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Mark specification requirements separately from host-selected timeouts and escalation policies.</p>
</li>
<li id="q-113-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First inspect the CQ for an existing completion; resetting can conceal an interrupt-handling problem.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-abort">Base 2.4 §5.2.1</a> · <a href="#ref-fatal">Base 2.4 §9.1–9.6.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-commrecovery">Base 2.4 §9.1–9.6.2.1 (PCIe-applicable rules; stop before 9.6.2.2)</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-114" data-question="114"><h2><a class="qa-qid" href="#q-114">Q114</a> How should the host recover when Abort itself times out?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-114-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-114-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Now both target outcome and Admin-channel health are uncertain. Repeated Abort submissions do not establish that old commands stopped.</p>
</li>
<li id="q-114-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Recovery may widen to the controller, requiring coordination with all its queue and resource management.</p>
</li>
<li id="q-114-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Check Admin CQ phase/head, CFS/RDY and ACL accounting.</p>
</li>
<li id="q-114-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>Preserve Abort CID, target IDs, timing and observed CQEs; a subsequent reset does not fabricate an Abort result.</p>
</li>
<li id="q-114-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Exclude missed Admin CQEs; serious Admin failure calls for controller reset, state confirmation and reinitialization under Base 9.1/9.5.</p>
</li>
<li id="q-114-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>New commands use recovered queues; prior data effects still require command-specific persistence analysis.</p>
</li>
<li id="q-114-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Without an Abort CQE there is no IANP, DNR or More to decode. Successful reset does not prove a target write never happened.</p>
</li>
<li id="q-114-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-114-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Normal completion here does not guarantee an AER; a separate defined event requires support, configuration and a pending request. <a class="qa-rule-link" href="#common-command-9">Full rule in this volume</a></p>
</li>
<li id="q-114-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Correlate the completion with error records under the shared entry-creation rules; do not infer entry count directly from the number of failures. <a class="qa-rule-link" href="#common-command-10">Full rule in this volume</a></p>
</li>
<li id="q-114-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>PEL is not a per-command trace; supported defined events are logged under their recording conditions. <a class="qa-rule-link" href="#common-command-11">Full rule in this volume</a></p>
</li>
<li id="q-114-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Clearing CC.EN invalidates I/O queues and resets Admin pointers; retained base addresses do not validate old completions. <a class="qa-rule-link" href="#common-queue-12">Full rule in this volume</a></p>
</li>
<li id="q-114-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Rebuild affected-controller queues; do not assume CC.EN-reset register-retention exceptions. <a class="qa-rule-link" href="#common-queue-13">Full rule in this volume</a></p>
</li>
<li id="q-114-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Initialize queues and host tracking again; residual memory is not valid command state for a new lifetime. <a class="qa-rule-link" href="#common-queue-14">Full rule in this volume</a></p>
</li>
<li id="q-114-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Queues belong to a controller; CQ capacity and lifetime affect all SQs sharing it. <a class="qa-rule-link" href="#common-queue-15">Full rule in this volume</a></p>
</li>
<li id="q-114-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Correlate registers, new queue usability and background-operation logs rather than relying only on a host reset routine’s return value.</p>
</li>
<li id="q-114-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First check whether the Admin CQ is full or no longer being consumed.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-fatal">Base 2.4 §9.1–9.6.1</a> · <a href="#ref-abort">Base 2.4 §5.2.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-115" data-question="115"><h2><a class="qa-qid" href="#q-115">Q115</a> How are old commands, completions and queues handled after reset?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-115-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-115-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Reset separates queue lifetimes; surviving memory bytes are not evidence of valid commands or completions.</p>
</li>
<li id="q-115-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Rebuild affected I/O queues and outstanding tracking; stored data and independent background operations follow separate rules.</p>
</li>
<li id="q-115-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Check reset type, CC/CSTS and Admin-register retention; CC.EN-reset exceptions do not apply to every source.</p>
</li>
<li id="q-115-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>Reset host queue pointers/expected phase and separate new submissions from old tracking; inspect continuing operations through their logs.</p>
</li>
<li id="q-115-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Stop submissions, complete reset and access-termination checks, create new queues, then resume I/O with retry analysis of possible prior effects.</p>
</li>
<li id="q-115-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>New queues accept completions for their new lifetime; the host does not wait for all old CQEs after reset termination.</p>
</li>
<li id="q-115-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Reset is not universal per-command completion with one error code. Reset-aborted AERs expressly have no CQE; other commands do not universally return Command Abort Requested.</p>
</li>
<li id="q-115-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-115-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Normal completion here does not guarantee an AER; a separate defined event requires support, configuration and a pending request. <a class="qa-rule-link" href="#common-command-9">Full rule in this volume</a></p>
</li>
<li id="q-115-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Correlate the completion with error records under the shared entry-creation rules; do not infer entry count directly from the number of failures. <a class="qa-rule-link" href="#common-command-10">Full rule in this volume</a></p>
</li>
<li id="q-115-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>PEL is not a per-command trace; supported defined events are logged under their recording conditions. <a class="qa-rule-link" href="#common-command-11">Full rule in this volume</a></p>
</li>
<li id="q-115-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Clearing CC.EN invalidates I/O queues and resets Admin pointers; retained base addresses do not validate old completions. <a class="qa-rule-link" href="#common-queue-12">Full rule in this volume</a></p>
</li>
<li id="q-115-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Rebuild affected-controller queues; do not assume CC.EN-reset register-retention exceptions. <a class="qa-rule-link" href="#common-queue-13">Full rule in this volume</a></p>
</li>
<li id="q-115-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Initialize queues and host tracking again; residual memory is not valid command state for a new lifetime. <a class="qa-rule-link" href="#common-queue-14">Full rule in this volume</a></p>
</li>
<li id="q-115-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Queues belong to a controller; CQ capacity and lifetime affect all SQs sharing it. <a class="qa-rule-link" href="#common-queue-15">Full rule in this volume</a></p>
</li>
<li id="q-115-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Validate new queues and termination of old-buffer accesses; new-command success alone does not exclude late old-command activity.</p>
</li>
<li id="q-115-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First inspect reused phase or tracking state that could make stale CQEs appear new.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-queue">Base 2.4 §3.3.1</a> · <a href="#ref-cqe">Base 2.4 §4.2.1, 4.2.3–4.2.4</a> · <a href="#ref-commrecovery">Base 2.4 §9.1–9.6.2.1 (PCIe-applicable rules; stop before 9.6.2.2)</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-116" data-question="116"><h2><a class="qa-qid" href="#q-116">Q116</a> How do command, ready and long-operation timeouts differ?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-116-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-116-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Command completion, readiness and background-operation completion are different waits; sharing one deadline causes false timeouts.</p>
</li>
<li id="q-116-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Host command timeouts are software policy, readiness concerns controller state and background progress belongs to the management operation.</p>
</li>
<li id="q-116-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Disable uses CAP.TO; enable uses ready-mode and CRTO/CAP rules; interpret function estimates and maxima under their own definitions.</p>
</li>
<li id="q-116-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>Observe CQEs, RDY and operation logs. AER remains outstanding without an event and should not use an ordinary command timeout.</p>
</li>
<li id="q-116-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Name the awaited transition and timer start. After Sanitize initiation succeeds, monitor its status rather than expecting a second command CQE.</p>
</li>
<li id="q-116-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>The wait succeeds when its specified state is reached; command success and media-operation completion can occur separately.</p>
</li>
<li id="q-116-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>CAP.TO is not universal across commands, and an estimated duration is not automatically a mandatory deadline.</p>
</li>
<li id="q-116-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-116-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Normal completion here does not guarantee an AER; a separate defined event requires support, configuration and a pending request. <a class="qa-rule-link" href="#common-command-9">Full rule in this volume</a></p>
</li>
<li id="q-116-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Correlate the completion with error records under the shared entry-creation rules; do not infer entry count directly from the number of failures. <a class="qa-rule-link" href="#common-command-10">Full rule in this volume</a></p>
</li>
<li id="q-116-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>PEL is not a per-command trace; supported defined events are logged under their recording conditions. <a class="qa-rule-link" href="#common-command-11">Full rule in this volume</a></p>
</li>
<li id="q-116-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Clearing CC.EN invalidates I/O queues and resets Admin pointers; retained base addresses do not validate old completions. <a class="qa-rule-link" href="#common-queue-12">Full rule in this volume</a></p>
</li>
<li id="q-116-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Rebuild affected-controller queues; do not assume CC.EN-reset register-retention exceptions. <a class="qa-rule-link" href="#common-queue-13">Full rule in this volume</a></p>
</li>
<li id="q-116-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Initialize queues and host tracking again; residual memory is not valid command state for a new lifetime. <a class="qa-rule-link" href="#common-queue-14">Full rule in this volume</a></p>
</li>
<li id="q-116-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Queues belong to a controller; CQ capacity and lifetime affect all SQs sharing it. <a class="qa-rule-link" href="#common-queue-15">Full rule in this volume</a></p>
</li>
<li id="q-116-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Record source, units, starting event and whether each timeout is an estimate or limit.</p>
</li>
<li id="q-116-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First check which timer was applied to which awaited state.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-cap">Base 2.4 §3.1.4 (CAP, VS)</a> · <a href="#ref-crto">Base 2.4 §3.1.4 (CRTO)</a> · <a href="#ref-ready">Base 2.4 §3.5.3–3.5.4</a> · <a href="#ref-abort">Base 2.4 §5.2.1</a> · <a href="#ref-aerfull">Base 2.4 §5.2.2 (PCIe-applicable events)</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-117" data-question="117"><h2><a class="qa-qid" href="#q-117">Q117</a> How is a timeout located along submission, execution and completion?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-117-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-117-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Evidence along the command lifetime localizes missing progress before blaming slow firmware execution.</p>
</li>
<li id="q-117-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Analyze the target together with its SQ, CQ, shared vector and neighboring commands to locate shared bottlenecks.</p>
</li>
<li id="q-117-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Use SQE snapshots, tail doorbell, reported SQHD, CQ phase/head, interrupt configuration and CSTS as interface evidence.</p>
</li>
<li id="q-117-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>Advanced SQHD establishes consumption, not completion of every command; a valid target CQE establishes its result, while interrupts notify the host to inspect CQs.</p>
</li>
<li id="q-117-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Check visibility, doorbell update, new CQ phase and host consumption/head updates. State uncertainty when internal fetch timing is unobservable.</p>
</li>
<li id="q-117-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>An existing CQE localizes the issue beyond execution; a doorbell write alone does not prove command fetch.</p>
</li>
<li id="q-117-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>This diagnosis has no single NVMe status; preserve stage-specific evidence rather than inventing a timeout status.</p>
</li>
<li id="q-117-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-117-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Normal completion here does not guarantee an AER; a separate defined event requires support, configuration and a pending request. <a class="qa-rule-link" href="#common-command-9">Full rule in this volume</a></p>
</li>
<li id="q-117-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Correlate the completion with error records under the shared entry-creation rules; do not infer entry count directly from the number of failures. <a class="qa-rule-link" href="#common-command-10">Full rule in this volume</a></p>
</li>
<li id="q-117-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>PEL is not a per-command trace; supported defined events are logged under their recording conditions. <a class="qa-rule-link" href="#common-command-11">Full rule in this volume</a></p>
</li>
<li id="q-117-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Clearing CC.EN invalidates I/O queues and resets Admin pointers; retained base addresses do not validate old completions. <a class="qa-rule-link" href="#common-queue-12">Full rule in this volume</a></p>
</li>
<li id="q-117-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Rebuild affected-controller queues; do not assume CC.EN-reset register-retention exceptions. <a class="qa-rule-link" href="#common-queue-13">Full rule in this volume</a></p>
</li>
<li id="q-117-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Initialize queues and host tracking again; residual memory is not valid command state for a new lifetime. <a class="qa-rule-link" href="#common-queue-14">Full rule in this volume</a></p>
</li>
<li id="q-117-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Queues belong to a controller; CQ capacity and lifetime affect all SQs sharing it. <a class="qa-rule-link" href="#common-queue-15">Full rule in this volume</a></p>
</li>
<li id="q-117-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Correlate valid completions, shared CQ space and interrupt masking to identify host-side stalls.</p>
</li>
<li id="q-117-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First inspect the expected-phase CQ slot to distinguish an unreported result from an unconsumed completion.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-sqe">Base 2.4 §4.1.1</a> · <a href="#ref-cqe">Base 2.4 §4.2.1, 4.2.3–4.2.4</a> · <a href="#ref-queue">Base 2.4 §3.3.1</a> · <a href="#ref-pcie">PCIe Transport 1.4 §3.1–3.4</a> · <a href="#ref-irq">PCIe Transport 1.4 §3.5</a> · <a href="#ref-fatal">Base 2.4 §9.1–9.6.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<section id="common-rules" class="qa-common"><h2>Shared rules linked from the answers</h2><p>Each shared mechanism is explained in full once in this volume. Use browser Back to return to the question; explicit command or feature exceptions take precedence.</p>
<article id="common-command-8"><h3>Command completion, events and records · How are DNR and More set?</h3><p>For a CQE, DNR=1 means the identical command is expected to fail if resubmitted to any controller in this subsystem; DNR=0 means it may succeed. Do not assign DNR=1 solely from an error name unless that condition mandates it. More=1 identifies additional information for this command in the Error Information Log. DNR should be zero when SCT=SC=0.</p></article>
<article id="common-command-9"><h3>Command completion, events and records · Is an asynchronous event generated?</h3><p>Command completion and asynchronous notification are separate. Success here does not itself guarantee an event. For a defined resulting event, check support, applicable notification configuration, masking and an outstanding Asynchronous Event Request.</p></article>
<article id="common-command-10"><h3>Command completion, events and records · Are Error Information or other logs updated?</h3><p>A successful CQE does not require a new Error Information entry. For an error with More=1, read LID 01h and correlate SQID, CID and Error Count; not every unsuccessful CQE requires a new entry. Re-read the interfaces named in this question for the state the operation changes.</p></article>
<article id="common-command-11"><h3>Command completion, events and records · Is it recorded in the Persistent Event Log?</h3><p>The optional Persistent Event Log is an event history, not a trace of every command. Check LPA support and the Supported Events Bitmap, then the logging condition for the particular event. Command success or failure alone does not require an entry.</p></article>
<article id="common-queue-12"><h3>Queue reset and scope · What survives or continues after Controller Reset?</h3><p>Clearing CC.EN initiates a Controller Level Reset: I/O queues are deleted and Admin Queue pointers reset. Retention of AQA/ASQ/ACQ for this reset does not validate old CQEs. Reinitialize Admin CQ phases, enable, then configure and recreate I/O queues.</p></article>
<article id="common-queue-13"><h3>Queue reset and scope · What survives or continues after NVM Subsystem Reset?</h3><p>Affected controllers undergo Controller Level Reset during an NVM Subsystem Reset; old queues cannot be reused. Re-establish transport and register state and the Admin/I/O environment. Do not apply the AQA retention exception of a CC.EN reset to this different reset source.</p></article>
<article id="common-queue-14"><h3>Queue reset and scope · What survives or continues after a power cycle?</h3><p>After a power cycle, initialize and create queues again. Residual SQE/CQE bytes in host memory are not valid commands or completions for the new queue lifetime; rebuild host pointers, phases and outstanding-command tracking.</p></article>
<article id="common-queue-15"><h3>Queue reset and scope · Are other controllers or namespaces affected?</h3><p>Queues belong to their controller; equal QIDs on different controllers do not identify the same queue. SQs sharing a CQ are directly coupled through CQ capacity and deletion ordering. Queue reset neither deletes a namespace nor reverses completed writes.</p></article>
</section>
<section id="source-index"><h2>Source locations and existing figure guides</h2><p>Base printed page = PDF page−26; the other two use identical numbers. Locations follow the supplied PDF body and retain figure numbers. Shared pages contribute only the relevant definitions, excluding Fabrics and PCIe link/packet content.</p><ul class="qa-references">
<li id="ref-cap"><strong>Base 2.4 · §3.1.4 (CAP, VS)</strong><br>Printed pages 54–59 · PDF 80–85 · Figure 36–37</li>
<li id="ref-crto"><strong>Base 2.4 · §3.1.4 (CRTO)</strong><br>Printed pages 72–73 · PDF 98–99 · Figure 57</li>
<li id="ref-queue"><strong>Base 2.4 · §3.3.1</strong><br>Printed pages 88–91 · PDF 114–117 · Figure 73–74</li>
<li id="ref-order"><strong>Base 2.4 · §3.4.1–3.4.5</strong><br>Printed pages 101–105 · PDF 127–131 · Figure 80–81</li>
<li id="ref-ready"><strong>Base 2.4 · §3.5.3–3.5.4</strong><br>Printed pages 109–113 · PDF 135–139 · Figure 84–85</li>
<li id="ref-reset"><strong>Base 2.4 · §3.7.1–3.7.4</strong><br>Printed pages 120–124 · PDF 146–150</li>
<li id="ref-sqe"><strong>Base 2.4 · §4.1.1</strong><br>Printed pages 139–142 · PDF 165–168 · Figure 92–93</li>
<li id="ref-cqe"><strong>Base 2.4 · §4.2.1, 4.2.3–4.2.4</strong><br>Printed pages 144–157 · PDF 170–183 · Figure 97–105, 109</li>
<li id="ref-status"><strong>Base 2.4 · §4.2.3</strong><br>Printed pages 145–155 · PDF 171–181 · Figure 101–105</li>
<li id="ref-abort"><strong>Base 2.4 · §5.2.1</strong><br>Printed pages 181–182 · PDF 207–208 · Figure 147–149</li>
<li id="ref-aer"><strong>Base 2.4 · §5.2.2</strong><br>Printed pages 183–190 · PDF 209–216 · Figure 150–156</li>
<li id="ref-aerfull"><strong>Base 2.4 · §5.2.2 (PCIe-applicable events)</strong><br>Printed pages 183–191 · PDF 209–217 · Figure 150–160</li>
<li id="ref-error"><strong>Base 2.4 · §5.2.13.1.2</strong><br>Printed pages 218–220 · PDF 244–246 · Figure 212</li>
<li id="ref-pel"><strong>Base 2.4 · §5.2.13.1.14 (header, reset, hardware, Set Feature events)</strong><br>Printed pages 244–256, 258, 262–264 · PDF 270–282, 284, 288–290 · Figure 232–244, 246, 252–253</li>
<li id="ref-idctrl"><strong>Base 2.4 · §5.2.14.2.1</strong><br>Printed pages 340–387 · PDF 366–413 · Figure 338–341</li>
<li id="ref-commrecovery"><strong>Base 2.4 · §9.1–9.6.2.1 (PCIe-applicable rules; stop before 9.6.2.2)</strong><br>Printed pages 825–828 · PDF 851–854</li>
<li id="ref-fatal"><strong>Base 2.4 · §9.1–9.6.1</strong><br>Printed pages 825–826 · PDF 851–852</li>
<li id="ref-pcie"><strong>PCIe Transport 1.4 · §3.1–3.4</strong><br>Printed pages 9–13 · PDF 9–13 · Figure 3–8</li>
<li id="ref-irq"><strong>PCIe Transport 1.4 · §3.5</strong><br>Printed pages 13–16 · PDF 13–16 · Figure 9</li>
</ul><h3>When you need a field guide</h3><p>Existing figure explanations have canonical locations; use these links instead of duplicating the same guide.</p><ul>
<li><a href="/nvme/figure-reference/command/en/#figure-b101">Base 2.4 Figure 101 · Completion Queue Entry: Status Field</a></li>
<li><a href="/nvme/figure-reference/command/en/#figure-b104">Base 2.4 Figure 104 · Status Code – Command Specific Status Values</a></li>
<li><a href="/nvme/figure-reference/identify/en/#figure-b338">Base 2.4 Figure 338 · Identify – Identify Controller Data Structure, I/O Command Set Independent</a></li>
<li><a href="/nvme/figure-reference/init/en/#figure-b36">Base 2.4 Figure 36 · Offset 0h: CAP – Controller Capabilities</a></li>
<li><a href="/nvme/figure-reference/command/en/#figure-b93">Base 2.4 Figure 93 · Common Command Format</a></li>
<li><a href="/nvme/figure-reference/command/en/#figure-b97">Base 2.4 Figure 97 · Common Completion Queue Entry Layout – Admin and All I/O Command Sets</a></li>
</ul><details><summary>Original documents used</summary><ul class="qr-sources">
<li>NVM Express Base Specification · Revision 2.4 · 2026-07-31<br><code>NVM-Express-Base-Specification-Revision-2.4-Ratified-2026.07.31.pdf</code></li>
<li>NVM Express NVM Command Set Specification · Revision 1.3 · 2026-07-31<br><code>NVM-Express-NVM-Command-Set-Specification-Revision-1.3-Ratified-2026.07.31.pdf</code></li>
<li>NVM Express NVMe over PCIe Transport Specification · Revision 1.4 · 2026-07-31<br><code>NVM-Express-NVMe-over-PCIe-Transport-Specification-Revision-1.4-Ratified-2026.07.31.pdf</code></li>
</ul></details></section>
</main>
<nav class="qr-top" aria-label="Bank and editions"><a href="#content">Skip to content</a><a href="/nvme/question-bank/en/">Question index</a><a href="/nvme/question-bank/recovery/zh-tw/">繁體中文</a><a href="/DOCS/nvme-question-bank/recovery.html">Chinese tutorial HTML</a></nav>
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
