---
layout: post
title: "PCIe Chapter 2: Reading Configuration Space and Finding Capabilities"
date: 2026-10-20 00:00:00 +0800
last_modified_at: 2026-10-28 00:00:00 +0800
permalink: /pcie/chapter-2-en/
categories: [PCIe]
tags: [PCIe, Specification]
lang: en
spec_teaching: true
spec_series: pcie
description: "從 Header Layout 選對欄位圖，沿 Capability 清單查詢裝置序號，再用混合屬性案例學習組成寫值。"
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

/* Applied only to explicitly authorized teaching roots. */
html .spec-teaching[data-spec-series] .st-terms { margin:.35rem 0 1rem; padding:.5rem .8rem; border-inline-start:3px solid var(--st-accent); background:var(--st-soft); font-size:.88em; color:var(--st-muted); }
html .spec-teaching[data-spec-series] .st-terms > div { display:flex; flex-wrap:wrap; gap:.2em .7em; }
html .spec-teaching[data-spec-series] .st-terms dt { font-weight:650; }
html .spec-teaching[data-spec-series] .st-terms dd { margin:0; flex:1 1 14em; }
html .spec-teaching[data-spec-series] {
 --st-diagram-width:900px;
 --st-paper:#f2f6f8; --st-surface:#fff; --st-ink:#192d40; --st-muted:#4c6479;
 --st-line:#cbd9e3; --st-accent:#145f9d; --st-soft:#edf5fc;
 --paper:var(--st-paper); --surface:var(--st-surface); --surface-2:var(--st-soft); --surface-alt:var(--st-soft);
 --ink:var(--st-ink); --muted:var(--st-muted); --line:var(--st-line);
 --accent:var(--st-accent); --accent-2:var(--st-accent); --soft:var(--st-soft); --blue-soft:var(--st-soft); --teal-soft:var(--st-soft);
 --qr-paper:var(--st-paper); --qr-surface:var(--st-surface); --qr-ink:var(--st-ink); --qr-muted:var(--st-muted);
 --qr-line:var(--st-line); --qr-accent:var(--st-accent); --qr-soft:var(--st-soft);
 color:var(--st-ink); background:var(--st-paper); font-size:17px; line-height:1.9;
 font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","Noto Sans TC","PingFang TC","Microsoft JhengHei",sans-serif;
}
html .spec-teaching[data-spec-series="nvme"] { --st-accent:#086b56; --st-soft:#e7f4ee; }
@media(prefers-color-scheme:dark) {
 html:not([data-theme="light"]) .spec-teaching { --st-paper:#101b26; --st-surface:#172635; --st-ink:#e5eef5; --st-muted:#b7c8d6; --st-line:#40566a; --st-accent:#81bdf0; --st-soft:#1b354b; }
 html:not([data-theme="light"]) .spec-teaching[data-spec-series="nvme"] { --st-accent:#79d8b4; --st-soft:#173d32; }
}
html[data-theme="dark"] .spec-teaching { --st-paper:#101b26; --st-surface:#172635; --st-ink:#e5eef5; --st-muted:#b7c8d6; --st-line:#40566a; --st-accent:#81bdf0; --st-soft:#1b354b; }
html[data-theme="dark"] .spec-teaching[data-spec-series="nvme"] { --st-accent:#79d8b4; --st-soft:#173d32; }
.spec-teaching * { box-sizing:border-box; }
.spec-teaching :is(h1,h2,h3,h4,h5,p,li,td,th,summary,strong,figcaption) { color:var(--st-ink); }
.spec-teaching svg text { font-family:inherit; }
.spec-teaching h1 { font-size:clamp(1.8rem,3.2vw,2.65rem); line-height:1.4; }
.spec-teaching h2 { font-size:clamp(1.3rem,2.5vw,1.7rem); line-height:1.55; }
.spec-teaching h3 { font-size:1.15rem; line-height:1.65; }
.spec-teaching h4 { font-size:1rem; line-height:1.7; }
.spec-teaching :is(h1,h2,h3,h4) { overflow-wrap:anywhere; }
.spec-teaching p { margin:.7rem 0 1.15rem; }
.spec-teaching :is(a,summary) { text-underline-offset:.2em; }
.spec-teaching :focus-visible { outline:3px solid var(--st-accent); outline-offset:4px; }
.spec-teaching :is(.qa-takeaway,.qa-answer-lead,.st-takeaway) { color:var(--st-ink); font-weight:650; font-size:1.06rem; line-height:1.9; }
.spec-teaching :is(.qa-question,.qr-card,.guided-walk) { border:1px solid var(--st-line); border-radius:12px; background:var(--st-surface); padding:clamp(18px,3vw,30px); margin:1.8rem 0; }
.spec-teaching :is(.qa-flow,.qr-note,.qr-observations,.st-context,.st-route) { background:var(--st-soft); border-left:4px solid var(--st-accent); padding:1rem 1.2rem; margin:1.4rem 0; }
.spec-teaching :is(.qr-step,.qa-qid,.st-label) { color:var(--st-accent); font-weight:700; }
.spec-teaching :is(.qa-citations,.qa-source-links,.qr-case-sources,.walk-source,.st-source) { font-size:.84rem; line-height:1.75; color:var(--st-muted); overflow-wrap:anywhere; }
.spec-teaching :is(.qr-table,.table-wrap) { overflow-x:auto; margin:1.4rem 0; border-radius:7px; }
.spec-teaching :is(th,td) { line-height:1.8; vertical-align:top; min-width:120px; }
.spec-teaching :is(table,td) { background:var(--st-surface); }
.spec-teaching th { background:var(--st-soft); }
.spec-teaching .st-step { border-left:3px solid var(--st-line); padding:.6rem 1rem; margin:1.2rem 0; }
.spec-teaching .st-step:target { border-left-color:var(--st-accent); background:var(--st-soft); }
.spec-teaching .st-glossary { border:1px solid var(--st-line); padding:.7rem 1rem; margin:1.4rem 0; border-radius:8px; }
.spec-teaching .st-glossary > summary { min-height:44px; cursor:pointer; }
.spec-teaching .st-specs { display:flex; flex-wrap:wrap; gap:.4rem 1rem; color:var(--st-muted); font-size:.8rem; line-height:1.8; margin:1rem 0; }
.spec-teaching .st-specs span { border-bottom:2px solid var(--st-accent); padding:.2rem 0; }
@media(max-width:620px) { .spec-teaching :is(.qa-question,.qr-card,.guided-walk) { padding:16px; } .spec-teaching .diagram svg { min-width:var(--st-diagram-width); } }
@media print {
 .spec-teaching { --st-paper:#fff!important; --st-surface:#fff!important; --st-ink:#000!important; --st-muted:#333!important; --st-line:#999!important; --st-accent:#000!important; --st-soft:#fff!important; }
 .spec-teaching details > * { display:block!important; }
 .spec-teaching details::details-content { content-visibility:visible!important; }
 .spec-teaching .st-step { break-inside:avoid; }
}

/* Native reading guides: selection highlights; it never hides teaching content.
   build_pcie_course.py changes .pcie-article to .pcie-article for the posts. */
.pcie-article .guided-walk { margin: 1.8rem 0; padding: 1.2rem; border: 1px solid var(--line); border-radius: 12px; background: var(--surface); min-width: 0; }
.pcie-article .guided-walk > h3 { margin-top: 0; }
.pcie-article .walk-help { color: var(--muted); font-size: .85rem; }
.pcie-article .walk-order { margin-bottom: 1.1rem; }
/* Keep native radio semantics and keyboard handling; the associated label is
   the visible control, so a radio cannot wrap away from its own label. */
.pcie-article .walk-choice { position: absolute; width: 1px; height: 1px; margin: -1px; padding: 0; border: 0; overflow: hidden; clip-path: inset(50%); white-space: nowrap; }
.pcie-article .walk-label { display: inline-flex; align-items: center; min-height: 44px; padding: .35rem .7rem; margin: .25rem .8rem .25rem 0; border: 2px solid var(--line); border-radius: 8px; cursor: pointer; font-size: .9rem; line-height: 1.5; color: var(--ink); background: var(--surface-alt); }
.pcie-article .walk-choice:checked + .walk-label { border-color: var(--accent); background: var(--blue-soft); font-weight: 700; }
.pcie-article .walk-choice:focus-visible + .walk-label { outline: 3px solid var(--focus); outline-offset: 3px; }
.pcie-article .walk-view { margin-top: 1rem; min-width: 0; }
.pcie-article .walk-diagram { margin: 0 0 1.2rem; }
.pcie-article .walk-diagram svg { width: 100%; height: auto; display: block; }
.pcie-article .walk-diagram svg a { cursor: pointer; }
.pcie-article .walk-diagram svg a:focus-visible { outline: 3px solid var(--focus); outline-offset: 4px; }
.pcie-article .walk-diagram figcaption { margin-top: .8rem; }
.pcie-article .walk-steps { max-width: none; padding-left: 1.6rem; }
.pcie-article .walk-step { padding: .6rem .9rem; margin: .7rem 0; border: 2px solid transparent; border-left: 5px solid var(--line); border-radius: 5px; background: var(--surface); }
.pcie-article .walk-step h4 { margin: .2rem 0 .5rem; }
.pcie-article .walk-condition { font-size: .9rem; color: var(--muted); }
.pcie-article .walk-source { border-top: 1px solid var(--line); padding-top: .35rem; color: var(--muted); font-size: .85rem; }
.pcie-article .walk-step p:last-child { margin-bottom: .3rem; }
.pcie-article .walk-components { border-top: 1px solid var(--line); margin-top: 1.4rem; padding-top: .4rem; }
.pcie-article .walk-component-links { display: flex; flex-wrap: wrap; gap: .4rem 1.2rem; list-style: none; padding-left: 0; }
.pcie-article .walk-component-links a { min-height: 44px; min-width: 44px; }
.pcie-article .walk-component { padding: .7rem 1rem; margin: 1rem 0; border: 1px solid var(--line); border-radius: 8px; }
.pcie-article .walk-component > h4 { margin-top: .2rem; }
.pcie-article .walk-component:target { outline: 3px solid var(--accent-2); outline-offset: 3px; }
.pcie-article .walk-component details { margin-bottom: .3rem; }

.pcie-article .walk-choice[data-walk-step="1"]:checked ~ .walk-view .walk-step[data-walk-step="1"],
.pcie-article .walk-choice[data-walk-step="2"]:checked ~ .walk-view .walk-step[data-walk-step="2"],
.pcie-article .walk-choice[data-walk-step="3"]:checked ~ .walk-view .walk-step[data-walk-step="3"],
.pcie-article .walk-choice[data-walk-step="4"]:checked ~ .walk-view .walk-step[data-walk-step="4"],
.pcie-article .walk-choice[data-walk-step="5"]:checked ~ .walk-view .walk-step[data-walk-step="5"],
.pcie-article .walk-choice[data-walk-step="6"]:checked ~ .walk-view .walk-step[data-walk-step="6"],
.pcie-article .walk-choice[data-walk-step="7"]:checked ~ .walk-view .walk-step[data-walk-step="7"],
.pcie-article .walk-choice[data-walk-step="8"]:checked ~ .walk-view .walk-step[data-walk-step="8"] { border-color: var(--accent); background: var(--blue-soft); }

.pcie-article .walk-choice[data-walk-step="1"]:checked ~ .walk-view .walk-node[data-walk-steps~="1"],
.pcie-article .walk-choice[data-walk-step="2"]:checked ~ .walk-view .walk-node[data-walk-steps~="2"],
.pcie-article .walk-choice[data-walk-step="3"]:checked ~ .walk-view .walk-node[data-walk-steps~="3"],
.pcie-article .walk-choice[data-walk-step="4"]:checked ~ .walk-view .walk-node[data-walk-steps~="4"],
.pcie-article .walk-choice[data-walk-step="5"]:checked ~ .walk-view .walk-node[data-walk-steps~="5"],
.pcie-article .walk-choice[data-walk-step="6"]:checked ~ .walk-view .walk-node[data-walk-steps~="6"],
.pcie-article .walk-choice[data-walk-step="7"]:checked ~ .walk-view .walk-node[data-walk-steps~="7"],
.pcie-article .walk-choice[data-walk-step="8"]:checked ~ .walk-view .walk-node[data-walk-steps~="8"] { --walk-active-weight: 750; }
.pcie-article .walk-choice[data-walk-step="1"]:checked ~ .walk-view .walk-node[data-walk-steps~="1"] > :is(rect, circle, ellipse, polygon, path, line, polyline),
.pcie-article .walk-choice[data-walk-step="2"]:checked ~ .walk-view .walk-node[data-walk-steps~="2"] > :is(rect, circle, ellipse, polygon, path, line, polyline),
.pcie-article .walk-choice[data-walk-step="3"]:checked ~ .walk-view .walk-node[data-walk-steps~="3"] > :is(rect, circle, ellipse, polygon, path, line, polyline),
.pcie-article .walk-choice[data-walk-step="4"]:checked ~ .walk-view .walk-node[data-walk-steps~="4"] > :is(rect, circle, ellipse, polygon, path, line, polyline),
.pcie-article .walk-choice[data-walk-step="5"]:checked ~ .walk-view .walk-node[data-walk-steps~="5"] > :is(rect, circle, ellipse, polygon, path, line, polyline),
.pcie-article .walk-choice[data-walk-step="6"]:checked ~ .walk-view .walk-node[data-walk-steps~="6"] > :is(rect, circle, ellipse, polygon, path, line, polyline),
.pcie-article .walk-choice[data-walk-step="7"]:checked ~ .walk-view .walk-node[data-walk-steps~="7"] > :is(rect, circle, ellipse, polygon, path, line, polyline),
.pcie-article .walk-choice[data-walk-step="8"]:checked ~ .walk-view .walk-node[data-walk-steps~="8"] > :is(rect, circle, ellipse, polygon, path, line, polyline) { stroke: var(--accent); stroke-width: 3.5px; vector-effect: non-scaling-stroke; }
.pcie-article .walk-node text { font-weight: var(--walk-active-weight, inherit); }

@media (max-width: 620px) {
  .pcie-article .guided-walk { padding: .8rem; }
  .pcie-article .walk-label { margin-right: .45rem; padding-left: .45rem; padding-right: .45rem; }
  .pcie-article .walk-steps { padding-left: 1.15rem; }
  .pcie-article .walk-step { padding: .5rem .6rem; }
  .pcie-article .walk-diagram { overflow-x: auto; }
  .pcie-article .walk-diagram svg { min-width: var(--st-diagram-width, 700px); }
}
@media (forced-colors: active) {
  .pcie-article .walk-choice:checked + .walk-label { border-color: Highlight; }
  .pcie-article .walk-step { border-color: CanvasText; }
}
@media print {
  .pcie-article .guided-walk { border: 1px solid #999; padding: .7rem; break-inside: auto; }
  .pcie-article .walk-choice, .pcie-article .walk-label, .pcie-article .walk-help { display: none; }
  .pcie-article .walk-step { display: list-item !important; border-color: #999 !important; background: transparent !important; }
  .pcie-article .walk-node { --walk-active-weight: 500 !important; }
  .pcie-article .walk-node > :is(rect, circle, ellipse, polygon, path, line, polyline) { stroke: #333 !important; stroke-width: 1.5px !important; }
  .pcie-article .walk-diagram { overflow: visible; }
  .pcie-article .walk-diagram svg { min-width: 0; }
  .pcie-article .walk-component details > * { display: block !important; }
  .pcie-article .walk-component details::details-content { content-visibility: visible !important; }
}

/* SVG text follows the selected reading theme. */
.pcie-article svg text { fill: var(--ink); }
.pcie-article .walk-summary { margin: 1rem 0 1.5rem; }

html:not([data-theme="dark"]) .pcie-article { color-scheme: light; }
html[data-theme="dark"] .pcie-article { color-scheme: dark; }

.pcie-article { background: transparent; margin: 1.5rem 0; }
.pcie-article .lesson { padding: 0; border: 0; background: transparent; }
</style>
<div class="pcie-article spec-teaching" data-spec-series="pcie" lang="en">
<nav class="bottom-nav" aria-label="Course and editions"><a href="/DOCS/pcie-course/index.html">Course overview</a><a href="/DOCS/pcie-course/chapter-2.html">Full Chinese tutorial</a><a href="/pcie/chapter-2-zh-tw/">繁體中文</a></nav>
<article class="lesson">
<p class="lead">Starting from an already discovered Function, this chapter queries Device Serial Number (DSN). The feature selects the list; pointers locate its structure; register definitions then determine how to read and assemble the serial number.</p>
<p><strong>Simulated data:</strong> Locations and values are created for teaching and do not represent a particular device or platform.</p>
<figure class="diagram"><svg viewBox="0 0 840 580" class="course-diagram" role="img" aria-labelledby="ch2-dsn-en-svg-title ch2-dsn-en-svg-desc"><title id="ch2-dsn-en-svg-title">Two independent capability lists</title><desc id="ch2-dsn-en-svg-desc">The conventional list does not continue into the Extended list.</desc><g><rect x="270" y="20" width="300" height="80" rx="10" fill="var(--blue-soft)" stroke="var(--line)" stroke-width="2"/><text x="420" y="47" text-anchor="middle" fill="var(--ink)" font-size="18">Function 03:00.0</text><text x="420" y="72" text-anchor="middle" fill="var(--ink)" font-size="16">Configuration Space</text></g><g><rect x="20" y="180" width="350" height="80" rx="10" fill="var(--blue-soft)" stroke="var(--line)" stroke-width="2"/><text x="195" y="207" text-anchor="middle" fill="var(--ink)" font-size="18">Conventional list</text><text x="195" y="232" text-anchor="middle" fill="var(--ink)" font-size="16">0x34 → 0x40</text></g><g><rect x="470" y="180" width="350" height="80" rx="10" fill="var(--blue-soft)" stroke="var(--line)" stroke-width="2"/><text x="645" y="207" text-anchor="middle" fill="var(--ink)" font-size="18">Extended list</text><text x="645" y="232" text-anchor="middle" fill="var(--ink)" font-size="16">Start at 0x100</text></g><g><rect x="20" y="325" width="350" height="80" rx="10" fill="var(--blue-soft)" stroke="var(--line)" stroke-width="2"/><text x="195" y="352" text-anchor="middle" fill="var(--ink)" font-size="18">Null → PCIe → MSI-X</text><text x="195" y="377" text-anchor="middle" fill="var(--ink)" font-size="16">0x50 → 0x70 → 0xD0</text></g><g><rect x="470" y="325" width="350" height="80" rx="10" fill="var(--blue-soft)" stroke="var(--line)" stroke-width="2"/><text x="645" y="352" text-anchor="middle" fill="var(--ink)" font-size="18">AER → DSN</text><text x="645" y="377" text-anchor="middle" fill="var(--ink)" font-size="16">0x100 → 0x180</text></g><g><rect x="470" y="470" width="350" height="80" rx="10" fill="var(--blue-soft)" stroke="var(--line)" stroke-width="2"/><text x="645" y="497" text-anchor="middle" fill="var(--ink)" font-size="18">Read the serial number</text><text x="645" y="522" text-anchor="middle" fill="var(--ink)" font-size="16">base+0x04 / base+0x08</text></g><g><path d="M420 100 V140 H195 V180 M420 140 H645 V180" fill="none" stroke="var(--accent)" stroke-width="2.5"/><text x="420" y="130" text-anchor="middle" fill="var(--ink)" font-size="15">Choose the list for the feature</text></g><g><path d="M195 260 V325" fill="none" stroke="var(--accent)" stroke-width="2.5"/><text x="195" y="302" text-anchor="middle" fill="var(--ink)" font-size="15">Next: Function-relative</text></g><g><path d="M645 260 V325" fill="none" stroke="var(--accent)" stroke-width="2.5"/><text x="645" y="302" text-anchor="middle" fill="var(--ink)" font-size="15">Next=0x180</text></g><g><path d="M645 405 V470" fill="none" stroke="var(--accent)" stroke-width="2.5"/><text x="645" y="448" text-anchor="middle" fill="var(--ink)" font-size="15">ID=0003h; Version=1</text></g></svg><figcaption>An authored query map. The two lists have independent entry points. Next is Function-relative; data offsets are relative to the located DSN structure. Base 6.0 Figures 7-42/7-43/7-241, printed/PDF pp.1009–1010 and 1205.</figcaption></figure><dl class="st-terms" aria-label="Terms in this passage"><div><dt>MSI-X</dt><dd>Message Signaled Interrupts Extension</dd></div><div><dt>AER</dt><dd>Advanced Error Reporting</dd></div></dl>

<p><a href="/DOCS/pcie-course/chapter-2.html">Full Chinese tutorial</a> · <a href="/DOCS/pcie-course/index.html">Course roadmap</a> · <a href="/pcie/chapter-2-zh-tw/">繁體中文</a></p>
<aside class="note"><strong>Version and assumptions</strong><p>Definitions follow PCI Express Base Specification Revision 6.0. Addresses and values are author-created, not measurements. The target is an already discovered ordinary Type 0 PCI Express Endpoint, not an RCiEP or VF; ARI, SR-IOV, and RCRB lists are excluded. Reads succeed, the snapshot is stable, and the platform can access the full Configuration Space. The example does not support Flit Mode, allowing its AER (Advanced Error Reporting) Header to use Version 2. Printed and PDF page numbers coincide.</p><dl class="st-terms" aria-label="Terms in this passage"><div><dt>VF</dt><dd>Virtual Function</dd></div><div><dt>ARI</dt><dd>Alternative Routing-ID Interpretation</dd></div><div><dt>SR-IOV</dt><dd>Single Root I/O Virtualization</dd></div></dl></aside>
<section id="space"><h2>Separate the target, configuration offset, and CPU address</h2>
<p>Segment and BDF (Bus, Device, and Function identifier) select the Function. A byte offset then selects a Register in its 4096-byte Configuration Space: the first 256 bytes are PCI-compatible, and 0x100–0xFFF is the extended region. ECAM (Enhanced Configuration Access Mechanism) provides CPU memory-mapped configuration access. The platform supplies its physical mapping; the offset alone is only a position within the selected Function.</p><dl class="st-terms" aria-label="Terms in this passage"><div><dt>BDF</dt><dd>Bus/Device/Function</dd></div></dl>
<p>The conventional Capability list starts through the Header's Capabilities Pointer, at 0x34 for the Type 0/1 layouts used here. The Extended list starts independently at 0x100. The PCI Express Capability belongs to the conventional list; DSN belongs to the Extended list. A name containing PCIe does not establish which list to use.</p>
<details class="source-note"><summary>Reading locations</summary><p>Base 6.0 §7.2–§7.2.2.2, Figure 7-3 and Table 7-1, pp.905–909; Figure 7-4, p.916; Capabilities Pointer: §7.5.1.1.11, p.926; Extended list: §7.6–§7.6.3, Figures 7-42/7-43 and Table 7-39, pp.1008–1010.</p></details></section>
<section id="header-layout"><h2>Why can the same offset mean different things?</h2>
<p>First read the selected Function’s Header Type Register at <code>0x0E</code>. Bits 6:0 select the Header Layout: Figure 7-10 shows Type 0, and Figure 7-14 shows Type 1 for Root and Switch Ports. Read the bit positions across each figure and the Function-relative byte offset at the right.</p>
<div class="table-wrap"><table><caption>The same byte offsets in the two Header layouts</caption><thead><tr><th scope="col">Offset</th><th scope="col">Type 0</th><th scope="col">Type 1 (Root/Switch Port)</th></tr></thead><tbody><tr><td>0x10–0x14</td><td>Part of the Base Address Register (BAR) area</td><td>This Port’s BAR 0 and BAR 1</td></tr><tr><td>0x18</td><td>Part of the BAR area</td><td>Primary, Secondary and Subordinate Bus Number fields, among others</td></tr><tr><td>0x20</td><td>Part of the BAR area</td><td>Memory Base and Memory Limit</td></tr></tbody></table></div>
<p>For a 32-bit value at <code>0x18</code>, first obtain the Header Layout of that same Function. With Type 1, interpret the corresponding bytes as Bus Numbers; with Type 0, the location belongs to the BAR area. Read the particular BAR type and field definition before interpreting it. The Bus Numbers describe the downstream discovery range; Memory Base and Limit describe a resource window. <a href="/DOCS/pcie-course/chapter-3.html">Chapter 3</a> explains discovery and <a href="/DOCS/pcie-course/chapter-4.html">Chapter 4</a> resource allocation.</p>
<p>Read bit 7 separately from bits 6:0. The assumed value <code>0x80</code> selects Type 0 and indicates that the Device <em>may</em> contain multiple Functions; further probing is needed. VF rules differ and are outside this example. Header Layout and Configuration Request Type 0/1 are separately defined classifications.</p><dl class="st-terms" aria-label="Terms in this passage"><div><dt>VF</dt><dd>Virtual Function</dd></div></dl>
<p class="term-note">Reading route: Base 6.0 §7.5.1.1.9, Figure 7-8 and Table 7-7 (printed/PDF pp.924–925); Figure 7-10 (p.928); Figure 7-14 and its applicability note (p.936). Select the figure from Header Type, then read its offset and field definition.</p></section>

<section id="lists"><h2>An ID of zero is different from a Next pointer of zero</h2>
<p>A conventional Capability normally starts with an ID in the low byte and a Next pointer in the high byte of a 16-bit read. The teaching list follows <code>0x40 → 0x50 → 0x70 → 0xD0 → 0</code>, representing PM, Null, PCIe, and MSI-X.</p><dl class="st-terms" aria-label="Terms in this passage"><div><dt>MSI-X</dt><dd>Message Signaled Interrupts Extension</dd></div></dl>
<div class="table-wrap"><table><caption>Representative reads; locations are byte offsets within the Function</caption><thead><tr><th scope="col">Location and width</th><th scope="col">Value</th><th scope="col">Interpretation</th></tr></thead><tbody><tr><td>0x50, 16 bits</td><td>0x7000</td><td>Conventional ID 00h is Null; Next=0x70, so traversal continues.</td></tr><tr><td>0x100, 32 bits</td><td>0x18020001</td><td>Extended ID 0001h, AER Version 2; Next=0x180.</td></tr><tr><td>0x180, 32 bits</td><td>0x00010003</td><td>Extended ID 0003h, DSN Version 1; Next=0 ends the list.</td></tr></tbody></table></div>
<pre><code>Extended ID = header &amp; 0xFFFF
Version     = (header &gt;&gt; 16) &amp; 0xF
Next        = (header &gt;&gt; 20) &amp; 0xFFC</code></pre>
<p>Next already gives a byte offset from the beginning of the Function. Read at that offset directly; DWORD alignment does not change its unit. For an unknown ID, follow a valid Header to the next entry. The course separately checks range, alignment, and revisited offsets to detect unreliable traversal; valid positions need not increase.</p>
<details class="source-note"><summary>ID and list sources</summary><p>PM: Figure 7-18/Table 7-14, p.945; PCIe: Figure 7-22/Table 7-18, p.953; MSI-X: Figure 7-59/Table 7-48, pp.1021–1022; Null: §7.9.27, Figure 7-384/Table 7-336, p.1315. Extended Header: Table 7-39, p.1010; AER (Advanced Error Reporting): Figure 7-154/Table 7-134, p.1112. Flit Mode support requires AER Version 3 and is excluded here.</p></details></section>
<section id="dsn"><h2>After finding DSN, distinguish data location from display order</h2>
<p>Figure 7-242/Table 7-221 identify DSN as ID 0003h. Figure 7-241 then places its Lower DW and Upper DW at structure offsets +0x04 and +0x08. The example reads 0x33221100 at 0x184 and 0x77665544 at 0x188, each as 32 bits.</p><dl class="st-terms" aria-label="Terms in this passage"><div><dt>DW</dt><dd>Double Word, a four-byte unit</dd></div></dl>
<pre><code>Register integer = (0x77665544 &lt;&lt; 32) | 0x33221100
                 = 0x7766554433221100</code></pre>
<p>Table 7-222 separately maps Register bytes to EUI-64 bytes. Written from the highest EUI byte to the lowest, the example is <code>00-11-22-33-44-55-66-77</code>. These values illustrate reconstruction, not an allocated or usable product identifier. Real values must follow the IEEE company identifier and manufacturer extension rules, and the value alone does not authenticate hardware.</p>
<p>DSN is optional. An ordinary Multi-Function Device implementing DSN must implement it in Function 0; other Functions implementing it must return the same value. DSN therefore does not replace the Function Number in BDF (Bus, Device, and Function identifier).</p><dl class="st-terms" aria-label="Terms in this passage"><div><dt>BDF</dt><dd>Bus/Device/Function</dd></div></dl>
<details class="source-note"><summary>Exact DSN references</summary><p>Base 6.0 §7.9.3–§7.9.3.2, Figures 7-241–7-243 and Tables 7-221/7-222, pp.1205–1207. RCiEP and PF/VF conditions differ and are excluded here.</p></details></section>
<section id="meaning"><h2>A read value is not automatically safe to write back</h2>
<p>Read the Attributes column with the field definition. RO restricts software writes; RW1C (write one to clear) leaves status unchanged when written as zero.</p>
<aside class="example"><strong>Simulated data: writing mixed attributes</strong><p>This hypothetical 8-bit layout illustrates how to construct a value; it is not an actual Register or a prescribed access width. Assume no intervening hardware or software update. The read value is <code>0000 1101b</code> (0x0D). Set RW bit 1 while preserving bit 0 and both event statuses.</p><p>On a narrow screen, scroll the table horizontally to see all columns.</p>
<div class="table-wrap"><table><caption>Construct the write by field attribute</caption><thead><tr><th scope="col">Bits</th><th scope="col">Assumed attribute</th><th scope="col">Read → write</th><th scope="col">Reason</th></tr></thead><tbody><tr><td>7:6</td><td>RsvdZ</td><td>00 → 00</td><td>Write zero</td></tr><tr><td>5:4</td><td>RsvdP</td><td>00 → 00</td><td>Preserve the read value</td></tr><tr><td>3:2</td><td>RW1C</td><td>11 → 00</td><td>Write zero to preserve events</td></tr><tr><td>1:0</td><td>RW</td><td>01 → 11</td><td>Set bit 1 and retain bit 0</td></tr></tbody></table></div>
<p>Write <code>0000 0011b</code> (0x03). Under these assumptions, RW becomes 11 and RW1C stays 11, giving a readback of <code>0000 1111b</code> (0x0F). Simply OR-ing bit 1 into the read value would write 0x0F and clear both RW1C statuses.</p>
<p>For a real Register, consult all field definitions and permitted access methods. Hardware may update status between the read and write, and other software may change control bits; handle those races using the field rules and platform synchronization. The example does not guarantee that every race is avoided.</p></aside>
<p>Software must preserve the read value when writing RsvdP (reserved, preserve on writes) bits, whereas RsvdZ (reserved, write zero) requires zero on writes. Reserved fields cannot all use the same update rule. A failed read is not a valid indication of absence, and a successful zero read does not prove that a meaningful Register exists there. Establish the entry point and valid result before interpreting the format.</p>
<details class="source-note"><summary>Attributes and evidence limits</summary><p>Base 6.0 §7.4, Table 7-2, pp.913–915. Unimplemented Registers return successful zero reads absent other errors: §7.3.3, p.913. An all-zero Extended Header at 0x100 indicates no Extended Capabilities: §7.6.1, p.1009. That rule differs from a conventional Null Capability ID of zero.</p></details></section>
<section id="questions"><h2>Apply the complete query to changed values</h2>
<p>The worked query starts at 0x100, reaches DSN at 0x180, and reads its data at 0x184 and 0x188. Next locates a different structure; a data offset locates a field in the current structure. The following variations apply that distinction.</p>
<details class="question"><summary>If 0x180 returns 0x24010003, does the DSN Lower DW move to 0x244?</summary><p>No. 0x240 points to the next structure. The current DSN remains at 0x180, with its Lower DW at 0x184. (Figure 7-241, p.1205; Table 7-39, p.1010.)</p></details>
<details class="question"><summary>Does failure to find DSN in the conventional list prove lack of support?</summary><p>No. DSN belongs to the Extended list and requires an interface that can access it. Searching the wrong list or lacking access is not valid absence evidence. (§7.6.1, p.1009; §7.9.3, p.1205.)</p></details></section>
<p>Continue with <a href="/DOCS/pcie-course/chapter-3.html">Chapter 3</a> to see how software establishes a discovery path before it knows the downstream BDFs.</p>
</article>
<nav class="bottom-nav" aria-label="Course and editions"><a href="/DOCS/pcie-course/index.html">Course overview</a><a href="/DOCS/pcie-course/chapter-2.html">Full Chinese tutorial</a><a href="/pcie/chapter-2-zh-tw/">繁體中文</a></nav>
</div>
