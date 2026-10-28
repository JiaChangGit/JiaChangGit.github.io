---
layout: post
title: "PCIe Chapter 23: Power Budgeting, Allocation, and Emergency Reduction"
date: 2026-10-24 00:00:00 +0800
last_modified_at: 2026-10-29 00:00:00 +0800
permalink: /pcie/chapter-23-en/
categories: [PCIe]
tags: [PCIe, Specification]
lang: en
spec_teaching: true
spec_series: pcie
description: "裝置已進 D0，功率限制還有哪些層次？"
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
<nav class="bottom-nav" aria-label="Course and editions"><a href="/DOCS/pcie-course/index.html">Course overview</a><a href="/DOCS/pcie-course/chapter-23.html">Full Chinese tutorial</a><a href="/pcie/chapter-23-zh-tw/">繁體中文</a></nav>
<article class="lesson">
<p>D0 identifies a Function power state; system grants and active power mechanisms still constrain consumption. Power Budgeting reports demand under specified conditions. DPA (Dynamic Power Allocation) adjusts a Function allocation within D0. Read the demand data first, then follow a complete reduction/increase example.</p><figure class="diagram"><svg viewBox="0 0 900 280" style="min-width:640px" role="img" aria-labelledby="ch23-en-t ch23-en-d"><title id="ch23-en-t">Different power mechanisms and their scopes</title><desc id="ch23-en-d">Three parallel mechanisms: consumption reports, card grants and D0 allocation. Emergency reduction has priority when supported.</desc><g data-walk-target="n0"><rect x="20" y="25" width="260" height="95" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="150" y="60" text-anchor="middle" font-size="17">Reported consumption</text><text x="150" y="94" text-anchor="middle" font-size="16">Power Budgeting</text></g><g data-walk-target="a"><text x="150" y="157" text-anchor="middle" font-size="16">Group matching conditions</text></g><g data-walk-target="n1"><rect x="320" y="25" width="260" height="95" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="450" y="60" text-anchor="middle" font-size="17">Card power grant</text><text x="450" y="94" text-anchor="middle" font-size="16">Slot / Power Limit</text></g><g data-walk-target="b"><text x="450" y="157" text-anchor="middle" font-size="16">Check the grant mechanism</text></g><g data-walk-target="n2"><rect x="620" y="25" width="260" height="95" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="750" y="60" text-anchor="middle" font-size="17">Function allocation</text><text x="750" y="94" text-anchor="middle" font-size="16">DPA within D0</text></g><g data-walk-target="c"><text x="750" y="157" text-anchor="middle" font-size="16">Read control and status</text></g><g data-walk-target="n3"><rect x="20" y="205" width="860" height="55" rx="10" fill="var(--surface-alt)" stroke="var(--accent)"/><text x="450" y="239" text-anchor="middle" font-size="17">Emergency Power Reduction: priority when supported</text></g></svg><figcaption>The columns describe separate mechanisms, not a required execution sequence. Author-drawn from Base 6.0 §§6.8, 6.9, 6.16 and 6.24. DPA means Dynamic Power Allocation.</figcaption></figure><section id="budget"><h2>Establish whose consumption is being reported</h2>
<p>A Function is a software-visible unit; an add-in card can contain several Functions and Devices. Table 6-10 <em>Power Budgeting Deployments</em> (p.743) determines reporting scope from capability placement. For a multifunction Device with Power Budgeting in exactly one Function, the data covers the Device. When multiple Functions implement it, their data is per-Function and is summed according to the table.</p>
<p>Establish that scope before calculating watts. A multi-device card can report at card or Device level; adding every readable value without that distinction can count the same demand twice. Section 6.8.1 separately describes firmware allocations and the budget manager's responsibilities. The platform chooses its management process.</p>
<p><strong>[Simulated data] The following data is created for teaching and does not represent specific hardware or a platform.</strong> Our card contains one single-function Endpoint. Function 0 covers all consumption, with no other Device or external power source. It draws from 12 V and 3.3 V rails and is currently in D0. Assume System Allocated=0, Extended Power Budgeting Supported=0 and exactly four non-extended data entries. Separately, the platform has already granted sufficient power under the applicable form factor and system budget.</p>
<p class="source-note">Source: §6.8 <em>Power Budgeting Mechanism</em>, §6.8.1 <em>System Power Budgeting Process Recommendations</em> and Table 6-10, document/PDF pp.742–744.</p></section>

<section id="budget-entries"><h2>Select data, decode conditions, then add matching rails</h2>
<p>Walk the Extended Capability (configuration-space extension) list to ID 0004h, Version 1h; call its base C. Figure 7-136 locates 8-bit Data Select at C+04h, 32-bit Data at C+08h and Power Budgeting Capability at C+0Ch. Check System Allocated, then <strong>write a Data Select index and read Data</strong>. Indexing starts at zero, but its default is undefined, so explicitly select each entry.</p>
<p>Next use Figure 7-139 / Table 7-122. Base Power occupies bits [7:0]. Data Scale's low bits are [9:8], while its third bit is at bit 21. The scale bits are not contiguous. Our non-extended case has the third bit clear; encoding 001b gives 0.1×. Identify PM State, PM Sub State, Type and Power Rail before multiplying Base Power by the scale:</p>
<div class="table-wrap"><table><thead><tr><th scope="col">Index</th><th scope="col">Data</th><th scope="col">PM State / Sub State</th><th scope="col">Type</th><th scope="col">Power Rail</th><th scope="col">Base Power</th><th scope="col">Data Scale</th><th scope="col">Power</th></tr></thead><tbody><tr data-budget-entry="0"><td>0</td><td>000181B4h</td><td>D0 / 0</td><td>011b</td><td>000b / 12 V</td><td>180</td><td>0.1×</td><td>18 W</td></tr><tr data-budget-entry="1"><td>1</td><td>00058132h</td><td>D0 / 0</td><td>011b</td><td>001b / 3.3 V</td><td>50</td><td>0.1×</td><td>5 W</td></tr><tr data-budget-entry="2"><td>2</td><td>000381C8h</td><td>D0 / 0</td><td>111b</td><td>000b / 12 V</td><td>200</td><td>0.1×</td><td>20 W</td></tr><tr data-budget-entry="3"><td>3</td><td>0007813Ch</td><td>D0 / 0</td><td>111b</td><td>001b / 3.3 V</td><td>60</td><td>0.1×</td><td>6 W</td></tr></tbody></table></div>
<p>For entry 0, 000181B4h contains Base Power=B4h=180 and Data Scale=001b, giving 18 W. Type=011b means Sustained Power; Power Rail=000b means 12 V. Entry 1 matches the condition on the other rail, for <strong>23 W</strong> D0 sustained consumption. Entries 2/3 use Type=111b, Maximum Power, and total <strong>26 W</strong>.</p>
<p>Table 7-122 gives different measurement definitions: unless the form factor explicitly says otherwise, Sustained Power is a 5-second average at maximum throughput; Maximum Power uses a 1 ms moving window. The 23 W and 26 W describe different conditions and are not added together. A Thermal entry belongs to cooling assessment, not another electrical rail to add again.</p>
<p>Index 4 exceeds this case's four entries, so Data returns all zeros. On a device supporting Extended Power Budgeting, disabled extended entries are also hidden as zeros; interpret a zero with support, enable and index context. Table 7-122 also defines alternative power-range encodings when Base Power exceeds EFh under its stated conditions. F0h cannot always be treated as 240 W.</p>
<p>System Allocated=0 makes this case relevant to the responsible budget manager. If the bit is 1, the Device's budget is already included in the system budget; software must ignore its reported data for budgeting decisions to avoid counting it again. The Device still consumes power.</p>
<p class="source-note">Source: §§7.8.1–7.8.1.5; Figure 7-136 (p.1090), Figure 7-137 / Table 7-120 (p.1091), Figure 7-139 / Table 7-122 (pp.1094–1097), Figure 7-140 / Table 7-123 (p.1098). Index and zero-return rules: pp.1091, 1093.</p></section>

<section id="grants"><h2>Does reporting 26 W grant the card 26 W?</h2>
<p>Power Budgeting reports demand. Check the active grant mechanism separately. Under §6.9, Downstream Port Slot Capabilities supply the Slot Power Limit. Set_Slot_Power_Limit Message carries it to the Upstream Port across the same Link, where Device Capabilities exposes Captured Slot Power Limit Value/Scale. The limit applies to the entire adapter.</p>
<p>Before receiving a higher grant, the card must obey the applicable form-factor initial limit. The Slot mechanism does not permit an arbitrary lower value either. Section 6.8.3 separately defines Power Limit PM Sub State and Out of Band Power Limit mechanisms with distinct priority rules. Power Limit Enable and Power Limit PM Sub State may be configured through Configuration Writes only while all Device Functions are in D0uninitialized; changing them after any Function leaves that state has undefined behavior.</p>
<p>The runtime example therefore uses DPA. Power Budgeting has up to eight PM Sub States; DPA has up to 32 substates. Their numbers have no automatic correspondence. Function D0/D1 states and Link L1.1/L1.2 states describe still other mechanisms.</p>
<p class="source-note">Source: §6.8.3 <em>Power Limit Mechanismsm</em> (title as printed) and §6.9 <em>Slot Power Limit Control</em>, document/PDF pp.744–746.</p></section>

<section id="dpa"><h2>Reduce a D0 allocation from 26 W to 10 W</h2>
<p>DPA is optional for applicable Endpoint Functions in D0. Substates run contiguously from 0 through Substate_Max. Substate 0 has the highest allocation; successive allocations must not increase. Software can select 2 directly from 0 without visiting 1. The Function must respond to Configuration Space accesses in every substate.</p>
<p>Assume our single-function card also implements DPA at base D. Figure 7-281 provides the layout; Figure 7-282 / Table 7-251 identifies ID 0016h, Version 1h. Build its allocation table in this order:</p>
<ol><li>Figure 7-283 / Table 7-252: DPA Capability at D+04h reads 08031002h. Substate_Max=2 means three substates. Power Allocation Scale=01b gives 1.0×; Transition Latency Unit=00b gives 1 ms; Value 0=3 and Value 1=8.</li><li>Figure 7-284 / Table 7-253: DPA Latency Indicator at D+08h reads 00000004h. Bit 2=1 selects Value 1 for target substate 2; bits 0/1=0 select Value 0.</li><li>Figures 7-287 / 7-288 and Table 7-256: the Power Allocation Array starts at D+10h, with one byte per substate, not one DWORD.</li></ol>
<div class="table-wrap"><table><thead><tr><th scope="col">Substate</th><th scope="col">Array offset</th><th scope="col">Array byte</th><th scope="col">Allocation</th><th scope="col">Indicator bit</th><th scope="col">Maximum latency</th></tr></thead><tbody><tr data-dpa-profile="0"><td>0</td><td>D+10h</td><td>1Ah</td><td>26 W</td><td>0</td><td>3 ms</td></tr><tr data-dpa-profile="1"><td>1</td><td>D+11h</td><td>12h</td><td>18 W</td><td>0</td><td>3 ms</td></tr><tr data-dpa-profile="2"><td>2</td><td>D+12h</td><td>0Ah</td><td>10 W</td><td>1</td><td>8 ms</td></tr></tbody></table></div>
<p>The maximum transition latency into substate 2 is therefore <strong>8 ms</strong>; returning to substate 0 uses <strong>3 ms</strong>. The <strong>target substate</strong> selects the limit, and completion may occur sooner. DPA's scale encodings differ from Power Budgeting Data Scale; read their respective tables.</p>
<p class="source-note">Source: §6.16 <em>Dynamic Power Allocation (DPA) Capability</em>, document/PDF pp.777–778; §7.9.12, Figures 7-281–7-288 and Tables 7-251–7-256, pp.1236–1241.</p></section>

<section id="dpa-transition"><h2>Read Control and Status together</h2>
<p>Figure 7-285 / Table 7-254 places Status at D+0Ch: bits [4:0] are Substate Status and bit 8 is Substate Control Enabled. Initial Status=0100h means Enabled=1 and current substate 0. Figure 7-286 / Table 7-255 places Control at D+0Eh; bits [4:0] select the target. Its RsvdP bits (reserved bits whose values must be preserved) are initially zero here. Assume the Function remains in D0, with no Reset, emergency reduction or other software writes, and the reduction completes before the increase is requested.</p>
<figure class="diagram"><svg viewBox="0 0 900 300" style="min-width:640px" role="img" aria-labelledby="dpa-transition-title dpa-transition-desc"><title id="dpa-transition-title">Lower allocation: 26 W → 10 W / Higher allocation: 10 W → 26 W</title><desc id="dpa-transition-desc">Substate Status=0 / 26 W during transition. Substate Status=0 / 26 W during transition.</desc><text x="30" y="32" font-size="18">Lower allocation: 26 W → 10 W</text><path d="M100 70 H800" stroke="var(--accent)" stroke-width="2"/><polygon points="800,70 790,65 790,75" fill="var(--accent)"/><path d="M100 58 V82 M800 58 V82" stroke="var(--accent)" stroke-width="2"/><text x="100" y="106" text-anchor="middle" font-size="16">Request 2</text><text x="800" y="106" text-anchor="middle" font-size="16">At 2 (≤8 ms)</text><text x="450" y="60" text-anchor="middle" font-size="16">Substate Status=0 / 26 W during transition</text><text x="30" y="179" font-size="18">Higher allocation: 10 W → 26 W</text><path d="M100 217 H800" stroke="var(--accent)" stroke-width="2"/><polygon points="800,217 790,212 790,222" fill="var(--accent)"/><path d="M100 205 V229 M800 205 V229" stroke="var(--accent)" stroke-width="2"/><text x="100" y="253" text-anchor="middle" font-size="16">Request 0</text><text x="800" y="253" text-anchor="middle" font-size="16">At 0 (≤3 ms)</text><text x="450" y="207" text-anchor="middle" font-size="16">Substate Status=0 / 26 W during transition</text></svg><figcaption>Author-drawn from §6.16. These are two transition directions, not two transitions that must occur consecutively. The watts indicate allocations, not measured instantaneous power.</figcaption></figure>
<div class="table-wrap"><table><thead><tr><th scope="col">Observation</th><th scope="col">Control</th><th scope="col">Status</th><th scope="col">Allocation</th><th scope="col">Budget interpretation</th></tr></thead><tbody><tr data-dpa-transition="initial"><td>Before reduction</td><td>0000h</td><td>0100h</td><td>26 W</td><td>Budget the initial allocation</td></tr><tr data-dpa-transition="down-pending"><td>Reduction in progress</td><td>0002h</td><td>0100h</td><td>26 W</td><td>Keep the higher allocation until transition completion</td></tr><tr data-dpa-transition="down-done"><td>Reduction completed</td><td>0002h</td><td>0102h</td><td>10 W</td><td>The lower allocation now applies</td></tr><tr data-dpa-transition="up-pending"><td>Increase has begun</td><td>0000h</td><td>0100h</td><td>26 W</td><td>Reserve the higher allocation before requesting the increase</td></tr></tbody></table></div>
<p>During a reduction, Status must retain the higher allocation until completion. While Substate Control=2 but Substate Status still reports 0, reserve 26 W; do not give the difference to another card yet. Once Substate Status reports 2, the Function must obey its 10 W allocation.</p>
<p>During an increase, Substate Status must already indicate the higher allocation. Observing target 0 alone therefore does not establish completion. Prepare the 26 W budget before issuing the request, then use the target's maximum transition latency and any necessary Device information for subsequent actions. Status describes the allocation the Function must obey, not instantaneous sensed power or guaranteed application performance.</p>
<p>Section 6.16 permits a new target before the previous transition completes. The Device may alter an ongoing transition, or compare against the latest target after completion and transition again. Our case avoids intervening requests to show the two directions clearly. Preserve every Control write when interpreting a real trace; one final Status does not reconstruct that history.</p>
<p class="source-note">Source: §6.16, document/PDF pp.777–778; §§7.9.12.4–7.9.12.5, Figures 7-285 / 7-286 and Tables 7-254 / 7-255, pp.1239–1240.</p></section>

<section id="dpa-handoff"><h2>Does writing 1 enable Substate Control?</h2>
<p>Check the attribute first. Substate Control Enabled is RW1C (write one to clear), in Status bit 8, not DPA Control. Hardware sets it after a Conventional Reset or FLR (Function Level Reset); software cannot directly set it back to 1.</p>
<p>For example, with Status=0102h in substate 2, writing 0100h to Status clears Enabled. Subsequent target writes to Control no longer directly initiate DPA transitions. This allows Device-specific software to take over allocation; its policy depends on that software and Device mechanism. Disabled does not promise a permanent 10 W allocation.</p>
<p class="source-note">Source: §6.16, document/PDF p.777; §7.9.12.4 / Table 7-254, pp.1239–1240.</p></section>

<section id="emergency"><h2>Will normal operation resume automatically after emergency reduction?</h2>
<p>Emergency Power Reduction State is an optional fail-safe intended to prevent system damage and overrides the normal power mechanisms discussed here. Read Emergency Power Reduction Supported and Emergency Power Reduction Initialization Required in Device Capabilities 2, then use Table 6-16 to identify allowed triggers. Continue into §6.24's text for exit behavior.</p>
<p>For example, Supported=10b permits the applicable form-factor mechanism only if that form factor actually defines such a request. Vendor-specific and autonomous triggers also follow Table 6-16. There is no universal standard Configuration-bit write sequence that triggers every platform.</p>
<div class="table-wrap"><table><thead><tr><th scope="col">Initialization Required</th><th scope="col">Entry</th><th scope="col">Exit</th></tr></thead><tbody><tr><td>0</td><td>The Function may reduce performance or enter a Device-specific dormant state; its Upstream Port remains operating and outstanding requests must complete normally</td><td>Normal operation resumes without software intervention</td></tr><tr><td>1</td><td>The Function ceases normal operation; its Upstream Port may enter DL_Down. If it stays DL_Up, outstanding requests must still complete normally</td><td>Software intervention is required. If the port entered DL_Down, all Functions are reset and full reconfiguration is required</td></tr></tbody></table></div>
<p>Initialization Required=1 can also leave the port in DL_Up, so accessible Configuration Space alone does not establish that software reinitialization is unnecessary. Notification of required reinitialization and external signaling details require platform, form-factor or vendor documentation. Power Budgeting must also report the appropriate emergency-state consumption; the normal D0 26 W value cannot simply be reused.</p>
<p class="source-note">Source: §6.24 <em>Emergency Power Reduction State</em>, Table 6-16 <em>Emergency Power Reduction Supported Values</em>, document/PDF pp.812–813; §7.5.3.15, p.993; §7.8.1.4, p.1097.</p></section>

<section id="virtual-functions"><h2>Which PF/VF power belongs in the same allocation?</h2><dl class="st-terms" aria-label="Terms in this passage"><div><dt>PF</dt><dd>Physical Function</dd></div><div><dt>VF</dt><dd>Virtual Function</dd></div></dl>
<p>A PF (Physical Function) and VF (Virtual Function) have distinct roles in SR-IOV (Single Root I/O Virtualization). A PF may implement Power Budgeting, covering all associated VFs; VFs must not implement it. VF DPA allocation is likewise managed through its associated PF; VFs must not implement DPA Capability.</p>
<p>Some or all Functions of a general multifunction Device may implement DPA; their allocations are summed. One Function's DPA may also account for Functions lacking it, with implementation-specific associations. Do not copy the single-function case into an extra 26 W allocation for every VF.</p>
<p>D-states follow §5.10 separately. PFs must implement Power Management Capability; VFs may implement it. A VF without it behaves as if programmed into its PF's equivalent power state. When a VF implements it, putting the PF in a lower-power state than the VF has undefined behavior; software should lower the VFs first. That differs from changing DPA allocation while remaining in D0.</p>
<p class="source-note">Source: §§5.10–5.10.1, document/PDF p.655; §6.16.1, p.778; §7.8.1, p.1090.</p></section><section id="sources"><h2>Edition and sources</h2><p>This chapter uses PCI Express Base Specification Revision 6.0 (6.0-1.0-PUB). Document and PDF page numbers match. Example values and observations are author assumptions; no hardware measurement was performed.</p><details class="source-note"><summary>Complete source locations</summary><ul><li>§6.8 <em>Power Budgeting Mechanism</em>, pp.742–745; Table 6-10 <em>Power Budgeting Deployments</em>, p.743; §6.8.1 <em>System Power Budgeting Process Recommendations</em>, pp.743–744; §6.8.3 <em>Power Limit Mechanismsm</em>, pp.744–745; §6.9 <em>Slot Power Limit Control</em>, pp.745–746.</li><li>§7.8.1 <em>Power Budgeting Extended Capability</em>, pp.1090–1098; Figure 7-136 (layout), p.1090; Figure 7-137 / Table 7-120 (header), p.1091; §7.8.1.2 <em>Power Budgeting Data Select Register</em>, p.1091; §7.8.1.3 / Figure 7-138 / Table 7-121 <em>Power Budgeting Control Register</em>, pp.1091–1093; §7.8.1.4 / Figure 7-139 / Table 7-122 <em>Power Budgeting Data Register</em>, pp.1093–1097; §7.8.1.5 / Figure 7-140 / Table 7-123 <em>Power Budgeting Capability Register</em>, p.1098.</li><li>§6.16 <em>Dynamic Power Allocation (DPA) Capability</em>, pp.777–778; §6.16.1 <em>DPA Capability with Multi-Function Devices</em>, p.778.</li><li>§7.9.12 <em>Dynamic Power Allocation Extended Capability (DPA Capability)</em>, pp.1236–1241; Figure 7-281 <em>Dynamic Power Allocation Extended Capability Structure</em>, p.1237; Figure 7-282 / Table 7-251 <em>DPA Extended Capability Header</em>, pp.1237–1238; Figure 7-283 / Table 7-252 <em>DPA Capability Register</em>, pp.1238–1239; Figure 7-284 / Table 7-253 <em>DPA Latency Indicator Register</em>, p.1239; Figure 7-285 / Table 7-254 <em>DPA Status Register</em>, pp.1239–1240; Figure 7-286 / Table 7-255 <em>DPA Control Register</em>, p.1240; Figure 7-287 <em>DPA Power Allocation Array</em>, p.1240; Figure 7-288 / Table 7-256 <em>Substate Power Allocation Register (0 to Substate_Max)</em>, p.1241.</li><li>§6.24 <em>Emergency Power Reduction State</em>, pp.812–813; Table 6-16 <em>Emergency Power Reduction Supported Values</em>, p.812; §7.5.3.15 <em>Device Capabilities 2 Register</em>, p.993 (support and initialization fields); §5.10 <em>SR-IOV Power Management</em> / §5.10.1 <em>VF Device Power Management States</em>, p.655.</li></ul></details></section>
</article>
<nav class="bottom-nav" aria-label="Course and editions"><a href="/DOCS/pcie-course/index.html">Course overview</a><a href="/DOCS/pcie-course/chapter-23.html">Full Chinese tutorial</a><a href="/pcie/chapter-23-zh-tw/">繁體中文</a></nav>
</div>
