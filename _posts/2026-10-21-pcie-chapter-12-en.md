---
layout: post
title: "PCIe Chapter 12: Error Evidence, Reporting, and Containment"
date: 2026-10-21 00:00:00 +0800
last_modified_at: 2026-10-28 00:00:00 +0800
permalink: /pcie/chapter-12-en/
categories: [PCIe]
tags: [PCIe, Specification]
lang: en
spec_teaching: true
spec_series: pcie
description: "沿 AER 紀錄連到 DPC，帶讀清中斷、等待 Link 停止、隔離中的讀取回覆與解除後恢復。"
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
<nav class="bottom-nav" aria-label="Course and editions"><a href="/DOCS/pcie-course/index.html">Course overview</a><a href="/DOCS/pcie-course/chapter-12.html">Full Chinese tutorial</a><a href="/pcie/chapter-12-zh-tw/">繁體中文</a></nav>
<article class="lesson">
<section id="chapter-overview"><h2>Preserve evidence along an error-reporting path</h2><figure class="diagram"><svg viewBox="0 0 900 500" role="img" aria-labelledby="ch12-guide-title ch12-guide-desc"><title id="ch12-guide-title">First follow normal reporting toward the root, then inspect the masked branch. DPC (Downstream Port Containment) is expanded separately. The reported identifier is a locator, not a complete physical-cause diagnosis.</title><desc id="ch12-guide-desc">First follow normal reporting toward the root, then inspect the masked branch. DPC (Downstream Port Containment) is expanded separately. The reported identifier is a locator, not a complete physical-cause diagnosis.</desc><g data-walk-target="status"><rect x="30" y="20" width="360" height="70" rx="9" fill="var(--surface-alt)" stroke="var(--line)" /><text x="210.0" y="45" text-anchor="middle" font-size="16">Source function: records error status</text></g><g data-walk-target="control"><rect x="30" y="170" width="360" height="75" rx="9" fill="var(--surface-alt)" stroke="var(--line)" /><text x="210.0" y="195" text-anchor="middle" font-size="16">Per-error mask and severity</text><text x="210.0" y="218" text-anchor="middle" font-size="16">and applicable reporting controls</text></g><g data-walk-target="record"><path d="M210 90 L210 170" fill="none" stroke="var(--accent)" stroke-width="2" /><polygon points="210.0,170.0 215.0,160.0 205.0,160.0" fill="var(--accent)" /></g><g data-walk-target="root"><rect x="510" y="170" width="360" height="75" rx="9" fill="var(--surface-alt)" stroke="var(--line)" /><text x="690.0" y="195" text-anchor="middle" font-size="16">Root: notification and source records</text></g><g data-walk-target="message"><path d="M390 210 L510 210" fill="none" stroke="var(--accent)" stroke-width="2" /><polygon points="510.0,210.0 500.0,205.0 500.0,215.0" fill="var(--accent)" /><text x="450.0" y="201.0" text-anchor="middle" font-size="16">Error Message →</text></g><g data-walk-target="save"><rect x="510" y="355" width="360" height="85" rx="9" fill="var(--surface-alt)" stroke="var(--line)" /><text x="690.0" y="380" text-anchor="middle" font-size="16">Software preserves evidence at both ends</text><text x="690.0" y="403" text-anchor="middle" font-size="16">Check validity and event correlation</text></g><g data-walk-target="notify"><path d="M690 245 L690 355" fill="none" stroke="var(--accent)" stroke-width="2" /><polygon points="690.0,355.0 695.0,345.0 685.0,345.0" fill="var(--accent)" /></g><g data-walk-target="masked"><rect x="30" y="355" width="360" height="85" rx="9" fill="var(--surface-alt)" stroke="var(--line)" /><text x="210.0" y="380" text-anchor="middle" font-size="16">Status may remain without a message</text><text x="210.0" y="403" text-anchor="middle" font-size="16">Log updates follow their specific rules</text></g><g data-walk-target="mask-path"><path d="M210 245 L210 355" fill="none" stroke="var(--accent)" stroke-width="2" /><polygon points="210.0,355.0 215.0,345.0 205.0,345.0" fill="var(--accent)" /><text x="210.0" y="291.0" text-anchor="middle" font-size="16">The masked error in this example</text></g></svg><figcaption>First follow normal reporting toward the root, then inspect the masked branch. DPC (Downstream Port Containment) is expanded separately. The reported identifier is a locator, not a complete physical-cause diagnosis.</figcaption></figure><p class="lead">AER (Advanced Error Reporting) supplies error status, reporting controls and related records. Follow normal error reporting before comparing masked errors and DPC containment. Chapter 5 provides transaction context and Chapter 7 provides notification context.</p><dl class="st-terms" aria-label="Terms in this passage"><div><dt>DPC</dt><dd>Downstream Port Containment</dd></div></dl><p><strong>Specification route:</strong> Classification in Figure 6-1 → status, mask and severity → reporting in Figure 6-3 → root records → preservation and clearing → DPC.</p></section>
<p class="lead">PCIe error analysis connects detection, reporting, reception, and containment. Status does not prove that a message arrived; Source ID identifies a reporter rather than the physical root cause. Two separate AER and DPC examples show how to respect those boundaries.</p><dl class="st-terms" aria-label="Terms in this passage"><div><dt>AER</dt><dd>Advanced Error Reporting</dd></div></dl><aside class="note"><strong>Version and assumptions</strong><p>Based on PCIe Base 6.0. All values and event sequences are author-created, using ordinary non-SR-IOV Functions. The AER example supports neither Flit Mode nor End-End TLP Prefixes and has DPC disabled. The later DPC example is a separate event. The manager has appropriate ownership, and no unspecified concurrent events occur.</p><dl class="st-terms" aria-label="Terms in this passage"><div><dt>TLP</dt><dd>Transaction Layer Packet</dd></div></dl></aside>
<section id="model"><h2>Connect evidence from the Function to the Root</h2><p>Correctable Errors can be recovered by the protocol but may affect performance. Uncorrectable Errors affect functionality and are classified Non-Fatal or Fatal. Non-Fatal does not establish successful work, and Fatal does not directly diagnose a failed chip. AER adds detailed status, masks, severity, and logs to baseline reporting; absence of AER does not imply absence of all reporting.</p><p>Inspect source Status, the Mask/Severity/Device Control settings at detection, valid Header Logs, and then Root Error Status/Source ID. Check DPC separately if containment is possible. Later configuration reads do not automatically reconstruct earlier settings. Sources: §6.2.1–§6.2.4 (pp.669–679), Figure 6-1 (p.670).</p></section>
<section id="aer"><h2>Two status bits, one unmasked error</h2><p>Traverse Extended Capabilities on 03:00.0 and use Figure 7-154 to identify AER ID=0x0001. This example has base=0x100, Version=2, Next=0; Base 6.0 does not imply this Function implements all Flit features. Earlier records were cleared, settings remained unchanged, and forwarding along the path is enabled.</p><div class="table-wrap"><table><caption>Source Function reads</caption><thead><tr><th scope="col">Register / offset</th><th scope="col">Value</th><th scope="col">Interpretation</th></tr></thead><tbody><tr><td>Header / 0x100</td><td>0x00020001</td><td>AER, Version 2.</td></tr><tr><td>Uncorrectable Status / 0x104</td><td>0x00044000</td><td>Completion Timeout bit 14; Malformed TLP bit 18.</td></tr><tr><td>Mask / 0x108</td><td>0x00040000</td><td>Masks the recorded Malformed TLP error.</td></tr><tr><td>Severity / 0x10C</td><td>0x00040000</td><td>Non-Fatal Timeout; Fatal Malformed TLP.</td></tr><tr><td>AER Capabilities and Control / 0x118</td><td>0x0000100E</td><td>FEP=14; Timeout Header Log Capable=1.</td></tr><tr><td>Device Control / 0x78, 16 bits</td><td>0x2816</td><td>Non-Fatal and Fatal Reporting Enables set.</td></tr></tbody></table><dl class="st-terms" aria-label="Terms in this passage"><div><dt>TLP</dt><dd>Transaction Layer Packet</dd></div></dl></div>
<p><code>0x00044000 &amp; ~0x00040000 = 0x00004000</code>: only the recorded Timeout is unmasked. A masked error can set Status but does not generate its Error Message or update the Header Log, TLP Prefix Log, or FEP. Fatal severity does not override masking. Under these assumptions, Timeout produces ERR_NONFATAL according to Severity and Device Control. These are configured values, not reset defaults.</p><p>The complete path also includes Bridge forwarding, Root primary-interface transmission controls, and interrupt conditions. Follow Figure 6-3 through the path. Unsupported Request and Advisory Non-Fatal errors have additional rules; the example's arithmetic is not a general reporting algorithm.</p><details class="source-note"><summary>Fields and reporting</summary><p>Figures 7-154–7-157/Tables 7-134–7-137 (pp.1112–1117); Figure 7-25/Table 7-21 (pp.958–962); §6.2.3.2.2 (p.673), §6.2.6/Figure 6-3 (pp.683–685), §6.2.8.1 (p.692).</p></details></section>
<section id="log"><h2>Validate the log before decoding the transaction</h2><p>FEP=14 is valid because Status bit 14 is set. Completion Timeout Header Log Capable bit 12 supports recording the timed-out Request. Multiple Header Recording bits 9 and 10 are clear; there is no Flit or Prefix support. The example has four DWORDs of log capacity but uses a three-DWORD Header.</p><div class="table-wrap"><table><caption>Request Header associated with the Timeout</caption><thead><tr><th scope="col">Offset</th><th scope="col">DWORD value</th><th scope="col">Content</th></tr></thead><tbody><tr><td>0x11C</td><td>0x00000040</td><td>3 DW Memory Read, Length=64 DW.</td></tr><tr><td>0x120</td><td>0x030013FF</td><td>Requester=0x0300, Tag=0x13, both Byte Enables=0xF.</td></tr><tr><td>0x124</td><td>0x40001000</td><td>Starting address.</td></tr><tr><td>0x128</td><td>Not interpreted</td><td>The fourth DWORD is undefined for this 12-byte Header.</td></tr></tbody></table><dl class="st-terms" aria-label="Terms in this passage"><div><dt>DW</dt><dd>Double Word, a four-byte unit</dd></div></dl></div><p>The Request covers 0x40001000–0x400010FF, or 256 bytes. It is the Request that did not complete in time, not a timed-out Completion. Figure 7-161 places Header byte 0 at bits 31:24 for DWORD reads; do not reverse these values again. Flit logs require Logged TLP was Flit Mode, Header Log Size, Logged TLP Size, and Type/OHC interpretation.</p><dl class="st-terms" aria-label="Terms in this passage"><div><dt>OHC</dt><dd>Orthogonal Header Content</dd></div></dl><p>This locates a transaction and its timeout, not the responsible Endpoint, Completer, Link, or platform component. It cannot be assigned to the masked Malformed TLP event, which did not create this log.</p><details class="source-note"><summary>Validity and format</summary><p>§6.2.4.2 (pp.679–680); Figures 7-160/7-161, Tables 7-140/7-141 (pp.1121–1123). Memory Requests: <a href="/pcie/chapter-5-en/">Chapter 5</a>.</p></details></section>
<section id="root"><h2>The Root Source ID identifies the first reporter</h2><div class="table-wrap"><table><caption>Root Port snapshot for the same AER example</caption><thead><tr><th scope="col">Root AER base=0x100</th><th scope="col">Value</th><th scope="col">Meaning</th></tr></thead><tbody><tr><td>Root Error Command / 0x12C</td><td>0x00000002</td><td>Non-Fatal interrupt reporting enabled.</td></tr><tr><td>Root Error Status / 0x130</td><td>0x00000024</td><td>Uncorrectable Received and Non-Fatal Received.</td></tr><tr><td>Error Source ID / 0x134</td><td>0x03000000</td><td>Upper 16 bits=0x0300, or 03:00.0.</td></tr></tbody></table></div><p>The Root interrupt message number is 0 and primary-interface transmission conditions are satisfied. Source ID identifies the Endpoint reporting Timeout, not the physical cause. A second message in the same category sets Multiple without replacing the first Source ID.</p><p>Root Status updates independently of Root Error Command/Root Control, but still requires applicable primary-interface transmission enables. CPU interrupt delivery additionally requires vector and routing evidence. Sources: Figures 7-162–7-164/Tables 7-142–7-144 (pp.1123–1127).</p></section>
<section id="preserve"><h2>Preserve correlated records before clearing</h2><p>The author recommends saving status, configuration, FEP, valid logs, and Root/DPC evidence while checking for concurrency. Separate register reads are not automatically an atomic snapshot. Clearing the status indicated by FEP can advance hardware to another log, destroying the original association if done before capture.</p><p>With Multiple Header Recording enabled and valid FEP, the specification recommends processing records through FEP rather than clearing unrelated status; it lists an exception for masked errors known to lack recorded headers. PCI Status and AER Status are also cleared independently. Sources: §6.2.4.2 (pp.679–681, footnote 108), §6.2.7.1 (p.691).</p></section>
<section id="dpc"><h2>DPC can contain the error before its original message reaches the Root</h2><p>Now consider a separate event on Switch Downstream Port 02:01.0, with DPC base=0x300 and no RP Extensions.</p><div class="table-wrap"><table><caption>Separate DPC example</caption><thead><tr><th scope="col">Field / offset</th><th scope="col">Value</th><th scope="col">Meaning</th></tr></thead><tbody><tr><td>Header / 0x300</td><td>0x0001001D</td><td>ID=0x001D, Version=1.</td></tr><tr><td>Control / 0x306, 16 bits</td><td>0x000A</td><td>Trigger Enable=10b; Interrupt Enable=1.</td></tr><tr><td>Status / 0x308, 16 bits</td><td>0x000B</td><td>Triggered, Reason=01b, Interrupt Status=1.</td></tr><tr><td>Error Source ID / 0x30A, 16 bits</td><td>0x0300</td><td>The triggering ERR_NONFATAL came from 03:00.0.</td></tr></tbody></table></div>
<p>Enable=10b triggers on a local unmasked Uncorrectable Error or a received ERR_NONFATAL/ERR_FATAL. Reason=01b makes Source ID meaningful here; Reason=00b would not. The triggering message is discarded at the Port rather than forwarded to the Root. This example enables DPC interrupts but not DPC ERR_COR, so the earlier Root value 0x24 is not an expected companion snapshot.</p><h3 id="dpc-release">Why does the Link remain down after acknowledging the interrupt?</h3>
<p>Figure 7-300 places DPC Trigger Status in bit 0 and DPC Interrupt Status in bit 3. Both clear on a write of 1, but they have different effects: bit 3 handles interrupt status; bit 0 keeps containment active. Clearing bit 0 permits the Link Training and Status State Machine (LTSSM) to leave Disabled and return to Detect to attempt Link establishment.</p>
<div class="example"><p><strong>Simulated data: this teaching scenario does not represent a particular device or platform.</strong> Continue the separate DPC event above: 02:01.0 received ERR_NONFATAL from 03:00.0 and DPC Status reads <code>0x000B</code>. This example saves evidence, clears only interrupt status, and then waits for containment-release conditions. The upstream management path to the Switch remains available; the disabled Link is the one from 02:01.0 to 03:00.0. No new DPC event or concurrent software write occurs.</p>
<div class="table-wrap"><table><caption>Two writes to the same DPC Status register handle notification and containment separately</caption><thead><tr><th scope="col">Action and location</th><th scope="col">DPC Interrupt Status, bit 3</th><th scope="col">DPC Trigger Status, bit 0</th><th scope="col">Result</th></tr></thead><tbody><tr><td>Read 0x308: 0x000B</td><td>1</td><td>1</td><td>Interrupt and containment are recorded; Reason=01b.</td></tr><tr><td>After saving evidence, write 0x0008 to 0x308 using 16 bits</td><td>Clears to 0</td><td>Remains 1</td><td>The example reads 0x0003; the Port remains in DPC.</td></tr><tr><td>After release conditions are met, write 0x0001 to 0x308 using 16 bits</td><td>Remains 0 here</td><td>Clears to 0</td><td>Return to Detect; Reason is invalid, so no fixed whole-register readback is specified.</td></tr></tbody></table></div>
<p>Splitting the writes makes their effects visible; the specification does not require every software implementation to use this sequence. The release conditions are mandatory. <strong>Writing the read value <code>0x000B</code> back is not an interrupt-only acknowledgment:</strong> it writes 1 to both bit 3 and bit 0, releasing containment as well.</p>
<p>The waiting branch below follows §6.2.11: software must observe Data Link Layer Link Active=0 in Link Status before releasing DPC. Releasing it earlier has undefined results. DPC RP Busy is Reserved on this Switch Downstream Port; a Root Port supporting RP Extensions must additionally wait for that bit to read 0.</p>
<figure class="diagram"><svg viewBox="0 0 820 675" style="min-width: 640px" role="img" aria-labelledby="dpc-release-title dpc-release-desc"><title id="dpc-release-title">Acknowledge the DPC interrupt, wait for Link inactivity, then release containment</title><desc id="dpc-release-desc">The example preserves evidence, clears Interrupt Status only, and keeps Trigger Status set while Link Active remains one. Once Link Active reads zero and software chooses recovery, software clears Trigger Status. Detect and Link training follow; device recovery is a later step.</desc><rect x="20" y="20" width="490" height="80" rx="10" fill="var(--blue-soft)" stroke="var(--line)"/><text x="265" y="52" text-anchor="middle" font-size="17">Save DPC status and associated evidence</text><text x="265" y="80" text-anchor="middle" font-size="17">Switch Downstream Port 02:01.0</text><path d="M265 100 V145 M259 135 L265 145 L271 135" fill="none" stroke="var(--accent)" stroke-width="2.5"/><rect x="20" y="145" width="490" height="85" rx="10" fill="var(--blue-soft)" stroke="var(--line)"/><text x="265" y="179.5" text-anchor="middle" font-size="17">Write 0x0008 to DPC Status</text><text x="265" y="207.5" text-anchor="middle" font-size="17">Interrupt Status=0; Trigger Status stays 1</text><path d="M265 230 V285 M259 275 L265 285 L271 275" fill="none" stroke="var(--accent)" stroke-width="2.5"/><path d="M265 285 L510 327.5 L265 370 L20 327.5 Z" fill="var(--blue-soft)" stroke="var(--line)"/><text x="265" y="319.5" text-anchor="middle" font-size="17">Read Link Active</text><text x="265" y="347.5" text-anchor="middle" font-size="17">Is it 0 or 1?</text><path d="M265 370 V425 M259 415 L265 425 L271 415" fill="none" stroke="var(--accent)" stroke-width="2.5"/><rect x="20" y="425" width="490" height="85" rx="10" fill="var(--blue-soft)" stroke="var(--line)"/><text x="265" y="459.5" text-anchor="middle" font-size="17">Write 0x0001 to DPC Status</text><text x="265" y="487.5" text-anchor="middle" font-size="17">Trigger Status clears; LTSSM goes to Detect</text><path d="M265 510 V565 M259 555 L265 565 L271 555" fill="none" stroke="var(--accent)" stroke-width="2.5"/><rect x="20" y="565" width="490" height="85" rx="10" fill="var(--blue-soft)" stroke="var(--line)"/><text x="265" y="599.5" text-anchor="middle" font-size="17">Observe Link training and readiness</text><text x="265" y="627.5" text-anchor="middle" font-size="17">Then restore configuration and device service</text><rect x="550" y="280" width="250" height="105" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><path d="M510 327 H550 M540 321 L550 327 L540 333 M675 280 V252 H265 V285 M259 275 L265 285 L271 275" fill="none" stroke="var(--accent)" stroke-width="2.5"/><text x="675" y="307" text-anchor="middle" font-size="17">Link Active=1</text><text x="675" y="335" text-anchor="middle" font-size="17">Keep Trigger Status=1</text><text x="675" y="363" text-anchor="middle" font-size="17">Wait and read again</text><text x="375" y="405" text-anchor="middle" font-size="16">0; recovery selected</text><text x="529" y="315" text-anchor="middle" font-size="16">1</text></svg><figcaption>Author-created software flow for this Switch Port, not an LTSSM state diagram. The right branch waits; only the downward branch releases containment. Root Ports with RP Extensions additionally require DPC RP Busy=0.</figcaption></figure><dl class="st-terms" aria-label="Terms in this passage"><div><dt>LTSSM</dt><dd>Link Training and Status State Machine</dd></div></dl>
</div>
<h3>Who responds to a new Memory Read during containment?</h3>
<p>Follow §2.9.3, <em>Transaction Layer Behavior During Downstream Port Containment</em>. Assume the Root Complex sends a new, valid Memory Read targeting a BAR in 03:00.0 through 02:01.0. It is submitted for downstream transmission after the Port is already in DPC. The Port discards this Request and generates an error Completion.</p><dl class="st-terms" aria-label="Terms in this passage"><div><dt>BAR</dt><dd>Base Address Register</dd></div></dl>
<p>Figure 7-299 and Table 7-263 determine the status: DPC Control=<code>0x000A</code> has DPC Completion Control, bit 2, cleared, so the response is <strong>Completer Abort (CA)</strong>. Setting that bit instead selects Unsupported Request (UR). The Completion's Completer ID identifies Downstream Port 02:01.0, which terminates this Request. The earlier DPC Error Source ID of 03:00.0 identifies the sender of the message that triggered containment.</p>
<p>CA in this scenario comes from the Port's DPC handling; it does not establish that the Endpoint accepted or executed the read. A Request transmitted before containment, whose Completion is prevented from returning by DPC, is a different case. Without the Root Port Extensions completion-synthesis mechanism in this example, its Requester may encounter Completion Timeout. Track termination of the new Request separately from completion of earlier work.</p>
<h3>What remains after containment is released?</h3>
<p>Table 7-264 requires the Port to leave DPC and the LTSSM to transition to Detect when DPC Trigger Status clears. Training is only being attempted. Software still observes Link and Data Link recovery, honors the applicable §6.6.1 timing for the first Configuration Read following Conventional Reset, and restores configuration and driver operation. <a href="/pcie/chapter-9-en/">Chapter 9</a> covers the reset and readiness conditions.</p>
<p>Release changes log interpretation too: DPC Trigger Reason is invalid when DPC Trigger Status is clear, so analyze this event using the saved snapshot. Once release requirements are met, the specification permits clearing Trigger Status regardless of other status bits associated with the triggering event. Clearing every error record is therefore not a prerequisite for release. Rebuilding device work, resolving earlier outstanding data and restoring application service still require device, driver and platform recovery procedures.</p>
<details class="source-note"><summary>Reading path: fields, contained transactions and release conditions</summary><p>PCI Express Base Specification Revision 6.0: Figure 7-300 <em>DPC Status Register</em>/Table 7-264, §7.9.14.4 (PDF/printed pp.1252–1253), locates Trigger Status, Interrupt Status, Reason validity and applicable RP Busy. Section 6.2.11 <em>Downstream Port Containment (DPC)</em> (p.694) requires Link Active=0 before release; §6.2.11.1 <em>DPC Interrupts</em> (p.697) gives interrupt conditions. During containment, use §2.9.3 <em>Transaction Layer Behavior During Downstream Port Containment</em> (p.262), then Figure 7-299 <em>DPC Control Register</em>/Table 7-263, §7.9.14.3 (pp.1250–1251), for DPC Completion Control. Source interpretation uses Figure 7-301/Table 7-265, §7.9.14.5 <em>DPC Error Source ID Register</em> (pp.1253–1254). First configuration access after release follows §6.6.1 <em>Conventional Reset</em> (pp.721–723). PDF and printed page numbers match here. The software sequence is an author-created demonstration.</p></details>
</section>
<section id="questions"><h2>Check the evidence limits</h2><details class="question"><summary>Can FEP=14 identify the latest Timeout when Status bit 14 is clear?</summary><p>No. FEP is invalid; a nonzero log cannot replace the validity condition. Source: §6.2.4.2.</p></details><details class="question"><summary>Does Status=0 prove an error never occurred?</summary><p>No. Status may have been cleared or reset, and detection and implementation conditions also matter. Sources: §6.2.4.2, Table 7-135.</p></details></section>
</article>
<nav class="bottom-nav" aria-label="Course and editions"><a href="/DOCS/pcie-course/index.html">Course overview</a><a href="/DOCS/pcie-course/chapter-12.html">Full Chinese tutorial</a><a href="/pcie/chapter-12-zh-tw/">繁體中文</a></nav>
</div>
