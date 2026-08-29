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

## Specification findings

### 1. Roles in the NVMe specification family

<!-- claim:BASE12-FAMILY -->

The Base Specification defines the common NVMe protocol; a Transport Specification binds it to a transport, and an I/O Command Set Specification extends commands and data structures. This is an applicability relationship, not a protocol stack.

> Source: NVME-BASE-2.4, Rev. 2.4, §1.1.1, printed pages 1, PDF pages 27

### 2. Normative keyword strength

<!-- claim:BASE12-KEYWORDS -->

The specification assigns distinct force to mandatory, may, optional, reserved, shall, and should. A summary must not strengthen may or should into shall.

> Source: NVME-BASE-2.4, Rev. 2.4, §1.4.1, printed pages 2-3, PDF pages 28-29

### 3. Radix and capacity units

<!-- claim:BASE12-NUMBERS -->

A value is interpreted together with its radix and units. Hexadecimal uses the h suffix, binary uses b, and decimal may omit d. Decimal and binary capacity prefixes represent different multipliers.

> Source: NVME-BASE-2.4, Rev. 2.4, §1.4.2, printed pages 3-5, PDF pages 29-31

### 4. Byte, word, and dword relationships

<!-- claim:BASE12-DWORD -->

NVMe expresses field locations in bytes, words, and dwords. A word is two bytes and a dword is four bytes; field decoding starts by confirming byte and bit numbering.

> Source: NVME-BASE-2.4, Rev. 2.4, §1.4.3, printed pages 5, PDF pages 31

### 5. PCIe queue-pair model

<!-- claim:BASE12-QUEUE -->

In the PCIe memory-based model, Submission and Completion Queues reside in memory. Multiple I/O Submission Queues may share an I/O Completion Queue, while the Admin queue pair remains one-to-one.

> Source: NVME-BASE-2.4, Rev. 2.4, §2.1, printed pages 21-23, PDF pages 47-49

### 6. NVM storage hierarchy

<!-- claim:BASE12-STORAGE -->

The storage model expresses containment through the NVM subsystem, domain, Endurance Group, NVM Set or Reclaim Group, Reclaim Unit, and namespace. A namespace is the formatted capacity a host accesses through a controller.

> Source: NVME-BASE-2.4, Rev. 2.4, §2.3.1, printed pages 26-33, PDF pages 52-59

### 7. Admin and I/O Command Sets

<!-- claim:BASE12-COMMANDSET -->

The Admin Command Set manages controllers and queues; an I/O Command Set defines data operations on namespaces. Base describes common mechanisms, while each I/O Command Set Specification describes command semantics.

> Source: NVME-BASE-2.4, Rev. 2.4, §2.3.2, printed pages 33, PDF pages 59

### 8. Subsystem objects and NSIDs

<!-- claim:BASE12-SUBSYSTEM -->

Controllers, ports, namespaces, and PCI Functions are distinct objects. An NSID is a controller-visible handle for a namespace, not the namespace itself.

> Source: NVME-BASE-2.4, Rev. 2.4, §2.3.3, printed pages 33-35, PDF pages 59-61

### 9. Multi-path and namespace sharing

<!-- claim:BASE12-MULTIPATH -->

Multi-path I/O provides two or more independent paths from one host to one namespace; namespace sharing lets two or more hosts access one shared namespace through different controllers. Both require at least two controllers.

> Source: NVME-BASE-2.4, Rev. 2.4, §2.4.1, printed pages 35-37, PDF pages 61-63

### 10. Asymmetric path characteristics

<!-- claim:BASE12-ASYMMETRY -->

With multi-path or sharing, controllers need not provide identical access characteristics to the same namespace; the host may select paths using the state reported by each controller.

> Source: NVME-BASE-2.4, Rev. 2.4, §2.4.2, printed pages 37, PDF pages 63

## Figure index

This report introduces all 18 in-scope Figures. Use the section links below for the 100-minute presentation path; every Figure remains available as an appendix item.

- [§1.1](#section-1-1)

- [§1.4](#section-1-4)

- [§2](#section-2)

- [§2.1](#section-2-1)

- [§2.3](#section-2-3)

- [§2.4](#section-2-4)

## Figure-by-Figure Guide

The source uses Figure numbers for diagrams and field-layout tables. No source artwork is reproduced; compact field and keyword indexes come from the locally verified PDFs.

<a id="section-1-1"></a>

### §1.1

<details markdown="1">
<summary><strong>Figure 1: NVMe Family of Specifications</strong></summary>

<!-- claim:BASE12-FIG-001-CLAIM figure-table:BASE12-FIG-001 -->

Figure 1, "NVMe Family of Specifications": Places NVMe Family of Specifications in the NVMe document and command-set hierarchy. Read from the common Base requirements toward the transport and command-set layer; keep these source-derived labels distinct: NVMe Family.

- Purpose: Places NVMe Family of Specifications in the NVMe document and command-set hierarchy.

- How to read: Read from the common Base requirements toward the transport and command-set layer; keep these source-derived labels distinct: NVMe Family.

- Conditions and limits: The Figure is explanatory or structural; this guide does not turn its visual relationship into a new requirement. Only the PCIe/memory-based portion is in scope.

- Informative example: Start with NVMe Family, then follow the branch containing the cited condition; cite the document that owns the requirement instead of assuming every layer defines it. This example adds no requirement.

- Source field index: NVMe Family

- Source keyword index: none

> Source: NVME-BASE-2.4, Rev. 2.4, §1.1.1, Figure 1, printed pages 1, PDF pages 27

</details>

<a id="section-1-4"></a>

### §1.4

<details markdown="1">
<summary><strong>Figure 2: Decimal and Binary Units</strong></summary>

<!-- claim:BASE12-FIG-002-CLAIM figure-table:BASE12-FIG-002 -->

Figure 2, "Decimal and Binary Units": Defines the numeric-unit or byte-width convention illustrated by Decimal and Binary Units. Separate decimal units from binary units and preserve byte/word/Dword boundaries. Evidence index: Decimal and Binary Units.

- Purpose: Defines the numeric-unit or byte-width convention illustrated by Decimal and Binary Units.

- How to read: Separate decimal units from binary units and preserve byte/word/Dword boundaries. Evidence index: Decimal and Binary Units.

- Conditions and limits: The Figure is explanatory or structural; this guide does not turn its visual relationship into a new requirement.

- Informative example: Normalize one value using Decimal and Binary Units, then verify its storage width against the cited condition before comparing it. This example adds no requirement.

- Source field index: Decimal and Binary Units

- Source keyword index: none

> Source: NVME-BASE-2.4, Rev. 2.4, §1.4.2, Figure 2, printed pages 3, PDF pages 29

</details>

<details markdown="1">
<summary><strong>Figure 3: Byte, Word, and Dword Relationships</strong></summary>

<!-- claim:BASE12-FIG-003-CLAIM figure-table:BASE12-FIG-003 -->

Figure 3, "Byte, Word, and Dword Relationships": Defines the numeric-unit or byte-width convention illustrated by Byte, Word, and Dword Relationships. Separate decimal units from binary units and preserve byte/word/Dword boundaries. Evidence index: Byte, Word, and Dword Relationships.

- Purpose: Defines the numeric-unit or byte-width convention illustrated by Byte, Word, and Dword Relationships.

- How to read: Separate decimal units from binary units and preserve byte/word/Dword boundaries. Evidence index: Byte, Word, and Dword Relationships.

- Conditions and limits: The Figure is explanatory or structural; this guide does not turn its visual relationship into a new requirement.

- Informative example: Normalize one value using Byte, Word, and Dword Relationships, then verify its storage width against the cited condition before comparing it. This example adds no requirement.

- Source field index: Byte, Word, and Dword Relationships

- Source keyword index: none

> Source: NVME-BASE-2.4, Rev. 2.4, §1.4.3, Figure 3, printed pages 5, PDF pages 31

</details>

<a id="section-2"></a>

### §2

<details markdown="1">
<summary><strong>Figure 5: Types of NVMe Command Sets</strong></summary>

<!-- claim:BASE12-FIG-005-CLAIM figure-table:BASE12-FIG-005 -->

Figure 5, "Types of NVMe Command Sets": Places Types of NVMe Command Sets in the NVMe document and command-set hierarchy. Read from the common Base requirements toward the transport and command-set layer; keep these source-derived labels distinct: Command Set, Command.

- Purpose: Places Types of NVMe Command Sets in the NVMe document and command-set hierarchy.

- How to read: Read from the common Base requirements toward the transport and command-set layer; keep these source-derived labels distinct: Command Set, Command.

- Conditions and limits: The Figure is explanatory or structural; this guide does not turn its visual relationship into a new requirement. Only the PCIe/memory-based portion is in scope.

- Informative example: Start with Command Set, then follow the branch containing Command; cite the document that owns the requirement instead of assuming every layer defines it. This example adds no requirement.

- Source field index: Command Set, Command

- Source keyword index: none

> Source: NVME-BASE-2.4, Rev. 2.4, §2, Figure 5, printed pages 21, PDF pages 47

</details>

<a id="section-2-1"></a>

### §2.1

<details markdown="1">
<summary><strong>Figure 6: Queue Pair Example, 1:1 Mapping</strong></summary>

<!-- claim:BASE12-FIG-006-CLAIM figure-table:BASE12-FIG-006 -->

Figure 6, "Queue Pair Example, 1:1 Mapping": Shows the queue or command relationship expressed by Queue Pair Example, 1:1 Mapping. Trace ownership and direction from host to SQ, controller, and CQ; keep the indexed elements distinct: Queue Pair, 1:1.

- Purpose: Shows the queue or command relationship expressed by Queue Pair Example, 1:1 Mapping.

- How to read: Trace ownership and direction from host to SQ, controller, and CQ; keep the indexed elements distinct: Queue Pair, 1:1.

- Conditions and limits: The Figure is explanatory or structural; this guide does not turn its visual relationship into a new requirement.

- Informative example: Trace one command through Figure 6, using Queue Pair and 1:1 as checkpoints for ownership or pointer movement. This example adds no requirement.

- Source field index: Queue Pair, 1:1

- Source keyword index: none

> Source: NVME-BASE-2.4, Rev. 2.4, §2.1, Figure 6, printed pages 22, PDF pages 48

</details>

<details markdown="1">
<summary><strong>Figure 7: Queue Pair Example, n:1 Mapping</strong></summary>

<!-- claim:BASE12-FIG-007-CLAIM figure-table:BASE12-FIG-007 -->

Figure 7, "Queue Pair Example, n:1 Mapping": Shows the queue or command relationship expressed by Queue Pair Example, n:1 Mapping. Trace ownership and direction from host to SQ, controller, and CQ; keep the indexed elements distinct: Queue Pair.

- Purpose: Shows the queue or command relationship expressed by Queue Pair Example, n:1 Mapping.

- How to read: Trace ownership and direction from host to SQ, controller, and CQ; keep the indexed elements distinct: Queue Pair.

- Conditions and limits: The Figure is explanatory or structural; this guide does not turn its visual relationship into a new requirement.

- Informative example: Trace one command through Figure 7, using Queue Pair and the cited condition as checkpoints for ownership or pointer movement. This example adds no requirement.

- Source field index: Queue Pair

- Source keyword index: none

> Source: NVME-BASE-2.4, Rev. 2.4, §2.1, Figure 7, printed pages 22, PDF pages 48

</details>

<a id="section-2-3"></a>

### §2.3

<details markdown="1">
<summary><strong>Figure 11: Simple NVM Storage Hierarchy with NVM Sets</strong></summary>

<!-- claim:BASE12-FIG-011-CLAIM figure-table:BASE12-FIG-011 -->

Figure 11, "Simple NVM Storage Hierarchy with NVM Sets": Shows the object or capacity relationships in Simple NVM Storage Hierarchy with NVM Sets. Separate logical identifiers from controllers, namespaces, ports, and capacity containers. Evidence index: NVM Storage Hierarchy, NVM Set.

- Purpose: Shows the object or capacity relationships in Simple NVM Storage Hierarchy with NVM Sets.

- How to read: Separate logical identifiers from controllers, namespaces, ports, and capacity containers. Evidence index: NVM Storage Hierarchy, NVM Set.

- Conditions and limits: The Figure is explanatory or structural; this guide does not turn its visual relationship into a new requirement.

- Informative example: Choose one object labeled by NVM Storage Hierarchy and trace its relationship to NVM Set without treating an identifier as the object itself. This example adds no requirement.

- Source field index: NVM Storage Hierarchy, NVM Set

- Source keyword index: none

> Source: NVME-BASE-2.4, Rev. 2.4, §2.3.1, Figure 11, printed pages 27, PDF pages 53

</details>

<details markdown="1">
<summary><strong>Figure 12: Simple NVM Storage Hierarchy with One Reclaim Group</strong></summary>

<!-- claim:BASE12-FIG-012-CLAIM figure-table:BASE12-FIG-012 -->

Figure 12, "Simple NVM Storage Hierarchy with One Reclaim Group": Shows the object or capacity relationships in Simple NVM Storage Hierarchy with One Reclaim Group. Separate logical identifiers from controllers, namespaces, ports, and capacity containers. Evidence index: NVM Storage Hierarchy, Reclaim Group.

- Purpose: Shows the object or capacity relationships in Simple NVM Storage Hierarchy with One Reclaim Group.

- How to read: Separate logical identifiers from controllers, namespaces, ports, and capacity containers. Evidence index: NVM Storage Hierarchy, Reclaim Group.

- Conditions and limits: The Figure is explanatory or structural; this guide does not turn its visual relationship into a new requirement.

- Informative example: Choose one object labeled by NVM Storage Hierarchy and trace its relationship to Reclaim Group without treating an identifier as the object itself. This example adds no requirement.

- Source field index: NVM Storage Hierarchy, Reclaim Group

- Source keyword index: none

> Source: NVME-BASE-2.4, Rev. 2.4, §2.3.1, Figure 12, printed pages 28, PDF pages 54

</details>

<details markdown="1">
<summary><strong>Figure 13: Simple NVM Storage Hierarchy with Multiple Reclaim Groups</strong></summary>

<!-- claim:BASE12-FIG-013-CLAIM figure-table:BASE12-FIG-013 -->

Figure 13, "Simple NVM Storage Hierarchy with Multiple Reclaim Groups": Shows the object or capacity relationships in Simple NVM Storage Hierarchy with Multiple Reclaim Groups. Separate logical identifiers from controllers, namespaces, ports, and capacity containers. Evidence index: NVM Storage Hierarchy, Reclaim Group.

- Purpose: Shows the object or capacity relationships in Simple NVM Storage Hierarchy with Multiple Reclaim Groups.

- How to read: Separate logical identifiers from controllers, namespaces, ports, and capacity containers. Evidence index: NVM Storage Hierarchy, Reclaim Group.

- Conditions and limits: The Figure is explanatory or structural; this guide does not turn its visual relationship into a new requirement.

- Informative example: Choose one object labeled by NVM Storage Hierarchy and trace its relationship to Reclaim Group without treating an identifier as the object itself. This example adds no requirement.

- Source field index: NVM Storage Hierarchy, Reclaim Group

- Source keyword index: none

> Source: NVME-BASE-2.4, Rev. 2.4, §2.3.1, Figure 13, printed pages 29, PDF pages 55

</details>

<details markdown="1">
<summary><strong>Figure 14: Complex NVM Storage Hierarchy with NVM Sets</strong></summary>

<!-- claim:BASE12-FIG-014-CLAIM figure-table:BASE12-FIG-014 -->

Figure 14, "Complex NVM Storage Hierarchy with NVM Sets": Shows the object or capacity relationships in Complex NVM Storage Hierarchy with NVM Sets. Separate logical identifiers from controllers, namespaces, ports, and capacity containers. Evidence index: NVM Storage Hierarchy, NVM Set.

- Purpose: Shows the object or capacity relationships in Complex NVM Storage Hierarchy with NVM Sets.

- How to read: Separate logical identifiers from controllers, namespaces, ports, and capacity containers. Evidence index: NVM Storage Hierarchy, NVM Set.

- Conditions and limits: The Figure is explanatory or structural; this guide does not turn its visual relationship into a new requirement.

- Informative example: Choose one object labeled by NVM Storage Hierarchy and trace its relationship to NVM Set without treating an identifier as the object itself. This example adds no requirement.

- Source field index: NVM Storage Hierarchy, NVM Set

- Source keyword index: none

> Source: NVME-BASE-2.4, Rev. 2.4, §2.3.1, Figure 14, printed pages 30, PDF pages 56

</details>

<details markdown="1">
<summary><strong>Figure 15: Complex NVM Storage Hierarchy with Multiple Reclaim Groups</strong></summary>

<!-- claim:BASE12-FIG-015-CLAIM figure-table:BASE12-FIG-015 -->

Figure 15, "Complex NVM Storage Hierarchy with Multiple Reclaim Groups": Shows the object or capacity relationships in Complex NVM Storage Hierarchy with Multiple Reclaim Groups. Separate logical identifiers from controllers, namespaces, ports, and capacity containers. Evidence index: NVM Storage Hierarchy, Reclaim Group.

- Purpose: Shows the object or capacity relationships in Complex NVM Storage Hierarchy with Multiple Reclaim Groups.

- How to read: Separate logical identifiers from controllers, namespaces, ports, and capacity containers. Evidence index: NVM Storage Hierarchy, Reclaim Group.

- Conditions and limits: The Figure is explanatory or structural; this guide does not turn its visual relationship into a new requirement.

- Informative example: Choose one object labeled by NVM Storage Hierarchy and trace its relationship to Reclaim Group without treating an identifier as the object itself. This example adds no requirement.

- Source field index: NVM Storage Hierarchy, Reclaim Group

- Source keyword index: none

> Source: NVME-BASE-2.4, Rev. 2.4, §2.3.1, Figure 15, printed pages 31, PDF pages 57

</details>

<details markdown="1">
<summary><strong>Figure 16: Single-Namespace NVM Subsystem</strong></summary>

<!-- claim:BASE12-FIG-016-CLAIM figure-table:BASE12-FIG-016 -->

Figure 16, "Single-Namespace NVM Subsystem": Shows the object or capacity relationships in Single-Namespace NVM Subsystem. Separate logical identifiers from controllers, namespaces, ports, and capacity containers. Evidence index: NVM Subsystem, Namespace.

- Purpose: Shows the object or capacity relationships in Single-Namespace NVM Subsystem.

- How to read: Separate logical identifiers from controllers, namespaces, ports, and capacity containers. Evidence index: NVM Subsystem, Namespace.

- Conditions and limits: The Figure is explanatory or structural; this guide does not turn its visual relationship into a new requirement.

- Informative example: Choose one object labeled by NVM Subsystem and trace its relationship to Namespace without treating an identifier as the object itself. This example adds no requirement.

- Source field index: NVM Subsystem, Namespace

- Source keyword index: none

> Source: NVME-BASE-2.4, Rev. 2.4, §2.3.3, Figure 16, printed pages 32, PDF pages 58

</details>

<details markdown="1">
<summary><strong>Figure 17: Two-Namespace NVM Subsystem</strong></summary>

<!-- claim:BASE12-FIG-017-CLAIM figure-table:BASE12-FIG-017 -->

Figure 17, "Two-Namespace NVM Subsystem": Shows the object or capacity relationships in Two-Namespace NVM Subsystem. Separate logical identifiers from controllers, namespaces, ports, and capacity containers. Evidence index: NVM Subsystem, Namespace.

- Purpose: Shows the object or capacity relationships in Two-Namespace NVM Subsystem.

- How to read: Separate logical identifiers from controllers, namespaces, ports, and capacity containers. Evidence index: NVM Subsystem, Namespace.

- Conditions and limits: The Figure is explanatory or structural; this guide does not turn its visual relationship into a new requirement.

- Informative example: Choose one object labeled by NVM Subsystem and trace its relationship to Namespace without treating an identifier as the object itself. This example adds no requirement.

- Source field index: NVM Subsystem, Namespace

- Source keyword index: none

> Source: NVME-BASE-2.4, Rev. 2.4, §2.3.3, Figure 17, printed pages 33, PDF pages 59

</details>

<details markdown="1">
<summary><strong>Figure 18: Complex NVM Subsystem</strong></summary>

<!-- claim:BASE12-FIG-018-CLAIM figure-table:BASE12-FIG-018 -->

Figure 18, "Complex NVM Subsystem": Shows the object or capacity relationships in Complex NVM Subsystem. Separate logical identifiers from controllers, namespaces, ports, and capacity containers. Evidence index: NVM Subsystem.

- Purpose: Shows the object or capacity relationships in Complex NVM Subsystem.

- How to read: Separate logical identifiers from controllers, namespaces, ports, and capacity containers. Evidence index: NVM Subsystem.

- Conditions and limits: The Figure is explanatory or structural; this guide does not turn its visual relationship into a new requirement.

- Informative example: Choose one object labeled by NVM Subsystem and trace its relationship to the cited condition without treating an identifier as the object itself. This example adds no requirement.

- Source field index: NVM Subsystem

- Source keyword index: none

> Source: NVME-BASE-2.4, Rev. 2.4, §2.3.3, Figure 18, printed pages 34, PDF pages 60

</details>

<a id="section-2-4"></a>

### §2.4

<details markdown="1">
<summary><strong>Figure 19: NVM Express Controller with Two Namespaces</strong></summary>

<!-- claim:BASE12-FIG-019-CLAIM figure-table:BASE12-FIG-019 -->

Figure 19, "NVM Express Controller with Two Namespaces": Shows the object or capacity relationships in NVM Express Controller with Two Namespaces. Separate logical identifiers from controllers, namespaces, ports, and capacity containers. Evidence index: Namespace, Controller.

- Purpose: Shows the object or capacity relationships in NVM Express Controller with Two Namespaces.

- How to read: Separate logical identifiers from controllers, namespaces, ports, and capacity containers. Evidence index: Namespace, Controller.

- Conditions and limits: The Figure is explanatory or structural; this guide does not turn its visual relationship into a new requirement.

- Informative example: Choose one object labeled by Namespace and trace its relationship to Controller without treating an identifier as the object itself. This example adds no requirement.

- Source field index: Namespace, Controller

- Source keyword index: none

> Source: NVME-BASE-2.4, Rev. 2.4, §2.4.1, Figure 19, printed pages 35, PDF pages 61

</details>

<details markdown="1">
<summary><strong>Figure 20: NVM Subsystem with Two Controllers and One Port</strong></summary>

<!-- claim:BASE12-FIG-020-CLAIM figure-table:BASE12-FIG-020 -->

Figure 20, "NVM Subsystem with Two Controllers and One Port": Shows the object or capacity relationships in NVM Subsystem with Two Controllers and One Port. Separate logical identifiers from controllers, namespaces, ports, and capacity containers. Evidence index: NVM Subsystem, Controller.

- Purpose: Shows the object or capacity relationships in NVM Subsystem with Two Controllers and One Port.

- How to read: Separate logical identifiers from controllers, namespaces, ports, and capacity containers. Evidence index: NVM Subsystem, Controller.

- Conditions and limits: The Figure is explanatory or structural; this guide does not turn its visual relationship into a new requirement.

- Informative example: Choose one object labeled by NVM Subsystem and trace its relationship to Controller without treating an identifier as the object itself. This example adds no requirement.

- Source field index: NVM Subsystem, Controller

- Source keyword index: none

> Source: NVME-BASE-2.4, Rev. 2.4, §2.4.1, Figure 20, printed pages 35, PDF pages 61

</details>

<details markdown="1">
<summary><strong>Figure 21: NVM Subsystem with Two Controllers and Two Ports</strong></summary>

<!-- claim:BASE12-FIG-021-CLAIM figure-table:BASE12-FIG-021 -->

Figure 21, "NVM Subsystem with Two Controllers and Two Ports": Shows the object or capacity relationships in NVM Subsystem with Two Controllers and Two Ports. Separate logical identifiers from controllers, namespaces, ports, and capacity containers. Evidence index: NVM Subsystem, Controller.

- Purpose: Shows the object or capacity relationships in NVM Subsystem with Two Controllers and Two Ports.

- How to read: Separate logical identifiers from controllers, namespaces, ports, and capacity containers. Evidence index: NVM Subsystem, Controller.

- Conditions and limits: The Figure is explanatory or structural; this guide does not turn its visual relationship into a new requirement.

- Informative example: Choose one object labeled by NVM Subsystem and trace its relationship to Controller without treating an identifier as the object itself. This example adds no requirement.

- Source field index: NVM Subsystem, Controller

- Source keyword index: none

> Source: NVME-BASE-2.4, Rev. 2.4, §2.4.1, Figure 21, printed pages 36, PDF pages 62

</details>

<details markdown="1">
<summary><strong>Figure 22: PCI Express Device Supporting Single Root I/O Virtualization (SR-IOV)</strong></summary>

<!-- claim:BASE12-FIG-022-CLAIM figure-table:BASE12-FIG-022 -->

Figure 22, "PCI Express Device Supporting Single Root I/O Virtualization (SR-IOV)": Shows the Physical Function and Virtual Function relationships in PCI Express Device Supporting Single Root I/O Virtualization (SR-IOV). Separate PCIe Function identity, controller ownership, and shared device resources. Evidence index: SR, IOV.

- Purpose: Shows the Physical Function and Virtual Function relationships in PCI Express Device Supporting Single Root I/O Virtualization (SR-IOV).

- How to read: Separate PCIe Function identity, controller ownership, and shared device resources. Evidence index: SR, IOV.

- Conditions and limits: The Figure is explanatory or structural; this guide does not turn its visual relationship into a new requirement.

- Informative example: Start at the function represented by SR, then trace its relationship to IOV without treating shared resources as private. This example adds no requirement.

- Source field index: SR, IOV

- Source keyword index: none

> Source: NVME-BASE-2.4, Rev. 2.4, §2.4.1, Figure 22, printed pages 37, PDF pages 63

</details>

## Use and limitations

Use the claim IDs as stable PPT traceability keys. Re-check affected claims if the source revision, errata set, or approved scope changes.
