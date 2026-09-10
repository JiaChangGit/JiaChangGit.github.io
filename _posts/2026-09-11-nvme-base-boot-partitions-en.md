---
permalink: /nvme/boot-partitions-en/
layout: post
read_time: true
show_date: true
title: "NVMe Base 2.4: Boot Partitions: reading, updating, and write protection"
date: 2026-09-11
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
[繁體中文]({% post_url 2026-09-11-nvme-base-boot-partitions-zh-tw %})


<div class="nvme-note">
<section id="topic-overview" class="topic-overview">
<p class="reader-paragraph opening"><span class="paragraph-number" aria-label="00.01">00.01.</span><span class="paragraph-text">Boot Partitions store boot images. Start with how a host retrieves boot data before normal I/O queues exist, then follow image updates, active-partition selection, and write protection.</span></p><dl class="term-note" aria-label="Terms in this passage"><div><dt>Host</dt><dd>The system running the operating system and issuing NVMe commands.</dd></div><div><dt>I/O</dt><dd>Input/Output, the class of data operations performed on a namespace.</dd></div></dl>
<h2 id="main-ideas">The main ideas</h2>
<div class="topic-map">
<article><span class="axis-number">01</span><h3>Retrieve a boot image</h3><p class="axis-paragraph"><span class="axis-paragraph-number" aria-label="01-01">01-01</span><span class="paragraph-text">Follow partition selection, range selection, and transfer into host memory as one boot-read workflow.</span></p></article>
<article><span class="axis-number">02</span><h3>Update and activate an image</h3><p class="axis-paragraph"><span class="axis-paragraph-number" aria-label="02-01">02-01</span><span class="paragraph-text">Separate transferring a new image, replacing partition contents, and selecting the active partition.</span></p></article>
<article><span class="axis-number">03</span><h3>Protect written contents</h3><p class="axis-paragraph"><span class="axis-paragraph-number" aria-label="03-01">03-01</span><span class="paragraph-text">Compare write-protection states and the restrictions that persist across resets or power loss.</span></p></article>
</div>
<div class="overview-connections"><h3>Connecting the main ideas</h3>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="00.02">00.02.</span><span class="paragraph-text">Reading selects a partition and range and supplies host destination memory. Updating separates image transfer, replacement, and active-partition selection. Write protection constrains updates; its persistence depends on the reset or power condition.</span></p>
</div>
</section>
<section class="lesson" id="module-boot-read"><h2 id="heading-boot-read"><span class="section-number">01</span> Two Boot read paths</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="01.01">01.01.</span><span class="paragraph-text">First determine whether an Admin-command environment exists, then choose properties or LID 15h. Both access boot contents, but their return formats and observation points differ.</span></p><dl class="term-note" aria-label="Terms in this passage"><div><dt>Admin</dt><dd>Administrative, the control path used to create, configure, query, or manage controllers and queues.</dd></div><div><dt>LID</dt><dd>Log Page Identifier: selects the type of log page to read.</dd></div></dl>
<!-- claim:BASEBOOT-BOOT-MODEL -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="01.02">01.02.</span><span class="paragraph-text">Boot Partitions are optional; support provides two equally sized partitions with IDs 0h and 1h. A host can read through properties without creating queues or enabling the controller.</span></p><dl class="term-note" aria-label="Terms in this passage"><div><dt>controller</dt><dd>Controller, the entity that implements the NVMe interface, fetches commands, and reports completions.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §8.1.3</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §8.1.3, printed pages 586, PDF pages 612</p></details>
<div class="table-wrap"><table><caption>Two Boot read paths</caption><thead><tr><th scope="col">Read path or field</th><th scope="col">Where data or status is obtained</th><th scope="col">Operating context and unit</th></tr></thead><tbody><tr><td>Properties</td><td>BRS reports read state</td><td>Does not require CC.EN=1</td></tr><tr><td>LID 15h</td><td>16-byte header + data</td><td>The Admin-command CQE reports the command result</td></tr><tr><td>BPID</td><td>Selects the partition to read</td><td>Not the active ID</td></tr><tr><td>BPSZ</td><td>128 KiB per unit</td><td>Not a byte count</td></tr></tbody></table></div><dl class="term-note" aria-label="Terms in this passage"><div><dt>BPID</dt><dd>Boot Partition Identifier; selects 0 or 1 independently of the active partition.</dd></div><div><dt>BPSZ</dt><dd>Boot Partition Size; each unit is 128 KiB.</dd></div><div><dt>BRS</dt><dd>Boot Read Status: 00b no request, 01b in progress, 10b success, 11b error.</dd></div><div><dt>CQE</dt><dd>Completion Queue Entry, one completion-result structure in a CQ.</dd></div><div><dt>CC</dt><dd>Controller Configuration, the property through which the host selects settings and enables or disables a controller.</dd></div><div><dt>EN</dt><dd>Enable, the CC bit controlling controller enable state.</dd></div></dl>
<aside class="worked-example"><h3>Illustrative example</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="01.03">01.03.</span><span class="paragraph-text">With BPSZ=2, LID 15h contains 262144 bytes of boot data plus a 16-byte header, totaling 262160 bytes. Reading BP1 does not activate BP1, and a log read does not advance the property's BRS.</span></p></aside>
</section>
<section class="lesson" id="module-boot-protection"><h2 id="heading-boot-protection"><span class="section-number">02</span> The complete update and protection lifecycle</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="02.01">02.01.</span><span class="paragraph-text">Track image transfer, partition contents, active selection, and write protection separately. Successful download has not yet written a Boot Partition, and a successful write has not automatically activated it.</span></p>
<!-- claim:BASEBOOT-BOOT-UPDATE -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="02.02">02.02.</span><span class="paragraph-text">A boot image is downloaded in order from its beginning using Firmware Image Download. After unlocking the target, Firmware Commit CA=110b writes the partition selected by BPID. The host may read it back, use CA=111b to change the active ID, and relock it. An interrupted update can leave mixed old/new contents, so verification before activation is recommended.</span></p><dl class="term-note" aria-label="Terms in this passage"><div><dt>CA</dt><dd>Commit Action, the Firmware Commit field selecting replacement, activation, and reset policy.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §8.1.3.2</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §8.1.3.2, printed pages 587-588, PDF pages 613-614</p></details>
<div class="table-wrap"><table><caption>The complete update and protection lifecycle</caption><thead><tr><th scope="col">Protection mechanism and state</th><th scope="col">Operations changing it</th><th scope="col">Result of reset or power cycling</th></tr></thead><tbody><tr><td>FID 85h unlocked</td><td>Survives controller reset</td><td>Locked after power cycle</td></tr><tr><td>FID 85h until power cycle</td><td>Ordinary Set cannot unlock</td><td>Unavailable for shared multi-domain partitions</td></tr><tr><td>RPMB enabled/unlocked</td><td>Controller reset relocks</td><td>Protection enablement cannot be reversed</td></tr><tr><td>Both mechanisms</td><td>Only one owns control at a time</td><td>RPMB enablement transfers ownership</td></tr></tbody></table></div><dl class="term-note" aria-label="Terms in this passage"><div><dt>FID</dt><dd>Feature Identifier: selects the Feature to read or configure.</dd></div></dl>
<aside class="worked-example"><h3>Illustrative example</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="02.03">02.03.</span><span class="paragraph-text">To leave BP0 unchanged and unlock BP1, FID 85h CDW11 is (001b &lt;&lt; 3) | 000b = 08h. A subsequent Get does not return 000b for BP0; it returns its actual state, or 100b when RPMB owns protection.</span></p><dl class="term-note" aria-label="Terms in this passage"><div><dt>CDW</dt><dd>CDW (Command Dword): a 32-bit command field. In CDW10, 10 is the field index, not a byte offset.</dd></div></dl></aside>
</section>
<section id="spec-reading"><h2>Where to continue in the specification</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="03.01">03.01.</span><span class="paragraph-text">Use the flow above to frame the problem, then open the corresponding sections for fields and full conditions. The Chinese tutorial also explains every in-scope figure with its takeaway, example, and details.</span></p>
<div class="table-wrap"><table><thead><tr><th scope="col">Concept to explain</th><th scope="col">Specification sections</th></tr></thead><tbody><tr><td>Two Boot read paths</td><td>Base 2.4 §8.1.3 · Base 2.4 §8.1.3.1 · Base 2.4 §5.2.13.1.21</td></tr><tr><td>The complete update and protection lifecycle</td><td>Base 2.4 §8.1.3.2 · Base 2.4 §8.1.3.3 · Base 2.4 §5.2.30.1.39 · Base 2.4 §8.1.3.3.1-8.1.3.3.3 · Base 2.4 §5.2.30.1.39; 8.1.3.3.3</td></tr></tbody></table></div>
<a class="reading-link" href="/DOCS/nvme-spec-report/base-boot-partitions/tutorial-zh-tw.html">Open the complete Chinese tutorial and figure explanations →</a></section>
<section id="knowledge-check"><h2 id="review-questions">Check your understanding</h2>
<!-- qa:base-boot-partitions-1 -->
<details class="review-question" id="qa-base-boot-partitions-1"><summary>1. Does writing a new boot image to a partition also change the active partition?</summary>
<div data-qa-answer="base-boot-partitions-1"><p class="reader-paragraph review-answer"><span class="paragraph-number" aria-label="04.01">04.01.</span><span class="paragraph-text">Writing and selecting the active ID are separate actions. CA=110b writes the selected partition; after an optional readback, CA=111b selects the active ID. This separation allows checking the image before switching.</span></p></div>
<details class="source-note"><summary>Sources</summary>
<p>Source: NVME-BASE-2.4, Rev. 2.4, §8.1.3.2, printed pages 587-588, PDF pages 613-614</p>
<p>Source: NVME-BASE-2.4, Rev. 2.4, §8.1.3, printed pages 586, PDF pages 612</p>
</details></details>
<!-- qa:base-boot-partitions-2 -->
<details class="review-question" id="qa-base-boot-partitions-2"><summary>2. Must a Controller Level Reset relock an unlocked Boot Partition?</summary>
<div data-qa-answer="base-boot-partitions-2"><p class="reader-paragraph review-answer"><span class="paragraph-number" aria-label="04.02">04.02.</span><span class="paragraph-text">First identify the controlling mechanism. The Set Features unlocked state survives this reset but a power cycle relocks it. With RPMB protection enabled, either event relocks it.</span></p></div>
<details class="source-note"><summary>Sources</summary>
<p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.39, printed pages 513-514, PDF pages 539-540</p>
<p>Source: NVME-BASE-2.4, Rev. 2.4, §8.1.3.3.1-8.1.3.3.3, printed pages 589-594, PDF pages 615-620</p>
</details></details>
</section>
<footer class="reference-editions"><details class="source-note"><summary>Specification editions</summary><p>NVM Express Base Specification, Revision 2.4</p></details></footer>
</div>
