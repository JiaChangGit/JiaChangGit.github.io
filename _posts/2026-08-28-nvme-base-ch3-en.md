---
layout: post
read_time: true
show_date: true
title: "NVMe Base 2.4 Chapter 3: Controllers, Queues, Initialization, and Resets"
date: 2026-08-28
description: "Source-located PCIe/NVMe report for PPT authoring."
tags: [NVMe, PCIe, Specification]
category: NVMe
author: Jia-Chang
github: JiaChangGit/JiaChangGit.github.io/tree/main/DOCS/nvme-spec-report
toc: yes
---

# NVMe Base 2.4 Chapter 3: Controllers, Queues, Initialization, and Resets

Purpose: a source-located engineering report for GitHub Pages and a 100-minute presentation.

Scope: §3; printed pages 38–138; PDF pages 64–164. Only PCIe/memory-based and common NVMe content appears below.

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

### 1. BASE3-STATIC

<!-- claim:BASE3-STATIC -->

A memory-based controller shall support only the static controller model.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.1, printed pages 38, PDF pages 64

### 2. BASE3-TYPES

<!-- claim:BASE3-TYPES -->

This report uses the I/O and Administrative controller roles. The former performs user-data I/O; the latter is management-oriented and does not support data I/O commands. Both have one Admin Submission/Completion Queue pair.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.3-3.1.3.2, printed pages 39-43, PDF pages 65-69

### 3. BASE3-ORDER

<!-- claim:BASE3-ORDER -->

Except for fused operations, fetched commands and completions have no general ordering guarantee. Enforcing any required order is the host's responsibility.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.3, printed pages 40, PDF pages 66

### 4. BASE3-PROPERTY

<!-- claim:BASE3-PROPERTY -->

The host shall access a property at its starting offset using the specified width; the PCIe Transport adds the access rules for a memory-based controller.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4, printed pages 52-54, PDF pages 78-80

### 5. BASE3-NAMESPACE

<!-- claim:BASE3-NAMESPACE -->

NSID 0h is invalid and FFFFFFFFh is the broadcast value. Other NSIDs still need allocated/unallocated and active/inactive classification; numeric range alone is insufficient.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.2.1, printed pages 78-80, PDF pages 104-106

### 6. BASE3-MEDIA

<!-- claim:BASE3-MEDIA -->

NVM Sets, Endurance Groups, Reclaim Groups, and Reclaim Units describe capacity grouping, endurance management, and reclamation granularity. Support and identifiers are determined from Identify data and log-page capabilities.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.2.2-3.2.4, printed pages 80-85, PDF pages 106-111

### 7. BASE3-DOMAIN

<!-- claim:BASE3-DOMAIN -->

A domain is a failure or communication boundary inside an NVM subsystem. In a multi-domain subsystem, each domain identifier shall be unique within that subsystem.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.2.5, printed pages 85-88, PDF pages 111-114

### 8. BASE3-QUEUE

<!-- claim:BASE3-QUEUE -->

A PCIe queue is a circular buffer in host-addressable memory with head and tail pointers. The host creates an I/O Completion Queue before its Submission Queue and advances pointers through doorbells.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.3.1, printed pages 88-91, PDF pages 114-117

### 9. BASE3-PROCESS

<!-- claim:BASE3-PROCESS -->

Command processing separates ordering, fused and atomic semantics, arbitration, and outstanding-command limits. Priority belongs to a Submission Queue, not to each command as an independent attribute.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.4.1-3.4.5, printed pages 101-105, PDF pages 127-131

### 10. BASE3-INIT

<!-- claim:BASE3-INIT -->

PCIe initialization reads CAP, configures AQA/ASQ/ACQ and CC, then waits for CSTS.RDY. Ready mode and CRTO affect host wait and error handling.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.5.1, 3.5.3-3.5.4, printed pages 105-113, PDF pages 131-139

### 11. BASE3-SHUTDOWN

<!-- claim:BASE3-SHUTDOWN -->

Normal shutdown begins when the host sets CC.SHN and the controller reports progress in CSTS.SHST. NVM subsystem shutdown has a wider scope and is not the same as one controller shutdown.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.6.1, 3.6.3, printed pages 113-120, PDF pages 139-146

### 12. BASE3-RESET

<!-- claim:BASE3-RESET -->

NVM Subsystem, Controller Level, and Queue Level resets have different scopes. A recovery flow first determines which state is cleared and whether queues still exist.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.7, printed pages 120-125, PDF pages 146-151

### 13. BASE3-CAPACITY

<!-- claim:BASE3-CAPACITY -->

The capacity model tracks available or configured capacity separately at subsystem, Endurance Group, NVM Set, and namespace levels. Values from different levels are not directly interchangeable.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.8, printed pages 125-129, PDF pages 151-155

### 14. BASE3-KEEPALIVE

<!-- claim:BASE3-KEEPALIVE -->

Keep Alive uses KATO and KATT for host/controller liveness monitoring. This report retains only controller-common and PCIe-applicable timer, command, and timeout behavior.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.9, printed pages 129-135, PDF pages 155-161

### 15. BASE3-FIRMWARE

<!-- claim:BASE3-FIRMWARE -->

A privileged action may affect other hosts or controllers. Firmware update separates image download, commit/activation, and any required reset; the host sequences the flow using the reported activation action.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.10-3.11, printed pages 135-138, PDF pages 161-164

## Figure-by-Figure Guide

The source uses Figure numbers for both diagrams and field-layout tables. No source artwork is reproduced.

### Figure 23: Controller Types

<!-- claim:BASE3-FIG-023-CLAIM figure-table:BASE3-FIG-023 -->

Figure 23, “Controller Types”: Provides a structured index to a concept, support condition, or example. Identify the named object, then read adjacent conditions, legend, and exceptions. This report explains only the PCIe/memory-based portion.

- Purpose: Provides a structured index to a concept, support condition, or example.

- How to read: Identify the named object, then read adjacent conditions, legend, and exceptions.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Choose a concrete controller configuration and map it to the relationships shown. This example adds no requirement.

- Scope: only the PCIe/memory-based portion is introduced.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.3, Figure 23, printed pages 39, PDF pages 65

### Figure 24: NVM Subsystem with Three I/O Controllers

<!-- claim:BASE3-FIG-024-CLAIM figure-table:BASE3-FIG-024 -->

Figure 24, “NVM Subsystem with Three I/O Controllers”: Shows containment, connection, or capacity relationships among subsystem objects. Keep controllers, ports, namespaces, identifiers, and capacity levels distinct.

- Purpose: Shows containment, connection, or capacity relationships among subsystem objects.

- How to read: Keep controllers, ports, namespaces, identifiers, and capacity levels distinct.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: For one namespace, mark its NSID, controller, and capacity hierarchy. This example adds no requirement.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.3.1, Figure 24, printed pages 41, PDF pages 67

### Figure 25: NVM Subsystem with One Administrative and Two I/O Controllers

<!-- claim:BASE3-FIG-025-CLAIM figure-table:BASE3-FIG-025 -->

Figure 25, “NVM Subsystem with One Administrative and Two I/O Controllers”: Shows containment, connection, or capacity relationships among subsystem objects. Keep controllers, ports, namespaces, identifiers, and capacity levels distinct.

- Purpose: Shows containment, connection, or capacity relationships among subsystem objects.

- How to read: Keep controllers, ports, namespaces, identifiers, and capacity levels distinct.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: For one namespace, mark its NSID, controller, and capacity hierarchy. This example adds no requirement.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.3.2, Figure 25, printed pages 42, PDF pages 68

### Figure 26: NVM Subsystem with One Administrative Controller

<!-- claim:BASE3-FIG-026-CLAIM figure-table:BASE3-FIG-026 -->

Figure 26, “NVM Subsystem with One Administrative Controller”: Shows containment, connection, or capacity relationships among subsystem objects. Keep controllers, ports, namespaces, identifiers, and capacity levels distinct.

- Purpose: Shows containment, connection, or capacity relationships among subsystem objects.

- How to read: Keep controllers, ports, namespaces, identifiers, and capacity levels distinct.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: For one namespace, mark its NSID, controller, and capacity hierarchy. This example adds no requirement.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.3.2, Figure 26, printed pages 42, PDF pages 68

### Figure 27: Controller IDs FFF0h to FFFFh

<!-- claim:BASE3-FIG-027-CLAIM figure-table:BASE3-FIG-027 -->

Figure 27, “Controller IDs FFF0h to FFFFh”: Provides a structured index to a concept, support condition, or example. Identify the named object, then read adjacent conditions, legend, and exceptions.

- Purpose: Provides a structured index to a concept, support condition, or example.

- How to read: Identify the named object, then read adjacent conditions, legend, and exceptions.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Choose a concrete controller configuration and map it to the relationships shown. This example adds no requirement.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.3.3, Figure 27, printed pages 44, PDF pages 70

### Figure 28: Admin Command Support Requirements

<!-- claim:BASE3-FIG-028-CLAIM figure-table:BASE3-FIG-028 -->

Figure 28, “Admin Command Support Requirements”: Provides a structured index to a concept, support condition, or example. Identify the named object, then read adjacent conditions, legend, and exceptions. This report explains only the PCIe/memory-based portion.

- Purpose: Provides a structured index to a concept, support condition, or example.

- How to read: Identify the named object, then read adjacent conditions, legend, and exceptions.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Choose a concrete controller configuration and map it to the relationships shown. This example adds no requirement.

- Scope: only the PCIe/memory-based portion is introduced.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.3.3.3, Figure 28, printed pages 45-47, PDF pages 71-73

### Figure 30: Common I/O Command Support Requirements

<!-- claim:BASE3-FIG-030-CLAIM figure-table:BASE3-FIG-030 -->

Figure 30, “Common I/O Command Support Requirements”: Provides a structured index to a concept, support condition, or example. Identify the named object, then read adjacent conditions, legend, and exceptions. This report explains only the PCIe/memory-based portion.

- Purpose: Provides a structured index to a concept, support condition, or example.

- How to read: Identify the named object, then read adjacent conditions, legend, and exceptions.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Choose a concrete controller configuration and map it to the relationships shown. This example adds no requirement.

- Scope: only the PCIe/memory-based portion is introduced.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.3.4, Figure 30, printed pages 47-48, PDF pages 73-74

### Figure 31: Log Page Support Requirements

<!-- claim:BASE3-FIG-031-CLAIM figure-table:BASE3-FIG-031 -->

Figure 31, “Log Page Support Requirements”: Provides a structured index to a concept, support condition, or example. Identify the named object, then read adjacent conditions, legend, and exceptions. This report explains only the PCIe/memory-based portion.

- Purpose: Provides a structured index to a concept, support condition, or example.

- How to read: Identify the named object, then read adjacent conditions, legend, and exceptions.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Choose a concrete controller configuration and map it to the relationships shown. This example adds no requirement.

- Scope: only the PCIe/memory-based portion is introduced.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.3.4, Figure 31, printed pages 48-50, PDF pages 74-76

### Figure 32: Feature Support Requirements

<!-- claim:BASE3-FIG-032-CLAIM figure-table:BASE3-FIG-032 -->

Figure 32, “Feature Support Requirements”: Provides a structured index to a concept, support condition, or example. Identify the named object, then read adjacent conditions, legend, and exceptions. This report explains only the PCIe/memory-based portion.

- Purpose: Provides a structured index to a concept, support condition, or example.

- How to read: Identify the named object, then read adjacent conditions, legend, and exceptions.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Choose a concrete controller configuration and map it to the relationships shown. This example adds no requirement.

- Scope: only the PCIe/memory-based portion is introduced.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.3.5, Figure 32, printed pages 50-52, PDF pages 76-78

### Figure 33: Property Definition

<!-- claim:BASE3-FIG-033-CLAIM figure-table:BASE3-FIG-033 -->

Figure 33, “Property Definition”: Provides a structured index to a concept, support condition, or example. Identify the named object, then read adjacent conditions, legend, and exceptions. This report explains only the PCIe/memory-based portion.

- Purpose: Provides a structured index to a concept, support condition, or example.

- How to read: Identify the named object, then read adjacent conditions, legend, and exceptions.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Choose a concrete controller configuration and map it to the relationships shown. This example adds no requirement.

- Scope: only the PCIe/memory-based portion is introduced.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4, Figure 33, printed pages 52-53, PDF pages 78-79

### Figure 34: Memory-Based Property Definition

<!-- claim:BASE3-FIG-034-CLAIM figure-table:BASE3-FIG-034 -->

Figure 34, “Memory-Based Property Definition”: Provides a structured index to a concept, support condition, or example. Identify the named object, then read adjacent conditions, legend, and exceptions.

- Purpose: Provides a structured index to a concept, support condition, or example.

- How to read: Identify the named object, then read adjacent conditions, legend, and exceptions.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Choose a concrete controller configuration and map it to the relationships shown. This example adds no requirement.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4, Figure 34, printed pages 54, PDF pages 80

### Figure 36: Offset 0h: CAP – Controller Capabilities

<!-- claim:BASE3-FIG-036-CLAIM figure-table:BASE3-FIG-036 -->

Figure 36, “Offset 0h: CAP – Controller Capabilities”: Organizes a field, bit, or register layout. Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Purpose: Organizes a field, bit, or register layout.

- How to read: Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Check capability support first, then decode using the specified width and mask. This example adds no requirement.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.1, Figure 36, printed pages 55-58, PDF pages 81-84

### Figure 37: Specification Version Descriptor

<!-- claim:BASE3-FIG-037-CLAIM figure-table:BASE3-FIG-037 -->

Figure 37, “Specification Version Descriptor”: Shows how PRP or SGL structures describe a data buffer. Check address, offset, length, alignment, and next-level pointers in order.

- Purpose: Shows how PRP or SGL structures describe a data buffer.

- How to read: Check address, offset, length, alignment, and next-level pointers in order.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Use a buffer crossing two memory pages to check the first offset and later alignment. This example adds no requirement.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.1, Figure 37, printed pages 58, PDF pages 84

### Figure 38: NVM Express Base Specification Version Property Reset Values

<!-- claim:BASE3-FIG-038-CLAIM figure-table:BASE3-FIG-038 -->

Figure 38, “NVM Express Base Specification Version Property Reset Values”: Provides a structured index to a concept, support condition, or example. Identify the named object, then read adjacent conditions, legend, and exceptions.

- Purpose: Provides a structured index to a concept, support condition, or example.

- How to read: Identify the named object, then read adjacent conditions, legend, and exceptions.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Choose a concrete controller configuration and map it to the relationships shown. This example adds no requirement.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.1, Figure 38, printed pages 58-59, PDF pages 84-85

### Figure 39: Offset Ch: INTMS – Interrupt Mask Set

<!-- claim:BASE3-FIG-039-CLAIM figure-table:BASE3-FIG-039 -->

Figure 39, “Offset Ch: INTMS – Interrupt Mask Set”: Organizes a field, bit, or register layout. Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Purpose: Organizes a field, bit, or register layout.

- How to read: Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Check capability support first, then decode using the specified width and mask. This example adds no requirement.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.2, Figure 39, printed pages 59, PDF pages 85

### Figure 40: Offset 10h: INTMC – Interrupt Mask Clear

<!-- claim:BASE3-FIG-040-CLAIM figure-table:BASE3-FIG-040 -->

Figure 40, “Offset 10h: INTMC – Interrupt Mask Clear”: Organizes a field, bit, or register layout. Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Purpose: Organizes a field, bit, or register layout.

- How to read: Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Check capability support first, then decode using the specified width and mask. This example adds no requirement.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.2, Figure 40, printed pages 59, PDF pages 85

### Figure 41: Offset 14h: CC – Controller Configuration

<!-- claim:BASE3-FIG-041-CLAIM figure-table:BASE3-FIG-041 -->

Figure 41, “Offset 14h: CC – Controller Configuration”: Organizes a field, bit, or register layout. Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Purpose: Organizes a field, bit, or register layout.

- How to read: Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Check capability support first, then decode using the specified width and mask. This example adds no requirement.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.5, Figure 41, printed pages 60-63, PDF pages 86-89

### Figure 42: Offset 1Ch: CSTS – Controller Status

<!-- claim:BASE3-FIG-042-CLAIM figure-table:BASE3-FIG-042 -->

Figure 42, “Offset 1Ch: CSTS – Controller Status”: Organizes status or error fields and their classification. Read the type and control bits before decoding a code within that type; do not assign meaning to reserved values.

- Purpose: Organizes status or error fields and their classification.

- How to read: Read the type and control bits before decoding a code within that type; do not assign meaning to reserved values.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: For a failed CQE, decode SCT first, then SC and DNR. This example adds no requirement.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.5, Figure 42, printed pages 63-65, PDF pages 89-91

### Figure 43: Offset 20h: NSSR – NVM Subsystem Reset

<!-- claim:BASE3-FIG-043-CLAIM figure-table:BASE3-FIG-043 -->

Figure 43, “Offset 20h: NSSR – NVM Subsystem Reset”: Organizes a field, bit, or register layout. Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Purpose: Organizes a field, bit, or register layout.

- How to read: Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Check capability support first, then decode using the specified width and mask. This example adds no requirement.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.6, Figure 43, printed pages 66, PDF pages 92

### Figure 44: Offset 24h: AQA – Admin Queue Attributes

<!-- claim:BASE3-FIG-044-CLAIM figure-table:BASE3-FIG-044 -->

Figure 44, “Offset 24h: AQA – Admin Queue Attributes”: Organizes a queue or command relationship or processing sequence. Follow host, SQ, controller, CQ, and pointer or phase direction.

- Purpose: Organizes a queue or command relationship or processing sequence.

- How to read: Follow host, SQ, controller, CQ, and pointer or phase direction.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Choose one queue identifier and trace one command and its completion. This example adds no requirement.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.6, Figure 44, printed pages 66, PDF pages 92

### Figure 45: Offset 28h: ASQ – Admin Submission Queue Base Address

<!-- claim:BASE3-FIG-045-CLAIM figure-table:BASE3-FIG-045 -->

Figure 45, “Offset 28h: ASQ – Admin Submission Queue Base Address”: Organizes a queue or command relationship or processing sequence. Follow host, SQ, controller, CQ, and pointer or phase direction.

- Purpose: Organizes a queue or command relationship or processing sequence.

- How to read: Follow host, SQ, controller, CQ, and pointer or phase direction.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Choose one queue identifier and trace one command and its completion. This example adds no requirement.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.6, Figure 45, printed pages 66, PDF pages 92

### Figure 46: Offset 30h: ACQ – Admin Completion Queue Base Address

<!-- claim:BASE3-FIG-046-CLAIM figure-table:BASE3-FIG-046 -->

Figure 46, “Offset 30h: ACQ – Admin Completion Queue Base Address”: Organizes a queue or command relationship or processing sequence. Follow host, SQ, controller, CQ, and pointer or phase direction.

- Purpose: Organizes a queue or command relationship or processing sequence.

- How to read: Follow host, SQ, controller, CQ, and pointer or phase direction.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Choose one queue identifier and trace one command and its completion. This example adds no requirement.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.9, Figure 46, printed pages 67, PDF pages 93

### Figure 47: Offset 38h: CMBLOC – Controller Memory Buffer Location

<!-- claim:BASE3-FIG-047-CLAIM figure-table:BASE3-FIG-047 -->

Figure 47, “Offset 38h: CMBLOC – Controller Memory Buffer Location”: Organizes a field, bit, or register layout. Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Purpose: Organizes a field, bit, or register layout.

- How to read: Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Check capability support first, then decode using the specified width and mask. This example adds no requirement.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.9, Figure 47, printed pages 67-68, PDF pages 93-94

### Figure 48: Offset 3Ch: CMBSZ – Controller Memory Buffer Size

<!-- claim:BASE3-FIG-048-CLAIM figure-table:BASE3-FIG-048 -->

Figure 48, “Offset 3Ch: CMBSZ – Controller Memory Buffer Size”: Organizes a field, bit, or register layout. Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Purpose: Organizes a field, bit, or register layout.

- How to read: Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Check capability support first, then decode using the specified width and mask. This example adds no requirement.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.11, Figure 48, printed pages 68-69, PDF pages 94-95

### Figure 49: Offset 40h: BPINFO – Boot Partition Information

<!-- claim:BASE3-FIG-049-CLAIM figure-table:BASE3-FIG-049 -->

Figure 49, “Offset 40h: BPINFO – Boot Partition Information”: Organizes a field, bit, or register layout. Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Purpose: Organizes a field, bit, or register layout.

- How to read: Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Check capability support first, then decode using the specified width and mask. This example adds no requirement.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.12, Figure 49, printed pages 69, PDF pages 95

### Figure 50: Offset 44h: BPRSEL – Boot Partition Read Select

<!-- claim:BASE3-FIG-050-CLAIM figure-table:BASE3-FIG-050 -->

Figure 50, “Offset 44h: BPRSEL – Boot Partition Read Select”: Organizes a field, bit, or register layout. Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Purpose: Organizes a field, bit, or register layout.

- How to read: Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Check capability support first, then decode using the specified width and mask. This example adds no requirement.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.12, Figure 50, printed pages 69-70, PDF pages 95-96

### Figure 51: Offset 48h: BPMBL – Boot Partition Memory Buffer Location

<!-- claim:BASE3-FIG-051-CLAIM figure-table:BASE3-FIG-051 -->

Figure 51, “Offset 48h: BPMBL – Boot Partition Memory Buffer Location”: Organizes a field, bit, or register layout. Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Purpose: Organizes a field, bit, or register layout.

- How to read: Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Check capability support first, then decode using the specified width and mask. This example adds no requirement.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.14, Figure 51, printed pages 70, PDF pages 96

### Figure 52: Offset 50h: CMBMSC – Controller Memory Buffer Memory Space Control

<!-- claim:BASE3-FIG-052-CLAIM figure-table:BASE3-FIG-052 -->

Figure 52, “Offset 50h: CMBMSC – Controller Memory Buffer Memory Space Control”: Organizes a field, bit, or register layout. Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Purpose: Organizes a field, bit, or register layout.

- How to read: Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Check capability support first, then decode using the specified width and mask. This example adds no requirement.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.14, Figure 52, printed pages 70-71, PDF pages 96-97

### Figure 53: Offset 58h: CMBSTS – Controller Memory Buffer Status

<!-- claim:BASE3-FIG-053-CLAIM figure-table:BASE3-FIG-053 -->

Figure 53, “Offset 58h: CMBSTS – Controller Memory Buffer Status”: Organizes status or error fields and their classification. Read the type and control bits before decoding a code within that type; do not assign meaning to reserved values.

- Purpose: Organizes status or error fields and their classification.

- How to read: Read the type and control bits before decoding a code within that type; do not assign meaning to reserved values.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: For a failed CQE, decode SCT first, then SC and DNR. This example adds no requirement.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.16, Figure 53, printed pages 71, PDF pages 97

### Figure 54: Offset 5Ch: CMBEBS – Controller Memory Buffer Elasticity Buffer Size

<!-- claim:BASE3-FIG-054-CLAIM figure-table:BASE3-FIG-054 -->

Figure 54, “Offset 5Ch: CMBEBS – Controller Memory Buffer Elasticity Buffer Size”: Organizes a field, bit, or register layout. Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Purpose: Organizes a field, bit, or register layout.

- How to read: Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Check capability support first, then decode using the specified width and mask. This example adds no requirement.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.16, Figure 54, printed pages 71, PDF pages 97

### Figure 55: Offset 60h: CMBSWTP – Controller Memory Buffer Sustained Write Throughput

<!-- claim:BASE3-FIG-055-CLAIM figure-table:BASE3-FIG-055 -->

Figure 55, “Offset 60h: CMBSWTP – Controller Memory Buffer Sustained Write Throughput”: Organizes a field, bit, or register layout. Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Purpose: Organizes a field, bit, or register layout.

- How to read: Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Check capability support first, then decode using the specified width and mask. This example adds no requirement.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.19, Figure 55, printed pages 72, PDF pages 98

### Figure 56: Offset 64h: NSSD – NVM Subsystem Shutdown

<!-- claim:BASE3-FIG-056-CLAIM figure-table:BASE3-FIG-056 -->

Figure 56, “Offset 64h: NSSD – NVM Subsystem Shutdown”: Organizes a field, bit, or register layout. Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Purpose: Organizes a field, bit, or register layout.

- How to read: Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Check capability support first, then decode using the specified width and mask. This example adds no requirement.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.19, Figure 56, printed pages 72, PDF pages 98

### Figure 57: Offset 68h: CRTO – Controller Ready Timeouts

<!-- claim:BASE3-FIG-057-CLAIM figure-table:BASE3-FIG-057 -->

Figure 57, “Offset 68h: CRTO – Controller Ready Timeouts”: Organizes a field, bit, or register layout. Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Purpose: Organizes a field, bit, or register layout.

- How to read: Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Check capability support first, then decode using the specified width and mask. This example adds no requirement.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.21, Figure 57, printed pages 73, PDF pages 99

### Figure 58: Offset E00h: PMRCAP – Persistent Memory Region Capabilities

<!-- claim:BASE3-FIG-058-CLAIM figure-table:BASE3-FIG-058 -->

Figure 58, “Offset E00h: PMRCAP – Persistent Memory Region Capabilities”: Organizes a field, bit, or register layout. Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Purpose: Organizes a field, bit, or register layout.

- How to read: Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Check capability support first, then decode using the specified width and mask. This example adds no requirement.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.21, Figure 58, printed pages 73-74, PDF pages 99-100

### Figure 59: Offset E04h: PMRCTL – Persistent Memory Region Control

<!-- claim:BASE3-FIG-059-CLAIM figure-table:BASE3-FIG-059 -->

Figure 59, “Offset E04h: PMRCTL – Persistent Memory Region Control”: Organizes a field, bit, or register layout. Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Purpose: Organizes a field, bit, or register layout.

- How to read: Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Check capability support first, then decode using the specified width and mask. This example adds no requirement.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.22, Figure 59, printed pages 74, PDF pages 100

### Figure 60: Offset E08h: PMRSTS – Persistent Memory Region Status

<!-- claim:BASE3-FIG-060-CLAIM figure-table:BASE3-FIG-060 -->

Figure 60, “Offset E08h: PMRSTS – Persistent Memory Region Status”: Organizes status or error fields and their classification. Read the type and control bits before decoding a code within that type; do not assign meaning to reserved values.

- Purpose: Organizes status or error fields and their classification.

- How to read: Read the type and control bits before decoding a code within that type; do not assign meaning to reserved values.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: For a failed CQE, decode SCT first, then SC and DNR. This example adds no requirement.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.23, Figure 60, printed pages 75, PDF pages 101

### Figure 61: Offset E0Ch: PMREBS – Persistent Memory Region Elasticity Buffer Size

<!-- claim:BASE3-FIG-061-CLAIM figure-table:BASE3-FIG-061 -->

Figure 61, “Offset E0Ch: PMREBS – Persistent Memory Region Elasticity Buffer Size”: Organizes a field, bit, or register layout. Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Purpose: Organizes a field, bit, or register layout.

- How to read: Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Check capability support first, then decode using the specified width and mask. This example adds no requirement.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.24, Figure 61, printed pages 76, PDF pages 102

### Figure 62: Offset E10h: PMRSWTP – Persistent Memory Region Sustained Write Throughput

<!-- claim:BASE3-FIG-062-CLAIM figure-table:BASE3-FIG-062 -->

Figure 62, “Offset E10h: PMRSWTP – Persistent Memory Region Sustained Write Throughput”: Organizes a field, bit, or register layout. Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Purpose: Organizes a field, bit, or register layout.

- How to read: Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Check capability support first, then decode using the specified width and mask. This example adds no requirement.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.24, Figure 62, printed pages 76, PDF pages 102

### Figure 63: Offset E14h: PMRMSCL – Persistent Memory Region Memory Space Control Lower

<!-- claim:BASE3-FIG-063-CLAIM figure-table:BASE3-FIG-063 -->

Figure 63, “Offset E14h: PMRMSCL – Persistent Memory Region Memory Space Control Lower”: Organizes a field, bit, or register layout. Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Purpose: Organizes a field, bit, or register layout.

- How to read: Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Check capability support first, then decode using the specified width and mask. This example adds no requirement.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.26, Figure 63, printed pages 77, PDF pages 103

### Figure 64: Offset E18h: PMRMSCU – Persistent Memory Region Memory Space Control Upper

<!-- claim:BASE3-FIG-064-CLAIM figure-table:BASE3-FIG-064 -->

Figure 64, “Offset E18h: PMRMSCU – Persistent Memory Region Memory Space Control Upper”: Organizes a field, bit, or register layout. Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Purpose: Organizes a field, bit, or register layout.

- How to read: Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Check capability support first, then decode using the specified width and mask. This example adds no requirement.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.26, Figure 64, printed pages 77, PDF pages 103

### Figure 65: NSID Types and Relationship to Namespace

<!-- claim:BASE3-FIG-065-CLAIM figure-table:BASE3-FIG-065 -->

Figure 65, “NSID Types and Relationship to Namespace”: Shows containment, connection, or capacity relationships among subsystem objects. Keep controllers, ports, namespaces, identifiers, and capacity levels distinct.

- Purpose: Shows containment, connection, or capacity relationships among subsystem objects.

- How to read: Keep controllers, ports, namespaces, identifiers, and capacity levels distinct.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: For one namespace, mark its NSID, controller, and capacity hierarchy. This example adds no requirement.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.2.1, Figure 65, printed pages 78-79, PDF pages 104-105

### Figure 66: NSID Types

<!-- claim:BASE3-FIG-066-CLAIM figure-table:BASE3-FIG-066 -->

Figure 66, “NSID Types”: Provides a structured index to a concept, support condition, or example. Identify the named object, then read adjacent conditions, legend, and exceptions.

- Purpose: Provides a structured index to a concept, support condition, or example.

- How to read: Identify the named object, then read adjacent conditions, legend, and exceptions.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Choose a concrete controller configuration and map it to the relationships shown. This example adds no requirement.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.2.1.5, Figure 66, printed pages 79, PDF pages 105

### Figure 67: NVM Sets and Associated Namespaces

<!-- claim:BASE3-FIG-067-CLAIM figure-table:BASE3-FIG-067 -->

Figure 67, “NVM Sets and Associated Namespaces”: Shows containment, connection, or capacity relationships among subsystem objects. Keep controllers, ports, namespaces, identifiers, and capacity levels distinct.

- Purpose: Shows containment, connection, or capacity relationships among subsystem objects.

- How to read: Keep controllers, ports, namespaces, identifiers, and capacity levels distinct.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: For one namespace, mark its NSID, controller, and capacity hierarchy. This example adds no requirement.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.2.2, Figure 67, printed pages 81, PDF pages 107

### Figure 68: NVM Set Aware Admin Commands

<!-- claim:BASE3-FIG-068-CLAIM figure-table:BASE3-FIG-068 -->

Figure 68, “NVM Set Aware Admin Commands”: Shows containment, connection, or capacity relationships among subsystem objects. Keep controllers, ports, namespaces, identifiers, and capacity levels distinct.

- Purpose: Shows containment, connection, or capacity relationships among subsystem objects.

- How to read: Keep controllers, ports, namespaces, identifiers, and capacity levels distinct.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: For one namespace, mark its NSID, controller, and capacity hierarchy. This example adds no requirement.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.2.2, Figure 68, printed pages 81, PDF pages 107

### Figure 69: NVM Sets and Associated Namespaces

<!-- claim:BASE3-FIG-069-CLAIM figure-table:BASE3-FIG-069 -->

Figure 69, “NVM Sets and Associated Namespaces”: Shows containment, connection, or capacity relationships among subsystem objects. Keep controllers, ports, namespaces, identifiers, and capacity levels distinct.

- Purpose: Shows containment, connection, or capacity relationships among subsystem objects.

- How to read: Keep controllers, ports, namespaces, identifiers, and capacity levels distinct.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: For one namespace, mark its NSID, controller, and capacity hierarchy. This example adds no requirement.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.2.3, Figure 69, printed pages 83, PDF pages 109

### Figure 70: Flexible Data Placement Logical View of Non-Volatile Storage

<!-- claim:BASE3-FIG-070-CLAIM figure-table:BASE3-FIG-070 -->

Figure 70, “Flexible Data Placement Logical View of Non-Volatile Storage”: Provides a structured index to a concept, support condition, or example. Identify the named object, then read adjacent conditions, legend, and exceptions.

- Purpose: Provides a structured index to a concept, support condition, or example.

- How to read: Identify the named object, then read adjacent conditions, legend, and exceptions.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Choose a concrete controller configuration and map it to the relationships shown. This example adds no requirement.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.2.4, Figure 70, printed pages 85, PDF pages 111

### Figure 71: Example 1 Domain Structure

<!-- claim:BASE3-FIG-071-CLAIM figure-table:BASE3-FIG-071 -->

Figure 71, “Example 1 Domain Structure”: Shows containment, connection, or capacity relationships among subsystem objects. Keep controllers, ports, namespaces, identifiers, and capacity levels distinct.

- Purpose: Shows containment, connection, or capacity relationships among subsystem objects.

- How to read: Keep controllers, ports, namespaces, identifiers, and capacity levels distinct.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: For one namespace, mark its NSID, controller, and capacity hierarchy. This example adds no requirement.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.2.5.1, Figure 71, printed pages 86, PDF pages 112

### Figure 73: Empty Queue Definition

<!-- claim:BASE3-FIG-073-CLAIM figure-table:BASE3-FIG-073 -->

Figure 73, “Empty Queue Definition”: Organizes a queue or command relationship or processing sequence. Follow host, SQ, controller, CQ, and pointer or phase direction.

- Purpose: Organizes a queue or command relationship or processing sequence.

- How to read: Follow host, SQ, controller, CQ, and pointer or phase direction.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Choose one queue identifier and trace one command and its completion. This example adds no requirement.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.3.1.4, Figure 73, printed pages 91, PDF pages 117

### Figure 74: Full Queue Definition

<!-- claim:BASE3-FIG-074-CLAIM figure-table:BASE3-FIG-074 -->

Figure 74, “Full Queue Definition”: Organizes a queue or command relationship or processing sequence. Follow host, SQ, controller, CQ, and pointer or phase direction.

- Purpose: Organizes a queue or command relationship or processing sequence.

- How to read: Follow host, SQ, controller, CQ, and pointer or phase direction.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Choose one queue identifier and trace one command and its completion. This example adds no requirement.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.3.1.4, Figure 74, printed pages 91, PDF pages 117

### Figure 80: Round Robin Arbitration

<!-- claim:BASE3-FIG-080-CLAIM figure-table:BASE3-FIG-080 -->

Figure 80, “Round Robin Arbitration”: Provides a structured index to a concept, support condition, or example. Identify the named object, then read adjacent conditions, legend, and exceptions.

- Purpose: Provides a structured index to a concept, support condition, or example.

- How to read: Identify the named object, then read adjacent conditions, legend, and exceptions.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Choose a concrete controller configuration and map it to the relationships shown. This example adds no requirement.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.4.4, Figure 80, printed pages 103, PDF pages 129

### Figure 81: Weighted Round Robin with Urgent Priority Class Arbitration

<!-- claim:BASE3-FIG-081-CLAIM figure-table:BASE3-FIG-081 -->

Figure 81, “Weighted Round Robin with Urgent Priority Class Arbitration”: Provides a structured index to a concept, support condition, or example. Identify the named object, then read adjacent conditions, legend, and exceptions.

- Purpose: Provides a structured index to a concept, support condition, or example.

- How to read: Identify the named object, then read adjacent conditions, legend, and exceptions.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Choose a concrete controller configuration and map it to the relationships shown. This example adds no requirement.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.4.4.2, Figure 81, printed pages 104, PDF pages 130

### Figure 84: Admin Commands Permitted to Return a Status Code of Admin Command Media Not

<!-- claim:BASE3-FIG-084-CLAIM figure-table:BASE3-FIG-084 -->

Figure 84, “Admin Commands Permitted to Return a Status Code of Admin Command Media Not”: Organizes status or error fields and their classification. Read the type and control bits before decoding a code within that type; do not assign meaning to reserved values. This report explains only the PCIe/memory-based portion.

- Purpose: Organizes status or error fields and their classification.

- How to read: Read the type and control bits before decoding a code within that type; do not assign meaning to reserved values.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: For a failed CQE, decode SCT first, then SC and DNR. This example adds no requirement.

- Scope: only the PCIe/memory-based portion is introduced.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.5.3, Figure 84, printed pages 110-111, PDF pages 136-137

### Figure 85: Shutdown Processing Interactions

<!-- claim:BASE3-FIG-085-CLAIM figure-table:BASE3-FIG-085 -->

Figure 85, “Shutdown Processing Interactions”: Provides a structured index to a concept, support condition, or example. Identify the named object, then read adjacent conditions, legend, and exceptions. This report explains only the PCIe/memory-based portion.

- Purpose: Provides a structured index to a concept, support condition, or example.

- How to read: Identify the named object, then read adjacent conditions, legend, and exceptions.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Choose a concrete controller configuration and map it to the relationships shown. This example adds no requirement.

- Scope: only the PCIe/memory-based portion is introduced.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.6, Figure 85, printed pages 113, PDF pages 139

### Figure 86: Simple NVM Subsystem

<!-- claim:BASE3-FIG-086-CLAIM figure-table:BASE3-FIG-086 -->

Figure 86, “Simple NVM Subsystem”: Shows containment, connection, or capacity relationships among subsystem objects. Keep controllers, ports, namespaces, identifiers, and capacity levels distinct.

- Purpose: Shows containment, connection, or capacity relationships among subsystem objects.

- How to read: Keep controllers, ports, namespaces, identifiers, and capacity levels distinct.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: For one namespace, mark its NSID, controller, and capacity hierarchy. This example adds no requirement.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.8.2, Figure 86, printed pages 126, PDF pages 152

### Figure 87: Vertically-Organized NVM Subsystem

<!-- claim:BASE3-FIG-087-CLAIM figure-table:BASE3-FIG-087 -->

Figure 87, “Vertically-Organized NVM Subsystem”: Shows containment, connection, or capacity relationships among subsystem objects. Keep controllers, ports, namespaces, identifiers, and capacity levels distinct.

- Purpose: Shows containment, connection, or capacity relationships among subsystem objects.

- How to read: Keep controllers, ports, namespaces, identifiers, and capacity levels distinct.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: For one namespace, mark its NSID, controller, and capacity hierarchy. This example adds no requirement.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.8.2.2, Figure 87, printed pages 127, PDF pages 153

### Figure 88: Horizontally-Organized Dual NAND NVM Subsystem

<!-- claim:BASE3-FIG-088-CLAIM figure-table:BASE3-FIG-088 -->

Figure 88, “Horizontally-Organized Dual NAND NVM Subsystem”: Shows containment, connection, or capacity relationships among subsystem objects. Keep controllers, ports, namespaces, identifiers, and capacity levels distinct.

- Purpose: Shows containment, connection, or capacity relationships among subsystem objects.

- How to read: Keep controllers, ports, namespaces, identifiers, and capacity levels distinct.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: For one namespace, mark its NSID, controller, and capacity hierarchy. This example adds no requirement.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.8.2.3, Figure 88, printed pages 128, PDF pages 154

### Figure 89: Capacity Information Field Usage

<!-- claim:BASE3-FIG-089-CLAIM figure-table:BASE3-FIG-089 -->

Figure 89, “Capacity Information Field Usage”: Organizes a field, bit, or register layout. Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Purpose: Organizes a field, bit, or register layout.

- How to read: Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Check capability support first, then decode using the specified width and mask. This example adds no requirement.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.8.3, Figure 89, printed pages 129, PDF pages 155

### Figure 90: Detecting Timeout Takes up to 2 * KATT

<!-- claim:BASE3-FIG-090-CLAIM figure-table:BASE3-FIG-090 -->

Figure 90, “Detecting Timeout Takes up to 2 * KATT”: Provides a structured index to a concept, support condition, or example. Identify the named object, then read adjacent conditions, legend, and exceptions. This report explains only the PCIe/memory-based portion.

- Purpose: Provides a structured index to a concept, support condition, or example.

- How to read: Identify the named object, then read adjacent conditions, legend, and exceptions.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Choose a concrete controller configuration and map it to the relationships shown. This example adds no requirement.

- Scope: only the PCIe/memory-based portion is introduced.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.9.4.1, Figure 90, printed pages 133, PDF pages 159

### Figure 91: Example Privileged Action Admin Commands

<!-- claim:BASE3-FIG-091-CLAIM figure-table:BASE3-FIG-091 -->

Figure 91, “Example Privileged Action Admin Commands”: Provides a structured index to a concept, support condition, or example. Identify the named object, then read adjacent conditions, legend, and exceptions. This report explains only the PCIe/memory-based portion.

- Purpose: Provides a structured index to a concept, support condition, or example.

- How to read: Identify the named object, then read adjacent conditions, legend, and exceptions.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Choose a concrete controller configuration and map it to the relationships shown. This example adds no requirement.

- Scope: only the PCIe/memory-based portion is introduced.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.10, Figure 91, printed pages 135, PDF pages 161

## Use and limitations

Use the claim IDs as stable PPT traceability keys. Re-check affected claims if the source revision, errata set, or approved scope changes.
