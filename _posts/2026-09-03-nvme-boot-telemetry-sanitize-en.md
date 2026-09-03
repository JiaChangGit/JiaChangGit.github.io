---
permalink: /nvme/boot-telemetry-sanitize-en/
layout: post
read_time: true
show_date: true
title: "NVMe 2.4: Boot Partitions, Telemetry, and Sanitize"
date: 2026-09-03
description: "Source-located PCIe/NVMe report for PPT authoring."
lang: en
img: posts/2026/cat_title.jpg
tags: [NVMe, PCIe, Specification]
category: NVMe
author: Jia-Chang
github: JiaChangGit/JiaChangGit.github.io/tree/main/DOCS/nvme-spec-report
toc: yes
---
[繁體中文]({% post_url 2026-09-03-nvme-boot-telemetry-sanitize-zh-tw %})


# NVMe 2.4: Boot Partitions, Telemetry, and Sanitize

Purpose: a source-located engineering report for GitHub Pages and a 100-minute presentation.

Scope: Base §§8.1.3, 8.1.30, 8.1.27 (excluding 8.1.27.6), 5.2.26; LIDs 15h/07h/08h/81h; FIDs 85h/17h; NVM §§4.1.7 and 5.12, with required referenced figures. Only PCIe/memory-based and common NVMe content appears below.

## Source versions

NVM Express Base Specification, Revision 2.4
NVM Express NVM Command Set Specification, Revision 1.3

Verification date: 2026-09-03. No additional errata, ECNs, Technical Proposals, controller-vendor documents, or source text from the external PCI Express Base Specification are included.

## Reading map

```text
Discover capability -> Read / capture / sanitize -> Track state and evidence -> Verify outcome
```

Boot, Telemetry, and Sanitize manage boot images, diagnostic snapshots, and user-data sanitization. They share a capability-command-evidence reading method but have different scopes and completion conditions.

## Normative language

shall is mandatory, may permits a choice, should expresses a preferred recommendation, and optional means support is not required. The report preserves these terms and never promotes one into another.

## Acronyms first: complete glossary

Every abbreviation below is introduced before it is used in the slide narrative. The term alone is never enough: retain owner, width, unit, scope, and state.

| Acronym / term | Plain-language meaning | Source |
|---|---|---|
| `BPID` | Boot Partition Identifier; selects 0 or 1 independently of the active partition. | NVME-BASE-2.4 Rev. 2.4, §5.2.13.1.21, printed pp. 283-284, PDF pp. 309-310 |
| `BRS` | Boot Read Status: 00b no request, 01b in progress, 10b success, 11b error. | NVME-BASE-2.4 Rev. 2.4, §8.1.3.1, printed pp. 586-587, PDF pp. 612-613 |
| `BPCAP` | Boot Partition Capabilities; identifies the supported combination of Set Features and RPMB protection. | NVME-BASE-2.4 Rev. 2.4, §8.1.3.3, printed pp. 588-589, PDF pp. 614-615 |
| `BP0WPS` | Boot Partition 0 Write Protection State; bits 2:0 of FID 85h. | NVME-BASE-2.4 Rev. 2.4, §5.2.30.1.39, printed pp. 513-514, PDF pp. 539-540 |
| `CTHID` | Create Telemetry Host-Initiated Data; the 07h capture request, cleared for subsequent reads of that snapshot. | NVME-BASE-2.4 Rev. 2.4, §5.2.13.1.8, printed pp. 232-235, PDF pp. 258-261 |
| `MCDA` | Maximum Created Data Area; selects the largest area to create when supported and capture is requested. | NVME-BASE-2.4 Rev. 2.4, §5.2.13.1.8, printed pp. 232-235, PDF pp. 258-261 |
| `MCDAS` | Maximum Created Data Area Supported; bit 0 of the 07h LID Specific Parameter, advertising MCDA support. | NVME-BASE-2.4 Rev. 2.4, §5.2.13.1.8, printed pp. 232-235, PDF pp. 258-261 |
| `ETDAS` | Extended Telemetry Data Area 4 Supported; the host's Area 4 declaration in Host Behavior Support. | NVME-BASE-2.4 Rev. 2.4, §8.1.30; 5.2.30.1.15, printed pp. 476,733-734, PDF pp. 502,759-760 |
| `TCDA` | Telemetry Controller-Initiated Data Available; in 2.4, indicates an update since the last RAE=0 acknowledgement. | NVME-BASE-2.4 Rev. 2.4, §5.2.13.1.9, printed pp. 237, PDF pp. 263 |
| `TCDGN` | Telemetry Controller-Initiated Data Generation Number; an eight-bit generation incremented at the end of an update. | NVME-BASE-2.4 Rev. 2.4, §8.1.30, printed pp. 734-735, PDF pp. 760-761 |
| `RAE` | Retain Asynchronous Event; use one during Telemetry collection and zero to acknowledge completion. | NVME-BASE-2.4 Rev. 2.4, §8.1.30, printed pp. 734-735, PDF pp. 760-761 |
| `SANACT` | Sanitize Action; selects the method, Exit Failure Mode, or Exit Media Verification. | NVME-BASE-2.4 Rev. 2.4, §5.2.26, printed pp. 448-451, PDF pp. 474-477 |
| `AUSE` | Allow Unrestricted Sanitize Exit; selects whether failure can be exited without a successful retry. | NVME-BASE-2.4 Rev. 2.4, §8.1.27.4, printed pp. 719-730, PDF pp. 745-756 |
| `NDAS` | No-Deallocate After Sanitize; a command request interpreted with SANICAP.NDI and NODRM. | NVME-BASE-2.4 Rev. 2.4, §5.2.30.1.16; 8.1.27.2-8.1.27.3, printed pp. 477-478,715-719, PDF pp. 503-504,741-745 |
| `NODRM` | No-Deallocate Response Mode; FID 17h bit zero selects error or warning for inhibited NDAS. | NVME-BASE-2.4 Rev. 2.4, §5.2.30.1.16; 8.1.27.2-8.1.27.3, printed pp. 477-478,715-719, PDF pp. 503-504,741-745 |
| `EMVS` | Enter Media Verification State; requests verification after successful processing, subject to method and capability restrictions. | NVME-BASE-2.4 Rev. 2.4, §5.2.26, printed pp. 449, PDF pp. 475 |
| `PREQ` | Purge Request; interpreted with SPRRS for purge request/reporting; its bit position differs between the Sanitize commands. | NVME-BASE-2.4 Rev. 2.4, §8.1.27.2-8.1.27.3, printed pp. 714-717, PDF pp. 740-743 |
| `SPROG` | Sanitize Progress; raw/65536, indicating progress only for the currently measured phase. | NVME-BASE-2.4 Rev. 2.4, §5.2.13.1.38; 8.1.27.3, printed pp. 314-319,718, PDF pp. 340-345,744 |
| `SOS` | Sanitize Operation Status; SSTAT bits 2:0, interpreted separately from the current SANS state. | NVME-BASE-2.4 Rev. 2.4, §5.2.13.1.38, printed pp. 313-319, PDF pp. 339-345 |
| `MVCNCLD` | Media Verification Canceled; records canceled verification and affects the transition after processing. | NVME-BASE-2.4 Rev. 2.4, §8.1.27.4.6-8.1.27.4.7, printed pp. 727-730, PDF pp. 753-756 |
| `PRCHK` | Protection Information Check; three bits request guard, application-tag, and reference-tag checking; verification reads use 000b. | NVME-NVM-CS-1.3 Rev. 1.3, §5.12.1, printed pp. 174-175, PDF pp. 174-175 |
| `STC` | Storage Tag Check; here it selects storage-tag checking for NVM Reads and is zero for verification reads. | NVME-NVM-CS-1.3 Rev. 1.3, §5.12.1, printed pp. 174-175, PDF pp. 174-175 |

## Visual atlas: locate the system before reading fields

Each redraw answers a different question: architecture locates components, sequence shows ownership, decode turns bits into engineering values, and state views preserve failure evidence. These are teaching redraws, not copies of specification artwork.

### Visual 01: Two Boot read paths

**View type:** `sequence`

```text
1. CAP.BPS
2. BPINFO active/size
3. BPMBL buffer
4. BPRSEL request
5. BRS result
```

**Question answered:** First determine whether an Admin-command environment exists, then choose properties or LID 15h. Both access boot contents, but their return formats and observation points differ.

**Supporting Figures:** Figure 36, Figure 49, Figure 50, Figure 51, Figure 279, Figure 280, Figure 679

**Sources:** NVME-BASE-2.4 Rev. 2.4, §8.1.3, printed pp. 586, PDF pp. 612; NVME-BASE-2.4 Rev. 2.4, §8.1.3.1, printed pp. 586-587, PDF pp. 612-613; NVME-BASE-2.4 Rev. 2.4, §5.2.13.1.21, printed pp. 283-284, PDF pp. 309-310

### Visual 02: The complete update and protection lifecycle

**View type:** `sequence`

```text
1. Download in order
2. Unlock target
3. Commit CA=110b
4. Read/verify; CA=111b
5. Relock
```

**Question answered:** Track image transfer, partition contents, active selection, and write protection separately. Successful download has not yet written a Boot Partition, and a successful write has not automatically activated it.

**Supporting Figures:** Figure 187, Figure 542, Figure 680, Figure 681, Figure 682, Figure 683, Figure 684, Figure 756, Figure 765, Figure 766

**Sources:** NVME-BASE-2.4 Rev. 2.4, §8.1.3.2, printed pp. 587-588, PDF pp. 613-614; NVME-BASE-2.4 Rev. 2.4, §8.1.3.2, printed pp. 588, PDF pp. 614; NVME-BASE-2.4 Rev. 2.4, §8.1.3.3, printed pp. 588-589, PDF pp. 614-615; NVME-BASE-2.4 Rev. 2.4, §5.2.30.1.39, printed pp. 513-514, PDF pp. 539-540; NVME-BASE-2.4 Rev. 2.4, §8.1.3.3.1-8.1.3.3.3, printed pp. 589-594, PDF pp. 615-620; NVME-BASE-2.4 Rev. 2.4, §5.2.30.1.39; 8.1.3.3.3, printed pp. 513-514,593-594, PDF pp. 539-540,619-620

### Visual 03: Computing snapshots from Last Block

**View type:** `decode`

```text
1. Read 512-byte header
2. Check DA4S/ETDAS
3. Decode last blocks
4. Compute inclusive extent
5. Read aligned blocks
```

**Question answered:** Areas are differently sized views starting at the same block 1. Decode the header, select the final applicable populated area, and do not add the three Last Block numbers.

**Supporting Figures:** Figure 221, Figure 223, Figure 338, Figure 491, Figure 780, Figure 781

**Sources:** NVME-BASE-2.4 Rev. 2.4, §8.1.30; 5.2.13.1.8-5.2.13.1.9, printed pp. 232-237,733-737, PDF pp. 258-263,759-763; NVME-BASE-2.4 Rev. 2.4, §8.1.30; 5.2.30.1.15, printed pp. 476,733-734, PDF pp. 502,759-760; NVME-BASE-2.4 Rev. 2.4, §5.2.13.1.8-5.2.13.1.9, printed pp. 232-237, PDF pp. 258-263

### Visual 04: Create, read, verify consistency, acknowledge

**View type:** `sequence`

```text
1. Capability / event setup
2. Capture or observe update
3. RAE=1 chunk reads
4. Recheck generation/TCDA
5. 08h RAE=0 acknowledgement
```

**Question answered:** Separate creating 07h data from subsequent reads; the controller decides 08h capture timing. For both, verify generation and distinguish event acknowledgement from payload deletion.

**Supporting Figures:** Figure 204, Figure 210, Figure 211, Figure 220, Figure 222, Figure 151, Figure 152, Figure 155, Figure 474

**Sources:** NVME-BASE-2.4 Rev. 2.4, §5.2.13.1.8, printed pp. 232-235, PDF pp. 258-261; NVME-BASE-2.4 Rev. 2.4, §8.1.30, printed pp. 734-735, PDF pp. 760-761; NVME-BASE-2.4 Rev. 2.4, §5.2.13.1.9, printed pp. 237, PDF pp. 263; NVME-BASE-2.4 Rev. 2.4, §5.2.13.1.8-5.2.13.1.9, printed pp. 233,235,237, PDF pp. 259,261,263; NVME-BASE-2.4 Rev. 2.4, §8.1.30; 5.2.30.1.6, printed pp. 734-735,466-468, PDF pp. 760-761,492-494

### Visual 05: Define the sanitization target first

**View type:** `architecture`

```text
1. Select target
2. Enumerate user-data locations
3. Check method/support
4. Apply purge requirement
5. Audit permitted evidence
```

**Question answered:** Sanitize scope is not simply everything on a disk. Classify the target, data provenance, and whether it can contain user data; this also establishes its relationship with Boot and diagnostics.

**Supporting Figures:** Figure 770, Figure 771, Figure 200, Figure 201

**Sources:** NVME-BASE-2.4 Rev. 2.4, §8.1.27, printed pp. 711-712, PDF pp. 737-738; NVME-BASE-2.4 Rev. 2.4, §8.1.27, printed pp. 711-712, PDF pp. 737-738; NVME-BASE-2.4 Rev. 2.4, §8.1.27.2-8.1.27.3, printed pp. 714-717, PDF pp. 740-743; NVME-NVM-CS-1.3 Rev. 1.3, §5.12, printed pp. 174, PDF pp. 174

### Visual 06: Combining command parameters with capabilities

**View type:** `decode`

```text
1. SANICAP / target
2. SANACT and modifiers
3. FID 17h policy
4. Preflight and CQE
5. LID 81h operation result
```

**Question answered:** Separate advertised capabilities, command requests, and Feature policy. Command acceptance, operation success, and satisfaction of no-deallocate are three outcomes requiring different evidence.

**Supporting Figures:** Figure 338, Figure 451, Figure 452, Figure 453, Figure 454, Figure 492

**Sources:** NVME-BASE-2.4 Rev. 2.4, §5.2.26, printed pp. 448-451, PDF pp. 474-477; NVME-BASE-2.4 Rev. 2.4, §8.1.27.1; 5.2.27, printed pp. 713,453, PDF pp. 739,479; NVME-BASE-2.4 Rev. 2.4, §5.2.30.1.16; 8.1.27.2-8.1.27.3, printed pp. 477-478,715-719, PDF pp. 503-504,741-745; NVME-BASE-2.4 Rev. 2.4, §5.2.26, printed pp. 449, PDF pp. 475; NVME-BASE-2.4 Rev. 2.4, §5.2.26; 8.1.27.1, printed pp. 449-451,712-714, PDF pp. 475-477,738-740; NVME-BASE-2.4 Rev. 2.4, §5.2.26; 8.1.27.3, printed pp. 451,717, PDF pp. 477,743

### Visual 07: Reconstruct background work from state, log, and AER

**View type:** `state`

```text
Idle | A1: AUSE=0 | Restricted Processing
Idle | B1: AUSE=1 | Unrestricted Processing
Restricted Processing | C1: success; no verification | Idle
Restricted Processing | D1: processing fails | Restricted Failure
Restricted Processing | F1: success; EMVS=1; not canceled | Media Verification
Restricted Failure | A2: restricted retry | Restricted Processing
Unrestricted Processing | C2: success; no verification | Idle
Unrestricted Processing | D2: processing fails | Unrestricted Failure
Unrestricted Processing | F2: success; EMVS=1; not canceled | Media Verification
Unrestricted Failure | A3: restricted retry | Restricted Processing
Unrestricted Failure | B2: unrestricted retry | Unrestricted Processing
Unrestricted Failure | E: Exit Failure Mode | Idle
Media Verification | G: exit / applicable reset / cancellation | Post-Verification Deallocation
Post-Verification Deallocation | H: deallocation succeeds | Idle
Post-Verification Deallocation | I1: failure; original AUSE=0 | Restricted Failure
Post-Verification Deallocation | I2: failure; original AUSE=1 | Unrestricted Failure
```

**Question answered:** Start with the seven states in Figure 772 and attach transition conditions from Figures 773–779. Status describes results, state describes the current position, and events report transitions.

**Supporting Figures:** Figure 312, Figure 151, Figure 152, Figure 156, Figure 772, Figure 773, Figure 774, Figure 775, Figure 776, Figure 777, Figure 778, Figure 779

**Sources:** NVME-BASE-2.4 Rev. 2.4, §5.2.26.1; 8.1.27.1, printed pp. 451,712-713, PDF pp. 477,738-739; NVME-BASE-2.4 Rev. 2.4, §8.1.27.4, printed pp. 719-730, PDF pp. 745-756; NVME-BASE-2.4 Rev. 2.4, §8.1.27.4.6-8.1.27.4.7, printed pp. 727-730, PDF pp. 753-756; NVME-BASE-2.4 Rev. 2.4, §5.2.13.1.38, printed pp. 313-319, PDF pp. 339-345; NVME-BASE-2.4 Rev. 2.4, §5.2.13.1.38; 8.1.27.3, printed pp. 314-319,718, PDF pp. 340-345,744; NVME-BASE-2.4 Rev. 2.4, §8.1.27.1; 8.1.27.4, printed pp. 712-713,720, PDF pp. 738-739,746

### Visual 08: Restrictions and verification reads

**View type:** `state`

```text
1. Target/state
2. Admin/I/O permission
3. PRCHK=000b and STC=0
4. Allocated media readable?
5. Data + specific status
```

**Question answered:** Evaluate the command allowlist and the NVM Read exception separately. Determine target/state, then PI checking and allocation; ordinary-read behavior cannot be applied unchanged to verification.

**Supporting Figures:** Figure 11, Figure 12, Figure 144, Figure 145, Figure 146, Figure 200, Figure 201, Figure 311

**Sources:** NVME-BASE-2.4 Rev. 2.4, §8.1.27.5; 5.1.1-5.1.2, printed pp. 178-181,730-732, PDF pp. 204-207,756-758; NVME-BASE-2.4 Rev. 2.4, §8.1.27.5, printed pp. 730-732, PDF pp. 756-758; NVME-NVM-CS-1.3 Rev. 1.3, §4.1.7; 5.12, printed pp. 113,173-175, PDF pp. 113,173-175; NVME-NVM-CS-1.3 Rev. 1.3, §5.12, printed pp. 174, PDF pp. 174; NVME-NVM-CS-1.3 Rev. 1.3, §5.12.1, printed pp. 174-175, PDF pp. 174-175; NVME-BASE-2.4 Rev. 2.4, §8.1.3.1; 8.1.27.4.2, printed pp. 587,721, PDF pp. 613,747

## Mental Model and complete teaching path

The modules follow engineering causality rather than specification-section order. Related Figures return at the point where they support the flow.

### Module 01: Two Boot read paths

**Explanation.** First determine whether an Admin-command environment exists, then choose properties or LID 15h. Both access boot contents, but their return formats and observation points differ.

```text
CAP.BPS
  ↓
BPINFO active/size
  ↓
BPMBL buffer
  ↓
BPRSEL request
  ↓
BRS result
```

#### Comparison

| Item | What it answers | Engineering note |
|---|---|---|
| Properties | BRS reports read state | Does not require CC.EN=1 |
| LID 15h | 16-byte header + data | The Admin-command CQE reports the command result |
| BPID | Selects the partition to read | Not the active ID |
| BPSZ | 128 KiB per unit | Not a byte count |

**Informative example.** With BPSZ=2, LID 15h contains 262144 bytes of boot data plus a 16-byte header, totaling 262160 bytes. Reading BP1 does not activate BP1, and a log read does not advance the property's BRS.

**Common mistake / debugging.** For an unfinished property read, inspect BRS and the buffer; reset is not an allowed normal completion step. BPINFO in LID 15h is a returned field and reading it does not modify the property of the same name.

**Supporting sources:** NVME-BASE-2.4 Rev. 2.4, §8.1.3, printed pp. 586, PDF pp. 612; NVME-BASE-2.4 Rev. 2.4, §8.1.3.1, printed pp. 586-587, PDF pp. 612-613; NVME-BASE-2.4 Rev. 2.4, §5.2.13.1.21, printed pp. 283-284, PDF pp. 309-310

**Related Figures:** Figure 36, Figure 49, Figure 50, Figure 51, Figure 279, Figure 280, Figure 679

### Module 02: The complete update and protection lifecycle

**Explanation.** Track image transfer, partition contents, active selection, and write protection separately. Successful download has not yet written a Boot Partition, and a successful write has not automatically activated it.

```text
Download in order
  ↓
Unlock target
  ↓
Commit CA=110b
  ↓
Read/verify; CA=111b
  ↓
Relock
```

#### Comparison

| Item | What it answers | Engineering note |
|---|---|---|
| FID 85h unlocked | Survives controller reset | Locked after power cycle |
| FID 85h until power cycle | Ordinary Set cannot unlock | Unavailable for shared multi-domain partitions |
| RPMB enabled/unlocked | Controller reset relocks | Protection enablement cannot be reversed |
| Both mechanisms | Only one owns control at a time | RPMB enablement transfers ownership |

**Informative example.** To leave BP0 unchanged and unlock BP1, FID 85h CDW11 is (001b << 3) | 000b = 08h. A subsequent Get does not return 000b for BP0; it returns its actual state, or 100b when RPMB owns protection.

**Common mistake / debugging.** The same reset test has different expected results for the two mechanisms. Preserve the power-cycle/reset type so that relocking can be classified as expected behavior or a defect.

**Supporting sources:** NVME-BASE-2.4 Rev. 2.4, §8.1.3.2, printed pp. 587-588, PDF pp. 613-614; NVME-BASE-2.4 Rev. 2.4, §8.1.3.2, printed pp. 588, PDF pp. 614; NVME-BASE-2.4 Rev. 2.4, §8.1.3.3, printed pp. 588-589, PDF pp. 614-615; NVME-BASE-2.4 Rev. 2.4, §5.2.30.1.39, printed pp. 513-514, PDF pp. 539-540; NVME-BASE-2.4 Rev. 2.4, §8.1.3.3.1-8.1.3.3.3, printed pp. 589-594, PDF pp. 615-620; NVME-BASE-2.4 Rev. 2.4, §5.2.30.1.39; 8.1.3.3.3, printed pp. 513-514,593-594, PDF pp. 539-540,619-620

**Related Figures:** Figure 187, Figure 542, Figure 680, Figure 681, Figure 682, Figure 683, Figure 684, Figure 756, Figure 765, Figure 766

### Module 03: Computing snapshots from Last Block

**Explanation.** Areas are differently sized views starting at the same block 1. Decode the header, select the final applicable populated area, and do not add the three Last Block numbers.

```text
Read 512-byte header
  ↓
Check DA4S/ETDAS
  ↓
Decode last blocks
  ↓
Compute inclusive extent
  ↓
Read aligned blocks
```

#### Comparison

| Item | What it answers | Engineering note |
|---|---|---|
| Area 1 | 1 through L1 | L1=0 means no data |
| Area 2 | 1 through L2 | L2 >= L1 |
| Area 3 | 1 through L3 | L3 >= L2 |
| Area 4 | 1 through L4 | Check support separately |

**Informative example.** For Last Blocks=65/1000/30000, Area 3 payload is 30000×512=15360000 bytes and the log including its header is 15360512 bytes. Values 0/1000/1000 mean Area 1 is empty and Area 3 adds no content beyond Area 2.

**Common mistake / debugging.** THS in LID 07h and TCS in LID 08h have different offsets; do not reuse one header layout for the other. Snapshot payload is vendor-defined, so unknown bytes cannot be assigned invented diagnostic fields.

**Supporting sources:** NVME-BASE-2.4 Rev. 2.4, §8.1.30; 5.2.13.1.8-5.2.13.1.9, printed pp. 232-237,733-737, PDF pp. 258-263,759-763; NVME-BASE-2.4 Rev. 2.4, §8.1.30; 5.2.30.1.15, printed pp. 476,733-734, PDF pp. 502,759-760; NVME-BASE-2.4 Rev. 2.4, §5.2.13.1.8-5.2.13.1.9, printed pp. 232-237, PDF pp. 258-263

**Related Figures:** Figure 221, Figure 223, Figure 338, Figure 491, Figure 780, Figure 781

### Module 04: Create, read, verify consistency, acknowledge

**Explanation.** Separate creating 07h data from subsequent reads; the controller decides 08h capture timing. For both, verify generation and distinguish event acknowledgement from payload deletion.

```text
Capability / event setup
  ↓
Capture or observe update
  ↓
RAE=1 chunk reads
  ↓
Recheck generation/TCDA
  ↓
08h RAE=0 acknowledgement
```

#### Comparison

| Item | What it answers | Engineering note |
|---|---|---|
| CTHID=1 | Triggers a new 07h capture | Do not create again for subsequent chunks |
| MCDA | Limits the areas created | Check MCDAS first |
| RAE=1 | Retains the event | Does not exclude another reader |
| TCDA=0 | No update since acknowledgement | In 2.4 it does not mean payload disappearance |

**Informative example.** If generation is 2Ah before reading and 2Bh afterward, the chunks cannot be accepted as one consistent capture. Even if it remains 2Ah, an 08h collection must consider the race where another host clears TCDA to zero.

**Common mistake / debugging.** Do not describe RAE=0 as deleting the snapshot or treat the AER as the payload. The event supplies a collection trigger and locator; Get Log Page still retrieves the data.

**Supporting sources:** NVME-BASE-2.4 Rev. 2.4, §5.2.13.1.8, printed pp. 232-235, PDF pp. 258-261; NVME-BASE-2.4 Rev. 2.4, §8.1.30, printed pp. 734-735, PDF pp. 760-761; NVME-BASE-2.4 Rev. 2.4, §5.2.13.1.9, printed pp. 237, PDF pp. 263; NVME-BASE-2.4 Rev. 2.4, §5.2.13.1.8-5.2.13.1.9, printed pp. 233,235,237, PDF pp. 259,261,263; NVME-BASE-2.4 Rev. 2.4, §8.1.30; 5.2.30.1.6, printed pp. 734-735,466-468, PDF pp. 760-761,492-494

**Related Figures:** Figure 204, Figure 210, Figure 211, Figure 220, Figure 222, Figure 151, Figure 152, Figure 155, Figure 474

### Module 05: Define the sanitization target first

**Explanation.** Sanitize scope is not simply everything on a disk. Classify the target, data provenance, and whether it can contain user data; this also establishes its relationship with Boot and diagnostics.

```text
Select target
  ↓
Enumerate user-data locations
  ↓
Check method/support
  ↓
Apply purge requirement
  ↓
Audit permitted evidence
```

#### Comparison

| Item | What it answers | Engineering note |
|---|---|---|
| Boot/RPMB | Unaffected by sanitize | Managed by their own mechanisms |
| Logs/features | Modify user data when necessary | Namespace media alone is insufficient |
| All namespace sanitizes | Complete work on each target | Does not thereby establish subsystem GDE |
| Crypto Erase | Changes keys and handles unencrypted data | Old key copies matter too |

**Informative example.** Even after every namespace is sanitized, that fact does not prove subsystem-level data such as CMB has undergone subsystem sanitization. Conversely, successful subsystem sanitize does not update or erase the boot image in a Boot Partition.

**Common mistake / debugging.** Using zero-filled reads as the only success criterion misclassifies results. Establish the method, allocation state, and verification state before applying NVM Command Set result definitions.

**Supporting sources:** NVME-BASE-2.4 Rev. 2.4, §8.1.27, printed pp. 711-712, PDF pp. 737-738; NVME-BASE-2.4 Rev. 2.4, §8.1.27, printed pp. 711-712, PDF pp. 737-738; NVME-BASE-2.4 Rev. 2.4, §8.1.27.2-8.1.27.3, printed pp. 714-717, PDF pp. 740-743; NVME-NVM-CS-1.3 Rev. 1.3, §5.12, printed pp. 174, PDF pp. 174

**Related Figures:** Figure 770, Figure 771, Figure 200, Figure 201

### Module 06: Combining command parameters with capabilities

**Explanation.** Separate advertised capabilities, command requests, and Feature policy. Command acceptance, operation success, and satisfaction of no-deallocate are three outcomes requiring different evidence.

```text
SANICAP / target
  ↓
SANACT and modifiers
  ↓
FID 17h policy
  ↓
Preflight and CQE
  ↓
LID 81h operation result
```

#### Comparison

| Item | What it answers | Engineering note |
|---|---|---|
| NDAS=1, NDI=0 | Successful sanitize must not deallocate | Other validity conditions still apply |
| NDAS=1, NDI=1, NODRM=0 | Command rejected | Invalid Field in Command |
| NDAS=1, NDI=1, NODRM=1 | Processing permitted | Success can report SOS=100b |
| EMVS=1 | Subsystem requires VERS=1 | Block/Crypto + NDAS=0 |

**Informative example.** SANACT=010b, AUSE=0, EMVS=1, NDAS=0, and PREQ=0 encode CDW10=0402h. It applies only with VERS/Block Erase support and other preconditions satisfied. Separately, OWPASS=0h means 16 passes, not skipping overwrite.

**Common mistake / debugging.** PREQ is bit 4 in Figure 454 but bit 11 in Figure 451. Sharing an untyped builder between the two commands can set reserved bits in the namespace command.

**Supporting sources:** NVME-BASE-2.4 Rev. 2.4, §5.2.26, printed pp. 448-451, PDF pp. 474-477; NVME-BASE-2.4 Rev. 2.4, §8.1.27.1; 5.2.27, printed pp. 713,453, PDF pp. 739,479; NVME-BASE-2.4 Rev. 2.4, §5.2.30.1.16; 8.1.27.2-8.1.27.3, printed pp. 477-478,715-719, PDF pp. 503-504,741-745; NVME-BASE-2.4 Rev. 2.4, §5.2.26, printed pp. 449, PDF pp. 475; NVME-BASE-2.4 Rev. 2.4, §5.2.26; 8.1.27.1, printed pp. 449-451,712-714, PDF pp. 475-477,738-740; NVME-BASE-2.4 Rev. 2.4, §5.2.26; 8.1.27.3, printed pp. 451,717, PDF pp. 477,743

**Related Figures:** Figure 338, Figure 451, Figure 452, Figure 453, Figure 454, Figure 492

### Module 07: Reconstruct background work from state, log, and AER

**Explanation.** Start with the seven states in Figure 772 and attach transition conditions from Figures 773–779. Status describes results, state describes the current position, and events report transitions.

```text
Idle
  ↓
Restricted/Unrestricted Processing
  ↓
Failure OR Verification
  ↓
Post-Verification Deallocation
  ↓
Idle + final log
```

#### Comparison

| Item | What it answers | Engineering note |
|---|---|---|
| Restricted Failure | Retry in restricted mode | Exit Failure Mode cannot escape it |
| Unrestricted Failure | Retry or Exit Failure Mode | Idle does not rewrite failure history |
| Media Verification | Processing succeeded | The operation is still Sanitizing |
| Post-Verification Deallocation | SPROG starts again at zero | Failure records FAILS=6h |

**Informative example.** SPROG=8000h represents 50% of the currently measured phase. Media Verification uses SPROG=FFFFh while SOS can remain 010b; leaving verification for deallocation starts progress again at zero. This is not progress regression.

**Common mistake / debugging.** Preserve SCDW10, SOS, SANS, FAILS, MVCNCLD, and event timestamps. Recording only a completion event conflates success, failure, and entry into verification.

**Supporting sources:** NVME-BASE-2.4 Rev. 2.4, §5.2.26.1; 8.1.27.1, printed pp. 451,712-713, PDF pp. 477,738-739; NVME-BASE-2.4 Rev. 2.4, §8.1.27.4, printed pp. 719-730, PDF pp. 745-756; NVME-BASE-2.4 Rev. 2.4, §8.1.27.4.6-8.1.27.4.7, printed pp. 727-730, PDF pp. 753-756; NVME-BASE-2.4 Rev. 2.4, §5.2.13.1.38, printed pp. 313-319, PDF pp. 339-345; NVME-BASE-2.4 Rev. 2.4, §5.2.13.1.38; 8.1.27.3, printed pp. 314-319,718, PDF pp. 340-345,744; NVME-BASE-2.4 Rev. 2.4, §8.1.27.1; 8.1.27.4, printed pp. 712-713,720, PDF pp. 738-739,746

**Related Figures:** Figure 312, Figure 151, Figure 152, Figure 156, Figure 772, Figure 773, Figure 774, Figure 775, Figure 776, Figure 777, Figure 778, Figure 779

### Module 08: Restrictions and verification reads

**Explanation.** Evaluate the command allowlist and the NVM Read exception separately. Determine target/state, then PI checking and allocation; ordinary-read behavior cannot be applied unchanged to verification.

```text
Target/state
  ↓
Admin/I/O permission
  ↓
PRCHK=000b and STC=0
  ↓
Allocated media readable?
  ↓
Data + specific status
```

#### Comparison

| Item | What it answers | Engineering note |
|---|---|---|
| PI checking requested | Invalid Field in Command | Not permitted for verification reads |
| Allocated media readable | Return media data | Integrity errors can be ignored when readable |
| Allocated media unreadable | Unrecovered Read Error | Do not invent data |
| Deallocated LBA | Use deallocated/unwritten rules | Not evidence of the old media pattern |

**Informative example.** A verification read with PRCHK=000b and STC=0, readable allocated LBAs, and no other abort cause completes as Successful Media Verification Read. Requesting PI checking changes the expected branch to Invalid Field in Command.

**Common mistake / debugging.** Do not assume all Get Log Page requests are permitted during subsystem sanitize; 07h/08h are absent from Figure 144. Namespace sanitize restrictions require a separate attached/target-scope evaluation.

**Supporting sources:** NVME-BASE-2.4 Rev. 2.4, §8.1.27.5; 5.1.1-5.1.2, printed pp. 178-181,730-732, PDF pp. 204-207,756-758; NVME-BASE-2.4 Rev. 2.4, §8.1.27.5, printed pp. 730-732, PDF pp. 756-758; NVME-NVM-CS-1.3 Rev. 1.3, §4.1.7; 5.12, printed pp. 113,173-175, PDF pp. 113,173-175; NVME-NVM-CS-1.3 Rev. 1.3, §5.12, printed pp. 174, PDF pp. 174; NVME-NVM-CS-1.3 Rev. 1.3, §5.12.1, printed pp. 174-175, PDF pp. 174-175; NVME-BASE-2.4 Rev. 2.4, §8.1.3.1; 8.1.27.4.2, printed pp. 587,721, PDF pp. 613,747

**Related Figures:** Figure 11, Figure 12, Figure 144, Figure 145, Figure 146, Figure 200, Figure 201, Figure 311

## Source-located specification findings

The mental model above explains causality. This section preserves each source-located conclusion and its normative strength for speaker notes and review.

### 1. Two Boot Partitions

<!-- claim:BASEBTS-BOOT-MODEL -->

Boot Partitions are optional; support provides two equally sized partitions with IDs 0h and 1h. A host can read through properties without creating queues or enabling the controller.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §8.1.3, printed pages 586, PDF pages 612

### 2. Property reads and BRS

<!-- claim:BASEBTS-BOOT-READ -->

The host checks CAP.BPS and the active ID/size in BPINFO, allocates a contiguous buffer and programs BPMBL, then writes BPRSEL only when no read is active. BRS=01b means transfer in progress, 10b success, and 11b error; reset, shutdown, and changes to transport-specific properties are prohibited during the read.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §8.1.3.1, printed pages 586-587, PDF pages 612-613

### 3. The alternative LID 15h read path

<!-- claim:BASEBTS-BOOT-LOG -->

LID 15h selects a partition through BPID in CDW10.LSP and returns a 16-byte header followed by data; BPSZ is measured in 128 KiB units. Reading this log does not modify the BPINFO, BPRSEL, or BPMBL properties.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.21, printed pages 283-284, PDF pages 309-310

### 4. Download, write, verify, activate

<!-- claim:BASEBTS-BOOT-UPDATE -->

A boot image is downloaded in order from its beginning using Firmware Image Download. After unlocking the target, Firmware Commit CA=110b writes the partition selected by BPID. The host may read it back, use CA=111b to change the active ID, and relock it. An interrupted update can leave mixed old/new contents, so verification before activation is recommended.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §8.1.3.2, printed pages 587-588, PDF pages 613-614

### 5. Update-sequence boundaries

<!-- claim:BASEBTS-BOOT-SEQUENCE -->

The host should avoid reading a Boot Partition while it is being written and should avoid overlapping firmware/boot-image update sequences. A single sequence should use the same controller or Management Endpoint; crossing endpoints may cause Commit to end with Invalid Firmware Image.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §8.1.3.2, printed pages 588, PDF pages 614

### 6. Protection capabilities and ownership

<!-- claim:BASEBTS-BOOT-CAP -->

BPCAP reports Set Features and RPMB boot-protection capabilities. FID 85h controls protection when it is the only mechanism or RPMB protection is not enabled; enabled RPMB protection takes control. Only one mechanism owns the state at a time, and all controllers sharing a partition enforce its protection.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §8.1.3.3, printed pages 588-589, PDF pages 614-615

### 7. Decoding FID 85h

<!-- claim:BASEBTS-BOOT-FID -->

BP0WPS occupies CDW11[2:0] and BP1WPS [5:3]. Value 000b is a Set-only no-change request; 001b/010b/011b mean unlocked/locked/locked until power cycle. Get reports 100b for RPMB ownership, but it is not a valid Set value. This Feature is not saveable and defaults to locked after a power cycle.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.39, printed pages 513-514, PDF pages 539-540

### 8. Reset differences between protection mechanisms

<!-- claim:BASEBTS-BOOT-RESET -->

Set Features unlocked state survives a Controller Level Reset but returns to locked after a power cycle; ordinary Set cannot escape locked-until-power-cycle. With RPMB protection enabled, either a power cycle or Controller Level Reset relocks an unlocked partition, and enabling protection is irreversible.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §8.1.3.3.1-8.1.3.3.3, printed pages 589-594, PDF pages 615-620

### 9. Protection-state rejection conditions

<!-- claim:BASEBTS-BOOT-REJECT -->

FID 85h rejects changes to locked-until-power-cycle or RPMB-owned states with Feature Not Changeable. A shared partition in a multi-domain subsystem cannot use locked-until-power-cycle. When both mechanisms exist, RPMB boot protection cannot be enabled while either partition is in that state to bypass it.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.39; 8.1.3.3.3, printed pages 513-514,593-594, PDF pages 539-540,619-620

### 10. Header and cumulative Data Areas

<!-- claim:BASEBTS-TEL-MODEL -->

Telemetry uses block 0 for its header and 512-byte blocks. Every Data Area begins at block 1. Areas 2/3/4 are larger cumulative sets, not disjoint regions placed after Area 1. Last Block is an inclusive block number; payload format and size are vendor-defined.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §8.1.30; 5.2.13.1.8-5.2.13.1.9, printed pages 232-237,733-737, PDF pages 258-263,759-763

### 11. CTHID and MCDA

<!-- claim:BASEBTS-TEL-CREATE -->

CTHID for LID 07h is CDW10 bit 8: one requests a new capture and zero does not update that snapshot. MCDA occupies bits 11:9 and applies only when MCDAS=1 and CTHID=1; 001b through 100b request creation through Areas 1 through 4, while 000b lets the controller decide. MCDAS comes from the LID Specific Parameter in Supported Log Pages.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.8, printed pages 232-235, PDF pages 258-261

### 12. Both sides of Data Area 4 support

<!-- claim:BASEBTS-TEL-DA4 -->

The controller advertises Telemetry through LPA.TS and Area 4 through LPA.DA4S; the host advertises support with ETDAS=1 in FID 16h Host Behavior Support. DA4S and ETDAS together determine Area 4 applicability; creating Area 4 also requires a populated Area 3.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §8.1.30; 5.2.30.1.15, printed pages 476,733-734, PDF pages 502,759-760

### 13. Offsets, lengths, and defined ranges

<!-- claim:BASEBTS-TEL-ALIGN -->

For LID 07h/08h, offset and transfer length must be multiples of 512 bytes or the command reports Invalid Field in Command. The controller returns requested blocks, but data beyond the applicable final Data Area boundary has undefined contents.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.8-5.2.13.1.9, printed pages 232-237, PDF pages 258-263

### 14. Consistency and read acknowledgement

<!-- claim:BASEBTS-TEL-CONSISTENCY -->

The host records the header generation, collects chunks with RAE=1, and rereads the header; a changed generation calls for rereading. For 08h it also checks that another reader has not cleared TCDA, then acknowledges completion by reading any portion with RAE=0. Generation is eight bits and wraps from FFh to 0h.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §8.1.30, printed pages 734-735, PDF pages 760-761

### 15. TCDA=0 in revision 2.4

<!-- claim:BASEBTS-TEL-TCDA -->

In Base 2.4, TCDA=0 means no update since the last successful RAE=0 read. The header is readable before the first capture; after a capture, both the header and current saved internal state are returned even with TCDA=0. The older interpretation that zero means header-only must not be carried into 2.4.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.9, printed pages 237, PDF pages 263

### 16. Snapshot persistence conditions

<!-- claim:BASEBTS-TEL-PERSIST -->

The 07h snapshot stays unchanged until another CTHID=1 request, Firmware Commit, or power-on reset. For 08h, Areas 1–3 persist across all resets and Area 4 may persist across Controller Level Resets; TCDA and TCDGN persist across power cycles and resets.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.8-5.2.13.1.9, printed pages 233,235,237, PDF pages 259,261,263

### 17. Enabling Telemetry notices

<!-- claim:BASEBTS-TEL-EVENT -->

The host enables Telemetry Log Notices with TLN bit 10 of FID 0Bh. The controller reports a Notice-type Telemetry Log Changed AER; TCDA in 07h/08h also exposes an update. The .1.5 reference in 8.1.30 is misplaced: AEC is actually in 5.2.30.1.6 in this revision.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §8.1.30; 5.2.30.1.6, printed pages 734-735,466-468, PDF pages 760-761,492-494

### 18. Subsystem versus namespace scope

<!-- claim:BASEBTS-SAN-SCOPE -->

Subsystem and namespace sanitize cover different data. Sanitizing every namespace individually is not equivalent to subsystem sanitize and does not thereby set subsystem GDE to one. Neither affects Boot Partitions or RPMB; logs/features containing user data may need modification.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §8.1.27, printed pages 711-712, PDF pages 737-738

### 19. Cache and memory boundaries

<!-- claim:BASEBTS-SAN-MEDIA -->

Sanitize covers the target's allocated/deallocated media and caches holding its user data. For subsystem sanitize, modification of CMB queue contents is implementation-defined while other CMB data is processed; HMB is unaffected. PMR must be disabled before subsystem sanitize starts and its data is within scope; namespace sanitize does not affect CMB, HMB, PMR, or PDA.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §8.1.27, printed pages 711-712, PDF pages 737-738

### 20. Three methods and clear/purge

<!-- claim:BASEBTS-SAN-METHOD -->

Block Erase uses media-specific erasure; Crypto Erase changes all relevant media encryption keys and processes unencrypted data with appropriate methods; Overwrite writes a pattern. PREQ/SPRRS govern purge requests and reporting. Crypto Erase must fail if old keys or unencrypted data requiring sanitization remain unaltered.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §8.1.27.2-8.1.27.3, printed pages 714-717, PDF pages 740-743

### 21. Sanitize command encoding

<!-- claim:BASEBTS-SAN-COMMAND -->

CDW10 contains SANACT[2:0], AUSE[3], OWPASS[7:4], OIPBP[8], NDAS[9], EMVS[10], and PREQ[11]; CDW11 contains OVRPAT. SANACT 001b selects Exit Failure Mode, 010b Block Erase, 011b Overwrite, 100b Crypto Erase, and 101b Exit Media Verification; other values are reserved.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.26, printed pages 448-451, PDF pages 474-477

### 22. Sanitize Namespace has a different field layout

<!-- claim:BASEBTS-SAN-NAMESPACE -->

Figure 454, referenced by the main scope, defines the namespace command: SANACT permits only 001b, 100b, and 101b; AUSE is bit 3, PREQ bit 4, and EMVS bit 10. There are no Overwrite/NDAS fields, so subsystem Sanitize CDW10 cannot be copied unchanged.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §8.1.27.1; 5.2.27, printed pages 713,453, PDF pages 739,479

### 23. NDAS, NDI, NODRM, and NODMMAS

<!-- claim:BASEBTS-SAN-NDAS -->

NDAS requests retained allocation for this command; NDI indicates inhibition of that request. With NDAS=1 and NDI=1, NODRM=0 in FID 17h rejects the command with Invalid Field in Command, while NODRM=1 permits processing and reports unexpected deallocation as SOS=100b after success. NODMMAS=10b separately describes additional media modification when applicable.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.16; 8.1.27.2-8.1.27.3, printed pages 477-478,715-719, PDF pages 503-504,741-745

### 24. Command combinations for Media Verification

<!-- claim:BASEBTS-SAN-EMVS -->

Subsystem sanitize with EMVS=1 requires VERS=1, Block Erase or Crypto Erase, and NDAS=0; combining it with Overwrite or NDAS=1 is rejected with Invalid Field in Command. SANACT=101b applies only in Media Verification and starts subsequent deallocation rather than a new sanitize operation.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.26, printed pages 449, PDF pages 475

### 25. Rejections before starting

<!-- claim:BASEBTS-SAN-PREFLIGHT -->

Enabled PMR, namespace write protection, a suspended controller, or pending firmware activation/reset may prevent subsystem sanitize. If the initiating command does not return Successful Completion, it starts no operation, changes no target Sanitize Status, and alters no user data; an anticipated operation failure should instead be reported through the subsequent log.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.26; 8.1.27.1, printed pages 449-451,712-714, PDF pages 475-477,738-740

### 26. A CQE is not sanitize completion

<!-- claim:BASEBTS-SAN-BACKGROUND -->

Sanitize runs in the background. Starting an operation updates LID 81h before completing its initiating command; the host uses the status log and events for subsequent progress. An active operation cannot be aborted and continues across reset/power cycle, although specified resets may cancel verification.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.26.1; 8.1.27.1, printed pages 451,712-713, PDF pages 477,738-739

### 27. Overwrite-pass parity

<!-- claim:BASEBTS-SAN-OVERWRITE -->

OWPASS=0h means 16 passes. With OIPBP=0, user data uses OVRPAT and PI bytes are FFh. With OIPBP=1 and an even pass count, the first pass uses the inverted pattern and PI=00h; with an odd count it starts with the original pattern and PI=FFh, then inverts on each subsequent pass.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.26; 8.1.27.3, printed pages 451,717, PDF pages 477,743

### 28. Seven states and two failure paths

<!-- claim:BASEBTS-SAN-STATE -->

Each supported target has its own state machine. AUSE=0/1 selects Restricted/Unrestricted Processing, and failure enters the corresponding Failure state. Restricted Failure requires a restricted sanitize retry; Unrestricted Failure permits retry or Exit Failure Mode to Idle. Idle therefore does not necessarily mean the last sanitize succeeded.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §8.1.27.4, printed pages 719-730, PDF pages 745-756

### 29. Verification and deallocation transitions

<!-- claim:BASEBTS-SAN-VERIFY-STATE -->

Successful processing enters Media Verification when requested by EMVS and not canceled. Exit Media Verification, an applicable reset, or a composition change preventing verification moves the target to Post-Verification Deallocation. Success returns to Idle; failure follows the original AUSE into Restricted/Unrestricted Failure with FAILS=6h.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §8.1.27.4.6-8.1.27.4.7, printed pages 727-730, PDF pages 753-756

### 30. Scope and state in LID 81h

<!-- claim:BASEBTS-SAN-STATUS -->

For LID 81h, NSID=0h or FFFFFFFFh selects the subsystem and an allocated NSID selects a namespace. SSTAT includes SOS, OPC, GDE, MVCNCLD, NDE, and PRGD; SSI contains SANS/FAILS; SCDW10 records initiating parameters. MNSOIP reports the concurrent namespace-operation limit and STNSID identifies a namespace target. The log persists across power cycles/resets.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.38, printed pages 313-319, PDF pages 339-345

### 31. SPROG and time estimates

<!-- claim:BASEBTS-SAN-PROGRESS -->

SPROG is raw/65536 and reports progress for Processing or Post-Verification Deallocation, resetting to zero on entry. It can be FFFFh in Media Verification while SOS still says Sanitizing, so it cannot alone prove completion. Time estimates distinguish method and additional media modification; FFFFFFFFh means no estimate is reported.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.38; 8.1.27.3, printed pages 314-319,718, PDF pages 340-345,744

### 32. Three Sanitize events

<!-- claim:BASEBTS-SAN-EVENT -->

Sanitize AERs use AET=110b and LID=81h; AEI=01h/02h/03h means Completed, Completed With Unexpected Deallocation, or Entered Media Verification. DW1 EVNTSP is zero for the subsystem or the target NSID. Interpret the event together with the log: Completed does not automatically mean success.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §8.1.27.1; 8.1.27.4, printed pages 712-713,720, PDF pages 738-739,746

### 33. Command restrictions during execution

<!-- claim:BASEBTS-SAN-RESTRICT -->

During subsystem sanitize, Figure 144 identifies allowed Admin commands and log pages; Boot Partition is listed but Telemetry 07h/08h is not. Disallowed operations are restricted with Sanitize In Progress. Namespace sanitize instead uses Figures 145/146 and the target NSID. NVM Reads in Media Verification have a specific exception.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §8.1.27.5; 5.1.1-5.1.2, printed pages 178-181,730-732, PDF pages 204-207,756-758

### 34. Multiple controllers, power, and firmware restrictions

<!-- claim:BASEBTS-SAN-POWER -->

Starting sanitize updates the target log on controllers and suspends autonomous power-state management. Affected I/O/self-tests are aborted and relevant streams released according to the target; new firmware activation is prohibited while the operation is active. A subsystem operation also prevents PMR enablement and PDA access.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §8.1.27.5, printed pages 730-732, PDF pages 756-758

### 35. Where the NVM Command Set extends behavior

<!-- claim:BASEBTS-NVM-BRIDGE -->

NVM 4.1.7 uses the Base Sanitize command; 5.12 adds permitted Admin behavior, post-sanitize data values, and Media Verification Reads. Error Information returns zero in LBA, while other fields containing user data remain subject to Base processing.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-NVM-CS-1.3, Rev. 1.3, §4.1.7; 5.12, printed pages 113,173-175, PDF pages 113,173-175

### 36. Sanitize does not imply zero-filled reads

<!-- claim:BASEBTS-NVM-VALUES -->

After success, audit values are vendor-specific for Block Erase, indeterminate for Crypto Erase, and governed by the Base pattern mechanism for Overwrite. Reads of deallocated blocks instead follow Deallocated or Unwritten Logical Blocks rules; PI-checking reads without deallocation may encounter PI check errors.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-NVM-CS-1.3, Rev. 1.3, §5.12, printed pages 174, PDF pages 174

### 37. Three Media Verification Read branches

<!-- claim:BASEBTS-NVM-VERIFY -->

A Media Verification Read requests no PI checking: PRCHK=000b and STC=0. Readable allocated media returns its data while ignoring integrity errors when the media can be read, completing with Successful Media Verification Read unless another error aborts it. Unreadable allocated media produces Unrecovered Read Error. Requesting PI checking produces Invalid Field in Command.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-NVM-CS-1.3, Rev. 1.3, §5.12.1, printed pages 174-175, PDF pages 174-175

### 38. Checking source cross-references

<!-- claim:BASEBTS-SOURCE-XREF -->

The boot-log section 0 reference can be resolved within the same revision to LID 15h in 5.2.13.1.21. The SPROG paragraph cites Figure 311, which actually describes Reservation Notification; SPROG is defined in Figure 312. These are suspected cross-reference defects found by internal comparison, not claimed official errata.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §8.1.3.1; 8.1.27.4.2, printed pages 587,721, PDF pages 613,747

## Figure index

This report introduces all 80 in-scope Figures. Use the section links below for the 100-minute presentation path; every Figure remains available as an appendix item. 48 Figures are outside the main section range but are included to explain cited dependencies and necessary prerequisites.

- [§5.12](#section-5-12)

- [§5.2](#section-5-2)

- [§8.1](#section-8-1)

- [Referenced Figure dependencies (outside the main section range)](#section-dependency)

## Figure and field-table teaching reference

The source uses Figure numbers for diagrams and field-layout tables. No source artwork is reproduced; compact field and keyword indexes come from the locally verified PDFs.

<a id="section-5-12"></a>

### §5.12

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 200: Sanitize Operations - Admin Commands Allowed</strong></summary>

<!-- claim:BASEBTS-NVMCS-FIG-200-CLAIM figure-table:BASEBTS-NVMCS-FIG-200 -->

**SPEC.** Figure 200, "Sanitize Operations - Admin Commands Allowed": The NVM Command Set adds Error Information behavior during sanitize: return zero in LBA. Base Figure 200 is a different table and cannot be substituted. Decode the source-specific fields below.

#### Where this Figure fits

The NVM Command Set adds Error Information behavior during sanitize: return zero in LBA. Base Figure 200 is a different table and cannot be substituted.

The indexed fields below belong to this source document and this Figure. The worked example connects them to the full operation.

#### Teaching redraw

```text
[Locate source: Get Log Page]
          ↓
[Extract field: Error Information] → [Apply encoding: LBA]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `Get Log Page` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `Error Information` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `LBA` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Confirm NVME-NVM-CS-1.3, §5.12, Figure 200; equal Figure numbers in different documents are different sources.
2. Apply the field/state rule above to the captured raw input.
3. Evaluate the command allowlist and the NVM Read exception separately. Determine target/state, then PI checking and allocation; ordinary-read behavior cannot be applied unchanged to verification.
4. Compare the observation with the worked scenario and retain the cited source and target identity.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 200 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §5.12 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| Rule | The NVM Command Set adds Error Information behavior during sanitize: return zero in LBA. Base Figure 200 is a different table and cannot be substituted. |
| Boundary | Do not assume all Get Log Page requests are permitted during subsystem sanitize; 07h/08h are absent from Figure 144. Namespace sanitize restrictions require a separate attached/target-scope evaluation. |

**Informative example.** A verification read with PRCHK=000b and STC=0, readable allocated LBAs, and no other abort cause completes as Successful Media Verification Read. Requesting PI checking changes the expected branch to Invalid Field in Command.

**Common misconception.** Do not assume all Get Log Page requests are permitted during subsystem sanitize; 07h/08h are absent from Figure 144. Namespace sanitize restrictions require a separate attached/target-scope evaluation.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Symptom / correction | Do not assume all Get Log Page requests are permitted during subsystem sanitize; 07h/08h are absent from Figure 144. Namespace sanitize restrictions require a separate attached/target-scope evaluation. |

#### Questions the reader should now answer

1. Which source-specific fields establish the decision?
2. Which capability, target, or state would change the worked result?

**Source field index:** Get Log Page, Error Information, LBA

**Source keyword index:** none

> Source: NVME-NVM-CS-1.3, Rev. 1.3, §5.12, Figure 200, printed pages 173, PDF pages 173

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 201: Sanitize Operation Types - User Data Values</strong></summary>

<!-- claim:BASEBTS-NVMCS-FIG-201-CLAIM figure-table:BASEBTS-NVMCS-FIG-201 -->

**SPEC.** Figure 201, "Sanitize Operation Types - User Data Values": Audit values are vendor-specific, indeterminate, or governed by Overwrite for the three methods; deallocated-block reads follow separate rules. Decode the source-specific fields below.

#### Where this Figure fits

Audit values are vendor-specific, indeterminate, or governed by Overwrite for the three methods; deallocated-block reads follow separate rules.

The indexed fields below belong to this source document and this Figure. The worked example connects them to the full operation.

#### Teaching redraw

```text
[Locate source: Block Erase]
          ↓
[Extract field: Crypto Erase] → [Apply encoding: Overwrite]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `Block Erase` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `Crypto Erase` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `Overwrite` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Confirm NVME-NVM-CS-1.3, §5.12, Figure 201; equal Figure numbers in different documents are different sources.
2. Apply the field/state rule above to the captured raw input.
3. Sanitize scope is not simply everything on a disk. Classify the target, data provenance, and whether it can contain user data; this also establishes its relationship with Boot and diagnostics.
4. Compare the observation with the worked scenario and retain the cited source and target identity.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 201 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §5.12 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| Rule | Audit values are vendor-specific, indeterminate, or governed by Overwrite for the three methods; deallocated-block reads follow separate rules. |
| Boundary | Using zero-filled reads as the only success criterion misclassifies results. Establish the method, allocation state, and verification state before applying NVM Command Set result definitions. |

**Informative example.** Even after every namespace is sanitized, that fact does not prove subsystem-level data such as CMB has undergone subsystem sanitization. Conversely, successful subsystem sanitize does not update or erase the boot image in a Boot Partition.

**Common misconception.** Using zero-filled reads as the only success criterion misclassifies results. Establish the method, allocation state, and verification state before applying NVM Command Set result definitions.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Symptom / correction | Using zero-filled reads as the only success criterion misclassifies results. Establish the method, allocation state, and verification state before applying NVM Command Set result definitions. |

#### Questions the reader should now answer

1. Which source-specific fields establish the decision?
2. Which capability, target, or state would change the worked result?

**Source field index:** Block Erase, Crypto Erase, Overwrite

**Source keyword index:** shall not, shall, may

> Source: NVME-NVM-CS-1.3, Rev. 1.3, §5.12, Figure 201, printed pages 174, PDF pages 174

</details>

<a id="section-5-2"></a>

### §5.2

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 220: Telemetry Host-Initiated Log Specific Parameter Field</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-220-CLAIM figure-table:BASEBTS-BASE-FIG-220 -->

**SPEC.** Figure 220, "Telemetry Host-Initiated Log Specific Parameter Field": CTHID occupies CDW10 bit 8 and MCDA bits 11:9. Apply MCDA only with MCDAS=1 and CTHID=1; subsequent reads of that snapshot use CTHID=0. Decode the source-specific fields below.

#### Where this Figure fits

CTHID occupies CDW10 bit 8 and MCDA bits 11:9. Apply MCDA only with MCDAS=1 and CTHID=1; subsequent reads of that snapshot use CTHID=0.

The indexed fields below belong to this source document and this Figure. The worked example connects them to the full operation.

#### Teaching redraw

```text
[Locate source: CTHID]
          ↓
[Extract field: MCDA] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `CTHID` | Create Telemetry Host-Initiated Data; the 07h capture request, cleared for subsequent reads of that snapshot. |
| `MCDA` | Maximum Created Data Area; selects the largest area to create when supported and capture is requested. |

#### Read in this order

1. Confirm NVME-BASE-2.4, §5.2.13.1.8, Figure 220; equal Figure numbers in different documents are different sources.
2. Apply the field/state rule above to the captured raw input.
3. Separate creating 07h data from subsequent reads; the controller decides 08h capture timing. For both, verify generation and distinguish event acknowledgement from payload deletion.
4. Compare the observation with the worked scenario and retain the cited source and target identity.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 220 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §5.2.13.1.8 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| Rule | CTHID occupies CDW10 bit 8 and MCDA bits 11:9. Apply MCDA only with MCDAS=1 and CTHID=1; subsequent reads of that snapshot use CTHID=0. |
| Boundary | Do not describe RAE=0 as deleting the snapshot or treat the AER as the payload. The event supplies a collection trigger and locator; Get Log Page still retrieves the data. |

**Informative example.** If generation is 2Ah before reading and 2Bh afterward, the chunks cannot be accepted as one consistent capture. Even if it remains 2Ah, an 08h collection must consider the race where another host clears TCDA to zero.

**Common misconception.** Do not describe RAE=0 as deleting the snapshot or treat the AER as the payload. The event supplies a collection trigger and locator; Get Log Page still retrieves the data.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Symptom / correction | Do not describe RAE=0 as deleting the snapshot or treat the AER as the payload. The event supplies a collection trigger and locator; Get Log Page still retrieves the data. |

#### Questions the reader should now answer

1. Which source-specific fields establish the decision?
2. Which capability, target, or state would change the worked result?

**Source field index:** CTHID, MCDA

**Source keyword index:** shall not, shall, may, reserved

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.8, Figure 220, printed pages 232-233, PDF pages 258-259

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 221: Telemetry Host-Initiated Log Page</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-221-CLAIM figure-table:BASEBTS-BASE-FIG-221 -->

**SPEC.** Figure 221, "Telemetry Host-Initiated Log Page": For 07h, Last Blocks occupy bytes 8–19, THS 380, THDGN 381, TCDA/TCDGN 382/383, and RID 384–511. Read the header before fetching cumulative-area payloads. Decode the source-specific fields below.

#### Where this Figure fits

For 07h, Last Blocks occupy bytes 8–19, THS 380, THDGN 381, TCDA/TCDGN 382/383, and RID 384–511. Read the header before fetching cumulative-area payloads.

The indexed fields below belong to this source document and this Figure. The worked example connects them to the full operation.

#### Teaching redraw

```text
[Locate source: THDA1LB]
          ↓
[Extract field: THDA2LB] → [Apply encoding: THDA3LB]
                                      ↓
[Validate evidence: THDA4LB]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `THDA1LB` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `THDA2LB` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `THDA3LB` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `THDA4LB` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `THS` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `THDGN` | Telemetry Host-Initiated Data Generation Number; checks whether chunks still belong to one snapshot. |
| `TCDA` | Telemetry Controller-Initiated Data Available; in 2.4, indicates an update since the last RAE=0 acknowledgement. |
| `TCDGN` | Telemetry Controller-Initiated Data Generation Number; an eight-bit generation incremented at the end of an update. |
| `RID` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Confirm NVME-BASE-2.4, §5.2.13.1.8, Figure 221; equal Figure numbers in different documents are different sources.
2. Apply the field/state rule above to the captured raw input.
3. Areas are differently sized views starting at the same block 1. Decode the header, select the final applicable populated area, and do not add the three Last Block numbers.
4. Compare the observation with the worked scenario and retain the cited source and target identity.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 221 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §5.2.13.1.8 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| Rule | For 07h, Last Blocks occupy bytes 8–19, THS 380, THDGN 381, TCDA/TCDGN 382/383, and RID 384–511. Read the header before fetching cumulative-area payloads. |
| Boundary | THS in LID 07h and TCS in LID 08h have different offsets; do not reuse one header layout for the other. Snapshot payload is vendor-defined, so unknown bytes cannot be assigned invented diagnostic fields. |

**Informative example.** For Last Blocks=65/1000/30000, Area 3 payload is 30000×512=15360000 bytes and the log including its header is 15360512 bytes. Values 0/1000/1000 mean Area 1 is empty and Area 3 adds no content beyond Area 2.

**Common misconception.** THS in LID 07h and TCS in LID 08h have different offsets; do not reuse one header layout for the other. Snapshot payload is vendor-defined, so unknown bytes cannot be assigned invented diagnostic fields.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Symptom / correction | THS in LID 07h and TCS in LID 08h have different offsets; do not reuse one header layout for the other. Snapshot payload is vendor-defined, so unknown bytes cannot be assigned invented diagnostic fields. |

#### Questions the reader should now answer

1. Which source-specific fields establish the decision?
2. Which capability, target, or state would change the worked result?

**Source field index:** THDA1LB, THDA2LB, THDA3LB, THDA4LB, THS, THDGN, TCDA, TCDGN, RID

**Source keyword index:** shall not, shall, should, may, reserved

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.8, Figure 221, printed pages 234-235, PDF pages 260-261

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 222: Telemetry Host-Initiated Log Page - LID Specific Parameter Field</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-222-CLAIM figure-table:BASEBTS-BASE-FIG-222 -->

**SPEC.** Figure 222, "Telemetry Host-Initiated Log Page - LID Specific Parameter Field": LID Specific Parameter bit 0 is MCDAS. It advertises MCDA support, not which area has already been created. Decode the source-specific fields below.

#### Where this Figure fits

LID Specific Parameter bit 0 is MCDAS. It advertises MCDA support, not which area has already been created.

The indexed fields below belong to this source document and this Figure. The worked example connects them to the full operation.

#### Teaching redraw

```text
[Locate source: MCDAS]
          ↓
[Extract field: evidence] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `MCDAS` | Maximum Created Data Area Supported; bit 0 of the 07h LID Specific Parameter, advertising MCDA support. |

#### Read in this order

1. Confirm NVME-BASE-2.4, §5.2.13.1.8, Figure 222; equal Figure numbers in different documents are different sources.
2. Apply the field/state rule above to the captured raw input.
3. Separate creating 07h data from subsequent reads; the controller decides 08h capture timing. For both, verify generation and distinguish event acknowledgement from payload deletion.
4. Compare the observation with the worked scenario and retain the cited source and target identity.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 222 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §5.2.13.1.8 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| Rule | LID Specific Parameter bit 0 is MCDAS. It advertises MCDA support, not which area has already been created. |
| Boundary | Do not describe RAE=0 as deleting the snapshot or treat the AER as the payload. The event supplies a collection trigger and locator; Get Log Page still retrieves the data. |

**Informative example.** If generation is 2Ah before reading and 2Bh afterward, the chunks cannot be accepted as one consistent capture. Even if it remains 2Ah, an 08h collection must consider the race where another host clears TCDA to zero.

**Common misconception.** Do not describe RAE=0 as deleting the snapshot or treat the AER as the payload. The event supplies a collection trigger and locator; Get Log Page still retrieves the data.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Symptom / correction | Do not describe RAE=0 as deleting the snapshot or treat the AER as the payload. The event supplies a collection trigger and locator; Get Log Page still retrieves the data. |

#### Questions the reader should now answer

1. Which source-specific fields establish the decision?
2. Which capability, target, or state would change the worked result?

**Source field index:** MCDAS

**Source keyword index:** shall, may, reserved

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.8, Figure 222, printed pages 235, PDF pages 261

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 223: Telemetry Controller-Initiated Log Page</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-223-CLAIM figure-table:BASEBTS-BASE-FIG-223 -->

**SPEC.** Figure 223, "Telemetry Controller-Initiated Log Page": For 08h, TCS is byte 381 and TCDA/TCDGN are 382/383. TCDGN increments as the final update step; reread the header after collection. Interpret TCDA=0 using 2.4's no-update-since-acknowledgement meaning. Decode the source-specific fields below.

#### Where this Figure fits

For 08h, TCS is byte 381 and TCDA/TCDGN are 382/383. TCDGN increments as the final update step; reread the header after collection. Interpret TCDA=0 using 2.4's no-update-since-acknowledgement meaning.

The indexed fields below belong to this source document and this Figure. The worked example connects them to the full operation.

#### Teaching redraw

```text
[Locate source: TCDA1LB]
          ↓
[Extract field: TCDA2LB] → [Apply encoding: TCDA3LB]
                                      ↓
[Validate evidence: TCDA4LB]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `TCDA1LB` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `TCDA2LB` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `TCDA3LB` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `TCDA4LB` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `TCS` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `TCDA` | Telemetry Controller-Initiated Data Available; in 2.4, indicates an update since the last RAE=0 acknowledgement. |
| `TCDGN` | Telemetry Controller-Initiated Data Generation Number; an eight-bit generation incremented at the end of an update. |
| `RID` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Confirm NVME-BASE-2.4, §5.2.13.1.9, Figure 223; equal Figure numbers in different documents are different sources.
2. Apply the field/state rule above to the captured raw input.
3. Separate creating 07h data from subsequent reads; the controller decides 08h capture timing. For both, verify generation and distinguish event acknowledgement from payload deletion.
4. Compare the observation with the worked scenario and retain the cited source and target identity.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 223 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §5.2.13.1.9 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| Rule | For 08h, TCS is byte 381 and TCDA/TCDGN are 382/383. TCDGN increments as the final update step; reread the header after collection. Interpret TCDA=0 using 2.4's no-update-since-acknowledgement meaning. |
| Boundary | Do not describe RAE=0 as deleting the snapshot or treat the AER as the payload. The event supplies a collection trigger and locator; Get Log Page still retrieves the data. |

**Informative example.** If generation is 2Ah before reading and 2Bh afterward, the chunks cannot be accepted as one consistent capture. Even if it remains 2Ah, an 08h collection must consider the race where another host clears TCDA to zero.

**Common misconception.** Do not describe RAE=0 as deleting the snapshot or treat the AER as the payload. The event supplies a collection trigger and locator; Get Log Page still retrieves the data.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Symptom / correction | Do not describe RAE=0 as deleting the snapshot or treat the AER as the payload. The event supplies a collection trigger and locator; Get Log Page still retrieves the data. |

#### Questions the reader should now answer

1. Which source-specific fields establish the decision?
2. Which capability, target, or state would change the worked result?

**Source field index:** TCDA1LB, TCDA2LB, TCDA3LB, TCDA4LB, TCS, TCDA, TCDGN, RID

**Source keyword index:** shall not, shall, should, may, reserved

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.9, Figure 223, printed pages 236-237, PDF pages 262-263

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 279: Boot Partition Log Specific Parameter Field</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-279-CLAIM figure-table:BASEBTS-BASE-FIG-279 -->

**SPEC.** Figure 279, "Boot Partition Log Specific Parameter Field": LID 15h uses CDW10 bit 8 as BPID and reserves other LSP bits; that same bit means CTHID for 07h. Decode the source-specific fields below.

#### Where this Figure fits

LID 15h uses CDW10 bit 8 as BPID and reserves other LSP bits; that same bit means CTHID for 07h.

The indexed fields below belong to this source document and this Figure. The worked example connects them to the full operation.

#### Teaching redraw

```text
[Locate source: BPID]
          ↓
[Extract field: evidence] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `BPID` | Boot Partition Identifier; selects 0 or 1 independently of the active partition. |

#### Read in this order

1. Confirm NVME-BASE-2.4, §5.2.13.1.21, Figure 279; equal Figure numbers in different documents are different sources.
2. Apply the field/state rule above to the captured raw input.
3. First determine whether an Admin-command environment exists, then choose properties or LID 15h. Both access boot contents, but their return formats and observation points differ.
4. Compare the observation with the worked scenario and retain the cited source and target identity.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 279 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §5.2.13.1.21 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| Rule | LID 15h uses CDW10 bit 8 as BPID and reserves other LSP bits; that same bit means CTHID for 07h. |
| Boundary | For an unfinished property read, inspect BRS and the buffer; reset is not an allowed normal completion step. BPINFO in LID 15h is a returned field and reading it does not modify the property of the same name. |

**Informative example.** With BPSZ=2, LID 15h contains 262144 bytes of boot data plus a 16-byte header, totaling 262160 bytes. Reading BP1 does not activate BP1, and a log read does not advance the property's BRS.

**Common misconception.** For an unfinished property read, inspect BRS and the buffer; reset is not an allowed normal completion step. BPINFO in LID 15h is a returned field and reading it does not modify the property of the same name.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Symptom / correction | For an unfinished property read, inspect BRS and the buffer; reset is not an allowed normal completion step. BPINFO in LID 15h is a returned field and reading it does not modify the property of the same name. |

#### Questions the reader should now answer

1. Which source-specific fields establish the decision?
2. Which capability, target, or state would change the worked result?

**Source field index:** BPID

**Source keyword index:** shall, reserved

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.21, Figure 279, printed pages 283, PDF pages 309

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 280: Boot Partition Log Page</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-280-CLAIM figure-table:BASEBTS-BASE-FIG-280 -->

**SPEC.** Figure 280, "Boot Partition Log Page": Header bytes are 0–15; BPINFO occupies 4–7 with ABPID at bit 31 and BPSZ at bits 14:0. BPD begins at byte 16 and is BPSZ×128 KiB long. Decode the source-specific fields below.

#### Where this Figure fits

Header bytes are 0–15; BPINFO occupies 4–7 with ABPID at bit 31 and BPSZ at bits 14:0. BPD begins at byte 16 and is BPSZ×128 KiB long.

The indexed fields below belong to this source document and this Figure. The worked example connects them to the full operation.

#### Teaching redraw

```text
[Locate source: LID]
          ↓
[Extract field: BPINFO] → [Apply encoding: ABPID]
                                      ↓
[Validate evidence: BPSZ]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `LID` | Log Page Identifier, the Get Log Page field selecting a log page. |
| `BPINFO` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `ABPID` | Active Boot Partition ID; identifies the partition selected as the boot image. |
| `BPSZ` | Boot Partition Size; each unit is 128 KiB. |
| `BPD` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Confirm NVME-BASE-2.4, §5.2.13.1.21, Figure 280; equal Figure numbers in different documents are different sources.
2. Apply the field/state rule above to the captured raw input.
3. First determine whether an Admin-command environment exists, then choose properties or LID 15h. Both access boot contents, but their return formats and observation points differ.
4. Compare the observation with the worked scenario and retain the cited source and target identity.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 280 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §5.2.13.1.21 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| Rule | Header bytes are 0–15; BPINFO occupies 4–7 with ABPID at bit 31 and BPSZ at bits 14:0. BPD begins at byte 16 and is BPSZ×128 KiB long. |
| Boundary | For an unfinished property read, inspect BRS and the buffer; reset is not an allowed normal completion step. BPINFO in LID 15h is a returned field and reading it does not modify the property of the same name. |

**Informative example.** With BPSZ=2, LID 15h contains 262144 bytes of boot data plus a 16-byte header, totaling 262160 bytes. Reading BP1 does not activate BP1, and a log read does not advance the property's BRS.

**Common misconception.** For an unfinished property read, inspect BRS and the buffer; reset is not an allowed normal completion step. BPINFO in LID 15h is a returned field and reading it does not modify the property of the same name.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Symptom / correction | For an unfinished property read, inspect BRS and the buffer; reset is not an allowed normal completion step. BPINFO in LID 15h is a returned field and reading it does not modify the property of the same name. |

#### Questions the reader should now answer

1. Which source-specific fields establish the decision?
2. Which capability, target, or state would change the worked result?

**Source field index:** LID, BPINFO, ABPID, BPSZ, BPD

**Source keyword index:** shall not, should not, shall, should, reserved

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.21, Figure 280, printed pages 284, PDF pages 310

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 312: Sanitize Status Log Page</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-312-CLAIM figure-table:BASEBTS-BASE-FIG-312 -->

**SPEC.** Figure 312, "Sanitize Status Log Page": The 512-byte log has SPROG[1:0], SSTAT[3:2], SCDW10[7:4], estimates[35:8], SSI[36], MNSOIP[43:40], and STNSID[47:44]. Select the target with NSID, then interpret SOS/SANS/FAILS and progress together. Decode the source-specific fields below.

#### Where this Figure fits

The 512-byte log has SPROG[1:0], SSTAT[3:2], SCDW10[7:4], estimates[35:8], SSI[36], MNSOIP[43:40], and STNSID[47:44]. Select the target with NSID, then interpret SOS/SANS/FAILS and progress together.

The indexed fields below belong to this source document and this Figure. The worked example connects them to the full operation.

#### Teaching redraw

```text
[Locate source: SPROG]
          ↓
[Extract field: SSTAT] → [Apply encoding: SCDW10]
                                      ↓
[Validate evidence: ETO]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `SPROG` | Sanitize Progress; raw/65536, indicating progress only for the currently measured phase. |
| `SSTAT` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `SCDW10` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `ETO` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `ETPVDS` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `SSI` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `MNSOIP` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `STNSID` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Confirm NVME-BASE-2.4, §5.2.13.1.38, Figure 312; equal Figure numbers in different documents are different sources.
2. Apply the field/state rule above to the captured raw input.
3. Start with the seven states in Figure 772 and attach transition conditions from Figures 773–779. Status describes results, state describes the current position, and events report transitions.
4. Compare the observation with the worked scenario and retain the cited source and target identity.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 312 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §5.2.13.1.38 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| Rule | The 512-byte log has SPROG[1:0], SSTAT[3:2], SCDW10[7:4], estimates[35:8], SSI[36], MNSOIP[43:40], and STNSID[47:44]. Select the target with NSID, then interpret SOS/SANS/FAILS and progress together. |
| Boundary | Preserve SCDW10, SOS, SANS, FAILS, MVCNCLD, and event timestamps. Recording only a completion event conflates success, failure, and entry into verification. |

**Informative example.** SPROG=8000h represents 50% of the currently measured phase. Media Verification uses SPROG=FFFFh while SOS can remain 010b; leaving verification for deallocation starts progress again at zero. This is not progress regression.

**Common misconception.** Preserve SCDW10, SOS, SANS, FAILS, MVCNCLD, and event timestamps. Recording only a completion event conflates success, failure, and entry into verification.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Symptom / correction | Preserve SCDW10, SOS, SANS, FAILS, MVCNCLD, and event timestamps. Recording only a completion event conflates success, failure, and entry into verification. |

#### Questions the reader should now answer

1. Which source-specific fields establish the decision?
2. Which capability, target, or state would change the worked result?

**Source field index:** SPROG, SSTAT, SCDW10, ETO, ETPVDS, SSI, MNSOIP, STNSID

**Source keyword index:** shall, reserved

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.38, Figure 312, printed pages 314-319, PDF pages 340-345

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 451: Sanitize - Command Dword 10</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-451-CLAIM figure-table:BASEBTS-BASE-FIG-451 -->

**SPEC.** Figure 451, "Sanitize - Command Dword 10": Select the action with SANACT before decoding method-dependent bits. OWPASS=0 means 16, and EMVS cannot combine with Overwrite/NDAS=1. PREQ bit 11 differs from the namespace command. Decode the source-specific fields below.

#### Where this Figure fits

Select the action with SANACT before decoding method-dependent bits. OWPASS=0 means 16, and EMVS cannot combine with Overwrite/NDAS=1. PREQ bit 11 differs from the namespace command.

The indexed fields below belong to this source document and this Figure. The worked example connects them to the full operation.

#### Teaching redraw

```text
[Locate source: SANACT]
          ↓
[Extract field: AUSE] → [Apply encoding: OWPASS]
                                      ↓
[Validate evidence: OIPBP]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `SANACT` | Sanitize Action; selects the method, Exit Failure Mode, or Exit Media Verification. |
| `AUSE` | Allow Unrestricted Sanitize Exit; selects whether failure can be exited without a successful retry. |
| `OWPASS` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `OIPBP` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `NDAS` | No-Deallocate After Sanitize; a command request interpreted with SANICAP.NDI and NODRM. |
| `EMVS` | Enter Media Verification State; requests verification after successful processing, subject to method and capability restrictions. |
| `PREQ` | Purge Request; interpreted with SPRRS for purge request/reporting; its bit position differs between the Sanitize commands. |

#### Read in this order

1. Confirm NVME-BASE-2.4, §5.2.26, Figure 451; equal Figure numbers in different documents are different sources.
2. Apply the field/state rule above to the captured raw input.
3. Separate advertised capabilities, command requests, and Feature policy. Command acceptance, operation success, and satisfaction of no-deallocate are three outcomes requiring different evidence.
4. Compare the observation with the worked scenario and retain the cited source and target identity.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 451 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §5.2.26 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| Rule | Select the action with SANACT before decoding method-dependent bits. OWPASS=0 means 16, and EMVS cannot combine with Overwrite/NDAS=1. PREQ bit 11 differs from the namespace command. |
| Boundary | PREQ is bit 4 in Figure 454 but bit 11 in Figure 451. Sharing an untyped builder between the two commands can set reserved bits in the namespace command. |

**Informative example.** SANACT=010b, AUSE=0, EMVS=1, NDAS=0, and PREQ=0 encode CDW10=0402h. It applies only with VERS/Block Erase support and other preconditions satisfied. Separately, OWPASS=0h means 16 passes, not skipping overwrite.

**Common misconception.** PREQ is bit 4 in Figure 454 but bit 11 in Figure 451. Sharing an untyped builder between the two commands can set reserved bits in the namespace command.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Symptom / correction | PREQ is bit 4 in Figure 454 but bit 11 in Figure 451. Sharing an untyped builder between the two commands can set reserved bits in the namespace command. |

#### Questions the reader should now answer

1. Which source-specific fields establish the decision?
2. Which capability, target, or state would change the worked result?

**Source field index:** SANACT, AUSE, OWPASS, OIPBP, NDAS, EMVS, PREQ

**Source keyword index:** shall not, should not, shall, should, reserved

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.26, Figure 451, printed pages 450-451, PDF pages 476-477

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 452: Sanitize - Command Dword 11</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-452-CLAIM figure-table:BASEBTS-BASE-FIG-452 -->

**SPEC.** Figure 452, "Sanitize - Command Dword 11": The 32-bit OVRPAT in CDW11 applies only to Overwrite. Combine it with OIPBP and pass parity to derive each pass's pattern. Decode the source-specific fields below.

#### Where this Figure fits

The 32-bit OVRPAT in CDW11 applies only to Overwrite. Combine it with OIPBP and pass parity to derive each pass's pattern.

The indexed fields below belong to this source document and this Figure. The worked example connects them to the full operation.

#### Teaching redraw

```text
[Locate source: OVRPAT]
          ↓
[Extract field: evidence] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `OVRPAT` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Confirm NVME-BASE-2.4, §5.2.26, Figure 452; equal Figure numbers in different documents are different sources.
2. Apply the field/state rule above to the captured raw input.
3. Separate advertised capabilities, command requests, and Feature policy. Command acceptance, operation success, and satisfaction of no-deallocate are three outcomes requiring different evidence.
4. Compare the observation with the worked scenario and retain the cited source and target identity.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 452 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §5.2.26 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| Rule | The 32-bit OVRPAT in CDW11 applies only to Overwrite. Combine it with OIPBP and pass parity to derive each pass's pattern. |
| Boundary | PREQ is bit 4 in Figure 454 but bit 11 in Figure 451. Sharing an untyped builder between the two commands can set reserved bits in the namespace command. |

**Informative example.** SANACT=010b, AUSE=0, EMVS=1, NDAS=0, and PREQ=0 encode CDW10=0402h. It applies only with VERS/Block Erase support and other preconditions satisfied. Separately, OWPASS=0h means 16 passes, not skipping overwrite.

**Common misconception.** PREQ is bit 4 in Figure 454 but bit 11 in Figure 451. Sharing an untyped builder between the two commands can set reserved bits in the namespace command.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Symptom / correction | PREQ is bit 4 in Figure 454 but bit 11 in Figure 451. Sharing an untyped builder between the two commands can set reserved bits in the namespace command. |

#### Questions the reader should now answer

1. Which source-specific fields establish the decision?
2. Which capability, target, or state would change the worked result?

**Source field index:** OVRPAT

**Source keyword index:** shall, reserved

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.26, Figure 452, printed pages 451, PDF pages 477

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 453: Sanitize - Command Specific Status Values</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-453-CLAIM figure-table:BASEBTS-BASE-FIG-453 -->

**SPEC.** Figure 453, "Sanitize - Command Specific Status Values": These are command-specific failures of the initiating command. Record them separately from later background-operation Sanitize Failed/SOS results. Decode the source-specific fields below.

#### Where this Figure fits

These are command-specific failures of the initiating command. Record them separately from later background-operation Sanitize Failed/SOS results.

The indexed fields below belong to this source document and this Figure. The worked example connects them to the full operation.

#### Teaching redraw

```text
[Locate source: Firmware Activation Requires Reset]
          ↓
[Extract field: PMR Enabled] → [Apply encoding: Controller Suspended]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `Firmware Activation Requires Reset` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `PMR Enabled` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `Controller Suspended` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Confirm NVME-BASE-2.4, §5.2.26, Figure 453; equal Figure numbers in different documents are different sources.
2. Apply the field/state rule above to the captured raw input.
3. Separate advertised capabilities, command requests, and Feature policy. Command acceptance, operation success, and satisfaction of no-deallocate are three outcomes requiring different evidence.
4. Compare the observation with the worked scenario and retain the cited source and target identity.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 453 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §5.2.26 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| Rule | These are command-specific failures of the initiating command. Record them separately from later background-operation Sanitize Failed/SOS results. |
| Boundary | PREQ is bit 4 in Figure 454 but bit 11 in Figure 451. Sharing an untyped builder between the two commands can set reserved bits in the namespace command. |

**Informative example.** SANACT=010b, AUSE=0, EMVS=1, NDAS=0, and PREQ=0 encode CDW10=0402h. It applies only with VERS/Block Erase support and other preconditions satisfied. Separately, OWPASS=0h means 16 passes, not skipping overwrite.

**Common misconception.** PREQ is bit 4 in Figure 454 but bit 11 in Figure 451. Sharing an untyped builder between the two commands can set reserved bits in the namespace command.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Symptom / correction | PREQ is bit 4 in Figure 454 but bit 11 in Figure 451. Sharing an untyped builder between the two commands can set reserved bits in the namespace command. |

#### Questions the reader should now answer

1. Which source-specific fields establish the decision?
2. Which capability, target, or state would change the worked result?

**Source field index:** Firmware Activation Requires Reset, PMR Enabled, Controller Suspended

**Source keyword index:** shall, reserved

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.26, Figure 453, printed pages 451, PDF pages 477

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 492: Sanitize Config - Command Dword 11</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-492-CLAIM figure-table:BASEBTS-BASE-FIG-492 -->

**SPEC.** Figure 492, "Sanitize Config - Command Dword 11": FID 17h CDW11 bit 0 is NODRM. It selects error/warning response when NDI=1 and command NDAS=1; it is not a switch required for every sanitize. Decode the source-specific fields below.

#### Where this Figure fits

FID 17h CDW11 bit 0 is NODRM. It selects error/warning response when NDI=1 and command NDAS=1; it is not a switch required for every sanitize.

The indexed fields below belong to this source document and this Figure. The worked example connects them to the full operation.

#### Teaching redraw

```text
[Locate source: NODRM]
          ↓
[Extract field: evidence] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `NODRM` | No-Deallocate Response Mode; FID 17h bit zero selects error or warning for inhibited NDAS. |

#### Read in this order

1. Confirm NVME-BASE-2.4, §5.2.30.1.16, Figure 492; equal Figure numbers in different documents are different sources.
2. Apply the field/state rule above to the captured raw input.
3. Separate advertised capabilities, command requests, and Feature policy. Command acceptance, operation success, and satisfaction of no-deallocate are three outcomes requiring different evidence.
4. Compare the observation with the worked scenario and retain the cited source and target identity.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 492 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §5.2.30.1.16 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| Rule | FID 17h CDW11 bit 0 is NODRM. It selects error/warning response when NDI=1 and command NDAS=1; it is not a switch required for every sanitize. |
| Boundary | PREQ is bit 4 in Figure 454 but bit 11 in Figure 451. Sharing an untyped builder between the two commands can set reserved bits in the namespace command. |

**Informative example.** SANACT=010b, AUSE=0, EMVS=1, NDAS=0, and PREQ=0 encode CDW10=0402h. It applies only with VERS/Block Erase support and other preconditions satisfied. Separately, OWPASS=0h means 16 passes, not skipping overwrite.

**Common misconception.** PREQ is bit 4 in Figure 454 but bit 11 in Figure 451. Sharing an untyped builder between the two commands can set reserved bits in the namespace command.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Symptom / correction | PREQ is bit 4 in Figure 454 but bit 11 in Figure 451. Sharing an untyped builder between the two commands can set reserved bits in the namespace command. |

#### Questions the reader should now answer

1. Which source-specific fields establish the decision?
2. Which capability, target, or state would change the worked result?

**Source field index:** NODRM

**Source keyword index:** shall, may, reserved

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.16, Figure 492, printed pages 477-478, PDF pages 503-504

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 542: Boot Partition Write Protection Config - Command Dword 11</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-542-CLAIM figure-table:BASEBTS-BASE-FIG-542 -->

**SPEC.** Figure 542, "Boot Partition Write Protection Config - Command Dword 11": The two three-bit state fields are set independently. 000b only requests no change in Set; Get returns actual state and uses 100b only to report RPMB ownership. Decode the source-specific fields below.

#### Where this Figure fits

The two three-bit state fields are set independently. 000b only requests no change in Set; Get returns actual state and uses 100b only to report RPMB ownership.

The indexed fields below belong to this source document and this Figure. The worked example connects them to the full operation.

#### Teaching redraw

```text
[Locate source: BP0WPS]
          ↓
[Extract field: BP1WPS] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `BP0WPS` | Boot Partition 0 Write Protection State; bits 2:0 of FID 85h. |
| `BP1WPS` | Boot Partition 1 Write Protection State; bits 5:3 of FID 85h. |

#### Read in this order

1. Confirm NVME-BASE-2.4, §5.2.30.1.39, Figure 542; equal Figure numbers in different documents are different sources.
2. Apply the field/state rule above to the captured raw input.
3. Track image transfer, partition contents, active selection, and write protection separately. Successful download has not yet written a Boot Partition, and a successful write has not automatically activated it.
4. Compare the observation with the worked scenario and retain the cited source and target identity.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 542 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §5.2.30.1.39 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| Rule | The two three-bit state fields are set independently. 000b only requests no change in Set; Get returns actual state and uses 100b only to report RPMB ownership. |
| Boundary | The same reset test has different expected results for the two mechanisms. Preserve the power-cycle/reset type so that relocking can be classified as expected behavior or a defect. |

**Informative example.** To leave BP0 unchanged and unlock BP1, FID 85h CDW11 is (001b << 3) | 000b = 08h. A subsequent Get does not return 000b for BP0; it returns its actual state, or 100b when RPMB owns protection.

**Common misconception.** The same reset test has different expected results for the two mechanisms. Preserve the power-cycle/reset type so that relocking can be classified as expected behavior or a defect.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Symptom / correction | The same reset test has different expected results for the two mechanisms. Preserve the power-cycle/reset type so that relocking can be classified as expected behavior or a defect. |

#### Questions the reader should now answer

1. Which source-specific fields establish the decision?
2. Which capability, target, or state would change the worked result?

**Source field index:** BP0WPS, BP1WPS

**Source keyword index:** shall not, shall, should, may, reserved

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.39, Figure 542, printed pages 513-514, PDF pages 539-540

</details>

<a id="section-8-1"></a>

### §8.1

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 679: Boot Partition Overview</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-679-CLAIM figure-table:BASEBTS-BASE-FIG-679 -->

**SPEC.** Figure 679, "Boot Partition Overview": Separate the two equal Boot Partitions from this read's host buffer. Active ID selects the boot image, not a restriction to reading only the active partition. Decode the source-specific fields below.

#### Where this Figure fits

Separate the two equal Boot Partitions from this read's host buffer. Active ID selects the boot image, not a restriction to reading only the active partition.

The indexed fields below belong to this source document and this Figure. The worked example connects them to the full operation.

#### Teaching redraw

```text
[Locate source: Boot Partition 0]
          ↓
[Extract field: Boot Partition 1] → [Apply encoding: Host Memory Buffer]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `Boot Partition 0` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `Boot Partition 1` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `Host Memory Buffer` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Confirm NVME-BASE-2.4, §8.1.3.1, Figure 679; equal Figure numbers in different documents are different sources.
2. Apply the field/state rule above to the captured raw input.
3. First determine whether an Admin-command environment exists, then choose properties or LID 15h. Both access boot contents, but their return formats and observation points differ.
4. Compare the observation with the worked scenario and retain the cited source and target identity.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 679 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §8.1.3.1 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| Rule | Separate the two equal Boot Partitions from this read's host buffer. Active ID selects the boot image, not a restriction to reading only the active partition. |
| Boundary | For an unfinished property read, inspect BRS and the buffer; reset is not an allowed normal completion step. BPINFO in LID 15h is a returned field and reading it does not modify the property of the same name. |

**Informative example.** With BPSZ=2, LID 15h contains 262144 bytes of boot data plus a 16-byte header, totaling 262160 bytes. Reading BP1 does not activate BP1, and a log read does not advance the property's BRS.

**Common misconception.** For an unfinished property read, inspect BRS and the buffer; reset is not an allowed normal completion step. BPINFO in LID 15h is a returned field and reading it does not modify the property of the same name.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Symptom / correction | For an unfinished property read, inspect BRS and the buffer; reset is not an allowed normal completion step. BPINFO in LID 15h is a returned field and reading it does not modify the property of the same name. |

#### Questions the reader should now answer

1. Which source-specific fields establish the decision?
2. Which capability, target, or state would change the worked result?

**Source field index:** Boot Partition 0, Boot Partition 1, Host Memory Buffer

**Source keyword index:** shall not, shall, should, may

> Source: NVME-BASE-2.4, Rev. 2.4, §8.1.3.1, Figure 679, printed pages 587, PDF pages 613

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 680: Set Features Boot Partition Write Protection State Machine Model</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-680-CLAIM figure-table:BASEBTS-BASE-FIG-680 -->

**SPEC.** Figure 680, "Set Features Boot Partition Write Protection State Machine Model": Set Features switches unlocked/locked and can move either to locked-until-power-cycle; a power cycle returns to locked. There is no ordinary Set-unlock edge from locked-until-power-cycle. Decode the source-specific fields below.

#### Where this Figure fits

Set Features switches unlocked/locked and can move either to locked-until-power-cycle; a power cycle returns to locked. There is no ordinary Set-unlock edge from locked-until-power-cycle.

The indexed fields below belong to this source document and this Figure. The worked example connects them to the full operation.

#### Teaching redraw

```text
[Locate source: Write Unlocked]
          ↓
[Extract field: Write Locked] → [Apply encoding: Write Locked Until Power Cycle]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `Write Unlocked` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `Write Locked` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `Write Locked Until Power Cycle` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Confirm NVME-BASE-2.4, §8.1.3.3.1, Figure 680; equal Figure numbers in different documents are different sources.
2. Apply the field/state rule above to the captured raw input.
3. Track image transfer, partition contents, active selection, and write protection separately. Successful download has not yet written a Boot Partition, and a successful write has not automatically activated it.
4. Compare the observation with the worked scenario and retain the cited source and target identity.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 680 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §8.1.3.3.1 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| Rule | Set Features switches unlocked/locked and can move either to locked-until-power-cycle; a power cycle returns to locked. There is no ordinary Set-unlock edge from locked-until-power-cycle. |
| Boundary | The same reset test has different expected results for the two mechanisms. Preserve the power-cycle/reset type so that relocking can be classified as expected behavior or a defect. |

**Informative example.** To leave BP0 unchanged and unlock BP1, FID 85h CDW11 is (001b << 3) | 000b = 08h. A subsequent Get does not return 000b for BP0; it returns its actual state, or 100b when RPMB owns protection.

**Common misconception.** The same reset test has different expected results for the two mechanisms. Preserve the power-cycle/reset type so that relocking can be classified as expected behavior or a defect.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Symptom / correction | The same reset test has different expected results for the two mechanisms. Preserve the power-cycle/reset type so that relocking can be classified as expected behavior or a defect. |

#### Questions the reader should now answer

1. Which source-specific fields establish the decision?
2. Which capability, target, or state would change the worked result?

**Source field index:** Write Unlocked, Write Locked, Write Locked Until Power Cycle

**Source keyword index:** shall

> Source: NVME-BASE-2.4, Rev. 2.4, §8.1.3.3.1, Figure 680, printed pages 589, PDF pages 615

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 681: Set Features Boot Partition Write Protection State Definitions</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-681-CLAIM figure-table:BASEBTS-BASE-FIG-681 -->

**SPEC.** Figure 681, "Set Features Boot Partition Write Protection State Definitions": Compare all three states: controller reset preserves them, while power cycle changes unlocked and until-power-cycle to locked. Decode the source-specific fields below.

#### Where this Figure fits

Compare all three states: controller reset preserves them, while power cycle changes unlocked and until-power-cycle to locked.

The indexed fields below belong to this source document and this Figure. The worked example connects them to the full operation.

#### Teaching redraw

```text
[Locate source: Power Cycles]
          ↓
[Extract field: Controller Level Resets] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `Power Cycles` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `Controller Level Resets` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Confirm NVME-BASE-2.4, §8.1.3.3.1, Figure 681; equal Figure numbers in different documents are different sources.
2. Apply the field/state rule above to the captured raw input.
3. Track image transfer, partition contents, active selection, and write protection separately. Successful download has not yet written a Boot Partition, and a successful write has not automatically activated it.
4. Compare the observation with the worked scenario and retain the cited source and target identity.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 681 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §8.1.3.3.1 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| Rule | Compare all three states: controller reset preserves them, while power cycle changes unlocked and until-power-cycle to locked. |
| Boundary | The same reset test has different expected results for the two mechanisms. Preserve the power-cycle/reset type so that relocking can be classified as expected behavior or a defect. |

**Informative example.** To leave BP0 unchanged and unlock BP1, FID 85h CDW11 is (001b << 3) | 000b = 08h. A subsequent Get does not return 000b for BP0; it returns its actual state, or 100b when RPMB owns protection.

**Common misconception.** The same reset test has different expected results for the two mechanisms. Preserve the power-cycle/reset type so that relocking can be classified as expected behavior or a defect.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Symptom / correction | The same reset test has different expected results for the two mechanisms. Preserve the power-cycle/reset type so that relocking can be classified as expected behavior or a defect. |

#### Questions the reader should now answer

1. Which source-specific fields establish the decision?
2. Which capability, target, or state would change the worked result?

**Source field index:** Power Cycles, Controller Level Resets

**Source keyword index:** may

> Source: NVME-BASE-2.4, Rev. 2.4, §8.1.3.3.1, Figure 681, printed pages 590, PDF pages 616

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 682: RPMB Boot Partition Write Protection State Machine Model</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-682-CLAIM figure-table:BASEBTS-BASE-FIG-682 -->

**SPEC.** Figure 682, "RPMB Boot Partition Write Protection State Machine Model": Before and after RPMB enablement are different regions; once enabled, authenticated configuration writes unlock/lock and resets return to locked. Decode the source-specific fields below.

#### Where this Figure fits

Before and after RPMB enablement are different regions; once enabled, authenticated configuration writes unlock/lock and resets return to locked.

The indexed fields below belong to this source document and this Figure. The worked example connects them to the full operation.

#### Teaching redraw

```text
[Locate source: RPMB Disabled]
          ↓
[Extract field: RPMB Enabled] → [Apply encoding: Write Locked]
                                      ↓
[Validate evidence: Write Unlocked]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `RPMB Disabled` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `RPMB Enabled` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `Write Locked` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `Write Unlocked` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Confirm NVME-BASE-2.4, §8.1.3.3.2, Figure 682; equal Figure numbers in different documents are different sources.
2. Apply the field/state rule above to the captured raw input.
3. Track image transfer, partition contents, active selection, and write protection separately. Successful download has not yet written a Boot Partition, and a successful write has not automatically activated it.
4. Compare the observation with the worked scenario and retain the cited source and target identity.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 682 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §8.1.3.3.2 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| Rule | Before and after RPMB enablement are different regions; once enabled, authenticated configuration writes unlock/lock and resets return to locked. |
| Boundary | The same reset test has different expected results for the two mechanisms. Preserve the power-cycle/reset type so that relocking can be classified as expected behavior or a defect. |

**Informative example.** To leave BP0 unchanged and unlock BP1, FID 85h CDW11 is (001b << 3) | 000b = 08h. A subsequent Get does not return 000b for BP0; it returns its actual state, or 100b when RPMB owns protection.

**Common misconception.** The same reset test has different expected results for the two mechanisms. Preserve the power-cycle/reset type so that relocking can be classified as expected behavior or a defect.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Symptom / correction | The same reset test has different expected results for the two mechanisms. Preserve the power-cycle/reset type so that relocking can be classified as expected behavior or a defect. |

#### Questions the reader should now answer

1. Which source-specific fields establish the decision?
2. Which capability, target, or state would change the worked result?

**Source field index:** RPMB Disabled, RPMB Enabled, Write Locked, Write Unlocked

**Source keyword index:** shall

> Source: NVME-BASE-2.4, Rev. 2.4, §8.1.3.3.2, Figure 682, printed pages 591, PDF pages 617

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 683: RPMB Boot Partition Write Protection State Definitions</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-683-CLAIM figure-table:BASEBTS-BASE-FIG-683 -->

**SPEC.** Figure 683, "RPMB Boot Partition Write Protection State Definitions": For RPMB-only protection before enablement, unlocked can persist; once enabled, unlocked does not survive reset/power cycle. Dual-mechanism support also requires Figure 684's defaults and ownership rules. Decode the source-specific fields below.

#### Where this Figure fits

For RPMB-only protection before enablement, unlocked can persist; once enabled, unlocked does not survive reset/power cycle. Dual-mechanism support also requires Figure 684's defaults and ownership rules.

The indexed fields below belong to this source document and this Figure. The worked example connects them to the full operation.

#### Teaching redraw

```text
[Locate source: RPMB Protection Enabled]
          ↓
[Extract field: Persistence] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `RPMB Protection Enabled` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `Persistence` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Confirm NVME-BASE-2.4, §8.1.3.3.2, Figure 683; equal Figure numbers in different documents are different sources.
2. Apply the field/state rule above to the captured raw input.
3. Track image transfer, partition contents, active selection, and write protection separately. Successful download has not yet written a Boot Partition, and a successful write has not automatically activated it.
4. Compare the observation with the worked scenario and retain the cited source and target identity.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 683 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §8.1.3.3.2 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| Rule | For RPMB-only protection before enablement, unlocked can persist; once enabled, unlocked does not survive reset/power cycle. Dual-mechanism support also requires Figure 684's defaults and ownership rules. |
| Boundary | The same reset test has different expected results for the two mechanisms. Preserve the power-cycle/reset type so that relocking can be classified as expected behavior or a defect. |

**Informative example.** To leave BP0 unchanged and unlock BP1, FID 85h CDW11 is (001b << 3) | 000b = 08h. A subsequent Get does not return 000b for BP0; it returns its actual state, or 100b when RPMB owns protection.

**Common misconception.** The same reset test has different expected results for the two mechanisms. Preserve the power-cycle/reset type so that relocking can be classified as expected behavior or a defect.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Symptom / correction | The same reset test has different expected results for the two mechanisms. Preserve the power-cycle/reset type so that relocking can be classified as expected behavior or a defect. |

#### Questions the reader should now answer

1. Which source-specific fields establish the decision?
2. Which capability, target, or state would change the worked result?

**Source field index:** RPMB Protection Enabled, Persistence

**Source keyword index:** shall

> Source: NVME-BASE-2.4, Rev. 2.4, §8.1.3.3.2, Figure 683, printed pages 591, PDF pages 617

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 684: Boot Partition Write Protection State Machine Model</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-684-CLAIM figure-table:BASEBTS-BASE-FIG-684 -->

**SPEC.** Figure 684, "Boot Partition Write Protection State Machine Model": Track states in the Set Features region, then transfer through the enable gate to RPMB; until-power-cycle cannot be bypassed through RPMB enablement. Decode the source-specific fields below.

#### Where this Figure fits

Track states in the Set Features region, then transfer through the enable gate to RPMB; until-power-cycle cannot be bypassed through RPMB enablement.

The indexed fields below belong to this source document and this Figure. The worked example connects them to the full operation.

#### Teaching redraw

```text
[Locate source: Set Features Owner]
          ↓
[Extract field: RPMB Owner] → [Apply encoding: Enable Gate]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `Set Features Owner` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `RPMB Owner` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `Enable Gate` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Confirm NVME-BASE-2.4, §8.1.3.3.3, Figure 684; equal Figure numbers in different documents are different sources.
2. Apply the field/state rule above to the captured raw input.
3. Track image transfer, partition contents, active selection, and write protection separately. Successful download has not yet written a Boot Partition, and a successful write has not automatically activated it.
4. Compare the observation with the worked scenario and retain the cited source and target identity.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 684 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §8.1.3.3.3 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| Rule | Track states in the Set Features region, then transfer through the enable gate to RPMB; until-power-cycle cannot be bypassed through RPMB enablement. |
| Boundary | The same reset test has different expected results for the two mechanisms. Preserve the power-cycle/reset type so that relocking can be classified as expected behavior or a defect. |

**Informative example.** To leave BP0 unchanged and unlock BP1, FID 85h CDW11 is (001b << 3) | 000b = 08h. A subsequent Get does not return 000b for BP0; it returns its actual state, or 100b when RPMB owns protection.

**Common misconception.** The same reset test has different expected results for the two mechanisms. Preserve the power-cycle/reset type so that relocking can be classified as expected behavior or a defect.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Symptom / correction | The same reset test has different expected results for the two mechanisms. Preserve the power-cycle/reset type so that relocking can be classified as expected behavior or a defect. |

#### Questions the reader should now answer

1. Which source-specific fields establish the decision?
2. Which capability, target, or state would change the worked result?

**Source field index:** Set Features Owner, RPMB Owner, Enable Gate

**Source keyword index:** none

> Source: NVME-BASE-2.4, Rev. 2.4, §8.1.3.3.3, Figure 684, printed pages 593, PDF pages 619

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 770: Sanitization Operation Scope Based on Sanitize Operation</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-770-CLAIM figure-table:BASEBTS-BASE-FIG-770 -->

**SPEC.** Figure 770, "Sanitization Operation Scope Based on Sanitize Operation": Evaluate both targets for each data class: Boot/RPMB stay unchanged, user-data locations are processed, and CMB/PMR/PDA differences cannot be summarized as all namespaces. Decode the source-specific fields below.

#### Where this Figure fits

Evaluate both targets for each data class: Boot/RPMB stay unchanged, user-data locations are processed, and CMB/PMR/PDA differences cannot be summarized as all namespaces.

The indexed fields below belong to this source document and this Figure. The worked example connects them to the full operation.

#### Teaching redraw

```text
[Locate source: Subsystem Target]
          ↓
[Extract field: Namespace Target] → [Apply encoding: User Data]
                                      ↓
[Validate evidence: Boot Partition]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `Subsystem Target` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `Namespace Target` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `User Data` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `Boot Partition` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `CMB` | Controller Memory Buffer, controller-provided memory in which selected queues or data structures may reside. |
| `PMR` | Persistent Memory Region, a controller-exposed memory region with persistence semantics. |

#### Read in this order

1. Confirm NVME-BASE-2.4, §8.1.27, Figure 770; equal Figure numbers in different documents are different sources.
2. Apply the field/state rule above to the captured raw input.
3. Sanitize scope is not simply everything on a disk. Classify the target, data provenance, and whether it can contain user data; this also establishes its relationship with Boot and diagnostics.
4. Compare the observation with the worked scenario and retain the cited source and target identity.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 770 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §8.1.27 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| Rule | Evaluate both targets for each data class: Boot/RPMB stay unchanged, user-data locations are processed, and CMB/PMR/PDA differences cannot be summarized as all namespaces. |
| Boundary | Using zero-filled reads as the only success criterion misclassifies results. Establish the method, allocation state, and verification state before applying NVM Command Set result definitions. |

**Informative example.** Even after every namespace is sanitized, that fact does not prove subsystem-level data such as CMB has undergone subsystem sanitization. Conversely, successful subsystem sanitize does not update or erase the boot image in a Boot Partition.

**Common misconception.** Using zero-filled reads as the only success criterion misclassifies results. Establish the method, allocation state, and verification state before applying NVM Command Set result definitions.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Symptom / correction | Using zero-filled reads as the only success criterion misclassifies results. Establish the method, allocation state, and verification state before applying NVM Command Set result definitions. |

#### Questions the reader should now answer

1. Which source-specific fields establish the decision?
2. Which capability, target, or state would change the worked result?

**Source field index:** Subsystem Target, Namespace Target, User Data, Boot Partition, CMB, PMR

**Source keyword index:** shall not, shall, may, optional

> Source: NVME-BASE-2.4, Rev. 2.4, §8.1.27, Figure 770, printed pages 711-712, PDF pages 737-738

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 771: Sanitize Operations - Overwrite Mechanism</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-771-CLAIM figure-table:BASEBTS-BASE-FIG-771 -->

**SPEC.** Figure 771, "Sanitize Operations - Overwrite Mechanism": Use total-pass parity to determine whether the first pass is inverted, then invert between passes; PI bytes follow FFh/00h rules too. OVRPAT alone is insufficient. Decode the source-specific fields below.

#### Where this Figure fits

Use total-pass parity to determine whether the first pass is inverted, then invert between passes; PI bytes follow FFh/00h rules too. OVRPAT alone is insufficient.

The indexed fields below belong to this source document and this Figure. The worked example connects them to the full operation.

#### Teaching redraw

```text
[Locate source: OIPBP]
          ↓
[Extract field: OWPASS] → [Apply encoding: OVRPAT]
                                      ↓
[Validate evidence: PI]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `OIPBP` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `OWPASS` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `OVRPAT` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `PI` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Confirm NVME-BASE-2.4, §8.1.27.3, Figure 771; equal Figure numbers in different documents are different sources.
2. Apply the field/state rule above to the captured raw input.
3. Separate advertised capabilities, command requests, and Feature policy. Command acceptance, operation success, and satisfaction of no-deallocate are three outcomes requiring different evidence.
4. Compare the observation with the worked scenario and retain the cited source and target identity.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 771 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §8.1.27.3 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| Rule | Use total-pass parity to determine whether the first pass is inverted, then invert between passes; PI bytes follow FFh/00h rules too. OVRPAT alone is insufficient. |
| Boundary | PREQ is bit 4 in Figure 454 but bit 11 in Figure 451. Sharing an untyped builder between the two commands can set reserved bits in the namespace command. |

**Informative example.** SANACT=010b, AUSE=0, EMVS=1, NDAS=0, and PREQ=0 encode CDW10=0402h. It applies only with VERS/Block Erase support and other preconditions satisfied. Separately, OWPASS=0h means 16 passes, not skipping overwrite.

**Common misconception.** PREQ is bit 4 in Figure 454 but bit 11 in Figure 451. Sharing an untyped builder between the two commands can set reserved bits in the namespace command.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Symptom / correction | PREQ is bit 4 in Figure 454 but bit 11 in Figure 451. Sharing an untyped builder between the two commands can set reserved bits in the namespace command. |

#### Questions the reader should now answer

1. Which source-specific fields establish the decision?
2. Which capability, target, or state would change the worked result?

**Source field index:** OIPBP, OWPASS, OVRPAT, PI

**Source keyword index:** shall, may

> Source: NVME-BASE-2.4, Rev. 2.4, §8.1.27.3, Figure 771, printed pages 717, PDF pages 743

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 772: Sanitize Operation State Machine</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-772-CLAIM figure-table:BASEBTS-BASE-FIG-772 -->

**SPEC.** Figure 772, "Sanitize Operation State Machine": Seven states split into processing/failure paths through AUSE, use EMVS to reach verification, then return through deallocation. Interpret each edge with Figures 773–779. Decode the source-specific fields below.

#### Where this Figure fits

Seven states split into processing/failure paths through AUSE, use EMVS to reach verification, then return through deallocation. Interpret each edge with Figures 773–779.

The indexed fields below belong to this source document and this Figure. The worked example connects them to the full operation.

#### Teaching redraw

```text
[Locate source: Idle]
          ↓
[Extract field: Restricted Processing] → [Apply encoding: Restricted Failure]
                                      ↓
[Validate evidence: Unrestricted Processing]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `Idle` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `Restricted Processing` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `Restricted Failure` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `Unrestricted Processing` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `Unrestricted Failure` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `Media Verification` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `Post-Verification Deallocation` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Confirm NVME-BASE-2.4, §8.1.27.4, Figure 772; equal Figure numbers in different documents are different sources.
2. Apply the field/state rule above to the captured raw input.
3. Start with the seven states in Figure 772 and attach transition conditions from Figures 773–779. Status describes results, state describes the current position, and events report transitions.
4. Compare the observation with the worked scenario and retain the cited source and target identity.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 772 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §8.1.27.4 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| Rule | Seven states split into processing/failure paths through AUSE, use EMVS to reach verification, then return through deallocation. Interpret each edge with Figures 773–779. |
| Boundary | Preserve SCDW10, SOS, SANS, FAILS, MVCNCLD, and event timestamps. Recording only a completion event conflates success, failure, and entry into verification. |

**Informative example.** SPROG=8000h represents 50% of the currently measured phase. Media Verification uses SPROG=FFFFh while SOS can remain 010b; leaving verification for deallocation starts progress again at zero. This is not progress regression.

**Common misconception.** Preserve SCDW10, SOS, SANS, FAILS, MVCNCLD, and event timestamps. Recording only a completion event conflates success, failure, and entry into verification.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Symptom / correction | Preserve SCDW10, SOS, SANS, FAILS, MVCNCLD, and event timestamps. Recording only a completion event conflates success, failure, and entry into verification. |

#### Questions the reader should now answer

1. Which source-specific fields establish the decision?
2. Which capability, target, or state would change the worked result?

**Source field index:** Idle, Restricted Processing, Restricted Failure, Unrestricted Processing, Unrestricted Failure, Media Verification, Post-Verification Deallocation

**Source keyword index:** shall

> Source: NVME-BASE-2.4, Rev. 2.4, §8.1.27.4, Figure 772, printed pages 720, PDF pages 746

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 773: Idle State Transition Conditions</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-773-CLAIM figure-table:BASEBTS-BASE-FIG-773 -->

**SPEC.** Figure 773, "Idle State Transition Conditions": A1/B1 leave Idle for Restricted/Unrestricted Processing respectively. Entry clears SPROG and MVCNCLD; it does not mean the operation is complete. Decode the source-specific fields below.

#### Where this Figure fits

A1/B1 leave Idle for Restricted/Unrestricted Processing respectively. Entry clears SPROG and MVCNCLD; it does not mean the operation is complete.

The indexed fields below belong to this source document and this Figure. The worked example connects them to the full operation.

#### Teaching redraw

```text
[Locate source: A1]
          ↓
[Extract field: AUSE=0] → [Apply encoding: B1]
                                      ↓
[Validate evidence: AUSE=1]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `A1` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `AUSE=0` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `B1` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `AUSE=1` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Confirm NVME-BASE-2.4, §8.1.27.4.1, Figure 773; equal Figure numbers in different documents are different sources.
2. Apply the field/state rule above to the captured raw input.
3. Start with the seven states in Figure 772 and attach transition conditions from Figures 773–779. Status describes results, state describes the current position, and events report transitions.
4. Compare the observation with the worked scenario and retain the cited source and target identity.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 773 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §8.1.27.4.1 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| Rule | A1/B1 leave Idle for Restricted/Unrestricted Processing respectively. Entry clears SPROG and MVCNCLD; it does not mean the operation is complete. |
| Boundary | Preserve SCDW10, SOS, SANS, FAILS, MVCNCLD, and event timestamps. Recording only a completion event conflates success, failure, and entry into verification. |

**Informative example.** SPROG=8000h represents 50% of the currently measured phase. Media Verification uses SPROG=FFFFh while SOS can remain 010b; leaving verification for deallocation starts progress again at zero. This is not progress regression.

**Common misconception.** Preserve SCDW10, SOS, SANS, FAILS, MVCNCLD, and event timestamps. Recording only a completion event conflates success, failure, and entry into verification.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Symptom / correction | Preserve SCDW10, SOS, SANS, FAILS, MVCNCLD, and event timestamps. Recording only a completion event conflates success, failure, and entry into verification. |

#### Questions the reader should now answer

1. Which source-specific fields establish the decision?
2. Which capability, target, or state would change the worked result?

**Source field index:** A1, AUSE=0, B1, AUSE=1

**Source keyword index:** shall not, shall, should

> Source: NVME-BASE-2.4, Rev. 2.4, §8.1.27.4.1, Figure 773, printed pages 721, PDF pages 747

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 774: Restricted Processing State Transition Conditions</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-774-CLAIM figure-table:BASEBTS-BASE-FIG-774 -->

**SPEC.** Figure 774, "Restricted Processing State Transition Conditions": Restricted Processing succeeds through C1 to Idle or F1 to Verification depending on EMVS/MVCNCLD; D1 reports processing failure. Decode the source-specific fields below.

#### Where this Figure fits

Restricted Processing succeeds through C1 to Idle or F1 to Verification depending on EMVS/MVCNCLD; D1 reports processing failure.

The indexed fields below belong to this source document and this Figure. The worked example connects them to the full operation.

#### Teaching redraw

```text
[Locate source: C1]
          ↓
[Extract field: D1] → [Apply encoding: F1]
                                      ↓
[Validate evidence: EMVS]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `C1` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `D1` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `F1` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `EMVS` | Enter Media Verification State; requests verification after successful processing, subject to method and capability restrictions. |
| `MVCNCLD` | Media Verification Canceled; records canceled verification and affects the transition after processing. |

#### Read in this order

1. Confirm NVME-BASE-2.4, §8.1.27.4.2, Figure 774; equal Figure numbers in different documents are different sources.
2. Apply the field/state rule above to the captured raw input.
3. Start with the seven states in Figure 772 and attach transition conditions from Figures 773–779. Status describes results, state describes the current position, and events report transitions.
4. Compare the observation with the worked scenario and retain the cited source and target identity.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 774 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §8.1.27.4.2 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| Rule | Restricted Processing succeeds through C1 to Idle or F1 to Verification depending on EMVS/MVCNCLD; D1 reports processing failure. |
| Boundary | Preserve SCDW10, SOS, SANS, FAILS, MVCNCLD, and event timestamps. Recording only a completion event conflates success, failure, and entry into verification. |

**Informative example.** SPROG=8000h represents 50% of the currently measured phase. Media Verification uses SPROG=FFFFh while SOS can remain 010b; leaving verification for deallocation starts progress again at zero. This is not progress regression.

**Common misconception.** Preserve SCDW10, SOS, SANS, FAILS, MVCNCLD, and event timestamps. Recording only a completion event conflates success, failure, and entry into verification.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Symptom / correction | Preserve SCDW10, SOS, SANS, FAILS, MVCNCLD, and event timestamps. Recording only a completion event conflates success, failure, and entry into verification. |

#### Questions the reader should now answer

1. Which source-specific fields establish the decision?
2. Which capability, target, or state would change the worked result?

**Source field index:** C1, D1, F1, EMVS, MVCNCLD

**Source keyword index:** shall

> Source: NVME-BASE-2.4, Rev. 2.4, §8.1.27.4.2, Figure 774, printed pages 722, PDF pages 748

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 775: Restricted Failure State Transition Conditions</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-775-CLAIM figure-table:BASEBTS-BASE-FIG-775 -->

**SPEC.** Figure 775, "Restricted Failure State Transition Conditions": Restricted Failure recovers through A2 into Restricted Processing; Exit Failure Mode and AUSE=1 cannot substitute for a successful restricted retry. Decode the source-specific fields below.

#### Where this Figure fits

Restricted Failure recovers through A2 into Restricted Processing; Exit Failure Mode and AUSE=1 cannot substitute for a successful restricted retry.

The indexed fields below belong to this source document and this Figure. The worked example connects them to the full operation.

#### Teaching redraw

```text
[Locate source: A2]
          ↓
[Extract field: Restricted Retry] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `A2` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `Restricted Retry` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Confirm NVME-BASE-2.4, §8.1.27.4.3, Figure 775; equal Figure numbers in different documents are different sources.
2. Apply the field/state rule above to the captured raw input.
3. Start with the seven states in Figure 772 and attach transition conditions from Figures 773–779. Status describes results, state describes the current position, and events report transitions.
4. Compare the observation with the worked scenario and retain the cited source and target identity.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 775 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §8.1.27.4.3 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| Rule | Restricted Failure recovers through A2 into Restricted Processing; Exit Failure Mode and AUSE=1 cannot substitute for a successful restricted retry. |
| Boundary | Preserve SCDW10, SOS, SANS, FAILS, MVCNCLD, and event timestamps. Recording only a completion event conflates success, failure, and entry into verification. |

**Informative example.** SPROG=8000h represents 50% of the currently measured phase. Media Verification uses SPROG=FFFFh while SOS can remain 010b; leaving verification for deallocation starts progress again at zero. This is not progress regression.

**Common misconception.** Preserve SCDW10, SOS, SANS, FAILS, MVCNCLD, and event timestamps. Recording only a completion event conflates success, failure, and entry into verification.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Symptom / correction | Preserve SCDW10, SOS, SANS, FAILS, MVCNCLD, and event timestamps. Recording only a completion event conflates success, failure, and entry into verification. |

#### Questions the reader should now answer

1. Which source-specific fields establish the decision?
2. Which capability, target, or state would change the worked result?

**Source field index:** A2, Restricted Retry

**Source keyword index:** shall, should

> Source: NVME-BASE-2.4, Rev. 2.4, §8.1.27.4.3, Figure 775, printed pages 724, PDF pages 750

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 776: Unrestricted Processing State Transition Conditions</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-776-CLAIM figure-table:BASEBTS-BASE-FIG-776 -->

**SPEC.** Figure 776, "Unrestricted Processing State Transition Conditions": C2/D2/F2 from Unrestricted Processing mean successful Idle return, failure, or entry into Verification; unrestricted does not mean ordinary I/O is unrestricted. Decode the source-specific fields below.

#### Where this Figure fits

C2/D2/F2 from Unrestricted Processing mean successful Idle return, failure, or entry into Verification; unrestricted does not mean ordinary I/O is unrestricted.

The indexed fields below belong to this source document and this Figure. The worked example connects them to the full operation.

#### Teaching redraw

```text
[Locate source: C2]
          ↓
[Extract field: D2] → [Apply encoding: F2]
                                      ↓
[Validate evidence: EMVS]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `C2` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `D2` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `F2` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `EMVS` | Enter Media Verification State; requests verification after successful processing, subject to method and capability restrictions. |
| `MVCNCLD` | Media Verification Canceled; records canceled verification and affects the transition after processing. |

#### Read in this order

1. Confirm NVME-BASE-2.4, §8.1.27.4.4, Figure 776; equal Figure numbers in different documents are different sources.
2. Apply the field/state rule above to the captured raw input.
3. Start with the seven states in Figure 772 and attach transition conditions from Figures 773–779. Status describes results, state describes the current position, and events report transitions.
4. Compare the observation with the worked scenario and retain the cited source and target identity.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 776 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §8.1.27.4.4 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| Rule | C2/D2/F2 from Unrestricted Processing mean successful Idle return, failure, or entry into Verification; unrestricted does not mean ordinary I/O is unrestricted. |
| Boundary | Preserve SCDW10, SOS, SANS, FAILS, MVCNCLD, and event timestamps. Recording only a completion event conflates success, failure, and entry into verification. |

**Informative example.** SPROG=8000h represents 50% of the currently measured phase. Media Verification uses SPROG=FFFFh while SOS can remain 010b; leaving verification for deallocation starts progress again at zero. This is not progress regression.

**Common misconception.** Preserve SCDW10, SOS, SANS, FAILS, MVCNCLD, and event timestamps. Recording only a completion event conflates success, failure, and entry into verification.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Symptom / correction | Preserve SCDW10, SOS, SANS, FAILS, MVCNCLD, and event timestamps. Recording only a completion event conflates success, failure, and entry into verification. |

#### Questions the reader should now answer

1. Which source-specific fields establish the decision?
2. Which capability, target, or state would change the worked result?

**Source field index:** C2, D2, F2, EMVS, MVCNCLD

**Source keyword index:** shall

> Source: NVME-BASE-2.4, Rev. 2.4, §8.1.27.4.4, Figure 776, printed pages 725, PDF pages 751

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 777: Unrestricted Failure State Transition Conditions</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-777-CLAIM figure-table:BASEBTS-BASE-FIG-777 -->

**SPEC.** Figure 777, "Unrestricted Failure State Transition Conditions": Unrestricted Failure permits A3 restricted retry, B2 unrestricted retry, or E Exit Failure Mode to Idle; E is not proof of successful sanitization. Decode the source-specific fields below.

#### Where this Figure fits

Unrestricted Failure permits A3 restricted retry, B2 unrestricted retry, or E Exit Failure Mode to Idle; E is not proof of successful sanitization.

The indexed fields below belong to this source document and this Figure. The worked example connects them to the full operation.

#### Teaching redraw

```text
[Locate source: A3]
          ↓
[Extract field: B2] → [Apply encoding: E]
                                      ↓
[Validate evidence: Exit Failure Mode]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `A3` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `B2` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `E` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `Exit Failure Mode` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Confirm NVME-BASE-2.4, §8.1.27.4.5, Figure 777; equal Figure numbers in different documents are different sources.
2. Apply the field/state rule above to the captured raw input.
3. Start with the seven states in Figure 772 and attach transition conditions from Figures 773–779. Status describes results, state describes the current position, and events report transitions.
4. Compare the observation with the worked scenario and retain the cited source and target identity.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 777 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §8.1.27.4.5 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| Rule | Unrestricted Failure permits A3 restricted retry, B2 unrestricted retry, or E Exit Failure Mode to Idle; E is not proof of successful sanitization. |
| Boundary | Preserve SCDW10, SOS, SANS, FAILS, MVCNCLD, and event timestamps. Recording only a completion event conflates success, failure, and entry into verification. |

**Informative example.** SPROG=8000h represents 50% of the currently measured phase. Media Verification uses SPROG=FFFFh while SOS can remain 010b; leaving verification for deallocation starts progress again at zero. This is not progress regression.

**Common misconception.** Preserve SCDW10, SOS, SANS, FAILS, MVCNCLD, and event timestamps. Recording only a completion event conflates success, failure, and entry into verification.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Symptom / correction | Preserve SCDW10, SOS, SANS, FAILS, MVCNCLD, and event timestamps. Recording only a completion event conflates success, failure, and entry into verification. |

#### Questions the reader should now answer

1. Which source-specific fields establish the decision?
2. Which capability, target, or state would change the worked result?

**Source field index:** A3, B2, E, Exit Failure Mode

**Source keyword index:** shall

> Source: NVME-BASE-2.4, Rev. 2.4, §8.1.27.4.5, Figure 777, printed pages 727, PDF pages 753

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 778: Media Verification State Transition Conditions</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-778-CLAIM figure-table:BASEBTS-BASE-FIG-778 -->

**SPEC.** Figure 778, "Media Verification State Transition Conditions": G enters Post-Verification Deallocation on the exit action, specified resets, or a composition change preventing verification; check MVCNCLD for canceled verification. Decode the source-specific fields below.

#### Where this Figure fits

G enters Post-Verification Deallocation on the exit action, specified resets, or a composition change preventing verification; check MVCNCLD for canceled verification.

The indexed fields below belong to this source document and this Figure. The worked example connects them to the full operation.

#### Teaching redraw

```text
[Locate source: G]
          ↓
[Extract field: Exit Media Verification] → [Apply encoding: Reset]
                                      ↓
[Validate evidence: MVCNCLD]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `G` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `Exit Media Verification` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `Reset` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `MVCNCLD` | Media Verification Canceled; records canceled verification and affects the transition after processing. |

#### Read in this order

1. Confirm NVME-BASE-2.4, §8.1.27.4.6, Figure 778; equal Figure numbers in different documents are different sources.
2. Apply the field/state rule above to the captured raw input.
3. Start with the seven states in Figure 772 and attach transition conditions from Figures 773–779. Status describes results, state describes the current position, and events report transitions.
4. Compare the observation with the worked scenario and retain the cited source and target identity.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 778 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §8.1.27.4.6 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| Rule | G enters Post-Verification Deallocation on the exit action, specified resets, or a composition change preventing verification; check MVCNCLD for canceled verification. |
| Boundary | Preserve SCDW10, SOS, SANS, FAILS, MVCNCLD, and event timestamps. Recording only a completion event conflates success, failure, and entry into verification. |

**Informative example.** SPROG=8000h represents 50% of the currently measured phase. Media Verification uses SPROG=FFFFh while SOS can remain 010b; leaving verification for deallocation starts progress again at zero. This is not progress regression.

**Common misconception.** Preserve SCDW10, SOS, SANS, FAILS, MVCNCLD, and event timestamps. Recording only a completion event conflates success, failure, and entry into verification.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Symptom / correction | Preserve SCDW10, SOS, SANS, FAILS, MVCNCLD, and event timestamps. Recording only a completion event conflates success, failure, and entry into verification. |

#### Questions the reader should now answer

1. Which source-specific fields establish the decision?
2. Which capability, target, or state would change the worked result?

**Source field index:** G, Exit Media Verification, Reset, MVCNCLD

**Source keyword index:** shall

> Source: NVME-BASE-2.4, Rev. 2.4, §8.1.27.4.6, Figure 778, printed pages 728, PDF pages 754

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 779: Post-Verification Deallocation state Transition Conditions</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-779-CLAIM figure-table:BASEBTS-BASE-FIG-779 -->

**SPEC.** Figure 779, "Post-Verification Deallocation state Transition Conditions": Successful deallocation takes H to Idle; failure follows original AUSE through I1/I2 to Failure, with FAILS=6h distinguishing it from processing failure. Decode the source-specific fields below.

#### Where this Figure fits

Successful deallocation takes H to Idle; failure follows original AUSE through I1/I2 to Failure, with FAILS=6h distinguishing it from processing failure.

The indexed fields below belong to this source document and this Figure. The worked example connects them to the full operation.

#### Teaching redraw

```text
[Locate source: H]
          ↓
[Extract field: I1] → [Apply encoding: I2]
                                      ↓
[Validate evidence: FAILS]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `H` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `I1` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `I2` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `FAILS` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Confirm NVME-BASE-2.4, §8.1.27.4.7, Figure 779; equal Figure numbers in different documents are different sources.
2. Apply the field/state rule above to the captured raw input.
3. Start with the seven states in Figure 772 and attach transition conditions from Figures 773–779. Status describes results, state describes the current position, and events report transitions.
4. Compare the observation with the worked scenario and retain the cited source and target identity.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 779 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §8.1.27.4.7 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| Rule | Successful deallocation takes H to Idle; failure follows original AUSE through I1/I2 to Failure, with FAILS=6h distinguishing it from processing failure. |
| Boundary | Preserve SCDW10, SOS, SANS, FAILS, MVCNCLD, and event timestamps. Recording only a completion event conflates success, failure, and entry into verification. |

**Informative example.** SPROG=8000h represents 50% of the currently measured phase. Media Verification uses SPROG=FFFFh while SOS can remain 010b; leaving verification for deallocation starts progress again at zero. This is not progress regression.

**Common misconception.** Preserve SCDW10, SOS, SANS, FAILS, MVCNCLD, and event timestamps. Recording only a completion event conflates success, failure, and entry into verification.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Symptom / correction | Preserve SCDW10, SOS, SANS, FAILS, MVCNCLD, and event timestamps. Recording only a completion event conflates success, failure, and entry into verification. |

#### Questions the reader should now answer

1. Which source-specific fields establish the decision?
2. Which capability, target, or state would change the worked result?

**Source field index:** H, I1, I2, FAILS

**Source keyword index:** shall

> Source: NVME-BASE-2.4, Rev. 2.4, §8.1.27.4.7, Figure 779, printed pages 729, PDF pages 755

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 780: Telemetry Log Example - All Data Areas Populated</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-780-CLAIM figure-table:BASEBTS-BASE-FIG-780 -->

**SPEC.** Figure 780, "Telemetry Log Example - All Data Areas Populated": Areas ending at 65/1000/30000 share prefixes; Area 3 includes Areas 1 and 2, so do not sum their lengths. Decode the source-specific fields below.

#### Where this Figure fits

Areas ending at 65/1000/30000 share prefixes; Area 3 includes Areas 1 and 2, so do not sum their lengths.

The indexed fields below belong to this source document and this Figure. The worked example connects them to the full operation.

#### Teaching redraw

```text
[Locate source: Last Block 65]
          ↓
[Extract field: Last Block 1000] → [Apply encoding: Last Block 30000]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `Last Block 65` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `Last Block 1000` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `Last Block 30000` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Confirm NVME-BASE-2.4, §8.1.30, Figure 780; equal Figure numbers in different documents are different sources.
2. Apply the field/state rule above to the captured raw input.
3. Areas are differently sized views starting at the same block 1. Decode the header, select the final applicable populated area, and do not add the three Last Block numbers.
4. Compare the observation with the worked scenario and retain the cited source and target identity.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 780 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §8.1.30 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| Rule | Areas ending at 65/1000/30000 share prefixes; Area 3 includes Areas 1 and 2, so do not sum their lengths. |
| Boundary | THS in LID 07h and TCS in LID 08h have different offsets; do not reuse one header layout for the other. Snapshot payload is vendor-defined, so unknown bytes cannot be assigned invented diagnostic fields. |

**Informative example.** For Last Blocks=65/1000/30000, Area 3 payload is 30000×512=15360000 bytes and the log including its header is 15360512 bytes. Values 0/1000/1000 mean Area 1 is empty and Area 3 adds no content beyond Area 2.

**Common misconception.** THS in LID 07h and TCS in LID 08h have different offsets; do not reuse one header layout for the other. Snapshot payload is vendor-defined, so unknown bytes cannot be assigned invented diagnostic fields.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Symptom / correction | THS in LID 07h and TCS in LID 08h have different offsets; do not reuse one header layout for the other. Snapshot payload is vendor-defined, so unknown bytes cannot be assigned invented diagnostic fields. |

#### Questions the reader should now answer

1. Which source-specific fields establish the decision?
2. Which capability, target, or state would change the worked result?

**Source field index:** Last Block 65, Last Block 1000, Last Block 30000

**Source keyword index:** none

> Source: NVME-BASE-2.4, Rev. 2.4, §8.1.30, Figure 780, printed pages 736, PDF pages 762

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 781: Telemetry Log Example - Data Area 2 Populated</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-781-CLAIM figure-table:BASEBTS-BASE-FIG-781 -->

**SPEC.** Figure 781, "Telemetry Log Example - Data Area 2 Populated": Endpoints 0/1000/1000 mean empty Area 1, populated Area 2, and no additional Area 3 data; the Area 3 view still covers the same blocks as Area 2. Decode the source-specific fields below.

#### Where this Figure fits

Endpoints 0/1000/1000 mean empty Area 1, populated Area 2, and no additional Area 3 data; the Area 3 view still covers the same blocks as Area 2.

The indexed fields below belong to this source document and this Figure. The worked example connects them to the full operation.

#### Teaching redraw

```text
[Locate source: Last Block 0]
          ↓
[Extract field: Last Block 1000] → [Apply encoding: Equal Endpoints]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `Last Block 0` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `Last Block 1000` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `Equal Endpoints` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Confirm NVME-BASE-2.4, §8.1.30, Figure 781; equal Figure numbers in different documents are different sources.
2. Apply the field/state rule above to the captured raw input.
3. Areas are differently sized views starting at the same block 1. Decode the header, select the final applicable populated area, and do not add the three Last Block numbers.
4. Compare the observation with the worked scenario and retain the cited source and target identity.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 781 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §8.1.30 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| Rule | Endpoints 0/1000/1000 mean empty Area 1, populated Area 2, and no additional Area 3 data; the Area 3 view still covers the same blocks as Area 2. |
| Boundary | THS in LID 07h and TCS in LID 08h have different offsets; do not reuse one header layout for the other. Snapshot payload is vendor-defined, so unknown bytes cannot be assigned invented diagnostic fields. |

**Informative example.** For Last Blocks=65/1000/30000, Area 3 payload is 30000×512=15360000 bytes and the log including its header is 15360512 bytes. Values 0/1000/1000 mean Area 1 is empty and Area 3 adds no content beyond Area 2.

**Common misconception.** THS in LID 07h and TCS in LID 08h have different offsets; do not reuse one header layout for the other. Snapshot payload is vendor-defined, so unknown bytes cannot be assigned invented diagnostic fields.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Symptom / correction | THS in LID 07h and TCS in LID 08h have different offsets; do not reuse one header layout for the other. Snapshot payload is vendor-defined, so unknown bytes cannot be assigned invented diagnostic fields. |

#### Questions the reader should now answer

1. Which source-specific fields establish the decision?
2. Which capability, target, or state would change the worked result?

**Source field index:** Last Block 0, Last Block 1000, Equal Endpoints

**Source keyword index:** may

> Source: NVME-BASE-2.4, Rev. 2.4, §8.1.30, Figure 781, printed pages 737, PDF pages 763

</details>

<a id="section-dependency"></a>

### Referenced Figure dependencies (outside the main section range)

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 11: Protection Information Field Definition</strong></summary>

<!-- claim:BASEBTS-NVMCS-FIG-011-CLAIM figure-table:BASEBTS-NVMCS-FIG-011 -->

**SPEC.** Figure 11, "Protection Information Field Definition": PRACT governs PI handling; the three PRCHK bits request Guard/Application/Reference Tag checking. Media Verification explicitly requires PRCHK=000b. Decode the source-specific fields below.

#### Where this Figure fits

PRACT governs PI handling; the three PRCHK bits request Guard/Application/Reference Tag checking. Media Verification explicitly requires PRCHK=000b.

The indexed fields below belong to this source document and this Figure. The worked example connects them to the full operation.

#### Teaching redraw

```text
[Locate source: PRACT]
          ↓
[Extract field: PRCHK] → [Apply encoding: GRDCHK]
                                      ↓
[Validate evidence: ATCHK]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `PRACT` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `PRCHK` | Protection Information Check; three bits request guard, application-tag, and reference-tag checking; verification reads use 000b. |
| `GRDCHK` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `ATCHK` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `RTCHK` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Confirm NVME-NVM-CS-1.3, §2.1.5, Figure 11; equal Figure numbers in different documents are different sources.
2. Apply the field/state rule above to the captured raw input.
3. Evaluate the command allowlist and the NVM Read exception separately. Determine target/state, then PI checking and allocation; ordinary-read behavior cannot be applied unchanged to verification.
4. Compare the observation with the worked scenario and retain the cited source and target identity.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 11 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §2.1.5 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| Rule | PRACT governs PI handling; the three PRCHK bits request Guard/Application/Reference Tag checking. Media Verification explicitly requires PRCHK=000b. |
| Boundary | Do not assume all Get Log Page requests are permitted during subsystem sanitize; 07h/08h are absent from Figure 144. Namespace sanitize restrictions require a separate attached/target-scope evaluation. |

**Informative example.** A verification read with PRCHK=000b and STC=0, readable allocated LBAs, and no other abort cause completes as Successful Media Verification Read. Requesting PI checking changes the expected branch to Invalid Field in Command.

**Common misconception.** Do not assume all Get Log Page requests are permitted during subsystem sanitize; 07h/08h are absent from Figure 144. Namespace sanitize restrictions require a separate attached/target-scope evaluation.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Symptom / correction | Do not assume all Get Log Page requests are permitted during subsystem sanitize; 07h/08h are absent from Figure 144. Namespace sanitize restrictions require a separate attached/target-scope evaluation. |

#### Questions the reader should now answer

1. Which source-specific fields establish the decision?
2. Which capability, target, or state would change the worked result?

**Source field index:** PRACT, PRCHK, GRDCHK, ATCHK, RTCHK

**Source keyword index:** shall not, shall, may, optional

> Source: NVME-NVM-CS-1.3, Rev. 1.3, §2.1.5, Figure 11, printed pages 21-22, PDF pages 21-22

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 12: Storage Tag Check Definition</strong></summary>

<!-- claim:BASEBTS-NVMCS-FIG-012-CLAIM figure-table:BASEBTS-NVMCS-FIG-012 -->

**SPEC.** Figure 12, "Storage Tag Check Definition": Here STC is Storage Tag Check, not Self-test Code from another report; verification Reads require STC=0. Decode the source-specific fields below.

#### Where this Figure fits

Here STC is Storage Tag Check, not Self-test Code from another report; verification Reads require STC=0.

The indexed fields below belong to this source document and this Figure. The worked example connects them to the full operation.

#### Teaching redraw

```text
[Locate source: STC]
          ↓
[Extract field: Storage Tag] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `STC` | Storage Tag Check; here it selects storage-tag checking for NVM Reads and is zero for verification reads. |
| `Storage Tag` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Confirm NVME-NVM-CS-1.3, §2.1.5, Figure 12; equal Figure numbers in different documents are different sources.
2. Apply the field/state rule above to the captured raw input.
3. Evaluate the command allowlist and the NVM Read exception separately. Determine target/state, then PI checking and allocation; ordinary-read behavior cannot be applied unchanged to verification.
4. Compare the observation with the worked scenario and retain the cited source and target identity.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 12 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §2.1.5 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| Rule | Here STC is Storage Tag Check, not Self-test Code from another report; verification Reads require STC=0. |
| Boundary | Do not assume all Get Log Page requests are permitted during subsystem sanitize; 07h/08h are absent from Figure 144. Namespace sanitize restrictions require a separate attached/target-scope evaluation. |

**Informative example.** A verification read with PRCHK=000b and STC=0, readable allocated LBAs, and no other abort cause completes as Successful Media Verification Read. Requesting PI checking changes the expected branch to Invalid Field in Command.

**Common misconception.** Do not assume all Get Log Page requests are permitted during subsystem sanitize; 07h/08h are absent from Figure 144. Namespace sanitize restrictions require a separate attached/target-scope evaluation.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Symptom / correction | Do not assume all Get Log Page requests are permitted during subsystem sanitize; 07h/08h are absent from Figure 144. Namespace sanitize restrictions require a separate attached/target-scope evaluation. |

#### Questions the reader should now answer

1. Which source-specific fields establish the decision?
2. Which capability, target, or state would change the worked result?

**Source field index:** STC, Storage Tag

**Source keyword index:** shall not, shall, may, optional

> Source: NVME-NVM-CS-1.3, Rev. 1.3, §2.1.5, Figure 12, printed pages 22, PDF pages 22

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 36: Offset 0h: CAP - Controller Capabilities</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-036-CLAIM figure-table:BASEBTS-BASE-FIG-036 -->

**SPEC.** Figure 36, "Offset 0h: CAP - Controller Capabilities": Check BPS before using Boot properties; Boot support does not imply an enabled controller. Decode the source-specific fields below.

#### Where this Figure fits

Check BPS before using Boot properties; Boot support does not imply an enabled controller.

The indexed fields below belong to this source document and this Figure. The worked example connects them to the full operation.

#### Teaching redraw

```text
[Locate source: CAP.BPS]
          ↓
[Extract field: evidence] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `CAP.BPS` | Controller Capabilities, the controller property at offset 00h that reports queue, page-size, timeout, and other capabilities. Here CAP.BPS selects its BPS member field. |

#### Read in this order

1. Confirm NVME-BASE-2.4, §3.1.4.1, Figure 36; equal Figure numbers in different documents are different sources.
2. Apply the field/state rule above to the captured raw input.
3. First determine whether an Admin-command environment exists, then choose properties or LID 15h. Both access boot contents, but their return formats and observation points differ.
4. Compare the observation with the worked scenario and retain the cited source and target identity.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 36 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.1.4.1 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| Rule | Check BPS before using Boot properties; Boot support does not imply an enabled controller. |
| Boundary | For an unfinished property read, inspect BRS and the buffer; reset is not an allowed normal completion step. BPINFO in LID 15h is a returned field and reading it does not modify the property of the same name. |

**Informative example.** With BPSZ=2, LID 15h contains 262144 bytes of boot data plus a 16-byte header, totaling 262160 bytes. Reading BP1 does not activate BP1, and a log read does not advance the property's BRS.

**Common misconception.** For an unfinished property read, inspect BRS and the buffer; reset is not an allowed normal completion step. BPINFO in LID 15h is a returned field and reading it does not modify the property of the same name.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Symptom / correction | For an unfinished property read, inspect BRS and the buffer; reset is not an allowed normal completion step. BPINFO in LID 15h is a returned field and reading it does not modify the property of the same name. |

#### Questions the reader should now answer

1. Which source-specific fields establish the decision?
2. Which capability, target, or state would change the worked result?

**Source field index:** CAP.BPS

**Source keyword index:** shall not, shall, should, may, optional, reserved

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.1, Figure 36, printed pages 55-58, PDF pages 81-84

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 49: Offset 40h: BPINFO - Boot Partition Information</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-049-CLAIM figure-table:BASEBTS-BASE-FIG-049 -->

**SPEC.** Figure 49, "Offset 40h: BPINFO - Boot Partition Information": ABPID identifies the active partition, BPSZ uses 128 KiB units, and BRS distinguishes no request/in progress/success/error with 00b/01b/10b/11b. Decode the source-specific fields below.

#### Where this Figure fits

ABPID identifies the active partition, BPSZ uses 128 KiB units, and BRS distinguishes no request/in progress/success/error with 00b/01b/10b/11b.

The indexed fields below belong to this source document and this Figure. The worked example connects them to the full operation.

#### Teaching redraw

```text
[Locate source: ABPID]
          ↓
[Extract field: BPSZ] → [Apply encoding: BRS]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `ABPID` | Active Boot Partition ID; identifies the partition selected as the boot image. |
| `BPSZ` | Boot Partition Size; each unit is 128 KiB. |
| `BRS` | Boot Read Status: 00b no request, 01b in progress, 10b success, 11b error. |

#### Read in this order

1. Confirm NVME-BASE-2.4, §3.1.4.13, Figure 49; equal Figure numbers in different documents are different sources.
2. Apply the field/state rule above to the captured raw input.
3. First determine whether an Admin-command environment exists, then choose properties or LID 15h. Both access boot contents, but their return formats and observation points differ.
4. Compare the observation with the worked scenario and retain the cited source and target identity.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 49 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.1.4.13 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| Rule | ABPID identifies the active partition, BPSZ uses 128 KiB units, and BRS distinguishes no request/in progress/success/error with 00b/01b/10b/11b. |
| Boundary | For an unfinished property read, inspect BRS and the buffer; reset is not an allowed normal completion step. BPINFO in LID 15h is a returned field and reading it does not modify the property of the same name. |

**Informative example.** With BPSZ=2, LID 15h contains 262144 bytes of boot data plus a 16-byte header, totaling 262160 bytes. Reading BP1 does not activate BP1, and a log read does not advance the property's BRS.

**Common misconception.** For an unfinished property read, inspect BRS and the buffer; reset is not an allowed normal completion step. BPINFO in LID 15h is a returned field and reading it does not modify the property of the same name.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Symptom / correction | For an unfinished property read, inspect BRS and the buffer; reset is not an allowed normal completion step. BPINFO in LID 15h is a returned field and reading it does not modify the property of the same name. |

#### Questions the reader should now answer

1. Which source-specific fields establish the decision?
2. Which capability, target, or state would change the worked result?

**Source field index:** ABPID, BPSZ, BRS

**Source keyword index:** shall not, shall, optional, reserved

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.13, Figure 49, printed pages 69, PDF pages 95

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 50: Offset 44h: BPRSEL - Boot Partition Read Select</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-050-CLAIM figure-table:BASEBTS-BASE-FIG-050 -->

**SPEC.** Figure 50, "Offset 44h: BPRSEL - Boot Partition Read Select": BPRSEL bit 31 is BPID, bit 30 is reserved, [29:10] is BPROF in 4 KiB units, and [9:0] is BPRSZ in 4 KiB units; writing initiates a read. Decode the source-specific fields below.

#### Where this Figure fits

BPRSEL bit 31 is BPID, bit 30 is reserved, [29:10] is BPROF in 4 KiB units, and [9:0] is BPRSZ in 4 KiB units; writing initiates a read.

The indexed fields below belong to this source document and this Figure. The worked example connects them to the full operation.

#### Teaching redraw

```text
[Locate source: BPID]
          ↓
[Extract field: BPRSZ] → [Apply encoding: BPROF]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `BPID` | Boot Partition Identifier; selects 0 or 1 independently of the active partition. |
| `BPRSZ` | Boot Partition Read Size; uses 4 KiB units, not BPSZ units. |
| `BPROF` | Boot Partition Read Offset; BPRSEL bits 29:10 in 4 KiB units; bit 30 is reserved. |

#### Read in this order

1. Confirm NVME-BASE-2.4, §3.1.4.14, Figure 50; equal Figure numbers in different documents are different sources.
2. Apply the field/state rule above to the captured raw input.
3. First determine whether an Admin-command environment exists, then choose properties or LID 15h. Both access boot contents, but their return formats and observation points differ.
4. Compare the observation with the worked scenario and retain the cited source and target identity.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 50 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.1.4.14 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| Rule | BPRSEL bit 31 is BPID, bit 30 is reserved, [29:10] is BPROF in 4 KiB units, and [9:0] is BPRSZ in 4 KiB units; writing initiates a read. |
| Boundary | For an unfinished property read, inspect BRS and the buffer; reset is not an allowed normal completion step. BPINFO in LID 15h is a returned field and reading it does not modify the property of the same name. |

**Informative example.** With BPSZ=2, LID 15h contains 262144 bytes of boot data plus a 16-byte header, totaling 262160 bytes. Reading BP1 does not activate BP1, and a log read does not advance the property's BRS.

**Common misconception.** For an unfinished property read, inspect BRS and the buffer; reset is not an allowed normal completion step. BPINFO in LID 15h is a returned field and reading it does not modify the property of the same name.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Symptom / correction | For an unfinished property read, inspect BRS and the buffer; reset is not an allowed normal completion step. BPINFO in LID 15h is a returned field and reading it does not modify the property of the same name. |

#### Questions the reader should now answer

1. Which source-specific fields establish the decision?
2. Which capability, target, or state would change the worked result?

**Source field index:** BPID, BPRSZ, BPROF

**Source keyword index:** shall not, shall, optional, reserved

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.14, Figure 50, printed pages 69-70, PDF pages 95-96

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 51: Offset 48h: BPMBL - Boot Partition Memory Buffer Location</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-051-CLAIM figure-table:BASEBTS-BASE-FIG-051 -->

**SPEC.** Figure 51, "Offset 48h: BPMBL - Boot Partition Memory Buffer Location": BPMBL[63:12] provides the Boot Memory Buffer base address; the low 12 bits are reserved. Establish a contiguous, aligned host buffer first. Decode the source-specific fields below.

#### Where this Figure fits

BPMBL[63:12] provides the Boot Memory Buffer base address; the low 12 bits are reserved. Establish a contiguous, aligned host buffer first.

The indexed fields below belong to this source document and this Figure. The worked example connects them to the full operation.

#### Teaching redraw

```text
[Locate source: BMBBA]
          ↓
[Extract field: evidence] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `BMBBA` | Boot Memory Buffer Base Address; BPMBL bits 63:12, with the low 12 bits reserved. |

#### Read in this order

1. Confirm NVME-BASE-2.4, §3.1.4.15, Figure 51; equal Figure numbers in different documents are different sources.
2. Apply the field/state rule above to the captured raw input.
3. First determine whether an Admin-command environment exists, then choose properties or LID 15h. Both access boot contents, but their return formats and observation points differ.
4. Compare the observation with the worked scenario and retain the cited source and target identity.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 51 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.1.4.15 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| Rule | BPMBL[63:12] provides the Boot Memory Buffer base address; the low 12 bits are reserved. Establish a contiguous, aligned host buffer first. |
| Boundary | For an unfinished property read, inspect BRS and the buffer; reset is not an allowed normal completion step. BPINFO in LID 15h is a returned field and reading it does not modify the property of the same name. |

**Informative example.** With BPSZ=2, LID 15h contains 262144 bytes of boot data plus a 16-byte header, totaling 262160 bytes. Reading BP1 does not activate BP1, and a log read does not advance the property's BRS.

**Common misconception.** For an unfinished property read, inspect BRS and the buffer; reset is not an allowed normal completion step. BPINFO in LID 15h is a returned field and reading it does not modify the property of the same name.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Symptom / correction | For an unfinished property read, inspect BRS and the buffer; reset is not an allowed normal completion step. BPINFO in LID 15h is a returned field and reading it does not modify the property of the same name. |

#### Questions the reader should now answer

1. Which source-specific fields establish the decision?
2. Which capability, target, or state would change the worked result?

**Source field index:** BMBBA

**Source keyword index:** shall not, shall, optional, reserved

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.15, Figure 51, printed pages 70, PDF pages 96

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 144: NVM Subsystem Sanitize Operations and Format NVM Command - Admin</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-144-CLAIM figure-table:BASEBTS-BASE-FIG-144 -->

**SPEC.** Figure 144, "NVM Subsystem Sanitize Operations and Format NVM Command - Admin": Read the Sanitize column's command allowlist and per-command restrictions. Boot is readable; Telemetry 07h/08h is not listed. Only common and memory-based command rows are used. Decode the source-specific fields below.

#### Where this Figure fits

Read the Sanitize column's command allowlist and per-command restrictions. Boot is readable; Telemetry 07h/08h is not listed. Only common and memory-based command rows are used.

The indexed fields below belong to this source document and this Figure. The worked example connects them to the full operation.

#### Teaching redraw

```text
[Locate source: Get Log Page]
          ↓
[Extract field: Boot Partition] → [Apply encoding: Sanitize Status]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `Get Log Page` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `Boot Partition` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `Sanitize Status` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Confirm NVME-BASE-2.4, §5.1.1, Figure 144; equal Figure numbers in different documents are different sources.
2. Apply the field/state rule above to the captured raw input.
3. Evaluate the command allowlist and the NVM Read exception separately. Determine target/state, then PI checking and allocation; ordinary-read behavior cannot be applied unchanged to verification.
4. Compare the observation with the worked scenario and retain the cited source and target identity.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 144 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §5.1.1 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| Rule | Read the Sanitize column's command allowlist and per-command restrictions. Boot is readable; Telemetry 07h/08h is not listed. Only common and memory-based command rows are used. |
| Boundary | Do not assume all Get Log Page requests are permitted during subsystem sanitize; 07h/08h are absent from Figure 144. Namespace sanitize restrictions require a separate attached/target-scope evaluation. |

**Informative example.** A verification read with PRCHK=000b and STC=0, readable allocated LBAs, and no other abort cause completes as Successful Media Verification Read. Requesting PI checking changes the expected branch to Invalid Field in Command.

**Common misconception.** Do not assume all Get Log Page requests are permitted during subsystem sanitize; 07h/08h are absent from Figure 144. Namespace sanitize restrictions require a separate attached/target-scope evaluation.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Symptom / correction | Do not assume all Get Log Page requests are permitted during subsystem sanitize; 07h/08h are absent from Figure 144. Namespace sanitize restrictions require a separate attached/target-scope evaluation. |

#### Questions the reader should now answer

1. Which source-specific fields establish the decision?
2. Which capability, target, or state would change the worked result?

**Source field index:** Get Log Page, Boot Partition, Sanitize Status

**Source keyword index:** shall, should, may

> Source: NVME-BASE-2.4, Rev. 2.4, §5.1.1, Figure 144, printed pages 178-179, PDF pages 204-205

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 145: Namespace Sanitize Operations - Admin Command Restrictions, All Controllers</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-145-CLAIM figure-table:BASEBTS-BASE-FIG-145 -->

**SPEC.** Figure 145, "Namespace Sanitize Operations - Admin Command Restrictions, All Controllers": This table applies to all controllers: for example, deletion of a namespace being sanitized and firmware updates are restricted. Establish the target relationship before choosing a status. Decode the source-specific fields below.

#### Where this Figure fits

This table applies to all controllers: for example, deletion of a namespace being sanitized and firmware updates are restricted. Establish the target relationship before choosing a status.

The indexed fields below belong to this source document and this Figure. The worked example connects them to the full operation.

#### Teaching redraw

```text
[Locate source: Set Features]
          ↓
[Extract field: Namespace Management] → [Apply encoding: Firmware Commit]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `Set Features` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `Namespace Management` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `Firmware Commit` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Confirm NVME-BASE-2.4, §5.1.2, Figure 145; equal Figure numbers in different documents are different sources.
2. Apply the field/state rule above to the captured raw input.
3. Evaluate the command allowlist and the NVM Read exception separately. Determine target/state, then PI checking and allocation; ordinary-read behavior cannot be applied unchanged to verification.
4. Compare the observation with the worked scenario and retain the cited source and target identity.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 145 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §5.1.2 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| Rule | This table applies to all controllers: for example, deletion of a namespace being sanitized and firmware updates are restricted. Establish the target relationship before choosing a status. |
| Boundary | Do not assume all Get Log Page requests are permitted during subsystem sanitize; 07h/08h are absent from Figure 144. Namespace sanitize restrictions require a separate attached/target-scope evaluation. |

**Informative example.** A verification read with PRCHK=000b and STC=0, readable allocated LBAs, and no other abort cause completes as Successful Media Verification Read. Requesting PI checking changes the expected branch to Invalid Field in Command.

**Common misconception.** Do not assume all Get Log Page requests are permitted during subsystem sanitize; 07h/08h are absent from Figure 144. Namespace sanitize restrictions require a separate attached/target-scope evaluation.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Symptom / correction | Do not assume all Get Log Page requests are permitted during subsystem sanitize; 07h/08h are absent from Figure 144. Namespace sanitize restrictions require a separate attached/target-scope evaluation. |

#### Questions the reader should now answer

1. Which source-specific fields establish the decision?
2. Which capability, target, or state would change the worked result?

**Source field index:** Set Features, Namespace Management, Firmware Commit

**Source keyword index:** shall

> Source: NVME-BASE-2.4, Rev. 2.4, §5.1.2, Figure 145, printed pages 179-180, PDF pages 205-206

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 146: Namespace Sanitize Operations - Admin Command Restrictions if Sanitizing</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-146-CLAIM figure-table:BASEBTS-BASE-FIG-146 -->

**SPEC.** Figure 146, "Namespace Sanitize Operations - Admin Command Restrictions if Sanitizing": This table adds restrictions for controllers with an attached namespace being sanitized. Do not conflate all-controller restrictions with attached-controller restrictions. Decode the source-specific fields below.

#### Where this Figure fits

This table adds restrictions for controllers with an attached namespace being sanitized. Do not conflate all-controller restrictions with attached-controller restrictions.

The indexed fields below belong to this source document and this Figure. The worked example connects them to the full operation.

#### Teaching redraw

```text
[Locate source: Attached Namespace]
          ↓
[Extract field: Admin command restrictions] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `Attached Namespace` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `Admin command restrictions` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Confirm NVME-BASE-2.4, §5.1.2, Figure 146; equal Figure numbers in different documents are different sources.
2. Apply the field/state rule above to the captured raw input.
3. Evaluate the command allowlist and the NVM Read exception separately. Determine target/state, then PI checking and allocation; ordinary-read behavior cannot be applied unchanged to verification.
4. Compare the observation with the worked scenario and retain the cited source and target identity.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 146 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §5.1.2 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| Rule | This table adds restrictions for controllers with an attached namespace being sanitized. Do not conflate all-controller restrictions with attached-controller restrictions. |
| Boundary | Do not assume all Get Log Page requests are permitted during subsystem sanitize; 07h/08h are absent from Figure 144. Namespace sanitize restrictions require a separate attached/target-scope evaluation. |

**Informative example.** A verification read with PRCHK=000b and STC=0, readable allocated LBAs, and no other abort cause completes as Successful Media Verification Read. Requesting PI checking changes the expected branch to Invalid Field in Command.

**Common misconception.** Do not assume all Get Log Page requests are permitted during subsystem sanitize; 07h/08h are absent from Figure 144. Namespace sanitize restrictions require a separate attached/target-scope evaluation.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Symptom / correction | Do not assume all Get Log Page requests are permitted during subsystem sanitize; 07h/08h are absent from Figure 144. Namespace sanitize restrictions require a separate attached/target-scope evaluation. |

#### Questions the reader should now answer

1. Which source-specific fields establish the decision?
2. Which capability, target, or state would change the worked result?

**Source field index:** Attached Namespace, Admin command restrictions

**Source keyword index:** should not, shall, should, may, reserved

> Source: NVME-BASE-2.4, Rev. 2.4, §5.1.2, Figure 146, printed pages 180-181, PDF pages 206-207

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 151: Asynchronous Event Request - Completion Queue Entry Dword 0</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-151-CLAIM figure-table:BASEBTS-BASE-FIG-151 -->

**SPEC.** Figure 151, "Asynchronous Event Request - Completion Queue Entry Dword 0": CQE DW0[23:16] is LID, [15:8] AEI, and [2:0] AET. Sanitize uses LID 81h/AET 110b; Telemetry uses the Notice type. Decode the source-specific fields below.

#### Where this Figure fits

CQE DW0[23:16] is LID, [15:8] AEI, and [2:0] AET. Sanitize uses LID 81h/AET 110b; Telemetry uses the Notice type.

The indexed fields below belong to this source document and this Figure. The worked example connects them to the full operation.

#### Teaching redraw

```text
[Locate source: LID]
          ↓
[Extract field: AEI] → [Apply encoding: AET]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `LID` | Log Page Identifier, the Get Log Page field selecting a log page. |
| `AEI` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `AET` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Confirm NVME-BASE-2.4, §5.2.2.1, Figure 151; equal Figure numbers in different documents are different sources.
2. Apply the field/state rule above to the captured raw input.
3. Start with the seven states in Figure 772 and attach transition conditions from Figures 773–779. Status describes results, state describes the current position, and events report transitions.
4. Compare the observation with the worked scenario and retain the cited source and target identity.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 151 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §5.2.2.1 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| Rule | CQE DW0[23:16] is LID, [15:8] AEI, and [2:0] AET. Sanitize uses LID 81h/AET 110b; Telemetry uses the Notice type. |
| Boundary | Preserve SCDW10, SOS, SANS, FAILS, MVCNCLD, and event timestamps. Recording only a completion event conflates success, failure, and entry into verification. |

**Informative example.** SPROG=8000h represents 50% of the currently measured phase. Media Verification uses SPROG=FFFFh while SOS can remain 010b; leaving verification for deallocation starts progress again at zero. This is not progress regression.

**Common misconception.** Preserve SCDW10, SOS, SANS, FAILS, MVCNCLD, and event timestamps. Recording only a completion event conflates success, failure, and entry into verification.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Symptom / correction | Preserve SCDW10, SOS, SANS, FAILS, MVCNCLD, and event timestamps. Recording only a completion event conflates success, failure, and entry into verification. |

#### Questions the reader should now answer

1. Which source-specific fields establish the decision?
2. Which capability, target, or state would change the worked result?

**Source field index:** LID, AEI, AET

**Source keyword index:** shall not, shall, should, may, reserved

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.2.1, Figure 151, printed pages 184-185, PDF pages 210-211

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 152: Asynchronous Event Request - Completion Queue Entry Dword 1</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-152-CLAIM figure-table:BASEBTS-BASE-FIG-152 -->

**SPEC.** Figure 152, "Asynchronous Event Request - Completion Queue Entry Dword 1": AER DW1 is the event-specific parameter. Sanitize uses zero for a subsystem and NSID for a namespace; it is not progress. Decode the source-specific fields below.

#### Where this Figure fits

AER DW1 is the event-specific parameter. Sanitize uses zero for a subsystem and NSID for a namespace; it is not progress.

The indexed fields below belong to this source document and this Figure. The worked example connects them to the full operation.

#### Teaching redraw

```text
[Locate source: EVNTSP]
          ↓
[Extract field: evidence] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `EVNTSP` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Confirm NVME-BASE-2.4, §5.2.2.1, Figure 152; equal Figure numbers in different documents are different sources.
2. Apply the field/state rule above to the captured raw input.
3. Start with the seven states in Figure 772 and attach transition conditions from Figures 773–779. Status describes results, state describes the current position, and events report transitions.
4. Compare the observation with the worked scenario and retain the cited source and target identity.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 152 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §5.2.2.1 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| Rule | AER DW1 is the event-specific parameter. Sanitize uses zero for a subsystem and NSID for a namespace; it is not progress. |
| Boundary | Preserve SCDW10, SOS, SANS, FAILS, MVCNCLD, and event timestamps. Recording only a completion event conflates success, failure, and entry into verification. |

**Informative example.** SPROG=8000h represents 50% of the currently measured phase. Media Verification uses SPROG=FFFFh while SOS can remain 010b; leaving verification for deallocation starts progress again at zero. This is not progress regression.

**Common misconception.** Preserve SCDW10, SOS, SANS, FAILS, MVCNCLD, and event timestamps. Recording only a completion event conflates success, failure, and entry into verification.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Symptom / correction | Preserve SCDW10, SOS, SANS, FAILS, MVCNCLD, and event timestamps. Recording only a completion event conflates success, failure, and entry into verification. |

#### Questions the reader should now answer

1. Which source-specific fields establish the decision?
2. Which capability, target, or state would change the worked result?

**Source field index:** EVNTSP

**Source keyword index:** shall not, shall, should, may, reserved

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.2.1, Figure 152, printed pages 185, PDF pages 211

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 155: Asynchronous Event Information - Notice</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-155-CLAIM figure-table:BASEBTS-BASE-FIG-155 -->

**SPEC.** Figure 155, "Asynchronous Event Information - Notice": Use the Telemetry Log Changed Notice slice: locate 08h from the event and read the log; the event does not contain the diagnostic payload. Decode the source-specific fields below.

#### Where this Figure fits

Use the Telemetry Log Changed Notice slice: locate 08h from the event and read the log; the event does not contain the diagnostic payload.

The indexed fields below belong to this source document and this Figure. The worked example connects them to the full operation.

#### Teaching redraw

```text
[Locate source: Telemetry Log Changed]
          ↓
[Extract field: evidence] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `Telemetry Log Changed` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Confirm NVME-BASE-2.4, §5.2.2.1, Figure 155; equal Figure numbers in different documents are different sources.
2. Apply the field/state rule above to the captured raw input.
3. Separate creating 07h data from subsequent reads; the controller decides 08h capture timing. For both, verify generation and distinguish event acknowledgement from payload deletion.
4. Compare the observation with the worked scenario and retain the cited source and target identity.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 155 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §5.2.2.1 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| Rule | Use the Telemetry Log Changed Notice slice: locate 08h from the event and read the log; the event does not contain the diagnostic payload. |
| Boundary | Do not describe RAE=0 as deleting the snapshot or treat the AER as the payload. The event supplies a collection trigger and locator; Get Log Page still retrieves the data. |

**Informative example.** If generation is 2Ah before reading and 2Bh afterward, the chunks cannot be accepted as one consistent capture. Even if it remains 2Ah, an 08h collection must consider the race where another host clears TCDA to zero.

**Common misconception.** Do not describe RAE=0 as deleting the snapshot or treat the AER as the payload. The event supplies a collection trigger and locator; Get Log Page still retrieves the data.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Symptom / correction | Do not describe RAE=0 as deleting the snapshot or treat the AER as the payload. The event supplies a collection trigger and locator; Get Log Page still retrieves the data. |

#### Questions the reader should now answer

1. Which source-specific fields establish the decision?
2. Which capability, target, or state would change the worked result?

**Source field index:** Telemetry Log Changed

**Source keyword index:** shall not, shall, should, may, reserved

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.2.1, Figure 155, printed pages 186-189, PDF pages 212-215

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 156: Asynchronous Event Information - I/O Command Specific Status</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-156-CLAIM figure-table:BASEBTS-BASE-FIG-156 -->

**SPEC.** Figure 156, "Asynchronous Event Information - I/O Command Specific Status": Read Sanitize AEI 01h/02h/03h with SOS/SANS. Entered Media Verification is not completion of the entire operation. Decode the source-specific fields below.

#### Where this Figure fits

Read Sanitize AEI 01h/02h/03h with SOS/SANS. Entered Media Verification is not completion of the entire operation.

The indexed fields below belong to this source document and this Figure. The worked example connects them to the full operation.

#### Teaching redraw

```text
[Locate source: Sanitize Operation Completed]
          ↓
[Extract field: Unexpected Deallocation] → [Apply encoding: Entered Media Verification]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `Sanitize Operation Completed` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `Unexpected Deallocation` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `Entered Media Verification` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Confirm NVME-BASE-2.4, §5.2.2.1, Figure 156; equal Figure numbers in different documents are different sources.
2. Apply the field/state rule above to the captured raw input.
3. Start with the seven states in Figure 772 and attach transition conditions from Figures 773–779. Status describes results, state describes the current position, and events report transitions.
4. Compare the observation with the worked scenario and retain the cited source and target identity.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 156 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §5.2.2.1 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| Rule | Read Sanitize AEI 01h/02h/03h with SOS/SANS. Entered Media Verification is not completion of the entire operation. |
| Boundary | Preserve SCDW10, SOS, SANS, FAILS, MVCNCLD, and event timestamps. Recording only a completion event conflates success, failure, and entry into verification. |

**Informative example.** SPROG=8000h represents 50% of the currently measured phase. Media Verification uses SPROG=FFFFh while SOS can remain 010b; leaving verification for deallocation starts progress again at zero. This is not progress regression.

**Common misconception.** Preserve SCDW10, SOS, SANS, FAILS, MVCNCLD, and event timestamps. Recording only a completion event conflates success, failure, and entry into verification.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Symptom / correction | Preserve SCDW10, SOS, SANS, FAILS, MVCNCLD, and event timestamps. Recording only a completion event conflates success, failure, and entry into verification. |

#### Questions the reader should now answer

1. Which source-specific fields establish the decision?
2. Which capability, target, or state would change the worked result?

**Source field index:** Sanitize Operation Completed, Unexpected Deallocation, Entered Media Verification

**Source keyword index:** shall, should, reserved

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.2.1, Figure 156, printed pages 189-190, PDF pages 215-216

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 187: Firmware Commit - Command Dword 10</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-187-CLAIM figure-table:BASEBTS-BASE-FIG-187 -->

**SPEC.** Figure 187, "Firmware Commit - Command Dword 10": For Boot, use BPID and CA=110b/111b: the former replaces partition contents and the latter changes the active ID. They are separate actions. Decode the source-specific fields below.

#### Where this Figure fits

For Boot, use BPID and CA=110b/111b: the former replaces partition contents and the latter changes the active ID. They are separate actions.

The indexed fields below belong to this source document and this Figure. The worked example connects them to the full operation.

#### Teaching redraw

```text
[Locate source: BPID]
          ↓
[Extract field: CA] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `BPID` | Boot Partition Identifier; selects 0 or 1 independently of the active partition. |
| `CA` | Commit Action, the Firmware Commit field selecting replacement, activation, and reset policy. |

#### Read in this order

1. Confirm NVME-BASE-2.4, §5.2.9, Figure 187; equal Figure numbers in different documents are different sources.
2. Apply the field/state rule above to the captured raw input.
3. Track image transfer, partition contents, active selection, and write protection separately. Successful download has not yet written a Boot Partition, and a successful write has not automatically activated it.
4. Compare the observation with the worked scenario and retain the cited source and target identity.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 187 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §5.2.9 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| Rule | For Boot, use BPID and CA=110b/111b: the former replaces partition contents and the latter changes the active ID. They are separate actions. |
| Boundary | The same reset test has different expected results for the two mechanisms. Preserve the power-cycle/reset type so that relocking can be classified as expected behavior or a defect. |

**Informative example.** To leave BP0 unchanged and unlock BP1, FID 85h CDW11 is (001b << 3) | 000b = 08h. A subsequent Get does not return 000b for BP0; it returns its actual state, or 100b when RPMB owns protection.

**Common misconception.** The same reset test has different expected results for the two mechanisms. Preserve the power-cycle/reset type so that relocking can be classified as expected behavior or a defect.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Symptom / correction | The same reset test has different expected results for the two mechanisms. Preserve the power-cycle/reset type so that relocking can be classified as expected behavior or a defect. |

#### Questions the reader should now answer

1. Which source-specific fields establish the decision?
2. Which capability, target, or state would change the worked result?

**Source field index:** BPID, CA

**Source keyword index:** shall, may, reserved

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.9, Figure 187, printed pages 203, PDF pages 229

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 188: Firmware Commit - Completion Queue Entry Dword 0</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-188-CLAIM figure-table:BASEBTS-BASE-FIG-188 -->

**SPEC.** Figure 188, "Firmware Commit - Completion Queue Entry Dword 0": MUD supplies completion evidence for overlapping updates; the single-controller/endpoint image-sequence boundary still applies. Decode the source-specific fields below.

#### Where this Figure fits

MUD supplies completion evidence for overlapping updates; the single-controller/endpoint image-sequence boundary still applies.

The indexed fields below belong to this source document and this Figure. The worked example connects them to the full operation.

#### Teaching redraw

```text
[Locate source: MUD]
          ↓
[Extract field: evidence] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `MUD` | Multiple Update Detected, the completion bit indicating detection of overlapping firmware-update sequences. |

#### Read in this order

1. Confirm NVME-BASE-2.4, §5.2.9.1, Figure 188; equal Figure numbers in different documents are different sources.
2. Apply the field/state rule above to the captured raw input.
3. Track image transfer, partition contents, active selection, and write protection separately. Successful download has not yet written a Boot Partition, and a successful write has not automatically activated it.
4. Compare the observation with the worked scenario and retain the cited source and target identity.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 188 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §5.2.9.1 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| Rule | MUD supplies completion evidence for overlapping updates; the single-controller/endpoint image-sequence boundary still applies. |
| Boundary | The same reset test has different expected results for the two mechanisms. Preserve the power-cycle/reset type so that relocking can be classified as expected behavior or a defect. |

**Informative example.** To leave BP0 unchanged and unlock BP1, FID 85h CDW11 is (001b << 3) | 000b = 08h. A subsequent Get does not return 000b for BP0; it returns its actual state, or 100b when RPMB owns protection.

**Common misconception.** The same reset test has different expected results for the two mechanisms. Preserve the power-cycle/reset type so that relocking can be classified as expected behavior or a defect.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Symptom / correction | The same reset test has different expected results for the two mechanisms. Preserve the power-cycle/reset type so that relocking can be classified as expected behavior or a defect. |

#### Questions the reader should now answer

1. Which source-specific fields establish the decision?
2. Which capability, target, or state would change the worked result?

**Source field index:** MUD

**Source keyword index:** shall, should, may, reserved

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.9.1, Figure 188, printed pages 204, PDF pages 230

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 189: Firmware Commit - Command Specific Status Values</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-189-CLAIM figure-table:BASEBTS-BASE-FIG-189 -->

**SPEC.** Figure 189, "Firmware Commit - Command Specific Status Values": Boot Partition Write Prohibited points to protection state; Invalid Firmware Image points to image/sequence validation. Classify status before choosing a retry step. Decode the source-specific fields below.

#### Where this Figure fits

Boot Partition Write Prohibited points to protection state; Invalid Firmware Image points to image/sequence validation. Classify status before choosing a retry step.

The indexed fields below belong to this source document and this Figure. The worked example connects them to the full operation.

#### Teaching redraw

```text
[Locate source: Boot Partition Write Prohibited]
          ↓
[Extract field: Invalid Firmware Image] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `Boot Partition Write Prohibited` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `Invalid Firmware Image` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Confirm NVME-BASE-2.4, §5.2.9.1, Figure 189; equal Figure numbers in different documents are different sources.
2. Apply the field/state rule above to the captured raw input.
3. Track image transfer, partition contents, active selection, and write protection separately. Successful download has not yet written a Boot Partition, and a successful write has not automatically activated it.
4. Compare the observation with the worked scenario and retain the cited source and target identity.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 189 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §5.2.9.1 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| Rule | Boot Partition Write Prohibited points to protection state; Invalid Firmware Image points to image/sequence validation. Classify status before choosing a retry step. |
| Boundary | The same reset test has different expected results for the two mechanisms. Preserve the power-cycle/reset type so that relocking can be classified as expected behavior or a defect. |

**Informative example.** To leave BP0 unchanged and unlock BP1, FID 85h CDW11 is (001b << 3) | 000b = 08h. A subsequent Get does not return 000b for BP0; it returns its actual state, or 100b when RPMB owns protection.

**Common misconception.** The same reset test has different expected results for the two mechanisms. Preserve the power-cycle/reset type so that relocking can be classified as expected behavior or a defect.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Symptom / correction | The same reset test has different expected results for the two mechanisms. Preserve the power-cycle/reset type so that relocking can be classified as expected behavior or a defect. |

#### Questions the reader should now answer

1. Which source-specific fields establish the decision?
2. Which capability, target, or state would change the worked result?

**Source field index:** Boot Partition Write Prohibited, Invalid Firmware Image

**Source keyword index:** should not, shall, should, may, reserved

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.9.1, Figure 189, printed pages 204-205, PDF pages 230-231

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 190: Firmware Image Download - Data Pointer</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-190-CLAIM figure-table:BASEBTS-BASE-FIG-190 -->

**SPEC.** Figure 190, "Firmware Image Download - Data Pointer": Download DPTR identifies the host buffer for this image portion, not the destination Boot Partition address. Decode the source-specific fields below.

#### Where this Figure fits

Download DPTR identifies the host buffer for this image portion, not the destination Boot Partition address.

The indexed fields below belong to this source document and this Figure. The worked example connects them to the full operation.

#### Teaching redraw

```text
[Locate source: DPTR]
          ↓
[Extract field: evidence] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `DPTR` | Data Pointer, the SQE field identifying a command data buffer. |

#### Read in this order

1. Confirm NVME-BASE-2.4, §5.2.10, Figure 190; equal Figure numbers in different documents are different sources.
2. Apply the field/state rule above to the captured raw input.
3. Track image transfer, partition contents, active selection, and write protection separately. Successful download has not yet written a Boot Partition, and a successful write has not automatically activated it.
4. Compare the observation with the worked scenario and retain the cited source and target identity.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 190 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §5.2.10 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| Rule | Download DPTR identifies the host buffer for this image portion, not the destination Boot Partition address. |
| Boundary | The same reset test has different expected results for the two mechanisms. Preserve the power-cycle/reset type so that relocking can be classified as expected behavior or a defect. |

**Informative example.** To leave BP0 unchanged and unlock BP1, FID 85h CDW11 is (001b << 3) | 000b = 08h. A subsequent Get does not return 000b for BP0; it returns its actual state, or 100b when RPMB owns protection.

**Common misconception.** The same reset test has different expected results for the two mechanisms. Preserve the power-cycle/reset type so that relocking can be classified as expected behavior or a defect.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Symptom / correction | The same reset test has different expected results for the two mechanisms. Preserve the power-cycle/reset type so that relocking can be classified as expected behavior or a defect. |

#### Questions the reader should now answer

1. Which source-specific fields establish the decision?
2. Which capability, target, or state would change the worked result?

**Source field index:** DPTR

**Source keyword index:** should not, shall, should, may, reserved

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.10, Figure 190, printed pages 205, PDF pages 231

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 191: Firmware Image Download - Command Dword 10</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-191-CLAIM figure-table:BASEBTS-BASE-FIG-191 -->

**SPEC.** Figure 191, "Firmware Image Download - Command Dword 10": NUMD is the portion's zero-based dword count: 512 bytes encodes as 127, with Download alignment/granularity requirements checked separately. Decode the source-specific fields below.

#### Where this Figure fits

NUMD is the portion's zero-based dword count: 512 bytes encodes as 127, with Download alignment/granularity requirements checked separately.

The indexed fields below belong to this source document and this Figure. The worked example connects them to the full operation.

#### Teaching redraw

```text
[Locate source: NUMD]
          ↓
[Extract field: evidence] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `NUMD` | Number of Dwords, a zero-based transfer-dword count; actual bytes = (NUMD + 1) × 4. |

#### Read in this order

1. Confirm NVME-BASE-2.4, §5.2.10, Figure 191; equal Figure numbers in different documents are different sources.
2. Apply the field/state rule above to the captured raw input.
3. Track image transfer, partition contents, active selection, and write protection separately. Successful download has not yet written a Boot Partition, and a successful write has not automatically activated it.
4. Compare the observation with the worked scenario and retain the cited source and target identity.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 191 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §5.2.10 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| Rule | NUMD is the portion's zero-based dword count: 512 bytes encodes as 127, with Download alignment/granularity requirements checked separately. |
| Boundary | The same reset test has different expected results for the two mechanisms. Preserve the power-cycle/reset type so that relocking can be classified as expected behavior or a defect. |

**Informative example.** To leave BP0 unchanged and unlock BP1, FID 85h CDW11 is (001b << 3) | 000b = 08h. A subsequent Get does not return 000b for BP0; it returns its actual state, or 100b when RPMB owns protection.

**Common misconception.** The same reset test has different expected results for the two mechanisms. Preserve the power-cycle/reset type so that relocking can be classified as expected behavior or a defect.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Symptom / correction | The same reset test has different expected results for the two mechanisms. Preserve the power-cycle/reset type so that relocking can be classified as expected behavior or a defect. |

#### Questions the reader should now answer

1. Which source-specific fields establish the decision?
2. Which capability, target, or state would change the worked result?

**Source field index:** NUMD

**Source keyword index:** should not, shall, should, may, reserved

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.10, Figure 191, printed pages 205, PDF pages 231

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 192: Firmware Image Download - Command Dword 11</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-192-CLAIM figure-table:BASEBTS-BASE-FIG-192 -->

**SPEC.** Figure 192, "Firmware Image Download - Command Dword 11": OFST is an image offset in dwords. Boot images are sent in order from the beginning; do not borrow other ordering assumptions for ordinary firmware portions. Decode the source-specific fields below.

#### Where this Figure fits

OFST is an image offset in dwords. Boot images are sent in order from the beginning; do not borrow other ordering assumptions for ordinary firmware portions.

The indexed fields below belong to this source document and this Figure. The worked example connects them to the full operation.

#### Teaching redraw

```text
[Locate source: OFST]
          ↓
[Extract field: evidence] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `OFST` | Offset, the dword-based image-relative offset in Firmware Image Download. |

#### Read in this order

1. Confirm NVME-BASE-2.4, §5.2.10, Figure 192; equal Figure numbers in different documents are different sources.
2. Apply the field/state rule above to the captured raw input.
3. Track image transfer, partition contents, active selection, and write protection separately. Successful download has not yet written a Boot Partition, and a successful write has not automatically activated it.
4. Compare the observation with the worked scenario and retain the cited source and target identity.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 192 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §5.2.10 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| Rule | OFST is an image offset in dwords. Boot images are sent in order from the beginning; do not borrow other ordering assumptions for ordinary firmware portions. |
| Boundary | The same reset test has different expected results for the two mechanisms. Preserve the power-cycle/reset type so that relocking can be classified as expected behavior or a defect. |

**Informative example.** To leave BP0 unchanged and unlock BP1, FID 85h CDW11 is (001b << 3) | 000b = 08h. A subsequent Get does not return 000b for BP0; it returns its actual state, or 100b when RPMB owns protection.

**Common misconception.** The same reset test has different expected results for the two mechanisms. Preserve the power-cycle/reset type so that relocking can be classified as expected behavior or a defect.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Symptom / correction | The same reset test has different expected results for the two mechanisms. Preserve the power-cycle/reset type so that relocking can be classified as expected behavior or a defect. |

#### Questions the reader should now answer

1. Which source-specific fields establish the decision?
2. Which capability, target, or state would change the worked result?

**Source field index:** OFST

**Source keyword index:** shall not, shall, may

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.10, Figure 192, printed pages 206, PDF pages 232

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 193: Firmware Image Download - Command Specific Status Values</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-193-CLAIM figure-table:BASEBTS-BASE-FIG-193 -->

**SPEC.** Figure 193, "Firmware Image Download - Command Specific Status Values": Overlapping Range reports overlapping download portions; preserve each offset and length to reconstruct the offending range. Decode the source-specific fields below.

#### Where this Figure fits

Overlapping Range reports overlapping download portions; preserve each offset and length to reconstruct the offending range.

The indexed fields below belong to this source document and this Figure. The worked example connects them to the full operation.

#### Teaching redraw

```text
[Locate source: Overlapping Range]
          ↓
[Extract field: evidence] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `Overlapping Range` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Confirm NVME-BASE-2.4, §5.2.10, Figure 193; equal Figure numbers in different documents are different sources.
2. Apply the field/state rule above to the captured raw input.
3. Track image transfer, partition contents, active selection, and write protection separately. Successful download has not yet written a Boot Partition, and a successful write has not automatically activated it.
4. Compare the observation with the worked scenario and retain the cited source and target identity.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 193 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §5.2.10 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| Rule | Overlapping Range reports overlapping download portions; preserve each offset and length to reconstruct the offending range. |
| Boundary | The same reset test has different expected results for the two mechanisms. Preserve the power-cycle/reset type so that relocking can be classified as expected behavior or a defect. |

**Informative example.** To leave BP0 unchanged and unlock BP1, FID 85h CDW11 is (001b << 3) | 000b = 08h. A subsequent Get does not return 000b for BP0; it returns its actual state, or 100b when RPMB owns protection.

**Common misconception.** The same reset test has different expected results for the two mechanisms. Preserve the power-cycle/reset type so that relocking can be classified as expected behavior or a defect.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Symptom / correction | The same reset test has different expected results for the two mechanisms. Preserve the power-cycle/reset type so that relocking can be classified as expected behavior or a defect. |

#### Questions the reader should now answer

1. Which source-specific fields establish the decision?
2. Which capability, target, or state would change the worked result?

**Source field index:** Overlapping Range

**Source keyword index:** shall not, shall, may

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.10, Figure 193, printed pages 206, PDF pages 232

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 198: Get Features - Command Dword 10</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-198-CLAIM figure-table:BASEBTS-BASE-FIG-198 -->

**SPEC.** Figure 198, "Get Features - Command Dword 10": Get Features uses FID for the feature and SEL for current/default/saved/capabilities. Do not confuse values for FID 85h/17h with their capabilities. Decode the source-specific fields below.

#### Where this Figure fits

Get Features uses FID for the feature and SEL for current/default/saved/capabilities. Do not confuse values for FID 85h/17h with their capabilities.

The indexed fields below belong to this source document and this Figure. The worked example connects them to the full operation.

#### Teaching redraw

```text
[Locate source: FID]
          ↓
[Extract field: SEL] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `FID` | Feature Identifier, the eight-bit identifier selecting a function in Get/Set Features. |
| `SEL` | Select, the Get Features field choosing current, default, saved, or supported-capabilities view. |

#### Read in this order

1. Confirm NVME-BASE-2.4, §5.2.12, Figure 198; equal Figure numbers in different documents are different sources.
2. Apply the field/state rule above to the captured raw input.
3. Track image transfer, partition contents, active selection, and write protection separately. Successful download has not yet written a Boot Partition, and a successful write has not automatically activated it.
4. Compare the observation with the worked scenario and retain the cited source and target identity.

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
| Rule | Get Features uses FID for the feature and SEL for current/default/saved/capabilities. Do not confuse values for FID 85h/17h with their capabilities. |
| Boundary | The same reset test has different expected results for the two mechanisms. Preserve the power-cycle/reset type so that relocking can be classified as expected behavior or a defect. |

**Informative example.** To leave BP0 unchanged and unlock BP1, FID 85h CDW11 is (001b << 3) | 000b = 08h. A subsequent Get does not return 000b for BP0; it returns its actual state, or 100b when RPMB owns protection.

**Common misconception.** The same reset test has different expected results for the two mechanisms. Preserve the power-cycle/reset type so that relocking can be classified as expected behavior or a defect.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Symptom / correction | The same reset test has different expected results for the two mechanisms. Preserve the power-cycle/reset type so that relocking can be classified as expected behavior or a defect. |

#### Questions the reader should now answer

1. Which source-specific fields establish the decision?
2. Which capability, target, or state would change the worked result?

**Source field index:** FID, SEL

**Source keyword index:** shall, may, optional, reserved

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.12, Figure 198, printed pages 209-210, PDF pages 235-236

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 199: Get Features - Command Dword 14</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-199-CLAIM figure-table:BASEBTS-BASE-FIG-199 -->

**SPEC.** Figure 199, "Get Features - Command Dword 14": The CDW14 UUID Index belongs to the common Feature interface; these standard FIDs do not call for invented vendor-UUID mappings. Decode the source-specific fields below.

#### Where this Figure fits

The CDW14 UUID Index belongs to the common Feature interface; these standard FIDs do not call for invented vendor-UUID mappings.

The indexed fields below belong to this source document and this Figure. The worked example connects them to the full operation.

#### Teaching redraw

```text
[Locate source: UUID Index]
          ↓
[Extract field: evidence] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `UUID Index` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Confirm NVME-BASE-2.4, §5.2.12, Figure 199; equal Figure numbers in different documents are different sources.
2. Apply the field/state rule above to the captured raw input.
3. Track image transfer, partition contents, active selection, and write protection separately. Successful download has not yet written a Boot Partition, and a successful write has not automatically activated it.
4. Compare the observation with the worked scenario and retain the cited source and target identity.

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
| Rule | The CDW14 UUID Index belongs to the common Feature interface; these standard FIDs do not call for invented vendor-UUID mappings. |
| Boundary | The same reset test has different expected results for the two mechanisms. Preserve the power-cycle/reset type so that relocking can be classified as expected behavior or a defect. |

**Informative example.** To leave BP0 unchanged and unlock BP1, FID 85h CDW11 is (001b << 3) | 000b = 08h. A subsequent Get does not return 000b for BP0; it returns its actual state, or 100b when RPMB owns protection.

**Common misconception.** The same reset test has different expected results for the two mechanisms. Preserve the power-cycle/reset type so that relocking can be classified as expected behavior or a defect.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Symptom / correction | The same reset test has different expected results for the two mechanisms. Preserve the power-cycle/reset type so that relocking can be classified as expected behavior or a defect. |

#### Questions the reader should now answer

1. Which source-specific fields establish the decision?
2. Which capability, target, or state would change the worked result?

**Source field index:** UUID Index

**Source keyword index:** shall, may, optional, reserved

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.12, Figure 199, printed pages 210, PDF pages 236

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 201: Completion Queue Entry Dword 0 when Select is set to 11b</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-201-CLAIM figure-table:BASEBTS-BASE-FIG-201 -->

**SPEC.** Figure 201, "Completion Queue Entry Dword 0 when Select is set to 11b": For SEL=011b, bits 2/1/0 report changeable/namespace-specific/saveable, not current BP0WPS or NODRM values. Decode the source-specific fields below.

#### Where this Figure fits

For SEL=011b, bits 2/1/0 report changeable/namespace-specific/saveable, not current BP0WPS or NODRM values.

The indexed fields below belong to this source document and this Figure. The worked example connects them to the full operation.

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

1. Confirm NVME-BASE-2.4, §5.2.12.2, Figure 201; equal Figure numbers in different documents are different sources.
2. Apply the field/state rule above to the captured raw input.
3. Track image transfer, partition contents, active selection, and write protection separately. Successful download has not yet written a Boot Partition, and a successful write has not automatically activated it.
4. Compare the observation with the worked scenario and retain the cited source and target identity.

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
| Rule | For SEL=011b, bits 2/1/0 report changeable/namespace-specific/saveable, not current BP0WPS or NODRM values. |
| Boundary | The same reset test has different expected results for the two mechanisms. Preserve the power-cycle/reset type so that relocking can be classified as expected behavior or a defect. |

**Informative example.** To leave BP0 unchanged and unlock BP1, FID 85h CDW11 is (001b << 3) | 000b = 08h. A subsequent Get does not return 000b for BP0; it returns its actual state, or 100b when RPMB owns protection.

**Common misconception.** The same reset test has different expected results for the two mechanisms. Preserve the power-cycle/reset type so that relocking can be classified as expected behavior or a defect.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Symptom / correction | The same reset test has different expected results for the two mechanisms. Preserve the power-cycle/reset type so that relocking can be classified as expected behavior or a defect. |

#### Questions the reader should now answer

1. Which source-specific fields establish the decision?
2. Which capability, target, or state would change the worked result?

**Source field index:** CHANG, NSSPEC, SVBL

**Source keyword index:** may, reserved

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.12.2, Figure 201, printed pages 212, PDF pages 238

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 203: Get Log Page - Data Pointer</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-203-CLAIM figure-table:BASEBTS-BASE-FIG-203 -->

**SPEC.** Figure 203, "Get Log Page - Data Pointer": Get Log Page's data pointer identifies a receive buffer large enough for the encoded NUMD request. Decode the source-specific fields below.

#### Where this Figure fits

Get Log Page's data pointer identifies a receive buffer large enough for the encoded NUMD request.

The indexed fields below belong to this source document and this Figure. The worked example connects them to the full operation.

#### Teaching redraw

```text
[Locate source: DPTR]
          ↓
[Extract field: evidence] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `DPTR` | Data Pointer, the SQE field identifying a command data buffer. |

#### Read in this order

1. Confirm NVME-BASE-2.4, §5.2.13, Figure 203; equal Figure numbers in different documents are different sources.
2. Apply the field/state rule above to the captured raw input.
3. Areas are differently sized views starting at the same block 1. Decode the header, select the final applicable populated area, and do not add the three Last Block numbers.
4. Compare the observation with the worked scenario and retain the cited source and target identity.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 203 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §5.2.13 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| Rule | Get Log Page's data pointer identifies a receive buffer large enough for the encoded NUMD request. |
| Boundary | THS in LID 07h and TCS in LID 08h have different offsets; do not reuse one header layout for the other. Snapshot payload is vendor-defined, so unknown bytes cannot be assigned invented diagnostic fields. |

**Informative example.** For Last Blocks=65/1000/30000, Area 3 payload is 30000×512=15360000 bytes and the log including its header is 15360512 bytes. Values 0/1000/1000 mean Area 1 is empty and Area 3 adds no content beyond Area 2.

**Common misconception.** THS in LID 07h and TCS in LID 08h have different offsets; do not reuse one header layout for the other. Snapshot payload is vendor-defined, so unknown bytes cannot be assigned invented diagnostic fields.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Symptom / correction | THS in LID 07h and TCS in LID 08h have different offsets; do not reuse one header layout for the other. Snapshot payload is vendor-defined, so unknown bytes cannot be assigned invented diagnostic fields. |

#### Questions the reader should now answer

1. Which source-specific fields establish the decision?
2. Which capability, target, or state would change the worked result?

**Source field index:** DPTR

**Source keyword index:** shall, should, optional, reserved

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13, Figure 203, printed pages 213, PDF pages 239

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 204: Get Log Page - Command Dword 10</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-204-CLAIM figure-table:BASEBTS-BASE-FIG-204 -->

**SPEC.** Figure 204, "Get Log Page - Command Dword 10": CDW10[7:0]=LID, [14:8]=LSP, [15]=RAE, and [31:16]=NUMDL. LID determines whether LSP means Boot BPID or Telemetry capture controls. Decode the source-specific fields below.

#### Where this Figure fits

CDW10[7:0]=LID, [14:8]=LSP, [15]=RAE, and [31:16]=NUMDL. LID determines whether LSP means Boot BPID or Telemetry capture controls.

The indexed fields below belong to this source document and this Figure. The worked example connects them to the full operation.

#### Teaching redraw

```text
[Locate source: LID]
          ↓
[Extract field: LSP] → [Apply encoding: RAE]
                                      ↓
[Validate evidence: NUMDL]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `LID` | Log Page Identifier, the Get Log Page field selecting a log page. |
| `LSP` | Log Specific Field, a command selector whose meaning is defined by the selected log page. |
| `RAE` | Retain Asynchronous Event; use one during Telemetry collection and zero to acknowledge completion. |
| `NUMDL` | Number of Dwords Lower, the low 16 bits of Get Log Page NUMD. |

#### Read in this order

1. Confirm NVME-BASE-2.4, §5.2.13, Figure 204; equal Figure numbers in different documents are different sources.
2. Apply the field/state rule above to the captured raw input.
3. Separate creating 07h data from subsequent reads; the controller decides 08h capture timing. For both, verify generation and distinguish event acknowledgement from payload deletion.
4. Compare the observation with the worked scenario and retain the cited source and target identity.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 204 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §5.2.13 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| Rule | CDW10[7:0]=LID, [14:8]=LSP, [15]=RAE, and [31:16]=NUMDL. LID determines whether LSP means Boot BPID or Telemetry capture controls. |
| Boundary | Do not describe RAE=0 as deleting the snapshot or treat the AER as the payload. The event supplies a collection trigger and locator; Get Log Page still retrieves the data. |

**Informative example.** If generation is 2Ah before reading and 2Bh afterward, the chunks cannot be accepted as one consistent capture. Even if it remains 2Ah, an 08h collection must consider the race where another host clears TCDA to zero.

**Common misconception.** Do not describe RAE=0 as deleting the snapshot or treat the AER as the payload. The event supplies a collection trigger and locator; Get Log Page still retrieves the data.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Symptom / correction | Do not describe RAE=0 as deleting the snapshot or treat the AER as the payload. The event supplies a collection trigger and locator; Get Log Page still retrieves the data. |

#### Questions the reader should now answer

1. Which source-specific fields establish the decision?
2. Which capability, target, or state would change the worked result?

**Source field index:** LID, LSP, RAE, NUMDL

**Source keyword index:** shall, should, optional, reserved

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13, Figure 204, printed pages 213, PDF pages 239

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 205: Get Log Page - Command Dword 11</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-205-CLAIM figure-table:BASEBTS-BASE-FIG-205 -->

**SPEC.** Figure 205, "Get Log Page - Command Dword 11": NUMDU and NUMDL form the zero-based dword count; LSI is a separate log-specific selector, not LSP. Decode the source-specific fields below.

#### Where this Figure fits

NUMDU and NUMDL form the zero-based dword count; LSI is a separate log-specific selector, not LSP.

The indexed fields below belong to this source document and this Figure. The worked example connects them to the full operation.

#### Teaching redraw

```text
[Locate source: NUMDU]
          ↓
[Extract field: LSI] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `NUMDU` | Number of Dwords Upper, the high 16 bits of Get Log Page NUMD. |
| `LSI` | Log Specific Identifier, an identifier whose meaning is defined by the selected log page. |

#### Read in this order

1. Confirm NVME-BASE-2.4, §5.2.13, Figure 205; equal Figure numbers in different documents are different sources.
2. Apply the field/state rule above to the captured raw input.
3. Areas are differently sized views starting at the same block 1. Decode the header, select the final applicable populated area, and do not add the three Last Block numbers.
4. Compare the observation with the worked scenario and retain the cited source and target identity.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 205 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §5.2.13 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| Rule | NUMDU and NUMDL form the zero-based dword count; LSI is a separate log-specific selector, not LSP. |
| Boundary | THS in LID 07h and TCS in LID 08h have different offsets; do not reuse one header layout for the other. Snapshot payload is vendor-defined, so unknown bytes cannot be assigned invented diagnostic fields. |

**Informative example.** For Last Blocks=65/1000/30000, Area 3 payload is 30000×512=15360000 bytes and the log including its header is 15360512 bytes. Values 0/1000/1000 mean Area 1 is empty and Area 3 adds no content beyond Area 2.

**Common misconception.** THS in LID 07h and TCS in LID 08h have different offsets; do not reuse one header layout for the other. Snapshot payload is vendor-defined, so unknown bytes cannot be assigned invented diagnostic fields.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Symptom / correction | THS in LID 07h and TCS in LID 08h have different offsets; do not reuse one header layout for the other. Snapshot payload is vendor-defined, so unknown bytes cannot be assigned invented diagnostic fields. |

#### Questions the reader should now answer

1. Which source-specific fields establish the decision?
2. Which capability, target, or state would change the worked result?

**Source field index:** NUMDU, LSI

**Source keyword index:** shall, may, reserved

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13, Figure 205, printed pages 214, PDF pages 240

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 206: Get Log Page - Command Dword 12</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-206-CLAIM figure-table:BASEBTS-BASE-FIG-206 -->

**SPEC.** Figure 206, "Get Log Page - Command Dword 12": The low 32 bits of LPO occupy CDW12; Telemetry byte offsets must align to 512-byte blocks. Decode the source-specific fields below.

#### Where this Figure fits

The low 32 bits of LPO occupy CDW12; Telemetry byte offsets must align to 512-byte blocks.

The indexed fields below belong to this source document and this Figure. The worked example connects them to the full operation.

#### Teaching redraw

```text
[Locate source: LPOL]
          ↓
[Extract field: evidence] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `LPOL` | Log Page Offset Lower, the low 32 bits of the Get Log Page byte offset. |

#### Read in this order

1. Confirm NVME-BASE-2.4, §5.2.13, Figure 206; equal Figure numbers in different documents are different sources.
2. Apply the field/state rule above to the captured raw input.
3. Areas are differently sized views starting at the same block 1. Decode the header, select the final applicable populated area, and do not add the three Last Block numbers.
4. Compare the observation with the worked scenario and retain the cited source and target identity.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 206 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §5.2.13 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| Rule | The low 32 bits of LPO occupy CDW12; Telemetry byte offsets must align to 512-byte blocks. |
| Boundary | THS in LID 07h and TCS in LID 08h have different offsets; do not reuse one header layout for the other. Snapshot payload is vendor-defined, so unknown bytes cannot be assigned invented diagnostic fields. |

**Informative example.** For Last Blocks=65/1000/30000, Area 3 payload is 30000×512=15360000 bytes and the log including its header is 15360512 bytes. Values 0/1000/1000 mean Area 1 is empty and Area 3 adds no content beyond Area 2.

**Common misconception.** THS in LID 07h and TCS in LID 08h have different offsets; do not reuse one header layout for the other. Snapshot payload is vendor-defined, so unknown bytes cannot be assigned invented diagnostic fields.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Symptom / correction | THS in LID 07h and TCS in LID 08h have different offsets; do not reuse one header layout for the other. Snapshot payload is vendor-defined, so unknown bytes cannot be assigned invented diagnostic fields. |

#### Questions the reader should now answer

1. Which source-specific fields establish the decision?
2. Which capability, target, or state would change the worked result?

**Source field index:** LPOL

**Source keyword index:** shall, may, reserved

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13, Figure 206, printed pages 214, PDF pages 240

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 207: Get Log Page - Command Dword 13</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-207-CLAIM figure-table:BASEBTS-BASE-FIG-207 -->

**SPEC.** Figure 207, "Get Log Page - Command Dword 13": The high 32 bits of LPO occupy CDW13; do not truncate a large-log offset to 32 bits before computing it. Decode the source-specific fields below.

#### Where this Figure fits

The high 32 bits of LPO occupy CDW13; do not truncate a large-log offset to 32 bits before computing it.

The indexed fields below belong to this source document and this Figure. The worked example connects them to the full operation.

#### Teaching redraw

```text
[Locate source: LPOU]
          ↓
[Extract field: evidence] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `LPOU` | Log Page Offset Upper, the high 32 bits of the Get Log Page byte offset. |

#### Read in this order

1. Confirm NVME-BASE-2.4, §5.2.13, Figure 207; equal Figure numbers in different documents are different sources.
2. Apply the field/state rule above to the captured raw input.
3. Areas are differently sized views starting at the same block 1. Decode the header, select the final applicable populated area, and do not add the three Last Block numbers.
4. Compare the observation with the worked scenario and retain the cited source and target identity.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 207 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §5.2.13 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| Rule | The high 32 bits of LPO occupy CDW13; do not truncate a large-log offset to 32 bits before computing it. |
| Boundary | THS in LID 07h and TCS in LID 08h have different offsets; do not reuse one header layout for the other. Snapshot payload is vendor-defined, so unknown bytes cannot be assigned invented diagnostic fields. |

**Informative example.** For Last Blocks=65/1000/30000, Area 3 payload is 30000×512=15360000 bytes and the log including its header is 15360512 bytes. Values 0/1000/1000 mean Area 1 is empty and Area 3 adds no content beyond Area 2.

**Common misconception.** THS in LID 07h and TCS in LID 08h have different offsets; do not reuse one header layout for the other. Snapshot payload is vendor-defined, so unknown bytes cannot be assigned invented diagnostic fields.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Symptom / correction | THS in LID 07h and TCS in LID 08h have different offsets; do not reuse one header layout for the other. Snapshot payload is vendor-defined, so unknown bytes cannot be assigned invented diagnostic fields. |

#### Questions the reader should now answer

1. Which source-specific fields establish the decision?
2. Which capability, target, or state would change the worked result?

**Source field index:** LPOU

**Source keyword index:** shall, may, reserved

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13, Figure 207, printed pages 214, PDF pages 240

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 208: Get Log Page - Command Dword 14</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-208-CLAIM figure-table:BASEBTS-BASE-FIG-208 -->

**SPEC.** Figure 208, "Get Log Page - Command Dword 14": CSI/OT/UUID Index in CDW14 provide common decoding context. Apply the LID's offset semantics rather than mistaking a byte offset for an index. Decode the source-specific fields below.

#### Where this Figure fits

CSI/OT/UUID Index in CDW14 provide common decoding context. Apply the LID's offset semantics rather than mistaking a byte offset for an index.

The indexed fields below belong to this source document and this Figure. The worked example connects them to the full operation.

#### Teaching redraw

```text
[Locate source: CSI]
          ↓
[Extract field: OT] → [Apply encoding: UUID Index]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `CSI` | Command Set Identifier, selecting the I/O Command Set context for a command or log page. |
| `OT` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `UUID Index` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Confirm NVME-BASE-2.4, §5.2.13, Figure 208; equal Figure numbers in different documents are different sources.
2. Apply the field/state rule above to the captured raw input.
3. Areas are differently sized views starting at the same block 1. Decode the header, select the final applicable populated area, and do not add the three Last Block numbers.
4. Compare the observation with the worked scenario and retain the cited source and target identity.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 208 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §5.2.13 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| Rule | CSI/OT/UUID Index in CDW14 provide common decoding context. Apply the LID's offset semantics rather than mistaking a byte offset for an index. |
| Boundary | THS in LID 07h and TCS in LID 08h have different offsets; do not reuse one header layout for the other. Snapshot payload is vendor-defined, so unknown bytes cannot be assigned invented diagnostic fields. |

**Informative example.** For Last Blocks=65/1000/30000, Area 3 payload is 30000×512=15360000 bytes and the log including its header is 15360512 bytes. Values 0/1000/1000 mean Area 1 is empty and Area 3 adds no content beyond Area 2.

**Common misconception.** THS in LID 07h and TCS in LID 08h have different offsets; do not reuse one header layout for the other. Snapshot payload is vendor-defined, so unknown bytes cannot be assigned invented diagnostic fields.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Symptom / correction | THS in LID 07h and TCS in LID 08h have different offsets; do not reuse one header layout for the other. Snapshot payload is vendor-defined, so unknown bytes cannot be assigned invented diagnostic fields. |

#### Questions the reader should now answer

1. Which source-specific fields establish the decision?
2. Which capability, target, or state would change the worked result?

**Source field index:** CSI, OT, UUID Index

**Source keyword index:** shall, may, reserved

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13, Figure 208, printed pages 214-215, PDF pages 240-241

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 209: Get Log Page - Log Page Identifiers</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-209-CLAIM figure-table:BASEBTS-BASE-FIG-209 -->

**SPEC.** Figure 209, "Get Log Page - Log Page Identifiers": Use only the 07h, 08h, 15h, and 81h rows, connecting each ID to its section without extending into other logs. Decode the source-specific fields below.

#### Where this Figure fits

Use only the 07h, 08h, 15h, and 81h rows, connecting each ID to its section without extending into other logs.

The indexed fields below belong to this source document and this Figure. The worked example connects them to the full operation.

#### Teaching redraw

```text
[Locate source: LID 07h]
          ↓
[Extract field: LID 08h] → [Apply encoding: LID 15h]
                                      ↓
[Validate evidence: LID 81h]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `LID 07h` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `LID 08h` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `LID 15h` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `LID 81h` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Confirm NVME-BASE-2.4, §5.2.13, Figure 209; equal Figure numbers in different documents are different sources.
2. Apply the field/state rule above to the captured raw input.
3. Areas are differently sized views starting at the same block 1. Decode the header, select the final applicable populated area, and do not add the three Last Block numbers.
4. Compare the observation with the worked scenario and retain the cited source and target identity.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 209 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §5.2.13 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| Rule | Use only the 07h, 08h, 15h, and 81h rows, connecting each ID to its section without extending into other logs. |
| Boundary | THS in LID 07h and TCS in LID 08h have different offsets; do not reuse one header layout for the other. Snapshot payload is vendor-defined, so unknown bytes cannot be assigned invented diagnostic fields. |

**Informative example.** For Last Blocks=65/1000/30000, Area 3 payload is 30000×512=15360000 bytes and the log including its header is 15360512 bytes. Values 0/1000/1000 mean Area 1 is empty and Area 3 adds no content beyond Area 2.

**Common misconception.** THS in LID 07h and TCS in LID 08h have different offsets; do not reuse one header layout for the other. Snapshot payload is vendor-defined, so unknown bytes cannot be assigned invented diagnostic fields.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Symptom / correction | THS in LID 07h and TCS in LID 08h have different offsets; do not reuse one header layout for the other. Snapshot payload is vendor-defined, so unknown bytes cannot be assigned invented diagnostic fields. |

#### Questions the reader should now answer

1. Which source-specific fields establish the decision?
2. Which capability, target, or state would change the worked result?

**Source field index:** LID 07h, LID 08h, LID 15h, LID 81h

**Source keyword index:** may, optional, reserved

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13, Figure 209, printed pages 215-216, PDF pages 241-242

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 210: Supported Log Pages Log Page</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-210-CLAIM figure-table:BASEBTS-BASE-FIG-210 -->

**SPEC.** Figure 210, "Supported Log Pages Log Page": Supported Log Pages provides a descriptor per LID; the 07h descriptor is the lookup point for MCDAS. Decode the source-specific fields below.

#### Where this Figure fits

Supported Log Pages provides a descriptor per LID; the 07h descriptor is the lookup point for MCDAS.

The indexed fields below belong to this source document and this Figure. The worked example connects them to the full operation.

#### Teaching redraw

```text
[Locate source: Supported Log Pages]
          ↓
[Extract field: LID Support and Effects] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `Supported Log Pages` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `LID Support and Effects` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Confirm NVME-BASE-2.4, §5.2.13.1.1, Figure 210; equal Figure numbers in different documents are different sources.
2. Apply the field/state rule above to the captured raw input.
3. Separate creating 07h data from subsequent reads; the controller decides 08h capture timing. For both, verify generation and distinguish event acknowledgement from payload deletion.
4. Compare the observation with the worked scenario and retain the cited source and target identity.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 210 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §5.2.13.1.1 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| Rule | Supported Log Pages provides a descriptor per LID; the 07h descriptor is the lookup point for MCDAS. |
| Boundary | Do not describe RAE=0 as deleting the snapshot or treat the AER as the payload. The event supplies a collection trigger and locator; Get Log Page still retrieves the data. |

**Informative example.** If generation is 2Ah before reading and 2Bh afterward, the chunks cannot be accepted as one consistent capture. Even if it remains 2Ah, an 08h collection must consider the race where another host clears TCDA to zero.

**Common misconception.** Do not describe RAE=0 as deleting the snapshot or treat the AER as the payload. The event supplies a collection trigger and locator; Get Log Page still retrieves the data.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Symptom / correction | Do not describe RAE=0 as deleting the snapshot or treat the AER as the payload. The event supplies a collection trigger and locator; Get Log Page still retrieves the data. |

#### Questions the reader should now answer

1. Which source-specific fields establish the decision?
2. Which capability, target, or state would change the worked result?

**Source field index:** Supported Log Pages, LID Support and Effects

**Source keyword index:** shall, may, reserved

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.1, Figure 210, printed pages 217, PDF pages 243

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 211: LID Supported and Effects Data Structure</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-211-CLAIM figure-table:BASEBTS-BASE-FIG-211 -->

**SPEC.** Figure 211, "LID Supported and Effects Data Structure": Check LSUPP before decoding that LID's specific parameter. MCDAS bit 0 belongs to this parameter, not to CTHID. Decode the source-specific fields below.

#### Where this Figure fits

Check LSUPP before decoding that LID's specific parameter. MCDAS bit 0 belongs to this parameter, not to CTHID.

The indexed fields below belong to this source document and this Figure. The worked example connects them to the full operation.

#### Teaching redraw

```text
[Locate source: LSUPP]
          ↓
[Extract field: LID Specific Parameter] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `LSUPP` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `LID Specific Parameter` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Confirm NVME-BASE-2.4, §5.2.13.1.1, Figure 211; equal Figure numbers in different documents are different sources.
2. Apply the field/state rule above to the captured raw input.
3. Separate creating 07h data from subsequent reads; the controller decides 08h capture timing. For both, verify generation and distinguish event acknowledgement from payload deletion.
4. Compare the observation with the worked scenario and retain the cited source and target identity.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 211 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §5.2.13.1.1 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| Rule | Check LSUPP before decoding that LID's specific parameter. MCDAS bit 0 belongs to this parameter, not to CTHID. |
| Boundary | Do not describe RAE=0 as deleting the snapshot or treat the AER as the payload. The event supplies a collection trigger and locator; Get Log Page still retrieves the data. |

**Informative example.** If generation is 2Ah before reading and 2Bh afterward, the chunks cannot be accepted as one consistent capture. Even if it remains 2Ah, an 08h collection must consider the race where another host clears TCDA to zero.

**Common misconception.** Do not describe RAE=0 as deleting the snapshot or treat the AER as the payload. The event supplies a collection trigger and locator; Get Log Page still retrieves the data.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Symptom / correction | Do not describe RAE=0 as deleting the snapshot or treat the AER as the payload. The event supplies a collection trigger and locator; Get Log Page still retrieves the data. |

#### Questions the reader should now answer

1. Which source-specific fields establish the decision?
2. Which capability, target, or state would change the worked result?

**Source field index:** LSUPP, LID Specific Parameter

**Source keyword index:** shall, should, may, reserved

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.1, Figure 211, printed pages 217-218, PDF pages 243-244

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 311: Reservation Notification Log Page</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-311-CLAIM figure-table:BASEBTS-BASE-FIG-311 -->

**SPEC.** Figure 311, "Reservation Notification Log Page": This Reservation Notification structure reports notification counts/types and does not contain SPROG. The reference in 8.1.27.4.2 appears misplaced; use Figure 312 for progress. Decode the source-specific fields below.

#### Where this Figure fits

This Reservation Notification structure reports notification counts/types and does not contain SPROG. The reference in 8.1.27.4.2 appears misplaced; use Figure 312 for progress.

The indexed fields below belong to this source document and this Figure. The worked example connects them to the full operation.

#### Teaching redraw

```text
[Locate source: Reservation Notification]
          ↓
[Extract field: Log Page Count] → [Apply encoding: Notification Type]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `Reservation Notification` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `Log Page Count` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `Notification Type` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Confirm NVME-BASE-2.4, §5.2.13.1.37, Figure 311; equal Figure numbers in different documents are different sources.
2. Apply the field/state rule above to the captured raw input.
3. Evaluate the command allowlist and the NVM Read exception separately. Determine target/state, then PI checking and allocation; ordinary-read behavior cannot be applied unchanged to verification.
4. Compare the observation with the worked scenario and retain the cited source and target identity.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 311 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §5.2.13.1.37 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| Rule | This Reservation Notification structure reports notification counts/types and does not contain SPROG. The reference in 8.1.27.4.2 appears misplaced; use Figure 312 for progress. |
| Boundary | Do not assume all Get Log Page requests are permitted during subsystem sanitize; 07h/08h are absent from Figure 144. Namespace sanitize restrictions require a separate attached/target-scope evaluation. |

**Informative example.** A verification read with PRCHK=000b and STC=0, readable allocated LBAs, and no other abort cause completes as Successful Media Verification Read. Requesting PI checking changes the expected branch to Invalid Field in Command.

**Common misconception.** Do not assume all Get Log Page requests are permitted during subsystem sanitize; 07h/08h are absent from Figure 144. Namespace sanitize restrictions require a separate attached/target-scope evaluation.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Symptom / correction | Do not assume all Get Log Page requests are permitted during subsystem sanitize; 07h/08h are absent from Figure 144. Namespace sanitize restrictions require a separate attached/target-scope evaluation. |

#### Questions the reader should now answer

1. Which source-specific fields establish the decision?
2. Which capability, target, or state would change the worked result?

**Source field index:** Reservation Notification, Log Page Count, Notification Type

**Source keyword index:** shall, may, reserved

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.37, Figure 311, printed pages 313, PDF pages 339

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 338: Identify - Identify Controller Data Structure, I/O Command Set Independent</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-338-CLAIM figure-table:BASEBTS-BASE-FIG-338 -->

**SPEC.** Figure 338, "Identify - Identify Controller Data Structure, I/O Command Set Independent": Decode only this report's fields: BPCAP byte 102, LPA byte 261, SANICAP bytes 328–331, and MDS in CTRATT. Check methods, VERS/NVERS, SPRRS, NDI, and NODMMAS separately. Decode the source-specific fields below.

#### Where this Figure fits

Decode only this report's fields: BPCAP byte 102, LPA byte 261, SANICAP bytes 328–331, and MDS in CTRATT. Check methods, VERS/NVERS, SPRRS, NDI, and NODMMAS separately.

The indexed fields below belong to this source document and this Figure. The worked example connects them to the full operation.

#### Teaching redraw

```text
[Locate source: BPCAP]
          ↓
[Extract field: LPA] → [Apply encoding: SANICAP]
                                      ↓
[Validate evidence: CTRATT]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `BPCAP` | Boot Partition Capabilities; identifies the supported combination of Set Features and RPMB protection. |
| `LPA` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `SANICAP` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `CTRATT` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Confirm NVME-BASE-2.4, §5.2.14.2.1, Figure 338; equal Figure numbers in different documents are different sources.
2. Apply the field/state rule above to the captured raw input.
3. Separate advertised capabilities, command requests, and Feature policy. Command acceptance, operation success, and satisfaction of no-deallocate are three outcomes requiring different evidence.
4. Compare the observation with the worked scenario and retain the cited source and target identity.

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
| Rule | Decode only this report's fields: BPCAP byte 102, LPA byte 261, SANICAP bytes 328–331, and MDS in CTRATT. Check methods, VERS/NVERS, SPRRS, NDI, and NODMMAS separately. |
| Boundary | PREQ is bit 4 in Figure 454 but bit 11 in Figure 451. Sharing an untyped builder between the two commands can set reserved bits in the namespace command. |

**Informative example.** SANACT=010b, AUSE=0, EMVS=1, NDAS=0, and PREQ=0 encode CDW10=0402h. It applies only with VERS/Block Erase support and other preconditions satisfied. Separately, OWPASS=0h means 16 passes, not skipping overwrite.

**Common misconception.** PREQ is bit 4 in Figure 454 but bit 11 in Figure 451. Sharing an untyped builder between the two commands can set reserved bits in the namespace command.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Symptom / correction | PREQ is bit 4 in Figure 454 but bit 11 in Figure 451. Sharing an untyped builder between the two commands can set reserved bits in the namespace command. |

#### Questions the reader should now answer

1. Which source-specific fields establish the decision?
2. Which capability, target, or state would change the worked result?

**Source field index:** BPCAP, LPA, SANICAP, CTRATT

**Source keyword index:** shall not, should not, shall, should, may, optional, reserved

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.14.2.1, Figure 338, printed pages 340-382, PDF pages 366-408

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 454: Sanitize Namespace - Command Dword 10</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-454-CLAIM figure-table:BASEBTS-BASE-FIG-454 -->

**SPEC.** Figure 454, "Sanitize Namespace - Command Dword 10": Namespace CDW10 offers Exit Failure/Crypto Erase/Exit Verification, with PREQ at bit 4 and EMVS at bit 10, and no NDAS or Overwrite parameters. Decode the source-specific fields below.

#### Where this Figure fits

Namespace CDW10 offers Exit Failure/Crypto Erase/Exit Verification, with PREQ at bit 4 and EMVS at bit 10, and no NDAS or Overwrite parameters.

The indexed fields below belong to this source document and this Figure. The worked example connects them to the full operation.

#### Teaching redraw

```text
[Locate source: SANACT]
          ↓
[Extract field: AUSE] → [Apply encoding: PREQ]
                                      ↓
[Validate evidence: EMVS]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `SANACT` | Sanitize Action; selects the method, Exit Failure Mode, or Exit Media Verification. |
| `AUSE` | Allow Unrestricted Sanitize Exit; selects whether failure can be exited without a successful retry. |
| `PREQ` | Purge Request; interpreted with SPRRS for purge request/reporting; its bit position differs between the Sanitize commands. |
| `EMVS` | Enter Media Verification State; requests verification after successful processing, subject to method and capability restrictions. |

#### Read in this order

1. Confirm NVME-BASE-2.4, §5.2.27, Figure 454; equal Figure numbers in different documents are different sources.
2. Apply the field/state rule above to the captured raw input.
3. Separate advertised capabilities, command requests, and Feature policy. Command acceptance, operation success, and satisfaction of no-deallocate are three outcomes requiring different evidence.
4. Compare the observation with the worked scenario and retain the cited source and target identity.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 454 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §5.2.27 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| Rule | Namespace CDW10 offers Exit Failure/Crypto Erase/Exit Verification, with PREQ at bit 4 and EMVS at bit 10, and no NDAS or Overwrite parameters. |
| Boundary | PREQ is bit 4 in Figure 454 but bit 11 in Figure 451. Sharing an untyped builder between the two commands can set reserved bits in the namespace command. |

**Informative example.** SANACT=010b, AUSE=0, EMVS=1, NDAS=0, and PREQ=0 encode CDW10=0402h. It applies only with VERS/Block Erase support and other preconditions satisfied. Separately, OWPASS=0h means 16 passes, not skipping overwrite.

**Common misconception.** PREQ is bit 4 in Figure 454 but bit 11 in Figure 451. Sharing an untyped builder between the two commands can set reserved bits in the namespace command.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Symptom / correction | PREQ is bit 4 in Figure 454 but bit 11 in Figure 451. Sharing an untyped builder between the two commands can set reserved bits in the namespace command. |

#### Questions the reader should now answer

1. Which source-specific fields establish the decision?
2. Which capability, target, or state would change the worked result?

**Source field index:** SANACT, AUSE, PREQ, EMVS

**Source keyword index:** shall not, should not, shall, should, reserved

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.27, Figure 454, printed pages 453, PDF pages 479

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 464: Set Features - Command Dword 10</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-464-CLAIM figure-table:BASEBTS-BASE-FIG-464 -->

**SPEC.** Figure 464, "Set Features - Command Dword 10": Set Features FID selects the CDW11 interpretation. SV requests saving; successful setting alone does not prove persistence through power cycles. Decode the source-specific fields below.

#### Where this Figure fits

Set Features FID selects the CDW11 interpretation. SV requests saving; successful setting alone does not prove persistence through power cycles.

The indexed fields below belong to this source document and this Figure. The worked example connects them to the full operation.

#### Teaching redraw

```text
[Locate source: FID]
          ↓
[Extract field: SV] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `FID` | Feature Identifier, the eight-bit identifier selecting a function in Get/Set Features. |
| `SV` | Save, the Set Features bit requesting that the controller also save the configured value. |

#### Read in this order

1. Confirm NVME-BASE-2.4, §5.2.30, Figure 464; equal Figure numbers in different documents are different sources.
2. Apply the field/state rule above to the captured raw input.
3. Track image transfer, partition contents, active selection, and write protection separately. Successful download has not yet written a Boot Partition, and a successful write has not automatically activated it.
4. Compare the observation with the worked scenario and retain the cited source and target identity.

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
| Rule | Set Features FID selects the CDW11 interpretation. SV requests saving; successful setting alone does not prove persistence through power cycles. |
| Boundary | The same reset test has different expected results for the two mechanisms. Preserve the power-cycle/reset type so that relocking can be classified as expected behavior or a defect. |

**Informative example.** To leave BP0 unchanged and unlock BP1, FID 85h CDW11 is (001b << 3) | 000b = 08h. A subsequent Get does not return 000b for BP0; it returns its actual state, or 100b when RPMB owns protection.

**Common misconception.** The same reset test has different expected results for the two mechanisms. Preserve the power-cycle/reset type so that relocking can be classified as expected behavior or a defect.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Symptom / correction | The same reset test has different expected results for the two mechanisms. Preserve the power-cycle/reset type so that relocking can be classified as expected behavior or a defect. |

#### Questions the reader should now answer

1. Which source-specific fields establish the decision?
2. Which capability, target, or state would change the worked result?

**Source field index:** FID, SV

**Source keyword index:** shall, optional, reserved

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30, Figure 464, printed pages 457, PDF pages 483

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 465: Set Features - Command Dword 14</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-465-CLAIM figure-table:BASEBTS-BASE-FIG-465 -->

**SPEC.** Figure 465, "Set Features - Command Dword 14": Interpret the Set UUID Index with feature identity; these standard FIDs do not expand into a vendor-feature protocol. Decode the source-specific fields below.

#### Where this Figure fits

Interpret the Set UUID Index with feature identity; these standard FIDs do not expand into a vendor-feature protocol.

The indexed fields below belong to this source document and this Figure. The worked example connects them to the full operation.

#### Teaching redraw

```text
[Locate source: UUID Index]
          ↓
[Extract field: evidence] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `UUID Index` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Confirm NVME-BASE-2.4, §5.2.30, Figure 465; equal Figure numbers in different documents are different sources.
2. Apply the field/state rule above to the captured raw input.
3. Track image transfer, partition contents, active selection, and write protection separately. Successful download has not yet written a Boot Partition, and a successful write has not automatically activated it.
4. Compare the observation with the worked scenario and retain the cited source and target identity.

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
| Rule | Interpret the Set UUID Index with feature identity; these standard FIDs do not expand into a vendor-feature protocol. |
| Boundary | The same reset test has different expected results for the two mechanisms. Preserve the power-cycle/reset type so that relocking can be classified as expected behavior or a defect. |

**Informative example.** To leave BP0 unchanged and unlock BP1, FID 85h CDW11 is (001b << 3) | 000b = 08h. A subsequent Get does not return 000b for BP0; it returns its actual state, or 100b when RPMB owns protection.

**Common misconception.** The same reset test has different expected results for the two mechanisms. Preserve the power-cycle/reset type so that relocking can be classified as expected behavior or a defect.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Symptom / correction | The same reset test has different expected results for the two mechanisms. Preserve the power-cycle/reset type so that relocking can be classified as expected behavior or a defect. |

#### Questions the reader should now answer

1. Which source-specific fields establish the decision?
2. Which capability, target, or state would change the worked result?

**Source field index:** UUID Index

**Source keyword index:** shall, optional, reserved

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30, Figure 465, printed pages 457, PDF pages 483

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 466: Set Features - Feature Identifiers</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-466-CLAIM figure-table:BASEBTS-BASE-FIG-466 -->

**SPEC.** Figure 466, "Set Features - Feature Identifiers": Use only rows/scopes for Boot protection, Sanitize Config, AEC, and Host Behavior Support. FID 17h is subsystem policy. Decode the source-specific fields below.

#### Where this Figure fits

Use only rows/scopes for Boot protection, Sanitize Config, AEC, and Host Behavior Support. FID 17h is subsystem policy.

The indexed fields below belong to this source document and this Figure. The worked example connects them to the full operation.

#### Teaching redraw

```text
[Locate source: FID 85h]
          ↓
[Extract field: FID 17h] → [Apply encoding: FID 0Bh]
                                      ↓
[Validate evidence: FID 16h]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `FID 85h` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `FID 17h` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `FID 0Bh` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `FID 16h` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Confirm NVME-BASE-2.4, §5.2.30, Figure 466; equal Figure numbers in different documents are different sources.
2. Apply the field/state rule above to the captured raw input.
3. Separate advertised capabilities, command requests, and Feature policy. Command acceptance, operation success, and satisfaction of no-deallocate are three outcomes requiring different evidence.
4. Compare the observation with the worked scenario and retain the cited source and target identity.

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
| Rule | Use only rows/scopes for Boot protection, Sanitize Config, AEC, and Host Behavior Support. FID 17h is subsystem policy. |
| Boundary | PREQ is bit 4 in Figure 454 but bit 11 in Figure 451. Sharing an untyped builder between the two commands can set reserved bits in the namespace command. |

**Informative example.** SANACT=010b, AUSE=0, EMVS=1, NDAS=0, and PREQ=0 encode CDW10=0402h. It applies only with VERS/Block Erase support and other preconditions satisfied. Separately, OWPASS=0h means 16 passes, not skipping overwrite.

**Common misconception.** PREQ is bit 4 in Figure 454 but bit 11 in Figure 451. Sharing an untyped builder between the two commands can set reserved bits in the namespace command.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Symptom / correction | PREQ is bit 4 in Figure 454 but bit 11 in Figure 451. Sharing an untyped builder between the two commands can set reserved bits in the namespace command. |

#### Questions the reader should now answer

1. Which source-specific fields establish the decision?
2. Which capability, target, or state would change the worked result?

**Source field index:** FID 85h, FID 17h, FID 0Bh, FID 16h

**Source keyword index:** shall, should, may, optional, reserved

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30, Figure 466, printed pages 457-459, PDF pages 483-485

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 474: Asynchronous Event Configuration - Command Dword 11</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-474-CLAIM figure-table:BASEBTS-BASE-FIG-474 -->

**SPEC.** Figure 474, "Asynchronous Event Configuration - Command Dword 11": Use TLN bit 10: when TCDA changes from 0h to 1h with TLN enabled, Telemetry Log Changed is reported. This table belongs to 5.2.30.1.6. Decode the source-specific fields below.

#### Where this Figure fits

Use TLN bit 10: when TCDA changes from 0h to 1h with TLN enabled, Telemetry Log Changed is reported. This table belongs to 5.2.30.1.6.

The indexed fields below belong to this source document and this Figure. The worked example connects them to the full operation.

#### Teaching redraw

```text
[Locate source: TLN]
          ↓
[Extract field: evidence] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `TLN` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Confirm NVME-BASE-2.4, §5.2.30.1.6, Figure 474; equal Figure numbers in different documents are different sources.
2. Apply the field/state rule above to the captured raw input.
3. Separate creating 07h data from subsequent reads; the controller decides 08h capture timing. For both, verify generation and distinguish event acknowledgement from payload deletion.
4. Compare the observation with the worked scenario and retain the cited source and target identity.

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
| Rule | Use TLN bit 10: when TCDA changes from 0h to 1h with TLN enabled, Telemetry Log Changed is reported. This table belongs to 5.2.30.1.6. |
| Boundary | Do not describe RAE=0 as deleting the snapshot or treat the AER as the payload. The event supplies a collection trigger and locator; Get Log Page still retrieves the data. |

**Informative example.** If generation is 2Ah before reading and 2Bh afterward, the chunks cannot be accepted as one consistent capture. Even if it remains 2Ah, an 08h collection must consider the race where another host clears TCDA to zero.

**Common misconception.** Do not describe RAE=0 as deleting the snapshot or treat the AER as the payload. The event supplies a collection trigger and locator; Get Log Page still retrieves the data.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Symptom / correction | Do not describe RAE=0 as deleting the snapshot or treat the AER as the payload. The event supplies a collection trigger and locator; Get Log Page still retrieves the data. |

#### Questions the reader should now answer

1. Which source-specific fields establish the decision?
2. Which capability, target, or state would change the worked result?

**Source field index:** TLN

**Source keyword index:** shall not, shall, may, optional, reserved

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.6, Figure 474, printed pages 466-468, PDF pages 492-494

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 491: Host Behavior Support - Data Structure</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-491-CLAIM figure-table:BASEBTS-BASE-FIG-491 -->

**SPEC.** Figure 491, "Host Behavior Support - Data Structure": ETDAS=1 at Host Behavior Support byte 1 declares host Area 4 support; controller DA4S is still required. Decode the source-specific fields below.

#### Where this Figure fits

ETDAS=1 at Host Behavior Support byte 1 declares host Area 4 support; controller DA4S is still required.

The indexed fields below belong to this source document and this Figure. The worked example connects them to the full operation.

#### Teaching redraw

```text
[Locate source: ETDAS]
          ↓
[Extract field: evidence] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `ETDAS` | Extended Telemetry Data Area 4 Supported; the host's Area 4 declaration in Host Behavior Support. |

#### Read in this order

1. Confirm NVME-BASE-2.4, §5.2.30.1.15, Figure 491; equal Figure numbers in different documents are different sources.
2. Apply the field/state rule above to the captured raw input.
3. Areas are differently sized views starting at the same block 1. Decode the header, select the final applicable populated area, and do not add the three Last Block numbers.
4. Compare the observation with the worked scenario and retain the cited source and target identity.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 491 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §5.2.30.1.15 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| Rule | ETDAS=1 at Host Behavior Support byte 1 declares host Area 4 support; controller DA4S is still required. |
| Boundary | THS in LID 07h and TCS in LID 08h have different offsets; do not reuse one header layout for the other. Snapshot payload is vendor-defined, so unknown bytes cannot be assigned invented diagnostic fields. |

**Informative example.** For Last Blocks=65/1000/30000, Area 3 payload is 30000×512=15360000 bytes and the log including its header is 15360512 bytes. Values 0/1000/1000 mean Area 1 is empty and Area 3 adds no content beyond Area 2.

**Common misconception.** THS in LID 07h and TCS in LID 08h have different offsets; do not reuse one header layout for the other. Snapshot payload is vendor-defined, so unknown bytes cannot be assigned invented diagnostic fields.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Symptom / correction | THS in LID 07h and TCS in LID 08h have different offsets; do not reuse one header layout for the other. Snapshot payload is vendor-defined, so unknown bytes cannot be assigned invented diagnostic fields. |

#### Questions the reader should now answer

1. Which source-specific fields establish the decision?
2. Which capability, target, or state would change the worked result?

**Source field index:** ETDAS

**Source keyword index:** shall not, shall, may, reserved

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.15, Figure 491, printed pages 476-477, PDF pages 502-503

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 756: RPMB Device Configuration Block Data Structure</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-756-CLAIM figure-table:BASEBTS-BASE-FIG-756 -->

**SPEC.** Figure 756, "RPMB Device Configuration Block Data Structure": The Device Configuration Block separates protection enablement from each partition's lock control; once enabled, writes attempting to disable RPMB Boot protection are rejected. Decode the source-specific fields below.

#### Where this Figure fits

The Device Configuration Block separates protection enablement from each partition's lock control; once enabled, writes attempting to disable RPMB Boot protection are rejected.

The indexed fields below belong to this source document and this Figure. The worked example connects them to the full operation.

#### Teaching redraw

```text
[Locate source: Boot Partition Write Protection Enable]
          ↓
[Extract field: Boot Partition Write Protection] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `Boot Partition Write Protection Enable` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `Boot Partition Write Protection` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Confirm NVME-BASE-2.4, §8.1.24, Figure 756; equal Figure numbers in different documents are different sources.
2. Apply the field/state rule above to the captured raw input.
3. Track image transfer, partition contents, active selection, and write protection separately. Successful download has not yet written a Boot Partition, and a successful write has not automatically activated it.
4. Compare the observation with the worked scenario and retain the cited source and target identity.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 756 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §8.1.24 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| Rule | The Device Configuration Block separates protection enablement from each partition's lock control; once enabled, writes attempting to disable RPMB Boot protection are rejected. |
| Boundary | The same reset test has different expected results for the two mechanisms. Preserve the power-cycle/reset type so that relocking can be classified as expected behavior or a defect. |

**Informative example.** To leave BP0 unchanged and unlock BP1, FID 85h CDW11 is (001b << 3) | 000b = 08h. A subsequent Get does not return 000b for BP0; it returns its actual state, or 100b when RPMB owns protection.

**Common misconception.** The same reset test has different expected results for the two mechanisms. Preserve the power-cycle/reset type so that relocking can be classified as expected behavior or a defect.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Symptom / correction | The same reset test has different expected results for the two mechanisms. Preserve the power-cycle/reset type so that relocking can be classified as expected behavior or a defect. |

#### Questions the reader should now answer

1. Which source-specific fields establish the decision?
2. Which capability, target, or state would change the worked result?

**Source field index:** Boot Partition Write Protection Enable, Boot Partition Write Protection

**Source keyword index:** shall not, shall, should, may, reserved

> Source: NVME-BASE-2.4, Rev. 2.4, §8.1.24, Figure 756, printed pages 691-692, PDF pages 717-718

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 757: RPMB Request and Response Message Types</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-757-CLAIM figure-table:BASEBTS-BASE-FIG-757 -->

**SPEC.** Figure 757, "RPMB Request and Response Message Types": Track authenticated configuration read/write message types needed for Boot and pair each request with its expected response. Decode the source-specific fields below.

#### Where this Figure fits

Track authenticated configuration read/write message types needed for Boot and pair each request with its expected response.

The indexed fields below belong to this source document and this Figure. The worked example connects them to the full operation.

#### Teaching redraw

```text
[Locate source: Authenticated Device Configuration Block Read]
          ↓
[Extract field: Authenticated Device Configuration Block Write] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `Authenticated Device Configuration Block Read` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `Authenticated Device Configuration Block Write` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Confirm NVME-BASE-2.4, §8.1.24, Figure 757; equal Figure numbers in different documents are different sources.
2. Apply the field/state rule above to the captured raw input.
3. Track image transfer, partition contents, active selection, and write protection separately. Successful download has not yet written a Boot Partition, and a successful write has not automatically activated it.
4. Compare the observation with the worked scenario and retain the cited source and target identity.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 757 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §8.1.24 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| Rule | Track authenticated configuration read/write message types needed for Boot and pair each request with its expected response. |
| Boundary | The same reset test has different expected results for the two mechanisms. Preserve the power-cycle/reset type so that relocking can be classified as expected behavior or a defect. |

**Informative example.** To leave BP0 unchanged and unlock BP1, FID 85h CDW11 is (001b << 3) | 000b = 08h. A subsequent Get does not return 000b for BP0; it returns its actual state, or 100b when RPMB owns protection.

**Common misconception.** The same reset test has different expected results for the two mechanisms. Preserve the power-cycle/reset type so that relocking can be classified as expected behavior or a defect.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Symptom / correction | The same reset test has different expected results for the two mechanisms. Preserve the power-cycle/reset type so that relocking can be classified as expected behavior or a defect. |

#### Questions the reader should now answer

1. Which source-specific fields establish the decision?
2. Which capability, target, or state would change the worked result?

**Source field index:** Authenticated Device Configuration Block Read, Authenticated Device Configuration Block Write

**Source keyword index:** shall, may, reserved

> Source: NVME-BASE-2.4, Rev. 2.4, §8.1.24, Figure 757, printed pages 692-693, PDF pages 718-719

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 758: RPMB Operation Result</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-758-CLAIM figure-table:BASEBTS-BASE-FIG-758 -->

**SPEC.** Figure 758, "RPMB Operation Result": Operation Result distinguishes success, authentication, counter, and other failures; transport-command completion does not itself prove successful RPMB writing. Decode the source-specific fields below.

#### Where this Figure fits

Operation Result distinguishes success, authentication, counter, and other failures; transport-command completion does not itself prove successful RPMB writing.

The indexed fields below belong to this source document and this Figure. The worked example connects them to the full operation.

#### Teaching redraw

```text
[Locate source: Result]
          ↓
[Extract field: Authentication Failure] → [Apply encoding: Counter Failure]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `Result` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `Authentication Failure` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `Counter Failure` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Confirm NVME-BASE-2.4, §8.1.24, Figure 758; equal Figure numbers in different documents are different sources.
2. Apply the field/state rule above to the captured raw input.
3. Track image transfer, partition contents, active selection, and write protection separately. Successful download has not yet written a Boot Partition, and a successful write has not automatically activated it.
4. Compare the observation with the worked scenario and retain the cited source and target identity.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 758 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §8.1.24 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| Rule | Operation Result distinguishes success, authentication, counter, and other failures; transport-command completion does not itself prove successful RPMB writing. |
| Boundary | The same reset test has different expected results for the two mechanisms. Preserve the power-cycle/reset type so that relocking can be classified as expected behavior or a defect. |

**Informative example.** To leave BP0 unchanged and unlock BP1, FID 85h CDW11 is (001b << 3) | 000b = 08h. A subsequent Get does not return 000b for BP0; it returns its actual state, or 100b when RPMB owns protection.

**Common misconception.** The same reset test has different expected results for the two mechanisms. Preserve the power-cycle/reset type so that relocking can be classified as expected behavior or a defect.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Symptom / correction | The same reset test has different expected results for the two mechanisms. Preserve the power-cycle/reset type so that relocking can be classified as expected behavior or a defect. |

#### Questions the reader should now answer

1. Which source-specific fields establish the decision?
2. Which capability, target, or state would change the worked result?

**Source field index:** Result, Authentication Failure, Counter Failure

**Source keyword index:** may, reserved

> Source: NVME-BASE-2.4, Rev. 2.4, §8.1.24, Figure 758, printed pages 693, PDF pages 719

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 760: RPMB Data Frame</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-760-CLAIM figure-table:BASEBTS-BASE-FIG-760 -->

**SPEC.** Figure 760, "RPMB Data Frame": Message type, counter, nonce, result, and authentication provide different response-validation evidence in the frame; payload alone is insufficient. Decode the source-specific fields below.

#### Where this Figure fits

Message type, counter, nonce, result, and authentication provide different response-validation evidence in the frame; payload alone is insufficient.

The indexed fields below belong to this source document and this Figure. The worked example connects them to the full operation.

#### Teaching redraw

```text
[Locate source: Message Type]
          ↓
[Extract field: Result] → [Apply encoding: Write Counter]
                                      ↓
[Validate evidence: Nonce]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `Message Type` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `Result` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `Write Counter` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `Nonce` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `Authentication` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Confirm NVME-BASE-2.4, §8.1.24, Figure 760; equal Figure numbers in different documents are different sources.
2. Apply the field/state rule above to the captured raw input.
3. Track image transfer, partition contents, active selection, and write protection separately. Successful download has not yet written a Boot Partition, and a successful write has not automatically activated it.
4. Compare the observation with the worked scenario and retain the cited source and target identity.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 760 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §8.1.24 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| Rule | Message type, counter, nonce, result, and authentication provide different response-validation evidence in the frame; payload alone is insufficient. |
| Boundary | The same reset test has different expected results for the two mechanisms. Preserve the power-cycle/reset type so that relocking can be classified as expected behavior or a defect. |

**Informative example.** To leave BP0 unchanged and unlock BP1, FID 85h CDW11 is (001b << 3) | 000b = 08h. A subsequent Get does not return 000b for BP0; it returns its actual state, or 100b when RPMB owns protection.

**Common misconception.** The same reset test has different expected results for the two mechanisms. Preserve the power-cycle/reset type so that relocking can be classified as expected behavior or a defect.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Symptom / correction | The same reset test has different expected results for the two mechanisms. Preserve the power-cycle/reset type so that relocking can be classified as expected behavior or a defect. |

#### Questions the reader should now answer

1. Which source-specific fields establish the decision?
2. Which capability, target, or state would change the worked result?

**Source field index:** Message Type, Result, Write Counter, Nonce, Authentication

**Source keyword index:** shall not, shall, optional

> Source: NVME-BASE-2.4, Rev. 2.4, §8.1.24, Figure 760, printed pages 694, PDF pages 720

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 761: RPMB - Authentication Key Data Flow</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-761-CLAIM figure-table:BASEBTS-BASE-FIG-761 -->

**SPEC.** Figure 761, "RPMB - Authentication Key Data Flow": Authentication-key programming is prerequisite context for authenticated configuration; verify its result rather than equating key submission with success. Decode the source-specific fields below.

#### Where this Figure fits

Authentication-key programming is prerequisite context for authenticated configuration; verify its result rather than equating key submission with success.

The indexed fields below belong to this source document and this Figure. The worked example connects them to the full operation.

#### Teaching redraw

```text
[Locate source: Authentication Key]
          ↓
[Extract field: Program Result] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `Authentication Key` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `Program Result` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Confirm NVME-BASE-2.4, §8.1.24.2.1, Figure 761; equal Figure numbers in different documents are different sources.
2. Apply the field/state rule above to the captured raw input.
3. Track image transfer, partition contents, active selection, and write protection separately. Successful download has not yet written a Boot Partition, and a successful write has not automatically activated it.
4. Compare the observation with the worked scenario and retain the cited source and target identity.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 761 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §8.1.24.2.1 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| Rule | Authentication-key programming is prerequisite context for authenticated configuration; verify its result rather than equating key submission with success. |
| Boundary | The same reset test has different expected results for the two mechanisms. Preserve the power-cycle/reset type so that relocking can be classified as expected behavior or a defect. |

**Informative example.** To leave BP0 unchanged and unlock BP1, FID 85h CDW11 is (001b << 3) | 000b = 08h. A subsequent Get does not return 000b for BP0; it returns its actual state, or 100b when RPMB owns protection.

**Common misconception.** The same reset test has different expected results for the two mechanisms. Preserve the power-cycle/reset type so that relocking can be classified as expected behavior or a defect.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Symptom / correction | The same reset test has different expected results for the two mechanisms. Preserve the power-cycle/reset type so that relocking can be classified as expected behavior or a defect. |

#### Questions the reader should now answer

1. Which source-specific fields establish the decision?
2. Which capability, target, or state would change the worked result?

**Source field index:** Authentication Key, Program Result

**Source keyword index:** none

> Source: NVME-BASE-2.4, Rev. 2.4, §8.1.24.2.1, Figure 761, printed pages 695-696, PDF pages 721-722

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 762: RPMB - Read Write Counter Value Flow</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-762-CLAIM figure-table:BASEBTS-BASE-FIG-762 -->

**SPEC.** Figure 762, "RPMB - Read Write Counter Value Flow": Obtain and validate the write counter, use nonce/authentication to verify the response, then construct the protected configuration write. Decode the source-specific fields below.

#### Where this Figure fits

Obtain and validate the write counter, use nonce/authentication to verify the response, then construct the protected configuration write.

The indexed fields below belong to this source document and this Figure. The worked example connects them to the full operation.

#### Teaching redraw

```text
[Locate source: Write Counter]
          ↓
[Extract field: Nonce] → [Apply encoding: Authenticated Response]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `Write Counter` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `Nonce` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `Authenticated Response` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Confirm NVME-BASE-2.4, §8.1.24.2.2, Figure 762; equal Figure numbers in different documents are different sources.
2. Apply the field/state rule above to the captured raw input.
3. Track image transfer, partition contents, active selection, and write protection separately. Successful download has not yet written a Boot Partition, and a successful write has not automatically activated it.
4. Compare the observation with the worked scenario and retain the cited source and target identity.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 762 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §8.1.24.2.2 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| Rule | Obtain and validate the write counter, use nonce/authentication to verify the response, then construct the protected configuration write. |
| Boundary | The same reset test has different expected results for the two mechanisms. Preserve the power-cycle/reset type so that relocking can be classified as expected behavior or a defect. |

**Informative example.** To leave BP0 unchanged and unlock BP1, FID 85h CDW11 is (001b << 3) | 000b = 08h. A subsequent Get does not return 000b for BP0; it returns its actual state, or 100b when RPMB owns protection.

**Common misconception.** The same reset test has different expected results for the two mechanisms. Preserve the power-cycle/reset type so that relocking can be classified as expected behavior or a defect.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Symptom / correction | The same reset test has different expected results for the two mechanisms. Preserve the power-cycle/reset type so that relocking can be classified as expected behavior or a defect. |

#### Questions the reader should now answer

1. Which source-specific fields establish the decision?
2. Which capability, target, or state would change the worked result?

**Source field index:** Write Counter, Nonce, Authenticated Response

**Source keyword index:** none

> Source: NVME-BASE-2.4, Rev. 2.4, §8.1.24.2.2, Figure 762, printed pages 696, PDF pages 722

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 765: RPMB - Authenticated Device Configuration Block Write Flow</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-765-CLAIM figure-table:BASEBTS-BASE-FIG-765 -->

**SPEC.** Figure 765, "RPMB - Authenticated Device Configuration Block Write Flow": Verify the result after an authenticated configuration write. This changes Boot protection state, not image contents as Firmware Commit does. Decode the source-specific fields below.

#### Where this Figure fits

Verify the result after an authenticated configuration write. This changes Boot protection state, not image contents as Firmware Commit does.

The indexed fields below belong to this source document and this Figure. The worked example connects them to the full operation.

#### Teaching redraw

```text
[Locate source: Configuration Write]
          ↓
[Extract field: Counter] → [Apply encoding: Result Read]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `Configuration Write` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `Counter` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `Result Read` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Confirm NVME-BASE-2.4, §8.1.24.3, Figure 765; equal Figure numbers in different documents are different sources.
2. Apply the field/state rule above to the captured raw input.
3. Track image transfer, partition contents, active selection, and write protection separately. Successful download has not yet written a Boot Partition, and a successful write has not automatically activated it.
4. Compare the observation with the worked scenario and retain the cited source and target identity.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 765 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §8.1.24.3 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| Rule | Verify the result after an authenticated configuration write. This changes Boot protection state, not image contents as Firmware Commit does. |
| Boundary | The same reset test has different expected results for the two mechanisms. Preserve the power-cycle/reset type so that relocking can be classified as expected behavior or a defect. |

**Informative example.** To leave BP0 unchanged and unlock BP1, FID 85h CDW11 is (001b << 3) | 000b = 08h. A subsequent Get does not return 000b for BP0; it returns its actual state, or 100b when RPMB owns protection.

**Common misconception.** The same reset test has different expected results for the two mechanisms. Preserve the power-cycle/reset type so that relocking can be classified as expected behavior or a defect.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Symptom / correction | The same reset test has different expected results for the two mechanisms. Preserve the power-cycle/reset type so that relocking can be classified as expected behavior or a defect. |

#### Questions the reader should now answer

1. Which source-specific fields establish the decision?
2. Which capability, target, or state would change the worked result?

**Source field index:** Configuration Write, Counter, Result Read

**Source keyword index:** should

> Source: NVME-BASE-2.4, Rev. 2.4, §8.1.24.3, Figure 765, printed pages 700, PDF pages 726

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 766: RPMB - Authenticated Device Configuration Block Read Flow</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-766-CLAIM figure-table:BASEBTS-BASE-FIG-766 -->

**SPEC.** Figure 766, "RPMB - Authenticated Device Configuration Block Read Flow": Authenticated configuration read retrieves verifiable protection settings used to establish which mechanism currently controls the partition. Decode the source-specific fields below.

#### Where this Figure fits

Authenticated configuration read retrieves verifiable protection settings used to establish which mechanism currently controls the partition.

The indexed fields below belong to this source document and this Figure. The worked example connects them to the full operation.

#### Teaching redraw

```text
[Locate source: Configuration Read]
          ↓
[Extract field: Nonce] → [Apply encoding: Authentication]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `Configuration Read` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `Nonce` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `Authentication` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Confirm NVME-BASE-2.4, §8.1.24.4, Figure 766; equal Figure numbers in different documents are different sources.
2. Apply the field/state rule above to the captured raw input.
3. Track image transfer, partition contents, active selection, and write protection separately. Successful download has not yet written a Boot Partition, and a successful write has not automatically activated it.
4. Compare the observation with the worked scenario and retain the cited source and target identity.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 766 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §8.1.24.4 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| Rule | Authenticated configuration read retrieves verifiable protection settings used to establish which mechanism currently controls the partition. |
| Boundary | The same reset test has different expected results for the two mechanisms. Preserve the power-cycle/reset type so that relocking can be classified as expected behavior or a defect. |

**Informative example.** To leave BP0 unchanged and unlock BP1, FID 85h CDW11 is (001b << 3) | 000b = 08h. A subsequent Get does not return 000b for BP0; it returns its actual state, or 100b when RPMB owns protection.

**Common misconception.** The same reset test has different expected results for the two mechanisms. Preserve the power-cycle/reset type so that relocking can be classified as expected behavior or a defect.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Symptom / correction | The same reset test has different expected results for the two mechanisms. Preserve the power-cycle/reset type so that relocking can be classified as expected behavior or a defect. |

#### Questions the reader should now answer

1. Which source-specific fields establish the decision?
2. Which capability, target, or state would change the worked result?

**Source field index:** Configuration Read, Nonce, Authentication

**Source keyword index:** shall not, shall, may

> Source: NVME-BASE-2.4, Rev. 2.4, §8.1.24.4, Figure 766, printed pages 701, PDF pages 727

</details>

## Use and limitations

Use the claim IDs as stable PPT traceability keys. Re-check affected claims if the source revision, errata set, or approved scope changes.

## Self-questions and worked answers

32 answered questions revisit this report's scope. Each answer retains the same source links as the teaching module; calculations and debugging examples are informative.

### Q01. What is the governing interpretation for “Two Boot read paths”?

<!-- qa:base-boot-telemetry-sanitize-boot-read-lead -->

**Answer.**

First determine whether an Admin-command environment exists, then choose properties or LID 15h. Both access boot contents, but their return formats and observation points differ.

> Source: NVME-BASE-2.4, Rev. 2.4, §8.1.3, printed pages 586, PDF pages 612; Source: NVME-BASE-2.4, Rev. 2.4, §8.1.3.1, printed pages 586-587, PDF pages 612-613; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.21, printed pages 283-284, PDF pages 309-310

### Q02. Which concepts or conditions must be distinguished in “Two Boot read paths”?

<!-- qa:base-boot-telemetry-sanitize-boot-read-rows -->

**Answer.**

- Properties — BRS reports read state — Does not require CC.EN=1
- LID 15h — 16-byte header + data — The Admin-command CQE reports the command result
- BPID — Selects the partition to read — Not the active ID
- BPSZ — 128 KiB per unit — Not a byte count

> Source: NVME-BASE-2.4, Rev. 2.4, §8.1.3, printed pages 586, PDF pages 612; Source: NVME-BASE-2.4, Rev. 2.4, §8.1.3.1, printed pages 586-587, PDF pages 612-613; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.21, printed pages 283-284, PDF pages 309-310

### Q03. How does “Two Boot read paths” apply to a concrete calculation or operational scenario?

<!-- qa:base-boot-telemetry-sanitize-boot-read-example -->

**Answer.**

With BPSZ=2, LID 15h contains 262144 bytes of boot data plus a 16-byte header, totaling 262160 bytes. Reading BP1 does not activate BP1, and a log read does not advance the property's BRS.

> Source: NVME-BASE-2.4, Rev. 2.4, §8.1.3, printed pages 586, PDF pages 612; Source: NVME-BASE-2.4, Rev. 2.4, §8.1.3.1, printed pages 586-587, PDF pages 612-613; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.21, printed pages 283-284, PDF pages 309-310

### Q04. What misinterpretation is most likely in “Two Boot read paths”, and how is it debugged?

<!-- qa:base-boot-telemetry-sanitize-boot-read-pitfall -->

**Answer.**

For an unfinished property read, inspect BRS and the buffer; reset is not an allowed normal completion step. BPINFO in LID 15h is a returned field and reading it does not modify the property of the same name.

> Source: NVME-BASE-2.4, Rev. 2.4, §8.1.3, printed pages 586, PDF pages 612; Source: NVME-BASE-2.4, Rev. 2.4, §8.1.3.1, printed pages 586-587, PDF pages 612-613; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.21, printed pages 283-284, PDF pages 309-310

### Q05. What is the governing interpretation for “The complete update and protection lifecycle”?

<!-- qa:base-boot-telemetry-sanitize-boot-protection-lead -->

**Answer.**

Track image transfer, partition contents, active selection, and write protection separately. Successful download has not yet written a Boot Partition, and a successful write has not automatically activated it.

> Source: NVME-BASE-2.4, Rev. 2.4, §8.1.3.2, printed pages 587-588, PDF pages 613-614; Source: NVME-BASE-2.4, Rev. 2.4, §8.1.3.2, printed pages 588, PDF pages 614; Source: NVME-BASE-2.4, Rev. 2.4, §8.1.3.3, printed pages 588-589, PDF pages 614-615; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.39, printed pages 513-514, PDF pages 539-540; Source: NVME-BASE-2.4, Rev. 2.4, §8.1.3.3.1-8.1.3.3.3, printed pages 589-594, PDF pages 615-620; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.39; 8.1.3.3.3, printed pages 513-514,593-594, PDF pages 539-540,619-620

### Q06. Which concepts or conditions must be distinguished in “The complete update and protection lifecycle”?

<!-- qa:base-boot-telemetry-sanitize-boot-protection-rows -->

**Answer.**

- FID 85h unlocked — Survives controller reset — Locked after power cycle
- FID 85h until power cycle — Ordinary Set cannot unlock — Unavailable for shared multi-domain partitions
- RPMB enabled/unlocked — Controller reset relocks — Protection enablement cannot be reversed
- Both mechanisms — Only one owns control at a time — RPMB enablement transfers ownership

> Source: NVME-BASE-2.4, Rev. 2.4, §8.1.3.2, printed pages 587-588, PDF pages 613-614; Source: NVME-BASE-2.4, Rev. 2.4, §8.1.3.2, printed pages 588, PDF pages 614; Source: NVME-BASE-2.4, Rev. 2.4, §8.1.3.3, printed pages 588-589, PDF pages 614-615; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.39, printed pages 513-514, PDF pages 539-540; Source: NVME-BASE-2.4, Rev. 2.4, §8.1.3.3.1-8.1.3.3.3, printed pages 589-594, PDF pages 615-620; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.39; 8.1.3.3.3, printed pages 513-514,593-594, PDF pages 539-540,619-620

### Q07. How does “The complete update and protection lifecycle” apply to a concrete calculation or operational scenario?

<!-- qa:base-boot-telemetry-sanitize-boot-protection-example -->

**Answer.**

To leave BP0 unchanged and unlock BP1, FID 85h CDW11 is (001b << 3) | 000b = 08h. A subsequent Get does not return 000b for BP0; it returns its actual state, or 100b when RPMB owns protection.

> Source: NVME-BASE-2.4, Rev. 2.4, §8.1.3.2, printed pages 587-588, PDF pages 613-614; Source: NVME-BASE-2.4, Rev. 2.4, §8.1.3.2, printed pages 588, PDF pages 614; Source: NVME-BASE-2.4, Rev. 2.4, §8.1.3.3, printed pages 588-589, PDF pages 614-615; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.39, printed pages 513-514, PDF pages 539-540; Source: NVME-BASE-2.4, Rev. 2.4, §8.1.3.3.1-8.1.3.3.3, printed pages 589-594, PDF pages 615-620; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.39; 8.1.3.3.3, printed pages 513-514,593-594, PDF pages 539-540,619-620

### Q08. What misinterpretation is most likely in “The complete update and protection lifecycle”, and how is it debugged?

<!-- qa:base-boot-telemetry-sanitize-boot-protection-pitfall -->

**Answer.**

The same reset test has different expected results for the two mechanisms. Preserve the power-cycle/reset type so that relocking can be classified as expected behavior or a defect.

> Source: NVME-BASE-2.4, Rev. 2.4, §8.1.3.2, printed pages 587-588, PDF pages 613-614; Source: NVME-BASE-2.4, Rev. 2.4, §8.1.3.2, printed pages 588, PDF pages 614; Source: NVME-BASE-2.4, Rev. 2.4, §8.1.3.3, printed pages 588-589, PDF pages 614-615; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.39, printed pages 513-514, PDF pages 539-540; Source: NVME-BASE-2.4, Rev. 2.4, §8.1.3.3.1-8.1.3.3.3, printed pages 589-594, PDF pages 615-620; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.39; 8.1.3.3.3, printed pages 513-514,593-594, PDF pages 539-540,619-620

### Q09. What is the governing interpretation for “Computing snapshots from Last Block”?

<!-- qa:base-boot-telemetry-sanitize-telemetry-layout-lead -->

**Answer.**

Areas are differently sized views starting at the same block 1. Decode the header, select the final applicable populated area, and do not add the three Last Block numbers.

> Source: NVME-BASE-2.4, Rev. 2.4, §8.1.30; 5.2.13.1.8-5.2.13.1.9, printed pages 232-237,733-737, PDF pages 258-263,759-763; Source: NVME-BASE-2.4, Rev. 2.4, §8.1.30; 5.2.30.1.15, printed pages 476,733-734, PDF pages 502,759-760; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.8-5.2.13.1.9, printed pages 232-237, PDF pages 258-263

### Q10. Which concepts or conditions must be distinguished in “Computing snapshots from Last Block”?

<!-- qa:base-boot-telemetry-sanitize-telemetry-layout-rows -->

**Answer.**

- Area 1 — 1 through L1 — L1=0 means no data
- Area 2 — 1 through L2 — L2 >= L1
- Area 3 — 1 through L3 — L3 >= L2
- Area 4 — 1 through L4 — Check support separately

> Source: NVME-BASE-2.4, Rev. 2.4, §8.1.30; 5.2.13.1.8-5.2.13.1.9, printed pages 232-237,733-737, PDF pages 258-263,759-763; Source: NVME-BASE-2.4, Rev. 2.4, §8.1.30; 5.2.30.1.15, printed pages 476,733-734, PDF pages 502,759-760; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.8-5.2.13.1.9, printed pages 232-237, PDF pages 258-263

### Q11. How does “Computing snapshots from Last Block” apply to a concrete calculation or operational scenario?

<!-- qa:base-boot-telemetry-sanitize-telemetry-layout-example -->

**Answer.**

For Last Blocks=65/1000/30000, Area 3 payload is 30000×512=15360000 bytes and the log including its header is 15360512 bytes. Values 0/1000/1000 mean Area 1 is empty and Area 3 adds no content beyond Area 2.

> Source: NVME-BASE-2.4, Rev. 2.4, §8.1.30; 5.2.13.1.8-5.2.13.1.9, printed pages 232-237,733-737, PDF pages 258-263,759-763; Source: NVME-BASE-2.4, Rev. 2.4, §8.1.30; 5.2.30.1.15, printed pages 476,733-734, PDF pages 502,759-760; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.8-5.2.13.1.9, printed pages 232-237, PDF pages 258-263

### Q12. What misinterpretation is most likely in “Computing snapshots from Last Block”, and how is it debugged?

<!-- qa:base-boot-telemetry-sanitize-telemetry-layout-pitfall -->

**Answer.**

THS in LID 07h and TCS in LID 08h have different offsets; do not reuse one header layout for the other. Snapshot payload is vendor-defined, so unknown bytes cannot be assigned invented diagnostic fields.

> Source: NVME-BASE-2.4, Rev. 2.4, §8.1.30; 5.2.13.1.8-5.2.13.1.9, printed pages 232-237,733-737, PDF pages 258-263,759-763; Source: NVME-BASE-2.4, Rev. 2.4, §8.1.30; 5.2.30.1.15, printed pages 476,733-734, PDF pages 502,759-760; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.8-5.2.13.1.9, printed pages 232-237, PDF pages 258-263

### Q13. What is the governing interpretation for “Create, read, verify consistency, acknowledge”?

<!-- qa:base-boot-telemetry-sanitize-telemetry-capture-lead -->

**Answer.**

Separate creating 07h data from subsequent reads; the controller decides 08h capture timing. For both, verify generation and distinguish event acknowledgement from payload deletion.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.8, printed pages 232-235, PDF pages 258-261; Source: NVME-BASE-2.4, Rev. 2.4, §8.1.30, printed pages 734-735, PDF pages 760-761; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.9, printed pages 237, PDF pages 263; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.8-5.2.13.1.9, printed pages 233,235,237, PDF pages 259,261,263; Source: NVME-BASE-2.4, Rev. 2.4, §8.1.30; 5.2.30.1.6, printed pages 734-735,466-468, PDF pages 760-761,492-494

### Q14. Which concepts or conditions must be distinguished in “Create, read, verify consistency, acknowledge”?

<!-- qa:base-boot-telemetry-sanitize-telemetry-capture-rows -->

**Answer.**

- CTHID=1 — Triggers a new 07h capture — Do not create again for subsequent chunks
- MCDA — Limits the areas created — Check MCDAS first
- RAE=1 — Retains the event — Does not exclude another reader
- TCDA=0 — No update since acknowledgement — In 2.4 it does not mean payload disappearance

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.8, printed pages 232-235, PDF pages 258-261; Source: NVME-BASE-2.4, Rev. 2.4, §8.1.30, printed pages 734-735, PDF pages 760-761; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.9, printed pages 237, PDF pages 263; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.8-5.2.13.1.9, printed pages 233,235,237, PDF pages 259,261,263; Source: NVME-BASE-2.4, Rev. 2.4, §8.1.30; 5.2.30.1.6, printed pages 734-735,466-468, PDF pages 760-761,492-494

### Q15. How does “Create, read, verify consistency, acknowledge” apply to a concrete calculation or operational scenario?

<!-- qa:base-boot-telemetry-sanitize-telemetry-capture-example -->

**Answer.**

If generation is 2Ah before reading and 2Bh afterward, the chunks cannot be accepted as one consistent capture. Even if it remains 2Ah, an 08h collection must consider the race where another host clears TCDA to zero.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.8, printed pages 232-235, PDF pages 258-261; Source: NVME-BASE-2.4, Rev. 2.4, §8.1.30, printed pages 734-735, PDF pages 760-761; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.9, printed pages 237, PDF pages 263; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.8-5.2.13.1.9, printed pages 233,235,237, PDF pages 259,261,263; Source: NVME-BASE-2.4, Rev. 2.4, §8.1.30; 5.2.30.1.6, printed pages 734-735,466-468, PDF pages 760-761,492-494

### Q16. What misinterpretation is most likely in “Create, read, verify consistency, acknowledge”, and how is it debugged?

<!-- qa:base-boot-telemetry-sanitize-telemetry-capture-pitfall -->

**Answer.**

Do not describe RAE=0 as deleting the snapshot or treat the AER as the payload. The event supplies a collection trigger and locator; Get Log Page still retrieves the data.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.8, printed pages 232-235, PDF pages 258-261; Source: NVME-BASE-2.4, Rev. 2.4, §8.1.30, printed pages 734-735, PDF pages 760-761; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.9, printed pages 237, PDF pages 263; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.8-5.2.13.1.9, printed pages 233,235,237, PDF pages 259,261,263; Source: NVME-BASE-2.4, Rev. 2.4, §8.1.30; 5.2.30.1.6, printed pages 734-735,466-468, PDF pages 760-761,492-494

### Q17. What is the governing interpretation for “Define the sanitization target first”?

<!-- qa:base-boot-telemetry-sanitize-sanitize-scope-lead -->

**Answer.**

Sanitize scope is not simply everything on a disk. Classify the target, data provenance, and whether it can contain user data; this also establishes its relationship with Boot and diagnostics.

> Source: NVME-BASE-2.4, Rev. 2.4, §8.1.27, printed pages 711-712, PDF pages 737-738; Source: NVME-BASE-2.4, Rev. 2.4, §8.1.27, printed pages 711-712, PDF pages 737-738; Source: NVME-BASE-2.4, Rev. 2.4, §8.1.27.2-8.1.27.3, printed pages 714-717, PDF pages 740-743; Source: NVME-NVM-CS-1.3, Rev. 1.3, §5.12, printed pages 174, PDF pages 174

### Q18. Which concepts or conditions must be distinguished in “Define the sanitization target first”?

<!-- qa:base-boot-telemetry-sanitize-sanitize-scope-rows -->

**Answer.**

- Boot/RPMB — Unaffected by sanitize — Managed by their own mechanisms
- Logs/features — Modify user data when necessary — Namespace media alone is insufficient
- All namespace sanitizes — Complete work on each target — Does not thereby establish subsystem GDE
- Crypto Erase — Changes keys and handles unencrypted data — Old key copies matter too

> Source: NVME-BASE-2.4, Rev. 2.4, §8.1.27, printed pages 711-712, PDF pages 737-738; Source: NVME-BASE-2.4, Rev. 2.4, §8.1.27, printed pages 711-712, PDF pages 737-738; Source: NVME-BASE-2.4, Rev. 2.4, §8.1.27.2-8.1.27.3, printed pages 714-717, PDF pages 740-743; Source: NVME-NVM-CS-1.3, Rev. 1.3, §5.12, printed pages 174, PDF pages 174

### Q19. How does “Define the sanitization target first” apply to a concrete calculation or operational scenario?

<!-- qa:base-boot-telemetry-sanitize-sanitize-scope-example -->

**Answer.**

Even after every namespace is sanitized, that fact does not prove subsystem-level data such as CMB has undergone subsystem sanitization. Conversely, successful subsystem sanitize does not update or erase the boot image in a Boot Partition.

> Source: NVME-BASE-2.4, Rev. 2.4, §8.1.27, printed pages 711-712, PDF pages 737-738; Source: NVME-BASE-2.4, Rev. 2.4, §8.1.27, printed pages 711-712, PDF pages 737-738; Source: NVME-BASE-2.4, Rev. 2.4, §8.1.27.2-8.1.27.3, printed pages 714-717, PDF pages 740-743; Source: NVME-NVM-CS-1.3, Rev. 1.3, §5.12, printed pages 174, PDF pages 174

### Q20. What misinterpretation is most likely in “Define the sanitization target first”, and how is it debugged?

<!-- qa:base-boot-telemetry-sanitize-sanitize-scope-pitfall -->

**Answer.**

Using zero-filled reads as the only success criterion misclassifies results. Establish the method, allocation state, and verification state before applying NVM Command Set result definitions.

> Source: NVME-BASE-2.4, Rev. 2.4, §8.1.27, printed pages 711-712, PDF pages 737-738; Source: NVME-BASE-2.4, Rev. 2.4, §8.1.27, printed pages 711-712, PDF pages 737-738; Source: NVME-BASE-2.4, Rev. 2.4, §8.1.27.2-8.1.27.3, printed pages 714-717, PDF pages 740-743; Source: NVME-NVM-CS-1.3, Rev. 1.3, §5.12, printed pages 174, PDF pages 174

### Q21. What is the governing interpretation for “Combining command parameters with capabilities”?

<!-- qa:base-boot-telemetry-sanitize-sanitize-command-lead -->

**Answer.**

Separate advertised capabilities, command requests, and Feature policy. Command acceptance, operation success, and satisfaction of no-deallocate are three outcomes requiring different evidence.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.26, printed pages 448-451, PDF pages 474-477; Source: NVME-BASE-2.4, Rev. 2.4, §8.1.27.1; 5.2.27, printed pages 713,453, PDF pages 739,479; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.16; 8.1.27.2-8.1.27.3, printed pages 477-478,715-719, PDF pages 503-504,741-745; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.26, printed pages 449, PDF pages 475; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.26; 8.1.27.1, printed pages 449-451,712-714, PDF pages 475-477,738-740; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.26; 8.1.27.3, printed pages 451,717, PDF pages 477,743

### Q22. Which concepts or conditions must be distinguished in “Combining command parameters with capabilities”?

<!-- qa:base-boot-telemetry-sanitize-sanitize-command-rows -->

**Answer.**

- NDAS=1, NDI=0 — Successful sanitize must not deallocate — Other validity conditions still apply
- NDAS=1, NDI=1, NODRM=0 — Command rejected — Invalid Field in Command
- NDAS=1, NDI=1, NODRM=1 — Processing permitted — Success can report SOS=100b
- EMVS=1 — Subsystem requires VERS=1 — Block/Crypto + NDAS=0

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.26, printed pages 448-451, PDF pages 474-477; Source: NVME-BASE-2.4, Rev. 2.4, §8.1.27.1; 5.2.27, printed pages 713,453, PDF pages 739,479; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.16; 8.1.27.2-8.1.27.3, printed pages 477-478,715-719, PDF pages 503-504,741-745; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.26, printed pages 449, PDF pages 475; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.26; 8.1.27.1, printed pages 449-451,712-714, PDF pages 475-477,738-740; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.26; 8.1.27.3, printed pages 451,717, PDF pages 477,743

### Q23. How does “Combining command parameters with capabilities” apply to a concrete calculation or operational scenario?

<!-- qa:base-boot-telemetry-sanitize-sanitize-command-example -->

**Answer.**

SANACT=010b, AUSE=0, EMVS=1, NDAS=0, and PREQ=0 encode CDW10=0402h. It applies only with VERS/Block Erase support and other preconditions satisfied. Separately, OWPASS=0h means 16 passes, not skipping overwrite.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.26, printed pages 448-451, PDF pages 474-477; Source: NVME-BASE-2.4, Rev. 2.4, §8.1.27.1; 5.2.27, printed pages 713,453, PDF pages 739,479; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.16; 8.1.27.2-8.1.27.3, printed pages 477-478,715-719, PDF pages 503-504,741-745; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.26, printed pages 449, PDF pages 475; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.26; 8.1.27.1, printed pages 449-451,712-714, PDF pages 475-477,738-740; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.26; 8.1.27.3, printed pages 451,717, PDF pages 477,743

### Q24. What misinterpretation is most likely in “Combining command parameters with capabilities”, and how is it debugged?

<!-- qa:base-boot-telemetry-sanitize-sanitize-command-pitfall -->

**Answer.**

PREQ is bit 4 in Figure 454 but bit 11 in Figure 451. Sharing an untyped builder between the two commands can set reserved bits in the namespace command.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.26, printed pages 448-451, PDF pages 474-477; Source: NVME-BASE-2.4, Rev. 2.4, §8.1.27.1; 5.2.27, printed pages 713,453, PDF pages 739,479; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.16; 8.1.27.2-8.1.27.3, printed pages 477-478,715-719, PDF pages 503-504,741-745; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.26, printed pages 449, PDF pages 475; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.26; 8.1.27.1, printed pages 449-451,712-714, PDF pages 475-477,738-740; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.26; 8.1.27.3, printed pages 451,717, PDF pages 477,743

### Q25. What is the governing interpretation for “Reconstruct background work from state, log, and AER”?

<!-- qa:base-boot-telemetry-sanitize-sanitize-state-lead -->

**Answer.**

Start with the seven states in Figure 772 and attach transition conditions from Figures 773–779. Status describes results, state describes the current position, and events report transitions.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.26.1; 8.1.27.1, printed pages 451,712-713, PDF pages 477,738-739; Source: NVME-BASE-2.4, Rev. 2.4, §8.1.27.4, printed pages 719-730, PDF pages 745-756; Source: NVME-BASE-2.4, Rev. 2.4, §8.1.27.4.6-8.1.27.4.7, printed pages 727-730, PDF pages 753-756; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.38, printed pages 313-319, PDF pages 339-345; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.38; 8.1.27.3, printed pages 314-319,718, PDF pages 340-345,744; Source: NVME-BASE-2.4, Rev. 2.4, §8.1.27.1; 8.1.27.4, printed pages 712-713,720, PDF pages 738-739,746

### Q26. Which concepts or conditions must be distinguished in “Reconstruct background work from state, log, and AER”?

<!-- qa:base-boot-telemetry-sanitize-sanitize-state-rows -->

**Answer.**

- Restricted Failure — Retry in restricted mode — Exit Failure Mode cannot escape it
- Unrestricted Failure — Retry or Exit Failure Mode — Idle does not rewrite failure history
- Media Verification — Processing succeeded — The operation is still Sanitizing
- Post-Verification Deallocation — SPROG starts again at zero — Failure records FAILS=6h

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.26.1; 8.1.27.1, printed pages 451,712-713, PDF pages 477,738-739; Source: NVME-BASE-2.4, Rev. 2.4, §8.1.27.4, printed pages 719-730, PDF pages 745-756; Source: NVME-BASE-2.4, Rev. 2.4, §8.1.27.4.6-8.1.27.4.7, printed pages 727-730, PDF pages 753-756; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.38, printed pages 313-319, PDF pages 339-345; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.38; 8.1.27.3, printed pages 314-319,718, PDF pages 340-345,744; Source: NVME-BASE-2.4, Rev. 2.4, §8.1.27.1; 8.1.27.4, printed pages 712-713,720, PDF pages 738-739,746

### Q27. How does “Reconstruct background work from state, log, and AER” apply to a concrete calculation or operational scenario?

<!-- qa:base-boot-telemetry-sanitize-sanitize-state-example -->

**Answer.**

SPROG=8000h represents 50% of the currently measured phase. Media Verification uses SPROG=FFFFh while SOS can remain 010b; leaving verification for deallocation starts progress again at zero. This is not progress regression.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.26.1; 8.1.27.1, printed pages 451,712-713, PDF pages 477,738-739; Source: NVME-BASE-2.4, Rev. 2.4, §8.1.27.4, printed pages 719-730, PDF pages 745-756; Source: NVME-BASE-2.4, Rev. 2.4, §8.1.27.4.6-8.1.27.4.7, printed pages 727-730, PDF pages 753-756; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.38, printed pages 313-319, PDF pages 339-345; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.38; 8.1.27.3, printed pages 314-319,718, PDF pages 340-345,744; Source: NVME-BASE-2.4, Rev. 2.4, §8.1.27.1; 8.1.27.4, printed pages 712-713,720, PDF pages 738-739,746

### Q28. What misinterpretation is most likely in “Reconstruct background work from state, log, and AER”, and how is it debugged?

<!-- qa:base-boot-telemetry-sanitize-sanitize-state-pitfall -->

**Answer.**

Preserve SCDW10, SOS, SANS, FAILS, MVCNCLD, and event timestamps. Recording only a completion event conflates success, failure, and entry into verification.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.26.1; 8.1.27.1, printed pages 451,712-713, PDF pages 477,738-739; Source: NVME-BASE-2.4, Rev. 2.4, §8.1.27.4, printed pages 719-730, PDF pages 745-756; Source: NVME-BASE-2.4, Rev. 2.4, §8.1.27.4.6-8.1.27.4.7, printed pages 727-730, PDF pages 753-756; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.38, printed pages 313-319, PDF pages 339-345; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.38; 8.1.27.3, printed pages 314-319,718, PDF pages 340-345,744; Source: NVME-BASE-2.4, Rev. 2.4, §8.1.27.1; 8.1.27.4, printed pages 712-713,720, PDF pages 738-739,746

### Q29. What is the governing interpretation for “Restrictions and verification reads”?

<!-- qa:base-boot-telemetry-sanitize-sanitize-read-lead -->

**Answer.**

Evaluate the command allowlist and the NVM Read exception separately. Determine target/state, then PI checking and allocation; ordinary-read behavior cannot be applied unchanged to verification.

> Source: NVME-BASE-2.4, Rev. 2.4, §8.1.27.5; 5.1.1-5.1.2, printed pages 178-181,730-732, PDF pages 204-207,756-758; Source: NVME-BASE-2.4, Rev. 2.4, §8.1.27.5, printed pages 730-732, PDF pages 756-758; Source: NVME-NVM-CS-1.3, Rev. 1.3, §4.1.7; 5.12, printed pages 113,173-175, PDF pages 113,173-175; Source: NVME-NVM-CS-1.3, Rev. 1.3, §5.12, printed pages 174, PDF pages 174; Source: NVME-NVM-CS-1.3, Rev. 1.3, §5.12.1, printed pages 174-175, PDF pages 174-175; Source: NVME-BASE-2.4, Rev. 2.4, §8.1.3.1; 8.1.27.4.2, printed pages 587,721, PDF pages 613,747

### Q30. Which concepts or conditions must be distinguished in “Restrictions and verification reads”?

<!-- qa:base-boot-telemetry-sanitize-sanitize-read-rows -->

**Answer.**

- PI checking requested — Invalid Field in Command — Not permitted for verification reads
- Allocated media readable — Return media data — Integrity errors can be ignored when readable
- Allocated media unreadable — Unrecovered Read Error — Do not invent data
- Deallocated LBA — Use deallocated/unwritten rules — Not evidence of the old media pattern

> Source: NVME-BASE-2.4, Rev. 2.4, §8.1.27.5; 5.1.1-5.1.2, printed pages 178-181,730-732, PDF pages 204-207,756-758; Source: NVME-BASE-2.4, Rev. 2.4, §8.1.27.5, printed pages 730-732, PDF pages 756-758; Source: NVME-NVM-CS-1.3, Rev. 1.3, §4.1.7; 5.12, printed pages 113,173-175, PDF pages 113,173-175; Source: NVME-NVM-CS-1.3, Rev. 1.3, §5.12, printed pages 174, PDF pages 174; Source: NVME-NVM-CS-1.3, Rev. 1.3, §5.12.1, printed pages 174-175, PDF pages 174-175; Source: NVME-BASE-2.4, Rev. 2.4, §8.1.3.1; 8.1.27.4.2, printed pages 587,721, PDF pages 613,747

### Q31. How does “Restrictions and verification reads” apply to a concrete calculation or operational scenario?

<!-- qa:base-boot-telemetry-sanitize-sanitize-read-example -->

**Answer.**

A verification read with PRCHK=000b and STC=0, readable allocated LBAs, and no other abort cause completes as Successful Media Verification Read. Requesting PI checking changes the expected branch to Invalid Field in Command.

> Source: NVME-BASE-2.4, Rev. 2.4, §8.1.27.5; 5.1.1-5.1.2, printed pages 178-181,730-732, PDF pages 204-207,756-758; Source: NVME-BASE-2.4, Rev. 2.4, §8.1.27.5, printed pages 730-732, PDF pages 756-758; Source: NVME-NVM-CS-1.3, Rev. 1.3, §4.1.7; 5.12, printed pages 113,173-175, PDF pages 113,173-175; Source: NVME-NVM-CS-1.3, Rev. 1.3, §5.12, printed pages 174, PDF pages 174; Source: NVME-NVM-CS-1.3, Rev. 1.3, §5.12.1, printed pages 174-175, PDF pages 174-175; Source: NVME-BASE-2.4, Rev. 2.4, §8.1.3.1; 8.1.27.4.2, printed pages 587,721, PDF pages 613,747

### Q32. What misinterpretation is most likely in “Restrictions and verification reads”, and how is it debugged?

<!-- qa:base-boot-telemetry-sanitize-sanitize-read-pitfall -->

**Answer.**

Do not assume all Get Log Page requests are permitted during subsystem sanitize; 07h/08h are absent from Figure 144. Namespace sanitize restrictions require a separate attached/target-scope evaluation.

> Source: NVME-BASE-2.4, Rev. 2.4, §8.1.27.5; 5.1.1-5.1.2, printed pages 178-181,730-732, PDF pages 204-207,756-758; Source: NVME-BASE-2.4, Rev. 2.4, §8.1.27.5, printed pages 730-732, PDF pages 756-758; Source: NVME-NVM-CS-1.3, Rev. 1.3, §4.1.7; 5.12, printed pages 113,173-175, PDF pages 113,173-175; Source: NVME-NVM-CS-1.3, Rev. 1.3, §5.12, printed pages 174, PDF pages 174; Source: NVME-NVM-CS-1.3, Rev. 1.3, §5.12.1, printed pages 174-175, PDF pages 174-175; Source: NVME-BASE-2.4, Rev. 2.4, §8.1.3.1; 8.1.27.4.2, printed pages 587,721, PDF pages 613,747
