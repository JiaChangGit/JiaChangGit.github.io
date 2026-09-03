---
layout: post
read_time: true
show_date: true
title: "NVMe Base 2.4: Device Self-test, HMB, Doorbell Emulation, and Vendor Commands"
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
[繁體中文]({% post_url 2026-09-02-nvme-base-self-test-hmb-emulation-zh-tw %})


# NVMe Base 2.4: Device Self-test, HMB, Doorbell Emulation, and Vendor Commands

Purpose: a source-located engineering report for GitHub Pages and a 100-minute presentation.

Scope: Base §§5.2.6, 5.2.13.1.7, 5.2.30.2.3, 8.1.8, 8.1.29, 8.2.3, and 8.2.4, plus NVM Command Set 1.3 §4.1.4.3; includes the minimum dependency slice needed to construct commands and gate capabilities. Only PCIe/memory-based and common NVMe content appears below.

## Source versions

NVM Express Base Specification, Revision 2.4
NVM Express NVM Command Set Specification, Revision 1.3

Verification date: 2026-09-02. No additional errata, ECNs, Technical Proposals, controller-vendor documents, or source text from the external PCI Express Base Specification are included.

## Reading map

```text
Discover capability -> Construct command / memory -> Controller background work -> Read completion / log evidence
```

Three engineering tracks share one rule: establish capability and ownership boundaries, submit the command or MMIO notification, then prove the result with CQEs, log pages, and memory-lifecycle evidence.

## Normative language

shall is mandatory, may permits a choice, should expresses a preferred recommendation, and optional means support is not required. The report preserves these terms and never promotes one into another.

## Acronyms first: complete glossary

Every abbreviation below is introduced before it is used in the slide narrative. The term alone is never enough: retain owner, width, unit, scope, and state.

| Acronym / term | Plain-language meaning | Source |
|---|---|---|
| `DST` | Device Self-test, a background operation using diagnostic segments to check a controller and optional namespace media. | NVME-BASE-2.4 Rev. 2.4, §5.2.14.2.1, 8.1.8, printed pp. 352-358, 614, PDF pp. 378-384, 640 |
| `OACS.DSTS` | The Device Self-test Supported bit in Optional Admin Command Support, gating availability of the command. | NVME-BASE-2.4 Rev. 2.4, §5.2.14.2.1, 8.1.8, printed pp. 352-358, 614, PDF pp. 378-384, 640 |
| `STC` | Self-test Code is the Device Self-test CDW10 action nibble; STC in a result entry instead means Status Code and is gated by SCVLD. | NVME-BASE-2.4 Rev. 2.4, §5.2.6, printed pp. 199-200, PDF pp. 225-226 |
| `DSTP` | Device Self-test Parameter, CDW15 with vendor-defined meaning only for vendor-specific STC Eh. | NVME-BASE-2.4 Rev. 2.4, §5.2.6, printed pp. 199-200, PDF pp. 225-226 |
| `DSTO` | Device Self-test Options, the Identify Controller field reporting refresh and concurrency options. | NVME-BASE-2.4 Rev. 2.4, §5.2.14.2.1, 8.1.8, printed pp. 352-358, 614, PDF pp. 378-384, 640 |
| `SDSO` | Single Device Self-test Operation, the bit selecting one subsystem-wide operation or one per controller. | NVME-BASE-2.4 Rev. 2.4, §5.2.14.2.1, 8.1.8, printed pp. 352-358, 614, PDF pp. 378-384, 640 |
| `EDSTT` | Extended Device Self-test Time, the nominal extended-test duration in minutes at power state 0. | NVME-BASE-2.4 Rev. 2.4, §8.1.8.1-8.1.8.2, printed pp. 615-616, PDF pp. 641-642 |
| `DSTOS` | Device Self-test Operation Status, the LID 06h nibble identifying the current operation. | NVME-BASE-2.4 Rev. 2.4, §5.2.13.1.7, printed pp. 229-230, PDF pp. 255-256 |
| `DSTCS` | Device Self-test Completion Status, the LID 06h completion percentage from 0 through 100. | NVME-BASE-2.4 Rev. 2.4, §5.2.13.1.7, printed pp. 229-230, PDF pp. 255-256 |
| `DSTR` | Device Self-test Result, the result-entry nibble identifying success, abort, or segment failure. | NVME-BASE-2.4 Rev. 2.4, §5.2.13.1.7, printed pp. 231, PDF pp. 257 |
| `SEGN` | Segment Number, identifying the first failed diagnostic segment only when DSTR is 7h. | NVME-BASE-2.4 Rev. 2.4, §5.2.13.1.7, printed pp. 231, PDF pp. 257 |
| `VDINFO` | Valid Diagnostic Information, the bitmap independently gating NSID, FLBA, SCT, and SC. | NVME-BASE-2.4 Rev. 2.4, §5.2.13.1.7, printed pp. 231-232, PDF pp. 257-258 |
| `FVLD` | Failing LBA Valid, the validity bit determining whether FLBA may be interpreted. | NVME-NVM-CS-1.3 Rev. 1.3, §4.1.4.3, printed pp. 76, PDF pp. 76 |
| `FLBA` | Failing LBA, defined by the NVM Command Set as one logical block address that caused self-test failure. | NVME-NVM-CS-1.3 Rev. 1.3, §4.1.4.3, printed pp. 76, PDF pp. 76 |
| `POH` | Power On Hours, accumulated power-on hours when a self-test result is created, excluding specified low-power time. | NVME-BASE-2.4 Rev. 2.4, §5.2.13.1.7, 8.1.8, printed pp. 229-232, 614-616, PDF pp. 255-258, 640-642 |
| `HMB` | Host Memory Buffer, volatile memory ranges allocated by the host for exclusive controller use while enabled. | NVME-BASE-2.4 Rev. 2.4, §5.2.30.2.3, 8.2.4, printed pp. 515-516, 744, PDF pp. 541-542, 770 |
| `HMPRE` | Host Memory Buffer Preferred Size, the controller's preferred allocation in 4-KiB units. | NVME-BASE-2.4 Rev. 2.4, §5.2.14.2.1, 8.2.4, printed pp. 357, 362, 744, PDF pp. 383, 388, 770 |
| `HMMIN` | Host Memory Buffer Minimum Size, the controller's minimum requested size in 4-KiB units. | NVME-BASE-2.4 Rev. 2.4, §5.2.14.2.1, 8.2.4, printed pp. 357, 362, 744, PDF pp. 383, 388, 770 |
| `HMMINDS` | Host Memory Buffer Minimum Descriptor Entry Size, the minimum usable descriptor size in 4-KiB units. | NVME-BASE-2.4 Rev. 2.4, §5.2.14.2.1, 8.2.4, printed pp. 357, 362, 744, PDF pp. 383, 388, 770 |
| `HMMAXD` | Host Memory Maximum Descriptor Entries, the maximum descriptor-entry count the controller can use. | NVME-BASE-2.4 Rev. 2.4, §5.2.14.2.1, 8.2.4, printed pp. 357, 362, 744, PDF pp. 383, 388, 770 |
| `HMDL` | Host Memory Descriptor List, a contiguous host-memory array of 16-byte HMB descriptors. | NVME-BASE-2.4 Rev. 2.4, §5.2.30.2.3, printed pp. 517-518, PDF pp. 543-544 |
| `HMDLEC` | Host Memory Descriptor List Entry Count, the number of valid entries in the HMDL. | NVME-BASE-2.4 Rev. 2.4, §5.2.30, 5.2.30.2.3, printed pp. 456-459, 516-518, PDF pp. 482-485, 542-544 |
| `HSIZE` | Host Memory Buffer Size, the total HMB size in CC.MPS memory-page units. | NVME-BASE-2.4 Rev. 2.4, §5.2.30.2.3, printed pp. 516-518, PDF pp. 542-544 |
| `EHM` | Enable Host Memory, the bit enabling or disabling controller use of HMB. | NVME-BASE-2.4 Rev. 2.4, §5.2.30.2.3, printed pp. 515-516, PDF pp. 541-542 |
| `MR` | Memory Return, indicating return of exactly the same previous HMB size, addresses, descriptors, and contents. | NVME-BASE-2.4 Rev. 2.4, §8.2.4, printed pp. 744, PDF pp. 770 |
| `HMNARE` | Host Memory Non-operational Access Restriction Enable, the bit configuring non-operational HMB-access policy. | NVME-BASE-2.4 Rev. 2.4, §5.2.30.2.3, printed pp. 516-519, PDF pp. 542-545 |
| `HMNAR` | Host Memory Non-operational Access Restricted, the state bit reporting whether restriction is currently active. | NVME-BASE-2.4 Rev. 2.4, §5.2.30.2.3, printed pp. 516-519, PDF pp. 542-545 |
| `BADD` | Buffer Address, the CC.MPS-aligned memory-page address in an HMB descriptor. | NVME-BASE-2.4 Rev. 2.4, §5.2.30.2.3, printed pp. 517-518, PDF pp. 543-544 |
| `BSIZE` | Buffer Size, the contiguous range length in CC.MPS pages in an HMB descriptor. | NVME-BASE-2.4 Rev. 2.4, §5.2.30.2.3, printed pp. 517-518, PDF pp. 543-544 |
| `DSTRD` | Doorbell Stride, the CAP field determining spacing between adjacent doorbell registers. | NVME-BASE-2.4 Rev. 2.4, §3.1.4.1, 8.2.3, printed pp. 56, 744, PDF pp. 82, 770 |
| `NDT` | Number of Dwords in Data Transfer, the actual data-dword count in the standard vendor-specific format. | NVME-BASE-2.4 Rev. 2.4, §4.1.1, 8.1.29, printed pp. 143, 733, PDF pp. 169, 759 |
| `NDM` | Number of Dwords in Metadata Transfer, the actual metadata-dword count in the standard vendor-specific format. | NVME-BASE-2.4 Rev. 2.4, §4.1.1, 8.1.29, printed pp. 143, 733, PDF pp. 169, 759 |
| `AVSCC` | Admin Vendor Specific Command Configuration, the Identify field reporting the vendor-specific Admin-command format. | NVME-BASE-2.4 Rev. 2.4, §5.2.14.2.1, 8.1.29, printed pp. 356, 374, 733, PDF pp. 382, 400, 759 |
| `ICSVSCC` | I/O Command Set Vendor Specific Command Configuration, the Identify field reporting the vendor-specific I/O-command format. | NVME-BASE-2.4 Rev. 2.4, §5.2.14.2.1, 8.1.29, printed pp. 356, 374, 733, PDF pp. 382, 400, 759 |
| `VSCF` | Vendor Specific Command Format, the AVSCC bit indicating whether Admin commands use Figure 94. | NVME-BASE-2.4 Rev. 2.4, §5.2.14.2.1, 8.1.29, printed pp. 356, 374, 733, PDF pp. 382, 400, 759 |
| `SNVSCF` | Same NVM Vendor Specific Command Format, the ICSVSCC bit indicating whether I/O commands use Figure 94. | NVME-BASE-2.4 Rev. 2.4, §5.2.14.2.1, 8.1.29, printed pp. 356, 374, 733, PDF pp. 382, 400, 759 |
| `NSID` | Namespace Identifier, a controller-visible numeric handle for a namespace; the identifier is not the namespace object itself. | NVME-BASE-2.4 Rev. 2.4, §5.2.6, printed pp. 199, PDF pp. 225 |
| `CQE` | Completion Queue Entry, one completion-result structure in a CQ. | NVME-BASE-2.4 Rev. 2.4, §5.2.6, printed pp. 201, PDF pp. 227 |
| `FID` | Feature Identifier, the eight-bit identifier selecting a function in Get/Set Features. | NVME-BASE-2.4 Rev. 2.4, §5.2.30, 5.2.30.2.3, printed pp. 456-459, 516-518, PDF pp. 482-485, 542-544 |
| `SEL` | Select, the Get Features field choosing current, default, saved, or supported-capabilities view. | NVME-BASE-2.4 Rev. 2.4, §5.2.12, 5.2.30.2.3, printed pp. 209-212, 518-519, PDF pp. 235-238, 544-545 |

## Visual atlas: locate the system before reading fields

Each redraw answers a different question: architecture locates components, sequence shows ownership, decode turns bits into engineering values, and state views preserve failure evidence. These are teaching redraws, not copies of specification artwork.

### Visual 01: Start with three boundaries: operation, memory ownership, and encoded address

**View type:** `architecture`

```text
[Identify capability]
  ├─ [Choose engineering track]
  ├─ [Submit command / allocate memory]
  ├─ [Controller enters new state]
  ├─ [CQE/log/memory fence]
  └─ [Debug first broken boundary]
```

**Question answered:** These sections do not describe one feature. Device Self-test manages a background diagnostic operation, HMB manages ownership transfer of host memory, and DSTRD plus the vendor-command format turn encoded values into safe memory accesses. The shared method is to locate a capability gate, identify the state or ownership transition, and then collect observable evidence.

**Supporting Figures:** Figure 36, Figure 94, Figure 176, Figure 545

**Sources:** NVME-BASE-2.4 Rev. 2.4, §5.2.6, printed pp. 201, PDF pp. 227; NVME-BASE-2.4 Rev. 2.4, §5.2.30.2.3, 8.2.4, printed pp. 515-516, 744, PDF pp. 541-542, 770; NVME-BASE-2.4 Rev. 2.4, §3.1.4.1, 8.2.3, printed pp. 56, 744, PDF pp. 82, 770; NVME-BASE-2.4 Rev. 2.4, §5.2.14.2.1, 8.1.29, printed pp. 356, 374, 733, PDF pp. 382, 400, 759

### Visual 02: Device Self-test: gate capability before submitting a background operation

**View type:** `state`

```text
[OACS.DSTS=1] → [Read SDSO/EDSTT] → [Choose NSID + STC] → [Submit Admin SQE] → [CQE: start accepted] → [Poll LID 06h]
timeout / failure ──→ preserve trigger + previous state + evidence
```

**Question answered:** Self-test is not a synchronous diagnostic RPC. The host first uses OACS.DSTS, DSTO.SDSO, and EDSTT to establish support, concurrency scope, and timing, then constructs the command from NSID and STC. When the Admin CQE returns, the background operation has only entered the lifecycle observed through LID 06h.

**Supporting Figures:** Figure 93, Figure 176, Figure 177, Figure 178, Figure 179, Figure 180, Figure 338

**Sources:** NVME-BASE-2.4 Rev. 2.4, §5.2.14.2.1, 8.1.8, printed pp. 352-358, 614, PDF pp. 378-384, 640; NVME-BASE-2.4 Rev. 2.4, §5.2.6, printed pp. 199, PDF pp. 225; NVME-BASE-2.4 Rev. 2.4, §5.2.6, printed pp. 199-200, PDF pp. 225-226; NVME-BASE-2.4 Rev. 2.4, §5.2.6, printed pp. 200, PDF pp. 226; NVME-BASE-2.4 Rev. 2.4, §5.2.6, printed pp. 201, PDF pp. 227

### Visual 03: LID 06h: decode current operation separately from twenty history entries

**View type:** `decode`

```text
[RAW: Get LID06 564 bytes] → [LOCATE: Read DSTOS/DSTCS] → [DECODE: Select newest RDS1]
[VALIDATE: Decode DSTC/DSTR] → [APPLY: Gate fields with VDINFO] → [EVIDENCE: NVM FLBA + timeline]
VALIDATE fail ──→ return to RAW evidence
```

**Question answered:** DSTOS/DSTCS in the header answer what is running now, while RDS1 through RDS20 answer how earlier operations ended. Each result then separates operation code, result reason, segment, validity bitmap, and diagnostic payload. The NVM Command Set gives FLBA an LBA meaning only when FVLD is one.

**Supporting Figures:** Figure 203, Figure 204, Figure 205, Figure 206, Figure 207, Figure 208, Figure 209, Figure 218, Figure 219, Figure 111, Figure 700, Figure 701

**Sources:** NVME-BASE-2.4 Rev. 2.4, §5.2.13, printed pp. 213-216, PDF pp. 239-242; NVME-BASE-2.4 Rev. 2.4, §5.2.13.1.7, printed pp. 229-230, PDF pp. 255-256; NVME-BASE-2.4 Rev. 2.4, §5.2.13.1.7, printed pp. 229-230, PDF pp. 255-256; NVME-BASE-2.4 Rev. 2.4, §5.2.13.1.7, printed pp. 231, PDF pp. 257; NVME-BASE-2.4 Rev. 2.4, §5.2.13.1.7, printed pp. 231-232, PDF pp. 257-258; NVME-NVM-CS-1.3 Rev. 1.3, §4.1.4.3, printed pp. 76, PDF pp. 76; NVME-BASE-2.4 Rev. 2.4, §5.2.13.1.7, 8.1.8, printed pp. 229-232, 614-616, PDF pp. 255-258, 640-642

### Visual 04: HMB: enable/disable completion is an ownership fence

**View type:** `state`

```text
[Read HMPRE/HMMIN/limits] → [Allocate pages + HMDL] → [Set FID0Dh EHM=1] → [Controller exclusive use] → [Set EHM=0] → [Disable CQE→host reclaim]
timeout / failure ──→ preserve trigger + previous state + evidence
```

**Question answered:** HMB is not merely controller cache. It is an ownership protocol: the host allocates pages and a descriptor list, stops writing after successful enable, the controller initializes and uses them, and the host disables HMB before reclaiming memory. Modification rights return only when the CQE is posted.

**Supporting Figures:** Figure 338, Figure 545, Figure 552, Figure 553

**Sources:** NVME-BASE-2.4 Rev. 2.4, §5.2.14.2.1, 8.2.4, printed pp. 357, 362, 744, PDF pp. 383, 388, 770; NVME-BASE-2.4 Rev. 2.4, §5.2.30.2.3, 8.2.4, printed pp. 515-516, 744, PDF pp. 541-542, 770; NVME-BASE-2.4 Rev. 2.4, §5.2.30.2.3, printed pp. 515-516, PDF pp. 541-542; NVME-BASE-2.4 Rev. 2.4, §8.2.4, printed pp. 744, PDF pp. 770

### Visual 05: HMB commands and descriptors: reconcile every size, count, and address with one page model

**View type:** `decode`

```text
[RAW: CC.MPS→page bytes] → [LOCATE: HMPRE/HMMIN→target bytes] → [DECODE: Split aligned ranges]
[VALIDATE: Write 16-byte entries] → [APPLY: sum(BSIZE)=HSIZE] → [EVIDENCE: Build CDW11..15]
VALIDATE fail ──→ return to RAW evidence
```

**Question answered:** HSIZE, BSIZE, and BADD use CC.MPS pages, while HMPRE, HMMIN, and HMMINDS use 4-KiB units. The unit systems are not interchangeable. HMDL is 16-byte aligned with fixed 16-byte entries, and HMDLEC is an entry count—not zero based and not a byte length.

**Supporting Figures:** Figure 197, Figure 198, Figure 200, Figure 463, Figure 464, Figure 466, Figure 545, Figure 546, Figure 547, Figure 548, Figure 549, Figure 550, Figure 551, Figure 552, Figure 553

**Sources:** NVME-BASE-2.4 Rev. 2.4, §5.2.30, 5.2.30.2.3, printed pp. 456-459, 516-518, PDF pp. 482-485, 542-544; NVME-BASE-2.4 Rev. 2.4, §5.2.30.2.3, printed pp. 517-518, PDF pp. 543-544; NVME-BASE-2.4 Rev. 2.4, §5.2.30.2.3, printed pp. 516-518, PDF pp. 542-544; NVME-BASE-2.4 Rev. 2.4, §5.2.12, 5.2.30.2.3, printed pp. 209-212, 518-519, PDF pp. 235-238, 544-545

### Visual 06: HMB across non-operational state, RTD3, and reset: three different boundaries

**View type:** `state`

```text
[HMB enabled] → [Optional HMNARE policy] → [Non-op→HMNAR state] → [Disable before RTD3/reset] → [Preserve or replace contents] → [MR=1 exact-match return]
timeout / failure ──→ preserve trigger + previous state + evidence
```

**Question answered:** HMNARE is access policy, HMNAR is current state, and MR says whether exactly the same prior contents are returned after reset or RTD3. They are not interchangeable. Controller Level Reset loses the assignment, RTD3 calls for release beforehand, and non-operational restriction only limits access in selected states.

**Supporting Figures:** Figure 338, Figure 545, Figure 552, Figure 553

**Sources:** NVME-BASE-2.4 Rev. 2.4, §5.2.30.2.3, printed pp. 516-519, PDF pp. 542-545; NVME-BASE-2.4 Rev. 2.4, §8.2.4, printed pp. 744, PDF pp. 770; NVME-BASE-2.4 Rev. 2.4, §8.2.4, printed pp. 744, PDF pp. 770

### Visual 07: DSTRD and NDT/NDM: decode to byte boundaries before memory access

**View type:** `decode`

```text
[RAW: Read capability bit/field] → [LOCATE: Select the correct formula] → [DECODE: Convert to byte stride/length]
[VALIDATE: Check overflow/alignment] → [APPLY: Perform MMIO/DMA] → [EVIDENCE: Retain raw+decoded trace]
VALIDATE fail ──→ return to RAW evidence
```

**Question answered:** Software emulators and vendor-command passthrough both handle untrusted encoded values. DSTRD becomes bytes through 2^(2+x); NDT/NDM are already actual dword counts and are multiplied by four without adding one. The formulas differ, but both prove address and length before MMIO or DMA.

**Supporting Figures:** Figure 36, Figure 93, Figure 94, Figure 338

**Sources:** NVME-BASE-2.4 Rev. 2.4, §3.1.4.1, 8.2.3, printed pp. 56, 744, PDF pp. 82, 770; NVME-BASE-2.4 Rev. 2.4, §8.2.3, printed pp. 744, PDF pp. 770; NVME-BASE-2.4 Rev. 2.4, §5.2.14.2.1, 8.1.29, printed pp. 356, 374, 733, PDF pp. 382, 400, 759; NVME-BASE-2.4 Rev. 2.4, §4.1.1, 8.1.29, printed pp. 143, 733, PDF pp. 169, 759; NVME-BASE-2.4 Rev. 2.4, §4.1.1, 8.1.29, printed pp. 143, 733, PDF pp. 169, 759; NVME-BASE-2.4 Rev. 2.4, §5.2.6, 5.2.30.2.3, 8.1.29, 8.2.3, printed pp. 199-201, 515-519, 733, 744, PDF pp. 225-227, 541-545, 759, 770

## Mental Model and complete teaching path

The modules follow engineering causality rather than specification-section order. Related Figures return at the point where they support the flow.

### Module 01: Start with three boundaries: operation, memory ownership, and encoded address

**Explanation.** These sections do not describe one feature. Device Self-test manages a background diagnostic operation, HMB manages ownership transfer of host memory, and DSTRD plus the vendor-command format turn encoded values into safe memory accesses. The shared method is to locate a capability gate, identify the state or ownership transition, and then collect observable evidence.

```text
Identify capability
  ↓
Choose engineering track
  ↓
Submit command / allocate memory
  ↓
Controller enters new state
  ↓
CQE/log/memory fence
  ↓
Debug first broken boundary
```

#### Comparison

| Item | What it answers | Engineering note |
|---|---|---|
| Self-test | Operation lifecycle | CQE + LID 06h |
| HMB | Exclusive-ownership lifecycle | Get FID 0Dh + disable CQE |
| Doorbell emulation | Encoded byte stride | MMIO address/write trace |
| Vendor command | Buffer-length contract | VSCF/SNVSCF + NDT/NDM |

**Informative example.** The same Successful Completion means only that a self-test operation started, but for HMB disable it returns ownership to the host. Equal status codes do not imply equal completion boundaries.

**Common mistake / debugging.** Do not reduce every topic to command success or failure. Record which transition succeeded, who currently owns memory, and which log or Get Features result is still required to prove the later outcome.

**Supporting sources:** NVME-BASE-2.4 Rev. 2.4, §5.2.6, printed pp. 201, PDF pp. 227; NVME-BASE-2.4 Rev. 2.4, §5.2.30.2.3, 8.2.4, printed pp. 515-516, 744, PDF pp. 541-542, 770; NVME-BASE-2.4 Rev. 2.4, §3.1.4.1, 8.2.3, printed pp. 56, 744, PDF pp. 82, 770; NVME-BASE-2.4 Rev. 2.4, §5.2.14.2.1, 8.1.29, printed pp. 356, 374, 733, PDF pp. 382, 400, 759

**Related Figures:** Figure 36, Figure 94, Figure 176, Figure 545

### Module 02: Device Self-test: gate capability before submitting a background operation

**Explanation.** Self-test is not a synchronous diagnostic RPC. The host first uses OACS.DSTS, DSTO.SDSO, and EDSTT to establish support, concurrency scope, and timing, then constructs the command from NSID and STC. When the Admin CQE returns, the background operation has only entered the lifecycle observed through LID 06h.

```text
OACS.DSTS=1
  ↓
Read SDSO/EDSTT
  ↓
Choose NSID + STC
  ↓
Submit Admin SQE
  ↓
CQE: start accepted
  ↓
Poll LID 06h
```

#### Comparison

| Item | What it answers | Engineering note |
|---|---|---|
| NSID=0 | Controller only | No namespace media |
| Active NSID | One namespace | Invalid and inactive status differ |
| NSID=FFFFFFFFh | All attached/accessible namespaces | Set is captured at start |
| STC=Fh | Abort current operation | Success does not prove one existed |

**Informative example.** To start a short test for namespace 5, use NSID 00000005h and STC 1h, so CDW10 is 00000001h and CDW15 is zero. Immediately issuing extended STC 2h should produce command-specific status 1Dh rather than a second operation.

**Common mistake / debugging.** The common failure is treating the CQE timestamp as test completion or checking only controller-local state when SDSO is one. Retain controller ID, NSID, STC, CDW15, CQE status, and the first subsequent LID 06h.

**Supporting sources:** NVME-BASE-2.4 Rev. 2.4, §5.2.14.2.1, 8.1.8, printed pp. 352-358, 614, PDF pp. 378-384, 640; NVME-BASE-2.4 Rev. 2.4, §5.2.6, printed pp. 199, PDF pp. 225; NVME-BASE-2.4 Rev. 2.4, §5.2.6, printed pp. 199-200, PDF pp. 225-226; NVME-BASE-2.4 Rev. 2.4, §5.2.6, printed pp. 200, PDF pp. 226; NVME-BASE-2.4 Rev. 2.4, §5.2.6, printed pp. 201, PDF pp. 227

**Related Figures:** Figure 93, Figure 176, Figure 177, Figure 178, Figure 179, Figure 180, Figure 338

### Module 03: LID 06h: decode current operation separately from twenty history entries

**Explanation.** DSTOS/DSTCS in the header answer what is running now, while RDS1 through RDS20 answer how earlier operations ended. Each result then separates operation code, result reason, segment, validity bitmap, and diagnostic payload. The NVM Command Set gives FLBA an LBA meaning only when FVLD is one.

```text
Get LID06 564 bytes
  ↓
Read DSTOS/DSTCS
  ↓
Select newest RDS1
  ↓
Decode DSTC/DSTR
  ↓
Gate fields with VDINFO
  ↓
NVM FLBA + timeline
```

#### Comparison

| Item | What it answers | Engineering note |
|---|---|---|
| DSTOS/DSTCS | Current state/progress | Ignore percentage when DSTOS=0 |
| DSTR=7h + SEGN | Known first failed segment | Ignore SEGN for other DSTR |
| FVLD + FLBA | One failing LBA | Not a list of every failed LBA |
| POH + STCT/STC | Failure context | Validity bits still apply |

**Informative example.** The complete log is 564 bytes or 141 dwords, so NUMD is 140 or 008Ch. With LSP 0 and RAE 0, CDW10 is 008C0006h. If RDS1.DSTS is 17h, high nibble 1h means short test and low nibble 7h means a known failed segment; only then read SEGN.

**Common mistake / debugging.** A parser must not declare media failure because FLBA is nonzero. Check DSTR, then FVLD and NSIDVLD, and only then decode bytes 23:16 under the NVM Command Set. Preserve the raw 28-byte result so a validity-decoding defect does not destroy evidence.

**Supporting sources:** NVME-BASE-2.4 Rev. 2.4, §5.2.13, printed pp. 213-216, PDF pp. 239-242; NVME-BASE-2.4 Rev. 2.4, §5.2.13.1.7, printed pp. 229-230, PDF pp. 255-256; NVME-BASE-2.4 Rev. 2.4, §5.2.13.1.7, printed pp. 229-230, PDF pp. 255-256; NVME-BASE-2.4 Rev. 2.4, §5.2.13.1.7, printed pp. 231, PDF pp. 257; NVME-BASE-2.4 Rev. 2.4, §5.2.13.1.7, printed pp. 231-232, PDF pp. 257-258; NVME-NVM-CS-1.3 Rev. 1.3, §4.1.4.3, printed pp. 76, PDF pp. 76; NVME-BASE-2.4 Rev. 2.4, §5.2.13.1.7, 8.1.8, printed pp. 229-232, 614-616, PDF pp. 255-258, 640-642

**Related Figures:** Figure 203, Figure 204, Figure 205, Figure 206, Figure 207, Figure 208, Figure 209, Figure 218, Figure 219, Figure 111, Figure 700, Figure 701

### Module 04: HMB: enable/disable completion is an ownership fence

**Explanation.** HMB is not merely controller cache. It is an ownership protocol: the host allocates pages and a descriptor list, stops writing after successful enable, the controller initializes and uses them, and the host disables HMB before reclaiming memory. Modification rights return only when the CQE is posted.

```text
Read HMPRE/HMMIN/limits
  ↓
Allocate pages + HMDL
  ↓
Set FID0Dh EHM=1
  ↓
Controller exclusive use
  ↓
Set EHM=0
  ↓
Disable CQE→host reclaim
```

#### Comparison

| Item | What it answers | Engineering note |
|---|---|---|
| Before enable | Host owns and initializes descriptors | Validate alignment/count |
| After enable CQE | Controller exclusive use | Host shall not write |
| Disable in flight | Controller may still retrieve data | Host still waits |
| After disable CQE | Host may modify/reclaim | Record fence timestamp |

**Informative example.** If a driver removes DMA mappings after issuing EHM zero but before its CQE, the controller may still retrieve required data; that is a use-after-unmap. The correct fence is disable completion, not the SQ-tail doorbell write.

**Common mistake / debugging.** Treating enable completion as shared host/controller access creates a data race. Track write protection and DMA ownership for HMDL and every range, and release them only after disable completion.

**Supporting sources:** NVME-BASE-2.4 Rev. 2.4, §5.2.14.2.1, 8.2.4, printed pp. 357, 362, 744, PDF pp. 383, 388, 770; NVME-BASE-2.4 Rev. 2.4, §5.2.30.2.3, 8.2.4, printed pp. 515-516, 744, PDF pp. 541-542, 770; NVME-BASE-2.4 Rev. 2.4, §5.2.30.2.3, printed pp. 515-516, PDF pp. 541-542; NVME-BASE-2.4 Rev. 2.4, §8.2.4, printed pp. 744, PDF pp. 770

**Related Figures:** Figure 338, Figure 545, Figure 552, Figure 553

### Module 05: HMB commands and descriptors: reconcile every size, count, and address with one page model

**Explanation.** HSIZE, BSIZE, and BADD use CC.MPS pages, while HMPRE, HMMIN, and HMMINDS use 4-KiB units. The unit systems are not interchangeable. HMDL is 16-byte aligned with fixed 16-byte entries, and HMDLEC is an entry count—not zero based and not a byte length.

```text
CC.MPS→page bytes
  ↓
HMPRE/HMMIN→target bytes
  ↓
Split aligned ranges
  ↓
Write 16-byte entries
  ↓
sum(BSIZE)=HSIZE
  ↓
Build CDW11..15
```

#### Comparison

| Item | What it answers | Engineering note |
|---|---|---|
| HMPRE/HMMIN | 4-KiB units | Capability request |
| HSIZE/BSIZE | CC.MPS units | Configured memory |
| HMDL address | 16-byte aligned | CDW13 low + CDW14 high |
| BADD | CC.MPS aligned | BSIZE=0 entry ignored |

**Informative example.** With CC.MPS zero and HSIZE 64, HMB is 256 KiB. HMDL 00000012_34567000h and HMDLEC 2 produce CDW13 34567000h, CDW14 00000012h, and CDW15 2. Two BSIZE-32 ranges are 128 KiB each, totaling 256 KiB.

**Common mistake / debugging.** A common error copies HMPRE directly into HSIZE while CC.MPS is 8 KiB, or sets HMDLEC two while mapping one 16-byte entry. Log capability units, CC.MPS, every BADD/BSIZE, page sum, and command dwords together.

**Supporting sources:** NVME-BASE-2.4 Rev. 2.4, §5.2.30, 5.2.30.2.3, printed pp. 456-459, 516-518, PDF pp. 482-485, 542-544; NVME-BASE-2.4 Rev. 2.4, §5.2.30.2.3, printed pp. 517-518, PDF pp. 543-544; NVME-BASE-2.4 Rev. 2.4, §5.2.30.2.3, printed pp. 516-518, PDF pp. 542-544; NVME-BASE-2.4 Rev. 2.4, §5.2.12, 5.2.30.2.3, printed pp. 209-212, 518-519, PDF pp. 235-238, 544-545

**Related Figures:** Figure 197, Figure 198, Figure 200, Figure 463, Figure 464, Figure 466, Figure 545, Figure 546, Figure 547, Figure 548, Figure 549, Figure 550, Figure 551, Figure 552, Figure 553

### Module 06: HMB across non-operational state, RTD3, and reset: three different boundaries

**Explanation.** HMNARE is access policy, HMNAR is current state, and MR says whether exactly the same prior contents are returned after reset or RTD3. They are not interchangeable. Controller Level Reset loses the assignment, RTD3 calls for release beforehand, and non-operational restriction only limits access in selected states.

```text
HMB enabled
  ↓
Optional HMNARE policy
  ↓
Non-op→HMNAR state
  ↓
Disable before RTD3/reset
  ↓
Preserve or replace contents
  ↓
MR=1 exact-match return
```

#### Comparison

| Item | What it answers | Engineering note |
|---|---|---|
| HMNARE | Configured policy | Requires CTRATT.HMBR |
| HMNAR | Current restriction state | May be zero in operational state |
| MR=1 | Return identical old HMB | Same size/address/list/content |
| MR=0 | New undefined contents | Controller initializes again |

**Informative example.** If the allocator returns the same pages after resume but moves HMDL to a new address, MR cannot be one because the descriptor-list address must also match exactly. Enable it as a new MR-zero allocation.

**Common mistake / debugging.** Do not hash only data pages. MR validation compares HSIZE, HMDL address, HMDLEC, every descriptor, and all HMB contents. NOPPME is also not an HMNARE control; the specification explicitly separates them.

**Supporting sources:** NVME-BASE-2.4 Rev. 2.4, §5.2.30.2.3, printed pp. 516-519, PDF pp. 542-545; NVME-BASE-2.4 Rev. 2.4, §8.2.4, printed pp. 744, PDF pp. 770; NVME-BASE-2.4 Rev. 2.4, §8.2.4, printed pp. 744, PDF pp. 770

**Related Figures:** Figure 338, Figure 545, Figure 552, Figure 553

### Module 07: DSTRD and NDT/NDM: decode to byte boundaries before memory access

**Explanation.** Software emulators and vendor-command passthrough both handle untrusted encoded values. DSTRD becomes bytes through 2^(2+x); NDT/NDM are already actual dword counts and are multiplied by four without adding one. The formulas differ, but both prove address and length before MMIO or DMA.

```text
Read capability bit/field
  ↓
Select the correct formula
  ↓
Convert to byte stride/length
  ↓
Check overflow/alignment
  ↓
Perform MMIO/DMA
  ↓
Retain raw+decoded trace
```

#### Comparison

| Item | What it answers | Engineering note |
|---|---|---|
| DSTRD | 2^(2+x) bytes | 0→4 B; 4→64 B |
| NDT | Value×4 data bytes | Not zero based |
| NDM | Value×4 metadata bytes | Independent buffer bound |
| VSCF/SNVSCF | Format gate | Admin and I/O are separate |

**Informative example.** An emulator with DSTRD 4 gets a 64-byte stride and can place doorbells on discrete cachelines. Vendor-command NDT 0100h is 256 dwords or 1024 bytes—not 1028 bytes. Retain both raw encoding and decoded bytes for each.

**Common mistake / debugging.** A helper that treats every NVMe length as zero based adds four bytes to NDT/NDM. Multiplying DSTRD directly by four also fails for nonzero values. Bind each field's formula to its owning Figure.

**Supporting sources:** NVME-BASE-2.4 Rev. 2.4, §3.1.4.1, 8.2.3, printed pp. 56, 744, PDF pp. 82, 770; NVME-BASE-2.4 Rev. 2.4, §8.2.3, printed pp. 744, PDF pp. 770; NVME-BASE-2.4 Rev. 2.4, §5.2.14.2.1, 8.1.29, printed pp. 356, 374, 733, PDF pp. 382, 400, 759; NVME-BASE-2.4 Rev. 2.4, §4.1.1, 8.1.29, printed pp. 143, 733, PDF pp. 169, 759; NVME-BASE-2.4 Rev. 2.4, §4.1.1, 8.1.29, printed pp. 143, 733, PDF pp. 169, 759; NVME-BASE-2.4 Rev. 2.4, §5.2.6, 5.2.30.2.3, 8.1.29, 8.2.3, printed pp. 199-201, 515-519, 733, 744, PDF pp. 225-227, 541-545, 759, 770

**Related Figures:** Figure 36, Figure 93, Figure 94, Figure 338

## Source-located specification findings

The mental model above explains causality. This section preserves each source-located conclusion and its normative strength for speaker notes and review.

### 1. Gate self-test capability and concurrency scope

<!-- claim:BASEDIAGMEM-SELFTEST-GATE -->

Before starting Device Self-test, read Identify Controller. OACS.DSTS gates command support, EDSTT gives the nominal extended-operation time in minutes at power state 0, and DSTO.SDSO selects one subsystem-wide operation versus one operation per controller. These fields answer different questions.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.14.2.1, 8.1.8, printed pages 352-358, 614, PDF pages 378-384, 640

### 2. NSID selects the test scope

<!-- claim:BASEDIAGMEM-SELFTEST-NSID -->

Device Self-test is performed by the controller that receives the command. NSID 00000000h tests only the controller, 00000001h through FFFFFFFEh select one namespace, and FFFFFFFFh includes every attached namespace accessible through that controller when the operation starts. Invalid and inactive NSIDs produce different status results.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.6, printed pages 199, PDF pages 225

### 3. STC and CDW15 command encoding

<!-- claim:BASEDIAGMEM-SELFTEST-STC -->

CDW10.STC[3:0] selects the action: 1h short, 2h extended, 3h Host-Initiated Refresh, Eh vendor specific, and Fh abort; other encodings are reserved. CDW15.DSTP is vendor specific only when STC is Eh and is reserved otherwise.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.6, printed pages 199-200, PDF pages 225-226

### 4. State matrix while an operation is active

<!-- claim:BASEDIAGMEM-SELFTEST-INPROGRESS -->

When an operation is already running, a new short, extended, or Host-Initiated Refresh request is aborted with Device Self-test in Progress; a new vendor-specific request remains vendor specific. STC Fh instead aborts the current operation, creates the newest result, clears current status, and then completes successfully in that order.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.6, printed pages 200, PDF pages 226

### 5. A CQE is not test completion

<!-- claim:BASEDIAGMEM-SELFTEST-COMPLETION -->

The Admin CQE for Device Self-test proves that the start or abort action was processed, not that the background test finished. Command-specific status 1Dh means an operation is already in progress; software records the CQE separately from later LID 06h evidence.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.6, printed pages 201, PDF pages 227

### 6. Background-test suspend/resume contract

<!-- claim:BASEDIAGMEM-SELFTEST-BACKGROUND -->

Device Self-test is background work composed of vendor-specific segments. If another command requires suspension, the controller shall suspend the self-test, process and complete that command, and then resume the self-test in order. Which commands may run concurrently remains vendor specific.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §8.1.8, printed pages 614, PDF pages 640

### 7. Reset differences between short and extended tests

<!-- claim:BASEDIAGMEM-SELFTEST-TIMING -->

A short operation should finish within two minutes and is aborted by a Controller Level Reset. An extended operation should finish within EDSTT, shall persist across Controller Level Reset and power restoration, and resumes afterward. The two operations cannot share one reset expectation.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §8.1.8.1-8.1.8.2, printed pages 615-616, PDF pages 641-642

### 8. Format, sanitize, and abort conditions

<!-- claim:BASEDIAGMEM-SELFTEST-ABORTS -->

Both short and extended operations are aborted by an applicable Format NVM command, sanitize start, or STC Fh, and may be aborted when the namespace is removed from inventory. Figure 701 shows that Format NSID and secure-erase selections affect whether abort is required; the opcode alone is insufficient.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §8.1.8.1-8.1.8.2, printed pages 615-616, PDF pages 641-642

### 9. Constructing the 564-byte LID 06h command

<!-- claim:BASEDIAGMEM-SELFTEST-LOG-COMMAND -->

The minimum Get Log Page slice for LID 06h uses LID 06h, LSP 0, RAE selected by event policy, NUMD for 564 bytes, LPOL/LPOU 0, OT 0, CSI 0, and UIDX 0. 564 bytes are 141 dwords, so zero-based NUMD is 140 or 008Ch; with RAE 0, CDW10 is 008C0006h.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13, printed pages 213-216, PDF pages 239-242

### 10. Current operation and completion percentage

<!-- claim:BASEDIAGMEM-SELFTEST-CURRENT -->

In LID 06h, byte 0 DSTOS identifies the current operation and byte 1 DSTCS[6:0] is the completion percentage; the host should ignore DSTCS when DSTOS is zero. When an operation completes or is aborted, the controller creates a result entry before clearing in-progress status to zero.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.7, printed pages 229-230, PDF pages 255-256

### 11. Twenty newest-first results

<!-- claim:BASEDIAGMEM-SELFTEST-HISTORY -->

LID 06h retains 20 results of 28 bytes each, with RDS1 always the most recently completed or aborted operation. An unused entry uses DSTR Fh and DSTC 0h, while the host ignores its other fields; residual nonzero bytes are not history records.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.7, printed pages 229-230, PDF pages 255-256

### 12. Conditional DSTS and SEGN decoding

<!-- claim:BASEDIAGMEM-SELFTEST-RESULT -->

In each result DSTS, the high-nibble DSTC records the original self-test code and low-nibble DSTR records the completion or abort reason. SEGN identifies the first failed segment only when DSTR is 7h and is ignored for other DSTR values.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.7, printed pages 231, PDF pages 257

### 13. VDINFO contains four independent validity gates

<!-- claim:BASEDIAGMEM-SELFTEST-VALIDITY -->

VDINFO NSIDVLD, FVLD, SCTVLD, and SCVLD are independent validity gates. NSID, FLBA, STCT, and STC are interpreted only when their corresponding bit is one; validate the bit before the value instead of inferring validity from nonzero data.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.7, printed pages 231-232, PDF pages 257-258

### 14. NVM Command Set completes FLBA semantics

<!-- claim:BASEDIAGMEM-SELFTEST-NVM-FLBA -->

Base leaves Figure 219 FLBA to the applicable I/O Command Set. NVM Command Set 1.3 defines bytes 23:16 as the logical block address that caused the failure; when multiple logical blocks fail, only one is reported, and it is valid only when FVLD is one.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-NVM-CS-1.3, Rev. 1.3, §4.1.4.3, printed pages 76, PDF pages 76

### 15. Reconstruct self-test across three timestamps

<!-- claim:BASEDIAGMEM-SELFTEST-DEBUG -->

Debugging separates command, current state, and historical result into three timestamps: retain STC/NSID/CQE, poll DSTOS/DSTCS, and after completion retain DSTS, SEGN, VDINFO, POH, NSID, FLBA, STCT, STC, and vendor bytes. This distinguishes command rejection, operation abort, and media failure.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.7, 8.1.8, printed pages 229-232, 614-616, PDF pages 255-258, 640-642

### 16. HMB capability and descriptor limits

<!-- claim:BASEDIAGMEM-HMB-CAPABILITY -->

HMPRE zero means HMB is unsupported; a nonzero value is the preferred size in 4-KiB units, while HMMIN gives the minimum request. HMMINDS and HMMAXD constrain descriptors. The controller shall still function correctly when the host cannot provide HMB.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.14.2.1, 8.2.4, printed pages 357, 362, 744, PDF pages 383, 388, 770

### 17. HMB is an ownership transfer

<!-- claim:BASEDIAGMEM-HMB-OWNERSHIP -->

HMB is host-allocated memory leased exclusively to the controller. After successful Set Features enable, the host shall stop writing both the descriptor list and every described memory range until disable completes. This is an ownership transfer, not merely a performance hint.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.2.3, 8.2.4, printed pages 515-516, 744, PDF pages 541-542, 770

### 18. Set Features layout for FID 0Dh

<!-- claim:BASEDIAGMEM-HMB-SET-COMMAND -->

Set Features uses FID 0Dh. CDW11 holds EHM, MR, and HMNARE; CDW12 holds HSIZE; CDW13/14 form the 64-bit HMDL address; and CDW15 is HMDLEC. The HMDL address is 16-byte aligned, and HMDLEC zero returns Invalid Field in Command.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30, 5.2.30.2.3, printed pages 456-459, 516-518, PDF pages 482-485, 542-544

### 19. HMDL and descriptor page math

<!-- claim:BASEDIAGMEM-HMB-DESCRIPTORS -->

HMDL is a contiguous array of 16-byte descriptors. Each entry BADD is aligned to the CC.MPS memory-page size, and BSIZE gives a contiguous length in the same page units. The controller ignores an entry whose BSIZE is zero, and HSIZE is reconciled with the usable descriptor-page total.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.2.3, printed pages 517-518, PDF pages 543-544

### 20. Complete 256-KiB HMB calculation

<!-- claim:BASEDIAGMEM-HMB-NUMERIC -->

Informative example: CC.MPS zero means a 4-KiB page, so HSIZE 64 means 256 KiB. For HMDL 00000012_34567000h and HMDLEC 2, CDW13 is 34567000h, CDW14 is 00000012h, and CDW15 is 00000002h. Two descriptors of BSIZE 32 pages each total exactly 64 pages.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.2.3, printed pages 516-518, PDF pages 542-544

### 21. Enable/disable completion fence

<!-- claim:BASEDIAGMEM-HMB-SEQUENCE -->

Reissuing EHM one while HMB is already enabled is aborted with Command Sequence Error; issuing EHM zero while disabled succeeds without action. Before disable completion, the controller should retrieve needed data; only the posted CQE means the host may safely modify or reclaim the buffer.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.2.3, printed pages 515-516, PDF pages 541-542

### 22. Get Features separates policy from state

<!-- claim:BASEDIAGMEM-HMB-GET -->

Get Features uses FID 0Dh. On successful SEL other than supported capabilities, CQE.DW0 returns EHM, HMNARE, and HMNAR, while the data buffer returns a 4-KiB Attributes structure containing HSIZE, HMDL address, and HMDLEC. Enabled and currently access-restricted are different states.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.12, 5.2.30.2.3, printed pages 209-212, 518-519, PDF pages 235-238, 544-545

### 23. HMNARE and HMNAR are different

<!-- claim:BASEDIAGMEM-HMB-NONOP -->

HMNARE may be enabled only when Identify.CTRATT.HMBR is one. HMNARE is policy, while HMNAR reports whether a non-operational state currently restricts the controller; Admin commands and background operations initiated by them are explicit exceptions. NOPPME does not alter this HMB restriction.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.2.3, printed pages 516-519, PDF pages 542-545

### 24. Memory Return after reset or RTD3

<!-- claim:BASEDIAGMEM-HMB-RESET-RTD3 -->

HMB is not persistent in the controller across Controller Level Reset. The host should provide resources again afterward. MR one returns prior contents and requires the exact same size, descriptor-list address, descriptor-list contents, and HMB contents. Disable before RTD3, then select MR according to content preservation on resume.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §8.2.4, printed pages 744, PDF pages 770

### 25. Data correctness during surprise removal

<!-- claim:BASEDIAGMEM-HMB-SURPRISE -->

During surprise removal while HMB is in use, the controller shall ensure no data loss or data corruption. This does not make HMB contents persistent; it means internal correctness cannot depend on the host always completing the normal release flow.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §8.2.4, printed pages 744, PDF pages 770

### 26. DSTRD encoding to cacheline stride

<!-- claim:BASEDIAGMEM-DOORBELL-STRIDE -->

CAP.DSTRD produces a spacing of 2^(2+DSTRD) bytes. DSTRD values 0, 2, and 4 yield 4, 16, and 64 bytes; software emulation can use 64-byte spacing to separate doorbells by cacheline, while the expected hardware-interface value is 0h.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.1, 8.2.3, printed pages 56, 744, PDF pages 82, 770

### 27. Doorbell evidence chain for emulators

<!-- claim:BASEDIAGMEM-DOORBELL-DEBUG -->

Emulator debugging retains not only the doorbell value but CAP.DSTRD, computed byte stride, queue identifier, monitored cacheline, and write timestamp. Treating encoded DSTRD directly as bytes places queue notifications at the wrong address.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §8.2.3, printed pages 744, PDF pages 770

### 28. Gate Admin and I/O vendor formats independently

<!-- claim:BASEDIAGMEM-VENDOR-GATE -->

The standard Vendor Specific command format is optional. AVSCC.VSCF controls vendor-specific Admin commands, while ICSVSCC.SNVSCF controls vendor-specific I/O commands. Read the capabilities independently; one being set does not prove that the other command class uses Figure 94.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.14.2.1, 8.1.29, printed pages 356, 374, 733, PDF pages 382, 400, 759

### 29. Boundary-safe Figure 94 layout

<!-- claim:BASEDIAGMEM-VENDOR-FORMAT -->

Figure 94 retains common CDW0, NSID, metadata/data pointers, and CDW12-CDW15, while defining CDW10/11 as NDT/NDM. An unused NSID is cleared to zero; an invalid NSID used by the command returns Invalid Namespace or Format, while inactive-NSID behavior remains vendor specific.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §4.1.1, 8.1.29, printed pages 143, 733, PDF pages 169, 759

### 30. NDT/NDM are actual dword counts

<!-- claim:BASEDIAGMEM-VENDOR-LENGTH -->

NDT and NDM are actual dword counts, not zero based. NDT 00000100h means 256 dwords or 1024 bytes; a driver can validate application buffers with NDT/NDM to prevent data or metadata-transfer overflow. VSCF or SNVSCF still gates use of the standard format.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §4.1.1, 8.1.29, printed pages 143, 733, PDF pages 169, 759

### 31. Debug from the first broken boundary

<!-- claim:BASEDIAGMEM-BOUNDARY-DEBUG -->

All three tracks debug from the first broken boundary: self-test compares command, current status, and result; HMB compares capability, descriptor math, ownership, and disable CQE; emulation/vendor commands compare capability encoding, byte count or stride, and actual memory access.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.6, 5.2.30.2.3, 8.1.29, 8.2.3, printed pages 199-201, 515-519, 733, 744, PDF pages 225-227, 541-545, 759, 770

## Figure index

This report introduces all 36 in-scope Figures. Use the section links below for the 100-minute presentation path; every Figure remains available as an appendix item. 17 Figures are outside the main section range but are included to explain cited dependencies and necessary prerequisites.

- [§4.1](#section-4-1)

- [§5.2](#section-5-2)

- [§8.1](#section-8-1)

- [Referenced Figure dependencies (outside the main section range)](#section-dependency)

## Figure and field-table teaching reference

The source uses Figure numbers for diagrams and field-layout tables. No source artwork is reproduced; compact field and keyword indexes come from the locally verified PDFs.

<a id="section-4-1"></a>

### §4.1

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 111: Self-test Results Data Structure</strong></summary>

<!-- claim:BASEDIAGMEM-FIG-111-CLAIM figure-table:BASEDIAGMEM-FIG-111 -->

**SPEC.** Figure 111, "Self-test Results Data Structure": Defines the concrete layout or value relationships for Self-test Results Data Structure. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is FLBA, bytes 23:16, FVLD, one failed logical block.

#### Where this Figure fits

Figure 111 sits in §4.1.4.3 and acts as a layout checkpoint. Read it after the report mental model has established the owning object and before software turns FLBA into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a structure or capability field table. Locate it using the structure base and offset, read in byte/bit order, and separate capability gates, value encoding, and reserved areas. Presence in the table does not mean the function is supported.

#### Teaching redraw

```text
[Locate source: FLBA]
          ↓
[Extract field: bytes 23:16] → [Apply encoding: FVLD]
                                      ↓
[Validate evidence: one failed logical block]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `FLBA` | Failing LBA, defined by the NVM Command Set as one logical block address that caused self-test failure. |
| `bytes 23:16` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `FVLD` | Failing LBA Valid, the validity bit determining whether FLBA may be interpreted. |
| `one failed logical block` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §4.1.4.3 is the applicable context.
2. Decode FLBA at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check bytes 23:16 as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 111 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §4.1.4.3 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes FLBA, bytes 23:16, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §4.1.4.3, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 111. Annotate the bytes containing FLBA, decode them, and independently verify bytes 23:16. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of FLBA in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand FLBA and state its unit or object scope?
2. Can the reader explain why bytes 23:16 is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** FLBA, bytes 23:16, FVLD, one failed logical block

**Source keyword index:** none

> Source: NVME-NVM-CS-1.3, Rev. 1.3, §4.1.4.3, Figure 111, printed pages 76, PDF pages 76

</details>

<a id="section-5-2"></a>

### §5.2

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 176: Device Self-test Namespace Test Action</strong></summary>

<!-- claim:BASEDIAGMEM-FIG-176-CLAIM figure-table:BASEDIAGMEM-FIG-176 -->

**SPEC.** Figure 176, "Device Self-test Namespace Test Action": Shows the object or capacity relationships in Device Self-test Namespace Test Action. Separate logical identifiers from controllers, namespaces, ports, and capacity containers. Evidence index: NSID 00000000h, NSID 00000001h-FFFFFFFEh, NSID FFFFFFFFh.

#### Where this Figure fits

Figure 176 sits in §5.2.6 and acts as a hierarchy checkpoint. Read it after the report mental model has established the owning object and before software turns NSID 00000000h into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is an object or capacity relationship Figure. Separate containment, accessibility, identifier reference, and sharing. Adjacent boxes need not be one-to-one, and an identifier is not the physical or logical object it references.

#### Teaching redraw

```text
[Locate source: NSID 00000000h]
          ↓
[Extract field: NSID 00000001h-FFFFFFFEh] → [Apply encoding: NSID FFFFFFFFh]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `NSID 00000000h` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `NSID 00000001h-FFFFFFFEh` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `NSID FFFFFFFFh` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §5.2.6 is the applicable context.
2. Decode NSID 00000000h at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check NSID 00000001h-FFFFFFFEh as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 176 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §5.2.6 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes NSID 00000000h, NSID 00000001h-FFFFFFFEh, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §5.2.6, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 176. Annotate the bytes containing NSID 00000000h, decode them, and independently verify NSID 00000001h-FFFFFFFEh. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of NSID 00000000h in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand NSID 00000000h and state its unit or object scope?
2. Can the reader explain why NSID 00000001h-FFFFFFFEh is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** NSID 00000000h, NSID 00000001h-FFFFFFFEh, NSID FFFFFFFFh

**Source keyword index:** none

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.6, Figure 176, printed pages 199, PDF pages 225

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 177: Device Self-test - Command Dword 10</strong></summary>

<!-- claim:BASEDIAGMEM-FIG-177-CLAIM figure-table:BASEDIAGMEM-FIG-177 -->

**SPEC.** Figure 177, "Device Self-test - Command Dword 10": Defines command-specific fields in CDW10 for Device Self-test. Locate CDW10, then decode the named fields without borrowing semantics from another command. Evidence index: STC 1h, STC 2h, STC 3h, STC Eh, STC Fh.

#### Where this Figure fits

Figure 177 sits in §5.2.6 and acts as a command checkpoint. Read it after the report mental model has established the owning object and before software turns STC 1h into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a command-construction field table. Build the common SQE, locate the specified CDW, encode each bit range, clear reserved bits, and validate the result against transfer length, buffer, and completion status. Equal field names do not imply equal semantics across commands.

#### Teaching redraw

```text
[Locate source: STC 1h]
          ↓
[Extract field: STC 2h] → [Apply encoding: STC 3h]
                                      ↓
[Validate evidence: STC Eh]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `STC 1h` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `STC 2h` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `STC 3h` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `STC Eh` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `STC Fh` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §5.2.6 is the applicable context.
2. Decode STC 1h at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check STC 2h as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 177 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §5.2.6 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes STC 1h, STC 2h, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §5.2.6, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 177. Annotate the bytes containing STC 1h, decode them, and independently verify STC 2h. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of STC 1h in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand STC 1h and state its unit or object scope?
2. Can the reader explain why STC 2h is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** STC 1h, STC 2h, STC 3h, STC Eh, STC Fh

**Source keyword index:** `may`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.6, Figure 177, printed pages 199, PDF pages 225

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 178: Device Self-test - Command Dword 15</strong></summary>

<!-- claim:BASEDIAGMEM-FIG-178-CLAIM figure-table:BASEDIAGMEM-FIG-178 -->

**SPEC.** Figure 178, "Device Self-test - Command Dword 15": Defines command-specific fields in CDW15 for Device Self-test. Locate CDW15, then decode the named fields without borrowing semantics from another command. Evidence index: DSTP.

#### Where this Figure fits

Figure 178 sits in §5.2.6 and acts as a command checkpoint. Read it after the report mental model has established the owning object and before software turns DSTP into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a command-construction field table. Build the common SQE, locate the specified CDW, encode each bit range, clear reserved bits, and validate the result against transfer length, buffer, and completion status. Equal field names do not imply equal semantics across commands.

#### Teaching redraw

```text
[Locate source: DSTP]
          ↓
[Extract field: evidence] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `DSTP` | Device Self-test Parameter, CDW15 with vendor-defined meaning only for vendor-specific STC Eh. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §5.2.6 is the applicable context.
2. Decode DSTP at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check the cited condition as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 178 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §5.2.6 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes DSTP, the cited condition, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §5.2.6, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 178. Annotate the bytes containing DSTP, decode them, and independently verify the cited condition. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of DSTP in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand DSTP and state its unit or object scope?
2. Can the reader explain why the cited condition is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** DSTP

**Source keyword index:** `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.6, Figure 178, printed pages 200, PDF pages 226

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 179: Device Self-test - Command Processing</strong></summary>

<!-- claim:BASEDIAGMEM-FIG-179-CLAIM figure-table:BASEDIAGMEM-FIG-179 -->

**SPEC.** Figure 179, "Device Self-test - Command Processing": Shows the queue or command relationship expressed by Device Self-test - Command Processing. Trace ownership and direction from host to SQ, controller, and CQ; keep the indexed elements distinct: self-test in progress, new STC, abort, result creation.

#### Where this Figure fits

Figure 179 sits in §5.2.6 and acts as a queue checkpoint. Read it after the report mental model has established the owning object and before software turns self-test in progress into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a queue or command-flow Figure. Label host and controller ownership first, then trace head, tail, phase, or arbitration changes. An arrow represents a state or ownership transition and does not automatically prove command completion.

#### Teaching redraw

```text
[Locate source: self-test in progress]
          ↓
[Extract field: new STC] → [Apply encoding: abort]
                                      ↓
[Validate evidence: result creation]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `self-test in progress` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `new STC` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `abort` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `result creation` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §5.2.6 is the applicable context.
2. Decode self-test in progress at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check new STC as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 179 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §5.2.6 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes self-test in progress, new STC, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §5.2.6, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 179. Annotate the bytes containing self-test in progress, decode them, and independently verify new STC. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of self-test in progress in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand self-test in progress and state its unit or object scope?
2. Can the reader explain why new STC is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** self-test in progress, new STC, abort, result creation

**Source keyword index:** none

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.6, Figure 179, printed pages 200, PDF pages 226

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 180: Device Self-test - Command Specific Status Values</strong></summary>

<!-- claim:BASEDIAGMEM-FIG-180-CLAIM figure-table:BASEDIAGMEM-FIG-180 -->

**SPEC.** Figure 180, "Device Self-test - Command Specific Status Values": Defines the concrete layout or value relationships for Device Self-test - Command Specific Status Values. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is Device Self-test in Progress, status 1Dh.

#### Where this Figure fits

Figure 180 sits in §5.2.6 and acts as a layout checkpoint. Read it after the report mental model has established the owning object and before software turns Device Self-test in Progress into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a structure or capability field table. Locate it using the structure base and offset, read in byte/bit order, and separate capability gates, value encoding, and reserved areas. Presence in the table does not mean the function is supported.

#### Teaching redraw

```text
[Locate source: Device Self-test in Progress]
          ↓
[Extract field: status 1Dh] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `Device Self-test in Progress` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `status 1Dh` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §5.2.6 is the applicable context.
2. Decode Device Self-test in Progress at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check status 1Dh as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 180 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §5.2.6 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes Device Self-test in Progress, status 1Dh, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §5.2.6, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 180. Annotate the bytes containing Device Self-test in Progress, decode them, and independently verify status 1Dh. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of Device Self-test in Progress in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand Device Self-test in Progress and state its unit or object scope?
2. Can the reader explain why status 1Dh is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** Device Self-test in Progress, status 1Dh

**Source keyword index:** none

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.6, Figure 180, printed pages 201, PDF pages 227

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 218: Device Self-test Log Page</strong></summary>

<!-- claim:BASEDIAGMEM-FIG-218-CLAIM figure-table:BASEDIAGMEM-FIG-218 -->

**SPEC.** Figure 218, "Device Self-test Log Page": Connects Device Self-test Log Page to a self-test, host-memory, doorbell, or vendor-command engineering boundary. Resolve capability and owner first, decode DSTOS, DSTCS, RDS1, RDS20, 564 bytes, then verify the completion, log, or memory-lifecycle evidence.

#### Where this Figure fits

Figure 218 sits in §5.2.13.1.7 and acts as a relationship checkpoint. Read it after the report mental model has established the owning object and before software turns DSTOS into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This Figure explains a specific relationship or example. Identify each component type and owner, then decide whether each connection represents data flow, control flow, containment, or a condition. Visual placement alone creates no normative requirement.

#### Teaching redraw

```text
[Locate source: DSTOS]
          ↓
[Extract field: DSTCS] → [Apply encoding: RDS1]
                                      ↓
[Validate evidence: RDS20]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `DSTOS` | Device Self-test Operation Status, the LID 06h nibble identifying the current operation. |
| `DSTCS` | Device Self-test Completion Status, the LID 06h completion percentage from 0 through 100. |
| `RDS1` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `RDS20` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `564 bytes` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §5.2.13.1.7 is the applicable context.
2. Decode DSTOS at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check DSTCS as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 218 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §5.2.13.1.7 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes DSTOS, DSTCS, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §5.2.13.1.7, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 218. Annotate the bytes containing DSTOS, decode them, and independently verify DSTCS. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of DSTOS in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand DSTOS and state its unit or object scope?
2. Can the reader explain why DSTCS is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** DSTOS, DSTCS, RDS1, RDS20, 564 bytes

**Source keyword index:** `shall not`, `shall`, `should`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.7, Figure 218, printed pages 230, PDF pages 256

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 219: Self-test Result Data Structure</strong></summary>

<!-- claim:BASEDIAGMEM-FIG-219-CLAIM figure-table:BASEDIAGMEM-FIG-219 -->

**SPEC.** Figure 219, "Self-test Result Data Structure": Defines the concrete layout or value relationships for Self-test Result Data Structure. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is DSTC, DSTR, SEGN, VDINFO, POH, NSID, FLBA, STCT, STC, VS.

#### Where this Figure fits

Figure 219 sits in §5.2.13.1.7 and acts as a layout checkpoint. Read it after the report mental model has established the owning object and before software turns DSTC into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a structure or capability field table. Locate it using the structure base and offset, read in byte/bit order, and separate capability gates, value encoding, and reserved areas. Presence in the table does not mean the function is supported.

#### Teaching redraw

```text
[Locate source: DSTC]
          ↓
[Extract field: DSTR] → [Apply encoding: SEGN]
                                      ↓
[Validate evidence: VDINFO]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `DSTC` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `DSTR` | Device Self-test Result, the result-entry nibble identifying success, abort, or segment failure. |
| `SEGN` | Segment Number, identifying the first failed diagnostic segment only when DSTR is 7h. |
| `VDINFO` | Valid Diagnostic Information, the bitmap independently gating NSID, FLBA, SCT, and SC. |
| `POH` | Power On Hours, accumulated power-on hours when a self-test result is created, excluding specified low-power time. |
| `NSID` | Namespace Identifier, a controller-visible numeric handle for a namespace; the identifier is not the namespace object itself. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §5.2.13.1.7 is the applicable context.
2. Decode DSTC at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check DSTR as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 219 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §5.2.13.1.7 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes DSTC, DSTR, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §5.2.13.1.7, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 219. Annotate the bytes containing DSTC, decode them, and independently verify DSTR. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of DSTC in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand DSTC and state its unit or object scope?
2. Can the reader explain why DSTR is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** DSTC, DSTR, SEGN, VDINFO, POH, NSID, FLBA, STCT, STC, VS

**Source keyword index:** `should`, `may`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.7, Figure 219, printed pages 231-232, PDF pages 257-258

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 545: Host Memory Buffer - Command Dword 11</strong></summary>

<!-- claim:BASEDIAGMEM-FIG-545-CLAIM figure-table:BASEDIAGMEM-FIG-545 -->

**SPEC.** Figure 545, "Host Memory Buffer - Command Dword 11": Defines command-specific fields in CDW11 for Host Memory Buffer. Locate CDW11, then decode the named fields without borrowing semantics from another command. Evidence index: CTZ, HMNARE, MR, EHM.

#### Where this Figure fits

Figure 545 sits in §5.2.30.2.3 and acts as a command checkpoint. Read it after the report mental model has established the owning object and before software turns CTZ into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a command-construction field table. Build the common SQE, locate the specified CDW, encode each bit range, clear reserved bits, and validate the result against transfer length, buffer, and completion status. Equal field names do not imply equal semantics across commands.

#### Teaching redraw

```text
[Locate source: CTZ]
          ↓
[Extract field: HMNARE] → [Apply encoding: MR]
                                      ↓
[Validate evidence: EHM]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `CTZ` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `HMNARE` | Host Memory Non-operational Access Restriction Enable, the bit configuring non-operational HMB-access policy. |
| `MR` | Memory Return, indicating return of exactly the same previous HMB size, addresses, descriptors, and contents. |
| `EHM` | Enable Host Memory, the bit enabling or disabling controller use of HMB. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §5.2.30.2.3 is the applicable context.
2. Decode CTZ at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check HMNARE as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 545 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §5.2.30.2.3 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes CTZ, HMNARE, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §5.2.30.2.3, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 545. Annotate the bytes containing CTZ, decode them, and independently verify HMNARE. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of CTZ in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand CTZ and state its unit or object scope?
2. Can the reader explain why HMNARE is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** CTZ, HMNARE, MR, EHM

**Source keyword index:** `shall not`, `shall`, `may`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.2.3, Figure 545, printed pages 516-517, PDF pages 542-543

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 546: Host Memory Buffer - Command Dword 12</strong></summary>

<!-- claim:BASEDIAGMEM-FIG-546-CLAIM figure-table:BASEDIAGMEM-FIG-546 -->

**SPEC.** Figure 546, "Host Memory Buffer - Command Dword 12": Defines command-specific fields in CDW12 for Host Memory Buffer. Locate CDW12, then decode the named fields without borrowing semantics from another command. Evidence index: HSIZE, CC.MPS units.

#### Where this Figure fits

Figure 546 sits in §5.2.30.2.3 and acts as a command checkpoint. Read it after the report mental model has established the owning object and before software turns HSIZE into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a command-construction field table. Build the common SQE, locate the specified CDW, encode each bit range, clear reserved bits, and validate the result against transfer length, buffer, and completion status. Equal field names do not imply equal semantics across commands.

#### Teaching redraw

```text
[Locate source: HSIZE]
          ↓
[Extract field: CC.MPS units] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `HSIZE` | Host Memory Buffer Size, the total HMB size in CC.MPS memory-page units. |
| `CC.MPS units` | Controller Configuration, the property through which the host selects settings and enables or disables a controller. Here CC.MPS units selects its MPS units member field. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §5.2.30.2.3 is the applicable context.
2. Decode HSIZE at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check CC.MPS units as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 546 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §5.2.30.2.3 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes HSIZE, CC.MPS units, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §5.2.30.2.3, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 546. Annotate the bytes containing HSIZE, decode them, and independently verify CC.MPS units. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of HSIZE in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand HSIZE and state its unit or object scope?
2. Can the reader explain why CC.MPS units is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** HSIZE, CC.MPS units

**Source keyword index:** none

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.2.3, Figure 546, printed pages 517, PDF pages 543

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 547: Host Memory Buffer - Command Dword 13</strong></summary>

<!-- claim:BASEDIAGMEM-FIG-547-CLAIM figure-table:BASEDIAGMEM-FIG-547 -->

**SPEC.** Figure 547, "Host Memory Buffer - Command Dword 13": Defines command-specific fields in CDW13 for Host Memory Buffer. Locate CDW13, then decode the named fields without borrowing semantics from another command. Evidence index: HMDLLA, 16-byte alignment.

#### Where this Figure fits

Figure 547 sits in §5.2.30.2.3 and acts as a command checkpoint. Read it after the report mental model has established the owning object and before software turns HMDLLA into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a command-construction field table. Build the common SQE, locate the specified CDW, encode each bit range, clear reserved bits, and validate the result against transfer length, buffer, and completion status. Equal field names do not imply equal semantics across commands.

#### Teaching redraw

```text
[Locate source: HMDLLA]
          ↓
[Extract field: 16-byte alignment] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `HMDLLA` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `16-byte alignment` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §5.2.30.2.3 is the applicable context.
2. Decode HMDLLA at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check 16-byte alignment as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 547 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §5.2.30.2.3 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes HMDLLA, 16-byte alignment, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §5.2.30.2.3, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 547. Annotate the bytes containing HMDLLA, decode them, and independently verify 16-byte alignment. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of HMDLLA in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand HMDLLA and state its unit or object scope?
2. Can the reader explain why 16-byte alignment is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** HMDLLA, 16-byte alignment

**Source keyword index:** `shall`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.2.3, Figure 547, printed pages 517, PDF pages 543

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 548: Host Memory Buffer - Command Dword 14</strong></summary>

<!-- claim:BASEDIAGMEM-FIG-548-CLAIM figure-table:BASEDIAGMEM-FIG-548 -->

**SPEC.** Figure 548, "Host Memory Buffer - Command Dword 14": Defines command-specific fields in CDW14 for Host Memory Buffer. Locate CDW14, then decode the named fields without borrowing semantics from another command. Evidence index: HMDLUA.

#### Where this Figure fits

Figure 548 sits in §5.2.30.2.3 and acts as a command checkpoint. Read it after the report mental model has established the owning object and before software turns HMDLUA into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a command-construction field table. Build the common SQE, locate the specified CDW, encode each bit range, clear reserved bits, and validate the result against transfer length, buffer, and completion status. Equal field names do not imply equal semantics across commands.

#### Teaching redraw

```text
[Locate source: HMDLUA]
          ↓
[Extract field: evidence] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `HMDLUA` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §5.2.30.2.3 is the applicable context.
2. Decode HMDLUA at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check the cited condition as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 548 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §5.2.30.2.3 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes HMDLUA, the cited condition, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §5.2.30.2.3, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 548. Annotate the bytes containing HMDLUA, decode them, and independently verify the cited condition. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of HMDLUA in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand HMDLUA and state its unit or object scope?
2. Can the reader explain why the cited condition is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** HMDLUA

**Source keyword index:** none

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.2.3, Figure 548, printed pages 517, PDF pages 543

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 549: Host Memory Buffer - Command Dword 15</strong></summary>

<!-- claim:BASEDIAGMEM-FIG-549-CLAIM figure-table:BASEDIAGMEM-FIG-549 -->

**SPEC.** Figure 549, "Host Memory Buffer - Command Dword 15": Defines command-specific fields in CDW15 for Host Memory Buffer. Locate CDW15, then decode the named fields without borrowing semantics from another command. Evidence index: HMDLEC.

#### Where this Figure fits

Figure 549 sits in §5.2.30.2.3 and acts as a command checkpoint. Read it after the report mental model has established the owning object and before software turns HMDLEC into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a command-construction field table. Build the common SQE, locate the specified CDW, encode each bit range, clear reserved bits, and validate the result against transfer length, buffer, and completion status. Equal field names do not imply equal semantics across commands.

#### Teaching redraw

```text
[Locate source: HMDLEC]
          ↓
[Extract field: evidence] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `HMDLEC` | Host Memory Descriptor List Entry Count, the number of valid entries in the HMDL. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §5.2.30.2.3 is the applicable context.
2. Decode HMDLEC at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check the cited condition as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 549 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §5.2.30.2.3 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes HMDLEC, the cited condition, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §5.2.30.2.3, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 549. Annotate the bytes containing HMDLEC, decode them, and independently verify the cited condition. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of HMDLEC in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand HMDLEC and state its unit or object scope?
2. Can the reader explain why the cited condition is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** HMDLEC

**Source keyword index:** `shall`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.2.3, Figure 549, printed pages 518, PDF pages 544

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 550: Host Memory Buffer - Host Memory Descriptor List</strong></summary>

<!-- claim:BASEDIAGMEM-FIG-550-CLAIM figure-table:BASEDIAGMEM-FIG-550 -->

**SPEC.** Figure 550, "Host Memory Buffer - Host Memory Descriptor List": Defines the concrete layout or value relationships for Host Memory Buffer - Host Memory Descriptor List. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is 16-byte descriptor entries, HMDLEC.

#### Where this Figure fits

Figure 550 sits in §5.2.30.2.3 and acts as a relationship checkpoint. Read it after the report mental model has established the owning object and before software turns 16-byte descriptor entries into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This Figure explains a specific relationship or example. Identify each component type and owner, then decide whether each connection represents data flow, control flow, containment, or a condition. Visual placement alone creates no normative requirement.

#### Teaching redraw

```text
[Locate source: 16-byte descriptor entries]
          ↓
[Extract field: HMDLEC] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `16-byte descriptor entries` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `HMDLEC` | Host Memory Descriptor List Entry Count, the number of valid entries in the HMDL. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §5.2.30.2.3 is the applicable context.
2. Decode 16-byte descriptor entries at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check HMDLEC as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 550 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §5.2.30.2.3 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes 16-byte descriptor entries, HMDLEC, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §5.2.30.2.3, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 550. Annotate the bytes containing 16-byte descriptor entries, decode them, and independently verify HMDLEC. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of 16-byte descriptor entries in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand 16-byte descriptor entries and state its unit or object scope?
2. Can the reader explain why HMDLEC is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** 16-byte descriptor entries, HMDLEC

**Source keyword index:** `shall`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.2.3, Figure 550, printed pages 518, PDF pages 544

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 551: Host Memory Buffer - Host Memory Buffer Descriptor Entry</strong></summary>

<!-- claim:BASEDIAGMEM-FIG-551-CLAIM figure-table:BASEDIAGMEM-FIG-551 -->

**SPEC.** Figure 551, "Host Memory Buffer - Host Memory Buffer Descriptor Entry": Defines the concrete layout or value relationships for Host Memory Buffer - Host Memory Buffer Descriptor Entry. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is BADD, BSIZE, CC.MPS alignment.

#### Where this Figure fits

Figure 551 sits in §5.2.30.2.3 and acts as a relationship checkpoint. Read it after the report mental model has established the owning object and before software turns BADD into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This Figure explains a specific relationship or example. Identify each component type and owner, then decide whether each connection represents data flow, control flow, containment, or a condition. Visual placement alone creates no normative requirement.

#### Teaching redraw

```text
[Locate source: BADD]
          ↓
[Extract field: BSIZE] → [Apply encoding: CC.MPS alignment]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `BADD` | Buffer Address, the CC.MPS-aligned memory-page address in an HMB descriptor. |
| `BSIZE` | Buffer Size, the contiguous range length in CC.MPS pages in an HMB descriptor. |
| `CC.MPS alignment` | Controller Configuration, the property through which the host selects settings and enables or disables a controller. Here CC.MPS alignment selects its MPS alignment member field. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §5.2.30.2.3 is the applicable context.
2. Decode BADD at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check BSIZE as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 551 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §5.2.30.2.3 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes BADD, BSIZE, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §5.2.30.2.3, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 551. Annotate the bytes containing BADD, decode them, and independently verify BSIZE. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of BADD in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand BADD and state its unit or object scope?
2. Can the reader explain why BSIZE is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** BADD, BSIZE, CC.MPS alignment

**Source keyword index:** `shall`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.2.3, Figure 551, printed pages 518, PDF pages 544

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 552: Host Memory Buffer - Completion Queue Entry Dword 0</strong></summary>

<!-- claim:BASEDIAGMEM-FIG-552-CLAIM figure-table:BASEDIAGMEM-FIG-552 -->

**SPEC.** Figure 552, "Host Memory Buffer - Completion Queue Entry Dword 0": Shows the queue or command relationship expressed by Host Memory Buffer - Completion Queue Entry Dword 0. Trace ownership and direction from host to SQ, controller, and CQ; keep the indexed elements distinct: HMNAR, HMNARE, EHM.

#### Where this Figure fits

Figure 552 sits in §5.2.30.2.3 and acts as a queue checkpoint. Read it after the report mental model has established the owning object and before software turns HMNAR into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a queue or command-flow Figure. Label host and controller ownership first, then trace head, tail, phase, or arbitration changes. An arrow represents a state or ownership transition and does not automatically prove command completion.

#### Teaching redraw

```text
[Locate source: HMNAR]
          ↓
[Extract field: HMNARE] → [Apply encoding: EHM]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `HMNAR` | Host Memory Non-operational Access Restricted, the state bit reporting whether restriction is currently active. |
| `HMNARE` | Host Memory Non-operational Access Restriction Enable, the bit configuring non-operational HMB-access policy. |
| `EHM` | Enable Host Memory, the bit enabling or disabling controller use of HMB. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §5.2.30.2.3 is the applicable context.
2. Decode HMNAR at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check HMNARE as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 552 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §5.2.30.2.3 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes HMNAR, HMNARE, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §5.2.30.2.3, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 552. Annotate the bytes containing HMNAR, decode them, and independently verify HMNARE. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of HMNAR in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand HMNAR and state its unit or object scope?
2. Can the reader explain why HMNARE is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** HMNAR, HMNARE, EHM

**Source keyword index:** `shall`, `may`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.2.3, Figure 552, printed pages 518-519, PDF pages 544-545

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 553: Host Memory Buffer - Attributes Data Structure</strong></summary>

<!-- claim:BASEDIAGMEM-FIG-553-CLAIM figure-table:BASEDIAGMEM-FIG-553 -->

**SPEC.** Figure 553, "Host Memory Buffer - Attributes Data Structure": Defines the concrete layout or value relationships for Host Memory Buffer - Attributes Data Structure. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is HSIZE, HMDLAL, HMDLAU, HMDLEC, 4096 bytes.

#### Where this Figure fits

Figure 553 sits in §5.2.30.2.3 and acts as a layout checkpoint. Read it after the report mental model has established the owning object and before software turns HSIZE into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a structure or capability field table. Locate it using the structure base and offset, read in byte/bit order, and separate capability gates, value encoding, and reserved areas. Presence in the table does not mean the function is supported.

#### Teaching redraw

```text
[Locate source: HSIZE]
          ↓
[Extract field: HMDLAL] → [Apply encoding: HMDLAU]
                                      ↓
[Validate evidence: HMDLEC]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `HSIZE` | Host Memory Buffer Size, the total HMB size in CC.MPS memory-page units. |
| `HMDLAL` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `HMDLAU` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `HMDLEC` | Host Memory Descriptor List Entry Count, the number of valid entries in the HMDL. |
| `4096 bytes` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §5.2.30.2.3 is the applicable context.
2. Decode HSIZE at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check HMDLAL as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 553 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §5.2.30.2.3 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes HSIZE, HMDLAL, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §5.2.30.2.3, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 553. Annotate the bytes containing HSIZE, decode them, and independently verify HMDLAL. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of HSIZE in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand HSIZE and state its unit or object scope?
2. Can the reader explain why HMDLAL is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** HSIZE, HMDLAL, HMDLAU, HMDLEC, 4096 bytes

**Source keyword index:** `shall`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.2.3, Figure 553, printed pages 519, PDF pages 545

</details>

<a id="section-8-1"></a>

### §8.1

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 700: Example Device Self-test Operation (Informative)</strong></summary>

<!-- claim:BASEDIAGMEM-FIG-700-CLAIM figure-table:BASEDIAGMEM-FIG-700 -->

**SPEC.** Figure 700, "Example Device Self-test Operation (Informative)": Defines the concrete layout or value relationships for Example Device Self-test Operation (Informative). Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is segment, test performed, failure criteria, informative.

#### Where this Figure fits

Figure 700 sits in §8.1.8 and acts as a layout checkpoint. Read it after the report mental model has established the owning object and before software turns segment into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a structure or capability field table. Locate it using the structure base and offset, read in byte/bit order, and separate capability gates, value encoding, and reserved areas. Presence in the table does not mean the function is supported.

#### Teaching redraw

```text
[Locate source: segment]
          ↓
[Extract field: test performed] → [Apply encoding: failure criteria]
                                      ↓
[Validate evidence: informative]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `segment` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `test performed` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `failure criteria` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `informative` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §8.1.8 is the applicable context.
2. Decode segment at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check test performed as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 700 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §8.1.8 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes segment, test performed, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §8.1.8, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 700. Annotate the bytes containing segment, decode them, and independently verify test performed. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of segment in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand segment and state its unit or object scope?
2. Can the reader explain why test performed is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** segment, test performed, failure criteria, informative

**Source keyword index:** `shall`, `should`, `may`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §8.1.8, Figure 700, printed pages 615, PDF pages 641

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 701: Format NVM command Aborting a Device Self-Test Operation</strong></summary>

<!-- claim:BASEDIAGMEM-FIG-701-CLAIM figure-table:BASEDIAGMEM-FIG-701 -->

**SPEC.** Figure 701, "Format NVM command Aborting a Device Self-Test Operation": Defines the concrete layout or value relationships for Format NVM command Aborting a Device Self-Test Operation. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is SES, FNS, SENS, Format NSID, Self-test NSID, abort decision.

#### Where this Figure fits

Figure 701 sits in §8.1.8.1-8.1.8.2 and acts as a layout checkpoint. Read it after the report mental model has established the owning object and before software turns SES into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a structure or capability field table. Locate it using the structure base and offset, read in byte/bit order, and separate capability gates, value encoding, and reserved areas. Presence in the table does not mean the function is supported.

#### Teaching redraw

```text
[Locate source: SES]
          ↓
[Extract field: FNS] → [Apply encoding: SENS]
                                      ↓
[Validate evidence: Format NSID]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `SES` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `FNS` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `SENS` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `Format NSID` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `Self-test NSID` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `abort decision` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §8.1.8.1-8.1.8.2 is the applicable context.
2. Decode SES at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check FNS as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 701 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §8.1.8.1-8.1.8.2 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes SES, FNS, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §8.1.8.1-8.1.8.2, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 701. Annotate the bytes containing SES, decode them, and independently verify FNS. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of SES in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand SES and state its unit or object scope?
2. Can the reader explain why FNS is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** SES, FNS, SENS, Format NSID, Self-test NSID, abort decision

**Source keyword index:** `shall`, `should`, `may`, `optional`

> Source: NVME-BASE-2.4, Rev. 2.4, §8.1.8.1-8.1.8.2, Figure 701, printed pages 616, PDF pages 642

</details>

<a id="section-dependency"></a>

### Referenced Figure dependencies (outside the main section range)

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 36: Offset 0h: CAP - Controller Capabilities</strong></summary>

<!-- claim:BASEDIAGMEM-FIG-036-CLAIM figure-table:BASEDIAGMEM-FIG-036 -->

**SPEC.** Figure 36, "Offset 0h: CAP - Controller Capabilities": Defines CAP (Controller Capabilities) at offset 0h and identifies the fields that software must decode at that location. Start at CAP, then map bit ranges to access type, reset value, and field meaning. Evidence index: DSTRD, 2^(2+DSTRD) bytes.

#### Where this Figure fits

Figure 36 sits in §3.1.4.1 and acts as a register checkpoint. Read it after the report mental model has established the owning object and before software turns DSTRD into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a register or property field table. Locate the base offset, verify access width, reset value, and bit range, and only then convert bits into state or capability. Preserve the complete register snapshot so adjacent conditions are not lost by extracting one bit.

#### Teaching redraw

```text
[Locate source: DSTRD]
          ↓
[Extract field: 2^(2+DSTRD) bytes] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `DSTRD` | Doorbell Stride, the CAP field determining spacing between adjacent doorbell registers. |
| `2^(2+DSTRD) bytes` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.1.4.1 is the applicable context.
2. Decode DSTRD at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check 2^(2+DSTRD) bytes as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

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
| It answers | How the cited section organizes DSTRD, 2^(2+DSTRD) bytes, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.1.4.1, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 36. Annotate the bytes containing DSTRD, decode them, and independently verify 2^(2+DSTRD) bytes. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of DSTRD in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand DSTRD and state its unit or object scope?
2. Can the reader explain why 2^(2+DSTRD) bytes is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** DSTRD, 2^(2+DSTRD) bytes

**Source keyword index:** `shall not`, `shall`, `should`, `may`, `optional`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.1, Figure 36, printed pages 55-58, PDF pages 81-84

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 93: Common Command Format</strong></summary>

<!-- claim:BASEDIAGMEM-FIG-093-CLAIM figure-table:BASEDIAGMEM-FIG-093 -->

**SPEC.** Figure 93, "Common Command Format": Defines the concrete layout or value relationships for Common Command Format. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is OPC, CID, NSID, DPTR, CDW10-CDW15.

#### Where this Figure fits

Figure 93 sits in §4.1.1 and acts as a command checkpoint. Read it after the report mental model has established the owning object and before software turns OPC into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a command-construction field table. Build the common SQE, locate the specified CDW, encode each bit range, clear reserved bits, and validate the result against transfer length, buffer, and completion status. Equal field names do not imply equal semantics across commands.

#### Teaching redraw

```text
[Locate source: OPC]
          ↓
[Extract field: CID] → [Apply encoding: NSID]
                                      ↓
[Validate evidence: DPTR]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `OPC` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `CID` | Command Identifier, used with the SQ identifier to identify an outstanding command. |
| `NSID` | Namespace Identifier, a controller-visible numeric handle for a namespace; the identifier is not the namespace object itself. |
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

**Source field index:** OPC, CID, NSID, DPTR, CDW10-CDW15

**Source keyword index:** `shall`, `may`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §4.1.1, Figure 93, printed pages 140-142, PDF pages 166-168

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 94: Common Command Format - Vendor Specific Commands (Optional)</strong></summary>

<!-- claim:BASEDIAGMEM-FIG-094-CLAIM figure-table:BASEDIAGMEM-FIG-094 -->

**SPEC.** Figure 94, "Common Command Format - Vendor Specific Commands (Optional)": Defines the concrete layout or value relationships for Common Command Format - Vendor Specific Commands (Optional). Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is NSID, MDPTR, NDT, NDM, CDW12-CDW15.

#### Where this Figure fits

Figure 94 sits in §4.1.1 and acts as a command checkpoint. Read it after the report mental model has established the owning object and before software turns NSID into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a command-construction field table. Build the common SQE, locate the specified CDW, encode each bit range, clear reserved bits, and validate the result against transfer length, buffer, and completion status. Equal field names do not imply equal semantics across commands.

#### Teaching redraw

```text
[Locate source: NSID]
          ↓
[Extract field: MDPTR] → [Apply encoding: NDT]
                                      ↓
[Validate evidence: NDM]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `NSID` | Namespace Identifier, a controller-visible numeric handle for a namespace; the identifier is not the namespace object itself. |
| `MDPTR` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `NDT` | Number of Dwords in Data Transfer, the actual data-dword count in the standard vendor-specific format. |
| `NDM` | Number of Dwords in Metadata Transfer, the actual metadata-dword count in the standard vendor-specific format. |
| `CDW12-CDW15` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §4.1.1 is the applicable context.
2. Decode NSID at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check MDPTR as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 94 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §4.1.1 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes NSID, MDPTR, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §4.1.1, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 94. Annotate the bytes containing NSID, decode them, and independently verify MDPTR. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of NSID in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand NSID and state its unit or object scope?
2. Can the reader explain why MDPTR is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** NSID, MDPTR, NDT, NDM, CDW12-CDW15

**Source keyword index:** `shall`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §4.1.1, Figure 94, printed pages 143, PDF pages 169

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 197: Get Features - Data Pointer</strong></summary>

<!-- claim:BASEDIAGMEM-FIG-197-CLAIM figure-table:BASEDIAGMEM-FIG-197 -->

**SPEC.** Figure 197, "Get Features - Data Pointer": Connects Get Features - Data Pointer to a self-test, host-memory, doorbell, or vendor-command engineering boundary. Resolve capability and owner first, decode DPTR, PRP1, PRP2, then verify the completion, log, or memory-lifecycle evidence.

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
<summary><strong>NVME-BASE-2.4 — Figure 198: Get Features - Command Dword 10</strong></summary>

<!-- claim:BASEDIAGMEM-FIG-198-CLAIM figure-table:BASEDIAGMEM-FIG-198 -->

**SPEC.** Figure 198, "Get Features - Command Dword 10": Defines command-specific fields in CDW10 for Get Features. Locate CDW10, then decode the named fields without borrowing semantics from another command. Evidence index: SEL, FID.

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
<summary><strong>NVME-BASE-2.4 — Figure 200: Feature Identifiers for Get Features</strong></summary>

<!-- claim:BASEDIAGMEM-FIG-200-CLAIM figure-table:BASEDIAGMEM-FIG-200 -->

**SPEC.** Figure 200, "Feature Identifiers for Get Features": Defines the identifier composition or namespace of values shown by Feature Identifiers for Get Features. Keep the value width, issuing authority, uniqueness scope, and reserved values separate. Evidence index: FID 0Dh, Controller scope, data buffer.

#### Where this Figure fits

Figure 200 sits in §5.2.12 and acts as a identifier checkpoint. Read it after the report mental model has established the owning object and before software turns FID 0Dh into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is an identifier-format Figure. Record width and encoding, then identify assignment authority, uniqueness scope, reserved values, and lifetime. Equal-width identifiers are not automatically interchangeable.

#### Teaching redraw

```text
[Locate source: FID 0Dh]
          ↓
[Extract field: Controller scope] → [Apply encoding: data buffer]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `FID 0Dh` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `Controller scope` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `data buffer` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §5.2.12 is the applicable context.
2. Decode FID 0Dh at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check Controller scope as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
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
| It answers | How the cited section organizes FID 0Dh, Controller scope, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §5.2.12, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 200. Annotate the bytes containing FID 0Dh, decode them, and independently verify Controller scope. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of FID 0Dh in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand FID 0Dh and state its unit or object scope?
2. Can the reader explain why Controller scope is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** FID 0Dh, Controller scope, data buffer

**Source keyword index:** `may`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.12, Figure 200, printed pages 210-211, PDF pages 236-237

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 203: Get Log Page - Data Pointer</strong></summary>

<!-- claim:BASEDIAGMEM-FIG-203-CLAIM figure-table:BASEDIAGMEM-FIG-203 -->

**SPEC.** Figure 203, "Get Log Page - Data Pointer": Connects Get Log Page - Data Pointer to a self-test, host-memory, doorbell, or vendor-command engineering boundary. Resolve capability and owner first, decode DPTR, then verify the completion, log, or memory-lifecycle evidence.

#### Where this Figure fits

Figure 203 sits in §5.2.13 and acts as a command checkpoint. Read it after the report mental model has established the owning object and before software turns DPTR into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a command-construction field table. Build the common SQE, locate the specified CDW, encode each bit range, clear reserved bits, and validate the result against transfer length, buffer, and completion status. Equal field names do not imply equal semantics across commands.

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

1. Locate the structure, register, queue, or object named by the caption and confirm that §5.2.13 is the applicable context.
2. Decode DPTR at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check the cited condition as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

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
| It answers | How the cited section organizes DPTR, the cited condition, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §5.2.13, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 203. Annotate the bytes containing DPTR, decode them, and independently verify the cited condition. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

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
2. Can the reader explain why the cited condition is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** DPTR

**Source keyword index:** none

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13, Figure 203, printed pages 213, PDF pages 239

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 204: Get Log Page - Command Dword 10</strong></summary>

<!-- claim:BASEDIAGMEM-FIG-204-CLAIM figure-table:BASEDIAGMEM-FIG-204 -->

**SPEC.** Figure 204, "Get Log Page - Command Dword 10": Defines command-specific fields in CDW10 for Get Log Page. Locate CDW10, then decode the named fields without borrowing semantics from another command. Evidence index: NUMDL, RAE, LSP, LID 06h.

#### Where this Figure fits

Figure 204 sits in §5.2.13 and acts as a command checkpoint. Read it after the report mental model has established the owning object and before software turns NUMDL into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a command-construction field table. Build the common SQE, locate the specified CDW, encode each bit range, clear reserved bits, and validate the result against transfer length, buffer, and completion status. Equal field names do not imply equal semantics across commands.

#### Teaching redraw

```text
[Locate source: NUMDL]
          ↓
[Extract field: RAE] → [Apply encoding: LSP]
                                      ↓
[Validate evidence: LID 06h]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `NUMDL` | Number of Dwords Lower, the low 16 bits of Get Log Page NUMD. |
| `RAE` | Retain Asynchronous Event, the Get Log Page selector controlling retention of a related asynchronous event. |
| `LSP` | Log Specific Field, a command selector whose meaning is defined by the selected log page. |
| `LID 06h` | Identifier 06h for the Device Self-test Log Page, containing current operation state and twenty historical results. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §5.2.13 is the applicable context.
2. Decode NUMDL at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check RAE as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

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
| It answers | How the cited section organizes NUMDL, RAE, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §5.2.13, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 204. Annotate the bytes containing NUMDL, decode them, and independently verify RAE. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of NUMDL in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand NUMDL and state its unit or object scope?
2. Can the reader explain why RAE is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** NUMDL, RAE, LSP, LID 06h

**Source keyword index:** `shall`, `should`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13, Figure 204, printed pages 213, PDF pages 239

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 205: Get Log Page - Command Dword 11</strong></summary>

<!-- claim:BASEDIAGMEM-FIG-205-CLAIM figure-table:BASEDIAGMEM-FIG-205 -->

**SPEC.** Figure 205, "Get Log Page - Command Dword 11": Defines command-specific fields in CDW11 for Get Log Page. Locate CDW11, then decode the named fields without borrowing semantics from another command. Evidence index: LSI, NUMDU.

#### Where this Figure fits

Figure 205 sits in §5.2.13 and acts as a command checkpoint. Read it after the report mental model has established the owning object and before software turns LSI into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a command-construction field table. Build the common SQE, locate the specified CDW, encode each bit range, clear reserved bits, and validate the result against transfer length, buffer, and completion status. Equal field names do not imply equal semantics across commands.

#### Teaching redraw

```text
[Locate source: LSI]
          ↓
[Extract field: NUMDU] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `LSI` | Log Specific Identifier, an identifier whose meaning is defined by the selected log page. |
| `NUMDU` | Number of Dwords Upper, the high 16 bits of Get Log Page NUMD. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §5.2.13 is the applicable context.
2. Decode LSI at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check NUMDU as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

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
| It answers | How the cited section organizes LSI, NUMDU, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §5.2.13, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 205. Annotate the bytes containing LSI, decode them, and independently verify NUMDU. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of LSI in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand LSI and state its unit or object scope?
2. Can the reader explain why NUMDU is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** LSI, NUMDU

**Source keyword index:** `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13, Figure 205, printed pages 214, PDF pages 240

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 206: Get Log Page - Command Dword 12</strong></summary>

<!-- claim:BASEDIAGMEM-FIG-206-CLAIM figure-table:BASEDIAGMEM-FIG-206 -->

**SPEC.** Figure 206, "Get Log Page - Command Dword 12": Defines command-specific fields in CDW12 for Get Log Page. Locate CDW12, then decode the named fields without borrowing semantics from another command. Evidence index: LPOL, OT.

#### Where this Figure fits

Figure 206 sits in §5.2.13 and acts as a command checkpoint. Read it after the report mental model has established the owning object and before software turns LPOL into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a command-construction field table. Build the common SQE, locate the specified CDW, encode each bit range, clear reserved bits, and validate the result against transfer length, buffer, and completion status. Equal field names do not imply equal semantics across commands.

#### Teaching redraw

```text
[Locate source: LPOL]
          ↓
[Extract field: OT] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `LPOL` | Log Page Offset Lower, the low 32 bits of the Get Log Page byte offset. |
| `OT` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §5.2.13 is the applicable context.
2. Decode LPOL at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check OT as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

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
| It answers | How the cited section organizes LPOL, OT, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §5.2.13, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 206. Annotate the bytes containing LPOL, decode them, and independently verify OT. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of LPOL in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand LPOL and state its unit or object scope?
2. Can the reader explain why OT is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** LPOL, OT

**Source keyword index:** `shall`, `may`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13, Figure 206, printed pages 214, PDF pages 240

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 207: Get Log Page - Command Dword 13</strong></summary>

<!-- claim:BASEDIAGMEM-FIG-207-CLAIM figure-table:BASEDIAGMEM-FIG-207 -->

**SPEC.** Figure 207, "Get Log Page - Command Dword 13": Defines command-specific fields in CDW13 for Get Log Page. Locate CDW13, then decode the named fields without borrowing semantics from another command. Evidence index: LPOU.

#### Where this Figure fits

Figure 207 sits in §5.2.13 and acts as a command checkpoint. Read it after the report mental model has established the owning object and before software turns LPOU into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a command-construction field table. Build the common SQE, locate the specified CDW, encode each bit range, clear reserved bits, and validate the result against transfer length, buffer, and completion status. Equal field names do not imply equal semantics across commands.

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

1. Locate the structure, register, queue, or object named by the caption and confirm that §5.2.13 is the applicable context.
2. Decode LPOU at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check the cited condition as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

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
| It answers | How the cited section organizes LPOU, the cited condition, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §5.2.13, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 207. Annotate the bytes containing LPOU, decode them, and independently verify the cited condition. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of LPOU in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand LPOU and state its unit or object scope?
2. Can the reader explain why the cited condition is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** LPOU

**Source keyword index:** none

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13, Figure 207, printed pages 214, PDF pages 240

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 208: Get Log Page - Command Dword 14</strong></summary>

<!-- claim:BASEDIAGMEM-FIG-208-CLAIM figure-table:BASEDIAGMEM-FIG-208 -->

**SPEC.** Figure 208, "Get Log Page - Command Dword 14": Defines command-specific fields in CDW14 for Get Log Page. Locate CDW14, then decode the named fields without borrowing semantics from another command. Evidence index: CSI, OT, UIDX.

#### Where this Figure fits

Figure 208 sits in §5.2.13 and acts as a command checkpoint. Read it after the report mental model has established the owning object and before software turns CSI into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a command-construction field table. Build the common SQE, locate the specified CDW, encode each bit range, clear reserved bits, and validate the result against transfer length, buffer, and completion status. Equal field names do not imply equal semantics across commands.

#### Teaching redraw

```text
[Locate source: CSI]
          ↓
[Extract field: OT] → [Apply encoding: UIDX]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `CSI` | Command Set Identifier, selecting the I/O Command Set context for a command or log page. |
| `OT` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `UIDX` | UUID Index, an index into the UUID List; zero indicates that no UUID is specified. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §5.2.13 is the applicable context.
2. Decode CSI at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check OT as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

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
| It answers | How the cited section organizes CSI, OT, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §5.2.13, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 208. Annotate the bytes containing CSI, decode them, and independently verify OT. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of CSI in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand CSI and state its unit or object scope?
2. Can the reader explain why OT is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** CSI, OT, UIDX

**Source keyword index:** `shall`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13, Figure 208, printed pages 214-215, PDF pages 240-241

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 209: Get Log Page - Log Page Identifiers</strong></summary>

<!-- claim:BASEDIAGMEM-FIG-209-CLAIM figure-table:BASEDIAGMEM-FIG-209 -->

**SPEC.** Figure 209, "Get Log Page - Log Page Identifiers": Defines the identifier composition or namespace of values shown by Get Log Page - Log Page Identifiers. Keep the value width, issuing authority, uniqueness scope, and reserved values separate. Evidence index: LID 06h, CSI = N, Controller / Domain / NVM subsystem, Device Self-test, §5.2.13.1.7.

#### Where this Figure fits

Figure 209 sits in §5.2.13 and acts as a identifier checkpoint. Read it after the report mental model has established the owning object and before software turns LID 06h into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is an identifier-format Figure. Record width and encoding, then identify assignment authority, uniqueness scope, reserved values, and lifetime. Equal-width identifiers are not automatically interchangeable.

#### Teaching redraw

```text
[Locate source: LID 06h]
          ↓
[Extract field: CSI = N] → [Apply encoding: Controller / Domain / NVM subsystem]
                                      ↓
[Validate evidence: Device Self-test]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `LID 06h` | Identifier 06h for the Device Self-test Log Page, containing current operation state and twenty historical results. |
| `CSI = N` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `Controller / Domain / NVM subsystem` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `Device Self-test` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `§5.2.13.1.7` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §5.2.13 is the applicable context.
2. Decode LID 06h at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check CSI = N as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

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
| It answers | How the cited section organizes LID 06h, CSI = N, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §5.2.13, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 209. Annotate the bytes containing LID 06h, decode them, and independently verify CSI = N. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of LID 06h in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand LID 06h and state its unit or object scope?
2. Can the reader explain why CSI = N is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** LID 06h, CSI = N, Controller / Domain / NVM subsystem, Device Self-test, §5.2.13.1.7

**Source keyword index:** `shall`, `may`, `optional`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13, Figure 209, printed pages 215-216, PDF pages 241-242

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 338: Identify Controller Data Structure</strong></summary>

<!-- claim:BASEDIAGMEM-FIG-338-CLAIM figure-table:BASEDIAGMEM-FIG-338 -->

**SPEC.** Figure 338, "Identify Controller Data Structure": Defines the concrete layout or value relationships for Identify Controller Data Structure. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is OACS.DSTS, EDSTT, DSTO.SDSO, HMPRE, HMMIN, HMMINDS, HMMAXD, CTRATT.HMBR, AVSCC.VSCF, ICSVSCC.SNVSCF.

#### Where this Figure fits

Figure 338 sits in §5.2.14.2.1 and acts as a layout checkpoint. Read it after the report mental model has established the owning object and before software turns OACS.DSTS into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a structure or capability field table. Locate it using the structure base and offset, read in byte/bit order, and separate capability gates, value encoding, and reserved areas. Presence in the table does not mean the function is supported.

#### Teaching redraw

```text
[Locate source: OACS.DSTS]
          ↓
[Extract field: EDSTT] → [Apply encoding: DSTO.SDSO]
                                      ↓
[Validate evidence: HMPRE]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `OACS.DSTS` | The Device Self-test Supported bit in Optional Admin Command Support, gating availability of the command. |
| `EDSTT` | Extended Device Self-test Time, the nominal extended-test duration in minutes at power state 0. |
| `DSTO.SDSO` | Device Self-test Options, the Identify Controller field reporting refresh and concurrency options. Here DSTO.SDSO selects its SDSO member field. |
| `HMPRE` | Host Memory Buffer Preferred Size, the controller's preferred allocation in 4-KiB units. |
| `HMMIN` | Host Memory Buffer Minimum Size, the controller's minimum requested size in 4-KiB units. |
| `HMMINDS` | Host Memory Buffer Minimum Descriptor Entry Size, the minimum usable descriptor size in 4-KiB units. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §5.2.14.2.1 is the applicable context.
2. Decode OACS.DSTS at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check EDSTT as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
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
| It answers | How the cited section organizes OACS.DSTS, EDSTT, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §5.2.14.2.1, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 338. Annotate the bytes containing OACS.DSTS, decode them, and independently verify EDSTT. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of OACS.DSTS in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand OACS.DSTS and state its unit or object scope?
2. Can the reader explain why EDSTT is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** OACS.DSTS, EDSTT, DSTO.SDSO, HMPRE, HMMIN, HMMINDS, HMMAXD, CTRATT.HMBR, AVSCC.VSCF, ICSVSCC.SNVSCF

**Source keyword index:** `shall not`, `should not`, `shall`, `should`, `may`, `optional`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.14.2.1, Figure 338, printed pages 340-364, PDF pages 366-390

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 463: Set Features - Data Pointer</strong></summary>

<!-- claim:BASEDIAGMEM-FIG-463-CLAIM figure-table:BASEDIAGMEM-FIG-463 -->

**SPEC.** Figure 463, "Set Features - Data Pointer": Connects Set Features - Data Pointer to a self-test, host-memory, doorbell, or vendor-command engineering boundary. Resolve capability and owner first, decode DPTR, PRP1, PRP2, then verify the completion, log, or memory-lifecycle evidence.

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
<summary><strong>NVME-BASE-2.4 — Figure 464: Set Features - Command Dword 10</strong></summary>

<!-- claim:BASEDIAGMEM-FIG-464-CLAIM figure-table:BASEDIAGMEM-FIG-464 -->

**SPEC.** Figure 464, "Set Features - Command Dword 10": Defines command-specific fields in CDW10 for Set Features. Locate CDW10, then decode the named fields without borrowing semantics from another command. Evidence index: SV, FID.

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
<summary><strong>NVME-BASE-2.4 — Figure 466: Feature Identifiers for Set Features</strong></summary>

<!-- claim:BASEDIAGMEM-FIG-466-CLAIM figure-table:BASEDIAGMEM-FIG-466 -->

**SPEC.** Figure 466, "Feature Identifiers for Set Features": Defines the identifier composition or namespace of values shown by Feature Identifiers for Set Features. Keep the value width, issuing authority, uniqueness scope, and reserved values separate. Evidence index: FID 0Dh, Controller scope, saveable, changeable.

#### Where this Figure fits

Figure 466 sits in §5.2.30 and acts as a identifier checkpoint. Read it after the report mental model has established the owning object and before software turns FID 0Dh into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is an identifier-format Figure. Record width and encoding, then identify assignment authority, uniqueness scope, reserved values, and lifetime. Equal-width identifiers are not automatically interchangeable.

#### Teaching redraw

```text
[Locate source: FID 0Dh]
          ↓
[Extract field: Controller scope] → [Apply encoding: saveable]
                                      ↓
[Validate evidence: changeable]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `FID 0Dh` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `Controller scope` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `saveable` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `changeable` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §5.2.30 is the applicable context.
2. Decode FID 0Dh at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check Controller scope as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
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
| It answers | How the cited section organizes FID 0Dh, Controller scope, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §5.2.30, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 466. Annotate the bytes containing FID 0Dh, decode them, and independently verify Controller scope. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of FID 0Dh in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand FID 0Dh and state its unit or object scope?
2. Can the reader explain why Controller scope is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** FID 0Dh, Controller scope, saveable, changeable

**Source keyword index:** `shall`, `should`, `may`, `optional`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30, Figure 466, printed pages 457-459, PDF pages 483-485

</details>

## Use and limitations

Use the claim IDs as stable PPT traceability keys. Re-check affected claims if the source revision, errata set, or approved scope changes.

## Self-questions and worked answers

28 answered questions revisit this report's scope. Each answer retains the same source links as the teaching module; calculations and debugging examples are informative.

### Q01. What is the governing interpretation for “Start with three boundaries: operation, memory ownership, and encoded address”?

<!-- qa:base-self-test-hmb-emulation-three-boundaries-lead -->

**Answer.**

These sections do not describe one feature. Device Self-test manages a background diagnostic operation, HMB manages ownership transfer of host memory, and DSTRD plus the vendor-command format turn encoded values into safe memory accesses. The shared method is to locate a capability gate, identify the state or ownership transition, and then collect observable evidence.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.6, printed pages 201, PDF pages 227; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.2.3, 8.2.4, printed pages 515-516, 744, PDF pages 541-542, 770; Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.1, 8.2.3, printed pages 56, 744, PDF pages 82, 770; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.14.2.1, 8.1.29, printed pages 356, 374, 733, PDF pages 382, 400, 759

### Q02. Which concepts or conditions must be distinguished in “Start with three boundaries: operation, memory ownership, and encoded address”?

<!-- qa:base-self-test-hmb-emulation-three-boundaries-rows -->

**Answer.**

- Self-test — Operation lifecycle — CQE + LID 06h
- HMB — Exclusive-ownership lifecycle — Get FID 0Dh + disable CQE
- Doorbell emulation — Encoded byte stride — MMIO address/write trace
- Vendor command — Buffer-length contract — VSCF/SNVSCF + NDT/NDM

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.6, printed pages 201, PDF pages 227; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.2.3, 8.2.4, printed pages 515-516, 744, PDF pages 541-542, 770; Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.1, 8.2.3, printed pages 56, 744, PDF pages 82, 770; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.14.2.1, 8.1.29, printed pages 356, 374, 733, PDF pages 382, 400, 759

### Q03. How does “Start with three boundaries: operation, memory ownership, and encoded address” apply to a concrete calculation or operational scenario?

<!-- qa:base-self-test-hmb-emulation-three-boundaries-example -->

**Answer.**

The same Successful Completion means only that a self-test operation started, but for HMB disable it returns ownership to the host. Equal status codes do not imply equal completion boundaries.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.6, printed pages 201, PDF pages 227; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.2.3, 8.2.4, printed pages 515-516, 744, PDF pages 541-542, 770; Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.1, 8.2.3, printed pages 56, 744, PDF pages 82, 770; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.14.2.1, 8.1.29, printed pages 356, 374, 733, PDF pages 382, 400, 759

### Q04. What misinterpretation is most likely in “Start with three boundaries: operation, memory ownership, and encoded address”, and how is it debugged?

<!-- qa:base-self-test-hmb-emulation-three-boundaries-pitfall -->

**Answer.**

Do not reduce every topic to command success or failure. Record which transition succeeded, who currently owns memory, and which log or Get Features result is still required to prove the later outcome.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.6, printed pages 201, PDF pages 227; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.2.3, 8.2.4, printed pages 515-516, 744, PDF pages 541-542, 770; Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.1, 8.2.3, printed pages 56, 744, PDF pages 82, 770; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.14.2.1, 8.1.29, printed pages 356, 374, 733, PDF pages 382, 400, 759

### Q05. What is the governing interpretation for “Device Self-test: gate capability before submitting a background operation”?

<!-- qa:base-self-test-hmb-emulation-selftest-command-state-machine-lead -->

**Answer.**

Self-test is not a synchronous diagnostic RPC. The host first uses OACS.DSTS, DSTO.SDSO, and EDSTT to establish support, concurrency scope, and timing, then constructs the command from NSID and STC. When the Admin CQE returns, the background operation has only entered the lifecycle observed through LID 06h.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.14.2.1, 8.1.8, printed pages 352-358, 614, PDF pages 378-384, 640; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.6, printed pages 199, PDF pages 225; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.6, printed pages 199-200, PDF pages 225-226; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.6, printed pages 200, PDF pages 226; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.6, printed pages 201, PDF pages 227

### Q06. Which concepts or conditions must be distinguished in “Device Self-test: gate capability before submitting a background operation”?

<!-- qa:base-self-test-hmb-emulation-selftest-command-state-machine-rows -->

**Answer.**

- NSID=0 — Controller only — No namespace media
- Active NSID — One namespace — Invalid and inactive status differ
- NSID=FFFFFFFFh — All attached/accessible namespaces — Set is captured at start
- STC=Fh — Abort current operation — Success does not prove one existed

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.14.2.1, 8.1.8, printed pages 352-358, 614, PDF pages 378-384, 640; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.6, printed pages 199, PDF pages 225; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.6, printed pages 199-200, PDF pages 225-226; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.6, printed pages 200, PDF pages 226; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.6, printed pages 201, PDF pages 227

### Q07. How does “Device Self-test: gate capability before submitting a background operation” apply to a concrete calculation or operational scenario?

<!-- qa:base-self-test-hmb-emulation-selftest-command-state-machine-example -->

**Answer.**

To start a short test for namespace 5, use NSID 00000005h and STC 1h, so CDW10 is 00000001h and CDW15 is zero. Immediately issuing extended STC 2h should produce command-specific status 1Dh rather than a second operation.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.14.2.1, 8.1.8, printed pages 352-358, 614, PDF pages 378-384, 640; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.6, printed pages 199, PDF pages 225; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.6, printed pages 199-200, PDF pages 225-226; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.6, printed pages 200, PDF pages 226; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.6, printed pages 201, PDF pages 227

### Q08. What misinterpretation is most likely in “Device Self-test: gate capability before submitting a background operation”, and how is it debugged?

<!-- qa:base-self-test-hmb-emulation-selftest-command-state-machine-pitfall -->

**Answer.**

The common failure is treating the CQE timestamp as test completion or checking only controller-local state when SDSO is one. Retain controller ID, NSID, STC, CDW15, CQE status, and the first subsequent LID 06h.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.14.2.1, 8.1.8, printed pages 352-358, 614, PDF pages 378-384, 640; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.6, printed pages 199, PDF pages 225; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.6, printed pages 199-200, PDF pages 225-226; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.6, printed pages 200, PDF pages 226; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.6, printed pages 201, PDF pages 227

### Q09. What is the governing interpretation for “LID 06h: decode current operation separately from twenty history entries”?

<!-- qa:base-self-test-hmb-emulation-selftest-observe-debug-lead -->

**Answer.**

DSTOS/DSTCS in the header answer what is running now, while RDS1 through RDS20 answer how earlier operations ended. Each result then separates operation code, result reason, segment, validity bitmap, and diagnostic payload. The NVM Command Set gives FLBA an LBA meaning only when FVLD is one.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13, printed pages 213-216, PDF pages 239-242; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.7, printed pages 229-230, PDF pages 255-256; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.7, printed pages 229-230, PDF pages 255-256; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.7, printed pages 231, PDF pages 257; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.7, printed pages 231-232, PDF pages 257-258; Source: NVME-NVM-CS-1.3, Rev. 1.3, §4.1.4.3, printed pages 76, PDF pages 76; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.7, 8.1.8, printed pages 229-232, 614-616, PDF pages 255-258, 640-642

### Q10. Which concepts or conditions must be distinguished in “LID 06h: decode current operation separately from twenty history entries”?

<!-- qa:base-self-test-hmb-emulation-selftest-observe-debug-rows -->

**Answer.**

- DSTOS/DSTCS — Current state/progress — Ignore percentage when DSTOS=0
- DSTR=7h + SEGN — Known first failed segment — Ignore SEGN for other DSTR
- FVLD + FLBA — One failing LBA — Not a list of every failed LBA
- POH + STCT/STC — Failure context — Validity bits still apply

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13, printed pages 213-216, PDF pages 239-242; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.7, printed pages 229-230, PDF pages 255-256; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.7, printed pages 229-230, PDF pages 255-256; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.7, printed pages 231, PDF pages 257; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.7, printed pages 231-232, PDF pages 257-258; Source: NVME-NVM-CS-1.3, Rev. 1.3, §4.1.4.3, printed pages 76, PDF pages 76; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.7, 8.1.8, printed pages 229-232, 614-616, PDF pages 255-258, 640-642

### Q11. How does “LID 06h: decode current operation separately from twenty history entries” apply to a concrete calculation or operational scenario?

<!-- qa:base-self-test-hmb-emulation-selftest-observe-debug-example -->

**Answer.**

The complete log is 564 bytes or 141 dwords, so NUMD is 140 or 008Ch. With LSP 0 and RAE 0, CDW10 is 008C0006h. If RDS1.DSTS is 17h, high nibble 1h means short test and low nibble 7h means a known failed segment; only then read SEGN.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13, printed pages 213-216, PDF pages 239-242; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.7, printed pages 229-230, PDF pages 255-256; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.7, printed pages 229-230, PDF pages 255-256; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.7, printed pages 231, PDF pages 257; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.7, printed pages 231-232, PDF pages 257-258; Source: NVME-NVM-CS-1.3, Rev. 1.3, §4.1.4.3, printed pages 76, PDF pages 76; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.7, 8.1.8, printed pages 229-232, 614-616, PDF pages 255-258, 640-642

### Q12. What misinterpretation is most likely in “LID 06h: decode current operation separately from twenty history entries”, and how is it debugged?

<!-- qa:base-self-test-hmb-emulation-selftest-observe-debug-pitfall -->

**Answer.**

A parser must not declare media failure because FLBA is nonzero. Check DSTR, then FVLD and NSIDVLD, and only then decode bytes 23:16 under the NVM Command Set. Preserve the raw 28-byte result so a validity-decoding defect does not destroy evidence.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13, printed pages 213-216, PDF pages 239-242; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.7, printed pages 229-230, PDF pages 255-256; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.7, printed pages 229-230, PDF pages 255-256; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.7, printed pages 231, PDF pages 257; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.7, printed pages 231-232, PDF pages 257-258; Source: NVME-NVM-CS-1.3, Rev. 1.3, §4.1.4.3, printed pages 76, PDF pages 76; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.7, 8.1.8, printed pages 229-232, 614-616, PDF pages 255-258, 640-642

### Q13. What is the governing interpretation for “HMB: enable/disable completion is an ownership fence”?

<!-- qa:base-self-test-hmb-emulation-hmb-ownership-lifecycle-lead -->

**Answer.**

HMB is not merely controller cache. It is an ownership protocol: the host allocates pages and a descriptor list, stops writing after successful enable, the controller initializes and uses them, and the host disables HMB before reclaiming memory. Modification rights return only when the CQE is posted.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.14.2.1, 8.2.4, printed pages 357, 362, 744, PDF pages 383, 388, 770; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.2.3, 8.2.4, printed pages 515-516, 744, PDF pages 541-542, 770; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.2.3, printed pages 515-516, PDF pages 541-542; Source: NVME-BASE-2.4, Rev. 2.4, §8.2.4, printed pages 744, PDF pages 770

### Q14. Which concepts or conditions must be distinguished in “HMB: enable/disable completion is an ownership fence”?

<!-- qa:base-self-test-hmb-emulation-hmb-ownership-lifecycle-rows -->

**Answer.**

- Before enable — Host owns and initializes descriptors — Validate alignment/count
- After enable CQE — Controller exclusive use — Host shall not write
- Disable in flight — Controller may still retrieve data — Host still waits
- After disable CQE — Host may modify/reclaim — Record fence timestamp

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.14.2.1, 8.2.4, printed pages 357, 362, 744, PDF pages 383, 388, 770; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.2.3, 8.2.4, printed pages 515-516, 744, PDF pages 541-542, 770; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.2.3, printed pages 515-516, PDF pages 541-542; Source: NVME-BASE-2.4, Rev. 2.4, §8.2.4, printed pages 744, PDF pages 770

### Q15. How does “HMB: enable/disable completion is an ownership fence” apply to a concrete calculation or operational scenario?

<!-- qa:base-self-test-hmb-emulation-hmb-ownership-lifecycle-example -->

**Answer.**

If a driver removes DMA mappings after issuing EHM zero but before its CQE, the controller may still retrieve required data; that is a use-after-unmap. The correct fence is disable completion, not the SQ-tail doorbell write.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.14.2.1, 8.2.4, printed pages 357, 362, 744, PDF pages 383, 388, 770; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.2.3, 8.2.4, printed pages 515-516, 744, PDF pages 541-542, 770; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.2.3, printed pages 515-516, PDF pages 541-542; Source: NVME-BASE-2.4, Rev. 2.4, §8.2.4, printed pages 744, PDF pages 770

### Q16. What misinterpretation is most likely in “HMB: enable/disable completion is an ownership fence”, and how is it debugged?

<!-- qa:base-self-test-hmb-emulation-hmb-ownership-lifecycle-pitfall -->

**Answer.**

Treating enable completion as shared host/controller access creates a data race. Track write protection and DMA ownership for HMDL and every range, and release them only after disable completion.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.14.2.1, 8.2.4, printed pages 357, 362, 744, PDF pages 383, 388, 770; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.2.3, 8.2.4, printed pages 515-516, 744, PDF pages 541-542, 770; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.2.3, printed pages 515-516, PDF pages 541-542; Source: NVME-BASE-2.4, Rev. 2.4, §8.2.4, printed pages 744, PDF pages 770

### Q17. What is the governing interpretation for “HMB commands and descriptors: reconcile every size, count, and address with one page model”?

<!-- qa:base-self-test-hmb-emulation-hmb-command-math-lead -->

**Answer.**

HSIZE, BSIZE, and BADD use CC.MPS pages, while HMPRE, HMMIN, and HMMINDS use 4-KiB units. The unit systems are not interchangeable. HMDL is 16-byte aligned with fixed 16-byte entries, and HMDLEC is an entry count—not zero based and not a byte length.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30, 5.2.30.2.3, printed pages 456-459, 516-518, PDF pages 482-485, 542-544; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.2.3, printed pages 517-518, PDF pages 543-544; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.2.3, printed pages 516-518, PDF pages 542-544; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.12, 5.2.30.2.3, printed pages 209-212, 518-519, PDF pages 235-238, 544-545

### Q18. Which concepts or conditions must be distinguished in “HMB commands and descriptors: reconcile every size, count, and address with one page model”?

<!-- qa:base-self-test-hmb-emulation-hmb-command-math-rows -->

**Answer.**

- HMPRE/HMMIN — 4-KiB units — Capability request
- HSIZE/BSIZE — CC.MPS units — Configured memory
- HMDL address — 16-byte aligned — CDW13 low + CDW14 high
- BADD — CC.MPS aligned — BSIZE=0 entry ignored

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30, 5.2.30.2.3, printed pages 456-459, 516-518, PDF pages 482-485, 542-544; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.2.3, printed pages 517-518, PDF pages 543-544; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.2.3, printed pages 516-518, PDF pages 542-544; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.12, 5.2.30.2.3, printed pages 209-212, 518-519, PDF pages 235-238, 544-545

### Q19. How does “HMB commands and descriptors: reconcile every size, count, and address with one page model” apply to a concrete calculation or operational scenario?

<!-- qa:base-self-test-hmb-emulation-hmb-command-math-example -->

**Answer.**

With CC.MPS zero and HSIZE 64, HMB is 256 KiB. HMDL 00000012_34567000h and HMDLEC 2 produce CDW13 34567000h, CDW14 00000012h, and CDW15 2. Two BSIZE-32 ranges are 128 KiB each, totaling 256 KiB.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30, 5.2.30.2.3, printed pages 456-459, 516-518, PDF pages 482-485, 542-544; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.2.3, printed pages 517-518, PDF pages 543-544; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.2.3, printed pages 516-518, PDF pages 542-544; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.12, 5.2.30.2.3, printed pages 209-212, 518-519, PDF pages 235-238, 544-545

### Q20. What misinterpretation is most likely in “HMB commands and descriptors: reconcile every size, count, and address with one page model”, and how is it debugged?

<!-- qa:base-self-test-hmb-emulation-hmb-command-math-pitfall -->

**Answer.**

A common error copies HMPRE directly into HSIZE while CC.MPS is 8 KiB, or sets HMDLEC two while mapping one 16-byte entry. Log capability units, CC.MPS, every BADD/BSIZE, page sum, and command dwords together.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30, 5.2.30.2.3, printed pages 456-459, 516-518, PDF pages 482-485, 542-544; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.2.3, printed pages 517-518, PDF pages 543-544; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.2.3, printed pages 516-518, PDF pages 542-544; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.12, 5.2.30.2.3, printed pages 209-212, 518-519, PDF pages 235-238, 544-545

### Q21. What is the governing interpretation for “HMB across non-operational state, RTD3, and reset: three different boundaries”?

<!-- qa:base-self-test-hmb-emulation-hmb-reset-power-lead -->

**Answer.**

HMNARE is access policy, HMNAR is current state, and MR says whether exactly the same prior contents are returned after reset or RTD3. They are not interchangeable. Controller Level Reset loses the assignment, RTD3 calls for release beforehand, and non-operational restriction only limits access in selected states.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.2.3, printed pages 516-519, PDF pages 542-545; Source: NVME-BASE-2.4, Rev. 2.4, §8.2.4, printed pages 744, PDF pages 770; Source: NVME-BASE-2.4, Rev. 2.4, §8.2.4, printed pages 744, PDF pages 770

### Q22. Which concepts or conditions must be distinguished in “HMB across non-operational state, RTD3, and reset: three different boundaries”?

<!-- qa:base-self-test-hmb-emulation-hmb-reset-power-rows -->

**Answer.**

- HMNARE — Configured policy — Requires CTRATT.HMBR
- HMNAR — Current restriction state — May be zero in operational state
- MR=1 — Return identical old HMB — Same size/address/list/content
- MR=0 — New undefined contents — Controller initializes again

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.2.3, printed pages 516-519, PDF pages 542-545; Source: NVME-BASE-2.4, Rev. 2.4, §8.2.4, printed pages 744, PDF pages 770; Source: NVME-BASE-2.4, Rev. 2.4, §8.2.4, printed pages 744, PDF pages 770

### Q23. How does “HMB across non-operational state, RTD3, and reset: three different boundaries” apply to a concrete calculation or operational scenario?

<!-- qa:base-self-test-hmb-emulation-hmb-reset-power-example -->

**Answer.**

If the allocator returns the same pages after resume but moves HMDL to a new address, MR cannot be one because the descriptor-list address must also match exactly. Enable it as a new MR-zero allocation.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.2.3, printed pages 516-519, PDF pages 542-545; Source: NVME-BASE-2.4, Rev. 2.4, §8.2.4, printed pages 744, PDF pages 770; Source: NVME-BASE-2.4, Rev. 2.4, §8.2.4, printed pages 744, PDF pages 770

### Q24. What misinterpretation is most likely in “HMB across non-operational state, RTD3, and reset: three different boundaries”, and how is it debugged?

<!-- qa:base-self-test-hmb-emulation-hmb-reset-power-pitfall -->

**Answer.**

Do not hash only data pages. MR validation compares HSIZE, HMDL address, HMDLEC, every descriptor, and all HMB contents. NOPPME is also not an HMNARE control; the specification explicitly separates them.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.2.3, printed pages 516-519, PDF pages 542-545; Source: NVME-BASE-2.4, Rev. 2.4, §8.2.4, printed pages 744, PDF pages 770; Source: NVME-BASE-2.4, Rev. 2.4, §8.2.4, printed pages 744, PDF pages 770

### Q25. What is the governing interpretation for “DSTRD and NDT/NDM: decode to byte boundaries before memory access”?

<!-- qa:base-self-test-hmb-emulation-encoded-boundary-safety-lead -->

**Answer.**

Software emulators and vendor-command passthrough both handle untrusted encoded values. DSTRD becomes bytes through 2^(2+x); NDT/NDM are already actual dword counts and are multiplied by four without adding one. The formulas differ, but both prove address and length before MMIO or DMA.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.1, 8.2.3, printed pages 56, 744, PDF pages 82, 770; Source: NVME-BASE-2.4, Rev. 2.4, §8.2.3, printed pages 744, PDF pages 770; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.14.2.1, 8.1.29, printed pages 356, 374, 733, PDF pages 382, 400, 759; Source: NVME-BASE-2.4, Rev. 2.4, §4.1.1, 8.1.29, printed pages 143, 733, PDF pages 169, 759; Source: NVME-BASE-2.4, Rev. 2.4, §4.1.1, 8.1.29, printed pages 143, 733, PDF pages 169, 759; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.6, 5.2.30.2.3, 8.1.29, 8.2.3, printed pages 199-201, 515-519, 733, 744, PDF pages 225-227, 541-545, 759, 770

### Q26. Which concepts or conditions must be distinguished in “DSTRD and NDT/NDM: decode to byte boundaries before memory access”?

<!-- qa:base-self-test-hmb-emulation-encoded-boundary-safety-rows -->

**Answer.**

- DSTRD — 2^(2+x) bytes — 0→4 B; 4→64 B
- NDT — Value×4 data bytes — Not zero based
- NDM — Value×4 metadata bytes — Independent buffer bound
- VSCF/SNVSCF — Format gate — Admin and I/O are separate

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.1, 8.2.3, printed pages 56, 744, PDF pages 82, 770; Source: NVME-BASE-2.4, Rev. 2.4, §8.2.3, printed pages 744, PDF pages 770; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.14.2.1, 8.1.29, printed pages 356, 374, 733, PDF pages 382, 400, 759; Source: NVME-BASE-2.4, Rev. 2.4, §4.1.1, 8.1.29, printed pages 143, 733, PDF pages 169, 759; Source: NVME-BASE-2.4, Rev. 2.4, §4.1.1, 8.1.29, printed pages 143, 733, PDF pages 169, 759; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.6, 5.2.30.2.3, 8.1.29, 8.2.3, printed pages 199-201, 515-519, 733, 744, PDF pages 225-227, 541-545, 759, 770

### Q27. How does “DSTRD and NDT/NDM: decode to byte boundaries before memory access” apply to a concrete calculation or operational scenario?

<!-- qa:base-self-test-hmb-emulation-encoded-boundary-safety-example -->

**Answer.**

An emulator with DSTRD 4 gets a 64-byte stride and can place doorbells on discrete cachelines. Vendor-command NDT 0100h is 256 dwords or 1024 bytes—not 1028 bytes. Retain both raw encoding and decoded bytes for each.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.1, 8.2.3, printed pages 56, 744, PDF pages 82, 770; Source: NVME-BASE-2.4, Rev. 2.4, §8.2.3, printed pages 744, PDF pages 770; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.14.2.1, 8.1.29, printed pages 356, 374, 733, PDF pages 382, 400, 759; Source: NVME-BASE-2.4, Rev. 2.4, §4.1.1, 8.1.29, printed pages 143, 733, PDF pages 169, 759; Source: NVME-BASE-2.4, Rev. 2.4, §4.1.1, 8.1.29, printed pages 143, 733, PDF pages 169, 759; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.6, 5.2.30.2.3, 8.1.29, 8.2.3, printed pages 199-201, 515-519, 733, 744, PDF pages 225-227, 541-545, 759, 770

### Q28. What misinterpretation is most likely in “DSTRD and NDT/NDM: decode to byte boundaries before memory access”, and how is it debugged?

<!-- qa:base-self-test-hmb-emulation-encoded-boundary-safety-pitfall -->

**Answer.**

A helper that treats every NVMe length as zero based adds four bytes to NDT/NDM. Multiplying DSTRD directly by four also fails for nonzero values. Bind each field's formula to its owning Figure.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.1, 8.2.3, printed pages 56, 744, PDF pages 82, 770; Source: NVME-BASE-2.4, Rev. 2.4, §8.2.3, printed pages 744, PDF pages 770; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.14.2.1, 8.1.29, printed pages 356, 374, 733, PDF pages 382, 400, 759; Source: NVME-BASE-2.4, Rev. 2.4, §4.1.1, 8.1.29, printed pages 143, 733, PDF pages 169, 759; Source: NVME-BASE-2.4, Rev. 2.4, §4.1.1, 8.1.29, printed pages 143, 733, PDF pages 169, 759; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.6, 5.2.30.2.3, 8.1.29, 8.2.3, printed pages 199-201, 515-519, 733, 744, PDF pages 225-227, 541-545, 759, 770
