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
}
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
    entries = document["entries"]
    by_key = {
        (item["report_id"], item["type"], int(item["number"])): item
        for item in entries
    }

    updated = 0
    for report_id, filename in TEXT_FILES.items():
        source_path = args.evidence_dir / filename
        if not source_path.is_file():
            raise FileNotFoundError(f"Missing local evidence: {source_path}")
        source_text = source_path.read_text(encoding="utf-8")
        if report_id == NEW_REPORT_ID:
            blocks = figure_blocks(source_text)
        else:
            blocks = {
                ("Figure", number): lines
                for number, lines in legacy_figure_blocks(source_text).items()
            }
        for (item_type, number), lines in blocks.items():
            entry = by_key.get((report_id, item_type, number))
            if entry is None:
                continue
            if report_id == NEW_REPORT_ID:
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
