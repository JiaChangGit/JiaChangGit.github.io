---
layout: post
read_time: true
show_date: true
title: "NVMe Base 2.4: Power/Thermal Features and Power Management"
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
[繁體中文]({% post_url 2026-09-02-nvme-base-power-thermal-features-zh-tw %})


<div class="nvme-note">
<section id="topic-overview" class="topic-overview">
<p class="opening">NVMe power and temperature management involve tradeoffs among energy use, response latency, and operating capability. This note establishes the meaning of a power state, then explains host settings, automatic idle transitions, and temperature controls.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>NVMe</dt><dd>Non-Volatile Memory Express, the specification family for a host interface to a non-volatile-memory subsystem.</dd></div></dl>
<h2 id="main-ideas">The main ideas</h2>
<div class="topic-map">
<article><span class="axis-number">01</span><h3>Power states</h3><p>Compare power, I/O capability, and entry/exit latency.</p></article>
<article><span class="axis-number">02</span><h3>Settings and automatic transitions</h3><p>Understand Get/Set Features, APST, and limits on background work.</p></article>
<article><span class="axis-number">03</span><h3>Temperature control</h3><p>Distinguish temperature-event notification from thermal-management behavior.</p></article>
</div>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>APST</dt><dd>Autonomous Power State Transition, the mechanism for controller-directed entry into non-operational states based on idle timers.</dd></div><div><dt>I/O</dt><dd>Input/Output, the class of data operations performed on a namespace.</dd></div></dl>
<p>Features are controller functions the host can query or configure. Support, the current value, and persistence across power loss are distinct properties.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>controller</dt><dd>Controller, the entity that implements the NVMe interface, fetches commands, and reports completions.</dd></div></dl>
</section>
<section class="lesson" id="module-feature-read-set-loop"><h2 id="heading-feature-read-set-loop"><span class="section-number">01</span> Feature capabilities, reads, and settings</h2>
<p>A Feature is not a simple register. The host first reads capability with SEL=011b, then retrieves current/default/saved views, confirms scope and persistence, and only then writes. Set completion proves command outcome; a follow-up Get and runtime telemetry prove that software observes the new policy.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>SEL</dt><dd>Select, the Get Features field choosing current, default, saved, or supported-capabilities view.</dd></div></dl>
<details class="technical-note"><summary>Mechanism and applicable conditions</summary>
<!-- claim:BASEPOWER-READ-FIRST -->
<p>Get Features is the Admin command that retrieves Feature attributes. An engineering flow starts by identifying the FID, querying capability, and retrieving current/default/saved values instead of guessing before a write.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>Admin</dt><dd>Administrative, the control path used to create, configure, query, or manage controllers and queues.</dd></div><div><dt>FID</dt><dd>Feature Identifier, the eight-bit identifier selecting a function in Get/Set Features.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §5.2.12</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.12, printed pages 209, PDF pages 235</p></details>
<!-- claim:BASEPOWER-GET-SELECT -->
<p>CDW10.SEL selects current=000b, default=001b, saved=010b, or supported capabilities=011b; CDW10.FID selects the Feature. Other SEL encodings are reserved.</p><details class="source-note"><summary>Sources: Base 2.4 §5.2.12</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.12, printed pages 209-210, PDF pages 235-236</p></details>
<!-- claim:BASEPOWER-GET-CAP -->
<p>With SEL=011b, CQE.DW0 reports CHANG, NSSPEC, and SVBL: changeable, namespace-specific, and saveable. These capability bits are distinct from the Feature value and must not be decoded as one.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>namespace</dt><dd>Namespace, a formatted quantity of non-volatile memory accessed by a host through a controller.</dd></div><div><dt>NSSPEC</dt><dd>Namespace Specific, the capability bit indicating whether a Feature has per-namespace scope.</dd></div><div><dt>CHANG</dt><dd>Changeable, the capability bit indicating whether Set Features can modify the Feature value.</dd></div><div><dt>SVBL</dt><dd>Saveable, the supported-capabilities bit indicating whether a Feature can be saved.</dd></div><div><dt>CQE</dt><dd>Completion Queue Entry, one completion-result structure in a CQ.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §5.2.12.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.12.1, printed pages 211-212, PDF pages 237-238</p></details>
<!-- claim:BASEPOWER-SET-SAVE -->
<p>CDW10.SV=1 requests a saved value that can persist across reset/power-cycle boundaries. If the Feature is not saveable, the controller returns Feature Identifier Not Saveable. Read SVBL before setting SV.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>SV</dt><dd>Save, the Set Features bit requesting that the controller also save the configured value.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §5.2.30</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30, printed pages 457, PDF pages 483</p></details>
<!-- claim:BASEPOWER-SET-AFTER -->
<p>After Set Features succeeds, subsequent commands shall use the new setting. If software needs a batch of commands to use one consistent setting, the host should allow existing in-flight commands to complete before switching.</p><details class="source-note"><summary>Sources: Base 2.4 §5.2.30</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30, printed pages 459, PDF pages 485</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">Item</th><th scope="col">Role or distinction</th><th scope="col">Conditions</th></tr></thead><tbody><tr><td>SEL=000b</td><td>Current value</td><td>Observe current controller policy</td></tr><tr><td>SEL=001b</td><td>Default value</td><td>Establish a rollback baseline</td></tr><tr><td>SEL=010b</td><td>Saved value</td><td>Does not prove a value was saved</td></tr><tr><td>SEL=011b</td><td>CHANG/NSSPEC/SVBL</td><td>Capability gate before writing</td></tr></tbody></table></div><dl class="term-note" aria-label="Terms in this passage"><div><dt>NSSPEC</dt><dd>Namespace Specific, the capability bit indicating whether a Feature has per-namespace scope.</dd></div><div><dt>CHANG</dt><dd>Changeable, the capability bit indicating whether Set Features can modify the Feature value.</dd></div><div><dt>SVBL</dt><dd>Saveable, the supported-capabilities bit indicating whether a Feature can be saved.</dd></div></dl>
<aside class="worked-example"><h3>Example</h3><p>For FID 02h current, CDW10=00000002h. For supported capabilities, SEL=3 so CDW10=(3×100h)+02h=00000302h. If CHANG=0, stop before Set; if CHANG=1, construct CDW11 from NPSS and the PSDs.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>NPSS</dt><dd>Number of Power States Support, the zero-based field reporting the highest supported power-state number.</dd></div><div><dt>FID</dt><dd>Feature Identifier, the eight-bit identifier selecting a function in Get/Set Features.</dd></div></dl></aside>
<details class="technical-note"><summary>Fields and data structures in more depth</summary>
<!-- figure-table:BASEPOWER-FIG-197 -->
<details class="field-note" id="figure-BASEPOWER-FIG-197"><summary>Base Figure 197 · Get Features – Data Pointer</summary>
<!-- claim:BASEPOWER-FIG-197-CLAIM -->
<p>Figure 197, "Get Features – Data Pointer": Maps the power/thermal control relationship represented by Get Features – Data Pointer.</p><details class="source-note"><summary>Sources: Base 2.4 §5.2.12</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.12, Figure 197, printed pages 209, PDF pages 235</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>DPTR</dt><dd>Data Pointer, the SQE field identifying a command data buffer.</dd></div></dl>
</details>
<!-- figure-table:BASEPOWER-FIG-198 -->
<details class="field-note" id="figure-BASEPOWER-FIG-198"><summary>Base Figure 198 · Get Features – Command Dword 10</summary>
<!-- claim:BASEPOWER-FIG-198-CLAIM -->
<p>Figure 198, "Get Features – Command Dword 10": Defines the concrete layout or value relationships for Get Features – Command Dword 10.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>Dword</dt><dd>Double word, four bytes or 32 bits; NVMe command fields are commonly identified by CDW number.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §5.2.12</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.12, Figure 198, printed pages 209-210, PDF pages 235-236</p></details>

</details>
<!-- figure-table:BASEPOWER-FIG-199 -->
<details class="field-note" id="figure-BASEPOWER-FIG-199"><summary>Base Figure 199 · Get Features – Command Dword 14</summary>
<!-- claim:BASEPOWER-FIG-199-CLAIM -->
<p>Figure 199, "Get Features – Command Dword 14": Defines the concrete layout or value relationships for Get Features – Command Dword 14.</p><details class="source-note"><summary>Sources: Base 2.4 §5.2.12</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.12, Figure 199, printed pages 210, PDF pages 236</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>UIDX</dt><dd>UUID Index, an index into the UUID List; zero indicates that no UUID is specified.</dd></div></dl>
</details>
<!-- figure-table:BASEPOWER-FIG-200 -->
<details class="field-note" id="figure-BASEPOWER-FIG-200"><summary>Base Figure 200 · Feature Identifiers for Get Features</summary>
<!-- claim:BASEPOWER-FIG-200-CLAIM -->
<p>Figure 200, "Feature Identifiers for Get Features": Defines the identifier composition or namespace of values shown by Feature Identifiers for Get Features.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>namespace</dt><dd>Namespace, a formatted quantity of non-volatile memory accessed by a host through a controller.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §5.2.12</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.12, Figure 200, printed pages 210-211, PDF pages 236-237</p></details>

</details>
<!-- figure-table:BASEPOWER-FIG-201 -->
<details class="field-note" id="figure-BASEPOWER-FIG-201"><summary>Base Figure 201 · Get Features – Select Supported Capabilities</summary>
<!-- claim:BASEPOWER-FIG-201-CLAIM -->
<p>Figure 201, "Get Features – Select Supported Capabilities": Defines the concrete layout or value relationships for Get Features – Select Supported Capabilities.</p><details class="source-note"><summary>Sources: Base 2.4 §5.2.12.2</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.12.2, Figure 201, printed pages 212, PDF pages 238</p></details>

</details>
<!-- figure-table:BASEPOWER-FIG-202 -->
<details class="field-note" id="figure-BASEPOWER-FIG-202"><summary>Base Figure 202 · Get Features – Command Specific Status Values</summary>
<!-- claim:BASEPOWER-FIG-202-CLAIM -->
<p>Figure 202, "Get Features – Command Specific Status Values": Defines the concrete layout or value relationships for Get Features – Command Specific Status Values.</p><details class="source-note"><summary>Sources: Base 2.4 §5.2.12.2</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.12.2, Figure 202, printed pages 212, PDF pages 238</p></details>

</details>
<!-- figure-table:BASEPOWER-FIG-463 -->
<details class="field-note" id="figure-BASEPOWER-FIG-463"><summary>Base Figure 463 · Set Features – Data Pointer</summary>
<!-- claim:BASEPOWER-FIG-463-CLAIM -->
<p>Figure 463, "Set Features – Data Pointer": Maps the power/thermal control relationship represented by Set Features – Data Pointer.</p><details class="source-note"><summary>Sources: Base 2.4 §5.2.30</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30, Figure 463, printed pages 456, PDF pages 482</p></details>

</details>
<!-- figure-table:BASEPOWER-FIG-464 -->
<details class="field-note" id="figure-BASEPOWER-FIG-464"><summary>Base Figure 464 · Set Features – Command Dword 10</summary>
<!-- claim:BASEPOWER-FIG-464-CLAIM -->
<p>Figure 464, "Set Features – Command Dword 10": Defines the concrete layout or value relationships for Set Features – Command Dword 10.</p><details class="source-note"><summary>Sources: Base 2.4 §5.2.30</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30, Figure 464, printed pages 457, PDF pages 483</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>SV</dt><dd>Save, the Set Features bit requesting that the controller also save the configured value.</dd></div></dl>
</details>
<!-- figure-table:BASEPOWER-FIG-465 -->
<details class="field-note" id="figure-BASEPOWER-FIG-465"><summary>Base Figure 465 · Set Features – Command Dword 14</summary>
<!-- claim:BASEPOWER-FIG-465-CLAIM -->
<p>Figure 465, "Set Features – Command Dword 14": Defines the concrete layout or value relationships for Set Features – Command Dword 14.</p><details class="source-note"><summary>Sources: Base 2.4 §5.2.30</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30, Figure 465, printed pages 457, PDF pages 483</p></details>

</details>
<!-- figure-table:BASEPOWER-FIG-466 -->
<details class="field-note" id="figure-BASEPOWER-FIG-466"><summary>Base Figure 466 · Feature Identifiers for Set Features</summary>
<!-- claim:BASEPOWER-FIG-466-CLAIM -->
<p>Figure 466, "Feature Identifiers for Set Features": Defines the identifier composition or namespace of values shown by Feature Identifiers for Set Features.</p><details class="source-note"><summary>Sources: Base 2.4 §5.2.30</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30, Figure 466, printed pages 457-459, PDF pages 483-485</p></details>

</details>
<!-- figure-table:BASEPOWER-FIG-093 -->
<details class="field-note" id="figure-BASEPOWER-FIG-093"><summary>Base Figure 93 · Common Command Format</summary>
<!-- claim:BASEPOWER-FIG-093-CLAIM -->
<p>Figure 93, "Common Command Format": Defines the concrete layout or value relationships for Common Command Format.</p><details class="source-note"><summary>Sources: Base 2.4 §4.1.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.1.1, Figure 93, printed pages 140-142, PDF pages 166-168</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>MPTR</dt><dd>Metadata Pointer, the SQE field identifying a separate metadata buffer.</dd></div><div><dt>NSID</dt><dd>Namespace Identifier, a controller-visible numeric handle for a namespace; the identifier is not the namespace object itself.</dd></div><div><dt>CID</dt><dd>Command Identifier, used with the SQ identifier to identify an outstanding command.</dd></div></dl>
</details>
</details>
</section>
<section class="lesson" id="module-power-state-mental-model"><h2 id="heading-power-state-mental-model"><span class="section-number">02</span> Power-state power, latency, and performance</h2>
<p>A state number alone cannot establish workload suitability. Read MP, NOPS, ENLAT/EXLAT, IDLP/ACTP, and relative performance together in each PSD. Increasing PS numbers reduce maximum power monotonically, but latency and throughput do not necessarily change by a fixed ratio.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>ENLAT</dt><dd>Entry Latency, the maximum latency to enter a power state, in microseconds.</dd></div><div><dt>EXLAT</dt><dd>Exit Latency, the maximum latency to exit a power state, in microseconds.</dd></div><div><dt>ACTP</dt><dd>Active Power, average active power under the specified workload and time window.</dd></div><div><dt>IDLP</dt><dd>Idle Power, typical power under the specification's idle measurement conditions.</dd></div><div><dt>NOPS</dt><dd>Non-Operational State, the PSD bit indicating that the state does not process I/O commands.</dd></div><div><dt>PSD</dt><dd>Power State Descriptor, the structure describing power, latency, operational type, and relative performance for one power state.</dd></div><div><dt>MP</dt><dd>Maximum Power, the sustained maximum power of a power state.</dd></div><div><dt>PS</dt><dd>Power State, a controller power/performance operating point; PS0 has the highest maximum power.</dd></div></dl>
<details class="technical-note"><summary>Mechanism and applicable conditions</summary>
<!-- claim:BASEPOWER-POWER-STATES -->
<p>A controller shall support at least one power state and may support up to 32, numbered contiguously from zero. PS0 has the highest maximum power; each subsequent state's maximum power does not exceed the preceding state.</p><details class="source-note"><summary>Sources: Base 2.4 §8.1.19</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §8.1.19, printed pages 666-667, PDF pages 692-693</p></details>
<!-- claim:BASEPOWER-POWER-METRICS -->
<p>A Power State Descriptor (PSD) combines maximum power, operational/non-operational type, entry/exit latency, idle/active power, and relative performance. MP is a sustained maximum; IDLP and ACTP use different measurement conditions and are not interchangeable with an instantaneous sample.</p><details class="source-note"><summary>Sources: Base 2.4 §8.1.19</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §8.1.19, printed pages 666-668, PDF pages 692-694</p></details>
<!-- claim:BASEPOWER-TRANSITION -->
<p>The maximum direct-transition time from an old state to a new state is the old state's EXLAT plus the new state's ENLAT. If a controller transitions through multiple states, the transition times for every segment are summed.</p><details class="source-note"><summary>Sources: Base 2.4 §8.1.19.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §8.1.19.1, printed pages 668-669, PDF pages 694-695</p></details>
<!-- claim:BASEPOWER-RELATIVE -->
<p>Relative Read/Write Throughput and Latency use smaller-is-better encodings, but comparisons are valid only within the same characteristic. A throughput code and a latency code are not combined into one score.</p><details class="source-note"><summary>Sources: Base 2.4 §8.1.19.2</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §8.1.19.2, printed pages 668, PDF pages 694</p></details>
<!-- claim:BASEPOWER-NONOP -->
<p>A non-operational power state does not process I/O commands, but may still service properties, PMR, CMB, Admin/background work, or transport-specific accesses. Non-operational does not mean the controller is powered off.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>Admin</dt><dd>Administrative, the control path used to create, configure, query, or manage controllers and queues.</dd></div><div><dt>CMB</dt><dd>Controller Memory Buffer, controller-provided memory in which selected queues or data structures may reside.</dd></div><div><dt>PMR</dt><dd>Persistent Memory Region, a controller-exposed memory region with persistence semantics.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §8.1.19</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §8.1.19, printed pages 667-668, PDF pages 693-694</p></details>
<!-- claim:BASEPOWER-FID02 -->
<p>FID 02h uses CDW11.PS[4:0] to select a power state and WH[7:5] for a workload hint. PS shall be within the range advertised by Identify Controller.NPSS; an unsupported PS should be aborted with Invalid Field in Command.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>WH</dt><dd>Workload Hint, a host-supplied workload category hint rather than a performance guarantee.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §5.2.30.1.2</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.2, printed pages 460-461, PDF pages 486-487</p></details>
<!-- claim:BASEPOWER-WORKLOAD -->
<p>WH=000b means unknown workload; 001b represents idle, 32 random 1-MiB writes, then idle; 010b represents 80,000 sequential 128-KiB writes. Encodings 011b through 111b are reserved.</p><details class="source-note"><summary>Sources: Base 2.4 §8.1.19.3</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §8.1.19.3, printed pages 669, PDF pages 695</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">Item</th><th scope="col">Role or distinction</th><th scope="col">Conditions</th></tr></thead><tbody><tr><td>MP</td><td>Sustained maximum power</td><td>Not an instantaneous sample</td></tr><tr><td>IDLP/ACTP</td><td>Idle typical / active average</td><td>Different measurement conditions</td></tr><tr><td>ENLAT/EXLAT</td><td>Maximum entry/exit latency</td><td>Sum across transitions</td></tr><tr><td>RRT/RRL/RWT/RWL</td><td>Relative throughput/latency</td><td>Compare only like characteristics</td></tr></tbody></table></div>
<aside class="worked-example"><h3>Example</h3><p>Informative calculation: current PS1.EXLAT=100 µs and target PS3.ENLAT=2500 µs produce a direct-transition budget of 2600 µs. If the path is PS1→PS2→PS3, sum PS1.EXLAT+PS2.ENLAT and PS2.EXLAT+PS3.ENLAT instead of reusing 2600 µs.</p></aside>
<details class="technical-note"><summary>Fields and data structures in more depth</summary>
<!-- figure-table:BASEPOWER-FIG-468 -->
<details class="field-note" id="figure-BASEPOWER-FIG-468"><summary>Base Figure 468 · Power Management – Command Dword 11</summary>
<!-- claim:BASEPOWER-FIG-468-CLAIM -->
<p>Figure 468, "Power Management – Command Dword 11": Defines the concrete layout or value relationships for Power Management – Command Dword 11.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>Dword</dt><dd>Double word, four bytes or 32 bits; NVMe command fields are commonly identified by CDW number.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §5.2.30.1.2</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.2, Figure 468, printed pages 461, PDF pages 487</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>WH</dt><dd>Workload Hint, a host-supplied workload category hint rather than a performance guarantee.</dd></div></dl>
</details>
<!-- figure-table:BASEPOWER-FIG-738 -->
<details class="field-note" id="figure-BASEPOWER-FIG-738"><summary>Base Figure 738 · Power Management Overview</summary>
<!-- claim:BASEPOWER-FIG-738-CLAIM -->
<p>Figure 738, "Power Management Overview": Maps the power/thermal control relationship represented by Power Management Overview.</p><details class="source-note"><summary>Sources: Base 2.4 §8.1.19</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §8.1.19, Figure 738, printed pages 666, PDF pages 692</p></details>

</details>
<!-- figure-table:BASEPOWER-FIG-739 -->
<details class="field-note" id="figure-BASEPOWER-FIG-739"><summary>Base Figure 739 · Power State Characteristics</summary>
<!-- claim:BASEPOWER-FIG-739-CLAIM -->
<p>Figure 739, "Power State Characteristics": Shows the state or timing progression represented by Power State Characteristics.</p><details class="source-note"><summary>Sources: Base 2.4 §8.1.19</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §8.1.19, Figure 739, printed pages 667, PDF pages 693</p></details>

</details>
<!-- figure-table:BASEPOWER-FIG-740 -->
<details class="field-note" id="figure-BASEPOWER-FIG-740"><summary>Base Figure 740 · Workload Hints</summary>
<!-- claim:BASEPOWER-FIG-740-CLAIM -->
<p>Figure 740, "Workload Hints": Maps the power/thermal control relationship represented by Workload Hints.</p><details class="source-note"><summary>Sources: Base 2.4 §8.1.19.3</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §8.1.19.3, Figure 740, printed pages 669, PDF pages 695</p></details>

</details>
<!-- figure-table:BASEPOWER-FIG-338 -->
<details class="field-note" id="figure-BASEPOWER-FIG-338"><summary>Base Figure 338 · Identify Controller Data Structure</summary>
<!-- claim:BASEPOWER-FIG-338-CLAIM -->
<p>Figure 338, "Identify Controller Data Structure": Defines the concrete layout or value relationships for Identify Controller Data Structure.</p><details class="source-note"><summary>Sources: Base 2.4 §5.2.14.2.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.14.2.1, Figure 338, printed pages 340-364, PDF pages 366-390</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>WCTEMP</dt><dd>Warning Composite Temperature Threshold, the composite warning threshold reported by Identify Controller.</dd></div><div><dt>MNTMT</dt><dd>Minimum Thermal Management Temperature, the minimum Kelvin value accepted for HCTM.</dd></div><div><dt>MXTMT</dt><dd>Maximum Thermal Management Temperature, the maximum Kelvin value accepted for HCTM.</dd></div><div><dt>RTD3E</dt><dd>Runtime D3 Entry Latency, the expected time for entering a PCIe D3cold use case.</dd></div><div><dt>RTD3R</dt><dd>Runtime D3 Resume Latency, the expected time for resuming from a PCIe D3cold use case.</dd></div></dl>
</details>
<!-- figure-table:BASEPOWER-FIG-340 -->
<details class="field-note" id="figure-BASEPOWER-FIG-340"><summary>Base Figure 340 · Power State Descriptor Data Structure</summary>
<!-- claim:BASEPOWER-FIG-340-CLAIM -->
<p>Figure 340, "Power State Descriptor Data Structure": Defines the concrete layout or value relationships for Power State Descriptor Data Structure.</p><details class="source-note"><summary>Sources: Base 2.4 §5.2.14.2.2</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.14.2.2, Figure 340, printed pages 383-386, PDF pages 409-412</p></details>

</details>
</details>
</section>
<section class="lesson" id="module-apst-state-machine"><h2 id="heading-apst-state-machine"><span class="section-number">03</span> APST idle conditions and automatic transitions</h2>
<p>The 256-byte APST buffer is not a performance table. It contains 32 rules stating which non-operational state to enter after a given idle duration. APSTE enables timer rules, entries with ITPT=0 are inactive, and arriving I/O returns the controller to its most recent operational state.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>APSTE</dt><dd>Autonomous Power State Transition Enable, the bit enabling APST-table timer evaluation.</dd></div><div><dt>ITPT</dt><dd>Idle Time Prior to Transition, the APST-entry idle threshold in milliseconds.</dd></div></dl>
<figure><figcaption><strong>How idle time affects power state</strong></figcaption><ol class="flow-steps"><li>The host configures idle time ITPT and target state ITPS in APST entries.</li><li>When APST is enabled, the controller evaluates idle timers.</li><li>At the applicable threshold, it enters the selected non-operational power state.</li><li>Resuming I/O requires accounting for the exit latency of that state.</li></ol><figcaption>APST uses idle time to save power while introducing transition latency.</figcaption></figure>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>ITPS</dt><dd>Idle Transition Power State, the target non-operational power state selected by an APST entry.</dd></div></dl>
<details class="technical-note"><summary>Mechanism and applicable conditions</summary>
<!-- claim:BASEPOWER-FID0C -->
<p>FID 0Ch APSTE=1 enables Autonomous Power State Transition (APST); the default is zero. Enabling it allows controller transitions based on APST-table idle timers; it does not guarantee entry into a particular state.</p><details class="source-note"><summary>Sources: Base 2.4 §5.2.30.1.7</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.7, printed pages 468-469, PDF pages 494-495</p></details>
<!-- claim:BASEPOWER-APST-ENTRY -->
<p>The APST data structure is 256 bytes with 32 eight-byte entries. Each entry uses ITPT[31:8] as the idle threshold in milliseconds and ITPS[7:3] as the target non-operational state; ITPT=0 disables that entry.</p><details class="source-note"><summary>Sources: Base 2.4 §5.2.30.1.7</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.7, printed pages 469, PDF pages 495</p></details>
<!-- claim:BASEPOWER-APST-NOPPME -->
<p>APSTE controls timer-based entry, while NOPPME controls whether controller-initiated background operations may temporarily exceed a non-operational limit. These are orthogonal switches; autonomous state entry does not imply permission to raise power for background work.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>NOPPME</dt><dd>Non-Operational Power State Permissive Mode Enable, controlling whether controller background work may temporarily exceed a non-operational power limit.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §5.2.30.1.7</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.7, printed pages 469, PDF pages 495</p></details>
<!-- claim:BASEPOWER-NONOP-IO -->
<p>The host should drain I/O before manually entering a non-operational state. If an I/O command arrives, the controller autonomously returns to the most recently used operational state before processing I/O.</p><details class="source-note"><summary>Sources: Base 2.4 §8.1.19</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §8.1.19, printed pages 668, PDF pages 694</p></details>
<!-- claim:BASEPOWER-SET-DPTR -->
<p>Set Features uses DPTR only when the selected Feature defines a data structure. With PRPs, that data buffer shall not cross more than one memory-page boundary because PRP2 cannot point to a PRP List here.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>DPTR</dt><dd>Data Pointer, the SQE field identifying a command data buffer.</dd></div><div><dt>PRP</dt><dd>Physical Region Page, a pointer format describing a host-addressable data buffer in memory-page units.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §5.2.30</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30, printed pages 456-457, PDF pages 482-483</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">Item</th><th scope="col">Role or distinction</th><th scope="col">Conditions</th></tr></thead><tbody><tr><td>APSTE=0</td><td>Host-directed entry only</td><td>The table may exist but timers do not drive entry</td></tr><tr><td>APSTE=1</td><td>Host- or timer-directed entry</td><td>ITPT must be met continuously</td></tr><tr><td>NOPPME=0</td><td>Background work stays within non-op limits</td><td>Controller work may be deferred</td></tr><tr><td>NOPPME=1</td><td>Background work may raise power temporarily</td><td>Still capped by the last operational state</td></tr></tbody></table></div><dl class="term-note" aria-label="Terms in this passage"><div><dt>NOPPME</dt><dd>Non-Operational Power State Permissive Mode Enable, controlling whether controller background work may temporarily exceed a non-operational power limit.</dd></div></dl>
<aside class="worked-example"><h3>Example</h3><p>To enter PS3 after 2000 ms idle: ITPT=2000=07D0h, shifted into bits31:8 gives 07D00000h; ITPS=3 in bits7:3 gives 18h, so the low dword is 07D00018h. Reserved bits and the entry high dword remain zero; 32 entries total 256 bytes.</p></aside>
<details class="technical-note"><summary>Fields and data structures in more depth</summary>
<!-- figure-table:BASEPOWER-FIG-475 -->
<details class="field-note" id="figure-BASEPOWER-FIG-475"><summary>Base Figure 475 · Autonomous Power State Transition – Command Dword 11</summary>
<!-- claim:BASEPOWER-FIG-475-CLAIM -->
<p>Figure 475, "Autonomous Power State Transition – Command Dword 11": Defines the concrete layout or value relationships for Autonomous Power State Transition – Command Dword 11.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>Dword</dt><dd>Double word, four bytes or 32 bits; NVMe command fields are commonly identified by CDW number.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §5.2.30.1.7</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.7, Figure 475, printed pages 468, PDF pages 494</p></details>

</details>
<!-- figure-table:BASEPOWER-FIG-476 -->
<details class="field-note" id="figure-BASEPOWER-FIG-476"><summary>Base Figure 476 · Autonomous Power State Transition Data Structure</summary>
<!-- claim:BASEPOWER-FIG-476-CLAIM -->
<p>Figure 476, "Autonomous Power State Transition Data Structure": Defines the concrete layout or value relationships for Autonomous Power State Transition Data Structure.</p><details class="source-note"><summary>Sources: Base 2.4 §5.2.30.1.7</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.7, Figure 476, printed pages 469, PDF pages 495</p></details>

</details>
<!-- figure-table:BASEPOWER-FIG-477 -->
<details class="field-note" id="figure-BASEPOWER-FIG-477"><summary>Base Figure 477 · Autonomous Power State Transition Entry</summary>
<!-- claim:BASEPOWER-FIG-477-CLAIM -->
<p>Figure 477, "Autonomous Power State Transition Entry": Shows the state or timing progression represented by Autonomous Power State Transition Entry.</p><details class="source-note"><summary>Sources: Base 2.4 §5.2.30.1.7</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.7, Figure 477, printed pages 469, PDF pages 495</p></details>

</details>
<!-- figure-table:BASEPOWER-FIG-478 -->
<details class="field-note" id="figure-BASEPOWER-FIG-478"><summary>Base Figure 478 · APST and NOPPME Interaction</summary>
<!-- claim:BASEPOWER-FIG-478-CLAIM -->
<p>Figure 478, "APST and NOPPME Interaction": Maps the power/thermal control relationship represented by APST and NOPPME Interaction.</p><details class="source-note"><summary>Sources: Base 2.4 §5.2.30.1.7</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.7, Figure 478, printed pages 469, PDF pages 495</p></details>

</details>
</details>
</section>
<section class="lesson" id="module-temperature-event-loop"><h2 id="heading-temperature-event-loop"><span class="section-number">04</span> Temperature thresholds, sensors, and notifications</h2>
<p>FID 04h is more than a temperature number. TMPSEL selects a sensor, THSEL selects over or under, TMPTH sets the trigger point, TMPTHH sets the event clear point, and SMART/Health.TTC plus AEC enable return controller state to the host.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>TMPSEL</dt><dd>Temperature Sensor Select, the field choosing Composite Temperature or sensor 1 through 8.</dd></div><div><dt>TMPTHH</dt><dd>Temperature Threshold Hysteresis, Kelvin hysteresis used when ending a threshold event.</dd></div><div><dt>THSEL</dt><dd>Threshold Type Select, choosing an over-temperature or under-temperature threshold.</dd></div><div><dt>TMPTH</dt><dd>Temperature Threshold, a 16-bit threshold value in Kelvin.</dd></div><div><dt>TTC</dt><dd>Temperature Threshold Critical Warning, the temperature-threshold bit in SMART/Health Critical Warning.</dd></div></dl>
<details class="technical-note"><summary>Mechanism and applicable conditions</summary>
<!-- claim:BASEPOWER-FID04 -->
<p>FID 04h sets over/under thresholds for Composite Temperature and up to eight implemented temperature sensors. Temperature is encoded in Kelvin; reaching an over threshold or falling to/below an under threshold may set the SMART/Health Temperature Threshold critical warning and trigger an asynchronous event.</p><details class="source-note"><summary>Sources: Base 2.4 §5.2.30.1.3</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.3, printed pages 462-463, PDF pages 488-489</p></details>
<!-- claim:BASEPOWER-HYST -->
<p>In Figure 470, TMPSEL selects a sensor, THSEL selects over/under, TMPTH is the threshold, and TMPTHH is hysteresis. An over event ends at threshold minus hysteresis; an under event ends at threshold plus hysteresis.</p><details class="source-note"><summary>Sources: Base 2.4 §5.2.30.1.3.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.3.1, printed pages 463-464, PDF pages 489-490</p></details>
<!-- claim:BASEPOWER-OBSERVE -->
<p>Successful configuration is not the end of verification. Observe SMART/Health Composite Temperature, the TTC critical warning, warning-temperature time, HCTM transition counters, and implemented sensor readings together with CQE and host latency.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>HCTM</dt><dd>Host Controlled Thermal Management, the two-stage controller thermal response configured by host TMT1/TMT2 values.</dd></div><div><dt>CQE</dt><dd>Completion Queue Entry, one completion-result structure in a CQ.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §5.2.13.1.3</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.3, printed pages 220-225, PDF pages 246-251</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">Item</th><th scope="col">Role or distinction</th><th scope="col">Conditions</th></tr></thead><tbody><tr><td>TMPSEL</td><td>Composite or sensor 1-8</td><td>Get does not use all-sensors selection</td></tr><tr><td>THSEL</td><td>Over/under</td><td>Comparison direction is reversed</td></tr><tr><td>TMPTH</td><td>Trigger Kelvin</td><td>Log raw K and converted °C</td></tr><tr><td>TMPTHH</td><td>Clear hysteresis in Kelvin</td><td>Not a second trigger threshold</td></tr></tbody></table></div>
<aside class="worked-example"><h3>Example</h3><p>For a Composite over threshold of 343 K (about 70 °C) and 5 K hysteresis: TMPSEL=0, THSEL=0, TMPTH=0157h, and TMPTHH=5, giving CDW11=(5&lt;&lt;22)+0157h=01400157h. The event triggers at ≥343 K and ends only after falling to 338 K (about 65 °C).</p></aside>
<details class="technical-note"><summary>Fields and data structures in more depth</summary>
<!-- figure-table:BASEPOWER-FIG-470 -->
<details class="field-note" id="figure-BASEPOWER-FIG-470"><summary>Base Figure 470 · Temperature Threshold – Command Dword 11</summary>
<!-- claim:BASEPOWER-FIG-470-CLAIM -->
<p>Figure 470, "Temperature Threshold – Command Dword 11": Defines the concrete layout or value relationships for Temperature Threshold – Command Dword 11.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>Dword</dt><dd>Double word, four bytes or 32 bits; NVMe command fields are commonly identified by CDW number.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §5.2.30.1.3.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.3.1, Figure 470, printed pages 463-464, PDF pages 489-490</p></details>

</details>
<!-- figure-table:BASEPOWER-FIG-213 -->
<details class="field-note" id="figure-BASEPOWER-FIG-213"><summary>Base Figure 213 · SMART / Health Information Log</summary>
<!-- claim:BASEPOWER-FIG-213-CLAIM -->
<p>Figure 213, "SMART / Health Information Log": Defines the concrete layout or value relationships for SMART / Health Information Log.</p><details class="source-note"><summary>Sources: Base 2.4 §5.2.13.1.3</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.3, Figure 213, printed pages 220-225, PDF pages 246-251</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>HCTM</dt><dd>Host Controlled Thermal Management, the two-stage controller thermal response configured by host TMT1/TMT2 values.</dd></div></dl>
</details>
<!-- figure-table:BASEPOWER-FIG-474 -->
<details class="field-note" id="figure-BASEPOWER-FIG-474"><summary>Base Figure 474 · Asynchronous Event Configuration – Command Dword 11</summary>
<!-- claim:BASEPOWER-FIG-474-CLAIM -->
<p>Figure 474, "Asynchronous Event Configuration – Command Dword 11": Defines the concrete layout or value relationships for Asynchronous Event Configuration – Command Dword 11.</p><details class="source-note"><summary>Sources: Base 2.4 §5.2.30.1.6</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.6, Figure 474, printed pages 466-468, PDF pages 492-494</p></details>

</details>
</details>
</section>
<section class="lesson" id="module-hctm-control-loop"><h2 id="heading-hctm-control-loop"><span class="section-number">05</span> Two levels of HCTM thermal management</h2>
<p>HCTM does not select a fixed clock or power state. It gives the controller two temperature boundaries, TMT1/TMT2. At TMT1 the controller minimizes performance impact; at TMT2 it applies stronger thermal control. Actual hysteresis and internal actions are vendor implementation details.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>HCTM</dt><dd>Host Controlled Thermal Management, the two-stage controller thermal response configured by host TMT1/TMT2 values.</dd></div><div><dt>TMT1</dt><dd>Thermal Management Temperature 1, the lighter thermal-management threshold in Kelvin.</dd></div><div><dt>TMT2</dt><dd>Thermal Management Temperature 2, the stronger thermal-management threshold in Kelvin.</dd></div></dl>
<details class="technical-note"><summary>Mechanism and applicable conditions</summary>
<!-- claim:BASEPOWER-FID10 -->
<p>FID 10h uses TMT1[31:16] as the lighter thermal-management threshold and TMT2[15:0] as the heavier threshold, both in Kelvin; zero independently disables the corresponding threshold.</p><details class="source-note"><summary>Sources: Base 2.4 §5.2.30.1.10</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.10, printed pages 471-472, PDF pages 497-498</p></details>
<!-- claim:BASEPOWER-HCTM -->
<p>A nonzero TMT1 shall be less than TMT2, and both shall lie between MNTMT and MXTMT; otherwise the command returns Invalid Field in Command. At TMT1 the controller acts to minimize impact, while TMT2 invokes stronger action; hysteresis is vendor-specific.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>MNTMT</dt><dd>Minimum Thermal Management Temperature, the minimum Kelvin value accepted for HCTM.</dd></div><div><dt>MXTMT</dt><dd>Maximum Thermal Management Temperature, the maximum Kelvin value accepted for HCTM.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §5.2.30.1.10, 8.1.19.5</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.10, 8.1.19.5, printed pages 472, 670-671, PDF pages 498, 696-697</p></details>
<!-- claim:BASEPOWER-FID11 -->
<p>FID 11h NOPPME=1 allows a controller-initiated background operation to raise power temporarily, no higher than the last operational state's limit. With NOPPME=0, such work shall not exceed the current non-operational-state limits.</p><details class="source-note"><summary>Sources: Base 2.4 §5.2.30.1.11</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.11, printed pages 472-473, PDF pages 498-499</p></details>
<!-- claim:BASEPOWER-RTD3 -->
<p>RTD3E and RTD3R describe entry and resume time for evaluating idle break-even in a PCIe D3cold use case; the NVMe text explicitly says these are not D3hot times. Complete PCIe D-state semantics are not present in the supplied source and are not invented here.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>RTD3E</dt><dd>Runtime D3 Entry Latency, the expected time for entering a PCIe D3cold use case.</dd></div><div><dt>RTD3R</dt><dd>Runtime D3 Resume Latency, the expected time for resuming from a PCIe D3cold use case.</dd></div><div><dt>PCIe</dt><dd>PCI Express, the transport and device interconnect used by an NVMe memory-based controller.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §8.1.19.4</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §8.1.19.4, printed pages 669-670, PDF pages 695-696</p></details>
<!-- claim:BASEPOWER-GET-STATUS -->
<p>For an inapplicable Controller Identifier, Get Features reports command-specific status 1Fh, Invalid Controller Identifier; interpret the status code together with SCT.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>SCT</dt><dd>Status Code Type, the category selected before interpreting SC.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §5.2.12.2</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.12.2, printed pages 212, PDF pages 238</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">Item</th><th scope="col">Role or distinction</th><th scope="col">Conditions</th></tr></thead><tbody><tr><td>TMT1</td><td>Lighter-control boundary</td><td>Objective is to minimize impact</td></tr><tr><td>TMT2</td><td>Stronger-control boundary</td><td>Thermal control takes priority</td></tr><tr><td>MNTMT/MXTMT</td><td>Legal configuration range</td><td>Validate on the host first</td></tr><tr><td>SMART counters</td><td>Transition count/time</td><td>Evidence that the control loop acted</td></tr></tbody></table></div><dl class="term-note" aria-label="Terms in this passage"><div><dt>MNTMT</dt><dd>Minimum Thermal Management Temperature, the minimum Kelvin value accepted for HCTM.</dd></div><div><dt>MXTMT</dt><dd>Maximum Thermal Management Temperature, the maximum Kelvin value accepted for HCTM.</dd></div></dl>
<aside class="worked-example"><h3>Example</h3><p>If MNTMT=273 K and MXTMT=373 K, TMT1=343 K and TMT2=353 K are legal, and CDW11=(0157h&lt;&lt;16)+0161h=01570161h. FID 10h is saveable; if SVBL=1 and policy requires persistence, CDW10.SV=1 with FID=10h gives CDW10=80000010h.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>SV</dt><dd>Save, the Set Features bit requesting that the controller also save the configured value.</dd></div></dl></aside>
<details class="technical-note"><summary>Fields and data structures in more depth</summary>
<!-- figure-table:BASEPOWER-FIG-482 -->
<details class="field-note" id="figure-BASEPOWER-FIG-482"><summary>Base Figure 482 · Host Controlled Thermal Management – Command Dword 11</summary>
<!-- claim:BASEPOWER-FIG-482-CLAIM -->
<p>Figure 482, "Host Controlled Thermal Management – Command Dword 11": Defines the concrete layout or value relationships for Host Controlled Thermal Management – Command Dword 11.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>Dword</dt><dd>Double word, four bytes or 32 bits; NVMe command fields are commonly identified by CDW number.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §5.2.30.1.10</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.10, Figure 482, printed pages 472, PDF pages 498</p></details>

</details>
<!-- figure-table:BASEPOWER-FIG-741 -->
<details class="field-note" id="figure-BASEPOWER-FIG-741"><summary>Base Figure 741 · Host Controlled Thermal Management</summary>
<!-- claim:BASEPOWER-FIG-741-CLAIM -->
<p>Figure 741, "Host Controlled Thermal Management": Maps the power/thermal control relationship represented by Host Controlled Thermal Management.</p><details class="source-note"><summary>Sources: Base 2.4 §8.1.19.5</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §8.1.19.5, Figure 741, printed pages 671, PDF pages 697</p></details>

</details>
</details>
</section>
<section id="additional-details"><h2 id="further-mechanisms">Additional mechanisms and data formats</h2>
<!-- claim:BASEPOWER-GET-SAVED -->
<p>If a saved value is requested but saved values are unsupported or none exists, the controller operates using the default value. A successful read therefore does not prove that a value was previously saved.</p><details class="source-note"><summary>Sources: Base 2.4 §5.2.12</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.12, printed pages 210, PDF pages 236</p></details>
<!-- claim:BASEPOWER-GET-UIDX -->
<p>CDW14.UIDX is meaningful only when the controller supports the UUID List and the Feature uses a UUID association; otherwise it remains zero.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>UIDX</dt><dd>UUID Index, an index into the UUID List; zero indicates that no UUID is specified.</dd></div><div><dt>UUID</dt><dd>Universally Unique Identifier, a 128-bit identifier whose association scope is defined by the containing structure.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §5.2.12</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.12, printed pages 210, PDF pages 236</p></details>
<!-- claim:BASEPOWER-FID-SCOPE -->
<p>All five FIDs in this report have Controller scope. FIDs 02h, 04h, 0Ch, and 11h are not saveable; FID 10h is saveable. Only FID 0Ch uses a 256-byte data structure.</p><details class="source-note"><summary>Sources: Base 2.4 §5.2.30</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30, printed pages 457-459, PDF pages 483-485</p></details>
<!-- figure-table:BASEPOWER-FIG-483 -->
<details class="field-note" id="figure-BASEPOWER-FIG-483"><summary>Base Figure 483 · Non-Operational Power State Configuration – Command Dword 11</summary>
<!-- claim:BASEPOWER-FIG-483-CLAIM -->
<p>Figure 483, "Non-Operational Power State Configuration – Command Dword 11": Defines the concrete layout or value relationships for Non-Operational Power State Configuration – Command Dword 11.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>Dword</dt><dd>Double word, four bytes or 32 bits; NVMe command fields are commonly identified by CDW number.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §5.2.30.1.11</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.11, Figure 483, printed pages 472-473, PDF pages 498-499</p></details>

</details>
</section>
<section id="knowledge-check"><h2 id="review-questions">Check your understanding</h2>
<!-- qa:base-power-features-feature-values -->
<details class="review-question" id="qa-base-power-features-feature-values"><summary>1. Why are Supported, Current, Default, and Saved not interchangeable Feature values?</summary>
<div data-qa-answer="base-power-features-feature-values"><p>Supported Capabilities describes how the Feature may be used. Current is the active value, Default the default value, and Saved the persisted value subject to support. The read selection determines the reply’s meaning.</p></div>
<details class="source-note"><summary>Sources</summary>
<p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.12, printed pages 209-210, PDF pages 235-236</p>
<p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.12, printed pages 210, PDF pages 236</p>
<p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.12.1, printed pages 211-212, PDF pages 237-238</p>
</details></details>
<!-- qa:base-power-features-power-latency -->
<details class="review-question" id="qa-base-power-features-power-latency"><summary>2. Why might the lowest-idle-power state be unsuitable for a workload that frequently resumes I/O?</summary>
<div data-qa-answer="base-power-features-power-latency"><p>Transitions can incur latency on every entry and exit. Savings during a short idle period must be evaluated alongside entry/exit delays and response-time needs, rather than power numbers alone.</p></div>
<details class="source-note"><summary>Sources</summary>
<p>Source: NVME-BASE-2.4, Rev. 2.4, §8.1.19, printed pages 666-668, PDF pages 692-694</p>
<p>Source: NVME-BASE-2.4, Rev. 2.4, §8.1.19.1, printed pages 668-669, PDF pages 694-695</p>
</details></details>
<!-- qa:base-power-features-apst -->
<details class="review-question" id="qa-base-power-features-apst"><summary>3. What do idle time and target state determine in an APST entry?</summary>
<div data-qa-answer="base-power-features-apst"><p>Idle time specifies the wait before an automatic transition under the applicable conditions. The target selects the destination Power State. Both must be combined with that state’s capabilities and restrictions.</p></div>
<details class="source-note"><summary>Sources</summary>
<p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.7, printed pages 468-469, PDF pages 494-495</p>
<p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.7, printed pages 469, PDF pages 495</p>
</details></details>
<!-- qa:base-power-features-thermal-controls -->
<details class="review-question" id="qa-base-power-features-thermal-controls"><summary>4. Why configure and interpret Temperature Threshold separately from HCTM?</summary>
<div data-qa-answer="base-power-features-thermal-controls"><p>Temperature Threshold governs temperature conditions and notifications; HCTM provides host-controlled thermal-management behavior. Learning that a threshold was crossed and requesting thermal management are different actions.</p></div>
<details class="source-note"><summary>Sources</summary>
<p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.3, printed pages 462-463, PDF pages 488-489</p>
<p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.10, 8.1.19.5, printed pages 472, 670-671, PDF pages 498, 696-697</p>
</details></details>
</section>
<footer class="reference-editions"><details class="source-note"><summary>Specification editions</summary><p>NVM Express Base Specification, Revision 2.4</p></details></footer>
</div>
