---
layout: post
title: "PCIe Chapter 27：ATS、PRI 與 PASID 的位址轉譯流程"
date: 2026-10-24 00:00:00 +0800
last_modified_at: 2026-10-29 00:00:00 +0800
permalink: /pcie/chapter-27-zh-tw/
categories: [PCIe]
tags: [PCIe, Specification]
lang: zh-TW
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
<div class="pcie-article spec-teaching" data-spec-series="pcie" lang="zh-Hant-TW">
<nav class="bottom-nav" aria-label="課程與語言版本"><a href="/DOCS/pcie-course/index.html">課程總覽</a><a href="/DOCS/pcie-course/chapter-27.html">繁中完整教學</a><a href="/pcie/chapter-27-en/">English</a></nav>
<article class="lesson">
<p>ATS 查映射與權限，PRI 請平台準備頁面，PASID 補充位址空間身分。本章用同一組案例，將轉譯查詢、實際讀取、映射失效與頁面群組分開追蹤，再接回各自的設定與規格圖表。</p><dl class="st-terms" aria-label="本段名詞"><div><dt>ATS</dt><dd>Address Translation Services，位址轉譯服務</dd></div><div><dt>PRI</dt><dd>Page Request Interface，頁面要求介面</dd></div><div><dt>PASID</dt><dd>Process Address Space ID，程序位址空間識別碼</dd></div></dl><figure class="diagram"><svg viewBox="0 0 900 350" style="min-width:680px" role="img" aria-labelledby="ch27-zh-t ch27-zh-d"><title id="ch27-zh-t">轉譯查詢、實際存取與缺頁時的獨立支線</title><desc id="ch27-zh-d">ATS 先取得轉譯，再進行已轉譯 Memory 存取。缺頁時才使用 PRI 並回到 ATS；映射改變另走失效交換。</desc><g data-walk-target="dev"><rect x="20" y="15" width="270" height="55" rx="9" fill="var(--surface-alt)" stroke="var(--line)"/><text x="155" y="49" text-anchor="middle" font-size="17">Endpoint / ATC</text></g><g data-walk-target="ta"><rect x="610" y="15" width="270" height="55" rx="9" fill="var(--surface-alt)" stroke="var(--line)"/><text x="745" y="49" text-anchor="middle" font-size="17">Platform / TA + Memory</text></g><g data-walk-target="query"><text x="450" y="100" text-anchor="middle" font-size="16">ATS：查轉譯</text><path d="M290 115 H610" stroke="var(--accent)" stroke-width="2"/><polygon points="610,115 600,110 600,120" fill="var(--accent)"/></g><g data-walk-target="reply"><text x="450" y="160" text-anchor="middle" font-size="16">Translation Completion：映射與權限</text><path d="M610 175 H290" stroke="var(--accent)" stroke-width="2"/><polygon points="290,175 300,170 300,180" fill="var(--accent)"/></g><g data-walk-target="memory"><text x="450" y="220" text-anchor="middle" font-size="16">Memory Request：用轉譯位址存取</text><path d="M290 235 H610" stroke="var(--accent)" stroke-width="2"/><polygon points="610,235 600,230 600,240" fill="var(--accent)"/></g><g data-walk-target="pri"><rect x="45" y="285" width="810" height="45" rx="8" fill="var(--surface-alt)" stroke="var(--line)"/><text x="450" y="314" text-anchor="middle" font-size="16">缺頁時另走 PRI → 群組回覆 → 再查 ATS</text></g></svg><figcaption>作者繪製的流程定位。ATC（Address Translation Cache，位址轉譯快取）保存結果；TA（Translation Agent，轉譯代理）處理平台轉譯與保護資訊。PRI 是需要時才使用的支線。</figcaption></figure><dl class="st-terms" aria-label="本段名詞"><div><dt>ATS</dt><dd>Address Translation Services，位址轉譯服務</dd></div><div><dt>PRI</dt><dd>Page Request Interface，頁面要求介面</dd></div></dl><section id="lookup"><h2>想追一筆 DMA，先把哪些角色放到圖上？</h2><dl class="st-terms" aria-label="本段名詞"><div><dt>DMA</dt><dd>Direct Memory Access，裝置直接存取記憶體</dd></div></dl><p>先開 Figure 10-1 <em>Example Illustrating a Platform with TA, ATPT, and ATC Elements</em>。裝置的 ATC 保存轉譯結果；平台的 TA 依 ATPT（Address Translation and Protection Table，位址轉譯與保護資料表）判斷映射與權限。TA 與資料表可以分開或整合，具體實作由平台決定。再用 Figure 10-2 追 Request 與 Translation Completion，才開始看實際 DMA（Direct Memory Access，裝置直接記憶體存取）。</p><p><strong>【模擬資料】以下資料為教學用途建立，不代表特定硬體或平台。</strong>本章使用單一 Endpoint Function，Requester ID=0300h，PASID=00021h，處於 D0、Bus Master Enable=1。平台已允許這個身分使用相應服務，路徑可傳遞本例封包；TC0／TC1 的必要傳輸已就緒。正常算例採 Non-Flit Mode，沒有 Reset、Replay 或 PASID 停用／重用事件。</p><dl class="st-terms" aria-label="本段名詞"><div><dt>PASID</dt><dd>Process Address Space ID，程序位址空間識別碼</dd></div></dl><p>本章直接依 Base 6.0 Chapter 10 與 §6.20；平台頁表格式、特定 IOMMU（Input/Output Memory Management Unit，I/O 記憶體管理單元）暫存器及作業系統介面另須查實際文件。Switch 可透明轉送 ATS 封包，不必因此成為 TA，或各自具有 ATS Requester Capability。</p><p class="source-note">Base 6.0 §10.1.1，Figures 10-1／10-2，pp.1470–1474；本章的身分、設定、映射及 Trace 均為作者建立。</p></section>
<section id="pasid"><h2>同樣 PASID=21h，就一定是同一個程序嗎？</h2><p>先依 §6.20 把 PASID 與 Requester ID 配對。各 Function 有自己的 PASID 集合；另一個 RID=0310h 使用 21h，並不由此得到與 0300h 相同的位址空間。PASID 也不是作業系統 PID 的通用編碼，Function 如何將它連到工作上下文，由裝置與平台處理。</p><dl class="st-terms" aria-label="本段名詞"><div><dt>RID</dt><dd>Routing ID，封包使用的路由識別碼</dd></div></dl><p>Non-Flit Mode 的 PASID 位於 End-End TLP Prefix，依 Figure 6-20／Table 6-15 解碼。本例 Execute Requested=0、Privileged Mode Requested=0，PASID=00021h，四個位元組為 <code data-pasid-prefix="example">91 00 00 21</code>。Flit Mode 改放在 OHC-A1（承載 PASID 等資訊的標頭區塊）；Translation Request 的 No Write 也須改讀這個區塊，不能把 Non-Flit 的欄位位置直接套過去。</p><dl class="st-terms" aria-label="本段名詞"><div><dt>TLP</dt><dd>Transaction Layer Packet，交易層封包</dd></div></dl><p>Max PASID Width=8 允許 0–255，21h 在範圍內；PASID=0 也是可用值，不能自行當成保留編碼。一般 Completion 不允許帶 PASID，Translation Completion 也一樣；收到它時，裝置須依 Requester ID／Tag 找回原 Translation Request 保存的 PASID 上下文。後文的 PRG（Page Request Group，頁面要求群組）Response 則是規格另外允許帶 PASID 的 Message。</p><p class="source-note">Base 6.0 §§6.20–6.20.2.2，Figure 6-20 <em>PASID TLP Prefix</em>、Table 6-15，pp.791–793；§10.1.3 <em>Process Address Space ID (PASID)</em>，pp.1477–1478。</p></section>
<section id="configure"><h2>能力、啟用與目前需求，該分別查哪張圖？</h2><p>先找三個不同結構：PASID ID=001Bh、ATS ID=000Fh、Page Request ID=0013h，本版的 Version 均為 1。起點分別記為 P、A、R。Figures 7-185、10-29、10-33 定位結構，再用各自的 Register Table 解碼：</p><div class="table-wrap"><table><thead><tr><th scope="col">Structure / field</th><th scope="col">Offset</th><th scope="col">模擬值</th><th scope="col">解讀</th></tr></thead><tbody><tr data-ats-config="pasid-cap"><td>PASID Capability</td><td>P+04h</td><td>0808h</td><td>Max PASID Width=8; Translated Requests with PASID Supported=1</td></tr><tr data-ats-config="pasid-control"><td>PASID Control</td><td>P+06h</td><td>0009h</td><td>PASID Enable=1; Translated Requests with PASID Enable=1</td></tr><tr data-ats-config="ats-cap"><td>ATS Capability</td><td>A+04h</td><td>0024h</td><td>Invalidate Queue Depth=4; Page Aligned Request=1</td></tr><tr data-ats-config="ats-control"><td>ATS Control</td><td>A+06h</td><td>8000h</td><td>Enable=1; STU=0 → 4 KiB; AMAE=0</td></tr><tr data-ats-config="pri-status"><td>Page Request Status, before enable</td><td>R+06h</td><td>8100h</td><td>Stopped=1; PRG Response PASID Required=1</td></tr><tr data-ats-config="pri-capacity"><td>Outstanding Page Request Capacity</td><td>R+08h</td><td>00000004h</td><td>4 requests</td></tr><tr data-ats-config="pri-allocation"><td>Outstanding Page Request Allocation</td><td>R+0Ch</td><td>00000003h</td><td>3 requests</td></tr><tr data-ats-config="pri-control"><td>Page Request Control, after enable</td><td>R+04h</td><td>0001h</td><td>Enable=1</td></tr></tbody></table></div><p>PASID Capability 的 0808h 表示 8-bit 寬度、支援 Translated Requests with PASID；本例不要求 Execute／Privileged Mode。Control=0009h 同時啟用 PASID 與帶 PASID 的 Translated Requests。必須在 ATS Enable=0 時先設好 PASID Control，再將 ATS Control 設為 8000h；ATS Enable 已為一時改任何 PASID Control bit，行為為 undefined。</p><p>ATS 的 STU（Smallest Translation Unit，最小轉譯單位）=0，表示 2<sup>0</sup>×4 KiB＝4 KiB；它不是關閉轉譯。Invalidate Queue Depth=4 是失效要求的資源資訊，不是 Page Request 額度。ATS Memory Attributes 在本例未啟用，不自行解讀其平台特定值。</p><p>在 Page Request Enable=0 時，將 Allocation 設為 3，低於 Capacity=4；確認 Stopped=1 後才啟用。在啟用中更改 Allocation，行為為 undefined（規格未定義）；尚未成功停止就重新啟用，結果則為 indeterminate（無法確定）。<strong>Stopped 只在 Enable=0 時有意義</strong>；啟用後不能靠它的零或一判斷「目前沒有 Page Request」。</p><p>ATS 不必搭配 PRI；PASID 也不是只有 ATS／PRI 才能使用。Root Complex 的 PASID 支援與啟用機制由平台定義，不能在 Root Port 內尋找與 Endpoint 相同的 PASID Control。</p><p class="source-note">Base 6.0 §7.8.9，Figures 7-185–7-188、Tables 7-159–7-161，pp.1148–1151；§10.5.1，Figures 10-29–10-32、Tables 10-9–10-11，pp.1513–1516；§10.5.2，Figures 10-33–10-36、Tables 10-13–10-15，pp.1516–1520。</p></section>
<section id="translation-case"><h2>要讀 40001234h 的四個位元組，先查什麼？</h2><p>先依 Table 10-1 分辨 AT（Address Type，位址類型）：00b 是 Untranslated，01b 是 Translation Request，10b 是 Translated。00b 的位址由 TA 決定如何處理，不代表所有平台都把它直接當成 CPU 虛擬位址；10b 也不代表平台跳過權限檢查。</p><p>案例要讀未轉譯位址 40001234h。因 Page Aligned Request=1，先對齊到 40001000h，再按 Figures 10-10／10-11 形成 AT=01b 的 MRd（Memory Read，讀取要求）。TA 再以 CplD（Completion with Data，帶資料的完成封包）回覆轉譯結果。Length=2 DW 表示最多回一筆 8-byte 轉譯項目，並非向應用程式讀八個位元組。NW（No Write，不要求寫入）=1，本例只需要讀取。</p><dl class="st-terms" aria-label="本段名詞"><div><dt>DW</dt><dd>Double Word，4 bytes的資料單位</dd></div></dl><div class="table-wrap"><table><caption>MRd 是讀取要求；CplD 是帶資料的完成封包。以下依序追蹤查轉譯與讀資料。</caption><thead><tr><th scope="col">TLP</th><th scope="col">AT</th><th scope="col">Requester ID</th><th scope="col">Tag</th><th scope="col">Length</th><th scope="col">Address / data</th></tr></thead><tbody><tr data-ats-step="query"><td>MRd / Translation Request</td><td>01b</td><td>0300h</td><td>2Ah</td><td>2 DW</td><td>40001000h; NW=1</td></tr><tr data-ats-step="translation"><td>CplD / Translation Completion</td><td>—</td><td>0300h</td><td>2Ah</td><td>2 DW</td><td>Base=90000000h; S=0; R=1; W=0; U=0</td></tr><tr data-ats-step="read"><td>MRd / Memory Read</td><td>10b</td><td>0300h</td><td>2Bh</td><td>1 DW</td><td>90000234h</td></tr><tr data-ats-step="data"><td>CplD / Memory Read data</td><td>—</td><td>0300h</td><td>2Bh</td><td>1 DW</td><td>4 bytes application data</td></tr></tbody></table><dl class="st-terms" aria-label="本段名詞"><div><dt>TLP</dt><dd>Transaction Layer Packet，交易層封包</dd></div><div><dt>DW</dt><dd>Double Word，4 bytes的資料單位</dd></div></dl></div><p>Translation Completion 依 Figure 10-14 <em>Translation Completion Data Entry</em> 與 Table 10-3 解碼：本例 S=0 表示 4 KiB，R=1、W=0、U=0 允許以這個轉譯位址做非零長度讀取；Global、Priv、Exe、N、AMA 均假設為零。未轉譯頁內 offset=234h，故實際位址為 90000000h＋234h＝90000234h。對應範圍是 90000000h–90000FFFh，四個位元組 沒有跨頁。</p><p>後面 Tag=2Bh 的 Memory Read 是另一筆 Transaction。本例 Trace 最後觀察到 SC（Successful Completion，成功完成狀態）與四個位元組的應用資料，才確認這筆讀取的結果。前一筆 Tag=2Ah 的 SC 只配對轉譯查詢。Translation Request 也不能拿來當成其他 Write 已完成的排序屏障。</p><p class="source-note">Base 6.0 §§10.2.1–10.2.2，Table 10-1、Figures 10-6–10-13，pp.1478–1483；§10.2.3，Figure 10-14／Table 10-3，pp.1484–1489；§10.2.4，p.1496。兩種模式的基本 Header 另見 <a href="/DOCS/pcie-course/chapter-14.html">Chapter 14</a>。</p></section>
<section id="permissions"><h2>收到 SC，為何仍可能不能發 Translated Read？</h2><div class="table-wrap"><table><thead><tr><th scope="col">Translation Completion</th><th scope="col">R / W / U</th><th scope="col">後續處理</th></tr></thead><tbody><tr><td>SC / CplD</td><td>1 / 0 / 0</td><td>可依有效範圍與其他條件使用轉譯位址做 Read，不得用來寫入</td></tr><tr><td>SC / CplD</td><td>0 / 0 / undefined</td><td>沒有可用映射權限；不得快取此項目或使用 Translated Address</td></tr><tr><td>SC / CplD</td><td>1 / 0 / 1</td><td>只允許適用的未轉譯讀取；不得使用回覆中的 Translated Address</td></tr></tbody></table></div><p>R=W=0 時，S 與範圍資訊仍用來描述該區段；地址及其他指定欄位則為 undefined。平台日後可能把無效映射變成有效，卻不必因此送失效通知，所以 ATC 不得保存這筆「沒有權限」的結果當成持久的負向快取。</p><p>U（Untranslated access only，只允許未轉譯存取）=1 時，可快取規格允許的權限／範圍資訊，但不得把回覆地址放進 AT=10b 的 Request。若 R=1、W=0，之後需要寫入，也應另取新轉譯與相應授權，不能自行改 ATC 的 W bit。</p><p>另外，Table 10-2 的 UR（Unsupported Request，不支援要求）與 CA（Completer Abort，完成端中止）是沒有 Data 的失敗回覆。收到 UR 後，Function 必須停用 ATC，在重新啟用前不得再使用轉譯位址；CA 則表示 TA 因內部錯誤無法完成轉譯。RRS（要求重試狀態）不允許用於 Translation Request，收到時按 Malformed TLP 處理。上一章 Configuration Request 可暫時回 RRS 的條件，不能搬到這裡。以上結果也不足以單獨診斷頁面未駐留、權限被拒或平台哪個元件故障。</p><p class="source-note">Base 6.0 §10.2.3，Table 10-2 <em>Translation Completion with No Data Status Codes</em>，p.1484；§§10.2.3.1–10.2.3.5，pp.1487–1489。</p></section>
<section id="invalidate"><h2>映射改變後，收到第一筆失效回覆就結束嗎？</h2><p>接續案例，平台要改變 PASID=21h、40001000h–40001FFFh 的映射。先依模式看 Figures 10-18／10-19 的 Invalidate Request，再看 Figure 10-20 的未轉譯範圍與 Global Invalidate。假設這次 ITag=3、TC0、只針對本 PASID，範圍 4 KiB，沒有 Global Mapping。</p><p>裝置須讓新 Request 不再使用舊轉譯；相關 Outstanding Reads 必須完成或標記丟棄，相關 Posted Writes 則須推送到 TA，不能只刪 ATC entry 就回完成。若 Invalidate Request 與尚未回來的 Translation Completion 範圍重疊，還須依 §10.3.6 處理舊查詢結果，避免失效後又把舊映射放回 ATC。</p><p>為了追蹤跨 TC 的推送，本段再補一項教學條件：裝置後來有寫入需求，已另行查詢並取得 R=W=1 的有效轉譯，接著在 TC0、TC1 發出相關 Posted Writes。裝置用這兩個 TC 的回覆完成所需推送。Figure 10-5 示範一筆 Request 對應多筆 Invalidate Completion；依 Figures 10-21／10-22 解碼，此處的回覆是 <strong>Msg，Message Code=02h，依 ID 路由</strong>，不是一般 Cpl。ITag Vector 的 bit3 對應 ITag=3：</p><dl class="st-terms" aria-label="本段名詞"><div><dt>TC</dt><dd>Traffic Class，流量類別</dd></div></dl><div class="table-wrap"><table><thead><tr><th scope="col">Received TC</th><th scope="col">ITag Vector</th><th scope="col">CC</th><th scope="col">Still required</th><th scope="col">Result</th></tr></thead><tbody><tr data-invalidate-step="tc0"><td>0</td><td>00000008h</td><td>2</td><td>1</td><td>Pending</td></tr><tr data-invalidate-step="tc1"><td>1</td><td>00000008h</td><td>2</td><td>0</td><td>Complete</td></tr></tbody></table></div><p>兩筆 CC（Completion Count，失效完成訊息總數）都為 2，ITag Vector 都是 00000008h。第一筆只收齊一部分；TA 收到兩筆後，才可把本次失效視為完成並釋放這個 ITag。若 CC 編碼為零，表示八筆，不能解成不需要回覆。這個 ITag 與 Memory Request 的 Tag、PRI 的 PRG Index 都是不同機制。</p><p>前述條件保證的是規格定義的失效與推送範圍，不是應用資料已持久保存的保證；記憶體回收仍須配合平台生命週期。ATS Capability 存在時，即使 ATS Enable=0，Function 仍須能接受失效並回覆；Bus Master Enable=0 也不免除這項責任。不能因 Enable 快照為零，就把 Invalidate Completion 當成不合法。</p><p class="source-note">Base 6.0 §10.1.1，Figures 10-4／10-5，pp.1474–1476；§§10.3–10.3.6，Figures 10-18–10-22，pp.1497–1503；§10.3.8，p.1505。</p></section>
<section id="invalidate-scope"><h2>同一段位址，哪些 PASID 的快取會失效？</h2><p>先回到 Figure 10-20：Invalidate Request 的資料指出<strong>未轉譯位址範圍</strong>；Global Invalidate 欄位與要求是否帶 PASID 一起決定範圍。以下是作者建立的教學假設：Function 處於 D0、PASID Enable 已設置，目標 Function 支援 Global Invalidate；位址範圍含 <code>40001000h</code>，PASID <code>21h</code> 與 <code>22h</code> 均有效。</p><p>手機閱讀時，可左右滑動表格查看完整內容。</p><div class="table-wrap"><table><thead><tr><th>失效要求</th><th>ATC 應處理的項目</th><th>怎麼接回本章案例</th></tr></thead><tbody><tr><td>帶 PASID=21h，Global Invalidate=0</td><td>該範圍內、以 PASID 21h 查得的 non-Global Mapping；Global Mapping 可保留。</td><td>原案例只處理 21h 的非全域映射；不因此失效 22h 的非全域映射。</td></tr><tr><td>帶 PASID=21h，Global Invalidate=1</td><td>該範圍內、與任何 PASID 有關的 Global 和 non-Global Mapping；要求中 PASID 值被忽略。</td><td>21h、22h 在該範圍的相關映射都要處理；範圍外的映射不因此失效。</td></tr><tr><td>要求不帶 PASID</td><td>範圍內以「不帶 PASID」查得的項目；另外，所有位址上以任何 PASID 查得的項目也要失效。</td><td>第二個範圍比訊息的位址範圍更廣，讀 §10.3.8 時要分開看這兩條。</td></tr></tbody></table></div><p>若 Function 不支援 Global Invalidate，帶 PASID 的要求中該 bit 由 ATC 忽略，依 §10.3.8 處理以指定 PASID 查得的範圍內項目；要求不帶 PASID 時，該 bit 是 Reserved。沒有符合的項目，仍須回覆 Invalidate Completion。PASID Enable 為 0 時，規格也要求回覆；超出 Max PASID Width 範圍的 PASID 則可能被回報為 UR。</p><p>以上是訊息所要求的快取處理範圍；在途 Read、Posted Write 與 Completion 的條件仍要依前一節完成。Base 6.0 §10.3.1、§10.3.8，Figure 10-20，文件／PDF pp.1498、1505。</p></section>
<section id="implicit-invalidate"><h2>沒有收到失效訊息，快取也可能失效嗎？</h2><p>會。§10.3.7 列出由事件直接引起的<strong>隱含失效</strong>；這些事件不會另外送出 Invalidate Completion Message。</p><p>手機閱讀時，可左右滑動表格查看完整內容。</p><div class="table-wrap"><table><thead><tr><th>事件</th><th>ATC 項目的失效範圍</th></tr></thead><tbody><tr><td>Conventional Reset、Function Level Reset，或 ATS Capability 的 E 從 0 變為 1</td><td>所有 ATC 項目，包括與 PASID 有關的項目。</td></tr><tr><td>依規格停止使用某個 PASID</td><td>以該 PASID 要求的所有 non-Global Mapping 項目。</td></tr></tbody></table></div><p>例如，停止使用 PASID 21h 與重新啟用 ATS 都可能影響同一項快取，但兩者影響的範圍不同；單憑「沒有看到失效回覆」不能判定快取仍有效。停止或重用 PASID 還要完成 §6.20.1 的協調，不能以隱含失效取代在途工作的處理。Base 6.0 §10.3.7，文件／PDF p.1504。</p></section>
<section id="invalidate-race"><h2>舊轉譯回覆與失效要求交錯時，ATC 怎麼辦？</h2><p><strong>教學情境：</strong>Endpoint 已送出涵蓋 <code>40001000h</code> 的 Translation Request，回覆尚未到達；平台接著針對重疊範圍送出 Invalidate Request。兩者可能使用不同 TC，Link 不會替它們提供一般的跨 TC 順序。</p><ol><li>ATC 以 §10.3.6 的範圍規則，比對每個尚未完成的 Translation Request 與到達的 Invalidate Request。若有重疊，標記該查詢無效。</li><li>對應結果必須按規定捨棄，避免失效完成後又將舊映射留在 ATC。若回覆在 Invalidate Completion 送出前先到，規格允許實作暫時使用結果，但仍須滿足 §10.3.3 對新要求、在途 Read 和 Posted Write 的條件。</li><li>確認相關工作符合完成條件後，才送出 Invalidate Completion；平台收齊要求的全部回覆後，才把該次失效視為完成。</li></ol><p>因此，在此案例中「收到一筆轉譯回覆」和「平台已完成失效交換」是不同時間點。若啟用 Shadow Functions（影子功能），§10.3.3 也把 Function 與其 Shadows 的相關要求納入完成條件；一次失效可針對其中一者提出，對應的 Posted Write 推送仍須依規格處理。Base 6.0 §10.3.3、§10.3.6，文件／PDF pp.1501、1503–1504。</p></section>
<section id="invalidate-queue"><h2>Invalidate Queue Depth=4，代表最多只能接受四個要求嗎？</h2><p>不宜把不同機制合成同一個數字。Invalidate Queue Depth（失效佇列深度）描述 Function 在對 Link 施加反壓前可緩衝的失效要求數；<code>00000b</code> 表示此 Function 不需要這種 Invalidate Flow Control，不是「容量為零」。實際排列在輸入端、輸出端或兩者之間，由實作決定。</p><p>§10.3.4 禁止 Function 為了送出先前的 Invalidate Completion，才接受下一筆 Invalidate Request：兩者都是 Posted 交易，這種相依可能造成死結。規格的實作說明指出，單一 TA 對同一 ATC 最多有 32 筆尚未完成的失效；這個上限不要求輸入佇列本身一定是 32 格。</p><p>SR-IOV 情境要另外看 PF 與 VF 的共用範圍：所有關聯 VF 共用 PF 的 Invalidation Request queue；TA 必須讓指向該共用佇列、尚未完成的總數不超過 PF 的 Invalidate Queue Depth。本章前面假設的值為 4；若實際是 PF／VF 共用配置，就要合計相關 Function 的要求，不能替每個 VF 各算四筆。</p><dl class="st-terms" aria-label="本段名詞"><div><dt>SR-IOV</dt><dd>Single Root I/O Virtualization，單根I/O虛擬化</dd></div><div><dt>PF</dt><dd>Physical Function，實體功能</dd></div><div><dt>VF</dt><dd>Virtual Function，虛擬功能</dd></div></dl><p>Invalidate Completion 可在相同 TC、相同 CC 等條件成立時，用 ITag Vector 的多個 bit 合併回覆；拆成多個片段時，Requester ID、CC 和 ITag Vector 必須一致。合併訊息仍要讓 TA 為每個 ITag 收齊所需的回覆。Base 6.0 §10.3.2、§10.3.4–§10.3.5，文件／PDF pp.1500–1503。</p></section>
<section id="pri"><h2>頁面尚未駐留時，PRI 如何接回 ATS？</h2><p>失效完成後，裝置重新查詢 40001000h 的轉譯，這次收到 R=W=0 的回覆。平台另提供一項資訊：接下來工作需要的 40001000h 與 40002000h 兩頁尚未駐留，而這個 Function 具有合法讀取用途。缺頁是本段另設的教學條件，不能單憑 R=W=0 判定。</p><p>依 §10.4，PRI 可請平台準備頁面。兩筆 Page Request 均使用 PASID=21h、R=1、W=0、PRG（Page Request Group，頁面要求群組）Index=005h；第一筆 L=0，最後一筆 L=1。本例 PRG Response PASID Required=1，所以成功回覆也須帶相同 PASID。</p><figure class="diagram" id="pri-group-figure"><svg viewBox="0 0 900 570" style="min-width:720px" role="img" aria-labelledby="ch27-pri-zh-t ch27-pri-zh-d"><title id="ch27-pri-zh-t">兩筆頁面要求、一筆群組回覆，再重新查轉譯</title><desc id="ch27-pri-zh-d">PRG5以PASID21h提出兩筆要求，只在第二筆設Last。群組成功回覆歸還兩份額度，不提供實體位址，仍須重新走ATS。</desc><text x="130" y="35" text-anchor="middle" font-size="17">Endpoint: RID 0300h</text><path d="M130 65 V520" stroke="var(--line)" stroke-width="2"/><text x="770" y="35" text-anchor="middle" font-size="17">Host / TA</text><path d="M770 65 V520" stroke="var(--line)" stroke-width="2"/><text x="450" y="95" text-anchor="middle" font-size="16">Page 40001000h; PRG=005h; L=0</text><path d="M130 110 L770 145" stroke="var(--accent)" stroke-width="2"/><polygon points="770,145 760,140 760,150" fill="var(--accent)"/><text x="450" y="195" text-anchor="middle" font-size="16">Page 40002000h; PRG=005h; L=1</text><path d="M130 210 L770 245" stroke="var(--accent)" stroke-width="2"/><polygon points="770,245 760,240 760,250" fill="var(--accent)"/><text x="450" y="295" text-anchor="middle" font-size="16">PRG Response: Success; PRG=005h</text><path d="M770 310 L130 345" stroke="var(--accent)" stroke-width="2"/><polygon points="130,345 140,340 140,350" fill="var(--accent)"/><text x="450" y="390" text-anchor="middle" font-size="16">重新發出 ATS Translation Request</text><path d="M130 405 L770 440" stroke="var(--accent)" stroke-width="2"/><polygon points="770,440 760,435 760,445" fill="var(--accent)"/><text x="450" y="470" text-anchor="middle" font-size="16">Translation Completion：新的映射</text><path d="M770 485 L130 520" stroke="var(--accent)" stroke-width="2"/><polygon points="130,520 140,515 140,525" fill="var(--accent)"/><text x="450" y="558" text-anchor="middle" font-size="16">本組都使用 PASID=00021h；頁面要求均為 R=1、W=0。</text></svg><figcaption>作者建立的時序。PRI 群組成功後再查 ATS；新轉譯位址由後續 Translation Completion 提供。</figcaption></figure><dl class="st-terms" aria-label="本段名詞"><div><dt>RID</dt><dd>Routing ID，封包使用的路由識別碼</dd></div></dl><p>Page Request 使用 Code=04h、Route to Root Complex；PRG Response 使用 Code=05h、Route by ID。兩者都須走 TC0。依 Non-Flit 的 Figures 10-23／10-27 或 Flit 的 Figures 10-24／10-28 讀取，Page Address、PRG Index 與回覆 Code 都有自己的欄位，不是一般 Memory Completion。</p><p>Table 10-8 的 Success=0000b 表示這個群組所有頁面已成功駐留，不回傳實體頁框。案例接著重發 ATS，假設新的有效 4 KiB 映射基址為 A0000000h，原本 offset=234h 的存取才改用 A0000234h。這個新基址來自新的 Translation Completion，不是從 PRG Response 解碼。</p><p>若群組中有一頁無法滿足，介面沒有「回一半成功」的格式；須依整組 Response Code 處理。Invalid Request=0001b 表示頁面不存在或權限無法給予，在映射未改變前重送不會成功；Response Failure=1111b 則是介面終止失敗，須依規則恢復。不同 PRG 不保證按送出順序完成。</p><p class="source-note">Base 6.0 §§10.4–10.4.2.2，Figures 10-23／10-24、10-27／10-28，Tables 10-6–10-8，pp.1505–1513。</p></section>
<section id="pri-credit"><h2>兩頁放同一群組，為何還是要先留兩份額度？</h2><p>Outstanding Page Request Allocation=3 表示這個介面可同時保留三筆尚未完成的 Page Request，不是三個群組。§10.5.2.5 要求在開始一個 PRG 前，先預留該群組全部所需額度。因此本例開始前便為兩筆要求保留兩份；下表把「已送出」和「預留但還沒送出」分開：</p><div class="table-wrap"><table><thead><tr><th scope="col">時點</th><th scope="col">已送出且未回覆</th><th scope="col">本組預留且未送出</th><th scope="col">可供新群組</th></tr></thead><tbody><tr data-pri-credit="initial"><td>尚未開始</td><td>0</td><td>0</td><td>3</td></tr><tr data-pri-credit="reserve"><td>先預留本組兩筆</td><td>0</td><td>2</td><td>1</td></tr><tr data-pri-credit="first"><td>First Page Request; L=0</td><td>1</td><td>1</td><td>1</td></tr><tr data-pri-credit="last"><td>Second Page Request; L=1</td><td>2</td><td>0</td><td>1</td></tr><tr data-pri-credit="reply"><td>One PRG Success response</td><td>0</td><td>0</td><td>3</td></tr></tbody></table></div><p>最後只收到一筆 PRG Success，卻一次歸還本組兩筆 Page Request 的額度；PRG Index 也因此可再使用。若只剩一份可用額度，不能先送兩頁群組的第一頁，再等額度回來才送第二頁。Page Request 額度也不是 <a href="/DOCS/pcie-course/chapter-17.html">Chapter 17 的逐 Link Flow Control Credit</a>，兩者須分開追蹤。</p><p>同一 Function 的 Allocation 在所有 PASID 間共用，不是每個 PASID 各有三份。對 SR-IOV，Page Request Interface 可由 PF 與 VFs 共用，但每筆封包仍保留實際要求 Function 的 RID；ATS 的 VF Capability Enable 又可各自控制，不能只讀 PF 就代替所有 VF。這是 <a href="/DOCS/pcie-course/chapter-26.html">Chapter 26</a> 的作用範圍在此處的延伸。</p><dl class="st-terms" aria-label="本段名詞"><div><dt>SR-IOV</dt><dd>Single Root I/O Virtualization，單根I/O虛擬化</dd></div></dl><p class="source-note">Base 6.0 §10.4，p.1506；§10.5.1，p.1513；§10.5.2，p.1516；§10.5.2.5 <em>Outstanding Page Request Allocation (Offset 0Ch)</em>，p.1520。</p></section>
<section id="reading"><h2>下次遇到轉譯問題，如何安排查閱順序？</h2><p>先確認 RID、PASID、模式及平台服務，再核對各結構的 Support／Enable。沿 Table 10-1 看 AT 類型，依原 Request／Tag 配對 Translation Completion，先讀 S、R、W、U 與上下文，再決定實際 Memory Request。映射有改變就追 Invalidate 的範圍、ITag Vector、CC 與在途交易；有 Page Request 才另追 PRG、Last、PASID、額度與 Response Code。</p><p>若 PASID 準備停用或重用，還須依 §6.20.1 及 Chapter 10 的停止規則處理舊 Request、Posted Writes、ATC 與 Page Requests；改一個識別碼並不會自行結束舊工作。Reset 與 ATS Enable 從零變一也會引起隱含失效，不能拿先前快照當成目前快取內容。</p></section>
<section id="sources"><h2>版本與完整來源路線</h2><p>本章以 PCI Express Base Specification Revision 6.0（6.0-1.0-PUB）為準，文件印刷頁與 PDF 檢視器頁碼相同。拓撲、設定、映射、封包欄位及額度推演皆為作者建立，未執行硬體操作或平台頁面服務。本章沒有以外部網站作技術依據。</p><details class="source-note"><summary>依分析目的查來源</summary><ul><li>架構：§10.1.1 <em>Address Translation Services (ATS) Overview</em>，pp.1470–1476；Figure 10-1 <em>Example Illustrating a Platform with TA, ATPT, and ATC Elements</em>，p.1470；Figure 10-2 <em>Example ATS Translation Request/Completion Exchange</em>，p.1471；§10.1.2 <em>Page Request Interface Extension</em>，pp.1476–1477；§10.1.3 <em>Process Address Space ID (PASID)</em>，pp.1477–1478。</li><li>PASID：§6.20 <em>PASID</em>、§6.20.1 <em>Managing PASID Usage</em>、§§6.20.2–6.20.2.2，pp.791–794；Figure 6-20／Table 6-15 <em>PASID TLP Prefix</em>，pp.792–793；§7.8.9 <em>PASID Extended Capability Structure</em>，Figures 7-185–7-188、Tables 7-159–7-161，pp.1148–1151。</li><li>查詢與權限：§10.2.1 <em>Memory Requests with Address Type</em>，Table 10-1 <em>Address Type (AT) Field Encodings</em>，pp.1478–1480；§10.2.2 <em>Translation Requests</em>，Figures 10-10–10-13，pp.1480–1483；§10.2.3 <em>Translation Completion</em>，Table 10-2，p.1484；Figure 10-14 <em>Translation Completion Data Entry</em>、Table 10-3 <em>Translation Completion Data Fields</em>，pp.1485–1487；§§10.2.3.1–10.2.3.5，pp.1487–1489；§10.2.4 <em>Completions with Multiple Translations</em>，p.1496。</li><li>失效：Figures 10-4／10-5，pp.1474–1476；§10.3 <em>ATS Invalidation</em>、§10.3.1 <em>Invalidate Request</em>，Figures 10-18／10-19／10-20，pp.1497–1498；§10.3.2 <em>Invalidate Completion</em>，Figures 10-21／10-22，pp.1499–1500；§§10.3.3–10.3.8，pp.1501–1505：完成語意、接受、排序、隱含失效與 PASID 範圍。</li><li>頁面：§10.4 <em>Page Request Services</em>、§10.4.1 <em>Page Request Message</em>，Figures 10-23／10-24、Table 10-6，pp.1505–1508；§10.4.2 <em>Page Request Group Response Message</em>，Figures 10-27／10-28、Tables 10-7／10-8，pp.1511–1513。</li><li>配置：§10.5.1 <em>ATS Extended Capability</em>，Figures 10-29–10-32、Tables 10-9–10-11，pp.1513–1516；§10.5.2 <em>Page Request Extended Capability Structure</em>，Figures 10-33–10-36、Tables 10-13–10-15，pp.1516–1519；§10.5.2.4／§10.5.2.5，pp.1519–1520：實體容量與允許額度。</li><li>平台邊界：TA／IOMMU 頁表、軟體如何準備或回收頁面、程序與 PASID 的對應、錯誤恢復與裝置工作排程，需實際平台與裝置文件。不能由 Translation Completion 或 PRG Success 單獨宣稱存取、隔離政策或應用資料已完成。</li></ul></details></section>
</article>
<nav class="bottom-nav" aria-label="課程與語言版本"><a href="/DOCS/pcie-course/index.html">課程總覽</a><a href="/DOCS/pcie-course/chapter-27.html">繁中完整教學</a><a href="/pcie/chapter-27-en/">English</a></nav>
</div>
