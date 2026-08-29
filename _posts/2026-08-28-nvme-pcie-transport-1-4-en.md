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

## Specification findings

### 1. Transport and Base precedence

<!-- claim:PCIE14-SCOPE -->

The PCIe Transport supplements the Base Specification with PCIe-specific structures, extensions, requirements, and behavior; common NVMe behavior remains in Base. In a conflict, Base has higher precedence than a Transport Specification.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §1.2, printed pages 6, PDF pages 6

### 2. PCIe Reset-column convention

<!-- claim:PCIE14-CONVENTION -->

This document inherits Base conventions. In register or property tables, the Reset column instead denotes the post-reset field value defined by the applicable PCI or PCIe specification.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §1.3, printed pages 6-7, PDF pages 6-7

### 3. Transport normative language

<!-- claim:PCIE14-KEYWORDS -->

The force of shall, may, and should remains defined by Base 2.4; a Transport summary must not strengthen or weaken the normative language.

> Source: NVME-BASE-2.4, Rev. 2.4, §1.4.1, printed pages 2-3, PDF pages 28-29

### 4. PCIe transport overview

<!-- claim:PCIE14-OVERVIEW -->

The PCIe transport uses memory-mapped I/O for data and register access, along with PCIe configuration space and message-signaled interrupts.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §2, printed pages 8, PDF pages 8

### 5. BAR and register access

<!-- claim:PCIE14-MMIO -->

NVMe controller registers reside in memory space identified by BAR0/BAR1. The host shall use native-width or aligned 32-bit accesses and shall not issue locked accesses; violation produces undefined behavior.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.1, printed pages 9-10, PDF pages 9-10

### 6. SQ/CQ doorbell offsets

<!-- claim:PCIE14-DOORBELL -->

SQ-tail and CQ-head doorbells begin at offset 1000h, with stride determined by CAP.DSTRD; queue identifier y participates in the offset calculation.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.1.2.1-3.1.2.2, printed pages 10-11, PDF pages 10-11

### 7. Queues and interrupt vectors

<!-- claim:PCIE14-QUEUE -->

PCIe permits multiple Submission Queues to share a Completion Queue. If interrupts are enabled when creating the CQ, Interrupt Vector shall be initialized to the corresponding MSI-X or multiple-message MSI vector.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.2, printed pages 11, PDF pages 11

### 8. PCIe reset recovery

<!-- claim:PCIE14-RESET -->

PCIe reset sources include Base controller/reset flows and PCIe-level resets. Recovery logic uses the reset type to determine controller-property, queue, and PCI-configuration state.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.3, printed pages 11-12, PDF pages 11-12

### 9. PCIe command flow

<!-- claim:PCIE14-COMMAND -->

The command flow writes an SQE, updates the SQ-tail doorbell, lets the controller fetch and execute, posts a CQE, optionally interrupts, processes the CQE, and updates the CQ-head doorbell. A doorbell conveys a pointer, not the command body.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.4, printed pages 12-13, PDF pages 12-13

### 10. Interrupt modes and delay

<!-- claim:PCIE14-INTERRUPT -->

Modes are pin-based, single-message MSI, multiple-message MSI, and MSI-X. The specification recommends MSI-X. Coalescing can reduce interrupt rate at the cost of latency, and Admin-CQ interrupts should not be delayed.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.5, printed pages 13-16, PDF pages 13-16

### 11. Slot power limit

<!-- claim:PCIE14-POWER -->

The host shall never select an NVMe power state whose consumption exceeds the PCIe slot power limit; violation results in undefined power behavior.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.6, printed pages 16, PDF pages 16

### 12. NVMe and PCIe error layers

<!-- claim:PCIE14-ERROR -->

NVMe command errors are reported in CQE status, while PCIe transport or link errors use PCIe mechanisms plus this document’s NVMe-specific requirements. Their recovery scopes differ.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.7, printed pages 16, PDF pages 16

### 13. PCI configuration requirements

<!-- claim:PCIE14-CONFIG -->

Section 3.8 defines additional NVMe-controller requirements for the PCI header, Power Management, MSI/MSI-X, PCIe capability, and AER. Original PCI/PCIe field semantics remain governed by PCI-SIG specifications.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1-3.8.7, printed pages 16-35, PDF pages 16-35

### 14. Platform security and isolation dependencies

<!-- claim:PCIE14-SECURITY -->

Power-loss signaling, confidential computing, and TDISP map platform events or isolation state to NVMe-controller behavior. Implementation still requires external PCIe/TDISP specifications not supplied for this report.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.8-3.8.10, printed pages 35-39, PDF pages 35-39

### 15. Receiver-eye measurement

<!-- claim:PCIE14-EOM -->

The Physical Interface Receiver Eye Opening Measurement log page reports measurements through a header, lane descriptors, and EOM data. The host checks support and size before parsing lanes and parameters.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.9, printed pages 39-46, PDF pages 39-46

### 16. Host implementation checklist

<!-- claim:PCIE14-HOST -->

Annex A is an informative host checklist: write the SQE before its doorbell, use phase to identify a new CQE, advance CQ head after consumption, and service every relevant CQ associated with an interrupt vector.

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

## Figure-by-Figure Guide

The source uses Figure numbers for diagrams and field-layout tables. No source artwork is reproduced; compact field and keyword indexes come from the locally verified PDFs.

<a id="section-1-2"></a>

### §1.2

<details markdown="1">
<summary><strong>Figure 1: NVMe Family of Specifications</strong></summary>

<!-- claim:PCIE14-FIG-001-CLAIM figure-table:PCIE14-FIG-001 -->

Figure 1, "NVMe Family of Specifications": Places NVMe Family of Specifications in the NVMe document and command-set hierarchy. Read from the common Base requirements toward the transport and command-set layer; keep these source-derived labels distinct: NVMe Family.

- Purpose: Places NVMe Family of Specifications in the NVMe document and command-set hierarchy.

- How to read: Read from the common Base requirements toward the transport and command-set layer; keep these source-derived labels distinct: NVMe Family.

- Conditions and limits: The Figure is explanatory or structural; this guide does not turn its visual relationship into a new requirement. Only the PCIe/memory-based portion is in scope.

- Informative example: Start with NVMe Family, then follow the branch containing the cited condition; cite the document that owns the requirement instead of assuming every layer defines it. This example adds no requirement.

- Source field index: NVMe Family

- Source keyword index: none

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §1.2, Figure 1, printed pages 6, PDF pages 6

</details>

<a id="section-2"></a>

### §2

<details markdown="1">
<summary><strong>Figure 2: Example of Transport Protocol Layers</strong></summary>

<!-- claim:PCIE14-FIG-002-CLAIM figure-table:PCIE14-FIG-002 -->

Figure 2, "Example of Transport Protocol Layers": Separates the responsibilities of the protocol layers in Example of Transport Protocol Layers. Read vertically by layer and horizontally by peer interaction; do not assign a transport rule to the Base layer. Evidence index: Transport Protocol Layers.

- Purpose: Separates the responsibilities of the protocol layers in Example of Transport Protocol Layers.

- How to read: Read vertically by layer and horizontally by peer interaction; do not assign a transport rule to the Base layer. Evidence index: Transport Protocol Layers.

- Conditions and limits: The Figure is explanatory or structural; this guide does not turn its visual relationship into a new requirement.

- Informative example: Start with Transport Protocol Layers, follow the operation to the cited condition, and cite the layer that defines the observed behavior. This example adds no requirement.

- Source field index: Transport Protocol Layers

- Source keyword index: none

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §2, Figure 2, printed pages 8, PDF pages 8

</details>

<a id="section-3-1"></a>

### §3.1

<details markdown="1">
<summary><strong>Figure 3: PCI Express Registers</strong></summary>

<!-- claim:PCIE14-FIG-003-CLAIM figure-table:PCIE14-FIG-003 -->

Figure 3, "PCI Express Registers": Defines the concrete layout or value relationships for PCI Express Registers. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is PMCAP, MSICAP, MSIXCAP, MSIX, PXCAP, AERCAP, MSI, MLBAR.

- Purpose: Defines the concrete layout or value relationships for PCI Express Registers.

- How to read: Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is PMCAP, MSICAP, MSIXCAP, MSIX, PXCAP, AERCAP, MSI, MLBAR.

- Conditions and limits: Source keyword index: `shall not`, `shall`, `should`, `may`, `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Use PMCAP as the first parser checkpoint and MSICAP as a second, independent boundary check. This example adds no requirement.

- Source field index: PMCAP, MSICAP, MSIXCAP, MSIX, PXCAP, AERCAP, MSI, MLBAR

- Source keyword index: `shall not`, `shall`, `should`, `may`, `reserved`

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.1, Figure 3, printed pages 9, PDF pages 9

</details>

<details markdown="1">
<summary><strong>Figure 4: PCI Express Specific Controller Property Definitions</strong></summary>

<!-- claim:PCIE14-FIG-004-CLAIM figure-table:PCIE14-FIG-004 -->

Figure 4, "PCI Express Specific Controller Property Definitions": Defines the concrete layout or value relationships for PCI Express Specific Controller Property Definitions. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is SQ0TDBL, CAP.DSTRD, CQ0HDBL, SQ1TDBL, CQ1HDBL, SQ2TDBL, CQ2HDBL, Controller.

- Purpose: Defines the concrete layout or value relationships for PCI Express Specific Controller Property Definitions.

- How to read: Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is SQ0TDBL, CAP.DSTRD, CQ0HDBL, SQ1TDBL, CQ1HDBL, SQ2TDBL, CQ2HDBL, Controller.

- Conditions and limits: Source keyword index: `optional`, `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Use SQ0TDBL as the first parser checkpoint and CAP.DSTRD as a second, independent boundary check. This example adds no requirement.

- Source field index: SQ0TDBL, CAP.DSTRD, CQ0HDBL, SQ1TDBL, CQ1HDBL, SQ2TDBL, CQ2HDBL, Controller

- Source keyword index: `optional`, `reserved`

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.1, Figure 4, printed pages 9-10, PDF pages 9-10

</details>

<details markdown="1">
<summary><strong>Figure 5: Offset (1000h + ((2y) * (4 &lt;&lt; CAP.DSTRD))): SQyTDBL - Submission Queue y Tail</strong></summary>

<!-- claim:PCIE14-FIG-005-CLAIM figure-table:PCIE14-FIG-005 -->

Figure 5, "Offset (1000h + ((2y) * (4 << CAP.DSTRD))): SQyTDBL - Submission Queue y Tail": Shows the queue or command relationship expressed by Offset (1000h + ((2y) * (4 << CAP.DSTRD))): SQyTDBL - Submission Queue y Tail. Trace ownership and direction from host to SQ, controller, and CQ; keep the indexed elements distinct: SQT, CAP.DSTRD, Submission Queue.

- Purpose: Shows the queue or command relationship expressed by Offset (1000h + ((2y) * (4 << CAP.DSTRD))): SQyTDBL - Submission Queue y Tail.

- How to read: Trace ownership and direction from host to SQ, controller, and CQ; keep the indexed elements distinct: SQT, CAP.DSTRD, Submission Queue.

- Conditions and limits: Source keyword index: `shall`, `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Trace one command through Figure 5, using SQT and CAP.DSTRD as checkpoints for ownership or pointer movement. This example adds no requirement.

- Source field index: SQT, CAP.DSTRD, Submission Queue

- Source keyword index: `shall`, `reserved`

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.1.2.1, Figure 5, printed pages 10, PDF pages 10

</details>

<details markdown="1">
<summary><strong>Figure 6: Offset (1000h + ((2y + 1) * (4 &lt;&lt; CAP.DSTRD))): CQyHDBL - Completion Queue y Head</strong></summary>

<!-- claim:PCIE14-FIG-006-CLAIM figure-table:PCIE14-FIG-006 -->

Figure 6, "Offset (1000h + ((2y + 1) * (4 << CAP.DSTRD))): CQyHDBL - Completion Queue y Head": Shows the queue or command relationship expressed by Offset (1000h + ((2y + 1) * (4 << CAP.DSTRD))): CQyHDBL - Completion Queue y Head. Trace ownership and direction from host to SQ, controller, and CQ; keep the indexed elements distinct: CQH, CAP.DSTRD, CC.PI, Completion Queue.

- Purpose: Shows the queue or command relationship expressed by Offset (1000h + ((2y + 1) * (4 << CAP.DSTRD))): CQyHDBL - Completion Queue y Head.

- How to read: Trace ownership and direction from host to SQ, controller, and CQ; keep the indexed elements distinct: CQH, CAP.DSTRD, CC.PI, Completion Queue.

- Conditions and limits: Source keyword index: `shall`, `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Trace one command through Figure 6, using CQH and CAP.DSTRD as checkpoints for ownership or pointer movement. This example adds no requirement.

- Source field index: CQH, CAP.DSTRD, CC.PI, Completion Queue

- Source keyword index: `shall`, `reserved`

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.1.2.1, Figure 6, printed pages 10-11, PDF pages 10-11

</details>

<a id="section-3-2"></a>

### §3.2

<details markdown="1">
<summary><strong>Figure 7: Create I/O Completion Queue - Command Dword 11</strong></summary>

<!-- claim:PCIE14-FIG-007-CLAIM figure-table:PCIE14-FIG-007 -->

Figure 7, "Create I/O Completion Queue - Command Dword 11": Defines command-specific fields in CDW11 for Create I/O Completion Queue. Locate CDW11, then decode the named fields without borrowing semantics from another command. Evidence index: IV, MSI, MSICAP.MC.MME, MSIXCAP.MXC.TS, Completion Queue, Command.

- Purpose: Defines command-specific fields in CDW11 for Create I/O Completion Queue.

- How to read: Locate CDW11, then decode the named fields without borrowing semantics from another command. Evidence index: IV, MSI, MSICAP.MC.MME, MSIXCAP.MXC.TS, Completion Queue, Command.

- Conditions and limits: Source keyword index: `shall not`, `shall`, `should`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Build one Create I/O Completion Queue entry, set IV, and independently validate MSI before ringing the Submission Queue doorbell. This example adds no requirement.

- Source field index: IV, MSI, MSICAP.MC.MME, MSIXCAP.MXC.TS, Completion Queue, Command

- Source keyword index: `shall not`, `shall`, `should`

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.2, Figure 7, printed pages 11, PDF pages 11

</details>

<a id="section-3-4"></a>

### §3.4

<details markdown="1">
<summary><strong>Figure 8: Command Processing</strong></summary>

<!-- claim:PCIE14-FIG-008-CLAIM figure-table:PCIE14-FIG-008 -->

Figure 8, "Command Processing": Shows the queue or command relationship expressed by Command Processing. Trace ownership and direction from host to SQ, controller, and CQ; keep the indexed elements distinct: Command.

- Purpose: Shows the queue or command relationship expressed by Command Processing.

- How to read: Trace ownership and direction from host to SQ, controller, and CQ; keep the indexed elements distinct: Command.

- Conditions and limits: The Figure is explanatory or structural; this guide does not turn its visual relationship into a new requirement.

- Informative example: Trace one command through Figure 8, using Command and the cited condition as checkpoints for ownership or pointer movement. This example adds no requirement.

- Source field index: Command

- Source keyword index: none

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.4.1, Figure 8, printed pages 13, PDF pages 13

</details>

<a id="section-3-5"></a>

### §3.5

<details markdown="1">
<summary><strong>Figure 9: Pin Based, Single MSI, and Multiple MSI Behavior</strong></summary>

<!-- claim:PCIE14-FIG-009-CLAIM figure-table:PCIE14-FIG-009 -->

Figure 9, "Pin Based, Single MSI, and Multiple MSI Behavior": Shows the interrupt delivery or masking relationship represented by Pin Based, Single MSI, and Multiple MSI Behavior. Trace the vector/message source, mask state, and delivery destination separately. Evidence index: MSI.

- Purpose: Shows the interrupt delivery or masking relationship represented by Pin Based, Single MSI, and Multiple MSI Behavior.

- How to read: Trace the vector/message source, mask state, and delivery destination separately. Evidence index: MSI.

- Conditions and limits: The Figure is explanatory or structural; this guide does not turn its visual relationship into a new requirement.

- Informative example: Select the source represented by MSI, then confirm the mask or vector condition represented by the cited condition before expecting delivery. This example adds no requirement.

- Source field index: MSI

- Source keyword index: none

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.5.1, Figure 9, printed pages 15, PDF pages 15

</details>

<a id="section-3-8"></a>

### §3.8

<details markdown="1">
<summary><strong>Figure 10: PCI Express Type 0/1 Common Configuration Space</strong></summary>

<!-- claim:PCIE14-FIG-010-CLAIM figure-table:PCIE14-FIG-010 -->

Figure 10, "PCI Express Type 0/1 Common Configuration Space": Defines the concrete layout or value relationships for PCI Express Type 0/1 Common Configuration Space. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is PCI Express Type 0/1 Common Configuration Space.

- Purpose: Defines the concrete layout or value relationships for PCI Express Type 0/1 Common Configuration Space.

- How to read: Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is PCI Express Type 0/1 Common Configuration Space.

- Conditions and limits: The Figure is explanatory or structural; this guide does not turn its visual relationship into a new requirement.

- Informative example: Use PCI Express Type 0/1 Common Configuration Space as the first parser checkpoint and the cited condition as a second, independent boundary check. This example adds no requirement.

- Source field index: PCI Express Type 0/1 Common Configuration Space

- Source keyword index: none

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8, Figure 10, printed pages 16-17, PDF pages 16-17

</details>

<details markdown="1">
<summary><strong>Figure 11: Offset 00h: ID - Identifiers</strong></summary>

<!-- claim:PCIE14-FIG-011-CLAIM figure-table:PCIE14-FIG-011 -->

Figure 11, "Offset 00h: ID - Identifiers": Defines ID (Identifiers) at offset 00h and identifies the fields that software must decode at that location. Start at ID, then map bit ranges to access type, reset value, and field meaning. Evidence index: ID, DID, VID.

- Purpose: Defines ID (Identifiers) at offset 00h and identifies the fields that software must decode at that location.

- How to read: Start at ID, then map bit ranges to access type, reset value, and field meaning. Evidence index: ID, DID, VID.

- Conditions and limits: The Figure is explanatory or structural; this guide does not turn its visual relationship into a new requirement.

- Informative example: Read ID with the required width, then verify ID and DID separately before using either value. This example adds no requirement.

- Source field index: ID, DID, VID

- Source keyword index: none

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.1, Figure 11, printed pages 17, PDF pages 17

</details>

<details markdown="1">
<summary><strong>Figure 12: Offset 04h: CMD - Command</strong></summary>

<!-- claim:PCIE14-FIG-012-CLAIM figure-table:PCIE14-FIG-012 -->

Figure 12, "Offset 04h: CMD - Command": Defines CMD (Command) at offset 04h and identifies the fields that software must decode at that location. Start at CMD, then map bit ranges to access type, reset value, and field meaning. Evidence index: CMD, SIG, ID, FBE, SERR, SEE, IDSEL, ISWCC.

- Purpose: Defines CMD (Command) at offset 04h and identifies the fields that software must decode at that location.

- How to read: Start at CMD, then map bit ranges to access type, reset value, and field meaning. Evidence index: CMD, SIG, ID, FBE, SERR, SEE, IDSEL, ISWCC.

- Conditions and limits: Source keyword index: `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Read CMD with the required width, then verify CMD and SIG separately before using either value. This example adds no requirement.

- Source field index: CMD, SIG, ID, FBE, SERR, SEE, IDSEL, ISWCC

- Source keyword index: `reserved`

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.2, Figure 12, printed pages 17, PDF pages 17

</details>

<details markdown="1">
<summary><strong>Figure 13: Offset 06h: STS - Device Status</strong></summary>

<!-- claim:PCIE14-FIG-013-CLAIM figure-table:PCIE14-FIG-013 -->

Figure 13, "Offset 06h: STS - Device Status": Defines STS (Device Status) at offset 06h and identifies the fields that software must decode at that location. Start at STS, then map bit ranges to access type, reset value, and field meaning. Evidence index: STS, DPE, SSE, RMA, RTA, STA, DEVSEL, DEVT.

- Purpose: Defines STS (Device Status) at offset 06h and identifies the fields that software must decode at that location.

- How to read: Start at STS, then map bit ranges to access type, reset value, and field meaning. Evidence index: STS, DPE, SSE, RMA, RTA, STA, DEVSEL, DEVT.

- Conditions and limits: Source keyword index: `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Read STS with the required width, then verify STS and DPE separately before using either value. This example adds no requirement.

- Source field index: STS, DPE, SSE, RMA, RTA, STA, DEVSEL, DEVT

- Source keyword index: `reserved`

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.3, Figure 13, printed pages 18, PDF pages 18

</details>

<details markdown="1">
<summary><strong>Figure 14: Offset 08h: RID - Revision ID</strong></summary>

<!-- claim:PCIE14-FIG-014-CLAIM figure-table:PCIE14-FIG-014 -->

Figure 14, "Offset 08h: RID - Revision ID": Defines RID (Revision ID) at offset 08h and identifies the fields that software must decode at that location. Start at RID, then map bit ranges to access type, reset value, and field meaning. Evidence index: RID, ID.

- Purpose: Defines RID (Revision ID) at offset 08h and identifies the fields that software must decode at that location.

- How to read: Start at RID, then map bit ranges to access type, reset value, and field meaning. Evidence index: RID, ID.

- Conditions and limits: The Figure is explanatory or structural; this guide does not turn its visual relationship into a new requirement.

- Informative example: Read RID with the required width, then verify RID and ID separately before using either value. This example adds no requirement.

- Source field index: RID, ID

- Source keyword index: none

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.4, Figure 14, printed pages 18, PDF pages 18

</details>

<details markdown="1">
<summary><strong>Figure 15: Offset 09h: CC - Class Code</strong></summary>

<!-- claim:PCIE14-FIG-015-CLAIM figure-table:PCIE14-FIG-015 -->

Figure 15, "Offset 09h: CC - Class Code": Defines CC (Class Code) at offset 09h and identifies the fields that software must decode at that location. Start at CC, then map bit ranges to access type, reset value, and field meaning. Evidence index: CC, BCC, SCC, PI.

- Purpose: Defines CC (Class Code) at offset 09h and identifies the fields that software must decode at that location.

- How to read: Start at CC, then map bit ranges to access type, reset value, and field meaning. Evidence index: CC, BCC, SCC, PI.

- Conditions and limits: The Figure is explanatory or structural; this guide does not turn its visual relationship into a new requirement.

- Informative example: Read CC with the required width, then verify CC and BCC separately before using either value. This example adds no requirement.

- Source field index: CC, BCC, SCC, PI

- Source keyword index: none

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.5, Figure 15, printed pages 18, PDF pages 18

</details>

<details markdown="1">
<summary><strong>Figure 16: Offset 0Ch: CLS - Cache Line Size</strong></summary>

<!-- claim:PCIE14-FIG-016-CLAIM figure-table:PCIE14-FIG-016 -->

Figure 16, "Offset 0Ch: CLS - Cache Line Size": Defines CLS (Cache Line Size) at offset 0Ch and identifies the fields that software must decode at that location. Start at CLS, then map bit ranges to access type, reset value, and field meaning. Evidence index: CLS.

- Purpose: Defines CLS (Cache Line Size) at offset 0Ch and identifies the fields that software must decode at that location.

- How to read: Start at CLS, then map bit ranges to access type, reset value, and field meaning. Evidence index: CLS.

- Conditions and limits: The Figure is explanatory or structural; this guide does not turn its visual relationship into a new requirement.

- Informative example: Read CLS with the required width, then verify CLS and the cited condition separately before using either value. This example adds no requirement.

- Source field index: CLS

- Source keyword index: none

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.6, Figure 16, printed pages 18, PDF pages 18

</details>

<details markdown="1">
<summary><strong>Figure 17: Offset 0Dh: MLT - Master Latency Timer</strong></summary>

<!-- claim:PCIE14-FIG-017-CLAIM figure-table:PCIE14-FIG-017 -->

Figure 17, "Offset 0Dh: MLT - Master Latency Timer": Defines MLT (Master Latency Timer) at offset 0Dh and identifies the fields that software must decode at that location. Start at MLT, then map bit ranges to access type, reset value, and field meaning. Evidence index: MLT.

- Purpose: Defines MLT (Master Latency Timer) at offset 0Dh and identifies the fields that software must decode at that location.

- How to read: Start at MLT, then map bit ranges to access type, reset value, and field meaning. Evidence index: MLT.

- Conditions and limits: The Figure is explanatory or structural; this guide does not turn its visual relationship into a new requirement.

- Informative example: Read MLT with the required width, then verify MLT and the cited condition separately before using either value. This example adds no requirement.

- Source field index: MLT

- Source keyword index: none

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.7, Figure 17, printed pages 18, PDF pages 18

</details>

<details markdown="1">
<summary><strong>Figure 18: Offset 0Eh: HTYPE - Header Type</strong></summary>

<!-- claim:PCIE14-FIG-018-CLAIM figure-table:PCIE14-FIG-018 -->

Figure 18, "Offset 0Eh: HTYPE - Header Type": Defines HTYPE (Header Type) at offset 0Eh and identifies the fields that software must decode at that location. Start at HTYPE, then map bit ranges to access type, reset value, and field meaning. Evidence index: HTYPE, MFD, HL.

- Purpose: Defines HTYPE (Header Type) at offset 0Eh and identifies the fields that software must decode at that location.

- How to read: Start at HTYPE, then map bit ranges to access type, reset value, and field meaning. Evidence index: HTYPE, MFD, HL.

- Conditions and limits: The Figure is explanatory or structural; this guide does not turn its visual relationship into a new requirement.

- Informative example: Read HTYPE with the required width, then verify HTYPE and MFD separately before using either value. This example adds no requirement.

- Source field index: HTYPE, MFD, HL

- Source keyword index: none

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.8, Figure 18, printed pages 19, PDF pages 19

</details>

<details markdown="1">
<summary><strong>Figure 19: Offset 0Fh: BIST - Built-In Self Test (Optional)</strong></summary>

<!-- claim:PCIE14-FIG-019-CLAIM figure-table:PCIE14-FIG-019 -->

Figure 19, "Offset 0Fh: BIST - Built-In Self Test (Optional)": Defines BIST (Built-In Self Test (Optional)) at offset 0Fh and identifies the fields that software must decode at that location. Start at BIST, then map bit ranges to access type, reset value, and field meaning. Evidence index: BIST, BC, SB, SIG, CC.

- Purpose: Defines BIST (Built-In Self Test (Optional)) at offset 0Fh and identifies the fields that software must decode at that location.

- How to read: Start at BIST, then map bit ranges to access type, reset value, and field meaning. Evidence index: BIST, BC, SB, SIG, CC.

- Conditions and limits: Source keyword index: `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Read BIST with the required width, then verify BIST and BC separately before using either value. This example adds no requirement.

- Source field index: BIST, BC, SB, SIG, CC

- Source keyword index: `reserved`

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.9, Figure 19, printed pages 19, PDF pages 19

</details>

<details markdown="1">
<summary><strong>Figure 20: Offset 10h: MLBAR (BAR0) - Memory Register Base Address, lower 32-bits</strong></summary>

<!-- claim:PCIE14-FIG-020-CLAIM figure-table:PCIE14-FIG-020 -->

Figure 20, "Offset 10h: MLBAR (BAR0) - Memory Register Base Address, lower 32-bits": Defines the concrete layout or value relationships for Offset 10h: MLBAR (BAR0) - Memory Register Base Address, lower 32-bits. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is BA, PF, TP, RTE, MLBAR, BAR0, SIG.

- Purpose: Defines the concrete layout or value relationships for Offset 10h: MLBAR (BAR0) - Memory Register Base Address, lower 32-bits.

- How to read: Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is BA, PF, TP, RTE, MLBAR, BAR0, SIG.

- Conditions and limits: Source keyword index: `may`, `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Use BA as the first parser checkpoint and PF as a second, independent boundary check. This example adds no requirement.

- Source field index: BA, PF, TP, RTE, MLBAR, BAR0, SIG

- Source keyword index: `may`, `reserved`

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.10, Figure 20, printed pages 19, PDF pages 19

</details>

<details markdown="1">
<summary><strong>Figure 21: Offset 14h: MUBAR (BAR1) - Memory Register Base Address, upper 32-bits</strong></summary>

<!-- claim:PCIE14-FIG-021-CLAIM figure-table:PCIE14-FIG-021 -->

Figure 21, "Offset 14h: MUBAR (BAR1) - Memory Register Base Address, upper 32-bits": Defines the concrete layout or value relationships for Offset 14h: MUBAR (BAR1) - Memory Register Base Address, upper 32-bits. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is BA, MUBAR, BAR1.

- Purpose: Defines the concrete layout or value relationships for Offset 14h: MUBAR (BAR1) - Memory Register Base Address, upper 32-bits.

- How to read: Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is BA, MUBAR, BAR1.

- Conditions and limits: Source keyword index: `may`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Use BA as the first parser checkpoint and MUBAR as a second, independent boundary check. This example adds no requirement.

- Source field index: BA, MUBAR, BAR1

- Source keyword index: `may`

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.11, Figure 21, printed pages 19, PDF pages 19

</details>

<details markdown="1">
<summary><strong>Figure 22: Offset 18h: BAR2 - Index/Data Pair Register Base Address or Vendor Specific</strong></summary>

<!-- claim:PCIE14-FIG-022-CLAIM figure-table:PCIE14-FIG-022 -->

Figure 22, "Offset 18h: BAR2 - Index/Data Pair Register Base Address or Vendor Specific": Defines BAR2 (Index/Data Pair Register Base Address or Vendor Specific) at offset 18h and identifies the fields that software must decode at that location. Start at BAR2, then map bit ranges to access type, reset value, and field meaning. Evidence index: BA, RTE, BAR2.

- Purpose: Defines BAR2 (Index/Data Pair Register Base Address or Vendor Specific) at offset 18h and identifies the fields that software must decode at that location.

- How to read: Start at BAR2, then map bit ranges to access type, reset value, and field meaning. Evidence index: BA, RTE, BAR2.

- Conditions and limits: Source keyword index: `may`, `optional`, `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Read BAR2 with the required width, then verify BA and RTE separately before using either value. This example adds no requirement.

- Source field index: BA, RTE, BAR2

- Source keyword index: `may`, `optional`, `reserved`

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.12, Figure 22, printed pages 20, PDF pages 20

</details>

<details markdown="1">
<summary><strong>Figure 23: Offset 28h: CCPTR - CardBus CIS Pointer</strong></summary>

<!-- claim:PCIE14-FIG-023-CLAIM figure-table:PCIE14-FIG-023 -->

Figure 23, "Offset 28h: CCPTR - CardBus CIS Pointer": Defines CCPTR (CardBus CIS Pointer) at offset 28h and identifies the fields that software must decode at that location. Start at CCPTR, then map bit ranges to access type, reset value, and field meaning. Evidence index: CCPTR, CIS.

- Purpose: Defines CCPTR (CardBus CIS Pointer) at offset 28h and identifies the fields that software must decode at that location.

- How to read: Start at CCPTR, then map bit ranges to access type, reset value, and field meaning. Evidence index: CCPTR, CIS.

- Conditions and limits: Source keyword index: `shall`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Read CCPTR with the required width, then verify CCPTR and CIS separately before using either value. This example adds no requirement.

- Source field index: CCPTR, CIS

- Source keyword index: `shall`

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.16, Figure 23, printed pages 20, PDF pages 20

</details>

<details markdown="1">
<summary><strong>Figure 24: Offset 2Ch: SS - Subsystem Identifiers</strong></summary>

<!-- claim:PCIE14-FIG-024-CLAIM figure-table:PCIE14-FIG-024 -->

Figure 24, "Offset 2Ch: SS - Subsystem Identifiers": Defines SS (Subsystem Identifiers) at offset 2Ch and identifies the fields that software must decode at that location. Start at SS, then map bit ranges to access type, reset value, and field meaning. Evidence index: SSID, SSVID, SS, ID.

- Purpose: Defines SS (Subsystem Identifiers) at offset 2Ch and identifies the fields that software must decode at that location.

- How to read: Start at SS, then map bit ranges to access type, reset value, and field meaning. Evidence index: SSID, SSVID, SS, ID.

- Conditions and limits: The Figure is explanatory or structural; this guide does not turn its visual relationship into a new requirement.

- Informative example: Read SS with the required width, then verify SSID and SSVID separately before using either value. This example adds no requirement.

- Source field index: SSID, SSVID, SS, ID

- Source keyword index: none

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.17, Figure 24, printed pages 20, PDF pages 20

</details>

<details markdown="1">
<summary><strong>Figure 25: Offset 30h: EROM - Expansion ROM (Optional)</strong></summary>

<!-- claim:PCIE14-FIG-025-CLAIM figure-table:PCIE14-FIG-025 -->

Figure 25, "Offset 30h: EROM - Expansion ROM (Optional)": Defines EROM (Expansion ROM (Optional)) at offset 30h and identifies the fields that software must decode at that location. Start at EROM, then map bit ranges to access type, reset value, and field meaning. Evidence index: RBA, EROM, ROM.

- Purpose: Defines EROM (Expansion ROM (Optional)) at offset 30h and identifies the fields that software must decode at that location.

- How to read: Start at EROM, then map bit ranges to access type, reset value, and field meaning. Evidence index: RBA, EROM, ROM.

- Conditions and limits: The Figure is explanatory or structural; this guide does not turn its visual relationship into a new requirement.

- Informative example: Read EROM with the required width, then verify RBA and EROM separately before using either value. This example adds no requirement.

- Source field index: RBA, EROM, ROM

- Source keyword index: none

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.18, Figure 25, printed pages 20, PDF pages 20

</details>

<details markdown="1">
<summary><strong>Figure 26: Offset 34h: CAP - Capabilities Pointer</strong></summary>

<!-- claim:PCIE14-FIG-026-CLAIM figure-table:PCIE14-FIG-026 -->

Figure 26, "Offset 34h: CAP - Capabilities Pointer": Defines CAP (Capabilities Pointer) at offset 34h and identifies the fields that software must decode at that location. Start at CAP, then map bit ranges to access type, reset value, and field meaning. Evidence index: CP, CAP.

- Purpose: Defines CAP (Capabilities Pointer) at offset 34h and identifies the fields that software must decode at that location.

- How to read: Start at CAP, then map bit ranges to access type, reset value, and field meaning. Evidence index: CP, CAP.

- Conditions and limits: The Figure is explanatory or structural; this guide does not turn its visual relationship into a new requirement.

- Informative example: Read CAP with the required width, then verify CP and CAP separately before using either value. This example adds no requirement.

- Source field index: CP, CAP

- Source keyword index: none

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.19, Figure 26, printed pages 21, PDF pages 21

</details>

<details markdown="1">
<summary><strong>Figure 27: Offset 3Ch: INTR - Interrupt Information</strong></summary>

<!-- claim:PCIE14-FIG-027-CLAIM figure-table:PCIE14-FIG-027 -->

Figure 27, "Offset 3Ch: INTR - Interrupt Information": Defines INTR (Interrupt Information) at offset 3Ch and identifies the fields that software must decode at that location. Start at INTR, then map bit ranges to access type, reset value, and field meaning. Evidence index: IPIN, ILINE, INTR, Interrupt.

- Purpose: Defines INTR (Interrupt Information) at offset 3Ch and identifies the fields that software must decode at that location.

- How to read: Start at INTR, then map bit ranges to access type, reset value, and field meaning. Evidence index: IPIN, ILINE, INTR, Interrupt.

- Conditions and limits: The Figure is explanatory or structural; this guide does not turn its visual relationship into a new requirement.

- Informative example: Read INTR with the required width, then verify IPIN and ILINE separately before using either value. This example adds no requirement.

- Source field index: IPIN, ILINE, INTR, Interrupt

- Source keyword index: none

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.20, Figure 27, printed pages 21, PDF pages 21

</details>

<details markdown="1">
<summary><strong>Figure 28: Offset 3Eh: MGNT - Minimum Grant</strong></summary>

<!-- claim:PCIE14-FIG-028-CLAIM figure-table:PCIE14-FIG-028 -->

Figure 28, "Offset 3Eh: MGNT - Minimum Grant": Defines MGNT (Minimum Grant) at offset 3Eh and identifies the fields that software must decode at that location. Start at MGNT, then map bit ranges to access type, reset value, and field meaning. Evidence index: GNT, MGNT.

- Purpose: Defines MGNT (Minimum Grant) at offset 3Eh and identifies the fields that software must decode at that location.

- How to read: Start at MGNT, then map bit ranges to access type, reset value, and field meaning. Evidence index: GNT, MGNT.

- Conditions and limits: The Figure is explanatory or structural; this guide does not turn its visual relationship into a new requirement.

- Informative example: Read MGNT with the required width, then verify GNT and MGNT separately before using either value. This example adds no requirement.

- Source field index: GNT, MGNT

- Source keyword index: none

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.21, Figure 28, printed pages 21, PDF pages 21

</details>

<details markdown="1">
<summary><strong>Figure 29: Offset 3Fh: MLAT - Maximum Latency</strong></summary>

<!-- claim:PCIE14-FIG-029-CLAIM figure-table:PCIE14-FIG-029 -->

Figure 29, "Offset 3Fh: MLAT - Maximum Latency": Defines MLAT (Maximum Latency) at offset 3Fh and identifies the fields that software must decode at that location. Start at MLAT, then map bit ranges to access type, reset value, and field meaning. Evidence index: LAT, MLAT, CC.

- Purpose: Defines MLAT (Maximum Latency) at offset 3Fh and identifies the fields that software must decode at that location.

- How to read: Start at MLAT, then map bit ranges to access type, reset value, and field meaning. Evidence index: LAT, MLAT, CC.

- Conditions and limits: The Figure is explanatory or structural; this guide does not turn its visual relationship into a new requirement.

- Informative example: Read MLAT with the required width, then verify LAT and MLAT separately before using either value. This example adds no requirement.

- Source field index: LAT, MLAT, CC

- Source keyword index: none

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.22, Figure 29, printed pages 21, PDF pages 21

</details>

<details markdown="1">
<summary><strong>Figure 30: PCI Power Management Capabilities</strong></summary>

<!-- claim:PCIE14-FIG-030-CLAIM figure-table:PCIE14-FIG-030 -->

Figure 30, "PCI Power Management Capabilities": Defines the concrete layout or value relationships for PCI Power Management Capabilities. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is PMCAP, PID, ID, PC, PMCS.

- Purpose: Defines the concrete layout or value relationships for PCI Power Management Capabilities.

- How to read: Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is PMCAP, PID, ID, PC, PMCS.

- Conditions and limits: The Figure is explanatory or structural; this guide does not turn its visual relationship into a new requirement.

- Informative example: Use PMCAP as the first parser checkpoint and PID as a second, independent boundary check. This example adds no requirement.

- Source field index: PMCAP, PID, ID, PC, PMCS

- Source keyword index: none

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.22, Figure 30, printed pages 21, PDF pages 21

</details>

<details markdown="1">
<summary><strong>Figure 31: Offset PMCAP: PID - PCI Power Management Capability ID</strong></summary>

<!-- claim:PCIE14-FIG-031-CLAIM figure-table:PCIE14-FIG-031 -->

Figure 31, "Offset PMCAP: PID - PCI Power Management Capability ID": Defines PID (PCI Power Management Capability ID) at offset PMCAP and identifies the fields that software must decode at that location. Start at PID, then map bit ranges to access type, reset value, and field meaning. Evidence index: NEXT, CID, PMCAP, PID, ID.

- Purpose: Defines PID (PCI Power Management Capability ID) at offset PMCAP and identifies the fields that software must decode at that location.

- How to read: Start at PID, then map bit ranges to access type, reset value, and field meaning. Evidence index: NEXT, CID, PMCAP, PID, ID.

- Conditions and limits: Source keyword index: `may`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Read PID with the required width, then verify NEXT and CID separately before using either value. This example adds no requirement.

- Source field index: NEXT, CID, PMCAP, PID, ID

- Source keyword index: `may`

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.2.1, Figure 31, printed pages 21, PDF pages 21

</details>

<details markdown="1">
<summary><strong>Figure 32: Offset PMCAP + 2h: PC - PCI Power Management Capabilities</strong></summary>

<!-- claim:PCIE14-FIG-032-CLAIM figure-table:PCIE14-FIG-032 -->

Figure 32, "Offset PMCAP + 2h: PC - PCI Power Management Capabilities": Defines PC (PCI Power Management Capabilities) at offset PMCAP + 2h and identifies the fields that software must decode at that location. Start at PC, then map bit ranges to access type, reset value, and field meaning. Evidence index: PSUP, D2S, D1S, AUXC, DSI, PMEC, VS, PMCAP.

- Purpose: Defines PC (PCI Power Management Capabilities) at offset PMCAP + 2h and identifies the fields that software must decode at that location.

- How to read: Start at PC, then map bit ranges to access type, reset value, and field meaning. Evidence index: PSUP, D2S, D1S, AUXC, DSI, PMEC, VS, PMCAP.

- Conditions and limits: Source keyword index: `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Read PC with the required width, then verify PSUP and D2S separately before using either value. This example adds no requirement.

- Source field index: PSUP, D2S, D1S, AUXC, DSI, PMEC, VS, PMCAP

- Source keyword index: `reserved`

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.2.2, Figure 32, printed pages 22, PDF pages 22

</details>

<details markdown="1">
<summary><strong>Figure 33: Offset PMCAP + 4h: PMCS - PCI Power Management Control and Status</strong></summary>

<!-- claim:PCIE14-FIG-033-CLAIM figure-table:PCIE14-FIG-033 -->

Figure 33, "Offset PMCAP + 4h: PMCS - PCI Power Management Control and Status": Defines PMCS (PCI Power Management Control and Status) at offset PMCAP + 4h and identifies the fields that software must decode at that location. Start at PMCS, then map bit ranges to access type, reset value, and field meaning. Evidence index: PMES, DSC, DSE, PMEE, NSFRST, PS, PMCAP, PMCS.

- Purpose: Defines PMCS (PCI Power Management Control and Status) at offset PMCAP + 4h and identifies the fields that software must decode at that location.

- How to read: Start at PMCS, then map bit ranges to access type, reset value, and field meaning. Evidence index: PMES, DSC, DSE, PMEE, NSFRST, PS, PMCAP, PMCS.

- Conditions and limits: Source keyword index: `optional`, `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Read PMCS with the required width, then verify PMES and DSC separately before using either value. This example adds no requirement.

- Source field index: PMES, DSC, DSE, PMEE, NSFRST, PS, PMCAP, PMCS

- Source keyword index: `optional`, `reserved`

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.2.3, Figure 33, printed pages 22, PDF pages 22

</details>

<details markdown="1">
<summary><strong>Figure 34: Message Signaled Interrupt Capability (Optional)</strong></summary>

<!-- claim:PCIE14-FIG-034-CLAIM figure-table:PCIE14-FIG-034 -->

Figure 34, "Message Signaled Interrupt Capability (Optional)": Defines the concrete layout or value relationships for Message Signaled Interrupt Capability (Optional). Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is MSICAP, MID, ID, MC, MA, MUA, MD, MMASK.

- Purpose: Defines the concrete layout or value relationships for Message Signaled Interrupt Capability (Optional).

- How to read: Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is MSICAP, MID, ID, MC, MA, MUA, MD, MMASK.

- Conditions and limits: Source keyword index: `optional`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Use MSICAP as the first parser checkpoint and MID as a second, independent boundary check. This example adds no requirement.

- Source field index: MSICAP, MID, ID, MC, MA, MUA, MD, MMASK

- Source keyword index: `optional`

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.2.3, Figure 34, printed pages 22, PDF pages 22

</details>

<details markdown="1">
<summary><strong>Figure 35: Offset MSICAP: MID - Message Signaled Interrupt Identifiers</strong></summary>

<!-- claim:PCIE14-FIG-035-CLAIM figure-table:PCIE14-FIG-035 -->

Figure 35, "Offset MSICAP: MID - Message Signaled Interrupt Identifiers": Defines MID (Message Signaled Interrupt Identifiers) at offset MSICAP and identifies the fields that software must decode at that location. Start at MID, then map bit ranges to access type, reset value, and field meaning. Evidence index: NEXT, CID, MSICAP, MID, ID, MSI, Interrupt.

- Purpose: Defines MID (Message Signaled Interrupt Identifiers) at offset MSICAP and identifies the fields that software must decode at that location.

- How to read: Start at MID, then map bit ranges to access type, reset value, and field meaning. Evidence index: NEXT, CID, MSICAP, MID, ID, MSI, Interrupt.

- Conditions and limits: Source keyword index: `may`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Read MID with the required width, then verify NEXT and CID separately before using either value. This example adds no requirement.

- Source field index: NEXT, CID, MSICAP, MID, ID, MSI, Interrupt

- Source keyword index: `may`

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.3.1, Figure 35, printed pages 23, PDF pages 23

</details>

<details markdown="1">
<summary><strong>Figure 36: Offset MSICAP + 2h: MC - Message Signaled Interrupt Message Control</strong></summary>

<!-- claim:PCIE14-FIG-036-CLAIM figure-table:PCIE14-FIG-036 -->

Figure 36, "Offset MSICAP + 2h: MC - Message Signaled Interrupt Message Control": Defines MC (Message Signaled Interrupt Message Control) at offset MSICAP + 2h and identifies the fields that software must decode at that location. Start at MC, then map bit ranges to access type, reset value, and field meaning. Evidence index: PVM, C64, MME, MMC, MSIE, MSICAP, MC, MSI.

- Purpose: Defines MC (Message Signaled Interrupt Message Control) at offset MSICAP + 2h and identifies the fields that software must decode at that location.

- How to read: Start at MC, then map bit ranges to access type, reset value, and field meaning. Evidence index: PVM, C64, MME, MMC, MSIE, MSICAP, MC, MSI.

- Conditions and limits: Source keyword index: `shall`, `should`, `may`, `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Read MC with the required width, then verify PVM and C64 separately before using either value. This example adds no requirement.

- Source field index: PVM, C64, MME, MMC, MSIE, MSICAP, MC, MSI

- Source keyword index: `shall`, `should`, `may`, `reserved`

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.3.2, Figure 36, printed pages 23, PDF pages 23

</details>

<details markdown="1">
<summary><strong>Figure 37: Offset MSICAP + 4h: MA - Message Signaled Interrupt Message Address</strong></summary>

<!-- claim:PCIE14-FIG-037-CLAIM figure-table:PCIE14-FIG-037 -->

Figure 37, "Offset MSICAP + 4h: MA - Message Signaled Interrupt Message Address": Defines MA (Message Signaled Interrupt Message Address) at offset MSICAP + 4h and identifies the fields that software must decode at that location. Start at MA, then map bit ranges to access type, reset value, and field meaning. Evidence index: ADDR, MSICAP, MA, SIG, Interrupt.

- Purpose: Defines MA (Message Signaled Interrupt Message Address) at offset MSICAP + 4h and identifies the fields that software must decode at that location.

- How to read: Start at MA, then map bit ranges to access type, reset value, and field meaning. Evidence index: ADDR, MSICAP, MA, SIG, Interrupt.

- Conditions and limits: Source keyword index: `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Read MA with the required width, then verify ADDR and MSICAP separately before using either value. This example adds no requirement.

- Source field index: ADDR, MSICAP, MA, SIG, Interrupt

- Source keyword index: `reserved`

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.3.3, Figure 37, printed pages 23, PDF pages 23

</details>

<details markdown="1">
<summary><strong>Figure 38: Offset MSICAP + 8h: MUA - Message Signaled Interrupt Upper Address</strong></summary>

<!-- claim:PCIE14-FIG-038-CLAIM figure-table:PCIE14-FIG-038 -->

Figure 38, "Offset MSICAP + 8h: MUA - Message Signaled Interrupt Upper Address": Defines MUA (Message Signaled Interrupt Upper Address) at offset MSICAP + 8h and identifies the fields that software must decode at that location. Start at MUA, then map bit ranges to access type, reset value, and field meaning. Evidence index: UADDR, MSICAP, MUA, MSI, Interrupt.

- Purpose: Defines MUA (Message Signaled Interrupt Upper Address) at offset MSICAP + 8h and identifies the fields that software must decode at that location.

- How to read: Start at MUA, then map bit ranges to access type, reset value, and field meaning. Evidence index: UADDR, MSICAP, MUA, MSI, Interrupt.

- Conditions and limits: The Figure is explanatory or structural; this guide does not turn its visual relationship into a new requirement.

- Informative example: Read MUA with the required width, then verify UADDR and MSICAP separately before using either value. This example adds no requirement.

- Source field index: UADDR, MSICAP, MUA, MSI, Interrupt

- Source keyword index: none

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.3.4, Figure 38, printed pages 23, PDF pages 23

</details>

<details markdown="1">
<summary><strong>Figure 39: Offset MSICAP + Ch: MD - Message Signaled Interrupt Message Data</strong></summary>

<!-- claim:PCIE14-FIG-039-CLAIM figure-table:PCIE14-FIG-039 -->

Figure 39, "Offset MSICAP + Ch: MD - Message Signaled Interrupt Message Data": Defines MD (Message Signaled Interrupt Message Data) at offset MSICAP + Ch and identifies the fields that software must decode at that location. Start at MD, then map bit ranges to access type, reset value, and field meaning. Evidence index: DATA, MSICAP, MD, MSI, AD, Interrupt.

- Purpose: Defines MD (Message Signaled Interrupt Message Data) at offset MSICAP + Ch and identifies the fields that software must decode at that location.

- How to read: Start at MD, then map bit ranges to access type, reset value, and field meaning. Evidence index: DATA, MSICAP, MD, MSI, AD, Interrupt.

- Conditions and limits: The Figure is explanatory or structural; this guide does not turn its visual relationship into a new requirement.

- Informative example: Read MD with the required width, then verify DATA and MSICAP separately before using either value. This example adds no requirement.

- Source field index: DATA, MSICAP, MD, MSI, AD, Interrupt

- Source keyword index: none

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.3.5, Figure 39, printed pages 23, PDF pages 23

</details>

<details markdown="1">
<summary><strong>Figure 40: Offset MSICAP + 10h: MMASK - Message Signaled Interrupt Mask Bits (Optional)</strong></summary>

<!-- claim:PCIE14-FIG-040-CLAIM figure-table:PCIE14-FIG-040 -->

Figure 40, "Offset MSICAP + 10h: MMASK - Message Signaled Interrupt Mask Bits (Optional)": Defines MMASK (Message Signaled Interrupt Mask Bits (Optional)) at offset MSICAP + 10h and identifies the fields that software must decode at that location. Start at MMASK, then map bit ranges to access type, reset value, and field meaning. Evidence index: MASK, MSICAP, MMASK, Interrupt.

- Purpose: Defines MMASK (Message Signaled Interrupt Mask Bits (Optional)) at offset MSICAP + 10h and identifies the fields that software must decode at that location.

- How to read: Start at MMASK, then map bit ranges to access type, reset value, and field meaning. Evidence index: MASK, MSICAP, MMASK, Interrupt.

- Conditions and limits: The Figure is explanatory or structural; this guide does not turn its visual relationship into a new requirement.

- Informative example: Read MMASK with the required width, then verify MASK and MSICAP separately before using either value. This example adds no requirement.

- Source field index: MASK, MSICAP, MMASK, Interrupt

- Source keyword index: none

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.3.6, Figure 40, printed pages 24, PDF pages 24

</details>

<details markdown="1">
<summary><strong>Figure 41: Offset MSICAP + 14h: MPEND - Message Signaled Interrupt Pending Bits (Optional)</strong></summary>

<!-- claim:PCIE14-FIG-041-CLAIM figure-table:PCIE14-FIG-041 -->

Figure 41, "Offset MSICAP + 14h: MPEND - Message Signaled Interrupt Pending Bits (Optional)": Defines MPEND (Message Signaled Interrupt Pending Bits (Optional)) at offset MSICAP + 14h and identifies the fields that software must decode at that location. Start at MPEND, then map bit ranges to access type, reset value, and field meaning. Evidence index: PEND, MSICAP, MPEND, MSIX, Interrupt.

- Purpose: Defines MPEND (Message Signaled Interrupt Pending Bits (Optional)) at offset MSICAP + 14h and identifies the fields that software must decode at that location.

- How to read: Start at MPEND, then map bit ranges to access type, reset value, and field meaning. Evidence index: PEND, MSICAP, MPEND, MSIX, Interrupt.

- Conditions and limits: Source keyword index: `optional`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Read MPEND with the required width, then verify PEND and MSICAP separately before using either value. This example adds no requirement.

- Source field index: PEND, MSICAP, MPEND, MSIX, Interrupt

- Source keyword index: `optional`

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.3.7, Figure 41, printed pages 24, PDF pages 24

</details>

<details markdown="1">
<summary><strong>Figure 42: MSI-X Capability (Optional)</strong></summary>

<!-- claim:PCIE14-FIG-042-CLAIM figure-table:PCIE14-FIG-042 -->

Figure 42, "MSI-X Capability (Optional)": Defines the concrete layout or value relationships for MSI-X Capability (Optional). Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is MSIX, MSIXCAP, MXID, ID, MXC, MTAB, BIR, MPBA.

- Purpose: Defines the concrete layout or value relationships for MSI-X Capability (Optional).

- How to read: Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is MSIX, MSIXCAP, MXID, ID, MXC, MTAB, BIR, MPBA.

- Conditions and limits: Source keyword index: `shall not`, `shall`, `should`, `may`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Use MSIX as the first parser checkpoint and MSIXCAP as a second, independent boundary check. This example adds no requirement.

- Source field index: MSIX, MSIXCAP, MXID, ID, MXC, MTAB, BIR, MPBA

- Source keyword index: `shall not`, `shall`, `should`, `may`

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.3.7, Figure 42, printed pages 24, PDF pages 24

</details>

<details markdown="1">
<summary><strong>Figure 43: Offset MSIXCAP: MXID - MSI-X Identifiers</strong></summary>

<!-- claim:PCIE14-FIG-043-CLAIM figure-table:PCIE14-FIG-043 -->

Figure 43, "Offset MSIXCAP: MXID - MSI-X Identifiers": Defines MXID (MSI-X Identifiers) at offset MSIXCAP and identifies the fields that software must decode at that location. Start at MXID, then map bit ranges to access type, reset value, and field meaning. Evidence index: NEXT, CID, MSIXCAP, MXID, MSIX, ID.

- Purpose: Defines MXID (MSI-X Identifiers) at offset MSIXCAP and identifies the fields that software must decode at that location.

- How to read: Start at MXID, then map bit ranges to access type, reset value, and field meaning. Evidence index: NEXT, CID, MSIXCAP, MXID, MSIX, ID.

- Conditions and limits: Source keyword index: `may`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Read MXID with the required width, then verify NEXT and CID separately before using either value. This example adds no requirement.

- Source field index: NEXT, CID, MSIXCAP, MXID, MSIX, ID

- Source keyword index: `may`

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.4.1, Figure 43, printed pages 24, PDF pages 24

</details>

<details markdown="1">
<summary><strong>Figure 44: Offset MSIXCAP + 2h: MXC - MSI-X Message Control</strong></summary>

<!-- claim:PCIE14-FIG-044-CLAIM figure-table:PCIE14-FIG-044 -->

Figure 44, "Offset MSIXCAP + 2h: MXC - MSI-X Message Control": Defines MXC (MSI-X Message Control) at offset MSIXCAP + 2h and identifies the fields that software must decode at that location. Start at MXC, then map bit ranges to access type, reset value, and field meaning. Evidence index: MXE, FM, TS, MSIXCAP, MXC, MSIX, MSI, SIG.

- Purpose: Defines MXC (MSI-X Message Control) at offset MSIXCAP + 2h and identifies the fields that software must decode at that location.

- How to read: Start at MXC, then map bit ranges to access type, reset value, and field meaning. Evidence index: MXE, FM, TS, MSIXCAP, MXC, MSIX, MSI, SIG.

- Conditions and limits: Source keyword index: `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Read MXC with the required width, then verify MXE and FM separately before using either value. This example adds no requirement.

- Source field index: MXE, FM, TS, MSIXCAP, MXC, MSIX, MSI, SIG

- Source keyword index: `reserved`

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.4.2, Figure 44, printed pages 24-25, PDF pages 24-25

</details>

<details markdown="1">
<summary><strong>Figure 45: Offset MSIXCAP + 4h: MTAB - MSI-X Table Offset / Table BIR</strong></summary>

<!-- claim:PCIE14-FIG-045-CLAIM figure-table:PCIE14-FIG-045 -->

Figure 45, "Offset MSIXCAP + 4h: MTAB - MSI-X Table Offset / Table BIR": Defines MTAB (MSI-X Table Offset / Table BIR) at offset MSIXCAP + 4h and identifies the fields that software must decode at that location. Start at MTAB, then map bit ranges to access type, reset value, and field meaning. Evidence index: TO, TBIR, MSIXCAP, MTAB, MSIX, BIR, MSI, BAR.

- Purpose: Defines MTAB (MSI-X Table Offset / Table BIR) at offset MSIXCAP + 4h and identifies the fields that software must decode at that location.

- How to read: Start at MTAB, then map bit ranges to access type, reset value, and field meaning. Evidence index: TO, TBIR, MSIXCAP, MTAB, MSIX, BIR, MSI, BAR.

- Conditions and limits: Source keyword index: `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Read MTAB with the required width, then verify TO and TBIR separately before using either value. This example adds no requirement.

- Source field index: TO, TBIR, MSIXCAP, MTAB, MSIX, BIR, MSI, BAR

- Source keyword index: `reserved`

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.4.3, Figure 45, printed pages 25, PDF pages 25

</details>

<details markdown="1">
<summary><strong>Figure 46: Offset MSIXCAP + 8h: MPBA - MSI-X PBA Offset / PBA BIR</strong></summary>

<!-- claim:PCIE14-FIG-046-CLAIM figure-table:PCIE14-FIG-046 -->

Figure 46, "Offset MSIXCAP + 8h: MPBA - MSI-X PBA Offset / PBA BIR": Defines MPBA (MSI-X PBA Offset / PBA BIR) at offset MSIXCAP + 8h and identifies the fields that software must decode at that location. Start at MPBA, then map bit ranges to access type, reset value, and field meaning. Evidence index: PBAO, PBIR, MSIXCAP, MPBA, MSIX, PBA, BIR, MSI.

- Purpose: Defines MPBA (MSI-X PBA Offset / PBA BIR) at offset MSIXCAP + 8h and identifies the fields that software must decode at that location.

- How to read: Start at MPBA, then map bit ranges to access type, reset value, and field meaning. Evidence index: PBAO, PBIR, MSIXCAP, MPBA, MSIX, PBA, BIR, MSI.

- Conditions and limits: Source keyword index: `may`, `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Read MPBA with the required width, then verify PBAO and PBIR separately before using either value. This example adds no requirement.

- Source field index: PBAO, PBIR, MSIXCAP, MPBA, MSIX, PBA, BIR, MSI

- Source keyword index: `may`, `reserved`

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.4.4, Figure 46, printed pages 25, PDF pages 25

</details>

<details markdown="1">
<summary><strong>Figure 47: PCI Express Capability</strong></summary>

<!-- claim:PCIE14-FIG-047-CLAIM figure-table:PCIE14-FIG-047 -->

Figure 47, "PCI Express Capability": Defines the concrete layout or value relationships for PCI Express Capability. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is PXCAP, PXID, ID, PXDCAP, PXDC, PXDS, PXLCAP, PXLC.

- Purpose: Defines the concrete layout or value relationships for PCI Express Capability.

- How to read: Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is PXCAP, PXID, ID, PXDCAP, PXDC, PXDS, PXLCAP, PXLC.

- Conditions and limits: The Figure is explanatory or structural; this guide does not turn its visual relationship into a new requirement.

- Informative example: Use PXCAP as the first parser checkpoint and PXID as a second, independent boundary check. This example adds no requirement.

- Source field index: PXCAP, PXID, ID, PXDCAP, PXDC, PXDS, PXLCAP, PXLC

- Source keyword index: none

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.5, Figure 47, printed pages 26, PDF pages 26

</details>

<details markdown="1">
<summary><strong>Figure 48: Offset PXCAP: PXID - PCI Express Capability ID</strong></summary>

<!-- claim:PCIE14-FIG-048-CLAIM figure-table:PCIE14-FIG-048 -->

Figure 48, "Offset PXCAP: PXID - PCI Express Capability ID": Defines PXID (PCI Express Capability ID) at offset PXCAP and identifies the fields that software must decode at that location. Start at PXID, then map bit ranges to access type, reset value, and field meaning. Evidence index: NEXT, CID, PXCAP, PXID, ID.

- Purpose: Defines PXID (PCI Express Capability ID) at offset PXCAP and identifies the fields that software must decode at that location.

- How to read: Start at PXID, then map bit ranges to access type, reset value, and field meaning. Evidence index: NEXT, CID, PXCAP, PXID, ID.

- Conditions and limits: Source keyword index: `may`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Read PXID with the required width, then verify NEXT and CID separately before using either value. This example adds no requirement.

- Source field index: NEXT, CID, PXCAP, PXID, ID

- Source keyword index: `may`

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.5.1, Figure 48, printed pages 26, PDF pages 26

</details>

<details markdown="1">
<summary><strong>Figure 49: Offset PXCAP + 2h: PXCAP - PCI Express Capabilities</strong></summary>

<!-- claim:PCIE14-FIG-049-CLAIM figure-table:PCIE14-FIG-049 -->

Figure 49, "Offset PXCAP + 2h: PXCAP - PCI Express Capabilities": Defines PXCAP (PCI Express Capabilities) at offset PXCAP + 2h and identifies the fields that software must decode at that location. Start at PXCAP, then map bit ranges to access type, reset value, and field meaning. Evidence index: IMN, SI, DPT, VER, PXCAP, SIG, MSI.

- Purpose: Defines PXCAP (PCI Express Capabilities) at offset PXCAP + 2h and identifies the fields that software must decode at that location.

- How to read: Start at PXCAP, then map bit ranges to access type, reset value, and field meaning. Evidence index: IMN, SI, DPT, VER, PXCAP, SIG, MSI.

- Conditions and limits: Source keyword index: `shall`, `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Read PXCAP with the required width, then verify IMN and SI separately before using either value. This example adds no requirement.

- Source field index: IMN, SI, DPT, VER, PXCAP, SIG, MSI

- Source keyword index: `shall`, `reserved`

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.5.2, Figure 49, printed pages 26, PDF pages 26

</details>

<details markdown="1">
<summary><strong>Figure 50: Offset PXCAP + 4h: PXDCAP - PCI Express Device Capabilities</strong></summary>

<!-- claim:PCIE14-FIG-050-CLAIM figure-table:PCIE14-FIG-050 -->

Figure 50, "Offset PXCAP + 4h: PXDCAP - PCI Express Device Capabilities": Defines PXDCAP (PCI Express Device Capabilities) at offset PXCAP + 4h and identifies the fields that software must decode at that location. Start at PXDCAP, then map bit ranges to access type, reset value, and field meaning. Evidence index: FLRC, CSPLS, CSPLV, RER, L1L, L0SL, ETFS, PFS.

- Purpose: Defines PXDCAP (PCI Express Device Capabilities) at offset PXCAP + 4h and identifies the fields that software must decode at that location.

- How to read: Start at PXDCAP, then map bit ranges to access type, reset value, and field meaning. Evidence index: FLRC, CSPLS, CSPLV, RER, L1L, L0SL, ETFS, PFS.

- Conditions and limits: Source keyword index: `shall`, `may`, `optional`, `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Read PXDCAP with the required width, then verify FLRC and CSPLS separately before using either value. This example adds no requirement.

- Source field index: FLRC, CSPLS, CSPLV, RER, L1L, L0SL, ETFS, PFS

- Source keyword index: `shall`, `may`, `optional`, `reserved`

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.5.3, Figure 50, printed pages 26-27, PDF pages 26-27

</details>

<details markdown="1">
<summary><strong>Figure 51: Offset PXCAP + 8h: PXDC - PCI Express Device Control</strong></summary>

<!-- claim:PCIE14-FIG-051-CLAIM figure-table:PCIE14-FIG-051 -->

Figure 51, "Offset PXCAP + 8h: PXDC - PCI Express Device Control": Defines PXDC (PCI Express Device Control) at offset PXCAP + 8h and identifies the fields that software must decode at that location. Start at PXDC, then map bit ranges to access type, reset value, and field meaning. Evidence index: IFLR, MRRS, ENS, APPME, PFE, ETE, MPS, ERO.

- Purpose: Defines PXDC (PCI Express Device Control) at offset PXCAP + 8h and identifies the fields that software must decode at that location.

- How to read: Start at PXDC, then map bit ranges to access type, reset value, and field meaning. Evidence index: IFLR, MRRS, ENS, APPME, PFE, ETE, MPS, ERO.

- Conditions and limits: Source keyword index: `shall not`, `shall`, `may`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Read PXDC with the required width, then verify IFLR and MRRS separately before using either value. This example adds no requirement.

- Source field index: IFLR, MRRS, ENS, APPME, PFE, ETE, MPS, ERO

- Source keyword index: `shall not`, `shall`, `may`

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.5.4, Figure 51, printed pages 27-28, PDF pages 27-28

</details>

<details markdown="1">
<summary><strong>Figure 52: Offset PXCAP + Ah: PXDS - PCI Express Device Status</strong></summary>

<!-- claim:PCIE14-FIG-052-CLAIM figure-table:PCIE14-FIG-052 -->

Figure 52, "Offset PXCAP + Ah: PXDS - PCI Express Device Status": Defines PXDS (PCI Express Device Status) at offset PXCAP + Ah and identifies the fields that software must decode at that location. Start at PXDS, then map bit ranges to access type, reset value, and field meaning. Evidence index: TP, APD, URD, FED, NFED, CED, PXCAP, PXDS.

- Purpose: Defines PXDS (PCI Express Device Status) at offset PXCAP + Ah and identifies the fields that software must decode at that location.

- How to read: Start at PXDS, then map bit ranges to access type, reset value, and field meaning. Evidence index: TP, APD, URD, FED, NFED, CED, PXCAP, PXDS.

- Conditions and limits: Source keyword index: `shall`, `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Read PXDS with the required width, then verify TP and APD separately before using either value. This example adds no requirement.

- Source field index: TP, APD, URD, FED, NFED, CED, PXCAP, PXDS

- Source keyword index: `shall`, `reserved`

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.5.5, Figure 52, printed pages 28, PDF pages 28

</details>

<details markdown="1">
<summary><strong>Figure 53: Offset PXCAP + Ch: PXLCAP - PCI Express Link Capabilities</strong></summary>

<!-- claim:PCIE14-FIG-053-CLAIM figure-table:PCIE14-FIG-053 -->

Figure 53, "Offset PXCAP + Ch: PXLCAP - PCI Express Link Capabilities": Defines PXLCAP (PCI Express Link Capabilities) at offset PXCAP + Ch and identifies the fields that software must decode at that location. Start at PXLCAP, then map bit ranges to access type, reset value, and field meaning. Evidence index: PN, AOC, LBNC, DLLLA, SDERC, CPM, L1EL, L0SEL.

- Purpose: Defines PXLCAP (PCI Express Link Capabilities) at offset PXCAP + Ch and identifies the fields that software must decode at that location.

- How to read: Start at PXLCAP, then map bit ranges to access type, reset value, and field meaning. Evidence index: PN, AOC, LBNC, DLLLA, SDERC, CPM, L1EL, L0SEL.

- Conditions and limits: Source keyword index: `shall not`, `shall`, `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Read PXLCAP with the required width, then verify PN and AOC separately before using either value. This example adds no requirement.

- Source field index: PN, AOC, LBNC, DLLLA, SDERC, CPM, L1EL, L0SEL

- Source keyword index: `shall not`, `shall`, `reserved`

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.5.6, Figure 53, printed pages 28-29, PDF pages 28-29

</details>

<details markdown="1">
<summary><strong>Figure 54: Offset PXCAP + 10h: PXLC - PCI Express Link Control</strong></summary>

<!-- claim:PCIE14-FIG-054-CLAIM figure-table:PCIE14-FIG-054 -->

Figure 54, "Offset PXCAP + 10h: PXLC - PCI Express Link Control": Defines PXLC (PCI Express Link Control) at offset PXCAP + 10h and identifies the fields that software must decode at that location. Start at PXLC, then map bit ranges to access type, reset value, and field meaning. Evidence index: HAWD, ECPM, ES, CCC, RCB, ASPMC, PXCAP, PXLC.

- Purpose: Defines PXLC (PCI Express Link Control) at offset PXCAP + 10h and identifies the fields that software must decode at that location.

- How to read: Start at PXLC, then map bit ranges to access type, reset value, and field meaning. Evidence index: HAWD, ECPM, ES, CCC, RCB, ASPMC, PXCAP, PXLC.

- Conditions and limits: Source keyword index: `shall`, `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Read PXLC with the required width, then verify HAWD and ECPM separately before using either value. This example adds no requirement.

- Source field index: HAWD, ECPM, ES, CCC, RCB, ASPMC, PXCAP, PXLC

- Source keyword index: `shall`, `reserved`

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.5.7, Figure 54, printed pages 29, PDF pages 29

</details>

<details markdown="1">
<summary><strong>Figure 55: Offset PXCAP + 12h: PXLS - PCI Express Link Status</strong></summary>

<!-- claim:PCIE14-FIG-055-CLAIM figure-table:PCIE14-FIG-055 -->

Figure 55, "Offset PXCAP + 12h: PXLS - PCI Express Link Status": Defines PXLS (PCI Express Link Status) at offset PXCAP + 12h and identifies the fields that software must decode at that location. Start at PXLS, then map bit ranges to access type, reset value, and field meaning. Evidence index: SCC, NLW, CLS, PXCAP, PXLS, SIG.

- Purpose: Defines PXLS (PCI Express Link Status) at offset PXCAP + 12h and identifies the fields that software must decode at that location.

- How to read: Start at PXLS, then map bit ranges to access type, reset value, and field meaning. Evidence index: SCC, NLW, CLS, PXCAP, PXLS, SIG.

- Conditions and limits: Source keyword index: `shall`, `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Read PXLS with the required width, then verify SCC and NLW separately before using either value. This example adds no requirement.

- Source field index: SCC, NLW, CLS, PXCAP, PXLS, SIG

- Source keyword index: `shall`, `reserved`

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.5.8, Figure 55, printed pages 29, PDF pages 29

</details>

<details markdown="1">
<summary><strong>Figure 56: Offset PXCAP + 24h: PXDCAP2 - PCI Express Device Capabilities 2</strong></summary>

<!-- claim:PCIE14-FIG-056-CLAIM figure-table:PCIE14-FIG-056 -->

Figure 56, "Offset PXCAP + 24h: PXDCAP2 - PCI Express Device Capabilities 2": Defines PXDCAP2 (PCI Express Device Capabilities 2) at offset PXCAP + 24h and identifies the fields that software must decode at that location. Start at PXDCAP2, then map bit ranges to access type, reset value, and field meaning. Evidence index: MEETP, EETPS, EFFS, OBFFS, TPHCS, LTRS, NPRPR, AORS.

- Purpose: Defines PXDCAP2 (PCI Express Device Capabilities 2) at offset PXCAP + 24h and identifies the fields that software must decode at that location.

- How to read: Start at PXDCAP2, then map bit ranges to access type, reset value, and field meaning. Evidence index: MEETP, EETPS, EFFS, OBFFS, TPHCS, LTRS, NPRPR, AORS.

- Conditions and limits: Source keyword index: `shall`, `optional`, `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Read PXDCAP2 with the required width, then verify MEETP and EETPS separately before using either value. This example adds no requirement.

- Source field index: MEETP, EETPS, EFFS, OBFFS, TPHCS, LTRS, NPRPR, AORS

- Source keyword index: `shall`, `optional`, `reserved`

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.5.9, Figure 56, printed pages 30, PDF pages 30

</details>

<details markdown="1">
<summary><strong>Figure 57: Offset PXCAP + 28h: PXDC2 - PCI Express Device Control 2</strong></summary>

<!-- claim:PCIE14-FIG-057-CLAIM figure-table:PCIE14-FIG-057 -->

Figure 57, "Offset PXCAP + 28h: PXDC2 - PCI Express Device Control 2": Defines PXDC2 (PCI Express Device Control 2) at offset PXCAP + 28h and identifies the fields that software must decode at that location. Start at PXDC2, then map bit ranges to access type, reset value, and field meaning. Evidence index: OBFFE, LTRME, CTD, CTV, PXCAP, PXDC2, SIG, OBFF.

- Purpose: Defines PXDC2 (PCI Express Device Control 2) at offset PXCAP + 28h and identifies the fields that software must decode at that location.

- How to read: Start at PXDC2, then map bit ranges to access type, reset value, and field meaning. Evidence index: OBFFE, LTRME, CTD, CTV, PXCAP, PXDC2, SIG, OBFF.

- Conditions and limits: Source keyword index: `may`, `optional`, `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Read PXDC2 with the required width, then verify OBFFE and LTRME separately before using either value. This example adds no requirement.

- Source field index: OBFFE, LTRME, CTD, CTV, PXCAP, PXDC2, SIG, OBFF

- Source keyword index: `may`, `optional`, `reserved`

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.5.10, Figure 57, printed pages 30-31, PDF pages 30-31

</details>

<details markdown="1">
<summary><strong>Figure 58: Advanced Error Reporting Capability (Optional)</strong></summary>

<!-- claim:PCIE14-FIG-058-CLAIM figure-table:PCIE14-FIG-058 -->

Figure 58, "Advanced Error Reporting Capability (Optional)": Defines the status/error classification represented by Advanced Error Reporting Capability (Optional). Resolve the category before the individual code or flag; keep reserved values uninterpreted. Evidence index: AERCAP, AERID, AER, ID, AERUCES, AERUCEM, AERUCESEV, AERCES.

- Purpose: Defines the status/error classification represented by Advanced Error Reporting Capability (Optional).

- How to read: Resolve the category before the individual code or flag; keep reserved values uninterpreted. Evidence index: AERCAP, AERID, AER, ID, AERUCES, AERUCEM, AERUCESEV, AERCES.

- Conditions and limits: Source keyword index: `optional`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: For one reported condition, identify AERCAP first and then check AERID instead of decoding an isolated numeric value. This example adds no requirement.

- Source field index: AERCAP, AERID, AER, ID, AERUCES, AERUCEM, AERUCESEV, AERCES

- Source keyword index: `optional`

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.5.10, Figure 58, printed pages 31, PDF pages 31

</details>

<details markdown="1">
<summary><strong>Figure 59: Offset AERCAP: AERID - AER Capability ID</strong></summary>

<!-- claim:PCIE14-FIG-059-CLAIM figure-table:PCIE14-FIG-059 -->

Figure 59, "Offset AERCAP: AERID - AER Capability ID": Defines AERID (AER Capability ID) at offset AERCAP and identifies the fields that software must decode at that location. Start at AERID, then map bit ranges to access type, reset value, and field meaning. Evidence index: NEXT, CVER, CID, AERCAP, AERID, AER, ID.

- Purpose: Defines AERID (AER Capability ID) at offset AERCAP and identifies the fields that software must decode at that location.

- How to read: Start at AERID, then map bit ranges to access type, reset value, and field meaning. Evidence index: NEXT, CVER, CID, AERCAP, AERID, AER, ID.

- Conditions and limits: Source keyword index: `may`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Read AERID with the required width, then verify NEXT and CVER separately before using either value. This example adds no requirement.

- Source field index: NEXT, CVER, CID, AERCAP, AERID, AER, ID

- Source keyword index: `may`

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.6.1, Figure 59, printed pages 31, PDF pages 31

</details>

<details markdown="1">
<summary><strong>Figure 60: Offset AERCAP + 4: AERUCES - AER Uncorrectable Error Status Register</strong></summary>

<!-- claim:PCIE14-FIG-060-CLAIM figure-table:PCIE14-FIG-060 -->

Figure 60, "Offset AERCAP + 4: AERUCES - AER Uncorrectable Error Status Register": Defines AERUCES (AER Uncorrectable Error Status Register) at offset AERCAP + 4 and identifies the fields that software must decode at that location. Start at AERUCES, then map bit ranges to access type, reset value, and field meaning. Evidence index: TPBES, AOEBS, MCBTS, UIES, ACSVS, ECRCES, ROS, CAS.

- Purpose: Defines AERUCES (AER Uncorrectable Error Status Register) at offset AERCAP + 4 and identifies the fields that software must decode at that location.

- How to read: Start at AERUCES, then map bit ranges to access type, reset value, and field meaning. Evidence index: TPBES, AOEBS, MCBTS, UIES, ACSVS, ECRCES, ROS, CAS.

- Conditions and limits: Source keyword index: `optional`, `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Read AERUCES with the required width, then verify TPBES and AOEBS separately before using either value. This example adds no requirement.

- Source field index: TPBES, AOEBS, MCBTS, UIES, ACSVS, ECRCES, ROS, CAS

- Source keyword index: `optional`, `reserved`

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.6.2, Figure 60, printed pages 31-32, PDF pages 31-32

</details>

<details markdown="1">
<summary><strong>Figure 61: Offset AERCAP + 8: AERUCEM - AER Uncorrectable Error Mask Register</strong></summary>

<!-- claim:PCIE14-FIG-061-CLAIM figure-table:PCIE14-FIG-061 -->

Figure 61, "Offset AERCAP + 8: AERUCEM - AER Uncorrectable Error Mask Register": Defines AERUCEM (AER Uncorrectable Error Mask Register) at offset AERCAP + 8 and identifies the fields that software must decode at that location. Start at AERUCEM, then map bit ranges to access type, reset value, and field meaning. Evidence index: TPBEM, AOEBM, MCBTM, UIEM, ACSVM, ECRCEM, ROM, CAM.

- Purpose: Defines AERUCEM (AER Uncorrectable Error Mask Register) at offset AERCAP + 8 and identifies the fields that software must decode at that location.

- How to read: Start at AERUCEM, then map bit ranges to access type, reset value, and field meaning. Evidence index: TPBEM, AOEBM, MCBTM, UIEM, ACSVM, ECRCEM, ROM, CAM.

- Conditions and limits: Source keyword index: `optional`, `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Read AERUCEM with the required width, then verify TPBEM and AOEBM separately before using either value. This example adds no requirement.

- Source field index: TPBEM, AOEBM, MCBTM, UIEM, ACSVM, ECRCEM, ROM, CAM

- Source keyword index: `optional`, `reserved`

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.6.3, Figure 61, printed pages 32, PDF pages 32

</details>

<details markdown="1">
<summary><strong>Figure 62: Offset AERCAP + Ch: AERUCESEV - AER Uncorrectable Error Severity Register</strong></summary>

<!-- claim:PCIE14-FIG-062-CLAIM figure-table:PCIE14-FIG-062 -->

Figure 62, "Offset AERCAP + Ch: AERUCESEV - AER Uncorrectable Error Severity Register": Defines AERUCESEV (AER Uncorrectable Error Severity Register) at offset AERCAP + Ch and identifies the fields that software must decode at that location. Start at AERUCESEV, then map bit ranges to access type, reset value, and field meaning. Evidence index: TPBESEV, AOEBSEV, MCBTSEV, UIESEV, ACSVSEV, ECRCESEV, ROSEV, CASEV.

- Purpose: Defines AERUCESEV (AER Uncorrectable Error Severity Register) at offset AERCAP + Ch and identifies the fields that software must decode at that location.

- How to read: Start at AERUCESEV, then map bit ranges to access type, reset value, and field meaning. Evidence index: TPBESEV, AOEBSEV, MCBTSEV, UIESEV, ACSVSEV, ECRCESEV, ROSEV, CASEV.

- Conditions and limits: Source keyword index: `optional`, `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Read AERUCESEV with the required width, then verify TPBESEV and AOEBSEV separately before using either value. This example adds no requirement.

- Source field index: TPBESEV, AOEBSEV, MCBTSEV, UIESEV, ACSVSEV, ECRCESEV, ROSEV, CASEV

- Source keyword index: `optional`, `reserved`

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.6.4, Figure 62, printed pages 32-33, PDF pages 32-33

</details>

<details markdown="1">
<summary><strong>Figure 63: Offset AERCAP + 10h: AERCES - AER Correctable Error Status Register</strong></summary>

<!-- claim:PCIE14-FIG-063-CLAIM figure-table:PCIE14-FIG-063 -->

Figure 63, "Offset AERCAP + 10h: AERCES - AER Correctable Error Status Register": Defines AERCES (AER Correctable Error Status Register) at offset AERCAP + 10h and identifies the fields that software must decode at that location. Start at AERCES, then map bit ranges to access type, reset value, and field meaning. Evidence index: HLOS, CIES, AERCAP, AERCES, AER, SIG, RWC, ANFES.

- Purpose: Defines AERCES (AER Correctable Error Status Register) at offset AERCAP + 10h and identifies the fields that software must decode at that location.

- How to read: Start at AERCES, then map bit ranges to access type, reset value, and field meaning. Evidence index: HLOS, CIES, AERCAP, AERCES, AER, SIG, RWC, ANFES.

- Conditions and limits: Source keyword index: `optional`, `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Read AERCES with the required width, then verify HLOS and CIES separately before using either value. This example adds no requirement.

- Source field index: HLOS, CIES, AERCAP, AERCES, AER, SIG, RWC, ANFES

- Source keyword index: `optional`, `reserved`

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.6.5, Figure 63, printed pages 33, PDF pages 33

</details>

<details markdown="1">
<summary><strong>Figure 64: Offset AERCAP + 14h: AERCEM - AER Correctable Error Mask Register</strong></summary>

<!-- claim:PCIE14-FIG-064-CLAIM figure-table:PCIE14-FIG-064 -->

Figure 64, "Offset AERCAP + 14h: AERCEM - AER Correctable Error Mask Register": Defines AERCEM (AER Correctable Error Mask Register) at offset AERCAP + 14h and identifies the fields that software must decode at that location. Start at AERCEM, then map bit ranges to access type, reset value, and field meaning. Evidence index: HLOM, CIEM, AERCAP, AERCEM, AER, SIG, ANFEM, RTM.

- Purpose: Defines AERCEM (AER Correctable Error Mask Register) at offset AERCAP + 14h and identifies the fields that software must decode at that location.

- How to read: Start at AERCEM, then map bit ranges to access type, reset value, and field meaning. Evidence index: HLOM, CIEM, AERCAP, AERCEM, AER, SIG, ANFEM, RTM.

- Conditions and limits: Source keyword index: `optional`, `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Read AERCEM with the required width, then verify HLOM and CIEM separately before using either value. This example adds no requirement.

- Source field index: HLOM, CIEM, AERCAP, AERCEM, AER, SIG, ANFEM, RTM

- Source keyword index: `optional`, `reserved`

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.6.6, Figure 64, printed pages 33, PDF pages 33

</details>

<details markdown="1">
<summary><strong>Figure 65: Offset AERCAP + 18h: AERCC - AER Capabilities and Control Register</strong></summary>

<!-- claim:PCIE14-FIG-065-CLAIM figure-table:PCIE14-FIG-065 -->

Figure 65, "Offset AERCAP + 18h: AERCC - AER Capabilities and Control Register": Defines AERCC (AER Capabilities and Control Register) at offset AERCAP + 18h and identifies the fields that software must decode at that location. Start at AERCC, then map bit ranges to access type, reset value, and field meaning. Evidence index: TPLP, MHRE, MHRC, ECE, ECC, EGE, EGC, FEP.

- Purpose: Defines AERCC (AER Capabilities and Control Register) at offset AERCAP + 18h and identifies the fields that software must decode at that location.

- How to read: Start at AERCC, then map bit ranges to access type, reset value, and field meaning. Evidence index: TPLP, MHRE, MHRC, ECE, ECC, EGE, EGC, FEP.

- Conditions and limits: Source keyword index: `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Read AERCC with the required width, then verify TPLP and MHRE separately before using either value. This example adds no requirement.

- Source field index: TPLP, MHRE, MHRC, ECE, ECC, EGE, EGC, FEP

- Source keyword index: `reserved`

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.6.7, Figure 65, printed pages 34, PDF pages 34

</details>

<details markdown="1">
<summary><strong>Figure 66: Offset AERCAP + 1Ch: AERHL - AER Header Log Register</strong></summary>

<!-- claim:PCIE14-FIG-066-CLAIM figure-table:PCIE14-FIG-066 -->

Figure 66, "Offset AERCAP + 1Ch: AERHL - AER Header Log Register": Defines AERHL (AER Header Log Register) at offset AERCAP + 1Ch and identifies the fields that software must decode at that location. Start at AERHL, then map bit ranges to access type, reset value, and field meaning. Evidence index: AERCAP, AERHL, AER, HB3, HB2, HB1, HB0, HB7.

- Purpose: Defines AERHL (AER Header Log Register) at offset AERCAP + 1Ch and identifies the fields that software must decode at that location.

- How to read: Start at AERHL, then map bit ranges to access type, reset value, and field meaning. Evidence index: AERCAP, AERHL, AER, HB3, HB2, HB1, HB0, HB7.

- Conditions and limits: The Figure is explanatory or structural; this guide does not turn its visual relationship into a new requirement.

- Informative example: Read AERHL with the required width, then verify AERCAP and AERHL separately before using either value. This example adds no requirement.

- Source field index: AERCAP, AERHL, AER, HB3, HB2, HB1, HB0, HB7

- Source keyword index: none

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.6.8, Figure 66, printed pages 34, PDF pages 34

</details>

<details markdown="1">
<summary><strong>Figure 67: Offset AERCAP + 38h: AERTLP - AER TLP Prefix Log Register (Optional)</strong></summary>

<!-- claim:PCIE14-FIG-067-CLAIM figure-table:PCIE14-FIG-067 -->

Figure 67, "Offset AERCAP + 38h: AERTLP - AER TLP Prefix Log Register (Optional)": Defines AERTLP (AER TLP Prefix Log Register (Optional)) at offset AERCAP + 38h and identifies the fields that software must decode at that location. Start at AERTLP, then map bit ranges to access type, reset value, and field meaning. Evidence index: AERCAP, AERTLP, AER, TLP, TPL1B3, TPL1B2, TPL1B1, TPL1B0.

- Purpose: Defines AERTLP (AER TLP Prefix Log Register (Optional)) at offset AERCAP + 38h and identifies the fields that software must decode at that location.

- How to read: Start at AERTLP, then map bit ranges to access type, reset value, and field meaning. Evidence index: AERCAP, AERTLP, AER, TLP, TPL1B3, TPL1B2, TPL1B1, TPL1B0.

- Conditions and limits: Source keyword index: `shall`, `may`, `optional`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Read AERTLP with the required width, then verify AERCAP and AERTLP separately before using either value. This example adds no requirement.

- Source field index: AERCAP, AERTLP, AER, TLP, TPL1B3, TPL1B2, TPL1B1, TPL1B0

- Source keyword index: `shall`, `may`, `optional`

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.6.9, Figure 67, printed pages 35, PDF pages 35

</details>

<details markdown="1">
<summary><strong>Figure 68: Example of an Eve Diagram in the Printable Eye Field</strong></summary>

<!-- claim:PCIE14-FIG-068-CLAIM figure-table:PCIE14-FIG-068 -->

Figure 68, "Example of an Eve Diagram in the Printable Eye Field": Defines the concrete layout or value relationships for Example of an Eve Diagram in the Printable Eye Field. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is TEE, VM, OS, TDISP, SR, IOV, SIOV, MI.

- Purpose: Defines the concrete layout or value relationships for Example of an Eve Diagram in the Printable Eye Field.

- How to read: Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is TEE, VM, OS, TDISP, SR, IOV, SIOV, MI.

- Conditions and limits: Source keyword index: `shall`, `may`. The index locates normative language but does not replace the condition attached to each field. The source caption spells "Eve"; the section context identifies a receiver eye. The caption is preserved for traceability.

- Informative example: Use TEE as the first parser checkpoint and VM as a second, independent boundary check. This example adds no requirement.

- Source field index: TEE, VM, OS, TDISP, SR, IOV, SIOV, MI

- Source keyword index: `shall`, `may`

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.9, Figure 68, printed pages 37, PDF pages 37

</details>

<details markdown="1">
<summary><strong>Figure 69: NVMe TDISP DEVICE_INTERFACE_REPORT Reporting Structure</strong></summary>

<!-- claim:PCIE14-FIG-069-CLAIM figure-table:PCIE14-FIG-069 -->

Figure 69, "NVMe TDISP DEVICE_INTERFACE_REPORT Reporting Structure": Defines the concrete layout or value relationships for NVMe TDISP DEVICE_INTERFACE_REPORT Reporting Structure. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is TDISP.

- Purpose: Defines the concrete layout or value relationships for NVMe TDISP DEVICE_INTERFACE_REPORT Reporting Structure.

- How to read: Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is TDISP.

- Conditions and limits: The Figure is explanatory or structural; this guide does not turn its visual relationship into a new requirement.

- Informative example: Use TDISP as the first parser checkpoint and the cited condition as a second, independent boundary check. This example adds no requirement.

- Source field index: TDISP

- Source keyword index: none

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.10, Figure 69, printed pages 38-39, PDF pages 38-39

</details>

<a id="section-3-9"></a>

### §3.9

<details markdown="1">
<summary><strong>Figure 70: Get Log Page - Log Page Identifiers</strong></summary>

<!-- claim:PCIE14-FIG-070-CLAIM figure-table:PCIE14-FIG-070 -->

Figure 70, "Get Log Page - Log Page Identifiers": Defines the identifier composition or namespace of values shown by Get Log Page - Log Page Identifiers. Keep the value width, issuing authority, uniqueness scope, and reserved values separate. Evidence index: CSI1, CSI.

- Purpose: Defines the identifier composition or namespace of values shown by Get Log Page - Log Page Identifiers.

- How to read: Keep the value width, issuing authority, uniqueness scope, and reserved values separate. Evidence index: CSI1, CSI.

- Conditions and limits: The Figure is explanatory or structural; this guide does not turn its visual relationship into a new requirement.

- Informative example: Parse CSI1 at its defined width, then validate the scope associated with CSI before using it as an identity key. This example adds no requirement.

- Source field index: CSI1, CSI

- Source keyword index: none

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.9, Figure 70, printed pages 39, PDF pages 39

</details>

<details markdown="1">
<summary><strong>Figure 71: Size of Physical Interface Receiver Eye Opening Measurement Log Page</strong></summary>

<!-- claim:PCIE14-FIG-071-CLAIM figure-table:PCIE14-FIG-071 -->

Figure 71, "Size of Physical Interface Receiver Eye Opening Measurement Log Page": Shows the receiver-eye measurement information in Size of Physical Interface Receiver Eye Opening Measurement Log Page. Confirm support and returned length before interpreting lane, parameter, header, or descriptor data. Evidence index: Size of Physical Interface Receiver Eye Opening Measurement Log Page.

- Purpose: Shows the receiver-eye measurement information in Size of Physical Interface Receiver Eye Opening Measurement Log Page.

- How to read: Confirm support and returned length before interpreting lane, parameter, header, or descriptor data. Evidence index: Size of Physical Interface Receiver Eye Opening Measurement Log Page.

- Conditions and limits: The Figure is explanatory or structural; this guide does not turn its visual relationship into a new requirement.

- Informative example: Check that Size of Physical Interface Receiver Eye Opening Measurement Log Page is present, then parse the cited condition only when the returned structure is long enough. This example adds no requirement.

- Source field index: Size of Physical Interface Receiver Eye Opening Measurement Log Page

- Source keyword index: none

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.9.1.1, Figure 71, printed pages 40, PDF pages 40

</details>

<details markdown="1">
<summary><strong>Figure 72: Physical Interface Receiver Eye Opening Measurement Log Specific Parameter Field</strong></summary>

<!-- claim:PCIE14-FIG-072-CLAIM figure-table:PCIE14-FIG-072 -->

Figure 72, "Physical Interface Receiver Eye Opening Measurement Log Specific Parameter Field": Defines the concrete layout or value relationships for Physical Interface Receiver Eye Opening Measurement Log Specific Parameter Field. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is ACT, MQUAL, LPOU, LPOL, EOM, EOMIP.

- Purpose: Defines the concrete layout or value relationships for Physical Interface Receiver Eye Opening Measurement Log Specific Parameter Field.

- How to read: Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is ACT, MQUAL, LPOU, LPOL, EOM, EOMIP.

- Conditions and limits: Source keyword index: `shall`, `may`, `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Use ACT as the first parser checkpoint and MQUAL as a second, independent boundary check. This example adds no requirement.

- Source field index: ACT, MQUAL, LPOU, LPOL, EOM, EOMIP

- Source keyword index: `shall`, `may`, `reserved`

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.9.1.1, Figure 72, printed pages 40-41, PDF pages 40-41

</details>

<details markdown="1">
<summary><strong>Figure 73: Physical Interface Receiver Eye Opening Measurement Log Specific Identifier Field</strong></summary>

<!-- claim:PCIE14-FIG-073-CLAIM figure-table:PCIE14-FIG-073 -->

Figure 73, "Physical Interface Receiver Eye Opening Measurement Log Specific Identifier Field": Defines the concrete layout or value relationships for Physical Interface Receiver Eye Opening Measurement Log Specific Identifier Field. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is TC, ID, EOM.

- Purpose: Defines the concrete layout or value relationships for Physical Interface Receiver Eye Opening Measurement Log Specific Identifier Field.

- How to read: Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is TC, ID, EOM.

- Conditions and limits: Source keyword index: `shall`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Use TC as the first parser checkpoint and ID as a second, independent boundary check. This example adds no requirement.

- Source field index: TC, ID, EOM

- Source keyword index: `shall`

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.9.1.1, Figure 73, printed pages 41, PDF pages 41

</details>

<details markdown="1">
<summary><strong>Figure 74: Physical Interface Receiver Eye Opening Measurement Log Page</strong></summary>

<!-- claim:PCIE14-FIG-074-CLAIM figure-table:PCIE14-FIG-074 -->

Figure 74, "Physical Interface Receiver Eye Opening Measurement Log Page": Shows the receiver-eye measurement information in Physical Interface Receiver Eye Opening Measurement Log Page. Confirm support and returned length before interpreting lane, parameter, header, or descriptor data. Evidence index: Physical Interface Receiver Eye Opening Measurement Log Page.

- Purpose: Shows the receiver-eye measurement information in Physical Interface Receiver Eye Opening Measurement Log Page.

- How to read: Confirm support and returned length before interpreting lane, parameter, header, or descriptor data. Evidence index: Physical Interface Receiver Eye Opening Measurement Log Page.

- Conditions and limits: The Figure is explanatory or structural; this guide does not turn its visual relationship into a new requirement.

- Informative example: Check that Physical Interface Receiver Eye Opening Measurement Log Page is present, then parse the cited condition only when the returned structure is long enough. This example adds no requirement.

- Source field index: Physical Interface Receiver Eye Opening Measurement Log Page

- Source keyword index: none

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.9.1.1, Figure 74, printed pages 41, PDF pages 41

</details>

<details markdown="1">
<summary><strong>Figure 75: EOM Header</strong></summary>

<!-- claim:PCIE14-FIG-075-CLAIM figure-table:PCIE14-FIG-075 -->

Figure 75, "EOM Header": Shows the receiver-eye measurement information in EOM Header. Confirm support and returned length before interpreting lane, parameter, header, or descriptor data. Evidence index: EOM.

- Purpose: Shows the receiver-eye measurement information in EOM Header.

- How to read: Confirm support and returned length before interpreting lane, parameter, header, or descriptor data. Evidence index: EOM.

- Conditions and limits: The Figure is explanatory or structural; this guide does not turn its visual relationship into a new requirement.

- Informative example: Check that EOM is present, then parse the cited condition only when the returned structure is long enough. This example adds no requirement.

- Source field index: EOM

- Source keyword index: none

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.9.1.1, Figure 75, printed pages 42-43, PDF pages 42-43

</details>

<details markdown="1">
<summary><strong>Figure 76: EOM Lane Descriptor</strong></summary>

<!-- claim:PCIE14-FIG-076-CLAIM figure-table:PCIE14-FIG-076 -->

Figure 76, "EOM Lane Descriptor": Defines the concrete layout or value relationships for EOM Lane Descriptor. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is MSTAT, MSCS, LN, EYE, TOP, BTM, LFT, RGT.

- Purpose: Defines the concrete layout or value relationships for EOM Lane Descriptor.

- How to read: Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is MSTAT, MSCS, LN, EYE, TOP, BTM, LFT, RGT.

- Conditions and limits: Source keyword index: `shall`, `may`, `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Use MSTAT as the first parser checkpoint and MSCS as a second, independent boundary check. This example adds no requirement.

- Source field index: MSTAT, MSCS, LN, EYE, TOP, BTM, LFT, RGT

- Source keyword index: `shall`, `may`, `reserved`

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.9.1.1, Figure 76, printed pages 43-45, PDF pages 43-45

</details>

<details markdown="1">
<summary><strong>Figure 77: Example of an Eve Diagram in the Printable Eye Field</strong></summary>

<!-- claim:PCIE14-FIG-077-CLAIM figure-table:PCIE14-FIG-077 -->

Figure 77, "Example of an Eve Diagram in the Printable Eye Field": Defines the concrete layout or value relationships for Example of an Eve Diagram in the Printable Eye Field. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is Example of an Eve Diagram in the Printable Eye Field.

- Purpose: Defines the concrete layout or value relationships for Example of an Eve Diagram in the Printable Eye Field.

- How to read: Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is Example of an Eve Diagram in the Printable Eye Field.

- Conditions and limits: The Figure is explanatory or structural; this guide does not turn its visual relationship into a new requirement. The source caption spells "Eve"; the section context identifies a receiver eye. The caption is preserved for traceability.

- Informative example: Use Example of an Eve Diagram in the Printable Eye Field as the first parser checkpoint and the cited condition as a second, independent boundary check. This example adds no requirement.

- Source field index: Example of an Eve Diagram in the Printable Eye Field

- Source keyword index: none

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.9.1.1, Figure 77, printed pages 46, PDF pages 46

</details>

## Use and limitations

Use the claim IDs as stable PPT traceability keys. Re-check affected claims if the source revision, errata set, or approved scope changes.
