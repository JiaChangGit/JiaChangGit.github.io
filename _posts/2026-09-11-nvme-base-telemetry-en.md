---
permalink: /nvme/telemetry-en/
layout: post
read_time: true
show_date: true
title: "NVMe Base 2.4: Telemetry: capture and consistent retrieval"
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
[繁體中文]({% post_url 2026-09-11-nvme-base-telemetry-zh-tw %})


<div class="nvme-note">
<section id="topic-overview" class="topic-overview">
<p class="reader-paragraph opening"><span class="paragraph-number" aria-label="00.01">00.01.</span><span class="paragraph-text">Telemetry exposes collected internal state as host-readable logs. The goal is a complete, consistent capture: who creates it, how large each area is, and whether it changes during segmented retrieval.</span></p><dl class="term-note" aria-label="Terms in this passage"><div><dt>Host</dt><dd>The system running the operating system and issuing NVMe commands.</dd></div></dl>
<h2 id="main-ideas">The main ideas</h2>
<div class="topic-map">
<article><span class="axis-number">01</span><h3>Establish who created the capture</h3><p class="axis-paragraph"><span class="axis-paragraph-number" aria-label="01-01">01-01</span><span class="paragraph-text">Host-initiated and controller-initiated logs have different creation and acknowledgment rules.</span></p><dl class="term-note" aria-label="Terms in this passage"><div><dt>controller</dt><dd>Controller, the entity that implements the NVMe interface, fetches commands, and reports completions.</dd></div></dl></article>
<article><span class="axis-number">02</span><h3>Use the header to find the data</h3><p class="axis-paragraph"><span class="axis-paragraph-number" aria-label="02-01">02-01</span><span class="paragraph-text">Read the header and area boundaries to plan retrieval. Standardized locations and vendor-specific payload formats answer different questions.</span></p></article>
<article><span class="axis-number">03</span><h3>Keep segmented reads consistent</h3><p class="axis-paragraph"><span class="axis-paragraph-number" aria-label="03-01">03-01</span><span class="paragraph-text">Check capture identity and change information so that multiple reads do not combine data from different captures.</span></p></article>
</div>
<div class="overview-connections"><h3>Connecting the main ideas</h3>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="00.02">00.02.</span><span class="paragraph-text">Distinguish host-initiated and controller-initiated logs, then use the header to establish area boundaries. Preserve capture identity across reads and acknowledge retrieval according to that log’s rules. Standardized locations do not define the contents of vendor-specific payloads.</span></p>
</div>
</section>
<section class="lesson" id="module-telemetry-layout"><h2 id="heading-telemetry-layout"><span class="section-number">01</span> Computing snapshots from Last Block</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="01.01">01.01.</span><span class="paragraph-text">Areas are differently sized views starting at the same block 1. Read the fields the header, select the final applicable populated area, and do not add the three Last Block numbers.</span></p>
<figure><div class="diagram-scroll"><svg viewBox="0 0 760 260" role="img"><title>Telemetry Data Areas are cumulative</title><desc>The header occupies block 0. Each Data Area starts at block 1, and larger areas include the data in smaller areas.</desc><rect x="20" y="20" width="155" height="210" rx="6" class="v-command"/><text x="97.5" y="118.5" text-anchor="middle" font-size="17">Header</text><text x="97.5" y="143.5" text-anchor="middle" font-size="17">Block 0</text><rect x="205" y="20" width="160" height="55" rx="6" class="v-object"/><text x="285.0" y="53.5" text-anchor="middle" font-size="17">Area 1</text><rect x="205" y="95" width="325" height="55" rx="6" class="v-decision"/><text x="367.5" y="128.5" text-anchor="middle" font-size="17">Area 2</text><rect x="205" y="170" width="535" height="55" rx="6" class="v-success"/><text x="472.5" y="203.5" text-anchor="middle" font-size="17">Area 3</text></svg></div><figcaption>The header occupies block 0. Each Data Area starts at block 1, and larger areas include the data in smaller areas.</figcaption></figure>

<!-- claim:BASETELEMETRY-TEL-MODEL -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="01.02">01.02.</span><span class="paragraph-text">Telemetry uses block 0 for its header and 512-byte blocks. Every Data Area begins at block 1. Areas 2/3/4 are larger cumulative sets, not disjoint regions placed after Area 1. Last Block is an inclusive block number; payload format and size are vendor-defined.</span></p><details class="source-note"><summary>Sources: Base 2.4 §8.1.30; 5.2.13.1.8-5.2.13.1.9</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §8.1.30; 5.2.13.1.8-5.2.13.1.9, printed pages 232-237,733-737, PDF pages 258-263,759-763</p></details>
<div class="table-wrap"><table><caption>Computing snapshots from Last Block</caption><thead><tr><th scope="col">Data area</th><th scope="col">Included blocks</th><th scope="col">Last Block constraints</th></tr></thead><tbody><tr><td>Area 1</td><td>1 through L1</td><td>L1=0 means no data</td></tr><tr><td>Area 2</td><td>1 through L2</td><td>L2 &gt;= L1</td></tr><tr><td>Area 3</td><td>1 through L3</td><td>L3 &gt;= L2</td></tr><tr><td>Area 4</td><td>1 through L4</td><td>Check support separately</td></tr></tbody></table></div>
<aside class="worked-example"><h3>Illustrative example</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="01.03">01.03.</span><span class="paragraph-text">For Last Blocks=65/1000/30000, Area 3 payload is 30000×512=15360000 bytes and the log including its header is 15360512 bytes. Values 0/1000/1000 mean Area 1 is empty and Area 3 adds no content beyond Area 2.</span></p></aside>
</section>
<section class="lesson" id="module-telemetry-capture"><h2 id="heading-telemetry-capture"><span class="section-number">02</span> Snapshot creation, chunked reads, and acknowledgement</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="02.01">02.01.</span><span class="paragraph-text">Separate creating 07h data from subsequent reads; the controller decides 08h capture timing. For both, verify generation and distinguish event acknowledgement from payload deletion.</span></p>
<figure><figcaption><strong>Keep segmented reads on one snapshot</strong></figcaption><ol class="flow-steps"><li>Read the header and save its generation number.</li><li>Read the data in segments from the same snapshot.</li><li>Read the header again and compare generation numbers.</li><li>Treat the segments as one snapshot only when the generations match.</li></ol><figcaption>The generation number identifies a data version; creating a snapshot and reading an existing snapshot are different operations.</figcaption></figure>

<!-- claim:BASETELEMETRY-TEL-CREATE -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="02.02">02.02.</span><span class="paragraph-text">CTHID for LID 07h is CDW10 bit 8: one requests a new capture and zero does not update that snapshot. MCDA occupies bits 11:9 and applies only when MCDAS=1 and CTHID=1; 001b through 100b request creation through Areas 1 through 4, while 000b lets the controller decide. MCDAS comes from the LID Specific Parameter in Supported Log Pages.</span></p><dl class="term-note" aria-label="Terms in this passage"><div><dt>CTHID</dt><dd>Create Telemetry Host-Initiated Data; the 07h capture request, cleared for subsequent reads of that snapshot.</dd></div><div><dt>MCDAS</dt><dd>Maximum Created Data Area Supported; bit 0 of the 07h LID Specific Parameter, advertising MCDA support.</dd></div><div><dt>MCDA</dt><dd>Maximum Created Data Area; selects the largest area to create when supported and capture is requested.</dd></div><div><dt>CDW</dt><dd>CDW (Command Dword): a 32-bit command field. In CDW10, 10 is the field index, not a byte offset.</dd></div><div><dt>LID</dt><dd>Log Page Identifier: selects the type of log page to read.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §5.2.13.1.8</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.8, printed pages 232-235, PDF pages 258-261</p></details>
<div class="table-wrap"><table><caption>Snapshot creation, chunked reads, and acknowledgement</caption><thead><tr><th scope="col">Snapshot-control field</th><th scope="col">Action or report</th><th scope="col">Consideration during chunked reads</th></tr></thead><tbody><tr><td>CTHID=1</td><td>Triggers a new 07h capture</td><td>Do not create again for subsequent chunks</td></tr><tr><td>MCDA</td><td>Limits the areas created</td><td>Check MCDAS first</td></tr><tr><td>RAE=1</td><td>Retains the event</td><td>Does not exclude another reader</td></tr><tr><td>TCDA=0</td><td>No update since acknowledgement</td><td>In 2.4 it does not mean payload disappearance</td></tr></tbody></table></div><dl class="term-note" aria-label="Terms in this passage"><div><dt>TCDA</dt><dd>Telemetry Controller-Initiated Data Available; in 2.4, indicates an update since the last RAE=0 acknowledgement.</dd></div><div><dt>RAE</dt><dd>Retain Asynchronous Event; use one during Telemetry collection and zero to acknowledge completion.</dd></div></dl>
<aside class="worked-example"><h3>Illustrative example</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="02.03">02.03.</span><span class="paragraph-text">If generation is 2Ah before reading and 2Bh afterward, the chunks cannot be accepted as one consistent capture. Even if it remains 2Ah, an 08h collection must consider the race where another host clears TCDA to zero.</span></p></aside>
</section>
<section id="spec-reading"><h2>Where to continue in the specification</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="03.01">03.01.</span><span class="paragraph-text">Use the flow above to frame the problem, then open the corresponding sections for fields and full conditions. The Chinese tutorial also explains every in-scope figure with its takeaway, example, and details.</span></p>
<div class="table-wrap"><table><thead><tr><th scope="col">Concept to explain</th><th scope="col">Specification sections</th></tr></thead><tbody><tr><td>Computing snapshots from Last Block</td><td>Base 2.4 §8.1.30; 5.2.13.1.8-5.2.13.1.9 · Base 2.4 §8.1.30; 5.2.30.1.15 · Base 2.4 §5.2.13.1.8-5.2.13.1.9</td></tr><tr><td>Snapshot creation, chunked reads, and acknowledgement</td><td>Base 2.4 §5.2.13.1.8 · Base 2.4 §8.1.30 · Base 2.4 §5.2.13.1.9 · Base 2.4 §5.2.13.1.8-5.2.13.1.9 · Base 2.4 §8.1.30; 5.2.30.1.6</td></tr></tbody></table></div>
<a class="reading-link" href="/DOCS/nvme-spec-report/base-telemetry/tutorial-zh-tw.html">Open the complete Chinese tutorial and figure explanations →</a></section>
<section id="knowledge-check"><h2 id="review-questions">Check your understanding</h2>
<!-- qa:base-telemetry-1 -->
<details class="review-question" id="qa-base-telemetry-1"><summary>1. If Area 1 Last Block is 3 and Area 2 Last Block is 7, which payload blocks belong to Area 2?</summary>
<div data-qa-answer="base-telemetry-1"><p class="reader-paragraph review-answer"><span class="paragraph-number" aria-label="04.01">04.01.</span><span class="paragraph-text">Area 2 contains blocks 1 through 7, totaling 7×512=3584 bytes, including Area 1 blocks 1 through 3. The header is block 0 and occupies another 512 bytes. Last Block is inclusive.</span></p></div>
<details class="source-note"><summary>Sources</summary>
<p>Source: NVME-BASE-2.4, Rev. 2.4, §8.1.30; 5.2.13.1.8-5.2.13.1.9, printed pages 232-237,733-737, PDF pages 258-263,759-763</p>
</details></details>
<!-- qa:base-telemetry-2 -->
<details class="review-question" id="qa-base-telemetry-2"><summary>2. Why reread the Telemetry header after collecting its data in chunks?</summary>
<div data-qa-answer="base-telemetry-2"><p class="reader-paragraph review-answer"><span class="paragraph-number" aria-label="04.02">04.02.</span><span class="paragraph-text">A new snapshot generation may appear during collection. Rereading generation checks that the chunks still belong together; a change requires recollection. For controller-initiated data, also check TCDA to account for acknowledgement by another reader.</span></p></div>
<details class="source-note"><summary>Sources</summary>
<p>Source: NVME-BASE-2.4, Rev. 2.4, §8.1.30, printed pages 734-735, PDF pages 760-761</p>
<p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.9, printed pages 237, PDF pages 263</p>
</details></details>
</section>
<footer class="reference-editions"><details class="source-note"><summary>Specification editions</summary><p>NVM Express Base Specification, Revision 2.4</p></details></footer>
</div>
