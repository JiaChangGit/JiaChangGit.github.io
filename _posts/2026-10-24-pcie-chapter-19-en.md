---
layout: post
title: "PCIe Chapter 19: LTSSM, Equalization, and Retimers"
date: 2026-10-24 00:00:00 +0800
last_modified_at: 2026-10-29 00:00:00 +0800
permalink: /pcie/chapter-19-en/
categories: [PCIe]
tags: [PCIe, Specification]
lang: en
spec_teaching: true
spec_series: pcie
description: "Link 還沒到正常傳送狀態，應該追哪個階段？"
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
<nav class="bottom-nav" aria-label="Course and editions"><a href="/DOCS/pcie-course/index.html">Course overview</a><a href="/DOCS/pcie-course/chapter-19.html">Full Chinese tutorial</a><a href="/pcie/chapter-19-zh-tw/">繁體中文</a></nav>
<article class="lesson">
<p>The LTSSM (Link Training and Status State Machine) describes Link detection, training, and operation. First follow the normal path, then connect a Polling case to received/transmitted sequences, counts, and timeouts. Retimers and speed changes follow their own applicable conditions.</p><figure class="diagram"><svg viewBox="0 0 900 430" style="min-width:640px" role="img" aria-labelledby="ch19-en-t ch19-en-d"><title id="ch19-en-t">LTSSM training and return to L0</title><desc id="ch19-en-d">A selected initial-training path and the L0 to Recovery to L0 path. Other branches are omitted.</desc><g data-walk-target="detect"><rect x="20" y="35" width="190" height="74" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="115.0" y="64" text-anchor="middle" font-size="16">Detect</text><text x="115.0" y="88" text-anchor="middle" font-size="16">Far-end termination</text></g><g data-walk-target="poll"><rect x="300" y="35" width="250" height="74" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="425.0" y="64" text-anchor="middle" font-size="16">Polling</text><text x="425.0" y="88" text-anchor="middle" font-size="16">Training sequences</text></g><g data-walk-target="config"><rect x="630" y="35" width="250" height="74" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="755.0" y="64" text-anchor="middle" font-size="16">Configuration</text><text x="755.0" y="88" text-anchor="middle" font-size="16">Lane / width negotiation</text></g><g data-walk-target="recovery"><rect x="220" y="290" width="310" height="74" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="375.0" y="319" text-anchor="middle" font-size="16">Recovery</text><text x="375.0" y="343" text-anchor="middle" font-size="16">Lock / alignment / rate</text></g><g data-walk-target="l0"><rect x="630" y="290" width="250" height="74" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="755.0" y="319" text-anchor="middle" font-size="16">L0: normal operation</text><text x="755.0" y="343" text-anchor="middle" font-size="16"></text></g><g data-walk-target="a"><path d="M210 72 H300" fill="none" stroke="var(--accent)" stroke-width="2"/><polygon points="300,72 290,67 290,77" fill="var(--accent)"/><text x="255" y="60" text-anchor="middle" font-size="16"></text></g><g data-walk-target="b"><path d="M550 72 H630" fill="none" stroke="var(--accent)" stroke-width="2"/><polygon points="630,72 620,67 620,77" fill="var(--accent)"/><text x="590" y="60" text-anchor="middle" font-size="16"></text></g><g data-walk-target="c"><path d="M755 109 V290" fill="none" stroke="var(--accent)" stroke-width="2"/><polygon points="755,290 750,280 760,280" fill="var(--accent)"/><text x="805" y="205" text-anchor="middle" font-size="16">Training done</text></g><g data-walk-target="d"><path d="M630 315 H530" fill="none" stroke="var(--accent)" stroke-width="2"/><polygon points="530,315 540,310 540,320" fill="var(--accent)"/><text x="580" y="300" text-anchor="middle" font-size="16">Trigger</text></g><g data-walk-target="e"><path d="M530 347 H630" fill="none" stroke="var(--accent)" stroke-width="2"/><polygon points="630,347 620,342 620,352" fill="var(--accent)"/><text x="580" y="378" text-anchor="middle" font-size="16">Resume</text></g></svg><figcaption><p>Selected main-state paths based on Figure 4-48; the illustrated Recovery exit returns to L0. Other exits remain possible. Arrows do not replace substate receive, count, and timeout rules, or establish final Data Link / Transaction success.</p></figcaption></figure>
<section id="route"><h2>Find the state, then its transition rules</h2><p>For an LTSSM (Link Training and Status State Machine) log, establish the Port, Link, direction, and time first. Figure 4-48 locates the main state; §4.2.6 explains its task; §4.2.7 supplies substate actions, receive conditions, and timeouts. Read them together.</p><p>This chapter works through Polling during initial Link establishment. Use Figure 4-49 for entry after Receiver Detection (far-end termination detection), then Figure 4-50 for Polling.Active and Polling.Configuration. Later sections connect speed changes, equalization, and Retimers to the observations needed for each situation.</p><p class="source-note">Base 6.0 §4.2.6 <em>Link Training and Status State Machine (LTSSM) Descriptions</em> (pp.444–452); §4.2.7 <em>Link Training and Status State Rules</em>; Figure 4-48 <em>Main State Diagram for Link Training and Status State Machine</em> (pp.452–454); Figures 4-49 <em>Detect Substate Machine</em> (p.456) and 4-50 <em>Polling Substate Machine</em> (p.464).</p></section>

<section id="polling-gates"><h2>What remains after seeing a valid TS1 or TS2?</h2><p><strong>One valid sequence is one successful reception. Transition rules also depend on consecutive reception, transmission counts, and the Lane set.</strong> TS1 and TS2 are Training Sequence Ordered Sets. Each end transmits its own sequences and independently checks received content.</p><div class="example"><p><strong>Simulated data:</strong> Author-created teaching data, not a hardware or platform measurement. Root Port 00:01.0 connects directly to Endpoint 01:00.0, with no Retimer. Observe the Root Port's LTSSM and transmit/receive records during initial 2.5 GT/s, 8b/10b training. Detect found receivers on two candidate Lanes. Labels A and B mean paired capture channels; Configuration has not yet assigned Logical Lane Numbers.</p><p>Assume Enter Compliance=0, no Loopback or compliance-test request, and no polarity inversion. Received TS1s use PAD Link/Lane numbers and Compliance Receive=0. PAD is the placeholder used before assigning numbers, not Lane 0. All observations below occur before their substate timeout expires.</p><h3>First check both local transmission and per-Lane reception</h3><p>In Polling.Active the Root Port sends TS1. The normal transition on p.457 requires at least 1024 transmitted TS1 Ordered Sets and eight consecutive qualifying training sequences on every Lane that detected a receiver during Detect. The transmission count is local; receive conditions apply per Lane. Do not add opposite-direction counts together.</p><div class="table-wrap"><table><thead><tr><th scope="col">Point in one Polling.Active entry</th><th scope="col">Local TS1 sent</th><th scope="col">Lane A qualifying run</th><th scope="col">Lane B qualifying run</th><th scope="col">Next state on the selected normal path</th></tr></thead><tbody><tr data-polling-stage="active-early"><td>A0</td><td>1000</td><td>8</td><td>7</td><td>Polling.Active</td></tr><tr data-polling-stage="active-tx"><td>A1</td><td>1023</td><td>31</td><td>30</td><td>Polling.Active</td></tr><tr data-polling-stage="active-ready"><td>A2</td><td>1024</td><td>32</td><td>31</td><td>Polling.Configuration</td></tr></tbody></table></div><p>A0 lacks both complete conditions. At A1 both receive runs are sufficient, but local transmission is one TS1 short. A2 meets both. These are counts reconstructed from a complete tool record, not mandated public Configuration registers.</p><h3>Polling.Configuration uses a new transmit-count origin</h3><p>The Root Port now sends TS2 with PAD Link/Lane numbers. Section 4.2.7.2.3 requires eight consecutive TS2s on a Lane that detected a receiver, plus <strong>16 transmitted TS2s after receiving one TS2</strong>, before entering Configuration. Both candidate Lanes meet the receive condition here; next compare the transmit count using the required origin.</p><div class="table-wrap"><table><thead><tr><th scope="col">Point in one Polling.Configuration entry</th><th scope="col">Sent before first received TS2</th><th scope="col">Sent after first received TS2</th><th scope="col">Local TS2 total</th><th scope="col">Lane A / B consecutive TS2</th><th scope="col">Next state</th></tr></thead><tbody><tr data-polling-stage="config-wait"><td>B0</td><td>6</td><td>15</td><td>21</td><td>8 / 8</td><td>Polling.Configuration</td></tr><tr data-polling-stage="config-ready"><td>B1</td><td>6</td><td>16</td><td>22</td><td>9 / 9</td><td>Configuration</td></tr></tbody></table></div><p>The total of 21 at B0 includes only 15 after the required origin. B1 reaches 16. A tool summary saying “21 TS2s sent” therefore needs the location of the first received TS2 before this rule can be evaluated.</p><figure class="diagram"><svg viewBox="0 0 900 690" style="min-width:640px" role="img" aria-labelledby="polling-gates-title polling-gates-desc"><title id="polling-gates-title">Polling conditions for the normal path</title><desc id="polling-gates-desc">Waiting loops apply before the timeout; timeout branches are explained in the table.</desc><rect x="260" y="35" width="380" height="60" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="450" y="73" text-anchor="middle" font-size="20">Polling.Active</text><rect x="260" y="300" width="380" height="60" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="450" y="338" text-anchor="middle" font-size="20">Polling.Configuration</text><rect x="260" y="610" width="380" height="60" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="450" y="648" text-anchor="middle" font-size="20">Configuration</text><polygon points="450,120 635,190 450,260 265,190" fill="var(--surface-alt)" stroke="var(--line)"/><text x="450" y="182" text-anchor="middle" font-size="16">Sent ≥1024 TS1 and all detected</text><text x="450" y="208" text-anchor="middle" font-size="16">Lanes meet consecutive receive rules?</text><path d="M635 190 H790 V65 H640" fill="none" stroke="var(--accent)" stroke-width="2"/><polygon points="640,65 650,60 650,70" fill="var(--accent)"/><text x="710" y="230" text-anchor="middle" font-size="16">No: keep sending TS1</text><polygon points="450,420 635,490 450,560 265,490" fill="var(--surface-alt)" stroke="var(--line)"/><text x="450" y="482" text-anchor="middle" font-size="16">Received eight consecutive TS2</text><text x="450" y="508" text-anchor="middle" font-size="16">and sent 16 after the first TS2?</text><path d="M635 490 H790 V330 H640" fill="none" stroke="var(--accent)" stroke-width="2"/><polygon points="640,330 650,325 650,335" fill="var(--accent)"/><text x="710" y="530" text-anchor="middle" font-size="16">No: keep sending TS2</text><path d="M450 95 V120" fill="none" stroke="var(--accent)" stroke-width="2"/><polygon points="450,120 445,110 455,110" fill="var(--accent)"/><path d="M450 260 V300" fill="none" stroke="var(--accent)" stroke-width="2"/><polygon points="450,300 445,290 455,290" fill="var(--accent)"/><path d="M450 360 V420" fill="none" stroke="var(--accent)" stroke-width="2"/><polygon points="450,420 445,410 455,410" fill="var(--accent)"/><path d="M450 560 V610" fill="none" stroke="var(--accent)" stroke-width="2"/><polygon points="450,610 445,600 455,600" fill="var(--accent)"/><text x="475" y="286" font-size="16">Yes</text><text x="475" y="593" font-size="16">Yes</text></svg><figcaption>Author-drawn normal-path conditions. Waiting loops apply only before timeout. The Active receive test uses the case's selected sequence conditions; consult §4.2.7.2.1 for all accepted sequences and timeout branches. This is not the full LTSSM.</figcaption></figure><h3>Configuration still has work to do</h3><p>B1 advances this Port only to Configuration. Linkwidth and Lanenum substates in Figure 4-51 (p.482) must establish Link Number, Logical Lane Numbers, and width, followed by the remaining training before L0. Passing Polling on two candidate Lanes alone does not fix the final width at x2. See <a href="/DOCS/pcie-course/chapter-8.html">Chapter 8</a> for capability versus result and <a href="/DOCS/pcie-course/chapter-17.html#initialization">Chapter 17</a> for Data Link and Flow Control initialization after Physical Link establishment.</p></div><p class="source-note">Base 6.0 §4.2.7.1.2 <em>Detect.Active</em> (p.456); §4.2.7.2.1 <em>Polling.Active</em> (pp.457–458); §§4.2.7.2.3 <em>Polling.Configuration</em> and 4.2.7.2.4 <em>Polling.Speed</em> (p.463); Figure 4-50 (p.464); §4.2.7.3 <em>Configuration</em> (p.464 onward).</p></section>

<section id="timeouts"><h2>A timeout does not always mean a return to Detect</h2><p>The preceding case takes normal transitions. A stalled Link requires the timeout rules for the specific substate.</p><div class="table-wrap"><table><thead><tr><th scope="col">Location</th><th scope="col">Specified condition</th><th scope="col">Next evidence to inspect</th></tr></thead><tbody><tr><td>Detect.Active with receivers on some but not all Lanes</td><td>Wait 12 ms and perform Receiver Detection again</td><td>Exactly the same successful Lane set permits Polling; otherwise return to Detect.Quiet</td></tr><tr><td>Polling.Active</td><td>24 ms timeout with an alternate partial-Lane path</td><td>Eight qualifying consecutive sequences on at least one Lane, at least 1024 TS1s transmitted after the first received TS1/TS2, and Electrical Idle exit on the predetermined Lane set. The rules can permit Polling.Configuration, Polling.Compliance, or Detect</td></tr><tr><td>Polling.Configuration</td><td>Transition conditions still unmet at the 48 ms timeout</td><td>Return to Detect. Separate a missing receive run from insufficient transmission after the first received TS2</td></tr></tbody></table></div><p>Section 4.2.6 gives LTSSM timeouts a −0 / +50% tolerance unless stated otherwise. Nominal 24 ms and 48 ms therefore have upper limits of 36 ms and 72 ms. Do not require every implementation to transition at exactly 24.000 ms or 48.000 ms. Establish the timer origin, observation time, and continuity of the record.</p><p>The Polling.Active timeout path uses “any Lane” and an implementation-specific predetermined Lane set, unlike the normal all-detected-Lanes condition. It permits further training without identifying a broken Lane. Polling.Compliance can also follow Enter Compliance or specified training-control conditions; recover the actual control and received sequence history.</p><p class="source-note">Base 6.0 §4.2.6 (p.444); §4.2.7.1.2 (p.456); §4.2.7.2.1 (pp.457–458); §4.2.7.2.3 (p.463).</p></section>

<section id="status-map"><h2>Why can Link Training be zero during Polling?</h2><p>Link Training in Link Status describes selected conditions, not every LTSSM state. This case reads the Root Port. The bit is inapplicable and hardwired to zero in Endpoints, Switch Upstream Ports, and PCI Express to PCI/PCI-X Bridges.</p><div class="table-wrap"><table><thead><tr><th scope="col">Root Port progress</th><th scope="col">Link Training</th><th scope="col">Interpretation</th></tr></thead><tbody><tr><td>Polling</td><td>0</td><td>Training sequences are still exchanged; zero does not imply L0</td></tr><tr><td>Initial Configuration</td><td>1</td><td>Polling has ended; width, Lane, and subsequent training remain</td></tr><tr><td>L0</td><td>0</td><td>History and other states distinguish this zero from the earlier Polling zero</td></tr></tbody></table></div><p>Use Table 4-48 for state mapping, then Table 7-26 for field applicability. The former's LinkUp is a Physical Layer indication to the Data Link Layer. Data Link Layer Link Active in Link Status instead reports DL_Active when reporting is supported. See <a href="/DOCS/pcie-course/chapter-8.html">Chapter 8</a> and <a href="/DOCS/pcie-course/chapter-17.html#initialization">Chapter 17</a> for the complete cross-layer explanation.</p><p class="source-note">Base 6.0 Table 4-48 <em>Link Status Mapped to the LTSSM</em> (p.453); §7.5.3.8, Figure 7-29, and Table 7-26 <em>Link Status Register</em> (pp.978–979).</p></section>

<section id="equalization"><h2>Follow Recovery when increasing speed</h2><p>Initial training reaches L0 at 2.5 GT/s even when both ends support higher rates. A later speed change uses Recovery from L0. Advertised higher rates during Polling are not the current signaling rate. Section 4.2.7.2.4 explicitly makes Polling.Speed unreachable.</p><p>Equalization (per-Lane transmitter/receiver adjustment to compensate for the channel) has rate-specific procedures. Section 4.2.4 requires the applicable procedure for the first transition to each rate at or above 8.0 GT/s, while defining jointly supported/advertised bypass mechanisms. Separate the normal procedure, bypass to the highest NRZ rate, and No Equalization Needed. One end's bit does not justify skipping work across the whole path.</p><dl class="st-terms" aria-label="Terms in this passage"><div><dt>NRZ</dt><dd>Non-Return-to-Zero</dd></div></dl><p>Connect the requesting end, Recovery substates, applicable equalization, and final speed/width. The two-ended Register and state walkthrough in <a href="/DOCS/pcie-course/chapter-8.html">Chapter 8</a> supplies the lookup entry. Recovery alone does not imply re-enumeration or clearing every Data Link state; actual LinkUp and Reset history matter.</p><p class="source-note">Base 6.0 §4.2.6.4 (p.445); §4.2.7.2.4 and the p.464 note <em>Support for Higher Data Rates Than 2.5 GT/s</em>; §4.2.4 <em>Link Equalization Procedure for 8.0 GT/s and Higher Data Rates</em> (pp.392–393).</p></section>

<section id="retimer"><h2>Separate one Link from its electrical segments</h2><p>A Retimer understands Physical Layer protocol and restores signal timing. Figure 4-61 marks the full Link and its Link Segments. Each Retimer has two Pseudo Ports whose orientation is determined dynamically during Configuration.</p><div class="table-wrap"><table><thead><tr><th scope="col">Illustrative path: Root Port → one Retimer → Endpoint</th><th scope="col">Roles</th><th scope="col">Analysis position</th></tr></thead><tbody><tr><td>Root Port to Retimer</td><td>Root Port Downstream Port faces the Retimer Upstream Pseudo Port</td><td>First electrical segment</td></tr><tr><td>Retimer to Endpoint</td><td>Retimer Downstream Pseudo Port faces the Endpoint Upstream Port</td><td>Second electrical segment</td></tr><tr><td>Root Port to Endpoint overall</td><td>Still one PCIe Link</td><td>No additional Data Link / Transaction-layer Switch</td></tr></tbody></table></div><p>Next read the modes in §4.3.2. Forwarding mode forwards applicable Symbols and Electrical Idle. Execution mode participates in specified cases such as Polling.Compliance and equalization Phases 2/3. Locate the Pseudo Port and direction when investigating one segment rather than assigning the Root Port's overall result to every segment.</p><p>Base 6.0 permits at most two Retimers per Link, with possible additional form-factor limits. Transparency to Data Link and Transaction Layers means no extra Bridge bus-number assignment and no independent TLP Ack/Replay domain per electrical segment. Electrical compliance still needs applicable Chapter 8 requirements and measurements.</p><dl class="st-terms" aria-label="Terms in this passage"><div><dt>TLP</dt><dd>Transaction Layer Packet</dd></div></dl><p class="source-note">Base 6.0 §4.3 <em>Retimers</em> (pp.564–565); §4.3.2 and Figure 4-61 <em>Supported Retimer Topologies</em> (pp.566–567). The table is an author-organized topology illustration.</p></section>

<section id="power"><h2>Check power and test branches by their purpose</h2><p>L0p (partial-Lane power saving within L0) is Flit-only, targets a symmetric width, and keeps at least one active Lane per direction. It does not first leave L0 to rebuild the entire Link; the two ends can briefly use different widths during a transition. L0s is a separate fast power state and must not be supported/advertised in Flit Mode, on Retimer Links, or with separate reference clocks and independent SSC (Spread Spectrum Clocking).</p><p>Polling.Compliance serves testing; the Loopback Lead requests the test and the Follower returns data; Hot Reset uses in-band signaling to reset a configured Link and associated downstream device. Figure 4-48 has distinct branches for them. A trace with “no TLP” still needs the state and entry conditions to distinguish training, power saving, and testing. See <a href="/DOCS/pcie-course/chapter-9.html">Chapter 9</a> for L1, Function power states, and platform policy.</p><dl class="st-terms" aria-label="Terms in this passage"><div><dt>TLP</dt><dd>Transaction Layer Packet</dd></div></dl><p class="source-note">Base 6.0 §4.2.6.2 (p.444); §§4.2.6.6–4.2.6.7 (pp.445–447); Figure 4-47 transition explanation (p.450); §§4.2.6.8–4.2.6.12 (pp.451–452).</p></section>

<section id="sources"><h2>Edition and sources</h2><p>PCI Express Base Specification Revision 6.0 (6.0-1.0-PUB) is the authority. Printed and PDF-viewer page numbers match at these locations. Topology and counts are author-created; capture-channel labels are not assigned Lane Numbers.</p><details class="source-note"><summary>Reading locations and purpose</summary><ul><li>§4.2.6 (pp.444–452): main-state tasks and timeout tolerance; Table 4-48 (p.453) and Figure 4-48 (p.454): state/status mapping.</li><li>§4.2.7.1.1 <em>Detect.Quiet</em> (p.455); §4.2.7.1.2 <em>Detect.Active</em> and Figure 4-49 (p.456): detection and retry branches.</li><li>§4.2.7.2.1 <em>Polling.Active</em> (pp.457–458); §§4.2.7.2.3 <em>Polling.Configuration</em> and 4.2.7.2.4 <em>Polling.Speed</em> (p.463); Figure 4-50 (p.464): transmit/consecutive-receive case.</li><li>§4.2.7.3 <em>Configuration</em> (p.464 onward), Figure 4-51 <em>Configuration Substate Machine</em> (p.482), §4.2.7.3.1.1 <em>Downstream Lanes</em> (pp.464–465): width and Lane work remains after Polling.</li><li>§7.5.3.8 <em>Link Status Register</em>, Figure 7-29, Table 7-26 (pp.978–979): Link Training meaning and applicability.</li><li>§4.2.4 (pp.392–393): first equalization and bypass; §§4.3 / 4.3.2 and Figure 4-61 (pp.564–567): Retimer roles, modes, and segments.</li></ul></details></section>
</article>
<nav class="bottom-nav" aria-label="Course and editions"><a href="/DOCS/pcie-course/index.html">Course overview</a><a href="/DOCS/pcie-course/chapter-19.html">Full Chinese tutorial</a><a href="/pcie/chapter-19-zh-tw/">繁體中文</a></nav>
</div>
