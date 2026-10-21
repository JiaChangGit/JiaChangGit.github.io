---
layout: post
title: "PCIe Chapter 10: Device and Link Power Management"
date: 2026-10-21 00:00:00 +0800
permalink: /pcie/chapter-10-en/
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
<nav class="bottom-nav" aria-label="Course and editions"><a href="/DOCS/pcie-course/index.html">Course overview</a><a href="/DOCS/pcie-course/chapter-10.html">Full Chinese tutorial</a><a href="/pcie/chapter-10-zh-tw/">繁體中文</a></nav>
<article class="lesson">
<p class="lead">PCIe power management spans Functions, Links, and the platform. D-states, ASPM, L1 Substates, and wake each have distinct controls and evidence; an Enable bit alone does not establish current state. PMCSR and L1.2 examples connect discovery, configuration, and recovery.</p>
<p><a href="/DOCS/pcie-course/chapter-10.html">Full Chinese tutorial</a> · <a href="/pcie/chapter-10-zh-tw/">繁體中文</a> · <a href="/DOCS/pcie-course/index.html">Course roadmap</a></p>
<aside class="note"><strong>Versions and assumptions</strong><p>PCIe follows Base 6.0; platform background uses ACPI 6.6. All numeric examples are authored. PMCSR concerns ordinary Endpoint 03:00.0. The separate L1.2 Link has the necessary capabilities at both ends, LTR, CLKREQ#, and suitable timing design. Neither example includes SR-IOV or adds undeclared features to earlier examples.</p></aside>
<section id="states"><h2>Function D-states and Link L-states are separate</h2><p>D0 is the normal Function state, but ASPM can save Link power during idle periods in D0. D1/D2 are optional. D3hot retains main power; D3cold lacks main power but may retain auxiliary power for wake. D0uninitialized after reset does not establish readiness of the work interface.</p><p>L0 supports transmission. L0s can operate independently by direction, but is unsupported in Flit Mode, with Retimers, or under specified independent-SSC clock conditions. L0p is Flit-only and idles some Lanes while retaining at least one active Lane in each direction. L1 can have L1.0/L1.1/L1.2 substates. L2/L3 follow main-power removal and differ by the presence of Vaux.</p><details class="source-note"><summary>State sources</summary><p>§5.2–§5.3.1, Tables 5-1/5-2 (pp.600–609); L0s/L0p: §4.2.6.6–§4.2.6.7 (p.445).</p></details></section>
<section id="pmcsr"><h2>Read PM capabilities, then construct the D0 write correctly</h2><p>Conventional Capability ID=0x01 identifies PM. An authored full-DWORD read at 0x40 returns 0xC8035001: ID=0x01, Next=0x50, Version=3, no D1/D2 support. PME_Support=<code>(value &gt;&gt; 27) &amp; 0x1F = 0x19</code> allows PME from D0, D3hot, and D3cold. Assume no optional Data Register, Aux_Current=0 using self-power, and necessary power availability. This is capability evidence, not proof of a complete wake path.</p><div class="table-wrap"><table><caption>16-bit operations on PMCSR at 0x44</caption><thead><tr><th scope="col">Action</th><th scope="col">Value</th><th scope="col">Meaning</th></tr></thead><tbody><tr><td>Read</td><td>0x810B</td><td>D3hot, No_Soft_Reset=1, PME_En=1, PME_Status=1.</td></tr><tr><td>Write D0</td><td>0x0108</td><td>Clear PowerState; write zero to RW1CS PME_Status to preserve the event.</td></tr><tr><td>Read after waiting</td><td>0x8108</td><td>D0 with the event retained.</td></tr><tr><td>Explicitly clear after servicing</td><td>0x8108</td><td>Intentionally write 1 to PME_Status; absent a new event, readback is 0x0108.</td></tr></tbody></table></div><p>Assume no concurrent changes or new events. No_Soft_Reset=1 preserves internal state for the specified software D3hot-to-D0 transition, returning to D0active; it does not remove recovery delays. Immediate Readiness=0 and no other timing exception require at least 10 ms before further access, including Configuration. No_Soft_Reset=0 requires full reinitialization and does not guarantee old state was cleared. D3cold, Fundamental Reset, and DL_Down from L2/L3 Ready do not inherit this preservation guarantee.</p><p>PowerState has no D3cold encoding. Unsupported D1/D2 writes complete normally without changing state. PME_Status can record a qualifying event even with PME_En=0. Entering D3hot still requires handling outstanding transactions and state preservation.</p><details class="source-note"><summary>Capabilities, write semantics, and delays</summary><p>Figures 7-17–7-19, Tables 7-14/7-15 (pp.944–949); §5.3.1.4 (pp.606–608); Figure 5-18/Table 5-14 (pp.654–655). Figure 7-18 numbers bits across the full DWORD including the Header; do not apply those bit numbers to a 16-bit read at +0x02.</p></details></section>
<section id="aspm"><h2>ASPM enablement needs capabilities and a latency policy</h2><p>ASPM manages an idle Link in D0; PCI-PM uses software-directed D-state changes. An ordinary non-ARI multifunction device must have all Functions outside D0 before initiating L1 on behalf of PCI-PM.</p><p>Inspect both Link Capabilities ASPM Support fields, then Link Control ASPM Control. Enablement does not report current L1 residency. Compare Link Capabilities L1 Exit Latency with Endpoint Device Capabilities L1 Acceptable Latency across the path. Exits can overlap across Links, so adding every Port's latency is incorrect; Figure 5-8's example finishes at T+34 μs.</p><details class="source-note"><summary>ASPM sources</summary><p>§5.3.2 (pp.609–610), §5.4.1/Figure 5-8 (pp.621–640); Tables 7-20, 7-23, 7-24 (pp.956–957, 967–972).</p></details></section>
<section id="substates"><h2>Configure L1.2 using both ends and the required order</h2><div class="table-wrap"><table><caption>Separate L1.2 configuration snapshot</caption><thead><tr><th scope="col">Location</th><th scope="col">Downstream Port</th><th scope="col">Upstream Port</th></tr></thead><tbody><tr><td>Header, 0x200</td><td>0x0001001E</td><td>0x0001001E</td></tr><tr><td>Capabilities, 0x204</td><td>0x00280A1F</td><td>0x0051141F</td></tr><tr><td>Control 1, 0x208</td><td>0x40801404</td><td>0x40800004</td></tr><tr><td>Control 2, 0x20C</td><td>0x00000051</td><td>0x00000051</td></tr></tbody></table></div><p>Separate list traversal happens to locate ID=0x001E, Version=1, Next=0 at 0x200 on both ends. Version 1 lacks the +0x10 Status Register. Both low-five capability fields are 0x1F, indicating all four Substate capabilities and overall support. Advertised T_POWER_ON is 10/100 μs, and common-mode restoration is 10/20 μs. Configured Control 2 Value=10, Scale=1 gives 100 μs. Control 1 enables only ASPM L1.2 at bit 2. Common_Mode_Restore_Time is set to 20 μs on the Downstream Port and is RsvdP on the Upstream Port.</p><p>The platform has validated these settings for the connection; taking the larger advertised values is not asserted as a universal algorithm. Both ends must support the selected Substate. Configure ASPM Substates while ASPM L1 is disabled, and PCI-PM Substates while in D0. Program applicable timing and identical LTR thresholds first, then enable corresponding bits on the Downstream Port before the Upstream Port. Disable in the reverse order. Clear applicable L1.2 Enables before changing timing fields; restore ASPM L1 under policy afterward.</p><details class="source-note"><summary>L1 Substates lookup and configuration</summary><p>Figures 7-146–7-150/Tables 7-129–7-132 (pp.1103–1108); §5.5, §5.5.4–§5.5.5/Table 5-11 (pp.640, 650–651). L1.1 retains common mode; L1.2 need not. Both use CLKREQ#, and ASPM L1.2 requires LTR.</p></details></section>
<section id="ltr"><h2>The same Enable can produce different entry decisions</h2><p>Control 1 threshold Value=128, Scale=2 gives 128 × 1024 ns=131072 ns (131.072 μs). Assume ASPM L1.0, deasserted CLKREQ#, and all other entry conditions satisfied. Latest valid snoop/no-snoop LTR requirements of 204800/102400 ns fail because no-snoop is below threshold. Changing them to 204800/153600 ns satisfies both, requiring entry under these assumptions.</p><p>No requirement for a traffic class is a separate branch, not Requirement=1 with Value=0; the latter requests the best possible service. These are latest valid reports, not Max Latency Register limits. LTR is also not a hard Root Complex latency guarantee. L1.1 is not enabled here, so it is not an assumed fallback. Before enabling Endpoint LTR, the Root Complex and intervening Switches must support it, with devices closest to the Root Port enabled first.</p><details class="source-note"><summary>LTR and entry conditions</summary><p>§5.5.1 (p.644); Figure 6-15, §6.18 (pp.781–782); Table 7-131 (pp.1107–1108).</p></details></section>
<section id="wake"><h2>Wake restores communication before identifying the source</h2><p>L2 cannot carry ordinary TLPs. The device uses form-factor-appropriate WAKE# or Beacon to request power, clock, and Link restoration, then sends PM_PME with its Requester ID. PME_En, auxiliary power, and platform routing must cooperate. (§5.3.3.1–§5.3.3.2, pp.615–616.)</p><p>Platform background: <a href="https://uefi.org/sites/default/files/resources/ACPI_Spec_6.6.pdf#page=568">ACPI 6.6 §7.3.8–§7.3.11</a> describes D0/D3hot power dependencies through _PR0/_PR3, not PCIe Registers. Document pp.497–498 correspond to PDF pp.568–569.</p></section>
<section id="questions"><h2>Check whether the conditions are sufficient</h2><details class="question"><summary>Does No_Soft_Reset=1 preserve all state through D3cold?</summary><p>No. It applies to the specified software D3hot-to-D0 transition.</p></details><details class="question"><summary>Can only the Endpoint enable L1.2 when its partner lacks support?</summary><p>No. Both capabilities, configuration order, LTR, and timing conditions must hold.</p></details></section>
</article>
<nav class="bottom-nav" aria-label="Course and editions"><a href="/DOCS/pcie-course/index.html">Course overview</a><a href="/DOCS/pcie-course/chapter-10.html">Full Chinese tutorial</a><a href="/pcie/chapter-10-zh-tw/">繁體中文</a></nav>
</div>
