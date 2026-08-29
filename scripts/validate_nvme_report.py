#!/usr/bin/env python3
"""驗證 NVMe 四份報告、十六個版本、來源定位與純 HTML 契約。"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTROL = ROOT / ".ai" / "nvme-report"
CLAIM_MARKER = re.compile(
    r'(?:claim:|data-claim-id=["\'])([A-Z][A-Z0-9-]{2,})(?:["\'])?'
)
FIGURE_TABLE_MARKER = re.compile(
    r'(?:figure-table:|data-figure-table-id=["\'])([A-Z][A-Z0-9-]{2,})(?:["\'])?'
)
ABSOLUTE_PATH = re.compile(r"^(?:[A-Za-z]:[\\/]|/|\\\\)")


def load_json(name: str) -> dict:
    path = CONTROL / name
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(f"無法讀取 {path.relative_to(ROOT)}：{error}") from error


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


class StrictOfflineHTMLParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.errors: list[str] = []
        self.lang = ""
        self.has_viewport = False
        self.table_stack: list[int] = []
        self.max_table_columns = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {key.lower(): value or "" for key, value in attrs}
        tag = tag.lower()
        if tag == "html":
            self.lang = values.get("lang", "")
        if tag == "meta" and values.get("name", "").lower() == "viewport":
            self.has_viewport = True
        if tag in {"style", "script", "iframe", "object", "embed"}:
            self.errors.append(f"禁止 <{tag}>")
        if "style" in values:
            self.errors.append(f"<{tag}> 禁止 style attribute")
        if tag == "link" and values.get("rel", "").lower() == "stylesheet":
            self.errors.append("禁止 stylesheet")
        resource_attr = {
            "img": "src",
            "script": "src",
            "link": "href",
            "iframe": "src",
            "object": "data",
            "embed": "src",
        }.get(tag)
        resource = values.get(resource_attr, "") if resource_attr else ""
        if resource and re.match(r"^(?:https?:)?//", resource, re.IGNORECASE):
            self.errors.append(f"<{tag}> 禁止外部資源：{resource}")
        if tag == "img" and not values.get("alt"):
            self.errors.append("img 必須有 alt")
        if tag == "table":
            self.table_stack.append(0)
        elif tag == "tr" and self.table_stack:
            self.table_stack[-1] = 0
        elif tag in {"th", "td"} and self.table_stack:
            self.table_stack[-1] += 1
            self.max_table_columns = max(self.max_table_columns, self.table_stack[-1])

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "table" and self.table_stack:
            self.table_stack.pop()


def validate_html(path: Path, max_columns: int = 4) -> list[str]:
    parser = StrictOfflineHTMLParser()
    parser.feed(path.read_text(encoding="utf-8"))
    errors = list(dict.fromkeys(parser.errors))
    if parser.lang != "zh-Hant-TW":
        errors.append(f'html lang 必須是 "zh-Hant-TW"，目前為 {parser.lang!r}')
    if not parser.has_viewport:
        errors.append("缺少 viewport meta")
    if parser.max_table_columns > max_columns:
        errors.append(
            f"表格最多偵測到 {parser.max_table_columns} 欄；iPad 契約建議不超過 {max_columns} 欄"
        )
    return errors


def claim_ids(text: str) -> set[str]:
    return set(CLAIM_MARKER.findall(text))


def figure_table_ids(text: str) -> set[str]:
    return set(FIGURE_TABLE_MARKER.findall(text))


def validate_setup(source_dir: Path | None) -> list[str]:
    errors: list[str] = []
    source_register = load_json("source-register.json")
    scope = load_json("scope.json")
    contract = load_json("output-contract.json")
    claims_doc = load_json("claims.json")
    figures = load_json("figure-table-register.json")

    sources = source_register.get("sources", [])
    source_ids = [item.get("id") for item in sources]
    if len(sources) != 3 or len(source_ids) != len(set(source_ids)):
        errors.append("source-register 必須有三個唯一來源 ID")
    for item in sources:
        for field in (
            "id",
            "title",
            "revision",
            "ratified_date",
            "filename",
            "sha256",
            "size_bytes",
            "pdf_pages",
        ):
            if not item.get(field):
                errors.append(f"來源 {item.get('id', '<unknown>')} 缺少 {field}")
        filename = str(item.get("filename", ""))
        if ABSOLUTE_PATH.match(filename):
            errors.append(f"來源 {item.get('id')} 不得保存本機絕對路徑")
        if (ROOT / filename).exists():
            errors.append(f"來源 PDF 不得放在公開儲存庫：{filename}")
        if source_dir:
            source_path = source_dir / filename
            if not source_path.is_file():
                errors.append(f"找不到來源：{source_path}")
            else:
                if source_path.stat().st_size != item.get("size_bytes"):
                    errors.append(f"來源大小不符：{filename}")
                if sha256_file(source_path) != str(item.get("sha256", "")).lower():
                    errors.append(f"來源 SHA-256 不符：{filename}")

    allowed = set(scope.get("allowed_statuses", []))
    if scope.get("default_status") != "EXCLUDE":
        errors.append("未指定範圍的預設狀態必須是 EXCLUDE")
    for entry in scope.get("entries", []):
        if entry.get("status") not in allowed:
            errors.append(f"scope entry {entry.get('id')} 使用未知狀態")
        if entry.get("source_id") not in source_ids:
            errors.append(f"scope entry {entry.get('id')} 使用未知來源")

    artifacts = contract.get("artifacts", [])
    formats = [item.get("format") for item in artifacts]
    if len(artifacts) != 16 or formats.count("html") != 8 or formats.count("markdown") != 8:
        errors.append("輸出契約必須固定為八份 HTML 與八份 Markdown")
    report_ids = {item.get("id") for item in scope.get("reports", [])}
    artifact_report_ids = {item.get("report_id") for item in artifacts}
    if len(report_ids) != 4 or artifact_report_ids != report_ids:
        errors.append("輸出契約必須完整對應 scope.json 的四份報告")
    artifact_ids = [item.get("id") for item in artifacts]
    if len(artifact_ids) != len(set(artifact_ids)):
        errors.append("artifact ID 不得重複")
    paths = [item.get("path") for item in artifacts]
    if len(paths) != len(set(paths)):
        errors.append("輸出路徑不得重複")
    for path in paths:
        if not path or ABSOLUTE_PATH.match(str(path)):
            errors.append(f"輸出路徑必須是儲存庫相對路徑：{path!r}")

    claims = claims_doc.get("claims", [])
    claim_names = [item.get("id") for item in claims]
    if len(claim_names) != len(set(claim_names)):
        errors.append("claim ID 不得重複")
    if not isinstance(figures.get("entries"), list):
        errors.append("figure-table-register entries 必須是陣列")
    return errors


def validate_publish() -> list[str]:
    errors = validate_setup(None)
    scope = load_json("scope.json")
    contract = load_json("output-contract.json")
    claims_doc = load_json("claims.json")
    figure_doc = load_json("figure-table-register.json")
    source_ids = {item["id"] for item in load_json("source-register.json")["sources"]}

    if scope.get("approval_status") != "approved":
        errors.append("scope.json 尚未 approved，禁止 publish")
    if not scope.get("entries"):
        errors.append("scope.json 尚未列出任何核准範圍")
    if any(item.get("status") == "OPEN" for item in scope.get("entries", [])):
        errors.append("publish 階段不得保留 OPEN 範圍")

    claims = claims_doc.get("claims", [])
    allowed_keywords = set(claims_doc.get("allowed_normative_keywords", []))
    if not claims:
        errors.append("publish 階段至少需要一筆 claim")
    required_claim_fields = {
        "id",
        "report_id",
        "source_id",
        "revision",
        "section",
        "figure",
        "table",
        "printed_pages",
        "pdf_pages",
        "normative_keyword",
        "zh_tw",
        "en",
        "citation_zh_tw",
        "citation_en",
        "scope_entry_id",
    }
    scope_status = {item.get("id"): item.get("status") for item in scope.get("entries", [])}
    for item in claims:
        missing = sorted(required_claim_fields - set(item))
        if missing:
            errors.append(f"claim {item.get('id')} 缺少：{', '.join(missing)}")
            continue
        if item["source_id"] not in source_ids:
            errors.append(f"claim {item['id']} 使用未知來源")
        if item["normative_keyword"] not in allowed_keywords:
            errors.append(f"claim {item['id']} 使用未知 normative keyword")
        if item["scope_entry_id"] not in scope_status:
            errors.append(f"claim {item['id']} 未對應核准 scope entry")
        elif scope_status[item["scope_entry_id"]] not in {"INCLUDE", "PREREQUISITE_ONLY"}:
            errors.append(
                f"claim {item['id']} 對應 {scope_status[item['scope_entry_id']]} 範圍，不得公開"
            )

    all_claims = {item.get("id") for item in claims if item.get("id")}
    claims_by_id = {item.get("id"): item for item in claims if item.get("id")}
    claims_by_report: dict[str, set[str]] = {}
    for item in claims:
        if item.get("id") and item.get("report_id"):
            claims_by_report.setdefault(item["report_id"], set()).add(item["id"])
    artifact_claims: dict[str, set[str]] = {}
    artifact_texts: dict[str, str] = {}
    max_columns = int(contract.get("html_policy", {}).get("recommended_max_table_columns", 4))
    for artifact in contract.get("artifacts", []):
        path = ROOT / artifact["path"]
        if not path.is_file():
            errors.append(f"缺少輸出：{artifact['path']}")
            continue
        text = path.read_text(encoding="utf-8")
        artifact_texts[artifact["id"]] = text
        ids = claim_ids(text)
        artifact_claims[artifact["id"]] = ids
        unknown = sorted(ids - all_claims)
        if unknown:
            errors.append(f"{artifact['path']} 出現未知 claim：{', '.join(unknown)}")
        expected_claims = claims_by_report.get(artifact.get("report_id", ""), set())
        unrelated = sorted(ids - expected_claims)
        if unrelated:
            errors.append(f"{artifact['path']} 包含其他報告的 claim：{', '.join(unrelated)}")
        if artifact.get("claim_coverage") == "all":
            missing = sorted(expected_claims - ids)
            if missing:
                errors.append(f"{artifact['path']} 缺少 claim：{', '.join(missing)}")
        citation_field = "citation_en" if artifact.get("language") == "en" else "citation_zh_tw"
        for claim_id in sorted(ids & all_claims):
            citation = claims_by_id[claim_id].get(citation_field, "")
            if not citation or citation not in text:
                errors.append(
                    f"{artifact['path']} 的 {claim_id} 缺少完整 {citation_field} 來源定位"
                )
        source_markers = contract.get("source_markers", {})
        for source_id in artifact.get("required_source_ids", []):
            marker = source_markers.get(source_id)
            if not marker:
                errors.append(f"{artifact['path']} 的來源 {source_id} 未設定版本標記")
                continue
            if marker not in text:
                errors.append(f"{artifact['path']} 缺少來源版本標記：{marker}")
        if artifact["format"] == "html":
            for message in validate_html(path, max_columns):
                errors.append(f"{artifact['path']}：{message}")
        else:
            if not text.startswith("---\n"):
                errors.append(f"{artifact['path']} 缺少 Jekyll front matter")
            if "layout: post" not in text:
                errors.append(f"{artifact['path']} 的 layout 必須是 post")
            if "toc: yes" not in text:
                errors.append(f"{artifact['path']} 必須啟用 toc")

    parity_groups: dict[str, list[set[str]]] = {}
    for artifact in contract.get("artifacts", []):
        group = artifact.get("parity_group")
        if group and artifact["id"] in artifact_claims:
            parity_groups.setdefault(group, []).append(artifact_claims[artifact["id"]])
    for group, sets in parity_groups.items():
        if len(sets) > 1 and any(item != sets[0] for item in sets[1:]):
            errors.append(f"parity group {group} 的 claim ID 集合不一致")

    required_figure_fields = {
        "id",
        "report_id",
        "source_id",
        "type",
        "number",
        "section",
        "printed_pages",
        "pdf_pages",
        "scope_entry_id",
        "scope_status",
        "mode",
        "required_artifact_ids",
        "introduced_in",
    }
    for item in figure_doc.get("entries", []):
        missing_fields = sorted(required_figure_fields - set(item))
        if missing_fields:
            errors.append(
                f"Figure/Table {item.get('id', '<unknown>')} 缺少：{', '.join(missing_fields)}"
            )
            continue
        if item["source_id"] not in source_ids:
            errors.append(f"Figure/Table {item['id']} 使用未知來源")
        if item["type"] not in {"Figure", "Table"}:
            errors.append(f"Figure/Table {item['id']} type 必須是 Figure 或 Table")
        if item["scope_entry_id"] not in scope_status:
            errors.append(f"Figure/Table {item['id']} 未對應核准 scope entry")
        if item.get("scope_status") != "INCLUDE":
            continue
        coverage = set(item.get("introduced_in", []))
        required_coverage = set(item.get("required_artifact_ids", []))
        missing = sorted(required_coverage - coverage)
        if missing:
            errors.append(
                f"Figure/Table {item.get('id', '<unknown>')} 缺少介紹版本：{', '.join(missing)}"
            )
        for artifact_id in coverage:
            if artifact_id not in artifact_texts:
                errors.append(f"Figure/Table {item['id']} 指向未知或缺少的輸出：{artifact_id}")
            elif item["id"] not in figure_table_ids(artifact_texts[artifact_id]):
                errors.append(f"輸出 {artifact_id} 未包含 Figure/Table 標記：{item['id']}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase", choices=("auto", "setup", "publish"), default="auto")
    parser.add_argument("--source-dir", type=Path, help="本機三份 PDF 所在目錄；不會寫入登記檔")
    args = parser.parse_args()

    try:
        phase = args.phase
        if phase == "auto":
            scope = load_json("scope.json")
            phase = "publish" if scope.get("production_status") == "ready_for_publish" else "setup"
        errors = validate_publish() if phase == "publish" else validate_setup(args.source_dir)
    except ValueError as error:
        errors = [str(error)]

    if errors:
        for error in errors:
            print(f"[FAIL] {error}")
        return 1
    source_note = "，含本機來源 SHA-256" if args.source_dir else ""
    print(f"[OK] NVMe report {phase} contract validated{source_note}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
