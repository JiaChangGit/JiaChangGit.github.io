---
layout: post
title: "PCIe Chapter 22: Link Diagnostics, Lane Margining, and Flit Records"
date: 2026-10-24 00:00:00 +0800
last_modified_at: 2026-10-29 00:00:00 +0800
permalink: /pcie/chapter-22-en/
categories: [PCIe]
tags: [PCIe, Specification]
lang: en
spec_teaching: true
spec_series: pcie
description: "要檢查某條 Lane，設定空間應該怎麼查？"
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
<nav class="bottom-nav" aria-label="Course and editions"><a href="/DOCS/pcie-course/index.html">Course overview</a><a href="/DOCS/pcie-course/chapter-22.html">Full Chinese tutorial</a><a href="/pcie/chapter-22-zh-tw/">繁體中文</a></nav>
<article class="lesson">
<p>Lane Margining examines receiver timing and voltage margin. Start from its Extended Capability (configuration-space extension), then establish port, lane numbering, and readiness before accessing controls and results. Flit logging and error injection serve separate diagnostic purposes.</p><figure class="diagram"><svg viewBox="0 0 900 250" role="img" aria-labelledby="ch22-en-t ch22-en-d"><title id="ch22-en-t">Roles and events in this chapter</title><desc id="ch22-en-d">Locate a Lane capability, check readiness, and find its control and status fields.</desc><g data-walk-target="n0"><rect x="30" y="40" width="350" height="44" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="205.0" y="69" text-anchor="middle" font-size="16">Find the port capability</text></g><g data-walk-target="n1"><rect x="515" y="40" width="350" height="44" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="690.0" y="69" text-anchor="middle" font-size="16">Check mode and readiness</text></g><g data-walk-target="n2"><rect x="515" y="175" width="350" height="44" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="690.0" y="204" text-anchor="middle" font-size="16">Select lane / receiver controls</text></g><g data-walk-target="n3"><rect x="30" y="175" width="350" height="44" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="205.0" y="204" text-anchor="middle" font-size="16">Read results; restore settings</text></g><g data-walk-target="a"><path d="M380 74 L515 74" stroke="var(--accent)" stroke-width="2" fill="none"/><polygon points="515,74 505.0,79.0 505.0,69.0" fill="var(--accent)"/><text x="447.5" y="64.0" text-anchor="middle" font-size="16"></text></g><g data-walk-target="b"><path d="M690 84 L690 175" stroke="var(--accent)" stroke-width="2" fill="none"/><polygon points="690,175 685.0,165.0 695.0,165.0" fill="var(--accent)"/><text x="690.0" y="129.5" text-anchor="middle" font-size="16"></text></g><g data-walk-target="c"><path d="M515 209 L380 209" stroke="var(--accent)" stroke-width="2" fill="none"/><polygon points="380,209 390.0,204.0 390.0,214.0" fill="var(--accent)"/><text x="447.5" y="199.0" text-anchor="middle" font-size="16"></text></g></svg><figcaption>Author-drawn teaching diagram based on PCI Express Base 6.0. Exchanges unrelated to this lesson are omitted.</figcaption></figure><section id="walk"><h2>Which figures lead from an Endpoint to Lane 3?</h2>
<p><strong>[Simulated data] The following data is created for teaching and does not represent specific hardware or a platform.</strong> A Root Port connects directly to an Endpoint, with no Retimer (signal-regenerating component) or Lane Reversal (reversed lane ordering). The Link is in L0 at 16.0 GT/s x4; both ports have a maximum width of x8. We examine active default Lane 3 at the Endpoint receiver, receiving data from the Root Port.</p>
<p>The Root Port is a Downstream Port; the Endpoint port is an Upstream Port. This case controls the Endpoint receiver through its own configuration space. For a multifunction Endpoint, only Function 0 contains this Lane Margining (receiver-margin measurement) capability.</p>
<div class="table-wrap"><table><thead><tr><th scope="col">Reading order</th><th scope="col">Source</th><th scope="col">What to carry forward</th></tr></thead><tbody>
<tr><td>1. Locate the structure</td><td>Figure 7-126 / Table 7-111, p.1080</td><td>Walk the Extended Capability (configuration-space extension) list to ID 0027h, Version 1h; call its base C</td></tr>
<tr><td>2. Locate the lane entry</td><td>Figure 7-125, pp.1079–1080</td><td>Lane 0 Control begins at C+08h, with four bytes per lane: Lane 3 Control=C+14h, Status=C+16h</td></tr>
<tr><td>3. Check readiness</td><td>Figures 7-127 / 7-128, Tables 7-112 / 7-113, pp.1080–1081</td><td>Assume Margining uses Driver Software=0 and Margining Ready=1. Margining Software Ready is undefined in this case and adds no readiness gate</td></tr>
<tr><td>4. Select the receiver</td><td>Figure 4-60, p.553; receiver encodings, p.552</td><td>The Endpoint Upstream Port receiver is Rx(F), Receiver Number=110b; the Root Port's own Rx(A) uses 001b</td></tr>
<tr><td>5. Build and decode commands</td><td>Figures 7-129 / 7-130, Tables 7-114 / 7-115, pp.1082–1083; Table 4-63, pp.554–556</td><td>Chapter 7 supplies field locations; Chapter 4 supplies command and response semantics</td></tr>
</tbody></table></div>
<p>Entries use <strong>default lane numbers</strong>, unaffected by negotiated width or Lane Reversal. Entries beyond Maximum Link Width have undefined values. Separately confirm that the chosen lane belongs to the current width before testing it; our active x4 includes Lane 3.</p>
<p class="source-note">Source: §§7.7.10–7.7.10.5, document/PDF pp.1077–1083; §4.2.18.1 and Figure 4-60, pp.552–553.</p></section>

<section id="margin-session"><h2>How does one command reach a usable response?</h2>
<p>First complete §4.2.18.3 preparation: the current rate must be at least 16.0 GT/s and the tested lane must be active. Program the Upstream Port's Functions to D-states preventing L1 entry, and set ASPM Control (autonomous Link power-saving control) to 00b at both ports. Save Hardware Autonomous Speed Disable and Hardware Autonomous Width Disable; set each to 1 at both ports if writable, and restore the saved values after testing.</p>
<p>Assume preparation is complete and only one lane is tested at a time. Figure 7-129 Control and Figure 7-130 Status share corresponding field positions. Bit 7 is RsvdP (preserve the reserved value), initially 0 here. Values below are whole 16-bit register values, not a memory byte-order illustration.</p>
<figure class="diagram"><svg viewBox="0 0 900 235" style="min-width:640px" role="img" aria-labelledby="margin-fields-title margin-fields-desc"><title id="margin-fields-title">Command and response payloads have different meanings</title><desc id="margin-fields-desc">Control 051E targets Rx F with five timing steps right. Status 821E reports in-progress execution and two errors.</desc>
<text x="30" y="30" font-size="17">Control：051Eh → timing, 5 steps right</text>
<rect x="30" y="48" width="390" height="58" fill="var(--surface-alt)" stroke="var(--line)"/><rect x="420" y="48" width="65" height="58" fill="var(--surface-alt)" stroke="var(--line)"/><rect x="485" y="48" width="75" height="58" fill="var(--surface-alt)" stroke="var(--line)"/><rect x="560" y="48" width="160" height="58" fill="var(--surface-alt)" stroke="var(--line)"/><rect x="720" y="48" width="150" height="58" fill="var(--surface-alt)" stroke="var(--line)"/>
<g text-anchor="middle" font-size="16"><text x="225" y="72">[15:8] Payload=05h</text><text x="225" y="94">Direction and steps</text><text x="452" y="72">[7]</text><text x="452" y="94">RsvdP</text><text x="522" y="72">[6]</text><text x="522" y="94">0b</text><text x="640" y="72">[5:3] Type</text><text x="640" y="94">011b</text><text x="795" y="72">[2:0] Receiver</text><text x="795" y="94">110b：Rx(F)</text></g>
<text x="30" y="147" font-size="17">Status：821Eh → in progress, MErrorCount=2</text><path d="M30 163 H870" stroke="var(--accent)" stroke-width="2"/><text x="30" y="192" font-size="16">Payload=82h：bits [7:6]=10b; bits [5:0]=000010b</text><text x="30" y="220" font-size="16">Usage Model [6]=0b: Lane Margining</text></svg><figcaption>Author-drawn from Figures 7-129 / 7-130 and Table 4-63. Match receiver and command fields, then decode the response payload.</figcaption></figure>
<p><strong>Complete a No Command handshake before changing commands.</strong> Table 4-63 defines Receiver=000b, Type=111b, Payload=9Ch and Usage Model=0b, giving Control=9C38h in this case. Write each new Control atomically, then read Status atomically. Match receiver, type, usage model and the command-specific expected payload. For a No Command response, check Receiver Number Status=000b, Margin Type Status=111b and Usage Model Status=0b. Under Table 7-115, Margin Payload Status is not meaningful for this comparison.</p>
<p>If the Link remains in L0 at 16.0 GT/s or higher, the target must apply and respond to a valid command within 1 ms of receiving it; a Step Margin response can still indicate setup in progress. Section 4.2.18.3 recommends spacing Status reads at least 10 μs apart. If no matching response arrives within 10 ms after a new command, software may declare receiver margining failure. A Configuration Write Completion is a separate event; a margin-command response is also distinct from a Data Link Layer Ack.</p>
<p class="source-note">Source: §§4.2.18.2–4.2.18.3, document/PDF pp.557–561; Figures 7-129 / 7-130 and Tables 7-114 / 7-115, pp.1082–1083.</p></section>

<section id="margin-example"><h2>Query capabilities, then move five timing steps right</h2>
<p>Continue the simulated Rx(F) case. <strong>Every new command row below follows a completed No Command handshake</strong>, including changes only to Payload. Table 4-63 places commands on the left and responses on the right. A Report response replaces the query payload with the requested value.</p>
<div class="table-wrap"><table><thead><tr><th scope="col">Command / observation</th><th scope="col">Control write</th><th scope="col">Status read</th><th scope="col">Interpretation</th></tr></thead><tbody>
<tr data-margin-case="cap"><td>Report Margin Control Capabilities</td><td>880Eh</td><td>150Eh</td><td>Payload=15h: independent error sampler, sample-count reporting, independent left/right timing supported; voltage margining supported; independent up/down voltage not supported</td></tr>
<tr data-margin-case="steps"><td>Report MNumTimingSteps</td><td>8A0Eh</td><td>200Eh</td><td>Reports a maximum of 32 steps</td></tr>
<tr data-margin-case="offset"><td>Report MMaxTimingOffset</td><td>8B0Eh</td><td>190Eh</td><td>Reports a maximum timing offset of 25% of a nominal UI (unit interval)</td></tr>
<tr data-margin-case="limit"><td>Set Error Count Limit</td><td>C516h</td><td>C516h</td><td>Payload high two bits=11b; low six bits=5. The response reports the registered limit of 5</td></tr>
<tr data-margin-case="setup"><td>Step Margin: five steps right, initial read</td><td>051Eh</td><td>401Eh</td><td>Payload high two bits=01b: setup in progress; measurement has not started; error count=0</td></tr>
<tr data-margin-case="running"><td>Same command, later read</td><td>051Eh</td><td>801Eh</td><td>10b: margining in progress; error count=0</td></tr>
<tr data-margin-case="errors"><td>Same command, another read</td><td>051Eh</td><td>821Eh</td><td>10b: still in progress; MErrorCount=2, below the assumed limit of 5</td></tr>
</tbody></table></div>
<p>For example, 880Eh is <code>(88h &lt;&lt; 8) | (001b &lt;&lt; 3) | 110b</code>. Report Margin Control Capabilities payload 15h maps bit 4 to MIndErrorSampler, bit 3 to MSampleReportingMethod, bit 2 to MIndLeftRightTiming, bit 1 to MIndUpDownVoltage and bit 0 to MVoltageSupported. Bit 3=0 selects sample-count reporting. Bit 1=0 disallows selecting up/down independently; voltage support itself is still advertised by bit 0.</p>
<p>For Step Margin payload 05h, §4.2.18.1.2 applies: MIndLeftRightTiming=1 makes bit 6=0 select right, and bits [5:0]=5 select the step count. Table 8-12 requires monotonically increasing offsets, not equally spaced steps. Knowing that 32 steps reach a maximum 25% UI therefore does not establish a proportional time conversion for step 5.</p>
<p>Status 821Eh instead has payload 82h: execution status in the high two bits and MErrorCount (the margin-test error count) in the low six. With the assumed independent sampler, the two errors are sampler bit errors; normal Link traffic may remain error-free. With MIndErrorSampler=0, apply the logical-error conditions in §4.2.18.2, such as a Port entering Recovery. These counts measure different events.</p>
<p>Obtain the sampled amount through the advertised reporting method; our case can use Report MSampleCount after the required handshakes while margining continues. The specification <strong>recommends</strong> at least 10<sup>8</sup> bits per position before moving on, unless the error limit is exceeded. Exclude setup time from actual sampling. The case has not supplied a sampled amount, so these Status reads demonstrate command and execution-state decoding rather than a completed margin assessment at this position. A zero-error snapshot describes only the observed samples.</p>
<p>The other Step Margin statuses are 11b, NAK (unsupported margin command), with MErrorCount=0; and 00b, too many errors, with automatic return to the default sample position. With an independent sampler, ending the test upon exceeding the limit is optional, so read execution status as well. Hardware must not remain in 01b setup for more than 100 ms after receiving a new valid command. Software may declare failure if it still observes 01b 200 ms after issuing the command. The NAK here is a margin-command execution response, distinct from a Data Link Layer Nak requesting replay.</p>
<p class="source-note">Source: §§4.2.18.1–4.2.18.3, Table 4-63 <em>Margin Commands and Corresponding Responses</em>, document/PDF pp.553–561; §8.4.4 and Table 8-12 <em>Lane Margining</em>, pp.1395–1398.</p></section>

<section id="restore"><h2>How is testing in one direction ended?</h2>
<p>No Command separates commands; <strong>it does not return an ongoing Step Margin to the normal sample position</strong>. At the end of each voltage/timing direction, first complete the No Command handshake required before changing commands. Then perform the §4.2.18.3 broadcast sequence below in both Downstream and Upstream Ports. Wait for each target response before proceeding. With no Retimer, the responders are the Root Port's Rx(A) and Endpoint's Rx(F).</p>
<ol><li>Go to Normal Settings: Control=0F10h in this case; return to the normal sample position.</li><li>No Command: Control=9C38h; wait for the handshake.</li><li>Clear Error Log: Control=5510h; clear accumulated margin-test errors.</li><li>No Command: Control=9C38h; check the response again.</li></ol>
<p>Receiver=000b broadcasts these commands. Except for No Command, a response identifies its actual responder: the Endpoint's assumed Go to Normal Settings response is 0F16h, while the Root Port's is 0F11h. Control and Status need not be bit-for-bit identical. Clear Error Log clears margining error records, not every AER (Advanced Error Reporting) status.</p>
<p>When testing finishes, restore the saved autonomous speed/width disable values. If the rate changes during margining, results are inaccurate; software must exit and set Control to No Command so later return to 16.0 GT/s or higher does not restart margining unexpectedly. For Recovery, apply the independent/shared-sampler rules governing suspension, default-position restoration and resumption. A later L0 snapshot does not establish an uninterrupted measurement.</p>
<p class="source-note">Source: §4.2.18, document/PDF p.550; §§4.2.18.1–4.2.18.3, pp.553–561.</p></section>
<section id="logs"><h2>Which questions belong to margining or Flit records?</h2><p>Margining changes test conditions and reports behavior at a selected sample position. For errors recorded during transmission, choose a structure by purpose below. See <a href="/DOCS/pcie-course/chapter-18.html">Chapter 18</a> for Flit Mode (fixed-length transfer-unit mode), formats and replay.</p><div class="table-wrap"><table><thead><tr><th scope="col">Observation</th><th scope="col">Source entry</th><th scope="col">Scope and purpose</th></tr></thead><tbody><tr><td>64.0 GT/s physical-layer status</td><td>§7.7.7 / Figure 7-97, pp.1055–1056</td><td>Equalization and rate-related status; if 64.0 GT/s is unsupported, non-header register behavior is undefined</td></tr><tr><td>Flit error records, counters and FBER measurement</td><td>§7.7.8 / Figure 7-103, pp.1060–1061</td><td>Effective only in Flit Mode. Error logs, counter control/status and FBER (First Bit Error Rate) measurement have distinct fields and conditions</td></tr><tr><td>Initial width and Segment information</td><td>§7.7.9 / Figure 7-120, Table 7-110, pp.1072, 1077</td><td>Device Status 3 Initial Link Width records initial training; read Negotiated Link Width separately for the current width</td></tr><tr><td>Intentional test-error injection</td><td>§7.8.13 / Figure 7-211, pp.1171–1172</td><td>Flit Error Injection (intentional Flit test-error generation) is optional and effective only in Flit Mode; discovery and test activation are separate steps</td></tr></tbody></table></div><p>For a Retimer, the Downstream Port sends commands downstream through Control SKP Ordered Sets (SKP sequences carrying Link-control information) and receives responses upstream. These receivers remain within the same Link. Our Endpoint Rx(F) uses its own Control/Status rather than this Retimer relay path.</p></section>
<section id="result"><h2>What context makes a result reusable?</h2><p>Save port/function, default lane, receiver number, rate/mode, reported capabilities, direction, steps, start/end times, execution status, errors and sampled amount. Record retraining, rate changes and restoration commands as well. These identify whether two observations used the same position, error definition and comparable sample populations.</p><p>Section 7.7.7 notes that 64.0 GT/s parity errors are recorded in the 16.0 GT/s Local, First Retimer and Second Retimer Data Parity Mismatch Status Registers. To track one speed, software <strong>should</strong> clear these records on speed changes; preserve the old records before beginning the next observation interval.</p><p>This case covers capability queries, one timing position and restoration. A full margin profile requires more positions/directions and adequate sampling. Parameters may differ across rates. Voltage margining is optional at 16.0 GT/s and required at 32.0/64.0 GT/s. At 64.0 GT/s, Step Margin applies to all three PAM4 (four-level signaling) eyes simultaneously; use that rate's parameters. Internal receiver observations differ from the <a href="/DOCS/pcie-course/chapter-21.html">external stressed-eye and BER tests in Chapter 21</a> and alone do not establish full electrical compliance.</p><dl class="st-terms" aria-label="Terms in this passage"><div><dt>PAM4</dt><dd>Pulse Amplitude Modulation with 4 levels</dd></div></dl></section><section id="sources"><h2>Edition and sources</h2><p>This chapter uses PCI Express Base Specification Revision 6.0 (6.0-1.0-PUB). Document and PDF page numbers match. Example values are author assumptions, not hardware measurements.</p><details class="source-note"><summary>Complete source locations</summary><ul><li>§4.2.18 <em>Lane Margining at Receiver</em>, pp.550–561; §4.2.18.1 <em>Receiver Number, Margin Type, Usage Model, and Margin Payload Fields</em>, pp.551–557; Figure 4-60 <em>Receiver Number Assignment</em>, p.553; Table 4-63 <em>Margin Commands and Corresponding Responses</em>, pp.554–556.</li><li>§4.2.18.2 <em>Margin Command and Response Flow</em>, pp.557–560; §4.2.18.3 <em>Receiver Margin Testing Requirements</em>, pp.560–561.</li><li>§7.7.10 <em>Lane Margining at the Receiver Extended Capability</em>, pp.1077–1083; Figure 7-125 (layout), pp.1079–1080; Figure 7-126 / Table 7-111 (header), p.1080; Figure 7-127 / Table 7-112 (port capabilities), pp.1080–1081; Figure 7-128 / Table 7-113 (port status), p.1081; Figure 7-129 / Table 7-114 <em>Lane N: Margining Control Register Entry</em>, p.1082; Figure 7-130 / Table 7-115 <em>Lane N: Margining Lane Status Register Entry</em>, p.1083.</li><li>§8.4.4 <em>Lane Margining at the Receiver - Electrical Requirements</em>, pp.1395–1398; Table 8-12 <em>Lane Margining</em>, pp.1396–1398.</li><li>§4.2.3.1.1 <em>PAM4 Signaling</em>, p.343 (FBER); §7.7.7 <em>Physical Layer 64.0 GT/s Extended Capability</em>, pp.1055–1056, Figure 7-97; §7.7.8 <em>Flit Logging Extended Capability</em>, pp.1060–1061, Figure 7-103 <em>Flit Logging Extended Capability Structure</em>; §7.7.9 <em>Device 3 Extended Capability Structure</em>, p.1072, Figure 7-120; §7.7.9.4 / Table 7-110 <em>Device Status 3 Register</em>, p.1077; §7.8.13 <em>Flit Error Injection Extended Capability</em>, pp.1171–1172, Figure 7-211 <em>Flit Error Injection Extended Capability Structure</em>.</li></ul></details></section>
</article>
<nav class="bottom-nav" aria-label="Course and editions"><a href="/DOCS/pcie-course/index.html">Course overview</a><a href="/DOCS/pcie-course/chapter-22.html">Full Chinese tutorial</a><a href="/pcie/chapter-22-zh-tw/">繁體中文</a></nav>
</div>
