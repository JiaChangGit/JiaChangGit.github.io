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
}
FIGURE = re.compile(r"^Figure\s+(\d+):\s*(.+)$", re.IGNORECASE)
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
    "discovery controller",
    "command capsule",
    "response capsule",
    "in capsule",
    "nqn",
)
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


def figure_blocks(text: str) -> dict[int, list[str]]:
    """Collect page-bounded context around each Figure caption.

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

    blocks: dict[int, list[str]] = defaultdict(list)
    for page_lines in pages:
        captions = [
            (index, FIGURE.match(line))
            for index, line in enumerate(page_lines)
            if FIGURE.match(line)
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
            blocks[int(match.group(1))].append("__FIGURE_CONTEXT_BOUNDARY__")
            blocks[int(match.group(1))].extend(page_lines[start:end])
    return blocks


def allowed_lines(lines: list[str]) -> list[str]:
    return [
        line
        for line in lines
        if not any(term in line.lower() for term in FORBIDDEN_EVIDENCE)
    ]


def evidence_lines(
    lines: list[str], caption: str, number: int
) -> tuple[list[str], bool]:
    """Select the part of a page window that belongs to the Figure grid.

    Field/register Figures place their rows after the caption, so preceding
    tokens usually belong to the previous Figure. Conceptual diagrams are read
    from both sides of the caption but do not receive a normative-keyword index.
    """

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
        match = FIGURE.match(line)
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
    args = parser.parse_args()

    document = json.loads(args.register.read_text(encoding="utf-8"))
    entries = document["entries"]
    by_key = {(item["report_id"], int(item["number"])): item for item in entries}

    updated = 0
    for report_id, filename in TEXT_FILES.items():
        source_path = args.evidence_dir / filename
        if not source_path.is_file():
            raise FileNotFoundError(f"Missing local evidence: {source_path}")
        blocks = figure_blocks(source_path.read_text(encoding="utf-8"))
        for number, lines in blocks.items():
            entry = by_key.get((report_id, number))
            if entry is None:
                continue
            selected, structured = evidence_lines(lines, entry["title"], number)
            if not structured:
                selected = []
            filtered = allowed_lines(selected)
            compact = "\n".join(filtered)
            entry["key_items"] = key_items(filtered, entry["title"])
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
