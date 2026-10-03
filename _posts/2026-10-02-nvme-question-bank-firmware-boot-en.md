---
layout: post
title: "NVMe Self-Study Bank: Firmware update and boot partitions"
date: 2026-10-02 00:00:00 +0800
categories: [nvme]
permalink: /nvme/question-bank/firmware-boot/en/
lang: en
nvme_quickref: true
nvme_qa: true
---

<div class="nvme-quickref nvme-qa">
<nav class="qr-top" aria-label="Bank and editions"><a href="#content">Skip to content</a><a href="/nvme/question-bank/en/">Question index</a><a href="/nvme/question-bank/firmware-boot/zh-tw/">繁體中文</a><a href="/DOCS/nvme-question-bank/firmware-boot.html">Chinese tutorial HTML</a></nav>
<main id="content"><p class="qr-eyebrow">BASE 2.4 / NVM 1.3 / PCIe 1.4 · Q1–320</p>
<header><p class="qa-range">Q136–Q148</p><h1>Firmware update and boot partitions</h1><p class="qr-intro">Separate download, commit and activation, then compare boot-image access and selection.</p><p>Practice first, then reveal 17 answer items per question. All numerical examples are hypothetical. Status is written SCT/SC; h indicates hexadecimal.</p></header>
<aside class="qa-glossary"><h2>Terms used in this volume</h2><dl><dt>Controller / namespace</dt><dd>A controller receives commands and manages access. A namespace is a logical storage space that commands can address. An NVM subsystem contains controllers and nonvolatile storage resources.</dd><dt>SQ / CQ / SQE / CQE</dt><dd>Submission and Completion Queues carry command entries (SQEs) and completion entries (CQEs). QID identifies a queue, CID distinguishes outstanding commands in one SQ, and NSID identifies a namespace.</dd><dt>Register / Identify / Feature / Log</dt><dd>A register exposes control or state. Identify queries capabilities and attributes; features query or configure operation; log pages report specific state or records. FID, LID, CNS and CSI select features, logs, Identify structures and command sets.</dd><dt>index / offset / zero-based</dt><dd>An index selects an entry, usually starting at 0; an offset measures distance from an origin in specified units. A zero-based count encodes count−1, but not every zero-valued field is a count. A Dword is 4 bytes; a byte is 8 bits.</dd><dt>Scope / reset / retention</dt><dd>Scope names the affected objects; retention means preserving state. Controller Reset (clearing CC.EN) is one form of Controller Level Reset, or CLR. Different CLR triggers can retain different registers.</dd></dl></aside>
<section id="overview" class="qa-overview"><h2>From image bytes to activation</h2><p class="qa-takeaway">Slot contents, pending activation and running revision describe different stages.</p>
<div class="qr-table" tabindex="0" role="region" aria-label="Horizontally scrollable comparison table"><table><thead><tr><th scope="col">Stage</th><th scope="col">Evidence</th><th scope="col">Conclusion</th></tr></thead><tbody><tr><td>Download</td><td>Offset, length, coverage</td><td>Transferred, not activated</td></tr><tr><td>Commit</td><td>Slot, action, status</td><td>Stored or activation scheduled</td></tr><tr><td>Activation</td><td>Required reset, revision, active slot</td><td>Establish running version</td></tr><tr><td>Boot partition</td><td>Active partition, read state, protection</td><td>Interpret boot access/protection</td></tr></tbody></table></div>
<p><strong>Worked interpretation: </strong>Pending slot activation need not change FR early; boot CA7 selects a partition and is not ordinary firmware activation.</p>
<p class="qa-citations">Sources: <a href="#ref-firmware">Base 2.4 §3.11–3.11.1, 5.2.9–5.2.10</a> · <a href="#ref-fwlog">Base 2.4 §5.2.13.1.4</a> · <a href="#ref-boot">Base 2.4 §8.1.3–8.1.3.3.3</a> · <a href="#ref-bootreg">Base 2.4 §3.1.4 (BPINFO, BPRSEL, BPMBL)</a> · <a href="#ref-bootprotect">Base 2.4 §5.2.30.1.39</a></p>
</section>
<div class="qa-controls" hidden><label>Search this page <input type="search" id="qa-search" placeholder="Question number, field or keyword"></label><button type="button" data-expand="true">Expand all answers</button><button type="button" data-expand="false">Collapse all answers</button><output id="qa-count" aria-live="polite"></output></div>
<section id="question-index"><h2>Questions in this volume</h2><ol class="qa-index">
<li><a href="#q-136">Q136 · Where are firmware slot count, protection and usage reported?</a></li>
<li><a href="#q-137">Q137 · How do OFST and NUMD describe firmware download pieces?</a></li>
<li><a href="#q-138">Q138 · How are overlap, gaps, order and invalid images handled?</a></li>
<li><a href="#q-139">Q139 · How are Firmware Commit slot and action selected?</a></li>
<li><a href="#q-140">Q140 · How do immediate and reset-triggered activation differ?</a></li>
<li><a href="#q-141">Q141 · When is Firmware Activation Starting reported?</a></li>
<li><a href="#q-142">Q142 · How are firmware-update interruptions recovered?</a></li>
<li><a href="#q-143">Q143 · How does firmware-load failure recovery work?</a></li>
<li><a href="#q-144">Q144 · How is completed activation verified?</a></li>
<li><a href="#q-145">Q145 · What should persist or be rediscovered after activation?</a></li>
<li><a href="#q-146">Q146 · How are boot partition support, state and active ID discovered?</a></li>
<li><a href="#q-147">Q147 · How are boot images downloaded, committed and selected?</a></li>
<li><a href="#q-148">Q148 · How do boot and controller-firmware updates differ?</a></li>
</ol></section>
<article class="qa-question" id="q-136" data-question="136"><h2><a class="qa-qid" href="#q-136">Q136</a> Where are firmware slot count, protection and usage reported?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-136-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-136-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>The original premise needs correction: the log reports contents/activation, while Identify.FRMW reports slot count and slot 1 read-only capability.</p>
</li>
<li id="q-136-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Firmware slots are shared within a domain; identify the update domain first.</p>
</li>
<li id="q-136-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>OACS advertises firmware commands; FRMW reports slot count, slot 1 protection and reset-free activation capability.</p>
</li>
<li id="q-136-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>LID 03h CAFS is current slot, NAFS the pending next-reset slot and FRS1–7 the slot revisions.</p>
</li>
<li id="q-136-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Read FRMW then LID 03h and choose a writable slot; do not probe protection by attempting overwrite.</p>
</li>
<li id="q-136-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Establish count, populated slots, running slot and pending activation separately.</p>
</li>
<li id="q-136-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>All-zero revision can mean empty or unsupported and cannot establish count; invalid/read-only slots use Invalid Firmware Slot.</p>
</li>
<li id="q-136-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-136-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Starting reset-free activation triggers Firmware Activation Starting on affected controllers when notices are enabled. <a class="qa-rule-link" href="#common-firmware_op-9">Full rule in this volume</a></p>
</li>
<li id="q-136-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Distinguish active and next-reset slots with Firmware Slot Information and confirm running revision through Identify.FR. <a class="qa-rule-link" href="#common-firmware_op-10">Full rule in this volume</a></p>
</li>
<li id="q-136-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>PEL Commit 02h records old/requested revisions, action, slot and status. <a class="qa-rule-link" href="#common-firmware_op-11">Full rule in this volume</a></p>
</li>
<li id="q-136-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>A CLR between download and completed Commit discards staged portions. <a class="qa-rule-link" href="#common-firmware_op-12">Full rule in this volume</a></p>
</li>
<li id="q-136-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Subsystem reset affects its covered controllers and satisfies a required subsystem-reset activation. <a class="qa-rule-link" href="#common-firmware_op-13">Full rule in this volume</a></p>
</li>
<li id="q-136-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Entering D3cold during activation Commit can resume with the old or newly activated image; verify it. <a class="qa-rule-link" href="#common-firmware_op-14">Full rule in this volume</a></p>
</li>
<li id="q-136-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Controllers in one domain share slots/image, covering the subsystem in a single-domain system. <a class="qa-rule-link" href="#common-firmware_op-15">Full rule in this volume</a></p>
</li>
<li id="q-136-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Identify.FR reflects the running image, not automatically the pending slot revision.</p>
</li>
<li id="q-136-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First read FRMW before interpreting an empty slot as nonexistent.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-firmware">Base 2.4 §3.11–3.11.1, 5.2.9–5.2.10</a> · <a href="#ref-fwlog">Base 2.4 §5.2.13.1.4</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-fwpel">Base 2.4 §5.2.13.1.14.2.2, 5.2.13.1.14.2.4</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-137" data-question="137"><h2><a class="qa-qid" href="#q-137">Q137</a> How do OFST and NUMD describe firmware download pieces?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-137-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-137-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Segmentation avoids transferring an entire image at once but requires correct positions and lengths.</p>
</li>
<li id="q-137-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>OFST is relative to the whole image, not the host buffer for the current piece.</p>
</li>
<li id="q-137-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Check FWUG alignment/granularity and applicable transfer limits such as MDTS, honoring FWUG special values.</p>
</li>
<li id="q-137-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>OFST counts Dwords and NUMD is zero-based Dword length: byte start=OFST×4 and length=(NUMD+1)×4.</p>
</li>
<li id="q-137-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>For 4096-byte pieces use OFST0/NUMD1023 then OFST1024/NUMD1023 with each pointer addressing that piece.</p>
</li>
<li id="q-137-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Download success completes the piece, not Commit or activation.</p>
</li>
<li id="q-137-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>FWUG violations may return Invalid Field and overlaps Overlapping Range; unit mistakes create misplaced data and gaps.</p>
</li>
<li id="q-137-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-137-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Starting reset-free activation triggers Firmware Activation Starting on affected controllers when notices are enabled. <a class="qa-rule-link" href="#common-firmware_op-9">Full rule in this volume</a></p>
</li>
<li id="q-137-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Distinguish active and next-reset slots with Firmware Slot Information and confirm running revision through Identify.FR. <a class="qa-rule-link" href="#common-firmware_op-10">Full rule in this volume</a></p>
</li>
<li id="q-137-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>PEL Commit 02h records old/requested revisions, action, slot and status. <a class="qa-rule-link" href="#common-firmware_op-11">Full rule in this volume</a></p>
</li>
<li id="q-137-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>A CLR between download and completed Commit discards staged portions. <a class="qa-rule-link" href="#common-firmware_op-12">Full rule in this volume</a></p>
</li>
<li id="q-137-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Subsystem reset affects its covered controllers and satisfies a required subsystem-reset activation. <a class="qa-rule-link" href="#common-firmware_op-13">Full rule in this volume</a></p>
</li>
<li id="q-137-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Entering D3cold during activation Commit can resume with the old or newly activated image; verify it. <a class="qa-rule-link" href="#common-firmware_op-14">Full rule in this volume</a></p>
</li>
<li id="q-137-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Controllers in one domain share slots/image, covering the subsystem in a single-domain system. <a class="qa-rule-link" href="#common-firmware_op-15">Full rule in this volume</a></p>
</li>
<li id="q-137-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Verify complete coverage from each range and compare with the source image.</p>
</li>
<li id="q-137-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First check the zero-based length and Dword offset units.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-firmware">Base 2.4 §3.11–3.11.1, 5.2.9–5.2.10</a> · <a href="#ref-fwlog">Base 2.4 §5.2.13.1.4</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-fwpel">Base 2.4 §5.2.13.1.14.2.2, 5.2.13.1.14.2.4</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-138" data-question="138"><h2><a class="qa-qid" href="#q-138">Q138</a> How are overlap, gaps, order and invalid images handled?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-138-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-138-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Separate segment-transfer errors from whole-image validation; successful pieces can still form an invalid incomplete image.</p>
</li>
<li id="q-138-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Keep one image per update sequence and use the same controller; avoid interleaving firmware/boot updates.</p>
</li>
<li id="q-138-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Check FWUG, image requirements and supported multiple-update detection.</p>
</li>
<li id="q-138-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>Firmware pieces may arrive out of order; boot pieces must be ordered from the start. Range overlap and MUD sequence-overlap reporting are distinct.</p>
</li>
<li id="q-138-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Track ranges and successful transfers, verify no gaps/overlap, Commit, then begin the next image.</p>
</li>
<li id="q-138-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>A valid complete image proceeds through Commit; individual pieces need not validate the complete image.</p>
</li>
<li id="q-138-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Overlap may use 1/14h and invalid Commit image 1/07h. Overlapping update sequences can have undefined results, not a universal recovery status.</p>
</li>
<li id="q-138-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-138-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Starting reset-free activation triggers Firmware Activation Starting on affected controllers when notices are enabled. <a class="qa-rule-link" href="#common-firmware_op-9">Full rule in this volume</a></p>
</li>
<li id="q-138-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Distinguish active and next-reset slots with Firmware Slot Information and confirm running revision through Identify.FR. <a class="qa-rule-link" href="#common-firmware_op-10">Full rule in this volume</a></p>
</li>
<li id="q-138-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>PEL Commit 02h records old/requested revisions, action, slot and status. <a class="qa-rule-link" href="#common-firmware_op-11">Full rule in this volume</a></p>
</li>
<li id="q-138-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>A CLR between download and completed Commit discards staged portions. <a class="qa-rule-link" href="#common-firmware_op-12">Full rule in this volume</a></p>
</li>
<li id="q-138-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Subsystem reset affects its covered controllers and satisfies a required subsystem-reset activation. <a class="qa-rule-link" href="#common-firmware_op-13">Full rule in this volume</a></p>
</li>
<li id="q-138-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Entering D3cold during activation Commit can resume with the old or newly activated image; verify it. <a class="qa-rule-link" href="#common-firmware_op-14">Full rule in this volume</a></p>
</li>
<li id="q-138-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Controllers in one domain share slots/image, covering the subsystem in a single-domain system. <a class="qa-rule-link" href="#common-firmware_op-15">Full rule in this volume</a></p>
</li>
<li id="q-138-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Preserve ranges and Commit results to separate transfer completion, completeness and activation validity.</p>
</li>
<li id="q-138-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First check whether firmware and boot ordering rules were interchanged.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-boot">Base 2.4 §8.1.3–8.1.3.3.3</a> · <a href="#ref-firmware">Base 2.4 §3.11–3.11.1, 5.2.9–5.2.10</a> · <a href="#ref-fwlog">Base 2.4 §5.2.13.1.4</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-fwpel">Base 2.4 §5.2.13.1.14.2.2, 5.2.13.1.14.2.4</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-139" data-question="139"><h2><a class="qa-qid" href="#q-139">Q139</a> How are Firmware Commit slot and action selected?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-139-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-139-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Commit can store, schedule or activate immediately, depending on the update plan and capability.</p>
</li>
<li id="q-139-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>FS selects firmware slots while BPID selects boot partitions.</p>
</li>
<li id="q-139-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Read FRMW, active/pending slots and MTFA before choosing reset-free activation.</p>
</li>
<li id="q-139-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>CA0 stores only,1 stores/schedules CLR activation,2 schedules an existing slot and 3 activates immediately. FS0 lets the controller select a slot 1–7.</p>
</li>
<li id="q-139-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Download when needed, then Commit; activating an existing stored image need not redownload it.</p>
</li>
<li id="q-139-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>CA0 leaves the running version unchanged, CA1/2 await reset and CA3 remains outstanding until activation succeeds or fails.</p>
</li>
<li id="q-139-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Invalid/read-only slots and images have distinct errors; required-reset statuses can indicate successful storage with activation still pending.</p>
</li>
<li id="q-139-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-139-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Starting reset-free activation triggers Firmware Activation Starting on affected controllers when notices are enabled. <a class="qa-rule-link" href="#common-firmware_op-9">Full rule in this volume</a></p>
</li>
<li id="q-139-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Distinguish active and next-reset slots with Firmware Slot Information and confirm running revision through Identify.FR. <a class="qa-rule-link" href="#common-firmware_op-10">Full rule in this volume</a></p>
</li>
<li id="q-139-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>PEL Commit 02h records old/requested revisions, action, slot and status. <a class="qa-rule-link" href="#common-firmware_op-11">Full rule in this volume</a></p>
</li>
<li id="q-139-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>A CLR between download and completed Commit discards staged portions. <a class="qa-rule-link" href="#common-firmware_op-12">Full rule in this volume</a></p>
</li>
<li id="q-139-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Subsystem reset affects its covered controllers and satisfies a required subsystem-reset activation. <a class="qa-rule-link" href="#common-firmware_op-13">Full rule in this volume</a></p>
</li>
<li id="q-139-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Entering D3cold during activation Commit can resume with the old or newly activated image; verify it. <a class="qa-rule-link" href="#common-firmware_op-14">Full rule in this volume</a></p>
</li>
<li id="q-139-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Controllers in one domain share slots/image, covering the subsystem in a single-domain system. <a class="qa-rule-link" href="#common-firmware_op-15">Full rule in this volume</a></p>
</li>
<li id="q-139-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Derive FR/CAFS/NAFS expectations from CA rather than demanding immediate FR change for every action.</p>
</li>
<li id="q-139-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First inspect CA before diagnosing a store-only operation as activation failure.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-firmware">Base 2.4 §3.11–3.11.1, 5.2.9–5.2.10</a> · <a href="#ref-fwlog">Base 2.4 §5.2.13.1.4</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-fwpel">Base 2.4 §5.2.13.1.14.2.2, 5.2.13.1.14.2.4</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-140" data-question="140"><h2><a class="qa-qid" href="#q-140">Q140</a> How do immediate and reset-triggered activation differ?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-140-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-140-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Immediate activation can preserve the operating environment, but image changes may require reset; honor the reported reset type.</p>
</li>
<li id="q-140-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Activation covers the domain, while the chosen reset can have broader scope.</p>
</li>
<li id="q-140-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Check reset-free capability, MTFA and Commit status; capability does not guarantee every image qualifies.</p>
</li>
<li id="q-140-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>Required resets use 1/0Bh,1/10h and 1/11h;1/12h means activation exceeds MTFA, leaving the image committed but inactive.</p>
</li>
<li id="q-140-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>After CA3 success check the new revision; otherwise perform the required reset and reinitialize. A narrower reset does not satisfy a stronger requirement.</p>
</li>
<li id="q-140-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>CA1/2 success allows activation by applicable CLR methods; explicit Conventional/Subsystem requirements narrow the trigger.</p>
</li>
<li id="q-140-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>If Conventional Reset was required, clearing CC.EN alone leaves the old image running and unchanged FR is expected.</p>
</li>
<li id="q-140-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-140-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Starting reset-free activation triggers Firmware Activation Starting on affected controllers when notices are enabled. <a class="qa-rule-link" href="#common-firmware_op-9">Full rule in this volume</a></p>
</li>
<li id="q-140-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Distinguish active and next-reset slots with Firmware Slot Information and confirm running revision through Identify.FR. <a class="qa-rule-link" href="#common-firmware_op-10">Full rule in this volume</a></p>
</li>
<li id="q-140-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>PEL Commit 02h records old/requested revisions, action, slot and status. <a class="qa-rule-link" href="#common-firmware_op-11">Full rule in this volume</a></p>
</li>
<li id="q-140-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>A CLR between download and completed Commit discards staged portions. <a class="qa-rule-link" href="#common-firmware_op-12">Full rule in this volume</a></p>
</li>
<li id="q-140-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Subsystem reset affects its covered controllers and satisfies a required subsystem-reset activation. <a class="qa-rule-link" href="#common-firmware_op-13">Full rule in this volume</a></p>
</li>
<li id="q-140-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Entering D3cold during activation Commit can resume with the old or newly activated image; verify it. <a class="qa-rule-link" href="#common-firmware_op-14">Full rule in this volume</a></p>
</li>
<li id="q-140-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Controllers in one domain share slots/image, covering the subsystem in a single-domain system. <a class="qa-rule-link" href="#common-firmware_op-15">Full rule in this volume</a></p>
</li>
<li id="q-140-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Correlate CA, status, actual reset source and recovered FR.</p>
</li>
<li id="q-140-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First identify the actual reset type rather than the host operation’s generic name.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-firmware">Base 2.4 §3.11–3.11.1, 5.2.9–5.2.10</a> · <a href="#ref-fwlog">Base 2.4 §5.2.13.1.4</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-fwpel">Base 2.4 §5.2.13.1.14.2.2, 5.2.13.1.14.2.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-141" data-question="141"><h2><a class="qa-qid" href="#q-141">Q141</a> When is Firmware Activation Starting reported?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-141-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-141-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>The event announces reset-free activation and possible processing pause, not successful completion.</p>
</li>
<li id="q-141-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Affected controllers report according to their notification settings, not solely the Commit recipient.</p>
</li>
<li id="q-141-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Check enabled activation notices, posted AERs and activation capabilities/timing.</p>
</li>
<li id="q-141-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>The Notice event points to LID 03h; CSTS.PP reports processing pause.</p>
</li>
<li id="q-141-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Handle the event at activation start, observe processing recovery, then check Commit and FR.</p>
</li>
<li id="q-141-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Success requires the relevant completion and running revision; Starting establishes initiation only.</p>
</li>
<li id="q-141-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Disabled notices or unavailable AERs alter notification observation; load failure has its own error event.</p>
</li>
<li id="q-141-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-141-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Starting reset-free activation triggers Firmware Activation Starting on affected controllers when notices are enabled. <a class="qa-rule-link" href="#common-firmware_op-9">Full rule in this volume</a></p>
</li>
<li id="q-141-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Distinguish active and next-reset slots with Firmware Slot Information and confirm running revision through Identify.FR. <a class="qa-rule-link" href="#common-firmware_op-10">Full rule in this volume</a></p>
</li>
<li id="q-141-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>PEL Commit 02h records old/requested revisions, action, slot and status. <a class="qa-rule-link" href="#common-firmware_op-11">Full rule in this volume</a></p>
</li>
<li id="q-141-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>A CLR between download and completed Commit discards staged portions. <a class="qa-rule-link" href="#common-firmware_op-12">Full rule in this volume</a></p>
</li>
<li id="q-141-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Subsystem reset affects its covered controllers and satisfies a required subsystem-reset activation. <a class="qa-rule-link" href="#common-firmware_op-13">Full rule in this volume</a></p>
</li>
<li id="q-141-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Entering D3cold during activation Commit can resume with the old or newly activated image; verify it. <a class="qa-rule-link" href="#common-firmware_op-14">Full rule in this volume</a></p>
</li>
<li id="q-141-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Controllers in one domain share slots/image, covering the subsystem in a single-domain system. <a class="qa-rule-link" href="#common-firmware_op-15">Full rule in this volume</a></p>
</li>
<li id="q-141-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Correlate event timing, PP and completion to distinguish activation stalls from unhandled notifications.</p>
</li>
<li id="q-141-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First check the activation-notice configuration, not merely whether an AER was submitted.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-aerfull">Base 2.4 §5.2.2 (PCIe-applicable events)</a> · <a href="#ref-aec">Base 2.4 §5.2.30.1.6</a> · <a href="#ref-cc">Base 2.4 §3.1.4 (CC, CSTS, NSSR)</a> · <a href="#ref-firmware">Base 2.4 §3.11–3.11.1, 5.2.9–5.2.10</a> · <a href="#ref-fwlog">Base 2.4 §5.2.13.1.4</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-fwpel">Base 2.4 §5.2.13.1.14.2.2, 5.2.13.1.14.2.4</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-142" data-question="142"><h2><a class="qa-qid" href="#q-142">Q142</a> How are firmware-update interruptions recovered?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-142-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-142-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Staging, committing and activation have different persistence; identify the interruption stage first.</p>
</li>
<li id="q-142-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Storage and activation are domain-wide and interruption can affect its shared controllers.</p>
</li>
<li id="q-142-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Preserve last completed transfers/Commit, CA/FS and revision/slot snapshots, then reread after recovery.</p>
</li>
<li id="q-142-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>CLR between download and completed Commit discards staging; D3cold during activation Commit may resume with old or new firmware.</p>
</li>
<li id="q-142-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Recover, inspect running/stored revisions and redownload uncommitted staging rather than assuming resumable offsets.</p>
</li>
<li id="q-142-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Decide completion/retry/recommit only after identifying running revision, pending state and capabilities.</p>
</li>
<li id="q-142-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Do not invent status for a lost CQE; retaining old firmware can be a valid interrupted-activation outcome.</p>
</li>
<li id="q-142-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-142-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Starting reset-free activation triggers Firmware Activation Starting on affected controllers when notices are enabled. <a class="qa-rule-link" href="#common-firmware_op-9">Full rule in this volume</a></p>
</li>
<li id="q-142-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Distinguish active and next-reset slots with Firmware Slot Information and confirm running revision through Identify.FR. <a class="qa-rule-link" href="#common-firmware_op-10">Full rule in this volume</a></p>
</li>
<li id="q-142-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>PEL Commit 02h records old/requested revisions, action, slot and status. <a class="qa-rule-link" href="#common-firmware_op-11">Full rule in this volume</a></p>
</li>
<li id="q-142-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>A CLR between download and completed Commit discards staged portions. <a class="qa-rule-link" href="#common-firmware_op-12">Full rule in this volume</a></p>
</li>
<li id="q-142-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Subsystem reset affects its covered controllers and satisfies a required subsystem-reset activation. <a class="qa-rule-link" href="#common-firmware_op-13">Full rule in this volume</a></p>
</li>
<li id="q-142-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Entering D3cold during activation Commit can resume with the old or newly activated image; verify it. <a class="qa-rule-link" href="#common-firmware_op-14">Full rule in this volume</a></p>
</li>
<li id="q-142-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Controllers in one domain share slots/image, covering the subsystem in a single-domain system. <a class="qa-rule-link" href="#common-firmware_op-15">Full rule in this volume</a></p>
</li>
<li id="q-142-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Use Commit/Reset PEL history but compare requested NFR with actual FR.</p>
</li>
<li id="q-142-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First identify the last completed Commit rather than the last downloaded piece.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-firmware">Base 2.4 §3.11–3.11.1, 5.2.9–5.2.10</a> · <a href="#ref-fwlog">Base 2.4 §5.2.13.1.4</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-fwpel">Base 2.4 §5.2.13.1.14.2.2, 5.2.13.1.14.2.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-143" data-question="143"><h2><a class="qa-qid" href="#q-143">Q143</a> How does firmware-load failure recovery work?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-143-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-143-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Recovery depends on available previously activated or baseline images when a new image cannot load.</p>
</li>
<li id="q-143-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Recovery affects controllers using the image; one slot alone does not describe full history.</p>
</li>
<li id="q-143-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Check FR, active/pending slots, revisions, load-error events and PEL.</p>
</li>
<li id="q-143-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>On load failure, revert to the most recently activated slot image or available read-only baseline and report Firmware Image Load Error.</p>
</li>
<li id="q-143-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Read recovered FR and failure evidence before attempting the same image again.</p>
</li>
<li id="q-143-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Running old firmware can demonstrate recovery while the attempted update remains failed.</p>
</li>
<li id="q-143-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Overwriting the active slot may remove the prior image; no guarantee exists of returning to any chosen historical revision.</p>
</li>
<li id="q-143-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-143-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Starting reset-free activation triggers Firmware Activation Starting on affected controllers when notices are enabled. <a class="qa-rule-link" href="#common-firmware_op-9">Full rule in this volume</a></p>
</li>
<li id="q-143-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Distinguish active and next-reset slots with Firmware Slot Information and confirm running revision through Identify.FR. <a class="qa-rule-link" href="#common-firmware_op-10">Full rule in this volume</a></p>
</li>
<li id="q-143-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>PEL Commit 02h records old/requested revisions, action, slot and status. <a class="qa-rule-link" href="#common-firmware_op-11">Full rule in this volume</a></p>
</li>
<li id="q-143-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>A CLR between download and completed Commit discards staged portions. <a class="qa-rule-link" href="#common-firmware_op-12">Full rule in this volume</a></p>
</li>
<li id="q-143-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Subsystem reset affects its covered controllers and satisfies a required subsystem-reset activation. <a class="qa-rule-link" href="#common-firmware_op-13">Full rule in this volume</a></p>
</li>
<li id="q-143-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Entering D3cold during activation Commit can resume with the old or newly activated image; verify it. <a class="qa-rule-link" href="#common-firmware_op-14">Full rule in this volume</a></p>
</li>
<li id="q-143-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Controllers in one domain share slots/image, covering the subsystem in a single-domain system. <a class="qa-rule-link" href="#common-firmware_op-15">Full rule in this volume</a></p>
</li>
<li id="q-143-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Compare actual slot/baseline availability rather than demanding rollback to unavailable content.</p>
</li>
<li id="q-143-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First check whether the active slot was overwritten.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-aerfull">Base 2.4 §5.2.2 (PCIe-applicable events)</a> · <a href="#ref-firmware">Base 2.4 §3.11–3.11.1, 5.2.9–5.2.10</a> · <a href="#ref-fwlog">Base 2.4 §5.2.13.1.4</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-fwpel">Base 2.4 §5.2.13.1.14.2.2, 5.2.13.1.14.2.4</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-144" data-question="144"><h2><a class="qa-qid" href="#q-144">Q144</a> How is completed activation verified?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-144-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-144-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Activation can change capabilities/effects; refresh caches rather than relying solely on revision text.</p>
</li>
<li id="q-144-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Compare the same affected controller/domain and namespace identities before and after.</p>
</li>
<li id="q-144-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Read FR/FRMW/CAP, slot information and relevant-CSI Commands Supported and Effects.</p>
</li>
<li id="q-144-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>CAFS identifies current slot, NAFS pending activation and FR running revision; Effects reports support and possible capability/inventory changes.</p>
</li>
<li id="q-144-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Establish activation completion, refresh capability and validate required commands/formats.</p>
</li>
<li id="q-144-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Running revision, active slot and activation outcome should agree; pending activation does not require early FR changes.</p>
</li>
<li id="q-144-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Diagnose readiness/media restrictions and new capability before declaring image corruption.</p>
</li>
<li id="q-144-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-144-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Starting reset-free activation triggers Firmware Activation Starting on affected controllers when notices are enabled. <a class="qa-rule-link" href="#common-firmware_op-9">Full rule in this volume</a></p>
</li>
<li id="q-144-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Distinguish active and next-reset slots with Firmware Slot Information and confirm running revision through Identify.FR. <a class="qa-rule-link" href="#common-firmware_op-10">Full rule in this volume</a></p>
</li>
<li id="q-144-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>PEL Commit 02h records old/requested revisions, action, slot and status. <a class="qa-rule-link" href="#common-firmware_op-11">Full rule in this volume</a></p>
</li>
<li id="q-144-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>A CLR between download and completed Commit discards staged portions. <a class="qa-rule-link" href="#common-firmware_op-12">Full rule in this volume</a></p>
</li>
<li id="q-144-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Subsystem reset affects its covered controllers and satisfies a required subsystem-reset activation. <a class="qa-rule-link" href="#common-firmware_op-13">Full rule in this volume</a></p>
</li>
<li id="q-144-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Entering D3cold during activation Commit can resume with the old or newly activated image; verify it. <a class="qa-rule-link" href="#common-firmware_op-14">Full rule in this volume</a></p>
</li>
<li id="q-144-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Controllers in one domain share slots/image, covering the subsystem in a single-domain system. <a class="qa-rule-link" href="#common-firmware_op-15">Full rule in this volume</a></p>
</li>
<li id="q-144-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Compare applicable fields and CSI rather than reserved or unrelated structures.</p>
</li>
<li id="q-144-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First exclude stale Identify/effects buffers.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-commandseffects">Base 2.4 §5.2.13.1.6</a> · <a href="#ref-firmware">Base 2.4 §3.11–3.11.1, 5.2.9–5.2.10</a> · <a href="#ref-fwlog">Base 2.4 §5.2.13.1.4</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-fwpel">Base 2.4 §5.2.13.1.14.2.2, 5.2.13.1.14.2.4</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-145" data-question="145"><h2><a class="qa-qid" href="#q-145">Q145</a> What should persist or be rediscovered after activation?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-145-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-145-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Do not require every byte to remain unchanged: capability can evolve while data/configuration obey their persistence rules.</p>
</li>
<li id="q-145-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Separate reset-free activation from actual reset, which independently changes queues, features and registers.</p>
</li>
<li id="q-145-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Compare feature saved/current/persistence, namespace identity/attachment, capabilities and UUID list.</p>
</li>
<li id="q-145-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>FR identifies the image, not feature restoration. Incompatible UUID-slot changes can require reset to avoid reinterpreting old indices.</p>
</li>
<li id="q-145-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Snapshot before update, record activation/reset path, compare each function’s persistence and restore required host state.</p>
</li>
<li id="q-145-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Validate the actual activation/reset path, distinguishing permitted capability changes from improper data/configuration loss.</p>
</li>
<li id="q-145-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Firmware change does not justify arbitrary loss, nor does updating preserve queues across a real reset.</p>
</li>
<li id="q-145-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-145-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Starting reset-free activation triggers Firmware Activation Starting on affected controllers when notices are enabled. <a class="qa-rule-link" href="#common-firmware_op-9">Full rule in this volume</a></p>
</li>
<li id="q-145-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Distinguish active and next-reset slots with Firmware Slot Information and confirm running revision through Identify.FR. <a class="qa-rule-link" href="#common-firmware_op-10">Full rule in this volume</a></p>
</li>
<li id="q-145-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>PEL Commit 02h records old/requested revisions, action, slot and status. <a class="qa-rule-link" href="#common-firmware_op-11">Full rule in this volume</a></p>
</li>
<li id="q-145-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>A CLR between download and completed Commit discards staged portions. <a class="qa-rule-link" href="#common-firmware_op-12">Full rule in this volume</a></p>
</li>
<li id="q-145-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Subsystem reset affects its covered controllers and satisfies a required subsystem-reset activation. <a class="qa-rule-link" href="#common-firmware_op-13">Full rule in this volume</a></p>
</li>
<li id="q-145-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Entering D3cold during activation Commit can resume with the old or newly activated image; verify it. <a class="qa-rule-link" href="#common-firmware_op-14">Full rule in this volume</a></p>
</li>
<li id="q-145-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Controllers in one domain share slots/image, covering the subsystem in a single-domain system. <a class="qa-rule-link" href="#common-firmware_op-15">Full rule in this volume</a></p>
</li>
<li id="q-145-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Map differences to requirements: changed capability, retained values and rebuilt state.</p>
</li>
<li id="q-145-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First establish whether CLR occurred before setting persistence expectations.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-uuid">Base 2.4 §8.1.31.1–8.1.31.2</a> · <a href="#ref-idns">NVM Command Set 1.3 §4.1.5.1–4.1.5.4</a> · <a href="#ref-firmware">Base 2.4 §3.11–3.11.1, 5.2.9–5.2.10</a> · <a href="#ref-fwlog">Base 2.4 §5.2.13.1.4</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-fwpel">Base 2.4 §5.2.13.1.14.2.2, 5.2.13.1.14.2.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-146" data-question="146"><h2><a class="qa-qid" href="#q-146">Q146</a> How are boot partition support, state and active ID discovered?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-146-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-146-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Boot partitions provide pre-queue/pre-enable image access through a simplified interface, not ordinary namespace LBAs.</p>
</li>
<li id="q-146-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Supported controllers expose two equal partitions, IDs 0/1, potentially shared across controllers.</p>
</li>
<li id="q-146-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Read CAP.BPS and BPINFO.ABPID/BPSZ/BRS, Identify.BPC for protection and supported LID 15h for log access.</p>
</li>
<li id="q-146-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>BPMBL supplies buffer address, BPRSEL selects partition/range and BRS reports transfer state.</p>
</li>
<li id="q-146-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Allocate contiguous memory, ensure no read is active, configure address/selection and wait for BRS; do not reset/shutdown/change transport properties during the read.</p>
</li>
<li id="q-146-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>BRS10b indicates transferred data and 11b transfer error; the register-based flow has no NVMe CQE.</p>
</li>
<li id="q-146-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Do not invent Invalid Field CQEs for BPRSEL writes; the log path separately follows Get Log completion rules.</p>
</li>
<li id="q-146-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>The register path has no DNR/More; LID 15h uses its Get Log Page CQE.</p>
</li>
<li id="q-146-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Boot register reads have no success AER; log-read success does not trigger Firmware Activation Starting.</p>
</li>
<li id="q-146-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Register reads report through BRS, without updating firmware-slot history; the log path returns selected boot data and uses its own CQE/error rules.</p>
</li>
<li id="q-146-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>Ordinary boot reads are not Firmware Commit events; actual Commit completion follows PEL rules.</p>
</li>
<li id="q-146-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>Boot contents are not cleared like queue state, but the host must not reset during an active register read. Recheck properties/state afterward.</p>
</li>
<li id="q-146-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Rediscover partitions and read state after subsystem reset; reset is not boot-image erasure and does not validate an incomplete buffer.</p>
</li>
<li id="q-146-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Boot images persist in nonvolatile storage and can be reread after power cycling; FID 85h defaults to Write Locked independently of image contents.</p>
</li>
<li id="q-146-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Controllers may share partitions, but one controller’s completed transfer does not complete another’s buffer.</p>
</li>
<li id="q-146-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Verify capability, selected active ID, size, status and content; ABPID alone does not validate the image.</p>
</li>
<li id="q-146-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First distinguish register and log interfaces before applying offset/completion semantics.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-boot">Base 2.4 §8.1.3–8.1.3.3.3</a> · <a href="#ref-bootreg">Base 2.4 §3.1.4 (BPINFO, BPRSEL, BPMBL)</a> · <a href="#ref-bootlog">Base 2.4 §5.2.13.1.21</a> · <a href="#ref-bootprotect">Base 2.4 §5.2.30.1.39</a> · <a href="#ref-firmware">Base 2.4 §3.11–3.11.1, 5.2.9–5.2.10</a> · <a href="#ref-fwlog">Base 2.4 §5.2.13.1.4</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-fwpel">Base 2.4 §5.2.13.1.14.2.2, 5.2.13.1.14.2.4</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-147" data-question="147"><h2><a class="qa-qid" href="#q-147">Q147</a> How are boot images downloaded, committed and selected?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-147-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-147-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Two partitions allow updating and verifying the inactive image before selection, reducing interrupted-update risk.</p>
</li>
<li id="q-147-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>BPID selects the written/activated partition, with protection enforced by all sharing controllers.</p>
</li>
<li id="q-147-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Check BPS/BPC, ABPID and the active protection mechanism; FID 85h and RPMB do not simultaneously control protection.</p>
</li>
<li id="q-147-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>Download in order; CommitCA6 replaces the selected partition and CA7 selects it active.</p>
</li>
<li id="q-147-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Download, unlock target, commitCA6, verify, selectCA7 and restore protection.</p>
</li>
<li id="q-147-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>CA6 success writes the partition without necessarily changing ABPID; verify ABPID after CA7.</p>
</li>
<li id="q-147-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Locked writes use Boot Partition Write Prohibited; reset/power interruption can leave mixed contents requiring verification before activation.</p>
</li>
<li id="q-147-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-147-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>BootCA6/CA7 are not controller-firmware activation and do not require Firmware Activation Starting.</p>
</li>
<li id="q-147-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Verify commit, ABPID, boot-data readback and protection; firmware-slot information is not a boot-image inventory.</p>
</li>
<li id="q-147-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>PEL Commit 02h records old/requested revisions, action, slot and status. <a class="qa-rule-link" href="#common-firmware_op-11">Full rule in this volume</a></p>
</li>
<li id="q-147-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>CLR discards uncommitted staging; interrupted boot commit can leave old/new/mixed content and needs verification.</p>
</li>
<li id="q-147-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Subsystem-reset interruption does not guarantee atomic rollback; inspect active ID, protection and content.</p>
</li>
<li id="q-147-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>Power loss during boot commit can leave mixed content; the Set Features protection mechanism returns to Write Locked on a power cycle.</p>
</li>
<li id="q-147-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Shared boot partitions require coordinated update/protection across all sharing controllers.</p>
</li>
<li id="q-147-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Compare downloaded/readback content and ABPID separately.</p>
</li>
<li id="q-147-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First check whether onlyCA6 was performed while expecting automatic active selection.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-boot">Base 2.4 §8.1.3–8.1.3.3.3</a> · <a href="#ref-bootprotect">Base 2.4 §5.2.30.1.39</a> · <a href="#ref-bootreg">Base 2.4 §3.1.4 (BPINFO, BPRSEL, BPMBL)</a> · <a href="#ref-firmware">Base 2.4 §3.11–3.11.1, 5.2.9–5.2.10</a> · <a href="#ref-fwlog">Base 2.4 §5.2.13.1.4</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-fwpel">Base 2.4 §5.2.13.1.14.2.2, 5.2.13.1.14.2.4</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-148" data-question="148"><h2><a class="qa-qid" href="#q-148">Q148</a> How do boot and controller-firmware updates differ?</h2>
<p class="qa-prompt">First describe the normal sequence and one invalid-precondition example, then reveal the answer.</p>
<details class="qa-answer" id="q-148-answer"><summary>Reveal the full answer · 17 perspectives</summary><ol class="qa-items">
<li id="q-148-a-01" data-answer="1"><h3><span>01</span> What problem does this function solve?</h3>
<p>Boot images are for host booting; controller firmware runs the SSD. Shared download commands do not imply shared semantics.</p>
</li>
<li id="q-148-a-02" data-answer="2"><h3><span>02</span> What is its scope?</h3>
<p>Boot uses IDs 0/1; firmware uses slots 1–7 within a domain.</p>
</li>
<li id="q-148-a-03" data-answer="3"><h3><span>03</span> Which register, Identify field, feature or log page establishes support?</h3>
<p>Boot discovery uses BPS/BPC/BPINFO; firmware uses OACS/FRMW/MTFA and LID 03h.</p>
</li>
<li id="q-148-a-04" data-answer="4"><h3><span>04</span> Which commands and fields matter?</h3>
<p>Firmware download may be out of order withCA0–3; boot download is ordered withCA6/7.</p>
</li>
<li id="q-148-a-05" data-answer="5"><h3><span>05</span> What is the normal sequence?</h3>
<p>Identify the target before selecting capabilities, order, action and verification; do not interleave update sequences.</p>
</li>
<li id="q-148-a-06" data-answer="6"><h3><span>06</span> What indicates success?</h3>
<p>Verify firmware via running revision/slot and boot via content/ABPID; boot update does not require FR to change.</p>
</li>
<li id="q-148-a-07" data-answer="7"><h3><span>07</span> What status applies to unsupported, invalid or out-of-order requests?</h3>
<p>Interrupted boot commits can mix contents; firmware load failure has image fallback rules. Do not transfer guarantees between them.</p>
</li>
<li id="q-148-a-08" data-answer="8"><h3><span>08</span> How are DNR and More set?</h3>
<p>Applies to a CQE. No fixed DNR/More override is specified here; use the CQE bit rules in this volume. <a class="qa-rule-link" href="#common-command-8">Full rule in this volume</a></p>
</li>
<li id="q-148-a-09" data-answer="9"><h3><span>09</span> Is an asynchronous event generated?</h3>
<p>Reset-free controller-firmware activation follows the enabled Starting notice; Boot CA6/CA7 do not require that notice.</p>
</li>
<li id="q-148-a-10" data-answer="10"><h3><span>10</span> Are Error Information or other logs updated?</h3>
<p>Firmware uses slot information and running revision; boot uses ABPID, content and protection. Preserve target-specific commit/error evidence.</p>
</li>
<li id="q-148-a-11" data-answer="11"><h3><span>11</span> Is it recorded in the Persistent Event Log?</h3>
<p>PEL Commit 02h records old/requested revisions, action, slot and status. <a class="qa-rule-link" href="#common-firmware_op-11">Full rule in this volume</a></p>
</li>
<li id="q-148-a-12" data-answer="12"><h3><span>12</span> What survives or continues after Controller Reset?</h3>
<p>CLR discards uncommitted staging; committed firmware follows activation rules, while interrupted boot writes can leave mixed contents.</p>
</li>
<li id="q-148-a-13" data-answer="13"><h3><span>13</span> What survives or continues after NVM Subsystem Reset?</h3>
<p>Subsystem reset can satisfy firmware activation requirements but does not validate an interrupted boot write; inspect the appropriate result.</p>
</li>
<li id="q-148-a-14" data-answer="14"><h3><span>14</span> What survives or continues after a power cycle?</h3>
<p>After power loss verify actual firmware/fallback or potentially mixed boot contents; power restoration alone proves neither update successful.</p>
</li>
<li id="q-148-a-15" data-answer="15"><h3><span>15</span> Are other controllers or namespaces affected?</h3>
<p>Coordinate the firmware domain or all controllers sharing a boot partition, not only the submitting path.</p>
</li>
<li id="q-148-a-16" data-answer="16"><h3><span>16</span> Are Identify, features, logs and command behavior consistent?</h3>
<p>Record target-specific state/persistence rather than conflating boot Active selection with firmware CAFS.</p>
</li>
<li id="q-148-a-17" data-answer="17"><h3><span>17</span> What should be checked first when the result differs?</h3>
<p>First determine whether the host boots from the image or the SSD controller executes it.</p>
</li>
</ol>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-boot">Base 2.4 §8.1.3–8.1.3.3.3</a> · <a href="#ref-bootprotect">Base 2.4 §5.2.30.1.39</a> · <a href="#ref-firmware">Base 2.4 §3.11–3.11.1, 5.2.9–5.2.10</a> · <a href="#ref-fwlog">Base 2.4 §5.2.13.1.4</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-fwpel">Base 2.4 §5.2.13.1.14.2.2, 5.2.13.1.14.2.4</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<section id="common-rules" class="qa-common"><h2>Shared rules linked from the answers</h2><p>Each shared mechanism is explained in full once in this volume. Use browser Back to return to the question; explicit command or feature exceptions take precedence.</p>
<article id="common-command-8"><h3>Command completion, events and records · How are DNR and More set?</h3><p>For a CQE, DNR=1 means the identical command is expected to fail if resubmitted to any controller in this subsystem; DNR=0 means it may succeed. Do not assign DNR=1 solely from an error name unless that condition mandates it. More=1 identifies additional information for this command in the Error Information Log. DNR should be zero when SCT=SC=0.</p></article>
<article id="common-firmware_op-9"><h3>Shared conditions for this topic · Is an asynchronous event generated?</h3><p>Starting reset-free activation triggers Firmware Activation Starting on affected controllers when notices are enabled. Load failure has a separate error event; each successful download segment does not trigger activation.</p></article>
<article id="common-firmware_op-10"><h3>Shared conditions for this topic · Are Error Information or other logs updated?</h3><p>Distinguish active and next-reset slots with Firmware Slot Information and confirm running revision through Identify.FR. Use More for error details; stored does not mean executing.</p></article>
<article id="common-firmware_op-11"><h3>Shared conditions for this topic · Is it recorded in the Persistent Event Log?</h3><p>PEL Commit 02h records old/requested revisions, action, slot and status. Requested NFR is not proof of activation; Reset-event FA/FREV provide outcome evidence.</p></article>
<article id="common-firmware_op-12"><h3>Shared conditions for this topic · What survives or continues after Controller Reset?</h3><p>A CLR between download and completed Commit discards staged portions. Committed slots/pending activation follow CA and required reset type; not every reset activates the image.</p></article>
<article id="common-firmware_op-13"><h3>Shared conditions for this topic · What survives or continues after NVM Subsystem Reset?</h3><p>Subsystem reset affects its covered controllers and satisfies a required subsystem-reset activation. Recheck revision, slots and capabilities; uncommitted staging cannot be reused.</p></article>
<article id="common-firmware_op-14"><h3>Shared conditions for this topic · What survives or continues after a power cycle?</h3><p>Entering D3cold during activation Commit can resume with the old or newly activated image; verify it. Uncommitted downloaded portions are not a persistent slot.</p></article>
<article id="common-firmware_op-15"><h3>Shared conditions for this topic · Are other controllers or namespaces affected?</h3><p>Controllers in one domain share slots/image, covering the subsystem in a single-domain system. Coordinate affected accessors and avoid overlapping update sequences.</p></article>
</section>
<section id="source-index"><h2>Source locations and existing figure guides</h2><p>Base printed page = PDF page−26; the other two use identical numbers. Locations follow the supplied PDF body and retain figure numbers. Shared pages contribute only the relevant definitions, excluding Fabrics and PCIe link/packet content.</p><ul class="qa-references">
<li id="ref-cc"><strong>Base 2.4 · §3.1.4 (CC, CSTS, NSSR)</strong><br>Printed pages 60–66 · PDF 86–92 · Figure 41–43</li>
<li id="ref-bootreg"><strong>Base 2.4 · §3.1.4 (BPINFO, BPRSEL, BPMBL)</strong><br>Printed pages 69–70 · PDF 95–96 · Figure 49–51</li>
<li id="ref-reset"><strong>Base 2.4 · §3.7.1–3.7.4</strong><br>Printed pages 120–124 · PDF 146–150</li>
<li id="ref-firmware"><strong>Base 2.4 · §3.11–3.11.1, 5.2.9–5.2.10</strong><br>Printed pages 135–138, 202–206 · PDF 161–164, 228–232 · Figure 187–193</li>
<li id="ref-status"><strong>Base 2.4 · §4.2.3</strong><br>Printed pages 145–155 · PDF 171–181 · Figure 101–105</li>
<li id="ref-feature"><strong>Base 2.4 · §4.4</strong><br>Printed pages 166–169 · PDF 192–195 · Figure 126–127</li>
<li id="ref-aer"><strong>Base 2.4 · §5.2.2</strong><br>Printed pages 183–190 · PDF 209–216 · Figure 150–156</li>
<li id="ref-aerfull"><strong>Base 2.4 · §5.2.2 (PCIe-applicable events)</strong><br>Printed pages 183–191 · PDF 209–217 · Figure 150–160</li>
<li id="ref-error"><strong>Base 2.4 · §5.2.13.1.2</strong><br>Printed pages 218–220 · PDF 244–246 · Figure 212</li>
<li id="ref-fwlog"><strong>Base 2.4 · §5.2.13.1.4</strong><br>Printed pages 225–226 · PDF 251–252 · Figure 215</li>
<li id="ref-commandseffects"><strong>Base 2.4 · §5.2.13.1.6</strong><br>Printed pages 226–229 · PDF 252–255 · Figure 216–217</li>
<li id="ref-pel"><strong>Base 2.4 · §5.2.13.1.14 (header, reset, hardware, Set Feature events)</strong><br>Printed pages 244–256, 258, 262–264 · PDF 270–282, 284, 288–290 · Figure 232–244, 246, 252–253</li>
<li id="ref-fwpel"><strong>Base 2.4 · §5.2.13.1.14.2.2, 5.2.13.1.14.2.4</strong><br>Printed pages 252–255 · PDF 278–281 · Figure 238, 240–241</li>
<li id="ref-bootlog"><strong>Base 2.4 · §5.2.13.1.21</strong><br>Printed pages 283–284 · PDF 309–310 · Figure 279–280</li>
<li id="ref-idctrl"><strong>Base 2.4 · §5.2.14.2.1</strong><br>Printed pages 340–387 · PDF 366–413 · Figure 338–341</li>
<li id="ref-aec"><strong>Base 2.4 · §5.2.30.1.6</strong><br>Printed pages 466–468 · PDF 492–494 · Figure 474</li>
<li id="ref-bootprotect"><strong>Base 2.4 · §5.2.30.1.39</strong><br>Printed pages 512–514 · PDF 538–540 · Figure 542</li>
<li id="ref-boot"><strong>Base 2.4 · §8.1.3–8.1.3.3.3</strong><br>Printed pages 586–592 · PDF 612–618 · Figure 679–683</li>
<li id="ref-uuid"><strong>Base 2.4 · §8.1.31.1–8.1.31.2</strong><br>Printed pages 737–738 · PDF 763–764 · Figure 782</li>
<li id="ref-idns"><strong>NVM Command Set 1.3 · §4.1.5.1–4.1.5.4</strong><br>Printed pages 84–107 · PDF 84–107 · Figure 123–130</li>
</ul><h3>When you need a field guide</h3><p>Existing figure explanations have canonical locations; use these links instead of duplicating the same guide.</p><ul>
<li><a href="/nvme/figure-reference/command/en/#figure-b101">Base 2.4 Figure 101 · Completion Queue Entry: Status Field</a></li>
<li><a href="/nvme/figure-reference/command/en/#figure-b104">Base 2.4 Figure 104 · Status Code – Command Specific Status Values</a></li>
<li><a href="/nvme/figure-reference/identify/en/#figure-b338">Base 2.4 Figure 338 · Identify – Identify Controller Data Structure, I/O Command Set Independent</a></li>
<li><a href="/nvme/figure-reference/init/en/#figure-b41">Base 2.4 Figure 41 · Offset 14h: CC – Controller Configuration</a></li>
<li><a href="/nvme/figure-reference/init/en/#figure-b42">Base 2.4 Figure 42 · Offset 1Ch: CSTS – Controller Status</a></li>
<li><a href="/nvme/figure-reference/identify/en/#figure-n123">NVM Command Set 1.3 Figure 123 · Identify – Identify Namespace Data Structure, NVM Command Set</a></li>
</ul><details><summary>Original documents used</summary><ul class="qr-sources">
<li>NVM Express Base Specification · Revision 2.4 · 2026-07-31<br><code>NVM-Express-Base-Specification-Revision-2.4-Ratified-2026.07.31.pdf</code></li>
<li>NVM Express NVM Command Set Specification · Revision 1.3 · 2026-07-31<br><code>NVM-Express-NVM-Command-Set-Specification-Revision-1.3-Ratified-2026.07.31.pdf</code></li>
<li>NVM Express NVMe over PCIe Transport Specification · Revision 1.4 · 2026-07-31<br><code>NVM-Express-NVMe-over-PCIe-Transport-Specification-Revision-1.4-Ratified-2026.07.31.pdf</code></li>
</ul></details></section>
</main>
<nav class="qr-top" aria-label="Bank and editions"><a href="#content">Skip to content</a><a href="/nvme/question-bank/en/">Question index</a><a href="/nvme/question-bank/firmware-boot/zh-tw/">繁體中文</a><a href="/DOCS/nvme-question-bank/firmware-boot.html">Chinese tutorial HTML</a></nav>
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
