---
layout: post
read_time: true
show_date: true
title: "NVMe Base 2.4: Firmware Update and LID 03h Verification"
date: 2026-09-01
description: "A source-located engineering tutorial from firmware download through LID 03h verification."
lang: en
img: posts/2026/cat_title.jpg
tags: [NVMe, PCIe, Specification]
category: NVMe
author: Jia-Chang
github: JiaChangGit/JiaChangGit.github.io/tree/main/DOCS/nvme-spec-report
toc: yes
---

# NVMe Base 2.4: Firmware Update and LID 03h Verification

This tutorial builds an end-to-end engineering model: capability readout, image download, commit and activation, reset boundaries, and verification with Firmware Slot Information (LID 03h).

## Scope and source semantics

Scope: §3.11, §3.11.1, §5.2.9, §5.2.10, the minimum common §5.2.13 fields needed for LID 03h, and §5.2.13.1.4; main printed pages 135-138, 202-206, 212-216, and 225-226, plus the minimum dependency slice.

NVM Express Base Specification, Revision 2.4

NVM Express NVMe over PCIe Transport Specification, Revision 1.4 — §3.3 reset terminology only

Excluded: every other LID, unapproved transport-specific material, NVM Command Set 1.3, and the full Boot Partition feature flow. BPID and CA=110b/111b remain only as cross-references.

`shall` is mandatory, `should` is a preferred recommendation, `may` permits a choice, and `reserved` is not assigned an invented meaning. `[SPEC]` is a source-faithful paraphrase; `[Explanation]`, `[Inference]`, and `[Informative example]` add no requirement.

## Mental Model

```text
Downloaded portions -> committed slot -> current / next active image -> Identify.FR + LID 03h
```

## PART 1 — Mental Model: Images, Slots, and Domains

**[Explanation]** A firmware update is not an immediate file replacement. Track four distinct states: downloaded image data, an image stored in a slot, the currently executing image, and an image scheduled for activation at a later reset.

### Start with the firmware-sharing boundary

<!-- claim:BASEFWLOG-MODEL-DOMAIN -->

**[SPEC]** Controllers in one domain share firmware slots, and the same firmware image is applied to all controllers in that domain. If multiple domains are not supported, that scope is the entire NVM subsystem.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.9, printed pages 202, PDF pages 228

### FR: currently active revision

<!-- claim:BASEFWLOG-CAP-FR -->

**[SPEC]** Identify Controller FR is the eight-byte ASCII string for the currently active firmware revision in the controller's domain. It is the same revision information available from LID 03h.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.14.1, printed pages 340, PDF pages 366

### MDS and ULIST

<!-- claim:BASEFWLOG-CAP-MDS-ULIST -->

**[SPEC]** CTRATT.MDS determines whether LID 03h returns domain-scoped or NVM-subsystem-scoped information, while CTRATT.ULIST indicates UUID List reporting support.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.14.1, printed pages 346, PDF pages 372

### FRMW: slot and activation capabilities

<!-- claim:BASEFWLOG-CAP-FRMW -->

**[SPEC]** FRMW.SMUD, FAWR, NOFS, and FFSRO describe overlapping-update detection, activation without reset, the domain's supported slot count (1 through 7), and whether slot 1 is read-only.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.14.1, printed pages 354, PDF pages 380

### MTFA: command-processing pause

<!-- claim:BASEFWLOG-CAP-MTFA -->

**[SPEC]** MTFA is in 100 ms units and reports the maximum time command processing is temporarily stopped during activation. It shall be valid when activation without reset is supported; 0h means the maximum is undefined.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.14.1, printed pages 357, PDF pages 383

### FWUG: download granularity and alignment

<!-- claim:BASEFWLOG-CAP-FWUG -->

**[SPEC]** FWUG constrains NUMD and OFST granularity/alignment in 4 KiB units: 1h is 4 KiB, 2h is 8 KiB, 0h reports no information, and FFh permits any dword granularity and alignment. A controller may return Invalid Field in Command for a violation.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.14.1, printed pages 359, PDF pages 385

### MPTFAWR: immediate-activation completion time

<!-- claim:BASEFWLOG-CAP-MPTFAWR -->

**[SPEC]** MPTFAWR is a 100 ms-unit estimate of the maximum processing time to complete Firmware Commit with CA=011b, including time to commit the image to a slot. It shall be 0h when activation without reset is unsupported.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.14.1, printed pages 364, PDF pages 390

**[Inference]** Use the domain as the firmware-state sharing key. Recording only a PCI Function or controller ID can incorrectly turn one shared slot set into several apparently independent firmware stores.

## PART 2 — Build the Download Sequence: Portions, Alignment, Invalidation

**[Explanation]** An image may be transferred in portions, but the controller sees dword ranges rather than a filename or byte-oriented file offset. Every portion must satisfy buffer, zero-based length, image-relative offset, and FWUG constraints together.

### Plan update sequences as serialized work

<!-- claim:BASEFWLOG-FW-SEQUENCE -->

**[SPEC]** The host should not overlap firmware or Boot Partition update sequences and should use only one controller or Management Endpoint throughout a sequence. SMUD and MUD are detection/reporting capabilities, not permission to overlap sequences.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.11, printed pages 137, PDF pages 163

### Portion ordering, overlap, and FWUG

<!-- claim:BASEFWLOG-DOWNLOAD-RANGE -->

**[SPEC]** Firmware Image Download may split an image into portions, and firmware-image portions may arrive out of order. The host should avoid overlapping ranges and comply with FWUG. Boot Partition portions shall be submitted in order.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.10, printed pages 205-206, PDF pages 231-232

### DPTR, NUMD, OFST, and actual bytes

<!-- claim:BASEFWLOG-DOWNLOAD-FIELDS -->

**[SPEC]** DPTR points to the source buffer. NUMD is a zero-based dword count, so bytes=(NUMD+1)×4; OFST is a dword offset from the image start, so byte offset=OFST×4. The portion containing the image start shall use OFST=0h.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.10, printed pages 205-206, PDF pages 231-232

### When downloaded portions are discarded

<!-- claim:BASEFWLOG-FW-DISCARD -->

**[SPEC]** The first Firmware Image Download after Firmware Commit completes, and a Controller Level Reset after download but before Firmware Commit completion, shall cause the controller to discard remaining downloaded portions.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.11, 5.2.10, printed pages 137, 205-206, PDF pages 163, 231-232

**[Inference]** A driver should detect overlap on byte intervals before converting to NUMD and OFST. Performing interval checks only after zero-based encoding makes off-by-one defects much more likely.

## PART 3 — Commit and Activation: CA Selects the State Transition

**[Explanation]** Firmware Commit combines validation, slot placement, and activation policy. The key question is not merely whether the command succeeded, but which slot now holds the image, whether it is active, and which reset—if any—still remains.

### What Firmware Commit actually does

<!-- claim:BASEFWLOG-COMMIT-PURPOSE -->

**[SPEC]** Firmware Commit validates the last downloaded image, places it in a firmware slot, and uses Commit Action to choose placement only, activation at a later Controller Level Reset, or immediate activation. Successful commit does not by itself mean the image is currently active.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.9, printed pages 202-203, PDF pages 228-229

### CA and FS decision matrix

<!-- claim:BASEFWLOG-COMMIT-CDW10 -->

**[SPEC]** CDW10[5:3] is CA and CDW10[2:0] is FS. CA 000b places only, 001b places and schedules activation at the next CLR, 010b schedules an existing slot, and 011b activates immediately. With FS=0h, the controller shall choose a slot from 1 through 7.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.9, printed pages 203, PDF pages 229

### Boot Partition cross-reference boundary

<!-- claim:BASEFWLOG-COMMIT-BOOT -->

**[SPEC]** BPID and CA=110b/111b belong to Boot Partition handling: 110b replaces the selected partition, 111b marks it active, and Boot Partition Write Prohibited is one of the Firmware Commit command-specific status values.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.9, printed pages 203-205, PDF pages 229-231

### MUD: evidence of overlapping sequences

<!-- claim:BASEFWLOG-COMMIT-MUD -->

**[SPEC]** Firmware Commit CQE.DW0[1:0] MUD reports overlap detected through a Management Endpoint and an Admin Submission Queue. If FRMW.SMUD is 0, MUD shall be 00b; MUD is valid whether the command succeeds or is aborted.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.9, printed pages 204, PDF pages 230

### Status selects the next recovery action

<!-- claim:BASEFWLOG-COMMIT-STATUS -->

**[SPEC]** Firmware Commit command-specific status distinguishes invalid slot/image, required Conventional/NVM Subsystem/Controller Level Reset, MTFA violation, activation prohibited, overlapping range, Boot Partition write prohibition, and personality incompatibility.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.9, printed pages 204-205, PDF pages 230-231

### Complete reset-based flow

<!-- claim:BASEFWLOG-FW-RESET -->

**[SPEC]** The reset-based flow is one or more Firmware Image Download commands, Firmware Commit to validate and place the image, a Controller Level Reset capable of causing activation, and reinitialization of the controller and I/O queues.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.11, printed pages 135-136, PDF pages 161-162

### Immediate activation is not background work

<!-- claim:BASEFWLOG-FW-IMMEDIATE -->

**[SPEC]** CA=011b requests immediate activation. Firmware Commit is not a background operation and remains in progress until activation succeeds or fails. If Firmware Activation notices are enabled, an affected controller may send Firmware Activation Starting.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.11, printed pages 136, PDF pages 162

### Load failure and fallback

<!-- claim:BASEFWLOG-FW-FAILURE -->

**[SPEC]** If the new image cannot be loaded, the controller shall revert to the image in the most recently activated slot; if that image also cannot be loaded, it loads an available baseline read-only image and generates Firmware Image Load Error.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.11, printed pages 136-137, PDF pages 162-163

### Do not conflate PCIe reset names

<!-- claim:BASEFWLOG-RESET-XREF -->

**[SPEC]** Conventional Reset and Function Level Reset are PCIe-specific Controller Level Reset methods defined by NVMe over PCIe Transport. When Firmware Commit status names one of them, select the reset under Transport §3.3; FLR and Conventional Reset are not interchangeable.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.3, printed pages 11, PDF pages 11

### UUID List positional stability

<!-- claim:BASEFWLOG-UUID-LIST -->

**[SPEC]** Across firmware revisions, UUID List entry positions should remain stable: new UUIDs should be appended, a removed UUID should be replaced in place with the NVMe Invalid UUID, an invalid entry should not be reused, and the list should not be shortened or removed.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.11.1, printed pages 137-138, PDF pages 163-164

### Reset boundary caused by UUID changes

<!-- claim:BASEFWLOG-UUID-RESET -->

**[SPEC]** If a downloaded image replaces the NVMe Invalid UUID or a different valid UUID with a valid UUID in an existing entry, the controller shall require reset, and all controllers affected by that UUID List change shall be reset.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.11.1, printed pages 138, PDF pages 164

### Figure 337/338 cross-reference discrepancy

<!-- claim:BASEFWLOG-XREF-337 -->

**[SPEC]** Source §5.2.9 points Firmware Revision to Figure 337, but Figure 337 contains Command Set Identifiers and FR appears in Figure 338. Without separately approved errata, this report preserves and discloses the internal source discrepancy instead of silently rewriting it.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.9, 5.2.14.1, printed pages 202, 340, PDF pages 228, 366

**[Inference]** Recovery logic should branch on the complete SCT/SC rather than a success/failure boolean. When status requires Conventional Reset, substituting FLR does not satisfy the indicated activation boundary.

## PART 4 — Verify with LID 03h: From Command to the 512-Byte Layout

**[Explanation]** LID 03h is the observation surface for the firmware workflow. AFI reports current and next active slots, while FRS1-FRS7 report stored revisions. It does not replace Firmware Commit completion or choose the required reset for the host.

### Minimum command slice for LID 03h

<!-- claim:BASEFWLOG-LOG-COMMAND -->

**[SPEC]** Reading LID 03h needs only the required DPTR and CDW10-CDW14 slice: LID=03h, LSP=0, RAE=0, NUMDL/NUMDU for 512 bytes, LSI=0, LPOL/LPOU=0, OT=0, and UIDX=0. LID 03h does not use CSI, which the controller ignores under Figure 208's rule.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13, printed pages 212-215, PDF pages 238-241

### Concrete command calculation for 512 bytes

<!-- claim:BASEFWLOG-LOG-LENGTH -->

**[SPEC]** NUMDL and NUMDU form a zero-based dword count. LID 03h is 512 bytes, or 128 dwords, so NUMD=127=0000007Fh, NUMDL=007Fh, and NUMDU=0000h. With LSP=0 and RAE=0, CDW10=007F0003h.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13, printed pages 213-215, PDF pages 239-241

### RAE event side effect

<!-- claim:BASEFWLOG-LOG-RAE -->

**[SPEC]** RAE=0 clears the corresponding asynchronous event on successful completion, while RAE=1 retains it. If the command fails, the controller shall retain the event. Firmware Activation Starting is cleared by reading LID 03h with RAE=0.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.2, 5.2.13, printed pages 186, 213, PDF pages 212, 239

### Full-read and offset boundary

<!-- claim:BASEFWLOG-LOG-OFFSET -->

**[SPEC]** This report uses the complete 512-byte LID 03h with LPOL=LPOU=0 and OT=0. A general byte offset is dword aligned, and an offset beyond the log page shall return Invalid Field in Command. LID 03h needs no index-offset branch.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13, printed pages 214-215, PDF pages 240-241

### Domain/subsystem scope of LID 03h

<!-- claim:BASEFWLOG-LOG-SCOPE -->

**[SPEC]** The LID 03h row in Figure 209 specifies CSI=N, scope=Domain/NVM subsystem, and reference §5.2.13.1.4. With MDS=1, the data is for the domain containing the controller that processed the command; otherwise it is for the NVM subsystem.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13, printed pages 215-216, PDF pages 241-242

### What LID 03h answers

<!-- claim:BASEFWLOG-LID03-DESCRIPTION -->

**[SPEC]** The 512-byte Firmware Slot Information log page reports the firmware revision stored in each supported slot and identifies the current active slot plus the next active slot when reported. Revisions are ASCII strings.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.4, printed pages 225-226, PDF pages 251-252

### AFI: current and next active slots

<!-- claim:BASEFWLOG-LID03-AFI -->

**[SPEC]** In AFI byte 0, NAFS is bits 6:4 and CAFS is bits 2:0; bits 7 and 3 are reserved. Nonzero NAFS identifies the slot to activate at the next CLR capable of causing activation; NAFS=0 means no next slot is indicated. CAFS identifies the source slot of the running image.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.4, printed pages 226, PDF pages 252

### FRS1-FRS7 and reserved regions

<!-- claim:BASEFWLOG-LID03-FRS -->

**[SPEC]** FRS1 through FRS7 occupy bytes 8-63, eight bytes per slot. If a slot has no valid revision or is unsupported, its FRS shall be cleared to 0h. Bytes 1-7 and 64-511 are reserved and are not additional slots.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.4, printed pages 226, PDF pages 252

**[Inference]** Verification should compare Identify.FR, LID 03h CAFS, and the corresponding FRSx together. Comparing only the ASCII revision loses slot identity when two slots happen to contain the same string.

## End-to-End Example

**[Informative example]** Assume NOFS=3, FFSRO=1, FWUG=1h, and CAFS=1. Use writable slot 2. Split 12 KiB into three 4 KiB portions. Each portion is 1024 dwords, so NUMD=1023=000003FFh; OFST values are 00000000h, 00000400h, and 00000800h. Commit with CA=001b and FS=010b, giving CDW10=0000000Ah. Before reset, read all 512 bytes of LID 03h with NUMD=127 and CDW10=007F0003h. AFI=21h decodes to NAFS=2 and CAFS=1. Perform the required reset, reinitialize, then verify CAFS=2 together with FRS2 and Identify.FR.

## Debug Decision Flow

| Symptom | First evidence | Likely mistake | Next action |
|---|---|---|---|
| Download Invalid Field | NUMD, OFST, FWUG | NUMD treated as a direct count | Recompute byte intervals |
| Invalid Firmware Slot | NOFS, FFSRO, FS | Slot 1 assumed writable | Select a supported writable slot |
| Reset-required status | Full SCT/SC | All resets treated as equal | Follow status and PCIe §3.3 |
| LID 03h unchanged | MDS/DID, controller, AFI | Slots assumed per controller | Verify within the same domain |
| FRSx is zero | NOFS, slot validity, buffer offset | Zero treated as an empty revision string | Treat as unsupported/no valid revision |

## Appendix A — Supporting Figure / Field Reference

Figures are traceable evidence for the workflow, not the article outline. Dependency entries expose only the required slice; Figure 209 is limited to the LID 03h row.

<details markdown="1">
<summary><strong>Figure 187: Firmware Commit – Command Dword 10</strong> — main-scope evidence</summary>

<!-- claim:BASEFWLOG-FIG-187-CLAIM figure-table:BASEFWLOG-FIG-187 -->

**[SPEC]** Figure 187, "Firmware Commit – Command Dword 10": Defines the concrete layout or value relationships for Firmware Commit – Command Dword 10. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is BPID, CA, FS.

**[Explanation]** Defines the concrete layout or value relationships for Firmware Commit – Command Dword 10. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is BPID, CA, FS.

Source field index: BPID, CA, FS

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.9, Figure 187, printed pages 203, PDF pages 229

</details>

<details markdown="1">
<summary><strong>Figure 188: Firmware Commit – Completion Queue Entry Dword 0</strong> — main-scope evidence</summary>

<!-- claim:BASEFWLOG-FIG-188-CLAIM figure-table:BASEFWLOG-FIG-188 -->

**[SPEC]** Figure 188, "Firmware Commit – Completion Queue Entry Dword 0": Shows the queue or command relationship expressed by Firmware Commit – Completion Queue Entry Dword 0. Trace ownership and direction from host to SQ, controller, and CQ; keep the indexed elements distinct: MUD, MEFWO, ASQFWO.

**[Explanation]** Shows the queue or command relationship expressed by Firmware Commit – Completion Queue Entry Dword 0. Trace ownership and direction from host to SQ, controller, and CQ; keep the indexed elements distinct: MUD, MEFWO, ASQFWO.

Source field index: MUD, MEFWO, ASQFWO

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.9.1, Figure 188, printed pages 204, PDF pages 230

</details>

<details markdown="1">
<summary><strong>Figure 189: Firmware Commit – Command Specific Status Values</strong> — main-scope evidence</summary>

<!-- claim:BASEFWLOG-FIG-189-CLAIM figure-table:BASEFWLOG-FIG-189 -->

**[SPEC]** Figure 189, "Firmware Commit – Command Specific Status Values": Defines the concrete layout or value relationships for Firmware Commit – Command Specific Status Values. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is Invalid Firmware Slot, Invalid Firmware Image, reset-required status, MTFA, Overlapping Range.

**[Explanation]** Defines the concrete layout or value relationships for Firmware Commit – Command Specific Status Values. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is Invalid Firmware Slot, Invalid Firmware Image, reset-required status, MTFA, Overlapping Range.

Source field index: Invalid Firmware Slot, Invalid Firmware Image, reset-required status, MTFA, Overlapping Range

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.9.1, Figure 189, printed pages 204-205, PDF pages 230-231

</details>

<details markdown="1">
<summary><strong>Figure 190: Firmware Image Download – Data Pointer</strong> — main-scope evidence</summary>

<!-- claim:BASEFWLOG-FIG-190-CLAIM figure-table:BASEFWLOG-FIG-190 -->

**[SPEC]** Figure 190, "Firmware Image Download – Data Pointer": Defines how Firmware Image Download – Data Pointer identifies the destination or source buffer for this command. Resolve pointer type and address before checking transfer length and alignment. Evidence index: DPTR.

**[Explanation]** Defines how Firmware Image Download – Data Pointer identifies the destination or source buffer for this command. Resolve pointer type and address before checking transfer length and alignment. Evidence index: DPTR.

Source field index: DPTR

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.10, Figure 190, printed pages 205, PDF pages 231

</details>

<details markdown="1">
<summary><strong>Figure 191: Firmware Image Download – Command Dword 10</strong> — main-scope evidence</summary>

<!-- claim:BASEFWLOG-FIG-191-CLAIM figure-table:BASEFWLOG-FIG-191 -->

**[SPEC]** Figure 191, "Firmware Image Download – Command Dword 10": Defines the concrete layout or value relationships for Firmware Image Download – Command Dword 10. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is NUMD, FWUG.

**[Explanation]** Defines the concrete layout or value relationships for Firmware Image Download – Command Dword 10. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is NUMD, FWUG.

Source field index: NUMD, FWUG

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.10, Figure 191, printed pages 205, PDF pages 231

</details>

<details markdown="1">
<summary><strong>Figure 192: Firmware Image Download – Command Dword 11</strong> — main-scope evidence</summary>

<!-- claim:BASEFWLOG-FIG-192-CLAIM figure-table:BASEFWLOG-FIG-192 -->

**[SPEC]** Figure 192, "Firmware Image Download – Command Dword 11": Defines the concrete layout or value relationships for Firmware Image Download – Command Dword 11. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is OFST, FWUG.

**[Explanation]** Defines the concrete layout or value relationships for Firmware Image Download – Command Dword 11. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is OFST, FWUG.

Source field index: OFST, FWUG

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.10, Figure 192, printed pages 206, PDF pages 232

</details>

<details markdown="1">
<summary><strong>Figure 193: Firmware Image Download – Command Specific Status Values</strong> — main-scope evidence</summary>

<!-- claim:BASEFWLOG-FIG-193-CLAIM figure-table:BASEFWLOG-FIG-193 -->

**[SPEC]** Figure 193, "Firmware Image Download – Command Specific Status Values": Defines the concrete layout or value relationships for Firmware Image Download – Command Specific Status Values. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is Overlapping Range.

**[Explanation]** Defines the concrete layout or value relationships for Firmware Image Download – Command Specific Status Values. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is Overlapping Range.

Source field index: Overlapping Range

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.10, Figure 193, printed pages 206, PDF pages 232

</details>

<details markdown="1">
<summary><strong>Figure 203: Get Log Page – Data Pointer</strong> — main-scope evidence</summary>

<!-- claim:BASEFWLOG-FIG-203-CLAIM figure-table:BASEFWLOG-FIG-203 -->

**[SPEC]** Figure 203, "Get Log Page – Data Pointer": Defines how Get Log Page – Data Pointer identifies the destination or source buffer for this command. Resolve pointer type and address before checking transfer length and alignment. Evidence index: DPTR.

**[Explanation]** Defines how Get Log Page – Data Pointer identifies the destination or source buffer for this command. Resolve pointer type and address before checking transfer length and alignment. Evidence index: DPTR.

Source field index: DPTR

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13, Figure 203, printed pages 213, PDF pages 239

</details>

<details markdown="1">
<summary><strong>Figure 204: Get Log Page – Command Dword 10</strong> — main-scope evidence</summary>

<!-- claim:BASEFWLOG-FIG-204-CLAIM figure-table:BASEFWLOG-FIG-204 -->

**[SPEC]** Figure 204, "Get Log Page – Command Dword 10": Defines the returned log-page layout and selection context for Get Log Page – Command Dword 10. Start with the fixed header and scope, validate counts or lengths, then walk entries or data areas in order. Evidence index: NUMDL, RAE, LSP, LID.

**[Explanation]** Defines the returned log-page layout and selection context for Get Log Page – Command Dword 10. Start with the fixed header and scope, validate counts or lengths, then walk entries or data areas in order. Evidence index: NUMDL, RAE, LSP, LID.

Source field index: NUMDL, RAE, LSP, LID

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13, Figure 204, printed pages 213, PDF pages 239

</details>

<details markdown="1">
<summary><strong>Figure 205: Get Log Page – Command Dword 11</strong> — main-scope evidence</summary>

<!-- claim:BASEFWLOG-FIG-205-CLAIM figure-table:BASEFWLOG-FIG-205 -->

**[SPEC]** Figure 205, "Get Log Page – Command Dword 11": Defines the returned log-page layout and selection context for Get Log Page – Command Dword 11. Start with the fixed header and scope, validate counts or lengths, then walk entries or data areas in order. Evidence index: LSI, NUMDU.

**[Explanation]** Defines the returned log-page layout and selection context for Get Log Page – Command Dword 11. Start with the fixed header and scope, validate counts or lengths, then walk entries or data areas in order. Evidence index: LSI, NUMDU.

Source field index: LSI, NUMDU

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13, Figure 205, printed pages 214, PDF pages 240

</details>

<details markdown="1">
<summary><strong>Figure 206: Get Log Page – Command Dword 12</strong> — main-scope evidence</summary>

<!-- claim:BASEFWLOG-FIG-206-CLAIM figure-table:BASEFWLOG-FIG-206 -->

**[SPEC]** Figure 206, "Get Log Page – Command Dword 12": Defines the returned log-page layout and selection context for Get Log Page – Command Dword 12. Start with the fixed header and scope, validate counts or lengths, then walk entries or data areas in order. Evidence index: LPOL, OT.

**[Explanation]** Defines the returned log-page layout and selection context for Get Log Page – Command Dword 12. Start with the fixed header and scope, validate counts or lengths, then walk entries or data areas in order. Evidence index: LPOL, OT.

Source field index: LPOL, OT

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13, Figure 206, printed pages 214, PDF pages 240

</details>

<details markdown="1">
<summary><strong>Figure 207: Get Log Page – Command Dword 13</strong> — main-scope evidence</summary>

<!-- claim:BASEFWLOG-FIG-207-CLAIM figure-table:BASEFWLOG-FIG-207 -->

**[SPEC]** Figure 207, "Get Log Page – Command Dword 13": Defines the returned log-page layout and selection context for Get Log Page – Command Dword 13. Start with the fixed header and scope, validate counts or lengths, then walk entries or data areas in order. Evidence index: LPOU.

**[Explanation]** Defines the returned log-page layout and selection context for Get Log Page – Command Dword 13. Start with the fixed header and scope, validate counts or lengths, then walk entries or data areas in order. Evidence index: LPOU.

Source field index: LPOU

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13, Figure 207, printed pages 214, PDF pages 240

</details>

<details markdown="1">
<summary><strong>Figure 208: Get Log Page – Command Dword 14</strong> — main-scope evidence</summary>

<!-- claim:BASEFWLOG-FIG-208-CLAIM figure-table:BASEFWLOG-FIG-208 -->

**[SPEC]** Figure 208, "Get Log Page – Command Dword 14": Defines the returned log-page layout and selection context for Get Log Page – Command Dword 14. Start with the fixed header and scope, validate counts or lengths, then walk entries or data areas in order. Evidence index: CSI, OT, UIDX.

**[Explanation]** Defines the returned log-page layout and selection context for Get Log Page – Command Dword 14. Start with the fixed header and scope, validate counts or lengths, then walk entries or data areas in order. Evidence index: CSI, OT, UIDX.

Source field index: CSI, OT, UIDX

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13, Figure 208, printed pages 214-215, PDF pages 240-241

</details>

<details markdown="1">
<summary><strong>Figure 209: Get Log Page – Log Page Identifiers</strong> — main-scope evidence</summary>

<!-- claim:BASEFWLOG-FIG-209-CLAIM figure-table:BASEFWLOG-FIG-209 -->

**[SPEC]** Figure 209, "Get Log Page – Log Page Identifiers": Defines the returned log-page layout and selection context for Get Log Page – Log Page Identifiers. Start with the fixed header and scope, validate counts or lengths, then walk entries or data areas in order. Evidence index: LID 03h, CSI = N, Domain / NVM subsystem, Firmware Slot Information, §5.2.13.1.4, MDS.

**[Explanation]** Defines the returned log-page layout and selection context for Get Log Page – Log Page Identifiers. Start with the fixed header and scope, validate counts or lengths, then walk entries or data areas in order. Evidence index: LID 03h, CSI = N, Domain / NVM subsystem, Firmware Slot Information, §5.2.13.1.4, MDS.

Source field index: LID 03h, CSI = N, Domain / NVM subsystem, Firmware Slot Information, §5.2.13.1.4, MDS

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13, Figure 209, printed pages 215-216, PDF pages 241-242

</details>

<details markdown="1">
<summary><strong>Figure 215: Firmware Slot Information Log Page</strong> — main-scope evidence</summary>

<!-- claim:BASEFWLOG-FIG-215-CLAIM figure-table:BASEFWLOG-FIG-215 -->

**[SPEC]** Figure 215, "Firmware Slot Information Log Page": Defines the returned log-page layout and selection context for Firmware Slot Information Log Page. Start with the fixed header and scope, validate counts or lengths, then walk entries or data areas in order. Evidence index: AFI, NAFS, CAFS, FRS1, FRS2, FRS3, FRS4, FRS5, FRS6, FRS7, Reserved bytes 1:7 and 64:511.

**[Explanation]** Defines the returned log-page layout and selection context for Firmware Slot Information Log Page. Start with the fixed header and scope, validate counts or lengths, then walk entries or data areas in order. Evidence index: AFI, NAFS, CAFS, FRS1, FRS2, FRS3, FRS4, FRS5, FRS6, FRS7, Reserved bytes 1:7 and 64:511.

Source field index: AFI, NAFS, CAFS, FRS1, FRS2, FRS3, FRS4, FRS5, FRS6, FRS7, Reserved bytes 1:7 and 64:511

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.4, Figure 215, printed pages 226, PDF pages 252

</details>

<details markdown="1">
<summary><strong>Figure 93: Common Command Format</strong> — minimum dependency slice</summary>

<!-- claim:BASEFWLOG-FIG-093-CLAIM figure-table:BASEFWLOG-FIG-093 -->

**[SPEC]** Figure 93, "Common Command Format": Defines the concrete layout or value relationships for Common Command Format. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is DPTR, PRP1, PRP2, SGL1.

**[Explanation]** Defines the concrete layout or value relationships for Common Command Format. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is DPTR, PRP1, PRP2, SGL1.

Source field index: DPTR, PRP1, PRP2, SGL1

> Source: NVME-BASE-2.4, Rev. 2.4, §4.1.1, Figure 93, printed pages 140-142, PDF pages 166-168

</details>

<details markdown="1">
<summary><strong>Figure 155: Asynchronous Event Information – Notice</strong> — minimum dependency slice</summary>

<!-- claim:BASEFWLOG-FIG-155-CLAIM figure-table:BASEFWLOG-FIG-155 -->

**[SPEC]** Figure 155, "Asynchronous Event Information – Notice": Defines the event record, event taxonomy, or logging condition represented by Asynchronous Event Information – Notice. Resolve event type and record length before decoding event-specific data. Evidence index: Firmware Activation Starting, CSTS.PP, Firmware Slot Information, RAE.

**[Explanation]** Defines the event record, event taxonomy, or logging condition represented by Asynchronous Event Information – Notice. Resolve event type and record length before decoding event-specific data. Evidence index: Firmware Activation Starting, CSTS.PP, Firmware Slot Information, RAE.

Source field index: Firmware Activation Starting, CSTS.PP, Firmware Slot Information, RAE

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.2.1, Figure 155, printed pages 186, PDF pages 212

</details>

<details markdown="1">
<summary><strong>Figure 337: Command Set Identifiers</strong> — minimum dependency slice</summary>

<!-- claim:BASEFWLOG-FIG-337-CLAIM figure-table:BASEFWLOG-FIG-337 -->

**[SPEC]** Figure 337, "Command Set Identifiers": Defines the identifier composition or namespace of values shown by Command Set Identifiers. Keep the value width, issuing authority, uniqueness scope, and reserved values separate. Evidence index: Command Set Identifier.

**[Explanation]** Defines the identifier composition or namespace of values shown by Command Set Identifiers. Keep the value width, issuing authority, uniqueness scope, and reserved values separate. Evidence index: Command Set Identifier.

Source field index: Command Set Identifier

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.14.1, Figure 337, printed pages 340, PDF pages 366

</details>

<details markdown="1">
<summary><strong>Figure 338: Identify – Identify Controller Data Structure, I/O Command Set Independent</strong> — minimum dependency slice</summary>

<!-- claim:BASEFWLOG-FIG-338-CLAIM figure-table:BASEFWLOG-FIG-338 -->

**[SPEC]** Figure 338, "Identify – Identify Controller Data Structure, I/O Command Set Independent": Defines the concrete layout or value relationships for Identify – Identify Controller Data Structure, I/O Command Set Independent. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is FR, MDS, ULIST, SMUD, FAWR, NOFS, FFSRO, MTFA, FWUG, DID, MPTFAWR.

**[Explanation]** Defines the concrete layout or value relationships for Identify – Identify Controller Data Structure, I/O Command Set Independent. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is FR, MDS, ULIST, SMUD, FAWR, NOFS, FFSRO, MTFA, FWUG, DID, MPTFAWR.

Source field index: FR, MDS, ULIST, SMUD, FAWR, NOFS, FFSRO, MTFA, FWUG, DID, MPTFAWR

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.14.2.1, Figure 338, printed pages 340-364, PDF pages 366-390

</details>

<details markdown="1">
<summary><strong>Figure 347: UUID List</strong> — minimum dependency slice</summary>

<!-- claim:BASEFWLOG-FIG-347-CLAIM figure-table:BASEFWLOG-FIG-347 -->

**[SPEC]** Figure 347, "UUID List": Defines the identifier composition or namespace of values shown by UUID List. Keep the value width, issuing authority, uniqueness scope, and reserved values separate. Evidence index: UUID1, UUID2, UUID126, UUID127, NVMe Invalid UUID.

**[Explanation]** Defines the identifier composition or namespace of values shown by UUID List. Keep the value width, issuing authority, uniqueness scope, and reserved values separate. Evidence index: UUID1, UUID2, UUID126, UUID127, NVMe Invalid UUID.

Source field index: UUID1, UUID2, UUID126, UUID127, NVMe Invalid UUID

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.14.2.14, Figure 347, printed pages 396, PDF pages 422

</details>

<details markdown="1">
<summary><strong>Figure 348: UUID List Entry</strong> — minimum dependency slice</summary>

<!-- claim:BASEFWLOG-FIG-348-CLAIM figure-table:BASEFWLOG-FIG-348 -->

**[SPEC]** Figure 348, "UUID List Entry": Defines the identifier composition or namespace of values shown by UUID List Entry. Keep the value width, issuing authority, uniqueness scope, and reserved values separate. Evidence index: ULEH, IDASSOC, UUID.

**[Explanation]** Defines the identifier composition or namespace of values shown by UUID List Entry. Keep the value width, issuing authority, uniqueness scope, and reserved values separate. Evidence index: ULEH, IDASSOC, UUID.

Source field index: ULEH, IDASSOC, UUID

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.14.2.14, Figure 348, printed pages 396, PDF pages 422

</details>

<details markdown="1">
<summary><strong>Figure 474: Asynchronous Event Configuration – Command Dword 11</strong> — minimum dependency slice</summary>

<!-- claim:BASEFWLOG-FIG-474-CLAIM figure-table:BASEFWLOG-FIG-474 -->

**[SPEC]** Figure 474, "Asynchronous Event Configuration – Command Dword 11": Defines the event record, event taxonomy, or logging condition represented by Asynchronous Event Configuration – Command Dword 11. Resolve event type and record length before decoding event-specific data. Evidence index: Firmware Activation Notices.

**[Explanation]** Defines the event record, event taxonomy, or logging condition represented by Asynchronous Event Configuration – Command Dword 11. Resolve event type and record length before decoding event-specific data. Evidence index: Firmware Activation Notices.

Source field index: Firmware Activation Notices

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.6, Figure 474, printed pages 466-468, PDF pages 492-494

</details>

## Limits

Verification date: 2026-09-01. No additional errata, ECNs, Technical Proposals, controller-vendor documents, or PCI Express Base Specification source text are included. Re-check affected claim IDs when the approved source set changes.
