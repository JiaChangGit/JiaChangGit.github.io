---
layout: post
read_time: true
show_date: true
title: "NVMe Base 2.4: Device Self-test and Namespace Management"
date: 2026-09-02
description: "Source-located PCIe/NVMe report for PPT authoring."
lang: en
img: posts/2026/cat_title.jpg
tags: [NVMe, PCIe, Specification]
category: NVMe
author: Jia-Chang
github: JiaChangGit/JiaChangGit.github.io/tree/main/DOCS/nvme-spec-report
toc: yes
---
[繁體中文]({% post_url 2026-09-02-nvme-base-self-test-namespace-management-zh-tw %})


# NVMe Base 2.4: Device Self-test and Namespace Management

Purpose: a source-located engineering report for GitHub Pages and a 100-minute presentation.

Scope: Base §§5.2.6, 5.2.13.1.7 (LID 06h only), 5.2.24, 5.2.25, 8.1.8, and 8.1.17 (excluding §8.1.17.3), plus NVM Command Set 1.3 §§2.1.1, 4.1.4.3, 4.1.6, and 5.8; includes the minimum dependency slice needed for understanding and implementation. Only PCIe/memory-based and common NVMe content appears below.

## Source versions

NVM Express Base Specification, Revision 2.4
NVM Express NVM Command Set Specification, Revision 1.3

Verification date: 2026-09-02. No additional errata, ECNs, Technical Proposals, controller-vendor documents, or source text from the external PCI Express Base Specification are included.

## Reading map

```text
Discover capability and capacity -> Run self-test / construct namespace -> Observe LID 06h / receive NSID -> Attach, verify, detach, or delete
```

The report separates diagnostic and provisioning lifecycles. LID 06h proves the result of a background self-test, while Namespace Management first creates an unattached namespace, then uses a Controller List to establish access and closes verification through events, Identify data, and CQEs.

## Normative language

shall is mandatory, may permits a choice, should expresses a preferred recommendation, and optional means support is not required. The report preserves these terms and never promotes one into another.

## Acronyms first: complete glossary

Every abbreviation below is introduced before it is used in the slide narrative. The term alone is never enough: retain owner, width, unit, scope, and state.

| Acronym / term | Plain-language meaning | Source |
|---|---|---|
| `DST` | Device Self-test, a background operation using diagnostic segments to check a controller and optional namespace media. | NVME-BASE-2.4 Rev. 2.4, §5.2.14.2.1, 8.1.8, printed pp. 353-358, 614, PDF pp. 379-384, 640 |
| `OACS.DSTS` | The Device Self-test Supported bit in Optional Admin Command Support, gating availability of the command. | NVME-BASE-2.4 Rev. 2.4, §5.2.14.2.1, 8.1.8, printed pp. 353-358, 614, PDF pp. 379-384, 640 |
| `STC` | Self-test Code is the Device Self-test CDW10 action nibble; STC in a result entry instead means Status Code and is gated by SCVLD. | NVME-BASE-2.4 Rev. 2.4, §5.2.6, printed pp. 199-200, PDF pp. 225-226 |
| `DSTP` | Device Self-test Parameter, CDW15 with vendor-defined meaning only for vendor-specific STC Eh. | NVME-BASE-2.4 Rev. 2.4, §5.2.6, printed pp. 199-200, PDF pp. 225-226 |
| `DSTO` | Device Self-test Options, the Identify Controller field reporting refresh and concurrency options. | NVME-BASE-2.4 Rev. 2.4, §5.2.14.2.1, 8.1.8, printed pp. 353-358, 614, PDF pp. 379-384, 640 |
| `SDSO` | Single Device Self-test Operation, the bit selecting one subsystem-wide operation or one per controller. | NVME-BASE-2.4 Rev. 2.4, §5.2.14.2.1, 8.1.8, printed pp. 353-358, 614, PDF pp. 379-384, 640 |
| `EDSTT` | Extended Device Self-test Time, the nominal extended-test duration in minutes at power state 0. | NVME-BASE-2.4 Rev. 2.4, §8.1.8.1-8.1.8.2, printed pp. 615-616, PDF pp. 641-642 |
| `LID 06h` | Identifier 06h for the Device Self-test Log Page, containing current operation state and twenty historical results. | NVME-BASE-2.4 Rev. 2.4, §5.2.13, printed pp. 213-216, PDF pp. 239-242 |
| `DSTOS` | Device Self-test Operation Status, the LID 06h nibble identifying the current operation. | NVME-BASE-2.4 Rev. 2.4, §5.2.13.1.7, printed pp. 229-230, PDF pp. 255-256 |
| `DSTCS` | Device Self-test Completion Status, the LID 06h completion percentage from 0 through 100. | NVME-BASE-2.4 Rev. 2.4, §5.2.13.1.7, printed pp. 229-230, PDF pp. 255-256 |
| `DSTR` | Device Self-test Result, the result-entry nibble identifying success, abort, or segment failure. | NVME-BASE-2.4 Rev. 2.4, §5.2.13.1.7, printed pp. 229-232, PDF pp. 255-258 |
| `SEGN` | Segment Number, identifying the first failed diagnostic segment only when DSTR is 7h. | NVME-BASE-2.4 Rev. 2.4, §5.2.13.1.7, printed pp. 229-232, PDF pp. 255-258 |
| `VDINFO` | Valid Diagnostic Information, the bitmap independently gating NSID, FLBA, SCT, and SC. | NVME-BASE-2.4 Rev. 2.4, §5.2.13.1.7, printed pp. 231-232, PDF pp. 257-258 |
| `FVLD` | Failing LBA Valid, the validity bit determining whether FLBA may be interpreted. | NVME-NVM-CS-1.3 Rev. 1.3, §4.1.4.3, printed pp. 76, PDF pp. 76 |
| `FLBA` | Failing LBA, defined by the NVM Command Set as one logical block address that caused self-test failure. | NVME-NVM-CS-1.3 Rev. 1.3, §4.1.4.3, printed pp. 76, PDF pp. 76 |
| `NSID` | Namespace Identifier, a controller-visible numeric handle for a namespace; the identifier is not the namespace object itself. | NVME-BASE-2.4 Rev. 2.4, §8.1.17, printed pp. 660, PDF pp. 686 |
| `OACS.NMS` | The Namespace Management Supported bit in Optional Admin Command Support; one advertises the complete Manage-plus-Attach capability. | NVME-BASE-2.4 Rev. 2.4, §8.1.17, printed pp. 660, PDF pp. 686 |
| `NSZE` | Namespace Size, the total logical-block count whose LBA range is zero through NSZE minus one. | NVME-NVM-CS-1.3 Rev. 1.3, §2.1.1, printed pp. 13-14, PDF pp. 13-14 |
| `NCAP` | Namespace Capacity, the maximum logical blocks that may be allocated to the namespace at any time. | NVME-NVM-CS-1.3 Rev. 1.3, §2.1.1, printed pp. 13-14, PDF pp. 13-14 |
| `NUSE` | Namespace Utilization, the logical blocks currently allocated in the namespace. | NVME-NVM-CS-1.3 Rev. 1.3, §2.1.1, printed pp. 13-14, PDF pp. 13-14 |
| `THINP` | Thin Provisioning, the NSFEAT bit governing whether NCAP may be below NSZE and whether the controller tracks NUSE. | NVME-NVM-CS-1.3 Rev. 1.3, §2.1.1, printed pp. 13, PDF pp. 13 |
| `CNS` | Controller or Namespace Structure, the Identify-command field selecting which data structure is returned. | NVME-BASE-2.4 Rev. 2.4, §8.1.17.1, printed pp. 661-662, PDF pp. 687-688 |
| `DPTR` | Data Pointer, the SQE field identifying a command data buffer. | NVME-BASE-2.4 Rev. 2.4, §5.2.25, printed pp. 446-448, PDF pp. 472-474 |
| `PRP` | Physical Region Page, a pointer format describing a host-addressable data buffer in memory-page units. | NVME-BASE-2.4 Rev. 2.4, §5.2.24, printed pp. 444-445, PDF pp. 470-471 |
| `SEL` | Select; the Namespace Management create/delete/restore selector, distinct from Get Features SEL. | NVME-BASE-2.4 Rev. 2.4, §5.2.25, printed pp. 446-448, PDF pp. 472-474 |
| `CSI` | Command Set Identifier, selecting the I/O Command Set context for a command or log page. | NVME-BASE-2.4 Rev. 2.4, §5.2.25, printed pp. 446-448, PDF pp. 472-474 |
| `SIOCS` | Specified I/O Command Set, the Base create-buffer region at bytes 0:511 containing fields for the selected I/O Command Set. | NVME-BASE-2.4 Rev. 2.4, §5.2.25, printed pp. 446-448, PDF pp. 472-474 |
| `FLBAS` | Formatted LBA Size, selecting the LBA format used by a namespace and related metadata-placement control. | NVME-NVM-CS-1.3 Rev. 1.3, §4.1.6.4, printed pp. 111-113, PDF pp. 111-113 |
| `DPS` | End-to-end Data Protection Type Settings, the create field selecting Protection Information type and position. | NVME-NVM-CS-1.3 Rev. 1.3, §4.1.6.2, printed pp. 110, PDF pp. 110 |
| `NMIC` | Namespace Multi-path I/O and Namespace Sharing Capabilities, the create field declaring namespace sharing and multipath properties. | NVME-NVM-CS-1.3 Rev. 1.3, §4.1.6.4, printed pp. 111-113, PDF pp. 111-113 |
| `ANAGRPID` | ANA Group Identifier, identifying the Asymmetric Namespace Access group for a namespace; zero at create lets the controller choose. | NVME-NVM-CS-1.3 Rev. 1.3, §4.1.6.4, printed pp. 111-113, PDF pp. 111-113 |
| `NVMSETID` | NVM Set Identifier, selecting the NVM Set from which capacity is allocated when creating a namespace. | NVME-BASE-2.4 Rev. 2.4, §8.1.17, printed pp. 661, PDF pp. 687 |
| `ENDGID` | Endurance Group Identifier, selecting the Endurance Group for a created namespace. | NVME-BASE-2.4 Rev. 2.4, §8.1.17, printed pp. 661, PDF pp. 687 |
| `LBSTM` | Logical Block Storage Tag Mask, the 64-bit create field selecting Storage Tag bits to mask. | NVME-NVM-CS-1.3 Rev. 1.3, §4.1.6.2, printed pp. 110, PDF pp. 110 |
| `FDP` | Flexible Data Placement, a capability connecting data-placement hints with media-reclamation management. | NVME-NVM-CS-1.3 Rev. 1.3, §4.1.6.3, printed pp. 110-111, PDF pp. 110-111 |
| `NPHNDLS` | Number of Placement Handles, the entry count for the Placement Handle List in the NVM create payload, with a maximum of 128. | NVME-NVM-CS-1.3 Rev. 1.3, §4.1.6.3, printed pp. 110-111, PDF pp. 110-111 |
| `NSG` | Namespace Size Granularity, the controller's preferred NSZE allocation granularity in bytes. | NVME-NVM-CS-1.3 Rev. 1.3, §5.8, printed pp. 165, PDF pp. 165 |
| `NCG` | Namespace Capacity Granularity, the controller's preferred NCAP allocation granularity in bytes. | NVME-NVM-CS-1.3 Rev. 1.3, §5.8, printed pp. 165, PDF pp. 165 |
| `MAXDNA` | Maximum Domain Namespace Attachments, limiting the aggregate attachment count across I/O controllers in a Domain. | NVME-BASE-2.4 Rev. 2.4, §5.2.24, printed pp. 444-445, PDF pp. 470-471 |
| `MAXCNA` | Maximum I/O Controller Namespace Attachments, limiting the namespaces attached to one I/O controller. | NVME-BASE-2.4 Rev. 2.4, §5.2.24, printed pp. 444-445, PDF pp. 470-471 |
| `RDNCS` | Restore Default Namespace Configuration Supported, the capability bit advertising the Restore Default operation. | NVME-BASE-2.4 Rev. 2.4, §5.2.25.1, printed pp. 447-448, PDF pp. 473-474 |
| `DNCS` | Default Namespace Configuration Status, indicating whether the namespace configuration matches the active firmware image defaults. | NVME-BASE-2.4 Rev. 2.4, §5.2.25.1, printed pp. 447-448, PDF pp. 473-474 |
| `CQE` | Completion Queue Entry, one completion-result structure in a CQ. | NVME-BASE-2.4 Rev. 2.4, §5.2.25, 8.1.17.1, printed pp. 446-448, 662, PDF pp. 472-474, 688 |
| `AER (Admin)` | Asynchronous Event Request, a host-posted Admin command whose CQE delivers events such as namespace attribute changes. | NVME-BASE-2.4 Rev. 2.4, §8.1.17.1-8.1.17.2, printed pp. 662-663, PDF pp. 688-689 |
| `AEN` | Asynchronous Event Notification, a notification delivered through a submitted Asynchronous Event Request. | NVME-BASE-2.4 Rev. 2.4, §8.1.17.1-8.1.17.2, printed pp. 662-663, PDF pp. 688-689 |

## Visual atlas: locate the system before reading fields

Each redraw answers a different question: architecture locates components, sequence shows ownership, decode turns bits into engineering values, and state views preserve failure evidence. These are teaching redraws, not copies of specification artwork.

### Visual 01: Separate two lifecycles: diagnostic evidence and namespace provisioning

**View type:** `architecture`

```text
[Capability snapshot]
  ├─ [Self-test operation]
  ├─ [LID 06h evidence]
  ├─ [Namespace create]
  ├─ [Attach relationship]
  └─ [Identify/event verification]
```

**Question answered:** Device Self-test and Namespace Management both use Admin commands but mutate different objects. Self-test creates a background operation: its command CQE is only an acceptance point and LID 06h proves the outcome. Namespace Management creates or removes a namespace object: Create returns an NSID, but Attachment is still required to establish controller access. Separating the tracks explains why completion is not always the endpoint.

**Supporting Figures:** Figure 93, Figure 176, Figure 218, Figure 445, Figure 450, Figure 155

**Sources:** NVME-BASE-2.4 Rev. 2.4, §5.2.6, printed pp. 201, PDF pp. 227; NVME-BASE-2.4 Rev. 2.4, §8.1.17, printed pp. 660, PDF pp. 686; NVME-BASE-2.4 Rev. 2.4, §5.2.25, 8.1.17.1, printed pp. 446-448, 662, PDF pp. 472-474, 688

### Visual 02: Device Self-test: from capability gate to an LID 06h result

**View type:** `state`

```text
[OACS.DSTS gate] → [Choose NSID + STC] → [Admin CQE: start accepted] → [Poll DSTOS/DSTCS] → [Create RDS1] → [VDINFO gate + FLBA]
timeout / failure ──→ preserve trigger + previous state + evidence
```

**Question answered:** Use OACS.DSTS, EDSTT, and DSTO.SDSO to establish support, timing, and concurrency expectations before constructing the command from NSID and STC. After the CQE, poll DSTOS/DSTCS. At operation end, RDS1 is created before current status is cleared, preventing software from losing the final result during a transition window.

**Supporting Figures:** Figure 176, Figure 177, Figure 178, Figure 179, Figure 180, Figure 203, Figure 204, Figure 205, Figure 206, Figure 207, Figure 208, Figure 209, Figure 218, Figure 219, Figure 111, Figure 700, Figure 701

**Sources:** NVME-BASE-2.4 Rev. 2.4, §5.2.14.2.1, 8.1.8, printed pp. 353-358, 614, PDF pp. 379-384, 640; NVME-BASE-2.4 Rev. 2.4, §5.2.6, printed pp. 199, PDF pp. 225; NVME-BASE-2.4 Rev. 2.4, §5.2.6, printed pp. 199-200, PDF pp. 225-226; NVME-BASE-2.4 Rev. 2.4, §5.2.13.1.7, printed pp. 229-230, PDF pp. 255-256; NVME-BASE-2.4 Rev. 2.4, §5.2.13.1.7, printed pp. 229-232, PDF pp. 255-258; NVME-BASE-2.4 Rev. 2.4, §5.2.13.1.7, printed pp. 231-232, PDF pp. 257-258; NVME-NVM-CS-1.3 Rev. 1.3, §4.1.4.3, printed pp. 76, PDF pp. 76

### Visual 03: Put three capacity values and two granularities into one byte model

**View type:** `decode`

```text
[RAW: Read LBA format] → [LOCATE: NSZE/NCAP/NUSE blocks] → [DECODE: Multiply by LBA bytes]
[VALIDATE: Check NSG/NCG divisibility] → [APPLY: Estimate allocation rounding] → [EVIDENCE: Record addressable and consumed]
VALIDATE fail ──→ return to RAW evidence
```

**Question answered:** NSZE, NCAP, and NUSE use logical blocks; NSG and NCG use bytes; and actual NVM consumption may be rounded to an allocation unit. Convert with the selected LBA size before comparing. NSZE≥NCAP≥NUSE is a capacity relationship, while NSG/NCG divisibility is a waste-minimization hint, not the same kind of gate.

**Supporting Figures:** Figure 123, Figure 132, Figure 133

**Sources:** NVME-NVM-CS-1.3 Rev. 1.3, §2.1.1, printed pp. 13-14, PDF pp. 13-14; NVME-NVM-CS-1.3 Rev. 1.3, §2.1.1, printed pp. 13, PDF pp. 13; NVME-BASE-2.4 Rev. 2.4, §8.1.17, printed pp. 661, PDF pp. 687; NVME-NVM-CS-1.3 Rev. 1.3, §5.8, printed pp. 165, PDF pp. 165; NVME-NVM-CS-1.3 Rev. 1.3, §5.8, printed pp. 165, PDF pp. 165

### Visual 04: Create payload: the Base envelope contains 512 NVM-specific bytes

**View type:** `decode`

```text
[RAW: SEL=Create, CSI=00h] → [LOCATE: Allocate zeroed 4096-byte buffer] → [DECODE: Fill NSZE/NCAP/FLBAS]
[VALIDATE: Fill DPS/NMIC/group IDs] → [APPLY: Validate LBSTM/NPHNDLS] → [EVIDENCE: DPTR + SQE snapshot]
VALIDATE fail ──→ return to RAW evidence
```

**Question answered:** Base Figure 448 defines a 4096-byte envelope, while NVM Command Set Figure 134 defines NVM fields and the Placement Handle List within the first 768 bytes. The host selects operation and command set through SEL/CSI, then fills NSZE, NCAP, format, protection, sharing, and group identifiers. Reserved regions are zeroed, while Protection Information and FDP have separate capability gates.

**Supporting Figures:** Figure 36, Figure 93, Figure 127, Figure 134, Figure 445, Figure 446, Figure 447, Figure 448

**Sources:** NVME-BASE-2.4 Rev. 2.4, §5.2.25, printed pp. 446-448, PDF pp. 472-474; NVME-NVM-CS-1.3 Rev. 1.3, §4.1.6.4, printed pp. 111-113, PDF pp. 111-113; NVME-NVM-CS-1.3 Rev. 1.3, §4.1.6.2, printed pp. 110, PDF pp. 110; NVME-NVM-CS-1.3 Rev. 1.3, §4.1.6.3, printed pp. 110-111, PDF pp. 110-111; NVME-BASE-2.4 Rev. 2.4, §8.1.17, printed pp. 661, PDF pp. 687

### Visual 05: Namespace lifecycle: Create builds the object; Attach establishes access

**View type:** `state`

```text
[Unallocated NSID] → [Create→allocated/unattached] → [Preserve CQE DW0 NSID] → [Attach→active on controller] → [Detach→inactive on controller] → [Delete→unallocated]
timeout / failure ──→ preserve trigger + previous state + evidence
```

**Question answered:** Create, Attach, Detach, and Delete change two dimensions: whether the namespace is allocated and whether a controller is attached. After Create returns NSID in CQE DW0, the object is allocated but no controller is attached. A Controller List in Attach establishes access. Detach preserves capacity, while Delete makes the NSID unallocated.

**Supporting Figures:** Figure 139, Figure 338, Figure 442, Figure 443, Figure 444, Figure 450

**Sources:** NVME-BASE-2.4 Rev. 2.4, §8.1.17, printed pp. 660, PDF pp. 686; NVME-BASE-2.4 Rev. 2.4, §8.1.17, printed pp. 660, PDF pp. 686; NVME-BASE-2.4 Rev. 2.4, §5.2.24, printed pp. 444-445, PDF pp. 470-471; NVME-BASE-2.4 Rev. 2.4, §5.2.24, printed pp. 444-445, PDF pp. 470-471; NVME-BASE-2.4 Rev. 2.4, §5.2.25, 8.1.17.1, printed pp. 446-448, 662, PDF pp. 472-474, 688

### Visual 06: Delete and Restore Default: empty inventory before crossing the configuration boundary

**View type:** `state`

```text
[Detach every controller] → [Delete NSID or FFFFFFFFh] → [Confirm empty Allocated list] → [RDNCS=1 gate] → [SEL=2h Restore] → [DNCS=1 + refresh Identify]
timeout / failure ──→ preserve trigger + previous state + evidence
```

**Question answered:** Delete All and Restore Default are different operations. Delete with NSID FFFFFFFFh succeeds even when no namespaces exist. Restore Default requires RDNCS, SEL 2h, and an empty subsystem inventory. Before successful completion, the controller applies defaults for the current active firmware image and sets DNCS to one.

**Supporting Figures:** Figure 304, Figure 338, Figure 446, Figure 449, Figure 474

**Sources:** NVME-BASE-2.4 Rev. 2.4, §5.2.25, 8.1.17.1, printed pp. 446, 448, 662, PDF pp. 472, 474, 688; NVME-BASE-2.4 Rev. 2.4, §5.2.25.1, printed pp. 447-448, PDF pp. 473-474; NVME-BASE-2.4 Rev. 2.4, §8.1.17.1-8.1.17.2, printed pp. 662-663, PDF pp. 688-689

### Visual 07: Namespace events say inventory changed; Identify says what it became

**View type:** `sequence`

```text
Host / software        Shared object        Controller / evidence
Host → Shared: Host posts AER
Shared → Controller: Create/Attach/Detach/Delete
Controller → Shared: Controller updates inventory
Shared → Host: AEN CQE posted
Host → Shared: Host reissues Identify by CNS
Shared → Controller: Compare before/after lists
```

**Question answered:** Attached and Allocated Namespace Attribute Changed notices correspond to different inventories. Create normally changes the Allocated list, Attach/Detach changes the Active list, and Delete may change both. The event code is not the new list, so the host reissues Identify with the appropriate CNS. Delete reporting also distinguishes the processing controller from other controllers.

**Supporting Figures:** Figure 155, Figure 474

**Sources:** NVME-BASE-2.4 Rev. 2.4, §8.1.17, printed pp. 660, PDF pp. 686; NVME-BASE-2.4 Rev. 2.4, §8.1.17.1-8.1.17.2, printed pp. 662-663, PDF pp. 688-689; NVME-BASE-2.4 Rev. 2.4, §5.2.25, 8.1.17.1, printed pp. 446-448, 662, PDF pp. 472-474, 688

### Visual 08: End to end: place capacity, command, object, attachment, and evidence on one timeline

**View type:** `sequence`

```text
Host / software        Shared object        Controller / evidence
Host → Shared: Capability/capacity snapshot
Shared → Controller: Raw Create SQE + buffer
Controller → Shared: CQE DW0 returned NSID
Shared → Host: Raw Attach SQE + Controller List
Host → Shared: AEN + Identify refresh
Shared → Controller: I/O/detach/delete outcome
```

**Question answered:** A namespace defect is rarely one field in isolation. The pre-create capability snapshot, 4096-byte payload, CQE DW0, Controller List, attachment limits, events, and post-Identify result must all join to one NSID and controller set. Debugging finds the first inconsistent boundary instead of guessing backward from a final I/O failure.

**Supporting Figures:** Figure 123, Figure 127, Figure 134, Figure 139, Figure 338, Figure 442, Figure 443, Figure 444, Figure 445, Figure 446, Figure 447, Figure 448, Figure 449, Figure 450

**Sources:** NVME-BASE-2.4 Rev. 2.4, §5.2.24-5.2.25, printed pp. 445, 448, PDF pp. 471, 474; NVME-BASE-2.4 Rev. 2.4, §5.2.24-5.2.25, 8.1.17.1, printed pp. 444-448, 661-663, PDF pp. 470-474, 687-689; NVME-BASE-2.4 Rev. 2.4, §5.2.24, printed pp. 444-445, PDF pp. 470-471; NVME-NVM-CS-1.3 Rev. 1.3, §4.1.6.2, printed pp. 110, PDF pp. 110; NVME-NVM-CS-1.3 Rev. 1.3, §4.1.6.3, printed pp. 110-111, PDF pp. 110-111

## Mental Model and complete teaching path

The modules follow engineering causality rather than specification-section order. Related Figures return at the point where they support the flow.

### Module 01: Separate two lifecycles: diagnostic evidence and namespace provisioning

**Explanation.** Device Self-test and Namespace Management both use Admin commands but mutate different objects. Self-test creates a background operation: its command CQE is only an acceptance point and LID 06h proves the outcome. Namespace Management creates or removes a namespace object: Create returns an NSID, but Attachment is still required to establish controller access. Separating the tracks explains why completion is not always the endpoint.

```text
Capability snapshot
  ↓
Self-test operation
  ↓
LID 06h evidence
  ↓
Namespace create
  ↓
Attach relationship
  ↓
Identify/event verification
```

#### Comparison

| Item | What it answers | Engineering note |
|---|---|---|
| Self-test object | Background operation | CQE→current state→history result |
| Namespace object | Allocated capacity and format | Create CQE DW0→NSID |
| Access relationship | Namespace-to-controller attachment | Attach CQE→Active NSID list |
| Inventory evidence | Allocated/Active lists | Refresh Identify after AEN |

**Informative example.** A Create completion returning NSID 7 proves that namespace 7 exists, but it is still unattached and cannot immediately receive I/O. Likewise, a successful Self-test start CQE proves only that an operation began, not that the test passed. Each CQE needs later evidence, but the evidence types differ.

**Common mistake / debugging.** Do not summarize the flow as a successful Admin command. A trace labels the object changed, the boundary crossed by success, and the LID, Identify, or event evidence still outstanding.

**Supporting sources:** NVME-BASE-2.4 Rev. 2.4, §5.2.6, printed pp. 201, PDF pp. 227; NVME-BASE-2.4 Rev. 2.4, §8.1.17, printed pp. 660, PDF pp. 686; NVME-BASE-2.4 Rev. 2.4, §5.2.25, 8.1.17.1, printed pp. 446-448, 662, PDF pp. 472-474, 688

**Related Figures:** Figure 93, Figure 176, Figure 218, Figure 445, Figure 450, Figure 155

### Module 02: Device Self-test: from capability gate to an LID 06h result

**Explanation.** Use OACS.DSTS, EDSTT, and DSTO.SDSO to establish support, timing, and concurrency expectations before constructing the command from NSID and STC. After the CQE, poll DSTOS/DSTCS. At operation end, RDS1 is created before current status is cleared, preventing software from losing the final result during a transition window.

```text
OACS.DSTS gate
  ↓
Choose NSID + STC
  ↓
Admin CQE: start accepted
  ↓
Poll DSTOS/DSTCS
  ↓
Create RDS1
  ↓
VDINFO gate + FLBA
```

#### Comparison

| Item | What it answers | Engineering note |
|---|---|---|
| NSID=0 | Controller only | No namespace media |
| Active NSID | One namespace | Separate invalid/inactive status |
| NSID=FFFFFFFFh | Accessible attached set at start | The set is not tracked dynamically |
| STC=Fh | Abort current operation | Write result before clearing current |

**Informative example.** For a complete LID 06h read, 564/4 is 141 dwords and NUMD is 141−1=140=008Ch. With RAE zero, LSP zero, and LID 06h, CDW10 is 008C0006h. If RDS1.DSTS is 17h, DSTC 1h means short and DSTR 7h is the condition that permits reading SEGN.

**Common mistake / debugging.** A nonzero FLBA is not valid evidence. Decode DSTR, check FVLD and NSIDVLD, and only then apply the NVM Command Set meaning for FLBA bytes 23:16. Preserve the raw 28-byte entry.

**Supporting sources:** NVME-BASE-2.4 Rev. 2.4, §5.2.14.2.1, 8.1.8, printed pp. 353-358, 614, PDF pp. 379-384, 640; NVME-BASE-2.4 Rev. 2.4, §5.2.6, printed pp. 199, PDF pp. 225; NVME-BASE-2.4 Rev. 2.4, §5.2.6, printed pp. 199-200, PDF pp. 225-226; NVME-BASE-2.4 Rev. 2.4, §5.2.13.1.7, printed pp. 229-230, PDF pp. 255-256; NVME-BASE-2.4 Rev. 2.4, §5.2.13.1.7, printed pp. 229-232, PDF pp. 255-258; NVME-BASE-2.4 Rev. 2.4, §5.2.13.1.7, printed pp. 231-232, PDF pp. 257-258; NVME-NVM-CS-1.3 Rev. 1.3, §4.1.4.3, printed pp. 76, PDF pp. 76

**Related Figures:** Figure 176, Figure 177, Figure 178, Figure 179, Figure 180, Figure 203, Figure 204, Figure 205, Figure 206, Figure 207, Figure 208, Figure 209, Figure 218, Figure 219, Figure 111, Figure 700, Figure 701

### Module 03: Put three capacity values and two granularities into one byte model

**Explanation.** NSZE, NCAP, and NUSE use logical blocks; NSG and NCG use bytes; and actual NVM consumption may be rounded to an allocation unit. Convert with the selected LBA size before comparing. NSZE≥NCAP≥NUSE is a capacity relationship, while NSG/NCG divisibility is a waste-minimization hint, not the same kind of gate.

```text
Read LBA format
  ↓
NSZE/NCAP/NUSE blocks
  ↓
Multiply by LBA bytes
  ↓
Check NSG/NCG divisibility
  ↓
Estimate allocation rounding
  ↓
Record addressable and consumed
```

#### Comparison

| Item | What it answers | Engineering note |
|---|---|---|
| NSZE | Logical blocks | LBA 0 through NSZE−1 |
| NCAP | Logical blocks | Maximum allocatable capacity |
| NUSE | Logical blocks | Tracked when THINP is one |
| NSG/NCG | Bytes | Preferred hint, not a sole abort gate |

**Informative example.** With 4-KiB LBAs, NSG 1 MiB, and NCG 2 MiB, NSZE=NCAP=1024 represents 4 MiB, is divisible by both hints, and is fully provisioned. NSZE=NCAP=1000 represents 3,906.25 KiB and violates both hints. Allocation capacity may be wasted, but an otherwise valid create is not aborted solely for this reason.

**Common mistake / debugging.** A common error divides NSZE 1024 directly by NSG 1 MiB or treats a granularity violation as Invalid Field. The worksheet lists raw blocks, LBA bytes, converted bytes, remainder, and the controller allocation unit.

**Supporting sources:** NVME-NVM-CS-1.3 Rev. 1.3, §2.1.1, printed pp. 13-14, PDF pp. 13-14; NVME-NVM-CS-1.3 Rev. 1.3, §2.1.1, printed pp. 13, PDF pp. 13; NVME-BASE-2.4 Rev. 2.4, §8.1.17, printed pp. 661, PDF pp. 687; NVME-NVM-CS-1.3 Rev. 1.3, §5.8, printed pp. 165, PDF pp. 165; NVME-NVM-CS-1.3 Rev. 1.3, §5.8, printed pp. 165, PDF pp. 165

**Related Figures:** Figure 123, Figure 132, Figure 133

### Module 04: Create payload: the Base envelope contains 512 NVM-specific bytes

**Explanation.** Base Figure 448 defines a 4096-byte envelope, while NVM Command Set Figure 134 defines NVM fields and the Placement Handle List within the first 768 bytes. The host selects operation and command set through SEL/CSI, then fills NSZE, NCAP, format, protection, sharing, and group identifiers. Reserved regions are zeroed, while Protection Information and FDP have separate capability gates.

```text
SEL=Create, CSI=00h
  ↓
Allocate zeroed 4096-byte buffer
  ↓
Fill NSZE/NCAP/FLBAS
  ↓
Fill DPS/NMIC/group IDs
  ↓
Validate LBSTM/NPHNDLS
  ↓
DPTR + SQE snapshot
```

#### Comparison

| Item | What it answers | Engineering note |
|---|---|---|
| Base 0:511 | SIOCS | NVM-specific create data |
| Base 512:1023 | Reserved | Host clears to zero |
| Base 1024:4095 | Vendor Specific | Do not invent a meaning |
| NVM 512:767 | Placement Handle List | Validated only when FDP is enabled |

**Informative example.** To create a 4-MiB namespace with 4096-byte LBAs, set NSZE and NCAP to 1024, so bytes 7:0 and 15:8 each contain 0000000000000400h. NVMSETID zero with ENDGID five lets the controller select an NVM Set inside Endurance Group five; NVMSETID seven with ENDGID zero is Invalid Field.

**Common mistake / debugging.** Do not dump only Figure 134 values. Debug evidence also retains LBA-format capability, LBAFEE, Figure 127 masking limits, FDP enablement, the complete 4096-byte buffer, and a reserved-byte scan.

**Supporting sources:** NVME-BASE-2.4 Rev. 2.4, §5.2.25, printed pp. 446-448, PDF pp. 472-474; NVME-NVM-CS-1.3 Rev. 1.3, §4.1.6.4, printed pp. 111-113, PDF pp. 111-113; NVME-NVM-CS-1.3 Rev. 1.3, §4.1.6.2, printed pp. 110, PDF pp. 110; NVME-NVM-CS-1.3 Rev. 1.3, §4.1.6.3, printed pp. 110-111, PDF pp. 110-111; NVME-BASE-2.4 Rev. 2.4, §8.1.17, printed pp. 661, PDF pp. 687

**Related Figures:** Figure 36, Figure 93, Figure 127, Figure 134, Figure 445, Figure 446, Figure 447, Figure 448

### Module 05: Namespace lifecycle: Create builds the object; Attach establishes access

**Explanation.** Create, Attach, Detach, and Delete change two dimensions: whether the namespace is allocated and whether a controller is attached. After Create returns NSID in CQE DW0, the object is allocated but no controller is attached. A Controller List in Attach establishes access. Detach preserves capacity, while Delete makes the NSID unallocated.

```text
Unallocated NSID
  ↓
Create→allocated/unattached
  ↓
Preserve CQE DW0 NSID
  ↓
Attach→active on controller
  ↓
Detach→inactive on controller
  ↓
Delete→unallocated
```

#### Comparison

| Item | What it answers | Engineering note |
|---|---|---|
| Create | Object/capacity | Does not attach automatically |
| Attach | Access relationship | Controller List may contain multiple CNTLIDs |
| Detach | Controller-local active state | Namespace remains allocated |
| Delete | Subsystem inventory | NSID becomes unallocated |

**Informative example.** Create returns NSID seven. A Controller List names controllers three and five through NUMCIDS and its entries. After Attach, NSID seven is active on both. Detaching only controller three leaves it inactive there and active on controller five, while the namespace remains allocated.

**Common mistake / debugging.** Equal NSID values do not imply equal active state on every controller. Inventory and I/O traces carry controller ID, while attachment limits separately check Domain MAXDNA and per-controller MAXCNA.

**Supporting sources:** NVME-BASE-2.4 Rev. 2.4, §8.1.17, printed pp. 660, PDF pp. 686; NVME-BASE-2.4 Rev. 2.4, §8.1.17, printed pp. 660, PDF pp. 686; NVME-BASE-2.4 Rev. 2.4, §5.2.24, printed pp. 444-445, PDF pp. 470-471; NVME-BASE-2.4 Rev. 2.4, §5.2.24, printed pp. 444-445, PDF pp. 470-471; NVME-BASE-2.4 Rev. 2.4, §5.2.25, 8.1.17.1, printed pp. 446-448, 662, PDF pp. 472-474, 688

**Related Figures:** Figure 139, Figure 338, Figure 442, Figure 443, Figure 444, Figure 450

### Module 06: Delete and Restore Default: empty inventory before crossing the configuration boundary

**Explanation.** Delete All and Restore Default are different operations. Delete with NSID FFFFFFFFh succeeds even when no namespaces exist. Restore Default requires RDNCS, SEL 2h, and an empty subsystem inventory. Before successful completion, the controller applies defaults for the current active firmware image and sets DNCS to one.

```text
Detach every controller
  ↓
Delete NSID or FFFFFFFFh
  ↓
Confirm empty Allocated list
  ↓
RDNCS=1 gate
  ↓
SEL=2h Restore
  ↓
DNCS=1 + refresh Identify
```

#### Comparison

| Item | What it answers | Engineering note |
|---|---|---|
| Delete one | NSID=target | Object is gone after success |
| Delete all | NSID=FFFFFFFFh | Succeeds with zero namespaces |
| Restore | SEL=2h, NSID ignored | Remaining namespace→Sequence Error |
| Post-condition | DNCS=1 | Refresh Identify for actual defaults |

**Informative example.** Detach NSID seven and delete it, then confirm that the Allocated Namespace ID list is empty. If RDNCS is one, issue SEL 2h with NSID zero. After the successful CQE, read DNCS one and re-enumerate default namespaces. DNCS is state evidence, not a complete description of the default layout.

**Common mistake / debugging.** A Delete All CQE does not prove Restore completion, and DNCS alone does not reveal default NSZE or format. Preserve operation selector, inventory snapshot, CQE, and post-operation Identify at each stage.

**Supporting sources:** NVME-BASE-2.4 Rev. 2.4, §5.2.25, 8.1.17.1, printed pp. 446, 448, 662, PDF pp. 472, 474, 688; NVME-BASE-2.4 Rev. 2.4, §5.2.25.1, printed pp. 447-448, PDF pp. 473-474; NVME-BASE-2.4 Rev. 2.4, §8.1.17.1-8.1.17.2, printed pp. 662-663, PDF pp. 688-689

**Related Figures:** Figure 304, Figure 338, Figure 446, Figure 449, Figure 474

### Module 07: Namespace events say inventory changed; Identify says what it became

**Explanation.** Attached and Allocated Namespace Attribute Changed notices correspond to different inventories. Create normally changes the Allocated list, Attach/Detach changes the Active list, and Delete may change both. The event code is not the new list, so the host reissues Identify with the appropriate CNS. Delete reporting also distinguishes the processing controller from other controllers.

```text
Host posts AER
  ↓
Create/Attach/Detach/Delete
  ↓
Controller updates inventory
  ↓
AEN CQE posted
  ↓
Host reissues Identify by CNS
  ↓
Compare before/after lists
```

#### Comparison

| Item | What it answers | Engineering note |
|---|---|---|
| CNS 02h | Active Namespace ID list | Attached notice |
| CNS 10h | Allocated Namespace ID list | Allocated notice |
| Create | Allocated change | New NSID is not yet active |
| Delete | Allocated and possibly Active | Processing-controller rule differs |

**Informative example.** Controller three processes Delete for attached NSID seven. Other notice-enabled controllers report according to §8.1.17.2, while requirements differ for the processing controller. Instead of counting events alone, the host retains before/after Active and Allocated lists for every controller.

**Common mistake / debugging.** A common mistake treats an AEN as an inventory delta. It triggers refresh; the authoritative data is the subsequent Identify result. Before/after differences may expose a missed event, but software cannot invent a notification that was not received.

**Supporting sources:** NVME-BASE-2.4 Rev. 2.4, §8.1.17, printed pp. 660, PDF pp. 686; NVME-BASE-2.4 Rev. 2.4, §8.1.17.1-8.1.17.2, printed pp. 662-663, PDF pp. 688-689; NVME-BASE-2.4 Rev. 2.4, §5.2.25, 8.1.17.1, printed pp. 446-448, 662, PDF pp. 472-474, 688

**Related Figures:** Figure 155, Figure 474

### Module 08: End to end: place capacity, command, object, attachment, and evidence on one timeline

**Explanation.** A namespace defect is rarely one field in isolation. The pre-create capability snapshot, 4096-byte payload, CQE DW0, Controller List, attachment limits, events, and post-Identify result must all join to one NSID and controller set. Debugging finds the first inconsistent boundary instead of guessing backward from a final I/O failure.

```text
Capability/capacity snapshot
  ↓
Raw Create SQE + buffer
  ↓
CQE DW0 returned NSID
  ↓
Raw Attach SQE + Controller List
  ↓
AEN + Identify refresh
  ↓
I/O/detach/delete outcome
```

#### Comparison

| Item | What it answers | Engineering note |
|---|---|---|
| Create Invalid Format | FLBAS/DPS/LBSTM/LBAFEE | Locate the format gate first |
| Insufficient Capacity | NSZE/NCAP, unallocated bytes, group IDs | Separate logical and consumed |
| Attach limit | MAXDNA/MAXCNA and prior counts | Separate Domain and controller |
| I/O inactive NSID | Attach CQE, Active list, controller ID | Create success is insufficient |

**Informative example.** Case: Create returns NSID seven but Attach returns 27h. Check controller five's MAXCNA and the Domain MAXDNA prior counts. If the per-controller limit is already reached, do not modify the create payload or retry I/O. Recovery selects another controller, detaches another namespace, or stops and reports the capacity policy.

**Common mistake / debugging.** Do not retain only a human-readable status. Preserve SCT/SC/DNR, raw SQE, buffer hash, returned NSID, Controller List, timestamp, and before/after inventories so the rejected gate remains recomputable.

**Supporting sources:** NVME-BASE-2.4 Rev. 2.4, §5.2.24-5.2.25, printed pp. 445, 448, PDF pp. 471, 474; NVME-BASE-2.4 Rev. 2.4, §5.2.24-5.2.25, 8.1.17.1, printed pp. 444-448, 661-663, PDF pp. 470-474, 687-689; NVME-BASE-2.4 Rev. 2.4, §5.2.24, printed pp. 444-445, PDF pp. 470-471; NVME-NVM-CS-1.3 Rev. 1.3, §4.1.6.2, printed pp. 110, PDF pp. 110; NVME-NVM-CS-1.3 Rev. 1.3, §4.1.6.3, printed pp. 110-111, PDF pp. 110-111

**Related Figures:** Figure 123, Figure 127, Figure 134, Figure 139, Figure 338, Figure 442, Figure 443, Figure 444, Figure 445, Figure 446, Figure 447, Figure 448, Figure 449, Figure 450

## Source-located specification findings

The mental model above explains causality. This section preserves each source-located conclusion and its normative strength for speaker notes and review.

### 1. Gate Self-test capability and concurrency scope

<!-- claim:BASENSMGMT-SELFTEST-GATE -->

Before starting Device Self-test, read Identify Controller. OACS.DSTS gates command support, EDSTT gives the nominal extended-operation duration in minutes at power state 0, and DSTO.SDSO selects one subsystem-wide operation versus one operation per controller. They describe support, time, and concurrency scope respectively.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.14.2.1, 8.1.8, printed pages 353-358, 614, PDF pages 379-384, 640

### 2. NSID selects Self-test scope

<!-- claim:BASENSMGMT-SELFTEST-NSID -->

Device Self-test is performed by the controller receiving the command. NSID 00000000h tests only that controller; 00000001h through FFFFFFFEh select one active namespace; and FFFFFFFFh includes all attached namespaces accessible through that controller when the operation starts. Invalid and inactive NSIDs are distinct errors.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.6, printed pages 199, PDF pages 225

### 3. STC and CDW15 command encoding

<!-- claim:BASENSMGMT-SELFTEST-STC -->

CDW10.STC[3:0] selects 1h short, 2h extended, 3h Host-Initiated Refresh, Eh vendor specific, or Fh abort; the other encodings are reserved. CDW15.DSTP is vendor specific only when STC is Eh and is reserved for other STC values.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.6, printed pages 199-200, PDF pages 225-226

### 4. Command matrix while an operation is active

<!-- claim:BASENSMGMT-SELFTEST-INPROGRESS -->

While an operation is active, a new short, extended, or Host-Initiated Refresh request shall be aborted with Device Self-test in Progress. STC Fh instead aborts the current operation, creates the newest result, clears current status, and successfully completes the abort command in that order.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.6, printed pages 200, PDF pages 226

### 5. A CQE is not background-test completion

<!-- claim:BASENSMGMT-SELFTEST-COMPLETION -->

The Device Self-test Admin CQE proves only that the start or abort action was processed; it does not mean that the background test has finished. Software treats the command CQE, current LID 06h state, and final result entry as three distinct timestamps.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.6, printed pages 201, PDF pages 227

### 6. Background-test suspend/resume contract

<!-- claim:BASENSMGMT-SELFTEST-BACKGROUND -->

Device Self-test is background work composed of vendor-specific segments. If processing another command requires suspension, the controller shall suspend the self-test, process and complete that command, and resume the self-test in order. Which commands may run concurrently remains vendor specific.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §8.1.8, printed pages 614, PDF pages 640

### 7. Reset differences between short and extended tests

<!-- claim:BASENSMGMT-SELFTEST-TIMING -->

A short operation should finish within two minutes and is aborted by Controller Level Reset. An extended operation should finish within EDSTT, shall persist across Controller Level Reset and power restoration, and resumes afterward. The two test types do not share one reset expectation.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §8.1.8.1-8.1.8.2, printed pages 615-616, PDF pages 641-642

### 8. Format, sanitize, and abort conditions

<!-- claim:BASENSMGMT-SELFTEST-ABORTS -->

Both short and extended operations are aborted by an applicable Format NVM command, sanitize start, or STC Fh, and may be aborted when the namespace is removed from inventory. Figure 701 requires the Format NSID, secure-erase selection, and Self-test NSID to be evaluated together.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §8.1.8.1-8.1.8.2, printed pages 615-616, PDF pages 641-642

### 9. Constructing the 564-byte LID 06h command

<!-- claim:BASENSMGMT-SELFTEST-LOG-COMMAND -->

A complete LID 06h read transfers 564 bytes or 141 dwords, so zero-based NUMD is 140 or 008Ch. Use LID 06h, LSP zero, LPOL/LPOU zero, OT zero, CSI zero, and UIDX zero. With RAE zero, CDW10 is 008C0006h.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13, printed pages 213-216, PDF pages 239-242

### 10. Current operation and completion percentage

<!-- claim:BASENSMGMT-SELFTEST-CURRENT -->

In LID 06h, byte 0 DSTOS identifies the current operation and byte 1 DSTCS[6:0] gives completion percentage; the host should ignore DSTCS when DSTOS is zero. When an operation completes or is aborted, the controller creates a result entry before clearing in-progress status to zero.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.7, printed pages 229-230, PDF pages 255-256

### 11. Twenty newest-first result entries

<!-- claim:BASENSMGMT-SELFTEST-HISTORY -->

LID 06h retains twenty 28-byte results with RDS1 newest. The high DSTS nibble DSTC records the original self-test code and the low nibble DSTR records completion or abort reason. SEGN is interpreted only when DSTR is 7h.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.7, printed pages 229-232, PDF pages 255-258

### 12. Validate the validity bit before the field

<!-- claim:BASENSMGMT-SELFTEST-VALIDITY -->

VDINFO NSIDVLD, FVLD, SCTVLD, and SCVLD are four independent validity gates. NSID, FLBA, STCT, and STC are interpreted only when the corresponding bit is one; a parser does not infer validity from a nonzero field.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.7, printed pages 231-232, PDF pages 257-258

### 13. NVM Command Set completes FLBA semantics

<!-- claim:BASENSMGMT-SELFTEST-NVM-FLBA -->

NVM Command Set 1.3 defines result bytes 23:16 as the logical block address that caused the failure. If multiple logical blocks fail, only one is reported, and it is valid only when FVLD is one.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-NVM-CS-1.3, Rev. 1.3, §4.1.4.3, printed pages 76, PDF pages 76

### 14. The NSZE, NCAP, NUSE capacity inequality

<!-- claim:BASENSMGMT-CAPACITY-MODEL -->

Namespace Size (NSZE) is the total logical-block range from LBA zero through n minus one; Namespace Capacity (NCAP) is the maximum allocatable blocks at any time; and Namespace Utilization (NUSE) is the number currently allocated. NSZE is always at least NCAP, which is at least NUSE.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-NVM-CS-1.3, Rev. 1.3, §2.1.1, printed pages 13-14, PDF pages 13-14

### 15. THINP governs NCAP/NUSE reporting

<!-- claim:BASENSMGMT-THIN-PROVISIONING -->

With NSFEAT.THINP one, a controller may report NCAP below NSZE and shall track NUSE. With THINP zero, the controller shall report NCAP equal to NSZE and may report NUSE as always equal to NCAP.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-NVM-CS-1.3, Rev. 1.3, §2.1.1, printed pages 13, PDF pages 13

### 16. The complete capability combines Manage and Attach

<!-- claim:BASENSMGMT-NSMGMT-CAPABILITY -->

The complete Namespace Management capability consists of Namespace Management and Namespace Attachment. A supporting controller shall implement both, set OACS.NMS to one, and support the Attached Namespace Attribute Changed event; the Allocated event is a should, while Namespace Granularity and Restore Default are may capabilities.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §8.1.17, printed pages 660, PDF pages 686

### 17. Allocated, active, inactive, and unallocated

<!-- claim:BASENSMGMT-NSID-LIFECYCLE -->

After create succeeds, the namespace is allocated but not attached and therefore is not active on a controller. Detach makes its NSID inactive on that controller; delete makes the NSID unallocated in the subsystem. Affected outstanding and later commands are handled as though issued to an inactive NSID.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §8.1.17, printed pages 660, PDF pages 686

### 18. Capability and capacity preflight before create

<!-- claim:BASENSMGMT-CREATE-PREFLIGHT -->

Before create, read common namespace capabilities with NSID FFFFFFFFh and CNS 00h; if supported, read Namespace Granularity with CNS 16h and determine available capacity. Only then construct the 4096-byte create buffer.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §8.1.17.1, printed pages 661-662, PDF pages 687-688

### 19. The Base 4096-byte create envelope

<!-- claim:BASENSMGMT-CREATE-BASE-COMMAND -->

Create uses NSID zero, SEL 0h, and CSI 00h for the NVM Command Set. DPTR identifies a 4096-byte structure: bytes 0:511 are I/O-Command-Set-specific, 512:1023 are reserved, and 1024:4095 are vendor specific. The host clears reserved bytes to zero.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.25, printed pages 446-448, PDF pages 472-474

### 20. NVM host-specified create fields

<!-- claim:BASENSMGMT-CREATE-NVM-PAYLOAD -->

The primary host-specified NVM create fields are NSZE, NCAP, FLBAS, DPS, NMIC, ANAGRPID, NVMSETID, ENDGID, LBSTM, NPHNDLS, and the Placement Handle List. After successful create, the namespace is formatted with these attributes, and unused reserved fields should be zero.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-NVM-CS-1.3, Rev. 1.3, §4.1.6.4, printed pages 111-113, PDF pages 111-113

### 21. Protection Information and LBSTM gates

<!-- claim:BASENSMGMT-PROTECTION-VALIDATION -->

End-to-end Data Protection settings are applied during create. Without LBAFEE, specified combinations using nonzero STS with 16-bit, or 32-bit or 64-bit Guard Protection Information, are aborted with Invalid Namespace or Format. An LBSTM that violates Figure 127 capability returns Invalid Field in Command.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-NVM-CS-1.3, Rev. 1.3, §4.1.6.2, printed pages 110, PDF pages 110

### 22. FDP Placement Handle validation

<!-- claim:BASENSMGMT-FDP-VALIDATION -->

NPHNDLS and the Placement Handle List participate in validation only when Flexible Data Placement (FDP) is enabled in the selected Endurance Group and SEL is Create. NPHNDLS may not exceed the supported Reclaim Unit Handles or 128; duplicates, out-of-range handles, incompatible formats, or no available handle lead to Invalid Placement Handle List or Invalid Format.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-NVM-CS-1.3, Rev. 1.3, §4.1.6.3, printed pages 110-111, PDF pages 110-111

### 23. NVMSETID/ENDGID decision matrix

<!-- claim:BASENSMGMT-GROUP-SELECTION -->

The NVMSETID/ENDGID matrix is: both zero lets the controller choose both; NVMSETID zero with nonzero ENDGID selects an NVM Set inside the specified Endurance Group; nonzero NVMSETID with zero ENDGID is Invalid Field; and both nonzero are valid only when that NVM Set belongs to the specified Endurance Group.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §8.1.17, printed pages 661, PDF pages 687

### 24. Requested size need not equal capacity consumption

<!-- claim:BASENSMGMT-ALLOCATION-ROUNDING -->

A controller may round actual capacity consumption up to an internal allocation unit. In the specification example, 32 blocks times 4 KiB equals a 128-KiB namespace but may consume 1 MiB with a 1-MiB allocation unit; capacity consumption therefore need not equal logical-block size times block count.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §8.1.17, printed pages 661, PDF pages 687

### 25. NSG/NCG are allocation hints, not validity gates

<!-- claim:BASENSMGMT-GRANULARITY-HINTS -->

Namespace Granularity NSG and NCG are byte-unit hints. If NSZE times LBA size is divisible by NSG, NCAP times LBA size is divisible by NCG, and NSZE equals NCAP, the namespace is fully provisioned and all allocated capacity is LBA-addressable. Violating a hint may waste capacity, but an otherwise valid create shall not be aborted solely for that reason.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-NVM-CS-1.3, Rev. 1.3, §5.8, printed pages 165, PDF pages 165

### 26. Controller List establishes access relationships

<!-- claim:BASENSMGMT-ATTACH-COMMAND -->

Namespace Attachment DPTR points to a 4096-byte Controller List; SEL 0h attaches and SEL 1h detaches. With PRPs, the buffer cannot use a PRP List because it may not cross more than one memory-page boundary. Attach/detach state persists across all reset events.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.24, printed pages 444-445, PDF pages 470-471

### 27. MAXDNA and MAXCNA are two levels of limits

<!-- claim:BASENSMGMT-ATTACH-LIMITS -->

Before attach, check Domain-aggregate MAXDNA and per-I/O-controller MAXCNA separately. Exceeding a nonzero limit returns Namespace Attachment Limit Exceeded. I/O Command Set support and enablement are additional independent gates, so attach failures do not collapse to one status.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.24, printed pages 444-445, PDF pages 470-471

### 28. CQE DW0 returns an NSID that is not yet attached

<!-- claim:BASENSMGMT-CREATE-COMPLETION -->

On successful create, the controller selects an available NSID and returns it in CQE DW0; the namespace is still unattached. Software preserves the returned NSID and then establishes controller access through Namespace Attachment instead of issuing I/O immediately after the create CQE.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.25, 8.1.17.1, printed pages 446-448, 662, PDF pages 472-474, 688

### 29. A controlled detach-then-delete flow

<!-- claim:BASENSMGMT-DELETE -->

Delete NSID selects a created namespace, while FFFFFFFFh means delete all and succeeds even when no namespace exists. Delete removes the namespace and has a detach side effect; the host should detach it from every controller first so events and outstanding-I/O behavior remain controlled.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.25, 8.1.17.1, printed pages 446, 448, 662, PDF pages 472, 474, 688

### 30. RDNCS, delete-all, and DNCS

<!-- claim:BASENSMGMT-RESTORE-DEFAULT -->

Restore Default uses SEL 2h; NSID should be zero and is ignored by the controller. Check RDNCS, delete every namespace in the subsystem, and then issue restore; any remaining namespace causes Command Sequence Error. Before success, the controller applies the current active firmware image's default configuration and sets DNCS to one.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.25.1, printed pages 447-448, PDF pages 473-474

### 31. Use command-specific status to locate the failed gate

<!-- claim:BASENSMGMT-COMMAND-STATUS -->

Debug evidence retains command-specific status. Attachment may return already attached 18h, private 19h, not attached 1Ah, Controller List invalid 1Ch, ANA attach failed 25h, limit 27h, or I/O Command Set 29h/2Ah. Management may return Invalid Format 0Ah, insufficient capacity 15h, NSID unavailable 16h, thin provisioning unsupported 1Bh, or ANA group invalid 24h.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.24-5.2.25, printed pages 445, 448, PDF pages 471, 474

### 32. Refresh Identify inventory after AER

<!-- claim:BASENSMGMT-NAMESPACE-EVENTS -->

Create changes the Allocated Namespace ID list, attach/detach changes the Active Namespace ID list, and delete may change both. When the corresponding notice is enabled, the host reissues Identify after the asynchronous event rather than inferring inventory from the event code alone. Section 8.1.17.2 distinguishes the controller processing delete from the other controllers.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §8.1.17.1-8.1.17.2, printed pages 662-663, PDF pages 688-689

### 33. NSG/NCG calculation with 4-KiB LBAs

<!-- claim:BASENSMGMT-GRANULARITY-EXAMPLE -->

Informative example: with 4-KiB LBAs, NSG 1 MiB equals 256 LBAs and NCG 2 MiB equals 512 LBAs. NSZE and NCAP of 1024 satisfy both granularities. Values of 1000 violate NSG/NCG divisibility, but an otherwise valid create is not aborted solely for that hint violation.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-NVM-CS-1.3, Rev. 1.3, §5.8, printed pages 165, PDF pages 165

### 34. Debug from the first lifecycle boundary

<!-- claim:BASENSMGMT-END-TO-END-DEBUG -->

A complete trace retains OACS.NMS and limits, common Identify and granularity snapshots, the 4096-byte create buffer, raw SQE, CQE DW0 NSID, Controller List, attach CQE, AER, refreshed Identify result, and inactive/unallocated state after detach/delete. The first inconsistent boundary is the debugging start point.

**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.24-5.2.25, 8.1.17.1, printed pages 444-448, 661-663, PDF pages 470-474, 687-689

## Figure index

This report introduces all 39 in-scope Figures. Use the section links below for the 100-minute presentation path; every Figure remains available as an appendix item. 19 Figures are outside the main section range but are included to explain cited dependencies and necessary prerequisites.

- [§4.1](#section-4-1)

- [§5.2](#section-5-2)

- [§8.1](#section-8-1)

- [Referenced Figure dependencies (outside the main section range)](#section-dependency)

## Figure and field-table teaching reference

The source uses Figure numbers for diagrams and field-layout tables. No source artwork is reproduced; compact field and keyword indexes come from the locally verified PDFs.

<a id="section-4-1"></a>

### §4.1

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 111: Self-test Results Data Structure</strong></summary>

<!-- claim:BASENSMGMT-FIG-111-CLAIM figure-table:BASENSMGMT-FIG-111 -->

**SPEC.** Figure 111, "Self-test Results Data Structure": Defines the concrete layout or value relationships for Self-test Results Data Structure. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is FLBA, bytes 23:16, FVLD, one failed logical block.

#### Where this Figure fits

Figure 111 sits in §4.1.4.3 and acts as a layout checkpoint. Read it after the report mental model has established the owning object and before software turns FLBA into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a structure or capability field table. Locate it using the structure base and offset, read in byte/bit order, and separate capability gates, value encoding, and reserved areas. Presence in the table does not mean the function is supported.

#### Teaching redraw

```text
[Locate source: FLBA]
          ↓
[Extract field: bytes 23:16] → [Apply encoding: FVLD]
                                      ↓
[Validate evidence: one failed logical block]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `FLBA` | Failing LBA, defined by the NVM Command Set as one logical block address that caused self-test failure. |
| `bytes 23:16` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `FVLD` | Failing LBA Valid, the validity bit determining whether FLBA may be interpreted. |
| `one failed logical block` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §4.1.4.3 is the applicable context.
2. Decode FLBA at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check bytes 23:16 as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 111 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §4.1.4.3 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes FLBA, bytes 23:16, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §4.1.4.3, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 111. Annotate the bytes containing FLBA, decode them, and independently verify bytes 23:16. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of FLBA in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand FLBA and state its unit or object scope?
2. Can the reader explain why bytes 23:16 is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** FLBA, bytes 23:16, FVLD, one failed logical block

**Source keyword index:** none

> Source: NVME-NVM-CS-1.3, Rev. 1.3, §4.1.4.3, Figure 111, printed pages 76, PDF pages 76

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 134: Namespace Management - Host Specified Fields</strong></summary>

<!-- claim:BASENSMGMT-FIG-134-CLAIM figure-table:BASENSMGMT-FIG-134 -->

**SPEC.** Figure 134, "Namespace Management - Host Specified Fields": Defines the concrete layout or value relationships for Namespace Management - Host Specified Fields. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is NSZE, NCAP, FLBAS, DPS, NMIC, ANAGRPID, NVMSETID, ENDGID, LBSTM, NPHNDLS, Placement Handle List.

#### Where this Figure fits

Figure 134 sits in §4.1.6.4 and acts as a hierarchy checkpoint. Read it after the report mental model has established the owning object and before software turns NSZE into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is an object or capacity relationship Figure. Separate containment, accessibility, identifier reference, and sharing. Adjacent boxes need not be one-to-one, and an identifier is not the physical or logical object it references.

#### Teaching redraw

```text
[Locate source: NSZE]
          ↓
[Extract field: NCAP] → [Apply encoding: FLBAS]
                                      ↓
[Validate evidence: DPS]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `NSZE` | Namespace Size, the total logical-block count whose LBA range is zero through NSZE minus one. |
| `NCAP` | Namespace Capacity, the maximum logical blocks that may be allocated to the namespace at any time. |
| `FLBAS` | Formatted LBA Size, selecting the LBA format used by a namespace and related metadata-placement control. |
| `DPS` | End-to-end Data Protection Type Settings, the create field selecting Protection Information type and position. |
| `NMIC` | Namespace Multi-path I/O and Namespace Sharing Capabilities, the create field declaring namespace sharing and multipath properties. |
| `ANAGRPID` | ANA Group Identifier, identifying the Asymmetric Namespace Access group for a namespace; zero at create lets the controller choose. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §4.1.6.4 is the applicable context.
2. Decode NSZE at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check NCAP as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 134 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §4.1.6.4 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes NSZE, NCAP, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §4.1.6.4, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 134. Annotate the bytes containing NSZE, decode them, and independently verify NCAP. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of NSZE in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand NSZE and state its unit or object scope?
2. Can the reader explain why NCAP is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** NSZE, NCAP, FLBAS, DPS, NMIC, ANAGRPID, NVMSETID, ENDGID, LBSTM, NPHNDLS, Placement Handle List

**Source keyword index:** `shall`, `may`, `reserved`

> Source: NVME-NVM-CS-1.3, Rev. 1.3, §4.1.6.4, Figure 134, printed pages 112-113, PDF pages 112-113

</details>

<a id="section-5-2"></a>

### §5.2

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 176: Device Self-test Namespace Test Action</strong></summary>

<!-- claim:BASENSMGMT-FIG-176-CLAIM figure-table:BASENSMGMT-FIG-176 -->

**SPEC.** Figure 176, "Device Self-test Namespace Test Action": Shows the object or capacity relationships in Device Self-test Namespace Test Action. Separate logical identifiers from controllers, namespaces, ports, and capacity containers. Evidence index: NSID 00000000h, active NSID, NSID FFFFFFFFh.

#### Where this Figure fits

Figure 176 sits in §5.2.6 and acts as a hierarchy checkpoint. Read it after the report mental model has established the owning object and before software turns NSID 00000000h into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is an object or capacity relationship Figure. Separate containment, accessibility, identifier reference, and sharing. Adjacent boxes need not be one-to-one, and an identifier is not the physical or logical object it references.

#### Teaching redraw

```text
[Locate source: NSID 00000000h]
          ↓
[Extract field: active NSID] → [Apply encoding: NSID FFFFFFFFh]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `NSID 00000000h` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `active NSID` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `NSID FFFFFFFFh` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §5.2.6 is the applicable context.
2. Decode NSID 00000000h at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check active NSID as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 176 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §5.2.6 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes NSID 00000000h, active NSID, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §5.2.6, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 176. Annotate the bytes containing NSID 00000000h, decode them, and independently verify active NSID. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of NSID 00000000h in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand NSID 00000000h and state its unit or object scope?
2. Can the reader explain why active NSID is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** NSID 00000000h, active NSID, NSID FFFFFFFFh

**Source keyword index:** none

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.6, Figure 176, printed pages 199, PDF pages 225

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 177: Device Self-test - Command Dword 10</strong></summary>

<!-- claim:BASENSMGMT-FIG-177-CLAIM figure-table:BASENSMGMT-FIG-177 -->

**SPEC.** Figure 177, "Device Self-test - Command Dword 10": Defines command-specific fields in CDW10 for Device Self-test. Locate CDW10, then decode the named fields without borrowing semantics from another command. Evidence index: STC 1h, STC 2h, STC 3h, STC Eh, STC Fh.

#### Where this Figure fits

Figure 177 sits in §5.2.6 and acts as a command checkpoint. Read it after the report mental model has established the owning object and before software turns STC 1h into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a command-construction field table. Build the common SQE, locate the specified CDW, encode each bit range, clear reserved bits, and validate the result against transfer length, buffer, and completion status. Equal field names do not imply equal semantics across commands.

#### Teaching redraw

```text
[Locate source: STC 1h]
          ↓
[Extract field: STC 2h] → [Apply encoding: STC 3h]
                                      ↓
[Validate evidence: STC Eh]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `STC 1h` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `STC 2h` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `STC 3h` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `STC Eh` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `STC Fh` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §5.2.6 is the applicable context.
2. Decode STC 1h at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check STC 2h as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 177 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §5.2.6 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes STC 1h, STC 2h, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §5.2.6, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 177. Annotate the bytes containing STC 1h, decode them, and independently verify STC 2h. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of STC 1h in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand STC 1h and state its unit or object scope?
2. Can the reader explain why STC 2h is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** STC 1h, STC 2h, STC 3h, STC Eh, STC Fh

**Source keyword index:** `may`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.6, Figure 177, printed pages 199, PDF pages 225

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 178: Device Self-test - Command Dword 15</strong></summary>

<!-- claim:BASENSMGMT-FIG-178-CLAIM figure-table:BASENSMGMT-FIG-178 -->

**SPEC.** Figure 178, "Device Self-test - Command Dword 15": Defines command-specific fields in CDW15 for Device Self-test. Locate CDW15, then decode the named fields without borrowing semantics from another command. Evidence index: DSTP.

#### Where this Figure fits

Figure 178 sits in §5.2.6 and acts as a command checkpoint. Read it after the report mental model has established the owning object and before software turns DSTP into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a command-construction field table. Build the common SQE, locate the specified CDW, encode each bit range, clear reserved bits, and validate the result against transfer length, buffer, and completion status. Equal field names do not imply equal semantics across commands.

#### Teaching redraw

```text
[Locate source: DSTP]
          ↓
[Extract field: evidence] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `DSTP` | Device Self-test Parameter, CDW15 with vendor-defined meaning only for vendor-specific STC Eh. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §5.2.6 is the applicable context.
2. Decode DSTP at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check the cited condition as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 178 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §5.2.6 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes DSTP, the cited condition, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §5.2.6, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 178. Annotate the bytes containing DSTP, decode them, and independently verify the cited condition. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of DSTP in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand DSTP and state its unit or object scope?
2. Can the reader explain why the cited condition is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** DSTP

**Source keyword index:** `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.6, Figure 178, printed pages 200, PDF pages 226

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 179: Device Self-test - Command Processing</strong></summary>

<!-- claim:BASENSMGMT-FIG-179-CLAIM figure-table:BASENSMGMT-FIG-179 -->

**SPEC.** Figure 179, "Device Self-test - Command Processing": Shows the queue or command relationship expressed by Device Self-test - Command Processing. Trace ownership and direction from host to SQ, controller, and CQ; keep the indexed elements distinct: self-test in progress, abort, result creation.

#### Where this Figure fits

Figure 179 sits in §5.2.6 and acts as a queue checkpoint. Read it after the report mental model has established the owning object and before software turns self-test in progress into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a queue or command-flow Figure. Label host and controller ownership first, then trace head, tail, phase, or arbitration changes. An arrow represents a state or ownership transition and does not automatically prove command completion.

#### Teaching redraw

```text
[Locate source: self-test in progress]
          ↓
[Extract field: abort] → [Apply encoding: result creation]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `self-test in progress` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `abort` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `result creation` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §5.2.6 is the applicable context.
2. Decode self-test in progress at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check abort as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 179 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §5.2.6 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes self-test in progress, abort, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §5.2.6, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 179. Annotate the bytes containing self-test in progress, decode them, and independently verify abort. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of self-test in progress in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand self-test in progress and state its unit or object scope?
2. Can the reader explain why abort is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** self-test in progress, abort, result creation

**Source keyword index:** none

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.6, Figure 179, printed pages 200, PDF pages 226

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 180: Device Self-test - Command Specific Status Values</strong></summary>

<!-- claim:BASENSMGMT-FIG-180-CLAIM figure-table:BASENSMGMT-FIG-180 -->

**SPEC.** Figure 180, "Device Self-test - Command Specific Status Values": Defines the concrete layout or value relationships for Device Self-test - Command Specific Status Values. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is Device Self-test in Progress, status 1Dh.

#### Where this Figure fits

Figure 180 sits in §5.2.6 and acts as a layout checkpoint. Read it after the report mental model has established the owning object and before software turns Device Self-test in Progress into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a structure or capability field table. Locate it using the structure base and offset, read in byte/bit order, and separate capability gates, value encoding, and reserved areas. Presence in the table does not mean the function is supported.

#### Teaching redraw

```text
[Locate source: Device Self-test in Progress]
          ↓
[Extract field: status 1Dh] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `Device Self-test in Progress` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `status 1Dh` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §5.2.6 is the applicable context.
2. Decode Device Self-test in Progress at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check status 1Dh as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 180 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §5.2.6 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes Device Self-test in Progress, status 1Dh, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §5.2.6, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 180. Annotate the bytes containing Device Self-test in Progress, decode them, and independently verify status 1Dh. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of Device Self-test in Progress in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand Device Self-test in Progress and state its unit or object scope?
2. Can the reader explain why status 1Dh is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** Device Self-test in Progress, status 1Dh

**Source keyword index:** none

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.6, Figure 180, printed pages 201, PDF pages 227

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 218: Device Self-test Log Page</strong></summary>

<!-- claim:BASENSMGMT-FIG-218-CLAIM figure-table:BASENSMGMT-FIG-218 -->

**SPEC.** Figure 218, "Device Self-test Log Page": Connects Device Self-test Log Page to the Self-test evidence path or namespace lifecycle. Identify the object and lifecycle state, decode DSTOS, DSTCS, RDS1-RDS20, 564 bytes, then verify the next transition with a CQE, log, event, or Identify snapshot.

#### Where this Figure fits

Figure 218 sits in §5.2.13.1.7 and acts as a relationship checkpoint. Read it after the report mental model has established the owning object and before software turns DSTOS into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This Figure explains a specific relationship or example. Identify each component type and owner, then decide whether each connection represents data flow, control flow, containment, or a condition. Visual placement alone creates no normative requirement.

#### Teaching redraw

```text
[Locate source: DSTOS]
          ↓
[Extract field: DSTCS] → [Apply encoding: RDS1-RDS20]
                                      ↓
[Validate evidence: 564 bytes]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `DSTOS` | Device Self-test Operation Status, the LID 06h nibble identifying the current operation. |
| `DSTCS` | Device Self-test Completion Status, the LID 06h completion percentage from 0 through 100. |
| `RDS1-RDS20` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `564 bytes` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §5.2.13.1.7 is the applicable context.
2. Decode DSTOS at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check DSTCS as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 218 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §5.2.13.1.7 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes DSTOS, DSTCS, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §5.2.13.1.7, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 218. Annotate the bytes containing DSTOS, decode them, and independently verify DSTCS. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of DSTOS in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand DSTOS and state its unit or object scope?
2. Can the reader explain why DSTCS is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** DSTOS, DSTCS, RDS1-RDS20, 564 bytes

**Source keyword index:** `shall not`, `shall`, `should`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.7, Figure 218, printed pages 230, PDF pages 256

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 219: Self-test Result Data Structure</strong></summary>

<!-- claim:BASENSMGMT-FIG-219-CLAIM figure-table:BASENSMGMT-FIG-219 -->

**SPEC.** Figure 219, "Self-test Result Data Structure": Defines the concrete layout or value relationships for Self-test Result Data Structure. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is DSTC, DSTR, SEGN, VDINFO, NSID, FLBA, STCT, STC.

#### Where this Figure fits

Figure 219 sits in §5.2.13.1.7 and acts as a layout checkpoint. Read it after the report mental model has established the owning object and before software turns DSTC into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a structure or capability field table. Locate it using the structure base and offset, read in byte/bit order, and separate capability gates, value encoding, and reserved areas. Presence in the table does not mean the function is supported.

#### Teaching redraw

```text
[Locate source: DSTC]
          ↓
[Extract field: DSTR] → [Apply encoding: SEGN]
                                      ↓
[Validate evidence: VDINFO]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `DSTC` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `DSTR` | Device Self-test Result, the result-entry nibble identifying success, abort, or segment failure. |
| `SEGN` | Segment Number, identifying the first failed diagnostic segment only when DSTR is 7h. |
| `VDINFO` | Valid Diagnostic Information, the bitmap independently gating NSID, FLBA, SCT, and SC. |
| `NSID` | Namespace Identifier, a controller-visible numeric handle for a namespace; the identifier is not the namespace object itself. |
| `FLBA` | Failing LBA, defined by the NVM Command Set as one logical block address that caused self-test failure. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §5.2.13.1.7 is the applicable context.
2. Decode DSTC at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check DSTR as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 219 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §5.2.13.1.7 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes DSTC, DSTR, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §5.2.13.1.7, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 219. Annotate the bytes containing DSTC, decode them, and independently verify DSTR. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of DSTC in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand DSTC and state its unit or object scope?
2. Can the reader explain why DSTR is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** DSTC, DSTR, SEGN, VDINFO, NSID, FLBA, STCT, STC

**Source keyword index:** `should`, `may`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.7, Figure 219, printed pages 231-232, PDF pages 257-258

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 442: Namespace Attachment - Data Pointer</strong></summary>

<!-- claim:BASENSMGMT-FIG-442-CLAIM figure-table:BASENSMGMT-FIG-442 -->

**SPEC.** Figure 442, "Namespace Attachment - Data Pointer": Shows the object or capacity relationships in Namespace Attachment - Data Pointer. Separate logical identifiers from controllers, namespaces, ports, and capacity containers. Evidence index: DPTR, Controller List, one page boundary.

#### Where this Figure fits

Figure 442 sits in §5.2.24 and acts as a command checkpoint. Read it after the report mental model has established the owning object and before software turns DPTR into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a command-construction field table. Build the common SQE, locate the specified CDW, encode each bit range, clear reserved bits, and validate the result against transfer length, buffer, and completion status. Equal field names do not imply equal semantics across commands.

#### Teaching redraw

```text
[Locate source: DPTR]
          ↓
[Extract field: Controller List] → [Apply encoding: one page boundary]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `DPTR` | Data Pointer, the SQE field identifying a command data buffer. |
| `Controller List` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `one page boundary` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §5.2.24 is the applicable context.
2. Decode DPTR at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check Controller List as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 442 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §5.2.24 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes DPTR, Controller List, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §5.2.24, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 442. Annotate the bytes containing DPTR, decode them, and independently verify Controller List. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

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
2. Can the reader explain why Controller List is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** DPTR, Controller List, one page boundary

**Source keyword index:** `shall not`, `shall`, `may`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.24, Figure 442, printed pages 445, PDF pages 471

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 443: Namespace Attachment - Command Dword 10</strong></summary>

<!-- claim:BASENSMGMT-FIG-443-CLAIM figure-table:BASENSMGMT-FIG-443 -->

**SPEC.** Figure 443, "Namespace Attachment - Command Dword 10": Defines command-specific fields in CDW10 for Namespace Attachment. Locate CDW10, then decode the named fields without borrowing semantics from another command. Evidence index: SEL 0h Attach, SEL 1h Detach.

#### Where this Figure fits

Figure 443 sits in §5.2.24 and acts as a command checkpoint. Read it after the report mental model has established the owning object and before software turns SEL 0h Attach into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a command-construction field table. Build the common SQE, locate the specified CDW, encode each bit range, clear reserved bits, and validate the result against transfer length, buffer, and completion status. Equal field names do not imply equal semantics across commands.

#### Teaching redraw

```text
[Locate source: SEL 0h Attach]
          ↓
[Extract field: SEL 1h Detach] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `SEL 0h Attach` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `SEL 1h Detach` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §5.2.24 is the applicable context.
2. Decode SEL 0h Attach at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check SEL 1h Detach as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 443 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §5.2.24 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes SEL 0h Attach, SEL 1h Detach, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §5.2.24, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 443. Annotate the bytes containing SEL 0h Attach, decode them, and independently verify SEL 1h Detach. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of SEL 0h Attach in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand SEL 0h Attach and state its unit or object scope?
2. Can the reader explain why SEL 1h Detach is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** SEL 0h Attach, SEL 1h Detach

**Source keyword index:** `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.24, Figure 443, printed pages 445, PDF pages 471

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 444: Namespace Attachment - Command Specific Status Values</strong></summary>

<!-- claim:BASENSMGMT-FIG-444-CLAIM figure-table:BASENSMGMT-FIG-444 -->

**SPEC.** Figure 444, "Namespace Attachment - Command Specific Status Values": Defines the concrete layout or value relationships for Namespace Attachment - Command Specific Status Values. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is status 18h-1Ch, status 25h, status 27h, status 29h-2Ah.

#### Where this Figure fits

Figure 444 sits in §5.2.24 and acts as a hierarchy checkpoint. Read it after the report mental model has established the owning object and before software turns status 18h-1Ch into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is an object or capacity relationship Figure. Separate containment, accessibility, identifier reference, and sharing. Adjacent boxes need not be one-to-one, and an identifier is not the physical or logical object it references.

#### Teaching redraw

```text
[Locate source: status 18h-1Ch]
          ↓
[Extract field: status 25h] → [Apply encoding: status 27h]
                                      ↓
[Validate evidence: status 29h-2Ah]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `status 18h-1Ch` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `status 25h` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `status 27h` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `status 29h-2Ah` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §5.2.24 is the applicable context.
2. Decode status 18h-1Ch at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check status 25h as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 444 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §5.2.24 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes status 18h-1Ch, status 25h, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §5.2.24, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 444. Annotate the bytes containing status 18h-1Ch, decode them, and independently verify status 25h. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of status 18h-1Ch in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand status 18h-1Ch and state its unit or object scope?
2. Can the reader explain why status 25h is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** status 18h-1Ch, status 25h, status 27h, status 29h-2Ah

**Source keyword index:** none

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.24, Figure 444, printed pages 445, PDF pages 471

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 445: Namespace Management - Data Pointer</strong></summary>

<!-- claim:BASENSMGMT-FIG-445-CLAIM figure-table:BASENSMGMT-FIG-445 -->

**SPEC.** Figure 445, "Namespace Management - Data Pointer": Shows the object or capacity relationships in Namespace Management - Data Pointer. Separate logical identifiers from controllers, namespaces, ports, and capacity containers. Evidence index: DPTR, 4096-byte create buffer.

#### Where this Figure fits

Figure 445 sits in §5.2.25 and acts as a command checkpoint. Read it after the report mental model has established the owning object and before software turns DPTR into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a command-construction field table. Build the common SQE, locate the specified CDW, encode each bit range, clear reserved bits, and validate the result against transfer length, buffer, and completion status. Equal field names do not imply equal semantics across commands.

#### Teaching redraw

```text
[Locate source: DPTR]
          ↓
[Extract field: 4096-byte create buffer] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `DPTR` | Data Pointer, the SQE field identifying a command data buffer. |
| `4096-byte create buffer` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §5.2.25 is the applicable context.
2. Decode DPTR at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check 4096-byte create buffer as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 445 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §5.2.25 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes DPTR, 4096-byte create buffer, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §5.2.25, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 445. Annotate the bytes containing DPTR, decode them, and independently verify 4096-byte create buffer. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

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
2. Can the reader explain why 4096-byte create buffer is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** DPTR, 4096-byte create buffer

**Source keyword index:** `shall not`, `shall`, `may`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.25, Figure 445, printed pages 446, PDF pages 472

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 446: Namespace Management - Command Dword 10</strong></summary>

<!-- claim:BASENSMGMT-FIG-446-CLAIM figure-table:BASENSMGMT-FIG-446 -->

**SPEC.** Figure 446, "Namespace Management - Command Dword 10": Defines command-specific fields in CDW10 for Namespace Management. Locate CDW10, then decode the named fields without borrowing semantics from another command. Evidence index: SEL 0h Create, SEL 1h Delete, SEL 2h Restore.

#### Where this Figure fits

Figure 446 sits in §5.2.25 and acts as a command checkpoint. Read it after the report mental model has established the owning object and before software turns SEL 0h Create into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a command-construction field table. Build the common SQE, locate the specified CDW, encode each bit range, clear reserved bits, and validate the result against transfer length, buffer, and completion status. Equal field names do not imply equal semantics across commands.

#### Teaching redraw

```text
[Locate source: SEL 0h Create]
          ↓
[Extract field: SEL 1h Delete] → [Apply encoding: SEL 2h Restore]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `SEL 0h Create` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `SEL 1h Delete` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `SEL 2h Restore` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §5.2.25 is the applicable context.
2. Decode SEL 0h Create at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check SEL 1h Delete as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 446 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §5.2.25 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes SEL 0h Create, SEL 1h Delete, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §5.2.25, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 446. Annotate the bytes containing SEL 0h Create, decode them, and independently verify SEL 1h Delete. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of SEL 0h Create in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand SEL 0h Create and state its unit or object scope?
2. Can the reader explain why SEL 1h Delete is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** SEL 0h Create, SEL 1h Delete, SEL 2h Restore

**Source keyword index:** `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.25, Figure 446, printed pages 446-447, PDF pages 472-473

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 447: Namespace Management - Command Dword 11</strong></summary>

<!-- claim:BASENSMGMT-FIG-447-CLAIM figure-table:BASENSMGMT-FIG-447 -->

**SPEC.** Figure 447, "Namespace Management - Command Dword 11": Defines command-specific fields in CDW11 for Namespace Management. Locate CDW11, then decode the named fields without borrowing semantics from another command. Evidence index: CSI, NVM Command Set 00h.

#### Where this Figure fits

Figure 447 sits in §5.2.25 and acts as a command checkpoint. Read it after the report mental model has established the owning object and before software turns CSI into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a command-construction field table. Build the common SQE, locate the specified CDW, encode each bit range, clear reserved bits, and validate the result against transfer length, buffer, and completion status. Equal field names do not imply equal semantics across commands.

#### Teaching redraw

```text
[Locate source: CSI]
          ↓
[Extract field: NVM Command Set 00h] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `CSI` | Command Set Identifier, selecting the I/O Command Set context for a command or log page. |
| `NVM Command Set 00h` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §5.2.25 is the applicable context.
2. Decode CSI at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check NVM Command Set 00h as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 447 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §5.2.25 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes CSI, NVM Command Set 00h, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §5.2.25, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 447. Annotate the bytes containing CSI, decode them, and independently verify NVM Command Set 00h. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

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
2. Can the reader explain why NVM Command Set 00h is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** CSI, NVM Command Set 00h

**Source keyword index:** `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.25, Figure 447, printed pages 447, PDF pages 473

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 448: Namespace Management - Data Structure for Create</strong></summary>

<!-- claim:BASENSMGMT-FIG-448-CLAIM figure-table:BASENSMGMT-FIG-448 -->

**SPEC.** Figure 448, "Namespace Management - Data Structure for Create": Defines the concrete layout or value relationships for Namespace Management - Data Structure for Create. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is SIOCS bytes 0:511, reserved bytes 512:1023, VS bytes 1024:4095.

#### Where this Figure fits

Figure 448 sits in §5.2.25 and acts as a hierarchy checkpoint. Read it after the report mental model has established the owning object and before software turns SIOCS bytes 0:511 into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is an object or capacity relationship Figure. Separate containment, accessibility, identifier reference, and sharing. Adjacent boxes need not be one-to-one, and an identifier is not the physical or logical object it references.

#### Teaching redraw

```text
[Locate source: SIOCS bytes 0:511]
          ↓
[Extract field: reserved bytes 512:1023] → [Apply encoding: VS bytes 1024:4095]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `SIOCS bytes 0:511` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `reserved bytes 512:1023` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `VS bytes 1024:4095` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §5.2.25 is the applicable context.
2. Decode SIOCS bytes 0:511 at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check reserved bytes 512:1023 as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 448 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §5.2.25 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes SIOCS bytes 0:511, reserved bytes 512:1023, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §5.2.25, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 448. Annotate the bytes containing SIOCS bytes 0:511, decode them, and independently verify reserved bytes 512:1023. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of SIOCS bytes 0:511 in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand SIOCS bytes 0:511 and state its unit or object scope?
2. Can the reader explain why reserved bytes 512:1023 is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** SIOCS bytes 0:511, reserved bytes 512:1023, VS bytes 1024:4095

**Source keyword index:** `shall`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.25, Figure 448, printed pages 447, PDF pages 473

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 449: Namespace Management - Command Specific Status Values</strong></summary>

<!-- claim:BASENSMGMT-FIG-449-CLAIM figure-table:BASENSMGMT-FIG-449 -->

**SPEC.** Figure 449, "Namespace Management - Command Specific Status Values": Defines the concrete layout or value relationships for Namespace Management - Command Specific Status Values. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is Invalid Format, Insufficient Capacity, NSID Unavailable, Thin Provisioning Not Supported.

#### Where this Figure fits

Figure 449 sits in §5.2.25 and acts as a hierarchy checkpoint. Read it after the report mental model has established the owning object and before software turns Invalid Format into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is an object or capacity relationship Figure. Separate containment, accessibility, identifier reference, and sharing. Adjacent boxes need not be one-to-one, and an identifier is not the physical or logical object it references.

#### Teaching redraw

```text
[Locate source: Invalid Format]
          ↓
[Extract field: Insufficient Capacity] → [Apply encoding: NSID Unavailable]
                                      ↓
[Validate evidence: Thin Provisioning Not Supported]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `Invalid Format` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `Insufficient Capacity` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `NSID Unavailable` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `Thin Provisioning Not Supported` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §5.2.25 is the applicable context.
2. Decode Invalid Format at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check Insufficient Capacity as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 449 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §5.2.25 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes Invalid Format, Insufficient Capacity, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §5.2.25, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 449. Annotate the bytes containing Invalid Format, decode them, and independently verify Insufficient Capacity. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of Invalid Format in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand Invalid Format and state its unit or object scope?
2. Can the reader explain why Insufficient Capacity is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** Invalid Format, Insufficient Capacity, NSID Unavailable, Thin Provisioning Not Supported

**Source keyword index:** `may`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.25, Figure 449, printed pages 448, PDF pages 474

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 450: Namespace Management - Completion Queue Entry Dword 0</strong></summary>

<!-- claim:BASENSMGMT-FIG-450-CLAIM figure-table:BASENSMGMT-FIG-450 -->

**SPEC.** Figure 450, "Namespace Management - Completion Queue Entry Dword 0": Shows the queue or command relationship expressed by Namespace Management - Completion Queue Entry Dword 0. Trace ownership and direction from host to SQ, controller, and CQ; keep the indexed elements distinct: CQE DW0, created NSID.

#### Where this Figure fits

Figure 450 sits in §5.2.25 and acts as a queue checkpoint. Read it after the report mental model has established the owning object and before software turns CQE DW0 into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a queue or command-flow Figure. Label host and controller ownership first, then trace head, tail, phase, or arbitration changes. An arrow represents a state or ownership transition and does not automatically prove command completion.

#### Teaching redraw

```text
[Locate source: CQE DW0]
          ↓
[Extract field: created NSID] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `CQE DW0` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `created NSID` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §5.2.25 is the applicable context.
2. Decode CQE DW0 at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check created NSID as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 450 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §5.2.25 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes CQE DW0, created NSID, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §5.2.25, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 450. Annotate the bytes containing CQE DW0, decode them, and independently verify created NSID. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of CQE DW0 in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand CQE DW0 and state its unit or object scope?
2. Can the reader explain why created NSID is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** CQE DW0, created NSID

**Source keyword index:** `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.25, Figure 450, printed pages 448, PDF pages 474

</details>

<a id="section-8-1"></a>

### §8.1

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 700: Example Device Self-test Operation (Informative)</strong></summary>

<!-- claim:BASENSMGMT-FIG-700-CLAIM figure-table:BASENSMGMT-FIG-700 -->

**SPEC.** Figure 700, "Example Device Self-test Operation (Informative)": Defines the concrete layout or value relationships for Example Device Self-test Operation (Informative). Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is segment, test performed, failure criteria, informative.

#### Where this Figure fits

Figure 700 sits in §8.1.8 and acts as a layout checkpoint. Read it after the report mental model has established the owning object and before software turns segment into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a structure or capability field table. Locate it using the structure base and offset, read in byte/bit order, and separate capability gates, value encoding, and reserved areas. Presence in the table does not mean the function is supported.

#### Teaching redraw

```text
[Locate source: segment]
          ↓
[Extract field: test performed] → [Apply encoding: failure criteria]
                                      ↓
[Validate evidence: informative]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `segment` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `test performed` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `failure criteria` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `informative` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §8.1.8 is the applicable context.
2. Decode segment at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check test performed as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 700 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §8.1.8 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes segment, test performed, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §8.1.8, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 700. Annotate the bytes containing segment, decode them, and independently verify test performed. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of segment in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand segment and state its unit or object scope?
2. Can the reader explain why test performed is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** segment, test performed, failure criteria, informative

**Source keyword index:** `shall`, `should`, `may`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §8.1.8, Figure 700, printed pages 615, PDF pages 641

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 701: Format NVM command Aborting a Device Self-Test Operation</strong></summary>

<!-- claim:BASENSMGMT-FIG-701-CLAIM figure-table:BASENSMGMT-FIG-701 -->

**SPEC.** Figure 701, "Format NVM command Aborting a Device Self-Test Operation": Defines the concrete layout or value relationships for Format NVM command Aborting a Device Self-Test Operation. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is SES, FNS, SENS, Format NSID, Self-test NSID, abort decision.

#### Where this Figure fits

Figure 701 sits in §8.1.8.1-8.1.8.2 and acts as a layout checkpoint. Read it after the report mental model has established the owning object and before software turns SES into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a structure or capability field table. Locate it using the structure base and offset, read in byte/bit order, and separate capability gates, value encoding, and reserved areas. Presence in the table does not mean the function is supported.

#### Teaching redraw

```text
[Locate source: SES]
          ↓
[Extract field: FNS] → [Apply encoding: SENS]
                                      ↓
[Validate evidence: Format NSID]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `SES` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `FNS` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `SENS` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `Format NSID` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `Self-test NSID` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `abort decision` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §8.1.8.1-8.1.8.2 is the applicable context.
2. Decode SES at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check FNS as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 701 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §8.1.8.1-8.1.8.2 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes SES, FNS, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §8.1.8.1-8.1.8.2, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 701. Annotate the bytes containing SES, decode them, and independently verify FNS. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of SES in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand SES and state its unit or object scope?
2. Can the reader explain why FNS is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** SES, FNS, SENS, Format NSID, Self-test NSID, abort decision

**Source keyword index:** `shall`, `should`, `may`, `optional`

> Source: NVME-BASE-2.4, Rev. 2.4, §8.1.8.1-8.1.8.2, Figure 701, printed pages 616, PDF pages 642

</details>

<a id="section-dependency"></a>

### Referenced Figure dependencies (outside the main section range)

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 36: Offset 0h: CAP - Controller Capabilities</strong></summary>

<!-- claim:BASENSMGMT-FIG-036-CLAIM figure-table:BASENSMGMT-FIG-036 -->

**SPEC.** Figure 36, "Offset 0h: CAP - Controller Capabilities": Defines CAP (Controller Capabilities) at offset 0h and identifies the fields that software must decode at that location. Start at CAP, then map bit ranges to access type, reset value, and field meaning. Evidence index: CSS, active I/O Command Set.

#### Where this Figure fits

Figure 36 sits in §3.1.4.1 and acts as a register checkpoint. Read it after the report mental model has established the owning object and before software turns CSS into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a register or property field table. Locate the base offset, verify access width, reset value, and bit range, and only then convert bits into state or capability. Preserve the complete register snapshot so adjacent conditions are not lost by extracting one bit.

#### Teaching redraw

```text
[Locate source: CSS]
          ↓
[Extract field: active I/O Command Set] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `CSS` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `active I/O Command Set` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §3.1.4.1 is the applicable context.
2. Decode CSS at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check active I/O Command Set as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 36 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §3.1.4.1 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes CSS, active I/O Command Set, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §3.1.4.1, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 36. Annotate the bytes containing CSS, decode them, and independently verify active I/O Command Set. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of CSS in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand CSS and state its unit or object scope?
2. Can the reader explain why active I/O Command Set is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** CSS, active I/O Command Set

**Source keyword index:** `shall not`, `shall`, `should`, `may`, `optional`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.1, Figure 36, printed pages 55-58, PDF pages 81-84

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 93: Common Command Format</strong></summary>

<!-- claim:BASENSMGMT-FIG-093-CLAIM figure-table:BASENSMGMT-FIG-093 -->

**SPEC.** Figure 93, "Common Command Format": Defines the concrete layout or value relationships for Common Command Format. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is OPC, NSID, DPTR, CDW10-CDW15.

#### Where this Figure fits

Figure 93 sits in §4.1.1 and acts as a command checkpoint. Read it after the report mental model has established the owning object and before software turns OPC into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a command-construction field table. Build the common SQE, locate the specified CDW, encode each bit range, clear reserved bits, and validate the result against transfer length, buffer, and completion status. Equal field names do not imply equal semantics across commands.

#### Teaching redraw

```text
[Locate source: OPC]
          ↓
[Extract field: NSID] → [Apply encoding: DPTR]
                                      ↓
[Validate evidence: CDW10-CDW15]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `OPC` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `NSID` | Namespace Identifier, a controller-visible numeric handle for a namespace; the identifier is not the namespace object itself. |
| `DPTR` | Data Pointer, the SQE field identifying a command data buffer. |
| `CDW10-CDW15` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §4.1.1 is the applicable context.
2. Decode OPC at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
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
| It answers | How the cited section organizes OPC, NSID, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §4.1.1, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 93. Annotate the bytes containing OPC, decode them, and independently verify NSID. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of OPC in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand OPC and state its unit or object scope?
2. Can the reader explain why NSID is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** OPC, NSID, DPTR, CDW10-CDW15

**Source keyword index:** `shall`, `may`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §4.1.1, Figure 93, printed pages 140-142, PDF pages 166-168

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 123: Identify - Identify Namespace Data Structure, NVM Command Set</strong></summary>

<!-- claim:BASENSMGMT-FIG-123-CLAIM figure-table:BASENSMGMT-FIG-123 -->

**SPEC.** Figure 123, "Identify - Identify Namespace Data Structure, NVM Command Set": Defines the concrete layout or value relationships for Identify - Identify Namespace Data Structure, NVM Command Set. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is NSZE, NCAP, NUSE, NSFEAT.THINP, FLBAS, DPS, NMIC.

#### Where this Figure fits

Figure 123 sits in §4.1.5.1 and acts as a hierarchy checkpoint. Read it after the report mental model has established the owning object and before software turns NSZE into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is an object or capacity relationship Figure. Separate containment, accessibility, identifier reference, and sharing. Adjacent boxes need not be one-to-one, and an identifier is not the physical or logical object it references.

#### Teaching redraw

```text
[Locate source: NSZE]
          ↓
[Extract field: NCAP] → [Apply encoding: NUSE]
                                      ↓
[Validate evidence: NSFEAT.THINP]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `NSZE` | Namespace Size, the total logical-block count whose LBA range is zero through NSZE minus one. |
| `NCAP` | Namespace Capacity, the maximum logical blocks that may be allocated to the namespace at any time. |
| `NUSE` | Namespace Utilization, the logical blocks currently allocated in the namespace. |
| `NSFEAT.THINP` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `FLBAS` | Formatted LBA Size, selecting the LBA format used by a namespace and related metadata-placement control. |
| `DPS` | End-to-end Data Protection Type Settings, the create field selecting Protection Information type and position. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §4.1.5.1 is the applicable context.
2. Decode NSZE at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check NCAP as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 123 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §4.1.5.1 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes NSZE, NCAP, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §4.1.5.1, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 123. Annotate the bytes containing NSZE, decode them, and independently verify NCAP. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of NSZE in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand NSZE and state its unit or object scope?
2. Can the reader explain why NCAP is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** NSZE, NCAP, NUSE, NSFEAT.THINP, FLBAS, DPS, NMIC

**Source keyword index:** `shall not`, `shall`, `should`, `may`, `optional`, `reserved`

> Source: NVME-NVM-CS-1.3, Rev. 1.3, §4.1.5.1, Figure 123, printed pages 85-87, PDF pages 85-87

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 127: NVM Command Set I/O Command Set Specific Identify Namespace Data Structure</strong></summary>

<!-- claim:BASENSMGMT-FIG-127-CLAIM figure-table:BASENSMGMT-FIG-127 -->

**SPEC.** Figure 127, "NVM Command Set I/O Command Set Specific Identify Namespace Data Structure": Defines the concrete layout or value relationships for NVM Command Set I/O Command Set Specific Identify Namespace Data Structure. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is LBSTM, Storage Tag Masking Level, LBAFEE.

#### Where this Figure fits

Figure 127 sits in §4.1.5.3 and acts as a hierarchy checkpoint. Read it after the report mental model has established the owning object and before software turns LBSTM into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is an object or capacity relationship Figure. Separate containment, accessibility, identifier reference, and sharing. Adjacent boxes need not be one-to-one, and an identifier is not the physical or logical object it references.

#### Teaching redraw

```text
[Locate source: LBSTM]
          ↓
[Extract field: Storage Tag Masking Level] → [Apply encoding: LBAFEE]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `LBSTM` | Logical Block Storage Tag Mask, the 64-bit create field selecting Storage Tag bits to mask. |
| `Storage Tag Masking Level` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `LBAFEE` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §4.1.5.3 is the applicable context.
2. Decode LBSTM at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check Storage Tag Masking Level as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 127 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §4.1.5.3 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes LBSTM, Storage Tag Masking Level, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §4.1.5.3, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 127. Annotate the bytes containing LBSTM, decode them, and independently verify Storage Tag Masking Level. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of LBSTM in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand LBSTM and state its unit or object scope?
2. Can the reader explain why Storage Tag Masking Level is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** LBSTM, Storage Tag Masking Level, LBAFEE

**Source keyword index:** `shall`, `should`, `may`, `optional`, `reserved`

> Source: NVME-NVM-CS-1.3, Rev. 1.3, §4.1.5.3, Figure 127, printed pages 97-101, PDF pages 97-101

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 132: Namespace Granularity List</strong></summary>

<!-- claim:BASENSMGMT-FIG-132-CLAIM figure-table:BASENSMGMT-FIG-132 -->

**SPEC.** Figure 132, "Namespace Granularity List": Shows the object or capacity relationships in Namespace Granularity List. Separate logical identifiers from controllers, namespaces, ports, and capacity containers. Evidence index: NGA.GDM, ND, NGD0-NGD63, CNS 16h.

#### Where this Figure fits

Figure 132 sits in §4.1.5.8 and acts as a hierarchy checkpoint. Read it after the report mental model has established the owning object and before software turns NGA.GDM into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is an object or capacity relationship Figure. Separate containment, accessibility, identifier reference, and sharing. Adjacent boxes need not be one-to-one, and an identifier is not the physical or logical object it references.

#### Teaching redraw

```text
[Locate source: NGA.GDM]
          ↓
[Extract field: ND] → [Apply encoding: NGD0-NGD63]
                                      ↓
[Validate evidence: CNS 16h]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `NGA.GDM` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `ND` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `NGD0-NGD63` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `CNS 16h` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §4.1.5.8 is the applicable context.
2. Decode NGA.GDM at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check ND as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 132 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §4.1.5.8 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes NGA.GDM, ND, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §4.1.5.8, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 132. Annotate the bytes containing NGA.GDM, decode them, and independently verify ND. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of NGA.GDM in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand NGA.GDM and state its unit or object scope?
2. Can the reader explain why ND is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** NGA.GDM, ND, NGD0-NGD63, CNS 16h

**Source keyword index:** `shall`, `reserved`

> Source: NVME-NVM-CS-1.3, Rev. 1.3, §4.1.5.8, Figure 132, printed pages 108, PDF pages 108

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 133: Namespace Granularity Descriptor</strong></summary>

<!-- claim:BASENSMGMT-FIG-133-CLAIM figure-table:BASENSMGMT-FIG-133 -->

**SPEC.** Figure 133, "Namespace Granularity Descriptor": Defines the concrete layout or value relationships for Namespace Granularity Descriptor. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is NSG bytes 7:0, NCG bytes 15:8, byte units.

#### Where this Figure fits

Figure 133 sits in §4.1.5.8 and acts as a hierarchy checkpoint. Read it after the report mental model has established the owning object and before software turns NSG bytes 7:0 into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is an object or capacity relationship Figure. Separate containment, accessibility, identifier reference, and sharing. Adjacent boxes need not be one-to-one, and an identifier is not the physical or logical object it references.

#### Teaching redraw

```text
[Locate source: NSG bytes 7:0]
          ↓
[Extract field: NCG bytes 15:8] → [Apply encoding: byte units]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `NSG bytes 7:0` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `NCG bytes 15:8` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `byte units` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §4.1.5.8 is the applicable context.
2. Decode NSG bytes 7:0 at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check NCG bytes 15:8 as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 133 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §4.1.5.8 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes NSG bytes 7:0, NCG bytes 15:8, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §4.1.5.8, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 133. Annotate the bytes containing NSG bytes 7:0, decode them, and independently verify NCG bytes 15:8. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of NSG bytes 7:0 in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand NSG bytes 7:0 and state its unit or object scope?
2. Can the reader explain why NCG bytes 15:8 is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** NSG bytes 7:0, NCG bytes 15:8, byte units

**Source keyword index:** none

> Source: NVME-NVM-CS-1.3, Rev. 1.3, §4.1.5.8, Figure 133, printed pages 108, PDF pages 108

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 139: Controller List Format</strong></summary>

<!-- claim:BASENSMGMT-FIG-139-CLAIM figure-table:BASENSMGMT-FIG-139 -->

**SPEC.** Figure 139, "Controller List Format": Defines the concrete layout or value relationships for Controller List Format. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is NUMCIDS, Controller Identifier list, 4096 bytes.

#### Where this Figure fits

Figure 139 sits in §4.6.1 and acts as a layout checkpoint. Read it after the report mental model has established the owning object and before software turns NUMCIDS into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a structure or capability field table. Locate it using the structure base and offset, read in byte/bit order, and separate capability gates, value encoding, and reserved areas. Presence in the table does not mean the function is supported.

#### Teaching redraw

```text
[Locate source: NUMCIDS]
          ↓
[Extract field: Controller Identifier list] → [Apply encoding: 4096 bytes]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `NUMCIDS` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `Controller Identifier list` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `4096 bytes` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §4.6.1 is the applicable context.
2. Decode NUMCIDS at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check Controller Identifier list as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
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
| It answers | How the cited section organizes NUMCIDS, Controller Identifier list, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §4.6.1, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 139. Annotate the bytes containing NUMCIDS, decode them, and independently verify Controller Identifier list. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

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
2. Can the reader explain why Controller Identifier list is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** NUMCIDS, Controller Identifier list, 4096 bytes

**Source keyword index:** `may`

> Source: NVME-BASE-2.4, Rev. 2.4, §4.6.1, Figure 139, printed pages 172, PDF pages 198

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 155: Asynchronous Event Information - Notice</strong></summary>

<!-- claim:BASENSMGMT-FIG-155-CLAIM figure-table:BASENSMGMT-FIG-155 -->

**SPEC.** Figure 155, "Asynchronous Event Information - Notice": Defines the concrete layout or value relationships for Asynchronous Event Information - Notice. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is Attached Namespace Attribute Changed, Allocated Namespace Attribute Changed, CNS 02h, CNS 10h.

#### Where this Figure fits

Figure 155 sits in §5.2.2.1 and acts as a layout checkpoint. Read it after the report mental model has established the owning object and before software turns Attached Namespace Attribute Changed into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a structure or capability field table. Locate it using the structure base and offset, read in byte/bit order, and separate capability gates, value encoding, and reserved areas. Presence in the table does not mean the function is supported.

#### Teaching redraw

```text
[Locate source: Attached Namespace Attribute Changed]
          ↓
[Extract field: Allocated Namespace Attribute Changed] → [Apply encoding: CNS 02h]
                                      ↓
[Validate evidence: CNS 10h]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `Attached Namespace Attribute Changed` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `Allocated Namespace Attribute Changed` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `CNS 02h` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `CNS 10h` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §5.2.2.1 is the applicable context.
2. Decode Attached Namespace Attribute Changed at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check Allocated Namespace Attribute Changed as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
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
| It answers | How the cited section organizes Attached Namespace Attribute Changed, Allocated Namespace Attribute Changed, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §5.2.2.1, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 155. Annotate the bytes containing Attached Namespace Attribute Changed, decode them, and independently verify Allocated Namespace Attribute Changed. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of Attached Namespace Attribute Changed in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand Attached Namespace Attribute Changed and state its unit or object scope?
2. Can the reader explain why Allocated Namespace Attribute Changed is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** Attached Namespace Attribute Changed, Allocated Namespace Attribute Changed, CNS 02h, CNS 10h

**Source keyword index:** `shall not`, `shall`, `may`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.2.1, Figure 155, printed pages 186, PDF pages 212

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 203: Get Log Page - Data Pointer</strong></summary>

<!-- claim:BASENSMGMT-FIG-203-CLAIM figure-table:BASENSMGMT-FIG-203 -->

**SPEC.** Figure 203, "Get Log Page - Data Pointer": Connects Get Log Page - Data Pointer to the Self-test evidence path or namespace lifecycle. Identify the object and lifecycle state, decode DPTR, LID 06h destination buffer, then verify the next transition with a CQE, log, event, or Identify snapshot.

#### Where this Figure fits

Figure 203 sits in §5.2.13 and acts as a command checkpoint. Read it after the report mental model has established the owning object and before software turns DPTR into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a command-construction field table. Build the common SQE, locate the specified CDW, encode each bit range, clear reserved bits, and validate the result against transfer length, buffer, and completion status. Equal field names do not imply equal semantics across commands.

#### Teaching redraw

```text
[Locate source: DPTR]
          ↓
[Extract field: LID 06h destination buffer] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `DPTR` | Data Pointer, the SQE field identifying a command data buffer. |
| `LID 06h destination buffer` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §5.2.13 is the applicable context.
2. Decode DPTR at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check LID 06h destination buffer as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
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
| It answers | How the cited section organizes DPTR, LID 06h destination buffer, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §5.2.13, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 203. Annotate the bytes containing DPTR, decode them, and independently verify LID 06h destination buffer. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

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
2. Can the reader explain why LID 06h destination buffer is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** DPTR, LID 06h destination buffer

**Source keyword index:** none

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13, Figure 203, printed pages 213, PDF pages 239

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 204: Get Log Page - Command Dword 10</strong></summary>

<!-- claim:BASENSMGMT-FIG-204-CLAIM figure-table:BASENSMGMT-FIG-204 -->

**SPEC.** Figure 204, "Get Log Page - Command Dword 10": Defines command-specific fields in CDW10 for Get Log Page. Locate CDW10, then decode the named fields without borrowing semantics from another command. Evidence index: NUMDL, RAE, LSP, LID 06h.

#### Where this Figure fits

Figure 204 sits in §5.2.13 and acts as a command checkpoint. Read it after the report mental model has established the owning object and before software turns NUMDL into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a command-construction field table. Build the common SQE, locate the specified CDW, encode each bit range, clear reserved bits, and validate the result against transfer length, buffer, and completion status. Equal field names do not imply equal semantics across commands.

#### Teaching redraw

```text
[Locate source: NUMDL]
          ↓
[Extract field: RAE] → [Apply encoding: LSP]
                                      ↓
[Validate evidence: LID 06h]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `NUMDL` | Number of Dwords Lower, the low 16 bits of Get Log Page NUMD. |
| `RAE` | Retain Asynchronous Event, the Get Log Page selector controlling retention of a related asynchronous event. |
| `LSP` | Log Specific Field, a command selector whose meaning is defined by the selected log page. |
| `LID 06h` | Identifier 06h for the Device Self-test Log Page, containing current operation state and twenty historical results. |

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

**Source field index:** NUMDL, RAE, LSP, LID 06h

**Source keyword index:** `shall`, `should`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13, Figure 204, printed pages 213, PDF pages 239

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 205: Get Log Page - Command Dword 11</strong></summary>

<!-- claim:BASENSMGMT-FIG-205-CLAIM figure-table:BASENSMGMT-FIG-205 -->

**SPEC.** Figure 205, "Get Log Page - Command Dword 11": Defines command-specific fields in CDW11 for Get Log Page. Locate CDW11, then decode the named fields without borrowing semantics from another command. Evidence index: LSI, NUMDU.

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
<summary><strong>NVME-BASE-2.4 — Figure 206: Get Log Page - Command Dword 12</strong></summary>

<!-- claim:BASENSMGMT-FIG-206-CLAIM figure-table:BASENSMGMT-FIG-206 -->

**SPEC.** Figure 206, "Get Log Page - Command Dword 12": Defines command-specific fields in CDW12 for Get Log Page. Locate CDW12, then decode the named fields without borrowing semantics from another command. Evidence index: LPOL, OT.

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
<summary><strong>NVME-BASE-2.4 — Figure 207: Get Log Page - Command Dword 13</strong></summary>

<!-- claim:BASENSMGMT-FIG-207-CLAIM figure-table:BASENSMGMT-FIG-207 -->

**SPEC.** Figure 207, "Get Log Page - Command Dword 13": Defines command-specific fields in CDW13 for Get Log Page. Locate CDW13, then decode the named fields without borrowing semantics from another command. Evidence index: LPOU.

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
<summary><strong>NVME-BASE-2.4 — Figure 208: Get Log Page - Command Dword 14</strong></summary>

<!-- claim:BASENSMGMT-FIG-208-CLAIM figure-table:BASENSMGMT-FIG-208 -->

**SPEC.** Figure 208, "Get Log Page - Command Dword 14": Defines command-specific fields in CDW14 for Get Log Page. Locate CDW14, then decode the named fields without borrowing semantics from another command. Evidence index: CSI, OT, UIDX.

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
| `CSI` | Command Set Identifier, selecting the I/O Command Set context for a command or log page. |
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
<summary><strong>NVME-BASE-2.4 — Figure 209: Get Log Page - Log Page Identifiers</strong></summary>

<!-- claim:BASENSMGMT-FIG-209-CLAIM figure-table:BASENSMGMT-FIG-209 -->

**SPEC.** Figure 209, "Get Log Page - Log Page Identifiers": Defines the identifier composition or namespace of values shown by Get Log Page - Log Page Identifiers. Keep the value width, issuing authority, uniqueness scope, and reserved values separate. Evidence index: LID 06h, CSI = N, Controller / Domain / NVM subsystem, Device Self-test.

#### Where this Figure fits

Figure 209 sits in §5.2.13 and acts as a identifier checkpoint. Read it after the report mental model has established the owning object and before software turns LID 06h into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is an identifier-format Figure. Record width and encoding, then identify assignment authority, uniqueness scope, reserved values, and lifetime. Equal-width identifiers are not automatically interchangeable.

#### Teaching redraw

```text
[Locate source: LID 06h]
          ↓
[Extract field: CSI = N] → [Apply encoding: Controller / Domain / NVM subsystem]
                                      ↓
[Validate evidence: Device Self-test]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `LID 06h` | Identifier 06h for the Device Self-test Log Page, containing current operation state and twenty historical results. |
| `CSI = N` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `Controller / Domain / NVM subsystem` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `Device Self-test` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §5.2.13 is the applicable context.
2. Decode LID 06h at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
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
| It answers | How the cited section organizes LID 06h, CSI = N, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §5.2.13, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 209. Annotate the bytes containing LID 06h, decode them, and independently verify CSI = N. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of LID 06h in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand LID 06h and state its unit or object scope?
2. Can the reader explain why CSI = N is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** LID 06h, CSI = N, Controller / Domain / NVM subsystem, Device Self-test

**Source keyword index:** `shall`, `may`, `optional`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13, Figure 209, printed pages 215-216, PDF pages 241-242

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 304: Manufacturer Default Configuration Status Log Page</strong></summary>

<!-- claim:BASENSMGMT-FIG-304-CLAIM figure-table:BASENSMGMT-FIG-304 -->

**SPEC.** Figure 304, "Manufacturer Default Configuration Status Log Page": Connects Manufacturer Default Configuration Status Log Page to the Self-test evidence path or namespace lifecycle. Identify the object and lifecycle state, decode DNCS, default namespace configuration status, then verify the next transition with a CQE, log, event, or Identify snapshot.

#### Where this Figure fits

Figure 304 sits in §5.2.13.1.31 and acts as a relationship checkpoint. Read it after the report mental model has established the owning object and before software turns DNCS into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This Figure explains a specific relationship or example. Identify each component type and owner, then decide whether each connection represents data flow, control flow, containment, or a condition. Visual placement alone creates no normative requirement.

#### Teaching redraw

```text
[Locate source: DNCS]
          ↓
[Extract field: default namespace configuration status] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `DNCS` | Default Namespace Configuration Status, indicating whether the namespace configuration matches the active firmware image defaults. |
| `default namespace configuration status` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §5.2.13.1.31 is the applicable context.
2. Decode DNCS at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check default namespace configuration status as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 304 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §5.2.13.1.31 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes DNCS, default namespace configuration status, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §5.2.13.1.31, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 304. Annotate the bytes containing DNCS, decode them, and independently verify default namespace configuration status. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of DNCS in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand DNCS and state its unit or object scope?
2. Can the reader explain why default namespace configuration status is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** DNCS, default namespace configuration status

**Source keyword index:** `shall`, `should`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.31, Figure 304, printed pages 301-302, PDF pages 327-328

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 338: Identify Controller Data Structure</strong></summary>

<!-- claim:BASENSMGMT-FIG-338-CLAIM figure-table:BASENSMGMT-FIG-338 -->

**SPEC.** Figure 338, "Identify Controller Data Structure": Defines the concrete layout or value relationships for Identify Controller Data Structure. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is OACS.DSTS, EDSTT, DSTO.SDSO, OACS.NMS, RDNCS, MAXDNA, MAXCNA.

#### Where this Figure fits

Figure 338 sits in §5.2.14.2.1 and acts as a layout checkpoint. Read it after the report mental model has established the owning object and before software turns OACS.DSTS into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a structure or capability field table. Locate it using the structure base and offset, read in byte/bit order, and separate capability gates, value encoding, and reserved areas. Presence in the table does not mean the function is supported.

#### Teaching redraw

```text
[Locate source: OACS.DSTS]
          ↓
[Extract field: EDSTT] → [Apply encoding: DSTO.SDSO]
                                      ↓
[Validate evidence: OACS.NMS]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `OACS.DSTS` | The Device Self-test Supported bit in Optional Admin Command Support, gating availability of the command. |
| `EDSTT` | Extended Device Self-test Time, the nominal extended-test duration in minutes at power state 0. |
| `DSTO.SDSO` | Device Self-test Options, the Identify Controller field reporting refresh and concurrency options. Here DSTO.SDSO selects its SDSO member field. |
| `OACS.NMS` | The Namespace Management Supported bit in Optional Admin Command Support; one advertises the complete Manage-plus-Attach capability. |
| `RDNCS` | Restore Default Namespace Configuration Supported, the capability bit advertising the Restore Default operation. |
| `MAXDNA` | Maximum Domain Namespace Attachments, limiting the aggregate attachment count across I/O controllers in a Domain. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §5.2.14.2.1 is the applicable context.
2. Decode OACS.DSTS at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check EDSTT as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
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
| It answers | How the cited section organizes OACS.DSTS, EDSTT, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §5.2.14.2.1, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 338. Annotate the bytes containing OACS.DSTS, decode them, and independently verify EDSTT. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of OACS.DSTS in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand OACS.DSTS and state its unit or object scope?
2. Can the reader explain why EDSTT is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** OACS.DSTS, EDSTT, DSTO.SDSO, OACS.NMS, RDNCS, MAXDNA, MAXCNA

**Source keyword index:** `shall not`, `should not`, `shall`, `should`, `may`, `optional`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.14.2.1, Figure 338, printed pages 340, 353, 365, 378, PDF pages 366, 379, 391, 404

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 346: Identify - I/O Command Set Independent Identify Namespace Data Structure</strong></summary>

<!-- claim:BASENSMGMT-FIG-346-CLAIM figure-table:BASENSMGMT-FIG-346 -->

**SPEC.** Figure 346, "Identify - I/O Command Set Independent Identify Namespace Data Structure": Defines the concrete layout or value relationships for Identify - I/O Command Set Independent Identify Namespace Data Structure. Follow byte/bit order, length, access type, and reserved areas; the source-derived evidence index is ANAGRPID, NVMSETID, ENDGID.

#### Where this Figure fits

Figure 346 sits in §5.2.14.2.3 and acts as a hierarchy checkpoint. Read it after the report mental model has established the owning object and before software turns ANAGRPID into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is an object or capacity relationship Figure. Separate containment, accessibility, identifier reference, and sharing. Adjacent boxes need not be one-to-one, and an identifier is not the physical or logical object it references.

#### Teaching redraw

```text
[Locate source: ANAGRPID]
          ↓
[Extract field: NVMSETID] → [Apply encoding: ENDGID]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `ANAGRPID` | ANA Group Identifier, identifying the Asymmetric Namespace Access group for a namespace; zero at create lets the controller choose. |
| `NVMSETID` | NVM Set Identifier, selecting the NVM Set from which capacity is allocated when creating a namespace. |
| `ENDGID` | Endurance Group Identifier, selecting the Endurance Group for a created namespace. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §5.2.14.2.3 is the applicable context.
2. Decode ANAGRPID at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check NVMSETID as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
4. Keep reserved values uninterpreted and record the raw bytes or register value before converting the result into a software state.

#### Input → Decode → Validate → Evidence worksheet

| Stage | Record | Stop condition |
|---|---|---|
| Input | Complete raw register, buffer, or CQE snapshot for Figure 346 | Object, scope, or snapshot timing is unknown |
| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |
| Validate | §5.2.14.2.3 conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |
| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |

#### What it answers and what it does not

| Reading level | Content |
|---|---|
| It answers | How the cited section organizes ANAGRPID, NVMSETID, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §5.2.14.2.3, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 346. Annotate the bytes containing ANAGRPID, decode them, and independently verify NVMSETID. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of ANAGRPID in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand ANAGRPID and state its unit or object scope?
2. Can the reader explain why NVMSETID is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** ANAGRPID, NVMSETID, ENDGID

**Source keyword index:** `shall`, `should`, `may`, `optional`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.14.2.3, Figure 346, printed pages 391-394, PDF pages 417-420

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 474: Asynchronous Event Configuration - Command Dword 11</strong></summary>

<!-- claim:BASENSMGMT-FIG-474-CLAIM figure-table:BASENSMGMT-FIG-474 -->

**SPEC.** Figure 474, "Asynchronous Event Configuration - Command Dword 11": Defines command-specific fields in CDW11 for Asynchronous Event Configuration. Locate CDW11, then decode the named fields without borrowing semantics from another command. Evidence index: Attached Namespace Attribute Notices, Allocated Namespace Attribute Notices.

#### Where this Figure fits

Figure 474 sits in §5.2.30.1.6 and acts as a command checkpoint. Read it after the report mental model has established the owning object and before software turns Attached Namespace Attribute Notices into a decision. The Figure supports the cited section; it is not a substitute for the surrounding normative text.

This is a command-construction field table. Build the common SQE, locate the specified CDW, encode each bit range, clear reserved bits, and validate the result against transfer length, buffer, and completion status. Equal field names do not imply equal semantics across commands.

#### Teaching redraw

```text
[Locate source: Attached Namespace Attribute Notices]
          ↓
[Extract field: Allocated Namespace Attribute Notices] → [Apply encoding: evidence]
                                      ↓
[Validate evidence: evidence]
```

#### Terms to learn before reading

| Term | Plain-language meaning |
|---|---|
| `Attached Namespace Attribute Notices` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |
| `Allocated Namespace Attribute Notices` | A source field label in this Figure. Its bit range, value encoding, and conditions are read from the cited Figure before the value is used. |

#### Read in this order

1. Locate the structure, register, queue, or object named by the caption and confirm that §5.2.30.1.6 is the applicable context.
2. Decode Attached Namespace Attribute Notices at its stated width and position; do not infer its unit or reset behavior from the abbreviation.
3. Cross-check Allocated Namespace Attribute Notices as an independent condition, then validate every count, address, selector, or state against the returned buffer and capability gates.
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
| It answers | How the cited section organizes Attached Namespace Attribute Notices, Allocated Namespace Attribute Notices, and the other indexed fields. |
| It does not answer | Whether an optional capability is implemented, whether a command completed, or whether a value from another scope is equivalent. |
| Cross-check | The surrounding text in §5.2.30.1.6, the capability that enables the structure, and the actual transfer or register width. |

**Informative example.** Informative example: capture the raw value or buffer associated with Figure 474. Annotate the bytes containing Attached Namespace Attribute Notices, decode them, and independently verify Allocated Namespace Attribute Notices. If either field exceeds the returned boundary, selects a reserved encoding, or conflicts with the capability context, stop the parser or command builder and report the exact field rather than continuing with a guessed default. This example describes a verification method and adds no requirement.

**Common misconception.** A common misreading is to treat the presence of Attached Namespace Attribute Notices in the Figure as proof that the capability is enabled or that the value is valid. A layout defines where and how to interpret a field when applicable; support, state, command outcome, and scope still come from their own gates and surrounding requirements.

#### Debug matrix

| Symptom | First checks |
|---|---|
| Wrong value | Check byte/bit range, endian, radix, zero-based encoding, and unit. |
| Intermittent behavior | Check ownership, update order, snapshot timing, and whether two actors share the object. |
| Parser overrun | Compare declared count/length with actual returned bytes before walking the next entry. |
| Unexpected status | Preserve the full category and context; do not log an isolated numeric code. |

#### Questions the reader should now answer

1. Can the reader expand Attached Namespace Attribute Notices and state its unit or object scope?
2. Can the reader explain why Allocated Namespace Attribute Notices is checked separately?
3. Can the reader identify the raw evidence that would distinguish an encoding error from a real controller state?

**Source field index:** Attached Namespace Attribute Notices, Allocated Namespace Attribute Notices

**Source keyword index:** `shall not`, `shall`, `reserved`

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.6, Figure 474, printed pages 466-468, PDF pages 492-494

</details>

## Use and limitations

Use the claim IDs as stable PPT traceability keys. Re-check affected claims if the source revision, errata set, or approved scope changes.

## Self-questions and worked answers

32 answered questions revisit this report's scope. Each answer retains the same source links as the teaching module; calculations and debugging examples are informative.

### Q01. What is the governing interpretation for “Separate two lifecycles: diagnostic evidence and namespace provisioning”?

<!-- qa:base-self-test-namespace-management-diagnostic-and-provisioning-lead -->

**Answer.**

Device Self-test and Namespace Management both use Admin commands but mutate different objects. Self-test creates a background operation: its command CQE is only an acceptance point and LID 06h proves the outcome. Namespace Management creates or removes a namespace object: Create returns an NSID, but Attachment is still required to establish controller access. Separating the tracks explains why completion is not always the endpoint.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.6, printed pages 201, PDF pages 227; Source: NVME-BASE-2.4, Rev. 2.4, §8.1.17, printed pages 660, PDF pages 686; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.25, 8.1.17.1, printed pages 446-448, 662, PDF pages 472-474, 688

### Q02. Which concepts or conditions must be distinguished in “Separate two lifecycles: diagnostic evidence and namespace provisioning”?

<!-- qa:base-self-test-namespace-management-diagnostic-and-provisioning-rows -->

**Answer.**

- Self-test object — Background operation — CQE→current state→history result
- Namespace object — Allocated capacity and format — Create CQE DW0→NSID
- Access relationship — Namespace-to-controller attachment — Attach CQE→Active NSID list
- Inventory evidence — Allocated/Active lists — Refresh Identify after AEN

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.6, printed pages 201, PDF pages 227; Source: NVME-BASE-2.4, Rev. 2.4, §8.1.17, printed pages 660, PDF pages 686; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.25, 8.1.17.1, printed pages 446-448, 662, PDF pages 472-474, 688

### Q03. How does “Separate two lifecycles: diagnostic evidence and namespace provisioning” apply to a concrete calculation or operational scenario?

<!-- qa:base-self-test-namespace-management-diagnostic-and-provisioning-example -->

**Answer.**

A Create completion returning NSID 7 proves that namespace 7 exists, but it is still unattached and cannot immediately receive I/O. Likewise, a successful Self-test start CQE proves only that an operation began, not that the test passed. Each CQE needs later evidence, but the evidence types differ.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.6, printed pages 201, PDF pages 227; Source: NVME-BASE-2.4, Rev. 2.4, §8.1.17, printed pages 660, PDF pages 686; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.25, 8.1.17.1, printed pages 446-448, 662, PDF pages 472-474, 688

### Q04. What misinterpretation is most likely in “Separate two lifecycles: diagnostic evidence and namespace provisioning”, and how is it debugged?

<!-- qa:base-self-test-namespace-management-diagnostic-and-provisioning-pitfall -->

**Answer.**

Do not summarize the flow as a successful Admin command. A trace labels the object changed, the boundary crossed by success, and the LID, Identify, or event evidence still outstanding.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.6, printed pages 201, PDF pages 227; Source: NVME-BASE-2.4, Rev. 2.4, §8.1.17, printed pages 660, PDF pages 686; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.25, 8.1.17.1, printed pages 446-448, 662, PDF pages 472-474, 688

### Q05. What is the governing interpretation for “Device Self-test: from capability gate to an LID 06h result”?

<!-- qa:base-self-test-namespace-management-selftest-command-state-machine-lead -->

**Answer.**

Use OACS.DSTS, EDSTT, and DSTO.SDSO to establish support, timing, and concurrency expectations before constructing the command from NSID and STC. After the CQE, poll DSTOS/DSTCS. At operation end, RDS1 is created before current status is cleared, preventing software from losing the final result during a transition window.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.14.2.1, 8.1.8, printed pages 353-358, 614, PDF pages 379-384, 640; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.6, printed pages 199, PDF pages 225; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.6, printed pages 199-200, PDF pages 225-226; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.7, printed pages 229-230, PDF pages 255-256; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.7, printed pages 229-232, PDF pages 255-258; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.7, printed pages 231-232, PDF pages 257-258; Source: NVME-NVM-CS-1.3, Rev. 1.3, §4.1.4.3, printed pages 76, PDF pages 76

### Q06. Which concepts or conditions must be distinguished in “Device Self-test: from capability gate to an LID 06h result”?

<!-- qa:base-self-test-namespace-management-selftest-command-state-machine-rows -->

**Answer.**

- NSID=0 — Controller only — No namespace media
- Active NSID — One namespace — Separate invalid/inactive status
- NSID=FFFFFFFFh — Accessible attached set at start — The set is not tracked dynamically
- STC=Fh — Abort current operation — Write result before clearing current

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.14.2.1, 8.1.8, printed pages 353-358, 614, PDF pages 379-384, 640; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.6, printed pages 199, PDF pages 225; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.6, printed pages 199-200, PDF pages 225-226; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.7, printed pages 229-230, PDF pages 255-256; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.7, printed pages 229-232, PDF pages 255-258; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.7, printed pages 231-232, PDF pages 257-258; Source: NVME-NVM-CS-1.3, Rev. 1.3, §4.1.4.3, printed pages 76, PDF pages 76

### Q07. How does “Device Self-test: from capability gate to an LID 06h result” apply to a concrete calculation or operational scenario?

<!-- qa:base-self-test-namespace-management-selftest-command-state-machine-example -->

**Answer.**

For a complete LID 06h read, 564/4 is 141 dwords and NUMD is 141−1=140=008Ch. With RAE zero, LSP zero, and LID 06h, CDW10 is 008C0006h. If RDS1.DSTS is 17h, DSTC 1h means short and DSTR 7h is the condition that permits reading SEGN.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.14.2.1, 8.1.8, printed pages 353-358, 614, PDF pages 379-384, 640; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.6, printed pages 199, PDF pages 225; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.6, printed pages 199-200, PDF pages 225-226; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.7, printed pages 229-230, PDF pages 255-256; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.7, printed pages 229-232, PDF pages 255-258; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.7, printed pages 231-232, PDF pages 257-258; Source: NVME-NVM-CS-1.3, Rev. 1.3, §4.1.4.3, printed pages 76, PDF pages 76

### Q08. What misinterpretation is most likely in “Device Self-test: from capability gate to an LID 06h result”, and how is it debugged?

<!-- qa:base-self-test-namespace-management-selftest-command-state-machine-pitfall -->

**Answer.**

A nonzero FLBA is not valid evidence. Decode DSTR, check FVLD and NSIDVLD, and only then apply the NVM Command Set meaning for FLBA bytes 23:16. Preserve the raw 28-byte entry.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.14.2.1, 8.1.8, printed pages 353-358, 614, PDF pages 379-384, 640; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.6, printed pages 199, PDF pages 225; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.6, printed pages 199-200, PDF pages 225-226; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.7, printed pages 229-230, PDF pages 255-256; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.7, printed pages 229-232, PDF pages 255-258; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.7, printed pages 231-232, PDF pages 257-258; Source: NVME-NVM-CS-1.3, Rev. 1.3, §4.1.4.3, printed pages 76, PDF pages 76

### Q09. What is the governing interpretation for “Put three capacity values and two granularities into one byte model”?

<!-- qa:base-self-test-namespace-management-capacity-granularity-math-lead -->

**Answer.**

NSZE, NCAP, and NUSE use logical blocks; NSG and NCG use bytes; and actual NVM consumption may be rounded to an allocation unit. Convert with the selected LBA size before comparing. NSZE≥NCAP≥NUSE is a capacity relationship, while NSG/NCG divisibility is a waste-minimization hint, not the same kind of gate.

> Source: NVME-NVM-CS-1.3, Rev. 1.3, §2.1.1, printed pages 13-14, PDF pages 13-14; Source: NVME-NVM-CS-1.3, Rev. 1.3, §2.1.1, printed pages 13, PDF pages 13; Source: NVME-BASE-2.4, Rev. 2.4, §8.1.17, printed pages 661, PDF pages 687; Source: NVME-NVM-CS-1.3, Rev. 1.3, §5.8, printed pages 165, PDF pages 165; Source: NVME-NVM-CS-1.3, Rev. 1.3, §5.8, printed pages 165, PDF pages 165

### Q10. Which concepts or conditions must be distinguished in “Put three capacity values and two granularities into one byte model”?

<!-- qa:base-self-test-namespace-management-capacity-granularity-math-rows -->

**Answer.**

- NSZE — Logical blocks — LBA 0 through NSZE−1
- NCAP — Logical blocks — Maximum allocatable capacity
- NUSE — Logical blocks — Tracked when THINP is one
- NSG/NCG — Bytes — Preferred hint, not a sole abort gate

> Source: NVME-NVM-CS-1.3, Rev. 1.3, §2.1.1, printed pages 13-14, PDF pages 13-14; Source: NVME-NVM-CS-1.3, Rev. 1.3, §2.1.1, printed pages 13, PDF pages 13; Source: NVME-BASE-2.4, Rev. 2.4, §8.1.17, printed pages 661, PDF pages 687; Source: NVME-NVM-CS-1.3, Rev. 1.3, §5.8, printed pages 165, PDF pages 165; Source: NVME-NVM-CS-1.3, Rev. 1.3, §5.8, printed pages 165, PDF pages 165

### Q11. How does “Put three capacity values and two granularities into one byte model” apply to a concrete calculation or operational scenario?

<!-- qa:base-self-test-namespace-management-capacity-granularity-math-example -->

**Answer.**

With 4-KiB LBAs, NSG 1 MiB, and NCG 2 MiB, NSZE=NCAP=1024 represents 4 MiB, is divisible by both hints, and is fully provisioned. NSZE=NCAP=1000 represents 3,906.25 KiB and violates both hints. Allocation capacity may be wasted, but an otherwise valid create is not aborted solely for this reason.

> Source: NVME-NVM-CS-1.3, Rev. 1.3, §2.1.1, printed pages 13-14, PDF pages 13-14; Source: NVME-NVM-CS-1.3, Rev. 1.3, §2.1.1, printed pages 13, PDF pages 13; Source: NVME-BASE-2.4, Rev. 2.4, §8.1.17, printed pages 661, PDF pages 687; Source: NVME-NVM-CS-1.3, Rev. 1.3, §5.8, printed pages 165, PDF pages 165; Source: NVME-NVM-CS-1.3, Rev. 1.3, §5.8, printed pages 165, PDF pages 165

### Q12. What misinterpretation is most likely in “Put three capacity values and two granularities into one byte model”, and how is it debugged?

<!-- qa:base-self-test-namespace-management-capacity-granularity-math-pitfall -->

**Answer.**

A common error divides NSZE 1024 directly by NSG 1 MiB or treats a granularity violation as Invalid Field. The worksheet lists raw blocks, LBA bytes, converted bytes, remainder, and the controller allocation unit.

> Source: NVME-NVM-CS-1.3, Rev. 1.3, §2.1.1, printed pages 13-14, PDF pages 13-14; Source: NVME-NVM-CS-1.3, Rev. 1.3, §2.1.1, printed pages 13, PDF pages 13; Source: NVME-BASE-2.4, Rev. 2.4, §8.1.17, printed pages 661, PDF pages 687; Source: NVME-NVM-CS-1.3, Rev. 1.3, §5.8, printed pages 165, PDF pages 165; Source: NVME-NVM-CS-1.3, Rev. 1.3, §5.8, printed pages 165, PDF pages 165

### Q13. What is the governing interpretation for “Create payload: the Base envelope contains 512 NVM-specific bytes”?

<!-- qa:base-self-test-namespace-management-namespace-create-payload-lead -->

**Answer.**

Base Figure 448 defines a 4096-byte envelope, while NVM Command Set Figure 134 defines NVM fields and the Placement Handle List within the first 768 bytes. The host selects operation and command set through SEL/CSI, then fills NSZE, NCAP, format, protection, sharing, and group identifiers. Reserved regions are zeroed, while Protection Information and FDP have separate capability gates.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.25, printed pages 446-448, PDF pages 472-474; Source: NVME-NVM-CS-1.3, Rev. 1.3, §4.1.6.4, printed pages 111-113, PDF pages 111-113; Source: NVME-NVM-CS-1.3, Rev. 1.3, §4.1.6.2, printed pages 110, PDF pages 110; Source: NVME-NVM-CS-1.3, Rev. 1.3, §4.1.6.3, printed pages 110-111, PDF pages 110-111; Source: NVME-BASE-2.4, Rev. 2.4, §8.1.17, printed pages 661, PDF pages 687

### Q14. Which concepts or conditions must be distinguished in “Create payload: the Base envelope contains 512 NVM-specific bytes”?

<!-- qa:base-self-test-namespace-management-namespace-create-payload-rows -->

**Answer.**

- Base 0:511 — SIOCS — NVM-specific create data
- Base 512:1023 — Reserved — Host clears to zero
- Base 1024:4095 — Vendor Specific — Do not invent a meaning
- NVM 512:767 — Placement Handle List — Validated only when FDP is enabled

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.25, printed pages 446-448, PDF pages 472-474; Source: NVME-NVM-CS-1.3, Rev. 1.3, §4.1.6.4, printed pages 111-113, PDF pages 111-113; Source: NVME-NVM-CS-1.3, Rev. 1.3, §4.1.6.2, printed pages 110, PDF pages 110; Source: NVME-NVM-CS-1.3, Rev. 1.3, §4.1.6.3, printed pages 110-111, PDF pages 110-111; Source: NVME-BASE-2.4, Rev. 2.4, §8.1.17, printed pages 661, PDF pages 687

### Q15. How does “Create payload: the Base envelope contains 512 NVM-specific bytes” apply to a concrete calculation or operational scenario?

<!-- qa:base-self-test-namespace-management-namespace-create-payload-example -->

**Answer.**

To create a 4-MiB namespace with 4096-byte LBAs, set NSZE and NCAP to 1024, so bytes 7:0 and 15:8 each contain 0000000000000400h. NVMSETID zero with ENDGID five lets the controller select an NVM Set inside Endurance Group five; NVMSETID seven with ENDGID zero is Invalid Field.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.25, printed pages 446-448, PDF pages 472-474; Source: NVME-NVM-CS-1.3, Rev. 1.3, §4.1.6.4, printed pages 111-113, PDF pages 111-113; Source: NVME-NVM-CS-1.3, Rev. 1.3, §4.1.6.2, printed pages 110, PDF pages 110; Source: NVME-NVM-CS-1.3, Rev. 1.3, §4.1.6.3, printed pages 110-111, PDF pages 110-111; Source: NVME-BASE-2.4, Rev. 2.4, §8.1.17, printed pages 661, PDF pages 687

### Q16. What misinterpretation is most likely in “Create payload: the Base envelope contains 512 NVM-specific bytes”, and how is it debugged?

<!-- qa:base-self-test-namespace-management-namespace-create-payload-pitfall -->

**Answer.**

Do not dump only Figure 134 values. Debug evidence also retains LBA-format capability, LBAFEE, Figure 127 masking limits, FDP enablement, the complete 4096-byte buffer, and a reserved-byte scan.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.25, printed pages 446-448, PDF pages 472-474; Source: NVME-NVM-CS-1.3, Rev. 1.3, §4.1.6.4, printed pages 111-113, PDF pages 111-113; Source: NVME-NVM-CS-1.3, Rev. 1.3, §4.1.6.2, printed pages 110, PDF pages 110; Source: NVME-NVM-CS-1.3, Rev. 1.3, §4.1.6.3, printed pages 110-111, PDF pages 110-111; Source: NVME-BASE-2.4, Rev. 2.4, §8.1.17, printed pages 661, PDF pages 687

### Q17. What is the governing interpretation for “Namespace lifecycle: Create builds the object; Attach establishes access”?

<!-- qa:base-self-test-namespace-management-namespace-lifecycle-lead -->

**Answer.**

Create, Attach, Detach, and Delete change two dimensions: whether the namespace is allocated and whether a controller is attached. After Create returns NSID in CQE DW0, the object is allocated but no controller is attached. A Controller List in Attach establishes access. Detach preserves capacity, while Delete makes the NSID unallocated.

> Source: NVME-BASE-2.4, Rev. 2.4, §8.1.17, printed pages 660, PDF pages 686; Source: NVME-BASE-2.4, Rev. 2.4, §8.1.17, printed pages 660, PDF pages 686; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.24, printed pages 444-445, PDF pages 470-471; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.24, printed pages 444-445, PDF pages 470-471; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.25, 8.1.17.1, printed pages 446-448, 662, PDF pages 472-474, 688

### Q18. Which concepts or conditions must be distinguished in “Namespace lifecycle: Create builds the object; Attach establishes access”?

<!-- qa:base-self-test-namespace-management-namespace-lifecycle-rows -->

**Answer.**

- Create — Object/capacity — Does not attach automatically
- Attach — Access relationship — Controller List may contain multiple CNTLIDs
- Detach — Controller-local active state — Namespace remains allocated
- Delete — Subsystem inventory — NSID becomes unallocated

> Source: NVME-BASE-2.4, Rev. 2.4, §8.1.17, printed pages 660, PDF pages 686; Source: NVME-BASE-2.4, Rev. 2.4, §8.1.17, printed pages 660, PDF pages 686; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.24, printed pages 444-445, PDF pages 470-471; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.24, printed pages 444-445, PDF pages 470-471; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.25, 8.1.17.1, printed pages 446-448, 662, PDF pages 472-474, 688

### Q19. How does “Namespace lifecycle: Create builds the object; Attach establishes access” apply to a concrete calculation or operational scenario?

<!-- qa:base-self-test-namespace-management-namespace-lifecycle-example -->

**Answer.**

Create returns NSID seven. A Controller List names controllers three and five through NUMCIDS and its entries. After Attach, NSID seven is active on both. Detaching only controller three leaves it inactive there and active on controller five, while the namespace remains allocated.

> Source: NVME-BASE-2.4, Rev. 2.4, §8.1.17, printed pages 660, PDF pages 686; Source: NVME-BASE-2.4, Rev. 2.4, §8.1.17, printed pages 660, PDF pages 686; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.24, printed pages 444-445, PDF pages 470-471; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.24, printed pages 444-445, PDF pages 470-471; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.25, 8.1.17.1, printed pages 446-448, 662, PDF pages 472-474, 688

### Q20. What misinterpretation is most likely in “Namespace lifecycle: Create builds the object; Attach establishes access”, and how is it debugged?

<!-- qa:base-self-test-namespace-management-namespace-lifecycle-pitfall -->

**Answer.**

Equal NSID values do not imply equal active state on every controller. Inventory and I/O traces carry controller ID, while attachment limits separately check Domain MAXDNA and per-controller MAXCNA.

> Source: NVME-BASE-2.4, Rev. 2.4, §8.1.17, printed pages 660, PDF pages 686; Source: NVME-BASE-2.4, Rev. 2.4, §8.1.17, printed pages 660, PDF pages 686; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.24, printed pages 444-445, PDF pages 470-471; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.24, printed pages 444-445, PDF pages 470-471; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.25, 8.1.17.1, printed pages 446-448, 662, PDF pages 472-474, 688

### Q21. What is the governing interpretation for “Delete and Restore Default: empty inventory before crossing the configuration boundary”?

<!-- qa:base-self-test-namespace-management-delete-restore-state-lead -->

**Answer.**

Delete All and Restore Default are different operations. Delete with NSID FFFFFFFFh succeeds even when no namespaces exist. Restore Default requires RDNCS, SEL 2h, and an empty subsystem inventory. Before successful completion, the controller applies defaults for the current active firmware image and sets DNCS to one.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.25, 8.1.17.1, printed pages 446, 448, 662, PDF pages 472, 474, 688; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.25.1, printed pages 447-448, PDF pages 473-474; Source: NVME-BASE-2.4, Rev. 2.4, §8.1.17.1-8.1.17.2, printed pages 662-663, PDF pages 688-689

### Q22. Which concepts or conditions must be distinguished in “Delete and Restore Default: empty inventory before crossing the configuration boundary”?

<!-- qa:base-self-test-namespace-management-delete-restore-state-rows -->

**Answer.**

- Delete one — NSID=target — Object is gone after success
- Delete all — NSID=FFFFFFFFh — Succeeds with zero namespaces
- Restore — SEL=2h, NSID ignored — Remaining namespace→Sequence Error
- Post-condition — DNCS=1 — Refresh Identify for actual defaults

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.25, 8.1.17.1, printed pages 446, 448, 662, PDF pages 472, 474, 688; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.25.1, printed pages 447-448, PDF pages 473-474; Source: NVME-BASE-2.4, Rev. 2.4, §8.1.17.1-8.1.17.2, printed pages 662-663, PDF pages 688-689

### Q23. How does “Delete and Restore Default: empty inventory before crossing the configuration boundary” apply to a concrete calculation or operational scenario?

<!-- qa:base-self-test-namespace-management-delete-restore-state-example -->

**Answer.**

Detach NSID seven and delete it, then confirm that the Allocated Namespace ID list is empty. If RDNCS is one, issue SEL 2h with NSID zero. After the successful CQE, read DNCS one and re-enumerate default namespaces. DNCS is state evidence, not a complete description of the default layout.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.25, 8.1.17.1, printed pages 446, 448, 662, PDF pages 472, 474, 688; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.25.1, printed pages 447-448, PDF pages 473-474; Source: NVME-BASE-2.4, Rev. 2.4, §8.1.17.1-8.1.17.2, printed pages 662-663, PDF pages 688-689

### Q24. What misinterpretation is most likely in “Delete and Restore Default: empty inventory before crossing the configuration boundary”, and how is it debugged?

<!-- qa:base-self-test-namespace-management-delete-restore-state-pitfall -->

**Answer.**

A Delete All CQE does not prove Restore completion, and DNCS alone does not reveal default NSZE or format. Preserve operation selector, inventory snapshot, CQE, and post-operation Identify at each stage.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.25, 8.1.17.1, printed pages 446, 448, 662, PDF pages 472, 474, 688; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.25.1, printed pages 447-448, PDF pages 473-474; Source: NVME-BASE-2.4, Rev. 2.4, §8.1.17.1-8.1.17.2, printed pages 662-663, PDF pages 688-689

### Q25. What is the governing interpretation for “Namespace events say inventory changed; Identify says what it became”?

<!-- qa:base-self-test-namespace-management-namespace-events-lead -->

**Answer.**

Attached and Allocated Namespace Attribute Changed notices correspond to different inventories. Create normally changes the Allocated list, Attach/Detach changes the Active list, and Delete may change both. The event code is not the new list, so the host reissues Identify with the appropriate CNS. Delete reporting also distinguishes the processing controller from other controllers.

> Source: NVME-BASE-2.4, Rev. 2.4, §8.1.17, printed pages 660, PDF pages 686; Source: NVME-BASE-2.4, Rev. 2.4, §8.1.17.1-8.1.17.2, printed pages 662-663, PDF pages 688-689; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.25, 8.1.17.1, printed pages 446-448, 662, PDF pages 472-474, 688

### Q26. Which concepts or conditions must be distinguished in “Namespace events say inventory changed; Identify says what it became”?

<!-- qa:base-self-test-namespace-management-namespace-events-rows -->

**Answer.**

- CNS 02h — Active Namespace ID list — Attached notice
- CNS 10h — Allocated Namespace ID list — Allocated notice
- Create — Allocated change — New NSID is not yet active
- Delete — Allocated and possibly Active — Processing-controller rule differs

> Source: NVME-BASE-2.4, Rev. 2.4, §8.1.17, printed pages 660, PDF pages 686; Source: NVME-BASE-2.4, Rev. 2.4, §8.1.17.1-8.1.17.2, printed pages 662-663, PDF pages 688-689; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.25, 8.1.17.1, printed pages 446-448, 662, PDF pages 472-474, 688

### Q27. How does “Namespace events say inventory changed; Identify says what it became” apply to a concrete calculation or operational scenario?

<!-- qa:base-self-test-namespace-management-namespace-events-example -->

**Answer.**

Controller three processes Delete for attached NSID seven. Other notice-enabled controllers report according to §8.1.17.2, while requirements differ for the processing controller. Instead of counting events alone, the host retains before/after Active and Allocated lists for every controller.

> Source: NVME-BASE-2.4, Rev. 2.4, §8.1.17, printed pages 660, PDF pages 686; Source: NVME-BASE-2.4, Rev. 2.4, §8.1.17.1-8.1.17.2, printed pages 662-663, PDF pages 688-689; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.25, 8.1.17.1, printed pages 446-448, 662, PDF pages 472-474, 688

### Q28. What misinterpretation is most likely in “Namespace events say inventory changed; Identify says what it became”, and how is it debugged?

<!-- qa:base-self-test-namespace-management-namespace-events-pitfall -->

**Answer.**

A common mistake treats an AEN as an inventory delta. It triggers refresh; the authoritative data is the subsequent Identify result. Before/after differences may expose a missed event, but software cannot invent a notification that was not received.

> Source: NVME-BASE-2.4, Rev. 2.4, §8.1.17, printed pages 660, PDF pages 686; Source: NVME-BASE-2.4, Rev. 2.4, §8.1.17.1-8.1.17.2, printed pages 662-663, PDF pages 688-689; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.25, 8.1.17.1, printed pages 446-448, 662, PDF pages 472-474, 688

### Q29. What is the governing interpretation for “End to end: place capacity, command, object, attachment, and evidence on one timeline”?

<!-- qa:base-self-test-namespace-management-namespace-end-to-end-debug-lead -->

**Answer.**

A namespace defect is rarely one field in isolation. The pre-create capability snapshot, 4096-byte payload, CQE DW0, Controller List, attachment limits, events, and post-Identify result must all join to one NSID and controller set. Debugging finds the first inconsistent boundary instead of guessing backward from a final I/O failure.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.24-5.2.25, printed pages 445, 448, PDF pages 471, 474; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.24-5.2.25, 8.1.17.1, printed pages 444-448, 661-663, PDF pages 470-474, 687-689; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.24, printed pages 444-445, PDF pages 470-471; Source: NVME-NVM-CS-1.3, Rev. 1.3, §4.1.6.2, printed pages 110, PDF pages 110; Source: NVME-NVM-CS-1.3, Rev. 1.3, §4.1.6.3, printed pages 110-111, PDF pages 110-111

### Q30. Which concepts or conditions must be distinguished in “End to end: place capacity, command, object, attachment, and evidence on one timeline”?

<!-- qa:base-self-test-namespace-management-namespace-end-to-end-debug-rows -->

**Answer.**

- Create Invalid Format — FLBAS/DPS/LBSTM/LBAFEE — Locate the format gate first
- Insufficient Capacity — NSZE/NCAP, unallocated bytes, group IDs — Separate logical and consumed
- Attach limit — MAXDNA/MAXCNA and prior counts — Separate Domain and controller
- I/O inactive NSID — Attach CQE, Active list, controller ID — Create success is insufficient

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.24-5.2.25, printed pages 445, 448, PDF pages 471, 474; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.24-5.2.25, 8.1.17.1, printed pages 444-448, 661-663, PDF pages 470-474, 687-689; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.24, printed pages 444-445, PDF pages 470-471; Source: NVME-NVM-CS-1.3, Rev. 1.3, §4.1.6.2, printed pages 110, PDF pages 110; Source: NVME-NVM-CS-1.3, Rev. 1.3, §4.1.6.3, printed pages 110-111, PDF pages 110-111

### Q31. How does “End to end: place capacity, command, object, attachment, and evidence on one timeline” apply to a concrete calculation or operational scenario?

<!-- qa:base-self-test-namespace-management-namespace-end-to-end-debug-example -->

**Answer.**

Case: Create returns NSID seven but Attach returns 27h. Check controller five's MAXCNA and the Domain MAXDNA prior counts. If the per-controller limit is already reached, do not modify the create payload or retry I/O. Recovery selects another controller, detaches another namespace, or stops and reports the capacity policy.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.24-5.2.25, printed pages 445, 448, PDF pages 471, 474; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.24-5.2.25, 8.1.17.1, printed pages 444-448, 661-663, PDF pages 470-474, 687-689; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.24, printed pages 444-445, PDF pages 470-471; Source: NVME-NVM-CS-1.3, Rev. 1.3, §4.1.6.2, printed pages 110, PDF pages 110; Source: NVME-NVM-CS-1.3, Rev. 1.3, §4.1.6.3, printed pages 110-111, PDF pages 110-111

### Q32. What misinterpretation is most likely in “End to end: place capacity, command, object, attachment, and evidence on one timeline”, and how is it debugged?

<!-- qa:base-self-test-namespace-management-namespace-end-to-end-debug-pitfall -->

**Answer.**

Do not retain only a human-readable status. Preserve SCT/SC/DNR, raw SQE, buffer hash, returned NSID, Controller List, timestamp, and before/after inventories so the rejected gate remains recomputable.

> Source: NVME-BASE-2.4, Rev. 2.4, §5.2.24-5.2.25, printed pages 445, 448, PDF pages 471, 474; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.24-5.2.25, 8.1.17.1, printed pages 444-448, 661-663, PDF pages 470-474, 687-689; Source: NVME-BASE-2.4, Rev. 2.4, §5.2.24, printed pages 444-445, PDF pages 470-471; Source: NVME-NVM-CS-1.3, Rev. 1.3, §4.1.6.2, printed pages 110, PDF pages 110; Source: NVME-NVM-CS-1.3, Rev. 1.3, §4.1.6.3, printed pages 110-111, PDF pages 110-111
