---
permalink: /nvme/boot-telemetry-sanitize-en/
layout: post
read_time: true
show_date: true
title: "NVMe 2.4: Boot Partitions, Telemetry, and Sanitize"
date: 2026-09-03
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
[繁體中文]({% post_url 2026-09-03-nvme-boot-telemetry-sanitize-zh-tw %})


<div class="nvme-note">
<section id="topic-overview" class="topic-overview">
<p class="opening">Boot Partitions, Telemetry, and Sanitize handle boot images, device internal-state data, and data sanitization. This note connects them through a shared control model: establish capabilities, then distinguish the command request, background state, and reported data to understand what an operation actually accomplished.</p>
<h2 id="main-ideas">The main ideas</h2>
<div class="topic-map">
<article><span class="axis-number">01</span><h3>Boot Partitions</h3><p>Read and update boot images, distinguishing the active partition from write protection.</p></article>
<article><span class="axis-number">02</span><h3>Telemetry</h3><p>Understand data areas, snapshot versions, and consistency across segmented reads.</p></article>
<article><span class="axis-number">03</span><h3>Sanitize</h3><p>Distinguish targets, methods, background states, and post-sanitization read behavior.</p></article>
</div>

<p>Command completion and background-operation completion can be separate events. Get Log Page retrieves reported data; Get/Set Features query and configure functions. Relevant identifiers and fields are explained where used.</p>
</section>
<section class="lesson" id="module-boot-read"><h2 id="heading-boot-read"><span class="section-number">01</span> Two Boot read paths</h2>
<p>First determine whether an Admin-command environment exists, then choose properties or LID 15h. Both access boot contents, but their return formats and observation points differ.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>Admin</dt><dd>Administrative, the control path used to create, configure, query, or manage controllers and queues.</dd></div><div><dt>LID</dt><dd>Log Page Identifier: selects the type of log page to read.</dd></div></dl>
<details class="technical-note"><summary>Mechanism and applicable conditions</summary>
<!-- claim:BASEBTS-BOOT-MODEL -->
<p>Boot Partitions are optional; support provides two equally sized partitions with IDs 0h and 1h. A host can read through properties without creating queues or enabling the controller.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>controller</dt><dd>Controller, the entity that implements the NVMe interface, fetches commands, and reports completions.</dd></div><div><dt>Host</dt><dd>The system running the operating system and issuing NVMe commands.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §8.1.3</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §8.1.3, printed pages 586, PDF pages 612</p></details>
<!-- claim:BASEBTS-BOOT-READ -->
<p>The host checks CAP.BPS and the active ID/size in BPINFO, allocates a contiguous buffer and programs BPMBL, then writes BPRSEL only when no read is active. BRS=01b means transfer in progress, 10b success, and 11b error; reset, shutdown, and changes to transport-specific properties are prohibited during the read.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>BRS</dt><dd>Boot Read Status: 00b no request, 01b in progress, 10b success, 11b error.</dd></div><div><dt>CAP</dt><dd>Controller Capabilities, the controller property at offset 00h that reports queue, page-size, timeout, and other capabilities.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §8.1.3.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §8.1.3.1, printed pages 586-587, PDF pages 612-613</p></details>
<!-- claim:BASEBTS-BOOT-LOG -->
<p>LID 15h selects a partition through BPID in CDW10.LSP and returns a 16-byte header followed by data; BPSZ is measured in 128 KiB units. Reading this log does not modify the BPINFO, BPRSEL, or BPMBL properties.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>BPID</dt><dd>Boot Partition Identifier; selects 0 or 1 independently of the active partition.</dd></div><div><dt>BPSZ</dt><dd>Boot Partition Size; each unit is 128 KiB.</dd></div><div><dt>CDW</dt><dd>Command Dword: a 32-bit unit in a command, followed by its index.</dd></div><div><dt>LSP</dt><dd>Log Specific Field, a command selector whose meaning is defined by the selected log page.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §5.2.13.1.21</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.21, printed pages 283-284, PDF pages 309-310</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">Item</th><th scope="col">Role or distinction</th><th scope="col">Conditions</th></tr></thead><tbody><tr><td>Properties</td><td>BRS reports read state</td><td>Does not require CC.EN=1</td></tr><tr><td>LID 15h</td><td>16-byte header + data</td><td>The Admin-command CQE reports the command result</td></tr><tr><td>BPID</td><td>Selects the partition to read</td><td>Not the active ID</td></tr><tr><td>BPSZ</td><td>128 KiB per unit</td><td>Not a byte count</td></tr></tbody></table></div><dl class="term-note" aria-label="Terms in this passage"><div><dt>BPID</dt><dd>Boot Partition Identifier; selects 0 or 1 independently of the active partition.</dd></div><div><dt>BPSZ</dt><dd>Boot Partition Size; each unit is 128 KiB.</dd></div><div><dt>BRS</dt><dd>Boot Read Status: 00b no request, 01b in progress, 10b success, 11b error.</dd></div><div><dt>CQE</dt><dd>Completion Queue Entry, one completion-result structure in a CQ.</dd></div><div><dt>CC</dt><dd>Controller Configuration, the property through which the host selects settings and enables or disables a controller.</dd></div><div><dt>EN</dt><dd>Enable, the CC bit controlling controller enable state.</dd></div></dl>
<aside class="worked-example"><h3>Example</h3><p>With BPSZ=2, LID 15h contains 262144 bytes of boot data plus a 16-byte header, totaling 262160 bytes. Reading BP1 does not activate BP1, and a log read does not advance the property's BRS.</p></aside>
<details class="technical-note"><summary>Fields and data structures in more depth</summary>
<!-- figure-table:BASEBTS-BASE-FIG-279 -->
<details class="field-note" id="figure-BASEBTS-BASE-FIG-279"><summary>Base Figure 279 · Boot Partition Log Specific Parameter Field</summary>
<!-- claim:BASEBTS-BASE-FIG-279-CLAIM -->
<p>Figure 279, "Boot Partition Log Specific Parameter Field": LID 15h uses CDW10 bit 8 as BPID and reserves other LSP bits; that same bit means CTHID for 07h.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>CTHID</dt><dd>Create Telemetry Host-Initiated Data; the 07h capture request, cleared for subsequent reads of that snapshot.</dd></div><div><dt>CDW</dt><dd>Command Dword: a 32-bit unit in a command, followed by its index.</dd></div><div><dt>LSP</dt><dd>Log Specific Field, a command selector whose meaning is defined by the selected log page.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §5.2.13.1.21</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.21, Figure 279, printed pages 283, PDF pages 309</p></details>

</details>
<!-- figure-table:BASEBTS-BASE-FIG-280 -->
<details class="field-note" id="figure-BASEBTS-BASE-FIG-280"><summary>Base Figure 280 · Boot Partition Log Page</summary>
<!-- claim:BASEBTS-BASE-FIG-280-CLAIM -->
<p>Figure 280, "Boot Partition Log Page": Header bytes are 0–15; BPINFO occupies 4–7 with ABPID at bit 31 and BPSZ at bits 14:0. BPD begins at byte 16 and is BPSZ×128 KiB long.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>ABPID</dt><dd>Active Boot Partition ID; identifies the partition selected as the boot image.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §5.2.13.1.21</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.21, Figure 280, printed pages 284, PDF pages 310</p></details>

</details>
<!-- figure-table:BASEBTS-BASE-FIG-679 -->
<details class="field-note" id="figure-BASEBTS-BASE-FIG-679"><summary>Base Figure 679 · Boot Partition Overview</summary>
<!-- claim:BASEBTS-BASE-FIG-679-CLAIM -->
<p>Figure 679, "Boot Partition Overview": Separate the two equal Boot Partitions from this read's host buffer. Active ID selects the boot image, not a restriction to reading only the active partition.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>Host</dt><dd>The system running the operating system and issuing NVMe commands.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §8.1.3.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §8.1.3.1, Figure 679, printed pages 587, PDF pages 613</p></details>

</details>
<!-- figure-table:BASEBTS-BASE-FIG-036 -->
<details class="field-note" id="figure-BASEBTS-BASE-FIG-036"><summary>Base Figure 36 · Offset 0h: CAP - Controller Capabilities</summary>
<!-- claim:BASEBTS-BASE-FIG-036-CLAIM -->
<p>Figure 36, "Offset 0h: CAP - Controller Capabilities": Check BPS before using Boot properties; Boot support does not imply an enabled controller.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>controller</dt><dd>Controller, the entity that implements the NVMe interface, fetches commands, and reports completions.</dd></div><div><dt>CAP</dt><dd>Controller Capabilities, the controller property at offset 00h that reports queue, page-size, timeout, and other capabilities.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §3.1.4.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.1, Figure 36, printed pages 55-58, PDF pages 81-84</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>CAP.BPS</dt><dd>Controller Capabilities, the controller property at offset 00h that reports queue, page-size, timeout, and other capabilities. Here CAP.BPS selects its BPS member field.</dd></div></dl>
</details>
<!-- figure-table:BASEBTS-BASE-FIG-049 -->
<details class="field-note" id="figure-BASEBTS-BASE-FIG-049"><summary>Base Figure 49 · Offset 40h: BPINFO - Boot Partition Information</summary>
<!-- claim:BASEBTS-BASE-FIG-049-CLAIM -->
<p>Figure 49, "Offset 40h: BPINFO - Boot Partition Information": ABPID identifies the active partition, BPSZ uses 128 KiB units, and BRS distinguishes no request/in progress/success/error with 00b/01b/10b/11b.</p><details class="source-note"><summary>Sources: Base 2.4 §3.1.4.13</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.13, Figure 49, printed pages 69, PDF pages 95</p></details>

</details>
<!-- figure-table:BASEBTS-BASE-FIG-050 -->
<details class="field-note" id="figure-BASEBTS-BASE-FIG-050"><summary>Base Figure 50 · Offset 44h: BPRSEL - Boot Partition Read Select</summary>
<!-- claim:BASEBTS-BASE-FIG-050-CLAIM -->
<p>Figure 50, "Offset 44h: BPRSEL - Boot Partition Read Select": BPRSEL bit 31 is BPID, bit 30 is reserved, [29:10] is BPROF in 4 KiB units, and [9:0] is BPRSZ in 4 KiB units; writing initiates a read.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>BPROF</dt><dd>Boot Partition Read Offset; BPRSEL bits 29:10 in 4 KiB units; bit 30 is reserved.</dd></div><div><dt>BPRSZ</dt><dd>Boot Partition Read Size; uses 4 KiB units, not BPSZ units.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §3.1.4.14</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.14, Figure 50, printed pages 69-70, PDF pages 95-96</p></details>

</details>
<!-- figure-table:BASEBTS-BASE-FIG-051 -->
<details class="field-note" id="figure-BASEBTS-BASE-FIG-051"><summary>Base Figure 51 · Offset 48h: BPMBL - Boot Partition Memory Buffer Location</summary>
<!-- claim:BASEBTS-BASE-FIG-051-CLAIM -->
<p>Figure 51, "Offset 48h: BPMBL - Boot Partition Memory Buffer Location": BPMBL[63:12] provides the Boot Memory Buffer base address; the low 12 bits are reserved. Establish a contiguous, aligned host buffer first.</p><details class="source-note"><summary>Sources: Base 2.4 §3.1.4.15</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.15, Figure 51, printed pages 70, PDF pages 96</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>BMBBA</dt><dd>Boot Memory Buffer Base Address; BPMBL bits 63:12, with the low 12 bits reserved.</dd></div></dl>
</details>
</details>
</section>
<section class="lesson" id="module-boot-protection"><h2 id="heading-boot-protection"><span class="section-number">02</span> The complete update and protection lifecycle</h2>
<p>Track image transfer, partition contents, active selection, and write protection separately. Successful download has not yet written a Boot Partition, and a successful write has not automatically activated it.</p>
<details class="technical-note"><summary>Mechanism and applicable conditions</summary>
<!-- claim:BASEBTS-BOOT-UPDATE -->
<p>A boot image is downloaded in order from its beginning using Firmware Image Download. After unlocking the target, Firmware Commit CA=110b writes the partition selected by BPID. The host may read it back, use CA=111b to change the active ID, and relock it. An interrupted update can leave mixed old/new contents, so verification before activation is recommended.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>Host</dt><dd>The system running the operating system and issuing NVMe commands.</dd></div><div><dt>CA</dt><dd>Commit Action, the Firmware Commit field selecting replacement, activation, and reset policy.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §8.1.3.2</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §8.1.3.2, printed pages 587-588, PDF pages 613-614</p></details>
<!-- claim:BASEBTS-BOOT-SEQUENCE -->
<p>The host should avoid reading a Boot Partition while it is being written and should avoid overlapping firmware/boot-image update sequences. A single sequence should use the same controller or Management Endpoint; crossing endpoints may cause Commit to end with Invalid Firmware Image.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>controller</dt><dd>Controller, the entity that implements the NVMe interface, fetches commands, and reports completions.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §8.1.3.2</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §8.1.3.2, printed pages 588, PDF pages 614</p></details>
<!-- claim:BASEBTS-BOOT-CAP -->
<p>BPCAP reports Set Features and RPMB boot-protection capabilities. FID 85h controls protection when it is the only mechanism or RPMB protection is not enabled; enabled RPMB protection takes control. Only one mechanism owns the state at a time, and all controllers sharing a partition enforce its protection.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>BPCAP</dt><dd>Boot Partition Capabilities; identifies the supported combination of Set Features and RPMB protection.</dd></div><div><dt>FID</dt><dd>Feature Identifier: selects the Feature to read or configure.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §8.1.3.3</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §8.1.3.3, printed pages 588-589, PDF pages 614-615</p></details>
<!-- claim:BASEBTS-BOOT-FID -->
<p>BP0WPS occupies CDW11[2:0] and BP1WPS [5:3]. Value 000b is a Set-only no-change request; 001b/010b/011b mean unlocked/locked/locked until power cycle. Get reports 100b for RPMB ownership, but it is not a valid Set value. This Feature is not saveable and defaults to locked after a power cycle.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>BP0WPS</dt><dd>Boot Partition 0 Write Protection State; bits 2:0 of FID 85h.</dd></div><div><dt>BP1WPS</dt><dd>Boot Partition 1 Write Protection State; bits 5:3 of FID 85h.</dd></div><div><dt>CDW</dt><dd>Command Dword: a 32-bit unit in a command, followed by its index.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §5.2.30.1.39</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.39, printed pages 513-514, PDF pages 539-540</p></details>
<!-- claim:BASEBTS-BOOT-RESET -->
<p>Set Features unlocked state survives a Controller Level Reset but returns to locked after a power cycle; ordinary Set cannot escape locked-until-power-cycle. With RPMB protection enabled, either a power cycle or Controller Level Reset relocks an unlocked partition, and enabling protection is irreversible.</p><details class="source-note"><summary>Sources: Base 2.4 §8.1.3.3.1-8.1.3.3.3</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §8.1.3.3.1-8.1.3.3.3, printed pages 589-594, PDF pages 615-620</p></details>
<!-- claim:BASEBTS-BOOT-REJECT -->
<p>FID 85h rejects changes to locked-until-power-cycle or RPMB-owned states with Feature Not Changeable. A shared partition in a multi-domain subsystem cannot use locked-until-power-cycle. When both mechanisms exist, RPMB boot protection cannot be enabled while either partition is in that state to bypass it.</p><details class="source-note"><summary>Sources: Base 2.4 §5.2.30.1.39; 8.1.3.3.3</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.39; 8.1.3.3.3, printed pages 513-514,593-594, PDF pages 539-540,619-620</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">Item</th><th scope="col">Role or distinction</th><th scope="col">Conditions</th></tr></thead><tbody><tr><td>FID 85h unlocked</td><td>Survives controller reset</td><td>Locked after power cycle</td></tr><tr><td>FID 85h until power cycle</td><td>Ordinary Set cannot unlock</td><td>Unavailable for shared multi-domain partitions</td></tr><tr><td>RPMB enabled/unlocked</td><td>Controller reset relocks</td><td>Protection enablement cannot be reversed</td></tr><tr><td>Both mechanisms</td><td>Only one owns control at a time</td><td>RPMB enablement transfers ownership</td></tr></tbody></table></div><dl class="term-note" aria-label="Terms in this passage"><div><dt>controller</dt><dd>Controller, the entity that implements the NVMe interface, fetches commands, and reports completions.</dd></div><div><dt>FID</dt><dd>Feature Identifier: selects the Feature to read or configure.</dd></div></dl>
<aside class="worked-example"><h3>Example</h3><p>To leave BP0 unchanged and unlock BP1, FID 85h CDW11 is (001b &lt;&lt; 3) | 000b = 08h. A subsequent Get does not return 000b for BP0; it returns its actual state, or 100b when RPMB owns protection.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>CDW</dt><dd>Command Dword: a 32-bit unit in a command, followed by its index.</dd></div></dl></aside>
<details class="technical-note"><summary>Fields and data structures in more depth</summary>
<!-- figure-table:BASEBTS-BASE-FIG-542 -->
<details class="field-note" id="figure-BASEBTS-BASE-FIG-542"><summary>Base Figure 542 · Boot Partition Write Protection Config - Command Dword 11</summary>
<!-- claim:BASEBTS-BASE-FIG-542-CLAIM -->
<p>Figure 542, "Boot Partition Write Protection Config - Command Dword 11": The two three-bit state fields are set independently. 000b only requests no change in Set; Get returns actual state and uses 100b only to report RPMB ownership.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>Dword</dt><dd>Double word: 32 bits, or 4 bytes.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §5.2.30.1.39</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.39, Figure 542, printed pages 513-514, PDF pages 539-540</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>BP0WPS</dt><dd>Boot Partition 0 Write Protection State; bits 2:0 of FID 85h.</dd></div><div><dt>BP1WPS</dt><dd>Boot Partition 1 Write Protection State; bits 5:3 of FID 85h.</dd></div></dl>
</details>
<!-- figure-table:BASEBTS-BASE-FIG-680 -->
<details class="field-note" id="figure-BASEBTS-BASE-FIG-680"><summary>Base Figure 680 · Set Features Boot Partition Write Protection State Machine Model</summary>
<!-- claim:BASEBTS-BASE-FIG-680-CLAIM -->
<p>Figure 680, "Set Features Boot Partition Write Protection State Machine Model": Set Features switches unlocked/locked and can move either to locked-until-power-cycle; a power cycle returns to locked. There is no ordinary Set-unlock edge from locked-until-power-cycle.</p><details class="source-note"><summary>Sources: Base 2.4 §8.1.3.3.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §8.1.3.3.1, Figure 680, printed pages 589, PDF pages 615</p></details>

</details>
<!-- figure-table:BASEBTS-BASE-FIG-681 -->
<details class="field-note" id="figure-BASEBTS-BASE-FIG-681"><summary>Base Figure 681 · Set Features Boot Partition Write Protection State Definitions</summary>
<!-- claim:BASEBTS-BASE-FIG-681-CLAIM -->
<p>Figure 681, "Set Features Boot Partition Write Protection State Definitions": Compare all three states: controller reset preserves them, while power cycle changes unlocked and until-power-cycle to locked.</p><details class="source-note"><summary>Sources: Base 2.4 §8.1.3.3.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §8.1.3.3.1, Figure 681, printed pages 590, PDF pages 616</p></details>

</details>
<!-- figure-table:BASEBTS-BASE-FIG-682 -->
<details class="field-note" id="figure-BASEBTS-BASE-FIG-682"><summary>Base Figure 682 · RPMB Boot Partition Write Protection State Machine Model</summary>
<!-- claim:BASEBTS-BASE-FIG-682-CLAIM -->
<p>Figure 682, "RPMB Boot Partition Write Protection State Machine Model": Before and after RPMB enablement are different regions; once enabled, authenticated configuration writes unlock/lock and resets return to locked.</p><details class="source-note"><summary>Sources: Base 2.4 §8.1.3.3.2</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §8.1.3.3.2, Figure 682, printed pages 591, PDF pages 617</p></details>

</details>
<!-- figure-table:BASEBTS-BASE-FIG-683 -->
<details class="field-note" id="figure-BASEBTS-BASE-FIG-683"><summary>Base Figure 683 · RPMB Boot Partition Write Protection State Definitions</summary>
<!-- claim:BASEBTS-BASE-FIG-683-CLAIM -->
<p>Figure 683, "RPMB Boot Partition Write Protection State Definitions": For RPMB-only protection before enablement, unlocked can persist; once enabled, unlocked does not survive reset/power cycle. Dual-mechanism support also requires Figure 684's defaults and ownership rules.</p><details class="source-note"><summary>Sources: Base 2.4 §8.1.3.3.2</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §8.1.3.3.2, Figure 683, printed pages 591, PDF pages 617</p></details>

</details>
<!-- figure-table:BASEBTS-BASE-FIG-684 -->
<details class="field-note" id="figure-BASEBTS-BASE-FIG-684"><summary>Base Figure 684 · Boot Partition Write Protection State Machine Model</summary>
<!-- claim:BASEBTS-BASE-FIG-684-CLAIM -->
<p>Figure 684, "Boot Partition Write Protection State Machine Model": Track states in the Set Features region, then transfer through the enable gate to RPMB; until-power-cycle cannot be bypassed through RPMB enablement.</p><details class="source-note"><summary>Sources: Base 2.4 §8.1.3.3.3</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §8.1.3.3.3, Figure 684, printed pages 593, PDF pages 619</p></details>

</details>
<!-- figure-table:BASEBTS-BASE-FIG-187 -->
<details class="field-note" id="figure-BASEBTS-BASE-FIG-187"><summary>Base Figure 187 · Firmware Commit - Command Dword 10</summary>
<!-- claim:BASEBTS-BASE-FIG-187-CLAIM -->
<p>Figure 187, "Firmware Commit - Command Dword 10": For Boot, use BPID and CA=110b/111b: the former replaces partition contents and the latter changes the active ID. They are separate actions.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>CA</dt><dd>Commit Action, the Firmware Commit field selecting replacement, activation, and reset policy.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §5.2.9</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.9, Figure 187, printed pages 203, PDF pages 229</p></details>

</details>
<!-- figure-table:BASEBTS-BASE-FIG-756 -->
<details class="field-note" id="figure-BASEBTS-BASE-FIG-756"><summary>Base Figure 756 · RPMB Device Configuration Block Data Structure</summary>
<!-- claim:BASEBTS-BASE-FIG-756-CLAIM -->
<p>Figure 756, "RPMB Device Configuration Block Data Structure": The Device Configuration Block separates protection enablement from each partition's lock control; once enabled, writes attempting to disable RPMB Boot protection are rejected.</p><details class="source-note"><summary>Sources: Base 2.4 §8.1.24</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §8.1.24, Figure 756, printed pages 691-692, PDF pages 717-718</p></details>

</details>
<!-- figure-table:BASEBTS-BASE-FIG-765 -->
<details class="field-note" id="figure-BASEBTS-BASE-FIG-765"><summary>Base Figure 765 · RPMB - Authenticated Device Configuration Block Write Flow</summary>
<!-- claim:BASEBTS-BASE-FIG-765-CLAIM -->
<p>Figure 765, "RPMB - Authenticated Device Configuration Block Write Flow": Verify the result after an authenticated configuration write. This changes Boot protection state, not image contents as Firmware Commit does.</p><details class="source-note"><summary>Sources: Base 2.4 §8.1.24.3</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §8.1.24.3, Figure 765, printed pages 700, PDF pages 726</p></details>

</details>
<!-- figure-table:BASEBTS-BASE-FIG-766 -->
<details class="field-note" id="figure-BASEBTS-BASE-FIG-766"><summary>Base Figure 766 · RPMB - Authenticated Device Configuration Block Read Flow</summary>
<!-- claim:BASEBTS-BASE-FIG-766-CLAIM -->
<p>Figure 766, "RPMB - Authenticated Device Configuration Block Read Flow": Authenticated configuration read retrieves verifiable protection settings used to establish which mechanism currently controls the partition.</p><details class="source-note"><summary>Sources: Base 2.4 §8.1.24.4</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §8.1.24.4, Figure 766, printed pages 701, PDF pages 727</p></details>

</details>
</details>
</section>
<section class="lesson" id="module-telemetry-layout"><h2 id="heading-telemetry-layout"><span class="section-number">03</span> Computing snapshots from Last Block</h2>
<p>Areas are differently sized views starting at the same block 1. Read the fields the header, select the final applicable populated area, and do not add the three Last Block numbers.</p>
<figure><div class="diagram-scroll"><svg viewBox="0 0 760 260" role="img"><title>Telemetry Data Areas are cumulative</title><desc>The header occupies block 0. Each Data Area starts at block 1, and larger areas include the data in smaller areas.</desc><rect x="20" y="20" width="155" height="210" rx="6" class="v-command"/><text x="97.5" y="118.5" text-anchor="middle" font-size="17">Header</text><text x="97.5" y="143.5" text-anchor="middle" font-size="17">Block 0</text><rect x="205" y="20" width="160" height="55" rx="6" class="v-object"/><text x="285.0" y="53.5" text-anchor="middle" font-size="17">Area 1</text><rect x="205" y="95" width="325" height="55" rx="6" class="v-decision"/><text x="367.5" y="128.5" text-anchor="middle" font-size="17">Area 2</text><rect x="205" y="170" width="535" height="55" rx="6" class="v-success"/><text x="472.5" y="203.5" text-anchor="middle" font-size="17">Area 3</text></svg></div><figcaption>The header occupies block 0. Each Data Area starts at block 1, and larger areas include the data in smaller areas.</figcaption></figure>

<details class="technical-note"><summary>Mechanism and applicable conditions</summary>
<!-- claim:BASEBTS-TEL-MODEL -->
<p>Telemetry uses block 0 for its header and 512-byte blocks. Every Data Area begins at block 1. Areas 2/3/4 are larger cumulative sets, not disjoint regions placed after Area 1. Last Block is an inclusive block number; payload format and size are vendor-defined.</p><details class="source-note"><summary>Sources: Base 2.4 §8.1.30; 5.2.13.1.8-5.2.13.1.9</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §8.1.30; 5.2.13.1.8-5.2.13.1.9, printed pages 232-237,733-737, PDF pages 258-263,759-763</p></details>
<!-- claim:BASEBTS-TEL-DA4 -->
<p>The controller advertises Telemetry through LPA.TS and Area 4 through LPA.DA4S; the host advertises support with ETDAS=1 in FID 16h Host Behavior Support. DA4S and ETDAS together determine Area 4 applicability; creating Area 4 also requires a populated Area 3.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>ETDAS</dt><dd>Extended Telemetry Data Area 4 Supported; the host's Area 4 declaration in Host Behavior Support.</dd></div><div><dt>Host</dt><dd>The system running the operating system and issuing NVMe commands.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §8.1.30; 5.2.30.1.15</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §8.1.30; 5.2.30.1.15, printed pages 476,733-734, PDF pages 502,759-760</p></details>
<!-- claim:BASEBTS-TEL-ALIGN -->
<p>For LID 07h/08h, offset and transfer length must be multiples of 512 bytes or the command reports Invalid Field in Command. The controller returns requested blocks, but data beyond the applicable final Data Area boundary has undefined contents.</p><details class="source-note"><summary>Sources: Base 2.4 §5.2.13.1.8-5.2.13.1.9</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.8-5.2.13.1.9, printed pages 232-237, PDF pages 258-263</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">Item</th><th scope="col">Role or distinction</th><th scope="col">Conditions</th></tr></thead><tbody><tr><td>Area 1</td><td>1 through L1</td><td>L1=0 means no data</td></tr><tr><td>Area 2</td><td>1 through L2</td><td>L2 &gt;= L1</td></tr><tr><td>Area 3</td><td>1 through L3</td><td>L3 &gt;= L2</td></tr><tr><td>Area 4</td><td>1 through L4</td><td>Check support separately</td></tr></tbody></table></div>
<aside class="worked-example"><h3>Example</h3><p>For Last Blocks=65/1000/30000, Area 3 payload is 30000×512=15360000 bytes and the log including its header is 15360512 bytes. Values 0/1000/1000 mean Area 1 is empty and Area 3 adds no content beyond Area 2.</p></aside>
<details class="technical-note"><summary>Fields and data structures in more depth</summary>
<!-- figure-table:BASEBTS-BASE-FIG-221 -->
<details class="field-note" id="figure-BASEBTS-BASE-FIG-221"><summary>Base Figure 221 · Telemetry Host-Initiated Log Page</summary>
<!-- claim:BASEBTS-BASE-FIG-221-CLAIM -->
<p>Figure 221, "Telemetry Host-Initiated Log Page": For 07h, Last Blocks occupy bytes 8–19, THS 380, THDGN 381, TCDA/TCDGN 382/383, and RID 384–511. Read the header before fetching cumulative-area payloads.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>TCDGN</dt><dd>Telemetry Controller-Initiated Data Generation Number; an eight-bit generation incremented at the end of an update.</dd></div><div><dt>THDGN</dt><dd>Telemetry Host-Initiated Data Generation Number; checks whether chunks still belong to one snapshot.</dd></div><div><dt>Host</dt><dd>The system running the operating system and issuing NVMe commands.</dd></div><div><dt>TCDA</dt><dd>Telemetry Controller-Initiated Data Available; in 2.4, indicates an update since the last RAE=0 acknowledgement.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §5.2.13.1.8</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.8, Figure 221, printed pages 234-235, PDF pages 260-261</p></details>

</details>
<!-- figure-table:BASEBTS-BASE-FIG-223 -->
<details class="field-note" id="figure-BASEBTS-BASE-FIG-223"><summary>Base Figure 223 · Telemetry Controller-Initiated Log Page</summary>
<!-- claim:BASEBTS-BASE-FIG-223-CLAIM -->
<p>Figure 223, "Telemetry Controller-Initiated Log Page": For 08h, TCS is byte 381 and TCDA/TCDGN are 382/383. TCDGN increments as the final update step; reread the header after collection. Interpret TCDA=0 using 2.4's no-update-since-acknowledgement meaning.</p><details class="source-note"><summary>Sources: Base 2.4 §5.2.13.1.9</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.9, Figure 223, printed pages 236-237, PDF pages 262-263</p></details>

</details>
<!-- figure-table:BASEBTS-BASE-FIG-780 -->
<details class="field-note" id="figure-BASEBTS-BASE-FIG-780"><summary>Base Figure 780 · Telemetry Log Example - All Data Areas Populated</summary>
<!-- claim:BASEBTS-BASE-FIG-780-CLAIM -->
<p>Figure 780, "Telemetry Log Example - All Data Areas Populated": Areas ending at 65/1000/30000 share prefixes; Area 3 includes Areas 1 and 2, so do not sum their lengths.</p><details class="source-note"><summary>Sources: Base 2.4 §8.1.30</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §8.1.30, Figure 780, printed pages 736, PDF pages 762</p></details>

</details>
<!-- figure-table:BASEBTS-BASE-FIG-781 -->
<details class="field-note" id="figure-BASEBTS-BASE-FIG-781"><summary>Base Figure 781 · Telemetry Log Example - Data Area 2 Populated</summary>
<!-- claim:BASEBTS-BASE-FIG-781-CLAIM -->
<p>Figure 781, "Telemetry Log Example - Data Area 2 Populated": Endpoints 0/1000/1000 mean empty Area 1, populated Area 2, and no additional Area 3 data; the Area 3 view still covers the same blocks as Area 2.</p><details class="source-note"><summary>Sources: Base 2.4 §8.1.30</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §8.1.30, Figure 781, printed pages 737, PDF pages 763</p></details>

</details>
<!-- figure-table:BASEBTS-BASE-FIG-338 -->
<details class="field-note" id="figure-BASEBTS-BASE-FIG-338"><summary>Base Figure 338 · Identify - Identify Controller Data Structure, I/O Command Set Independent</summary>
<!-- claim:BASEBTS-BASE-FIG-338-CLAIM -->
<p>Figure 338, "Identify - Identify Controller Data Structure, I/O Command Set Independent": Read the fields only this report's fields: BPCAP byte 102, LPA byte 261, SANICAP bytes 328–331, and MDS in CTRATT. Check methods, VERS/NVERS, SPRRS, NDI, and NODMMAS separately.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>BPCAP</dt><dd>Boot Partition Capabilities; identifies the supported combination of Set Features and RPMB protection.</dd></div><div><dt>I/O</dt><dd>Input/Output, the class of data operations performed on a namespace.</dd></div><div><dt>MDS</dt><dd>Multiple Domain Subsystem, the capability bit indicating whether an NVM subsystem contains multiple domains.</dd></div><div><dt>NDI</dt><dd>No-Deallocate Inhibited; advertises whether the controller inhibits NDAS.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §5.2.14.2.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.14.2.1, Figure 338, printed pages 340-382, PDF pages 366-408</p></details>

</details>
<!-- figure-table:BASEBTS-BASE-FIG-491 -->
<details class="field-note" id="figure-BASEBTS-BASE-FIG-491"><summary>Base Figure 491 · Host Behavior Support - Data Structure</summary>
<!-- claim:BASEBTS-BASE-FIG-491-CLAIM -->
<p>Figure 491, "Host Behavior Support - Data Structure": ETDAS=1 at Host Behavior Support byte 1 declares host Area 4 support; controller DA4S is still required.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>ETDAS</dt><dd>Extended Telemetry Data Area 4 Supported; the host's Area 4 declaration in Host Behavior Support.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §5.2.30.1.15</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.15, Figure 491, printed pages 476-477, PDF pages 502-503</p></details>

</details>
</details>
</section>
<section class="lesson" id="module-telemetry-capture"><h2 id="heading-telemetry-capture"><span class="section-number">04</span> Snapshot creation, chunked reads, and acknowledgement</h2>
<p>Separate creating 07h data from subsequent reads; the controller decides 08h capture timing. For both, verify generation and distinguish event acknowledgement from payload deletion.</p>
<figure><figcaption><strong>Keep segmented reads on one snapshot</strong></figcaption><ol class="flow-steps"><li>Read the header and save its generation number.</li><li>Read the data in segments from the same snapshot.</li><li>Read the header again and compare generation numbers.</li><li>Treat the segments as one snapshot only when the generations match.</li></ol><figcaption>The generation number identifies a data version; creating a snapshot and reading an existing snapshot are different operations.</figcaption></figure>

<details class="technical-note"><summary>Mechanism and applicable conditions</summary>
<!-- claim:BASEBTS-TEL-CREATE -->
<p>CTHID for LID 07h is CDW10 bit 8: one requests a new capture and zero does not update that snapshot. MCDA occupies bits 11:9 and applies only when MCDAS=1 and CTHID=1; 001b through 100b request creation through Areas 1 through 4, while 000b lets the controller decide. MCDAS comes from the LID Specific Parameter in Supported Log Pages.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>CTHID</dt><dd>Create Telemetry Host-Initiated Data; the 07h capture request, cleared for subsequent reads of that snapshot.</dd></div><div><dt>MCDAS</dt><dd>Maximum Created Data Area Supported; bit 0 of the 07h LID Specific Parameter, advertising MCDA support.</dd></div><div><dt>MCDA</dt><dd>Maximum Created Data Area; selects the largest area to create when supported and capture is requested.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §5.2.13.1.8</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.8, printed pages 232-235, PDF pages 258-261</p></details>
<!-- claim:BASEBTS-TEL-CONSISTENCY -->
<p>The host records the header generation, collects chunks with RAE=1, and rereads the header; a changed generation calls for rereading. For 08h it also checks that another reader has not cleared TCDA, then acknowledges completion by reading any portion with RAE=0. Generation is eight bits and wraps from FFh to 0h.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>portion</dt><dd>A contiguous portion sent in one firmware-download transfer.</dd></div><div><dt>Host</dt><dd>The system running the operating system and issuing NVMe commands.</dd></div><div><dt>TCDA</dt><dd>Telemetry Controller-Initiated Data Available; in 2.4, indicates an update since the last RAE=0 acknowledgement.</dd></div><div><dt>RAE</dt><dd>Retain Asynchronous Event; use one during Telemetry collection and zero to acknowledge completion.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §8.1.30</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §8.1.30, printed pages 734-735, PDF pages 760-761</p></details>
<!-- claim:BASEBTS-TEL-TCDA -->
<p>In Base 2.4, TCDA=0 means no update since the last successful RAE=0 read. The header is readable before the first capture; after a capture, both the header and current saved internal state are returned even with TCDA=0. The older interpretation that zero means header-only must not be carried into 2.4.</p><details class="source-note"><summary>Sources: Base 2.4 §5.2.13.1.9</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.9, printed pages 237, PDF pages 263</p></details>
<!-- claim:BASEBTS-TEL-PERSIST -->
<p>The 07h snapshot stays unchanged until another CTHID=1 request, Firmware Commit, or power-on reset. For 08h, Areas 1–3 persist across all resets and Area 4 may persist across Controller Level Resets; TCDA and TCDGN persist across power cycles and resets.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>TCDGN</dt><dd>Telemetry Controller-Initiated Data Generation Number; an eight-bit generation incremented at the end of an update.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §5.2.13.1.8-5.2.13.1.9</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.8-5.2.13.1.9, printed pages 233,235,237, PDF pages 259,261,263</p></details>
<!-- claim:BASEBTS-TEL-EVENT -->
<p>The host enables Telemetry Log Notices with TLN bit 10 of FID 0Bh. The controller reports a Notice-type Telemetry Log Changed AER; TCDA in 07h/08h also exposes an update.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>AER</dt><dd>Advanced Error Reporting, the PCIe capability for classifying, masking, and logging link or transaction errors.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §8.1.30; 5.2.30.1.6</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §8.1.30; 5.2.30.1.6, printed pages 734-735,466-468, PDF pages 760-761,492-494</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">Item</th><th scope="col">Role or distinction</th><th scope="col">Conditions</th></tr></thead><tbody><tr><td>CTHID=1</td><td>Triggers a new 07h capture</td><td>Do not create again for subsequent chunks</td></tr><tr><td>MCDA</td><td>Limits the areas created</td><td>Check MCDAS first</td></tr><tr><td>RAE=1</td><td>Retains the event</td><td>Does not exclude another reader</td></tr><tr><td>TCDA=0</td><td>No update since acknowledgement</td><td>In 2.4 it does not mean payload disappearance</td></tr></tbody></table></div><dl class="term-note" aria-label="Terms in this passage"><div><dt>CTHID</dt><dd>Create Telemetry Host-Initiated Data; the 07h capture request, cleared for subsequent reads of that snapshot.</dd></div><div><dt>MCDAS</dt><dd>Maximum Created Data Area Supported; bit 0 of the 07h LID Specific Parameter, advertising MCDA support.</dd></div><div><dt>MCDA</dt><dd>Maximum Created Data Area; selects the largest area to create when supported and capture is requested.</dd></div><div><dt>TCDA</dt><dd>Telemetry Controller-Initiated Data Available; in 2.4, indicates an update since the last RAE=0 acknowledgement.</dd></div><div><dt>RAE</dt><dd>Retain Asynchronous Event; use one during Telemetry collection and zero to acknowledge completion.</dd></div></dl>
<aside class="worked-example"><h3>Example</h3><p>If generation is 2Ah before reading and 2Bh afterward, the chunks cannot be accepted as one consistent capture. Even if it remains 2Ah, an 08h collection must consider the race where another host clears TCDA to zero.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>Host</dt><dd>The system running the operating system and issuing NVMe commands.</dd></div></dl></aside>
<details class="technical-note"><summary>Fields and data structures in more depth</summary>
<!-- figure-table:BASEBTS-BASE-FIG-220 -->
<details class="field-note" id="figure-BASEBTS-BASE-FIG-220"><summary>Base Figure 220 · Telemetry Host-Initiated Log Specific Parameter Field</summary>
<!-- claim:BASEBTS-BASE-FIG-220-CLAIM -->
<p>Figure 220, "Telemetry Host-Initiated Log Specific Parameter Field": CTHID occupies CDW10 bit 8 and MCDA bits 11:9. Apply MCDA only with MCDAS=1 and CTHID=1; subsequent reads of that snapshot use CTHID=0.</p><details class="source-note"><summary>Sources: Base 2.4 §5.2.13.1.8</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.8, Figure 220, printed pages 232-233, PDF pages 258-259</p></details>

</details>
<!-- figure-table:BASEBTS-BASE-FIG-222 -->
<details class="field-note" id="figure-BASEBTS-BASE-FIG-222"><summary>Base Figure 222 · Telemetry Host-Initiated Log Page - LID Specific Parameter Field</summary>
<!-- claim:BASEBTS-BASE-FIG-222-CLAIM -->
<p>Figure 222, "Telemetry Host-Initiated Log Page - LID Specific Parameter Field": LID Specific Parameter bit 0 is MCDAS. It advertises MCDA support, not which area has already been created.</p><details class="source-note"><summary>Sources: Base 2.4 §5.2.13.1.8</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.8, Figure 222, printed pages 235, PDF pages 261</p></details>

</details>
<!-- figure-table:BASEBTS-BASE-FIG-151 -->
<details class="field-note" id="figure-BASEBTS-BASE-FIG-151"><summary>Base Figure 151 · Asynchronous Event Request - Completion Queue Entry Dword 0</summary>
<!-- claim:BASEBTS-BASE-FIG-151-CLAIM -->
<p>Figure 151, "Asynchronous Event Request - Completion Queue Entry Dword 0": CQE DW0[23:16] is LID, [15:8] AEI, and [2:0] AET. Sanitize uses LID 81h/AET 110b; Telemetry uses the Notice type.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>Dword</dt><dd>Double word: 32 bits, or 4 bytes.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §5.2.2.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.2.1, Figure 151, printed pages 184-185, PDF pages 210-211</p></details>

</details>
<!-- figure-table:BASEBTS-BASE-FIG-152 -->
<details class="field-note" id="figure-BASEBTS-BASE-FIG-152"><summary>Base Figure 152 · Asynchronous Event Request - Completion Queue Entry Dword 1</summary>
<!-- claim:BASEBTS-BASE-FIG-152-CLAIM -->
<p>Figure 152, "Asynchronous Event Request - Completion Queue Entry Dword 1": AER DW1 is the event-specific parameter. Sanitize uses zero for a subsystem and NSID for a namespace; it is not progress.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>namespace</dt><dd>Namespace, a formatted quantity of non-volatile memory accessed by a host through a controller.</dd></div><div><dt>NSID</dt><dd>Namespace Identifier, a controller-visible numeric handle for a namespace; the identifier is not the namespace object itself.</dd></div><div><dt>AER</dt><dd>Advanced Error Reporting, the PCIe capability for classifying, masking, and logging link or transaction errors.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §5.2.2.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.2.1, Figure 152, printed pages 185, PDF pages 211</p></details>

</details>
<!-- figure-table:BASEBTS-BASE-FIG-155 -->
<details class="field-note" id="figure-BASEBTS-BASE-FIG-155"><summary>Base Figure 155 · Asynchronous Event Information - Notice</summary>
<!-- claim:BASEBTS-BASE-FIG-155-CLAIM -->
<p>Figure 155, "Asynchronous Event Information - Notice": Use the Telemetry Log Changed Notice 部分內容: find 08h from the event and read the log; the event does not contain the diagnostic payload.</p><details class="source-note"><summary>Sources: Base 2.4 §5.2.2.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.2.1, Figure 155, printed pages 186-189, PDF pages 212-215</p></details>

</details>
<!-- figure-table:BASEBTS-BASE-FIG-204 -->
<details class="field-note" id="figure-BASEBTS-BASE-FIG-204"><summary>Base Figure 204 · Get Log Page - Command Dword 10</summary>
<!-- claim:BASEBTS-BASE-FIG-204-CLAIM -->
<p>Figure 204, "Get Log Page - Command Dword 10": CDW10[7:0]=LID, [14:8]=LSP, [15]=RAE, and [31:16]=NUMDL. LID determines whether LSP means Boot BPID or Telemetry capture controls.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>NUMDL</dt><dd>Number of Dwords Lower, the low 16 bits of Get Log Page NUMD.</dd></div><div><dt>LSP</dt><dd>Log Specific Field, a command selector whose meaning is defined by the selected log page.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §5.2.13</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13, Figure 204, printed pages 213, PDF pages 239</p></details>

</details>
<!-- figure-table:BASEBTS-BASE-FIG-210 -->
<details class="field-note" id="figure-BASEBTS-BASE-FIG-210"><summary>Base Figure 210 · Supported Log Pages Log Page</summary>
<!-- claim:BASEBTS-BASE-FIG-210-CLAIM -->
<p>Figure 210, "Supported Log Pages Log Page": Supported Log Pages provides a descriptor per LID; the 07h descriptor is the lookup point for MCDAS.</p><details class="source-note"><summary>Sources: Base 2.4 §5.2.13.1.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.1, Figure 210, printed pages 217, PDF pages 243</p></details>

</details>
<!-- figure-table:BASEBTS-BASE-FIG-211 -->
<details class="field-note" id="figure-BASEBTS-BASE-FIG-211"><summary>Base Figure 211 · LID Supported and Effects Data Structure</summary>
<!-- claim:BASEBTS-BASE-FIG-211-CLAIM -->
<p>Figure 211, "LID Supported and Effects Data Structure": Check LSUPP before reading the fields that LID's specific parameter. MCDAS bit 0 belongs to this parameter, not to CTHID.</p><details class="source-note"><summary>Sources: Base 2.4 §5.2.13.1.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.1, Figure 211, printed pages 217-218, PDF pages 243-244</p></details>

</details>
<!-- figure-table:BASEBTS-BASE-FIG-474 -->
<details class="field-note" id="figure-BASEBTS-BASE-FIG-474"><summary>Base Figure 474 · Asynchronous Event Configuration - Command Dword 11</summary>
<!-- claim:BASEBTS-BASE-FIG-474-CLAIM -->
<p>Figure 474, "Asynchronous Event Configuration - Command Dword 11": Use TLN bit 10: when TCDA changes from 0h to 1h with TLN enabled, Telemetry Log Changed is reported. This table belongs to 5.2.30.1.6.</p><details class="source-note"><summary>Sources: Base 2.4 §5.2.30.1.6</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.6, Figure 474, printed pages 466-468, PDF pages 492-494</p></details>

</details>
</details>
</section>
<section class="lesson" id="module-sanitize-scope"><h2 id="heading-sanitize-scope"><span class="section-number">05</span> Define the sanitization target first</h2>
<p>Sanitize scope is not simply everything on a disk. Classify the target, data provenance, and whether it can contain user data; this also establishes its relationship with Boot and diagnostics.</p>
<details class="technical-note"><summary>Mechanism and applicable conditions</summary>
<!-- claim:BASEBTS-SAN-SCOPE -->
<p>Subsystem and namespace sanitize cover different data. Sanitizing every namespace individually is not equivalent to subsystem sanitize and does not thereby set subsystem GDE to one. Neither affects Boot Partitions or RPMB; logs/features containing user data may need modification.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>namespace</dt><dd>Namespace, a formatted quantity of non-volatile memory accessed by a host through a controller.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §8.1.27</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §8.1.27, printed pages 711-712, PDF pages 737-738</p></details>
<!-- claim:BASEBTS-SAN-MEDIA -->
<p>Sanitize covers the target's allocated/deallocated media and caches holding its user data. For subsystem sanitize, modification of CMB queue contents is implementation-defined while other CMB data is processed; HMB is unaffected. PMR must be disabled before subsystem sanitize starts and its data is within scope; namespace sanitize does not affect CMB, HMB, PMR, or PDA.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>CMB</dt><dd>Controller Memory Buffer, controller-provided memory in which selected queues or data structures may reside.</dd></div><div><dt>HMB</dt><dd>Host Memory Buffer, volatile memory ranges allocated by the host for exclusive controller use while enabled.</dd></div><div><dt>PMR</dt><dd>Persistent Memory Region, a controller-exposed memory region with persistence semantics.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §8.1.27</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §8.1.27, printed pages 711-712, PDF pages 737-738</p></details>
<!-- claim:BASEBTS-SAN-METHOD -->
<p>Block Erase uses media-specific erasure; Crypto Erase changes all relevant media encryption keys and processes unencrypted data with appropriate methods; Overwrite writes a pattern. PREQ/SPRRS govern purge requests and reporting. Crypto Erase must fail if old keys or unencrypted data requiring sanitization remain unaltered.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>PREQ</dt><dd>Purge Request; interpreted with SPRRS for purge request/reporting; its bit position differs between the Sanitize commands.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §8.1.27.2-8.1.27.3</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §8.1.27.2-8.1.27.3, printed pages 714-717, PDF pages 740-743</p></details>
<!-- claim:BASEBTS-NVM-VALUES -->
<p>After success, audit values are vendor-specific for Block Erase, indeterminate for Crypto Erase, and governed by the Base pattern mechanism for Overwrite. Reads of deallocated blocks instead follow Deallocated or Unwritten Logical Blocks rules; PI-checking reads without deallocation may encounter PI check errors.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>PI</dt><dd>Protection Information: Guard and tag fields used to check data and its associated information.</dd></div></dl><details class="source-note"><summary>Sources: NVM Command Set 1.3 §5.12</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §5.12, printed pages 174, PDF pages 174</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">Item</th><th scope="col">Role or distinction</th><th scope="col">Conditions</th></tr></thead><tbody><tr><td>Boot/RPMB</td><td>Unaffected by sanitize</td><td>Managed by their own mechanisms</td></tr><tr><td>Logs/features</td><td>Modify user data when necessary</td><td>Namespace media alone is insufficient</td></tr><tr><td>All namespace sanitizes</td><td>Complete work on each target</td><td>Does not thereby establish subsystem GDE</td></tr><tr><td>Crypto Erase</td><td>Changes keys and handles unencrypted data</td><td>Old key copies matter too</td></tr></tbody></table></div><dl class="term-note" aria-label="Terms in this passage"><div><dt>namespace</dt><dd>Namespace, a formatted quantity of non-volatile memory accessed by a host through a controller.</dd></div></dl>
<aside class="worked-example"><h3>Example</h3><p>Even after every namespace is sanitized, that fact does not prove subsystem-level data such as CMB has undergone subsystem sanitization. Conversely, successful subsystem sanitize does not update or erase the boot image in a Boot Partition.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>CMB</dt><dd>Controller Memory Buffer, controller-provided memory in which selected queues or data structures may reside.</dd></div></dl></aside>
<details class="technical-note"><summary>Fields and data structures in more depth</summary>
<!-- figure-table:BASEBTS-NVMCS-FIG-200 -->
<details class="field-note" id="figure-BASEBTS-NVMCS-FIG-200"><summary>NVM Figure 200 · Sanitize Operations - Admin Commands Allowed</summary>
<!-- claim:BASEBTS-NVMCS-FIG-200-CLAIM -->
<p>Figure 200, "Sanitize Operations - Admin Commands Allowed": The NVM Command Set adds Error Information behavior during sanitize: return zero in LBA. Base Figure 200 is a different table and cannot be substituted.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>NVM</dt><dd>Non-Volatile Memory, memory that retains data without power.</dd></div></dl><details class="source-note"><summary>Sources: NVM Command Set 1.3 §5.12</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §5.12, Figure 200, printed pages 173, PDF pages 173</p></details>

</details>
<!-- figure-table:BASEBTS-NVMCS-FIG-201 -->
<details class="field-note" id="figure-BASEBTS-NVMCS-FIG-201"><summary>NVM Figure 201 · Sanitize Operation Types - User Data Values</summary>
<!-- claim:BASEBTS-NVMCS-FIG-201-CLAIM -->
<p>Figure 201, "Sanitize Operation Types - User Data Values": Audit values are vendor-specific, indeterminate, or governed by Overwrite for the three methods; deallocated-block reads follow separate rules.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §5.12</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §5.12, Figure 201, printed pages 174, PDF pages 174</p></details>

</details>
<!-- figure-table:BASEBTS-BASE-FIG-770 -->
<details class="field-note" id="figure-BASEBTS-BASE-FIG-770"><summary>Base Figure 770 · Sanitization Operation Scope Based on Sanitize Operation</summary>
<!-- claim:BASEBTS-BASE-FIG-770-CLAIM -->
<p>Figure 770, "Sanitization Operation Scope Based on Sanitize Operation": Evaluate both targets for each data class: Boot/RPMB stay unchanged, user-data locations are processed, and CMB/PMR/PDA differences cannot be summarized as all namespaces.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>PMR</dt><dd>Persistent Memory Region, a controller-exposed memory region with persistence semantics.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §8.1.27</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §8.1.27, Figure 770, printed pages 711-712, PDF pages 737-738</p></details>

</details>
<!-- figure-table:BASEBTS-BASE-FIG-771 -->
<details class="field-note" id="figure-BASEBTS-BASE-FIG-771"><summary>Base Figure 771 · Sanitize Operations - Overwrite Mechanism</summary>
<!-- claim:BASEBTS-BASE-FIG-771-CLAIM -->
<p>Figure 771, "Sanitize Operations - Overwrite Mechanism": Use total-pass parity to determine whether the first pass is inverted, then invert between passes; PI bytes follow FFh/00h rules too. OVRPAT alone is insufficient.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>PI</dt><dd>Protection Information: Guard and tag fields used to check data and its associated information.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §8.1.27.3</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §8.1.27.3, Figure 771, printed pages 717, PDF pages 743</p></details>

</details>
<!-- figure-table:BASEBTS-BASE-FIG-201 -->
<details class="field-note" id="figure-BASEBTS-BASE-FIG-201"><summary>Base Figure 201 · Completion Queue Entry Dword 0 when Select is set to 11b</summary>
<!-- claim:BASEBTS-BASE-FIG-201-CLAIM -->
<p>Figure 201, "Completion Queue Entry Dword 0 when Select is set to 11b": For SEL=011b, bits 2/1/0 report changeable/namespace-specific/saveable, not current BP0WPS or NODRM values.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>BP0WPS</dt><dd>Boot Partition 0 Write Protection State; bits 2:0 of FID 85h.</dd></div><div><dt>Dword</dt><dd>Double word: 32 bits, or 4 bytes.</dd></div><div><dt>NODRM</dt><dd>No-Deallocate Response Mode; FID 17h bit zero selects error or warning for inhibited NDAS.</dd></div><div><dt>SEL</dt><dd>Select, the Get Features field choosing current, default, saved, or supported-capabilities view.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §5.2.12.2</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.12.2, Figure 201, printed pages 212, PDF pages 238</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>NSSPEC</dt><dd>Namespace Specific, the capability bit indicating whether a Feature has per-namespace scope.</dd></div><div><dt>CHANG</dt><dd>Changeable, the capability bit indicating whether Set Features can modify the Feature value.</dd></div><div><dt>SVBL</dt><dd>Saveable, the supported-capabilities bit indicating whether a Feature can be saved.</dd></div></dl>
</details>
</details>
</section>
<section class="lesson" id="module-sanitize-command"><h2 id="heading-sanitize-command"><span class="section-number">06</span> Combining command parameters with capabilities</h2>
<p>Separate advertised capabilities, command requests, and Feature policy. Command acceptance, operation success, and satisfaction of no-deallocate are three outcomes requiring different evidence.</p>
<details class="technical-note"><summary>Mechanism and applicable conditions</summary>
<!-- claim:BASEBTS-SAN-COMMAND -->
<p>CDW10 contains SANACT[2:0], AUSE[3], OWPASS[7:4], OIPBP[8], NDAS[9], EMVS[10], and PREQ[11]; CDW11 contains OVRPAT. SANACT 001b selects Exit Failure Mode, 010b Block Erase, 011b Overwrite, 100b Crypto Erase, and 101b Exit Media Verification; other values are reserved.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>SANACT</dt><dd>Sanitize Action; selects the method, Exit Failure Mode, or Exit Media Verification.</dd></div><div><dt>AUSE</dt><dd>Allow Unrestricted Sanitize Exit; selects whether failure can be exited without a successful retry.</dd></div><div><dt>EMVS</dt><dd>Enter Media Verification State; requests verification after successful processing, subject to method and capability restrictions.</dd></div><div><dt>NDAS</dt><dd>No-Deallocate After Sanitize; a command request interpreted with SANICAP.NDI and NODRM.</dd></div><div><dt>PREQ</dt><dd>Purge Request; interpreted with SPRRS for purge request/reporting; its bit position differs between the Sanitize commands.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §5.2.26</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.26, printed pages 448-451, PDF pages 474-477</p></details>
<!-- claim:BASEBTS-SAN-NAMESPACE -->
<p>The Namespace Sanitize command has the following layout: SANACT permits only 001b, 100b, and 101b; AUSE is bit 3, PREQ bit 4, and EMVS bit 10. There are no Overwrite/NDAS fields, so subsystem Sanitize CDW10 cannot be copied unchanged.</p><details class="source-note"><summary>Sources: Base 2.4 §8.1.27.1; 5.2.27</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §8.1.27.1; 5.2.27, printed pages 713,453, PDF pages 739,479</p></details>
<!-- claim:BASEBTS-SAN-NDAS -->
<p>NDAS requests retained allocation for this command; NDI indicates inhibition of that request. With NDAS=1 and NDI=1, NODRM=0 in FID 17h rejects the command with Invalid Field in Command, while NODRM=1 permits processing and reports unexpected deallocation as SOS=100b after success. NODMMAS=10b separately describes additional media modification when applicable.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>NODRM</dt><dd>No-Deallocate Response Mode; FID 17h bit zero selects error or warning for inhibited NDAS.</dd></div><div><dt>NDI</dt><dd>No-Deallocate Inhibited; advertises whether the controller inhibits NDAS.</dd></div><div><dt>SOS</dt><dd>Sanitize Operation Status; SSTAT bits 2:0, interpreted separately from the current SANS state.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §5.2.30.1.16; 8.1.27.2-8.1.27.3</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.16; 8.1.27.2-8.1.27.3, printed pages 477-478,715-719, PDF pages 503-504,741-745</p></details>
<!-- claim:BASEBTS-SAN-EMVS -->
<p>Subsystem sanitize with EMVS=1 requires VERS=1, Block Erase or Crypto Erase, and NDAS=0; combining it with Overwrite or NDAS=1 is rejected with Invalid Field in Command. SANACT=101b applies only in Media Verification and starts subsequent deallocation rather than a new sanitize operation.</p><details class="source-note"><summary>Sources: Base 2.4 §5.2.26</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.26, printed pages 449, PDF pages 475</p></details>
<!-- claim:BASEBTS-SAN-PREFLIGHT -->
<p>Enabled PMR, namespace write protection, a suspended controller, or pending firmware activation/reset may prevent subsystem sanitize. If the initiating command does not return Successful Completion, it starts no operation, changes no target Sanitize Status, and alters no user data; an anticipated operation failure should instead be reported through the subsequent log.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>PMR</dt><dd>Persistent Memory Region, a controller-exposed memory region with persistence semantics.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §5.2.26; 8.1.27.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.26; 8.1.27.1, printed pages 449-451,712-714, PDF pages 475-477,738-740</p></details>
<!-- claim:BASEBTS-SAN-OVERWRITE -->
<p>OWPASS=0h means 16 passes. With OIPBP=0, user data uses OVRPAT and PI bytes are FFh. With OIPBP=1 and an even pass count, the first pass uses the inverted pattern and PI=00h; with an odd count it starts with the original pattern and PI=FFh, then inverts on each subsequent pass.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>PI</dt><dd>Protection Information: Guard and tag fields used to check data and its associated information.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §5.2.26; 8.1.27.3</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.26; 8.1.27.3, printed pages 451,717, PDF pages 477,743</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">Item</th><th scope="col">Role or distinction</th><th scope="col">Conditions</th></tr></thead><tbody><tr><td>NDAS=1, NDI=0</td><td>Successful sanitize must not deallocate</td><td>Other validity conditions still apply</td></tr><tr><td>NDAS=1, NDI=1, NODRM=0</td><td>Command rejected</td><td>Invalid Field in Command</td></tr><tr><td>NDAS=1, NDI=1, NODRM=1</td><td>Processing permitted</td><td>Success can report SOS=100b</td></tr><tr><td>EMVS=1</td><td>Subsystem requires VERS=1</td><td>Block/Crypto + NDAS=0</td></tr></tbody></table></div><dl class="term-note" aria-label="Terms in this passage"><div><dt>NODRM</dt><dd>No-Deallocate Response Mode; FID 17h bit zero selects error or warning for inhibited NDAS.</dd></div><div><dt>EMVS</dt><dd>Enter Media Verification State; requests verification after successful processing, subject to method and capability restrictions.</dd></div><div><dt>NDAS</dt><dd>No-Deallocate After Sanitize; a command request interpreted with SANICAP.NDI and NODRM.</dd></div><div><dt>NDI</dt><dd>No-Deallocate Inhibited; advertises whether the controller inhibits NDAS.</dd></div><div><dt>SOS</dt><dd>Sanitize Operation Status; SSTAT bits 2:0, interpreted separately from the current SANS state.</dd></div></dl>
<aside class="worked-example"><h3>Example</h3><p>SANACT=010b, AUSE=0, EMVS=1, NDAS=0, and PREQ=0 encode CDW10=0402h. It applies only with VERS/Block Erase support and other preconditions satisfied. Separately, OWPASS=0h means 16 passes, not skipping overwrite.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>SANACT</dt><dd>Sanitize Action; selects the method, Exit Failure Mode, or Exit Media Verification.</dd></div><div><dt>AUSE</dt><dd>Allow Unrestricted Sanitize Exit; selects whether failure can be exited without a successful retry.</dd></div><div><dt>PREQ</dt><dd>Purge Request; interpreted with SPRRS for purge request/reporting; its bit position differs between the Sanitize commands.</dd></div></dl></aside>
<details class="technical-note"><summary>Fields and data structures in more depth</summary>
<!-- figure-table:BASEBTS-BASE-FIG-451 -->
<details class="field-note" id="figure-BASEBTS-BASE-FIG-451"><summary>Base Figure 451 · Sanitize - Command Dword 10</summary>
<!-- claim:BASEBTS-BASE-FIG-451-CLAIM -->
<p>Figure 451, "Sanitize - Command Dword 10": Select the action with SANACT before reading the fields method-dependent bits. OWPASS=0 means 16, and EMVS cannot combine with Overwrite/NDAS=1. PREQ bit 11 differs from the namespace command.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>Dword</dt><dd>Double word: 32 bits, or 4 bytes.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §5.2.26</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.26, Figure 451, printed pages 450-451, PDF pages 476-477</p></details>

</details>
<!-- figure-table:BASEBTS-BASE-FIG-452 -->
<details class="field-note" id="figure-BASEBTS-BASE-FIG-452"><summary>Base Figure 452 · Sanitize - Command Dword 11</summary>
<!-- claim:BASEBTS-BASE-FIG-452-CLAIM -->
<p>Figure 452, "Sanitize - Command Dword 11": The 32-bit OVRPAT in CDW11 applies only to Overwrite. Combine it with OIPBP and pass parity to derive each pass's pattern.</p><details class="source-note"><summary>Sources: Base 2.4 §5.2.26</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.26, Figure 452, printed pages 451, PDF pages 477</p></details>

</details>
<!-- figure-table:BASEBTS-BASE-FIG-453 -->
<details class="field-note" id="figure-BASEBTS-BASE-FIG-453"><summary>Base Figure 453 · Sanitize - Command Specific Status Values</summary>
<!-- claim:BASEBTS-BASE-FIG-453-CLAIM -->
<p>Figure 453, "Sanitize - Command Specific Status Values": These are command-specific failures of the initiating command. Record them separately from later background-operation Sanitize Failed/SOS results.</p><details class="source-note"><summary>Sources: Base 2.4 §5.2.26</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.26, Figure 453, printed pages 451, PDF pages 477</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>PMR</dt><dd>Persistent Memory Region, a controller-exposed memory region with persistence semantics.</dd></div></dl>
</details>
<!-- figure-table:BASEBTS-BASE-FIG-492 -->
<details class="field-note" id="figure-BASEBTS-BASE-FIG-492"><summary>Base Figure 492 · Sanitize Config - Command Dword 11</summary>
<!-- claim:BASEBTS-BASE-FIG-492-CLAIM -->
<p>Figure 492, "Sanitize Config - Command Dword 11": FID 17h CDW11 bit 0 is NODRM. It selects error/warning response when NDI=1 and command NDAS=1; it is not a switch required for every sanitize.</p><details class="source-note"><summary>Sources: Base 2.4 §5.2.30.1.16</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.16, Figure 492, printed pages 477-478, PDF pages 503-504</p></details>

</details>
<!-- figure-table:BASEBTS-BASE-FIG-454 -->
<details class="field-note" id="figure-BASEBTS-BASE-FIG-454"><summary>Base Figure 454 · Sanitize Namespace - Command Dword 10</summary>
<!-- claim:BASEBTS-BASE-FIG-454-CLAIM -->
<p>Figure 454, "Sanitize Namespace - Command Dword 10": Namespace CDW10 offers Exit Failure/Crypto Erase/Exit Verification, with PREQ at bit 4 and EMVS at bit 10, and no NDAS or Overwrite parameters.</p><details class="source-note"><summary>Sources: Base 2.4 §5.2.27</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.27, Figure 454, printed pages 453, PDF pages 479</p></details>

</details>
</details>
</section>
<section class="lesson" id="module-sanitize-state"><h2 id="heading-sanitize-state"><span class="section-number">07</span> Background sanitize state and progress</h2>
<p>Start with the seven states in Figure 772 and attach transition conditions from Figures 773–779. Status describes results, state describes the current position, and events report transitions.</p>
<details class="technical-note"><summary>Mechanism and applicable conditions</summary>
<!-- claim:BASEBTS-SAN-BACKGROUND -->
<p>Sanitize runs in the background. Starting an operation updates LID 81h before completing its initiating command; the host uses the status log and events for subsequent progress. An active operation cannot be aborted and continues across reset/power cycle, although specified resets may cancel verification.</p><details class="source-note"><summary>Sources: Base 2.4 §5.2.26.1; 8.1.27.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.26.1; 8.1.27.1, printed pages 451,712-713, PDF pages 477,738-739</p></details>
<!-- claim:BASEBTS-SAN-STATE -->
<p>Each supported target has its own state machine. AUSE=0/1 selects Restricted/Unrestricted Processing, and failure enters the corresponding Failure state. Restricted Failure requires a restricted sanitize retry; Unrestricted Failure permits retry or Exit Failure Mode to Idle. Idle therefore does not necessarily mean the last sanitize succeeded.</p><details class="source-note"><summary>Sources: Base 2.4 §8.1.27.4</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §8.1.27.4, printed pages 719-730, PDF pages 745-756</p></details>
<!-- claim:BASEBTS-SAN-VERIFY-STATE -->
<p>Successful processing enters Media Verification when requested by EMVS and not canceled. Exit Media Verification, an applicable reset, or a composition change preventing verification moves the target to Post-Verification Deallocation. Success returns to Idle; failure follows the original AUSE into Restricted/Unrestricted Failure with FAILS=6h.</p><details class="source-note"><summary>Sources: Base 2.4 §8.1.27.4.6-8.1.27.4.7</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §8.1.27.4.6-8.1.27.4.7, printed pages 727-730, PDF pages 753-756</p></details>
<!-- claim:BASEBTS-SAN-STATUS -->
<p>For LID 81h, NSID=0h or FFFFFFFFh selects the subsystem and an allocated NSID selects a namespace. SSTAT includes SOS, OPC, GDE, MVCNCLD, NDE, and PRGD; SSI contains SANS/FAILS; SCDW10 records initiating parameters. MNSOIP reports the concurrent namespace-operation limit and STNSID identifies a namespace target. The log persists across power cycles/resets.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>MVCNCLD</dt><dd>Media Verification Canceled; records canceled verification and affects the transition after processing.</dd></div><div><dt>NSID</dt><dd>Namespace Identifier, a controller-visible numeric handle for a namespace; the identifier is not the namespace object itself.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §5.2.13.1.38</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.38, printed pages 313-319, PDF pages 339-345</p></details>
<!-- claim:BASEBTS-SAN-PROGRESS -->
<p>SPROG is raw/65536 and reports progress for Processing or Post-Verification Deallocation, resetting to zero on entry. It can be FFFFh in Media Verification while SOS still says Sanitizing, so it cannot alone prove completion. Time estimates distinguish method and additional media modification; FFFFFFFFh means no estimate is reported.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>SPROG</dt><dd>Sanitize Progress; raw/65536, indicating progress only for the currently measured phase.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §5.2.13.1.38; 8.1.27.3</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.38; 8.1.27.3, printed pages 314-319,718, PDF pages 340-345,744</p></details>
<!-- claim:BASEBTS-SAN-EVENT -->
<p>Sanitize AERs use AET=110b and LID=81h; AEI=01h/02h/03h means Completed, Completed With Unexpected Deallocation, or Entered Media Verification. DW1 EVNTSP is zero for the subsystem or the target NSID. Interpret the event together with the log: Completed does not automatically mean success.</p><details class="source-note"><summary>Sources: Base 2.4 §8.1.27.1; 8.1.27.4</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §8.1.27.1; 8.1.27.4, printed pages 712-713,720, PDF pages 738-739,746</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">Item</th><th scope="col">Role or distinction</th><th scope="col">Conditions</th></tr></thead><tbody><tr><td>Restricted Failure</td><td>Retry in restricted mode</td><td>Exit Failure Mode cannot escape it</td></tr><tr><td>Unrestricted Failure</td><td>Retry or Exit Failure Mode</td><td>Idle does not rewrite failure history</td></tr><tr><td>Media Verification</td><td>Processing succeeded</td><td>The operation is still Sanitizing</td></tr><tr><td>Post-Verification Deallocation</td><td>SPROG starts again at zero</td><td>Failure records FAILS=6h</td></tr></tbody></table></div><dl class="term-note" aria-label="Terms in this passage"><div><dt>SPROG</dt><dd>Sanitize Progress; raw/65536, indicating progress only for the currently measured phase.</dd></div></dl>
<aside class="worked-example"><h3>Example</h3><p>SPROG=8000h represents 50% of the currently measured phase. Media Verification uses SPROG=FFFFh while SOS can remain 010b; leaving verification for deallocation starts progress again at zero. This is not progress regression.</p></aside>
<details class="technical-note"><summary>Fields and data structures in more depth</summary>
<!-- figure-table:BASEBTS-BASE-FIG-312 -->
<details class="field-note" id="figure-BASEBTS-BASE-FIG-312"><summary>Base Figure 312 · Sanitize Status Log Page</summary>
<!-- claim:BASEBTS-BASE-FIG-312-CLAIM -->
<p>Figure 312, "Sanitize Status Log Page": The 512-byte log has SPROG[1:0], SSTAT[3:2], SCDW10[7:4], estimates[35:8], SSI[36], MNSOIP[43:40], and STNSID[47:44]. Select the target with NSID, then interpret SOS/SANS/FAILS and progress together.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>NSID</dt><dd>Namespace Identifier, a controller-visible numeric handle for a namespace; the identifier is not the namespace object itself.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §5.2.13.1.38</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.38, Figure 312, printed pages 314-319, PDF pages 340-345</p></details>

</details>
<!-- figure-table:BASEBTS-BASE-FIG-772 -->
<details class="field-note" id="figure-BASEBTS-BASE-FIG-772"><summary>Base Figure 772 · Sanitize Operation State Machine</summary>
<!-- claim:BASEBTS-BASE-FIG-772-CLAIM -->
<p>Figure 772, "Sanitize Operation State Machine": Seven states split into processing/failure paths through AUSE, use EMVS to reach verification, then return through deallocation. Interpret each edge with Figures 773–779.</p><details class="source-note"><summary>Sources: Base 2.4 §8.1.27.4</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §8.1.27.4, Figure 772, printed pages 720, PDF pages 746</p></details>

</details>
<!-- figure-table:BASEBTS-BASE-FIG-773 -->
<details class="field-note" id="figure-BASEBTS-BASE-FIG-773"><summary>Base Figure 773 · Idle State Transition Conditions</summary>
<!-- claim:BASEBTS-BASE-FIG-773-CLAIM -->
<p>Figure 773, "Idle State Transition Conditions": A1/B1 leave Idle for Restricted/Unrestricted Processing respectively. Entry clears SPROG and MVCNCLD; it does not mean the operation is complete.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>MVCNCLD</dt><dd>Media Verification Canceled; records canceled verification and affects the transition after processing.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §8.1.27.4.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §8.1.27.4.1, Figure 773, printed pages 721, PDF pages 747</p></details>

</details>
<!-- figure-table:BASEBTS-BASE-FIG-774 -->
<details class="field-note" id="figure-BASEBTS-BASE-FIG-774"><summary>Base Figure 774 · Restricted Processing State Transition Conditions</summary>
<!-- claim:BASEBTS-BASE-FIG-774-CLAIM -->
<p>Figure 774, "Restricted Processing State Transition Conditions": Restricted Processing succeeds through C1 to Idle or F1 to Verification depending on EMVS/MVCNCLD; D1 reports processing failure.</p><details class="source-note"><summary>Sources: Base 2.4 §8.1.27.4.2</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §8.1.27.4.2, Figure 774, printed pages 722, PDF pages 748</p></details>

</details>
<!-- figure-table:BASEBTS-BASE-FIG-775 -->
<details class="field-note" id="figure-BASEBTS-BASE-FIG-775"><summary>Base Figure 775 · Restricted Failure State Transition Conditions</summary>
<!-- claim:BASEBTS-BASE-FIG-775-CLAIM -->
<p>Figure 775, "Restricted Failure State Transition Conditions": Restricted Failure recovers through A2 into Restricted Processing; Exit Failure Mode and AUSE=1 cannot substitute for a successful restricted retry.</p><details class="source-note"><summary>Sources: Base 2.4 §8.1.27.4.3</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §8.1.27.4.3, Figure 775, printed pages 724, PDF pages 750</p></details>

</details>
<!-- figure-table:BASEBTS-BASE-FIG-776 -->
<details class="field-note" id="figure-BASEBTS-BASE-FIG-776"><summary>Base Figure 776 · Unrestricted Processing State Transition Conditions</summary>
<!-- claim:BASEBTS-BASE-FIG-776-CLAIM -->
<p>Figure 776, "Unrestricted Processing State Transition Conditions": C2/D2/F2 from Unrestricted Processing mean successful Idle return, failure, or entry into Verification; unrestricted does not mean ordinary I/O is unrestricted.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>I/O</dt><dd>Input/Output, the class of data operations performed on a namespace.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §8.1.27.4.4</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §8.1.27.4.4, Figure 776, printed pages 725, PDF pages 751</p></details>

</details>
<!-- figure-table:BASEBTS-BASE-FIG-777 -->
<details class="field-note" id="figure-BASEBTS-BASE-FIG-777"><summary>Base Figure 777 · Unrestricted Failure State Transition Conditions</summary>
<!-- claim:BASEBTS-BASE-FIG-777-CLAIM -->
<p>Figure 777, "Unrestricted Failure State Transition Conditions": Unrestricted Failure permits A3 restricted retry, B2 unrestricted retry, or E Exit Failure Mode to Idle; E is not proof of successful sanitization.</p><details class="source-note"><summary>Sources: Base 2.4 §8.1.27.4.5</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §8.1.27.4.5, Figure 777, printed pages 727, PDF pages 753</p></details>

</details>
<!-- figure-table:BASEBTS-BASE-FIG-778 -->
<details class="field-note" id="figure-BASEBTS-BASE-FIG-778"><summary>Base Figure 778 · Media Verification State Transition Conditions</summary>
<!-- claim:BASEBTS-BASE-FIG-778-CLAIM -->
<p>Figure 778, "Media Verification State Transition Conditions": G enters Post-Verification Deallocation on the exit action, specified resets, or a composition change preventing verification; check MVCNCLD for canceled verification.</p><details class="source-note"><summary>Sources: Base 2.4 §8.1.27.4.6</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §8.1.27.4.6, Figure 778, printed pages 728, PDF pages 754</p></details>

</details>
<!-- figure-table:BASEBTS-BASE-FIG-779 -->
<details class="field-note" id="figure-BASEBTS-BASE-FIG-779"><summary>Base Figure 779 · Post-Verification Deallocation state Transition Conditions</summary>
<!-- claim:BASEBTS-BASE-FIG-779-CLAIM -->
<p>Figure 779, "Post-Verification Deallocation state Transition Conditions": Successful deallocation takes H to Idle; failure follows original AUSE through I1/I2 to Failure, with FAILS=6h distinguishing it from processing failure.</p><details class="source-note"><summary>Sources: Base 2.4 §8.1.27.4.7</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §8.1.27.4.7, Figure 779, printed pages 729, PDF pages 755</p></details>

</details>
<!-- figure-table:BASEBTS-BASE-FIG-156 -->
<details class="field-note" id="figure-BASEBTS-BASE-FIG-156"><summary>Base Figure 156 · Asynchronous Event Information - I/O Command Specific Status</summary>
<!-- claim:BASEBTS-BASE-FIG-156-CLAIM -->
<p>Figure 156, "Asynchronous Event Information - I/O Command Specific Status": Read Sanitize AEI 01h/02h/03h with SOS/SANS. Entered Media Verification is not completion of the entire operation.</p><details class="source-note"><summary>Sources: Base 2.4 §5.2.2.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.2.1, Figure 156, printed pages 189-190, PDF pages 215-216</p></details>

</details>
</details>
</section>
<section class="lesson" id="module-sanitize-read"><h2 id="heading-sanitize-read"><span class="section-number">08</span> Restrictions and verification reads</h2>
<p>Evaluate the command allowlist and the NVM Read exception separately. Determine target/state, then PI checking and allocation; ordinary-read behavior cannot be applied unchanged to verification.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>NVM</dt><dd>Non-Volatile Memory, memory that retains data without power.</dd></div><div><dt>PI</dt><dd>Protection Information: Guard and tag fields used to check data and its associated information.</dd></div></dl>
<details class="technical-note"><summary>Mechanism and applicable conditions</summary>
<!-- claim:BASEBTS-SAN-RESTRICT -->
<p>During subsystem sanitize, Figure 144 identifies allowed Admin commands and log pages; Boot Partition is listed but Telemetry 07h/08h is not. Disallowed operations are restricted with Sanitize In Progress. Namespace sanitize instead uses Figures 145/146 and the target NSID. NVM Reads in Media Verification have a specific exception.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>NSID</dt><dd>Namespace Identifier, a controller-visible numeric handle for a namespace; the identifier is not the namespace object itself.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §8.1.27.5; 5.1.1-5.1.2</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §8.1.27.5; 5.1.1-5.1.2, printed pages 178-181,730-732, PDF pages 204-207,756-758</p></details>
<!-- claim:BASEBTS-SAN-POWER -->
<p>Starting sanitize updates the target log on controllers and suspends autonomous power-state management. Affected I/O/self-tests are aborted and relevant streams released according to the target; new firmware activation is prohibited while the operation is active. A subsystem operation also prevents PMR enablement and PDA access.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>I/O</dt><dd>Input/Output, the class of data operations performed on a namespace.</dd></div><div><dt>PMR</dt><dd>Persistent Memory Region, a controller-exposed memory region with persistence semantics.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §8.1.27.5</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §8.1.27.5, printed pages 730-732, PDF pages 756-758</p></details>
<!-- claim:BASEBTS-NVM-BRIDGE -->
<p>NVM 4.1.7 uses the Base Sanitize command; 5.12 adds permitted Admin behavior, post-sanitize data values, and Media Verification Reads. Error Information returns zero in LBA, while other fields containing user data remain subject to Base processing.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §4.1.7; 5.12</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §4.1.7; 5.12, printed pages 113,173-175, PDF pages 113,173-175</p></details>
<!-- claim:BASEBTS-NVM-VERIFY -->
<p>A Media Verification Read requests no PI checking: PRCHK=000b and STC=0. Readable allocated media returns its data while ignoring integrity errors when the media can be read, completing with Successful Media Verification Read unless another error aborts it. Unreadable allocated media produces Unrecovered Read Error. Requesting PI checking produces Invalid Field in Command.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>PRCHK</dt><dd>Protection Information Check; three bits request guard, application-tag, and reference-tag checking; verification reads use 000b.</dd></div><div><dt>STC</dt><dd>Storage Tag Check; here it selects storage-tag checking for NVM Reads and is zero for verification reads.</dd></div></dl><details class="source-note"><summary>Sources: NVM Command Set 1.3 §5.12.1</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §5.12.1, printed pages 174-175, PDF pages 174-175</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">Item</th><th scope="col">Role or distinction</th><th scope="col">Conditions</th></tr></thead><tbody><tr><td>PI checking requested</td><td>Invalid Field in Command</td><td>Not permitted for verification reads</td></tr><tr><td>Allocated media readable</td><td>Return media data</td><td>Integrity errors can be ignored when readable</td></tr><tr><td>Allocated media unreadable</td><td>Unrecovered Read Error</td><td>Do not invent data</td></tr><tr><td>Deallocated LBA</td><td>Use deallocated/unwritten rules</td><td>Not evidence of the old media pattern</td></tr></tbody></table></div>
<aside class="worked-example"><h3>Example</h3><p>A verification read with PRCHK=000b and STC=0, readable allocated LBAs, and no other abort cause completes as Successful Media Verification Read. Requesting PI checking changes the expected branch to Invalid Field in Command.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>PRCHK</dt><dd>Protection Information Check; three bits request guard, application-tag, and reference-tag checking; verification reads use 000b.</dd></div><div><dt>STC</dt><dd>Storage Tag Check; here it selects storage-tag checking for NVM Reads and is zero for verification reads.</dd></div></dl></aside>
<details class="technical-note"><summary>Fields and data structures in more depth</summary>
<!-- figure-table:BASEBTS-NVMCS-FIG-011 -->
<details class="field-note" id="figure-BASEBTS-NVMCS-FIG-011"><summary>NVM Figure 11 · Protection Information Field Definition</summary>
<!-- claim:BASEBTS-NVMCS-FIG-011-CLAIM -->
<p>Figure 11, "Protection Information Field Definition": PRACT governs PI handling; the three PRCHK bits request Guard/Application/Reference Tag checking. Media Verification explicitly requires PRCHK=000b.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>Protection Information</dt><dd>PI: protection fields containing a Guard and tags for checking data and its associated information.</dd></div><div><dt>Guard</dt><dd>The PI check-value field; the selected format determines its width and calculation.</dd></div></dl><details class="source-note"><summary>Sources: NVM Command Set 1.3 §2.1.5</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §2.1.5, Figure 11, printed pages 21-22, PDF pages 21-22</p></details>

</details>
<!-- figure-table:BASEBTS-NVMCS-FIG-012 -->
<details class="field-note" id="figure-BASEBTS-NVMCS-FIG-012"><summary>NVM Figure 12 · Storage Tag Check Definition</summary>
<!-- claim:BASEBTS-NVMCS-FIG-012-CLAIM -->
<p>Figure 12, "Storage Tag Check Definition": Here STC is Storage Tag Check, not Self-test Code from another report; verification Reads require STC=0.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §2.1.5</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §2.1.5, Figure 12, printed pages 22, PDF pages 22</p></details>

</details>
<!-- figure-table:BASEBTS-BASE-FIG-144 -->
<details class="field-note" id="figure-BASEBTS-BASE-FIG-144"><summary>Base Figure 144 · NVM Subsystem Sanitize Operations and Format NVM Command - Admin</summary>
<!-- claim:BASEBTS-BASE-FIG-144-CLAIM -->
<p>Figure 144, "NVM Subsystem Sanitize Operations and Format NVM Command - Admin": Read the Sanitize column's command allowlist and per-command restrictions. Boot is readable; Telemetry 07h/08h is not listed. Only common and memory-based command rows are used.</p><details class="source-note"><summary>Sources: Base 2.4 §5.1.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.1.1, Figure 144, printed pages 178-179, PDF pages 204-205</p></details>

</details>
<!-- figure-table:BASEBTS-BASE-FIG-145 -->
<details class="field-note" id="figure-BASEBTS-BASE-FIG-145"><summary>Base Figure 145 · Namespace Sanitize Operations - Admin Command Restrictions, All Controllers</summary>
<!-- claim:BASEBTS-BASE-FIG-145-CLAIM -->
<p>Figure 145, "Namespace Sanitize Operations - Admin Command Restrictions, All Controllers": This table applies to all controllers: for example, deletion of a namespace being sanitized and firmware updates are restricted. Establish the target relationship before choosing a status.</p><details class="source-note"><summary>Sources: Base 2.4 §5.1.2</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.1.2, Figure 145, printed pages 179-180, PDF pages 205-206</p></details>

</details>
<!-- figure-table:BASEBTS-BASE-FIG-146 -->
<details class="field-note" id="figure-BASEBTS-BASE-FIG-146"><summary>Base Figure 146 · Namespace Sanitize Operations - Admin Command Restrictions if Sanitizing</summary>
<!-- claim:BASEBTS-BASE-FIG-146-CLAIM -->
<p>Figure 146, "Namespace Sanitize Operations - Admin Command Restrictions if Sanitizing": This table adds restrictions for controllers with an attached namespace being sanitized. Do not conflate all-controller restrictions with attached-controller restrictions.</p><details class="source-note"><summary>Sources: Base 2.4 §5.1.2</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.1.2, Figure 146, printed pages 180-181, PDF pages 206-207</p></details>

</details>
<!-- figure-table:BASEBTS-BASE-FIG-311 -->
<details class="field-note" id="figure-BASEBTS-BASE-FIG-311"><summary>Base Figure 311 · Reservation Notification Log Page</summary>
<!-- claim:BASEBTS-BASE-FIG-311-CLAIM -->
<p>Figure 311, "Reservation Notification Log Page": This Reservation Notification structure reports notification counts/types and does not contain SPROG. The reference in 8.1.27.4.2 appears misplaced; use Figure 312 for progress.</p><details class="source-note"><summary>Sources: Base 2.4 §5.2.13.1.37</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.37, Figure 311, printed pages 313, PDF pages 339</p></details>

</details>
</details>
</section>
<section id="additional-details"><h2 id="further-mechanisms">Additional mechanisms and data formats</h2>
<!-- figure-table:BASEBTS-BASE-FIG-188 -->
<details class="field-note" id="figure-BASEBTS-BASE-FIG-188"><summary>Base Figure 188 · Firmware Commit - Completion Queue Entry Dword 0</summary>
<!-- claim:BASEBTS-BASE-FIG-188-CLAIM -->
<p>Figure 188, "Firmware Commit - Completion Queue Entry Dword 0": MUD supplies completion evidence for overlapping updates; the single-controller/endpoint image-sequence boundary still applies.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>Dword</dt><dd>Double word: 32 bits, or 4 bytes.</dd></div><div><dt>MUD</dt><dd>Multiple Update Detected, the completion bit indicating detection of overlapping firmware-update sequences.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §5.2.9.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.9.1, Figure 188, printed pages 204, PDF pages 230</p></details>

</details>
<!-- figure-table:BASEBTS-BASE-FIG-189 -->
<details class="field-note" id="figure-BASEBTS-BASE-FIG-189"><summary>Base Figure 189 · Firmware Commit - Command Specific Status Values</summary>
<!-- claim:BASEBTS-BASE-FIG-189-CLAIM -->
<p>Figure 189, "Firmware Commit - Command Specific Status Values": Boot Partition Write Prohibited points to protection state; Invalid Firmware Image points to image/sequence validation. Classify status before choosing a retry step.</p><details class="source-note"><summary>Sources: Base 2.4 §5.2.9.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.9.1, Figure 189, printed pages 204-205, PDF pages 230-231</p></details>

</details>
<!-- figure-table:BASEBTS-BASE-FIG-190 -->
<details class="field-note" id="figure-BASEBTS-BASE-FIG-190"><summary>Base Figure 190 · Firmware Image Download - Data Pointer</summary>
<!-- claim:BASEBTS-BASE-FIG-190-CLAIM -->
<p>Figure 190, "Firmware Image Download - Data Pointer": Download DPTR identifies the host buffer for this image portion, not the destination Boot Partition address.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>portion</dt><dd>A contiguous portion sent in one firmware-download transfer.</dd></div><div><dt>DPTR</dt><dd>Data Pointer, the SQE field identifying a command data buffer.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §5.2.10</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.10, Figure 190, printed pages 205, PDF pages 231</p></details>

</details>
<!-- figure-table:BASEBTS-BASE-FIG-191 -->
<details class="field-note" id="figure-BASEBTS-BASE-FIG-191"><summary>Base Figure 191 · Firmware Image Download - Command Dword 10</summary>
<!-- claim:BASEBTS-BASE-FIG-191-CLAIM -->
<p>Figure 191, "Firmware Image Download - Command Dword 10": NUMD is the portion's zero-based dword count: 512 bytes encodes as 127, with Download alignment/granularity requirements checked separately.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>NUMD</dt><dd>Number of Dwords, a zero-based transfer-dword count; actual bytes = (NUMD + 1) × 4.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §5.2.10</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.10, Figure 191, printed pages 205, PDF pages 231</p></details>

</details>
<!-- figure-table:BASEBTS-BASE-FIG-192 -->
<details class="field-note" id="figure-BASEBTS-BASE-FIG-192"><summary>Base Figure 192 · Firmware Image Download - Command Dword 11</summary>
<!-- claim:BASEBTS-BASE-FIG-192-CLAIM -->
<p>Figure 192, "Firmware Image Download - Command Dword 11": OFST is an image offset in dwords. Boot images are sent in order from the beginning; do not borrow other ordering assumptions for ordinary firmware portions.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>OFST</dt><dd>Offset, the dword-based image-relative offset in Firmware Image Download.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §5.2.10</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.10, Figure 192, printed pages 206, PDF pages 232</p></details>

</details>
<!-- figure-table:BASEBTS-BASE-FIG-193 -->
<details class="field-note" id="figure-BASEBTS-BASE-FIG-193"><summary>Base Figure 193 · Firmware Image Download - Command Specific Status Values</summary>
<!-- claim:BASEBTS-BASE-FIG-193-CLAIM -->
<p>Figure 193, "Firmware Image Download - Command Specific Status Values": Overlapping Range reports overlapping download portions; preserve each offset and length to reconstruct the offending range.</p><details class="source-note"><summary>Sources: Base 2.4 §5.2.10</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.10, Figure 193, printed pages 206, PDF pages 232</p></details>

</details>
<!-- figure-table:BASEBTS-BASE-FIG-198 -->
<details class="field-note" id="figure-BASEBTS-BASE-FIG-198"><summary>Base Figure 198 · Get Features - Command Dword 10</summary>
<!-- claim:BASEBTS-BASE-FIG-198-CLAIM -->
<p>Figure 198, "Get Features - Command Dword 10": Get Features uses FID for the feature and SEL for current/default/saved/capabilities. Do not confuse values for FID 85h/17h with their capabilities.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>SEL</dt><dd>Select, the Get Features field choosing current, default, saved, or supported-capabilities view.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §5.2.12</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.12, Figure 198, printed pages 209-210, PDF pages 235-236</p></details>

</details>
<!-- figure-table:BASEBTS-BASE-FIG-199 -->
<details class="field-note" id="figure-BASEBTS-BASE-FIG-199"><summary>Base Figure 199 · Get Features - Command Dword 14</summary>
<!-- claim:BASEBTS-BASE-FIG-199-CLAIM -->
<p>Figure 199, "Get Features - Command Dword 14": The CDW14 UUID Index belongs to the common Feature interface; these standard FIDs do not call for invented vendor-UUID mappings.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>UUID</dt><dd>Universally Unique Identifier, a 128-bit identifier whose association scope is defined by the containing structure.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §5.2.12</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.12, Figure 199, printed pages 210, PDF pages 236</p></details>

</details>
<!-- figure-table:BASEBTS-BASE-FIG-203 -->
<details class="field-note" id="figure-BASEBTS-BASE-FIG-203"><summary>Base Figure 203 · Get Log Page - Data Pointer</summary>
<!-- claim:BASEBTS-BASE-FIG-203-CLAIM -->
<p>Figure 203, "Get Log Page - Data Pointer": Get Log Page's data pointer identifies a receive buffer large enough for the encoded NUMD request.</p><details class="source-note"><summary>Sources: Base 2.4 §5.2.13</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13, Figure 203, printed pages 213, PDF pages 239</p></details>

</details>
<!-- figure-table:BASEBTS-BASE-FIG-205 -->
<details class="field-note" id="figure-BASEBTS-BASE-FIG-205"><summary>Base Figure 205 · Get Log Page - Command Dword 11</summary>
<!-- claim:BASEBTS-BASE-FIG-205-CLAIM -->
<p>Figure 205, "Get Log Page - Command Dword 11": NUMDU and NUMDL form the zero-based dword count; LSI is a separate log-specific selector, not LSP.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>NUMDL</dt><dd>Number of Dwords Lower, the low 16 bits of Get Log Page NUMD.</dd></div><div><dt>NUMDU</dt><dd>Number of Dwords Upper, the high 16 bits of Get Log Page NUMD.</dd></div><div><dt>LSI</dt><dd>Log Specific Identifier, an identifier whose meaning is defined by the selected log page.</dd></div><div><dt>LSP</dt><dd>Log Specific Field, a command selector whose meaning is defined by the selected log page.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §5.2.13</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13, Figure 205, printed pages 214, PDF pages 240</p></details>

</details>
<!-- figure-table:BASEBTS-BASE-FIG-206 -->
<details class="field-note" id="figure-BASEBTS-BASE-FIG-206"><summary>Base Figure 206 · Get Log Page - Command Dword 12</summary>
<!-- claim:BASEBTS-BASE-FIG-206-CLAIM -->
<p>Figure 206, "Get Log Page - Command Dword 12": The low 32 bits of LPO occupy CDW12; Telemetry byte offsets must align to 512-byte blocks.</p><details class="source-note"><summary>Sources: Base 2.4 §5.2.13</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13, Figure 206, printed pages 214, PDF pages 240</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>LPOL</dt><dd>Log Page Offset Lower, the low 32 bits of the Get Log Page byte offset.</dd></div></dl>
</details>
<!-- figure-table:BASEBTS-BASE-FIG-207 -->
<details class="field-note" id="figure-BASEBTS-BASE-FIG-207"><summary>Base Figure 207 · Get Log Page - Command Dword 13</summary>
<!-- claim:BASEBTS-BASE-FIG-207-CLAIM -->
<p>Figure 207, "Get Log Page - Command Dword 13": The high 32 bits of LPO occupy CDW13; do not truncate a large-log offset to 32 bits before computing it.</p><details class="source-note"><summary>Sources: Base 2.4 §5.2.13</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13, Figure 207, printed pages 214, PDF pages 240</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>LPOU</dt><dd>Log Page Offset Upper, the high 32 bits of the Get Log Page byte offset.</dd></div></dl>
</details>
<!-- figure-table:BASEBTS-BASE-FIG-208 -->
<details class="field-note" id="figure-BASEBTS-BASE-FIG-208"><summary>Base Figure 208 · Get Log Page - Command Dword 14</summary>
<!-- claim:BASEBTS-BASE-FIG-208-CLAIM -->
<p>Figure 208, "Get Log Page - Command Dword 14": CSI/OT/UUID Index in CDW14 provide common reading the fields context. Apply the LID's offset semantics rather than mistaking a byte offset for an index.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>CSI</dt><dd>I/O Command Set Identifier: selects an I/O command set; NVM uses 00h.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §5.2.13</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13, Figure 208, printed pages 214-215, PDF pages 240-241</p></details>

</details>
<!-- figure-table:BASEBTS-BASE-FIG-209 -->
<details class="field-note" id="figure-BASEBTS-BASE-FIG-209"><summary>Base Figure 209 · Get Log Page - Log Page Identifiers</summary>
<!-- claim:BASEBTS-BASE-FIG-209-CLAIM -->
<p>Figure 209, "Get Log Page - Log Page Identifiers": Use only the 07h, 08h, 15h, and 81h rows, connecting each ID to its section without extending into other logs.</p><details class="source-note"><summary>Sources: Base 2.4 §5.2.13</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13, Figure 209, printed pages 215-216, PDF pages 241-242</p></details>

</details>
<!-- figure-table:BASEBTS-BASE-FIG-464 -->
<details class="field-note" id="figure-BASEBTS-BASE-FIG-464"><summary>Base Figure 464 · Set Features - Command Dword 10</summary>
<!-- claim:BASEBTS-BASE-FIG-464-CLAIM -->
<p>Figure 464, "Set Features - Command Dword 10": Set Features FID selects the CDW11 interpretation. SV requests saving; successful setting alone does not prove persistence through power cycles.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>SV</dt><dd>Save, the Set Features bit requesting that the controller also save the configured value.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §5.2.30</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30, Figure 464, printed pages 457, PDF pages 483</p></details>

</details>
<!-- figure-table:BASEBTS-BASE-FIG-465 -->
<details class="field-note" id="figure-BASEBTS-BASE-FIG-465"><summary>Base Figure 465 · Set Features - Command Dword 14</summary>
<!-- claim:BASEBTS-BASE-FIG-465-CLAIM -->
<p>Figure 465, "Set Features - Command Dword 14": Interpret the Set UUID Index with feature identity; these standard FIDs do not expand into a vendor-feature protocol.</p><details class="source-note"><summary>Sources: Base 2.4 §5.2.30</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30, Figure 465, printed pages 457, PDF pages 483</p></details>

</details>
<!-- figure-table:BASEBTS-BASE-FIG-466 -->
<details class="field-note" id="figure-BASEBTS-BASE-FIG-466"><summary>Base Figure 466 · Set Features - Feature Identifiers</summary>
<!-- claim:BASEBTS-BASE-FIG-466-CLAIM -->
<p>Figure 466, "Set Features - Feature Identifiers": Use only rows/scopes for Boot protection, Sanitize Config, AEC, and Host Behavior Support. FID 17h is subsystem policy.</p><details class="source-note"><summary>Sources: Base 2.4 §5.2.30</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30, Figure 466, printed pages 457-459, PDF pages 483-485</p></details>

</details>
<!-- figure-table:BASEBTS-BASE-FIG-757 -->
<details class="field-note" id="figure-BASEBTS-BASE-FIG-757"><summary>Base Figure 757 · RPMB Request and Response Message Types</summary>
<!-- claim:BASEBTS-BASE-FIG-757-CLAIM -->
<p>Figure 757, "RPMB Request and Response Message Types": Track authenticated configuration read/write message types needed for Boot and pair each request with its expected response.</p><details class="source-note"><summary>Sources: Base 2.4 §8.1.24</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §8.1.24, Figure 757, printed pages 692-693, PDF pages 718-719</p></details>

</details>
<!-- figure-table:BASEBTS-BASE-FIG-758 -->
<details class="field-note" id="figure-BASEBTS-BASE-FIG-758"><summary>Base Figure 758 · RPMB Operation Result</summary>
<!-- claim:BASEBTS-BASE-FIG-758-CLAIM -->
<p>Figure 758, "RPMB Operation Result": Operation Result distinguishes success, authentication, counter, and other failures; transport-command completion does not itself prove successful RPMB writing.</p><details class="source-note"><summary>Sources: Base 2.4 §8.1.24</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §8.1.24, Figure 758, printed pages 693, PDF pages 719</p></details>

</details>
<!-- figure-table:BASEBTS-BASE-FIG-760 -->
<details class="field-note" id="figure-BASEBTS-BASE-FIG-760"><summary>Base Figure 760 · RPMB Data Frame</summary>
<!-- claim:BASEBTS-BASE-FIG-760-CLAIM -->
<p>Figure 760, "RPMB Data Frame": Message type, counter, nonce, result, and authentication provide different response-validation evidence in the frame; payload alone is insufficient.</p><details class="source-note"><summary>Sources: Base 2.4 §8.1.24</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §8.1.24, Figure 760, printed pages 694, PDF pages 720</p></details>

</details>
<!-- figure-table:BASEBTS-BASE-FIG-761 -->
<details class="field-note" id="figure-BASEBTS-BASE-FIG-761"><summary>Base Figure 761 · RPMB - Authentication Key Data Flow</summary>
<!-- claim:BASEBTS-BASE-FIG-761-CLAIM -->
<p>Figure 761, "RPMB - Authentication Key Data Flow": Authentication-key programming is prerequisite context for authenticated configuration; verify its result rather than equating key submission with success.</p><details class="source-note"><summary>Sources: Base 2.4 §8.1.24.2.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §8.1.24.2.1, Figure 761, printed pages 695-696, PDF pages 721-722</p></details>

</details>
<!-- figure-table:BASEBTS-BASE-FIG-762 -->
<details class="field-note" id="figure-BASEBTS-BASE-FIG-762"><summary>Base Figure 762 · RPMB - Read Write Counter Value Flow</summary>
<!-- claim:BASEBTS-BASE-FIG-762-CLAIM -->
<p>Figure 762, "RPMB - Read Write Counter Value Flow": Obtain and validate the write counter, use nonce/authentication to verify the response, then construct the protected configuration write.</p><details class="source-note"><summary>Sources: Base 2.4 §8.1.24.2.2</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §8.1.24.2.2, Figure 762, printed pages 696, PDF pages 722</p></details>

</details>
</section>
<section id="knowledge-check"><h2 id="review-questions">Check your understanding</h2>
<!-- qa:base-boot-telemetry-sanitize-boot-active -->
<details class="review-question" id="qa-base-boot-telemetry-sanitize-boot-active"><summary>1. Does writing a new boot image to a partition also change the active partition?</summary>
<div data-qa-answer="base-boot-telemetry-sanitize-boot-active"><p>Writing and selecting the active ID are separate actions. CA=110b writes the selected partition; after an optional readback, CA=111b selects the active ID. This separation allows checking the image before switching.</p></div>
<details class="source-note"><summary>Sources</summary>
<p>Source: NVME-BASE-2.4, Rev. 2.4, §8.1.3.2, printed pages 587-588, PDF pages 613-614</p>
<p>Source: NVME-BASE-2.4, Rev. 2.4, §8.1.3, printed pages 586, PDF pages 612</p>
</details></details>
<!-- qa:base-boot-telemetry-sanitize-boot-reset -->
<details class="review-question" id="qa-base-boot-telemetry-sanitize-boot-reset"><summary>2. Must a Controller Level Reset relock an unlocked Boot Partition?</summary>
<div data-qa-answer="base-boot-telemetry-sanitize-boot-reset"><p>First identify the controlling mechanism. The Set Features unlocked state survives this reset but a power cycle relocks it. With RPMB protection enabled, either event relocks it.</p></div>
<details class="source-note"><summary>Sources</summary>
<p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.39, printed pages 513-514, PDF pages 539-540</p>
<p>Source: NVME-BASE-2.4, Rev. 2.4, §8.1.3.3.1-8.1.3.3.3, printed pages 589-594, PDF pages 615-620</p>
</details></details>
<!-- qa:base-boot-telemetry-sanitize-telemetry-areas -->
<details class="review-question" id="qa-base-boot-telemetry-sanitize-telemetry-areas"><summary>3. If Area 1 Last Block is 3 and Area 2 Last Block is 7, which payload blocks belong to Area 2?</summary>
<div data-qa-answer="base-boot-telemetry-sanitize-telemetry-areas"><p>Area 2 contains blocks 1 through 7, totaling 7×512=3584 bytes, including Area 1 blocks 1 through 3. The header is block 0 and occupies another 512 bytes. Last Block is inclusive.</p></div>
<details class="source-note"><summary>Sources</summary>
<p>Source: NVME-BASE-2.4, Rev. 2.4, §8.1.30; 5.2.13.1.8-5.2.13.1.9, printed pages 232-237,733-737, PDF pages 258-263,759-763</p>
</details></details>
<!-- qa:base-boot-telemetry-sanitize-telemetry-generation -->
<details class="review-question" id="qa-base-boot-telemetry-sanitize-telemetry-generation"><summary>4. Why reread the Telemetry header after collecting its data in chunks?</summary>
<div data-qa-answer="base-boot-telemetry-sanitize-telemetry-generation"><p>A new snapshot generation may appear during collection. Rereading generation checks that the chunks still belong together; a change requires recollection. For controller-initiated data, also check TCDA to account for acknowledgement by another reader.</p></div>
<details class="source-note"><summary>Sources</summary>
<p>Source: NVME-BASE-2.4, Rev. 2.4, §8.1.30, printed pages 734-735, PDF pages 760-761</p>
<p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.9, printed pages 237, PDF pages 263</p>
</details></details>
<!-- qa:base-boot-telemetry-sanitize-sanitize-completion -->
<details class="review-question" id="qa-base-boot-telemetry-sanitize-sanitize-completion"><summary>5. Does Successful Completion of the Sanitize command mean sanitization has finished?</summary>
<div data-qa-answer="base-boot-telemetry-sanitize-sanitize-completion"><p>It indicates success of the initiating command; the background operation may still be running. Use the corresponding Sanitize Status to determine the operation state. SPROG and time estimates describe progress and do not replace the final status.</p></div>
<details class="source-note"><summary>Sources</summary>
<p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.26.1; 8.1.27.1, printed pages 451,712-713, PDF pages 477,738-739</p>
<p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.38, printed pages 313-319, PDF pages 339-345</p>
<p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.38; 8.1.27.3, printed pages 314-319,718, PDF pages 340-345,744</p>
</details></details>
<!-- qa:base-boot-telemetry-sanitize-sanitize-data -->
<details class="review-question" id="qa-base-boot-telemetry-sanitize-sanitize-data"><summary>6. Why is an all-zero readback not a universal success criterion for sanitization?</summary>
<div data-qa-answer="base-boot-telemetry-sanitize-sanitize-data"><p>Methods have different read-value rules, and deallocation selects another set of rules. Block Erase, Crypto Erase, and Overwrite do not share one expected pattern; Media Verification also has its own read semantics. Establish the operation state before interpreting data by method and block state.</p></div>
<details class="source-note"><summary>Sources</summary>
<p>Source: NVME-BASE-2.4, Rev. 2.4, §8.1.27.2-8.1.27.3, printed pages 714-717, PDF pages 740-743</p>
<p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §5.12, printed pages 174, PDF pages 174</p>
<p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §5.12.1, printed pages 174-175, PDF pages 174-175</p>
</details></details>
</section>
<footer class="reference-editions"><details class="source-note"><summary>Specification editions</summary><p>NVM Express Base Specification, Revision 2.4</p><p>NVM Express NVM Command Set Specification, Revision 1.3</p></details></footer>
</div>
