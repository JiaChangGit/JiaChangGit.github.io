---
layout: post
title: "PCIe Chapter 20: Transmitter Electrical Requirements"
date: 2026-10-24 00:00:00 +0800
last_modified_at: 2026-10-29 00:00:00 +0800
permalink: /pcie/chapter-20-en/
categories: [PCIe]
tags: [PCIe, Specification]
lang: en
spec_teaching: true
spec_series: pcie
description: "要判讀發送端電氣規格，為什麼不能先抄一個電壓上限？"
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
<nav class="bottom-nav" aria-label="Course and editions"><a href="/DOCS/pcie-course/index.html">Course overview</a><a href="/DOCS/pcie-course/chapter-20.html">Full Chinese tutorial</a><a href="/pcie/chapter-20-zh-tw/">繁體中文</a></nav>
<article class="lesson">
<p>Tx (Transmitter) limits depend on the measurement reference point, clock architecture, rate, and test pattern. Begin with the path in Figure 8-1, then connect voltage, equalization, and jitter to the applicable conditions.</p><figure class="diagram"><svg viewBox="0 0 900 420" role="img" aria-labelledby="ch20-en-t ch20-en-d"><title id="ch20-en-t">Tx measurement path and reference conditions</title><desc id="ch20-en-d">Choose the transmitter measurement point and its applicable test conditions.</desc><g data-walk-target="dut"><rect x="20" y="60" width="230" height="44" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="135.0" y="89" text-anchor="middle" font-size="16">Tx under test</text></g><g data-walk-target="breakout"><rect x="335" y="60" width="230" height="44" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="450.0" y="89" text-anchor="middle" font-size="16">Breakout channel</text></g><g data-walk-target="scope"><rect x="650" y="60" width="230" height="44" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="765.0" y="89" text-anchor="middle" font-size="16">Measurement equipment</text></g><g data-walk-target="ref"><rect x="20" y="290" width="230" height="44" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="135.0" y="319" text-anchor="middle" font-size="16">Reference clock conditions</text></g><g data-walk-target="process"><rect x="470" y="290" width="410" height="68" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="675.0" y="319" text-anchor="middle" font-size="16">Select processing / reference plane</text><text x="675.0" y="343" text-anchor="middle" font-size="16">Check parameter, units, and notes</text></g><g data-walk-target="a"><path d="M250 94 L335 94" stroke="var(--accent)" stroke-width="2" fill="none"/><polygon points="335,94 325.0,99.0 325.0,89.0" fill="var(--accent)"/><text x="292.5" y="84.0" text-anchor="middle" font-size="16">Signal</text></g><g data-walk-target="b"><path d="M565 94 L650 94" stroke="var(--accent)" stroke-width="2" fill="none"/><polygon points="650,94 640.0,99.0 640.0,89.0" fill="var(--accent)"/><text x="607.5" y="84.0" text-anchor="middle" font-size="16">Waveform</text></g><g data-walk-target="c"><path d="M135 290 L135 104" stroke="var(--accent)" stroke-width="2" fill="none"/><polygon points="135,104 140.0,114.0 130.0,114.0" fill="var(--accent)"/><text x="230" y="210" text-anchor="middle" font-size="16">Architecture</text></g><g data-walk-target="d"><path d="M765 104 L675 290" stroke="var(--accent)" stroke-width="2" fill="none"/><polygon points="675,290 675.4856429311786,278.8302125828915 684.227215692394,283.6866418946778" fill="var(--accent)"/><text x="795" y="210" text-anchor="middle" font-size="16">Post-process</text></g></svg><figcaption>Author-drawn measurement overview. Select processing for the actual parameter and retain its method and exceptions.</figcaption></figure>
<section id="setup"><h2>Connect the accessible point to the specified reference plane</h2><p>In Figure 8-1 locate the DUT (Device Under Test) Tx pins, the Breakout Channel leading to connectors, and accessible point TP1. A waveform captured at TP1 includes that channel's effects.</p><p>Next locate the Replica Channel and its TP2/TP3 ends. It reproduces the breakout path's electrical characteristics to help refer measurements to the pins; it is not another series path traversed by Tx data. Section 8.3.1.1 de-embeds voltage parameters to pins unless stated otherwise.</p><p>De-embedding removes measurement-path effects using channel characteristics. It is not subtraction of a fixed voltage or jitter value. Section 8.3.5.2 also explains high-frequency noise amplification and the applicable processing limits.</p><p>Record the DUT/Lane, rate, full/reduced swing, pattern, clock architecture, measurement point, and processing before comparing a report with a parameter limit.</p><p class="source-note">Base 6.0 §8.3.1 <em>Measurement Setup for Characterizing Transmitters</em>, Figure 8-1 <em>Tx Test Board for Non-Embedded Refclk</em> (p.1318); §8.3.1.1 <em>Breakout and Replica Channels</em> (pp.1319–1320); §§8.3.5.1–8.3.5.2 (pp.1336–1337).</p></section>

<section id="clock-route"><h2>Choose sampling and processing from the clock architecture</h2><p>Refclk (Reference Clock) location, availability at DUT pins, and SRIS testing (separate reference clocks with independent spread spectrum) affect the method. In Table 8-5 select the column and row before reading their intersection.</p><div class="table-wrap"><table><thead><tr><th scope="col">Selected conditions</th><th scope="col">Table 8-5 position</th><th scope="col">Sampling and processing</th></tr></thead><tbody><tr><td>Non-Embedded Refclk; available at DUT pins; not testing SRIS</td><td>Right column, first row</td><td>1-port measurement, CC CDR, clean external Refclk</td></tr><tr><td>Embedded Refclk; available at DUT pins; not testing SRIS</td><td>Left column, first row</td><td>2-port measurement, CC CDR, PLL (note 1), and 10 ns transport delay</td></tr></tbody></table></div><p>CDR (Clock and Data Recovery) here is the processing model; CC means Common Clock. The second row captures Tx data and Tx Refclk simultaneously to remove shared clock jitter. This choice is separate from D+ and D− being two conductors. Obtain PLL (Phase-Locked Loop) characteristics from the rate-specific Refclk section and transport delay from §8.6.6; do not silently set the latter to zero.</p><p>For Independent Refclk (IR), §8.3.5.3 requires single-port jitter measurement with the appropriate model CDR. The table above reads only two selected combinations; use the full table for others. A DUT supporting several Refclk modes needs testing in each supported mode.</p><p class="source-note">Base 6.0 Figure 8-2 <em>Tx Test board for Embedded Refclk</em> (p.1319); §§8.3.5.3 <em>Independent Refclk Measurement and Post Processing</em> and 8.3.5.4 <em>Embedded and Non-Embedded Refclk Measurement and Post Processing</em>, Table 8-5 <em>Tx Measurement and Post Processing For Different Refclks</em> (p.1338).</p></section>

<section id="voltage"><h2>Identify the voltage quantity before looking up its limit</h2><p>Read §8.3.2, then Figure 8-3. D+ and D− are individual single-ended voltages. Subtract them for differential voltage and average them for common mode.</p><p><code>VDIFF = VD+ − VD−</code>; <code>VCM = (VD+ + VD−) / 2</code>. Peak-to-peak voltage, written mVPP here, is the maximum minus minimum of the same quantity. Equation 8-1's <code>VDIFFp-p = 2 × max|VD+ − VD−|</code> specifically assumes a symmetric differential swing.</p><p>Figure 8-3 relates these waveforms; it does not let an arbitrary curve height stand in for a specified Tx measurement. Follow the applicable §8.3.3.6 or §8.3.3.7 method, then select the rate, parameter, and units in Table 8-6.</p><p class="source-note">Base 6.0 §8.3.2 <em>Voltage Level Definitions</em>, Equations 8-1 <em>VDIFFp-p</em> and 8-2 <em>VTX-AC-CM-PP</em> (p.1320); Figure 8-3 <em>Single-ended and Differential Levels</em> (p.1321).</p></section>

<section id="voltage-case"><h2>Why does 450 mVPP single-ended become 900 mVPP differential?</h2><div class="example"><p><strong>Simulated data:</strong> Author-created teaching data, not a device/platform measurement. Assume one Endpoint Tx Lane driving from the DUT toward TP1 at 5.0 GT/s, full swing, Non-Embedded Refclk, clean external clock, and no SRIS test. The chosen method is 1-port measurement with CC CDR. Assume the applicable compliance test load and the channel processing required for differential voltage.</p><p>Section 8.3.3.6 uses average transition eye amplitude at 0.5 UI over 500 Compliance Pattern repetitions at 2.5/5.0 GT/s. The following are idealized representative levels under that assumption; they explain amplitudes without modeling edges, overshoot, or noise. UI (Unit Interval) supplies the time unit for that sampling location.</p><div class="table-wrap"><table><thead><tr><th scope="col">Complementary representative state</th><th scope="col">D+ (mV)</th><th scope="col">D− (mV)</th><th scope="col">VDIFF (mV)</th><th scope="col">VCM (mV)</th></tr></thead><tbody><tr data-voltage-state="high"><td>H</td><td>825</td><td>375</td><td>+450</td><td>600</td></tr><tr data-voltage-state="low"><td>L</td><td>375</td><td>825</td><td>−450</td><td>600</td></tr></tbody></table></div><p>State H gives <code>825 − 375 = +450 mV</code>; state L gives <code>375 − 825 = −450 mV</code>. Differential peak-to-peak is therefore <code>+450 − (−450) = 900 mVPP</code>. Each individual conductor varies from 375 to 825 mV, only <code>450 mVPP</code> single-ended. Both states give <code>600 mV</code> common mode, an average potential rather than differential swing.</p><figure class="diagram"><svg viewBox="0 0 900 460" style="min-width:640px" role="img" aria-labelledby="voltage-levels-title voltage-levels-desc"><title id="voltage-levels-title">Single-ended and differential voltage in the author case</title><desc id="voltage-levels-desc">Complementary 825/375 mV single-ended levels produce +450/-450 mV differential levels, a 900 mV differential peak-to-peak swing, and 600 mV common mode.</desc><text x="450" y="30" text-anchor="middle" font-size="19">Single-ended: D+ solid / D− dashed</text><text x="90" y="85" font-size="17">825 mV</text><text x="90" y="170" font-size="17">375 mV</text><path d="M185 80 H330 V165 H480 V80 H630 V165 H780" stroke="var(--accent)" stroke-width="3" fill="none"/><path d="M185 165 H330 V80 H480 V165 H630 V80 H780" stroke="var(--accent)" stroke-width="2" stroke-dasharray="7 5" fill="none"/><path d="M810 80 H830 V165 H810" stroke="var(--accent)" stroke-width="2" fill="none"/><text x="845" y="128" text-anchor="middle" font-size="15">450</text><text x="845" y="150" text-anchor="middle" font-size="15">mVPP</text><text x="450" y="232" text-anchor="middle" font-size="19">Differential: D+ − D−</text><text x="90" y="286" font-size="17">+450 mV</text><text x="115" y="330" font-size="17">0 mV</text><text x="90" y="373" font-size="17">−450 mV</text><path d="M185 325 H780" stroke="var(--line)" stroke-dasharray="4 5" fill="none"/><path d="M185 280 H330 V370 H480 V280 H630 V370 H780" stroke="var(--accent)" stroke-width="3" fill="none"/><path d="M810 280 H830 V370 H810" stroke="var(--accent)" stroke-width="2" fill="none"/><text x="845" y="327" text-anchor="middle" font-size="15">900</text><text x="845" y="350" text-anchor="middle" font-size="15">mVPP</text><text x="450" y="425" text-anchor="middle" font-size="18">VCM = (D+ + D−) / 2 = 600 mV</text></svg><figcaption>Author-drawn idealized waveforms with no time scale, transition duration, or noise. The two plots use their labeled voltage scales. Common-mode 600 mV is not the differential zero.</figcaption></figure><h3>Follow Note 3 back to the method</h3><p>In Table 8-6 choose <code>VTX-DIFF-PP</code> and the 5.0 GT/s column. Full-swing differential peak-to-peak voltage is <code>800–1000 mVPP</code>. Note 3 points to §§8.3.3.6 / 8.3.3.7. Compare 900 mVPP from this case, rather than the 450 mVPP of D+ alone.</p><p>Under the stated measurement assumptions, that one swing result is in range. Jitter, common-mode noise, equalization, and other requirements need their own measurements. Two representative levels yielding 600 mV do not prove that a complete waveform has no AC common-mode noise.</p><p>Reduced-swing operation selects the separate <code>VTX-DIFF-PP-LOW</code> row. Both rows have a 1000 mVPP maximum in this edition, but different minima. A copied upper limit loses that mode distinction.</p></div><p class="source-note">Base 6.0 §8.3.3.6 <em>Method for Measuring VTX-DIFF-PP at 2.5 GT/s and 5.0 GT/s</em> (p.1326); Table 8-6 <em>Data Rate Dependent Transmitter Parameters</em>, differential-swing rows (p.1348), Note 3 (p.1351).</p></section>

<section id="equalization"><h2>Change methods when the rate and preset change</h2><p>At 2.5/5.0 GT/s Tx equalization is de-emphasis, measured using the specified transition/non-transition average eye-amplitude ratio in §§8.3.3.1 / 8.3.3.4. Higher rates use coefficients and presets (predefined equalization combinations). Two representative levels from the preceding case are not a complete preset test.</p><p>For swing at 8.0/16.0/32.0/64.0 GT/s, §8.3.3.7 sets the applicable precursor/postcursor coefficients to zero and uses a low-frequency Compliance Pattern segment: 64 zeros then 64 ones at 8.0/16.0/32.0 GT/s, or 64 PAM4 level-0 then 64 level-3 symbols at 64.0 GT/s. Measure the specified late portion of each half-cycle and average 500 repetitions.</p><dl class="st-terms" aria-label="Terms in this passage"><div><dt>PAM4</dt><dd>Pulse Amplitude Modulation with 4 levels</dd></div></dl><p>For the preset itself, Figure 8-7 compares measured equalized output with a reconstruction made by applying coefficients to measured unequalized output, finding the best fit. Table 8-1 applies to 8.0/16.0/32.0 GT/s; Table 8-2 applies to 64.0 GT/s. Their ratios and tolerances define presets; coefficient magnitude is not output-voltage magnitude.</p><p>This connects to <a href="/DOCS/pcie-course/chapter-19.html#equalization">Chapter 19</a>: the Link exchanges setting requests, while this chapter checks the resulting output. A requested setting, finished training, and a passed electrical requirement are separate observations.</p><p class="source-note">Base 6.0 §§8.3.3.1–8.3.3.3 (pp.1321–1323); Tables 8-1 / 8-2 (pp.1324–1325); §§8.3.3.4–8.3.3.7 and Figure 8-7 <em>Methodology for measuring Tx equalization coefficients and presets</em> (pp.1325–1326).</p></section>

<section id="jitter"><h2>Use the measured jitter quantity to select the pattern</h2><p>Jitter (timing variation of edges or pulse widths) depends on pattern, equalization, and processing. Start with §8.3.5 before selecting a Table 8-6 parameter row.</p><div class="table-wrap"><table><thead><tr><th scope="col">Rate and measured quantity</th><th scope="col">Pattern in §8.3.5</th><th scope="col">Tx equalization condition</th></tr></thead><tbody><tr><td>2.5 / 5.0 GT/s jitter</td><td>Compliance Pattern, with specified zero-crossing treatment</td><td>Use the applicable rate-specific de-emphasis setting</td></tr><tr><td>8.0 / 16.0 GT/s jitter</td><td>Compliance Pattern, with specified zero-crossing treatment</td><td>The preset yielding the lowest jitter should be selected</td></tr><tr><td>32.0 GT/s jitter</td><td>Jitter Measurement Pattern</td><td>Must use no Tx equalization</td></tr><tr><td>64.0 GT/s uncorrelated total jitter and deterministic jitter</td><td>Jitter Measurement Pattern, all twelve transitions between four PAM4 levels</td><td>Must use no Tx equalization</td></tr><tr><td>64.0 GT/s uncorrelated total pulse width jitter and deterministic pulse width jitter</td><td>High Swing Toggle Pattern, transitions between levels 0 and 3</td><td>Must use no Tx equalization</td></tr></tbody></table><dl class="st-terms" aria-label="Terms in this passage"><div><dt>PAM4</dt><dd>Pulse Amplitude Modulation with 4 levels</dd></div></dl></div><p>Tx jitter measurements at 32.0 and 64.0 GT/s require at least 50 GHz oscilloscope bandwidth. At 64.0 GT/s the specified fourth-order Bessel-Thomson filter, down 3 dB at 33 GHz, is recommended. Preserve the difference between a requirement and a recommendation.</p><p>Section 8.3.5 requires other PCIe Lanes to transmit Compliance Pattern while measuring one Tx Lane, to capture die/package crosstalk. The DUT must also drive as many outputs as normal system operation would use. Follow these task-specific conditions rather than treating §8.3.1's general environment introduction as the complete procedure.</p><p>Finally check the reference plane for the actual item. Table 8-6 explicitly says that <code>VTX-AC-CM-PP</code> and <code>VTX-AC-CM-PP-filtered</code> noise analysis is done without de-embedding. These common-mode voltage parameters are not jitter, and are an exception to the general voltage-processing rule. A report saying “everything referred to pins” still needs a row-by-row applicability check.</p><p class="source-note">Base 6.0 §8.3.5 <em>Tx Jitter Parameters</em> (p.1336), §§8.3.5.1–8.3.5.2 (pp.1336–1338); Table 8-6 common-mode rows and notes (p.1350). This is a reading guide, not the full compliance procedure.</p></section>

<section id="sources"><h2>Edition and sources</h2><p>PCI Express Base Specification Revision 6.0 (6.0-1.0-PUB) is the authority. Printed and PDF-viewer page numbers match at these locations. Idealized levels and measurement assumptions are marked beside the case; they are not device measurements or certification.</p><details class="source-note"><summary>Reading locations and purpose</summary><ul><li>§8.3.1, Figures 8-1 / 8-2 (pp.1318–1319); §8.3.1.1 (pp.1319–1320): test points, Breakout/Replica Channels, and reference plane.</li><li>§8.3.2 <em>Voltage Level Definitions</em>, Equations 8-1 / 8-2 (p.1320); Figure 8-3 (p.1321): single-ended, differential, and common mode.</li><li>§8.3.3 <em>Tx Voltage Parameters</em> and §§8.3.3.1–8.3.3.7 (pp.1321–1326); Tables 8-1 / 8-2, Figure 8-7: rate-specific swing, equalization, and preset methods.</li><li>§8.3.5 <em>Tx Jitter Parameters</em> and §§8.3.5.1–8.3.5.5 (pp.1336–1338), Table 8-5 (p.1338): patterns, environment, clock sampling, and processing. Full PLL/transport-delay definitions follow the table into the relevant Refclk section and §8.6.6; their algorithms are not expanded here.</li><li>§8.3.6 <em>Data Rate Dependent Parameters</em>, Table 8-6 (p.1347 onward): this case uses differential swing on p.1348 and Note 3 on p.1351; AC common-mode rows on p.1350 illustrate the no-de-embedding exception.</li></ul></details></section>
</article>
<nav class="bottom-nav" aria-label="Course and editions"><a href="/DOCS/pcie-course/index.html">Course overview</a><a href="/DOCS/pcie-course/chapter-20.html">Full Chinese tutorial</a><a href="/pcie/chapter-20-zh-tw/">繁體中文</a></nav>
</div>
