---
layout: post
read_time: true
show_date: true
title: "NVMe Base 2.4: Firmware Update and LID 03h Verification"
date: 2026-09-01
description: "An NVMe technical report covering the main ideas, mechanisms, conditions, and examples."
lang: en
img: posts/2026/cat_title.jpg
tags: [NVMe, PCIe, Specification]
category: NVMe
author: Jia-Chang
github: JiaChangGit/JiaChangGit.github.io/tree/main/DOCS/nvme-spec-report
toc: yes
nvme_notes: true
---
[繁體中文]({% post_url 2026-08-31-nvme-base-firmware-log-admin-zh-tw %})


<div class="nvme-note">
<section id="topic-overview" class="topic-overview">
<p class="opening">Firmware updates involve transferring an image, storing it in a slot, and changing the running version. This note explains how Firmware Image Download, Firmware Commit, and Firmware Slot Information cooperate, distinguishing the state changed by each step.</p>
<h2 id="main-ideas">The main ideas</h2>
<div class="topic-map">
<article><span class="axis-number">01</span><h3>Capabilities and update units</h3><p>Establish available slots, write restrictions, and download granularity.</p></article>
<article><span class="axis-number">02</span><h3>Download and activation</h3><p>Understand image ranges, Commit Action, and reset requirements.</p></article>
<article><span class="axis-number">03</span><h3>Running version</h3><p>Use current and next active slots to distinguish stored and running images.</p></article>
</div>

<p>A firmware slot stores an image; a revision string alone does not establish that the image is running. Controller capabilities, command completion, and slot information provide distinct information.</p>
</section>
<section class="lesson" id="module-fw-capability-plan"><h2 id="heading-fw-capability-plan"><span class="section-number">01</span> Capabilities and limits before an update</h2>
<p>Firmware update is not a fixed command recipe. FRMW controls slots and activation capability, FWUG controls download granularity and alignment, MTFA and MPTFAWR bound waiting time, and MDS/DID define which controllers share the result.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>MPTFAWR</dt><dd>Maximum Processing Time for Firmware Activation Without Reset, the maximum processing time for immediate activation without a reset.</dd></div><div><dt>FRMW</dt><dd>Firmware Updates, the Identify Controller field reporting slot count, slot-1 read-only state, and activation capabilities.</dd></div><div><dt>FWUG</dt><dd>Firmware Update Granularity, the capability field governing download-portion granularity and alignment.</dd></div><div><dt>MTFA</dt><dd>Maximum Time for Firmware Activation, the maximum time activation may pause command processing.</dd></div><div><dt>DID</dt><dd>Domain Identifier, the identifier of a domain within an NVM subsystem.</dd></div><div><dt>MDS</dt><dd>Multiple Domain Subsystem, the capability bit indicating whether an NVM subsystem contains multiple domains.</dd></div></dl>
<details class="technical-note"><summary>Mechanism and applicable conditions</summary>
<!-- claim:BASEFWLOG-CAP-FRMW -->
<p>FRMW.SMUD, FAWR, NOFS, and FFSRO describe overlapping-update detection, activation without reset, the domain's supported slot count (1 through 7), and whether slot 1 is read-only.</p><details class="source-note"><summary>Sources: Base 2.4 §5.2.14.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.14.1, printed pages 354, PDF pages 380</p></details>
<!-- claim:BASEFWLOG-CAP-FWUG -->
<p>FWUG constrains NUMD and OFST granularity/alignment in 4 KiB units: 1h is 4 KiB, 2h is 8 KiB, 0h reports no information, and FFh permits any dword granularity and alignment. A controller may return Invalid Field in Command for a violation.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>controller</dt><dd>Controller, the entity that implements the NVMe interface, fetches commands, and reports completions.</dd></div><div><dt>NUMD</dt><dd>Number of Dwords, a zero-based transfer-dword count; actual bytes = (NUMD + 1) × 4.</dd></div><div><dt>OFST</dt><dd>Offset, the dword-based image-relative offset in Firmware Image Download.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §5.2.14.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.14.1, printed pages 359, PDF pages 385</p></details>
<!-- claim:BASEFWLOG-CAP-MTFA -->
<p>MTFA is in 100 ms units and reports the maximum time command processing is temporarily stopped during activation. It shall be valid when activation without reset is supported; 0h means the maximum is undefined.</p><details class="source-note"><summary>Sources: Base 2.4 §5.2.14.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.14.1, printed pages 357, PDF pages 383</p></details>
<!-- claim:BASEFWLOG-CAP-MPTFAWR -->
<p>MPTFAWR is a 100 ms-unit estimate of the maximum processing time to complete Firmware Commit with CA=011b, including time to commit the image to a slot. It shall be 0h when activation without reset is unsupported.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>CA</dt><dd>Commit Action, the Firmware Commit field selecting replacement, activation, and reset policy.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §5.2.14.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.14.1, printed pages 364, PDF pages 390</p></details>
<!-- claim:BASEFWLOG-CAP-MDS-ULIST -->
<p>CTRATT.MDS determines whether LID 03h returns domain-scoped or NVM-subsystem-scoped information, while CTRATT.ULIST indicates UUID List reporting support. With MDS=1, DID shall be nonzero; in a single-domain subsystem, DID shall be 0h.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>LID 03h</dt><dd>Identifier 03h for the Firmware Slot Information log page.</dd></div><div><dt>ULIST</dt><dd>UUID List, the capability bit indicating support for the UUID List data structure.</dd></div><div><dt>UUID</dt><dd>Universally Unique Identifier, a 128-bit identifier whose association scope is defined by the containing structure.</dd></div><div><dt>LID</dt><dd>Log Page Identifier, the Get Log Page field selecting a log page.</dd></div><div><dt>NVM</dt><dd>Non-Volatile Memory, memory that retains data without power.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §5.2.14.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.14.1, printed pages 346, 364, PDF pages 372, 390</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">Item</th><th scope="col">Role or distinction</th><th scope="col">Conditions</th></tr></thead><tbody><tr><td>FRMW</td><td>Available slots, slot-1 read-only state, activation capability</td><td>Read before selecting FS and CA</td></tr><tr><td>FWUG</td><td>Download-portion granularity and alignment</td><td>Convert to bytes before splitting the image</td></tr><tr><td>MTFA / MPTFAWR</td><td>Timing bounds for activation interruption</td><td>Do not hard-code timeout</td></tr><tr><td>MDS / DID</td><td>Domain that shares firmware slots</td><td>A PCI Function is not the complete scope</td></tr></tbody></table></div><dl class="term-note" aria-label="Terms in this passage"><div><dt>CA</dt><dd>Commit Action, the Firmware Commit field selecting replacement, activation, and reset policy.</dd></div><div><dt>FS</dt><dd>Firmware Slot, the Firmware Commit field selecting the target slot.</dd></div></dl>
<aside class="worked-example"><h3>Example</h3><p>If FWUG decodes to 4 KiB, a 12 KiB image can be split into three 4 KiB portions; the final transfer is not an arbitrary short tail. The plan must also establish that slot 2 is legal and writable and select a timeout for the activation path.</p></aside>
<details class="technical-note"><summary>Fields and data structures in more depth</summary>
<!-- figure-table:BASEFWLOG-FIG-337 -->
<details class="field-note" id="figure-BASEFWLOG-FIG-337"><summary>Base Figure 337 · Command Set Identifiers</summary>
<!-- claim:BASEFWLOG-FIG-337-CLAIM -->
<p>Figure 337, "Command Set Identifiers": Defines the identifier composition or namespace of values shown by Command Set Identifiers.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>namespace</dt><dd>Namespace, a formatted quantity of non-volatile memory accessed by a host through a controller.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §5.2.14.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.14.1, Figure 337, printed pages 340, PDF pages 366</p></details>

</details>
<!-- figure-table:BASEFWLOG-FIG-338 -->
<details class="field-note" id="figure-BASEFWLOG-FIG-338"><summary>Base Figure 338 · Identify – Identify Controller Data Structure, I/O Command Set Independent</summary>
<!-- claim:BASEFWLOG-FIG-338-CLAIM -->
<p>Figure 338, "Identify – Identify Controller Data Structure, I/O Command Set Independent": Defines the concrete layout or value relationships for Identify – Identify Controller Data Structure, I/O Command Set Independent.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>I/O</dt><dd>Input/Output, the class of data operations performed on a namespace.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §5.2.14.2.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.14.2.1, Figure 338, printed pages 340-364, PDF pages 366-390</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>ULIST</dt><dd>UUID List, the capability bit indicating support for the UUID List data structure.</dd></div><div><dt>FR</dt><dd>Firmware Revision, the eight-byte ASCII Identify Controller field reporting the active firmware revision.</dd></div></dl>
</details>
</details>
</section>
<section class="lesson" id="module-fw-download-geometry"><h2 id="heading-fw-download-geometry"><span class="section-number">02</span> Download lengths, offsets, and portions</h2>
<p>Each Firmware Image Download uses DPTR for the host buffer, zero-based NUMD for transfer dwords, and OFST for the image-relative dword offset. The host must prove buffer validity, length, offset, FWUG compliance, and absence of gaps or overlaps.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>DPTR</dt><dd>Data Pointer, the SQE field identifying a command data buffer.</dd></div><div><dt>NUMD</dt><dd>Number of Dwords, a zero-based transfer-dword count; actual bytes = (NUMD + 1) × 4.</dd></div><div><dt>OFST</dt><dd>Offset, the dword-based image-relative offset in Firmware Image Download.</dd></div></dl>
<details class="technical-note"><summary>Mechanism and applicable conditions</summary>
<!-- claim:BASEFWLOG-DOWNLOAD-RANGE -->
<p>Firmware Image Download may split an image into portions, and firmware-image portions may arrive out of order. The host should avoid overlapping ranges and comply with FWUG. Boot Partition portions shall be submitted in order.</p><details class="source-note"><summary>Sources: Base 2.4 §5.2.10</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.10, printed pages 205-206, PDF pages 231-232</p></details>
<!-- claim:BASEFWLOG-DOWNLOAD-FIELDS -->
<p>An Admin command over NVMe over PCIe shall not use SGL, so DPTR uses PRPs to identify the source buffer. NUMD is a zero-based dword count, so bytes=(NUMD+1)×4; OFST is a dword offset from the image start, so byte offset=OFST×4. The portion containing the image start shall use OFST=0h.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>Admin</dt><dd>Administrative, the control path used to create, configure, query, or manage controllers and queues.</dd></div><div><dt>NVMe</dt><dd>Non-Volatile Memory Express, the specification family for a host interface to a non-volatile-memory subsystem.</dd></div><div><dt>PCIe</dt><dd>PCI Express, the transport and device interconnect used by an NVMe memory-based controller.</dd></div><div><dt>SGL</dt><dd>Scatter Gather List, a descriptor-and-segment format for one or more data-buffer regions.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §4.1.1, 5.2.10</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.1.1, 5.2.10, printed pages 140-142, 205-206, PDF pages 166-168, 231-232</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">Item</th><th scope="col">Role or distinction</th><th scope="col">Conditions</th></tr></thead><tbody><tr><td>DPTR</td><td>Host buffer for this transfer</td><td>A valid address does not prove a valid length</td></tr><tr><td>NUMD</td><td>Zero-based dword count for this transfer</td><td>4096 bytes → 1024 dwords → 03FFh</td></tr><tr><td>OFST</td><td>Dword offset from the image start</td><td>The second 4 KiB portion starts at 1024 dwords</td></tr><tr><td>FWUG</td><td>Portion alignment and granularity gate</td><td>Validate the image and each portion separately</td></tr></tbody></table></div><dl class="term-note" aria-label="Terms in this passage"><div><dt>Dword</dt><dd>Double word, four bytes or 32 bits; NVMe command fields are commonly identified by CDW number.</dd></div></dl>
<aside class="worked-example"><h3>Example</h3><p>For a 12 KiB image in 4 KiB chunks: portion 0 uses NUMD=03FFh and OFST=00000000h; portion 1 uses NUMD=03FFh and OFST=00000400h; portion 2 uses NUMD=03FFh and OFST=00000800h. Commit follows only after all three completions succeed.</p></aside>
<details class="technical-note"><summary>Fields and data structures in more depth</summary>
<!-- figure-table:BASEFWLOG-FIG-190 -->
<details class="field-note" id="figure-BASEFWLOG-FIG-190"><summary>Base Figure 190 · Firmware Image Download – Data Pointer</summary>
<!-- claim:BASEFWLOG-FIG-190-CLAIM -->
<p>Figure 190, "Firmware Image Download – Data Pointer": Defines how Firmware Image Download – Data Pointer identifies the destination or source buffer for this command.</p><details class="source-note"><summary>Sources: Base 2.4 §5.2.10</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.10, Figure 190, printed pages 205, PDF pages 231</p></details>

</details>
<!-- figure-table:BASEFWLOG-FIG-191 -->
<details class="field-note" id="figure-BASEFWLOG-FIG-191"><summary>Base Figure 191 · Firmware Image Download – Command Dword 10</summary>
<!-- claim:BASEFWLOG-FIG-191-CLAIM -->
<p>Figure 191, "Firmware Image Download – Command Dword 10": Defines the concrete layout or value relationships for Firmware Image Download – Command Dword 10.</p><details class="source-note"><summary>Sources: Base 2.4 §5.2.10</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.10, Figure 191, printed pages 205, PDF pages 231</p></details>

</details>
<!-- figure-table:BASEFWLOG-FIG-192 -->
<details class="field-note" id="figure-BASEFWLOG-FIG-192"><summary>Base Figure 192 · Firmware Image Download – Command Dword 11</summary>
<!-- claim:BASEFWLOG-FIG-192-CLAIM -->
<p>Figure 192, "Firmware Image Download – Command Dword 11": Defines the concrete layout or value relationships for Firmware Image Download – Command Dword 11.</p><details class="source-note"><summary>Sources: Base 2.4 §5.2.10</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.10, Figure 192, printed pages 206, PDF pages 232</p></details>

</details>
<!-- figure-table:BASEFWLOG-FIG-193 -->
<details class="field-note" id="figure-BASEFWLOG-FIG-193"><summary>Base Figure 193 · Firmware Image Download – Command Specific Status Values</summary>
<!-- claim:BASEFWLOG-FIG-193-CLAIM -->
<p>Figure 193, "Firmware Image Download – Command Specific Status Values": Defines the concrete layout or value relationships for Firmware Image Download – Command Specific Status Values.</p><details class="source-note"><summary>Sources: Base 2.4 §5.2.10</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.10, Figure 193, printed pages 206, PDF pages 232</p></details>

</details>
<!-- figure-table:BASEFWLOG-FIG-093 -->
<details class="field-note" id="figure-BASEFWLOG-FIG-093"><summary>Base Figure 93 · Common Command Format</summary>
<!-- claim:BASEFWLOG-FIG-093-CLAIM -->
<p>Figure 93, "Common Command Format": Defines the concrete layout or value relationships for Common Command Format.</p><details class="source-note"><summary>Sources: Base 2.4 §4.1.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.1.1, Figure 93, printed pages 140-142, PDF pages 166-168</p></details>

</details>
</details>
</section>
<section class="lesson" id="module-fw-commit-state"><h2 id="heading-fw-commit-state"><span class="section-number">03</span> Commit storage and activation choices</h2>
<p>Commit Action (CA) is not a success flag; it selects replacement, activation, and reset boundary. Firmware Slot (FS) selects the target slot, while CQE status determines whether software verifies, performs a specific reset, waits, or stops.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>CQE</dt><dd>Completion Queue Entry, one completion-result structure in a CQ.</dd></div></dl>
<figure><figcaption><strong>Downloading, storing, and activating have different effects</strong></figcaption><ol class="flow-steps"><li>Firmware Image Download transfers portions of the image.</li><li>Firmware Commit uses CA to choose slot replacement and activation behavior.</li><li>Activation requiring reset changes the running image after the specified reset.</li><li>Firmware Slot Information distinguishes the current active slot from the next active slot.</li></ol><figcaption>Transfer complete, image stored, and image running are different states.</figcaption></figure>

<details class="technical-note"><summary>Mechanism and applicable conditions</summary>
<!-- claim:BASEFWLOG-COMMIT-PURPOSE -->
<p>Firmware Commit validates the last downloaded image, places it in a firmware slot, and uses Commit Action to choose placement only, activation at a later Controller Level Reset, or immediate activation. Successful commit does not by itself mean the image is currently active.</p><details class="source-note"><summary>Sources: Base 2.4 §5.2.9</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.9, printed pages 202-203, PDF pages 228-229</p></details>
<!-- claim:BASEFWLOG-COMMIT-CDW10 -->
<p>CDW10[5:3] is CA and CDW10[2:0] is FS. CA 000b places only, 001b places and schedules activation at the next CLR, 010b schedules an existing slot, and 011b activates immediately. With FS=0h, the controller shall choose a slot from 1 through 7.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>controller</dt><dd>Controller, the entity that implements the NVMe interface, fetches commands, and reports completions.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §5.2.9</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.9, printed pages 203, PDF pages 229</p></details>
<!-- claim:BASEFWLOG-COMMIT-MUD -->
<p>Firmware Commit CQE.DW0[1:0] MUD reports overlap detected through a Management Endpoint and an Admin Submission Queue. If FRMW.SMUD is 0, MUD shall be 00b; MUD is valid whether the command succeeds or is aborted.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>Admin</dt><dd>Administrative, the control path used to create, configure, query, or manage controllers and queues.</dd></div><div><dt>MUD</dt><dd>Multiple Update Detected, the completion bit indicating detection of overlapping firmware-update sequences.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §5.2.9</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.9, printed pages 204, PDF pages 230</p></details>
<!-- claim:BASEFWLOG-COMMIT-STATUS -->
<p>Firmware Commit command-specific status distinguishes invalid slot/image, required Conventional/NVM Subsystem/Controller Level Reset, MTFA violation, activation prohibited, overlapping range, Boot Partition write prohibition, and personality incompatibility.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>NVM</dt><dd>Non-Volatile Memory, memory that retains data without power.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §5.2.9</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.9, printed pages 204-205, PDF pages 230-231</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">Item</th><th scope="col">Role or distinction</th><th scope="col">Conditions</th></tr></thead><tbody><tr><td>CA</td><td>Replacement and activation behavior</td><td>Do not log only a decimal value</td></tr><tr><td>FS</td><td>Target firmware slot</td><td>Zero may let the controller choose; follow the definition</td></tr><tr><td>SCT / SC</td><td>Success, reset scope, or failure cause</td><td>0Bh, 10h, and 11h imply different reset scopes</td></tr><tr><td>MUD</td><td>Evidence of overlapping update sequences</td><td>It may be meaningful even when the command aborts</td></tr></tbody></table></div><dl class="term-note" aria-label="Terms in this passage"><div><dt>controller</dt><dd>Controller, the entity that implements the NVMe interface, fetches commands, and reports completions.</dd></div><div><dt>MUD</dt><dd>Multiple Update Detected, the completion bit indicating detection of overlapping firmware-update sequences.</dd></div><div><dt>SCT</dt><dd>Status Code Type, the category selected before interpreting SC.</dd></div><div><dt>SC</dt><dd>Status Code, the specific completion result interpreted in the context of SCT.</dd></div></dl>
<aside class="worked-example"><h3>Example</h3><p>If completion reports Firmware Activation Requires Controller Level Reset, Commit may have succeeded while the image is not yet current. Software records the status, performs the specified reset, and then verifies Identify.FR and LID 03h.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>LID 03h</dt><dd>Identifier 03h for the Firmware Slot Information log page.</dd></div><div><dt>LID</dt><dd>Log Page Identifier, the Get Log Page field selecting a log page.</dd></div><div><dt>FR</dt><dd>Firmware Revision, the eight-byte ASCII Identify Controller field reporting the active firmware revision.</dd></div></dl></aside>
<details class="technical-note"><summary>Fields and data structures in more depth</summary>
<!-- figure-table:BASEFWLOG-FIG-187 -->
<details class="field-note" id="figure-BASEFWLOG-FIG-187"><summary>Base Figure 187 · Firmware Commit – Command Dword 10</summary>
<!-- claim:BASEFWLOG-FIG-187-CLAIM -->
<p>Figure 187, "Firmware Commit – Command Dword 10": Defines the concrete layout or value relationships for Firmware Commit – Command Dword 10.</p><details class="source-note"><summary>Sources: Base 2.4 §5.2.9</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.9, Figure 187, printed pages 203, PDF pages 229</p></details>

</details>
<!-- figure-table:BASEFWLOG-FIG-188 -->
<details class="field-note" id="figure-BASEFWLOG-FIG-188"><summary>Base Figure 188 · Firmware Commit – Completion Queue Entry Dword 0</summary>
<!-- claim:BASEFWLOG-FIG-188-CLAIM -->
<p>Figure 188, "Firmware Commit – Completion Queue Entry Dword 0": Shows the queue or command relationship expressed by Firmware Commit – Completion Queue Entry Dword 0.</p><details class="source-note"><summary>Sources: Base 2.4 §5.2.9.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.9.1, Figure 188, printed pages 204, PDF pages 230</p></details>

</details>
<!-- figure-table:BASEFWLOG-FIG-189 -->
<details class="field-note" id="figure-BASEFWLOG-FIG-189"><summary>Base Figure 189 · Firmware Commit – Command Specific Status Values</summary>
<!-- claim:BASEFWLOG-FIG-189-CLAIM -->
<p>Figure 189, "Firmware Commit – Command Specific Status Values": Defines the concrete layout or value relationships for Firmware Commit – Command Specific Status Values.</p><details class="source-note"><summary>Sources: Base 2.4 §5.2.9.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.9.1, Figure 189, printed pages 204-205, PDF pages 230-231</p></details>

</details>
</details>
</section>
<section class="lesson" id="module-fw-lid03-proof"><h2 id="heading-fw-lid03-proof"><span class="section-number">04</span> Current and pending versions in LID 03h</h2>
<p>Get Log Page first builds a 512-byte transfer from common command fields and selects Firmware Slot Information with LID=03h. AFI separates CAFS from NAFS, FRS1-FRS7 report slot revisions, and Identify.FR plus domain scope provide the final cross-check.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>CAFS</dt><dd>Current Active Firmware Slot, the low three AFI bits identifying the currently executing firmware slot.</dd></div><div><dt>NAFS</dt><dd>Next Active Firmware Slot, AFI bits 6:4 identifying the slot scheduled for the next reset; zero means none is scheduled.</dd></div><div><dt>AFI</dt><dd>Active Firmware Info, the LID 03h byte containing the current active slot and the slot scheduled for the next reset.</dd></div></dl>
<details class="technical-note"><summary>Mechanism and applicable conditions</summary>
<!-- claim:BASEFWLOG-LOG-COMMAND -->
<p>When reading LID 03h, no namespace is used, so NSID shall be 0h, and DPTR uses PRPs to identify the 512-byte destination buffer. The required CDW10-CDW14 slice is LID=03h, LSP=0, RAE=0, NUMDL/NUMDU for 512 bytes, LSI=0, LPOL/LPOU=0, OT=0, and UIDX=0. LID 03h does not use CSI, which the controller ignores under Figure 208's rule.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>namespace</dt><dd>Namespace, a formatted quantity of non-volatile memory accessed by a host through a controller.</dd></div><div><dt>NUMDL</dt><dd>Number of Dwords Lower, the low 16 bits of Get Log Page NUMD.</dd></div><div><dt>NUMDU</dt><dd>Number of Dwords Upper, the high 16 bits of Get Log Page NUMD.</dd></div><div><dt>LPOL</dt><dd>Log Page Offset Lower, the low 32 bits of the Get Log Page byte offset.</dd></div><div><dt>LPOU</dt><dd>Log Page Offset Upper, the high 32 bits of the Get Log Page byte offset.</dd></div><div><dt>NSID</dt><dd>Namespace Identifier, a controller-visible numeric handle for a namespace; the identifier is not the namespace object itself.</dd></div><div><dt>UIDX</dt><dd>UUID Index, an index into the UUID List; zero indicates that no UUID is specified.</dd></div><div><dt>CSI</dt><dd>Command Set Identifier, selecting the I/O Command Set context for a command or log page.</dd></div><div><dt>LSI</dt><dd>Log Specific Identifier, an identifier whose meaning is defined by the selected log page.</dd></div><div><dt>LSP</dt><dd>Log Specific Field, a command selector whose meaning is defined by the selected log page.</dd></div><div><dt>RAE</dt><dd>Retain Asynchronous Event, the Get Log Page selector controlling retention of a related asynchronous event.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §4.1.1, 5.2.13</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.1.1, 5.2.13, printed pages 140-142, 212-215, PDF pages 166-168, 238-241</p></details>
<!-- claim:BASEFWLOG-LOG-LENGTH -->
<p>NUMDL and NUMDU form a zero-based dword count. LID 03h is 512 bytes, or 128 dwords, so NUMD=127=0000007Fh, NUMDL=007Fh, and NUMDU=0000h. With LSP=0 and RAE=0, CDW10=007F0003h.</p><details class="source-note"><summary>Sources: Base 2.4 §5.2.13</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13, printed pages 213-215, PDF pages 239-241</p></details>
<!-- claim:BASEFWLOG-LOG-SCOPE -->
<p>The LID 03h row in Figure 209 specifies CSI=N, scope=Domain/NVM subsystem, and reference §5.2.13.1.4. With MDS=1, the data is for the domain containing the controller that processed the command; otherwise it is for the NVM subsystem.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>NVM subsystem</dt><dd>NVM subsystem, the NVMe system boundary containing controllers, ports, namespaces, and non-volatile storage resources.</dd></div><div><dt>NVM</dt><dd>Non-Volatile Memory, memory that retains data without power.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §5.2.13</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13, printed pages 215-216, PDF pages 241-242</p></details>
<!-- claim:BASEFWLOG-LID03-AFI -->
<p>In AFI byte 0, NAFS is bits 6:4 and CAFS is bits 2:0; bits 7 and 3 are reserved. Nonzero NAFS identifies the slot to activate at the next CLR capable of causing activation; NAFS=0 means no next slot is indicated. CAFS identifies the source slot of the running image.</p><details class="source-note"><summary>Sources: Base 2.4 §5.2.13.1.4</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.4, printed pages 226, PDF pages 252</p></details>
<!-- claim:BASEFWLOG-LID03-FRS -->
<p>FRS1 through FRS7 occupy bytes 8-63, eight bytes per slot. If a slot has no valid revision or is unsupported, its FRS shall be cleared to 0h. Bytes 1-7 and 64-511 are reserved.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>FRS</dt><dd>Firmware Revision for Slot, the eight-byte revision-string field for each slot in LID 03h.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §5.2.13.1.4</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.4, printed pages 226, PDF pages 252</p></details>
<!-- claim:BASEFWLOG-CAP-FR -->
<p>Identify Controller FR is the eight-byte ASCII string for the currently active firmware revision in the controller's domain. It is the same revision information available from LID 03h.</p><details class="source-note"><summary>Sources: Base 2.4 §5.2.14.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.14.1, printed pages 340, PDF pages 366</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">Item</th><th scope="col">Role or distinction</th><th scope="col">Conditions</th></tr></thead><tbody><tr><td>CAFS</td><td>Currently executing slot</td><td>It is not next-reset intent</td></tr><tr><td>NAFS</td><td>Slot scheduled after the next reset</td><td>Zero means none scheduled</td></tr><tr><td>FRSx</td><td>Eight-byte revision for slot x</td><td>All-zero bytes are not an ASCII string</td></tr><tr><td>Identify.FR</td><td>Independent observation of current revision</td><td>Cross-check against the FRSx selected by CAFS</td></tr></tbody></table></div>
<aside class="worked-example"><h3>Example</h3><p>With AFI=22h, CAFS=2 and NAFS=2: slot 2 is current and remains scheduled after reset. CAFS=1 with NAFS=2 means activation has not crossed the reset boundary. This is an informative decode and remains subject to the bit definitions in Figure 215.</p></aside>
<details class="technical-note"><summary>Fields and data structures in more depth</summary>
<!-- figure-table:BASEFWLOG-FIG-203 -->
<details class="field-note" id="figure-BASEFWLOG-FIG-203"><summary>Base Figure 203 · Get Log Page – Data Pointer</summary>
<!-- claim:BASEFWLOG-FIG-203-CLAIM -->
<p>Figure 203, "Get Log Page – Data Pointer": Defines how Get Log Page – Data Pointer identifies the destination or source buffer for this command.</p><details class="source-note"><summary>Sources: Base 2.4 §5.2.13</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13, Figure 203, printed pages 213, PDF pages 239</p></details>

</details>
<!-- figure-table:BASEFWLOG-FIG-204 -->
<details class="field-note" id="figure-BASEFWLOG-FIG-204"><summary>Base Figure 204 · Get Log Page – Command Dword 10</summary>
<!-- claim:BASEFWLOG-FIG-204-CLAIM -->
<p>Figure 204, "Get Log Page – Command Dword 10": Defines the returned log-page layout and selection context for Get Log Page – Command Dword 10.</p><details class="source-note"><summary>Sources: Base 2.4 §5.2.13</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13, Figure 204, printed pages 213, PDF pages 239</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>NUMDL</dt><dd>Number of Dwords Lower, the low 16 bits of Get Log Page NUMD.</dd></div><div><dt>LSP</dt><dd>Log Specific Field, a command selector whose meaning is defined by the selected log page.</dd></div><div><dt>RAE</dt><dd>Retain Asynchronous Event, the Get Log Page selector controlling retention of a related asynchronous event.</dd></div></dl>
</details>
<!-- figure-table:BASEFWLOG-FIG-205 -->
<details class="field-note" id="figure-BASEFWLOG-FIG-205"><summary>Base Figure 205 · Get Log Page – Command Dword 11</summary>
<!-- claim:BASEFWLOG-FIG-205-CLAIM -->
<p>Figure 205, "Get Log Page – Command Dword 11": Defines the returned log-page layout and selection context for Get Log Page – Command Dword 11.</p><details class="source-note"><summary>Sources: Base 2.4 §5.2.13</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13, Figure 205, printed pages 214, PDF pages 240</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>NUMDU</dt><dd>Number of Dwords Upper, the high 16 bits of Get Log Page NUMD.</dd></div><div><dt>LSI</dt><dd>Log Specific Identifier, an identifier whose meaning is defined by the selected log page.</dd></div></dl>
</details>
<!-- figure-table:BASEFWLOG-FIG-206 -->
<details class="field-note" id="figure-BASEFWLOG-FIG-206"><summary>Base Figure 206 · Get Log Page – Command Dword 12</summary>
<!-- claim:BASEFWLOG-FIG-206-CLAIM -->
<p>Figure 206, "Get Log Page – Command Dword 12": Defines the returned log-page layout and selection context for Get Log Page – Command Dword 12.</p><details class="source-note"><summary>Sources: Base 2.4 §5.2.13</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13, Figure 206, printed pages 214, PDF pages 240</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>LPOL</dt><dd>Log Page Offset Lower, the low 32 bits of the Get Log Page byte offset.</dd></div></dl>
</details>
<!-- figure-table:BASEFWLOG-FIG-207 -->
<details class="field-note" id="figure-BASEFWLOG-FIG-207"><summary>Base Figure 207 · Get Log Page – Command Dword 13</summary>
<!-- claim:BASEFWLOG-FIG-207-CLAIM -->
<p>Figure 207, "Get Log Page – Command Dword 13": Defines the returned log-page layout and selection context for Get Log Page – Command Dword 13.</p><details class="source-note"><summary>Sources: Base 2.4 §5.2.13</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13, Figure 207, printed pages 214, PDF pages 240</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>LPOU</dt><dd>Log Page Offset Upper, the high 32 bits of the Get Log Page byte offset.</dd></div></dl>
</details>
<!-- figure-table:BASEFWLOG-FIG-208 -->
<details class="field-note" id="figure-BASEFWLOG-FIG-208"><summary>Base Figure 208 · Get Log Page – Command Dword 14</summary>
<!-- claim:BASEFWLOG-FIG-208-CLAIM -->
<p>Figure 208, "Get Log Page – Command Dword 14": Defines the returned log-page layout and selection context for Get Log Page – Command Dword 14.</p><details class="source-note"><summary>Sources: Base 2.4 §5.2.13</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13, Figure 208, printed pages 214-215, PDF pages 240-241</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>UIDX</dt><dd>UUID Index, an index into the UUID List; zero indicates that no UUID is specified.</dd></div><div><dt>CSI</dt><dd>Command Set Identifier, selecting the I/O Command Set context for a command or log page.</dd></div></dl>
</details>
<!-- figure-table:BASEFWLOG-FIG-209 -->
<details class="field-note" id="figure-BASEFWLOG-FIG-209"><summary>Base Figure 209 · Get Log Page – Log Page Identifiers</summary>
<!-- claim:BASEFWLOG-FIG-209-CLAIM -->
<p>Figure 209, "Get Log Page – Log Page Identifiers": Defines the returned log-page layout and selection context for Get Log Page – Log Page Identifiers.</p><details class="source-note"><summary>Sources: Base 2.4 §5.2.13</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13, Figure 209, printed pages 215-216, PDF pages 241-242</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>NVM subsystem</dt><dd>NVM subsystem, the NVMe system boundary containing controllers, ports, namespaces, and non-volatile storage resources.</dd></div><div><dt>NVM</dt><dd>Non-Volatile Memory, memory that retains data without power.</dd></div></dl>
</details>
<!-- figure-table:BASEFWLOG-FIG-215 -->
<details class="field-note" id="figure-BASEFWLOG-FIG-215"><summary>Base Figure 215 · Firmware Slot Information Log Page</summary>
<!-- claim:BASEFWLOG-FIG-215-CLAIM -->
<p>Figure 215, "Firmware Slot Information Log Page": Defines the returned log-page layout and selection context for Firmware Slot Information Log Page.</p><details class="source-note"><summary>Sources: Base 2.4 §5.2.13.1.4</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.4, Figure 215, printed pages 226, PDF pages 252</p></details>

</details>
</details>
</section>
<section id="additional-details"><h2 id="further-mechanisms">Additional mechanisms and data formats</h2>
<!-- claim:BASEFWLOG-MODEL-DOMAIN -->
<p>Controllers in one domain share firmware slots, and the same firmware image is applied to all controllers in that domain. If multiple domains are not supported, that scope is the entire NVM subsystem.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>NVM subsystem</dt><dd>NVM subsystem, the NVMe system boundary containing controllers, ports, namespaces, and non-volatile storage resources.</dd></div><div><dt>NVM</dt><dd>Non-Volatile Memory, memory that retains data without power.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §5.2.9</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.9, printed pages 202, PDF pages 228</p></details>
<!-- claim:BASEFWLOG-FW-RESET -->
<p>The reset-based flow is one or more Firmware Image Download commands, Firmware Commit to validate and place the image, a Controller Level Reset capable of causing activation, and reinitialization of the controller and I/O queues.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>I/O</dt><dd>Input/Output, the class of data operations performed on a namespace.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §3.11</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §3.11, printed pages 135-136, PDF pages 161-162</p></details>
<!-- claim:BASEFWLOG-FW-IMMEDIATE -->
<p>CA=011b requests immediate activation. Firmware Commit is not a background operation and remains in progress until activation succeeds or fails. If Firmware Activation notices are enabled, an affected controller may send Firmware Activation Starting.</p><details class="source-note"><summary>Sources: Base 2.4 §3.11</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §3.11, printed pages 136, PDF pages 162</p></details>
<!-- claim:BASEFWLOG-FW-FAILURE -->
<p>If the new image cannot be loaded, the controller shall revert to the image in the most recently activated slot; if that image also cannot be loaded, it loads an available baseline read-only image and generates Firmware Image Load Error.</p><details class="source-note"><summary>Sources: Base 2.4 §3.11</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §3.11, printed pages 136-137, PDF pages 162-163</p></details>
<!-- claim:BASEFWLOG-FW-SEQUENCE -->
<p>The host should not overlap firmware or Boot Partition update sequences and should use only one controller or Management Endpoint throughout a sequence.</p><details class="source-note"><summary>Sources: Base 2.4 §3.11</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §3.11, printed pages 137, PDF pages 163</p></details>
<!-- claim:BASEFWLOG-FW-DISCARD -->
<p>The first Firmware Image Download after Firmware Commit completes, and a Controller Level Reset after download but before Firmware Commit completion, shall cause the controller to discard remaining downloaded portions.</p><details class="source-note"><summary>Sources: Base 2.4 §3.11, 5.2.10</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §3.11, 5.2.10, printed pages 137, 205-206, PDF pages 163, 231-232</p></details>
<!-- claim:BASEFWLOG-UUID-LIST -->
<p>Across firmware revisions, UUID List entry positions should remain stable: new UUIDs should be appended, a removed UUID should be replaced in place with the NVMe Invalid UUID, an invalid entry should not be reused, and the list should not be shortened or removed.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>NVMe</dt><dd>Non-Volatile Memory Express, the specification family for a host interface to a non-volatile-memory subsystem.</dd></div><div><dt>UUID</dt><dd>Universally Unique Identifier, a 128-bit identifier whose association scope is defined by the containing structure.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §3.11.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §3.11.1, printed pages 137-138, PDF pages 163-164</p></details>
<!-- claim:BASEFWLOG-UUID-RESET -->
<p>If a downloaded image replaces the NVMe Invalid UUID or a different valid UUID with a valid UUID in an existing entry, the controller shall require reset, and all controllers affected by that UUID List change shall be reset.</p><details class="source-note"><summary>Sources: Base 2.4 §3.11.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §3.11.1, printed pages 138, PDF pages 164</p></details>
<!-- claim:BASEFWLOG-COMMIT-BOOT -->
<p>BPID and CA=110b/111b belong to Boot Partition handling: 110b replaces the selected partition, 111b marks it active, and Boot Partition Write Prohibited is one of the Firmware Commit command-specific status values.</p><details class="source-note"><summary>Sources: Base 2.4 §5.2.9</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.9, printed pages 203-205, PDF pages 229-231</p></details>
<!-- claim:BASEFWLOG-LOG-RAE -->
<p>RAE=0 clears the corresponding asynchronous event on successful completion, while RAE=1 retains it. If the command fails, the controller shall retain the event. Firmware Activation Starting is cleared by reading LID 03h with RAE=0.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>RAE</dt><dd>Retain Asynchronous Event, the Get Log Page selector controlling retention of a related asynchronous event.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §5.2.2, 5.2.13</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.2, 5.2.13, printed pages 186, 213, PDF pages 212, 239</p></details>
<!-- claim:BASEFWLOG-LOG-OFFSET -->
<p>This report uses the complete 512-byte LID 03h with LPOL=LPOU=0 and OT=0. A general byte offset is dword aligned, and an offset beyond the log page shall return Invalid Field in Command. LID 03h needs no index-offset branch.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>LPOL</dt><dd>Log Page Offset Lower, the low 32 bits of the Get Log Page byte offset.</dd></div><div><dt>LPOU</dt><dd>Log Page Offset Upper, the high 32 bits of the Get Log Page byte offset.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §5.2.13</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13, printed pages 214-215, PDF pages 240-241</p></details>
<!-- claim:BASEFWLOG-LID03-DESCRIPTION -->
<p>The 512-byte Firmware Slot Information log page reports the firmware revision stored in each supported slot and identifies the current active slot plus the next active slot when reported. Revisions are ASCII strings.</p><details class="source-note"><summary>Sources: Base 2.4 §5.2.13.1.4</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.4, printed pages 225-226, PDF pages 251-252</p></details>
<!-- claim:BASEFWLOG-RESET-XREF -->
<p>NVMe over PCIe Transport lists Conventional Reset and Function Level Reset as distinct additional transport-specific Controller Level Reset methods. Except for Controller Reset, Controller Level Reset resets PCI register space as defined by the PCI Express Base Specification.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>PCIe</dt><dd>PCI Express, the transport and device interconnect used by an NVMe memory-based controller.</dd></div></dl><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.3</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.3, printed pages 11, PDF pages 11</p></details>
<!-- claim:BASEFWLOG-XREF-337 -->
<p>Source §5.2.9 points Firmware Revision to Figure 337, but Figure 337 contains Command Set Identifiers and FR appears in Figure 338. Without separately approved errata, this report preserves and discloses the internal source discrepancy instead of silently rewriting it.</p><details class="source-note"><summary>Sources: Base 2.4 §5.2.9, 5.2.14.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.9, 5.2.14.1, printed pages 202, 340, PDF pages 228, 366</p></details>
<!-- figure-table:BASEFWLOG-FIG-155 -->
<details class="field-note" id="figure-BASEFWLOG-FIG-155"><summary>Base Figure 155 · Asynchronous Event Information – Notice</summary>
<!-- claim:BASEFWLOG-FIG-155-CLAIM -->
<p>Figure 155, "Asynchronous Event Information – Notice": Defines the event record, event taxonomy, or logging condition represented by Asynchronous Event Information – Notice.</p><details class="source-note"><summary>Sources: Base 2.4 §5.2.2.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.2.1, Figure 155, printed pages 186, PDF pages 212</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>CSTS.PP</dt><dd>Controller Status, the property through which a controller reports ready, fatal-status, and shutdown state. Here CSTS.PP selects its PP member field.</dd></div><div><dt>CSTS</dt><dd>Controller Status, the property through which a controller reports ready, fatal-status, and shutdown state.</dd></div></dl>
</details>
<!-- figure-table:BASEFWLOG-FIG-347 -->
<details class="field-note" id="figure-BASEFWLOG-FIG-347"><summary>Base Figure 347 · UUID List</summary>
<!-- claim:BASEFWLOG-FIG-347-CLAIM -->
<p>Figure 347, "UUID List": Defines the identifier composition or namespace of values shown by UUID List.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>namespace</dt><dd>Namespace, a formatted quantity of non-volatile memory accessed by a host through a controller.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §5.2.14.2.14</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.14.2.14, Figure 347, printed pages 396, PDF pages 422</p></details>

</details>
<!-- figure-table:BASEFWLOG-FIG-348 -->
<details class="field-note" id="figure-BASEFWLOG-FIG-348"><summary>Base Figure 348 · UUID List Entry</summary>
<!-- claim:BASEFWLOG-FIG-348-CLAIM -->
<p>Figure 348, "UUID List Entry": Defines the identifier composition or namespace of values shown by UUID List Entry.</p><details class="source-note"><summary>Sources: Base 2.4 §5.2.14.2.14</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.14.2.14, Figure 348, printed pages 396, PDF pages 422</p></details>

</details>
<!-- figure-table:BASEFWLOG-FIG-474 -->
<details class="field-note" id="figure-BASEFWLOG-FIG-474"><summary>Base Figure 474 · Asynchronous Event Configuration – Command Dword 11</summary>
<!-- claim:BASEFWLOG-FIG-474-CLAIM -->
<p>Figure 474, "Asynchronous Event Configuration – Command Dword 11": Defines the event record, event taxonomy, or logging condition represented by Asynchronous Event Configuration – Command Dword 11.</p><details class="source-note"><summary>Sources: Base 2.4 §5.2.30.1.6</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.6, Figure 474, printed pages 466-468, PDF pages 492-494</p></details>

</details>
</section>
<section id="knowledge-check"><h2 id="review-questions">Check your understanding</h2>
<!-- qa:base-admin-fw-logs-download-activate -->
<details class="review-question" id="qa-base-admin-fw-logs-download-activate"><summary>1. Is new firmware executing as soon as Firmware Image Download completes?</summary>
<div data-qa-answer="base-admin-fw-logs-download-activate"><p>Download transfers the image. Commit selects storage or activation behavior, and activation may require a specified reset. Commit results and slot information establish the currently running version.</p></div>
<details class="source-note"><summary>Sources</summary>
<p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.10, printed pages 205-206, PDF pages 231-232</p>
<p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.9, printed pages 202-203, PDF pages 228-229</p>
</details></details>
<!-- qa:base-admin-fw-logs-download-units -->
<details class="review-question" id="qa-base-admin-fw-logs-download-units"><summary>2. What do NUMD=255 and OFST=256 describe?</summary>
<div data-qa-answer="base-admin-fw-logs-download-units"><p>NUMD is a zero-based dword length: 256 dwords, or 1024 bytes, are transferred. OFST is a dword offset from the image start, so the transfer begins at byte 1024. Their encoding roles differ.</p></div>
<details class="source-note"><summary>Sources</summary>
<p>Source: NVME-BASE-2.4, Rev. 2.4, §4.1.1, 5.2.10, printed pages 140-142, 205-206, PDF pages 166-168, 231-232</p>
</details></details>
<!-- qa:base-admin-fw-logs-slot-version -->
<details class="review-question" id="qa-base-admin-fw-logs-slot-version"><summary>3. Does a new version in a slot’s FRS prove that it is running?</summary>
<div data-qa-answer="base-admin-fw-logs-slot-version"><p>FRS describes the revision stored in a slot. Active-slot and next-active-slot information are also needed. Stored, currently running, and pending activation are distinct states.</p></div>
<details class="source-note"><summary>Sources</summary>
<p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.4, printed pages 226, PDF pages 252</p>
<p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.4, printed pages 226, PDF pages 252</p>
</details></details>
<!-- qa:base-admin-fw-logs-firmware-domain -->
<details class="review-question" id="qa-base-admin-fw-logs-firmware-domain"><summary>4. Why is a firmware update not always a private change to one controller?</summary>
<div data-qa-answer="base-admin-fw-logs-firmware-domain"><p>Firmware scope may involve shared domain or NVM subsystem resources. Establish the relationship between the controller and update scope to understand effects on other controllers.</p></div>
<details class="source-note"><summary>Sources</summary>
<p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.9, printed pages 202, PDF pages 228</p>
</details></details>
</section>
<footer class="reference-editions"><details class="source-note"><summary>Specification editions</summary><p>NVM Express Base Specification, Revision 2.4</p><p>NVM Express NVMe over PCIe Transport Specification, Revision 1.4</p></details></footer>
</div>
