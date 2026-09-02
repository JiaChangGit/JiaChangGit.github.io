---
layout: post
read_time: true
show_date: true
title: "NVMe Base 2.4 Chapters 1-2: Specification Language, PCIe Queues, and Storage Model"
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

# NVMe Base 2.4 Chapters 1-2: Specification Language, PCIe Queues, and Storage Model

Purpose: a source-located engineering report for GitHub Pages and a 100-minute presentation.

Scope: §1-§2; printed pages 1-37; PDF pages 27-63. Only PCIe/memory-based and common NVMe content appears below.

## Source versions

NVM Express Base Specification, Revision 2.4

Verification date: 2026-08-29. No additional errata, ECNs, Technical Proposals, controller-vendor documents, or source text from the external PCI Express Base Specification are included.

## Reading map

```text
Host / CPU core -> Submission Queue -> NVMe controller -> Completion Queue
```

The host places commands in a Submission Queue; the controller fetches and executes them, then posts completions to a Completion Queue.

## Normative language

shall is mandatory, may permits a choice, should expresses a preferred recommendation, and optional means support is not required. The report preserves these terms and never promotes one into another.

## Acronyms first: complete glossary

Every abbreviation below is introduced before it is used in the slide narrative. The term alone is never enough: retain owner, width, unit, scope, and state.

| Acronym / term | Plain-language meaning | Source |
|---|---|---|
| `NVMe` | Non-Volatile Memory Express, the specification family for a host interface to a non-volatile-memory subsystem. | NVME-BASE-2.4 Rev. 2.4, §1.1.1, printed pp. 1, PDF pp. 27 |
| `NVM` | Non-Volatile Memory, memory that retains data without power. | NVME-BASE-2.4 Rev. 2.4, §1.1.1, printed pp. 1, PDF pp. 27 |
| `I/O` | Input/Output, the class of data operations performed on a namespace. | NVME-BASE-2.4 Rev. 2.4, §2.3.2, printed pp. 33, PDF pp. 59 |
| `Admin` | Administrative, the control path used to create, configure, query, or manage controllers and queues. | NVME-BASE-2.4 Rev. 2.4, §2.3.2, printed pp. 33, PDF pp. 59 |
| `SQ` | Submission Queue, the queue into which the host places commands. | NVME-BASE-2.4 Rev. 2.4, §2.1, printed pp. 21-23, PDF pp. 47-49 |
| `CQ` | Completion Queue, the queue into which a controller posts command completions. | NVME-BASE-2.4 Rev. 2.4, §2.1, printed pp. 21-23, PDF pp. 47-49 |
| `SQE` | Submission Queue Entry, one command structure in an SQ. | NVME-BASE-2.4 Rev. 2.4, §2.1, printed pp. 21-23, PDF pp. 47-49 |
| `CQE` | Completion Queue Entry, one completion-result structure in a CQ. | NVME-BASE-2.4 Rev. 2.4, §2.1, printed pp. 21-23, PDF pp. 47-49 |
| `NSID` | Namespace Identifier, a controller-visible numeric handle for a namespace; the identifier is not the namespace object itself. | NVME-BASE-2.4 Rev. 2.4, §2.3.3, printed pp. 33-35, PDF pp. 59-61 |
| `NVM subsystem` | NVM subsystem, the NVMe system boundary containing controllers, ports, namespaces, and non-volatile storage resources. | NVME-BASE-2.4 Rev. 2.4, §2.3.1, printed pp. 26-33, PDF pp. 52-59 |
| `namespace` | Namespace, a formatted quantity of non-volatile memory accessed by a host through a controller. | NVME-BASE-2.4 Rev. 2.4, §2.3.1, printed pp. 26-33, PDF pp. 52-59 |
| `NVM Set` | NVM Set, a capacity grouping that associates namespaces with a managed set of NVM resources. | NVME-BASE-2.4 Rev. 2.4, §2.3.1, printed pp. 26-33, PDF pp. 52-59 |
| `Endurance Group` | Endurance Group, a group of NVM resources for isolating and reporting endurance-related state. | NVME-BASE-2.4 Rev. 2.4, §2.3.1, printed pp. 26-33, PDF pp. 52-59 |
| `Reclaim Group` | Reclaim Group, a set of non-volatile storage resources with shared reclamation behavior. | NVME-BASE-2.4 Rev. 2.4, §2.3.1, printed pp. 26-33, PDF pp. 52-59 |
| `Reclaim Unit` | Reclaim Unit, a smaller management granularity used when a controller reclaims media. | NVME-BASE-2.4 Rev. 2.4, §2.3.1, printed pp. 26-33, PDF pp. 52-59 |
| `SR-IOV` | Single Root I/O Virtualization, a PCIe capability that exposes one PF and multiple VFs from one device. | NVME-BASE-2.4 Rev. 2.4, §2.4.1, printed pp. 35-37, PDF pp. 61-63 |
| `PF` | Physical Function, a full-featured PCIe function that can manage associated VFs. | NVME-BASE-2.4 Rev. 2.4, §2.4.1, printed pp. 35-37, PDF pp. 61-63 |
| `VF` | Virtual Function, a resource-constrained virtual PCIe function created by SR-IOV. | NVME-BASE-2.4 Rev. 2.4, §2.4.1, printed pp. 35-37, PDF pp. 61-63 |
| `Dword` | Double word, four bytes or 32 bits; NVMe command fields are commonly identified by CDW number. | NVME-BASE-2.4 Rev. 2.4, §1.4.3, printed pp. 5, PDF pp. 31 |
| `0's-based` | Zero-based encoding, where field value zero represents an actual quantity of one; decoding generally adds one. | NVME-BASE-2.4 Rev. 2.4, §1.4.2, printed pp. 3-5, PDF pp. 29-31 |

## Visual atlas: locate the system before reading fields

Each redraw answers a different question: architecture locates components, sequence shows ownership, decode turns bits into engineering values, and state views preserve failure evidence. These are teaching redraws, not copies of specification artwork.

### Visual 01: Find the owning specification: do not read document applicability as a protocol stack

**View type:** `architecture`

```text
[Need: what operation?]
  ├─ [Base: common mechanism]
  ├─ [PCIe Transport: memory and regist…]
  └─ [I/O Command Set: data-operation s…]
```

**Question answered:** When a command, register, or data format appears, the first question is not merely where it is located, but which specification owns the definition. Base supplies the common protocol, the Transport adds the PCIe binding, and an I/O Command Set defines namespace data operations. The boxes in Figure 1 show applicability, not mandatory packet traversal through a stack.

**Supporting Figures:** Figure 1, Figure 5

**Sources:** NVME-BASE-2.4 Rev. 2.4, §1.1.1, printed pp. 1, PDF pp. 27; NVME-BASE-2.4 Rev. 2.4, §2.3.2, printed pp. 33, PDF pp. 59

### Visual 02: Decode the number before interpreting the field

**View type:** `decode`

```text
[RAW: Raw bits] → [LOCATE: Confirm bit/byte range] → [DECODE: Apply radix and endian] → [VALIDATE: Apply unit/zero-based rule]
VALIDATE fail ──→ return to RAW evidence
```

**Question answered:** An NVMe number carries radix, unit, width, endian convention, and sometimes zero-based encoding. Equal-looking field values can represent different quantities when any one of these attributes differs. Figures 2 and 3 are the common foundation for later register, SQE, CQE, and log-page calculations.

**Supporting Figures:** Figure 2, Figure 3

**Sources:** NVME-BASE-2.4 Rev. 2.4, §1.4.2, printed pp. 3-5, PDF pp. 29-31; NVME-BASE-2.4 Rev. 2.4, §1.4.3, printed pp. 5, PDF pp. 31

### Visual 03: Queue pairs are the traffic rules for every command flow

**View type:** `sequence`

```text
Host / software        Shared object        Controller / evidence
Host → Shared: Host fills SQE
Shared → Controller: Host publishes SQ tail
Controller → Shared: Controller fetches/executes
Shared → Host: Controller writes CQE
Host → Shared: Host consumes CQE
```

**Question answered:** The host does not write a command directly into the controller. It builds an SQE in memory and publishes a new SQ tail; the controller fetches and executes the command, then places a CQE into a CQ. The 1:1 and n:1 distinction in Figures 6 and 7 concerns whether multiple SQs share one CQ, not whether commands share one SQE.

**Supporting Figures:** Figure 6, Figure 7

**Sources:** NVME-BASE-2.4 Rev. 2.4, §2.1, printed pp. 21-23, PDF pp. 47-49; NVME-BASE-2.4 Rev. 2.4, §2.3.3, printed pp. 33-35, PDF pp. 59-61

### Visual 04: Build the storage and path mental model upward from a namespace

**View type:** `architecture`

```text
[NVM subsystem]
  ├─ [Domain/Endurance Group]
  ├─ [NVM Set or Reclaim Group]
  ├─ [Namespace]
  └─ [Controller-visible NSID]
```

**Question answered:** A namespace is the formatted capacity actually accessed by the host, while capacity management, endurance, reclamation, and paths live at different levels. Figures 11-18 describe containment using NVM Sets or Reclaim Groups; Figures 19-22 instead show controllers, ports, paths, and PCIe Functions. The two groups answer different questions and must not be collapsed into a falsely one-to-one tree.

**Supporting Figures:** Figure 11, Figure 12, Figure 13, Figure 14, Figure 15, Figure 16, Figure 17, Figure 18, Figure 19, Figure 20, Figure 21, Figure 22

**Sources:** NVME-BASE-2.4 Rev. 2.4, §2.3.1, printed pp. 26-33, PDF pp. 52-59; NVME-BASE-2.4 Rev. 2.4, §2.3.3, printed pp. 33-35, PDF pp. 59-61; NVME-BASE-2.4 Rev. 2.4, §2.4.1, printed pp. 35-37, PDF pp. 61-63; NVME-BASE-2.4 Rev. 2.4, §2.4.2, printed pp. 37, PDF pp. 63

## Mental Model and complete teaching path

The modules follow engineering causality rather than specification-section order. Related Figures return at the point where they support the flow.

### Module 01: Find the owning specification: do not read document applicability as a protocol stack

**Explanation.** When a command, register, or data format appears, the first question is not merely where it is located, but which specification owns the definition. Base supplies the common protocol, the Transport adds the PCIe binding, and an I/O Command Set defines namespace data operations. The boxes in Figure 1 show applicability, not mandatory packet traversal through a stack.

```text
Need: what operation?
  ↓
Base: common mechanism
  ↓
PCIe Transport: memory and register binding
  ↓
I/O Command Set: data-operation semantics
```

#### Comparison

| Item | What it answers | Engineering note |
|---|---|---|
| Base | Common commands, queues, status, and structures | Do not assume it owns every PCIe-register detail |
| PCIe Transport | BARs, MMIO, doorbells, interrupts, and PCIe-specific behavior | It does not override Base in a conflict |
| I/O Command Set | Specific namespace I/O commands and extensions | It does not redefine the transport |

**Informative example.** To implement Firmware Image Download, read Base for command fields and completion status, then use the PCIe Transport for Admin-command data-pointer and memory-access constraints. The Admin command can be understood without an I/O Command Set, while the PCIe Transport alone does not provide complete command semantics.

**Common mistake / debugging.** A common mistake is to infer a call stack from vertical placement in Figure 1. Label each statement as an owner definition, extension, or binding, then cite the source that actually owns the normative requirement.

**Supporting sources:** NVME-BASE-2.4 Rev. 2.4, §1.1.1, printed pp. 1, PDF pp. 27; NVME-BASE-2.4 Rev. 2.4, §2.3.2, printed pp. 33, PDF pp. 59

**Related Figures:** Figure 1, Figure 5

### Module 02: Decode the number before interpreting the field

**Explanation.** An NVMe number carries radix, unit, width, endian convention, and sometimes zero-based encoding. Equal-looking field values can represent different quantities when any one of these attributes differs. Figures 2 and 3 are the common foundation for later register, SQE, CQE, and log-page calculations.

```text
Raw bits
  ↓
Confirm bit/byte range
  ↓
Apply radix and endian
  ↓
Apply unit/zero-based rule
  ↓
Obtain engineering value
```

#### Comparison

| Item | What it answers | Engineering note |
|---|---|---|
| 1000 | Decimal 1000 | No b/h suffix means decimal |
| 1000b | Binary value 8 | b is a radix marker, not a bit unit |
| 1000h | Hexadecimal value 4096 | Common for offsets and register values |
| NUMD=0 | One actual dword | Add one only when the field is explicitly zero-based |

**Informative example.** Informative example: a 512-byte transfer contains 512 / 4 = 128 dwords. If NUMD is zero-based, the encoded value is 128 - 1 = 127 = 007Fh. Treating 007Fh as a byte count under-allocates the buffer; forgetting the subtraction requests 129 dwords.

**Common mistake / debugging.** During debugging, record five items together: raw value, bit range, radix, unit, and encoding rule. A decimal result without the original hexadecimal value is usually insufficient to isolate off-by-one, byte-swap, or unit defects.

**Supporting sources:** NVME-BASE-2.4 Rev. 2.4, §1.4.2, printed pp. 3-5, PDF pp. 29-31; NVME-BASE-2.4 Rev. 2.4, §1.4.3, printed pp. 5, PDF pp. 31

**Related Figures:** Figure 2, Figure 3

### Module 03: Queue pairs are the traffic rules for every command flow

**Explanation.** The host does not write a command directly into the controller. It builds an SQE in memory and publishes a new SQ tail; the controller fetches and executes the command, then places a CQE into a CQ. The 1:1 and n:1 distinction in Figures 6 and 7 concerns whether multiple SQs share one CQ, not whether commands share one SQE.

```text
Host fills SQE
  ↓
Host publishes SQ tail
  ↓
Controller fetches/executes
  ↓
Controller writes CQE
  ↓
Host consumes CQE
```

#### Comparison

| Item | What it answers | Engineering note |
|---|---|---|
| Admin queue pair | One Admin SQ to one Admin CQ | Initialization and management path |
| I/O 1:1 | One I/O SQ to one I/O CQ | Simple tracking and clear isolation |
| I/O n:1 | Multiple I/O SQs share one I/O CQ | Merged completion path; SQID/CID still recover the command |

**Informative example.** Informative example: SQ 3 and SQ 4 share CQ 2. Both commands may use CID 5 and remain distinguishable because the identity key is (SQID, CID): (3,5) and (4,5). An outstanding-command map keyed only by CID can associate a completion with the wrong command.

**Common mistake / debugging.** A queue defect is easier to isolate by separating three ownership questions: who writes the entry, who advances the pointer, and who may reuse the slot. Treating a doorbell write as command completion, or reusing resources before CQE consumption, are classic lifecycle errors.

**Supporting sources:** NVME-BASE-2.4 Rev. 2.4, §2.1, printed pp. 21-23, PDF pp. 47-49; NVME-BASE-2.4 Rev. 2.4, §2.3.3, printed pp. 33-35, PDF pp. 59-61

**Related Figures:** Figure 6, Figure 7

### Module 04: Build the storage and path mental model upward from a namespace

**Explanation.** A namespace is the formatted capacity actually accessed by the host, while capacity management, endurance, reclamation, and paths live at different levels. Figures 11-18 describe containment using NVM Sets or Reclaim Groups; Figures 19-22 instead show controllers, ports, paths, and PCIe Functions. The two groups answer different questions and must not be collapsed into a falsely one-to-one tree.

```text
NVM subsystem
  ↓
Domain/Endurance Group
  ↓
NVM Set or Reclaim Group
  ↓
Namespace
  ↓
Controller-visible NSID
```

#### Comparison

| Item | What it answers | Engineering note |
|---|---|---|
| Multi-path I/O | One host and one namespace with two or more independent paths | Focus: path redundancy |
| Namespace sharing | Two or more hosts access one shared namespace | Focus: host ownership and coordination |
| SR-IOV | One PCIe device exposes PFs/VFs | A PCIe Function need not be an independent subsystem |

**Informative example.** Informative example: host A accesses namespace X through controllers 1 and 2, creating multi-path I/O. When host B also accesses the same namespace X through controller 2, namespace sharing is present as well. NSIDs may differ between controllers, so cross-controller comparison begins with namespace identity rather than raw NSID equality.

**Common mistake / debugging.** On a debug diagram, label object identity, owner, and scope separately. A controller seeing an NSID proves an access relationship; it does not prove ownership of the underlying media or equal NSID values on another controller.

**Supporting sources:** NVME-BASE-2.4 Rev. 2.4, §2.3.1, printed pp. 26-33, PDF pp. 52-59; NVME-BASE-2.4 Rev. 2.4, §2.3.3, printed pp. 33-35, PDF pp. 59-61; NVME-BASE-2.4 Rev. 2.4, §2.4.1, printed pp. 35-37, PDF pp. 61-63; NVME-BASE-2.4 Rev. 2.4, §2.4.2, printed pp. 37, PDF pp. 63

**Related Figures:** Figure 11, Figure 12, Figure 13, Figure 14, Figure 15, Figure 16, Figure 17, Figure 18, Figure 19, Figure 20, Figure 21, Figure 22

## Source-located specification findings

The mental model above explains causality. This section preserves each source-located conclusion and its normative strength for speaker notes and review.

### 1. Roles in the NVMe specification family

<!-- claim:BASE12-FAMILY -->

The Base Specification defines the common NVMe protocol; a Transport Specification binds it to a transport, and an I/O Command Set Specification extends commands and data structures. This is an applicability relationship, not a protocol stack.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §1.1.1, printed pages 1, PDF pages 27

### 2. Normative keyword strength

<!-- claim:BASE12-KEYWORDS -->

The specification assigns distinct force to mandatory, may, optional, reserved, shall, and should. A summary must not strengthen may or should into shall.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §1.4.1, printed pages 2-3, PDF pages 28-29

### 3. Radix and capacity units

<!-- claim:BASE12-NUMBERS -->

A value is interpreted together with its radix and units. Hexadecimal uses the h suffix, binary uses b, and decimal may omit d. Decimal and binary capacity prefixes represent different multipliers.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §1.4.2, printed pages 3-5, PDF pages 29-31

### 4. Byte, word, and dword relationships

<!-- claim:BASE12-DWORD -->

NVMe expresses field locations in bytes, words, and dwords. A word is two bytes and a dword is four bytes; field decoding starts by confirming byte and bit numbering.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §1.4.3, printed pages 5, PDF pages 31

### 5. PCIe queue-pair model

<!-- claim:BASE12-QUEUE -->

In the PCIe memory-based model, Submission and Completion Queues reside in memory. Multiple I/O Submission Queues may share an I/O Completion Queue, while the Admin queue pair remains one-to-one.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §2.1, printed pages 21-23, PDF pages 47-49

### 6. NVM storage hierarchy

<!-- claim:BASE12-STORAGE -->

The storage model expresses containment through the NVM subsystem, domain, Endurance Group, NVM Set or Reclaim Group, Reclaim Unit, and namespace. A namespace is the formatted capacity a host accesses through a controller.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §2.3.1, printed pages 26-33, PDF pages 52-59

### 7. Admin and I/O Command Sets

<!-- claim:BASE12-COMMANDSET -->

The Admin Command Set manages controllers and queues; an I/O Command Set defines data operations on namespaces. Base describes common mechanisms, while each I/O Command Set Specification describes command semantics.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §2.3.2, printed pages 33, PDF pages 59

### 8. Subsystem objects and NSIDs

<!-- claim:BASE12-SUBSYSTEM -->

Controllers, ports, namespaces, and PCI Functions are distinct objects. An NSID is a controller-visible handle for a namespace, not the namespace itself.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §2.3.3, printed pages 33-35, PDF pages 59-61

### 9. Multi-path and namespace sharing

<!-- claim:BASE12-MULTIPATH -->

Multi-path I/O provides two or more independent paths from one host to one namespace; namespace sharing lets two or more hosts access one shared namespace through different controllers. Both require at least two controllers.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §2.4.1, printed pages 35-37, PDF pages 61-63

### 10. Asymmetric path characteristics

<!-- claim:BASE12-ASYMMETRY -->

With multi-path or sharing, controllers need not provide identical access characteristics to the same namespace; the host may select paths using the state reported by each controller.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §2.4.2, printed pages 37, PDF pages 63

## Figure index

This report introduces all 18 in-scope Figures. Use the section links below for the 100-minute presentation path; every Figure remains available as an appendix item.

- [§1.1](#section-1-1)

- [§1.4](#section-1-4)

- [§2](#section-2)

- [§2.1](#section-2-1)

- [§2.3](#section-2-3)

- [§2.4](#section-2-4)

## Figure and field-table teaching reference

The source uses Figure numbers for diagrams and field-layout tables. No source artwork is reproduced; compact field and keyword indexes come from the locally verified PDFs.

<a id="section-1-1"></a>

### §1.1

<details markdown="1">
<summary><strong>Figure 1: NVMe Family of Specifications</strong></summary>

<!-- claim:BASE12-FIG-001-CLAIM figure-table:BASE12-FIG-001 -->

**SPEC.** Figure 1, "NVMe Family of Specifications": Places NVMe Family of Specifications in the NVMe document and command-set hierarchy. Read from the common Base requirements toward the transport and command-set layer; keep these source-derived labels distinct: NVMe Family.

#### Where this Figure fits

Figure 1 sits in §1.1.1 and acts as a relationship checkpoint. Read it after the report mental model has established the owning object and before software turns NVMe Family into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

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

1. Locate the structure, register, queue, or object named by the caption and confirm that §1.1.1 is the applicable context.
2. Decode NVMe Family at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check the cited condition as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 1 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §1.1.1 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes NVMe Family, the cited condition, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §1.1.1, the capability that enables the structure, and the actual transfer or register width. |

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

> Source: NVME-BASE-2.4, Rev. 2.4, §1.1.1, Figure 1, printed pages 1, PDF pages 27

</details>

<a id="section-1-4"></a>

### §1.4

<details markdown="1">
<summary><strong>Figure 2: Decimal and Binary Units</strong></summary>

<!-- claim:BASE12-FIG-002-CLAIM figure-table:BASE12-FIG-002 -->

**SPEC.** Figure 2, "Decimal and Binary Units": Defines the numeric-unit or byte-width convention illustrated by Decimal and Binary Units. Separate decimal units from binary units and preserve byte/word/Dword boundaries. Evidence index: Decimal and Binary Units.

#### Where this Figure fits

Figure 2 sits in §1.4.2 and acts as a relationship checkpoint. Read it after the report mental model has established the owning object and before software turns Decimal and Binary Units into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This Figure explains a specific relationship or example. Identify each component type and owner, then decide whether each connection represents data flow, control flow, containment, or a condition. Visual placement alone creates no normative requirement.

#### Teaching redraw

```text
[Locate source: Decimal and Binary Units]
          ↓
[Extract field: evidence] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `Decimal and Binary Units` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §1.4.2 is the applicable context.
2. Decode Decimal and Binary Units at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check the cited condition as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 2 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §1.4.2 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes Decimal and Binary Units, the cited condition, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §1.4.2, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 2. Annotate the bytes containing Decimal and Binary Units, decode them, and independently verify the cited condition. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of Decimal and Binary Units in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand Decimal and Binary Units and state its unit or object scope?
2. Can the reader explain why the cited condition is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** Decimal and Binary Units

**Source keyword index:** none

> Source: NVME-BASE-2.4, Rev. 2.4, §1.4.2, Figure 2, printed pages 3, PDF pages 29

</details>

<details markdown="1">
<summary><strong>Figure 3: Byte, Word, and Dword Relationships</strong></summary>

<!-- claim:BASE12-FIG-003-CLAIM figure-table:BASE12-FIG-003 -->

**SPEC.** Figure 3, "Byte, Word, and Dword Relationships": Defines the numeric-unit or byte-width convention illustrated by Byte, Word, and Dword Relationships. Separate decimal units from binary units and preserve byte/word/Dword boundaries. Evidence index: Byte, Word, and Dword Relationships.

#### Where this Figure fits

Figure 3 sits in §1.4.3 and acts as a relationship checkpoint. Read it after the report mental model has established the owning object and before software turns Byte, Word, and Dword Relationships into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This Figure explains a specific relationship or example. Identify each component type and owner, then decide whether each connection represents data flow, control flow, containment, or a condition. Visual placement alone creates no normative requirement.

#### Teaching redraw

```text
[Locate source: Byte, Word, and Dword Relationships]
          ↓
[Extract field: evidence] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `Byte, Word, and Dword Relationships` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §1.4.3 is the applicable context.
2. Decode Byte, Word, and Dword Relationships at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check the cited condition as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 3 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §1.4.3 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes Byte, Word, and Dword Relationships, the cited condition, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §1.4.3, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 3. Annotate the bytes containing Byte, Word, and Dword Relationships, decode them, and independently verify the cited condition. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of Byte, Word, and Dword Relationships in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand Byte, Word, and Dword Relationships and state its unit or object scope?
2. Can the reader explain why the cited condition is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** Byte, Word, and Dword Relationships

**Source keyword index:** none

> Source: NVME-BASE-2.4, Rev. 2.4, §1.4.3, Figure 3, printed pages 5, PDF pages 31

</details>

<a id="section-2"></a>

### §2

<details markdown="1">
<summary><strong>Figure 5: Types of NVMe Command Sets</strong></summary>

<!-- claim:BASE12-FIG-005-CLAIM figure-table:BASE12-FIG-005 -->

**SPEC.** Figure 5, "Types of NVMe Command Sets": Places Types of NVMe Command Sets in the NVMe document and command-set hierarchy. Read from the common Base requirements toward the transport and command-set layer; keep these source-derived labels distinct: Command Set, Command.

#### Where this Figure fits

Figure 5 sits in §2 and acts as a relationship checkpoint. Read it after the report mental model has established the owning object and before software turns Command Set into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This Figure explains a specific relationship or example. Identify each component type and owner, then decide whether each connection represents data flow, control flow, containment, or a condition. Visual placement alone creates no normative requirement.

#### Teaching redraw

```text
[Locate source: Command Set]
          ↓
[Extract field: Command] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `Command Set` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `Command` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §2 is the applicable context.
2. Decode Command Set at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check Command as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 5 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §2 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes Command Set, Command, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §2, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 5. Annotate the bytes containing Command Set, decode them, and independently verify Command. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of Command Set in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand Command Set and state its unit or object scope?
2. Can the reader explain why Command is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** Command Set, Command

**Source keyword index:** none

> Source: NVME-BASE-2.4, Rev. 2.4, §2, Figure 5, printed pages 21, PDF pages 47

</details>

<a id="section-2-1"></a>

### §2.1

<details markdown="1">
<summary><strong>Figure 6: Queue Pair Example, 1:1 Mapping</strong></summary>

<!-- claim:BASE12-FIG-006-CLAIM figure-table:BASE12-FIG-006 -->

**SPEC.** Figure 6, "Queue Pair Example, 1:1 Mapping": Shows the queue or command relationship expressed by Queue Pair Example, 1:1 Mapping. Trace ownership and direction from host to SQ, controller, and CQ; keep the indexed elements distinct: Queue Pair, 1:1.

#### Where this Figure fits

Figure 6 sits in §2.1 and acts as a queue checkpoint. Read it after the report mental model has established the owning object and before software turns Queue Pair into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a queue or command-flow Figure. Label host and controller ownership first, then trace head, tail, phase, or arbitration changes. An arrow represents a state or ownership transition and does not automatically prove command completion.

#### Teaching redraw

```text
[Locate source: Queue Pair]
          ↓
[Extract field: 1:1] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `Queue Pair` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `1:1` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §2.1 is the applicable context.
2. Decode Queue Pair at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check 1:1 as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 6 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §2.1 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes Queue Pair, 1:1, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §2.1, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 6. Annotate the bytes containing Queue Pair, decode them, and independently verify 1:1. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of Queue Pair in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand Queue Pair and state its unit or object scope?
2. Can the reader explain why 1:1 is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** Queue Pair, 1:1

**Source keyword index:** none

> Source: NVME-BASE-2.4, Rev. 2.4, §2.1, Figure 6, printed pages 22, PDF pages 48

</details>

<details markdown="1">
<summary><strong>Figure 7: Queue Pair Example, n:1 Mapping</strong></summary>

<!-- claim:BASE12-FIG-007-CLAIM figure-table:BASE12-FIG-007 -->

**SPEC.** Figure 7, "Queue Pair Example, n:1 Mapping": Shows the queue or command relationship expressed by Queue Pair Example, n:1 Mapping. Trace ownership and direction from host to SQ, controller, and CQ; keep the indexed elements distinct: Queue Pair.

#### Where this Figure fits

Figure 7 sits in §2.1 and acts as a queue checkpoint. Read it after the report mental model has established the owning object and before software turns Queue Pair into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a queue or command-flow Figure. Label host and controller ownership first, then trace head, tail, phase, or arbitration changes. An arrow represents a state or ownership transition and does not automatically prove command completion.

#### Teaching redraw

```text
[Locate source: Queue Pair]
          ↓
[Extract field: evidence] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `Queue Pair` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §2.1 is the applicable context.
2. Decode Queue Pair at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check the cited condition as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 7 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §2.1 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes Queue Pair, the cited condition, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §2.1, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 7. Annotate the bytes containing Queue Pair, decode them, and independently verify the cited condition. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of Queue Pair in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand Queue Pair and state its unit or object scope?
2. Can the reader explain why the cited condition is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** Queue Pair

**Source keyword index:** none

> Source: NVME-BASE-2.4, Rev. 2.4, §2.1, Figure 7, printed pages 22, PDF pages 48

</details>

<a id="section-2-3"></a>

### §2.3

<details markdown="1">
<summary><strong>Figure 11: Simple NVM Storage Hierarchy with NVM Sets</strong></summary>

<!-- claim:BASE12-FIG-011-CLAIM figure-table:BASE12-FIG-011 -->

**SPEC.** Figure 11, "Simple NVM Storage Hierarchy with NVM Sets": Shows the object or capacity relationships in Simple NVM Storage Hierarchy with NVM Sets. Separate logical identifiers from controllers, namespaces, ports, and capacity containers. Evidence index: NVM Storage Hierarchy, NVM Set.

#### Where this Figure fits

Figure 11 sits in §2.3.1 and acts as a hierarchy checkpoint. Read it after the report mental model has established the owning object and before software turns NVM Storage Hierarchy into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is an object or capacity relationship Figure. Separate containment, accessibility, identifier reference, and sharing. Adjacent boxes need not be one-to-one, and an identifier is not the physical or logical object it references.

#### Teaching redraw

```text
[Locate source: NVM Storage Hierarchy]
          ↓
[Extract field: NVM Set] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `NVM Storage Hierarchy` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `NVM Set` | NVM Set, a capacity grouping that associates namespaces with a managed set of NVM resources. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §2.3.1 is the applicable context.
2. Decode NVM Storage Hierarchy at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check NVM Set as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 11 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §2.3.1 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes NVM Storage Hierarchy, NVM Set, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §2.3.1, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 11. Annotate the bytes containing NVM Storage Hierarchy, decode them, and independently verify NVM Set. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of NVM Storage Hierarchy in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand NVM Storage Hierarchy and state its unit or object scope?
2. Can the reader explain why NVM Set is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** NVM Storage Hierarchy, NVM Set

**Source keyword index:** none

> Source: NVME-BASE-2.4, Rev. 2.4, §2.3.1, Figure 11, printed pages 27, PDF pages 53

</details>

<details markdown="1">
<summary><strong>Figure 12: Simple NVM Storage Hierarchy with One Reclaim Group</strong></summary>

<!-- claim:BASE12-FIG-012-CLAIM figure-table:BASE12-FIG-012 -->

**SPEC.** Figure 12, "Simple NVM Storage Hierarchy with One Reclaim Group": Shows the object or capacity relationships in Simple NVM Storage Hierarchy with One Reclaim Group. Separate logical identifiers from controllers, namespaces, ports, and capacity containers. Evidence index: NVM Storage Hierarchy, Reclaim Group.

#### Where this Figure fits

Figure 12 sits in §2.3.1 and acts as a relationship checkpoint. Read it after the report mental model has established the owning object and before software turns NVM Storage Hierarchy into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This Figure explains a specific relationship or example. Identify each component type and owner, then decide whether each connection represents data flow, control flow, containment, or a condition. Visual placement alone creates no normative requirement.

#### Teaching redraw

```text
[Locate source: NVM Storage Hierarchy]
          ↓
[Extract field: Reclaim Group] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `NVM Storage Hierarchy` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `Reclaim Group` | Reclaim Group, a set of non-volatile storage resources with shared reclamation behavior. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §2.3.1 is the applicable context.
2. Decode NVM Storage Hierarchy at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check Reclaim Group as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 12 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §2.3.1 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes NVM Storage Hierarchy, Reclaim Group, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §2.3.1, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 12. Annotate the bytes containing NVM Storage Hierarchy, decode them, and independently verify Reclaim Group. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of NVM Storage Hierarchy in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand NVM Storage Hierarchy and state its unit or object scope?
2. Can the reader explain why Reclaim Group is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** NVM Storage Hierarchy, Reclaim Group

**Source keyword index:** none

> Source: NVME-BASE-2.4, Rev. 2.4, §2.3.1, Figure 12, printed pages 28, PDF pages 54

</details>

<details markdown="1">
<summary><strong>Figure 13: Simple NVM Storage Hierarchy with Multiple Reclaim Groups</strong></summary>

<!-- claim:BASE12-FIG-013-CLAIM figure-table:BASE12-FIG-013 -->

**SPEC.** Figure 13, "Simple NVM Storage Hierarchy with Multiple Reclaim Groups": Shows the object or capacity relationships in Simple NVM Storage Hierarchy with Multiple Reclaim Groups. Separate logical identifiers from controllers, namespaces, ports, and capacity containers. Evidence index: NVM Storage Hierarchy, Reclaim Group.

#### Where this Figure fits

Figure 13 sits in §2.3.1 and acts as a relationship checkpoint. Read it after the report mental model has established the owning object and before software turns NVM Storage Hierarchy into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This Figure explains a specific relationship or example. Identify each component type and owner, then decide whether each connection represents data flow, control flow, containment, or a condition. Visual placement alone creates no normative requirement.

#### Teaching redraw

```text
[Locate source: NVM Storage Hierarchy]
          ↓
[Extract field: Reclaim Group] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `NVM Storage Hierarchy` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `Reclaim Group` | Reclaim Group, a set of non-volatile storage resources with shared reclamation behavior. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §2.3.1 is the applicable context.
2. Decode NVM Storage Hierarchy at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check Reclaim Group as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 13 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §2.3.1 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes NVM Storage Hierarchy, Reclaim Group, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §2.3.1, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 13. Annotate the bytes containing NVM Storage Hierarchy, decode them, and independently verify Reclaim Group. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of NVM Storage Hierarchy in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand NVM Storage Hierarchy and state its unit or object scope?
2. Can the reader explain why Reclaim Group is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** NVM Storage Hierarchy, Reclaim Group

**Source keyword index:** none

> Source: NVME-BASE-2.4, Rev. 2.4, §2.3.1, Figure 13, printed pages 29, PDF pages 55

</details>

<details markdown="1">
<summary><strong>Figure 14: Complex NVM Storage Hierarchy with NVM Sets</strong></summary>

<!-- claim:BASE12-FIG-014-CLAIM figure-table:BASE12-FIG-014 -->

**SPEC.** Figure 14, "Complex NVM Storage Hierarchy with NVM Sets": Shows the object or capacity relationships in Complex NVM Storage Hierarchy with NVM Sets. Separate logical identifiers from controllers, namespaces, ports, and capacity containers. Evidence index: NVM Storage Hierarchy, NVM Set.

#### Where this Figure fits

Figure 14 sits in §2.3.1 and acts as a hierarchy checkpoint. Read it after the report mental model has established the owning object and before software turns NVM Storage Hierarchy into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is an object or capacity relationship Figure. Separate containment, accessibility, identifier reference, and sharing. Adjacent boxes need not be one-to-one, and an identifier is not the physical or logical object it references.

#### Teaching redraw

```text
[Locate source: NVM Storage Hierarchy]
          ↓
[Extract field: NVM Set] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `NVM Storage Hierarchy` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `NVM Set` | NVM Set, a capacity grouping that associates namespaces with a managed set of NVM resources. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §2.3.1 is the applicable context.
2. Decode NVM Storage Hierarchy at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check NVM Set as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 14 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §2.3.1 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes NVM Storage Hierarchy, NVM Set, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §2.3.1, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 14. Annotate the bytes containing NVM Storage Hierarchy, decode them, and independently verify NVM Set. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of NVM Storage Hierarchy in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand NVM Storage Hierarchy and state its unit or object scope?
2. Can the reader explain why NVM Set is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** NVM Storage Hierarchy, NVM Set

**Source keyword index:** none

> Source: NVME-BASE-2.4, Rev. 2.4, §2.3.1, Figure 14, printed pages 30, PDF pages 56

</details>

<details markdown="1">
<summary><strong>Figure 15: Complex NVM Storage Hierarchy with Multiple Reclaim Groups</strong></summary>

<!-- claim:BASE12-FIG-015-CLAIM figure-table:BASE12-FIG-015 -->

**SPEC.** Figure 15, "Complex NVM Storage Hierarchy with Multiple Reclaim Groups": Shows the object or capacity relationships in Complex NVM Storage Hierarchy with Multiple Reclaim Groups. Separate logical identifiers from controllers, namespaces, ports, and capacity containers. Evidence index: NVM Storage Hierarchy, Reclaim Group.

#### Where this Figure fits

Figure 15 sits in §2.3.1 and acts as a relationship checkpoint. Read it after the report mental model has established the owning object and before software turns NVM Storage Hierarchy into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This Figure explains a specific relationship or example. Identify each component type and owner, then decide whether each connection represents data flow, control flow, containment, or a condition. Visual placement alone creates no normative requirement.

#### Teaching redraw

```text
[Locate source: NVM Storage Hierarchy]
          ↓
[Extract field: Reclaim Group] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `NVM Storage Hierarchy` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `Reclaim Group` | Reclaim Group, a set of non-volatile storage resources with shared reclamation behavior. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §2.3.1 is the applicable context.
2. Decode NVM Storage Hierarchy at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check Reclaim Group as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 15 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §2.3.1 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes NVM Storage Hierarchy, Reclaim Group, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §2.3.1, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 15. Annotate the bytes containing NVM Storage Hierarchy, decode them, and independently verify Reclaim Group. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of NVM Storage Hierarchy in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand NVM Storage Hierarchy and state its unit or object scope?
2. Can the reader explain why Reclaim Group is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** NVM Storage Hierarchy, Reclaim Group

**Source keyword index:** none

> Source: NVME-BASE-2.4, Rev. 2.4, §2.3.1, Figure 15, printed pages 31, PDF pages 57

</details>

<details markdown="1">
<summary><strong>Figure 16: Single-Namespace NVM Subsystem</strong></summary>

<!-- claim:BASE12-FIG-016-CLAIM figure-table:BASE12-FIG-016 -->

**SPEC.** Figure 16, "Single-Namespace NVM Subsystem": Shows the object or capacity relationships in Single-Namespace NVM Subsystem. Separate logical identifiers from controllers, namespaces, ports, and capacity containers. Evidence index: NVM Subsystem, Namespace.

#### Where this Figure fits

Figure 16 sits in §2.3.3 and acts as a hierarchy checkpoint. Read it after the report mental model has established the owning object and before software turns NVM Subsystem into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is an object or capacity relationship Figure. Separate containment, accessibility, identifier reference, and sharing. Adjacent boxes need not be one-to-one, and an identifier is not the physical or logical object it references.

#### Teaching redraw

```text
[Locate source: NVM Subsystem]
          ↓
[Extract field: Namespace] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `NVM Subsystem` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `Namespace` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §2.3.3 is the applicable context.
2. Decode NVM Subsystem at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check Namespace as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 16 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §2.3.3 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes NVM Subsystem, Namespace, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §2.3.3, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 16. Annotate the bytes containing NVM Subsystem, decode them, and independently verify Namespace. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

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
2. Can the reader explain why Namespace is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** NVM Subsystem, Namespace

**Source keyword index:** none

> Source: NVME-BASE-2.4, Rev. 2.4, §2.3.3, Figure 16, printed pages 32, PDF pages 58

</details>

<details markdown="1">
<summary><strong>Figure 17: Two-Namespace NVM Subsystem</strong></summary>

<!-- claim:BASE12-FIG-017-CLAIM figure-table:BASE12-FIG-017 -->

**SPEC.** Figure 17, "Two-Namespace NVM Subsystem": Shows the object or capacity relationships in Two-Namespace NVM Subsystem. Separate logical identifiers from controllers, namespaces, ports, and capacity containers. Evidence index: NVM Subsystem, Namespace.

#### Where this Figure fits

Figure 17 sits in §2.3.3 and acts as a hierarchy checkpoint. Read it after the report mental model has established the owning object and before software turns NVM Subsystem into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is an object or capacity relationship Figure. Separate containment, accessibility, identifier reference, and sharing. Adjacent boxes need not be one-to-one, and an identifier is not the physical or logical object it references.

#### Teaching redraw

```text
[Locate source: NVM Subsystem]
          ↓
[Extract field: Namespace] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `NVM Subsystem` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `Namespace` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §2.3.3 is the applicable context.
2. Decode NVM Subsystem at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check Namespace as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 17 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §2.3.3 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes NVM Subsystem, Namespace, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §2.3.3, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 17. Annotate the bytes containing NVM Subsystem, decode them, and independently verify Namespace. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

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
2. Can the reader explain why Namespace is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** NVM Subsystem, Namespace

**Source keyword index:** none

> Source: NVME-BASE-2.4, Rev. 2.4, §2.3.3, Figure 17, printed pages 33, PDF pages 59

</details>

<details markdown="1">
<summary><strong>Figure 18: Complex NVM Subsystem</strong></summary>

<!-- claim:BASE12-FIG-018-CLAIM figure-table:BASE12-FIG-018 -->

**SPEC.** Figure 18, "Complex NVM Subsystem": Shows the object or capacity relationships in Complex NVM Subsystem. Separate logical identifiers from controllers, namespaces, ports, and capacity containers. Evidence index: NVM Subsystem.

#### Where this Figure fits

Figure 18 sits in §2.3.3 and acts as a hierarchy checkpoint. Read it after the report mental model has established the owning object and before software turns NVM Subsystem into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

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

1. Locate the structure, register, queue, or object named by the caption and confirm that §2.3.3 is the applicable context.
2. Decode NVM Subsystem at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check the cited condition as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 18 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §2.3.3 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes NVM Subsystem, the cited condition, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §2.3.3, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 18. Annotate the bytes containing NVM Subsystem, decode them, and independently verify the cited condition. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

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

> Source: NVME-BASE-2.4, Rev. 2.4, §2.3.3, Figure 18, printed pages 34, PDF pages 60

</details>

<a id="section-2-4"></a>

### §2.4

<details markdown="1">
<summary><strong>Figure 19: NVM Express Controller with Two Namespaces</strong></summary>

<!-- claim:BASE12-FIG-019-CLAIM figure-table:BASE12-FIG-019 -->

**SPEC.** Figure 19, "NVM Express Controller with Two Namespaces": Shows the object or capacity relationships in NVM Express Controller with Two Namespaces. Separate logical identifiers from controllers, namespaces, ports, and capacity containers. Evidence index: Namespace, Controller.

#### Where this Figure fits

Figure 19 sits in §2.4.1 and acts as a hierarchy checkpoint. Read it after the report mental model has established the owning object and before software turns Namespace into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is an object or capacity relationship Figure. Separate containment, accessibility, identifier reference, and sharing. Adjacent boxes need not be one-to-one, and an identifier is not the physical or logical object it references.

#### Teaching redraw

```text
[Locate source: Namespace]
          ↓
[Extract field: Controller] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `Namespace` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `Controller` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §2.4.1 is the applicable context.
2. Decode Namespace at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check Controller as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 19 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §2.4.1 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes Namespace, Controller, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §2.4.1, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 19. Annotate the bytes containing Namespace, decode them, and independently verify Controller. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of Namespace in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand Namespace and state its unit or object scope?
2. Can the reader explain why Controller is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** Namespace, Controller

**Source keyword index:** none

> Source: NVME-BASE-2.4, Rev. 2.4, §2.4.1, Figure 19, printed pages 35, PDF pages 61

</details>

<details markdown="1">
<summary><strong>Figure 20: NVM Subsystem with Two Controllers and One Port</strong></summary>

<!-- claim:BASE12-FIG-020-CLAIM figure-table:BASE12-FIG-020 -->

**SPEC.** Figure 20, "NVM Subsystem with Two Controllers and One Port": Shows the object or capacity relationships in NVM Subsystem with Two Controllers and One Port. Separate logical identifiers from controllers, namespaces, ports, and capacity containers. Evidence index: NVM Subsystem, Controller.

#### Where this Figure fits

Figure 20 sits in §2.4.1 and acts as a hierarchy checkpoint. Read it after the report mental model has established the owning object and before software turns NVM Subsystem into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is an object or capacity relationship Figure. Separate containment, accessibility, identifier reference, and sharing. Adjacent boxes need not be one-to-one, and an identifier is not the physical or logical object it references.

#### Teaching redraw

```text
[Locate source: NVM Subsystem]
          ↓
[Extract field: Controller] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `NVM Subsystem` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `Controller` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §2.4.1 is the applicable context.
2. Decode NVM Subsystem at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check Controller as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 20 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §2.4.1 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes NVM Subsystem, Controller, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §2.4.1, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 20. Annotate the bytes containing NVM Subsystem, decode them, and independently verify Controller. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

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
2. Can the reader explain why Controller is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** NVM Subsystem, Controller

**Source keyword index:** none

> Source: NVME-BASE-2.4, Rev. 2.4, §2.4.1, Figure 20, printed pages 35, PDF pages 61

</details>

<details markdown="1">
<summary><strong>Figure 21: NVM Subsystem with Two Controllers and Two Ports</strong></summary>

<!-- claim:BASE12-FIG-021-CLAIM figure-table:BASE12-FIG-021 -->

**SPEC.** Figure 21, "NVM Subsystem with Two Controllers and Two Ports": Shows the object or capacity relationships in NVM Subsystem with Two Controllers and Two Ports. Separate logical identifiers from controllers, namespaces, ports, and capacity containers. Evidence index: NVM Subsystem, Controller.

#### Where this Figure fits

Figure 21 sits in §2.4.1 and acts as a hierarchy checkpoint. Read it after the report mental model has established the owning object and before software turns NVM Subsystem into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is an object or capacity relationship Figure. Separate containment, accessibility, identifier reference, and sharing. Adjacent boxes need not be one-to-one, and an identifier is not the physical or logical object it references.

#### Teaching redraw

```text
[Locate source: NVM Subsystem]
          ↓
[Extract field: Controller] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `NVM Subsystem` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `Controller` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §2.4.1 is the applicable context.
2. Decode NVM Subsystem at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check Controller as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 21 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §2.4.1 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes NVM Subsystem, Controller, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §2.4.1, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 21. Annotate the bytes containing NVM Subsystem, decode them, and independently verify Controller. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

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
2. Can the reader explain why Controller is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** NVM Subsystem, Controller

**Source keyword index:** none

> Source: NVME-BASE-2.4, Rev. 2.4, §2.4.1, Figure 21, printed pages 36, PDF pages 62

</details>

<details markdown="1">
<summary><strong>Figure 22: PCI Express Device Supporting Single Root I/O Virtualization (SR-IOV)</strong></summary>

<!-- claim:BASE12-FIG-022-CLAIM figure-table:BASE12-FIG-022 -->

**SPEC.** Figure 22, "PCI Express Device Supporting Single Root I/O Virtualization (SR-IOV)": Shows the Physical Function and Virtual Function relationships in PCI Express Device Supporting Single Root I/O Virtualization (SR-IOV). Separate PCIe Function identity, controller ownership, and shared device resources. Evidence index: SR, IOV.

#### Where this Figure fits

Figure 22 sits in §2.4.1 and acts as a relationship checkpoint. Read it after the report mental model has established the owning object and before software turns SR into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This Figure explains a specific relationship or example. Identify each component type and owner, then decide whether each connection represents data flow, control flow, containment, or a condition. Visual placement alone creates no normative requirement.

#### Teaching redraw

```text
[Locate source: SR]
          ↓
[Extract field: IOV] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `SR` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `IOV` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §2.4.1 is the applicable context.
2. Decode SR at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check IOV as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 22 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §2.4.1 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes SR, IOV, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §2.4.1, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 22. Annotate the bytes containing SR, decode them, and independently verify IOV. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of SR in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand SR and state its unit or object scope?
2. Can the reader explain why IOV is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** SR, IOV

**Source keyword index:** none

> Source: NVME-BASE-2.4, Rev. 2.4, §2.4.1, Figure 22, printed pages 37, PDF pages 63

</details>

## Use and limitations

Use the claim IDs as stable PPT traceability keys. Re-check affected claims if the source revision, errata set, or approved scope changes.
