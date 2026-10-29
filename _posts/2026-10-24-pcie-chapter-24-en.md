---
layout: post
title: "PCIe Chapter 24: TPH, LTR, and OBFF Platform Coordination"
date: 2026-10-24 00:00:00 +0800
last_modified_at: 2026-10-29 00:00:00 +0800
permalink: /pcie/chapter-24-en/
categories: [PCIe]
tags: [PCIe, Specification]
lang: en
spec_teaching: true
spec_series: pcie
description: "資料用途、可等待的延遲與平台活動時窗，分別要查哪條規格路線？"
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
<nav class="bottom-nav" aria-label="Course and editions"><a href="/DOCS/pcie-course/index.html">Course overview</a><a href="/DOCS/pcie-course/chapter-24.html">Full Chinese tutorial</a><a href="/pcie/chapter-24-zh-tw/">繁體中文</a></nav>
<article class="lesson">
<p>TPH (TLP Processing Hints) adds intended-use information to Memory Requests. LTR (Latency Tolerance Reporting) reports service-latency needs upstream. OBFF (Optimized Buffer Flush/Fill) communicates favorable platform activity windows downstream. The three mechanisms have separate support and enable conditions.</p><dl class="st-terms" aria-label="Terms in this passage"><div><dt>TLP</dt><dd>Transaction Layer Packet</dd></div></dl><figure class="diagram"><svg viewBox="0 0 900 310" style="min-width:640px" role="img" aria-labelledby="ch24-en-t ch24-en-d"><title id="ch24-en-t">Three independent kinds of platform information</title><desc id="ch24-en-d">TPH accompanies Memory Requests. A Switch aggregates LTR reports upstream. OBFF indications propagate downstream with local reception.</desc><g data-walk-target="rc"><rect x="20" y="15" width="200" height="48" rx="8" fill="var(--surface-alt)" stroke="var(--line)"/><text x="120" y="44" text-anchor="middle" font-size="15">Root Complex / Root Port</text></g><g data-walk-target="sw"><rect x="350" y="15" width="200" height="48" rx="8" fill="var(--surface-alt)" stroke="var(--line)"/><text x="450" y="44" text-anchor="middle" font-size="15">Switch</text></g><g data-walk-target="ep"><rect x="680" y="15" width="200" height="48" rx="8" fill="var(--surface-alt)" stroke="var(--line)"/><text x="780" y="44" text-anchor="middle" font-size="15">Endpoint A / B</text></g><g data-walk-target="tph"><text x="450" y="95" text-anchor="middle" font-size="16">TPH: Memory Request with usage hints</text><path d="M680 115 H550" stroke="var(--accent)" stroke-width="2"/><polygon points="550,115 560,110 560,120" fill="var(--accent)"/><path d="M350 115 H220" stroke="var(--accent)" stroke-width="2"/><polygon points="220,115 230,110 230,120" fill="var(--accent)"/><text x="450" y="122" text-anchor="middle" font-size="15">Memory TLP</text></g><g data-walk-target="ltr"><text x="450" y="180" text-anchor="middle" font-size="16">LTR: aggregate, subtract Switch latency</text><path d="M680 200 H550" stroke="var(--accent)" stroke-width="2"/><polygon points="550,200 560,195 560,205" fill="var(--accent)"/><path d="M350 200 H220" stroke="var(--accent)" stroke-width="2"/><polygon points="220,200 230,195 230,205" fill="var(--accent)"/><text x="450" y="207" text-anchor="middle" font-size="15">min − Lswitch</text></g><g data-walk-target="obff"><text x="450" y="265" text-anchor="middle" font-size="16">OBFF: platform activity indications</text><path d="M220 285 H350" stroke="var(--accent)" stroke-width="2"/><polygon points="350,285 340,280 340,290" fill="var(--accent)"/><path d="M550 285 H680" stroke="var(--accent)" stroke-width="2"/><polygon points="680,285 670,280 670,290" fill="var(--accent)"/><text x="450" y="292" text-anchor="middle" font-size="15">Local receive</text></g></svg><figcaption>Author-drawn comparison of information flow, not an execution sequence. LTR and OBFF Messages terminate at the adjacent receiver; a Switch aggregates LTR or propagates OBFF according to the respective rules.</figcaption></figure><dl class="st-terms" aria-label="Terms in this passage"><div><dt>TPH</dt><dd>TLP Processing Hints</dd></div><div><dt>TLP</dt><dd>Transaction Layer Packet</dd></div><div><dt>LTR</dt><dd>Latency Tolerance Reporting</dd></div><div><dt>OBFF</dt><dd>Optimized Buffer Flush/Fill</dd></div></dl>
<section id="scenario"><h2>Keep the participants in view</h2><p>The topology is Root Port → Switch → Endpoints A and B, each with only Function 0 in D0. Basic Link operation and resource configuration are ready. The independent-Port background is in <a href="/DOCS/pcie-course/chapter-1.html">Chapter 1</a>.</p><p><strong>Simulated data:</strong> the topology, values and timings below were created for teaching and do not represent particular hardware. Assume that the relevant TPH (Request processing hints), LTR (service-latency reporting) and OBFF (platform activity hints) capabilities have each been checked along their required paths. The platform supplies valid steering values. WAKE# is unavailable on the Links used for the OBFF example, so Message signaling is used. These are separate assumptions, not consequences of finding one capability.</p></section>
<section id="tph"><h2>A device writes data that the host will soon read</h2><p>Open Table 6-13, <em>Processing Hint Mapping</em>. The device-write/host-read usage model maps to Target, PH[1:0]=10b. This information does not change the Memory Write Transaction type or grant access rights.</p><p>Next, §6.17.2 defines the Steering Tag (ST), a system-specific value identifying a processing resource. Software obtains the appropriate platform value; a tag is not a universal CPU number. Section 6.17.4 requires the Requester, Completer and every intermediate routing element to support the associated capabilities. TPH Completer Supported is Device Capabilities 2 [13:12] for Root Ports and Endpoints; it is Reserved for Switch Functions, so it is not a per-Switch-port support test.</p></section>
<section id="tph-table"><h2>Connect capability, table and selected mode</h2><p>Walk the Extended Capability list to ID=0017h, Version=1, and call the base T. Figure 7-289 locates the structure; Tables 7-258 and 7-259 decode its fields. Assume software has configured tags 0031h, 0042h, 0053h and 0064h.</p><div class="table-wrap"><table><thead><tr><th scope="col">Offset</th><th scope="col">Simulated value</th><th scope="col">Decoded fields</th></tr></thead><tbody><tr data-tph-case="cap"><td>T+04h</td><td>00030203h</td><td>No ST=1; Interrupt Vector=1; Extended TPH=0; Location=01b; Size=3 → 4 entries</td></tr><tr data-tph-case="entry"><td>T+10h</td><td>0053h</td><td>ST entry 2; ST Lower=53h; upper byte RsvdP</td></tr><tr data-tph-case="control"><td>T+08h</td><td>00000101h</td><td>ST Mode Select=001b; TPH Requester Enable=01b</td></tr></tbody></table></div><p>ST Table Location=01b places the table in this structure. ST Table Size=3 is N−1 encoded, hence four entries. Figure 7-293 starts the table at T+0Ch with 2-byte entries. In Interrupt Vector Mode, valid MSI-X vector 2 selects entry 2 at T+0Ch+2×2=T+10h. Assume both the enabled vector range and the table cover that entry.</p><dl class="st-terms" aria-label="Terms in this passage"><div><dt>MSI-X</dt><dd>Message Signaled Interrupts Extension</dd></div></dl><p>Control 00000101h selects Interrupt Vector Mode and permits ordinary TPH, not Extended TPH. Extended TPH support is clear, so the entry's upper byte is RsvdP; ST Lower supplies 53h. This identifies the selected hint, not an observed cache destination or performance improvement.</p><p>With Location=10b, look in the MSI-X Table instead; a Function cannot place the table in both locations. No ST Mode requires zero tags and still permits Processing Hints. The specification recommends quiescing the Function or disabling the TPH Requester during table updates to avoid nondeterministic values. Preserve that recommendation strength.</p><dl class="st-terms" aria-label="Terms in this passage"><div><dt>MSI-X</dt><dd>Message Signaled Interrupts Extension</dd></div></dl><p class="source-note">Base 6.0 §§6.17.2–6.17.4, pp.779–781; §7.9.13, Figures 7-289–7-294 and Tables 7-257–7-260, pp.1241–1245. Basic Request layout: <a href="/DOCS/pcie-course/chapter-14.html">Chapter 14</a>.</p></section>
<section id="ltr"><h2>First distinguish configuration registers from reported fields</h2><p>LTR reports Endpoint Memory Read/Write service requirements for central platform power policy. It does not directly control Link or Switch-internal power management. Check Device Capabilities 2 [11], LTR Mechanism Supported, and Device Control 2 [10], LTR Mechanism Enable. Do not enable an Endpoint unless the Root Complex and all intermediate Switches support LTR. Enable devices closest to the Root Port first.</p><p>Figure 7-142 locates the LTR Extended Capability, ID=0018h, Version=1. With base L, Max Snoop Latency is L+04h and Max No-Snoop Latency is L+06h. These software-writable limits provide platform information; they are not a log of the latest device report. Ordinary multi-Function devices implement this structure only in Function 0. Root Ports and Switch Downstream Ports do not implement this structure, although they can support and process LTR through Device Capabilities 2/Control 2.</p><p><strong>Author example:</strong> Max Snoop Latency=080Ah means Value=10 and Scale=010b: 10×1,024 ns=10,240 ns. Bits [15:13] are RsvdP; this register has no Requirement bit. In a Message, Snoop Latency=880Ah instead represents a valid 10,240 ns requirement. Do not copy 880Ah into the configuration register.</p><p class="source-note">Base 6.0 §6.18, pp.781–782; §7.5.3.15, p.991; §7.5.3.16, p.996; §7.8.2, Figures 7-142–7-145 and Tables 7-126–7-128, pp.1101–1103.</p></section>
<section id="ltr-message"><h2>Decode both reported traffic classes</h2><p>Use Figure 2-57 for Non-Flit Mode, or Figure 2-58 after Flit processing and TLP reassembly. The base headers differ. Table 2-33 identifies Message Code=10h, Routing=100b, TC0 and no Data Payload. The two latency fields are in the Header, not a MsgD payload.</p><p>Figure 6-15, <em>Latency Fields Format for LTR Messages</em>, gives each 16-bit field: Requirement [15], Reserved [14:13], Scale [12:10] and Value [9:0]. Decode time only for Requirement=1. Permitted scales 000b–101b multiply by 1, 32, 1,024, 32,768, 1,048,576 or 33,554,432 ns.</p><div class="table-wrap"><table><thead><tr><th scope="col">Source / field</th><th scope="col">Raw 16 bits</th><th scope="col">Requirement [15]</th><th scope="col">Scale [12:10]</th><th scope="col">Value [9:0]</th><th scope="col">Meaning</th></tr></thead><tbody><tr data-ltr-field="a-snoop"><td>A / Snoop</td><td>880Ah</td><td>1</td><td>010b</td><td>10</td><td>10,240 ns</td></tr><tr data-ltr-field="a-nosnoop"><td>A / No-Snoop</td><td>080Ah</td><td>0</td><td>010b</td><td>10</td><td>Ignored</td></tr><tr data-ltr-field="b-snoop"><td>B / Snoop</td><td>8C01h</td><td>1</td><td>011b</td><td>1</td><td>32,768 ns</td></tr><tr data-ltr-field="b-nosnoop"><td>B / No-Snoop</td><td>8808h</td><td>1</td><td>010b</td><td>8</td><td>8,192 ns</td></tr></tbody></table></div><p>A's No-Snoop Requirement=0 makes its retained Value and Scale irrelevant. It does not request zero latency. By contrast, Requirement=1 with Value=0 says that any delay affects the device and requests the best possible service; it is not a hardware promise of zero delay.</p><p class="source-note">Base 6.0 §2.2.8.8, Table 2-33 and Figures 2-57/2-58, pp.187–188; §6.18, Figure 6-15, pp.781–782.</p></section>
<section id="ltr-aggregate"><h2>Why does the Switch report different values?</h2><p>Routing=100b terminates at the adjacent receiver. Under §6.18 the Switch collects requirements from enabled Downstream Ports, takes separate minima for Snoop and No-Snoop, and subtracts all Switch-induced latency, Lswitch. Clamp a negative result to zero. Its Upstream Port transmits a conglomerated Message rather than forwarding A's original Message unchanged.</p><p>Assume a fixed Lswitch=1,024 ns and no other valid sources. A sets the tighter Snoop requirement; only B supplies a No-Snoop requirement:</p><div class="table-wrap"><table><thead><tr><th scope="col">Traffic</th><th scope="col">Downstream minimum</th><th scope="col">Lswitch</th><th scope="col">Upstream value</th><th scope="col">Upstream encoding</th></tr></thead><tbody><tr data-ltr-aggregate="snoop"><td>Snoop</td><td>10,240 ns</td><td>1,024 ns</td><td>9,216 ns</td><td>8809h</td></tr><tr data-ltr-aggregate="nosnoop"><td>No-Snoop</td><td>8,192 ns</td><td>1,024 ns</td><td>7,168 ns</td><td>8807h</td></tr></tbody></table></div><p>A platform Snoop service time of 9,216 ns plus 1,024 ns in the Switch matches A's 10,240 ns report. If B's Port goes DL_Down, invalidate B's old values. Snoop remains constrained by A; No-Snoop now has no requirement and its upstream Requirement must be clear.</p><p>For Requirement=1 and Value=0, the Switch uses zero regardless of Scale. A zero conglomerated result must have both Value and Scale zero. A Not Permitted Scale is not an arithmetic operand: §6.18 treats that source as effectively infinite for Switch aggregation. The normal example uses only permitted encodings.</p><p>If Lswitch changes with operating mode, it must not exceed 20% of the downstream minimum unless even the lowest-latency mode exceeds that bound, in which case that mode must be used. A multi-Function device similarly selects the lowest requirements per traffic class; Snoop and No-Snoop may come from different Functions.</p><p class="source-note">Base 6.0 §6.18, pp.782–784; Table 2-33, p.187.</p></section>
<section id="ltr-update"><h2>Track updates and the service interval</h2><p>During a sequence of Requests, the RC must comprehend an updated requirement before servicing a subsequent Request; the new value must take effect within the previously reported latency. The Implementation Note recommends reporting a tighter requirement early enough to allow that old latency interval, and a looser one after the final Request needing the preceding value.</p><p>If the latest effective Message reported a requirement, a PMCSR Write directing the device to non-D0 requires a Message clearing both Requirement bits before the transition. Clearing LTR Mechanism Enable through a Configuration Write also requires withdrawal; the FLR rule is marked MUST@FLIT in this edition and needs its mode qualification. DL_Down invalidates a Downstream Port's old reports and resets that Port's LTR Mechanism Enable to its default.</p><dl class="st-terms" aria-label="Terms in this passage"><div><dt>FLR</dt><dd>Function Level Reset</dd></div></dl><p>The RC is strongly encouraged, not required, to honor requested service latencies. Non-Posted service latency ends at the start of the <strong>first Completion</strong>, not at the end of all Split Completions. The Posted definition concerns a credit-blocked Request and return of credits permitting transmission to continue. Clock PM may add clock-restoration delay; Figures 6-16 and 6-17 connect those timing components and update scheduling. Link exit details remain in <a href="/DOCS/pcie-course/chapter-10.html">Chapter 10</a>.</p><p class="source-note">Base 6.0 §6.18, pp.782–787; Figure 6-16 <em>CLKREQ# and Clock Power Management</em>, p.785; Figure 6-17 <em>Use of LTR and Clock Power Management</em>, p.786; §7.5.3.16, p.996.</p></section>
<section id="obff"><h2>Why may a low-power Link have no activity Message?</h2><p>Figure 6-19 shows topology segments using WAKE# or Messages, with Switch conversion between them. Here WAKE# is unavailable on the relevant Links and the platform has established Message delivery support. Endpoint capability alone is insufficient to enable the mechanism.</p><p>Device Capabilities 2 [19:18] reports supported signaling; Device Control 2 [14:13] selects it: 00b disabled, 01b Message Variation A, 10b Message Variation B, 11b WAKE#. A and B are alternative configurations of the same Downstream Port:</p><div class="table-wrap"><table><thead><tr><th scope="col">OBFF Enable [14:13]</th><th scope="col">Downstream Port at Tx_L0s / L1</th><th scope="col">Trace interpretation</th></tr></thead><tbody><tr><td>01b / Variation A</td><td>Discard this indication while Tx_L0s / L1</td><td>No obligation to wake the Link for this hint</td></tr><tr><td>10b / Variation B</td><td>Direct the Link to L0, then transmit</td><td>Expect a Link exit before the Message</td></tr></tbody></table></div><p>Thus, seeing no indication during L1 can be required by Variation A. Read the actual egress Port's Enable and the contemporaneous Link state. For Variation B, inspect the return to L0 followed by Message transmission. Each segment handles the indication; this is not one unchanged end-to-end broadcast.</p><p>OBFF recommends enabling all Upstream Ports before Downstream Ports; Root Ports must be enabled after all other Ports. This differs from LTR's closest-to-Root-Port-first order. Initial OBFF configuration must assume CPU Active until the first observed transition, regardless of the current logical WAKE# level.</p><p class="source-note">Base 6.0 §6.19, Figure 6-19, pp.787–790; §7.5.3.15, p.992; §7.5.3.16, p.997.</p></section>
<section id="obff-code"><h2>Interpret the received indication</h2><p>Use Figure 2-59 or 2-60 for the mode and Table 2-34 for Message Code=12h, Routing=100b, TC0 and no Data Payload. Only Downstream transmission is permitted. Requester ID is the transmitting Port's ID on that segment. Figure 6-18 maps codes to WAKE# patterns; actual WAKE# electrical requirements require the applicable Card Electromechanical specification.</p><div class="table-wrap"><table><thead><tr><th scope="col">OBFF Code</th><th scope="col">Platform indication</th></tr></thead><tbody><tr><td>0000b / Idle</td><td>Platform in an idle low-power state</td></tr><tr><td>0001b / OBFF</td><td>Memory path available for device Memory Read/Write bus mastering</td></tr><tr><td>1111b / CPU Active</td><td>System active for all device actions, including bus mastering and interrupts</td></tr></tbody></table></div><p>A receiver enabled for OBFF Message signaling must treat a Reserved OBFF Code as CPU Active. At an unsupported or disabled Port, the Message is an Unsupported Request. Receiving a Message while enabled for WAKE# signaling has undefined behavior.</p><p>Non-D0 Functions must not respond to OBFF/CPU Active indications. A working Function may still issue bus mastering or interrupt traffic whenever otherwise enabled. The platform is recommended not to return to Idle within 10 μs of opening an activity window, while Endpoints are recommended not to assume any particular window duration. This does not guarantee a 10 μs window on every occurrence.</p><p class="source-note">Base 6.0 §2.2.8.9, Table 2-34 and Figures 2-59/2-60, pp.188–189; §6.19, Figure 6-18 <em>Codes and Equivalent WAKE# Patterns</em>, pp.787–790.</p></section>
<section id="reading"><h2>Choose the next lookup from the actual question</h2><p>For an unexpected data-placement result, follow PH, ST Mode, table selection, Requester Enable and target/path support. For inconsistent latency reports, follow Support/Enable, reported fields, aggregation and update history. For a missing activity indication, follow signaling selection, egress Variation, Link state and receiver configuration. Then examine platform policy and measured effects.</p><p>“LTR enabled, so the Link should enter L1” conflates central-resource requirements with ASPM's own support, controls and entry conditions. “ST=53h, therefore data is in CPU 53's cache” requires a platform tag mapping and evidence of the processing result. A decoded hint tells you what information was supplied, not that every intended optimization occurred.</p></section>
<section id="sources"><h2>Edition and source boundaries</h2><p>PCI Express Base Specification Revision 6.0 (6.0-1.0-PUB) is the technical source. Printed and PDF-viewer page numbers match. All topology, register and timing examples are author-created; no hardware writes or performance measurements were performed. No external website supplies technical claims in this chapter.</p><details class="source-note"><summary>Source map by task</summary><ul><li>§6.17 <em>TLP Processing Hints (TPH)</em>, §§6.17.1–6.17.4, pp.778–781; Table 6-13 <em>Processing Hint Mapping</em> and Table 6-14 <em>ST Modes of Operation</em>, pp.779–780. §7.9.13 <em>TPH Requester Extended Capability</em>, Figures 7-289–7-294, Tables 7-257–7-260, pp.1241–1245: modes, table location/size, Control and entries.</li><li>§2.2.8.8 <em>Latency Tolerance Reporting (LTR) Message</em>, Table 2-33 <em>LTR Message</em>, Figures 2-57/2-58 <em>LTR Message - Non-Flit Mode / Flit Mode</em>, pp.187–188. §6.18 <em>Latency Tolerance Reporting (LTR) Mechanism</em>, pp.781–787; Figure 6-15 <em>Latency Fields Format for LTR Messages</em>, p.781; Figures 6-16/6-17, pp.785–786: messages, fields, aggregation and timing.</li><li>§7.8.2 <em>Latency Tolerance Reporting (LTR) Extended Capability</em>, Figures 7-142–7-145, Tables 7-126–7-128, pp.1101–1103: platform limits and Function/Port applicability.</li><li>§2.2.8.9 <em>Optimized Buffer Flush/Fill (OBFF) Message</em>, Table 2-34 <em>OBFF Message</em>, Figures 2-59/2-60 <em>OBFF Message - Non-Flit Mode / Flit Mode</em>, pp.188–189. §6.19 <em>Optimized Buffer Flush/Fill (OBFF) Mechanism</em>, pp.787–790; Figure 6-18, p.788; Figure 6-19 <em>Example Platform Topology Showing a Link Where OBFF is Carried by Messages</em>, p.789: signaling conversion and Variations.</li><li>§7.5.3.15 <em>Device Capabilities 2 Register (Offset 24h)</em>, pp.991–992; §7.5.3.16 <em>Device Control 2 Register (Offset 28h)</em>, pp.996–997. Offsets here are relative to the PCI Express Capability base.</li><li>External boundaries: use the applicable PCI Express Card Electromechanical Specification for WAKE# electrical requirements. Tag-to-resource mapping, platform policy and achieved benefit need platform documentation and measurements.</li></ul></details></section>
</article>
<nav class="bottom-nav" aria-label="Course and editions"><a href="/DOCS/pcie-course/index.html">Course overview</a><a href="/DOCS/pcie-course/chapter-24.html">Full Chinese tutorial</a><a href="/pcie/chapter-24-zh-tw/">繁體中文</a></nav>
</div>
