#!/usr/bin/env python3
"""Refresh compact Figure evidence from local, gitignored PDF text extracts.

The script never copies source paragraphs into the repository. It stores only
short field/identifier tokens, normative-keyword presence, and a digest used to
detect stale evidence. The report generator consumes the tracked register, so
normal CI builds do not need access to the source PDFs.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTROL = ROOT / ".ai" / "nvme-report"
TEXT_FILES = {
    "base-ch1-2": "base-ch1-2.txt",
    "base-ch3": "base-ch3.txt",
    "base-ch4": "base-ch4.txt",
    "pcie-transport-1.4": "pcie-transport-1.4.txt",
    "base-admin-fw-logs": "base-admin-fw-logs.txt",
    "base-power-features": "base-full.txt",
    "base-self-test-hmb-emulation": "base-full.txt",
    "base-self-test-namespace-management": "base-full.txt",
}
TEXT_SOURCE_IDS = {
    "pcie-transport-1.4": "NVME-PCIE-TRANSPORT-1.4",
}
ADDITIONAL_TEXT_FILES = [
    ("base-self-test-hmb-emulation", "NVME-NVM-CS-1.3", "nvm-cs-full.txt"),
    ("base-self-test-namespace-management", "NVME-NVM-CS-1.3", "nvm-cs-full.txt"),
]
CAPTION = re.compile(r"^(Figure|Table)\s+(\d+):\s*(.+)$", re.IGNORECASE)
LEGACY_FIGURE = re.compile(r"^Figure\s+(\d+):\s*(.+)$", re.IGNORECASE)
TOKEN = re.compile(r"\b[A-Z][A-Z0-9]{1,11}(?:\.[A-Z][A-Z0-9]{1,11})*\b")
FIELD_NAME = re.compile(
    r"([A-Za-z][A-Za-z0-9 /_-]{2,80})\s+\(([A-Z][A-Z0-9]{1,11})\)\s*:"
)
KEYWORDS = (
    "shall not",
    "should not",
    "shall",
    "should",
    "may",
    "optional",
    "reserved",
)
FORBIDDEN_EVIDENCE = (
    "fabric",
    "message-based",
    "discovery",
    "exported nvm subsystem",
    "cross-controller reset",
    "lost host communication",
    "pull model ddc",
    "command capsule",
    "response capsule",
    "in capsule",
    "nqn",
)
LEGACY_FORBIDDEN_EVIDENCE = (
    "fabric",
    "message-based",
    "discovery controller",
    "command capsule",
    "response capsule",
    "in capsule",
    "nqn",
)
NEW_REPORT_ID = "base-admin-fw-logs"
NEW_REPORT_PREFIX = "BASEFWLOG"
NEW_ARTIFACT_IDS = [
    "basefwlog-tutorial-html",
    "basefwlog-detailed-html",
    "basefwlog-zh-md",
    "basefwlog-en-md",
]
MAIN_FIGURES = set(range(187, 194)) | set(range(203, 210)) | {215}
DEPENDENCY_FIGURES = {
    93,
    155,
    337,
    338,
    347,
    348,
    474,
}
TITLE_OVERRIDES = {
    84: "Admin Commands Permitted to Return a Status Code of Admin Command Media Not Ready",
    245: "Additional Hardware Error Information for correctable and uncorrectable PCIe errors",
}
KEY_ITEM_OVERRIDES = {
    93: ["DPTR", "PRP1", "PRP2", "SGL1"],
    155: ["Firmware Activation Starting", "CSTS.PP", "Firmware Slot Information", "RAE"],
    187: ["BPID", "CA", "FS"],
    188: ["MUD", "MEFWO", "ASQFWO"],
    189: ["Invalid Firmware Slot", "Invalid Firmware Image", "reset-required status", "MTFA", "Overlapping Range"],
    190: ["DPTR"],
    191: ["NUMD", "FWUG"],
    192: ["OFST", "FWUG"],
    193: ["Overlapping Range"],
    203: ["DPTR"],
    204: ["NUMDL", "RAE", "LSP", "LID"],
    205: ["LSI", "NUMDU"],
    206: ["LPOL", "OT"],
    207: ["LPOU"],
    208: ["CSI", "OT", "UIDX"],
    209: ["LID 03h", "CSI = N", "Domain / NVM subsystem", "Firmware Slot Information", "§5.2.13.1.4", "MDS"],
    215: ["AFI", "NAFS", "CAFS", "FRS1", "FRS2", "FRS3", "FRS4", "FRS5", "FRS6", "FRS7", "Reserved bytes 1:7 and 64:511"],
    337: ["Command Set Identifier"],
    338: ["FR", "MDS", "ULIST", "SMUD", "FAWR", "NOFS", "FFSRO", "MTFA", "FWUG", "DID", "MPTFAWR"],
    347: ["UUID1", "UUID2", "UUID126", "UUID127", "NVMe Invalid UUID"],
    348: ["ULEH", "IDASSOC", "UUID"],
    474: ["Firmware Activation Notices"],
}
DEPENDENCY_FOCUS = {
    155: {
        "zh_tw": "只取 firmware activation notice、CSTS.PP 與以 Firmware Slot Information log 清除事件的關係。",
        "en": "Use only the firmware-activation notice, CSTS.PP, and the Firmware Slot Information log used to clear the event.",
    },
    337: {
        "zh_tw": "§5.2.9 的正文指向 Figure 337，但 Figure 337 實際列的是 Command Set Identifier；firmware 欄位位於 Figure 338。",
        "en": "Section 5.2.9 points to Figure 337, but Figure 337 lists Command Set Identifiers; the firmware fields are in Figure 338.",
    },
    338: {
        "zh_tw": "只取 firmware update 需要的 FR、CTRATT.MDS／ULIST、FRMW／SMUD／FAWR／NOFS／FFSRO、MTFA、FWUG、DID 與 MPTFAWR；其餘 Identify Controller 欄位不展開。",
        "en": "Use only FR, CTRATT.MDS/ULIST, FRMW/SMUD/FAWR/NOFS/FFSRO, MTFA, FWUG, DID, and MPTFAWR for the firmware workflow; other Identify Controller fields are not expanded.",
    },
    347: {
        "zh_tw": "用於 §3.11.1 的 UUID list slot 穩定性與不得縮短清單的規則。",
        "en": "Used for the UUID-list slot-stability and no-shortening rules in section 3.11.1.",
    },
    348: {
        "zh_tw": "用於判斷 UUID list entry 是空值、NVMe Invalid UUID 或有效 UUID。",
        "en": "Used to distinguish an empty entry, the NVMe Invalid UUID, and a valid UUID.",
    },
    474: {
        "zh_tw": "只取 Firmware Activation Notices enable bit，對應 §3.11 的 activation-starting event。",
        "en": "Use only the Firmware Activation Notices enable bit associated with the activation-starting event in section 3.11.",
    },
}
DEPENDENCY_REFERENCES = {
    93: ["5.2.10", "5.2.13"],
    155: ["3.11", "5.2.30.1.6"],
    337: ["5.2.9"],
    338: ["3.11", "5.2.9", "5.2.10", "5.2.13"],
    347: ["3.11.1"],
    348: ["3.11.1"],
    474: ["3.11"],
}

POWER_REPORT_ID = "base-power-features"
POWER_REPORT_PREFIX = "BASEPOWER"
POWER_ARTIFACT_IDS = [
    "basepower-tutorial-html",
    "basepower-detailed-html",
    "basepower-zh-md",
    "basepower-en-md",
]
POWER_DEPENDENCY_FIGURES = {93, 213, 338, 340, 474}
POWER_FIGURES = {
    93: ("Common Command Format", "4.1.1", "140-142", "166-168"),
    197: ("Get Features – Data Pointer", "5.2.12", "209", "235"),
    198: ("Get Features – Command Dword 10", "5.2.12", "209-210", "235-236"),
    199: ("Get Features – Command Dword 14", "5.2.12", "210", "236"),
    200: ("Feature Identifiers for Get Features", "5.2.12", "210-211", "236-237"),
    201: ("Get Features – Select Supported Capabilities", "5.2.12.2", "212", "238"),
    202: ("Get Features – Command Specific Status Values", "5.2.12.2", "212", "238"),
    213: ("SMART / Health Information Log", "5.2.13.1.3", "220-225", "246-251"),
    338: ("Identify Controller Data Structure", "5.2.14.2.1", "340-364", "366-390"),
    340: ("Power State Descriptor Data Structure", "5.2.14.2.2", "383-386", "409-412"),
    463: ("Set Features – Data Pointer", "5.2.30", "456", "482"),
    464: ("Set Features – Command Dword 10", "5.2.30", "457", "483"),
    465: ("Set Features – Command Dword 14", "5.2.30", "457", "483"),
    466: ("Feature Identifiers for Set Features", "5.2.30", "457-459", "483-485"),
    468: ("Power Management – Command Dword 11", "5.2.30.1.2", "461", "487"),
    470: ("Temperature Threshold – Command Dword 11", "5.2.30.1.3.1", "463-464", "489-490"),
    474: ("Asynchronous Event Configuration – Command Dword 11", "5.2.30.1.6", "466-468", "492-494"),
    475: ("Autonomous Power State Transition – Command Dword 11", "5.2.30.1.7", "468", "494"),
    476: ("Autonomous Power State Transition Data Structure", "5.2.30.1.7", "469", "495"),
    477: ("Autonomous Power State Transition Entry", "5.2.30.1.7", "469", "495"),
    478: ("APST and NOPPME Interaction", "5.2.30.1.7", "469", "495"),
    482: ("Host Controlled Thermal Management – Command Dword 11", "5.2.30.1.10", "472", "498"),
    483: ("Non-Operational Power State Configuration – Command Dword 11", "5.2.30.1.11", "472-473", "498-499"),
    738: ("Power Management Overview", "8.1.19", "666", "692"),
    739: ("Power State Characteristics", "8.1.19", "667", "693"),
    740: ("Workload Hints", "8.1.19.3", "669", "695"),
    741: ("Host Controlled Thermal Management", "8.1.19.5", "671", "697"),
}
POWER_KEY_ITEM_OVERRIDES = {
    93: ["OPC", "CID", "NSID", "MPTR", "DPTR", "CDW10-CDW15"],
    197: ["DPTR", "PRP1", "PRP2"],
    198: ["SEL", "FID"],
    199: ["UIDX"],
    200: ["FID 02h", "FID 04h", "FID 0Ch", "FID 10h", "FID 11h"],
    201: ["CHANG", "NSSPEC", "SVBL"],
    202: ["Invalid Controller Identifier"],
    213: ["Composite Temperature", "TTC", "Temperature Sensor", "HCTM counters"],
    338: ["NPSS", "APSTA", "HCTMA", "WCTEMP", "MNTMT", "MXTMT", "RTD3E", "RTD3R"],
    340: ["MP", "NOPS", "ENLAT", "EXLAT", "IDLP", "ACTP", "RRT/RRL", "RWT/RWL"],
    463: ["DPTR", "PRP1", "PRP2"],
    464: ["SV", "FID"],
    465: ["UIDX"],
    466: ["FID 02h", "FID 04h", "FID 0Ch", "FID 10h", "FID 11h"],
    468: ["WH", "PS"],
    470: ["TMPTHH", "THSEL", "TMPSEL", "TMPTH"],
    474: ["TTHRY", "SHCW"],
    475: ["APSTE"],
    476: ["32 entries", "256 bytes"],
    477: ["ITPT", "ITPS"],
    478: ["APSTE", "NOPPME", "host entry", "timer entry", "background operations"],
    482: ["TMT1", "TMT2"],
    483: ["NOPPME"],
    738: ["Static Power Management", "Dynamic Power Management", "Power State Descriptor"],
    739: ["MP", "IDLP", "ACTP", "ENLAT", "EXLAT"],
    740: ["WH 000b", "WH 001b", "WH 010b"],
    741: ["TMT1", "TMT2", "hysteresis", "thermal throttling"],
}
POWER_DEPENDENCY_FOCUS = {
    93: {
        "zh_tw": "只取 Admin SQE 中 DPTR 與 command-specific dword 的固定位置。",
        "en": "Use only the fixed Admin-SQE locations of DPTR and command-specific dwords.",
    },
    213: {
        "zh_tw": "只取 temperature、TTC critical warning、warning time、HCTM counters 與 sensor readings。",
        "en": "Use only temperature, the TTC critical warning, warning time, HCTM counters, and sensor readings.",
    },
    338: {
        "zh_tw": "只取 power/thermal Feature 的 capability gates 與溫度／RTD3 limits。",
        "en": "Use only capability gates and temperature/RTD3 limits required by the power/thermal Features.",
    },
    340: {
        "zh_tw": "只取 power、operational flag、entry/exit latency、idle/active power 與 relative performance；不取已排除的 IIELL。",
        "en": "Use power, the operational flag, entry/exit latency, idle/active power, and relative performance; omit the excluded IIELL field.",
    },
    474: {
        "zh_tw": "只取 Temperature Threshold Hysteresis 與 SMART/Health critical-warning 事件 enable 欄位。",
        "en": "Use only Temperature Threshold Hysteresis and SMART/Health critical-warning event enables.",
    },
}
POWER_DEPENDENCY_REFERENCES = {
    93: ["5.2.12", "5.2.30"],
    213: ["5.2.30.1.3", "5.2.30.1.10", "8.1.19.5"],
    338: ["5.2.30.1.2", "5.2.30.1.7", "5.2.30.1.10", "8.1.19"],
    340: ["8.1.19", "8.1.19.1", "8.1.19.2"],
    474: ["5.2.30.1.3.1"],
}

DIAGMEM_REPORT_ID = "base-self-test-hmb-emulation"
DIAGMEM_REPORT_PREFIX = "BASEDIAGMEM"
DIAGMEM_ARTIFACT_IDS = [
    "basediagmem-tutorial-html",
    "basediagmem-detailed-html",
    "basediagmem-zh-md",
    "basediagmem-en-md",
]
DIAGMEM_DEPENDENCY_FIGURES = {
    ("NVME-BASE-2.4", number)
    for number in {36, 93, 94, 197, 198, 200, 203, 204, 205, 206, 207, 208, 209, 338, 463, 464, 466}
}
DIAGMEM_FIGURES = {
    ("NVME-BASE-2.4", 36): ("Offset 0h: CAP - Controller Capabilities", "3.1.4.1", "55-58", "81-84"),
    ("NVME-BASE-2.4", 93): ("Common Command Format", "4.1.1", "140-142", "166-168"),
    ("NVME-BASE-2.4", 94): ("Common Command Format - Vendor Specific Commands (Optional)", "4.1.1", "143", "169"),
    ("NVME-BASE-2.4", 176): ("Device Self-test Namespace Test Action", "5.2.6", "199", "225"),
    ("NVME-BASE-2.4", 177): ("Device Self-test - Command Dword 10", "5.2.6", "199", "225"),
    ("NVME-BASE-2.4", 178): ("Device Self-test - Command Dword 15", "5.2.6", "200", "226"),
    ("NVME-BASE-2.4", 179): ("Device Self-test - Command Processing", "5.2.6", "200", "226"),
    ("NVME-BASE-2.4", 180): ("Device Self-test - Command Specific Status Values", "5.2.6", "201", "227"),
    ("NVME-BASE-2.4", 197): ("Get Features - Data Pointer", "5.2.12", "209", "235"),
    ("NVME-BASE-2.4", 198): ("Get Features - Command Dword 10", "5.2.12", "209-210", "235-236"),
    ("NVME-BASE-2.4", 200): ("Feature Identifiers for Get Features", "5.2.12", "210-211", "236-237"),
    ("NVME-BASE-2.4", 203): ("Get Log Page - Data Pointer", "5.2.13", "213", "239"),
    ("NVME-BASE-2.4", 204): ("Get Log Page - Command Dword 10", "5.2.13", "213", "239"),
    ("NVME-BASE-2.4", 205): ("Get Log Page - Command Dword 11", "5.2.13", "214", "240"),
    ("NVME-BASE-2.4", 206): ("Get Log Page - Command Dword 12", "5.2.13", "214", "240"),
    ("NVME-BASE-2.4", 207): ("Get Log Page - Command Dword 13", "5.2.13", "214", "240"),
    ("NVME-BASE-2.4", 208): ("Get Log Page - Command Dword 14", "5.2.13", "214-215", "240-241"),
    ("NVME-BASE-2.4", 209): ("Get Log Page - Log Page Identifiers", "5.2.13", "215-216", "241-242"),
    ("NVME-BASE-2.4", 218): ("Device Self-test Log Page", "5.2.13.1.7", "230", "256"),
    ("NVME-BASE-2.4", 219): ("Self-test Result Data Structure", "5.2.13.1.7", "231-232", "257-258"),
    ("NVME-BASE-2.4", 338): ("Identify Controller Data Structure", "5.2.14.2.1", "340-364", "366-390"),
    ("NVME-BASE-2.4", 463): ("Set Features - Data Pointer", "5.2.30", "456", "482"),
    ("NVME-BASE-2.4", 464): ("Set Features - Command Dword 10", "5.2.30", "457", "483"),
    ("NVME-BASE-2.4", 466): ("Feature Identifiers for Set Features", "5.2.30", "457-459", "483-485"),
    ("NVME-BASE-2.4", 545): ("Host Memory Buffer - Command Dword 11", "5.2.30.2.3", "516-517", "542-543"),
    ("NVME-BASE-2.4", 546): ("Host Memory Buffer - Command Dword 12", "5.2.30.2.3", "517", "543"),
    ("NVME-BASE-2.4", 547): ("Host Memory Buffer - Command Dword 13", "5.2.30.2.3", "517", "543"),
    ("NVME-BASE-2.4", 548): ("Host Memory Buffer - Command Dword 14", "5.2.30.2.3", "517", "543"),
    ("NVME-BASE-2.4", 549): ("Host Memory Buffer - Command Dword 15", "5.2.30.2.3", "518", "544"),
    ("NVME-BASE-2.4", 550): ("Host Memory Buffer - Host Memory Descriptor List", "5.2.30.2.3", "518", "544"),
    ("NVME-BASE-2.4", 551): ("Host Memory Buffer - Host Memory Buffer Descriptor Entry", "5.2.30.2.3", "518", "544"),
    ("NVME-BASE-2.4", 552): ("Host Memory Buffer - Completion Queue Entry Dword 0", "5.2.30.2.3", "518-519", "544-545"),
    ("NVME-BASE-2.4", 553): ("Host Memory Buffer - Attributes Data Structure", "5.2.30.2.3", "519", "545"),
    ("NVME-BASE-2.4", 700): ("Example Device Self-test Operation (Informative)", "8.1.8", "615", "641"),
    ("NVME-BASE-2.4", 701): ("Format NVM command Aborting a Device Self-Test Operation", "8.1.8.1-8.1.8.2", "616", "642"),
    ("NVME-NVM-CS-1.3", 111): ("Self-test Results Data Structure", "4.1.4.3", "76", "76"),
}
DIAGMEM_KEY_ITEM_OVERRIDES = {
    ("NVME-BASE-2.4", 36): ["DSTRD", "2^(2+DSTRD) bytes"],
    ("NVME-BASE-2.4", 93): ["OPC", "CID", "NSID", "DPTR", "CDW10-CDW15"],
    ("NVME-BASE-2.4", 94): ["NSID", "MDPTR", "NDT", "NDM", "CDW12-CDW15"],
    ("NVME-BASE-2.4", 176): ["NSID 00000000h", "NSID 00000001h-FFFFFFFEh", "NSID FFFFFFFFh"],
    ("NVME-BASE-2.4", 177): ["STC 1h", "STC 2h", "STC 3h", "STC Eh", "STC Fh"],
    ("NVME-BASE-2.4", 178): ["DSTP"],
    ("NVME-BASE-2.4", 179): ["self-test in progress", "new STC", "abort", "result creation"],
    ("NVME-BASE-2.4", 180): ["Device Self-test in Progress", "status 1Dh"],
    ("NVME-BASE-2.4", 197): ["DPTR", "PRP1", "PRP2"],
    ("NVME-BASE-2.4", 198): ["SEL", "FID"],
    ("NVME-BASE-2.4", 200): ["FID 0Dh", "Controller scope", "data buffer"],
    ("NVME-BASE-2.4", 203): ["DPTR"],
    ("NVME-BASE-2.4", 204): ["NUMDL", "RAE", "LSP", "LID 06h"],
    ("NVME-BASE-2.4", 205): ["LSI", "NUMDU"],
    ("NVME-BASE-2.4", 206): ["LPOL", "OT"],
    ("NVME-BASE-2.4", 207): ["LPOU"],
    ("NVME-BASE-2.4", 208): ["CSI", "OT", "UIDX"],
    ("NVME-BASE-2.4", 209): ["LID 06h", "CSI = N", "Controller / Domain / NVM subsystem", "Device Self-test", "§5.2.13.1.7"],
    ("NVME-BASE-2.4", 218): ["DSTOS", "DSTCS", "RDS1", "RDS20", "564 bytes"],
    ("NVME-BASE-2.4", 219): ["DSTC", "DSTR", "SEGN", "VDINFO", "POH", "NSID", "FLBA", "STCT", "STC", "VS"],
    ("NVME-BASE-2.4", 338): ["OACS.DSTS", "EDSTT", "DSTO.SDSO", "HMPRE", "HMMIN", "HMMINDS", "HMMAXD", "CTRATT.HMBR", "AVSCC.VSCF", "ICSVSCC.SNVSCF"],
    ("NVME-BASE-2.4", 463): ["DPTR", "PRP1", "PRP2"],
    ("NVME-BASE-2.4", 464): ["SV", "FID"],
    ("NVME-BASE-2.4", 466): ["FID 0Dh", "Controller scope", "saveable", "changeable"],
    ("NVME-BASE-2.4", 545): ["CTZ", "HMNARE", "MR", "EHM"],
    ("NVME-BASE-2.4", 546): ["HSIZE", "CC.MPS units"],
    ("NVME-BASE-2.4", 547): ["HMDLLA", "16-byte alignment"],
    ("NVME-BASE-2.4", 548): ["HMDLUA"],
    ("NVME-BASE-2.4", 549): ["HMDLEC"],
    ("NVME-BASE-2.4", 550): ["16-byte descriptor entries", "HMDLEC"],
    ("NVME-BASE-2.4", 551): ["BADD", "BSIZE", "CC.MPS alignment"],
    ("NVME-BASE-2.4", 552): ["HMNAR", "HMNARE", "EHM"],
    ("NVME-BASE-2.4", 553): ["HSIZE", "HMDLAL", "HMDLAU", "HMDLEC", "4096 bytes"],
    ("NVME-BASE-2.4", 700): ["segment", "test performed", "failure criteria", "informative"],
    ("NVME-BASE-2.4", 701): ["SES", "FNS", "SENS", "Format NSID", "Self-test NSID", "abort decision"],
    ("NVME-NVM-CS-1.3", 111): ["FLBA", "bytes 23:16", "FVLD", "one failed logical block"],
}
DIAGMEM_DEPENDENCY_FOCUS = {
    ("NVME-BASE-2.4", 36): {"zh_tw": "只取 CAP.DSTRD encoding 與 byte-stride 公式。", "en": "Use only CAP.DSTRD encoding and its byte-stride formula."},
    ("NVME-BASE-2.4", 93): {"zh_tw": "只取 command common fields 與 command-specific dword 位置。", "en": "Use only common command fields and command-specific dword locations."},
    ("NVME-BASE-2.4", 94): {"zh_tw": "只取 §8.1.29 引用的 standard vendor-specific layout。", "en": "Use only the standard vendor-specific layout referenced by §8.1.29."},
    ("NVME-BASE-2.4", 197): {"zh_tw": "只取 HMB Get Features data-buffer pointer。", "en": "Use only the HMB Get Features data-buffer pointer."},
    ("NVME-BASE-2.4", 198): {"zh_tw": "只取 FID 0Dh 與 SEL。", "en": "Use only FID 0Dh and SEL."},
    ("NVME-BASE-2.4", 200): {"zh_tw": "只取 FID 0Dh row。", "en": "Use only the FID 0Dh row."},
    ("NVME-BASE-2.4", 203): {"zh_tw": "只取 LID 06h destination buffer。", "en": "Use only the LID 06h destination buffer."},
    ("NVME-BASE-2.4", 204): {"zh_tw": "只取 LID 06h 的 LID／NUMDL／RAE／LSP。", "en": "Use only LID/NUMDL/RAE/LSP for LID 06h."},
    ("NVME-BASE-2.4", 205): {"zh_tw": "只取 LID 06h 的 NUMDU 與 LSI=0。", "en": "Use only NUMDU and LSI zero for LID 06h."},
    ("NVME-BASE-2.4", 206): {"zh_tw": "只取完整讀取所需的 LPOL=0 與 OT=0。", "en": "Use only LPOL zero and OT zero for a complete read."},
    ("NVME-BASE-2.4", 207): {"zh_tw": "只取完整讀取所需的 LPOU=0。", "en": "Use only LPOU zero for a complete read."},
    ("NVME-BASE-2.4", 208): {"zh_tw": "只取 LID 06h 不使用的 CSI／UIDX 與 OT=0。", "en": "Use only unused CSI/UIDX and OT zero for LID 06h."},
    ("NVME-BASE-2.4", 209): {"zh_tw": "只取 LID 06h row，不列出其他 log pages。", "en": "Use only the LID 06h row; do not enumerate other log pages."},
    ("NVME-BASE-2.4", 338): {"zh_tw": "只取 Device Self-test、HMB 與 standard vendor-command capability fields。", "en": "Use only Device Self-test, HMB, and standard vendor-command capability fields."},
    ("NVME-BASE-2.4", 463): {"zh_tw": "只取 HMB Set Features data buffer pointer。", "en": "Use only the HMB Set Features data-buffer pointer."},
    ("NVME-BASE-2.4", 464): {"zh_tw": "只取 FID 0Dh 與 SV。", "en": "Use only FID 0Dh and SV."},
    ("NVME-BASE-2.4", 466): {"zh_tw": "只取 FID 0Dh row。", "en": "Use only the FID 0Dh row."},
}
DIAGMEM_DEPENDENCY_REFERENCES = {
    ("NVME-BASE-2.4", 36): ["8.2.3"],
    ("NVME-BASE-2.4", 93): ["5.2.6", "8.1.29"],
    ("NVME-BASE-2.4", 94): ["8.1.29"],
    ("NVME-BASE-2.4", 197): ["5.2.30.2.3"],
    ("NVME-BASE-2.4", 198): ["5.2.30.2.3"],
    ("NVME-BASE-2.4", 200): ["5.2.30.2.3"],
    ("NVME-BASE-2.4", 203): ["5.2.13.1.7"],
    ("NVME-BASE-2.4", 204): ["5.2.13.1.7"],
    ("NVME-BASE-2.4", 205): ["5.2.13.1.7"],
    ("NVME-BASE-2.4", 206): ["5.2.13.1.7"],
    ("NVME-BASE-2.4", 207): ["5.2.13.1.7"],
    ("NVME-BASE-2.4", 208): ["5.2.13.1.7"],
    ("NVME-BASE-2.4", 209): ["5.2.13.1.7"],
    ("NVME-BASE-2.4", 338): ["5.2.6", "5.2.30.2.3", "8.1.29", "8.2.4"],
    ("NVME-BASE-2.4", 463): ["5.2.30.2.3"],
    ("NVME-BASE-2.4", 464): ["5.2.30.2.3"],
    ("NVME-BASE-2.4", 466): ["5.2.30.2.3"],
}

NSMGMT_REPORT_ID = "base-self-test-namespace-management"
NSMGMT_REPORT_PREFIX = "BASENSMGMT"
NSMGMT_ARTIFACT_IDS = [
    "basensmgmt-tutorial-html",
    "basensmgmt-detailed-html",
    "basensmgmt-zh-md",
    "basensmgmt-en-md",
]
NSMGMT_DEPENDENCY_FIGURES = {
    ("NVME-BASE-2.4", number)
    for number in {36, 93, 139, 155, 203, 204, 205, 206, 207, 208, 209, 304, 338, 346, 474}
} | {
    ("NVME-NVM-CS-1.3", number) for number in {123, 127, 132, 133}
}
NSMGMT_FIGURES = {
    ("NVME-BASE-2.4", 36): ("Offset 0h: CAP - Controller Capabilities", "3.1.4.1", "55-58", "81-84"),
    ("NVME-BASE-2.4", 93): ("Common Command Format", "4.1.1", "140-142", "166-168"),
    ("NVME-BASE-2.4", 139): ("Controller List Format", "4.6.1", "172", "198"),
    ("NVME-BASE-2.4", 155): ("Asynchronous Event Information - Notice", "5.2.2.1", "186", "212"),
    ("NVME-BASE-2.4", 176): ("Device Self-test Namespace Test Action", "5.2.6", "199", "225"),
    ("NVME-BASE-2.4", 177): ("Device Self-test - Command Dword 10", "5.2.6", "199", "225"),
    ("NVME-BASE-2.4", 178): ("Device Self-test - Command Dword 15", "5.2.6", "200", "226"),
    ("NVME-BASE-2.4", 179): ("Device Self-test - Command Processing", "5.2.6", "200", "226"),
    ("NVME-BASE-2.4", 180): ("Device Self-test - Command Specific Status Values", "5.2.6", "201", "227"),
    ("NVME-BASE-2.4", 203): ("Get Log Page - Data Pointer", "5.2.13", "213", "239"),
    ("NVME-BASE-2.4", 204): ("Get Log Page - Command Dword 10", "5.2.13", "213", "239"),
    ("NVME-BASE-2.4", 205): ("Get Log Page - Command Dword 11", "5.2.13", "214", "240"),
    ("NVME-BASE-2.4", 206): ("Get Log Page - Command Dword 12", "5.2.13", "214", "240"),
    ("NVME-BASE-2.4", 207): ("Get Log Page - Command Dword 13", "5.2.13", "214", "240"),
    ("NVME-BASE-2.4", 208): ("Get Log Page - Command Dword 14", "5.2.13", "214-215", "240-241"),
    ("NVME-BASE-2.4", 209): ("Get Log Page - Log Page Identifiers", "5.2.13", "215-216", "241-242"),
    ("NVME-BASE-2.4", 218): ("Device Self-test Log Page", "5.2.13.1.7", "230", "256"),
    ("NVME-BASE-2.4", 219): ("Self-test Result Data Structure", "5.2.13.1.7", "231-232", "257-258"),
    ("NVME-BASE-2.4", 304): ("Manufacturer Default Configuration Status Log Page", "5.2.13.1.31", "301-302", "327-328"),
    ("NVME-BASE-2.4", 338): ("Identify Controller Data Structure", "5.2.14.2.1", "340, 353, 365, 378", "366, 379, 391, 404"),
    ("NVME-BASE-2.4", 346): ("Identify - I/O Command Set Independent Identify Namespace Data Structure", "5.2.14.2.3", "391-394", "417-420"),
    ("NVME-BASE-2.4", 442): ("Namespace Attachment - Data Pointer", "5.2.24", "445", "471"),
    ("NVME-BASE-2.4", 443): ("Namespace Attachment - Command Dword 10", "5.2.24", "445", "471"),
    ("NVME-BASE-2.4", 444): ("Namespace Attachment - Command Specific Status Values", "5.2.24", "445", "471"),
    ("NVME-BASE-2.4", 445): ("Namespace Management - Data Pointer", "5.2.25", "446", "472"),
    ("NVME-BASE-2.4", 446): ("Namespace Management - Command Dword 10", "5.2.25", "446-447", "472-473"),
    ("NVME-BASE-2.4", 447): ("Namespace Management - Command Dword 11", "5.2.25", "447", "473"),
    ("NVME-BASE-2.4", 448): ("Namespace Management - Data Structure for Create", "5.2.25", "447", "473"),
    ("NVME-BASE-2.4", 449): ("Namespace Management - Command Specific Status Values", "5.2.25", "448", "474"),
    ("NVME-BASE-2.4", 450): ("Namespace Management - Completion Queue Entry Dword 0", "5.2.25", "448", "474"),
    ("NVME-BASE-2.4", 474): ("Asynchronous Event Configuration - Command Dword 11", "5.2.30.1.6", "466-468", "492-494"),
    ("NVME-BASE-2.4", 700): ("Example Device Self-test Operation (Informative)", "8.1.8", "615", "641"),
    ("NVME-BASE-2.4", 701): ("Format NVM command Aborting a Device Self-Test Operation", "8.1.8.1-8.1.8.2", "616", "642"),
    ("NVME-NVM-CS-1.3", 111): ("Self-test Results Data Structure", "4.1.4.3", "76", "76"),
    ("NVME-NVM-CS-1.3", 123): ("Identify - Identify Namespace Data Structure, NVM Command Set", "4.1.5.1", "85-87", "85-87"),
    ("NVME-NVM-CS-1.3", 127): ("NVM Command Set I/O Command Set Specific Identify Namespace Data Structure", "4.1.5.3", "97-101", "97-101"),
    ("NVME-NVM-CS-1.3", 132): ("Namespace Granularity List", "4.1.5.8", "108", "108"),
    ("NVME-NVM-CS-1.3", 133): ("Namespace Granularity Descriptor", "4.1.5.8", "108", "108"),
    ("NVME-NVM-CS-1.3", 134): ("Namespace Management - Host Specified Fields", "4.1.6.4", "112-113", "112-113"),
}
NSMGMT_KEY_ITEM_OVERRIDES = {
    ("NVME-BASE-2.4", 36): ["CSS", "active I/O Command Set"],
    ("NVME-BASE-2.4", 93): ["OPC", "NSID", "DPTR", "CDW10-CDW15"],
    ("NVME-BASE-2.4", 139): ["NUMCIDS", "Controller Identifier list", "4096 bytes"],
    ("NVME-BASE-2.4", 155): ["Attached Namespace Attribute Changed", "Allocated Namespace Attribute Changed", "CNS 02h", "CNS 10h"],
    ("NVME-BASE-2.4", 176): ["NSID 00000000h", "active NSID", "NSID FFFFFFFFh"],
    ("NVME-BASE-2.4", 177): ["STC 1h", "STC 2h", "STC 3h", "STC Eh", "STC Fh"],
    ("NVME-BASE-2.4", 178): ["DSTP"],
    ("NVME-BASE-2.4", 179): ["self-test in progress", "abort", "result creation"],
    ("NVME-BASE-2.4", 180): ["Device Self-test in Progress", "status 1Dh"],
    ("NVME-BASE-2.4", 203): ["DPTR", "LID 06h destination buffer"],
    ("NVME-BASE-2.4", 204): ["NUMDL", "RAE", "LSP", "LID 06h"],
    ("NVME-BASE-2.4", 205): ["LSI", "NUMDU"],
    ("NVME-BASE-2.4", 206): ["LPOL", "OT"],
    ("NVME-BASE-2.4", 207): ["LPOU"],
    ("NVME-BASE-2.4", 208): ["CSI", "OT", "UIDX"],
    ("NVME-BASE-2.4", 209): ["LID 06h", "CSI = N", "Controller / Domain / NVM subsystem", "Device Self-test"],
    ("NVME-BASE-2.4", 218): ["DSTOS", "DSTCS", "RDS1-RDS20", "564 bytes"],
    ("NVME-BASE-2.4", 219): ["DSTC", "DSTR", "SEGN", "VDINFO", "NSID", "FLBA", "STCT", "STC"],
    ("NVME-BASE-2.4", 304): ["DNCS", "default namespace configuration status"],
    ("NVME-BASE-2.4", 338): ["OACS.DSTS", "EDSTT", "DSTO.SDSO", "OACS.NMS", "RDNCS", "MAXDNA", "MAXCNA"],
    ("NVME-BASE-2.4", 346): ["ANAGRPID", "NVMSETID", "ENDGID"],
    ("NVME-BASE-2.4", 442): ["DPTR", "Controller List", "one page boundary"],
    ("NVME-BASE-2.4", 443): ["SEL 0h Attach", "SEL 1h Detach"],
    ("NVME-BASE-2.4", 444): ["status 18h-1Ch", "status 25h", "status 27h", "status 29h-2Ah"],
    ("NVME-BASE-2.4", 445): ["DPTR", "4096-byte create buffer"],
    ("NVME-BASE-2.4", 446): ["SEL 0h Create", "SEL 1h Delete", "SEL 2h Restore"],
    ("NVME-BASE-2.4", 447): ["CSI", "NVM Command Set 00h"],
    ("NVME-BASE-2.4", 448): ["SIOCS bytes 0:511", "reserved bytes 512:1023", "VS bytes 1024:4095"],
    ("NVME-BASE-2.4", 449): ["Invalid Format", "Insufficient Capacity", "NSID Unavailable", "Thin Provisioning Not Supported"],
    ("NVME-BASE-2.4", 450): ["CQE DW0", "created NSID"],
    ("NVME-BASE-2.4", 474): ["Attached Namespace Attribute Notices", "Allocated Namespace Attribute Notices"],
    ("NVME-BASE-2.4", 700): ["segment", "test performed", "failure criteria", "informative"],
    ("NVME-BASE-2.4", 701): ["SES", "FNS", "SENS", "Format NSID", "Self-test NSID", "abort decision"],
    ("NVME-NVM-CS-1.3", 111): ["FLBA", "bytes 23:16", "FVLD", "one failed logical block"],
    ("NVME-NVM-CS-1.3", 123): ["NSZE", "NCAP", "NUSE", "NSFEAT.THINP", "FLBAS", "DPS", "NMIC"],
    ("NVME-NVM-CS-1.3", 127): ["LBSTM", "Storage Tag Masking Level", "LBAFEE"],
    ("NVME-NVM-CS-1.3", 132): ["NGA.GDM", "ND", "NGD0-NGD63", "CNS 16h"],
    ("NVME-NVM-CS-1.3", 133): ["NSG bytes 7:0", "NCG bytes 15:8", "byte units"],
    ("NVME-NVM-CS-1.3", 134): ["NSZE", "NCAP", "FLBAS", "DPS", "NMIC", "ANAGRPID", "NVMSETID", "ENDGID", "LBSTM", "NPHNDLS", "Placement Handle List"],
}
NSMGMT_DEPENDENCY_FOCUS = {
    ("NVME-BASE-2.4", 36): {"zh_tw": "只取 restore default 所需的 active I/O Command Set context。", "en": "Use only the active-I/O-Command-Set context needed by restore default."},
    ("NVME-BASE-2.4", 93): {"zh_tw": "只取 Self-test／Namespace commands 共用的 NSID、DPTR 與 command dwords。", "en": "Use only NSID, DPTR, and command dwords shared by Self-test and Namespace commands."},
    ("NVME-BASE-2.4", 139): {"zh_tw": "只取 Namespace Attachment 使用的 4096-byte Controller List。", "en": "Use only the 4096-byte Controller List consumed by Namespace Attachment."},
    ("NVME-BASE-2.4", 155): {"zh_tw": "只取 Attached／Allocated Namespace Attribute Changed notices。", "en": "Use only Attached/Allocated Namespace Attribute Changed notices."},
    ("NVME-BASE-2.4", 203): {"zh_tw": "只取 LID 06h destination buffer。", "en": "Use only the LID 06h destination buffer."},
    ("NVME-BASE-2.4", 204): {"zh_tw": "只取 LID 06h 的 LID／NUMDL／RAE／LSP。", "en": "Use only LID/NUMDL/RAE/LSP for LID 06h."},
    ("NVME-BASE-2.4", 205): {"zh_tw": "只取 LID 06h 的 NUMDU 與 LSI=0。", "en": "Use only NUMDU and LSI zero for LID 06h."},
    ("NVME-BASE-2.4", 206): {"zh_tw": "只取完整讀取的 LPOL=0 與 OT=0。", "en": "Use only LPOL zero and OT zero for a complete read."},
    ("NVME-BASE-2.4", 207): {"zh_tw": "只取完整讀取的 LPOU=0。", "en": "Use only LPOU zero for a complete read."},
    ("NVME-BASE-2.4", 208): {"zh_tw": "只取 LID 06h 未使用的 CSI／UIDX 與 OT=0。", "en": "Use only unused CSI/UIDX and OT zero for LID 06h."},
    ("NVME-BASE-2.4", 209): {"zh_tw": "只取 LID 06h row，不列其他 log page。", "en": "Use only the LID 06h row; do not enumerate other log pages."},
    ("NVME-BASE-2.4", 304): {"zh_tw": "只取 restore default 後的 DNCS observation。", "en": "Use only DNCS observation after restore default."},
    ("NVME-BASE-2.4", 338): {"zh_tw": "只取 Self-test 與 Namespace Management capability／limit fields。", "en": "Use only Self-test and Namespace Management capability/limit fields."},
    ("NVME-BASE-2.4", 346): {"zh_tw": "只取 create／identify 會用到的 namespace group identifiers。", "en": "Use only namespace group identifiers used by create/identify."},
    ("NVME-BASE-2.4", 474): {"zh_tw": "只取 attached／allocated namespace notice enable bits。", "en": "Use only attached/allocated namespace notice-enable bits."},
    ("NVME-NVM-CS-1.3", 123): {"zh_tw": "只取容量、格式與 sharing／protection 欄位。", "en": "Use only capacity, format, sharing, and protection fields."},
    ("NVME-NVM-CS-1.3", 127): {"zh_tw": "只取 §4.1.6.2 直接引用的 LBSTM mask capability。", "en": "Use only LBSTM mask capability directly referenced by §4.1.6.2."},
    ("NVME-NVM-CS-1.3", 132): {"zh_tw": "只取 CNS 16h list header 與 descriptor mapping。", "en": "Use only the CNS 16h list header and descriptor mapping."},
    ("NVME-NVM-CS-1.3", 133): {"zh_tw": "只取 NSG／NCG byte-unit hints。", "en": "Use only NSG/NCG byte-unit hints."},
}
NSMGMT_DEPENDENCY_REFERENCES = {
    ("NVME-BASE-2.4", 36): ["5.2.25.1"],
    ("NVME-BASE-2.4", 93): ["5.2.6", "5.2.24", "5.2.25", "8.1.17"],
    ("NVME-BASE-2.4", 139): ["5.2.24"],
    ("NVME-BASE-2.4", 155): ["8.1.17", "8.1.17.1"],
    ("NVME-BASE-2.4", 203): ["5.2.13.1.7"],
    ("NVME-BASE-2.4", 204): ["5.2.13.1.7"],
    ("NVME-BASE-2.4", 205): ["5.2.13.1.7"],
    ("NVME-BASE-2.4", 206): ["5.2.13.1.7"],
    ("NVME-BASE-2.4", 207): ["5.2.13.1.7"],
    ("NVME-BASE-2.4", 208): ["5.2.13.1.7"],
    ("NVME-BASE-2.4", 209): ["5.2.13.1.7"],
    ("NVME-BASE-2.4", 304): ["5.2.25.1"],
    ("NVME-BASE-2.4", 338): ["5.2.6", "5.2.24", "5.2.25.1", "8.1.17"],
    ("NVME-BASE-2.4", 346): ["8.1.17"],
    ("NVME-BASE-2.4", 474): ["8.1.17.2"],
    ("NVME-NVM-CS-1.3", 123): ["2.1.1", "4.1.6"],
    ("NVME-NVM-CS-1.3", 127): ["4.1.6.2"],
    ("NVME-NVM-CS-1.3", 132): ["5.8"],
    ("NVME-NVM-CS-1.3", 133): ["5.8"],
}
NOISE = {
    "ADMIN",
    "BASE",
    "BITS",
    "BYTE",
    "BYTES",
    "COMMAND",
    "CONTROLLER",
    "DESCRIPTION",
    "DWORD",
    "FIGURE",
    "HOST",
    "IMPL",
    "IO",
    "NVM",
    "NVME",
    "OPTIONAL",
    "PCI",
    "PCIE",
    "PDF",
    "READ",
    "RESERVED",
    "RESET",
    "RO",
    "RW",
    "SECTION",
    "SPEC",
    "SUBSYSTEM",
    "TYPE",
    "VALUE",
    "VALUES",
    "WRITE",
}
TITLE_CONCEPTS = (
    "NVMe Family",
    "Command Set",
    "Submission Queue",
    "Completion Queue",
    "Queue Pair",
    "Transport Protocol Layers",
    "NVM Storage Hierarchy",
    "NVM Subsystem",
    "I/O Controller",
    "Administrative Controller",
    "Shared Namespace",
    "Private Namespace",
    "NVM Set",
    "Reclaim Group",
    "Reclaim Unit",
    "Endurance Group",
    "Namespace",
    "Domain",
    "Memory Page",
    "Phase Tag",
    "Status Code",
    "Power State",
    "Interrupt",
    "Controller",
    "Controller ID",
    "Command",
)


def clean(line: str) -> str:
    return " ".join(line.replace("\u00ad", "").split())


def figure_blocks(text: str) -> dict[tuple[str, int], list[str]]:
    """Collect page-bounded context around each Figure/Table caption.

    Diagram labels often precede a caption, while register rows follow it. The
    extractor therefore retains a small same-page window on both sides and
    merges repeated captions for multi-page field grids. It never lets a final
    Figure absorb the following annex or section.
    """

    pages: list[list[str]] = []
    page: list[str] = []
    for raw in text.splitlines():
        line = clean(raw)
        if line.startswith("===== PDF PAGE"):
            if page:
                pages.append(page)
            page = []
            continue
        if not line or (
            line.startswith("NVM Express") and "Revision" in line
        ):
            continue
        if line.isdigit():
            continue
        page.append(line)
    if page:
        pages.append(page)

    blocks: dict[tuple[str, int], list[str]] = defaultdict(list)
    for page_lines in pages:
        captions = [
            (index, CAPTION.match(line))
            for index, line in enumerate(page_lines)
            if CAPTION.match(line)
        ]
        for position, (index, match) in enumerate(captions):
            assert match is not None
            previous_caption = captions[position - 1][0] if position else -1
            next_caption = (
                captions[position + 1][0]
                if position + 1 < len(captions)
                else len(page_lines)
            )
            start = max(previous_caption + 1, index - 36)
            end = min(next_caption, index + 100)
            key = (match.group(1).title(), int(match.group(2)))
            blocks[key].append("__FIGURE_CONTEXT_BOUNDARY__")
            blocks[key].extend(page_lines[start:end])
    return blocks


def legacy_figure_blocks(text: str) -> dict[int, list[str]]:
    """Use the original Figure-only page windows for the four existing reports."""

    pages: list[list[str]] = []
    page: list[str] = []
    for raw in text.splitlines():
        line = clean(raw)
        if line.startswith("===== PDF PAGE"):
            if page:
                pages.append(page)
            page = []
            continue
        if not line or (line.startswith("NVM Express") and "Revision" in line):
            continue
        if line.isdigit():
            continue
        page.append(line)
    if page:
        pages.append(page)

    blocks: dict[int, list[str]] = defaultdict(list)
    for page_lines in pages:
        captions = [
            (index, LEGACY_FIGURE.match(line))
            for index, line in enumerate(page_lines)
            if LEGACY_FIGURE.match(line)
        ]
        for position, (index, match) in enumerate(captions):
            assert match is not None
            previous_caption = captions[position - 1][0] if position else -1
            next_caption = (
                captions[position + 1][0]
                if position + 1 < len(captions)
                else len(page_lines)
            )
            start = max(previous_caption + 1, index - 36)
            end = min(next_caption, index + 100)
            number = int(match.group(1))
            blocks[number].append("__FIGURE_CONTEXT_BOUNDARY__")
            blocks[number].extend(page_lines[start:end])
    return blocks


def allowed_lines(lines: list[str]) -> list[str]:
    return [
        line
        for line in lines
        if not any(term in line.lower() for term in FORBIDDEN_EVIDENCE)
    ]


def legacy_allowed_lines(lines: list[str]) -> list[str]:
    return [
        line
        for line in lines
        if not any(term in line.lower() for term in LEGACY_FORBIDDEN_EVIDENCE)
    ]


def evidence_lines(
    lines: list[str], caption: str, item_type: str, number: int
) -> tuple[list[str], bool]:
    """Select the part of a page window that belongs to the Figure grid.

    Field/register Figures place their rows after the caption, so preceding
    tokens usually belong to the previous Figure. Conceptual diagrams are read
    from both sides of the caption but do not receive a normative-keyword index.
    """

    structured = bool(
        re.search(
            r"offset|dword|entry|layout|format|status|capabilit|field|"
            r"identifier|definition|descriptor|register|values|requirements|"
            r"log page|data structure|event|information|list|measurement|pointer",
            caption,
            re.IGNORECASE,
        )
    )
    if not structured:
        return lines, False

    result: list[str] = []
    collecting = False
    for line in lines:
        if line == "__FIGURE_CONTEXT_BOUNDARY__":
            collecting = False
            continue
        match = CAPTION.match(line)
        if match:
            collecting = (
                match.group(1).title() == item_type and int(match.group(2)) == number
            )
            continue
        if collecting:
            if line.startswith(("Offset ", "Annex ")) or re.match(
                r"^\d+(?:\.\d+)+\s+[A-Za-z]", line
            ):
                collecting = False
                continue
            result.append(line)
    return result, True


def legacy_evidence_lines(
    lines: list[str], caption: str, number: int
) -> tuple[list[str], bool]:
    """Preserve the evidence-selection behavior used by the existing reports."""

    structured = bool(
        re.search(
            r"offset|dword|entry|layout|format|status|capabilit|field|"
            r"identifier|definition|descriptor|register|values|requirements",
            caption,
            re.IGNORECASE,
        )
    )
    if not structured:
        return lines, False

    result: list[str] = []
    collecting = False
    for line in lines:
        if line == "__FIGURE_CONTEXT_BOUNDARY__":
            collecting = False
            continue
        match = LEGACY_FIGURE.match(line)
        if match:
            collecting = int(match.group(1)) == number
            continue
        if collecting:
            if line.startswith(("Offset ", "Annex ")) or re.match(
                r"^\d+(?:\.\d+)+\s+[A-Za-z]", line
            ):
                collecting = False
                continue
            result.append(line)
    return result, True


def key_items(lines: list[str], caption: str) -> list[str]:
    candidates: list[str] = []

    # Prefer symbols explicitly defined as field names.
    for line in lines:
        for match in FIELD_NAME.finditer(line):
            candidates.append(match.group(2))

    # Then add symbols from the caption and the compact source block.
    for line in [caption, *lines]:
        for token in TOKEN.findall(line.replace("MSI-X", "MSIX")):
            if token not in NOISE and not token.isdigit():
                candidates.append(token)

    for concept in TITLE_CONCEPTS:
        if concept.lower() in caption.lower():
            candidates.append(concept)
    ratio = re.search(r"\b\d+:\d+\b", caption)
    if ratio:
        candidates.append(ratio.group(0))

    result: list[str] = []
    for item in candidates:
        normalized = item.strip("._-/")
        if not normalized or normalized in NOISE or normalized in result:
            continue
        result.append(normalized)
        if len(result) == 8:
            break
    if not result:
        # Diagram captions occasionally contain no acronym. Retaining the short
        # caption as an index is still source-specific and is not source prose.
        result.append(caption[:80])
    return result


def source_keywords(lines: list[str]) -> list[str]:
    joined = " ".join(lines).lower()
    result: list[str] = []
    for keyword in KEYWORDS:
        if re.search(rf"\b{re.escape(keyword)}\b", joined):
            result.append(keyword)
    return result


def sync_new_report_entries(document: dict, inventory_path: Path) -> None:
    """Replace generated register rows for the cross-section firmware/log report."""

    inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
    report = inventory["reports"][NEW_REPORT_ID]
    by_number = {int(item["number"]): item for item in report["figures"]}
    selected = MAIN_FIGURES | DEPENDENCY_FIGURES
    missing = sorted(selected - set(by_number))
    if missing:
        raise ValueError(f"Source inventory is missing Figures: {missing}")

    retained = [
        item for item in document["entries"] if item.get("report_id") != NEW_REPORT_ID
    ]
    generated = []
    for number in sorted(selected):
        source = by_number[number]
        dependency = number in DEPENDENCY_FIGURES
        generated.append(
            {
                "id": f"{NEW_REPORT_PREFIX}-FIG-{number:03d}",
                "report_id": NEW_REPORT_ID,
                "source_id": "NVME-BASE-2.4",
                "type": "Figure",
                "number": str(number),
                "title": TITLE_OVERRIDES.get(number, source["caption"]),
                "section": source["section"],
                "printed_pages": source["printed_pages"],
                "pdf_pages": source["pdf_pages"],
                "scope_entry_id": (
                    "BASE-FWLOG-DEPENDENCY-INCLUDE"
                    if dependency
                    else "BASE-FWLOG-INCLUDE"
                ),
                "scope_status": "INCLUDE",
                "mode": "dependency-slice" if dependency else (
                    "scope-reduced" if number == 209 else "full"
                ),
                "role": "referenced_dependency" if dependency else "in_scope",
                "referenced_from": DEPENDENCY_REFERENCES.get(number, []),
                "dependency_focus": DEPENDENCY_FOCUS.get(number),
                "required_artifact_ids": list(NEW_ARTIFACT_IDS),
                "introduced_in": list(NEW_ARTIFACT_IDS),
            }
        )
    document["entries"] = retained + generated


def sync_power_report_entries(document: dict) -> None:
    """Replace the power/thermal report rows from its reviewed allowlist."""

    retained = [
        item for item in document["entries"] if item.get("report_id") != POWER_REPORT_ID
    ]
    generated = []
    for number, (title, section, printed_pages, pdf_pages) in POWER_FIGURES.items():
        dependency = number in POWER_DEPENDENCY_FIGURES
        mode = "dependency-slice" if dependency else "full"
        if number in {200, 466, 468}:
            mode = "scope-reduced"
        generated.append(
            {
                "id": f"{POWER_REPORT_PREFIX}-FIG-{number:03d}",
                "report_id": POWER_REPORT_ID,
                "source_id": "NVME-BASE-2.4",
                "type": "Figure",
                "number": str(number),
                "title": title,
                "section": section,
                "printed_pages": printed_pages,
                "pdf_pages": pdf_pages,
                "scope_entry_id": (
                    "BASE-POWER-DEPENDENCY-INCLUDE"
                    if dependency
                    else "BASE-POWER-INCLUDE"
                ),
                "scope_status": "INCLUDE",
                "mode": mode,
                "role": "referenced_dependency" if dependency else "in_scope",
                "referenced_from": POWER_DEPENDENCY_REFERENCES.get(number, []),
                "dependency_focus": POWER_DEPENDENCY_FOCUS.get(number),
                "required_artifact_ids": list(POWER_ARTIFACT_IDS),
                "introduced_in": list(POWER_ARTIFACT_IDS),
            }
        )
    document["entries"] = retained + generated


def sync_diagmem_report_entries(document: dict) -> None:
    """Replace the mixed Base/NVM self-test and HMB report rows."""

    retained = [
        item for item in document["entries"] if item.get("report_id") != DIAGMEM_REPORT_ID
    ]
    generated = []
    for (source_id, number), (title, section, printed_pages, pdf_pages) in DIAGMEM_FIGURES.items():
        key = (source_id, number)
        dependency = key in DIAGMEM_DEPENDENCY_FIGURES
        mode = "dependency-slice" if dependency else "full"
        scope_reduced = key in {
            ("NVME-BASE-2.4", 200),
            ("NVME-BASE-2.4", 209),
            ("NVME-BASE-2.4", 338),
            ("NVME-BASE-2.4", 466),
        }
        generated.append(
            {
                "id": f"{DIAGMEM_REPORT_PREFIX}-FIG-{number:03d}",
                "report_id": DIAGMEM_REPORT_ID,
                "source_id": source_id,
                "type": "Figure",
                "number": str(number),
                "title": title,
                "section": section,
                "printed_pages": printed_pages,
                "pdf_pages": pdf_pages,
                "scope_entry_id": (
                    "BASE-DIAGMEM-DEPENDENCY-INCLUDE"
                    if dependency
                    else (
                        "NVMCS-DIAGMEM-INCLUDE"
                        if source_id == "NVME-NVM-CS-1.3"
                        else "BASE-DIAGMEM-INCLUDE"
                    )
                ),
                "scope_status": "INCLUDE",
                "mode": mode,
                "scope_reduced": scope_reduced,
                "role": "referenced_dependency" if dependency else "in_scope",
                "referenced_from": DIAGMEM_DEPENDENCY_REFERENCES.get(key, []),
                "dependency_focus": DIAGMEM_DEPENDENCY_FOCUS.get(key),
                "required_artifact_ids": list(DIAGMEM_ARTIFACT_IDS),
                "introduced_in": list(DIAGMEM_ARTIFACT_IDS),
            }
        )
    document["entries"] = retained + generated


def sync_nsmgmt_report_entries(document: dict) -> None:
    """Replace the mixed Base/NVM self-test and namespace-management rows."""

    retained = [
        item for item in document["entries"] if item.get("report_id") != NSMGMT_REPORT_ID
    ]
    generated = []
    for (source_id, number), (title, section, printed_pages, pdf_pages) in NSMGMT_FIGURES.items():
        key = (source_id, number)
        dependency = key in NSMGMT_DEPENDENCY_FIGURES
        scope_reduced = key in {
            ("NVME-BASE-2.4", 36),
            ("NVME-BASE-2.4", 155),
            ("NVME-BASE-2.4", 209),
            ("NVME-BASE-2.4", 338),
            ("NVME-BASE-2.4", 346),
            ("NVME-BASE-2.4", 474),
            ("NVME-NVM-CS-1.3", 123),
            ("NVME-NVM-CS-1.3", 127),
            ("NVME-NVM-CS-1.3", 132),
            ("NVME-NVM-CS-1.3", 133),
        }
        scope_entry = (
            "BASE-NSMGMT-DEPENDENCY-INCLUDE"
            if dependency and source_id == "NVME-BASE-2.4"
            else (
                "NVMCS-NSMGMT-DEPENDENCY-INCLUDE"
                if dependency
                else (
                    "NVMCS-NSMGMT-INCLUDE"
                    if source_id == "NVME-NVM-CS-1.3"
                    else "BASE-NSMGMT-INCLUDE"
                )
            )
        )
        generated.append(
            {
                "id": f"{NSMGMT_REPORT_PREFIX}-FIG-{number:03d}",
                "report_id": NSMGMT_REPORT_ID,
                "source_id": source_id,
                "type": "Figure",
                "number": str(number),
                "title": title,
                "section": section,
                "printed_pages": printed_pages,
                "pdf_pages": pdf_pages,
                "scope_entry_id": scope_entry,
                "scope_status": "INCLUDE",
                "mode": "dependency-slice" if dependency else "full",
                "scope_reduced": scope_reduced,
                "role": "referenced_dependency" if dependency else "in_scope",
                "referenced_from": NSMGMT_DEPENDENCY_REFERENCES.get(key, []),
                "dependency_focus": NSMGMT_DEPENDENCY_FOCUS.get(key),
                "required_artifact_ids": list(NSMGMT_ARTIFACT_IDS),
                "introduced_in": list(NSMGMT_ARTIFACT_IDS),
            }
        )
    document["entries"] = retained + generated


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--evidence-dir",
        type=Path,
        default=ROOT / "tmp" / "pdfs" / "nvme-report",
    )
    parser.add_argument(
        "--register",
        type=Path,
        default=CONTROL / "figure-table-register.json",
    )
    parser.add_argument(
        "--inventory",
        type=Path,
        default=ROOT / "tmp" / "pdfs" / "nvme-report" / "inventory.json",
    )
    args = parser.parse_args()

    document = json.loads(args.register.read_text(encoding="utf-8"))
    sync_new_report_entries(document, args.inventory)
    sync_power_report_entries(document)
    sync_diagmem_report_entries(document)
    sync_nsmgmt_report_entries(document)
    entries = document["entries"]
    by_key = {
        (item["report_id"], item["source_id"], item["type"], int(item["number"])): item
        for item in entries
    }

    updated = 0
    evidence_sources = [
        (report_id, TEXT_SOURCE_IDS.get(report_id, "NVME-BASE-2.4"), filename)
        for report_id, filename in TEXT_FILES.items()
    ] + list(ADDITIONAL_TEXT_FILES)
    for report_id, source_id, filename in evidence_sources:
        source_path = args.evidence_dir / filename
        if not source_path.is_file():
            raise FileNotFoundError(f"Missing local evidence: {source_path}")
        source_text = source_path.read_text(encoding="utf-8")
        if report_id in {NEW_REPORT_ID, POWER_REPORT_ID, DIAGMEM_REPORT_ID, NSMGMT_REPORT_ID}:
            blocks = figure_blocks(source_text)
        else:
            blocks = {
                ("Figure", number): lines
                for number, lines in legacy_figure_blocks(source_text).items()
            }
        for (item_type, number), lines in blocks.items():
            entry = by_key.get((report_id, source_id, item_type, number))
            if entry is None:
                continue
            if report_id in {NEW_REPORT_ID, POWER_REPORT_ID, DIAGMEM_REPORT_ID, NSMGMT_REPORT_ID}:
                selected, structured = evidence_lines(
                    lines, entry["title"], item_type, number
                )
                filter_evidence = allowed_lines
            else:
                selected, structured = legacy_evidence_lines(
                    lines, entry["title"], number
                )
                filter_evidence = legacy_allowed_lines
            if not structured:
                selected = []
            filtered = filter_evidence(selected)
            compact = "\n".join(filtered)
            entry["key_items"] = key_items(filtered, entry["title"])
            if report_id == NEW_REPORT_ID and number in KEY_ITEM_OVERRIDES:
                entry["key_items"] = list(KEY_ITEM_OVERRIDES[number])
            if report_id == POWER_REPORT_ID and number in POWER_KEY_ITEM_OVERRIDES:
                entry["key_items"] = list(POWER_KEY_ITEM_OVERRIDES[number])
            diagmem_key = (source_id, number)
            if report_id == DIAGMEM_REPORT_ID and diagmem_key in DIAGMEM_KEY_ITEM_OVERRIDES:
                entry["key_items"] = list(DIAGMEM_KEY_ITEM_OVERRIDES[diagmem_key])
            if report_id == NSMGMT_REPORT_ID and diagmem_key in NSMGMT_KEY_ITEM_OVERRIDES:
                entry["key_items"] = list(NSMGMT_KEY_ITEM_OVERRIDES[diagmem_key])
            entry["source_keywords"] = (
                source_keywords(filtered) if structured else []
            )
            entry["evidence_digest"] = hashlib.sha256(
                compact.encode("utf-8")
            ).hexdigest()
            updated += 1

    missing = [
        item["id"]
        for item in entries
        if item.get("scope_status") == "INCLUDE"
        and (not item.get("key_items") or not item.get("evidence_digest"))
    ]
    if missing:
        raise ValueError(
            "Included Figures missing compact evidence: " + ", ".join(missing)
        )

    args.register.write_text(
        json.dumps(document, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Updated compact evidence for {updated} Figure records")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
