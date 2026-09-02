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

## Acronyms first: complete glossary

Every abbreviation below is introduced before it is used in the slide narrative. The term alone is never enough: retain owner, width, unit, scope, and state.

| Acronym / term | Plain-language meaning | Source |
|---|---|---|
| `SQE` | Submission Queue Entry, one command structure in an SQ. | NVME-BASE-2.4 Rev. 2.4, §4.1.1, printed pp. 139-143, PDF pp. 165-169 |
| `CQE` | Completion Queue Entry, one completion-result structure in a CQ. | NVME-BASE-2.4 Rev. 2.4, §4.2.1, printed pp. 144-145, PDF pp. 170-171 |
| `CDW` | Command Dword, a 32-bit numbered command field in an SQE. | NVME-BASE-2.4 Rev. 2.4, §4.1.1, printed pp. 139-143, PDF pp. 165-169 |
| `CID` | Command Identifier, used with the SQ identifier to identify an outstanding command. | NVME-BASE-2.4 Rev. 2.4, §4.1.1, printed pp. 140, PDF pp. 166 |
| `SQID` | Submission Queue Identifier, the numeric identifier of the SQ containing a command. | NVME-BASE-2.4 Rev. 2.4, §4.1.1, printed pp. 140, PDF pp. 166 |
| `NSID` | Namespace Identifier, a controller-visible numeric handle for a namespace; the identifier is not the namespace object itself. | NVME-BASE-2.4 Rev. 2.4, §4.1.1, printed pp. 139-143, PDF pp. 165-169 |
| `PSDT` | PRP or SGL for Data Transfer, the CDW0 field selecting PRP or SGL interpretation for DPTR. | NVME-BASE-2.4 Rev. 2.4, §4.1.1, printed pp. 140-142, PDF pp. 166-168 |
| `DPTR` | Data Pointer, the SQE field identifying a command data buffer. | NVME-BASE-2.4 Rev. 2.4, §4.1.1, printed pp. 140-142, PDF pp. 166-168 |
| `MPTR` | Metadata Pointer, the SQE field identifying a separate metadata buffer. | NVME-BASE-2.4 Rev. 2.4, §4.1.1, printed pp. 139-143, PDF pp. 165-169 |
| `PRP` | Physical Region Page, a pointer format describing a host-addressable data buffer in memory-page units. | NVME-BASE-2.4 Rev. 2.4, §4.3.1, printed pp. 158-159, PDF pp. 184-185 |
| `SGL` | Scatter Gather List, a descriptor-and-segment format for one or more data-buffer regions. | NVME-BASE-2.4 Rev. 2.4, §4.3.2, printed pp. 159-166, PDF pp. 185-192 |
| `SCT` | Status Code Type, the category selected before interpreting SC. | NVME-BASE-2.4 Rev. 2.4, §4.2.3, printed pp. 145-155, PDF pp. 171-181 |
| `SC` | Status Code, the specific completion result interpreted in the context of SCT. | NVME-BASE-2.4 Rev. 2.4, §4.2.3, printed pp. 145-155, PDF pp. 171-181 |
| `DNR` | Do Not Retry, a CQE-status bit indicating that retrying the same command is not expected to succeed. | NVME-BASE-2.4 Rev. 2.4, §4.2.3, printed pp. 145-155, PDF pp. 171-181 |
| `CRD` | Command Retry Delay, the status field selecting a controller-recommended retry delay. | NVME-BASE-2.4 Rev. 2.4, §4.2.3, printed pp. 145-155, PDF pp. 171-181 |
| `P` | Phase Tag, the toggling bit used by the host to decide whether a CQ slot contains a new completion. | NVME-BASE-2.4 Rev. 2.4, §4.2.4, printed pp. 155-158, PDF pp. 181-184 |
| `PBAO` | Page Base Address and Offset, the first-PRP layout combining a page base address with an in-page offset. | NVME-BASE-2.4 Rev. 2.4, §4.3.1, printed pp. 158-159, PDF pp. 184-185 |
| `VID` | Vendor ID, a PCI-SIG-assigned identifier for a vendor. | NVME-BASE-2.4 Rev. 2.4, §4.5, printed pp. 169-172, PDF pp. 195-198 |
| `SSVID` | Subsystem Vendor ID, the PCI identifier for a subsystem vendor. | NVME-BASE-2.4 Rev. 2.4, §4.5, printed pp. 169-172, PDF pp. 195-198 |
| `SN` | Serial Number, a string identifying a product instance. | NVME-BASE-2.4 Rev. 2.4, §4.5, printed pp. 169-172, PDF pp. 195-198 |
| `MN` | Model Number, a string identifying a product model. | NVME-BASE-2.4 Rev. 2.4, §4.5, printed pp. 169-172, PDF pp. 195-198 |
| `OUI` | Organizationally Unique Identifier, an IEEE-assigned identifier prefix for an organization. | NVME-BASE-2.4 Rev. 2.4, §4.5, printed pp. 169-172, PDF pp. 195-198 |
| `EUI64` | 64-bit Extended Unique Identifier, a 64-bit identifier constructed from IEEE-assigned space. | NVME-BASE-2.4 Rev. 2.4, §4.5, printed pp. 169-172, PDF pp. 195-198 |
| `NGUID` | Namespace Globally Unique Identifier, a 128-bit global identifier for a namespace. | NVME-BASE-2.4 Rev. 2.4, §4.5, printed pp. 169-172, PDF pp. 195-198 |
| `UUID` | Universally Unique Identifier, a 128-bit identifier whose association scope is defined by the containing structure. | NVME-BASE-2.4 Rev. 2.4, §4.5, printed pp. 169-172, PDF pp. 195-198 |
| `NAA` | Network Address Authority, the WWN nibble selecting an identifier format and assignment method. | NVME-BASE-2.4 Rev. 2.4, §4.5, printed pp. 169-172, PDF pp. 195-198 |
| `WWN` | World Wide Name, a global naming format used for storage and networking devices. | NVME-BASE-2.4 Rev. 2.4, §4.5, printed pp. 169-172, PDF pp. 195-198 |
| `UTF-8` | Unicode Transformation Format - 8-bit, a text encoding that represents a Unicode code point with one to four bytes. | NVME-BASE-2.4 Rev. 2.4, §4.8, printed pp. 175, PDF pp. 201 |

## Visual atlas: locate the system before reading fields

Each redraw answers a different question: architecture locates components, sequence shows ownership, decode turns bits into engineering values, and state views preserve failure evidence. These are teaching redraws, not copies of specification artwork.

### Visual 01: Fix the 64-byte SQE skeleton before applying command-specific fields

**View type:** `decode`

```text
[RAW: Clear 64-byte SQE] → [LOCATE: Fill CDW0: OPC/CID/PSDT] → [DECODE: Fill NSID for command]
[VALIDATE: Build MPTR/DPTR] → [APPLY: Fill CDW10-15] → [EVIDENCE: Submit last]
VALIDATE fail ──→ return to RAW evidence
```

**Question answered:** The common SQE fixes the locations of CDW0, NSID, metadata/data pointers, and CDW10-15. OPC selects the command, CID creates the completion association, and PSDT selects DPTR interpretation. Only after these common fields are established should command-specific CDW10-15 definitions be applied. Figures 92-94 are the coordinate system for all later command construction.

**Supporting Figures:** Figure 92, Figure 93, Figure 94

**Sources:** NVME-BASE-2.4 Rev. 2.4, §4.1.1, printed pp. 139-143, PDF pp. 165-169; NVME-BASE-2.4 Rev. 2.4, §4.1.1, printed pp. 140, PDF pp. 166; NVME-BASE-2.4 Rev. 2.4, §4.1.1, printed pp. 140-142, PDF pp. 166-168

### Visual 02: Decode CQE ownership first, identity second, and status last

**View type:** `decode`

```text
[RAW: Check Phase Tag] → [LOCATE: Read SQHD/SQID/CID] → [DECODE: Recover command by SQID/CID]
[VALIDATE: Decode SCT] → [APPLY: Decode SC/DNR/CRD] → [EVIDENCE: Advance CQ head]
VALIDATE fail ──→ return to RAW evidence
```

**Question answered:** The host first uses the Phase Tag to determine whether a CQ slot contains a new completion. After ownership is established, SQID/CID recovers the command; SCT then selects the status category before SC, DNR, and CRD are interpreted. Figures 97-109 must be read in this order so a stale CQE or wrong category is not mistaken for a command failure.

**Supporting Figures:** Figure 97, Figure 98, Figure 99, Figure 101, Figure 102, Figure 103, Figure 104, Figure 105, Figure 107, Figure 108, Figure 109

**Sources:** NVME-BASE-2.4 Rev. 2.4, §4.2.1, printed pp. 144-145, PDF pp. 170-171; NVME-BASE-2.4 Rev. 2.4, §4.2.3, printed pp. 145-155, PDF pp. 171-181; NVME-BASE-2.4 Rev. 2.4, §4.2.4, printed pp. 155-158, PDF pp. 181-184

### Visual 03: PRP calculation: the first page may have an offset; later entries return to page boundaries

**View type:** `decode`

```text
[RAW: Obtain MPS/page size] → [LOCATE: Compute PRP1 page offset] → [DECODE: Compute bytes available in first …]
[VALIDATE: Compute remaining bytes] → [APPLY: Choose PRP2 page or list] → [EVIDENCE: Validate later-page alignment]
VALIDATE fail ──→ return to RAW evidence
```

**Question answered:** PRP1 may address any byte within the first memory page, so first-segment capacity is page_size minus offset. If data crosses that page, PRP2 represents either the second page or a PRP List depending on remaining length; later page addresses must be page aligned. Figures 110-113 define address calculation, not merely pointer names.

**Supporting Figures:** Figure 110, Figure 111, Figure 112, Figure 113

**Sources:** NVME-BASE-2.4 Rev. 2.4, §4.3.1, printed pp. 158-159, PDF pp. 184-185; NVME-BASE-2.4 Rev. 2.4, §4.1.1, printed pp. 140-142, PDF pp. 166-168

### Visual 04: An SGL is a typed descriptor chain, not another PRP List

**View type:** `decode`

```text
[RAW: Select SGL through PSDT] → [LOCATE: Read descriptor type/subtype] → [DECODE: Validate length]
[VALIDATE: For data: add interval] → [APPLY: For segment: walk descriptors] → [EVIDENCE: Stop at Last Segment]
VALIDATE fail ──→ return to RAW evidence
```

**Question answered:** An SGL descriptor combines type/subtype, address, and length. A Data Block addresses data, Segment and Last Segment address more descriptors, and Bit Bucket represents data that need not be stored in memory. Figures 114-125 require type-first decoding; blindly following an address before decoding type is incorrect.

**Supporting Figures:** Figure 114, Figure 115, Figure 116, Figure 117, Figure 118, Figure 119, Figure 120, Figure 121, Figure 122, Figure 125

**Sources:** NVME-BASE-2.4 Rev. 2.4, §4.3.2, printed pp. 159-166, PDF pp. 185-192; NVME-BASE-2.4 Rev. 2.4, §4.1.1, printed pp. 140-142, PDF pp. 166-168

### Visual 05: Features, identifiers, lists, and UTF-8 all require scope validation

**View type:** `decode`

```text
[RAW: Identify data kind] → [LOCATE: Obtain width/count] → [DECODE: Confirm authority/scope]
[VALIDATE: Validate reserved/padding] → [APPLY: Build a stable comparison key] → [EVIDENCE: evidence]
VALIDATE fail ──→ return to RAW evidence
```

**Question answered:** Feature current/default/saved values define time and persistence scope; VID, SN, EUI64, NGUID, and UUID define identity scope; Controller/Namespace Lists define count and array boundaries; UTF-8 defines byte-sequence and code-point boundaries. Figures 126-142 appear diverse but share one parser rule: never interpret a value without its scope.

**Supporting Figures:** Figure 126, Figure 127, Figure 128, Figure 129, Figure 130, Figure 131, Figure 132, Figure 133, Figure 134, Figure 135, Figure 136, Figure 137, Figure 138, Figure 139, Figure 140, Figure 142

**Sources:** NVME-BASE-2.4 Rev. 2.4, §4.4, printed pp. 166-169, PDF pp. 192-195; NVME-BASE-2.4 Rev. 2.4, §4.5, printed pp. 169-172, PDF pp. 195-198; NVME-BASE-2.4 Rev. 2.4, §4.6, printed pp. 172-173, PDF pp. 198-199; NVME-BASE-2.4 Rev. 2.4, §4.8, printed pp. 175, PDF pp. 201

## Mental Model and complete teaching path

The modules follow engineering causality rather than specification-section order. Related Figures return at the point where they support the flow.

### Module 01: Fix the 64-byte SQE skeleton before applying command-specific fields

**Explanation.** The common SQE fixes the locations of CDW0, NSID, metadata/data pointers, and CDW10-15. OPC selects the command, CID creates the completion association, and PSDT selects DPTR interpretation. Only after these common fields are established should command-specific CDW10-15 definitions be applied. Figures 92-94 are the coordinate system for all later command construction.

```text
Clear 64-byte SQE
  ↓
Fill CDW0: OPC/CID/PSDT
  ↓
Fill NSID for command
  ↓
Build MPTR/DPTR
  ↓
Fill CDW10-15
  ↓
Submit last
```

#### Comparison

| Item | What it answers | Engineering note |
|---|---|---|
| CDW0 | Command identity and data-pointer selector | Common to all commands |
| NSID | Namespace scope | When unused, clear or use a special value only as the command defines |
| MPTR/DPTR | Metadata and data buffers | Selected by PSDT and command rules |
| CDW10-15 | Command-specific payload | Never borrow semantics from another command |

**Informative example.** Informative example: the same CID can be used on different SQs, but outstanding commands within one SQ must not create an identity collision. The driver tracks commands by (SQID,CID), completes every SQE field and required memory ordering, and only then updates the SQ tail.

**Common mistake / debugging.** Retain the raw 64-byte SQE dump together with decoded fields. A high-level command object alone cannot expose bit shifts, endian defects, uncleared reserved bits, or an incorrect PSDT.

**Supporting sources:** NVME-BASE-2.4 Rev. 2.4, §4.1.1, printed pp. 139-143, PDF pp. 165-169; NVME-BASE-2.4 Rev. 2.4, §4.1.1, printed pp. 140, PDF pp. 166; NVME-BASE-2.4 Rev. 2.4, §4.1.1, printed pp. 140-142, PDF pp. 166-168

**Related Figures:** Figure 92, Figure 93, Figure 94

### Module 02: Decode CQE ownership first, identity second, and status last

**Explanation.** The host first uses the Phase Tag to determine whether a CQ slot contains a new completion. After ownership is established, SQID/CID recovers the command; SCT then selects the status category before SC, DNR, and CRD are interpreted. Figures 97-109 must be read in this order so a stale CQE or wrong category is not mistaken for a command failure.

```text
Check Phase Tag
  ↓
Read SQHD/SQID/CID
  ↓
Recover command by SQID/CID
  ↓
Decode SCT
  ↓
Decode SC/DNR/CRD
  ↓
Advance CQ head
```

#### Comparison

| Item | What it answers | Engineering note |
|---|---|---|
| SCT | Status category | Always decode first |
| SC | Specific result within the category | Never interpret without SCT |
| DNR | Expectation for retrying the same command | Not synonymous with permanent hardware failure |
| CRD | Recommended retry-delay selector | Use only for an applicable status |

**Informative example.** Informative example: SC value 02h can belong to different status tables under different SCT values. A correct log retains the complete status field and reports P, SCT, SC, DNR, CRD, and the raw 16-bit value. 'SC=2' alone is insufficient for recovery.

**Common mistake / debugging.** CQ-wrap defects commonly appear as duplicate completions or commands that never complete. Compare producer/consumer expected phase, the CQ-head doorbell, and raw DW3 for each slot; do not act on other CQE fields before validating the Phase Tag.

**Supporting sources:** NVME-BASE-2.4 Rev. 2.4, §4.2.1, printed pp. 144-145, PDF pp. 170-171; NVME-BASE-2.4 Rev. 2.4, §4.2.3, printed pp. 145-155, PDF pp. 171-181; NVME-BASE-2.4 Rev. 2.4, §4.2.4, printed pp. 155-158, PDF pp. 181-184

**Related Figures:** Figure 97, Figure 98, Figure 99, Figure 101, Figure 102, Figure 103, Figure 104, Figure 105, Figure 107, Figure 108, Figure 109

### Module 03: PRP calculation: the first page may have an offset; later entries return to page boundaries

**Explanation.** PRP1 may address any byte within the first memory page, so first-segment capacity is page_size minus offset. If data crosses that page, PRP2 represents either the second page or a PRP List depending on remaining length; later page addresses must be page aligned. Figures 110-113 define address calculation, not merely pointer names.

```text
Obtain MPS/page size
  ↓
Compute PRP1 page offset
  ↓
Compute bytes available in first page
  ↓
Compute remaining bytes
  ↓
Choose PRP2 page or list
  ↓
Validate later-page alignment
```

#### Comparison

| Item | What it answers | Engineering note |
|---|---|---|
| Data stays in first page | PRP1 is sufficient | PRP2 does not carry another segment |
| Remaining data fits one page | PRP2 addresses the second data page | Address is page aligned |
| Remaining data exceeds one page | PRP2 addresses a PRP List | List entries address data pages |

**Informative example.** Informative example: with a 4096-byte page, PRP1 offset 1000, and a 9000-byte transfer, the first page carries 4096-1000=3096 bytes. The remaining 5904 bytes require two later pages, so PRP2 addresses a PRP List containing at least two data-page addresses.

**Common mistake / debugging.** A PRP debug dump should include MPS, transfer length, PRP1 offset, each physical address, and the byte interval covered by each entry. Checking only for nonzero addresses misses list-versus-page mistakes, a missing final page, or use of a virtual address as a physical address.

**Supporting sources:** NVME-BASE-2.4 Rev. 2.4, §4.3.1, printed pp. 158-159, PDF pp. 184-185; NVME-BASE-2.4 Rev. 2.4, §4.1.1, printed pp. 140-142, PDF pp. 166-168

**Related Figures:** Figure 110, Figure 111, Figure 112, Figure 113

### Module 04: An SGL is a typed descriptor chain, not another PRP List

**Explanation.** An SGL descriptor combines type/subtype, address, and length. A Data Block addresses data, Segment and Last Segment address more descriptors, and Bit Bucket represents data that need not be stored in memory. Figures 114-125 require type-first decoding; blindly following an address before decoding type is incorrect.

```text
Select SGL through PSDT
  ↓
Read descriptor type/subtype
  ↓
Validate length
  ↓
For data: add interval
  ↓
For segment: walk descriptors
  ↓
Stop at Last Segment
```

#### Comparison

| Item | What it answers | Engineering note |
|---|---|---|
| PRP | Page-based addresses | First-page offset plus later-page alignment |
| SGL Data Block | Address plus byte length | A descriptor represents a data region |
| SGL Segment | Address plus descriptor-list length | Points to more descriptors, not data |
| Bit Bucket | Consumes transfer length only | Does not represent a readable or writable memory buffer |

**Informative example.** Informative example: a 12 KiB request is covered by two Data Block descriptors of 8 KiB and 4 KiB. If the first descriptor is actually a Segment, its 8 KiB value describes a descriptor-list length rather than data length, and a parser that accumulates it as data is fundamentally wrong.

**Common mistake / debugging.** An SGL validator should bound nesting, descriptor count, total byte length, overflow, and loops. At every step, log type/subtype before deciding whether the address denotes data or another descriptor sequence; reversing that order can cause out-of-bounds traversal or cycles.

**Supporting sources:** NVME-BASE-2.4 Rev. 2.4, §4.3.2, printed pp. 159-166, PDF pp. 185-192; NVME-BASE-2.4 Rev. 2.4, §4.1.1, printed pp. 140-142, PDF pp. 166-168

**Related Figures:** Figure 114, Figure 115, Figure 116, Figure 117, Figure 118, Figure 119, Figure 120, Figure 121, Figure 122, Figure 125

### Module 05: Features, identifiers, lists, and UTF-8 all require scope validation

**Explanation.** Feature current/default/saved values define time and persistence scope; VID, SN, EUI64, NGUID, and UUID define identity scope; Controller/Namespace Lists define count and array boundaries; UTF-8 defines byte-sequence and code-point boundaries. Figures 126-142 appear diverse but share one parser rule: never interpret a value without its scope.

```text
Identify data kind
  ↓
Obtain width/count
  ↓
Confirm authority/scope
  ↓
Validate reserved/padding
  ↓
Build a stable comparison key
```

#### Comparison

| Item | What it answers | Engineering note |
|---|---|---|
| VID/SSVID | Vendor/subsystem-vendor identity | Assignment authorities differ |
| SN/MN | Product instance/model strings | Interpret fixed fields and padding |
| EUI64/NGUID/UUID | Different formats and uniqueness scopes | Similar length does not make them interchangeable |
| List | Count plus identifiers | Validate count before iteration |

**Informative example.** Informative example: a Namespace List claims five IDs but the returned buffer contains only three complete entries. A safe parser rejects the structure using buffer length and format limits rather than reading a fourth entry because the count looks plausible. A fixed UTF-8 field follows the same boundary rule: a truncated multibyte character is not accepted as half a character.

**Common mistake / debugging.** An identity database stores value, type, width, source object, and scope together. Storing only a hexadecimal string can create false equality among EUI64, NGUID, UUID, or identifiers obtained from different controllers.

**Supporting sources:** NVME-BASE-2.4 Rev. 2.4, §4.4, printed pp. 166-169, PDF pp. 192-195; NVME-BASE-2.4 Rev. 2.4, §4.5, printed pp. 169-172, PDF pp. 195-198; NVME-BASE-2.4 Rev. 2.4, §4.6, printed pp. 172-173, PDF pp. 198-199; NVME-BASE-2.4 Rev. 2.4, §4.8, printed pp. 175, PDF pp. 201

**Related Figures:** Figure 126, Figure 127, Figure 128, Figure 129, Figure 130, Figure 131, Figure 132, Figure 133, Figure 134, Figure 135, Figure 136, Figure 137, Figure 138, Figure 139, Figure 140, Figure 142

## Source-located specification findings

The mental model above explains causality. This section preserves each source-located conclusion and its normative strength for speaker notes and review.

### 1. Common SQE layout

<!-- claim:BASE4-SQE -->

The common Admin and I/O SQE is 64 bytes. CDW0, NSID, data pointers, and CDW10-15 establish the common layout before each command defines command-specific content.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §4.1.1, printed pages 139-143, PDF pages 165-169

### 2. CID uniqueness

<!-- claim:BASE4-CID -->

CID in combination with the Submission Queue identifier uniquely identifies a command. FFFFh should be avoided because the Error Information log uses it when an error is not associated with a particular command.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §4.1.1, printed pages 140, PDF pages 166

### 3. PRP/SGL selection

<!-- claim:BASE4-PSDT -->

CDW0.PSDT selects PRP or SGL interpretation for DPTR. An Admin command over PCIe shall use PRPs unless its command definition specifies otherwise.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §4.1.1, printed pages 140-142, PDF pages 166-168

### 4. Common CQE and Phase Tag

<!-- claim:BASE4-CQE -->

The common CQE is at least 16 bytes. If multiple writes construct it, the Phase Tag shall be updated in the last write so the host does not consume a partial entry.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §4.2.1, printed pages 144-145, PDF pages 170-171

### 5. SCT, SC, and DNR

<!-- claim:BASE4-STATUS -->

Status decoding starts with Status Code Type (SCT), then Status Code (SC), together with control bits such as Do Not Retry (DNR). An SC value is not interpreted without its SCT.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §4.2.3, printed pages 145-155, PDF pages 171-181

### 6. Completion Queue phase

<!-- claim:BASE4-PHASE -->

The Phase Tag lets the host distinguish a new entry in a circular Completion Queue. After consuming CQEs, the host advances the CQ head doorbell and expects phase inversion on wrap.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §4.2.4, printed pages 155-158, PDF pages 181-184

### 7. PRP alignment and pages

<!-- claim:BASE4-PRP -->

A fixed-size PRP entry points to a physical memory page. The first entry may contain a page offset; subsequent PRPs shall obey page alignment, and transfer length determines the required entry count.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §4.3.1, printed pages 158-159, PDF pages 184-185

### 8. SGL descriptors and length

<!-- claim:BASE4-SGL -->

An SGL describes a data buffer through one or more descriptors and segments. SGL length shall equal or exceed the requested transfer length; this report covers only generic descriptors applicable to PCIe.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §4.3.2, printed pages 159-166, PDF pages 185-192

### 9. Feature values and persistence

<!-- claim:BASE4-FEATURE -->

A Feature may have default, saved, and current values. Saved-value support and persistence across resets or power cycles are determined from SSFS and each Feature capability.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §4.4, printed pages 166-169, PDF pages 192-195

### 10. Scope of global identifiers

<!-- claim:BASE4-IDENTIFIER -->

VID/SSVID, SN/MN, IEEE OUI, EUI64, NGUID, and UUID differ in origin, length, and uniqueness scope and are not interchangeable. This section is informative.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §4.5, printed pages 169-172, PDF pages 195-198

### 11. Controller and Namespace Lists

<!-- claim:BASE4-LISTS -->

Controller and Namespace Lists provide a count followed by identifiers. A parser first validates the count, defined limit, and reserved area before consuming entries.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §4.6, printed pages 172-173, PDF pages 198-199

### 12. UTF-8 input validation

<!-- claim:BASE4-UTF8 -->

UTF-8 input processing validates encoding, prohibited code points, and truncation using the specified flow; an arbitrary byte sequence is not automatically a valid string.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

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

## Figure and field-table teaching reference

The source uses Figure numbers for diagrams and field-layout tables. No source artwork is reproduced; compact field and keyword indexes come from the locally verified PDFs.

<a id="section-4-1"></a>

### §4.1

<details markdown="1">
<summary><strong>Figure 92: Command Dword 0</strong></summary>

<!-- claim:BASE4-FIG-092-CLAIM figure-table:BASE4-FIG-092 -->

**SPEC.** Figure 92, "Command Dword 0": Defines the concrete layout or value relationships for Command Dword 0. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is CID, PSDT, FUSE, OPC, FN, DTD, PRP, SGL.

#### Where this Figure fits

Figure 92 sits in §4.1.1 and acts as a command checkpoint. Read it after the report mental model has established the owning object and before software turns CID into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a command-construction field table. Build the common SQE, locate the specified CDW, encode each bit range, clear reserved bits, and validate the result against transfer length, buffer, and completion status. Equal field names do not imply equal semantics across commands.

#### Teaching redraw

```text
[Locate source: CID]
          ↓
[Extract field: PSDT] → [Apply encoding: FUSE]
                                      ↓
[Validate evidence: OPC]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `CID` | Command Identifier, used with the SQ identifier to identify an outstanding command. |
| `PSDT` | PRP or SGL for Data Transfer, the CDW0 field selecting PRP or SGL interpretation for DPTR. |
| `FUSE` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `OPC` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `FN` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `DTD` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §4.1.1 is the applicable context.
2. Decode CID at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check PSDT as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 92 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §4.1.1 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes CID, PSDT, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §4.1.1, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 92. Annotate the bytes containing CID, decode them, and independently verify PSDT. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of CID in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand CID and state its unit or object scope?
2. Can the reader explain why PSDT is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** CID, PSDT, FUSE, OPC, FN, DTD, PRP, SGL

**Source keyword index:** `shall not`, `should not`, `shall`, `should`, `may`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §4.1.1, Figure 92, printed pages 139-140, PDF pages 165-166

</details>

<details markdown="1">
<summary><strong>Figure 93: Common Command Format</strong></summary>

<!-- claim:BASE4-FIG-093-CLAIM figure-table:BASE4-FIG-093 -->

**SPEC.** Figure 93, "Common Command Format": Defines the concrete layout or value relationships for Common Command Format. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is CDW0, NSID, CDW2, CDW3, MPTR, DPTR, PRP2, PRP1.

#### Where this Figure fits

Figure 93 sits in §4.1.1 and acts as a command checkpoint. Read it after the report mental model has established the owning object and before software turns CDW0 into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a command-construction field table. Build the common SQE, locate the specified CDW, encode each bit range, clear reserved bits, and validate the result against transfer length, buffer, and completion status. Equal field names do not imply equal semantics across commands.

#### Teaching redraw

```text
[Locate source: CDW0]
          ↓
[Extract field: NSID] → [Apply encoding: CDW2]
                                      ↓
[Validate evidence: CDW3]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `CDW0` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `NSID` | Namespace Identifier, a controller-visible numeric handle for a namespace; the identifier is not the namespace object itself. |
| `CDW2` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `CDW3` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `MPTR` | Metadata Pointer, the SQE field identifying a separate metadata buffer. |
| `DPTR` | Data Pointer, the SQE field identifying a command data buffer. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §4.1.1 is the applicable context.
2. Decode CDW0 at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check NSID as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 93 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §4.1.1 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes CDW0, NSID, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §4.1.1, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 93. Annotate the bytes containing CDW0, decode them, and independently verify NSID. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of CDW0 in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand CDW0 and state its unit or object scope?
2. Can the reader explain why NSID is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** CDW0, NSID, CDW2, CDW3, MPTR, DPTR, PRP2, PRP1

**Source keyword index:** `shall`, `may`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §4.1.1, Figure 93, printed pages 140-142, PDF pages 166-168

</details>

<details markdown="1">
<summary><strong>Figure 94: Common Command Format - Vendor Specific Commands (Optional)</strong></summary>

<!-- claim:BASE4-FIG-094-CLAIM figure-table:BASE4-FIG-094 -->

**SPEC.** Figure 94, "Common Command Format - Vendor Specific Commands (Optional)": Defines the concrete layout or value relationships for Common Command Format - Vendor Specific Commands (Optional). Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is CDW0, NSID, MDPTR, NDT, NDM, CDW12, CDW13, CDW14.

#### Where this Figure fits

Figure 94 sits in §4.1.1 and acts as a command checkpoint. Read it after the report mental model has established the owning object and before software turns CDW0 into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a command-construction field table. Build the common SQE, locate the specified CDW, encode each bit range, clear reserved bits, and validate the result against transfer length, buffer, and completion status. Equal field names do not imply equal semantics across commands.

#### Teaching redraw

```text
[Locate source: CDW0]
          ↓
[Extract field: NSID] → [Apply encoding: MDPTR]
                                      ↓
[Validate evidence: NDT]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `CDW0` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `NSID` | Namespace Identifier, a controller-visible numeric handle for a namespace; the identifier is not the namespace object itself. |
| `MDPTR` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `NDT` | Number of Dwords in Data Transfer, the actual data-dword count in the standard vendor-specific format. |
| `NDM` | Number of Dwords in Metadata Transfer, the actual metadata-dword count in the standard vendor-specific format. |
| `CDW12` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §4.1.1 is the applicable context.
2. Decode CDW0 at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check NSID as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 94 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §4.1.1 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes CDW0, NSID, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §4.1.1, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 94. Annotate the bytes containing CDW0, decode them, and independently verify NSID. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of CDW0 in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand CDW0 and state its unit or object scope?
2. Can the reader explain why NSID is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** CDW0, NSID, MDPTR, NDT, NDM, CDW12, CDW13, CDW14

**Source keyword index:** `shall`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §4.1.1, Figure 94, printed pages 143, PDF pages 169

</details>

<a id="section-4-2"></a>

### §4.2

<details markdown="1">
<summary><strong>Figure 97: Common Completion Queue Entry Layout - Admin and All I/O Command Sets</strong></summary>

<!-- claim:BASE4-FIG-097-CLAIM figure-table:BASE4-FIG-097 -->

**SPEC.** Figure 97, "Common Completion Queue Entry Layout - Admin and All I/O Command Sets": Defines the concrete layout or value relationships for Common Completion Queue Entry Layout - Admin and All I/O Command Sets. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is DW0, DW1, DW2, SQ, DW3, Command Set, Completion Queue, Command.

#### Where this Figure fits

Figure 97 sits in §4.2.1 and acts as a queue checkpoint. Read it after the report mental model has established the owning object and before software turns DW0 into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a queue or command-flow Figure. Label host and controller ownership first, then trace head, tail, phase, or arbitration changes. An arrow represents a state or ownership transition and does not automatically prove command completion.

#### Teaching redraw

```text
[Locate source: DW0]
          ↓
[Extract field: DW1] → [Apply encoding: DW2]
                                      ↓
[Validate evidence: SQ]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `DW0` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `DW1` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `DW2` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `SQ` | Submission Queue, the queue into which the host places commands. |
| `DW3` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `Command Set` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §4.2.1 is the applicable context.
2. Decode DW0 at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check DW1 as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 97 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §4.2.1 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes DW0, DW1, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §4.2.1, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 97. Annotate the bytes containing DW0, decode them, and independently verify DW1. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of DW0 in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand DW0 and state its unit or object scope?
2. Can the reader explain why DW1 is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** DW0, DW1, DW2, SQ, DW3, Command Set, Completion Queue, Command

**Source keyword index:** none

> Source: NVME-BASE-2.4, Rev. 2.4, §4.2.1, Figure 97, printed pages 144, PDF pages 170

</details>

<details markdown="1">
<summary><strong>Figure 98: Completion Queue Entry: DW 2</strong></summary>

<!-- claim:BASE4-FIG-098-CLAIM figure-table:BASE4-FIG-098 -->

**SPEC.** Figure 98, "Completion Queue Entry: DW 2": Shows the queue or command relationship expressed by Completion Queue Entry: DW 2. Trace ownership and direction from host to SQ, controller, and CQ; keep the indexed elements distinct: SQID, SQHD, DW, SQ, CID, Completion Queue.

#### Where this Figure fits

Figure 98 sits in §4.2.1 and acts as a queue checkpoint. Read it after the report mental model has established the owning object and before software turns SQID into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a queue or command-flow Figure. Label host and controller ownership first, then trace head, tail, phase, or arbitration changes. An arrow represents a state or ownership transition and does not automatically prove command completion.

#### Teaching redraw

```text
[Locate source: SQID]
          ↓
[Extract field: SQHD] → [Apply encoding: DW]
                                      ↓
[Validate evidence: SQ]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `SQID` | Submission Queue Identifier, the numeric identifier of the SQ containing a command. |
| `SQHD` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `DW` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `SQ` | Submission Queue, the queue into which the host places commands. |
| `CID` | Command Identifier, used with the SQ identifier to identify an outstanding command. |
| `Completion Queue` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §4.2.1 is the applicable context.
2. Decode SQID at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check SQHD as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 98 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §4.2.1 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes SQID, SQHD, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §4.2.1, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 98. Annotate the bytes containing SQID, decode them, and independently verify SQHD. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of SQID in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand SQID and state its unit or object scope?
2. Can the reader explain why SQHD is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** SQID, SQHD, DW, SQ, CID, Completion Queue

**Source keyword index:** `may`

> Source: NVME-BASE-2.4, Rev. 2.4, §4.2.1, Figure 98, printed pages 144, PDF pages 170

</details>

<details markdown="1">
<summary><strong>Figure 99: Completion Queue Entry: DW 3</strong></summary>

<!-- claim:BASE4-FIG-099-CLAIM figure-table:BASE4-FIG-099 -->

**SPEC.** Figure 99, "Completion Queue Entry: DW 3": Shows the queue or command relationship expressed by Completion Queue Entry: DW 3. Trace ownership and direction from host to SQ, controller, and CQ; keep the indexed elements distinct: STATUS, CID, DW, SQ, Completion Queue.

#### Where this Figure fits

Figure 99 sits in §4.2.1 and acts as a queue checkpoint. Read it after the report mental model has established the owning object and before software turns STATUS into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a queue or command-flow Figure. Label host and controller ownership first, then trace head, tail, phase, or arbitration changes. An arrow represents a state or ownership transition and does not automatically prove command completion.

#### Teaching redraw

```text
[Locate source: STATUS]
          ↓
[Extract field: CID] → [Apply encoding: DW]
                                      ↓
[Validate evidence: SQ]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `STATUS` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `CID` | Command Identifier, used with the SQ identifier to identify an outstanding command. |
| `DW` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `SQ` | Submission Queue, the queue into which the host places commands. |
| `Completion Queue` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §4.2.1 is the applicable context.
2. Decode STATUS at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check CID as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 99 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §4.2.1 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes STATUS, CID, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §4.2.1, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 99. Annotate the bytes containing STATUS, decode them, and independently verify CID. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of STATUS in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand STATUS and state its unit or object scope?
2. Can the reader explain why CID is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** STATUS, CID, DW, SQ, Completion Queue

**Source keyword index:** none

> Source: NVME-BASE-2.4, Rev. 2.4, §4.2.1, Figure 99, printed pages 145, PDF pages 171

</details>

<details markdown="1">
<summary><strong>Figure 101: Completion Queue Entry: Status Field</strong></summary>

<!-- claim:BASE4-FIG-101-CLAIM figure-table:BASE4-FIG-101 -->

**SPEC.** Figure 101, "Completion Queue Entry: Status Field": Defines the concrete layout or value relationships for Completion Queue Entry: Status Field. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is DNR, CRD, SCT, SC, ACRE, CRDT1, CRDT2, CRDT3.

#### Where this Figure fits

Figure 101 sits in §4.2.3 and acts as a queue checkpoint. Read it after the report mental model has established the owning object and before software turns DNR into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a queue or command-flow Figure. Label host and controller ownership first, then trace head, tail, phase, or arbitration changes. An arrow represents a state or ownership transition and does not automatically prove command completion.

#### Teaching redraw

```text
[Locate source: DNR]
          ↓
[Extract field: CRD] → [Apply encoding: SCT]
                                      ↓
[Validate evidence: SC]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `DNR` | Do Not Retry, a CQE-status bit indicating that retrying the same command is not expected to succeed. |
| `CRD` | Command Retry Delay, the status field selecting a controller-recommended retry delay. |
| `SCT` | Status Code Type, the category selected before interpreting SC. |
| `SC` | Status Code, the specific completion result interpreted in the context of SCT. |
| `ACRE` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `CRDT1` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §4.2.3 is the applicable context.
2. Decode DNR at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check CRD as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 101 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §4.2.3 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes DNR, CRD, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §4.2.3, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 101. Annotate the bytes containing DNR, decode them, and independently verify CRD. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of DNR in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand DNR and state its unit or object scope?
2. Can the reader explain why CRD is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** DNR, CRD, SCT, SC, ACRE, CRDT1, CRDT2, CRDT3

**Source keyword index:** `should not`, `should`, `may`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §4.2.3, Figure 101, printed pages 145-146, PDF pages 171-172

</details>

<details markdown="1">
<summary><strong>Figure 102: Status Code - Status Code Type Values</strong></summary>

<!-- claim:BASE4-FIG-102-CLAIM figure-table:BASE4-FIG-102 -->

**SPEC.** Figure 102, "Status Code - Status Code Type Values": Defines the status/error classification represented by Status Code - Status Code Type Values. Resolve the category before the individual code or flag; keep reserved values uninterpreted. Evidence index: SC, Status Code.

#### Where this Figure fits

Figure 102 sits in §4.2.3 and acts as a status checkpoint. Read it after the report mental model has established the owning object and before software turns SC into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a status or error classification. Identify the containing structure and category before decoding the individual code, control bits, and retry indication. Reserved values remain uninterpreted, and a similar name does not map the code into another error layer.

#### Teaching redraw

```text
[Locate source: SC]
          ↓
[Extract field: Status Code] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `SC` | Status Code, the specific completion result interpreted in the context of SCT. |
| `Status Code` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §4.2.3 is the applicable context.
2. Decode SC at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check Status Code as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 102 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §4.2.3 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes SC, Status Code, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §4.2.3, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 102. Annotate the bytes containing SC, decode them, and independently verify Status Code. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of SC in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand SC and state its unit or object scope?
2. Can the reader explain why Status Code is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** SC, Status Code

**Source keyword index:** `shall`, `may`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §4.2.3, Figure 102, printed pages 146, PDF pages 172

</details>

<details markdown="1">
<summary><strong>Figure 103: Status Code - Generic Command Status Values</strong></summary>

<!-- claim:BASE4-FIG-103-CLAIM figure-table:BASE4-FIG-103 -->

**SPEC.** Figure 103, "Status Code - Generic Command Status Values": Defines the status/error classification represented by Status Code - Generic Command Status Values. Resolve the category before the individual code or flag; keep reserved values uninterpreted. Evidence index: ID, SQ, TCG, SGL, PRP, ZNS, RACQA, CMB.

#### Where this Figure fits

Figure 103 sits in §4.2.3 and acts as a status checkpoint. Read it after the report mental model has established the owning object and before software turns ID into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a status or error classification. Identify the containing structure and category before decoding the individual code, control bits, and retry indication. Reserved values remain uninterpreted, and a similar name does not map the code into another error layer.

#### Teaching redraw

```text
[Locate source: ID]
          ↓
[Extract field: SQ] → [Apply encoding: TCG]
                                      ↓
[Validate evidence: SGL]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `ID` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `SQ` | Submission Queue, the queue into which the host places commands. |
| `TCG` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `SGL` | Scatter Gather List, a descriptor-and-segment format for one or more data-buffer regions. |
| `PRP` | Physical Region Page, a pointer format describing a host-addressable data buffer in memory-page units. |
| `ZNS` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §4.2.3 is the applicable context.
2. Decode ID at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check SQ as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 103 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §4.2.3 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes ID, SQ, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §4.2.3, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 103. Annotate the bytes containing ID, decode them, and independently verify SQ. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

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
2. Can the reader explain why SQ is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** ID, SQ, TCG, SGL, PRP, ZNS, RACQA, CMB

**Source keyword index:** `shall not`, `shall`, `should`, `may`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §4.2.3, Figure 103, printed pages 147-150, PDF pages 173-176

</details>

<details markdown="1">
<summary><strong>Figure 104: Status Code - Command Specific Status Values</strong></summary>

<!-- claim:BASE4-FIG-104-CLAIM figure-table:BASE4-FIG-104 -->

**SPEC.** Figure 104, "Status Code - Command Specific Status Values": Defines the status/error classification represented by Status Code - Command Specific Status Values. Resolve the category before the individual code or flag; keep reserved values uninterpreted. Evidence index: ANA, NOTE, Status Code, Command.

#### Where this Figure fits

Figure 104 sits in §4.2.3.2 and acts as a status checkpoint. Read it after the report mental model has established the owning object and before software turns ANA into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a status or error classification. Identify the containing structure and category before decoding the individual code, control bits, and retry indication. Reserved values remain uninterpreted, and a similar name does not map the code into another error layer.

#### Teaching redraw

```text
[Locate source: ANA]
          ↓
[Extract field: NOTE] → [Apply encoding: Status Code]
                                      ↓
[Validate evidence: Command]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `ANA` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `NOTE` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `Status Code` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `Command` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §4.2.3.2 is the applicable context.
2. Decode ANA at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check NOTE as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 104 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §4.2.3.2 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes ANA, NOTE, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §4.2.3.2, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 104. Annotate the bytes containing ANA, decode them, and independently verify NOTE. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of ANA in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand ANA and state its unit or object scope?
2. Can the reader explain why NOTE is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** ANA, NOTE, Status Code, Command

**Source keyword index:** `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §4.2.3.2, Figure 104, printed pages 151-152, PDF pages 177-178

</details>

<details markdown="1">
<summary><strong>Figure 105: Status Code - Command Specific Status Values, I/O Command Set Specific</strong></summary>

<!-- claim:BASE4-FIG-105-CLAIM figure-table:BASE4-FIG-105 -->

**SPEC.** Figure 105, "Status Code - Command Specific Status Values, I/O Command Set Specific": Defines the status/error classification represented by Status Code - Command Specific Status Values, I/O Command Set Specific. Resolve the category before the individual code or flag; keep reserved values uninterpreted. Evidence index: ID, Command Set, Status Code, Command.

#### Where this Figure fits

Figure 105 sits in §4.2.3.2 and acts as a status checkpoint. Read it after the report mental model has established the owning object and before software turns ID into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a status or error classification. Identify the containing structure and category before decoding the individual code, control bits, and retry indication. Reserved values remain uninterpreted, and a similar name does not map the code into another error layer.

#### Teaching redraw

```text
[Locate source: ID]
          ↓
[Extract field: Command Set] → [Apply encoding: Status Code]
                                      ↓
[Validate evidence: Command]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `ID` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `Command Set` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `Status Code` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `Command` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §4.2.3.2 is the applicable context.
2. Decode ID at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check Command Set as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 105 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §4.2.3.2 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes ID, Command Set, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §4.2.3.2, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 105. Annotate the bytes containing ID, decode them, and independently verify Command Set. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

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
2. Can the reader explain why Command Set is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** ID, Command Set, Status Code, Command

**Source keyword index:** `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §4.2.3.2, Figure 105, printed pages 152-153, PDF pages 178-179

</details>

<details markdown="1">
<summary><strong>Figure 107: Status Code - Media and Data Integrity Error Values</strong></summary>

<!-- claim:BASE4-FIG-107-CLAIM figure-table:BASE4-FIG-107 -->

**SPEC.** Figure 107, "Status Code - Media and Data Integrity Error Values": Defines the status/error classification represented by Status Code - Media and Data Integrity Error Values. Resolve the category before the individual code or flag; keep reserved values uninterpreted. Evidence index: TCG, SCT, Status Code.

#### Where this Figure fits

Figure 107 sits in §4.2.3.2 and acts as a status checkpoint. Read it after the report mental model has established the owning object and before software turns TCG into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a status or error classification. Identify the containing structure and category before decoding the individual code, control bits, and retry indication. Reserved values remain uninterpreted, and a similar name does not map the code into another error layer.

#### Teaching redraw

```text
[Locate source: TCG]
          ↓
[Extract field: SCT] → [Apply encoding: Status Code]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `TCG` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `SCT` | Status Code Type, the category selected before interpreting SC. |
| `Status Code` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §4.2.3.2 is the applicable context.
2. Decode TCG at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check SCT as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 107 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §4.2.3.2 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes TCG, SCT, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §4.2.3.2, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 107. Annotate the bytes containing TCG, decode them, and independently verify SCT. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of TCG in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand TCG and state its unit or object scope?
2. Can the reader explain why SCT is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** TCG, SCT, Status Code

**Source keyword index:** `should`, `may`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §4.2.3.2, Figure 107, printed pages 154-155, PDF pages 180-181

</details>

<details markdown="1">
<summary><strong>Figure 108: Status Code - Path Related Status Values</strong></summary>

<!-- claim:BASE4-FIG-108-CLAIM figure-table:BASE4-FIG-108 -->

**SPEC.** Figure 108, "Status Code - Path Related Status Values": Defines the status/error classification represented by Status Code - Path Related Status Values. Resolve the category before the individual code or flag; keep reserved values uninterpreted. Evidence index: DNR, ANA, Status Code.

#### Where this Figure fits

Figure 108 sits in §4.2.3.3 and acts as a status checkpoint. Read it after the report mental model has established the owning object and before software turns DNR into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a status or error classification. Identify the containing structure and category before decoding the individual code, control bits, and retry indication. Reserved values remain uninterpreted, and a similar name does not map the code into another error layer.

#### Teaching redraw

```text
[Locate source: DNR]
          ↓
[Extract field: ANA] → [Apply encoding: Status Code]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `DNR` | Do Not Retry, a CQE-status bit indicating that retrying the same command is not expected to succeed. |
| `ANA` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `Status Code` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §4.2.3.3 is the applicable context.
2. Decode DNR at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check ANA as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 108 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §4.2.3.3 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes DNR, ANA, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §4.2.3.3, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 108. Annotate the bytes containing DNR, decode them, and independently verify ANA. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of DNR in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand DNR and state its unit or object scope?
2. Can the reader explain why ANA is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** DNR, ANA, Status Code

**Source keyword index:** `should not`, `should`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §4.2.3.3, Figure 108, printed pages 155, PDF pages 181

</details>

<details markdown="1">
<summary><strong>Figure 109: Phase Tag bit Transition Example</strong></summary>

<!-- claim:BASE4-FIG-109-CLAIM figure-table:BASE4-FIG-109 -->

**SPEC.** Figure 109, "Phase Tag bit Transition Example": Shows the queue or command relationship expressed by Phase Tag bit Transition Example. Trace ownership and direction from host to SQ, controller, and CQ; keep the indexed elements distinct: Phase Tag.

#### Where this Figure fits

Figure 109 sits in §4.2.4 and acts as a queue checkpoint. Read it after the report mental model has established the owning object and before software turns Phase Tag into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a queue or command-flow Figure. Label host and controller ownership first, then trace head, tail, phase, or arbitration changes. An arrow represents a state or ownership transition and does not automatically prove command completion.

#### Teaching redraw

```text
[Locate source: Phase Tag]
          ↓
[Extract field: evidence] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `Phase Tag` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §4.2.4 is the applicable context.
2. Decode Phase Tag at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check the cited condition as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 109 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §4.2.4 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes Phase Tag, the cited condition, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §4.2.4, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 109. Annotate the bytes containing Phase Tag, decode them, and independently verify the cited condition. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of Phase Tag in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand Phase Tag and state its unit or object scope?
2. Can the reader explain why the cited condition is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** Phase Tag

**Source keyword index:** none

> Source: NVME-BASE-2.4, Rev. 2.4, §4.2.4, Figure 109, printed pages 156-157, PDF pages 182-183

</details>

<a id="section-4-3"></a>

### §4.3

<details markdown="1">
<summary><strong>Figure 110: PRP Entry Layout</strong></summary>

<!-- claim:BASE4-FIG-110-CLAIM figure-table:BASE4-FIG-110 -->

**SPEC.** Figure 110, "PRP Entry Layout": Defines the concrete layout or value relationships for PRP Entry Layout. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is PRP.

#### Where this Figure fits

Figure 110 sits in §4.3.1 and acts as a memory checkpoint. Read it after the report mental model has established the owning object and before software turns PRP into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a data-buffer mapping Figure. Read pointer type, address, length, page or segment boundary, and next entry in that order. Maintain the byte interval covered at every step to detect overlap, gaps, overflow, and alignment defects.

#### Teaching redraw

```text
[Locate source: PRP]
          ↓
[Extract field: evidence] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `PRP` | Physical Region Page, a pointer format describing a host-addressable data buffer in memory-page units. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §4.3.1 is the applicable context.
2. Decode PRP at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check the cited condition as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 110 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §4.3.1 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes PRP, the cited condition, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §4.3.1, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 110. Annotate the bytes containing PRP, decode them, and independently verify the cited condition. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of PRP in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand PRP and state its unit or object scope?
2. Can the reader explain why the cited condition is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** PRP

**Source keyword index:** none

> Source: NVME-BASE-2.4, Rev. 2.4, §4.3.1, Figure 110, printed pages 158, PDF pages 184

</details>

<details markdown="1">
<summary><strong>Figure 111: PRP Entry - Page Base Address and Offset</strong></summary>

<!-- claim:BASE4-FIG-111-CLAIM figure-table:BASE4-FIG-111 -->

**SPEC.** Figure 111, "PRP Entry - Page Base Address and Offset": Shows how PRP Entry - Page Base Address and Offset maps a transfer onto host-memory locations. Follow address, length, page/segment boundaries, and the link to the next entry in order. Evidence index: PBAO, PRP.

#### Where this Figure fits

Figure 111 sits in §4.3.1 and acts as a memory checkpoint. Read it after the report mental model has established the owning object and before software turns PBAO into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a data-buffer mapping Figure. Read pointer type, address, length, page or segment boundary, and next entry in that order. Maintain the byte interval covered at every step to detect overlap, gaps, overflow, and alignment defects.

#### Teaching redraw

```text
[Locate source: PBAO]
          ↓
[Extract field: PRP] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `PBAO` | Page Base Address and Offset, the first-PRP layout combining a page base address with an in-page offset. |
| `PRP` | Physical Region Page, a pointer format describing a host-addressable data buffer in memory-page units. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §4.3.1 is the applicable context.
2. Decode PBAO at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check PRP as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 111 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §4.3.1 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes PBAO, PRP, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §4.3.1, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 111. Annotate the bytes containing PBAO, decode them, and independently verify PRP. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

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
2. Can the reader explain why PRP is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** PBAO, PRP

**Source keyword index:** `shall`, `may`

> Source: NVME-BASE-2.4, Rev. 2.4, §4.3.1, Figure 111, printed pages 158, PDF pages 184

</details>

<details markdown="1">
<summary><strong>Figure 112: PRP List Layout for Physically Contiguous Memory Pages</strong></summary>

<!-- claim:BASE4-FIG-112-CLAIM figure-table:BASE4-FIG-112 -->

**SPEC.** Figure 112, "PRP List Layout for Physically Contiguous Memory Pages": Defines the concrete layout or value relationships for PRP List Layout for Physically Contiguous Memory Pages. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is PRP, Memory Page.

#### Where this Figure fits

Figure 112 sits in §4.3.1 and acts as a memory checkpoint. Read it after the report mental model has established the owning object and before software turns PRP into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a data-buffer mapping Figure. Read pointer type, address, length, page or segment boundary, and next entry in that order. Maintain the byte interval covered at every step to detect overlap, gaps, overflow, and alignment defects.

#### Teaching redraw

```text
[Locate source: PRP]
          ↓
[Extract field: Memory Page] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `PRP` | Physical Region Page, a pointer format describing a host-addressable data buffer in memory-page units. |
| `Memory Page` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §4.3.1 is the applicable context.
2. Decode PRP at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check Memory Page as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 112 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §4.3.1 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes PRP, Memory Page, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §4.3.1, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 112. Annotate the bytes containing PRP, decode them, and independently verify Memory Page. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of PRP in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand PRP and state its unit or object scope?
2. Can the reader explain why Memory Page is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** PRP, Memory Page

**Source keyword index:** none

> Source: NVME-BASE-2.4, Rev. 2.4, §4.3.1, Figure 112, printed pages 159, PDF pages 185

</details>

<details markdown="1">
<summary><strong>Figure 113: PRP List Layout for Physically Non-Contiguous Memory Pages</strong></summary>

<!-- claim:BASE4-FIG-113-CLAIM figure-table:BASE4-FIG-113 -->

**SPEC.** Figure 113, "PRP List Layout for Physically Non-Contiguous Memory Pages": Defines the concrete layout or value relationships for PRP List Layout for Physically Non-Contiguous Memory Pages. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is PRP, CC.MPS, Memory Page.

#### Where this Figure fits

Figure 113 sits in §4.3.1 and acts as a memory checkpoint. Read it after the report mental model has established the owning object and before software turns PRP into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a data-buffer mapping Figure. Read pointer type, address, length, page or segment boundary, and next entry in that order. Maintain the byte interval covered at every step to detect overlap, gaps, overflow, and alignment defects.

#### Teaching redraw

```text
[Locate source: PRP]
          ↓
[Extract field: CC.MPS] → [Apply encoding: Memory Page]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `PRP` | Physical Region Page, a pointer format describing a host-addressable data buffer in memory-page units. |
| `CC.MPS` | Controller Configuration, the property through which the host selects settings and enables or disables a controller. Here CC.MPS selects its MPS member field. |
| `Memory Page` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §4.3.1 is the applicable context.
2. Decode PRP at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check CC.MPS as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 113 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §4.3.1 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes PRP, CC.MPS, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §4.3.1, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 113. Annotate the bytes containing PRP, decode them, and independently verify CC.MPS. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of PRP in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand PRP and state its unit or object scope?
2. Can the reader explain why CC.MPS is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** PRP, CC.MPS, Memory Page

**Source keyword index:** `shall`, `should`, `may`

> Source: NVME-BASE-2.4, Rev. 2.4, §4.3.1, Figure 113, printed pages 159, PDF pages 185

</details>

<details markdown="1">
<summary><strong>Figure 114: SGL Validation Error Conditions</strong></summary>

<!-- claim:BASE4-FIG-114-CLAIM figure-table:BASE4-FIG-114 -->

**SPEC.** Figure 114, "SGL Validation Error Conditions": Defines the status/error classification represented by SGL Validation Error Conditions. Resolve the category before the individual code or flag; keep reserved values uninterpreted. Evidence index: SGL.

#### Where this Figure fits

Figure 114 sits in §4.3.2 and acts as a status checkpoint. Read it after the report mental model has established the owning object and before software turns SGL into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a status or error classification. Identify the containing structure and category before decoding the individual code, control bits, and retry indication. Reserved values remain uninterpreted, and a similar name does not map the code into another error layer.

#### Teaching redraw

```text
[Locate source: SGL]
          ↓
[Extract field: evidence] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `SGL` | Scatter Gather List, a descriptor-and-segment format for one or more data-buffer regions. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §4.3.2 is the applicable context.
2. Decode SGL at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check the cited condition as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 114 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §4.3.2 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes SGL, the cited condition, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §4.3.2, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 114. Annotate the bytes containing SGL, decode them, and independently verify the cited condition. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of SGL in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand SGL and state its unit or object scope?
2. Can the reader explain why the cited condition is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** SGL

**Source keyword index:** none

> Source: NVME-BASE-2.4, Rev. 2.4, §4.3.2, Figure 114, printed pages 161, PDF pages 187

</details>

<details markdown="1">
<summary><strong>Figure 115: SGL Segment</strong></summary>

<!-- claim:BASE4-FIG-115-CLAIM figure-table:BASE4-FIG-115 -->

**SPEC.** Figure 115, "SGL Segment": Shows how SGL Segment maps a transfer onto host-memory locations. Follow address, length, page/segment boundaries, and the link to the next entry in order. Evidence index: SGL.

#### Where this Figure fits

Figure 115 sits in §4.3.2 and acts as a memory checkpoint. Read it after the report mental model has established the owning object and before software turns SGL into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a data-buffer mapping Figure. Read pointer type, address, length, page or segment boundary, and next entry in that order. Maintain the byte interval covered at every step to detect overlap, gaps, overflow, and alignment defects.

#### Teaching redraw

```text
[Locate source: SGL]
          ↓
[Extract field: evidence] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `SGL` | Scatter Gather List, a descriptor-and-segment format for one or more data-buffer regions. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §4.3.2 is the applicable context.
2. Decode SGL at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check the cited condition as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 115 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §4.3.2 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes SGL, the cited condition, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §4.3.2, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 115. Annotate the bytes containing SGL, decode them, and independently verify the cited condition. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of SGL in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand SGL and state its unit or object scope?
2. Can the reader explain why the cited condition is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** SGL

**Source keyword index:** none

> Source: NVME-BASE-2.4, Rev. 2.4, §4.3.2, Figure 115, printed pages 161, PDF pages 187

</details>

<details markdown="1">
<summary><strong>Figure 116: Generic SGL Descriptor Format</strong></summary>

<!-- claim:BASE4-FIG-116-CLAIM figure-table:BASE4-FIG-116 -->

**SPEC.** Figure 116, "Generic SGL Descriptor Format": Defines the concrete layout or value relationships for Generic SGL Descriptor Format. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is DTS, SGLID, SGLDT, SGLDST, SGL, NULL.

#### Where this Figure fits

Figure 116 sits in §4.3.2 and acts as a memory checkpoint. Read it after the report mental model has established the owning object and before software turns DTS into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a data-buffer mapping Figure. Read pointer type, address, length, page or segment boundary, and next entry in that order. Maintain the byte interval covered at every step to detect overlap, gaps, overflow, and alignment defects.

#### Teaching redraw

```text
[Locate source: DTS]
          ↓
[Extract field: SGLID] → [Apply encoding: SGLDT]
                                      ↓
[Validate evidence: SGLDST]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `DTS` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `SGLID` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `SGLDT` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `SGLDST` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `SGL` | Scatter Gather List, a descriptor-and-segment format for one or more data-buffer regions. |
| `NULL` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §4.3.2 is the applicable context.
2. Decode DTS at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check SGLID as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 116 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §4.3.2 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes DTS, SGLID, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §4.3.2, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 116. Annotate the bytes containing DTS, decode them, and independently verify SGLID. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of DTS in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand DTS and state its unit or object scope?
2. Can the reader explain why SGLID is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** DTS, SGLID, SGLDT, SGLDST, SGL, NULL

**Source keyword index:** `shall`, `may`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §4.3.2, Figure 116, printed pages 161, PDF pages 187

</details>

<details markdown="1">
<summary><strong>Figure 117: SGL Descriptor Type</strong></summary>

<!-- claim:BASE4-FIG-117-CLAIM figure-table:BASE4-FIG-117 -->

**SPEC.** Figure 117, "SGL Descriptor Type": Defines the concrete layout or value relationships for SGL Descriptor Type. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is SGL.

#### Where this Figure fits

Figure 117 sits in §4.3.2 and acts as a memory checkpoint. Read it after the report mental model has established the owning object and before software turns SGL into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a data-buffer mapping Figure. Read pointer type, address, length, page or segment boundary, and next entry in that order. Maintain the byte interval covered at every step to detect overlap, gaps, overflow, and alignment defects.

#### Teaching redraw

```text
[Locate source: SGL]
          ↓
[Extract field: evidence] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `SGL` | Scatter Gather List, a descriptor-and-segment format for one or more data-buffer regions. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §4.3.2 is the applicable context.
2. Decode SGL at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check the cited condition as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 117 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §4.3.2 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes SGL, the cited condition, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §4.3.2, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 117. Annotate the bytes containing SGL, decode them, and independently verify the cited condition. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of SGL in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand SGL and state its unit or object scope?
2. Can the reader explain why the cited condition is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** SGL

**Source keyword index:** `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §4.3.2, Figure 117, printed pages 161-162, PDF pages 187-188

</details>

<details markdown="1">
<summary><strong>Figure 118: SGL Descriptor Sub Type Values</strong></summary>

<!-- claim:BASE4-FIG-118-CLAIM figure-table:BASE4-FIG-118 -->

**SPEC.** Figure 118, "SGL Descriptor Sub Type Values": Defines the concrete layout or value relationships for SGL Descriptor Sub Type Values. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is SGL.

#### Where this Figure fits

Figure 118 sits in §4.3.2 and acts as a memory checkpoint. Read it after the report mental model has established the owning object and before software turns SGL into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a data-buffer mapping Figure. Read pointer type, address, length, page or segment boundary, and next entry in that order. Maintain the byte interval covered at every step to detect overlap, gaps, overflow, and alignment defects.

#### Teaching redraw

```text
[Locate source: SGL]
          ↓
[Extract field: evidence] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `SGL` | Scatter Gather List, a descriptor-and-segment format for one or more data-buffer regions. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §4.3.2 is the applicable context.
2. Decode SGL at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check the cited condition as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 118 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §4.3.2 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes SGL, the cited condition, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §4.3.2, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 118. Annotate the bytes containing SGL, decode them, and independently verify the cited condition. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of SGL in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand SGL and state its unit or object scope?
2. Can the reader explain why the cited condition is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** SGL

**Source keyword index:** `shall`, `may`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §4.3.2, Figure 118, printed pages 162, PDF pages 188

</details>

<details markdown="1">
<summary><strong>Figure 119: SGL Data Block descriptor</strong></summary>

<!-- claim:BASE4-FIG-119-CLAIM figure-table:BASE4-FIG-119 -->

**SPEC.** Figure 119, "SGL Data Block descriptor": Defines the concrete layout or value relationships for SGL Data Block descriptor. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is ADDR, LEN, SGLID, SGLDT, SGLDST, SGL, SGLS.

#### Where this Figure fits

Figure 119 sits in §4.3.2 and acts as a memory checkpoint. Read it after the report mental model has established the owning object and before software turns ADDR into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a data-buffer mapping Figure. Read pointer type, address, length, page or segment boundary, and next entry in that order. Maintain the byte interval covered at every step to detect overlap, gaps, overflow, and alignment defects.

#### Teaching redraw

```text
[Locate source: ADDR]
          ↓
[Extract field: LEN] → [Apply encoding: SGLID]
                                      ↓
[Validate evidence: SGLDT]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `ADDR` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `LEN` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `SGLID` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `SGLDT` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `SGLDST` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `SGL` | Scatter Gather List, a descriptor-and-segment format for one or more data-buffer regions. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §4.3.2 is the applicable context.
2. Decode ADDR at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check LEN as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 119 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §4.3.2 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes ADDR, LEN, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §4.3.2, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 119. Annotate the bytes containing ADDR, decode them, and independently verify LEN. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

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
2. Can the reader explain why LEN is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** ADDR, LEN, SGLID, SGLDT, SGLDST, SGL, SGLS

**Source keyword index:** `shall`, `may`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §4.3.2, Figure 119, printed pages 162-163, PDF pages 188-189

</details>

<details markdown="1">
<summary><strong>Figure 120: SGL Bit Bucket descriptor</strong></summary>

<!-- claim:BASE4-FIG-120-CLAIM figure-table:BASE4-FIG-120 -->

**SPEC.** Figure 120, "SGL Bit Bucket descriptor": Defines the concrete layout or value relationships for SGL Bit Bucket descriptor. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is LEN, SGLID, SGLDT, SGLDST, SGL, NLB.

#### Where this Figure fits

Figure 120 sits in §4.3.2 and acts as a memory checkpoint. Read it after the report mental model has established the owning object and before software turns LEN into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a data-buffer mapping Figure. Read pointer type, address, length, page or segment boundary, and next entry in that order. Maintain the byte interval covered at every step to detect overlap, gaps, overflow, and alignment defects.

#### Teaching redraw

```text
[Locate source: LEN]
          ↓
[Extract field: SGLID] → [Apply encoding: SGLDT]
                                      ↓
[Validate evidence: SGLDST]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `LEN` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `SGLID` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `SGLDT` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `SGLDST` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `SGL` | Scatter Gather List, a descriptor-and-segment format for one or more data-buffer regions. |
| `NLB` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §4.3.2 is the applicable context.
2. Decode LEN at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check SGLID as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 120 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §4.3.2 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes LEN, SGLID, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §4.3.2, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 120. Annotate the bytes containing LEN, decode them, and independently verify SGLID. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of LEN in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand LEN and state its unit or object scope?
2. Can the reader explain why SGLID is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** LEN, SGLID, SGLDT, SGLDST, SGL, NLB

**Source keyword index:** `shall`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §4.3.2, Figure 120, printed pages 163, PDF pages 189

</details>

<details markdown="1">
<summary><strong>Figure 121: SGL Segment descriptor</strong></summary>

<!-- claim:BASE4-FIG-121-CLAIM figure-table:BASE4-FIG-121 -->

**SPEC.** Figure 121, "SGL Segment descriptor": Defines the concrete layout or value relationships for SGL Segment descriptor. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is ADDR, LEN, SGLID, SGLDT, SGDST, SGL.

#### Where this Figure fits

Figure 121 sits in §4.3.2 and acts as a memory checkpoint. Read it after the report mental model has established the owning object and before software turns ADDR into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a data-buffer mapping Figure. Read pointer type, address, length, page or segment boundary, and next entry in that order. Maintain the byte interval covered at every step to detect overlap, gaps, overflow, and alignment defects.

#### Teaching redraw

```text
[Locate source: ADDR]
          ↓
[Extract field: LEN] → [Apply encoding: SGLID]
                                      ↓
[Validate evidence: SGLDT]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `ADDR` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `LEN` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `SGLID` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `SGLDT` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `SGDST` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `SGL` | Scatter Gather List, a descriptor-and-segment format for one or more data-buffer regions. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §4.3.2 is the applicable context.
2. Decode ADDR at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check LEN as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 121 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §4.3.2 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes ADDR, LEN, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §4.3.2, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 121. Annotate the bytes containing ADDR, decode them, and independently verify LEN. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

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
2. Can the reader explain why LEN is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** ADDR, LEN, SGLID, SGLDT, SGDST, SGL

**Source keyword index:** `shall`, `may`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §4.3.2, Figure 121, printed pages 163, PDF pages 189

</details>

<details markdown="1">
<summary><strong>Figure 122: SGL Last Segment descriptor</strong></summary>

<!-- claim:BASE4-FIG-122-CLAIM figure-table:BASE4-FIG-122 -->

**SPEC.** Figure 122, "SGL Last Segment descriptor": Defines the concrete layout or value relationships for SGL Last Segment descriptor. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is ADDR, LEN, SGLID, SGLDT, SGLDST, SGL.

#### Where this Figure fits

Figure 122 sits in §4.3.2 and acts as a memory checkpoint. Read it after the report mental model has established the owning object and before software turns ADDR into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a data-buffer mapping Figure. Read pointer type, address, length, page or segment boundary, and next entry in that order. Maintain the byte interval covered at every step to detect overlap, gaps, overflow, and alignment defects.

#### Teaching redraw

```text
[Locate source: ADDR]
          ↓
[Extract field: LEN] → [Apply encoding: SGLID]
                                      ↓
[Validate evidence: SGLDT]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `ADDR` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `LEN` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `SGLID` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `SGLDT` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `SGLDST` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `SGL` | Scatter Gather List, a descriptor-and-segment format for one or more data-buffer regions. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §4.3.2 is the applicable context.
2. Decode ADDR at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check LEN as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 122 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §4.3.2 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes ADDR, LEN, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §4.3.2, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 122. Annotate the bytes containing ADDR, decode them, and independently verify LEN. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

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
2. Can the reader explain why LEN is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** ADDR, LEN, SGLID, SGLDT, SGLDST, SGL

**Source keyword index:** `shall`, `may`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §4.3.2, Figure 122, printed pages 164, PDF pages 190

</details>

<details markdown="1">
<summary><strong>Figure 125: SGL Read Example</strong></summary>

<!-- claim:BASE4-FIG-125-CLAIM figure-table:BASE4-FIG-125 -->

**SPEC.** Figure 125, "SGL Read Example": Shows how SGL Read Example maps a transfer onto host-memory locations. Follow address, length, page/segment boundaries, and the link to the next entry in order. Evidence index: SGL.

#### Where this Figure fits

Figure 125 sits in §4.3.2.1 and acts as a memory checkpoint. Read it after the report mental model has established the owning object and before software turns SGL into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a data-buffer mapping Figure. Read pointer type, address, length, page or segment boundary, and next entry in that order. Maintain the byte interval covered at every step to detect overlap, gaps, overflow, and alignment defects.

#### Teaching redraw

```text
[Locate source: SGL]
          ↓
[Extract field: evidence] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `SGL` | Scatter Gather List, a descriptor-and-segment format for one or more data-buffer regions. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §4.3.2.1 is the applicable context.
2. Decode SGL at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check the cited condition as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 125 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §4.3.2.1 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes SGL, the cited condition, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §4.3.2.1, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 125. Annotate the bytes containing SGL, decode them, and independently verify the cited condition. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of SGL in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand SGL and state its unit or object scope?
2. Can the reader explain why the cited condition is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** SGL

**Source keyword index:** none

> Source: NVME-BASE-2.4, Rev. 2.4, §4.3.2.1, Figure 125, printed pages 166, PDF pages 192

</details>

<a id="section-4-4"></a>

### §4.4

<details markdown="1">
<summary><strong>Figure 126: Current Value after Reset with Scope of Entire NVM Subsystem</strong></summary>

<!-- claim:BASE4-FIG-126-CLAIM figure-table:BASE4-FIG-126 -->

**SPEC.** Figure 126, "Current Value after Reset with Scope of Entire NVM Subsystem": Shows the object or capacity relationships in Current Value after Reset with Scope of Entire NVM Subsystem. Separate logical identifiers from controllers, namespaces, ports, and capacity containers. Evidence index: NVM Subsystem.

#### Where this Figure fits

Figure 126 sits in §4.4 and acts as a hierarchy checkpoint. Read it after the report mental model has established the owning object and before software turns NVM Subsystem into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

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

1. Locate the structure, register, queue, or object named by the caption and confirm that §4.4 is the applicable context.
2. Decode NVM Subsystem at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check the cited condition as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 126 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §4.4 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes NVM Subsystem, the cited condition, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §4.4, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 126. Annotate the bytes containing NVM Subsystem, decode them, and independently verify the cited condition. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

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

> Source: NVME-BASE-2.4, Rev. 2.4, §4.4, Figure 126, printed pages 167, PDF pages 193

</details>

<details markdown="1">
<summary><strong>Figure 127: Current Value after Reset with Scope of Subset of the NVM Subsystem</strong></summary>

<!-- claim:BASE4-FIG-127-CLAIM figure-table:BASE4-FIG-127 -->

**SPEC.** Figure 127, "Current Value after Reset with Scope of Subset of the NVM Subsystem": Shows the object or capacity relationships in Current Value after Reset with Scope of Subset of the NVM Subsystem. Separate logical identifiers from controllers, namespaces, ports, and capacity containers. Evidence index: NVM Subsystem.

#### Where this Figure fits

Figure 127 sits in §4.4 and acts as a hierarchy checkpoint. Read it after the report mental model has established the owning object and before software turns NVM Subsystem into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

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

1. Locate the structure, register, queue, or object named by the caption and confirm that §4.4 is the applicable context.
2. Decode NVM Subsystem at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check the cited condition as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 127 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §4.4 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes NVM Subsystem, the cited condition, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §4.4, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 127. Annotate the bytes containing NVM Subsystem, decode them, and independently verify the cited condition. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

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

> Source: NVME-BASE-2.4, Rev. 2.4, §4.4, Figure 127, printed pages 168, PDF pages 194

</details>

<a id="section-4-5"></a>

### §4.5

<details markdown="1">
<summary><strong>Figure 128: PCI Vendor ID (VID) and PCI Subsystem Vendor ID (SSVID)</strong></summary>

<!-- claim:BASE4-FIG-128-CLAIM figure-table:BASE4-FIG-128 -->

**SPEC.** Figure 128, "PCI Vendor ID (VID) and PCI Subsystem Vendor ID (SSVID)": Shows the object or capacity relationships in PCI Vendor ID (VID) and PCI Subsystem Vendor ID (SSVID). Separate logical identifiers from controllers, namespaces, ports, and capacity containers. Evidence index: ID, VID, SSVID.

#### Where this Figure fits

Figure 128 sits in §4.5.1 and acts as a hierarchy checkpoint. Read it after the report mental model has established the owning object and before software turns ID into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is an object or capacity relationship Figure. Separate containment, accessibility, identifier reference, and sharing. Adjacent boxes need not be one-to-one, and an identifier is not the physical or logical object it references.

#### Teaching redraw

```text
[Locate source: ID]
          ↓
[Extract field: VID] → [Apply encoding: SSVID]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `ID` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `VID` | Vendor ID, a PCI-SIG-assigned identifier for a vendor. |
| `SSVID` | Subsystem Vendor ID, the PCI identifier for a subsystem vendor. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §4.5.1 is the applicable context.
2. Decode ID at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check VID as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 128 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §4.5.1 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes ID, VID, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §4.5.1, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 128. Annotate the bytes containing ID, decode them, and independently verify VID. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

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
2. Can the reader explain why VID is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** ID, VID, SSVID

**Source keyword index:** none

> Source: NVME-BASE-2.4, Rev. 2.4, §4.5.1, Figure 128, printed pages 169, PDF pages 195

</details>

<details markdown="1">
<summary><strong>Figure 129: Serial Number (SN) and Model Number (MN)</strong></summary>

<!-- claim:BASE4-FIG-129-CLAIM figure-table:BASE4-FIG-129 -->

**SPEC.** Figure 129, "Serial Number (SN) and Model Number (MN)": Defines the identifier composition or namespace of values shown by Serial Number (SN) and Model Number (MN). Keep the value width, issuing authority, uniqueness scope, and reserved values separate. Evidence index: SN, MN.

#### Where this Figure fits

Figure 129 sits in §4.5.2 and acts as a identifier checkpoint. Read it after the report mental model has established the owning object and before software turns SN into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is an identifier-format Figure. Record width and encoding, then identify assignment authority, uniqueness scope, reserved values, and lifetime. Equal-width identifiers are not automatically interchangeable.

#### Teaching redraw

```text
[Locate source: SN]
          ↓
[Extract field: MN] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `SN` | Serial Number, a string identifying a product instance. |
| `MN` | Model Number, a string identifying a product model. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §4.5.2 is the applicable context.
2. Decode SN at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check MN as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 129 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §4.5.2 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes SN, MN, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §4.5.2, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 129. Annotate the bytes containing SN, decode them, and independently verify MN. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of SN in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand SN and state its unit or object scope?
2. Can the reader explain why MN is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** SN, MN

**Source keyword index:** none

> Source: NVME-BASE-2.4, Rev. 2.4, §4.5.2, Figure 129, printed pages 170, PDF pages 196

</details>

<details markdown="1">
<summary><strong>Figure 130: IEEE OUI Identifier (IEEE)</strong></summary>

<!-- claim:BASE4-FIG-130-CLAIM figure-table:BASE4-FIG-130 -->

**SPEC.** Figure 130, "IEEE OUI Identifier (IEEE)": Defines the identifier composition or namespace of values shown by IEEE OUI Identifier (IEEE). Keep the value width, issuing authority, uniqueness scope, and reserved values separate. Evidence index: IEEE, OUI.

#### Where this Figure fits

Figure 130 sits in §4.5.3 and acts as a identifier checkpoint. Read it after the report mental model has established the owning object and before software turns IEEE into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is an identifier-format Figure. Record width and encoding, then identify assignment authority, uniqueness scope, reserved values, and lifetime. Equal-width identifiers are not automatically interchangeable.

#### Teaching redraw

```text
[Locate source: IEEE]
          ↓
[Extract field: OUI] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `IEEE` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `OUI` | Organizationally Unique Identifier, an IEEE-assigned identifier prefix for an organization. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §4.5.3 is the applicable context.
2. Decode IEEE at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check OUI as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 130 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §4.5.3 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes IEEE, OUI, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §4.5.3, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 130. Annotate the bytes containing IEEE, decode them, and independently verify OUI. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of IEEE in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand IEEE and state its unit or object scope?
2. Can the reader explain why OUI is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** IEEE, OUI

**Source keyword index:** none

> Source: NVME-BASE-2.4, Rev. 2.4, §4.5.3, Figure 130, printed pages 170, PDF pages 196

</details>

<details markdown="1">
<summary><strong>Figure 131: IEEE Extended Unique Identifier (EUI64), MA-L Format</strong></summary>

<!-- claim:BASE4-FIG-131-CLAIM figure-table:BASE4-FIG-131 -->

**SPEC.** Figure 131, "IEEE Extended Unique Identifier (EUI64), MA-L Format": Defines the concrete layout or value relationships for IEEE Extended Unique Identifier (EUI64), MA-L Format. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is IEEE, EUI64, MA, EUI, OUI.

#### Where this Figure fits

Figure 131 sits in §4.5.4 and acts as a identifier checkpoint. Read it after the report mental model has established the owning object and before software turns IEEE into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is an identifier-format Figure. Record width and encoding, then identify assignment authority, uniqueness scope, reserved values, and lifetime. Equal-width identifiers are not automatically interchangeable.

#### Teaching redraw

```text
[Locate source: IEEE]
          ↓
[Extract field: EUI64] → [Apply encoding: MA]
                                      ↓
[Validate evidence: EUI]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `IEEE` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `EUI64` | 64-bit Extended Unique Identifier, a 64-bit identifier constructed from IEEE-assigned space. |
| `MA` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `EUI` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `OUI` | Organizationally Unique Identifier, an IEEE-assigned identifier prefix for an organization. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §4.5.4 is the applicable context.
2. Decode IEEE at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check EUI64 as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 131 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §4.5.4 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes IEEE, EUI64, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §4.5.4, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 131. Annotate the bytes containing IEEE, decode them, and independently verify EUI64. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of IEEE in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand IEEE and state its unit or object scope?
2. Can the reader explain why EUI64 is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** IEEE, EUI64, MA, EUI, OUI

**Source keyword index:** none

> Source: NVME-BASE-2.4, Rev. 2.4, §4.5.4, Figure 131, printed pages 170, PDF pages 196

</details>

<details markdown="1">
<summary><strong>Figure 132: IEEE Extended Unique Identifier (EUI64), OUI Identifier</strong></summary>

<!-- claim:BASE4-FIG-132-CLAIM figure-table:BASE4-FIG-132 -->

**SPEC.** Figure 132, "IEEE Extended Unique Identifier (EUI64), OUI Identifier": Defines the identifier composition or namespace of values shown by IEEE Extended Unique Identifier (EUI64), OUI Identifier. Keep the value width, issuing authority, uniqueness scope, and reserved values separate. Evidence index: IEEE, EUI64, OUI.

#### Where this Figure fits

Figure 132 sits in §4.5.4 and acts as a identifier checkpoint. Read it after the report mental model has established the owning object and before software turns IEEE into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is an identifier-format Figure. Record width and encoding, then identify assignment authority, uniqueness scope, reserved values, and lifetime. Equal-width identifiers are not automatically interchangeable.

#### Teaching redraw

```text
[Locate source: IEEE]
          ↓
[Extract field: EUI64] → [Apply encoding: OUI]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `IEEE` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `EUI64` | 64-bit Extended Unique Identifier, a 64-bit identifier constructed from IEEE-assigned space. |
| `OUI` | Organizationally Unique Identifier, an IEEE-assigned identifier prefix for an organization. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §4.5.4 is the applicable context.
2. Decode IEEE at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check EUI64 as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 132 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §4.5.4 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes IEEE, EUI64, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §4.5.4, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 132. Annotate the bytes containing IEEE, decode them, and independently verify EUI64. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of IEEE in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand IEEE and state its unit or object scope?
2. Can the reader explain why EUI64 is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** IEEE, EUI64, OUI

**Source keyword index:** none

> Source: NVME-BASE-2.4, Rev. 2.4, §4.5.4, Figure 132, printed pages 170, PDF pages 196

</details>

<details markdown="1">
<summary><strong>Figure 133: IEEE Extended Unique Identifier (EUI64), Ext. ID (cont)</strong></summary>

<!-- claim:BASE4-FIG-133-CLAIM figure-table:BASE4-FIG-133 -->

**SPEC.** Figure 133, "IEEE Extended Unique Identifier (EUI64), Ext. ID (cont)": Defines the identifier composition or namespace of values shown by IEEE Extended Unique Identifier (EUI64), Ext. ID (cont). Keep the value width, issuing authority, uniqueness scope, and reserved values separate. Evidence index: IEEE, EUI64, ID, MA, WWN, NAA.

#### Where this Figure fits

Figure 133 sits in §4.5.4 and acts as a identifier checkpoint. Read it after the report mental model has established the owning object and before software turns IEEE into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is an identifier-format Figure. Record width and encoding, then identify assignment authority, uniqueness scope, reserved values, and lifetime. Equal-width identifiers are not automatically interchangeable.

#### Teaching redraw

```text
[Locate source: IEEE]
          ↓
[Extract field: EUI64] → [Apply encoding: ID]
                                      ↓
[Validate evidence: MA]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `IEEE` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `EUI64` | 64-bit Extended Unique Identifier, a 64-bit identifier constructed from IEEE-assigned space. |
| `ID` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `MA` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `WWN` | World Wide Name, a global naming format used for storage and networking devices. |
| `NAA` | Network Address Authority, the WWN nibble selecting an identifier format and assignment method. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §4.5.4 is the applicable context.
2. Decode IEEE at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check EUI64 as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 133 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §4.5.4 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes IEEE, EUI64, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §4.5.4, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 133. Annotate the bytes containing IEEE, decode them, and independently verify EUI64. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of IEEE in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand IEEE and state its unit or object scope?
2. Can the reader explain why EUI64 is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** IEEE, EUI64, ID, MA, WWN, NAA

**Source keyword index:** none

> Source: NVME-BASE-2.4, Rev. 2.4, §4.5.4, Figure 133, printed pages 170-171, PDF pages 196-197

</details>

<details markdown="1">
<summary><strong>Figure 134: MA-L similarity to WWN</strong></summary>

<!-- claim:BASE4-FIG-134-CLAIM figure-table:BASE4-FIG-134 -->

**SPEC.** Figure 134, "MA-L similarity to WWN": Defines the identifier composition or namespace of values shown by MA-L similarity to WWN. Keep the value width, issuing authority, uniqueness scope, and reserved values separate. Evidence index: MA, WWN.

#### Where this Figure fits

Figure 134 sits in §4.5.4 and acts as a identifier checkpoint. Read it after the report mental model has established the owning object and before software turns MA into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is an identifier-format Figure. Record width and encoding, then identify assignment authority, uniqueness scope, reserved values, and lifetime. Equal-width identifiers are not automatically interchangeable.

#### Teaching redraw

```text
[Locate source: MA]
          ↓
[Extract field: WWN] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `MA` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `WWN` | World Wide Name, a global naming format used for storage and networking devices. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §4.5.4 is the applicable context.
2. Decode MA at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check WWN as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 134 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §4.5.4 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes MA, WWN, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §4.5.4, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 134. Annotate the bytes containing MA, decode them, and independently verify WWN. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of MA in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand MA and state its unit or object scope?
2. Can the reader explain why WWN is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** MA, WWN

**Source keyword index:** none

> Source: NVME-BASE-2.4, Rev. 2.4, §4.5.4, Figure 134, printed pages 171, PDF pages 197

</details>

<details markdown="1">
<summary><strong>Figure 135: Namespace Globally Unique Identifier (NGUID)</strong></summary>

<!-- claim:BASE4-FIG-135-CLAIM figure-table:BASE4-FIG-135 -->

**SPEC.** Figure 135, "Namespace Globally Unique Identifier (NGUID)": Defines the identifier composition or namespace of values shown by Namespace Globally Unique Identifier (NGUID). Keep the value width, issuing authority, uniqueness scope, and reserved values separate. Evidence index: NGUID, Namespace.

#### Where this Figure fits

Figure 135 sits in §4.5.5 and acts as a hierarchy checkpoint. Read it after the report mental model has established the owning object and before software turns NGUID into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is an object or capacity relationship Figure. Separate containment, accessibility, identifier reference, and sharing. Adjacent boxes need not be one-to-one, and an identifier is not the physical or logical object it references.

#### Teaching redraw

```text
[Locate source: NGUID]
          ↓
[Extract field: Namespace] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `NGUID` | Namespace Globally Unique Identifier, a 128-bit global identifier for a namespace. |
| `Namespace` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §4.5.5 is the applicable context.
2. Decode NGUID at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check Namespace as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 135 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §4.5.5 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes NGUID, Namespace, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §4.5.5, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 135. Annotate the bytes containing NGUID, decode them, and independently verify Namespace. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of NGUID in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand NGUID and state its unit or object scope?
2. Can the reader explain why Namespace is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** NGUID, Namespace

**Source keyword index:** none

> Source: NVME-BASE-2.4, Rev. 2.4, §4.5.5, Figure 135, printed pages 171, PDF pages 197

</details>

<details markdown="1">
<summary><strong>Figure 136: Namespace Globally Unique Identifier (NGUID), OUI</strong></summary>

<!-- claim:BASE4-FIG-136-CLAIM figure-table:BASE4-FIG-136 -->

**SPEC.** Figure 136, "Namespace Globally Unique Identifier (NGUID), OUI": Defines the identifier composition or namespace of values shown by Namespace Globally Unique Identifier (NGUID), OUI. Keep the value width, issuing authority, uniqueness scope, and reserved values separate. Evidence index: NGUID, OUI, VSP, ID, Namespace.

#### Where this Figure fits

Figure 136 sits in §4.5.5 and acts as a hierarchy checkpoint. Read it after the report mental model has established the owning object and before software turns NGUID into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is an object or capacity relationship Figure. Separate containment, accessibility, identifier reference, and sharing. Adjacent boxes need not be one-to-one, and an identifier is not the physical or logical object it references.

#### Teaching redraw

```text
[Locate source: NGUID]
          ↓
[Extract field: OUI] → [Apply encoding: VSP]
                                      ↓
[Validate evidence: ID]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `NGUID` | Namespace Globally Unique Identifier, a 128-bit global identifier for a namespace. |
| `OUI` | Organizationally Unique Identifier, an IEEE-assigned identifier prefix for an organization. |
| `VSP` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `ID` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `Namespace` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §4.5.5 is the applicable context.
2. Decode NGUID at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check OUI as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 136 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §4.5.5 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes NGUID, OUI, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §4.5.5, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 136. Annotate the bytes containing NGUID, decode them, and independently verify OUI. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of NGUID in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand NGUID and state its unit or object scope?
2. Can the reader explain why OUI is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** NGUID, OUI, VSP, ID, Namespace

**Source keyword index:** none

> Source: NVME-BASE-2.4, Rev. 2.4, §4.5.5, Figure 136, printed pages 171, PDF pages 197

</details>

<details markdown="1">
<summary><strong>Figure 137: Namespace Globally Unique Identifier</strong></summary>

<!-- claim:BASE4-FIG-137-CLAIM figure-table:BASE4-FIG-137 -->

**SPEC.** Figure 137, "Namespace Globally Unique Identifier": Defines the identifier composition or namespace of values shown by Namespace Globally Unique Identifier. Keep the value width, issuing authority, uniqueness scope, and reserved values separate. Evidence index: NGUID, WWN, IEEE, NAA, Namespace.

#### Where this Figure fits

Figure 137 sits in §4.5.5 and acts as a hierarchy checkpoint. Read it after the report mental model has established the owning object and before software turns NGUID into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is an object or capacity relationship Figure. Separate containment, accessibility, identifier reference, and sharing. Adjacent boxes need not be one-to-one, and an identifier is not the physical or logical object it references.

#### Teaching redraw

```text
[Locate source: NGUID]
          ↓
[Extract field: WWN] → [Apply encoding: IEEE]
                                      ↓
[Validate evidence: NAA]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `NGUID` | Namespace Globally Unique Identifier, a 128-bit global identifier for a namespace. |
| `WWN` | World Wide Name, a global naming format used for storage and networking devices. |
| `IEEE` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `NAA` | Network Address Authority, the WWN nibble selecting an identifier format and assignment method. |
| `Namespace` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §4.5.5 is the applicable context.
2. Decode NGUID at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check WWN as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 137 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §4.5.5 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes NGUID, WWN, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §4.5.5, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 137. Annotate the bytes containing NGUID, decode them, and independently verify WWN. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of NGUID in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand NGUID and state its unit or object scope?
2. Can the reader explain why WWN is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** NGUID, WWN, IEEE, NAA, Namespace

**Source keyword index:** none

> Source: NVME-BASE-2.4, Rev. 2.4, §4.5.5, Figure 137, printed pages 171, PDF pages 197

</details>

<details markdown="1">
<summary><strong>Figure 138: Namespace Globally Unique Identifier (NGUID), NGUID similarity to WWN</strong></summary>

<!-- claim:BASE4-FIG-138-CLAIM figure-table:BASE4-FIG-138 -->

**SPEC.** Figure 138, "Namespace Globally Unique Identifier (NGUID), NGUID similarity to WWN": Defines the identifier composition or namespace of values shown by Namespace Globally Unique Identifier (NGUID), NGUID similarity to WWN. Keep the value width, issuing authority, uniqueness scope, and reserved values separate. Evidence index: NGUID, WWN, OUI, NAA, Namespace.

#### Where this Figure fits

Figure 138 sits in §4.5.5 and acts as a hierarchy checkpoint. Read it after the report mental model has established the owning object and before software turns NGUID into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is an object or capacity relationship Figure. Separate containment, accessibility, identifier reference, and sharing. Adjacent boxes need not be one-to-one, and an identifier is not the physical or logical object it references.

#### Teaching redraw

```text
[Locate source: NGUID]
          ↓
[Extract field: WWN] → [Apply encoding: OUI]
                                      ↓
[Validate evidence: NAA]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `NGUID` | Namespace Globally Unique Identifier, a 128-bit global identifier for a namespace. |
| `WWN` | World Wide Name, a global naming format used for storage and networking devices. |
| `OUI` | Organizationally Unique Identifier, an IEEE-assigned identifier prefix for an organization. |
| `NAA` | Network Address Authority, the WWN nibble selecting an identifier format and assignment method. |
| `Namespace` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §4.5.5 is the applicable context.
2. Decode NGUID at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check WWN as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 138 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §4.5.5 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes NGUID, WWN, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §4.5.5, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 138. Annotate the bytes containing NGUID, decode them, and independently verify WWN. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of NGUID in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand NGUID and state its unit or object scope?
2. Can the reader explain why WWN is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** NGUID, WWN, OUI, NAA, Namespace

**Source keyword index:** none

> Source: NVME-BASE-2.4, Rev. 2.4, §4.5.5, Figure 138, printed pages 171, PDF pages 197

</details>

<a id="section-4-6"></a>

### §4.6

<details markdown="1">
<summary><strong>Figure 139: Controller List Format</strong></summary>

<!-- claim:BASE4-FIG-139-CLAIM figure-table:BASE4-FIG-139 -->

**SPEC.** Figure 139, "Controller List Format": Defines the concrete layout or value relationships for Controller List Format. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is NUMCIDS, Controller.

#### Where this Figure fits

Figure 139 sits in §4.6.1 and acts as a layout checkpoint. Read it after the report mental model has established the owning object and before software turns NUMCIDS into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a structure or capability field table. Locate it using the structure base and offset, read in byte/bit order, and separate capability gates, value encoding, and reserved areas. Presence in the table does not mean the function is supported.

#### Teaching redraw

```text
[Locate source: NUMCIDS]
          ↓
[Extract field: Controller] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `NUMCIDS` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `Controller` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §4.6.1 is the applicable context.
2. Decode NUMCIDS at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check Controller as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 139 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §4.6.1 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes NUMCIDS, Controller, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §4.6.1, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 139. Annotate the bytes containing NUMCIDS, decode them, and independently verify Controller. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of NUMCIDS in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand NUMCIDS and state its unit or object scope?
2. Can the reader explain why Controller is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** NUMCIDS, Controller

**Source keyword index:** `may`

> Source: NVME-BASE-2.4, Rev. 2.4, §4.6.1, Figure 139, printed pages 172, PDF pages 198

</details>

<details markdown="1">
<summary><strong>Figure 140: Namespace List Format</strong></summary>

<!-- claim:BASE4-FIG-140-CLAIM figure-table:BASE4-FIG-140 -->

**SPEC.** Figure 140, "Namespace List Format": Defines the concrete layout or value relationships for Namespace List Format. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is ID, Namespace.

#### Where this Figure fits

Figure 140 sits in §4.6.2 and acts as a hierarchy checkpoint. Read it after the report mental model has established the owning object and before software turns ID into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is an object or capacity relationship Figure. Separate containment, accessibility, identifier reference, and sharing. Adjacent boxes need not be one-to-one, and an identifier is not the physical or logical object it references.

#### Teaching redraw

```text
[Locate source: ID]
          ↓
[Extract field: Namespace] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `ID` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `Namespace` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §4.6.2 is the applicable context.
2. Decode ID at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check Namespace as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 140 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §4.6.2 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes ID, Namespace, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §4.6.2, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 140. Annotate the bytes containing ID, decode them, and independently verify Namespace. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

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
2. Can the reader explain why Namespace is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** ID, Namespace

**Source keyword index:** none

> Source: NVME-BASE-2.4, Rev. 2.4, §4.6.2, Figure 140, printed pages 172, PDF pages 198

</details>

<a id="section-4-8"></a>

### §4.8

<details markdown="1">
<summary><strong>Figure 142: UTF-8 Input Processing</strong></summary>

<!-- claim:BASE4-FIG-142-CLAIM figure-table:BASE4-FIG-142 -->

**SPEC.** Figure 142, "UTF-8 Input Processing": Shows the input-validation sequence required by UTF-8 Input Processing. Follow decoding, prohibited-code-point, and truncation checks in order. Evidence index: UTF.

#### Where this Figure fits

Figure 142 sits in §4.8 and acts as a relationship checkpoint. Read it after the report mental model has established the owning object and before software turns UTF into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This Figure explains a specific relationship or example. Identify each component type and owner, then decide whether each connection represents data flow, control flow, containment, or a condition. Visual placement alone creates no normative requirement.

#### Teaching redraw

```text
[Locate source: UTF]
          ↓
[Extract field: evidence] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `UTF` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §4.8 is the applicable context.
2. Decode UTF at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check the cited condition as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 142 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §4.8 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes UTF, the cited condition, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §4.8, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 142. Annotate the bytes containing UTF, decode them, and independently verify the cited condition. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of UTF in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand UTF and state its unit or object scope?
2. Can the reader explain why the cited condition is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** UTF

**Source keyword index:** none

> Source: NVME-BASE-2.4, Rev. 2.4, §4.8, Figure 142, printed pages 175, PDF pages 201

</details>

## Use and limitations

Use the claim IDs as stable PPT traceability keys. Re-check affected claims if the source revision, errata set, or approved scope changes.
