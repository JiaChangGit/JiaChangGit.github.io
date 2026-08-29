---
layout: post
read_time: true
show_date: true
title: "NVMe Base 2.4 Chapter 4: SQE, CQE, Status, PRP, and SGL"
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

# NVMe Base 2.4 Chapter 4: SQE, CQE, Status, PRP, and SGL

Purpose: a source-located engineering report for GitHub Pages and a 100-minute presentation.

Scope: §4; printed pages 139-175; PDF pages 165-201. Only PCIe/memory-based and common NVMe content appears below.

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

### 1. Common SQE layout

<!-- claim:BASE4-SQE -->

The common Admin and I/O SQE is 64 bytes. CDW0, NSID, data pointers, and CDW10-15 establish the common layout before each command defines command-specific content.

> Source: NVME-BASE-2.4, Rev. 2.4, §4.1.1, printed pages 139-143, PDF pages 165-169

### 2. CID uniqueness

<!-- claim:BASE4-CID -->

CID in combination with the Submission Queue identifier uniquely identifies a command. FFFFh should be avoided because the Error Information log uses it when an error is not associated with a particular command.

> Source: NVME-BASE-2.4, Rev. 2.4, §4.1.1, printed pages 140, PDF pages 166

### 3. PRP/SGL selection

<!-- claim:BASE4-PSDT -->

CDW0.PSDT selects PRP or SGL interpretation for DPTR. An Admin command over PCIe shall use PRPs unless its command definition specifies otherwise.

> Source: NVME-BASE-2.4, Rev. 2.4, §4.1.1, printed pages 140-142, PDF pages 166-168

### 4. Common CQE and Phase Tag

<!-- claim:BASE4-CQE -->

The common CQE is at least 16 bytes. If multiple writes construct it, the Phase Tag shall be updated in the last write so the host does not consume a partial entry.

> Source: NVME-BASE-2.4, Rev. 2.4, §4.2.1, printed pages 144-145, PDF pages 170-171

### 5. SCT, SC, and DNR

<!-- claim:BASE4-STATUS -->

Status decoding starts with Status Code Type (SCT), then Status Code (SC), together with control bits such as Do Not Retry (DNR). An SC value is not interpreted without its SCT.

> Source: NVME-BASE-2.4, Rev. 2.4, §4.2.3, printed pages 145-155, PDF pages 171-181

### 6. Completion Queue phase

<!-- claim:BASE4-PHASE -->

The Phase Tag lets the host distinguish a new entry in a circular Completion Queue. After consuming CQEs, the host advances the CQ head doorbell and expects phase inversion on wrap.

> Source: NVME-BASE-2.4, Rev. 2.4, §4.2.4, printed pages 155-158, PDF pages 181-184

### 7. PRP alignment and pages

<!-- claim:BASE4-PRP -->

A fixed-size PRP entry points to a physical memory page. The first entry may contain a page offset; subsequent PRPs shall obey page alignment, and transfer length determines the required entry count.

> Source: NVME-BASE-2.4, Rev. 2.4, §4.3.1, printed pages 158-159, PDF pages 184-185

### 8. SGL descriptors and length

<!-- claim:BASE4-SGL -->

An SGL describes a data buffer through one or more descriptors and segments. SGL length shall equal or exceed the requested transfer length; this report covers only generic descriptors applicable to PCIe.

> Source: NVME-BASE-2.4, Rev. 2.4, §4.3.2, printed pages 159-166, PDF pages 185-192

### 9. Feature values and persistence

<!-- claim:BASE4-FEATURE -->

A Feature may have default, saved, and current values. Saved-value support and persistence across resets or power cycles are determined from SSFS and each Feature capability.

> Source: NVME-BASE-2.4, Rev. 2.4, §4.4, printed pages 166-169, PDF pages 192-195

### 10. Scope of global identifiers

<!-- claim:BASE4-IDENTIFIER -->

VID/SSVID, SN/MN, IEEE OUI, EUI64, NGUID, and UUID differ in origin, length, and uniqueness scope and are not interchangeable. This section is informative.

> Source: NVME-BASE-2.4, Rev. 2.4, §4.5, printed pages 169-172, PDF pages 195-198

### 11. Controller and Namespace Lists

<!-- claim:BASE4-LISTS -->

Controller and Namespace Lists provide a count followed by identifiers. A parser first validates the count, defined limit, and reserved area before consuming entries.

> Source: NVME-BASE-2.4, Rev. 2.4, §4.6, printed pages 172-173, PDF pages 198-199

### 12. UTF-8 input validation

<!-- claim:BASE4-UTF8 -->

UTF-8 input processing validates encoding, prohibited code points, and truncation using the specified flow; an arbitrary byte sequence is not automatically a valid string.

> Source: NVME-BASE-2.4, Rev. 2.4, §4.8, printed pages 175, PDF pages 201

## Figure index

This report introduces all 44 in-scope Figures. Use the section links below for the 100-minute presentation path; every Figure remains available as an appendix item.

- [§4.1](#section-4-1)

- [§4.2](#section-4-2)

- [§4.3](#section-4-3)

- [§4.4](#section-4-4)

- [§4.5](#section-4-5)

- [§4.6](#section-4-6)

- [§4.8](#section-4-8)

## Figure-by-Figure Guide

The source uses Figure numbers for diagrams and field-layout tables. No source artwork is reproduced; compact field and keyword indexes come from the locally verified PDFs.

<a id="section-4-1"></a>

### §4.1

<details markdown="1">
<summary><strong>Figure 92: Command Dword 0</strong></summary>

<!-- claim:BASE4-FIG-092-CLAIM figure-table:BASE4-FIG-092 -->

Figure 92, "Command Dword 0": Defines the concrete layout or value relationships for Command Dword 0. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is CID, PSDT, FUSE, OPC, FN, DTD, PRP, SGL.

- Purpose: Defines the concrete layout or value relationships for Command Dword 0.

- How to read: Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is CID, PSDT, FUSE, OPC, FN, DTD, PRP, SGL.

- Conditions and limits: Source keyword index: `shall not`, `should not`, `shall`, `should`, `may`, `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Use CID as the first parser checkpoint and PSDT as a second, independent boundary check. This example adds no requirement.

- Source field index: CID, PSDT, FUSE, OPC, FN, DTD, PRP, SGL

- Source keyword index: `shall not`, `should not`, `shall`, `should`, `may`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §4.1.1, Figure 92, printed pages 139-140, PDF pages 165-166

</details>

<details markdown="1">
<summary><strong>Figure 93: Common Command Format</strong></summary>

<!-- claim:BASE4-FIG-093-CLAIM figure-table:BASE4-FIG-093 -->

Figure 93, "Common Command Format": Defines the concrete layout or value relationships for Common Command Format. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is CDW0, NSID, CDW2, CDW3, MPTR, DPTR, PRP2, PRP1.

- Purpose: Defines the concrete layout or value relationships for Common Command Format.

- How to read: Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is CDW0, NSID, CDW2, CDW3, MPTR, DPTR, PRP2, PRP1.

- Conditions and limits: Source keyword index: `shall`, `may`, `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Use CDW0 as the first parser checkpoint and NSID as a second, independent boundary check. This example adds no requirement.

- Source field index: CDW0, NSID, CDW2, CDW3, MPTR, DPTR, PRP2, PRP1

- Source keyword index: `shall`, `may`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §4.1.1, Figure 93, printed pages 140-142, PDF pages 166-168

</details>

<details markdown="1">
<summary><strong>Figure 94: Common Command Format - Vendor Specific Commands (Optional)</strong></summary>

<!-- claim:BASE4-FIG-094-CLAIM figure-table:BASE4-FIG-094 -->

Figure 94, "Common Command Format - Vendor Specific Commands (Optional)": Defines the concrete layout or value relationships for Common Command Format - Vendor Specific Commands (Optional). Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is CDW0, NSID, MDPTR, NDT, NDM, CDW12, CDW13, CDW14.

- Purpose: Defines the concrete layout or value relationships for Common Command Format - Vendor Specific Commands (Optional).

- How to read: Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is CDW0, NSID, MDPTR, NDT, NDM, CDW12, CDW13, CDW14.

- Conditions and limits: Source keyword index: `shall`, `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Use CDW0 as the first parser checkpoint and NSID as a second, independent boundary check. This example adds no requirement.

- Source field index: CDW0, NSID, MDPTR, NDT, NDM, CDW12, CDW13, CDW14

- Source keyword index: `shall`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §4.1.1, Figure 94, printed pages 143, PDF pages 169

</details>

<a id="section-4-2"></a>

### §4.2

<details markdown="1">
<summary><strong>Figure 97: Common Completion Queue Entry Layout - Admin and All I/O Command Sets</strong></summary>

<!-- claim:BASE4-FIG-097-CLAIM figure-table:BASE4-FIG-097 -->

Figure 97, "Common Completion Queue Entry Layout - Admin and All I/O Command Sets": Defines the concrete layout or value relationships for Common Completion Queue Entry Layout - Admin and All I/O Command Sets. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is DW0, DW1, DW2, SQ, DW3, Command Set, Completion Queue, Command.

- Purpose: Defines the concrete layout or value relationships for Common Completion Queue Entry Layout - Admin and All I/O Command Sets.

- How to read: Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is DW0, DW1, DW2, SQ, DW3, Command Set, Completion Queue, Command.

- Conditions and limits: The Figure is explanatory or structural; this guide does not turn its visual relationship into a new requirement.

- Informative example: Use DW0 as the first parser checkpoint and DW1 as a second, independent boundary check. This example adds no requirement.

- Source field index: DW0, DW1, DW2, SQ, DW3, Command Set, Completion Queue, Command

- Source keyword index: none

> Source: NVME-BASE-2.4, Rev. 2.4, §4.2.1, Figure 97, printed pages 144, PDF pages 170

</details>

<details markdown="1">
<summary><strong>Figure 98: Completion Queue Entry: DW 2</strong></summary>

<!-- claim:BASE4-FIG-098-CLAIM figure-table:BASE4-FIG-098 -->

Figure 98, "Completion Queue Entry: DW 2": Shows the queue or command relationship expressed by Completion Queue Entry: DW 2. Trace ownership and direction from host to SQ, controller, and CQ; keep the indexed elements distinct: SQID, SQHD, DW, SQ, CID, Completion Queue.

- Purpose: Shows the queue or command relationship expressed by Completion Queue Entry: DW 2.

- How to read: Trace ownership and direction from host to SQ, controller, and CQ; keep the indexed elements distinct: SQID, SQHD, DW, SQ, CID, Completion Queue.

- Conditions and limits: Source keyword index: `may`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Trace one command through Figure 98, using SQID and SQHD as checkpoints for ownership or pointer movement. This example adds no requirement.

- Source field index: SQID, SQHD, DW, SQ, CID, Completion Queue

- Source keyword index: `may`

> Source: NVME-BASE-2.4, Rev. 2.4, §4.2.1, Figure 98, printed pages 144, PDF pages 170

</details>

<details markdown="1">
<summary><strong>Figure 99: Completion Queue Entry: DW 3</strong></summary>

<!-- claim:BASE4-FIG-099-CLAIM figure-table:BASE4-FIG-099 -->

Figure 99, "Completion Queue Entry: DW 3": Shows the queue or command relationship expressed by Completion Queue Entry: DW 3. Trace ownership and direction from host to SQ, controller, and CQ; keep the indexed elements distinct: STATUS, CID, DW, SQ, Completion Queue.

- Purpose: Shows the queue or command relationship expressed by Completion Queue Entry: DW 3.

- How to read: Trace ownership and direction from host to SQ, controller, and CQ; keep the indexed elements distinct: STATUS, CID, DW, SQ, Completion Queue.

- Conditions and limits: The Figure is explanatory or structural; this guide does not turn its visual relationship into a new requirement.

- Informative example: Trace one command through Figure 99, using STATUS and CID as checkpoints for ownership or pointer movement. This example adds no requirement.

- Source field index: STATUS, CID, DW, SQ, Completion Queue

- Source keyword index: none

> Source: NVME-BASE-2.4, Rev. 2.4, §4.2.1, Figure 99, printed pages 145, PDF pages 171

</details>

<details markdown="1">
<summary><strong>Figure 101: Completion Queue Entry: Status Field</strong></summary>

<!-- claim:BASE4-FIG-101-CLAIM figure-table:BASE4-FIG-101 -->

Figure 101, "Completion Queue Entry: Status Field": Defines the concrete layout or value relationships for Completion Queue Entry: Status Field. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is DNR, CRD, SCT, SC, ACRE, CRDT1, CRDT2, CRDT3.

- Purpose: Defines the concrete layout or value relationships for Completion Queue Entry: Status Field.

- How to read: Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is DNR, CRD, SCT, SC, ACRE, CRDT1, CRDT2, CRDT3.

- Conditions and limits: Source keyword index: `should not`, `should`, `may`, `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Use DNR as the first parser checkpoint and CRD as a second, independent boundary check. This example adds no requirement.

- Source field index: DNR, CRD, SCT, SC, ACRE, CRDT1, CRDT2, CRDT3

- Source keyword index: `should not`, `should`, `may`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §4.2.3, Figure 101, printed pages 145-146, PDF pages 171-172

</details>

<details markdown="1">
<summary><strong>Figure 102: Status Code - Status Code Type Values</strong></summary>

<!-- claim:BASE4-FIG-102-CLAIM figure-table:BASE4-FIG-102 -->

Figure 102, "Status Code - Status Code Type Values": Defines the status/error classification represented by Status Code - Status Code Type Values. Resolve the category before the individual code or flag; keep reserved values uninterpreted. Evidence index: SC, Status Code.

- Purpose: Defines the status/error classification represented by Status Code - Status Code Type Values.

- How to read: Resolve the category before the individual code or flag; keep reserved values uninterpreted. Evidence index: SC, Status Code.

- Conditions and limits: Source keyword index: `shall`, `may`, `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: For one reported condition, identify SC first and then check Status Code instead of decoding an isolated numeric value. This example adds no requirement.

- Source field index: SC, Status Code

- Source keyword index: `shall`, `may`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §4.2.3, Figure 102, printed pages 146, PDF pages 172

</details>

<details markdown="1">
<summary><strong>Figure 103: Status Code - Generic Command Status Values</strong></summary>

<!-- claim:BASE4-FIG-103-CLAIM figure-table:BASE4-FIG-103 -->

Figure 103, "Status Code - Generic Command Status Values": Defines the status/error classification represented by Status Code - Generic Command Status Values. Resolve the category before the individual code or flag; keep reserved values uninterpreted. Evidence index: ID, SQ, TCG, SGL, PRP, ZNS, RACQA, CMB.

- Purpose: Defines the status/error classification represented by Status Code - Generic Command Status Values.

- How to read: Resolve the category before the individual code or flag; keep reserved values uninterpreted. Evidence index: ID, SQ, TCG, SGL, PRP, ZNS, RACQA, CMB.

- Conditions and limits: Source keyword index: `shall not`, `shall`, `should`, `may`, `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: For one reported condition, identify ID first and then check SQ instead of decoding an isolated numeric value. This example adds no requirement.

- Source field index: ID, SQ, TCG, SGL, PRP, ZNS, RACQA, CMB

- Source keyword index: `shall not`, `shall`, `should`, `may`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §4.2.3, Figure 103, printed pages 147-150, PDF pages 173-176

</details>

<details markdown="1">
<summary><strong>Figure 104: Status Code - Command Specific Status Values</strong></summary>

<!-- claim:BASE4-FIG-104-CLAIM figure-table:BASE4-FIG-104 -->

Figure 104, "Status Code - Command Specific Status Values": Defines the status/error classification represented by Status Code - Command Specific Status Values. Resolve the category before the individual code or flag; keep reserved values uninterpreted. Evidence index: ANA, NOTE, Status Code, Command.

- Purpose: Defines the status/error classification represented by Status Code - Command Specific Status Values.

- How to read: Resolve the category before the individual code or flag; keep reserved values uninterpreted. Evidence index: ANA, NOTE, Status Code, Command.

- Conditions and limits: Source keyword index: `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: For one reported condition, identify ANA first and then check NOTE instead of decoding an isolated numeric value. This example adds no requirement.

- Source field index: ANA, NOTE, Status Code, Command

- Source keyword index: `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §4.2.3.2, Figure 104, printed pages 151-152, PDF pages 177-178

</details>

<details markdown="1">
<summary><strong>Figure 105: Status Code - Command Specific Status Values, I/O Command Set Specific</strong></summary>

<!-- claim:BASE4-FIG-105-CLAIM figure-table:BASE4-FIG-105 -->

Figure 105, "Status Code - Command Specific Status Values, I/O Command Set Specific": Defines the status/error classification represented by Status Code - Command Specific Status Values, I/O Command Set Specific. Resolve the category before the individual code or flag; keep reserved values uninterpreted. Evidence index: ID, Command Set, Status Code, Command.

- Purpose: Defines the status/error classification represented by Status Code - Command Specific Status Values, I/O Command Set Specific.

- How to read: Resolve the category before the individual code or flag; keep reserved values uninterpreted. Evidence index: ID, Command Set, Status Code, Command.

- Conditions and limits: Source keyword index: `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: For one reported condition, identify ID first and then check Command Set instead of decoding an isolated numeric value. This example adds no requirement.

- Source field index: ID, Command Set, Status Code, Command

- Source keyword index: `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §4.2.3.2, Figure 105, printed pages 152-153, PDF pages 178-179

</details>

<details markdown="1">
<summary><strong>Figure 107: Status Code - Media and Data Integrity Error Values</strong></summary>

<!-- claim:BASE4-FIG-107-CLAIM figure-table:BASE4-FIG-107 -->

Figure 107, "Status Code - Media and Data Integrity Error Values": Defines the status/error classification represented by Status Code - Media and Data Integrity Error Values. Resolve the category before the individual code or flag; keep reserved values uninterpreted. Evidence index: TCG, SCT, Status Code.

- Purpose: Defines the status/error classification represented by Status Code - Media and Data Integrity Error Values.

- How to read: Resolve the category before the individual code or flag; keep reserved values uninterpreted. Evidence index: TCG, SCT, Status Code.

- Conditions and limits: Source keyword index: `should`, `may`, `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: For one reported condition, identify TCG first and then check SCT instead of decoding an isolated numeric value. This example adds no requirement.

- Source field index: TCG, SCT, Status Code

- Source keyword index: `should`, `may`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §4.2.3.2, Figure 107, printed pages 154-155, PDF pages 180-181

</details>

<details markdown="1">
<summary><strong>Figure 108: Status Code - Path Related Status Values</strong></summary>

<!-- claim:BASE4-FIG-108-CLAIM figure-table:BASE4-FIG-108 -->

Figure 108, "Status Code - Path Related Status Values": Defines the status/error classification represented by Status Code - Path Related Status Values. Resolve the category before the individual code or flag; keep reserved values uninterpreted. Evidence index: DNR, ANA, Status Code.

- Purpose: Defines the status/error classification represented by Status Code - Path Related Status Values.

- How to read: Resolve the category before the individual code or flag; keep reserved values uninterpreted. Evidence index: DNR, ANA, Status Code.

- Conditions and limits: Source keyword index: `should not`, `should`, `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: For one reported condition, identify DNR first and then check ANA instead of decoding an isolated numeric value. This example adds no requirement.

- Source field index: DNR, ANA, Status Code

- Source keyword index: `should not`, `should`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §4.2.3.3, Figure 108, printed pages 155, PDF pages 181

</details>

<details markdown="1">
<summary><strong>Figure 109: Phase Tag bit Transition Example</strong></summary>

<!-- claim:BASE4-FIG-109-CLAIM figure-table:BASE4-FIG-109 -->

Figure 109, "Phase Tag bit Transition Example": Shows the queue or command relationship expressed by Phase Tag bit Transition Example. Trace ownership and direction from host to SQ, controller, and CQ; keep the indexed elements distinct: Phase Tag.

- Purpose: Shows the queue or command relationship expressed by Phase Tag bit Transition Example.

- How to read: Trace ownership and direction from host to SQ, controller, and CQ; keep the indexed elements distinct: Phase Tag.

- Conditions and limits: The Figure is explanatory or structural; this guide does not turn its visual relationship into a new requirement.

- Informative example: Trace one command through Figure 109, using Phase Tag and the cited condition as checkpoints for ownership or pointer movement. This example adds no requirement.

- Source field index: Phase Tag

- Source keyword index: none

> Source: NVME-BASE-2.4, Rev. 2.4, §4.2.4, Figure 109, printed pages 156-157, PDF pages 182-183

</details>

<a id="section-4-3"></a>

### §4.3

<details markdown="1">
<summary><strong>Figure 110: PRP Entry Layout</strong></summary>

<!-- claim:BASE4-FIG-110-CLAIM figure-table:BASE4-FIG-110 -->

Figure 110, "PRP Entry Layout": Defines the concrete layout or value relationships for PRP Entry Layout. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is PRP.

- Purpose: Defines the concrete layout or value relationships for PRP Entry Layout.

- How to read: Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is PRP.

- Conditions and limits: The Figure is explanatory or structural; this guide does not turn its visual relationship into a new requirement.

- Informative example: Use PRP as the first parser checkpoint and the cited condition as a second, independent boundary check. This example adds no requirement.

- Source field index: PRP

- Source keyword index: none

> Source: NVME-BASE-2.4, Rev. 2.4, §4.3.1, Figure 110, printed pages 158, PDF pages 184

</details>

<details markdown="1">
<summary><strong>Figure 111: PRP Entry - Page Base Address and Offset</strong></summary>

<!-- claim:BASE4-FIG-111-CLAIM figure-table:BASE4-FIG-111 -->

Figure 111, "PRP Entry - Page Base Address and Offset": Shows how PRP Entry - Page Base Address and Offset maps a transfer onto host-memory locations. Follow address, length, page/segment boundaries, and the link to the next entry in order. Evidence index: PBAO, PRP.

- Purpose: Shows how PRP Entry - Page Base Address and Offset maps a transfer onto host-memory locations.

- How to read: Follow address, length, page/segment boundaries, and the link to the next entry in order. Evidence index: PBAO, PRP.

- Conditions and limits: Source keyword index: `shall`, `may`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Map a transfer beginning at PBAO, then verify the boundary or next element identified by PRP before continuing. This example adds no requirement.

- Source field index: PBAO, PRP

- Source keyword index: `shall`, `may`

> Source: NVME-BASE-2.4, Rev. 2.4, §4.3.1, Figure 111, printed pages 158, PDF pages 184

</details>

<details markdown="1">
<summary><strong>Figure 112: PRP List Layout for Physically Contiguous Memory Pages</strong></summary>

<!-- claim:BASE4-FIG-112-CLAIM figure-table:BASE4-FIG-112 -->

Figure 112, "PRP List Layout for Physically Contiguous Memory Pages": Defines the concrete layout or value relationships for PRP List Layout for Physically Contiguous Memory Pages. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is PRP, Memory Page.

- Purpose: Defines the concrete layout or value relationships for PRP List Layout for Physically Contiguous Memory Pages.

- How to read: Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is PRP, Memory Page.

- Conditions and limits: The Figure is explanatory or structural; this guide does not turn its visual relationship into a new requirement.

- Informative example: Use PRP as the first parser checkpoint and Memory Page as a second, independent boundary check. This example adds no requirement.

- Source field index: PRP, Memory Page

- Source keyword index: none

> Source: NVME-BASE-2.4, Rev. 2.4, §4.3.1, Figure 112, printed pages 159, PDF pages 185

</details>

<details markdown="1">
<summary><strong>Figure 113: PRP List Layout for Physically Non-Contiguous Memory Pages</strong></summary>

<!-- claim:BASE4-FIG-113-CLAIM figure-table:BASE4-FIG-113 -->

Figure 113, "PRP List Layout for Physically Non-Contiguous Memory Pages": Defines the concrete layout or value relationships for PRP List Layout for Physically Non-Contiguous Memory Pages. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is PRP, CC.MPS, Memory Page.

- Purpose: Defines the concrete layout or value relationships for PRP List Layout for Physically Non-Contiguous Memory Pages.

- How to read: Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is PRP, CC.MPS, Memory Page.

- Conditions and limits: Source keyword index: `shall`, `should`, `may`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Use PRP as the first parser checkpoint and CC.MPS as a second, independent boundary check. This example adds no requirement.

- Source field index: PRP, CC.MPS, Memory Page

- Source keyword index: `shall`, `should`, `may`

> Source: NVME-BASE-2.4, Rev. 2.4, §4.3.1, Figure 113, printed pages 159, PDF pages 185

</details>

<details markdown="1">
<summary><strong>Figure 114: SGL Validation Error Conditions</strong></summary>

<!-- claim:BASE4-FIG-114-CLAIM figure-table:BASE4-FIG-114 -->

Figure 114, "SGL Validation Error Conditions": Defines the status/error classification represented by SGL Validation Error Conditions. Resolve the category before the individual code or flag; keep reserved values uninterpreted. Evidence index: SGL.

- Purpose: Defines the status/error classification represented by SGL Validation Error Conditions.

- How to read: Resolve the category before the individual code or flag; keep reserved values uninterpreted. Evidence index: SGL.

- Conditions and limits: The Figure is explanatory or structural; this guide does not turn its visual relationship into a new requirement.

- Informative example: For one reported condition, identify SGL first and then check the cited condition instead of decoding an isolated numeric value. This example adds no requirement.

- Source field index: SGL

- Source keyword index: none

> Source: NVME-BASE-2.4, Rev. 2.4, §4.3.2, Figure 114, printed pages 161, PDF pages 187

</details>

<details markdown="1">
<summary><strong>Figure 115: SGL Segment</strong></summary>

<!-- claim:BASE4-FIG-115-CLAIM figure-table:BASE4-FIG-115 -->

Figure 115, "SGL Segment": Shows how SGL Segment maps a transfer onto host-memory locations. Follow address, length, page/segment boundaries, and the link to the next entry in order. Evidence index: SGL.

- Purpose: Shows how SGL Segment maps a transfer onto host-memory locations.

- How to read: Follow address, length, page/segment boundaries, and the link to the next entry in order. Evidence index: SGL.

- Conditions and limits: The Figure is explanatory or structural; this guide does not turn its visual relationship into a new requirement.

- Informative example: Map a transfer beginning at SGL, then verify the boundary or next element identified by the cited condition before continuing. This example adds no requirement.

- Source field index: SGL

- Source keyword index: none

> Source: NVME-BASE-2.4, Rev. 2.4, §4.3.2, Figure 115, printed pages 161, PDF pages 187

</details>

<details markdown="1">
<summary><strong>Figure 116: Generic SGL Descriptor Format</strong></summary>

<!-- claim:BASE4-FIG-116-CLAIM figure-table:BASE4-FIG-116 -->

Figure 116, "Generic SGL Descriptor Format": Defines the concrete layout or value relationships for Generic SGL Descriptor Format. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is DTS, SGLID, SGLDT, SGLDST, SGL, NULL.

- Purpose: Defines the concrete layout or value relationships for Generic SGL Descriptor Format.

- How to read: Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is DTS, SGLID, SGLDT, SGLDST, SGL, NULL.

- Conditions and limits: Source keyword index: `shall`, `may`, `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Use DTS as the first parser checkpoint and SGLID as a second, independent boundary check. This example adds no requirement.

- Source field index: DTS, SGLID, SGLDT, SGLDST, SGL, NULL

- Source keyword index: `shall`, `may`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §4.3.2, Figure 116, printed pages 161, PDF pages 187

</details>

<details markdown="1">
<summary><strong>Figure 117: SGL Descriptor Type</strong></summary>

<!-- claim:BASE4-FIG-117-CLAIM figure-table:BASE4-FIG-117 -->

Figure 117, "SGL Descriptor Type": Defines the concrete layout or value relationships for SGL Descriptor Type. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is SGL.

- Purpose: Defines the concrete layout or value relationships for SGL Descriptor Type.

- How to read: Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is SGL.

- Conditions and limits: Source keyword index: `reserved`. The index locates normative language but does not replace the condition attached to each field. Only the PCIe/memory-based portion is in scope.

- Informative example: Use SGL as the first parser checkpoint and the cited condition as a second, independent boundary check. This example adds no requirement.

- Source field index: SGL

- Source keyword index: `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §4.3.2, Figure 117, printed pages 161-162, PDF pages 187-188

</details>

<details markdown="1">
<summary><strong>Figure 118: SGL Descriptor Sub Type Values</strong></summary>

<!-- claim:BASE4-FIG-118-CLAIM figure-table:BASE4-FIG-118 -->

Figure 118, "SGL Descriptor Sub Type Values": Defines the concrete layout or value relationships for SGL Descriptor Sub Type Values. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is SGL.

- Purpose: Defines the concrete layout or value relationships for SGL Descriptor Sub Type Values.

- How to read: Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is SGL.

- Conditions and limits: Source keyword index: `shall`, `may`, `reserved`. The index locates normative language but does not replace the condition attached to each field. Only the PCIe/memory-based portion is in scope.

- Informative example: Use SGL as the first parser checkpoint and the cited condition as a second, independent boundary check. This example adds no requirement.

- Source field index: SGL

- Source keyword index: `shall`, `may`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §4.3.2, Figure 118, printed pages 162, PDF pages 188

</details>

<details markdown="1">
<summary><strong>Figure 119: SGL Data Block descriptor</strong></summary>

<!-- claim:BASE4-FIG-119-CLAIM figure-table:BASE4-FIG-119 -->

Figure 119, "SGL Data Block descriptor": Defines the concrete layout or value relationships for SGL Data Block descriptor. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is ADDR, LEN, SGLID, SGLDT, SGLDST, SGL, SGLS.

- Purpose: Defines the concrete layout or value relationships for SGL Data Block descriptor.

- How to read: Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is ADDR, LEN, SGLID, SGLDT, SGLDST, SGL, SGLS.

- Conditions and limits: Source keyword index: `shall`, `may`, `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Use ADDR as the first parser checkpoint and LEN as a second, independent boundary check. This example adds no requirement.

- Source field index: ADDR, LEN, SGLID, SGLDT, SGLDST, SGL, SGLS

- Source keyword index: `shall`, `may`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §4.3.2, Figure 119, printed pages 162-163, PDF pages 188-189

</details>

<details markdown="1">
<summary><strong>Figure 120: SGL Bit Bucket descriptor</strong></summary>

<!-- claim:BASE4-FIG-120-CLAIM figure-table:BASE4-FIG-120 -->

Figure 120, "SGL Bit Bucket descriptor": Defines the concrete layout or value relationships for SGL Bit Bucket descriptor. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is LEN, SGLID, SGLDT, SGLDST, SGL, NLB.

- Purpose: Defines the concrete layout or value relationships for SGL Bit Bucket descriptor.

- How to read: Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is LEN, SGLID, SGLDT, SGLDST, SGL, NLB.

- Conditions and limits: Source keyword index: `shall`, `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Use LEN as the first parser checkpoint and SGLID as a second, independent boundary check. This example adds no requirement.

- Source field index: LEN, SGLID, SGLDT, SGLDST, SGL, NLB

- Source keyword index: `shall`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §4.3.2, Figure 120, printed pages 163, PDF pages 189

</details>

<details markdown="1">
<summary><strong>Figure 121: SGL Segment descriptor</strong></summary>

<!-- claim:BASE4-FIG-121-CLAIM figure-table:BASE4-FIG-121 -->

Figure 121, "SGL Segment descriptor": Defines the concrete layout or value relationships for SGL Segment descriptor. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is ADDR, LEN, SGLID, SGLDT, SGDST, SGL.

- Purpose: Defines the concrete layout or value relationships for SGL Segment descriptor.

- How to read: Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is ADDR, LEN, SGLID, SGLDT, SGDST, SGL.

- Conditions and limits: Source keyword index: `shall`, `may`, `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Use ADDR as the first parser checkpoint and LEN as a second, independent boundary check. This example adds no requirement.

- Source field index: ADDR, LEN, SGLID, SGLDT, SGDST, SGL

- Source keyword index: `shall`, `may`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §4.3.2, Figure 121, printed pages 163, PDF pages 189

</details>

<details markdown="1">
<summary><strong>Figure 122: SGL Last Segment descriptor</strong></summary>

<!-- claim:BASE4-FIG-122-CLAIM figure-table:BASE4-FIG-122 -->

Figure 122, "SGL Last Segment descriptor": Defines the concrete layout or value relationships for SGL Last Segment descriptor. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is ADDR, LEN, SGLID, SGLDT, SGLDST, SGL.

- Purpose: Defines the concrete layout or value relationships for SGL Last Segment descriptor.

- How to read: Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is ADDR, LEN, SGLID, SGLDT, SGLDST, SGL.

- Conditions and limits: Source keyword index: `shall`, `may`, `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Use ADDR as the first parser checkpoint and LEN as a second, independent boundary check. This example adds no requirement.

- Source field index: ADDR, LEN, SGLID, SGLDT, SGLDST, SGL

- Source keyword index: `shall`, `may`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §4.3.2, Figure 122, printed pages 164, PDF pages 190

</details>

<details markdown="1">
<summary><strong>Figure 125: SGL Read Example</strong></summary>

<!-- claim:BASE4-FIG-125-CLAIM figure-table:BASE4-FIG-125 -->

Figure 125, "SGL Read Example": Shows how SGL Read Example maps a transfer onto host-memory locations. Follow address, length, page/segment boundaries, and the link to the next entry in order. Evidence index: SGL.

- Purpose: Shows how SGL Read Example maps a transfer onto host-memory locations.

- How to read: Follow address, length, page/segment boundaries, and the link to the next entry in order. Evidence index: SGL.

- Conditions and limits: The Figure is explanatory or structural; this guide does not turn its visual relationship into a new requirement.

- Informative example: Map a transfer beginning at SGL, then verify the boundary or next element identified by the cited condition before continuing. This example adds no requirement.

- Source field index: SGL

- Source keyword index: none

> Source: NVME-BASE-2.4, Rev. 2.4, §4.3.2.1, Figure 125, printed pages 166, PDF pages 192

</details>

<a id="section-4-4"></a>

### §4.4

<details markdown="1">
<summary><strong>Figure 126: Current Value after Reset with Scope of Entire NVM Subsystem</strong></summary>

<!-- claim:BASE4-FIG-126-CLAIM figure-table:BASE4-FIG-126 -->

Figure 126, "Current Value after Reset with Scope of Entire NVM Subsystem": Shows the object or capacity relationships in Current Value after Reset with Scope of Entire NVM Subsystem. Separate logical identifiers from controllers, namespaces, ports, and capacity containers. Evidence index: NVM Subsystem.

- Purpose: Shows the object or capacity relationships in Current Value after Reset with Scope of Entire NVM Subsystem.

- How to read: Separate logical identifiers from controllers, namespaces, ports, and capacity containers. Evidence index: NVM Subsystem.

- Conditions and limits: The Figure is explanatory or structural; this guide does not turn its visual relationship into a new requirement.

- Informative example: Choose one object labeled by NVM Subsystem and trace its relationship to the cited condition without treating an identifier as the object itself. This example adds no requirement.

- Source field index: NVM Subsystem

- Source keyword index: none

> Source: NVME-BASE-2.4, Rev. 2.4, §4.4, Figure 126, printed pages 167, PDF pages 193

</details>

<details markdown="1">
<summary><strong>Figure 127: Current Value after Reset with Scope of Subset of the NVM Subsystem</strong></summary>

<!-- claim:BASE4-FIG-127-CLAIM figure-table:BASE4-FIG-127 -->

Figure 127, "Current Value after Reset with Scope of Subset of the NVM Subsystem": Shows the object or capacity relationships in Current Value after Reset with Scope of Subset of the NVM Subsystem. Separate logical identifiers from controllers, namespaces, ports, and capacity containers. Evidence index: NVM Subsystem.

- Purpose: Shows the object or capacity relationships in Current Value after Reset with Scope of Subset of the NVM Subsystem.

- How to read: Separate logical identifiers from controllers, namespaces, ports, and capacity containers. Evidence index: NVM Subsystem.

- Conditions and limits: The Figure is explanatory or structural; this guide does not turn its visual relationship into a new requirement.

- Informative example: Choose one object labeled by NVM Subsystem and trace its relationship to the cited condition without treating an identifier as the object itself. This example adds no requirement.

- Source field index: NVM Subsystem

- Source keyword index: none

> Source: NVME-BASE-2.4, Rev. 2.4, §4.4, Figure 127, printed pages 168, PDF pages 194

</details>

<a id="section-4-5"></a>

### §4.5

<details markdown="1">
<summary><strong>Figure 128: PCI Vendor ID (VID) and PCI Subsystem Vendor ID (SSVID)</strong></summary>

<!-- claim:BASE4-FIG-128-CLAIM figure-table:BASE4-FIG-128 -->

Figure 128, "PCI Vendor ID (VID) and PCI Subsystem Vendor ID (SSVID)": Shows the object or capacity relationships in PCI Vendor ID (VID) and PCI Subsystem Vendor ID (SSVID). Separate logical identifiers from controllers, namespaces, ports, and capacity containers. Evidence index: ID, VID, SSVID.

- Purpose: Shows the object or capacity relationships in PCI Vendor ID (VID) and PCI Subsystem Vendor ID (SSVID).

- How to read: Separate logical identifiers from controllers, namespaces, ports, and capacity containers. Evidence index: ID, VID, SSVID.

- Conditions and limits: The Figure is explanatory or structural; this guide does not turn its visual relationship into a new requirement.

- Informative example: Choose one object labeled by ID and trace its relationship to VID without treating an identifier as the object itself. This example adds no requirement.

- Source field index: ID, VID, SSVID

- Source keyword index: none

> Source: NVME-BASE-2.4, Rev. 2.4, §4.5.1, Figure 128, printed pages 169, PDF pages 195

</details>

<details markdown="1">
<summary><strong>Figure 129: Serial Number (SN) and Model Number (MN)</strong></summary>

<!-- claim:BASE4-FIG-129-CLAIM figure-table:BASE4-FIG-129 -->

Figure 129, "Serial Number (SN) and Model Number (MN)": Defines the identifier composition or namespace of values shown by Serial Number (SN) and Model Number (MN). Keep the value width, issuing authority, uniqueness scope, and reserved values separate. Evidence index: SN, MN.

- Purpose: Defines the identifier composition or namespace of values shown by Serial Number (SN) and Model Number (MN).

- How to read: Keep the value width, issuing authority, uniqueness scope, and reserved values separate. Evidence index: SN, MN.

- Conditions and limits: The Figure is explanatory or structural; this guide does not turn its visual relationship into a new requirement.

- Informative example: Parse SN at its defined width, then validate the scope associated with MN before using it as an identity key. This example adds no requirement.

- Source field index: SN, MN

- Source keyword index: none

> Source: NVME-BASE-2.4, Rev. 2.4, §4.5.2, Figure 129, printed pages 170, PDF pages 196

</details>

<details markdown="1">
<summary><strong>Figure 130: IEEE OUI Identifier (IEEE)</strong></summary>

<!-- claim:BASE4-FIG-130-CLAIM figure-table:BASE4-FIG-130 -->

Figure 130, "IEEE OUI Identifier (IEEE)": Defines the identifier composition or namespace of values shown by IEEE OUI Identifier (IEEE). Keep the value width, issuing authority, uniqueness scope, and reserved values separate. Evidence index: IEEE, OUI.

- Purpose: Defines the identifier composition or namespace of values shown by IEEE OUI Identifier (IEEE).

- How to read: Keep the value width, issuing authority, uniqueness scope, and reserved values separate. Evidence index: IEEE, OUI.

- Conditions and limits: The Figure is explanatory or structural; this guide does not turn its visual relationship into a new requirement.

- Informative example: Parse IEEE at its defined width, then validate the scope associated with OUI before using it as an identity key. This example adds no requirement.

- Source field index: IEEE, OUI

- Source keyword index: none

> Source: NVME-BASE-2.4, Rev. 2.4, §4.5.3, Figure 130, printed pages 170, PDF pages 196

</details>

<details markdown="1">
<summary><strong>Figure 131: IEEE Extended Unique Identifier (EUI64), MA-L Format</strong></summary>

<!-- claim:BASE4-FIG-131-CLAIM figure-table:BASE4-FIG-131 -->

Figure 131, "IEEE Extended Unique Identifier (EUI64), MA-L Format": Defines the concrete layout or value relationships for IEEE Extended Unique Identifier (EUI64), MA-L Format. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is IEEE, EUI64, MA, EUI, OUI.

- Purpose: Defines the concrete layout or value relationships for IEEE Extended Unique Identifier (EUI64), MA-L Format.

- How to read: Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is IEEE, EUI64, MA, EUI, OUI.

- Conditions and limits: The Figure is explanatory or structural; this guide does not turn its visual relationship into a new requirement.

- Informative example: Use IEEE as the first parser checkpoint and EUI64 as a second, independent boundary check. This example adds no requirement.

- Source field index: IEEE, EUI64, MA, EUI, OUI

- Source keyword index: none

> Source: NVME-BASE-2.4, Rev. 2.4, §4.5.4, Figure 131, printed pages 170, PDF pages 196

</details>

<details markdown="1">
<summary><strong>Figure 132: IEEE Extended Unique Identifier (EUI64), OUI Identifier</strong></summary>

<!-- claim:BASE4-FIG-132-CLAIM figure-table:BASE4-FIG-132 -->

Figure 132, "IEEE Extended Unique Identifier (EUI64), OUI Identifier": Defines the identifier composition or namespace of values shown by IEEE Extended Unique Identifier (EUI64), OUI Identifier. Keep the value width, issuing authority, uniqueness scope, and reserved values separate. Evidence index: IEEE, EUI64, OUI.

- Purpose: Defines the identifier composition or namespace of values shown by IEEE Extended Unique Identifier (EUI64), OUI Identifier.

- How to read: Keep the value width, issuing authority, uniqueness scope, and reserved values separate. Evidence index: IEEE, EUI64, OUI.

- Conditions and limits: The Figure is explanatory or structural; this guide does not turn its visual relationship into a new requirement.

- Informative example: Parse IEEE at its defined width, then validate the scope associated with EUI64 before using it as an identity key. This example adds no requirement.

- Source field index: IEEE, EUI64, OUI

- Source keyword index: none

> Source: NVME-BASE-2.4, Rev. 2.4, §4.5.4, Figure 132, printed pages 170, PDF pages 196

</details>

<details markdown="1">
<summary><strong>Figure 133: IEEE Extended Unique Identifier (EUI64), Ext. ID (cont)</strong></summary>

<!-- claim:BASE4-FIG-133-CLAIM figure-table:BASE4-FIG-133 -->

Figure 133, "IEEE Extended Unique Identifier (EUI64), Ext. ID (cont)": Defines the identifier composition or namespace of values shown by IEEE Extended Unique Identifier (EUI64), Ext. ID (cont). Keep the value width, issuing authority, uniqueness scope, and reserved values separate. Evidence index: IEEE, EUI64, ID, MA, WWN, NAA.

- Purpose: Defines the identifier composition or namespace of values shown by IEEE Extended Unique Identifier (EUI64), Ext. ID (cont).

- How to read: Keep the value width, issuing authority, uniqueness scope, and reserved values separate. Evidence index: IEEE, EUI64, ID, MA, WWN, NAA.

- Conditions and limits: The Figure is explanatory or structural; this guide does not turn its visual relationship into a new requirement.

- Informative example: Parse IEEE at its defined width, then validate the scope associated with EUI64 before using it as an identity key. This example adds no requirement.

- Source field index: IEEE, EUI64, ID, MA, WWN, NAA

- Source keyword index: none

> Source: NVME-BASE-2.4, Rev. 2.4, §4.5.4, Figure 133, printed pages 170-171, PDF pages 196-197

</details>

<details markdown="1">
<summary><strong>Figure 134: MA-L similarity to WWN</strong></summary>

<!-- claim:BASE4-FIG-134-CLAIM figure-table:BASE4-FIG-134 -->

Figure 134, "MA-L similarity to WWN": Defines the identifier composition or namespace of values shown by MA-L similarity to WWN. Keep the value width, issuing authority, uniqueness scope, and reserved values separate. Evidence index: MA, WWN.

- Purpose: Defines the identifier composition or namespace of values shown by MA-L similarity to WWN.

- How to read: Keep the value width, issuing authority, uniqueness scope, and reserved values separate. Evidence index: MA, WWN.

- Conditions and limits: The Figure is explanatory or structural; this guide does not turn its visual relationship into a new requirement.

- Informative example: Parse MA at its defined width, then validate the scope associated with WWN before using it as an identity key. This example adds no requirement.

- Source field index: MA, WWN

- Source keyword index: none

> Source: NVME-BASE-2.4, Rev. 2.4, §4.5.4, Figure 134, printed pages 171, PDF pages 197

</details>

<details markdown="1">
<summary><strong>Figure 135: Namespace Globally Unique Identifier (NGUID)</strong></summary>

<!-- claim:BASE4-FIG-135-CLAIM figure-table:BASE4-FIG-135 -->

Figure 135, "Namespace Globally Unique Identifier (NGUID)": Defines the identifier composition or namespace of values shown by Namespace Globally Unique Identifier (NGUID). Keep the value width, issuing authority, uniqueness scope, and reserved values separate. Evidence index: NGUID, Namespace.

- Purpose: Defines the identifier composition or namespace of values shown by Namespace Globally Unique Identifier (NGUID).

- How to read: Keep the value width, issuing authority, uniqueness scope, and reserved values separate. Evidence index: NGUID, Namespace.

- Conditions and limits: The Figure is explanatory or structural; this guide does not turn its visual relationship into a new requirement.

- Informative example: Parse NGUID at its defined width, then validate the scope associated with Namespace before using it as an identity key. This example adds no requirement.

- Source field index: NGUID, Namespace

- Source keyword index: none

> Source: NVME-BASE-2.4, Rev. 2.4, §4.5.5, Figure 135, printed pages 171, PDF pages 197

</details>

<details markdown="1">
<summary><strong>Figure 136: Namespace Globally Unique Identifier (NGUID), OUI</strong></summary>

<!-- claim:BASE4-FIG-136-CLAIM figure-table:BASE4-FIG-136 -->

Figure 136, "Namespace Globally Unique Identifier (NGUID), OUI": Defines the identifier composition or namespace of values shown by Namespace Globally Unique Identifier (NGUID), OUI. Keep the value width, issuing authority, uniqueness scope, and reserved values separate. Evidence index: NGUID, OUI, VSP, ID, Namespace.

- Purpose: Defines the identifier composition or namespace of values shown by Namespace Globally Unique Identifier (NGUID), OUI.

- How to read: Keep the value width, issuing authority, uniqueness scope, and reserved values separate. Evidence index: NGUID, OUI, VSP, ID, Namespace.

- Conditions and limits: The Figure is explanatory or structural; this guide does not turn its visual relationship into a new requirement.

- Informative example: Parse NGUID at its defined width, then validate the scope associated with OUI before using it as an identity key. This example adds no requirement.

- Source field index: NGUID, OUI, VSP, ID, Namespace

- Source keyword index: none

> Source: NVME-BASE-2.4, Rev. 2.4, §4.5.5, Figure 136, printed pages 171, PDF pages 197

</details>

<details markdown="1">
<summary><strong>Figure 137: Namespace Globally Unique Identifier</strong></summary>

<!-- claim:BASE4-FIG-137-CLAIM figure-table:BASE4-FIG-137 -->

Figure 137, "Namespace Globally Unique Identifier": Defines the identifier composition or namespace of values shown by Namespace Globally Unique Identifier. Keep the value width, issuing authority, uniqueness scope, and reserved values separate. Evidence index: NGUID, WWN, IEEE, NAA, Namespace.

- Purpose: Defines the identifier composition or namespace of values shown by Namespace Globally Unique Identifier.

- How to read: Keep the value width, issuing authority, uniqueness scope, and reserved values separate. Evidence index: NGUID, WWN, IEEE, NAA, Namespace.

- Conditions and limits: The Figure is explanatory or structural; this guide does not turn its visual relationship into a new requirement.

- Informative example: Parse NGUID at its defined width, then validate the scope associated with WWN before using it as an identity key. This example adds no requirement.

- Source field index: NGUID, WWN, IEEE, NAA, Namespace

- Source keyword index: none

> Source: NVME-BASE-2.4, Rev. 2.4, §4.5.5, Figure 137, printed pages 171, PDF pages 197

</details>

<details markdown="1">
<summary><strong>Figure 138: Namespace Globally Unique Identifier (NGUID), NGUID similarity to WWN</strong></summary>

<!-- claim:BASE4-FIG-138-CLAIM figure-table:BASE4-FIG-138 -->

Figure 138, "Namespace Globally Unique Identifier (NGUID), NGUID similarity to WWN": Defines the identifier composition or namespace of values shown by Namespace Globally Unique Identifier (NGUID), NGUID similarity to WWN. Keep the value width, issuing authority, uniqueness scope, and reserved values separate. Evidence index: NGUID, WWN, OUI, NAA, Namespace.

- Purpose: Defines the identifier composition or namespace of values shown by Namespace Globally Unique Identifier (NGUID), NGUID similarity to WWN.

- How to read: Keep the value width, issuing authority, uniqueness scope, and reserved values separate. Evidence index: NGUID, WWN, OUI, NAA, Namespace.

- Conditions and limits: The Figure is explanatory or structural; this guide does not turn its visual relationship into a new requirement.

- Informative example: Parse NGUID at its defined width, then validate the scope associated with WWN before using it as an identity key. This example adds no requirement.

- Source field index: NGUID, WWN, OUI, NAA, Namespace

- Source keyword index: none

> Source: NVME-BASE-2.4, Rev. 2.4, §4.5.5, Figure 138, printed pages 171, PDF pages 197

</details>

<a id="section-4-6"></a>

### §4.6

<details markdown="1">
<summary><strong>Figure 139: Controller List Format</strong></summary>

<!-- claim:BASE4-FIG-139-CLAIM figure-table:BASE4-FIG-139 -->

Figure 139, "Controller List Format": Defines the concrete layout or value relationships for Controller List Format. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is NUMCIDS, Controller.

- Purpose: Defines the concrete layout or value relationships for Controller List Format.

- How to read: Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is NUMCIDS, Controller.

- Conditions and limits: Source keyword index: `may`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Use NUMCIDS as the first parser checkpoint and Controller as a second, independent boundary check. This example adds no requirement.

- Source field index: NUMCIDS, Controller

- Source keyword index: `may`

> Source: NVME-BASE-2.4, Rev. 2.4, §4.6.1, Figure 139, printed pages 172, PDF pages 198

</details>

<details markdown="1">
<summary><strong>Figure 140: Namespace List Format</strong></summary>

<!-- claim:BASE4-FIG-140-CLAIM figure-table:BASE4-FIG-140 -->

Figure 140, "Namespace List Format": Defines the concrete layout or value relationships for Namespace List Format. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is ID, Namespace.

- Purpose: Defines the concrete layout or value relationships for Namespace List Format.

- How to read: Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is ID, Namespace.

- Conditions and limits: The Figure is explanatory or structural; this guide does not turn its visual relationship into a new requirement.

- Informative example: Use ID as the first parser checkpoint and Namespace as a second, independent boundary check. This example adds no requirement.

- Source field index: ID, Namespace

- Source keyword index: none

> Source: NVME-BASE-2.4, Rev. 2.4, §4.6.2, Figure 140, printed pages 172, PDF pages 198

</details>

<a id="section-4-8"></a>

### §4.8

<details markdown="1">
<summary><strong>Figure 142: UTF-8 Input Processing</strong></summary>

<!-- claim:BASE4-FIG-142-CLAIM figure-table:BASE4-FIG-142 -->

Figure 142, "UTF-8 Input Processing": Shows the input-validation sequence required by UTF-8 Input Processing. Follow decoding, prohibited-code-point, and truncation checks in order. Evidence index: UTF.

- Purpose: Shows the input-validation sequence required by UTF-8 Input Processing.

- How to read: Follow decoding, prohibited-code-point, and truncation checks in order. Evidence index: UTF.

- Conditions and limits: The Figure is explanatory or structural; this guide does not turn its visual relationship into a new requirement.

- Informative example: Validate UTF first and reject the input if the check associated with the cited condition fails before accepting the string. This example adds no requirement.

- Source field index: UTF

- Source keyword index: none

> Source: NVME-BASE-2.4, Rev. 2.4, §4.8, Figure 142, printed pages 175, PDF pages 201

</details>

## Use and limitations

Use the claim IDs as stable PPT traceability keys. Re-check affected claims if the source revision, errata set, or approved scope changes.
