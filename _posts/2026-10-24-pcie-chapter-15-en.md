---
layout: post
title: "PCIe Chapter 15: Request Handling, Completions, and Advanced Transactions"
date: 2026-10-24 00:00:00 +0800
last_modified_at: 2026-10-28 00:00:00 +0800
permalink: /pcie/chapter-15-en/
categories: [PCIe]
tags: [PCIe, Specification]
lang: en
spec_teaching: true
spec_series: pcie
description: "沿接收處理圖定位格式與支援檢查，以32-bit CAS帶讀能力、兩個運算值、目標範圍和成功回覆，再比較DMWr重試與逾時後的未確認結果。"
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
<nav class="bottom-nav" aria-label="Course and editions"><a href="/DOCS/pcie-course/index.html">Course overview</a><a href="/DOCS/pcie-course/chapter-15.html">Full Chinese tutorial</a><a href="/pcie/chapter-15-zh-tw/">繁體中文</a></nav>
<article class="lesson">
<p>After parsing a TLP (Transaction Layer Packet), follow the receiver into validity and acceptance checks. An AtomicOp (Atomic Operation) performs an atomic read-modify-write; DMWr (Deferrable Memory Write) supports shared work submission. Both return completions, with different operation and status rules.</p><figure class="diagram"><svg viewBox="0 0 900 420" role="img" aria-labelledby="ch15-en-t ch15-en-d"><title id="ch15-en-t">Roles and events in this chapter</title><desc id="ch15-en-d">Trace reception checks, request execution, and the required completion response.</desc><g data-walk-target="rx"><rect x="25" y="30" width="260" height="44" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="155.0" y="59" text-anchor="middle" font-size="16">Receiver: parse request</text></g><g data-walk-target="check"><rect x="330" y="30" width="540" height="44" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="600.0" y="59" text-anchor="middle" font-size="16">Check target, support, size, and access</text></g><g data-walk-target="atom"><rect x="40" y="190" width="360" height="68" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="220.0" y="219" text-anchor="middle" font-size="16">AtomicOp: atomic read-modify-write</text><text x="220.0" y="243" text-anchor="middle" font-size="16">Return the original value</text></g><g data-walk-target="dmw"><rect x="500" y="190" width="350" height="68" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="675.0" y="219" text-anchor="middle" font-size="16">DMWr: accept shared work</text><text x="675.0" y="243" text-anchor="middle" font-size="16">Return applicable status</text></g><g data-walk-target="done"><rect x="290" y="335" width="320" height="44" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="450.0" y="364" text-anchor="middle" font-size="16">Requester: handle completion</text></g><g data-walk-target="a"><path d="M285 52 L330 52" stroke="var(--accent)" stroke-width="2" fill="none"/><polygon points="330,52 320.0,57.0 320.0,47.0" fill="var(--accent)"/><text x="307.5" y="42.0" text-anchor="middle" font-size="16"></text></g><g data-walk-target="b"><path d="M450 98 L220 190" stroke="var(--accent)" stroke-width="2" fill="none"/><polygon points="220,190 227.42781352708207,181.64370978203266 231.1417202906231,190.92847669088525" fill="var(--accent)"/><text x="335.0" y="134.0" text-anchor="middle" font-size="16">AtomicOp</text></g><g data-walk-target="c"><path d="M720 98 L670 190" stroke="var(--accent)" stroke-width="2" fill="none"/><polygon points="670,190 670.3820106563359,178.82618830217524 679.1682557520613,183.60132150637384" fill="var(--accent)"/><text x="695.0" y="134.0" text-anchor="middle" font-size="16">DMWr</text></g><g data-walk-target="d"><path d="M220 258 L350 335" stroke="var(--accent)" stroke-width="2" fill="none"/><polygon points="350,335 338.8479049790518,334.20578551779596 343.94411457319427,325.601795293919" fill="var(--accent)"/><text x="285.0" y="286.5" text-anchor="middle" font-size="16">Completion</text></g><g data-walk-target="f"><path d="M670 258 L550 335" stroke="var(--accent)" stroke-width="2" fill="none"/><polygon points="550,335 555.7160971423175,325.39134590800614 561.1165815589857,333.8076852586577" fill="var(--accent)"/><text x="610.0" y="286.5" text-anchor="middle" font-size="16">Completion</text></g></svg><figcaption>Author-drawn teaching diagram based on PCI Express Base 6.0. Exchanges unrelated to this lesson are omitted.</figcaption></figure><section id="receive"><h2>What happens after a request reaches the receiver?</h2>
<p>The previous chapter established the packet structure. Here, the Data Link Layer has checked transmission integrity, and the Transaction Layer applies packet formation and request-specific rules. Start at Figure 2-81 (p.206), follow the valid-format path, then separate Requests from Completions.</p>
<p>The first decision explicitly says <strong>Ignoring Reserved Fields</strong>. A receiver must ignore values in Reserved fields; a nonzero Reserved value alone does not establish a Malformed TLP. Other constrained fields retain their own mandatory or optional checks. This rule concerns fields marked Reserved, not Reserved encodings within active fields such as Fmt/Type; those follow their mode-specific rules. A TLP determined to be Malformed must be discarded.</p><dl class="st-terms" aria-label="Terms in this passage"><div><dt>TLP</dt><dd>Transaction Layer Packet</dd></div></dl>
<p>For a Request, continue to Figure 2-83 (p.213): determine type support, then apply the rules for that Request. The dashed programming-model check is optional. It permits certain devices to handle accesses that violate their programming model as Completer Abort; it is not a mandatory stage of every transaction. The flowchart directs the analysis, while sections 6.15 and 6.32 supply the operation-specific rules for CAS and DMWr.</p>
<p class="source">Reading route: §2.3 Handling of Received TLPs, pp.204–206, Figure 2-81 Flowchart for Handling of Received TLPs, p.206; §2.3.1 Request Handling Rules, pp.208–213, Figure 2-83 Flowchart for Handling of Received Request, p.213. Document and PDF pages match.</p></section>
<section id="malformed-credit"><h2>What happens to Flow Control when a TLP is Malformed?</h2>
<p>Continue from Figure 2-81: the Receiver has obtained a TLP from the Data Link Layer and now checks Transaction Layer formation. <strong>Every received Malformed TLP must be discarded.</strong> Read the text in §2.3 as well to determine whether Receiver Flow Control information is updated; the diagram's discard box alone does not show every condition.</p>
<div class="example"><p><strong>Teaching example:</strong> Two independent received packets have each been determined Malformed. Assume the Receiver has the VC (Virtual Channel) and buffer observations needed for the corresponding case.</p>
<p>On a phone, scroll the table horizontally to see all columns.</p><div class="table-wrap"><table><thead><tr><th scope="col">Receiver observation</th><th scope="col">Discard and Flow Control handling</th></tr></thead><tbody><tr><td>The buffer to release is ambiguous, or the TLP maps to an uninitialized or disabled VC</td><td>Discard without updating Receiver Flow Control information.</td></tr><tr><td>Other Malformed TLP</td><td>Discard; the Receiver may choose not to update Flow Control information.</td></tr></tbody></table><dl class="st-terms" aria-label="Terms in this passage"><div><dt>VC</dt><dd>Virtual Channel</dd></div></dl></div>
<p>The second row permits not updating; it does not require an update or require every device to omit one. These rules concern Receiver tracking. A single discard does not establish the state of every physical buffer or that the transmitter has received new credits. See <a href="/DOCS/pcie-course/chapter-17.html">Chapter 17</a> for the normal credit-update flow.</p></div>
<p>Separate Reserved fields from reserved encodings. In Non-Flit Mode, with Extended Fmt Field Supported=1, reserved Fmt/Type encodings are Malformed. With that capability clear, processing received TLPs with Fmt[2]=1 is undefined. With Fmt[2]=0 and an undefined Type value, the TLP is Malformed. These rules differ from ignoring values in fields marked Reserved. See <a href="/DOCS/pcie-course/chapter-14.html#prefix-reading">Chapter 14</a> for Prefix decoding.</p>
<p class="source">PCI Express Base 6.0 §2.3 and Figure 2-81, printed/PDF pp.204–206; §7.5.3.15 and Table 7-33, p.992. Check individual format rules for mandatory or optional validation.</p></section>
<section id="atomic"><h2>What must support an atomic update?</h2>
<p>An AtomicOp (Atomic Operation) reads a target location, potentially updates it, and returns its original value in one transaction. The read-modify-write sequence is atomic with respect to accesses to that location. First establish the operation in section 6.15, then follow its actual path.</p>
<div class="table-wrap"><table><thead><tr><th scope="col">Operation</th><th scope="col">Request data</th><th scope="col">Normal execution and return</th></tr></thead><tbody><tr><td>FetchAdd</td><td>One add operand</td><td>Write the sum; return the original value</td></tr><tr><td>Swap</td><td>One swap operand</td><td>Write the replacement; return the original value</td></tr><tr><td>CAS (Compare and Swap)</td><td>Compare operand, then swap operand</td><td>Replace only on equality; return the original value in either case</td></tr></tbody></table></div>
<p><strong>【模擬資料】Teaching assumptions, not measurements of a particular device or platform.</strong>Endpoint 03:00.0 sends a 32-bit CAS through one Switch toward host memory served by Root Port 00:01.0. The Request enters Switch Downstream Port 02:01.0 and exits Upstream Port 01:00.0. Both Links are operational. Address <code>0x80001FFC</code> is a platform-authorized AtomicOp target.</p>
<div class="table-wrap"><table><thead><tr><th scope="col">Participant</th><th scope="col">Fields to inspect</th><th scope="col">Assumptions and purpose</th></tr></thead><tbody>
<tr><td>Source Endpoint 03:00.0</td><td>Device Control 2: AtomicOp Requester Enable, bit 6; Command: Bus Master Enable</td><td>Both are 1. Requester capability has also been established through the device interface; a writable enable bit alone does not establish it.</td></tr>
<tr><td>Switch path</td><td>Device Capabilities 2: AtomicOp Routing Supported, bit 6; actual egress Device Control 2: AtomicOp Egress Blocking, bit 7</td><td>Relevant path Ports report Routing Supported = 1. The actual egress is Upstream Port 01:00.0, with Egress Blocking = 0.</td></tr>
<tr><td>Target Root Port 00:01.0</td><td>Device Capabilities 2: 32-bit AtomicOp Completer Supported, bit 7</td><td>1, with target permissions and platform configuration established. Routing support cannot substitute for completer support.</td></tr></tbody></table></div>
<p>These capability fields are RO in Table 7-33. The two AtomicOp controls are RW where applicable in Table 7-34. Offsets are relative to the PCI Express Capability: Device Capabilities 2 at +24h, Device Control 2 at +28h. Locate the Capability before adding the offset. Base 6.0 does not define a universal requester-capability discovery interface; it even permits a writable Requester Enable without requester capability.</p>
<p class="source">Reading route: §6.15 Atomic Operations (AtomicOps), pp.772–773; §6.15.2 AtomicOp Transaction Protocol Summary, pp.774–775; §6.15.3.1 Root Ports with AtomicOp Completer Capabilities, p.775; §7.5.3.15 Device Capabilities 2 Register (Offset 24h), Table 7-33, p.990; §7.5.3.16 Device Control 2 Register (Offset 28h), Table 7-34, p.996.</p></section>
<section id="cas-outcome"><h2>Does a successful CAS always replace the value?</h2>
<p><strong>No. CAS (Compare and Swap) writes its swap operand only when the original value equals the compare operand. A mismatch is also a normal execution result.</strong> The requester compares the returned original value with its submitted compare operand. Successful Completion (SC) has no separate comparison-match flag.</p>
<div class="example"><p><strong>【模擬資料】Teaching assumptions, not measurements of a particular device or platform.</strong> Use the preceding path with both Links in Non-Flit Mode. Each alternative independently starts at 7, with no concurrent updates. These are not sequential transactions. Requests are properly formed, EP=0, TH=0, with no Prefix and no access error.</p>
<p>Requester ID is 0300h, Tag is 2Ah, TC=0, and the address is <code>0x80001FFC</code>. For replacement, Request Data contains compare value 7 followed by swap value 9, both 32-bit operands. Values are already decoded; this example does not prescribe the target memory's endian format.</p><dl class="st-terms" aria-label="Terms in this passage"><div><dt>TC</dt><dd>Traffic Class</dd></div></dl>
<figure class="diagram"><svg style="min-width:640px" viewBox="0 0 800 520" role="img" aria-labelledby="cas-outcome-title cas-outcome-desc"><title id="cas-outcome-title">A completed CAS can either replace or preserve the value</title><desc id="cas-outcome-desc">Two independent cases start at 7. Compare 7 writes 9; compare 5 leaves 7. Both return original value 7 with SC.</desc><rect x="130" y="15" width="540" height="44" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="400.0" y="43.0" text-anchor="middle" font-size="18">Supported, valid 32-bit CAS</text><path d="M400 59 V84" fill="none" stroke="var(--accent)" stroke-width="2.5"/><polygon points="400,84 395,74 405,74" fill="var(--accent)"/><rect x="130" y="85" width="540" height="44" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="400.0" y="113.0" text-anchor="middle" font-size="18">Read original value 7 atomically</text><path d="M400 129 V154" fill="none" stroke="var(--accent)" stroke-width="2.5"/><polygon points="400,154 395,144 405,144" fill="var(--accent)"/><polygon points="400,155 550,220 400,285 250,220" fill="var(--surface-alt)" stroke="var(--accent)" stroke-width="2"/><text x="400" y="226" text-anchor="middle" font-size="18">Original = compare?</text><path d="M250 220 H165 V323" fill="none" stroke="var(--accent)" stroke-width="2.5"/><polygon points="165,323 160,313 170,313" fill="var(--accent)"/><path d="M550 220 H635 V323" fill="none" stroke="var(--accent)" stroke-width="2.5"/><polygon points="635,323 630,313 640,313" fill="var(--accent)"/><text x="135" y="205" text-anchor="middle" font-size="18">Yes: compare 7</text><text x="665" y="205" text-anchor="middle" font-size="18">No: compare 5</text><rect x="35" y="325" width="260" height="50" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="165.0" y="356.0" text-anchor="middle" font-size="18">Write swap value 9</text><rect x="505" y="325" width="260" height="50" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="635.0" y="356.0" text-anchor="middle" font-size="18">Keep target value 7</text><path d="M165 375 V405 H310 V434" fill="none" stroke="var(--accent)" stroke-width="2.5"/><polygon points="310,434 305,424 315,424" fill="var(--accent)"/><path d="M635 375 V405 H490 V434" fill="none" stroke="var(--accent)" stroke-width="2.5"/><polygon points="490,434 485,424 495,424" fill="var(--accent)"/><rect x="130" y="435" width="540" height="44" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="400.0" y="463.0" text-anchor="middle" font-size="18">Return SC + original value 7</text><text x="400" y="509" text-anchor="middle" font-size="18">Requester compares returned value with its compare operand</text></svg><figcaption>Author-drawn decision flow based on §6.15. These are alternative cases, not two CAS Requests in sequence. SC = Successful Completion.</figcaption></figure>
<div class="table-wrap"><table style="min-width:640px"><thead><tr><th scope="col">Two independent cases</th><th scope="col">Replacement</th><th scope="col">Comparison mismatch</th></tr></thead><tbody><tr><td>Original value before execution</td><td>7</td><td>7</td></tr><tr><td>Request Data: compare / swap</td><td>7 / 9</td><td>5 / 9</td></tr><tr><td>Target after execution</td><td>9</td><td>7, unchanged</td></tr><tr><td>Completion Status</td><td>SC, 000b</td><td>SC, 000b</td></tr><tr><td>Completion Data</td><td>Original value 7</td><td>Original value 7</td></tr><tr><td>Requester interpretation</td><td>Returned 7 equals submitted compare 7: replacement occurred</td><td>Returned 7 differs from submitted compare 5: no replacement</td></tr></tbody></table></div>
<h3>Why does an 8-byte Request operate on only 4 bytes?</h3>
<p>Read the CAS row and 32 Bits column of Table 2-15 (p.162): Request Length=2 DW, carrying two operands totaling 8 bytes. The target read, possible write, and returned original value each use one 32-bit value. A DW (Double Word) is 4 bytes.</p>
<p>Then read the natural-alignment and 4-KB-boundary rules on p.163. The address is divisible by 4. The target range <code>0x80001FFC–0x80001FFF</code> occupies the final 4 bytes of a 4-KB page without crossing it. Adding all 8 Request Data bytes to the target address would falsely flag a boundary violation. Both CAS operands act on one location, not two adjacent locations.</p>
<h3>Which Completion fields have AtomicOp-specific meaning?</h3>
<p>Use Figure 2-73 (p.196) to locate Requester ID and Tag and confirm 0300h / 2Ah; <a href="/DOCS/pcie-course/chapter-5.html">Chapter 5</a> explains matching. The successful response is CplD with Length=1 DW, Byte Count=4, and original value 7. A 2-DW Request does not require a 2-DW Completion.</p>
<p>Section 2.2.9.1 specifies that AtomicOp Completion Byte Count equals the operand size and Lower Address is Reserved. Although the target's low seven address bits are 7Ch, do not use Lower Address to reconstruct this result. For a Non-Flit AtomicOp Request with TH=0, First/Last DW BE are also Reserved. Memory Read byte-enable and Split Completion calculations do not apply to this example.</p>
<p class="source">Connected sources: §6.15, pp.772–773, establishes CAS semantics; §2.2.7.1 Non-Flit Mode, Table 2-15 Length Field Values for AtomicOp Requests, pp.162–163, establishes operand count, alignment, and target range; §2.2.9.1 Completion Rules for Non-Flit Mode, Figure 2-73 Completion Header Format - Non-Flit Mode, p.196, and Table 2-37 Completion Status Field Values, p.197, establish response fields and the SC encoding. Document and PDF pages match.</p></div>
<p>The field layout here is Non-Flit. Flit Mode retains the section 6.15 comparison, replacement, and original-value semantics, but uses its own Header Base/OHC rules. Do not reuse these field positions; see <a href="/DOCS/pcie-course/chapter-14.html#packet-layout">Chapter 14</a> for the layout-reading method.</p><dl class="st-terms" aria-label="Terms in this passage"><div><dt>OHC</dt><dd>Orthogonal Header Content</dd></div></dl></section>
<section id="defer"><h2>How does DMWr retry differ from a CAS mismatch?</h2>
<p>DMWr (Deferrable Memory Write, a non-posted write whose acceptance may be deferred) supports uses such as shared work queues. It requires a Completion but does not compare and exchange an operand. For a temporary condition, the completer may return Request Retry Status (RRS), leaving the target unchanged.</p>
<p><strong>【模擬資料】Teaching assumptions, not measurements of a particular device or platform.</strong> A separate path and completer support DMWr, all required controls are enabled, and DMWr Requester Enable is 1. A first submission encounters a temporarily unavailable queue; the completer returns RRS without enqueuing the item. The requester may later submit a new Request under its implementation policy. A successful submission then proceeds according to the queue interface; acceptance of an item and completion of its work are separate events.</p>
<div class="table-wrap"><table><thead><tr><th scope="col">Observed result</th><th scope="col">Completer action</th><th scope="col">Requester decision</th></tr></thead><tbody>
<tr><td>CAS: SC, returned value differs from compare</td><td>Comparison completed; no replacement</td><td>This transaction has a known outcome. Any further attempt follows the synchronization protocol.</td></tr>
<tr><td>DMWr: RRS for a temporary condition</td><td>No acceptance of this update; target unchanged</td><td>Retry is permitted, not required; timing and whether to modify a new Request are implementation specific.</td></tr>
<tr><td>Ordinary Posted Memory Write</td><td>No ordinary Completion conveys temporary rejection</td><td>Use the device interface or another synchronization mechanism to establish acceptance or work completion.</td></tr></tbody></table></div>
<p>The temporary-condition RRS in section 6.32 is not an error, and the completer must not assume another attempt. DMWr has additional atomicity, size, routing, Egress Blocking, and error rules. A shared status name does not make Configuration Request retry handling applicable.</p>
<p class="source">Reading route: §6.32 Deferrable Memory Write, pp.857–860; p.858 covers temporary-condition RRS and unchanged targets; p.860 covers Requester Enable and retry discretion. Table 2-37, p.197, encodes RRS as 010b.</p></section>
<section id="timeout"><h2>Can a timed-out CAS simply be sent again?</h2>
<p>First identify the retry layer. Data Link Replay protects one transmission between adjacent partners and prevents duplicate delivery. A requester-generated new CAS causes another operation. See <a href="/DOCS/pcie-course/chapter-8.html">Chapter 8</a> for that distinction.</p>
<p>Completion Timeout records the requester's failure to receive a required response. For the preceding CAS, at least two timelines remain possible: the Request never reached the target, or the target performed the comparison and replacement but the requester did not receive the Completion. A requester-side Timeout alone cannot distinguish them.</p>
<p>Recovery therefore cannot treat an unconfirmed operation as unexecuted and blindly issue it again. Preserve the original Request, Requester ID/Tag, path traces, and error evidence, then follow the platform or device synchronization and recovery protocol. A later memory value may reflect other agents' updates and cannot replace the missing Completion. This is an analysis boundary derived from the response mechanism; Base 6.0 supplies no universal software-retry algorithm.</p>
<p>A normal SC also needs request-specific interpretation. CAS returns the original value to establish whether replacement occurred. A split Memory Read needs all required Completions. Section 2.8 timeout ranges detect abnormal conditions and must not estimate normal service latency. If a subsequent Request must follow observation of an AtomicOp at the completer, section 6.15.2 requires the requester to wait for its Completion before issuing that Request.</p>
<p>Atomicity applies to the target operation. For Root Ports supporting AtomicOps, section 6.15.3.1 additionally requires host-memory accesses on behalf of an AtomicOp to be atomic relative to processor/device accesses to that range and to preserve processor atomic-operation atomicity. The complete synchronization algorithm, publication ordering at other locations, and software memory attributes still require platform and CPU documentation; one CAS does not establish those conditions.</p>
<p class="source">Reading route: §2.8 Completion Timeout Mechanism, pp.259–260; §6.15.2, p.774; §6.15.3.1, p.775. Replay versus software retry is applied here without repeating its state machines.</p>
<h3>Are Locked Transactions the same mechanism?</h3><p>Locked Transactions have different section 6.5.1 restrictions: only the Root Complex may initiate them; PCI Express Endpoints must not support locked accesses; new software must not cause locked accesses to I/O devices. They are not an unrestricted fallback for unsupported AtomicOps.</p></section>
<section id="sources"><h2>Edition and sources</h2><p>Technical authority: PCI Express Base Specification Revision 6.0 (6.0-1.0-PUB). Printed document and PDF viewer pages match. Diagrams and numerical scenarios are author-created from the cited rules, not copied specification figures or hardware measurements. This revision teaches CAS outcomes and DMWr retry; full AtomicOp formats, DMWr capabilities, and all error conditions remain for deeper coverage.</p><details class="source-note"><summary>Complete source locations and purpose</summary><ul>
<li>§2.3 Handling of Received TLPs, pp.204–206; Figure 2-81 Flowchart for Handling of Received TLPs, p.206: receive entry, Reserved fields, and Request/Completion branches.</li>
<li>§2.3.1 Request Handling Rules, pp.208–213; Figure 2-83 Flowchart for Handling of Received Request, p.213: support, optional programming-model checks, and response.</li>
<li>§2.2.7.1 Non-Flit Mode, pp.162–163; Table 2-15 Length Field Values for AtomicOp Requests, p.162: operands, Length, alignment, and CAS target range.</li>
<li>§2.2.9.1 Completion Rules for Non-Flit Mode, pp.196–198; Figure 2-73 Completion Header Format - Non-Flit Mode, p.196; Table 2-37 Completion Status Field Values, p.197: AtomicOp Byte Count, Reserved Lower Address, Requester ID/Tag, and status encodings.</li>
<li>§6.15 Atomic Operations (AtomicOps), pp.772–773; §6.15.2 AtomicOp Transaction Protocol Summary, pp.774–775; §6.15.3.1 Root Ports with AtomicOp Completer Capabilities, p.775: operations, path support, waiting, and host-memory atomicity.</li>
<li>§7.5.3.15 Device Capabilities 2 Register (Offset 24h), Table 7-33, p.990; §7.5.3.16 Device Control 2 Register (Offset 28h), Table 7-34, p.996: AtomicOp support, enable, blocking, field scope, and attributes.</li>
<li>§6.32 Deferrable Memory Write, pp.857–860: temporary-condition RRS, unchanged target, enable, and retry discretion.</li>
<li>§2.8 Completion Timeout Mechanism, pp.259–260: incomplete responses and service-latency limits; §6.5.1 Introduction, p.718: Locked Transaction initiator and support restrictions.</li></ul></details></section>
</article>
<nav class="bottom-nav" aria-label="Course and editions"><a href="/DOCS/pcie-course/index.html">Course overview</a><a href="/DOCS/pcie-course/chapter-15.html">Full Chinese tutorial</a><a href="/pcie/chapter-15-zh-tw/">繁體中文</a></nav>
</div>
