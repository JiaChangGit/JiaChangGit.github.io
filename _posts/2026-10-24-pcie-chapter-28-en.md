---
layout: post
title: "PCIe Chapter 28: ACS, Peer-to-Peer, and Multicast"
date: 2026-10-24 00:00:00 +0800
last_modified_at: 2026-10-29 00:00:00 +0800
permalink: /pcie/chapter-28-en/
categories: [PCIe]
tags: [PCIe, Specification]
lang: en
spec_teaching: true
spec_series: pcie
description: "同一顆 Switch 內，直送、導引與多播如何由欄位決定？"
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
<nav class="bottom-nav" aria-label="Course and editions"><a href="/DOCS/pcie-course/index.html">Course overview</a><a href="/DOCS/pcie-course/chapter-28.html">Full Chinese tutorial</a><a href="/pcie/chapter-28-zh-tw/">繁體中文</a></nav>
<article class="lesson">
<p>Sharing one Switch does not settle a packet's path. Follow ACS (Access Control Services) decisions at the ingress, then a four-window Multicast case with two outputs, address Overlay and ECRC handling.</p><dl class="st-terms" aria-label="Terms in this passage"><div><dt>ECRC</dt><dd>End-to-End Cyclic Redundancy Check</dd></div></dl><figure class="diagram"><svg viewBox="0 0 900 510" style="min-width:720px" role="img" aria-labelledby="ch28-en-t ch28-en-d"><title id="ch28-en-t">Ingress DP1 chooses the permitted route</title><desc id="ch28-en-d">A enters DP1. ACS determines direct routing toward B or redirection through UP0 to the RC. C is a second recipient in the later Multicast case.</desc><rect x="45" y="120" width="810" height="245" rx="12" fill="none" stroke="var(--line)"/><text x="65" y="147" font-size="16">Switch: UP0 + DP1 / DP2 / DP3</text><path d="M455 65 V160 M455 205 V245 M180 285 V245 H740 V285 M460 245 V285 M180 330 V430 M460 330 V430 M740 330 V430" fill="none" stroke="var(--line)" stroke-width="2"/><g data-walk-target="rc"><rect x="345" y="15" width="220" height="50" rx="8" fill="var(--surface-alt)" stroke="var(--line)"/><text x="455.0" y="46.0" text-anchor="middle" font-size="16">Root Complex / Root Port</text></g><g data-walk-target="up"><rect x="355" y="160" width="200" height="45" rx="8" fill="var(--surface-alt)" stroke="var(--line)"/><text x="455.0" y="188.5" text-anchor="middle" font-size="16">UP0: Port 0</text></g><g data-walk-target="p1"><rect x="85" y="285" width="190" height="45" rx="8" fill="var(--surface-alt)" stroke="var(--line)"/><text x="180.0" y="313.5" text-anchor="middle" font-size="16">DP1: Port 1 / ACS</text></g><g data-walk-target="p2"><rect x="365" y="285" width="190" height="45" rx="8" fill="var(--surface-alt)" stroke="var(--line)"/><text x="460.0" y="313.5" text-anchor="middle" font-size="16">DP2: Port 2 / ACS</text></g><g data-walk-target="p3"><rect x="645" y="285" width="190" height="45" rx="8" fill="var(--surface-alt)" stroke="var(--line)"/><text x="740.0" y="313.5" text-anchor="middle" font-size="16">DP3: Port 3 / ACS</text></g><g data-walk-target="a"><rect x="85" y="430" width="190" height="50" rx="8" fill="var(--surface-alt)" stroke="var(--line)"/><text x="180.0" y="461.0" text-anchor="middle" font-size="16">Endpoint A: 03:00.0</text></g><g data-walk-target="b"><rect x="365" y="430" width="190" height="50" rx="8" fill="var(--surface-alt)" stroke="var(--line)"/><text x="460.0" y="461.0" text-anchor="middle" font-size="16">Endpoint B: 04:00.0</text></g><g data-walk-target="c"><rect x="645" y="430" width="190" height="50" rx="8" fill="var(--surface-alt)" stroke="var(--line)"/><text x="740.0" y="461.0" text-anchor="middle" font-size="16">Endpoint C: 05:00.0</text></g><g data-walk-target="request"><path d="M180 430 V330" stroke="var(--accent)" stroke-width="2"/><polygon points="180,330 175,340 185,340" fill="var(--accent)"/><text x="195" y="394" font-size="15">Request</text></g><g data-walk-target="direct"><path d="M275 310 H365" stroke="var(--accent)" stroke-width="2"/><polygon points="365,310 355,305 355,315" fill="var(--accent)"/><text x="320" y="296" text-anchor="middle" font-size="15">Direct</text></g><g data-walk-target="redirect"><path d="M180 285 V220 H455 V205" fill="none" stroke="var(--accent)" stroke-dasharray="6 4" stroke-width="2"/><polygon points="455,65 450,75 460,75" fill="var(--accent)"/><text x="160" y="185" font-size="15">Via UP0 to RC</text></g></svg><figcaption>Author-created topology. UP0 is the Switch Upstream Port; DP1–DP3 are Downstream Ports. A's Request enters DP1; B's Completion enters DP2. Solid and dashed arrows are alternative routes. RC validation requires a separate result.</figcaption></figure><dl class="st-terms" aria-label="Terms in this passage"><div><dt>ACS</dt><dd>Access Control Services</dd></div></dl><section id="trace"><h2>Locate the ingress ACS controls before following A to B</h2><p>A enters the Switch through DP1; normal address decoding selects DP2 toward B. DP1 is the Ingress Port and DP2 the candidate Egress Port. Read the ingress DP1 ACS (Access Control Services) controls for this P2P (Peer-to-Peer) Request.</p><p><strong>Simulated data:</strong> UP0 has Port Number 0; DP1/DP2/DP3 have Numbers 1/2/3. A/B/C use Requester IDs 0300h/0400h/0500h. DP1 has Secondary and Subordinate Bus Number 03h, without FPB. B's BAR covers 90000000h–90000FFFh; C's covers A0000000h–A0000FFFh. Required resources, Windows, Memory Space Enable, Bus Master Enable and Link transport are ready. Packet examples use Non-Flit Mode, without Reset or Replay events.</p><dl class="st-terms" aria-label="Terms in this passage"><div><dt>FPB</dt><dd>Flattening Portal Bridge</dd></div><div><dt>BAR</dt><dd>Base Address Register</dd></div></dl><p>A issues a four-byte Memory Write to 90000500h with AT (Address Type)=00b. The AT definitions continue <a href="/DOCS/pcie-course/chapter-27.html">Chapter 27</a>. This case follows route selection. A Posted Write has no ordinary Completion; observing its destination's internal write result requires further evidence.</p><p class="source-note">Base 6.0 §§6.12–6.12.1.1, pp.751–755; address and Window routing: <a href="/DOCS/pcie-course/chapter-5.html">Chapter 5</a>.</p></section>
<section id="registers"><h2>Connect capability, control and the destination vector bit</h2><p>Walk the capability list for ID 000Dh, Version 1, and use Figure 7-131. With DP1's base A, A+04h is ACS Capability, A+06h ACS Control and A+08h the Egress Control Vector.</p><p>Capability 087Fh advertises the first seven controls, no ACS Enhanced Capability, and eight vector bits. Control 001Dh enables Source Validation, P2P Request Redirect, P2P Completion Redirect and Upstream Forwarding. Translation Blocking, P2P Egress Control and Direct Translated P2P are disabled.</p><p>For selective control toward B, use DP2's <strong>Port Number 2</strong>. Equation 7-4 gives offset 08h+(2 div 32)×4=08h, bit 2, mask 00000004h. The index is not B's Bus Number, Function Number or analyzer channel. Egress Control Enable determines whether that vector participates.</p><p>Vector Size 00h means 256 bits when Egress Control is supported. Without that capability, Size is undefined and the vector need not exist.</p><p class="source-note">Base 6.0 §§7.7.11–7.7.11.4, Figures 7-131–7-135, Tables 7-116–7-119, Equation 7-4, pp.1083–1089.</p></section>
<section id="request-case"><h2>Which settings change the route to the same address?</h2><p>Source Validation accepts this example's Requester Bus 03h within DP1's 03h–03h aperture. RID 0600h would instead cause ACS Violation. This aperture check does not authenticate a process or authorize every data address.</p><dl class="st-terms" aria-label="Terms in this passage"><div><dt>RID</dt><dd>Routing ID, the packet routing identity</dd></div></dl><p>Enabled Translation Blocking rejects an upstream Memory Request whose AT is not the default 00b. It takes precedence over Upstream Forwarding and P2P mechanisms. After ingress checks, use Table 6-11.</p><p>Each row below is an independent snapshot, not a programming sequence. E is P2P Egress Control Enable, R P2P Request Redirect Enable, V the ingress vector's bit for DP2, D Direct Translated P2P Enable, and TB Translation Blocking Enable. Translated rows assume a valid translation and Write permission. The comparison enabling both Direct and Redirect also assumes the ordering preconditions in §6.12.6.2 are satisfied.</p><div class="table-wrap"><table><thead><tr><th scope="col">ACS Control</th><th scope="col">AT</th><th scope="col">E</th><th scope="col">R</th><th scope="col">V</th><th scope="col">D</th><th scope="col">TB</th><th scope="col">Result</th></tr></thead><tbody><tr data-acs-route="redirect"><td>001Dh</td><td>00b</td><td>0</td><td>1</td><td>1</td><td>0</td><td>0</td><td>Redirect</td></tr><tr data-acs-route="select-direct"><td>003Dh</td><td>00b</td><td>1</td><td>1</td><td>0</td><td>0</td><td>0</td><td>Direct</td></tr><tr data-acs-route="select-redirect"><td>003Dh</td><td>00b</td><td>1</td><td>1</td><td>1</td><td>0</td><td>0</td><td>Redirect</td></tr><tr data-acs-route="block"><td>0039h</td><td>00b</td><td>1</td><td>0</td><td>1</td><td>0</td><td>0</td><td>ACS Violation</td></tr><tr data-acs-route="translated"><td>007Dh</td><td>10b</td><td>1</td><td>1</td><td>1</td><td>1</td><td>0</td><td>Direct</td></tr><tr data-acs-route="translation-block"><td>007Fh</td><td>10b</td><td>1</td><td>1</td><td>1</td><td>1</td><td>1</td><td>ACS Violation</td></tr></tbody></table></div><p>The normal case has E=0/R=1 and redirects toward the RC. With E=1/R=1/V=0, Table 6-11 instead requires direct routing; V=1 redirects. E=1/R=0/V=1 causes ACS Violation. Read R together with E and V.</p><p>For an applicable Memory Request with AT=10b and D=1, Direct Translated P2P overrides Request Redirect and Egress Control. However, TB=1 in the last row already requires ACS Violation; D does not override Translation Blocking. Direct routing still depends on valid routing and authorization.</p><p class="source-note">Base 6.0 §6.12.1.1, pp.752–754; §6.12.3, Table 6-11, pp.757–758; Table 7-118, pp.1087–1088; §6.12.6.2, p.761.</p></section>
<section id="ordering"><h2>Continue through the RC, return traffic and error handling</h2><p>Return to Control 001Dh. Required ACS Upstream Forwarding along the redirection path must be effective, and the RC must implement Redirected Request Validation. Upstream Forwarding handles traffic that would otherwise return through the receiving Downstream Port's own egress; relevant handling is undefined when it is disabled. A single-Function Switch Upstream Port does not thereby require its own ACS Capability.</p><p>RC validation decides whether a Request is reflected Downstream or blocked as ACS Violation. Its algorithms and specific controls are platform defined. Root Port Redirect capability does not imply any level of RC P2P support. For the normal example, additionally assume RC validation permits reflection through the Root Port, Switch UP0 and DP2 toward B. Downstream Ports do not redirect that Downstream Request back Upstream. B's internal write result still needs observation.</p><p>Separately consider B's Completion for an earlier Memory Read from A. It enters DP2, so read DP2's Completion Redirect control. When enabled, a peer Completion with RO (Relaxed Ordering)=0 redirects Upstream; RO=1 routes normally. Request Redirect, Egress Control and Translation Blocking do not affect Completions.</p><p>Completion redirection prevents a direct non-RO Completion from effectively passing a redirected Posted Request. Mixed paths need §6.12.6's ordering analysis; fewer hops alone do not establish legality. Full Passing rules are in <a href="/DOCS/pcie-course/chapter-15.html">Chapter 15</a>.</p><p>An ACS Violation on a Non-Posted Request requires a CA (Completer Abort) Completion; a Posted Write has no such ordinary reply. The handling component logs <strong>ACS Violation</strong>, not Completer Abort Error merely because it sent CA. Section 6.12.5 also specifies target-abort status and reporting. Continue AER handling in <a href="/DOCS/pcie-course/chapter-12.html">Chapter 12</a>.</p><dl class="st-terms" aria-label="Terms in this passage"><div><dt>AER</dt><dd>Advanced Error Reporting</dd></div></dl><p class="source-note">Base 6.0 §6.12.1.1, pp.753–754; §6.12.1.3, p.756; §6.12.2, p.757; §§6.12.5–6.12.6.2, pp.759–761.</p></section>
<section id="multicast"><h2>Select a group before copying the Write to B and C</h2><p>Multicast copies one Posted Request to configured outputs. Read Figure 6-14's windows, then §6.14.1's hit conditions, then membership. Only Memory Writes and Address Routed Messages can hit. A Non-Posted Memory Read inside the same address window remains unicast.</p><p>This separate simulated configuration gives all applicable Switch structures identical MC_Enable, MC_Num_Group, MC_Base_Address and MC_Index_Position. A/B/C have no Multicast Capability; B/C receive through Overlay. Both egress Ports support ECRC regeneration with the required AER and ECRC Check Capable support. Let M be the Multicast ID 0012h, Version 1 capability base:</p><dl class="st-terms" aria-label="Terms in this passage"><div><dt>ECRC</dt><dd>End-to-End Cyclic Redundancy Check</dd></div><div><dt>AER</dt><dd>Advanced Error Reporting</dd></div></dl><div class="table-wrap"><table><thead><tr><th scope="col">Register</th><th scope="col">Offset</th><th scope="col">Value</th><th scope="col">Fields</th></tr></thead><tbody><tr data-mc-config="cap"><td>Multicast Capability</td><td>M+04h</td><td>8003h</td><td>MC_Max_Group=3; MC_ECRC_Regeneration_Supported=1</td></tr><tr data-mc-config="control"><td>Multicast Control</td><td>M+06h</td><td>8003h</td><td>MC_Enable=1; MC_Num_Group=3</td></tr><tr data-mc-config="base"><td>MC_Base_Address</td><td>M+08h</td><td>000000008000000Ch</td><td>MC_Base_Address=80000000h; MC_Index_Position=12</td></tr></tbody></table></div><p>Use Figure 7-272 and Tables 7-244–7-246. MC_Max_Group=3 supports four groups; MC_Num_Group=3 configures four. Both use count-minus-one encoding. MC_Index_Position=12 gives 2<sup>12</sup>=4 KiB per window. The raw MC_Base_Address Register's low six bits encode Index Position; its trailing 0Ch is not part of the base address. With MC_Enable set, Index Position below 12 or Num_Group above Max_Group has undefined behavior. Base address bits below Index Position and those containing the group number must be zero.</p><p>MCG (Multicast Group) labels each window. Locate the address before selecting Ports.</p><figure class="diagram" id="multicast-window-figure"><svg viewBox="0 0 920 310" style="min-width:740px" role="img" aria-labelledby="mc28-en-t mc28-en-d"><title id="mc28-en-t">Four windows select groups, not Ports</title><desc id="mc28-en-d">Address 80002500h falls in group 2. Receive bits select DP2 and DP3; UP0 is not a member and DP1 cannot return to ingress.</desc><text x="460" y="30" text-anchor="middle" font-size="17">MC_Base_Address=80000000h; MC_Index_Position=12</text><rect x="20" y="60" width="210" height="100" rx="8" fill="var(--surface-alt)" stroke="var(--line)" stroke-width="1"/><text x="125" y="92" text-anchor="middle" font-size="17">MCG 0</text><text x="125" y="122" text-anchor="middle" font-size="15">80000000h</text><text x="125" y="147" text-anchor="middle" font-size="15">–80000FFFh</text><rect x="245" y="60" width="210" height="100" rx="8" fill="var(--surface-alt)" stroke="var(--line)" stroke-width="1"/><text x="350" y="92" text-anchor="middle" font-size="17">MCG 1</text><text x="350" y="122" text-anchor="middle" font-size="15">80001000h</text><text x="350" y="147" text-anchor="middle" font-size="15">–80001FFFh</text><rect x="470" y="60" width="210" height="100" rx="8" fill="var(--surface-alt)" stroke="var(--accent)" stroke-width="3"/><text x="575" y="92" text-anchor="middle" font-size="17">MCG 2</text><text x="575" y="122" text-anchor="middle" font-size="15">80002000h</text><text x="575" y="147" text-anchor="middle" font-size="15">–80002FFFh</text><rect x="695" y="60" width="210" height="100" rx="8" fill="var(--surface-alt)" stroke="var(--line)" stroke-width="1"/><text x="800" y="92" text-anchor="middle" font-size="17">MCG 3</text><text x="800" y="122" text-anchor="middle" font-size="15">80003000h</text><text x="800" y="147" text-anchor="middle" font-size="15">–80003FFFh</text><path d="M575 185 V160" stroke="var(--accent)" stroke-width="2"/><polygon points="575,160 570,170 580,170" fill="var(--accent)"/><text x="460" y="215" text-anchor="middle" font-size="17">80002500h → MCG 2; offset=500h</text><text x="460" y="255" text-anchor="middle" font-size="17">MC_Receive[2]=1: DP2 → B; DP3 → C</text><text x="460" y="290" text-anchor="middle" font-size="15">UP0: bit2=0; DP1: no return to ingress</text></svg><figcaption>Author-drawn interpretation of Figure 6-14. MCG, the group number, selects per-Port receive bits; it is not a Port Number.</figcaption></figure><p>A now sends a four-byte Memory Write to 80002500h with AT=10b, using a valid authorized translation. Section 6.14.1 gives MCG=((80002500h−80000000h)&gt;&gt;12)&amp;3Fh=2 and offset 500h. The full hit range is 80000000h–80003FFFh; 80004000h is excluded.</p><p>MC_Enable, type and range must all match. After a Multicast Hit, Multicast processing replaces normal address routing. Only ACS Source Validation can still apply; P2P Request Redirect, Egress Control and Translation Blocking do not choose these copies' exits.</p><p class="source-note">Base 6.0 §§6.14–6.14.1, Figure 6-14, pp.765–768; §§7.9.11–7.9.11.4, Figures 7-272–7-276, Tables 7-243–7-246, pp.1230–1234.</p></section>
<section id="membership"><h2>Distinguish blocked traffic, selected outputs and silent drops</h2><p>At ingress DP1, MC_Block_All[2]=0 and MC_Block_Untranslated[2]=1 permit this AT=10b Multicast Write. Changing AT to 00b causes MC Blocked TLP, not ACS redirection. Compare independent packet conditions:</p><dl class="st-terms" aria-label="Terms in this passage"><div><dt>TLP</dt><dd>Transaction Layer Packet</dd></div></dl><div class="table-wrap"><table><thead><tr><th scope="col">TLP</th><th scope="col">Address</th><th scope="col">AT</th><th scope="col">Block_All</th><th scope="col">Block_Untranslated</th><th scope="col">Result</th></tr></thead><tbody><tr data-mc-outcome="normal"><td>Memory Write</td><td>80002500h</td><td>10b</td><td>0000000000000000h</td><td>0000000000000004h</td><td>DP2 + DP3</td></tr><tr data-mc-outcome="untranslated"><td>Memory Write</td><td>80002500h</td><td>00b</td><td>0000000000000000h</td><td>0000000000000004h</td><td>MC Blocked TLP</td></tr><tr data-mc-outcome="all"><td>Memory Write</td><td>80002500h</td><td>10b</td><td>0000000000000004h</td><td>0000000000000000h</td><td>MC Blocked TLP</td></tr><tr data-mc-outcome="read"><td>Memory Read</td><td>80002500h</td><td>00b</td><td>0000000000000004h</td><td>0000000000000004h</td><td>Unicast</td></tr><tr data-mc-outcome="upper"><td>Memory Write</td><td>80004000h</td><td>10b</td><td>0000000000000000h</td><td>0000000000000000h</td><td>Unicast</td></tr></tbody></table><dl class="st-terms" aria-label="Terms in this passage"><div><dt>TLP</dt><dd>Transaction Layer Packet</dd></div></dl></div><p>After ingress checks, each Port's MC_Receive[2] selects an output. Bit 2 has mask 0000000000000004h. DP2 and DP3 receive copies; UP0 has no selected bit and gets no default upstream copy. DP1 cannot send back through the ingress, even with its own receive bit set.</p><div class="table-wrap"><table><thead><tr><th scope="col">Port</th><th scope="col">MC_Receive</th><th scope="col">Ingress?</th><th scope="col">MC_Overlay_BAR</th><th scope="col">Result</th></tr></thead><tbody><tr data-mc-port="up"><td>UP0</td><td>0000000000000000h</td><td>No</td><td>0000000000000000h</td><td>No copy</td></tr><tr data-mc-port="in"><td>DP1</td><td>0000000000000004h</td><td>Yes</td><td>0000000000000000h</td><td>No return</td></tr><tr data-mc-port="b"><td>DP2</td><td>0000000000000004h</td><td>No</td><td>000000009000000Ch</td><td>90000500h</td></tr><tr data-mc-port="c"><td>DP3</td><td>0000000000000004h</td><td>No</td><td>00000000A000000Ch</td><td>A0000500h</td></tr></tbody></table></div><p>If no eligible egress has MC_Receive[2] set, the packet is silently dropped. An MC_Block_All/MC_Block_Untranslated rejection instead drops the packet and logs/signals MC Blocked TLP under §6.14.4, with the blocking ingress responsible. Neither case creates an ordinary Posted Write Completion.</p><p>Existing Posted Ordering applies through replication and within each output stream. It does not promise simultaneous execution or all-or-nothing completion across recipients.</p><p class="source-note">Base 6.0 §6.14.1, pp.766–768; §6.14.2, p.768; §6.14.4, p.769; §§7.9.11.5–7.9.11.7, Figures 7-277–7-279, Tables 7-247–7-249, pp.1234–1235.</p></section>
<section id="overlay"><h2>Deliver copies to ordinary BARs without hiding ECRC errors</h2><p>DP2/DP3 apply MC_Overlay, an egress address replacement. Figure 7-280/Table 7-250 decode raw 000000009000000Ch as base 90000000h and MC_Overlay_Size=12; DP3 uses base A0000000h. Size below 6 disables Overlay; zero does not specify a one-byte aperture.</p><p>Equation 6-1 preserves address bits 11:0 and replaces the rest from each egress Overlay base. Address 80002500h becomes 90000500h at DP2 and A0000500h at DP3, inside their preconfigured BARs. Overlay acts on exit, not on ingress, and does not allocate the Endpoint BARs.</p><p>ECRC (End-to-End CRC) covers TLP integrity and is affected by the modified address. Apply Table 6-12 separately to each outgoing copy:</p><div class="table-wrap"><table><caption>Table 6-12 applied to each outgoing copy.</caption><thead><tr><th scope="col">Overlay</th><th scope="col">Incoming ECRC</th><th scope="col">Regeneration</th><th scope="col">Forwarding</th></tr></thead><tbody><tr><td>Off</td><td>Any</td><td>Any</td><td>Unmodified</td></tr><tr><td>On</td><td>Absent</td><td>Any</td><td>Modified address</td></tr><tr><td>On</td><td>Present</td><td>Unsupported</td><td>Drop ECRC; TD=0</td></tr><tr><td>On</td><td>Pass</td><td>Supported</td><td>Regenerated ECRC</td></tr><tr><td>On</td><td>Fail</td><td>Supported</td><td>Inverted regenerated ECRC</td></tr></tbody></table></div><p>The example's incoming ECRC passes, so each supported egress regenerates it over its modified TLP. If the original check fails, the egress sends an <strong>inverted regenerated ECRC</strong>, preserving a detectable error. Without regeneration support, it drops ECRC and clears TD. Output address, integrity handling and actual recipient data consumption remain successive observations.</p><p class="source-note">Base 6.0 §6.14.5, Equation 6-1, Table 6-12, pp.769–770; §7.9.11.8, Figure 7-280/Table 7-250, p.1236; regeneration prerequisites: Table 7-244, p.1232.</p></section>
<section id="reading"><h2>Build the next reading route from the actual packet</h2><p>Locate source, target, ingress, egress and direction before reading capability/control. For unicast P2P, connect source/translation checks, Direct Translated P2P and Table 6-11, then RC validation, Completions and errors. For Multicast, confirm the hit before ingress blocking, MC_Receive, output copies and Overlay. Missing destination data alone does not identify one failed component.</p><p>Before changing Multicast base or Index Position, §6.14.3 requires MC_Enable clear in every Function of the component for predictable results. Inconsistent common fields give indeterminate results. Even fields allowed to change at any time have ordered-update requirements. These static comparisons are not a live reconfiguration procedure. Linux P2P policy, IOMMU deployment and driver coordination need platform documents.</p><p class="source-note">Base 6.0 §6.14.3, p.769; §7.9.11, p.1230.</p></section>
<section id="sources"><h2>Edition and complete source route</h2><p>PCI Express Base Specification Revision 6.0 (6.0-1.0-PUB) supplies the rules. Printed and PDF-viewer page numbers match. All topology, register values and packet cases are author-created; no hardware was operated. No external website supplies PCIe technical claims.</p><details class="source-note"><summary>Sources by reading step</summary><ul><li>Scope: §6.12 <em>Access Control Services (ACS)</em>; §6.12.1 <em>ACS Component Capability Requirements</em> and §§6.12.1.1–6.12.1.3, pp.751–756.</li><li>Interactions and recovery: §6.12.2 <em>Interoperability</em>; §6.12.3 <em>ACS Peer-to-Peer Control Interactions</em>; Table 6-11 <em>ACS P2P Request Redirect and ACS P2P Egress Control Interactions</em>, pp.757–758; §6.12.5 <em>ACS Violation Error Handling</em>, pp.759–760; §6.12.6 <em>ACS Redirection Impacts on Ordering Rules</em> and §§6.12.6.1–6.12.6.2, pp.760–761.</li><li>ACS registers: §7.7.11 <em>ACS Extended Capability</em>, §§7.7.11.1–7.7.11.4, pp.1083–1089; Figures 7-131–7-135: <em>ACS Extended Capability</em>, <em>ACS Extended Capability Header</em>, <em>ACS Capability Register</em>, <em>ACS Control Register</em>, <em>Egress Control Vector Register</em>; Tables 7-116–7-119; Equation 7-4 <em>Egress Control Vector Access</em>, p.1088.</li><li>Multicast: §6.14 <em>Multicast Operations</em>, §6.14.1 <em>Multicast TLP Processing</em>, pp.765–768; Figure 6-14 <em>Segmentation of the Multicast Address Range</em>, p.766; §6.14.2 <em>Multicast Ordering</em>, p.768; §6.14.3 <em>Multicast Capability Structure Field Updates</em> and §6.14.4 <em>MC Blocked TLP Processing</em>, p.769.</li><li>Overlay: §6.14.5 <em>MC_Overlay Mechanism</em>, pp.769–770; Equation 6-1 <em>MC_Overlay Transform rules</em> and Table 6-12 <em>ECRC Rules for MC_Overlay</em>, p.770.</li><li>Multicast fields: §7.9.11 <em>Multicast Extended Capability</em>, §§7.9.11.1–7.9.11.8, pp.1230–1236; Figure 7-272 <em>Multicast Extended Capability Structure</em>, p.1231; Figures 7-273–7-280 and Tables 7-243–7-250 locate Header, Capability, Control, MC_Base_Address, MC_Receive, MC_Block_All, MC_Block_Untranslated and MC_Overlay_BAR.</li><li>External boundaries: RC validation algorithms, IOMMU/OS policy, driver coordination and device data persistence need actual platform and device documents. These controls alone do not establish complete isolation or application completion.</li></ul></details></section>
</article>
<nav class="bottom-nav" aria-label="Course and editions"><a href="/DOCS/pcie-course/index.html">Course overview</a><a href="/DOCS/pcie-course/chapter-28.html">Full Chinese tutorial</a><a href="/pcie/chapter-28-zh-tw/">繁體中文</a></nav>
</div>
