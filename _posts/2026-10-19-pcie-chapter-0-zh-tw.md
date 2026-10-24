---
layout: post
title: "PCIe Chapter 0：從系統全貌到第一次規格查詢"
date: 2026-10-19 00:00:00 +0800
last_modified_at: 2026-10-23 00:00:00 +0800
permalink: /pcie/chapter-0-zh-tw/
categories: [PCIe]
tags: [PCIe, Specification]
lang: zh-TW
spec_teaching: true
spec_series: pcie
description: "一個 PCIe 裝置如何被系統認識並使用？又該如何查出它支援什麼？"
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
<div class="pcie-article spec-teaching" data-spec-series="pcie" lang="zh-Hant-TW">
<nav class="bottom-nav" aria-label="課程與語言版本"><a href="/DOCS/pcie-course/index.html">課程總覽</a><a href="/DOCS/pcie-course/chapter-0.html">繁中完整教學</a><a href="/pcie/chapter-0-en/">English</a></nav>
<article class="lesson">
<p class="lead">PCI Express（PCIe）讓主機與周邊裝置交換要求與資料。本章先定位系統角色，再沿設定空間的能力清單完成連線查詢，分別取得支援速率與目前結果。</p>
<figure class="diagram"><svg viewBox="0 0 840 565" class="course-diagram" role="img" aria-labelledby="ch0-system-svg-title ch0-system-svg-desc"><title id="ch0-system-svg-title">從 CPU／記憶體定位 PCIe 角色</title><desc id="ch0-system-svg-desc">CPU與記憶體經Root Complex、Root Port及Switch連到Endpoint；連線不代表所有初始化均已完成。</desc><g><rect x="30" y="25" width="245" height="80" rx="10" fill="var(--blue-soft)" stroke="var(--line)" stroke-width="2"/><text x="152.5" y="52" text-anchor="middle" fill="var(--ink)" font-size="18">CPU／記憶體</text><text x="152.5" y="77" text-anchor="middle" fill="var(--ink)" font-size="16">準備與使用工作資料</text></g><g><rect x="335" y="25" width="280" height="80" rx="10" fill="var(--blue-soft)" stroke="var(--line)" stroke-width="2"/><text x="475" y="52" text-anchor="middle" fill="var(--ink)" font-size="18">Root Complex</text><text x="475" y="77" text-anchor="middle" fill="var(--ink)" font-size="16">連接主機與 I/O 階層</text></g><g><rect x="335" y="155" width="280" height="80" rx="10" fill="var(--blue-soft)" stroke="var(--line)" stroke-width="2"/><text x="475" y="182" text-anchor="middle" fill="var(--ink)" font-size="18">Root Port</text><text x="475" y="207" text-anchor="middle" fill="var(--ink)" font-size="16">對外連線的介面</text></g><g><rect x="335" y="305" width="280" height="80" rx="10" fill="var(--blue-soft)" stroke="var(--line)" stroke-width="2"/><text x="475" y="332" text-anchor="middle" fill="var(--ink)" font-size="18">Switch</text><text x="475" y="357" text-anchor="middle" fill="var(--ink)" font-size="16">延伸下游連接路徑</text></g><g><rect x="335" y="455" width="280" height="80" rx="10" fill="var(--blue-soft)" stroke="var(--line)" stroke-width="2"/><text x="475" y="482" text-anchor="middle" fill="var(--ink)" font-size="18">Endpoint</text><text x="475" y="507" text-anchor="middle" fill="var(--ink)" font-size="16">提供裝置功能</text></g><g><path d="M275 65 H335" fill="none" stroke="var(--accent)" stroke-width="2.5"/></g><g><path d="M475 105 V155" fill="none" stroke="var(--accent)" stroke-width="2.5"/></g><g><path d="M475 235 V305" fill="none" stroke="var(--accent)" stroke-width="2.5"/><text x="525" y="278" text-anchor="middle" fill="var(--ink)" font-size="15">Link</text></g><g><path d="M475 385 V455" fill="none" stroke="var(--accent)" stroke-width="2.5"/><text x="525" y="428" text-anchor="middle" fill="var(--ink)" font-size="15">Link</text></g></svg><figcaption>作者的系統關係圖。Root Complex 連接主機與 I/O；Root Port 對外建立 Link，Switch 延伸路徑，Endpoint 提供裝置功能。Base 6.0 Figure 1-2，文件頁／PDF 頁 103。</figcaption></figure>

<p><a href="/DOCS/pcie-course/chapter-0.html">完整中文教學與逐步圖解</a> · <a href="/DOCS/pcie-course/index.html">課程路線</a> · <a href="/pcie/chapter-0-en/">English</a></p>
<aside class="note"><strong>版本範圍</strong><p>欄位依 PCI Express Base Specification Revision 6.0，韌體背景依 PCI Firmware Specification Revision 3.3。後者 §1.2（p.7）參考的是 Base 5.0，因此不能把兩份文件視為同版配套。下列頁碼均對應本課程採用的 PDF，文件頁與 PDF 頁序相同。</p></aside>

<section id="system">
<h2>裝置接上後，還要完成哪些工作？</h2>
<p>Root Complex 把 CPU／記憶體子系統接到 I/O 階層；Root Port 對外建立 Link（相鄰兩端的連線），Switch 可以延伸連接路徑，Endpoint 提供裝置功能。Link（相鄰兩端的連線） 連接相鄰兩端，Lane 是構成 Link 的通道；x4 表示 4 個 Lane，不是 4 個裝置。</p>
<p>軟體辨識與設定的基本對象是 Function（可個別辨識與設定的功能）。一張卡可以有多個 Function（可個別辨識與設定的功能）；本例用 <code>0000:03:00.0</code> 表示 Segment（匯流排的邏輯分組）、Bus、Device、Function，其中 Bus、Device、Function 常合稱 BDF（Bus、Device、Function 識別號）。Segment 是邏輯分組，不是額外的硬體元件；這組識別號也不是記憶體位址。</p><dl class="st-terms" aria-label="本段名詞"><div><dt>BDF</dt><dd>Bus／Device／Function，匯流排、裝置與功能識別</dd></div></dl>
<p>兩端硬體先具備建立 Link 的條件，系統軟體再發現 Function、配置資源，驅動程式則準備裝置的工作介面。這是理解依賴關係的教學整理，實際平台可能分階段處理。Firmware 3.3 §3.5 要求韌體設定開機與主控台裝置的完整路徑，以及所有 Host Bridge，卻不保證每個 Endpoint 都已配置完成。</p>
<div class="table-wrap"><table><caption>同一項工作可能用到的三種存取</caption><thead><tr><th scope="col">目的</th><th scope="col">應找的資料</th></tr></thead><tbody>
<tr><td>辨識 Function、查 PCIe 能力</td><td>Configuration Space（設定空間）中的標頭與 Capability。</td></tr>
<tr><td>由 CPU 操作裝置介面</td><td>BAR 所描述的資源及裝置暫存器；若經記憶體映射存取，稱為 MMIO（Memory-Mapped I/O，記憶體映射 I/O）。</td></tr>
<tr><td>由裝置搬移工作資料</td><td>DMA（Direct Memory Access，直接記憶體存取）所用的緩衝區、裝置可用位址及存取條件。CPU 仍需先準備工作。</td></tr>
</tbody></table><dl class="st-terms" aria-label="本段名詞"><div><dt>BAR</dt><dd>Base Address Register，基底位址暫存器</dd></div></dl></div>
<p>BAR 是設定空間中的 Base Address Register，不是資料緩衝區。能讀取設定空間，尚不足以證明 MMIO 或 DMA 已準備好。</p><dl class="st-terms" aria-label="本段名詞"><div><dt>MMIO</dt><dd>Memory-Mapped I/O，記憶體映射輸入輸出</dd></div><div><dt>DMA</dt><dd>Direct Memory Access，裝置直接存取記憶體</dd></div></dl>
<details class="source-note"><summary>系統觀的規格位置</summary><p>Base 6.0 §1.2–§1.4，pp.100–109（Figure 1-2：p.103）；§2.1.1，pp.116–117；BAR：§7.5.1.2.1，pp.928–930。Firmware 3.3 §1.3，pp.8–9；§3.1–§3.2，pp.32–33；交接要求：§3.5，pp.34–35。</p></details>
</section>

<section id="query">
<h2>要查支援速率，為什麼不能只讀目前速率？</h2>
<p>先按查詢目的選欄位：能力描述支援範圍，控制描述相關設定，狀態描述目前結果。本次找到能力結構後，先讀本端支援集合，再查看連線目前的速率與寬度；控制上限留待後續連線章處理。</p>
<p>每個 Function 的 PCIe 設定空間為 4096 bytes。PCI Express Capability（描述或控制能力的結構） 位於前 256 bytes 的傳統 Capability（描述或控制能力的結構） 清單，不能因名稱含有 PCI Express，就跳去找 Extended Capability。（Base 6.0 §7.2／Figure 7-3，pp.905–906；§7.5.3，p.951。）</p>
<aside class="example"><strong>教學假設</strong><p>以下拓樸、位置與讀值由作者設計，不是實機量測。目標為已找到的一般 PCI Express Endpoint，並非整合於 Root Complex 的端點（Root Complex Integrated Endpoint，RCiEP），也不是虛擬化的 Virtual Function（VF）。本例使用傳統 BDF（Bus、Device、Function 識別號） 編址，不使用 Alternative Routing-ID Interpretation（ARI，另一種解讀 Function 識別號的方式）；設定讀取均成功。Link 已建立，查詢期間維持穩定，且已實作本題使用的 Link Capabilities 2 速率向量。所有 offset 都是該 Function 設定空間內的 byte 位移，不是 CPU 實體位址。</p><dl class="st-terms" aria-label="本段名詞"><div><dt>BDF</dt><dd>Bus／Device／Function，匯流排、裝置與功能識別</dd></div></dl></aside>
<div class="table-wrap"><table><caption>先沿清單找結構，再確認版本與類型</caption><thead><tr><th scope="col">步驟</th><th scope="col">假設讀值與判讀</th><th scope="col">Base 6.0 閱讀位置</th></tr></thead><tbody>
<tr><td>辨識標頭</td><td><code>0x0E</code> 讀 8 bits 得 <code>0x00</code>；<code>0x00 &amp; 0x7F = 0</code>，採 Type 0。<code>0x06</code> 讀 16 bits 得 <code>0x0010</code>，Status bit 4 為 1。</td><td>Figure 7-8／Table 7-7，pp.924–925；Figure 7-10，p.928；Figure 7-6／Table 7-5，pp.921–922。</td></tr>
<tr><td>找到清單入口</td><td><code>0x34</code> 讀 8 bits 得 <code>0x40</code>。先遮掉低 2 bits：<code>0x40 &amp; 0xFC = 0x40</code>。</td><td>§7.5.1.1.11，p.926。</td></tr>
<tr><td>經過 PM Capability</td><td><code>0x40</code> 讀 16 bits 得 <code>0x7001</code>；低 byte 的 ID 為 <code>0x01</code>，高 byte 的 Next Pointer 為 <code>0x70</code>。</td><td>Figure 7-18／Table 7-14，p.945。</td></tr>
<tr><td>找到 PCIe Capability</td><td><code>0x70</code> 讀 16 bits 得 <code>0x0010</code>；ID 為 <code>0x10</code>，Next Pointer 為 0。記下 <code>cap_base = 0x70</code>。</td><td>Figure 7-22／Table 7-18，p.953。</td></tr>
<tr><td>確認版本與類型</td><td><code>0x72</code> 讀 16 bits 得 <code>0x0002</code>；低 4 bits 為 Version 2，bits 7:4 為 0，表示 PCI Express Endpoint。</td><td>Figure 7-23／Table 7-19，pp.953–954。</td></tr>
</tbody></table></div>
<p>設定空間採小端序，所以 <code>0x7001</code> 的低位址 byte 是 <code>0x01</code>（Base 6.0 §7.5.1.1，p.916）。清單位置與順序可以改變；<code>0x70</code> 不能寫成通用常數。</p>
<p>若清單已結束卻沒找到目標，或讀取失敗，就不能繼續把某個位置當成該結構。讀不到資料也不等於已取得「不支援」的有效回覆。</p>
<p>Capability Version 2 不等於 PCIe Gen2，也不能單獨保證舊硬體實作了速率向量。本例已另列實作前提；採用 Base 6.0 解讀欄位，也不表示裝置必然支援 64 GT/s。舊硬體分支見 §7.5.3.18 的實作說明（p.1000）。</p>
</section>

<section id="decode">
<h2>找到結構後，怎麼把讀值轉成答案？</h2>
<figure class="diagram"><svg viewBox="0 0 840 355" class="course-diagram" role="img" aria-labelledby="ch0-query-svg-title ch0-query-svg-desc"><title id="ch0-query-svg-title">先找到結構，再分別讀能力與狀態</title><desc id="ch0-query-svg-desc">從傳統清單找到0x70，再分別加上能力與狀態欄位的相對位移。</desc><g><rect x="20" y="35" width="230" height="80" rx="10" fill="var(--blue-soft)" stroke="var(--line)" stroke-width="2"/><text x="135" y="62" text-anchor="middle" fill="var(--ink)" font-size="18">設定標頭</text><text x="135" y="87" text-anchor="middle" fill="var(--ink)" font-size="16">0x34 → 0x40</text></g><g><rect x="305" y="35" width="230" height="80" rx="10" fill="var(--blue-soft)" stroke="var(--line)" stroke-width="2"/><text x="420" y="62" text-anchor="middle" fill="var(--ink)" font-size="18">電源管理結構</text><text x="420" y="87" text-anchor="middle" fill="var(--ink)" font-size="16">ID=0x01；Next=0x70</text></g><g><rect x="590" y="35" width="230" height="80" rx="10" fill="var(--blue-soft)" stroke="var(--line)" stroke-width="2"/><text x="705" y="62" text-anchor="middle" fill="var(--ink)" font-size="18">PCIe 能力結構</text><text x="705" y="87" text-anchor="middle" fill="var(--ink)" font-size="16">ID=0x10；起點=0x70</text></g><g><rect x="120" y="240" width="270" height="80" rx="10" fill="var(--blue-soft)" stroke="var(--line)" stroke-width="2"/><text x="255" y="267" text-anchor="middle" fill="var(--ink)" font-size="18">支援速率</text><text x="255" y="292" text-anchor="middle" fill="var(--ink)" font-size="16">起點+0x2C → 0x9C</text></g><g><rect x="450" y="240" width="270" height="80" rx="10" fill="var(--blue-soft)" stroke="var(--line)" stroke-width="2"/><text x="585" y="267" text-anchor="middle" fill="var(--ink)" font-size="18">目前連線狀態</text><text x="585" y="292" text-anchor="middle" fill="var(--ink)" font-size="16">起點+0x12 → 0x82</text></g><g><path d="M250 75 H305" fill="none" stroke="var(--accent)" stroke-width="2.5"/><path d="M296 70 L305 75 L296 80" fill="none" stroke="var(--accent)" stroke-width="2.5"/></g><g><path d="M535 75 H590" fill="none" stroke="var(--accent)" stroke-width="2.5"/><path d="M581 70 L590 75 L581 80" fill="none" stroke="var(--accent)" stroke-width="2.5"/></g><g><path d="M705 115 V175 H255 V240 M585 175 V240" fill="none" stroke="var(--accent)" stroke-width="2.5"/><text x="440" y="160" text-anchor="middle" fill="var(--ink)" font-size="15">先核對版本與適用類型</text></g></svg><figcaption>先找到結構，再加上欄位相對位移。這是閱讀路線，不是硬體狀態機。Base 6.0 Figure 7-21，文件頁／PDF 頁 952。</figcaption></figure>
<p>先看 Figure 7-21（p.952），將欄位相對位移加到起點；接著先查能力的 Figure 7-38／Table 7-35（pp.998–1000），再回到狀態的 Figure 7-29／Table 7-26（pp.978–979）。順序由問題決定，圖用來定位，表格與條文用來判讀。每一步都要確認版本與適用對象，不能只從欄位名稱推測它的意義。</p>
<pre><code>Link Capabilities 2：0x70 + 0x2C = 0x9C，讀 32 bits → 0x0180001E
Link Status        ：0x70 + 0x12 = 0x82，讀 16 bits → 0x0043</code></pre>
<p>Supported Link Speeds Vector 在整個 Register 的 bits 7:1。先用遮罩保留，再右移成欄位值：</p>
<pre><code>(0x0180001E &amp; 0x000000FE) &gt;&gt; 1 = 0x0F</code></pre>
<p>欄位內 bits 0–3 都為 1，分別表示支援 <strong>2.5、5、8、16 GT/s</strong>；bits 4–5 為 0，未宣告 32、64 GT/s；bit 6 為保留位元。欄位 bit 0 原本位於 Register bit 1，兩種編號不要混用。完整讀值保留 bits 23、24，是 Table 7-35 對支援 16 GT/s 以上裝置的偵測能力要求；它們不證明路徑中已有 Retimer。</p>
<p>Link Status 則使用編碼，不是另一個支援 bitmap：</p>
<pre><code>Current Link Speed：0x0043 &amp; 0x000F = 3
Negotiated Link Width：(0x0043 &amp; 0x03F0) &gt;&gt; 4 = 4</code></pre>
<p>代碼 3 對應速率向量的欄位 bit 2，也就是 <strong>8 GT/s</strong>；寬度 4 表示 <strong>x4</strong>。這些遮罩以表中讀取寬度為前提，不能直接套到不同位置的 32-bit 讀值。</p>
<p>Table 7-26 指出，Link 未建立時，這兩個欄位為 undefined。<code>0x0043</code> 本身不能證明 Link 已建立；也不能僅憑 bit 13 為 0 就認定 Link 中斷，因為該狀態位是否實作取決於回報能力（Table 7-23、Table 7-26，pp.969、979）。</p>
</section>

<section id="limits">
<h2>目前只有 8 GT/s，可以認定裝置有問題嗎？</h2>
<p>Figure 7-21（p.952）先提供相對位置。找到能力欄位後，讀 Figure 7-38／Table 7-35（pp.998–1000）解釋速率向量；再用 Figure 7-29／Table 7-26（pp.978–979）讀目前速率與寬度。每一步都連同表格的編碼、版本及適用條件判讀。</p>
</section>

<section id="self-check">
<h2>換一個條件，原來的判斷還成立嗎？</h2>
<p>完整查詢先選 Function、沿清單找結構，再核對版本與類型，分別解碼能力及狀態。下面沿用這條路徑，只更動一項條件，說明需要重新確認的位置。</p>
<details class="question"><summary>Capability 起點改為 0x90，還能到 0x9C 查能力嗎？</summary><p>不能。依 Figure 7-21（p.952），Link Capabilities 2 應為 <code>0x90 + 0x2C = 0xBC</code>，Link Status 為 <code>0x90 + 0x12 = 0xA2</code>。起點是新教學假設，相對位移不變。</p></details>
<details class="question"><summary>Current Link Speed 為 4，是同時支援兩種速率嗎？</summary><p>不是。有效的 Link 狀態下，編碼 4 表示目前為 16 GT/s。支援集合仍須另外查向量。（Table 7-26、Table 7-35，pp.978、998。）</p></details>
<details class="question"><summary>Link 已中斷，手上仍有 0x0043 這筆讀值，能報成目前 8 GT/s、x4 嗎？</summary><p>不能。Table 7-26（p.978）將 Link 未建立時的速率與寬度定為 undefined；看似合理的數字不能取代有效條件。</p></details>
</section>
<p>下一步先釐清拓樸、Function 與識別範圍，再深入設定空間。逐步欄位圖、完整案例與來源整理，見<a href="/DOCS/pcie-course/chapter-0.html">Chapter 0 中文教學</a>；<a href="/DOCS/pcie-course/chapter-1.html">Chapter 1 已可閱讀</a>，Chapter 2–13 已完成，Chapter 14–19 仍在規劃中。</p>
</article>
<nav class="bottom-nav" aria-label="課程與語言版本"><a href="/DOCS/pcie-course/index.html">課程總覽</a><a href="/DOCS/pcie-course/chapter-0.html">繁中完整教學</a><a href="/pcie/chapter-0-en/">English</a></nav>
</div>
