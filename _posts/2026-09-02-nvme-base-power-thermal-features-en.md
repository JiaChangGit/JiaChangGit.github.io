---
layout: post
read_time: true
show_date: true
title: "NVMe Base 2.4: Power/Thermal Features and Power Management"
date: 2026-09-02
description: "Source-located PCIe/NVMe report for PPT authoring."
lang: en
img: posts/2026/cat_title.jpg
tags: [NVMe, PCIe, Specification]
category: NVMe
author: Jia-Chang
github: JiaChangGit/JiaChangGit.github.io/tree/main/DOCS/nvme-spec-report
toc: yes
---
[繁體中文]({% post_url 2026-09-02-nvme-base-power-thermal-features-zh-tw %})


# NVMe Base 2.4: Power/Thermal Features and Power Management

Purpose: a source-located engineering report for GitHub Pages and a 100-minute presentation.

Scope: §5.2.12, the common §5.2.30 command, FIDs 02h/04h/0Ch/10h/11h, and §8.1.19 through §8.1.19.5; includes five minimum dependency Figures and excludes Power Limit, IIELL, other FIDs, and transport-specific material. Only PCIe/memory-based and common NVMe content appears below.

## Source versions

NVM Express Base Specification, Revision 2.4

Verification date: 2026-09-02. No additional errata, ECNs, Technical Proposals, controller-vendor documents, or source text from the external PCI Express Base Specification are included.

## Reading map

```text
Get capability / value -> Choose host policy -> Set one Feature -> Observe completion / temperature
```

First use Get Features to separate capability from current value. Choose policy from Power State Descriptors, thermal capabilities, and workload; after Set Features succeeds, close the loop with completion evidence, SMART/Health, and observed latency/temperature.

## Normative language

shall is mandatory, may permits a choice, should expresses a preferred recommendation, and optional means support is not required. The report preserves these terms and never promotes one into another.

## Acronyms first: complete glossary

Every abbreviation below is introduced before it is used in the slide narrative. The term alone is never enough: retain owner, width, unit, scope, and state.

| Acronym / term | Plain-language meaning | Source |
|---|---|---|
| `FID` | Feature Identifier, the eight-bit identifier selecting a function in Get/Set Features. | NVME-BASE-2.4 Rev. 2.4, §5.2.12, printed pp. 209, PDF pp. 235 |
| `SEL` | Select, the Get Features field choosing current, default, saved, or supported-capabilities view. | NVME-BASE-2.4 Rev. 2.4, §5.2.12, printed pp. 209-210, PDF pp. 235-236 |
| `UIDX` | UUID Index, an index into the UUID List; zero indicates that no UUID is specified. | NVME-BASE-2.4 Rev. 2.4, §5.2.12, printed pp. 210, PDF pp. 236 |
| `CHANG` | Changeable, the capability bit indicating whether Set Features can modify the Feature value. | NVME-BASE-2.4 Rev. 2.4, §5.2.12.1, printed pp. 211-212, PDF pp. 237-238 |
| `NSSPEC` | Namespace Specific, the capability bit indicating whether a Feature has per-namespace scope. | NVME-BASE-2.4 Rev. 2.4, §5.2.12.1, printed pp. 211-212, PDF pp. 237-238 |
| `SVBL` | Saveable, the supported-capabilities bit indicating whether a Feature can be saved. | NVME-BASE-2.4 Rev. 2.4, §5.2.12.1, printed pp. 211-212, PDF pp. 237-238 |
| `SV` | Save, the Set Features bit requesting that the controller also save the configured value. | NVME-BASE-2.4 Rev. 2.4, §5.2.30, printed pp. 457, PDF pp. 483 |
| `DPTR` | Data Pointer, the SQE field identifying a command data buffer. | NVME-BASE-2.4 Rev. 2.4, §5.2.30, printed pp. 456-457, PDF pp. 482-483 |
| `PRP` | Physical Region Page, a pointer format describing a host-addressable data buffer in memory-page units. | NVME-BASE-2.4 Rev. 2.4, §5.2.30, printed pp. 456-457, PDF pp. 482-483 |
| `CQE` | Completion Queue Entry, one completion-result structure in a CQ. | NVME-BASE-2.4 Rev. 2.4, §5.2.12.2, printed pp. 212, PDF pp. 238 |
| `SCT` | Status Code Type, the category selected before interpreting SC. | NVME-BASE-2.4 Rev. 2.4, §5.2.12.2, printed pp. 212, PDF pp. 238 |
| `SC` | Status Code, the specific completion result interpreted in the context of SCT. | NVME-BASE-2.4 Rev. 2.4, §5.2.12.2, printed pp. 212, PDF pp. 238 |
| `PSD` | Power State Descriptor, the structure describing power, latency, operational type, and relative performance for one power state. | NVME-BASE-2.4 Rev. 2.4, §8.1.19, printed pp. 666-668, PDF pp. 692-694 |
| `PS` | Power State, a controller power/performance operating point; PS0 has the highest maximum power. | NVME-BASE-2.4 Rev. 2.4, §5.2.30.1.2, printed pp. 460-461, PDF pp. 486-487 |
| `NPSS` | Number of Power States Support, the zero-based field reporting the highest supported power-state number. | NVME-BASE-2.4 Rev. 2.4, §5.2.30.1.2, printed pp. 460-461, PDF pp. 486-487 |
| `MP` | Maximum Power, the sustained maximum power of a power state. | NVME-BASE-2.4 Rev. 2.4, §8.1.19, printed pp. 666-668, PDF pp. 692-694 |
| `NOPS` | Non-Operational State, the PSD bit indicating that the state does not process I/O commands. | NVME-BASE-2.4 Rev. 2.4, §8.1.19, printed pp. 667-668, PDF pp. 693-694 |
| `ENLAT` | Entry Latency, the maximum latency to enter a power state, in microseconds. | NVME-BASE-2.4 Rev. 2.4, §8.1.19.1, printed pp. 668-669, PDF pp. 694-695 |
| `EXLAT` | Exit Latency, the maximum latency to exit a power state, in microseconds. | NVME-BASE-2.4 Rev. 2.4, §8.1.19.1, printed pp. 668-669, PDF pp. 694-695 |
| `IDLP` | Idle Power, typical power under the specification's idle measurement conditions. | NVME-BASE-2.4 Rev. 2.4, §8.1.19, printed pp. 666-668, PDF pp. 692-694 |
| `ACTP` | Active Power, average active power under the specified workload and time window. | NVME-BASE-2.4 Rev. 2.4, §8.1.19, printed pp. 666-668, PDF pp. 692-694 |
| `WH` | Workload Hint, a host-supplied workload category hint rather than a performance guarantee. | NVME-BASE-2.4 Rev. 2.4, §8.1.19.3, printed pp. 669, PDF pp. 695 |
| `APST` | Autonomous Power State Transition, the mechanism for controller-directed entry into non-operational states based on idle timers. | NVME-BASE-2.4 Rev. 2.4, §5.2.30.1.7, printed pp. 468-469, PDF pp. 494-495 |
| `APSTE` | Autonomous Power State Transition Enable, the bit enabling APST-table timer evaluation. | NVME-BASE-2.4 Rev. 2.4, §5.2.30.1.7, printed pp. 468-469, PDF pp. 494-495 |
| `ITPT` | Idle Time Prior to Transition, the APST-entry idle threshold in milliseconds. | NVME-BASE-2.4 Rev. 2.4, §5.2.30.1.7, printed pp. 469, PDF pp. 495 |
| `ITPS` | Idle Transition Power State, the target non-operational power state selected by an APST entry. | NVME-BASE-2.4 Rev. 2.4, §5.2.30.1.7, printed pp. 469, PDF pp. 495 |
| `NOPPME` | Non-Operational Power State Permissive Mode Enable, controlling whether controller background work may temporarily exceed a non-operational power limit. | NVME-BASE-2.4 Rev. 2.4, §5.2.30.1.11, printed pp. 472-473, PDF pp. 498-499 |
| `TMPSEL` | Temperature Sensor Select, the field choosing Composite Temperature or sensor 1 through 8. | NVME-BASE-2.4 Rev. 2.4, §5.2.30.1.3.1, printed pp. 463-464, PDF pp. 489-490 |
| `THSEL` | Threshold Type Select, choosing an over-temperature or under-temperature threshold. | NVME-BASE-2.4 Rev. 2.4, §5.2.30.1.3.1, printed pp. 463-464, PDF pp. 489-490 |
| `TMPTH` | Temperature Threshold, a 16-bit threshold value in Kelvin. | NVME-BASE-2.4 Rev. 2.4, §5.2.30.1.3.1, printed pp. 463-464, PDF pp. 489-490 |
| `TMPTHH` | Temperature Threshold Hysteresis, Kelvin hysteresis used when ending a threshold event. | NVME-BASE-2.4 Rev. 2.4, §5.2.30.1.3.1, printed pp. 463-464, PDF pp. 489-490 |
| `TTC` | Temperature Threshold Critical Warning, the temperature-threshold bit in SMART/Health Critical Warning. | NVME-BASE-2.4 Rev. 2.4, §5.2.30.1.3, printed pp. 462-463, PDF pp. 488-489 |
| `HCTM` | Host Controlled Thermal Management, the two-stage controller thermal response configured by host TMT1/TMT2 values. | NVME-BASE-2.4 Rev. 2.4, §5.2.30.1.10, 8.1.19.5, printed pp. 472, 670-671, PDF pp. 498, 696-697 |
| `TMT1` | Thermal Management Temperature 1, the lighter thermal-management threshold in Kelvin. | NVME-BASE-2.4 Rev. 2.4, §5.2.30.1.10, printed pp. 471-472, PDF pp. 497-498 |
| `TMT2` | Thermal Management Temperature 2, the stronger thermal-management threshold in Kelvin. | NVME-BASE-2.4 Rev. 2.4, §5.2.30.1.10, printed pp. 471-472, PDF pp. 497-498 |
| `MNTMT` | Minimum Thermal Management Temperature, the minimum Kelvin value accepted for HCTM. | NVME-BASE-2.4 Rev. 2.4, §5.2.30.1.10, 8.1.19.5, printed pp. 472, 670-671, PDF pp. 498, 696-697 |
| `MXTMT` | Maximum Thermal Management Temperature, the maximum Kelvin value accepted for HCTM. | NVME-BASE-2.4 Rev. 2.4, §5.2.30.1.10, 8.1.19.5, printed pp. 472, 670-671, PDF pp. 498, 696-697 |
| `WCTEMP` | Warning Composite Temperature Threshold, the composite warning threshold reported by Identify Controller. | NVME-BASE-2.4 Rev. 2.4, §5.2.30.1.3, printed pp. 462-463, PDF pp. 488-489 |
| `RTD3E` | Runtime D3 Entry Latency, the expected time for entering a PCIe D3cold use case. | NVME-BASE-2.4 Rev. 2.4, §8.1.19.4, printed pp. 669-670, PDF pp. 695-696 |
| `RTD3R` | Runtime D3 Resume Latency, the expected time for resuming from a PCIe D3cold use case. | NVME-BASE-2.4 Rev. 2.4, §8.1.19.4, printed pp. 669-670, PDF pp. 695-696 |

## Visual atlas: locate the system before reading fields

Each redraw answers a different question: architecture locates components, sequence shows ownership, decode turns bits into engineering values, and state views preserve failure evidence. These are teaching redraws, not copies of specification artwork.

### Visual 01: Get first, Set second, then observe again

**View type:** `sequence`

```text
Host / software        Shared object        Controller / evidence
Host → Shared: Identify capability gates
Shared → Controller: Get SEL=011b
Controller → Shared: Get current/default
Shared → Host: Choose FID-specific value
Host → Shared: Set + decode CQE
Shared → Controller: Get again + observe runtime
```

**Question answered:** A Feature is not a simple register. The host first reads capability with SEL=011b, then retrieves current/default/saved views, confirms scope and persistence, and only then writes. Set completion proves command outcome; a follow-up Get and runtime telemetry prove that software observes the new policy.

**Supporting Figures:** Figure 93, Figure 197, Figure 198, Figure 199, Figure 200, Figure 201, Figure 202, Figure 463, Figure 464, Figure 465, Figure 466

**Sources:** NVME-BASE-2.4 Rev. 2.4, §5.2.12, printed pp. 209, PDF pp. 235; NVME-BASE-2.4 Rev. 2.4, §5.2.12, printed pp. 209-210, PDF pp. 235-236; NVME-BASE-2.4 Rev. 2.4, §5.2.12.1, printed pp. 211-212, PDF pp. 237-238; NVME-BASE-2.4 Rev. 2.4, §5.2.30, printed pp. 457, PDF pp. 483; NVME-BASE-2.4 Rev. 2.4, §5.2.30, printed pp. 459, PDF pp. 485

### Visual 02: A power state is a multidimensional power, latency, and performance operating point

**View type:** `architecture`

```text
[Identify.NPSS]
  ├─ [Read PSD[0..NPSS]]
  ├─ [Classify operational/non-operatio…]
  ├─ [Compute transition budget]
  ├─ [Apply workload-latency SLO]
  └─ [Choose FID 02h PS/WH]
```

**Question answered:** A state number alone cannot establish workload suitability. Read MP, NOPS, ENLAT/EXLAT, IDLP/ACTP, and relative performance together in each PSD. Increasing PS numbers reduce maximum power monotonically, but latency and throughput do not necessarily change by a fixed ratio.

**Supporting Figures:** Figure 338, Figure 340, Figure 468, Figure 738, Figure 739, Figure 740

**Sources:** NVME-BASE-2.4 Rev. 2.4, §8.1.19, printed pp. 666-667, PDF pp. 692-693; NVME-BASE-2.4 Rev. 2.4, §8.1.19, printed pp. 666-668, PDF pp. 692-694; NVME-BASE-2.4 Rev. 2.4, §8.1.19.1, printed pp. 668-669, PDF pp. 694-695; NVME-BASE-2.4 Rev. 2.4, §8.1.19.2, printed pp. 668, PDF pp. 694; NVME-BASE-2.4 Rev. 2.4, §8.1.19, printed pp. 667-668, PDF pp. 693-694; NVME-BASE-2.4 Rev. 2.4, §5.2.30.1.2, printed pp. 460-461, PDF pp. 486-487; NVME-BASE-2.4 Rev. 2.4, §8.1.19.3, printed pp. 669, PDF pp. 695

### Visual 03: APST is a state machine driven by idle timers

**View type:** `state`

```text
[APSTE=1] → [Start idle after I/O completes] → [Continuous idle > ITPT] → [Enter ITPS non-operational] → [I/O arrives] → [Return to most recent operational…]
timeout / failure ──→ preserve trigger + previous state + evidence
```

**Question answered:** The 256-byte APST buffer is not a performance table. It contains 32 rules stating which non-operational state to enter after a given idle duration. APSTE enables timer rules, entries with ITPT=0 are inactive, and arriving I/O returns the controller to its most recent operational state.

**Supporting Figures:** Figure 463, Figure 475, Figure 476, Figure 477, Figure 478

**Sources:** NVME-BASE-2.4 Rev. 2.4, §5.2.30.1.7, printed pp. 468-469, PDF pp. 494-495; NVME-BASE-2.4 Rev. 2.4, §5.2.30.1.7, printed pp. 469, PDF pp. 495; NVME-BASE-2.4 Rev. 2.4, §5.2.30.1.7, printed pp. 469, PDF pp. 495; NVME-BASE-2.4 Rev. 2.4, §8.1.19, printed pp. 668, PDF pp. 694; NVME-BASE-2.4 Rev. 2.4, §5.2.30, printed pp. 456-457, PDF pp. 482-483

### Visual 04: Temperature Threshold connects sensor, event, and clear point

**View type:** `state`

```text
[Select Composite/Sensor] → [Set over/under TMPTH] → [Set TMPTHH] → [Temperature crosses threshold] → [TTC + optional AEN] → [Event ends after clear point]
timeout / failure ──→ preserve trigger + previous state + evidence
```

**Question answered:** FID 04h is more than a temperature number. TMPSEL selects a sensor, THSEL selects over or under, TMPTH sets the trigger point, TMPTHH sets the event clear point, and SMART/Health.TTC plus AEC enable return controller state to the host.

**Supporting Figures:** Figure 213, Figure 470, Figure 474

**Sources:** NVME-BASE-2.4 Rev. 2.4, §5.2.30.1.3, printed pp. 462-463, PDF pp. 488-489; NVME-BASE-2.4 Rev. 2.4, §5.2.30.1.3.1, printed pp. 463-464, PDF pp. 489-490; NVME-BASE-2.4 Rev. 2.4, §5.2.13.1.3, printed pp. 220-225, PDF pp. 246-251

### Visual 05: HCTM uses two thresholds for lighter and stronger thermal response

**View type:** `state`

```text
[Read HCTMA/MNTMT/MXTMT] → [Choose TMT1<TMT2] → [Set FID10h] → [Temperature reaches TMT1] → [Temperature reaches TMT2] → [Read SMART counters/latency]
timeout / failure ──→ preserve trigger + previous state + evidence
```

**Question answered:** HCTM does not select a fixed clock or power state. It gives the controller two temperature boundaries, TMT1/TMT2. At TMT1 the controller minimizes performance impact; at TMT2 it applies stronger thermal control. Actual hysteresis and internal actions are vendor implementation details.

**Supporting Figures:** Figure 213, Figure 338, Figure 482, Figure 741

**Sources:** NVME-BASE-2.4 Rev. 2.4, §5.2.30.1.10, printed pp. 471-472, PDF pp. 497-498; NVME-BASE-2.4 Rev. 2.4, §5.2.30.1.10, 8.1.19.5, printed pp. 472, 670-671, PDF pp. 498, 696-697; NVME-BASE-2.4 Rev. 2.4, §5.2.13.1.3, printed pp. 220-225, PDF pp. 246-251

### Visual 06: Connect policy, state, events, and measurements into reproducible debug evidence

**View type:** `sequence`

```text
Host / software        Shared object        Controller / evidence
Host → Shared: Capability snapshot
Shared → Controller: Raw Get/Set commands
Controller → Shared: CQE + timestamp
Shared → Host: APST/PS transition
Host → Shared: Temperature/TTC/HCTM
Shared → Controller: I/O latency + recovery decision
```

**Question answered:** Power/thermal defects rarely reduce to one wrong bit. Capability, policy, transition, background work, thermal events, and host workload must share one timeline. FID 11h NOPPME, APST, manual PS, HCTM, and RTD3 control different layers and do not replace one another.

**Supporting Figures:** Figure 202, Figure 213, Figure 340, Figure 478, Figure 483

**Sources:** NVME-BASE-2.4 Rev. 2.4, §5.2.30.1.7, printed pp. 469, PDF pp. 495; NVME-BASE-2.4 Rev. 2.4, §5.2.30.1.11, printed pp. 472-473, PDF pp. 498-499; NVME-BASE-2.4 Rev. 2.4, §8.1.19.4, printed pp. 669-670, PDF pp. 695-696; NVME-BASE-2.4 Rev. 2.4, §5.2.13.1.3, printed pp. 220-225, PDF pp. 246-251; NVME-BASE-2.4 Rev. 2.4, §5.2.12.2, printed pp. 212, PDF pp. 238

## Mental Model and complete teaching path

The modules follow engineering causality rather than specification-section order. Related Figures return at the point where they support the flow.

### Module 01: Get first, Set second, then observe again

**Explanation.** A Feature is not a simple register. The host first reads capability with SEL=011b, then retrieves current/default/saved views, confirms scope and persistence, and only then writes. Set completion proves command outcome; a follow-up Get and runtime telemetry prove that software observes the new policy.

```text
Identify capability gates
  ↓
Get SEL=011b
  ↓
Get current/default
  ↓
Choose FID-specific value
  ↓
Set + decode CQE
  ↓
Get again + observe runtime
```

#### Comparison

| Item | What it answers | Engineering note |
|---|---|---|
| SEL=000b | Current value | Observe current controller policy |
| SEL=001b | Default value | Establish a rollback baseline |
| SEL=010b | Saved value | Does not prove a value was saved |
| SEL=011b | CHANG/NSSPEC/SVBL | Capability gate before writing |

**Informative example.** For FID 02h current, CDW10=00000002h. For supported capabilities, SEL=3 so CDW10=(3×100h)+02h=00000302h. If CHANG=0, stop before Set; if CHANG=1, construct CDW11 from NPSS and the PSDs.

**Common mistake / debugging.** Do not log only 'Get succeeded.' Retain raw CDW10/CDW14, CQE.DW0, SCT/SC/DNR, and the selected current/default/saved/capability view; otherwise the same 32-bit result can be decoded with the wrong semantics.

**Supporting sources:** NVME-BASE-2.4 Rev. 2.4, §5.2.12, printed pp. 209, PDF pp. 235; NVME-BASE-2.4 Rev. 2.4, §5.2.12, printed pp. 209-210, PDF pp. 235-236; NVME-BASE-2.4 Rev. 2.4, §5.2.12.1, printed pp. 211-212, PDF pp. 237-238; NVME-BASE-2.4 Rev. 2.4, §5.2.30, printed pp. 457, PDF pp. 483; NVME-BASE-2.4 Rev. 2.4, §5.2.30, printed pp. 459, PDF pp. 485

**Related Figures:** Figure 93, Figure 197, Figure 198, Figure 199, Figure 200, Figure 201, Figure 202, Figure 463, Figure 464, Figure 465, Figure 466

### Module 02: A power state is a multidimensional power, latency, and performance operating point

**Explanation.** A state number alone cannot establish workload suitability. Read MP, NOPS, ENLAT/EXLAT, IDLP/ACTP, and relative performance together in each PSD. Increasing PS numbers reduce maximum power monotonically, but latency and throughput do not necessarily change by a fixed ratio.

```text
Identify.NPSS
  ↓
Read PSD[0..NPSS]
  ↓
Classify operational/non-operational
  ↓
Compute transition budget
  ↓
Apply workload-latency SLO
  ↓
Choose FID 02h PS/WH
```

#### Comparison

| Item | What it answers | Engineering note |
|---|---|---|
| MP | Sustained maximum power | Not an instantaneous sample |
| IDLP/ACTP | Idle typical / active average | Different measurement conditions |
| ENLAT/EXLAT | Maximum entry/exit latency | Sum across transitions |
| RRT/RRL/RWT/RWL | Relative throughput/latency | Compare only like characteristics |

**Informative example.** Informative calculation: current PS1.EXLAT=100 µs and target PS3.ENLAT=2500 µs produce a direct-transition budget of 2600 µs. If the path is PS1→PS2→PS3, sum PS1.EXLAT+PS2.ENLAT and PS2.EXLAT+PS3.ENLAT instead of reusing 2600 µs.

**Common mistake / debugging.** A successful FID 02h Set proves only that the controller accepted PS. Debug evidence also needs NPSS, the complete target PSD, previous state, WH, CQE timestamp, and first-I/O latency; entry into a non-operational state additionally requires checking whether I/O was drained.

**Supporting sources:** NVME-BASE-2.4 Rev. 2.4, §8.1.19, printed pp. 666-667, PDF pp. 692-693; NVME-BASE-2.4 Rev. 2.4, §8.1.19, printed pp. 666-668, PDF pp. 692-694; NVME-BASE-2.4 Rev. 2.4, §8.1.19.1, printed pp. 668-669, PDF pp. 694-695; NVME-BASE-2.4 Rev. 2.4, §8.1.19.2, printed pp. 668, PDF pp. 694; NVME-BASE-2.4 Rev. 2.4, §8.1.19, printed pp. 667-668, PDF pp. 693-694; NVME-BASE-2.4 Rev. 2.4, §5.2.30.1.2, printed pp. 460-461, PDF pp. 486-487; NVME-BASE-2.4 Rev. 2.4, §8.1.19.3, printed pp. 669, PDF pp. 695

**Related Figures:** Figure 338, Figure 340, Figure 468, Figure 738, Figure 739, Figure 740

### Module 03: APST is a state machine driven by idle timers

**Explanation.** The 256-byte APST buffer is not a performance table. It contains 32 rules stating which non-operational state to enter after a given idle duration. APSTE enables timer rules, entries with ITPT=0 are inactive, and arriving I/O returns the controller to its most recent operational state.

```text
APSTE=1
  ↓
Start idle after I/O completes
  ↓
Continuous idle > ITPT
  ↓
Enter ITPS non-operational
  ↓
I/O arrives
  ↓
Return to most recent operational PS
```

#### Comparison

| Item | What it answers | Engineering note |
|---|---|---|
| APSTE=0 | Host-directed entry only | The table may exist but timers do not drive entry |
| APSTE=1 | Host- or timer-directed entry | ITPT must be met continuously |
| NOPPME=0 | Background work stays within non-op limits | Controller work may be deferred |
| NOPPME=1 | Background work may raise power temporarily | Still capped by the last operational state |

**Informative example.** To enter PS3 after 2000 ms idle: ITPT=2000=07D0h, shifted into bits31:8 gives 07D00000h; ITPS=3 in bits7:3 gives 18h, so the low dword is 07D00018h. Reserved bits and the entry high dword remain zero; 32 entries total 256 bytes.

**Common mistake / debugging.** Common errors include treating ITPT as microseconds, selecting an operational ITPS, leaving unused entries nonzero, or placing the 256-byte PRP buffer across an unsupported page boundary. Retain a hash of the full buffer and a per-entry decode.

**Supporting sources:** NVME-BASE-2.4 Rev. 2.4, §5.2.30.1.7, printed pp. 468-469, PDF pp. 494-495; NVME-BASE-2.4 Rev. 2.4, §5.2.30.1.7, printed pp. 469, PDF pp. 495; NVME-BASE-2.4 Rev. 2.4, §5.2.30.1.7, printed pp. 469, PDF pp. 495; NVME-BASE-2.4 Rev. 2.4, §8.1.19, printed pp. 668, PDF pp. 694; NVME-BASE-2.4 Rev. 2.4, §5.2.30, printed pp. 456-457, PDF pp. 482-483

**Related Figures:** Figure 463, Figure 475, Figure 476, Figure 477, Figure 478

### Module 04: Temperature Threshold connects sensor, event, and clear point

**Explanation.** FID 04h is more than a temperature number. TMPSEL selects a sensor, THSEL selects over or under, TMPTH sets the trigger point, TMPTHH sets the event clear point, and SMART/Health.TTC plus AEC enable return controller state to the host.

```text
Select Composite/Sensor
  ↓
Set over/under TMPTH
  ↓
Set TMPTHH
  ↓
Temperature crosses threshold
  ↓
TTC + optional AEN
  ↓
Event ends after clear point
```

#### Comparison

| Item | What it answers | Engineering note |
|---|---|---|
| TMPSEL | Composite or sensor 1-8 | Get does not use all-sensors selection |
| THSEL | Over/under | Comparison direction is reversed |
| TMPTH | Trigger Kelvin | Log raw K and converted °C |
| TMPTHH | Clear hysteresis in Kelvin | Not a second trigger threshold |

**Informative example.** For a Composite over threshold of 343 K (about 70 °C) and 5 K hysteresis: TMPSEL=0, THSEL=0, TMPTH=0157h, and TMPTHH=5, giving CDW11=(5<<22)+0157h=01400157h. The event triggers at ≥343 K and ends only after falling to 338 K (about 65 °C).

**Common mistake / debugging.** If no AEN appears, do not immediately conclude that the threshold failed. Check AEC.TTHRY/SHCW enables, TTC, raw sensor Kelvin, threshold type, hysteresis clear point, and an outstanding Asynchronous Event Request in order.

**Supporting sources:** NVME-BASE-2.4 Rev. 2.4, §5.2.30.1.3, printed pp. 462-463, PDF pp. 488-489; NVME-BASE-2.4 Rev. 2.4, §5.2.30.1.3.1, printed pp. 463-464, PDF pp. 489-490; NVME-BASE-2.4 Rev. 2.4, §5.2.13.1.3, printed pp. 220-225, PDF pp. 246-251

**Related Figures:** Figure 213, Figure 470, Figure 474

### Module 05: HCTM uses two thresholds for lighter and stronger thermal response

**Explanation.** HCTM does not select a fixed clock or power state. It gives the controller two temperature boundaries, TMT1/TMT2. At TMT1 the controller minimizes performance impact; at TMT2 it applies stronger thermal control. Actual hysteresis and internal actions are vendor implementation details.

```text
Read HCTMA/MNTMT/MXTMT
  ↓
Choose TMT1<TMT2
  ↓
Set FID10h
  ↓
Temperature reaches TMT1
  ↓
Temperature reaches TMT2
  ↓
Read SMART counters/latency
```

#### Comparison

| Item | What it answers | Engineering note |
|---|---|---|
| TMT1 | Lighter-control boundary | Objective is to minimize impact |
| TMT2 | Stronger-control boundary | Thermal control takes priority |
| MNTMT/MXTMT | Legal configuration range | Validate on the host first |
| SMART counters | Transition count/time | Evidence that the control loop acted |

**Informative example.** If MNTMT=273 K and MXTMT=373 K, TMT1=343 K and TMT2=353 K are legal, and CDW11=(0157h<<16)+0161h=01570161h. FID 10h is saveable; if SVBL=1 and policy requires persistence, CDW10.SV=1 with FID=10h gives CDW10=80000010h.

**Common mistake / debugging.** Reject TMT1=TMT2, TMT1>TMT2, out-of-range values, or Celsius written directly into Kelvin fields on the host. Hardware validation records ambient, airflow, workload, sensor cadence, and host latency so performance impact remains comparable.

**Supporting sources:** NVME-BASE-2.4 Rev. 2.4, §5.2.30.1.10, printed pp. 471-472, PDF pp. 497-498; NVME-BASE-2.4 Rev. 2.4, §5.2.30.1.10, 8.1.19.5, printed pp. 472, 670-671, PDF pp. 498, 696-697; NVME-BASE-2.4 Rev. 2.4, §5.2.13.1.3, printed pp. 220-225, PDF pp. 246-251

**Related Figures:** Figure 213, Figure 338, Figure 482, Figure 741

### Module 06: Connect policy, state, events, and measurements into reproducible debug evidence

**Explanation.** Power/thermal defects rarely reduce to one wrong bit. Capability, policy, transition, background work, thermal events, and host workload must share one timeline. FID 11h NOPPME, APST, manual PS, HCTM, and RTD3 control different layers and do not replace one another.

```text
Capability snapshot
  ↓
Raw Get/Set commands
  ↓
CQE + timestamp
  ↓
APST/PS transition
  ↓
Temperature/TTC/HCTM
  ↓
I/O latency + recovery decision
```

#### Comparison

| Item | What it answers | Engineering note |
|---|---|---|
| Policy plane | Raw FID02/04/0C/10/11 values | Proves what the host requested |
| State plane | PSD, APST timer, I/O return | Proves controller-state context |
| Thermal plane | Sensors, TTC, HCTM counters | Proves when thermal control acted |
| Outcome plane | CQE, latency, power/temperature trace | Proves impact and recovery |

**Informative example.** Case: APSTE=1 enters PS3 after 2 s idle and NOPPME=0. At 3 s, controller background work cannot raise power. The first read at 4 s returns to an operational state, and its latency spike is compared with PS3.EXLAT. If temperature also crosses TMT1, HCTM counters and the sensor timeline separate exit latency from thermal throttling.

**Common mistake / debugging.** Do not infer cause from one outcome. Establish Set success, follow-up Get value, continuous APST idle time, NOPPME background-power permission, and TMT1/TMT2 crossings before classifying a controller defect.

**Supporting sources:** NVME-BASE-2.4 Rev. 2.4, §5.2.30.1.7, printed pp. 469, PDF pp. 495; NVME-BASE-2.4 Rev. 2.4, §5.2.30.1.11, printed pp. 472-473, PDF pp. 498-499; NVME-BASE-2.4 Rev. 2.4, §8.1.19.4, printed pp. 669-670, PDF pp. 695-696; NVME-BASE-2.4 Rev. 2.4, §5.2.13.1.3, printed pp. 220-225, PDF pp. 246-251; NVME-BASE-2.4 Rev. 2.4, §5.2.12.2, printed pp. 212, PDF pp. 238

**Related Figures:** Figure 202, Figure 213, Figure 340, Figure 478, Figure 483

## Source-located specification findings

The mental model above explains causality. This section preserves each source-located conclusion and its normative strength for speaker notes and review.

### 1. Read before write: Feature capability inventory

<!-- claim:BASEPOWER-READ-FIRST -->

Get Features is the Admin command that retrieves Feature attributes. An engineering flow starts by identifying the FID, querying capability, and retrieving current/default/saved values instead of guessing before a write.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.12, printed pages 209, PDF pages 235

### 2. SEL and FID

<!-- claim:BASEPOWER-GET-SELECT -->

CDW10.SEL selects current=000b, default=001b, saved=010b, or supported capabilities=011b; CDW10.FID selects the Feature. Other SEL encodings are reserved.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.12, printed pages 209-210, PDF pages 235-236

### 3. Saved-value fallback

<!-- claim:BASEPOWER-GET-SAVED -->

If a saved value is requested but saved values are unsupported or none exists, the controller operates using the default value. A successful read therefore does not prove that a value was previously saved.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.12, printed pages 210, PDF pages 236

### 4. UIDX applicability

<!-- claim:BASEPOWER-GET-UIDX -->

CDW14.UIDX is meaningful only when the controller supports the UUID List and the Feature uses a UUID association; otherwise it remains zero.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.12, printed pages 210, PDF pages 236

### 5. CHANG/NSSPEC/SVBL

<!-- claim:BASEPOWER-GET-CAP -->

With SEL=011b, CQE.DW0 reports CHANG, NSSPEC, and SVBL: changeable, namespace-specific, and saveable. These capability bits are distinct from the Feature value and must not be decoded as one.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.12.1, printed pages 211-212, PDF pages 237-238

### 6. Get Features failure evidence

<!-- claim:BASEPOWER-GET-STATUS -->

If Get Features specifies an inapplicable Controller Identifier, command-specific status 1Fh is Invalid Controller Identifier. Debug evidence retains SCT, SC, DNR, CDW10, CDW14, and the target controller.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.12.2, printed pages 212, PDF pages 238

### 7. Set Features data buffer

<!-- claim:BASEPOWER-SET-DPTR -->

Set Features uses DPTR only when the selected Feature defines a data structure. With PRPs, that data buffer shall not cross more than one memory-page boundary because PRP2 cannot point to a PRP List here.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30, printed pages 456-457, PDF pages 482-483

### 8. SV and saveability

<!-- claim:BASEPOWER-SET-SAVE -->

CDW10.SV=1 requests a saved value that can persist across reset/power-cycle boundaries. If the Feature is not saveable, the controller returns Feature Identifier Not Saveable. Read SVBL before setting SV.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30, printed pages 457, PDF pages 483

### 9. Post-success transition boundary

<!-- claim:BASEPOWER-SET-AFTER -->

After Set Features succeeds, subsequent commands shall use the new setting. If software needs a batch of commands to use one consistent setting, the host should allow existing in-flight commands to complete before switching.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30, printed pages 459, PDF pages 485

### 10. Scope and persistence of the five FIDs

<!-- claim:BASEPOWER-FID-SCOPE -->

All five FIDs in this report have Controller scope. FIDs 02h, 04h, 0Ch, and 11h are not saveable; FID 10h is saveable. Only FID 0Ch uses a 256-byte data structure.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30, printed pages 457-459, PDF pages 483-485

### 11. Power-state numbering and limits

<!-- claim:BASEPOWER-POWER-STATES -->

A controller shall support at least one power state and may support up to 32, numbered contiguously from zero. PS0 has the highest maximum power; each subsequent state's maximum power does not exceed the preceding state.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §8.1.19, printed pages 666-667, PDF pages 692-693

### 12. Power State Descriptor mental model

<!-- claim:BASEPOWER-POWER-METRICS -->

A Power State Descriptor (PSD) combines maximum power, operational/non-operational type, entry/exit latency, idle/active power, and relative performance. MP is a sustained maximum; IDLP and ACTP use different measurement conditions and are not interchangeable with an instantaneous sample.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §8.1.19, printed pages 666-668, PDF pages 692-694

### 13. Entry/exit latency calculation

<!-- claim:BASEPOWER-TRANSITION -->

The maximum direct-transition time from an old state to a new state is the old state's EXLAT plus the new state's ENLAT. If a controller transitions through multiple states, the transition times for every segment are summed.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §8.1.19.1, printed pages 668-669, PDF pages 694-695

### 14. Relative-performance interpretation

<!-- claim:BASEPOWER-RELATIVE -->

Relative Read/Write Throughput and Latency use smaller-is-better encodings, but comparisons are valid only within the same characteristic. A throughput code and a latency code are not combined into one score.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §8.1.19.2, printed pages 668, PDF pages 694

### 15. Non-operational is not powered off

<!-- claim:BASEPOWER-NONOP -->

A non-operational power state does not process I/O commands, but may still service properties, PMR, CMB, Admin/background work, or transport-specific accesses. Non-operational does not mean the controller is powered off.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §8.1.19, printed pages 667-668, PDF pages 693-694

### 16. I/O-triggered operational return

<!-- claim:BASEPOWER-NONOP-IO -->

The host should drain I/O before manually entering a non-operational state. If an I/O command arrives, the controller autonomously returns to the most recently used operational state before processing I/O.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §8.1.19, printed pages 668, PDF pages 694

### 17. FID 02h: manual power state

<!-- claim:BASEPOWER-FID02 -->

FID 02h uses CDW11.PS[4:0] to select a power state and WH[7:5] for a workload hint. PS shall be within the range advertised by Identify Controller.NPSS; an unsupported PS should be aborted with Invalid Field in Command.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.2, printed pages 460-461, PDF pages 486-487

### 18. Workload Hint

<!-- claim:BASEPOWER-WORKLOAD -->

WH=000b means unknown workload; 001b represents idle, 32 random 1-MiB writes, then idle; 010b represents 80,000 sequential 128-KiB writes. Encodings 011b through 111b are reserved.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §8.1.19.3, printed pages 669, PDF pages 695

### 19. RTD3E/RTD3R boundary

<!-- claim:BASEPOWER-RTD3 -->

RTD3E and RTD3R describe entry and resume time for evaluating idle break-even in a PCIe D3cold use case; the NVMe text explicitly says these are not D3hot times. Complete PCIe D-state semantics are not present in the supplied source and are not invented here.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §8.1.19.4, printed pages 669-670, PDF pages 695-696

### 20. FID 04h: temperature threshold

<!-- claim:BASEPOWER-FID04 -->

FID 04h sets over/under thresholds for Composite Temperature and up to eight implemented temperature sensors. Temperature is encoded in Kelvin; reaching an over threshold or falling to/below an under threshold may set the SMART/Health Temperature Threshold critical warning and trigger an asynchronous event.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.3, printed pages 462-463, PDF pages 488-489

### 21. Temperature hysteresis

<!-- claim:BASEPOWER-HYST -->

In Figure 470, TMPSEL selects a sensor, THSEL selects over/under, TMPTH is the threshold, and TMPTHH is hysteresis. An over event ends at threshold minus hysteresis; an under event ends at threshold plus hysteresis.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.3.1, printed pages 463-464, PDF pages 489-490

### 22. FID 0Ch: APST enable

<!-- claim:BASEPOWER-FID0C -->

FID 0Ch APSTE=1 enables Autonomous Power State Transition (APST); the default is zero. Enabling it allows controller transitions based on APST-table idle timers; it does not guarantee entry into a particular state.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.7, printed pages 468-469, PDF pages 494-495

### 23. APST 256-byte table

<!-- claim:BASEPOWER-APST-ENTRY -->

The APST data structure is 256 bytes with 32 eight-byte entries. Each entry uses ITPT[31:8] as the idle threshold in milliseconds and ITPS[7:3] as the target non-operational state; ITPT=0 disables that entry.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.7, printed pages 469, PDF pages 495

### 24. APSTE × NOPPME

<!-- claim:BASEPOWER-APST-NOPPME -->

APSTE controls timer-based entry, while NOPPME controls whether controller-initiated background operations may temporarily exceed a non-operational limit. These are orthogonal switches; autonomous state entry does not imply permission to raise power for background work.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.7, printed pages 469, PDF pages 495

### 25. FID 10h: TMT1/TMT2

<!-- claim:BASEPOWER-FID10 -->

FID 10h uses TMT1[31:16] as the lighter thermal-management threshold and TMT2[15:0] as the heavier threshold, both in Kelvin; zero independently disables the corresponding threshold.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.10, printed pages 471-472, PDF pages 497-498

### 26. HCTM control loop

<!-- claim:BASEPOWER-HCTM -->

A nonzero TMT1 shall be less than TMT2, and both shall lie between MNTMT and MXTMT; otherwise the command returns Invalid Field in Command. At TMT1 the controller acts to minimize impact, while TMT2 invokes stronger action; hysteresis is vendor-specific.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.10, 8.1.19.5, printed pages 472, 670-671, PDF pages 498, 696-697

### 27. FID 11h: background-power permission

<!-- claim:BASEPOWER-FID11 -->

FID 11h NOPPME=1 allows a controller-initiated background operation to raise power temporarily, no higher than the last operational state's limit. With NOPPME=0, such work shall not exceed the current non-operational-state limits.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.11, printed pages 472-473, PDF pages 498-499

### 28. SMART/Health verification loop

<!-- claim:BASEPOWER-OBSERVE -->

Successful configuration is not the end of verification. Observe SMART/Health Composite Temperature, the TTC critical warning, warning-temperature time, HCTM transition counters, and implemented sensor readings together with CQE and host latency.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.3, printed pages 220-225, PDF pages 246-251

## Figure index

This report introduces all 27 in-scope Figures. Use the section links below for the 100-minute presentation path; every Figure remains available as an appendix item. 5 Figures are outside the main section range but are included to explain cited dependencies and necessary prerequisites.

- [§5.2](#section-5-2)

- [§8.1](#section-8-1)

- [Referenced Figure dependencies (outside the main section range)](#section-dependency)

## Figure and field-table teaching reference

The source uses Figure numbers for diagrams and field-layout tables. No source artwork is reproduced; compact field and keyword indexes come from the locally verified PDFs.

<a id="section-5-2"></a>

### §5.2

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 197: Get Features – Data Pointer</strong></summary>

<!-- claim:BASEPOWER-FIG-197-CLAIM figure-table:BASEPOWER-FIG-197 -->

**SPEC.** Figure 197, "Get Features – Data Pointer": Maps the power/thermal control relationship represented by Get Features – Data Pointer. Trace selector, state or threshold, transition condition, and observation evidence in order. Source-derived checkpoints: DPTR, PRP1, PRP2.

#### Where this Figure fits

Figure 197 sits in §5.2.12 and acts as a command checkpoint. Read it after the report mental model has established the owning object and before software turns DPTR into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a command-construction field table. Build the common SQE, locate the specified CDW, encode each bit range, clear reserved bits, and validate the result against transfer length, buffer, and completion status. Equal field names do not imply equal semantics across commands.

#### Teaching redraw

```text
[Locate source: DPTR]
          ↓
[Extract field: PRP1] → [Apply encoding: PRP2]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `DPTR` | Data Pointer, the SQE field identifying a command data buffer. |
| `PRP1` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `PRP2` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §5.2.12 is the applicable context.
2. Decode DPTR at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check PRP1 as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 197 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §5.2.12 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes DPTR, PRP1, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §5.2.12, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 197. Annotate the bytes containing DPTR, decode them, and independently verify PRP1. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of DPTR in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand DPTR and state its unit or object scope?
2. Can the reader explain why PRP1 is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** DPTR, PRP1, PRP2

**Source keyword index:** `shall`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.12, Figure 197, printed pages 209, PDF pages 235

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 198: Get Features – Command Dword 10</strong></summary>

<!-- claim:BASEPOWER-FIG-198-CLAIM figure-table:BASEPOWER-FIG-198 -->

**SPEC.** Figure 198, "Get Features – Command Dword 10": Defines the concrete layout or value relationships for Get Features – Command Dword 10. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is SEL, FID.

#### Where this Figure fits

Figure 198 sits in §5.2.12 and acts as a command checkpoint. Read it after the report mental model has established the owning object and before software turns SEL into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a command-construction field table. Build the common SQE, locate the specified CDW, encode each bit range, clear reserved bits, and validate the result against transfer length, buffer, and completion status. Equal field names do not imply equal semantics across commands.

#### Teaching redraw

```text
[Locate source: SEL]
          ↓
[Extract field: FID] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `SEL` | Select, the Get Features field choosing current, default, saved, or supported-capabilities view. |
| `FID` | Feature Identifier, the eight-bit identifier selecting a function in Get/Set Features. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §5.2.12 is the applicable context.
2. Decode SEL at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check FID as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 198 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §5.2.12 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes SEL, FID, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §5.2.12, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 198. Annotate the bytes containing SEL, decode them, and independently verify FID. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of SEL in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand SEL and state its unit or object scope?
2. Can the reader explain why FID is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** SEL, FID

**Source keyword index:** `shall`, `optional`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.12, Figure 198, printed pages 209-210, PDF pages 235-236

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 199: Get Features – Command Dword 14</strong></summary>

<!-- claim:BASEPOWER-FIG-199-CLAIM figure-table:BASEPOWER-FIG-199 -->

**SPEC.** Figure 199, "Get Features – Command Dword 14": Defines the concrete layout or value relationships for Get Features – Command Dword 14. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is UIDX.

#### Where this Figure fits

Figure 199 sits in §5.2.12 and acts as a command checkpoint. Read it after the report mental model has established the owning object and before software turns UIDX into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a command-construction field table. Build the common SQE, locate the specified CDW, encode each bit range, clear reserved bits, and validate the result against transfer length, buffer, and completion status. Equal field names do not imply equal semantics across commands.

#### Teaching redraw

```text
[Locate source: UIDX]
          ↓
[Extract field: evidence] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `UIDX` | UUID Index, an index into the UUID List; zero indicates that no UUID is specified. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §5.2.12 is the applicable context.
2. Decode UIDX at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check the cited condition as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 199 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §5.2.12 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes UIDX, the cited condition, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §5.2.12, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 199. Annotate the bytes containing UIDX, decode them, and independently verify the cited condition. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of UIDX in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand UIDX and state its unit or object scope?
2. Can the reader explain why the cited condition is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** UIDX

**Source keyword index:** `may`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.12, Figure 199, printed pages 210, PDF pages 236

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 200: Feature Identifiers for Get Features</strong></summary>

<!-- claim:BASEPOWER-FIG-200-CLAIM figure-table:BASEPOWER-FIG-200 -->

**SPEC.** Figure 200, "Feature Identifiers for Get Features": Defines the identifier composition or namespace of values shown by Feature Identifiers for Get Features. Keep the value width, issuing authority, uniqueness scope, and reserved values separate. Evidence index: FID 02h, FID 04h, FID 0Ch, FID 10h, FID 11h.

#### Where this Figure fits

Figure 200 sits in §5.2.12 and acts as a identifier checkpoint. Read it after the report mental model has established the owning object and before software turns FID 02h into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is an identifier-format Figure. Record width and encoding, then identify assignment authority, uniqueness scope, reserved values, and lifetime. Equal-width identifiers are not automatically interchangeable.

#### Teaching redraw

```text
[Locate source: FID 02h]
          ↓
[Extract field: FID 04h] → [Apply encoding: FID 0Ch]
                                      ↓
[Validate evidence: FID 10h]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `FID 02h` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `FID 04h` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `FID 0Ch` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `FID 10h` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `FID 11h` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §5.2.12 is the applicable context.
2. Decode FID 02h at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check FID 04h as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 200 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §5.2.12 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes FID 02h, FID 04h, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §5.2.12, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 200. Annotate the bytes containing FID 02h, decode them, and independently verify FID 04h. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of FID 02h in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand FID 02h and state its unit or object scope?
2. Can the reader explain why FID 04h is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** FID 02h, FID 04h, FID 0Ch, FID 10h, FID 11h

**Source keyword index:** `may`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.12, Figure 200, printed pages 210-211, PDF pages 236-237

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 201: Get Features – Select Supported Capabilities</strong></summary>

<!-- claim:BASEPOWER-FIG-201-CLAIM figure-table:BASEPOWER-FIG-201 -->

**SPEC.** Figure 201, "Get Features – Select Supported Capabilities": Defines the concrete layout or value relationships for Get Features – Select Supported Capabilities. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is CHANG, NSSPEC, SVBL.

#### Where this Figure fits

Figure 201 sits in §5.2.12.2 and acts as a relationship checkpoint. Read it after the report mental model has established the owning object and before software turns CHANG into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This Figure explains a specific relationship or example. Identify each component type and owner, then decide whether each connection represents data flow, control flow, containment, or a condition. Visual placement alone creates no normative requirement.

#### Teaching redraw

```text
[Locate source: CHANG]
          ↓
[Extract field: NSSPEC] → [Apply encoding: SVBL]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `CHANG` | Changeable, the capability bit indicating whether Set Features can modify the Feature value. |
| `NSSPEC` | Namespace Specific, the capability bit indicating whether a Feature has per-namespace scope. |
| `SVBL` | Saveable, the supported-capabilities bit indicating whether a Feature can be saved. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §5.2.12.2 is the applicable context.
2. Decode CHANG at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check NSSPEC as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 201 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §5.2.12.2 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes CHANG, NSSPEC, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §5.2.12.2, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 201. Annotate the bytes containing CHANG, decode them, and independently verify NSSPEC. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of CHANG in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand CHANG and state its unit or object scope?
2. Can the reader explain why NSSPEC is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** CHANG, NSSPEC, SVBL

**Source keyword index:** `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.12.2, Figure 201, printed pages 212, PDF pages 238

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 202: Get Features – Command Specific Status Values</strong></summary>

<!-- claim:BASEPOWER-FIG-202-CLAIM figure-table:BASEPOWER-FIG-202 -->

**SPEC.** Figure 202, "Get Features – Command Specific Status Values": Defines the concrete layout or value relationships for Get Features – Command Specific Status Values. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is Invalid Controller Identifier.

#### Where this Figure fits

Figure 202 sits in §5.2.12.2 and acts as a layout checkpoint. Read it after the report mental model has established the owning object and before software turns Invalid Controller Identifier into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a structure or capability field table. Locate it using the structure base and offset, read in byte/bit order, and separate capability gates, value encoding, and reserved areas. Presence in the table does not mean the function is supported.

#### Teaching redraw

```text
[Locate source: Invalid Controller Identifier]
          ↓
[Extract field: evidence] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `Invalid Controller Identifier` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §5.2.12.2 is the applicable context.
2. Decode Invalid Controller Identifier at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check the cited condition as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 202 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §5.2.12.2 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes Invalid Controller Identifier, the cited condition, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §5.2.12.2, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 202. Annotate the bytes containing Invalid Controller Identifier, decode them, and independently verify the cited condition. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of Invalid Controller Identifier in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand Invalid Controller Identifier and state its unit or object scope?
2. Can the reader explain why the cited condition is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** Invalid Controller Identifier

**Source keyword index:** none

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.12.2, Figure 202, printed pages 212, PDF pages 238

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 463: Set Features – Data Pointer</strong></summary>

<!-- claim:BASEPOWER-FIG-463-CLAIM figure-table:BASEPOWER-FIG-463 -->

**SPEC.** Figure 463, "Set Features – Data Pointer": Maps the power/thermal control relationship represented by Set Features – Data Pointer. Trace selector, state or threshold, transition condition, and observation evidence in order. Source-derived checkpoints: DPTR, PRP1, PRP2.

#### Where this Figure fits

Figure 463 sits in §5.2.30 and acts as a command checkpoint. Read it after the report mental model has established the owning object and before software turns DPTR into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a command-construction field table. Build the common SQE, locate the specified CDW, encode each bit range, clear reserved bits, and validate the result against transfer length, buffer, and completion status. Equal field names do not imply equal semantics across commands.

#### Teaching redraw

```text
[Locate source: DPTR]
          ↓
[Extract field: PRP1] → [Apply encoding: PRP2]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `DPTR` | Data Pointer, the SQE field identifying a command data buffer. |
| `PRP1` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `PRP2` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §5.2.30 is the applicable context.
2. Decode DPTR at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check PRP1 as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 463 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §5.2.30 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes DPTR, PRP1, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §5.2.30, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 463. Annotate the bytes containing DPTR, decode them, and independently verify PRP1. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of DPTR in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand DPTR and state its unit or object scope?
2. Can the reader explain why PRP1 is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** DPTR, PRP1, PRP2

**Source keyword index:** `shall not`, `shall`, `may`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30, Figure 463, printed pages 456, PDF pages 482

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 464: Set Features – Command Dword 10</strong></summary>

<!-- claim:BASEPOWER-FIG-464-CLAIM figure-table:BASEPOWER-FIG-464 -->

**SPEC.** Figure 464, "Set Features – Command Dword 10": Defines the concrete layout or value relationships for Set Features – Command Dword 10. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is SV, FID.

#### Where this Figure fits

Figure 464 sits in §5.2.30 and acts as a command checkpoint. Read it after the report mental model has established the owning object and before software turns SV into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a command-construction field table. Build the common SQE, locate the specified CDW, encode each bit range, clear reserved bits, and validate the result against transfer length, buffer, and completion status. Equal field names do not imply equal semantics across commands.

#### Teaching redraw

```text
[Locate source: SV]
          ↓
[Extract field: FID] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `SV` | Save, the Set Features bit requesting that the controller also save the configured value. |
| `FID` | Feature Identifier, the eight-bit identifier selecting a function in Get/Set Features. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §5.2.30 is the applicable context.
2. Decode SV at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check FID as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 464 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §5.2.30 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes SV, FID, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §5.2.30, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 464. Annotate the bytes containing SV, decode them, and independently verify FID. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of SV in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand SV and state its unit or object scope?
2. Can the reader explain why FID is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** SV, FID

**Source keyword index:** `shall`, `optional`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30, Figure 464, printed pages 457, PDF pages 483

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 465: Set Features – Command Dword 14</strong></summary>

<!-- claim:BASEPOWER-FIG-465-CLAIM figure-table:BASEPOWER-FIG-465 -->

**SPEC.** Figure 465, "Set Features – Command Dword 14": Defines the concrete layout or value relationships for Set Features – Command Dword 14. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is UIDX.

#### Where this Figure fits

Figure 465 sits in §5.2.30 and acts as a command checkpoint. Read it after the report mental model has established the owning object and before software turns UIDX into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a command-construction field table. Build the common SQE, locate the specified CDW, encode each bit range, clear reserved bits, and validate the result against transfer length, buffer, and completion status. Equal field names do not imply equal semantics across commands.

#### Teaching redraw

```text
[Locate source: UIDX]
          ↓
[Extract field: evidence] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `UIDX` | UUID Index, an index into the UUID List; zero indicates that no UUID is specified. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §5.2.30 is the applicable context.
2. Decode UIDX at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check the cited condition as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 465 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §5.2.30 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes UIDX, the cited condition, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §5.2.30, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 465. Annotate the bytes containing UIDX, decode them, and independently verify the cited condition. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of UIDX in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand UIDX and state its unit or object scope?
2. Can the reader explain why the cited condition is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** UIDX

**Source keyword index:** `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30, Figure 465, printed pages 457, PDF pages 483

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 466: Feature Identifiers for Set Features</strong></summary>

<!-- claim:BASEPOWER-FIG-466-CLAIM figure-table:BASEPOWER-FIG-466 -->

**SPEC.** Figure 466, "Feature Identifiers for Set Features": Defines the identifier composition or namespace of values shown by Feature Identifiers for Set Features. Keep the value width, issuing authority, uniqueness scope, and reserved values separate. Evidence index: FID 02h, FID 04h, FID 0Ch, FID 10h, FID 11h.

#### Where this Figure fits

Figure 466 sits in §5.2.30 and acts as a identifier checkpoint. Read it after the report mental model has established the owning object and before software turns FID 02h into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is an identifier-format Figure. Record width and encoding, then identify assignment authority, uniqueness scope, reserved values, and lifetime. Equal-width identifiers are not automatically interchangeable.

#### Teaching redraw

```text
[Locate source: FID 02h]
          ↓
[Extract field: FID 04h] → [Apply encoding: FID 0Ch]
                                      ↓
[Validate evidence: FID 10h]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `FID 02h` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `FID 04h` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `FID 0Ch` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `FID 10h` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `FID 11h` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §5.2.30 is the applicable context.
2. Decode FID 02h at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check FID 04h as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 466 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §5.2.30 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes FID 02h, FID 04h, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §5.2.30, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 466. Annotate the bytes containing FID 02h, decode them, and independently verify FID 04h. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of FID 02h in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand FID 02h and state its unit or object scope?
2. Can the reader explain why FID 04h is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** FID 02h, FID 04h, FID 0Ch, FID 10h, FID 11h

**Source keyword index:** `shall`, `should`, `may`, `optional`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30, Figure 466, printed pages 457-459, PDF pages 483-485

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 468: Power Management – Command Dword 11</strong></summary>

<!-- claim:BASEPOWER-FIG-468-CLAIM figure-table:BASEPOWER-FIG-468 -->

**SPEC.** Figure 468, "Power Management – Command Dword 11": Defines the concrete layout or value relationships for Power Management – Command Dword 11. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is WH, PS.

#### Where this Figure fits

Figure 468 sits in §5.2.30.1.2 and acts as a command checkpoint. Read it after the report mental model has established the owning object and before software turns WH into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a command-construction field table. Build the common SQE, locate the specified CDW, encode each bit range, clear reserved bits, and validate the result against transfer length, buffer, and completion status. Equal field names do not imply equal semantics across commands.

#### Teaching redraw

```text
[Locate source: WH]
          ↓
[Extract field: PS] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `WH` | Workload Hint, a host-supplied workload category hint rather than a performance guarantee. |
| `PS` | Power State, a controller power/performance operating point; PS0 has the highest maximum power. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §5.2.30.1.2 is the applicable context.
2. Decode WH at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check PS as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 468 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §5.2.30.1.2 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes WH, PS, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §5.2.30.1.2, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 468. Annotate the bytes containing WH, decode them, and independently verify PS. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of WH in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand WH and state its unit or object scope?
2. Can the reader explain why PS is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** WH, PS

**Source keyword index:** `shall not`, `shall`, `should`, `may`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.2, Figure 468, printed pages 461, PDF pages 487

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 470: Temperature Threshold – Command Dword 11</strong></summary>

<!-- claim:BASEPOWER-FIG-470-CLAIM figure-table:BASEPOWER-FIG-470 -->

**SPEC.** Figure 470, "Temperature Threshold – Command Dword 11": Defines the concrete layout or value relationships for Temperature Threshold – Command Dword 11. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is TMPTHH, THSEL, TMPSEL, TMPTH.

#### Where this Figure fits

Figure 470 sits in §5.2.30.1.3.1 and acts as a command checkpoint. Read it after the report mental model has established the owning object and before software turns TMPTHH into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a command-construction field table. Build the common SQE, locate the specified CDW, encode each bit range, clear reserved bits, and validate the result against transfer length, buffer, and completion status. Equal field names do not imply equal semantics across commands.

#### Teaching redraw

```text
[Locate source: TMPTHH]
          ↓
[Extract field: THSEL] → [Apply encoding: TMPSEL]
                                      ↓
[Validate evidence: TMPTH]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `TMPTHH` | Temperature Threshold Hysteresis, Kelvin hysteresis used when ending a threshold event. |
| `THSEL` | Threshold Type Select, choosing an over-temperature or under-temperature threshold. |
| `TMPSEL` | Temperature Sensor Select, the field choosing Composite Temperature or sensor 1 through 8. |
| `TMPTH` | Temperature Threshold, a 16-bit threshold value in Kelvin. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §5.2.30.1.3.1 is the applicable context.
2. Decode TMPTHH at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check THSEL as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 470 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §5.2.30.1.3.1 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes TMPTHH, THSEL, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §5.2.30.1.3.1, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 470. Annotate the bytes containing TMPTHH, decode them, and independently verify THSEL. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of TMPTHH in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand TMPTHH and state its unit or object scope?
2. Can the reader explain why THSEL is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** TMPTHH, THSEL, TMPSEL, TMPTH

**Source keyword index:** `shall`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.3.1, Figure 470, printed pages 463-464, PDF pages 489-490

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 475: Autonomous Power State Transition – Command Dword 11</strong></summary>

<!-- claim:BASEPOWER-FIG-475-CLAIM figure-table:BASEPOWER-FIG-475 -->

**SPEC.** Figure 475, "Autonomous Power State Transition – Command Dword 11": Defines the concrete layout or value relationships for Autonomous Power State Transition – Command Dword 11. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is APSTE.

#### Where this Figure fits

Figure 475 sits in §5.2.30.1.7 and acts as a command checkpoint. Read it after the report mental model has established the owning object and before software turns APSTE into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a command-construction field table. Build the common SQE, locate the specified CDW, encode each bit range, clear reserved bits, and validate the result against transfer length, buffer, and completion status. Equal field names do not imply equal semantics across commands.

#### Teaching redraw

```text
[Locate source: APSTE]
          ↓
[Extract field: evidence] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `APSTE` | Autonomous Power State Transition Enable, the bit enabling APST-table timer evaluation. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §5.2.30.1.7 is the applicable context.
2. Decode APSTE at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check the cited condition as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 475 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §5.2.30.1.7 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes APSTE, the cited condition, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §5.2.30.1.7, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 475. Annotate the bytes containing APSTE, decode them, and independently verify the cited condition. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of APSTE in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand APSTE and state its unit or object scope?
2. Can the reader explain why the cited condition is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** APSTE

**Source keyword index:** `shall`, `may`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.7, Figure 475, printed pages 468, PDF pages 494

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 476: Autonomous Power State Transition Data Structure</strong></summary>

<!-- claim:BASEPOWER-FIG-476-CLAIM figure-table:BASEPOWER-FIG-476 -->

**SPEC.** Figure 476, "Autonomous Power State Transition Data Structure": Defines the concrete layout or value relationships for Autonomous Power State Transition Data Structure. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is 32 entries, 256 bytes.

#### Where this Figure fits

Figure 476 sits in §5.2.30.1.7 and acts as a state checkpoint. Read it after the report mental model has established the owning object and before software turns 32 entries into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a state or timing Figure. Follow each arrow while recording trigger, observer, completion condition, and timeout source. Similar state names under different reset scopes do not imply preservation of the same queue or controller state.

#### Teaching redraw

```text
[Locate source: 32 entries]
          ↓
[Extract field: 256 bytes] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `32 entries` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `256 bytes` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §5.2.30.1.7 is the applicable context.
2. Decode 32 entries at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check 256 bytes as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 476 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §5.2.30.1.7 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes 32 entries, 256 bytes, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §5.2.30.1.7, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 476. Annotate the bytes containing 32 entries, decode them, and independently verify 256 bytes. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of 32 entries in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand 32 entries and state its unit or object scope?
2. Can the reader explain why 256 bytes is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** 32 entries, 256 bytes

**Source keyword index:** none

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.7, Figure 476, printed pages 469, PDF pages 495

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 477: Autonomous Power State Transition Entry</strong></summary>

<!-- claim:BASEPOWER-FIG-477-CLAIM figure-table:BASEPOWER-FIG-477 -->

**SPEC.** Figure 477, "Autonomous Power State Transition Entry": Shows the state or timing progression represented by Autonomous Power State Transition Entry. Follow the states or time bounds in arrow order and identify which actor observes each transition. Evidence index: ITPT, ITPS.

#### Where this Figure fits

Figure 477 sits in §5.2.30.1.7 and acts as a state checkpoint. Read it after the report mental model has established the owning object and before software turns ITPT into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a state or timing Figure. Follow each arrow while recording trigger, observer, completion condition, and timeout source. Similar state names under different reset scopes do not imply preservation of the same queue or controller state.

#### Teaching redraw

```text
[Locate source: ITPT]
          ↓
[Extract field: ITPS] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `ITPT` | Idle Time Prior to Transition, the APST-entry idle threshold in milliseconds. |
| `ITPS` | Idle Transition Power State, the target non-operational power state selected by an APST entry. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §5.2.30.1.7 is the applicable context.
2. Decode ITPT at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check ITPS as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 477 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §5.2.30.1.7 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes ITPT, ITPS, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §5.2.30.1.7, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 477. Annotate the bytes containing ITPT, decode them, and independently verify ITPS. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of ITPT in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand ITPT and state its unit or object scope?
2. Can the reader explain why ITPS is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** ITPT, ITPS

**Source keyword index:** `should not`, `shall`, `should`, `may`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.7, Figure 477, printed pages 469, PDF pages 495

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 478: APST and NOPPME Interaction</strong></summary>

<!-- claim:BASEPOWER-FIG-478-CLAIM figure-table:BASEPOWER-FIG-478 -->

**SPEC.** Figure 478, "APST and NOPPME Interaction": Maps the power/thermal control relationship represented by APST and NOPPME Interaction. Trace selector, state or threshold, transition condition, and observation evidence in order. Source-derived checkpoints: APSTE, NOPPME, host entry, timer entry, background operations.

#### Where this Figure fits

Figure 478 sits in §5.2.30.1.7 and acts as a relationship checkpoint. Read it after the report mental model has established the owning object and before software turns APSTE into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This Figure explains a specific relationship or example. Identify each component type and owner, then decide whether each connection represents data flow, control flow, containment, or a condition. Visual placement alone creates no normative requirement.

#### Teaching redraw

```text
[Locate source: APSTE]
          ↓
[Extract field: NOPPME] → [Apply encoding: host entry]
                                      ↓
[Validate evidence: timer entry]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `APSTE` | Autonomous Power State Transition Enable, the bit enabling APST-table timer evaluation. |
| `NOPPME` | Non-Operational Power State Permissive Mode Enable, controlling whether controller background work may temporarily exceed a non-operational power limit. |
| `host entry` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `timer entry` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `background operations` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §5.2.30.1.7 is the applicable context.
2. Decode APSTE at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check NOPPME as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 478 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §5.2.30.1.7 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes APSTE, NOPPME, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §5.2.30.1.7, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 478. Annotate the bytes containing APSTE, decode them, and independently verify NOPPME. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of APSTE in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand APSTE and state its unit or object scope?
2. Can the reader explain why NOPPME is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** APSTE, NOPPME, host entry, timer entry, background operations

**Source keyword index:** none

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.7, Figure 478, printed pages 469, PDF pages 495

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 482: Host Controlled Thermal Management – Command Dword 11</strong></summary>

<!-- claim:BASEPOWER-FIG-482-CLAIM figure-table:BASEPOWER-FIG-482 -->

**SPEC.** Figure 482, "Host Controlled Thermal Management – Command Dword 11": Defines the concrete layout or value relationships for Host Controlled Thermal Management – Command Dword 11. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is TMT1, TMT2.

#### Where this Figure fits

Figure 482 sits in §5.2.30.1.10 and acts as a command checkpoint. Read it after the report mental model has established the owning object and before software turns TMT1 into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a command-construction field table. Build the common SQE, locate the specified CDW, encode each bit range, clear reserved bits, and validate the result against transfer length, buffer, and completion status. Equal field names do not imply equal semantics across commands.

#### Teaching redraw

```text
[Locate source: TMT1]
          ↓
[Extract field: TMT2] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `TMT1` | Thermal Management Temperature 1, the lighter thermal-management threshold in Kelvin. |
| `TMT2` | Thermal Management Temperature 2, the stronger thermal-management threshold in Kelvin. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §5.2.30.1.10 is the applicable context.
2. Decode TMT1 at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check TMT2 as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 482 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §5.2.30.1.10 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes TMT1, TMT2, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §5.2.30.1.10, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 482. Annotate the bytes containing TMT1, decode them, and independently verify TMT2. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of TMT1 in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand TMT1 and state its unit or object scope?
2. Can the reader explain why TMT2 is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** TMT1, TMT2

**Source keyword index:** `shall`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.10, Figure 482, printed pages 472, PDF pages 498

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 483: Non-Operational Power State Configuration – Command Dword 11</strong></summary>

<!-- claim:BASEPOWER-FIG-483-CLAIM figure-table:BASEPOWER-FIG-483 -->

**SPEC.** Figure 483, "Non-Operational Power State Configuration – Command Dword 11": Defines the concrete layout or value relationships for Non-Operational Power State Configuration – Command Dword 11. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is NOPPME.

#### Where this Figure fits

Figure 483 sits in §5.2.30.1.11 and acts as a command checkpoint. Read it after the report mental model has established the owning object and before software turns NOPPME into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a command-construction field table. Build the common SQE, locate the specified CDW, encode each bit range, clear reserved bits, and validate the result against transfer length, buffer, and completion status. Equal field names do not imply equal semantics across commands.

#### Teaching redraw

```text
[Locate source: NOPPME]
          ↓
[Extract field: evidence] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `NOPPME` | Non-Operational Power State Permissive Mode Enable, controlling whether controller background work may temporarily exceed a non-operational power limit. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §5.2.30.1.11 is the applicable context.
2. Decode NOPPME at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check the cited condition as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 483 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §5.2.30.1.11 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes NOPPME, the cited condition, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §5.2.30.1.11, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 483. Annotate the bytes containing NOPPME, decode them, and independently verify the cited condition. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of NOPPME in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand NOPPME and state its unit or object scope?
2. Can the reader explain why the cited condition is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** NOPPME

**Source keyword index:** `shall not`, `shall`, `may`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.11, Figure 483, printed pages 472-473, PDF pages 498-499

</details>

<a id="section-8-1"></a>

### §8.1

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 738: Power Management Overview</strong></summary>

<!-- claim:BASEPOWER-FIG-738-CLAIM figure-table:BASEPOWER-FIG-738 -->

**SPEC.** Figure 738, "Power Management Overview": Maps the power/thermal control relationship represented by Power Management Overview. Trace selector, state or threshold, transition condition, and observation evidence in order. Source-derived checkpoints: Static Power Management, Dynamic Power Management, Power State Descriptor.

#### Where this Figure fits

Figure 738 sits in §8.1.19 and acts as a relationship checkpoint. Read it after the report mental model has established the owning object and before software turns Static Power Management into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This Figure explains a specific relationship or example. Identify each component type and owner, then decide whether each connection represents data flow, control flow, containment, or a condition. Visual placement alone creates no normative requirement.

#### Teaching redraw

```text
[Locate source: Static Power Management]
          ↓
[Extract field: Dynamic Power Management] → [Apply encoding: Power State Descriptor]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `Static Power Management` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `Dynamic Power Management` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `Power State Descriptor` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §8.1.19 is the applicable context.
2. Decode Static Power Management at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check Dynamic Power Management as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 738 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §8.1.19 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes Static Power Management, Dynamic Power Management, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §8.1.19, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 738. Annotate the bytes containing Static Power Management, decode them, and independently verify Dynamic Power Management. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of Static Power Management in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand Static Power Management and state its unit or object scope?
2. Can the reader explain why Dynamic Power Management is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** Static Power Management, Dynamic Power Management, Power State Descriptor

**Source keyword index:** none

> Source: NVME-BASE-2.4, Rev. 2.4, §8.1.19, Figure 738, printed pages 666, PDF pages 692

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 739: Power State Characteristics</strong></summary>

<!-- claim:BASEPOWER-FIG-739-CLAIM figure-table:BASEPOWER-FIG-739 -->

**SPEC.** Figure 739, "Power State Characteristics": Shows the state or timing progression represented by Power State Characteristics. Follow the states or time bounds in arrow order and identify which actor observes each transition. Evidence index: MP, IDLP, ACTP, ENLAT, EXLAT.

#### Where this Figure fits

Figure 739 sits in §8.1.19 and acts as a state checkpoint. Read it after the report mental model has established the owning object and before software turns MP into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a state or timing Figure. Follow each arrow while recording trigger, observer, completion condition, and timeout source. Similar state names under different reset scopes do not imply preservation of the same queue or controller state.

#### Teaching redraw

```text
[Locate source: MP]
          ↓
[Extract field: IDLP] → [Apply encoding: ACTP]
                                      ↓
[Validate evidence: ENLAT]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `MP` | Maximum Power, the sustained maximum power of a power state. |
| `IDLP` | Idle Power, typical power under the specification's idle measurement conditions. |
| `ACTP` | Active Power, average active power under the specified workload and time window. |
| `ENLAT` | Entry Latency, the maximum latency to enter a power state, in microseconds. |
| `EXLAT` | Exit Latency, the maximum latency to exit a power state, in microseconds. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §8.1.19 is the applicable context.
2. Decode MP at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check IDLP as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 739 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §8.1.19 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes MP, IDLP, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §8.1.19, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 739. Annotate the bytes containing MP, decode them, and independently verify IDLP. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of MP in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand MP and state its unit or object scope?
2. Can the reader explain why IDLP is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** MP, IDLP, ACTP, ENLAT, EXLAT

**Source keyword index:** none

> Source: NVME-BASE-2.4, Rev. 2.4, §8.1.19, Figure 739, printed pages 667, PDF pages 693

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 740: Workload Hints</strong></summary>

<!-- claim:BASEPOWER-FIG-740-CLAIM figure-table:BASEPOWER-FIG-740 -->

**SPEC.** Figure 740, "Workload Hints": Maps the power/thermal control relationship represented by Workload Hints. Trace selector, state or threshold, transition condition, and observation evidence in order. Source-derived checkpoints: WH 000b, WH 001b, WH 010b.

#### Where this Figure fits

Figure 740 sits in §8.1.19.3 and acts as a relationship checkpoint. Read it after the report mental model has established the owning object and before software turns WH 000b into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This Figure explains a specific relationship or example. Identify each component type and owner, then decide whether each connection represents data flow, control flow, containment, or a condition. Visual placement alone creates no normative requirement.

#### Teaching redraw

```text
[Locate source: WH 000b]
          ↓
[Extract field: WH 001b] → [Apply encoding: WH 010b]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `WH 000b` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `WH 001b` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `WH 010b` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §8.1.19.3 is the applicable context.
2. Decode WH 000b at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check WH 001b as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 740 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §8.1.19.3 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes WH 000b, WH 001b, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §8.1.19.3, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 740. Annotate the bytes containing WH 000b, decode them, and independently verify WH 001b. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of WH 000b in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand WH 000b and state its unit or object scope?
2. Can the reader explain why WH 001b is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** WH 000b, WH 001b, WH 010b

**Source keyword index:** none

> Source: NVME-BASE-2.4, Rev. 2.4, §8.1.19.3, Figure 740, printed pages 669, PDF pages 695

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 741: Host Controlled Thermal Management</strong></summary>

<!-- claim:BASEPOWER-FIG-741-CLAIM figure-table:BASEPOWER-FIG-741 -->

**SPEC.** Figure 741, "Host Controlled Thermal Management": Maps the power/thermal control relationship represented by Host Controlled Thermal Management. Trace selector, state or threshold, transition condition, and observation evidence in order. Source-derived checkpoints: TMT1, TMT2, hysteresis, thermal throttling.

#### Where this Figure fits

Figure 741 sits in §8.1.19.5 and acts as a relationship checkpoint. Read it after the report mental model has established the owning object and before software turns TMT1 into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This Figure explains a specific relationship or example. Identify each component type and owner, then decide whether each connection represents data flow, control flow, containment, or a condition. Visual placement alone creates no normative requirement.

#### Teaching redraw

```text
[Locate source: TMT1]
          ↓
[Extract field: TMT2] → [Apply encoding: hysteresis]
                                      ↓
[Validate evidence: thermal throttling]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `TMT1` | Thermal Management Temperature 1, the lighter thermal-management threshold in Kelvin. |
| `TMT2` | Thermal Management Temperature 2, the stronger thermal-management threshold in Kelvin. |
| `hysteresis` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `thermal throttling` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §8.1.19.5 is the applicable context.
2. Decode TMT1 at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check TMT2 as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 741 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §8.1.19.5 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes TMT1, TMT2, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §8.1.19.5, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 741. Annotate the bytes containing TMT1, decode them, and independently verify TMT2. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of TMT1 in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand TMT1 and state its unit or object scope?
2. Can the reader explain why TMT2 is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** TMT1, TMT2, hysteresis, thermal throttling

**Source keyword index:** none

> Source: NVME-BASE-2.4, Rev. 2.4, §8.1.19.5, Figure 741, printed pages 671, PDF pages 697

</details>

<a id="section-dependency"></a>

### Referenced Figure dependencies (outside the main section range)

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 93: Common Command Format</strong></summary>

<!-- claim:BASEPOWER-FIG-093-CLAIM figure-table:BASEPOWER-FIG-093 -->

**SPEC.** Figure 93, "Common Command Format": Defines the concrete layout or value relationships for Common Command Format. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is OPC, CID, NSID, MPTR, DPTR, CDW10-CDW15.

#### Where this Figure fits

Figure 93 sits in §4.1.1 and acts as a command checkpoint. Read it after the report mental model has established the owning object and before software turns OPC into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a command-construction field table. Build the common SQE, locate the specified CDW, encode each bit range, clear reserved bits, and validate the result against transfer length, buffer, and completion status. Equal field names do not imply equal semantics across commands.

#### Teaching redraw

```text
[Locate source: OPC]
          ↓
[Extract field: CID] → [Apply encoding: NSID]
                                      ↓
[Validate evidence: MPTR]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `OPC` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `CID` | Command Identifier, used with the SQ identifier to identify an outstanding command. |
| `NSID` | Namespace Identifier, a controller-visible numeric handle for a namespace; the identifier is not the namespace object itself. |
| `MPTR` | Metadata Pointer, the SQE field identifying a separate metadata buffer. |
| `DPTR` | Data Pointer, the SQE field identifying a command data buffer. |
| `CDW10-CDW15` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §4.1.1 is the applicable context.
2. Decode OPC at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check CID as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 93 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §4.1.1 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes OPC, CID, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §4.1.1, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 93. Annotate the bytes containing OPC, decode them, and independently verify CID. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of OPC in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand OPC and state its unit or object scope?
2. Can the reader explain why CID is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** OPC, CID, NSID, MPTR, DPTR, CDW10-CDW15

**Source keyword index:** `shall`, `may`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §4.1.1, Figure 93, printed pages 140-142, PDF pages 166-168

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 213: SMART / Health Information Log</strong></summary>

<!-- claim:BASEPOWER-FIG-213-CLAIM figure-table:BASEPOWER-FIG-213 -->

**SPEC.** Figure 213, "SMART / Health Information Log": Defines the concrete layout or value relationships for SMART / Health Information Log. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is Composite Temperature, TTC, Temperature Sensor, HCTM counters.

#### Where this Figure fits

Figure 213 sits in §5.2.13.1.3 and acts as a layout checkpoint. Read it after the report mental model has established the owning object and before software turns Composite Temperature into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a structure or capability field table. Locate it using the structure base and offset, read in byte/bit order, and separate capability gates, value encoding, and reserved areas. Presence in the table does not mean the function is supported.

#### Teaching redraw

```text
[Locate source: Composite Temperature]
          ↓
[Extract field: TTC] → [Apply encoding: Temperature Sensor]
                                      ↓
[Validate evidence: HCTM counters]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `Composite Temperature` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `TTC` | Temperature Threshold Critical Warning, the temperature-threshold bit in SMART/Health Critical Warning. |
| `Temperature Sensor` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `HCTM counters` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §5.2.13.1.3 is the applicable context.
2. Decode Composite Temperature at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check TTC as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 213 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §5.2.13.1.3 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes Composite Temperature, TTC, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §5.2.13.1.3, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 213. Annotate the bytes containing Composite Temperature, decode them, and independently verify TTC. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of Composite Temperature in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand Composite Temperature and state its unit or object scope?
2. Can the reader explain why TTC is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** Composite Temperature, TTC, Temperature Sensor, HCTM counters

**Source keyword index:** `shall not`, `shall`, `may`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.3, Figure 213, printed pages 220-225, PDF pages 246-251

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 338: Identify Controller Data Structure</strong></summary>

<!-- claim:BASEPOWER-FIG-338-CLAIM figure-table:BASEPOWER-FIG-338 -->

**SPEC.** Figure 338, "Identify Controller Data Structure": Defines the concrete layout or value relationships for Identify Controller Data Structure. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is NPSS, APSTA, HCTMA, WCTEMP, MNTMT, MXTMT, RTD3E, RTD3R.

#### Where this Figure fits

Figure 338 sits in §5.2.14.2.1 and acts as a layout checkpoint. Read it after the report mental model has established the owning object and before software turns NPSS into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a structure or capability field table. Locate it using the structure base and offset, read in byte/bit order, and separate capability gates, value encoding, and reserved areas. Presence in the table does not mean the function is supported.

#### Teaching redraw

```text
[Locate source: NPSS]
          ↓
[Extract field: APSTA] → [Apply encoding: HCTMA]
                                      ↓
[Validate evidence: WCTEMP]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `NPSS` | Number of Power States Support, the zero-based field reporting the highest supported power-state number. |
| `APSTA` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `HCTMA` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `WCTEMP` | Warning Composite Temperature Threshold, the composite warning threshold reported by Identify Controller. |
| `MNTMT` | Minimum Thermal Management Temperature, the minimum Kelvin value accepted for HCTM. |
| `MXTMT` | Maximum Thermal Management Temperature, the maximum Kelvin value accepted for HCTM. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §5.2.14.2.1 is the applicable context.
2. Decode NPSS at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check APSTA as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 338 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §5.2.14.2.1 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes NPSS, APSTA, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §5.2.14.2.1, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 338. Annotate the bytes containing NPSS, decode them, and independently verify APSTA. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of NPSS in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand NPSS and state its unit or object scope?
2. Can the reader explain why APSTA is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** NPSS, APSTA, HCTMA, WCTEMP, MNTMT, MXTMT, RTD3E, RTD3R

**Source keyword index:** `shall not`, `should not`, `shall`, `should`, `may`, `optional`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.14.2.1, Figure 338, printed pages 340-364, PDF pages 366-390

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 340: Power State Descriptor Data Structure</strong></summary>

<!-- claim:BASEPOWER-FIG-340-CLAIM figure-table:BASEPOWER-FIG-340 -->

**SPEC.** Figure 340, "Power State Descriptor Data Structure": Defines the concrete layout or value relationships for Power State Descriptor Data Structure. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is MP, NOPS, ENLAT, EXLAT, IDLP, ACTP, RRT/RRL, RWT/RWL.

#### Where this Figure fits

Figure 340 sits in §5.2.14.2.2 and acts as a state checkpoint. Read it after the report mental model has established the owning object and before software turns MP into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a state or timing Figure. Follow each arrow while recording trigger, observer, completion condition, and timeout source. Similar state names under different reset scopes do not imply preservation of the same queue or controller state.

#### Teaching redraw

```text
[Locate source: MP]
          ↓
[Extract field: NOPS] → [Apply encoding: ENLAT]
                                      ↓
[Validate evidence: EXLAT]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `MP` | Maximum Power, the sustained maximum power of a power state. |
| `NOPS` | Non-Operational State, the PSD bit indicating that the state does not process I/O commands. |
| `ENLAT` | Entry Latency, the maximum latency to enter a power state, in microseconds. |
| `EXLAT` | Exit Latency, the maximum latency to exit a power state, in microseconds. |
| `IDLP` | Idle Power, typical power under the specification's idle measurement conditions. |
| `ACTP` | Active Power, average active power under the specified workload and time window. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §5.2.14.2.2 is the applicable context.
2. Decode MP at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check NOPS as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 340 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §5.2.14.2.2 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes MP, NOPS, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §5.2.14.2.2, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 340. Annotate the bytes containing MP, decode them, and independently verify NOPS. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of MP in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand MP and state its unit or object scope?
2. Can the reader explain why NOPS is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** MP, NOPS, ENLAT, EXLAT, IDLP, ACTP, RRT/RRL, RWT/RWL

**Source keyword index:** `shall not`, `shall`, `may`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.14.2.2, Figure 340, printed pages 383-386, PDF pages 409-412

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 474: Asynchronous Event Configuration – Command Dword 11</strong></summary>

<!-- claim:BASEPOWER-FIG-474-CLAIM figure-table:BASEPOWER-FIG-474 -->

**SPEC.** Figure 474, "Asynchronous Event Configuration – Command Dword 11": Defines the concrete layout or value relationships for Asynchronous Event Configuration – Command Dword 11. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is TTHRY, SHCW.

#### Where this Figure fits

Figure 474 sits in §5.2.30.1.6 and acts as a command checkpoint. Read it after the report mental model has established the owning object and before software turns TTHRY into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a command-construction field table. Build the common SQE, locate the specified CDW, encode each bit range, clear reserved bits, and validate the result against transfer length, buffer, and completion status. Equal field names do not imply equal semantics across commands.

#### Teaching redraw

```text
[Locate source: TTHRY]
          ↓
[Extract field: SHCW] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `TTHRY` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `SHCW` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §5.2.30.1.6 is the applicable context.
2. Decode TTHRY at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check SHCW as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 474 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §5.2.30.1.6 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes TTHRY, SHCW, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §5.2.30.1.6, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 474. Annotate the bytes containing TTHRY, decode them, and independently verify SHCW. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of TTHRY in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand TTHRY and state its unit or object scope?
2. Can the reader explain why SHCW is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** TTHRY, SHCW

**Source keyword index:** `shall not`, `shall`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.6, Figure 474, printed pages 466-468, PDF pages 492-494

</details>

## Use and limitations

Use the claim IDs as stable PPT traceability keys. Re-check affected claims if the source revision, errata set, or approved scope changes.

## Self-questions and worked answers

24 answered questions revisit this report's scope. Each answer retains the same source links as the teaching module; calculations and debugging examples are informative.

### Q01. What is the governing interpretation for “Get first, Set second, then observe again”?

<!-- qa:base-power-features-feature-read-set-loop-lead -->

**Answer.**

A Feature is not a simple register. The host first reads capability with SEL=011b, then retrieves current/default/saved views, confirms scope and persistence, and only then writes. Set completion proves command outcome; a follow-up Get and runtime telemetry prove that software observes the new policy.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.12, printed pages 209, PDF pages 235; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.12, printed pages 209-210, PDF pages 235-236; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.12.1, printed pages 211-212, PDF pages 237-238; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30, printed pages 457, PDF pages 483; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30, printed pages 459, PDF pages 485

### Q02. Which concepts or conditions must be distinguished in “Get first, Set second, then observe again”?

<!-- qa:base-power-features-feature-read-set-loop-rows -->

**Answer.**

- SEL=000b — Current value — Observe current controller policy
- SEL=001b — Default value — Establish a rollback baseline
- SEL=010b — Saved value — Does not prove a value was saved
- SEL=011b — CHANG/NSSPEC/SVBL — Capability gate before writing

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.12, printed pages 209, PDF pages 235; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.12, printed pages 209-210, PDF pages 235-236; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.12.1, printed pages 211-212, PDF pages 237-238; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30, printed pages 457, PDF pages 483; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30, printed pages 459, PDF pages 485

### Q03. How does “Get first, Set second, then observe again” apply to a concrete calculation or operational scenario?

<!-- qa:base-power-features-feature-read-set-loop-example -->

**Answer.**

For FID 02h current, CDW10=00000002h. For supported capabilities, SEL=3 so CDW10=(3×100h)+02h=00000302h. If CHANG=0, stop before Set; if CHANG=1, construct CDW11 from NPSS and the PSDs.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.12, printed pages 209, PDF pages 235; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.12, printed pages 209-210, PDF pages 235-236; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.12.1, printed pages 211-212, PDF pages 237-238; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30, printed pages 457, PDF pages 483; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30, printed pages 459, PDF pages 485

### Q04. What misinterpretation is most likely in “Get first, Set second, then observe again”, and how is it debugged?

<!-- qa:base-power-features-feature-read-set-loop-pitfall -->

**Answer.**

Do not log only 'Get succeeded.' Retain raw CDW10/CDW14, CQE.DW0, SCT/SC/DNR, and the selected current/default/saved/capability view; otherwise the same 32-bit result can be decoded with the wrong semantics.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.12, printed pages 209, PDF pages 235; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.12, printed pages 209-210, PDF pages 235-236; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.12.1, printed pages 211-212, PDF pages 237-238; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30, printed pages 457, PDF pages 483; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30, printed pages 459, PDF pages 485

### Q05. What is the governing interpretation for “A power state is a multidimensional power, latency, and performance operating point”?

<!-- qa:base-power-features-power-state-mental-model-lead -->

**Answer.**

A state number alone cannot establish workload suitability. Read MP, NOPS, ENLAT/EXLAT, IDLP/ACTP, and relative performance together in each PSD. Increasing PS numbers reduce maximum power monotonically, but latency and throughput do not necessarily change by a fixed ratio.

> Source: NVME-BASE-2.4, Rev. 2.4, §8.1.19, printed pages 666-667, PDF pages 692-693; Source: NVME-BASE-2.4, Rev. 2.4, §8.1.19, printed pages 666-668, PDF pages 692-694; Source: NVME-BASE-2.4, Rev. 2.4, §8.1.19.1, printed pages 668-669, PDF pages 694-695; Source: NVME-BASE-2.4, Rev. 2.4, §8.1.19.2, printed pages 668, PDF pages 694; Source: NVME-BASE-2.4, Rev. 2.4, §8.1.19, printed pages 667-668, PDF pages 693-694; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.2, printed pages 460-461, PDF pages 486-487; Source: NVME-BASE-2.4, Rev. 2.4, §8.1.19.3, printed pages 669, PDF pages 695

### Q06. Which concepts or conditions must be distinguished in “A power state is a multidimensional power, latency, and performance operating point”?

<!-- qa:base-power-features-power-state-mental-model-rows -->

**Answer.**

- MP — Sustained maximum power — Not an instantaneous sample
- IDLP/ACTP — Idle typical / active average — Different measurement conditions
- ENLAT/EXLAT — Maximum entry/exit latency — Sum across transitions
- RRT/RRL/RWT/RWL — Relative throughput/latency — Compare only like characteristics

> Source: NVME-BASE-2.4, Rev. 2.4, §8.1.19, printed pages 666-667, PDF pages 692-693; Source: NVME-BASE-2.4, Rev. 2.4, §8.1.19, printed pages 666-668, PDF pages 692-694; Source: NVME-BASE-2.4, Rev. 2.4, §8.1.19.1, printed pages 668-669, PDF pages 694-695; Source: NVME-BASE-2.4, Rev. 2.4, §8.1.19.2, printed pages 668, PDF pages 694; Source: NVME-BASE-2.4, Rev. 2.4, §8.1.19, printed pages 667-668, PDF pages 693-694; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.2, printed pages 460-461, PDF pages 486-487; Source: NVME-BASE-2.4, Rev. 2.4, §8.1.19.3, printed pages 669, PDF pages 695

### Q07. How does “A power state is a multidimensional power, latency, and performance operating point” apply to a concrete calculation or operational scenario?

<!-- qa:base-power-features-power-state-mental-model-example -->

**Answer.**

Informative calculation: current PS1.EXLAT=100 µs and target PS3.ENLAT=2500 µs produce a direct-transition budget of 2600 µs. If the path is PS1→PS2→PS3, sum PS1.EXLAT+PS2.ENLAT and PS2.EXLAT+PS3.ENLAT instead of reusing 2600 µs.

> Source: NVME-BASE-2.4, Rev. 2.4, §8.1.19, printed pages 666-667, PDF pages 692-693; Source: NVME-BASE-2.4, Rev. 2.4, §8.1.19, printed pages 666-668, PDF pages 692-694; Source: NVME-BASE-2.4, Rev. 2.4, §8.1.19.1, printed pages 668-669, PDF pages 694-695; Source: NVME-BASE-2.4, Rev. 2.4, §8.1.19.2, printed pages 668, PDF pages 694; Source: NVME-BASE-2.4, Rev. 2.4, §8.1.19, printed pages 667-668, PDF pages 693-694; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.2, printed pages 460-461, PDF pages 486-487; Source: NVME-BASE-2.4, Rev. 2.4, §8.1.19.3, printed pages 669, PDF pages 695

### Q08. What misinterpretation is most likely in “A power state is a multidimensional power, latency, and performance operating point”, and how is it debugged?

<!-- qa:base-power-features-power-state-mental-model-pitfall -->

**Answer.**

A successful FID 02h Set proves only that the controller accepted PS. Debug evidence also needs NPSS, the complete target PSD, previous state, WH, CQE timestamp, and first-I/O latency; entry into a non-operational state additionally requires checking whether I/O was drained.

> Source: NVME-BASE-2.4, Rev. 2.4, §8.1.19, printed pages 666-667, PDF pages 692-693; Source: NVME-BASE-2.4, Rev. 2.4, §8.1.19, printed pages 666-668, PDF pages 692-694; Source: NVME-BASE-2.4, Rev. 2.4, §8.1.19.1, printed pages 668-669, PDF pages 694-695; Source: NVME-BASE-2.4, Rev. 2.4, §8.1.19.2, printed pages 668, PDF pages 694; Source: NVME-BASE-2.4, Rev. 2.4, §8.1.19, printed pages 667-668, PDF pages 693-694; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.2, printed pages 460-461, PDF pages 486-487; Source: NVME-BASE-2.4, Rev. 2.4, §8.1.19.3, printed pages 669, PDF pages 695

### Q09. What is the governing interpretation for “APST is a state machine driven by idle timers”?

<!-- qa:base-power-features-apst-state-machine-lead -->

**Answer.**

The 256-byte APST buffer is not a performance table. It contains 32 rules stating which non-operational state to enter after a given idle duration. APSTE enables timer rules, entries with ITPT=0 are inactive, and arriving I/O returns the controller to its most recent operational state.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.7, printed pages 468-469, PDF pages 494-495; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.7, printed pages 469, PDF pages 495; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.7, printed pages 469, PDF pages 495; Source: NVME-BASE-2.4, Rev. 2.4, §8.1.19, printed pages 668, PDF pages 694; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30, printed pages 456-457, PDF pages 482-483

### Q10. Which concepts or conditions must be distinguished in “APST is a state machine driven by idle timers”?

<!-- qa:base-power-features-apst-state-machine-rows -->

**Answer.**

- APSTE=0 — Host-directed entry only — The table may exist but timers do not drive entry
- APSTE=1 — Host- or timer-directed entry — ITPT must be met continuously
- NOPPME=0 — Background work stays within non-op limits — Controller work may be deferred
- NOPPME=1 — Background work may raise power temporarily — Still capped by the last operational state

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.7, printed pages 468-469, PDF pages 494-495; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.7, printed pages 469, PDF pages 495; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.7, printed pages 469, PDF pages 495; Source: NVME-BASE-2.4, Rev. 2.4, §8.1.19, printed pages 668, PDF pages 694; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30, printed pages 456-457, PDF pages 482-483

### Q11. How does “APST is a state machine driven by idle timers” apply to a concrete calculation or operational scenario?

<!-- qa:base-power-features-apst-state-machine-example -->

**Answer.**

To enter PS3 after 2000 ms idle: ITPT=2000=07D0h, shifted into bits31:8 gives 07D00000h; ITPS=3 in bits7:3 gives 18h, so the low dword is 07D00018h. Reserved bits and the entry high dword remain zero; 32 entries total 256 bytes.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.7, printed pages 468-469, PDF pages 494-495; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.7, printed pages 469, PDF pages 495; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.7, printed pages 469, PDF pages 495; Source: NVME-BASE-2.4, Rev. 2.4, §8.1.19, printed pages 668, PDF pages 694; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30, printed pages 456-457, PDF pages 482-483

### Q12. What misinterpretation is most likely in “APST is a state machine driven by idle timers”, and how is it debugged?

<!-- qa:base-power-features-apst-state-machine-pitfall -->

**Answer.**

Common errors include treating ITPT as microseconds, selecting an operational ITPS, leaving unused entries nonzero, or placing the 256-byte PRP buffer across an unsupported page boundary. Retain a hash of the full buffer and a per-entry decode.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.7, printed pages 468-469, PDF pages 494-495; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.7, printed pages 469, PDF pages 495; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.7, printed pages 469, PDF pages 495; Source: NVME-BASE-2.4, Rev. 2.4, §8.1.19, printed pages 668, PDF pages 694; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30, printed pages 456-457, PDF pages 482-483

### Q13. What is the governing interpretation for “Temperature Threshold connects sensor, event, and clear point”?

<!-- qa:base-power-features-temperature-event-loop-lead -->

**Answer.**

FID 04h is more than a temperature number. TMPSEL selects a sensor, THSEL selects over or under, TMPTH sets the trigger point, TMPTHH sets the event clear point, and SMART/Health.TTC plus AEC enable return controller state to the host.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.3, printed pages 462-463, PDF pages 488-489; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.3.1, printed pages 463-464, PDF pages 489-490; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.3, printed pages 220-225, PDF pages 246-251

### Q14. Which concepts or conditions must be distinguished in “Temperature Threshold connects sensor, event, and clear point”?

<!-- qa:base-power-features-temperature-event-loop-rows -->

**Answer.**

- TMPSEL — Composite or sensor 1-8 — Get does not use all-sensors selection
- THSEL — Over/under — Comparison direction is reversed
- TMPTH — Trigger Kelvin — Log raw K and converted °C
- TMPTHH — Clear hysteresis in Kelvin — Not a second trigger threshold

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.3, printed pages 462-463, PDF pages 488-489; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.3.1, printed pages 463-464, PDF pages 489-490; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.3, printed pages 220-225, PDF pages 246-251

### Q15. How does “Temperature Threshold connects sensor, event, and clear point” apply to a concrete calculation or operational scenario?

<!-- qa:base-power-features-temperature-event-loop-example -->

**Answer.**

For a Composite over threshold of 343 K (about 70 °C) and 5 K hysteresis: TMPSEL=0, THSEL=0, TMPTH=0157h, and TMPTHH=5, giving CDW11=(5<<22)+0157h=01400157h. The event triggers at ≥343 K and ends only after falling to 338 K (about 65 °C).

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.3, printed pages 462-463, PDF pages 488-489; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.3.1, printed pages 463-464, PDF pages 489-490; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.3, printed pages 220-225, PDF pages 246-251

### Q16. What misinterpretation is most likely in “Temperature Threshold connects sensor, event, and clear point”, and how is it debugged?

<!-- qa:base-power-features-temperature-event-loop-pitfall -->

**Answer.**

If no AEN appears, do not immediately conclude that the threshold failed. Check AEC.TTHRY/SHCW enables, TTC, raw sensor Kelvin, threshold type, hysteresis clear point, and an outstanding Asynchronous Event Request in order.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.3, printed pages 462-463, PDF pages 488-489; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.3.1, printed pages 463-464, PDF pages 489-490; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.3, printed pages 220-225, PDF pages 246-251

### Q17. What is the governing interpretation for “HCTM uses two thresholds for lighter and stronger thermal response”?

<!-- qa:base-power-features-hctm-control-loop-lead -->

**Answer.**

HCTM does not select a fixed clock or power state. It gives the controller two temperature boundaries, TMT1/TMT2. At TMT1 the controller minimizes performance impact; at TMT2 it applies stronger thermal control. Actual hysteresis and internal actions are vendor implementation details.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.10, printed pages 471-472, PDF pages 497-498; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.10, 8.1.19.5, printed pages 472, 670-671, PDF pages 498, 696-697; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.3, printed pages 220-225, PDF pages 246-251

### Q18. Which concepts or conditions must be distinguished in “HCTM uses two thresholds for lighter and stronger thermal response”?

<!-- qa:base-power-features-hctm-control-loop-rows -->

**Answer.**

- TMT1 — Lighter-control boundary — Objective is to minimize impact
- TMT2 — Stronger-control boundary — Thermal control takes priority
- MNTMT/MXTMT — Legal configuration range — Validate on the host first
- SMART counters — Transition count/time — Evidence that the control loop acted

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.10, printed pages 471-472, PDF pages 497-498; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.10, 8.1.19.5, printed pages 472, 670-671, PDF pages 498, 696-697; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.3, printed pages 220-225, PDF pages 246-251

### Q19. How does “HCTM uses two thresholds for lighter and stronger thermal response” apply to a concrete calculation or operational scenario?

<!-- qa:base-power-features-hctm-control-loop-example -->

**Answer.**

If MNTMT=273 K and MXTMT=373 K, TMT1=343 K and TMT2=353 K are legal, and CDW11=(0157h<<16)+0161h=01570161h. FID 10h is saveable; if SVBL=1 and policy requires persistence, CDW10.SV=1 with FID=10h gives CDW10=80000010h.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.10, printed pages 471-472, PDF pages 497-498; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.10, 8.1.19.5, printed pages 472, 670-671, PDF pages 498, 696-697; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.3, printed pages 220-225, PDF pages 246-251

### Q20. What misinterpretation is most likely in “HCTM uses two thresholds for lighter and stronger thermal response”, and how is it debugged?

<!-- qa:base-power-features-hctm-control-loop-pitfall -->

**Answer.**

Reject TMT1=TMT2, TMT1>TMT2, out-of-range values, or Celsius written directly into Kelvin fields on the host. Hardware validation records ambient, airflow, workload, sensor cadence, and host latency so performance impact remains comparable.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.10, printed pages 471-472, PDF pages 497-498; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.10, 8.1.19.5, printed pages 472, 670-671, PDF pages 498, 696-697; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.3, printed pages 220-225, PDF pages 246-251

### Q21. What is the governing interpretation for “Connect policy, state, events, and measurements into reproducible debug evidence”?

<!-- qa:base-power-features-end-to-end-debug-lead -->

**Answer.**

Power/thermal defects rarely reduce to one wrong bit. Capability, policy, transition, background work, thermal events, and host workload must share one timeline. FID 11h NOPPME, APST, manual PS, HCTM, and RTD3 control different layers and do not replace one another.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.7, printed pages 469, PDF pages 495; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.11, printed pages 472-473, PDF pages 498-499; Source: NVME-BASE-2.4, Rev. 2.4, §8.1.19.4, printed pages 669-670, PDF pages 695-696; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.3, printed pages 220-225, PDF pages 246-251; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.12.2, printed pages 212, PDF pages 238

### Q22. Which concepts or conditions must be distinguished in “Connect policy, state, events, and measurements into reproducible debug evidence”?

<!-- qa:base-power-features-end-to-end-debug-rows -->

**Answer.**

- Policy plane — Raw FID02/04/0C/10/11 values — Proves what the host requested
- State plane — PSD, APST timer, I/O return — Proves controller-state context
- Thermal plane — Sensors, TTC, HCTM counters — Proves when thermal control acted
- Outcome plane — CQE, latency, power/temperature trace — Proves impact and recovery

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.7, printed pages 469, PDF pages 495; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.11, printed pages 472-473, PDF pages 498-499; Source: NVME-BASE-2.4, Rev. 2.4, §8.1.19.4, printed pages 669-670, PDF pages 695-696; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.3, printed pages 220-225, PDF pages 246-251; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.12.2, printed pages 212, PDF pages 238

### Q23. How does “Connect policy, state, events, and measurements into reproducible debug evidence” apply to a concrete calculation or operational scenario?

<!-- qa:base-power-features-end-to-end-debug-example -->

**Answer.**

Case: APSTE=1 enters PS3 after 2 s idle and NOPPME=0. At 3 s, controller background work cannot raise power. The first read at 4 s returns to an operational state, and its latency spike is compared with PS3.EXLAT. If temperature also crosses TMT1, HCTM counters and the sensor timeline separate exit latency from thermal throttling.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.7, printed pages 469, PDF pages 495; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.11, printed pages 472-473, PDF pages 498-499; Source: NVME-BASE-2.4, Rev. 2.4, §8.1.19.4, printed pages 669-670, PDF pages 695-696; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.3, printed pages 220-225, PDF pages 246-251; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.12.2, printed pages 212, PDF pages 238

### Q24. What misinterpretation is most likely in “Connect policy, state, events, and measurements into reproducible debug evidence”, and how is it debugged?

<!-- qa:base-power-features-end-to-end-debug-pitfall -->

**Answer.**

Do not infer cause from one outcome. Establish Set success, follow-up Get value, continuous APST idle time, NOPPME background-power permission, and TMT1/TMT2 crossings before classifying a controller defect.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.7, printed pages 469, PDF pages 495; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.11, printed pages 472-473, PDF pages 498-499; Source: NVME-BASE-2.4, Rev. 2.4, §8.1.19.4, printed pages 669-670, PDF pages 695-696; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.3, printed pages 220-225, PDF pages 246-251; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.12.2, printed pages 212, PDF pages 238
