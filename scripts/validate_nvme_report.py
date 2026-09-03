#!/usr/bin/env python3
"""驗證 NVMe 十份報告、四十個版本、來源定位與離線 HTML 契約。"""

from __future__ import annotations

import argparse
import hashlib
import html as html_lib
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
FORBIDDEN_PUBLISHED = re.compile(
    r"NVMe\s+over\s+Fabrics|\bFabrics?\b|message-based|"
    r"\bDiscovery\b|command\s+capsule|response\s+capsule|\bcapsules?\b|\bNQN\b|"
    r"Exported\s+NVM\s+Subsystem|Cross-Controller\s+Reset|Lost\s+Host\s+Communication|"
    r"Pull\s+Model\s+DDC",
    re.IGNORECASE,
)
PLACEHOLDER_PHRASES = (
    "提供本節概念、支援條件或範例的結構化索引",
    "Provides a structured index to a concept",
    "選一個具體 controller 設定",
    "Choose a concrete controller configuration",
    "所指的特定關係或範例",
    "Explains the specific relationship or example named",
)
SOURCE_KEYWORDS = {
    "shall not",
    "should not",
    "shall",
    "should",
    "may",
    "mandatory",
    "optional",
    "reserved",
}


def forbidden_published(text: str, report_id: str):
    # NVM 1.3 §5.4 explicitly defines a memory-based template. The standalone
    # full-command-set scope includes it; its NQN field remains excluded.
    if report_id == 'nvm-command-set-1.3':
        text = re.sub(r'\bExported\s+NVM\s+Subsystem\b', '', text, flags=re.I)
    return FORBIDDEN_PUBLISHED.search(text)


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
        self.viewport_content = ""
        self.has_color_scheme = False
        self.theme_color_count = 0
        self.style_count = 0
        self.table_stack: list[int] = []
        self.max_table_columns = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {key.lower(): value or "" for key, value in attrs}
        tag = tag.lower()
        if tag == "html":
            self.lang = values.get("lang", "")
        if tag == "meta" and values.get("name", "").lower() == "viewport":
            self.has_viewport = True
            self.viewport_content = values.get("content", "")
        if tag == "meta" and values.get("name", "").lower() == "color-scheme":
            self.has_color_scheme = values.get("content", "").strip() == "light dark"
        if tag == "meta" and values.get("name", "").lower() == "theme-color":
            self.theme_color_count += 1
        if tag == "style":
            self.style_count += 1
        if tag in {"script", "iframe", "object", "embed"}:
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
    text = path.read_text(encoding="utf-8")
    parser.feed(text)
    errors = list(dict.fromkeys(parser.errors))
    if parser.lang != "zh-Hant-TW":
        errors.append(f'html lang 必須是 "zh-Hant-TW"，目前為 {parser.lang!r}')
    if not parser.has_viewport:
        errors.append("缺少 viewport meta")
    elif "viewport-fit=cover" not in parser.viewport_content:
        errors.append("viewport meta 缺少 viewport-fit=cover")
    if not parser.has_color_scheme:
        errors.append('缺少 color-scheme meta，或 content 不是 "light dark"')
    if parser.theme_color_count < 2:
        errors.append("HTML 必須提供 light／dark theme-color")
    if parser.style_count != 1:
        errors.append(f"HTML 必須使用一個內嵌 <style>，目前為 {parser.style_count} 個")
    for required_css in (
        "prefers-color-scheme: dark",
        "--spec:",
        "--explain:",
        "--infer:",
        "--example:",
        "--warn:",
        "--diagram-line:",
        "--command:",
        "--object:",
        "--decision:",
        "--success:",
        "--failure:",
        ".table-wrap",
        "-webkit-text-size-adjust: 100%",
        "safe-area-inset-top",
        "min-height: 44px",
        "prefers-reduced-motion: reduce",
        ":focus-visible",
        "@media (min-width: 1200px)",
    ):
        if required_css not in text:
            errors.append(f"內嵌 CSS 缺少資訊設計 token：{required_css}")
    if parser.max_table_columns > max_columns:
        errors.append(
            f"表格最多偵測到 {parser.max_table_columns} 欄；iPad 契約建議不超過 {max_columns} 欄"
        )
    for required_html in (
        'class="skip-link"',
        'class="ipad-read-guide"',
        'class="visual-atlas"',
        'class="visual-legend"',
        'class="legend-swatch role-command"',
        'class="legend-swatch role-object"',
        'class="legend-swatch role-decision"',
        'class="legend-swatch role-success"',
        'class="legend-swatch role-failure"',
        "<summary",
        "<figure",
        "<figcaption",
    ):
        if required_html not in text:
            errors.append(f"缺少 iPad 原生閱讀結構：{required_html}")
    if not re.search(r'<body class="edition-(?:tutorial|reference)">', text):
        errors.append("HTML 必須標示 tutorial 或 reference edition")
    if 'data-visual-kind="' not in text:
        errors.append("HTML 圖解缺少 data-visual-kind，無法辨識圖形用途")
    svg_blocks = re.findall(r"<svg\b.*?</svg>", text, re.IGNORECASE | re.DOTALL)
    for index, block in enumerate(svg_blocks, 1):
        if "<title" not in block or "<desc" not in block:
            errors.append(f"第 {index} 個 inline SVG 缺少 title／desc")
    return errors


def claim_ids(text: str) -> set[str]:
    return set(CLAIM_MARKER.findall(text))


def claim_id_sequence(text: str) -> list[str]:
    return CLAIM_MARKER.findall(text)


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
    if len(artifacts) != 40 or formats.count("html") != 20 or formats.count("markdown") != 20:
        errors.append("輸出契約必須固定為二十份 HTML 與二十份 Markdown")
    report_ids = {item.get("id") for item in scope.get("reports", [])}
    artifact_report_ids = {item.get("report_id") for item in artifacts}
    if len(report_ids) != 10 or artifact_report_ids != report_ids:
        errors.append("輸出契約必須完整對應 scope.json 的十份報告")
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
    try:
        from scripts.build_nvme_reports import REPORT_MODULES
        from scripts.nvme_report_questions import validate_questions
    except ModuleNotFoundError:
        from build_nvme_reports import REPORT_MODULES
        from nvme_report_questions import validate_questions
    errors = validate_setup(None)
    scope = load_json("scope.json")
    contract = load_json("output-contract.json")
    claims_doc = load_json("claims.json")
    figure_doc = load_json("figure-table-register.json")
    source_ids = {item["id"] for item in load_json("source-register.json")["sources"]}
    figure_entries = figure_doc.get("entries", [])
    included_figures_by_report: dict[str, list[dict]] = {}
    for item in figure_entries:
        if item.get("scope_status") == "INCLUDE":
            included_figures_by_report.setdefault(item.get("report_id", ""), []).append(item)
    report_scopes = {item.get("id"): item for item in scope.get("reports", [])}
    for report_id, report_scope in report_scopes.items():
        allowlist = set(report_scope.get("included_figure_ids", []))
        if not allowlist:
            continue
        actual = {
            item.get("id") for item in included_figures_by_report.get(report_id, [])
        }
        if actual != allowlist:
            errors.append(
                f"{report_id} 的 included_figure_ids 與 Figure register 不一致："
                f"missing={sorted(allowlist - actual)}, extra={sorted(actual - allowlist)}"
            )

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
    artifact_claim_sequences: dict[str, list[str]] = {}
    artifact_texts: dict[str, str] = {}
    max_columns = int(contract.get("html_policy", {}).get("recommended_max_table_columns", 4))
    for artifact in contract.get("artifacts", []):
        path = ROOT / artifact["path"]
        if not path.is_file():
            errors.append(f"缺少輸出：{artifact['path']}")
            continue
        text = path.read_text(encoding="utf-8")
        artifact_texts[artifact["id"]] = text
        for error in validate_questions(
            artifact['report_id'], REPORT_MODULES[artifact['report_id']], claims,
            text, 'en' if artifact.get('language') == 'en' else 'zh', artifact['format'],
        ):
            errors.append(f"{artifact['path']}：{error}")
        ids = claim_ids(text)
        artifact_claims[artifact["id"]] = ids
        artifact_claim_sequences[artifact["id"]] = claim_id_sequence(text)
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
        body_field = "en" if artifact.get("language") == "en" else "zh_tw"
        searchable_text = (
            html_lib.unescape(text) if artifact["format"] == "html" else text
        )
        for claim_id in sorted(ids & all_claims):
            citation = claims_by_id[claim_id].get(citation_field, "")
            if not citation or citation not in text:
                errors.append(
                    f"{artifact['path']} 的 {claim_id} 缺少完整 {citation_field} 來源定位"
                )
            expected_body = claims_by_id[claim_id].get(body_field, "")
            body_count = searchable_text.count(expected_body) if expected_body else 0
            if body_count != 1:
                errors.append(
                    f"{artifact['path']} 的 {claim_id} 正文應完整出現一次，目前 {body_count} 次"
                )
        forbidden = forbidden_published(searchable_text, artifact['report_id'])
        if forbidden:
            errors.append(
                f"{artifact['path']} 出現排除範圍詞彙：{forbidden.group(0)}"
            )
        for phrase in PLACEHOLDER_PHRASES:
            if phrase in searchable_text:
                errors.append(f"{artifact['path']} 仍含共用 placeholder：{phrase}")
        if artifact.get("report_id") == "base-admin-fw-logs":
            for required in ("Mental Model", "End-to-End", "Debug", "LID 03h", "007F0003h"):
                if required not in searchable_text:
                    errors.append(f"{artifact['path']} 缺少 firmware 教學結構：{required}")
            for forbidden_heading in ("Figure 逐圖導讀", "Figure-by-Figure Guide"):
                if forbidden_heading in searchable_text:
                    errors.append(
                        f"{artifact['path']} 不得以 {forbidden_heading} 作為教學骨架"
                    )

        if artifact.get("report_id") == "base-self-test-hmb-emulation":
            for required in ("Mental Model", "008C0006h", "HMDL", "DSTRD", "NDT"):
                if required not in searchable_text:
                    errors.append(f"{artifact['path']} 缺少 self-test/HMB 教學結構：{required}")

        if artifact.get("report_id") == "base-self-test-namespace-management":
            for required in (
                "Mental Model", "008C0006h", "NSZE", "NUSE", "NVMSETID",
                "Controller List", "DNCS", "Debug",
            ):
                if required not in searchable_text:
                    errors.append(
                        f"{artifact['path']} 缺少 self-test/namespace 教學結構：{required}"
                    )

        expected_figures = [
            item
            for item in included_figures_by_report.get(artifact.get("report_id", ""), [])
            if artifact["id"] in item.get("required_artifact_ids", [])
        ]
        figure_markers = figure_table_ids(text)
        if len(figure_markers) != len(expected_figures):
            errors.append(
                f"{artifact['path']} Figure 標記數 {len(figure_markers)}，"
                f"應為 {len(expected_figures)}"
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
            if expected_figures and text.count("<details") < len(expected_figures):
                errors.append(f"{artifact['path']} 每張 Figure 應使用 details 提供 iPad 摺疊導覽")
            if expected_figures and text.count('name="figures-') < len(expected_figures):
                errors.append(f"{artifact['path']} 每張 Figure 應使用原生 details name accordion")
            if artifact["id"].endswith("tutorial-html"):
                if expected_figures and text.count("新手教學重畫（非 Spec 原圖）") < len(expected_figures):
                    errors.append(f"{artifact['path']} 每張 Figure 應有新手讀圖教學")
            else:
                if expected_figures and text.count("詳細版查詢重畫") < len(expected_figures):
                    errors.append(f"{artifact['path']} 每張 Figure 應有詳細查詢重畫")
                if expected_figures and text.count("Input／Decode／Validate／Evidence") < len(expected_figures):
                    errors.append(f"{artifact['path']} 每張 Figure 應有欄位解碼索引")
            if expected_figures and 'id="figure-index"' not in text:
                errors.append(f"{artifact['path']} 缺少 Figure 索引")
        else:
            if not text.startswith("---\n"):
                errors.append(f"{artifact['path']} 缺少 Jekyll front matter")
            if "layout: post" not in text:
                errors.append(f"{artifact['path']} 的 layout 必須是 post")
            if "toc: yes" not in text:
                errors.append(f"{artifact['path']} 必須啟用 toc")
            expected_lang = artifact.get("language")
            if not re.search(
                rf"^lang:\s*{re.escape(str(expected_lang))}\s*$", text, re.MULTILINE
            ):
                errors.append(
                    f"{artifact['path']} front matter lang 應為 {expected_lang}"
                )
            if expected_figures and text.count('<details markdown="1">') < len(expected_figures):
                errors.append(f"{artifact['path']} 每張 Figure 應至少有一個 Markdown details")

    parity_groups: dict[str, list[tuple[set[str], list[str]]]] = {}
    for artifact in contract.get("artifacts", []):
        group = artifact.get("parity_group")
        if group and artifact["id"] in artifact_claims:
            parity_groups.setdefault(group, []).append(
                (artifact_claims[artifact["id"]], artifact_claim_sequences[artifact["id"]])
            )
    for group, pairs in parity_groups.items():
        sets = [item[0] for item in pairs]
        sequences = [item[1] for item in pairs]
        if len(sets) > 1 and any(item != sets[0] for item in sets[1:]):
            errors.append(f"parity group {group} 的 claim ID 集合不一致")
        if len(sequences) > 1 and any(item != sequences[0] for item in sequences[1:]):
            errors.append(f"parity group {group} 的 claim 順序不一致")

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
        "title",
    }
    for item in figure_entries:
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
            continue
        declared_status = scope_status[item["scope_entry_id"]]
        if item.get("scope_status") != declared_status:
            errors.append(
                f"Figure/Table {item['id']} scope_status 與 scope.json 不一致"
            )
        scope_entry = next(
            entry
            for entry in scope.get("entries", [])
            if entry.get("id") == item["scope_entry_id"]
        )
        if item.get("scope_status") == "EXCLUDE":
            if str(item["number"]) not in {
                str(number) for number in scope_entry.get("figures", [])
            }:
                errors.append(
                    f"Figure/Table {item['id']} 未列入 scope.json 的明確排除清單"
                )
            if item.get("required_artifact_ids") or item.get("introduced_in"):
                errors.append(f"排除的 Figure/Table {item['id']} 不得宣告輸出 coverage")
            continue
        if item.get("scope_status") != "INCLUDE":
            continue
        if item.get("role") == "referenced_dependency":
            if not item.get("referenced_from"):
                errors.append(f"Figure/Table {item['id']} 缺少 referenced_from")
            if item.get("mode") != "dependency-slice":
                errors.append(f"Figure/Table {item['id']} 的相依教學模式必須是 dependency-slice")
        if (
            item.get("report_id") == "base-admin-fw-logs"
            and item.get("role") == "referenced_dependency"
            and item.get("scope_entry_id") != "BASE-FWLOG-DEPENDENCY-INCLUDE"
        ):
            errors.append(f"Figure/Table {item['id']} 未對應第五份報告的相依範圍")
        if (
            item.get("report_id") == "base-power-features"
            and item.get("role") == "referenced_dependency"
            and item.get("scope_entry_id") != "BASE-POWER-DEPENDENCY-INCLUDE"
        ):
            errors.append(f"Figure/Table {item['id']} 未對應第六份報告的相依範圍")
        if (
            item.get("report_id") == "base-self-test-hmb-emulation"
            and item.get("role") == "referenced_dependency"
            and item.get("scope_entry_id") != "BASE-DIAGMEM-DEPENDENCY-INCLUDE"
        ):
            errors.append(f"Figure/Table {item['id']} 未對應第七份報告的相依範圍")
        if item.get("report_id") == "base-self-test-namespace-management" and item.get("role") == "referenced_dependency":
            expected_scope = (
                "NVMCS-NSMGMT-DEPENDENCY-INCLUDE"
                if item.get("source_id") == "NVME-NVM-CS-1.3"
                else "BASE-NSMGMT-DEPENDENCY-INCLUDE"
            )
            if item.get("scope_entry_id") != expected_scope:
                errors.append(f"Figure/Table {item['id']} 未對應第八份報告的相依範圍")
        if item.get("id") == "BASEFWLOG-FIG-209" and item.get("mode") != "scope-reduced":
            errors.append("BASEFWLOG-FIG-209 必須標示為 scope-reduced")
        if item.get("id") in {"BASEPOWER-FIG-200", "BASEPOWER-FIG-466", "BASEPOWER-FIG-468"} and item.get("mode") != "scope-reduced":
            errors.append(f"{item['id']} 必須標示為 scope-reduced")
        if item.get("id") in {"BASEDIAGMEM-FIG-200", "BASEDIAGMEM-FIG-209", "BASEDIAGMEM-FIG-338", "BASEDIAGMEM-FIG-466"} and not item.get("scope_reduced"):
            errors.append(f"{item['id']} 必須標示 scope_reduced")
        if item.get("id") in {
            "BASENSMGMT-FIG-036", "BASENSMGMT-FIG-155", "BASENSMGMT-FIG-209",
            "BASENSMGMT-FIG-338", "BASENSMGMT-FIG-346", "BASENSMGMT-FIG-474",
            "BASENSMGMT-FIG-123", "BASENSMGMT-FIG-127", "BASENSMGMT-FIG-132",
            "BASENSMGMT-FIG-133",
        } and not item.get("scope_reduced"):
            errors.append(f"{item['id']} 必須標示 scope_reduced")
        if not isinstance(item.get("key_items"), list) or not item.get("key_items"):
            errors.append(f"Figure/Table {item['id']} 缺少來源欄位索引")
        if any(
            not isinstance(value, str) or not value.strip() or len(value) > 80
            for value in item.get("key_items", [])
        ):
            errors.append(f"Figure/Table {item['id']} 的來源欄位索引格式錯誤")
        if any(
            FORBIDDEN_PUBLISHED.search(value)
            for value in item.get("key_items", [])
            if isinstance(value, str)
        ):
            errors.append(f"Figure/Table {item['id']} 的欄位索引含排除內容")
        if not re.fullmatch(r"[0-9a-f]{64}", str(item.get("evidence_digest", ""))):
            errors.append(f"Figure/Table {item['id']} 缺少有效 evidence_digest")
        keywords = item.get("source_keywords")
        if not isinstance(keywords, list) or any(
            keyword not in SOURCE_KEYWORDS for keyword in keywords
        ):
            errors.append(f"Figure/Table {item['id']} 的 source_keywords 無效")
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
