---
layout: post
read_time: true
show_date: true
title: "NVMe over PCIe Transport 1.4: Complete Transport Binding"
date: 2026-08-28
description: "Source-located PCIe/NVMe report for PPT authoring."
lang: en
img: posts/2026/catFlower_title.jpg
tags: [NVMe, PCIe, Specification]
category: NVMe
author: Jia-Chang
github: JiaChangGit/JiaChangGit.github.io/tree/main/DOCS/nvme-spec-report
toc: yes
---
[繁體中文]({% post_url 2026-08-28-nvme-pcie-transport-1-4-zh-tw %})


# NVMe over PCIe Transport 1.4: Complete Transport Binding

Purpose: a source-located engineering report for GitHub Pages and a 100-minute presentation.

Scope: §1-§3 and Annex A; printed/PDF pages 1-48. Only PCIe/memory-based and common NVMe content appears below.

## Source versions

NVM Express NVMe over PCIe Transport Specification, Revision 1.4
NVM Express Base Specification, Revision 2.4

Verification date: 2026-08-29. No additional errata, ECNs, Technical Proposals, controller-vendor documents, or source text from the external PCI Express Base Specification are included.

## Reading map

```text
Write SQE -> Ring SQ tail doorbell -> Controller executes -> Read CQE / ring CQ head
```

The PCIe transport combines queues in host memory with MMIO doorbells; PRPs or SGLs identify data in host-addressable memory.

## Normative language

shall is mandatory, may permits a choice, should expresses a preferred recommendation, and optional means support is not required. The report preserves these terms and never promotes one into another.

## Acronyms first: complete glossary

Every abbreviation below is introduced before it is used in the slide narrative. The term alone is never enough: retain owner, width, unit, scope, and state.

| Acronym / term | Plain-language meaning | Source |
|---|---|---|
| `PCIe` | PCI Express, the transport and device interconnect used by an NVMe memory-based controller. | NVME-PCIE-TRANSPORT-1.4 Rev. 1.4, §2, printed pp. 8, PDF pp. 8 |
| `NVMe` | Non-Volatile Memory Express, the specification family for a host interface to a non-volatile-memory subsystem. | NVME-PCIE-TRANSPORT-1.4 Rev. 1.4, §1.2, printed pp. 6, PDF pp. 6 |
| `MMIO` | Memory-Mapped I/O, access to device registers through CPU memory operations. | NVME-PCIE-TRANSPORT-1.4 Rev. 1.4, §3.1, printed pp. 9-10, PDF pp. 9-10 |
| `BAR` | Base Address Register, a PCI-configuration-space register locating a device memory space. | NVME-PCIE-TRANSPORT-1.4 Rev. 1.4, §3.1, printed pp. 9-10, PDF pp. 9-10 |
| `CAP` | Controller Capabilities, the controller property at offset 00h that reports queue, page-size, timeout, and other capabilities. | NVME-PCIE-TRANSPORT-1.4 Rev. 1.4, §3.1.2.1-3.1.2.2, printed pp. 10-11, PDF pp. 10-11 |
| `DSTRD` | Doorbell Stride, the CAP field determining spacing between adjacent doorbell registers. | NVME-PCIE-TRANSPORT-1.4 Rev. 1.4, §3.1.2.1-3.1.2.2, printed pp. 10-11, PDF pp. 10-11 |
| `SQ` | Submission Queue, the queue into which the host places commands. | NVME-PCIE-TRANSPORT-1.4 Rev. 1.4, §3.4, printed pp. 12-13, PDF pp. 12-13 |
| `CQ` | Completion Queue, the queue into which a controller posts command completions. | NVME-PCIE-TRANSPORT-1.4 Rev. 1.4, §3.4, printed pp. 12-13, PDF pp. 12-13 |
| `SQE` | Submission Queue Entry, one command structure in an SQ. | NVME-PCIE-TRANSPORT-1.4 Rev. 1.4, §3.4, printed pp. 12-13, PDF pp. 12-13 |
| `CQE` | Completion Queue Entry, one completion-result structure in a CQ. | NVME-PCIE-TRANSPORT-1.4 Rev. 1.4, §3.4, printed pp. 12-13, PDF pp. 12-13 |
| `SQyTDBL` | Submission Queue y Tail Doorbell, the MMIO register through which the host publishes the new tail of SQ y. | NVME-PCIE-TRANSPORT-1.4 Rev. 1.4, §3.1.2.1-3.1.2.2, printed pp. 10-11, PDF pp. 10-11 |
| `CQyHDBL` | Completion Queue y Head Doorbell, the MMIO register through which the host publishes the consumed head of CQ y. | NVME-PCIE-TRANSPORT-1.4 Rev. 1.4, §3.1.2.1-3.1.2.2, printed pp. 10-11, PDF pp. 10-11 |
| `MSI` | Message Signaled Interrupt, a PCI mechanism that delivers an interrupt through a memory-write message. | NVME-PCIE-TRANSPORT-1.4 Rev. 1.4, §3.5, printed pp. 13-16, PDF pp. 13-16 |
| `MSI-X` | MSI-X, an extended message-signaled-interrupt mechanism with more vectors, per-vector masking, and a table. | NVME-PCIE-TRANSPORT-1.4 Rev. 1.4, §3.5, printed pp. 13-16, PDF pp. 13-16 |
| `IV` | Interrupt Vector, the vector number assigned to a Completion Queue. | NVME-PCIE-TRANSPORT-1.4 Rev. 1.4, §3.2, printed pp. 11, PDF pp. 11 |
| `FLR` | Function Level Reset, a reset method scoped to one PCIe Function. | NVME-PCIE-TRANSPORT-1.4 Rev. 1.4, §3.3, printed pp. 11-12, PDF pp. 11-12 |
| `AER` | Advanced Error Reporting, the PCIe capability for classifying, masking, and logging link or transaction errors. | NVME-PCIE-TRANSPORT-1.4 Rev. 1.4, §3.7, printed pp. 16, PDF pp. 16 |
| `TLP` | Transaction Layer Packet, a packet carried by the PCIe transaction layer. | NVME-PCIE-TRANSPORT-1.4 Rev. 1.4, §3.7, printed pp. 16, PDF pp. 16 |
| `MPS (PCIe)` | Max Payload Size, the PCIe Device Control setting limiting TLP payload size. | NVME-PCIE-TRANSPORT-1.4 Rev. 1.4, §3.8.1-3.8.7, printed pp. 16-35, PDF pp. 16-35 |
| `MRRS` | Max Read Request Size, the setting limiting the size of read requests issued by a PCIe Function. | NVME-PCIE-TRANSPORT-1.4 Rev. 1.4, §3.8.1-3.8.7, printed pp. 16-35, PDF pp. 16-35 |
| `PMCAP` | Power Management Capability, the base of the PCI power-management capability structure. | NVME-PCIE-TRANSPORT-1.4 Rev. 1.4, §3.8.1-3.8.7, printed pp. 16-35, PDF pp. 16-35 |
| `MSICAP` | MSI Capability, the base of the MSI capability structure. | NVME-PCIE-TRANSPORT-1.4 Rev. 1.4, §3.8.1-3.8.7, printed pp. 16-35, PDF pp. 16-35 |
| `MSIXCAP` | MSI-X Capability, the base of the MSI-X capability structure. | NVME-PCIE-TRANSPORT-1.4 Rev. 1.4, §3.8.1-3.8.7, printed pp. 16-35, PDF pp. 16-35 |
| `PXCAP` | PCI Express Capability, the base of the PCIe capability structure. | NVME-PCIE-TRANSPORT-1.4 Rev. 1.4, §3.8.1-3.8.7, printed pp. 16-35, PDF pp. 16-35 |
| `AERCAP` | Advanced Error Reporting Capability, the base of the AER extended-capability structure. | NVME-PCIE-TRANSPORT-1.4 Rev. 1.4, §3.8.1-3.8.7, printed pp. 16-35, PDF pp. 16-35 |
| `BIR` | BAR Indicator Register, a selector identifying the PCIe BAR that contains a memory structure. | NVME-PCIE-TRANSPORT-1.4 Rev. 1.4, §3.8.1-3.8.7, printed pp. 16-35, PDF pp. 16-35 |
| `PBA` | Pending Bit Array, the MSI-X bit array recording vectors that are pending service. | NVME-PCIE-TRANSPORT-1.4 Rev. 1.4, §3.8.1-3.8.7, printed pp. 16-35, PDF pp. 16-35 |
| `EOM` | Eye Opening Measurement, the procedure and log data for measuring a PCIe receiver eye opening. | NVME-PCIE-TRANSPORT-1.4 Rev. 1.4, §3.9, printed pp. 39-46, PDF pp. 39-46 |
| `TDISP` | TEE Device Interface Security Protocol, a PCIe security protocol related to platform isolation and device-interface state. | NVME-PCIE-TRANSPORT-1.4 Rev. 1.4, §3.8.8-3.8.10, printed pp. 35-39, PDF pp. 35-39 |

## Visual atlas: locate the system before reading fields

Each redraw answers a different question: architecture locates components, sequence shows ownership, decode turns bits into engineering values, and state views preserve failure evidence. These are teaching redraws, not copies of specification artwork.

### Visual 01: Base defines NVMe; the PCIe Transport defines how it is realized on PCIe

**View type:** `architecture`

```text
[Base command/queue/status]
  ├─ [PCIe memory binding]
  ├─ [BAR/MMIO/host memory]
  ├─ [PCIe transaction/link]
  └─ [Controller execution]
```

**Question answered:** Figure 1 shows document applicability and Figure 2 separates protocol responsibility. Engineering analysis separates command semantics from the way host memory, MMIO, configuration space, and interrupts carry the operation. The Transport does not rewrite Base when the two conflict.

**Supporting Figures:** Figure 1, Figure 2

**Sources:** NVME-PCIE-TRANSPORT-1.4 Rev. 1.4, §1.2, printed pp. 6, PDF pp. 6; NVME-PCIE-TRANSPORT-1.4 Rev. 1.4, §1.3, printed pp. 6-7, PDF pp. 6-7; NVME-PCIE-TRANSPORT-1.4 Rev. 1.4, §2, printed pp. 8, PDF pp. 8

### Visual 02: From BAR to doorbell offset: preserve units at every step

**View type:** `decode`

```text
[RAW: Read BAR0/BAR1] → [LOCATE: Map MMIO base] → [DECODE: Read CAP.DSTRD]
[VALIDATE: Compute stride=4<<DSTRD] → [APPLY: Insert queue y and SQ/CQ index] → [EVIDENCE: Access with a legal width]
VALIDATE fail ──→ return to RAW evidence
```

**Question answered:** NVMe controller registers reside in the memory space designated by BAR0/BAR1. Doorbells begin at 1000h; SQ-tail and CQ-head registers for queue y are spaced using CAP.DSTRD. Figures 3-6 form one address derivation rather than four independent register tables.

**Supporting Figures:** Figure 3, Figure 4, Figure 5, Figure 6

**Sources:** NVME-PCIE-TRANSPORT-1.4 Rev. 1.4, §3.1, printed pp. 9-10, PDF pp. 9-10; NVME-PCIE-TRANSPORT-1.4 Rev. 1.4, §3.1.2.1-3.1.2.2, printed pp. 10-11, PDF pp. 10-11

### Visual 03: The eight Figure 8 command-processing steps are ownership handoffs

**View type:** `sequence`

```text
Host / software        Shared object        Controller / evidence
Host → Shared: 1 Host writes SQE
Shared → Controller: 2 Host writes SQ-tail doorbell
Controller → Shared: 3 Controller fetches
Shared → Host: 4 Execute
Host → Shared: 5 Controller writes CQE
Shared → Controller: 6 Interrupt
```

**Question answered:** SQE creation, doorbell write, controller fetch, CQE posting, interrupt delivery, and CQ-head update are not names for one event; they are successive ownership handoffs between host and controller. Their order governs both memory ordering and resource reuse.

**Supporting Figures:** Figure 7, Figure 8

**Sources:** NVME-PCIE-TRANSPORT-1.4 Rev. 1.4, §3.4, printed pp. 12-13, PDF pp. 12-13; NVME-PCIE-TRANSPORT-1.4 Rev. 1.4, §3.2, printed pp. 11, PDF pp. 11

### Visual 04: Interrupt-mode comparison: vector count, masking, and latency are separate dimensions

**View type:** `sequence`

```text
Host / software        Shared object        Controller / evidence
Host → Shared: Select interrupt capability
Shared → Controller: Configure enable/vector
Controller → Shared: Assign IV when creating CQ
Shared → Host: Controller generates interrupt
Host → Shared: Host services every related CQ
Shared → Controller: Tune coalescing if needed
```

**Question answered:** Pin-based, single-message MSI, multiple-message MSI, and MSI-X differ in more than performance. They provide different vector counts, masking locations, and capability structures; interrupt coalescing separately controls when multiple completions produce a notification. Figure 9 and Figures 34-46 belong with queue-to-vector mapping.

**Supporting Figures:** Figure 9, Figure 34, Figure 35, Figure 36, Figure 37, Figure 38, Figure 39, Figure 40, Figure 41, Figure 42, Figure 43, Figure 44, Figure 45, Figure 46

**Sources:** NVME-PCIE-TRANSPORT-1.4 Rev. 1.4, §3.5, printed pp. 13-16, PDF pp. 13-16; NVME-PCIE-TRANSPORT-1.4 Rev. 1.4, §3.2, printed pp. 11, PDF pp. 11; NVME-PCIE-TRANSPORT-1.4 Rev. 1.4, §Annex A, printed pp. 47-48, PDF pp. 47-48

### Visual 05: Configuration space is a capability map; AER is a transport-error map

**View type:** `decode`

```text
[RAW: Read Type 0 header] → [LOCATE: Locate capability chain] → [DECODE: Parse PM/MSI/MSI-X/PXCAP]
[VALIDATE: Locate AERCAP] → [APPLY: Read status+mask+severity] → [EVIDENCE: Preserve header/TLP prefix if nee…]
VALIDATE fail ──→ return to RAW evidence
```

**Question answered:** Figures 10-67 traverse the Type 0 header, Power Management, MSI/MSI-X, PCIe capability, and AER. Locate the capability or extended-capability base before applying offsets. AER status, mask, severity, and header log form one diagnostic set rather than isolated error bits.

**Supporting Figures:** Figure 10, Figure 11, Figure 12, Figure 13, Figure 14, Figure 15, Figure 16, Figure 17, Figure 18, Figure 19, Figure 20, Figure 21, Figure 22, Figure 23, Figure 24, Figure 25, Figure 26, Figure 27, Figure 28, Figure 29, Figure 30, Figure 31, Figure 32, Figure 33, Figure 34, Figure 35, Figure 36, Figure 37, Figure 38, Figure 39, Figure 40, Figure 41, Figure 42, Figure 43, Figure 44, Figure 45, Figure 46, Figure 47, Figure 48, Figure 49, Figure 50, Figure 51, Figure 52, Figure 53, Figure 54, Figure 55, Figure 56, Figure 57, Figure 58, Figure 59, Figure 60, Figure 61, Figure 62, Figure 63, Figure 64, Figure 65, Figure 66, Figure 67

**Sources:** NVME-PCIE-TRANSPORT-1.4 Rev. 1.4, §3.8.1-3.8.7, printed pp. 16-35, PDF pp. 16-35; NVME-PCIE-TRANSPORT-1.4 Rev. 1.4, §3.7, printed pp. 16, PDF pp. 16; NVME-PCIE-TRANSPORT-1.4 Rev. 1.4, §3.6, printed pp. 16, PDF pp. 16

### Visual 06: EOM parser: size first, header second, lane descriptors third

**View type:** `decode`

```text
[RAW: Confirm LID/support] → [LOCATE: Query required size] → [DECODE: Allocate buffer and fetch log]
[VALIDATE: Validate header/count] → [APPLY: Parse each lane descriptor] → [EVIDENCE: Apply measurement unit/scale]
VALIDATE fail ──→ return to RAW evidence
```

**Question answered:** The Physical Interface Receiver Eye Opening Measurement log page is variable length. The host confirms support and required size before parsing specific parameters/identifiers, the header, lane descriptors, and measurement data. Figures 70-77 form a parser pipeline rather than independent field translations.

**Supporting Figures:** Figure 70, Figure 71, Figure 72, Figure 73, Figure 74, Figure 75, Figure 76, Figure 77

**Sources:** NVME-PCIE-TRANSPORT-1.4 Rev. 1.4, §3.9, printed pp. 39-46, PDF pp. 39-46; NVME-PCIE-TRANSPORT-1.4 Rev. 1.4, §Annex A, printed pp. 47-48, PDF pp. 47-48

## Mental Model and complete teaching path

The modules follow engineering causality rather than specification-section order. Related Figures return at the point where they support the flow.

### Module 01: Base defines NVMe; the PCIe Transport defines how it is realized on PCIe

**Explanation.** Figure 1 shows document applicability and Figure 2 separates protocol responsibility. Engineering analysis separates command semantics from the way host memory, MMIO, configuration space, and interrupts carry the operation. The Transport does not rewrite Base when the two conflict.

```text
Base command/queue/status
  ↓
PCIe memory binding
  ↓
BAR/MMIO/host memory
  ↓
PCIe transaction/link
  ↓
Controller execution
```

#### Comparison

| Item | What it answers | Engineering note |
|---|---|---|
| Base | Common command and completion semantics | Highest-precedence NVMe definition |
| PCIe Transport | Address, register, doorbell, and interrupt binding | Adds PCIe-specific requirements |
| PCI-SIG specifications | Native PCIe capability and transaction semantics | This report covers only NVMe-specific statements present in the supplied source |

**Informative example.** Informative example: Base defines Firmware Commit CA/FS and status codes. The PCIe Transport adds where the SQE resides in host memory, where the doorbell resides in BAR0/1 memory space, and how a completion can trigger MSI-X.

**Common mistake / debugging.** Label the owning specification beside every field in a design document. A defect report that merges command status, PCIe AER, and device-register access into one 'NVMe error' usually chooses the wrong recovery layer as well.

**Supporting sources:** NVME-PCIE-TRANSPORT-1.4 Rev. 1.4, §1.2, printed pp. 6, PDF pp. 6; NVME-PCIE-TRANSPORT-1.4 Rev. 1.4, §1.3, printed pp. 6-7, PDF pp. 6-7; NVME-PCIE-TRANSPORT-1.4 Rev. 1.4, §2, printed pp. 8, PDF pp. 8

**Related Figures:** Figure 1, Figure 2

### Module 02: From BAR to doorbell offset: preserve units at every step

**Explanation.** NVMe controller registers reside in the memory space designated by BAR0/BAR1. Doorbells begin at 1000h; SQ-tail and CQ-head registers for queue y are spaced using CAP.DSTRD. Figures 3-6 form one address derivation rather than four independent register tables.

```text
Read BAR0/BAR1
  ↓
Map MMIO base
  ↓
Read CAP.DSTRD
  ↓
Compute stride=4<<DSTRD
  ↓
Insert queue y and SQ/CQ index
  ↓
Access with a legal width
```

#### Comparison

| Item | What it answers | Engineering note |
|---|---|---|
| SQ y tail | 1000h + (2y) x (4 << DSTRD) | Host publishes a new SQ tail |
| CQ y head | 1000h + (2y+1) x (4 << DSTRD) | Host publishes a consumed CQ head |
| Doorbell value | Queue pointer | Does not contain the SQE or CQE body |

**Informative example.** Informative example: with DSTRD=1, stride=4<<1=8 bytes. SQ-tail offset for queue 3 is 1000h+(6x8)=1030h; CQ-head offset is 1000h+(7x8)=1038h. They differ by one stride. Treating DSTRD itself as a byte count makes every nonzero-DSTRD doorbell address wrong.

**Common mistake / debugging.** A doorbell trace retains BAR base, DSTRD, queue ID, formula intermediates, final physical address, written pointer, and access width. Logging only the final virtual address cannot distinguish BAR mapping, stride, or queue-index defects.

**Supporting sources:** NVME-PCIE-TRANSPORT-1.4 Rev. 1.4, §3.1, printed pp. 9-10, PDF pp. 9-10; NVME-PCIE-TRANSPORT-1.4 Rev. 1.4, §3.1.2.1-3.1.2.2, printed pp. 10-11, PDF pp. 10-11

**Related Figures:** Figure 3, Figure 4, Figure 5, Figure 6

### Module 03: The eight Figure 8 command-processing steps are ownership handoffs

**Explanation.** SQE creation, doorbell write, controller fetch, CQE posting, interrupt delivery, and CQ-head update are not names for one event; they are successive ownership handoffs between host and controller. Their order governs both memory ordering and resource reuse.

```text
1 Host writes SQE
  ↓
2 Host writes SQ-tail doorbell
  ↓
3 Controller fetches
  ↓
4 Execute
  ↓
5 Controller writes CQE
  ↓
6 Interrupt
  ↓
7 Host processes CQE
  ↓
8 Host writes CQ-head doorbell
```

#### Comparison

| Item | What it answers | Engineering note |
|---|---|---|
| SQ-slot reuse | Controller has consumed the SQE | Completion SQHD assists tracking |
| Command-buffer reuse | Command completed and data is visible | Check command and data direction |
| CQ-slot release | Host completely consumed the CQE | Then write the CQ-head doorbell |

**Informative example.** Informative example: if the host rings the doorbell before writing the final SQE dword, the controller may fetch a partial command. In the other direction, updating CQ head before fully reading the CQE can let the controller reuse that CQ slot. Both are ownership-ordering failures, not opcode failures.

**Common mistake / debugging.** A timeline records CPU core, SQ tail, doorbell MMIO, SQHD, CQ phase, interrupt vector, and CQ head. Events from separate logs are aligned by CID/SQID and timestamp to isolate lost interrupts, stale phase, or memory-ordering defects.

**Supporting sources:** NVME-PCIE-TRANSPORT-1.4 Rev. 1.4, §3.4, printed pp. 12-13, PDF pp. 12-13; NVME-PCIE-TRANSPORT-1.4 Rev. 1.4, §3.2, printed pp. 11, PDF pp. 11

**Related Figures:** Figure 7, Figure 8

### Module 04: Interrupt-mode comparison: vector count, masking, and latency are separate dimensions

**Explanation.** Pin-based, single-message MSI, multiple-message MSI, and MSI-X differ in more than performance. They provide different vector counts, masking locations, and capability structures; interrupt coalescing separately controls when multiple completions produce a notification. Figure 9 and Figures 34-46 belong with queue-to-vector mapping.

```text
Select interrupt capability
  ↓
Configure enable/vector
  ↓
Assign IV when creating CQ
  ↓
Controller generates interrupt
  ↓
Host services every related CQ
  ↓
Tune coalescing if needed
```

#### Comparison

| Item | What it answers | Engineering note |
|---|---|---|
| Pin-based | Legacy shared signaling | Sharing and masking differ |
| Single MSI | One message/vector | Multiple CQs may share a service path |
| Multiple MSI | A set of contiguous messages | Constrained by MME/MMC capability |
| MSI-X | Table-based vectors with independent masks | Preferred by the specification |

**Informative example.** Informative example: CQ 1 and CQ 2 share vector 5. When vector 5 arrives, the handler cannot inspect only CQ 1; it services every relevant CQ mapped to the vector. Raising the coalescing threshold can reduce interrupt rate while increasing CQE wait time.

**Common mistake / debugging.** Interrupt debugging separates capability enable, CQ IV, MSI/MSI-X mask, pending state, controller CQE, and host handler. 'ISR did not run' cannot distinguish no generation, failed PCIe delivery, a masked vector, or a handler that skipped a CQ.

**Supporting sources:** NVME-PCIE-TRANSPORT-1.4 Rev. 1.4, §3.5, printed pp. 13-16, PDF pp. 13-16; NVME-PCIE-TRANSPORT-1.4 Rev. 1.4, §3.2, printed pp. 11, PDF pp. 11; NVME-PCIE-TRANSPORT-1.4 Rev. 1.4, §Annex A, printed pp. 47-48, PDF pp. 47-48

**Related Figures:** Figure 9, Figure 34, Figure 35, Figure 36, Figure 37, Figure 38, Figure 39, Figure 40, Figure 41, Figure 42, Figure 43, Figure 44, Figure 45, Figure 46

### Module 05: Configuration space is a capability map; AER is a transport-error map

**Explanation.** Figures 10-67 traverse the Type 0 header, Power Management, MSI/MSI-X, PCIe capability, and AER. Locate the capability or extended-capability base before applying offsets. AER status, mask, severity, and header log form one diagnostic set rather than isolated error bits.

```text
Read Type 0 header
  ↓
Locate capability chain
  ↓
Parse PM/MSI/MSI-X/PXCAP
  ↓
Locate AERCAP
  ↓
Read status+mask+severity
  ↓
Preserve header/TLP prefix if needed
```

#### Comparison

| Item | What it answers | Engineering note |
|---|---|---|
| NVMe CQE status | Command execution result | Decode in NVMe command context |
| PCIe Device Status | PCIe Function status summary | Located in PCIe capability |
| AER | Correctable/uncorrectable transport errors | Read status, mask, severity, and header together |
| Power state | Slot limit and device power control | Never choose an NVMe state above the slot power limit |

**Informative example.** Informative example: when an AERUCES bit is set, first check its mask to determine reporting, then its severity for handling, and finally the header log for transaction context. The bit cannot be translated directly into an NVMe SC.

**Common mistake / debugging.** A configuration dump retains the capability base as well as register values. The same relative offset under a different capability base denotes a different field. Capture the complete AER set before clearing any RW1C status.

**Supporting sources:** NVME-PCIE-TRANSPORT-1.4 Rev. 1.4, §3.8.1-3.8.7, printed pp. 16-35, PDF pp. 16-35; NVME-PCIE-TRANSPORT-1.4 Rev. 1.4, §3.7, printed pp. 16, PDF pp. 16; NVME-PCIE-TRANSPORT-1.4 Rev. 1.4, §3.6, printed pp. 16, PDF pp. 16

**Related Figures:** Figure 10, Figure 11, Figure 12, Figure 13, Figure 14, Figure 15, Figure 16, Figure 17, Figure 18, Figure 19, Figure 20, Figure 21, Figure 22, Figure 23, Figure 24, Figure 25, Figure 26, Figure 27, Figure 28, Figure 29, Figure 30, Figure 31, Figure 32, Figure 33, Figure 34, Figure 35, Figure 36, Figure 37, Figure 38, Figure 39, Figure 40, Figure 41, Figure 42, Figure 43, Figure 44, Figure 45, Figure 46, Figure 47, Figure 48, Figure 49, Figure 50, Figure 51, Figure 52, Figure 53, Figure 54, Figure 55, Figure 56, Figure 57, Figure 58, Figure 59, Figure 60, Figure 61, Figure 62, Figure 63, Figure 64, Figure 65, Figure 66, Figure 67

### Module 06: EOM parser: size first, header second, lane descriptors third

**Explanation.** The Physical Interface Receiver Eye Opening Measurement log page is variable length. The host confirms support and required size before parsing specific parameters/identifiers, the header, lane descriptors, and measurement data. Figures 70-77 form a parser pipeline rather than independent field translations.

```text
Confirm LID/support
  ↓
Query required size
  ↓
Allocate buffer and fetch log
  ↓
Validate header/count
  ↓
Parse each lane descriptor
  ↓
Apply measurement unit/scale
```

#### Comparison

| Item | What it answers | Engineering note |
|---|---|---|
| Specific parameter | Selects measurement action and quality/state | Establish request context first |
| Specific identifier | Selects lane/test context | Prevents mixing different measurements |
| Header | Global length and layout | Base for every later offset |
| Lane descriptor | Per-lane boundaries and status | Walk only within returned buffer |

**Informative example.** Informative example: the header claims eight lane descriptors while the returned buffer can contain only six complete descriptors. The parser reports a truncated structure and stops; it must not read beyond the buffer because the platform was expected to have eight lanes.

**Common mistake / debugging.** Retain request parameter, identifier, returned byte count, header-declared size, lane number, and measurement status. A final eye plot alone cannot reproduce selector, length, or lane-mapping defects.

**Supporting sources:** NVME-PCIE-TRANSPORT-1.4 Rev. 1.4, §3.9, printed pp. 39-46, PDF pp. 39-46; NVME-PCIE-TRANSPORT-1.4 Rev. 1.4, §Annex A, printed pp. 47-48, PDF pp. 47-48

**Related Figures:** Figure 70, Figure 71, Figure 72, Figure 73, Figure 74, Figure 75, Figure 76, Figure 77

## Source-located specification findings

The mental model above explains causality. This section preserves each source-located conclusion and its normative strength for speaker notes and review.

### 1. Transport and Base precedence

<!-- claim:PCIE14-SCOPE -->

The PCIe Transport supplements the Base Specification with PCIe-specific structures, extensions, requirements, and behavior; common NVMe behavior remains in Base. In a conflict, Base has higher precedence than a Transport Specification.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §1.2, printed pages 6, PDF pages 6

### 2. PCIe Reset-column convention

<!-- claim:PCIE14-CONVENTION -->

This document inherits Base conventions. In register or property tables, the Reset column instead denotes the post-reset field value defined by the applicable PCI or PCIe specification.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §1.3, printed pages 6-7, PDF pages 6-7

### 3. Transport normative language

<!-- claim:PCIE14-KEYWORDS -->

The force of shall, may, and should remains defined by Base 2.4; a Transport summary must not strengthen or weaken the normative language.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §1.4.1, printed pages 2-3, PDF pages 28-29

### 4. PCIe transport overview

<!-- claim:PCIE14-OVERVIEW -->

The PCIe transport uses memory-mapped I/O for data and register access, along with PCIe configuration space and message-signaled interrupts.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §2, printed pages 8, PDF pages 8

### 5. BAR and register access

<!-- claim:PCIE14-MMIO -->

NVMe controller registers reside in memory space identified by BAR0/BAR1. The host shall use native-width or aligned 32-bit accesses and shall not issue locked accesses; violation produces undefined behavior.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.1, printed pages 9-10, PDF pages 9-10

### 6. SQ/CQ doorbell offsets

<!-- claim:PCIE14-DOORBELL -->

SQ-tail and CQ-head doorbells begin at offset 1000h, with stride determined by CAP.DSTRD; queue identifier y participates in the offset calculation.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.1.2.1-3.1.2.2, printed pages 10-11, PDF pages 10-11

### 7. Queues and interrupt vectors

<!-- claim:PCIE14-QUEUE -->

PCIe permits multiple Submission Queues to share a Completion Queue. If interrupts are enabled when creating the CQ, Interrupt Vector shall be initialized to the corresponding MSI-X or multiple-message MSI vector.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.2, printed pages 11, PDF pages 11

### 8. PCIe reset recovery

<!-- claim:PCIE14-RESET -->

PCIe reset sources include Base controller/reset flows and PCIe-level resets. Recovery logic uses the reset type to determine controller-property, queue, and PCI-configuration state.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.3, printed pages 11-12, PDF pages 11-12

### 9. PCIe command flow

<!-- claim:PCIE14-COMMAND -->

The command flow writes an SQE, updates the SQ-tail doorbell, lets the controller fetch and execute, posts a CQE, optionally interrupts, processes the CQE, and updates the CQ-head doorbell. A doorbell conveys a pointer, not the command body.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.4, printed pages 12-13, PDF pages 12-13

### 10. Interrupt modes and delay

<!-- claim:PCIE14-INTERRUPT -->

Modes are pin-based, single-message MSI, multiple-message MSI, and MSI-X. The specification recommends MSI-X. Coalescing can reduce interrupt rate at the cost of latency, and Admin-CQ interrupts should not be delayed.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.5, printed pages 13-16, PDF pages 13-16

### 11. Slot power limit

<!-- claim:PCIE14-POWER -->

The host shall never select an NVMe power state whose consumption exceeds the PCIe slot power limit; violation results in undefined power behavior.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.6, printed pages 16, PDF pages 16

### 12. NVMe and PCIe error layers

<!-- claim:PCIE14-ERROR -->

NVMe command errors are reported in CQE status, while PCIe transport or link errors use PCIe mechanisms plus this document’s NVMe-specific requirements. Their recovery scopes differ.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.7, printed pages 16, PDF pages 16

### 13. PCI configuration requirements

<!-- claim:PCIE14-CONFIG -->

Section 3.8 defines additional NVMe-controller requirements for the PCI header, Power Management, MSI/MSI-X, PCIe capability, and AER. Original PCI/PCIe field semantics remain governed by PCI-SIG specifications.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1-3.8.7, printed pages 16-35, PDF pages 16-35

### 14. Platform security and isolation dependencies

<!-- claim:PCIE14-SECURITY -->

Power-loss signaling, confidential computing, and TDISP map platform events or isolation state to NVMe-controller behavior. Implementation still requires external PCIe/TDISP specifications not supplied for this report.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.8-3.8.10, printed pages 35-39, PDF pages 35-39

### 15. Receiver-eye measurement

<!-- claim:PCIE14-EOM -->

The Physical Interface Receiver Eye Opening Measurement log page reports measurements through a header, lane descriptors, and EOM data. The host checks support and size before parsing lanes and parameters.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.9, printed pages 39-46, PDF pages 39-46

### 16. Host implementation checklist

<!-- claim:PCIE14-HOST -->

Annex A is an informative host checklist: write the SQE before its doorbell, use phase to identify a new CQE, advance CQ head after consumption, and service every relevant CQ associated with an interrupt vector.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §Annex A, printed pages 47-48, PDF pages 47-48

## Figure index

This report introduces all 77 in-scope Figures. Use the section links below for the 100-minute presentation path; every Figure remains available as an appendix item.

- [§1.2](#section-1-2)

- [§2](#section-2)

- [§3.1](#section-3-1)

- [§3.2](#section-3-2)

- [§3.4](#section-3-4)

- [§3.5](#section-3-5)

- [§3.8](#section-3-8)

- [§3.9](#section-3-9)

## Figure and field-table teaching reference

The source uses Figure numbers for diagrams and field-layout tables. No source artwork is reproduced; compact field and keyword indexes come from the locally verified PDFs.

<a id="section-1-2"></a>

### §1.2

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 1: NVMe Family of Specifications</strong></summary>

<!-- claim:PCIE14-FIG-001-CLAIM figure-table:PCIE14-FIG-001 -->

**SPEC.** Figure 1, "NVMe Family of Specifications": Places NVMe Family of Specifications in the NVMe document and command-set hierarchy. Read from the common Base requirements toward the transport and command-set layer; keep these source-derived labels distinct: NVMe Family.

#### Where this Figure fits

Figure 1 sits in §1.2 and acts as a relationship checkpoint. Read it after the report mental model has established the owning object and before software turns NVMe Family into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This Figure explains a specific relationship or example. Identify each component type and owner, then decide whether each connection represents data flow, control flow, containment, or a condition. Visual placement alone creates no normative requirement.

#### Teaching redraw

```text
[Locate source: NVMe Family]
          ↓
[Extract field: evidence] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `NVMe Family` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §1.2 is the applicable context.
2. Decode NVMe Family at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check the cited condition as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 1 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §1.2 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes NVMe Family, the cited condition, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §1.2, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 1. Annotate the bytes containing NVMe Family, decode them, and independently verify the cited condition. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of NVMe Family in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand NVMe Family and state its unit or object scope?
2. Can the reader explain why the cited condition is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** NVMe Family

**Source keyword index:** none

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §1.2, Figure 1, printed pages 6, PDF pages 6

</details>

<a id="section-2"></a>

### §2

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 2: Example of Transport Protocol Layers</strong></summary>

<!-- claim:PCIE14-FIG-002-CLAIM figure-table:PCIE14-FIG-002 -->

**SPEC.** Figure 2, "Example of Transport Protocol Layers": Separates the responsibilities of the protocol layers in Example of Transport Protocol Layers. Read vertically by layer and horizontally by peer interaction; do not assign a transport rule to the Base layer. Evidence index: Transport Protocol Layers.

#### Where this Figure fits

Figure 2 sits in §2 and acts as a relationship checkpoint. Read it after the report mental model has established the owning object and before software turns Transport Protocol Layers into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This Figure explains a specific relationship or example. Identify each component type and owner, then decide whether each connection represents data flow, control flow, containment, or a condition. Visual placement alone creates no normative requirement.

#### Teaching redraw

```text
[Locate source: Transport Protocol Layers]
          ↓
[Extract field: evidence] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `Transport Protocol Layers` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §2 is the applicable context.
2. Decode Transport Protocol Layers at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check the cited condition as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 2 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §2 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes Transport Protocol Layers, the cited condition, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §2, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 2. Annotate the bytes containing Transport Protocol Layers, decode them, and independently verify the cited condition. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of Transport Protocol Layers in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand Transport Protocol Layers and state its unit or object scope?
2. Can the reader explain why the cited condition is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** Transport Protocol Layers

**Source keyword index:** none

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §2, Figure 2, printed pages 8, PDF pages 8

</details>

<a id="section-3-1"></a>

### §3.1

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 3: PCI Express Registers</strong></summary>

<!-- claim:PCIE14-FIG-003-CLAIM figure-table:PCIE14-FIG-003 -->

**SPEC.** Figure 3, "PCI Express Registers": Defines the concrete layout or value relationships for PCI Express Registers. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is PMCAP, MSICAP, MSIXCAP, MSIX, PXCAP, AERCAP, MSI, MLBAR.

#### Where this Figure fits

Figure 3 sits in §3.1 and acts as a layout checkpoint. Read it after the report mental model has established the owning object and before software turns PMCAP into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a structure or capability field table. Locate it using the structure base and offset, read in byte/bit order, and separate capability gates, value encoding, and reserved areas. Presence in the table does not mean the function is supported.

#### Teaching redraw

```text
[Locate source: PMCAP]
          ↓
[Extract field: MSICAP] → [Apply encoding: MSIXCAP]
                                      ↓
[Validate evidence: MSIX]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `PMCAP` | Power Management Capability, the base of the PCI power-management capability structure. |
| `MSICAP` | MSI Capability, the base of the MSI capability structure. |
| `MSIXCAP` | MSI-X Capability, the base of the MSI-X capability structure. |
| `MSIX` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `PXCAP` | PCI Express Capability, the base of the PCIe capability structure. |
| `AERCAP` | Advanced Error Reporting Capability, the base of the AER extended-capability structure. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.1 is the applicable context.
2. Decode PMCAP at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check MSICAP as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 3 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.1 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes PMCAP, MSICAP, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.1, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 3. Annotate the bytes containing PMCAP, decode them, and independently verify MSICAP. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of PMCAP in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand PMCAP and state its unit or object scope?
2. Can the reader explain why MSICAP is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** PMCAP, MSICAP, MSIXCAP, MSIX, PXCAP, AERCAP, MSI, MLBAR

**Source keyword index:** `shall not`, `shall`, `should`, `may`, `reserved`

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.1, Figure 3, printed pages 9, PDF pages 9

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 4: PCI Express Specific Controller Property Definitions</strong></summary>

<!-- claim:PCIE14-FIG-004-CLAIM figure-table:PCIE14-FIG-004 -->

**SPEC.** Figure 4, "PCI Express Specific Controller Property Definitions": Defines the concrete layout or value relationships for PCI Express Specific Controller Property Definitions. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is SQ0TDBL, CAP.DSTRD, CQ0HDBL, SQ1TDBL, CQ1HDBL, SQ2TDBL, CQ2HDBL, Controller.

#### Where this Figure fits

Figure 4 sits in §3.1 and acts as a relationship checkpoint. Read it after the report mental model has established the owning object and before software turns SQ0TDBL into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This Figure explains a specific relationship or example. Identify each component type and owner, then decide whether each connection represents data flow, control flow, containment, or a condition. Visual placement alone creates no normative requirement.

#### Teaching redraw

```text
[Locate source: SQ0TDBL]
          ↓
[Extract field: CAP.DSTRD] → [Apply encoding: CQ0HDBL]
                                      ↓
[Validate evidence: SQ1TDBL]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `SQ0TDBL` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `CAP.DSTRD` | Controller Capabilities, the controller property at offset 00h that reports queue, page-size, timeout, and other capabilities. Here CAP.DSTRD selects its DSTRD member field. |
| `CQ0HDBL` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `SQ1TDBL` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `CQ1HDBL` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `SQ2TDBL` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.1 is the applicable context.
2. Decode SQ0TDBL at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check CAP.DSTRD as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 4 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.1 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes SQ0TDBL, CAP.DSTRD, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.1, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 4. Annotate the bytes containing SQ0TDBL, decode them, and independently verify CAP.DSTRD. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of SQ0TDBL in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand SQ0TDBL and state its unit or object scope?
2. Can the reader explain why CAP.DSTRD is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** SQ0TDBL, CAP.DSTRD, CQ0HDBL, SQ1TDBL, CQ1HDBL, SQ2TDBL, CQ2HDBL, Controller

**Source keyword index:** `optional`, `reserved`

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.1, Figure 4, printed pages 9-10, PDF pages 9-10

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 5: Offset (1000h + ((2y) * (4 &lt;&lt; CAP.DSTRD))): SQyTDBL - Submission Queue y Tail</strong></summary>

<!-- claim:PCIE14-FIG-005-CLAIM figure-table:PCIE14-FIG-005 -->

**SPEC.** Figure 5, "Offset (1000h + ((2y) * (4 << CAP.DSTRD))): SQyTDBL - Submission Queue y Tail": Shows the queue or command relationship expressed by Offset (1000h + ((2y) * (4 << CAP.DSTRD))): SQyTDBL - Submission Queue y Tail. Trace ownership and direction from host to SQ, controller, and CQ; keep the indexed elements distinct: SQT, CAP.DSTRD, Submission Queue.

#### Where this Figure fits

Figure 5 sits in §3.1.2.1 and acts as a register checkpoint. Read it after the report mental model has established the owning object and before software turns SQT into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a register or property field table. Locate the base offset, verify access width, reset value, and bit range, and only then convert bits into state or capability. Preserve the complete register snapshot so adjacent conditions are not lost by extracting one bit.

#### Teaching redraw

```text
[Locate source: SQT]
          ↓
[Extract field: CAP.DSTRD] → [Apply encoding: Submission Queue]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `SQT` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `CAP.DSTRD` | Controller Capabilities, the controller property at offset 00h that reports queue, page-size, timeout, and other capabilities. Here CAP.DSTRD selects its DSTRD member field. |
| `Submission Queue` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.1.2.1 is the applicable context.
2. Decode SQT at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check CAP.DSTRD as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 5 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.1.2.1 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes SQT, CAP.DSTRD, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.1.2.1, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 5. Annotate the bytes containing SQT, decode them, and independently verify CAP.DSTRD. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of SQT in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand SQT and state its unit or object scope?
2. Can the reader explain why CAP.DSTRD is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** SQT, CAP.DSTRD, Submission Queue

**Source keyword index:** `shall`, `reserved`

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.1.2.1, Figure 5, printed pages 10, PDF pages 10

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 6: Offset (1000h + ((2y + 1) * (4 &lt;&lt; CAP.DSTRD))): CQyHDBL - Completion Queue y Head</strong></summary>

<!-- claim:PCIE14-FIG-006-CLAIM figure-table:PCIE14-FIG-006 -->

**SPEC.** Figure 6, "Offset (1000h + ((2y + 1) * (4 << CAP.DSTRD))): CQyHDBL - Completion Queue y Head": Shows the queue or command relationship expressed by Offset (1000h + ((2y + 1) * (4 << CAP.DSTRD))): CQyHDBL - Completion Queue y Head. Trace ownership and direction from host to SQ, controller, and CQ; keep the indexed elements distinct: CQH, CAP.DSTRD, CC.PI, Completion Queue.

#### Where this Figure fits

Figure 6 sits in §3.1.2.1 and acts as a register checkpoint. Read it after the report mental model has established the owning object and before software turns CQH into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a register or property field table. Locate the base offset, verify access width, reset value, and bit range, and only then convert bits into state or capability. Preserve the complete register snapshot so adjacent conditions are not lost by extracting one bit.

#### Teaching redraw

```text
[Locate source: CQH]
          ↓
[Extract field: CAP.DSTRD] → [Apply encoding: CC.PI]
                                      ↓
[Validate evidence: Completion Queue]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `CQH` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `CAP.DSTRD` | Controller Capabilities, the controller property at offset 00h that reports queue, page-size, timeout, and other capabilities. Here CAP.DSTRD selects its DSTRD member field. |
| `CC.PI` | Controller Configuration, the property through which the host selects settings and enables or disables a controller. Here CC.PI selects its PI member field. |
| `Completion Queue` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.1.2.1 is the applicable context.
2. Decode CQH at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check CAP.DSTRD as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 6 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.1.2.1 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes CQH, CAP.DSTRD, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.1.2.1, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 6. Annotate the bytes containing CQH, decode them, and independently verify CAP.DSTRD. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of CQH in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand CQH and state its unit or object scope?
2. Can the reader explain why CAP.DSTRD is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** CQH, CAP.DSTRD, CC.PI, Completion Queue

**Source keyword index:** `shall`, `reserved`

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.1.2.1, Figure 6, printed pages 10-11, PDF pages 10-11

</details>

<a id="section-3-2"></a>

### §3.2

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 7: Create I/O Completion Queue - Command Dword 11</strong></summary>

<!-- claim:PCIE14-FIG-007-CLAIM figure-table:PCIE14-FIG-007 -->

**SPEC.** Figure 7, "Create I/O Completion Queue - Command Dword 11": Defines command-specific fields in CDW11 for Create I/O Completion Queue. Locate CDW11, then decode the named fields without borrowing semantics from another command. Evidence index: IV, MSI, MSICAP.MC.MME, MSIXCAP.MXC.TS, Completion Queue, Command.

#### Where this Figure fits

Figure 7 sits in §3.2 and acts as a command checkpoint. Read it after the report mental model has established the owning object and before software turns IV into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a command-construction field table. Build the common SQE, locate the specified CDW, encode each bit range, clear reserved bits, and validate the result against transfer length, buffer, and completion status. Equal field names do not imply equal semantics across commands.

#### Teaching redraw

```text
[Locate source: IV]
          ↓
[Extract field: MSI] → [Apply encoding: MSICAP.MC.MME]
                                      ↓
[Validate evidence: MSIXCAP.MXC.TS]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `IV` | Interrupt Vector, the vector number assigned to a Completion Queue. |
| `MSI` | Message Signaled Interrupt, a PCI mechanism that delivers an interrupt through a memory-write message. |
| `MSICAP.MC.MME` | MSI Capability, the base of the MSI capability structure. Here MSICAP.MC.MME selects its MC.MME member field. |
| `MSIXCAP.MXC.TS` | MSI-X Capability, the base of the MSI-X capability structure. Here MSIXCAP.MXC.TS selects its MXC.TS member field. |
| `Completion Queue` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `Command` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.2 is the applicable context.
2. Decode IV at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check MSI as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 7 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.2 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes IV, MSI, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.2, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 7. Annotate the bytes containing IV, decode them, and independently verify MSI. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of IV in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand IV and state its unit or object scope?
2. Can the reader explain why MSI is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** IV, MSI, MSICAP.MC.MME, MSIXCAP.MXC.TS, Completion Queue, Command

**Source keyword index:** `shall not`, `shall`, `should`

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.2, Figure 7, printed pages 11, PDF pages 11

</details>

<a id="section-3-4"></a>

### §3.4

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 8: Command Processing</strong></summary>

<!-- claim:PCIE14-FIG-008-CLAIM figure-table:PCIE14-FIG-008 -->

**SPEC.** Figure 8, "Command Processing": Shows the queue or command relationship expressed by Command Processing. Trace ownership and direction from host to SQ, controller, and CQ; keep the indexed elements distinct: Command.

#### Where this Figure fits

Figure 8 sits in §3.4.1 and acts as a queue checkpoint. Read it after the report mental model has established the owning object and before software turns Command into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a queue or command-flow Figure. Label host and controller ownership first, then trace head, tail, phase, or arbitration changes. An arrow represents a state or ownership transition and does not automatically prove command completion.

#### Teaching redraw

```text
[Locate source: Command]
          ↓
[Extract field: evidence] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `Command` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.4.1 is the applicable context.
2. Decode Command at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check the cited condition as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 8 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.4.1 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes Command, the cited condition, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.4.1, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 8. Annotate the bytes containing Command, decode them, and independently verify the cited condition. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of Command in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand Command and state its unit or object scope?
2. Can the reader explain why the cited condition is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** Command

**Source keyword index:** none

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.4.1, Figure 8, printed pages 13, PDF pages 13

</details>

<a id="section-3-5"></a>

### §3.5

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 9: Pin Based, Single MSI, and Multiple MSI Behavior</strong></summary>

<!-- claim:PCIE14-FIG-009-CLAIM figure-table:PCIE14-FIG-009 -->

**SPEC.** Figure 9, "Pin Based, Single MSI, and Multiple MSI Behavior": Shows the interrupt delivery or masking relationship represented by Pin Based, Single MSI, and Multiple MSI Behavior. Trace the vector/message source, mask state, and delivery destination separately. Evidence index: MSI.

#### Where this Figure fits

Figure 9 sits in §3.5.1 and acts as a interrupt checkpoint. Read it after the report mental model has established the owning object and before software turns MSI into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is an interrupt-delivery or capability Figure. Separate vector source, enable, mask, pending state, delivery, and handler service. An interrupt only signals work; the CQE remains the source of command-completion data.

#### Teaching redraw

```text
[Locate source: MSI]
          ↓
[Extract field: evidence] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `MSI` | Message Signaled Interrupt, a PCI mechanism that delivers an interrupt through a memory-write message. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.5.1 is the applicable context.
2. Decode MSI at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check the cited condition as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 9 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.5.1 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes MSI, the cited condition, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.5.1, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 9. Annotate the bytes containing MSI, decode them, and independently verify the cited condition. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of MSI in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand MSI and state its unit or object scope?
2. Can the reader explain why the cited condition is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** MSI

**Source keyword index:** none

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.5.1, Figure 9, printed pages 15, PDF pages 15

</details>

<a id="section-3-8"></a>

### §3.8

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 10: PCI Express Type 0/1 Common Configuration Space</strong></summary>

<!-- claim:PCIE14-FIG-010-CLAIM figure-table:PCIE14-FIG-010 -->

**SPEC.** Figure 10, "PCI Express Type 0/1 Common Configuration Space": Defines the concrete layout or value relationships for PCI Express Type 0/1 Common Configuration Space. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is PCI Express Type 0/1 Common Configuration Space.

#### Where this Figure fits

Figure 10 sits in §3.8 and acts as a layout checkpoint. Read it after the report mental model has established the owning object and before software turns PCI Express Type 0/1 Common Configuration Space into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a structure or capability field table. Locate it using the structure base and offset, read in byte/bit order, and separate capability gates, value encoding, and reserved areas. Presence in the table does not mean the function is supported.

#### Teaching redraw

```text
[Locate source: PCI Express Type 0/1 Common Configuration Space]
          ↓
[Extract field: evidence] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `PCI Express Type 0/1 Common Configuration Space` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.8 is the applicable context.
2. Decode PCI Express Type 0/1 Common Configuration Space at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check the cited condition as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 10 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.8 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes PCI Express Type 0/1 Common Configuration Space, the cited condition, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.8, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 10. Annotate the bytes containing PCI Express Type 0/1 Common Configuration Space, decode them, and independently verify the cited condition. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of PCI Express Type 0/1 Common Configuration Space in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand PCI Express Type 0/1 Common Configuration Space and state its unit or object scope?
2. Can the reader explain why the cited condition is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** PCI Express Type 0/1 Common Configuration Space

**Source keyword index:** none

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8, Figure 10, printed pages 16-17, PDF pages 16-17

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 11: Offset 00h: ID - Identifiers</strong></summary>

<!-- claim:PCIE14-FIG-011-CLAIM figure-table:PCIE14-FIG-011 -->

**SPEC.** Figure 11, "Offset 00h: ID - Identifiers": Defines ID (Identifiers) at offset 00h and identifies the fields that software must decode at that location. Start at ID, then map bit ranges to access type, reset value, and field meaning. Evidence index: ID, DID, VID.

#### Where this Figure fits

Figure 11 sits in §3.8.1.1 and acts as a register checkpoint. Read it after the report mental model has established the owning object and before software turns ID into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a register or property field table. Locate the base offset, verify access width, reset value, and bit range, and only then convert bits into state or capability. Preserve the complete register snapshot so adjacent conditions are not lost by extracting one bit.

#### Teaching redraw

```text
[Locate source: ID]
          ↓
[Extract field: DID] → [Apply encoding: VID]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `ID` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `DID` | Domain Identifier, the identifier of a domain within an NVM subsystem. |
| `VID` | Vendor ID, a PCI-SIG-assigned identifier for a vendor. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.8.1.1 is the applicable context.
2. Decode ID at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check DID as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 11 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.8.1.1 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes ID, DID, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.8.1.1, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 11. Annotate the bytes containing ID, decode them, and independently verify DID. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of ID in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand ID and state its unit or object scope?
2. Can the reader explain why DID is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** ID, DID, VID

**Source keyword index:** none

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.1, Figure 11, printed pages 17, PDF pages 17

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 12: Offset 04h: CMD - Command</strong></summary>

<!-- claim:PCIE14-FIG-012-CLAIM figure-table:PCIE14-FIG-012 -->

**SPEC.** Figure 12, "Offset 04h: CMD - Command": Defines CMD (Command) at offset 04h and identifies the fields that software must decode at that location. Start at CMD, then map bit ranges to access type, reset value, and field meaning. Evidence index: CMD, SIG, ID, FBE, SERR, SEE, IDSEL, ISWCC.

#### Where this Figure fits

Figure 12 sits in §3.8.1.2 and acts as a register checkpoint. Read it after the report mental model has established the owning object and before software turns CMD into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a register or property field table. Locate the base offset, verify access width, reset value, and bit range, and only then convert bits into state or capability. Preserve the complete register snapshot so adjacent conditions are not lost by extracting one bit.

#### Teaching redraw

```text
[Locate source: CMD]
          ↓
[Extract field: SIG] → [Apply encoding: ID]
                                      ↓
[Validate evidence: FBE]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `CMD` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `SIG` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `ID` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `FBE` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `SERR` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `SEE` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.8.1.2 is the applicable context.
2. Decode CMD at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check SIG as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 12 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.8.1.2 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes CMD, SIG, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.8.1.2, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 12. Annotate the bytes containing CMD, decode them, and independently verify SIG. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of CMD in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand CMD and state its unit or object scope?
2. Can the reader explain why SIG is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** CMD, SIG, ID, FBE, SERR, SEE, IDSEL, ISWCC

**Source keyword index:** `reserved`

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.2, Figure 12, printed pages 17, PDF pages 17

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 13: Offset 06h: STS - Device Status</strong></summary>

<!-- claim:PCIE14-FIG-013-CLAIM figure-table:PCIE14-FIG-013 -->

**SPEC.** Figure 13, "Offset 06h: STS - Device Status": Defines STS (Device Status) at offset 06h and identifies the fields that software must decode at that location. Start at STS, then map bit ranges to access type, reset value, and field meaning. Evidence index: STS, DPE, SSE, RMA, RTA, STA, DEVSEL, DEVT.

#### Where this Figure fits

Figure 13 sits in §3.8.1.3 and acts as a register checkpoint. Read it after the report mental model has established the owning object and before software turns STS into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a register or property field table. Locate the base offset, verify access width, reset value, and bit range, and only then convert bits into state or capability. Preserve the complete register snapshot so adjacent conditions are not lost by extracting one bit.

#### Teaching redraw

```text
[Locate source: STS]
          ↓
[Extract field: DPE] → [Apply encoding: SSE]
                                      ↓
[Validate evidence: RMA]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `STS` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `DPE` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `SSE` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `RMA` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `RTA` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `STA` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.8.1.3 is the applicable context.
2. Decode STS at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check DPE as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 13 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.8.1.3 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes STS, DPE, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.8.1.3, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 13. Annotate the bytes containing STS, decode them, and independently verify DPE. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of STS in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand STS and state its unit or object scope?
2. Can the reader explain why DPE is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** STS, DPE, SSE, RMA, RTA, STA, DEVSEL, DEVT

**Source keyword index:** `reserved`

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.3, Figure 13, printed pages 18, PDF pages 18

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 14: Offset 08h: RID - Revision ID</strong></summary>

<!-- claim:PCIE14-FIG-014-CLAIM figure-table:PCIE14-FIG-014 -->

**SPEC.** Figure 14, "Offset 08h: RID - Revision ID": Defines RID (Revision ID) at offset 08h and identifies the fields that software must decode at that location. Start at RID, then map bit ranges to access type, reset value, and field meaning. Evidence index: RID, ID.

#### Where this Figure fits

Figure 14 sits in §3.8.1.4 and acts as a register checkpoint. Read it after the report mental model has established the owning object and before software turns RID into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a register or property field table. Locate the base offset, verify access width, reset value, and bit range, and only then convert bits into state or capability. Preserve the complete register snapshot so adjacent conditions are not lost by extracting one bit.

#### Teaching redraw

```text
[Locate source: RID]
          ↓
[Extract field: ID] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `RID` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `ID` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.8.1.4 is the applicable context.
2. Decode RID at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check ID as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 14 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.8.1.4 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes RID, ID, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.8.1.4, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 14. Annotate the bytes containing RID, decode them, and independently verify ID. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of RID in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand RID and state its unit or object scope?
2. Can the reader explain why ID is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** RID, ID

**Source keyword index:** none

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.4, Figure 14, printed pages 18, PDF pages 18

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 15: Offset 09h: CC - Class Code</strong></summary>

<!-- claim:PCIE14-FIG-015-CLAIM figure-table:PCIE14-FIG-015 -->

**SPEC.** Figure 15, "Offset 09h: CC - Class Code": Defines CC (Class Code) at offset 09h and identifies the fields that software must decode at that location. Start at CC, then map bit ranges to access type, reset value, and field meaning. Evidence index: CC, BCC, SCC, PI.

#### Where this Figure fits

Figure 15 sits in §3.8.1.5 and acts as a register checkpoint. Read it after the report mental model has established the owning object and before software turns CC into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a register or property field table. Locate the base offset, verify access width, reset value, and bit range, and only then convert bits into state or capability. Preserve the complete register snapshot so adjacent conditions are not lost by extracting one bit.

#### Teaching redraw

```text
[Locate source: CC]
          ↓
[Extract field: BCC] → [Apply encoding: SCC]
                                      ↓
[Validate evidence: PI]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `CC` | Controller Configuration, the property through which the host selects settings and enables or disables a controller. |
| `BCC` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `SCC` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `PI` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.8.1.5 is the applicable context.
2. Decode CC at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check BCC as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 15 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.8.1.5 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes CC, BCC, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.8.1.5, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 15. Annotate the bytes containing CC, decode them, and independently verify BCC. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of CC in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand CC and state its unit or object scope?
2. Can the reader explain why BCC is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** CC, BCC, SCC, PI

**Source keyword index:** none

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.5, Figure 15, printed pages 18, PDF pages 18

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 16: Offset 0Ch: CLS - Cache Line Size</strong></summary>

<!-- claim:PCIE14-FIG-016-CLAIM figure-table:PCIE14-FIG-016 -->

**SPEC.** Figure 16, "Offset 0Ch: CLS - Cache Line Size": Defines CLS (Cache Line Size) at offset 0Ch and identifies the fields that software must decode at that location. Start at CLS, then map bit ranges to access type, reset value, and field meaning. Evidence index: CLS.

#### Where this Figure fits

Figure 16 sits in §3.8.1.6 and acts as a register checkpoint. Read it after the report mental model has established the owning object and before software turns CLS into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a register or property field table. Locate the base offset, verify access width, reset value, and bit range, and only then convert bits into state or capability. Preserve the complete register snapshot so adjacent conditions are not lost by extracting one bit.

#### Teaching redraw

```text
[Locate source: CLS]
          ↓
[Extract field: evidence] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `CLS` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.8.1.6 is the applicable context.
2. Decode CLS at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check the cited condition as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 16 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.8.1.6 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes CLS, the cited condition, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.8.1.6, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 16. Annotate the bytes containing CLS, decode them, and independently verify the cited condition. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of CLS in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand CLS and state its unit or object scope?
2. Can the reader explain why the cited condition is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** CLS

**Source keyword index:** none

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.6, Figure 16, printed pages 18, PDF pages 18

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 17: Offset 0Dh: MLT - Master Latency Timer</strong></summary>

<!-- claim:PCIE14-FIG-017-CLAIM figure-table:PCIE14-FIG-017 -->

**SPEC.** Figure 17, "Offset 0Dh: MLT - Master Latency Timer": Defines MLT (Master Latency Timer) at offset 0Dh and identifies the fields that software must decode at that location. Start at MLT, then map bit ranges to access type, reset value, and field meaning. Evidence index: MLT.

#### Where this Figure fits

Figure 17 sits in §3.8.1.7 and acts as a register checkpoint. Read it after the report mental model has established the owning object and before software turns MLT into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a register or property field table. Locate the base offset, verify access width, reset value, and bit range, and only then convert bits into state or capability. Preserve the complete register snapshot so adjacent conditions are not lost by extracting one bit.

#### Teaching redraw

```text
[Locate source: MLT]
          ↓
[Extract field: evidence] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `MLT` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.8.1.7 is the applicable context.
2. Decode MLT at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check the cited condition as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 17 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.8.1.7 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes MLT, the cited condition, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.8.1.7, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 17. Annotate the bytes containing MLT, decode them, and independently verify the cited condition. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of MLT in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand MLT and state its unit or object scope?
2. Can the reader explain why the cited condition is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** MLT

**Source keyword index:** none

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.7, Figure 17, printed pages 18, PDF pages 18

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 18: Offset 0Eh: HTYPE - Header Type</strong></summary>

<!-- claim:PCIE14-FIG-018-CLAIM figure-table:PCIE14-FIG-018 -->

**SPEC.** Figure 18, "Offset 0Eh: HTYPE - Header Type": Defines HTYPE (Header Type) at offset 0Eh and identifies the fields that software must decode at that location. Start at HTYPE, then map bit ranges to access type, reset value, and field meaning. Evidence index: HTYPE, MFD, HL.

#### Where this Figure fits

Figure 18 sits in §3.8.1.8 and acts as a register checkpoint. Read it after the report mental model has established the owning object and before software turns HTYPE into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a register or property field table. Locate the base offset, verify access width, reset value, and bit range, and only then convert bits into state or capability. Preserve the complete register snapshot so adjacent conditions are not lost by extracting one bit.

#### Teaching redraw

```text
[Locate source: HTYPE]
          ↓
[Extract field: MFD] → [Apply encoding: HL]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `HTYPE` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `MFD` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `HL` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.8.1.8 is the applicable context.
2. Decode HTYPE at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check MFD as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 18 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.8.1.8 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes HTYPE, MFD, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.8.1.8, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 18. Annotate the bytes containing HTYPE, decode them, and independently verify MFD. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of HTYPE in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand HTYPE and state its unit or object scope?
2. Can the reader explain why MFD is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** HTYPE, MFD, HL

**Source keyword index:** none

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.8, Figure 18, printed pages 19, PDF pages 19

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 19: Offset 0Fh: BIST - Built-In Self Test (Optional)</strong></summary>

<!-- claim:PCIE14-FIG-019-CLAIM figure-table:PCIE14-FIG-019 -->

**SPEC.** Figure 19, "Offset 0Fh: BIST - Built-In Self Test (Optional)": Defines BIST (Built-In Self Test (Optional)) at offset 0Fh and identifies the fields that software must decode at that location. Start at BIST, then map bit ranges to access type, reset value, and field meaning. Evidence index: BIST, BC, SB, SIG, CC.

#### Where this Figure fits

Figure 19 sits in §3.8.1.9 and acts as a register checkpoint. Read it after the report mental model has established the owning object and before software turns BIST into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a register or property field table. Locate the base offset, verify access width, reset value, and bit range, and only then convert bits into state or capability. Preserve the complete register snapshot so adjacent conditions are not lost by extracting one bit.

#### Teaching redraw

```text
[Locate source: BIST]
          ↓
[Extract field: BC] → [Apply encoding: SB]
                                      ↓
[Validate evidence: SIG]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `BIST` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `BC` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `SB` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `SIG` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `CC` | Controller Configuration, the property through which the host selects settings and enables or disables a controller. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.8.1.9 is the applicable context.
2. Decode BIST at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check BC as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 19 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.8.1.9 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes BIST, BC, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.8.1.9, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 19. Annotate the bytes containing BIST, decode them, and independently verify BC. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of BIST in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand BIST and state its unit or object scope?
2. Can the reader explain why BC is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** BIST, BC, SB, SIG, CC

**Source keyword index:** `reserved`

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.9, Figure 19, printed pages 19, PDF pages 19

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 20: Offset 10h: MLBAR (BAR0) - Memory Register Base Address, lower 32-bits</strong></summary>

<!-- claim:PCIE14-FIG-020-CLAIM figure-table:PCIE14-FIG-020 -->

**SPEC.** Figure 20, "Offset 10h: MLBAR (BAR0) - Memory Register Base Address, lower 32-bits": Defines the concrete layout or value relationships for Offset 10h: MLBAR (BAR0) - Memory Register Base Address, lower 32-bits. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is BA, PF, TP, RTE, MLBAR, BAR0, SIG.

#### Where this Figure fits

Figure 20 sits in §3.8.1.10 and acts as a register checkpoint. Read it after the report mental model has established the owning object and before software turns BA into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a register or property field table. Locate the base offset, verify access width, reset value, and bit range, and only then convert bits into state or capability. Preserve the complete register snapshot so adjacent conditions are not lost by extracting one bit.

#### Teaching redraw

```text
[Locate source: BA]
          ↓
[Extract field: PF] → [Apply encoding: TP]
                                      ↓
[Validate evidence: RTE]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `BA` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `PF` | Physical Function, a full-featured PCIe function that can manage associated VFs. |
| `TP` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `RTE` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `MLBAR` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `BAR0` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.8.1.10 is the applicable context.
2. Decode BA at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check PF as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 20 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.8.1.10 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes BA, PF, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.8.1.10, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 20. Annotate the bytes containing BA, decode them, and independently verify PF. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of BA in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand BA and state its unit or object scope?
2. Can the reader explain why PF is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** BA, PF, TP, RTE, MLBAR, BAR0, SIG

**Source keyword index:** `may`, `reserved`

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.10, Figure 20, printed pages 19, PDF pages 19

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 21: Offset 14h: MUBAR (BAR1) - Memory Register Base Address, upper 32-bits</strong></summary>

<!-- claim:PCIE14-FIG-021-CLAIM figure-table:PCIE14-FIG-021 -->

**SPEC.** Figure 21, "Offset 14h: MUBAR (BAR1) - Memory Register Base Address, upper 32-bits": Defines the concrete layout or value relationships for Offset 14h: MUBAR (BAR1) - Memory Register Base Address, upper 32-bits. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is BA, MUBAR, BAR1.

#### Where this Figure fits

Figure 21 sits in §3.8.1.11 and acts as a register checkpoint. Read it after the report mental model has established the owning object and before software turns BA into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a register or property field table. Locate the base offset, verify access width, reset value, and bit range, and only then convert bits into state or capability. Preserve the complete register snapshot so adjacent conditions are not lost by extracting one bit.

#### Teaching redraw

```text
[Locate source: BA]
          ↓
[Extract field: MUBAR] → [Apply encoding: BAR1]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `BA` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `MUBAR` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `BAR1` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.8.1.11 is the applicable context.
2. Decode BA at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check MUBAR as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 21 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.8.1.11 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes BA, MUBAR, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.8.1.11, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 21. Annotate the bytes containing BA, decode them, and independently verify MUBAR. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of BA in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand BA and state its unit or object scope?
2. Can the reader explain why MUBAR is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** BA, MUBAR, BAR1

**Source keyword index:** `may`

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.11, Figure 21, printed pages 19, PDF pages 19

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 22: Offset 18h: BAR2 - Index/Data Pair Register Base Address or Vendor Specific</strong></summary>

<!-- claim:PCIE14-FIG-022-CLAIM figure-table:PCIE14-FIG-022 -->

**SPEC.** Figure 22, "Offset 18h: BAR2 - Index/Data Pair Register Base Address or Vendor Specific": Defines BAR2 (Index/Data Pair Register Base Address or Vendor Specific) at offset 18h and identifies the fields that software must decode at that location. Start at BAR2, then map bit ranges to access type, reset value, and field meaning. Evidence index: BA, RTE, BAR2.

#### Where this Figure fits

Figure 22 sits in §3.8.1.12 and acts as a register checkpoint. Read it after the report mental model has established the owning object and before software turns BA into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a register or property field table. Locate the base offset, verify access width, reset value, and bit range, and only then convert bits into state or capability. Preserve the complete register snapshot so adjacent conditions are not lost by extracting one bit.

#### Teaching redraw

```text
[Locate source: BA]
          ↓
[Extract field: RTE] → [Apply encoding: BAR2]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `BA` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `RTE` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `BAR2` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.8.1.12 is the applicable context.
2. Decode BA at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check RTE as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 22 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.8.1.12 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes BA, RTE, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.8.1.12, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 22. Annotate the bytes containing BA, decode them, and independently verify RTE. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of BA in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand BA and state its unit or object scope?
2. Can the reader explain why RTE is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** BA, RTE, BAR2

**Source keyword index:** `may`, `optional`, `reserved`

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.12, Figure 22, printed pages 20, PDF pages 20

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 23: Offset 28h: CCPTR - CardBus CIS Pointer</strong></summary>

<!-- claim:PCIE14-FIG-023-CLAIM figure-table:PCIE14-FIG-023 -->

**SPEC.** Figure 23, "Offset 28h: CCPTR - CardBus CIS Pointer": Defines CCPTR (CardBus CIS Pointer) at offset 28h and identifies the fields that software must decode at that location. Start at CCPTR, then map bit ranges to access type, reset value, and field meaning. Evidence index: CCPTR, CIS.

#### Where this Figure fits

Figure 23 sits in §3.8.1.16 and acts as a register checkpoint. Read it after the report mental model has established the owning object and before software turns CCPTR into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a register or property field table. Locate the base offset, verify access width, reset value, and bit range, and only then convert bits into state or capability. Preserve the complete register snapshot so adjacent conditions are not lost by extracting one bit.

#### Teaching redraw

```text
[Locate source: CCPTR]
          ↓
[Extract field: CIS] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `CCPTR` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `CIS` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.8.1.16 is the applicable context.
2. Decode CCPTR at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check CIS as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 23 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.8.1.16 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes CCPTR, CIS, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.8.1.16, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 23. Annotate the bytes containing CCPTR, decode them, and independently verify CIS. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of CCPTR in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand CCPTR and state its unit or object scope?
2. Can the reader explain why CIS is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** CCPTR, CIS

**Source keyword index:** `shall`

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.16, Figure 23, printed pages 20, PDF pages 20

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 24: Offset 2Ch: SS - Subsystem Identifiers</strong></summary>

<!-- claim:PCIE14-FIG-024-CLAIM figure-table:PCIE14-FIG-024 -->

**SPEC.** Figure 24, "Offset 2Ch: SS - Subsystem Identifiers": Defines SS (Subsystem Identifiers) at offset 2Ch and identifies the fields that software must decode at that location. Start at SS, then map bit ranges to access type, reset value, and field meaning. Evidence index: SSID, SSVID, SS, ID.

#### Where this Figure fits

Figure 24 sits in §3.8.1.17 and acts as a register checkpoint. Read it after the report mental model has established the owning object and before software turns SSID into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a register or property field table. Locate the base offset, verify access width, reset value, and bit range, and only then convert bits into state or capability. Preserve the complete register snapshot so adjacent conditions are not lost by extracting one bit.

#### Teaching redraw

```text
[Locate source: SSID]
          ↓
[Extract field: SSVID] → [Apply encoding: SS]
                                      ↓
[Validate evidence: ID]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `SSID` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `SSVID` | Subsystem Vendor ID, the PCI identifier for a subsystem vendor. |
| `SS` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `ID` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.8.1.17 is the applicable context.
2. Decode SSID at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check SSVID as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 24 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.8.1.17 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes SSID, SSVID, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.8.1.17, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 24. Annotate the bytes containing SSID, decode them, and independently verify SSVID. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of SSID in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand SSID and state its unit or object scope?
2. Can the reader explain why SSVID is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** SSID, SSVID, SS, ID

**Source keyword index:** none

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.17, Figure 24, printed pages 20, PDF pages 20

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 25: Offset 30h: EROM - Expansion ROM (Optional)</strong></summary>

<!-- claim:PCIE14-FIG-025-CLAIM figure-table:PCIE14-FIG-025 -->

**SPEC.** Figure 25, "Offset 30h: EROM - Expansion ROM (Optional)": Defines EROM (Expansion ROM (Optional)) at offset 30h and identifies the fields that software must decode at that location. Start at EROM, then map bit ranges to access type, reset value, and field meaning. Evidence index: RBA, EROM, ROM.

#### Where this Figure fits

Figure 25 sits in §3.8.1.18 and acts as a register checkpoint. Read it after the report mental model has established the owning object and before software turns RBA into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a register or property field table. Locate the base offset, verify access width, reset value, and bit range, and only then convert bits into state or capability. Preserve the complete register snapshot so adjacent conditions are not lost by extracting one bit.

#### Teaching redraw

```text
[Locate source: RBA]
          ↓
[Extract field: EROM] → [Apply encoding: ROM]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `RBA` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `EROM` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `ROM` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.8.1.18 is the applicable context.
2. Decode RBA at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check EROM as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 25 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.8.1.18 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes RBA, EROM, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.8.1.18, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 25. Annotate the bytes containing RBA, decode them, and independently verify EROM. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of RBA in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand RBA and state its unit or object scope?
2. Can the reader explain why EROM is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** RBA, EROM, ROM

**Source keyword index:** none

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.18, Figure 25, printed pages 20, PDF pages 20

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 26: Offset 34h: CAP - Capabilities Pointer</strong></summary>

<!-- claim:PCIE14-FIG-026-CLAIM figure-table:PCIE14-FIG-026 -->

**SPEC.** Figure 26, "Offset 34h: CAP - Capabilities Pointer": Defines CAP (Capabilities Pointer) at offset 34h and identifies the fields that software must decode at that location. Start at CAP, then map bit ranges to access type, reset value, and field meaning. Evidence index: CP, CAP.

#### Where this Figure fits

Figure 26 sits in §3.8.1.19 and acts as a register checkpoint. Read it after the report mental model has established the owning object and before software turns CP into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a register or property field table. Locate the base offset, verify access width, reset value, and bit range, and only then convert bits into state or capability. Preserve the complete register snapshot so adjacent conditions are not lost by extracting one bit.

#### Teaching redraw

```text
[Locate source: CP]
          ↓
[Extract field: CAP] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `CP` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `CAP` | Controller Capabilities, the controller property at offset 00h that reports queue, page-size, timeout, and other capabilities. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.8.1.19 is the applicable context.
2. Decode CP at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check CAP as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 26 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.8.1.19 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes CP, CAP, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.8.1.19, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 26. Annotate the bytes containing CP, decode them, and independently verify CAP. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of CP in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand CP and state its unit or object scope?
2. Can the reader explain why CAP is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** CP, CAP

**Source keyword index:** none

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.19, Figure 26, printed pages 21, PDF pages 21

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 27: Offset 3Ch: INTR - Interrupt Information</strong></summary>

<!-- claim:PCIE14-FIG-027-CLAIM figure-table:PCIE14-FIG-027 -->

**SPEC.** Figure 27, "Offset 3Ch: INTR - Interrupt Information": Defines INTR (Interrupt Information) at offset 3Ch and identifies the fields that software must decode at that location. Start at INTR, then map bit ranges to access type, reset value, and field meaning. Evidence index: IPIN, ILINE, INTR, Interrupt.

#### Where this Figure fits

Figure 27 sits in §3.8.1.20 and acts as a register checkpoint. Read it after the report mental model has established the owning object and before software turns IPIN into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a register or property field table. Locate the base offset, verify access width, reset value, and bit range, and only then convert bits into state or capability. Preserve the complete register snapshot so adjacent conditions are not lost by extracting one bit.

#### Teaching redraw

```text
[Locate source: IPIN]
          ↓
[Extract field: ILINE] → [Apply encoding: INTR]
                                      ↓
[Validate evidence: Interrupt]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `IPIN` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `ILINE` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `INTR` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `Interrupt` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.8.1.20 is the applicable context.
2. Decode IPIN at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check ILINE as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 27 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.8.1.20 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes IPIN, ILINE, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.8.1.20, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 27. Annotate the bytes containing IPIN, decode them, and independently verify ILINE. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of IPIN in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand IPIN and state its unit or object scope?
2. Can the reader explain why ILINE is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** IPIN, ILINE, INTR, Interrupt

**Source keyword index:** none

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.20, Figure 27, printed pages 21, PDF pages 21

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 28: Offset 3Eh: MGNT - Minimum Grant</strong></summary>

<!-- claim:PCIE14-FIG-028-CLAIM figure-table:PCIE14-FIG-028 -->

**SPEC.** Figure 28, "Offset 3Eh: MGNT - Minimum Grant": Defines MGNT (Minimum Grant) at offset 3Eh and identifies the fields that software must decode at that location. Start at MGNT, then map bit ranges to access type, reset value, and field meaning. Evidence index: GNT, MGNT.

#### Where this Figure fits

Figure 28 sits in §3.8.1.21 and acts as a register checkpoint. Read it after the report mental model has established the owning object and before software turns GNT into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a register or property field table. Locate the base offset, verify access width, reset value, and bit range, and only then convert bits into state or capability. Preserve the complete register snapshot so adjacent conditions are not lost by extracting one bit.

#### Teaching redraw

```text
[Locate source: GNT]
          ↓
[Extract field: MGNT] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `GNT` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `MGNT` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.8.1.21 is the applicable context.
2. Decode GNT at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check MGNT as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 28 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.8.1.21 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes GNT, MGNT, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.8.1.21, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 28. Annotate the bytes containing GNT, decode them, and independently verify MGNT. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of GNT in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand GNT and state its unit or object scope?
2. Can the reader explain why MGNT is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** GNT, MGNT

**Source keyword index:** none

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.21, Figure 28, printed pages 21, PDF pages 21

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 29: Offset 3Fh: MLAT - Maximum Latency</strong></summary>

<!-- claim:PCIE14-FIG-029-CLAIM figure-table:PCIE14-FIG-029 -->

**SPEC.** Figure 29, "Offset 3Fh: MLAT - Maximum Latency": Defines MLAT (Maximum Latency) at offset 3Fh and identifies the fields that software must decode at that location. Start at MLAT, then map bit ranges to access type, reset value, and field meaning. Evidence index: LAT, MLAT, CC.

#### Where this Figure fits

Figure 29 sits in §3.8.1.22 and acts as a register checkpoint. Read it after the report mental model has established the owning object and before software turns LAT into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a register or property field table. Locate the base offset, verify access width, reset value, and bit range, and only then convert bits into state or capability. Preserve the complete register snapshot so adjacent conditions are not lost by extracting one bit.

#### Teaching redraw

```text
[Locate source: LAT]
          ↓
[Extract field: MLAT] → [Apply encoding: CC]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `LAT` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `MLAT` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `CC` | Controller Configuration, the property through which the host selects settings and enables or disables a controller. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.8.1.22 is the applicable context.
2. Decode LAT at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check MLAT as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 29 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.8.1.22 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes LAT, MLAT, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.8.1.22, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 29. Annotate the bytes containing LAT, decode them, and independently verify MLAT. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of LAT in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand LAT and state its unit or object scope?
2. Can the reader explain why MLAT is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** LAT, MLAT, CC

**Source keyword index:** none

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.22, Figure 29, printed pages 21, PDF pages 21

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 30: PCI Power Management Capabilities</strong></summary>

<!-- claim:PCIE14-FIG-030-CLAIM figure-table:PCIE14-FIG-030 -->

**SPEC.** Figure 30, "PCI Power Management Capabilities": Defines the concrete layout or value relationships for PCI Power Management Capabilities. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is PMCAP, PID, ID, PC, PMCS.

#### Where this Figure fits

Figure 30 sits in §3.8.1.22 and acts as a relationship checkpoint. Read it after the report mental model has established the owning object and before software turns PMCAP into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This Figure explains a specific relationship or example. Identify each component type and owner, then decide whether each connection represents data flow, control flow, containment, or a condition. Visual placement alone creates no normative requirement.

#### Teaching redraw

```text
[Locate source: PMCAP]
          ↓
[Extract field: PID] → [Apply encoding: ID]
                                      ↓
[Validate evidence: PC]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `PMCAP` | Power Management Capability, the base of the PCI power-management capability structure. |
| `PID` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `ID` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `PC` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `PMCS` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.8.1.22 is the applicable context.
2. Decode PMCAP at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check PID as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 30 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.8.1.22 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes PMCAP, PID, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.8.1.22, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 30. Annotate the bytes containing PMCAP, decode them, and independently verify PID. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of PMCAP in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand PMCAP and state its unit or object scope?
2. Can the reader explain why PID is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** PMCAP, PID, ID, PC, PMCS

**Source keyword index:** none

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.22, Figure 30, printed pages 21, PDF pages 21

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 31: Offset PMCAP: PID - PCI Power Management Capability ID</strong></summary>

<!-- claim:PCIE14-FIG-031-CLAIM figure-table:PCIE14-FIG-031 -->

**SPEC.** Figure 31, "Offset PMCAP: PID - PCI Power Management Capability ID": Defines PID (PCI Power Management Capability ID) at offset PMCAP and identifies the fields that software must decode at that location. Start at PID, then map bit ranges to access type, reset value, and field meaning. Evidence index: NEXT, CID, PMCAP, PID, ID.

#### Where this Figure fits

Figure 31 sits in §3.8.2.1 and acts as a register checkpoint. Read it after the report mental model has established the owning object and before software turns NEXT into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a register or property field table. Locate the base offset, verify access width, reset value, and bit range, and only then convert bits into state or capability. Preserve the complete register snapshot so adjacent conditions are not lost by extracting one bit.

#### Teaching redraw

```text
[Locate source: NEXT]
          ↓
[Extract field: CID] → [Apply encoding: PMCAP]
                                      ↓
[Validate evidence: PID]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `NEXT` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `CID` | Command Identifier, used with the SQ identifier to identify an outstanding command. |
| `PMCAP` | Power Management Capability, the base of the PCI power-management capability structure. |
| `PID` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `ID` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.8.2.1 is the applicable context.
2. Decode NEXT at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check CID as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 31 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.8.2.1 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes NEXT, CID, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.8.2.1, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 31. Annotate the bytes containing NEXT, decode them, and independently verify CID. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of NEXT in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand NEXT and state its unit or object scope?
2. Can the reader explain why CID is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** NEXT, CID, PMCAP, PID, ID

**Source keyword index:** `may`

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.2.1, Figure 31, printed pages 21, PDF pages 21

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 32: Offset PMCAP + 2h: PC - PCI Power Management Capabilities</strong></summary>

<!-- claim:PCIE14-FIG-032-CLAIM figure-table:PCIE14-FIG-032 -->

**SPEC.** Figure 32, "Offset PMCAP + 2h: PC - PCI Power Management Capabilities": Defines PC (PCI Power Management Capabilities) at offset PMCAP + 2h and identifies the fields that software must decode at that location. Start at PC, then map bit ranges to access type, reset value, and field meaning. Evidence index: PSUP, D2S, D1S, AUXC, DSI, PMEC, VS, PMCAP.

#### Where this Figure fits

Figure 32 sits in §3.8.2.2 and acts as a register checkpoint. Read it after the report mental model has established the owning object and before software turns PSUP into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a register or property field table. Locate the base offset, verify access width, reset value, and bit range, and only then convert bits into state or capability. Preserve the complete register snapshot so adjacent conditions are not lost by extracting one bit.

#### Teaching redraw

```text
[Locate source: PSUP]
          ↓
[Extract field: D2S] → [Apply encoding: D1S]
                                      ↓
[Validate evidence: AUXC]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `PSUP` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `D2S` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `D1S` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `AUXC` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `DSI` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `PMEC` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.8.2.2 is the applicable context.
2. Decode PSUP at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check D2S as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 32 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.8.2.2 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes PSUP, D2S, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.8.2.2, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 32. Annotate the bytes containing PSUP, decode them, and independently verify D2S. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of PSUP in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand PSUP and state its unit or object scope?
2. Can the reader explain why D2S is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** PSUP, D2S, D1S, AUXC, DSI, PMEC, VS, PMCAP

**Source keyword index:** `reserved`

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.2.2, Figure 32, printed pages 22, PDF pages 22

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 33: Offset PMCAP + 4h: PMCS - PCI Power Management Control and Status</strong></summary>

<!-- claim:PCIE14-FIG-033-CLAIM figure-table:PCIE14-FIG-033 -->

**SPEC.** Figure 33, "Offset PMCAP + 4h: PMCS - PCI Power Management Control and Status": Defines PMCS (PCI Power Management Control and Status) at offset PMCAP + 4h and identifies the fields that software must decode at that location. Start at PMCS, then map bit ranges to access type, reset value, and field meaning. Evidence index: PMES, DSC, DSE, PMEE, NSFRST, PS, PMCAP, PMCS.

#### Where this Figure fits

Figure 33 sits in §3.8.2.3 and acts as a register checkpoint. Read it after the report mental model has established the owning object and before software turns PMES into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a register or property field table. Locate the base offset, verify access width, reset value, and bit range, and only then convert bits into state or capability. Preserve the complete register snapshot so adjacent conditions are not lost by extracting one bit.

#### Teaching redraw

```text
[Locate source: PMES]
          ↓
[Extract field: DSC] → [Apply encoding: DSE]
                                      ↓
[Validate evidence: PMEE]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `PMES` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `DSC` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `DSE` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `PMEE` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `NSFRST` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `PS` | Power State, a controller power/performance operating point; PS0 has the highest maximum power. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.8.2.3 is the applicable context.
2. Decode PMES at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check DSC as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 33 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.8.2.3 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes PMES, DSC, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.8.2.3, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 33. Annotate the bytes containing PMES, decode them, and independently verify DSC. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of PMES in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand PMES and state its unit or object scope?
2. Can the reader explain why DSC is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** PMES, DSC, DSE, PMEE, NSFRST, PS, PMCAP, PMCS

**Source keyword index:** `optional`, `reserved`

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.2.3, Figure 33, printed pages 22, PDF pages 22

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 34: Message Signaled Interrupt Capability (Optional)</strong></summary>

<!-- claim:PCIE14-FIG-034-CLAIM figure-table:PCIE14-FIG-034 -->

**SPEC.** Figure 34, "Message Signaled Interrupt Capability (Optional)": Defines the concrete layout or value relationships for Message Signaled Interrupt Capability (Optional). Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is MSICAP, MID, ID, MC, MA, MUA, MD, MMASK.

#### Where this Figure fits

Figure 34 sits in §3.8.2.3 and acts as a interrupt checkpoint. Read it after the report mental model has established the owning object and before software turns MSICAP into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is an interrupt-delivery or capability Figure. Separate vector source, enable, mask, pending state, delivery, and handler service. An interrupt only signals work; the CQE remains the source of command-completion data.

#### Teaching redraw

```text
[Locate source: MSICAP]
          ↓
[Extract field: MID] → [Apply encoding: ID]
                                      ↓
[Validate evidence: MC]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `MSICAP` | MSI Capability, the base of the MSI capability structure. |
| `MID` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `ID` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `MC` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `MA` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `MUA` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.8.2.3 is the applicable context.
2. Decode MSICAP at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check MID as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 34 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.8.2.3 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes MSICAP, MID, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.8.2.3, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 34. Annotate the bytes containing MSICAP, decode them, and independently verify MID. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of MSICAP in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand MSICAP and state its unit or object scope?
2. Can the reader explain why MID is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** MSICAP, MID, ID, MC, MA, MUA, MD, MMASK

**Source keyword index:** `optional`

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.2.3, Figure 34, printed pages 22, PDF pages 22

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 35: Offset MSICAP: MID - Message Signaled Interrupt Identifiers</strong></summary>

<!-- claim:PCIE14-FIG-035-CLAIM figure-table:PCIE14-FIG-035 -->

**SPEC.** Figure 35, "Offset MSICAP: MID - Message Signaled Interrupt Identifiers": Defines MID (Message Signaled Interrupt Identifiers) at offset MSICAP and identifies the fields that software must decode at that location. Start at MID, then map bit ranges to access type, reset value, and field meaning. Evidence index: NEXT, CID, MSICAP, MID, ID, MSI, Interrupt.

#### Where this Figure fits

Figure 35 sits in §3.8.3.1 and acts as a register checkpoint. Read it after the report mental model has established the owning object and before software turns NEXT into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a register or property field table. Locate the base offset, verify access width, reset value, and bit range, and only then convert bits into state or capability. Preserve the complete register snapshot so adjacent conditions are not lost by extracting one bit.

#### Teaching redraw

```text
[Locate source: NEXT]
          ↓
[Extract field: CID] → [Apply encoding: MSICAP]
                                      ↓
[Validate evidence: MID]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `NEXT` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `CID` | Command Identifier, used with the SQ identifier to identify an outstanding command. |
| `MSICAP` | MSI Capability, the base of the MSI capability structure. |
| `MID` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `ID` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `MSI` | Message Signaled Interrupt, a PCI mechanism that delivers an interrupt through a memory-write message. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.8.3.1 is the applicable context.
2. Decode NEXT at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check CID as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 35 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.8.3.1 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes NEXT, CID, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.8.3.1, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 35. Annotate the bytes containing NEXT, decode them, and independently verify CID. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of NEXT in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand NEXT and state its unit or object scope?
2. Can the reader explain why CID is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** NEXT, CID, MSICAP, MID, ID, MSI, Interrupt

**Source keyword index:** `may`

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.3.1, Figure 35, printed pages 23, PDF pages 23

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 36: Offset MSICAP + 2h: MC - Message Signaled Interrupt Message Control</strong></summary>

<!-- claim:PCIE14-FIG-036-CLAIM figure-table:PCIE14-FIG-036 -->

**SPEC.** Figure 36, "Offset MSICAP + 2h: MC - Message Signaled Interrupt Message Control": Defines MC (Message Signaled Interrupt Message Control) at offset MSICAP + 2h and identifies the fields that software must decode at that location. Start at MC, then map bit ranges to access type, reset value, and field meaning. Evidence index: PVM, C64, MME, MMC, MSIE, MSICAP, MC, MSI.

#### Where this Figure fits

Figure 36 sits in §3.8.3.2 and acts as a register checkpoint. Read it after the report mental model has established the owning object and before software turns PVM into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a register or property field table. Locate the base offset, verify access width, reset value, and bit range, and only then convert bits into state or capability. Preserve the complete register snapshot so adjacent conditions are not lost by extracting one bit.

#### Teaching redraw

```text
[Locate source: PVM]
          ↓
[Extract field: C64] → [Apply encoding: MME]
                                      ↓
[Validate evidence: MMC]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `PVM` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `C64` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `MME` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `MMC` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `MSIE` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `MSICAP` | MSI Capability, the base of the MSI capability structure. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.8.3.2 is the applicable context.
2. Decode PVM at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check C64 as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 36 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.8.3.2 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes PVM, C64, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.8.3.2, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 36. Annotate the bytes containing PVM, decode them, and independently verify C64. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of PVM in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand PVM and state its unit or object scope?
2. Can the reader explain why C64 is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** PVM, C64, MME, MMC, MSIE, MSICAP, MC, MSI

**Source keyword index:** `shall`, `should`, `may`, `reserved`

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.3.2, Figure 36, printed pages 23, PDF pages 23

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 37: Offset MSICAP + 4h: MA - Message Signaled Interrupt Message Address</strong></summary>

<!-- claim:PCIE14-FIG-037-CLAIM figure-table:PCIE14-FIG-037 -->

**SPEC.** Figure 37, "Offset MSICAP + 4h: MA - Message Signaled Interrupt Message Address": Defines MA (Message Signaled Interrupt Message Address) at offset MSICAP + 4h and identifies the fields that software must decode at that location. Start at MA, then map bit ranges to access type, reset value, and field meaning. Evidence index: ADDR, MSICAP, MA, SIG, Interrupt.

#### Where this Figure fits

Figure 37 sits in §3.8.3.3 and acts as a register checkpoint. Read it after the report mental model has established the owning object and before software turns ADDR into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a register or property field table. Locate the base offset, verify access width, reset value, and bit range, and only then convert bits into state or capability. Preserve the complete register snapshot so adjacent conditions are not lost by extracting one bit.

#### Teaching redraw

```text
[Locate source: ADDR]
          ↓
[Extract field: MSICAP] → [Apply encoding: MA]
                                      ↓
[Validate evidence: SIG]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `ADDR` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `MSICAP` | MSI Capability, the base of the MSI capability structure. |
| `MA` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `SIG` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `Interrupt` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.8.3.3 is the applicable context.
2. Decode ADDR at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check MSICAP as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 37 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.8.3.3 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes ADDR, MSICAP, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.8.3.3, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 37. Annotate the bytes containing ADDR, decode them, and independently verify MSICAP. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of ADDR in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand ADDR and state its unit or object scope?
2. Can the reader explain why MSICAP is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** ADDR, MSICAP, MA, SIG, Interrupt

**Source keyword index:** `reserved`

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.3.3, Figure 37, printed pages 23, PDF pages 23

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 38: Offset MSICAP + 8h: MUA - Message Signaled Interrupt Upper Address</strong></summary>

<!-- claim:PCIE14-FIG-038-CLAIM figure-table:PCIE14-FIG-038 -->

**SPEC.** Figure 38, "Offset MSICAP + 8h: MUA - Message Signaled Interrupt Upper Address": Defines MUA (Message Signaled Interrupt Upper Address) at offset MSICAP + 8h and identifies the fields that software must decode at that location. Start at MUA, then map bit ranges to access type, reset value, and field meaning. Evidence index: UADDR, MSICAP, MUA, MSI, Interrupt.

#### Where this Figure fits

Figure 38 sits in §3.8.3.4 and acts as a register checkpoint. Read it after the report mental model has established the owning object and before software turns UADDR into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a register or property field table. Locate the base offset, verify access width, reset value, and bit range, and only then convert bits into state or capability. Preserve the complete register snapshot so adjacent conditions are not lost by extracting one bit.

#### Teaching redraw

```text
[Locate source: UADDR]
          ↓
[Extract field: MSICAP] → [Apply encoding: MUA]
                                      ↓
[Validate evidence: MSI]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `UADDR` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `MSICAP` | MSI Capability, the base of the MSI capability structure. |
| `MUA` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `MSI` | Message Signaled Interrupt, a PCI mechanism that delivers an interrupt through a memory-write message. |
| `Interrupt` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.8.3.4 is the applicable context.
2. Decode UADDR at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check MSICAP as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 38 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.8.3.4 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes UADDR, MSICAP, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.8.3.4, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 38. Annotate the bytes containing UADDR, decode them, and independently verify MSICAP. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of UADDR in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand UADDR and state its unit or object scope?
2. Can the reader explain why MSICAP is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** UADDR, MSICAP, MUA, MSI, Interrupt

**Source keyword index:** none

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.3.4, Figure 38, printed pages 23, PDF pages 23

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 39: Offset MSICAP + Ch: MD - Message Signaled Interrupt Message Data</strong></summary>

<!-- claim:PCIE14-FIG-039-CLAIM figure-table:PCIE14-FIG-039 -->

**SPEC.** Figure 39, "Offset MSICAP + Ch: MD - Message Signaled Interrupt Message Data": Defines MD (Message Signaled Interrupt Message Data) at offset MSICAP + Ch and identifies the fields that software must decode at that location. Start at MD, then map bit ranges to access type, reset value, and field meaning. Evidence index: DATA, MSICAP, MD, MSI, AD, Interrupt.

#### Where this Figure fits

Figure 39 sits in §3.8.3.5 and acts as a register checkpoint. Read it after the report mental model has established the owning object and before software turns DATA into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a register or property field table. Locate the base offset, verify access width, reset value, and bit range, and only then convert bits into state or capability. Preserve the complete register snapshot so adjacent conditions are not lost by extracting one bit.

#### Teaching redraw

```text
[Locate source: DATA]
          ↓
[Extract field: MSICAP] → [Apply encoding: MD]
                                      ↓
[Validate evidence: MSI]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `DATA` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `MSICAP` | MSI Capability, the base of the MSI capability structure. |
| `MD` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `MSI` | Message Signaled Interrupt, a PCI mechanism that delivers an interrupt through a memory-write message. |
| `AD` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `Interrupt` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.8.3.5 is the applicable context.
2. Decode DATA at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check MSICAP as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 39 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.8.3.5 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes DATA, MSICAP, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.8.3.5, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 39. Annotate the bytes containing DATA, decode them, and independently verify MSICAP. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of DATA in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand DATA and state its unit or object scope?
2. Can the reader explain why MSICAP is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** DATA, MSICAP, MD, MSI, AD, Interrupt

**Source keyword index:** none

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.3.5, Figure 39, printed pages 23, PDF pages 23

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 40: Offset MSICAP + 10h: MMASK - Message Signaled Interrupt Mask Bits (Optional)</strong></summary>

<!-- claim:PCIE14-FIG-040-CLAIM figure-table:PCIE14-FIG-040 -->

**SPEC.** Figure 40, "Offset MSICAP + 10h: MMASK - Message Signaled Interrupt Mask Bits (Optional)": Defines MMASK (Message Signaled Interrupt Mask Bits (Optional)) at offset MSICAP + 10h and identifies the fields that software must decode at that location. Start at MMASK, then map bit ranges to access type, reset value, and field meaning. Evidence index: MASK, MSICAP, MMASK, Interrupt.

#### Where this Figure fits

Figure 40 sits in §3.8.3.6 and acts as a register checkpoint. Read it after the report mental model has established the owning object and before software turns MASK into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a register or property field table. Locate the base offset, verify access width, reset value, and bit range, and only then convert bits into state or capability. Preserve the complete register snapshot so adjacent conditions are not lost by extracting one bit.

#### Teaching redraw

```text
[Locate source: MASK]
          ↓
[Extract field: MSICAP] → [Apply encoding: MMASK]
                                      ↓
[Validate evidence: Interrupt]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `MASK` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `MSICAP` | MSI Capability, the base of the MSI capability structure. |
| `MMASK` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `Interrupt` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.8.3.6 is the applicable context.
2. Decode MASK at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check MSICAP as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 40 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.8.3.6 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes MASK, MSICAP, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.8.3.6, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 40. Annotate the bytes containing MASK, decode them, and independently verify MSICAP. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of MASK in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand MASK and state its unit or object scope?
2. Can the reader explain why MSICAP is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** MASK, MSICAP, MMASK, Interrupt

**Source keyword index:** none

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.3.6, Figure 40, printed pages 24, PDF pages 24

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 41: Offset MSICAP + 14h: MPEND - Message Signaled Interrupt Pending Bits (Optional)</strong></summary>

<!-- claim:PCIE14-FIG-041-CLAIM figure-table:PCIE14-FIG-041 -->

**SPEC.** Figure 41, "Offset MSICAP + 14h: MPEND - Message Signaled Interrupt Pending Bits (Optional)": Defines MPEND (Message Signaled Interrupt Pending Bits (Optional)) at offset MSICAP + 14h and identifies the fields that software must decode at that location. Start at MPEND, then map bit ranges to access type, reset value, and field meaning. Evidence index: PEND, MSICAP, MPEND, MSIX, Interrupt.

#### Where this Figure fits

Figure 41 sits in §3.8.3.7 and acts as a register checkpoint. Read it after the report mental model has established the owning object and before software turns PEND into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a register or property field table. Locate the base offset, verify access width, reset value, and bit range, and only then convert bits into state or capability. Preserve the complete register snapshot so adjacent conditions are not lost by extracting one bit.

#### Teaching redraw

```text
[Locate source: PEND]
          ↓
[Extract field: MSICAP] → [Apply encoding: MPEND]
                                      ↓
[Validate evidence: MSIX]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `PEND` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `MSICAP` | MSI Capability, the base of the MSI capability structure. |
| `MPEND` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `MSIX` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `Interrupt` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.8.3.7 is the applicable context.
2. Decode PEND at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check MSICAP as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 41 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.8.3.7 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes PEND, MSICAP, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.8.3.7, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 41. Annotate the bytes containing PEND, decode them, and independently verify MSICAP. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of PEND in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand PEND and state its unit or object scope?
2. Can the reader explain why MSICAP is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** PEND, MSICAP, MPEND, MSIX, Interrupt

**Source keyword index:** `optional`

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.3.7, Figure 41, printed pages 24, PDF pages 24

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 42: MSI-X Capability (Optional)</strong></summary>

<!-- claim:PCIE14-FIG-042-CLAIM figure-table:PCIE14-FIG-042 -->

**SPEC.** Figure 42, "MSI-X Capability (Optional)": Defines the concrete layout or value relationships for MSI-X Capability (Optional). Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is MSIX, MSIXCAP, MXID, ID, MXC, MTAB, BIR, MPBA.

#### Where this Figure fits

Figure 42 sits in §3.8.3.7 and acts as a interrupt checkpoint. Read it after the report mental model has established the owning object and before software turns MSIX into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is an interrupt-delivery or capability Figure. Separate vector source, enable, mask, pending state, delivery, and handler service. An interrupt only signals work; the CQE remains the source of command-completion data.

#### Teaching redraw

```text
[Locate source: MSIX]
          ↓
[Extract field: MSIXCAP] → [Apply encoding: MXID]
                                      ↓
[Validate evidence: ID]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `MSIX` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `MSIXCAP` | MSI-X Capability, the base of the MSI-X capability structure. |
| `MXID` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `ID` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `MXC` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `MTAB` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.8.3.7 is the applicable context.
2. Decode MSIX at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check MSIXCAP as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 42 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.8.3.7 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes MSIX, MSIXCAP, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.8.3.7, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 42. Annotate the bytes containing MSIX, decode them, and independently verify MSIXCAP. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of MSIX in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand MSIX and state its unit or object scope?
2. Can the reader explain why MSIXCAP is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** MSIX, MSIXCAP, MXID, ID, MXC, MTAB, BIR, MPBA

**Source keyword index:** `shall not`, `shall`, `should`, `may`

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.3.7, Figure 42, printed pages 24, PDF pages 24

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 43: Offset MSIXCAP: MXID - MSI-X Identifiers</strong></summary>

<!-- claim:PCIE14-FIG-043-CLAIM figure-table:PCIE14-FIG-043 -->

**SPEC.** Figure 43, "Offset MSIXCAP: MXID - MSI-X Identifiers": Defines MXID (MSI-X Identifiers) at offset MSIXCAP and identifies the fields that software must decode at that location. Start at MXID, then map bit ranges to access type, reset value, and field meaning. Evidence index: NEXT, CID, MSIXCAP, MXID, MSIX, ID.

#### Where this Figure fits

Figure 43 sits in §3.8.4.1 and acts as a register checkpoint. Read it after the report mental model has established the owning object and before software turns NEXT into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a register or property field table. Locate the base offset, verify access width, reset value, and bit range, and only then convert bits into state or capability. Preserve the complete register snapshot so adjacent conditions are not lost by extracting one bit.

#### Teaching redraw

```text
[Locate source: NEXT]
          ↓
[Extract field: CID] → [Apply encoding: MSIXCAP]
                                      ↓
[Validate evidence: MXID]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `NEXT` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `CID` | Command Identifier, used with the SQ identifier to identify an outstanding command. |
| `MSIXCAP` | MSI-X Capability, the base of the MSI-X capability structure. |
| `MXID` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `MSIX` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `ID` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.8.4.1 is the applicable context.
2. Decode NEXT at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check CID as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 43 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.8.4.1 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes NEXT, CID, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.8.4.1, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 43. Annotate the bytes containing NEXT, decode them, and independently verify CID. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of NEXT in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand NEXT and state its unit or object scope?
2. Can the reader explain why CID is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** NEXT, CID, MSIXCAP, MXID, MSIX, ID

**Source keyword index:** `may`

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.4.1, Figure 43, printed pages 24, PDF pages 24

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 44: Offset MSIXCAP + 2h: MXC - MSI-X Message Control</strong></summary>

<!-- claim:PCIE14-FIG-044-CLAIM figure-table:PCIE14-FIG-044 -->

**SPEC.** Figure 44, "Offset MSIXCAP + 2h: MXC - MSI-X Message Control": Defines MXC (MSI-X Message Control) at offset MSIXCAP + 2h and identifies the fields that software must decode at that location. Start at MXC, then map bit ranges to access type, reset value, and field meaning. Evidence index: MXE, FM, TS, MSIXCAP, MXC, MSIX, MSI, SIG.

#### Where this Figure fits

Figure 44 sits in §3.8.4.2 and acts as a register checkpoint. Read it after the report mental model has established the owning object and before software turns MXE into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a register or property field table. Locate the base offset, verify access width, reset value, and bit range, and only then convert bits into state or capability. Preserve the complete register snapshot so adjacent conditions are not lost by extracting one bit.

#### Teaching redraw

```text
[Locate source: MXE]
          ↓
[Extract field: FM] → [Apply encoding: TS]
                                      ↓
[Validate evidence: MSIXCAP]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `MXE` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `FM` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `TS` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `MSIXCAP` | MSI-X Capability, the base of the MSI-X capability structure. |
| `MXC` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `MSIX` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.8.4.2 is the applicable context.
2. Decode MXE at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check FM as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 44 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.8.4.2 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes MXE, FM, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.8.4.2, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 44. Annotate the bytes containing MXE, decode them, and independently verify FM. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of MXE in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand MXE and state its unit or object scope?
2. Can the reader explain why FM is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** MXE, FM, TS, MSIXCAP, MXC, MSIX, MSI, SIG

**Source keyword index:** `reserved`

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.4.2, Figure 44, printed pages 24-25, PDF pages 24-25

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 45: Offset MSIXCAP + 4h: MTAB - MSI-X Table Offset / Table BIR</strong></summary>

<!-- claim:PCIE14-FIG-045-CLAIM figure-table:PCIE14-FIG-045 -->

**SPEC.** Figure 45, "Offset MSIXCAP + 4h: MTAB - MSI-X Table Offset / Table BIR": Defines MTAB (MSI-X Table Offset / Table BIR) at offset MSIXCAP + 4h and identifies the fields that software must decode at that location. Start at MTAB, then map bit ranges to access type, reset value, and field meaning. Evidence index: TO, TBIR, MSIXCAP, MTAB, MSIX, BIR, MSI, BAR.

#### Where this Figure fits

Figure 45 sits in §3.8.4.3 and acts as a register checkpoint. Read it after the report mental model has established the owning object and before software turns TO into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a register or property field table. Locate the base offset, verify access width, reset value, and bit range, and only then convert bits into state or capability. Preserve the complete register snapshot so adjacent conditions are not lost by extracting one bit.

#### Teaching redraw

```text
[Locate source: TO]
          ↓
[Extract field: TBIR] → [Apply encoding: MSIXCAP]
                                      ↓
[Validate evidence: MTAB]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `TO` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `TBIR` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `MSIXCAP` | MSI-X Capability, the base of the MSI-X capability structure. |
| `MTAB` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `MSIX` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `BIR` | BAR Indicator Register, a selector identifying the PCIe BAR that contains a memory structure. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.8.4.3 is the applicable context.
2. Decode TO at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check TBIR as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 45 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.8.4.3 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes TO, TBIR, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.8.4.3, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 45. Annotate the bytes containing TO, decode them, and independently verify TBIR. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of TO in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand TO and state its unit or object scope?
2. Can the reader explain why TBIR is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** TO, TBIR, MSIXCAP, MTAB, MSIX, BIR, MSI, BAR

**Source keyword index:** `reserved`

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.4.3, Figure 45, printed pages 25, PDF pages 25

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 46: Offset MSIXCAP + 8h: MPBA - MSI-X PBA Offset / PBA BIR</strong></summary>

<!-- claim:PCIE14-FIG-046-CLAIM figure-table:PCIE14-FIG-046 -->

**SPEC.** Figure 46, "Offset MSIXCAP + 8h: MPBA - MSI-X PBA Offset / PBA BIR": Defines MPBA (MSI-X PBA Offset / PBA BIR) at offset MSIXCAP + 8h and identifies the fields that software must decode at that location. Start at MPBA, then map bit ranges to access type, reset value, and field meaning. Evidence index: PBAO, PBIR, MSIXCAP, MPBA, MSIX, PBA, BIR, MSI.

#### Where this Figure fits

Figure 46 sits in §3.8.4.4 and acts as a register checkpoint. Read it after the report mental model has established the owning object and before software turns PBAO into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a register or property field table. Locate the base offset, verify access width, reset value, and bit range, and only then convert bits into state or capability. Preserve the complete register snapshot so adjacent conditions are not lost by extracting one bit.

#### Teaching redraw

```text
[Locate source: PBAO]
          ↓
[Extract field: PBIR] → [Apply encoding: MSIXCAP]
                                      ↓
[Validate evidence: MPBA]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `PBAO` | Page Base Address and Offset, the first-PRP layout combining a page base address with an in-page offset. |
| `PBIR` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `MSIXCAP` | MSI-X Capability, the base of the MSI-X capability structure. |
| `MPBA` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `MSIX` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `PBA` | Pending Bit Array, the MSI-X bit array recording vectors that are pending service. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.8.4.4 is the applicable context.
2. Decode PBAO at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check PBIR as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 46 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.8.4.4 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes PBAO, PBIR, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.8.4.4, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 46. Annotate the bytes containing PBAO, decode them, and independently verify PBIR. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of PBAO in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand PBAO and state its unit or object scope?
2. Can the reader explain why PBIR is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** PBAO, PBIR, MSIXCAP, MPBA, MSIX, PBA, BIR, MSI

**Source keyword index:** `may`, `reserved`

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.4.4, Figure 46, printed pages 25, PDF pages 25

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 47: PCI Express Capability</strong></summary>

<!-- claim:PCIE14-FIG-047-CLAIM figure-table:PCIE14-FIG-047 -->

**SPEC.** Figure 47, "PCI Express Capability": Defines the concrete layout or value relationships for PCI Express Capability. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is PXCAP, PXID, ID, PXDCAP, PXDC, PXDS, PXLCAP, PXLC.

#### Where this Figure fits

Figure 47 sits in §3.8.5 and acts as a layout checkpoint. Read it after the report mental model has established the owning object and before software turns PXCAP into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a structure or capability field table. Locate it using the structure base and offset, read in byte/bit order, and separate capability gates, value encoding, and reserved areas. Presence in the table does not mean the function is supported.

#### Teaching redraw

```text
[Locate source: PXCAP]
          ↓
[Extract field: PXID] → [Apply encoding: ID]
                                      ↓
[Validate evidence: PXDCAP]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `PXCAP` | PCI Express Capability, the base of the PCIe capability structure. |
| `PXID` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `ID` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `PXDCAP` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `PXDC` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `PXDS` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.8.5 is the applicable context.
2. Decode PXCAP at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check PXID as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 47 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.8.5 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes PXCAP, PXID, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.8.5, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 47. Annotate the bytes containing PXCAP, decode them, and independently verify PXID. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of PXCAP in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand PXCAP and state its unit or object scope?
2. Can the reader explain why PXID is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** PXCAP, PXID, ID, PXDCAP, PXDC, PXDS, PXLCAP, PXLC

**Source keyword index:** none

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.5, Figure 47, printed pages 26, PDF pages 26

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 48: Offset PXCAP: PXID - PCI Express Capability ID</strong></summary>

<!-- claim:PCIE14-FIG-048-CLAIM figure-table:PCIE14-FIG-048 -->

**SPEC.** Figure 48, "Offset PXCAP: PXID - PCI Express Capability ID": Defines PXID (PCI Express Capability ID) at offset PXCAP and identifies the fields that software must decode at that location. Start at PXID, then map bit ranges to access type, reset value, and field meaning. Evidence index: NEXT, CID, PXCAP, PXID, ID.

#### Where this Figure fits

Figure 48 sits in §3.8.5.1 and acts as a register checkpoint. Read it after the report mental model has established the owning object and before software turns NEXT into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a register or property field table. Locate the base offset, verify access width, reset value, and bit range, and only then convert bits into state or capability. Preserve the complete register snapshot so adjacent conditions are not lost by extracting one bit.

#### Teaching redraw

```text
[Locate source: NEXT]
          ↓
[Extract field: CID] → [Apply encoding: PXCAP]
                                      ↓
[Validate evidence: PXID]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `NEXT` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `CID` | Command Identifier, used with the SQ identifier to identify an outstanding command. |
| `PXCAP` | PCI Express Capability, the base of the PCIe capability structure. |
| `PXID` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `ID` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.8.5.1 is the applicable context.
2. Decode NEXT at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check CID as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 48 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.8.5.1 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes NEXT, CID, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.8.5.1, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 48. Annotate the bytes containing NEXT, decode them, and independently verify CID. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of NEXT in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand NEXT and state its unit or object scope?
2. Can the reader explain why CID is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** NEXT, CID, PXCAP, PXID, ID

**Source keyword index:** `may`

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.5.1, Figure 48, printed pages 26, PDF pages 26

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 49: Offset PXCAP + 2h: PXCAP - PCI Express Capabilities</strong></summary>

<!-- claim:PCIE14-FIG-049-CLAIM figure-table:PCIE14-FIG-049 -->

**SPEC.** Figure 49, "Offset PXCAP + 2h: PXCAP - PCI Express Capabilities": Defines PXCAP (PCI Express Capabilities) at offset PXCAP + 2h and identifies the fields that software must decode at that location. Start at PXCAP, then map bit ranges to access type, reset value, and field meaning. Evidence index: IMN, SI, DPT, VER, PXCAP, SIG, MSI.

#### Where this Figure fits

Figure 49 sits in §3.8.5.2 and acts as a register checkpoint. Read it after the report mental model has established the owning object and before software turns IMN into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a register or property field table. Locate the base offset, verify access width, reset value, and bit range, and only then convert bits into state or capability. Preserve the complete register snapshot so adjacent conditions are not lost by extracting one bit.

#### Teaching redraw

```text
[Locate source: IMN]
          ↓
[Extract field: SI] → [Apply encoding: DPT]
                                      ↓
[Validate evidence: VER]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `IMN` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `SI` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `DPT` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `VER` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `PXCAP` | PCI Express Capability, the base of the PCIe capability structure. |
| `SIG` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.8.5.2 is the applicable context.
2. Decode IMN at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check SI as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 49 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.8.5.2 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes IMN, SI, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.8.5.2, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 49. Annotate the bytes containing IMN, decode them, and independently verify SI. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of IMN in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand IMN and state its unit or object scope?
2. Can the reader explain why SI is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** IMN, SI, DPT, VER, PXCAP, SIG, MSI

**Source keyword index:** `shall`, `reserved`

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.5.2, Figure 49, printed pages 26, PDF pages 26

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 50: Offset PXCAP + 4h: PXDCAP - PCI Express Device Capabilities</strong></summary>

<!-- claim:PCIE14-FIG-050-CLAIM figure-table:PCIE14-FIG-050 -->

**SPEC.** Figure 50, "Offset PXCAP + 4h: PXDCAP - PCI Express Device Capabilities": Defines PXDCAP (PCI Express Device Capabilities) at offset PXCAP + 4h and identifies the fields that software must decode at that location. Start at PXDCAP, then map bit ranges to access type, reset value, and field meaning. Evidence index: FLRC, CSPLS, CSPLV, RER, L1L, L0SL, ETFS, PFS.

#### Where this Figure fits

Figure 50 sits in §3.8.5.3 and acts as a register checkpoint. Read it after the report mental model has established the owning object and before software turns FLRC into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a register or property field table. Locate the base offset, verify access width, reset value, and bit range, and only then convert bits into state or capability. Preserve the complete register snapshot so adjacent conditions are not lost by extracting one bit.

#### Teaching redraw

```text
[Locate source: FLRC]
          ↓
[Extract field: CSPLS] → [Apply encoding: CSPLV]
                                      ↓
[Validate evidence: RER]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `FLRC` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `CSPLS` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `CSPLV` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `RER` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `L1L` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `L0SL` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.8.5.3 is the applicable context.
2. Decode FLRC at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check CSPLS as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 50 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.8.5.3 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes FLRC, CSPLS, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.8.5.3, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 50. Annotate the bytes containing FLRC, decode them, and independently verify CSPLS. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of FLRC in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand FLRC and state its unit or object scope?
2. Can the reader explain why CSPLS is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** FLRC, CSPLS, CSPLV, RER, L1L, L0SL, ETFS, PFS

**Source keyword index:** `shall`, `may`, `optional`, `reserved`

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.5.3, Figure 50, printed pages 26-27, PDF pages 26-27

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 51: Offset PXCAP + 8h: PXDC - PCI Express Device Control</strong></summary>

<!-- claim:PCIE14-FIG-051-CLAIM figure-table:PCIE14-FIG-051 -->

**SPEC.** Figure 51, "Offset PXCAP + 8h: PXDC - PCI Express Device Control": Defines PXDC (PCI Express Device Control) at offset PXCAP + 8h and identifies the fields that software must decode at that location. Start at PXDC, then map bit ranges to access type, reset value, and field meaning. Evidence index: IFLR, MRRS, ENS, APPME, PFE, ETE, MPS, ERO.

#### Where this Figure fits

Figure 51 sits in §3.8.5.4 and acts as a register checkpoint. Read it after the report mental model has established the owning object and before software turns IFLR into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a register or property field table. Locate the base offset, verify access width, reset value, and bit range, and only then convert bits into state or capability. Preserve the complete register snapshot so adjacent conditions are not lost by extracting one bit.

#### Teaching redraw

```text
[Locate source: IFLR]
          ↓
[Extract field: MRRS] → [Apply encoding: ENS]
                                      ↓
[Validate evidence: APPME]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `IFLR` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `MRRS` | Max Read Request Size, the setting limiting the size of read requests issued by a PCIe Function. |
| `ENS` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `APPME` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `PFE` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `ETE` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.8.5.4 is the applicable context.
2. Decode IFLR at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check MRRS as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 51 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.8.5.4 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes IFLR, MRRS, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.8.5.4, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 51. Annotate the bytes containing IFLR, decode them, and independently verify MRRS. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of IFLR in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand IFLR and state its unit or object scope?
2. Can the reader explain why MRRS is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** IFLR, MRRS, ENS, APPME, PFE, ETE, MPS, ERO

**Source keyword index:** `shall not`, `shall`, `may`

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.5.4, Figure 51, printed pages 27-28, PDF pages 27-28

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 52: Offset PXCAP + Ah: PXDS - PCI Express Device Status</strong></summary>

<!-- claim:PCIE14-FIG-052-CLAIM figure-table:PCIE14-FIG-052 -->

**SPEC.** Figure 52, "Offset PXCAP + Ah: PXDS - PCI Express Device Status": Defines PXDS (PCI Express Device Status) at offset PXCAP + Ah and identifies the fields that software must decode at that location. Start at PXDS, then map bit ranges to access type, reset value, and field meaning. Evidence index: TP, APD, URD, FED, NFED, CED, PXCAP, PXDS.

#### Where this Figure fits

Figure 52 sits in §3.8.5.5 and acts as a register checkpoint. Read it after the report mental model has established the owning object and before software turns TP into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a register or property field table. Locate the base offset, verify access width, reset value, and bit range, and only then convert bits into state or capability. Preserve the complete register snapshot so adjacent conditions are not lost by extracting one bit.

#### Teaching redraw

```text
[Locate source: TP]
          ↓
[Extract field: APD] → [Apply encoding: URD]
                                      ↓
[Validate evidence: FED]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `TP` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `APD` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `URD` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `FED` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `NFED` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `CED` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.8.5.5 is the applicable context.
2. Decode TP at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check APD as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 52 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.8.5.5 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes TP, APD, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.8.5.5, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 52. Annotate the bytes containing TP, decode them, and independently verify APD. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of TP in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand TP and state its unit or object scope?
2. Can the reader explain why APD is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** TP, APD, URD, FED, NFED, CED, PXCAP, PXDS

**Source keyword index:** `shall`, `reserved`

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.5.5, Figure 52, printed pages 28, PDF pages 28

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 53: Offset PXCAP + Ch: PXLCAP - PCI Express Link Capabilities</strong></summary>

<!-- claim:PCIE14-FIG-053-CLAIM figure-table:PCIE14-FIG-053 -->

**SPEC.** Figure 53, "Offset PXCAP + Ch: PXLCAP - PCI Express Link Capabilities": Defines PXLCAP (PCI Express Link Capabilities) at offset PXCAP + Ch and identifies the fields that software must decode at that location. Start at PXLCAP, then map bit ranges to access type, reset value, and field meaning. Evidence index: PN, AOC, LBNC, DLLLA, SDERC, CPM, L1EL, L0SEL.

#### Where this Figure fits

Figure 53 sits in §3.8.5.6 and acts as a register checkpoint. Read it after the report mental model has established the owning object and before software turns PN into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a register or property field table. Locate the base offset, verify access width, reset value, and bit range, and only then convert bits into state or capability. Preserve the complete register snapshot so adjacent conditions are not lost by extracting one bit.

#### Teaching redraw

```text
[Locate source: PN]
          ↓
[Extract field: AOC] → [Apply encoding: LBNC]
                                      ↓
[Validate evidence: DLLLA]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `PN` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `AOC` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `LBNC` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `DLLLA` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `SDERC` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `CPM` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.8.5.6 is the applicable context.
2. Decode PN at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check AOC as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 53 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.8.5.6 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes PN, AOC, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.8.5.6, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 53. Annotate the bytes containing PN, decode them, and independently verify AOC. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of PN in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand PN and state its unit or object scope?
2. Can the reader explain why AOC is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** PN, AOC, LBNC, DLLLA, SDERC, CPM, L1EL, L0SEL

**Source keyword index:** `shall not`, `shall`, `reserved`

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.5.6, Figure 53, printed pages 28-29, PDF pages 28-29

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 54: Offset PXCAP + 10h: PXLC - PCI Express Link Control</strong></summary>

<!-- claim:PCIE14-FIG-054-CLAIM figure-table:PCIE14-FIG-054 -->

**SPEC.** Figure 54, "Offset PXCAP + 10h: PXLC - PCI Express Link Control": Defines PXLC (PCI Express Link Control) at offset PXCAP + 10h and identifies the fields that software must decode at that location. Start at PXLC, then map bit ranges to access type, reset value, and field meaning. Evidence index: HAWD, ECPM, ES, CCC, RCB, ASPMC, PXCAP, PXLC.

#### Where this Figure fits

Figure 54 sits in §3.8.5.7 and acts as a register checkpoint. Read it after the report mental model has established the owning object and before software turns HAWD into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a register or property field table. Locate the base offset, verify access width, reset value, and bit range, and only then convert bits into state or capability. Preserve the complete register snapshot so adjacent conditions are not lost by extracting one bit.

#### Teaching redraw

```text
[Locate source: HAWD]
          ↓
[Extract field: ECPM] → [Apply encoding: ES]
                                      ↓
[Validate evidence: CCC]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `HAWD` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `ECPM` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `ES` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `CCC` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `RCB` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `ASPMC` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.8.5.7 is the applicable context.
2. Decode HAWD at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check ECPM as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 54 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.8.5.7 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes HAWD, ECPM, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.8.5.7, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 54. Annotate the bytes containing HAWD, decode them, and independently verify ECPM. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of HAWD in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand HAWD and state its unit or object scope?
2. Can the reader explain why ECPM is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** HAWD, ECPM, ES, CCC, RCB, ASPMC, PXCAP, PXLC

**Source keyword index:** `shall`, `reserved`

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.5.7, Figure 54, printed pages 29, PDF pages 29

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 55: Offset PXCAP + 12h: PXLS - PCI Express Link Status</strong></summary>

<!-- claim:PCIE14-FIG-055-CLAIM figure-table:PCIE14-FIG-055 -->

**SPEC.** Figure 55, "Offset PXCAP + 12h: PXLS - PCI Express Link Status": Defines PXLS (PCI Express Link Status) at offset PXCAP + 12h and identifies the fields that software must decode at that location. Start at PXLS, then map bit ranges to access type, reset value, and field meaning. Evidence index: SCC, NLW, CLS, PXCAP, PXLS, SIG.

#### Where this Figure fits

Figure 55 sits in §3.8.5.8 and acts as a register checkpoint. Read it after the report mental model has established the owning object and before software turns SCC into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a register or property field table. Locate the base offset, verify access width, reset value, and bit range, and only then convert bits into state or capability. Preserve the complete register snapshot so adjacent conditions are not lost by extracting one bit.

#### Teaching redraw

```text
[Locate source: SCC]
          ↓
[Extract field: NLW] → [Apply encoding: CLS]
                                      ↓
[Validate evidence: PXCAP]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `SCC` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `NLW` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `CLS` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `PXCAP` | PCI Express Capability, the base of the PCIe capability structure. |
| `PXLS` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `SIG` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.8.5.8 is the applicable context.
2. Decode SCC at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check NLW as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 55 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.8.5.8 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes SCC, NLW, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.8.5.8, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 55. Annotate the bytes containing SCC, decode them, and independently verify NLW. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of SCC in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand SCC and state its unit or object scope?
2. Can the reader explain why NLW is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** SCC, NLW, CLS, PXCAP, PXLS, SIG

**Source keyword index:** `shall`, `reserved`

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.5.8, Figure 55, printed pages 29, PDF pages 29

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 56: Offset PXCAP + 24h: PXDCAP2 - PCI Express Device Capabilities 2</strong></summary>

<!-- claim:PCIE14-FIG-056-CLAIM figure-table:PCIE14-FIG-056 -->

**SPEC.** Figure 56, "Offset PXCAP + 24h: PXDCAP2 - PCI Express Device Capabilities 2": Defines PXDCAP2 (PCI Express Device Capabilities 2) at offset PXCAP + 24h and identifies the fields that software must decode at that location. Start at PXDCAP2, then map bit ranges to access type, reset value, and field meaning. Evidence index: MEETP, EETPS, EFFS, OBFFS, TPHCS, LTRS, NPRPR, AORS.

#### Where this Figure fits

Figure 56 sits in §3.8.5.9 and acts as a register checkpoint. Read it after the report mental model has established the owning object and before software turns MEETP into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a register or property field table. Locate the base offset, verify access width, reset value, and bit range, and only then convert bits into state or capability. Preserve the complete register snapshot so adjacent conditions are not lost by extracting one bit.

#### Teaching redraw

```text
[Locate source: MEETP]
          ↓
[Extract field: EETPS] → [Apply encoding: EFFS]
                                      ↓
[Validate evidence: OBFFS]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `MEETP` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `EETPS` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `EFFS` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `OBFFS` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `TPHCS` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `LTRS` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.8.5.9 is the applicable context.
2. Decode MEETP at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check EETPS as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 56 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.8.5.9 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes MEETP, EETPS, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.8.5.9, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 56. Annotate the bytes containing MEETP, decode them, and independently verify EETPS. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of MEETP in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand MEETP and state its unit or object scope?
2. Can the reader explain why EETPS is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** MEETP, EETPS, EFFS, OBFFS, TPHCS, LTRS, NPRPR, AORS

**Source keyword index:** `shall`, `optional`, `reserved`

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.5.9, Figure 56, printed pages 30, PDF pages 30

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 57: Offset PXCAP + 28h: PXDC2 - PCI Express Device Control 2</strong></summary>

<!-- claim:PCIE14-FIG-057-CLAIM figure-table:PCIE14-FIG-057 -->

**SPEC.** Figure 57, "Offset PXCAP + 28h: PXDC2 - PCI Express Device Control 2": Defines PXDC2 (PCI Express Device Control 2) at offset PXCAP + 28h and identifies the fields that software must decode at that location. Start at PXDC2, then map bit ranges to access type, reset value, and field meaning. Evidence index: OBFFE, LTRME, CTD, CTV, PXCAP, PXDC2, SIG, OBFF.

#### Where this Figure fits

Figure 57 sits in §3.8.5.10 and acts as a register checkpoint. Read it after the report mental model has established the owning object and before software turns OBFFE into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a register or property field table. Locate the base offset, verify access width, reset value, and bit range, and only then convert bits into state or capability. Preserve the complete register snapshot so adjacent conditions are not lost by extracting one bit.

#### Teaching redraw

```text
[Locate source: OBFFE]
          ↓
[Extract field: LTRME] → [Apply encoding: CTD]
                                      ↓
[Validate evidence: CTV]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `OBFFE` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `LTRME` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `CTD` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `CTV` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `PXCAP` | PCI Express Capability, the base of the PCIe capability structure. |
| `PXDC2` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.8.5.10 is the applicable context.
2. Decode OBFFE at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check LTRME as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 57 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.8.5.10 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes OBFFE, LTRME, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.8.5.10, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 57. Annotate the bytes containing OBFFE, decode them, and independently verify LTRME. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of OBFFE in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand OBFFE and state its unit or object scope?
2. Can the reader explain why LTRME is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** OBFFE, LTRME, CTD, CTV, PXCAP, PXDC2, SIG, OBFF

**Source keyword index:** `may`, `optional`, `reserved`

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.5.10, Figure 57, printed pages 30-31, PDF pages 30-31

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 58: Advanced Error Reporting Capability (Optional)</strong></summary>

<!-- claim:PCIE14-FIG-058-CLAIM figure-table:PCIE14-FIG-058 -->

**SPEC.** Figure 58, "Advanced Error Reporting Capability (Optional)": Defines the status/error classification represented by Advanced Error Reporting Capability (Optional). Resolve the category before the individual code or flag; keep reserved values uninterpreted. Evidence index: AERCAP, AERID, AER, ID, AERUCES, AERUCEM, AERUCESEV, AERCES.

#### Where this Figure fits

Figure 58 sits in §3.8.5.10 and acts as a status checkpoint. Read it after the report mental model has established the owning object and before software turns AERCAP into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a status or error classification. Identify the containing structure and category before decoding the individual code, control bits, and retry indication. Reserved values remain uninterpreted, and a similar name does not map the code into another error layer.

#### Teaching redraw

```text
[Locate source: AERCAP]
          ↓
[Extract field: AERID] → [Apply encoding: AER]
                                      ↓
[Validate evidence: ID]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `AERCAP` | Advanced Error Reporting Capability, the base of the AER extended-capability structure. |
| `AERID` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `AER` | Advanced Error Reporting, the PCIe capability for classifying, masking, and logging link or transaction errors. |
| `ID` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `AERUCES` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `AERUCEM` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.8.5.10 is the applicable context.
2. Decode AERCAP at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check AERID as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 58 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.8.5.10 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes AERCAP, AERID, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.8.5.10, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 58. Annotate the bytes containing AERCAP, decode them, and independently verify AERID. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of AERCAP in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand AERCAP and state its unit or object scope?
2. Can the reader explain why AERID is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** AERCAP, AERID, AER, ID, AERUCES, AERUCEM, AERUCESEV, AERCES

**Source keyword index:** `optional`

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.5.10, Figure 58, printed pages 31, PDF pages 31

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 59: Offset AERCAP: AERID - AER Capability ID</strong></summary>

<!-- claim:PCIE14-FIG-059-CLAIM figure-table:PCIE14-FIG-059 -->

**SPEC.** Figure 59, "Offset AERCAP: AERID - AER Capability ID": Defines AERID (AER Capability ID) at offset AERCAP and identifies the fields that software must decode at that location. Start at AERID, then map bit ranges to access type, reset value, and field meaning. Evidence index: NEXT, CVER, CID, AERCAP, AERID, AER, ID.

#### Where this Figure fits

Figure 59 sits in §3.8.6.1 and acts as a register checkpoint. Read it after the report mental model has established the owning object and before software turns NEXT into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a register or property field table. Locate the base offset, verify access width, reset value, and bit range, and only then convert bits into state or capability. Preserve the complete register snapshot so adjacent conditions are not lost by extracting one bit.

#### Teaching redraw

```text
[Locate source: NEXT]
          ↓
[Extract field: CVER] → [Apply encoding: CID]
                                      ↓
[Validate evidence: AERCAP]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `NEXT` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `CVER` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `CID` | Command Identifier, used with the SQ identifier to identify an outstanding command. |
| `AERCAP` | Advanced Error Reporting Capability, the base of the AER extended-capability structure. |
| `AERID` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `AER` | Advanced Error Reporting, the PCIe capability for classifying, masking, and logging link or transaction errors. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.8.6.1 is the applicable context.
2. Decode NEXT at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check CVER as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 59 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.8.6.1 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes NEXT, CVER, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.8.6.1, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 59. Annotate the bytes containing NEXT, decode them, and independently verify CVER. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of NEXT in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand NEXT and state its unit or object scope?
2. Can the reader explain why CVER is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** NEXT, CVER, CID, AERCAP, AERID, AER, ID

**Source keyword index:** `may`

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.6.1, Figure 59, printed pages 31, PDF pages 31

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 60: Offset AERCAP + 4: AERUCES - AER Uncorrectable Error Status Register</strong></summary>

<!-- claim:PCIE14-FIG-060-CLAIM figure-table:PCIE14-FIG-060 -->

**SPEC.** Figure 60, "Offset AERCAP + 4: AERUCES - AER Uncorrectable Error Status Register": Defines AERUCES (AER Uncorrectable Error Status Register) at offset AERCAP + 4 and identifies the fields that software must decode at that location. Start at AERUCES, then map bit ranges to access type, reset value, and field meaning. Evidence index: TPBES, AOEBS, MCBTS, UIES, ACSVS, ECRCES, ROS, CAS.

#### Where this Figure fits

Figure 60 sits in §3.8.6.2 and acts as a register checkpoint. Read it after the report mental model has established the owning object and before software turns TPBES into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a register or property field table. Locate the base offset, verify access width, reset value, and bit range, and only then convert bits into state or capability. Preserve the complete register snapshot so adjacent conditions are not lost by extracting one bit.

#### Teaching redraw

```text
[Locate source: TPBES]
          ↓
[Extract field: AOEBS] → [Apply encoding: MCBTS]
                                      ↓
[Validate evidence: UIES]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `TPBES` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `AOEBS` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `MCBTS` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `UIES` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `ACSVS` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `ECRCES` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.8.6.2 is the applicable context.
2. Decode TPBES at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check AOEBS as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 60 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.8.6.2 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes TPBES, AOEBS, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.8.6.2, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 60. Annotate the bytes containing TPBES, decode them, and independently verify AOEBS. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of TPBES in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand TPBES and state its unit or object scope?
2. Can the reader explain why AOEBS is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** TPBES, AOEBS, MCBTS, UIES, ACSVS, ECRCES, ROS, CAS

**Source keyword index:** `optional`, `reserved`

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.6.2, Figure 60, printed pages 31-32, PDF pages 31-32

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 61: Offset AERCAP + 8: AERUCEM - AER Uncorrectable Error Mask Register</strong></summary>

<!-- claim:PCIE14-FIG-061-CLAIM figure-table:PCIE14-FIG-061 -->

**SPEC.** Figure 61, "Offset AERCAP + 8: AERUCEM - AER Uncorrectable Error Mask Register": Defines AERUCEM (AER Uncorrectable Error Mask Register) at offset AERCAP + 8 and identifies the fields that software must decode at that location. Start at AERUCEM, then map bit ranges to access type, reset value, and field meaning. Evidence index: TPBEM, AOEBM, MCBTM, UIEM, ACSVM, ECRCEM, ROM, CAM.

#### Where this Figure fits

Figure 61 sits in §3.8.6.3 and acts as a register checkpoint. Read it after the report mental model has established the owning object and before software turns TPBEM into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a register or property field table. Locate the base offset, verify access width, reset value, and bit range, and only then convert bits into state or capability. Preserve the complete register snapshot so adjacent conditions are not lost by extracting one bit.

#### Teaching redraw

```text
[Locate source: TPBEM]
          ↓
[Extract field: AOEBM] → [Apply encoding: MCBTM]
                                      ↓
[Validate evidence: UIEM]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `TPBEM` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `AOEBM` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `MCBTM` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `UIEM` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `ACSVM` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `ECRCEM` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.8.6.3 is the applicable context.
2. Decode TPBEM at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check AOEBM as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 61 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.8.6.3 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes TPBEM, AOEBM, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.8.6.3, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 61. Annotate the bytes containing TPBEM, decode them, and independently verify AOEBM. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of TPBEM in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand TPBEM and state its unit or object scope?
2. Can the reader explain why AOEBM is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** TPBEM, AOEBM, MCBTM, UIEM, ACSVM, ECRCEM, ROM, CAM

**Source keyword index:** `optional`, `reserved`

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.6.3, Figure 61, printed pages 32, PDF pages 32

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 62: Offset AERCAP + Ch: AERUCESEV - AER Uncorrectable Error Severity Register</strong></summary>

<!-- claim:PCIE14-FIG-062-CLAIM figure-table:PCIE14-FIG-062 -->

**SPEC.** Figure 62, "Offset AERCAP + Ch: AERUCESEV - AER Uncorrectable Error Severity Register": Defines AERUCESEV (AER Uncorrectable Error Severity Register) at offset AERCAP + Ch and identifies the fields that software must decode at that location. Start at AERUCESEV, then map bit ranges to access type, reset value, and field meaning. Evidence index: TPBESEV, AOEBSEV, MCBTSEV, UIESEV, ACSVSEV, ECRCESEV, ROSEV, CASEV.

#### Where this Figure fits

Figure 62 sits in §3.8.6.4 and acts as a register checkpoint. Read it after the report mental model has established the owning object and before software turns TPBESEV into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a register or property field table. Locate the base offset, verify access width, reset value, and bit range, and only then convert bits into state or capability. Preserve the complete register snapshot so adjacent conditions are not lost by extracting one bit.

#### Teaching redraw

```text
[Locate source: TPBESEV]
          ↓
[Extract field: AOEBSEV] → [Apply encoding: MCBTSEV]
                                      ↓
[Validate evidence: UIESEV]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `TPBESEV` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `AOEBSEV` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `MCBTSEV` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `UIESEV` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `ACSVSEV` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `ECRCESEV` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.8.6.4 is the applicable context.
2. Decode TPBESEV at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check AOEBSEV as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 62 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.8.6.4 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes TPBESEV, AOEBSEV, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.8.6.4, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 62. Annotate the bytes containing TPBESEV, decode them, and independently verify AOEBSEV. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of TPBESEV in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand TPBESEV and state its unit or object scope?
2. Can the reader explain why AOEBSEV is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** TPBESEV, AOEBSEV, MCBTSEV, UIESEV, ACSVSEV, ECRCESEV, ROSEV, CASEV

**Source keyword index:** `optional`, `reserved`

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.6.4, Figure 62, printed pages 32-33, PDF pages 32-33

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 63: Offset AERCAP + 10h: AERCES - AER Correctable Error Status Register</strong></summary>

<!-- claim:PCIE14-FIG-063-CLAIM figure-table:PCIE14-FIG-063 -->

**SPEC.** Figure 63, "Offset AERCAP + 10h: AERCES - AER Correctable Error Status Register": Defines AERCES (AER Correctable Error Status Register) at offset AERCAP + 10h and identifies the fields that software must decode at that location. Start at AERCES, then map bit ranges to access type, reset value, and field meaning. Evidence index: HLOS, CIES, AERCAP, AERCES, AER, SIG, RWC, ANFES.

#### Where this Figure fits

Figure 63 sits in §3.8.6.5 and acts as a register checkpoint. Read it after the report mental model has established the owning object and before software turns HLOS into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a register or property field table. Locate the base offset, verify access width, reset value, and bit range, and only then convert bits into state or capability. Preserve the complete register snapshot so adjacent conditions are not lost by extracting one bit.

#### Teaching redraw

```text
[Locate source: HLOS]
          ↓
[Extract field: CIES] → [Apply encoding: AERCAP]
                                      ↓
[Validate evidence: AERCES]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `HLOS` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `CIES` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `AERCAP` | Advanced Error Reporting Capability, the base of the AER extended-capability structure. |
| `AERCES` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `AER` | Advanced Error Reporting, the PCIe capability for classifying, masking, and logging link or transaction errors. |
| `SIG` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.8.6.5 is the applicable context.
2. Decode HLOS at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check CIES as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 63 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.8.6.5 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes HLOS, CIES, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.8.6.5, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 63. Annotate the bytes containing HLOS, decode them, and independently verify CIES. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of HLOS in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand HLOS and state its unit or object scope?
2. Can the reader explain why CIES is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** HLOS, CIES, AERCAP, AERCES, AER, SIG, RWC, ANFES

**Source keyword index:** `optional`, `reserved`

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.6.5, Figure 63, printed pages 33, PDF pages 33

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 64: Offset AERCAP + 14h: AERCEM - AER Correctable Error Mask Register</strong></summary>

<!-- claim:PCIE14-FIG-064-CLAIM figure-table:PCIE14-FIG-064 -->

**SPEC.** Figure 64, "Offset AERCAP + 14h: AERCEM - AER Correctable Error Mask Register": Defines AERCEM (AER Correctable Error Mask Register) at offset AERCAP + 14h and identifies the fields that software must decode at that location. Start at AERCEM, then map bit ranges to access type, reset value, and field meaning. Evidence index: HLOM, CIEM, AERCAP, AERCEM, AER, SIG, ANFEM, RTM.

#### Where this Figure fits

Figure 64 sits in §3.8.6.6 and acts as a register checkpoint. Read it after the report mental model has established the owning object and before software turns HLOM into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a register or property field table. Locate the base offset, verify access width, reset value, and bit range, and only then convert bits into state or capability. Preserve the complete register snapshot so adjacent conditions are not lost by extracting one bit.

#### Teaching redraw

```text
[Locate source: HLOM]
          ↓
[Extract field: CIEM] → [Apply encoding: AERCAP]
                                      ↓
[Validate evidence: AERCEM]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `HLOM` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `CIEM` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `AERCAP` | Advanced Error Reporting Capability, the base of the AER extended-capability structure. |
| `AERCEM` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `AER` | Advanced Error Reporting, the PCIe capability for classifying, masking, and logging link or transaction errors. |
| `SIG` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.8.6.6 is the applicable context.
2. Decode HLOM at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check CIEM as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 64 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.8.6.6 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes HLOM, CIEM, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.8.6.6, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 64. Annotate the bytes containing HLOM, decode them, and independently verify CIEM. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of HLOM in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand HLOM and state its unit or object scope?
2. Can the reader explain why CIEM is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** HLOM, CIEM, AERCAP, AERCEM, AER, SIG, ANFEM, RTM

**Source keyword index:** `optional`, `reserved`

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.6.6, Figure 64, printed pages 33, PDF pages 33

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 65: Offset AERCAP + 18h: AERCC - AER Capabilities and Control Register</strong></summary>

<!-- claim:PCIE14-FIG-065-CLAIM figure-table:PCIE14-FIG-065 -->

**SPEC.** Figure 65, "Offset AERCAP + 18h: AERCC - AER Capabilities and Control Register": Defines AERCC (AER Capabilities and Control Register) at offset AERCAP + 18h and identifies the fields that software must decode at that location. Start at AERCC, then map bit ranges to access type, reset value, and field meaning. Evidence index: TPLP, MHRE, MHRC, ECE, ECC, EGE, EGC, FEP.

#### Where this Figure fits

Figure 65 sits in §3.8.6.7 and acts as a register checkpoint. Read it after the report mental model has established the owning object and before software turns TPLP into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a register or property field table. Locate the base offset, verify access width, reset value, and bit range, and only then convert bits into state or capability. Preserve the complete register snapshot so adjacent conditions are not lost by extracting one bit.

#### Teaching redraw

```text
[Locate source: TPLP]
          ↓
[Extract field: MHRE] → [Apply encoding: MHRC]
                                      ↓
[Validate evidence: ECE]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `TPLP` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `MHRE` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `MHRC` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `ECE` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `ECC` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `EGE` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.8.6.7 is the applicable context.
2. Decode TPLP at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check MHRE as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 65 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.8.6.7 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes TPLP, MHRE, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.8.6.7, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 65. Annotate the bytes containing TPLP, decode them, and independently verify MHRE. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of TPLP in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand TPLP and state its unit or object scope?
2. Can the reader explain why MHRE is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** TPLP, MHRE, MHRC, ECE, ECC, EGE, EGC, FEP

**Source keyword index:** `reserved`

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.6.7, Figure 65, printed pages 34, PDF pages 34

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 66: Offset AERCAP + 1Ch: AERHL - AER Header Log Register</strong></summary>

<!-- claim:PCIE14-FIG-066-CLAIM figure-table:PCIE14-FIG-066 -->

**SPEC.** Figure 66, "Offset AERCAP + 1Ch: AERHL - AER Header Log Register": Defines AERHL (AER Header Log Register) at offset AERCAP + 1Ch and identifies the fields that software must decode at that location. Start at AERHL, then map bit ranges to access type, reset value, and field meaning. Evidence index: AERCAP, AERHL, AER, HB3, HB2, HB1, HB0, HB7.

#### Where this Figure fits

Figure 66 sits in §3.8.6.8 and acts as a register checkpoint. Read it after the report mental model has established the owning object and before software turns AERCAP into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a register or property field table. Locate the base offset, verify access width, reset value, and bit range, and only then convert bits into state or capability. Preserve the complete register snapshot so adjacent conditions are not lost by extracting one bit.

#### Teaching redraw

```text
[Locate source: AERCAP]
          ↓
[Extract field: AERHL] → [Apply encoding: AER]
                                      ↓
[Validate evidence: HB3]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `AERCAP` | Advanced Error Reporting Capability, the base of the AER extended-capability structure. |
| `AERHL` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `AER` | Advanced Error Reporting, the PCIe capability for classifying, masking, and logging link or transaction errors. |
| `HB3` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `HB2` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `HB1` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.8.6.8 is the applicable context.
2. Decode AERCAP at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check AERHL as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 66 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.8.6.8 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes AERCAP, AERHL, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.8.6.8, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 66. Annotate the bytes containing AERCAP, decode them, and independently verify AERHL. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of AERCAP in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand AERCAP and state its unit or object scope?
2. Can the reader explain why AERHL is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** AERCAP, AERHL, AER, HB3, HB2, HB1, HB0, HB7

**Source keyword index:** none

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.6.8, Figure 66, printed pages 34, PDF pages 34

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 67: Offset AERCAP + 38h: AERTLP - AER TLP Prefix Log Register (Optional)</strong></summary>

<!-- claim:PCIE14-FIG-067-CLAIM figure-table:PCIE14-FIG-067 -->

**SPEC.** Figure 67, "Offset AERCAP + 38h: AERTLP - AER TLP Prefix Log Register (Optional)": Defines AERTLP (AER TLP Prefix Log Register (Optional)) at offset AERCAP + 38h and identifies the fields that software must decode at that location. Start at AERTLP, then map bit ranges to access type, reset value, and field meaning. Evidence index: AERCAP, AERTLP, AER, TLP, TPL1B3, TPL1B2, TPL1B1, TPL1B0.

#### Where this Figure fits

Figure 67 sits in §3.8.6.9 and acts as a register checkpoint. Read it after the report mental model has established the owning object and before software turns AERCAP into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a register or property field table. Locate the base offset, verify access width, reset value, and bit range, and only then convert bits into state or capability. Preserve the complete register snapshot so adjacent conditions are not lost by extracting one bit.

#### Teaching redraw

```text
[Locate source: AERCAP]
          ↓
[Extract field: AERTLP] → [Apply encoding: AER]
                                      ↓
[Validate evidence: TLP]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `AERCAP` | Advanced Error Reporting Capability, the base of the AER extended-capability structure. |
| `AERTLP` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `AER` | Advanced Error Reporting, the PCIe capability for classifying, masking, and logging link or transaction errors. |
| `TLP` | Transaction Layer Packet, a packet carried by the PCIe transaction layer. |
| `TPL1B3` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `TPL1B2` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.8.6.9 is the applicable context.
2. Decode AERCAP at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check AERTLP as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 67 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.8.6.9 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes AERCAP, AERTLP, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.8.6.9, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 67. Annotate the bytes containing AERCAP, decode them, and independently verify AERTLP. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of AERCAP in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand AERCAP and state its unit or object scope?
2. Can the reader explain why AERTLP is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** AERCAP, AERTLP, AER, TLP, TPL1B3, TPL1B2, TPL1B1, TPL1B0

**Source keyword index:** `shall`, `may`, `optional`

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.6.9, Figure 67, printed pages 35, PDF pages 35

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 68: Example of an Eve Diagram in the Printable Eye Field</strong></summary>

<!-- claim:PCIE14-FIG-068-CLAIM figure-table:PCIE14-FIG-068 -->

**SPEC.** Figure 68, "Example of an Eve Diagram in the Printable Eye Field": Defines the concrete layout or value relationships for Example of an Eve Diagram in the Printable Eye Field. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is TEE, VM, OS, TDISP, SR, IOV, SIOV, MI.

#### Where this Figure fits

Figure 68 sits in §3.8.9 and acts as a measurement checkpoint. Read it after the report mental model has established the owning object and before software turns TEE into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a measurement-data Figure. Confirm support, request selectors, and returned length before parsing headers, descriptors, units, and scale. Produce results only for complete lanes or entries actually returned.

#### Teaching redraw

```text
[Locate source: TEE]
          ↓
[Extract field: VM] → [Apply encoding: OS]
                                      ↓
[Validate evidence: TDISP]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `TEE` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `VM` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `OS` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `TDISP` | TEE Device Interface Security Protocol, a PCIe security protocol related to platform isolation and device-interface state. |
| `SR` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `IOV` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.8.9 is the applicable context.
2. Decode TEE at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check VM as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 68 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.8.9 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes TEE, VM, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.8.9, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 68. Annotate the bytes containing TEE, decode them, and independently verify VM. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of TEE in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand TEE and state its unit or object scope?
2. Can the reader explain why VM is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** TEE, VM, OS, TDISP, SR, IOV, SIOV, MI

**Source keyword index:** `shall`, `may`

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.9, Figure 68, printed pages 37, PDF pages 37

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 69: NVMe TDISP DEVICE_INTERFACE_REPORT Reporting Structure</strong></summary>

<!-- claim:PCIE14-FIG-069-CLAIM figure-table:PCIE14-FIG-069 -->

**SPEC.** Figure 69, "NVMe TDISP DEVICE_INTERFACE_REPORT Reporting Structure": Defines the concrete layout or value relationships for NVMe TDISP DEVICE_INTERFACE_REPORT Reporting Structure. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is TDISP.

#### Where this Figure fits

Figure 69 sits in §3.8.10 and acts as a layout checkpoint. Read it after the report mental model has established the owning object and before software turns TDISP into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a structure or capability field table. Locate it using the structure base and offset, read in byte/bit order, and separate capability gates, value encoding, and reserved areas. Presence in the table does not mean the function is supported.

#### Teaching redraw

```text
[Locate source: TDISP]
          ↓
[Extract field: evidence] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `TDISP` | TEE Device Interface Security Protocol, a PCIe security protocol related to platform isolation and device-interface state. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.8.10 is the applicable context.
2. Decode TDISP at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check the cited condition as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 69 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.8.10 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes TDISP, the cited condition, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.8.10, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 69. Annotate the bytes containing TDISP, decode them, and independently verify the cited condition. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of TDISP in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand TDISP and state its unit or object scope?
2. Can the reader explain why the cited condition is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** TDISP

**Source keyword index:** none

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.10, Figure 69, printed pages 38-39, PDF pages 38-39

</details>

<a id="section-3-9"></a>

### §3.9

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 70: Get Log Page - Log Page Identifiers</strong></summary>

<!-- claim:PCIE14-FIG-070-CLAIM figure-table:PCIE14-FIG-070 -->

**SPEC.** Figure 70, "Get Log Page - Log Page Identifiers": Defines the identifier composition or namespace of values shown by Get Log Page - Log Page Identifiers. Keep the value width, issuing authority, uniqueness scope, and reserved values separate. Evidence index: CSI1, CSI.

#### Where this Figure fits

Figure 70 sits in §3.9 and acts as a identifier checkpoint. Read it after the report mental model has established the owning object and before software turns CSI1 into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is an identifier-format Figure. Record width and encoding, then identify assignment authority, uniqueness scope, reserved values, and lifetime. Equal-width identifiers are not automatically interchangeable.

#### Teaching redraw

```text
[Locate source: CSI1]
          ↓
[Extract field: CSI] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `CSI1` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `CSI` | Command Set Identifier, selecting the I/O Command Set context for a command or log page. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.9 is the applicable context.
2. Decode CSI1 at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check CSI as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 70 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.9 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes CSI1, CSI, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.9, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 70. Annotate the bytes containing CSI1, decode them, and independently verify CSI. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of CSI1 in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand CSI1 and state its unit or object scope?
2. Can the reader explain why CSI is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** CSI1, CSI

**Source keyword index:** none

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.9, Figure 70, printed pages 39, PDF pages 39

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 71: Size of Physical Interface Receiver Eye Opening Measurement Log Page</strong></summary>

<!-- claim:PCIE14-FIG-071-CLAIM figure-table:PCIE14-FIG-071 -->

**SPEC.** Figure 71, "Size of Physical Interface Receiver Eye Opening Measurement Log Page": Shows the receiver-eye measurement information in Size of Physical Interface Receiver Eye Opening Measurement Log Page. Confirm support and returned length before interpreting lane, parameter, header, or descriptor data. Evidence index: Size of Physical Interface Receiver Eye Opening Measurement Log Page.

#### Where this Figure fits

Figure 71 sits in §3.9.1.1 and acts as a measurement checkpoint. Read it after the report mental model has established the owning object and before software turns Size of Physical Interface Receiver Eye Opening Measurement Log Page into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a measurement-data Figure. Confirm support, request selectors, and returned length before parsing headers, descriptors, units, and scale. Produce results only for complete lanes or entries actually returned.

#### Teaching redraw

```text
[Locate source: Size of Physical Interface Receiver Eye Opening Measurement Log Page]
          ↓
[Extract field: evidence] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `Size of Physical Interface Receiver Eye Opening Measurement Log Page` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.9.1.1 is the applicable context.
2. Decode Size of Physical Interface Receiver Eye Opening Measurement Log Page at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check the cited condition as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 71 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.9.1.1 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes Size of Physical Interface Receiver Eye Opening Measurement Log Page, the cited condition, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.9.1.1, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 71. Annotate the bytes containing Size of Physical Interface Receiver Eye Opening Measurement Log Page, decode them, and independently verify the cited condition. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of Size of Physical Interface Receiver Eye Opening Measurement Log Page in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand Size of Physical Interface Receiver Eye Opening Measurement Log Page and state its unit or object scope?
2. Can the reader explain why the cited condition is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** Size of Physical Interface Receiver Eye Opening Measurement Log Page

**Source keyword index:** none

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.9.1.1, Figure 71, printed pages 40, PDF pages 40

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 72: Physical Interface Receiver Eye Opening Measurement Log Specific Parameter Field</strong></summary>

<!-- claim:PCIE14-FIG-072-CLAIM figure-table:PCIE14-FIG-072 -->

**SPEC.** Figure 72, "Physical Interface Receiver Eye Opening Measurement Log Specific Parameter Field": Defines the concrete layout or value relationships for Physical Interface Receiver Eye Opening Measurement Log Specific Parameter Field. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is ACT, MQUAL, LPOU, LPOL, EOM, EOMIP.

#### Where this Figure fits

Figure 72 sits in §3.9.1.1 and acts as a measurement checkpoint. Read it after the report mental model has established the owning object and before software turns ACT into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a measurement-data Figure. Confirm support, request selectors, and returned length before parsing headers, descriptors, units, and scale. Produce results only for complete lanes or entries actually returned.

#### Teaching redraw

```text
[Locate source: ACT]
          ↓
[Extract field: MQUAL] → [Apply encoding: LPOU]
                                      ↓
[Validate evidence: LPOL]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `ACT` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `MQUAL` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `LPOU` | Log Page Offset Upper, the high 32 bits of the Get Log Page byte offset. |
| `LPOL` | Log Page Offset Lower, the low 32 bits of the Get Log Page byte offset. |
| `EOM` | Eye Opening Measurement, the procedure and log data for measuring a PCIe receiver eye opening. |
| `EOMIP` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.9.1.1 is the applicable context.
2. Decode ACT at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check MQUAL as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 72 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.9.1.1 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes ACT, MQUAL, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.9.1.1, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 72. Annotate the bytes containing ACT, decode them, and independently verify MQUAL. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of ACT in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand ACT and state its unit or object scope?
2. Can the reader explain why MQUAL is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** ACT, MQUAL, LPOU, LPOL, EOM, EOMIP

**Source keyword index:** `shall`, `may`, `reserved`

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.9.1.1, Figure 72, printed pages 40-41, PDF pages 40-41

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 73: Physical Interface Receiver Eye Opening Measurement Log Specific Identifier Field</strong></summary>

<!-- claim:PCIE14-FIG-073-CLAIM figure-table:PCIE14-FIG-073 -->

**SPEC.** Figure 73, "Physical Interface Receiver Eye Opening Measurement Log Specific Identifier Field": Defines the concrete layout or value relationships for Physical Interface Receiver Eye Opening Measurement Log Specific Identifier Field. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is TC, ID, EOM.

#### Where this Figure fits

Figure 73 sits in §3.9.1.1 and acts as a identifier checkpoint. Read it after the report mental model has established the owning object and before software turns TC into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is an identifier-format Figure. Record width and encoding, then identify assignment authority, uniqueness scope, reserved values, and lifetime. Equal-width identifiers are not automatically interchangeable.

#### Teaching redraw

```text
[Locate source: TC]
          ↓
[Extract field: ID] → [Apply encoding: EOM]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `TC` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `ID` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `EOM` | Eye Opening Measurement, the procedure and log data for measuring a PCIe receiver eye opening. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.9.1.1 is the applicable context.
2. Decode TC at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check ID as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 73 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.9.1.1 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes TC, ID, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.9.1.1, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 73. Annotate the bytes containing TC, decode them, and independently verify ID. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of TC in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand TC and state its unit or object scope?
2. Can the reader explain why ID is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** TC, ID, EOM

**Source keyword index:** `shall`

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.9.1.1, Figure 73, printed pages 41, PDF pages 41

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 74: Physical Interface Receiver Eye Opening Measurement Log Page</strong></summary>

<!-- claim:PCIE14-FIG-074-CLAIM figure-table:PCIE14-FIG-074 -->

**SPEC.** Figure 74, "Physical Interface Receiver Eye Opening Measurement Log Page": Shows the receiver-eye measurement information in Physical Interface Receiver Eye Opening Measurement Log Page. Confirm support and returned length before interpreting lane, parameter, header, or descriptor data. Evidence index: Physical Interface Receiver Eye Opening Measurement Log Page.

#### Where this Figure fits

Figure 74 sits in §3.9.1.1 and acts as a measurement checkpoint. Read it after the report mental model has established the owning object and before software turns Physical Interface Receiver Eye Opening Measurement Log Page into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a measurement-data Figure. Confirm support, request selectors, and returned length before parsing headers, descriptors, units, and scale. Produce results only for complete lanes or entries actually returned.

#### Teaching redraw

```text
[Locate source: Physical Interface Receiver Eye Opening Measurement Log Page]
          ↓
[Extract field: evidence] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `Physical Interface Receiver Eye Opening Measurement Log Page` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.9.1.1 is the applicable context.
2. Decode Physical Interface Receiver Eye Opening Measurement Log Page at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check the cited condition as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 74 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.9.1.1 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes Physical Interface Receiver Eye Opening Measurement Log Page, the cited condition, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.9.1.1, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 74. Annotate the bytes containing Physical Interface Receiver Eye Opening Measurement Log Page, decode them, and independently verify the cited condition. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of Physical Interface Receiver Eye Opening Measurement Log Page in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand Physical Interface Receiver Eye Opening Measurement Log Page and state its unit or object scope?
2. Can the reader explain why the cited condition is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** Physical Interface Receiver Eye Opening Measurement Log Page

**Source keyword index:** none

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.9.1.1, Figure 74, printed pages 41, PDF pages 41

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 75: EOM Header</strong></summary>

<!-- claim:PCIE14-FIG-075-CLAIM figure-table:PCIE14-FIG-075 -->

**SPEC.** Figure 75, "EOM Header": Shows the receiver-eye measurement information in EOM Header. Confirm support and returned length before interpreting lane, parameter, header, or descriptor data. Evidence index: EOM.

#### Where this Figure fits

Figure 75 sits in §3.9.1.1 and acts as a measurement checkpoint. Read it after the report mental model has established the owning object and before software turns EOM into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a measurement-data Figure. Confirm support, request selectors, and returned length before parsing headers, descriptors, units, and scale. Produce results only for complete lanes or entries actually returned.

#### Teaching redraw

```text
[Locate source: EOM]
          ↓
[Extract field: evidence] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `EOM` | Eye Opening Measurement, the procedure and log data for measuring a PCIe receiver eye opening. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.9.1.1 is the applicable context.
2. Decode EOM at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check the cited condition as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 75 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.9.1.1 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes EOM, the cited condition, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.9.1.1, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 75. Annotate the bytes containing EOM, decode them, and independently verify the cited condition. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of EOM in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand EOM and state its unit or object scope?
2. Can the reader explain why the cited condition is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** EOM

**Source keyword index:** none

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.9.1.1, Figure 75, printed pages 42-43, PDF pages 42-43

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 76: EOM Lane Descriptor</strong></summary>

<!-- claim:PCIE14-FIG-076-CLAIM figure-table:PCIE14-FIG-076 -->

**SPEC.** Figure 76, "EOM Lane Descriptor": Defines the concrete layout or value relationships for EOM Lane Descriptor. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is MSTAT, MSCS, LN, EYE, TOP, BTM, LFT, RGT.

#### Where this Figure fits

Figure 76 sits in §3.9.1.1 and acts as a measurement checkpoint. Read it after the report mental model has established the owning object and before software turns MSTAT into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a measurement-data Figure. Confirm support, request selectors, and returned length before parsing headers, descriptors, units, and scale. Produce results only for complete lanes or entries actually returned.

#### Teaching redraw

```text
[Locate source: MSTAT]
          ↓
[Extract field: MSCS] → [Apply encoding: LN]
                                      ↓
[Validate evidence: EYE]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `MSTAT` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `MSCS` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `LN` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `EYE` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `TOP` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `BTM` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.9.1.1 is the applicable context.
2. Decode MSTAT at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check MSCS as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 76 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.9.1.1 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes MSTAT, MSCS, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.9.1.1, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 76. Annotate the bytes containing MSTAT, decode them, and independently verify MSCS. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of MSTAT in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand MSTAT and state its unit or object scope?
2. Can the reader explain why MSCS is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** MSTAT, MSCS, LN, EYE, TOP, BTM, LFT, RGT

**Source keyword index:** `shall`, `may`, `reserved`

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.9.1.1, Figure 76, printed pages 43-45, PDF pages 43-45

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 77: Example of an Eve Diagram in the Printable Eye Field</strong></summary>

<!-- claim:PCIE14-FIG-077-CLAIM figure-table:PCIE14-FIG-077 -->

**SPEC.** Figure 77, "Example of an Eve Diagram in the Printable Eye Field": Defines the concrete layout or value relationships for Example of an Eve Diagram in the Printable Eye Field. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is Example of an Eve Diagram in the Printable Eye Field.

#### Where this Figure fits

Figure 77 sits in §3.9.1.1 and acts as a measurement checkpoint. Read it after the report mental model has established the owning object and before software turns Example of an Eve Diagram in the Printable Eye Field into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a measurement-data Figure. Confirm support, request selectors, and returned length before parsing headers, descriptors, units, and scale. Produce results only for complete lanes or entries actually returned.

#### Teaching redraw

```text
[Locate source: Example of an Eve Diagram in the Printable Eye Field]
          ↓
[Extract field: evidence] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `Example of an Eve Diagram in the Printable Eye Field` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.9.1.1 is the applicable context.
2. Decode Example of an Eve Diagram in the Printable Eye Field at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check the cited condition as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 77 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.9.1.1 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes Example of an Eve Diagram in the Printable Eye Field, the cited condition, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.9.1.1, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 77. Annotate the bytes containing Example of an Eve Diagram in the Printable Eye Field, decode them, and independently verify the cited condition. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of Example of an Eve Diagram in the Printable Eye Field in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand Example of an Eve Diagram in the Printable Eye Field and state its unit or object scope?
2. Can the reader explain why the cited condition is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** Example of an Eve Diagram in the Printable Eye Field

**Source keyword index:** none

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.9.1.1, Figure 77, printed pages 46, PDF pages 46

</details>

## Use and limitations

Use the claim IDs as stable PPT traceability keys. Re-check affected claims if the source revision, errata set, or approved scope changes.

## Self-questions and worked answers

24 answered questions revisit this report's scope. Each answer retains the same source links as the teaching module; calculations and debugging examples are informative.

### Q01. What is the governing interpretation for “Base defines NVMe; the PCIe Transport defines how it is realized on PCIe”?

<!-- qa:pcie-transport-1.4-layers-lead -->

**Answer.**

Figure 1 shows document applicability and Figure 2 separates protocol responsibility. Engineering analysis separates command semantics from the way host memory, MMIO, configuration space, and interrupts carry the operation. The Transport does not rewrite Base when the two conflict.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §1.2, printed pages 6, PDF pages 6; Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §1.3, printed pages 6-7, PDF pages 6-7; Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §2, printed pages 8, PDF pages 8

### Q02. Which concepts or conditions must be distinguished in “Base defines NVMe; the PCIe Transport defines how it is realized on PCIe”?

<!-- qa:pcie-transport-1.4-layers-rows -->

**Answer.**

- Base — Common command and completion semantics — Highest-precedence NVMe definition
- PCIe Transport — Address, register, doorbell, and interrupt binding — Adds PCIe-specific requirements
- PCI-SIG specifications — Native PCIe capability and transaction semantics — This report covers only NVMe-specific statements present in the supplied source

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §1.2, printed pages 6, PDF pages 6; Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §1.3, printed pages 6-7, PDF pages 6-7; Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §2, printed pages 8, PDF pages 8

### Q03. How does “Base defines NVMe; the PCIe Transport defines how it is realized on PCIe” apply to a concrete calculation or operational scenario?

<!-- qa:pcie-transport-1.4-layers-example -->

**Answer.**

Informative example: Base defines Firmware Commit CA/FS and status codes. The PCIe Transport adds where the SQE resides in host memory, where the doorbell resides in BAR0/1 memory space, and how a completion can trigger MSI-X.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §1.2, printed pages 6, PDF pages 6; Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §1.3, printed pages 6-7, PDF pages 6-7; Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §2, printed pages 8, PDF pages 8

### Q04. What misinterpretation is most likely in “Base defines NVMe; the PCIe Transport defines how it is realized on PCIe”, and how is it debugged?

<!-- qa:pcie-transport-1.4-layers-pitfall -->

**Answer.**

Label the owning specification beside every field in a design document. A defect report that merges command status, PCIe AER, and device-register access into one 'NVMe error' usually chooses the wrong recovery layer as well.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §1.2, printed pages 6, PDF pages 6; Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §1.3, printed pages 6-7, PDF pages 6-7; Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §2, printed pages 8, PDF pages 8

### Q05. What is the governing interpretation for “From BAR to doorbell offset: preserve units at every step”?

<!-- qa:pcie-transport-1.4-mmio-doorbell-lead -->

**Answer.**

NVMe controller registers reside in the memory space designated by BAR0/BAR1. Doorbells begin at 1000h; SQ-tail and CQ-head registers for queue y are spaced using CAP.DSTRD. Figures 3-6 form one address derivation rather than four independent register tables.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.1, printed pages 9-10, PDF pages 9-10; Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.1.2.1-3.1.2.2, printed pages 10-11, PDF pages 10-11

### Q06. Which concepts or conditions must be distinguished in “From BAR to doorbell offset: preserve units at every step”?

<!-- qa:pcie-transport-1.4-mmio-doorbell-rows -->

**Answer.**

- SQ y tail — 1000h + (2y) x (4 << DSTRD) — Host publishes a new SQ tail
- CQ y head — 1000h + (2y+1) x (4 << DSTRD) — Host publishes a consumed CQ head
- Doorbell value — Queue pointer — Does not contain the SQE or CQE body

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.1, printed pages 9-10, PDF pages 9-10; Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.1.2.1-3.1.2.2, printed pages 10-11, PDF pages 10-11

### Q07. How does “From BAR to doorbell offset: preserve units at every step” apply to a concrete calculation or operational scenario?

<!-- qa:pcie-transport-1.4-mmio-doorbell-example -->

**Answer.**

Informative example: with DSTRD=1, stride=4<<1=8 bytes. SQ-tail offset for queue 3 is 1000h+(6x8)=1030h; CQ-head offset is 1000h+(7x8)=1038h. They differ by one stride. Treating DSTRD itself as a byte count makes every nonzero-DSTRD doorbell address wrong.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.1, printed pages 9-10, PDF pages 9-10; Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.1.2.1-3.1.2.2, printed pages 10-11, PDF pages 10-11

### Q08. What misinterpretation is most likely in “From BAR to doorbell offset: preserve units at every step”, and how is it debugged?

<!-- qa:pcie-transport-1.4-mmio-doorbell-pitfall -->

**Answer.**

A doorbell trace retains BAR base, DSTRD, queue ID, formula intermediates, final physical address, written pointer, and access width. Logging only the final virtual address cannot distinguish BAR mapping, stride, or queue-index defects.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.1, printed pages 9-10, PDF pages 9-10; Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.1.2.1-3.1.2.2, printed pages 10-11, PDF pages 10-11

### Q09. What is the governing interpretation for “The eight Figure 8 command-processing steps are ownership handoffs”?

<!-- qa:pcie-transport-1.4-command-lead -->

**Answer.**

SQE creation, doorbell write, controller fetch, CQE posting, interrupt delivery, and CQ-head update are not names for one event; they are successive ownership handoffs between host and controller. Their order governs both memory ordering and resource reuse.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.4, printed pages 12-13, PDF pages 12-13; Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.2, printed pages 11, PDF pages 11

### Q10. Which concepts or conditions must be distinguished in “The eight Figure 8 command-processing steps are ownership handoffs”?

<!-- qa:pcie-transport-1.4-command-rows -->

**Answer.**

- SQ-slot reuse — Controller has consumed the SQE — Completion SQHD assists tracking
- Command-buffer reuse — Command completed and data is visible — Check command and data direction
- CQ-slot release — Host completely consumed the CQE — Then write the CQ-head doorbell

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.4, printed pages 12-13, PDF pages 12-13; Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.2, printed pages 11, PDF pages 11

### Q11. How does “The eight Figure 8 command-processing steps are ownership handoffs” apply to a concrete calculation or operational scenario?

<!-- qa:pcie-transport-1.4-command-example -->

**Answer.**

Informative example: if the host rings the doorbell before writing the final SQE dword, the controller may fetch a partial command. In the other direction, updating CQ head before fully reading the CQE can let the controller reuse that CQ slot. Both are ownership-ordering failures, not opcode failures.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.4, printed pages 12-13, PDF pages 12-13; Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.2, printed pages 11, PDF pages 11

### Q12. What misinterpretation is most likely in “The eight Figure 8 command-processing steps are ownership handoffs”, and how is it debugged?

<!-- qa:pcie-transport-1.4-command-pitfall -->

**Answer.**

A timeline records CPU core, SQ tail, doorbell MMIO, SQHD, CQ phase, interrupt vector, and CQ head. Events from separate logs are aligned by CID/SQID and timestamp to isolate lost interrupts, stale phase, or memory-ordering defects.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.4, printed pages 12-13, PDF pages 12-13; Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.2, printed pages 11, PDF pages 11

### Q13. What is the governing interpretation for “Interrupt-mode comparison: vector count, masking, and latency are separate dimensions”?

<!-- qa:pcie-transport-1.4-interrupts-lead -->

**Answer.**

Pin-based, single-message MSI, multiple-message MSI, and MSI-X differ in more than performance. They provide different vector counts, masking locations, and capability structures; interrupt coalescing separately controls when multiple completions produce a notification. Figure 9 and Figures 34-46 belong with queue-to-vector mapping.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.5, printed pages 13-16, PDF pages 13-16; Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.2, printed pages 11, PDF pages 11; Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §Annex A, printed pages 47-48, PDF pages 47-48

### Q14. Which concepts or conditions must be distinguished in “Interrupt-mode comparison: vector count, masking, and latency are separate dimensions”?

<!-- qa:pcie-transport-1.4-interrupts-rows -->

**Answer.**

- Pin-based — Legacy shared signaling — Sharing and masking differ
- Single MSI — One message/vector — Multiple CQs may share a service path
- Multiple MSI — A set of contiguous messages — Constrained by MME/MMC capability
- MSI-X — Table-based vectors with independent masks — Preferred by the specification

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.5, printed pages 13-16, PDF pages 13-16; Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.2, printed pages 11, PDF pages 11; Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §Annex A, printed pages 47-48, PDF pages 47-48

### Q15. How does “Interrupt-mode comparison: vector count, masking, and latency are separate dimensions” apply to a concrete calculation or operational scenario?

<!-- qa:pcie-transport-1.4-interrupts-example -->

**Answer.**

Informative example: CQ 1 and CQ 2 share vector 5. When vector 5 arrives, the handler cannot inspect only CQ 1; it services every relevant CQ mapped to the vector. Raising the coalescing threshold can reduce interrupt rate while increasing CQE wait time.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.5, printed pages 13-16, PDF pages 13-16; Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.2, printed pages 11, PDF pages 11; Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §Annex A, printed pages 47-48, PDF pages 47-48

### Q16. What misinterpretation is most likely in “Interrupt-mode comparison: vector count, masking, and latency are separate dimensions”, and how is it debugged?

<!-- qa:pcie-transport-1.4-interrupts-pitfall -->

**Answer.**

Interrupt debugging separates capability enable, CQ IV, MSI/MSI-X mask, pending state, controller CQE, and host handler. 'ISR did not run' cannot distinguish no generation, failed PCIe delivery, a masked vector, or a handler that skipped a CQ.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.5, printed pages 13-16, PDF pages 13-16; Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.2, printed pages 11, PDF pages 11; Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §Annex A, printed pages 47-48, PDF pages 47-48

### Q17. What is the governing interpretation for “Configuration space is a capability map; AER is a transport-error map”?

<!-- qa:pcie-transport-1.4-config-error-lead -->

**Answer.**

Figures 10-67 traverse the Type 0 header, Power Management, MSI/MSI-X, PCIe capability, and AER. Locate the capability or extended-capability base before applying offsets. AER status, mask, severity, and header log form one diagnostic set rather than isolated error bits.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1-3.8.7, printed pages 16-35, PDF pages 16-35; Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.7, printed pages 16, PDF pages 16; Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.6, printed pages 16, PDF pages 16

### Q18. Which concepts or conditions must be distinguished in “Configuration space is a capability map; AER is a transport-error map”?

<!-- qa:pcie-transport-1.4-config-error-rows -->

**Answer.**

- NVMe CQE status — Command execution result — Decode in NVMe command context
- PCIe Device Status — PCIe Function status summary — Located in PCIe capability
- AER — Correctable/uncorrectable transport errors — Read status, mask, severity, and header together
- Power state — Slot limit and device power control — Never choose an NVMe state above the slot power limit

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1-3.8.7, printed pages 16-35, PDF pages 16-35; Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.7, printed pages 16, PDF pages 16; Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.6, printed pages 16, PDF pages 16

### Q19. How does “Configuration space is a capability map; AER is a transport-error map” apply to a concrete calculation or operational scenario?

<!-- qa:pcie-transport-1.4-config-error-example -->

**Answer.**

Informative example: when an AERUCES bit is set, first check its mask to determine reporting, then its severity for handling, and finally the header log for transaction context. The bit cannot be translated directly into an NVMe SC.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1-3.8.7, printed pages 16-35, PDF pages 16-35; Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.7, printed pages 16, PDF pages 16; Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.6, printed pages 16, PDF pages 16

### Q20. What misinterpretation is most likely in “Configuration space is a capability map; AER is a transport-error map”, and how is it debugged?

<!-- qa:pcie-transport-1.4-config-error-pitfall -->

**Answer.**

A configuration dump retains the capability base as well as register values. The same relative offset under a different capability base denotes a different field. Capture the complete AER set before clearing any RW1C status.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1-3.8.7, printed pages 16-35, PDF pages 16-35; Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.7, printed pages 16, PDF pages 16; Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.6, printed pages 16, PDF pages 16

### Q21. What is the governing interpretation for “EOM parser: size first, header second, lane descriptors third”?

<!-- qa:pcie-transport-1.4-eom-lead -->

**Answer.**

The Physical Interface Receiver Eye Opening Measurement log page is variable length. The host confirms support and required size before parsing specific parameters/identifiers, the header, lane descriptors, and measurement data. Figures 70-77 form a parser pipeline rather than independent field translations.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.9, printed pages 39-46, PDF pages 39-46; Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §Annex A, printed pages 47-48, PDF pages 47-48

### Q22. Which concepts or conditions must be distinguished in “EOM parser: size first, header second, lane descriptors third”?

<!-- qa:pcie-transport-1.4-eom-rows -->

**Answer.**

- Specific parameter — Selects measurement action and quality/state — Establish request context first
- Specific identifier — Selects lane/test context — Prevents mixing different measurements
- Header — Global length and layout — Base for every later offset
- Lane descriptor — Per-lane boundaries and status — Walk only within returned buffer

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.9, printed pages 39-46, PDF pages 39-46; Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §Annex A, printed pages 47-48, PDF pages 47-48

### Q23. How does “EOM parser: size first, header second, lane descriptors third” apply to a concrete calculation or operational scenario?

<!-- qa:pcie-transport-1.4-eom-example -->

**Answer.**

Informative example: the header claims eight lane descriptors while the returned buffer can contain only six complete descriptors. The parser reports a truncated structure and stops; it must not read beyond the buffer because the platform was expected to have eight lanes.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.9, printed pages 39-46, PDF pages 39-46; Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §Annex A, printed pages 47-48, PDF pages 47-48

### Q24. What misinterpretation is most likely in “EOM parser: size first, header second, lane descriptors third”, and how is it debugged?

<!-- qa:pcie-transport-1.4-eom-pitfall -->

**Answer.**

Retain request parameter, identifier, returned byte count, header-declared size, lane number, and measurement status. A final eye plot alone cannot reproduce selector, length, or lane-mapping defects.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.9, printed pages 39-46, PDF pages 39-46; Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §Annex A, printed pages 47-48, PDF pages 47-48
