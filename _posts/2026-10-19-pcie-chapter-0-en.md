---
layout: post
title: "PCIe Chapter 0: From the System View to Your First Specification Query"
date: 2026-10-19 00:00:00 +0800
permalink: /pcie/chapter-0-en/
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

html:not([data-theme="dark"]) .pcie-article { color-scheme: light; }
html[data-theme="dark"] .pcie-article { color-scheme: dark; }

.pcie-article { background: transparent; margin: 1.5rem 0; }
.pcie-article .lesson { padding: 0; border: 0; background: transparent; }
</style>
<div class="pcie-article" lang="en">
<nav class="bottom-nav" aria-label="Course and editions"><a href="/DOCS/pcie-course/index.html">Course overview</a><a href="/DOCS/pcie-course/chapter-0.html">Full Chinese tutorial</a><a href="/pcie/chapter-0-zh-tw/">繁體中文</a></nav>
<article class="lesson">
<p class="lead">A system can list a PCIe device before that device is ready to move data. Likewise, a feature defined in a specification is not necessarily supported by the device in front of you. This chapter establishes the system context, then works through one query: locating capability fields in Configuration Space and separating supported behavior from current operation.</p>
<p><a href="/DOCS/pcie-course/chapter-0.html">Full Chinese tutorial and diagrams</a> · <a href="/DOCS/pcie-course/index.html">Course roadmap</a> · <a href="/pcie/chapter-0-zh-tw/">繁體中文</a></p>
<aside class="note"><strong>Version scope</strong><p>Register definitions follow PCI Express Base Specification Revision 6.0; firmware context follows PCI Firmware Specification Revision 3.3. The latter references Base 5.0 in §1.2 (p.7), so these documents must not be treated as a matched revision set. All page numbers below refer to the PDFs used for this course; printed and PDF page numbers coincide.</p></aside>

<section id="system">
<h2>What must happen after a device is connected?</h2>
<p>A Root Complex connects the CPU/memory subsystem to the I/O hierarchy. A Root Port establishes an outward Link, a Switch extends the connection paths, and an Endpoint provides device functionality. A Link connects two adjacent ends; Lanes make up that Link. x4 means four Lanes, not four devices.</p>
<p>The basic object identified and configured by software is a Function. One card can expose multiple Functions. The example notation <code>0000:03:00.0</code> identifies a Segment, Bus, Device, and Function; Bus, Device, and Function are commonly abbreviated as BDF. A Segment is a logical grouping, not an additional hardware component, and this identifier is not a memory address.</p>
<p>Hardware at both ends must first meet the conditions for establishing a Link. System software discovers Functions and assigns resources; the device driver prepares the device-specific working interface. This is a teaching model of dependencies, and a platform may perform the work in stages. Firmware 3.3 §3.5 requires firmware to configure the complete paths to boot and console devices, as well as all Host Bridges. It does not guarantee that every Endpoint has been configured.</p>
<div class="table-wrap"><table><caption>Three kinds of access that may participate in one operation</caption><thead><tr><th scope="col">Purpose</th><th scope="col">Information to locate</th></tr></thead><tbody>
<tr><td>Identify a Function or query PCIe capabilities</td><td>The headers and Capability structures in Configuration Space.</td></tr>
<tr><td>Operate the device interface from the CPU</td><td>Resources described by BARs and the device's register definitions. Access through memory mapping is MMIO (Memory-Mapped I/O).</td></tr>
<tr><td>Move working data through device-initiated accesses</td><td>DMA (Direct Memory Access) buffers, device-visible addresses, and access conditions. The CPU still prepares the work.</td></tr>
</tbody></table></div>
<p>A BAR is a Base Address Register in Configuration Space, not the data buffer itself. Readable Configuration Space alone does not establish that MMIO or DMA is ready.</p>
<details class="source-note"><summary>Specification locations for the system context</summary><p>Base 6.0 §1.2–§1.4, pp.100–109 (Figure 1-2: p.103); §2.1.1, pp.116–117; BARs: §7.5.1.2.1, pp.928–930. Firmware 3.3 §1.3, pp.8–9; §3.1–§3.2, pp.32–33; handoff requirements: §3.5, pp.34–35.</p></details>
</section>

<section id="query">
<h2>Why does current speed not tell us which speeds are supported?</h2>
<p>Capability fields describe supported behavior, control fields describe related settings, and status fields describe the current result. This query first checks the local Port's supported set and then the Link's current speed. Neither answer substitutes for the other.</p>
<p>Each Function has 4096 bytes of PCIe Configuration Space. The PCI Express Capability is in the conventional Capability list within the first 256 bytes. Its name does not mean that it belongs to the separate Extended Capability list. (Base 6.0 §7.2 / Figure 7-3, pp.905–906; §7.5.3, p.951.)</p>
<aside class="example"><strong>Teaching assumptions</strong><p>The topology, locations, and values below are author-created, not hardware measurements. The target is an already discovered, ordinary PCI Express Endpoint, not a Root Complex Integrated Endpoint (RCiEP) or a Virtual Function (VF) used in virtualization. Conventional Bus/Device/Function (BDF) addressing is used, without Alternative Routing-ID Interpretation (ARI), which interprets Function identifiers differently. All configuration reads succeed. The Link is up and remains stable throughout the query, and the Link Capabilities 2 speed vector used here is implemented. Every offset is a byte offset within this Function's Configuration Space, not a CPU physical address.</p></aside>
<div class="table-wrap"><table><caption>Follow the list, then check the structure version and component type</caption><thead><tr><th scope="col">Step</th><th scope="col">Assumed read and interpretation</th><th scope="col">Base 6.0 reading location</th></tr></thead><tbody>
<tr><td>Identify the header</td><td>An 8-bit read at <code>0x0E</code> returns <code>0x00</code>; <code>0x00 &amp; 0x7F = 0</code> selects Type 0. A 16-bit read at <code>0x06</code> returns <code>0x0010</code>, with Status bit 4 set.</td><td>Figure 7-8 / Table 7-7, pp.924–925; Figure 7-10, p.928; Figure 7-6 / Table 7-5, pp.921–922.</td></tr>
<tr><td>Find the list entry</td><td>An 8-bit read at <code>0x34</code> returns <code>0x40</code>. Mask the low two bits first: <code>0x40 &amp; 0xFC = 0x40</code>.</td><td>§7.5.1.1.11, p.926.</td></tr>
<tr><td>Pass the PM Capability</td><td>A 16-bit read at <code>0x40</code> returns <code>0x7001</code>: the low-byte ID is <code>0x01</code> and the high-byte Next Pointer is <code>0x70</code>.</td><td>Figure 7-18 / Table 7-14, p.945.</td></tr>
<tr><td>Find the PCIe Capability</td><td>A 16-bit read at <code>0x70</code> returns <code>0x0010</code>: the ID is <code>0x10</code> and the Next Pointer is zero. Record <code>cap_base = 0x70</code>.</td><td>Figure 7-22 / Table 7-18, p.953.</td></tr>
<tr><td>Check version and type</td><td>A 16-bit read at <code>0x72</code> returns <code>0x0002</code>: the low four bits give Version 2, and bits 7:4 give type 0, a PCI Express Endpoint.</td><td>Figure 7-23 / Table 7-19, pp.953–954.</td></tr>
</tbody></table></div>
<p>Configuration Space uses little-endian formatting, so the lower-addressed byte of <code>0x7001</code> is <code>0x01</code> (Base 6.0 §7.5.1.1, p.916). List locations and ordering can differ; <code>0x70</code> is not a universal constant.</p>
<p>If the list ends without the target, or a read fails, there is no basis for interpreting an arbitrary location as that structure. An unsuccessful read is not a valid response declaring lack of support.</p>
<p>Capability Version 2 does not mean PCIe Gen2, and by itself does not guarantee that older hardware implements the speed vector. Implementation is a separate assumption here. Using Base 6.0 to interpret the fields also does not mean that the device must support 64 GT/s. For older hardware, see the implementation note in §7.5.3.18 (p.1000).</p>
</section>

<section id="decode">
<h2>How do the register values become an answer?</h2>
<p>Start with Figure 7-21 (p.952) and add each register's relative offset to the Capability base. Then consult the capability definition in Figure 7-38 / Table 7-35 (pp.998–1000), followed by the status definition in Figure 7-29 / Table 7-26 (pp.978–979). The question determines the reading order. Figures locate fields; tables and surrounding requirements explain their interpretation. Check the revision and applicable component at every step rather than inferring meaning from a field name alone.</p>
<pre><code>Link Capabilities 2: 0x70 + 0x2C = 0x9C; read 32 bits → 0x0180001E
Link Status:         0x70 + 0x12 = 0x82; read 16 bits → 0x0043</code></pre>
<p>The Supported Link Speeds Vector occupies register bits 7:1. Mask those positions, then shift the field down:</p>
<pre><code>(0x0180001E &amp; 0x000000FE) &gt;&gt; 1 = 0x0F</code></pre>
<p>Field bits 0–3 are all set, indicating support for <strong>2.5, 5, 8, and 16 GT/s</strong>. Bits 4–5 are clear, so 32 and 64 GT/s are not advertised; bit 6 is reserved. Field bit 0 was originally register bit 1, so these two numbering systems must remain distinct. The full read value keeps register bits 23 and 24 set to meet Table 7-35's detection-capability requirements for devices supporting 16 GT/s or above. Those bits do not prove that Retimers are present in the path.</p>
<p>Link Status instead contains an encoded value, not another supported-speed bitmap:</p>
<pre><code>Current Link Speed: 0x0043 &amp; 0x000F = 3
Negotiated Link Width: (0x0043 &amp; 0x03F0) &gt;&gt; 4 = 4</code></pre>
<p>Code 3 selects field bit 2 of the speed vector, meaning <strong>8 GT/s</strong>; width 4 means <strong>x4</strong>. These masks assume the stated read widths. They cannot be applied directly to a 32-bit value read at a different offset.</p>
<p>Table 7-26 makes both fields undefined when the Link is not up. The value <code>0x0043</code> does not itself establish that the Link is up. Nor does a clear bit 13 alone establish that the Link is down: implementation of that status bit depends on reporting capability (Table 7-23 and Table 7-26, pp.969 and 979).</p>
</section>

<section id="limits">
<h2>Does operating at only 8 GT/s prove a fault?</h2>
<p><strong>Example deduction:</strong> Under the stated assumptions, the local Port advertises speeds up to 16 GT/s, while its Link currently operates at 8 GT/s and x4. These reads do not explain the lower speed. The partner's capabilities, relevant settings, and Link state must also be checked. x4 is not evidence of the maximum supported width, and GT/s is not application GB/s. Useful throughput also depends on Lane count, encoding, packet overhead, and workload (Base 6.0 §1.2, pp.101–102).</p>
</section>

<section id="self-check">
<h2>Does the same conclusion survive a changed condition?</h2>
<details class="question"><summary>If the Capability base moves to 0x90, can the capability still be read at 0x9C?</summary><p>No. From Figure 7-21 (p.952), Link Capabilities 2 moves to <code>0x90 + 0x2C = 0xBC</code>, and Link Status to <code>0x90 + 0x12 = 0xA2</code>. The new base is a teaching assumption; the relative offsets stay the same.</p></details>
<details class="question"><summary>If Current Link Speed is 4, does that mean two speeds are supported simultaneously?</summary><p>No. With valid Link-state conditions, code 4 means a current speed of 16 GT/s. The supported set still requires a separate vector read. (Table 7-26 and Table 7-35, pp.978 and 998.)</p></details>
<details class="question"><summary>If the Link is down and a previously obtained value is 0x0043, can it describe the current speed and width?</summary><p>No. Table 7-26 (p.978) defines speed and width as undefined when the Link is not up. Plausible numbers do not replace the required validity condition.</p></details>
</section>
<p>The next step is to clarify topology, Functions, and identification scope before studying Configuration Space in depth. See the <a href="/DOCS/pcie-course/chapter-0.html">full Chapter 0 Chinese tutorial</a> for field diagrams, the expanded example, and source references. <a href="/DOCS/pcie-course/chapter-1.html">Chapter 1 is now available</a>; Chapters 2–7 are available, and Chapters 8–19 remain planned.</p>
</article>
<nav class="bottom-nav" aria-label="Course and editions"><a href="/DOCS/pcie-course/index.html">Course overview</a><a href="/DOCS/pcie-course/chapter-0.html">Full Chinese tutorial</a><a href="/pcie/chapter-0-zh-tw/">繁體中文</a></nav>
</div>
