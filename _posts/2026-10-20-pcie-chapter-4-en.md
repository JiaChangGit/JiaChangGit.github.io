---
layout: post
title: "PCIe Chapter 4: BARs, Address Spaces, and Resource Allocation"
date: 2026-10-20 00:00:00 +0800
permalink: /pcie/chapter-4-en/
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
<nav class="bottom-nav" aria-label="Course and editions"><a href="/DOCS/pcie-course/index.html">Course overview</a><a href="/DOCS/pcie-course/chapter-4.html">Full Chinese tutorial</a><a href="/pcie/chapter-4-zh-tw/">繁體中文</a></nav>
<article class="lesson">
<p class="lead">Discovering a Function is followed by resource allocation and forwarding setup. BARs describe the Endpoint's own resources, Bridge Windows determine which address ranges reach downstream, and Command bits control permitted accesses. All three must be consistent.</p>
<p><a href="/DOCS/pcie-course/chapter-4.html">Full Chinese tutorial</a> · <a href="/DOCS/pcie-course/index.html">Course roadmap</a> · <a href="/pcie/chapter-4-zh-tw/">繁體中文</a></p>
<aside class="note"><strong>Versions and assumptions</strong><p>Fields follow Base 6.0; address views and handoff follow PCI Firmware 3.3, which is not its matching edition. The example is an ordinary Type 0 PCI Express Endpoint, not a VF, without Enhanced Allocation or Resizable BAR. Values are author-created, with no hardware operation. During sizing the driver is not using the device, no transactions are outstanding, and MSE/BME are clear. Software saves original BARs and confirms configuration write completion. Printed and PDF page numbers coincide.</p></aside>
<section id="format"><h2>Identify the format before calculating size</h2>
<p>A BAR resides in Configuration Space; it is not a workload buffer. A Type 0 Header has six DWORD locations, and a 64-bit BAR consumes two consecutive locations. A Bridge's Type 1 Header has only two BAR locations, distinct from its downstream Memory Windows.</p>
<p>A Memory BAR has bit 0 clear; bits 2:1 encode 32-bit as 00b and 64-bit as 10b, with Prefetchable in bit 3. An I/O BAR has bit 0 set and address bits beginning at bit 2, so the Memory BAR's four-bit mask does not apply. This example uses no I/O BAR: an ordinary PCIe Endpoint must not depend on OS allocation of I/O resources and must not generate I/O Requests.</p>
<p>Prefetchable expresses permitted behavior such as reads without side effects and tolerance of write merging, not current CPU cache state. A Prefetchable BAR on this ordinary Endpoint must support 64-bit addressing; a non-Prefetchable BAR may be 32-bit.</p>
<details class="source-note"><summary>Reading order</summary><p>Locate the BAR through Figure 7-10 (p.928) or Figure 7-14 (p.936). Decode its format through Figures 7-11/7-12 and Table 7-9 (p.929), then read capacity, pairing, and alignment rules in §7.5.1.2.1 (p.930). Ordinary Endpoint restrictions: §1.3.2.2, p.105.</p></details></section>
<section id="size"><h2>Size probes require the correct 32-bit or 64-bit width</h2>
<p>The specified method disables the corresponding decoding, saves the original BAR, writes all ones, reads it back, and masks the encoding bits. Invert and add one within the intended width. Restore the original value, or establish a consistent new allocation before re-enabling decoding. Clearing BME does not remove earlier outstanding transactions; their absence is a separate assumption here.</p>
<div class="table-wrap"><table><caption>Teaching probe and allocation results</caption><thead><tr><th scope="col">Resource</th><th scope="col">Readback after all-one writes</th><th scope="col">Size and allocation</th></tr></thead><tbody><tr><td>BAR0, 0x10</td><td>0xFFFFC000</td><td>32-bit non-Prefetchable; 16 KiB at 0x80004000–0x80007FFF.</td></tr><tr><td>BAR2/BAR3, 0x18/0x1C</td><td>0xFFE0000C/0xFFFFFFFF</td><td>64-bit Prefetchable; 2 MiB at 0x120000000–0x1201FFFFF.</td></tr></tbody></table></div>
<pre><code>BAR0 mask = 0xFFFFC000 &amp; 0xFFFFFFF0
size = ((~mask) &amp; 0xFFFFFFFF) + 1 = 0x4000

BAR2/3 mask = (0xFFFFFFFF &lt;&lt; 32) | (0xFFE0000C &amp; 0xFFFFFFF0)
size = ((~mask) &amp; 0xFFFFFFFFFFFFFFFF) + 1 = 0x200000</code></pre>
<p>BAR3 is BAR2's upper DWORD, not a separate I/O BAR despite reading all ones. The assigned values are 0x80004000 for BAR0 and 0x2000000C/0x00000001 for BAR2/3. An initial zero BAR does not prove absence; use the valid unimplemented result from the correct probe, and do not misinterpret an all-zero mask as a 4 GiB request.</p>
<p>Assume BAR0+0x120 is a valid device Register, yielding PCI address 0x80004120. The example separately assumes identical CPU/PCI mapping, so the CPU uses that same number. This is not a platform-wide guarantee. The Register and the available resource addresses are also teaching assumptions.</p>
<details class="source-note"><summary>Sources and limits</summary><p>Base 6.0 §7.5.1.2.1, pp.928–930, including the 32/64-bit sizing explanation on p.930. Firmware 3.3 §3.1.1 (p.32) permits non-identity MMIO mapping. Every allocation also needs platform resources, alignment, non-overlap, and address-width checks.</p></details></section>
<section id="window"><h2>Every Bridge Window on the path must contain the target</h2>
<p>The path to 03:00.0 passes through Root Port 00:01.0, Switch Upstream Port 01:00.0, and Downstream A 02:01.0. All three support and use the following windows in the example. The platform reserves the ranges, with no competing sibling allocation.</p>
<div class="table-wrap"><table><caption>Shared teaching configuration for the three Bridges</caption><thead><tr><th scope="col">Fields</th><th scope="col">Values</th><th scope="col">Decoded inclusive range</th></tr></thead><tbody><tr><td>Memory Base/Limit at 0x20/0x22, 16 bits each</td><td>0x8000/0x8000</td><td>0x80000000–0x800FFFFF</td></tr><tr><td>Prefetchable Base/Limit at 0x24/0x26, 16 bits each; Upper at 0x28/0x2C, 32 bits each</td><td>0x2001/0x2011; both Upper values are 1</td><td>0x120000000–0x1201FFFFF</td></tr></tbody></table></div>
<p>The Base's omitted lower 20 address bits become zero, while the Limit's become one, creating inclusive ranges with 1 MiB granularity. A low nibble of one in the Prefetchable fields indicates 64-bit support, with Upper fields supplying address bits 63:32. A window may exceed a BAR's size, but its gaps need not contain valid Registers. Bus Number ranges do not replace Memory Windows.</p>
<details class="source-note"><summary>Sources</summary><p>Figure 7-14, p.936; §7.5.1.3.8–§7.5.1.3.10, pp.940–941. The full tutorial derives the masks, shifts, and range containment.</p></details></section>
<section id="control"><h2>MSE and BME control different behavior</h2>
<p>Command is a 16-bit Register at 0x04. Bit 0 controls I/O Space, bit 1 MSE controls received Memory accesses, and bit 2 BME controls Function-originated Memory/I/O Requests. A Type 1 Port's BME also controls forwarding those Requests upstream, without blocking Completions.</p>
<p>With resources, windows, platform mapping, and the device interface ready, Command=0x0002 on the Endpoint and all three Bridges permits the example's CPU MMIO read while prohibiting Endpoint-originated DMA Memory Requests. BME does not block the read's Completion. BME=0 also prohibits MSI/MSI-X because they use in-band Memory Writes.</p>
<p>Changing the Endpoint to 0x0006 adds permission to originate the relevant Requests, but does not prepare buffers, device work, platform translation, or upstream Port BME. Do not update Command by blindly writing back a DWORD that includes Status at 0x06, since Status contains RW1C bits.</p>
<details class="source-note"><summary>Control sources</summary><p>Base 6.0 §7.5.1.1.3, Figure 7-5/Table 7-4, pp.917–920; BME, Completion, and MSI behavior on p.919. Command/Status layout: Figure 7-4, p.916; Status RW1C: Table 7-5, pp.922–923.</p></details></section>
<section id="checks"><h2>Keep allocation and handoff conclusions separate</h2>
<p>Firmware 3.3 §3.5 (pp.34–35) uses I/O/Memory Enable and ROM Enable to determine corresponding resource configuration, not BME to establish BAR validity. Enabled resources must be correctly configured by firmware, but drivers still prepare device-specific work.</p>
<details class="question"><summary>Can the 16 KiB BAR move to 0x80005000?</summary><p>No. Its lower 14 bits are not all zero, violating natural alignment. The example's 0x80004000 base meets the requirement. (§7.5.1.2.1, p.930.)</p></details>
<details class="question"><summary>Do correct windows permit a successful MMIO read when Endpoint MSE is clear?</summary><p>Success cannot be expected. With MSE clear, the Endpoint handles received Memory Space accesses as UR. A forwarding path does not replace target enablement. (Table 7-4, p.918.)</p></details></section>
<p>Chapter 5 will continue with Requests and Completions; later chapters remain planned.</p>
</article>
<nav class="bottom-nav" aria-label="Course and editions"><a href="/DOCS/pcie-course/index.html">Course overview</a><a href="/DOCS/pcie-course/chapter-4.html">Full Chinese tutorial</a><a href="/pcie/chapter-4-zh-tw/">繁體中文</a></nav>
</div>
