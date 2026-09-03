---
layout: post
read_time: true
show_date: true
title: "NVMe Base 2.4 Chapter 3: Controllers, Queues, Initialization, and Resets"
date: 2026-08-28
description: "Source-located PCIe/NVMe report for PPT authoring."
lang: en
img: posts/2026/cat_title.jpg
tags: [NVMe, PCIe, Specification]
category: NVMe
author: Jia-Chang
github: JiaChangGit/JiaChangGit.github.io/tree/main/DOCS/nvme-spec-report
toc: yes
---
[繁體中文]({% post_url 2026-08-28-nvme-base-ch3-zh-tw %})


# NVMe Base 2.4 Chapter 3: Controllers, Queues, Initialization, and Resets

Purpose: a source-located engineering report for GitHub Pages and a 100-minute presentation.

Scope: §3; printed pages 38-138; PDF pages 64-164. Only PCIe/memory-based and common NVMe content appears below.

## Source versions

NVM Express Base Specification, Revision 2.4

Verification date: 2026-08-29. No additional errata, ECNs, Technical Proposals, controller-vendor documents, or source text from the external PCI Express Base Specification are included.

## Reading map

```text
Properties / CAP -> CC.EN = 1 -> CSTS.RDY = 1 -> Queues active
```

The host reads capabilities and configures Admin queues before enabling the controller; normal queue processing starts only after CSTS.RDY reports ready.

## Normative language

shall is mandatory, may permits a choice, should expresses a preferred recommendation, and optional means support is not required. The report preserves these terms and never promotes one into another.

## Acronyms first: complete glossary

Every abbreviation below is introduced before it is used in the slide narrative. The term alone is never enough: retain owner, width, unit, scope, and state.

| Acronym / term | Plain-language meaning | Source |
|---|---|---|
| `controller` | Controller, the entity that implements the NVMe interface, fetches commands, and reports completions. | NVME-BASE-2.4 Rev. 2.4, §3.1.3-3.1.3.2, printed pp. 39-43, PDF pp. 65-69 |
| `I/O controller` | I/O controller, a controller type capable of executing user-data I/O commands. | NVME-BASE-2.4 Rev. 2.4, §3.1.3-3.1.3.2, printed pp. 39-43, PDF pp. 65-69 |
| `Administrative controller` | Administrative controller, a management-oriented controller type that does not execute user-data I/O commands. | NVME-BASE-2.4 Rev. 2.4, §3.1.3-3.1.3.2, printed pp. 39-43, PDF pp. 65-69 |
| `CAP` | Controller Capabilities, the controller property at offset 00h that reports queue, page-size, timeout, and other capabilities. | NVME-BASE-2.4 Rev. 2.4, §3.5.1, 3.5.3-3.5.4, printed pp. 105-113, PDF pp. 131-139 |
| `CC` | Controller Configuration, the property through which the host selects settings and enables or disables a controller. | NVME-BASE-2.4 Rev. 2.4, §3.5.1, 3.5.3-3.5.4, printed pp. 105-113, PDF pp. 131-139 |
| `CSTS` | Controller Status, the property through which a controller reports ready, fatal-status, and shutdown state. | NVME-BASE-2.4 Rev. 2.4, §3.5.1, 3.5.3-3.5.4, printed pp. 105-113, PDF pp. 131-139 |
| `EN` | Enable, the CC bit controlling controller enable state. | NVME-BASE-2.4 Rev. 2.4, §3.5.1, 3.5.3-3.5.4, printed pp. 105-113, PDF pp. 131-139 |
| `RDY` | Ready, the CSTS bit indicating whether the controller is ready for normal command processing. | NVME-BASE-2.4 Rev. 2.4, §3.5.1, 3.5.3-3.5.4, printed pp. 105-113, PDF pp. 131-139 |
| `AQA` | Admin Queue Attributes, the property describing Admin SQ and Admin CQ sizes. | NVME-BASE-2.4 Rev. 2.4, §3.5.1, 3.5.3-3.5.4, printed pp. 105-113, PDF pp. 131-139 |
| `ASQ` | Admin Submission Queue Base Address, the base address of the Admin SQ in addressable memory. | NVME-BASE-2.4 Rev. 2.4, §3.5.1, 3.5.3-3.5.4, printed pp. 105-113, PDF pp. 131-139 |
| `ACQ` | Admin Completion Queue Base Address, the base address of the Admin CQ in addressable memory. | NVME-BASE-2.4 Rev. 2.4, §3.5.1, 3.5.3-3.5.4, printed pp. 105-113, PDF pp. 131-139 |
| `NSID` | Namespace Identifier, a controller-visible numeric handle for a namespace; the identifier is not the namespace object itself. | NVME-BASE-2.4 Rev. 2.4, §3.2.1, printed pp. 78-80, PDF pp. 104-106 |
| `NSSR` | NVM Subsystem Reset, the property used to initiate an NVM subsystem reset. | NVME-BASE-2.4 Rev. 2.4, §3.7, printed pp. 120-125, PDF pp. 146-151 |
| `NSSD` | NVM Subsystem Shutdown, the property controlling the wider-scope subsystem shutdown. | NVME-BASE-2.4 Rev. 2.4, §3.6.1, 3.6.3, printed pp. 113-120, PDF pp. 139-146 |
| `SHN` | Shutdown Notification, the CC field through which the host declares a shutdown type. | NVME-BASE-2.4 Rev. 2.4, §3.6.1, 3.6.3, printed pp. 113-120, PDF pp. 139-146 |
| `SHST` | Shutdown Status, the CSTS field through which the controller reports shutdown progress. | NVME-BASE-2.4 Rev. 2.4, §3.6.1, 3.6.3, printed pp. 113-120, PDF pp. 139-146 |
| `CRTO` | Controller Ready Timeouts, the property reporting wait times for specific ready modes. | NVME-BASE-2.4 Rev. 2.4, §3.5.1, 3.5.3-3.5.4, printed pp. 105-113, PDF pp. 131-139 |
| `CMB` | Controller Memory Buffer, controller-provided memory in which selected queues or data structures may reside. | NVME-BASE-2.4 Rev. 2.4, §3.1.4, printed pp. 52-54, PDF pp. 78-80 |
| `PMR` | Persistent Memory Region, a controller-exposed memory region with persistence semantics. | NVME-BASE-2.4 Rev. 2.4, §3.1.4, printed pp. 52-54, PDF pp. 78-80 |
| `BIR` | BAR Indicator Register, a selector identifying the PCIe BAR that contains a memory structure. | NVME-BASE-2.4 Rev. 2.4, §3.1.4, printed pp. 52-54, PDF pp. 78-80 |
| `MPS` | Memory Page Size, the controller memory-page-size setting; it affects queue addresses and PRP alignment. | NVME-BASE-2.4 Rev. 2.4, §3.3.1, printed pp. 88-91, PDF pp. 114-117 |
| `KATO` | Keep Alive Timeout, the negotiated liveness timeout between host and controller. | NVME-BASE-2.4 Rev. 2.4, §3.9, printed pp. 129-135, PDF pp. 155-161 |
| `KATT` | Keep Alive Timeout Total, the controller timing basis for detecting a keep-alive timeout. | NVME-BASE-2.4 Rev. 2.4, §3.9, printed pp. 129-135, PDF pp. 155-161 |
| `FDP` | Flexible Data Placement, a capability connecting data-placement hints with media-reclamation management. | NVME-BASE-2.4 Rev. 2.4, §3.2.2-3.2.4, printed pp. 80-85, PDF pp. 106-111 |
| `NVM Set` | NVM Set, a capacity grouping that associates namespaces with a managed set of NVM resources. | NVME-BASE-2.4 Rev. 2.4, §3.2.2-3.2.4, printed pp. 80-85, PDF pp. 106-111 |
| `Endurance Group` | Endurance Group, a group of NVM resources for isolating and reporting endurance-related state. | NVME-BASE-2.4 Rev. 2.4, §3.2.2-3.2.4, printed pp. 80-85, PDF pp. 106-111 |
| `Reclaim Group` | Reclaim Group, a set of non-volatile storage resources with shared reclamation behavior. | NVME-BASE-2.4 Rev. 2.4, §3.2.2-3.2.4, printed pp. 80-85, PDF pp. 106-111 |
| `Reclaim Unit` | Reclaim Unit, a smaller management granularity used when a controller reclaims media. | NVME-BASE-2.4 Rev. 2.4, §3.2.2-3.2.4, printed pp. 80-85, PDF pp. 106-111 |
| `NVM subsystem` | NVM subsystem, the NVMe system boundary containing controllers, ports, namespaces, and non-volatile storage resources. | NVME-BASE-2.4 Rev. 2.4, §3.2.5, printed pp. 85-88, PDF pp. 111-114 |

## Visual atlas: locate the system before reading fields

Each redraw answers a different question: architecture locates components, sequence shows ownership, decode turns bits into engineering values, and state views preserve failure evidence. These are teaching redraws, not copies of specification artwork.

### Visual 01: Separate controller type, identity, and capability first

**View type:** `architecture`

```text
[Identify controller type]
  ├─ [Obtain Controller ID]
  ├─ [Resolve command/log/feature suppo…]
  └─ [Build the allowed operation set]
```

**Question answered:** Controller type answers what work a controller can perform, Controller ID answers which controller it is, and support-requirement Figures answer the required support level of a command, log, or feature in a particular context. Figures 23-32 belong in one reading sequence, but the three questions cannot be collapsed into one Boolean.

**Supporting Figures:** Figure 23, Figure 24, Figure 25, Figure 26, Figure 27, Figure 28, Figure 30, Figure 31, Figure 32

**Sources:** NVME-BASE-2.4 Rev. 2.4, §3.1.1, printed pp. 38, PDF pp. 64; NVME-BASE-2.4 Rev. 2.4, §3.1.3-3.1.3.2, printed pp. 39-43, PDF pp. 65-69; NVME-BASE-2.4 Rev. 2.4, §3.1.3, printed pp. 40, PDF pp. 66

### Visual 02: From CAP to CSTS.RDY: initialization is a state machine with preconditions

**View type:** `state`

```text
[Read CAP/VS] → [Configure AQA, ASQ, ACQ] → [Select CC fields] → [Write CC.EN=1] → [Wait for CSTS.RDY=1 or timeout]
timeout / failure ──→ preserve trigger + previous state + evidence
```

**Question answered:** Properties are not an independent register list. CAP constrains page-size, queue, and timeout capabilities; AQA, ASQ, and ACQ establish Admin queues; CC selects settings and enables the controller; CSTS.RDY finally declares readiness for normal command processing. Figures 33-46 and Figure 57 should be read along this causal chain.

**Supporting Figures:** Figure 33, Figure 34, Figure 36, Figure 37, Figure 38, Figure 41, Figure 42, Figure 44, Figure 45, Figure 46, Figure 57

**Sources:** NVME-BASE-2.4 Rev. 2.4, §3.1.4, printed pp. 52-54, PDF pp. 78-80; NVME-BASE-2.4 Rev. 2.4, §3.5.1, 3.5.3-3.5.4, printed pp. 105-113, PDF pp. 131-139

### Visual 03: Separate ring-buffer state, doorbells, and arbitration

**View type:** `sequence`

```text
Host / software        Shared object        Controller / evidence
Host → Shared: Host writes SQE
Shared → Controller: Host advances tail
Controller → Shared: Arbiter selects SQ
Shared → Host: Controller advances SQ head
Host → Shared: Controller posts CQE
Shared → Controller: Host advances CQ head
```

**Question answered:** Figures 73 and 74 define empty/full state for a queue, while Figures 80 and 81 define arbitration among SQs competing for controller service. The first problem concerns head/tail state within one ring; the second selects among candidate SQs. Priority belongs to the SQ, not to each command as an independent priority.

**Supporting Figures:** Figure 73, Figure 74, Figure 80, Figure 81

**Sources:** NVME-BASE-2.4 Rev. 2.4, §3.3.1, printed pp. 88-91, PDF pp. 114-117; NVME-BASE-2.4 Rev. 2.4, §3.4.1-3.4.5, printed pp. 101-105, PDF pp. 127-131; NVME-BASE-2.4 Rev. 2.4, §3.1.3, printed pp. 40, PDF pp. 66

### Visual 04: CMB, PMR, capacity, and namespaces are different resource views

**View type:** `architecture`

```text
[Identify resource type]
  ├─ [Use BIR to select BAR]
  ├─ [Check enable/status]
  ├─ [Place data for the allowed use]
  └─ [Track namespace/capacity hierarch…]
```

**Question answered:** CMB and PMR properties describe the location, capability, and state of controller-exposed memory regions; capacity Figures 86-89 describe available or allocated capacity at NVM-subsystem levels. Both concern memory, but they are different spaces and cannot be merged into one free-capacity value.

**Supporting Figures:** Figure 47, Figure 48, Figure 52, Figure 53, Figure 54, Figure 55, Figure 58, Figure 59, Figure 60, Figure 61, Figure 62, Figure 63, Figure 64, Figure 86, Figure 87, Figure 88, Figure 89

**Sources:** NVME-BASE-2.4 Rev. 2.4, §3.1.4, printed pp. 52-54, PDF pp. 78-80; NVME-BASE-2.4 Rev. 2.4, §3.8, printed pp. 125-129, PDF pp. 151-155; NVME-BASE-2.4 Rev. 2.4, §3.2.2-3.2.4, printed pp. 80-85, PDF pp. 106-111

### Visual 05: Recovery boundaries across shutdown, reset, Keep Alive, and firmware update

**View type:** `state`

```text
[Identify event source] → [Determine affected scope] → [Stop new work] → [Wait for state/timeout] → [Rebuild cleared resources] → [Verify I/O recovery]
timeout / failure ──→ preserve trigger + previous state + evidence
```

**Question answered:** The common lifecycle question is which layer of state remains valid. Normal shutdown coordinates through CC.SHN and CSTS.SHST; resets exist at subsystem, controller, and queue levels; Keep Alive monitors host-controller liveness; firmware activation may require a particular reset. The same temporary inability to process commands does not imply the same recovery.

**Supporting Figures:** Figure 43, Figure 56, Figure 84, Figure 85, Figure 90, Figure 91

**Sources:** NVME-BASE-2.4 Rev. 2.4, §3.6.1, 3.6.3, printed pp. 113-120, PDF pp. 139-146; NVME-BASE-2.4 Rev. 2.4, §3.7, printed pp. 120-125, PDF pp. 146-151; NVME-BASE-2.4 Rev. 2.4, §3.9, printed pp. 129-135, PDF pp. 155-161; NVME-BASE-2.4 Rev. 2.4, §3.10-3.11, printed pp. 135-138, PDF pp. 161-164

## Mental Model and complete teaching path

The modules follow engineering causality rather than specification-section order. Related Figures return at the point where they support the flow.

### Module 01: Separate controller type, identity, and capability first

**Explanation.** Controller type answers what work a controller can perform, Controller ID answers which controller it is, and support-requirement Figures answer the required support level of a command, log, or feature in a particular context. Figures 23-32 belong in one reading sequence, but the three questions cannot be collapsed into one Boolean.

```text
Identify controller type
  ↓
Obtain Controller ID
  ↓
Resolve command/log/feature support row
  ↓
Build the allowed operation set
```

#### Comparison

| Item | What it answers | Engineering note |
|---|---|---|
| I/O controller | Can execute user-data I/O | Optional capabilities still require individual checks |
| Administrative controller | Management purpose without data I/O commands | An Admin Queue does not make it an I/O controller |
| Support marker | Expresses support strength for a row and context | Never decode it without its column and footnote |

**Informative example.** Informative example: after detecting an Administrative controller, software still creates the Admin SQ/CQ and performs management commands, but it must not attach a namespace data path to that controller. Classifying by the mere presence of an Admin Queue incorrectly merges I/O and Administrative controllers.

**Common mistake / debugging.** A capability-matrix parser must preserve row, column, footnote, and controller type. Promoting an O, M, or conditional note into a global capability creates incorrect results in another controller or command-set context.

**Supporting sources:** NVME-BASE-2.4 Rev. 2.4, §3.1.1, printed pp. 38, PDF pp. 64; NVME-BASE-2.4 Rev. 2.4, §3.1.3-3.1.3.2, printed pp. 39-43, PDF pp. 65-69; NVME-BASE-2.4 Rev. 2.4, §3.1.3, printed pp. 40, PDF pp. 66

**Related Figures:** Figure 23, Figure 24, Figure 25, Figure 26, Figure 27, Figure 28, Figure 30, Figure 31, Figure 32

### Module 02: From CAP to CSTS.RDY: initialization is a state machine with preconditions

**Explanation.** Properties are not an independent register list. CAP constrains page-size, queue, and timeout capabilities; AQA, ASQ, and ACQ establish Admin queues; CC selects settings and enables the controller; CSTS.RDY finally declares readiness for normal command processing. Figures 33-46 and Figure 57 should be read along this causal chain.

```text
Read CAP/VS
  ↓
Configure AQA, ASQ, ACQ
  ↓
Select CC fields
  ↓
Write CC.EN=1
  ↓
Wait for CSTS.RDY=1 or timeout
```

#### Comparison

| Item | What it answers | Engineering note |
|---|---|---|
| CAP | Capabilities and limits | Read before writing configuration |
| AQA/ASQ/ACQ | Admin-queue sizes and addresses | Must match page and alignment capabilities |
| CC | Host selections and enable | Written values must be compatible with CAP |
| CSTS | Controller-reported state | RDY, CFS, and SHST are not interchangeable |

**Informative example.** Informative example: the host selects a 4 KiB MPS, so ASQ and ACQ base addresses must obey that page-size alignment. After writing CC.EN=1, the host waits for CSTS.RDY=1 within the CAP/CRTO time bound. If CFS appears first, the flow enters error recovery rather than creating I/O queues.

**Common mistake / debugging.** Initialization logs should retain offset, width, raw value, and timestamp for each property access. A single 'enable failed' message cannot distinguish incompatible settings, address alignment, CFS, or a ready transition still within its timeout.

**Supporting sources:** NVME-BASE-2.4 Rev. 2.4, §3.1.4, printed pp. 52-54, PDF pp. 78-80; NVME-BASE-2.4 Rev. 2.4, §3.5.1, 3.5.3-3.5.4, printed pp. 105-113, PDF pp. 131-139

**Related Figures:** Figure 33, Figure 34, Figure 36, Figure 37, Figure 38, Figure 41, Figure 42, Figure 44, Figure 45, Figure 46, Figure 57

### Module 03: Separate ring-buffer state, doorbells, and arbitration

**Explanation.** Figures 73 and 74 define empty/full state for a queue, while Figures 80 and 81 define arbitration among SQs competing for controller service. The first problem concerns head/tail state within one ring; the second selects among candidate SQs. Priority belongs to the SQ, not to each command as an independent priority.

```text
Host writes SQE
  ↓
Host advances tail
  ↓
Arbiter selects SQ
  ↓
Controller advances SQ head
  ↓
Controller posts CQE
  ↓
Host advances CQ head
```

#### Comparison

| Item | What it answers | Engineering note |
|---|---|---|
| Empty | Head equals tail under the empty ownership definition | No entry can be fetched |
| Full | The next tail would reach an unreleased head | The host must not overwrite an entry |
| Round Robin | Candidate SQs take turns receiving service | Completion order is not submission order |
| Weighted RR + Urgent | Priority class and weight influence selection | Interpret only under the applicable configuration |

**Informative example.** Informative example: an SQ of depth four has four slots, but full/empty detection still needs the ownership rule; an unsigned tail-minus-head value alone is insufficient. If SQ 1 and SQ 2 both contain commands, selecting SQ 2 first does not guarantee its command completes first because execution times may differ.

**Common mistake / debugging.** During debugging, record the software tail, doorbell value, controller-consumed head, and completion SQHD separately. Combining them into one 'queue index' hides distinct root causes such as a lost doorbell, stale head, premature slot reuse, or arbitration starvation.

**Supporting sources:** NVME-BASE-2.4 Rev. 2.4, §3.3.1, printed pp. 88-91, PDF pp. 114-117; NVME-BASE-2.4 Rev. 2.4, §3.4.1-3.4.5, printed pp. 101-105, PDF pp. 127-131; NVME-BASE-2.4 Rev. 2.4, §3.1.3, printed pp. 40, PDF pp. 66

**Related Figures:** Figure 73, Figure 74, Figure 80, Figure 81

### Module 04: CMB, PMR, capacity, and namespaces are different resource views

**Explanation.** CMB and PMR properties describe the location, capability, and state of controller-exposed memory regions; capacity Figures 86-89 describe available or allocated capacity at NVM-subsystem levels. Both concern memory, but they are different spaces and cannot be merged into one free-capacity value.

```text
Identify resource type
  ↓
Use BIR to select BAR
  ↓
Check enable/status
  ↓
Place data for the allowed use
  ↓
Track namespace/capacity hierarchy separately
```

#### Comparison

| Item | What it answers | Engineering note |
|---|---|---|
| CMB | Controller-provided working memory | Capability bits decide whether SQs, CQs, lists, or data may reside there |
| PMR | A region with persistence semantics | Enable, ready, error, and address control must be read together |
| Capacity model | Capacity of subsystem/group/set/namespace levels | Fields from different levels must not be subtracted directly |

**Informative example.** Informative example: enough CMB space for an SQ does not add the same amount of namespace capacity. The former is placement space for queues or data structures; the latter is formatted non-volatile capacity accessible to the host.

**Common mistake / debugging.** A memory-map debug diagram should separate host memory, CMB, PMR, and namespace media. For a CMB or PMR address, retain BIR, BAR base, offset, enable state, and ready state rather than logging only the final CPU virtual address.

**Supporting sources:** NVME-BASE-2.4 Rev. 2.4, §3.1.4, printed pp. 52-54, PDF pp. 78-80; NVME-BASE-2.4 Rev. 2.4, §3.8, printed pp. 125-129, PDF pp. 151-155; NVME-BASE-2.4 Rev. 2.4, §3.2.2-3.2.4, printed pp. 80-85, PDF pp. 106-111

**Related Figures:** Figure 47, Figure 48, Figure 52, Figure 53, Figure 54, Figure 55, Figure 58, Figure 59, Figure 60, Figure 61, Figure 62, Figure 63, Figure 64, Figure 86, Figure 87, Figure 88, Figure 89

### Module 05: Recovery boundaries across shutdown, reset, Keep Alive, and firmware update

**Explanation.** The common lifecycle question is which layer of state remains valid. Normal shutdown coordinates through CC.SHN and CSTS.SHST; resets exist at subsystem, controller, and queue levels; Keep Alive monitors host-controller liveness; firmware activation may require a particular reset. The same temporary inability to process commands does not imply the same recovery.

```text
Identify event source
  ↓
Determine affected scope
  ↓
Stop new work
  ↓
Wait for state/timeout
  ↓
Rebuild cleared resources
  ↓
Verify I/O recovery
```

#### Comparison

| Item | What it answers | Engineering note |
|---|---|---|
| Normal shutdown | Protected stop with progress reporting | Observe SHN/SHST |
| Controller reset | Controller-scope state | Queue preservation depends on reset type |
| NVM subsystem reset | Wider subsystem scope | May affect multiple controllers |
| Keep Alive timeout | Liveness failure | Must not be equated with media failure |

**Informative example.** Informative example: for a normal shutdown, the host stops submitting new I/O, sets CC.SHN, and observes CSTS.SHST. If controller fatal status appears while waiting, subsequent recovery follows reset scope and rebuilds resources rather than assuming normal shutdown completed.

**Common mistake / debugging.** A recovery trace must record trigger, scope, start/completion timestamps, timeout source, and rebuild list. A single 'reset device' message makes queue-level, controller-level, and subsystem-level state loss indistinguishable.

**Supporting sources:** NVME-BASE-2.4 Rev. 2.4, §3.6.1, 3.6.3, printed pp. 113-120, PDF pp. 139-146; NVME-BASE-2.4 Rev. 2.4, §3.7, printed pp. 120-125, PDF pp. 146-151; NVME-BASE-2.4 Rev. 2.4, §3.9, printed pp. 129-135, PDF pp. 155-161; NVME-BASE-2.4 Rev. 2.4, §3.10-3.11, printed pp. 135-138, PDF pp. 161-164

**Related Figures:** Figure 43, Figure 56, Figure 84, Figure 85, Figure 90, Figure 91

## Source-located specification findings

The mental model above explains causality. This section preserves each source-located conclusion and its normative strength for speaker notes and review.

### 1. Static controller model

<!-- claim:BASE3-STATIC -->

A memory-based controller shall support only the static controller model.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.1, printed pages 38, PDF pages 64

### 2. I/O and Administrative controllers

<!-- claim:BASE3-TYPES -->

This report uses the I/O and Administrative controller roles. The former performs user-data I/O; the latter is management-oriented and does not support data I/O commands. Both have one Admin Submission/Completion Queue pair.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.3-3.1.3.2, printed pages 39-43, PDF pages 65-69

### 3. Command and completion ordering

<!-- claim:BASE3-ORDER -->

Except for fused operations, fetched commands and completions have no general ordering guarantee. Enforcing any required order is the host's responsibility.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.3, printed pages 40, PDF pages 66

### 4. Property access width

<!-- claim:BASE3-PROPERTY -->

The host shall access a property at its starting offset using the specified width; the PCIe Transport adds the access rules for a memory-based controller.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4, printed pages 52-54, PDF pages 78-80

### 5. NSID states and special values

<!-- claim:BASE3-NAMESPACE -->

NSID 0h is invalid and FFFFFFFFh is the broadcast value. Other NSIDs still need allocated/unallocated and active/inactive classification; numeric range alone is insufficient.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.2.1, printed pages 78-80, PDF pages 104-106

### 6. Media and reclamation hierarchy

<!-- claim:BASE3-MEDIA -->

NVM Sets, Endurance Groups, Reclaim Groups, and Reclaim Units describe capacity grouping, endurance management, and reclamation granularity. Support and identifiers are determined from Identify data and log-page capabilities.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.2.2-3.2.4, printed pages 80-85, PDF pages 106-111

### 7. Domain boundaries and identifiers

<!-- claim:BASE3-DOMAIN -->

A domain is a failure or communication boundary inside an NVM subsystem. In a multi-domain subsystem, each domain identifier shall be unique within that subsystem.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.2.5, printed pages 85-88, PDF pages 111-114

### 8. PCIe queue creation and pointers

<!-- claim:BASE3-QUEUE -->

A PCIe queue is a circular buffer in host-addressable memory with head and tail pointers. The host creates an I/O Completion Queue before its Submission Queue and advances pointers through doorbells.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.3.1, printed pages 88-91, PDF pages 114-117

### 9. Command processing and arbitration

<!-- claim:BASE3-PROCESS -->

Command processing separates ordering, fused and atomic semantics, arbitration, and outstanding-command limits. Priority belongs to a Submission Queue, not to each command as an independent attribute.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.4.1-3.4.5, printed pages 101-105, PDF pages 127-131

### 10. Controller initialization

<!-- claim:BASE3-INIT -->

PCIe initialization reads CAP, configures AQA/ASQ/ACQ and CC, then waits for CSTS.RDY. Ready mode and CRTO affect host wait and error handling.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.5.1, 3.5.3-3.5.4, printed pages 105-113, PDF pages 131-139

### 11. Shutdown state flow

<!-- claim:BASE3-SHUTDOWN -->

Normal shutdown begins when the host sets CC.SHN and the controller reports progress in CSTS.SHST. NVM subsystem shutdown has a wider scope and is not the same as one controller shutdown.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.6.1, 3.6.3, printed pages 113-120, PDF pages 139-146

### 12. Reset levels and scope

<!-- claim:BASE3-RESET -->

NVM Subsystem, Controller Level, and Queue Level resets have different scopes. A recovery flow first determines which state is cleared and whether queues still exist.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.7, printed pages 120-125, PDF pages 146-151

### 13. Capacity model

<!-- claim:BASE3-CAPACITY -->

The capacity model tracks available or configured capacity separately at subsystem, Endurance Group, NVM Set, and namespace levels. Values from different levels are not directly interchangeable.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.8, printed pages 125-129, PDF pages 151-155

### 14. Keep Alive timers

<!-- claim:BASE3-KEEPALIVE -->

Keep Alive uses KATO and KATT for host/controller liveness monitoring. This report retains only controller-common and PCIe-applicable timer, command, and timeout behavior.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.9, printed pages 129-135, PDF pages 155-161

### 15. Firmware updates and privileged actions

<!-- claim:BASE3-FIRMWARE -->

A privileged action may affect other hosts or controllers. Firmware update separates image download, commit/activation, and any required reset; the host sequences the flow using the reported activation action.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.10-3.11, printed pages 135-138, PDF pages 161-164

## Figure index

This report introduces all 59 in-scope Figures. Use the section links below for the 100-minute presentation path; every Figure remains available as an appendix item.

- [§3.1](#section-3-1)

- [§3.2](#section-3-2)

- [§3.3](#section-3-3)

- [§3.4](#section-3-4)

- [§3.5](#section-3-5)

- [§3.6](#section-3-6)

- [§3.8](#section-3-8)

- [§3.9](#section-3-9)

- [§3.10](#section-3-10)

## Figure and field-table teaching reference

The source uses Figure numbers for diagrams and field-layout tables. No source artwork is reproduced; compact field and keyword indexes come from the locally verified PDFs.

<a id="section-3-1"></a>

### §3.1

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 23: Controller Types</strong></summary>

<!-- claim:BASE3-FIG-023-CLAIM figure-table:BASE3-FIG-023 -->

**SPEC.** Figure 23, "Controller Types": Shows the object or capacity relationships in Controller Types. Separate logical identifiers from controllers, namespaces, ports, and capacity containers. Evidence index: Controller.

#### Where this Figure fits

Figure 23 sits in §3.1.3 and acts as a relationship checkpoint. Read it after the report mental model has established the owning object and before software turns Controller into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This Figure explains a specific relationship or example. Identify each component type and owner, then decide whether each connection represents data flow, control flow, containment, or a condition. Visual placement alone creates no normative requirement.

#### Teaching redraw

```text
[Locate source: Controller]
          ↓
[Extract field: evidence] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `Controller` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.1.3 is the applicable context.
2. Decode Controller at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check the cited condition as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 23 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.1.3 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes Controller, the cited condition, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.1.3, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 23. Annotate the bytes containing Controller, decode them, and independently verify the cited condition. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of Controller in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand Controller and state its unit or object scope?
2. Can the reader explain why the cited condition is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** Controller

**Source keyword index:** none

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.3, Figure 23, printed pages 39, PDF pages 65

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 24: NVM Subsystem with Three I/O Controllers</strong></summary>

<!-- claim:BASE3-FIG-024-CLAIM figure-table:BASE3-FIG-024 -->

**SPEC.** Figure 24, "NVM Subsystem with Three I/O Controllers": Shows the object or capacity relationships in NVM Subsystem with Three I/O Controllers. Separate logical identifiers from controllers, namespaces, ports, and capacity containers. Evidence index: NVM Subsystem, I/O Controller, Controller.

#### Where this Figure fits

Figure 24 sits in §3.1.3.1 and acts as a hierarchy checkpoint. Read it after the report mental model has established the owning object and before software turns NVM Subsystem into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is an object or capacity relationship Figure. Separate containment, accessibility, identifier reference, and sharing. Adjacent boxes need not be one-to-one, and an identifier is not the physical or logical object it references.

#### Teaching redraw

```text
[Locate source: NVM Subsystem]
          ↓
[Extract field: I/O Controller] → [Apply encoding: Controller]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `NVM Subsystem` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `I/O Controller` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `Controller` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.1.3.1 is the applicable context.
2. Decode NVM Subsystem at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check I/O Controller as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 24 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.1.3.1 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes NVM Subsystem, I/O Controller, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.1.3.1, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 24. Annotate the bytes containing NVM Subsystem, decode them, and independently verify I/O Controller. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of NVM Subsystem in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand NVM Subsystem and state its unit or object scope?
2. Can the reader explain why I/O Controller is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** NVM Subsystem, I/O Controller, Controller

**Source keyword index:** none

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.3.1, Figure 24, printed pages 41, PDF pages 67

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 25: NVM Subsystem with One Administrative and Two I/O Controllers</strong></summary>

<!-- claim:BASE3-FIG-025-CLAIM figure-table:BASE3-FIG-025 -->

**SPEC.** Figure 25, "NVM Subsystem with One Administrative and Two I/O Controllers": Shows the object or capacity relationships in NVM Subsystem with One Administrative and Two I/O Controllers. Separate logical identifiers from controllers, namespaces, ports, and capacity containers. Evidence index: NVM Subsystem, I/O Controller, Controller.

#### Where this Figure fits

Figure 25 sits in §3.1.3.2 and acts as a hierarchy checkpoint. Read it after the report mental model has established the owning object and before software turns NVM Subsystem into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is an object or capacity relationship Figure. Separate containment, accessibility, identifier reference, and sharing. Adjacent boxes need not be one-to-one, and an identifier is not the physical or logical object it references.

#### Teaching redraw

```text
[Locate source: NVM Subsystem]
          ↓
[Extract field: I/O Controller] → [Apply encoding: Controller]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `NVM Subsystem` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `I/O Controller` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `Controller` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.1.3.2 is the applicable context.
2. Decode NVM Subsystem at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check I/O Controller as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 25 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.1.3.2 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes NVM Subsystem, I/O Controller, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.1.3.2, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 25. Annotate the bytes containing NVM Subsystem, decode them, and independently verify I/O Controller. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of NVM Subsystem in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand NVM Subsystem and state its unit or object scope?
2. Can the reader explain why I/O Controller is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** NVM Subsystem, I/O Controller, Controller

**Source keyword index:** none

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.3.2, Figure 25, printed pages 42, PDF pages 68

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 26: NVM Subsystem with One Administrative Controller</strong></summary>

<!-- claim:BASE3-FIG-026-CLAIM figure-table:BASE3-FIG-026 -->

**SPEC.** Figure 26, "NVM Subsystem with One Administrative Controller": Shows the object or capacity relationships in NVM Subsystem with One Administrative Controller. Separate logical identifiers from controllers, namespaces, ports, and capacity containers. Evidence index: NVM Subsystem, Administrative Controller, Controller.

#### Where this Figure fits

Figure 26 sits in §3.1.3.2 and acts as a hierarchy checkpoint. Read it after the report mental model has established the owning object and before software turns NVM Subsystem into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is an object or capacity relationship Figure. Separate containment, accessibility, identifier reference, and sharing. Adjacent boxes need not be one-to-one, and an identifier is not the physical or logical object it references.

#### Teaching redraw

```text
[Locate source: NVM Subsystem]
          ↓
[Extract field: Administrative Controller] → [Apply encoding: Controller]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `NVM Subsystem` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `Administrative Controller` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `Controller` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.1.3.2 is the applicable context.
2. Decode NVM Subsystem at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check Administrative Controller as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 26 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.1.3.2 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes NVM Subsystem, Administrative Controller, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.1.3.2, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 26. Annotate the bytes containing NVM Subsystem, decode them, and independently verify Administrative Controller. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of NVM Subsystem in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand NVM Subsystem and state its unit or object scope?
2. Can the reader explain why Administrative Controller is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** NVM Subsystem, Administrative Controller, Controller

**Source keyword index:** none

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.3.2, Figure 26, printed pages 42, PDF pages 68

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 27: Controller IDs FFF0h to FFFFh</strong></summary>

<!-- claim:BASE3-FIG-027-CLAIM figure-table:BASE3-FIG-027 -->

**SPEC.** Figure 27, "Controller IDs FFF0h to FFFFh": Defines the identifier composition or namespace of values shown by Controller IDs FFF0h to FFFFh. Keep the value width, issuing authority, uniqueness scope, and reserved values separate. Evidence index: Controller, Controller ID.

#### Where this Figure fits

Figure 27 sits in §3.1.3.3 and acts as a relationship checkpoint. Read it after the report mental model has established the owning object and before software turns Controller into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This Figure explains a specific relationship or example. Identify each component type and owner, then decide whether each connection represents data flow, control flow, containment, or a condition. Visual placement alone creates no normative requirement.

#### Teaching redraw

```text
[Locate source: Controller]
          ↓
[Extract field: Controller ID] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `Controller` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `Controller ID` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.1.3.3 is the applicable context.
2. Decode Controller at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check Controller ID as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 27 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.1.3.3 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes Controller, Controller ID, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.1.3.3, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 27. Annotate the bytes containing Controller, decode them, and independently verify Controller ID. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of Controller in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand Controller and state its unit or object scope?
2. Can the reader explain why Controller ID is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** Controller, Controller ID

**Source keyword index:** none

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.3.3, Figure 27, printed pages 44, PDF pages 70

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 28: Admin Command Support Requirements</strong></summary>

<!-- claim:BASE3-FIG-028-CLAIM figure-table:BASE3-FIG-028 -->

**SPEC.** Figure 28, "Admin Command Support Requirements": Summarizes the support levels assigned by Admin Command Support Requirements. Resolve the row and controller/command-set context before interpreting its support marker. Evidence index: MI, O10, O11, Command.

#### Where this Figure fits

Figure 28 sits in §3.1.3.3.3 and acts as a relationship checkpoint. Read it after the report mental model has established the owning object and before software turns MI into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This Figure explains a specific relationship or example. Identify each component type and owner, then decide whether each connection represents data flow, control flow, containment, or a condition. Visual placement alone creates no normative requirement.

#### Teaching redraw

```text
[Locate source: MI]
          ↓
[Extract field: O10] → [Apply encoding: O11]
                                      ↓
[Validate evidence: Command]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `MI` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `O10` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `O11` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `Command` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.1.3.3.3 is the applicable context.
2. Decode MI at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check O10 as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 28 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.1.3.3.3 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes MI, O10, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.1.3.3.3, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 28. Annotate the bytes containing MI, decode them, and independently verify O10. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of MI in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand MI and state its unit or object scope?
2. Can the reader explain why O10 is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** MI, O10, O11, Command

**Source keyword index:** `optional`

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.3.3.3, Figure 28, printed pages 45-47, PDF pages 71-73

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 30: Common I/O Command Support Requirements</strong></summary>

<!-- claim:BASE3-FIG-030-CLAIM figure-table:BASE3-FIG-030 -->

**SPEC.** Figure 30, "Common I/O Command Support Requirements": Summarizes the support levels assigned by Common I/O Command Support Requirements. Resolve the row and controller/command-set context before interpreting its support marker. Evidence index: FDPS, Command.

#### Where this Figure fits

Figure 30 sits in §3.1.3.4 and acts as a relationship checkpoint. Read it after the report mental model has established the owning object and before software turns FDPS into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This Figure explains a specific relationship or example. Identify each component type and owner, then decide whether each connection represents data flow, control flow, containment, or a condition. Visual placement alone creates no normative requirement.

#### Teaching redraw

```text
[Locate source: FDPS]
          ↓
[Extract field: Command] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `FDPS` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `Command` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.1.3.4 is the applicable context.
2. Decode FDPS at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check Command as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 30 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.1.3.4 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes FDPS, Command, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.1.3.4, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 30. Annotate the bytes containing FDPS, decode them, and independently verify Command. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of FDPS in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand FDPS and state its unit or object scope?
2. Can the reader explain why Command is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** FDPS, Command

**Source keyword index:** `optional`

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.3.4, Figure 30, printed pages 47-48, PDF pages 73-74

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 31: Log Page Support Requirements</strong></summary>

<!-- claim:BASE3-FIG-031-CLAIM figure-table:BASE3-FIG-031 -->

**SPEC.** Figure 31, "Log Page Support Requirements": Summarizes the support levels assigned by Log Page Support Requirements. Resolve the row and controller/command-set context before interpreting its support marker. Evidence index: M3, SMART, O4, O6, O12, O13, FDP, O5.

#### Where this Figure fits

Figure 31 sits in §3.1.3.4 and acts as a relationship checkpoint. Read it after the report mental model has established the owning object and before software turns M3 into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This Figure explains a specific relationship or example. Identify each component type and owner, then decide whether each connection represents data flow, control flow, containment, or a condition. Visual placement alone creates no normative requirement.

#### Teaching redraw

```text
[Locate source: M3]
          ↓
[Extract field: SMART] → [Apply encoding: O4]
                                      ↓
[Validate evidence: O6]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `M3` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `SMART` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `O4` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `O6` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `O12` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `O13` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.1.3.4 is the applicable context.
2. Decode M3 at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check SMART as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 31 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.1.3.4 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes M3, SMART, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.1.3.4, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 31. Annotate the bytes containing M3, decode them, and independently verify SMART. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of M3 in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand M3 and state its unit or object scope?
2. Can the reader explain why SMART is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** M3, SMART, O4, O6, O12, O13, FDP, O5

**Source keyword index:** `shall`, `optional`

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.3.4, Figure 31, printed pages 48-50, PDF pages 74-76

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 32: Feature Support Requirements</strong></summary>

<!-- claim:BASE3-FIG-032-CLAIM figure-table:BASE3-FIG-032 -->

**SPEC.** Figure 32, "Feature Support Requirements": Summarizes the support levels assigned by Feature Support Requirements. Resolve the row and controller/command-set context before interpreting its support marker. Evidence index: LBA, O8, M10, M7, O9, O6, O5, O3.

#### Where this Figure fits

Figure 32 sits in §3.1.3.5 and acts as a relationship checkpoint. Read it after the report mental model has established the owning object and before software turns LBA into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This Figure explains a specific relationship or example. Identify each component type and owner, then decide whether each connection represents data flow, control flow, containment, or a condition. Visual placement alone creates no normative requirement.

#### Teaching redraw

```text
[Locate source: LBA]
          ↓
[Extract field: O8] → [Apply encoding: M10]
                                      ↓
[Validate evidence: M7]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `LBA` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `O8` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `M10` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `M7` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `O9` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `O6` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.1.3.5 is the applicable context.
2. Decode LBA at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check O8 as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 32 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.1.3.5 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes LBA, O8, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.1.3.5, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 32. Annotate the bytes containing LBA, decode them, and independently verify O8. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of LBA in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand LBA and state its unit or object scope?
2. Can the reader explain why O8 is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** LBA, O8, M10, M7, O9, O6, O5, O3

**Source keyword index:** `optional`

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.3.5, Figure 32, printed pages 50-52, PDF pages 76-78

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 33: Property Definition</strong></summary>

<!-- claim:BASE3-FIG-033-CLAIM figure-table:BASE3-FIG-033 -->

**SPEC.** Figure 33, "Property Definition": Defines the concrete layout or value relationships for Property Definition. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is OFST, CAP, VS, M2, INTMS, INTMC, CC, CSTS.

#### Where this Figure fits

Figure 33 sits in §3.1.4 and acts as a relationship checkpoint. Read it after the report mental model has established the owning object and before software turns OFST into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This Figure explains a specific relationship or example. Identify each component type and owner, then decide whether each connection represents data flow, control flow, containment, or a condition. Visual placement alone creates no normative requirement.

#### Teaching redraw

```text
[Locate source: OFST]
          ↓
[Extract field: CAP] → [Apply encoding: VS]
                                      ↓
[Validate evidence: M2]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `OFST` | Offset, the dword-based image-relative offset in Firmware Image Download. |
| `CAP` | Controller Capabilities, the controller property at offset 00h that reports queue, page-size, timeout, and other capabilities. |
| `VS` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `M2` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `INTMS` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `INTMC` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.1.4 is the applicable context.
2. Decode OFST at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check CAP as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 33 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.1.4 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes OFST, CAP, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.1.4, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 33. Annotate the bytes containing OFST, decode them, and independently verify CAP. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of OFST in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand OFST and state its unit or object scope?
2. Can the reader explain why CAP is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** OFST, CAP, VS, M2, INTMS, INTMC, CC, CSTS

**Source keyword index:** `optional`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4, Figure 33, printed pages 52-53, PDF pages 78-79

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 34: Memory-Based Property Definition</strong></summary>

<!-- claim:BASE3-FIG-034-CLAIM figure-table:BASE3-FIG-034 -->

**SPEC.** Figure 34, "Memory-Based Property Definition": Defines the concrete layout or value relationships for Memory-Based Property Definition. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is OFST, CAP.DSTRD.

#### Where this Figure fits

Figure 34 sits in §3.1.4 and acts as a relationship checkpoint. Read it after the report mental model has established the owning object and before software turns OFST into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This Figure explains a specific relationship or example. Identify each component type and owner, then decide whether each connection represents data flow, control flow, containment, or a condition. Visual placement alone creates no normative requirement.

#### Teaching redraw

```text
[Locate source: OFST]
          ↓
[Extract field: CAP.DSTRD] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `OFST` | Offset, the dword-based image-relative offset in Firmware Image Download. |
| `CAP.DSTRD` | Controller Capabilities, the controller property at offset 00h that reports queue, page-size, timeout, and other capabilities. Here CAP.DSTRD selects its DSTRD member field. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.1.4 is the applicable context.
2. Decode OFST at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check CAP.DSTRD as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 34 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.1.4 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes OFST, CAP.DSTRD, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.1.4, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 34. Annotate the bytes containing OFST, decode them, and independently verify CAP.DSTRD. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of OFST in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand OFST and state its unit or object scope?
2. Can the reader explain why CAP.DSTRD is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** OFST, CAP.DSTRD

**Source keyword index:** `optional`

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4, Figure 34, printed pages 54, PDF pages 80

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 36: Offset 0h: CAP - Controller Capabilities</strong></summary>

<!-- claim:BASE3-FIG-036-CLAIM figure-table:BASE3-FIG-036 -->

**SPEC.** Figure 36, "Offset 0h: CAP - Controller Capabilities": Defines CAP (Controller Capabilities) at offset 0h and identifies the fields that software must decode at that location. Start at CAP, then map bit ranges to access type, reset value, and field meaning. Evidence index: NSSES, CRMS, CRIMS, CRWMS, NSSS, CMBS, PMRS, MPSMAX.

#### Where this Figure fits

Figure 36 sits in §3.1.4.1 and acts as a register checkpoint. Read it after the report mental model has established the owning object and before software turns NSSES into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a register or property field table. Locate the base offset, verify access width, reset value, and bit range, and only then convert bits into state or capability. Preserve the complete register snapshot so adjacent conditions are not lost by extracting one bit.

#### Teaching redraw

```text
[Locate source: NSSES]
          ↓
[Extract field: CRMS] → [Apply encoding: CRIMS]
                                      ↓
[Validate evidence: CRWMS]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `NSSES` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `CRMS` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `CRIMS` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `CRWMS` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `NSSS` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `CMBS` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.1.4.1 is the applicable context.
2. Decode NSSES at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check CRMS as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
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
| It answers | How the cited section organizes NSSES, CRMS, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.1.4.1, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 36. Annotate the bytes containing NSSES, decode them, and independently verify CRMS. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of NSSES in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand NSSES and state its unit or object scope?
2. Can the reader explain why CRMS is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** NSSES, CRMS, CRIMS, CRWMS, NSSS, CMBS, PMRS, MPSMAX

**Source keyword index:** `shall not`, `shall`, `should`, `may`, `optional`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.1, Figure 36, printed pages 55-58, PDF pages 81-84

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 37: Specification Version Descriptor</strong></summary>

<!-- claim:BASE3-FIG-037-CLAIM figure-table:BASE3-FIG-037 -->

**SPEC.** Figure 37, "Specification Version Descriptor": Defines the concrete layout or value relationships for Specification Version Descriptor. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is MJR, MNR, TER.

#### Where this Figure fits

Figure 37 sits in §3.1.4.1 and acts as a relationship checkpoint. Read it after the report mental model has established the owning object and before software turns MJR into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This Figure explains a specific relationship or example. Identify each component type and owner, then decide whether each connection represents data flow, control flow, containment, or a condition. Visual placement alone creates no normative requirement.

#### Teaching redraw

```text
[Locate source: MJR]
          ↓
[Extract field: MNR] → [Apply encoding: TER]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `MJR` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `MNR` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `TER` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.1.4.1 is the applicable context.
2. Decode MJR at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check MNR as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 37 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.1.4.1 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes MJR, MNR, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.1.4.1, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 37. Annotate the bytes containing MJR, decode them, and independently verify MNR. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of MJR in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand MJR and state its unit or object scope?
2. Can the reader explain why MNR is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** MJR, MNR, TER

**Source keyword index:** none

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.1, Figure 37, printed pages 58, PDF pages 84

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 38: NVM Express Base Specification Version Property Reset Values</strong></summary>

<!-- claim:BASE3-FIG-038-CLAIM figure-table:BASE3-FIG-038 -->

**SPEC.** Figure 38, "NVM Express Base Specification Version Property Reset Values": Defines the concrete layout or value relationships for NVM Express Base Specification Version Property Reset Values. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is MJR, MNR, TER.

#### Where this Figure fits

Figure 38 sits in §3.1.4.1 and acts as a state checkpoint. Read it after the report mental model has established the owning object and before software turns MJR into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a state or timing Figure. Follow each arrow while recording trigger, observer, completion condition, and timeout source. Similar state names under different reset scopes do not imply preservation of the same queue or controller state.

#### Teaching redraw

```text
[Locate source: MJR]
          ↓
[Extract field: MNR] → [Apply encoding: TER]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `MJR` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `MNR` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `TER` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.1.4.1 is the applicable context.
2. Decode MJR at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check MNR as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 38 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.1.4.1 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes MJR, MNR, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.1.4.1, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 38. Annotate the bytes containing MJR, decode them, and independently verify MNR. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of MJR in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand MJR and state its unit or object scope?
2. Can the reader explain why MNR is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** MJR, MNR, TER

**Source keyword index:** none

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.1, Figure 38, printed pages 58-59, PDF pages 84-85

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 39: Offset Ch: INTMS - Interrupt Mask Set</strong></summary>

<!-- claim:BASE3-FIG-039-CLAIM figure-table:BASE3-FIG-039 -->

**SPEC.** Figure 39, "Offset Ch: INTMS - Interrupt Mask Set": Defines INTMS (Interrupt Mask Set) at offset Ch and identifies the fields that software must decode at that location. Start at INTMS, then map bit ranges to access type, reset value, and field meaning. Evidence index: IVMS, INTMS, RWS, MSI, Interrupt.

#### Where this Figure fits

Figure 39 sits in §3.1.4.2 and acts as a register checkpoint. Read it after the report mental model has established the owning object and before software turns IVMS into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a register or property field table. Locate the base offset, verify access width, reset value, and bit range, and only then convert bits into state or capability. Preserve the complete register snapshot so adjacent conditions are not lost by extracting one bit.

#### Teaching redraw

```text
[Locate source: IVMS]
          ↓
[Extract field: INTMS] → [Apply encoding: RWS]
                                      ↓
[Validate evidence: MSI]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `IVMS` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `INTMS` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `RWS` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `MSI` | Message Signaled Interrupt, a PCI mechanism that delivers an interrupt through a memory-write message. |
| `Interrupt` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.1.4.2 is the applicable context.
2. Decode IVMS at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check INTMS as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 39 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.1.4.2 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes IVMS, INTMS, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.1.4.2, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 39. Annotate the bytes containing IVMS, decode them, and independently verify INTMS. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of IVMS in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand IVMS and state its unit or object scope?
2. Can the reader explain why INTMS is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** IVMS, INTMS, RWS, MSI, Interrupt

**Source keyword index:** none

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.2, Figure 39, printed pages 59, PDF pages 85

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 40: Offset 10h: INTMC - Interrupt Mask Clear</strong></summary>

<!-- claim:BASE3-FIG-040-CLAIM figure-table:BASE3-FIG-040 -->

**SPEC.** Figure 40, "Offset 10h: INTMC - Interrupt Mask Clear": Defines INTMC (Interrupt Mask Clear) at offset 10h and identifies the fields that software must decode at that location. Start at INTMC, then map bit ranges to access type, reset value, and field meaning. Evidence index: IVMC, INTMC, RWC, Interrupt.

#### Where this Figure fits

Figure 40 sits in §3.1.4.2 and acts as a register checkpoint. Read it after the report mental model has established the owning object and before software turns IVMC into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a register or property field table. Locate the base offset, verify access width, reset value, and bit range, and only then convert bits into state or capability. Preserve the complete register snapshot so adjacent conditions are not lost by extracting one bit.

#### Teaching redraw

```text
[Locate source: IVMC]
          ↓
[Extract field: INTMC] → [Apply encoding: RWC]
                                      ↓
[Validate evidence: Interrupt]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `IVMC` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `INTMC` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `RWC` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `Interrupt` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.1.4.2 is the applicable context.
2. Decode IVMC at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check INTMC as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 40 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.1.4.2 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes IVMC, INTMC, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.1.4.2, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 40. Annotate the bytes containing IVMC, decode them, and independently verify INTMC. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of IVMC in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand IVMC and state its unit or object scope?
2. Can the reader explain why INTMC is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** IVMC, INTMC, RWC, Interrupt

**Source keyword index:** none

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.2, Figure 40, printed pages 59, PDF pages 85

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 41: Offset 14h: CC - Controller Configuration</strong></summary>

<!-- claim:BASE3-FIG-041-CLAIM figure-table:BASE3-FIG-041 -->

**SPEC.** Figure 41, "Offset 14h: CC - Controller Configuration": Defines CC (Controller Configuration) at offset 14h and identifies the fields that software must decode at that location. Start at CC, then map bit ranges to access type, reset value, and field meaning. Evidence index: CRIME, SHN, AMS, MPS, CSS, EN, CC, CC.EN.

#### Where this Figure fits

Figure 41 sits in §3.1.4.5 and acts as a register checkpoint. Read it after the report mental model has established the owning object and before software turns CRIME into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a register or property field table. Locate the base offset, verify access width, reset value, and bit range, and only then convert bits into state or capability. Preserve the complete register snapshot so adjacent conditions are not lost by extracting one bit.

#### Teaching redraw

```text
[Locate source: CRIME]
          ↓
[Extract field: SHN] → [Apply encoding: AMS]
                                      ↓
[Validate evidence: MPS]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `CRIME` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `SHN` | Shutdown Notification, the CC field through which the host declares a shutdown type. |
| `AMS` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `MPS` | Memory Page Size, the controller memory-page-size setting; it affects queue addresses and PRP alignment. |
| `CSS` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `EN` | Enable, the CC bit controlling controller enable state. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.1.4.5 is the applicable context.
2. Decode CRIME at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check SHN as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 41 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.1.4.5 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes CRIME, SHN, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.1.4.5, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 41. Annotate the bytes containing CRIME, decode them, and independently verify SHN. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of CRIME in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand CRIME and state its unit or object scope?
2. Can the reader explain why SHN is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** CRIME, SHN, AMS, MPS, CSS, EN, CC, CC.EN

**Source keyword index:** `shall not`, `shall`, `should`, `may`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.5, Figure 41, printed pages 60-63, PDF pages 86-89

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 42: Offset 1Ch: CSTS - Controller Status</strong></summary>

<!-- claim:BASE3-FIG-042-CLAIM figure-table:BASE3-FIG-042 -->

**SPEC.** Figure 42, "Offset 1Ch: CSTS - Controller Status": Defines CSTS (Controller Status) at offset 1Ch and identifies the fields that software must decode at that location. Start at CSTS, then map bit ranges to access type, reset value, and field meaning. Evidence index: ST, PP, NSSRO, SHST, CLR, CFS, RDY, CSTS.

#### Where this Figure fits

Figure 42 sits in §3.1.4.5 and acts as a register checkpoint. Read it after the report mental model has established the owning object and before software turns ST into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a register or property field table. Locate the base offset, verify access width, reset value, and bit range, and only then convert bits into state or capability. Preserve the complete register snapshot so adjacent conditions are not lost by extracting one bit.

#### Teaching redraw

```text
[Locate source: ST]
          ↓
[Extract field: PP] → [Apply encoding: NSSRO]
                                      ↓
[Validate evidence: SHST]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `ST` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `PP` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `NSSRO` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `SHST` | Shutdown Status, the CSTS field through which the controller reports shutdown progress. |
| `CLR` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `CFS` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.1.4.5 is the applicable context.
2. Decode ST at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check PP as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 42 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.1.4.5 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes ST, PP, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.1.4.5, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 42. Annotate the bytes containing ST, decode them, and independently verify PP. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of ST in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand ST and state its unit or object scope?
2. Can the reader explain why PP is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** ST, PP, NSSRO, SHST, CLR, CFS, RDY, CSTS

**Source keyword index:** `shall not`, `should not`, `shall`, `should`, `may`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.5, Figure 42, printed pages 63-65, PDF pages 89-91

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 43: Offset 20h: NSSR - NVM Subsystem Reset</strong></summary>

<!-- claim:BASE3-FIG-043-CLAIM figure-table:BASE3-FIG-043 -->

**SPEC.** Figure 43, "Offset 20h: NSSR - NVM Subsystem Reset": Defines NSSR (NVM Subsystem Reset) at offset 20h and identifies the fields that software must decode at that location. Start at NSSR, then map bit ranges to access type, reset value, and field meaning. Evidence index: NSSRC, NSSR, NVM Subsystem.

#### Where this Figure fits

Figure 43 sits in §3.1.4.6 and acts as a register checkpoint. Read it after the report mental model has established the owning object and before software turns NSSRC into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a register or property field table. Locate the base offset, verify access width, reset value, and bit range, and only then convert bits into state or capability. Preserve the complete register snapshot so adjacent conditions are not lost by extracting one bit.

#### Teaching redraw

```text
[Locate source: NSSRC]
          ↓
[Extract field: NSSR] → [Apply encoding: NVM Subsystem]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `NSSRC` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `NSSR` | NVM Subsystem Reset, the property used to initiate an NVM subsystem reset. |
| `NVM Subsystem` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.1.4.6 is the applicable context.
2. Decode NSSRC at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check NSSR as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 43 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.1.4.6 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes NSSRC, NSSR, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.1.4.6, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 43. Annotate the bytes containing NSSRC, decode them, and independently verify NSSR. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of NSSRC in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand NSSRC and state its unit or object scope?
2. Can the reader explain why NSSR is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** NSSRC, NSSR, NVM Subsystem

**Source keyword index:** `shall`

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.6, Figure 43, printed pages 66, PDF pages 92

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 44: Offset 24h: AQA - Admin Queue Attributes</strong></summary>

<!-- claim:BASE3-FIG-044-CLAIM figure-table:BASE3-FIG-044 -->

**SPEC.** Figure 44, "Offset 24h: AQA - Admin Queue Attributes": Defines AQA (Admin Queue Attributes) at offset 24h and identifies the fields that software must decode at that location. Start at AQA, then map bit ranges to access type, reset value, and field meaning. Evidence index: ACQS, ASQS, AQA.

#### Where this Figure fits

Figure 44 sits in §3.1.4.6 and acts as a register checkpoint. Read it after the report mental model has established the owning object and before software turns ACQS into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a register or property field table. Locate the base offset, verify access width, reset value, and bit range, and only then convert bits into state or capability. Preserve the complete register snapshot so adjacent conditions are not lost by extracting one bit.

#### Teaching redraw

```text
[Locate source: ACQS]
          ↓
[Extract field: ASQS] → [Apply encoding: AQA]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `ACQS` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `ASQS` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `AQA` | Admin Queue Attributes, the property describing Admin SQ and Admin CQ sizes. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.1.4.6 is the applicable context.
2. Decode ACQS at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check ASQS as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 44 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.1.4.6 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes ACQS, ASQS, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.1.4.6, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 44. Annotate the bytes containing ACQS, decode them, and independently verify ASQS. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of ACQS in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand ACQS and state its unit or object scope?
2. Can the reader explain why ASQS is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** ACQS, ASQS, AQA

**Source keyword index:** `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.6, Figure 44, printed pages 66, PDF pages 92

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 45: Offset 28h: ASQ - Admin Submission Queue Base Address</strong></summary>

<!-- claim:BASE3-FIG-045-CLAIM figure-table:BASE3-FIG-045 -->

**SPEC.** Figure 45, "Offset 28h: ASQ - Admin Submission Queue Base Address": Defines ASQ (Admin Submission Queue Base Address) at offset 28h and identifies the fields that software must decode at that location. Start at ASQ, then map bit ranges to access type, reset value, and field meaning. Evidence index: ASQB, ASQ, CC.MPS, Submission Queue.

#### Where this Figure fits

Figure 45 sits in §3.1.4.6 and acts as a register checkpoint. Read it after the report mental model has established the owning object and before software turns ASQB into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a register or property field table. Locate the base offset, verify access width, reset value, and bit range, and only then convert bits into state or capability. Preserve the complete register snapshot so adjacent conditions are not lost by extracting one bit.

#### Teaching redraw

```text
[Locate source: ASQB]
          ↓
[Extract field: ASQ] → [Apply encoding: CC.MPS]
                                      ↓
[Validate evidence: Submission Queue]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `ASQB` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `ASQ` | Admin Submission Queue Base Address, the base address of the Admin SQ in addressable memory. |
| `CC.MPS` | Controller Configuration, the property through which the host selects settings and enables or disables a controller. Here CC.MPS selects its MPS member field. |
| `Submission Queue` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.1.4.6 is the applicable context.
2. Decode ASQB at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check ASQ as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 45 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.1.4.6 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes ASQB, ASQ, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.1.4.6, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 45. Annotate the bytes containing ASQB, decode them, and independently verify ASQ. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of ASQB in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand ASQB and state its unit or object scope?
2. Can the reader explain why ASQ is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** ASQB, ASQ, CC.MPS, Submission Queue

**Source keyword index:** `shall`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.6, Figure 45, printed pages 66, PDF pages 92

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 46: Offset 30h: ACQ - Admin Completion Queue Base Address</strong></summary>

<!-- claim:BASE3-FIG-046-CLAIM figure-table:BASE3-FIG-046 -->

**SPEC.** Figure 46, "Offset 30h: ACQ - Admin Completion Queue Base Address": Defines ACQ (Admin Completion Queue Base Address) at offset 30h and identifies the fields that software must decode at that location. Start at ACQ, then map bit ranges to access type, reset value, and field meaning. Evidence index: ACQB, ACQ, CC.MPS, Completion Queue.

#### Where this Figure fits

Figure 46 sits in §3.1.4.9 and acts as a register checkpoint. Read it after the report mental model has established the owning object and before software turns ACQB into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a register or property field table. Locate the base offset, verify access width, reset value, and bit range, and only then convert bits into state or capability. Preserve the complete register snapshot so adjacent conditions are not lost by extracting one bit.

#### Teaching redraw

```text
[Locate source: ACQB]
          ↓
[Extract field: ACQ] → [Apply encoding: CC.MPS]
                                      ↓
[Validate evidence: Completion Queue]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `ACQB` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `ACQ` | Admin Completion Queue Base Address, the base address of the Admin CQ in addressable memory. |
| `CC.MPS` | Controller Configuration, the property through which the host selects settings and enables or disables a controller. Here CC.MPS selects its MPS member field. |
| `Completion Queue` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.1.4.9 is the applicable context.
2. Decode ACQB at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check ACQ as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 46 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.1.4.9 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes ACQB, ACQ, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.1.4.9, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 46. Annotate the bytes containing ACQB, decode them, and independently verify ACQ. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of ACQB in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand ACQB and state its unit or object scope?
2. Can the reader explain why ACQ is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** ACQB, ACQ, CC.MPS, Completion Queue

**Source keyword index:** `shall`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.9, Figure 46, printed pages 67, PDF pages 93

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 47: Offset 38h: CMBLOC - Controller Memory Buffer Location</strong></summary>

<!-- claim:BASE3-FIG-047-CLAIM figure-table:BASE3-FIG-047 -->

**SPEC.** Figure 47, "Offset 38h: CMBLOC - Controller Memory Buffer Location": Defines CMBLOC (Controller Memory Buffer Location) at offset 38h and identifies the fields that software must decode at that location. Start at CMBLOC, then map bit ranges to access type, reset value, and field meaning. Evidence index: CQMMS, BIR, CMBLOC, CMB, BAR, Controller.

#### Where this Figure fits

Figure 47 sits in §3.1.4.9 and acts as a register checkpoint. Read it after the report mental model has established the owning object and before software turns CQMMS into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a register or property field table. Locate the base offset, verify access width, reset value, and bit range, and only then convert bits into state or capability. Preserve the complete register snapshot so adjacent conditions are not lost by extracting one bit.

#### Teaching redraw

```text
[Locate source: CQMMS]
          ↓
[Extract field: BIR] → [Apply encoding: CMBLOC]
                                      ↓
[Validate evidence: CMB]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `CQMMS` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `BIR` | BAR Indicator Register, a selector identifying the PCIe BAR that contains a memory structure. |
| `CMBLOC` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `CMB` | Controller Memory Buffer, controller-provided memory in which selected queues or data structures may reside. |
| `BAR` | Base Address Register, a PCI-configuration-space register locating a device memory space. |
| `Controller` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.1.4.9 is the applicable context.
2. Decode CQMMS at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check BIR as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 47 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.1.4.9 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes CQMMS, BIR, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.1.4.9, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 47. Annotate the bytes containing CQMMS, decode them, and independently verify BIR. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of CQMMS in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand CQMMS and state its unit or object scope?
2. Can the reader explain why BIR is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** CQMMS, BIR, CMBLOC, CMB, BAR, Controller

**Source keyword index:** `shall`

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.9, Figure 47, printed pages 67-68, PDF pages 93-94

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 48: Offset 3Ch: CMBSZ - Controller Memory Buffer Size</strong></summary>

<!-- claim:BASE3-FIG-048-CLAIM figure-table:BASE3-FIG-048 -->

**SPEC.** Figure 48, "Offset 3Ch: CMBSZ - Controller Memory Buffer Size": Defines CMBSZ (Controller Memory Buffer Size) at offset 3Ch and identifies the fields that software must decode at that location. Start at CMBSZ, then map bit ranges to access type, reset value, and field meaning. Evidence index: SZ, SZU, WDS, RDS, LISTS, CQS, SQS, CMBSZ.

#### Where this Figure fits

Figure 48 sits in §3.1.4.11 and acts as a register checkpoint. Read it after the report mental model has established the owning object and before software turns SZ into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a register or property field table. Locate the base offset, verify access width, reset value, and bit range, and only then convert bits into state or capability. Preserve the complete register snapshot so adjacent conditions are not lost by extracting one bit.

#### Teaching redraw

```text
[Locate source: SZ]
          ↓
[Extract field: SZU] → [Apply encoding: WDS]
                                      ↓
[Validate evidence: RDS]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `SZ` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `SZU` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `WDS` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `RDS` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `LISTS` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `CQS` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.1.4.11 is the applicable context.
2. Decode SZ at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check SZU as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 48 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.1.4.11 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes SZ, SZU, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.1.4.11, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 48. Annotate the bytes containing SZ, decode them, and independently verify SZU. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of SZ in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand SZ and state its unit or object scope?
2. Can the reader explain why SZU is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** SZ, SZU, WDS, RDS, LISTS, CQS, SQS, CMBSZ

**Source keyword index:** `shall not`, `shall`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.11, Figure 48, printed pages 68-69, PDF pages 94-95

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 49: Offset 40h: BPINFO - Boot Partition Information</strong></summary>

<!-- claim:BASE3-FIG-049-CLAIM figure-table:BASE3-FIG-049 -->

**SPEC.** Figure 49, "Offset 40h: BPINFO - Boot Partition Information": Defines BPINFO (Boot Partition Information) at offset 40h and identifies the fields that software must decode at that location. Start at BPINFO, then map bit ranges to access type, reset value, and field meaning. Evidence index: ABPID, BRS, BPSZ, BPINFO, ID, BPRSEL.BPID.

#### Where this Figure fits

Figure 49 sits in §3.1.4.12 and acts as a register checkpoint. Read it after the report mental model has established the owning object and before software turns ABPID into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a register or property field table. Locate the base offset, verify access width, reset value, and bit range, and only then convert bits into state or capability. Preserve the complete register snapshot so adjacent conditions are not lost by extracting one bit.

#### Teaching redraw

```text
[Locate source: ABPID]
          ↓
[Extract field: BRS] → [Apply encoding: BPSZ]
                                      ↓
[Validate evidence: BPINFO]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `ABPID` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `BRS` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `BPSZ` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `BPINFO` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `ID` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `BPRSEL.BPID` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.1.4.12 is the applicable context.
2. Decode ABPID at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check BRS as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 49 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.1.4.12 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes ABPID, BRS, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.1.4.12, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 49. Annotate the bytes containing ABPID, decode them, and independently verify BRS. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of ABPID in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand ABPID and state its unit or object scope?
2. Can the reader explain why BRS is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** ABPID, BRS, BPSZ, BPINFO, ID, BPRSEL.BPID

**Source keyword index:** `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.12, Figure 49, printed pages 69, PDF pages 95

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 50: Offset 44h: BPRSEL - Boot Partition Read Select</strong></summary>

<!-- claim:BASE3-FIG-050-CLAIM figure-table:BASE3-FIG-050 -->

**SPEC.** Figure 50, "Offset 44h: BPRSEL - Boot Partition Read Select": Defines BPRSEL (Boot Partition Read Select) at offset 44h and identifies the fields that software must decode at that location. Start at BPRSEL, then map bit ranges to access type, reset value, and field meaning. Evidence index: BPID, BPROF, BPRSZ, BPRSEL.

#### Where this Figure fits

Figure 50 sits in §3.1.4.12 and acts as a register checkpoint. Read it after the report mental model has established the owning object and before software turns BPID into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a register or property field table. Locate the base offset, verify access width, reset value, and bit range, and only then convert bits into state or capability. Preserve the complete register snapshot so adjacent conditions are not lost by extracting one bit.

#### Teaching redraw

```text
[Locate source: BPID]
          ↓
[Extract field: BPROF] → [Apply encoding: BPRSZ]
                                      ↓
[Validate evidence: BPRSEL]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `BPID` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `BPROF` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `BPRSZ` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `BPRSEL` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.1.4.12 is the applicable context.
2. Decode BPID at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check BPROF as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 50 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.1.4.12 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes BPID, BPROF, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.1.4.12, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 50. Annotate the bytes containing BPID, decode them, and independently verify BPROF. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of BPID in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand BPID and state its unit or object scope?
2. Can the reader explain why BPROF is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** BPID, BPROF, BPRSZ, BPRSEL

**Source keyword index:** `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.12, Figure 50, printed pages 69-70, PDF pages 95-96

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 51: Offset 48h: BPMBL - Boot Partition Memory Buffer Location</strong></summary>

<!-- claim:BASE3-FIG-051-CLAIM figure-table:BASE3-FIG-051 -->

**SPEC.** Figure 51, "Offset 48h: BPMBL - Boot Partition Memory Buffer Location": Defines BPMBL (Boot Partition Memory Buffer Location) at offset 48h and identifies the fields that software must decode at that location. Start at BPMBL, then map bit ranges to access type, reset value, and field meaning. Evidence index: BMBBA, BPMBL.

#### Where this Figure fits

Figure 51 sits in §3.1.4.14 and acts as a register checkpoint. Read it after the report mental model has established the owning object and before software turns BMBBA into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a register or property field table. Locate the base offset, verify access width, reset value, and bit range, and only then convert bits into state or capability. Preserve the complete register snapshot so adjacent conditions are not lost by extracting one bit.

#### Teaching redraw

```text
[Locate source: BMBBA]
          ↓
[Extract field: BPMBL] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `BMBBA` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `BPMBL` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.1.4.14 is the applicable context.
2. Decode BMBBA at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check BPMBL as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 51 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.1.4.14 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes BMBBA, BPMBL, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.1.4.14, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 51. Annotate the bytes containing BMBBA, decode them, and independently verify BPMBL. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of BMBBA in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand BMBBA and state its unit or object scope?
2. Can the reader explain why BPMBL is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** BMBBA, BPMBL

**Source keyword index:** `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.14, Figure 51, printed pages 70, PDF pages 96

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 52: Offset 50h: CMBMSC - Controller Memory Buffer Memory Space Control</strong></summary>

<!-- claim:BASE3-FIG-052-CLAIM figure-table:BASE3-FIG-052 -->

**SPEC.** Figure 52, "Offset 50h: CMBMSC - Controller Memory Buffer Memory Space Control": Defines CMBMSC (Controller Memory Buffer Memory Space Control) at offset 50h and identifies the fields that software must decode at that location. Start at CMBMSC, then map bit ranges to access type, reset value, and field meaning. Evidence index: CBA, CMSE, CRE, CMBMSC, CMBSMSC.CRE, CMBLOC, CMBSZ, Controller.

#### Where this Figure fits

Figure 52 sits in §3.1.4.14 and acts as a register checkpoint. Read it after the report mental model has established the owning object and before software turns CBA into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a register or property field table. Locate the base offset, verify access width, reset value, and bit range, and only then convert bits into state or capability. Preserve the complete register snapshot so adjacent conditions are not lost by extracting one bit.

#### Teaching redraw

```text
[Locate source: CBA]
          ↓
[Extract field: CMSE] → [Apply encoding: CRE]
                                      ↓
[Validate evidence: CMBMSC]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `CBA` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `CMSE` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `CRE` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `CMBMSC` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `CMBSMSC.CRE` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `CMBLOC` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.1.4.14 is the applicable context.
2. Decode CBA at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check CMSE as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 52 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.1.4.14 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes CBA, CMSE, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.1.4.14, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 52. Annotate the bytes containing CBA, decode them, and independently verify CMSE. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of CBA in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand CBA and state its unit or object scope?
2. Can the reader explain why CMSE is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** CBA, CMSE, CRE, CMBMSC, CMBSMSC.CRE, CMBLOC, CMBSZ, Controller

**Source keyword index:** `shall`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.14, Figure 52, printed pages 70-71, PDF pages 96-97

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 53: Offset 58h: CMBSTS - Controller Memory Buffer Status</strong></summary>

<!-- claim:BASE3-FIG-053-CLAIM figure-table:BASE3-FIG-053 -->

**SPEC.** Figure 53, "Offset 58h: CMBSTS - Controller Memory Buffer Status": Defines CMBSTS (Controller Memory Buffer Status) at offset 58h and identifies the fields that software must decode at that location. Start at CMBSTS, then map bit ranges to access type, reset value, and field meaning. Evidence index: CBAI, CMBSTS, CMBMSC.CBA, CMBMSC.CRE, CMBMSC.CMSE, Controller.

#### Where this Figure fits

Figure 53 sits in §3.1.4.16 and acts as a register checkpoint. Read it after the report mental model has established the owning object and before software turns CBAI into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a register or property field table. Locate the base offset, verify access width, reset value, and bit range, and only then convert bits into state or capability. Preserve the complete register snapshot so adjacent conditions are not lost by extracting one bit.

#### Teaching redraw

```text
[Locate source: CBAI]
          ↓
[Extract field: CMBSTS] → [Apply encoding: CMBMSC.CBA]
                                      ↓
[Validate evidence: CMBMSC.CRE]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `CBAI` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `CMBSTS` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `CMBMSC.CBA` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `CMBMSC.CRE` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `CMBMSC.CMSE` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `Controller` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.1.4.16 is the applicable context.
2. Decode CBAI at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check CMBSTS as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 53 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.1.4.16 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes CBAI, CMBSTS, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.1.4.16, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 53. Annotate the bytes containing CBAI, decode them, and independently verify CMBSTS. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of CBAI in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand CBAI and state its unit or object scope?
2. Can the reader explain why CMBSTS is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** CBAI, CMBSTS, CMBMSC.CBA, CMBMSC.CRE, CMBMSC.CMSE, Controller

**Source keyword index:** `shall`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.16, Figure 53, printed pages 71, PDF pages 97

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 54: Offset 5Ch: CMBEBS - Controller Memory Buffer Elasticity Buffer Size</strong></summary>

<!-- claim:BASE3-FIG-054-CLAIM figure-table:BASE3-FIG-054 -->

**SPEC.** Figure 54, "Offset 5Ch: CMBEBS - Controller Memory Buffer Elasticity Buffer Size": Defines CMBEBS (Controller Memory Buffer Elasticity Buffer Size) at offset 5Ch and identifies the fields that software must decode at that location. Start at CMBEBS, then map bit ranges to access type, reset value, and field meaning. Evidence index: CMBWBZ, CMBRBB, CMBSZU, CMBEBS, CMB, Controller.

#### Where this Figure fits

Figure 54 sits in §3.1.4.16 and acts as a register checkpoint. Read it after the report mental model has established the owning object and before software turns CMBWBZ into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a register or property field table. Locate the base offset, verify access width, reset value, and bit range, and only then convert bits into state or capability. Preserve the complete register snapshot so adjacent conditions are not lost by extracting one bit.

#### Teaching redraw

```text
[Locate source: CMBWBZ]
          ↓
[Extract field: CMBRBB] → [Apply encoding: CMBSZU]
                                      ↓
[Validate evidence: CMBEBS]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `CMBWBZ` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `CMBRBB` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `CMBSZU` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `CMBEBS` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `CMB` | Controller Memory Buffer, controller-provided memory in which selected queues or data structures may reside. |
| `Controller` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.1.4.16 is the applicable context.
2. Decode CMBWBZ at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check CMBRBB as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 54 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.1.4.16 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes CMBWBZ, CMBRBB, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.1.4.16, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 54. Annotate the bytes containing CMBWBZ, decode them, and independently verify CMBRBB. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of CMBWBZ in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand CMBWBZ and state its unit or object scope?
2. Can the reader explain why CMBRBB is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** CMBWBZ, CMBRBB, CMBSZU, CMBEBS, CMB, Controller

**Source keyword index:** `shall`, `may`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.16, Figure 54, printed pages 71, PDF pages 97

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 55: Offset 60h: CMBSWTP - Controller Memory Buffer Sustained Write Throughput</strong></summary>

<!-- claim:BASE3-FIG-055-CLAIM figure-table:BASE3-FIG-055 -->

**SPEC.** Figure 55, "Offset 60h: CMBSWTP - Controller Memory Buffer Sustained Write Throughput": Defines CMBSWTP (Controller Memory Buffer Sustained Write Throughput) at offset 60h and identifies the fields that software must decode at that location. Start at CMBSWTP, then map bit ranges to access type, reset value, and field meaning. Evidence index: CMBSWTV, CMBSWTU, CMBSWTP, CMB, TLP, MPS, PXDC, Controller.

#### Where this Figure fits

Figure 55 sits in §3.1.4.19 and acts as a register checkpoint. Read it after the report mental model has established the owning object and before software turns CMBSWTV into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a register or property field table. Locate the base offset, verify access width, reset value, and bit range, and only then convert bits into state or capability. Preserve the complete register snapshot so adjacent conditions are not lost by extracting one bit.

#### Teaching redraw

```text
[Locate source: CMBSWTV]
          ↓
[Extract field: CMBSWTU] → [Apply encoding: CMBSWTP]
                                      ↓
[Validate evidence: CMB]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `CMBSWTV` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `CMBSWTU` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `CMBSWTP` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `CMB` | Controller Memory Buffer, controller-provided memory in which selected queues or data structures may reside. |
| `TLP` | Transaction Layer Packet, a packet carried by the PCIe transaction layer. |
| `MPS` | Memory Page Size, the controller memory-page-size setting; it affects queue addresses and PRP alignment. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.1.4.19 is the applicable context.
2. Decode CMBSWTV at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check CMBSWTU as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 55 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.1.4.19 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes CMBSWTV, CMBSWTU, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.1.4.19, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 55. Annotate the bytes containing CMBSWTV, decode them, and independently verify CMBSWTU. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of CMBSWTV in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand CMBSWTV and state its unit or object scope?
2. Can the reader explain why CMBSWTU is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** CMBSWTV, CMBSWTU, CMBSWTP, CMB, TLP, MPS, PXDC, Controller

**Source keyword index:** `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.19, Figure 55, printed pages 72, PDF pages 98

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 56: Offset 64h: NSSD - NVM Subsystem Shutdown</strong></summary>

<!-- claim:BASE3-FIG-056-CLAIM figure-table:BASE3-FIG-056 -->

**SPEC.** Figure 56, "Offset 64h: NSSD - NVM Subsystem Shutdown": Defines NSSD (NVM Subsystem Shutdown) at offset 64h and identifies the fields that software must decode at that location. Start at NSSD, then map bit ranges to access type, reset value, and field meaning. Evidence index: NSSC, NSSD, CAP.CPS, NVM Subsystem.

#### Where this Figure fits

Figure 56 sits in §3.1.4.19 and acts as a register checkpoint. Read it after the report mental model has established the owning object and before software turns NSSC into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a register or property field table. Locate the base offset, verify access width, reset value, and bit range, and only then convert bits into state or capability. Preserve the complete register snapshot so adjacent conditions are not lost by extracting one bit.

#### Teaching redraw

```text
[Locate source: NSSC]
          ↓
[Extract field: NSSD] → [Apply encoding: CAP.CPS]
                                      ↓
[Validate evidence: NVM Subsystem]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `NSSC` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `NSSD` | NVM Subsystem Shutdown, the property controlling the wider-scope subsystem shutdown. |
| `CAP.CPS` | Controller Capabilities, the controller property at offset 00h that reports queue, page-size, timeout, and other capabilities. Here CAP.CPS selects its CPS member field. |
| `NVM Subsystem` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.1.4.19 is the applicable context.
2. Decode NSSC at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check NSSD as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 56 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.1.4.19 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes NSSC, NSSD, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.1.4.19, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 56. Annotate the bytes containing NSSC, decode them, and independently verify NSSD. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of NSSC in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand NSSC and state its unit or object scope?
2. Can the reader explain why NSSD is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** NSSC, NSSD, CAP.CPS, NVM Subsystem

**Source keyword index:** `shall`

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.19, Figure 56, printed pages 72, PDF pages 98

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 57: Offset 68h: CRTO - Controller Ready Timeouts</strong></summary>

<!-- claim:BASE3-FIG-057-CLAIM figure-table:BASE3-FIG-057 -->

**SPEC.** Figure 57, "Offset 68h: CRTO - Controller Ready Timeouts": Defines CRTO (Controller Ready Timeouts) at offset 68h and identifies the fields that software must decode at that location. Start at CRTO, then map bit ranges to access type, reset value, and field meaning. Evidence index: CRIMT, CRWMT, CRTO, CAP.CRMS.CRIMS, CC.EN, CC.CRIME, CRTO.CRIMT, Controller.

#### Where this Figure fits

Figure 57 sits in §3.1.4.21 and acts as a register checkpoint. Read it after the report mental model has established the owning object and before software turns CRIMT into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a register or property field table. Locate the base offset, verify access width, reset value, and bit range, and only then convert bits into state or capability. Preserve the complete register snapshot so adjacent conditions are not lost by extracting one bit.

#### Teaching redraw

```text
[Locate source: CRIMT]
          ↓
[Extract field: CRWMT] → [Apply encoding: CRTO]
                                      ↓
[Validate evidence: CAP.CRMS.CRIMS]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `CRIMT` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `CRWMT` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `CRTO` | Controller Ready Timeouts, the property reporting wait times for specific ready modes. |
| `CAP.CRMS.CRIMS` | Controller Capabilities, the controller property at offset 00h that reports queue, page-size, timeout, and other capabilities. Here CAP.CRMS.CRIMS selects its CRMS.CRIMS member field. |
| `CC.EN` | Controller Configuration, the property through which the host selects settings and enables or disables a controller. Here CC.EN selects its EN member field. |
| `CC.CRIME` | Controller Configuration, the property through which the host selects settings and enables or disables a controller. Here CC.CRIME selects its CRIME member field. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.1.4.21 is the applicable context.
2. Decode CRIMT at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check CRWMT as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 57 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.1.4.21 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes CRIMT, CRWMT, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.1.4.21, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 57. Annotate the bytes containing CRIMT, decode them, and independently verify CRWMT. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of CRIMT in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand CRIMT and state its unit or object scope?
2. Can the reader explain why CRWMT is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** CRIMT, CRWMT, CRTO, CAP.CRMS.CRIMS, CC.EN, CC.CRIME, CRTO.CRIMT, Controller

**Source keyword index:** `should not`, `shall`, `should`, `may`

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.21, Figure 57, printed pages 73, PDF pages 99

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 58: Offset E00h: PMRCAP - Persistent Memory Region Capabilities</strong></summary>

<!-- claim:BASE3-FIG-058-CLAIM figure-table:BASE3-FIG-058 -->

**SPEC.** Figure 58, "Offset E00h: PMRCAP - Persistent Memory Region Capabilities": Defines PMRCAP (Persistent Memory Region Capabilities) at offset E00h and identifies the fields that software must decode at that location. Start at PMRCAP, then map bit ranges to access type, reset value, and field meaning. Evidence index: CMSS, PMRTO, PMRWBM, CPMTSTSR, CMR, PMRTU, BIR, WDS.

#### Where this Figure fits

Figure 58 sits in §3.1.4.21 and acts as a register checkpoint. Read it after the report mental model has established the owning object and before software turns CMSS into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a register or property field table. Locate the base offset, verify access width, reset value, and bit range, and only then convert bits into state or capability. Preserve the complete register snapshot so adjacent conditions are not lost by extracting one bit.

#### Teaching redraw

```text
[Locate source: CMSS]
          ↓
[Extract field: PMRTO] → [Apply encoding: PMRWBM]
                                      ↓
[Validate evidence: CPMTSTSR]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `CMSS` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `PMRTO` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `PMRWBM` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `CPMTSTSR` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `CMR` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `PMRTU` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.1.4.21 is the applicable context.
2. Decode CMSS at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check PMRTO as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 58 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.1.4.21 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes CMSS, PMRTO, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.1.4.21, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 58. Annotate the bytes containing CMSS, decode them, and independently verify PMRTO. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of CMSS in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand CMSS and state its unit or object scope?
2. Can the reader explain why PMRTO is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** CMSS, PMRTO, PMRWBM, CPMTSTSR, CMR, PMRTU, BIR, WDS

**Source keyword index:** `shall not`, `shall`, `should`, `may`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.21, Figure 58, printed pages 73-74, PDF pages 99-100

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 59: Offset E04h: PMRCTL - Persistent Memory Region Control</strong></summary>

<!-- claim:BASE3-FIG-059-CLAIM figure-table:BASE3-FIG-059 -->

**SPEC.** Figure 59, "Offset E04h: PMRCTL - Persistent Memory Region Control": Defines PMRCTL (Persistent Memory Region Control) at offset E04h and identifies the fields that software must decode at that location. Start at PMRCTL, then map bit ranges to access type, reset value, and field meaning. Evidence index: EN, PMRCTL, PMRSTS.NRDY.

#### Where this Figure fits

Figure 59 sits in §3.1.4.22 and acts as a register checkpoint. Read it after the report mental model has established the owning object and before software turns EN into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a register or property field table. Locate the base offset, verify access width, reset value, and bit range, and only then convert bits into state or capability. Preserve the complete register snapshot so adjacent conditions are not lost by extracting one bit.

#### Teaching redraw

```text
[Locate source: EN]
          ↓
[Extract field: PMRCTL] → [Apply encoding: PMRSTS.NRDY]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `EN` | Enable, the CC bit controlling controller enable state. |
| `PMRCTL` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `PMRSTS.NRDY` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.1.4.22 is the applicable context.
2. Decode EN at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check PMRCTL as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 59 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.1.4.22 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes EN, PMRCTL, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.1.4.22, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 59. Annotate the bytes containing EN, decode them, and independently verify PMRCTL. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of EN in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand EN and state its unit or object scope?
2. Can the reader explain why PMRCTL is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** EN, PMRCTL, PMRSTS.NRDY

**Source keyword index:** `shall`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.22, Figure 59, printed pages 74, PDF pages 100

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 60: Offset E08h: PMRSTS - Persistent Memory Region Status</strong></summary>

<!-- claim:BASE3-FIG-060-CLAIM figure-table:BASE3-FIG-060 -->

**SPEC.** Figure 60, "Offset E08h: PMRSTS - Persistent Memory Region Status": Defines PMRSTS (Persistent Memory Region Status) at offset E08h and identifies the fields that software must decode at that location. Start at PMRSTS, then map bit ranges to access type, reset value, and field meaning. Evidence index: CBAI, HSTS, NRDY, ERR, PMRSTS, PMRMSCU.CBA, PMRMSCL.CBA, PMRCAP.CMSS.

#### Where this Figure fits

Figure 60 sits in §3.1.4.23 and acts as a register checkpoint. Read it after the report mental model has established the owning object and before software turns CBAI into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a register or property field table. Locate the base offset, verify access width, reset value, and bit range, and only then convert bits into state or capability. Preserve the complete register snapshot so adjacent conditions are not lost by extracting one bit.

#### Teaching redraw

```text
[Locate source: CBAI]
          ↓
[Extract field: HSTS] → [Apply encoding: NRDY]
                                      ↓
[Validate evidence: ERR]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `CBAI` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `HSTS` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `NRDY` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `ERR` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `PMRSTS` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `PMRMSCU.CBA` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.1.4.23 is the applicable context.
2. Decode CBAI at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check HSTS as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 60 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.1.4.23 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes CBAI, HSTS, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.1.4.23, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 60. Annotate the bytes containing CBAI, decode them, and independently verify HSTS. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of CBAI in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand CBAI and state its unit or object scope?
2. Can the reader explain why HSTS is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** CBAI, HSTS, NRDY, ERR, PMRSTS, PMRMSCU.CBA, PMRMSCL.CBA, PMRCAP.CMSS

**Source keyword index:** `shall`, `may`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.23, Figure 60, printed pages 75, PDF pages 101

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 61: Offset E0Ch: PMREBS - Persistent Memory Region Elasticity Buffer Size</strong></summary>

<!-- claim:BASE3-FIG-061-CLAIM figure-table:BASE3-FIG-061 -->

**SPEC.** Figure 61, "Offset E0Ch: PMREBS - Persistent Memory Region Elasticity Buffer Size": Defines PMREBS (Persistent Memory Region Elasticity Buffer Size) at offset E0Ch and identifies the fields that software must decode at that location. Start at PMREBS, then map bit ranges to access type, reset value, and field meaning. Evidence index: PMRWBZ, PMRRBB, PMRSZU, PMREBS, PMR.

#### Where this Figure fits

Figure 61 sits in §3.1.4.24 and acts as a register checkpoint. Read it after the report mental model has established the owning object and before software turns PMRWBZ into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a register or property field table. Locate the base offset, verify access width, reset value, and bit range, and only then convert bits into state or capability. Preserve the complete register snapshot so adjacent conditions are not lost by extracting one bit.

#### Teaching redraw

```text
[Locate source: PMRWBZ]
          ↓
[Extract field: PMRRBB] → [Apply encoding: PMRSZU]
                                      ↓
[Validate evidence: PMREBS]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `PMRWBZ` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `PMRRBB` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `PMRSZU` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `PMREBS` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `PMR` | Persistent Memory Region, a controller-exposed memory region with persistence semantics. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.1.4.24 is the applicable context.
2. Decode PMRWBZ at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check PMRRBB as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 61 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.1.4.24 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes PMRWBZ, PMRRBB, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.1.4.24, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 61. Annotate the bytes containing PMRWBZ, decode them, and independently verify PMRRBB. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of PMRWBZ in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand PMRWBZ and state its unit or object scope?
2. Can the reader explain why PMRRBB is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** PMRWBZ, PMRRBB, PMRSZU, PMREBS, PMR

**Source keyword index:** `shall`, `may`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.24, Figure 61, printed pages 76, PDF pages 102

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 62: Offset E10h: PMRSWTP - Persistent Memory Region Sustained Write Throughput</strong></summary>

<!-- claim:BASE3-FIG-062-CLAIM figure-table:BASE3-FIG-062 -->

**SPEC.** Figure 62, "Offset E10h: PMRSWTP - Persistent Memory Region Sustained Write Throughput": Defines PMRSWTP (Persistent Memory Region Sustained Write Throughput) at offset E10h and identifies the fields that software must decode at that location. Start at PMRSWTP, then map bit ranges to access type, reset value, and field meaning. Evidence index: PMRSWTV, PMRSWTU, PMRSWTP, PMR, TLP, MPS, PXDC.

#### Where this Figure fits

Figure 62 sits in §3.1.4.24 and acts as a register checkpoint. Read it after the report mental model has established the owning object and before software turns PMRSWTV into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a register or property field table. Locate the base offset, verify access width, reset value, and bit range, and only then convert bits into state or capability. Preserve the complete register snapshot so adjacent conditions are not lost by extracting one bit.

#### Teaching redraw

```text
[Locate source: PMRSWTV]
          ↓
[Extract field: PMRSWTU] → [Apply encoding: PMRSWTP]
                                      ↓
[Validate evidence: PMR]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `PMRSWTV` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `PMRSWTU` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `PMRSWTP` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `PMR` | Persistent Memory Region, a controller-exposed memory region with persistence semantics. |
| `TLP` | Transaction Layer Packet, a packet carried by the PCIe transaction layer. |
| `MPS` | Memory Page Size, the controller memory-page-size setting; it affects queue addresses and PRP alignment. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.1.4.24 is the applicable context.
2. Decode PMRSWTV at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check PMRSWTU as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 62 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.1.4.24 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes PMRSWTV, PMRSWTU, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.1.4.24, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 62. Annotate the bytes containing PMRSWTV, decode them, and independently verify PMRSWTU. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of PMRSWTV in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand PMRSWTV and state its unit or object scope?
2. Can the reader explain why PMRSWTU is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** PMRSWTV, PMRSWTU, PMRSWTP, PMR, TLP, MPS, PXDC

**Source keyword index:** `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.24, Figure 62, printed pages 76, PDF pages 102

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 63: Offset E14h: PMRMSCL - Persistent Memory Region Memory Space Control Lower</strong></summary>

<!-- claim:BASE3-FIG-063-CLAIM figure-table:BASE3-FIG-063 -->

**SPEC.** Figure 63, "Offset E14h: PMRMSCL - Persistent Memory Region Memory Space Control Lower": Defines PMRMSCL (Persistent Memory Region Memory Space Control Lower) at offset E14h and identifies the fields that software must decode at that location. Start at PMRMSCL, then map bit ranges to access type, reset value, and field meaning. Evidence index: CBA, CMSE, PMRMSCL, PMRMSCU.CBA.

#### Where this Figure fits

Figure 63 sits in §3.1.4.26 and acts as a register checkpoint. Read it after the report mental model has established the owning object and before software turns CBA into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a register or property field table. Locate the base offset, verify access width, reset value, and bit range, and only then convert bits into state or capability. Preserve the complete register snapshot so adjacent conditions are not lost by extracting one bit.

#### Teaching redraw

```text
[Locate source: CBA]
          ↓
[Extract field: CMSE] → [Apply encoding: PMRMSCL]
                                      ↓
[Validate evidence: PMRMSCU.CBA]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `CBA` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `CMSE` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `PMRMSCL` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `PMRMSCU.CBA` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.1.4.26 is the applicable context.
2. Decode CBA at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check CMSE as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 63 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.1.4.26 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes CBA, CMSE, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.1.4.26, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 63. Annotate the bytes containing CBA, decode them, and independently verify CMSE. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of CBA in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand CBA and state its unit or object scope?
2. Can the reader explain why CMSE is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** CBA, CMSE, PMRMSCL, PMRMSCU.CBA

**Source keyword index:** `shall`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.26, Figure 63, printed pages 77, PDF pages 103

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 64: Offset E18h: PMRMSCU - Persistent Memory Region Memory Space Control Upper</strong></summary>

<!-- claim:BASE3-FIG-064-CLAIM figure-table:BASE3-FIG-064 -->

**SPEC.** Figure 64, "Offset E18h: PMRMSCU - Persistent Memory Region Memory Space Control Upper": Defines PMRMSCU (Persistent Memory Region Memory Space Control Upper) at offset E18h and identifies the fields that software must decode at that location. Start at PMRMSCU, then map bit ranges to access type, reset value, and field meaning. Evidence index: CBA, PMRMSCU.

#### Where this Figure fits

Figure 64 sits in §3.1.4.26 and acts as a register checkpoint. Read it after the report mental model has established the owning object and before software turns CBA into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a register or property field table. Locate the base offset, verify access width, reset value, and bit range, and only then convert bits into state or capability. Preserve the complete register snapshot so adjacent conditions are not lost by extracting one bit.

#### Teaching redraw

```text
[Locate source: CBA]
          ↓
[Extract field: PMRMSCU] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `CBA` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `PMRMSCU` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.1.4.26 is the applicable context.
2. Decode CBA at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check PMRMSCU as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 64 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.1.4.26 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes CBA, PMRMSCU, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.1.4.26, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 64. Annotate the bytes containing CBA, decode them, and independently verify PMRMSCU. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of CBA in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand CBA and state its unit or object scope?
2. Can the reader explain why PMRMSCU is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** CBA, PMRMSCU

**Source keyword index:** none

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.26, Figure 64, printed pages 77, PDF pages 103

</details>

<a id="section-3-2"></a>

### §3.2

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 65: NSID Types and Relationship to Namespace</strong></summary>

<!-- claim:BASE3-FIG-065-CLAIM figure-table:BASE3-FIG-065 -->

**SPEC.** Figure 65, "NSID Types and Relationship to Namespace": Defines the identifier composition or namespace of values shown by NSID Types and Relationship to Namespace. Keep the value width, issuing authority, uniqueness scope, and reserved values separate. Evidence index: NSID, Namespace.

#### Where this Figure fits

Figure 65 sits in §3.2.1 and acts as a hierarchy checkpoint. Read it after the report mental model has established the owning object and before software turns NSID into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is an object or capacity relationship Figure. Separate containment, accessibility, identifier reference, and sharing. Adjacent boxes need not be one-to-one, and an identifier is not the physical or logical object it references.

#### Teaching redraw

```text
[Locate source: NSID]
          ↓
[Extract field: Namespace] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `NSID` | Namespace Identifier, a controller-visible numeric handle for a namespace; the identifier is not the namespace object itself. |
| `Namespace` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.2.1 is the applicable context.
2. Decode NSID at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check Namespace as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 65 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.2.1 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes NSID, Namespace, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.2.1, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 65. Annotate the bytes containing NSID, decode them, and independently verify Namespace. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

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
2. Can the reader explain why Namespace is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** NSID, Namespace

**Source keyword index:** none

> Source: NVME-BASE-2.4, Rev. 2.4, §3.2.1, Figure 65, printed pages 78-79, PDF pages 104-105

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 66: NSID Types</strong></summary>

<!-- claim:BASE3-FIG-066-CLAIM figure-table:BASE3-FIG-066 -->

**SPEC.** Figure 66, "NSID Types": Defines the identifier composition or namespace of values shown by NSID Types. Keep the value width, issuing authority, uniqueness scope, and reserved values separate. Evidence index: NSID.

#### Where this Figure fits

Figure 66 sits in §3.2.1.5 and acts as a relationship checkpoint. Read it after the report mental model has established the owning object and before software turns NSID into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This Figure explains a specific relationship or example. Identify each component type and owner, then decide whether each connection represents data flow, control flow, containment, or a condition. Visual placement alone creates no normative requirement.

#### Teaching redraw

```text
[Locate source: NSID]
          ↓
[Extract field: evidence] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `NSID` | Namespace Identifier, a controller-visible numeric handle for a namespace; the identifier is not the namespace object itself. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.2.1.5 is the applicable context.
2. Decode NSID at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check the cited condition as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 66 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.2.1.5 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes NSID, the cited condition, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.2.1.5, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 66. Annotate the bytes containing NSID, decode them, and independently verify the cited condition. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

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
2. Can the reader explain why the cited condition is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** NSID

**Source keyword index:** none

> Source: NVME-BASE-2.4, Rev. 2.4, §3.2.1.5, Figure 66, printed pages 79, PDF pages 105

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 67: NVM Sets and Associated Namespaces</strong></summary>

<!-- claim:BASE3-FIG-067-CLAIM figure-table:BASE3-FIG-067 -->

**SPEC.** Figure 67, "NVM Sets and Associated Namespaces": Shows the object or capacity relationships in NVM Sets and Associated Namespaces. Separate logical identifiers from controllers, namespaces, ports, and capacity containers. Evidence index: NVM Set, Namespace.

#### Where this Figure fits

Figure 67 sits in §3.2.2 and acts as a hierarchy checkpoint. Read it after the report mental model has established the owning object and before software turns NVM Set into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is an object or capacity relationship Figure. Separate containment, accessibility, identifier reference, and sharing. Adjacent boxes need not be one-to-one, and an identifier is not the physical or logical object it references.

#### Teaching redraw

```text
[Locate source: NVM Set]
          ↓
[Extract field: Namespace] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `NVM Set` | NVM Set, a capacity grouping that associates namespaces with a managed set of NVM resources. |
| `Namespace` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.2.2 is the applicable context.
2. Decode NVM Set at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check Namespace as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 67 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.2.2 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes NVM Set, Namespace, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.2.2, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 67. Annotate the bytes containing NVM Set, decode them, and independently verify Namespace. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of NVM Set in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand NVM Set and state its unit or object scope?
2. Can the reader explain why Namespace is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** NVM Set, Namespace

**Source keyword index:** none

> Source: NVME-BASE-2.4, Rev. 2.4, §3.2.2, Figure 67, printed pages 81, PDF pages 107

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 68: NVM Set Aware Admin Commands</strong></summary>

<!-- claim:BASE3-FIG-068-CLAIM figure-table:BASE3-FIG-068 -->

**SPEC.** Figure 68, "NVM Set Aware Admin Commands": Shows the object or capacity relationships in NVM Set Aware Admin Commands. Separate logical identifiers from controllers, namespaces, ports, and capacity containers. Evidence index: NVM Set, Command.

#### Where this Figure fits

Figure 68 sits in §3.2.2 and acts as a hierarchy checkpoint. Read it after the report mental model has established the owning object and before software turns NVM Set into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is an object or capacity relationship Figure. Separate containment, accessibility, identifier reference, and sharing. Adjacent boxes need not be one-to-one, and an identifier is not the physical or logical object it references.

#### Teaching redraw

```text
[Locate source: NVM Set]
          ↓
[Extract field: Command] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `NVM Set` | NVM Set, a capacity grouping that associates namespaces with a managed set of NVM resources. |
| `Command` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.2.2 is the applicable context.
2. Decode NVM Set at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check Command as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 68 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.2.2 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes NVM Set, Command, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.2.2, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 68. Annotate the bytes containing NVM Set, decode them, and independently verify Command. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of NVM Set in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand NVM Set and state its unit or object scope?
2. Can the reader explain why Command is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** NVM Set, Command

**Source keyword index:** none

> Source: NVME-BASE-2.4, Rev. 2.4, §3.2.2, Figure 68, printed pages 81, PDF pages 107

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 69: NVM Sets and Associated Namespaces</strong></summary>

<!-- claim:BASE3-FIG-069-CLAIM figure-table:BASE3-FIG-069 -->

**SPEC.** Figure 69, "NVM Sets and Associated Namespaces": Shows the object or capacity relationships in NVM Sets and Associated Namespaces. Separate logical identifiers from controllers, namespaces, ports, and capacity containers. Evidence index: NVM Set, Namespace.

#### Where this Figure fits

Figure 69 sits in §3.2.3 and acts as a hierarchy checkpoint. Read it after the report mental model has established the owning object and before software turns NVM Set into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is an object or capacity relationship Figure. Separate containment, accessibility, identifier reference, and sharing. Adjacent boxes need not be one-to-one, and an identifier is not the physical or logical object it references.

#### Teaching redraw

```text
[Locate source: NVM Set]
          ↓
[Extract field: Namespace] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `NVM Set` | NVM Set, a capacity grouping that associates namespaces with a managed set of NVM resources. |
| `Namespace` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.2.3 is the applicable context.
2. Decode NVM Set at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check Namespace as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 69 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.2.3 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes NVM Set, Namespace, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.2.3, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 69. Annotate the bytes containing NVM Set, decode them, and independently verify Namespace. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of NVM Set in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand NVM Set and state its unit or object scope?
2. Can the reader explain why Namespace is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** NVM Set, Namespace

**Source keyword index:** none

> Source: NVME-BASE-2.4, Rev. 2.4, §3.2.3, Figure 69, printed pages 83, PDF pages 109

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 70: Flexible Data Placement Logical View of Non-Volatile Storage</strong></summary>

<!-- claim:BASE3-FIG-070-CLAIM figure-table:BASE3-FIG-070 -->

**SPEC.** Figure 70, "Flexible Data Placement Logical View of Non-Volatile Storage": Shows the object or capacity relationships in Flexible Data Placement Logical View of Non-Volatile Storage. Separate logical identifiers from controllers, namespaces, ports, and capacity containers. Evidence index: Flexible Data Placement Logical View of Non-Volatile Storage.

#### Where this Figure fits

Figure 70 sits in §3.2.4 and acts as a relationship checkpoint. Read it after the report mental model has established the owning object and before software turns Flexible Data Placement Logical View of Non-Volatile Storage into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This Figure explains a specific relationship or example. Identify each component type and owner, then decide whether each connection represents data flow, control flow, containment, or a condition. Visual placement alone creates no normative requirement.

#### Teaching redraw

```text
[Locate source: Flexible Data Placement Logical View of Non-Volatile Storage]
          ↓
[Extract field: evidence] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `Flexible Data Placement Logical View of Non-Volatile Storage` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.2.4 is the applicable context.
2. Decode Flexible Data Placement Logical View of Non-Volatile Storage at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check the cited condition as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 70 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.2.4 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes Flexible Data Placement Logical View of Non-Volatile Storage, the cited condition, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.2.4, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 70. Annotate the bytes containing Flexible Data Placement Logical View of Non-Volatile Storage, decode them, and independently verify the cited condition. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of Flexible Data Placement Logical View of Non-Volatile Storage in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand Flexible Data Placement Logical View of Non-Volatile Storage and state its unit or object scope?
2. Can the reader explain why the cited condition is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** Flexible Data Placement Logical View of Non-Volatile Storage

**Source keyword index:** none

> Source: NVME-BASE-2.4, Rev. 2.4, §3.2.4, Figure 70, printed pages 85, PDF pages 111

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 71: Example 1 Domain Structure</strong></summary>

<!-- claim:BASE3-FIG-071-CLAIM figure-table:BASE3-FIG-071 -->

**SPEC.** Figure 71, "Example 1 Domain Structure": Defines the concrete layout or value relationships for Example 1 Domain Structure. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is Domain.

#### Where this Figure fits

Figure 71 sits in §3.2.5.1 and acts as a hierarchy checkpoint. Read it after the report mental model has established the owning object and before software turns Domain into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is an object or capacity relationship Figure. Separate containment, accessibility, identifier reference, and sharing. Adjacent boxes need not be one-to-one, and an identifier is not the physical or logical object it references.

#### Teaching redraw

```text
[Locate source: Domain]
          ↓
[Extract field: evidence] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `Domain` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.2.5.1 is the applicable context.
2. Decode Domain at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check the cited condition as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 71 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.2.5.1 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes Domain, the cited condition, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.2.5.1, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 71. Annotate the bytes containing Domain, decode them, and independently verify the cited condition. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of Domain in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand Domain and state its unit or object scope?
2. Can the reader explain why the cited condition is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** Domain

**Source keyword index:** none

> Source: NVME-BASE-2.4, Rev. 2.4, §3.2.5.1, Figure 71, printed pages 86, PDF pages 112

</details>

<a id="section-3-3"></a>

### §3.3

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 73: Empty Queue Definition</strong></summary>

<!-- claim:BASE3-FIG-073-CLAIM figure-table:BASE3-FIG-073 -->

**SPEC.** Figure 73, "Empty Queue Definition": Defines the concrete layout or value relationships for Empty Queue Definition. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is Empty Queue Definition.

#### Where this Figure fits

Figure 73 sits in §3.3.1.4 and acts as a queue checkpoint. Read it after the report mental model has established the owning object and before software turns Empty Queue Definition into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a queue or command-flow Figure. Label host and controller ownership first, then trace head, tail, phase, or arbitration changes. An arrow represents a state or ownership transition and does not automatically prove command completion.

#### Teaching redraw

```text
[Locate source: Empty Queue Definition]
          ↓
[Extract field: evidence] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `Empty Queue Definition` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.3.1.4 is the applicable context.
2. Decode Empty Queue Definition at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check the cited condition as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 73 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.3.1.4 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes Empty Queue Definition, the cited condition, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.3.1.4, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 73. Annotate the bytes containing Empty Queue Definition, decode them, and independently verify the cited condition. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of Empty Queue Definition in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand Empty Queue Definition and state its unit or object scope?
2. Can the reader explain why the cited condition is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** Empty Queue Definition

**Source keyword index:** `shall`

> Source: NVME-BASE-2.4, Rev. 2.4, §3.3.1.4, Figure 73, printed pages 91, PDF pages 117

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 74: Full Queue Definition</strong></summary>

<!-- claim:BASE3-FIG-074-CLAIM figure-table:BASE3-FIG-074 -->

**SPEC.** Figure 74, "Full Queue Definition": Defines the concrete layout or value relationships for Full Queue Definition. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is Full Queue Definition.

#### Where this Figure fits

Figure 74 sits in §3.3.1.4 and acts as a queue checkpoint. Read it after the report mental model has established the owning object and before software turns Full Queue Definition into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a queue or command-flow Figure. Label host and controller ownership first, then trace head, tail, phase, or arbitration changes. An arrow represents a state or ownership transition and does not automatically prove command completion.

#### Teaching redraw

```text
[Locate source: Full Queue Definition]
          ↓
[Extract field: evidence] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `Full Queue Definition` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.3.1.4 is the applicable context.
2. Decode Full Queue Definition at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check the cited condition as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 74 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.3.1.4 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes Full Queue Definition, the cited condition, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.3.1.4, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 74. Annotate the bytes containing Full Queue Definition, decode them, and independently verify the cited condition. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of Full Queue Definition in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand Full Queue Definition and state its unit or object scope?
2. Can the reader explain why the cited condition is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** Full Queue Definition

**Source keyword index:** none

> Source: NVME-BASE-2.4, Rev. 2.4, §3.3.1.4, Figure 74, printed pages 91, PDF pages 117

</details>

<a id="section-3-4"></a>

### §3.4

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 80: Round Robin Arbitration</strong></summary>

<!-- claim:BASE3-FIG-080-CLAIM figure-table:BASE3-FIG-080 -->

**SPEC.** Figure 80, "Round Robin Arbitration": Shows how Round Robin Arbitration selects work from competing Submission Queues. Track priority class, service order, and the point at which the arbiter selects the next command. Evidence index: Round Robin Arbitration.

#### Where this Figure fits

Figure 80 sits in §3.4.4 and acts as a queue checkpoint. Read it after the report mental model has established the owning object and before software turns Round Robin Arbitration into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a queue or command-flow Figure. Label host and controller ownership first, then trace head, tail, phase, or arbitration changes. An arrow represents a state or ownership transition and does not automatically prove command completion.

#### Teaching redraw

```text
[Locate source: Round Robin Arbitration]
          ↓
[Extract field: evidence] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `Round Robin Arbitration` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.4.4 is the applicable context.
2. Decode Round Robin Arbitration at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check the cited condition as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 80 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.4.4 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes Round Robin Arbitration, the cited condition, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.4.4, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 80. Annotate the bytes containing Round Robin Arbitration, decode them, and independently verify the cited condition. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of Round Robin Arbitration in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand Round Robin Arbitration and state its unit or object scope?
2. Can the reader explain why the cited condition is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** Round Robin Arbitration

**Source keyword index:** none

> Source: NVME-BASE-2.4, Rev. 2.4, §3.4.4, Figure 80, printed pages 103, PDF pages 129

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 81: Weighted Round Robin with Urgent Priority Class Arbitration</strong></summary>

<!-- claim:BASE3-FIG-081-CLAIM figure-table:BASE3-FIG-081 -->

**SPEC.** Figure 81, "Weighted Round Robin with Urgent Priority Class Arbitration": Shows how Weighted Round Robin with Urgent Priority Class Arbitration selects work from competing Submission Queues. Track priority class, service order, and the point at which the arbiter selects the next command. Evidence index: Weighted Round Robin with Urgent Priority Class Arbitration.

#### Where this Figure fits

Figure 81 sits in §3.4.4.2 and acts as a queue checkpoint. Read it after the report mental model has established the owning object and before software turns Weighted Round Robin with Urgent Priority Class Arbitration into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a queue or command-flow Figure. Label host and controller ownership first, then trace head, tail, phase, or arbitration changes. An arrow represents a state or ownership transition and does not automatically prove command completion.

#### Teaching redraw

```text
[Locate source: Weighted Round Robin with Urgent Priority Class Arbitration]
          ↓
[Extract field: evidence] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `Weighted Round Robin with Urgent Priority Class Arbitration` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.4.4.2 is the applicable context.
2. Decode Weighted Round Robin with Urgent Priority Class Arbitration at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check the cited condition as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 81 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.4.4.2 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes Weighted Round Robin with Urgent Priority Class Arbitration, the cited condition, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.4.4.2, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 81. Annotate the bytes containing Weighted Round Robin with Urgent Priority Class Arbitration, decode them, and independently verify the cited condition. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of Weighted Round Robin with Urgent Priority Class Arbitration in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand Weighted Round Robin with Urgent Priority Class Arbitration and state its unit or object scope?
2. Can the reader explain why the cited condition is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** Weighted Round Robin with Urgent Priority Class Arbitration

**Source keyword index:** none

> Source: NVME-BASE-2.4, Rev. 2.4, §3.4.4.2, Figure 81, printed pages 104, PDF pages 130

</details>

<a id="section-3-5"></a>

### §3.5

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 84: Admin Commands Permitted to Return a Status Code of Admin Command Media Not</strong></summary>

<!-- claim:BASE3-FIG-084-CLAIM figure-table:BASE3-FIG-084 -->

**SPEC.** Figure 84, "Admin Commands Permitted to Return a Status Code of Admin Command Media Not": Defines the status/error classification represented by Admin Commands Permitted to Return a Status Code of Admin Command Media Not. Resolve the category before the individual code or flag; keep reserved values uninterpreted. Evidence index: LBA, TCG, CAP.CRMS, CAP.CRMS.CRWMS, CAP.CRMS.CRIMS, CC.CRIME, Status Code, Command.

#### Where this Figure fits

Figure 84 sits in §3.5.3 and acts as a status checkpoint. Read it after the report mental model has established the owning object and before software turns LBA into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a status or error classification. Identify the containing structure and category before decoding the individual code, control bits, and retry indication. Reserved values remain uninterpreted, and a similar name does not map the code into another error layer.

#### Teaching redraw

```text
[Locate source: LBA]
          ↓
[Extract field: TCG] → [Apply encoding: CAP.CRMS]
                                      ↓
[Validate evidence: CAP.CRMS.CRWMS]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `LBA` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `TCG` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `CAP.CRMS` | Controller Capabilities, the controller property at offset 00h that reports queue, page-size, timeout, and other capabilities. Here CAP.CRMS selects its CRMS member field. |
| `CAP.CRMS.CRWMS` | Controller Capabilities, the controller property at offset 00h that reports queue, page-size, timeout, and other capabilities. Here CAP.CRMS.CRWMS selects its CRMS.CRWMS member field. |
| `CAP.CRMS.CRIMS` | Controller Capabilities, the controller property at offset 00h that reports queue, page-size, timeout, and other capabilities. Here CAP.CRMS.CRIMS selects its CRMS.CRIMS member field. |
| `CC.CRIME` | Controller Configuration, the property through which the host selects settings and enables or disables a controller. Here CC.CRIME selects its CRIME member field. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.5.3 is the applicable context.
2. Decode LBA at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check TCG as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 84 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.5.3 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes LBA, TCG, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.5.3, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 84. Annotate the bytes containing LBA, decode them, and independently verify TCG. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of LBA in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand LBA and state its unit or object scope?
2. Can the reader explain why TCG is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** LBA, TCG, CAP.CRMS, CAP.CRMS.CRWMS, CAP.CRMS.CRIMS, CC.CRIME, Status Code, Command

**Source keyword index:** `shall`, `should`, `may`

> Source: NVME-BASE-2.4, Rev. 2.4, §3.5.3, Figure 84, printed pages 110-111, PDF pages 136-137

</details>

<a id="section-3-6"></a>

### §3.6

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 85: Shutdown Processing Interactions</strong></summary>

<!-- claim:BASE3-FIG-085-CLAIM figure-table:BASE3-FIG-085 -->

**SPEC.** Figure 85, "Shutdown Processing Interactions": Shows the state or timing progression represented by Shutdown Processing Interactions. Follow the states or time bounds in arrow order and identify which actor observes each transition. Evidence index: Shutdown Processing Interactions.

#### Where this Figure fits

Figure 85 sits in §3.6 and acts as a state checkpoint. Read it after the report mental model has established the owning object and before software turns Shutdown Processing Interactions into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a state or timing Figure. Follow each arrow while recording trigger, observer, completion condition, and timeout source. Similar state names under different reset scopes do not imply preservation of the same queue or controller state.

#### Teaching redraw

```text
[Locate source: Shutdown Processing Interactions]
          ↓
[Extract field: evidence] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `Shutdown Processing Interactions` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.6 is the applicable context.
2. Decode Shutdown Processing Interactions at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check the cited condition as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 85 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.6 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes Shutdown Processing Interactions, the cited condition, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.6, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 85. Annotate the bytes containing Shutdown Processing Interactions, decode them, and independently verify the cited condition. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of Shutdown Processing Interactions in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand Shutdown Processing Interactions and state its unit or object scope?
2. Can the reader explain why the cited condition is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** Shutdown Processing Interactions

**Source keyword index:** none

> Source: NVME-BASE-2.4, Rev. 2.4, §3.6, Figure 85, printed pages 113, PDF pages 139

</details>

<a id="section-3-8"></a>

### §3.8

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 86: Simple NVM Subsystem</strong></summary>

<!-- claim:BASE3-FIG-086-CLAIM figure-table:BASE3-FIG-086 -->

**SPEC.** Figure 86, "Simple NVM Subsystem": Shows the object or capacity relationships in Simple NVM Subsystem. Separate logical identifiers from controllers, namespaces, ports, and capacity containers. Evidence index: NVM Subsystem.

#### Where this Figure fits

Figure 86 sits in §3.8.2 and acts as a hierarchy checkpoint. Read it after the report mental model has established the owning object and before software turns NVM Subsystem into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is an object or capacity relationship Figure. Separate containment, accessibility, identifier reference, and sharing. Adjacent boxes need not be one-to-one, and an identifier is not the physical or logical object it references.

#### Teaching redraw

```text
[Locate source: NVM Subsystem]
          ↓
[Extract field: evidence] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `NVM Subsystem` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.8.2 is the applicable context.
2. Decode NVM Subsystem at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check the cited condition as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 86 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.8.2 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes NVM Subsystem, the cited condition, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.8.2, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 86. Annotate the bytes containing NVM Subsystem, decode them, and independently verify the cited condition. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of NVM Subsystem in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand NVM Subsystem and state its unit or object scope?
2. Can the reader explain why the cited condition is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** NVM Subsystem

**Source keyword index:** none

> Source: NVME-BASE-2.4, Rev. 2.4, §3.8.2, Figure 86, printed pages 126, PDF pages 152

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 87: Vertically-Organized NVM Subsystem</strong></summary>

<!-- claim:BASE3-FIG-087-CLAIM figure-table:BASE3-FIG-087 -->

**SPEC.** Figure 87, "Vertically-Organized NVM Subsystem": Shows the object or capacity relationships in Vertically-Organized NVM Subsystem. Separate logical identifiers from controllers, namespaces, ports, and capacity containers. Evidence index: NVM Subsystem.

#### Where this Figure fits

Figure 87 sits in §3.8.2.2 and acts as a hierarchy checkpoint. Read it after the report mental model has established the owning object and before software turns NVM Subsystem into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is an object or capacity relationship Figure. Separate containment, accessibility, identifier reference, and sharing. Adjacent boxes need not be one-to-one, and an identifier is not the physical or logical object it references.

#### Teaching redraw

```text
[Locate source: NVM Subsystem]
          ↓
[Extract field: evidence] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `NVM Subsystem` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.8.2.2 is the applicable context.
2. Decode NVM Subsystem at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check the cited condition as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 87 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.8.2.2 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes NVM Subsystem, the cited condition, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.8.2.2, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 87. Annotate the bytes containing NVM Subsystem, decode them, and independently verify the cited condition. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of NVM Subsystem in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand NVM Subsystem and state its unit or object scope?
2. Can the reader explain why the cited condition is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** NVM Subsystem

**Source keyword index:** none

> Source: NVME-BASE-2.4, Rev. 2.4, §3.8.2.2, Figure 87, printed pages 127, PDF pages 153

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 88: Horizontally-Organized Dual NAND NVM Subsystem</strong></summary>

<!-- claim:BASE3-FIG-088-CLAIM figure-table:BASE3-FIG-088 -->

**SPEC.** Figure 88, "Horizontally-Organized Dual NAND NVM Subsystem": Shows the object or capacity relationships in Horizontally-Organized Dual NAND NVM Subsystem. Separate logical identifiers from controllers, namespaces, ports, and capacity containers. Evidence index: NAND, NVM Subsystem.

#### Where this Figure fits

Figure 88 sits in §3.8.2.3 and acts as a hierarchy checkpoint. Read it after the report mental model has established the owning object and before software turns NAND into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is an object or capacity relationship Figure. Separate containment, accessibility, identifier reference, and sharing. Adjacent boxes need not be one-to-one, and an identifier is not the physical or logical object it references.

#### Teaching redraw

```text
[Locate source: NAND]
          ↓
[Extract field: NVM Subsystem] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `NAND` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `NVM Subsystem` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.8.2.3 is the applicable context.
2. Decode NAND at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check NVM Subsystem as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 88 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.8.2.3 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes NAND, NVM Subsystem, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.8.2.3, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 88. Annotate the bytes containing NAND, decode them, and independently verify NVM Subsystem. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of NAND in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand NAND and state its unit or object scope?
2. Can the reader explain why NVM Subsystem is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** NAND, NVM Subsystem

**Source keyword index:** none

> Source: NVME-BASE-2.4, Rev. 2.4, §3.8.2.3, Figure 88, printed pages 128, PDF pages 154

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 89: Capacity Information Field Usage</strong></summary>

<!-- claim:BASE3-FIG-089-CLAIM figure-table:BASE3-FIG-089 -->

**SPEC.** Figure 89, "Capacity Information Field Usage": Defines the concrete layout or value relationships for Capacity Information Field Usage. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is TNVMCAP, UNVMCAP, MEGCAP, TEGCAP, UEGCAP.

#### Where this Figure fits

Figure 89 sits in §3.8.3 and acts as a hierarchy checkpoint. Read it after the report mental model has established the owning object and before software turns TNVMCAP into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is an object or capacity relationship Figure. Separate containment, accessibility, identifier reference, and sharing. Adjacent boxes need not be one-to-one, and an identifier is not the physical or logical object it references.

#### Teaching redraw

```text
[Locate source: TNVMCAP]
          ↓
[Extract field: UNVMCAP] → [Apply encoding: MEGCAP]
                                      ↓
[Validate evidence: TEGCAP]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `TNVMCAP` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `UNVMCAP` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `MEGCAP` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `TEGCAP` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `UEGCAP` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.8.3 is the applicable context.
2. Decode TNVMCAP at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check UNVMCAP as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 89 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.8.3 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes TNVMCAP, UNVMCAP, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.8.3, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 89. Annotate the bytes containing TNVMCAP, decode them, and independently verify UNVMCAP. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of TNVMCAP in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand TNVMCAP and state its unit or object scope?
2. Can the reader explain why UNVMCAP is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** TNVMCAP, UNVMCAP, MEGCAP, TEGCAP, UEGCAP

**Source keyword index:** none

> Source: NVME-BASE-2.4, Rev. 2.4, §3.8.3, Figure 89, printed pages 129, PDF pages 155

</details>

<a id="section-3-9"></a>

### §3.9

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 90: Detecting Timeout Takes up to 2 * KATT</strong></summary>

<!-- claim:BASE3-FIG-090-CLAIM figure-table:BASE3-FIG-090 -->

**SPEC.** Figure 90, "Detecting Timeout Takes up to 2 * KATT": Shows the state or timing progression represented by Detecting Timeout Takes up to 2 * KATT. Follow the states or time bounds in arrow order and identify which actor observes each transition. Evidence index: KATT.

#### Where this Figure fits

Figure 90 sits in §3.9.4.1 and acts as a state checkpoint. Read it after the report mental model has established the owning object and before software turns KATT into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a state or timing Figure. Follow each arrow while recording trigger, observer, completion condition, and timeout source. Similar state names under different reset scopes do not imply preservation of the same queue or controller state.

#### Teaching redraw

```text
[Locate source: KATT]
          ↓
[Extract field: evidence] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `KATT` | Keep Alive Timeout Total, the controller timing basis for detecting a keep-alive timeout. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.9.4.1 is the applicable context.
2. Decode KATT at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check the cited condition as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 90 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.9.4.1 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes KATT, the cited condition, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.9.4.1, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 90. Annotate the bytes containing KATT, decode them, and independently verify the cited condition. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of KATT in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand KATT and state its unit or object scope?
2. Can the reader explain why the cited condition is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** KATT

**Source keyword index:** none

> Source: NVME-BASE-2.4, Rev. 2.4, §3.9.4.1, Figure 90, printed pages 133, PDF pages 159

</details>

<a id="section-3-10"></a>

### §3.10

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 91: Example Privileged Action Admin Commands</strong></summary>

<!-- claim:BASE3-FIG-091-CLAIM figure-table:BASE3-FIG-091 -->

**SPEC.** Figure 91, "Example Privileged Action Admin Commands": Identifies the privileged-operation boundary illustrated by Example Privileged Action Admin Commands. Separate the requesting command from the privilege or controller state that authorizes it. Evidence index: Command.

#### Where this Figure fits

Figure 91 sits in §3.10 and acts as a relationship checkpoint. Read it after the report mental model has established the owning object and before software turns Command into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This Figure explains a specific relationship or example. Identify each component type and owner, then decide whether each connection represents data flow, control flow, containment, or a condition. Visual placement alone creates no normative requirement.

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

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.10 is the applicable context.
2. Decode Command at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check the cited condition as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 91 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.10 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes Command, the cited condition, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.10, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 91. Annotate the bytes containing Command, decode them, and independently verify the cited condition. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

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

> Source: NVME-BASE-2.4, Rev. 2.4, §3.10, Figure 91, printed pages 135, PDF pages 161

</details>

## Use and limitations

Use the claim IDs as stable PPT traceability keys. Re-check affected claims if the source revision, errata set, or approved scope changes.

## Self-questions and worked answers

20 answered questions revisit this report's scope. Each answer retains the same source links as the teaching module; calculations and debugging examples are informative.

### Q01. What is the governing interpretation for “Separate controller type, identity, and capability first”?

<!-- qa:base-ch3-identity-lead -->

**Answer.**

Controller type answers what work a controller can perform, Controller ID answers which controller it is, and support-requirement Figures answer the required support level of a command, log, or feature in a particular context. Figures 23-32 belong in one reading sequence, but the three questions cannot be collapsed into one Boolean.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.1, printed pages 38, PDF pages 64; Source: NVME-BASE-2.4, Rev. 2.4, §3.1.3-3.1.3.2, printed pages 39-43, PDF pages 65-69; Source: NVME-BASE-2.4, Rev. 2.4, §3.1.3, printed pages 40, PDF pages 66

### Q02. Which concepts or conditions must be distinguished in “Separate controller type, identity, and capability first”?

<!-- qa:base-ch3-identity-rows -->

**Answer.**

- I/O controller — Can execute user-data I/O — Optional capabilities still require individual checks
- Administrative controller — Management purpose without data I/O commands — An Admin Queue does not make it an I/O controller
- Support marker — Expresses support strength for a row and context — Never decode it without its column and footnote

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.1, printed pages 38, PDF pages 64; Source: NVME-BASE-2.4, Rev. 2.4, §3.1.3-3.1.3.2, printed pages 39-43, PDF pages 65-69; Source: NVME-BASE-2.4, Rev. 2.4, §3.1.3, printed pages 40, PDF pages 66

### Q03. How does “Separate controller type, identity, and capability first” apply to a concrete calculation or operational scenario?

<!-- qa:base-ch3-identity-example -->

**Answer.**

Informative example: after detecting an Administrative controller, software still creates the Admin SQ/CQ and performs management commands, but it must not attach a namespace data path to that controller. Classifying by the mere presence of an Admin Queue incorrectly merges I/O and Administrative controllers.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.1, printed pages 38, PDF pages 64; Source: NVME-BASE-2.4, Rev. 2.4, §3.1.3-3.1.3.2, printed pages 39-43, PDF pages 65-69; Source: NVME-BASE-2.4, Rev. 2.4, §3.1.3, printed pages 40, PDF pages 66

### Q04. What misinterpretation is most likely in “Separate controller type, identity, and capability first”, and how is it debugged?

<!-- qa:base-ch3-identity-pitfall -->

**Answer.**

A capability-matrix parser must preserve row, column, footnote, and controller type. Promoting an O, M, or conditional note into a global capability creates incorrect results in another controller or command-set context.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.1, printed pages 38, PDF pages 64; Source: NVME-BASE-2.4, Rev. 2.4, §3.1.3-3.1.3.2, printed pages 39-43, PDF pages 65-69; Source: NVME-BASE-2.4, Rev. 2.4, §3.1.3, printed pages 40, PDF pages 66

### Q05. What is the governing interpretation for “From CAP to CSTS.RDY: initialization is a state machine with preconditions”?

<!-- qa:base-ch3-properties-init-lead -->

**Answer.**

Properties are not an independent register list. CAP constrains page-size, queue, and timeout capabilities; AQA, ASQ, and ACQ establish Admin queues; CC selects settings and enables the controller; CSTS.RDY finally declares readiness for normal command processing. Figures 33-46 and Figure 57 should be read along this causal chain.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4, printed pages 52-54, PDF pages 78-80; Source: NVME-BASE-2.4, Rev. 2.4, §3.5.1, 3.5.3-3.5.4, printed pages 105-113, PDF pages 131-139

### Q06. Which concepts or conditions must be distinguished in “From CAP to CSTS.RDY: initialization is a state machine with preconditions”?

<!-- qa:base-ch3-properties-init-rows -->

**Answer.**

- CAP — Capabilities and limits — Read before writing configuration
- AQA/ASQ/ACQ — Admin-queue sizes and addresses — Must match page and alignment capabilities
- CC — Host selections and enable — Written values must be compatible with CAP
- CSTS — Controller-reported state — RDY, CFS, and SHST are not interchangeable

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4, printed pages 52-54, PDF pages 78-80; Source: NVME-BASE-2.4, Rev. 2.4, §3.5.1, 3.5.3-3.5.4, printed pages 105-113, PDF pages 131-139

### Q07. How does “From CAP to CSTS.RDY: initialization is a state machine with preconditions” apply to a concrete calculation or operational scenario?

<!-- qa:base-ch3-properties-init-example -->

**Answer.**

Informative example: the host selects a 4 KiB MPS, so ASQ and ACQ base addresses must obey that page-size alignment. After writing CC.EN=1, the host waits for CSTS.RDY=1 within the CAP/CRTO time bound. If CFS appears first, the flow enters error recovery rather than creating I/O queues.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4, printed pages 52-54, PDF pages 78-80; Source: NVME-BASE-2.4, Rev. 2.4, §3.5.1, 3.5.3-3.5.4, printed pages 105-113, PDF pages 131-139

### Q08. What misinterpretation is most likely in “From CAP to CSTS.RDY: initialization is a state machine with preconditions”, and how is it debugged?

<!-- qa:base-ch3-properties-init-pitfall -->

**Answer.**

Initialization logs should retain offset, width, raw value, and timestamp for each property access. A single 'enable failed' message cannot distinguish incompatible settings, address alignment, CFS, or a ready transition still within its timeout.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4, printed pages 52-54, PDF pages 78-80; Source: NVME-BASE-2.4, Rev. 2.4, §3.5.1, 3.5.3-3.5.4, printed pages 105-113, PDF pages 131-139

### Q09. What is the governing interpretation for “Separate ring-buffer state, doorbells, and arbitration”?

<!-- qa:base-ch3-queue-arbitration-lead -->

**Answer.**

Figures 73 and 74 define empty/full state for a queue, while Figures 80 and 81 define arbitration among SQs competing for controller service. The first problem concerns head/tail state within one ring; the second selects among candidate SQs. Priority belongs to the SQ, not to each command as an independent priority.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.3.1, printed pages 88-91, PDF pages 114-117; Source: NVME-BASE-2.4, Rev. 2.4, §3.4.1-3.4.5, printed pages 101-105, PDF pages 127-131; Source: NVME-BASE-2.4, Rev. 2.4, §3.1.3, printed pages 40, PDF pages 66

### Q10. Which concepts or conditions must be distinguished in “Separate ring-buffer state, doorbells, and arbitration”?

<!-- qa:base-ch3-queue-arbitration-rows -->

**Answer.**

- Empty — Head equals tail under the empty ownership definition — No entry can be fetched
- Full — The next tail would reach an unreleased head — The host must not overwrite an entry
- Round Robin — Candidate SQs take turns receiving service — Completion order is not submission order
- Weighted RR + Urgent — Priority class and weight influence selection — Interpret only under the applicable configuration

> Source: NVME-BASE-2.4, Rev. 2.4, §3.3.1, printed pages 88-91, PDF pages 114-117; Source: NVME-BASE-2.4, Rev. 2.4, §3.4.1-3.4.5, printed pages 101-105, PDF pages 127-131; Source: NVME-BASE-2.4, Rev. 2.4, §3.1.3, printed pages 40, PDF pages 66

### Q11. How does “Separate ring-buffer state, doorbells, and arbitration” apply to a concrete calculation or operational scenario?

<!-- qa:base-ch3-queue-arbitration-example -->

**Answer.**

Informative example: an SQ of depth four has four slots, but full/empty detection still needs the ownership rule; an unsigned tail-minus-head value alone is insufficient. If SQ 1 and SQ 2 both contain commands, selecting SQ 2 first does not guarantee its command completes first because execution times may differ.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.3.1, printed pages 88-91, PDF pages 114-117; Source: NVME-BASE-2.4, Rev. 2.4, §3.4.1-3.4.5, printed pages 101-105, PDF pages 127-131; Source: NVME-BASE-2.4, Rev. 2.4, §3.1.3, printed pages 40, PDF pages 66

### Q12. What misinterpretation is most likely in “Separate ring-buffer state, doorbells, and arbitration”, and how is it debugged?

<!-- qa:base-ch3-queue-arbitration-pitfall -->

**Answer.**

During debugging, record the software tail, doorbell value, controller-consumed head, and completion SQHD separately. Combining them into one 'queue index' hides distinct root causes such as a lost doorbell, stale head, premature slot reuse, or arbitration starvation.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.3.1, printed pages 88-91, PDF pages 114-117; Source: NVME-BASE-2.4, Rev. 2.4, §3.4.1-3.4.5, printed pages 101-105, PDF pages 127-131; Source: NVME-BASE-2.4, Rev. 2.4, §3.1.3, printed pages 40, PDF pages 66

### Q13. What is the governing interpretation for “CMB, PMR, capacity, and namespaces are different resource views”?

<!-- qa:base-ch3-memory-capacity-lead -->

**Answer.**

CMB and PMR properties describe the location, capability, and state of controller-exposed memory regions; capacity Figures 86-89 describe available or allocated capacity at NVM-subsystem levels. Both concern memory, but they are different spaces and cannot be merged into one free-capacity value.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4, printed pages 52-54, PDF pages 78-80; Source: NVME-BASE-2.4, Rev. 2.4, §3.8, printed pages 125-129, PDF pages 151-155; Source: NVME-BASE-2.4, Rev. 2.4, §3.2.2-3.2.4, printed pages 80-85, PDF pages 106-111

### Q14. Which concepts or conditions must be distinguished in “CMB, PMR, capacity, and namespaces are different resource views”?

<!-- qa:base-ch3-memory-capacity-rows -->

**Answer.**

- CMB — Controller-provided working memory — Capability bits decide whether SQs, CQs, lists, or data may reside there
- PMR — A region with persistence semantics — Enable, ready, error, and address control must be read together
- Capacity model — Capacity of subsystem/group/set/namespace levels — Fields from different levels must not be subtracted directly

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4, printed pages 52-54, PDF pages 78-80; Source: NVME-BASE-2.4, Rev. 2.4, §3.8, printed pages 125-129, PDF pages 151-155; Source: NVME-BASE-2.4, Rev. 2.4, §3.2.2-3.2.4, printed pages 80-85, PDF pages 106-111

### Q15. How does “CMB, PMR, capacity, and namespaces are different resource views” apply to a concrete calculation or operational scenario?

<!-- qa:base-ch3-memory-capacity-example -->

**Answer.**

Informative example: enough CMB space for an SQ does not add the same amount of namespace capacity. The former is placement space for queues or data structures; the latter is formatted non-volatile capacity accessible to the host.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4, printed pages 52-54, PDF pages 78-80; Source: NVME-BASE-2.4, Rev. 2.4, §3.8, printed pages 125-129, PDF pages 151-155; Source: NVME-BASE-2.4, Rev. 2.4, §3.2.2-3.2.4, printed pages 80-85, PDF pages 106-111

### Q16. What misinterpretation is most likely in “CMB, PMR, capacity, and namespaces are different resource views”, and how is it debugged?

<!-- qa:base-ch3-memory-capacity-pitfall -->

**Answer.**

A memory-map debug diagram should separate host memory, CMB, PMR, and namespace media. For a CMB or PMR address, retain BIR, BAR base, offset, enable state, and ready state rather than logging only the final CPU virtual address.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4, printed pages 52-54, PDF pages 78-80; Source: NVME-BASE-2.4, Rev. 2.4, §3.8, printed pages 125-129, PDF pages 151-155; Source: NVME-BASE-2.4, Rev. 2.4, §3.2.2-3.2.4, printed pages 80-85, PDF pages 106-111

### Q17. What is the governing interpretation for “Recovery boundaries across shutdown, reset, Keep Alive, and firmware update”?

<!-- qa:base-ch3-lifecycle-lead -->

**Answer.**

The common lifecycle question is which layer of state remains valid. Normal shutdown coordinates through CC.SHN and CSTS.SHST; resets exist at subsystem, controller, and queue levels; Keep Alive monitors host-controller liveness; firmware activation may require a particular reset. The same temporary inability to process commands does not imply the same recovery.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.6.1, 3.6.3, printed pages 113-120, PDF pages 139-146; Source: NVME-BASE-2.4, Rev. 2.4, §3.7, printed pages 120-125, PDF pages 146-151; Source: NVME-BASE-2.4, Rev. 2.4, §3.9, printed pages 129-135, PDF pages 155-161; Source: NVME-BASE-2.4, Rev. 2.4, §3.10-3.11, printed pages 135-138, PDF pages 161-164

### Q18. Which concepts or conditions must be distinguished in “Recovery boundaries across shutdown, reset, Keep Alive, and firmware update”?

<!-- qa:base-ch3-lifecycle-rows -->

**Answer.**

- Normal shutdown — Protected stop with progress reporting — Observe SHN/SHST
- Controller reset — Controller-scope state — Queue preservation depends on reset type
- NVM subsystem reset — Wider subsystem scope — May affect multiple controllers
- Keep Alive timeout — Liveness failure — Must not be equated with media failure

> Source: NVME-BASE-2.4, Rev. 2.4, §3.6.1, 3.6.3, printed pages 113-120, PDF pages 139-146; Source: NVME-BASE-2.4, Rev. 2.4, §3.7, printed pages 120-125, PDF pages 146-151; Source: NVME-BASE-2.4, Rev. 2.4, §3.9, printed pages 129-135, PDF pages 155-161; Source: NVME-BASE-2.4, Rev. 2.4, §3.10-3.11, printed pages 135-138, PDF pages 161-164

### Q19. How does “Recovery boundaries across shutdown, reset, Keep Alive, and firmware update” apply to a concrete calculation or operational scenario?

<!-- qa:base-ch3-lifecycle-example -->

**Answer.**

Informative example: for a normal shutdown, the host stops submitting new I/O, sets CC.SHN, and observes CSTS.SHST. If controller fatal status appears while waiting, subsequent recovery follows reset scope and rebuilds resources rather than assuming normal shutdown completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.6.1, 3.6.3, printed pages 113-120, PDF pages 139-146; Source: NVME-BASE-2.4, Rev. 2.4, §3.7, printed pages 120-125, PDF pages 146-151; Source: NVME-BASE-2.4, Rev. 2.4, §3.9, printed pages 129-135, PDF pages 155-161; Source: NVME-BASE-2.4, Rev. 2.4, §3.10-3.11, printed pages 135-138, PDF pages 161-164

### Q20. What misinterpretation is most likely in “Recovery boundaries across shutdown, reset, Keep Alive, and firmware update”, and how is it debugged?

<!-- qa:base-ch3-lifecycle-pitfall -->

**Answer.**

A recovery trace must record trigger, scope, start/completion timestamps, timeout source, and rebuild list. A single 'reset device' message makes queue-level, controller-level, and subsystem-level state loss indistinguishable.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.6.1, 3.6.3, printed pages 113-120, PDF pages 139-146; Source: NVME-BASE-2.4, Rev. 2.4, §3.7, printed pages 120-125, PDF pages 146-151; Source: NVME-BASE-2.4, Rev. 2.4, §3.9, printed pages 129-135, PDF pages 155-161; Source: NVME-BASE-2.4, Rev. 2.4, §3.10-3.11, printed pages 135-138, PDF pages 161-164
