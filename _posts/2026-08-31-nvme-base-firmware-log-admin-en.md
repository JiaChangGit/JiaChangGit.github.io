---
layout: post
read_time: true
show_date: true
title: "NVMe Base 2.4: Firmware Update and LID 03h Verification"
date: 2026-09-01
description: "Slide-ready bilingual source for firmware update and LID 03h."
lang: en
img: posts/2026/cat_title.jpg
tags: [NVMe, PCIe, Specification]
category: NVMe
author: Jia-Chang
github: JiaChangGit/JiaChangGit.github.io/tree/main/DOCS/nvme-spec-report
toc: yes
---

# NVMe Base 2.4: Firmware Update and LID 03h Verification

PPT authoring edition. The Chinese and English editions use the same slide modules, claim order, calculations, and source boundaries.

NVM Express Base Specification, Revision 2.4

NVM Express NVMe over PCIe Transport Specification, Revision 1.4 — §3.3 only

---

## Slide 01 — The real problem

> A successful download is not a successful activation. Track placement, pending activation, the reset boundary, and post-activation evidence separately.

```text
Download -> Commit / place -> activate now or later -> reset if required -> LID 03h verify
```

---

## Slide 02 — Vocabulary before fields

| State | Meaning | Evidence |
|---|---|---|
| Downloaded | Portions are temporary | NUMD / OFST |
| Stored | Image is in a slot | FRSx |
| Pending | Slot is selected for a later reset | NAFS |
| Active | Image is executing | CAFS + Identify.FR |

---

## Slide 03 — Mental Model and capability gate

Firmware slots belong to a domain. Before constructing a command, read FRMW, FWUG, MTFA, MPTFAWR, MDS/DID, and the current FR.

| Field | Question answered | Unit / range |
|---|---|---|
| FRMW | slots, read-only, immediate activation | bits |
| FWUG | chunk granularity and alignment | 4 KiB |
| MTFA | command-processing pause | 100 ms |
| MPTFAWR | CA=011b completion estimate | 100 ms |

Source map: Figure 338 (printed/PDF 340-365/366-391); Figures 347-348 (396/422).

<details markdown="1">
<summary><strong>Speaker notes / source claims</strong></summary>

<!-- claim:BASEFWLOG-MODEL-DOMAIN -->

**[SPEC]** Controllers in one domain share firmware slots, and the same firmware image is applied to all controllers in that domain. If multiple domains are not supported, that scope is the entire NVM subsystem.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.9, printed pages 202, PDF pages 228

<!-- claim:BASEFWLOG-CAP-FR -->

**[SPEC]** Identify Controller FR is the eight-byte ASCII string for the currently active firmware revision in the controller's domain. It is the same revision information available from LID 03h.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.14.1, printed pages 340, PDF pages 366

<!-- claim:BASEFWLOG-CAP-MDS-ULIST -->

**[SPEC]** CTRATT.MDS determines whether LID 03h returns domain-scoped or NVM-subsystem-scoped information, while CTRATT.ULIST indicates UUID List reporting support. With MDS=1, DID shall be nonzero; in a single-domain subsystem, DID shall be 0h.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.14.1, printed pages 346, 364, PDF pages 372, 390

<!-- claim:BASEFWLOG-CAP-FRMW -->

**[SPEC]** FRMW.SMUD, FAWR, NOFS, and FFSRO describe overlapping-update detection, activation without reset, the domain's supported slot count (1 through 7), and whether slot 1 is read-only.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.14.1, printed pages 354, PDF pages 380

<!-- claim:BASEFWLOG-CAP-MTFA -->

**[SPEC]** MTFA is in 100 ms units and reports the maximum time command processing is temporarily stopped during activation. It shall be valid when activation without reset is supported; 0h means the maximum is undefined.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.14.1, printed pages 357, PDF pages 383

<!-- claim:BASEFWLOG-CAP-FWUG -->

**[SPEC]** FWUG constrains NUMD and OFST granularity/alignment in 4 KiB units: 1h is 4 KiB, 2h is 8 KiB, 0h reports no information, and FFh permits any dword granularity and alignment. A controller may return Invalid Field in Command for a violation.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.14.1, printed pages 359, PDF pages 385

<!-- claim:BASEFWLOG-CAP-MPTFAWR -->

**[SPEC]** MPTFAWR is a 100 ms-unit estimate of the maximum processing time to complete Firmware Commit with CA=011b, including time to commit the image to a slot. It shall be 0h when activation without reset is unsupported.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.14.1, printed pages 364, PDF pages 390

</details>

---

## Slide 04 — Download means dword ranges

```text
bytes = (NUMD + 1) × 4
byte offset = OFST × 4
```

**Example:** 4 KiB = 1024 dwords, so NUMD=03FFh. A portion beginning at byte 8192 uses OFST=0800h.

Source map: Figure 93 (140-142/166-168); Figures 190-193 (205-206/231-232).

<details markdown="1">
<summary><strong>Speaker notes / source claims</strong></summary>

<!-- claim:BASEFWLOG-FW-SEQUENCE -->

**[SPEC]** The host should not overlap firmware or Boot Partition update sequences and should use only one controller or Management Endpoint throughout a sequence.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.11, printed pages 137, PDF pages 163

<!-- claim:BASEFWLOG-DOWNLOAD-RANGE -->

**[SPEC]** Firmware Image Download may split an image into portions, and firmware-image portions may arrive out of order. The host should avoid overlapping ranges and comply with FWUG. Boot Partition portions shall be submitted in order.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.10, printed pages 205-206, PDF pages 231-232

<!-- claim:BASEFWLOG-DOWNLOAD-FIELDS -->

**[SPEC]** An Admin command over NVMe over PCIe shall not use SGL, so DPTR uses PRPs to identify the source buffer. NUMD is a zero-based dword count, so bytes=(NUMD+1)×4; OFST is a dword offset from the image start, so byte offset=OFST×4. The portion containing the image start shall use OFST=0h.

> Source: NVME-BASE-2.4, Rev. 2.4, §4.1.1, 5.2.10, printed pages 140-142, 205-206, PDF pages 166-168, 231-232

<!-- claim:BASEFWLOG-FW-DISCARD -->

**[SPEC]** The first Firmware Image Download after Firmware Commit completes, and a Controller Level Reset after download but before Firmware Commit completion, shall cause the controller to discard remaining downloaded portions.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.11, 5.2.10, printed pages 137, 205-206, PDF pages 163, 231-232

</details>

---

## Slide 05 — Commit Action is a state transition

| CA | Placement | Activation |
|---|---|---|
| 000b | downloaded image -> slot | none |
| 001b | downloaded image -> slot | next capable CLR |
| 010b | existing slot | next capable CLR |
| 011b | downloaded or existing slot | immediate; command waits |

Source map: Figures 187-189 (203-205/229-231).

<details markdown="1">
<summary><strong>Speaker notes / source claims</strong></summary>

<!-- claim:BASEFWLOG-COMMIT-PURPOSE -->

**[SPEC]** Firmware Commit validates the last downloaded image, places it in a firmware slot, and uses Commit Action to choose placement only, activation at a later Controller Level Reset, or immediate activation. Successful commit does not by itself mean the image is currently active.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.9, printed pages 202-203, PDF pages 228-229

<!-- claim:BASEFWLOG-COMMIT-CDW10 -->

**[SPEC]** CDW10[5:3] is CA and CDW10[2:0] is FS. CA 000b places only, 001b places and schedules activation at the next CLR, 010b schedules an existing slot, and 011b activates immediately. With FS=0h, the controller shall choose a slot from 1 through 7.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.9, printed pages 203, PDF pages 229

<!-- claim:BASEFWLOG-COMMIT-BOOT -->

**[SPEC]** BPID and CA=110b/111b belong to Boot Partition handling: 110b replaces the selected partition, 111b marks it active, and Boot Partition Write Prohibited is one of the Firmware Commit command-specific status values.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.9, printed pages 203-205, PDF pages 229-231

<!-- claim:BASEFWLOG-COMMIT-MUD -->

**[SPEC]** Firmware Commit CQE.DW0[1:0] MUD reports overlap detected through a Management Endpoint and an Admin Submission Queue. If FRMW.SMUD is 0, MUD shall be 00b; MUD is valid whether the command succeeds or is aborted.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.9, printed pages 204, PDF pages 230

<!-- claim:BASEFWLOG-COMMIT-STATUS -->

**[SPEC]** Firmware Commit command-specific status distinguishes invalid slot/image, required Conventional/NVM Subsystem/Controller Level Reset, MTFA violation, activation prohibited, overlapping range, Boot Partition write prohibition, and personality incompatibility.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.9, printed pages 204-205, PDF pages 230-231

</details>

---

## Slide 06 — Activation has four branches

```text
CA 000b -> stored only
CA 001b / 010b -> pending -> required CLR -> reinitialize
CA 011b -> command in progress -> success or reset-required / time / prohibited status
load failure -> most recently active image -> baseline read-only fallback
```

Source map: Figures 155 and 474 (186/212 and 466-468/492-494); Figures 347-348 (396/422).

<details markdown="1">
<summary><strong>Speaker notes / source claims</strong></summary>

<!-- claim:BASEFWLOG-FW-RESET -->

**[SPEC]** The reset-based flow is one or more Firmware Image Download commands, Firmware Commit to validate and place the image, a Controller Level Reset capable of causing activation, and reinitialization of the controller and I/O queues.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.11, printed pages 135-136, PDF pages 161-162

<!-- claim:BASEFWLOG-FW-IMMEDIATE -->

**[SPEC]** CA=011b requests immediate activation. Firmware Commit is not a background operation and remains in progress until activation succeeds or fails. If Firmware Activation notices are enabled, an affected controller may send Firmware Activation Starting.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.11, printed pages 136, PDF pages 162

<!-- claim:BASEFWLOG-FW-FAILURE -->

**[SPEC]** If the new image cannot be loaded, the controller shall revert to the image in the most recently activated slot; if that image also cannot be loaded, it loads an available baseline read-only image and generates Firmware Image Load Error.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.11, printed pages 136-137, PDF pages 162-163

<!-- claim:BASEFWLOG-RESET-XREF -->

**[SPEC]** NVMe over PCIe Transport lists Conventional Reset and Function Level Reset as distinct additional transport-specific Controller Level Reset methods. Except for Controller Reset, Controller Level Reset resets PCI register space as defined by the PCI Express Base Specification.

> Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.3, printed pages 11, PDF pages 11

<!-- claim:BASEFWLOG-UUID-LIST -->

**[SPEC]** Across firmware revisions, UUID List entry positions should remain stable: new UUIDs should be appended, a removed UUID should be replaced in place with the NVMe Invalid UUID, an invalid entry should not be reused, and the list should not be shortened or removed.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.11.1, printed pages 137-138, PDF pages 163-164

<!-- claim:BASEFWLOG-UUID-RESET -->

**[SPEC]** If a downloaded image replaces the NVMe Invalid UUID or a different valid UUID with a valid UUID in an existing entry, the controller shall require reset, and all controllers affected by that UUID List change shall be reset.

> Source: NVME-BASE-2.4, Rev. 2.4, §3.11.1, printed pages 138, PDF pages 164

<!-- claim:BASEFWLOG-XREF-337 -->

**[SPEC]** Source §5.2.9 points Firmware Revision to Figure 337, but Figure 337 contains Command Set Identifiers and FR appears in Figure 338. Without separately approved errata, this report preserves and discloses the internal source discrepancy instead of silently rewriting it.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.9, 5.2.14.1, printed pages 202, 340, PDF pages 228, 366

</details>

---

## Slide 07 — Status selects recovery

| SC | Meaning | Correct direction |
|---|---|---|
| 06h / 07h | invalid slot / image | fix target or image |
| 0Bh | Conventional Reset required | do not substitute FLR |
| 10h | NVM Subsystem Reset required | smaller reset keeps old image |
| 11h | Controller Level Reset required | activate at next CLR |
| 12h | maximum-time violation | image committed; schedule with CA=010b |
| 13h / 14h | prohibited / overlap | policy or range fix |

---

## Slide 08 — Construct the LID 03h command

```text
512 bytes / 4 = 128 dwords
NUMD = 128 - 1 = 127 = 007Fh
CDW10 = NUMDL[31:16] | RAE=0 | LSP=0 | LID=03h
      = 007F0003h
```

Source map: Figure 93 (140-142/166-168); Figures 203-209 (213-216/239-242).

<details markdown="1">
<summary><strong>Speaker notes / source claims</strong></summary>

<!-- claim:BASEFWLOG-LOG-COMMAND -->

**[SPEC]** When reading LID 03h, no namespace is used, so NSID shall be 0h, and DPTR uses PRPs to identify the 512-byte destination buffer. The required CDW10-CDW14 slice is LID=03h, LSP=0, RAE=0, NUMDL/NUMDU for 512 bytes, LSI=0, LPOL/LPOU=0, OT=0, and UIDX=0. LID 03h does not use CSI, which the controller ignores under Figure 208's rule.

> Source: NVME-BASE-2.4, Rev. 2.4, §4.1.1, 5.2.13, printed pages 140-142, 212-215, PDF pages 166-168, 238-241

<!-- claim:BASEFWLOG-LOG-LENGTH -->

**[SPEC]** NUMDL and NUMDU form a zero-based dword count. LID 03h is 512 bytes, or 128 dwords, so NUMD=127=0000007Fh, NUMDL=007Fh, and NUMDU=0000h. With LSP=0 and RAE=0, CDW10=007F0003h.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13, printed pages 213-215, PDF pages 239-241

<!-- claim:BASEFWLOG-LOG-RAE -->

**[SPEC]** RAE=0 clears the corresponding asynchronous event on successful completion, while RAE=1 retains it. If the command fails, the controller shall retain the event. Firmware Activation Starting is cleared by reading LID 03h with RAE=0.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.2, 5.2.13, printed pages 186, 213, PDF pages 212, 239

<!-- claim:BASEFWLOG-LOG-OFFSET -->

**[SPEC]** This report uses the complete 512-byte LID 03h with LPOL=LPOU=0 and OT=0. A general byte offset is dword aligned, and an offset beyond the log page shall return Invalid Field in Command. LID 03h needs no index-offset branch.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13, printed pages 214-215, PDF pages 240-241

<!-- claim:BASEFWLOG-LOG-SCOPE -->

**[SPEC]** The LID 03h row in Figure 209 specifies CSI=N, scope=Domain/NVM subsystem, and reference §5.2.13.1.4. With MDS=1, the data is for the domain containing the controller that processed the command; otherwise it is for the NVM subsystem.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13, printed pages 215-216, PDF pages 241-242

</details>

---

## Slide 09 — Decode AFI before revision strings

```text
byte 0: [7 R][6:4 NAFS][3 R][2:0 CAFS]
bytes 1:7: reserved
bytes 8:63: FRS1 ... FRS7 (8 bytes each)
bytes 64:511: reserved
```

**Example:** AFI=21h means NAFS=2 and CAFS=1. Slot 2 is pending; slot 1 is still executing.

Source map: Figure 215 (printed/PDF 226/252).

<details markdown="1">
<summary><strong>Speaker notes / source claims</strong></summary>

<!-- claim:BASEFWLOG-LID03-DESCRIPTION -->

**[SPEC]** The 512-byte Firmware Slot Information log page reports the firmware revision stored in each supported slot and identifies the current active slot plus the next active slot when reported. Revisions are ASCII strings.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.4, printed pages 225-226, PDF pages 251-252

<!-- claim:BASEFWLOG-LID03-AFI -->

**[SPEC]** In AFI byte 0, NAFS is bits 6:4 and CAFS is bits 2:0; bits 7 and 3 are reserved. Nonzero NAFS identifies the slot to activate at the next CLR capable of causing activation; NAFS=0 means no next slot is indicated. CAFS identifies the source slot of the running image.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.4, printed pages 226, PDF pages 252

<!-- claim:BASEFWLOG-LID03-FRS -->

**[SPEC]** FRS1 through FRS7 occupy bytes 8-63, eight bytes per slot. If a slot has no valid revision or is unsupported, its FRS shall be cleared to 0h. Bytes 1-7 and 64-511 are reserved.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.4, printed pages 226, PDF pages 252

</details>

---

## Slide 10 — End-to-End Example

| Stage | Concrete value | Evidence |
|---|---|---|
| Capability | NOFS=3, FFSRO=1, FWUG=1h | choose writable slot 2 |
| Download | NUMD=03FFh; OFST=0/0400h/0800h | 12 KiB transferred |
| Commit | CA=001b, FS=2, CDW10=0000000Ah | slot 2 pending |
| Pre-reset | LID03 CDW10=007F0003h, AFI=21h | CAFS1 / NAFS2 |
| Post-reset | CAFS=2, FRS2=Identify.FR | activation verified |

---

## Slide 11 — Debug from the first broken boundary

| Symptom | First evidence |
|---|---|
| Download Invalid Field | PRP, NUMD, OFST, FWUG |
| Commit invalid slot | NOFS, FFSRO, FS |
| Reset-required SC | full SCT/SC and actual reset trace |
| FRS2 valid, CAFS still 1 | CA, NAFS, reset type |
| controllers disagree | MDS, DID, processing controller |

---

## Slide 12 — Takeaway and source boundary

> Treat firmware update as a state machine with domain scope. Commands move the state; completion status selects recovery; LID 03h proves the resulting slot state.

Included: §3.11, §3.11.1, §5.2.9, §5.2.10, the minimum common §5.2.13 fields needed for LID 03h, and §5.2.13.1.4; main printed pages 135-138, 202-206, 212-216, and 225-226, plus the minimum dependency slice

Verification date: 2026-09-01. No additional errata, ECNs, vendor documents, or PCI Express Base Specification source text are included.

## Acronyms first: complete glossary

Every abbreviation below is introduced before it is used in the slide narrative. The term alone is never enough: retain owner, width, unit, scope, and state.

| Acronym / term | Plain-language meaning | Source |
|---|---|---|
| `LID` | Log Page Identifier, the Get Log Page field selecting a log page. | NVME-BASE-2.4 Rev. 2.4, §4.1.1, 5.2.13, printed pp. 140-142, 212-215, PDF pp. 166-168, 238-241 |
| `LID 03h` | Identifier 03h for the Firmware Slot Information log page. | NVME-BASE-2.4 Rev. 2.4, §5.2.13.1.4, printed pp. 225-226, PDF pp. 251-252 |
| `AFI` | Active Firmware Info, the LID 03h byte containing the current active slot and the slot scheduled for the next reset. | NVME-BASE-2.4 Rev. 2.4, §5.2.13.1.4, printed pp. 226, PDF pp. 252 |
| `CAFS` | Current Active Firmware Slot, the low three AFI bits identifying the currently executing firmware slot. | NVME-BASE-2.4 Rev. 2.4, §5.2.13.1.4, printed pp. 226, PDF pp. 252 |
| `NAFS` | Next Active Firmware Slot, AFI bits 6:4 identifying the slot scheduled for the next reset; zero means none is scheduled. | NVME-BASE-2.4 Rev. 2.4, §5.2.13.1.4, printed pp. 226, PDF pp. 252 |
| `FRS` | Firmware Revision for Slot, the eight-byte revision-string field for each slot in LID 03h. | NVME-BASE-2.4 Rev. 2.4, §5.2.13.1.4, printed pp. 226, PDF pp. 252 |
| `FR` | Firmware Revision, the eight-byte ASCII Identify Controller field reporting the active firmware revision. | NVME-BASE-2.4 Rev. 2.4, §5.2.14.1, printed pp. 340, PDF pp. 366 |
| `FRMW` | Firmware Updates, the Identify Controller field reporting slot count, slot-1 read-only state, and activation capabilities. | NVME-BASE-2.4 Rev. 2.4, §5.2.14.1, printed pp. 354, PDF pp. 380 |
| `FWUG` | Firmware Update Granularity, the capability field governing download-portion granularity and alignment. | NVME-BASE-2.4 Rev. 2.4, §5.2.14.1, printed pp. 359, PDF pp. 385 |
| `MTFA` | Maximum Time for Firmware Activation, the maximum time activation may pause command processing. | NVME-BASE-2.4 Rev. 2.4, §5.2.14.1, printed pp. 357, PDF pp. 383 |
| `MPTFAWR` | Maximum Processing Time for Firmware Activation Without Reset, the maximum processing time for immediate activation without a reset. | NVME-BASE-2.4 Rev. 2.4, §5.2.14.1, printed pp. 364, PDF pp. 390 |
| `MDS` | Multiple Domain Subsystem, the capability bit indicating whether an NVM subsystem contains multiple domains. | NVME-BASE-2.4 Rev. 2.4, §5.2.14.1, printed pp. 346, 364, PDF pp. 372, 390 |
| `DID` | Domain Identifier, the identifier of a domain within an NVM subsystem. | NVME-BASE-2.4 Rev. 2.4, §5.2.14.1, printed pp. 346, 364, PDF pp. 372, 390 |
| `ULIST` | UUID List, the capability bit indicating support for the UUID List data structure. | NVME-BASE-2.4 Rev. 2.4, §5.2.14.1, printed pp. 346, 364, PDF pp. 372, 390 |
| `UUID` | Universally Unique Identifier, a 128-bit identifier whose association scope is defined by the containing structure. | NVME-BASE-2.4 Rev. 2.4, §3.11.1, printed pp. 137-138, PDF pp. 163-164 |
| `DPTR` | Data Pointer, the SQE field identifying a command data buffer. | NVME-BASE-2.4 Rev. 2.4, §4.1.1, 5.2.10, printed pp. 140-142, 205-206, PDF pp. 166-168, 231-232 |
| `PRP` | Physical Region Page, a pointer format describing a host-addressable data buffer in memory-page units. | NVME-BASE-2.4 Rev. 2.4, §4.1.1, 5.2.10, printed pp. 140-142, 205-206, PDF pp. 166-168, 231-232 |
| `NUMD` | Number of Dwords, a zero-based transfer-dword count; actual bytes = (NUMD + 1) × 4. | NVME-BASE-2.4 Rev. 2.4, §4.1.1, 5.2.10, printed pp. 140-142, 205-206, PDF pp. 166-168, 231-232 |
| `NUMDL` | Number of Dwords Lower, the low 16 bits of Get Log Page NUMD. | NVME-BASE-2.4 Rev. 2.4, §4.1.1, 5.2.13, printed pp. 140-142, 212-215, PDF pp. 166-168, 238-241 |
| `NUMDU` | Number of Dwords Upper, the high 16 bits of Get Log Page NUMD. | NVME-BASE-2.4 Rev. 2.4, §4.1.1, 5.2.13, printed pp. 140-142, 212-215, PDF pp. 166-168, 238-241 |
| `OFST` | Offset, the dword-based image-relative offset in Firmware Image Download. | NVME-BASE-2.4 Rev. 2.4, §4.1.1, 5.2.10, printed pp. 140-142, 205-206, PDF pp. 166-168, 231-232 |
| `RAE` | Retain Asynchronous Event, the Get Log Page selector controlling retention of a related asynchronous event. | NVME-BASE-2.4 Rev. 2.4, §5.2.2, 5.2.13, printed pp. 186, 213, PDF pp. 212, 239 |
| `LSP` | Log Specific Field, a command selector whose meaning is defined by the selected log page. | NVME-BASE-2.4 Rev. 2.4, §4.1.1, 5.2.13, printed pp. 140-142, 212-215, PDF pp. 166-168, 238-241 |
| `LSI` | Log Specific Identifier, an identifier whose meaning is defined by the selected log page. | NVME-BASE-2.4 Rev. 2.4, §4.1.1, 5.2.13, printed pp. 140-142, 212-215, PDF pp. 166-168, 238-241 |
| `LPOL` | Log Page Offset Lower, the low 32 bits of the Get Log Page byte offset. | NVME-BASE-2.4 Rev. 2.4, §5.2.13, printed pp. 214-215, PDF pp. 240-241 |
| `LPOU` | Log Page Offset Upper, the high 32 bits of the Get Log Page byte offset. | NVME-BASE-2.4 Rev. 2.4, §5.2.13, printed pp. 214-215, PDF pp. 240-241 |
| `CSI` | Command Set Identifier, the command-set context associated with a log page. | NVME-BASE-2.4 Rev. 2.4, §4.1.1, 5.2.13, printed pp. 140-142, 212-215, PDF pp. 166-168, 238-241 |
| `UIDX` | UUID Index, an index into the UUID List; zero indicates that no UUID is specified. | NVME-BASE-2.4 Rev. 2.4, §4.1.1, 5.2.13, printed pp. 140-142, 212-215, PDF pp. 166-168, 238-241 |
| `CA` | Commit Action, the Firmware Commit field selecting replacement, activation, and reset policy. | NVME-BASE-2.4 Rev. 2.4, §5.2.9, printed pp. 203, PDF pp. 229 |
| `FS` | Firmware Slot, the Firmware Commit field selecting the target slot. | NVME-BASE-2.4 Rev. 2.4, §5.2.9, printed pp. 203, PDF pp. 229 |
| `MUD` | Multiple Update Detected, the completion bit indicating detection of overlapping firmware-update sequences. | NVME-BASE-2.4 Rev. 2.4, §5.2.9, printed pp. 204, PDF pp. 230 |
| `SCT` | Status Code Type, the category selected before interpreting SC. | NVME-BASE-2.4 Rev. 2.4, §5.2.9, printed pp. 204-205, PDF pp. 230-231 |
| `SC` | Status Code, the specific completion result interpreted in the context of SCT. | NVME-BASE-2.4 Rev. 2.4, §5.2.9, printed pp. 204-205, PDF pp. 230-231 |
| `CQE` | Completion Queue Entry, one completion-result structure in a CQ. | NVME-BASE-2.4 Rev. 2.4, §5.2.9, printed pp. 204-205, PDF pp. 230-231 |
| `AEN` | Asynchronous Event Notification, a notification delivered through a submitted Asynchronous Event Request. | NVME-BASE-2.4 Rev. 2.4, §5.2.2, 5.2.13, printed pp. 186, 213, PDF pp. 212, 239 |

## Visual atlas: locate the system before reading fields

Each redraw answers a different question: architecture locates components, sequence shows ownership, decode turns bits into engineering values, and state views preserve failure evidence. These are teaching redraws, not copies of specification artwork.

### Visual 01: Read capabilities before choosing a firmware-update plan

**View type:** `architecture`

```text
[Identify Controller snapshot]
  ├─ [FRMW: slots / activation]
  ├─ [FWUG: chunks / alignment]
  ├─ [MTFA / MPTFAWR: timeout]
  ├─ [MDS / DID: sharing scope]
  └─ [Build a legal update plan]
```

**Question answered:** Firmware update is not a fixed command recipe. FRMW controls slots and activation capability, FWUG controls download granularity and alignment, MTFA and MPTFAWR bound waiting time, and MDS/DID define which controllers share the result.

**Supporting Figures:** Figure 337, Figure 338

**Sources:** NVME-BASE-2.4 Rev. 2.4, §5.2.14.1, printed pp. 354, PDF pp. 380; NVME-BASE-2.4 Rev. 2.4, §5.2.14.1, printed pp. 359, PDF pp. 385; NVME-BASE-2.4 Rev. 2.4, §5.2.14.1, printed pp. 357, PDF pp. 383; NVME-BASE-2.4 Rev. 2.4, §5.2.14.1, printed pp. 364, PDF pp. 390; NVME-BASE-2.4 Rev. 2.4, §5.2.14.1, printed pp. 346, 364, PDF pp. 372, 390

### Visual 02: Download is byte-range geometry, not a direct file upload

**View type:** `architecture`

```text
[Image bytes]
  ├─ [Split by FWUG]
  ├─ [bytes / 4 → dwords]
  ├─ [NUMD = dwords - 1]
  ├─ [OFST = sent bytes / 4]
  └─ [Advance after CQE success]
```

**Question answered:** Each Firmware Image Download uses DPTR for the host buffer, zero-based NUMD for transfer dwords, and OFST for the image-relative dword offset. The host must prove buffer validity, length, offset, FWUG compliance, and absence of gaps or overlaps.

**Supporting Figures:** Figure 93, Figure 190, Figure 191, Figure 192, Figure 193

**Sources:** NVME-BASE-2.4 Rev. 2.4, §5.2.10, printed pp. 205-206, PDF pp. 231-232; NVME-BASE-2.4 Rev. 2.4, §4.1.1, 5.2.10, printed pp. 140-142, 205-206, PDF pp. 166-168, 231-232

### Visual 03: Commit converts downloaded portions into slot state and activation policy

**View type:** `architecture`

```text
[Downloaded portions complete]
  ├─ [Encode CA / FS]
  ├─ [Controller validates image]
  ├─ [Place in slot / schedule or activ…]
  ├─ [Decode complete SCT / SC / MUD]
  └─ [Choose reset / verify / stop]
```

**Question answered:** Commit Action (CA) is not a success flag; it selects replacement, activation, and reset boundary. Firmware Slot (FS) selects the target slot, while CQE status determines whether software verifies, performs a specific reset, waits, or stops.

**Supporting Figures:** Figure 187, Figure 188, Figure 189

**Sources:** NVME-BASE-2.4 Rev. 2.4, §5.2.9, printed pp. 202-203, PDF pp. 228-229; NVME-BASE-2.4 Rev. 2.4, §5.2.9, printed pp. 203, PDF pp. 229; NVME-BASE-2.4 Rev. 2.4, §5.2.9, printed pp. 204, PDF pp. 230; NVME-BASE-2.4 Rev. 2.4, §5.2.9, printed pp. 204-205, PDF pp. 230-231

### Visual 04: LID 03h verification is more than reading one revision string

**View type:** `architecture`

```text
[Build Get Log Page SQE]
  ├─ [LID=03h / NUMD=127]
  ├─ [Read the 512-byte buffer]
  ├─ [AFI → CAFS / NAFS]
  ├─ [Decode FRS1-FRS7 per slot]
  └─ [Compare Identify.FR and expected …]
```

**Question answered:** Get Log Page first builds a 512-byte transfer from common command fields and selects Firmware Slot Information with LID=03h. AFI separates CAFS from NAFS, FRS1-FRS7 report slot revisions, and Identify.FR plus domain scope provide the final cross-check.

**Supporting Figures:** Figure 203, Figure 204, Figure 205, Figure 206, Figure 207, Figure 208, Figure 209, Figure 215, Figure 338

**Sources:** NVME-BASE-2.4 Rev. 2.4, §4.1.1, 5.2.13, printed pp. 140-142, 212-215, PDF pp. 166-168, 238-241; NVME-BASE-2.4 Rev. 2.4, §5.2.13, printed pp. 213-215, PDF pp. 239-241; NVME-BASE-2.4 Rev. 2.4, §5.2.13, printed pp. 215-216, PDF pp. 241-242; NVME-BASE-2.4 Rev. 2.4, §5.2.13.1.4, printed pp. 226, PDF pp. 252; NVME-BASE-2.4 Rev. 2.4, §5.2.13.1.4, printed pp. 226, PDF pp. 252; NVME-BASE-2.4 Rev. 2.4, §5.2.14.1, printed pp. 340, PDF pp. 366

## Appendix A — Supporting Figure / Field Reference

Figures are traceable evidence for the workflow, not the article outline. Dependency entries expose only the required slice; Figure 209 is limited to the LID 03h row.

<details markdown="1">
<summary><strong>Figure 187: Firmware Commit – Command Dword 10</strong></summary>

<!-- claim:BASEFWLOG-FIG-187-CLAIM figure-table:BASEFWLOG-FIG-187 -->

**SPEC.** Figure 187, "Firmware Commit – Command Dword 10": Defines the concrete layout or value relationships for Firmware Commit – Command Dword 10. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is BPID, CA, FS.

#### Where this Figure fits

Figure 187 sits in §5.2.9 and acts as a command checkpoint. Read it after the report mental model has established the owning object and before software turns BPID into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a command-construction field table. Build the common SQE, locate the specified CDW, encode each bit range, clear reserved bits, and validate the result against transfer length, buffer, and completion status. Equal field names do not imply equal semantics across commands.

#### Teaching redraw

```text
[Locate source: BPID]
          ↓
[Extract field: CA] → [Apply encoding: FS]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `BPID` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `CA` | Commit Action, the Firmware Commit field selecting replacement, activation, and reset policy. |
| `FS` | Firmware Slot, the Firmware Commit field selecting the target slot. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §5.2.9 is the applicable context.
2. Decode BPID at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check CA as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 187 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §5.2.9 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes BPID, CA, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §5.2.9, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 187. Annotate the bytes containing BPID, decode them, and independently verify CA. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of BPID in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand BPID and state its unit or object scope?
2. Can the reader explain why CA is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** BPID, CA, FS

**Source keyword index:** `shall`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.9, Figure 187, printed pages 203, PDF pages 229

</details>

<details markdown="1">
<summary><strong>Figure 188: Firmware Commit – Completion Queue Entry Dword 0</strong></summary>

<!-- claim:BASEFWLOG-FIG-188-CLAIM figure-table:BASEFWLOG-FIG-188 -->

**SPEC.** Figure 188, "Firmware Commit – Completion Queue Entry Dword 0": Shows the queue or command relationship expressed by Firmware Commit – Completion Queue Entry Dword 0. Trace ownership and direction from host to SQ, controller, and CQ; keep the indexed elements distinct: MUD, MEFWO, ASQFWO.

#### Where this Figure fits

Figure 188 sits in §5.2.9.1 and acts as a queue checkpoint. Read it after the report mental model has established the owning object and before software turns MUD into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a queue or command-flow Figure. Label host and controller ownership first, then trace head, tail, phase, or arbitration changes. An arrow represents a state or ownership transition and does not automatically prove command completion.

#### Teaching redraw

```text
[Locate source: MUD]
          ↓
[Extract field: MEFWO] → [Apply encoding: ASQFWO]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `MUD` | Multiple Update Detected, the completion bit indicating detection of overlapping firmware-update sequences. |
| `MEFWO` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `ASQFWO` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §5.2.9.1 is the applicable context.
2. Decode MUD at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check MEFWO as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 188 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §5.2.9.1 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes MUD, MEFWO, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §5.2.9.1, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 188. Annotate the bytes containing MUD, decode them, and independently verify MEFWO. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of MUD in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand MUD and state its unit or object scope?
2. Can the reader explain why MEFWO is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** MUD, MEFWO, ASQFWO

**Source keyword index:** `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.9.1, Figure 188, printed pages 204, PDF pages 230

</details>

<details markdown="1">
<summary><strong>Figure 189: Firmware Commit – Command Specific Status Values</strong></summary>

<!-- claim:BASEFWLOG-FIG-189-CLAIM figure-table:BASEFWLOG-FIG-189 -->

**SPEC.** Figure 189, "Firmware Commit – Command Specific Status Values": Defines the concrete layout or value relationships for Firmware Commit – Command Specific Status Values. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is Invalid Firmware Slot, Invalid Firmware Image, reset-required status, MTFA, Overlapping Range.

#### Where this Figure fits

Figure 189 sits in §5.2.9.1 and acts as a layout checkpoint. Read it after the report mental model has established the owning object and before software turns Invalid Firmware Slot into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a structure or capability field table. Locate it using the structure base and offset, read in byte/bit order, and separate capability gates, value encoding, and reserved areas. Presence in the table does not mean the function is supported.

#### Teaching redraw

```text
[Locate source: Invalid Firmware Slot]
          ↓
[Extract field: Invalid Firmware Image] → [Apply encoding: reset-required status]
                                      ↓
[Validate evidence: MTFA]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `Invalid Firmware Slot` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `Invalid Firmware Image` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `reset-required status` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `MTFA` | Maximum Time for Firmware Activation, the maximum time activation may pause command processing. |
| `Overlapping Range` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §5.2.9.1 is the applicable context.
2. Decode Invalid Firmware Slot at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check Invalid Firmware Image as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 189 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §5.2.9.1 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes Invalid Firmware Slot, Invalid Firmware Image, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §5.2.9.1, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 189. Annotate the bytes containing Invalid Firmware Slot, decode them, and independently verify Invalid Firmware Image. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of Invalid Firmware Slot in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand Invalid Firmware Slot and state its unit or object scope?
2. Can the reader explain why Invalid Firmware Image is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** Invalid Firmware Slot, Invalid Firmware Image, reset-required status, MTFA, Overlapping Range

**Source keyword index:** `shall`, `should`, `may`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.9.1, Figure 189, printed pages 204-205, PDF pages 230-231

</details>

<details markdown="1">
<summary><strong>Figure 190: Firmware Image Download – Data Pointer</strong></summary>

<!-- claim:BASEFWLOG-FIG-190-CLAIM figure-table:BASEFWLOG-FIG-190 -->

**SPEC.** Figure 190, "Firmware Image Download – Data Pointer": Defines how Firmware Image Download – Data Pointer identifies the destination or source buffer for this command. Resolve pointer type and address before checking transfer length and alignment. Evidence index: DPTR.

#### Where this Figure fits

Figure 190 sits in §5.2.10 and acts as a command checkpoint. Read it after the report mental model has established the owning object and before software turns DPTR into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a command-construction field table. Build the common SQE, locate the specified CDW, encode each bit range, clear reserved bits, and validate the result against transfer length, buffer, and completion status. Equal field names do not imply equal semantics across commands.

#### Teaching redraw

```text
[Locate source: DPTR]
          ↓
[Extract field: evidence] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `DPTR` | Data Pointer, the SQE field identifying a command data buffer. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §5.2.10 is the applicable context.
2. Decode DPTR at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check the cited condition as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 190 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §5.2.10 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes DPTR, the cited condition, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §5.2.10, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 190. Annotate the bytes containing DPTR, decode them, and independently verify the cited condition. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of DPTR in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand DPTR and state its unit or object scope?
2. Can the reader explain why the cited condition is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** DPTR

**Source keyword index:** `should`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.10, Figure 190, printed pages 205, PDF pages 231

</details>

<details markdown="1">
<summary><strong>Figure 191: Firmware Image Download – Command Dword 10</strong></summary>

<!-- claim:BASEFWLOG-FIG-191-CLAIM figure-table:BASEFWLOG-FIG-191 -->

**SPEC.** Figure 191, "Firmware Image Download – Command Dword 10": Defines the concrete layout or value relationships for Firmware Image Download – Command Dword 10. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is NUMD, FWUG.

#### Where this Figure fits

Figure 191 sits in §5.2.10 and acts as a command checkpoint. Read it after the report mental model has established the owning object and before software turns NUMD into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a command-construction field table. Build the common SQE, locate the specified CDW, encode each bit range, clear reserved bits, and validate the result against transfer length, buffer, and completion status. Equal field names do not imply equal semantics across commands.

#### Teaching redraw

```text
[Locate source: NUMD]
          ↓
[Extract field: FWUG] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `NUMD` | Number of Dwords, a zero-based transfer-dword count; actual bytes = (NUMD + 1) × 4. |
| `FWUG` | Firmware Update Granularity, the capability field governing download-portion granularity and alignment. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §5.2.10 is the applicable context.
2. Decode NUMD at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check FWUG as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 191 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §5.2.10 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes NUMD, FWUG, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §5.2.10, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 191. Annotate the bytes containing NUMD, decode them, and independently verify FWUG. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of NUMD in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand NUMD and state its unit or object scope?
2. Can the reader explain why FWUG is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** NUMD, FWUG

**Source keyword index:** `may`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.10, Figure 191, printed pages 205, PDF pages 231

</details>

<details markdown="1">
<summary><strong>Figure 192: Firmware Image Download – Command Dword 11</strong></summary>

<!-- claim:BASEFWLOG-FIG-192-CLAIM figure-table:BASEFWLOG-FIG-192 -->

**SPEC.** Figure 192, "Firmware Image Download – Command Dword 11": Defines the concrete layout or value relationships for Firmware Image Download – Command Dword 11. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is OFST, FWUG.

#### Where this Figure fits

Figure 192 sits in §5.2.10 and acts as a command checkpoint. Read it after the report mental model has established the owning object and before software turns OFST into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a command-construction field table. Build the common SQE, locate the specified CDW, encode each bit range, clear reserved bits, and validate the result against transfer length, buffer, and completion status. Equal field names do not imply equal semantics across commands.

#### Teaching redraw

```text
[Locate source: OFST]
          ↓
[Extract field: FWUG] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `OFST` | Offset, the dword-based image-relative offset in Firmware Image Download. |
| `FWUG` | Firmware Update Granularity, the capability field governing download-portion granularity and alignment. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §5.2.10 is the applicable context.
2. Decode OFST at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check FWUG as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 192 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §5.2.10 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes OFST, FWUG, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §5.2.10, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 192. Annotate the bytes containing OFST, decode them, and independently verify FWUG. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of OFST in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand OFST and state its unit or object scope?
2. Can the reader explain why FWUG is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** OFST, FWUG

**Source keyword index:** none

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.10, Figure 192, printed pages 206, PDF pages 232

</details>

<details markdown="1">
<summary><strong>Figure 193: Firmware Image Download – Command Specific Status Values</strong></summary>

<!-- claim:BASEFWLOG-FIG-193-CLAIM figure-table:BASEFWLOG-FIG-193 -->

**SPEC.** Figure 193, "Firmware Image Download – Command Specific Status Values": Defines the concrete layout or value relationships for Firmware Image Download – Command Specific Status Values. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is Overlapping Range.

#### Where this Figure fits

Figure 193 sits in §5.2.10 and acts as a layout checkpoint. Read it after the report mental model has established the owning object and before software turns Overlapping Range into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a structure or capability field table. Locate it using the structure base and offset, read in byte/bit order, and separate capability gates, value encoding, and reserved areas. Presence in the table does not mean the function is supported.

#### Teaching redraw

```text
[Locate source: Overlapping Range]
          ↓
[Extract field: evidence] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `Overlapping Range` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §5.2.10 is the applicable context.
2. Decode Overlapping Range at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check the cited condition as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 193 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §5.2.10 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes Overlapping Range, the cited condition, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §5.2.10, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 193. Annotate the bytes containing Overlapping Range, decode them, and independently verify the cited condition. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of Overlapping Range in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand Overlapping Range and state its unit or object scope?
2. Can the reader explain why the cited condition is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** Overlapping Range

**Source keyword index:** `may`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.10, Figure 193, printed pages 206, PDF pages 232

</details>

<details markdown="1">
<summary><strong>Figure 203: Get Log Page – Data Pointer</strong></summary>

<!-- claim:BASEFWLOG-FIG-203-CLAIM figure-table:BASEFWLOG-FIG-203 -->

**SPEC.** Figure 203, "Get Log Page – Data Pointer": Defines how Get Log Page – Data Pointer identifies the destination or source buffer for this command. Resolve pointer type and address before checking transfer length and alignment. Evidence index: DPTR.

#### Where this Figure fits

Figure 203 sits in §5.2.13 and acts as a command checkpoint. Read it after the report mental model has established the owning object and before software turns DPTR into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a command-construction field table. Build the common SQE, locate the specified CDW, encode each bit range, clear reserved bits, and validate the result against transfer length, buffer, and completion status. Equal field names do not imply equal semantics across commands.

#### Teaching redraw

```text
[Locate source: DPTR]
          ↓
[Extract field: evidence] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `DPTR` | Data Pointer, the SQE field identifying a command data buffer. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §5.2.13 is the applicable context.
2. Decode DPTR at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check the cited condition as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 203 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §5.2.13 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes DPTR, the cited condition, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §5.2.13, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 203. Annotate the bytes containing DPTR, decode them, and independently verify the cited condition. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of DPTR in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand DPTR and state its unit or object scope?
2. Can the reader explain why the cited condition is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** DPTR

**Source keyword index:** none

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13, Figure 203, printed pages 213, PDF pages 239

</details>

<details markdown="1">
<summary><strong>Figure 204: Get Log Page – Command Dword 10</strong></summary>

<!-- claim:BASEFWLOG-FIG-204-CLAIM figure-table:BASEFWLOG-FIG-204 -->

**SPEC.** Figure 204, "Get Log Page – Command Dword 10": Defines the returned log-page layout and selection context for Get Log Page – Command Dword 10. Start with the fixed header and scope, validate counts or lengths, then walk entries or data areas in order. Evidence index: NUMDL, RAE, LSP, LID.

#### Where this Figure fits

Figure 204 sits in §5.2.13 and acts as a command checkpoint. Read it after the report mental model has established the owning object and before software turns NUMDL into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a command-construction field table. Build the common SQE, locate the specified CDW, encode each bit range, clear reserved bits, and validate the result against transfer length, buffer, and completion status. Equal field names do not imply equal semantics across commands.

#### Teaching redraw

```text
[Locate source: NUMDL]
          ↓
[Extract field: RAE] → [Apply encoding: LSP]
                                      ↓
[Validate evidence: LID]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `NUMDL` | Number of Dwords Lower, the low 16 bits of Get Log Page NUMD. |
| `RAE` | Retain Asynchronous Event, the Get Log Page selector controlling retention of a related asynchronous event. |
| `LSP` | Log Specific Field, a command selector whose meaning is defined by the selected log page. |
| `LID` | Log Page Identifier, the Get Log Page field selecting a log page. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §5.2.13 is the applicable context.
2. Decode NUMDL at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check RAE as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 204 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §5.2.13 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes NUMDL, RAE, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §5.2.13, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 204. Annotate the bytes containing NUMDL, decode them, and independently verify RAE. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of NUMDL in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand NUMDL and state its unit or object scope?
2. Can the reader explain why RAE is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** NUMDL, RAE, LSP, LID

**Source keyword index:** `shall`, `should`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13, Figure 204, printed pages 213, PDF pages 239

</details>

<details markdown="1">
<summary><strong>Figure 205: Get Log Page – Command Dword 11</strong></summary>

<!-- claim:BASEFWLOG-FIG-205-CLAIM figure-table:BASEFWLOG-FIG-205 -->

**SPEC.** Figure 205, "Get Log Page – Command Dword 11": Defines the returned log-page layout and selection context for Get Log Page – Command Dword 11. Start with the fixed header and scope, validate counts or lengths, then walk entries or data areas in order. Evidence index: LSI, NUMDU.

#### Where this Figure fits

Figure 205 sits in §5.2.13 and acts as a command checkpoint. Read it after the report mental model has established the owning object and before software turns LSI into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a command-construction field table. Build the common SQE, locate the specified CDW, encode each bit range, clear reserved bits, and validate the result against transfer length, buffer, and completion status. Equal field names do not imply equal semantics across commands.

#### Teaching redraw

```text
[Locate source: LSI]
          ↓
[Extract field: NUMDU] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `LSI` | Log Specific Identifier, an identifier whose meaning is defined by the selected log page. |
| `NUMDU` | Number of Dwords Upper, the high 16 bits of Get Log Page NUMD. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §5.2.13 is the applicable context.
2. Decode LSI at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check NUMDU as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 205 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §5.2.13 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes LSI, NUMDU, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §5.2.13, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 205. Annotate the bytes containing LSI, decode them, and independently verify NUMDU. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of LSI in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand LSI and state its unit or object scope?
2. Can the reader explain why NUMDU is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** LSI, NUMDU

**Source keyword index:** `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13, Figure 205, printed pages 214, PDF pages 240

</details>

<details markdown="1">
<summary><strong>Figure 206: Get Log Page – Command Dword 12</strong></summary>

<!-- claim:BASEFWLOG-FIG-206-CLAIM figure-table:BASEFWLOG-FIG-206 -->

**SPEC.** Figure 206, "Get Log Page – Command Dword 12": Defines the returned log-page layout and selection context for Get Log Page – Command Dword 12. Start with the fixed header and scope, validate counts or lengths, then walk entries or data areas in order. Evidence index: LPOL, OT.

#### Where this Figure fits

Figure 206 sits in §5.2.13 and acts as a command checkpoint. Read it after the report mental model has established the owning object and before software turns LPOL into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a command-construction field table. Build the common SQE, locate the specified CDW, encode each bit range, clear reserved bits, and validate the result against transfer length, buffer, and completion status. Equal field names do not imply equal semantics across commands.

#### Teaching redraw

```text
[Locate source: LPOL]
          ↓
[Extract field: OT] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `LPOL` | Log Page Offset Lower, the low 32 bits of the Get Log Page byte offset. |
| `OT` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §5.2.13 is the applicable context.
2. Decode LPOL at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check OT as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 206 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §5.2.13 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes LPOL, OT, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §5.2.13, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 206. Annotate the bytes containing LPOL, decode them, and independently verify OT. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of LPOL in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand LPOL and state its unit or object scope?
2. Can the reader explain why OT is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** LPOL, OT

**Source keyword index:** `shall`, `may`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13, Figure 206, printed pages 214, PDF pages 240

</details>

<details markdown="1">
<summary><strong>Figure 207: Get Log Page – Command Dword 13</strong></summary>

<!-- claim:BASEFWLOG-FIG-207-CLAIM figure-table:BASEFWLOG-FIG-207 -->

**SPEC.** Figure 207, "Get Log Page – Command Dword 13": Defines the returned log-page layout and selection context for Get Log Page – Command Dword 13. Start with the fixed header and scope, validate counts or lengths, then walk entries or data areas in order. Evidence index: LPOU.

#### Where this Figure fits

Figure 207 sits in §5.2.13 and acts as a command checkpoint. Read it after the report mental model has established the owning object and before software turns LPOU into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a command-construction field table. Build the common SQE, locate the specified CDW, encode each bit range, clear reserved bits, and validate the result against transfer length, buffer, and completion status. Equal field names do not imply equal semantics across commands.

#### Teaching redraw

```text
[Locate source: LPOU]
          ↓
[Extract field: evidence] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `LPOU` | Log Page Offset Upper, the high 32 bits of the Get Log Page byte offset. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §5.2.13 is the applicable context.
2. Decode LPOU at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check the cited condition as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 207 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §5.2.13 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes LPOU, the cited condition, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §5.2.13, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 207. Annotate the bytes containing LPOU, decode them, and independently verify the cited condition. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of LPOU in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand LPOU and state its unit or object scope?
2. Can the reader explain why the cited condition is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** LPOU

**Source keyword index:** none

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13, Figure 207, printed pages 214, PDF pages 240

</details>

<details markdown="1">
<summary><strong>Figure 208: Get Log Page – Command Dword 14</strong></summary>

<!-- claim:BASEFWLOG-FIG-208-CLAIM figure-table:BASEFWLOG-FIG-208 -->

**SPEC.** Figure 208, "Get Log Page – Command Dword 14": Defines the returned log-page layout and selection context for Get Log Page – Command Dword 14. Start with the fixed header and scope, validate counts or lengths, then walk entries or data areas in order. Evidence index: CSI, OT, UIDX.

#### Where this Figure fits

Figure 208 sits in §5.2.13 and acts as a command checkpoint. Read it after the report mental model has established the owning object and before software turns CSI into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a command-construction field table. Build the common SQE, locate the specified CDW, encode each bit range, clear reserved bits, and validate the result against transfer length, buffer, and completion status. Equal field names do not imply equal semantics across commands.

#### Teaching redraw

```text
[Locate source: CSI]
          ↓
[Extract field: OT] → [Apply encoding: UIDX]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `CSI` | Command Set Identifier, the command-set context associated with a log page. |
| `OT` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `UIDX` | UUID Index, an index into the UUID List; zero indicates that no UUID is specified. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §5.2.13 is the applicable context.
2. Decode CSI at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check OT as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 208 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §5.2.13 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes CSI, OT, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §5.2.13, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 208. Annotate the bytes containing CSI, decode them, and independently verify OT. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of CSI in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand CSI and state its unit or object scope?
2. Can the reader explain why OT is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** CSI, OT, UIDX

**Source keyword index:** `shall`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13, Figure 208, printed pages 214-215, PDF pages 240-241

</details>

<details markdown="1">
<summary><strong>Figure 209: Get Log Page – Log Page Identifiers</strong></summary>

<!-- claim:BASEFWLOG-FIG-209-CLAIM figure-table:BASEFWLOG-FIG-209 -->

**SPEC.** Figure 209, "Get Log Page – Log Page Identifiers": Defines the returned log-page layout and selection context for Get Log Page – Log Page Identifiers. Start with the fixed header and scope, validate counts or lengths, then walk entries or data areas in order. Evidence index: LID 03h, CSI = N, Domain / NVM subsystem, Firmware Slot Information, §5.2.13.1.4, MDS.

#### Where this Figure fits

Figure 209 sits in §5.2.13 and acts as a identifier checkpoint. Read it after the report mental model has established the owning object and before software turns LID 03h into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is an identifier-format Figure. Record width and encoding, then identify assignment authority, uniqueness scope, reserved values, and lifetime. Equal-width identifiers are not automatically interchangeable.

#### Teaching redraw

```text
[Locate source: LID 03h]
          ↓
[Extract field: CSI = N] → [Apply encoding: Domain / NVM subsystem]
                                      ↓
[Validate evidence: Firmware Slot Information]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `LID 03h` | Identifier 03h for the Firmware Slot Information log page. |
| `CSI = N` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `Domain / NVM subsystem` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `Firmware Slot Information` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `§5.2.13.1.4` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `MDS` | Multiple Domain Subsystem, the capability bit indicating whether an NVM subsystem contains multiple domains. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §5.2.13 is the applicable context.
2. Decode LID 03h at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check CSI = N as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 209 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §5.2.13 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes LID 03h, CSI = N, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §5.2.13, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 209. Annotate the bytes containing LID 03h, decode them, and independently verify CSI = N. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of LID 03h in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand LID 03h and state its unit or object scope?
2. Can the reader explain why CSI = N is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** LID 03h, CSI = N, Domain / NVM subsystem, Firmware Slot Information, §5.2.13.1.4, MDS

**Source keyword index:** `may`, `optional`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13, Figure 209, printed pages 215-216, PDF pages 241-242

</details>

<details markdown="1">
<summary><strong>Figure 215: Firmware Slot Information Log Page</strong></summary>

<!-- claim:BASEFWLOG-FIG-215-CLAIM figure-table:BASEFWLOG-FIG-215 -->

**SPEC.** Figure 215, "Firmware Slot Information Log Page": Defines the returned log-page layout and selection context for Firmware Slot Information Log Page. Start with the fixed header and scope, validate counts or lengths, then walk entries or data areas in order. Evidence index: AFI, NAFS, CAFS, FRS1, FRS2, FRS3, FRS4, FRS5, FRS6, FRS7, Reserved bytes 1:7 and 64:511.

#### Where this Figure fits

Figure 215 sits in §5.2.13.1.4 and acts as a layout checkpoint. Read it after the report mental model has established the owning object and before software turns AFI into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a structure or capability field table. Locate it using the structure base and offset, read in byte/bit order, and separate capability gates, value encoding, and reserved areas. Presence in the table does not mean the function is supported.

#### Teaching redraw

```text
[Locate source: AFI]
          ↓
[Extract field: NAFS] → [Apply encoding: CAFS]
                                      ↓
[Validate evidence: FRS1]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `AFI` | Active Firmware Info, the LID 03h byte containing the current active slot and the slot scheduled for the next reset. |
| `NAFS` | Next Active Firmware Slot, AFI bits 6:4 identifying the slot scheduled for the next reset; zero means none is scheduled. |
| `CAFS` | Current Active Firmware Slot, the low three AFI bits identifying the currently executing firmware slot. |
| `FRS1` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `FRS2` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `FRS3` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §5.2.13.1.4 is the applicable context.
2. Decode AFI at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check NAFS as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 215 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §5.2.13.1.4 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes AFI, NAFS, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §5.2.13.1.4, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 215. Annotate the bytes containing AFI, decode them, and independently verify NAFS. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of AFI in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand AFI and state its unit or object scope?
2. Can the reader explain why NAFS is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** AFI, NAFS, CAFS, FRS1, FRS2, FRS3, FRS4, FRS5, FRS6, FRS7, Reserved bytes 1:7 and 64:511

**Source keyword index:** `shall`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.4, Figure 215, printed pages 226, PDF pages 252

</details>

<details markdown="1">
<summary><strong>Figure 93: Common Command Format</strong></summary>

<!-- claim:BASEFWLOG-FIG-093-CLAIM figure-table:BASEFWLOG-FIG-093 -->

**SPEC.** Figure 93, "Common Command Format": Defines the concrete layout or value relationships for Common Command Format. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is DPTR, PRP1, PRP2, SGL1.

#### Where this Figure fits

Figure 93 sits in §4.1.1 and acts as a command checkpoint. Read it after the report mental model has established the owning object and before software turns DPTR into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a command-construction field table. Build the common SQE, locate the specified CDW, encode each bit range, clear reserved bits, and validate the result against transfer length, buffer, and completion status. Equal field names do not imply equal semantics across commands.

#### Teaching redraw

```text
[Locate source: DPTR]
          ↓
[Extract field: PRP1] → [Apply encoding: PRP2]
                                      ↓
[Validate evidence: SGL1]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `DPTR` | Data Pointer, the SQE field identifying a command data buffer. |
| `PRP1` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `PRP2` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `SGL1` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §4.1.1 is the applicable context.
2. Decode DPTR at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check PRP1 as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
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
| It answers | How the cited section organizes DPTR, PRP1, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §4.1.1, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 93. Annotate the bytes containing DPTR, decode them, and independently verify PRP1. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of DPTR in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand DPTR and state its unit or object scope?
2. Can the reader explain why PRP1 is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** DPTR, PRP1, PRP2, SGL1

**Source keyword index:** `shall`, `may`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §4.1.1, Figure 93, printed pages 140-142, PDF pages 166-168

</details>

<details markdown="1">
<summary><strong>Figure 155: Asynchronous Event Information – Notice</strong></summary>

<!-- claim:BASEFWLOG-FIG-155-CLAIM figure-table:BASEFWLOG-FIG-155 -->

**SPEC.** Figure 155, "Asynchronous Event Information – Notice": Defines the event record, event taxonomy, or logging condition represented by Asynchronous Event Information – Notice. Resolve event type and record length before decoding event-specific data. Evidence index: Firmware Activation Starting, CSTS.PP, Firmware Slot Information, RAE.

#### Where this Figure fits

Figure 155 sits in §5.2.2.1 and acts as a layout checkpoint. Read it after the report mental model has established the owning object and before software turns Firmware Activation Starting into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a structure or capability field table. Locate it using the structure base and offset, read in byte/bit order, and separate capability gates, value encoding, and reserved areas. Presence in the table does not mean the function is supported.

#### Teaching redraw

```text
[Locate source: Firmware Activation Starting]
          ↓
[Extract field: CSTS.PP] → [Apply encoding: Firmware Slot Information]
                                      ↓
[Validate evidence: RAE]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `Firmware Activation Starting` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `CSTS.PP` | Controller Status, the property through which a controller reports ready, fatal-status, and shutdown state. Here CSTS.PP selects its PP member field. |
| `Firmware Slot Information` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `RAE` | Retain Asynchronous Event, the Get Log Page selector controlling retention of a related asynchronous event. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §5.2.2.1 is the applicable context.
2. Decode Firmware Activation Starting at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check CSTS.PP as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 155 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §5.2.2.1 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes Firmware Activation Starting, CSTS.PP, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §5.2.2.1, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 155. Annotate the bytes containing Firmware Activation Starting, decode them, and independently verify CSTS.PP. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of Firmware Activation Starting in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand Firmware Activation Starting and state its unit or object scope?
2. Can the reader explain why CSTS.PP is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** Firmware Activation Starting, CSTS.PP, Firmware Slot Information, RAE

**Source keyword index:** `shall not`, `shall`, `may`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.2.1, Figure 155, printed pages 186, PDF pages 212

</details>

<details markdown="1">
<summary><strong>Figure 337: Command Set Identifiers</strong></summary>

<!-- claim:BASEFWLOG-FIG-337-CLAIM figure-table:BASEFWLOG-FIG-337 -->

**SPEC.** Figure 337, "Command Set Identifiers": Defines the identifier composition or namespace of values shown by Command Set Identifiers. Keep the value width, issuing authority, uniqueness scope, and reserved values separate. Evidence index: Command Set Identifier.

#### Where this Figure fits

Figure 337 sits in §5.2.14.1 and acts as a identifier checkpoint. Read it after the report mental model has established the owning object and before software turns Command Set Identifier into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is an identifier-format Figure. Record width and encoding, then identify assignment authority, uniqueness scope, reserved values, and lifetime. Equal-width identifiers are not automatically interchangeable.

#### Teaching redraw

```text
[Locate source: Command Set Identifier]
          ↓
[Extract field: evidence] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `Command Set Identifier` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §5.2.14.1 is the applicable context.
2. Decode Command Set Identifier at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check the cited condition as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 337 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §5.2.14.1 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes Command Set Identifier, the cited condition, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §5.2.14.1, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 337. Annotate the bytes containing Command Set Identifier, decode them, and independently verify the cited condition. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of Command Set Identifier in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand Command Set Identifier and state its unit or object scope?
2. Can the reader explain why the cited condition is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** Command Set Identifier

**Source keyword index:** `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.14.1, Figure 337, printed pages 340, PDF pages 366

</details>

<details markdown="1">
<summary><strong>Figure 338: Identify – Identify Controller Data Structure, I/O Command Set Independent</strong></summary>

<!-- claim:BASEFWLOG-FIG-338-CLAIM figure-table:BASEFWLOG-FIG-338 -->

**SPEC.** Figure 338, "Identify – Identify Controller Data Structure, I/O Command Set Independent": Defines the concrete layout or value relationships for Identify – Identify Controller Data Structure, I/O Command Set Independent. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is FR, MDS, ULIST, SMUD, FAWR, NOFS, FFSRO, MTFA, FWUG, DID, MPTFAWR.

#### Where this Figure fits

Figure 338 sits in §5.2.14.2.1 and acts as a layout checkpoint. Read it after the report mental model has established the owning object and before software turns FR into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a structure or capability field table. Locate it using the structure base and offset, read in byte/bit order, and separate capability gates, value encoding, and reserved areas. Presence in the table does not mean the function is supported.

#### Teaching redraw

```text
[Locate source: FR]
          ↓
[Extract field: MDS] → [Apply encoding: ULIST]
                                      ↓
[Validate evidence: SMUD]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `FR` | Firmware Revision, the eight-byte ASCII Identify Controller field reporting the active firmware revision. |
| `MDS` | Multiple Domain Subsystem, the capability bit indicating whether an NVM subsystem contains multiple domains. |
| `ULIST` | UUID List, the capability bit indicating support for the UUID List data structure. |
| `SMUD` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `FAWR` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `NOFS` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §5.2.14.2.1 is the applicable context.
2. Decode FR at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check MDS as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 338 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §5.2.14.2.1 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes FR, MDS, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §5.2.14.2.1, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 338. Annotate the bytes containing FR, decode them, and independently verify MDS. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of FR in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand FR and state its unit or object scope?
2. Can the reader explain why MDS is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** FR, MDS, ULIST, SMUD, FAWR, NOFS, FFSRO, MTFA, FWUG, DID, MPTFAWR

**Source keyword index:** `shall not`, `shall`, `should`, `may`, `optional`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.14.2.1, Figure 338, printed pages 340-364, PDF pages 366-390

</details>

<details markdown="1">
<summary><strong>Figure 347: UUID List</strong></summary>

<!-- claim:BASEFWLOG-FIG-347-CLAIM figure-table:BASEFWLOG-FIG-347 -->

**SPEC.** Figure 347, "UUID List": Defines the identifier composition or namespace of values shown by UUID List. Keep the value width, issuing authority, uniqueness scope, and reserved values separate. Evidence index: UUID1, UUID2, UUID126, UUID127, NVMe Invalid UUID.

#### Where this Figure fits

Figure 347 sits in §5.2.14.2.14 and acts as a identifier checkpoint. Read it after the report mental model has established the owning object and before software turns UUID1 into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is an identifier-format Figure. Record width and encoding, then identify assignment authority, uniqueness scope, reserved values, and lifetime. Equal-width identifiers are not automatically interchangeable.

#### Teaching redraw

```text
[Locate source: UUID1]
          ↓
[Extract field: UUID2] → [Apply encoding: UUID126]
                                      ↓
[Validate evidence: UUID127]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `UUID1` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `UUID2` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `UUID126` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `UUID127` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `NVMe Invalid UUID` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §5.2.14.2.14 is the applicable context.
2. Decode UUID1 at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check UUID2 as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 347 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §5.2.14.2.14 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes UUID1, UUID2, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §5.2.14.2.14, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 347. Annotate the bytes containing UUID1, decode them, and independently verify UUID2. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of UUID1 in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand UUID1 and state its unit or object scope?
2. Can the reader explain why UUID2 is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** UUID1, UUID2, UUID126, UUID127, NVMe Invalid UUID

**Source keyword index:** `shall`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.14.2.14, Figure 347, printed pages 396, PDF pages 422

</details>

<details markdown="1">
<summary><strong>Figure 348: UUID List Entry</strong></summary>

<!-- claim:BASEFWLOG-FIG-348-CLAIM figure-table:BASEFWLOG-FIG-348 -->

**SPEC.** Figure 348, "UUID List Entry": Defines the identifier composition or namespace of values shown by UUID List Entry. Keep the value width, issuing authority, uniqueness scope, and reserved values separate. Evidence index: ULEH, IDASSOC, UUID.

#### Where this Figure fits

Figure 348 sits in §5.2.14.2.14 and acts as a identifier checkpoint. Read it after the report mental model has established the owning object and before software turns ULEH into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is an identifier-format Figure. Record width and encoding, then identify assignment authority, uniqueness scope, reserved values, and lifetime. Equal-width identifiers are not automatically interchangeable.

#### Teaching redraw

```text
[Locate source: ULEH]
          ↓
[Extract field: IDASSOC] → [Apply encoding: UUID]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `ULEH` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `IDASSOC` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `UUID` | Universally Unique Identifier, a 128-bit identifier whose association scope is defined by the containing structure. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §5.2.14.2.14 is the applicable context.
2. Decode ULEH at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check IDASSOC as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 348 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §5.2.14.2.14 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes ULEH, IDASSOC, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §5.2.14.2.14, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 348. Annotate the bytes containing ULEH, decode them, and independently verify IDASSOC. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of ULEH in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand ULEH and state its unit or object scope?
2. Can the reader explain why IDASSOC is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** ULEH, IDASSOC, UUID

**Source keyword index:** `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.14.2.14, Figure 348, printed pages 396, PDF pages 422

</details>

<details markdown="1">
<summary><strong>Figure 474: Asynchronous Event Configuration – Command Dword 11</strong></summary>

<!-- claim:BASEFWLOG-FIG-474-CLAIM figure-table:BASEFWLOG-FIG-474 -->

**SPEC.** Figure 474, "Asynchronous Event Configuration – Command Dword 11": Defines the event record, event taxonomy, or logging condition represented by Asynchronous Event Configuration – Command Dword 11. Resolve event type and record length before decoding event-specific data. Evidence index: Firmware Activation Notices.

#### Where this Figure fits

Figure 474 sits in §5.2.30.1.6 and acts as a command checkpoint. Read it after the report mental model has established the owning object and before software turns Firmware Activation Notices into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a command-construction field table. Build the common SQE, locate the specified CDW, encode each bit range, clear reserved bits, and validate the result against transfer length, buffer, and completion status. Equal field names do not imply equal semantics across commands.

#### Teaching redraw

```text
[Locate source: Firmware Activation Notices]
          ↓
[Extract field: evidence] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `Firmware Activation Notices` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §5.2.30.1.6 is the applicable context.
2. Decode Firmware Activation Notices at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check the cited condition as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 474 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §5.2.30.1.6 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes Firmware Activation Notices, the cited condition, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §5.2.30.1.6, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 474. Annotate the bytes containing Firmware Activation Notices, decode them, and independently verify the cited condition. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of Firmware Activation Notices in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand Firmware Activation Notices and state its unit or object scope?
2. Can the reader explain why the cited condition is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** Firmware Activation Notices

**Source keyword index:** `shall not`, `shall`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.6, Figure 474, printed pages 466-468, PDF pages 492-494

</details>
