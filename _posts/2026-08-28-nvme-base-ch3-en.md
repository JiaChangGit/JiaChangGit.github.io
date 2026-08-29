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

## Specification findings

### 1. Static controller model

<!-- claim:BASE3-STATIC -->

A memory-based controller shall support only the static controller model.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.1, printed pages 38, PDF pages 64

### 2. I/O and Administrative controllers

<!-- claim:BASE3-TYPES -->

This report uses the I/O and Administrative controller roles. The former performs user-data I/O; the latter is management-oriented and does not support data I/O commands. Both have one Admin Submission/Completion Queue pair.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.3-3.1.3.2, printed pages 39-43, PDF pages 65-69

### 3. Command and completion ordering

<!-- claim:BASE3-ORDER -->

Except for fused operations, fetched commands and completions have no general ordering guarantee. Enforcing any required order is the host's responsibility.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.3, printed pages 40, PDF pages 66

### 4. Property access width

<!-- claim:BASE3-PROPERTY -->

The host shall access a property at its starting offset using the specified width; the PCIe Transport adds the access rules for a memory-based controller.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4, printed pages 52-54, PDF pages 78-80

### 5. NSID states and special values

<!-- claim:BASE3-NAMESPACE -->

NSID 0h is invalid and FFFFFFFFh is the broadcast value. Other NSIDs still need allocated/unallocated and active/inactive classification; numeric range alone is insufficient.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.2.1, printed pages 78-80, PDF pages 104-106

### 6. Media and reclamation hierarchy

<!-- claim:BASE3-MEDIA -->

NVM Sets, Endurance Groups, Reclaim Groups, and Reclaim Units describe capacity grouping, endurance management, and reclamation granularity. Support and identifiers are determined from Identify data and log-page capabilities.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.2.2-3.2.4, printed pages 80-85, PDF pages 106-111

### 7. Domain boundaries and identifiers

<!-- claim:BASE3-DOMAIN -->

A domain is a failure or communication boundary inside an NVM subsystem. In a multi-domain subsystem, each domain identifier shall be unique within that subsystem.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.2.5, printed pages 85-88, PDF pages 111-114

### 8. PCIe queue creation and pointers

<!-- claim:BASE3-QUEUE -->

A PCIe queue is a circular buffer in host-addressable memory with head and tail pointers. The host creates an I/O Completion Queue before its Submission Queue and advances pointers through doorbells.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.3.1, printed pages 88-91, PDF pages 114-117

### 9. Command processing and arbitration

<!-- claim:BASE3-PROCESS -->

Command processing separates ordering, fused and atomic semantics, arbitration, and outstanding-command limits. Priority belongs to a Submission Queue, not to each command as an independent attribute.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.4.1-3.4.5, printed pages 101-105, PDF pages 127-131

### 10. Controller initialization

<!-- claim:BASE3-INIT -->

PCIe initialization reads CAP, configures AQA/ASQ/ACQ and CC, then waits for CSTS.RDY. Ready mode and CRTO affect host wait and error handling.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.5.1, 3.5.3-3.5.4, printed pages 105-113, PDF pages 131-139

### 11. Shutdown state flow

<!-- claim:BASE3-SHUTDOWN -->

Normal shutdown begins when the host sets CC.SHN and the controller reports progress in CSTS.SHST. NVM subsystem shutdown has a wider scope and is not the same as one controller shutdown.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.6.1, 3.6.3, printed pages 113-120, PDF pages 139-146

### 12. Reset levels and scope

<!-- claim:BASE3-RESET -->

NVM Subsystem, Controller Level, and Queue Level resets have different scopes. A recovery flow first determines which state is cleared and whether queues still exist.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.7, printed pages 120-125, PDF pages 146-151

### 13. Capacity model

<!-- claim:BASE3-CAPACITY -->

The capacity model tracks available or configured capacity separately at subsystem, Endurance Group, NVM Set, and namespace levels. Values from different levels are not directly interchangeable.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.8, printed pages 125-129, PDF pages 151-155

### 14. Keep Alive timers

<!-- claim:BASE3-KEEPALIVE -->

Keep Alive uses KATO and KATT for host/controller liveness monitoring. This report retains only controller-common and PCIe-applicable timer, command, and timeout behavior.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.9, printed pages 129-135, PDF pages 155-161

### 15. Firmware updates and privileged actions

<!-- claim:BASE3-FIRMWARE -->

A privileged action may affect other hosts or controllers. Firmware update separates image download, commit/activation, and any required reset; the host sequences the flow using the reported activation action.

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

## Figure-by-Figure Guide

The source uses Figure numbers for diagrams and field-layout tables. No source artwork is reproduced; compact field and keyword indexes come from the locally verified PDFs.

<a id="section-3-1"></a>

### §3.1

<details markdown="1">
<summary><strong>Figure 23: Controller Types</strong></summary>

<!-- claim:BASE3-FIG-023-CLAIM figure-table:BASE3-FIG-023 -->

Figure 23, "Controller Types": Shows the object or capacity relationships in Controller Types. Separate logical identifiers from controllers, namespaces, ports, and capacity containers. Evidence index: Controller.

- Purpose: Shows the object or capacity relationships in Controller Types.

- How to read: Separate logical identifiers from controllers, namespaces, ports, and capacity containers. Evidence index: Controller.

- Conditions and limits: The Figure is explanatory or structural; this guide does not turn its visual relationship into a new requirement. Only the PCIe/memory-based portion is in scope.

- Informative example: Choose one object labeled by Controller and trace its relationship to the cited condition without treating an identifier as the object itself. This example adds no requirement.

- Source field index: Controller

- Source keyword index: none

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.3, Figure 23, printed pages 39, PDF pages 65

</details>

<details markdown="1">
<summary><strong>Figure 24: NVM Subsystem with Three I/O Controllers</strong></summary>

<!-- claim:BASE3-FIG-024-CLAIM figure-table:BASE3-FIG-024 -->

Figure 24, "NVM Subsystem with Three I/O Controllers": Shows the object or capacity relationships in NVM Subsystem with Three I/O Controllers. Separate logical identifiers from controllers, namespaces, ports, and capacity containers. Evidence index: NVM Subsystem, I/O Controller, Controller.

- Purpose: Shows the object or capacity relationships in NVM Subsystem with Three I/O Controllers.

- How to read: Separate logical identifiers from controllers, namespaces, ports, and capacity containers. Evidence index: NVM Subsystem, I/O Controller, Controller.

- Conditions and limits: The Figure is explanatory or structural; this guide does not turn its visual relationship into a new requirement.

- Informative example: Choose one object labeled by NVM Subsystem and trace its relationship to I/O Controller without treating an identifier as the object itself. This example adds no requirement.

- Source field index: NVM Subsystem, I/O Controller, Controller

- Source keyword index: none

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.3.1, Figure 24, printed pages 41, PDF pages 67

</details>

<details markdown="1">
<summary><strong>Figure 25: NVM Subsystem with One Administrative and Two I/O Controllers</strong></summary>

<!-- claim:BASE3-FIG-025-CLAIM figure-table:BASE3-FIG-025 -->

Figure 25, "NVM Subsystem with One Administrative and Two I/O Controllers": Shows the object or capacity relationships in NVM Subsystem with One Administrative and Two I/O Controllers. Separate logical identifiers from controllers, namespaces, ports, and capacity containers. Evidence index: NVM Subsystem, I/O Controller, Controller.

- Purpose: Shows the object or capacity relationships in NVM Subsystem with One Administrative and Two I/O Controllers.

- How to read: Separate logical identifiers from controllers, namespaces, ports, and capacity containers. Evidence index: NVM Subsystem, I/O Controller, Controller.

- Conditions and limits: The Figure is explanatory or structural; this guide does not turn its visual relationship into a new requirement.

- Informative example: Choose one object labeled by NVM Subsystem and trace its relationship to I/O Controller without treating an identifier as the object itself. This example adds no requirement.

- Source field index: NVM Subsystem, I/O Controller, Controller

- Source keyword index: none

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.3.2, Figure 25, printed pages 42, PDF pages 68

</details>

<details markdown="1">
<summary><strong>Figure 26: NVM Subsystem with One Administrative Controller</strong></summary>

<!-- claim:BASE3-FIG-026-CLAIM figure-table:BASE3-FIG-026 -->

Figure 26, "NVM Subsystem with One Administrative Controller": Shows the object or capacity relationships in NVM Subsystem with One Administrative Controller. Separate logical identifiers from controllers, namespaces, ports, and capacity containers. Evidence index: NVM Subsystem, Administrative Controller, Controller.

- Purpose: Shows the object or capacity relationships in NVM Subsystem with One Administrative Controller.

- How to read: Separate logical identifiers from controllers, namespaces, ports, and capacity containers. Evidence index: NVM Subsystem, Administrative Controller, Controller.

- Conditions and limits: The Figure is explanatory or structural; this guide does not turn its visual relationship into a new requirement.

- Informative example: Choose one object labeled by NVM Subsystem and trace its relationship to Administrative Controller without treating an identifier as the object itself. This example adds no requirement.

- Source field index: NVM Subsystem, Administrative Controller, Controller

- Source keyword index: none

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.3.2, Figure 26, printed pages 42, PDF pages 68

</details>

<details markdown="1">
<summary><strong>Figure 27: Controller IDs FFF0h to FFFFh</strong></summary>

<!-- claim:BASE3-FIG-027-CLAIM figure-table:BASE3-FIG-027 -->

Figure 27, "Controller IDs FFF0h to FFFFh": Defines the identifier composition or namespace of values shown by Controller IDs FFF0h to FFFFh. Keep the value width, issuing authority, uniqueness scope, and reserved values separate. Evidence index: Controller, Controller ID.

- Purpose: Defines the identifier composition or namespace of values shown by Controller IDs FFF0h to FFFFh.

- How to read: Keep the value width, issuing authority, uniqueness scope, and reserved values separate. Evidence index: Controller, Controller ID.

- Conditions and limits: The Figure is explanatory or structural; this guide does not turn its visual relationship into a new requirement.

- Informative example: Parse Controller at its defined width, then validate the scope associated with Controller ID before using it as an identity key. This example adds no requirement.

- Source field index: Controller, Controller ID

- Source keyword index: none

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.3.3, Figure 27, printed pages 44, PDF pages 70

</details>

<details markdown="1">
<summary><strong>Figure 28: Admin Command Support Requirements</strong></summary>

<!-- claim:BASE3-FIG-028-CLAIM figure-table:BASE3-FIG-028 -->

Figure 28, "Admin Command Support Requirements": Summarizes the support levels assigned by Admin Command Support Requirements. Resolve the row and controller/command-set context before interpreting its support marker. Evidence index: MI, O10, O11, Command.

- Purpose: Summarizes the support levels assigned by Admin Command Support Requirements.

- How to read: Resolve the row and controller/command-set context before interpreting its support marker. Evidence index: MI, O10, O11, Command.

- Conditions and limits: Source keyword index: `optional`. The index locates normative language but does not replace the condition attached to each field. Only the PCIe/memory-based portion is in scope.

- Informative example: Look up MI in the applicable row, then confirm the context identified by O10 before labeling it required or optional. This example adds no requirement.

- Source field index: MI, O10, O11, Command

- Source keyword index: `optional`

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.3.3.3, Figure 28, printed pages 45-47, PDF pages 71-73

</details>

<details markdown="1">
<summary><strong>Figure 30: Common I/O Command Support Requirements</strong></summary>

<!-- claim:BASE3-FIG-030-CLAIM figure-table:BASE3-FIG-030 -->

Figure 30, "Common I/O Command Support Requirements": Summarizes the support levels assigned by Common I/O Command Support Requirements. Resolve the row and controller/command-set context before interpreting its support marker. Evidence index: FDPS, Command.

- Purpose: Summarizes the support levels assigned by Common I/O Command Support Requirements.

- How to read: Resolve the row and controller/command-set context before interpreting its support marker. Evidence index: FDPS, Command.

- Conditions and limits: Source keyword index: `optional`. The index locates normative language but does not replace the condition attached to each field. Only the PCIe/memory-based portion is in scope.

- Informative example: Look up FDPS in the applicable row, then confirm the context identified by Command before labeling it required or optional. This example adds no requirement.

- Source field index: FDPS, Command

- Source keyword index: `optional`

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.3.4, Figure 30, printed pages 47-48, PDF pages 73-74

</details>

<details markdown="1">
<summary><strong>Figure 31: Log Page Support Requirements</strong></summary>

<!-- claim:BASE3-FIG-031-CLAIM figure-table:BASE3-FIG-031 -->

Figure 31, "Log Page Support Requirements": Summarizes the support levels assigned by Log Page Support Requirements. Resolve the row and controller/command-set context before interpreting its support marker. Evidence index: M3, SMART, O4, O6, O12, O13, FDP, O5.

- Purpose: Summarizes the support levels assigned by Log Page Support Requirements.

- How to read: Resolve the row and controller/command-set context before interpreting its support marker. Evidence index: M3, SMART, O4, O6, O12, O13, FDP, O5.

- Conditions and limits: Source keyword index: `shall`, `optional`. The index locates normative language but does not replace the condition attached to each field. Only the PCIe/memory-based portion is in scope.

- Informative example: Look up M3 in the applicable row, then confirm the context identified by SMART before labeling it required or optional. This example adds no requirement.

- Source field index: M3, SMART, O4, O6, O12, O13, FDP, O5

- Source keyword index: `shall`, `optional`

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.3.4, Figure 31, printed pages 48-50, PDF pages 74-76

</details>

<details markdown="1">
<summary><strong>Figure 32: Feature Support Requirements</strong></summary>

<!-- claim:BASE3-FIG-032-CLAIM figure-table:BASE3-FIG-032 -->

Figure 32, "Feature Support Requirements": Summarizes the support levels assigned by Feature Support Requirements. Resolve the row and controller/command-set context before interpreting its support marker. Evidence index: LBA, O8, M10, M7, O9, O6, O5, O3.

- Purpose: Summarizes the support levels assigned by Feature Support Requirements.

- How to read: Resolve the row and controller/command-set context before interpreting its support marker. Evidence index: LBA, O8, M10, M7, O9, O6, O5, O3.

- Conditions and limits: Source keyword index: `optional`. The index locates normative language but does not replace the condition attached to each field. Only the PCIe/memory-based portion is in scope.

- Informative example: Look up LBA in the applicable row, then confirm the context identified by O8 before labeling it required or optional. This example adds no requirement.

- Source field index: LBA, O8, M10, M7, O9, O6, O5, O3

- Source keyword index: `optional`

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.3.5, Figure 32, printed pages 50-52, PDF pages 76-78

</details>

<details markdown="1">
<summary><strong>Figure 33: Property Definition</strong></summary>

<!-- claim:BASE3-FIG-033-CLAIM figure-table:BASE3-FIG-033 -->

Figure 33, "Property Definition": Defines the concrete layout or value relationships for Property Definition. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is OFST, CAP, VS, M2, INTMS, INTMC, CC, CSTS.

- Purpose: Defines the concrete layout or value relationships for Property Definition.

- How to read: Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is OFST, CAP, VS, M2, INTMS, INTMC, CC, CSTS.

- Conditions and limits: Source keyword index: `optional`, `reserved`. The index locates normative language but does not replace the condition attached to each field. Only the PCIe/memory-based portion is in scope.

- Informative example: Use OFST as the first parser checkpoint and CAP as a second, independent boundary check. This example adds no requirement.

- Source field index: OFST, CAP, VS, M2, INTMS, INTMC, CC, CSTS

- Source keyword index: `optional`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4, Figure 33, printed pages 52-53, PDF pages 78-79

</details>

<details markdown="1">
<summary><strong>Figure 34: Memory-Based Property Definition</strong></summary>

<!-- claim:BASE3-FIG-034-CLAIM figure-table:BASE3-FIG-034 -->

Figure 34, "Memory-Based Property Definition": Defines the concrete layout or value relationships for Memory-Based Property Definition. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is OFST, CAP.DSTRD.

- Purpose: Defines the concrete layout or value relationships for Memory-Based Property Definition.

- How to read: Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is OFST, CAP.DSTRD.

- Conditions and limits: Source keyword index: `optional`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Use OFST as the first parser checkpoint and CAP.DSTRD as a second, independent boundary check. This example adds no requirement.

- Source field index: OFST, CAP.DSTRD

- Source keyword index: `optional`

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4, Figure 34, printed pages 54, PDF pages 80

</details>

<details markdown="1">
<summary><strong>Figure 36: Offset 0h: CAP - Controller Capabilities</strong></summary>

<!-- claim:BASE3-FIG-036-CLAIM figure-table:BASE3-FIG-036 -->

Figure 36, "Offset 0h: CAP - Controller Capabilities": Defines CAP (Controller Capabilities) at offset 0h and identifies the fields that software must decode at that location. Start at CAP, then map bit ranges to access type, reset value, and field meaning. Evidence index: NSSES, CRMS, CRIMS, CRWMS, NSSS, CMBS, PMRS, MPSMAX.

- Purpose: Defines CAP (Controller Capabilities) at offset 0h and identifies the fields that software must decode at that location.

- How to read: Start at CAP, then map bit ranges to access type, reset value, and field meaning. Evidence index: NSSES, CRMS, CRIMS, CRWMS, NSSS, CMBS, PMRS, MPSMAX.

- Conditions and limits: Source keyword index: `shall not`, `shall`, `should`, `may`, `optional`, `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Read CAP with the required width, then verify NSSES and CRMS separately before using either value. This example adds no requirement.

- Source field index: NSSES, CRMS, CRIMS, CRWMS, NSSS, CMBS, PMRS, MPSMAX

- Source keyword index: `shall not`, `shall`, `should`, `may`, `optional`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.1, Figure 36, printed pages 55-58, PDF pages 81-84

</details>

<details markdown="1">
<summary><strong>Figure 37: Specification Version Descriptor</strong></summary>

<!-- claim:BASE3-FIG-037-CLAIM figure-table:BASE3-FIG-037 -->

Figure 37, "Specification Version Descriptor": Defines the concrete layout or value relationships for Specification Version Descriptor. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is MJR, MNR, TER.

- Purpose: Defines the concrete layout or value relationships for Specification Version Descriptor.

- How to read: Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is MJR, MNR, TER.

- Conditions and limits: The Figure is explanatory or structural; this guide does not turn its visual relationship into a new requirement.

- Informative example: Use MJR as the first parser checkpoint and MNR as a second, independent boundary check. This example adds no requirement.

- Source field index: MJR, MNR, TER

- Source keyword index: none

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.1, Figure 37, printed pages 58, PDF pages 84

</details>

<details markdown="1">
<summary><strong>Figure 38: NVM Express Base Specification Version Property Reset Values</strong></summary>

<!-- claim:BASE3-FIG-038-CLAIM figure-table:BASE3-FIG-038 -->

Figure 38, "NVM Express Base Specification Version Property Reset Values": Defines the concrete layout or value relationships for NVM Express Base Specification Version Property Reset Values. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is MJR, MNR, TER.

- Purpose: Defines the concrete layout or value relationships for NVM Express Base Specification Version Property Reset Values.

- How to read: Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is MJR, MNR, TER.

- Conditions and limits: The Figure is explanatory or structural; this guide does not turn its visual relationship into a new requirement.

- Informative example: Use MJR as the first parser checkpoint and MNR as a second, independent boundary check. This example adds no requirement.

- Source field index: MJR, MNR, TER

- Source keyword index: none

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.1, Figure 38, printed pages 58-59, PDF pages 84-85

</details>

<details markdown="1">
<summary><strong>Figure 39: Offset Ch: INTMS - Interrupt Mask Set</strong></summary>

<!-- claim:BASE3-FIG-039-CLAIM figure-table:BASE3-FIG-039 -->

Figure 39, "Offset Ch: INTMS - Interrupt Mask Set": Defines INTMS (Interrupt Mask Set) at offset Ch and identifies the fields that software must decode at that location. Start at INTMS, then map bit ranges to access type, reset value, and field meaning. Evidence index: IVMS, INTMS, RWS, MSI, Interrupt.

- Purpose: Defines INTMS (Interrupt Mask Set) at offset Ch and identifies the fields that software must decode at that location.

- How to read: Start at INTMS, then map bit ranges to access type, reset value, and field meaning. Evidence index: IVMS, INTMS, RWS, MSI, Interrupt.

- Conditions and limits: The Figure is explanatory or structural; this guide does not turn its visual relationship into a new requirement.

- Informative example: Read INTMS with the required width, then verify IVMS and INTMS separately before using either value. This example adds no requirement.

- Source field index: IVMS, INTMS, RWS, MSI, Interrupt

- Source keyword index: none

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.2, Figure 39, printed pages 59, PDF pages 85

</details>

<details markdown="1">
<summary><strong>Figure 40: Offset 10h: INTMC - Interrupt Mask Clear</strong></summary>

<!-- claim:BASE3-FIG-040-CLAIM figure-table:BASE3-FIG-040 -->

Figure 40, "Offset 10h: INTMC - Interrupt Mask Clear": Defines INTMC (Interrupt Mask Clear) at offset 10h and identifies the fields that software must decode at that location. Start at INTMC, then map bit ranges to access type, reset value, and field meaning. Evidence index: IVMC, INTMC, RWC, Interrupt.

- Purpose: Defines INTMC (Interrupt Mask Clear) at offset 10h and identifies the fields that software must decode at that location.

- How to read: Start at INTMC, then map bit ranges to access type, reset value, and field meaning. Evidence index: IVMC, INTMC, RWC, Interrupt.

- Conditions and limits: The Figure is explanatory or structural; this guide does not turn its visual relationship into a new requirement.

- Informative example: Read INTMC with the required width, then verify IVMC and INTMC separately before using either value. This example adds no requirement.

- Source field index: IVMC, INTMC, RWC, Interrupt

- Source keyword index: none

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.2, Figure 40, printed pages 59, PDF pages 85

</details>

<details markdown="1">
<summary><strong>Figure 41: Offset 14h: CC - Controller Configuration</strong></summary>

<!-- claim:BASE3-FIG-041-CLAIM figure-table:BASE3-FIG-041 -->

Figure 41, "Offset 14h: CC - Controller Configuration": Defines CC (Controller Configuration) at offset 14h and identifies the fields that software must decode at that location. Start at CC, then map bit ranges to access type, reset value, and field meaning. Evidence index: CRIME, SHN, AMS, MPS, CSS, EN, CC, CC.EN.

- Purpose: Defines CC (Controller Configuration) at offset 14h and identifies the fields that software must decode at that location.

- How to read: Start at CC, then map bit ranges to access type, reset value, and field meaning. Evidence index: CRIME, SHN, AMS, MPS, CSS, EN, CC, CC.EN.

- Conditions and limits: Source keyword index: `shall not`, `shall`, `should`, `may`, `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Read CC with the required width, then verify CRIME and SHN separately before using either value. This example adds no requirement.

- Source field index: CRIME, SHN, AMS, MPS, CSS, EN, CC, CC.EN

- Source keyword index: `shall not`, `shall`, `should`, `may`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.5, Figure 41, printed pages 60-63, PDF pages 86-89

</details>

<details markdown="1">
<summary><strong>Figure 42: Offset 1Ch: CSTS - Controller Status</strong></summary>

<!-- claim:BASE3-FIG-042-CLAIM figure-table:BASE3-FIG-042 -->

Figure 42, "Offset 1Ch: CSTS - Controller Status": Defines CSTS (Controller Status) at offset 1Ch and identifies the fields that software must decode at that location. Start at CSTS, then map bit ranges to access type, reset value, and field meaning. Evidence index: ST, PP, NSSRO, SHST, CLR, CFS, RDY, CSTS.

- Purpose: Defines CSTS (Controller Status) at offset 1Ch and identifies the fields that software must decode at that location.

- How to read: Start at CSTS, then map bit ranges to access type, reset value, and field meaning. Evidence index: ST, PP, NSSRO, SHST, CLR, CFS, RDY, CSTS.

- Conditions and limits: Source keyword index: `shall not`, `should not`, `shall`, `should`, `may`, `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Read CSTS with the required width, then verify ST and PP separately before using either value. This example adds no requirement.

- Source field index: ST, PP, NSSRO, SHST, CLR, CFS, RDY, CSTS

- Source keyword index: `shall not`, `should not`, `shall`, `should`, `may`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.5, Figure 42, printed pages 63-65, PDF pages 89-91

</details>

<details markdown="1">
<summary><strong>Figure 43: Offset 20h: NSSR - NVM Subsystem Reset</strong></summary>

<!-- claim:BASE3-FIG-043-CLAIM figure-table:BASE3-FIG-043 -->

Figure 43, "Offset 20h: NSSR - NVM Subsystem Reset": Defines NSSR (NVM Subsystem Reset) at offset 20h and identifies the fields that software must decode at that location. Start at NSSR, then map bit ranges to access type, reset value, and field meaning. Evidence index: NSSRC, NSSR, NVM Subsystem.

- Purpose: Defines NSSR (NVM Subsystem Reset) at offset 20h and identifies the fields that software must decode at that location.

- How to read: Start at NSSR, then map bit ranges to access type, reset value, and field meaning. Evidence index: NSSRC, NSSR, NVM Subsystem.

- Conditions and limits: Source keyword index: `shall`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Read NSSR with the required width, then verify NSSRC and NSSR separately before using either value. This example adds no requirement.

- Source field index: NSSRC, NSSR, NVM Subsystem

- Source keyword index: `shall`

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.6, Figure 43, printed pages 66, PDF pages 92

</details>

<details markdown="1">
<summary><strong>Figure 44: Offset 24h: AQA - Admin Queue Attributes</strong></summary>

<!-- claim:BASE3-FIG-044-CLAIM figure-table:BASE3-FIG-044 -->

Figure 44, "Offset 24h: AQA - Admin Queue Attributes": Defines AQA (Admin Queue Attributes) at offset 24h and identifies the fields that software must decode at that location. Start at AQA, then map bit ranges to access type, reset value, and field meaning. Evidence index: ACQS, ASQS, AQA.

- Purpose: Defines AQA (Admin Queue Attributes) at offset 24h and identifies the fields that software must decode at that location.

- How to read: Start at AQA, then map bit ranges to access type, reset value, and field meaning. Evidence index: ACQS, ASQS, AQA.

- Conditions and limits: Source keyword index: `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Read AQA with the required width, then verify ACQS and ASQS separately before using either value. This example adds no requirement.

- Source field index: ACQS, ASQS, AQA

- Source keyword index: `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.6, Figure 44, printed pages 66, PDF pages 92

</details>

<details markdown="1">
<summary><strong>Figure 45: Offset 28h: ASQ - Admin Submission Queue Base Address</strong></summary>

<!-- claim:BASE3-FIG-045-CLAIM figure-table:BASE3-FIG-045 -->

Figure 45, "Offset 28h: ASQ - Admin Submission Queue Base Address": Defines ASQ (Admin Submission Queue Base Address) at offset 28h and identifies the fields that software must decode at that location. Start at ASQ, then map bit ranges to access type, reset value, and field meaning. Evidence index: ASQB, ASQ, CC.MPS, Submission Queue.

- Purpose: Defines ASQ (Admin Submission Queue Base Address) at offset 28h and identifies the fields that software must decode at that location.

- How to read: Start at ASQ, then map bit ranges to access type, reset value, and field meaning. Evidence index: ASQB, ASQ, CC.MPS, Submission Queue.

- Conditions and limits: Source keyword index: `shall`, `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Read ASQ with the required width, then verify ASQB and ASQ separately before using either value. This example adds no requirement.

- Source field index: ASQB, ASQ, CC.MPS, Submission Queue

- Source keyword index: `shall`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.6, Figure 45, printed pages 66, PDF pages 92

</details>

<details markdown="1">
<summary><strong>Figure 46: Offset 30h: ACQ - Admin Completion Queue Base Address</strong></summary>

<!-- claim:BASE3-FIG-046-CLAIM figure-table:BASE3-FIG-046 -->

Figure 46, "Offset 30h: ACQ - Admin Completion Queue Base Address": Defines ACQ (Admin Completion Queue Base Address) at offset 30h and identifies the fields that software must decode at that location. Start at ACQ, then map bit ranges to access type, reset value, and field meaning. Evidence index: ACQB, ACQ, CC.MPS, Completion Queue.

- Purpose: Defines ACQ (Admin Completion Queue Base Address) at offset 30h and identifies the fields that software must decode at that location.

- How to read: Start at ACQ, then map bit ranges to access type, reset value, and field meaning. Evidence index: ACQB, ACQ, CC.MPS, Completion Queue.

- Conditions and limits: Source keyword index: `shall`, `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Read ACQ with the required width, then verify ACQB and ACQ separately before using either value. This example adds no requirement.

- Source field index: ACQB, ACQ, CC.MPS, Completion Queue

- Source keyword index: `shall`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.9, Figure 46, printed pages 67, PDF pages 93

</details>

<details markdown="1">
<summary><strong>Figure 47: Offset 38h: CMBLOC - Controller Memory Buffer Location</strong></summary>

<!-- claim:BASE3-FIG-047-CLAIM figure-table:BASE3-FIG-047 -->

Figure 47, "Offset 38h: CMBLOC - Controller Memory Buffer Location": Defines CMBLOC (Controller Memory Buffer Location) at offset 38h and identifies the fields that software must decode at that location. Start at CMBLOC, then map bit ranges to access type, reset value, and field meaning. Evidence index: CQMMS, BIR, CMBLOC, CMB, BAR, Controller.

- Purpose: Defines CMBLOC (Controller Memory Buffer Location) at offset 38h and identifies the fields that software must decode at that location.

- How to read: Start at CMBLOC, then map bit ranges to access type, reset value, and field meaning. Evidence index: CQMMS, BIR, CMBLOC, CMB, BAR, Controller.

- Conditions and limits: Source keyword index: `shall`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Read CMBLOC with the required width, then verify CQMMS and BIR separately before using either value. This example adds no requirement.

- Source field index: CQMMS, BIR, CMBLOC, CMB, BAR, Controller

- Source keyword index: `shall`

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.9, Figure 47, printed pages 67-68, PDF pages 93-94

</details>

<details markdown="1">
<summary><strong>Figure 48: Offset 3Ch: CMBSZ - Controller Memory Buffer Size</strong></summary>

<!-- claim:BASE3-FIG-048-CLAIM figure-table:BASE3-FIG-048 -->

Figure 48, "Offset 3Ch: CMBSZ - Controller Memory Buffer Size": Defines CMBSZ (Controller Memory Buffer Size) at offset 3Ch and identifies the fields that software must decode at that location. Start at CMBSZ, then map bit ranges to access type, reset value, and field meaning. Evidence index: SZ, SZU, WDS, RDS, LISTS, CQS, SQS, CMBSZ.

- Purpose: Defines CMBSZ (Controller Memory Buffer Size) at offset 3Ch and identifies the fields that software must decode at that location.

- How to read: Start at CMBSZ, then map bit ranges to access type, reset value, and field meaning. Evidence index: SZ, SZU, WDS, RDS, LISTS, CQS, SQS, CMBSZ.

- Conditions and limits: Source keyword index: `shall not`, `shall`, `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Read CMBSZ with the required width, then verify SZ and SZU separately before using either value. This example adds no requirement.

- Source field index: SZ, SZU, WDS, RDS, LISTS, CQS, SQS, CMBSZ

- Source keyword index: `shall not`, `shall`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.11, Figure 48, printed pages 68-69, PDF pages 94-95

</details>

<details markdown="1">
<summary><strong>Figure 49: Offset 40h: BPINFO - Boot Partition Information</strong></summary>

<!-- claim:BASE3-FIG-049-CLAIM figure-table:BASE3-FIG-049 -->

Figure 49, "Offset 40h: BPINFO - Boot Partition Information": Defines BPINFO (Boot Partition Information) at offset 40h and identifies the fields that software must decode at that location. Start at BPINFO, then map bit ranges to access type, reset value, and field meaning. Evidence index: ABPID, BRS, BPSZ, BPINFO, ID, BPRSEL.BPID.

- Purpose: Defines BPINFO (Boot Partition Information) at offset 40h and identifies the fields that software must decode at that location.

- How to read: Start at BPINFO, then map bit ranges to access type, reset value, and field meaning. Evidence index: ABPID, BRS, BPSZ, BPINFO, ID, BPRSEL.BPID.

- Conditions and limits: Source keyword index: `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Read BPINFO with the required width, then verify ABPID and BRS separately before using either value. This example adds no requirement.

- Source field index: ABPID, BRS, BPSZ, BPINFO, ID, BPRSEL.BPID

- Source keyword index: `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.12, Figure 49, printed pages 69, PDF pages 95

</details>

<details markdown="1">
<summary><strong>Figure 50: Offset 44h: BPRSEL - Boot Partition Read Select</strong></summary>

<!-- claim:BASE3-FIG-050-CLAIM figure-table:BASE3-FIG-050 -->

Figure 50, "Offset 44h: BPRSEL - Boot Partition Read Select": Defines BPRSEL (Boot Partition Read Select) at offset 44h and identifies the fields that software must decode at that location. Start at BPRSEL, then map bit ranges to access type, reset value, and field meaning. Evidence index: BPID, BPROF, BPRSZ, BPRSEL.

- Purpose: Defines BPRSEL (Boot Partition Read Select) at offset 44h and identifies the fields that software must decode at that location.

- How to read: Start at BPRSEL, then map bit ranges to access type, reset value, and field meaning. Evidence index: BPID, BPROF, BPRSZ, BPRSEL.

- Conditions and limits: Source keyword index: `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Read BPRSEL with the required width, then verify BPID and BPROF separately before using either value. This example adds no requirement.

- Source field index: BPID, BPROF, BPRSZ, BPRSEL

- Source keyword index: `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.12, Figure 50, printed pages 69-70, PDF pages 95-96

</details>

<details markdown="1">
<summary><strong>Figure 51: Offset 48h: BPMBL - Boot Partition Memory Buffer Location</strong></summary>

<!-- claim:BASE3-FIG-051-CLAIM figure-table:BASE3-FIG-051 -->

Figure 51, "Offset 48h: BPMBL - Boot Partition Memory Buffer Location": Defines BPMBL (Boot Partition Memory Buffer Location) at offset 48h and identifies the fields that software must decode at that location. Start at BPMBL, then map bit ranges to access type, reset value, and field meaning. Evidence index: BMBBA, BPMBL.

- Purpose: Defines BPMBL (Boot Partition Memory Buffer Location) at offset 48h and identifies the fields that software must decode at that location.

- How to read: Start at BPMBL, then map bit ranges to access type, reset value, and field meaning. Evidence index: BMBBA, BPMBL.

- Conditions and limits: Source keyword index: `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Read BPMBL with the required width, then verify BMBBA and BPMBL separately before using either value. This example adds no requirement.

- Source field index: BMBBA, BPMBL

- Source keyword index: `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.14, Figure 51, printed pages 70, PDF pages 96

</details>

<details markdown="1">
<summary><strong>Figure 52: Offset 50h: CMBMSC - Controller Memory Buffer Memory Space Control</strong></summary>

<!-- claim:BASE3-FIG-052-CLAIM figure-table:BASE3-FIG-052 -->

Figure 52, "Offset 50h: CMBMSC - Controller Memory Buffer Memory Space Control": Defines CMBMSC (Controller Memory Buffer Memory Space Control) at offset 50h and identifies the fields that software must decode at that location. Start at CMBMSC, then map bit ranges to access type, reset value, and field meaning. Evidence index: CBA, CMSE, CRE, CMBMSC, CMBSMSC.CRE, CMBLOC, CMBSZ, Controller.

- Purpose: Defines CMBMSC (Controller Memory Buffer Memory Space Control) at offset 50h and identifies the fields that software must decode at that location.

- How to read: Start at CMBMSC, then map bit ranges to access type, reset value, and field meaning. Evidence index: CBA, CMSE, CRE, CMBMSC, CMBSMSC.CRE, CMBLOC, CMBSZ, Controller.

- Conditions and limits: Source keyword index: `shall`, `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Read CMBMSC with the required width, then verify CBA and CMSE separately before using either value. This example adds no requirement.

- Source field index: CBA, CMSE, CRE, CMBMSC, CMBSMSC.CRE, CMBLOC, CMBSZ, Controller

- Source keyword index: `shall`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.14, Figure 52, printed pages 70-71, PDF pages 96-97

</details>

<details markdown="1">
<summary><strong>Figure 53: Offset 58h: CMBSTS - Controller Memory Buffer Status</strong></summary>

<!-- claim:BASE3-FIG-053-CLAIM figure-table:BASE3-FIG-053 -->

Figure 53, "Offset 58h: CMBSTS - Controller Memory Buffer Status": Defines CMBSTS (Controller Memory Buffer Status) at offset 58h and identifies the fields that software must decode at that location. Start at CMBSTS, then map bit ranges to access type, reset value, and field meaning. Evidence index: CBAI, CMBSTS, CMBMSC.CBA, CMBMSC.CRE, CMBMSC.CMSE, Controller.

- Purpose: Defines CMBSTS (Controller Memory Buffer Status) at offset 58h and identifies the fields that software must decode at that location.

- How to read: Start at CMBSTS, then map bit ranges to access type, reset value, and field meaning. Evidence index: CBAI, CMBSTS, CMBMSC.CBA, CMBMSC.CRE, CMBMSC.CMSE, Controller.

- Conditions and limits: Source keyword index: `shall`, `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Read CMBSTS with the required width, then verify CBAI and CMBSTS separately before using either value. This example adds no requirement.

- Source field index: CBAI, CMBSTS, CMBMSC.CBA, CMBMSC.CRE, CMBMSC.CMSE, Controller

- Source keyword index: `shall`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.16, Figure 53, printed pages 71, PDF pages 97

</details>

<details markdown="1">
<summary><strong>Figure 54: Offset 5Ch: CMBEBS - Controller Memory Buffer Elasticity Buffer Size</strong></summary>

<!-- claim:BASE3-FIG-054-CLAIM figure-table:BASE3-FIG-054 -->

Figure 54, "Offset 5Ch: CMBEBS - Controller Memory Buffer Elasticity Buffer Size": Defines CMBEBS (Controller Memory Buffer Elasticity Buffer Size) at offset 5Ch and identifies the fields that software must decode at that location. Start at CMBEBS, then map bit ranges to access type, reset value, and field meaning. Evidence index: CMBWBZ, CMBRBB, CMBSZU, CMBEBS, CMB, Controller.

- Purpose: Defines CMBEBS (Controller Memory Buffer Elasticity Buffer Size) at offset 5Ch and identifies the fields that software must decode at that location.

- How to read: Start at CMBEBS, then map bit ranges to access type, reset value, and field meaning. Evidence index: CMBWBZ, CMBRBB, CMBSZU, CMBEBS, CMB, Controller.

- Conditions and limits: Source keyword index: `shall`, `may`, `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Read CMBEBS with the required width, then verify CMBWBZ and CMBRBB separately before using either value. This example adds no requirement.

- Source field index: CMBWBZ, CMBRBB, CMBSZU, CMBEBS, CMB, Controller

- Source keyword index: `shall`, `may`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.16, Figure 54, printed pages 71, PDF pages 97

</details>

<details markdown="1">
<summary><strong>Figure 55: Offset 60h: CMBSWTP - Controller Memory Buffer Sustained Write Throughput</strong></summary>

<!-- claim:BASE3-FIG-055-CLAIM figure-table:BASE3-FIG-055 -->

Figure 55, "Offset 60h: CMBSWTP - Controller Memory Buffer Sustained Write Throughput": Defines CMBSWTP (Controller Memory Buffer Sustained Write Throughput) at offset 60h and identifies the fields that software must decode at that location. Start at CMBSWTP, then map bit ranges to access type, reset value, and field meaning. Evidence index: CMBSWTV, CMBSWTU, CMBSWTP, CMB, TLP, MPS, PXDC, Controller.

- Purpose: Defines CMBSWTP (Controller Memory Buffer Sustained Write Throughput) at offset 60h and identifies the fields that software must decode at that location.

- How to read: Start at CMBSWTP, then map bit ranges to access type, reset value, and field meaning. Evidence index: CMBSWTV, CMBSWTU, CMBSWTP, CMB, TLP, MPS, PXDC, Controller.

- Conditions and limits: Source keyword index: `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Read CMBSWTP with the required width, then verify CMBSWTV and CMBSWTU separately before using either value. This example adds no requirement.

- Source field index: CMBSWTV, CMBSWTU, CMBSWTP, CMB, TLP, MPS, PXDC, Controller

- Source keyword index: `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.19, Figure 55, printed pages 72, PDF pages 98

</details>

<details markdown="1">
<summary><strong>Figure 56: Offset 64h: NSSD - NVM Subsystem Shutdown</strong></summary>

<!-- claim:BASE3-FIG-056-CLAIM figure-table:BASE3-FIG-056 -->

Figure 56, "Offset 64h: NSSD - NVM Subsystem Shutdown": Defines NSSD (NVM Subsystem Shutdown) at offset 64h and identifies the fields that software must decode at that location. Start at NSSD, then map bit ranges to access type, reset value, and field meaning. Evidence index: NSSC, NSSD, CAP.CPS, NVM Subsystem.

- Purpose: Defines NSSD (NVM Subsystem Shutdown) at offset 64h and identifies the fields that software must decode at that location.

- How to read: Start at NSSD, then map bit ranges to access type, reset value, and field meaning. Evidence index: NSSC, NSSD, CAP.CPS, NVM Subsystem.

- Conditions and limits: Source keyword index: `shall`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Read NSSD with the required width, then verify NSSC and NSSD separately before using either value. This example adds no requirement.

- Source field index: NSSC, NSSD, CAP.CPS, NVM Subsystem

- Source keyword index: `shall`

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.19, Figure 56, printed pages 72, PDF pages 98

</details>

<details markdown="1">
<summary><strong>Figure 57: Offset 68h: CRTO - Controller Ready Timeouts</strong></summary>

<!-- claim:BASE3-FIG-057-CLAIM figure-table:BASE3-FIG-057 -->

Figure 57, "Offset 68h: CRTO - Controller Ready Timeouts": Defines CRTO (Controller Ready Timeouts) at offset 68h and identifies the fields that software must decode at that location. Start at CRTO, then map bit ranges to access type, reset value, and field meaning. Evidence index: CRIMT, CRWMT, CRTO, CAP.CRMS.CRIMS, CC.EN, CC.CRIME, CRTO.CRIMT, Controller.

- Purpose: Defines CRTO (Controller Ready Timeouts) at offset 68h and identifies the fields that software must decode at that location.

- How to read: Start at CRTO, then map bit ranges to access type, reset value, and field meaning. Evidence index: CRIMT, CRWMT, CRTO, CAP.CRMS.CRIMS, CC.EN, CC.CRIME, CRTO.CRIMT, Controller.

- Conditions and limits: Source keyword index: `should not`, `shall`, `should`, `may`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Read CRTO with the required width, then verify CRIMT and CRWMT separately before using either value. This example adds no requirement.

- Source field index: CRIMT, CRWMT, CRTO, CAP.CRMS.CRIMS, CC.EN, CC.CRIME, CRTO.CRIMT, Controller

- Source keyword index: `should not`, `shall`, `should`, `may`

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.21, Figure 57, printed pages 73, PDF pages 99

</details>

<details markdown="1">
<summary><strong>Figure 58: Offset E00h: PMRCAP - Persistent Memory Region Capabilities</strong></summary>

<!-- claim:BASE3-FIG-058-CLAIM figure-table:BASE3-FIG-058 -->

Figure 58, "Offset E00h: PMRCAP - Persistent Memory Region Capabilities": Defines PMRCAP (Persistent Memory Region Capabilities) at offset E00h and identifies the fields that software must decode at that location. Start at PMRCAP, then map bit ranges to access type, reset value, and field meaning. Evidence index: CMSS, PMRTO, PMRWBM, CPMTSTSR, CMR, PMRTU, BIR, WDS.

- Purpose: Defines PMRCAP (Persistent Memory Region Capabilities) at offset E00h and identifies the fields that software must decode at that location.

- How to read: Start at PMRCAP, then map bit ranges to access type, reset value, and field meaning. Evidence index: CMSS, PMRTO, PMRWBM, CPMTSTSR, CMR, PMRTU, BIR, WDS.

- Conditions and limits: Source keyword index: `shall not`, `shall`, `should`, `may`, `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Read PMRCAP with the required width, then verify CMSS and PMRTO separately before using either value. This example adds no requirement.

- Source field index: CMSS, PMRTO, PMRWBM, CPMTSTSR, CMR, PMRTU, BIR, WDS

- Source keyword index: `shall not`, `shall`, `should`, `may`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.21, Figure 58, printed pages 73-74, PDF pages 99-100

</details>

<details markdown="1">
<summary><strong>Figure 59: Offset E04h: PMRCTL - Persistent Memory Region Control</strong></summary>

<!-- claim:BASE3-FIG-059-CLAIM figure-table:BASE3-FIG-059 -->

Figure 59, "Offset E04h: PMRCTL - Persistent Memory Region Control": Defines PMRCTL (Persistent Memory Region Control) at offset E04h and identifies the fields that software must decode at that location. Start at PMRCTL, then map bit ranges to access type, reset value, and field meaning. Evidence index: EN, PMRCTL, PMRSTS.NRDY.

- Purpose: Defines PMRCTL (Persistent Memory Region Control) at offset E04h and identifies the fields that software must decode at that location.

- How to read: Start at PMRCTL, then map bit ranges to access type, reset value, and field meaning. Evidence index: EN, PMRCTL, PMRSTS.NRDY.

- Conditions and limits: Source keyword index: `shall`, `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Read PMRCTL with the required width, then verify EN and PMRCTL separately before using either value. This example adds no requirement.

- Source field index: EN, PMRCTL, PMRSTS.NRDY

- Source keyword index: `shall`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.22, Figure 59, printed pages 74, PDF pages 100

</details>

<details markdown="1">
<summary><strong>Figure 60: Offset E08h: PMRSTS - Persistent Memory Region Status</strong></summary>

<!-- claim:BASE3-FIG-060-CLAIM figure-table:BASE3-FIG-060 -->

Figure 60, "Offset E08h: PMRSTS - Persistent Memory Region Status": Defines PMRSTS (Persistent Memory Region Status) at offset E08h and identifies the fields that software must decode at that location. Start at PMRSTS, then map bit ranges to access type, reset value, and field meaning. Evidence index: CBAI, HSTS, NRDY, ERR, PMRSTS, PMRMSCU.CBA, PMRMSCL.CBA, PMRCAP.CMSS.

- Purpose: Defines PMRSTS (Persistent Memory Region Status) at offset E08h and identifies the fields that software must decode at that location.

- How to read: Start at PMRSTS, then map bit ranges to access type, reset value, and field meaning. Evidence index: CBAI, HSTS, NRDY, ERR, PMRSTS, PMRMSCU.CBA, PMRMSCL.CBA, PMRCAP.CMSS.

- Conditions and limits: Source keyword index: `shall`, `may`, `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Read PMRSTS with the required width, then verify CBAI and HSTS separately before using either value. This example adds no requirement.

- Source field index: CBAI, HSTS, NRDY, ERR, PMRSTS, PMRMSCU.CBA, PMRMSCL.CBA, PMRCAP.CMSS

- Source keyword index: `shall`, `may`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.23, Figure 60, printed pages 75, PDF pages 101

</details>

<details markdown="1">
<summary><strong>Figure 61: Offset E0Ch: PMREBS - Persistent Memory Region Elasticity Buffer Size</strong></summary>

<!-- claim:BASE3-FIG-061-CLAIM figure-table:BASE3-FIG-061 -->

Figure 61, "Offset E0Ch: PMREBS - Persistent Memory Region Elasticity Buffer Size": Defines PMREBS (Persistent Memory Region Elasticity Buffer Size) at offset E0Ch and identifies the fields that software must decode at that location. Start at PMREBS, then map bit ranges to access type, reset value, and field meaning. Evidence index: PMRWBZ, PMRRBB, PMRSZU, PMREBS, PMR.

- Purpose: Defines PMREBS (Persistent Memory Region Elasticity Buffer Size) at offset E0Ch and identifies the fields that software must decode at that location.

- How to read: Start at PMREBS, then map bit ranges to access type, reset value, and field meaning. Evidence index: PMRWBZ, PMRRBB, PMRSZU, PMREBS, PMR.

- Conditions and limits: Source keyword index: `shall`, `may`, `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Read PMREBS with the required width, then verify PMRWBZ and PMRRBB separately before using either value. This example adds no requirement.

- Source field index: PMRWBZ, PMRRBB, PMRSZU, PMREBS, PMR

- Source keyword index: `shall`, `may`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.24, Figure 61, printed pages 76, PDF pages 102

</details>

<details markdown="1">
<summary><strong>Figure 62: Offset E10h: PMRSWTP - Persistent Memory Region Sustained Write Throughput</strong></summary>

<!-- claim:BASE3-FIG-062-CLAIM figure-table:BASE3-FIG-062 -->

Figure 62, "Offset E10h: PMRSWTP - Persistent Memory Region Sustained Write Throughput": Defines PMRSWTP (Persistent Memory Region Sustained Write Throughput) at offset E10h and identifies the fields that software must decode at that location. Start at PMRSWTP, then map bit ranges to access type, reset value, and field meaning. Evidence index: PMRSWTV, PMRSWTU, PMRSWTP, PMR, TLP, MPS, PXDC.

- Purpose: Defines PMRSWTP (Persistent Memory Region Sustained Write Throughput) at offset E10h and identifies the fields that software must decode at that location.

- How to read: Start at PMRSWTP, then map bit ranges to access type, reset value, and field meaning. Evidence index: PMRSWTV, PMRSWTU, PMRSWTP, PMR, TLP, MPS, PXDC.

- Conditions and limits: Source keyword index: `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Read PMRSWTP with the required width, then verify PMRSWTV and PMRSWTU separately before using either value. This example adds no requirement.

- Source field index: PMRSWTV, PMRSWTU, PMRSWTP, PMR, TLP, MPS, PXDC

- Source keyword index: `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.24, Figure 62, printed pages 76, PDF pages 102

</details>

<details markdown="1">
<summary><strong>Figure 63: Offset E14h: PMRMSCL - Persistent Memory Region Memory Space Control Lower</strong></summary>

<!-- claim:BASE3-FIG-063-CLAIM figure-table:BASE3-FIG-063 -->

Figure 63, "Offset E14h: PMRMSCL - Persistent Memory Region Memory Space Control Lower": Defines PMRMSCL (Persistent Memory Region Memory Space Control Lower) at offset E14h and identifies the fields that software must decode at that location. Start at PMRMSCL, then map bit ranges to access type, reset value, and field meaning. Evidence index: CBA, CMSE, PMRMSCL, PMRMSCU.CBA.

- Purpose: Defines PMRMSCL (Persistent Memory Region Memory Space Control Lower) at offset E14h and identifies the fields that software must decode at that location.

- How to read: Start at PMRMSCL, then map bit ranges to access type, reset value, and field meaning. Evidence index: CBA, CMSE, PMRMSCL, PMRMSCU.CBA.

- Conditions and limits: Source keyword index: `shall`, `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Read PMRMSCL with the required width, then verify CBA and CMSE separately before using either value. This example adds no requirement.

- Source field index: CBA, CMSE, PMRMSCL, PMRMSCU.CBA

- Source keyword index: `shall`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.26, Figure 63, printed pages 77, PDF pages 103

</details>

<details markdown="1">
<summary><strong>Figure 64: Offset E18h: PMRMSCU - Persistent Memory Region Memory Space Control Upper</strong></summary>

<!-- claim:BASE3-FIG-064-CLAIM figure-table:BASE3-FIG-064 -->

Figure 64, "Offset E18h: PMRMSCU - Persistent Memory Region Memory Space Control Upper": Defines PMRMSCU (Persistent Memory Region Memory Space Control Upper) at offset E18h and identifies the fields that software must decode at that location. Start at PMRMSCU, then map bit ranges to access type, reset value, and field meaning. Evidence index: CBA, PMRMSCU.

- Purpose: Defines PMRMSCU (Persistent Memory Region Memory Space Control Upper) at offset E18h and identifies the fields that software must decode at that location.

- How to read: Start at PMRMSCU, then map bit ranges to access type, reset value, and field meaning. Evidence index: CBA, PMRMSCU.

- Conditions and limits: The Figure is explanatory or structural; this guide does not turn its visual relationship into a new requirement.

- Informative example: Read PMRMSCU with the required width, then verify CBA and PMRMSCU separately before using either value. This example adds no requirement.

- Source field index: CBA, PMRMSCU

- Source keyword index: none

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.26, Figure 64, printed pages 77, PDF pages 103

</details>

<a id="section-3-2"></a>

### §3.2

<details markdown="1">
<summary><strong>Figure 65: NSID Types and Relationship to Namespace</strong></summary>

<!-- claim:BASE3-FIG-065-CLAIM figure-table:BASE3-FIG-065 -->

Figure 65, "NSID Types and Relationship to Namespace": Defines the identifier composition or namespace of values shown by NSID Types and Relationship to Namespace. Keep the value width, issuing authority, uniqueness scope, and reserved values separate. Evidence index: NSID, Namespace.

- Purpose: Defines the identifier composition or namespace of values shown by NSID Types and Relationship to Namespace.

- How to read: Keep the value width, issuing authority, uniqueness scope, and reserved values separate. Evidence index: NSID, Namespace.

- Conditions and limits: The Figure is explanatory or structural; this guide does not turn its visual relationship into a new requirement.

- Informative example: Parse NSID at its defined width, then validate the scope associated with Namespace before using it as an identity key. This example adds no requirement.

- Source field index: NSID, Namespace

- Source keyword index: none

> Source: NVME-BASE-2.4, Rev. 2.4, §3.2.1, Figure 65, printed pages 78-79, PDF pages 104-105

</details>

<details markdown="1">
<summary><strong>Figure 66: NSID Types</strong></summary>

<!-- claim:BASE3-FIG-066-CLAIM figure-table:BASE3-FIG-066 -->

Figure 66, "NSID Types": Defines the identifier composition or namespace of values shown by NSID Types. Keep the value width, issuing authority, uniqueness scope, and reserved values separate. Evidence index: NSID.

- Purpose: Defines the identifier composition or namespace of values shown by NSID Types.

- How to read: Keep the value width, issuing authority, uniqueness scope, and reserved values separate. Evidence index: NSID.

- Conditions and limits: The Figure is explanatory or structural; this guide does not turn its visual relationship into a new requirement.

- Informative example: Parse NSID at its defined width, then validate the scope associated with the cited condition before using it as an identity key. This example adds no requirement.

- Source field index: NSID

- Source keyword index: none

> Source: NVME-BASE-2.4, Rev. 2.4, §3.2.1.5, Figure 66, printed pages 79, PDF pages 105

</details>

<details markdown="1">
<summary><strong>Figure 67: NVM Sets and Associated Namespaces</strong></summary>

<!-- claim:BASE3-FIG-067-CLAIM figure-table:BASE3-FIG-067 -->

Figure 67, "NVM Sets and Associated Namespaces": Shows the object or capacity relationships in NVM Sets and Associated Namespaces. Separate logical identifiers from controllers, namespaces, ports, and capacity containers. Evidence index: NVM Set, Namespace.

- Purpose: Shows the object or capacity relationships in NVM Sets and Associated Namespaces.

- How to read: Separate logical identifiers from controllers, namespaces, ports, and capacity containers. Evidence index: NVM Set, Namespace.

- Conditions and limits: The Figure is explanatory or structural; this guide does not turn its visual relationship into a new requirement.

- Informative example: Choose one object labeled by NVM Set and trace its relationship to Namespace without treating an identifier as the object itself. This example adds no requirement.

- Source field index: NVM Set, Namespace

- Source keyword index: none

> Source: NVME-BASE-2.4, Rev. 2.4, §3.2.2, Figure 67, printed pages 81, PDF pages 107

</details>

<details markdown="1">
<summary><strong>Figure 68: NVM Set Aware Admin Commands</strong></summary>

<!-- claim:BASE3-FIG-068-CLAIM figure-table:BASE3-FIG-068 -->

Figure 68, "NVM Set Aware Admin Commands": Shows the object or capacity relationships in NVM Set Aware Admin Commands. Separate logical identifiers from controllers, namespaces, ports, and capacity containers. Evidence index: NVM Set, Command.

- Purpose: Shows the object or capacity relationships in NVM Set Aware Admin Commands.

- How to read: Separate logical identifiers from controllers, namespaces, ports, and capacity containers. Evidence index: NVM Set, Command.

- Conditions and limits: The Figure is explanatory or structural; this guide does not turn its visual relationship into a new requirement.

- Informative example: Choose one object labeled by NVM Set and trace its relationship to Command without treating an identifier as the object itself. This example adds no requirement.

- Source field index: NVM Set, Command

- Source keyword index: none

> Source: NVME-BASE-2.4, Rev. 2.4, §3.2.2, Figure 68, printed pages 81, PDF pages 107

</details>

<details markdown="1">
<summary><strong>Figure 69: NVM Sets and Associated Namespaces</strong></summary>

<!-- claim:BASE3-FIG-069-CLAIM figure-table:BASE3-FIG-069 -->

Figure 69, "NVM Sets and Associated Namespaces": Shows the object or capacity relationships in NVM Sets and Associated Namespaces. Separate logical identifiers from controllers, namespaces, ports, and capacity containers. Evidence index: NVM Set, Namespace.

- Purpose: Shows the object or capacity relationships in NVM Sets and Associated Namespaces.

- How to read: Separate logical identifiers from controllers, namespaces, ports, and capacity containers. Evidence index: NVM Set, Namespace.

- Conditions and limits: The Figure is explanatory or structural; this guide does not turn its visual relationship into a new requirement.

- Informative example: Choose one object labeled by NVM Set and trace its relationship to Namespace without treating an identifier as the object itself. This example adds no requirement.

- Source field index: NVM Set, Namespace

- Source keyword index: none

> Source: NVME-BASE-2.4, Rev. 2.4, §3.2.3, Figure 69, printed pages 83, PDF pages 109

</details>

<details markdown="1">
<summary><strong>Figure 70: Flexible Data Placement Logical View of Non-Volatile Storage</strong></summary>

<!-- claim:BASE3-FIG-070-CLAIM figure-table:BASE3-FIG-070 -->

Figure 70, "Flexible Data Placement Logical View of Non-Volatile Storage": Shows the object or capacity relationships in Flexible Data Placement Logical View of Non-Volatile Storage. Separate logical identifiers from controllers, namespaces, ports, and capacity containers. Evidence index: Flexible Data Placement Logical View of Non-Volatile Storage.

- Purpose: Shows the object or capacity relationships in Flexible Data Placement Logical View of Non-Volatile Storage.

- How to read: Separate logical identifiers from controllers, namespaces, ports, and capacity containers. Evidence index: Flexible Data Placement Logical View of Non-Volatile Storage.

- Conditions and limits: The Figure is explanatory or structural; this guide does not turn its visual relationship into a new requirement.

- Informative example: Choose one object labeled by Flexible Data Placement Logical View of Non-Volatile Storage and trace its relationship to the cited condition without treating an identifier as the object itself. This example adds no requirement.

- Source field index: Flexible Data Placement Logical View of Non-Volatile Storage

- Source keyword index: none

> Source: NVME-BASE-2.4, Rev. 2.4, §3.2.4, Figure 70, printed pages 85, PDF pages 111

</details>

<details markdown="1">
<summary><strong>Figure 71: Example 1 Domain Structure</strong></summary>

<!-- claim:BASE3-FIG-071-CLAIM figure-table:BASE3-FIG-071 -->

Figure 71, "Example 1 Domain Structure": Defines the concrete layout or value relationships for Example 1 Domain Structure. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is Domain.

- Purpose: Defines the concrete layout or value relationships for Example 1 Domain Structure.

- How to read: Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is Domain.

- Conditions and limits: The Figure is explanatory or structural; this guide does not turn its visual relationship into a new requirement.

- Informative example: Use Domain as the first parser checkpoint and the cited condition as a second, independent boundary check. This example adds no requirement.

- Source field index: Domain

- Source keyword index: none

> Source: NVME-BASE-2.4, Rev. 2.4, §3.2.5.1, Figure 71, printed pages 86, PDF pages 112

</details>

<a id="section-3-3"></a>

### §3.3

<details markdown="1">
<summary><strong>Figure 73: Empty Queue Definition</strong></summary>

<!-- claim:BASE3-FIG-073-CLAIM figure-table:BASE3-FIG-073 -->

Figure 73, "Empty Queue Definition": Defines the concrete layout or value relationships for Empty Queue Definition. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is Empty Queue Definition.

- Purpose: Defines the concrete layout or value relationships for Empty Queue Definition.

- How to read: Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is Empty Queue Definition.

- Conditions and limits: Source keyword index: `shall`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Use Empty Queue Definition as the first parser checkpoint and the cited condition as a second, independent boundary check. This example adds no requirement.

- Source field index: Empty Queue Definition

- Source keyword index: `shall`

> Source: NVME-BASE-2.4, Rev. 2.4, §3.3.1.4, Figure 73, printed pages 91, PDF pages 117

</details>

<details markdown="1">
<summary><strong>Figure 74: Full Queue Definition</strong></summary>

<!-- claim:BASE3-FIG-074-CLAIM figure-table:BASE3-FIG-074 -->

Figure 74, "Full Queue Definition": Defines the concrete layout or value relationships for Full Queue Definition. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is Full Queue Definition.

- Purpose: Defines the concrete layout or value relationships for Full Queue Definition.

- How to read: Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is Full Queue Definition.

- Conditions and limits: The Figure is explanatory or structural; this guide does not turn its visual relationship into a new requirement.

- Informative example: Use Full Queue Definition as the first parser checkpoint and the cited condition as a second, independent boundary check. This example adds no requirement.

- Source field index: Full Queue Definition

- Source keyword index: none

> Source: NVME-BASE-2.4, Rev. 2.4, §3.3.1.4, Figure 74, printed pages 91, PDF pages 117

</details>

<a id="section-3-4"></a>

### §3.4

<details markdown="1">
<summary><strong>Figure 80: Round Robin Arbitration</strong></summary>

<!-- claim:BASE3-FIG-080-CLAIM figure-table:BASE3-FIG-080 -->

Figure 80, "Round Robin Arbitration": Shows how Round Robin Arbitration selects work from competing Submission Queues. Track priority class, service order, and the point at which the arbiter selects the next command. Evidence index: Round Robin Arbitration.

- Purpose: Shows how Round Robin Arbitration selects work from competing Submission Queues.

- How to read: Track priority class, service order, and the point at which the arbiter selects the next command. Evidence index: Round Robin Arbitration.

- Conditions and limits: The Figure is explanatory or structural; this guide does not turn its visual relationship into a new requirement.

- Informative example: Compare queues represented by Round Robin Arbitration and the cited condition, then advance only the queue chosen by the stated arbitration rule. This example adds no requirement.

- Source field index: Round Robin Arbitration

- Source keyword index: none

> Source: NVME-BASE-2.4, Rev. 2.4, §3.4.4, Figure 80, printed pages 103, PDF pages 129

</details>

<details markdown="1">
<summary><strong>Figure 81: Weighted Round Robin with Urgent Priority Class Arbitration</strong></summary>

<!-- claim:BASE3-FIG-081-CLAIM figure-table:BASE3-FIG-081 -->

Figure 81, "Weighted Round Robin with Urgent Priority Class Arbitration": Shows how Weighted Round Robin with Urgent Priority Class Arbitration selects work from competing Submission Queues. Track priority class, service order, and the point at which the arbiter selects the next command. Evidence index: Weighted Round Robin with Urgent Priority Class Arbitration.

- Purpose: Shows how Weighted Round Robin with Urgent Priority Class Arbitration selects work from competing Submission Queues.

- How to read: Track priority class, service order, and the point at which the arbiter selects the next command. Evidence index: Weighted Round Robin with Urgent Priority Class Arbitration.

- Conditions and limits: The Figure is explanatory or structural; this guide does not turn its visual relationship into a new requirement.

- Informative example: Compare queues represented by Weighted Round Robin with Urgent Priority Class Arbitration and the cited condition, then advance only the queue chosen by the stated arbitration rule. This example adds no requirement.

- Source field index: Weighted Round Robin with Urgent Priority Class Arbitration

- Source keyword index: none

> Source: NVME-BASE-2.4, Rev. 2.4, §3.4.4.2, Figure 81, printed pages 104, PDF pages 130

</details>

<a id="section-3-5"></a>

### §3.5

<details markdown="1">
<summary><strong>Figure 84: Admin Commands Permitted to Return a Status Code of Admin Command Media Not</strong></summary>

<!-- claim:BASE3-FIG-084-CLAIM figure-table:BASE3-FIG-084 -->

Figure 84, "Admin Commands Permitted to Return a Status Code of Admin Command Media Not": Defines the status/error classification represented by Admin Commands Permitted to Return a Status Code of Admin Command Media Not. Resolve the category before the individual code or flag; keep reserved values uninterpreted. Evidence index: LBA, TCG, CAP.CRMS, CAP.CRMS.CRWMS, CAP.CRMS.CRIMS, CC.CRIME, Status Code, Command.

- Purpose: Defines the status/error classification represented by Admin Commands Permitted to Return a Status Code of Admin Command Media Not.

- How to read: Resolve the category before the individual code or flag; keep reserved values uninterpreted. Evidence index: LBA, TCG, CAP.CRMS, CAP.CRMS.CRWMS, CAP.CRMS.CRIMS, CC.CRIME, Status Code, Command.

- Conditions and limits: Source keyword index: `shall`, `should`, `may`. The index locates normative language but does not replace the condition attached to each field. Only the PCIe/memory-based portion is in scope.

- Informative example: For one reported condition, identify LBA first and then check TCG instead of decoding an isolated numeric value. This example adds no requirement.

- Source field index: LBA, TCG, CAP.CRMS, CAP.CRMS.CRWMS, CAP.CRMS.CRIMS, CC.CRIME, Status Code, Command

- Source keyword index: `shall`, `should`, `may`

> Source: NVME-BASE-2.4, Rev. 2.4, §3.5.3, Figure 84, printed pages 110-111, PDF pages 136-137

</details>

<a id="section-3-6"></a>

### §3.6

<details markdown="1">
<summary><strong>Figure 85: Shutdown Processing Interactions</strong></summary>

<!-- claim:BASE3-FIG-085-CLAIM figure-table:BASE3-FIG-085 -->

Figure 85, "Shutdown Processing Interactions": Shows the state or timing progression represented by Shutdown Processing Interactions. Follow the states or time bounds in arrow order and identify which actor observes each transition. Evidence index: Shutdown Processing Interactions.

- Purpose: Shows the state or timing progression represented by Shutdown Processing Interactions.

- How to read: Follow the states or time bounds in arrow order and identify which actor observes each transition. Evidence index: Shutdown Processing Interactions.

- Conditions and limits: The Figure is explanatory or structural; this guide does not turn its visual relationship into a new requirement. Only the PCIe/memory-based portion is in scope.

- Informative example: Begin at Shutdown Processing Interactions, record the transition that reaches the cited condition, and evaluate timeout or reset behavior only at the stated boundary. This example adds no requirement.

- Source field index: Shutdown Processing Interactions

- Source keyword index: none

> Source: NVME-BASE-2.4, Rev. 2.4, §3.6, Figure 85, printed pages 113, PDF pages 139

</details>

<a id="section-3-8"></a>

### §3.8

<details markdown="1">
<summary><strong>Figure 86: Simple NVM Subsystem</strong></summary>

<!-- claim:BASE3-FIG-086-CLAIM figure-table:BASE3-FIG-086 -->

Figure 86, "Simple NVM Subsystem": Shows the object or capacity relationships in Simple NVM Subsystem. Separate logical identifiers from controllers, namespaces, ports, and capacity containers. Evidence index: NVM Subsystem.

- Purpose: Shows the object or capacity relationships in Simple NVM Subsystem.

- How to read: Separate logical identifiers from controllers, namespaces, ports, and capacity containers. Evidence index: NVM Subsystem.

- Conditions and limits: The Figure is explanatory or structural; this guide does not turn its visual relationship into a new requirement.

- Informative example: Choose one object labeled by NVM Subsystem and trace its relationship to the cited condition without treating an identifier as the object itself. This example adds no requirement.

- Source field index: NVM Subsystem

- Source keyword index: none

> Source: NVME-BASE-2.4, Rev. 2.4, §3.8.2, Figure 86, printed pages 126, PDF pages 152

</details>

<details markdown="1">
<summary><strong>Figure 87: Vertically-Organized NVM Subsystem</strong></summary>

<!-- claim:BASE3-FIG-087-CLAIM figure-table:BASE3-FIG-087 -->

Figure 87, "Vertically-Organized NVM Subsystem": Shows the object or capacity relationships in Vertically-Organized NVM Subsystem. Separate logical identifiers from controllers, namespaces, ports, and capacity containers. Evidence index: NVM Subsystem.

- Purpose: Shows the object or capacity relationships in Vertically-Organized NVM Subsystem.

- How to read: Separate logical identifiers from controllers, namespaces, ports, and capacity containers. Evidence index: NVM Subsystem.

- Conditions and limits: The Figure is explanatory or structural; this guide does not turn its visual relationship into a new requirement.

- Informative example: Choose one object labeled by NVM Subsystem and trace its relationship to the cited condition without treating an identifier as the object itself. This example adds no requirement.

- Source field index: NVM Subsystem

- Source keyword index: none

> Source: NVME-BASE-2.4, Rev. 2.4, §3.8.2.2, Figure 87, printed pages 127, PDF pages 153

</details>

<details markdown="1">
<summary><strong>Figure 88: Horizontally-Organized Dual NAND NVM Subsystem</strong></summary>

<!-- claim:BASE3-FIG-088-CLAIM figure-table:BASE3-FIG-088 -->

Figure 88, "Horizontally-Organized Dual NAND NVM Subsystem": Shows the object or capacity relationships in Horizontally-Organized Dual NAND NVM Subsystem. Separate logical identifiers from controllers, namespaces, ports, and capacity containers. Evidence index: NAND, NVM Subsystem.

- Purpose: Shows the object or capacity relationships in Horizontally-Organized Dual NAND NVM Subsystem.

- How to read: Separate logical identifiers from controllers, namespaces, ports, and capacity containers. Evidence index: NAND, NVM Subsystem.

- Conditions and limits: The Figure is explanatory or structural; this guide does not turn its visual relationship into a new requirement.

- Informative example: Choose one object labeled by NAND and trace its relationship to NVM Subsystem without treating an identifier as the object itself. This example adds no requirement.

- Source field index: NAND, NVM Subsystem

- Source keyword index: none

> Source: NVME-BASE-2.4, Rev. 2.4, §3.8.2.3, Figure 88, printed pages 128, PDF pages 154

</details>

<details markdown="1">
<summary><strong>Figure 89: Capacity Information Field Usage</strong></summary>

<!-- claim:BASE3-FIG-089-CLAIM figure-table:BASE3-FIG-089 -->

Figure 89, "Capacity Information Field Usage": Defines the concrete layout or value relationships for Capacity Information Field Usage. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is TNVMCAP, UNVMCAP, MEGCAP, TEGCAP, UEGCAP.

- Purpose: Defines the concrete layout or value relationships for Capacity Information Field Usage.

- How to read: Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is TNVMCAP, UNVMCAP, MEGCAP, TEGCAP, UEGCAP.

- Conditions and limits: The Figure is explanatory or structural; this guide does not turn its visual relationship into a new requirement.

- Informative example: Use TNVMCAP as the first parser checkpoint and UNVMCAP as a second, independent boundary check. This example adds no requirement.

- Source field index: TNVMCAP, UNVMCAP, MEGCAP, TEGCAP, UEGCAP

- Source keyword index: none

> Source: NVME-BASE-2.4, Rev. 2.4, §3.8.3, Figure 89, printed pages 129, PDF pages 155

</details>

<a id="section-3-9"></a>

### §3.9

<details markdown="1">
<summary><strong>Figure 90: Detecting Timeout Takes up to 2 * KATT</strong></summary>

<!-- claim:BASE3-FIG-090-CLAIM figure-table:BASE3-FIG-090 -->

Figure 90, "Detecting Timeout Takes up to 2 * KATT": Shows the state or timing progression represented by Detecting Timeout Takes up to 2 * KATT. Follow the states or time bounds in arrow order and identify which actor observes each transition. Evidence index: KATT.

- Purpose: Shows the state or timing progression represented by Detecting Timeout Takes up to 2 * KATT.

- How to read: Follow the states or time bounds in arrow order and identify which actor observes each transition. Evidence index: KATT.

- Conditions and limits: The Figure is explanatory or structural; this guide does not turn its visual relationship into a new requirement. Only the PCIe/memory-based portion is in scope.

- Informative example: Begin at KATT, record the transition that reaches the cited condition, and evaluate timeout or reset behavior only at the stated boundary. This example adds no requirement.

- Source field index: KATT

- Source keyword index: none

> Source: NVME-BASE-2.4, Rev. 2.4, §3.9.4.1, Figure 90, printed pages 133, PDF pages 159

</details>

<a id="section-3-10"></a>

### §3.10

<details markdown="1">
<summary><strong>Figure 91: Example Privileged Action Admin Commands</strong></summary>

<!-- claim:BASE3-FIG-091-CLAIM figure-table:BASE3-FIG-091 -->

Figure 91, "Example Privileged Action Admin Commands": Identifies the privileged-operation boundary illustrated by Example Privileged Action Admin Commands. Separate the requesting command from the privilege or controller state that authorizes it. Evidence index: Command.

- Purpose: Identifies the privileged-operation boundary illustrated by Example Privileged Action Admin Commands.

- How to read: Separate the requesting command from the privilege or controller state that authorizes it. Evidence index: Command.

- Conditions and limits: The Figure is explanatory or structural; this guide does not turn its visual relationship into a new requirement. Only the PCIe/memory-based portion is in scope.

- Informative example: Check Command first, then verify the authorization condition associated with the cited condition before issuing the operation. This example adds no requirement.

- Source field index: Command

- Source keyword index: none

> Source: NVME-BASE-2.4, Rev. 2.4, §3.10, Figure 91, printed pages 135, PDF pages 161

</details>

## Use and limitations

Use the claim IDs as stable PPT traceability keys. Re-check affected claims if the source revision, errata set, or approved scope changes.
