---
layout: post
title: "PCIe Chapter 12: Error Evidence, Reporting, and Containment"
date: 2026-10-21 00:00:00 +0800
permalink: /pcie/chapter-12-en/
categories: [PCIe]
tags: [PCIe, Specification]
lang: en
---

<style>
/* Every selector is scoped so the same reading styles can be embedded in Jekyll. */
.pcie-article {
  --paper: #f2f6f8;
  --surface: #ffffff;
  --surface-alt: #f4f8fb;
  --ink: #192d40;
  --muted: #4c6479;
  --accent: #145f9d;
  --accent-2: #0b756c;
  --line: #cbd9e3;
  --blue-soft: #edf5fc;
  --teal-soft: #edf8f5;
  --warm-soft: #fff7e8;
  --warm-ink: #775016;
  --focus: #95530c;
  --radius: 14px;
  margin: 0;
  background: var(--paper);
  color: var(--ink);
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans TC", "PingFang TC", "Microsoft JhengHei", sans-serif;
  font-size: 17px;
  line-height: 1.85;
  -webkit-text-size-adjust: 100%;
  color-scheme: light dark;
  overflow-wrap: break-word;
}
.pcie-article *, .pcie-article *::before, .pcie-article *::after { box-sizing: border-box; }
.pcie-article a { color: var(--accent); text-decoration-thickness: 1px; text-underline-offset: .2em; display: inline-flex; align-items: center; min-height: 44px; min-width: 44px; }
.pcie-article a:hover { text-decoration-thickness: 2px; }
.pcie-article :focus-visible { outline: 3px solid var(--focus); outline-offset: 4px; border-radius: 3px; }
.pcie-article [id] { scroll-margin-top: 28px; }
.pcie-article .skip-link { position: absolute; left: 16px; top: -100px; padding: .5rem 1rem; background: var(--surface); z-index: 20; }
.pcie-article .skip-link:focus { top: 12px; }
.pcie-article .site-shell { width: min(100% - 56px, 1360px); margin: 0 auto; }
.pcie-article .topbar { display: flex; align-items: center; justify-content: space-between; gap: 16px; padding: max(22px, env(safe-area-inset-top)) 0 18px; border-bottom: 1px solid var(--line); }
.pcie-article .topbar a { font-size: .88rem; text-decoration: none; }
.pcie-article .series-name { font-weight: 750; letter-spacing: .04em; gap: 12px; }
.pcie-article .series-name span { color: var(--muted); font-weight: 450; letter-spacing: .02em; }
.pcie-article .page-header { padding: 50px 0 36px; max-width: 1050px; }
.pcie-article .eyebrow { font-size: .76rem; font-weight: 750; letter-spacing: .14em; color: var(--accent-2); margin: 0 0 15px; }
.pcie-article h1 { font-size: clamp(2rem, 3.4vw, 3.2rem); line-height: 1.35; letter-spacing: -.025em; font-weight: 750; margin: 0 0 20px; max-width: 24em; text-wrap: balance; }
.pcie-article .header-description { max-width: 49em; color: var(--muted); font-size: 1.08rem; line-height: 1.8; margin: 0; }
.pcie-article .edition { display: flex; flex-wrap: wrap; gap: 6px 22px; margin-top: 22px; font-size: .78rem; color: var(--muted); }
.pcie-article .reading-layout { display: grid; gap: 30px; align-items: start; padding-bottom: 48px; }
.pcie-article .toc-panel { border-top: 3px solid var(--accent-2); border-bottom: 1px solid var(--line); padding: 14px 0; }
.pcie-article .toc-label { margin: 0 0 9px; font-size: .74rem; font-weight: 750; letter-spacing: .12em; color: var(--muted); }
.pcie-article .toc-panel ol { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 2px 20px; list-style: none; padding: 0; margin: 0; }
.pcie-article .toc-panel a { width: 100%; font-size: .84rem; line-height: 1.55; color: var(--muted); text-decoration: none; padding: 8px 0; }
.pcie-article .toc-panel a:hover { color: var(--accent); text-decoration: underline; }
.pcie-article main { min-width: 0; }
.pcie-article .lesson { background: var(--surface); border: 1px solid var(--line); border-radius: var(--radius); padding: clamp(24px, 4vw, 54px); }
.pcie-article .lesson > :first-child { margin-top: 0; }
.pcie-article .lesson > section { margin-top: 3.1rem; }
.pcie-article .lesson > section:first-child { margin-top: 0; }
.pcie-article .lesson > section + section { border-top: 1px solid var(--line); padding-top: 2.7rem; }
.pcie-article h2 { font-size: 1.6rem; line-height: 1.55; letter-spacing: -.015em; margin: 0 0 1.2rem; font-weight: 700; }
.pcie-article h3 { font-size: 1.17rem; line-height: 1.6; margin: 2rem 0 .7rem; font-weight: 700; }
.pcie-article h4 { font-size: 1rem; line-height: 1.7; margin: 1.6rem 0 .5rem; }
.pcie-article p, .pcie-article ul, .pcie-article ol, .pcie-article dl, .pcie-article blockquote { max-width: 76ch; }
.pcie-article p { margin: .85rem 0 1.1rem; }
.pcie-article ul, .pcie-article ol { padding-left: 1.45rem; margin: .8rem 0 1.3rem; }
.pcie-article li { margin: .45rem 0; padding-left: .12rem; }
.pcie-article li::marker { color: var(--accent-2); }
.pcie-article strong { font-weight: 700; }
.pcie-article code { font-family: "SFMono-Regular", Consolas, "Liberation Mono", monospace; font-size: .87em; background: var(--surface-alt); border: 1px solid var(--line); border-radius: 4px; padding: .08em .28em; overflow-wrap: anywhere; }
.pcie-article pre { overflow-x: auto; padding: 1rem; background: var(--surface-alt); border: 1px solid var(--line); border-radius: 8px; font-size: .88rem; line-height: 1.7; }
.pcie-article pre code { background: none; border: 0; padding: 0; }
.pcie-article blockquote { margin: 1.3rem 0; padding: .2rem 1.3rem; border-left: 3px solid var(--accent-2); color: var(--muted); }
.pcie-article .lead { font-size: 1.08rem; line-height: 1.95; }
.pcie-article .question { color: var(--accent); font-weight: 700; }
.pcie-article .answer { margin-top: 1rem; }
.pcie-article .question .answer { font-weight: 400; color: var(--ink); }
.pcie-article details.question > :not(summary) { font-weight: 400; color: var(--ink); }
.pcie-article .term-note { color: var(--muted); font-size: .88rem; padding-left: 1rem; border-left: 2px solid var(--line); margin: 1rem 0 1.4rem; }
.pcie-article .example, .pcie-article .note, .pcie-article .takeaway { border: 1px solid var(--line); border-left: 4px solid var(--accent-2); border-radius: 0 10px 10px 0; background: var(--teal-soft); padding: 1rem 1.3rem; margin: 1.6rem 0; }
.pcie-article .example > :first-child, .pcie-article .note > :first-child, .pcie-article .takeaway > :first-child { margin-top: 0; }
.pcie-article .example > :last-child, .pcie-article .note > :last-child, .pcie-article .takeaway > :last-child { margin-bottom: 0; }
.pcie-article .note { border-left-color: var(--accent); background: var(--blue-soft); }
.pcie-article .takeaway { font-weight: 600; }
.pcie-article .table-wrap { max-width: 100%; overflow-x: auto; -webkit-overflow-scrolling: touch; margin: 1.5rem 0; border: 1px solid var(--line); border-radius: 9px; background: var(--surface); }
.pcie-article table { width: 100%; border-collapse: separate; border-spacing: 0; font-size: .9rem; line-height: 1.75; text-align: left; }
.pcie-article caption { text-align: left; padding: 12px 16px; font-weight: 650; color: var(--ink); background: var(--surface-alt); border-bottom: 1px solid var(--line); }
.pcie-article th, .pcie-article td { padding: 13px 16px; vertical-align: top; border-bottom: 1px solid var(--line); min-width: 9em; }
.pcie-article th { font-weight: 650; color: var(--ink); background: var(--blue-soft); }
.pcie-article thead th { position: sticky; top: 0; z-index: 2; }
.pcie-article tbody th, .pcie-article tbody td:first-child { position: sticky; left: 0; z-index: 1; background: var(--surface-alt); }
.pcie-article thead th:first-child { left: 0; z-index: 3; }
.pcie-article tbody tr:last-child td, .pcie-article tbody tr:last-child th { border-bottom: 0; }
.pcie-article td p, .pcie-article th p { margin: .2rem 0 .5rem; }
.pcie-article .field { font-family: "SFMono-Regular", Consolas, monospace; color: var(--accent); overflow-wrap: anywhere; }
.pcie-article figure { margin: 1.6rem 0; }
.pcie-article .diagram { padding: 20px; border: 1px solid var(--line); border-radius: 10px; background: var(--surface-alt); }
.pcie-article svg { display: block; width: 100%; height: auto; max-width: 100%; color: var(--ink); }
.pcie-article svg text { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans TC", "PingFang TC", "Microsoft JhengHei", sans-serif; }
.pcie-article .diagram .box { fill: var(--surface); stroke: var(--accent); stroke-width: 2; }
.pcie-article .diagram .arrow { fill: none; stroke: var(--accent); stroke-width: 2; }
.pcie-article .diagram svg[aria-labelledby="journey-title journey-desc"] text,
.pcie-article .diagram svg[aria-labelledby="msix-title msix-desc"] text { fill: var(--ink); font-size: 18px; }
.pcie-article figcaption { color: var(--muted); font-size: .85rem; line-height: 1.75; margin-top: 12px; }
.pcie-article details { border: 1px solid var(--line); border-radius: 9px; background: var(--surface-alt); padding: 0 18px; margin: 1.2rem 0; }
.pcie-article summary { cursor: pointer; min-height: 44px; padding: 12px 0; font-weight: 650; line-height: 1.65; }
.pcie-article summary::marker { color: var(--accent-2); }
.pcie-article details[open] { padding-bottom: 8px; }
.pcie-article details[open] > summary { border-bottom: 1px solid var(--line); margin-bottom: 12px; }
.pcie-article .source-note { background: transparent; font-size: .84rem; color: var(--muted); }
.pcie-article .source-note summary { font-weight: 500; }
.pcie-article .source-ref { font-size: .81rem; color: var(--muted); }
.pcie-article .route { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 14px; padding: 0; margin: 1.5rem 0; list-style-position: inside; max-width: none; }
.pcie-article .route > li { margin: 0; padding: 15px; border: 1px solid var(--line); border-top: 3px solid var(--accent-2); border-radius: 7px; background: var(--surface-alt); font-size: .88rem; }
.pcie-article .steps > li { margin: 1rem 0; padding-left: .3rem; }
.pcie-article .route > li::marker, .pcie-article .steps > li::marker { font-weight: 750; }
.pcie-article :target { outline: 2px solid var(--accent-2); outline-offset: 7px; }
.pcie-article main:target { outline: none; }
.pcie-article .bottom-nav { display: flex; justify-content: space-between; flex-wrap: wrap; gap: 12px; padding: 24px 4px 0; font-size: .88rem; }
.pcie-article .page-footer { border-top: 1px solid var(--line); padding: 22px 0 38px; font-size: .78rem; color: var(--muted); }
.pcie-article .page-footer p { margin: .3rem 0; }
.pcie-article .chapter-list { display: grid; gap: 18px; margin-top: 1.5rem; }
.pcie-article .chapter-card { padding: 21px 24px; border: 1px solid var(--line); border-radius: 10px; background: var(--surface); }
.pcie-article .chapter-card.ready { border-top: 4px solid var(--accent-2); background: var(--teal-soft); }
.pcie-article .chapter-meta { display: flex; flex-wrap: wrap; align-items: center; gap: 8px 16px; font-size: .75rem; color: var(--muted); font-weight: 650; }
.pcie-article .status { padding: 2px 9px; border: 1px solid var(--line); border-radius: 4px; }
.pcie-article .ready .status { color: var(--accent-2); border-color: var(--accent-2); }
.pcie-article .chapter-card h3 { font-size: 1.15rem; margin: 10px 0 8px; }
.pcie-article .chapter-card h3 a { min-height: 44px; }
.pcie-article .chapter-card .chapter-question { margin: 0 0 10px; color: var(--muted); font-size: .94rem; }
.pcie-article .chapter-card ul { font-size: .9rem; margin: .6rem 0; }
.pcie-article .prerequisites { font-size: .8rem; color: var(--muted); margin-bottom: 0; }
.pcie-article .start-link { padding: 9px 18px; border-radius: 6px; background: var(--accent); color: var(--surface); text-decoration: none; font-weight: 650; }
@media (min-width: 1200px) {
  .pcie-article .reading-layout { grid-template-columns: 232px minmax(0, 1fr); gap: 38px; }
  .pcie-article .toc-panel { position: sticky; top: calc(24px + env(safe-area-inset-top)); }
  .pcie-article .toc-panel ol { display: block; }
  .pcie-article .toc-panel li { margin: 2px 0; }
  .pcie-article .toc-panel a { padding: 7px 0; font-size: .8rem; }
  .pcie-article .page-header { padding-left: 270px; max-width: none; }
}
@media (min-width: 760px) and (max-width: 1199px) {
  .pcie-article .site-shell { width: min(100% - 48px, 900px); }
}
@media (max-width: 759px) {
  .pcie-article .site-shell { width: min(100% - 28px, 700px); }
  .pcie-article .topbar { gap: 10px; }
  .pcie-article .series-name { gap: 6px; }
  .pcie-article .series-name span { font-size: .72rem; }
  .pcie-article .page-header { padding: 32px 2px 26px; }
  .pcie-article .header-description { font-size: 1rem; }
  .pcie-article .toc-panel ol { grid-template-columns: 1fr; }
  .pcie-article .lesson { padding: 25px 19px; }
  .pcie-article h2 { font-size: 1.4rem; }
  .pcie-article .lesson > section + section { padding-top: 2rem; }
  .pcie-article .diagram { padding: 10px; overflow-x: auto; -webkit-overflow-scrolling: touch; }
  .pcie-article .diagram::before { content: "圖可左右捲動"; display: block; color: var(--muted); font-size: .8rem; margin-bottom: 8px; }
  .pcie-article[lang="en"] .diagram::before { content: "Scroll horizontally to view the diagram"; }
  .pcie-article .diagram svg { min-width: 700px; }
  .pcie-article .example, .pcie-article .note { padding: 1rem; }
  .pcie-article .chapter-card { padding: 18px; }
  .pcie-article .route { grid-template-columns: 1fr; }
}
  html[data-theme="dark"] .pcie-article {
    --paper: #101b26;
    --surface: #172635;
    --surface-alt: #1c3041;
    --ink: #e0ebf5;
    --muted: #b2c4d4;
    --accent: #8ac9ff;
    --accent-2: #75d4c4;
    --line: #40596b;
    --blue-soft: #203a50;
    --teal-soft: #183b3c;
    --warm-soft: #3e3324;
    --warm-ink: #edd09a;
    --focus: #ffcf83;
  }
  html[data-theme="dark"] .pcie-article .start-link { color: #102334; }
@media (prefers-reduced-motion: reduce) {
  .pcie-article *, .pcie-article *::before, .pcie-article *::after { animation: none !important; transition: none !important; scroll-behavior: auto !important; }
}
@media print {
  .pcie-article { --paper: #fff; --surface: #fff; --surface-alt: #f6f6f6; --ink: #111; --muted: #444; --accent: #174d73; --accent-2: #1e5a4c; --line: #aaa; --blue-soft: #f2f5f7; --teal-soft: #f0f6f3; color-scheme: light; font-size: 11pt; line-height: 1.7; background: #fff; }
  .pcie-article .site-shell { width: 100%; }
  .pcie-article .topbar, .pcie-article .skip-link, .pcie-article .toc-panel, .pcie-article .bottom-nav { display: none; }
  .pcie-article .reading-layout { display: block; padding: 0; }
  .pcie-article .page-header { padding: 0 0 20px; }
  .pcie-article h1 { font-size: 24pt; }
  .pcie-article h2 { font-size: 17pt; }
  .pcie-article h3 { font-size: 13pt; }
  .pcie-article .lesson { border: 0; padding: 0; }
  .pcie-article a { display: inline; min-width: 0; min-height: 0; text-decoration: underline; }
  .pcie-article h2, .pcie-article h3, .pcie-article h4, .pcie-article summary { break-after: avoid; }
  .pcie-article figure, .pcie-article tr, .pcie-article .example, .pcie-article .chapter-card { break-inside: avoid; }
  .pcie-article .table-wrap { overflow: visible; }
  .pcie-article th, .pcie-article td { min-width: 0; padding: 7px 9px; position: static !important; }
  .pcie-article details { background: transparent; }
  .pcie-article details > * { display: block !important; }
  .pcie-article details::details-content { content-visibility: visible !important; }
  .pcie-article .diagram { overflow: visible; }
  .pcie-article .diagram::before { display: none; }
  .pcie-article .diagram svg { min-width: 0; }
  .pcie-article .page-footer { margin-top: 20px; }
  .pcie-article :target { outline: 0; }
}
@media (forced-colors: active) {
  .pcie-article { --paper: Canvas; --surface: Canvas; --surface-alt: Canvas; --ink: CanvasText; --muted: CanvasText; --accent: LinkText; --accent-2: LinkText; --line: CanvasText; --blue-soft: Canvas; --teal-soft: Canvas; --warm-soft: Canvas; --warm-ink: CanvasText; --focus: Highlight; }
  .pcie-article a { text-decoration: underline; }
  .pcie-article .start-link { border: 1px solid LinkText; color: LinkText; background: Canvas; }
  .pcie-article svg { forced-color-adjust: none; }
}

/* Self-contained teaching diagrams use the same theme in standalone pages and posts. */
.pcie-article .course-diagram text { fill: var(--ink); font-family: inherit; font-size: 18px; }

html:not([data-theme="dark"]) .pcie-article { color-scheme: light; }
html[data-theme="dark"] .pcie-article { color-scheme: dark; }

.pcie-article { background: transparent; margin: 1.5rem 0; }
.pcie-article .lesson { padding: 0; border: 0; background: transparent; }
</style>
<div class="pcie-article" lang="en">
<nav class="bottom-nav" aria-label="Course and editions"><a href="/DOCS/pcie-course/index.html">Course overview</a><a href="/DOCS/pcie-course/chapter-12.html">Full Chinese tutorial</a><a href="/pcie/chapter-12-zh-tw/">繁體中文</a></nav>
<article class="lesson">
<p class="lead">PCIe error analysis connects detection, reporting, reception, and containment. Status does not prove that a message arrived; Source ID identifies a reporter rather than the physical root cause. Two separate AER and DPC examples show how to respect those boundaries.</p><aside class="note"><strong>Version and assumptions</strong><p>Based on PCIe Base 6.0. All values and event sequences are author-created, using ordinary non-SR-IOV Functions. The AER example supports neither Flit Mode nor End-End TLP Prefixes and has DPC disabled. The later DPC example is a separate event. The manager has appropriate ownership, and no unspecified concurrent events occur.</p></aside>
<section id="model"><h2>Connect evidence from the Function to the Root</h2><p>Correctable Errors can be recovered by the protocol but may affect performance. Uncorrectable Errors affect functionality and are classified Non-Fatal or Fatal. Non-Fatal does not establish successful work, and Fatal does not directly diagnose a failed chip. AER adds detailed status, masks, severity, and logs to baseline reporting; absence of AER does not imply absence of all reporting.</p><p>Inspect source Status, the Mask/Severity/Device Control settings at detection, valid Header Logs, and then Root Error Status/Source ID. Check DPC separately if containment is possible. Later configuration reads do not automatically reconstruct earlier settings. Sources: §6.2.1–§6.2.4 (pp.669–679), Figure 6-1 (p.670).</p></section>
<section id="aer"><h2>Two status bits, one unmasked error</h2><p>Traverse Extended Capabilities on 03:00.0 and use Figure 7-154 to identify AER ID=0x0001. This example has base=0x100, Version=2, Next=0; Base 6.0 does not imply this Function implements all Flit features. Earlier records were cleared, settings remained unchanged, and forwarding along the path is enabled.</p><div class="table-wrap"><table><caption>Source Function reads</caption><thead><tr><th scope="col">Register / offset</th><th scope="col">Value</th><th scope="col">Interpretation</th></tr></thead><tbody><tr><td>Header / 0x100</td><td>0x00020001</td><td>AER, Version 2.</td></tr><tr><td>Uncorrectable Status / 0x104</td><td>0x00044000</td><td>Completion Timeout bit 14; Malformed TLP bit 18.</td></tr><tr><td>Mask / 0x108</td><td>0x00040000</td><td>Masks the recorded Malformed TLP error.</td></tr><tr><td>Severity / 0x10C</td><td>0x00040000</td><td>Non-Fatal Timeout; Fatal Malformed TLP.</td></tr><tr><td>AER Capabilities and Control / 0x118</td><td>0x0000100E</td><td>FEP=14; Timeout Header Log Capable=1.</td></tr><tr><td>Device Control / 0x78, 16 bits</td><td>0x2816</td><td>Non-Fatal and Fatal Reporting Enables set.</td></tr></tbody></table></div>
<p><code>0x00044000 &amp; ~0x00040000 = 0x00004000</code>: only the recorded Timeout is unmasked. A masked error can set Status but does not generate its Error Message or update the Header Log, TLP Prefix Log, or FEP. Fatal severity does not override masking. Under these assumptions, Timeout produces ERR_NONFATAL according to Severity and Device Control. These are configured values, not reset defaults.</p><p>The complete path also includes Bridge forwarding, Root primary-interface transmission controls, and interrupt conditions. Follow Figure 6-3 through the path. Unsupported Request and Advisory Non-Fatal errors have additional rules; the example's arithmetic is not a general reporting algorithm.</p><details class="source-note"><summary>Fields and reporting</summary><p>Figures 7-154–7-157/Tables 7-134–7-137 (pp.1112–1117); Figure 7-25/Table 7-21 (pp.958–962); §6.2.3.2.2 (p.673), §6.2.6/Figure 6-3 (pp.683–685), §6.2.8.1 (p.692).</p></details></section>
<section id="log"><h2>Validate the log before decoding the transaction</h2><p>FEP=14 is valid because Status bit 14 is set. Completion Timeout Header Log Capable bit 12 supports recording the timed-out Request. Multiple Header Recording bits 9 and 10 are clear; there is no Flit or Prefix support. The example has four DWORDs of log capacity but uses a three-DWORD Header.</p><div class="table-wrap"><table><caption>Request Header associated with the Timeout</caption><thead><tr><th scope="col">Offset</th><th scope="col">DWORD value</th><th scope="col">Content</th></tr></thead><tbody><tr><td>0x11C</td><td>0x00000040</td><td>3 DW Memory Read, Length=64 DW.</td></tr><tr><td>0x120</td><td>0x030013FF</td><td>Requester=0x0300, Tag=0x13, both Byte Enables=0xF.</td></tr><tr><td>0x124</td><td>0x40001000</td><td>Starting address.</td></tr><tr><td>0x128</td><td>Not interpreted</td><td>The fourth DWORD is undefined for this 12-byte Header.</td></tr></tbody></table></div><p>The Request covers 0x40001000–0x400010FF, or 256 bytes. It is the Request that did not complete in time, not a timed-out Completion. Figure 7-161 places Header byte 0 at bits 31:24 for DWORD reads; do not reverse these values again. Flit logs require Logged TLP was Flit Mode, Header Log Size, Logged TLP Size, and Type/OHC interpretation.</p><p>This locates a transaction and its timeout, not the responsible Endpoint, Completer, Link, or platform component. It cannot be assigned to the masked Malformed TLP event, which did not create this log.</p><details class="source-note"><summary>Validity and format</summary><p>§6.2.4.2 (pp.679–680); Figures 7-160/7-161, Tables 7-140/7-141 (pp.1121–1123). Memory Requests: <a href="/pcie/chapter-5-en/">Chapter 5</a>.</p></details></section>
<section id="root"><h2>The Root Source ID identifies the first reporter</h2><div class="table-wrap"><table><caption>Root Port snapshot for the same AER example</caption><thead><tr><th scope="col">Root AER base=0x100</th><th scope="col">Value</th><th scope="col">Meaning</th></tr></thead><tbody><tr><td>Root Error Command / 0x12C</td><td>0x00000002</td><td>Non-Fatal interrupt reporting enabled.</td></tr><tr><td>Root Error Status / 0x130</td><td>0x00000024</td><td>Uncorrectable Received and Non-Fatal Received.</td></tr><tr><td>Error Source ID / 0x134</td><td>0x03000000</td><td>Upper 16 bits=0x0300, or 03:00.0.</td></tr></tbody></table></div><p>The Root interrupt message number is 0 and primary-interface transmission conditions are satisfied. Source ID identifies the Endpoint reporting Timeout, not the physical cause. A second message in the same category sets Multiple without replacing the first Source ID.</p><p>Root Status updates independently of Root Error Command/Root Control, but still requires applicable primary-interface transmission enables. CPU interrupt delivery additionally requires vector and routing evidence. Sources: Figures 7-162–7-164/Tables 7-142–7-144 (pp.1123–1127).</p></section>
<section id="preserve"><h2>Preserve correlated records before clearing</h2><p>The author recommends saving status, configuration, FEP, valid logs, and Root/DPC evidence while checking for concurrency. Separate register reads are not automatically an atomic snapshot. Clearing the status indicated by FEP can advance hardware to another log, destroying the original association if done before capture.</p><p>With Multiple Header Recording enabled and valid FEP, the specification recommends processing records through FEP rather than clearing unrelated status; it lists an exception for masked errors known to lack recorded headers. PCI Status and AER Status are also cleared independently. Sources: §6.2.4.2 (pp.679–681, footnote 108), §6.2.7.1 (p.691).</p></section>
<section id="dpc"><h2>DPC can contain the error before its original message reaches the Root</h2><p>Now consider a separate event on Switch Downstream Port 02:01.0, with DPC base=0x300 and no RP Extensions.</p><div class="table-wrap"><table><caption>Separate DPC example</caption><thead><tr><th scope="col">Field / offset</th><th scope="col">Value</th><th scope="col">Meaning</th></tr></thead><tbody><tr><td>Header / 0x300</td><td>0x0001001D</td><td>ID=0x001D, Version=1.</td></tr><tr><td>Control / 0x306, 16 bits</td><td>0x000A</td><td>Trigger Enable=10b; Interrupt Enable=1.</td></tr><tr><td>Status / 0x308, 16 bits</td><td>0x000B</td><td>Triggered, Reason=01b, Interrupt Status=1.</td></tr><tr><td>Error Source ID / 0x30A, 16 bits</td><td>0x0300</td><td>The triggering ERR_NONFATAL came from 03:00.0.</td></tr></tbody></table></div>
<p>Enable=10b triggers on a local unmasked Uncorrectable Error or a received ERR_NONFATAL/ERR_FATAL. Reason=01b makes Source ID meaningful here; Reason=00b would not. The triggering message is discarded at the Port rather than forwarded to the Root. This example enables DPC interrupts but not DPC ERR_COR, so the earlier Root value 0x24 is not an expected companion snapshot.</p><p>DPC drives the downstream Link to Disabled. Before release, software must observe Link Active=0; a Root Port with RP Extensions also requires RP Busy=0. RP Busy is Reserved on a Switch Port. Clearing Interrupt Status acknowledges notification; clearing Trigger Status releases DPC and returns the Link to Detect. Subsequent Configuration accesses must honor Conventional Reset timing, followed by software recovery. Clearing Trigger does not establish successful application work.</p><details class="source-note"><summary>Containment and release</summary><p>§6.2.11–§6.2.11.2 (pp.694–697); Figures 7-297–7-301/Tables 7-261–7-265 (pp.1248–1254). Ownership: <a href="/pcie/chapter-13-en/">Chapter 13</a>.</p></details></section>
<section id="questions"><h2>Check the evidence limits</h2><details class="question"><summary>Can FEP=14 identify the latest Timeout when Status bit 14 is clear?</summary><p>No. FEP is invalid; a nonzero log cannot replace the validity condition. Source: §6.2.4.2.</p></details><details class="question"><summary>Does Status=0 prove an error never occurred?</summary><p>No. Status may have been cleared or reset, and detection and implementation conditions also matter. Sources: §6.2.4.2, Table 7-135.</p></details></section>
</article>
<nav class="bottom-nav" aria-label="Course and editions"><a href="/DOCS/pcie-course/index.html">Course overview</a><a href="/DOCS/pcie-course/chapter-12.html">Full Chinese tutorial</a><a href="/pcie/chapter-12-zh-tw/">繁體中文</a></nav>
</div>
