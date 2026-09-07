---
layout: post
read_time: true
show_date: true
title: "NVMe Base 2.4: Device Self-test, HMB, Doorbell Emulation, and Vendor Commands"
date: 2026-09-02
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
[繁體中文]({% post_url 2026-09-02-nvme-base-self-test-hmb-emulation-zh-tw %})


<div class="nvme-note">
<section id="topic-overview" class="topic-overview">
<p class="reader-paragraph opening"><span class="paragraph-number" aria-hidden="true">01.</span>This note covers device self-test, Host Memory Buffer, and extensions involving memory and command formats. It distinguishes who starts a function, who supplies its data, and when the controller may still use the resources.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>controller</dt><dd>Controller, the entity that implements the NVMe interface, fetches commands, and reports completions.</dd></div><div><dt>Host</dt><dd>The system running the operating system and issuing NVMe commands.</dd></div></dl>
<h2 id="main-ideas">The main ideas</h2>
<div class="topic-map">
<article><span class="axis-number">01</span><h3>Self-test</h3><p class="reader-paragraph axis-description"><span class="paragraph-number" aria-hidden="true">02.</span>Distinguish the start command, background progress, and result records.</p></article>
<article><span class="axis-number">02</span><h3>Host Memory Buffer</h3><p class="reader-paragraph axis-description"><span class="paragraph-number" aria-hidden="true">03.</span>Understand how host memory is made available to the controller and when it can be reclaimed.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>controller</dt><dd>Controller, the entity that implements the NVMe interface, fetches commands, and reports completions.</dd></div><div><dt>Host</dt><dd>The system running the operating system and issuing NVMe commands.</dd></div></dl></article>
<article><span class="axis-number">03</span><h3>Memory and command extensions</h3><p class="reader-paragraph axis-description"><span class="paragraph-number" aria-hidden="true">04.</span>Understand descriptors, Doorbell Emulation, and vendor-command length boundaries.</p></article>
</div>

<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">05.</span>The host and controller each have memory. Knowing the address of a region does not establish that the other party has stopped using it, much like memory-lifetime rules in an operating system.</p>
</section>
<section class="lesson" id="module-three-boundaries"><h2 id="heading-three-boundaries"><span class="section-number">01</span> Background tests, host memory, and address encoding</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">06.</span>These sections do not describe one feature. Device Self-test manages a background diagnostic operation, HMB manages ownership transfer of host memory, and DSTRD plus the vendor-command format turn encoded values into safe memory accesses. The shared method is to find a capability gate, identify the state or ownership transition, and then collect observable evidence.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>DSTRD</dt><dd>Doorbell Stride, the CAP field determining spacing between adjacent doorbell registers.</dd></div><div><dt>HMB</dt><dd>Host Memory Buffer, volatile memory ranges allocated by the host for exclusive controller use while enabled.</dd></div></dl>
<details class="technical-note"><summary>Mechanism and applicable conditions</summary>
<!-- claim:BASEDIAGMEM-SELFTEST-COMPLETION -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">07.</span>The Admin CQE for Device Self-test proves that the start or abort action was processed, not that the background test finished. Command-specific status 1Dh means an operation is already in progress; software records the CQE separately from later LID 06h evidence.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>LID 06h</dt><dd>Identifier 06h for the Device Self-test Log Page, containing current operation state and twenty historical results.</dd></div><div><dt>Admin</dt><dd>Administrative, the control path used to create, configure, query, or manage controllers and queues.</dd></div><div><dt>CQE</dt><dd>Completion Queue Entry, one completion-result structure in a CQ.</dd></div><div><dt>LID</dt><dd>Log Page Identifier: selects the type of log page to read.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §5.2.6</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.6, printed pages 201, PDF pages 227</p></details>
<!-- claim:BASEDIAGMEM-HMB-OWNERSHIP -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">08.</span>HMB is host-allocated memory leased exclusively to the controller. After successful Set Features enable, the host shall stop writing both the descriptor list and every described memory range until disable completes. This is an ownership transfer, not merely a performance hint.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>HMB</dt><dd>Host Memory Buffer, volatile memory ranges allocated by the host for exclusive controller use while enabled.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §5.2.30.2.3, 8.2.4</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.2.3, 8.2.4, printed pages 515-516, 744, PDF pages 541-542, 770</p></details>
<!-- claim:BASEDIAGMEM-DOORBELL-STRIDE -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">09.</span>CAP.DSTRD produces a spacing of 2^(2+DSTRD) bytes. DSTRD values 0, 2, and 4 yield 4, 16, and 64 bytes; software emulation can use 64-byte spacing to separate doorbells by cacheline, while the expected hardware-interface value is 0h.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>DSTRD</dt><dd>Doorbell Stride, the CAP field determining spacing between adjacent doorbell registers.</dd></div><div><dt>CAP</dt><dd>Controller Capabilities, the controller property at offset 00h that reports queue, page-size, timeout, and other capabilities.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §3.1.4.1, 8.2.3</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.1, 8.2.3, printed pages 56, 744, PDF pages 82, 770</p></details>
<!-- claim:BASEDIAGMEM-VENDOR-GATE -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">10.</span>The standard Vendor Specific command format is optional. AVSCC.VSCF controls vendor-specific Admin commands, while ICSVSCC.SNVSCF controls vendor-specific I/O commands. Read the capabilities independently; one being set does not prove that the other command class uses Figure 94.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>ICSVSCC</dt><dd>I/O Command Set Vendor Specific Command Configuration, the Identify field reporting the vendor-specific I/O-command format.</dd></div><div><dt>SNVSCF</dt><dd>Same NVM Vendor Specific Command Format, the ICSVSCC bit indicating whether I/O commands use Figure 94.</dd></div><div><dt>AVSCC</dt><dd>Admin Vendor Specific Command Configuration, the Identify field reporting the vendor-specific Admin-command format.</dd></div><div><dt>Admin</dt><dd>Administrative, the control path used to create, configure, query, or manage controllers and queues.</dd></div><div><dt>VSCF</dt><dd>Vendor Specific Command Format, the AVSCC bit indicating whether Admin commands use Figure 94.</dd></div><div><dt>I/O</dt><dd>Input/Output, the class of data operations performed on a namespace.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §5.2.14.2.1, 8.1.29</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.14.2.1, 8.1.29, printed pages 356, 374, 733, PDF pages 382, 400, 759</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">Item</th><th scope="col">Role or distinction</th><th scope="col">Conditions</th></tr></thead><tbody><tr><td>Self-test</td><td>Operation lifecycle</td><td>CQE + LID 06h</td></tr><tr><td>HMB</td><td>Exclusive-ownership lifecycle</td><td>Get FID 0Dh + disable CQE</td></tr><tr><td>Doorbell emulation</td><td>Encoded byte stride</td><td>MMIO address/write trace</td></tr><tr><td>Vendor command</td><td>Buffer-length contract</td><td>VSCF/SNVSCF + NDT/NDM</td></tr></tbody></table></div><dl class="term-note" aria-label="Terms in this passage"><div><dt>LID 06h</dt><dd>Identifier 06h for the Device Self-test Log Page, containing current operation state and twenty historical results.</dd></div><div><dt>SNVSCF</dt><dd>Same NVM Vendor Specific Command Format, the ICSVSCC bit indicating whether I/O commands use Figure 94.</dd></div><div><dt>MMIO</dt><dd>Memory-Mapped I/O, access to device registers through CPU memory operations.</dd></div><div><dt>VSCF</dt><dd>Vendor Specific Command Format, the AVSCC bit indicating whether Admin commands use Figure 94.</dd></div><div><dt>CQE</dt><dd>Completion Queue Entry, one completion-result structure in a CQ.</dd></div><div><dt>FID</dt><dd>Feature Identifier: selects the Feature to read or configure.</dd></div><div><dt>LID</dt><dd>Log Page Identifier: selects the type of log page to read.</dd></div><div><dt>NDM</dt><dd>Number of Dwords in Metadata Transfer, the actual metadata-dword count in the standard vendor-specific format.</dd></div><div><dt>NDT</dt><dd>Number of Dwords in Data Transfer, the actual data-dword count in the standard vendor-specific format.</dd></div></dl>
<aside class="worked-example"><h3>Example</h3><p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">11.</span>The same Successful Completion means only that a self-test operation started, but for HMB disable it returns ownership to the host. Equal status codes do not imply equal completion boundaries.</p></aside>
<details class="technical-note"><summary>Fields and data structures in more depth</summary>
<!-- figure-table:BASEDIAGMEM-FIG-176 -->
<details class="field-note" id="figure-BASEDIAGMEM-FIG-176"><summary>Base Figure 176 · Device Self-test Namespace Test Action</summary>
<!-- claim:BASEDIAGMEM-FIG-176-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">12.</span>Figure 176, "Device Self-test Namespace Test Action": Shows the object or capacity relationships in Device Self-test Namespace Test Action.</p><details class="source-note"><summary>Sources: Base 2.4 §5.2.6</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.6, Figure 176, printed pages 199, PDF pages 225</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>NSID</dt><dd>Namespace Identifier, a controller-visible numeric handle for a namespace; the identifier is not the namespace object itself.</dd></div></dl>
</details>
<!-- figure-table:BASEDIAGMEM-FIG-545 -->
<details class="field-note" id="figure-BASEDIAGMEM-FIG-545"><summary>Base Figure 545 · Host Memory Buffer - Command Dword 11</summary>
<!-- claim:BASEDIAGMEM-FIG-545-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">13.</span>Figure 545, "Host Memory Buffer - Command Dword 11": Defines command-specific fields in CDW11 for Host Memory Buffer.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>Dword</dt><dd>Dword (double word): 32 bits, or 4 bytes. A word is 16 bits; for example, a zero-based dword count of 3 represents 4 Dwords, or 16 bytes.</dd></div><div><dt>CDW</dt><dd>CDW (Command Dword): a 32-bit command field. In CDW10, 10 is the field index, not a byte offset.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §5.2.30.2.3</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.2.3, Figure 545, printed pages 516-517, PDF pages 542-543</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>HMNARE</dt><dd>Host Memory Non-operational Access Restriction Enable, the bit configuring non-operational HMB-access policy.</dd></div><div><dt>EHM</dt><dd>Enable Host Memory, the bit enabling or disabling controller use of HMB.</dd></div><div><dt>MR</dt><dd>Memory Return, indicating return of exactly the same previous HMB size, addresses, descriptors, and contents.</dd></div></dl>
</details>
<!-- figure-table:BASEDIAGMEM-FIG-036 -->
<details class="field-note" id="figure-BASEDIAGMEM-FIG-036"><summary>Base Figure 36 · Offset 0h: CAP - Controller Capabilities</summary>
<!-- claim:BASEDIAGMEM-FIG-036-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">14.</span>Figure 36, "Offset 0h: CAP - Controller Capabilities": Defines CAP (Controller Capabilities) at offset 0h and identifies the fields that software must read the fields at that location.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>offset</dt><dd>offset: a displacement measured from a stated start. It answers “how far from the start,” unlike an index.</dd></div><div><dt>CAP</dt><dd>Controller Capabilities, the controller property at offset 00h that reports queue, page-size, timeout, and other capabilities.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §3.1.4.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.1, Figure 36, printed pages 55-58, PDF pages 81-84</p></details>

</details>
<!-- figure-table:BASEDIAGMEM-FIG-094 -->
<details class="field-note" id="figure-BASEDIAGMEM-FIG-094"><summary>Base Figure 94 · Common Command Format - Vendor Specific Commands (Optional)</summary>
<!-- claim:BASEDIAGMEM-FIG-094-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">15.</span>Figure 94, "Common Command Format - Vendor Specific Commands (Optional)": Defines the concrete layout or value relationships for Common Command Format - Vendor Specific Commands (Optional).</p><details class="source-note"><summary>Sources: Base 2.4 §4.1.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.1.1, Figure 94, printed pages 143, PDF pages 169</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>NSID</dt><dd>Namespace Identifier, a controller-visible numeric handle for a namespace; the identifier is not the namespace object itself.</dd></div><div><dt>CDW</dt><dd>CDW (Command Dword): a 32-bit command field. In CDW10, 10 is the field index, not a byte offset.</dd></div><div><dt>NDM</dt><dd>Number of Dwords in Metadata Transfer, the actual metadata-dword count in the standard vendor-specific format.</dd></div><div><dt>NDT</dt><dd>Number of Dwords in Data Transfer, the actual data-dword count in the standard vendor-specific format.</dd></div></dl>
</details>
</details>
</section>
<section class="lesson" id="module-selftest-command-state-machine"><h2 id="heading-selftest-command-state-machine"><span class="section-number">02</span> Starting and running Device Self-test</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">16.</span>Self-test is not a synchronous diagnostic RPC. The host first uses OACS.DSTS, DSTO.SDSO, and EDSTT to establish support, concurrency scope, and timing, then constructs the command from NSID and STC. When the Admin CQE returns, the background operation has only entered the lifecycle observed through LID 06h.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>OACS.DSTS</dt><dd>The Device Self-test Supported bit in Optional Admin Command Support, gating availability of the command.</dd></div><div><dt>EDSTT</dt><dd>Extended Device Self-test Time, the nominal extended-test duration in minutes at power state 0.</dd></div><div><dt>DSTO</dt><dd>Device Self-test Options, the Identify Controller field reporting refresh and concurrency options.</dd></div><div><dt>SDSO</dt><dd>Single Device Self-test Operation, the bit selecting one subsystem-wide operation or one per controller.</dd></div><div><dt>STC</dt><dd>Self-test Code is the Device Self-test CDW10 action nibble; STC in a result entry instead means Status Code and is gated by SCVLD.</dd></div></dl>
<details class="technical-note"><summary>Mechanism and applicable conditions</summary>
<!-- claim:BASEDIAGMEM-SELFTEST-GATE -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">17.</span>Before starting Device Self-test, read Identify Controller. OACS.DSTS gates command support, EDSTT gives the nominal extended-operation time in minutes at power state 0, and DSTO.SDSO selects one subsystem-wide operation versus one operation per controller. These fields answer different questions.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>OACS.DSTS</dt><dd>The Device Self-test Supported bit in Optional Admin Command Support, gating availability of the command.</dd></div><div><dt>EDSTT</dt><dd>Extended Device Self-test Time, the nominal extended-test duration in minutes at power state 0.</dd></div><div><dt>DSTO</dt><dd>Device Self-test Options, the Identify Controller field reporting refresh and concurrency options.</dd></div><div><dt>SDSO</dt><dd>Single Device Self-test Operation, the bit selecting one subsystem-wide operation or one per controller.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §5.2.14.2.1, 8.1.8</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.14.2.1, 8.1.8, printed pages 352-358, 614, PDF pages 378-384, 640</p></details>
<!-- claim:BASEDIAGMEM-SELFTEST-NSID -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">18.</span>Device Self-test is performed by the controller that receives the command. NSID 00000000h tests only the controller, 00000001h through FFFFFFFEh select one namespace, and FFFFFFFFh includes every attached namespace accessible through that controller when the operation starts. Invalid and inactive NSIDs produce different status results.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>namespace</dt><dd>Namespace, a formatted quantity of non-volatile memory accessed by a host through a controller.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §5.2.6</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.6, printed pages 199, PDF pages 225</p></details>
<!-- claim:BASEDIAGMEM-SELFTEST-STC -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">19.</span>CDW10.STC[3:0] selects the action: 1h short, 2h extended, 3h Host-Initiated Refresh, Eh vendor specific, and Fh abort; other encodings are reserved. CDW15.DSTP is vendor specific only when STC is Eh and is reserved otherwise.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>DSTP</dt><dd>Device Self-test Parameter, CDW15 with vendor-defined meaning only for vendor-specific STC Eh.</dd></div><div><dt>STC</dt><dd>Self-test Code is the Device Self-test CDW10 action nibble; STC in a result entry instead means Status Code and is gated by SCVLD.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §5.2.6</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.6, printed pages 199-200, PDF pages 225-226</p></details>
<!-- claim:BASEDIAGMEM-SELFTEST-INPROGRESS -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">20.</span>When an operation is already running, a new short, extended, or Host-Initiated Refresh request is aborted with Device Self-test in Progress; a new vendor-specific request remains vendor specific. STC Fh instead aborts the current operation, creates the newest result, clears current status, and then completes successfully in that order.</p><details class="source-note"><summary>Sources: Base 2.4 §5.2.6</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.6, printed pages 200, PDF pages 226</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">Item</th><th scope="col">Role or distinction</th><th scope="col">Conditions</th></tr></thead><tbody><tr><td>NSID=0</td><td>Controller only</td><td>No namespace media</td></tr><tr><td>Active NSID</td><td>One namespace</td><td>Invalid and inactive status differ</td></tr><tr><td>NSID=FFFFFFFFh</td><td>All attached/accessible namespaces</td><td>Set is captured at start</td></tr><tr><td>STC=Fh</td><td>Abort current operation</td><td>Success does not prove one existed</td></tr></tbody></table></div><dl class="term-note" aria-label="Terms in this passage"><div><dt>namespace</dt><dd>Namespace, a formatted quantity of non-volatile memory accessed by a host through a controller.</dd></div></dl>
<aside class="worked-example"><h3>Example</h3><p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">21.</span>To start a short test for namespace 5, use NSID 00000005h and STC 1h, so CDW10 is 00000001h and CDW15 is zero. Immediately issuing extended STC 2h should produce command-specific status 1Dh rather than a second operation.</p></aside>
<details class="technical-note"><summary>Fields and data structures in more depth</summary>
<!-- figure-table:BASEDIAGMEM-FIG-177 -->
<details class="field-note" id="figure-BASEDIAGMEM-FIG-177"><summary>Base Figure 177 · Device Self-test - Command Dword 10</summary>
<!-- claim:BASEDIAGMEM-FIG-177-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">22.</span>Figure 177, "Device Self-test - Command Dword 10": Defines command-specific fields in CDW10 for Device Self-test.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>Dword</dt><dd>Dword (double word): 32 bits, or 4 bytes. A word is 16 bits; for example, a zero-based dword count of 3 represents 4 Dwords, or 16 bytes.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §5.2.6</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.6, Figure 177, printed pages 199, PDF pages 225</p></details>

</details>
<!-- figure-table:BASEDIAGMEM-FIG-178 -->
<details class="field-note" id="figure-BASEDIAGMEM-FIG-178"><summary>Base Figure 178 · Device Self-test - Command Dword 15</summary>
<!-- claim:BASEDIAGMEM-FIG-178-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">23.</span>Figure 178, "Device Self-test - Command Dword 15": Defines command-specific fields in CDW15 for Device Self-test.</p><details class="source-note"><summary>Sources: Base 2.4 §5.2.6</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.6, Figure 178, printed pages 200, PDF pages 226</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>DSTP</dt><dd>Device Self-test Parameter, CDW15 with vendor-defined meaning only for vendor-specific STC Eh.</dd></div></dl>
</details>
<!-- figure-table:BASEDIAGMEM-FIG-179 -->
<details class="field-note" id="figure-BASEDIAGMEM-FIG-179"><summary>Base Figure 179 · Device Self-test - Command Processing</summary>
<!-- claim:BASEDIAGMEM-FIG-179-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">24.</span>Figure 179, "Device Self-test - Command Processing": Shows the queue or command relationship expressed by Device Self-test - Command Processing.</p><details class="source-note"><summary>Sources: Base 2.4 §5.2.6</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.6, Figure 179, printed pages 200, PDF pages 226</p></details>

</details>
<!-- figure-table:BASEDIAGMEM-FIG-180 -->
<details class="field-note" id="figure-BASEDIAGMEM-FIG-180"><summary>Base Figure 180 · Device Self-test - Command Specific Status Values</summary>
<!-- claim:BASEDIAGMEM-FIG-180-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">25.</span>Figure 180, "Device Self-test - Command Specific Status Values": Defines the concrete layout or value relationships for Device Self-test - Command Specific Status Values.</p><details class="source-note"><summary>Sources: Base 2.4 §5.2.6</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.6, Figure 180, printed pages 201, PDF pages 227</p></details>

</details>
<!-- figure-table:BASEDIAGMEM-FIG-093 -->
<details class="field-note" id="figure-BASEDIAGMEM-FIG-093"><summary>Base Figure 93 · Common Command Format</summary>
<!-- claim:BASEDIAGMEM-FIG-093-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">26.</span>Figure 93, "Common Command Format": Defines the concrete layout or value relationships for Common Command Format.</p><details class="source-note"><summary>Sources: Base 2.4 §4.1.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.1.1, Figure 93, printed pages 140-142, PDF pages 166-168</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>DPTR</dt><dd>Data Pointer, the SQE field identifying a command data buffer.</dd></div><div><dt>CID</dt><dd>Command Identifier, used with the SQ identifier to identify an outstanding command.</dd></div></dl>
</details>
<!-- figure-table:BASEDIAGMEM-FIG-338 -->
<details class="field-note" id="figure-BASEDIAGMEM-FIG-338"><summary>Base Figure 338 · Identify Controller Data Structure</summary>
<!-- claim:BASEDIAGMEM-FIG-338-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">27.</span>Figure 338, "Identify Controller Data Structure": Defines the concrete layout or value relationships for Identify Controller Data Structure.</p><details class="source-note"><summary>Sources: Base 2.4 §5.2.14.2.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.14.2.1, Figure 338, printed pages 340-364, PDF pages 366-390</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>DSTO.SDSO</dt><dd>Device Self-test Options, the Identify Controller field reporting refresh and concurrency options. Here DSTO.SDSO selects its SDSO member field.</dd></div><div><dt>HMMINDS</dt><dd>Host Memory Buffer Minimum Descriptor Entry Size, the minimum usable descriptor size in 4-KiB units.</dd></div><div><dt>ICSVSCC</dt><dd>I/O Command Set Vendor Specific Command Configuration, the Identify field reporting the vendor-specific I/O-command format.</dd></div><div><dt>HMMAXD</dt><dd>Host Memory Maximum Descriptor Entries, the maximum descriptor-entry count the controller can use.</dd></div><div><dt>AVSCC</dt><dd>Admin Vendor Specific Command Configuration, the Identify field reporting the vendor-specific Admin-command format.</dd></div><div><dt>HMMIN</dt><dd>Host Memory Buffer Minimum Size, the controller's minimum requested size in 4-KiB units.</dd></div><div><dt>HMPRE</dt><dd>Host Memory Buffer Preferred Size, the controller's preferred allocation in 4-KiB units.</dd></div></dl>
</details>
</details>
</section>
<section class="lesson" id="module-selftest-observe-results"><h2 id="heading-selftest-observe-results"><span class="section-number">03</span> Current progress and history in LID 06h</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">28.</span>DSTOS/DSTCS in the header answer what is running now, while RDS1 through RDS20 answer how earlier operations ended. Each result then separates operation code, result reason, segment, validity bitmap, and diagnostic payload. The NVM Command Set gives FLBA an LBA meaning only when FVLD is one.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>DSTCS</dt><dd>Device Self-test Completion Status, the LID 06h completion percentage from 0 through 100.</dd></div><div><dt>DSTOS</dt><dd>Device Self-test Operation Status, the LID 06h nibble identifying the current operation.</dd></div><div><dt>FLBA</dt><dd>Failing LBA, defined by the NVM Command Set as one logical block address that caused self-test failure.</dd></div><div><dt>FVLD</dt><dd>Failing LBA Valid, the validity bit determining whether FLBA may be interpreted.</dd></div><div><dt>NVM</dt><dd>Non-Volatile Memory, memory that retains data without power.</dd></div></dl>
<details class="technical-note"><summary>Mechanism and applicable conditions</summary>
<!-- claim:BASEDIAGMEM-SELFTEST-LOG-COMMAND -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">29.</span>The minimum Get Log Page slice for LID 06h uses LID 06h, LSP 0, RAE selected by event policy, NUMD for 564 bytes, LPOL/LPOU 0, OT 0, CSI 0, and UIDX 0. 564 bytes are 141 dwords, so zero-based NUMD is 140 or 008Ch; with RAE 0, CDW10 is 008C0006h.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>zero-based</dt><dd>zero-based: numbering starts at zero, so raw=3 can mean the fourth item or four units; the field definition still decides which.</dd></div><div><dt>LPOL</dt><dd>Log Page Offset Lower, the low 32 bits of the Get Log Page byte offset.</dd></div><div><dt>LPOU</dt><dd>Log Page Offset Upper, the high 32 bits of the Get Log Page byte offset.</dd></div><div><dt>NUMD</dt><dd>Number of Dwords, a zero-based transfer-dword count; actual bytes = (NUMD + 1) × 4.</dd></div><div><dt>UIDX</dt><dd>UUID Index, an index into the UUID List; zero indicates that no UUID is specified.</dd></div><div><dt>CSI</dt><dd>I/O Command Set Identifier: selects an I/O command set; NVM uses 00h.</dd></div><div><dt>LSP</dt><dd>Log Specific Field, a command selector whose meaning is defined by the selected log page.</dd></div><div><dt>RAE</dt><dd>Retain Asynchronous Event, the Get Log Page selector controlling retention of a related asynchronous event.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §5.2.13</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13, printed pages 213-216, PDF pages 239-242</p></details>
<!-- claim:BASEDIAGMEM-SELFTEST-CURRENT -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">30.</span>In LID 06h, byte 0 DSTOS identifies the current operation and byte 1 DSTCS[6:0] is the completion percentage; the host should ignore DSTCS when DSTOS is zero. When an operation completes or is aborted, the controller creates a result entry before clearing in-progress status to zero.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>DSTCS</dt><dd>Device Self-test Completion Status, the LID 06h completion percentage from 0 through 100.</dd></div><div><dt>DSTOS</dt><dd>Device Self-test Operation Status, the LID 06h nibble identifying the current operation.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §5.2.13.1.7</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.7, printed pages 229-230, PDF pages 255-256</p></details>
<!-- claim:BASEDIAGMEM-SELFTEST-HISTORY -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">31.</span>LID 06h retains 20 results of 28 bytes each, with RDS1 always the most recently completed or aborted operation. An unused entry uses DSTR Fh and DSTC 0h, while the host ignores its other fields; residual nonzero bytes are not history records.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>DSTR</dt><dd>Device Self-test Result, the result-entry nibble identifying success, abort, or segment failure.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §5.2.13.1.7</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.7, printed pages 229-230, PDF pages 255-256</p></details>
<!-- claim:BASEDIAGMEM-SELFTEST-RESULT -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">32.</span>In each result DSTS, the high-nibble DSTC records the original self-test code and low-nibble DSTR records the completion or abort reason. SEGN identifies the first failed segment only when DSTR is 7h and is ignored for other DSTR values.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>DSTR</dt><dd>Device Self-test Result, the result-entry nibble identifying success, abort, or segment failure.</dd></div><div><dt>SEGN</dt><dd>Segment Number, identifying the first failed diagnostic segment only when DSTR is 7h.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §5.2.13.1.7</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.7, printed pages 231, PDF pages 257</p></details>
<!-- claim:BASEDIAGMEM-SELFTEST-VALIDITY -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">33.</span>VDINFO NSIDVLD, FVLD, SCTVLD, and SCVLD are independent validity gates. NSID, FLBA, STCT, and STC are interpreted only when their corresponding bit is one; validate the bit before the value instead of inferring validity from nonzero data.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>VDINFO</dt><dd>Valid Diagnostic Information, the bitmap independently gating NSID, FLBA, SCT, and SC.</dd></div><div><dt>FLBA</dt><dd>Failing LBA, defined by the NVM Command Set as one logical block address that caused self-test failure.</dd></div><div><dt>FVLD</dt><dd>Failing LBA Valid, the validity bit determining whether FLBA may be interpreted.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §5.2.13.1.7</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.7, printed pages 231-232, PDF pages 257-258</p></details>
<!-- claim:BASEDIAGMEM-SELFTEST-NVM-FLBA -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">34.</span>Base leaves Figure 219 FLBA to the applicable I/O Command Set. NVM Command Set 1.3 defines bytes 23:16 as the logical block address that caused the failure; when multiple logical blocks fail, only one is reported, and it is valid only when FVLD is one.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>logical block</dt><dd>An addressable unit in a namespace; its data size is determined by the active format.</dd></div><div><dt>I/O</dt><dd>Input/Output, the class of data operations performed on a namespace.</dd></div><div><dt>NVM</dt><dd>Non-Volatile Memory, memory that retains data without power.</dd></div></dl><details class="source-note"><summary>Sources: NVM Command Set 1.3 §4.1.4.3</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §4.1.4.3, printed pages 76, PDF pages 76</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">Item</th><th scope="col">Role or distinction</th><th scope="col">Conditions</th></tr></thead><tbody><tr><td>DSTOS/DSTCS</td><td>Current state/progress</td><td>Ignore percentage when DSTOS=0</td></tr><tr><td>DSTR=7h + SEGN</td><td>Known first failed segment</td><td>Ignore SEGN for other DSTR</td></tr><tr><td>FVLD + FLBA</td><td>One failing LBA</td><td>Not a list of every failed LBA</td></tr><tr><td>POH + STCT/STC</td><td>Failure context</td><td>Validity bits still apply</td></tr></tbody></table></div><dl class="term-note" aria-label="Terms in this passage"><div><dt>SEGN</dt><dd>Segment Number, identifying the first failed diagnostic segment only when DSTR is 7h.</dd></div><div><dt>POH</dt><dd>Power On Hours, accumulated power-on hours when a self-test result is created, excluding specified low-power time.</dd></div></dl>
<aside class="worked-example"><h3>Example</h3><p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">35.</span>The complete log is 564 bytes or 141 dwords, so NUMD is 140 or 008Ch. With LSP 0 and RAE 0, CDW10 is 008C0006h. If RDS1.DSTS is 17h, high nibble 1h means short test and low nibble 7h means a known failed segment; only then read SEGN.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>NUMD</dt><dd>Number of Dwords, a zero-based transfer-dword count; actual bytes = (NUMD + 1) × 4.</dd></div><div><dt>LSP</dt><dd>Log Specific Field, a command selector whose meaning is defined by the selected log page.</dd></div><div><dt>RAE</dt><dd>Retain Asynchronous Event, the Get Log Page selector controlling retention of a related asynchronous event.</dd></div></dl></aside>
<details class="technical-note"><summary>Fields and data structures in more depth</summary>
<!-- figure-table:BASEDIAGMEM-FIG-111 -->
<details class="field-note" id="figure-BASEDIAGMEM-FIG-111"><summary>NVM Figure 111 · Self-test Results Data Structure</summary>
<!-- claim:BASEDIAGMEM-FIG-111-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">36.</span>Figure 111, "Self-test Results Data Structure": Defines the concrete layout or value relationships for Self-test Results Data Structure.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §4.1.4.3</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §4.1.4.3, Figure 111, printed pages 76, PDF pages 76</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>logical block</dt><dd>An addressable unit in a namespace; its data size is determined by the active format.</dd></div></dl>
</details>
<!-- figure-table:BASEDIAGMEM-FIG-218 -->
<details class="field-note" id="figure-BASEDIAGMEM-FIG-218"><summary>Base Figure 218 · Device Self-test Log Page</summary>
<!-- claim:BASEDIAGMEM-FIG-218-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">37.</span>Figure 218, "Device Self-test Log Page": Connects Device Self-test Log Page to a self-test, host-memory, doorbell, or vendor-command engineering boundary.</p><details class="source-note"><summary>Sources: Base 2.4 §5.2.13.1.7</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.7, Figure 218, printed pages 230, PDF pages 256</p></details>

</details>
<!-- figure-table:BASEDIAGMEM-FIG-219 -->
<details class="field-note" id="figure-BASEDIAGMEM-FIG-219"><summary>Base Figure 219 · Self-test Result Data Structure</summary>
<!-- claim:BASEDIAGMEM-FIG-219-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">38.</span>Figure 219, "Self-test Result Data Structure": Defines the concrete layout or value relationships for Self-test Result Data Structure.</p><details class="source-note"><summary>Sources: Base 2.4 §5.2.13.1.7</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.7, Figure 219, printed pages 231-232, PDF pages 257-258</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>VDINFO</dt><dd>Valid Diagnostic Information, the bitmap independently gating NSID, FLBA, SCT, and SC.</dd></div><div><dt>POH</dt><dd>Power On Hours, accumulated power-on hours when a self-test result is created, excluding specified low-power time.</dd></div></dl>
</details>
<!-- figure-table:BASEDIAGMEM-FIG-700 -->
<details class="field-note" id="figure-BASEDIAGMEM-FIG-700"><summary>Base Figure 700 · Example Device Self-test Operation (Informative)</summary>
<!-- claim:BASEDIAGMEM-FIG-700-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">39.</span>Figure 700, "Example Device Self-test Operation (Informative)": Defines the concrete layout or value relationships for Example Device Self-test Operation (Informative).</p><details class="source-note"><summary>Sources: Base 2.4 §8.1.8</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §8.1.8, Figure 700, printed pages 615, PDF pages 641</p></details>

</details>
<!-- figure-table:BASEDIAGMEM-FIG-701 -->
<details class="field-note" id="figure-BASEDIAGMEM-FIG-701"><summary>Base Figure 701 · Format NVM command Aborting a Device Self-Test Operation</summary>
<!-- claim:BASEDIAGMEM-FIG-701-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">40.</span>Figure 701, "Format NVM command Aborting a Device Self-Test Operation": Defines the concrete layout or value relationships for Format NVM command Aborting a Device Self-Test Operation.</p><details class="source-note"><summary>Sources: Base 2.4 §8.1.8.1-8.1.8.2</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §8.1.8.1-8.1.8.2, Figure 701, printed pages 616, PDF pages 642</p></details>

</details>
<!-- figure-table:BASEDIAGMEM-FIG-203 -->
<details class="field-note" id="figure-BASEDIAGMEM-FIG-203"><summary>Base Figure 203 · Get Log Page - Data Pointer</summary>
<!-- claim:BASEDIAGMEM-FIG-203-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">41.</span>Figure 203, "Get Log Page - Data Pointer": Connects Get Log Page - Data Pointer to a self-test, host-memory, doorbell, or vendor-command engineering boundary.</p><details class="source-note"><summary>Sources: Base 2.4 §5.2.13</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13, Figure 203, printed pages 213, PDF pages 239</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>DPTR</dt><dd>Data Pointer, the SQE field identifying a command data buffer.</dd></div></dl>
</details>
<!-- figure-table:BASEDIAGMEM-FIG-204 -->
<details class="field-note" id="figure-BASEDIAGMEM-FIG-204"><summary>Base Figure 204 · Get Log Page - Command Dword 10</summary>
<!-- claim:BASEDIAGMEM-FIG-204-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">42.</span>Figure 204, "Get Log Page - Command Dword 10": Defines command-specific fields in CDW10 for Get Log Page.</p><details class="source-note"><summary>Sources: Base 2.4 §5.2.13</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13, Figure 204, printed pages 213, PDF pages 239</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>NUMDL</dt><dd>Number of Dwords Lower, the low 16 bits of Get Log Page NUMD.</dd></div></dl>
</details>
<!-- figure-table:BASEDIAGMEM-FIG-205 -->
<details class="field-note" id="figure-BASEDIAGMEM-FIG-205"><summary>Base Figure 205 · Get Log Page - Command Dword 11</summary>
<!-- claim:BASEDIAGMEM-FIG-205-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">43.</span>Figure 205, "Get Log Page - Command Dword 11": Defines command-specific fields in CDW11 for Get Log Page.</p><details class="source-note"><summary>Sources: Base 2.4 §5.2.13</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13, Figure 205, printed pages 214, PDF pages 240</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>NUMDU</dt><dd>Number of Dwords Upper, the high 16 bits of Get Log Page NUMD.</dd></div><div><dt>LSI</dt><dd>Log Specific Identifier, an identifier whose meaning is defined by the selected log page.</dd></div></dl>
</details>
<!-- figure-table:BASEDIAGMEM-FIG-206 -->
<details class="field-note" id="figure-BASEDIAGMEM-FIG-206"><summary>Base Figure 206 · Get Log Page - Command Dword 12</summary>
<!-- claim:BASEDIAGMEM-FIG-206-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">44.</span>Figure 206, "Get Log Page - Command Dword 12": Defines command-specific fields in CDW12 for Get Log Page.</p><details class="source-note"><summary>Sources: Base 2.4 §5.2.13</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13, Figure 206, printed pages 214, PDF pages 240</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>LPOL</dt><dd>Log Page Offset Lower, the low 32 bits of the Get Log Page byte offset.</dd></div></dl>
</details>
<!-- figure-table:BASEDIAGMEM-FIG-207 -->
<details class="field-note" id="figure-BASEDIAGMEM-FIG-207"><summary>Base Figure 207 · Get Log Page - Command Dword 13</summary>
<!-- claim:BASEDIAGMEM-FIG-207-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">45.</span>Figure 207, "Get Log Page - Command Dword 13": Defines command-specific fields in CDW13 for Get Log Page.</p><details class="source-note"><summary>Sources: Base 2.4 §5.2.13</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13, Figure 207, printed pages 214, PDF pages 240</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>LPOU</dt><dd>Log Page Offset Upper, the high 32 bits of the Get Log Page byte offset.</dd></div></dl>
</details>
<!-- figure-table:BASEDIAGMEM-FIG-208 -->
<details class="field-note" id="figure-BASEDIAGMEM-FIG-208"><summary>Base Figure 208 · Get Log Page - Command Dword 14</summary>
<!-- claim:BASEDIAGMEM-FIG-208-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">46.</span>Figure 208, "Get Log Page - Command Dword 14": Defines command-specific fields in CDW14 for Get Log Page.</p><details class="source-note"><summary>Sources: Base 2.4 §5.2.13</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13, Figure 208, printed pages 214-215, PDF pages 240-241</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>UIDX</dt><dd>UUID Index, an index into the UUID List; zero indicates that no UUID is specified.</dd></div><div><dt>CSI</dt><dd>I/O Command Set Identifier: selects an I/O command set; NVM uses 00h.</dd></div></dl>
</details>
<!-- figure-table:BASEDIAGMEM-FIG-209 -->
<details class="field-note" id="figure-BASEDIAGMEM-FIG-209"><summary>Base Figure 209 · Get Log Page - Log Page Identifiers</summary>
<!-- claim:BASEDIAGMEM-FIG-209-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">47.</span>Figure 209, "Get Log Page - Log Page Identifiers": Defines the identifier composition or namespace of values shown by Get Log Page - Log Page Identifiers.</p><details class="source-note"><summary>Sources: Base 2.4 §5.2.13</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13, Figure 209, printed pages 215-216, PDF pages 241-242</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>NVM subsystem</dt><dd>NVM subsystem, the NVMe system boundary containing controllers, ports, namespaces, and non-volatile storage resources.</dd></div></dl>
</details>
</details>
</section>
<section class="lesson" id="module-hmb-ownership-lifecycle"><h2 id="heading-hmb-ownership-lifecycle"><span class="section-number">04</span> Providing, using, and reclaiming HMB memory</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">48.</span>HMB is not merely controller cache. It is an ownership protocol: the host allocates pages and a descriptor list, stops writing after successful enable, the controller initializes and uses them, and the host disables HMB before reclaiming memory. Modification rights return only when the CQE is posted.</p>
<figure><figcaption><strong>The lifetime of a Host Memory Buffer</strong></figcaption><ol class="flow-steps"><li>The host allocates memory and builds a descriptor list.</li><li>The HMB Feature makes those ranges available to the controller.</li><li>The host keeps the described memory valid while HMB is enabled.</li><li>The host reclaims memory only after disabling HMB and completing the required handoff.</li></ol><figcaption>The memory belongs to the host, but cannot be reclaimed while the controller may still use it.</figcaption></figure>

<details class="technical-note"><summary>Mechanism and applicable conditions</summary>
<!-- claim:BASEDIAGMEM-HMB-CAPABILITY -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">49.</span>HMPRE zero means HMB is unsupported; a nonzero value is the preferred size in 4-KiB units, while HMMIN gives the minimum request. HMMINDS and HMMAXD constrain descriptors. The controller shall still function correctly when the host cannot provide HMB.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>HMMINDS</dt><dd>Host Memory Buffer Minimum Descriptor Entry Size, the minimum usable descriptor size in 4-KiB units.</dd></div><div><dt>HMMAXD</dt><dd>Host Memory Maximum Descriptor Entries, the maximum descriptor-entry count the controller can use.</dd></div><div><dt>HMMIN</dt><dd>Host Memory Buffer Minimum Size, the controller's minimum requested size in 4-KiB units.</dd></div><div><dt>HMPRE</dt><dd>Host Memory Buffer Preferred Size, the controller's preferred allocation in 4-KiB units.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §5.2.14.2.1, 8.2.4</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.14.2.1, 8.2.4, printed pages 357, 362, 744, PDF pages 383, 388, 770</p></details>
<!-- claim:BASEDIAGMEM-HMB-SEQUENCE -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">50.</span>Reissuing EHM one while HMB is already enabled is aborted with Command Sequence Error; issuing EHM zero while disabled succeeds without action. Before disable completion, the controller should retrieve needed data; only the posted CQE means the host may safely modify or reclaim the buffer.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>EHM</dt><dd>Enable Host Memory, the bit enabling or disabling controller use of HMB.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §5.2.30.2.3</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.2.3, printed pages 515-516, PDF pages 541-542</p></details>
<!-- claim:BASEDIAGMEM-HMB-SURPRISE -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">51.</span>During surprise removal while HMB is in use, the controller shall ensure no data loss or data corruption. This does not make HMB contents persistent; it means internal correctness cannot depend on the host always completing the normal release flow.</p><details class="source-note"><summary>Sources: Base 2.4 §8.2.4</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §8.2.4, printed pages 744, PDF pages 770</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">Item</th><th scope="col">Role or distinction</th><th scope="col">Conditions</th></tr></thead><tbody><tr><td>Before enable</td><td>Host owns and initializes descriptors</td><td>Validate alignment/count</td></tr><tr><td>After enable CQE</td><td>Controller exclusive use</td><td>Host shall not write</td></tr><tr><td>Disable in flight</td><td>Controller may still retrieve data</td><td>Host still waits</td></tr><tr><td>After disable CQE</td><td>Host may modify/reclaim</td><td>Record fence timestamp</td></tr></tbody></table></div>
<aside class="worked-example"><h3>Example</h3><p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">52.</span>If a driver removes DMA mappings after issuing EHM zero but before its CQE, the controller may still retrieve required data; that is a use-after-unmap. The correct fence is disable completion, not the SQ-tail doorbell write.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>SQ</dt><dd>Submission Queue, the queue into which the host places commands.</dd></div></dl></aside>
<details class="technical-note"><summary>Fields and data structures in more depth</summary>
<!-- figure-table:BASEDIAGMEM-FIG-552 -->
<details class="field-note" id="figure-BASEDIAGMEM-FIG-552"><summary>Base Figure 552 · Host Memory Buffer - Completion Queue Entry Dword 0</summary>
<!-- claim:BASEDIAGMEM-FIG-552-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">53.</span>Figure 552, "Host Memory Buffer - Completion Queue Entry Dword 0": Shows the queue or command relationship expressed by Host Memory Buffer - Completion Queue Entry Dword 0.</p><details class="source-note"><summary>Sources: Base 2.4 §5.2.30.2.3</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.2.3, Figure 552, printed pages 518-519, PDF pages 544-545</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>HMNARE</dt><dd>Host Memory Non-operational Access Restriction Enable, the bit configuring non-operational HMB-access policy.</dd></div><div><dt>HMNAR</dt><dd>Host Memory Non-operational Access Restricted, the state bit reporting whether restriction is currently active.</dd></div></dl>
</details>
<!-- figure-table:BASEDIAGMEM-FIG-553 -->
<details class="field-note" id="figure-BASEDIAGMEM-FIG-553"><summary>Base Figure 553 · Host Memory Buffer - Attributes Data Structure</summary>
<!-- claim:BASEDIAGMEM-FIG-553-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">54.</span>Figure 553, "Host Memory Buffer - Attributes Data Structure": Defines the concrete layout or value relationships for Host Memory Buffer - Attributes Data Structure.</p><details class="source-note"><summary>Sources: Base 2.4 §5.2.30.2.3</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.2.3, Figure 553, printed pages 519, PDF pages 545</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>HMDLEC</dt><dd>Host Memory Descriptor List Entry Count, the number of valid entries in the HMDL.</dd></div><div><dt>HSIZE</dt><dd>Host Memory Buffer Size, the total HMB size in CC.MPS memory-page units.</dd></div></dl>
</details>
</details>
</section>
<section class="lesson" id="module-hmb-command-math"><h2 id="heading-hmb-command-math"><span class="section-number">05</span> HMB descriptors, sizes, and addresses</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">55.</span>HSIZE, BSIZE, and BADD use CC.MPS pages, while HMPRE, HMMIN, and HMMINDS use 4-KiB units. The unit systems are not interchangeable. HMDL is 16-byte aligned with fixed 16-byte entries, and HMDLEC is an entry count—not zero based and not a byte length.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>HMDLEC</dt><dd>Host Memory Descriptor List Entry Count, the number of valid entries in the HMDL.</dd></div><div><dt>BSIZE</dt><dd>Buffer Size, the contiguous range length in CC.MPS pages in an HMB descriptor.</dd></div><div><dt>HSIZE</dt><dd>Host Memory Buffer Size, the total HMB size in CC.MPS memory-page units.</dd></div><div><dt>BADD</dt><dd>Buffer Address, the CC.MPS-aligned memory-page address in an HMB descriptor.</dd></div><div><dt>HMDL</dt><dd>Host Memory Descriptor List, a contiguous host-memory array of 16-byte HMB descriptors.</dd></div><div><dt>MPS</dt><dd>Memory Page Size, the controller memory-page-size setting; it affects queue addresses and PRP alignment.</dd></div><div><dt>CC</dt><dd>Controller Configuration, the property through which the host selects settings and enables or disables a controller.</dd></div></dl>
<details class="technical-note"><summary>Mechanism and applicable conditions</summary>
<!-- claim:BASEDIAGMEM-HMB-SET-COMMAND -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">56.</span>Set Features uses FID 0Dh. CDW11 holds EHM, MR, and HMNARE; CDW12 holds HSIZE; CDW13/14 form the 64-bit HMDL address; and CDW15 is HMDLEC. The HMDL address is 16-byte aligned, and HMDLEC zero returns Invalid Field in Command.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>HMDL</dt><dd>Host Memory Descriptor List, a contiguous host-memory array of 16-byte HMB descriptors.</dd></div><div><dt>FID</dt><dd>Feature Identifier: selects the Feature to read or configure.</dd></div><div><dt>MR</dt><dd>Memory Return, indicating return of exactly the same previous HMB size, addresses, descriptors, and contents.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §5.2.30, 5.2.30.2.3</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30, 5.2.30.2.3, printed pages 456-459, 516-518, PDF pages 482-485, 542-544</p></details>
<!-- claim:BASEDIAGMEM-HMB-DESCRIPTORS -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">57.</span>HMDL is a contiguous array of 16-byte descriptors. Each entry BADD is aligned to the CC.MPS memory-page size, and BSIZE gives a contiguous length in the same page units. The controller ignores an entry whose BSIZE is zero, and HSIZE is reconciled with the usable descriptor-page total.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>BSIZE</dt><dd>Buffer Size, the contiguous range length in CC.MPS pages in an HMB descriptor.</dd></div><div><dt>BADD</dt><dd>Buffer Address, the CC.MPS-aligned memory-page address in an HMB descriptor.</dd></div><div><dt>MPS</dt><dd>Memory Page Size, the controller memory-page-size setting; it affects queue addresses and PRP alignment.</dd></div><div><dt>CC</dt><dd>Controller Configuration, the property through which the host selects settings and enables or disables a controller.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §5.2.30.2.3</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.2.3, printed pages 517-518, PDF pages 543-544</p></details>
<!-- claim:BASEDIAGMEM-HMB-NUMERIC -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">58.</span>Informative example: CC.MPS zero means a 4-KiB page, so HSIZE 64 means 256 KiB. For HMDL 00000012_34567000h and HMDLEC 2, CDW13 is 34567000h, CDW14 is 00000012h, and CDW15 is 00000002h. Two descriptors of BSIZE 32 pages each total exactly 64 pages.</p><details class="source-note"><summary>Sources: Base 2.4 §5.2.30.2.3</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.2.3, printed pages 516-518, PDF pages 542-544</p></details>
<!-- claim:BASEDIAGMEM-HMB-GET -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">59.</span>Get Features uses FID 0Dh. On successful SEL other than supported capabilities, CQE.DW0 returns EHM, HMNARE, and HMNAR, while the data buffer returns a 4-KiB Attributes structure containing HSIZE, HMDL address, and HMDLEC. Enabled and currently access-restricted are different states.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>HMNAR</dt><dd>Host Memory Non-operational Access Restricted, the state bit reporting whether restriction is currently active.</dd></div><div><dt>SEL</dt><dd>Select, the Get Features field choosing current, default, saved, or supported-capabilities view.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §5.2.12, 5.2.30.2.3</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.12, 5.2.30.2.3, printed pages 209-212, 518-519, PDF pages 235-238, 544-545</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">Item</th><th scope="col">Role or distinction</th><th scope="col">Conditions</th></tr></thead><tbody><tr><td>HMPRE/HMMIN</td><td>4-KiB units</td><td>Capability request</td></tr><tr><td>HSIZE/BSIZE</td><td>CC.MPS units</td><td>Configured memory</td></tr><tr><td>HMDL address</td><td>16-byte aligned</td><td>CDW13 low + CDW14 high</td></tr><tr><td>BADD</td><td>CC.MPS aligned</td><td>BSIZE=0 entry ignored</td></tr></tbody></table></div>
<aside class="worked-example"><h3>Example</h3><p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">60.</span>With CC.MPS zero and HSIZE 64, HMB is 256 KiB. HMDL 00000012_34567000h and HMDLEC 2 produce CDW13 34567000h, CDW14 00000012h, and CDW15 2. Two BSIZE-32 ranges are 128 KiB each, totaling 256 KiB.</p></aside>
<details class="technical-note"><summary>Fields and data structures in more depth</summary>
<!-- figure-table:BASEDIAGMEM-FIG-546 -->
<details class="field-note" id="figure-BASEDIAGMEM-FIG-546"><summary>Base Figure 546 · Host Memory Buffer - Command Dword 12</summary>
<!-- claim:BASEDIAGMEM-FIG-546-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">61.</span>Figure 546, "Host Memory Buffer - Command Dword 12": Defines command-specific fields in CDW12 for Host Memory Buffer.</p><details class="source-note"><summary>Sources: Base 2.4 §5.2.30.2.3</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.2.3, Figure 546, printed pages 517, PDF pages 543</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>CC.MPS units</dt><dd>Controller Configuration, the property through which the host selects settings and enables or disables a controller. Here CC.MPS units selects its MPS units member field.</dd></div></dl>
</details>
<!-- figure-table:BASEDIAGMEM-FIG-547 -->
<details class="field-note" id="figure-BASEDIAGMEM-FIG-547"><summary>Base Figure 547 · Host Memory Buffer - Command Dword 13</summary>
<!-- claim:BASEDIAGMEM-FIG-547-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">62.</span>Figure 547, "Host Memory Buffer - Command Dword 13": Defines command-specific fields in CDW13 for Host Memory Buffer.</p><details class="source-note"><summary>Sources: Base 2.4 §5.2.30.2.3</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.2.3, Figure 547, printed pages 517, PDF pages 543</p></details>

</details>
<!-- figure-table:BASEDIAGMEM-FIG-548 -->
<details class="field-note" id="figure-BASEDIAGMEM-FIG-548"><summary>Base Figure 548 · Host Memory Buffer - Command Dword 14</summary>
<!-- claim:BASEDIAGMEM-FIG-548-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">63.</span>Figure 548, "Host Memory Buffer - Command Dword 14": Defines command-specific fields in CDW14 for Host Memory Buffer.</p><details class="source-note"><summary>Sources: Base 2.4 §5.2.30.2.3</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.2.3, Figure 548, printed pages 517, PDF pages 543</p></details>

</details>
<!-- figure-table:BASEDIAGMEM-FIG-549 -->
<details class="field-note" id="figure-BASEDIAGMEM-FIG-549"><summary>Base Figure 549 · Host Memory Buffer - Command Dword 15</summary>
<!-- claim:BASEDIAGMEM-FIG-549-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">64.</span>Figure 549, "Host Memory Buffer - Command Dword 15": Defines command-specific fields in CDW15 for Host Memory Buffer.</p><details class="source-note"><summary>Sources: Base 2.4 §5.2.30.2.3</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.2.3, Figure 549, printed pages 518, PDF pages 544</p></details>

</details>
<!-- figure-table:BASEDIAGMEM-FIG-550 -->
<details class="field-note" id="figure-BASEDIAGMEM-FIG-550"><summary>Base Figure 550 · Host Memory Buffer - Host Memory Descriptor List</summary>
<!-- claim:BASEDIAGMEM-FIG-550-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">65.</span>Figure 550, "Host Memory Buffer - Host Memory Descriptor List": Defines the concrete layout or value relationships for Host Memory Buffer - Host Memory Descriptor List.</p><details class="source-note"><summary>Sources: Base 2.4 §5.2.30.2.3</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.2.3, Figure 550, printed pages 518, PDF pages 544</p></details>

</details>
<!-- figure-table:BASEDIAGMEM-FIG-551 -->
<details class="field-note" id="figure-BASEDIAGMEM-FIG-551"><summary>Base Figure 551 · Host Memory Buffer - Host Memory Buffer Descriptor Entry</summary>
<!-- claim:BASEDIAGMEM-FIG-551-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">66.</span>Figure 551, "Host Memory Buffer - Host Memory Buffer Descriptor Entry": Defines the concrete layout or value relationships for Host Memory Buffer - Host Memory Buffer Descriptor Entry.</p><details class="source-note"><summary>Sources: Base 2.4 §5.2.30.2.3</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.2.3, Figure 551, printed pages 518, PDF pages 544</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>CC.MPS alignment</dt><dd>Controller Configuration, the property through which the host selects settings and enables or disables a controller. Here CC.MPS alignment selects its MPS alignment member field.</dd></div></dl>
</details>
<!-- figure-table:BASEDIAGMEM-FIG-197 -->
<details class="field-note" id="figure-BASEDIAGMEM-FIG-197"><summary>Base Figure 197 · Get Features - Data Pointer</summary>
<!-- claim:BASEDIAGMEM-FIG-197-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">67.</span>Figure 197, "Get Features - Data Pointer": Connects Get Features - Data Pointer to a self-test, host-memory, doorbell, or vendor-command engineering boundary.</p><details class="source-note"><summary>Sources: Base 2.4 §5.2.12</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.12, Figure 197, printed pages 209, PDF pages 235</p></details>

</details>
<!-- figure-table:BASEDIAGMEM-FIG-198 -->
<details class="field-note" id="figure-BASEDIAGMEM-FIG-198"><summary>Base Figure 198 · Get Features - Command Dword 10</summary>
<!-- claim:BASEDIAGMEM-FIG-198-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">68.</span>Figure 198, "Get Features - Command Dword 10": Defines command-specific fields in CDW10 for Get Features.</p><details class="source-note"><summary>Sources: Base 2.4 §5.2.12</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.12, Figure 198, printed pages 209-210, PDF pages 235-236</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>SEL</dt><dd>Select, the Get Features field choosing current, default, saved, or supported-capabilities view.</dd></div></dl>
</details>
<!-- figure-table:BASEDIAGMEM-FIG-200 -->
<details class="field-note" id="figure-BASEDIAGMEM-FIG-200"><summary>Base Figure 200 · Feature Identifiers for Get Features</summary>
<!-- claim:BASEDIAGMEM-FIG-200-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">69.</span>Figure 200, "Feature Identifiers for Get Features": Defines the identifier composition or namespace of values shown by Feature Identifiers for Get Features.</p><details class="source-note"><summary>Sources: Base 2.4 §5.2.12</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.12, Figure 200, printed pages 210-211, PDF pages 236-237</p></details>

</details>
<!-- figure-table:BASEDIAGMEM-FIG-463 -->
<details class="field-note" id="figure-BASEDIAGMEM-FIG-463"><summary>Base Figure 463 · Set Features - Data Pointer</summary>
<!-- claim:BASEDIAGMEM-FIG-463-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">70.</span>Figure 463, "Set Features - Data Pointer": Connects Set Features - Data Pointer to a self-test, host-memory, doorbell, or vendor-command engineering boundary.</p><details class="source-note"><summary>Sources: Base 2.4 §5.2.30</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30, Figure 463, printed pages 456, PDF pages 482</p></details>

</details>
<!-- figure-table:BASEDIAGMEM-FIG-464 -->
<details class="field-note" id="figure-BASEDIAGMEM-FIG-464"><summary>Base Figure 464 · Set Features - Command Dword 10</summary>
<!-- claim:BASEDIAGMEM-FIG-464-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">71.</span>Figure 464, "Set Features - Command Dword 10": Defines command-specific fields in CDW10 for Set Features.</p><details class="source-note"><summary>Sources: Base 2.4 §5.2.30</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30, Figure 464, printed pages 457, PDF pages 483</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>SV</dt><dd>Save, the Set Features bit requesting that the controller also save the configured value.</dd></div></dl>
</details>
<!-- figure-table:BASEDIAGMEM-FIG-466 -->
<details class="field-note" id="figure-BASEDIAGMEM-FIG-466"><summary>Base Figure 466 · Feature Identifiers for Set Features</summary>
<!-- claim:BASEDIAGMEM-FIG-466-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">72.</span>Figure 466, "Feature Identifiers for Set Features": Defines the identifier composition or namespace of values shown by Feature Identifiers for Set Features.</p><details class="source-note"><summary>Sources: Base 2.4 §5.2.30</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30, Figure 466, printed pages 457-459, PDF pages 483-485</p></details>

</details>
</details>
</section>
<section class="lesson" id="module-hmb-reset-power"><h2 id="heading-hmb-reset-power"><span class="section-number">06</span> HMB state across power transitions and resets</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">73.</span>HMNARE is access policy, HMNAR is current state, and MR says whether exactly the same prior contents are returned after reset or RTD3. They are not interchangeable. Controller Level Reset loses the assignment, RTD3 calls for release beforehand, and non-operational restriction only limits access in selected states.</p>
<details class="technical-note"><summary>Mechanism and applicable conditions</summary>
<!-- claim:BASEDIAGMEM-HMB-NONOP -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">74.</span>HMNARE may be enabled only when Identify.CTRATT.HMBR is one. HMNARE is policy, while HMNAR reports whether a non-operational state currently restricts the controller; Admin commands and background operations initiated by them are explicit exceptions. NOPPME does not alter this HMB restriction.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>NOPPME</dt><dd>Non-Operational Power State Permissive Mode Enable, controlling whether controller background work may temporarily exceed a non-operational power limit.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §5.2.30.2.3</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.2.3, printed pages 516-519, PDF pages 542-545</p></details>
<!-- claim:BASEDIAGMEM-HMB-RESET-RTD3 -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">75.</span>HMB is not persistent in the controller across Controller Level Reset. The host should provide resources again afterward. MR one returns prior contents and requires the exact same size, descriptor-list address, descriptor-list contents, and HMB contents. Disable before RTD3, then select MR according to content preservation on resume.</p><details class="source-note"><summary>Sources: Base 2.4 §8.2.4</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §8.2.4, printed pages 744, PDF pages 770</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">Item</th><th scope="col">Role or distinction</th><th scope="col">Conditions</th></tr></thead><tbody><tr><td>HMNARE</td><td>Configured policy</td><td>Requires CTRATT.HMBR</td></tr><tr><td>HMNAR</td><td>Current restriction state</td><td>May be zero in operational state</td></tr><tr><td>MR=1</td><td>Return identical old HMB</td><td>Same size/address/list/content</td></tr><tr><td>MR=0</td><td>New undefined contents</td><td>Controller initializes again</td></tr></tbody></table></div>
<aside class="worked-example"><h3>Example</h3><p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">76.</span>If the allocator returns the same pages after resume but moves HMDL to a new address, MR cannot be one because the descriptor-list address must also match exactly. Enable it as a new MR-zero allocation.</p></aside>
</section>
<section class="lesson" id="module-encoded-boundary-safety"><h2 id="heading-encoded-boundary-safety"><span class="section-number">07</span> Units of DSTRD, NDT, and NDM</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">77.</span>Software emulators and vendor-command passthrough both handle untrusted encoded values. DSTRD becomes bytes through 2^(2+x); NDT/NDM are already actual dword counts and are multiplied by four without adding one. The formulas differ, but both prove address and length before MMIO or DMA.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>MMIO</dt><dd>Memory-Mapped I/O, access to device registers through CPU memory operations.</dd></div></dl>
<details class="technical-note"><summary>Mechanism and applicable conditions</summary>
<!-- claim:BASEDIAGMEM-VENDOR-FORMAT -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">78.</span>Figure 94 retains common CDW0, NSID, metadata/data pointers, and CDW12-CDW15, while defining CDW10/11 as NDT/NDM. An unused NSID is cleared to zero; an invalid NSID used by the command returns Invalid Namespace or Format, while inactive-NSID behavior remains vendor specific.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>metadata</dt><dd>Additional information stored with a logical block; it can contain protection information or serve other purposes.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §4.1.1, 8.1.29</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.1.1, 8.1.29, printed pages 143, 733, PDF pages 169, 759</p></details>
<!-- claim:BASEDIAGMEM-VENDOR-LENGTH -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">79.</span>NDT and NDM are actual dword counts, not zero based. NDT 00000100h means 256 dwords or 1024 bytes; a driver can validate application buffers with NDT/NDM to prevent data or metadata-transfer overflow. VSCF or SNVSCF still gates use of the standard format.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>metadata</dt><dd>Additional information stored with a logical block; it can contain protection information or serve other purposes.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §4.1.1, 8.1.29</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.1.1, 8.1.29, printed pages 143, 733, PDF pages 169, 759</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">Item</th><th scope="col">Role or distinction</th><th scope="col">Conditions</th></tr></thead><tbody><tr><td>DSTRD</td><td>2^(2+x) bytes</td><td>0→4 B; 4→64 B</td></tr><tr><td>NDT</td><td>Value×4 data bytes</td><td>Not zero based</td></tr><tr><td>NDM</td><td>Value×4 metadata bytes</td><td>Independent buffer bound</td></tr><tr><td>VSCF/SNVSCF</td><td>Format gate</td><td>Admin and I/O are separate</td></tr></tbody></table></div>
<aside class="worked-example"><h3>Example</h3><p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">80.</span>An emulator with DSTRD 4 gets a 64-byte stride and can place doorbells on discrete cachelines. Vendor-command NDT 0100h is 256 dwords or 1024 bytes—not 1028 bytes. Retain both raw encoding and interpret the fields bytes for each.</p></aside>
</section>
<section id="additional-details"><h2 id="further-mechanisms">Additional mechanisms and data formats</h2>
<!-- claim:BASEDIAGMEM-SELFTEST-BACKGROUND -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">81.</span>Device Self-test is background work composed of vendor-specific segments. If another command requires suspension, the controller shall suspend the self-test, process and complete that command, and then resume the self-test in order. Which commands may run concurrently remains vendor specific.</p><details class="source-note"><summary>Sources: Base 2.4 §8.1.8</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §8.1.8, printed pages 614, PDF pages 640</p></details>
<!-- claim:BASEDIAGMEM-SELFTEST-TIMING -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">82.</span>A short operation should finish within two minutes and is aborted by a Controller Level Reset. An extended operation should finish within EDSTT, shall persist across Controller Level Reset and power restoration, and resumes afterward. The two operations cannot share one reset expectation.</p><details class="source-note"><summary>Sources: Base 2.4 §8.1.8.1-8.1.8.2</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §8.1.8.1-8.1.8.2, printed pages 615-616, PDF pages 641-642</p></details>
<!-- claim:BASEDIAGMEM-SELFTEST-ABORTS -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">83.</span>Both short and extended operations are aborted by an applicable Format NVM command, sanitize start, or STC Fh, and may be aborted when the namespace is removed from inventory. Figure 701 shows that Format NSID and secure-erase selections affect whether abort is required; the opcode alone is insufficient.</p><details class="source-note"><summary>Sources: Base 2.4 §8.1.8.1-8.1.8.2</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §8.1.8.1-8.1.8.2, printed pages 615-616, PDF pages 641-642</p></details>
</section>
<section id="knowledge-check"><h2 id="review-questions">Check your understanding</h2>
<!-- qa:base-self-test-hmb-emulation-selftest-progress -->
<details class="review-question" id="qa-base-self-test-hmb-emulation-selftest-progress"><summary>1. After a successful Device Self-test start command, how can ongoing execution be determined?</summary>
<div data-qa-answer="base-self-test-hmb-emulation-selftest-progress"><p class="reader-paragraph review-answer"><span class="paragraph-number" aria-hidden="true">84.</span>The start completion is not the test’s final outcome. The Device Self-test log reports current operation and completion percentage for ongoing work, while result records describe finished tests.</p></div>
<details class="source-note"><summary>Sources</summary>
<p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.6, printed pages 201, PDF pages 227</p>
<p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.7, printed pages 229-230, PDF pages 255-256</p>
</details></details>
<!-- qa:base-self-test-hmb-emulation-flba-valid -->
<details class="review-question" id="qa-base-self-test-hmb-emulation-flba-valid"><summary>2. Can a plausible FLBA in a self-test result always be treated as the failure location?</summary>
<div data-qa-answer="base-self-test-hmb-emulation-flba-valid"><p class="reader-paragraph review-answer"><span class="paragraph-number" aria-hidden="true">85.</span>Check its validity bit first; the value cannot be interpreted if it is not marked valid. Even when valid, it may identify only one of several failed logical blocks, rather than the complete range.</p></div>
<details class="source-note"><summary>Sources</summary>
<p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.7, printed pages 231-232, PDF pages 257-258</p>
<p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §4.1.4.3, printed pages 76, PDF pages 76</p>
</details></details>
<!-- qa:base-self-test-hmb-emulation-hmb-ownership -->
<details class="review-question" id="qa-base-self-test-hmb-emulation-hmb-ownership"><summary>3. Can the host repurpose HMB memory while the controller is using it just because the host allocated it?</summary>
<div data-qa-answer="base-self-test-hmb-emulation-hmb-ownership"><p class="reader-paragraph review-answer"><span class="paragraph-number" aria-hidden="true">86.</span>No. The memory and its descriptors must remain valid while provided to the controller. Reclaim it only after the specified disable and return procedure. Allocation ownership and current permitted use are distinct.</p></div>
<details class="source-note"><summary>Sources</summary>
<p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.2.3, 8.2.4, printed pages 515-516, 744, PDF pages 541-542, 770</p>
<p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.2.3, printed pages 515-516, PDF pages 541-542</p>
</details></details>
<!-- qa:base-self-test-hmb-emulation-hmb-size -->
<details class="review-question" id="qa-base-self-test-hmb-emulation-hmb-size"><summary>4. Does knowing that HMB has four descriptors establish its total capacity?</summary>
<div data-qa-answer="base-self-test-hmb-emulation-hmb-size"><p class="reader-paragraph review-answer"><span class="paragraph-number" aria-hidden="true">87.</span>Each buffer size and the page size are also needed. Descriptor count measures segments; total capacity is the sum of segment page counts multiplied by page size, subject to HSIZE and capability limits.</p></div>
<details class="source-note"><summary>Sources</summary>
<p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.2.3, printed pages 517-518, PDF pages 543-544</p>
<p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.2.3, printed pages 516-518, PDF pages 542-544</p>
</details></details>
</section>
<footer class="reference-editions"><details class="source-note"><summary>Specification editions</summary><p>NVM Express Base Specification, Revision 2.4</p><p>NVM Express NVM Command Set Specification, Revision 1.3</p></details></footer>
</div>
