---
layout: post
title: "PCIe Chapter 12：錯誤證據、回報與隔離"
date: 2026-10-21 00:00:00 +0800
last_modified_at: 2026-10-28 00:00:00 +0800
permalink: /pcie/chapter-12-zh-tw/
categories: [PCIe]
tags: [PCIe, Specification]
lang: zh-TW
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
<div class="pcie-article spec-teaching" data-spec-series="pcie" lang="zh-Hant-TW">
<nav class="bottom-nav" aria-label="課程與語言版本"><a href="/DOCS/pcie-course/index.html">課程總覽</a><a href="/DOCS/pcie-course/chapter-12.html">繁中完整教學</a><a href="/pcie/chapter-12-en/">English</a></nav>
<article class="lesson">
<section id="chapter-overview"><h2>先看本章的角色與路徑</h2><figure class="diagram"><svg viewBox="0 0 900 500" role="img" aria-labelledby="ch12-guide-title ch12-guide-desc"><title id="ch12-guide-title">來源記錄狀態，符合條件時向 Root 回報；軟體先保存有效證據，再依規則清除。</title><desc id="ch12-guide-desc">來源記錄狀態，符合條件時向 Root 回報；軟體先保存有效證據，再依規則清除。</desc><g data-walk-target="status"><rect x="30" y="20" width="360" height="70" rx="9" fill="var(--surface-alt)" stroke="var(--line)"/><text x="210.0" y="45" text-anchor="middle" font-size="15">來源 Function：記錄錯誤狀態</text></g><g data-walk-target="control"><rect x="30" y="170" width="360" height="75" rx="9" fill="var(--surface-alt)" stroke="var(--line)"/><text x="210.0" y="195" text-anchor="middle" font-size="15">個別 Mask、Severity</text><text x="210.0" y="218" text-anchor="middle" font-size="15">及適用回報控制</text></g><g data-walk-target="record"><path d="M210 90 L210 170" fill="none" stroke="var(--accent)" stroke-width="2"/><polygon points="210.0,170.0 215.0,160.0 205.0,160.0" fill="var(--accent)"/></g><g data-walk-target="root"><rect x="510" y="170" width="360" height="75" rx="9" fill="var(--surface-alt)" stroke="var(--line)"/><text x="690.0" y="195" text-anchor="middle" font-size="15">Root：通知與來源紀錄</text></g><g data-walk-target="message"><path d="M390 210 L510 210" fill="none" stroke="var(--accent)" stroke-width="2"/><polygon points="510.0,210.0 500.0,205.0 500.0,215.0" fill="var(--accent)"/><text x="450.0" y="201.0" text-anchor="middle" font-size="13">Error Message →</text></g><g data-walk-target="save"><rect x="510" y="355" width="360" height="85" rx="9" fill="var(--surface-alt)" stroke="var(--line)"/><text x="690.0" y="380" text-anchor="middle" font-size="15">軟體保存兩端證據</text><text x="690.0" y="403" text-anchor="middle" font-size="15">核對有效性與事件關聯</text></g><g data-walk-target="notify"><path d="M690 245 L690 355" fill="none" stroke="var(--accent)" stroke-width="2"/><polygon points="690.0,355.0 695.0,345.0 685.0,345.0" fill="var(--accent)"/></g><g data-walk-target="masked"><rect x="30" y="355" width="360" height="85" rx="9" fill="var(--surface-alt)" stroke="var(--line)"/><text x="210.0" y="380" text-anchor="middle" font-size="15">狀態可保留，但本次不送訊息</text><text x="210.0" y="403" text-anchor="middle" font-size="15">Log 是否更新依各自規則</text></g><g data-walk-target="mask-path"><path d="M210 245 L210 355" fill="none" stroke="var(--accent)" stroke-width="2"/><polygon points="210.0,355.0 215.0,345.0 205.0,345.0" fill="var(--accent)"/><text x="210.0" y="291.0" text-anchor="middle" font-size="13">本例被 Mask 的錯誤</text></g></svg><figcaption><p>作者依本章案例繪製的證據關係圖。訊息來源識別與實體故障原因需依其他證據繼續判讀。</p></figcaption></figure><p class="lead">AER（Advanced Error Reporting，進階錯誤回報）提供錯誤狀態、回報控制及相關紀錄。本章先走正常的錯誤回報路徑，再解釋遮罩與 DPC 隔離如何改變軟體看到的資訊。</p><dl class="st-terms" aria-label="本段名詞"><div><dt>DPC</dt><dd>Downstream Port Containment，下游連接埠錯誤隔離</dd></div></dl><p>前情提要：Chapter 5 的交易識別用來解讀有效的 Header Log；Chapter 7 的通知概念用來理解 Root 端如何把事件交給軟體。</p><p><strong>規格路線：</strong>Figure 6-1 的分類 → Status／Mask／Severity → Figure 6-3 的回報路徑 → Root 紀錄 → 保存與清除 → DPC 分支。</p><dl class="st-terms" aria-label="本段名詞"><div><dt>DPC</dt><dd>Downstream Port Containment，下游連接埠錯誤隔離</dd></div></dl></section>
<p class="lead">PCIe 錯誤判讀需要串起偵測、回報、接收與隔離的證據。Status 記錄錯誤，不保證訊息送達；Source ID 識別回報者，不直接指出根本原因。本篇以 AER 與 DPC 的兩個獨立案例說明這些界線。</p><dl class="st-terms" aria-label="本段名詞"><div><dt>AER</dt><dd>Advanced Error Reporting，進階錯誤回報</dd></div></dl><aside class="note"><strong>版本與假設</strong><p>依 PCIe Base 6.0，所有值與事件順序均為作者設計，使用普通非 SR-IOV Function。AER 案例不支援 Flit Mode／End-End TLP Prefix，且未啟用 DPC；後面的 DPC 是另一事件。假設管理者有相應權限，讀取期間沒有未說明的新事件。</p><dl class="st-terms" aria-label="本段名詞"><div><dt>SR-IOV</dt><dd>Single Root I/O Virtualization，單根I/O虛擬化</dd></div><div><dt>TLP</dt><dd>Transaction Layer Packet，交易層封包</dd></div></dl></aside>
<section id="model"><h2>先建立從 Function 到 Root 的證據關係</h2><p>Correctable Error 可由協定恢復，但可能影響效能。Uncorrectable Error 影響功能，並依嚴重程度分為 Non-Fatal／Fatal；Non-Fatal 不能解成工作已成功，Fatal 也不是某顆晶片損壞的直接診斷。AER 提供比基本錯誤回報更細的狀態、遮罩、嚴重程度與 Log；沒有 AER 不等於完全沒有錯誤回報。</p><p>依序查看來源 Function 的 Status、偵測當時的 Mask／Severity／Device Control、有效 Header Log，再到 Root Error Status／Source ID 比對。若可能有隔離，另查 DPC Status。不同時間的設定不能自動套回事發時刻。依據：§6.2.1–§6.2.4（pp.669–679）、Figure 6-1（p.670）。</p></section>
<section id="aer"><h2>兩個 Status bit，只有一個未被遮罩</h2><p>在 03:00.0 走訪 Extended Capability 清單，依 Figure 7-154 找到 AER ID=0x0001。本例 base=0x100，Version=2、Next=0；不能把 Base 6.0 的所有 Flit 欄位都當成這個 Function 的能力。假設先前紀錄已清、設定自事件前未變，沿途轉送條件已啟用。</p><div class="table-wrap"><table><caption>來源 Function 的讀值</caption><thead><tr><th scope="col">Register／位置</th><th scope="col">值</th><th scope="col">判讀</th></tr></thead><tbody><tr><td>Header／0x100</td><td>0x00020001</td><td>AER，Version 2。</td></tr><tr><td>Uncorrectable Status／0x104</td><td>0x00044000</td><td>Completion Timeout bit 14、Malformed TLP bit 18。</td></tr><tr><td>Mask／0x108</td><td>0x00040000</td><td>只遮罩上述 Malformed TLP。</td></tr><tr><td>Severity／0x10C</td><td>0x00040000</td><td>Timeout 為 Non-Fatal；Malformed 為 Fatal。</td></tr><tr><td>AER Capabilities and Control／0x118</td><td>0x0000100E</td><td>FEP=14、Timeout Header Log Capable=1。</td></tr><tr><td>Device Control／0x78，16 bits</td><td>0x2816</td><td>Non-Fatal／Fatal Reporting Enable 均為 1。</td></tr></tbody></table><dl class="st-terms" aria-label="本段名詞"><div><dt>TLP</dt><dd>Transaction Layer Packet，交易層封包</dd></div></dl></div>
<p><code>0x00044000 &amp; ~0x00040000 = 0x00004000</code>，本例只有 Timeout 未遮罩。Masked error 仍能設定 Status，但不為該次錯誤送出 Error Message，也不寫入 Header Log、TLP Prefix Log 或 FEP。Fatal Severity 不會越過 Mask。本例 Timeout 依 Severity 與 Device Control 產生 ERR_NONFATAL；這些值是設定後快照，不是預設值。</p><p>完整回報還有沿途 Bridge、Root primary interface 與中斷條件。依 Figure 6-3 查整條路徑；Unsupported Request／Advisory Non-Fatal 另有規則，不能普遍套用本例運算。</p><details class="source-note"><summary>欄位與回報來源</summary><p>Figures 7-154–7-157／Tables 7-134–7-137（pp.1112–1117）；Figure 7-25／Table 7-21（pp.958–962）；§6.2.3.2.2（p.673）、§6.2.6／Figure 6-3（pp.683–685）、§6.2.8.1（p.692）。</p></details></section>
<section id="log"><h2>先確認 Log 有效，再解碼交易</h2><p>FEP=14 且 Status bit 14=1，因此 FEP 有效。Completion Timeout Header Log Capable bit 12=1 才支持本例記下超時 Request；Multiple Header Recording bits 9、10=0，沒有 Flit／Prefix。本例用四 DWORD Log 容量，並只解讀三 DWORD Header。</p><div class="table-wrap"><table><caption>Timeout 所對應的 Request Header</caption><thead><tr><th scope="col">位置</th><th scope="col">DWORD 值</th><th scope="col">內容</th></tr></thead><tbody><tr><td>0x11C</td><td>0x00000040</td><td>3 DW Memory Read，Length=64 DW。</td></tr><tr><td>0x120</td><td>0x030013FF</td><td>Requester=0x0300、Tag=0x13、兩個 Byte Enable 均為 0xF。</td></tr><tr><td>0x124</td><td>0x40001000</td><td>起始位址。</td></tr><tr><td>0x128</td><td>不解讀</td><td>12-byte Header 的第四個 DWORD 未定義。</td></tr></tbody></table><dl class="st-terms" aria-label="本段名詞"><div><dt>DW</dt><dd>Double Word，4 bytes的資料單位</dd></div></dl></div><p>Request 範圍為 0x40001000–0x400010FF，共 256 bytes；記錄的是未如期完成的 Request，不是超時的 Completion。Figure 7-161 的 DWORD 排列把 Header byte 0 放在 bits 31:24，不能再把上表反轉一次。Flit Log 須改查 Logged TLP was Flit Mode、Header Log Size、Logged TLP Size 與 Type／OHC。</p><dl class="st-terms" aria-label="本段名詞"><div><dt>OHC</dt><dd>Orthogonal Header Content，Flit模式的擴充標頭內容</dd></div></dl><p>Log 只能定位交易與等待結果，不能單獨指定 Endpoint、Completer、Link 或平台誰造成問題。它也不能分配給已 Mask、沒有本次 Log 的 Malformed TLP。</p><details class="source-note"><summary>有效性與格式</summary><p>§6.2.4.2（pp.679–680）；Figures 7-160、7-161／Tables 7-140、7-141（pp.1121–1123）；Memory Request 格式見 <a href="/pcie/chapter-5-zh-tw/">Chapter 5</a>。</p></details></section>
<section id="root"><h2>Root 的 Source ID 是第一個回報者</h2><div class="table-wrap"><table><caption>同一 AER 案例的 Root Port 快照</caption><thead><tr><th scope="col">Root AER base=0x100</th><th scope="col">值</th><th scope="col">意義</th></tr></thead><tbody><tr><td>Root Error Command／0x12C</td><td>0x00000002</td><td>Non-Fatal 中斷回報啟用。</td></tr><tr><td>Root Error Status／0x130</td><td>0x00000024</td><td>Uncorrectable Received 與 Non-Fatal Received。</td></tr><tr><td>Error Source ID／0x134</td><td>0x03000000</td><td>高 16 bits 為 0x0300，即 03:00.0。</td></tr></tbody></table></div><p>本例 Root 中斷向量編號為 0，且 primary interface 傳送條件已滿足。Source ID 表示回報 Timeout 的 Endpoint，不等於物理故障根因。第二個同類訊息會設 Multiple bit，但不取代第一個 Source ID。</p><p>Root Status 更新不受 Root Error Command／Root Control 控制，仍需要適用的 primary interface 傳送允許。要證明 CPU 收到中斷，還需向量與路由證據。依據：Figures 7-162–7-164／Tables 7-142–7-144（pp.1123–1127）。</p></section>
<section id="preserve"><h2>清除前，先保存能互相比對的紀錄</h2><p>作者建議先保存狀態、設定、FEP、有效 Log 與 Root／DPC 證據，並確認並行變化；多個 Register 的讀取不是自動原子快照。清除 FEP 指向的 Status 後，硬體可能換入下一筆 Log，所以先清再讀會破壞關聯。</p><p>啟用 Multiple Header Recording 且 FEP 有效時，規格建議依 FEP 逐筆處理，不清其他 Status；確定沒有 Header 的 masked error 有列明例外。PCI Status 與 AER Status 也不會互相連帶清除。依據：§6.2.4.2（pp.679–681，註腳 108）、§6.2.7.1（p.691）。</p></section>
<section id="dpc"><h2>DPC 可能在 Root 收到原訊息之前隔離</h2><p>換成另一事件：Switch Downstream Port 02:01.0 有 DPC base=0x300，不使用 RP Extensions。</p><div class="table-wrap"><table><caption>獨立 DPC 案例</caption><thead><tr><th scope="col">欄位／位置</th><th scope="col">值</th><th scope="col">意義</th></tr></thead><tbody><tr><td>Header／0x300</td><td>0x0001001D</td><td>ID=0x001D、Version=1。</td></tr><tr><td>Control／0x306，16 bits</td><td>0x000A</td><td>Trigger Enable=10b，Interrupt Enable=1。</td></tr><tr><td>Status／0x308，16 bits</td><td>0x000B</td><td>Triggered、Reason=01b、Interrupt Status=1。</td></tr><tr><td>Error Source ID／0x30A，16 bits</td><td>0x0300</td><td>觸發的 ERR_NONFATAL 來自 03:00.0。</td></tr></tbody></table></div>
<p>Enable=10b 可因本地未遮罩 Uncorrectable Error 或收到 ERR_NONFATAL／ERR_FATAL 觸發。此例 Reason=01b，Source ID 因而有效；若 Reason=00b，不能用 Source ID 判來源。觸發訊息在 Port 被丟棄，不再向 Root 轉送。本例只開 DPC 中斷、未開 DPC ERR_COR，所以不能要求 Root 出現前例的 0x24。</p><h3 id="dpc-release">清掉通知後，Link 為什麼還沒有回來？</h3>
<p>Figure 7-300 把 DPC Trigger Status 放在 bit 0，DPC Interrupt Status 放在 bit 3。兩者都能寫入 1 清除，但作用不同：bit 3 處理中斷狀態；bit 0 維持隔離，清除後才允許 LTSSM離開 Disabled，回到 Detect 嘗試建立 Link。</p><dl class="st-terms" aria-label="本段名詞"><div><dt>LTSSM</dt><dd>Link Training and Status State Machine，鏈結訓練與狀態機</dd></div></dl>
<div class="example"><p><strong>【模擬資料】以下資料為教學用途建立，不代表特定硬體或平台。</strong>延續上方獨立的 DPC 事件：02:01.0 已收到來自 03:00.0 的 ERR_NONFATAL，DPC Status 讀為 <code>0x000B</code>。本例選擇先保存證據、只清中斷，再等待解除隔離的條件。到 Switch 的上游管理路徑仍可用，軟體經由這條路徑讀寫 Port 的設定空間；本次停用的是 02:01.0 到 03:00.0 的 Link。假設過程中沒有新的 DPC 事件，也沒有其他軟體同時寫入這個 Register。</p>
<div class="table-wrap"><table><caption>同一 DPC Status 的兩次寫入，分別處理通知與隔離</caption><thead><tr><th scope="col">動作與位置</th><th scope="col">DPC Interrupt Status，bit 3</th><th scope="col">DPC Trigger Status，bit 0</th><th scope="col">後續行為</th></tr></thead><tbody><tr><td>讀取 0x308，得到 0x000B</td><td>1</td><td>1</td><td>已記錄中斷與隔離事件；Reason=01b。</td></tr><tr><td>保存證據後，以 16-bit 寫入 0x0008 到 0x308</td><td>清為 0</td><td>維持 1</td><td>本例再讀為 0x0003，Port 仍在 DPC。</td></tr><tr><td>符合釋放條件後，以 16-bit 寫入 0x0001 到 0x308</td><td>本例維持 0</td><td>清為 0</td><td>回到 Detect 嘗試訓練；Reason 已無效，不指定整個 Register 的固定讀值。</td></tr></tbody></table></div>
<p>這裡刻意拆成兩次寫入，讓通知與隔離的差別容易看清楚；規格沒有要求每套軟體都採這個拆法。真正必須遵守的是釋放條件。也因此，<strong>不能把讀出的 <code>0x000B</code> 原樣寫回，當成只清中斷的操作</strong>：那會同時對 bit 3 與 bit 0 寫 1，連隔離也一起釋放。</p>
<p>下圖的等待分支接到 §6.2.11：軟體必須先讀到 Link Status 的 Data Link Layer Link Active=0，才能釋放 DPC；若過早清除，結果為 undefined（規格未定義）。本例是 Switch Downstream Port，DPC RP Busy 不適用；支援 RP Extensions 的 Root Port 則還須等待該 bit 為 0。</p>
<figure class="diagram"><svg viewBox="0 0 820 675" style="min-width: 640px" role="img" aria-labelledby="dpc-release-title dpc-release-desc"><title id="dpc-release-title">先處理 DPC 中斷，再等 Link 停止後解除隔離</title><desc id="dpc-release-desc">本例先保存證據，只清 Interrupt Status。Link Active 仍為 1 時，Trigger Status 維持 1，繼續等待。讀到 Link Active 為 0 且軟體決定恢復後，才清 Trigger Status。Link 回到 Detect 嘗試訓練，裝置恢復仍在後面。</desc><rect x="20" y="20" width="490" height="80" rx="10" fill="var(--blue-soft)" stroke="var(--line)"/><text x="265" y="52" text-anchor="middle" font-size="17">保存 DPC 狀態與相關錯誤證據</text><text x="265" y="80" text-anchor="middle" font-size="17">本例管理 Switch Downstream Port 02:01.0</text><path d="M265 100 V145 M259 135 L265 145 L271 135" fill="none" stroke="var(--accent)" stroke-width="2.5"/><rect x="20" y="145" width="490" height="85" rx="10" fill="var(--blue-soft)" stroke="var(--line)"/><text x="265" y="179.5" text-anchor="middle" font-size="17">對 DPC Status 寫入 0x0008</text><text x="265" y="207.5" text-anchor="middle" font-size="17">只清中斷狀態，Trigger Status 仍為 1</text><path d="M265 230 V285 M259 275 L265 285 L271 275" fill="none" stroke="var(--accent)" stroke-width="2.5"/><path d="M265 285 L510 327.5 L265 370 L20 327.5 Z" fill="var(--blue-soft)" stroke="var(--line)"/><text x="265" y="319.5" text-anchor="middle" font-size="17">讀取 Link Active</text><text x="265" y="347.5" text-anchor="middle" font-size="17">是 0 還是 1？</text><path d="M265 370 V425 M259 415 L265 425 L271 415" fill="none" stroke="var(--accent)" stroke-width="2.5"/><rect x="20" y="425" width="490" height="85" rx="10" fill="var(--blue-soft)" stroke="var(--line)"/><text x="265" y="459.5" text-anchor="middle" font-size="17">對 DPC Status 寫入 0x0001</text><text x="265" y="487.5" text-anchor="middle" font-size="17">解除隔離，LTSSM 回到 Detect</text><path d="M265 510 V565 M259 555 L265 565 L271 555" fill="none" stroke="var(--accent)" stroke-width="2.5"/><rect x="20" y="565" width="490" height="85" rx="10" fill="var(--blue-soft)" stroke="var(--line)"/><text x="265" y="599.5" text-anchor="middle" font-size="17">觀察 Link 重建，完成適用的就緒等待</text><text x="265" y="627.5" text-anchor="middle" font-size="17">再恢復設定與裝置服務</text><rect x="550" y="280" width="250" height="105" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><path d="M510 327 H550 M540 321 L550 327 L540 333 M675 280 V252 H265 V285 M259 275 L265 285 L271 275" fill="none" stroke="var(--accent)" stroke-width="2.5"/><text x="675" y="307" text-anchor="middle" font-size="17">Link Active 仍為 1</text><text x="675" y="335" text-anchor="middle" font-size="17">維持 Trigger Status=1</text><text x="675" y="363" text-anchor="middle" font-size="17">等待後再讀取</text><text x="375" y="405" text-anchor="middle" font-size="16">0，且軟體決定恢復</text><text x="529" y="315" text-anchor="middle" font-size="16">1</text></svg><figcaption>作者整理的 Switch Port 軟體處理流程，並非 LTSSM 原始狀態圖。右側分支繼續等待；向下才會解除隔離。若換成支援 RP Extensions 的 Root Port，還須確認 DPC RP Busy=0。</figcaption></figure><dl class="st-terms" aria-label="本段名詞"><div><dt>LTSSM</dt><dd>Link Training and Status State Machine，鏈結訓練與狀態機</dd></div></dl>
</div>
<h3>隔離期間又來一筆 Memory Read，誰回覆？</h3>
<p>接著讀 §2.9.3 <em>Transaction Layer Behavior During Downstream Port Containment</em>。假設 Root Complex 送來一筆新的、格式合法的 Memory Read，原本應由 02:01.0 轉送到 03:00.0 的 BAR；它在 Port 已處於 DPC 時才提交給下游傳送路徑。這筆 Request 由 Port 丟棄，並由 Port 產生錯誤 Completion（交易回覆）。</p><dl class="st-terms" aria-label="本段名詞"><div><dt>BAR</dt><dd>Base Address Register，基底位址暫存器</dd></div></dl>
<p>為了知道回覆哪種錯誤，回到 Figure 7-299／Table 7-263：本例 DPC Control=<code>0x000A</code>，bit 2 的 DPC Completion Control=0，因此回覆 <strong>Completer Abort（CA，完成端中止）</strong>；若該 bit=1，才改回 Unsupported Request（UR，不支援的要求）。此 Completion 的 Completer ID 是 Downstream Port 02:01.0，因為這次由它終止 Request；前面 DPC Error Source ID 的 03:00.0 則是觸發隔離訊息的回報者。</p>
<p>在這個情境中收到 CA，是 Port 依 DPC 規則產生的結果，無法據此宣稱 Endpoint 已接受或執行該次讀取。若換成隔離前就已送出的 Request，且 DPC 使 Completion 無法回來，本例沒有 Root Port Extensions 的代回覆機制，Requester 仍可能遇到 Completion Timeout。新的 Request 如何被終止，與舊 Request 是否已完成，要分別追蹤。</p>
<h3>解除隔離後，還有哪些恢復工作？</h3>
<p>Table 7-264 說明，清除 DPC Trigger Status 後，Port 離開 DPC，LTSSM 必須回 Detect。這只是重新嘗試訓練；接著還要觀察 Link 與 Data Link 恢復，並依 §6.6.1 遵守 Conventional Reset（一般重設）之後首次 Configuration Read 的適用時序，才能繼續恢復設定與驅動程式。等待條件連回 <a href="/pcie/chapter-9-zh-tw/">Chapter 9</a>，不在這裡重複全部 Reset 流程。</p>
<p>解除隔離也會改變紀錄的判讀條件：DPC Trigger Status=0 後，DPC Trigger Reason 已不再有效，應使用先前保存的快照分析本次事件。規格允許在釋放要求已滿足後清除 Trigger Status，不必等所有相關錯誤 Status 都變成 0；因此，清空整片錯誤紀錄並不是恢復的必要前提。裝置如何重建工作、處理先前在途資料及恢復應用服務，則仍須裝置、驅動與平台的恢復程序。</p>
<details class="source-note"><summary>從欄位、隔離中的交易，到釋放條件</summary><p>依據 PCI Express Base Specification Revision 6.0。Figure 7-300 <em>DPC Status Register</em>／Table 7-264、§7.9.14.4（PDF／印刷 pp.1252–1253）定位 Trigger Status、Interrupt Status、Reason 有效條件與適用的 RP Busy。接 §6.2.11 <em>Downstream Port Containment (DPC)</em>（p.694），閱讀必須等 Link Active=0 才可釋放的要求；DPC 中斷條件見 §6.2.11.1 <em>DPC Interrupts</em>（p.697）。隔離期間 Request 的處理依 §2.9.3 <em>Transaction Layer Behavior During Downstream Port Containment</em>（p.262），再回 Figure 7-299 <em>DPC Control Register</em>／Table 7-263、§7.9.14.3（pp.1250–1251）查 DPC Completion Control。訊息來源欄位依 Figure 7-301／Table 7-265、§7.9.14.5 <em>DPC Error Source ID Register</em>（pp.1253–1254）。釋放後首次設定存取依 §6.6.1 <em>Conventional Reset</em>（pp.721–723）。上述 PDF 與印刷頁碼相同；本例的軟體處理順序是作者示範。</p></details>
</section>
<section id="questions"><h2>確認證據的限制</h2><details class="question"><summary>FEP=14，但 Status bit 14=0，還能用 Log 指認最新 Timeout 嗎？</summary><p>不能，FEP 已無效。非零 Log 不能取代有效條件。依據：§6.2.4.2。</p></details><details class="question"><summary>Status=0 能否證明從未發生錯誤？</summary><p>不能；狀態可能已清除或重設，也須考慮偵測與實作條件。依據：§6.2.4.2、Table 7-135。</p></details></section>
</article>
<nav class="bottom-nav" aria-label="課程與語言版本"><a href="/DOCS/pcie-course/index.html">課程總覽</a><a href="/DOCS/pcie-course/chapter-12.html">繁中完整教學</a><a href="/pcie/chapter-12-en/">English</a></nav>
</div>
