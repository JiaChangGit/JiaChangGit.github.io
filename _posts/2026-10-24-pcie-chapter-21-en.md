---
layout: post
title: "PCIe Chapter 21: Receiver, Channel, and Reference Clock"
date: 2026-10-24 00:00:00 +0800
last_modified_at: 2026-10-29 00:00:00 +0800
permalink: /pcie/chapter-21-en/
categories: [PCIe]
tags: [PCIe, Specification]
lang: en
spec_teaching: true
spec_series: pcie
description: "發送端符合規格，為什麼接收端還要另做測試？"
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
<nav class="bottom-nav" aria-label="Course and editions"><a href="/DOCS/pcie-course/index.html">Course overview</a><a href="/DOCS/pcie-course/chapter-21.html">Full Chinese tutorial</a><a href="/pcie/chapter-21-zh-tw/">繁體中文</a></nav>
<article class="lesson">
<p>Rx (Receiver) operates on the signal after the channel. Receiver capability must be evaluated with channel loss, equalization, and Refclk (Reference Clock) conditions. A transmitter waveform alone does not characterize the complete signal path.</p><figure class="diagram"><svg viewBox="0 0 900 420" style="min-width:640px" role="img" aria-labelledby="ch21-en-t ch21-en-d"><title id="ch21-en-t">Actual receiver and calibration-model paths</title><desc id="ch21-en-d">Distinguish the real Rx path from the separate calibration model.</desc><g data-walk-target="tx"><rect x="20" y="60" width="220" height="44" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="130.0" y="89" text-anchor="middle" font-size="16">Source / Tx settings</text></g><g data-walk-target="channel"><rect x="335" y="60" width="240" height="44" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="455.0" y="89" text-anchor="middle" font-size="16">Channel loss and crosstalk</text></g><g data-walk-target="rx"><rect x="650" y="60" width="230" height="44" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="765.0" y="89" text-anchor="middle" font-size="16">Actual Rx under test</text></g><g data-walk-target="clock"><rect x="30" y="300" width="300" height="44" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="180.0" y="329" text-anchor="middle" font-size="16">Refclk architecture and jitter</text></g><g data-walk-target="eye"><rect x="480" y="300" width="390" height="68" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="675.0" y="329" text-anchor="middle" font-size="16">TP2 data + calibration models</text><text x="675.0" y="353" text-anchor="middle" font-size="16">TP2P eye: apply valid conditions</text></g><g data-walk-target="a"><path d="M240 94 L335 94" stroke="var(--accent)" stroke-width="2" fill="none"/><polygon points="335,94 325.0,99.0 325.0,89.0" fill="var(--accent)"/><text x="287.5" y="84.0" text-anchor="middle" font-size="16">Signal</text></g><g data-walk-target="b"><path d="M575 94 L650 94" stroke="var(--accent)" stroke-width="2" fill="none"/><polygon points="650,94 640.0,99.0 640.0,89.0" fill="var(--accent)"/><text x="612.5" y="84.0" text-anchor="middle" font-size="16">Input</text></g><g data-walk-target="c"><path d="M330 334 L480 334" stroke="var(--accent)" stroke-width="2" fill="none"/><polygon points="480,334 470.0,339.0 470.0,329.0" fill="var(--accent)"/><text x="405.0" y="324.0" text-anchor="middle" font-size="16">Clock conditions</text></g><g data-walk-target="d"><path d="M455 104 V190 H675 V300" stroke="var(--accent)" stroke-width="2" fill="none"/><polygon points="675,300 670,290 680,290" fill="var(--accent)"/><text x="570" y="175" text-anchor="middle" font-size="16">Replica path during calibration</text></g></svg><figcaption><p>Author-drawn relationships: real receiver path above, separate calibration-model path below. Models are not appended to the measured DUT output.</p></figcaption></figure>
<section id="receiver"><h2>Separate the calibrated eye from the receiver result</h2><p>Rx (Receiver) testing first establishes a prescribed stressed input, then tests the actual receiver. A stressed eye combines specified channel loss, jitter, and interference. Successful calibration prepares the stimulus; it does not supply the DUT (Device Under Test) result.</p><p>Section 8.4.1 defines the recovered eye at the receiver latch input. At 2.5/5.0 GT/s this corresponds to Rx pins. At 8.0/16.0/32.0/64.0 GT/s it corresponds to the Rx die-pad signal after behavioral equalization. Measurement plus models constructs this inaccessible reference point.</p><p>The worked case uses 16.0 GT/s and builds on the preceding chapter's voltage/reference-plane explanation.</p><p class="source-note">Base 6.0 §8.4.1 <em>Receiver Stressed Eye Specification</em> (p.1357); §8.4.2.1 <em>Procedure for Calibrating a Stressed EH/EW Eye</em> (pp.1376–1379); §8.4.2.2 <em>Procedure for Testing Rx DUT</em> (p.1382 onward).</p></section>

<section id="rx-calibration"><h2>16.0 GT/s Endpoint: from the channel row to DUT testing</h2><div class="example"><p><strong>Simulated data:</strong> Author-created teaching data, not device or platform measurements. The DUT is an Endpoint supporting 32.0 GT/s. Test one Rx Lane at 16.0 GT/s with Common Refclk (CC). A test source drives the Endpoint; channel and eye values below are assumed.</p><h3>1. Select the row by the receiving component</h3><p>In §8.4.1.2 select <em>16.0 GT/s Non-Root Port</em> in Table 8-8, because the DUT is an Endpoint. The source's location does not choose the row. Nominal channel loss is 4.2–5.2 dB at 1 GHz and 24.5–25.5 dB at 8 GHz. The Root Port high-frequency row differs.</p><div class="table-wrap"><table><thead><tr><th scope="col">Frequency</th><th scope="col">Assumed SDD21</th><th scope="col">Positive loss magnitude</th><th scope="col">Selected nominal range</th></tr></thead><tbody><tr><td>1 GHz</td><td>−4.7 dB</td><td>4.7 dB</td><td>4.2–5.2 dB</td></tr><tr><td>8 GHz</td><td>−25.0 dB</td><td>25.0 dB</td><td>24.5–25.5 dB</td></tr></tbody></table></div><p>SDD21 describes differential-input to differential-output transmission. Negative dB here records attenuation, while the table lists positive loss. These two samples fit their nominal ranges but do not verify the complete mask, return loss, or other channel conditions. Figure 8-27 illustrates 8.0 GT/s; use its axes and boundaries as a reading example, and Table 8-8 for the actual 16.0 GT/s values.</p><p>The channel must also provide a series of loss options covering at least 2 dB below the high-frequency nominal minimum through 3 dB above the maximum. This case therefore needs at least <code>22.5–28.5 dB</code>, with adjacent options no more than <code>0.5 dB</code> apart. Those options support stress adjustment; a lone 25 dB result does not finish eye calibration.</p><h3>2. Follow TP2 and TP2P separately in Figure 8-26</h3><p>The upper calibration path runs from the source through the calibration and Replica Channels to TP2. Post-processing adds behavioral Rx package, equalization, and CDR (Clock and Data Recovery) models to construct the TP2P recovered eye. These models do not mandate matching internal DUT circuitry.</p><p>The lower path is used after calibration: reconnect the source to the actual DUT's Breakout Channel, then obtain its BER (Bit Error Rate). The upper-path package/equalization models are not physical components after the DUT and are not applied again to its measured BER.</p><p><strong>Record each loss reference separately.</strong> Section 8.4.1.2 describes calibration-channel SDD21 from TP3 to TP2. Section 8.4.2.1 specifically retains TP1–TP3 cable loss in the 16.0 GT/s total-channel methodology, while 32.0/64.0 GT/s treat that cable as part of the generator. The two nominal channel samples above do not replace the total loss used at every later step.</p><h3>3. Read Table 8-10 with Notes 4 and 8</h3><p>In the 16.0 GT/s column, <code>TRX-UI=62.5 ps</code>, target eye width <code>TRX-ST=0.30 UI</code>, and target eye height <code>VRX-ST=15 mVPP</code>. EH means Eye Height and EW means Eye Width, giving nominal width <code>0.30 × 62.5 = 18.75 ps</code>.</p><p>Note 4 references these targets to TP2P. Raw TP2 opening is not the target quantity. Note 8 turns common-mode interference off for EH/EW calibration and on for the stressed-eye jitter test. Here <code>VRX-CM-INT</code> is a 120 MHz, 150 mVPP single tone, measured at TP2 without post-processing.</p><p>Next follow the 16.0 GT/s procedure in §8.4.2.1: establish the applicable stresses and initial channel, select a Tx preset (predefined equalization setting) using modeled eye area, increase channel loss, then reselect the preset and adjust Sj (Sinusoidal Jitter), differential interference, and swing to a legal final combination. Figure 8-42 places these controls at the source, channel, and processing blocks.</p><h3>4. Repeated measurements check a calibration window</h3><p>Assume the other calibration steps and tool requirements have been completed for these conditions. The following excerpt gives five TP2P results for one final setting, evaluated by post-processing at the 10<sup>−12</sup> BER condition. Actual DUT errors are measured in step 5. The procedure requires at least five measurements, with enough measurements for stability. Final 16.0 GT/s mean EH must be 15 ± 1.5 mV and mean EW 18.75 ± 0.5 ps.</p><div class="table-wrap"><table><thead><tr><th scope="col">Calibration quantity</th><th scope="col">Five assumed values</th><th scope="col">Mean</th><th scope="col">Final mean window</th></tr></thead><tbody><tr data-rx-check="eh"><td>EH</td><td>14.5, 15.0, 15.5, 15.2, 14.8 mVPP</td><td>15 mVPP</td><td>13.5–16.5 mVPP</td></tr><tr data-rx-check="ew"><td>EW</td><td>18.5, 18.8, 18.9, 18.6, 18.95 ps</td><td>18.75 ps</td><td>18.25–19.25 ps</td></tr></tbody></table></div><p>Both means fit their final windows. With channel, stress, and preset-selection steps also complete, this setting can be used for DUT testing. An out-of-window result first returns to stimulus adjustment; the Endpoint receive result has not yet been obtained at that stage.</p><figure class="diagram"><svg viewBox="0 0 900 660" style="min-width:640px" role="img" aria-labelledby="rx-calibration-title rx-calibration-desc"><title id="rx-calibration-title">Calibration and DUT testing are separate stages</title><desc id="rx-calibration-desc">TP2 captures feed behavioral package, equalization and CDR models to produce TP2P eye targets. Valid calibration precedes moving the source to the DUT and testing BER. Invalid calibration returns to stress adjustment.</desc><text x="450" y="32" text-anchor="middle" font-size="21">A. Calibrate the applied stress</text><rect x="210" y="55" width="480" height="75" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="450" y="84" text-anchor="middle" font-size="18">Source → channel + replica → TP2</text><text x="450" y="110" text-anchor="middle" font-size="17"></text><rect x="210" y="155" width="480" height="75" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="450" y="184" text-anchor="middle" font-size="18">Rx package + behavioral EQ / CDR</text><text x="450" y="210" text-anchor="middle" font-size="17">TP2P: calibrated EH / EW</text><rect x="210" y="470" width="480" height="75" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="450" y="499" text-anchor="middle" font-size="18">Source → channel + breakout → Rx DUT</text><text x="450" y="525" text-anchor="middle" font-size="17">Lock, required stresses and Sj profile</text><polygon points="450,265 630,330 450,395 270,330" fill="var(--surface-alt)" stroke="var(--line)"/><text x="450" y="337" text-anchor="middle" font-size="18">Valid calibration?</text><path d="M630 330 H810 V92 H690" stroke="var(--accent)" stroke-width="2" fill="none"/><polygon points="690,92 700,87 700,97" fill="var(--accent)"/><text x="725" y="365" text-anchor="middle" font-size="16">No: adjust stress / loss</text><text x="470" y="420" font-size="16">Yes: reconnect cables</text><text x="450" y="455" text-anchor="middle" font-size="21">B. Test the real receiver</text><text x="450" y="610" text-anchor="middle" font-size="19">BER result over the required test conditions</text><path d="M450 130 V155" stroke="var(--accent)" stroke-width="2" fill="none"/><polygon points="450,155 445,145 455,145" fill="var(--accent)"/><path d="M450 230 V265" stroke="var(--accent)" stroke-width="2" fill="none"/><polygon points="450,265 445,255 455,255" fill="var(--accent)"/><path d="M450 395 V435" stroke="var(--accent)" stroke-width="2" fill="none"/><polygon points="450,435 445,425 455,425" fill="var(--accent)"/><path d="M450 545 V580" stroke="var(--accent)" stroke-width="2" fill="none"/><polygon points="450,580 445,570 455,570" fill="var(--accent)"/></svg><figcaption>Author-organized stages. The Replica calibration path and Breakout/DUT test path are used at different stages; model blocks are not additional receiver circuitry.</figcaption></figure><dl class="st-terms" aria-label="Terms in this passage"><div><dt>EQ</dt><dd>Equalization</dd></div></dl><h3>5. Reconnect the DUT and check the test coverage</h3><p>Section 8.4.2.2.1 requires the BERT (Bit Error Rate Tester) Tx to send Modified Compliance Pattern. The calibration preset is fixed during calibration, while DUT testing permits the specified optimization with the real receiver. Common-mode and other stresses must also use their test-stage settings. Section 8.4.2 requires other DUT PCIe Lanes to send or receive data; activity on other supported I/O is recommended.</p><p>This case uses 16.0 GT/s CC and a device supporting 32.0 GT/s, so read Figure 8-45 for the Sj mask. Follow its frequency and Sj-amplitude (UI) axes, then the surrounding rules: after initial CDR lock, apply the specified swept-Sj conditions. Test 33 kHz separately rather than leaving that tone on during other frequency measurements. For 16.0 GT/s, the additional 210 MHz tone uses the calibration's 100 MHz Sj amplitude minus 0.1 UI; omit that tone if calibration Sj was below 0.1 UI. Carry this value forward from the calibration record, not just its final EH/EW.</p><p>Assume the DUT report preserves only “CDR locked” and “no observed errors at one swept-frequency point.” Test volume, error counts, other selected points, and complete stress conditions are still missing. At 16.0 GT/s the target is BER <code>10<sup>−12</sup></code> over the applicable range. The specification does not require testing every continuous frequency, but recommends enough points to catch possible resonances and explicitly requires 33 kHz. One zero-error summary is insufficient.</p></div><p class="source-note">Base 6.0 §§8.4.1.1–8.4.1.2, Figure 8-26 <em>Rx Test board Topology for 16.0 and 32.0 GT/s</em>, Table 8-8 <em>Calibration Channel IL Limits</em> (pp.1357–1361); §8.4.2.1, Figure 8-42 <em>Layout for Calibrating the Stressed Jitter Eye at 16.0, 32.0, and 64.0 GT/s</em> (pp.1376–1379); Table 8-10 <em>Stressed Jitter Eye Parameters</em>, Notes 4/8 (p.1380); §8.4.2.2.1 <em>Sj Mask</em> (pp.1382–1385), Figure 8-45 (p.1385).</p></section>

<section id="channel"><h2>Connect calibration channels to the platform-channel boundary</h2><p>The preceding calibration channel generates a receiver-test stimulus. Platform-channel compliance follows §8.5.1. A captive channel is one whose full Tx-pin to Rx-pin path is comprehended by the platform design. Split-board/component designs refer to the appropriate form-factor specification, such as CEM, which takes precedence for that allocation. No unprovided form-factor values are imported here.</p><p>Follow Figures 8-56/8-57 from channel characteristics through behavioral Tx/Rx package models to a die-pad-to-die-pad topology. Include the victim path and enough aggressor paths to capture crosstalk, then apply the appropriate Tx conditions, equalization, and clock recovery.</p><p>Figure 8-57's official title names only 8.0 and 16.0 GT/s; neighboring text supplies 32.0/64.0 GT/s requirements. The 16.0 GT/s channel model uses a first-order CTLE (Continuous-Time Linear Equalizer) and two-tap DFE (Decision Feedback Equalizer) as a minimum-capability model. This is not mandated DUT circuitry, nor the preceding chapter's Tx test channel.</p><p class="source-note">Base 6.0 §8.5.1 <em>Channel Compliance Testing</em> (pp.1400–1402); Figures 8-56 <em>Flow Diagram for Channel Tolerancing at 2.5 and 5.0 GT/s</em> and 8-57 <em>Flow Diagram for Channel Tolerancing at 8.0 and 16.0 GT/s</em> (p.1401); §8.5.1.1 <em>Behavioral Transmitter and Receiver Package Models</em> (p.1402 onward).</p></section>

<section id="clock"><h2>Keep clock architecture in the analysis</h2><p>Refclk (Reference Clock) is more than a connection on a drawing. Common Refclk in §8.6.6 distributes one source to Tx and Rx, so some low-frequency movement propagates jointly. Relative timing at the latch also depends on Tx/Rx PLLs (Phase-Locked Loops), CDR, and transport-delay differences.</p><p>In Figure 8-89 locate the common source branches and the difference between transmitted data and receiver sampling-clock paths. Section 8.6.5 separates edge filtering, which reduces measurement-sampling artifacts, from behavioral filtering by PLLs, CDR, and applicable transport delay. Their combination yields effective Refclk jitter at the latch rather than a simple sum of raw jitter.</p><p>Section 8.6.4 does not define matching Refclk transfer functions and jitter limits for Independent Refclk (IR) there; other transmitter and receiver requirements still apply. Changing this case to IR requires a new Sj profile/model selection rather than reusing CC Figure 8-45. See <a href="/DOCS/pcie-course/chapter-20.html#clock-route">Chapter 20</a> for the already explained Tx clock-sampling table.</p><p>Refclk testing in §8.6.1 tests the clock source, while the worked case tests the Rx. Keep each test's reference point and result separate before connecting them into one analysis.</p><p class="source-note">Base 6.0 §8.6.1 <em>Refclk Test Setup</em> (p.1420); §§8.6.4 <em>Refclk Architectures Supported</em> and 8.6.5 <em>Filtering Functions Applied to Raw Data</em> (p.1426); §8.6.6 <em>Common Refclk Rx Architecture (CC)</em>, Figure 8-89 <em>Common Refclk Rx Architecture for all Data Rates Except 32.0 and 64.0 GT/s</em> (p.1428).</p></section>

<section id="sources"><h2>Edition and sources</h2><p>PCI Express Base Specification Revision 6.0 (6.0-1.0-PUB) is the authority. Printed and PDF-viewer pages match at these locations. Assumed readings and stage excerpts are author-created, not measurements or certification.</p><details class="source-note"><summary>Reading locations and purpose</summary><ul><li>§8.4.1 (p.1357): recovered-eye reference points; §§8.4.1.1–8.4.1.2, Figure 8-26, Figure 8-27 <em>Example Calibration Channel IL Mask Excluding Rx Package for 8.0 GT/s</em>, Table 8-8 (pp.1357–1361): channel and reference points.</li><li>§8.4.2 <em>Stressed Eye Test</em>, §8.4.2.1 (pp.1376–1379): source/channel/preset/stress adjustments; final 16.0 GT/s mean windows on p.1377 and cable inclusion on p.1376.</li><li>Table 8-10 (pp.1380–1381): targets, units, Notes 4/8; §8.4.2.1.1 <em>Post Processing Tool Requirements</em> (p.1381): tool consistency.</li><li>§§8.4.2.2 / 8.4.2.2.1 (pp.1382–1385): DUT pattern, lock, and Sj test; Figure 8-45 <em>Sj Mask for Receivers Operating in CC mode at 16.0 GT/s</em> (p.1385).</li><li>§8.5.1, Figures 8-56/8-57 (pp.1400–1402): platform boundary and minimum models; §8.6.1, §§8.6.4–8.6.6, Figure 8-89 (pp.1420, 1426–1428): Refclk setup, architecture, and filtering.</li></ul></details></section>
</article>
<nav class="bottom-nav" aria-label="Course and editions"><a href="/DOCS/pcie-course/index.html">Course overview</a><a href="/DOCS/pcie-course/chapter-21.html">Full Chinese tutorial</a><a href="/pcie/chapter-21-zh-tw/">繁體中文</a></nav>
</div>
