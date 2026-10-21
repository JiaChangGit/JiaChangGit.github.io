---
layout: post
title: "PCIe Chapter 1: Topology, Functions, and PCIe Identity"
date: 2026-10-20 00:00:00 +0800
permalink: /pcie/chapter-1-en/
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
<nav class="bottom-nav" aria-label="Course and editions"><a href="/DOCS/pcie-course/index.html">Course overview</a><a href="/DOCS/pcie-course/chapter-1.html">Full Chinese tutorial</a><a href="/pcie/chapter-1-zh-tw/">繁體中文</a></nav>
<article class="lesson">
<p class="lead">Two Functions do not necessarily mean two cards, and matching BDF values need the same Segment context before they can identify the same target. This chapter uses one example to connect physical Links, the bridge structure visible to software, and Function identifiers, then shows how register fields establish their relationships.</p>
<p><a href="/DOCS/pcie-course/chapter-1.html">Full Chinese tutorial and topology diagram</a> · <a href="/DOCS/pcie-course/index.html">Course roadmap</a> · <a href="/pcie/chapter-1-zh-tw/">繁體中文</a></p>
<aside class="note"><strong>Version and scope</strong><p>Register definitions follow PCI Express Base Specification Revision 6.0, with Segment context from PCI Firmware Specification Revision 3.3. Page numbers refer to the PDFs used by this course; printed and PDF page numbers coincide. The example uses conventional Bus/Device/Function (BDF) addressing, without Alternative Routing-ID Interpretation (ARI) or the identification scheme of Flattening Portal Bridge (FPB). Those mechanisms introduce additional discovery, numbering, or routing rules; ARI in particular changes how the Device/Function bits are interpreted. The example also excludes SR-IOV and Phantom/Shadow Functions. The latter mechanisms can use additional Function identifiers and are left to advanced chapters.</p></aside>

<section id="objects">
<h2>Why are a card, a Function, and a Port different objects?</h2>
<p>A card is a physical assembly. A Function is an object that software can identify and configure individually. One card can expose multiple Functions and may contain a Switch and multiple Endpoints. Function counts therefore do not directly establish card counts.</p>
<p>A Switch's Upstream Port faces the Root Complex, while its Downstream Ports face downstream components. Software sees each Switch Port as a PCI-to-PCI Bridge, with those bridges connected through an internal logical Bus. This does not turn external PCIe Links into a shared parallel bus, nor does each Bridge imply a separate chip.</p>
<p>Keep both views when reading a topology: Links describe connections between adjacent hardware components, while Bridge configuration describes the paths that software can identify toward downstream components.</p>
<details class="source-note"><summary>Specification locations for the Switch and its logical topology</summary><p>Base 6.0 §1.3.3, pp.106–107, with Figure 1-3 on p.107; §7.1, pp.903–904, with Figures 7-1 and 7-2 on p.904. The first explains Switch connections and bridge presentation; the latter contrasts the configuration structure visible to software. The example's internal Switch Bus connects only the virtual bridges for Downstream Ports. Endpoints sit at the other ends of external Links.</p></details>
</section>

<section id="types">
<h2>Which two fields establish a Function's role?</h2>
<p>First read the 8-bit Header Type at configuration offset <code>0x0E</code>. Its low seven bits select the header format, while bit 7 is the Multi-Function Device indication. Then locate the PCI Express Capability and read its 16-bit PCI Express Capabilities Register at base plus <code>0x02</code>. Device/Port Type in bits 7:4 identifies the PCIe role. Both names contain “Type,” but they answer different questions.</p>
<aside class="example"><strong>Teaching assumptions</strong><p>The addresses and values below are author-created, not hardware measurements. Enumeration is complete, the topology remains stable while it is read, and all configuration reads succeed. Each Function's PCI Express Capability has already been found by following the Capability list and happens to start at <code>0x70</code>, placing the role field at <code>0x72</code> in this example. Device/Port Type values in the table are extracted field values, not full Register reads. For the Capability search, see <a href="/DOCS/pcie-course/chapter-0.html#case">the Chapter 0 example</a>.</p></aside>
<div class="table-wrap"><table><caption>Decode the header format separately from the PCIe role</caption><thead><tr><th scope="col">Target</th><th scope="col">Header Type read</th><th scope="col">Device/Port Type field</th><th scope="col">Interpretation</th></tr></thead><tbody>
<tr><td>Endpoint A, Function 0</td><td><code>0x80</code></td><td><code>0x0</code></td><td>Type 0 header; may have multiple Functions; PCI Express Endpoint.</td></tr>
<tr><td>Root Port</td><td><code>0x01</code></td><td><code>0x4</code></td><td>Type 1 header; Root Port.</td></tr>
<tr><td>Switch Upstream Port</td><td><code>0x01</code></td><td><code>0x5</code></td><td>Type 1 header; Switch Upstream Port.</td></tr>
<tr><td>Switch Downstream Port</td><td><code>0x01</code></td><td><code>0x6</code></td><td>Type 1 header; Switch Downstream Port.</td></tr>
</tbody></table></div>
<pre><code>Header format: 0x80 &amp; 0x7F = 0
Multi-Function Device: (0x80 &amp; 0x80) &gt;&gt; 7 = 1
Device/Port Type: (PCIe_Capabilities &amp; 0x00F0) &gt;&gt; 4</code></pre>
<p>The value <code>0x80</code> means neither “Type 128” nor “eight Functions are present.” A set Multi-Function Device bit means that the device may contain multiple Functions. Actual Function presence still needs discovery evidence. Endpoint A here means the component providing Endpoint Functions; the example separately assumes that both Function 0 and Function 1 of that component have been found.</p>
<details class="source-note"><summary>Which figures and tables should be read first?</summary><p>Start with Base 6.0 §7.5.1.1.9, Figure 7-8 and Table 7-7 (pp.924–925), to separate the header format from bit 7. Then use Figure 7-21 (p.952) to locate the Register within the Capability, followed by Figure 7-23 and Table 7-19 (pp.953–954) for Device/Port Type. A Type 1 header identifies the bridge layout but does not by itself distinguish a Root Port from a Switch Port.</p></details>
</section>

<section id="path">
<h2>Which downstream path reaches 0000:03:00.1?</h2>
<p>The example places a Root Port and a Switch with two Downstream Ports in Segment <code>0000</code>. Endpoint A's two Functions are on Bus <code>03</code>, while Endpoint B is on Bus <code>04</code>. The table is a snapshot of an already configured topology. This chapter interprets the result; assigning Bus Numbers belongs to the enumeration chapter.</p>
<div class="table-wrap"><table><caption>Teaching snapshot: Bridge BDFs and downstream Bus ranges (all numbers are hexadecimal)</caption><thead><tr><th scope="col">Bridge role</th><th scope="col">BDF in Segment 0000</th><th scope="col">Secondary</th><th scope="col">Subordinate</th><th scope="col">Downstream components in this example</th></tr></thead><tbody>
<tr><td>Root Port</td><td><code>00:01.0</code></td><td><code>01</code></td><td><code>04</code></td><td>The Switch and both of its branches.</td></tr>
<tr><td>Switch Upstream Port</td><td><code>01:00.0</code></td><td><code>02</code></td><td><code>04</code></td><td>The two Downstream Ports on internal Bus 02.</td></tr>
<tr><td>Switch Downstream Port A</td><td><code>02:01.0</code></td><td><code>03</code></td><td><code>03</code></td><td>Endpoint A: <code>03:00.0</code> and <code>03:00.1</code>.</td></tr>
<tr><td>Switch Downstream Port B</td><td><code>02:02.0</code></td><td><code>04</code></td><td><code>04</code></td><td>Endpoint B: <code>04:00.0</code>.</td></tr>
</tbody></table></div>
<p>Secondary Bus Number identifies the Bus immediately downstream of a Bridge. Subordinate Bus Number bounds the upper end of its downstream Bus Number range. Target Bus <code>03</code> is within the Root Port's <code>01–04</code>, the Upstream Port's <code>02–04</code>, and Downstream Port A's <code>03–03</code> ranges. Downstream Port B covers only <code>04–04</code>, so it is outside the path to this target.</p>
<p>These ranges check the known topology; they do not establish that every number in a range has a populated Bus. A Bridge's own BDF also differs from the Bus it leads to: <code>02:01.0</code> is on Bus <code>02</code> and has Secondary <code>03</code>. This chapter does not derive a Bridge's own BDF from Primary Bus Number. Base 6.0 retains that field for legacy compatibility, and PCIe generally does not use it.</p>
<details class="source-note"><summary>Where are the downstream Bus Number fields?</summary><p>Base 6.0 §7.5.1.3, Figure 7-14 (p.936), shows the Type 1 Header. Secondary and Subordinate are 8-bit fields at byte offsets <code>0x19</code> and <code>0x1A</code>, respectively; their meanings are in §7.5.1.3.3–§7.5.1.3.4 (p.937). The neighboring Primary field is at <code>0x18</code>, with its PCIe compatibility explanation in §7.5.1.3.2 on the same page.</p></details>
</section>

<section id="identity">
<h2>What information do BDF, Segment, and Requester ID retain?</h2>
<p>Under conventional addressing, BDF contains an 8-bit Bus Number, a 5-bit Device Number, and a 3-bit Function Number. The first four digits of <code>0000:03:00.1</code> identify the Segment; the remaining <code>03:00.1</code> is the BDF within that Segment. These numbers describe a logical identification location, not a physical slot number.</p>
<div class="table-wrap"><table><caption>Matching or similar numbers can refer to different Functions</caption><thead><tr><th scope="col">Identifier</th><th scope="col">Object in this example</th><th scope="col">Distinction to preserve</th></tr></thead><tbody>
<tr><td><code>0000:03:00.0</code></td><td>Endpoint A, Function 0.</td><td>The next row shares its Bus and Device but has a different Function.</td></tr>
<tr><td><code>0000:03:00.1</code></td><td>Endpoint A, Function 1.</td><td>Use this Function's own Configuration Space reads.</td></tr>
<tr><td><code>0001:03:00.0</code></td><td>An Endpoint in another Segment.</td><td>Its BDF matches the first row, but its Segment differs.</td></tr>
</tbody></table></div>
<p>As a further teaching assumption, <code>03:00.0</code> has also been discovered in Segment <code>0001</code>. This is a second logical scope created for the example, not a downstream branch of the preceding table. Dropping the Segment would incorrectly merge distinct records.</p>
<p>When <code>0000:03:00.1</code> originates a Request, its 16-bit Requester ID is formed as follows in this example:</p>
<pre><code>Requester ID = (Bus &lt;&lt; 8) | (Device &lt;&lt; 3) | Function
             = (0x03 &lt;&lt; 8) | (0x00 &lt;&lt; 3) | 0x1
             = 0x0301</code></pre>
<p><strong>Example deduction:</strong> <code>0x0301</code> preserves the BDF but does not encode Segment <code>0000</code> into those 16 bits. This conclusion applies only to the Requester ID field. It does not mean that all PCIe packets lack Segment information: some Base 6.0 Flit Mode packets have separate related fields. BDF is also not a permanent hardware identity. If records come from different configurations at different times, matching or changed BDF values alone cannot establish whether they describe the same physical device.</p>
<details class="source-note"><summary>Specification locations for identification scope and bit allocation</summary><p>Conventional BDF: Base 6.0 §7.3.1 (p.911), §2.2.4.2 and Table 2-8 (p.147), and Figures 2-20 and 2-22 (p.148). Requester ID: §2.2.6.2 (pp.156–157); p.156 describes the 16-bit identifier and Bus/Device Numbers that can change at runtime, while p.157 separately discusses Segment fields. Segment Group scope: Firmware 3.3 §1.3 (pp.8–9) and §4.3.2.3 (p.47).</p></details>
</section>

<section id="self-check">
<h2>Do changed observations support the same conclusions?</h2>
<details class="question"><summary>Does a Header Type read of 0x80 prove that Function 1 exists?</summary><p>No. Table 7-7 (pp.924–925) establishes a Type 0 header and that the device may contain multiple Functions. Function 1 still needs valid discovery evidence before it can be reported as present. That evidence is a separate teaching assumption in this example.</p></details>
<details class="question"><summary>If the target becomes 0000:04:00.0, does its path still pass through Downstream Port A?</summary><p>No. In this snapshot, Bus <code>04</code> lies within Downstream Port B's <code>04–04</code> range, outside A's <code>03–03</code> range. The path still passes through the same Root Port and Upstream Port; only the downstream Switch branch changes. (Base 6.0 §7.5.1.3.3–§7.5.1.3.4, p.937.)</p></details>
<details class="question"><summary>Can two records with BDF 03:00.0 be treated as the same Function?</summary><p>Not yet. First establish the Segment and the configuration time represented by each record. The example's <code>0000:03:00.0</code> and <code>0001:03:00.0</code> are different Functions. Across different times, a matching BDF alone also does not establish the same hardware identity. (Firmware 3.3 §1.3, pp.8–9; Base 6.0 §2.2.6.2, p.156.)</p></details>
</section>
<p>With these identifiers understood, the next step is a systematic approach to querying a Function's Configuration Space and Capabilities. The <a href="/DOCS/pcie-course/chapter-1.html">full Chapter 1 Chinese tutorial</a> provides the topology diagram, expanded interpretation, and source references. Continue with <a href="/DOCS/pcie-course/chapter-2.html">Chapter 2 on Configuration Space and Capabilities</a>.</p>
</article>
<nav class="bottom-nav" aria-label="Course and editions"><a href="/DOCS/pcie-course/index.html">Course overview</a><a href="/DOCS/pcie-course/chapter-1.html">Full Chinese tutorial</a><a href="/pcie/chapter-1-zh-tw/">繁體中文</a></nav>
</div>
