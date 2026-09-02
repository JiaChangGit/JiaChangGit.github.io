#!/usr/bin/env python3
"""Build NVMe reports from tracked scope, claims, and compact PDF evidence."""

from __future__ import annotations

import argparse
import html
import json
import re
from pathlib import Path

try:
    from scripts.nvme_teaching_content import (
        REPORT_GLOSSARIES,
        REPORT_MODULES,
        TERM_LIBRARY,
        expanded_figure_guide,
        term_definition,
    )
except ModuleNotFoundError:  # Direct execution puts scripts/ on sys.path.
    from nvme_teaching_content import (
        REPORT_GLOSSARIES,
        REPORT_MODULES,
        TERM_LIBRARY,
        expanded_figure_guide,
        term_definition,
    )


ROOT = Path(__file__).resolve().parents[1]
CONTROL = ROOT / ".ai" / "nvme-report"
SOURCES = {
    "NVME-BASE-2.4": {
        "revision": "2.4",
        "marker": "NVM Express Base Specification, Revision 2.4",
    },
    "NVME-PCIE-TRANSPORT-1.4": {
        "revision": "1.4",
        "marker": "NVM Express NVMe over PCIe Transport Specification, Revision 1.4",
    },
    "NVME-NVM-CS-1.3": {
        "revision": "1.3",
        "marker": "NVM Express NVM Command Set Specification, Revision 1.3",
    },
}


HTML_CSS = """
:root {
  color-scheme: light dark;
  --bg: #f4f7fb;
  --surface: #ffffff;
  --surface-2: #edf2f8;
  --text: #182235;
  --muted: #53627a;
  --line: #cbd6e5;
  --accent: #1d4ed8;
  --accent-soft: #dbeafe;
  --spec: #1d4ed8;
  --spec-soft: #eff6ff;
  --explain: #0f766e;
  --explain-soft: #ecfdf5;
  --infer: #7e22ce;
  --infer-soft: #faf5ff;
  --example: #15803d;
  --example-soft: #f0fdf4;
  --warn: #c2410c;
  --warn-soft: #fff7ed;
  --diagram-line: #475569;
  --diagram-line-soft: #94a3b8;
  --command: var(--spec);
  --command-soft: var(--spec-soft);
  --object: var(--explain);
  --object-soft: var(--explain-soft);
  --decision: var(--infer);
  --decision-soft: var(--infer-soft);
  --success: var(--example);
  --success-soft: var(--example-soft);
  --failure: var(--warn);
  --failure-soft: var(--warn-soft);
  --shadow: 0 10px 28px rgba(31, 53, 84, .10);
}
* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  margin: 0;
  background: var(--bg);
  color: var(--text);
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans TC", sans-serif;
  font-size: 17px;
  line-height: 1.72;
  -webkit-text-size-adjust: 100%;
  text-size-adjust: 100%;
}
a { color: var(--accent); text-underline-offset: .18em; }
a:focus-visible, summary:focus-visible { outline: 3px solid var(--warn); outline-offset: 3px; }
code, pre, kbd, samp { font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }
code { background: var(--surface-2); border-radius: .32rem; padding: .08rem .3rem; }
pre { background: #101827; color: #e5eefc; border-radius: .8rem; padding: 1rem; overflow: auto; line-height: 1.5; }
.topbar {
  position: sticky;
  top: 0;
  z-index: 5;
  border-bottom: 1px solid var(--line);
  background: color-mix(in srgb, var(--surface) 92%, transparent);
  backdrop-filter: blur(12px);
  padding-top: env(safe-area-inset-top);
}
.topbar-inner, main { width: min(900px, calc(100% - 28px)); margin-inline: auto; }
.topbar-inner { padding: .7rem 0; white-space: nowrap; overflow-x: auto; }
.topbar a { display: inline-flex; align-items: center; min-height: 44px; padding-inline: .28rem; }
section, article, details { scroll-margin-top: 4.25rem; }
main { padding: 1.3rem 0 4rem; }
.skip-link { position: fixed; left: .75rem; top: -8rem; z-index: 99; background: var(--warn); color: #fff; border-radius: .5rem; padding: .75rem 1rem; }
.skip-link:focus { top: calc(.5rem + env(safe-area-inset-top)); }
.hero {
  background: linear-gradient(135deg, var(--surface), var(--accent-soft));
  border: 1px solid var(--line);
  border-left: .45rem solid var(--accent);
  border-radius: 1rem;
  box-shadow: var(--shadow);
  padding: clamp(1.2rem, 4vw, 2.4rem);
  margin: 1rem 0 1.5rem;
}
.hero h1 { margin: 0 0 .45rem; font-size: clamp(1.9rem, 5vw, 3rem); line-height: 1.16; letter-spacing: -.025em; }
.eyebrow { color: var(--accent); font-size: .78rem; font-weight: 800; letter-spacing: .11em; text-transform: uppercase; }
.subtitle { color: var(--muted); font-size: 1.08rem; margin-bottom: 0; }
section, article.topic-card, details.figure-card {
  background: var(--surface);
  border: 1px solid var(--line);
  border-radius: .9rem;
  box-shadow: 0 4px 16px rgba(31, 53, 84, .06);
  margin: 1rem 0;
  padding: clamp(1rem, 3vw, 1.55rem);
}
section section { box-shadow: none; }
section > p, article.topic-card > p, .figure-card > p { max-width: 80ch; }
h2 { margin-top: 0; padding-bottom: .4rem; border-bottom: 2px solid var(--accent-soft); font-size: clamp(1.45rem, 4vw, 2rem); line-height: 1.3; }
h3 { line-height: 1.35; }
.toc ol { columns: 2; column-gap: 2rem; }
.toc li { break-inside: avoid; margin: .3rem 0; }
.badge {
  display: inline-block;
  border: 1px solid currentColor;
  border-radius: 999px;
  font-size: .76rem;
  font-weight: 800;
  line-height: 1;
  padding: .32rem .55rem;
  vertical-align: .12em;
}
.badge-spec { color: var(--spec); background: var(--spec-soft); }
.badge-explain { color: var(--explain); background: var(--explain-soft); }
.badge-infer { color: var(--infer); background: var(--infer-soft); }
.badge-example { color: var(--example); background: var(--example-soft); }
.badge-warn { color: var(--warn); background: var(--warn-soft); }
.callout { border-left: .35rem solid; border-radius: .55rem; padding: .8rem 1rem; margin: .85rem 0; }
.spec { border-color: var(--spec); background: var(--spec-soft); }
.explain { border-color: var(--explain); background: var(--explain-soft); }
.infer { border-color: var(--infer); background: var(--infer-soft); }
.example { border-color: var(--example); background: var(--example-soft); }
.warning { border-color: var(--warn); background: var(--warn-soft); }
fieldset { border: 1px solid var(--line); border-left: .35rem solid var(--explain); border-radius: .7rem; background: var(--explain-soft); margin: 1rem 0; padding: 1rem; }
legend { color: var(--explain); font-weight: 800; padding: 0 .4rem; }
mark { background: var(--accent-soft); color: var(--accent); border-radius: .3rem; padding: .1rem .35rem; }
.table-wrap { overflow-x: auto; margin: .85rem 0; border: 1px solid var(--line); border-radius: .7rem; }
table { width: 100%; min-width: 560px; border-collapse: collapse; background: var(--surface); }
th, td { border-bottom: 1px solid var(--line); padding: .68rem .72rem; text-align: left; vertical-align: top; }
th { background: var(--surface-2); color: var(--text); }
tr:last-child td { border-bottom: 0; }
.term { color: var(--accent); font-weight: 750; white-space: nowrap; }
.flow-svg { width: 100%; height: auto; background: var(--surface-2); border: 1px solid var(--line); border-radius: .8rem; }
.flow-node { fill: var(--surface); stroke: var(--accent); stroke-width: 2; }
.flow-node-alt { fill: var(--accent-soft); stroke: var(--accent); stroke-width: 2; }
.flow-line { stroke: var(--accent); stroke-width: 2.2; }
.flow-text { fill: var(--text); font-size: 14px; font-weight: 650; }
.mini-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: .8rem; }
.mini-card { border: 1px solid var(--line); border-radius: .65rem; background: var(--surface-2); padding: .8rem; }
.mini-card p { margin: .25rem 0; }
details { margin: .8rem 0; }
details > summary { cursor: pointer; color: var(--accent); font-weight: 750; min-height: 44px; display: flex; align-items: center; padding: .35rem .2rem; }
details.figure-card[open] > summary { border-bottom: 1px solid var(--line); margin-bottom: 1rem; padding-bottom: .8rem; }
.figure-meta { color: var(--muted); font-size: .92rem; }
.source-note { color: var(--muted); border-top: 1px dashed var(--line); margin-top: .8rem; padding-top: .65rem; font-size: .88rem; }
.chapter-bridge { color: var(--muted); font-size: 1.04rem; }
.back { text-align: right; font-size: .9rem; }
.ipad-toc { background: var(--surface); border: 1px solid var(--line); border-left: .35rem solid var(--accent); border-radius: .8rem; padding: .55rem 1rem; margin: 1rem 0; }
.ipad-toc > summary { min-height: 44px; display: flex; align-items: center; cursor: pointer; color: var(--accent); font-weight: 800; }
.ipad-toc a { display: inline-flex; align-items: center; min-height: 44px; padding-block: .3rem; }
.toc-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: .45rem .8rem; padding: .55rem 0; }
.toc-grid a { display: flex; align-items: center; min-height: 44px; border: 1px solid var(--line); border-radius: .55rem; background: var(--surface-2); padding: .45rem .7rem; text-decoration: none; }
.ipad-read-guide { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: .65rem; margin: 1rem 0; }
.read-chip { border: 1px solid var(--line); border-radius: .7rem; background: var(--surface); padding: .8rem; }
.read-chip strong { display: block; color: var(--accent); margin-bottom: .15rem; }
.visual-atlas { display: grid; grid-template-columns: minmax(0, 1fr); gap: 1rem; overflow: visible; padding: .25rem .15rem 1rem; }
.visual-card { min-width: 0; border: 1px solid var(--line); border-top: .32rem solid var(--accent); border-radius: .8rem; background: var(--surface); padding: 1rem; }
.visual-card[data-visual-kind="architecture"] { border-top-color: var(--object); }
.visual-card[data-visual-kind="sequence"] { border-top-color: var(--command); }
.visual-card[data-visual-kind="decode"] { border-top-color: var(--decision); }
.visual-card[data-visual-kind="state"] { border-top-color: var(--failure); }
.visual-card h3 { margin-top: 0; }
.visual-card p:last-child { margin-bottom: 0; }
.visual-board { border: 1px solid var(--line); border-radius: .8rem; background: var(--surface-2); padding: .65rem; margin: .9rem 0; }
.visual-board svg { display: block; width: 100%; height: auto; }
.visual-board figcaption { color: var(--muted); font-size: .86rem; margin-top: .55rem; }
.v-source, .v-command { fill: var(--command-soft); stroke: var(--command); stroke-width: 2; }
.v-structure, .v-object { fill: var(--object-soft); stroke: var(--object); stroke-width: 2; }
.v-state, .v-decision { fill: var(--decision-soft); stroke: var(--decision); stroke-width: 2; }
.v-evidence, .v-success { fill: var(--success-soft); stroke: var(--success); stroke-width: 3; }
.v-warning, .v-failure { fill: var(--failure-soft); stroke: var(--failure); stroke-width: 2.5; stroke-dasharray: 7 4; }
.v-line { stroke: var(--diagram-line); stroke-width: 2.2; fill: none; }
.v-line-soft { stroke: var(--diagram-line-soft); stroke-width: 1.5; fill: none; }
.v-line-dashed { stroke: var(--failure); stroke-width: 2; fill: none; stroke-dasharray: 7 5; }
.v-arrow { fill: var(--diagram-line); stroke: none; }
.v-arrow-failure { fill: var(--failure); stroke: none; }
.v-label-bg { fill: var(--surface-2); stroke: none; opacity: .96; }
.v-label { fill: var(--text); font-size: 14px; font-weight: 700; }
.v-small { fill: var(--muted); font-size: 11.5px; }
.v-role { fill: var(--muted); font-size: 10px; font-weight: 800; letter-spacing: .08em; }
.visual-legend { display: grid; grid-template-columns: repeat(5, minmax(0, 1fr)); gap: .55rem; margin: 1rem 0; }
.legend-item { border: 1px solid var(--line); border-radius: .7rem; background: var(--surface); padding: .72rem; min-width: 0; }
.legend-item strong { display: block; margin: .2rem 0; }
.legend-item small { color: var(--muted); }
.legend-swatch { display: inline-grid; place-items: center; width: 2rem; height: 1.45rem; border: 2px solid; border-radius: .35rem; font-size: .65rem; font-weight: 900; }
.role-command { color: var(--command); background: var(--command-soft); }
.role-object { color: var(--object); background: var(--object-soft); }
.role-decision { color: var(--decision); background: var(--decision-soft); transform: rotate(45deg); border-radius: .18rem; }
.role-decision > span { transform: rotate(-45deg); }
.role-success { color: var(--success); background: var(--success-soft); border-style: double; border-width: 3px; }
.role-failure { color: var(--failure); background: var(--failure-soft); border-style: dashed; }
.edition-note { border-left: .35rem solid var(--accent); background: var(--accent-soft); border-radius: .65rem; padding: .8rem 1rem; margin: 1rem 0; }
.reference-module { border-left: .35rem solid var(--decision); }
.claim-meta { display: grid; grid-template-columns: max-content 1fr; gap: .25rem .8rem; margin: .8rem 0; }
.claim-meta dt { color: var(--muted); font-weight: 700; }
.claim-meta dd { margin: 0; }
.worksheet { border-left: .35rem solid var(--infer); }
.req-shall { color: var(--warn); background: var(--warn-soft); }
.req-should { color: #9a6700; background: #fff8c5; }
.req-may { color: var(--spec); background: var(--spec-soft); }
.req-reserved { color: var(--muted); background: var(--surface-2); }
.table-wrap thead th { position: sticky; top: calc(58px + env(safe-area-inset-top)); z-index: 2; }
.table-wrap th:first-child, .table-wrap td:first-child { position: sticky; left: 0; background: var(--surface); z-index: 1; }
@media (max-width: 700px) {
  body { font-size: 16px; }
  .toc ol { columns: 1; }
  .mini-grid { grid-template-columns: 1fr; }
  table { min-width: 500px; }
  .hero { border-radius: .75rem; }
  .toc-grid, .ipad-read-guide, .visual-legend { grid-template-columns: 1fr; }
  .claim-meta { grid-template-columns: 1fr; }
  .claim-meta dt { margin-top: .35rem; }
}
@media (min-width: 1200px) {
  .topbar-inner, main { width: min(1180px, calc(100% - 48px)); }
  .toc-grid { grid-template-columns: repeat(3, minmax(0, 1fr)); }
  .visual-atlas { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .edition-reference .visual-atlas { grid-template-columns: 1fr; }
  .edition-reference .visual-card { display: grid; grid-template-columns: minmax(0, 1.25fr) minmax(16rem, .75fr); gap: 0 1.2rem; align-items: start; }
  .edition-reference .visual-card > .eyebrow, .edition-reference .visual-card > h3 { grid-column: 1 / -1; }
  .edition-reference .visual-card > .visual-board { grid-row: span 4; }
  .edition-reference table { min-width: 680px; }
}
@media (pointer: fine) {
  summary:hover, .toc-grid a:hover, .topbar a:hover { background: var(--accent-soft); border-radius: .4rem; }
}
@media (prefers-color-scheme: dark) {
  :root {
    --bg: #0c1220;
    --surface: #131d2e;
    --surface-2: #1a2940;
    --text: #e8eef8;
    --muted: #a8b5c8;
    --line: #34445d;
    --accent: #7fb0ff;
    --accent-soft: #172b4b;
    --spec: #93c5fd;
    --spec-soft: #142a49;
    --explain: #5eead4;
    --explain-soft: #12332f;
    --infer: #d8b4fe;
    --infer-soft: #2c1940;
    --example: #86efac;
    --example-soft: #14351f;
    --warn: #fdba74;
    --warn-soft: #3d2413;
    --diagram-line: #cbd5e1;
    --diagram-line-soft: #64748b;
    --shadow: 0 10px 28px rgba(0, 0, 0, .28);
  }
}
@media (prefers-reduced-motion: reduce) {
  html { scroll-behavior: auto; }
  *, *::before, *::after { scroll-behavior: auto !important; transition-duration: .001ms !important; animation-duration: .001ms !important; }
}
@media (forced-colors: active) {
  .callout, .visual-card, .visual-board, .badge, .legend-item, .legend-swatch { forced-color-adjust: auto; border: 2px solid CanvasText; }
}
@media print {
  .topbar { position: static; }
  body { background: #fff; color: #111; font-size: 11pt; }
  section, article.topic-card, details.figure-card, .hero { box-shadow: none; break-inside: avoid; }
  details > * { display: block; }
  .visual-atlas { display: block; overflow: visible; }
  .visual-card { break-inside: avoid; margin: 1rem 0; }
  .table-wrap thead th { position: static; }
}
"""


def page_shift(value: str, delta: int) -> str:
    return re.sub(r"\d+", lambda match: str(int(match.group()) + delta), value)


def c(
    key,
    section,
    pages,
    zh,
    en,
    keyword="none",
    source="NVME-BASE-2.4",
    scope_entry=None,
):
    pdf_pages = (
        pages
        if source in {"NVME-PCIE-TRANSPORT-1.4", "NVME-NVM-CS-1.3"}
        else page_shift(pages, 26)
    )
    return {
        "key": key,
        "source_id": source,
        "section": section,
        "printed_pages": pages,
        "pdf_pages": pdf_pages,
        "normative_keyword": keyword,
        "zh_tw": zh,
        "en": en,
        "scope_entry_id": scope_entry,
    }


REPORTS = {
    "base-ch1-2": {
        "prefix": "BASE12",
        "title_zh": "NVMe Base 2.4 第 1、2 章：規格語言、PCIe 佇列與儲存模型",
        "title_en": "NVMe Base 2.4 Chapters 1-2: Specification Language, PCIe Queues, and Storage Model",
        "source_id": "NVME-BASE-2.4",
        "scope_entry": "BASE12-INCLUDE",
        "range": "§1-§2；文件頁 1-37；PDF 頁 27-63",
        "range_en": "§1-§2; printed pages 1-37; PDF pages 27-63",
        "diagram": ["Host / CPU core", "Submission Queue", "NVMe controller", "Completion Queue"],
        "diagram_note_zh": "命令由 host 放入 Submission Queue；controller 取走並執行，再把完成結果寫入 Completion Queue。",
        "diagram_note_en": "The host places commands in a Submission Queue; the controller fetches and executes them, then posts completions to a Completion Queue.",
        "claims": [
            c("FAMILY", "1.1.1", "1", "Base Specification 定義通用 NVMe 協定；Transport Specification 綁定特定傳輸，I/O Command Set Specification 擴充命令與資料結構。這是適用關係，不是協定堆疊。", "The Base Specification defines the common NVMe protocol; a Transport Specification binds it to a transport, and an I/O Command Set Specification extends commands and data structures. This is an applicability relationship, not a protocol stack."),
            c("KEYWORDS", "1.4.1", "2-3", "規格的 mandatory、may、optional、reserved、shall、should 各有固定語氣；詳細版保留英文 keyword，不能把 may 或 should 翻成 shall。", "The specification assigns distinct force to mandatory, may, optional, reserved, shall, and should. A summary must not strengthen may or should into shall."),
            c("NUMBERS", "1.4.2", "3-5", "數值的解讀同時包含進位與單位；十六進位使用 h 後綴，二進位使用 b 後綴，十進位可省略 d。十進位與二進位容量前綴代表不同倍率。", "A value is interpreted together with its radix and units. Hexadecimal uses the h suffix, binary uses b, and decimal may omit d. Decimal and binary capacity prefixes represent different multipliers."),
            c("DWORD", "1.4.3", "5", "NVMe 以 byte、word、dword 表示欄位位置；一個 word 為 2 bytes，一個 dword 為 4 bytes。解欄位時先確認 byte 與 bit 編號。", "NVMe expresses field locations in bytes, words, and dwords. A word is two bytes and a dword is four bytes; field decoding starts by confirming byte and bit numbering."),
            c("QUEUE", "2.1", "21-23", "PCIe memory-based model 把 Submission Queue 與 Completion Queue 配置在記憶體。多個 I/O Submission Queues 可共用一個 I/O Completion Queue；Admin queue pair 維持一對一。", "In the PCIe memory-based model, Submission and Completion Queues reside in memory. Multiple I/O Submission Queues may share an I/O Completion Queue, while the Admin queue pair remains one-to-one."),
            c("STORAGE", "2.3.1", "26-33", "儲存模型用 NVM subsystem、domain、Endurance Group、NVM Set／Reclaim Group、Reclaim Unit 與 namespace 表達包含關係。namespace 是 host 實際透過 controller 存取的格式化容量。", "The storage model expresses containment through the NVM subsystem, domain, Endurance Group, NVM Set or Reclaim Group, Reclaim Unit, and namespace. A namespace is the formatted capacity a host accesses through a controller."),
            c("COMMANDSET", "2.3.2", "33", "Admin Command Set 管理 controller 與 queue；I/O Command Set 定義對 namespace 的資料操作。Base 說明通用機制，個別 I/O Command Set Specification 說明命令語意。", "The Admin Command Set manages controllers and queues; an I/O Command Set defines data operations on namespaces. Base describes common mechanisms, while each I/O Command Set Specification describes command semantics."),
            c("SUBSYSTEM", "2.3.3", "33-35", "controller、port、namespace 與 PCI Function 是不同物件；NSID 是 controller 用來指向 namespace 的 handle，不是 namespace 本身。", "Controllers, ports, namespaces, and PCI Functions are distinct objects. An NSID is a controller-visible handle for a namespace, not the namespace itself."),
            c("MULTIPATH", "2.4.1", "35-37", "multi-path I/O 是同一 host 到同一 namespace 的兩條以上獨立路徑；namespace sharing 是兩個以上 host 經不同 controller 存取同一 shared namespace。兩者都需要至少兩個 controller。", "Multi-path I/O provides two or more independent paths from one host to one namespace; namespace sharing lets two or more hosts access one shared namespace through different controllers. Both require at least two controllers."),
            c("ASYMMETRY", "2.4.2", "37", "支援多路徑或共享時，各 controller 對同一 namespace 的存取特性不一定相同；host 可依 controller 所回報的狀態選擇路徑。", "With multi-path or sharing, controllers need not provide identical access characteristics to the same namespace; the host may select paths using the state reported by each controller.", "may"),
        ],
    },
    "base-ch3": {
        "prefix": "BASE3",
        "title_zh": "NVMe Base 2.4 第 3 章：Controller、Queue、初始化與重設",
        "title_en": "NVMe Base 2.4 Chapter 3: Controllers, Queues, Initialization, and Resets",
        "source_id": "NVME-BASE-2.4",
        "scope_entry": "BASE3-INCLUDE",
        "range": "§3；文件頁 38-138；PDF 頁 64-164",
        "range_en": "§3; printed pages 38-138; PDF pages 64-164",
        "diagram": ["Properties / CAP", "CC.EN = 1", "CSTS.RDY = 1", "Queues active"],
        "diagram_note_zh": "host 先讀能力與設定 Admin queues，再啟用 controller；只有 CSTS.RDY 回報 ready 後才進入正常 queue processing。",
        "diagram_note_en": "The host reads capabilities and configures Admin queues before enabling the controller; normal queue processing starts only after CSTS.RDY reports ready.",
        "claims": [
            c("STATIC", "3.1.1", "38", "memory-based controller 必須（shall）只支援 static controller model。", "A memory-based controller shall support only the static controller model.", "shall"),
            c("TYPES", "3.1.3-3.1.3.2", "39-43", "本輪只使用 I/O controller 與 Administrative controller：前者可執行使用者資料的 I/O，後者以管理為目的且不支援資料 I/O command。兩者都具有一組 Admin Submission／Completion Queue。", "This report uses the I/O and Administrative controller roles. The former performs user-data I/O; the latter is management-oriented and does not support data I/O commands. Both have one Admin Submission/Completion Queue pair."),
            c("ORDER", "3.1.3", "40", "除 fused operation 外，controller 取走的命令與完成沒有一般性的先後保證；若有順序需求，強制該順序是 host 的責任。", "Except for fused operations, fetched commands and completions have no general ordering guarantee. Enforcing any required order is the host's responsibility."),
            c("PROPERTY", "3.1.4", "52-54", "host 必須（shall）以 property 指定的寬度，從 property 起始 offset 存取；memory-based controller 的實際存取規則由 PCIe Transport 補充。", "The host shall access a property at its starting offset using the specified width; the PCIe Transport adds the access rules for a memory-based controller.", "shall"),
            c("NAMESPACE", "3.2.1", "78-80", "NSID 0h 無效，FFFFFFFFh 是 broadcast 值；其餘 NSID 還要區分 allocated／unallocated 與 active／inactive，不能只看數字是否落在範圍內。", "NSID 0h is invalid and FFFFFFFFh is the broadcast value. Other NSIDs still need allocated/unallocated and active/inactive classification; numeric range alone is insufficient."),
            c("MEDIA", "3.2.2-3.2.4", "80-85", "NVM Set、Endurance Group、Reclaim Group 與 Reclaim Unit 分別描述容量集合、耐久度管理與回收粒度。是否支援及其 identifier 由 Identify／log page 能力判定。", "NVM Sets, Endurance Groups, Reclaim Groups, and Reclaim Units describe capacity grouping, endurance management, and reclamation granularity. Support and identifiers are determined from Identify data and log-page capabilities."),
            c("DOMAIN", "3.2.5", "85-88", "domain 是 NVM subsystem 內的故障／通訊邊界。多 domain subsystem 的 identifier 必須（shall）在該 subsystem 內唯一。", "A domain is a failure or communication boundary inside an NVM subsystem. In a multi-domain subsystem, each domain identifier shall be unique within that subsystem.", "shall"),
            c("QUEUE", "3.3.1", "88-91", "PCIe queue 由 host-addressable memory 中的環形 buffer、head 與 tail pointer 構成。host 建立 I/O Completion Queue 後再建立對應 Submission Queue，並以 doorbell 推進 pointer。", "A PCIe queue is a circular buffer in host-addressable memory with head and tail pointers. The host creates an I/O Completion Queue before its Submission Queue and advances pointers through doorbells."),
            c("PROCESS", "3.4.1-3.4.5", "101-105", "command processing 要分開看 ordering、fused／atomic semantics、arbitration 與 outstanding command 上限；priority 屬於 Submission Queue，不是每一筆 command 的獨立欄位。", "Command processing separates ordering, fused and atomic semantics, arbitration, and outstanding-command limits. Priority belongs to a Submission Queue, not to each command as an independent attribute."),
            c("INIT", "3.5.1, 3.5.3-3.5.4", "105-113", "PCIe 初始化以 CAP 判斷能力與 timeout，設定 AQA／ASQ／ACQ 與 CC，接著等待 CSTS.RDY。ready mode 與 CRTO 會影響 host 等待與錯誤處理。", "PCIe initialization reads CAP, configures AQA/ASQ/ACQ and CC, then waits for CSTS.RDY. Ready mode and CRTO affect host wait and error handling."),
            c("SHUTDOWN", "3.6.1, 3.6.3", "113-120", "正常 shutdown 由 host 設定 CC.SHN，controller 透過 CSTS.SHST 回報進度；NVM subsystem shutdown 是更大範圍的處理，不能與單一 controller shutdown 混為一談。", "Normal shutdown begins when the host sets CC.SHN and the controller reports progress in CSTS.SHST. NVM subsystem shutdown has a wider scope and is not the same as one controller shutdown."),
            c("RESET", "3.7", "120-125", "NVM Subsystem Reset、Controller Level Reset 與 Queue Level Reset 的影響範圍不同；設計 recovery flow 前先確認哪一層狀態會被清除、queue 是否仍存在。", "NVM Subsystem, Controller Level, and Queue Level resets have different scopes. A recovery flow first determines which state is cleared and whether queues still exist."),
            c("CAPACITY", "3.8", "125-129", "capacity model 分開追蹤 NVM subsystem、Endurance Group、NVM Set 與 namespace 的可用或配置容量；同一數值不可跨層級直接比較。", "The capacity model tracks available or configured capacity separately at subsystem, Endurance Group, NVM Set, and namespace levels. Values from different levels are not directly interchangeable."),
            c("KEEPALIVE", "3.9", "129-135", "Keep Alive 以 KATO／KATT 建立 host 與 controller 的存活監測；本報告只保留 controller 共通與 PCIe 可用的 timer、command 與 timeout 行為。", "Keep Alive uses KATO and KATT for host/controller liveness monitoring. This report retains only controller-common and PCIe-applicable timer, command, and timeout behavior."),
            c("FIRMWARE", "3.10-3.11", "135-138", "privileged action 會影響其他 host 或 controller；firmware update 分成 image download、commit／activate 與可能的 reset，host 依回報的 activation action 安排流程。", "A privileged action may affect other hosts or controllers. Firmware update separates image download, commit/activation, and any required reset; the host sequences the flow using the reported activation action."),
        ],
    },
    "base-ch4": {
        "prefix": "BASE4",
        "title_zh": "NVMe Base 2.4 第 4 章：SQE、CQE、Status、PRP 與 SGL",
        "title_en": "NVMe Base 2.4 Chapter 4: SQE, CQE, Status, PRP, and SGL",
        "source_id": "NVME-BASE-2.4",
        "scope_entry": "BASE4-INCLUDE",
        "range": "§4；文件頁 139-175；PDF 頁 165-201",
        "range_en": "§4; printed pages 139-175; PDF pages 165-201",
        "diagram": ["64-byte SQE", "PRP or SGL", "Command execution", "16-byte+ CQE"],
        "diagram_note_zh": "SQE 以 CID 與 SQID 識別 command，data pointer 描述 buffer；CQE 回報 SQ head、SQID、CID、phase 與 status。",
        "diagram_note_en": "The SQE identifies a command with CID plus SQID and describes buffers through data pointers; the CQE reports SQ head, SQID, CID, phase, and status.",
        "claims": [
            c("SQE", "4.1.1", "139-143", "Admin 與 I/O common SQE 固定為 64 bytes。CDW0、NSID、data pointer 與 CDW10-15 的通用位置先固定，再由各 command 定義命令專屬內容。", "The common Admin and I/O SQE is 64 bytes. CDW0, NSID, data pointers, and CDW10-15 establish the common layout before each command defines command-specific content."),
            c("CID", "4.1.1", "140", "CID 與 Submission Queue identifier 的組合用來唯一識別 command；FFFFh 宜（should）避免使用，因 Error Information log 以該值表示錯誤未對應特定 command。", "CID in combination with the Submission Queue identifier uniquely identifies a command. FFFFh should be avoided because the Error Information log uses it when an error is not associated with a particular command.", "should"),
            c("PSDT", "4.1.1", "140-142", "CDW0.PSDT 決定 DPTR 解讀為 PRP 或 SGL。NVMe over PCIe 的 Admin command 原則上必須（shall）使用 PRP，除非 command 定義另有規定。", "CDW0.PSDT selects PRP or SGL interpretation for DPTR. An Admin command over PCIe shall use PRPs unless its command definition specifies otherwise.", "shall"),
            c("CQE", "4.2.1", "144-145", "common CQE 至少 16 bytes；若以多次寫入建立 CQE，Phase Tag 必須（shall）在最後一次寫入更新，避免 host 看到半成品。", "The common CQE is at least 16 bytes. If multiple writes construct it, the Phase Tag shall be updated in the last write so the host does not consume a partial entry.", "shall"),
            c("STATUS", "4.2.3", "145-155", "status 要先解 Status Code Type（SCT），再解 Status Code（SC），同時檢查 Do Not Retry（DNR）等控制 bit；數值不能脫離 SCT 單獨解讀。", "Status decoding starts with Status Code Type (SCT), then Status Code (SC), together with control bits such as Do Not Retry (DNR). An SC value is not interpreted without its SCT."),
            c("PHASE", "4.2.4", "155-158", "Phase Tag 讓 host 判斷環形 Completion Queue slot 是否為新完成項目；host 消費 CQE 後推進 CQ head doorbell，wrap 時預期 phase 翻轉。", "The Phase Tag lets the host distinguish a new entry in a circular Completion Queue. After consuming CQEs, the host advances the CQ head doorbell and expects phase inversion on wrap."),
            c("PRP", "4.3.1", "158-159", "PRP 以固定大小 entry 指向 physical memory page。第一個 entry 可含 page offset；後續 PRP 必須（shall）符合 page alignment，資料長度決定需要幾個 entry。", "A fixed-size PRP entry points to a physical memory page. The first entry may contain a page offset; subsequent PRPs shall obey page alignment, and transfer length determines the required entry count.", "shall"),
            c("SGL", "4.3.2", "159-166", "SGL 由一個以上 descriptor／segment 描述資料 buffer。SGL length 必須（shall）大於等於 requested transfer length；本報告只介紹 PCIe 可用的通用 descriptor。", "An SGL describes a data buffer through one or more descriptors and segments. SGL length shall equal or exceed the requested transfer length; this report covers only generic descriptors applicable to PCIe.", "shall"),
            c("FEATURE", "4.4", "166-169", "Feature 可能具有 default、saved、current value；saved value 支援與跨 reset／power cycle 的 persistence 由 SSFS 與各 Feature capability 判定。", "A Feature may have default, saved, and current values. Saved-value support and persistence across resets or power cycles are determined from SSFS and each Feature capability."),
            c("IDENTIFIER", "4.5", "169-172", "VID／SSVID、SN／MN、IEEE OUI、EUI64、NGUID 與 UUID 的來源、長度與唯一性範圍不同；不能只因外觀相似就互換。此節為 informative。", "VID/SSVID, SN/MN, IEEE OUI, EUI64, NGUID, and UUID differ in origin, length, and uniqueness scope and are not interchangeable. This section is informative."),
            c("LISTS", "4.6", "172-173", "Controller List 與 Namespace List 都先給出數量，再排列 identifier；實作 parser 時，先依格式定義的上限與保留區驗證輸入。", "Controller and Namespace Lists provide a count followed by identifiers. A parser first validates the count, defined limit, and reserved area before consuming entries."),
            c("UTF8", "4.8", "175", "處理 UTF-8 輸入時要依規格流程驗證編碼、禁止的 code point 與截斷情況；不可把任意 byte sequence 當成有效字串。", "UTF-8 input processing validates encoding, prohibited code points, and truncation using the specified flow; an arbitrary byte sequence is not automatically a valid string."),
        ],
    },
    "base-admin-fw-logs": {
        "prefix": "BASEFWLOG",
        "title_zh": "NVMe Base 2.4：Firmware Update 與 LID 03h 驗證",
        "title_en": "NVMe Base 2.4: Firmware Update and LID 03h Verification",
        "source_id": "NVME-BASE-2.4",
        "scope_entry": "BASE-FWLOG-INCLUDE",
        "date": "2026-09-01",
        "verified_date": "2026-09-01",
        "range": "§3.11、§3.11.1、§5.2.9、§5.2.10、§5.2.13 的 LID 03h 必要共通欄位、§5.2.13.1.4；主範圍文件頁 135-138、202-206、212-216、225-226，並含最小 dependency slice",
        "range_en": "§3.11, §3.11.1, §5.2.9, §5.2.10, the minimum common §5.2.13 fields needed for LID 03h, and §5.2.13.1.4; main printed pages 135-138, 202-206, 212-216, and 225-226, plus the minimum dependency slice",
        "diagram": ["Image Download", "Firmware Commit", "Activate / Reset", "Get Log Page"],
        "diagram_note_zh": "host 以 OFST／NUMD 傳送 image portions，Firmware Commit 驗證並決定 slot／activation action；需要時完成 reset 與重新初始化，再用 LID 03h 比對目前與下一個 active slot。",
        "diagram_note_en": "The host transfers image portions with OFST and NUMD, Firmware Commit validates them and selects a slot and activation action, and LID 03h then verifies the current and next active slots after any required reset and reinitialization.",
        "claims": [
            c("MODEL-DOMAIN", "5.2.9", "202", "同一 domain 內的 controllers 共用 firmware slots，且相同 firmware image 會套用到該 domain 的所有 controllers；若不支援 multiple domains，範圍就是整個 NVM subsystem。", "Controllers in one domain share firmware slots, and the same firmware image is applied to all controllers in that domain. If multiple domains are not supported, that scope is the entire NVM subsystem."),
            c("FW-RESET", "3.11", "135-136", "需要 reset 的標準流程是：一筆以上 Firmware Image Download、Firmware Commit 驗證並放入 slot、執行能觸發該 activation 的 Controller Level Reset，然後重新初始化 controller 與 I/O queues。", "The reset-based flow is one or more Firmware Image Download commands, Firmware Commit to validate and place the image, a Controller Level Reset capable of causing activation, and reinitialization of the controller and I/O queues."),
            c("FW-IMMEDIATE", "3.11", "136", "CA=011b 要求立即 activation。Firmware Commit 不是 background operation，會保持進行中直到 activation 成功或失敗；若 Firmware Activation notice 已啟用，受影響 controller 可（may）送出 Firmware Activation Starting event。", "CA=011b requests immediate activation. Firmware Commit is not a background operation and remains in progress until activation succeeds or fails. If Firmware Activation notices are enabled, an affected controller may send Firmware Activation Starting.", "may"),
            c("FW-FAILURE", "3.11", "136-137", "若新 image 無法成功載入，controller 必須（shall）回復到最近 activation 的 slot image；若該 image 也無法載入，則載入可用的 baseline read-only image，並產生 Firmware Image Load Error event。", "If the new image cannot be loaded, the controller shall revert to the image in the most recently activated slot; if that image also cannot be loaded, it loads an available baseline read-only image and generates Firmware Image Load Error.", "shall"),
            c("FW-SEQUENCE", "3.11", "137", "host 不宜（should not）讓 firmware／Boot Partition update sequences 重疊，且同一 sequence 宜（should）只使用一個 controller 或 Management Endpoint。", "The host should not overlap firmware or Boot Partition update sequences and should use only one controller or Management Endpoint throughout a sequence.", "should"),
            c("FW-DISCARD", "3.11, 5.2.10", "137, 205-206", "Firmware Commit 完成後的第一筆新 Firmware Image Download，以及 download 後、Firmware Commit 完成前發生的 Controller Level Reset，都必須（shall）使 controller 丟棄尚存的已下載 portions。", "The first Firmware Image Download after Firmware Commit completes, and a Controller Level Reset after download but before Firmware Commit completion, shall cause the controller to discard remaining downloaded portions.", "shall"),
            c("UUID-LIST", "3.11.1", "137-138", "firmware revisions 間的 UUID List 宜（should）保持 entry 位置穩定：新增 UUID 宜接在尾端；移除時宜原位改成 NVMe Invalid UUID；不宜重用 invalid entry，也不宜縮短或移除清單。", "Across firmware revisions, UUID List entry positions should remain stable: new UUIDs should be appended, a removed UUID should be replaced in place with the NVMe Invalid UUID, an invalid entry should not be reused, and the list should not be shortened or removed.", "should"),
            c("UUID-RESET", "3.11.1", "138", "若 downloaded image 在既有 entry 中，以有效 UUID 取代 NVMe Invalid UUID 或另一個有效 UUID，controller 必須（shall）要求 reset；所有受這個 UUID List 變更影響的 controllers 都必須（shall）reset。", "If a downloaded image replaces the NVMe Invalid UUID or a different valid UUID with a valid UUID in an existing entry, the controller shall require reset, and all controllers affected by that UUID List change shall be reset.", "shall"),
            c("CAP-FR", "5.2.14.1", "340", "Identify Controller 的 FR 是目前 active firmware revision 的 8-byte ASCII string，scope 是 controller 所屬 domain；它與 LID 03h 回報的目前 revision 資訊相同。", "Identify Controller FR is the eight-byte ASCII string for the currently active firmware revision in the controller's domain. It is the same revision information available from LID 03h."),
            c("CAP-MDS-ULIST", "5.2.14.1", "346, 364", "CTRATT.MDS 判斷 LID 03h 回傳 domain scope 還是整個 NVM subsystem scope；CTRATT.ULIST 判斷 controller 是否支援 UUID List reporting。MDS=1 時 DID 必須（shall）非零；single-domain subsystem 的 DID 必須（shall）為 0h。", "CTRATT.MDS determines whether LID 03h returns domain-scoped or NVM-subsystem-scoped information, while CTRATT.ULIST indicates UUID List reporting support. With MDS=1, DID shall be nonzero; in a single-domain subsystem, DID shall be 0h.", "shall"),
            c("CAP-FRMW", "5.2.14.1", "354", "FRMW 的 SMUD、FAWR、NOFS 與 FFSRO 分別表示重疊 update 偵測、免 reset activation、domain 支援的 slot 數（1 到 7）以及 slot 1 是否 read-only。", "FRMW.SMUD, FAWR, NOFS, and FFSRO describe overlapping-update detection, activation without reset, the domain's supported slot count (1 through 7), and whether slot 1 is read-only."),
            c("CAP-MTFA", "5.2.14.1", "357", "MTFA 以 100 ms 為單位，表示 activation 時 controller 暫停處理 commands 的最長時間；支援免 reset activation 時此欄位必須（shall）有效，0h 表示最大時間未定義。", "MTFA is in 100 ms units and reports the maximum time command processing is temporarily stopped during activation. It shall be valid when activation without reset is supported; 0h means the maximum is undefined.", "shall"),
            c("CAP-FWUG", "5.2.14.1", "359", "FWUG 以 4 KiB 為單位限制 NUMD 與 OFST 的 granularity／alignment：1h=4 KiB、2h=8 KiB、0h=未提供資訊、FFh=可用任何 dword granularity 與 alignment。違反時 controller 可（may）回 Invalid Field in Command。", "FWUG constrains NUMD and OFST granularity/alignment in 4 KiB units: 1h is 4 KiB, 2h is 8 KiB, 0h reports no information, and FFh permits any dword granularity and alignment. A controller may return Invalid Field in Command for a violation.", "may"),
            c("CAP-MPTFAWR", "5.2.14.1", "364", "MPTFAWR 以 100 ms 為單位，估算 CA=011b 的 Firmware Commit 從處理到完成所需最大時間，且包含把 image commit 到 slot 的時間；不支援免 reset activation 時必須（shall）為 0h。", "MPTFAWR is a 100 ms-unit estimate of the maximum processing time to complete Firmware Commit with CA=011b, including time to commit the image to a slot. It shall be 0h when activation without reset is unsupported.", "shall"),
            c("COMMIT-PURPOSE", "5.2.9", "202-203", "Firmware Commit 驗證最後下載的 image、把它放入 firmware slot，並依 Commit Action 決定只放置、在後續 Controller Level Reset activation，或立即 activation。成功 commit 不等於當下已 active。", "Firmware Commit validates the last downloaded image, places it in a firmware slot, and uses Commit Action to choose placement only, activation at a later Controller Level Reset, or immediate activation. Successful commit does not by itself mean the image is currently active."),
            c("COMMIT-CDW10", "5.2.9", "203", "CDW10[5:3] 是 CA，CDW10[2:0] 是 FS。CA 000b 只放置；001b 放置並排定下次 CLR activation；010b 排定既有 slot；011b 立即 activation。FS=0h 時 controller 必須（shall）在 slot 1 到 7 中選一個。", "CDW10[5:3] is CA and CDW10[2:0] is FS. CA 000b places only, 001b places and schedules activation at the next CLR, 010b schedules an existing slot, and 011b activates immediately. With FS=0h, the controller shall choose a slot from 1 through 7.", "shall"),
            c("COMMIT-BOOT", "5.2.9", "203-205", "BPID 與 CA=110b／111b 屬於 Boot Partition：110b 取代指定 partition，111b 將它標成 active；Boot Partition Write Prohibited 是 Firmware Commit 的 command-specific status 之一。", "BPID and CA=110b/111b belong to Boot Partition handling: 110b replaces the selected partition, 111b marks it active, and Boot Partition Write Prohibited is one of the Firmware Commit command-specific status values."),
            c("COMMIT-MUD", "5.2.9", "204", "Firmware Commit CQE.DW0[1:0] 的 MUD 分別回報 Management Endpoint 與 Admin Submission Queue 偵測到的 overlap。若 FRMW.SMUD=0，MUD 必須（shall）為 00b；MUD 在 command 成功或 aborted 時都有效。", "Firmware Commit CQE.DW0[1:0] MUD reports overlap detected through a Management Endpoint and an Admin Submission Queue. If FRMW.SMUD is 0, MUD shall be 00b; MUD is valid whether the command succeeds or is aborted.", "shall"),
            c("COMMIT-STATUS", "5.2.9", "204-205", "Firmware Commit 的 command-specific status 區分 invalid slot／image、需要 Conventional／NVM Subsystem／Controller Level Reset、MTFA violation、activation prohibited、overlapping range、Boot Partition write prohibited 與 personality incompatibility。", "Firmware Commit command-specific status distinguishes invalid slot/image, required Conventional/NVM Subsystem/Controller Level Reset, MTFA violation, activation prohibited, overlapping range, Boot Partition write prohibition, and personality incompatibility."),
            c("DOWNLOAD-RANGE", "5.2.10", "205-206", "Firmware Image Download 可分成多個 portions，firmware image portions 可不依序送達；host 宜（should）避免 ranges 重疊並符合 FWUG。Boot Partition portions 則必須（shall）依序提交。", "Firmware Image Download may split an image into portions, and firmware-image portions may arrive out of order. The host should avoid overlapping ranges and comply with FWUG. Boot Partition portions shall be submitted in order.", "shall"),
            c("DOWNLOAD-FIELDS", "4.1.1, 5.2.10", "140-142, 205-206", "NVMe over PCIe 的 Admin command 不得使用 SGL，因此 DPTR 以 PRP 指向本次來源 buffer；NUMD 是 0's-based dword count，所以 bytes=(NUMD+1)×4；OFST 是距 image 起點的 dword offset，所以 byte offset=OFST×4。包含 image 起點的 portion 必須（shall）令 OFST=0h。", "An Admin command over NVMe over PCIe shall not use SGL, so DPTR uses PRPs to identify the source buffer. NUMD is a zero-based dword count, so bytes=(NUMD+1)×4; OFST is a dword offset from the image start, so byte offset=OFST×4. The portion containing the image start shall use OFST=0h.", "shall"),
            c("LOG-COMMAND", "4.1.1, 5.2.13", "140-142, 212-215", "讀 LID 03h 時，未使用 namespace，因此 NSID 必須（shall）為 0h；DPTR 以 PRP 指向 512-byte destination buffer。必要的 CDW10-CDW14 slice 為 LID=03h、LSP=0、RAE=0、NUMDL/NUMDU 表示 512 bytes、LSI=0、LPOL/LPOU=0、OT=0、UIDX=0；CSI 對 LID 03h 不使用，controller 依 Figure 208 規則忽略。", "When reading LID 03h, no namespace is used, so NSID shall be 0h, and DPTR uses PRPs to identify the 512-byte destination buffer. The required CDW10-CDW14 slice is LID=03h, LSP=0, RAE=0, NUMDL/NUMDU for 512 bytes, LSI=0, LPOL/LPOU=0, OT=0, and UIDX=0. LID 03h does not use CSI, which the controller ignores under Figure 208's rule.", "shall"),
            c("LOG-LENGTH", "5.2.13", "213-215", "NUMDL 與 NUMDU 合成 0's-based dword count。LID 03h 固定 512 bytes=128 dwords，因此 NUMD=127=0000007Fh，NUMDL=007Fh、NUMDU=0000h；在 LSP=0、RAE=0 下，CDW10=007F0003h。", "NUMDL and NUMDU form a zero-based dword count. LID 03h is 512 bytes, or 128 dwords, so NUMD=127=0000007Fh, NUMDL=007Fh, and NUMDU=0000h. With LSP=0 and RAE=0, CDW10=007F0003h."),
            c("LOG-RAE", "5.2.2, 5.2.13", "186, 213", "RAE=0 會在 command 成功時清除對應 asynchronous event，RAE=1 則保留；若 command 未成功，controller 必須（shall）保留 event。Firmware Activation Starting event 要以 RAE=0 讀取 LID 03h 才會清除。", "RAE=0 clears the corresponding asynchronous event on successful completion, while RAE=1 retains it. If the command fails, the controller shall retain the event. Firmware Activation Starting is cleared by reading LID 03h with RAE=0.", "shall"),
            c("LOG-OFFSET", "5.2.13", "214-215", "本報告以完整 512-byte LID 03h、LPOL=LPOU=0、OT=0 為基準。一般 byte offset 必須 dword aligned；超過 log page 大小的 offset 必須（shall）回 Invalid Field in Command。LID 03h 不需要 index-offset 分支。", "This report uses the complete 512-byte LID 03h with LPOL=LPOU=0 and OT=0. A general byte offset is dword aligned, and an offset beyond the log page shall return Invalid Field in Command. LID 03h needs no index-offset branch.", "shall"),
            c("LOG-SCOPE", "5.2.13", "215-216", "Figure 209 的 LID 03h row 指定 CSI=N、scope=Domain／NVM subsystem、reference=§5.2.13.1.4。MDS=1 時回傳處理 command 之 controller 所屬 domain；否則回傳整個 NVM subsystem 的資訊。", "The LID 03h row in Figure 209 specifies CSI=N, scope=Domain/NVM subsystem, and reference §5.2.13.1.4. With MDS=1, the data is for the domain containing the controller that processed the command; otherwise it is for the NVM subsystem."),
            c("LID03-DESCRIPTION", "5.2.13.1.4", "225-226", "Firmware Slot Information log page 固定 512 bytes，說明每個支援 slot 內的 firmware revision，並指出 current active slot 與（若 controller 有回報）next active slot。revision 以 ASCII string 表示。", "The 512-byte Firmware Slot Information log page reports the firmware revision stored in each supported slot and identifies the current active slot plus the next active slot when reported. Revisions are ASCII strings."),
            c("LID03-AFI", "5.2.13.1.4", "226", "byte 0 的 AFI 中，NAFS=bits 6:4、CAFS=bits 2:0；bits 7 與 3 reserved。NAFS 非零表示將於下一次能觸發 activation 的 CLR 啟用該 slot，NAFS=0 表示 controller 未指出 next slot；CAFS 是目前執行 image 的來源 slot。", "In AFI byte 0, NAFS is bits 6:4 and CAFS is bits 2:0; bits 7 and 3 are reserved. Nonzero NAFS identifies the slot to activate at the next CLR capable of causing activation; NAFS=0 means no next slot is indicated. CAFS identifies the source slot of the running image."),
            c("LID03-FRS", "5.2.13.1.4", "226", "FRS1 到 FRS7 位於 bytes 8-63，每格 8 bytes；slot 沒有有效 revision 或不支援時，該 FRS 必須（shall）清為 0h。bytes 1-7 與 64-511 reserved。", "FRS1 through FRS7 occupy bytes 8-63, eight bytes per slot. If a slot has no valid revision or is unsupported, its FRS shall be cleared to 0h. Bytes 1-7 and 64-511 are reserved.", "shall"),
            c("RESET-XREF", "3.3", "11", "NVMe over PCIe Transport 將 Conventional Reset 與 Function Level Reset 分別列為額外的 transport-specific Controller Level Reset 方法；除 Controller Reset 外，Controller Level Reset 會依 PCI Express Base Specification 重設 PCI register space。", "NVMe over PCIe Transport lists Conventional Reset and Function Level Reset as distinct additional transport-specific Controller Level Reset methods. Except for Controller Reset, Controller Level Reset resets PCI register space as defined by the PCI Express Base Specification.", "none", "NVME-PCIE-TRANSPORT-1.4", "BASE-FWLOG-PCIE-RESET-PREREQUISITE"),
            c("XREF-337", "5.2.9, 5.2.14.1", "202, 340", "來源 §5.2.9 將 Firmware Revision 欄位指向 Figure 337；但 Figure 337 是 Command Set Identifiers，FR 實際列在 Figure 338。未取得另行核准的 errata，因此保留並揭露這個來源內部交叉引用差異，不靜默改寫。", "Source §5.2.9 points Firmware Revision to Figure 337, but Figure 337 contains Command Set Identifiers and FR appears in Figure 338. Without separately approved errata, this report preserves and discloses the internal source discrepancy instead of silently rewriting it."),
        ],
    },
    "base-power-features": {
        "prefix": "BASEPOWER",
        "title_zh": "NVMe Base 2.4：Power／Thermal Features 與 Power Management",
        "title_en": "NVMe Base 2.4: Power/Thermal Features and Power Management",
        "source_id": "NVME-BASE-2.4",
        "scope_entry": "BASE-POWER-INCLUDE",
        "date": "2026-09-02",
        "verified_date": "2026-09-02",
        "range": "§5.2.12、§5.2.30 共通命令、FID 02h／04h／0Ch／10h／11h，以及 §8.1.19～§8.1.19.5；含五張最小 dependency Figure，排除 Power Limit、IIELL、其他 FID 與傳輸專屬內容",
        "range_en": "§5.2.12, the common §5.2.30 command, FIDs 02h/04h/0Ch/10h/11h, and §8.1.19 through §8.1.19.5; includes five minimum dependency Figures and excludes Power Limit, IIELL, other FIDs, and transport-specific material",
        "diagram": ["Get capability / value", "Choose host policy", "Set one Feature", "Observe completion / temperature"],
        "diagram_note_zh": "先用 Get Features 區分支援能力與目前值，再依 Power State Descriptor、溫度能力與工作負載選 policy；Set Features 成功後，以 completion、SMART/Health 與實際 latency／temperature 形成驗證閉環。",
        "diagram_note_en": "First use Get Features to separate capability from current value. Choose policy from Power State Descriptors, thermal capabilities, and workload; after Set Features succeeds, close the loop with completion evidence, SMART/Health, and observed latency/temperature.",
        "claims": [
            c("READ-FIRST", "5.2.12", "209", "Get Features 是讀取 Feature 屬性的 Admin command。工程流程不應從寫入猜測開始，而要先辨認 FID、查 capability，再取得 current／default／saved value。", "Get Features is the Admin command that retrieves Feature attributes. An engineering flow starts by identifying the FID, querying capability, and retrieving current/default/saved values instead of guessing before a write."),
            c("GET-SELECT", "5.2.12", "209-210", "CDW10.SEL 選擇 current=000b、default=001b、saved=010b 或 supported capabilities=011b；CDW10.FID 選 Feature。其餘 SEL encoding reserved。", "CDW10.SEL selects current=000b, default=001b, saved=010b, or supported capabilities=011b; CDW10.FID selects the Feature. Other SEL encodings are reserved.", "reserved"),
            c("GET-SAVED", "5.2.12", "210", "若要求 saved value，但 controller 不支援 saved value 或尚無 saved value，controller 會以 default value 運作。這不是『讀取成功就代表曾經儲存』。", "If a saved value is requested but saved values are unsupported or none exists, the controller operates using the default value. A successful read therefore does not prove that a value was previously saved."),
            c("GET-UIDX", "5.2.12", "210", "CDW14.UIDX 只有在 controller 支援 UUID List 且該 Feature 需要 UUID 關聯時才有意義；未使用時保留為 0。", "CDW14.UIDX is meaningful only when the controller supports the UUID List and the Feature uses a UUID association; otherwise it remains zero."),
            c("GET-CAP", "5.2.12.1", "211-212", "SEL=011b 時，CQE.DW0 以 CHANG、NSSPEC、SVBL 回報是否可變更、是否 namespace-specific、是否可 save。這三個 capability bits 與 Feature value 是兩種不同資料，不能混解。", "With SEL=011b, CQE.DW0 reports CHANG, NSSPEC, and SVBL: changeable, namespace-specific, and saveable. These capability bits are distinct from the Feature value and must not be decoded as one."),
            c("GET-STATUS", "5.2.12.2", "212", "若 Get Features 指定不適用的 Controller Identifier，command-specific status 1Fh 是 Invalid Controller Identifier。Debug 要同時保存 SCT、SC、DNR、CDW10、CDW14 與 target controller。", "If Get Features specifies an inapplicable Controller Identifier, command-specific status 1Fh is Invalid Controller Identifier. Debug evidence retains SCT, SC, DNR, CDW10, CDW14, and the target controller."),
            c("SET-DPTR", "5.2.30", "456-457", "Set Features 的 DPTR 只在所選 Feature 定義 data structure 時使用。以 PRP 指向 buffer 時，該 data buffer 不得跨越超過一個 memory page boundary，因 PRP2 不能在此指向 PRP List。", "Set Features uses DPTR only when the selected Feature defines a data structure. With PRPs, that data buffer shall not cross more than one memory-page boundary because PRP2 cannot point to a PRP List here.", "shall not"),
            c("SET-SAVE", "5.2.30", "457", "CDW10.SV=1 要求把值保存為跨 reset／power cycle 可用的 saved value；若 Feature 不可 save，controller 會回 Feature Identifier Not Saveable。先讀 SVBL，再決定是否設 SV。", "CDW10.SV=1 requests a saved value that can persist across reset/power-cycle boundaries. If the Feature is not saveable, the controller returns Feature Identifier Not Saveable. Read SVBL before setting SV."),
            c("SET-AFTER", "5.2.30", "459", "Set Features 成功後，後續 commands 必須（shall）使用新設定。若軟體需要讓一批 commands 一致套用舊值或新值，host 宜（should）先讓既有 in-flight commands 完成，再切換。", "After Set Features succeeds, subsequent commands shall use the new setting. If software needs a batch of commands to use one consistent setting, the host should allow existing in-flight commands to complete before switching.", "shall"),
            c("FID-SCOPE", "5.2.30", "457-459", "本報告五個 FID 的 scope 都是 Controller。FID 02h、04h、0Ch、11h 不支援 save；FID 10h 支援 save。只有 FID 0Ch 需要 256-byte data structure。", "All five FIDs in this report have Controller scope. FIDs 02h, 04h, 0Ch, and 11h are not saveable; FID 10h is saveable. Only FID 0Ch uses a 256-byte data structure."),
            c("POWER-STATES", "8.1.19", "666-667", "controller 必須（shall）至少支援一個 power state，最多可（may）支援 32 個，編號從 0 連續排列。PS0 的 maximum power 最高；後續 state 的 maximum power 不得高於前一個 state。", "A controller shall support at least one power state and may support up to 32, numbered contiguously from zero. PS0 has the highest maximum power; each subsequent state's maximum power does not exceed the preceding state.", "shall"),
            c("POWER-METRICS", "8.1.19", "666-668", "Power State Descriptor（PSD）把 maximum power、operational/non-operational、entry/exit latency、idle/active power 與 relative performance 放在同一份描述。MP 是 sustained maximum；IDLP 與 ACTP 是不同測量情境，不能拿單次瞬間功耗互相比。", "A Power State Descriptor (PSD) combines maximum power, operational/non-operational type, entry/exit latency, idle/active power, and relative performance. MP is a sustained maximum; IDLP and ACTP use different measurement conditions and are not interchangeable with an instantaneous sample."),
            c("TRANSITION", "8.1.19.1", "668-669", "從舊 state 直接切到新 state 的最大 transition time，是舊 state 的 EXLAT 加上新 state 的 ENLAT。若 controller 內部經過多個 state，則每一段 transition time 相加。", "The maximum direct-transition time from an old state to a new state is the old state's EXLAT plus the new state's ENLAT. If a controller transitions through multiple states, the transition times for every segment are summed."),
            c("RELATIVE", "8.1.19.2", "668", "Relative Read／Write Throughput 與 Latency 都是『值越小越好』，但只可在相同 characteristic 內比較；throughput code 不能與 latency code 混成一個總分。", "Relative Read/Write Throughput and Latency use smaller-is-better encodings, but comparisons are valid only within the same characteristic. A throughput code and a latency code are not combined into one score."),
            c("NONOP", "8.1.19", "667-668", "non-operational power state 不處理 I/O commands，但仍可能處理 property、PMR、CMB、Admin／background 或 transport-specific access。『non-operational』不是 controller 關機。", "A non-operational power state does not process I/O commands, but may still service properties, PMR, CMB, Admin/background work, or transport-specific accesses. Non-operational does not mean the controller is powered off.", "may"),
            c("NONOP-IO", "8.1.19", "668", "host 在手動切入 non-operational state 前宜（should）先 drain I/O。若 I/O command 到達，controller 會自主回到最近使用的 operational state，再處理 I/O。", "The host should drain I/O before manually entering a non-operational state. If an I/O command arrives, the controller autonomously returns to the most recently used operational state before processing I/O.", "should"),
            c("FID02", "5.2.30.1.2", "460-461", "FID 02h 用 CDW11.PS[4:0] 選 power state、WH[7:5] 提供 workload hint。指定的 PS 必須（shall）在 Identify Controller.NPSS 宣告範圍內；不支援的 PS 應（should）以 Invalid Field in Command 中止。", "FID 02h uses CDW11.PS[4:0] to select a power state and WH[7:5] for a workload hint. PS shall be within the range advertised by Identify Controller.NPSS; an unsupported PS should be aborted with Invalid Field in Command.", "shall"),
            c("WORKLOAD", "8.1.19.3", "669", "WH=000b 表示未知 workload；001b 對應先 idle、再做 32 筆 random 1 MiB writes、再 idle 的情境；010b 對應 80,000 筆 sequential 128 KiB writes。011b～111b reserved。", "WH=000b means unknown workload; 001b represents idle, 32 random 1-MiB writes, then idle; 010b represents 80,000 sequential 128-KiB writes. Encodings 011b through 111b are reserved.", "reserved"),
            c("RTD3", "8.1.19.4", "669-670", "RTD3E 與 RTD3R 分別描述進入與恢復時間，供 PCIe D3cold 使用情境評估 idle break-even；NVMe 文字明確說這不是 D3hot 的時間。PCIe D-state 的完整原始行為不在目前提供來源內，不能據此自行補寫。", "RTD3E and RTD3R describe entry and resume time for evaluating idle break-even in a PCIe D3cold use case; the NVMe text explicitly says these are not D3hot times. Complete PCIe D-state semantics are not present in the supplied source and are not invented here."),
            c("FID04", "5.2.30.1.3", "462-463", "FID 04h 可為 Composite Temperature 與最多八個實作的 temperature sensors 設 over／under threshold。溫度以 Kelvin 編碼；到達 over threshold 或低於等於 under threshold 時，SMART/Health 的 Temperature Threshold critical warning 可能觸發 asynchronous event。", "FID 04h sets over/under thresholds for Composite Temperature and up to eight implemented temperature sensors. Temperature is encoded in Kelvin; reaching an over threshold or falling to/below an under threshold may set the SMART/Health Temperature Threshold critical warning and trigger an asynchronous event.", "may"),
            c("HYST", "5.2.30.1.3.1", "463-464", "Figure 470 的 TMPSEL 選 sensor、THSEL 選 over/under、TMPTH 是 threshold、TMPTHH 是 hysteresis。over event 在溫度降到 threshold−hysteresis 時結束；under event在溫度升到 threshold+hysteresis 時結束。", "In Figure 470, TMPSEL selects a sensor, THSEL selects over/under, TMPTH is the threshold, and TMPTHH is hysteresis. An over event ends at threshold minus hysteresis; an under event ends at threshold plus hysteresis."),
            c("FID0C", "5.2.30.1.7", "468-469", "FID 0Ch 的 APSTE=1 啟用 Autonomous Power State Transition（APST）；預設值是 0。啟用只表示 controller 可依 APST table 的 idle timer 自主切換，並不保證一定進入任何特定 state。", "FID 0Ch APSTE=1 enables Autonomous Power State Transition (APST); the default is zero. Enabling it allows controller transitions based on APST-table idle timers; it does not guarantee entry into a particular state."),
            c("APST-ENTRY", "5.2.30.1.7", "469", "APST data structure 固定 256 bytes，共 32 個 8-byte entries。每格 ITPT[31:8] 是毫秒 idle threshold，ITPS[7:3] 是目標 non-operational state；ITPT=0 會停用該 entry。", "The APST data structure is 256 bytes with 32 eight-byte entries. Each entry uses ITPT[31:8] as the idle threshold in milliseconds and ITPS[7:3] as the target non-operational state; ITPT=0 disables that entry."),
            c("APST-NOPPME", "5.2.30.1.7", "469", "APSTE 控制 timer-based entry，NOPPME 控制 controller-initiated background operation 是否可暫時超過 non-operational limit。兩者是兩個正交開關：不要把『可自主進 state』誤解成『可為背景工作提高 power』。", "APSTE controls timer-based entry, while NOPPME controls whether controller-initiated background operations may temporarily exceed a non-operational limit. These are orthogonal switches; autonomous state entry does not imply permission to raise power for background work."),
            c("FID10", "5.2.30.1.10", "471-472", "FID 10h 的 TMT1[31:16] 是較輕度 thermal management threshold，TMT2[15:0] 是較重度 threshold，單位都是 Kelvin；0h 分別停用對應 threshold。", "FID 10h uses TMT1[31:16] as the lighter thermal-management threshold and TMT2[15:0] as the heavier threshold, both in Kelvin; zero independently disables the corresponding threshold."),
            c("HCTM", "5.2.30.1.10, 8.1.19.5", "472, 670-671", "非零 TMT1 必須（shall）小於 TMT2，且兩者必須落在 MNTMT～MXTMT 內；否則回 Invalid Field in Command。達 TMT1 時 controller 採降低影響的動作，達 TMT2 時採更強動作；hysteresis 由 vendor 決定。", "A nonzero TMT1 shall be less than TMT2, and both shall lie between MNTMT and MXTMT; otherwise the command returns Invalid Field in Command. At TMT1 the controller acts to minimize impact, while TMT2 invokes stronger action; hysteresis is vendor-specific.", "shall"),
            c("FID11", "5.2.30.1.11", "472-473", "FID 11h 的 NOPPME=1 允許 controller-initiated background operation 暫時把 power 提高到不超過最後一個 operational state 的上限；NOPPME=0 時，這類工作不得超過目前 non-operational state limits。", "FID 11h NOPPME=1 allows a controller-initiated background operation to raise power temporarily, no higher than the last operational state's limit. With NOPPME=0, such work shall not exceed the current non-operational-state limits.", "shall not"),
            c("OBSERVE", "5.2.13.1.3", "220-225", "設定完成不是驗證終點。SMART/Health 應同時觀察 Composite Temperature、TTC critical warning、warning temperature time、HCTM transition counters 與已實作 sensor readings，再對照 CQE 與 host latency。", "Successful configuration is not the end of verification. Observe SMART/Health Composite Temperature, the TTC critical warning, warning-temperature time, HCTM transition counters, and implemented sensor readings together with CQE and host latency."),
        ],
    },
    "base-self-test-hmb-emulation": {
        "prefix": "BASEDIAGMEM",
        "title_zh": "NVMe Base 2.4：Device Self-test、HMB、Doorbell Emulation 與 Vendor Commands",
        "title_en": "NVMe Base 2.4: Device Self-test, HMB, Doorbell Emulation, and Vendor Commands",
        "source_id": "NVME-BASE-2.4",
        "supporting_source_ids": ["NVME-NVM-CS-1.3"],
        "scope_entry": "BASE-DIAGMEM-INCLUDE",
        "date": "2026-09-02",
        "verified_date": "2026-09-02",
        "range": "Base §5.2.6、§5.2.13.1.7、§5.2.30.2.3、§8.1.8、§8.1.29、§8.2.3、§8.2.4，以及 NVM Command Set 1.3 §4.1.4.3；另含建構命令與能力判斷所需的最小 dependency slice",
        "range_en": "Base §§5.2.6, 5.2.13.1.7, 5.2.30.2.3, 8.1.8, 8.1.29, 8.2.3, and 8.2.4, plus NVM Command Set 1.3 §4.1.4.3; includes the minimum dependency slice needed to construct commands and gate capabilities",
        "diagram": ["Discover capability", "Construct command / memory", "Controller background work", "Read completion / log evidence"],
        "diagram_note_zh": "三條工程主線共享同一個原則：先確認 capability 與 ownership boundary，再提交 command 或 MMIO notification，最後用 CQE、log page 與記憶體生命週期證明結果。",
        "diagram_note_en": "Three engineering tracks share one rule: establish capability and ownership boundaries, submit the command or MMIO notification, then prove the result with CQEs, log pages, and memory-lifecycle evidence.",
        "claims": [
            c("SELFTEST-GATE", "5.2.14.2.1, 8.1.8", "352-358, 614", "啟動 Device Self-test 前，先讀 Identify Controller：OACS.DSTS 判斷 command 是否支援；EDSTT 是 extended operation 在 power state 0 的名目分鐘數；DSTO.SDSO 決定同時只能有一個 subsystem-wide operation，或每個 controller 各一個。這三個欄位回答不同問題。", "Before starting Device Self-test, read Identify Controller. OACS.DSTS gates command support, EDSTT gives the nominal extended-operation time in minutes at power state 0, and DSTO.SDSO selects one subsystem-wide operation versus one operation per controller. These fields answer different questions.", "none", "NVME-BASE-2.4", "BASE-DIAGMEM-DEPENDENCY-INCLUDE"),
            c("SELFTEST-NSID", "5.2.6", "199", "Device Self-test 由收到 command 的 controller 執行。NSID=00000000h 只測 controller；00000001h～FFFFFFFEh 指定一個 namespace；FFFFFFFFh 包含提交當下可由該 controller 存取的所有 attached namespaces。invalid 與 inactive NSID 會得到不同 status。", "Device Self-test is performed by the controller that receives the command. NSID 00000000h tests only the controller, 00000001h through FFFFFFFEh select one namespace, and FFFFFFFFh includes every attached namespace accessible through that controller when the operation starts. Invalid and inactive NSIDs produce different status results."),
            c("SELFTEST-STC", "5.2.6", "199-200", "CDW10.STC[3:0] 選動作：1h=short、2h=extended、3h=Host-Initiated Refresh、Eh=vendor specific、Fh=abort；其餘 encoding reserved。只有 STC=Eh 時 CDW15.DSTP 才是 vendor specific，其他情況 CDW15 reserved。", "CDW10.STC[3:0] selects the action: 1h short, 2h extended, 3h Host-Initiated Refresh, Eh vendor specific, and Fh abort; other encodings are reserved. CDW15.DSTP is vendor specific only when STC is Eh and is reserved otherwise.", "reserved"),
            c("SELFTEST-INPROGRESS", "5.2.6", "200", "已有 operation 時，再送 short、extended 或 Host-Initiated Refresh 必須以 Device Self-test in Progress 中止；vendor-specific 新命令的行為仍是 vendor specific。STC=Fh 則依序中止目前 operation、建立最新 result、清除 current status，最後成功完成 command。", "When an operation is already running, a new short, extended, or Host-Initiated Refresh request is aborted with Device Self-test in Progress; a new vendor-specific request remains vendor specific. STC Fh instead aborts the current operation, creates the newest result, clears current status, and then completes successfully in that order.", "shall"),
            c("SELFTEST-COMPLETION", "5.2.6", "201", "Device Self-test command 的 Admin CQE 只證明『啟動／中止動作已被處理』，不是背景測試已完成。command-specific status 1Dh 表示已有 operation in progress；software 必須把 CQE 與後續 LID 06h 分開記錄。", "The Admin CQE for Device Self-test proves that the start or abort action was processed, not that the background test finished. Command-specific status 1Dh means an operation is already in progress; software records the CQE separately from later LID 06h evidence."),
            c("SELFTEST-BACKGROUND", "8.1.8", "614", "Device Self-test 是由 vendor-specific segments 組成的背景工作。若另一個 command 必須暫停測試才能處理，controller 必須（shall）依序 suspend self-test、處理並完成該 command、再 resume self-test；同時可處理哪些 command 則由 vendor 決定。", "Device Self-test is background work composed of vendor-specific segments. If another command requires suspension, the controller shall suspend the self-test, process and complete that command, and then resume the self-test in order. Which commands may run concurrently remains vendor specific.", "shall"),
            c("SELFTEST-TIMING", "8.1.8.1-8.1.8.2", "615-616", "short operation 應（should）在兩分鐘內完成，且 Controller Level Reset 會中止；extended operation 應在 EDSTT 內完成，必須跨 Controller Level Reset 與 power restoration 持續並於之後 resume。兩者不能共用同一套 reset 預期。", "A short operation should finish within two minutes and is aborted by a Controller Level Reset. An extended operation should finish within EDSTT, shall persist across Controller Level Reset and power restoration, and resumes afterward. The two operations cannot share one reset expectation.", "should"),
            c("SELFTEST-ABORTS", "8.1.8.1-8.1.8.2", "615-616", "short 與 extended 都會被適用的 Format NVM、sanitize start 或 STC=Fh 中止，namespace 從 inventory 移除時則可能（may）中止。Figure 701 顯示 Format 的 NSID 與 secure-erase 選項會改變是否必須中止，不能只看 opcode。", "Both short and extended operations are aborted by an applicable Format NVM command, sanitize start, or STC Fh, and may be aborted when the namespace is removed from inventory. Figure 701 shows that Format NSID and secure-erase selections affect whether abort is required; the opcode alone is insufficient.", "may"),
            c("SELFTEST-LOG-COMMAND", "5.2.13", "213-216", "讀取 LID 06h 所需的最小 Get Log Page slice 是：LID=06h、LSP=0、RAE 依事件策略選擇、NUMD 表示 564 bytes、LPOL/LPOU=0、OT=0、CSI=0、UIDX=0。564 bytes=141 dwords，因此 0's-based NUMD=140=008Ch；RAE=0 時 CDW10=008C0006h。", "The minimum Get Log Page slice for LID 06h uses LID 06h, LSP 0, RAE selected by event policy, NUMD for 564 bytes, LPOL/LPOU 0, OT 0, CSI 0, and UIDX 0. 564 bytes are 141 dwords, so zero-based NUMD is 140 or 008Ch; with RAE 0, CDW10 is 008C0006h.", "none", "NVME-BASE-2.4", "BASE-DIAGMEM-DEPENDENCY-INCLUDE"),
            c("SELFTEST-CURRENT", "5.2.13.1.7", "229-230", "LID 06h 的 byte 0 以 DSTOS 表示目前 operation，byte 1 的 DSTCS[6:0] 是完成百分比；DSTOS=0 時 host 應忽略 DSTCS。controller 在 operation 完成或被中止時，必須先建立 result entry，之後才能把 in-progress status 清為 0。", "In LID 06h, byte 0 DSTOS identifies the current operation and byte 1 DSTCS[6:0] is the completion percentage; the host should ignore DSTCS when DSTOS is zero. When an operation completes or is aborted, the controller creates a result entry before clearing in-progress status to zero."),
            c("SELFTEST-HISTORY", "5.2.13.1.7", "229-230", "LID 06h 保留 20 筆、每筆 28 bytes 的結果，RDS1 永遠是最新完成或中止的 operation。未使用 entry 必須讓 DSTR=Fh 且 DSTC=0h，其他欄位由 host 忽略；不能把全零以外的殘值當成歷史結果。", "LID 06h retains 20 results of 28 bytes each, with RDS1 always the most recently completed or aborted operation. An unused entry uses DSTR Fh and DSTC 0h, while the host ignores its other fields; residual nonzero bytes are not history records.", "shall"),
            c("SELFTEST-RESULT", "5.2.13.1.7", "231", "每筆 DSTS 的高 nibble DSTC 表示原始 self-test code，低 nibble DSTR 表示完成／中止原因。只有 DSTR=7h 時 SEGN 才指出第一個失敗 segment；其他 DSTR 下 SEGN 應忽略。", "In each result DSTS, the high-nibble DSTC records the original self-test code and low-nibble DSTR records the completion or abort reason. SEGN identifies the first failed segment only when DSTR is 7h and is ignored for other DSTR values."),
            c("SELFTEST-VALIDITY", "5.2.13.1.7", "231-232", "VDINFO 的 NSIDVLD、FVLD、SCTVLD、SCVLD 是四個獨立 validity gates。NSID、FLBA、STCT、STC 只有在對應 bit=1 時才可解讀；先驗證 validity，再讀數值，不能用非零值猜測有效。", "VDINFO NSIDVLD, FVLD, SCTVLD, and SCVLD are independent validity gates. NSID, FLBA, STCT, and STC are interpreted only when their corresponding bit is one; validate the bit before the value instead of inferring validity from nonzero data."),
            c("SELFTEST-NVM-FLBA", "4.1.4.3", "76", "Base 將 Figure 219 的 FLBA 留給 I/O Command Set 定義。NVM Command Set 1.3 規定 bytes 23:16 是造成失敗的 logical block address；若有多個失敗 logical blocks，只回其中一個，且僅 FVLD=1 時有效。", "Base leaves Figure 219 FLBA to the applicable I/O Command Set. NVM Command Set 1.3 defines bytes 23:16 as the logical block address that caused the failure; when multiple logical blocks fail, only one is reported, and it is valid only when FVLD is one.", "none", "NVME-NVM-CS-1.3", "NVMCS-DIAGMEM-INCLUDE"),
            c("SELFTEST-DEBUG", "5.2.13.1.7, 8.1.8", "229-232, 614-616", "Debug 時把 command、current state 與歷史 result 分成三個時間點：保存 STC／NSID／CQE；輪詢 DSTOS／DSTCS；完成後保存 DSTS、SEGN、VDINFO、POH、NSID、FLBA、STCT、STC 與 vendor bytes。這樣才能分辨 command rejection、operation abort 與 media failure。", "Debugging separates command, current state, and historical result into three timestamps: retain STC/NSID/CQE, poll DSTOS/DSTCS, and after completion retain DSTS, SEGN, VDINFO, POH, NSID, FLBA, STCT, STC, and vendor bytes. This distinguishes command rejection, operation abort, and media failure."),
            c("HMB-CAPABILITY", "5.2.14.2.1, 8.2.4", "357, 362, 744", "HMPRE=0 表示 HMB 不支援；非零時以 4 KiB units 表示 preferred size，HMMIN 表示 minimum request。HMMINDS 與 HMMAXD 是 descriptor 限制。即使 host 無法提供 HMB，controller 仍必須（shall）正常運作。", "HMPRE zero means HMB is unsupported; a nonzero value is the preferred size in 4-KiB units, while HMMIN gives the minimum request. HMMINDS and HMMAXD constrain descriptors. The controller shall still function correctly when the host cannot provide HMB.", "shall", "NVME-BASE-2.4", "BASE-DIAGMEM-DEPENDENCY-INCLUDE"),
            c("HMB-OWNERSHIP", "5.2.30.2.3, 8.2.4", "515-516, 744", "HMB 是 host 配置、controller 專用的記憶體租約。Set Features enable 成功後，host 必須（shall）停止寫入 descriptor list 與所有描述的 memory ranges，直到 disable command 完成；這是 ownership transfer，不只是 performance hint。", "HMB is host-allocated memory leased exclusively to the controller. After successful Set Features enable, the host shall stop writing both the descriptor list and every described memory range until disable completes. This is an ownership transfer, not merely a performance hint.", "shall"),
            c("HMB-SET-COMMAND", "5.2.30, 5.2.30.2.3", "456-459, 516-518", "Set Features 使用 FID=0Dh；CDW11 放 EHM、MR、HMNARE，CDW12 放 HSIZE，CDW13／14 組成 64-bit HMDL address，CDW15 是 HMDLEC。HMDL address 必須 16-byte aligned；HMDLEC=0 必須回 Invalid Field in Command。", "Set Features uses FID 0Dh. CDW11 holds EHM, MR, and HMNARE; CDW12 holds HSIZE; CDW13/14 form the 64-bit HMDL address; and CDW15 is HMDLEC. The HMDL address is 16-byte aligned, and HMDLEC zero returns Invalid Field in Command.", "shall", "NVME-BASE-2.4", "BASE-DIAGMEM-DEPENDENCY-INCLUDE"),
            c("HMB-DESCRIPTORS", "5.2.30.2.3", "517-518", "HMDL 是連續的 16-byte descriptor array；每個 entry 的 BADD 必須依 CC.MPS memory page size 對齊，BSIZE 以相同 page units 表示連續長度。BSIZE=0 的 entry 由 controller 忽略；HSIZE 應與可用 descriptors 的 page 數相符。", "HMDL is a contiguous array of 16-byte descriptors. Each entry BADD is aligned to the CC.MPS memory-page size, and BSIZE gives a contiguous length in the same page units. The controller ignores an entry whose BSIZE is zero, and HSIZE is reconciled with the usable descriptor-page total."),
            c("HMB-NUMERIC", "5.2.30.2.3", "516-518", "說明性範例：CC.MPS=0 代表 4 KiB page；HSIZE=64 代表 256 KiB。若 HMDL=00000012_34567000h、HMDLEC=2，CDW13=34567000h、CDW14=00000012h、CDW15=00000002h。兩個 descriptor 各 BSIZE=32 pages 時，合計正好 64 pages。", "Informative example: CC.MPS zero means a 4-KiB page, so HSIZE 64 means 256 KiB. For HMDL 00000012_34567000h and HMDLEC 2, CDW13 is 34567000h, CDW14 is 00000012h, and CDW15 is 00000002h. Two descriptors of BSIZE 32 pages each total exactly 64 pages."),
            c("HMB-SEQUENCE", "5.2.30.2.3", "515-516", "HMB 已 enable 時再次送 EHM=1 必須以 Command Sequence Error 中止；尚未 enable 時送 EHM=0 則成功但不做事。disable completion 前 controller 應取回所需資料；CQE 被 posted 後才表示 host 可安全修改或回收 buffer。", "Reissuing EHM one while HMB is already enabled is aborted with Command Sequence Error; issuing EHM zero while disabled succeeds without action. Before disable completion, the controller should retrieve needed data; only the posted CQE means the host may safely modify or reclaim the buffer.", "should"),
            c("HMB-GET", "5.2.12, 5.2.30.2.3", "209-212, 518-519", "Get Features 使用 FID=0Dh；SEL≠supported-capabilities 成功時，CQE.DW0 回 EHM、HMNARE、HMNAR，data buffer 回 4 KiB Attributes data structure，包括 HSIZE、HMDL address 與 HMDLEC。『已啟用』與『目前正在限制 access』是不同狀態。", "Get Features uses FID 0Dh. On successful SEL other than supported capabilities, CQE.DW0 returns EHM, HMNARE, and HMNAR, while the data buffer returns a 4-KiB Attributes structure containing HSIZE, HMDL address, and HMDLEC. Enabled and currently access-restricted are different states.", "none", "NVME-BASE-2.4", "BASE-DIAGMEM-DEPENDENCY-INCLUDE"),
            c("HMB-NONOP", "5.2.30.2.3", "516-519", "HMNARE 只有 Identify.CTRATT.HMBR=1 時可啟用。HMNARE 是 policy，HMNAR 是 controller 此刻是否真的因 non-operational state 而被限制；Admin commands 與其啟動的 background operations 有明文例外。NOPPME 不改變這項 HMB restriction。", "HMNARE may be enabled only when Identify.CTRATT.HMBR is one. HMNARE is policy, while HMNAR reports whether a non-operational state currently restricts the controller; Admin commands and background operations initiated by them are explicit exceptions. NOPPME does not alter this HMB restriction."),
            c("HMB-RESET-RTD3", "8.2.4", "744", "HMB 不會跨 Controller Level Reset 保存在 controller。reset 後 host 應重新提供資源；若 MR=1 表示歸還先前內容，size、descriptor-list address、descriptor-list contents 與 HMB contents 必須完全相同。RTD3 前宜先 disable，恢復後再依是否保留內容選 MR。", "HMB is not persistent in the controller across Controller Level Reset. The host should provide resources again afterward. MR one returns prior contents and requires the exact same size, descriptor-list address, descriptor-list contents, and HMB contents. Disable before RTD3, then select MR according to content preservation on resume."),
            c("HMB-SURPRISE", "8.2.4", "744", "使用 HMB 時發生 surprise removal，controller 必須（shall）確保不造成 data loss 或 data corruption。這不代表 HMB 內容本身具有持久性，而是裝置不得把內部正確性依賴在 host 一定能先走正常 release 流程。", "During surprise removal while HMB is in use, the controller shall ensure no data loss or data corruption. This does not make HMB contents persistent; it means internal correctness cannot depend on the host always completing the normal release flow.", "shall"),
            c("DOORBELL-STRIDE", "3.1.4.1, 8.2.3", "56, 744", "CAP.DSTRD 的實際間距是 2^(2+DSTRD) bytes。DSTRD=0／2／4 分別得到 4／16／64 bytes；software emulation 可用 64-byte stride 把 doorbells 分散到 cacheline，硬體 NVMe interface 的 expected value 是 0h。", "CAP.DSTRD produces a spacing of 2^(2+DSTRD) bytes. DSTRD values 0, 2, and 4 yield 4, 16, and 64 bytes; software emulation can use 64-byte spacing to separate doorbells by cacheline, while the expected hardware-interface value is 0h."),
            c("DOORBELL-DEBUG", "8.2.3", "744", "emulator Debug 不只看 doorbell value，也要保存 CAP.DSTRD、計算後 byte stride、queue identifier、被監看的 cacheline 與 write timestamp。把 encoded DSTRD 直接當 bytes 會讓 queue notification 落到錯誤位址。", "Emulator debugging retains not only the doorbell value but CAP.DSTRD, computed byte stride, queue identifier, monitored cacheline, and write timestamp. Treating encoded DSTRD directly as bytes places queue notifications at the wrong address."),
            c("VENDOR-GATE", "5.2.14.2.1, 8.1.29", "356, 374, 733", "standard Vendor Specific command format 是 optional。AVSCC.VSCF 控制 vendor-specific Admin commands；ICSVSCC.SNVSCF 控制 vendor-specific I/O commands。兩個 capability 必須分開讀，不能因其中一個為 1 就假設另一類命令也使用 Figure 94。", "The standard Vendor Specific command format is optional. AVSCC.VSCF controls vendor-specific Admin commands, while ICSVSCC.SNVSCF controls vendor-specific I/O commands. Read the capabilities independently; one being set does not prove that the other command class uses Figure 94."),
            c("VENDOR-FORMAT", "4.1.1, 8.1.29", "143, 733", "Figure 94 保留 common CDW0、NSID、metadata/data pointers 與 CDW12-CDW15，並把 CDW10／11 定義成 NDT／NDM。若 command 不使用 NSID，必須清為 0；invalid NSID 在使用時必須回 Invalid Namespace or Format，inactive NSID 行為仍是 vendor specific。", "Figure 94 retains common CDW0, NSID, metadata/data pointers, and CDW12-CDW15, while defining CDW10/11 as NDT/NDM. An unused NSID is cleared to zero; an invalid NSID used by the command returns Invalid Namespace or Format, while inactive-NSID behavior remains vendor specific.", "shall"),
            c("VENDOR-LENGTH", "4.1.1, 8.1.29", "143, 733", "NDT 與 NDM 是實際 dword 數，不是 0's-based。NDT=00000100h 代表 256 dwords=1024 bytes；driver 可用 NDT／NDM 驗證 application buffer，避免 data 或 metadata transfer overflow。是否支援 standard format 仍先由 VSCF／SNVSCF gate。", "NDT and NDM are actual dword counts, not zero based. NDT 00000100h means 256 dwords or 1024 bytes; a driver can validate application buffers with NDT/NDM to prevent data or metadata-transfer overflow. VSCF or SNVSCF still gates use of the standard format."),
            c("BOUNDARY-DEBUG", "5.2.6, 5.2.30.2.3, 8.1.29, 8.2.3", "199-201, 515-519, 733, 744", "三條流程的共同 Debug 原則是找第一個 broken boundary：self-test 比對 command→current status→result；HMB 比對 capability→descriptor math→ownership→disable CQE；emulation／vendor command 比對 capability encoding→byte count／stride→實際 memory access。", "All three tracks debug from the first broken boundary: self-test compares command, current status, and result; HMB compares capability, descriptor math, ownership, and disable CQE; emulation/vendor commands compare capability encoding, byte count or stride, and actual memory access."),
        ],
    },
    "base-self-test-namespace-management": {
        "prefix": "BASENSMGMT",
        "title_zh": "NVMe Base 2.4：Device Self-test 與 Namespace Management",
        "title_en": "NVMe Base 2.4: Device Self-test and Namespace Management",
        "source_id": "NVME-BASE-2.4",
        "supporting_source_ids": ["NVME-NVM-CS-1.3"],
        "scope_entry": "BASE-NSMGMT-INCLUDE",
        "date": "2026-09-02",
        "verified_date": "2026-09-02",
        "range": "Base §5.2.6、§5.2.13.1.7（僅 LID 06h）、§5.2.24、§5.2.25、§8.1.8、§8.1.17（排除 §8.1.17.3），以及 NVM Command Set 1.3 §2.1.1、§4.1.4.3、§4.1.6、§5.8；另含理解與實作所需的最小 dependency slice",
        "range_en": "Base §§5.2.6, 5.2.13.1.7 (LID 06h only), 5.2.24, 5.2.25, 8.1.8, and 8.1.17 (excluding §8.1.17.3), plus NVM Command Set 1.3 §§2.1.1, 4.1.4.3, 4.1.6, and 5.8; includes the minimum dependency slice needed for understanding and implementation",
        "diagram": ["Discover capability and capacity", "Run self-test / construct namespace", "Observe LID 06h / receive NSID", "Attach, verify, detach, or delete"],
        "diagram_note_zh": "本報告把診斷與配置分成兩條生命週期：Self-test 用 LID 06h 證明背景 operation 的結果；Namespace Management 先建立未附掛 namespace，再用 Controller List 建立可存取關係，最後以 event、Identify 與 CQE 關閉驗證迴路。",
        "diagram_note_en": "The report separates diagnostic and provisioning lifecycles. LID 06h proves the result of a background self-test, while Namespace Management first creates an unattached namespace, then uses a Controller List to establish access and closes verification through events, Identify data, and CQEs.",
        "claims": [
            c("SELFTEST-GATE", "5.2.14.2.1, 8.1.8", "353-358, 614", "啟動 Device Self-test 前先讀 Identify Controller：OACS.DSTS 判斷 command 是否支援；EDSTT 是 extended operation 在 power state 0 的名目分鐘數；DSTO.SDSO 決定同時只有一個 subsystem-wide operation，或每個 controller 各一個。三者分別是支援、時間與 concurrency scope。", "Before starting Device Self-test, read Identify Controller. OACS.DSTS gates command support, EDSTT gives the nominal extended-operation duration in minutes at power state 0, and DSTO.SDSO selects one subsystem-wide operation versus one operation per controller. They describe support, time, and concurrency scope respectively.", "none", "NVME-BASE-2.4", "BASE-NSMGMT-DEPENDENCY-INCLUDE"),
            c("SELFTEST-NSID", "5.2.6", "199", "Device Self-test 由收到 command 的 controller 執行。NSID=00000000h 只測 controller；00000001h～FFFFFFFEh 指定一個 active namespace；FFFFFFFFh 包含提交當下該 controller 可存取的所有 attached namespaces。invalid 與 inactive NSID 是不同錯誤。", "Device Self-test is performed by the controller receiving the command. NSID 00000000h tests only that controller; 00000001h through FFFFFFFEh select one active namespace; and FFFFFFFFh includes all attached namespaces accessible through that controller when the operation starts. Invalid and inactive NSIDs are distinct errors."),
            c("SELFTEST-STC", "5.2.6", "199-200", "CDW10.STC[3:0] 選動作：1h=short、2h=extended、3h=Host-Initiated Refresh、Eh=vendor specific、Fh=abort；其餘 encoding reserved。只有 STC=Eh 時 CDW15.DSTP 才是 vendor specific，其他 STC 下 CDW15 reserved。", "CDW10.STC[3:0] selects 1h short, 2h extended, 3h Host-Initiated Refresh, Eh vendor specific, or Fh abort; the other encodings are reserved. CDW15.DSTP is vendor specific only when STC is Eh and is reserved for other STC values.", "reserved"),
            c("SELFTEST-INPROGRESS", "5.2.6", "200", "已有 operation 時，再送 short、extended 或 Host-Initiated Refresh 必須以 Device Self-test in Progress 中止；STC=Fh 則依序中止目前 operation、建立最新 result、清除 current status，再成功完成 abort command。", "While an operation is active, a new short, extended, or Host-Initiated Refresh request shall be aborted with Device Self-test in Progress. STC Fh instead aborts the current operation, creates the newest result, clears current status, and successfully completes the abort command in that order.", "shall"),
            c("SELFTEST-COMPLETION", "5.2.6", "201", "Device Self-test 的 Admin CQE 只證明啟動或中止動作已被處理，不代表背景測試完成。software 必須把 command CQE、LID 06h current state 與最後 result entry 當成三個不同時間點。", "The Device Self-test Admin CQE proves only that the start or abort action was processed; it does not mean that the background test has finished. Software treats the command CQE, current LID 06h state, and final result entry as three distinct timestamps."),
            c("SELFTEST-BACKGROUND", "8.1.8", "614", "Device Self-test 是由 vendor-specific segments 組成的背景工作。若處理另一個 command 必須暫停測試，controller 必須（shall）依序 suspend self-test、處理並完成該 command、再 resume self-test；可同時處理哪些 command 仍由 vendor 決定。", "Device Self-test is background work composed of vendor-specific segments. If processing another command requires suspension, the controller shall suspend the self-test, process and complete that command, and resume the self-test in order. Which commands may run concurrently remains vendor specific.", "shall"),
            c("SELFTEST-TIMING", "8.1.8.1-8.1.8.2", "615-616", "short operation 應（should）在兩分鐘內完成，Controller Level Reset 會中止；extended operation 應在 EDSTT 內完成，必須跨 Controller Level Reset 與 power restoration 持續並於之後 resume。兩種測試不能共用同一套 reset 預期。", "A short operation should finish within two minutes and is aborted by Controller Level Reset. An extended operation should finish within EDSTT, shall persist across Controller Level Reset and power restoration, and resumes afterward. The two test types do not share one reset expectation.", "should"),
            c("SELFTEST-ABORTS", "8.1.8.1-8.1.8.2", "615-616", "short 與 extended 都會被適用的 Format NVM、sanitize start 或 STC=Fh 中止，namespace 從 inventory 移除時則可能（may）中止。Figure 701 顯示必須同時看 Format NSID、secure-erase 選項與 Self-test NSID。", "Both short and extended operations are aborted by an applicable Format NVM command, sanitize start, or STC Fh, and may be aborted when the namespace is removed from inventory. Figure 701 requires the Format NSID, secure-erase selection, and Self-test NSID to be evaluated together.", "may"),
            c("SELFTEST-LOG-COMMAND", "5.2.13", "213-216", "完整讀取 LID 06h 使用 564 bytes=141 dwords，因此 0's-based NUMD=140=008Ch；LID=06h、LSP=0、LPOL/LPOU=0、OT=0、CSI=0、UIDX=0。RAE=0 時 CDW10=008C0006h。", "A complete LID 06h read transfers 564 bytes or 141 dwords, so zero-based NUMD is 140 or 008Ch. Use LID 06h, LSP zero, LPOL/LPOU zero, OT zero, CSI zero, and UIDX zero. With RAE zero, CDW10 is 008C0006h.", "none", "NVME-BASE-2.4", "BASE-NSMGMT-DEPENDENCY-INCLUDE"),
            c("SELFTEST-CURRENT", "5.2.13.1.7", "229-230", "LID 06h byte 0 的 DSTOS 表示目前 operation，byte 1 的 DSTCS[6:0] 是完成百分比；DSTOS=0 時 host 應忽略 DSTCS。operation 完成或中止時，controller 必須先建立 result entry，再把 in-progress status 清為 0。", "In LID 06h, byte 0 DSTOS identifies the current operation and byte 1 DSTCS[6:0] gives completion percentage; the host should ignore DSTCS when DSTOS is zero. When an operation completes or is aborted, the controller creates a result entry before clearing in-progress status to zero.", "shall"),
            c("SELFTEST-HISTORY", "5.2.13.1.7", "229-232", "LID 06h 保留 20 筆、每筆 28 bytes 的結果，RDS1 是最新一筆。DSTS 高 nibble DSTC 記原始 self-test code，低 nibble DSTR 記完成或中止原因；只有 DSTR=7h 時 SEGN 才可解讀。", "LID 06h retains twenty 28-byte results with RDS1 newest. The high DSTS nibble DSTC records the original self-test code and the low nibble DSTR records completion or abort reason. SEGN is interpreted only when DSTR is 7h."),
            c("SELFTEST-VALIDITY", "5.2.13.1.7", "231-232", "VDINFO 的 NSIDVLD、FVLD、SCTVLD、SCVLD 是四個獨立 validity gates。NSID、FLBA、STCT、STC 只有在對應 bit=1 時才可讀；parser 不得以欄位非零猜測有效。", "VDINFO NSIDVLD, FVLD, SCTVLD, and SCVLD are four independent validity gates. NSID, FLBA, STCT, and STC are interpreted only when the corresponding bit is one; a parser does not infer validity from a nonzero field."),
            c("SELFTEST-NVM-FLBA", "4.1.4.3", "76", "NVM Command Set 1.3 將 result bytes 23:16 定義為造成失敗的 logical block address。若多個 logical blocks 失敗，只回其中一個，而且僅在 FVLD=1 時有效。", "NVM Command Set 1.3 defines result bytes 23:16 as the logical block address that caused the failure. If multiple logical blocks fail, only one is reported, and it is valid only when FVLD is one.", "none", "NVME-NVM-CS-1.3", "NVMCS-NSMGMT-INCLUDE"),
            c("CAPACITY-MODEL", "2.1.1", "13-14", "Namespace Size（NSZE）是 LBA 0 到 n−1 的總 logical blocks；Namespace Capacity（NCAP）是任一時點最多可配置的 blocks；Namespace Utilization（NUSE）是目前已配置 blocks。永遠遵守 NSZE ≥ NCAP ≥ NUSE。", "Namespace Size (NSZE) is the total logical-block range from LBA zero through n minus one; Namespace Capacity (NCAP) is the maximum allocatable blocks at any time; and Namespace Utilization (NUSE) is the number currently allocated. NSZE is always at least NCAP, which is at least NUSE.", "none", "NVME-NVM-CS-1.3", "NVMCS-NSMGMT-INCLUDE"),
            c("THIN-PROVISIONING", "2.1.1", "13", "NSFEAT.THINP=1 時，controller 可（may）回報 NCAP<NSZE，並必須（shall）追蹤 NUSE。THINP=0 時，controller 必須回報 NCAP=NSZE，且可讓 NUSE 永遠等於 NCAP。", "With NSFEAT.THINP one, a controller may report NCAP below NSZE and shall track NUSE. With THINP zero, the controller shall report NCAP equal to NSZE and may report NUSE as always equal to NCAP.", "shall", "NVME-NVM-CS-1.3", "NVMCS-NSMGMT-INCLUDE"),
            c("NSMGMT-CAPABILITY", "8.1.17", "660", "完整 Namespace Management capability 由 Namespace Management command 與 Namespace Attachment command 組成。支援時 controller 必須支援兩者、設 OACS.NMS=1、支援 Attached Namespace Attribute Changed event；Allocated event 為 should，Namespace Granularity 與 Restore Default 為 may。", "The complete Namespace Management capability consists of Namespace Management and Namespace Attachment. A supporting controller shall implement both, set OACS.NMS to one, and support the Attached Namespace Attribute Changed event; the Allocated event is a should, while Namespace Granularity and Restore Default are may capabilities.", "shall"),
            c("NSID-LIFECYCLE", "8.1.17", "660", "create 成功後 namespace 已 allocated 但尚未 attached，因此對 controller 尚非 active。detach 使該 controller 上的 NSID 變 inactive；delete 使 subsystem 中的 NSID 變 unallocated。受影響的 outstanding 或後續 commands 依 inactive NSID 處理。", "After create succeeds, the namespace is allocated but not attached and therefore is not active on a controller. Detach makes its NSID inactive on that controller; delete makes the NSID unallocated in the subsystem. Affected outstanding and later commands are handled as though issued to an inactive NSID."),
            c("CREATE-PREFLIGHT", "8.1.17.1", "661-662", "create 前先以 NSID=FFFFFFFFh、CNS=00h 讀 common namespace capabilities；若支援，再用 CNS=16h 讀 Namespace Granularity，並確認可用 capacity。這三步完成後才建立 4096-byte create buffer。", "Before create, read common namespace capabilities with NSID FFFFFFFFh and CNS 00h; if supported, read Namespace Granularity with CNS 16h and determine available capacity. Only then construct the 4096-byte create buffer."),
            c("CREATE-BASE-COMMAND", "5.2.25", "446-448", "Create 使用 NSID=0、SEL=0h 與 CSI=00h（NVM Command Set）。DPTR 指向 4096-byte data structure：bytes 0:511 是 I/O Command Set specific、512:1023 reserved、1024:4095 vendor specific。reserved bytes 由 host 清為 0。", "Create uses NSID zero, SEL 0h, and CSI 00h for the NVM Command Set. DPTR identifies a 4096-byte structure: bytes 0:511 are I/O-Command-Set-specific, 512:1023 are reserved, and 1024:4095 are vendor specific. The host clears reserved bytes to zero.", "reserved"),
            c("CREATE-NVM-PAYLOAD", "4.1.6.4", "111-113", "NVM create payload 的主要 host-specified fields 是 NSZE、NCAP、FLBAS、DPS、NMIC、ANAGRPID、NVMSETID、ENDGID、LBSTM、NPHNDLS 與 Placement Handle List。成功 create 後，namespace 依這些屬性格式化；未使用的 reserved fields 應清為 0。", "The primary host-specified NVM create fields are NSZE, NCAP, FLBAS, DPS, NMIC, ANAGRPID, NVMSETID, ENDGID, LBSTM, NPHNDLS, and the Placement Handle List. After successful create, the namespace is formatted with these attributes, and unused reserved fields should be zero.", "should", "NVME-NVM-CS-1.3", "NVMCS-NSMGMT-INCLUDE"),
            c("PROTECTION-VALIDATION", "4.1.6.2", "110", "End-to-end Data Protection 設定在 create 時套用。LBAFEE 未啟用時，特定 16-bit STS 非零、32-bit 或 64-bit Guard Protection Information 組合必須以 Invalid Namespace or Format 中止；LBSTM 不符合 Figure 127 capability 時則回 Invalid Field in Command。", "End-to-end Data Protection settings are applied during create. Without LBAFEE, specified combinations using nonzero STS with 16-bit, or 32-bit or 64-bit Guard Protection Information, are aborted with Invalid Namespace or Format. An LBSTM that violates Figure 127 capability returns Invalid Field in Command.", "shall", "NVME-NVM-CS-1.3", "NVMCS-NSMGMT-INCLUDE"),
            c("FDP-VALIDATION", "4.1.6.3", "110-111", "只有指定 Endurance Group 已啟用 Flexible Data Placement（FDP）且 SEL=Create 時，NPHNDLS 與 Placement Handle List 才參與驗證。NPHNDLS 不得大於支援的 Reclaim Unit Handles 或 128；重複、越界、格式不相容或無可用 handle 會導向 Invalid Placement Handle List 或 Invalid Format。", "NPHNDLS and the Placement Handle List participate in validation only when Flexible Data Placement (FDP) is enabled in the selected Endurance Group and SEL is Create. NPHNDLS may not exceed the supported Reclaim Unit Handles or 128; duplicates, out-of-range handles, incompatible formats, or no available handle lead to Invalid Placement Handle List or Invalid Format.", "shall", "NVME-NVM-CS-1.3", "NVMCS-NSMGMT-INCLUDE"),
            c("GROUP-SELECTION", "8.1.17", "661", "NVMSETID／ENDGID 的決策矩陣為：兩者 0 由 controller 選兩者；NVMSETID=0、ENDGID≠0 時由指定 Endurance Group 內選 NVM Set；NVMSETID≠0、ENDGID=0 必須 Invalid Field；兩者非 0 時只有該 NVM Set 確實屬於指定 Endurance Group 才可配置。", "The NVMSETID/ENDGID matrix is: both zero lets the controller choose both; NVMSETID zero with nonzero ENDGID selects an NVM Set inside the specified Endurance Group; nonzero NVMSETID with zero ENDGID is Invalid Field; and both nonzero are valid only when that NVM Set belongs to the specified Endurance Group.", "shall"),
            c("ALLOCATION-ROUNDING", "8.1.17", "661", "controller 可（may）按內部 allocation unit 把實際消耗容量向上取整。Spec 範例中，32 blocks×4 KiB=128 KiB 的 namespace，在 1 MiB allocation unit 下可消耗 1 MiB；因此 capacity consumption 不一定等於 logical block size×block count。", "A controller may round actual capacity consumption up to an internal allocation unit. In the specification example, 32 blocks times 4 KiB equals a 128-KiB namespace but may consume 1 MiB with a 1-MiB allocation unit; capacity consumption therefore need not equal logical-block size times block count.", "may"),
            c("GRANULARITY-HINTS", "5.8", "165", "Namespace Granularity 的 NSG 與 NCG 都是 byte-unit hints。若 NSZE×LBA size 可整除 NSG、NCAP×LBA size 可整除 NCG 且 NSZE=NCAP，配置為 fully provisioned 且全部容量可由 LBA 定址；不符合 hint 可能浪費容量，但 otherwise-valid create 不得只因違反 hint 被中止。", "Namespace Granularity NSG and NCG are byte-unit hints. If NSZE times LBA size is divisible by NSG, NCAP times LBA size is divisible by NCG, and NSZE equals NCAP, the namespace is fully provisioned and all allocated capacity is LBA-addressable. Violating a hint may waste capacity, but an otherwise valid create shall not be aborted solely for that reason.", "shall not", "NVME-NVM-CS-1.3", "NVMCS-NSMGMT-INCLUDE"),
            c("ATTACH-COMMAND", "5.2.24", "444-445", "Namespace Attachment 的 DPTR 指向 4096-byte Controller List；SEL=0h attach、SEL=1h detach。以 PRP 指向此 buffer 時不得使用 PRP List，因 buffer 不可跨越超過一個 memory-page boundary。attach／detach 狀態跨所有 reset events 保留。", "Namespace Attachment DPTR points to a 4096-byte Controller List; SEL 0h attaches and SEL 1h detaches. With PRPs, the buffer cannot use a PRP List because it may not cross more than one memory-page boundary. Attach/detach state persists across all reset events.", "shall not"),
            c("ATTACH-LIMITS", "5.2.24", "444-445", "attach 前分別核對 Domain aggregate MAXDNA 與每個 I/O controller 的 MAXCNA；非零 limit 被超過時回 Namespace Attachment Limit Exceeded。還要核對 I/O Command Set support／enable state，不能把所有 attach failure 都歸成同一種 status。", "Before attach, check Domain-aggregate MAXDNA and per-I/O-controller MAXCNA separately. Exceeding a nonzero limit returns Namespace Attachment Limit Exceeded. I/O Command Set support and enablement are additional independent gates, so attach failures do not collapse to one status."),
            c("CREATE-COMPLETION", "5.2.25, 8.1.17.1", "446-448, 662", "Create 成功時 controller 選擇可用 NSID，CQE.DW0 回傳該 NSID；此刻 namespace 尚未 attached。software 必須先保存 returned NSID，再以 Namespace Attachment 建立 controller access，不能在 create CQE 後直接送 I/O。", "On successful create, the controller selects an available NSID and returns it in CQE DW0; the namespace is still unattached. Software preserves the returned NSID and then establishes controller access through Namespace Attachment instead of issuing I/O immediately after the create CQE."),
            c("DELETE", "5.2.25, 8.1.17.1", "446, 448, 662", "Delete 的 NSID 指定已建立 namespace；FFFFFFFFh 表示 delete all，即使目前零個 namespaces 也成功。delete 會使 namespace 從 subsystem 消失並具有 detach side effect；host 應先 detach 所有 controllers，讓 event 與 outstanding-I/O 行為更可控。", "Delete NSID selects a created namespace, while FFFFFFFFh means delete all and succeeds even when no namespace exists. Delete removes the namespace and has a detach side effect; the host should detach it from every controller first so events and outstanding-I/O behavior remain controlled.", "should"),
            c("RESTORE-DEFAULT", "5.2.25.1", "447-448", "Restore Default 使用 SEL=2h，NSID 應為 0 且 controller 會忽略它。先讀 RDNCS，刪除 subsystem 中所有 namespaces，再送 restore；若仍有 namespace，回 Command Sequence Error。成功前 controller 必須套用 current active firmware image 的 default configuration 並設 DNCS=1。", "Restore Default uses SEL 2h; NSID should be zero and is ignored by the controller. Check RDNCS, delete every namespace in the subsystem, and then issue restore; any remaining namespace causes Command Sequence Error. Before success, the controller applies the current active firmware image's default configuration and sets DNCS to one.", "shall"),
            c("COMMAND-STATUS", "5.2.24-5.2.25", "445, 448", "Debug 要保留 command-specific status：Attachment 可回 already attached 18h、private 19h、not attached 1Ah、Controller List invalid 1Ch、ANA attach failed 25h、limit 27h、I/O Command Set 29h／2Ah；Management 可回 Invalid Format 0Ah、insufficient capacity 15h、NSID unavailable 16h、thin provisioning unsupported 1Bh、ANA group invalid 24h。", "Debug evidence retains command-specific status. Attachment may return already attached 18h, private 19h, not attached 1Ah, Controller List invalid 1Ch, ANA attach failed 25h, limit 27h, or I/O Command Set 29h/2Ah. Management may return Invalid Format 0Ah, insufficient capacity 15h, NSID unavailable 16h, thin provisioning unsupported 1Bh, or ANA group invalid 24h."),
            c("NAMESPACE-EVENTS", "8.1.17.1-8.1.17.2", "662-663", "create 改變 Allocated Namespace ID list；attach／detach 改變 Active Namespace ID list；delete 可能同時改變兩者。啟用對應 notice 時，host 收到 asynchronous event 後應重新 Identify，而不是只用 event code 猜新 inventory。§8.1.17.2 對處理 delete 的 controller 與其他 controllers 規定不同 event reporting。", "Create changes the Allocated Namespace ID list, attach/detach changes the Active Namespace ID list, and delete may change both. When the corresponding notice is enabled, the host reissues Identify after the asynchronous event rather than inferring inventory from the event code alone. Section 8.1.17.2 distinguishes the controller processing delete from the other controllers."),
            c("GRANULARITY-EXAMPLE", "5.8", "165", "說明性範例：LBA=4 KiB、NSG=1 MiB（256 LBAs）、NCG=2 MiB（512 LBAs）。NSZE=NCAP=1024 同時滿足兩種 granularity；NSZE=1000、NCAP=1000 不滿足 NSG／NCG 整除，但若其他欄位都合法，controller 不得只因這個 hint violation 中止 create。", "Informative example: with 4-KiB LBAs, NSG 1 MiB equals 256 LBAs and NCG 2 MiB equals 512 LBAs. NSZE and NCAP of 1024 satisfy both granularities. Values of 1000 violate NSG/NCG divisibility, but an otherwise valid create is not aborted solely for that hint violation.", "shall not", "NVME-NVM-CS-1.3", "NVMCS-NSMGMT-INCLUDE"),
            c("END-TO-END-DEBUG", "5.2.24-5.2.25, 8.1.17.1", "444-448, 661-663", "完整 trace 至少保存：OACS.NMS／limits、common Identify 與 granularity snapshot、4096-byte create buffer、raw SQE、CQE.DW0 NSID、Controller List、attach CQE、AER、重新 Identify 結果，以及 detach／delete 後的 inactive／unallocated 狀態。第一個不一致的 boundary 才是 Debug 起點。", "A complete trace retains OACS.NMS and limits, common Identify and granularity snapshots, the 4096-byte create buffer, raw SQE, CQE DW0 NSID, Controller List, attach CQE, AER, refreshed Identify result, and inactive/unallocated state after detach/delete. The first inconsistent boundary is the debugging start point."),
        ],
    },
    "pcie-transport-1.4": {
        "prefix": "PCIE14",
        "title_zh": "NVMe over PCIe Transport 1.4：完整傳輸綁定",
        "title_en": "NVMe over PCIe Transport 1.4: Complete Transport Binding",
        "source_id": "NVME-PCIE-TRANSPORT-1.4",
        "scope_entry": "PCIE14-INCLUDE",
        "range": "§1-§3 與 Annex A；文件頁／PDF 頁 1-48",
        "range_en": "§1-§3 and Annex A; printed/PDF pages 1-48",
        "diagram": ["Write SQE", "Ring SQ tail doorbell", "Controller executes", "Read CQE / ring CQ head"],
        "diagram_note_zh": "PCIe transport 以 host memory 的 queue 配合 MMIO doorbell；資料可由 PRP／SGL 指到 host-addressable memory。",
        "diagram_note_en": "The PCIe transport combines queues in host memory with MMIO doorbells; PRPs or SGLs identify data in host-addressable memory.",
        "claims": [
            c("SCOPE", "1.2", "6", "PCIe Transport 補充 Base Specification，定義 PCIe 專屬資料結構、延伸、要求與行為；通用 NVMe 行為仍由 Base 定義。規格衝突時 Base 的優先序高於 Transport。", "The PCIe Transport supplements the Base Specification with PCIe-specific structures, extensions, requirements, and behavior; common NVMe behavior remains in Base. In a conflict, Base has higher precedence than a Transport Specification.", "shall", "NVME-PCIE-TRANSPORT-1.4"),
            c("CONVENTION", "1.3", "6-7", "本文件沿用 Base 的 conventions；register／property 表格中的 Reset 欄改表示依 PCI 或 PCIe 規格定義之 reset 後欄位值。", "This document inherits Base conventions. In register or property tables, the Reset column instead denotes the post-reset field value defined by the applicable PCI or PCIe specification.", "none", "NVME-PCIE-TRANSPORT-1.4"),
            c("KEYWORDS", "1.4.1", "2-3", "shall、may 與 should 的語氣仍由 Base 2.4 定義；Transport 摘要不得自行提高或降低規範強度。", "The force of shall, may, and should remains defined by Base 2.4; a Transport summary must not strengthen or weaken the normative language.", "none", "NVME-BASE-2.4"),
            c("OVERVIEW", "2", "8", "PCIe transport 使用 memory-mapped I/O 進行資料與 register 存取，並使用 PCIe configuration space 與 message-signaled interrupt。", "The PCIe transport uses memory-mapped I/O for data and register access, along with PCIe configuration space and message-signaled interrupts.", "none", "NVME-PCIE-TRANSPORT-1.4"),
            c("MMIO", "3.1", "9-10", "NVMe controller registers 位於 BAR0／BAR1 所指定的 memory space。host 必須（shall）使用 native width 或 aligned 32-bit access，不得發出 locked access；違反時行為未定義。", "NVMe controller registers reside in memory space identified by BAR0/BAR1. The host shall use native-width or aligned 32-bit accesses and shall not issue locked accesses; violation produces undefined behavior.", "shall", "NVME-PCIE-TRANSPORT-1.4"),
            c("DOORBELL", "3.1.2.1-3.1.2.2", "10-11", "SQ tail 與 CQ head doorbell 從 offset 1000h 起，實際 stride 由 CAP.DSTRD 決定；queue identifier y 參與 offset 計算。", "SQ-tail and CQ-head doorbells begin at offset 1000h, with stride determined by CAP.DSTRD; queue identifier y participates in the offset calculation.", "none", "NVME-PCIE-TRANSPORT-1.4"),
            c("QUEUE", "3.2", "11", "PCIe 支援多個 Submission Queues 共用一個 Completion Queue。建立 CQ 時若啟用 interrupt，Interrupt Vector 必須（shall）初始化成對應 MSI-X 或 multiple-message MSI vector。", "PCIe permits multiple Submission Queues to share a Completion Queue. If interrupts are enabled when creating the CQ, Interrupt Vector shall be initialized to the corresponding MSI-X or multiple-message MSI vector.", "shall", "NVME-PCIE-TRANSPORT-1.4"),
            c("RESET", "3.3", "11-12", "PCIe reset 來源包含 Base 定義的 controller/reset 流程與 PCIe 層級 reset。Recovery 設計要以 reset 類型判斷 controller property、queue 與 PCI configuration state。", "PCIe reset sources include Base controller/reset flows and PCIe-level resets. Recovery logic uses the reset type to determine controller-property, queue, and PCI-configuration state.", "none", "NVME-PCIE-TRANSPORT-1.4"),
            c("COMMAND", "3.4", "12-13", "command flow 是：寫 SQE、更新 SQ tail doorbell、controller 取走與執行、寫 CQE、發出 interrupt（若啟用）、host 處理 CQE、更新 CQ head doorbell。doorbell 只通告 pointer，不攜帶 command 本體。", "The command flow writes an SQE, updates the SQ-tail doorbell, lets the controller fetch and execute, posts a CQE, optionally interrupts, processes the CQE, and updates the CQ-head doorbell. A doorbell conveys a pointer, not the command body.", "none", "NVME-PCIE-TRANSPORT-1.4"),
            c("INTERRUPT", "3.5", "13-16", "可用模式為 pin-based、single-message MSI、multiple-message MSI 與 MSI-X。規格建議 MSI-X；coalescing 可降低 interrupt rate，但通常增加 latency。Admin CQ 的 interrupt 不宜（should not）延遲。", "Modes are pin-based, single-message MSI, multiple-message MSI, and MSI-X. The specification recommends MSI-X. Coalescing can reduce interrupt rate at the cost of latency, and Admin-CQ interrupts should not be delayed.", "should", "NVME-PCIE-TRANSPORT-1.4"),
            c("POWER", "3.6", "16", "host 絕不可（shall never）選擇功耗高於 PCIe slot power limit 的 NVMe power state；違反時 power behavior 未定義。", "The host shall never select an NVMe power state whose consumption exceeds the PCIe slot power limit; violation results in undefined power behavior.", "shall", "NVME-PCIE-TRANSPORT-1.4"),
            c("ERROR", "3.7", "16", "NVMe command error 由 CQE status 回報；PCIe transport／link error 則依 PCIe 機制與本文件的 NVMe-specific 要求處理，兩者的 recovery 層級不同。", "NVMe command errors are reported in CQE status, while PCIe transport or link errors use PCIe mechanisms plus this document’s NVMe-specific requirements. Their recovery scopes differ.", "none", "NVME-PCIE-TRANSPORT-1.4"),
            c("CONFIG", "3.8.1-3.8.7", "16-35", "§3.8 逐欄定義 NVMe controller 的 PCI header、Power Management、MSI／MSI-X、PCIe capability 與 AER 額外要求。PCI／PCIe 原始欄位語意仍以 PCI-SIG 規格為準。", "Section 3.8 defines additional NVMe-controller requirements for the PCI header, Power Management, MSI/MSI-X, PCIe capability, and AER. Original PCI/PCIe field semantics remain governed by PCI-SIG specifications.", "none", "NVME-PCIE-TRANSPORT-1.4"),
            c("SECURITY", "3.8.8-3.8.10", "35-39", "power-loss signaling、confidential computing 與 TDISP 把平台事件或隔離狀態映射到 NVMe controller 行為；實作仍需要本次未提供的外部 PCIe／TDISP 規格。", "Power-loss signaling, confidential computing, and TDISP map platform events or isolation state to NVMe-controller behavior. Implementation still requires external PCIe/TDISP specifications not supplied for this report.", "none", "NVME-PCIE-TRANSPORT-1.4"),
            c("EOM", "3.9", "39-46", "Physical Interface Receiver Eye Opening Measurement log page 以 header、lane descriptor 與 EOM data 回報量測；host 先查支援與大小，再依 lane／parameter 解析。", "The Physical Interface Receiver Eye Opening Measurement log page reports measurements through a header, lane descriptors, and EOM data. The host checks support and size before parsing lanes and parameters.", "none", "NVME-PCIE-TRANSPORT-1.4"),
            c("HOST", "Annex A", "47-48", "Annex A 是 informative host checklist：提交時先寫 SQE 再 doorbell；完成時以 phase 判斷新 CQE，完成讀取後再推進 CQ head；interrupt handler 要處理同 vector 的所有相關 CQ。", "Annex A is an informative host checklist: write the SQE before its doorbell, use phase to identify a new CQE, advance CQ head after consumption, and service every relevant CQ associated with an interrupt vector.", "none", "NVME-PCIE-TRANSPORT-1.4"),
        ],
    },
}

POST_IMAGES = {
    "base-ch1-2": {
        "zh": "posts/2026/dogMC_title.jpg",
        "en": "posts/2026/cat_title.jpg",
    },
    "base-ch3": {
        "zh": "posts/2026/dogMC_title.jpg",
        "en": "posts/2026/cat_title.jpg",
    },
    "base-ch4": {
        "zh": "posts/2026/dogMC_title.jpg",
        "en": "posts/2026/cat_title.jpg",
    },
    "base-admin-fw-logs": {
        "zh": "posts/2026/dogMC_title.jpg",
        "en": "posts/2026/cat_title.jpg",
    },
    "base-power-features": {
        "zh": "posts/2026/dogMC_title.jpg",
        "en": "posts/2026/cat_title.jpg",
    },
    "base-self-test-hmb-emulation": {
        "zh": "posts/2026/dogMC_title.jpg",
        "en": "posts/2026/cat_title.jpg",
    },
    "base-self-test-namespace-management": {
        "zh": "posts/2026/dogMC_title.jpg",
        "en": "posts/2026/cat_title.jpg",
    },
    "pcie-transport-1.4": {
        "zh": "posts/2026/lion_title.jpg",
        "en": "posts/2026/catFlower_title.jpg",
    },
}

CORE_TITLES = {
    "BASE12-FAMILY": ("NVMe 規格家族的分工", "Roles in the NVMe specification family"),
    "BASE12-KEYWORDS": ("規範性用語的強度", "Normative keyword strength"),
    "BASE12-NUMBERS": ("進位與容量單位", "Radix and capacity units"),
    "BASE12-DWORD": ("byte、word 與 dword", "Byte, word, and dword relationships"),
    "BASE12-QUEUE": ("PCIe queue pair 模型", "PCIe queue-pair model"),
    "BASE12-STORAGE": ("NVM 儲存階層", "NVM storage hierarchy"),
    "BASE12-COMMANDSET": ("Admin 與 I/O Command Set", "Admin and I/O Command Sets"),
    "BASE12-SUBSYSTEM": ("subsystem 物件與 NSID", "Subsystem objects and NSIDs"),
    "BASE12-MULTIPATH": ("multi-path 與 namespace sharing", "Multi-path and namespace sharing"),
    "BASE12-ASYMMETRY": ("非對稱路徑特性", "Asymmetric path characteristics"),
    "BASE3-STATIC": ("static controller model", "Static controller model"),
    "BASE3-TYPES": ("I/O 與 Administrative controller", "I/O and Administrative controllers"),
    "BASE3-ORDER": ("命令與完成順序", "Command and completion ordering"),
    "BASE3-PROPERTY": ("property 存取寬度", "Property access width"),
    "BASE3-NAMESPACE": ("NSID 狀態與特殊值", "NSID states and special values"),
    "BASE3-MEDIA": ("媒體與回收階層", "Media and reclamation hierarchy"),
    "BASE3-DOMAIN": ("domain 邊界與識別碼", "Domain boundaries and identifiers"),
    "BASE3-QUEUE": ("PCIe queue 建立與 pointer", "PCIe queue creation and pointers"),
    "BASE3-PROCESS": ("命令處理與 arbitration", "Command processing and arbitration"),
    "BASE3-INIT": ("controller 初始化", "Controller initialization"),
    "BASE3-SHUTDOWN": ("shutdown 狀態流程", "Shutdown state flow"),
    "BASE3-RESET": ("reset 層級與影響範圍", "Reset levels and scope"),
    "BASE3-CAPACITY": ("capacity model", "Capacity model"),
    "BASE3-KEEPALIVE": ("Keep Alive timer", "Keep Alive timers"),
    "BASE3-FIRMWARE": ("firmware update 與 privileged action", "Firmware updates and privileged actions"),
    "BASE4-SQE": ("common SQE 配置", "Common SQE layout"),
    "BASE4-CID": ("CID 唯一性", "CID uniqueness"),
    "BASE4-PSDT": ("PRP／SGL 選擇", "PRP/SGL selection"),
    "BASE4-CQE": ("common CQE 與 Phase Tag", "Common CQE and Phase Tag"),
    "BASE4-STATUS": ("SCT、SC 與 DNR", "SCT, SC, and DNR"),
    "BASE4-PHASE": ("Completion Queue phase", "Completion Queue phase"),
    "BASE4-PRP": ("PRP alignment 與 page", "PRP alignment and pages"),
    "BASE4-SGL": ("SGL descriptor 與 length", "SGL descriptors and length"),
    "BASE4-FEATURE": ("Feature value 與 persistence", "Feature values and persistence"),
    "BASE4-IDENTIFIER": ("全域識別碼的範圍", "Scope of global identifiers"),
    "BASE4-LISTS": ("Controller／Namespace List", "Controller and Namespace Lists"),
    "BASE4-UTF8": ("UTF-8 輸入驗證", "UTF-8 input validation"),
    "BASEFWLOG-MODEL-DOMAIN": ("先找出 firmware 的共享邊界", "Start with the firmware-sharing boundary"),
    "BASEFWLOG-FW-RESET": ("需要 reset 的完整流程", "Complete reset-based flow"),
    "BASEFWLOG-FW-IMMEDIATE": ("立即 activation 不是背景工作", "Immediate activation is not background work"),
    "BASEFWLOG-FW-FAILURE": ("載入失敗與 fallback", "Load failure and fallback"),
            "BASEFWLOG-FW-SEQUENCE": ("update sequence 應以串行方式規劃", "Plan update sequences as serialized work"),
    "BASEFWLOG-FW-DISCARD": ("downloaded portions 何時失效", "When downloaded portions are discarded"),
    "BASEFWLOG-UUID-LIST": ("UUID List 的位置穩定性", "UUID List positional stability"),
    "BASEFWLOG-UUID-RESET": ("UUID 變更造成的 reset 邊界", "Reset boundary caused by UUID changes"),
    "BASEFWLOG-CAP-FR": ("FR：目前 active revision", "FR: currently active revision"),
    "BASEFWLOG-CAP-MDS-ULIST": ("MDS、DID 與 ULIST", "MDS, DID, and ULIST"),
    "BASEFWLOG-CAP-FRMW": ("FRMW：slot 與 activation 能力", "FRMW: slot and activation capabilities"),
    "BASEFWLOG-CAP-MTFA": ("MTFA：暫停 command processing 的時間", "MTFA: command-processing pause"),
    "BASEFWLOG-CAP-FWUG": ("FWUG：download granularity 與 alignment", "FWUG: download granularity and alignment"),
    "BASEFWLOG-CAP-MPTFAWR": ("MPTFAWR：立即 activation 的完成時間", "MPTFAWR: immediate-activation completion time"),
    "BASEFWLOG-COMMIT-PURPOSE": ("Firmware Commit 的真正作用", "What Firmware Commit actually does"),
    "BASEFWLOG-COMMIT-CDW10": ("CA 與 FS 的決策矩陣", "CA and FS decision matrix"),
    "BASEFWLOG-COMMIT-BOOT": ("Boot Partition cross-reference 邊界", "Boot Partition cross-reference boundary"),
    "BASEFWLOG-COMMIT-MUD": ("MUD：重疊 sequence 的證據", "MUD: evidence of overlapping sequences"),
    "BASEFWLOG-COMMIT-STATUS": ("status 決定下一個 recovery 動作", "Status selects the next recovery action"),
    "BASEFWLOG-DOWNLOAD-RANGE": ("portion 順序、overlap 與 FWUG", "Portion ordering, overlap, and FWUG"),
    "BASEFWLOG-DOWNLOAD-FIELDS": ("DPTR、NUMD、OFST 與實際 bytes", "DPTR, NUMD, OFST, and actual bytes"),
    "BASEFWLOG-LOG-COMMAND": ("LID 03h 的最小 command slice", "Minimum command slice for LID 03h"),
    "BASEFWLOG-LOG-LENGTH": ("512 bytes 的實際 command 計算", "Concrete command calculation for 512 bytes"),
    "BASEFWLOG-LOG-RAE": ("RAE 的事件副作用", "RAE event side effect"),
    "BASEFWLOG-LOG-OFFSET": ("完整讀取與 offset 邊界", "Full-read and offset boundary"),
    "BASEFWLOG-LOG-SCOPE": ("LID 03h 的 domain／subsystem scope", "Domain/subsystem scope of LID 03h"),
    "BASEFWLOG-LID03-DESCRIPTION": ("LID 03h 回答的問題", "What LID 03h answers"),
    "BASEFWLOG-LID03-AFI": ("AFI：current 與 next active slot", "AFI: current and next active slots"),
    "BASEFWLOG-LID03-FRS": ("FRS1-FRS7 與 reserved 區", "FRS1-FRS7 and reserved regions"),
    "BASEFWLOG-RESET-XREF": ("PCIe reset 名稱不能混用", "Do not conflate PCIe reset names"),
    "BASEFWLOG-XREF-337": ("Figure 337／338 交叉引用差異", "Figure 337/338 cross-reference discrepancy"),
    "BASEPOWER-READ-FIRST": ("先讀後寫：Feature 能力盤點", "Read before write: Feature capability inventory"),
    "BASEPOWER-GET-SELECT": ("SEL 與 FID", "SEL and FID"),
    "BASEPOWER-GET-SAVED": ("saved value fallback", "Saved-value fallback"),
    "BASEPOWER-GET-UIDX": ("UIDX 使用條件", "UIDX applicability"),
    "BASEPOWER-GET-CAP": ("CHANG／NSSPEC／SVBL", "CHANG/NSSPEC/SVBL"),
    "BASEPOWER-GET-STATUS": ("Get Features failure evidence", "Get Features failure evidence"),
    "BASEPOWER-SET-DPTR": ("Set Features data buffer", "Set Features data buffer"),
    "BASEPOWER-SET-SAVE": ("SV 與 saveability", "SV and saveability"),
    "BASEPOWER-SET-AFTER": ("成功後的切換邊界", "Post-success transition boundary"),
    "BASEPOWER-FID-SCOPE": ("五個 FID 的 scope／persistence", "Scope and persistence of the five FIDs"),
    "BASEPOWER-POWER-STATES": ("power state 編號與上限", "Power-state numbering and limits"),
    "BASEPOWER-POWER-METRICS": ("Power State Descriptor mental model", "Power State Descriptor mental model"),
    "BASEPOWER-TRANSITION": ("entry／exit latency 計算", "Entry/exit latency calculation"),
    "BASEPOWER-RELATIVE": ("relative performance 解讀", "Relative-performance interpretation"),
    "BASEPOWER-NONOP": ("non-operational 不等於關機", "Non-operational is not powered off"),
    "BASEPOWER-NONOP-IO": ("I/O 觸發 operational return", "I/O-triggered operational return"),
    "BASEPOWER-FID02": ("FID 02h：手動 power state", "FID 02h: manual power state"),
    "BASEPOWER-WORKLOAD": ("Workload Hint", "Workload Hint"),
    "BASEPOWER-RTD3": ("RTD3E／RTD3R 邊界", "RTD3E/RTD3R boundary"),
    "BASEPOWER-FID04": ("FID 04h：temperature threshold", "FID 04h: temperature threshold"),
    "BASEPOWER-HYST": ("temperature hysteresis", "Temperature hysteresis"),
    "BASEPOWER-FID0C": ("FID 0Ch：APST enable", "FID 0Ch: APST enable"),
    "BASEPOWER-APST-ENTRY": ("APST 256-byte table", "APST 256-byte table"),
    "BASEPOWER-APST-NOPPME": ("APSTE × NOPPME", "APSTE × NOPPME"),
    "BASEPOWER-FID10": ("FID 10h：TMT1／TMT2", "FID 10h: TMT1/TMT2"),
    "BASEPOWER-HCTM": ("HCTM control loop", "HCTM control loop"),
    "BASEPOWER-FID11": ("FID 11h：background power permission", "FID 11h: background-power permission"),
    "BASEPOWER-OBSERVE": ("SMART／Health 驗證閉環", "SMART/Health verification loop"),
    "BASEDIAGMEM-SELFTEST-GATE": ("先確認 self-test capability 與 concurrency scope", "Gate self-test capability and concurrency scope"),
    "BASEDIAGMEM-SELFTEST-NSID": ("NSID 決定測試涵蓋範圍", "NSID selects the test scope"),
    "BASEDIAGMEM-SELFTEST-STC": ("STC 與 CDW15 的命令編碼", "STC and CDW15 command encoding"),
    "BASEDIAGMEM-SELFTEST-INPROGRESS": ("已有 operation 時的狀態矩陣", "State matrix while an operation is active"),
    "BASEDIAGMEM-SELFTEST-COMPLETION": ("CQE 不等於測試完成", "A CQE is not test completion"),
    "BASEDIAGMEM-SELFTEST-BACKGROUND": ("背景測試的 suspend／resume 契約", "Background-test suspend/resume contract"),
    "BASEDIAGMEM-SELFTEST-TIMING": ("short 與 extended 的 reset 差異", "Reset differences between short and extended tests"),
    "BASEDIAGMEM-SELFTEST-ABORTS": ("Format、sanitize 與 abort 條件", "Format, sanitize, and abort conditions"),
    "BASEDIAGMEM-SELFTEST-LOG-COMMAND": ("564-byte LID 06h command 計算", "Constructing the 564-byte LID 06h command"),
    "BASEDIAGMEM-SELFTEST-CURRENT": ("current operation 與完成百分比", "Current operation and completion percentage"),
    "BASEDIAGMEM-SELFTEST-HISTORY": ("20 筆 newest-first result ring", "Twenty newest-first results"),
    "BASEDIAGMEM-SELFTEST-RESULT": ("DSTS 與 SEGN 的條件式解碼", "Conditional DSTS and SEGN decoding"),
    "BASEDIAGMEM-SELFTEST-VALIDITY": ("VDINFO 是四個獨立 validity gates", "VDINFO contains four independent validity gates"),
    "BASEDIAGMEM-SELFTEST-NVM-FLBA": ("NVM Command Set 補完 FLBA 語意", "NVM Command Set completes FLBA semantics"),
    "BASEDIAGMEM-SELFTEST-DEBUG": ("以三個時間點重建 self-test", "Reconstruct self-test across three timestamps"),
    "BASEDIAGMEM-HMB-CAPABILITY": ("HMB capability 與 descriptor limits", "HMB capability and descriptor limits"),
    "BASEDIAGMEM-HMB-OWNERSHIP": ("HMB 是 ownership transfer", "HMB is an ownership transfer"),
    "BASEDIAGMEM-HMB-SET-COMMAND": ("FID 0Dh 的 Set Features layout", "Set Features layout for FID 0Dh"),
    "BASEDIAGMEM-HMB-DESCRIPTORS": ("HMDL 與 descriptor page math", "HMDL and descriptor page math"),
    "BASEDIAGMEM-HMB-NUMERIC": ("256 KiB HMB 完整計算", "Complete 256-KiB HMB calculation"),
    "BASEDIAGMEM-HMB-SEQUENCE": ("enable／disable 的 completion fence", "Enable/disable completion fence"),
    "BASEDIAGMEM-HMB-GET": ("Get Features 分開讀 policy 與 state", "Get Features separates policy from state"),
    "BASEDIAGMEM-HMB-NONOP": ("HMNARE 與 HMNAR 不相同", "HMNARE and HMNAR are different"),
    "BASEDIAGMEM-HMB-RESET-RTD3": ("reset／RTD3 後的 Memory Return", "Memory Return after reset or RTD3"),
    "BASEDIAGMEM-HMB-SURPRISE": ("surprise removal 的資料正確性", "Data correctness during surprise removal"),
    "BASEDIAGMEM-DOORBELL-STRIDE": ("DSTRD encoding 到 cacheline stride", "DSTRD encoding to cacheline stride"),
    "BASEDIAGMEM-DOORBELL-DEBUG": ("emulator 的 doorbell 證據鏈", "Doorbell evidence chain for emulators"),
    "BASEDIAGMEM-VENDOR-GATE": ("Admin 與 I/O vendor format 分開 gate", "Gate Admin and I/O vendor formats independently"),
    "BASEDIAGMEM-VENDOR-FORMAT": ("Figure 94 的 boundary-safe layout", "Boundary-safe Figure 94 layout"),
    "BASEDIAGMEM-VENDOR-LENGTH": ("NDT／NDM 是實際 dword count", "NDT/NDM are actual dword counts"),
    "BASEDIAGMEM-BOUNDARY-DEBUG": ("從第一個 broken boundary 開始 Debug", "Debug from the first broken boundary"),
    "BASENSMGMT-SELFTEST-GATE": ("先確認 Self-test capability 與 concurrency scope", "Gate Self-test capability and concurrency scope"),
    "BASENSMGMT-SELFTEST-NSID": ("NSID 決定 Self-test 涵蓋範圍", "NSID selects Self-test scope"),
    "BASENSMGMT-SELFTEST-STC": ("STC 與 CDW15 的命令編碼", "STC and CDW15 command encoding"),
    "BASENSMGMT-SELFTEST-INPROGRESS": ("operation in progress 的命令矩陣", "Command matrix while an operation is active"),
    "BASENSMGMT-SELFTEST-COMPLETION": ("CQE 不等於背景測試完成", "A CQE is not background-test completion"),
    "BASENSMGMT-SELFTEST-BACKGROUND": ("背景測試的 suspend／resume 契約", "Background-test suspend/resume contract"),
    "BASENSMGMT-SELFTEST-TIMING": ("short 與 extended 的 reset 差異", "Reset differences between short and extended tests"),
    "BASENSMGMT-SELFTEST-ABORTS": ("Format、sanitize 與 abort 條件", "Format, sanitize, and abort conditions"),
    "BASENSMGMT-SELFTEST-LOG-COMMAND": ("564-byte LID 06h command 計算", "Constructing the 564-byte LID 06h command"),
    "BASENSMGMT-SELFTEST-CURRENT": ("current operation 與完成百分比", "Current operation and completion percentage"),
    "BASENSMGMT-SELFTEST-HISTORY": ("20 筆 newest-first result history", "Twenty newest-first result entries"),
    "BASENSMGMT-SELFTEST-VALIDITY": ("先驗證 validity bit 再讀欄位", "Validate the validity bit before the field"),
    "BASENSMGMT-SELFTEST-NVM-FLBA": ("NVM Command Set 補完 FLBA 語意", "NVM Command Set completes FLBA semantics"),
    "BASENSMGMT-CAPACITY-MODEL": ("NSZE、NCAP、NUSE 的容量不等式", "The NSZE, NCAP, NUSE capacity inequality"),
    "BASENSMGMT-THIN-PROVISIONING": ("THINP 決定 NCAP／NUSE 回報責任", "THINP governs NCAP/NUSE reporting"),
    "BASENSMGMT-NSMGMT-CAPABILITY": ("完整 capability 是 Manage 加 Attach", "The complete capability combines Manage and Attach"),
    "BASENSMGMT-NSID-LIFECYCLE": ("allocated、active、inactive、unallocated", "Allocated, active, inactive, and unallocated"),
    "BASENSMGMT-CREATE-PREFLIGHT": ("create 前的 capability／capacity 盤點", "Capability and capacity preflight before create"),
    "BASENSMGMT-CREATE-BASE-COMMAND": ("Base 4096-byte create envelope", "The Base 4096-byte create envelope"),
    "BASENSMGMT-CREATE-NVM-PAYLOAD": ("NVM host-specified create fields", "NVM host-specified create fields"),
    "BASENSMGMT-PROTECTION-VALIDATION": ("Protection Information 與 LBSTM gates", "Protection Information and LBSTM gates"),
    "BASENSMGMT-FDP-VALIDATION": ("FDP Placement Handle validation", "FDP Placement Handle validation"),
    "BASENSMGMT-GROUP-SELECTION": ("NVMSETID／ENDGID 決策矩陣", "NVMSETID/ENDGID decision matrix"),
    "BASENSMGMT-ALLOCATION-ROUNDING": ("requested size 不等於 capacity consumption", "Requested size need not equal capacity consumption"),
    "BASENSMGMT-GRANULARITY-HINTS": ("NSG／NCG 是配置提示而非合法性門檻", "NSG/NCG are allocation hints, not validity gates"),
    "BASENSMGMT-ATTACH-COMMAND": ("Controller List 建立 access relationship", "Controller List establishes access relationships"),
    "BASENSMGMT-ATTACH-LIMITS": ("MAXDNA 與 MAXCNA 是兩層 limits", "MAXDNA and MAXCNA are two levels of limits"),
    "BASENSMGMT-CREATE-COMPLETION": ("CQE.DW0 回 NSID，但尚未 attached", "CQE DW0 returns an NSID that is not yet attached"),
    "BASENSMGMT-DELETE": ("detach 後再 delete 的可控流程", "A controlled detach-then-delete flow"),
    "BASENSMGMT-RESTORE-DEFAULT": ("RDNCS、delete-all 與 DNCS", "RDNCS, delete-all, and DNCS"),
    "BASENSMGMT-COMMAND-STATUS": ("用 command-specific status 定位 failure gate", "Use command-specific status to locate the failed gate"),
    "BASENSMGMT-NAMESPACE-EVENTS": ("AER 後重新 Identify inventory", "Refresh Identify inventory after AER"),
    "BASENSMGMT-GRANULARITY-EXAMPLE": ("4 KiB LBA 的 NSG／NCG 計算", "NSG/NCG calculation with 4-KiB LBAs"),
    "BASENSMGMT-END-TO-END-DEBUG": ("從第一個生命週期邊界開始 Debug", "Debug from the first lifecycle boundary"),
    "PCIE14-SCOPE": ("Transport 與 Base 的優先序", "Transport and Base precedence"),
    "PCIE14-CONVENTION": ("PCIe Reset 欄定義", "PCIe Reset-column convention"),
    "PCIE14-KEYWORDS": ("Transport 規範性用語", "Transport normative language"),
    "PCIE14-OVERVIEW": ("PCIe transport 概觀", "PCIe transport overview"),
    "PCIE14-MMIO": ("BAR 與 register 存取", "BAR and register access"),
    "PCIE14-DOORBELL": ("SQ／CQ doorbell offset", "SQ/CQ doorbell offsets"),
    "PCIE14-QUEUE": ("queue 與 interrupt vector", "Queues and interrupt vectors"),
    "PCIE14-RESET": ("PCIe reset recovery", "PCIe reset recovery"),
    "PCIE14-COMMAND": ("PCIe command flow", "PCIe command flow"),
    "PCIE14-INTERRUPT": ("interrupt 模式與延遲", "Interrupt modes and delay"),
    "PCIE14-POWER": ("slot power limit", "Slot power limit"),
    "PCIE14-ERROR": ("NVMe 與 PCIe error 分層", "NVMe and PCIe error layers"),
    "PCIE14-CONFIG": ("PCI configuration requirements", "PCI configuration requirements"),
    "PCIE14-SECURITY": ("平台安全與隔離依賴", "Platform security and isolation dependencies"),
    "PCIE14-EOM": ("receiver eye measurement", "Receiver-eye measurement"),
    "PCIE14-HOST": ("host implementation checklist", "Host implementation checklist"),
}

def artifact_ids(report_id: str) -> list[str]:
    key = {
        "base-ch1-2": "base12",
        "base-ch3": "base3",
        "base-ch4": "base4",
        "base-admin-fw-logs": "basefwlog",
        "base-power-features": "basepower",
        "base-self-test-hmb-emulation": "basediagmem",
        "base-self-test-namespace-management": "basensmgmt",
        "pcie-transport-1.4": "pcie14",
    }[report_id]
    return [
        f"{key}-tutorial-html",
        f"{key}-detailed-html",
        f"{key}-zh-md",
        f"{key}-en-md",
    ]


def cite(item: dict, language: str, figure: int | None = None) -> str:
    source = item["source_id"]
    rev = SOURCES[source]["revision"]
    fig = f", Figure {figure}" if figure is not None else ""
    if language == "en":
        return (
            f"Source: {source}, Rev. {rev}, §{item['section']}{fig}, "
            f"printed pages {item['printed_pages']}, PDF pages {item['pdf_pages']}"
        )
    return (
        f"來源：{source}, Rev. {rev}, §{item['section']}{fig}, "
        f"文件頁 {item['printed_pages']}, PDF 頁 {item['pdf_pages']}"
    )


def figure_explanation(figure: dict, language: str) -> dict[str, str]:
    """Return a source-specific, non-verbatim guide for one Figure."""

    title = figure["title"]
    lower_title = title.lower()
    number = figure["number"]
    is_fwlog = figure.get("report_id") == "base-admin-fw-logs"
    is_power = figure.get("report_id") == "base-power-features"
    is_diagmem = figure.get("report_id") == "base-self-test-hmb-emulation"
    is_nsmgmt = figure.get("report_id") == "base-self-test-namespace-management"
    items = list(figure.get("key_items", []))
    item_text = ", ".join(items)
    first = items[0] if items else title
    keywords = list(figure.get("source_keywords", []))
    keyword_text = ", ".join(f"`{item}`" for item in keywords) or "none"

    offset = re.match(
        r"^Offset\s+([^:]+):\s*([A-Z0-9-]+)\s+-\s+(.+)$", title
    )
    dword = re.match(r"^(.+?)\s+-\s+Command Dword\s+([0-9-]+)$", title)
    second = (
        items[1]
        if len(items) > 1
        else ("the cited condition" if language == "en" else "引用條件")
    )

    if language == "en":
        if offset:
            location, symbol, name = offset.groups()
            purpose = (
                f"Defines {symbol} ({name}) at offset {location} and identifies "
                "the fields that software must decode at that location."
            )
            reading = (
                f"Start at {symbol}, then map bit ranges to access type, reset value, "
                f"and field meaning. Evidence index: {item_text}."
            )
            example = (
                f"Read {symbol} with the required width, then verify {first} and "
                f"{second} separately before using either value."
            )
        elif dword:
            command, index = dword.groups()
            purpose = (
                f"Defines command-specific fields in CDW{index} for {command}."
            )
            reading = (
                f"Locate CDW{index}, then decode the named fields without borrowing "
                f"semantics from another command. Evidence index: {item_text}."
            )
            example = (
                f"Build one {command} entry, set {first}, and independently validate "
                f"{second} before ringing the Submission Queue doorbell."
            )
        elif "family of specifications" in lower_title or "types of nvme command sets" in lower_title:
            purpose = f"Places {title} in the NVMe document and command-set hierarchy."
            reading = (
                "Read from the common Base requirements toward the transport and command-set layer; "
                f"keep these source-derived labels distinct: {item_text}."
            )
            example = (
                f"Start with {first}, then follow the branch containing {second}; cite the document "
                "that owns the requirement instead of assuming every layer defines it."
            )
        elif "decimal and binary units" in lower_title or "byte, word, and dword" in lower_title:
            purpose = f"Defines the numeric-unit or byte-width convention illustrated by {title}."
            reading = (
                f"Separate decimal units from binary units and preserve byte/word/Dword boundaries. Evidence index: {item_text}."
            )
            example = (
                f"Normalize one value using {first}, then verify its storage width against {second} before comparing it."
            )
        elif "support requirements" in lower_title:
            purpose = f"Summarizes the support levels assigned by {title}."
            reading = (
                f"Resolve the row and controller/command-set context before interpreting its support marker. Evidence index: {item_text}."
            )
            example = (
                f"Look up {first} in the applicable row, then confirm the context identified by {second} before labeling it required or optional."
            )
        elif "status code" in lower_title or "error" in lower_title:
            purpose = f"Defines the status/error classification represented by {title}."
            reading = (
                "Resolve the category before the individual code or flag; keep "
                f"reserved values uninterpreted. Evidence index: {item_text}."
            )
            example = (
                f"For one reported condition, identify {first} first and then check "
                f"{second} instead of decoding an isolated numeric value."
            )
        elif is_fwlog and "data pointer" in lower_title:
            purpose = f"Defines how {title} identifies the destination or source buffer for this command."
            reading = (
                f"Resolve pointer type and address before checking transfer length and alignment. Evidence index: {item_text}."
            )
            example = (
                f"Validate the pointer form represented by {first}, then confirm the boundary associated with {second} before starting the transfer."
            )
        elif is_fwlog and "log page" in lower_title:
            purpose = f"Defines the returned log-page layout and selection context for {title}."
            reading = (
                f"Start with the fixed header and scope, validate counts or lengths, then walk entries or data areas in order. Evidence index: {item_text}."
            )
            example = (
                f"Read {first} first, use {second} as an independent size or identity check, and stop before any unreturned byte."
            )
        elif is_fwlog and ("event" in lower_title or "logging requirements" in lower_title):
            purpose = f"Defines the event record, event taxonomy, or logging condition represented by {title}."
            reading = (
                f"Resolve event type and record length before decoding event-specific data. Evidence index: {item_text}."
            )
            example = (
                f"Identify {first}, validate the record boundary using {second}, and decode only the data defined for that event type."
            )
        elif is_fwlog and ("operation" in lower_title or "state machine" in lower_title):
            purpose = f"Defines the operation or state progression represented by {title}."
            reading = (
                f"Follow request, state, transition condition, and completion in order. Evidence index: {item_text}."
            )
            example = (
                f"Begin with {first}, move to the state associated with {second} only when the cited transition condition is satisfied."
            )
        elif is_fwlog and any(word in lower_title for word in (" types", " codes", " scale", " sensors")):
            purpose = f"Defines the enumerated values, measurement scale, or sensor selection represented by {title}."
            reading = (
                f"Resolve the selector or code first, then apply its unit, scale, or reserved-value rule. Evidence index: {item_text}."
            )
            example = (
                f"Decode {first}, then apply the interpretation selected by {second}; do not assign meaning to a reserved value."
            )
        elif any(word in lower_title for word in ("layout", "format", "definition", "descriptor", "field", "register", "values", "structure", "capabilit", "configuration space", "command dword")):
            purpose = f"Defines the concrete layout or value relationships for {title}."
            reading = (
                "Follow byte/bit order, length, access type, and reserved areas; "
                f"the source-derived evidence index is {item_text}."
            )
            example = (
                f"Use {first} as the first parser checkpoint and {second} as a second, "
                "independent boundary check."
            )
        elif any(word in lower_title for word in ("identifier", "controller ids", "nsid types", "serial number", "model number", "oui", "eui64", "nguid", "uuid", "wwn")):
            purpose = f"Defines the identifier composition or namespace of values shown by {title}."
            reading = (
                f"Keep the value width, issuing authority, uniqueness scope, and reserved values separate. Evidence index: {item_text}."
            )
            example = (
                f"Parse {first} at its defined width, then validate the scope associated with {second} before using it as an identity key."
            )
        elif "virtualization" in lower_title or "sr-iov" in lower_title:
            purpose = f"Shows the Physical Function and Virtual Function relationships in {title}."
            reading = (
                f"Separate PCIe Function identity, controller ownership, and shared device resources. Evidence index: {item_text}."
            )
            example = (
                f"Start at the function represented by {first}, then trace its relationship to {second} without treating shared resources as private."
            )
        elif "queue" in lower_title or "command processing" in lower_title or "phase tag" in lower_title:
            purpose = f"Shows the queue or command relationship expressed by {title}."
            reading = (
                "Trace ownership and direction from host to SQ, controller, and CQ; "
                f"keep the indexed elements distinct: {item_text}."
            )
            example = (
                f"Trace one command through Figure {number}, using {first} and "
                f"{second} as checkpoints for ownership or pointer movement."
            )
        elif any(word in lower_title for word in ("namespace", "subsystem", "domain", "nvm set", "endurance", "capacity", "controller types", "storage hierarchy", "logical view of non-volatile storage")):
            purpose = f"Shows the object or capacity relationships in {title}."
            reading = (
                "Separate logical identifiers from controllers, namespaces, ports, "
                f"and capacity containers. Evidence index: {item_text}."
            )
            example = (
                f"Choose one object labeled by {first} and trace its relationship to "
                f"{second} without treating an identifier as the object itself."
            )
        elif "arbitration" in lower_title:
            purpose = f"Shows how {title} selects work from competing Submission Queues."
            reading = (
                f"Track priority class, service order, and the point at which the arbiter selects the next command. Evidence index: {item_text}."
            )
            example = (
                f"Compare queues represented by {first} and {second}, then advance only the queue chosen by the stated arbitration rule."
            )
        elif any(word in lower_title for word in ("shutdown", "timeout", "after reset", "power state", "reset sequence", "initialization sequence")):
            purpose = f"Shows the state or timing progression represented by {title}."
            reading = (
                f"Follow the states or time bounds in arrow order and identify which actor observes each transition. Evidence index: {item_text}."
            )
            example = (
                f"Begin at {first}, record the transition that reaches {second}, and evaluate timeout or reset behavior only at the stated boundary."
            )
        elif "privileged action" in lower_title:
            purpose = f"Identifies the privileged-operation boundary illustrated by {title}."
            reading = (
                f"Separate the requesting command from the privilege or controller state that authorizes it. Evidence index: {item_text}."
            )
            example = (
                f"Check {first} first, then verify the authorization condition associated with {second} before issuing the operation."
            )
        elif any(word in lower_title for word in ("prp entry", "prp list", "sgl segment", "sgl data block", "sgl bit bucket", "sgl read example")):
            purpose = f"Shows how {title} maps a transfer onto host-memory locations."
            reading = (
                f"Follow address, length, page/segment boundaries, and the link to the next entry in order. Evidence index: {item_text}."
            )
            example = (
                f"Map a transfer beginning at {first}, then verify the boundary or next element identified by {second} before continuing."
            )
        elif any(word in lower_title for word in ("interrupt", "msi", "msi-x", "pin based")):
            purpose = f"Shows the interrupt delivery or masking relationship represented by {title}."
            reading = (
                f"Trace the vector/message source, mask state, and delivery destination separately. Evidence index: {item_text}."
            )
            example = (
                f"Select the source represented by {first}, then confirm the mask or vector condition represented by {second} before expecting delivery."
            )
        elif "transport protocol layers" in lower_title:
            purpose = f"Separates the responsibilities of the protocol layers in {title}."
            reading = (
                f"Read vertically by layer and horizontally by peer interaction; do not assign a transport rule to the Base layer. Evidence index: {item_text}."
            )
            example = (
                f"Start with {first}, follow the operation to {second}, and cite the layer that defines the observed behavior."
            )
        elif "utf-8" in lower_title:
            purpose = f"Shows the input-validation sequence required by {title}."
            reading = (
                f"Follow decoding, prohibited-code-point, and truncation checks in order. Evidence index: {item_text}."
            )
            example = (
                f"Validate {first} first and reject the input if the check associated with {second} fails before accepting the string."
            )
        elif "eye" in lower_title or "eve diagram" in lower_title or "eom" in lower_title or "lane" in lower_title:
            purpose = f"Shows the receiver-eye measurement information in {title}."
            reading = (
                "Confirm support and returned length before interpreting lane, "
                f"parameter, header, or descriptor data. Evidence index: {item_text}."
            )
            example = (
                f"Check that {first} is present, then parse {second} only when the "
                "returned structure is long enough."
            )
        elif is_power:
            purpose = f"Maps the power/thermal control relationship represented by {title}."
            reading = (
                f"Trace selector, state or threshold, transition condition, and observation evidence in order. "
                f"Source-derived checkpoints: {item_text}."
            )
            example = (
                f"Record {first} as raw input, validate {second} against the cited capability or state, "
                "then correlate completion time with temperature and I/O-latency evidence."
            )
        elif is_diagmem:
            purpose = f"Connects {title} to a self-test, host-memory, doorbell, or vendor-command engineering boundary."
            reading = (
                f"Resolve capability and owner first, decode {item_text}, then verify the completion, log, or memory-lifecycle evidence."
            )
            example = (
                f"Capture {first} as raw evidence, validate {second} against the cited section, and reject any state or byte range that crosses the declared boundary."
            )
        elif is_nsmgmt:
            purpose = f"Connects {title} to the Self-test evidence path or namespace lifecycle."
            reading = (
                f"Identify the object and lifecycle state, decode {item_text}, then verify the next transition with a CQE, log, event, or Identify snapshot."
            )
            example = (
                f"Capture {first} as raw input, validate {second} against the cited capability and state, then record the resulting lifecycle transition."
            )
        else:
            purpose = f"Explains the specific relationship or example named {title}."
            reading = (
                f"Use the source-derived elements {item_text} as checkpoints and "
                "apply only the conditions in the cited section."
            )
            example = (
                f"Create a review row for Figure {number}, verify {first}, then verify "
                f"{second} against the cited section."
            )
        caveat = (
            f"Source keyword index: {keyword_text}. The index locates normative "
            "language but does not replace the condition attached to each field."
            if keywords
            else "The Figure is explanatory or structural; this guide does not turn its visual relationship into a new requirement."
        )
    else:
        if offset:
            location, symbol, name = offset.groups()
            purpose = (
                f"定義 offset {location} 的 {symbol}（{name}），並指出軟體在該位置"
                "必須分別解碼的欄位。"
            )
            reading = (
                f"先定位 {symbol}，再把 bit range 對到 access type、reset value 與欄位"
                f"語意；來源欄位索引：{item_text}。"
            )
            example = (
                f"依規定寬度讀取 {symbol}，先獨立驗證 {first}，再驗證 {second}，"
                "確認後才使用欄位值。"
            )
        elif dword:
            command, index = dword.groups()
            purpose = f"定義 {command} 在 CDW{index} 的 command-specific 欄位。"
            reading = (
                f"先定位 CDW{index}，再依本命令定義解碼，不借用其他 command 的語意；"
                f"來源欄位索引：{item_text}。"
            )
            example = (
                f"建立一筆 {command}，設定 {first} 後再獨立驗證 {second}，確認完成才"
                "更新 Submission Queue doorbell。"
            )
        elif "family of specifications" in lower_title or "types of nvme command sets" in lower_title:
            purpose = f"定位〈{title}〉在 NVMe 文件與 command set 階層中的位置。"
            reading = (
                f"由共通 Base 要求往 transport 與 command set 分支閱讀，並分開核對：{item_text}。"
            )
            example = (
                f"先從 {first} 出發，再沿包含 {second} 的分支找定義來源，不假設每一層都重複定義同一要求。"
            )
        elif "decimal and binary units" in lower_title or "byte, word, and dword" in lower_title:
            purpose = f"定義〈{title}〉使用的數值單位或 byte 寬度慣例。"
            reading = (
                f"分開十進位與二進位單位，並保留 byte／word／Dword 邊界；來源索引：{item_text}。"
            )
            example = (
                f"先依 {first} 正規化一個數值，再用 {second} 核對儲存寬度後才進行比較。"
            )
        elif "support requirements" in lower_title:
            purpose = f"統整〈{title}〉指定的支援等級。"
            reading = (
                f"先確認 row 與 controller／command-set 上下文，再解讀 support marker；來源索引：{item_text}。"
            )
            example = (
                f"先在適用 row 查找 {first}，再核對 {second} 所代表的上下文，最後才判斷必須或選用。"
            )
        elif "status code" in lower_title or "error" in lower_title:
            purpose = f"定義〈{title}〉所表示的 status／error 分類。"
            reading = (
                f"先判斷類別，再解個別 code 或 flag；保留值不自行賦義。來源欄位索引：{item_text}。"
            )
            example = (
                f"收到一筆狀態時先辨認 {first}，再檢查 {second}，不可脫離類別單看數值。"
            )
        elif is_fwlog and "data pointer" in lower_title:
            purpose = f"定義〈{title}〉如何指出本命令的來源或目的 buffer。"
            reading = (
                f"先判斷 pointer type 與 address，再核對 transfer length 和 alignment；來源欄位索引：{item_text}。"
            )
            example = (
                f"先驗證 {first} 所代表的 pointer 形式，再核對 {second} 對應的邊界，通過後才開始 transfer。"
            )
        elif is_fwlog and "log page" in lower_title:
            purpose = f"定義〈{title}〉的回傳配置與 selector／scope 上下文。"
            reading = (
                f"先讀固定 header 與 scope，驗證 count／length 後，再依序走訪 entry 或 data area；來源欄位索引：{item_text}。"
            )
            example = (
                f"先讀 {first}，再以 {second} 作為獨立的大小或 identity 檢查點，且不得解析超過實際回傳的 byte。"
            )
        elif is_fwlog and ("event" in lower_title or "logging requirements" in lower_title):
            purpose = f"定義〈{title}〉所表示的 event record、event 分類或記錄條件。"
            reading = (
                f"先判斷 Event Type 與 record length，再解 event-specific data；來源欄位索引：{item_text}。"
            )
            example = (
                f"先辨認 {first}，以 {second} 驗證 record 邊界，再只解析該 Event Type 定義的資料。"
            )
        elif is_fwlog and ("operation" in lower_title or "state machine" in lower_title):
            purpose = f"定義〈{title}〉所表示的 operation 或 state progression。"
            reading = (
                f"依序追蹤 request、state、transition condition 與 completion；來源欄位索引：{item_text}。"
            )
            example = (
                f"從 {first} 開始，只有在引用條文的 transition condition 成立時，才移到 {second} 所對應的 state。"
            )
        elif is_fwlog and any(word in lower_title for word in (" types", " codes", " scale", " sensors")):
            purpose = f"定義〈{title}〉中的列舉值、measurement scale 或 sensor selector。"
            reading = (
                f"先解 selector／code，再套用對應 unit、scale 或 reserved-value rule；來源欄位索引：{item_text}。"
            )
            example = (
                f"先解碼 {first}，再套用 {second} 選定的解讀方式；保留值不得自行賦義。"
            )
        elif any(word in lower_title for word in ("layout", "format", "definition", "descriptor", "field", "register", "values", "structure", "capabilit", "configuration space", "command dword")):
            purpose = f"定義〈{title}〉的實際配置或數值關係。"
            reading = (
                f"依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：{item_text}。"
            )
            example = (
                f"以 {first} 作為 parser 的第一個檢查點，再用 {second} 獨立檢查另一個邊界。"
            )
        elif any(word in lower_title for word in ("identifier", "controller ids", "nsid types", "serial number", "model number", "oui", "eui64", "nguid", "uuid", "wwn")):
            purpose = f"定義〈{title}〉的識別碼組成或數值空間。"
            reading = (
                f"分開數值寬度、核發來源、唯一性範圍與保留值；來源索引：{item_text}。"
            )
            example = (
                f"依定義寬度解析 {first}，再核對 {second} 的唯一性範圍後才把它當成 identity key。"
            )
        elif "virtualization" in lower_title or "sr-iov" in lower_title:
            purpose = f"呈現〈{title}〉中 Physical Function 與 Virtual Function 的關係。"
            reading = (
                f"分開 PCIe Function identity、controller ownership 與 shared device resource；來源索引：{item_text}。"
            )
            example = (
                f"從 {first} 所代表的 Function 出發，再追到 {second}，不要把 shared resource 誤當成 private resource。"
            )
        elif "queue" in lower_title or "command processing" in lower_title or "phase tag" in lower_title:
            purpose = f"呈現〈{title}〉中的 queue 或 command 關係。"
            reading = (
                f"沿 host、SQ、controller、CQ 的擁有者與方向閱讀，並分開追蹤：{item_text}。"
            )
            example = (
                f"沿 Figure {number} 追蹤一筆 command，以 {first} 與 {second} 作為擁有者或 pointer 變動檢查點。"
            )
        elif any(word in lower_title for word in ("namespace", "subsystem", "domain", "nvm set", "endurance", "capacity", "controller types", "storage hierarchy", "logical view of non-volatile storage")):
            purpose = f"呈現〈{title}〉中的物件或容量關係。"
            reading = (
                f"將邏輯 identifier、controller、namespace、port 與容量容器分開；來源索引：{item_text}。"
            )
            example = (
                f"選擇 {first} 標示的一個物件，再追到 {second}，過程中不把 identifier 當成物件本身。"
            )
        elif "arbitration" in lower_title:
            purpose = f"呈現〈{title}〉如何在多個 Submission Queue 間選擇工作。"
            reading = (
                f"分別追蹤 priority class、服務順序與 arbiter 選出下一筆 command 的時點；來源索引：{item_text}。"
            )
            example = (
                f"比較 {first} 與 {second} 所代表的 queue，再只推進由規定 arbitration rule 選中的 queue。"
            )
        elif any(word in lower_title for word in ("shutdown", "timeout", "after reset", "power state", "reset sequence", "initialization sequence")):
            purpose = f"呈現〈{title}〉的狀態或時間推進關係。"
            reading = (
                f"依箭頭順序追蹤 state 或 time bound，並標出每個 transition 的觀察者；來源索引：{item_text}。"
            )
            example = (
                f"從 {first} 開始，記錄到達 {second} 的 transition，只在規定邊界判斷 timeout 或 reset 行為。"
            )
        elif "privileged action" in lower_title:
            purpose = f"界定〈{title}〉所示的 privileged operation 邊界。"
            reading = (
                f"分開發出 command 的主體，以及授權該操作的 privilege／controller state；來源索引：{item_text}。"
            )
            example = (
                f"先核對 {first}，再確認 {second} 對應的授權條件成立後才發出操作。"
            )
        elif any(word in lower_title for word in ("prp entry", "prp list", "sgl segment", "sgl data block", "sgl bit bucket", "sgl read example")):
            purpose = f"呈現〈{title}〉如何把 transfer 對映到 host memory。"
            reading = (
                f"依序追蹤 address、length、page／segment boundary 與下一個 entry 的連結；來源索引：{item_text}。"
            )
            example = (
                f"從 {first} 所示位置開始對映 transfer，再核對 {second} 的邊界或下一個元素後才繼續。"
            )
        elif any(word in lower_title for word in ("interrupt", "msi", "msi-x", "pin based")):
            purpose = f"呈現〈{title}〉中的 interrupt 傳遞或 masking 關係。"
            reading = (
                f"分開追蹤 vector／message 來源、mask 狀態與傳遞目的端；來源索引：{item_text}。"
            )
            example = (
                f"選定 {first} 所代表的來源，再確認 {second} 對應的 mask 或 vector 條件後才預期 interrupt 送達。"
            )
        elif "transport protocol layers" in lower_title:
            purpose = f"分開〈{title}〉中各 protocol layer 的責任。"
            reading = (
                f"垂直按 layer、水平按 peer interaction 閱讀，不把 transport rule 歸到 Base layer；來源索引：{item_text}。"
            )
            example = (
                f"先從 {first} 出發，再沿操作追到 {second}，最後引用真正定義該行為的 layer。"
            )
        elif "utf-8" in lower_title:
            purpose = f"呈現〈{title}〉要求的輸入驗證順序。"
            reading = (
                f"依序執行 decoding、禁止 code point 與 truncation 檢查；來源索引：{item_text}。"
            )
            example = (
                f"先驗證 {first}；若 {second} 對應的檢查失敗，就在接受字串前拒絕輸入。"
            )
        elif "eye" in lower_title or "eve diagram" in lower_title or "eom" in lower_title or "lane" in lower_title:
            purpose = f"呈現〈{title}〉中的 receiver-eye measurement 資訊。"
            reading = (
                f"先確認支援與回傳長度，再解 lane、parameter、header 或 descriptor；來源索引：{item_text}。"
            )
            example = (
                f"先確認 {first} 已存在，只有在回傳結構長度足夠時才繼續解析 {second}。"
            )
        elif is_power:
            purpose = f"呈現〈{title}〉所描述的 power／thermal 控制關係。"
            reading = (
                f"依序追蹤 selector、state 或 threshold、transition condition 與觀測證據；"
                f"來源欄位索引：{item_text}。"
            )
            example = (
                f"保存 {first} 的 raw input，先用引用 capability／state 驗證 {second}，再把 completion time "
                "與 temperature、I/O latency 證據放在同一條 timeline。"
            )
        elif is_diagmem:
            purpose = f"把〈{title}〉連到 self-test、host memory、doorbell 或 vendor command 的工程邊界。"
            reading = (
                f"先辨認 capability 與 owner，再解碼 {item_text}，最後以 completion、log 或 memory lifecycle 證據核對。"
            )
            example = (
                f"保存 {first} 的 raw evidence，依引用 section 驗證 {second}，若 state 或 byte range 超出宣告邊界就拒絕繼續。"
            )
        elif is_nsmgmt:
            purpose = f"把〈{title}〉連到 Self-test 證據路徑或 namespace lifecycle。"
            reading = (
                f"先確認物件與 lifecycle state，再解碼 {item_text}，最後以 CQE、log、event 或 Identify snapshot 驗證下一個 transition。"
            )
            example = (
                f"保存 {first} 的 raw input，依 capability 與目前 state 驗證 {second}，再記錄實際發生的 lifecycle transition。"
            )
        else:
            purpose = f"解釋〈{title}〉所指的特定關係或範例。"
            reading = (
                f"以 PDF 擷取出的 {item_text} 作為核對點，只套用引用 section 明載的條件。"
            )
            example = (
                f"為 Figure {number} 建立檢查列，先核對 {first}，再依引用 section 核對 {second}。"
            )
        caveat = (
            f"來源 keyword 索引：{keyword_text}。索引用來定位規範性語句，不取代各欄位所附的完整條件。"
            if keywords
            else "這張 Figure 主要提供結構或說明；本導讀不把圖示關係提升為新的規格要求。"
        )

    if figure.get("mode") == "scope-reduced" or figure.get("scope_reduced"):
        caveat += (
            " Only the PCIe/memory-based portion is in scope."
            if language == "en"
            else " 本報告只解釋 PCIe／memory-based 部分。"
        )
    focus = figure.get("dependency_focus")
    if figure.get("role") == "referenced_dependency":
        references = ", ".join(f"§{item}" for item in figure.get("referenced_from", []))
        if language == "en":
            caveat += (
                f" This Figure is a dependency referenced from {references}; only the "
                "elements needed by the requested sections are taught here."
            )
            if focus:
                caveat += " " + focus["en"]
        else:
            caveat += (
                f" 這是 {references} 直接引用的範圍外相依 Figure；此處只教學指定章節需要的元素。"
            )
            if focus:
                caveat += " " + focus["zh_tw"]
    if "Eve Diagram" in title:
        caveat += (
            ' The source caption spells "Eve"; the section context identifies a receiver eye. The caption is preserved for traceability.'
            if language == "en"
            else " 原始 Figure caption 使用「Eve」；section 上下文說明的是 receiver eye。此處保留原 caption 以利追溯。"
        )
    return {
        "purpose": purpose,
        "reading": reading,
        "example": example,
        "caveat": caveat,
        "keyword_text": keyword_text,
        "item_text": item_text,
    }


def flow_svg(report: dict) -> str:
    boxes = []
    arrows = []
    labels = list(report["diagram"])[:4]
    role_order = ["command", "object", "decision", "success"]
    for index, label in enumerate(labels):
        x = 20 + index * 200
        role = role_order[index]
        boxes.append(
            f'<rect class="{visual_role_class(role)}" x="{x}" y="35" width="170" height="88" rx="10"/>'
            f'<text class="v-role" x="{x + 85}" y="57" text-anchor="middle">{visual_role_label(role, "zh")}</text>'
            + svg_text_block(label, x + 85, 91, limit=16, max_lines=2)
        )
        if index < len(labels) - 1:
            arrows.append(
                f'<line class="v-line" x1="{x + 170}" y1="79" x2="{x + 190}" y2="79" '
                'marker-end="url(#arrow)"/>'
            )
    return (
        '<svg class="flow-svg" viewBox="0 0 820 158" role="img" data-visual-kind="sequence" '
        'aria-labelledby="flow-title flow-desc">'
        '<title id="flow-title">NVMe report flow</title>'
        f'<desc id="flow-desc">{html.escape(report["diagram_note_zh"])}</desc>'
        '<defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="6" '
        'refY="3" orient="auto"><path d="M0,0 L0,6 L7,3 z" class="v-arrow"/>'
        '</marker></defs>'
        + "".join(arrows + boxes)
        + "</svg>"
    )


def make_claim(report_id: str, report: dict, item: dict) -> dict:
    claim_id = f"{report['prefix']}-{item['key']}"
    result = {
        "id": claim_id,
        "report_id": report_id,
        "source_id": item["source_id"],
        "revision": SOURCES[item["source_id"]]["revision"],
        "section": item["section"],
        "figure": None,
        "table": None,
        "printed_pages": item["printed_pages"],
        "pdf_pages": item["pdf_pages"],
        "normative_keyword": item["normative_keyword"],
        "zh_tw": item["zh_tw"],
        "en": item["en"],
        "scope_entry_id": item.get("scope_entry_id") or report["scope_entry"],
        "heading_zh_tw": CORE_TITLES[claim_id][0],
        "heading_en": CORE_TITLES[claim_id][1],
    }
    result["citation_zh_tw"] = cite(result, "zh")
    result["citation_en"] = cite(result, "en")
    return result


def make_figure_claim(report_id: str, report: dict, figure: dict) -> dict:
    figure_id = f"{report['prefix']}-FIG-{int(figure['number']):03d}"
    zh_parts = figure_explanation(figure, "zh")
    en_parts = figure_explanation(figure, "en")
    result = {
        "id": f"{figure_id}-CLAIM",
        "report_id": report_id,
        "source_id": figure["source_id"],
        "revision": SOURCES[figure["source_id"]]["revision"],
        "section": figure["section"],
        "figure": str(figure["number"]),
        "table": None,
        "printed_pages": figure["printed_pages"],
        "pdf_pages": figure["pdf_pages"],
        "normative_keyword": "none",
        "zh_tw": (
            f"Figure {figure['number']}〈{figure['title']}〉："
            f"{zh_parts['purpose']} {zh_parts['reading']}"
        ),
        "en": (
            f"Figure {figure['number']}, \"{figure['title']}\": "
            f"{en_parts['purpose']} {en_parts['reading']}"
        ),
        "scope_entry_id": figure["scope_entry_id"],
        "source_keywords": list(figure.get("source_keywords", [])),
        "key_items": list(figure.get("key_items", [])),
        "evidence_digest": figure.get("evidence_digest", ""),
    }
    result["citation_zh_tw"] = cite(result, "zh", int(figure["number"]))
    result["citation_en"] = cite(result, "en", int(figure["number"]))
    return result


def tutorial_check(report_id: str, claim_id: str) -> str:
    if any(key in claim_id for key in ("KEYWORD", "NUMBER", "DWORD")):
        return "先圈出 keyword、進位、單位與 bit／byte 編號，再開始解讀句子或欄位。"
    if any(key in claim_id for key in ("QUEUE", "COMMAND", "ORDER", "PROCESS")):
        return "畫出 host → SQ → controller → CQ，並在每一步標上由誰更新 pointer。"
    if any(key in claim_id for key in ("STORAGE", "SUBSYSTEM", "NAMESPACE", "MEDIA", "DOMAIN", "CAPACITY")):
        return "把 identifier 與實體／邏輯物件分開，再由 namespace 往上追到所屬容量階層。"
    if any(key in claim_id for key in ("INIT", "SHUTDOWN", "RESET", "STATIC")):
        return "先寫出目前 controller state，再核對哪個 register／property 觸發狀態轉換。"
    if any(key in claim_id for key in ("SQE", "CQE", "STATUS", "PHASE", "CID", "PSDT")):
        return "先定位 dword 與 bit 範圍，再決定這個欄位用於識別、資料指標或完成狀態。"
    if any(key in claim_id for key in ("PRP", "SGL", "LIST", "IDENTIFIER", "UTF8")):
        return "先驗證長度、alignment、type 與保留值，再沿 pointer 或 entry 順序解析。"
    if any(key in claim_id for key in ("MMIO", "DOORBELL", "CONFIG", "INTERRUPT", "PCIE14-POWER", "EOM")):
        return "先分辨欄位位於 PCI configuration space、MMIO register、host memory 或 log page。"
    if any(key in claim_id for key in ("GET-", "SET-", "FID", "APST", "HCTM", "HYST", "NONOP", "TRANSITION", "WORKLOAD", "OBSERVE")):
        return "先讀 capability 與目前值，再標出 command bit、單位、轉換條件、completion 與觀測證據。"
    if any(key in claim_id for key in ("FW-", "COMMIT", "DOWNLOAD", "UUID")):
        return "把 image portion、firmware slot、Commit Action 與 activation 所需 reset 分成四欄逐項核對。"
    if "LOG-" in claim_id:
        return "先用 LID 決定資料 scope，再核對 transfer length、offset type、RAE 與 log-specific header。"
    if any(key in claim_id for key in ("SELFTEST", "HMB-", "VENDOR-", "BOUNDARY-")):
        return "先找 capability gate 與 ownership／state boundary，再核對 encoded value、completion fence 與可觀測證據。"
    if any(key in claim_id for key in ("NSMGMT", "NSID-LIFECYCLE", "CREATE-", "ATTACH-", "DELETE", "RESTORE", "CAPACITY-MODEL", "THIN-PROVISIONING", "GRANULARITY", "GROUP-SELECTION", "PROTECTION", "FDP-")):
        return "先標出 namespace 的 allocated／attached state，再核對 capability、容量、command buffer、CQE／AER 與重新 Identify 的證據。"
    return {
        "base-ch1-2": "先確認概念位於規格家族、儲存階層或路徑層級，不把不同層級合併。",
        "base-ch3": "先寫清楚動作主體是 host 或 controller，再核對當下 lifecycle state。",
        "base-ch4": "先定位資料結構的 byte／dword 邊界，再閱讀欄位條件。",
        "base-admin-fw-logs": "先判斷目前位於 download、commit、activation 或 log verification 階段。",
        "base-power-features": "先分辨這一層是在描述 capability、host policy、controller state，還是觀測證據。",
        "base-self-test-hmb-emulation": "先判斷目前處理的是 background operation、host-memory ownership，或 encoded memory boundary。",
        "base-self-test-namespace-management": "先判斷目前處理的是 diagnostic operation、namespace object state，或 controller access relationship。",
        "pcie-transport-1.4": "先找 Base 的通用規則，再疊加 PCIe Transport 的專屬限制。",
    }[report_id]


def section_group(section: str) -> str:
    if section.lower().startswith("annex"):
        return section
    pieces = section.split(".")
    return ".".join(pieces[:2]) if len(pieces) > 1 else pieces[0]


def figure_group(figure: dict) -> str:
    if figure.get("role") == "referenced_dependency":
        return "dependency"
    return section_group(str(figure["section"]))


def figure_group_label(group: str, language: str) -> str:
    if group == "dependency":
        return (
            "Referenced Figure dependencies (outside the main section range)"
            if language == "en"
            else "引用相依 Figure（位於主章節範圍外）"
        )
    return f"§{group}"


def anchor(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def module_flow_svg(module: dict, language: str) -> str:
    nodes = module["nodes"][language]
    width = 820
    row_height = 82
    height = 26 + len(nodes) * row_height
    arrow_id = "module-arrow-" + anchor(module["id"])
    elements = [
        f'<defs><marker id="{arrow_id}" markerWidth="8" markerHeight="8" '
        'refX="7" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" '
        'class="v-arrow"/></marker></defs>'
    ]
    for index in range(len(nodes) - 1):
        y = 12 + index * row_height
        elements.append(
            f'<line class="v-line" x1="410" y1="{y + 58}" x2="410" '
            f'y2="{y + 76}" marker-end="url(#{arrow_id})"/>'
        )
    for index, label in enumerate(nodes):
        y = 12 + index * row_height
        role = visual_role(label)
        klass = visual_role_class(role)
        elements.append(
            f'<rect class="{klass}" x="90" y="{y}" width="640" height="58" rx="10"/>'
            f'<text class="v-role" x="112" y="{y + 22}">{visual_role_label(role, language)}</text>'
            + svg_text_block(label, 410, y + 38, limit=52, max_lines=1)
        )
    title = module["title"][language]
    return (
        f'<svg class="flow-svg" viewBox="0 0 {width} {height}" role="img" data-visual-kind="sequence" '
        f'aria-label="{html.escape(title)}"><title>{html.escape(title)}</title>'
        f'<desc>{html.escape(" → ".join(nodes))}</desc>{"".join(elements)}</svg>'
    )


def svg_label(value: str, limit: int = 28) -> str:
    clean = re.sub(r"\s+", " ", str(value)).strip()
    return clean if len(clean) <= limit else clean[: limit - 1] + "…"


def svg_label_lines(value: str, limit: int = 16, max_lines: int = 2) -> list[str]:
    """Wrap an SVG label without allowing connector lines to cross its text."""
    clean = re.sub(r"\s+", " ", str(value)).strip()
    if not clean:
        return [""]
    raw_tokens = clean.split(" ")
    tokens: list[str] = []
    for token in raw_tokens:
        if len(token) <= limit:
            tokens.append(token)
        else:
            tokens.extend(token[index : index + limit] for index in range(0, len(token), limit))
    lines: list[str] = []
    current = ""
    for token in tokens:
        candidate = token if not current else current + " " + token
        if len(candidate) <= limit:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = token
    if current:
        lines.append(current)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        lines[-1] = svg_label(lines[-1], max(4, limit - 1))
    return lines


def svg_text_block(
    value: str,
    x: float,
    y: float,
    *,
    klass: str = "v-label",
    limit: int = 16,
    max_lines: int = 2,
    line_height: int = 17,
) -> str:
    lines = svg_label_lines(value, limit, max_lines)
    start_y = y - ((len(lines) - 1) * line_height / 2)
    tspans = "".join(
        f'<tspan x="{x:g}" y="{start_y + index * line_height:g}">{html.escape(line)}</tspan>'
        for index, line in enumerate(lines)
    )
    return f'<text class="{klass}" x="{x:g}" y="{y:g}" text-anchor="middle">{tspans}</text>'


def visual_role(value: str) -> str:
    lower = str(value).lower()
    if any(word in lower for word in ("failure", "error", "invalid", "timeout", "abort", "stop", "reserved", "失敗", "錯誤", "無效", "逾時", "中止", "停止", "保留")):
        return "failure"
    if any(word in lower for word in ("evidence", "verify", "completion", "cqe", "result", "observe", "log", "trace", "證據", "驗證", "完成", "結果", "觀察", "紀錄")):
        return "success"
    if any(word in lower for word in ("capability", "support", "identify", "select", "gate", "threshold", "condition", "能力", "支援", "辨識", "選", "條件", "門檻")):
        return "decision"
    if any(word in lower for word in ("command", "host", "submit", "write", "read", "get ", "set ", "sqe", "送出", "提交", "寫", "讀", "命令")):
        return "command"
    return "object"


def visual_role_label(role: str, language: str) -> str:
    labels = {
        "command": {"zh": "REQUEST／INPUT", "en": "REQUEST / INPUT"},
        "object": {"zh": "OBJECT／STATE", "en": "OBJECT / STATE"},
        "decision": {"zh": "GATE／RULE", "en": "GATE / RULE"},
        "success": {"zh": "VALID／EVIDENCE", "en": "VALID / EVIDENCE"},
        "failure": {"zh": "WARNING／FAILURE", "en": "WARNING / FAILURE"},
    }
    return labels[role][language]


def visual_role_class(role: str) -> str:
    return {
        "command": "v-command",
        "object": "v-object",
        "decision": "v-decision",
        "success": "v-success",
        "failure": "v-failure",
    }[role]


def module_visual_kind(module_id: str) -> str:
    if module_id in {
        "queues", "queue-arbitration", "command", "interrupts",
        "feature-read-set-loop", "end-to-end-debug", "namespace-end-to-end-debug", "namespace-events",
    }:
        return "sequence"
    if module_id in {
        "numbers", "sqe", "cqe-status", "prp", "sgl", "identity-text",
        "mmio-doorbell", "config-error", "eom", "fw-download-geometry",
        "fw-lid03-proof", "selftest-observe-debug", "hmb-command-math",
        "encoded-boundary-safety", "namespace-create-payload", "capacity-granularity-math",
    }:
        return "decode"
    if module_id in {
        "lifecycle", "properties-init", "fw-commit-state", "apst-state-machine",
        "temperature-event-loop", "hctm-control-loop",
        "selftest-command-state-machine", "hmb-ownership-lifecycle", "hmb-reset-power",
        "namespace-lifecycle", "delete-restore-state",
    }:
        return "state"
    return "architecture"


def module_visual_svg(module: dict, language: str) -> str:
    """Return a relationship-specific view with routed connectors and semantic roles."""
    nodes = list(module["nodes"][language])[:6]
    kind = module_visual_kind(module["id"])
    title = module["title"][language]
    arrow_id = "atlas-arrow-" + anchor(module["id"])
    failure_arrow_id = arrow_id + "-failure"
    visual_height = 360 if kind == "decode" else 330
    head = (
        f'<svg viewBox="0 0 820 {visual_height}" role="img" data-visual-kind="{kind}" aria-label="{html.escape(title)}">'
        f'<title>{html.escape(title)}</title><desc>{html.escape(kind + ": " + " → ".join(nodes))}</desc>'
        f'<defs><marker id="{arrow_id}" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto">'
        '<path d="M0,0 L0,6 L9,3 z" class="v-arrow"/></marker>'
        f'<marker id="{failure_arrow_id}" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto">'
        '<path d="M0,0 L0,6 L9,3 z" class="v-arrow-failure"/></marker></defs>'
    )
    body: list[str] = []
    if kind == "sequence":
        lane_labels = (
            ["Host／software", "Shared object／buffer", "Controller／evidence"]
            if language == "zh"
            else ["Host / software", "Shared object / buffer", "Controller / evidence"]
        )
        xs = [130, 410, 690]
        for x in xs:
            body.append(f'<line class="v-line-soft" stroke-dasharray="6 6" x1="{x}" y1="62" x2="{x}" y2="315"/>')
        pairs = [(0, 1), (1, 2), (2, 1), (1, 0), (0, 2), (2, 0)]
        for index, label in enumerate(nodes):
            source, target = pairs[index]
            y = 92 + index * 42
            middle = (xs[source] + xs[target]) / 2
            label_width = min(240, max(100, abs(xs[source] - xs[target]) - 30))
            body.append(
                f'<line class="v-line" x1="{xs[source]}" y1="{y}" x2="{xs[target]}" y2="{y}" '
                f'marker-end="url(#{arrow_id})"/>'
            )
            body.append(f'<rect class="v-label-bg" x="{middle - label_width / 2}" y="{y - 22}" width="{label_width}" height="18" rx="4"/>')
            body.append(svg_text_block(label, middle, y - 9, klass="v-small", limit=30, max_lines=1, line_height=14))
        lane_classes = ["v-command", "v-object", "v-object"]
        lane_roles = (["HOST", "SHARED OBJECT", "CONTROLLER"] if language == "en" else ["HOST", "SHARED OBJECT", "CONTROLLER"])
        for x, label, klass, role in zip(xs, lane_labels, lane_classes, lane_roles):
            body.append(f'<rect class="{klass}" x="{x - 105}" y="18" width="210" height="40" rx="10"/>')
            body.append(f'<text class="v-role" x="{x - 94}" y="33">{role}</text>')
            body.append(svg_text_block(label, x, 45, limit=24, max_lines=1))
    elif kind == "decode":
        stage_labels = (
            ["RAW／輸入", "LOCATE／邊界", "DECODE／規則", "VALIDATE／條件", "APPLY／建構", "EVIDENCE／結果"]
            if language == "zh"
            else ["RAW / input", "LOCATE / boundary", "DECODE / rule", "VALIDATE / gate", "APPLY / build", "EVIDENCE / result"]
        )
        shown = nodes[:6]
        while len(shown) < 6:
            shown.append(stage_labels[len(shown)])
        positions = [(35, 45), (310, 45), (585, 45), (585, 190), (310, 190), (35, 190)]
        role_order = ["command", "object", "decision", "decision", "command", "success"]
        for (x1, y1), (x2, y2) in zip(positions, positions[1:]):
            if y1 == y2 and x2 > x1:
                body.append(f'<line class="v-line" x1="{x1 + 200}" y1="{y1 + 48}" x2="{x2 - 10}" y2="{y2 + 48}" marker-end="url(#{arrow_id})"/>')
            elif y1 == y2:
                body.append(f'<line class="v-line" x1="{x1}" y1="{y1 + 48}" x2="{x2 + 210}" y2="{y2 + 48}" marker-end="url(#{arrow_id})"/>')
            else:
                body.append(f'<line class="v-line" x1="{x1 + 100}" y1="{y1 + 96}" x2="{x2 + 100}" y2="{y2 - 10}" marker-end="url(#{arrow_id})"/>')
        for index, (stage, label, (x, y)) in enumerate(zip(stage_labels, shown, positions)):
            role = role_order[index]
            klass = visual_role_class(role)
            body.append(f'<rect class="{klass}" x="{x}" y="{y}" width="200" height="96" rx="12"/>')
            body.append(f'<text class="v-role" x="{x + 100}" y="{y + 23}" text-anchor="middle">{html.escape(stage)}</text>')
            body.append(svg_text_block(label, x + 100, y + 54, limit=19, max_lines=2))
            body.append(f'<text class="v-small" x="{x + 100}" y="{y + 84}" text-anchor="middle">{index + 1} / 6</text>')
        body.append(f'<path class="v-line-dashed" d="M135 296 C135 326,18 326,18 93 L25 93" marker-end="url(#{failure_arrow_id})"/>')
        body.append(
            '<text class="v-small" x="410" y="347" text-anchor="middle">'
            + ("驗證失敗時回到 raw evidence，不用猜測值繼續" if language == "zh" else "On validation failure, return to raw evidence instead of guessing")
            + "</text>"
        )
    elif kind == "state":
        shown = nodes[:6]
        count = max(len(shown), 1)
        box_width = min(132.0, (780 - (count - 1) * 26) / count)
        gap = 26.0
        total_width = count * box_width + (count - 1) * gap
        start_x = (820 - total_width) / 2
        for index in range(len(shown) - 1):
            x = start_x + index * (box_width + gap)
            next_x = start_x + (index + 1) * (box_width + gap)
            body.append(f'<line class="v-line" x1="{x + box_width}" y1="155" x2="{next_x - 8}" y2="155" marker-end="url(#{arrow_id})"/>')
        for index, label in enumerate(shown):
            x = start_x + index * (box_width + gap)
            role = visual_role(label)
            klass = visual_role_class(role)
            body.append(f'<rect class="{klass}" x="{x}" y="105" width="{box_width}" height="100" rx="20"/>')
            body.append(f'<text class="v-role" x="{x + box_width / 2}" y="128" text-anchor="middle">{visual_role_label(role, language)}</text>')
            body.append(svg_text_block(label, x + box_width / 2, 164, limit=14, max_lines=2))
        if len(shown) > 1:
            first_center = start_x + box_width / 2
            last_center = start_x + (len(shown) - 1) * (box_width + gap) + box_width / 2
            body.append(f'<path class="v-line-dashed" d="M{last_center:g} 220 C{last_center:g} 286,{first_center:g} 286,{first_center:g} 220" marker-end="url(#{failure_arrow_id})"/>')
        body.append(
            '<text class="v-small" x="410" y="314" text-anchor="middle">'
            + ("timeout／failure 必須保留 trigger、舊狀態與觀察證據" if language == "zh" else "Timeout or failure retains the trigger, prior state, and observed evidence")
            + "</text>"
        )
    else:
        hub = nodes[0] if nodes else title
        children = nodes[1:6]
        count = max(len(children), 1)
        child_gap = 18.0
        child_width = min(176.0, (780 - (count - 1) * child_gap) / count)
        total_width = count * child_width + (count - 1) * child_gap
        start_x = (820 - total_width) / 2
        centers = [start_x + index * (child_width + child_gap) + child_width / 2 for index in range(len(children))]
        if centers:
            body.append('<line class="v-line" x1="410" y1="102" x2="410" y2="140"/>')
            body.append(f'<line class="v-line" x1="{centers[0]:g}" y1="140" x2="{centers[-1]:g}" y2="140"/>')
            for center in centers:
                body.append(f'<line class="v-line" x1="{center:g}" y1="140" x2="{center:g}" y2="170" marker-end="url(#{arrow_id})"/>')
        body.append('<rect class="v-decision" x="250" y="28" width="320" height="74" rx="18"/>')
        body.append('<text class="v-role" x="410" y="50" text-anchor="middle">MENTAL MODEL／GATE</text>')
        body.append(svg_text_block(hub, 410, 76, limit=27, max_lines=2))
        for index, label in enumerate(children):
            x = start_x + index * (child_width + child_gap)
            role = visual_role(label)
            klass = visual_role_class(role)
            body.append(f'<rect class="{klass}" x="{x}" y="174" width="{child_width}" height="92" rx="12"/>')
            body.append(f'<text class="v-role" x="{x + child_width / 2}" y="198" text-anchor="middle">{visual_role_label(role, language)}</text>')
            body.append(svg_text_block(label, x + child_width / 2, 232, limit=16, max_lines=2))
        body.append(
            '<text class="v-small" x="410" y="322" text-anchor="middle">'
            + ("線條表示教學關係；真正 requirement 仍以引用段落為準" if language == "zh" else "Lines show teaching relationships; cited text owns the requirements")
            + "</text>"
        )
    return head + "".join(body) + "</svg>"


def report_visual_atlas_html(
    report_id: str,
    claims: list[dict],
    section_id: str = "visual-atlas",
    tutorial: bool = True,
) -> str:
    by_id = {item["id"]: item for item in claims}
    cards: list[str] = []
    kind_labels = {
        "architecture": "Architecture／Dependency",
        "sequence": "Sequence／Ownership",
        "decode": "Bit／Field Decode",
        "state": "State／Failure Loop",
    }
    for index, module in enumerate(REPORT_MODULES[report_id], 1):
        sources = [by_id[item] for item in module["sources"]]
        kind = module_visual_kind(module["id"])
        cards.extend(
            [
                f'<article class="visual-card" data-visual-kind="{kind}" id="atlas-{html.escape(module["id"])}">',
                f'<p class="eyebrow">VISUAL {index:02d} · {kind_labels[kind]}</p>',
                f'<h3>{html.escape(module["title"]["zh"])}</h3>',
                '<figure class="visual-board">',
                module_visual_svg(module, "zh"),
                (
                    '<figcaption>教學重畫：先辨認圖形類型、節點角色與箭頭方向，再回到 Spec Figure／欄位表核對。</figcaption></figure>'
                    if tutorial
                    else '<figcaption>查詢重畫：保留機制邊界、欄位角色與 evidence endpoint；精確要求仍以引用來源為準。</figcaption></figure>'
                ),
                ('<p><strong>這張圖回答：</strong>' if tutorial else '<p><strong>查詢用途：</strong>')
                + html.escape(module["lead"]["zh"])
                + "</p>",
                '<p><strong>支援 Figure：</strong>' + ", ".join(f"Figure {value}" for value in module["figures"]) + "</p>",
                '<p class="source-note">' + "；".join(html.escape(compact_citation(item, "zh")) for item in sources) + "</p>",
                "</article>",
            ]
        )
    return "".join(
        [
            f'<section id="{html.escape(section_id)}"><h2>'
            + ("概念圖譜：先看關係，再讀規格" if tutorial else "視覺索引：按機制查欄位與證據")
            + "</h2>",
            '<p class="chapter-bridge">'
            + (
                "iPad 採垂直單欄，桌面會自動排成雙欄。Architecture 看元件位置，Sequence 看 actor 交握，Decode 看 bit／byte 轉換，State 看正常與失敗轉移。每張圖都使用固定角色色與文字標籤。"
                if tutorial
                else "本區用於快速定位機制，不取代欄位表。桌面採寬版索引，iPad 採垂直單欄；先找視圖類型，再跳到 claim、Figure 與來源。"
            )
            + "</p>",
            '<div class="visual-atlas" aria-label="主題視覺索引">',
            *cards,
            "</div></section>",
        ]
    )


def ipad_read_guide_html(tutorial: bool) -> str:
    edition_note = (
        "這是從零建立 Mental Model 的教學版：先看圖與例子，再讀欄位、規範性文字與 Debug。"
        if tutorial
        else "這是工程查詢手冊：先用 keyword／欄位／症狀定位，再核對 requirement、來源與 raw evidence。"
    )
    return "".join(
        [
            f'<p class="edition-note"><strong>本版用途：</strong>{edition_note}</p>',
            '<aside class="ipad-read-guide" aria-label="跨裝置閱讀操作">',
            '<div class="read-chip"><strong>iPad／觸控</strong>點按 details 展開；圖譜採單欄，只有無法再拆的寬表在自己的容器內滑動。</div>',
            '<div class="read-chip"><strong>Desktop／鍵盤滑鼠</strong>寬螢幕自動改成雙欄圖譜；Tab、Enter 與瀏覽器尋找均可使用。</div>',
            '<div class="read-chip"><strong>可搜尋文字</strong>標題、縮寫、角色與來源都保留為 HTML 文字，不把唯一資訊鎖在 SVG。</div>',
            "</aside>",
            '<aside class="visual-legend" aria-label="所有報告共用的顏色與形狀語意">',
            '<div class="legend-item"><span class="legend-swatch role-command">IN</span><strong>藍｜Request／Input</strong><small>host request、command、raw input</small></div>',
            '<div class="legend-item"><span class="legend-swatch role-object">OBJ</span><strong>青綠｜Object／State</strong><small>queue、buffer、controller object、目前狀態</small></div>',
            '<div class="legend-item"><span class="legend-swatch role-decision"><span>?</span></span><strong>紫｜Gate／Rule</strong><small>capability、selector、條件與解碼規則</small></div>',
            '<div class="legend-item"><span class="legend-swatch role-success">OK</span><strong>綠｜Valid／Evidence</strong><small>completion、log、驗證通過與可重算證據</small></div>',
            '<div class="legend-item"><span class="legend-swatch role-failure">!</span><strong>橘｜Warning／Failure</strong><small>reserved、timeout、invalid、回復分支</small></div>',
            "</aside>",
        ]
    )


def generic_toc_html(report_id: str, tutorial: bool) -> str:
    module_links = "".join(
        f'<a href="#module-{html.escape(module["id"])}">{html.escape(module["title"]["zh"])}</a>'
        for module in REPORT_MODULES[report_id]
    )
    quick = '' if tutorial else '<a href="#quick-reference">快速查詢</a>'
    return (
        '<details class="ipad-toc" open><summary>章節導覽｜iPad 點按收合、Desktop 鍵盤可操作</summary><div class="toc-grid">'
        '<a href="#scope">範圍與語意</a>' + quick + '<a href="#visual-atlas">Visual Atlas</a>'
        '<a href="#glossary">縮寫 Glossary</a>' + module_links + '<a href="#claims">Spec 重點</a>'
        '<a href="#figure-index">Figure 索引</a><a href="#sources">來源與限制</a>'
        '</div></details>'
    )


def figure_teaching_svg(figure: dict, guide: dict, language: str) -> str:
    terms = [item[0] for item in guide["terms"]][:4]
    while len(terms) < 4:
        terms.append(("evidence" if language == "en" else "驗證證據") if len(terms) == 3 else guide["kind"])
    title = f"Figure {figure['number']}: {figure['title']}"
    arrow_id = "figure-arrow-" + anchor(figure["id"])
    head = (
        f'<svg viewBox="0 0 820 300" role="img" data-visual-kind="{html.escape(guide["kind"])}" aria-label="{html.escape(title)}">'
        f'<title>{html.escape(title)}</title><desc>{html.escape(guide["kind_text"])}</desc>'
        f'<defs><marker id="{arrow_id}" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto">'
        '<path d="M0,0 L0,6 L9,3 z" class="v-arrow"/></marker></defs>'
    )
    body: list[str] = []
    kind = guide["kind"]
    field_kinds = {"register", "command", "status", "identifier", "layout"}
    flow_kinds = {"queue", "interrupt", "state"}
    if kind in field_kinds:
        headers = ["Locate", "Extract", "Decode", "Validate"]
        role_order = ["command", "object", "decision", "success"]
        for index in range(3):
            x = 22 + index * 198
            body.append(f'<line class="v-line" x1="{x + 176}" y1="144" x2="{x + 190}" y2="144" marker-end="url(#{arrow_id})"/>')
        for index, (header, term) in enumerate(zip(headers, terms)):
            x = 22 + index * 198
            role = role_order[index]
            klass = visual_role_class(role)
            body.append(f'<rect class="{klass}" x="{x}" y="75" width="176" height="138" rx="10"/>')
            body.append(f'<text class="v-role" x="{x + 88}" y="101" text-anchor="middle">{header.upper()}</text>')
            body.append(svg_text_block(term, x + 88, 148, limit=17, max_lines=2))
            body.append(f'<text class="v-small" x="{x + 88}" y="190" text-anchor="middle">{index + 1} / 4</text>')
    elif kind in flow_kinds:
        xs = [125, 410, 695]
        labels = (["Host", "Queue／state", "Controller"] if language == "zh" else ["Host", "Queue / state", "Controller"])
        for x in xs:
            body.append(f'<line class="v-line-soft" stroke-dasharray="6 6" x1="{x}" y1="68" x2="{x}" y2="266"/>')
        pairs = [(0, 1), (1, 2), (2, 1), (1, 0)]
        for index, term in enumerate(terms):
            y = 100 + index * 42
            s, t = pairs[index]
            body.append(f'<line class="v-line" x1="{xs[s]}" y1="{y}" x2="{xs[t]}" y2="{y}" marker-end="url(#{arrow_id})"/>')
            middle = (xs[s] + xs[t]) / 2
            body.append(f'<rect class="v-label-bg" x="{middle - 103}" y="{y - 22}" width="206" height="18" rx="4"/>')
            body.append(svg_text_block(term, middle, y - 9, klass="v-small", limit=26, max_lines=1, line_height=14))
        for x, label, klass in zip(xs, labels, ["v-command", "v-object", "v-object"]):
            body.append(f'<rect class="{klass}" x="{x - 90}" y="24" width="180" height="38" rx="9"/>')
            body.append(svg_text_block(label, x, 49, limit=20, max_lines=1))
    elif kind in {"hierarchy", "relationship"}:
        children = terms[1:4] + ["scope"]
        centers = [106, 309, 512, 715]
        body.append('<line class="v-line" x1="410" y1="95" x2="410" y2="132"/>')
        body.append('<line class="v-line" x1="106" y1="132" x2="715" y2="132"/>')
        for center in centers:
            body.append(f'<line class="v-line" x1="{center}" y1="132" x2="{center}" y2="166" marker-end="url(#{arrow_id})"/>')
        body.append('<rect class="v-decision" x="260" y="25" width="300" height="70" rx="16"/>')
        body.append('<text class="v-role" x="410" y="47" text-anchor="middle">MODEL／RELATION</text>')
        body.append(svg_text_block(terms[0], 410, 72, limit=25, max_lines=2))
        for index, (term, center) in enumerate(zip(children, centers)):
            role = visual_role(term)
            body.append(f'<rect class="{visual_role_class(role)}" x="{center - 82}" y="170" width="164" height="88" rx="11"/>')
            body.append(f'<text class="v-role" x="{center}" y="193" text-anchor="middle">{visual_role_label(role, language)}</text>')
            body.append(svg_text_block(term, center, 226, limit=15, max_lines=2))
    else:
        labels = (["Pointer／selector", "Boundary／length", "Entry／lane", "Result／evidence"] if language == "zh" else ["Pointer / selector", "Boundary / length", "Entry / lane", "Result / evidence"])
        role_order = ["command", "object", "decision", "success"]
        for index in range(3):
            x = 35 + index * 190
            body.append(f'<line class="v-line" x1="{x + 160}" y1="148" x2="{x + 180}" y2="148" marker-end="url(#{arrow_id})"/>')
        for index, (label, term) in enumerate(zip(labels, terms)):
            x = 35 + index * 190
            role = role_order[index]
            klass = visual_role_class(role)
            body.append(f'<rect class="{klass}" x="{x}" y="76" width="160" height="144" rx="8"/>')
            body.append(f'<text class="v-role" x="{x + 80}" y="104" text-anchor="middle">{html.escape(label.upper())}</text>')
            body.append(svg_text_block(term, x + 80, 155, limit=15, max_lines=2))
    body.append(
        '<text class="v-small" x="410" y="286" text-anchor="middle">'
        + ("教學重畫：欄位位置與合法值仍須回到引用 Figure 核對" if language == "zh" else "Teaching redraw: verify field positions and legal values in the cited Figure")
        + "</text>"
    )
    return head + "".join(body) + "</svg>"


def figure_visual_text(figure: dict, guide: dict, language: str) -> list[str]:
    terms = [item[0] for item in guide["terms"]][:4]
    while len(terms) < 4:
        terms.append("evidence")
    labels = (
        ["定位來源", "擷取欄位", "套用編碼", "驗證證據"]
        if language == "zh"
        else ["Locate source", "Extract field", "Apply encoding", "Validate evidence"]
    )
    return [
        "```text",
        f"[{labels[0]}: {terms[0]}]",
        "          ↓",
        f"[{labels[1]}: {terms[1]}] → [{labels[2]}: {terms[2]}]",
        "                                      ↓",
        f"[{labels[3]}: {terms[3]}]",
        "```",
    ]


def compact_citation(item: dict, language: str) -> str:
    if language == "en":
        return (
            f"{item['source_id']} Rev. {item['revision']}, §{item['section']}, "
            f"printed pp. {item['printed_pages']}, PDF pp. {item['pdf_pages']}"
        )
    return (
        f"{item['source_id']} Rev. {item['revision']}，§{item['section']}，"
        f"文件頁 {item['printed_pages']}，PDF 頁 {item['pdf_pages']}"
    )


def glossary_html(report_id: str, claims: list[dict], tutorial: bool) -> str:
    by_id = {item["id"]: item for item in claims}
    rows = []
    for term, claim_id in REPORT_GLOSSARIES[report_id]:
        item = by_id[claim_id]
        rows.append(
            "<tr><td><span class=\"term\">"
            + html.escape(term)
            + "</span></td><td>"
            + html.escape(TERM_LIBRARY[term]["zh"])
            + "</td><td><small>"
            + html.escape(compact_citation(item, "zh"))
            + "</small></td></tr>"
        )
    intro = (
        "第一次閱讀先掌握全部核心詞；後文再次出現時會直接使用縮寫。"
        if tutorial
        else "本表同時是 parser、trace 與設計文件應採用的固定名詞索引。"
    )
    return "".join(
        [
            '<section id="glossary"><h2>先學縮寫：完整 Glossary</h2>',
            f'<p class="chapter-bridge">{intro}</p>',
            '<div class="callout explain"><span class="badge badge-explain">解釋</span> '
            "縮寫只是欄位名稱的壓縮；真正可用的工程資訊還包括 owner、width、unit、scope 與狀態。"
            "遇到未定義縮寫時先回本表，不用靠字面猜測。</div>",
            '<div class="table-wrap"><table><thead><tr><th>縮寫／名詞</th><th>第一次出現時要懂的意思</th><th>來源</th></tr></thead><tbody>',
            *rows,
            "</tbody></table></div></section>",
        ]
    )


def modules_html(report_id: str, claims: list[dict], tutorial: bool) -> str:
    by_id = {item["id"]: item for item in claims}
    parts = (
        [
            '<section id="learning-path"><h2>教學主線：Mental Model、完整流程與 Debug</h2>',
            '<p class="chapter-bridge">以下不依 Spec section 排列，而依「問題 → 元件關係 → 正常流程 → 數值／狀態範例 → failure branch → Debug」組織。流程圖負責時間順序，比較表負責差異；兩者不能互相替代。</p>',
        ]
        if tutorial
        else [
            '<section id="learning-path"><h2>詳細手冊：機制索引與欄位決策表</h2>',
            '<p class="chapter-bridge">本區不重走教學故事。每個模組改用「適用問題、判讀條件、例子／反例、證據與來源」壓縮，供 implementation review、trace triage 與 code review 快速查核。</p>',
        ]
    )
    for index, module in enumerate(REPORT_MODULES[report_id], 1):
        sources = [by_id[item] for item in module["sources"]]
        if tutorial:
            parts.extend(
                [
                    f'<article class="topic-card" id="module-{html.escape(module["id"])}">',
                    f'<p class="eyebrow">LEARNING MODULE {index:02d}</p>',
                    f'<h3>{html.escape(module["title"]["zh"])}</h3>',
                    '<p><span class="badge badge-explain">解釋</span> '
                    + html.escape(module["lead"]["zh"])
                    + "</p>",
                    '<figure><figcaption><strong>流程視圖：</strong>只表達先後與 owner；條件差異請看下方比較表。</figcaption>',
                    module_flow_svg(module, "zh"),
                    "</figure>",
                    '<h4>比較：這些概念差在哪裡</h4><div class="table-wrap"><table><thead><tr>'
                    '<th>項目</th><th>它回答什麼</th><th>Engineer 注意事項</th></tr></thead><tbody>',
                ]
            )
        else:
            parts.extend(
                [
                    f'<article class="topic-card reference-module" id="module-{html.escape(module["id"])}">',
                    f'<p class="eyebrow">MECHANISM INDEX {index:02d}</p>',
                    f'<h3>{html.escape(module["title"]["zh"])}</h3>',
                    '<div class="mini-grid"><div class="mini-card"><strong>適用問題</strong><p>'
                    + html.escape(module["lead"]["zh"])
                    + '</p></div><div class="mini-card"><strong>判讀終點</strong><p>'
                    + html.escape(module["nodes"]["zh"][-1])
                    + "；必須能回指 raw evidence 與來源條件。</p></div></div>",
                    '<h4>條件／差異速查</h4><div class="table-wrap"><table><thead><tr>'
                    '<th>對象</th><th>判讀問題</th><th>實作／Debug 條件</th></tr></thead><tbody>',
                ]
            )
        for row in module["rows"]["zh"]:
            parts.append("<tr>" + "".join(f"<td>{html.escape(value)}</td>" for value in row) + "</tr>")
        if tutorial:
            parts.extend(
                [
                    "</tbody></table></div>",
                    '<div class="callout example"><span class="badge badge-example">具體範例</span> '
                    + html.escape(module["example"]["zh"])
                    + "</div>",
                    '<div class="callout warning"><span class="badge badge-warn">常見誤解／Debug</span> '
                    + html.escape(module["pitfall"]["zh"])
                    + "</div>",
                ]
            )
        else:
            parts.extend(
                [
                    "</tbody></table></div>",
                    '<div class="mini-grid"><div class="mini-card"><strong>Informative example</strong><p>'
                    + html.escape(module["example"]["zh"])
                    + '</p></div><div class="mini-card"><strong>Failure／triage</strong><p>'
                    + html.escape(module["pitfall"]["zh"])
                    + "</p></div></div>",
                ]
            )
        parts.extend(
            [
                '<p class="source-note"><strong>支援來源：</strong>'
                + "；".join(html.escape(compact_citation(item, "zh")) for item in sources)
                + "。<strong>關聯 Figure：</strong>"
                + ", ".join(f"Figure {number}" for number in module["figures"])
                + "。</p>",
                '<p class="back"><a href="#top">回到頂端</a></p></article>',
            ]
        )
    parts.append("</section>")
    return "".join(parts)


def normative_badge_html(keyword: str) -> str:
    normalized = (keyword or "none").lower()
    if normalized in {"shall", "shall not", "mandatory"}:
        klass = "req-shall"
    elif normalized in {"should", "should not"}:
        klass = "req-should"
    elif normalized in {"may", "optional"}:
        klass = "req-may"
    else:
        klass = "req-reserved"
    return f'<span class="badge {klass}">{html.escape(normalized)}</span>'


def quick_reference_html(report_id: str, claims: list[dict]) -> str:
    """Build the scan-first front section used only by the detailed iPad manual."""
    rows = []
    for item in (claim for claim in claims if claim["figure"] is None):
        keyword = item["normative_keyword"] or "none"
        rows.append(
            '<tr><td><a href="#claim-'
            + html.escape(item["id"])
            + '">'
            + html.escape(item["heading_zh_tw"])
            + "</a></td><td><code>"
            + html.escape(keyword)
            + "</code></td><td>"
            + html.escape(tutorial_check(report_id, item["id"]))
            + "</td><td><small>"
            + html.escape(compact_citation(item, "zh"))
            + "</small></td></tr>"
        )
    return "".join(
        [
            '<section id="quick-reference"><h2>快速查詢入口</h2>',
            '<p class="chapter-bridge">這一版不是從頭帶讀的課本。遇到 command、欄位、status 或 trace 問題時，先用下表定位 requirement，再跳到完整論述與 Figure 證據。</p>',
            '<div class="callout explain"><span class="badge badge-explain">查詢順序</span> 症狀或問題 → 找主題 → 核對 normative keyword → 讀來源位置 → 再展開相關 Figure。<strong>shall</strong> 與 <strong>may</strong> 不可互換。</div>',
            '<h3>Debug evidence 記錄模板</h3>',
            '<p>快速查詢的終點不是「找到一個看起來相符的欄位」，而是留下另一位 engineer 可以重算的證據鏈。先固定時間點與 owner，再保存完整原始資料；只抄 decoded 結果會失去 endian、reserved bit、length 與 snapshot 一致性的檢查機會。接著把 capability gate、command input、completion 或觀測資料分開記錄，避免把「支援此機制」「已要求執行」和「已完成」混成同一個布林值。最後才引用下表的 requirement 與來源頁，寫出 decision 以及尚未被證明的部分。</p>',
            '<div class="table-wrap"><table><thead><tr><th>證據層</th><th>必須保存</th><th>判讀前的停止條件</th></tr></thead><tbody>',
            '<tr><td>Context</td><td>controller／namespace 身分、scope、lifecycle state、timestamp、觸發事件</td><td>不知道資料屬於哪個物件或哪個時間點</td></tr>',
            '<tr><td>Raw input</td><td>完整 command dwords、register value、buffer bytes、length、offset 與單位</td><td>只有轉換後數值，無法重新解碼</td></tr>',
            '<tr><td>Gate／result</td><td>capability、selector、completion SCT／SC、相關 log 或 event</td><td>support、request、completion、observation 任一層缺失</td></tr>',
            '<tr><td>Decision</td><td>引用的 section／Figure／頁碼、normative keyword、預期與實際差異</td><td>結論超出引用條件，或把 informative example 當成 requirement</td></tr>',
            '</tbody></table></div>',
            '<div class="callout warning"><span class="badge badge-warn">邊界</span> 同一欄位名稱若出現在不同 command、log page、controller scope 或 namespace scope，不得直接互相比較。先確認資料結構版本、byte range、0\'s-based encoding、單位與更新時機；遇到 Reserved／undefined value 時停止推導，不以 vendor 慣例補成規格行為。</div>',
            '<div class="table-wrap"><table><thead><tr><th>主題</th><th>keyword</th><th>快速判讀問題</th><th>來源</th></tr></thead><tbody>',
            *rows,
            "</tbody></table></div>",
            '<p class="back"><a href="#top">回到頂端</a></p></section>',
        ]
    )


def figure_card_html(figure: dict, item: dict, tutorial: bool) -> str:
    base = figure_explanation(figure, "zh")
    guide = expanded_figure_guide(figure, "zh")
    parts = [
        f'<details class="figure-card" name="figures-{anchor(figure_group(figure))}" id="figure-{figure["number"]}" '
        f'data-figure-table-id="{figure["id"]}">',
        f'<summary>Figure {figure["number"]}: {html.escape(figure["title"])}</summary>',
        f'<p class="figure-meta">§{html.escape(figure["section"])} ｜ '
        f'文件頁 {html.escape(figure["printed_pages"])} ｜ PDF 頁 {html.escape(figure["pdf_pages"])} ｜ '
        f'教學類型：{html.escape(guide["kind"])}</p>',
        '<div class="callout spec"><span class="badge badge-spec">SPEC</span> '
        + normative_badge_html(item["normative_keyword"])
        + " "
        f'<span data-claim-id="{item["id"]}">{html.escape(item["zh_tw"])}</span></div>',
    ]
    if tutorial:
        parts.extend(
            [
                '<h4>先知道它在故事中的位置</h4>',
                f'<p>{html.escape(guide["context"])}</p>',
                f'<p>{html.escape(guide["kind_text"])}</p>',
                '<figure class="visual-board">',
                figure_teaching_svg(figure, guide, "zh"),
                '<figcaption>新手教學重畫（非 Spec 原圖）：箭頭只表示閱讀／因果方向，不穿越節點文字；顏色與形狀依頁首固定圖例。</figcaption></figure>',
                '<h4>讀圖前先學縮寫／欄位</h4>',
                '<div class="table-wrap"><table><thead><tr><th>縮寫／欄位</th><th>白話解釋</th></tr></thead><tbody>',
            ]
        )
        for term, definition in guide["terms"]:
            parts.append(
                f'<tr><td><span class="term">{html.escape(term)}</span></td>'
                f'<td>{html.escape(definition)}</td></tr>'
            )
        parts.extend(
            [
                "</tbody></table></div>",
                '<h4>照這個順序讀</h4><ol>',
                *[f"<li>{html.escape(step)}</li>" for step in guide["steps"]],
                "</ol>",
                '<div class="callout example"><span class="badge badge-example">具體範例</span> '
                + html.escape(guide["example"])
                + "</div>",
                '<div class="callout warning"><span class="badge badge-warn">常見誤解</span> '
                + html.escape(guide["misconception"])
                + "</div>",
                '<h4>能回答／不能回答</h4><div class="table-wrap"><table><thead><tr><th>判讀層級</th><th>內容</th></tr></thead><tbody>',
                *[
                    "<tr>" + "".join(f"<td>{html.escape(value)}</td>" for value in row) + "</tr>"
                    for row in guide["answers"]
                ],
                "</tbody></table></div>",
                '<h4>Debug 對照表</h4><div class="table-wrap"><table><thead><tr><th>症狀</th><th>先查什麼</th></tr></thead><tbody>',
                *[
                    "<tr>" + "".join(f"<td>{html.escape(value)}</td>" for value in row) + "</tr>"
                    for row in guide["debug"]
                ],
                "</tbody></table></div>",
                '<h4>讀完後應能回答</h4><ol>',
                *[f"<li>{html.escape(value)}</li>" for value in guide["check"]],
                "</ol>",
            ]
        )
    else:
        parts.extend(
            [
                '<h4>追溯與欄位索引</h4><div class="mini-grid">',
                '<div class="mini-card"><strong>來源欄位索引</strong><p>' + html.escape(base["item_text"]) + "</p></div>",
                '<div class="mini-card"><strong>來源 keyword 索引</strong><p>' + html.escape(base["keyword_text"]) + "</p></div>",
                '<div class="mini-card"><strong>Claim ID</strong><p><code>' + html.escape(item["id"]) + "</code></p></div>",
                '<div class="mini-card"><strong>Figure role</strong><p>' + html.escape(figure.get("role", "in_scope")) + "／" + html.escape(figure.get("mode", "full")) + "</p></div>",
                "</div>",
                '<figure class="visual-board">',
                figure_teaching_svg(figure, guide, "zh"),
                '<figcaption>詳細版查詢重畫：用固定角色色定位 input、object、gate、evidence 與 failure；精確 bit range／encoding 仍以來源 Figure 為準。</figcaption></figure>',
                '<h4>欄位／名詞速查</h4><div class="table-wrap"><table><thead><tr><th>欄位</th><th>固定解釋</th></tr></thead><tbody>',
            ]
        )
        for term, definition in guide["terms"]:
            parts.append(f'<tr><td><code>{html.escape(term)}</code></td><td>{html.escape(definition)}</td></tr>')
        parts.extend(
            [
                "</tbody></table></div>",
                '<h4>Input／Decode／Validate／Evidence</h4><div class="table-wrap worksheet"><table><thead><tr><th>階段</th><th>必備資料</th><th>停止條件</th></tr></thead><tbody>',
                f'<tr><td>Input</td><td>Figure {figure["number"]} 的 raw register／buffer／CQE snapshot</td><td>owner、scope 或 snapshot 時機不明</td></tr>',
                f'<tr><td>Decode</td><td>{html.escape(", ".join(term for term, _ in guide["terms"]) or figure["title"])}</td><td>bit／byte boundary、unit 或 encoding 未確認</td></tr>',
                f'<tr><td>Validate</td><td>§{html.escape(figure["section"])} 的 capability、length、state 與互斥條件</td><td>reserved、越界、unsupported 或條件衝突</td></tr>',
                '<tr><td>Evidence</td><td>raw value、decoded value、decision、timestamp、owner</td><td>只有結論，無法重算</td></tr>',
                "</tbody></table></div>",
                '<h4>適用邊界</h4><div class="table-wrap"><table><thead><tr><th>可／不可回答</th><th>內容</th></tr></thead><tbody>',
                *[
                    "<tr>" + "".join(f"<td>{html.escape(value)}</td>" for value in row) + "</tr>"
                    for row in guide["answers"]
                ],
                "</tbody></table></div>",
                '<h4>症狀索引</h4><div class="table-wrap"><table><thead><tr><th>症狀</th><th>第一個證據</th></tr></thead><tbody>',
                *[
                    "<tr>" + "".join(f"<td>{html.escape(value)}</td>" for value in row) + "</tr>"
                    for row in guide["debug"]
                ],
                "</tbody></table></div>",
                '<div class="mini-grid"><div class="mini-card"><strong>Informative example</strong><p>'
                + html.escape(guide["example"])
                + '</p></div><div class="mini-card"><strong>Caveat</strong><p>'
                + html.escape(guide["misconception"])
                + "</p></div></div>",
            ]
        )
    parts.extend(
        [
            f'<p class="source-note">{html.escape(item["citation_zh_tw"])}</p>',
            '<p class="back"><a href="#figure-index">回到 Figure 索引</a> ｜ '
            '<a href="#top">回到頂端</a></p></details>',
        ]
    )
    return "".join(parts)


def render_html(
    report_id: str,
    report: dict,
    claims: list[dict],
    figures: list[dict],
    tutorial: bool,
) -> str:
    source_ids = [report["source_id"], *report.get("supporting_source_ids", [])]
    source_markers = [SOURCES[source_id]["marker"] for source_id in source_ids]
    if report_id == "pcie-transport-1.4":
        source_markers.append(SOURCES["NVME-BASE-2.4"]["marker"])
    label = "新手教學版｜iPad／Desktop" if tutorial else "快速查詢詳細手冊｜iPad／Desktop"
    figure_groups: list[str] = []
    for figure in figures:
        group = figure_group(figure)
        if group not in figure_groups:
            figure_groups.append(group)
    dependency_count = sum(
        item.get("role") == "referenced_dependency" for item in figures
    )
    figure_policy = (
        "<p><strong>Figure／Table 政策：</strong>不重製規格原圖；以下逐張說明用途、"
        "讀法、條件與說明性範例。指定正文沒有引用任何編號 Table；"
        "欄位表在本規格中以 Figure 編號。</p>"
        if report_id == "base-admin-fw-logs"
        else "<p><strong>Figure 政策：</strong>不重製規格原圖；以下逐張說明用途、"
        "讀法、條件與說明性範例。欄位表雖以表格呈現，在本範圍的規格中仍以 Figure 編號。</p>"
    )

    quick_nav = (
        '' if tutorial else '<a href="#quick-reference">快查</a> ｜ '
    )
    parts = [
        "<!doctype html>",
        '<html lang="zh-Hant-TW">',
        "<head>",
        '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">',
        '<meta name="color-scheme" content="light dark">',
        '<meta name="theme-color" content="#f4f7fb" media="(prefers-color-scheme: light)">',
        '<meta name="theme-color" content="#0c1220" media="(prefers-color-scheme: dark)">',
        f"<title>{html.escape(report['title_zh'])}｜{label}</title>",
        f"<style>{HTML_CSS}</style>",
        "</head>",
        '<body class="edition-tutorial">' if tutorial else '<body class="edition-reference">',
        '<a class="skip-link" href="#content">跳到正文</a>',
        '<nav class="topbar" id="top" aria-label="章節導覽"><div class="topbar-inner">'
        '<a href="#scope">範圍</a> ｜ ' + quick_nav + '<a href="#glossary">縮寫</a> ｜ '
        '<a href="#visual-atlas">圖解</a> ｜ <a href="#learning-path">Mental Model</a> ｜ <a href="#claims">Spec 重點</a> ｜ '
        '<a href="#figure-index">Figure 教學</a> ｜ <a href="#sources">來源</a></div></nav>',
        '<main id="content">',
        '<header class="hero"><p class="eyebrow">NVME ENGINEERING NOTES · '
        + html.escape(label)
        + "</p>",
        f"<h1>{html.escape(report['title_zh'])}</h1>",
        '<p class="subtitle">'
        + (
            "從縮寫與 Mental Model 開始，用圖、比較、數值範例與 failure branch 建立可用於開發及 Debug 的因果模型。"
            if tutorial
            else "以 keyword、欄位、command、status、Figure 與來源位置快速查詢；保留可直接核對的規範性強度與工程證據。"
        )
        + "</p>",
        "</header>",
        generic_toc_html(report_id, tutorial),
        ipad_read_guide_html(tutorial),
        '<section id="scope"><h2>範圍與閱讀方式</h2>',
        f"<p><strong>納入：</strong>{html.escape(report['range'])}。"
        "正文只保留 PCIe／memory-based 與通用 NVMe 內容；"
        "未納入主題不會出現在報告或 PPT。</p>",
        figure_policy,
        f"<p><strong>完整度：</strong>本檔介紹 {len(figures)} 張納入範圍的 Figure。"
        + (
            f"其中 {dependency_count} 張位於主章節範圍外，但因正文直接引用而納入相依教學。"
            if dependency_count
            else ""
        )
        + "100 分鐘口頭報告應以規格重點與必講 Figure 為主；其餘 Figure 作為附錄查閱，"
        "但仍完整保留於本檔。</p>",
        '<div class="table-wrap"><table><thead><tr><th>keyword</th><th>台灣繁體中文</th>'
        "<th>強度</th></tr></thead><tbody>"
        "<tr><td>shall</td><td>必須</td><td>強制要求</td></tr>"
        "<tr><td>may</td><td>可、得</td><td>允許選擇</td></tr>"
        "<tr><td>should</td><td>宜、建議</td><td>有偏好的建議</td></tr>"
        "<tr><td>optional</td><td>選用</td>"
        "<td>不要求支援；實作後仍依定義</td></tr></tbody></table></div></section>",
        '<section id="map"><h2>整體流程圖</h2>',
        flow_svg(report),
        f"<p>{html.escape(report['diagram_note_zh'])}</p></section>",
        glossary_html(report_id, claims, tutorial),
        report_visual_atlas_html(report_id, claims, tutorial=tutorial),
        quick_reference_html(report_id, claims) if not tutorial else "",
        modules_html(report_id, claims, tutorial),
        '<section id="claims"><h2>規格重點</h2>',
        '<p class="chapter-bridge">前面的 Mental Model 解釋元件如何互動；本節回到可逐條追溯的 Spec 結論。詳細版保留 claim ID 與 normative keyword，新手版則先提供判讀問題。</p>',
    ]
    core_claims = [item for item in claims if item["figure"] is None]
    for index, item in enumerate(core_claims, 1):
        heading = item["heading_zh_tw"]
        parts.extend(
            [
                f'<article class="topic-card" id="claim-{html.escape(item["id"])}"><p class="eyebrow">SPEC FINDING {index:02d}</p><h3>{heading}</h3>',
                '<div class="callout spec"><span class="badge badge-spec">SPEC</span> '
                + normative_badge_html(item["normative_keyword"])
                + " "
                + f'<span data-claim-id="{item["id"]}">{html.escape(item["zh_tw"])}</span></div>',
            ]
        )
        if tutorial:
            parts.extend(
                [
                    '<p><span class="badge badge-explain">讀法</span> '
                    + html.escape(heading)
                    + " 必須放回本章的 actor、scope 與 lifecycle boundary；先證明適用條件，再解碼欄位，最後才判斷結果。</p>",
                    "<p><strong>動手檢查：</strong>"
                + html.escape(tutorial_check(report_id, item["id"]))
                    + "</p>",
                ]
            )
        else:
            parts.append(
                '<dl class="claim-meta"><dt>Claim ID</dt><dd><code>'
                + html.escape(item["id"])
                + "</code></dd><dt>Normative keyword</dt><dd>"
                + normative_badge_html(item["normative_keyword"])
                + "</dd><dt>Section／pages</dt><dd>§"
                + html.escape(item["section"])
                + "；文件頁 "
                + html.escape(item["printed_pages"])
                + "；PDF 頁 "
                + html.escape(item["pdf_pages"])
                + "</dd></dl>"
            )
        parts.extend(
            [
                f'<p class="source-note">{html.escape(item["citation_zh_tw"])}</p>',
                "</article>",
            ]
        )
    parts.extend(
        [
            '</section><section id="figure-index"><h2>Figure 索引</h2>',
            "<p>依 section 跳轉；每張 Figure 可個別展開，減少 iPad 長頁面捲動。</p>",
            "<ul>",
            *[
                f'<li><a href="#section-{anchor(group)}">'
                f'{html.escape(figure_group_label(group, "zh"))}</a></li>'
                for group in figure_groups
            ],
            "</ul></section>",
            '<section id="figures"><h2>Figure／欄位表教學參考</h2>',
            '<p class="chapter-bridge">Spec 在本範圍以 Figure 編號同時表示架構圖、流程圖、register bit-field 與欄位表。每張卡片都先教縮寫與上下文，再說讀法、範例、限制與 Debug；主教學仍以前面的知識流程為骨架。</p>',
        ]
    )
    figure_claims = {
        int(item["figure"]): item for item in claims if item["figure"] is not None
    }
    active_group = ""
    for figure in figures:
        item = figure_claims[int(figure["number"])]
        group = figure_group(figure)
        if group != active_group:
            if active_group:
                parts.append("</section>")
            active_group = group
            parts.append(
                f'<section id="section-{anchor(group)}"><h3>'
                f'{html.escape(figure_group_label(group, "zh"))}</h3>'
            )
        parts.append(figure_card_html(figure, item, tutorial))
    if active_group:
        parts.append("</section>")
    parts.extend(
        [
            "</section>",
            '<section id="sources"><h2>來源與限制</h2>',
            *[f"<p>{html.escape(marker)}</p>" for marker in source_markers],
            f"<p>查證日期：{html.escape(report.get('verified_date', '2026-08-29'))}。目前未納入其他 Errata、ECN、"
            "Technical Proposal、controller vendor 文件或未提供的 "
            "PCI Express Base Specification 原文；PCIe 原生語意只轉述"
            "本次來源明載的 NVMe-specific requirement。</p>",
            "</section>",
            "</main>",
            "</body>",
            "</html>",
            "",
        ]
    )
    return "\n".join(parts)


def glossary_markdown(report_id: str, claims: list[dict], language: str) -> list[str]:
    english = language == "en"
    by_id = {item["id"]: item for item in claims}
    out = [
        "## " + ("Acronyms first: complete glossary" if english else "先學縮寫：完整 Glossary"),
        "",
        (
            "Every abbreviation below is introduced before it is used in the slide narrative. The term alone is never enough: retain owner, width, unit, scope, and state."
            if english
            else "下列縮寫會在投影片主線使用前先定義。縮寫本身永遠不夠；設計與 Debug 還要保留 owner、width、unit、scope 與 state。"
        ),
        "",
        (
            "| Acronym / term | Plain-language meaning | Source |"
            if english
            else "| 縮寫／名詞 | 白話解釋 | 來源 |"
        ),
        "|---|---|---|",
    ]
    for term, claim_id in REPORT_GLOSSARIES[report_id]:
        item = by_id[claim_id]
        out.append(
            f"| `{term}` | {TERM_LIBRARY[term][language]} | {compact_citation(item, language)} |"
        )
    out.extend([""])
    return out


def modules_markdown(report_id: str, claims: list[dict], language: str) -> list[str]:
    english = language == "en"
    by_id = {item["id"]: item for item in claims}
    out = [
        "## " + ("Mental Model and complete teaching path" if english else "Mental Model 與完整教學流程"),
        "",
        (
            "The modules follow engineering causality rather than specification-section order. Related Figures return at the point where they support the flow."
            if english
            else "以下依工程因果而非 Spec section 排列；相關 Figure 會回到它支援的流程節點，不以編號順序取代教學故事線。"
        ),
        "",
    ]
    for index, module in enumerate(REPORT_MODULES[report_id], 1):
        sources = [by_id[item] for item in module["sources"]]
        out.extend(
            [
                f"### Module {index:02d}: {module['title'][language]}",
                "",
                ("**Explanation.** " if english else "**解釋。** ") + module["lead"][language],
                "",
                "```text",
                "\n  ↓\n".join(module["nodes"][language]),
                "```",
                "",
                "#### " + ("Comparison" if english else "比較：這些概念差在哪裡"),
                "",
                (
                    "| Item | What it answers | Engineering note |"
                    if english
                    else "| 項目 | 它回答什麼 | Engineer 注意事項 |"
                ),
                "|---|---|---|",
            ]
        )
        for row in module["rows"][language]:
            out.append("| " + " | ".join(row) + " |")
        out.extend(
            [
                "",
                ("**Informative example.** " if english else "**說明性範例。** ")
                + module["example"][language],
                "",
                ("**Common mistake / debugging.** " if english else "**常見誤解／Debug。** ")
                + module["pitfall"][language],
                "",
                ("**Supporting sources:** " if english else "**支援來源：** ")
                + "; ".join(compact_citation(item, language) for item in sources),
                "",
                ("**Related Figures:** " if english else "**關聯 Figure：** ")
                + ", ".join(f"Figure {number}" for number in module["figures"]),
                "",
            ]
        )
    return out


def module_visual_text(module: dict, language: str) -> list[str]:
    nodes = [svg_label(value, 34) for value in module["nodes"][language]][:6]
    kind = module_visual_kind(module["id"])
    if kind == "architecture":
        hub = nodes[0]
        branches = nodes[1:]
        lines = [f"[{hub}]"]
        for index, value in enumerate(branches):
            branch = "└─" if index == len(branches) - 1 else "├─"
            lines.append(f"  {branch} [{value}]")
        return lines
    if kind == "sequence":
        lines = ["Host / software        Shared object        Controller / evidence"]
        for index, value in enumerate(nodes):
            prefix = "Host → Shared" if index % 4 == 0 else "Shared → Controller" if index % 4 == 1 else "Controller → Shared" if index % 4 == 2 else "Shared → Host"
            lines.append(f"{prefix}: {value}")
        return lines
    if kind == "decode":
        labels = ["RAW", "LOCATE", "DECODE", "VALIDATE", "APPLY", "EVIDENCE"]
        shown = nodes[:6]
        while len(shown) < 6:
            shown.append("evidence")
        stages = [f"[{label}: {value}]" for label, value in zip(labels, shown)]
        return [" → ".join(stages[:3]), " → ".join(stages[3:]), "VALIDATE fail ──→ return to RAW evidence"]
    return [" → ".join(f"[{value}]" for value in nodes), "timeout / failure ──→ preserve trigger + previous state + evidence"]


def visual_atlas_markdown(report_id: str, claims: list[dict], language: str) -> list[str]:
    english = language == "en"
    by_id = {item["id"]: item for item in claims}
    out = [
        "## " + ("Visual atlas: locate the system before reading fields" if english else "Visual Atlas：先用圖建立整體位置"),
        "",
        (
            "Each redraw answers a different question: architecture locates components, sequence shows ownership, decode turns bits into engineering values, and state views preserve failure evidence. These are teaching redraws, not copies of specification artwork."
            if english
            else "每張教學重畫回答不同問題：Architecture 定位元件、Sequence 顯示 ownership、Decode 把 bits 轉成工程值、State 保留 failure evidence；它們不是 Spec 原圖的複製。"
        ),
        "",
    ]
    for index, module in enumerate(REPORT_MODULES[report_id], 1):
        sources = [by_id[value] for value in module["sources"]]
        out.extend(
            [
                f"### Visual {index:02d}: {module['title'][language]}",
                "",
                f"**View type:** `{module_visual_kind(module['id'])}`",
                "",
                "```text",
                *module_visual_text(module, language),
                "```",
                "",
                ("**Question answered:** " if english else "**回答的問題：** ") + module["lead"][language],
                "",
                ("**Supporting Figures:** " if english else "**支援 Figure：** ") + ", ".join(f"Figure {value}" for value in module["figures"]),
                "",
                ("**Sources:** " if english else "**來源：** ") + "; ".join(compact_citation(item, language) for item in sources),
                "",
            ]
        )
    return out


def figure_card_markdown(
    figure: dict, item: dict, language: str
) -> list[str]:
    english = language == "en"
    base = figure_explanation(figure, language)
    guide = expanded_figure_guide(figure, language)
    statement = item["en"] if english else item["zh_tw"]
    citation = item["citation_en"] if english else item["citation_zh_tw"]
    out = [
        '<details markdown="1">',
        f"<summary><strong>Figure {figure['number']}: {html.escape(figure['title'])}</strong></summary>",
        "",
        f"<!-- claim:{item['id']} figure-table:{figure['id']} -->",
        "",
        ("**SPEC.** " if english else "**SPEC。** ") + statement,
        "",
        "#### " + ("Where this Figure fits" if english else "這張 Figure 在完整流程中的位置"),
        "",
        guide["context"],
        "",
        guide["kind_text"],
        "",
        "#### " + ("Teaching redraw" if english else "教學重畫（非 Spec 原圖）"),
        "",
        *figure_visual_text(figure, guide, language),
        "",
        "#### " + ("Terms to learn before reading" if english else "讀圖前先懂這些縮寫／欄位"),
        "",
        ("| Term | Plain-language meaning |" if english else "| 縮寫／欄位 | 白話解釋 |"),
        "|---|---|",
    ]
    for term, definition in guide["terms"]:
        out.append(f"| `{term}` | {definition} |")
    out.extend(
        [
            "",
            "#### " + ("Read in this order" if english else "照這個順序讀，不要直接跳到數值"),
            "",
        ]
    )
    for index, step in enumerate(guide["steps"], 1):
        out.append(f"{index}. {step}")
    out.extend(
        [
            "",
            "#### " + ("Input → Decode → Validate → Evidence worksheet" if english else "Input → Decode → Validate → Evidence 工作紙"),
            "",
            ("| Stage | Record | Stop condition |" if english else "| 階段 | 要記錄什麼 | 停止條件 |"),
            "|---|---|---|",
            (f"| Input | Complete raw register, buffer, or CQE snapshot for Figure {figure['number']} | Object, scope, or snapshot timing is unknown |" if english else f"| Input | Figure {figure['number']} 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |"),
            ("| Decode | Indexed fields, byte/bit range, unit, and encoding rule | A boundary, unit, or encoding rule is unconfirmed |" if english else "| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |"),
            (f"| Validate | §{figure['section']} conditions, capability gate, actual length or state | Reserved value, overrun, unsupported capability, or contradictory condition |" if english else f"| Validate | §{figure['section']} 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |"),
            ("| Evidence | Raw value, decoded value, decision, timestamp, and owner | A conclusion exists without recomputable evidence |" if english else "| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |"),
            "",
            "#### " + ("What it answers and what it does not" if english else "這張圖能回答什麼，不能回答什麼"),
            "",
            ("| Reading level | Content |" if english else "| 判讀層級 | 內容 |"),
            "|---|---|",
        ]
    )
    for row in guide["answers"]:
        out.append("| " + " | ".join(row) + " |")
    out.extend(
        [
            "",
            ("**Informative example.** " if english else "**說明性範例。** ") + guide["example"],
            "",
            ("**Common misconception.** " if english else "**常見誤解。** ") + guide["misconception"],
            "",
            "#### " + ("Debug matrix" if english else "Debug 對照表"),
            "",
            ("| Symptom | First checks |" if english else "| 症狀 | 先查什麼 |"),
            "|---|---|",
        ]
    )
    for row in guide["debug"]:
        out.append("| " + " | ".join(row) + " |")
    out.extend(
        [
            "",
            "#### " + ("Questions the reader should now answer" if english else "讀完後應能回答"),
            "",
        ]
    )
    for index, value in enumerate(guide["check"], 1):
        out.append(f"{index}. {value}")
    out.extend(
        [
            "",
            ("**Source field index:** " if english else "**來源欄位索引：** ") + base["item_text"],
            "",
            ("**Source keyword index:** " if english else "**來源 keyword 索引：** ") + base["keyword_text"],
            "",
            f"> {citation}",
            "",
            "</details>",
            "",
        ]
    )
    return out


def frontmatter(
    report_id: str, title: str, description: str, language: str
) -> str:
    lang = "en" if language == "en" else "zh-Hant-TW"
    image = POST_IMAGES[report_id][language]
    report_date = REPORTS[report_id].get("date", "2026-08-28")
    return f"""---
layout: post
read_time: true
show_date: true
title: "{title}"
date: {report_date}
description: "{description}"
lang: {lang}
img: {image}
tags: [NVMe, PCIe, Specification]
category: NVMe
author: Jia-Chang
github: JiaChangGit/JiaChangGit.github.io/tree/main/DOCS/nvme-spec-report
toc: yes
---
"""


def render_markdown(
    report_id: str,
    report: dict,
    claims: list[dict],
    figures: list[dict],
    language: str,
) -> str:
    english = language == "en"
    title = report["title_en"] if english else report["title_zh"]
    description = (
        "Source-located PCIe/NVMe report for PPT authoring."
        if english
        else "供 GitHub Pages 與 PPT 使用的 NVMe 規格導讀。"
    )
    fence = chr(96) * 3
    dependency_count = sum(
        item.get("role") == "referenced_dependency" for item in figures
    )
    out = [
        frontmatter(report_id, title, description, language),
        f"# {title}",
        "",
        (
            "Purpose: a source-located engineering report for GitHub Pages "
            "and a 100-minute presentation."
            if english
            else "用途：供 GitHub Pages 閱讀與 100 分鐘簡報製作；"
            "讀者已具備 PCIe 與 NVMe 基礎。"
        ),
        "",
        (
            "Scope: "
            + report["range_en"]
            + ". Only PCIe/memory-based and common NVMe content appears below."
            if english
            else "範圍：" + report["range"] + "。正文只保留 PCIe／memory-based "
            "與通用 NVMe 內容。"
        ),
        "",
        "## " + ("Source versions" if english else "來源版本"),
        "",
        *[
            SOURCES[source_id]["marker"]
            for source_id in [report["source_id"], *report.get("supporting_source_ids", [])]
        ],
    ]
    if report_id == "pcie-transport-1.4":
        out.append(SOURCES["NVME-BASE-2.4"]["marker"])
    out.extend(
        [
            "",
            (
                f"Verification date: {report.get('verified_date', '2026-08-29')}. No additional errata, ECNs, "
                "Technical Proposals, controller-vendor documents, or source text "
                "from the external PCI Express Base Specification are included."
                if english
                else f"查證日期：{report.get('verified_date', '2026-08-29')}。目前未納入其他 Errata、ECN、"
                "Technical Proposal、controller vendor 文件或未提供的 "
                "PCI Express Base Specification 原文。"
            ),
            "",
            "## " + ("Reading map" if english else "閱讀地圖"),
            "",
            fence + "text",
            " -> ".join(report["diagram"]),
            fence,
            "",
            report["diagram_note_en"] if english else report["diagram_note_zh"],
            "",
            "## " + ("Normative language" if english else "規範性用語"),
            "",
            (
                "shall is mandatory, may permits a choice, should expresses a "
                "preferred recommendation, and optional means support is not "
                "required. The report preserves these terms and never promotes "
                "one into another."
                if english
                else "shall 譯為「必須」，may 譯為「可／得」，should 譯為"
                "「宜／建議」，optional 譯為「選用」。本文不提高或降低原文語氣。"
            ),
            "",
        ]
    )
    out.extend(glossary_markdown(report_id, claims, language))
    out.extend(visual_atlas_markdown(report_id, claims, language))
    out.extend(modules_markdown(report_id, claims, language))
    out.extend(
        [
            "## " + ("Source-located specification findings" if english else "可追溯的規格重點"),
            "",
            (
                "The mental model above explains causality. This section preserves each source-located conclusion and its normative strength for speaker notes and review."
                if english
                else "前面的 Mental Model 解釋因果；本節保留每個可追溯結論與 normative 強度，供講者備註與審查。"
            ),
            "",
        ]
    )
    core_claims = [item for item in claims if item["figure"] is None]
    for index, item in enumerate(core_claims, 1):
        text = item["en"] if english else item["zh_tw"]
        citation = item["citation_en"] if english else item["citation_zh_tw"]
        heading = item["heading_en"] if english else item["heading_zh_tw"]
        out.extend(
            [
                f"### {index}. {heading}",
                "",
                f"<!-- claim:{item['id']} -->",
                "",
                text,
                "",
                (
                    "**Explanation.** Place this finding back into the teaching flow: establish object and scope, check capability and state, then convert the field into a software decision. Field presence is not proof of enablement, and a successful completion does not by itself prove that the next lifecycle stage has completed."
                    if english
                    else "**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。"
                ),
                "",
                f"> {citation}",
                "",
            ]
        )
    out.extend(
        [
            "## " + ("Figure index" if english else "Figure 索引"),
            "",
            (
                f"This report introduces all {len(figures)} in-scope Figures. Use the "
                "section links below for the 100-minute presentation path; every Figure "
                "remains available as an appendix item."
                + (
                    f" {dependency_count} Figures are outside the main section range but are included because the requested text directly references them."
                    if dependency_count
                    else ""
                )
                if english
                else f"本報告介紹全部 {len(figures)} 張納入範圍的 Figure。100 分鐘簡報"
                "以 section 主線與必講 Figure 為主，其餘 Figure 仍完整保留作為附錄。"
                + (
                    f"其中 {dependency_count} 張位於主章節範圍外，但因指定正文直接引用而納入相依教學。"
                    if dependency_count
                    else ""
                )
            ),
            "",
        ]
    )
    figure_groups: list[str] = []
    for figure in figures:
        group = figure_group(figure)
        if group not in figure_groups:
            figure_groups.append(group)
    for group in figure_groups:
        out.extend(
            [
                f"- [{figure_group_label(group, language)}](#section-{anchor(group)})",
                "",
            ]
        )
    out.extend(
        [
            "## " + ("Figure and field-table teaching reference" if english else "Figure／欄位表教學參考"),
            "",
            (
                ("The requested text contains no numbered Table reference. " if report_id == "base-admin-fw-logs" else "")
                + "The source uses Figure numbers for diagrams and field-layout tables. "
                "No source artwork is reproduced; compact field and keyword indexes "
                "come from the locally verified PDFs."
                if english
                else ("指定正文沒有引用任何編號 Table。" if report_id == "base-admin-fw-logs" else "")
                + "本範圍的規格以 Figure 編號同時涵蓋示意圖與欄位表；本文不重製原圖。"
                "欄位與 keyword 索引來自本機核對過的 PDF。"
            ),
            "",
        ]
    )
    figure_claims = {
        int(item["figure"]): item for item in claims if item["figure"] is not None
    }
    active_group = ""
    for figure in figures:
        item = figure_claims[int(figure["number"])]
        group = figure_group(figure)
        if group != active_group:
            active_group = group
            out.extend(
                [
                    f'<a id="section-{anchor(group)}"></a>',
                    "",
                    f"### {figure_group_label(group, language)}",
                    "",
                ]
            )
        out.extend(figure_card_markdown(figure, item, language))
    out.extend(
        [
            "## " + ("Use and limitations" if english else "使用與限制"),
            "",
            (
                "Use the claim IDs as stable PPT traceability keys. Re-check "
                "affected claims if the source revision, errata set, or approved "
                "scope changes."
                if english
                else "製作 PPT 時以 claim ID 作為追溯鍵。來源 revision、Errata "
                "集合或核准範圍改變時，必須重新核對受影響 claim。"
            ),
            "",
        ]
    )
    return "\n".join(out)


FIRMWARE_PARTS = [
    {
        "id": "mental-model",
        "zh": "PART 1 — 先建立 Mental Model：image、slot、domain",
        "en": "PART 1 — Mental Model: Images, Slots, and Domains",
        "intro_zh": "Firmware update 不是把檔案寫進裝置後立刻生效。Downloaded image、slot 內已保存的 image、目前執行中的 image，以及排定在下一次 reset 啟用的 image，是四個要分開追蹤的狀態。",
        "intro_en": "A firmware update is not an immediate file replacement. Track four distinct states: downloaded image data, an image stored in a slot, the currently executing image, and an image scheduled for activation at a later reset.",
        "claims": [
            "BASEFWLOG-MODEL-DOMAIN",
            "BASEFWLOG-CAP-FR",
            "BASEFWLOG-CAP-MDS-ULIST",
            "BASEFWLOG-CAP-FRMW",
            "BASEFWLOG-CAP-MTFA",
            "BASEFWLOG-CAP-FWUG",
            "BASEFWLOG-CAP-MPTFAWR",
        ],
        "inference_zh": "工程上應把 domain 當作 firmware 狀態的共享鍵。只記錄 PCI Function 或 controller ID，可能把同一組 shared slots 誤判成多套獨立 firmware。",
        "inference_en": "Use the domain as the firmware-state sharing key. Recording only a PCI Function or controller ID can incorrectly turn one shared slot set into several apparently independent firmware stores.",
    },
    {
        "id": "download",
        "zh": "PART 2 — 建立 Download Sequence：切片、對齊、失效條件",
        "en": "PART 2 — Build the Download Sequence: Portions, Alignment, Invalidation",
        "intro_zh": "Image 可以分段傳送，但 controller 看到的是 dword range，不是檔名或檔案 offset。每一段都要同時滿足 buffer、0's-based length、image-relative offset 與 FWUG。",
        "intro_en": "An image may be transferred in portions, but the controller sees dword ranges rather than a filename or byte-oriented file offset. Every portion must satisfy buffer, zero-based length, image-relative offset, and FWUG constraints together.",
        "claims": [
            "BASEFWLOG-FW-SEQUENCE",
            "BASEFWLOG-DOWNLOAD-RANGE",
            "BASEFWLOG-DOWNLOAD-FIELDS",
            "BASEFWLOG-FW-DISCARD",
        ],
        "inference_zh": "driver 應在送出 command 前用 byte interval 檢查 overlap，再轉成 NUMD／OFST；若先轉成 0's-based 欄位才檢查，最容易發生 off-by-one。",
        "inference_en": "A driver should detect overlap on byte intervals before converting to NUMD and OFST. Performing interval checks only after zero-based encoding makes off-by-one defects much more likely.",
    },
    {
        "id": "commit-activate",
        "zh": "PART 3 — Commit 與 Activation：CA 決定狀態轉移",
        "en": "PART 3 — Commit and Activation: CA Selects the State Transition",
        "intro_zh": "Firmware Commit 同時承擔驗證、slot placement 與 activation policy。最重要的判斷不是「command 成功了嗎」，而是成功後 image 位於哪個 slot、是否已 active、還欠哪一種 reset。",
        "intro_en": "Firmware Commit combines validation, slot placement, and activation policy. The key question is not merely whether the command succeeded, but which slot now holds the image, whether it is active, and which reset—if any—still remains.",
        "claims": [
            "BASEFWLOG-COMMIT-PURPOSE",
            "BASEFWLOG-COMMIT-CDW10",
            "BASEFWLOG-COMMIT-BOOT",
            "BASEFWLOG-COMMIT-MUD",
            "BASEFWLOG-COMMIT-STATUS",
            "BASEFWLOG-FW-RESET",
            "BASEFWLOG-FW-IMMEDIATE",
            "BASEFWLOG-FW-FAILURE",
            "BASEFWLOG-RESET-XREF",
            "BASEFWLOG-UUID-LIST",
            "BASEFWLOG-UUID-RESET",
            "BASEFWLOG-XREF-337",
        ],
        "inference_zh": "recovery code 應以完整 SCT／SC 分流，而不是只判斷 success／failure。回報需要 Conventional Reset 時，用 FLR 取代並不能滿足該狀態所指示的 activation 邊界。",
        "inference_en": "Recovery logic should branch on the complete SCT/SC rather than a success/failure boolean. When status requires Conventional Reset, substituting FLR does not satisfy the indicated activation boundary.",
    },
    {
        "id": "lid03",
        "zh": "PART 4 — 用 LID 03h 驗證：從 command 到 512-byte layout",
        "en": "PART 4 — Verify with LID 03h: From Command to the 512-Byte Layout",
        "intro_zh": "LID 03h 是 firmware workflow 的觀測面：AFI 回答 current／next active slot，FRS1-FRS7 回答各 slot 保存的 revision。它不替代 Firmware Commit completion，也不告訴 host 該用哪一種 reset。",
        "intro_en": "LID 03h is the observation surface for the firmware workflow. AFI reports current and next active slots, while FRS1-FRS7 report stored revisions. It does not replace Firmware Commit completion or choose the required reset for the host.",
        "claims": [
            "BASEFWLOG-LOG-COMMAND",
            "BASEFWLOG-LOG-LENGTH",
            "BASEFWLOG-LOG-RAE",
            "BASEFWLOG-LOG-OFFSET",
            "BASEFWLOG-LOG-SCOPE",
            "BASEFWLOG-LID03-DESCRIPTION",
            "BASEFWLOG-LID03-AFI",
            "BASEFWLOG-LID03-FRS",
        ],
        "inference_zh": "驗證時要同時比對 Identify.FR、LID 03h 的 CAFS 與對應 FRSx。只比 ASCII revision 可能在兩個 slots 恰好含相同字串時失去 slot 身分。",
        "inference_en": "Verification should compare Identify.FR, LID 03h CAFS, and the corresponding FRSx together. Comparing only the ASCII revision loses slot identity when two slots happen to contain the same string.",
    },
]


def firmware_mental_model_svg() -> str:
    return """<svg width="100%" height="260" viewBox="0 0 820 260" role="img" data-visual-kind="sequence" aria-labelledby="fw-model-title fw-model-desc">
<title id="fw-model-title">Firmware update mental model</title>
<desc id="fw-model-desc">Downloaded portions are committed to a shared firmware slot, selected for activation, and then observed through Identify FR and LID 03h.</desc>
<defs><marker id="fw-arrow" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" class="v-arrow"/></marker><marker id="fw-gate-arrow" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" class="v-arrow-failure"/></marker></defs>
<line class="v-line" x1="170" y1="106" x2="218" y2="106" marker-end="url(#fw-arrow)"/><line class="v-line" x1="410" y1="106" x2="458" y2="106" marker-end="url(#fw-arrow)"/><line class="v-line" x1="610" y1="106" x2="658" y2="106" marker-end="url(#fw-arrow)"/>
<path class="v-line-dashed" d="M315,174 C315,228 540,228 540,146" marker-end="url(#fw-gate-arrow)"/>
<rect class="v-command" x="20" y="66" width="150" height="80" rx="12"/><text class="v-role" x="95" y="88" text-anchor="middle">REQUEST</text><text class="v-label" x="95" y="111" text-anchor="middle">Downloaded</text><text class="v-label" x="95" y="132" text-anchor="middle">image portions</text>
<rect class="v-object" x="220" y="36" width="190" height="138" rx="12"/><text class="v-role" x="315" y="59" text-anchor="middle">SHARED OBJECT</text><text class="v-label" x="315" y="84" text-anchor="middle">Domain-shared slots</text><text class="v-small" x="315" y="111" text-anchor="middle">slot 1 · current</text><text class="v-small" x="315" y="133" text-anchor="middle">slot 2 · next</text><text class="v-small" x="315" y="155" text-anchor="middle">slot 3…7</text>
<rect class="v-decision" x="460" y="66" width="150" height="80" rx="12"/><text class="v-role" x="535" y="88" text-anchor="middle">ACTIVATION GATE</text><text class="v-label" x="535" y="113" text-anchor="middle">Running firmware</text>
<rect class="v-success" x="660" y="36" width="140" height="138" rx="12"/><text class="v-role" x="730" y="59" text-anchor="middle">EVIDENCE</text><text class="v-label" x="730" y="84" text-anchor="middle">Observation</text><text class="v-small" x="730" y="111" text-anchor="middle">Identify.FR</text><text class="v-small" x="730" y="133" text-anchor="middle">LID 03h AFI</text><text class="v-small" x="730" y="155" text-anchor="middle">FRS1…FRS7</text>
<rect class="v-label-bg" x="175" y="78" width="40" height="20" rx="5"/><text class="v-small" x="195" y="92" text-anchor="middle">Commit</text><rect class="v-label-bg" x="414" y="78" width="42" height="20" rx="5"/><text class="v-small" x="435" y="92" text-anchor="middle">select</text>
<text class="v-small" x="427" y="244" text-anchor="middle">immediate activation or reset boundary</text>
</svg>"""


def firmware_afi_svg() -> str:
    return """<svg width="100%" height="190" viewBox="0 0 820 190" role="img" data-visual-kind="decode" aria-labelledby="afi-title afi-desc">
<title id="afi-title">AFI and Firmware Slot Information layout</title>
<desc id="afi-desc">AFI byte zero contains NAFS in bits six through four and CAFS in bits two through zero, followed by reserved bytes and seven eight-byte revision fields.</desc>
<text class="v-label" x="20" y="28">AFI byte 0 · bit ruler</text>
<rect class="v-failure" x="20" y="42" width="80" height="42"/><rect class="v-decision" x="100" y="42" width="240" height="42"/><rect class="v-failure" x="340" y="42" width="80" height="42"/><rect class="v-success" x="420" y="42" width="240" height="42"/>
<text class="v-label" x="60" y="68" text-anchor="middle">R [7]</text><text class="v-label" x="220" y="68" text-anchor="middle">NAFS [6:4]</text><text class="v-label" x="380" y="68" text-anchor="middle">R [3]</text><text class="v-label" x="540" y="68" text-anchor="middle">CAFS [2:0]</text>
<text class="v-small" x="20" y="103">橘色虛線欄位為 Reserved；綠色欄位是目前 active slot 證據。</text>
<text class="v-label" x="20" y="130">512-byte log page · memory layout</text>
<rect class="v-success" x="20" y="142" width="70" height="36"/><rect class="v-failure" x="90" y="142" width="90" height="36"/><rect class="v-object" x="180" y="142" width="390" height="36"/><rect class="v-failure" x="570" y="142" width="230" height="36"/>
<text class="v-label" x="55" y="165" text-anchor="middle">AFI</text><text class="v-label" x="135" y="165" text-anchor="middle">R 1:7</text><text class="v-label" x="375" y="165" text-anchor="middle">FRS1…FRS7 · bytes 8:63</text><text class="v-label" x="685" y="165" text-anchor="middle">Reserved 64:511</text>
</svg>"""


def firmware_claim_order(claims: list[dict]) -> list[dict]:
    by_id = {item["id"]: item for item in claims if item["figure"] is None}
    return [by_id[claim_id] for part in FIRMWARE_PARTS for claim_id in part["claims"]]


def firmware_figure_appendix_html(
    claims: list[dict], figures: list[dict], tutorial: bool = False
) -> list[str]:
    figure_claims = {
        int(item["figure"]): item for item in claims if item["figure"] is not None
    }
    out = [
        '<section id="appendix"><h2>Appendix A — Supporting Figure／Field Reference</h2>',
        "<p id=\"figure-index\"><strong>[解釋]</strong> 下列 Figure 是主流程的可追溯證據，不是文章章節順序。"
        "<code>referenced_dependency</code> 只摘取理解所需欄位；Figure 209 只發布 LID 03h row。</p>",
    ]
    for figure in figures:
        item = figure_claims[int(figure["number"])]
        out.append(figure_card_html(figure, item, tutorial=tutorial))
    out.append("</section>")
    return out


FW_GLOSSARY = [
    ("Domain", "Firmware slots 的共享與 activation 範圍；不一定等於單一 controller。", "The sharing and activation scope for firmware slots; not necessarily one controller."),
    ("Firmware image", "可下載、驗證、保存並啟用的 firmware 內容。", "Firmware content that can be downloaded, validated, stored, and activated."),
    ("Firmware slot", "保存一個 firmware revision 的邏輯位置；不等於目前正在執行。", "A logical location holding one firmware revision; not necessarily the executing revision."),
    ("Activation", "讓某個 slot 的 image 成為 controller 正在執行的 firmware。", "Making the image in a slot become the firmware executed by the controller."),
    ("FR", "Firmware Revision；目前正在執行的 8-byte ASCII revision。", "Firmware Revision; the eight-byte ASCII revision currently executing."),
    ("FRMW", "Firmware Updates capability byte；集合 SMUD、FAWR、NOFS、FFSRO。", "Firmware Updates capability byte containing SMUD, FAWR, NOFS, and FFSRO."),
    ("SMUD", "Support Multiple Update Detection；能否偵測重疊 update sequence。", "Support Multiple Update Detection; whether overlapping update sequences can be detected."),
    ("FAWR", "Firmware Activation Without Reset；是否支援不經 reset 的 activation。", "Firmware Activation Without Reset support."),
    ("NOFS", "Number Of Firmware Slots；domain 支援 1 到 7 個 slots。", "Number Of Firmware Slots; one through seven slots in the domain."),
    ("FFSRO", "First Firmware Slot Read Only；slot 1 是否唯讀。", "First Firmware Slot Read Only."),
    ("MTFA", "Maximum Time for Firmware Activation；activation 暫停 command processing 的上限，100 ms units。", "Maximum Time for Firmware Activation; command-processing pause in 100 ms units."),
    ("FWUG", "Firmware Update Granularity；NUMD／OFST 的 granularity 與 alignment，4 KiB units。", "Firmware Update Granularity for NUMD/OFST alignment, in 4 KiB units."),
    ("MPTFAWR", "Maximum Processing Time for Firmware Activation Without Reset；CA=011b command 完成時間，100 ms units。", "Maximum Processing Time for Firmware Activation Without Reset, in 100 ms units."),
    ("DPTR / PRP", "Data Pointer／Physical Region Page；指向本次 transfer buffer。", "Data Pointer / Physical Region Page identifying the transfer buffer."),
    ("NUMD / OFST", "0's-based dword count／image-relative dword offset。", "Zero-based dword count / image-relative dword offset."),
    ("CA / FS", "Commit Action／Firmware Slot；決定 Commit 做什麼、作用在哪個 slot。", "Commit Action / Firmware Slot selecting the operation and target slot."),
    ("MUD", "Multiple Update Detected；Firmware Commit CQE 的 overlap 證據。", "Multiple Update Detected; overlap evidence in the Firmware Commit CQE."),
    ("LID / RAE", "Log Page Identifier／Retain Asynchronous Event。", "Log Page Identifier / Retain Asynchronous Event."),
    ("AFI", "Active Firmware Info；LID 03h byte 0。", "Active Firmware Info in byte 0 of LID 03h."),
    ("NAFS / CAFS", "Next／Current Active Firmware Slot。", "Next / Current Active Firmware Slot."),
    ("FRS1…FRS7", "Firmware Revision for Slot 1…7；每格 8-byte ASCII。", "Firmware Revision for Slots 1 through 7; eight ASCII bytes each."),
]


def fw_claim_html(item: dict) -> list[str]:
    return [
        f'<p><strong>[SPEC]</strong> <span data-claim-id="{item["id"]}">{html.escape(item["zh_tw"])}</span></p>',
        f"<p><small>{html.escape(item['citation_zh_tw'])}</small></p>",
    ]


def fw_glossary_html(claims: list[dict], compact: bool = False) -> str:
    by_id = {item["id"]: item for item in claims}
    rows = REPORT_GLOSSARIES["base-admin-fw-logs"]
    if compact:
        rows = rows[:18]
    return (
        '<div class="table-wrap"><table>'
        "<thead><tr><th>縮寫／名詞</th><th>先用一句話理解</th><th>來源</th></tr></thead><tbody>"
        + "".join(
            f'<tr><td><span class="term">{html.escape(term)}</span></td>'
            f"<td>{html.escape(TERM_LIBRARY[term]['zh'])}</td>"
            f"<td><small>{html.escape(compact_citation(by_id[claim_id], 'zh'))}</small></td></tr>"
            for term, claim_id in rows
        )
        + "</tbody></table></div>"
    )


def fw_html_shell_start(report: dict, label: str, subtitle: str, toc: str) -> list[str]:
    reference = "快速查詢" in label
    words_target = "ref-first-words" if reference else "words"
    model_target = "ref-start" if reference else "model"
    example_target = "ref-lid03" if reference else "example-story"
    debug_target = "ref-debug" if reference else "debug-story"
    return [
        "<!doctype html>",
        '<html lang="zh-Hant-TW">',
        "<head>",
        '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">',
        '<meta name="color-scheme" content="light dark">',
        '<meta name="theme-color" content="#f4f7fb" media="(prefers-color-scheme: light)">',
        '<meta name="theme-color" content="#0c1220" media="(prefers-color-scheme: dark)">',
        f"<title>{html.escape(report['title_zh'])}｜{label}</title>",
        f"<style>{HTML_CSS}</style>",
        "</head>",
        '<body class="edition-reference">' if reference else '<body class="edition-tutorial">',
        '<a class="skip-link" href="#content">跳到正文</a>',
        f'<nav class="topbar" id="top"><div class="topbar-inner"><a href="#{words_target}">縮寫</a> ｜ '
        '<a href="#fw-visual-atlas">圖解</a> ｜ '
        f'<a href="#{model_target}">Mental Model</a> ｜ <a href="#{example_target}">End-to-End</a> ｜ '
        f'<a href="#{debug_target}">Debug</a> ｜ <a href="#figure-index">Figure 教學</a></div></nav>',
        '<main id="content"><header class="hero"><p class="eyebrow">NVME-BASE-2.4 · REVISION 2.4 · 2026-09-02</p>',
        f"<h1>{html.escape(report['title_zh'])}</h1>",
        f'<p class="subtitle"><mark>{html.escape(label)}</mark>　{html.escape(subtitle)}</p>',
        "</header>",
        '<nav aria-label="目錄"><details class="ipad-toc" open><summary><strong>Contents／章節導覽</strong></summary>',
        toc,
        "</details></nav>",
        ipad_read_guide_html(not reference),
    ]


def render_firmware_tutorial_html(
    report: dict, claims: list[dict], figures: list[dict]
) -> str:
    by_id = {item["id"]: item for item in claims if item["figure"] is None}

    def add(ids: list[str]) -> list[str]:
        result: list[str] = []
        for claim_id in ids:
            result.extend(fw_claim_html(by_id[claim_id]))
        return result

    toc = """<ol>
<li><a href="#promise">這份教學要回答什麼</a></li>
<li><a href="#words">先把縮寫變成人話</a></li>
<li><a href="#model">Mental Model：四種 firmware 狀態</a></li>
<li><a href="#download-story">Download：bytes 如何變成 NUMD／OFST</a></li>
<li><a href="#commit-story">Commit：CA 如何決定 activation</a></li>
<li><a href="#verify-story">LID 03h：怎麼知道更新成功</a></li>
<li><a href="#example-story">End-to-End Example</a></li>
<li><a href="#debug-story">Debug：從症狀反推哪一步錯</a></li>
<li><a href="#tutorial-sources">來源與限制</a></li>
</ol>"""
    out = fw_html_shell_start(
        report,
        "新手教學版｜iPad／Desktop",
        "先理解狀態與因果，再看 command 欄位",
        toc,
    )
    out.extend(
        [
            '<section id="promise"><h2>這份教學要回答什麼</h2>',
            '<fieldset><legend><strong>讀完應該能做到</strong></legend>',
            "<p>看到一個 firmware image 時，能判斷它目前只是下載中、已放進 slot、已排定 activation，還是已經在執行；能算出 Firmware Image Download 與 LID 03h 的 command 欄位；也能從 completion status、AFI 與 FRSx 找出 Debug 下一步。</p>",
            "</fieldset>",
            "<p>全文只教 Base 2.4 §3.11、§5.2.9、§5.2.10 與 Firmware Slot Information（LID 03h）。其他 log pages 不混進來。讀者可先把 <em>firmware update</em> 想成搬家：Download 是把箱子搬到門口，Commit 是驗收並放進指定房間，Activation 才是正式入住；LID 03h 是入住後的門牌與房間清冊。</p>",
            "</section><hr>",
            '<section id="words"><h2>先把縮寫變成人話</h2>',
            "<p>後面第一次看到縮寫時，不必猜。先用這張表建立最低限度的字彙；每個縮寫的 bit、unit 與例外會在真正使用它的流程中再教一次。</p>",
            '<table border="1" cellpadding="8" cellspacing="0" width="100%"><thead><tr><th>先懂這四個詞</th><th>它在流程中的角色</th></tr></thead><tbody>',
            "<tr><td>Firmware image</td><td>被 download、驗證與 activation 的內容</td></tr>",
            "<tr><td>Firmware slot</td><td>保存 image 的位置；有內容不等於 active</td></tr>",
            "<tr><td>Domain</td><td>多個 controllers 共用 slots 的範圍</td></tr>",
            "<tr><td>Activation</td><td>讓 slot image 真正開始執行</td></tr>",
            "</tbody></table>",
            '<details><summary><strong>需要時展開：完整縮寫表</strong></summary>',
            fw_glossary_html(claims),
            "</details>",
            '<p><a href="#top">回到目錄</a></p></section><hr>',
            report_visual_atlas_html("base-admin-fw-logs", claims, "fw-visual-atlas", True),
            '<section id="model"><h2>Mental Model：先分清楚四種 firmware 狀態</h2>',
            firmware_mental_model_svg(),
            "<p>一個 downloaded image 還不屬於任何可執行狀態；Firmware Commit 驗證它，並依 Commit Action（CA）決定要放置、排定 activation，或立即 activation。Firmware slot 則是 domain 共享的容器，所以 Debug 不可只看發出 command 的 PCI Function。</p>",
            "<p>Multi-Domain Subsystem（MDS）bit 告訴 host 是否有多個 domains；Domain Identifier（DID）標出 controller 所屬 domain；UUID List（ULIST）bit 則表示是否支援 UUID List reporting。</p>",
        ]
    )
    out.extend(add(["BASEFWLOG-MODEL-DOMAIN", "BASEFWLOG-CAP-MDS-ULIST"]))
    out.extend(
        [
            '<fieldset><legend><strong>[解釋] 開始前先讀能力</strong></legend>',
            "<p><code>FRMW</code> 告訴你有幾個 slots、slot 1 能不能寫、能不能免 reset activation；<code>FWUG</code> 決定 download 切片要怎麼對齊；<code>MTFA</code> 與 <code>MPTFAWR</code> 則是兩種不同時間概念。先讀能力，後面的 command 才有合法參數。</p>",
            "</fieldset>",
        ]
    )
    out.extend(
        add(
            [
                "BASEFWLOG-CAP-FRMW",
                "BASEFWLOG-CAP-FWUG",
                "BASEFWLOG-CAP-MTFA",
                "BASEFWLOG-CAP-MPTFAWR",
            ]
        )
    )
    out.extend(
        [
            "<p><strong>[推論]</strong> 建議在 driver log 中把 FRMW、FWUG、MTFA、MPTFAWR 與 DID 當成同一份 update context；否則後面只留下 command bytes，無法判斷參數當時是否合法。</p>",
            '<fieldset><legend><strong>來源導覽</strong></legend><p>Identify Controller：Figure 338；本教學使用 FR（文件/PDF 340/366）、MDS／ULIST（346/372）、FRMW（354/380）、MTFA（357/383）、FWUG（359/385）、DID／MPTFAWR（364/390）。</p></fieldset>',
            '<p><a href="#top">回到目錄</a></p></section><hr>',
            '<section id="download-story"><h2>Download：bytes 如何變成 NUMD／OFST</h2>',
            "<p>Controller 不知道「第 2 個檔案區塊」；它只知道這一筆 command 從 image 的哪個 dword 開始，以及總共有幾個 dwords。這就是 <code>OFST</code> 與 <code>NUMD</code>。</p>",
            '''<pre aria-label="Firmware image portion layout">image byte 0
│
├── portion A: OFST=0       ── 4 KiB
├── portion B: OFST=0400h   ── 4 KiB
└── portion C: OFST=0800h   ── 4 KiB</pre>''',
            '<fieldset><legend><strong>0\'s-based 不要心算</strong></legend>',
            "<p><samp>actual dwords = NUMD + 1</samp><br><samp>transfer bytes = (NUMD + 1) × 4</samp><br><samp>image byte offset = OFST × 4</samp></p>",
            "</fieldset>",
            '<fieldset><legend><strong>來源導覽</strong></legend><p>Common Command Format：Figure 93，文件頁 140-142／PDF 頁 166-168。Firmware Image Download：Figures 190-193，文件頁 205-206／PDF 頁 231-232。</p></fieldset>',
        ]
    )
    out.extend(
        add(
            [
                "BASEFWLOG-FW-SEQUENCE",
                "BASEFWLOG-DOWNLOAD-RANGE",
                "BASEFWLOG-DOWNLOAD-FIELDS",
                "BASEFWLOG-FW-DISCARD",
            ]
        )
    )
    out.extend(
        [
            '<fieldset><legend><strong>[說明性範例] 一段 4 KiB</strong></legend>',
            "<p>4096 bytes ÷ 4 = 1024 dwords，所以 <code>NUMD=1024−1=1023=03FFh</code>。第二段從 byte 4096 開始，所以 <code>OFST=4096÷4=1024=0400h</code>。若 FWUG=1h，這組 length 與 offset 同時符合 4 KiB granularity／alignment。</p>",
            "</fieldset>",
            '<p><a href="#top">回到目錄</a></p></section><hr>',
            '<section id="commit-story"><h2>Commit：CA 如何決定 activation</h2>',
            "<p>Download 完成只代表 controller 收到 image portions。Firmware Commit 才驗證 image 並選 slot；CA（Commit Action）再決定成功後的狀態轉移。</p>",
            '<table border="1" cellpadding="8" cellspacing="0" width="100%"><thead><tr><th>CA</th><th>放進 slot</th><th>何時 active</th><th>接著觀察</th></tr></thead><tbody>',
            "<tr><td>000b</td><td>是</td><td>不 activation</td><td>FRSx</td></tr>",
            "<tr><td>001b</td><td>是</td><td>下次合適 CLR</td><td>NAFS → reset → CAFS</td></tr>",
            "<tr><td>010b</td><td>使用既有 slot</td><td>下次合適 CLR</td><td>NAFS → reset → CAFS</td></tr>",
            "<tr><td>011b</td><td>新 image 或既有 slot</td><td>立即</td><td>command completion → CAFS</td></tr>",
            "</tbody></table>",
        ]
    )
    out.extend(
        add(
            [
                "BASEFWLOG-COMMIT-PURPOSE",
                "BASEFWLOG-COMMIT-CDW10",
                "BASEFWLOG-COMMIT-MUD",
                "BASEFWLOG-COMMIT-STATUS",
                "BASEFWLOG-FW-RESET",
                "BASEFWLOG-FW-IMMEDIATE",
                "BASEFWLOG-FW-FAILURE",
                "BASEFWLOG-RESET-XREF",
            ]
        )
    )
    out.extend(
        [
            '<fieldset><legend><strong>[警告] Success 不等於現在已 active</strong></legend>',
            "<p>CA=000b 只放置；CA=001b／010b 仍欠一次能觸發 activation 的 CLR；CA=011b 才是立即路徑，而且 command 會等到成功或失敗。Completion status 若點名 Conventional Reset，就不能拿 FLR 當同義詞。</p>",
            "</fieldset>",
            '<fieldset><legend><strong>來源導覽</strong></legend><p>Firmware Commit CDW10、CQE.DW0 與 status：Figures 187-189，文件頁 203-205／PDF 頁 229-231。Activation event／enable：Figures 155、474，文件/PDF 頁 186/212、466-468/492-494。</p></fieldset>',
            '<details><summary><strong>進階但必要：UUID List 為什麼可能強迫 reset</strong></summary>',
        ]
    )
    out.extend(add(["BASEFWLOG-UUID-LIST", "BASEFWLOG-UUID-RESET"]))
    out.extend(
        [
            "<p>[解釋] UUID Index 是位置型語意；同一 entry 換成不同有效 UUID，舊 command 的 index 可能指向不同意義，因此 affected controllers 必須一起跨過 reset 邊界。</p></details>",
            '<p><a href="#top">回到目錄</a></p></section><hr>',
            '<section id="verify-story"><h2>LID 03h：怎麼知道更新成功</h2>',
            "<p>LID 是 Log Page Identifier；03h 指 Firmware Slot Information。它固定回傳 512 bytes。AFI 告訴你 current／next active slot，FRS1 到 FRS7 則是每個 slot 的 8-byte ASCII revision。</p>",
            firmware_afi_svg(),
            '<fieldset><legend><strong>完整讀取 LID 03h 的 command</strong></legend>',
            "<p><code>NSID=0h</code>；PRP 指向 512-byte buffer；512 bytes=128 dwords，所以 <code>NUMD=127=007Fh</code>；<code>LID=03h</code>、<code>LSP=0</code>、<code>RAE=0</code>，因此 <code>CDW10=007F0003h</code>。</p>",
            "</fieldset>",
        ]
    )
    out.extend(
        add(
            [
                "BASEFWLOG-LOG-COMMAND",
                "BASEFWLOG-LOG-LENGTH",
                "BASEFWLOG-LOG-RAE",
                "BASEFWLOG-LOG-SCOPE",
                "BASEFWLOG-LID03-DESCRIPTION",
                "BASEFWLOG-LID03-AFI",
                "BASEFWLOG-LID03-FRS",
            ]
        )
    )
    out.extend(
        [
            '<fieldset><legend><strong>[說明性範例] AFI=21h</strong></legend>',
            "<p><code>NAFS=(21h≫4)&amp;7=2</code>，<code>CAFS=21h&amp;7=1</code>。意思是目前從 slot 1 執行，controller 指出 slot 2 會在下一次合適 CLR activation。它不是「slot 2 已 active」。</p>",
            "</fieldset>",
            '<fieldset><legend><strong>來源導覽</strong></legend><p>Get Log Page command：Figures 203-208，文件頁 213-215／PDF 頁 239-241；LID 03h row：Figure 209，文件/PDF 頁 215/241；Firmware Slot Information layout：Figure 215，文件/PDF 頁 226/252。</p></fieldset>',
            '<p><a href="#top">回到目錄</a></p></section><hr>',
            '<section id="example-story"><h2>End-to-End Example：12 KiB image 更新到 slot 2</h2>',
            '<table border="1" cellpadding="8" cellspacing="0" width="100%"><thead><tr><th>階段</th><th>具體值</th><th>成功後狀態</th></tr></thead><tbody>',
            "<tr><td>Read capability</td><td>NOFS=3、FFSRO=1、FWUG=1h</td><td>選可寫 slot 2；4 KiB 對齊</td></tr>",
            "<tr><td>Download ×3</td><td>NUMD=03FFh；OFST=0／0400h／0800h</td><td>12 KiB portions 已下載，尚未 commit</td></tr>",
            "<tr><td>Commit</td><td>CA=001b、FS=2；CDW10=0000000Ah</td><td>slot 2 已放置，排定下次 CLR</td></tr>",
            "<tr><td>Pre-reset LID 03h</td><td>CDW10=007F0003h；例如 AFI=21h</td><td>CAFS=1、NAFS=2</td></tr>",
            "<tr><td>Required reset</td><td>依完整 SCT／SC 選 reset</td><td>重新初始化 controller／I/O queues</td></tr>",
            "<tr><td>Post-reset verify</td><td>CAFS=2；FRS2 與 Identify.FR 相符</td><td>slot 2 正在執行</td></tr>",
            "</tbody></table>",
            "<p><strong>[推論]</strong> FRS2 正確但 CAFS 仍為 1，通常代表 placement 已成功、activation 邊界尚未完成；先查 CA、Firmware Commit status 與真正執行的 reset 類型。</p>",
            '<p><a href="#top">回到目錄</a></p></section><hr>',
            '<section id="debug-story"><h2>Debug：從症狀反推哪一步錯</h2>',
            '<svg width="100%" height="270" viewBox="0 0 820 270" role="img" aria-labelledby="debug-title debug-desc"><title id="debug-title">Firmware update debug decision flow</title><desc id="debug-desc">A decision flow from download failure through commit status and LID 03h verification.</desc><defs><marker id="debug-arrow" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="currentColor"/></marker></defs><rect x="20" y="20" width="180" height="55" fill="none" stroke="currentColor"/><text x="110" y="52" text-anchor="middle" fill="currentColor">Download failed?</text><rect x="250" y="20" width="220" height="55" fill="none" stroke="currentColor"/><text x="360" y="44" text-anchor="middle" fill="currentColor">NUMD / OFST / FWUG</text><text x="360" y="63" text-anchor="middle" fill="currentColor">PRP + overlap</text><line x1="200" y1="47" x2="248" y2="47" stroke="currentColor" marker-end="url(#debug-arrow)"/><rect x="20" y="108" width="180" height="55" fill="none" stroke="currentColor"/><text x="110" y="140" text-anchor="middle" fill="currentColor">Commit failed?</text><rect x="250" y="108" width="220" height="55" fill="none" stroke="currentColor"/><text x="360" y="132" text-anchor="middle" fill="currentColor">SCT / SC + MUD</text><text x="360" y="151" text-anchor="middle" fill="currentColor">NOFS / FFSRO / CA</text><line x1="200" y1="135" x2="248" y2="135" stroke="currentColor" marker-end="url(#debug-arrow)"/><rect x="20" y="196" width="180" height="55" fill="none" stroke="currentColor"/><text x="110" y="228" text-anchor="middle" fill="currentColor">Verify mismatch?</text><rect x="250" y="196" width="220" height="55" fill="none" stroke="currentColor"/><text x="360" y="220" text-anchor="middle" fill="currentColor">DID + CAFS / NAFS</text><text x="360" y="239" text-anchor="middle" fill="currentColor">FRSx + Identify.FR</text><line x1="200" y1="223" x2="248" y2="223" stroke="currentColor" marker-end="url(#debug-arrow)"/><path d="M470,47 C650,47 650,223 472,223" fill="none" stroke="currentColor" marker-end="url(#debug-arrow)"/><text x="650" y="130" text-anchor="middle" fill="currentColor">record every boundary</text></svg>',
            '<table border="1" cellpadding="8" cellspacing="0" width="100%"><thead><tr><th>症狀</th><th>第一個要看的證據</th><th>不要先做什麼</th></tr></thead><tbody>',
            "<tr><td>Invalid Field during Download</td><td>(NUMD+1)×4、OFST×4、FWUG、PRP</td><td>不要直接縮小 random chunk 重試</td></tr>",
            "<tr><td>Invalid Firmware Slot</td><td>NOFS、FFSRO、FS</td><td>不要假設 slot 1 可寫</td></tr>",
            "<tr><td>Reset-required status</td><td>完整 SCT／SC</td><td>不要把 FLR、CLR、Conventional Reset 混用</td></tr>",
            "<tr><td>FRS2 有值但 CAFS=1</td><td>CA、NAFS、reset 類型</td><td>不要再次 download 同一 image</td></tr>",
            "<tr><td>讀到另一組 slot 狀態</td><td>MDS、DID、處理 command 的 controller</td><td>不要只用 PCI Function 當 scope</td></tr>",
            "</tbody></table>",
            "<p><strong>最小紀錄集合：</strong>FRMW、FWUG、MTFA、MPTFAWR、DID、每筆 NUMD／OFST、Commit CDW10、完整 CQE status／MUD、實際 reset 類型、activation 前後的 512-byte LID 03h。</p>",
            '<p><a href="#top">回到目錄</a></p></section><hr>',
            *firmware_figure_appendix_html(claims, figures, tutorial=True),
            '<section id="tutorial-sources"><h2>來源與限制</h2>',
            f"<p>{html.escape(report['range'])}。</p>",
            "<p>NVM Express Base Specification, Revision 2.4。另以 NVM Express NVMe over PCIe Transport Specification, Revision 1.4, §3.3, 文件／PDF 頁 11，辨識 Conventional Reset 與 Function Level Reset。</p>",
            "<p>未納入其他 Errata、ECN、Technical Proposal、controller vendor 文件或 PCI Express Base Specification 原文。若來源集合改變，應以頁內 claim ID 重新核對。</p>",
            '<p><a href="#top">回到目錄</a></p></section>',
            "</main></body></html>",
            "",
        ]
    )
    return "\n".join(out)


def render_firmware_reference_html(
    report: dict, claims: list[dict], figures: list[dict]
) -> str:
    by_id = {item["id"]: item for item in claims if item["figure"] is None}
    toc = """<ol>
<li><a href="#ref-start">End-to-End 一頁式操作順序</a></li>
<li><a href="#ref-glossary">縮寫與能力欄位</a></li>
<li><a href="#ref-download">Firmware Image Download</a></li>
<li><a href="#ref-commit">Firmware Commit／status</a></li>
<li><a href="#ref-lid03">Get Log Page LID 03h</a></li>
<li><a href="#ref-debug">Debug lookup</a></li>
<li><a href="#ref-claims">Normative／source detail</a></li>
<li><a href="#appendix">完整 Figure evidence appendix</a></li>
</ol>"""
    out = fw_html_shell_start(
        report,
        "快速查詢詳細手冊｜iPad／Desktop",
        "先查欄位與 status，再展開來源證據",
        toc,
    )
    out.extend(
        [
            '<section id="ref-first-words"><h2>快查前先對齊縮寫</h2>',
            '<p>先確認欄位名稱與工程角色，再進入一頁式操作順序；完整 glossary 與每個 bit／unit 仍保留在後方。</p>',
            fw_glossary_html(claims, compact=True),
            '<p><a href="#top">回到目錄</a></p></section><hr>',
            '<section id="ref-start"><h2>End-to-End 一頁式操作順序</h2>',
            '<table border="1" cellpadding="8" cellspacing="0" width="100%"><thead><tr><th>階段</th><th>必要輸入／欄位</th><th>完成證據</th><th>失敗先查</th></tr></thead><tbody>',
            "<tr><td>1. Capability</td><td>FRMW、FWUG、MTFA、MPTFAWR、MDS／DID</td><td>選出合法 slot／chunk／activation path</td><td>NOFS、FFSRO、FAWR</td></tr>",
            "<tr><td>2. Download</td><td>PRP、NUMD、OFST</td><td>每筆 Admin CQE success</td><td>0's-based、alignment、overlap</td></tr>",
            "<tr><td>3. Commit</td><td>CA、FS、必要時 BPID</td><td>CQE SCT／SC＋MUD</td><td>slot、image、reset status</td></tr>",
            "<tr><td>4. Activate</td><td>立即或指定 reset</td><td>controller／queues 重新可用</td><td>MTFA、MPTFAWR、reset 類型</td></tr>",
            "<tr><td>5. Verify</td><td>NSID=0、LID=03h、NUMD=127</td><td>CAFS／FRSx／Identify.FR 一致</td><td>domain、NAFS、buffer layout</td></tr>",
            "</tbody></table>",
            '<fieldset><legend><strong>Golden command</strong></legend><p>LID 03h full read：<code>NSID=00000000h</code>、<code>CDW10=007F0003h</code>、<code>CDW11-14=00000000h</code>、PRP 指向至少 512-byte destination buffer。</p></fieldset>',
            '<p><a href="#top">回到目錄</a></p></section><hr>',
            '<section id="ref-glossary"><h2>縮寫與能力欄位</h2>',
            fw_glossary_html(claims),
            '<p><a href="#top">回到目錄</a></p></section><hr>',
            report_visual_atlas_html("base-admin-fw-logs", claims, "fw-visual-atlas", False),
            '<section id="ref-download"><h2>Firmware Image Download 快查</h2>',
            '<table border="1" cellpadding="8" cellspacing="0" width="100%"><thead><tr><th>位置</th><th>欄位</th><th>公式／規則</th><th>錯誤風險</th></tr></thead><tbody>',
            "<tr><td>DPTR</td><td>PRP1／PRP2</td><td>NVMe/PCIe Admin 不使用 SGL</td><td>page crossing／buffer direction</td></tr>",
            "<tr><td>CDW10[31:0]</td><td>NUMD</td><td>bytes=(NUMD+1)×4</td><td>off-by-one、FWUG</td></tr>",
            "<tr><td>CDW11[31:0]</td><td>OFST</td><td>byte offset=OFST×4</td><td>first portion shall 0h</td></tr>",
            "<tr><td>CQE SC=14h</td><td>Overlapping Range</td><td>ranges overlap 或 granularity/alignment 問題</td><td>先重建 byte intervals</td></tr>",
            "</tbody></table>",
            '''<pre>4 KiB portion: 4096 / 4 = 1024 dwords → NUMD = 1023 = 03FFh
portion at byte 8192: 8192 / 4 = OFST 2048 = 0800h</pre>''',
            '<p><a href="#top">回到目錄</a></p></section><hr>',
            '<section id="ref-commit"><h2>Firmware Commit／status 快查</h2>',
            '<table border="1" cellpadding="8" cellspacing="0" width="100%"><thead><tr><th>CA</th><th>定義</th><th>FS</th><th>activation</th></tr></thead><tbody>',
            "<tr><td>000b</td><td>Downloaded image 取代 slot image</td><td>0=controller 選；1-7=指定</td><td>不 activation</td></tr>",
            "<tr><td>001b</td><td>Downloaded image 取代 slot image</td><td>同左</td><td>下次合適 CLR</td></tr>",
            "<tr><td>010b</td><td>使用既有 slot image</td><td>指定既有 slot</td><td>下次合適 CLR</td></tr>",
            "<tr><td>011b</td><td>Downloaded 或既有 slot image</td><td>指定 slot</td><td>立即；非 background</td></tr>",
            "<tr><td>100b-101b</td><td>Reserved</td><td>—</td><td>—</td></tr>",
            "<tr><td>110b／111b</td><td>replace／activate Boot Partition</td><td>由 BPID 選</td><td>Boot Partition path</td></tr>",
            "</tbody></table>",
            '<h3>Command-specific status（SCT=1h）</h3>',
            '<table border="1" cellpadding="8" cellspacing="0" width="100%"><thead><tr><th>SC</th><th>名稱</th><th>工程含意</th></tr></thead><tbody>',
            "<tr><td>06h</td><td>Invalid Firmware Slot</td><td>slot invalid、read-only 或超過 NOFS</td></tr>",
            "<tr><td>07h</td><td>Invalid Firmware Image</td><td>image invalid／未載入，或 slot 無 image</td></tr>",
            "<tr><td>0Bh</td><td>Requires Conventional Reset</td><td>先做 FLR／Controller Reset 仍繼續舊 image</td></tr>",
            "<tr><td>10h</td><td>Requires NVM Subsystem Reset</td><td>其他 CLR 仍繼續舊 image</td></tr>",
            "<tr><td>11h</td><td>Requires Controller Level Reset</td><td>下次 CLR activation；用於 CA=011b path</td></tr>",
            "<tr><td>12h</td><td>Maximum Time Violation</td><td>已 commit、未 active；可用 CA=010b 排定</td></tr>",
            "<tr><td>13h</td><td>Activation Prohibited</td><td>vendor-specific 禁止 activation</td></tr>",
            "<tr><td>14h</td><td>Overlapping Range</td><td>download ranges overlap</td></tr>",
            "<tr><td>1Eh</td><td>Boot Partition Write Prohibited</td><td>write locked</td></tr>",
            "<tr><td>3Dh</td><td>Manufacturing Default Personality Required</td><td>firmware 與 personality settings 不相容</td></tr>",
            "</tbody></table>",
            '<p><a href="#top">回到目錄</a></p></section><hr>',
            '<section id="ref-lid03"><h2>Get Log Page LID 03h 快查</h2>',
            firmware_afi_svg(),
            '<table border="1" cellpadding="8" cellspacing="0" width="100%"><thead><tr><th>位置</th><th>欄位</th><th>值／解碼</th><th>限制</th></tr></thead><tbody>',
            "<tr><td>Common NSID</td><td>NSID</td><td>0h</td><td>未使用 namespace</td></tr>",
            "<tr><td>CDW10[31:16]</td><td>NUMDL</td><td>007Fh</td><td>128 dwords，0's-based</td></tr>",
            "<tr><td>CDW10[15]</td><td>RAE</td><td>0=清 event；1=保留</td><td>失敗時 shall retain</td></tr>",
            "<tr><td>CDW10[14:8]</td><td>LSP</td><td>0h</td><td>LID 03h 未定義</td></tr>",
            "<tr><td>CDW10[7:0]</td><td>LID</td><td>03h</td><td>Firmware Slot Information</td></tr>",
            "<tr><td>CDW11-14</td><td>NUMDU／offset／selector</td><td>full read 時 0h</td><td>CSI=N、OT=0、UIDX=0</td></tr>",
            "<tr><td>byte 0</td><td>AFI</td><td>NAFS=[6:4]、CAFS=[2:0]</td><td>bits 7、3 reserved</td></tr>",
            "<tr><td>bytes 8:63</td><td>FRS1-FRS7</td><td>各 8-byte ASCII</td><td>invalid／unsupported shall 0h</td></tr>",
            "<tr><td>bytes 1:7、64:511</td><td>Reserved</td><td>不解析</td><td>不可當額外 slot</td></tr>",
            "</tbody></table>",
            '<p><a href="#top">回到目錄</a></p></section><hr>',
            '<section id="ref-debug"><h2>Debug lookup</h2>',
            '<table border="1" cellpadding="8" cellspacing="0" width="100%"><thead><tr><th>症狀</th><th>欄位／證據</th><th>判斷</th><th>動作</th></tr></thead><tbody>',
            "<tr><td>Download Invalid Field</td><td>PRP、NUMD、OFST、FWUG</td><td>length／alignment</td><td>以 bytes 重算</td></tr>",
            "<tr><td>MUD≠0</td><td>MEFWO／ASQFWO</td><td>不同 interface／queue overlap</td><td>序列化 update</td></tr>",
            "<tr><td>Commit SC 0Bh／10h／11h</td><td>完整 SC</td><td>reset scope 不同</td><td>執行指定 reset</td></tr>",
            "<tr><td>NAFS 正確、CAFS 未變</td><td>CA、SC、reset trace</td><td>pending 未跨 activation boundary</td><td>確認 reset 方法</td></tr>",
            "<tr><td>FRSx=0h</td><td>NOFS、slot validity</td><td>unsupported／no valid revision</td><td>不要解成 ASCII</td></tr>",
            "<tr><td>不同 controller 結果不同</td><td>MDS、DID</td><td>可能跨 domain</td><td>在同 domain 比較</td></tr>",
            "</tbody></table>",
            '<p><a href="#top">回到目錄</a></p></section><hr>',
            '<section id="ref-claims"><h2>Normative／source detail</h2>',
            "<p>[SPEC] 段落是可追溯的規格轉述；[推論] 與表格中的工程動作不提高 requirement 強度。依主題展開，避免快速查詢頁被長文淹沒。</p>",
        ]
    )
    for part in FIRMWARE_PARTS:
        out.extend(
            [
                f"<details><summary><strong>{html.escape(part['zh'])}</strong></summary>",
                "<p><strong>[解釋]</strong> " + html.escape(part["intro_zh"]) + "</p>",
            ]
        )
        for claim_id in part["claims"]:
            item = by_id[claim_id]
            out.extend([f"<h3>{html.escape(item['heading_zh_tw'])}</h3>"])
            out.extend(fw_claim_html(item))
        out.extend(
            [
                "<p><strong>[推論]</strong> " + html.escape(part["inference_zh"]) + "</p>",
                "</details>",
            ]
        )
    out.extend(['<p><a href="#top">回到目錄</a></p></section><hr>'])
    out.extend(firmware_figure_appendix_html(claims, figures))
    out.extend(
        [
            '<section><h2>來源與限制</h2>',
            f"<p>{html.escape(report['range'])}。</p>",
            "<p>NVM Express Base Specification, Revision 2.4；NVM Express NVMe over PCIe Transport Specification, Revision 1.4（僅 §3.3）。查證日期：2026-09-01。</p>",
            "<p>未納入額外 Errata、ECN、Technical Proposal、controller vendor 文件或 PCI Express Base Specification 原文。</p>",
            '<p><a href="#top">回到目錄</a></p></section>',
            "</main></body></html>",
            "",
        ]
    )
    return "\n".join(out)


def render_firmware_html(
    report: dict, claims: list[dict], figures: list[dict], tutorial: bool
) -> str:
    label = "新手教學版" if tutorial else "詳細 Spec 版"
    claims_by_id = {item["id"]: item for item in claims if item["figure"] is None}
    toc = "".join(
        f'<li><a href="#{part["id"]}">{html.escape(part["zh"])}</a></li>'
        for part in FIRMWARE_PARTS
    )
    parts = [
        "<!doctype html>",
        '<html lang="zh-Hant-TW">',
        "<head>",
        '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        f"<title>{html.escape(report['title_zh'])}｜{label}</title>",
        "</head>",
        "<body>",
        '<header id="top">',
        f"<h1>{html.escape(report['title_zh'])}</h1>",
        f"<p><strong>{label}</strong>｜從 Firmware Image Download 到 LID 03h 驗證的工程教學</p>",
        "<p>讀者前提：已理解 NVMe Admin Queue、SQE／CQE、Controller Level Reset 與 Identify 基礎。</p>",
        "</header>",
        '<nav aria-label="目錄"><details open><summary><strong>Contents／章節導覽</strong></summary><ol>',
        '<li><a href="#scope">範圍、來源與閱讀語意</a></li>',
        toc,
        '<li><a href="#example">End-to-End Example</a></li>',
        '<li><a href="#debug">Debug Decision Flow</a></li>',
        '<li><a href="#appendix">Appendix A — Supporting Figure／Field Reference</a></li>',
        "</ol></details></nav>",
        "<main>",
        '<section id="scope"><h2>範圍、來源與閱讀語意</h2>',
        f"<p><strong>納入：</strong>{html.escape(report['range'])}。</p>",
        "<p><strong>明確不納入：</strong>其他 LID、未核准的傳輸專屬內容、NVM Command Set 1.3，以及 Boot Partition 的完整功能流程。BPID 與 CA=110b／111b 只作 §5.2.9／§5.2.10 cross-reference。</p>",
        "<table><thead><tr><th>標記</th><th>用途</th><th>能否視為 requirement</th></tr></thead><tbody>",
        "<tr><td>[SPEC]</td><td>規格明文的精確轉述，保留 shall／may／should</td><td>依原 keyword</td></tr>",
        "<tr><td>[解釋]</td><td>把多個欄位連成可理解的機制</td><td>否</td></tr>",
        "<tr><td>[推論]</td><td>依 Spec 導出的工程實作含意</td><td>否</td></tr>",
        "<tr><td>[說明性範例]</td><td>協助計算與 Debug 的具體數值</td><td>否</td></tr>",
        "</tbody></table>",
        "<p><strong>規範強度：</strong><code>shall／shall not</code> 是強制要求；<code>should／should not</code> 是有偏好的建議；<code>may</code> 表示允許選擇；<code>reserved</code> 不得自行賦予意義。</p>",
        "<p><strong>來源：</strong>NVM Express Base Specification, Revision 2.4；NVMe over PCIe Transport Specification, Revision 1.4（僅 §3.3 reset 名稱）。查證日期：2026-09-01。</p>",
        "</section>",
        '<section aria-labelledby="model-picture"><h2 id="model-picture">一張圖先看完整故事</h2>',
        firmware_mental_model_svg(),
        "<p><strong>[解釋]</strong> Download 只建立暫存 portions；Commit 才把 image 驗證並放進 slot。Activation 再把某個 slot 的 image 變成正在執行的 firmware。最後以 Identify.FR 與 LID 03h 觀察結果。</p>",
        "</section>",
    ]
    for part in FIRMWARE_PARTS:
        parts.extend(
            [
                f'<section id="{part["id"]}"><h2>{html.escape(part["zh"])}</h2>',
                "<p><strong>[解釋]</strong> " + html.escape(part["intro_zh"]) + "</p>",
            ]
        )
        if part["id"] == "mental-model":
            parts.extend(
                [
                    "<table><thead><tr><th>物件／欄位</th><th>它回答什麼</th><th>Debug 時何時讀</th></tr></thead><tbody>",
                    "<tr><td>FRMW／FWUG／MTFA／MPTFAWR</td><td>能做什麼、限制與時間</td><td>任何 download 前</td></tr>",
                    "<tr><td>Downloaded portions</td><td>尚未 commit 的 image ranges</td><td>download／overlap 錯誤</td></tr>",
                    "<tr><td>Firmware slot</td><td>已保存但不一定 active 的 image</td><td>commit 與 LID 03h</td></tr>",
                    "<tr><td>Identify.FR＋AFI／FRSx</td><td>目前執行者與 slot 狀態</td><td>activation 後驗證</td></tr>",
                    "</tbody></table>",
                ]
            )
        if part["id"] == "commit-activate":
            parts.extend(
                [
                    "<table><thead><tr><th>CA</th><th>對 slot 的動作</th><th>activation 時點</th><th>LID 03h 觀察重點</th></tr></thead><tbody>",
                    "<tr><td>000b</td><td>放置 downloaded image</td><td>不 activation</td><td>FRSx 可變，CAFS 不因此改變</td></tr>",
                    "<tr><td>001b</td><td>放置 downloaded image</td><td>下次合適 CLR</td><td>reset 前看 NAFS；後看 CAFS</td></tr>",
                    "<tr><td>010b</td><td>使用既有 slot</td><td>下次合適 CLR</td><td>reset 前看 NAFS；後看 CAFS</td></tr>",
                    "<tr><td>011b</td><td>放置或使用既有 slot</td><td>立即；command 等到結果</td><td>完成後重新讀 CAFS／FRSx</td></tr>",
                    "</tbody></table>",
                ]
            )
        if part["id"] == "lid03":
            parts.extend([firmware_afi_svg()])
        for item_id in part["claims"]:
            item = claims_by_id[item_id]
            parts.extend(
                [
                    f"<article><h3>{html.escape(item['heading_zh_tw'])}</h3>",
                    f'<p><strong>[SPEC]</strong> <span data-claim-id="{item["id"]}">{html.escape(item["zh_tw"])}</span></p>',
                    f"<p><small>{html.escape(item['citation_zh_tw'])}</small></p>",
                    "</article>",
                ]
            )
        parts.extend(
            [
                "<p><strong>[推論]</strong> " + html.escape(part["inference_zh"]) + "</p>",
                '<p><a href="#top">回到目錄</a></p></section>',
            ]
        )
    parts.extend(
        [
            '<section id="example"><h2>End-to-End Example：12 KiB image，slot 2，下次 CLR 啟用</h2>',
            "<p><strong>[說明性範例]</strong> 假設 Identify 回報 <code>NOFS=3</code>、<code>FFSRO=1</code>、<code>FWUG=1h</code>，目前 LID 03h 為 <code>CAFS=1</code>。選 slot 2 可避開 read-only slot 1；FWUG=1h 代表 4 KiB granularity／alignment。</p>",
            "<ol><li>將 12 KiB 切成三個 4 KiB portions。每段 4096 bytes=1024 dwords，所以 <code>NUMD=1024-1=1023=000003FFh</code>。</li><li>三段的 <code>OFST</code> 依序為 <code>00000000h</code>、<code>00000400h</code>、<code>00000800h</code>；byte offsets 分別是 0、4096、8192。</li><li>送出 Firmware Commit：<code>CA=001b</code>、<code>FS=010b</code>，所以 <code>CDW10=0000000Ah</code>。成功只表示已排定下次合適 CLR，不表示 slot 2 已在執行。</li><li>reset 前讀完整 LID 03h：512 bytes=128 dwords，<code>NUMD=127</code>，<code>CDW10=007F0003h</code>。若 AFI=<code>21h</code>，則 <code>NAFS=2</code>、<code>CAFS=1</code>。</li><li>執行 Firmware Commit status 所要求且能觸發 activation 的 reset，重新初始化 controller／I/O queues，再讀 Identify.FR 與 LID 03h；確認 <code>CAFS=2</code> 且 FRS2 是預期 revision。</li></ol>",
            "<p><strong>[推論]</strong> 若 reset 後 FRS2 正確但 CAFS 仍為 1，代表 image 已在 slot 2，卻沒有完成預期的 activation；優先檢查 CA、completion status 與實際 reset 類型。</p>",
            '<p><a href="#top">回到目錄</a></p></section>',
            '<section id="debug"><h2>Debug Decision Flow</h2>',
            "<table><thead><tr><th>觀察點</th><th>先檢查</th><th>常見誤解</th><th>下一步</th></tr></thead><tbody>",
            "<tr><td>Download 回 Invalid Field</td><td>(NUMD+1)×4、OFST×4、FWUG</td><td>把 NUMD 當實際 dword 數</td><td>以 byte interval 重算 alignment</td></tr>",
            "<tr><td>Commit 回 Invalid Firmware Slot</td><td>NOFS、FFSRO、FS</td><td>slot 1 永遠可寫</td><td>改用支援且可寫的 slot</td></tr>",
            "<tr><td>Commit 要求 reset</td><td>完整 SCT／SC</td><td>所有 reset 等價</td><td>依 status 與 PCIe §3.3 選 reset</td></tr>",
            "<tr><td>LID 03h 看似沒更新</td><td>MDS／DID、處理 command 的 controller、AFI</td><td>每個 controller 有獨立 slots</td><td>回到同一 domain 核對</td></tr>",
            "<tr><td>FRSx 全零</td><td>NOFS、slot 有效性、buffer offset</td><td>零值是空字串 revision</td><td>視為 unsupported／no valid revision</td></tr>",
            "<tr><td>立即 activation timeout</td><td>MTFA、MPTFAWR、completion status</td><td>CA=011b 是背景工作</td><td>等待 command 結果並照 status recovery</td></tr>",
            "</tbody></table>",
            "<p><strong>最小紀錄集合：</strong>controller／domain identity、FRMW、FWUG、MTFA、MPTFAWR、每筆 NUMD／OFST、Commit CDW10、完整 CQE status／MUD、reset 類型、activation 前後的 512-byte LID 03h。</p>",
            '<p><a href="#top">回到目錄</a></p></section>',
        ]
    )
    if not tutorial:
        parts.extend(
            [
                '<section id="field-reference"><h2>Detailed Reference — 重要欄位速查</h2>',
                "<table><thead><tr><th>結構</th><th>欄位</th><th>encoding／unit</th><th>嚴謹注意事項</th></tr></thead><tbody>",
                "<tr><td>Firmware Image Download CDW10</td><td>NUMD[31:0]</td><td>0's-based dwords</td><td>實際 bytes=(NUMD+1)×4</td></tr>",
                "<tr><td>Firmware Image Download CDW11</td><td>OFST[31:0]</td><td>dwords</td><td>image 起點 portion shall 為 0h</td></tr>",
                "<tr><td>Firmware Commit CDW10</td><td>BPID／CA／FS</td><td>bit 31／[5:3]／[2:0]</td><td>100b-101b reserved</td></tr>",
                "<tr><td>Get Log Page CDW10</td><td>NUMDL／RAE／LSP／LID</td><td>[31:16]／15／[14:8]／[7:0]</td><td>LID 03h full read=007F0003h</td></tr>",
                "<tr><td>LID 03h byte 0</td><td>NAFS／CAFS</td><td>[6:4]／[2:0]</td><td>NAFS=0 只表示未指出 next slot</td></tr>",
                "<tr><td>LID 03h bytes 8:63</td><td>FRS1-FRS7</td><td>各 8-byte ASCII</td><td>invalid／unsupported slot shall 為 0h</td></tr>",
                "</tbody></table></section>",
            ]
        )
    parts.extend(firmware_figure_appendix_html(claims, figures))
    parts.extend(
        [
            '<section id="sources"><h2>來源與限制</h2>',
            "<p>主要來源：NVM Express Base Specification, Revision 2.4。Reset 名稱的最小外部依賴：NVM Express NVMe over PCIe Transport Specification, Revision 1.4, §3.3, 文件／PDF 頁 11。</p>",
            "<p>目前未納入額外 Errata、ECN、Technical Proposal、controller vendor 文件或 PCI Express Base Specification 原文。若 revision 或核准範圍改變，應用 claim ID 重新核對。</p>",
            '<p><a href="#top">回到目錄</a></p></section>',
            "</main>",
            "</body>",
            "</html>",
            "",
        ]
    )
    return "\n".join(parts)


def firmware_figure_appendix_markdown(
    claims: list[dict], figures: list[dict], language: str
) -> list[str]:
    english = language == "en"
    figure_claims = {
        int(item["figure"]): item for item in claims if item["figure"] is not None
    }
    out = [
        "## Appendix A — Supporting Figure / Field Reference",
        "",
        (
            "Figures are traceable evidence for the workflow, not the article outline. Dependency entries expose only the required slice; Figure 209 is limited to the LID 03h row."
            if english
            else "Figure 是主流程的可追溯證據，不是文章骨架。dependency entries 只取理解所需切片；Figure 209 只保留 LID 03h row。"
        ),
        "",
    ]
    for figure in figures:
        item = figure_claims[int(figure["number"])]
        out.extend(figure_card_markdown(figure, item, language))
    return out


def render_firmware_markdown(
    report: dict, claims: list[dict], figures: list[dict], language: str
) -> str:
    english = language == "en"
    title = report["title_en"] if english else report["title_zh"]
    description = (
        "A source-located engineering tutorial from firmware download through LID 03h verification."
        if english
        else "從 firmware download 到 LID 03h 驗證、可供 GitHub Pages 與 PPT 使用的工程教學。"
    )
    by_id = {item["id"]: item for item in claims if item["figure"] is None}
    out = [
        frontmatter("base-admin-fw-logs", title, description, language),
        f"# {title}",
        "",
        (
            "This tutorial builds an end-to-end engineering model: capability readout, image download, commit and activation, reset boundaries, and verification with Firmware Slot Information (LID 03h)."
            if english
            else "本教學建立完整工程模型：能力探測、image download、commit／activation、reset 邊界，以及用 Firmware Slot Information（LID 03h）驗證結果。"
        ),
        "",
        "## " + ("Scope and source semantics" if english else "範圍與來源語意"),
        "",
        ("Scope: " + report["range_en"] + "." if english else "範圍：" + report["range"] + "。"),
        "",
        SOURCES["NVME-BASE-2.4"]["marker"],
        "",
        SOURCES["NVME-PCIE-TRANSPORT-1.4"]["marker"]
        + (" — §3.3 reset terminology only" if english else " — 僅 §3.3 reset 名稱"),
        "",
        (
            "Excluded: every other LID, unapproved transport-specific material, NVM Command Set 1.3, and the full Boot Partition feature flow. BPID and CA=110b/111b remain only as cross-references."
            if english
            else "排除：其餘 LID、未核准的傳輸專屬內容、NVM Command Set 1.3、Boot Partition 完整功能流程；BPID 與 CA=110b／111b 只保留 cross-reference。"
        ),
        "",
        (
            "`shall` is mandatory, `should` is a preferred recommendation, `may` permits a choice, and `reserved` is not assigned an invented meaning. `[SPEC]` is a source-faithful paraphrase; `[Explanation]`, `[Inference]`, and `[Informative example]` add no requirement."
            if english
            else "`shall` 是強制要求，`should` 是有偏好的建議，`may` 表示允許選擇，`reserved` 不自行賦義。`[SPEC]` 是忠於來源的轉述；`[解釋]`、`[推論]`、`[說明性範例]` 不新增 requirement。"
        ),
        "",
        "## Mental Model",
        "",
        "```text",
        "Downloaded portions -> committed slot -> current / next active image -> Identify.FR + LID 03h",
        "```",
        "",
    ]
    for part in FIRMWARE_PARTS:
        out.extend(
            [
                f"## {part['en'] if english else part['zh']}",
                "",
                ("**[Explanation]** " if english else "**[解釋]** ")
                + (part["intro_en"] if english else part["intro_zh"]),
                "",
            ]
        )
        for item_id in part["claims"]:
            item = by_id[item_id]
            out.extend(
                [
                    f"### {item['heading_en'] if english else item['heading_zh_tw']}",
                    "",
                    f"<!-- claim:{item['id']} -->",
                    "",
                    "**[SPEC]** " + (item["en"] if english else item["zh_tw"]),
                    "",
                    "> " + (item["citation_en"] if english else item["citation_zh_tw"]),
                    "",
                ]
            )
        out.extend(
            [
                ("**[Inference]** " if english else "**[推論]** ")
                + (part["inference_en"] if english else part["inference_zh"]),
                "",
            ]
        )
    out.extend(
        [
            "## " + ("End-to-End Example" if english else "End-to-End Example：12 KiB image，slot 2，下次 CLR 啟用"),
            "",
            (
                "**[Informative example]** Assume NOFS=3, FFSRO=1, FWUG=1h, and CAFS=1. Use writable slot 2. Split 12 KiB into three 4 KiB portions. Each portion is 1024 dwords, so NUMD=1023=000003FFh; OFST values are 00000000h, 00000400h, and 00000800h. Commit with CA=001b and FS=010b, giving CDW10=0000000Ah. Before reset, read all 512 bytes of LID 03h with NUMD=127 and CDW10=007F0003h. AFI=21h decodes to NAFS=2 and CAFS=1. Perform the required reset, reinitialize, then verify CAFS=2 together with FRS2 and Identify.FR."
                if english
                else "**[說明性範例]** 假設 NOFS=3、FFSRO=1、FWUG=1h、CAFS=1，選可寫的 slot 2。12 KiB 切成三個 4 KiB portions；每段 1024 dwords，所以 NUMD=1023=000003FFh，OFST 依序是 00000000h、00000400h、00000800h。以 CA=001b、FS=010b commit，CDW10=0000000Ah。Reset 前完整讀 512-byte LID 03h：NUMD=127、CDW10=007F0003h；AFI=21h 解成 NAFS=2、CAFS=1。執行要求的 reset、重新初始化，再一起驗證 CAFS=2、FRS2 與 Identify.FR。"
            ),
            "",
            "## " + ("Debug Decision Flow" if english else "Debug Decision Flow"),
            "",
            (
                "| Symptom | First evidence | Likely mistake | Next action |\n|---|---|---|---|\n| Download Invalid Field | NUMD, OFST, FWUG | NUMD treated as a direct count | Recompute byte intervals |\n| Invalid Firmware Slot | NOFS, FFSRO, FS | Slot 1 assumed writable | Select a supported writable slot |\n| Reset-required status | Full SCT/SC | All resets treated as equal | Follow status and PCIe §3.3 |\n| LID 03h unchanged | MDS/DID, controller, AFI | Slots assumed per controller | Verify within the same domain |\n| FRSx is zero | NOFS, slot validity, buffer offset | Zero treated as an empty revision string | Treat as unsupported/no valid revision |"
                if english
                else "| 症狀 | 第一證據 | 常見錯誤 | 下一步 |\n|---|---|---|---|\n| Download Invalid Field | NUMD、OFST、FWUG | 把 NUMD 當直接 count | 重算 byte intervals |\n| Invalid Firmware Slot | NOFS、FFSRO、FS | 假設 slot 1 可寫 | 改用支援且可寫 slot |\n| reset-required status | 完整 SCT／SC | 把所有 reset 視為相同 | 依 status 與 PCIe §3.3 |\n| LID 03h 未更新 | MDS／DID、controller、AFI | 假設 slots 各 controller 獨立 | 在同一 domain 核對 |\n| FRSx 為零 | NOFS、slot validity、buffer offset | 當成空字串 revision | 視為 unsupported／no valid revision |"
            ),
            "",
        ]
    )
    out.extend(firmware_figure_appendix_markdown(claims, figures, language))
    out.extend(
        [
            "## " + ("Limits" if english else "限制"),
            "",
            (
                "Verification date: 2026-09-01. No additional errata, ECNs, Technical Proposals, controller-vendor documents, or PCI Express Base Specification source text are included. Re-check affected claim IDs when the approved source set changes."
                if english
                else "查證日期：2026-09-01。未納入其他 Errata、ECN、Technical Proposal、controller vendor 文件或 PCI Express Base Specification 原文。核准來源集合改變時，應依 claim ID 重查。"
            ),
            "",
        ]
    )
    return "\n".join(out)


def fw_ppt_claim_notes(items: list[dict], language: str) -> list[str]:
    english = language == "en"
    out = [
        '<details markdown="1">',
        "<summary><strong>Speaker notes / source claims</strong></summary>"
        if english
        else "<summary><strong>講者備註／來源論點</strong></summary>",
        "",
    ]
    for item in items:
        out.extend(
            [
                f"<!-- claim:{item['id']} -->",
                "",
                "**[SPEC]** " + (item["en"] if english else item["zh_tw"]),
                "",
                "> " + (item["citation_en"] if english else item["citation_zh_tw"]),
                "",
            ]
        )
    out.extend(["</details>", ""])
    return out


def render_firmware_ppt_markdown(
    report: dict, claims: list[dict], figures: list[dict], language: str
) -> str:
    english = language == "en"
    by_id = {item["id"]: item for item in claims if item["figure"] is None}
    title = report["title_en"] if english else report["title_zh"]
    description = (
        "Slide-ready bilingual source for firmware update and LID 03h."
        if english
        else "Firmware update 與 LID 03h 的投影片製作稿。"
    )
    out = [
        frontmatter("base-admin-fw-logs", title, description, language),
        f"# {title}",
        "",
        (
            "PPT authoring edition. The Chinese and English editions use the same slide modules, claim order, calculations, and source boundaries."
            if english
            else "PPT 製作版。中文版與英文版使用完全相同的 slide modules、claim 順序、計算與來源邊界。"
        ),
        "",
        SOURCES["NVME-BASE-2.4"]["marker"],
        "",
        SOURCES["NVME-PCIE-TRANSPORT-1.4"]["marker"]
        + (" — §3.3 only" if english else " — 僅 §3.3"),
        "",
        "---",
        "",
        "## Slide 01 — " + ("The real problem" if english else "真正要解決的問題"),
        "",
        (
            "> A successful download is not a successful activation. Track placement, pending activation, the reset boundary, and post-activation evidence separately."
            if english
            else "> Download 成功不等於 activation 成功；必須分開追蹤 placement、pending activation、reset 邊界與 activation 後證據。"
        ),
        "",
        "```text",
        "Download -> Commit / place -> activate now or later -> reset if required -> LID 03h verify",
        "```",
        "",
        "---",
        "",
        "## Slide 02 — " + ("Vocabulary before fields" if english else "先教名詞，再看欄位"),
        "",
        (
            "| State | Meaning | Evidence |\n|---|---|---|\n| Downloaded | Portions are temporary | NUMD / OFST |\n| Stored | Image is in a slot | FRSx |\n| Pending | Slot is selected for a later reset | NAFS |\n| Active | Image is executing | CAFS + Identify.FR |"
            if english
            else "| 狀態 | 意義 | 證據 |\n|---|---|---|\n| Downloaded | portions 暫存中 | NUMD／OFST |\n| Stored | image 已在 slot | FRSx |\n| Pending | 排定下一次 reset | NAFS |\n| Active | image 正在執行 | CAFS＋Identify.FR |"
        ),
        "",
        "---",
        "",
            "## Slide 03 — " + ("Mental Model and capability gate" if english else "Mental Model 與 capability gate"),
        "",
        (
            "Firmware slots belong to a domain. Before constructing a command, read FRMW, FWUG, MTFA, MPTFAWR, MDS/DID, and the current FR."
            if english
            else "Firmware slots 屬於 domain。建構 command 前，先讀 FRMW、FWUG、MTFA、MPTFAWR、MDS／DID 與目前 FR。"
        ),
        "",
        (
            "| Field | Question answered | Unit / range |\n|---|---|---|\n| FRMW | slots, read-only, immediate activation | bits |\n| FWUG | chunk granularity and alignment | 4 KiB |\n| MTFA | command-processing pause | 100 ms |\n| MPTFAWR | CA=011b completion estimate | 100 ms |"
            if english
            else "| 欄位 | 回答的問題 | unit／range |\n|---|---|---|\n| FRMW | slots、read-only、立即 activation | bits |\n| FWUG | chunk granularity／alignment | 4 KiB |\n| MTFA | command processing 暫停 | 100 ms |\n| MPTFAWR | CA=011b completion estimate | 100 ms |"
        ),
        "",
        ("Source map: Figure 338 (printed/PDF 340-365/366-391); Figures 347-348 (396/422)." if english else "來源地圖：Figure 338（文件/PDF 340-365/366-391）；Figures 347-348（396/422）。"),
        "",
    ]
    out.extend(fw_ppt_claim_notes([by_id[item] for item in FIRMWARE_PARTS[0]["claims"]], language))
    out.extend(
        [
            "---",
            "",
            "## Slide 04 — " + ("Download means dword ranges" if english else "Download 的本質是 dword ranges"),
            "",
            "```text",
            "bytes = (NUMD + 1) × 4",
            "byte offset = OFST × 4",
            "```",
            "",
            (
                "**Example:** 4 KiB = 1024 dwords, so NUMD=03FFh. A portion beginning at byte 8192 uses OFST=0800h."
                if english
                else "**範例：**4 KiB=1024 dwords，所以 NUMD=03FFh；從 byte 8192 開始的 portion 使用 OFST=0800h。"
            ),
            "",
            ("Source map: Figure 93 (140-142/166-168); Figures 190-193 (205-206/231-232)." if english else "來源地圖：Figure 93（文件/PDF 140-142/166-168）；Figures 190-193（205-206/231-232）。"),
            "",
        ]
    )
    out.extend(fw_ppt_claim_notes([by_id[item] for item in FIRMWARE_PARTS[1]["claims"]], language))
    commit_claims = [by_id[item] for item in FIRMWARE_PARTS[2]["claims"]]
    out.extend(
        [
            "---",
            "",
            "## Slide 05 — " + ("Commit Action is a state transition" if english else "Commit Action 是狀態轉移"),
            "",
            (
                "| CA | Placement | Activation |\n|---|---|---|\n| 000b | downloaded image -> slot | none |\n| 001b | downloaded image -> slot | next capable CLR |\n| 010b | existing slot | next capable CLR |\n| 011b | downloaded or existing slot | immediate; command waits |"
                if english
                else "| CA | placement | activation |\n|---|---|---|\n| 000b | downloaded image → slot | 不 activation |\n| 001b | downloaded image → slot | 下次合適 CLR |\n| 010b | existing slot | 下次合適 CLR |\n| 011b | downloaded／existing slot | 立即；command 等結果 |"
            ),
            "",
            ("Source map: Figures 187-189 (203-205/229-231)." if english else "來源地圖：Figures 187-189（文件/PDF 203-205/229-231）。"),
            "",
        ]
    )
    out.extend(fw_ppt_claim_notes(commit_claims[:5], language))
    out.extend(
        [
            "---",
            "",
            "## Slide 06 — " + ("Activation has four branches" if english else "Activation 有四條分支"),
            "",
            "```text",
            "CA 000b -> stored only",
            "CA 001b / 010b -> pending -> required CLR -> reinitialize",
            "CA 011b -> command in progress -> success or reset-required / time / prohibited status",
            "load failure -> most recently active image -> baseline read-only fallback",
            "```",
            "",
            ("Source map: Figures 155 and 474 (186/212 and 466-468/492-494); Figures 347-348 (396/422)." if english else "來源地圖：Figures 155、474（文件/PDF 186/212、466-468/492-494）；Figures 347-348（396/422）。"),
            "",
        ]
    )
    out.extend(fw_ppt_claim_notes(commit_claims[5:], language))
    out.extend(
        [
            "---",
            "",
            "## Slide 07 — " + ("Status selects recovery" if english else "Status 決定 recovery"),
            "",
            (
                "| SC | Meaning | Correct direction |\n|---|---|---|\n| 06h / 07h | invalid slot / image | fix target or image |\n| 0Bh | Conventional Reset required | do not substitute FLR |\n| 10h | NVM Subsystem Reset required | smaller reset keeps old image |\n| 11h | Controller Level Reset required | activate at next CLR |\n| 12h | maximum-time violation | image committed; schedule with CA=010b |\n| 13h / 14h | prohibited / overlap | policy or range fix |"
                if english
                else "| SC | 意義 | 正確方向 |\n|---|---|---|\n| 06h／07h | invalid slot／image | 修正 target／image |\n| 0Bh | 需要 Conventional Reset | 不可用 FLR 代替 |\n| 10h | 需要 NVM Subsystem Reset | 小範圍 reset 仍跑舊 image |\n| 11h | 需要 Controller Level Reset | 下次 CLR activation |\n| 12h | maximum-time violation | image 已 commit；可用 CA=010b 排定 |\n| 13h／14h | prohibited／overlap | 修正 policy／range |"
            ),
            "",
            "---",
            "",
            "## Slide 08 — " + ("Construct the LID 03h command" if english else "建構 LID 03h command"),
            "",
            "```text",
            "512 bytes / 4 = 128 dwords",
            "NUMD = 128 - 1 = 127 = 007Fh",
            "CDW10 = NUMDL[31:16] | RAE=0 | LSP=0 | LID=03h",
            "      = 007F0003h",
            "```",
            "",
            ("Source map: Figure 93 (140-142/166-168); Figures 203-209 (213-216/239-242)." if english else "來源地圖：Figure 93（文件/PDF 140-142/166-168）；Figures 203-209（213-216/239-242）。"),
            "",
        ]
    )
    lid_claims = [by_id[item] for item in FIRMWARE_PARTS[3]["claims"]]
    out.extend(fw_ppt_claim_notes(lid_claims[:5], language))
    out.extend(
        [
            "---",
            "",
            "## Slide 09 — " + ("Decode AFI before revision strings" if english else "先解 AFI，再讀 revision strings"),
            "",
            "```text",
            "byte 0: [7 R][6:4 NAFS][3 R][2:0 CAFS]",
            "bytes 1:7: reserved",
            "bytes 8:63: FRS1 ... FRS7 (8 bytes each)",
            "bytes 64:511: reserved",
            "```",
            "",
            (
                "**Example:** AFI=21h means NAFS=2 and CAFS=1. Slot 2 is pending; slot 1 is still executing."
                if english
                else "**範例：**AFI=21h 代表 NAFS=2、CAFS=1；slot 2 pending，slot 1 仍在執行。"
            ),
            "",
            ("Source map: Figure 215 (printed/PDF 226/252)." if english else "來源地圖：Figure 215（文件/PDF 226/252）。"),
            "",
        ]
    )
    out.extend(fw_ppt_claim_notes(lid_claims[5:], language))
    out.extend(
        [
            "---",
            "",
            "## Slide 10 — End-to-End Example",
            "",
            (
                "| Stage | Concrete value | Evidence |\n|---|---|---|\n| Capability | NOFS=3, FFSRO=1, FWUG=1h | choose writable slot 2 |\n| Download | NUMD=03FFh; OFST=0/0400h/0800h | 12 KiB transferred |\n| Commit | CA=001b, FS=2, CDW10=0000000Ah | slot 2 pending |\n| Pre-reset | LID03 CDW10=007F0003h, AFI=21h | CAFS1 / NAFS2 |\n| Post-reset | CAFS=2, FRS2=Identify.FR | activation verified |"
                if english
                else "| 階段 | 具體值 | 證據 |\n|---|---|---|\n| Capability | NOFS=3、FFSRO=1、FWUG=1h | 選可寫 slot 2 |\n| Download | NUMD=03FFh；OFST=0／0400h／0800h | 12 KiB transferred |\n| Commit | CA=001b、FS=2、CDW10=0000000Ah | slot 2 pending |\n| Pre-reset | LID03 CDW10=007F0003h、AFI=21h | CAFS1／NAFS2 |\n| Post-reset | CAFS=2、FRS2=Identify.FR | activation verified |"
            ),
            "",
            "---",
            "",
            "## Slide 11 — " + ("Debug from the first broken boundary" if english else "從第一個斷掉的邊界開始 Debug"),
            "",
            (
                "| Symptom | First evidence |\n|---|---|\n| Download Invalid Field | PRP, NUMD, OFST, FWUG |\n| Commit invalid slot | NOFS, FFSRO, FS |\n| Reset-required SC | full SCT/SC and actual reset trace |\n| FRS2 valid, CAFS still 1 | CA, NAFS, reset type |\n| controllers disagree | MDS, DID, processing controller |"
                if english
                else "| 症狀 | 第一證據 |\n|---|---|\n| Download Invalid Field | PRP、NUMD、OFST、FWUG |\n| Commit invalid slot | NOFS、FFSRO、FS |\n| reset-required SC | 完整 SCT／SC＋實際 reset trace |\n| FRS2 valid、CAFS 仍 1 | CA、NAFS、reset type |\n| controllers 結果不同 | MDS、DID、processing controller |"
            ),
            "",
            "---",
            "",
            "## Slide 12 — " + ("Takeaway and source boundary" if english else "結論與來源邊界"),
            "",
            (
                "> Treat firmware update as a state machine with domain scope. Commands move the state; completion status selects recovery; LID 03h proves the resulting slot state."
                if english
                else "> 把 firmware update 當成具有 domain scope 的 state machine：command 推進狀態、completion status 選 recovery、LID 03h 證明最後 slot 狀態。"
            ),
            "",
            ("Included: " + report["range_en"] if english else "納入：" + report["range"]),
            "",
            (
                "Verification date: 2026-09-01. No additional errata, ECNs, vendor documents, or PCI Express Base Specification source text are included."
                if english
                else "查證日期：2026-09-01。未納入額外 Errata、ECN、vendor 文件或 PCI Express Base Specification 原文。"
            ),
            "",
        ]
    )
    out.extend(glossary_markdown("base-admin-fw-logs", claims, language))
    out.extend(visual_atlas_markdown("base-admin-fw-logs", claims, language))
    out.extend(firmware_figure_appendix_markdown(claims, figures, language))
    return "\n".join(out)


def main() -> int:
    argparse.ArgumentParser(description=__doc__).parse_args()
    contract = json.loads(
        (CONTROL / "output-contract.json").read_text(encoding="utf-8")
    )
    register_doc = json.loads(
        (CONTROL / "figure-table-register.json").read_text(encoding="utf-8")
    )
    scope_doc = json.loads((CONTROL / "scope.json").read_text(encoding="utf-8"))
    figure_allowlists = {
        item["id"]: set(item.get("included_figure_ids", []))
        for item in scope_doc["reports"]
    }
    register_entries = register_doc["entries"]
    artifacts = {item["id"]: item for item in contract["artifacts"]}
    all_claims = []

    for report_id, report in REPORTS.items():
        figures = sorted(
            [
                item
                for item in register_entries
                if item["report_id"] == report_id
                and item["scope_status"] == "INCLUDE"
                and (
                    not figure_allowlists.get(report_id)
                    or item["id"] in figure_allowlists[report_id]
                )
            ],
            key=lambda item: (
                item.get("role") == "referenced_dependency",
                int(item["number"]),
            ),
        )
        for figure in figures:
            if not figure.get("key_items") or not figure.get("evidence_digest"):
                raise ValueError(
                    f"{figure['id']} lacks tracked compact PDF evidence"
                )
        report_claims = [
            make_claim(report_id, report, item) for item in report["claims"]
        ]
        report_claims.extend(
            make_figure_claim(report_id, report, item) for item in figures
        )
        all_claims.extend(report_claims)

        ids = artifact_ids(report_id)
        if report_id == "base-admin-fw-logs":
            output_text = {
                ids[0]: render_firmware_tutorial_html(report, report_claims, figures),
                ids[1]: render_firmware_reference_html(
                    report, report_claims, figures
                ),
                ids[2]: render_firmware_ppt_markdown(
                    report, report_claims, figures, "zh"
                ),
                ids[3]: render_firmware_ppt_markdown(
                    report, report_claims, figures, "en"
                ),
            }
        else:
            output_text = {
                ids[0]: render_html(
                    report_id, report, report_claims, figures, True
                ),
                ids[1]: render_html(
                    report_id, report, report_claims, figures, False
                ),
                ids[2]: render_markdown(
                    report_id, report, report_claims, figures, "zh"
                ),
                ids[3]: render_markdown(
                    report_id, report, report_claims, figures, "en"
                ),
            }
        for artifact_id, content in output_text.items():
            path = ROOT / artifacts[artifact_id]["path"]
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")

    claims_doc = {
        "schema_version": 3,
        "allowed_normative_keywords": [
            "mandatory",
            "may",
            "obsolete",
            "optional",
            "reserved",
            "shall",
            "shall not",
            "should",
            "should not",
            "none",
        ],
        "claims": all_claims,
    }
    (CONTROL / "claims.json").write_text(
        json.dumps(claims_doc, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        f"Built {len(contract['artifacts'])} artifacts, {len(all_claims)} claims, "
        f"using {len(register_entries)} tracked Figure records"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
