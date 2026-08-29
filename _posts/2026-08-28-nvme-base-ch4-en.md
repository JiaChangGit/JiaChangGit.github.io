---
layout: post
read_time: true
show_date: true
title: "NVMe Base 2.4 Chapter 4: SQE, CQE, Status, PRP, and SGL"
date: 2026-08-28
description: "Source-located PCIe/NVMe report for PPT authoring."
tags: [NVMe, PCIe, Specification]
category: NVMe
author: Jia-Chang
github: JiaChangGit/JiaChangGit.github.io/tree/main/DOCS/nvme-spec-report
toc: yes
---

# NVMe Base 2.4 Chapter 4: SQE, CQE, Status, PRP, and SGL

Purpose: a source-located engineering report for GitHub Pages and a 100-minute presentation.

Scope: §4; printed pages 139–175; PDF pages 165–201. Only PCIe/memory-based and common NVMe content appears below.

## Source versions

NVM Express Base Specification, Revision 2.4

Verification date: 2026-08-29. No additional errata, ECNs, Technical Proposals, controller-vendor documents, or source text from the external PCI Express Base Specification are included.

## Reading map

```text
64-byte SQE -> PRP or SGL -> Command execution -> 16-byte+ CQE
```

The SQE identifies a command with CID plus SQID and describes buffers through data pointers; the CQE reports SQ head, SQID, CID, phase, and status.

## Normative language

shall is mandatory, may permits a choice, should expresses a preferred recommendation, and optional means support is not required. The report preserves these terms and never promotes one into another.

## Specification findings

### 1. BASE4-SQE

<!-- claim:BASE4-SQE -->

The common Admin and I/O SQE is 64 bytes. CDW0, NSID, data pointers, and CDW10–15 establish the common layout before each command defines command-specific content.

> Source: NVME-BASE-2.4, Rev. 2.4, §4.1.1, printed pages 139-143, PDF pages 165-169

### 2. BASE4-CID

<!-- claim:BASE4-CID -->

CID in combination with the Submission Queue identifier uniquely identifies a command. FFFFh should be avoided because the Error Information log uses it when an error is not associated with a particular command.

> Source: NVME-BASE-2.4, Rev. 2.4, §4.1.1, printed pages 140, PDF pages 166

### 3. BASE4-PSDT

<!-- claim:BASE4-PSDT -->

CDW0.PSDT selects PRP or SGL interpretation for DPTR. An Admin command over PCIe shall use PRPs unless its command definition specifies otherwise.

> Source: NVME-BASE-2.4, Rev. 2.4, §4.1.1, printed pages 140-142, PDF pages 166-168

### 4. BASE4-CQE

<!-- claim:BASE4-CQE -->

The common CQE is at least 16 bytes. If multiple writes construct it, the Phase Tag shall be updated in the last write so the host does not consume a partial entry.

> Source: NVME-BASE-2.4, Rev. 2.4, §4.2.1, printed pages 144-145, PDF pages 170-171

### 5. BASE4-STATUS

<!-- claim:BASE4-STATUS -->

Status decoding starts with Status Code Type (SCT), then Status Code (SC), together with control bits such as Do Not Retry (DNR). An SC value is not interpreted without its SCT.

> Source: NVME-BASE-2.4, Rev. 2.4, §4.2.3, printed pages 145-155, PDF pages 171-181

### 6. BASE4-PHASE

<!-- claim:BASE4-PHASE -->

The Phase Tag lets the host distinguish a new entry in a circular Completion Queue. After consuming CQEs, the host advances the CQ head doorbell and expects phase inversion on wrap.

> Source: NVME-BASE-2.4, Rev. 2.4, §4.2.4, printed pages 155-158, PDF pages 181-184

### 7. BASE4-PRP

<!-- claim:BASE4-PRP -->

A fixed-size PRP entry points to a physical memory page. The first entry may contain a page offset; subsequent PRPs shall obey page alignment, and transfer length determines the required entry count.

> Source: NVME-BASE-2.4, Rev. 2.4, §4.3.1, printed pages 158-159, PDF pages 184-185

### 8. BASE4-SGL

<!-- claim:BASE4-SGL -->

An SGL describes a data buffer through one or more descriptors and segments. SGL length shall equal or exceed the requested transfer length; this report covers only generic descriptors applicable to PCIe.

> Source: NVME-BASE-2.4, Rev. 2.4, §4.3.2, printed pages 159-166, PDF pages 185-192

### 9. BASE4-FEATURE

<!-- claim:BASE4-FEATURE -->

A Feature may have default, saved, and current values. Saved-value support and persistence across resets or power cycles are determined from SSFS and each Feature capability.

> Source: NVME-BASE-2.4, Rev. 2.4, §4.4, printed pages 166-169, PDF pages 192-195

### 10. BASE4-IDENTIFIER

<!-- claim:BASE4-IDENTIFIER -->

VID/SSVID, SN/MN, IEEE OUI, EUI64, NGUID, and UUID differ in origin, length, and uniqueness scope and are not interchangeable. This section is informative.

> Source: NVME-BASE-2.4, Rev. 2.4, §4.5, printed pages 169-172, PDF pages 195-198

### 11. BASE4-LISTS

<!-- claim:BASE4-LISTS -->

Controller and Namespace Lists provide a count followed by identifiers. A parser first validates the count, defined limit, and reserved area before consuming entries.

> Source: NVME-BASE-2.4, Rev. 2.4, §4.6, printed pages 172-173, PDF pages 198-199

### 12. BASE4-UTF8

<!-- claim:BASE4-UTF8 -->

UTF-8 input processing validates encoding, prohibited code points, and truncation using the specified flow; an arbitrary byte sequence is not automatically a valid string.

> Source: NVME-BASE-2.4, Rev. 2.4, §4.8, printed pages 175, PDF pages 201

## Figure-by-Figure Guide

The source uses Figure numbers for both diagrams and field-layout tables. No source artwork is reproduced.

### Figure 92: Command Dword 0

<!-- claim:BASE4-FIG-092-CLAIM figure-table:BASE4-FIG-092 -->

Figure 92, “Command Dword 0”: Organizes a field, bit, or register layout. Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Purpose: Organizes a field, bit, or register layout.

- How to read: Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Check capability support first, then decode using the specified width and mask. This example adds no requirement.

> Source: NVME-BASE-2.4, Rev. 2.4, §4.1.1, Figure 92, printed pages 139-140, PDF pages 165-166

### Figure 93: Common Command Format

<!-- claim:BASE4-FIG-093-CLAIM figure-table:BASE4-FIG-093 -->

Figure 93, “Common Command Format”: Organizes a field, bit, or register layout. Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Purpose: Organizes a field, bit, or register layout.

- How to read: Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Check capability support first, then decode using the specified width and mask. This example adds no requirement.

> Source: NVME-BASE-2.4, Rev. 2.4, §4.1.1, Figure 93, printed pages 140-142, PDF pages 166-168

### Figure 94: Common Command Format – Vendor Specific Commands (Optional)

<!-- claim:BASE4-FIG-094-CLAIM figure-table:BASE4-FIG-094 -->

Figure 94, “Common Command Format – Vendor Specific Commands (Optional)”: Organizes a field, bit, or register layout. Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Purpose: Organizes a field, bit, or register layout.

- How to read: Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Check capability support first, then decode using the specified width and mask. This example adds no requirement.

> Source: NVME-BASE-2.4, Rev. 2.4, §4.1.1, Figure 94, printed pages 143, PDF pages 169

### Figure 97: Common Completion Queue Entry Layout – Admin and All I/O Command Sets

<!-- claim:BASE4-FIG-097-CLAIM figure-table:BASE4-FIG-097 -->

Figure 97, “Common Completion Queue Entry Layout – Admin and All I/O Command Sets”: Organizes a queue or command relationship or processing sequence. Follow host, SQ, controller, CQ, and pointer or phase direction.

- Purpose: Organizes a queue or command relationship or processing sequence.

- How to read: Follow host, SQ, controller, CQ, and pointer or phase direction.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Choose one queue identifier and trace one command and its completion. This example adds no requirement.

> Source: NVME-BASE-2.4, Rev. 2.4, §4.2.1, Figure 97, printed pages 144, PDF pages 170

### Figure 98: Completion Queue Entry: DW 2

<!-- claim:BASE4-FIG-098-CLAIM figure-table:BASE4-FIG-098 -->

Figure 98, “Completion Queue Entry: DW 2”: Organizes a queue or command relationship or processing sequence. Follow host, SQ, controller, CQ, and pointer or phase direction.

- Purpose: Organizes a queue or command relationship or processing sequence.

- How to read: Follow host, SQ, controller, CQ, and pointer or phase direction.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Choose one queue identifier and trace one command and its completion. This example adds no requirement.

> Source: NVME-BASE-2.4, Rev. 2.4, §4.2.1, Figure 98, printed pages 144, PDF pages 170

### Figure 99: Completion Queue Entry: DW 3

<!-- claim:BASE4-FIG-099-CLAIM figure-table:BASE4-FIG-099 -->

Figure 99, “Completion Queue Entry: DW 3”: Organizes a queue or command relationship or processing sequence. Follow host, SQ, controller, CQ, and pointer or phase direction.

- Purpose: Organizes a queue or command relationship or processing sequence.

- How to read: Follow host, SQ, controller, CQ, and pointer or phase direction.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Choose one queue identifier and trace one command and its completion. This example adds no requirement.

> Source: NVME-BASE-2.4, Rev. 2.4, §4.2.1, Figure 99, printed pages 145, PDF pages 171

### Figure 101: Completion Queue Entry: Status Field

<!-- claim:BASE4-FIG-101-CLAIM figure-table:BASE4-FIG-101 -->

Figure 101, “Completion Queue Entry: Status Field”: Organizes a queue or command relationship or processing sequence. Follow host, SQ, controller, CQ, and pointer or phase direction.

- Purpose: Organizes a queue or command relationship or processing sequence.

- How to read: Follow host, SQ, controller, CQ, and pointer or phase direction.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Choose one queue identifier and trace one command and its completion. This example adds no requirement.

> Source: NVME-BASE-2.4, Rev. 2.4, §4.2.3, Figure 101, printed pages 145-146, PDF pages 171-172

### Figure 102: Status Code – Status Code Type Values

<!-- claim:BASE4-FIG-102-CLAIM figure-table:BASE4-FIG-102 -->

Figure 102, “Status Code – Status Code Type Values”: Organizes status or error fields and their classification. Read the type and control bits before decoding a code within that type; do not assign meaning to reserved values.

- Purpose: Organizes status or error fields and their classification.

- How to read: Read the type and control bits before decoding a code within that type; do not assign meaning to reserved values.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: For a failed CQE, decode SCT first, then SC and DNR. This example adds no requirement.

> Source: NVME-BASE-2.4, Rev. 2.4, §4.2.3, Figure 102, printed pages 146, PDF pages 172

### Figure 103: Status Code – Generic Command Status Values

<!-- claim:BASE4-FIG-103-CLAIM figure-table:BASE4-FIG-103 -->

Figure 103, “Status Code – Generic Command Status Values”: Organizes status or error fields and their classification. Read the type and control bits before decoding a code within that type; do not assign meaning to reserved values.

- Purpose: Organizes status or error fields and their classification.

- How to read: Read the type and control bits before decoding a code within that type; do not assign meaning to reserved values.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: For a failed CQE, decode SCT first, then SC and DNR. This example adds no requirement.

> Source: NVME-BASE-2.4, Rev. 2.4, §4.2.3, Figure 103, printed pages 147-150, PDF pages 173-176

### Figure 104: Status Code – Command Specific Status Values

<!-- claim:BASE4-FIG-104-CLAIM figure-table:BASE4-FIG-104 -->

Figure 104, “Status Code – Command Specific Status Values”: Organizes status or error fields and their classification. Read the type and control bits before decoding a code within that type; do not assign meaning to reserved values.

- Purpose: Organizes status or error fields and their classification.

- How to read: Read the type and control bits before decoding a code within that type; do not assign meaning to reserved values.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: For a failed CQE, decode SCT first, then SC and DNR. This example adds no requirement.

> Source: NVME-BASE-2.4, Rev. 2.4, §4.2.3.2, Figure 104, printed pages 151-152, PDF pages 177-178

### Figure 105: Status Code – Command Specific Status Values, I/O Command Set Specific

<!-- claim:BASE4-FIG-105-CLAIM figure-table:BASE4-FIG-105 -->

Figure 105, “Status Code – Command Specific Status Values, I/O Command Set Specific”: Organizes status or error fields and their classification. Read the type and control bits before decoding a code within that type; do not assign meaning to reserved values.

- Purpose: Organizes status or error fields and their classification.

- How to read: Read the type and control bits before decoding a code within that type; do not assign meaning to reserved values.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: For a failed CQE, decode SCT first, then SC and DNR. This example adds no requirement.

> Source: NVME-BASE-2.4, Rev. 2.4, §4.2.3.2, Figure 105, printed pages 152-153, PDF pages 178-179

### Figure 107: Status Code – Media and Data Integrity Error Values

<!-- claim:BASE4-FIG-107-CLAIM figure-table:BASE4-FIG-107 -->

Figure 107, “Status Code – Media and Data Integrity Error Values”: Organizes status or error fields and their classification. Read the type and control bits before decoding a code within that type; do not assign meaning to reserved values.

- Purpose: Organizes status or error fields and their classification.

- How to read: Read the type and control bits before decoding a code within that type; do not assign meaning to reserved values.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: For a failed CQE, decode SCT first, then SC and DNR. This example adds no requirement.

> Source: NVME-BASE-2.4, Rev. 2.4, §4.2.3.2, Figure 107, printed pages 154-155, PDF pages 180-181

### Figure 108: Status Code – Path Related Status Values

<!-- claim:BASE4-FIG-108-CLAIM figure-table:BASE4-FIG-108 -->

Figure 108, “Status Code – Path Related Status Values”: Organizes status or error fields and their classification. Read the type and control bits before decoding a code within that type; do not assign meaning to reserved values.

- Purpose: Organizes status or error fields and their classification.

- How to read: Read the type and control bits before decoding a code within that type; do not assign meaning to reserved values.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: For a failed CQE, decode SCT first, then SC and DNR. This example adds no requirement.

> Source: NVME-BASE-2.4, Rev. 2.4, §4.2.3.3, Figure 108, printed pages 155, PDF pages 181

### Figure 109: Phase Tag bit Transition Example

<!-- claim:BASE4-FIG-109-CLAIM figure-table:BASE4-FIG-109 -->

Figure 109, “Phase Tag bit Transition Example”: Organizes a queue or command relationship or processing sequence. Follow host, SQ, controller, CQ, and pointer or phase direction.

- Purpose: Organizes a queue or command relationship or processing sequence.

- How to read: Follow host, SQ, controller, CQ, and pointer or phase direction.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Choose one queue identifier and trace one command and its completion. This example adds no requirement.

> Source: NVME-BASE-2.4, Rev. 2.4, §4.2.4, Figure 109, printed pages 156-157, PDF pages 182-183

### Figure 110: PRP Entry Layout

<!-- claim:BASE4-FIG-110-CLAIM figure-table:BASE4-FIG-110 -->

Figure 110, “PRP Entry Layout”: Shows how PRP or SGL structures describe a data buffer. Check address, offset, length, alignment, and next-level pointers in order.

- Purpose: Shows how PRP or SGL structures describe a data buffer.

- How to read: Check address, offset, length, alignment, and next-level pointers in order.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Use a buffer crossing two memory pages to check the first offset and later alignment. This example adds no requirement.

> Source: NVME-BASE-2.4, Rev. 2.4, §4.3.1, Figure 110, printed pages 158, PDF pages 184

### Figure 111: PRP Entry – Page Base Address and Offset

<!-- claim:BASE4-FIG-111-CLAIM figure-table:BASE4-FIG-111 -->

Figure 111, “PRP Entry – Page Base Address and Offset”: Shows how PRP or SGL structures describe a data buffer. Check address, offset, length, alignment, and next-level pointers in order.

- Purpose: Shows how PRP or SGL structures describe a data buffer.

- How to read: Check address, offset, length, alignment, and next-level pointers in order.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Use a buffer crossing two memory pages to check the first offset and later alignment. This example adds no requirement.

> Source: NVME-BASE-2.4, Rev. 2.4, §4.3.1, Figure 111, printed pages 158, PDF pages 184

### Figure 112: PRP List Layout for Physically Contiguous Memory Pages

<!-- claim:BASE4-FIG-112-CLAIM figure-table:BASE4-FIG-112 -->

Figure 112, “PRP List Layout for Physically Contiguous Memory Pages”: Shows how PRP or SGL structures describe a data buffer. Check address, offset, length, alignment, and next-level pointers in order.

- Purpose: Shows how PRP or SGL structures describe a data buffer.

- How to read: Check address, offset, length, alignment, and next-level pointers in order.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Use a buffer crossing two memory pages to check the first offset and later alignment. This example adds no requirement.

> Source: NVME-BASE-2.4, Rev. 2.4, §4.3.1, Figure 112, printed pages 159, PDF pages 185

### Figure 113: PRP List Layout for Physically Non-Contiguous Memory Pages

<!-- claim:BASE4-FIG-113-CLAIM figure-table:BASE4-FIG-113 -->

Figure 113, “PRP List Layout for Physically Non-Contiguous Memory Pages”: Shows how PRP or SGL structures describe a data buffer. Check address, offset, length, alignment, and next-level pointers in order.

- Purpose: Shows how PRP or SGL structures describe a data buffer.

- How to read: Check address, offset, length, alignment, and next-level pointers in order.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Use a buffer crossing two memory pages to check the first offset and later alignment. This example adds no requirement.

> Source: NVME-BASE-2.4, Rev. 2.4, §4.3.1, Figure 113, printed pages 159, PDF pages 185

### Figure 114: SGL Validation Error Conditions

<!-- claim:BASE4-FIG-114-CLAIM figure-table:BASE4-FIG-114 -->

Figure 114, “SGL Validation Error Conditions”: Shows how PRP or SGL structures describe a data buffer. Check address, offset, length, alignment, and next-level pointers in order.

- Purpose: Shows how PRP or SGL structures describe a data buffer.

- How to read: Check address, offset, length, alignment, and next-level pointers in order.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Use a buffer crossing two memory pages to check the first offset and later alignment. This example adds no requirement.

> Source: NVME-BASE-2.4, Rev. 2.4, §4.3.2, Figure 114, printed pages 161, PDF pages 187

### Figure 115: SGL Segment

<!-- claim:BASE4-FIG-115-CLAIM figure-table:BASE4-FIG-115 -->

Figure 115, “SGL Segment”: Shows how PRP or SGL structures describe a data buffer. Check address, offset, length, alignment, and next-level pointers in order.

- Purpose: Shows how PRP or SGL structures describe a data buffer.

- How to read: Check address, offset, length, alignment, and next-level pointers in order.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Use a buffer crossing two memory pages to check the first offset and later alignment. This example adds no requirement.

> Source: NVME-BASE-2.4, Rev. 2.4, §4.3.2, Figure 115, printed pages 161, PDF pages 187

### Figure 116: Generic SGL Descriptor Format

<!-- claim:BASE4-FIG-116-CLAIM figure-table:BASE4-FIG-116 -->

Figure 116, “Generic SGL Descriptor Format”: Shows how PRP or SGL structures describe a data buffer. Check address, offset, length, alignment, and next-level pointers in order.

- Purpose: Shows how PRP or SGL structures describe a data buffer.

- How to read: Check address, offset, length, alignment, and next-level pointers in order.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Use a buffer crossing two memory pages to check the first offset and later alignment. This example adds no requirement.

> Source: NVME-BASE-2.4, Rev. 2.4, §4.3.2, Figure 116, printed pages 161, PDF pages 187

### Figure 117: SGL Descriptor Type

<!-- claim:BASE4-FIG-117-CLAIM figure-table:BASE4-FIG-117 -->

Figure 117, “SGL Descriptor Type”: Shows how PRP or SGL structures describe a data buffer. Check address, offset, length, alignment, and next-level pointers in order. This report explains only the PCIe/memory-based portion.

- Purpose: Shows how PRP or SGL structures describe a data buffer.

- How to read: Check address, offset, length, alignment, and next-level pointers in order.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Use a buffer crossing two memory pages to check the first offset and later alignment. This example adds no requirement.

- Scope: only the PCIe/memory-based portion is introduced.

> Source: NVME-BASE-2.4, Rev. 2.4, §4.3.2, Figure 117, printed pages 161-162, PDF pages 187-188

### Figure 118: SGL Descriptor Sub Type Values

<!-- claim:BASE4-FIG-118-CLAIM figure-table:BASE4-FIG-118 -->

Figure 118, “SGL Descriptor Sub Type Values”: Shows how PRP or SGL structures describe a data buffer. Check address, offset, length, alignment, and next-level pointers in order. This report explains only the PCIe/memory-based portion.

- Purpose: Shows how PRP or SGL structures describe a data buffer.

- How to read: Check address, offset, length, alignment, and next-level pointers in order.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Use a buffer crossing two memory pages to check the first offset and later alignment. This example adds no requirement.

- Scope: only the PCIe/memory-based portion is introduced.

> Source: NVME-BASE-2.4, Rev. 2.4, §4.3.2, Figure 118, printed pages 162, PDF pages 188

### Figure 119: SGL Data Block descriptor

<!-- claim:BASE4-FIG-119-CLAIM figure-table:BASE4-FIG-119 -->

Figure 119, “SGL Data Block descriptor”: Shows how PRP or SGL structures describe a data buffer. Check address, offset, length, alignment, and next-level pointers in order.

- Purpose: Shows how PRP or SGL structures describe a data buffer.

- How to read: Check address, offset, length, alignment, and next-level pointers in order.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Use a buffer crossing two memory pages to check the first offset and later alignment. This example adds no requirement.

> Source: NVME-BASE-2.4, Rev. 2.4, §4.3.2, Figure 119, printed pages 162-163, PDF pages 188-189

### Figure 120: SGL Bit Bucket descriptor

<!-- claim:BASE4-FIG-120-CLAIM figure-table:BASE4-FIG-120 -->

Figure 120, “SGL Bit Bucket descriptor”: Shows how PRP or SGL structures describe a data buffer. Check address, offset, length, alignment, and next-level pointers in order.

- Purpose: Shows how PRP or SGL structures describe a data buffer.

- How to read: Check address, offset, length, alignment, and next-level pointers in order.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Use a buffer crossing two memory pages to check the first offset and later alignment. This example adds no requirement.

> Source: NVME-BASE-2.4, Rev. 2.4, §4.3.2, Figure 120, printed pages 163, PDF pages 189

### Figure 121: SGL Segment descriptor

<!-- claim:BASE4-FIG-121-CLAIM figure-table:BASE4-FIG-121 -->

Figure 121, “SGL Segment descriptor”: Shows how PRP or SGL structures describe a data buffer. Check address, offset, length, alignment, and next-level pointers in order.

- Purpose: Shows how PRP or SGL structures describe a data buffer.

- How to read: Check address, offset, length, alignment, and next-level pointers in order.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Use a buffer crossing two memory pages to check the first offset and later alignment. This example adds no requirement.

> Source: NVME-BASE-2.4, Rev. 2.4, §4.3.2, Figure 121, printed pages 163, PDF pages 189

### Figure 122: SGL Last Segment descriptor

<!-- claim:BASE4-FIG-122-CLAIM figure-table:BASE4-FIG-122 -->

Figure 122, “SGL Last Segment descriptor”: Shows how PRP or SGL structures describe a data buffer. Check address, offset, length, alignment, and next-level pointers in order.

- Purpose: Shows how PRP or SGL structures describe a data buffer.

- How to read: Check address, offset, length, alignment, and next-level pointers in order.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Use a buffer crossing two memory pages to check the first offset and later alignment. This example adds no requirement.

> Source: NVME-BASE-2.4, Rev. 2.4, §4.3.2, Figure 122, printed pages 164, PDF pages 190

### Figure 125: SGL Read Example

<!-- claim:BASE4-FIG-125-CLAIM figure-table:BASE4-FIG-125 -->

Figure 125, “SGL Read Example”: Shows how PRP or SGL structures describe a data buffer. Check address, offset, length, alignment, and next-level pointers in order.

- Purpose: Shows how PRP or SGL structures describe a data buffer.

- How to read: Check address, offset, length, alignment, and next-level pointers in order.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Use a buffer crossing two memory pages to check the first offset and later alignment. This example adds no requirement.

> Source: NVME-BASE-2.4, Rev. 2.4, §4.3.2.1, Figure 125, printed pages 166, PDF pages 192

### Figure 126: Current Value after Reset with Scope of Entire NVM Subsystem

<!-- claim:BASE4-FIG-126-CLAIM figure-table:BASE4-FIG-126 -->

Figure 126, “Current Value after Reset with Scope of Entire NVM Subsystem”: Shows containment, connection, or capacity relationships among subsystem objects. Keep controllers, ports, namespaces, identifiers, and capacity levels distinct.

- Purpose: Shows containment, connection, or capacity relationships among subsystem objects.

- How to read: Keep controllers, ports, namespaces, identifiers, and capacity levels distinct.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: For one namespace, mark its NSID, controller, and capacity hierarchy. This example adds no requirement.

> Source: NVME-BASE-2.4, Rev. 2.4, §4.4, Figure 126, printed pages 167, PDF pages 193

### Figure 127: Current Value after Reset with Scope of Subset of the NVM Subsystem

<!-- claim:BASE4-FIG-127-CLAIM figure-table:BASE4-FIG-127 -->

Figure 127, “Current Value after Reset with Scope of Subset of the NVM Subsystem”: Shows containment, connection, or capacity relationships among subsystem objects. Keep controllers, ports, namespaces, identifiers, and capacity levels distinct.

- Purpose: Shows containment, connection, or capacity relationships among subsystem objects.

- How to read: Keep controllers, ports, namespaces, identifiers, and capacity levels distinct.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: For one namespace, mark its NSID, controller, and capacity hierarchy. This example adds no requirement.

> Source: NVME-BASE-2.4, Rev. 2.4, §4.4, Figure 127, printed pages 168, PDF pages 194

### Figure 128: PCI Vendor ID (VID) and PCI Subsystem Vendor ID (SSVID)

<!-- claim:BASE4-FIG-128-CLAIM figure-table:BASE4-FIG-128 -->

Figure 128, “PCI Vendor ID (VID) and PCI Subsystem Vendor ID (SSVID)”: Shows containment, connection, or capacity relationships among subsystem objects. Keep controllers, ports, namespaces, identifiers, and capacity levels distinct.

- Purpose: Shows containment, connection, or capacity relationships among subsystem objects.

- How to read: Keep controllers, ports, namespaces, identifiers, and capacity levels distinct.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: For one namespace, mark its NSID, controller, and capacity hierarchy. This example adds no requirement.

> Source: NVME-BASE-2.4, Rev. 2.4, §4.5.1, Figure 128, printed pages 169, PDF pages 195

### Figure 129: Serial Number (SN) and Model Number (MN)

<!-- claim:BASE4-FIG-129-CLAIM figure-table:BASE4-FIG-129 -->

Figure 129, “Serial Number (SN) and Model Number (MN)”: Organizes identifier or list byte layout and scope. Check length, byte order, count, uniqueness scope, and reserved area.

- Purpose: Organizes identifier or list byte layout and scope.

- How to read: Check length, byte order, count, uniqueness scope, and reserved area.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: A parser validates count and length before reading identifiers. This example adds no requirement.

> Source: NVME-BASE-2.4, Rev. 2.4, §4.5.2, Figure 129, printed pages 170, PDF pages 196

### Figure 130: IEEE OUI Identifier (IEEE)

<!-- claim:BASE4-FIG-130-CLAIM figure-table:BASE4-FIG-130 -->

Figure 130, “IEEE OUI Identifier (IEEE)”: Organizes identifier or list byte layout and scope. Check length, byte order, count, uniqueness scope, and reserved area.

- Purpose: Organizes identifier or list byte layout and scope.

- How to read: Check length, byte order, count, uniqueness scope, and reserved area.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: A parser validates count and length before reading identifiers. This example adds no requirement.

> Source: NVME-BASE-2.4, Rev. 2.4, §4.5.3, Figure 130, printed pages 170, PDF pages 196

### Figure 131: IEEE Extended Unique Identifier (EUI64), MA-L Format

<!-- claim:BASE4-FIG-131-CLAIM figure-table:BASE4-FIG-131 -->

Figure 131, “IEEE Extended Unique Identifier (EUI64), MA-L Format”: Organizes a field, bit, or register layout. Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Purpose: Organizes a field, bit, or register layout.

- How to read: Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Check capability support first, then decode using the specified width and mask. This example adds no requirement.

> Source: NVME-BASE-2.4, Rev. 2.4, §4.5.4, Figure 131, printed pages 170, PDF pages 196

### Figure 132: IEEE Extended Unique Identifier (EUI64), OUI Identifier

<!-- claim:BASE4-FIG-132-CLAIM figure-table:BASE4-FIG-132 -->

Figure 132, “IEEE Extended Unique Identifier (EUI64), OUI Identifier”: Organizes identifier or list byte layout and scope. Check length, byte order, count, uniqueness scope, and reserved area.

- Purpose: Organizes identifier or list byte layout and scope.

- How to read: Check length, byte order, count, uniqueness scope, and reserved area.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: A parser validates count and length before reading identifiers. This example adds no requirement.

> Source: NVME-BASE-2.4, Rev. 2.4, §4.5.4, Figure 132, printed pages 170, PDF pages 196

### Figure 133: IEEE Extended Unique Identifier (EUI64), Ext. ID (cont)

<!-- claim:BASE4-FIG-133-CLAIM figure-table:BASE4-FIG-133 -->

Figure 133, “IEEE Extended Unique Identifier (EUI64), Ext. ID (cont)”: Organizes identifier or list byte layout and scope. Check length, byte order, count, uniqueness scope, and reserved area.

- Purpose: Organizes identifier or list byte layout and scope.

- How to read: Check length, byte order, count, uniqueness scope, and reserved area.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: A parser validates count and length before reading identifiers. This example adds no requirement.

> Source: NVME-BASE-2.4, Rev. 2.4, §4.5.4, Figure 133, printed pages 170-171, PDF pages 196-197

### Figure 134: MA-L similarity to WWN

<!-- claim:BASE4-FIG-134-CLAIM figure-table:BASE4-FIG-134 -->

Figure 134, “MA-L similarity to WWN”: Provides a structured index to a concept, support condition, or example. Identify the named object, then read adjacent conditions, legend, and exceptions.

- Purpose: Provides a structured index to a concept, support condition, or example.

- How to read: Identify the named object, then read adjacent conditions, legend, and exceptions.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Choose a concrete controller configuration and map it to the relationships shown. This example adds no requirement.

> Source: NVME-BASE-2.4, Rev. 2.4, §4.5.4, Figure 134, printed pages 171, PDF pages 197

### Figure 135: Namespace Globally Unique Identifier (NGUID)

<!-- claim:BASE4-FIG-135-CLAIM figure-table:BASE4-FIG-135 -->

Figure 135, “Namespace Globally Unique Identifier (NGUID)”: Shows containment, connection, or capacity relationships among subsystem objects. Keep controllers, ports, namespaces, identifiers, and capacity levels distinct.

- Purpose: Shows containment, connection, or capacity relationships among subsystem objects.

- How to read: Keep controllers, ports, namespaces, identifiers, and capacity levels distinct.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: For one namespace, mark its NSID, controller, and capacity hierarchy. This example adds no requirement.

> Source: NVME-BASE-2.4, Rev. 2.4, §4.5.5, Figure 135, printed pages 171, PDF pages 197

### Figure 136: Namespace Globally Unique Identifier (NGUID), OUI

<!-- claim:BASE4-FIG-136-CLAIM figure-table:BASE4-FIG-136 -->

Figure 136, “Namespace Globally Unique Identifier (NGUID), OUI”: Shows containment, connection, or capacity relationships among subsystem objects. Keep controllers, ports, namespaces, identifiers, and capacity levels distinct.

- Purpose: Shows containment, connection, or capacity relationships among subsystem objects.

- How to read: Keep controllers, ports, namespaces, identifiers, and capacity levels distinct.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: For one namespace, mark its NSID, controller, and capacity hierarchy. This example adds no requirement.

> Source: NVME-BASE-2.4, Rev. 2.4, §4.5.5, Figure 136, printed pages 171, PDF pages 197

### Figure 137: Namespace Globally Unique Identifier

<!-- claim:BASE4-FIG-137-CLAIM figure-table:BASE4-FIG-137 -->

Figure 137, “Namespace Globally Unique Identifier”: Shows containment, connection, or capacity relationships among subsystem objects. Keep controllers, ports, namespaces, identifiers, and capacity levels distinct.

- Purpose: Shows containment, connection, or capacity relationships among subsystem objects.

- How to read: Keep controllers, ports, namespaces, identifiers, and capacity levels distinct.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: For one namespace, mark its NSID, controller, and capacity hierarchy. This example adds no requirement.

> Source: NVME-BASE-2.4, Rev. 2.4, §4.5.5, Figure 137, printed pages 171, PDF pages 197

### Figure 138: Namespace Globally Unique Identifier (NGUID), NGUID similarity to WWN

<!-- claim:BASE4-FIG-138-CLAIM figure-table:BASE4-FIG-138 -->

Figure 138, “Namespace Globally Unique Identifier (NGUID), NGUID similarity to WWN”: Shows containment, connection, or capacity relationships among subsystem objects. Keep controllers, ports, namespaces, identifiers, and capacity levels distinct.

- Purpose: Shows containment, connection, or capacity relationships among subsystem objects.

- How to read: Keep controllers, ports, namespaces, identifiers, and capacity levels distinct.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: For one namespace, mark its NSID, controller, and capacity hierarchy. This example adds no requirement.

> Source: NVME-BASE-2.4, Rev. 2.4, §4.5.5, Figure 138, printed pages 171, PDF pages 197

### Figure 139: Controller List Format

<!-- claim:BASE4-FIG-139-CLAIM figure-table:BASE4-FIG-139 -->

Figure 139, “Controller List Format”: Organizes a field, bit, or register layout. Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Purpose: Organizes a field, bit, or register layout.

- How to read: Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Check capability support first, then decode using the specified width and mask. This example adds no requirement.

> Source: NVME-BASE-2.4, Rev. 2.4, §4.6.1, Figure 139, printed pages 172, PDF pages 198

### Figure 140: Namespace List Format

<!-- claim:BASE4-FIG-140-CLAIM figure-table:BASE4-FIG-140 -->

Figure 140, “Namespace List Format”: Organizes a field, bit, or register layout. Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Purpose: Organizes a field, bit, or register layout.

- How to read: Map offsets, bytes, or bits to names, access type, reset value, and conditions.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Check capability support first, then decode using the specified width and mask. This example adds no requirement.

> Source: NVME-BASE-2.4, Rev. 2.4, §4.6.2, Figure 140, printed pages 172, PDF pages 198

### Figure 142: UTF-8 Input Processing

<!-- claim:BASE4-FIG-142-CLAIM figure-table:BASE4-FIG-142 -->

Figure 142, “UTF-8 Input Processing”: Provides a structured index to a concept, support condition, or example. Identify the named object, then read adjacent conditions, legend, and exceptions.

- Purpose: Provides a structured index to a concept, support condition, or example.

- How to read: Identify the named object, then read adjacent conditions, legend, and exceptions.

- Normative force: this guide adds no shall, may, or should; use the adjacent source text and field descriptions.

- Informative example: Choose a concrete controller configuration and map it to the relationships shown. This example adds no requirement.

> Source: NVME-BASE-2.4, Rev. 2.4, §4.8, Figure 142, printed pages 175, PDF pages 201

## Use and limitations

Use the claim IDs as stable PPT traceability keys. Re-check affected claims if the source revision, errata set, or approved scope changes.
