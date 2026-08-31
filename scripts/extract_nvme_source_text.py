#!/usr/bin/env python3
"""Extract only the locally supplied NVMe source ranges for report authoring.

The extracted text is written below tmp/ (gitignored). It is evidence for local
authoring and is never a publishable artifact.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
SOURCE_FILES = {
    "base": "NVM-Express-Base-Specification-Revision-2.4-Ratified-2026.07.31.pdf",
    "pcie": "NVM-Express-NVMe-over-PCIe-Transport-Specification-Revision-1.4-Ratified-2026.07.31.pdf",
}
RANGES = {
    "base-ch1-2": ("base", [(27, 63)]),
    "base-ch3": ("base", [(64, 164)]),
    "base-ch4": ("base", [(165, 201)]),
    "pcie-transport-1.4": ("pcie", [(1, 48)]),
    # §3.11, §5.2.9, §5.2.10, the common/PCIe portions of §5.2.13,
    # plus the exact pages containing Figures referenced by those sections.
    # The broad 238-362 span is local evidence only; publication scope is
    # controlled separately and excludes §5.2.13.3 and Figure 257.
    "base-admin-fw-logs": (
        "base",
        [
            (111, 111),
            (136, 137),
            (161, 164),
            (166, 168),
            (171, 172),
            (180, 181),
            (212, 212),
            (228, 232),
            (234, 234),
            (238, 345),
            (362, 362),
            (366, 366),
            (380, 380),
            (383, 383),
            (385, 385),
            (409, 409),
            (417, 420),
            (421, 422),
            (473, 473),
            (476, 477),
            (483, 485),
            (492, 494),
            (496, 497),
            (511, 511),
            (528, 528),
            (596, 596),
            (704, 705),
            (746, 746),
            (764, 764),
            (766, 766),
        ],
    ),
}
FIGURE = re.compile(r"^Figure\s+(\d+):\s*(.+)$", re.IGNORECASE)
TABLE = re.compile(r"^Table\s+(\d+):\s*(.+)$", re.IGNORECASE)
SECTION = re.compile(r"^(\d+(?:\.\d+){0,5})\s+(.+)$")


def clean_line(line: str) -> str:
    return " ".join(
        line.replace("\u00ad", "").replace("\ufffdV", "-").split()
    )


def flatten_outline(reader: PdfReader) -> list[dict[str, object]]:
    records: list[dict[str, object]] = []

    def visit(items: list[object]) -> None:
        for item in items:
            if isinstance(item, list):
                visit(item)
                continue
            title = clean_line(str(item.get("/Title", "")))
            match = SECTION.match(title)
            if not match:
                continue
            records.append(
                {
                    "section": match.group(1),
                    "title": match.group(2),
                    "full_title": title,
                    "pdf_page": reader.get_destination_page_number(item) + 1,
                }
            )

    visit(reader.outline)
    return records


def caption_only(value: str) -> str:
    value = re.sub(r"\.{4,}\s*\d*\s*$", "", value).strip()
    return value


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-dir", required=True, type=Path)
    parser.add_argument(
        "--output-dir", type=Path, default=ROOT / "tmp" / "pdfs" / "nvme-report"
    )
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    readers = {
        key: PdfReader(args.source_dir / filename) for key, filename in SOURCE_FILES.items()
    }
    outlines = {key: flatten_outline(reader) for key, reader in readers.items()}
    inventory: dict[str, object] = {"reports": {}}

    for report_id, (source_key, page_ranges) in RANGES.items():
        reader = readers[source_key]
        page_records = []
        text_parts = []
        current_section = ""
        figures = []
        tables = []
        sections = []
        pdf_pages = [
            page
            for first_page, last_page in page_ranges
            for page in range(first_page, last_page + 1)
        ]
        for pdf_page in pdf_pages:
            text = reader.pages[pdf_page - 1].extract_text() or ""
            text_parts.append(f"\n===== PDF PAGE {pdf_page} =====\n{text}")
            printed_page = pdf_page - 26 if source_key == "base" else pdf_page
            lines = [clean_line(line) for line in text.splitlines() if clean_line(line)]
            earlier = [item for item in outlines[source_key] if item["pdf_page"] < pdf_page]
            if earlier:
                current_section = str(earlier[-1]["section"])
            page_headings = {
                str(item["full_title"]): item
                for item in outlines[source_key]
                if item["pdf_page"] == pdf_page
            }
            for line in lines:
                heading = page_headings.get(line)
                if heading:
                    current_section = str(heading["section"])
                    sections.append(
                        {
                            "section": current_section,
                            "title": heading["title"],
                            "printed_page": printed_page,
                            "pdf_page": pdf_page,
                        }
                    )
                figure_match = FIGURE.match(line)
                if figure_match:
                    if re.search(r"\.{4,}", figure_match.group(2)):
                        continue
                    caption = caption_only(figure_match.group(2))
                    figures.append(
                        {
                            "number": int(figure_match.group(1)),
                            "caption": caption,
                            "section": current_section,
                            "printed_page": printed_page,
                            "pdf_page": pdf_page,
                        }
                    )
                table_match = TABLE.match(line)
                if table_match:
                    if re.search(r"\.{4,}", table_match.group(2)):
                        continue
                    tables.append(
                        {
                            "number": int(table_match.group(1)),
                            "caption": caption_only(table_match.group(2)),
                            "section": current_section,
                            "printed_page": printed_page,
                            "pdf_page": pdf_page,
                        }
                    )
            page_records.append(
                {"printed_page": printed_page, "pdf_page": pdf_page, "text_length": len(text)}
            )
        (args.output_dir / f"{report_id}.txt").write_text(
            "".join(text_parts), encoding="utf-8"
        )
        def deduplicate(records: list[dict[str, object]]) -> list[dict[str, object]]:
            deduplicated: dict[int, dict[str, object]] = {}
            for record in records:
                number = int(record["number"])
                if number not in deduplicated:
                    deduplicated[number] = {
                        **record,
                        "printed_pages": str(record["printed_page"]),
                        "pdf_pages": str(record["pdf_page"]),
                    }
                    continue
                item = deduplicated[number]
                first_printed = min(
                    int(str(item["printed_pages"]).split("-")[0]),
                    int(record["printed_page"]),
                )
                last_printed = max(
                    int(str(item["printed_pages"]).split("-")[-1]),
                    int(record["printed_page"]),
                )
                first_pdf = min(
                    int(str(item["pdf_pages"]).split("-")[0]),
                    int(record["pdf_page"]),
                )
                last_pdf = max(
                    int(str(item["pdf_pages"]).split("-")[-1]),
                    int(record["pdf_page"]),
                )
                item["printed_pages"] = (
                    str(first_printed)
                    if first_printed == last_printed
                    else f"{first_printed}-{last_printed}"
                )
                item["pdf_pages"] = (
                    str(first_pdf) if first_pdf == last_pdf else f"{first_pdf}-{last_pdf}"
                )
            return list(deduplicated.values())

        inventory["reports"][report_id] = {
            "source": source_key,
            "pdf_page_ranges": [f"{first}-{last}" for first, last in page_ranges],
            "pages": page_records,
            "sections": sections,
            "figures": deduplicate(figures),
            "tables": deduplicate(tables),
        }

    (args.output_dir / "inventory.json").write_text(
        json.dumps(inventory, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"Extracted {len(RANGES)} report evidence sets to {args.output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
