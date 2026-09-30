---
layout: "post"
title: "NVMe Figure Reference 07 · Maintenance and Management"
date: "2026-09-29 09:00:00 +0800"
categories: ["nvme"]
tags: ["NVMe", "Reference"]
permalink: "/nvme/figure-reference/maintenance/en/"
nvme_quickref: true
lang: "en"
description: "NVMe source figures: uses, fields and interpretation with precise specification locations."
---

<div class="nvme-quickref">
<nav class="qr-top" aria-label="Editions and index"><a href="#content">Skip to content</a><a href="/nvme/figure-reference/en/">Index</a><a href="/nvme/figure-reference/maintenance/zh-tw/">繁體中文</a><a href="/DOCS/nvme-quick-reference/maintenance.html">Chinese HTML</a></nav>
<main id="content">
<header><p class="qr-eyebrow">LOOKUP · FIELD INTERPRETATION · SOURCE LOCATIONS</p><h1>NVMe Figure Reference 07 · Maintenance and Management</h1><p class="qr-intro">Separate the requested action, command completion and background result. Firmware commitment, namespace creation and acceptance of a Sanitize command each require different follow-up observations.</p></header>
<aside class="qr-note"><p>Each source figure has a use, field guide and worked interpretation. Example numbers are illustrative, not assumed device settings. Apply the conditions belonging to the field and command.</p><p>Use browser Find for fields, FID, LID, CNS or Figure. Positions follow the source: a byte is 8 bits and a Dword is 4 bytes. An index counts entries; an offset measures displacement from an origin in the specified unit.</p><p>FID (Feature Identifier) selects a feature; LID (Log Page Identifier) selects a log page; CNS (Controller or Namespace Structure) selects the structure returned by Identify.</p></aside>
<nav class="qr-toc" id="figure-index" aria-label="Volume figure index"><h2>Figures in this volume</h2><ol>
<li><a href="#figure-b187">Base 2.4 Figure 187 · Firmware Commit – Command Dword 10</a></li>
<li><a href="#figure-b191">Base 2.4 Figure 191 · Firmware Image Download – Command Dword 10</a></li>
<li><a href="#figure-b215">Base 2.4 Figure 215 · Firmware Slot Information Log Page</a></li>
<li><a href="#figure-b177">Base 2.4 Figure 177 · Device Self-test – Command Dword 10</a></li>
<li><a href="#figure-b218">Base 2.4 Figure 218 · Device Self-test Log Page</a></li>
<li><a href="#figure-b219">Base 2.4 Figure 219 · Self-test Result Data Structure</a></li>
<li><a href="#figure-b443">Base 2.4 Figure 443 · Namespace Attachment – Command Dword 10</a></li>
<li><a href="#figure-b446">Base 2.4 Figure 446 · Namespace Management – Command Dword 10</a></li>
<li><a href="#figure-n134">NVM Command Set 1.3 Figure 134 · Namespace Management – Host Specified Fields</a></li>
<li><a href="#figure-b195">Base 2.4 Figure 195 · Format NVM – Command Dword 10</a></li>
<li><a href="#figure-n91">NVM Command Set 1.3 Figure 91 · Format NVM – Command Dword 10 – NVM Command Set Specific Fields</a></li>
<li><a href="#figure-b451">Base 2.4 Figure 451 · Sanitize – Command Dword 10</a></li>
<li><a href="#figure-b454">Base 2.4 Figure 454 · Sanitize Namespace – Command Dword 10</a></li>
<li><a href="#figure-b312">Base 2.4 Figure 312 · Sanitize Status Log Page</a></li>
<li><a href="#figure-b541">Base 2.4 Figure 541 · Write Protection – Command Dword 11</a></li>
<li><a href="#figure-b542">Base 2.4 Figure 542 · Boot Partition Write Protection Config - Command Dword 11</a></li>
</ol></nav>
<article class="qr-card" id="figure-b187" data-figure="B187">
<h2><span class="qr-number">01</span>Firmware Commit – Command Dword 10</h2>
<p class="qr-original">Base 2.4 · Figure 187 · Firmware Commit – Command Dword 10</p>
<p class="qr-location">§5.2.9 · Printed pages 203 · PDF 229</p>
<p class="qr-explanation" data-paragraph="B187-1"><span class="qr-step">01.1 · Use</span>If a download did not change the running revision, inspect Commit Action to distinguish placement, activation after reset and immediate activation. Download and commit are separate steps.</p>
<p class="qr-explanation" data-paragraph="B187-2"><span class="qr-step">01.2 · Fields and relationships</span>FS bits 2:0 selects a slot, with zero letting the controller choose. CA bits 5:3 values 0/1/2/3 mean place without activation, place and activate at next Controller Level Reset, activate an existing slot at that reset, or activate immediately. CA=6/7 concern Boot Partitions with BPID bit 31.</p>
<p class="qr-explanation" data-paragraph="B187-3"><span class="qr-step">01.3 · Interpretation and example</span>After successful CA=1, the running firmware may still be old. Compare current and next-active slots and check whether completion specifies a particular reset requirement.</p>
<p class="qr-tags">Search terms: Firmware Commit · CA · FS · BPID · activate</p>
<div class="qr-related">Related lookups: <a href="/nvme/figure-reference/maintenance/en/#figure-b191">Base 2.4 Figure 191 · Firmware Image Download – Command Dword 10</a><a href="/nvme/figure-reference/maintenance/en/#figure-b215">Base 2.4 Figure 215 · Firmware Slot Information Log Page</a><a href="/nvme/figure-reference/command/en/#figure-b104">Base 2.4 Figure 104 · Status Code – Command Specific Status Values</a></div>
<a href="#figure-index">Back to this volume’s figure index</a></article>
<article class="qr-card" id="figure-b191" data-figure="B191">
<h2><span class="qr-number">02</span>Firmware Image Download – Command Dword 10</h2>
<p class="qr-original">Base 2.4 · Figure 191 · Firmware Image Download – Command Dword 10</p>
<p class="qr-location">§5.2.10 · Printed pages 205 · PDF 231</p>
<p class="qr-explanation" data-paragraph="B191-1"><span class="qr-step">02.1 · Use</span>Decode each firmware-download chunk length here. The whole-image size is not automatically the size of every command.</p>
<p class="qr-explanation" data-paragraph="B191-2"><span class="qr-step">02.2 · Fields and relationships</span>CDW10.NUMD bits 31:0 encodes Dword count minus one, giving 4×(NUMD+1) bytes. Combine it with CDW11.Offset and Identify.FWUG for chunk placement and granularity.</p>
<p class="qr-explanation" data-paragraph="B191-3"><span class="qr-step">02.3 · Interpretation and example</span>A4096-byte chunk uses NUMD=1023, not 4096. Record length and image offset separately; correct length alone does not satisfy offset or FWUG requirements.</p>
<p class="qr-tags">Search terms: Firmware Image Download · NUMD · FWUG · chunk</p>
<div class="qr-related">Related lookups: <a href="/nvme/figure-reference/maintenance/en/#figure-b187">Base 2.4 Figure 187 · Firmware Commit – Command Dword 10</a><a href="/nvme/figure-reference/identify/en/#figure-b338">Base 2.4 Figure 338 · Identify – Identify Controller Data Structure, I/O Command Set Independent</a></div>
<a href="#figure-index">Back to this volume’s figure index</a></article>
<article class="qr-card" id="figure-b215" data-figure="B215">
<h2><span class="qr-number">03</span>Firmware Slot Information Log Page</h2>
<p class="qr-original">Base 2.4 · Figure 215 · Firmware Slot Information Log Page</p>
<p class="qr-location">§5.2.13.1.4 · Printed pages 226 · PDF 252</p>
<p class="qr-explanation" data-paragraph="B215-1"><span class="qr-step">03.1 · Use</span>Use this log to distinguish stored and running firmware. A revision string in a slot does not make it active.</p>
<p class="qr-explanation" data-paragraph="B215-2"><span class="qr-step">03.2 · Fields and relationships</span>In AFI byte 0, CAFS bits 2:0 is the active slot and NAFS bits 6:4 the slot for the next reset able to activate it; NAFS=0 means unspecified. FRS1–7 are eight-byte revisions starting at byte 8.</p>
<p class="qr-explanation" data-paragraph="B215-3"><span class="qr-step">03.3 · Interpretation and example</span>CAFS=1/NAFS=2 with a new slot 2 revision means firmware was loaded from slot 1 while slot 2 awaits activation. A zero FRS can mean unsupported slot or no valid revision; it does not distinguish them.</p>
<p class="qr-tags">Search terms: LID 03h · AFI · CAFS · NAFS · FRS</p>
<div class="qr-related">Related lookups: <a href="/nvme/figure-reference/maintenance/en/#figure-b187">Base 2.4 Figure 187 · Firmware Commit – Command Dword 10</a></div>
<a href="#figure-index">Back to this volume’s figure index</a></article>
<article class="qr-card" id="figure-b177" data-figure="B177">
<h2><span class="qr-number">04</span>Device Self-test – Command Dword 10</h2>
<p class="qr-original">Base 2.4 · Figure 177 · Device Self-test – Command Dword 10</p>
<p class="qr-location">§5.2.6 · Printed pages 199 · PDF 225</p>
<p class="qr-explanation" data-paragraph="B177-1"><span class="qr-step">04.1 · Use</span>STC chooses the requested self-test action. Command completion differs from completion of the background test; inspect the log for its outcome.</p>
<p class="qr-explanation" data-paragraph="B177-2"><span class="qr-step">04.2 · Fields and relationships</span>CDW10.STC bits 3:0 values 1/2/3 start short, extended or Host-Initiated Refresh operations; Eh is vendor-specific and Fh aborts. NSID and capabilities separately determine target and applicability.</p>
<p class="qr-explanation" data-paragraph="B177-3"><span class="qr-step">04.3 · Interpretation and example</span>After a successful STC=2 submission, an extended test may still be in progress in the log. Admin CQE success is not proof that the test passed.</p>
<p class="qr-tags">Search terms: Device Self-test · STC · short · extended · Host-Initiated Refresh</p>
<div class="qr-related">Related lookups: <a href="/nvme/figure-reference/maintenance/en/#figure-b218">Base 2.4 Figure 218 · Device Self-test Log Page</a><a href="/nvme/figure-reference/maintenance/en/#figure-b219">Base 2.4 Figure 219 · Self-test Result Data Structure</a></div>
<a href="#figure-index">Back to this volume’s figure index</a></article>
<article class="qr-card" id="figure-b218" data-figure="B218">
<h2><span class="qr-number">05</span>Device Self-test Log Page</h2>
<p class="qr-original">Base 2.4 · Figure 218 · Device Self-test Log Page</p>
<p class="qr-location">§5.2.13.1.7 · Printed pages 230 · PDF 256</p>
<p class="qr-explanation" data-paragraph="B218-1"><span class="qr-step">05.1 · Use</span>This layout separates the current operation from historical outcomes. The first two bytes describe progress; the result list describes success or failure.</p>
<p class="qr-explanation" data-paragraph="B218-2"><span class="qr-step">05.2 · Fields and relationships</span>CDSTO byte 0 low 4 bits identifies the current operation; CDSTC byte 1 low 7 bits gives completion percentage. Ignore progress when DSTOS=0. Twenty 28-byte results begin at byte 4, newest completed or aborted operation first.</p>
<p class="qr-explanation" data-paragraph="B218-3"><span class="qr-step">05.3 · Interpretation and example</span>If byte 1 still contains 25 but DSTOS is zero, do not report a test stuck at 25%. Read the newest result for completion, command abort, reset abort or another cause.</p>
<p class="qr-tags">Search terms: LID 06h · CDSTO · CDSTC · DSTOS · RDS</p>
<div class="qr-related">Related lookups: <a href="/nvme/figure-reference/maintenance/en/#figure-b219">Base 2.4 Figure 219 · Self-test Result Data Structure</a><a href="/nvme/figure-reference/maintenance/en/#figure-b177">Base 2.4 Figure 177 · Device Self-test – Command Dword 10</a></div>
<a href="#figure-index">Back to this volume’s figure index</a></article>
<article class="qr-card" id="figure-b219" data-figure="B219">
<h2><span class="qr-number">06</span>Self-test Result Data Structure</h2>
<p class="qr-original">Base 2.4 · Figure 219 · Self-test Result Data Structure</p>
<p class="qr-location">§5.2.13.1.7 · Printed pages 231–232 · PDF 257–258</p>
<p class="qr-explanation" data-paragraph="B219-1"><span class="qr-step">06.1 · Use</span>Interpret an individual test result here, distinguishing detected failures from aborted operations. Diagnostic fields are not universally valid.</p>
<p class="qr-explanation" data-paragraph="B219-2"><span class="qr-step">06.2 · Fields and relationships</span>DSTS byte 0 high 4 bits gives test type and low 4 result; SEGN byte 1 is valid for a specific result. VDINFO byte 2 independently validates NSID, FLBA, SCT and SC. POH bytes 11:4 timestamps completion/abort in power-on hours; NSID bytes 15:12 and FLBA bytes 23:16 identify the failing target.</p>
<p class="qr-explanation" data-paragraph="B219-3"><span class="qr-step">06.3 · Interpretation and example</span>If FVLD is zero, all-zero FLBA bytes do not establish failure at LBA 0. DSTR=2 means a Controller Level Reset aborted the test, not a detected media failure.</p>
<p class="qr-tags">Search terms: DSTS · DSTR · DSTC · VDINFO · FLBA · SEGN · POH</p>
<div class="qr-related">Related lookups: <a href="/nvme/figure-reference/maintenance/en/#figure-b218">Base 2.4 Figure 218 · Device Self-test Log Page</a><a href="/nvme/figure-reference/command/en/#figure-b102">Base 2.4 Figure 102 · Status Code – Status Code Type Values</a></div>
<a href="#figure-index">Back to this volume’s figure index</a></article>
<article class="qr-card" id="figure-b443" data-figure="B443">
<h2><span class="qr-number">07</span>Namespace Attachment – Command Dword 10</h2>
<p class="qr-original">Base 2.4 · Figure 443 · Namespace Attachment – Command Dword 10</p>
<p class="qr-location">§5.2.24 · Printed pages 445 · PDF 471</p>
<p class="qr-explanation" data-paragraph="B443-1"><span class="qr-step">07.1 · Use</span>When a namespace exists but is inaccessible through one controller, inspect attachment and the controller list. Creating storage and making it accessible through a controller are different operations.</p>
<p class="qr-explanation" data-paragraph="B443-2"><span class="qr-step">07.2 · Fields and relationships</span>CDW10.SEL bits 3:0 values 0/1 mean Attach/Detach; other values are reserved. NSID chooses the namespace and a buffer lists target controllers. These SEL meanings differ from Namespace Management.</p>
<p class="qr-explanation" data-paragraph="B443-3"><span class="qr-step">07.3 · Interpretation and example</span>Detach is not Delete: it removes an association. On list-processing failure, Error Information can locate the first failed entry by byte offset; do not assume later controllers were processed.</p>
<p class="qr-tags">Search terms: Namespace Attachment · SEL · Attach · Detach · Controller List</p>
<div class="qr-related">Related lookups: <a href="/nvme/figure-reference/maintenance/en/#figure-b446">Base 2.4 Figure 446 · Namespace Management – Command Dword 10</a><a href="/nvme/figure-reference/logs/en/#figure-b212">Base 2.4 Figure 212 · Error Information Log Entry Data Structure</a></div>
<a href="#figure-index">Back to this volume’s figure index</a></article>
<article class="qr-card" id="figure-b446" data-figure="B446">
<h2><span class="qr-number">08</span>Namespace Management – Command Dword 10</h2>
<p class="qr-original">Base 2.4 · Figure 446 · Namespace Management – Command Dword 10</p>
<p class="qr-location">§5.2.25 · Printed pages 446–447 · PDF 472–473</p>
<p class="qr-explanation" data-paragraph="B446-1"><span class="qr-step">08.1 · Use</span>This selector distinguishes namespace-management actions that share one opcode. Opcode alone cannot tell Create from Delete.</p>
<p class="qr-explanation" data-paragraph="B446-2"><span class="qr-step">08.2 · Fields and relationships</span>CDW10.SEL bits 3:0 values 0/1/2 select Create, Delete or Restore Default Namespace Configuration. Other bits are reserved. Buffer and NSID interpretation depends on the action; Create also uses CSI to select its format.</p>
<p class="qr-explanation" data-paragraph="B446-3"><span class="qr-step">08.3 · Interpretation and example</span>A successfully returned new NSID establishes creation, not attachment to the desired controller. Restore means the default namespace configuration, not restoration of an arbitrary backup snapshot.</p>
<p class="qr-tags">Search terms: Namespace Management · SEL · Create · Delete · Restore</p>
<div class="qr-related">Related lookups: <a href="/nvme/figure-reference/maintenance/en/#figure-n134">NVM Command Set 1.3 Figure 134 · Namespace Management – Host Specified Fields</a><a href="/nvme/figure-reference/maintenance/en/#figure-b443">Base 2.4 Figure 443 · Namespace Attachment – Command Dword 10</a></div>
<a href="#figure-index">Back to this volume’s figure index</a></article>
<article class="qr-card" id="figure-n134" data-figure="N134">
<h2><span class="qr-number">09</span>Namespace Management – Host Specified Fields</h2>
<p class="qr-original">NVM Command Set 1.3 · Figure 134 · Namespace Management – Host Specified Fields</p>
<p class="qr-location">§4.1.6 · Printed pages 112–113 · PDF 112–113</p>
<p class="qr-explanation" data-paragraph="N134-1"><span class="qr-step">09.1 · Use</span>This table lists host-specified positions for NVM namespace creation. It reuses only part of Identify, so a complete Identify response is not an unmodified Create payload.</p>
<p class="qr-explanation" data-paragraph="N134-2"><span class="qr-step">09.2 · Fields and relationships</span>NSZE occupies bytes 7:0, NCAP bytes 15:8, FLBAS byte 26, DPS byte 29 and NMIC byte 30, followed by group identifiers. LBSTM occupies bytes 391:384. FDP uses NPHNDLS bytes 393:392 and the Placement Handle list from 512; reserved areas follow the Create definition.</p>
<p class="qr-explanation" data-paragraph="N134-3"><span class="qr-step">09.3 · Interpretation and example</span>With FDP supported and enabled, the list maps placement handles to RUHs. Otherwise those bytes cannot establish a valid mapping. NSZE/NCAP still count blocks of the chosen format, not bytes.</p>
<p class="qr-tags">Search terms: NSZE · NCAP · FLBAS · DPS · NMIC · NPHNDLS · Placement Handle</p>
<div class="qr-related">Related lookups: <a href="/nvme/figure-reference/identify/en/#figure-n123">NVM Command Set 1.3 Figure 123 · Identify – Identify Namespace Data Structure, NVM Command Set</a><a href="/nvme/figure-reference/identify/en/#figure-n125">NVM Command Set 1.3 Figure 125 · LBA Format Data Structure, NVM Command Set Specific</a><a href="/nvme/figure-reference/features/en/#figure-b294">Base 2.4 Figure 294 · FDP Configuration Descriptor</a></div>
<a href="#figure-index">Back to this volume’s figure index</a></article>
<article class="qr-card" id="figure-b195" data-figure="B195">
<h2><span class="qr-number">10</span>Format NVM – Command Dword 10</h2>
<p class="qr-original">Base 2.4 · Figure 195 · Format NVM – Command Dword 10</p>
<p class="qr-location">§5.2.11 · Printed pages 208–209 · PDF 234–235</p>
<p class="qr-explanation" data-paragraph="B195-1"><span class="qr-step">10.1 · Use</span>Decode the selected format and erase request here. Base supplies the common envelope; NVM defines PI and metadata semantics.</p>
<p class="qr-explanation" data-paragraph="B195-2"><span class="qr-step">10.2 · Fields and relationships</span>LBAFL bits 3:0 with LBAFU bits 13:12 forms the format index, with LBAFU subject to LBAFEE. SES bits 11:9 values 0/1/2 request no secure erase, User Data Erase or Cryptographic Erase. PIL bit 8, PI bits 7:5 and MSET bit 4 are command-set-specific.</p>
<p class="qr-explanation" data-paragraph="B195-3"><span class="qr-step">10.3 · Interpretation and example</span>A format index selects a list entry, not a byte size. SES=1 does not guarantee zero-filled data; a validator that accepts only zeros can reject permitted post-erase contents.</p>
<p class="qr-tags">Search terms: Format NVM · LBAFL · LBAFU · SES · LBAFEE · PI · MSET</p>
<div class="qr-related">Related lookups: <a href="/nvme/figure-reference/maintenance/en/#figure-n91">NVM Command Set 1.3 Figure 91 · Format NVM – Command Dword 10 – NVM Command Set Specific Fields</a><a href="/nvme/figure-reference/identify/en/#figure-n125">NVM Command Set 1.3 Figure 125 · LBA Format Data Structure, NVM Command Set Specific</a></div>
<a href="#figure-index">Back to this volume’s figure index</a></article>
<article class="qr-card" id="figure-n91" data-figure="N91">
<h2><span class="qr-number">11</span>Format NVM – Command Dword 10 – NVM Command Set Specific Fields</h2>
<p class="qr-original">NVM Command Set 1.3 · Figure 91 · Format NVM – Command Dword 10 – NVM Command Set Specific Fields</p>
<p class="qr-location">§4.1.1 · Printed pages 63 · PDF 63</p>
<p class="qr-explanation" data-paragraph="N91-1"><span class="qr-step">11.1 · Use</span>This table fills the three NVM-specific fields left by Base Format. PI type and Guard width are different selections; Type 3 does not mean 64-bit Guard.</p>
<p class="qr-explanation" data-paragraph="N91-2"><span class="qr-step">11.2 · Fields and relationships</span>MSET bit 4 chooses extended LBA or separate metadata. PI bits 7:5 disables protection at 0 or selects Types 1/2/3. PIL bit 8 chooses PI position; NVM Command Set 1.0 and later requires PIL=0, placing PI at the metadata tail.</p>
<p class="qr-explanation" data-paragraph="N91-3"><span class="qr-step">11.3 · Interpretation and example</span>MSET=1/PI=1 selects extended LBA with Type 1 protection. Obtain metadata size and Guard format from the selected LBAF/ELBAF instead of inferring them from these two controls.</p>
<p class="qr-tags">Search terms: Format NVM · PIL · PI · MSET · Type 1 · Type 2 · Type 3</p>
<div class="qr-related">Related lookups: <a href="/nvme/figure-reference/maintenance/en/#figure-b195">Base 2.4 Figure 195 · Format NVM – Command Dword 10</a><a href="/nvme/figure-reference/identify/en/#figure-n125">NVM Command Set 1.3 Figure 125 · LBA Format Data Structure, NVM Command Set Specific</a><a href="/nvme/figure-reference/identify/en/#figure-n128">NVM Command Set 1.3 Figure 128 · Extended LBA Format Data Structure, NVM Command Set Specific</a></div>
<a href="#figure-index">Back to this volume’s figure index</a></article>
<article class="qr-card" id="figure-b451" data-figure="B451">
<h2><span class="qr-number">12</span>Sanitize – Command Dword 10</h2>
<p class="qr-original">Base 2.4 · Figure 451 · Sanitize – Command Dword 10</p>
<p class="qr-location">§5.2.26 · Printed pages 450–451 · PDF 476–477</p>
<p class="qr-explanation" data-paragraph="B451-1"><span class="qr-step">12.1 · Use</span>Decode subsystem-wide sanitize action, overwrite passes and subsequent-state options here. Acceptance of the command and completion of sanitization require separate observations.</p>
<p class="qr-explanation" data-paragraph="B451-2"><span class="qr-step">12.2 · Fields and relationships</span>SANACT bits 2:0 selects 1 exit failure, 2 Block Erase, 3 Overwrite, 4 Crypto Erase or 5 exit Media Verification. AUSE bit 3 selects completion mode. OWPASS bits 7:4/OIPBP bit 8 apply to overwrite; NDAS bit 9, EMVS bit 10 and PREQ bit 11 control deallocation, verification and purge requests.</p>
<p class="qr-explanation" data-paragraph="B451-3"><span class="qr-step">12.3 · Interpretation and example</span>For overwrite, OWPASS=0 means 16 passes, not none. After acceptance, inspect LID=81h and SOS; Admin CQE success or a single SPROG value does not prove successful sanitization.</p>
<p class="qr-tags">Search terms: Sanitize · SANACT · AUSE · OWPASS · NDAS · EMVS · PREQ</p>
<div class="qr-related">Related lookups: <a href="/nvme/figure-reference/maintenance/en/#figure-b312">Base 2.4 Figure 312 · Sanitize Status Log Page</a><a href="/nvme/figure-reference/maintenance/en/#figure-b454">Base 2.4 Figure 454 · Sanitize Namespace – Command Dword 10</a></div>
<a href="#figure-index">Back to this volume’s figure index</a></article>
<article class="qr-card" id="figure-b454" data-figure="B454">
<h2><span class="qr-number">13</span>Sanitize Namespace – Command Dword 10</h2>
<p class="qr-original">Base 2.4 · Figure 454 · Sanitize Namespace – Command Dword 10</p>
<p class="qr-location">§5.2.27 · Printed pages 453 · PDF 479</p>
<p class="qr-explanation" data-paragraph="B454-1"><span class="qr-step">13.1 · Use</span>Namespace Sanitize has its own CDW10 layout. Do not copy every control bit from subsystem Sanitize.</p>
<p class="qr-explanation" data-paragraph="B454-2"><span class="qr-step">13.2 · Fields and relationships</span>Valid controls include SANACT bits 2:0, AUSE bit 3, PREQ bit 4 and EMVS bit 10. Crypto Erase 4 starts an operation; Block Erase and Overwrite encodings are reserved here. Bits 9:5 and 31:11 are reserved.</p>
<p class="qr-explanation" data-paragraph="B454-3"><span class="qr-step">13.3 · Interpretation and example</span>CDW10=0000041Ch contains SANACT=4, AUSE=1, PREQ=1 and EMVS=1. Placing PREQ at the subsystem command’s bit 11 instead writes a reserved bit, not a purge request.</p>
<p class="qr-tags">Search terms: Sanitize Namespace · SANACT · PREQ bit4 · EMVS · NSID</p>
<div class="qr-related">Related lookups: <a href="/nvme/figure-reference/maintenance/en/#figure-b451">Base 2.4 Figure 451 · Sanitize – Command Dword 10</a><a href="/nvme/figure-reference/maintenance/en/#figure-b312">Base 2.4 Figure 312 · Sanitize Status Log Page</a></div>
<a href="#figure-index">Back to this volume’s figure index</a></article>
<article class="qr-card" id="figure-b312" data-figure="B312">
<h2><span class="qr-number">14</span>Sanitize Status Log Page</h2>
<p class="qr-original">Base 2.4 · Figure 312 · Sanitize Status Log Page</p>
<p class="qr-location">§5.2.13.1.38 · Printed pages 314–319 · PDF 340–345</p>
<p class="qr-explanation" data-paragraph="B312-1"><span class="qr-step">14.1 · Use</span>This log reports progress, the latest outcome and current sanitize state. Determine whether the queried target is a subsystem or namespace before decoding scope-dependent fields.</p>
<p class="qr-explanation" data-paragraph="B312-2"><span class="qr-step">14.2 · Fields and relationships</span>SPROG bytes 1:0 is a progress fraction; SOS distinguishes never run, success, processing and failure. SCDW10 records starting parameters. Estimated-time fields have individual zero/FFFFFFFFh meanings. SSI supplements state/failure details alongside erased-state and STNSID information.</p>
<p class="qr-explanation" data-paragraph="B312-3"><span class="qr-step">14.3 · Interpretation and example</span>SPROGFFFFh alone is not success: SOS=3 still means failure. Decode SCDW10 using Figure 451 or 454 according to target, especially the different PREQ position.</p>
<p class="qr-tags">Search terms: LID 81h · SPROG · SOS · SCDW10 · SSI · GDE · NDE · STNSID</p>
<div class="qr-related">Related lookups: <a href="/nvme/figure-reference/maintenance/en/#figure-b451">Base 2.4 Figure 451 · Sanitize – Command Dword 10</a><a href="/nvme/figure-reference/maintenance/en/#figure-b454">Base 2.4 Figure 454 · Sanitize Namespace – Command Dword 10</a><a href="/nvme/figure-reference/logs/en/#figure-b234">Base 2.4 Figure 234 · Persistent Event Format</a></div>
<a href="#figure-index">Back to this volume’s figure index</a></article>
<article class="qr-card" id="figure-b541" data-figure="B541">
<h2><span class="qr-number">15</span>Write Protection – Command Dword 11</h2>
<p class="qr-original">Base 2.4 · Figure 541 · Write Protection – Command Dword 11</p>
<p class="qr-location">§5.2.30.1.38 · Printed pages 512 · PDF 538</p>
<p class="qr-explanation" data-paragraph="B541-1"><span class="qr-step">15.1 · Use</span>When writes are rejected, inspect namespace WPS to distinguish reversible, power-cycle-bound and permanent protection. Boot Partition protection uses different encodings.</p>
<p class="qr-explanation" data-paragraph="B541-2"><span class="qr-step">15.2 · Fields and relationships</span>CDW11.WPS bits 2:0 values 0/1/2/3 mean unprotected, protected, until-power-cycle and permanent. NWPC and Write Protection Control separately govern capability and entry permission; WPS describes requested/reported state.</p>
<p class="qr-explanation" data-paragraph="B541-3"><span class="qr-step">15.3 · Interpretation and example</span>Once WPS=2 or 3 is entered, requesting 0 through Set Features returns Feature Not Changeable. SEL=3.CHANG=1 does not make a permanent current state reversible.</p>
<p class="qr-tags">Search terms: FID 84h · WPS · Write Protect · Permanent Write Protect</p>
<div class="qr-related">Related lookups: <a href="/nvme/figure-reference/features/en/#figure-b201">Base 2.4 Figure 201 · Completion Queue Entry Dword 0 when Select is set to 11b</a><a href="/nvme/figure-reference/identify/en/#figure-b346">Base 2.4 Figure 346 · Identify – I/O Command Set Independent Identify Namespace Data Structure</a><a href="/nvme/figure-reference/maintenance/en/#figure-b542">Base 2.4 Figure 542 · Boot Partition Write Protection Config - Command Dword 11</a></div>
<a href="#figure-index">Back to this volume’s figure index</a></article>
<article class="qr-card" id="figure-b542" data-figure="B542">
<h2><span class="qr-number">16</span>Boot Partition Write Protection Config - Command Dword 11</h2>
<p class="qr-original">Base 2.4 · Figure 542 · Boot Partition Write Protection Config - Command Dword 11</p>
<p class="qr-location">§5.2.30.1.39 · Printed pages 513–514 · PDF 539–540</p>
<p class="qr-explanation" data-paragraph="B542-1"><span class="qr-step">16.1 · Use</span>Check each Boot Partition’s protection when updates are blocked. Zero does not mean unprotected as it does for namespace WPS.</p>
<p class="qr-explanation" data-paragraph="B542-2"><span class="qr-step">16.2 · Fields and relationships</span>BP0WPS bits 2:0 and BP1WPS bits 5:3 encode 0 no requested change (Set only), 1 unlocked, 2 locked and 3 locked until power cycle. Value 4 reports RPMB-controlled protection and is reserved for Set. Both default to locked.</p>
<p class="qr-explanation" data-paragraph="B542-3"><span class="qr-step">16.3 · Interpretation and example</span>To unlock partition 0 while leaving partition 1 unchanged, use 1 and 0, producing CDW11=1. Clearing both fields does not unlock both partitions. If CTRATT.MDS=1 and multiple controllers share the Boot Partition, requesting state 3 (locked until power cycle) fails with Feature Not Changeable.</p>
<p class="qr-tags">Search terms: FID 85h · BP0WPS · BP1WPS · RPMB · Boot Partition</p>
<div class="qr-related">Related lookups: <a href="/nvme/figure-reference/maintenance/en/#figure-b541">Base 2.4 Figure 541 · Write Protection – Command Dword 11</a><a href="/nvme/figure-reference/maintenance/en/#figure-b187">Base 2.4 Figure 187 · Firmware Commit – Command Dword 10</a></div>
<a href="#figure-index">Back to this volume’s figure index</a></article>
<footer id="source-files"><h2>Source documents</h2><p>Locations refer to the supplied ratified PDFs. For Base, PDF page = printed page +26; the other two use identical page numbers. Original figure numbers and English titles are retained for PDF search. Source PDFs are not redistributed.</p><ul class="qr-sources"><li>NVM Express Base Specification · Revision 2.4 · 2026-07-31<br><code>NVM-Express-Base-Specification-Revision-2.4-Ratified-2026.07.31.pdf</code></li><li>NVM Express NVM Command Set Specification · Revision 1.3 · 2026-07-31<br><code>NVM-Express-NVM-Command-Set-Specification-Revision-1.3-Ratified-2026.07.31.pdf</code></li><li>NVM Express NVMe over PCIe Transport Specification · Revision 1.4 · 2026-07-31<br><code>NVM-Express-NVMe-over-PCIe-Transport-Specification-Revision-1.4-Ratified-2026.07.31.pdf</code></li></ul></footer>
</main></div>
