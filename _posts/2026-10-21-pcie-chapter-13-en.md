---
layout: post
title: "PCIe Chapter 13: Firmware, ACPI, and OS Ownership"
date: 2026-10-21 00:00:00 +0800
permalink: /pcie/chapter-13-en/
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
<nav class="bottom-nav" aria-label="Course and editions"><a href="/DOCS/pcie-course/index.html">Course overview</a><a href="/DOCS/pcie-course/chapter-13.html">Full Chinese tutorial</a><a href="/pcie/chapter-13-zh-tw/">繁體中文</a></nav>
<article class="lesson">
<p class="lead">Locating a PCIe register does not establish permission to configure it. Firmware prepares the boot environment; the OS manages resources and features according to platform descriptions and negotiated ownership. This report separates UEFI, ACPI, and PCI Firmware responsibilities through nonzero-Start-Bus ECAM and _OSC examples.</p><aside class="note"><strong>Versions and sources</strong><p>The primary source is PCI Firmware 3.3; hardware semantics use PCIe Base 6.0. Firmware 3.3 references Base 5.0, so these are not a matched edition pair. UEFI 2.11/ACPI 6.6 supplement only the identified official indexed excerpts; full retrieval was unavailable. All example values are author assumptions.</p></aside>
<section id="roles"><h2>Choose the specification by the question</h2><div class="table-wrap"><table><caption>Document responsibilities</caption><thead><tr><th scope="col">Document</th><th scope="col">Use in this report</th></tr></thead><tbody><tr><td>UEFI 2.11 §14</td><td>PCI Bus/Device Drivers and the Root Bridge I/O and PCI I/O interface entry points.</td></tr><tr><td>ACPI; PCI Firmware 3.3 §3–§4</td><td>Host Bridge platform descriptions, _CRS, _OSC, and their PCI-specific rules.</td></tr><tr><td>PCIe Base 6.0</td><td>Hardware semantics of capabilities, registers, events, and transactions.</td></tr></tbody></table></div><p>UEFI PCI Device Drivers use PCI I/O in the boot services environment; PCI Bus Drivers create controller device handles. Root Bridge I/O is the entry point for bus-level access abstraction. These interfaces do not replace chipset-specific enumeration details, and an OS native driver is not necessarily a UEFI driver.</p><details class="source-note"><summary>UEFI verification boundary</summary><p><a href="https://uefi.org/sites/default/files/resources/UEFI_Spec_Final_2.11.pdf">UEFI 2.11</a> §14.3.7–§14.4 (document p.623) was checked through official indexed excerpts; interface locations through the <a href="https://uefi.org/specs/UEFI/2.11/">2.11 contents</a>. Full retrieval returned 403; unread material is not used to infer additional requirements.</p></details></section>
<section id="handoff"><h2>Handoff does not imply every device was configured</h2><p>Firmware §3.5 requires configuration of all Host Bridges and PCI-to-PCI Bridges leading to boot/console devices. The OS cannot assume every other path is configured. UEFI drivers/applications must not change BAR/Bridge assignments owned by the firmware configurator. Existing BAR interpretation still requires the corresponding Enables and platform translation information; CPU and BAR addresses may differ.</p><p>ACPI Host Bridge objects provide _HID/_CID, _CRS, and conditionally information such as _SEG. Segment and BDF identify the target together; a namespace path is not a BDF. Sources: PCI Firmware 3.3 §3.5 (pp.34–37), §4.1.5 (pp.45–46); BAR details in <a href="/pcie/chapter-4-en/">Chapter 4</a>.</p></section>
<section id="address"><h2>MCFG locates configuration access; _CRS bounds resources</h2><div class="table-wrap"><table><caption>Author-created nonzero Start Bus example</caption><thead><tr><th scope="col">Item</th><th scope="col">Value</th></tr></thead><tbody><tr><td>MCFG Base Address / Segment</td><td>0xE0000000 / 0x0002</td></tr><tr><td>Start Bus / End Bus</td><td>0x40 / 0x4F</td></tr><tr><td>Bus / Device / Function / Offset</td><td>0x42 / 0x03 / 0x01 / 0x180</td></tr><tr><td>Configuration access address</td><td>0xE4219180</td></tr></tbody></table></div><p>Select the Segment entry and check the Bus range, then calculate relative to Bus 0: <code>0xE0000000 + (0x42 &lt;&lt; 20) + (0x03 &lt;&lt; 15) + (0x01 &lt;&lt; 12) + 0x180 = 0xE4219180</code>. The entry covers 0xE4000000–0xE4FFFFFF, or 16 MiB. Subtracting Start Bus incorrectly produces 0xE0219180. Do not assume anything about the region between the Base and the supported range.</p><p>Suppose _CRS provides downstream Memory at 0x90000000–0x90FFFFFF without translation. BAR allocation still requires size, alignment, occupancy, and intervening-window checks. ECAM is not a BAR resource pool. MCFG and _CBA for hot-added Host Bridges also have different roles; Host Bridge addition is not ordinary Endpoint insertion.</p><details class="source-note"><summary>Reading route</summary><p>Firmware Table 4-1 (p.39) → Tables 4-2/4-3 (pp.41–42) → §4.1.4 (pp.44–45). _CBA: §4.1.3 (pp.42–44); _CRS: §3.5 (pp.35–37), §4.3.2 (p.47).</p></details></section>
<section id="osc"><h2>Declaring support, requesting control, and receiving ownership are distinct</h2><p>PCI Host Bridge _OSC applies to its originating hierarchy. Firmware §4.5.1 specifies UUID <code>33DB4D5B-1FF7-401C-9657-7441C03DD766</code>, Revision=1, and a three-DWORD buffer. DWORD 1 holds generic Query/return information. DWORD 2 is the one-way OS Support declaration; returned changes do not grant control. DWORD 3 carries Control requests and responses.</p><p>Input DWORD 1 bit 0=1 means Query; clearing it requests control. Returned bit 0 is Reserved. Return bits 1, 2, and 3 indicate failure, unrecognized UUID, and unrecognized Revision; bit 4 indicates Capabilities Masked. Preserved Control bits after an error are not successful grants.</p><p>A grant does not prove every device has the capability; a zero response does not prove absent hardware. Firmware cannot deny solely because it lacks explicit feature support; it needs explicit platform incompatibility knowledge. The OS must still inspect individual Slots/Functions.</p><details class="source-note"><summary>Interface and generic fields</summary><p>Firmware §4.5.1 (pp.48–49), Tables 4-4–4-6 (pp.49–58). Generic fields: official indexed excerpt from <a href="https://uefi.org/sites/default/files/resources/ACPI_Spec_6.6.pdf">ACPI 6.6 §6.2.12</a>, document p.401. Full retrieval failed; other ACPI behavior is not inferred. Firmware §4.5.3 (pp.61–62) also demonstrates 0x10 masking status.</p></details></section>
<section id="negotiation"><h2>Read a complete negotiation through its dependencies</h2><p>The example requests native Hot-Plug bit 0, native PME bit 2, AER bit 3, PCI Express Capability Structure bit 4, and DPC bit 7: Control=0x9D. DPC also requires Support bit 7 for Error Disconnect Recover (EDR). Support=0x9F declares bits 0–4 and 7: Extended Config operation regions, ASPM, Clock PM, Segment Groups, MSI, and EDR. LTR, Completion Timeout, and SFI control are not requested.</p><p>Hot-Plug, PME, and AER require Control bit 4; DPC additionally requires Control bit 3. Firmware retaining DPC must retain AER. Granting DPC requires granting AER and Capability control. Bit 4's broad name does not override individual ownership rules. ASPM Support is not PME Control and does not replace L1.2 hardware, timing, or LTR requirements.</p><div class="table-wrap"><table><caption>Three calls when the platform retains AER/DPC</caption><thead><tr><th scope="col">Stage</th><th scope="col">Input DWORD 1 / Control</th><th scope="col">Return DWORD 1 / Control</th></tr></thead><tbody><tr><td>First Query</td><td>0x00000001 / 0x0000009D</td><td>0x00000010 / 0x00000015</td></tr><tr><td>Adjusted Query</td><td>0x00000001 / 0x00000015</td><td>0x00000000 / 0x00000015</td></tr><tr><td>Control request</td><td>0x00000000 / 0x00000015</td><td>0x00000000 / 0x00000015</td></tr></tbody></table></div><p>Support remains 0x0000009F. The assumed platform has a known native-DPC incompatibility, no other errors, and no prior grants. <code>0x9D &amp; ~0x15 = 0x88</code> identifies masked AER/DPC. A Query must not change hardware settings; the specification strongly recommends querying until masking clears. The second row still does not transfer ownership. The third valid response grants Hot-Plug, PME, and the applicable Capability control.</p><details class="source-note"><summary>Dependencies and call ordering</summary><p>Firmware Tables 4-4–4-6 (pp.49–58), §4.5.2 (pp.59–60), §4.5.3 (pp.61–62). The example policy is author-created, not a copy of the specification's ASL platform example.</p></details></section>
<section id="ownership"><h2>Handoff responsibilities and limited EDR exceptions</h2><p>When granting Hot-Plug, firmware establishes native event routing and then stops updating slot indicators and power state. PME has corresponding routing/register restrictions. Subsequent calls within the same boot and Host Bridge must retain declared support and granted control requests; firmware cannot revoke grants. Firmware 3.3 provides no mechanism for the OS to relinquish acquired control.</p><p>Without AER/DPC ownership, the OS cannot arbitrarily modify Mask, Severity, or DPC Control. Table 4-6 nevertheless defines EDR cooperation exceptions. Between EDR Notify and the OS invocation of _OST, it permits specified Device/AER/RP PIO Status writes on the triggering Port, plus DPC Trigger Status handling. The latter is also permitted while processing subsequent hot-removal below a Port whose Trigger remains set. After the corresponding _OST returns, until downstream Function reinitialization or disablement completes, limited writes to specified downstream DPC/Device/AER Status are permitted. Firmware must honor the corresponding write prohibitions during each window.</p><p>These exceptions do not transfer full DPC Configuration ownership or remove Link-inactive/applicable-RP-Busy requirements. Determine the target, time window, notification, and _OST context together. If _OSC is absent, the OS must not enable features defined by this interface.</p><details class="source-note"><summary>Responsibilities and recovery exceptions</summary><p>Firmware Table 4-6 (pp.53–57), §4.5.2.2–§4.5.2.3 (p.59), §4.5.1 (p.49). Connect <a href="/pcie/chapter-11-en/">Chapter 11</a> slot capabilities with <a href="/pcie/chapter-12-en/">Chapter 12</a> containment requirements.</p></details></section>
<section id="questions"><h2>Keep the three evidence categories separate</h2><details class="question"><summary>Does Support bit 7=1 give the OS DPC ownership?</summary><p>No. It declares EDR support; valid Control requests, dependencies, and a successful non-Query grant are still required. Sources: Tables 4-4–4-6.</p></details><details class="question"><summary>Can successful MCFG access and _OSC negotiation override insufficient _CRS resources?</summary><p>No. Configuration access, ownership, and resource capacity are different questions. Sources: Firmware §3.5, §4.1, §4.5.</p></details></section>
</article>
<nav class="bottom-nav" aria-label="Course and editions"><a href="/DOCS/pcie-course/index.html">Course overview</a><a href="/DOCS/pcie-course/chapter-13.html">Full Chinese tutorial</a><a href="/pcie/chapter-13-zh-tw/">繁體中文</a></nav>
</div>
