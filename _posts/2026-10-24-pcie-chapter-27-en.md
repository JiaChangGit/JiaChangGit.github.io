---
layout: post
title: "PCIe Chapter 27: ATS, PRI, and PASID Address-Translation Flows"
date: 2026-10-24 00:00:00 +0800
last_modified_at: 2026-10-29 00:00:00 +0800
permalink: /pcie/chapter-27-en/
categories: [PCIe]
tags: [PCIe, Specification]
lang: en
spec_teaching: true
spec_series: pcie
description: "轉譯、失效與頁面群組的回覆，如何接回真正的資料存取？"
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
<nav class="bottom-nav" aria-label="Course and editions"><a href="/DOCS/pcie-course/index.html">Course overview</a><a href="/DOCS/pcie-course/chapter-27.html">Full Chinese tutorial</a><a href="/pcie/chapter-27-zh-tw/">繁體中文</a></nav>
<article class="lesson">
<p>ATS (Address Translation Services) obtains mappings and permissions. PRI (Page Request Interface) requests page service, while PASID (Process Address Space ID) adds address-space identity. Follow one case through lookup, data access, invalidation and page groups without treating their responses as equivalent.</p><figure class="diagram"><svg viewBox="0 0 900 350" style="min-width:680px" role="img" aria-labelledby="ch27-en-t ch27-en-d"><title id="ch27-en-t">Translation lookup, actual access and optional page service</title><desc id="ch27-en-d">ATS obtains translations before translated Memory access. PRI requests pages when needed and returns to ATS. Invalidation is a separate exchange when mappings change.</desc><g data-walk-target="dev"><rect x="20" y="15" width="270" height="55" rx="9" fill="var(--surface-alt)" stroke="var(--line)"/><text x="155" y="49" text-anchor="middle" font-size="17">Endpoint / ATC</text></g><g data-walk-target="ta"><rect x="610" y="15" width="270" height="55" rx="9" fill="var(--surface-alt)" stroke="var(--line)"/><text x="745" y="49" text-anchor="middle" font-size="17">Platform / TA + Memory</text></g><g data-walk-target="query"><text x="450" y="100" text-anchor="middle" font-size="16">ATS Translation Request</text><path d="M290 115 H610" stroke="var(--accent)" stroke-width="2"/><polygon points="610,115 600,110 600,120" fill="var(--accent)"/></g><g data-walk-target="reply"><text x="450" y="160" text-anchor="middle" font-size="16">Translation Completion: mapping + permissions</text><path d="M610 175 H290" stroke="var(--accent)" stroke-width="2"/><polygon points="290,175 300,170 300,180" fill="var(--accent)"/></g><g data-walk-target="memory"><text x="450" y="220" text-anchor="middle" font-size="16">Memory Request: translated address</text><path d="M290 235 H610" stroke="var(--accent)" stroke-width="2"/><polygon points="610,235 600,230 600,240" fill="var(--accent)"/></g><g data-walk-target="pri"><rect x="45" y="285" width="810" height="45" rx="8" fill="var(--surface-alt)" stroke="var(--line)"/><text x="450" y="314" text-anchor="middle" font-size="16">If pages are unavailable: PRI → group response → fresh ATS lookup</text></g></svg><figcaption>Author-drawn flow map. ATC (Address Translation Cache) stores results; TA (Translation Agent) uses platform translation/protection information. PRI is an optional branch when needed.</figcaption></figure><dl class="st-terms" aria-label="Terms in this passage"><div><dt>ATS</dt><dd>Address Translation Services</dd></div><div><dt>PRI</dt><dd>Page Request Interface</dd></div></dl>
<section id="lookup"><h2>Place the translation participants before tracing DMA</h2><dl class="st-terms" aria-label="Terms in this passage"><div><dt>DMA</dt><dd>Direct Memory Access, device access to memory</dd></div></dl><p>Figure 10-1 places the device ATC, platform TA and ATPT (Address Translation and Protection Table). TA and table may be integrated or separate. Figure 10-2 then traces the lookup before actual DMA (Direct Memory Access).</p><p><strong>Simulated data:</strong> the single Endpoint Function uses RID=0300h and PASID=00021h, is in D0 with Bus Master Enable set, and has platform authorization for these services. The path accepts the example packets; TC0/TC1 transport is ready. The numeric case uses Non-Flit Mode without Reset, Replay or PASID stop/reuse events. These are author assumptions, not hardware observations.</p><dl class="st-terms" aria-label="Terms in this passage"><div><dt>RID</dt><dd>Routing ID, the packet routing identity</dd></div><div><dt>PASID</dt><dd>Process Address Space ID</dd></div></dl><p>Base 6.0 Chapter 10 and §6.20 define the protocol. Platform page tables, IOMMU (Input/Output Memory Management Unit) registers and OS interfaces need their own documents. Switches can transparently forward ATS; they need not become TAs or implement ATS Requester Capabilities.</p><p class="source-note">Base 6.0 §10.1.1, Figures 10-1/10-2, pp.1470–1474.</p></section>
<section id="pasid"><h2>Equal PASIDs do not identify an address space across Functions</h2><p>Under §6.20 combine PASID with Requester ID. RID 0310h using PASID 21h is not thereby the same address space as RID 0300h/PASID 21h. PASID is not a universal OS PID encoding; mapping it to Function work context is device/platform specific.</p><dl class="st-terms" aria-label="Terms in this passage"><div><dt>RID</dt><dd>Routing ID, the packet routing identity</dd></div></dl><p>Figure 6-20/Table 6-15 locates the Non-Flit End-End Prefix. Execute Requested=0, Privileged Mode Requested=0 and PASID=00021h produce bytes <code data-pasid-prefix="example">91 00 00 21</code>. Flit Mode uses OHC-A1, a header block carrying PASID and related information. The Translation Request No Write bit also belongs in this block.</p><p>Max PASID Width=8 permits values 0–255, including 21h and 0. Hardware must not invent reserved PASID values. Ordinary Completions, including Translation Completions, must not carry PASID. Recover the original query's PASID through Requester ID/Tag context. PRG (Page Request Group) Response is a separately permitted Message type.</p><p class="source-note">Base 6.0 §§6.20–6.20.2.2, Figure 6-20/Table 6-15, pp.791–793; §10.1.3, pp.1477–1478.</p></section>
<section id="configure"><h2>Read three separate capability structures</h2><p>Locate PASID ID 001Bh, ATS ID 000Fh and Page Request ID 0013h, all Version 1 in this edition, with bases P, A and R. Figures 7-185, 10-29 and 10-33 locate the following fields:</p><div class="table-wrap"><table><thead><tr><th scope="col">Structure / field</th><th scope="col">Offset</th><th scope="col">Value</th><th scope="col">Decoded condition</th></tr></thead><tbody><tr data-ats-config="pasid-cap"><td>PASID Capability</td><td>P+04h</td><td>0808h</td><td>Max PASID Width=8; Translated Requests with PASID Supported=1</td></tr><tr data-ats-config="pasid-control"><td>PASID Control</td><td>P+06h</td><td>0009h</td><td>PASID Enable=1; Translated Requests with PASID Enable=1</td></tr><tr data-ats-config="ats-cap"><td>ATS Capability</td><td>A+04h</td><td>0024h</td><td>Invalidate Queue Depth=4; Page Aligned Request=1</td></tr><tr data-ats-config="ats-control"><td>ATS Control</td><td>A+06h</td><td>8000h</td><td>Enable=1; STU=0 → 4 KiB; AMAE=0</td></tr><tr data-ats-config="pri-status"><td>Page Request Status, before enable</td><td>R+06h</td><td>8100h</td><td>Stopped=1; PRG Response PASID Required=1</td></tr><tr data-ats-config="pri-capacity"><td>Outstanding Page Request Capacity</td><td>R+08h</td><td>00000004h</td><td>4 requests</td></tr><tr data-ats-config="pri-allocation"><td>Outstanding Page Request Allocation</td><td>R+0Ch</td><td>00000003h</td><td>3 requests</td></tr><tr data-ats-config="pri-control"><td>Page Request Control, after enable</td><td>R+04h</td><td>0001h</td><td>Enable=1</td></tr></tbody></table></div><p>PASID Capability value 0808h advertises an 8-bit width and Translated Requests with PASID support. Execute/Privileged operation is not requested. Control value 0009h enables PASID and translated Requests with PASID. Configure PASID while ATS Enable=0, then set ATS Control value 8000h. Changing any PASID Control bit while ATS is enabled has undefined behavior.</p><p>STU (Smallest Translation Unit)=0 means 2<sup>0</sup>×4 KiB=4 KiB, not disabled translation. Invalidate Queue Depth=4 concerns invalidation buffering, not Page Request allocation. AMA is not enabled in this example.</p><p>While Page Request Enable=0, allocate 3 of Capacity 4 and verify Stopped=1 before enabling. Changing Allocation while enabled is undefined; enabling before successful stop is indeterminate. Stopped is meaningful only when Enable=0, not a live outstanding-request indicator while enabled.</p><p>ATS need not support PRI, and PASID is independent of both. Root Complex PASID support/enable mechanisms are implementation specific; do not assume an Endpoint PASID Control exists in the Root Port.</p><p class="source-note">Base 6.0 §7.8.9, Figures 7-185–7-188, Tables 7-159–7-161, pp.1148–1151; §10.5.1, Figures 10-29–10-32, Tables 10-9–10-11, pp.1513–1516; §10.5.2, Figures 10-33–10-36, Tables 10-13–10-15, pp.1516–1520.</p></section>
<section id="ats-capability-details"><h2>How do ATS capability and control fields affect the example?</h2><p>Find ATS in the Extended Capability list. Figure 10-30 and Table 10-9 define ID <code>000Fh</code>, Version 1, and Next Capability Offset relative to Configuration Space. Call the discovered structure base A; Figure 10-29 places the 16-bit ATS Capability at A+04h and 16-bit ATS Control at A+06h.</p><p>In the earlier author-created non-VF example, Capability=<code>0024h</code> and Control=<code>8000h</code>. Figure 10-31 and Table 10-10 give Queue Depth=4, Page Aligned Request=1, and zero for Global Invalidate Supported, Relaxed Ordering Supported, and ATS Memory Attributes Supported. This is one function's snapshot.</p><p>On a phone, scroll the table sideways to see all columns.</p><div class="table-wrap"><table><thead><tr><th>Field</th><th>Effect on the flow</th></tr></thead><tbody><tr><td>Page Aligned Request</td><td>When set, the Function always uses a 4096-byte aligned untranslated address in a Translation Request; it does not fix STU to 4 KiB.</td></tr><tr><td>Global Invalidate Supported</td><td>Controls treatment of Global Invalidate with PASID; see the earlier invalidation-scope table.</td></tr><tr><td>Relaxed Ordering Supported</td><td>The Function may set RO in a Translation Request when the capability and the Device Control Enable Relaxed Ordering conditions permit. Support does not mean every Request sets it.</td></tr><tr><td>ATS Memory Attributes Supported</td><td>Indicates support for using AMA from Translation Completions in the ATC; without support the Function ignores Completion AMA.</td></tr></tbody></table></div><p>Figure 10-32 and Table 10-11 show E=1 and STU=0 in the example: translation caching is enabled and the smallest translation unit is 4 KiB. For a separate teaching value STU=2, <code>2² × 4 KiB = 16 KiB</code>. STU is a minimum translation/invalidation unit, not the complete Translation Request length.</p><p>AMAE permits the Requester to provide AMA in a TPH TLP Prefix; when AMAE is set, AMAD provides a default AMA and the corresponding optimization. With AMAE=0 in this case, AMAD does not establish enabled use. Table 10-11 lists zero as the default for STU, AMAD, AMAE and E. If the Endpoint supports PASID, changing any PASID Control bit while ATS E=1 has undefined behavior.</p><dl class="st-terms" aria-label="Terms in this passage"><div><dt>TPH</dt><dd>TLP Processing Hints</dd></div><div><dt>TLP</dt><dd>Transaction Layer Packet</dd></div></dl><p>In SR-IOV, VF and PF ATS capabilities can be enabled independently, but VF Invalidate Queue Depth and STU are hardwired to zero and the associated PF values apply. Do not infer a VF's usable depth or STU from those zeros alone. Base 6.0 §10.5.1–§10.5.1.3, Figures 10-29–10-32 and Tables 10-9–10-11, pp.1513–1516. Device Control Enable Relaxed Ordering is in Table 7-21, p.960.</p><dl class="st-terms" aria-label="Terms in this passage"><div><dt>SR-IOV</dt><dd>Single Root I/O Virtualization</dd></div><div><dt>VF</dt><dd>Virtual Function</dd></div><div><dt>PF</dt><dd>Physical Function</dd></div></dl></section>
<section id="translation-case"><h2>Read four bytes at untranslated address 40001234h</h2><p>Table 10-1 separates AT (Address Type): 00b is Untranslated, 01b is Translation Request, and 10b is Translated. AT00b does not universally mean CPU virtual address; the TA determines its interpretation. AT10b does not guarantee bypass of platform protection checks.</p><p>With Page Aligned Request=1, align the query to 40001000h. Figures 10-10/10-11 describe the MRd (Memory Read) with AT=01b. The TA returns the translation in a CplD (Completion with Data). Length=2 DW asks for at most one 8-byte translation entry, not eight application bytes. NW (No Write)=1 requests read-only use.</p><dl class="st-terms" aria-label="Terms in this passage"><div><dt>DW</dt><dd>Double Word, a four-byte unit</dd></div></dl><div class="table-wrap"><table><caption>MRd denotes a Read Request; CplD denotes a Completion carrying Data. Trace the lookup and data access separately.</caption><thead><tr><th scope="col">TLP</th><th scope="col">AT</th><th scope="col">Requester ID</th><th scope="col">Tag</th><th scope="col">Length</th><th scope="col">Address / data</th></tr></thead><tbody><tr data-ats-step="query"><td>MRd / Translation Request</td><td>01b</td><td>0300h</td><td>2Ah</td><td>2 DW</td><td>40001000h; NW=1</td></tr><tr data-ats-step="translation"><td>CplD / Translation Completion</td><td>—</td><td>0300h</td><td>2Ah</td><td>2 DW</td><td>Base=90000000h; S=0; R=1; W=0; U=0</td></tr><tr data-ats-step="read"><td>MRd / Memory Read</td><td>10b</td><td>0300h</td><td>2Bh</td><td>1 DW</td><td>90000234h</td></tr><tr data-ats-step="data"><td>CplD / Memory Read data</td><td>—</td><td>0300h</td><td>2Bh</td><td>1 DW</td><td>4 bytes application data</td></tr></tbody></table><dl class="st-terms" aria-label="Terms in this passage"><div><dt>TLP</dt><dd>Transaction Layer Packet</dd></div><div><dt>DW</dt><dd>Double Word, a four-byte unit</dd></div></dl></div><p>Decode Figure 10-14/Table 10-3: S=0 means 4 KiB; R=1, W=0, U=0 permits an appropriately scoped translated Read. Assume Global, Priv, Exe, N, AMA are zero. The page offset is 234h, so 90000000h + 234h = 90000234h. Its page is 90000000h–90000FFFh, and the four bytes do not cross it.</p><p>Memory Read Tag 2Bh is a new Transaction. Only the example's observed SC (Successful Completion) with four application bytes establishes that Read's result. Query Tag 2Ah completed the translation lookup. A Translation Request is not a flushing/ordering primitive for previous Writes.</p><p class="source-note">Base 6.0 §§10.2.1–10.2.2, Table 10-1, Figures 10-6–10-13, pp.1478–1483; §10.2.3, Figure 10-14/Table 10-3, pp.1484–1489; §10.2.4, p.1496. Mode-specific base Headers: <a href="/DOCS/pcie-course/chapter-14.html">Chapter 14</a>.</p></section>
<section id="translation-request-fields"><h2>How does Length request two translations?</h2><p>Continue the teaching example with STU=0 and Page Aligned Request=1. Starting at <code>40001000h</code>, request translations for two consecutive 4 KiB regions. Length=4 DW permits up to two translation entries: each is 8 bytes and represents one or more STUs. Length describes the translation information that may be returned, not the application's data size. The TA may return fewer entries, but not more than requested; decode each returned entry's range and permissions before using a mapping.</p><p>Under §§10.2.2.2 and 10.2.2.4, the implied request range is 2<sup>0+12</sup> × (4÷2) = 8 KiB. Length must indicate an even number of DWs and must not exceed the limit determined by the Root Port's Read Completion Boundary (RCB). An odd Length or one above the permitted limit is treated by the TA as a Malformed Packet.</p><p>Figures 10-10–10-13 separate the modes: in Non-Flit Mode, NW is in the Request Header; in Flit Mode, OHC-A1 is required and contains NW. NW=1 requests read-only access, but the TA may ignore that hint, so check the Translation Completion's R/W fields. In Flit Mode, NW=0 also requires explicit write permission; NW alone does not establish authorization.</p><p>With a PASID, the untranslated address is within that PASID's process address space. Tag has the same meaning as in Memory Read and helps match the translation response to its Request. A Translation Request is not a flushing or ordering primitive for other transactions.</p><p class="source-line">Base 6.0 §§10.2.2.1–10.2.2.6, Figures 10-10–10-13, pp.1481–1483; address type: §10.2.1, Table 10-1, pp.1478–1480.</p></section>
<section id="translation-range-fields"><h2>How is a translation larger than 4 KiB decoded?</h2><p>The earlier teaching entry uses S=0 for a 4 KiB range. For S=1, locate S and Translated Address in Figure 10-14, then read Table 10-5: starting at address bit 12, the run of 1s and the next 0 encode the range size. Those low bits convey size and cannot simply be interpreted as ordinary address bits.</p><div class="table-wrap"><table><thead><tr><th scope="col">S</th><th scope="col">Low address bits</th><th scope="col">Translation range</th></tr></thead><tbody><tr><td>0</td><td>Size is not determined by bit 12</td><td>4 KiB</td></tr><tr><td>1</td><td>bit 12=0</td><td>8 KiB</td></tr><tr><td>1</td><td>bit 12=1, bit 13=0</td><td>16 KiB</td></tr></tbody></table></div><p><strong>Teaching example:</strong> S=1 and the encoded Translated Address is <code>90001000h</code>, with bit 12=1 and bit 13=0. Table 10-5 gives 16 KiB; removing the low size-encoding bits gives <code>90000000h–90003FFFh</code>. Assume R=1, W=0 and U=0; use the permission together with the Request identity and other applicable conditions.</p><p>S encodes size in units based on 4 KiB; STU is the Function's configured minimum translation unit. STU=2 means 16 KiB, so this range meets that minimum. For STU=3, the minimum is 32 KiB, and the Function must treat this 16 KiB Translation Completion as UR (Unsupported Request).</p><p>Also read N (Non-snooped). If N=1, Memory Reads and Writes using the translation must clear No Snoop in the Request. N=0 does not require No Snoop to be set: Function behavior and Device Control Enable No Snoop still apply. When U=1, N is undefined and cannot determine a later Request's attributes.</p><p class="source-line">Base 6.0 §10.2.3, Figure 10-14 and Table 10-3, pp.1485–1486; §§10.2.3.1–10.2.3.3 and Table 10-5, pp.1487–1488.</p></section>
<section id="permissions"><h2>SC does not replace permission decoding</h2><div class="table-wrap"><table><thead><tr><th scope="col">Translation Completion</th><th scope="col">R / W / U</th><th scope="col">Next action</th></tr></thead><tbody><tr><td>SC / CplD</td><td>1 / 0 / 0</td><td>Use translated address for Read within all applicable conditions, not Write</td></tr><tr><td>SC / CplD</td><td>0 / 0 / undefined</td><td>No usable mapping permission; do not cache entry or use Translated Address</td></tr><tr><td>SC / CplD</td><td>1 / 0 / 1</td><td>Use only permitted untranslated Read; do not use returned Translated Address</td></tr></tbody></table></div><p>With R=W=0 the range still has meaning, but address and specified other fields are undefined. A later invalid-to-valid mapping change need not send invalidation, so the ATC must not retain this entry as a persistent negative cache.</p><p>U (Untranslated access only)=1 permits caching the specified permission/range information, not using the returned address in AT10b Requests. A later need to Write with a read-only entry requires a fresh translation and authorization, not editing W in the ATC.</p><p>Table 10-2's UR (Unsupported Request) and CA (Completer Abort) are no-data failure responses. UR requires the Function to disable its ATC and stop using translated addresses until the ATC is re-enabled. CA means an error in the TA prevented translation. The RRS retry status is not permitted for Translation Requests and is treated as Malformed TLP when received; the preceding chapter's Configuration RRS conditions do not apply. None of these results alone identifies page non-residence or one failed platform component.</p><p class="source-note">Base 6.0 §10.2.3, Table 10-2 <em>Translation Completion with No Data Status Codes</em>, p.1484; §§10.2.3.1–10.2.3.5, pp.1487–1489.</p></section>
<section id="invalidate"><h2>One invalidation can require more than one reply</h2><p>Suppose the platform changes PASID 21h's mapping for 40001000h–40001FFFh. Use the mode-specific Figures 10-18/10-19 and Figure 10-20's untranslated range. Assume ITag 3, TC0, a 4 KiB range for this PASID only, and no Global Mapping.</p><p>New Requests must not use stale translations. Related outstanding Reads must complete or be marked for discard; Posted Writes must be pushed to the TA. Deleting the ATC entry alone is insufficient. Section 10.3.6 also handles an overlapping outstanding Translation Request so a delayed old result does not repopulate the cache after invalidation.</p><p>For this multi-TC continuation, assume the Function later needed to Write, requested a new translation, and obtained R=W=1 before issuing relevant Posted Writes on TC0 and TC1. Replies on these two channels provide the required push. Figure 10-5 illustrates multiple Invalidate Completions for one Request. Figures 10-21/10-22 identify the replies as <strong>Msg, Code 02h, ID routed</strong>, not ordinary Cpl packets. ITag Vector bit 3 identifies ITag 3:</p><div class="table-wrap"><table><thead><tr><th scope="col">Received TC</th><th scope="col">ITag Vector</th><th scope="col">CC</th><th scope="col">Still required</th><th scope="col">Result</th></tr></thead><tbody><tr data-invalidate-step="tc0"><td>0</td><td>00000008h</td><td>2</td><td>1</td><td>Pending</td></tr><tr data-invalidate-step="tc1"><td>1</td><td>00000008h</td><td>2</td><td>0</td><td>Complete</td></tr></tbody></table><dl class="st-terms" aria-label="Terms in this passage"><div><dt>TC</dt><dd>Traffic Class</dd></div></dl></div><p>Both carry CC (Completion Count)=2 and vector 00000008h. The first leaves one response outstanding. Only after both arrive can the TA consider this invalidation complete and release ITag. CC encoding 0 means eight messages, not none. ITag, Memory Request Tag and PRI PRG Index are separate mechanisms.</p><p>These semantics cover invalidation and push to the TA, not application persistence; memory reclamation needs platform lifecycle coordination. A Function with ATS Capability must accept/complete invalidations even when ATS is disabled, and clearing BME does not remove that duty.</p><p class="source-note">Base 6.0 §10.1.1, Figures 10-4/10-5, pp.1474–1476; §§10.3–10.3.6, Figures 10-18–10-22, pp.1497–1503; §10.3.8, p.1505.</p></section>
<section id="invalidate-scope"><h2>Which PASIDs lose cached entries for a given range?</h2><p>Figure 10-20 identifies an <strong>untranslated address range</strong>; PASID presence and Global Invalidate determine its scope. <strong>Teaching assumptions:</strong> the function is in D0, PASID Enable is set, Global Invalidate is supported, the range includes <code>40001000h</code>, and PASIDs <code>21h</code> and <code>22h</code> are valid.</p><p>On a phone, scroll the table sideways to see all columns.</p><div class="table-wrap"><table><thead><tr><th>Request</th><th>ATC entries to handle</th><th>Relation to the example</th></tr></thead><tbody><tr><td>PASID=21h, Global Invalidate=0</td><td>Non-Global Mapping entries in range requested with PASID 21h; Global Mapping entries may be retained.</td><td>Non-Global entries for 22h are not invalidated by this request.</td></tr><tr><td>PASID=21h, Global Invalidate=1</td><td>Global and non-Global Mapping entries in range associated with any PASID; the request's PASID value is ignored.</td><td>Relevant entries for 21h and 22h in range are handled; out-of-range entries are not invalidated by this rule.</td></tr><tr><td>No PASID in request</td><td>Entries in range requested without PASID, plus entries at all addresses requested with any PASID.</td><td>The second scope is broader than the request's address range; read both rules in §10.3.8.</td></tr></tbody></table></div><p>If Global Invalidate is unsupported, the ATC ignores that bit in a request with PASID and applies §10.3.8 to in-range entries requested with the specified PASID. The bit is Reserved when the request has no PASID. An Invalidate Completion is still required if no entries match or PASID Enable is clear; an out-of-range PASID may be reported as UR.</p><p>Outstanding reads, posted writes, and completion requirements still apply. Base 6.0 §10.3.1 and §10.3.8, Figure 10-20, pp.1498 and 1505.</p></section>
<section id="implicit-invalidate"><h2>Can the cache be invalidated without a message?</h2><p>Yes. Section 10.3.7 lists <strong>implicit invalidation events</strong>, which do not send an explicit Invalidate Completion Message.</p><p>On a phone, scroll the table sideways to see all columns.</p><div class="table-wrap"><table><thead><tr><th>Event</th><th>ATC entries invalidated</th></tr></thead><tbody><tr><td>Conventional Reset, Function Level Reset, or ATS Capability E changing from 0 to 1</td><td>All ATC entries, including those associated with PASID values.</td></tr><tr><td>Stopping use of a PASID as defined by the specification</td><td>All non-Global Mapping entries requested using that PASID.</td></tr></tbody></table></div><p>Stopping PASID 21h and re-enabling ATS can affect the same cache entry, but their scopes differ. No observed completion does not establish that an entry remains valid. PASID stop and reuse also require the coordination in §6.20.1. Base 6.0 §10.3.7, p.1504.</p></section>
<section id="invalidate-race"><h2>What if an old translation response and invalidation cross?</h2><p><strong>Teaching scenario:</strong> An Endpoint has an outstanding Translation Request covering <code>40001000h</code>; the platform sends an overlapping Invalidate Request before its response arrives. They may use different TCs, so Link-level ordering does not establish their relative order.</p><ol><li>Per §10.3.6 the ATC checks outstanding Translation Request ranges against arriving invalidations and marks an overlapping request invalid.</li><li>The corresponding result must be discarded as required so an old mapping does not remain after invalidation. If the response arrives before Invalidate Completion is sent, an implementation may temporarily use it, provided the new-request, outstanding-read, and posted-write conditions of §10.3.3 are met.</li><li>After the applicable work meets completion conditions, send Invalidate Completion. The platform considers the invalidation complete only after collecting all required responses.</li></ol><p>Receipt of a translation response and completion of the invalidation exchange are distinct events. When Shadow Functions are enabled, §10.3.3 includes relevant requests from the Function and its Shadows; one invalidation may target either, subject to the specified Posted Write push conditions. Base 6.0 §10.3.3 and §10.3.6, pp.1501 and 1503–1504.</p></section>
<section id="invalidate-queue"><h2>Does Invalidate Queue Depth=4 mean only four requests can be accepted?</h2><p>These mechanisms describe different things. Invalidate Queue Depth is the number the function can buffer before applying Link backpressure; <code>00000b</code> means invalidate flow control is not necessary for a non-VF Function; Table 10-10 interprets non-VF zero as accepting 32 requests, while a VF reads zero and uses its associated PF value. Input, output, or hybrid queuing is an implementation choice.</p><p>Section 10.3.4 forbids making acceptance of a new Invalidate Request depend on transmitting an earlier Invalidate Completion: both are Posted transactions and such a dependency can deadlock. Its implementation note describes up to 32 outstanding invalidations from one TA to an ATC; this does not require a 32-entry input queue.</p><p>With SR-IOV, VFs associated with a PF share an Invalidation Request queue in the PF. For a nonzero PF Invalidate Queue Depth, the TA must keep the total outstanding targeting that shared queue within that value. If the earlier assumed value 4 is used in such a shared PF/VF configuration, count the relevant functions together.</p><dl class="st-terms" aria-label="Terms in this passage"><div><dt>SR-IOV</dt><dd>Single Root I/O Virtualization</dd></div></dl><p>Invalidate Completions may coalesce multiple ITag Vector bits when the specified conditions, including the same TC and CC, hold. All fragments must have identical Requester ID, CC, and ITag Vector; the TA still collects the required replies for each ITag. Base 6.0 §10.3.2 and §10.3.4–§10.3.5, pp.1500–1503.</p><dl class="st-terms" aria-label="Terms in this passage"><div><dt>TC</dt><dd>Traffic Class</dd></div></dl></section>
<section id="pri"><h2>Page service returns to ATS</h2><p>After invalidation completes, the device queries 40001000h again and receives R=W=0. For this continuation, platform page management separately confirms that both 40001000h and 40002000h are non-resident and the Function has legitimate Read work. Page non-residence is an additional teaching assumption; R=W=0 alone does not establish its cause.</p><p>Under §10.4 request both pages using PASID 21h, R=1, W=0 and PRG (Page Request Group) Index 005h. Only the second Message has Last=1. PRG Response PASID Required=1 in this case, so the successful response must contain the same PASID.</p><figure class="diagram" id="pri-group-figure"><svg viewBox="0 0 900 570" style="min-width:720px" role="img" aria-labelledby="ch27-pri-en-t ch27-pri-en-d"><title id="ch27-pri-en-t">Two Page Requests, one group response, then a fresh translation</title><desc id="ch27-pri-en-d">PRG 5 has two Requests using PASID 21h. Last is set only on the second Request. Success returns both request credits, not a physical address.</desc><text x="130" y="35" text-anchor="middle" font-size="17">Endpoint: RID 0300h</text><path d="M130 65 V520" stroke="var(--line)" stroke-width="2"/><text x="770" y="35" text-anchor="middle" font-size="17">Host / TA</text><path d="M770 65 V520" stroke="var(--line)" stroke-width="2"/><text x="450" y="95" text-anchor="middle" font-size="16">Page 40001000h; PRG=005h; L=0</text><path d="M130 110 L770 145" stroke="var(--accent)" stroke-width="2"/><polygon points="770,145 760,140 760,150" fill="var(--accent)"/><text x="450" y="195" text-anchor="middle" font-size="16">Page 40002000h; PRG=005h; L=1</text><path d="M130 210 L770 245" stroke="var(--accent)" stroke-width="2"/><polygon points="770,245 760,240 760,250" fill="var(--accent)"/><text x="450" y="295" text-anchor="middle" font-size="16">PRG Response: Success; PRG=005h</text><path d="M770 310 L130 345" stroke="var(--accent)" stroke-width="2"/><polygon points="130,345 140,340 140,350" fill="var(--accent)"/><text x="450" y="390" text-anchor="middle" font-size="16">Fresh ATS Translation Request</text><path d="M130 405 L770 440" stroke="var(--accent)" stroke-width="2"/><polygon points="770,440 760,435 760,445" fill="var(--accent)"/><text x="450" y="470" text-anchor="middle" font-size="16">Translation Completion: new mapping</text><path d="M770 485 L130 520" stroke="var(--accent)" stroke-width="2"/><polygon points="130,520 140,515 140,525" fill="var(--accent)"/><text x="450" y="558" text-anchor="middle" font-size="16">Same PASID=00021h throughout this group; R=1, W=0.</text></svg><figcaption>Author-created sequence. PRI success precedes a new ATS query; only that query supplies the new translated address.</figcaption></figure><p>Page Request uses Code 04h, Route to Root Complex; PRG Response uses Code 05h, Route by ID. Both use TC0. Select Non-Flit Figures 10-23/10-27 or Flit Figures 10-24/10-28 for their page, index and response fields rather than treating them as Memory Completions.</p><p>Table 10-8 Success (0000b) means all group pages were made resident. It supplies no physical frame address. The case then issues fresh ATS; assume its new valid 4 KiB mapping has base A0000000h. Offset 234h now gives A0000234h, obtained from the new Translation Completion rather than the PRG Response.</p><p>There is no partial-success format for a group. Invalid Request (0001b) means an address/permission cannot be satisfied and retry cannot succeed without a mapping change. Response Failure (1111b) terminates the interface and needs recovery under its rules. Different PRGs have no completion-order guarantee.</p><p class="source-note">Base 6.0 §§10.4–10.4.2.2, Figures 10-23/10-24 and 10-27/10-28, Tables 10-6–10-8, pp.1505–1513.</p></section>
<section id="pri-credit"><h2>Reserve all messages before starting a group</h2><p>Allocation 3 permits three outstanding Page Requests, not three groups. Section 10.5.2.5 requires availability for the whole PRG before its first Request. Distinguish issued messages from reserved messages not yet transmitted:</p><div class="table-wrap"><table><thead><tr><th scope="col">Stage</th><th scope="col">Sent, not yet answered</th><th scope="col">Reserved, not yet sent</th><th scope="col">Free for new groups</th></tr></thead><tbody><tr data-pri-credit="initial"><td>Initial</td><td>0</td><td>0</td><td>3</td></tr><tr data-pri-credit="reserve"><td>Reserve entire group</td><td>0</td><td>2</td><td>1</td></tr><tr data-pri-credit="first"><td>First Page Request; L=0</td><td>1</td><td>1</td><td>1</td></tr><tr data-pri-credit="last"><td>Second Page Request; L=1</td><td>2</td><td>0</td><td>1</td></tr><tr data-pri-credit="reply"><td>One PRG Success response</td><td>0</td><td>0</td><td>3</td></tr></tbody></table></div><p>One group response returns two message allocations and releases the PRG Index. With only one free allocation, do not send the first half of a two-page group while waiting for more. These are not the Link Flow Control Credits in <a href="/DOCS/pcie-course/chapter-17.html">Chapter 17</a>.</p><p>Allocation is shared by all PASIDs of the Function. For SR-IOV, a PF/VF Page Request Interface may be shared while packets preserve the actual requesting Function's RID. VF ATS Enable can be controlled independently of the PF. Continue the scope reasoning in <a href="/DOCS/pcie-course/chapter-26.html">Chapter 26</a>.</p><p class="source-note">Base 6.0 §10.4, p.1506; §10.5.1, p.1513; §10.5.2, p.1516; §10.5.2.5 <em>Outstanding Page Request Allocation (Offset 0Ch)</em>, p.1520.</p></section>
<section id="pri-pasid-stop"><h2>What happens to outstanding requests when PASID 21h stops?</h2><p><strong>Teaching scenario:</strong> Reuse PASID 21h and the earlier two-page PRG, but both requests are sent, the final one has L=1, and its PRG Response has not yet arrived. Stopping this PASID does not mean the entire Page Request Interface has stopped.</p><p>Section 10.4.1.2 provides two paths. Both stop queuing new requests for 21h and finish any incomplete multi-page group, including its final L=1 request.</p><p>On a phone, scroll the table sideways to see all columns.</p><div class="table-wrap"><table><thead><tr><th>Path</th><th>Function action</th><th>Outstanding resources</th></tr></thead><tbody><tr><td>Without Stop Marker</td><td>Wait for outstanding PRG Responses for this PASID, then indicate stop using a device-specific mechanism that says no Marker will be generated.</td><td>Release the corresponding resources when responses arrive.</td></tr><tr><td>With Stop Marker</td><td>Mark outstanding requests stale, indicate stop with a device-specific mechanism, and send a Marker. The last two actions may occur in either order or in parallel.</td><td>Later old PRG Responses still return allocation credits and PRG Index values; their other contents are ignored.</td></tr></tbody></table></div><p>The Stop Marker marks the PASID boundary. Once the Host receives it, old Page Requests for that PASID have been delivered, and subsequent requests with that PASID belong to its new use. The Marker has no response, PRG Index, or Page Request Allocation charge. Sending it does not immediately return old requests' credits.</p><p>Other outstanding transactions and platform/device coordination also matter when stopping or reusing a PASID. Base 6.0 §10.4.1.2–§10.4.1.2.1 and §10.5.2.5, pp.1509–1510 and 1520.</p></section>
<section id="pri-stop-marker"><h2>How can a trace distinguish a Stop Marker?</h2><p>Identify the Page Request Message, then consult Figures 10-25 and 10-26. A Stop Marker has <code>L=1, W=0, R=0</code>, Marker Type <code>00000b</code>, TC0, and Relaxed Ordering=0. Non-Flit Mode uses a PASID Prefix; Flit Mode uses OHC-A1 with PASID.</p><p>These fields mark a stop boundary, not a request to load a page without read or write access. The untranslated address and upper PRG Index bits are Reserved; do not interpret them as a page address or group number.</p><p>Behavior is undefined, for example, when the Host has no matching PASID stop request or an incomplete group for that PASID has not sent its final L=1 request. Base 6.0 §10.4.1.2.1, Figures 10-25 and 10-26, pp.1509–1510.</p></section>
<section id="pri-response-check"><h2>What should be checked in a PRG Response?</h2><p>Use Figure 10-27 or 10-28 for the mode and destination Function, then match the PRG Index to an outstanding group. When a Page Request has a PASID, Status.PRG Response PASID Required determines whether the Response must carry it; incompatible formats can lead to undefined Function behavior.</p><p>If one request in a PRG carries a PASID, all requests in that PRG must carry the same PASID; inconsistent values have undefined behavior. A PASID Page Request with Execute Requested set must also set R; W=1 requires explicit write permission because the Host may mark the page dirty. When PRG Response PASID Required=0, Responses do not carry PASID and the Function shares PRG Index values across PASIDs.</p><p>Table 10-8 defines Response Code <code>0000b</code> as group Success, <code>0001b</code> as Invalid Request, unused <code>0010b–1110b</code> values as treated like Response Failure, and <code>1111b</code> as Response Failure. Failure terminates normal page-request service; later PRG Responses are ignored until re-enablement.</p><p>An otherwise error-free response with an unexpected PRG Index sets Unexpected Page Request Group Index (UPRGI). Success still requires a new ATS lookup to obtain a translation. Base 6.0 §10.4.1.1, §10.4.2–§10.4.2.2, Table 10-8, pp.1508 and 1511–1513.</p></section>
<section id="pri-interface-stop"><h2>How do Enable and Stopped describe stopping the interface?</h2><p>In an SR-IOV arrangement using one PF Page Request Interface shared with its VFs, the PF implements the capability and its VFs must not. Each Page Request still carries the actual PF or VF Requester ID, and the corresponding PRG Response targets that Function. Base 6.0 §10.5.2, p.1516.</p><p>This concerns the <strong>whole interface</strong>, not the Stop Marker for one PASID. Locate the structure in Figure 10-33 and read Control and Status in Figures 10-35 and 10-36 and Tables 10-14 and 10-15. In the Header (Figure 10-34), ID is 0013h, Version is 1, and Next Capability Offset in bits 31:20 is relative to Configuration Space.</p><p>On a phone, scroll the table sideways to see all columns.</p><div class="table-wrap"><table><thead><tr><th>Read or action</th><th>Interpretation</th></tr></thead><tbody><tr><td>Enable=1</td><td>Page Requests are allowed; Stopped is undefined.</td></tr><tr><td>Enable=0, Stopped=0</td><td>No new requests are issued, but transmitted or queued requests remain; stopping is not complete.</td></tr><tr><td>Enable=0, Stopped=1</td><td>The interface is disabled. Normal stop waits for requests, but interface Reset or Response Failure while stopping may also cause an immediate transition; inspect event history.</td></tr></tbody></table></div><p>Writing Reset=1 clears internal credit and pending-request state only when Enable is clear or cleared in the same write. With Enable still set it initiates no action. Re-enabling before successful stop has indeterminate results.</p><p>Status.Response Failure and UPRGI are bits 0 and 1, respectively, and are RW1C (write one to clear). Re-enabling the interface also clears these flags. When PF and VFs share an interface, these events from associated Functions are recorded in the PF.</p><p>Outstanding Page Request Capacity is the read-only limit; Allocation is set before enabling, must not change while Enable=1, and must not exceed Capacity. With Shadow Functions enabled, Allocation is shared by the main Function and enabled Shadows; stopping a PASID does not immediately return its allocated credits.</p><p>Base 6.0 §10.5.2.1–§10.5.2.5, Figures 10-33–10-36 and Tables 10-13–10-15, pp.1517–1520.</p></section>
<section id="reading"><h2>Build the next reading route from the packet type</h2><p>Confirm RID, PASID, mode and platform service, then each Support/Enable. Use Table 10-1 for AT, match Translation Completions to their original Requests, decode size and permissions, and only then form data access. Mapping changes add range, ITag Vector, CC and in-flight Transaction checks; Page Requests add PRG, Last, PASID, allocation and Response Code checks.</p><p>Stopping/reusing PASID also needs §6.20.1 and Chapter 10's rules for old Requests, Posted Writes, ATC entries and Page Requests. Reset and ATS Enable changing from 0 to 1 cause implicit invalidation too; a prior snapshot is not a current cache inventory.</p></section>
<section id="sources"><h2>Edition and source route</h2><p>PCI Express Base Specification Revision 6.0 (6.0-1.0-PUB) supplies the rules. Printed and PDF-viewer pages match. All topology, fields, mappings and traces are author-created; no hardware or platform page service was operated. No external website supplies technical claims.</p><details class="source-note"><summary>Sources by analysis step</summary><ul><li>Architecture: §10.1.1 <em>Address Translation Services (ATS) Overview</em>, pp.1470–1476; Figure 10-1 <em>Example Illustrating a Platform with TA, ATPT, and ATC Elements</em>, p.1470; Figure 10-2 <em>Example ATS Translation Request/Completion Exchange</em>, p.1471; §10.1.2 <em>Page Request Interface Extension</em>, pp.1476–1477; §10.1.3 <em>Process Address Space ID (PASID)</em>, pp.1477–1478.</li><li>PASID: §6.20 <em>PASID</em>, §6.20.1 <em>Managing PASID Usage</em>, §§6.20.2–6.20.2.2, pp.791–794; Figure 6-20/Table 6-15 <em>PASID TLP Prefix</em>, pp.792–793; §7.8.9 <em>PASID Extended Capability Structure</em>, Figures 7-185–7-188, Tables 7-159–7-161, pp.1148–1151.</li><li>Lookup: §10.2.1 <em>Memory Requests with Address Type</em>, Table 10-1 <em>Address Type (AT) Field Encodings</em>, pp.1478–1480; §10.2.2 <em>Translation Requests</em>, Figures 10-10–10-13, pp.1480–1483; §10.2.3 <em>Translation Completion</em>, Table 10-2, p.1484; Figure 10-14 <em>Translation Completion Data Entry</em>, Table 10-3 <em>Translation Completion Data Fields</em>, pp.1485–1487; §§10.2.3.1–10.2.3.5, pp.1487–1489; §10.2.4 <em>Completions with Multiple Translations</em>, p.1496.</li><li>Invalidation: Figures 10-4/10-5, pp.1474–1476; §§10.3–10.3.1 <em>ATS Invalidation / Invalidate Request</em>, Figures 10-18–10-20, pp.1497–1498; §10.3.2 <em>Invalidate Completion</em>, Figures 10-21/10-22, pp.1499–1500; §§10.3.3–10.3.8, pp.1501–1505.</li><li>Pages: §10.4 <em>Page Request Services</em>, §10.4.1 <em>Page Request Message</em>, Figures 10-23/10-24, Table 10-6, pp.1505–1508; §10.4.2 <em>Page Request Group Response Message</em>, Figures 10-27/10-28, Tables 10-7/10-8, pp.1511–1513.</li><li>Configuration: §10.5.1 <em>ATS Extended Capability</em>, Figures 10-29–10-32, Tables 10-9–10-11, pp.1513–1516; §10.5.2 <em>Page Request Extended Capability Structure</em>, Figures 10-33–10-36, Tables 10-13–10-15, pp.1516–1519; §§10.5.2.4–10.5.2.5, pp.1519–1520.</li><li>External boundaries: page-table formats, preparing/reclaiming memory, process-to-PASID mapping and recovery need actual platform/device documents. Translation or PRG success alone does not establish data-access completion or correct isolation policy.</li></ul></details></section>
</article>
<nav class="bottom-nav" aria-label="Course and editions"><a href="/DOCS/pcie-course/index.html">Course overview</a><a href="/DOCS/pcie-course/chapter-27.html">Full Chinese tutorial</a><a href="/pcie/chapter-27-zh-tw/">繁體中文</a></nav>
</div>
