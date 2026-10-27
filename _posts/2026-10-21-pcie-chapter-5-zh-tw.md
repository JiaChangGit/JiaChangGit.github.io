---
layout: post
title: "PCIe Chapter 5：一次讀寫如何變成 PCIe 交易"
date: 2026-10-21 00:00:00 +0800
last_modified_at: 2026-10-28 00:00:00 +0800
permalink: /pcie/chapter-5-zh-tw/
categories: [PCIe]
tags: [PCIe, Specification]
lang: zh-TW
spec_teaching: true
spec_series: pcie
description: "從 Memory Read 與 Completion 欄位出發，帶讀位元組範圍與切分回覆，再以兩個 Requester 的 Trace 示範交易配對。"
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
<nav class="bottom-nav" aria-label="課程與語言版本"><a href="/DOCS/pcie-course/index.html">課程總覽</a><a href="/DOCS/pcie-course/chapter-5.html">繁中完整教學</a><a href="/pcie/chapter-5-en/">English</a></nav>
<article class="lesson">
<p><strong>【模擬資料】</strong>本章封包欄位與讀值為教學用途建立，不代表特定硬體或平台。</p>
<section id="chapter-overview"><h2>先看本章的角色與路徑</h2><figure class="diagram"><svg viewBox="0 0 900 480" role="img" aria-labelledby="ch5-guide-title ch5-guide-desc"><title id="ch5-guide-title">主機端提出讀取，裝置端回覆資料，主機端再依交易識別與完成資訊配對。</title><desc id="ch5-guide-desc">主機端提出讀取，裝置端回覆資料，主機端再依交易識別與完成資訊配對。</desc><g data-walk-target="requester"><rect x="60" y="20" width="310" height="60" rx="9" fill="var(--surface-alt)" stroke="var(--line)"/><text x="215.0" y="45" text-anchor="middle" font-size="15">主機端 Requester：提出讀取</text></g><g data-walk-target="completer"><rect x="530" y="20" width="310" height="60" rx="9" fill="var(--surface-alt)" stroke="var(--line)"/><text x="685.0" y="45" text-anchor="middle" font-size="15">裝置端 Completer：提供資料</text></g><g data-walk-target="host-line"><path d="M215 80 L215 460" fill="none" stroke="var(--accent)" stroke-width="2" stroke-dasharray="6 5"/></g><g data-walk-target="device-line"><path d="M685 80 L685 460" fill="none" stroke="var(--accent)" stroke-width="2" stroke-dasharray="6 5"/></g><g data-walk-target="request"><path d="M215 170 L685 170" fill="none" stroke="var(--accent)" stroke-width="2"/><polygon points="685.0,170.0 675.0,165.0 675.0,175.0" fill="var(--accent)"/><text x="450.0" y="161.0" text-anchor="middle" font-size="13">Memory Read Request →</text></g><g data-walk-target="completion"><path d="M685 300 L215 300" fill="none" stroke="var(--accent)" stroke-width="2"/><polygon points="215.0,300.0 225.0,305.0 225.0,295.0" fill="var(--accent)"/><text x="450.0" y="291.0" text-anchor="middle" font-size="13">← Completion with Data</text></g><g data-walk-target="match"><rect x="55" y="380" width="320" height="65" rx="9" fill="var(--surface-alt)" stroke="var(--line)"/><text x="215.0" y="405" text-anchor="middle" font-size="15">依 Requester ID／Tag 配對</text><text x="215.0" y="428" text-anchor="middle" font-size="15">檢查狀態、資料量及位址範圍</text></g></svg><figcaption><p>作者依 Base 6.0 的 Request／Completion 規則繪製的交換示意；分段回覆在正文另行放大。</p></figcaption></figure><p class="lead">一次 MMIO（Memory-Mapped I/O，記憶體映射輸入輸出）讀取，會由主機端提出要求，再由目標端回覆資料。PCIe 用 TLP（Transaction Layer Packet，交易層封包）承載這些交換。</p><p>前情提要：Chapter 4 已完成本例的 BAR、Bridge Window 與解碼配置。現在沿同一路徑觀察一筆 4-byte 讀取。</p><dl class="st-terms" aria-label="本段名詞"><div><dt>BAR</dt><dd>Base Address Register，基底位址暫存器</dd></div></dl><p><strong>規格路線：</strong>交易類別 Table 2-1 → Request 的 ID／Tag 與 Memory Request 格式 → Completion 格式 → 分段與邊界條件。</p></section>
<p class="lead">位址配置完成後，還要理解一次存取如何形成 Request，以及 Completion 如何回到要求者。本章以一筆 MMIO 讀取串起路由、交易配對、長度與位元組範圍，接著用分段回覆說明「一筆要求」為何不一定只有一個回覆。</p><dl class="st-terms" aria-label="本段名詞"><div><dt>MMIO</dt><dd>Memory-Mapped I/O，記憶體映射輸入輸出</dd></div></dl>
<p><a href="/DOCS/pcie-course/chapter-5.html">完整中文教學</a> · <a href="/DOCS/pcie-course/index.html">課程路線</a> · <a href="/pcie/chapter-5-en/">English</a></p>
<aside class="note"><strong>版本與假設</strong><p>依 Base 6.0 的 Non-Flit Mode。沿用普通 Endpoint 03:00.0、BAR0=0x80004000；資源、映射與 Link 均已就緒。數值為作者推演。案例為 TC0、RO／IDO／No Snoop／TH 均為零，不使用 ATS、PASID、IDE、AtomicOp 或 DMWr。CPU 存取如何轉成 TLP 由平台決定，本例另假設一筆 4-byte 存取產生一個 MRd。</p><dl class="st-terms" aria-label="本段名詞"><div><dt>ATS</dt><dd>Address Translation Services，位址轉譯服務</dd></div><div><dt>PASID</dt><dd>Process Address Space ID，程序位址空間識別碼</dd></div><div><dt>IDE</dt><dd>Integrity and Data Encryption，完整性與資料加密</dd></div><div><dt>TLP</dt><dd>Transaction Layer Packet，交易層封包</dd></div></dl></aside>
<section id="types"><h2>先辨認交易，再決定要等待什麼</h2>
<p>Transaction Layer Packet（TLP）承載交易。Requester 提出要求，Completer 服務目標；這些角色隨交易改變。Memory Request 依位址送往目標，Completion 則依原 Requester ID 回送。Requester ID 與 Tag 配對尚待完成的交易，同一 Requester 不得讓兩筆同時未完成、需要 Completion 的要求共用 Tag。Base 6.0 另有較大 Tag 的能力與啟用條件，不能把它永遠視為 8 bits。</p>
<div class="table-wrap"><table><caption>常見交易與成功回覆</caption><thead><tr><th scope="col">交易</th><th scope="col">要求分類</th><th scope="col">成功回覆</th></tr></thead><tbody><tr><td>Memory Read</td><td>Non-Posted</td><td>一個或多個 CplD。</td></tr><tr><td>一般 Memory Write</td><td>Posted</td><td>沒有普通 Completion。</td></tr><tr><td>Configuration／I/O Read</td><td>Non-Posted</td><td>CplD。</td></tr><tr><td>Configuration／I/O Write</td><td>Non-Posted</td><td>Cpl。</td></tr><tr><td>Message Request</td><td>Posted</td><td>沒有交易層 Completion；上層可能另定回應。</td></tr></tbody></table></div>
<p>Configuration 依 ID 路由；I/O 依 I/O 位址；Message 依其規定採位址、ID 或隱含路由。普通 MWr 沒收到 Completion 不構成重送理由，也不代表裝置工作已完成；工作結果仍依裝置介面判斷。</p>
<details class="source-note"><summary>來源與閱讀順序</summary><p>Base 6.0 Table 2-1（pp.116–117）、Table 2-3（pp.120–122）、Figures 2-27／2-28（pp.152–154）；§2.2.7.1（pp.162–165）、§2.2.8（pp.170–171）與 Table 2-42（pp.222–223）。</p></details></section>
<section id="read"><h2>把 4-byte 讀取對到封包欄位</h2>
<p>假設平台以 Requester ID=0x0000、Tag=0x12，讀取裝置 0x80004120 的 4 bytes。這個 Requester ID 是平台假設，不能由 Root Port BDF 直接推定。MRd 使用 Fmt=000b、Type=00000b、Length=1 DW、First BE=1111b、Last BE=0000b；Request 本身沒有資料 Payload。3 DW Header 的選擇來自本例的 32-bit 目標位址格式，不是因為資料剛好是 32 bits。</p><dl class="st-terms" aria-label="本段名詞"><div><dt>BDF</dt><dd>Bus／Device／Function，匯流排、裝置與功能識別</dd></div><div><dt>DW</dt><dd>Double Word，4 bytes的資料單位</dd></div></dl>
<p>成功 CplD 使用 Fmt=010b、Type=01010b，保留原 Requester ID／Tag，Completer ID=0x0300。Length=1 DW、Status=SC、Byte Count=4，Lower Address=0x20。若四個有效 bytes 為 78 56 34 12，且本例 Register 定義為 little-endian，值為 0x12345678。</p>
<p>若另讀取 0x80004121–0x80004126 的 6 bytes，並假設裝置允許該存取，Request 要用對齊位址 0x80004120、Length=2、First BE=1110b、Last BE=0111b。成功回覆 Payload 占 2 DW，但有效資料只有 6 bytes；Byte Count=6、Lower Address=0x21。未啟用的 non-Prefetchable bytes 不得在 Completer 被讀取。</p>
<details class="source-note"><summary>欄位定位</summary><p>Figure 2-31（p.163）→ Figure 2-26／Table 2-10（pp.150–151）→ Figure 2-73（p.196）→ Tables 2-37、2-40、2-41（pp.197、217–218）。Length 的單位與零編碼見 Table 2-4（p.122）：適用的資料交易中，0 表示 1024 DW。</p></details></section>
<section id="split"><h2>Byte Count 不一定等於這個回覆的 Payload</h2>
<p>另假設 Endpoint 從有效 DMA 位址 0x40001000 讀 256 bytes，Requester ID=0x0300、Tag=0x13，BME 與映射都已準備好。Requester 的最大讀取要求為 512 bytes；Completer 的有效 Payload 上限及 RCB 都為 128 bytes，路徑接收能力相容。這筆 Length=64 DW 的要求，可按下表回覆：</p><dl class="st-terms" aria-label="本段名詞"><div><dt>DMA</dt><dd>Direct Memory Access，裝置直接存取記憶體</dd></div></dl>
<div class="table-wrap"><table><caption>作者推演的兩段成功回覆</caption><thead><tr><th scope="col">資料範圍</th><th scope="col">Length</th><th scope="col">Byte Count</th><th scope="col">Lower Address</th></tr></thead><tbody><tr><td>0x40001000–0x4000107F</td><td>32 DW</td><td>256 bytes</td><td>0x00</td></tr><tr><td>0x40001080–0x400010FF</td><td>32 DW</td><td>128 bytes</td><td>0x00</td></tr></tbody></table></div>
<p>兩個回覆皆為 SC、BCM=0，並保留相同的 Requester ID／Tag。Byte Count 包含目前片段及後續尚待回傳的資料。同一要求的回覆按位址遞增；不同 Transaction ID 的回覆可交換順序，也不得合併成一個 Completion。</p>
<p>另一項獨立限制是 Request 不得跨 4 KiB：從 0x40001FF0 讀 32 bytes 會到 0x4000200F，必須拆成兩筆各 16 bytes 的要求。若讀取回覆失敗，Cpl 不帶有效讀取資料並終止該要求；UR／CA 不能當成讀到零，RRS 也不是 MMIO 的通用重試結果。</p>
<details class="source-note"><summary>切分與邊界來源</summary><p>§2.2.7.1（pp.162–163）；§2.3.1.1（pp.214–218）；§2.4.1 D5a／D5b（p.224）與 §2.4.2（p.228）。RCB 限制回覆切分位置，4 KiB 規則限制 Request，兩者不同。</p></details></section>
<section id="matching-trace"><h2>兩個裝置用了相同 Tag，回覆要怎麼分？</h2>
<p>先把每個 Completion 的 Requester ID（原要求者識別號）和 Tag（要求者分配的交易標籤）一起對回原始 Request，再用 Status、Length、Byte Count 和 Lower Address 檢查資料範圍。完成分組後，才知道哪筆讀取還缺哪些資料。</p>
<aside class="example"><strong>【模擬資料】同一段 Trace 中有兩筆讀取</strong><p>沿用前節的 256-byte DMA 讀取，另假設 Endpoint <code>04:00.0</code> 同時提出一筆讀取。兩者都使用 Tag <code>0x13</code>，但 Requester ID 不同。本例為 Non-Flit Mode，TC0、BCM=0；所有 bytes 都啟用，Payload 與 Length 相符，兩筆 Completion 都是 SC 且 EP=0。B 的最大讀取要求至少為 128 bytes，回覆路徑的有效 Payload 上限至少為 128 bytes；其他路徑與位址映射條件均已滿足。</p><dl class="st-terms" aria-label="本段名詞"><div><dt>DMA</dt><dd>Direct Memory Access，裝置直接存取記憶體</dd></div></dl>
<p>觀察點在 Root Port 與 Switch 之間；下表是工具已辨識的邏輯交易紀錄，假設擷取範圍涵蓋這兩筆 Request 和表內 Completion，且已排除 Replay 的重複顯示。擷取結束後是否還有封包，並不在資料中。螢幕較窄時，可左右滑動表格。</p>
<div class="table-wrap"><table style="min-width: 700px"><caption>依 Requester ID 與 Tag 分組</caption><thead><tr><th scope="col">紀錄</th><th scope="col">Requester ID／Tag</th><th scope="col">要求範圍或 Completion 欄位</th></tr></thead><tbody><tr><td>Request A</td><td>0x0300／0x13</td><td>讀取 0x40001000–0x400010FF，共 256 bytes。</td></tr><tr><td>Request B</td><td>0x0400／0x13</td><td>讀取 0x40002000–0x4000207F，共 128 bytes。</td></tr><tr><td>Completion A1</td><td>0x0300／0x13</td><td>Length=32 DW、Byte Count=256、Lower Address=0x00。</td></tr><tr><td>Completion B1</td><td>0x0400／0x13</td><td>Length=32 DW、Byte Count=128、Lower Address=0x00。</td></tr></tbody></table></div>
<p><strong>先配對：</strong>A1 的識別組合是 <code>0x0300／0x13</code>，所以對應 A；B1 對應 <code>0x0400／0x13</code> 的 B。Tag 雖然相同，兩筆 Transaction ID 仍不同。每個 Requester 必須在自己的未完成要求中維持 Tag 唯一，並不需要替整個系統預留同一個 Tag。</p>
<p><strong>再核對範圍：</strong>在本例全 byte 啟用的條件下，A1 的 32 DW 是 128 bytes，對應 <code>0x40001000–0x4000107F</code>；Byte Count=256 包含這 128 bytes 和後面還要返回的 128 bytes。這段 Trace 尚未看到 A 的 <code>0x40001080–0x400010FF</code>。B1 的 128 bytes 則覆蓋 B 要求的完整範圍，不能拿來填補 A。</p>
<p>兩個 Completion 的 Lower Address 都是 0x00，因為各自起始位址的低 7 bits 都為 0；這個欄位不足以單獨還原完整位址。表中沒有提供 Completer ID 或各端的完整紀錄，因此 B 的資料範圍雖已覆蓋，仍需核對 Completion 的其他欄位及 Requester 接收結果。A 的後半段可能在擷取結束後返回、未被擷取，或尚未返回；現有資料不足以判定 Timeout 或指定故障位置。</p></aside>
<p>規格閱讀順序：Figure 2-28 先建立 Transaction ID；Figure 2-73 找到 Completion 的 Requester ID、Tag、Status、Byte Count 和 Lower Address，再讀 §2.3.1.1 的 Byte Count 與遞增位址規則。不同 Transaction ID 的 Completion 允許互相超越，不表示一定會重新排序。核對完整封包時還要確認 Completer ID、TC、Attributes、資料長度與適用條件。（Base 6.0，文件頁／PDF 頁 153、196–198、215、218、224。）</p><dl class="st-terms" aria-label="本段名詞"><div><dt>TC</dt><dd>Traffic Class，流量類別</dd></div></dl></section>

<section id="checks"><h2>用兩個問題確認理解</h2><details class="question"><summary>第一個回覆帶 128 bytes，Byte Count=256，是錯誤嗎？</summary><p>不是。它還包含這筆要求後續的 128 bytes；本片段大小另由 Length 表示。</p></details><details class="question"><summary>只看到 Base 6.0，就能套 Figure 2-31 解所有封包嗎？</summary><p>不能。本章選用 Non-Flit Mode；Flit Mode 的 Header 定義在 §2.2.1.2，布局不同。</p></details></section>
<p>下一章將從合法交易進一步檢查 DMA 位址與資料可見性。所有來源頁碼均為 Base 6.0 的文件／PDF 頁碼，查核日期為 2026-10-28。</p>
</article>
<nav class="bottom-nav" aria-label="課程與語言版本"><a href="/DOCS/pcie-course/index.html">課程總覽</a><a href="/DOCS/pcie-course/chapter-5.html">繁中完整教學</a><a href="/pcie/chapter-5-en/">English</a></nav>
</div>
