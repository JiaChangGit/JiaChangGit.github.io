---
layout: post
read_time: true
show_date: true
title: "NVMe Base 2.4: Firmware Updates, Firmware Admin Commands, and Get Log Page"
date: 2026-08-31
description: "Source-located PCIe/NVMe report for PPT authoring."
lang: en
img: posts/2026/cat_title.jpg
tags: [NVMe, PCIe, Specification]
category: NVMe
author: Jia-Chang
github: JiaChangGit/JiaChangGit.github.io/tree/main/DOCS/nvme-spec-report
toc: yes
---

# NVMe Base 2.4: Firmware Updates, Firmware Admin Commands, and Get Log Page

Purpose: a source-located engineering report for GitHub Pages and a 100-minute presentation.

Scope: §3.11, §5.2.9, §5.2.10, §5.2.13.1-§5.2.13.2, and §5.2.13.4; main printed pages 135-138, 202-206, 212-319, and 336, plus directly referenced Figure dependencies. Only PCIe/memory-based and common NVMe content appears below.

## Source versions

NVM Express Base Specification, Revision 2.4

Verification date: 2026-08-31. No additional errata, ECNs, Technical Proposals, controller-vendor documents, or source text from the external PCI Express Base Specification are included.

## Reading map

```text
Image Download -> Firmware Commit -> Activate / Reset -> Get Log Page
```

The host downloads image portions using OFST and NUMD, Firmware Commit validates the image and selects a slot and activation action, and log pages plus asynchronous-event state verify the result after reset or immediate activation.

## Normative language

shall is mandatory, may permits a choice, should expresses a preferred recommendation, and optional means support is not required. The report preserves these terms and never promotes one into another.

## Specification findings

### 1. Reset-based firmware update

<!-- claim:BASEFWLOG-FW-RESET -->

A reset-based firmware update downloads the image with one or more Firmware Image Download commands, validates and places it in a firmware slot with Firmware Commit, performs a Controller Level Reset that can activate it, and then reinitializes the controller and I/O queues.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.11, printed pages 135-136, PDF pages 161-162

### 2. Immediate activation

<!-- claim:BASEFWLOG-FW-IMMEDIATE -->

Commit Action 011b requests immediate activation. Once activation starts, affected controllers may report Firmware Activation Starting when the notice is enabled; Firmware Commit remains in progress until activation succeeds or fails and is not a background operation.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.11, printed pages 136-137, PDF pages 162-163

### 3. Activation failure and fallback

<!-- claim:BASEFWLOG-FW-FAILURE -->

If immediate activation requires another reset or exceeds MTFA, the controller completes with the corresponding command-specific status. If the image cannot be loaded, the controller shall revert to the image in the most recently activated slot or an available baseline read-only image and report Firmware Image Load Error.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.11, printed pages 136-137, PDF pages 162-163

### 4. Update-sequence serialization

<!-- claim:BASEFWLOG-FW-SEQUENCE -->

The host should not overlap firmware or boot-partition update sequences and should use one controller or Management Endpoint for a sequence. The first new download after Firmware Commit, and a reset before commit completion, shall cause remaining downloaded portions to be discarded.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.11, printed pages 137, PDF pages 163

### 5. UUID-list stability across revisions

<!-- claim:BASEFWLOG-UUID-LIST -->

UUID-list slots should remain stable across firmware revisions: append new UUIDs, replace removed UUIDs with the NVMe Invalid UUID in place, do not reuse an invalidated slot, and do not shorten the list. If a downloaded image replaces an invalid or different valid UUID with a valid UUID, the controller shall require reset and all affected controllers shall be reset.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.11.1, printed pages 137-138, PDF pages 163-164

### 6. Purpose of Firmware Commit

<!-- claim:BASEFWLOG-COMMIT-PURPOSE -->

Firmware Commit validates the last downloaded image, places it in a firmware slot, and uses Commit Action to select placement only, activation on a later reset, or immediate activation. Controllers in one domain share firmware slots and the same firmware image.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.9, printed pages 202-203, PDF pages 228-229

### 7. Commit Action, slot, and BPID

<!-- claim:BASEFWLOG-COMMIT-CDW10 -->

CDW10 describes the operation through BPID, Commit Action (CA), and Firmware Slot (FS). CA values 000b-011b operate on firmware images, while 110b-111b operate on Boot Partitions. With FS=0h, the controller shall choose an available slot from 1 through 7.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.9, printed pages 203, PDF pages 229

### 8. Multiple Update Detected

<!-- claim:BASEFWLOG-COMMIT-MUD -->

Firmware Commit CQE DW0 uses Multiple Update Detected (MUD) to report overlap detected through a Management Endpoint or Admin Submission Queue. If Identify Controller SMUD is zero, MUD shall be 00b.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.9.1, printed pages 203-204, PDF pages 229-230

### 9. Firmware Commit status

<!-- claim:BASEFWLOG-COMMIT-STATUS -->

Firmware Commit status distinguishes invalid image or slot, required Conventional/NVM Subsystem/Controller Level Reset, MTFA violation, prohibited activation, overlapping ranges, and Boot Partition write lock. A successful commit does not necessarily mean the image is already active.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.9.1, printed pages 204-205, PDF pages 230-231

### 10. Download ranges and ordering

<!-- claim:BASEFWLOG-DOWNLOAD-RANGE -->

Firmware Image Download defines a zero-based dword range with NUMD and OFST. Firmware-image portions may arrive out of order, but Boot Partition portions shall be ordered. The host should avoid overlapping ranges and satisfy FWUG alignment and granularity.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.10, printed pages 205-206, PDF pages 231-232

### 11. DPTR, NUMD, and OFST

<!-- claim:BASEFWLOG-DOWNLOAD-FIELDS -->

DPTR points to the portion, CDW10.NUMD encodes the dword count minus one, and CDW11.OFST encodes the dword offset from the image start. The portion containing the image start shall use OFST=0h. Firmware Image Download does not activate the image.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.10, printed pages 205-206, PDF pages 231-232

### 12. Get Log Page command fields

<!-- claim:BASEFWLOG-LOG-COMMAND -->

Get Log Page uses DPTR and CDW10-CDW14. Its main selector and length fields are LID, LSP, RAE, NUMDL/NUMDU, LSI, LPOL/LPOU, CSI, OT, and UIDX; command-specific fields not defined by the selected log page remain reserved or are ignored as specified by Figure 208.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13, printed pages 212-215, PDF pages 238-241

### 13. Transfer length and offsets

<!-- claim:BASEFWLOG-LOG-LENGTH -->

NUMDL and NUMDU form a zero-based transfer length. When log-page offsets are supported, byte offsets shall work for every log page; index offsets (OT=1) are permitted only when Supported Log Pages reports IOS=1 for that LID. An offset beyond the log page or entry count shall complete with Invalid Field in Command.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13, printed pages 213-215, PDF pages 239-241

### 14. RAE and asynchronous events

<!-- claim:BASEFWLOG-LOG-RAE -->

With RAE=0, a successful Get Log Page clears the corresponding asynchronous event; RAE=1 retains it. If the command does not complete successfully, the controller shall retain the event. For a log page unrelated to asynchronous events, the host should normally clear RAE.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13, printed pages 213, PDF pages 239

### 15. LIDs and data scope

<!-- claim:BASEFWLOG-LOG-SCOPE -->

Figure 209 defines each LID together with CSI usage, data scope, and reference section. NVM-subsystem, domain, controller, and namespace scopes are not interchangeable. For subsystem- or controller-scoped log pages, an NSID other than 0h or FFFFFFFFh shall complete with Invalid Field in Command.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1, printed pages 215-217, PDF pages 241-243

### 16. Supported Log Pages

<!-- claim:BASEFWLOG-LOG-SUPPORT -->

Supported Log Pages (LID 00h) reports support and effects for each LID on the interface that received the command. SUPP, IOS, and the other LID Supported and Effects attributes are interpreted together with controller type, I/O Command Set, and UUID-selection state.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.1, printed pages 217-218, PDF pages 243-244

### 17. Operational log pages

<!-- claim:BASEFWLOG-LOG-OPERATIONS -->

Operational log pages cover Error Information, SMART/Health, Firmware Slot, namespace change, command effects, device self-test, telemetry, Endurance Group, predictable latency, and ANA. A parser first resolves scope from Figure 209, then follows each log page's header, entry count or generation number, and data-area boundaries.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.2-5.2.13.1.13, printed pages 218-244, PDF pages 244-270

### 18. Persistent Event Log

<!-- claim:BASEFWLOG-PERSISTENT-EVENT -->

The Persistent Event Log consists of a log header, event headers, and event-specific data, with LSP controlling establish/read/release context operations. Validate event length, header length, generation number, and context identifier before decoding Event Type. This report retains only common and PCIe-applicable events.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.14, printed pages 244-266, 268-270, PDF pages 270-292, 294-296

### 19. Capacity, management, and FDP logs

<!-- claim:BASEFWLOG-LOG-CAPACITY-FDP -->

Later common log pages cover Endurance Group events, Media Units, capacity configuration, Feature/NVMe-MI effects, lockdown, Boot Partition, management/reachability, device personality, and FDP. Their identifiers, descriptor counts, and variable-length arrays differ and cannot share one fixed parser.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.15-5.2.13.1.33, printed pages 270-301, PDF pages 296-327

### 20. Power, voltage, and sanitize logs

<!-- claim:BASEFWLOG-LOG-POWER-SANITIZE -->

Power Measurement, Voltage Measurement, Sanitize Namespace Status List, Reservation Notification, and Sanitize Status define their own measurement scale, sensor or target selector, generation, and state fields. Apply the matching scale before interpreting measurements and combine sanitize status with its target and state machine.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.34-5.2.13.1.38, printed pages 302-319, PDF pages 328-345

### 21. Log-page applicability for PCIe

<!-- claim:BASEFWLOG-PCIE-LOGS -->

Section 5.2.13.2 states that the memory-based transport model has no transport-specific log page; a PCIe controller uses the common log pages in section 5.2.13.1 with their capability and scope rules.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.2, printed pages 319, PDF pages 345

### 22. Get Log Page completion

<!-- claim:BASEFWLOG-LOG-COMPLETION -->

Get Log Page reports completion on the Admin Completion Queue. Command-specific status distinguishes Invalid Log Page, Invalid Controller Identifier, and I/O Command Set Not Supported. A reserved or unsupported LID completes with Invalid Log Page.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.4, printed pages 336, PDF pages 362

### 23. Figure 337/338 cross-reference discrepancy

<!-- claim:BASEFWLOG-XREF-337 -->

Source section 5.2.9 points the Firmware Revision field to Figure 337, but Figure 337 is titled and populated as Command Set Identifiers; Firmware Revision (FR) appears in Figure 338. With no additional errata in scope, this report preserves the internal cross-reference discrepancy and teaches both Figures rather than silently rewriting the specification.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.9, 5.2.14.1-5.2.14.2.1, printed pages 202, 340, PDF pages 228, 366

## Figure index

This report introduces all 146 in-scope Figures. Use the section links below for the 100-minute presentation path; every Figure remains available as an appendix item. 29 Figures are outside the main section range but are included because the requested text directly references them.

- [§5.2](#section-5-2)

- [Referenced Figure dependencies (outside the main section range)](#section-dependency)

## Figure-by-Figure Guide

The requested text contains no numbered Table reference. The source uses Figure numbers for diagrams and field-layout tables. No source artwork is reproduced; compact field and keyword indexes come from the locally verified PDFs.

<a id="section-5-2"></a>

### §5.2

<details markdown="1">
<summary><strong>Figure 187: Firmware Commit – Command Dword 10</strong></summary>

<!-- claim:BASEFWLOG-FIG-187-CLAIM figure-table:BASEFWLOG-FIG-187 -->

Figure 187, "Firmware Commit – Command Dword 10": Defines the concrete layout or value relationships for Firmware Commit – Command Dword 10. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is BPID, CA, FS, ID, BPINFO.ABPID, Command.

- Purpose: Defines the concrete layout or value relationships for Firmware Commit – Command Dword 10.

- How to read: Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is BPID, CA, FS, ID, BPINFO.ABPID, Command.

- Conditions and limits: Source keyword index: `shall`, `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Use BPID as the first parser checkpoint and CA as a second, independent boundary check. This example adds no requirement.

- Source field index: BPID, CA, FS, ID, BPINFO.ABPID, Command

- Source keyword index: `shall`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.9, Figure 187, printed pages 203, PDF pages 229

</details>

<details markdown="1">
<summary><strong>Figure 188: Firmware Commit – Completion Queue Entry Dword 0</strong></summary>

<!-- claim:BASEFWLOG-FIG-188-CLAIM figure-table:BASEFWLOG-FIG-188 -->

Figure 188, "Firmware Commit – Completion Queue Entry Dword 0": Shows the queue or command relationship expressed by Firmware Commit – Completion Queue Entry Dword 0. Trace ownership and direction from host to SQ, controller, and CQ; keep the indexed elements distinct: MUD, Completion Queue.

- Purpose: Shows the queue or command relationship expressed by Firmware Commit – Completion Queue Entry Dword 0.

- How to read: Trace ownership and direction from host to SQ, controller, and CQ; keep the indexed elements distinct: MUD, Completion Queue.

- Conditions and limits: Source keyword index: `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Trace one command through Figure 188, using MUD and Completion Queue as checkpoints for ownership or pointer movement. This example adds no requirement.

- Source field index: MUD, Completion Queue

- Source keyword index: `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.9.1, Figure 188, printed pages 204, PDF pages 230

</details>

<details markdown="1">
<summary><strong>Figure 189: Firmware Commit – Command Specific Status Values</strong></summary>

<!-- claim:BASEFWLOG-FIG-189-CLAIM figure-table:BASEFWLOG-FIG-189 -->

Figure 189, "Firmware Commit – Command Specific Status Values": Defines the concrete layout or value relationships for Firmware Commit – Command Specific Status Values. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is MTFA, Command.

- Purpose: Defines the concrete layout or value relationships for Firmware Commit – Command Specific Status Values.

- How to read: Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is MTFA, Command.

- Conditions and limits: Source keyword index: `shall`, `should`, `may`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Use MTFA as the first parser checkpoint and Command as a second, independent boundary check. This example adds no requirement.

- Source field index: MTFA, Command

- Source keyword index: `shall`, `should`, `may`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.9.1, Figure 189, printed pages 204-205, PDF pages 230-231

</details>

<details markdown="1">
<summary><strong>Figure 190: Firmware Image Download – Data Pointer</strong></summary>

<!-- claim:BASEFWLOG-FIG-190-CLAIM figure-table:BASEFWLOG-FIG-190 -->

Figure 190, "Firmware Image Download – Data Pointer": Defines how Firmware Image Download – Data Pointer identifies the destination or source buffer for this command. Resolve pointer type and address before checking transfer length and alignment. Evidence index: DPTR.

- Purpose: Defines how Firmware Image Download – Data Pointer identifies the destination or source buffer for this command.

- How to read: Resolve pointer type and address before checking transfer length and alignment. Evidence index: DPTR.

- Conditions and limits: Source keyword index: `should`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Validate the pointer form represented by DPTR, then confirm the boundary associated with the cited condition before starting the transfer. This example adds no requirement.

- Source field index: DPTR

- Source keyword index: `should`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.10, Figure 190, printed pages 205, PDF pages 231

</details>

<details markdown="1">
<summary><strong>Figure 191: Firmware Image Download – Command Dword 10</strong></summary>

<!-- claim:BASEFWLOG-FIG-191-CLAIM figure-table:BASEFWLOG-FIG-191 -->

Figure 191, "Firmware Image Download – Command Dword 10": Defines the concrete layout or value relationships for Firmware Image Download – Command Dword 10. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is NUMD, FWUG, Command.

- Purpose: Defines the concrete layout or value relationships for Firmware Image Download – Command Dword 10.

- How to read: Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is NUMD, FWUG, Command.

- Conditions and limits: Source keyword index: `may`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Use NUMD as the first parser checkpoint and FWUG as a second, independent boundary check. This example adds no requirement.

- Source field index: NUMD, FWUG, Command

- Source keyword index: `may`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.10, Figure 191, printed pages 205, PDF pages 231

</details>

<details markdown="1">
<summary><strong>Figure 192: Firmware Image Download – Command Dword 11</strong></summary>

<!-- claim:BASEFWLOG-FIG-192-CLAIM figure-table:BASEFWLOG-FIG-192 -->

Figure 192, "Firmware Image Download – Command Dword 11": Defines the concrete layout or value relationships for Firmware Image Download – Command Dword 11. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is OFST, FWUG.

- Purpose: Defines the concrete layout or value relationships for Firmware Image Download – Command Dword 11.

- How to read: Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is OFST, FWUG.

- Conditions and limits: The Figure is explanatory or structural; this guide does not turn its visual relationship into a new requirement.

- Informative example: Use OFST as the first parser checkpoint and FWUG as a second, independent boundary check. This example adds no requirement.

- Source field index: OFST, FWUG

- Source keyword index: none

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.10, Figure 192, printed pages 206, PDF pages 232

</details>

<details markdown="1">
<summary><strong>Figure 193: Firmware Image Download – Command Specific Status Values</strong></summary>

<!-- claim:BASEFWLOG-FIG-193-CLAIM figure-table:BASEFWLOG-FIG-193 -->

Figure 193, "Firmware Image Download – Command Specific Status Values": Defines the concrete layout or value relationships for Firmware Image Download – Command Specific Status Values. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is Overlapping Range.

- Purpose: Defines the concrete layout or value relationships for Firmware Image Download – Command Specific Status Values.

- How to read: Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is Overlapping Range.

- Conditions and limits: Source keyword index: `may`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Use Overlapping Range as the first parser checkpoint and the cited condition as a second, independent boundary check. This example adds no requirement.

- Source field index: Overlapping Range

- Source keyword index: `may`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.10, Figure 193, printed pages 206, PDF pages 232

</details>

<details markdown="1">
<summary><strong>Figure 203: Get Log Page – Data Pointer</strong></summary>

<!-- claim:BASEFWLOG-FIG-203-CLAIM figure-table:BASEFWLOG-FIG-203 -->

Figure 203, "Get Log Page – Data Pointer": Defines how Get Log Page – Data Pointer identifies the destination or source buffer for this command. Resolve pointer type and address before checking transfer length and alignment. Evidence index: DPTR.

- Purpose: Defines how Get Log Page – Data Pointer identifies the destination or source buffer for this command.

- How to read: Resolve pointer type and address before checking transfer length and alignment. Evidence index: DPTR.

- Conditions and limits: The Figure is explanatory or structural; this guide does not turn its visual relationship into a new requirement.

- Informative example: Validate the pointer form represented by DPTR, then confirm the boundary associated with the cited condition before starting the transfer. This example adds no requirement.

- Source field index: DPTR

- Source keyword index: none

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13, Figure 203, printed pages 213, PDF pages 239

</details>

<details markdown="1">
<summary><strong>Figure 204: Get Log Page – Command Dword 10</strong></summary>

<!-- claim:BASEFWLOG-FIG-204-CLAIM figure-table:BASEFWLOG-FIG-204 -->

Figure 204, "Get Log Page – Command Dword 10": Defines the returned log-page layout and selection context for Get Log Page – Command Dword 10. Start with the fixed header and scope, validate counts or lengths, then walk entries or data areas in order. Evidence index: NUMDL, RAE, LSP, LID, NUMDU, Command.

- Purpose: Defines the returned log-page layout and selection context for Get Log Page – Command Dword 10.

- How to read: Start with the fixed header and scope, validate counts or lengths, then walk entries or data areas in order. Evidence index: NUMDL, RAE, LSP, LID, NUMDU, Command.

- Conditions and limits: Source keyword index: `shall`, `should`, `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Read NUMDL first, use RAE as an independent size or identity check, and stop before any unreturned byte. This example adds no requirement.

- Source field index: NUMDL, RAE, LSP, LID, NUMDU, Command

- Source keyword index: `shall`, `should`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13, Figure 204, printed pages 213, PDF pages 239

</details>

<details markdown="1">
<summary><strong>Figure 205: Get Log Page – Command Dword 11</strong></summary>

<!-- claim:BASEFWLOG-FIG-205-CLAIM figure-table:BASEFWLOG-FIG-205 -->

Figure 205, "Get Log Page – Command Dword 11": Defines the returned log-page layout and selection context for Get Log Page – Command Dword 11. Start with the fixed header and scope, validate counts or lengths, then walk entries or data areas in order. Evidence index: LSI, NUMDU, Command.

- Purpose: Defines the returned log-page layout and selection context for Get Log Page – Command Dword 11.

- How to read: Start with the fixed header and scope, validate counts or lengths, then walk entries or data areas in order. Evidence index: LSI, NUMDU, Command.

- Conditions and limits: Source keyword index: `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Read LSI first, use NUMDU as an independent size or identity check, and stop before any unreturned byte. This example adds no requirement.

- Source field index: LSI, NUMDU, Command

- Source keyword index: `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13, Figure 205, printed pages 214, PDF pages 240

</details>

<details markdown="1">
<summary><strong>Figure 206: Get Log Page – Command Dword 12</strong></summary>

<!-- claim:BASEFWLOG-FIG-206-CLAIM figure-table:BASEFWLOG-FIG-206 -->

Figure 206, "Get Log Page – Command Dword 12": Defines the returned log-page layout and selection context for Get Log Page – Command Dword 12. Start with the fixed header and scope, validate counts or lengths, then walk entries or data areas in order. Evidence index: LPOL, OT, LPOU, IOS, LID, Command.

- Purpose: Defines the returned log-page layout and selection context for Get Log Page – Command Dword 12.

- How to read: Start with the fixed header and scope, validate counts or lengths, then walk entries or data areas in order. Evidence index: LPOL, OT, LPOU, IOS, LID, Command.

- Conditions and limits: Source keyword index: `shall`, `may`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Read LPOL first, use OT as an independent size or identity check, and stop before any unreturned byte. This example adds no requirement.

- Source field index: LPOL, OT, LPOU, IOS, LID, Command

- Source keyword index: `shall`, `may`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13, Figure 206, printed pages 214, PDF pages 240

</details>

<details markdown="1">
<summary><strong>Figure 207: Get Log Page – Command Dword 13</strong></summary>

<!-- claim:BASEFWLOG-FIG-207-CLAIM figure-table:BASEFWLOG-FIG-207 -->

Figure 207, "Get Log Page – Command Dword 13": Defines the returned log-page layout and selection context for Get Log Page – Command Dword 13. Start with the fixed header and scope, validate counts or lengths, then walk entries or data areas in order. Evidence index: LPOU, UUID, Command.

- Purpose: Defines the returned log-page layout and selection context for Get Log Page – Command Dword 13.

- How to read: Start with the fixed header and scope, validate counts or lengths, then walk entries or data areas in order. Evidence index: LPOU, UUID, Command.

- Conditions and limits: The Figure is explanatory or structural; this guide does not turn its visual relationship into a new requirement.

- Informative example: Read LPOU first, use UUID as an independent size or identity check, and stop before any unreturned byte. This example adds no requirement.

- Source field index: LPOU, UUID, Command

- Source keyword index: none

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13, Figure 207, printed pages 214, PDF pages 240

</details>

<details markdown="1">
<summary><strong>Figure 208: Get Log Page – Command Dword 14</strong></summary>

<!-- claim:BASEFWLOG-FIG-208-CLAIM figure-table:BASEFWLOG-FIG-208 -->

Figure 208, "Get Log Page – Command Dword 14": Defines the returned log-page layout and selection context for Get Log Page – Command Dword 14. Start with the fixed header and scope, validate counts or lengths, then walk entries or data areas in order. Evidence index: CSI, CC.CSS, Command.

- Purpose: Defines the returned log-page layout and selection context for Get Log Page – Command Dword 14.

- How to read: Start with the fixed header and scope, validate counts or lengths, then walk entries or data areas in order. Evidence index: CSI, CC.CSS, Command.

- Conditions and limits: Source keyword index: `shall`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Read CSI first, use CC.CSS as an independent size or identity check, and stop before any unreturned byte. This example adds no requirement.

- Source field index: CSI, CC.CSS, Command

- Source keyword index: `shall`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13, Figure 208, printed pages 214-215, PDF pages 240-241

</details>

<details markdown="1">
<summary><strong>Figure 209: Get Log Page – Log Page Identifiers</strong></summary>

<!-- claim:BASEFWLOG-FIG-209-CLAIM figure-table:BASEFWLOG-FIG-209 -->

Figure 209, "Get Log Page – Log Page Identifiers": Defines the returned log-page layout and selection context for Get Log Page – Log Page Identifiers. Start with the fixed header and scope, validate counts or lengths, then walk entries or data areas in order. Evidence index: CSI8, SMART, MI, FDP, SDSO, DSTO, UUID, MDS.

- Purpose: Defines the returned log-page layout and selection context for Get Log Page – Log Page Identifiers.

- How to read: Start with the fixed header and scope, validate counts or lengths, then walk entries or data areas in order. Evidence index: CSI8, SMART, MI, FDP, SDSO, DSTO, UUID, MDS.

- Conditions and limits: Source keyword index: `may`, `optional`, `reserved`. The index locates normative language but does not replace the condition attached to each field. Only the PCIe/memory-based portion is in scope.

- Informative example: Read CSI8 first, use SMART as an independent size or identity check, and stop before any unreturned byte. This example adds no requirement.

- Source field index: CSI8, SMART, MI, FDP, SDSO, DSTO, UUID, MDS

- Source keyword index: `may`, `optional`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13, Figure 209, printed pages 215-216, PDF pages 241-242

</details>

<details markdown="1">
<summary><strong>Figure 210: Supported Log Pages Log Page</strong></summary>

<!-- claim:BASEFWLOG-FIG-210-CLAIM figure-table:BASEFWLOG-FIG-210 -->

Figure 210, "Supported Log Pages Log Page": Defines the returned log-page layout and selection context for Supported Log Pages Log Page. Start with the fixed header and scope, validate counts or lengths, then walk entries or data areas in order. Evidence index: LIDS0, LIDS1, LIDS254, LIDS255, LID.

- Purpose: Defines the returned log-page layout and selection context for Supported Log Pages Log Page.

- How to read: Start with the fixed header and scope, validate counts or lengths, then walk entries or data areas in order. Evidence index: LIDS0, LIDS1, LIDS254, LIDS255, LID.

- Conditions and limits: The Figure is explanatory or structural; this guide does not turn its visual relationship into a new requirement.

- Informative example: Read LIDS0 first, use LIDS1 as an independent size or identity check, and stop before any unreturned byte. This example adds no requirement.

- Source field index: LIDS0, LIDS1, LIDS254, LIDS255, LID

- Source keyword index: none

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.1, Figure 210, printed pages 217, PDF pages 243

</details>

<details markdown="1">
<summary><strong>Figure 211: LID Supported and Effects Data Structure</strong></summary>

<!-- claim:BASEFWLOG-FIG-211-CLAIM figure-table:BASEFWLOG-FIG-211 -->

Figure 211, "LID Supported and Effects Data Structure": Defines the concrete layout or value relationships for LID Supported and Effects Data Structure. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is LIDSP, IOS, LSUPP, LID, OT, SPEDS, PA.

- Purpose: Defines the concrete layout or value relationships for LID Supported and Effects Data Structure.

- How to read: Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is LIDSP, IOS, LSUPP, LID, OT, SPEDS, PA.

- Conditions and limits: Source keyword index: `shall`, `should`, `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Use LIDSP as the first parser checkpoint and IOS as a second, independent boundary check. This example adds no requirement.

- Source field index: LIDSP, IOS, LSUPP, LID, OT, SPEDS, PA

- Source keyword index: `shall`, `should`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.1, Figure 211, printed pages 217-218, PDF pages 243-244

</details>

<details markdown="1">
<summary><strong>Figure 212: Error Information Log Entry Data Structure</strong></summary>

<!-- claim:BASEFWLOG-FIG-212-CLAIM figure-table:BASEFWLOG-FIG-212 -->

Figure 212, "Error Information Log Entry Data Structure": Defines the status/error classification represented by Error Information Log Entry Data Structure. Resolve the category before the individual code or flag; keep reserved values uninterpreted. Evidence index: ECNT, SQID, CID, STS, STATUS, PEL, BITLOC, BYTLOC.

- Purpose: Defines the status/error classification represented by Error Information Log Entry Data Structure.

- How to read: Resolve the category before the individual code or flag; keep reserved values uninterpreted. Evidence index: ECNT, SQID, CID, STS, STATUS, PEL, BITLOC, BYTLOC.

- Conditions and limits: Source keyword index: `shall`, `should`, `may`, `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: For one reported condition, identify ECNT first and then check SQID instead of decoding an isolated numeric value. This example adds no requirement.

- Source field index: ECNT, SQID, CID, STS, STATUS, PEL, BITLOC, BYTLOC

- Source keyword index: `shall`, `should`, `may`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.2, Figure 212, printed pages 218-220, PDF pages 244-246

</details>

<details markdown="1">
<summary><strong>Figure 213: SMART / Health Information Log Page</strong></summary>

<!-- claim:BASEFWLOG-FIG-213-CLAIM figure-table:BASEFWLOG-FIG-213 -->

Figure 213, "SMART / Health Information Log Page": Defines the returned log-page layout and selection context for SMART / Health Information Log Page. Start with the fixed header and scope, validate counts or lengths, then walk entries or data areas in order. Evidence index: CW, IPS, PMRRO, VMBF, AMRO, NDR, TTC, ASCBT.

- Purpose: Defines the returned log-page layout and selection context for SMART / Health Information Log Page.

- How to read: Start with the fixed header and scope, validate counts or lengths, then walk entries or data areas in order. Evidence index: CW, IPS, PMRRO, VMBF, AMRO, NDR, TTC, ASCBT.

- Conditions and limits: Source keyword index: `shall not`, `shall`, `may`, `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Read CW first, use IPS as an independent size or identity check, and stop before any unreturned byte. This example adds no requirement.

- Source field index: CW, IPS, PMRRO, VMBF, AMRO, NDR, TTC, ASCBT

- Source keyword index: `shall not`, `shall`, `may`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.3, Figure 213, printed pages 221-225, PDF pages 247-251

</details>

<details markdown="1">
<summary><strong>Figure 214: Temperature Sensor Data Structure</strong></summary>

<!-- claim:BASEFWLOG-FIG-214-CLAIM figure-table:BASEFWLOG-FIG-214 -->

Figure 214, "Temperature Sensor Data Structure": Defines the concrete layout or value relationships for Temperature Sensor Data Structure. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is TST.

- Purpose: Defines the concrete layout or value relationships for Temperature Sensor Data Structure.

- How to read: Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is TST.

- Conditions and limits: Source keyword index: `may`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Use TST as the first parser checkpoint and the cited condition as a second, independent boundary check. This example adds no requirement.

- Source field index: TST

- Source keyword index: `may`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.3, Figure 214, printed pages 225, PDF pages 251

</details>

<details markdown="1">
<summary><strong>Figure 215: Firmware Slot Information Log Page</strong></summary>

<!-- claim:BASEFWLOG-FIG-215-CLAIM figure-table:BASEFWLOG-FIG-215 -->

Figure 215, "Firmware Slot Information Log Page": Defines the returned log-page layout and selection context for Firmware Slot Information Log Page. Start with the fixed header and scope, validate counts or lengths, then walk entries or data areas in order. Evidence index: AFI, NAFS, CAFS, FRS1, FRS2, FRS3, FRS4, FRS5.

- Purpose: Defines the returned log-page layout and selection context for Firmware Slot Information Log Page.

- How to read: Start with the fixed header and scope, validate counts or lengths, then walk entries or data areas in order. Evidence index: AFI, NAFS, CAFS, FRS1, FRS2, FRS3, FRS4, FRS5.

- Conditions and limits: Source keyword index: `shall`, `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Read AFI first, use NAFS as an independent size or identity check, and stop before any unreturned byte. This example adds no requirement.

- Source field index: AFI, NAFS, CAFS, FRS1, FRS2, FRS3, FRS4, FRS5

- Source keyword index: `shall`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.4, Figure 215, printed pages 226, PDF pages 252

</details>

<details markdown="1">
<summary><strong>Figure 216: Commands Supported and Effects Log Page</strong></summary>

<!-- claim:BASEFWLOG-FIG-216-CLAIM figure-table:BASEFWLOG-FIG-216 -->

Figure 216, "Commands Supported and Effects Log Page": Defines the returned log-page layout and selection context for Commands Supported and Effects Log Page. Start with the fixed header and scope, validate counts or lengths, then walk entries or data areas in order. Evidence index: ACS0, ACS1, ACS254, ACS255, IOCS0, IOCS1, IOCS254, IOCS255.

- Purpose: Defines the returned log-page layout and selection context for Commands Supported and Effects Log Page.

- How to read: Start with the fixed header and scope, validate counts or lengths, then walk entries or data areas in order. Evidence index: ACS0, ACS1, ACS254, ACS255, IOCS0, IOCS1, IOCS254, IOCS255.

- Conditions and limits: Source keyword index: `should`, `may`, `optional`, `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Read ACS0 first, use ACS1 as an independent size or identity check, and stop before any unreturned byte. This example adds no requirement.

- Source field index: ACS0, ACS1, ACS254, ACS255, IOCS0, IOCS1, IOCS254, IOCS255

- Source keyword index: `should`, `may`, `optional`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.6, Figure 216, printed pages 227, PDF pages 253

</details>

<details markdown="1">
<summary><strong>Figure 217: Commands Supported and Effects Data Structure</strong></summary>

<!-- claim:BASEFWLOG-FIG-217-CLAIM figure-table:BASEFWLOG-FIG-217 -->

Figure 217, "Commands Supported and Effects Data Structure": Defines the concrete layout or value relationships for Commands Supported and Effects Data Structure. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is CSP, NSSCPE, DSCPE, EGSCPE, NSETSCPE, CSCPE, NSCPE, USS.

- Purpose: Defines the concrete layout or value relationships for Commands Supported and Effects Data Structure.

- How to read: Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is CSP, NSSCPE, DSCPE, EGSCPE, NSETSCPE, CSCPE, NSCPE, USS.

- Conditions and limits: Source keyword index: `should not`, `shall`, `should`, `may`, `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Use CSP as the first parser checkpoint and NSSCPE as a second, independent boundary check. This example adds no requirement.

- Source field index: CSP, NSSCPE, DSCPE, EGSCPE, NSETSCPE, CSCPE, NSCPE, USS

- Source keyword index: `should not`, `shall`, `should`, `may`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.6, Figure 217, printed pages 228-229, PDF pages 254-255

</details>

<details markdown="1">
<summary><strong>Figure 218: Device Self-test Log Page</strong></summary>

<!-- claim:BASEFWLOG-FIG-218-CLAIM figure-table:BASEFWLOG-FIG-218 -->

Figure 218, "Device Self-test Log Page": Defines the returned log-page layout and selection context for Device Self-test Log Page. Start with the fixed header and scope, validate counts or lengths, then walk entries or data areas in order. Evidence index: CDSTO, DSTOS, CDSTC, DSTCS, RDS1, RDS2, RDS19, RDS20.

- Purpose: Defines the returned log-page layout and selection context for Device Self-test Log Page.

- How to read: Start with the fixed header and scope, validate counts or lengths, then walk entries or data areas in order. Evidence index: CDSTO, DSTOS, CDSTC, DSTCS, RDS1, RDS2, RDS19, RDS20.

- Conditions and limits: Source keyword index: `shall not`, `shall`, `should`, `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Read CDSTO first, use DSTOS as an independent size or identity check, and stop before any unreturned byte. This example adds no requirement.

- Source field index: CDSTO, DSTOS, CDSTC, DSTCS, RDS1, RDS2, RDS19, RDS20

- Source keyword index: `shall not`, `shall`, `should`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.7, Figure 218, printed pages 230, PDF pages 256

</details>

<details markdown="1">
<summary><strong>Figure 219: Self-test Result Data Structure</strong></summary>

<!-- claim:BASEFWLOG-FIG-219-CLAIM figure-table:BASEFWLOG-FIG-219 -->

Figure 219, "Self-test Result Data Structure": Defines the concrete layout or value relationships for Self-test Result Data Structure. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is DSTS, DSTC, DSTR, SEGN, VDINFO, SCVLD, SCTVLD, FVLD.

- Purpose: Defines the concrete layout or value relationships for Self-test Result Data Structure.

- How to read: Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is DSTS, DSTC, DSTR, SEGN, VDINFO, SCVLD, SCTVLD, FVLD.

- Conditions and limits: Source keyword index: `should`, `may`, `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Use DSTS as the first parser checkpoint and DSTC as a second, independent boundary check. This example adds no requirement.

- Source field index: DSTS, DSTC, DSTR, SEGN, VDINFO, SCVLD, SCTVLD, FVLD

- Source keyword index: `should`, `may`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.7, Figure 219, printed pages 231-232, PDF pages 257-258

</details>

<details markdown="1">
<summary><strong>Figure 220: Telemetry Host-Initiated Log Specific Parameter Field</strong></summary>

<!-- claim:BASEFWLOG-FIG-220-CLAIM figure-table:BASEFWLOG-FIG-220 -->

Figure 220, "Telemetry Host-Initiated Log Specific Parameter Field": Defines the concrete layout or value relationships for Telemetry Host-Initiated Log Specific Parameter Field. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is MCDA, CTHID, MCDAS, LID, DA4S, ETDAS.

- Purpose: Defines the concrete layout or value relationships for Telemetry Host-Initiated Log Specific Parameter Field.

- How to read: Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is MCDA, CTHID, MCDAS, LID, DA4S, ETDAS.

- Conditions and limits: Source keyword index: `shall not`, `shall`, `may`, `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Use MCDA as the first parser checkpoint and CTHID as a second, independent boundary check. This example adds no requirement.

- Source field index: MCDA, CTHID, MCDAS, LID, DA4S, ETDAS

- Source keyword index: `shall not`, `shall`, `may`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.8, Figure 220, printed pages 232-233, PDF pages 258-259

</details>

<details markdown="1">
<summary><strong>Figure 221: Telemetry Host-Initiated Log Page</strong></summary>

<!-- claim:BASEFWLOG-FIG-221-CLAIM figure-table:BASEFWLOG-FIG-221 -->

Figure 221, "Telemetry Host-Initiated Log Page": Defines the returned log-page layout and selection context for Telemetry Host-Initiated Log Page. Start with the fixed header and scope, validate counts or lengths, then walk entries or data areas in order. Evidence index: LID, IEEE, THDA1LB, THDA2LB, THDA3LB, THDA4LB, THS, THDGN.

- Purpose: Defines the returned log-page layout and selection context for Telemetry Host-Initiated Log Page.

- How to read: Start with the fixed header and scope, validate counts or lengths, then walk entries or data areas in order. Evidence index: LID, IEEE, THDA1LB, THDA2LB, THDA3LB, THDA4LB, THS, THDGN.

- Conditions and limits: Source keyword index: `shall not`, `shall`, `should`, `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Read LID first, use IEEE as an independent size or identity check, and stop before any unreturned byte. This example adds no requirement.

- Source field index: LID, IEEE, THDA1LB, THDA2LB, THDA3LB, THDA4LB, THS, THDGN

- Source keyword index: `shall not`, `shall`, `should`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.8, Figure 221, printed pages 234-235, PDF pages 260-261

</details>

<details markdown="1">
<summary><strong>Figure 222: Telemetry Host-Initiated Log Page - LID Specific Parameter Field</strong></summary>

<!-- claim:BASEFWLOG-FIG-222-CLAIM figure-table:BASEFWLOG-FIG-222 -->

Figure 222, "Telemetry Host-Initiated Log Page - LID Specific Parameter Field": Defines the returned log-page layout and selection context for Telemetry Host-Initiated Log Page - LID Specific Parameter Field. Start with the fixed header and scope, validate counts or lengths, then walk entries or data areas in order. Evidence index: MCDAS, LID.

- Purpose: Defines the returned log-page layout and selection context for Telemetry Host-Initiated Log Page - LID Specific Parameter Field.

- How to read: Start with the fixed header and scope, validate counts or lengths, then walk entries or data areas in order. Evidence index: MCDAS, LID.

- Conditions and limits: Source keyword index: `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Read MCDAS first, use LID as an independent size or identity check, and stop before any unreturned byte. This example adds no requirement.

- Source field index: MCDAS, LID

- Source keyword index: `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.8, Figure 222, printed pages 235, PDF pages 261

</details>

<details markdown="1">
<summary><strong>Figure 223: Telemetry Controller-Initiated Log Page</strong></summary>

<!-- claim:BASEFWLOG-FIG-223-CLAIM figure-table:BASEFWLOG-FIG-223 -->

Figure 223, "Telemetry Controller-Initiated Log Page": Defines the returned log-page layout and selection context for Telemetry Controller-Initiated Log Page. Start with the fixed header and scope, validate counts or lengths, then walk entries or data areas in order. Evidence index: LID, IEEE, TCDA1LB, TCDA2LB, TCDA3LB, TCDA4LB, TCS, TCDA.

- Purpose: Defines the returned log-page layout and selection context for Telemetry Controller-Initiated Log Page.

- How to read: Start with the fixed header and scope, validate counts or lengths, then walk entries or data areas in order. Evidence index: LID, IEEE, TCDA1LB, TCDA2LB, TCDA3LB, TCDA4LB, TCS, TCDA.

- Conditions and limits: Source keyword index: `shall not`, `shall`, `should`, `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Read LID first, use IEEE as an independent size or identity check, and stop before any unreturned byte. This example adds no requirement.

- Source field index: LID, IEEE, TCDA1LB, TCDA2LB, TCDA3LB, TCDA4LB, TCS, TCDA

- Source keyword index: `shall not`, `shall`, `should`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.9, Figure 223, printed pages 236-237, PDF pages 262-263

</details>

<details markdown="1">
<summary><strong>Figure 224: Endurance Group Identifier - Log Specific Identifier</strong></summary>

<!-- claim:BASEFWLOG-FIG-224-CLAIM figure-table:BASEFWLOG-FIG-224 -->

Figure 224, "Endurance Group Identifier - Log Specific Identifier": Defines the identifier composition or namespace of values shown by Endurance Group Identifier - Log Specific Identifier. Keep the value width, issuing authority, uniqueness scope, and reserved values separate. Evidence index: ENDGID, Endurance Group.

- Purpose: Defines the identifier composition or namespace of values shown by Endurance Group Identifier - Log Specific Identifier.

- How to read: Keep the value width, issuing authority, uniqueness scope, and reserved values separate. Evidence index: ENDGID, Endurance Group.

- Conditions and limits: The Figure is explanatory or structural; this guide does not turn its visual relationship into a new requirement.

- Informative example: Parse ENDGID at its defined width, then validate the scope associated with Endurance Group before using it as an identity key. This example adds no requirement.

- Source field index: ENDGID, Endurance Group

- Source keyword index: none

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.10, Figure 224, printed pages 237, PDF pages 263

</details>

<details markdown="1">
<summary><strong>Figure 225: Endurance Group Information Log Page</strong></summary>

<!-- claim:BASEFWLOG-FIG-225-CLAIM figure-table:BASEFWLOG-FIG-225 -->

Figure 225, "Endurance Group Information Log Page": Defines the returned log-page layout and selection context for Endurance Group Information Log Page. Start with the fixed header and scope, validate counts or lengths, then walk entries or data areas in order. Evidence index: EGCW, EGRO, EGDR, EGASB, EGFEAT, AVSP, AVSPT, PUSED.

- Purpose: Defines the returned log-page layout and selection context for Endurance Group Information Log Page.

- How to read: Start with the fixed header and scope, validate counts or lengths, then walk entries or data areas in order. Evidence index: EGCW, EGRO, EGDR, EGASB, EGFEAT, AVSP, AVSPT, PUSED.

- Conditions and limits: Source keyword index: `shall not`, `shall`, `may`, `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Read EGCW first, use EGRO as an independent size or identity check, and stop before any unreturned byte. This example adds no requirement.

- Source field index: EGCW, EGRO, EGDR, EGASB, EGFEAT, AVSP, AVSPT, PUSED

- Source keyword index: `shall not`, `shall`, `may`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.10, Figure 225, printed pages 238-239, PDF pages 264-265

</details>

<details markdown="1">
<summary><strong>Figure 226: NVM Set Identifier – Log Specific Identifier</strong></summary>

<!-- claim:BASEFWLOG-FIG-226-CLAIM figure-table:BASEFWLOG-FIG-226 -->

Figure 226, "NVM Set Identifier – Log Specific Identifier": Defines the identifier composition or namespace of values shown by NVM Set Identifier – Log Specific Identifier. Keep the value width, issuing authority, uniqueness scope, and reserved values separate. Evidence index: NVMSETID, NVM Set.

- Purpose: Defines the identifier composition or namespace of values shown by NVM Set Identifier – Log Specific Identifier.

- How to read: Keep the value width, issuing authority, uniqueness scope, and reserved values separate. Evidence index: NVMSETID, NVM Set.

- Conditions and limits: The Figure is explanatory or structural; this guide does not turn its visual relationship into a new requirement.

- Informative example: Parse NVMSETID at its defined width, then validate the scope associated with NVM Set before using it as an identity key. This example adds no requirement.

- Source field index: NVMSETID, NVM Set

- Source keyword index: none

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.11, Figure 226, printed pages 240, PDF pages 266

</details>

<details markdown="1">
<summary><strong>Figure 227: Predictable Latency Per NVM Set Log Page</strong></summary>

<!-- claim:BASEFWLOG-FIG-227-CLAIM figure-table:BASEFWLOG-FIG-227 -->

Figure 227, "Predictable Latency Per NVM Set Log Page": Defines the returned log-page layout and selection context for Predictable Latency Per NVM Set Log Page. Start with the fixed header and scope, validate counts or lengths, then walk entries or data areas in order. Evidence index: STSNVMS, PLMW, ETYP, DEAT, MVEAT, DTWRT, DTWWT, DTWTM.

- Purpose: Defines the returned log-page layout and selection context for Predictable Latency Per NVM Set Log Page.

- How to read: Start with the fixed header and scope, validate counts or lengths, then walk entries or data areas in order. Evidence index: STSNVMS, PLMW, ETYP, DEAT, MVEAT, DTWRT, DTWWT, DTWTM.

- Conditions and limits: Source keyword index: `may`, `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Read STSNVMS first, use PLMW as an independent size or identity check, and stop before any unreturned byte. This example adds no requirement.

- Source field index: STSNVMS, PLMW, ETYP, DEAT, MVEAT, DTWRT, DTWWT, DTWTM

- Source keyword index: `may`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.11, Figure 227, printed pages 240-241, PDF pages 266-267

</details>

<details markdown="1">
<summary><strong>Figure 228: Predictable Latency Event Aggregate Log Page</strong></summary>

<!-- claim:BASEFWLOG-FIG-228-CLAIM figure-table:BASEFWLOG-FIG-228 -->

Figure 228, "Predictable Latency Event Aggregate Log Page": Defines the returned log-page layout and selection context for Predictable Latency Event Aggregate Log Page. Start with the fixed header and scope, validate counts or lengths, then walk entries or data areas in order. Evidence index: NUMENT, NEMENT.

- Purpose: Defines the returned log-page layout and selection context for Predictable Latency Event Aggregate Log Page.

- How to read: Start with the fixed header and scope, validate counts or lengths, then walk entries or data areas in order. Evidence index: NUMENT, NEMENT.

- Conditions and limits: The Figure is explanatory or structural; this guide does not turn its visual relationship into a new requirement.

- Informative example: Read NUMENT first, use NEMENT as an independent size or identity check, and stop before any unreturned byte. This example adds no requirement.

- Source field index: NUMENT, NEMENT

- Source keyword index: none

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.12, Figure 228, printed pages 241, PDF pages 267

</details>

<details markdown="1">
<summary><strong>Figure 229: Asymmetric Namespace Access Log Specific Parameter Field</strong></summary>

<!-- claim:BASEFWLOG-FIG-229-CLAIM figure-table:BASEFWLOG-FIG-229 -->

Figure 229, "Asymmetric Namespace Access Log Specific Parameter Field": Defines the concrete layout or value relationships for Asymmetric Namespace Access Log Specific Parameter Field. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is RGO, ANA, NSID, Namespace.

- Purpose: Defines the concrete layout or value relationships for Asymmetric Namespace Access Log Specific Parameter Field.

- How to read: Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is RGO, ANA, NSID, Namespace.

- Conditions and limits: Source keyword index: `shall`, `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Use RGO as the first parser checkpoint and ANA as a second, independent boundary check. This example adds no requirement.

- Source field index: RGO, ANA, NSID, Namespace

- Source keyword index: `shall`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.13, Figure 229, printed pages 242, PDF pages 268

</details>

<details markdown="1">
<summary><strong>Figure 230: Asymmetric Namespace Access Log Page</strong></summary>

<!-- claim:BASEFWLOG-FIG-230-CLAIM figure-table:BASEFWLOG-FIG-230 -->

Figure 230, "Asymmetric Namespace Access Log Page": Defines the returned log-page layout and selection context for Asymmetric Namespace Access Log Page. Start with the fixed header and scope, validate counts or lengths, then walk entries or data areas in order. Evidence index: CHGC, NAGD, ANA, NSID, Namespace.

- Purpose: Defines the returned log-page layout and selection context for Asymmetric Namespace Access Log Page.

- How to read: Start with the fixed header and scope, validate counts or lengths, then walk entries or data areas in order. Evidence index: CHGC, NAGD, ANA, NSID, Namespace.

- Conditions and limits: Source keyword index: `shall`, `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Read CHGC first, use NAGD as an independent size or identity check, and stop before any unreturned byte. This example adds no requirement.

- Source field index: CHGC, NAGD, ANA, NSID, Namespace

- Source keyword index: `shall`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.13, Figure 230, printed pages 242-243, PDF pages 268-269

</details>

<details markdown="1">
<summary><strong>Figure 231: ANA Group Descriptor format</strong></summary>

<!-- claim:BASEFWLOG-FIG-231-CLAIM figure-table:BASEFWLOG-FIG-231 -->

Figure 231, "ANA Group Descriptor format": Defines the concrete layout or value relationships for ANA Group Descriptor format. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is AGID, NNV, CHGC, ANASA, ANAS, ANA, ID, NSID.

- Purpose: Defines the concrete layout or value relationships for ANA Group Descriptor format.

- How to read: Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is AGID, NNV, CHGC, ANASA, ANAS, ANA, ID, NSID.

- Conditions and limits: Source keyword index: `shall`, `should`, `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Use AGID as the first parser checkpoint and NNV as a second, independent boundary check. This example adds no requirement.

- Source field index: AGID, NNV, CHGC, ANASA, ANAS, ANA, ID, NSID

- Source keyword index: `shall`, `should`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.13, Figure 231, printed pages 243-244, PDF pages 269-270

</details>

<details markdown="1">
<summary><strong>Figure 232: Persistent Event Log Specific Parameter Field</strong></summary>

<!-- claim:BASEFWLOG-FIG-232-CLAIM figure-table:BASEFWLOG-FIG-232 -->

Figure 232, "Persistent Event Log Specific Parameter Field": Defines the event record, event taxonomy, or logging condition represented by Persistent Event Log Specific Parameter Field. Resolve event type and record length before decoding event-specific data. Evidence index: ACT, LPOU, LPOL, NUMDU, NUMDL.

- Purpose: Defines the event record, event taxonomy, or logging condition represented by Persistent Event Log Specific Parameter Field.

- How to read: Resolve event type and record length before decoding event-specific data. Evidence index: ACT, LPOU, LPOL, NUMDU, NUMDL.

- Conditions and limits: Source keyword index: `shall`, `should`, `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Identify ACT, validate the record boundary using LPOU, and decode only the data defined for that event type. This example adds no requirement.

- Source field index: ACT, LPOU, LPOL, NUMDU, NUMDL

- Source keyword index: `shall`, `should`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.14, Figure 232, printed pages 246, PDF pages 272

</details>

<details markdown="1">
<summary><strong>Figure 233: Persistent Event Log Page</strong></summary>

<!-- claim:BASEFWLOG-FIG-233-CLAIM figure-table:BASEFWLOG-FIG-233 -->

Figure 233, "Persistent Event Log Page": Defines the returned log-page layout and selection context for Persistent Event Log Page. Start with the fixed header and scope, validate counts or lengths, then walk entries or data areas in order. Evidence index: LID, TNEV, TLL, LREV, LHL, TSTMP, POH, PWRCC.

- Purpose: Defines the returned log-page layout and selection context for Persistent Event Log Page.

- How to read: Start with the fixed header and scope, validate counts or lengths, then walk entries or data areas in order. Evidence index: LID, TNEV, TLL, LREV, LHL, TSTMP, POH, PWRCC.

- Conditions and limits: Source keyword index: `shall`, `may`, `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Read LID first, use TNEV as an independent size or identity check, and stop before any unreturned byte. This example adds no requirement.

- Source field index: LID, TNEV, TLL, LREV, LHL, TSTMP, POH, PWRCC

- Source keyword index: `shall`, `may`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.14, Figure 233, printed pages 247-249, PDF pages 273-275

</details>

<details markdown="1">
<summary><strong>Figure 234: Persistent Event Format</strong></summary>

<!-- claim:BASEFWLOG-FIG-234-CLAIM figure-table:BASEFWLOG-FIG-234 -->

Figure 234, "Persistent Event Format": Defines the event record, event taxonomy, or logging condition represented by Persistent Event Format. Resolve event type and record length before decoding event-specific data. Evidence index: ET, EHAI, PIT, CNTLID, ETSTP, PELPID, VSIL, EL.

- Purpose: Defines the event record, event taxonomy, or logging condition represented by Persistent Event Format.

- How to read: Resolve event type and record length before decoding event-specific data. Evidence index: ET, EHAI, PIT, CNTLID, ETSTP, PELPID, VSIL, EL.

- Conditions and limits: Source keyword index: `shall`, `may`, `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Identify ET, validate the record boundary using EHAI, and decode only the data defined for that event type. This example adds no requirement.

- Source field index: ET, EHAI, PIT, CNTLID, ETSTP, PELPID, VSIL, EL

- Source keyword index: `shall`, `may`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.14, Figure 234, printed pages 249-250, PDF pages 275-276

</details>

<details markdown="1">
<summary><strong>Figure 235: Persistent Event LID Specific Parameter Field</strong></summary>

<!-- claim:BASEFWLOG-FIG-235-CLAIM figure-table:BASEFWLOG-FIG-235 -->

Figure 235, "Persistent Event LID Specific Parameter Field": Defines the event record, event taxonomy, or logging condition represented by Persistent Event LID Specific Parameter Field. Resolve event type and record length before decoding event-specific data. Evidence index: ECRH, LID.

- Purpose: Defines the event record, event taxonomy, or logging condition represented by Persistent Event LID Specific Parameter Field.

- How to read: Resolve event type and record length before decoding event-specific data. Evidence index: ECRH, LID.

- Conditions and limits: Source keyword index: `shall`, `may`, `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Identify ECRH, validate the record boundary using LID, and decode only the data defined for that event type. This example adds no requirement.

- Source field index: ECRH, LID

- Source keyword index: `shall`, `may`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.14, Figure 235, printed pages 251, PDF pages 277

</details>

<details markdown="1">
<summary><strong>Figure 236: Persistent Event Log Event Types</strong></summary>

<!-- claim:BASEFWLOG-FIG-236-CLAIM figure-table:BASEFWLOG-FIG-236 -->

Figure 236, "Persistent Event Log Event Types": Defines the event record, event taxonomy, or logging condition represented by Persistent Event Log Event Types. Resolve event type and record length before decoding event-specific data. Evidence index: M1, NOTE, SMART, TCG.

- Purpose: Defines the event record, event taxonomy, or logging condition represented by Persistent Event Log Event Types.

- How to read: Resolve event type and record length before decoding event-specific data. Evidence index: M1, NOTE, SMART, TCG.

- Conditions and limits: Source keyword index: `optional`, `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Identify M1, validate the record boundary using NOTE, and decode only the data defined for that event type. This example adds no requirement.

- Source field index: M1, NOTE, SMART, TCG

- Source keyword index: `optional`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.14, Figure 236, printed pages 251, PDF pages 277

</details>

<details markdown="1">
<summary><strong>Figure 237: SMART / Health Log Snapshot Event Data Format (Event Type 01h)</strong></summary>

<!-- claim:BASEFWLOG-FIG-237-CLAIM figure-table:BASEFWLOG-FIG-237 -->

Figure 237, "SMART / Health Log Snapshot Event Data Format (Event Type 01h)": Defines the event record, event taxonomy, or logging condition represented by SMART / Health Log Snapshot Event Data Format (Event Type 01h). Resolve event type and record length before decoding event-specific data. Evidence index: ED, SMART.

- Purpose: Defines the event record, event taxonomy, or logging condition represented by SMART / Health Log Snapshot Event Data Format (Event Type 01h).

- How to read: Resolve event type and record length before decoding event-specific data. Evidence index: ED, SMART.

- Conditions and limits: The Figure is explanatory or structural; this guide does not turn its visual relationship into a new requirement.

- Informative example: Identify ED, validate the record boundary using SMART, and decode only the data defined for that event type. This example adds no requirement.

- Source field index: ED, SMART

- Source keyword index: none

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.14.2, Figure 237, printed pages 252, PDF pages 278

</details>

<details markdown="1">
<summary><strong>Figure 238: Firmware Commit Event Data Format (Event Type 02h)</strong></summary>

<!-- claim:BASEFWLOG-FIG-238-CLAIM figure-table:BASEFWLOG-FIG-238 -->

Figure 238, "Firmware Commit Event Data Format (Event Type 02h)": Defines the event record, event taxonomy, or logging condition represented by Firmware Commit Event Data Format (Event Type 02h). Resolve event type and record length before decoding event-specific data. Evidence index: OFR, NFR, FCA, FSLT, STCTFCC, SRFCC, VAFCRC.

- Purpose: Defines the event record, event taxonomy, or logging condition represented by Firmware Commit Event Data Format (Event Type 02h).

- How to read: Resolve event type and record length before decoding event-specific data. Evidence index: OFR, NFR, FCA, FSLT, STCTFCC, SRFCC, VAFCRC.

- Conditions and limits: The Figure is explanatory or structural; this guide does not turn its visual relationship into a new requirement.

- Informative example: Identify OFR, validate the record boundary using NFR, and decode only the data defined for that event type. This example adds no requirement.

- Source field index: OFR, NFR, FCA, FSLT, STCTFCC, SRFCC, VAFCRC

- Source keyword index: none

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.14.2, Figure 238, printed pages 252, PDF pages 278

</details>

<details markdown="1">
<summary><strong>Figure 239: Timestamp Change Event Format (Event Type 03h)</strong></summary>

<!-- claim:BASEFWLOG-FIG-239-CLAIM figure-table:BASEFWLOG-FIG-239 -->

Figure 239, "Timestamp Change Event Format (Event Type 03h)": Defines the event record, event taxonomy, or logging condition represented by Timestamp Change Event Format (Event Type 03h). Resolve event type and record length before decoding event-specific data. Evidence index: PTSTP, MSR.

- Purpose: Defines the event record, event taxonomy, or logging condition represented by Timestamp Change Event Format (Event Type 03h).

- How to read: Resolve event type and record length before decoding event-specific data. Evidence index: PTSTP, MSR.

- Conditions and limits: The Figure is explanatory or structural; this guide does not turn its visual relationship into a new requirement.

- Informative example: Identify PTSTP, validate the record boundary using MSR, and decode only the data defined for that event type. This example adds no requirement.

- Source field index: PTSTP, MSR

- Source keyword index: none

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.14.2, Figure 239, printed pages 253, PDF pages 279

</details>

<details markdown="1">
<summary><strong>Figure 240: Power-on or Reset Event (Event Type 04h)</strong></summary>

<!-- claim:BASEFWLOG-FIG-240-CLAIM figure-table:BASEFWLOG-FIG-240 -->

Figure 240, "Power-on or Reset Event (Event Type 04h)": Defines the event record, event taxonomy, or logging condition represented by Power-on or Reset Event (Event Type 04h). Resolve event type and record length before decoding event-specific data. Evidence index: FREV, RIL, CC.EN, EL, VSIL.

- Purpose: Defines the event record, event taxonomy, or logging condition represented by Power-on or Reset Event (Event Type 04h).

- How to read: Resolve event type and record length before decoding event-specific data. Evidence index: FREV, RIL, CC.EN, EL, VSIL.

- Conditions and limits: Source keyword index: `shall`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Identify FREV, validate the record boundary using RIL, and decode only the data defined for that event type. This example adds no requirement.

- Source field index: FREV, RIL, CC.EN, EL, VSIL

- Source keyword index: `shall`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.14.2, Figure 240, printed pages 253, PDF pages 279

</details>

<details markdown="1">
<summary><strong>Figure 241: Controller Reset Information descriptor</strong></summary>

<!-- claim:BASEFWLOG-FIG-241-CLAIM figure-table:BASEFWLOG-FIG-241 -->

Figure 241, "Controller Reset Information descriptor": Defines the concrete layout or value relationships for Controller Reset Information descriptor. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is CNTLID, FA, OIP, RDNF, CPWRC, POM, CTSTP, ID.

- Purpose: Defines the concrete layout or value relationships for Controller Reset Information descriptor.

- How to read: Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is CNTLID, FA, OIP, RDNF, CPWRC, POM, CTSTP, ID.

- Conditions and limits: Source keyword index: `may`, `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Use CNTLID as the first parser checkpoint and FA as a second, independent boundary check. This example adds no requirement.

- Source field index: CNTLID, FA, OIP, RDNF, CPWRC, POM, CTSTP, ID

- Source keyword index: `may`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.14.2, Figure 241, printed pages 253-254, PDF pages 279-280

</details>

<details markdown="1">
<summary><strong>Figure 242: NVM Subsystem Hardware Error Event Format (Event Type 05h)</strong></summary>

<!-- claim:BASEFWLOG-FIG-242-CLAIM figure-table:BASEFWLOG-FIG-242 -->

Figure 242, "NVM Subsystem Hardware Error Event Format (Event Type 05h)": Defines the status/error classification represented by NVM Subsystem Hardware Error Event Format (Event Type 05h). Resolve the category before the individual code or flag; keep reserved values uninterpreted. Evidence index: NSHEEC, AHEI, NVM Subsystem.

- Purpose: Defines the status/error classification represented by NVM Subsystem Hardware Error Event Format (Event Type 05h).

- How to read: Resolve the category before the individual code or flag; keep reserved values uninterpreted. Evidence index: NSHEEC, AHEI, NVM Subsystem.

- Conditions and limits: Source keyword index: `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: For one reported condition, identify NSHEEC first and then check AHEI instead of decoding an isolated numeric value. This example adds no requirement.

- Source field index: NSHEEC, AHEI, NVM Subsystem

- Source keyword index: `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.14.2, Figure 242, printed pages 254, PDF pages 280

</details>

<details markdown="1">
<summary><strong>Figure 243: NVM Subsystem Hardware Error Event Codes</strong></summary>

<!-- claim:BASEFWLOG-FIG-243-CLAIM figure-table:BASEFWLOG-FIG-243 -->

Figure 243, "NVM Subsystem Hardware Error Event Codes": Defines the status/error classification represented by NVM Subsystem Hardware Error Event Codes. Resolve the category before the individual code or flag; keep reserved values uninterpreted. Evidence index: EGCW, EGID, SMART, CSTS.CFS, CRTO.CRWMT, CC.CRIME, CRTO.CRIMT, CC.EN.

- Purpose: Defines the status/error classification represented by NVM Subsystem Hardware Error Event Codes.

- How to read: Resolve the category before the individual code or flag; keep reserved values uninterpreted. Evidence index: EGCW, EGID, SMART, CSTS.CFS, CRTO.CRWMT, CC.CRIME, CRTO.CRIMT, CC.EN.

- Conditions and limits: Source keyword index: `shall`, `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: For one reported condition, identify EGCW first and then check EGID instead of decoding an isolated numeric value. This example adds no requirement.

- Source field index: EGCW, EGID, SMART, CSTS.CFS, CRTO.CRWMT, CC.CRIME, CRTO.CRIMT, CC.EN

- Source keyword index: `shall`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.14.2, Figure 243, printed pages 254-256, PDF pages 280-282

</details>

<details markdown="1">
<summary><strong>Figure 244: Additional Hardware Error Information for Unexpected Power Loss Errors</strong></summary>

<!-- claim:BASEFWLOG-FIG-244-CLAIM figure-table:BASEFWLOG-FIG-244 -->

Figure 244, "Additional Hardware Error Information for Unexpected Power Loss Errors": Defines the status/error classification represented by Additional Hardware Error Information for Unexpected Power Loss Errors. Resolve the category before the individual code or flag; keep reserved values uninterpreted. Evidence index: UPL, UPLI, UPLOA, SMART, CSTS.SHST.

- Purpose: Defines the status/error classification represented by Additional Hardware Error Information for Unexpected Power Loss Errors.

- How to read: Resolve the category before the individual code or flag; keep reserved values uninterpreted. Evidence index: UPL, UPLI, UPLOA, SMART, CSTS.SHST.

- Conditions and limits: Source keyword index: `shall`, `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: For one reported condition, identify UPL first and then check UPLI instead of decoding an isolated numeric value. This example adds no requirement.

- Source field index: UPL, UPLI, UPLOA, SMART, CSTS.SHST

- Source keyword index: `shall`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.14.2, Figure 244, printed pages 256, PDF pages 282

</details>

<details markdown="1">
<summary><strong>Figure 245: Additional Hardware Error Information for correctable and uncorrectable PCIe errors</strong></summary>

<!-- claim:BASEFWLOG-FIG-245-CLAIM figure-table:BASEFWLOG-FIG-245 -->

Figure 245, "Additional Hardware Error Information for correctable and uncorrectable PCIe errors": Defines the status/error classification represented by Additional Hardware Error Information for correctable and uncorrectable PCIe errors. Resolve the category before the individual code or flag; keep reserved values uninterpreted. Evidence index: PCIEAS, PCIEAERS, PCIe AER Error Status, PCIe AER Error Mask.

- Purpose: Defines the status/error classification represented by Additional Hardware Error Information for correctable and uncorrectable PCIe errors.

- How to read: Resolve the category before the individual code or flag; keep reserved values uninterpreted. Evidence index: PCIEAS, PCIEAERS, PCIe AER Error Status, PCIe AER Error Mask.

- Conditions and limits: Source keyword index: `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: For one reported condition, identify PCIEAS first and then check PCIEAERS instead of decoding an isolated numeric value. This example adds no requirement.

- Source field index: PCIEAS, PCIEAERS, PCIe AER Error Status, PCIe AER Error Mask

- Source keyword index: `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.14.2, Figure 245, printed pages 256-257, PDF pages 282-283

</details>

<details markdown="1">
<summary><strong>Figure 246: Additional Hardware Error Information for Controller Ready Timeout</strong></summary>

<!-- claim:BASEFWLOG-FIG-246-CLAIM figure-table:BASEFWLOG-FIG-246 -->

Figure 246, "Additional Hardware Error Information for Controller Ready Timeout": Defines the status/error classification represented by Additional Hardware Error Information for Controller Ready Timeout. Resolve the category before the individual code or flag; keep reserved values uninterpreted. Evidence index: CST, CNR, ACMNR, NNR, CRIME, CRTO.CRWMT, CC.CRIME, CRTO.CRIMT.

- Purpose: Defines the status/error classification represented by Additional Hardware Error Information for Controller Ready Timeout.

- How to read: Resolve the category before the individual code or flag; keep reserved values uninterpreted. Evidence index: CST, CNR, ACMNR, NNR, CRIME, CRTO.CRWMT, CC.CRIME, CRTO.CRIMT.

- Conditions and limits: Source keyword index: `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: For one reported condition, identify CST first and then check CNR instead of decoding an isolated numeric value. This example adds no requirement.

- Source field index: CST, CNR, ACMNR, NNR, CRIME, CRTO.CRWMT, CC.CRIME, CRTO.CRIMT

- Source keyword index: `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.14.2, Figure 246, printed pages 258, PDF pages 284

</details>

<details markdown="1">
<summary><strong>Figure 247: Change Namespace Event Data Format (Event Type 06h)</strong></summary>

<!-- claim:BASEFWLOG-FIG-247-CLAIM figure-table:BASEFWLOG-FIG-247 -->

Figure 247, "Change Namespace Event Data Format (Event Type 06h)": Defines the event record, event taxonomy, or logging condition represented by Change Namespace Event Data Format (Event Type 06h). Resolve event type and record length before decoding event-specific data. Evidence index: NMCDW10, NSZE, NCAP, FLBAS, DPS, NMIC, ANAGRPID, NVMSETID.

- Purpose: Defines the event record, event taxonomy, or logging condition represented by Change Namespace Event Data Format (Event Type 06h).

- How to read: Resolve event type and record length before decoding event-specific data. Evidence index: NMCDW10, NSZE, NCAP, FLBAS, DPS, NMIC, ANAGRPID, NVMSETID.

- Conditions and limits: Source keyword index: `shall`, `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Identify NMCDW10, validate the record boundary using NSZE, and decode only the data defined for that event type. This example adds no requirement.

- Source field index: NMCDW10, NSZE, NCAP, FLBAS, DPS, NMIC, ANAGRPID, NVMSETID

- Source keyword index: `shall`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.14.2, Figure 247, printed pages 258-259, PDF pages 284-285

</details>

<details markdown="1">
<summary><strong>Figure 248: Format NVM Start Event Data Format (Event Type 07h)</strong></summary>

<!-- claim:BASEFWLOG-FIG-248-CLAIM figure-table:BASEFWLOG-FIG-248 -->

Figure 248, "Format NVM Start Event Data Format (Event Type 07h)": Defines the event record, event taxonomy, or logging condition represented by Format NVM Start Event Data Format (Event Type 07h). Resolve event type and record length before decoding event-specific data. Evidence index: NSID, FNA, FMCDW10, CDW10.

- Purpose: Defines the event record, event taxonomy, or logging condition represented by Format NVM Start Event Data Format (Event Type 07h).

- How to read: Resolve event type and record length before decoding event-specific data. Evidence index: NSID, FNA, FMCDW10, CDW10.

- Conditions and limits: Source keyword index: `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Identify NSID, validate the record boundary using FNA, and decode only the data defined for that event type. This example adds no requirement.

- Source field index: NSID, FNA, FMCDW10, CDW10

- Source keyword index: `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.14.2, Figure 248, printed pages 260, PDF pages 286

</details>

<details markdown="1">
<summary><strong>Figure 249: Format NVM Completion Event Data Format (Event Type 08h)</strong></summary>

<!-- claim:BASEFWLOG-FIG-249-CLAIM figure-table:BASEFWLOG-FIG-249 -->

Figure 249, "Format NVM Completion Event Data Format (Event Type 08h)": Defines the event record, event taxonomy, or logging condition represented by Format NVM Completion Event Data Format (Event Type 08h). Resolve event type and record length before decoding event-specific data. Evidence index: NSID, SFPI, FNVMS, INCPLTF, FNVME, CINFO, INFO, STATUS.

- Purpose: Defines the event record, event taxonomy, or logging condition represented by Format NVM Completion Event Data Format (Event Type 08h).

- How to read: Resolve event type and record length before decoding event-specific data. Evidence index: NSID, SFPI, FNVMS, INCPLTF, FNVME, CINFO, INFO, STATUS.

- Conditions and limits: Source keyword index: `shall`, `may`, `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Identify NSID, validate the record boundary using SFPI, and decode only the data defined for that event type. This example adds no requirement.

- Source field index: NSID, SFPI, FNVMS, INCPLTF, FNVME, CINFO, INFO, STATUS

- Source keyword index: `shall`, `may`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.14.2, Figure 249, printed pages 260-261, PDF pages 286-287

</details>

<details markdown="1">
<summary><strong>Figure 250: Sanitize Start Event Data Format (Event Type 09h)</strong></summary>

<!-- claim:BASEFWLOG-FIG-250-CLAIM figure-table:BASEFWLOG-FIG-250 -->

Figure 250, "Sanitize Start Event Data Format (Event Type 09h)": Defines the event record, event taxonomy, or logging condition represented by Sanitize Start Event Data Format (Event Type 09h). Resolve event type and record length before decoding event-specific data. Evidence index: SCDW10, SCDW11, NSID, SANICAP, CDW10, CDW11.

- Purpose: Defines the event record, event taxonomy, or logging condition represented by Sanitize Start Event Data Format (Event Type 09h).

- How to read: Resolve event type and record length before decoding event-specific data. Evidence index: SCDW10, SCDW11, NSID, SANICAP, CDW10, CDW11.

- Conditions and limits: Source keyword index: `shall`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Identify SCDW10, validate the record boundary using SCDW11, and decode only the data defined for that event type. This example adds no requirement.

- Source field index: SCDW10, SCDW11, NSID, SANICAP, CDW10, CDW11

- Source keyword index: `shall`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.14.2, Figure 250, printed pages 261, PDF pages 287

</details>

<details markdown="1">
<summary><strong>Figure 251: Sanitize Completion Event Data Format (Event Type 0Ah)</strong></summary>

<!-- claim:BASEFWLOG-FIG-251-CLAIM figure-table:BASEFWLOG-FIG-251 -->

Figure 251, "Sanitize Completion Event Data Format (Event Type 0Ah)": Defines the event record, event taxonomy, or logging condition represented by Sanitize Completion Event Data Format (Event Type 0Ah). Resolve event type and record length before decoding event-specific data. Evidence index: SPROG, SSTAT, CINFO, NSID.

- Purpose: Defines the event record, event taxonomy, or logging condition represented by Sanitize Completion Event Data Format (Event Type 0Ah).

- How to read: Resolve event type and record length before decoding event-specific data. Evidence index: SPROG, SSTAT, CINFO, NSID.

- Conditions and limits: Source keyword index: `shall`, `may`, `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Identify SPROG, validate the record boundary using SSTAT, and decode only the data defined for that event type. This example adds no requirement.

- Source field index: SPROG, SSTAT, CINFO, NSID

- Source keyword index: `shall`, `may`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.14.2, Figure 251, printed pages 261-262, PDF pages 287-288

</details>

<details markdown="1">
<summary><strong>Figure 252: Feature Persistent Event Logging Requirements</strong></summary>

<!-- claim:BASEFWLOG-FIG-252-CLAIM figure-table:BASEFWLOG-FIG-252 -->

Figure 252, "Feature Persistent Event Logging Requirements": Defines the event record, event taxonomy, or logging condition represented by Feature Persistent Event Logging Requirements. Resolve event type and record length before decoding event-specific data. Evidence index: PE, NR.

- Purpose: Defines the event record, event taxonomy, or logging condition represented by Feature Persistent Event Logging Requirements.

- How to read: Resolve event type and record length before decoding event-specific data. Evidence index: PE, NR.

- Conditions and limits: Source keyword index: `optional`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Identify PE, validate the record boundary using NR, and decode only the data defined for that event type. This example adds no requirement.

- Source field index: PE, NR

- Source keyword index: `optional`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.14.2, Figure 252, printed pages 262-263, PDF pages 288-289

</details>

<details markdown="1">
<summary><strong>Figure 253: Set Feature Event Data Format</strong></summary>

<!-- claim:BASEFWLOG-FIG-253-CLAIM figure-table:BASEFWLOG-FIG-253 -->

Figure 253, "Set Feature Event Data Format": Defines the event record, event taxonomy, or logging condition represented by Set Feature Event Data Format. Resolve event type and record length before decoding event-specific data. Evidence index: SFEL, MBC, LCCDW0, DWC, CDWS, MBUF, CCDW0.

- Purpose: Defines the event record, event taxonomy, or logging condition represented by Set Feature Event Data Format.

- How to read: Resolve event type and record length before decoding event-specific data. Evidence index: SFEL, MBC, LCCDW0, DWC, CDWS, MBUF, CCDW0.

- Conditions and limits: Source keyword index: `shall`, `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Identify SFEL, validate the record boundary using MBC, and decode only the data defined for that event type. This example adds no requirement.

- Source field index: SFEL, MBC, LCCDW0, DWC, CDWS, MBUF, CCDW0

- Source keyword index: `shall`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.14.2, Figure 253, printed pages 264, PDF pages 290

</details>

<details markdown="1">
<summary><strong>Figure 254: Telemetry Log Created Event Data Format (Event Type 0Ch)</strong></summary>

<!-- claim:BASEFWLOG-FIG-254-CLAIM figure-table:BASEFWLOG-FIG-254 -->

Figure 254, "Telemetry Log Created Event Data Format (Event Type 0Ch)": Defines the event record, event taxonomy, or logging condition represented by Telemetry Log Created Event Data Format (Event Type 0Ch). Resolve event type and record length before decoding event-specific data. Evidence index: TIL.

- Purpose: Defines the event record, event taxonomy, or logging condition represented by Telemetry Log Created Event Data Format (Event Type 0Ch).

- How to read: Resolve event type and record length before decoding event-specific data. Evidence index: TIL.

- Conditions and limits: The Figure is explanatory or structural; this guide does not turn its visual relationship into a new requirement.

- Informative example: Identify TIL, validate the record boundary using the cited condition, and decode only the data defined for that event type. This example adds no requirement.

- Source field index: TIL

- Source keyword index: none

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.14.2, Figure 254, printed pages 264, PDF pages 290

</details>

<details markdown="1">
<summary><strong>Figure 255: Thermal Excursion Event Data Format (Event Type 0Dh)</strong></summary>

<!-- claim:BASEFWLOG-FIG-255-CLAIM figure-table:BASEFWLOG-FIG-255 -->

Figure 255, "Thermal Excursion Event Data Format (Event Type 0Dh)": Defines the event record, event taxonomy, or logging condition represented by Thermal Excursion Event Data Format (Event Type 0Dh). Resolve event type and record length before decoding event-specific data. Evidence index: OTMP, THRESH, WCTEMP, CCTEMP, TMT1, TMT2.

- Purpose: Defines the event record, event taxonomy, or logging condition represented by Thermal Excursion Event Data Format (Event Type 0Dh).

- How to read: Resolve event type and record length before decoding event-specific data. Evidence index: OTMP, THRESH, WCTEMP, CCTEMP, TMT1, TMT2.

- Conditions and limits: Source keyword index: `may`, `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Identify OTMP, validate the record boundary using THRESH, and decode only the data defined for that event type. This example adds no requirement.

- Source field index: OTMP, THRESH, WCTEMP, CCTEMP, TMT1, TMT2

- Source keyword index: `may`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.14.2, Figure 255, printed pages 265-266, PDF pages 291-292

</details>

<details markdown="1">
<summary><strong>Figure 256: CDP Change Event Data Format (Event Type 0Fh)</strong></summary>

<!-- claim:BASEFWLOG-FIG-256-CLAIM figure-table:BASEFWLOG-FIG-256 -->

Figure 256, "CDP Change Event Data Format (Event Type 0Fh)": Defines the event record, event taxonomy, or logging condition represented by CDP Change Event Data Format (Event Type 0Fh). Resolve event type and record length before decoding event-specific data. Evidence index: PS, CDPRFS, CDPCE, PERID, PED, CDP, EL.

- Purpose: Defines the event record, event taxonomy, or logging condition represented by CDP Change Event Data Format (Event Type 0Fh).

- How to read: Resolve event type and record length before decoding event-specific data. Evidence index: PS, CDPRFS, CDPCE, PERID, PED, CDP, EL.

- Conditions and limits: Source keyword index: `shall`, `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Identify PS, validate the record boundary using CDPRFS, and decode only the data defined for that event type. This example adds no requirement.

- Source field index: PS, CDPRFS, CDPCE, PERID, PED, CDP, EL

- Source keyword index: `shall`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.14.2, Figure 256, printed pages 267, PDF pages 293

</details>

<details markdown="1">
<summary><strong>Figure 258: Vendor Specific Event Format (Event Type DEh)</strong></summary>

<!-- claim:BASEFWLOG-FIG-258-CLAIM figure-table:BASEFWLOG-FIG-258 -->

Figure 258, "Vendor Specific Event Format (Event Type DEh)": Defines the event record, event taxonomy, or logging condition represented by Vendor Specific Event Format (Event Type DEh). Resolve event type and record length before decoding event-specific data. Evidence index: EL, VSIL.

- Purpose: Defines the event record, event taxonomy, or logging condition represented by Vendor Specific Event Format (Event Type DEh).

- How to read: Resolve event type and record length before decoding event-specific data. Evidence index: EL, VSIL.

- Conditions and limits: The Figure is explanatory or structural; this guide does not turn its visual relationship into a new requirement.

- Informative example: Identify EL, validate the record boundary using VSIL, and decode only the data defined for that event type. This example adds no requirement.

- Source field index: EL, VSIL

- Source keyword index: none

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.14.2, Figure 258, printed pages 269, PDF pages 295

</details>

<details markdown="1">
<summary><strong>Figure 259: Vendor Specific Event Descriptor Format</strong></summary>

<!-- claim:BASEFWLOG-FIG-259-CLAIM figure-table:BASEFWLOG-FIG-259 -->

Figure 259, "Vendor Specific Event Descriptor Format": Defines the event record, event taxonomy, or logging condition represented by Vendor Specific Event Descriptor Format. Resolve event type and record length before decoding event-specific data. Evidence index: VSEC, VSEDT, UIDX, VSEDL, VSED, UUID.

- Purpose: Defines the event record, event taxonomy, or logging condition represented by Vendor Specific Event Descriptor Format.

- How to read: Resolve event type and record length before decoding event-specific data. Evidence index: VSEC, VSEDT, UIDX, VSEDL, VSED, UUID.

- Conditions and limits: Source keyword index: `should`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Identify VSEC, validate the record boundary using VSEDT, and decode only the data defined for that event type. This example adds no requirement.

- Source field index: VSEC, VSEDT, UIDX, VSEDL, VSED, UUID

- Source keyword index: `should`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.14.2, Figure 259, printed pages 269, PDF pages 295

</details>

<details markdown="1">
<summary><strong>Figure 260: Vendor Specific Event Data Type Codes</strong></summary>

<!-- claim:BASEFWLOG-FIG-260-CLAIM figure-table:BASEFWLOG-FIG-260 -->

Figure 260, "Vendor Specific Event Data Type Codes": Defines the event record, event taxonomy, or logging condition represented by Vendor Specific Event Data Type Codes. Resolve event type and record length before decoding event-specific data. Evidence index: ASCII.

- Purpose: Defines the event record, event taxonomy, or logging condition represented by Vendor Specific Event Data Type Codes.

- How to read: Resolve event type and record length before decoding event-specific data. Evidence index: ASCII.

- Conditions and limits: Source keyword index: `shall`, `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Identify ASCII, validate the record boundary using the cited condition, and decode only the data defined for that event type. This example adds no requirement.

- Source field index: ASCII

- Source keyword index: `shall`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.14.2, Figure 260, printed pages 269-270, PDF pages 295-296

</details>

<details markdown="1">
<summary><strong>Figure 261: Endurance Group Event Aggregate Log Page</strong></summary>

<!-- claim:BASEFWLOG-FIG-261-CLAIM figure-table:BASEFWLOG-FIG-261 -->

Figure 261, "Endurance Group Event Aggregate Log Page": Defines the returned log-page layout and selection context for Endurance Group Event Aggregate Log Page. Start with the fixed header and scope, validate counts or lengths, then walk entries or data areas in order. Evidence index: NUMENT, Endurance Group.

- Purpose: Defines the returned log-page layout and selection context for Endurance Group Event Aggregate Log Page.

- How to read: Start with the fixed header and scope, validate counts or lengths, then walk entries or data areas in order. Evidence index: NUMENT, Endurance Group.

- Conditions and limits: The Figure is explanatory or structural; this guide does not turn its visual relationship into a new requirement.

- Informative example: Read NUMENT first, use Endurance Group as an independent size or identity check, and stop before any unreturned byte. This example adds no requirement.

- Source field index: NUMENT, Endurance Group

- Source keyword index: none

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.15, Figure 261, printed pages 270, PDF pages 296

</details>

<details markdown="1">
<summary><strong>Figure 262: Domain Identifier – Log Specific Identifier</strong></summary>

<!-- claim:BASEFWLOG-FIG-262-CLAIM figure-table:BASEFWLOG-FIG-262 -->

Figure 262, "Domain Identifier – Log Specific Identifier": Defines the identifier composition or namespace of values shown by Domain Identifier – Log Specific Identifier. Keep the value width, issuing authority, uniqueness scope, and reserved values separate. Evidence index: DID, Domain.

- Purpose: Defines the identifier composition or namespace of values shown by Domain Identifier – Log Specific Identifier.

- How to read: Keep the value width, issuing authority, uniqueness scope, and reserved values separate. Evidence index: DID, Domain.

- Conditions and limits: Source keyword index: `shall`, `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Parse DID at its defined width, then validate the scope associated with Domain before using it as an identity key. This example adds no requirement.

- Source field index: DID, Domain

- Source keyword index: `shall`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.16, Figure 262, printed pages 271, PDF pages 297

</details>

<details markdown="1">
<summary><strong>Figure 263: Media Unit Status Log Page</strong></summary>

<!-- claim:BASEFWLOG-FIG-263-CLAIM figure-table:BASEFWLOG-FIG-263 -->

Figure 263, "Media Unit Status Log Page": Defines the returned log-page layout and selection context for Media Unit Status Log Page. Start with the fixed header and scope, validate counts or lengths, then walk entries or data areas in order. Evidence index: NMU, CCHANS, SELC, NOTE, ENDGID, NVMSETID, MUCS.

- Purpose: Defines the returned log-page layout and selection context for Media Unit Status Log Page.

- How to read: Start with the fixed header and scope, validate counts or lengths, then walk entries or data areas in order. Evidence index: NMU, CCHANS, SELC, NOTE, ENDGID, NVMSETID, MUCS.

- Conditions and limits: Source keyword index: `shall`, `may`, `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Read NMU first, use CCHANS as an independent size or identity check, and stop before any unreturned byte. This example adds no requirement.

- Source field index: NMU, CCHANS, SELC, NOTE, ENDGID, NVMSETID, MUCS

- Source keyword index: `shall`, `may`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.16, Figure 263, printed pages 271, PDF pages 297

</details>

<details markdown="1">
<summary><strong>Figure 264: Media Unit Status Descriptor</strong></summary>

<!-- claim:BASEFWLOG-FIG-264-CLAIM figure-table:BASEFWLOG-FIG-264 -->

Figure 264, "Media Unit Status Descriptor": Defines the concrete layout or value relationships for Media Unit Status Descriptor. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is MUID, DID, ENDGID, NVMSETID, CAF, AVSP, PUSED, CIO.

- Purpose: Defines the concrete layout or value relationships for Media Unit Status Descriptor.

- How to read: Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is MUID, DID, ENDGID, NVMSETID, CAF, AVSP, PUSED, CIO.

- Conditions and limits: Source keyword index: `shall`, `may`, `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Use MUID as the first parser checkpoint and DID as a second, independent boundary check. This example adds no requirement.

- Source field index: MUID, DID, ENDGID, NVMSETID, CAF, AVSP, PUSED, CIO

- Source keyword index: `shall`, `may`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.16, Figure 264, printed pages 272, PDF pages 298

</details>

<details markdown="1">
<summary><strong>Figure 265: Supported Capacity Configuration List Log Page</strong></summary>

<!-- claim:BASEFWLOG-FIG-265-CLAIM figure-table:BASEFWLOG-FIG-265 -->

Figure 265, "Supported Capacity Configuration List Log Page": Defines the returned log-page layout and selection context for Supported Capacity Configuration List Log Page. Start with the fixed header and scope, validate counts or lengths, then walk entries or data areas in order. Evidence index: SCCN, NOTE.

- Purpose: Defines the returned log-page layout and selection context for Supported Capacity Configuration List Log Page.

- How to read: Start with the fixed header and scope, validate counts or lengths, then walk entries or data areas in order. Evidence index: SCCN, NOTE.

- Conditions and limits: Source keyword index: `shall`, `may`, `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Read SCCN first, use NOTE as an independent size or identity check, and stop before any unreturned byte. This example adds no requirement.

- Source field index: SCCN, NOTE

- Source keyword index: `shall`, `may`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.17, Figure 265, printed pages 273, PDF pages 299

</details>

<details markdown="1">
<summary><strong>Figure 266: Capacity Configuration Descriptor</strong></summary>

<!-- claim:BASEFWLOG-FIG-266-CLAIM figure-table:BASEFWLOG-FIG-266 -->

Figure 266, "Capacity Configuration Descriptor": Defines the concrete layout or value relationships for Capacity Configuration Descriptor. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is CCID, DID, EGCN, NOTE.

- Purpose: Defines the concrete layout or value relationships for Capacity Configuration Descriptor.

- How to read: Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is CCID, DID, EGCN, NOTE.

- Conditions and limits: Source keyword index: `shall`, `may`, `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Use CCID as the first parser checkpoint and DID as a second, independent boundary check. This example adds no requirement.

- Source field index: CCID, DID, EGCN, NOTE

- Source keyword index: `shall`, `may`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.17, Figure 266, printed pages 273-274, PDF pages 299-300

</details>

<details markdown="1">
<summary><strong>Figure 267: Endurance Group Configuration Descriptor</strong></summary>

<!-- claim:BASEFWLOG-FIG-267-CLAIM figure-table:BASEFWLOG-FIG-267 -->

Figure 267, "Endurance Group Configuration Descriptor": Defines the concrete layout or value relationships for Endurance Group Configuration Descriptor. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is ENDGID, CADJF, TEGCAP, SEGCAP, EE, EGSETS, EGCHANS, NOTE.

- Purpose: Defines the concrete layout or value relationships for Endurance Group Configuration Descriptor.

- How to read: Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is ENDGID, CADJF, TEGCAP, SEGCAP, EE, EGSETS, EGCHANS, NOTE.

- Conditions and limits: Source keyword index: `shall`, `may`, `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Use ENDGID as the first parser checkpoint and CADJF as a second, independent boundary check. This example adds no requirement.

- Source field index: ENDGID, CADJF, TEGCAP, SEGCAP, EE, EGSETS, EGCHANS, NOTE

- Source keyword index: `shall`, `may`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.17, Figure 267, printed pages 274-275, PDF pages 300-301

</details>

<details markdown="1">
<summary><strong>Figure 268: Channel Configuration Descriptor</strong></summary>

<!-- claim:BASEFWLOG-FIG-268-CLAIM figure-table:BASEFWLOG-FIG-268 -->

Figure 268, "Channel Configuration Descriptor": Defines the concrete layout or value relationships for Channel Configuration Descriptor. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is CHID, CHMUS, NOTE.

- Purpose: Defines the concrete layout or value relationships for Channel Configuration Descriptor.

- How to read: Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is CHID, CHMUS, NOTE.

- Conditions and limits: Source keyword index: `may`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Use CHID as the first parser checkpoint and CHMUS as a second, independent boundary check. This example adds no requirement.

- Source field index: CHID, CHMUS, NOTE

- Source keyword index: `may`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.17, Figure 268, printed pages 275, PDF pages 301

</details>

<details markdown="1">
<summary><strong>Figure 269: Media Unit Configuration Descriptor</strong></summary>

<!-- claim:BASEFWLOG-FIG-269-CLAIM figure-table:BASEFWLOG-FIG-269 -->

Figure 269, "Media Unit Configuration Descriptor": Defines the concrete layout or value relationships for Media Unit Configuration Descriptor. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is MUID, MUDL.

- Purpose: Defines the concrete layout or value relationships for Media Unit Configuration Descriptor.

- How to read: Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is MUID, MUDL.

- Conditions and limits: Source keyword index: `shall`, `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Use MUID as the first parser checkpoint and MUDL as a second, independent boundary check. This example adds no requirement.

- Source field index: MUID, MUDL

- Source keyword index: `shall`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.17, Figure 269, printed pages 276, PDF pages 302

</details>

<details markdown="1">
<summary><strong>Figure 270: Feature Identifiers Effects Log Page</strong></summary>

<!-- claim:BASEFWLOG-FIG-270-CLAIM figure-table:BASEFWLOG-FIG-270 -->

Figure 270, "Feature Identifiers Effects Log Page": Defines the returned log-page layout and selection context for Feature Identifiers Effects Log Page. Start with the fixed header and scope, validate counts or lengths, then walk entries or data areas in order. Evidence index: FIS0, FIS1, FIS254, FIS255, FID.

- Purpose: Defines the returned log-page layout and selection context for Feature Identifiers Effects Log Page.

- How to read: Start with the fixed header and scope, validate counts or lengths, then walk entries or data areas in order. Evidence index: FIS0, FIS1, FIS254, FIS255, FID.

- Conditions and limits: Source keyword index: `optional`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Read FIS0 first, use FIS1 as an independent size or identity check, and stop before any unreturned byte. This example adds no requirement.

- Source field index: FIS0, FIS1, FIS254, FIS255, FID

- Source keyword index: `optional`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.18, Figure 270, printed pages 276, PDF pages 302

</details>

<details markdown="1">
<summary><strong>Figure 271: FID Supported and Effects Data Structure</strong></summary>

<!-- claim:BASEFWLOG-FIG-271-CLAIM figure-table:BASEFWLOG-FIG-271 -->

Figure 271, "FID Supported and Effects Data Structure": Defines the concrete layout or value relationships for FID Supported and Effects Data Structure. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is FSP, RUHS, CDQSCP, NSSCPE, DSCPE, EGSCPE, NSETSCPE, CSCPE.

- Purpose: Defines the concrete layout or value relationships for FID Supported and Effects Data Structure.

- How to read: Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is FSP, RUHS, CDQSCP, NSSCPE, DSCPE, EGSCPE, NSETSCPE, CSCPE.

- Conditions and limits: Source keyword index: `shall`, `may`, `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Use FSP as the first parser checkpoint and RUHS as a second, independent boundary check. This example adds no requirement.

- Source field index: FSP, RUHS, CDQSCP, NSSCPE, DSCPE, EGSCPE, NSETSCPE, CSCPE

- Source keyword index: `shall`, `may`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.18, Figure 271, printed pages 277-278, PDF pages 303-304

</details>

<details markdown="1">
<summary><strong>Figure 272: NVMe-MI Commands Supported and Effects Log Page</strong></summary>

<!-- claim:BASEFWLOG-FIG-272-CLAIM figure-table:BASEFWLOG-FIG-272 -->

Figure 272, "NVMe-MI Commands Supported and Effects Log Page": Defines the returned log-page layout and selection context for NVMe-MI Commands Supported and Effects Log Page. Start with the fixed header and scope, validate counts or lengths, then walk entries or data areas in order. Evidence index: MICS0, MICS1, MICS254, MICS255, MI, Command.

- Purpose: Defines the returned log-page layout and selection context for NVMe-MI Commands Supported and Effects Log Page.

- How to read: Start with the fixed header and scope, validate counts or lengths, then walk entries or data areas in order. Evidence index: MICS0, MICS1, MICS254, MICS255, MI, Command.

- Conditions and limits: Source keyword index: `optional`, `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Read MICS0 first, use MICS1 as an independent size or identity check, and stop before any unreturned byte. This example adds no requirement.

- Source field index: MICS0, MICS1, MICS254, MICS255, MI, Command

- Source keyword index: `optional`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.19, Figure 272, printed pages 278, PDF pages 304

</details>

<details markdown="1">
<summary><strong>Figure 273: NVMe-MI Commands Supported and Effects Data Structure</strong></summary>

<!-- claim:BASEFWLOG-FIG-273-CLAIM figure-table:BASEFWLOG-FIG-273 -->

Figure 273, "NVMe-MI Commands Supported and Effects Data Structure": Defines the concrete layout or value relationships for NVMe-MI Commands Supported and Effects Data Structure. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is CSP, NSSCPE, DSCPE, EGSCPE, NSETSCPE, CSCPE, NSCPE, CCC.

- Purpose: Defines the concrete layout or value relationships for NVMe-MI Commands Supported and Effects Data Structure.

- How to read: Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is CSP, NSSCPE, DSCPE, EGSCPE, NSETSCPE, CSCPE, NSCPE, CCC.

- Conditions and limits: Source keyword index: `shall`, `may`, `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Use CSP as the first parser checkpoint and NSSCPE as a second, independent boundary check. This example adds no requirement.

- Source field index: CSP, NSSCPE, DSCPE, EGSCPE, NSETSCPE, CSCPE, NSCPE, CCC

- Source keyword index: `shall`, `may`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.19, Figure 273, printed pages 279, PDF pages 305

</details>

<details markdown="1">
<summary><strong>Figure 274: Command and Feature Lockdown Log Specific Parameter Field</strong></summary>

<!-- claim:BASEFWLOG-FIG-274-CLAIM figure-table:BASEFWLOG-FIG-274 -->

Figure 274, "Command and Feature Lockdown Log Specific Parameter Field": Defines the concrete layout or value relationships for Command and Feature Lockdown Log Specific Parameter Field. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is ELPF, CNTTS, SCP, Command.

- Purpose: Defines the concrete layout or value relationships for Command and Feature Lockdown Log Specific Parameter Field.

- How to read: Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is ELPF, CNTTS, SCP, Command.

- Conditions and limits: Source keyword index: `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Use ELPF as the first parser checkpoint and CNTTS as a second, independent boundary check. This example adds no requirement.

- Source field index: ELPF, CNTTS, SCP, Command

- Source keyword index: `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.20, Figure 274, printed pages 280, PDF pages 306

</details>

<details markdown="1">
<summary><strong>Figure 275: Controller Identifier - Log Specific Identifier</strong></summary>

<!-- claim:BASEFWLOG-FIG-275-CLAIM figure-table:BASEFWLOG-FIG-275 -->

Figure 275, "Controller Identifier - Log Specific Identifier": Defines the identifier composition or namespace of values shown by Controller Identifier - Log Specific Identifier. Keep the value width, issuing authority, uniqueness scope, and reserved values separate. Evidence index: CNTLID, ELPF, UUID, Controller, Controller ID.

- Purpose: Defines the identifier composition or namespace of values shown by Controller Identifier - Log Specific Identifier.

- How to read: Keep the value width, issuing authority, uniqueness scope, and reserved values separate. Evidence index: CNTLID, ELPF, UUID, Controller, Controller ID.

- Conditions and limits: Source keyword index: `shall`, `should`, `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Parse CNTLID at its defined width, then validate the scope associated with ELPF before using it as an identity key. This example adds no requirement.

- Source field index: CNTLID, ELPF, UUID, Controller, Controller ID

- Source keyword index: `shall`, `should`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.20, Figure 275, printed pages 280, PDF pages 306

</details>

<details markdown="1">
<summary><strong>Figure 276: Command and Feature Lockdown Log Page</strong></summary>

<!-- claim:BASEFWLOG-FIG-276-CLAIM figure-table:BASEFWLOG-FIG-276 -->

Figure 276, "Command and Feature Lockdown Log Page": Defines the returned log-page layout and selection context for Command and Feature Lockdown Log Page. Start with the fixed header and scope, validate counts or lengths, then walk entries or data areas in order. Evidence index: CFILA, CS, SS, LNGTH, CFIL, CFI, Command.

- Purpose: Defines the returned log-page layout and selection context for Command and Feature Lockdown Log Page.

- How to read: Start with the fixed header and scope, validate counts or lengths, then walk entries or data areas in order. Evidence index: CFILA, CS, SS, LNGTH, CFIL, CFI, Command.

- Conditions and limits: Source keyword index: `shall`, `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Read CFILA first, use CS as an independent size or identity check, and stop before any unreturned byte. This example adds no requirement.

- Source field index: CFILA, CS, SS, LNGTH, CFIL, CFI, Command

- Source keyword index: `shall`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.20, Figure 276, printed pages 281, PDF pages 307

</details>

<details markdown="1">
<summary><strong>Figure 277: Command and Feature Lockdown Log Page – Enhanced</strong></summary>

<!-- claim:BASEFWLOG-FIG-277-CLAIM figure-table:BASEFWLOG-FIG-277 -->

Figure 277, "Command and Feature Lockdown Log Page – Enhanced": Defines the returned log-page layout and selection context for Command and Feature Lockdown Log Page – Enhanced. Start with the fixed header and scope, validate counts or lengths, then walk entries or data areas in order. Evidence index: VER, CFIA, CS, SS, CNTLID, SZE, NCFID, CFIDS.

- Purpose: Defines the returned log-page layout and selection context for Command and Feature Lockdown Log Page – Enhanced.

- How to read: Start with the fixed header and scope, validate counts or lengths, then walk entries or data areas in order. Evidence index: VER, CFIA, CS, SS, CNTLID, SZE, NCFID, CFIDS.

- Conditions and limits: Source keyword index: `shall`, `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Read VER first, use CFIA as an independent size or identity check, and stop before any unreturned byte. This example adds no requirement.

- Source field index: VER, CFIA, CS, SS, CNTLID, SZE, NCFID, CFIDS

- Source keyword index: `shall`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.20, Figure 277, printed pages 282-283, PDF pages 308-309

</details>

<details markdown="1">
<summary><strong>Figure 278: Command and Feature Identifier Descriptor</strong></summary>

<!-- claim:BASEFWLOG-FIG-278-CLAIM figure-table:BASEFWLOG-FIG-278 -->

Figure 278, "Command and Feature Identifier Descriptor": Defines the concrete layout or value relationships for Command and Feature Identifier Descriptor. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is CFI, CFIA, ACNTL, CS, CNTLID, Command.

- Purpose: Defines the concrete layout or value relationships for Command and Feature Identifier Descriptor.

- How to read: Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is CFI, CFIA, ACNTL, CS, CNTLID, Command.

- Conditions and limits: Source keyword index: `shall`, `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Use CFI as the first parser checkpoint and CFIA as a second, independent boundary check. This example adds no requirement.

- Source field index: CFI, CFIA, ACNTL, CS, CNTLID, Command

- Source keyword index: `shall`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.20, Figure 278, printed pages 283, PDF pages 309

</details>

<details markdown="1">
<summary><strong>Figure 279: Boot Partition Log Specific Parameter Field</strong></summary>

<!-- claim:BASEFWLOG-FIG-279-CLAIM figure-table:BASEFWLOG-FIG-279 -->

Figure 279, "Boot Partition Log Specific Parameter Field": Defines the concrete layout or value relationships for Boot Partition Log Specific Parameter Field. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is BPID.

- Purpose: Defines the concrete layout or value relationships for Boot Partition Log Specific Parameter Field.

- How to read: Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is BPID.

- Conditions and limits: Source keyword index: `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Use BPID as the first parser checkpoint and the cited condition as a second, independent boundary check. This example adds no requirement.

- Source field index: BPID

- Source keyword index: `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.21, Figure 279, printed pages 283, PDF pages 309

</details>

<details markdown="1">
<summary><strong>Figure 280: Boot Partition Log Page</strong></summary>

<!-- claim:BASEFWLOG-FIG-280-CLAIM figure-table:BASEFWLOG-FIG-280 -->

Figure 280, "Boot Partition Log Page": Defines the returned log-page layout and selection context for Boot Partition Log Page. Start with the fixed header and scope, validate counts or lengths, then walk entries or data areas in order. Evidence index: LID, BPINFO, ABPID, BPSZ, BPD, ID.

- Purpose: Defines the returned log-page layout and selection context for Boot Partition Log Page.

- How to read: Start with the fixed header and scope, validate counts or lengths, then walk entries or data areas in order. Evidence index: LID, BPINFO, ABPID, BPSZ, BPD, ID.

- Conditions and limits: Source keyword index: `shall`, `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Read LID first, use BPINFO as an independent size or identity check, and stop before any unreturned byte. This example adds no requirement.

- Source field index: LID, BPINFO, ABPID, BPSZ, BPD, ID

- Source keyword index: `shall`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.21, Figure 280, printed pages 284, PDF pages 310

</details>

<details markdown="1">
<summary><strong>Figure 281: Rotational Media Information Log Page</strong></summary>

<!-- claim:BASEFWLOG-FIG-281-CLAIM figure-table:BASEFWLOG-FIG-281 -->

Figure 281, "Rotational Media Information Log Page": Defines the returned log-page layout and selection context for Rotational Media Information Log Page. Start with the fixed header and scope, validate counts or lengths, then walk entries or data areas in order. Evidence index: ENDGID, NUMA, NRS, SPINC, FSPINC, LDC, FLDC.

- Purpose: Defines the returned log-page layout and selection context for Rotational Media Information Log Page.

- How to read: Start with the fixed header and scope, validate counts or lengths, then walk entries or data areas in order. Evidence index: ENDGID, NUMA, NRS, SPINC, FSPINC, LDC, FLDC.

- Conditions and limits: Source keyword index: `shall not`, `shall`, `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Read ENDGID first, use NUMA as an independent size or identity check, and stop before any unreturned byte. This example adds no requirement.

- Source field index: ENDGID, NUMA, NRS, SPINC, FSPINC, LDC, FLDC

- Source keyword index: `shall not`, `shall`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.22, Figure 281, printed pages 284-285, PDF pages 310-311

</details>

<details markdown="1">
<summary><strong>Figure 282: Dispersed Namespace Participating NVM Subsystems Log Page</strong></summary>

<!-- claim:BASEFWLOG-FIG-282-CLAIM figure-table:BASEFWLOG-FIG-282 -->

Figure 282, "Dispersed Namespace Participating NVM Subsystems Log Page": Defines the returned log-page layout and selection context for Dispersed Namespace Participating NVM Subsystems Log Page. Start with the fixed header and scope, validate counts or lengths, then walk entries or data areas in order. Evidence index: GENCTR, NUMPSUB, NVM Subsystem, Namespace.

- Purpose: Defines the returned log-page layout and selection context for Dispersed Namespace Participating NVM Subsystems Log Page.

- How to read: Start with the fixed header and scope, validate counts or lengths, then walk entries or data areas in order. Evidence index: GENCTR, NUMPSUB, NVM Subsystem, Namespace.

- Conditions and limits: Source keyword index: `shall`, `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Read GENCTR first, use NUMPSUB as an independent size or identity check, and stop before any unreturned byte. This example adds no requirement.

- Source field index: GENCTR, NUMPSUB, NVM Subsystem, Namespace

- Source keyword index: `shall`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.23, Figure 282, printed pages 285-286, PDF pages 311-312

</details>

<details markdown="1">
<summary><strong>Figure 283: Management Address List – Log Page</strong></summary>

<!-- claim:BASEFWLOG-FIG-283-CLAIM figure-table:BASEFWLOG-FIG-283 -->

Figure 283, "Management Address List – Log Page": Defines the returned log-page layout and selection context for Management Address List – Log Page. Start with the fixed header and scope, validate counts or lengths, then walk entries or data areas in order. Evidence index: MAD0, MAD1, MAD7.

- Purpose: Defines the returned log-page layout and selection context for Management Address List – Log Page.

- How to read: Start with the fixed header and scope, validate counts or lengths, then walk entries or data areas in order. Evidence index: MAD0, MAD1, MAD7.

- Conditions and limits: Source keyword index: `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Read MAD0 first, use MAD1 as an independent size or identity check, and stop before any unreturned byte. This example adds no requirement.

- Source field index: MAD0, MAD1, MAD7

- Source keyword index: `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.24, Figure 283, printed pages 286, PDF pages 312

</details>

<details markdown="1">
<summary><strong>Figure 284: Management Address Descriptor</strong></summary>

<!-- claim:BASEFWLOG-FIG-284-CLAIM figure-table:BASEFWLOG-FIG-284 -->

Figure 284, "Management Address Descriptor": Defines the concrete layout or value relationships for Management Address Descriptor. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is MAT, MADRS, SSD, URI, RFC, UTF.

- Purpose: Defines the concrete layout or value relationships for Management Address Descriptor.

- How to read: Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is MAT, MADRS, SSD, URI, RFC, UTF.

- Conditions and limits: Source keyword index: `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Use MAT as the first parser checkpoint and MADRS as a second, independent boundary check. This example adds no requirement.

- Source field index: MAT, MADRS, SSD, URI, RFC, UTF

- Source keyword index: `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.24, Figure 284, printed pages 286, PDF pages 312

</details>

<details markdown="1">
<summary><strong>Figure 285: Reachability Groups Log Specific Parameter Field</strong></summary>

<!-- claim:BASEFWLOG-FIG-285-CLAIM figure-table:BASEFWLOG-FIG-285 -->

Figure 285, "Reachability Groups Log Specific Parameter Field": Defines the concrete layout or value relationships for Reachability Groups Log Specific Parameter Field. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is RGO, NSID.

- Purpose: Defines the concrete layout or value relationships for Reachability Groups Log Specific Parameter Field.

- How to read: Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is RGO, NSID.

- Conditions and limits: Source keyword index: `shall`, `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Use RGO as the first parser checkpoint and NSID as a second, independent boundary check. This example adds no requirement.

- Source field index: RGO, NSID

- Source keyword index: `shall`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.25, Figure 285, printed pages 287, PDF pages 313

</details>

<details markdown="1">
<summary><strong>Figure 286: Reachability Groups Log Page</strong></summary>

<!-- claim:BASEFWLOG-FIG-286-CLAIM figure-table:BASEFWLOG-FIG-286 -->

Figure 286, "Reachability Groups Log Page": Defines the returned log-page layout and selection context for Reachability Groups Log Page. Start with the fixed header and scope, validate counts or lengths, then walk entries or data areas in order. Evidence index: CHNGC, NRGD, NSID.

- Purpose: Defines the returned log-page layout and selection context for Reachability Groups Log Page.

- How to read: Start with the fixed header and scope, validate counts or lengths, then walk entries or data areas in order. Evidence index: CHNGC, NRGD, NSID.

- Conditions and limits: Source keyword index: `shall`, `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Read CHNGC first, use NRGD as an independent size or identity check, and stop before any unreturned byte. This example adds no requirement.

- Source field index: CHNGC, NRGD, NSID

- Source keyword index: `shall`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.25, Figure 286, printed pages 287-288, PDF pages 313-314

</details>

<details markdown="1">
<summary><strong>Figure 287: Reachability Group Descriptor format</strong></summary>

<!-- claim:BASEFWLOG-FIG-287-CLAIM figure-table:BASEFWLOG-FIG-287 -->

Figure 287, "Reachability Group Descriptor format": Defines the concrete layout or value relationships for Reachability Group Descriptor format. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is RGID, NNID, CHNGC, ID, NSID, RGO.

- Purpose: Defines the concrete layout or value relationships for Reachability Group Descriptor format.

- How to read: Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is RGID, NNID, CHNGC, ID, NSID, RGO.

- Conditions and limits: Source keyword index: `shall`, `should`, `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Use RGID as the first parser checkpoint and NNID as a second, independent boundary check. This example adds no requirement.

- Source field index: RGID, NNID, CHNGC, ID, NSID, RGO

- Source keyword index: `shall`, `should`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.25, Figure 287, printed pages 288, PDF pages 314

</details>

<details markdown="1">
<summary><strong>Figure 288: Reachability Associations Log Specific Parameter Field</strong></summary>

<!-- claim:BASEFWLOG-FIG-288-CLAIM figure-table:BASEFWLOG-FIG-288 -->

Figure 288, "Reachability Associations Log Specific Parameter Field": Defines the concrete layout or value relationships for Reachability Associations Log Specific Parameter Field. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is RAO, RGID.

- Purpose: Defines the concrete layout or value relationships for Reachability Associations Log Specific Parameter Field.

- How to read: Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is RAO, RGID.

- Conditions and limits: Source keyword index: `shall`, `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Use RAO as the first parser checkpoint and RGID as a second, independent boundary check. This example adds no requirement.

- Source field index: RAO, RGID

- Source keyword index: `shall`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.26, Figure 288, printed pages 289, PDF pages 315

</details>

<details markdown="1">
<summary><strong>Figure 289: Reachability Associations Log Page</strong></summary>

<!-- claim:BASEFWLOG-FIG-289-CLAIM figure-table:BASEFWLOG-FIG-289 -->

Figure 289, "Reachability Associations Log Page": Defines the returned log-page layout and selection context for Reachability Associations Log Page. Start with the fixed header and scope, validate counts or lengths, then walk entries or data areas in order. Evidence index: CHNGC, NRAD.

- Purpose: Defines the returned log-page layout and selection context for Reachability Associations Log Page.

- How to read: Start with the fixed header and scope, validate counts or lengths, then walk entries or data areas in order. Evidence index: CHNGC, NRAD.

- Conditions and limits: Source keyword index: `shall`, `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Read CHNGC first, use NRAD as an independent size or identity check, and stop before any unreturned byte. This example adds no requirement.

- Source field index: CHNGC, NRAD

- Source keyword index: `shall`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.26, Figure 289, printed pages 289, PDF pages 315

</details>

<details markdown="1">
<summary><strong>Figure 290: Reachability Association Descriptor format</strong></summary>

<!-- claim:BASEFWLOG-FIG-290-CLAIM figure-table:BASEFWLOG-FIG-290 -->

Figure 290, "Reachability Association Descriptor format": Defines the concrete layout or value relationships for Reachability Association Descriptor format. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is RASID, NRID, CHNGC, RAC, ID, RGID, RAO.

- Purpose: Defines the concrete layout or value relationships for Reachability Association Descriptor format.

- How to read: Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is RASID, NRID, CHNGC, RAC, ID, RGID, RAO.

- Conditions and limits: Source keyword index: `shall`, `should`, `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Use RASID as the first parser checkpoint and NRID as a second, independent boundary check. This example adds no requirement.

- Source field index: RASID, NRID, CHNGC, RAC, ID, RGID, RAO

- Source keyword index: `shall`, `should`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.26, Figure 290, printed pages 290, PDF pages 316

</details>

<details markdown="1">
<summary><strong>Figure 291: Device Personalities Log Page</strong></summary>

<!-- claim:BASEFWLOG-FIG-291-CLAIM figure-table:BASEFWLOG-FIG-291 -->

Figure 291, "Device Personalities Log Page": Defines the returned log-page layout and selection context for Device Personalities Log Page. Start with the fixed header and scope, validate counts or lengths, then walk entries or data areas in order. Evidence index: NUMP, CDPLPV, DPLPHL, CDPLPS, CDP, PPS.

- Purpose: Defines the returned log-page layout and selection context for Device Personalities Log Page.

- How to read: Start with the fixed header and scope, validate counts or lengths, then walk entries or data areas in order. Evidence index: NUMP, CDPLPV, DPLPHL, CDPLPS, CDP, PPS.

- Conditions and limits: Source keyword index: `shall`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Read NUMP first, use CDPLPV as an independent size or identity check, and stop before any unreturned byte. This example adds no requirement.

- Source field index: NUMP, CDPLPV, DPLPHL, CDPLPS, CDP, PPS

- Source keyword index: `shall`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.28, Figure 291, printed pages 291, PDF pages 317

</details>

<details markdown="1">
<summary><strong>Figure 292: Personality Properties Data Structure</strong></summary>

<!-- claim:BASEFWLOG-FIG-292-CLAIM figure-table:BASEFWLOG-FIG-292 -->

Figure 292, "Personality Properties Data Structure": Defines the concrete layout or value relationships for Personality Properties Data Structure. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is PPS, PERID, MRSTT, AUS, PKAS, PCAS, PSCUDE, CDP.

- Purpose: Defines the concrete layout or value relationships for Personality Properties Data Structure.

- How to read: Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is PPS, PERID, MRSTT, AUS, PKAS, PCAS, PSCUDE, CDP.

- Conditions and limits: Source keyword index: `shall`, `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Use PPS as the first parser checkpoint and PERID as a second, independent boundary check. This example adds no requirement.

- Source field index: PPS, PERID, MRSTT, AUS, PKAS, PCAS, PSCUDE, CDP

- Source keyword index: `shall`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.28, Figure 292, printed pages 291-293, PDF pages 317-319

</details>

<details markdown="1">
<summary><strong>Figure 293: FDP Configurations Log Page</strong></summary>

<!-- claim:BASEFWLOG-FIG-293-CLAIM figure-table:BASEFWLOG-FIG-293 -->

Figure 293, "FDP Configurations Log Page": Defines the returned log-page layout and selection context for FDP Configurations Log Page. Start with the fixed header and scope, validate counts or lengths, then walk entries or data areas in order. Evidence index: VER, SZE, FDP, UMFDPC.

- Purpose: Defines the returned log-page layout and selection context for FDP Configurations Log Page.

- How to read: Start with the fixed header and scope, validate counts or lengths, then walk entries or data areas in order. Evidence index: VER, SZE, FDP, UMFDPC.

- Conditions and limits: Source keyword index: `shall`, `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Read VER first, use SZE as an independent size or identity check, and stop before any unreturned byte. This example adds no requirement.

- Source field index: VER, SZE, FDP, UMFDPC

- Source keyword index: `shall`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.29, Figure 293, printed pages 293, PDF pages 319

</details>

<details markdown="1">
<summary><strong>Figure 294: FDP Configuration Descriptor</strong></summary>

<!-- claim:BASEFWLOG-FIG-294-CLAIM figure-table:BASEFWLOG-FIG-294 -->

Figure 294, "FDP Configuration Descriptor": Defines the concrete layout or value relationships for FDP Configuration Descriptor. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is DSZE, FDPA, FDPCV, FDPVWC, RGIF, VSS, NRG, NRUH.

- Purpose: Defines the concrete layout or value relationships for FDP Configuration Descriptor.

- How to read: Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is DSZE, FDPA, FDPCV, FDPVWC, RGIF, VSS, NRG, NRUH.

- Conditions and limits: Source keyword index: `shall`, `should`, `may`, `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Use DSZE as the first parser checkpoint and FDPA as a second, independent boundary check. This example adds no requirement.

- Source field index: DSZE, FDPA, FDPCV, FDPVWC, RGIF, VSS, NRG, NRUH

- Source keyword index: `shall`, `should`, `may`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.29, Figure 294, printed pages 293-295, PDF pages 319-321

</details>

<details markdown="1">
<summary><strong>Figure 295: Reclaim Unit Handle Descriptor</strong></summary>

<!-- claim:BASEFWLOG-FIG-295-CLAIM figure-table:BASEFWLOG-FIG-295 -->

Figure 295, "Reclaim Unit Handle Descriptor": Defines the concrete layout or value relationships for Reclaim Unit Handle Descriptor. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is RUHT, FDP, NRG, RGIF, Reclaim Unit.

- Purpose: Defines the concrete layout or value relationships for Reclaim Unit Handle Descriptor.

- How to read: Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is RUHT, FDP, NRG, RGIF, Reclaim Unit.

- Conditions and limits: Source keyword index: `shall`, `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Use RUHT as the first parser checkpoint and FDP as a second, independent boundary check. This example adds no requirement.

- Source field index: RUHT, FDP, NRG, RGIF, Reclaim Unit

- Source keyword index: `shall`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.29, Figure 295, printed pages 295, PDF pages 321

</details>

<details markdown="1">
<summary><strong>Figure 296: Placement Identifier Format without Reclaim Group Identifier</strong></summary>

<!-- claim:BASEFWLOG-FIG-296-CLAIM figure-table:BASEFWLOG-FIG-296 -->

Figure 296, "Placement Identifier Format without Reclaim Group Identifier": Defines the concrete layout or value relationships for Placement Identifier Format without Reclaim Group Identifier. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is PHNDL, Reclaim Group.

- Purpose: Defines the concrete layout or value relationships for Placement Identifier Format without Reclaim Group Identifier.

- How to read: Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is PHNDL, Reclaim Group.

- Conditions and limits: The Figure is explanatory or structural; this guide does not turn its visual relationship into a new requirement.

- Informative example: Use PHNDL as the first parser checkpoint and Reclaim Group as a second, independent boundary check. This example adds no requirement.

- Source field index: PHNDL, Reclaim Group

- Source keyword index: none

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.29, Figure 296, printed pages 295, PDF pages 321

</details>

<details markdown="1">
<summary><strong>Figure 297: Placement Identifier Format with a non-zero RGIF</strong></summary>

<!-- claim:BASEFWLOG-FIG-297-CLAIM figure-table:BASEFWLOG-FIG-297 -->

Figure 297, "Placement Identifier Format with a non-zero RGIF": Defines the concrete layout or value relationships for Placement Identifier Format with a non-zero RGIF. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is RGID, PHNDL, RGIF, NRG.

- Purpose: Defines the concrete layout or value relationships for Placement Identifier Format with a non-zero RGIF.

- How to read: Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is RGID, PHNDL, RGIF, NRG.

- Conditions and limits: Source keyword index: `shall`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Use RGID as the first parser checkpoint and PHNDL as a second, independent boundary check. This example adds no requirement.

- Source field index: RGID, PHNDL, RGIF, NRG

- Source keyword index: `shall`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.29, Figure 297, printed pages 296, PDF pages 322

</details>

<details markdown="1">
<summary><strong>Figure 298: Reclaim Unit Handle Usage Log Page</strong></summary>

<!-- claim:BASEFWLOG-FIG-298-CLAIM figure-table:BASEFWLOG-FIG-298 -->

Figure 298, "Reclaim Unit Handle Usage Log Page": Defines the returned log-page layout and selection context for Reclaim Unit Handle Usage Log Page. Start with the fixed header and scope, validate counts or lengths, then walk entries or data areas in order. Evidence index: NRUH, FDP, Reclaim Unit.

- Purpose: Defines the returned log-page layout and selection context for Reclaim Unit Handle Usage Log Page.

- How to read: Start with the fixed header and scope, validate counts or lengths, then walk entries or data areas in order. Evidence index: NRUH, FDP, Reclaim Unit.

- Conditions and limits: Source keyword index: `shall`, `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Read NRUH first, use FDP as an independent size or identity check, and stop before any unreturned byte. This example adds no requirement.

- Source field index: NRUH, FDP, Reclaim Unit

- Source keyword index: `shall`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.30, Figure 298, printed pages 296, PDF pages 322

</details>

<details markdown="1">
<summary><strong>Figure 299: Reclaim Unit Handle Usage Descriptor</strong></summary>

<!-- claim:BASEFWLOG-FIG-299-CLAIM figure-table:BASEFWLOG-FIG-299 -->

Figure 299, "Reclaim Unit Handle Usage Descriptor": Defines the concrete layout or value relationships for Reclaim Unit Handle Usage Descriptor. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is RUHA, Reclaim Unit.

- Purpose: Defines the concrete layout or value relationships for Reclaim Unit Handle Usage Descriptor.

- How to read: Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is RUHA, Reclaim Unit.

- Conditions and limits: Source keyword index: `shall`, `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Use RUHA as the first parser checkpoint and Reclaim Unit as a second, independent boundary check. This example adds no requirement.

- Source field index: RUHA, Reclaim Unit

- Source keyword index: `shall`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.30, Figure 299, printed pages 296-297, PDF pages 322-323

</details>

<details markdown="1">
<summary><strong>Figure 300: FDP Statistics Log Page</strong></summary>

<!-- claim:BASEFWLOG-FIG-300-CLAIM figure-table:BASEFWLOG-FIG-300 -->

Figure 300, "FDP Statistics Log Page": Defines the returned log-page layout and selection context for FDP Statistics Log Page. Start with the fixed header and scope, validate counts or lengths, then walk entries or data areas in order. Evidence index: HBMW, MBMW, MBE, FDP.

- Purpose: Defines the returned log-page layout and selection context for FDP Statistics Log Page.

- How to read: Start with the fixed header and scope, validate counts or lengths, then walk entries or data areas in order. Evidence index: HBMW, MBMW, MBE, FDP.

- Conditions and limits: Source keyword index: `shall not`, `shall`, `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Read HBMW first, use MBMW as an independent size or identity check, and stop before any unreturned byte. This example adds no requirement.

- Source field index: HBMW, MBMW, MBE, FDP

- Source keyword index: `shall not`, `shall`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.31, Figure 300, printed pages 297, PDF pages 323

</details>

<details markdown="1">
<summary><strong>Figure 301: Command Dword 10 – Log Specific Field</strong></summary>

<!-- claim:BASEFWLOG-FIG-301-CLAIM figure-table:BASEFWLOG-FIG-301 -->

Figure 301, "Command Dword 10 – Log Specific Field": Defines the concrete layout or value relationships for Command Dword 10 – Log Specific Field. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is FDPET, FDP, Command.

- Purpose: Defines the concrete layout or value relationships for Command Dword 10 – Log Specific Field.

- How to read: Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is FDPET, FDP, Command.

- Conditions and limits: Source keyword index: `shall`, `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Use FDPET as the first parser checkpoint and FDP as a second, independent boundary check. This example adds no requirement.

- Source field index: FDPET, FDP, Command

- Source keyword index: `shall`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.32, Figure 301, printed pages 298, PDF pages 324

</details>

<details markdown="1">
<summary><strong>Figure 302: FDP Events Log Page</strong></summary>

<!-- claim:BASEFWLOG-FIG-302-CLAIM figure-table:BASEFWLOG-FIG-302 -->

Figure 302, "FDP Events Log Page": Defines the returned log-page layout and selection context for FDP Events Log Page. Start with the fixed header and scope, validate counts or lengths, then walk entries or data areas in order. Evidence index: NUMFDPE, FDP, NUMFDPC.

- Purpose: Defines the returned log-page layout and selection context for FDP Events Log Page.

- How to read: Start with the fixed header and scope, validate counts or lengths, then walk entries or data areas in order. Evidence index: NUMFDPE, FDP, NUMFDPC.

- Conditions and limits: Source keyword index: `shall`, `may`, `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Read NUMFDPE first, use FDP as an independent size or identity check, and stop before any unreturned byte. This example adds no requirement.

- Source field index: NUMFDPE, FDP, NUMFDPC

- Source keyword index: `shall`, `may`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.32, Figure 302, printed pages 298, PDF pages 324

</details>

<details markdown="1">
<summary><strong>Figure 303: FDP Event</strong></summary>

<!-- claim:BASEFWLOG-FIG-303-CLAIM figure-table:BASEFWLOG-FIG-303 -->

Figure 303, "FDP Event": Defines the event record, event taxonomy, or logging condition represented by FDP Event. Resolve event type and record length before decoding event-specific data. Evidence index: ETYP, FDPEF, LV, NSIDV, PIV, PID, ETMSP, NSID.

- Purpose: Defines the event record, event taxonomy, or logging condition represented by FDP Event.

- How to read: Resolve event type and record length before decoding event-specific data. Evidence index: ETYP, FDPEF, LV, NSIDV, PIV, PID, ETMSP, NSID.

- Conditions and limits: Source keyword index: `shall`, `should`, `may`, `optional`, `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Identify ETYP, validate the record boundary using FDPEF, and decode only the data defined for that event type. This example adds no requirement.

- Source field index: ETYP, FDPEF, LV, NSIDV, PIV, PID, ETMSP, NSID

- Source keyword index: `shall`, `should`, `may`, `optional`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.32, Figure 303, printed pages 299-300, PDF pages 325-326

</details>

<details markdown="1">
<summary><strong>Figure 304: Manufacturer Default Configuration Status Log Page</strong></summary>

<!-- claim:BASEFWLOG-FIG-304-CLAIM figure-table:BASEFWLOG-FIG-304 -->

Figure 304, "Manufacturer Default Configuration Status Log Page": Defines the returned log-page layout and selection context for Manufacturer Default Configuration Status Log Page. Start with the fixed header and scope, validate counts or lengths, then walk entries or data areas in order. Evidence index: MDCSV, MDCS, DCCS, DNCS, DSCS, RDCCS, RDNCS, RDSCS.

- Purpose: Defines the returned log-page layout and selection context for Manufacturer Default Configuration Status Log Page.

- How to read: Start with the fixed header and scope, validate counts or lengths, then walk entries or data areas in order. Evidence index: MDCSV, MDCS, DCCS, DNCS, DSCS, RDCCS, RDNCS, RDSCS.

- Conditions and limits: Source keyword index: `shall`, `should`, `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Read MDCSV first, use MDCS as an independent size or identity check, and stop before any unreturned byte. This example adds no requirement.

- Source field index: MDCSV, MDCS, DCCS, DNCS, DSCS, RDCCS, RDNCS, RDSCS

- Source keyword index: `shall`, `should`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.33, Figure 304, printed pages 301-302, PDF pages 327-328

</details>

<details markdown="1">
<summary><strong>Figure 305: Power Measurement Log Page</strong></summary>

<!-- claim:BASEFWLOG-FIG-305-CLAIM figure-table:BASEFWLOG-FIG-305 -->

Figure 305, "Power Measurement Log Page": Defines the returned log-page layout and selection context for Power Measurement Log Page. Start with the fixed header and scope, validate counts or lengths, then walk entries or data areas in order. Evidence index: VER, PMGN, PMA, PMT, PHDO, MIPWRTS, EPF, NCPDF.

- Purpose: Defines the returned log-page layout and selection context for Power Measurement Log Page.

- How to read: Start with the fixed header and scope, validate counts or lengths, then walk entries or data areas in order. Evidence index: VER, PMGN, PMA, PMT, PHDO, MIPWRTS, EPF, NCPDF.

- Conditions and limits: Source keyword index: `shall not`, `shall`, `should`, `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Read VER first, use PMGN as an independent size or identity check, and stop before any unreturned byte. This example adds no requirement.

- Source field index: VER, PMGN, PMA, PMT, PHDO, MIPWRTS, EPF, NCPDF

- Source keyword index: `shall not`, `shall`, `should`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.34, Figure 305, printed pages 303-306, PDF pages 329-332

</details>

<details markdown="1">
<summary><strong>Figure 306: Power Histogram Descriptor</strong></summary>

<!-- claim:BASEFWLOG-FIG-306-CLAIM figure-table:BASEFWLOG-FIG-306 -->

Figure 306, "Power Histogram Descriptor": Defines the concrete layout or value relationships for Power Histogram Descriptor. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is PHBC, PHBLT, PWRS, PWRV, PMT, PHBS, PMC.

- Purpose: Defines the concrete layout or value relationships for Power Histogram Descriptor.

- How to read: Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is PHBC, PHBLT, PWRS, PWRV, PMT, PHBS, PMC.

- Conditions and limits: Source keyword index: `shall not`, `shall`, `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Use PHBC as the first parser checkpoint and PHBLT as a second, independent boundary check. This example adds no requirement.

- Source field index: PHBC, PHBLT, PWRS, PWRV, PMT, PHBS, PMC

- Source keyword index: `shall not`, `shall`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.34, Figure 306, printed pages 306, PDF pages 332

</details>

<details markdown="1">
<summary><strong>Figure 307: Voltage Measurement Log Page</strong></summary>

<!-- claim:BASEFWLOG-FIG-307-CLAIM figure-table:BASEFWLOG-FIG-307 -->

Figure 307, "Voltage Measurement Log Page": Defines the returned log-page layout and selection context for Voltage Measurement Log Page. Start with the fixed header and scope, validate counts or lengths, then walk entries or data areas in order. Evidence index: VMGN, VMA, VMC, VSM, IVOLTS, VME, VSI, VSSS.

- Purpose: Defines the returned log-page layout and selection context for Voltage Measurement Log Page.

- How to read: Start with the fixed header and scope, validate counts or lengths, then walk entries or data areas in order. Evidence index: VMGN, VMA, VMC, VSM, IVOLTS, VME, VSI, VSSS.

- Conditions and limits: Source keyword index: `shall not`, `shall`, `should`, `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Read VMGN first, use VMA as an independent size or identity check, and stop before any unreturned byte. This example adds no requirement.

- Source field index: VMGN, VMA, VMC, VSM, IVOLTS, VME, VSI, VSSS

- Source keyword index: `shall not`, `shall`, `should`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.35, Figure 307, printed pages 307-311, PDF pages 333-337

</details>

<details markdown="1">
<summary><strong>Figure 308: Interval Voltage Measurement Descriptor</strong></summary>

<!-- claim:BASEFWLOG-FIG-308-CLAIM figure-table:BASEFWLOG-FIG-308 -->

Figure 308, "Interval Voltage Measurement Descriptor": Defines the concrete layout or value relationships for Interval Voltage Measurement Descriptor. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is IVOLM, NCVM, VOLV, VME, VOLSS.

- Purpose: Defines the concrete layout or value relationships for Interval Voltage Measurement Descriptor.

- How to read: Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is IVOLM, NCVM, VOLV, VME, VOLSS.

- Conditions and limits: Source keyword index: `shall`, `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Use IVOLM as the first parser checkpoint and NCVM as a second, independent boundary check. This example adds no requirement.

- Source field index: IVOLM, NCVM, VOLV, VME, VOLSS

- Source keyword index: `shall`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.35, Figure 308, printed pages 311, PDF pages 337

</details>

<details markdown="1">
<summary><strong>Figure 309: Sanitize Namespace Status List Log Specific Parameter Field</strong></summary>

<!-- claim:BASEFWLOG-FIG-309-CLAIM figure-table:BASEFWLOG-FIG-309 -->

Figure 309, "Sanitize Namespace Status List Log Specific Parameter Field": Defines the concrete layout or value relationships for Sanitize Namespace Status List Log Specific Parameter Field. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is NLT, NSID, CSTS.RDY, Namespace.

- Purpose: Defines the concrete layout or value relationships for Sanitize Namespace Status List Log Specific Parameter Field.

- How to read: Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is NLT, NSID, CSTS.RDY, Namespace.

- Conditions and limits: Source keyword index: `shall`, `may`, `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Use NLT as the first parser checkpoint and NSID as a second, independent boundary check. This example adds no requirement.

- Source field index: NLT, NSID, CSTS.RDY, Namespace

- Source keyword index: `shall`, `may`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.36, Figure 309, printed pages 311-312, PDF pages 337-338

</details>

<details markdown="1">
<summary><strong>Figure 310: Sanitize Namespace Status List Log Page</strong></summary>

<!-- claim:BASEFWLOG-FIG-310-CLAIM figure-table:BASEFWLOG-FIG-310 -->

Figure 310, "Sanitize Namespace Status List Log Page": Defines the returned log-page layout and selection context for Sanitize Namespace Status List Log Page. Start with the fixed header and scope, validate counts or lengths, then walk entries or data areas in order. Evidence index: GENCTR, NUMNSID, NSID, Namespace.

- Purpose: Defines the returned log-page layout and selection context for Sanitize Namespace Status List Log Page.

- How to read: Start with the fixed header and scope, validate counts or lengths, then walk entries or data areas in order. Evidence index: GENCTR, NUMNSID, NSID, Namespace.

- Conditions and limits: Source keyword index: `shall`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Read GENCTR first, use NUMNSID as an independent size or identity check, and stop before any unreturned byte. This example adds no requirement.

- Source field index: GENCTR, NUMNSID, NSID, Namespace

- Source keyword index: `shall`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.36, Figure 310, printed pages 312, PDF pages 338

</details>

<details markdown="1">
<summary><strong>Figure 311: Reservation Notification Log Page</strong></summary>

<!-- claim:BASEFWLOG-FIG-311-CLAIM figure-table:BASEFWLOG-FIG-311 -->

Figure 311, "Reservation Notification Log Page": Defines the returned log-page layout and selection context for Reservation Notification Log Page. Start with the fixed header and scope, validate counts or lengths, then walk entries or data areas in order. Evidence index: LPC, RNLPT, NALP, NSID, ID.

- Purpose: Defines the returned log-page layout and selection context for Reservation Notification Log Page.

- How to read: Start with the fixed header and scope, validate counts or lengths, then walk entries or data areas in order. Evidence index: LPC, RNLPT, NALP, NSID, ID.

- Conditions and limits: Source keyword index: `shall`, `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Read LPC first, use RNLPT as an independent size or identity check, and stop before any unreturned byte. This example adds no requirement.

- Source field index: LPC, RNLPT, NALP, NSID, ID

- Source keyword index: `shall`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.37, Figure 311, printed pages 313, PDF pages 339

</details>

<details markdown="1">
<summary><strong>Figure 312: Sanitize Status Log Page</strong></summary>

<!-- claim:BASEFWLOG-FIG-312-CLAIM figure-table:BASEFWLOG-FIG-312 -->

Figure 312, "Sanitize Status Log Page": Defines the returned log-page layout and selection context for Sanitize Status Log Page. Start with the fixed header and scope, validate counts or lengths, then walk entries or data areas in order. Evidence index: SPROG, OPC, SOS, SCDW10, ETO, ETBE, ETCE, ETODMM.

- Purpose: Defines the returned log-page layout and selection context for Sanitize Status Log Page.

- How to read: Start with the fixed header and scope, validate counts or lengths, then walk entries or data areas in order. Evidence index: SPROG, OPC, SOS, SCDW10, ETO, ETBE, ETCE, ETODMM.

- Conditions and limits: Source keyword index: `shall`, `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Read SPROG first, use OPC as an independent size or identity check, and stop before any unreturned byte. This example adds no requirement.

- Source field index: SPROG, OPC, SOS, SCDW10, ETO, ETBE, ETCE, ETODMM

- Source keyword index: `shall`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.38, Figure 312, printed pages 314-319, PDF pages 340-345

</details>

<details markdown="1">
<summary><strong>Figure 331: Get Log Page – Command Specific Status Values</strong></summary>

<!-- claim:BASEFWLOG-FIG-331-CLAIM figure-table:BASEFWLOG-FIG-331 -->

Figure 331, "Get Log Page – Command Specific Status Values": Defines the returned log-page layout and selection context for Get Log Page – Command Specific Status Values. Start with the fixed header and scope, validate counts or lengths, then walk entries or data areas in order. Evidence index: Invalid Log Page, Invalid Controller Identifier, I/O Command Set Not Supported.

- Purpose: Defines the returned log-page layout and selection context for Get Log Page – Command Specific Status Values.

- How to read: Start with the fixed header and scope, validate counts or lengths, then walk entries or data areas in order. Evidence index: Invalid Log Page, Invalid Controller Identifier, I/O Command Set Not Supported.

- Conditions and limits: Source keyword index: `may`, `reserved`. The index locates normative language but does not replace the condition attached to each field.

- Informative example: Read Invalid Log Page first, use Invalid Controller Identifier as an independent size or identity check, and stop before any unreturned byte. This example adds no requirement.

- Source field index: Invalid Log Page, Invalid Controller Identifier, I/O Command Set Not Supported

- Source keyword index: `may`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.3.6, Figure 331, printed pages 336, PDF pages 362

</details>

<a id="section-dependency"></a>

### Referenced Figure dependencies (outside the main section range)

<details markdown="1">
<summary><strong>Figure 70: Flexible Data Placement Logical View of Non-Volatile Storage</strong></summary>

<!-- claim:BASEFWLOG-FIG-070-CLAIM figure-table:BASEFWLOG-FIG-070 -->

Figure 70, "Flexible Data Placement Logical View of Non-Volatile Storage": Shows the object or capacity relationships in Flexible Data Placement Logical View of Non-Volatile Storage. Separate logical identifiers from controllers, namespaces, ports, and capacity containers. Evidence index: Endurance Group, Reclaim Group, Reclaim Unit, Reclaim Unit Handle.

- Purpose: Shows the object or capacity relationships in Flexible Data Placement Logical View of Non-Volatile Storage.

- How to read: Separate logical identifiers from controllers, namespaces, ports, and capacity containers. Evidence index: Endurance Group, Reclaim Group, Reclaim Unit, Reclaim Unit Handle.

- Conditions and limits: The Figure is explanatory or structural; this guide does not turn its visual relationship into a new requirement. This Figure is a dependency referenced from §5.2.13.1.29, §5.2.13.1.30; only the elements needed by the requested sections are taught here.

- Informative example: Choose one object labeled by Endurance Group and trace its relationship to Reclaim Group without treating an identifier as the object itself. This example adds no requirement.

- Source field index: Endurance Group, Reclaim Group, Reclaim Unit, Reclaim Unit Handle

- Source keyword index: none

> Source: NVME-BASE-2.4, Rev. 2.4, §3.2.4, Figure 70, printed pages 85, PDF pages 111

</details>

<details markdown="1">
<summary><strong>Figure 84: Admin Commands Permitted to Return a Status Code of Admin Command Media Not Ready</strong></summary>

<!-- claim:BASEFWLOG-FIG-084-CLAIM figure-table:BASEFWLOG-FIG-084 -->

Figure 84, "Admin Commands Permitted to Return a Status Code of Admin Command Media Not Ready": Defines the status/error classification represented by Admin Commands Permitted to Return a Status Code of Admin Command Media Not Ready. Resolve the category before the individual code or flag; keep reserved values uninterpreted. Evidence index: LBA, CAP.CRMS, CAP.CRMS.CRWMS, CAP.CRMS.CRIMS, CC.CRIME, Status Code, Command.

- Purpose: Defines the status/error classification represented by Admin Commands Permitted to Return a Status Code of Admin Command Media Not Ready.

- How to read: Resolve the category before the individual code or flag; keep reserved values uninterpreted. Evidence index: LBA, CAP.CRMS, CAP.CRMS.CRWMS, CAP.CRMS.CRIMS, CC.CRIME, Status Code, Command.

- Conditions and limits: Source keyword index: `shall`, `should`, `may`. The index locates normative language but does not replace the condition attached to each field. This Figure is a dependency referenced from §5.2.13.1.3; only the elements needed by the requested sections are taught here.

- Informative example: For one reported condition, identify LBA first and then check CAP.CRMS instead of decoding an isolated numeric value. This example adds no requirement.

- Source field index: LBA, CAP.CRMS, CAP.CRMS.CRWMS, CAP.CRMS.CRIMS, CC.CRIME, Status Code, Command

- Source keyword index: `shall`, `should`, `may`

> Source: NVME-BASE-2.4, Rev. 2.4, §3.5.3, Figure 84, printed pages 110-111, PDF pages 136-137

</details>

<details markdown="1">
<summary><strong>Figure 93: Common Command Format</strong></summary>

<!-- claim:BASEFWLOG-FIG-093-CLAIM figure-table:BASEFWLOG-FIG-093 -->

Figure 93, "Common Command Format": Defines the concrete layout or value relationships for Common Command Format. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is CDW0, NSID, CDW2, CDW3, MPTR, DPTR, PRP2, PRP1.

- Purpose: Defines the concrete layout or value relationships for Common Command Format.

- How to read: Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is CDW0, NSID, CDW2, CDW3, MPTR, DPTR, PRP2, PRP1.

- Conditions and limits: Source keyword index: `shall`, `may`, `reserved`. The index locates normative language but does not replace the condition attached to each field. This Figure is a dependency referenced from §5.2.10, §5.2.13; only the elements needed by the requested sections are taught here.

- Informative example: Use CDW0 as the first parser checkpoint and NSID as a second, independent boundary check. This example adds no requirement.

- Source field index: CDW0, NSID, CDW2, CDW3, MPTR, DPTR, PRP2, PRP1

- Source keyword index: `shall`, `may`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §4.1.1, Figure 93, printed pages 140-142, PDF pages 166-168

</details>

<details markdown="1">
<summary><strong>Figure 101: Completion Queue Entry: Status Field</strong></summary>

<!-- claim:BASEFWLOG-FIG-101-CLAIM figure-table:BASEFWLOG-FIG-101 -->

Figure 101, "Completion Queue Entry: Status Field": Defines the concrete layout or value relationships for Completion Queue Entry: Status Field. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is DNR, CRD, SCT, SC, ACRE, CRDT1, CRDT2, CRDT3.

- Purpose: Defines the concrete layout or value relationships for Completion Queue Entry: Status Field.

- How to read: Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is DNR, CRD, SCT, SC, ACRE, CRDT1, CRDT2, CRDT3.

- Conditions and limits: Source keyword index: `should not`, `should`, `may`, `reserved`. The index locates normative language but does not replace the condition attached to each field. This Figure is a dependency referenced from §5.2.13.1.2, §5.2.13.1.14; only the elements needed by the requested sections are taught here.

- Informative example: Use DNR as the first parser checkpoint and CRD as a second, independent boundary check. This example adds no requirement.

- Source field index: DNR, CRD, SCT, SC, ACRE, CRDT1, CRDT2, CRDT3

- Source keyword index: `should not`, `should`, `may`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §4.2.3, Figure 101, printed pages 145-146, PDF pages 171-172

</details>

<details markdown="1">
<summary><strong>Figure 102: Status Code – Status Code Type Values</strong></summary>

<!-- claim:BASEFWLOG-FIG-102-CLAIM figure-table:BASEFWLOG-FIG-102 -->

Figure 102, "Status Code – Status Code Type Values": Defines the status/error classification represented by Status Code – Status Code Type Values. Resolve the category before the individual code or flag; keep reserved values uninterpreted. Evidence index: SC, Status Code.

- Purpose: Defines the status/error classification represented by Status Code – Status Code Type Values.

- How to read: Resolve the category before the individual code or flag; keep reserved values uninterpreted. Evidence index: SC, Status Code.

- Conditions and limits: Source keyword index: `shall`, `may`, `reserved`. The index locates normative language but does not replace the condition attached to each field. This Figure is a dependency referenced from §5.2.13.1.14; only the elements needed by the requested sections are taught here.

- Informative example: For one reported condition, identify SC first and then check Status Code instead of decoding an isolated numeric value. This example adds no requirement.

- Source field index: SC, Status Code

- Source keyword index: `shall`, `may`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §4.2.3, Figure 102, printed pages 146, PDF pages 172

</details>

<details markdown="1">
<summary><strong>Figure 107: Status Code – Media and Data Integrity Error Values</strong></summary>

<!-- claim:BASEFWLOG-FIG-107-CLAIM figure-table:BASEFWLOG-FIG-107 -->

Figure 107, "Status Code – Media and Data Integrity Error Values": Defines the status/error classification represented by Status Code – Media and Data Integrity Error Values. Resolve the category before the individual code or flag; keep reserved values uninterpreted. Evidence index: TCG, SCT, Status Code.

- Purpose: Defines the status/error classification represented by Status Code – Media and Data Integrity Error Values.

- How to read: Resolve the category before the individual code or flag; keep reserved values uninterpreted. Evidence index: TCG, SCT, Status Code.

- Conditions and limits: Source keyword index: `should`, `may`, `reserved`. The index locates normative language but does not replace the condition attached to each field. This Figure is a dependency referenced from §5.2.13.1.14.2.5; only the elements needed by the requested sections are taught here.

- Informative example: For one reported condition, identify TCG first and then check SCT instead of decoding an isolated numeric value. This example adds no requirement.

- Source field index: TCG, SCT, Status Code

- Source keyword index: `should`, `may`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §4.2.3.2, Figure 107, printed pages 154-155, PDF pages 180-181

</details>

<details markdown="1">
<summary><strong>Figure 155: Asynchronous Event Information – Notice</strong></summary>

<!-- claim:BASEFWLOG-FIG-155-CLAIM figure-table:BASEFWLOG-FIG-155 -->

Figure 155, "Asynchronous Event Information – Notice": Defines the event record, event taxonomy, or logging condition represented by Asynchronous Event Information – Notice. Resolve event type and record length before decoding event-specific data. Evidence index: Firmware Activation Starting, CSTS.PP, Firmware Slot Information, RAE.

- Purpose: Defines the event record, event taxonomy, or logging condition represented by Asynchronous Event Information – Notice.

- How to read: Resolve event type and record length before decoding event-specific data. Evidence index: Firmware Activation Starting, CSTS.PP, Firmware Slot Information, RAE.

- Conditions and limits: Source keyword index: `shall not`, `shall`, `may`. The index locates normative language but does not replace the condition attached to each field. This Figure is a dependency referenced from §3.11, §5.2.30.1.6; only the elements needed by the requested sections are taught here. Use only the firmware-activation notice, CSTS.PP, and the Firmware Slot Information log used to clear the event.

- Informative example: Identify Firmware Activation Starting, validate the record boundary using CSTS.PP, and decode only the data defined for that event type. This example adds no requirement.

- Source field index: Firmware Activation Starting, CSTS.PP, Firmware Slot Information, RAE

- Source keyword index: `shall not`, `shall`, `may`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.2.1, Figure 155, printed pages 186, PDF pages 212

</details>

<details markdown="1">
<summary><strong>Figure 195: Format NVM – Command Dword 10</strong></summary>

<!-- claim:BASEFWLOG-FIG-195-CLAIM figure-table:BASEFWLOG-FIG-195 -->

Figure 195, "Format NVM – Command Dword 10": Defines the concrete layout or value relationships for Format NVM – Command Dword 10. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is LBAFU, SES, PIL, PI, MSET, LBA, LBAFEE, NOTE.

- Purpose: Defines the concrete layout or value relationships for Format NVM – Command Dword 10.

- How to read: Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is LBAFU, SES, PIL, PI, MSET, LBA, LBAFEE, NOTE.

- Conditions and limits: Source keyword index: `shall`, `should`, `may`, `reserved`. The index locates normative language but does not replace the condition attached to each field. This Figure is a dependency referenced from §5.2.13.1.14.2.7; only the elements needed by the requested sections are taught here.

- Informative example: Use LBAFU as the first parser checkpoint and SES as a second, independent boundary check. This example adds no requirement.

- Source field index: LBAFU, SES, PIL, PI, MSET, LBA, LBAFEE, NOTE

- Source keyword index: `shall`, `should`, `may`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.11, Figure 195, printed pages 208, PDF pages 234

</details>

<details markdown="1">
<summary><strong>Figure 337: Command Set Identifiers</strong></summary>

<!-- claim:BASEFWLOG-FIG-337-CLAIM figure-table:BASEFWLOG-FIG-337 -->

Figure 337, "Command Set Identifiers": Defines the identifier composition or namespace of values shown by Command Set Identifiers. Keep the value width, issuing authority, uniqueness scope, and reserved values separate. Evidence index: Command Set, Command.

- Purpose: Defines the identifier composition or namespace of values shown by Command Set Identifiers.

- How to read: Keep the value width, issuing authority, uniqueness scope, and reserved values separate. Evidence index: Command Set, Command.

- Conditions and limits: Source keyword index: `reserved`. The index locates normative language but does not replace the condition attached to each field. This Figure is a dependency referenced from §5.2.9, §5.2.13; only the elements needed by the requested sections are taught here. Section 5.2.9 points to Figure 337, but Figure 337 lists Command Set Identifiers; the firmware fields are in Figure 338.

- Informative example: Parse Command Set at its defined width, then validate the scope associated with Command before using it as an identity key. This example adds no requirement.

- Source field index: Command Set, Command

- Source keyword index: `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.14.1, Figure 337, printed pages 340, PDF pages 366

</details>

<details markdown="1">
<summary><strong>Figure 338: Identify – Identify Controller Data Structure, I/O Command Set Independent</strong></summary>

<!-- claim:BASEFWLOG-FIG-338-CLAIM figure-table:BASEFWLOG-FIG-338 -->

Figure 338, "Identify – Identify Controller Data Structure, I/O Command Set Independent": Defines the concrete layout or value relationships for Identify – Identify Controller Data Structure, I/O Command Set Independent. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is VID, SSVID, SN, MN, FR, FRMW, SMUD, FAWR.

- Purpose: Defines the concrete layout or value relationships for Identify – Identify Controller Data Structure, I/O Command Set Independent.

- How to read: Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is VID, SSVID, SN, MN, FR, FRMW, SMUD, FAWR.

- Conditions and limits: Source keyword index: `shall`, `should`, `may`, `optional`, `reserved`. The index locates normative language but does not replace the condition attached to each field. This Figure is a dependency referenced from §3.11, §5.2.9, §5.2.10, §5.2.13; only the elements needed by the requested sections are taught here. Use only FR, FRMW/SMUD/FAWR, MTFA, and FWUG for the firmware workflow; other Identify Controller fields are not expanded.

- Informative example: Use VID as the first parser checkpoint and SSVID as a second, independent boundary check. This example adds no requirement.

- Source field index: VID, SSVID, SN, MN, FR, FRMW, SMUD, FAWR

- Source keyword index: `shall`, `should`, `may`, `optional`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.14.2.1, Figure 338, printed pages 340-359, PDF pages 366-385

</details>

<details markdown="1">
<summary><strong>Figure 339: Identify – Voltage Sensor Data Structure</strong></summary>

<!-- claim:BASEFWLOG-FIG-339-CLAIM figure-table:BASEFWLOG-FIG-339 -->

Figure 339, "Identify – Voltage Sensor Data Structure": Defines the concrete layout or value relationships for Identify – Voltage Sensor Data Structure. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is IVMSR, VSRS, VSRV, VOLSS, PIT, PISL, PISV, VSEN1.

- Purpose: Defines the concrete layout or value relationships for Identify – Voltage Sensor Data Structure.

- How to read: Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is IVMSR, VSRS, VSRV, VOLSS, PIT, PISL, PISV, VSEN1.

- Conditions and limits: Source keyword index: `shall`, `reserved`. The index locates normative language but does not replace the condition attached to each field. This Figure is a dependency referenced from §5.2.13.1.35; only the elements needed by the requested sections are taught here.

- Informative example: Use IVMSR as the first parser checkpoint and VSRS as a second, independent boundary check. This example adds no requirement.

- Source field index: IVMSR, VSRS, VSRV, VOLSS, PIT, PISL, PISV, VSEN1

- Source keyword index: `shall`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.14.2.1, Figure 339, printed pages 383, PDF pages 409

</details>

<details markdown="1">
<summary><strong>Figure 346: Identify – I/O Command Set Independent Identify Namespace Data Structure</strong></summary>

<!-- claim:BASEFWLOG-FIG-346-CLAIM figure-table:BASEFWLOG-FIG-346 -->

Figure 346, "Identify – I/O Command Set Independent Identify Namespace Data Structure": Defines the concrete layout or value relationships for Identify – I/O Command Set Independent Identify Namespace Data Structure. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is NSFEAT, VWCNP, RMEDIA, UIDREUSE, NMIC, DISNS, SHRNS, RESCAP.

- Purpose: Defines the concrete layout or value relationships for Identify – I/O Command Set Independent Identify Namespace Data Structure.

- How to read: Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is NSFEAT, VWCNP, RMEDIA, UIDREUSE, NMIC, DISNS, SHRNS, RESCAP.

- Conditions and limits: Source keyword index: `shall`, `should`, `may`, `optional`, `reserved`. The index locates normative language but does not replace the condition attached to each field. This Figure is a dependency referenced from §5.2.13.1.14.2.6; only the elements needed by the requested sections are taught here.

- Informative example: Use NSFEAT as the first parser checkpoint and VWCNP as a second, independent boundary check. This example adds no requirement.

- Source field index: NSFEAT, VWCNP, RMEDIA, UIDREUSE, NMIC, DISNS, SHRNS, RESCAP

- Source keyword index: `shall`, `should`, `may`, `optional`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.14.2.8, Figure 346, printed pages 391-394, PDF pages 417-420

</details>

<details markdown="1">
<summary><strong>Figure 347: UUID List</strong></summary>

<!-- claim:BASEFWLOG-FIG-347-CLAIM figure-table:BASEFWLOG-FIG-347 -->

Figure 347, "UUID List": Defines the identifier composition or namespace of values shown by UUID List. Keep the value width, issuing authority, uniqueness scope, and reserved values separate. Evidence index: UUID1, UUID2, UUID126, UUID127, UUID.

- Purpose: Defines the identifier composition or namespace of values shown by UUID List.

- How to read: Keep the value width, issuing authority, uniqueness scope, and reserved values separate. Evidence index: UUID1, UUID2, UUID126, UUID127, UUID.

- Conditions and limits: Source keyword index: `shall`, `reserved`. The index locates normative language but does not replace the condition attached to each field. This Figure is a dependency referenced from §3.11.1; only the elements needed by the requested sections are taught here. Used for the UUID-list slot-stability and no-shortening rules in section 3.11.1.

- Informative example: Parse UUID1 at its defined width, then validate the scope associated with UUID2 before using it as an identity key. This example adds no requirement.

- Source field index: UUID1, UUID2, UUID126, UUID127, UUID

- Source keyword index: `shall`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.14.2.14, Figure 347, printed pages 396, PDF pages 422

</details>

<details markdown="1">
<summary><strong>Figure 348: UUID List Entry</strong></summary>

<!-- claim:BASEFWLOG-FIG-348-CLAIM figure-table:BASEFWLOG-FIG-348 -->

Figure 348, "UUID List Entry": Defines the identifier composition or namespace of values shown by UUID List Entry. Keep the value width, issuing authority, uniqueness scope, and reserved values separate. Evidence index: ULEH, IDASSOC, UUID, ID, RFC.

- Purpose: Defines the identifier composition or namespace of values shown by UUID List Entry.

- How to read: Keep the value width, issuing authority, uniqueness scope, and reserved values separate. Evidence index: ULEH, IDASSOC, UUID, ID, RFC.

- Conditions and limits: Source keyword index: `reserved`. The index locates normative language but does not replace the condition attached to each field. This Figure is a dependency referenced from §3.11.1; only the elements needed by the requested sections are taught here. Used to distinguish an empty entry, the NVMe Invalid UUID, and a valid UUID.

- Informative example: Parse ULEH at its defined width, then validate the scope associated with IDASSOC before using it as an identity key. This example adds no requirement.

- Source field index: ULEH, IDASSOC, UUID, ID, RFC

- Source keyword index: `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.14.2.14, Figure 348, printed pages 396, PDF pages 422

</details>

<details markdown="1">
<summary><strong>Figure 448: Namespace Management – Data Structure for Create</strong></summary>

<!-- claim:BASEFWLOG-FIG-448-CLAIM figure-table:BASEFWLOG-FIG-448 -->

Figure 448, "Namespace Management – Data Structure for Create": Defines the concrete layout or value relationships for Namespace Management – Data Structure for Create. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is SIOCS, VS, RDNCS, CSS, DNCS, Namespace.

- Purpose: Defines the concrete layout or value relationships for Namespace Management – Data Structure for Create.

- How to read: Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is SIOCS, VS, RDNCS, CSS, DNCS, Namespace.

- Conditions and limits: Source keyword index: `shall`, `reserved`. The index locates normative language but does not replace the condition attached to each field. This Figure is a dependency referenced from §5.2.13.1.14.2.6; only the elements needed by the requested sections are taught here.

- Informative example: Use SIOCS as the first parser checkpoint and VS as a second, independent boundary check. This example adds no requirement.

- Source field index: SIOCS, VS, RDNCS, CSS, DNCS, Namespace

- Source keyword index: `shall`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.25, Figure 448, printed pages 447, PDF pages 473

</details>

<details markdown="1">
<summary><strong>Figure 451: Sanitize – Command Dword 10</strong></summary>

<!-- claim:BASEFWLOG-FIG-451-CLAIM figure-table:BASEFWLOG-FIG-451 -->

Figure 451, "Sanitize – Command Dword 10": Defines the concrete layout or value relationships for Sanitize – Command Dword 10. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is PREQ, EMVS, NDAS, OIPBP, OWPASS, AUSE, SANACT, IEEE.

- Purpose: Defines the concrete layout or value relationships for Sanitize – Command Dword 10.

- How to read: Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is PREQ, EMVS, NDAS, OIPBP, OWPASS, AUSE, SANACT, IEEE.

- Conditions and limits: Source keyword index: `shall not`, `shall`, `should`, `reserved`. The index locates normative language but does not replace the condition attached to each field. This Figure is a dependency referenced from §5.2.13.1.14.2.9, §5.2.13.1.38; only the elements needed by the requested sections are taught here.

- Informative example: Use PREQ as the first parser checkpoint and EMVS as a second, independent boundary check. This example adds no requirement.

- Source field index: PREQ, EMVS, NDAS, OIPBP, OWPASS, AUSE, SANACT, IEEE

- Source keyword index: `shall not`, `shall`, `should`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.26, Figure 451, printed pages 450-451, PDF pages 476-477

</details>

<details markdown="1">
<summary><strong>Figure 452: Sanitize – Command Dword 11</strong></summary>

<!-- claim:BASEFWLOG-FIG-452-CLAIM figure-table:BASEFWLOG-FIG-452 -->

Figure 452, "Sanitize – Command Dword 11": Defines the concrete layout or value relationships for Sanitize – Command Dword 11. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is OVRPAT, SCT, Command.

- Purpose: Defines the concrete layout or value relationships for Sanitize – Command Dword 11.

- How to read: Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is OVRPAT, SCT, Command.

- Conditions and limits: Source keyword index: `shall`. The index locates normative language but does not replace the condition attached to each field. This Figure is a dependency referenced from §5.2.13.1.14.2.9, §5.2.13.1.38; only the elements needed by the requested sections are taught here.

- Informative example: Use OVRPAT as the first parser checkpoint and SCT as a second, independent boundary check. This example adds no requirement.

- Source field index: OVRPAT, SCT, Command

- Source keyword index: `shall`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.26, Figure 452, printed pages 451, PDF pages 477

</details>

<details markdown="1">
<summary><strong>Figure 466: Set Features – Feature Identifiers</strong></summary>

<!-- claim:BASEFWLOG-FIG-466-CLAIM figure-table:BASEFWLOG-FIG-466 -->

Figure 466, "Set Features – Feature Identifiers": Defines the identifier composition or namespace of values shown by Set Features – Feature Identifiers. Keep the value width, issuing authority, uniqueness scope, and reserved values separate. Evidence index: ID, MR, UUID.

- Purpose: Defines the identifier composition or namespace of values shown by Set Features – Feature Identifiers.

- How to read: Keep the value width, issuing authority, uniqueness scope, and reserved values separate. Evidence index: ID, MR, UUID.

- Conditions and limits: Source keyword index: `shall`, `should`, `may`, `optional`, `reserved`. The index locates normative language but does not replace the condition attached to each field. This Figure is a dependency referenced from §5.2.13.1.18; only the elements needed by the requested sections are taught here.

- Informative example: Parse ID at its defined width, then validate the scope associated with MR before using it as an identity key. This example adds no requirement.

- Source field index: ID, MR, UUID

- Source keyword index: `shall`, `should`, `may`, `optional`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30, Figure 466, printed pages 457-459, PDF pages 483-485

</details>

<details markdown="1">
<summary><strong>Figure 474: Asynchronous Event Configuration – Command Dword 11</strong></summary>

<!-- claim:BASEFWLOG-FIG-474-CLAIM figure-table:BASEFWLOG-FIG-474 -->

Figure 474, "Asynchronous Event Configuration – Command Dword 11": Defines the event record, event taxonomy, or logging condition represented by Asynchronous Event Configuration – Command Dword 11. Resolve event type and record length before decoding event-specific data. Evidence index: ZDCN, RLCCN, ANSAN, RGRP0, RASSN, TTHRY, NNSSHDN, EGEALCN.

- Purpose: Defines the event record, event taxonomy, or logging condition represented by Asynchronous Event Configuration – Command Dword 11.

- How to read: Resolve event type and record length before decoding event-specific data. Evidence index: ZDCN, RLCCN, ANSAN, RGRP0, RASSN, TTHRY, NNSSHDN, EGEALCN.

- Conditions and limits: Source keyword index: `shall not`, `shall`, `reserved`. The index locates normative language but does not replace the condition attached to each field. This Figure is a dependency referenced from §3.11; only the elements needed by the requested sections are taught here. Use only the Firmware Activation Notices enable bit associated with the activation-starting event in section 3.11.

- Informative example: Identify ZDCN, validate the record boundary using RLCCN, and decode only the data defined for that event type. This example adds no requirement.

- Source field index: ZDCN, RLCCN, ANSAN, RGRP0, RASSN, TTHRY, NNSSHDN, EGEALCN

- Source keyword index: `shall not`, `shall`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.6, Figure 474, printed pages 466-468, PDF pages 492-494

</details>

<details markdown="1">
<summary><strong>Figure 480: Timestamp – Data Structure for Get Features</strong></summary>

<!-- claim:BASEFWLOG-FIG-480-CLAIM figure-table:BASEFWLOG-FIG-480 -->

Figure 480, "Timestamp – Data Structure for Get Features": Defines the concrete layout or value relationships for Timestamp – Data Structure for Get Features. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is TSTMP, TSTMPS, TSTMPO, SYNC.

- Purpose: Defines the concrete layout or value relationships for Timestamp – Data Structure for Get Features.

- How to read: Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is TSTMP, TSTMPS, TSTMPO, SYNC.

- Conditions and limits: Source keyword index: `should`, `may`, `reserved`. The index locates normative language but does not replace the condition attached to each field. This Figure is a dependency referenced from §5.2.13.1.14; only the elements needed by the requested sections are taught here.

- Informative example: Use TSTMP as the first parser checkpoint and TSTMPS as a second, independent boundary check. This example adds no requirement.

- Source field index: TSTMP, TSTMPS, TSTMPO, SYNC

- Source keyword index: `should`, `may`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.8, Figure 480, printed pages 470-471, PDF pages 496-497

</details>

<details markdown="1">
<summary><strong>Figure 512: Personality Identifier List</strong></summary>

<!-- claim:BASEFWLOG-FIG-512-CLAIM figure-table:BASEFWLOG-FIG-512 -->

Figure 512, "Personality Identifier List": Defines the identifier composition or namespace of values shown by Personality Identifier List. Keep the value width, issuing authority, uniqueness scope, and reserved values separate. Evidence index: Manufacturing Default, Security, Lockdown Persistence, All Personalities.

- Purpose: Defines the identifier composition or namespace of values shown by Personality Identifier List.

- How to read: Keep the value width, issuing authority, uniqueness scope, and reserved values separate. Evidence index: Manufacturing Default, Security, Lockdown Persistence, All Personalities.

- Conditions and limits: Source keyword index: `may`, `reserved`. The index locates normative language but does not replace the condition attached to each field. This Figure is a dependency referenced from §5.2.13.1.28; only the elements needed by the requested sections are taught here.

- Informative example: Parse Manufacturing Default at its defined width, then validate the scope associated with Security before using it as an identity key. This example adds no requirement.

- Source field index: Manufacturing Default, Security, Lockdown Persistence, All Personalities

- Source keyword index: `may`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.25, Figure 512, printed pages 485, PDF pages 511

</details>

<details markdown="1">
<summary><strong>Figure 527: Start Voltage Measurements Data Structure</strong></summary>

<!-- claim:BASEFWLOG-FIG-527-CLAIM figure-table:BASEFWLOG-FIG-527 -->

Figure 527, "Start Voltage Measurements Data Structure": Defines the concrete layout or value relationships for Start Voltage Measurements Data Structure. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is LVOLTA, VMLT, VSSEL, SVMT, LVOLT, LOVT, LUVT, VOLSS.

- Purpose: Defines the concrete layout or value relationships for Start Voltage Measurements Data Structure.

- How to read: Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is LVOLTA, VMLT, VSSEL, SVMT, LVOLT, LOVT, LUVT, VOLSS.

- Conditions and limits: Source keyword index: `shall`, `reserved`. The index locates normative language but does not replace the condition attached to each field. This Figure is a dependency referenced from §5.2.13.1.35; only the elements needed by the requested sections are taught here.

- Informative example: Use LVOLTA as the first parser checkpoint and VMLT as a second, independent boundary check. This example adds no requirement.

- Source field index: LVOLTA, VMLT, VSSEL, SVMT, LVOLT, LOVT, LUVT, VOLSS

- Source keyword index: `shall`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.30, Figure 527, printed pages 502, PDF pages 528

</details>

<details markdown="1">
<summary><strong>Figure 656: Management Operation Specific – Reclaim Unit Handle Update Operation</strong></summary>

<!-- claim:BASEFWLOG-FIG-656-CLAIM figure-table:BASEFWLOG-FIG-656 -->

Figure 656, "Management Operation Specific – Reclaim Unit Handle Update Operation": Defines the operation or state progression represented by Management Operation Specific – Reclaim Unit Handle Update Operation. Follow request, state, transition condition, and completion in order. Evidence index: NPID, MAXPIDS, NRG, NRUH, Placement Identifier.

- Purpose: Defines the operation or state progression represented by Management Operation Specific – Reclaim Unit Handle Update Operation.

- How to read: Follow request, state, transition condition, and completion in order. Evidence index: NPID, MAXPIDS, NRG, NRUH, Placement Identifier.

- Conditions and limits: The Figure is explanatory or structural; this guide does not turn its visual relationship into a new requirement. This Figure is a dependency referenced from §5.2.13.1.29; only the elements needed by the requested sections are taught here.

- Informative example: Begin with NPID, move to the state associated with MAXPIDS only when the cited transition condition is satisfied. This example adds no requirement.

- Source field index: NPID, MAXPIDS, NRG, NRUH, Placement Identifier

- Source keyword index: none

> Source: NVME-BASE-2.4, Rev. 2.4, §7.4.1, Figure 656, printed pages 570, PDF pages 596

</details>

<details markdown="1">
<summary><strong>Figure 745: Power Measurement Types</strong></summary>

<!-- claim:BASEFWLOG-FIG-745-CLAIM figure-table:BASEFWLOG-FIG-745 -->

Figure 745, "Power Measurement Types": Defines the enumerated values, measurement scale, or sensor selection represented by Power Measurement Types. Resolve the selector or code first, then apply its unit, scale, or reserved-value rule. Evidence index: 0h, NVM subsystem total power, CSTS.SHST.

- Purpose: Defines the enumerated values, measurement scale, or sensor selection represented by Power Measurement Types.

- How to read: Resolve the selector or code first, then apply its unit, scale, or reserved-value rule. Evidence index: 0h, NVM subsystem total power, CSTS.SHST.

- Conditions and limits: Source keyword index: `may`, `reserved`. The index locates normative language but does not replace the condition attached to each field. This Figure is a dependency referenced from §5.2.13.1.34; only the elements needed by the requested sections are taught here.

- Informative example: Decode 0h, then apply the interpretation selected by NVM subsystem total power; do not assign meaning to a reserved value. This example adds no requirement.

- Source field index: 0h, NVM subsystem total power, CSTS.SHST

- Source keyword index: `may`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §8.1.20, Figure 745, printed pages 678, PDF pages 704

</details>

<details markdown="1">
<summary><strong>Figure 746: Power Measurement and Reporting Capabilities</strong></summary>

<!-- claim:BASEFWLOG-FIG-746-CLAIM figure-table:BASEFWLOG-FIG-746 -->

Figure 746, "Power Measurement and Reporting Capabilities": Defines the concrete layout or value relationships for Power Measurement and Reporting Capabilities. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is IPM, SMART, OLEC.

- Purpose: Defines the concrete layout or value relationships for Power Measurement and Reporting Capabilities.

- How to read: Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is IPM, SMART, OLEC.

- Conditions and limits: Source keyword index: `shall`. The index locates normative language but does not replace the condition attached to each field. This Figure is a dependency referenced from §5.2.13.1.34; only the elements needed by the requested sections are taught here.

- Informative example: Use IPM as the first parser checkpoint and SMART as a second, independent boundary check. This example adds no requirement.

- Source field index: IPM, SMART, OLEC

- Source keyword index: `shall`

> Source: NVME-BASE-2.4, Rev. 2.4, §8.1.20, Figure 746, printed pages 678, PDF pages 704

</details>

<details markdown="1">
<summary><strong>Figure 747: Power Scale</strong></summary>

<!-- claim:BASEFWLOG-FIG-747-CLAIM figure-table:BASEFWLOG-FIG-747 -->

Figure 747, "Power Scale": Defines the enumerated values, measurement scale, or sensor selection represented by Power Scale. Resolve the selector or code first, then apply its unit, scale, or reserved-value rule. Evidence index: 01b = 0.0001 W, 10b = 0.01 W.

- Purpose: Defines the enumerated values, measurement scale, or sensor selection represented by Power Scale.

- How to read: Resolve the selector or code first, then apply its unit, scale, or reserved-value rule. Evidence index: 01b = 0.0001 W, 10b = 0.01 W.

- Conditions and limits: The Figure is explanatory or structural; this guide does not turn its visual relationship into a new requirement. This Figure is a dependency referenced from §5.2.13.1.34; only the elements needed by the requested sections are taught here.

- Informative example: Decode 01b = 0.0001 W, then apply the interpretation selected by 10b = 0.01 W; do not assign meaning to a reserved value. This example adds no requirement.

- Source field index: 01b = 0.0001 W, 10b = 0.01 W

- Source keyword index: none

> Source: NVME-BASE-2.4, Rev. 2.4, §8.1.20, Figure 747, printed pages 679, PDF pages 705

</details>

<details markdown="1">
<summary><strong>Figure 772: Sanitize Operation State Machine</strong></summary>

<!-- claim:BASEFWLOG-FIG-772-CLAIM figure-table:BASEFWLOG-FIG-772 -->

Figure 772, "Sanitize Operation State Machine": Defines the operation or state progression represented by Sanitize Operation State Machine. Follow request, state, transition condition, and completion in order. Evidence index: SANS, Idle, Restricted Processing, Unrestricted Processing, Media Verification.

- Purpose: Defines the operation or state progression represented by Sanitize Operation State Machine.

- How to read: Follow request, state, transition condition, and completion in order. Evidence index: SANS, Idle, Restricted Processing, Unrestricted Processing, Media Verification.

- Conditions and limits: The Figure is explanatory or structural; this guide does not turn its visual relationship into a new requirement. This Figure is a dependency referenced from §5.2.13.1.38; only the elements needed by the requested sections are taught here.

- Informative example: Begin with SANS, move to the state associated with Idle only when the cited transition condition is satisfied. This example adds no requirement.

- Source field index: SANS, Idle, Restricted Processing, Unrestricted Processing, Media Verification

- Source keyword index: none

> Source: NVME-BASE-2.4, Rev. 2.4, §8.1.27.4, Figure 772, printed pages 720, PDF pages 746

</details>

<details markdown="1">
<summary><strong>Figure 782: UUID Index Field</strong></summary>

<!-- claim:BASEFWLOG-FIG-782-CLAIM figure-table:BASEFWLOG-FIG-782 -->

Figure 782, "UUID Index Field": Defines the concrete layout or value relationships for UUID Index Field. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is UIDX, UUID.

- Purpose: Defines the concrete layout or value relationships for UUID Index Field.

- How to read: Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is UIDX, UUID.

- Conditions and limits: Source keyword index: `shall`. The index locates normative language but does not replace the condition attached to each field. This Figure is a dependency referenced from §5.2.13; only the elements needed by the requested sections are taught here.

- Informative example: Use UIDX as the first parser checkpoint and UUID as a second, independent boundary check. This example adds no requirement.

- Source field index: UIDX, UUID

- Source keyword index: `shall`

> Source: NVME-BASE-2.4, Rev. 2.4, §8.1.31.2, Figure 782, printed pages 738, PDF pages 764

</details>

<details markdown="1">
<summary><strong>Figure 783: Voltage Sensors</strong></summary>

<!-- claim:BASEFWLOG-FIG-783-CLAIM figure-table:BASEFWLOG-FIG-783 -->

Figure 783, "Voltage Sensors": Defines the enumerated values, measurement scale, or sensor selection represented by Voltage Sensors. Resolve the selector or code first, then apply its unit, scale, or reserved-value rule. Evidence index: VSEN1, VSEN2, VSEN3, VSEN4.

- Purpose: Defines the enumerated values, measurement scale, or sensor selection represented by Voltage Sensors.

- How to read: Resolve the selector or code first, then apply its unit, scale, or reserved-value rule. Evidence index: VSEN1, VSEN2, VSEN3, VSEN4.

- Conditions and limits: The Figure is explanatory or structural; this guide does not turn its visual relationship into a new requirement. This Figure is a dependency referenced from §5.2.13.1.35; only the elements needed by the requested sections are taught here.

- Informative example: Decode VSEN1, then apply the interpretation selected by VSEN2; do not assign meaning to a reserved value. This example adds no requirement.

- Source field index: VSEN1, VSEN2, VSEN3, VSEN4

- Source keyword index: none

> Source: NVME-BASE-2.4, Rev. 2.4, §8.1.32, Figure 783, printed pages 740, PDF pages 766

</details>

## Use and limitations

Use the claim IDs as stable PPT traceability keys. Re-check affected claims if the source revision, errata set, or approved scope changes.
