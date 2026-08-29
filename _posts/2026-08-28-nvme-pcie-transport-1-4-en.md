---
layout: post
read_time: true
show_date: true
title: "NVMe over PCIe Transport 1.4: Complete Transport Binding"
date: 2026-08-28
description: "Source-located PCIe/NVMe report for PPT authoring."
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

### 1. PCIE14-SCOPE

<!-- claim:PCIE14-SCOPE -->

The PCIe Transport supplements the Base Specification with PCIe-specific structures, extensions, requirements, and behavior; common NVMe behavior remains in Base. In a conflict, Base has higher precedence than a Transport Specification.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §1.2, printed pages 6, PDF pages 6

### 2. PCIE14-CONVENTION

<!-- claim:PCIE14-CONVENTION -->

This document inherits Base conventions. In register or property tables, the Reset column instead denotes the post-reset field value defined by the applicable PCI or PCIe specification.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §1.3, printed pages 6-7, PDF pages 6-7

### 3. PCIE14-KEYWORDS

<!-- claim:PCIE14-KEYWORDS -->

The force of shall, may, and should remains defined by Base 2.4; a Transport summary must not strengthen or weaken the normative language.

> Source: NVME-BASE-2.4, Rev. 2.4, §1.4.1, printed pages 2-3, PDF pages 28-29

### 4. PCIE14-OVERVIEW

<!-- claim:PCIE14-OVERVIEW -->

The PCIe transport uses memory-mapped I/O for data and register access, along with PCIe configuration space and message-signaled interrupts.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §2, printed pages 8, PDF pages 8

### 5. PCIE14-MMIO

<!-- claim:PCIE14-MMIO -->

NVMe controller registers reside in memory space identified by BAR0/BAR1. The host shall use native-width or aligned 32-bit accesses and shall not issue locked accesses; violation produces undefined behavior.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.1, printed pages 9-10, PDF pages 9-10

### 6. PCIE14-DOORBELL

<!-- claim:PCIE14-DOORBELL -->

SQ-tail and CQ-head doorbells begin at offset 1000h, with stride determined by CAP.DSTRD; queue identifier y participates in the offset calculation.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.1.2.1-3.1.2.2, printed pages 10-11, PDF pages 10-11

### 7. PCIE14-QUEUE

<!-- claim:PCIE14-QUEUE -->

PCIe permits multiple Submission Queues to share a Completion Queue. If interrupts are enabled when creating the CQ, Interrupt Vector shall be initialized to the corresponding MSI-X or multiple-message MSI vector.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.2, printed pages 11, PDF pages 11

### 8. PCIE14-RESET

<!-- claim:PCIE14-RESET -->

PCIe reset sources include Base controller/reset flows and PCIe-level resets. Recovery logic uses the reset type to determine controller-property, queue, and PCI-configuration state.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.3, printed pages 11-12, PDF pages 11-12

### 9. PCIE14-COMMAND

<!-- claim:PCIE14-COMMAND -->

The command flow writes an SQE, updates the SQ-tail doorbell, lets the controller fetch and execute, posts a CQE, optionally interrupts, processes the CQE, and updates the CQ-head doorbell. A doorbell conveys a pointer, not the command body.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.4, printed pages 12-13, PDF pages 12-13

### 10. PCIE14-INTERRUPT

<!-- claim:PCIE14-INTERRUPT -->

Modes are pin-based, single-message MSI, multiple-message MSI, and MSI-X. The specification recommends MSI-X. Coalescing can reduce interrupt rate at the cost of latency, and Admin-CQ interrupts should not be delayed.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.5, printed pages 13-16, PDF pages 13-16

### 11. PCIE14-POWER

<!-- claim:PCIE14-POWER -->

The host shall never select an NVMe power state whose consumption exceeds the PCIe slot power limit; violation results in undefined power behavior.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.6, printed pages 16, PDF pages 16

### 12. PCIE14-ERROR

<!-- claim:PCIE14-ERROR -->

NVMe command errors are reported in CQE status, while PCIe transport or link errors use PCIe mechanisms plus this document’s NVMe-specific requirements. Their recovery scopes differ.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.7, printed pages 16, PDF pages 16

### 13. PCIE14-CONFIG

<!-- claim:PCIE14-CONFIG -->

Section 3.8 defines additional NVMe-controller requirements for the PCI header, Power Management, MSI/MSI-X, PCIe capability, and AER. Original PCI/PCIe field semantics remain governed by PCI-SIG specifications.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1-3.8.7, printed pages 16-35, PDF pages 16-35

### 14. PCIE14-SECURITY

<!-- claim:PCIE14-SECURITY -->

Power-loss signaling, confidential computing, and TDISP map platform events or isolation state to NVMe-controller behavior. Implementation still requires external PCIe/TDISP specifications not supplied for this report.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.8-3.8.10, printed pages 35-39, PDF pages 35-39

### 15. PCIE14-EOM

<!-- claim:PCIE14-EOM -->

The Physical Interface Receiver Eye Opening Measurement log page reports measurements through a header, lane descriptors, and EOM data. The host checks support and size before parsing lanes and parameters.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.9, printed pages 39-46, PDF pages 39-46

### 16. PCIE14-HOST

<!-- claim:PCIE14-HOST -->

Annex A is an informative host checklist: write the SQE before its doorbell, use phase to identify a new CQE, advance CQ head after consumption, and service every relevant CQ associated with an interrupt vector.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §Annex A, printed pages 47-48, PDF pages 47-48

## Figure-by-Figure Guide

The source uses Figure numbers for both diagrams and field-layout tables. No source artwork is reproduced.

### Figure 1: NVMe Family of Specifications

<!-- claim:PCIE14-FIG-001-CLAIM figure-table:PCIE14-FIG-001 -->

Figure 1, "NVMe Family of Specifications": Provides a structured index to a concept, support condition, or example. Identify the named object, then read adjacent conditions, legend, and exceptions. This report explains only the PCIe/memory-based portion.

- Purpose: Provides a structured index to a concept, support condition, or example.

- How to read: Identify the named object, then read adjacent conditions, legend, and exceptions.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Choose a concrete controller configuration and map it to the relationships shown. This example adds no requirement.

- Scope: only the PCIe/memory-based portion is introduced.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §1.2, Figure 1, printed pages 6, PDF pages 6

### Figure 2: Example of Transport Protocol Layers

<!-- claim:PCIE14-FIG-002-CLAIM figure-table:PCIE14-FIG-002 -->

Figure 2, "Example of Transport Protocol Layers": Provides a structured index to a concept, support condition, or example. Identify the named object, then read adjacent conditions, legend, and exceptions.

- Purpose: Provides a structured index to a concept, support condition, or example.

- How to read: Identify the named object, then read adjacent conditions, legend, and exceptions.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Choose a concrete controller configuration and map it to the relationships shown. This example adds no requirement.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §2, Figure 2, printed pages 8, PDF pages 8

### Figure 3: PCI Express Registers

<!-- claim:PCIE14-FIG-003-CLAIM figure-table:PCIE14-FIG-003 -->

Figure 3, "PCI Express Registers": Organizes a field, bit, or register layout. Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Purpose: Organizes a field, bit, or register layout.

- How to read: Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Check capability support first, then decode using the specified width and mask. This example adds no requirement.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.1, Figure 3, printed pages 9, PDF pages 9

### Figure 4: PCI Express Specific Controller Property Definitions

<!-- claim:PCIE14-FIG-004-CLAIM figure-table:PCIE14-FIG-004 -->

Figure 4, "PCI Express Specific Controller Property Definitions": Provides a structured index to a concept, support condition, or example. Identify the named object, then read adjacent conditions, legend, and exceptions.

- Purpose: Provides a structured index to a concept, support condition, or example.

- How to read: Identify the named object, then read adjacent conditions, legend, and exceptions.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Choose a concrete controller configuration and map it to the relationships shown. This example adds no requirement.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.1, Figure 4, printed pages 9-10, PDF pages 9-10

### Figure 5: Offset (1000h + ((2y) * (4 << CAP.DSTRD))): SQyTDBL - Submission Queue y Tail

<!-- claim:PCIE14-FIG-005-CLAIM figure-table:PCIE14-FIG-005 -->

Figure 5, "Offset (1000h + ((2y) * (4 << CAP.DSTRD))): SQyTDBL - Submission Queue y Tail": Organizes a queue or command relationship or processing sequence. Follow host, SQ, controller, CQ, and pointer or phase direction.

- Purpose: Organizes a queue or command relationship or processing sequence.

- How to read: Follow host, SQ, controller, CQ, and pointer or phase direction.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Choose one queue identifier and trace one command and its completion. This example adds no requirement.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.1.2.1, Figure 5, printed pages 10, PDF pages 10

### Figure 6: Offset (1000h + ((2y + 1) * (4 << CAP.DSTRD))): CQyHDBL - Completion Queue y Head

<!-- claim:PCIE14-FIG-006-CLAIM figure-table:PCIE14-FIG-006 -->

Figure 6, "Offset (1000h + ((2y + 1) * (4 << CAP.DSTRD))): CQyHDBL - Completion Queue y Head": Organizes a queue or command relationship or processing sequence. Follow host, SQ, controller, CQ, and pointer or phase direction.

- Purpose: Organizes a queue or command relationship or processing sequence.

- How to read: Follow host, SQ, controller, CQ, and pointer or phase direction.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Choose one queue identifier and trace one command and its completion. This example adds no requirement.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.1.2.1, Figure 6, printed pages 10-11, PDF pages 10-11

### Figure 7: Create I/O Completion Queue - Command Dword 11

<!-- claim:PCIE14-FIG-007-CLAIM figure-table:PCIE14-FIG-007 -->

Figure 7, "Create I/O Completion Queue - Command Dword 11": Organizes a queue or command relationship or processing sequence. Follow host, SQ, controller, CQ, and pointer or phase direction.

- Purpose: Organizes a queue or command relationship or processing sequence.

- How to read: Follow host, SQ, controller, CQ, and pointer or phase direction.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Choose one queue identifier and trace one command and its completion. This example adds no requirement.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.2, Figure 7, printed pages 11, PDF pages 11

### Figure 8: Command Processing

<!-- claim:PCIE14-FIG-008-CLAIM figure-table:PCIE14-FIG-008 -->

Figure 8, "Command Processing": Organizes a queue or command relationship or processing sequence. Follow host, SQ, controller, CQ, and pointer or phase direction.

- Purpose: Organizes a queue or command relationship or processing sequence.

- How to read: Follow host, SQ, controller, CQ, and pointer or phase direction.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Choose one queue identifier and trace one command and its completion. This example adds no requirement.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.4.1, Figure 8, printed pages 13, PDF pages 13

### Figure 9: Pin Based, Single MSI, and Multiple MSI Behavior

<!-- claim:PCIE14-FIG-009-CLAIM figure-table:PCIE14-FIG-009 -->

Figure 9, "Pin Based, Single MSI, and Multiple MSI Behavior": Shows interrupt capability, vector, or notification behavior. Separate capability presence, enable state, vector mapping, and pending or mask state.

- Purpose: Shows interrupt capability, vector, or notification behavior.

- How to read: Separate capability presence, enable state, vector mapping, and pending or mask state.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Assign vectors to two Completion Queues and check sharing and service behavior. This example adds no requirement.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.5.1, Figure 9, printed pages 15, PDF pages 15

### Figure 10: PCI Express Type 0/1 Common Configuration Space

<!-- claim:PCIE14-FIG-010-CLAIM figure-table:PCIE14-FIG-010 -->

Figure 10, "PCI Express Type 0/1 Common Configuration Space": Provides a structured index to a concept, support condition, or example. Identify the named object, then read adjacent conditions, legend, and exceptions.

- Purpose: Provides a structured index to a concept, support condition, or example.

- How to read: Identify the named object, then read adjacent conditions, legend, and exceptions.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Choose a concrete controller configuration and map it to the relationships shown. This example adds no requirement.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8, Figure 10, printed pages 16-17, PDF pages 16-17

### Figure 11: Offset 00h: ID - Identifiers

<!-- claim:PCIE14-FIG-011-CLAIM figure-table:PCIE14-FIG-011 -->

Figure 11, "Offset 00h: ID - Identifiers": Organizes a field, bit, or register layout. Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Purpose: Organizes a field, bit, or register layout.

- How to read: Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Check capability support first, then decode using the specified width and mask. This example adds no requirement.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.1, Figure 11, printed pages 17, PDF pages 17

### Figure 12: Offset 04h: CMD - Command

<!-- claim:PCIE14-FIG-012-CLAIM figure-table:PCIE14-FIG-012 -->

Figure 12, "Offset 04h: CMD - Command": Organizes a field, bit, or register layout. Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Purpose: Organizes a field, bit, or register layout.

- How to read: Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Check capability support first, then decode using the specified width and mask. This example adds no requirement.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.2, Figure 12, printed pages 17, PDF pages 17

### Figure 13: Offset 06h: STS - Device Status

<!-- claim:PCIE14-FIG-013-CLAIM figure-table:PCIE14-FIG-013 -->

Figure 13, "Offset 06h: STS - Device Status": Organizes status or error fields and their classification. Read the type and control bits before decoding a code within that type; do not assign meaning to reserved values.

- Purpose: Organizes status or error fields and their classification.

- How to read: Read the type and control bits before decoding a code within that type; do not assign meaning to reserved values.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: For a failed CQE, decode SCT first, then SC and DNR. This example adds no requirement.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.3, Figure 13, printed pages 18, PDF pages 18

### Figure 14: Offset 08h: RID - Revision ID

<!-- claim:PCIE14-FIG-014-CLAIM figure-table:PCIE14-FIG-014 -->

Figure 14, "Offset 08h: RID - Revision ID": Organizes a field, bit, or register layout. Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Purpose: Organizes a field, bit, or register layout.

- How to read: Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Check capability support first, then decode using the specified width and mask. This example adds no requirement.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.4, Figure 14, printed pages 18, PDF pages 18

### Figure 15: Offset 09h: CC - Class Code

<!-- claim:PCIE14-FIG-015-CLAIM figure-table:PCIE14-FIG-015 -->

Figure 15, "Offset 09h: CC - Class Code": Organizes a field, bit, or register layout. Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Purpose: Organizes a field, bit, or register layout.

- How to read: Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Check capability support first, then decode using the specified width and mask. This example adds no requirement.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.5, Figure 15, printed pages 18, PDF pages 18

### Figure 16: Offset 0Ch: CLS - Cache Line Size

<!-- claim:PCIE14-FIG-016-CLAIM figure-table:PCIE14-FIG-016 -->

Figure 16, "Offset 0Ch: CLS - Cache Line Size": Organizes a field, bit, or register layout. Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Purpose: Organizes a field, bit, or register layout.

- How to read: Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Check capability support first, then decode using the specified width and mask. This example adds no requirement.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.6, Figure 16, printed pages 18, PDF pages 18

### Figure 17: Offset 0Dh: MLT - Master Latency Timer

<!-- claim:PCIE14-FIG-017-CLAIM figure-table:PCIE14-FIG-017 -->

Figure 17, "Offset 0Dh: MLT - Master Latency Timer": Organizes a field, bit, or register layout. Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Purpose: Organizes a field, bit, or register layout.

- How to read: Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Check capability support first, then decode using the specified width and mask. This example adds no requirement.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.7, Figure 17, printed pages 18, PDF pages 18

### Figure 18: Offset 0Eh: HTYPE - Header Type

<!-- claim:PCIE14-FIG-018-CLAIM figure-table:PCIE14-FIG-018 -->

Figure 18, "Offset 0Eh: HTYPE - Header Type": Organizes a field, bit, or register layout. Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Purpose: Organizes a field, bit, or register layout.

- How to read: Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Check capability support first, then decode using the specified width and mask. This example adds no requirement.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.8, Figure 18, printed pages 19, PDF pages 19

### Figure 19: Offset 0Fh: BIST - Built-In Self Test (Optional)

<!-- claim:PCIE14-FIG-019-CLAIM figure-table:PCIE14-FIG-019 -->

Figure 19, "Offset 0Fh: BIST - Built-In Self Test (Optional)": Organizes a field, bit, or register layout. Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Purpose: Organizes a field, bit, or register layout.

- How to read: Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Check capability support first, then decode using the specified width and mask. This example adds no requirement.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.9, Figure 19, printed pages 19, PDF pages 19

### Figure 20: Offset 10h: MLBAR (BAR0) - Memory Register Base Address, lower 32-bits

<!-- claim:PCIE14-FIG-020-CLAIM figure-table:PCIE14-FIG-020 -->

Figure 20, "Offset 10h: MLBAR (BAR0) - Memory Register Base Address, lower 32-bits": Organizes a field, bit, or register layout. Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Purpose: Organizes a field, bit, or register layout.

- How to read: Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Check capability support first, then decode using the specified width and mask. This example adds no requirement.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.10, Figure 20, printed pages 19, PDF pages 19

### Figure 21: Offset 14h: MUBAR (BAR1) - Memory Register Base Address, upper 32-bits

<!-- claim:PCIE14-FIG-021-CLAIM figure-table:PCIE14-FIG-021 -->

Figure 21, "Offset 14h: MUBAR (BAR1) - Memory Register Base Address, upper 32-bits": Organizes a field, bit, or register layout. Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Purpose: Organizes a field, bit, or register layout.

- How to read: Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Check capability support first, then decode using the specified width and mask. This example adds no requirement.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.11, Figure 21, printed pages 19, PDF pages 19

### Figure 22: Offset 18h: BAR2 - Index/Data Pair Register Base Address or Vendor Specific

<!-- claim:PCIE14-FIG-022-CLAIM figure-table:PCIE14-FIG-022 -->

Figure 22, "Offset 18h: BAR2 - Index/Data Pair Register Base Address or Vendor Specific": Organizes a field, bit, or register layout. Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Purpose: Organizes a field, bit, or register layout.

- How to read: Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Check capability support first, then decode using the specified width and mask. This example adds no requirement.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.12, Figure 22, printed pages 20, PDF pages 20

### Figure 23: Offset 28h: CCPTR - CardBus CIS Pointer

<!-- claim:PCIE14-FIG-023-CLAIM figure-table:PCIE14-FIG-023 -->

Figure 23, "Offset 28h: CCPTR - CardBus CIS Pointer": Organizes a field, bit, or register layout. Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Purpose: Organizes a field, bit, or register layout.

- How to read: Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Check capability support first, then decode using the specified width and mask. This example adds no requirement.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.16, Figure 23, printed pages 20, PDF pages 20

### Figure 24: Offset 2Ch: SS - Subsystem Identifiers

<!-- claim:PCIE14-FIG-024-CLAIM figure-table:PCIE14-FIG-024 -->

Figure 24, "Offset 2Ch: SS - Subsystem Identifiers": Organizes a field, bit, or register layout. Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Purpose: Organizes a field, bit, or register layout.

- How to read: Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Check capability support first, then decode using the specified width and mask. This example adds no requirement.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.17, Figure 24, printed pages 20, PDF pages 20

### Figure 25: Offset 30h: EROM - Expansion ROM (Optional)

<!-- claim:PCIE14-FIG-025-CLAIM figure-table:PCIE14-FIG-025 -->

Figure 25, "Offset 30h: EROM - Expansion ROM (Optional)": Organizes a field, bit, or register layout. Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Purpose: Organizes a field, bit, or register layout.

- How to read: Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Check capability support first, then decode using the specified width and mask. This example adds no requirement.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.18, Figure 25, printed pages 20, PDF pages 20

### Figure 26: Offset 34h: CAP - Capabilities Pointer

<!-- claim:PCIE14-FIG-026-CLAIM figure-table:PCIE14-FIG-026 -->

Figure 26, "Offset 34h: CAP - Capabilities Pointer": Organizes a field, bit, or register layout. Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Purpose: Organizes a field, bit, or register layout.

- How to read: Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Check capability support first, then decode using the specified width and mask. This example adds no requirement.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.19, Figure 26, printed pages 21, PDF pages 21

### Figure 27: Offset 3Ch: INTR - Interrupt Information

<!-- claim:PCIE14-FIG-027-CLAIM figure-table:PCIE14-FIG-027 -->

Figure 27, "Offset 3Ch: INTR - Interrupt Information": Organizes a field, bit, or register layout. Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Purpose: Organizes a field, bit, or register layout.

- How to read: Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Check capability support first, then decode using the specified width and mask. This example adds no requirement.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.20, Figure 27, printed pages 21, PDF pages 21

### Figure 28: Offset 3Eh: MGNT - Minimum Grant

<!-- claim:PCIE14-FIG-028-CLAIM figure-table:PCIE14-FIG-028 -->

Figure 28, "Offset 3Eh: MGNT - Minimum Grant": Organizes a field, bit, or register layout. Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Purpose: Organizes a field, bit, or register layout.

- How to read: Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Check capability support first, then decode using the specified width and mask. This example adds no requirement.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.21, Figure 28, printed pages 21, PDF pages 21

### Figure 29: Offset 3Fh: MLAT - Maximum Latency

<!-- claim:PCIE14-FIG-029-CLAIM figure-table:PCIE14-FIG-029 -->

Figure 29, "Offset 3Fh: MLAT - Maximum Latency": Organizes a field, bit, or register layout. Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Purpose: Organizes a field, bit, or register layout.

- How to read: Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Check capability support first, then decode using the specified width and mask. This example adds no requirement.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.22, Figure 29, printed pages 21, PDF pages 21

### Figure 30: PCI Power Management Capabilities

<!-- claim:PCIE14-FIG-030-CLAIM figure-table:PCIE14-FIG-030 -->

Figure 30, "PCI Power Management Capabilities": Organizes a field, bit, or register layout. Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Purpose: Organizes a field, bit, or register layout.

- How to read: Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Check capability support first, then decode using the specified width and mask. This example adds no requirement.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.22, Figure 30, printed pages 21, PDF pages 21

### Figure 31: Offset PMCAP: PID - PCI Power Management Capability ID

<!-- claim:PCIE14-FIG-031-CLAIM figure-table:PCIE14-FIG-031 -->

Figure 31, "Offset PMCAP: PID - PCI Power Management Capability ID": Organizes a field, bit, or register layout. Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Purpose: Organizes a field, bit, or register layout.

- How to read: Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Check capability support first, then decode using the specified width and mask. This example adds no requirement.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.2.1, Figure 31, printed pages 21, PDF pages 21

### Figure 32: Offset PMCAP + 2h: PC - PCI Power Management Capabilities

<!-- claim:PCIE14-FIG-032-CLAIM figure-table:PCIE14-FIG-032 -->

Figure 32, "Offset PMCAP + 2h: PC - PCI Power Management Capabilities": Organizes a field, bit, or register layout. Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Purpose: Organizes a field, bit, or register layout.

- How to read: Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Check capability support first, then decode using the specified width and mask. This example adds no requirement.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.2.2, Figure 32, printed pages 22, PDF pages 22

### Figure 33: Offset PMCAP + 4h: PMCS - PCI Power Management Control and Status

<!-- claim:PCIE14-FIG-033-CLAIM figure-table:PCIE14-FIG-033 -->

Figure 33, "Offset PMCAP + 4h: PMCS - PCI Power Management Control and Status": Organizes status or error fields and their classification. Read the type and control bits before decoding a code within that type; do not assign meaning to reserved values.

- Purpose: Organizes status or error fields and their classification.

- How to read: Read the type and control bits before decoding a code within that type; do not assign meaning to reserved values.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: For a failed CQE, decode SCT first, then SC and DNR. This example adds no requirement.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.2.3, Figure 33, printed pages 22, PDF pages 22

### Figure 34: Message Signaled Interrupt Capability (Optional)

<!-- claim:PCIE14-FIG-034-CLAIM figure-table:PCIE14-FIG-034 -->

Figure 34, "Message Signaled Interrupt Capability (Optional)": Organizes a field, bit, or register layout. Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Purpose: Organizes a field, bit, or register layout.

- How to read: Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Check capability support first, then decode using the specified width and mask. This example adds no requirement.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.2.3, Figure 34, printed pages 22, PDF pages 22

### Figure 35: Offset MSICAP: MID - Message Signaled Interrupt Identifiers

<!-- claim:PCIE14-FIG-035-CLAIM figure-table:PCIE14-FIG-035 -->

Figure 35, "Offset MSICAP: MID - Message Signaled Interrupt Identifiers": Organizes a field, bit, or register layout. Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Purpose: Organizes a field, bit, or register layout.

- How to read: Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Check capability support first, then decode using the specified width and mask. This example adds no requirement.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.3.1, Figure 35, printed pages 23, PDF pages 23

### Figure 36: Offset MSICAP + 2h: MC - Message Signaled Interrupt Message Control

<!-- claim:PCIE14-FIG-036-CLAIM figure-table:PCIE14-FIG-036 -->

Figure 36, "Offset MSICAP + 2h: MC - Message Signaled Interrupt Message Control": Organizes a field, bit, or register layout. Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Purpose: Organizes a field, bit, or register layout.

- How to read: Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Check capability support first, then decode using the specified width and mask. This example adds no requirement.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.3.2, Figure 36, printed pages 23, PDF pages 23

### Figure 37: Offset MSICAP + 4h: MA - Message Signaled Interrupt Message Address

<!-- claim:PCIE14-FIG-037-CLAIM figure-table:PCIE14-FIG-037 -->

Figure 37, "Offset MSICAP + 4h: MA - Message Signaled Interrupt Message Address": Organizes a field, bit, or register layout. Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Purpose: Organizes a field, bit, or register layout.

- How to read: Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Check capability support first, then decode using the specified width and mask. This example adds no requirement.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.3.3, Figure 37, printed pages 23, PDF pages 23

### Figure 38: Offset MSICAP + 8h: MUA - Message Signaled Interrupt Upper Address

<!-- claim:PCIE14-FIG-038-CLAIM figure-table:PCIE14-FIG-038 -->

Figure 38, "Offset MSICAP + 8h: MUA - Message Signaled Interrupt Upper Address": Organizes a field, bit, or register layout. Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Purpose: Organizes a field, bit, or register layout.

- How to read: Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Check capability support first, then decode using the specified width and mask. This example adds no requirement.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.3.4, Figure 38, printed pages 23, PDF pages 23

### Figure 39: Offset MSICAP + Ch: MD - Message Signaled Interrupt Message Data

<!-- claim:PCIE14-FIG-039-CLAIM figure-table:PCIE14-FIG-039 -->

Figure 39, "Offset MSICAP + Ch: MD - Message Signaled Interrupt Message Data": Organizes a field, bit, or register layout. Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Purpose: Organizes a field, bit, or register layout.

- How to read: Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Check capability support first, then decode using the specified width and mask. This example adds no requirement.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.3.5, Figure 39, printed pages 23, PDF pages 23

### Figure 40: Offset MSICAP + 10h: MMASK - Message Signaled Interrupt Mask Bits (Optional)

<!-- claim:PCIE14-FIG-040-CLAIM figure-table:PCIE14-FIG-040 -->

Figure 40, "Offset MSICAP + 10h: MMASK - Message Signaled Interrupt Mask Bits (Optional)": Organizes a field, bit, or register layout. Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Purpose: Organizes a field, bit, or register layout.

- How to read: Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Check capability support first, then decode using the specified width and mask. This example adds no requirement.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.3.6, Figure 40, printed pages 24, PDF pages 24

### Figure 41: Offset MSICAP + 14h: MPEND - Message Signaled Interrupt Pending Bits (Optional)

<!-- claim:PCIE14-FIG-041-CLAIM figure-table:PCIE14-FIG-041 -->

Figure 41, "Offset MSICAP + 14h: MPEND - Message Signaled Interrupt Pending Bits (Optional)": Organizes a field, bit, or register layout. Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Purpose: Organizes a field, bit, or register layout.

- How to read: Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Check capability support first, then decode using the specified width and mask. This example adds no requirement.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.3.7, Figure 41, printed pages 24, PDF pages 24

### Figure 42: MSI-X Capability (Optional)

<!-- claim:PCIE14-FIG-042-CLAIM figure-table:PCIE14-FIG-042 -->

Figure 42, "MSI-X Capability (Optional)": Organizes a field, bit, or register layout. Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Purpose: Organizes a field, bit, or register layout.

- How to read: Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Check capability support first, then decode using the specified width and mask. This example adds no requirement.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.3.7, Figure 42, printed pages 24, PDF pages 24

### Figure 43: Offset MSIXCAP: MXID - MSI-X Identifiers

<!-- claim:PCIE14-FIG-043-CLAIM figure-table:PCIE14-FIG-043 -->

Figure 43, "Offset MSIXCAP: MXID - MSI-X Identifiers": Organizes a field, bit, or register layout. Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Purpose: Organizes a field, bit, or register layout.

- How to read: Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Check capability support first, then decode using the specified width and mask. This example adds no requirement.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.4.1, Figure 43, printed pages 24, PDF pages 24

### Figure 44: Offset MSIXCAP + 2h: MXC - MSI-X Message Control

<!-- claim:PCIE14-FIG-044-CLAIM figure-table:PCIE14-FIG-044 -->

Figure 44, "Offset MSIXCAP + 2h: MXC - MSI-X Message Control": Organizes a field, bit, or register layout. Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Purpose: Organizes a field, bit, or register layout.

- How to read: Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Check capability support first, then decode using the specified width and mask. This example adds no requirement.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.4.2, Figure 44, printed pages 24-25, PDF pages 24-25

### Figure 45: Offset MSIXCAP + 4h: MTAB - MSI-X Table Offset / Table BIR

<!-- claim:PCIE14-FIG-045-CLAIM figure-table:PCIE14-FIG-045 -->

Figure 45, "Offset MSIXCAP + 4h: MTAB - MSI-X Table Offset / Table BIR": Organizes a field, bit, or register layout. Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Purpose: Organizes a field, bit, or register layout.

- How to read: Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Check capability support first, then decode using the specified width and mask. This example adds no requirement.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.4.3, Figure 45, printed pages 25, PDF pages 25

### Figure 46: Offset MSIXCAP + 8h: MPBA - MSI-X PBA Offset / PBA BIR

<!-- claim:PCIE14-FIG-046-CLAIM figure-table:PCIE14-FIG-046 -->

Figure 46, "Offset MSIXCAP + 8h: MPBA - MSI-X PBA Offset / PBA BIR": Organizes a field, bit, or register layout. Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Purpose: Organizes a field, bit, or register layout.

- How to read: Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Check capability support first, then decode using the specified width and mask. This example adds no requirement.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.4.4, Figure 46, printed pages 25, PDF pages 25

### Figure 47: PCI Express Capability

<!-- claim:PCIE14-FIG-047-CLAIM figure-table:PCIE14-FIG-047 -->

Figure 47, "PCI Express Capability": Organizes a field, bit, or register layout. Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Purpose: Organizes a field, bit, or register layout.

- How to read: Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Check capability support first, then decode using the specified width and mask. This example adds no requirement.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.5, Figure 47, printed pages 26, PDF pages 26

### Figure 48: Offset PXCAP: PXID - PCI Express Capability ID

<!-- claim:PCIE14-FIG-048-CLAIM figure-table:PCIE14-FIG-048 -->

Figure 48, "Offset PXCAP: PXID - PCI Express Capability ID": Organizes a field, bit, or register layout. Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Purpose: Organizes a field, bit, or register layout.

- How to read: Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Check capability support first, then decode using the specified width and mask. This example adds no requirement.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.5.1, Figure 48, printed pages 26, PDF pages 26

### Figure 49: Offset PXCAP + 2h: PXCAP - PCI Express Capabilities

<!-- claim:PCIE14-FIG-049-CLAIM figure-table:PCIE14-FIG-049 -->

Figure 49, "Offset PXCAP + 2h: PXCAP - PCI Express Capabilities": Organizes a field, bit, or register layout. Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Purpose: Organizes a field, bit, or register layout.

- How to read: Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Check capability support first, then decode using the specified width and mask. This example adds no requirement.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.5.2, Figure 49, printed pages 26, PDF pages 26

### Figure 50: Offset PXCAP + 4h: PXDCAP - PCI Express Device Capabilities

<!-- claim:PCIE14-FIG-050-CLAIM figure-table:PCIE14-FIG-050 -->

Figure 50, "Offset PXCAP + 4h: PXDCAP - PCI Express Device Capabilities": Organizes a field, bit, or register layout. Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Purpose: Organizes a field, bit, or register layout.

- How to read: Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Check capability support first, then decode using the specified width and mask. This example adds no requirement.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.5.3, Figure 50, printed pages 26-27, PDF pages 26-27

### Figure 51: Offset PXCAP + 8h: PXDC - PCI Express Device Control

<!-- claim:PCIE14-FIG-051-CLAIM figure-table:PCIE14-FIG-051 -->

Figure 51, "Offset PXCAP + 8h: PXDC - PCI Express Device Control": Organizes a field, bit, or register layout. Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Purpose: Organizes a field, bit, or register layout.

- How to read: Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Check capability support first, then decode using the specified width and mask. This example adds no requirement.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.5.4, Figure 51, printed pages 27-28, PDF pages 27-28

### Figure 52: Offset PXCAP + Ah: PXDS - PCI Express Device Status

<!-- claim:PCIE14-FIG-052-CLAIM figure-table:PCIE14-FIG-052 -->

Figure 52, "Offset PXCAP + Ah: PXDS - PCI Express Device Status": Organizes status or error fields and their classification. Read the type and control bits before decoding a code within that type; do not assign meaning to reserved values.

- Purpose: Organizes status or error fields and their classification.

- How to read: Read the type and control bits before decoding a code within that type; do not assign meaning to reserved values.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: For a failed CQE, decode SCT first, then SC and DNR. This example adds no requirement.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.5.5, Figure 52, printed pages 28, PDF pages 28

### Figure 53: Offset PXCAP + Ch: PXLCAP - PCI Express Link Capabilities

<!-- claim:PCIE14-FIG-053-CLAIM figure-table:PCIE14-FIG-053 -->

Figure 53, "Offset PXCAP + Ch: PXLCAP - PCI Express Link Capabilities": Organizes a field, bit, or register layout. Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Purpose: Organizes a field, bit, or register layout.

- How to read: Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Check capability support first, then decode using the specified width and mask. This example adds no requirement.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.5.6, Figure 53, printed pages 28-29, PDF pages 28-29

### Figure 54: Offset PXCAP + 10h: PXLC - PCI Express Link Control

<!-- claim:PCIE14-FIG-054-CLAIM figure-table:PCIE14-FIG-054 -->

Figure 54, "Offset PXCAP + 10h: PXLC - PCI Express Link Control": Organizes a field, bit, or register layout. Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Purpose: Organizes a field, bit, or register layout.

- How to read: Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Check capability support first, then decode using the specified width and mask. This example adds no requirement.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.5.7, Figure 54, printed pages 29, PDF pages 29

### Figure 55: Offset PXCAP + 12h: PXLS - PCI Express Link Status

<!-- claim:PCIE14-FIG-055-CLAIM figure-table:PCIE14-FIG-055 -->

Figure 55, "Offset PXCAP + 12h: PXLS - PCI Express Link Status": Organizes status or error fields and their classification. Read the type and control bits before decoding a code within that type; do not assign meaning to reserved values.

- Purpose: Organizes status or error fields and their classification.

- How to read: Read the type and control bits before decoding a code within that type; do not assign meaning to reserved values.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: For a failed CQE, decode SCT first, then SC and DNR. This example adds no requirement.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.5.8, Figure 55, printed pages 29, PDF pages 29

### Figure 56: Offset PXCAP + 24h: PXDCAP2 - PCI Express Device Capabilities 2

<!-- claim:PCIE14-FIG-056-CLAIM figure-table:PCIE14-FIG-056 -->

Figure 56, "Offset PXCAP + 24h: PXDCAP2 - PCI Express Device Capabilities 2": Organizes a field, bit, or register layout. Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Purpose: Organizes a field, bit, or register layout.

- How to read: Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Check capability support first, then decode using the specified width and mask. This example adds no requirement.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.5.9, Figure 56, printed pages 30, PDF pages 30

### Figure 57: Offset PXCAP + 28h: PXDC2 - PCI Express Device Control 2

<!-- claim:PCIE14-FIG-057-CLAIM figure-table:PCIE14-FIG-057 -->

Figure 57, "Offset PXCAP + 28h: PXDC2 - PCI Express Device Control 2": Organizes a field, bit, or register layout. Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Purpose: Organizes a field, bit, or register layout.

- How to read: Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Check capability support first, then decode using the specified width and mask. This example adds no requirement.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.5.10, Figure 57, printed pages 30-31, PDF pages 30-31

### Figure 58: Advanced Error Reporting Capability (Optional)

<!-- claim:PCIE14-FIG-058-CLAIM figure-table:PCIE14-FIG-058 -->

Figure 58, "Advanced Error Reporting Capability (Optional)": Organizes status or error fields and their classification. Read the type and control bits before decoding a code within that type; do not assign meaning to reserved values.

- Purpose: Organizes status or error fields and their classification.

- How to read: Read the type and control bits before decoding a code within that type; do not assign meaning to reserved values.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: For a failed CQE, decode SCT first, then SC and DNR. This example adds no requirement.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.5.10, Figure 58, printed pages 31, PDF pages 31

### Figure 59: Offset AERCAP: AERID - AER Capability ID

<!-- claim:PCIE14-FIG-059-CLAIM figure-table:PCIE14-FIG-059 -->

Figure 59, "Offset AERCAP: AERID - AER Capability ID": Organizes a field, bit, or register layout. Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Purpose: Organizes a field, bit, or register layout.

- How to read: Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Check capability support first, then decode using the specified width and mask. This example adds no requirement.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.6.1, Figure 59, printed pages 31, PDF pages 31

### Figure 60: Offset AERCAP + 4: AERUCES - AER Uncorrectable Error Status Register

<!-- claim:PCIE14-FIG-060-CLAIM figure-table:PCIE14-FIG-060 -->

Figure 60, "Offset AERCAP + 4: AERUCES - AER Uncorrectable Error Status Register": Organizes status or error fields and their classification. Read the type and control bits before decoding a code within that type; do not assign meaning to reserved values.

- Purpose: Organizes status or error fields and their classification.

- How to read: Read the type and control bits before decoding a code within that type; do not assign meaning to reserved values.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: For a failed CQE, decode SCT first, then SC and DNR. This example adds no requirement.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.6.2, Figure 60, printed pages 31-32, PDF pages 31-32

### Figure 61: Offset AERCAP + 8: AERUCEM - AER Uncorrectable Error Mask Register

<!-- claim:PCIE14-FIG-061-CLAIM figure-table:PCIE14-FIG-061 -->

Figure 61, "Offset AERCAP + 8: AERUCEM - AER Uncorrectable Error Mask Register": Organizes status or error fields and their classification. Read the type and control bits before decoding a code within that type; do not assign meaning to reserved values.

- Purpose: Organizes status or error fields and their classification.

- How to read: Read the type and control bits before decoding a code within that type; do not assign meaning to reserved values.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: For a failed CQE, decode SCT first, then SC and DNR. This example adds no requirement.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.6.3, Figure 61, printed pages 32, PDF pages 32

### Figure 62: Offset AERCAP + Ch: AERUCESEV - AER Uncorrectable Error Severity Register

<!-- claim:PCIE14-FIG-062-CLAIM figure-table:PCIE14-FIG-062 -->

Figure 62, "Offset AERCAP + Ch: AERUCESEV - AER Uncorrectable Error Severity Register": Organizes status or error fields and their classification. Read the type and control bits before decoding a code within that type; do not assign meaning to reserved values.

- Purpose: Organizes status or error fields and their classification.

- How to read: Read the type and control bits before decoding a code within that type; do not assign meaning to reserved values.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: For a failed CQE, decode SCT first, then SC and DNR. This example adds no requirement.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.6.4, Figure 62, printed pages 32-33, PDF pages 32-33

### Figure 63: Offset AERCAP + 10h: AERCES - AER Correctable Error Status Register

<!-- claim:PCIE14-FIG-063-CLAIM figure-table:PCIE14-FIG-063 -->

Figure 63, "Offset AERCAP + 10h: AERCES - AER Correctable Error Status Register": Organizes status or error fields and their classification. Read the type and control bits before decoding a code within that type; do not assign meaning to reserved values.

- Purpose: Organizes status or error fields and their classification.

- How to read: Read the type and control bits before decoding a code within that type; do not assign meaning to reserved values.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: For a failed CQE, decode SCT first, then SC and DNR. This example adds no requirement.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.6.5, Figure 63, printed pages 33, PDF pages 33

### Figure 64: Offset AERCAP + 14h: AERCEM - AER Correctable Error Mask Register

<!-- claim:PCIE14-FIG-064-CLAIM figure-table:PCIE14-FIG-064 -->

Figure 64, "Offset AERCAP + 14h: AERCEM - AER Correctable Error Mask Register": Organizes status or error fields and their classification. Read the type and control bits before decoding a code within that type; do not assign meaning to reserved values.

- Purpose: Organizes status or error fields and their classification.

- How to read: Read the type and control bits before decoding a code within that type; do not assign meaning to reserved values.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: For a failed CQE, decode SCT first, then SC and DNR. This example adds no requirement.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.6.6, Figure 64, printed pages 33, PDF pages 33

### Figure 65: Offset AERCAP + 18h: AERCC - AER Capabilities and Control Register

<!-- claim:PCIE14-FIG-065-CLAIM figure-table:PCIE14-FIG-065 -->

Figure 65, "Offset AERCAP + 18h: AERCC - AER Capabilities and Control Register": Organizes a field, bit, or register layout. Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Purpose: Organizes a field, bit, or register layout.

- How to read: Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Check capability support first, then decode using the specified width and mask. This example adds no requirement.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.6.7, Figure 65, printed pages 34, PDF pages 34

### Figure 66: Offset AERCAP + 1Ch: AERHL - AER Header Log Register

<!-- claim:PCIE14-FIG-066-CLAIM figure-table:PCIE14-FIG-066 -->

Figure 66, "Offset AERCAP + 1Ch: AERHL - AER Header Log Register": Organizes a field, bit, or register layout. Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Purpose: Organizes a field, bit, or register layout.

- How to read: Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Check capability support first, then decode using the specified width and mask. This example adds no requirement.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.6.8, Figure 66, printed pages 34, PDF pages 34

### Figure 67: Offset AERCAP + 38h: AERTLP - AER TLP Prefix Log Register (Optional)

<!-- claim:PCIE14-FIG-067-CLAIM figure-table:PCIE14-FIG-067 -->

Figure 67, "Offset AERCAP + 38h: AERTLP - AER TLP Prefix Log Register (Optional)": Organizes a field, bit, or register layout. Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Purpose: Organizes a field, bit, or register layout.

- How to read: Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Check capability support first, then decode using the specified width and mask. This example adds no requirement.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.6.9, Figure 67, printed pages 35, PDF pages 35

### Figure 68: Example of an Eve Diagram in the Printable Eye Field

<!-- claim:PCIE14-FIG-068-CLAIM figure-table:PCIE14-FIG-068 -->

Figure 68, "Example of an Eve Diagram in the Printable Eye Field": Organizes a field, bit, or register layout. Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Purpose: Organizes a field, bit, or register layout.

- How to read: Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Check capability support first, then decode using the specified width and mask. This example adds no requirement.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.9, Figure 68, printed pages 37, PDF pages 37

### Figure 69: NVMe TDISP DEVICE_INTERFACE_REPORT Reporting Structure

<!-- claim:PCIE14-FIG-069-CLAIM figure-table:PCIE14-FIG-069 -->

Figure 69, "NVMe TDISP DEVICE_INTERFACE_REPORT Reporting Structure": Provides a structured index to a concept, support condition, or example. Identify the named object, then read adjacent conditions, legend, and exceptions.

- Purpose: Provides a structured index to a concept, support condition, or example.

- How to read: Identify the named object, then read adjacent conditions, legend, and exceptions.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Choose a concrete controller configuration and map it to the relationships shown. This example adds no requirement.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.10, Figure 69, printed pages 38-39, PDF pages 38-39

### Figure 70: Get Log Page - Log Page Identifiers

<!-- claim:PCIE14-FIG-070-CLAIM figure-table:PCIE14-FIG-070 -->

Figure 70, "Get Log Page - Log Page Identifiers": Organizes identifier or list byte layout and scope. Check length, byte order, count, uniqueness scope, and reserved area.

- Purpose: Organizes identifier or list byte layout and scope.

- How to read: Check length, byte order, count, uniqueness scope, and reserved area.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: A parser validates count and length before reading identifiers. This example adds no requirement.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.9, Figure 70, printed pages 39, PDF pages 39

### Figure 71: Size of Physical Interface Receiver Eye Opening Measurement Log Page

<!-- claim:PCIE14-FIG-071-CLAIM figure-table:PCIE14-FIG-071 -->

Figure 71, "Size of Physical Interface Receiver Eye Opening Measurement Log Page": Organizes receiver-eye measurement inputs, outputs, or data format. Check support and size before decoding lanes, parameters, headers, and descriptors.

- Purpose: Organizes receiver-eye measurement inputs, outputs, or data format.

- How to read: Check support and size before decoding lanes, parameters, headers, and descriptors.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Read the returned length first and parse only complete lane descriptors. This example adds no requirement.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.9.1.1, Figure 71, printed pages 40, PDF pages 40

### Figure 72: Physical Interface Receiver Eye Opening Measurement Log Specific Parameter Field

<!-- claim:PCIE14-FIG-072-CLAIM figure-table:PCIE14-FIG-072 -->

Figure 72, "Physical Interface Receiver Eye Opening Measurement Log Specific Parameter Field": Organizes a field, bit, or register layout. Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Purpose: Organizes a field, bit, or register layout.

- How to read: Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Check capability support first, then decode using the specified width and mask. This example adds no requirement.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.9.1.1, Figure 72, printed pages 40-41, PDF pages 40-41

### Figure 73: Physical Interface Receiver Eye Opening Measurement Log Specific Identifier Field

<!-- claim:PCIE14-FIG-073-CLAIM figure-table:PCIE14-FIG-073 -->

Figure 73, "Physical Interface Receiver Eye Opening Measurement Log Specific Identifier Field": Organizes a field, bit, or register layout. Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Purpose: Organizes a field, bit, or register layout.

- How to read: Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Check capability support first, then decode using the specified width and mask. This example adds no requirement.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.9.1.1, Figure 73, printed pages 41, PDF pages 41

### Figure 74: Physical Interface Receiver Eye Opening Measurement Log Page

<!-- claim:PCIE14-FIG-074-CLAIM figure-table:PCIE14-FIG-074 -->

Figure 74, "Physical Interface Receiver Eye Opening Measurement Log Page": Organizes receiver-eye measurement inputs, outputs, or data format. Check support and size before decoding lanes, parameters, headers, and descriptors.

- Purpose: Organizes receiver-eye measurement inputs, outputs, or data format.

- How to read: Check support and size before decoding lanes, parameters, headers, and descriptors.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Read the returned length first and parse only complete lane descriptors. This example adds no requirement.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.9.1.1, Figure 74, printed pages 41, PDF pages 41

### Figure 75: EOM Header

<!-- claim:PCIE14-FIG-075-CLAIM figure-table:PCIE14-FIG-075 -->

Figure 75, "EOM Header": Organizes receiver-eye measurement inputs, outputs, or data format. Check support and size before decoding lanes, parameters, headers, and descriptors.

- Purpose: Organizes receiver-eye measurement inputs, outputs, or data format.

- How to read: Check support and size before decoding lanes, parameters, headers, and descriptors.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Read the returned length first and parse only complete lane descriptors. This example adds no requirement.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.9.1.1, Figure 75, printed pages 42-43, PDF pages 42-43

### Figure 76: EOM Lane Descriptor

<!-- claim:PCIE14-FIG-076-CLAIM figure-table:PCIE14-FIG-076 -->

Figure 76, "EOM Lane Descriptor": Shows how PRP or SGL structures describe a data buffer. Check address, offset, length, alignment, and next-level pointers in order.

- Purpose: Shows how PRP or SGL structures describe a data buffer.

- How to read: Check address, offset, length, alignment, and next-level pointers in order.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Use a buffer crossing two memory pages to check the first offset and later alignment. This example adds no requirement.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.9.1.1, Figure 76, printed pages 43-45, PDF pages 43-45

### Figure 77: Example of an Eve Diagram in the Printable Eye Field

<!-- claim:PCIE14-FIG-077-CLAIM figure-table:PCIE14-FIG-077 -->

Figure 77, "Example of an Eve Diagram in the Printable Eye Field": Organizes a field, bit, or register layout. Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Purpose: Organizes a field, bit, or register layout.

- How to read: Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Check capability support first, then decode using the specified width and mask. This example adds no requirement.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.9.1.1, Figure 77, printed pages 46, PDF pages 46

## Use and limitations

Use the claim IDs as stable PPT traceability keys. Re-check affected claims if the source revision, errata set, or approved scope changes.
