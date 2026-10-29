---
layout: post
title: "PCIe Chapter 15：接收要求、完成回覆與進階交易"
date: 2026-10-24 00:00:00 +0800
last_modified_at: 2026-10-28 00:00:00 +0800
permalink: /pcie/chapter-15-zh-tw/
categories: [PCIe]
tags: [PCIe, Specification]
lang: zh-TW
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
<div class="pcie-article spec-teaching" data-spec-series="pcie" lang="zh-Hant-TW">
<nav class="bottom-nav" aria-label="課程與語言版本"><a href="/DOCS/pcie-course/index.html">課程總覽</a><a href="/DOCS/pcie-course/chapter-15.html">繁中完整教學</a><a href="/pcie/chapter-15-en/">English</a></nav>
<article class="lesson">
<p>前章已能定位 TLP（Transaction Layer Packet，交易層封包）的欄位。現在沿接收端追蹤：先檢查封包，再決定目標是否接受。AtomicOp（Atomic Operation，原子操作）與 DMWr（Deferrable Memory Write，可延後的記憶體寫入）都有完成回覆，但各自保證的操作與回覆狀態不同。</p><figure class="diagram"><svg viewBox="0 0 900 420" role="img" aria-labelledby="ch15-zh-t ch15-zh-d"><title id="ch15-zh-t">本章角色與事件</title><desc id="ch15-zh-d">由合法要求進到能力檢查，正常完成與暫時拒收分開閱讀。</desc><g data-walk-target="rx"><rect x="25" y="30" width="260" height="44" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="155.0" y="59" text-anchor="middle" font-size="16">接收端：解析要求</text></g><g data-walk-target="check"><rect x="330" y="30" width="540" height="44" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="600.0" y="59" text-anchor="middle" font-size="16">檢查目標、能力、大小與存取條件</text></g><g data-walk-target="atom"><rect x="40" y="190" width="360" height="68" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="220.0" y="219" text-anchor="middle" font-size="16">AtomicOp：原子讀改寫</text><text x="220.0" y="243" text-anchor="middle" font-size="16">回傳原值</text></g><g data-walk-target="dmw"><rect x="500" y="190" width="350" height="68" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="675.0" y="219" text-anchor="middle" font-size="16">DMWr：接收共享工作</text><text x="675.0" y="243" text-anchor="middle" font-size="16">依狀況回覆</text></g><g data-walk-target="done"><rect x="290" y="335" width="320" height="44" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="450.0" y="364" text-anchor="middle" font-size="16">要求者：依完成狀態往下走</text></g><g data-walk-target="a"><path d="M285 52 L330 52" stroke="var(--accent)" stroke-width="2" fill="none"/><polygon points="330,52 320.0,57.0 320.0,47.0" fill="var(--accent)"/><text x="307.5" y="42.0" text-anchor="middle" font-size="16"></text></g><g data-walk-target="b"><path d="M450 98 L220 190" stroke="var(--accent)" stroke-width="2" fill="none"/><polygon points="220,190 227.42781352708207,181.64370978203266 231.1417202906231,190.92847669088525" fill="var(--accent)"/><text x="335.0" y="134.0" text-anchor="middle" font-size="16">AtomicOp</text></g><g data-walk-target="c"><path d="M720 98 L670 190" stroke="var(--accent)" stroke-width="2" fill="none"/><polygon points="670,190 670.3820106563359,178.82618830217524 679.1682557520613,183.60132150637384" fill="var(--accent)"/><text x="695.0" y="134.0" text-anchor="middle" font-size="16">DMWr</text></g><g data-walk-target="d"><path d="M220 258 L350 335" stroke="var(--accent)" stroke-width="2" fill="none"/><polygon points="350,335 338.8479049790518,334.20578551779596 343.94411457319427,325.601795293919" fill="var(--accent)"/><text x="285.0" y="286.5" text-anchor="middle" font-size="16">完成回覆</text></g><g data-walk-target="f"><path d="M670 258 L550 335" stroke="var(--accent)" stroke-width="2" fill="none"/><polygon points="550,335 555.7160971423175,325.39134590800614 561.1165815589857,333.8076852586577" fill="var(--accent)"/><text x="610.0" y="286.5" text-anchor="middle" font-size="16">完成回覆</text></g></svg><figcaption>作者依 Base 6.0 繪製的教學示意；省略與本章無關的交換。</figcaption></figure><section id="receive"><h2>要求到了接收端，還要經過哪些判斷？</h2>
<p>前章已說明如何辨認封包結構。本章從接收端開始：Data Link Layer 已檢查傳輸完整性，接著由 Transaction Layer 按封包格式和要求種類處理。先看 Figure 2-81（p.206）的 Start，再沿符合格式的分支往下，最後分成 Request 與 Completion。</p>
<p>閱讀第一個判斷框時，留意 <strong>Ignoring Reserved Fields</strong>。接收端必須忽略 Reserved 欄位的值；封包中出現非零的 Reserved 值，並不能直接當成 Malformed TLP。至於有明確限制的格式欄位，仍須按各自的必要或可選檢查規則處理。這裡指標為 Reserved 的欄位，不包含 Fmt／Type 等有效欄位中的 Reserved 編碼；後者仍按適用模式的規則判斷。已判定為 Malformed 的 TLP 必須丟棄。</p><dl class="st-terms" aria-label="本段名詞"><div><dt>TLP</dt><dd>Transaction Layer Packet，交易層封包</dd></div></dl>
<p>確認是 Request 後，再接 Figure 2-83（p.213）：先判斷要求種類是否受支援，接著依該種類的規則執行。圖中虛線框是可選的 programming model 檢查；它允許特定裝置將違反自身存取限制的要求以 Completer Abort 處理，並非每筆要求都要依序走過的階段。這張圖提供分流，真正決定 CAS 或 DMWr 結果的細節，仍要回到 §6.15 或 §6.32。</p>
<p class="source">規格閱讀：§2.3 Handling of Received TLPs，pp.204–206，Figure 2-81 Flowchart for Handling of Received TLPs，p.206；§2.3.1 Request Handling Rules，pp.208–213，Figure 2-83 Flowchart for Handling of Received Request，p.213。文件頁與 PDF 頁相同。</p></section>
<section id="malformed-credit"><h2>封包格式錯誤時，接收端會怎麼處理 credit？</h2>
<p>接續 Figure 2-81：接收端已從 Data Link Layer 收到 TLP，現在檢查交易層格式。<strong>所有被判定為 Malformed 的 TLP 都必須丟棄。</strong>接著讀 §2.3 旁邊的文字，才能知道 Receiver Flow Control（接收端流量控制）資訊是否更新；不能只看圖上的「Discard TLP」。</p>
<div class="example"><p><strong>【模擬資料】以下資料為教學用途建立，不代表特定硬體或平台。</strong>兩筆互不相依的封包都已被判定為 Malformed。假設接收端已有各筆封包所需的 VC（Virtual Channel，虛擬通道）與緩衝區觀察資料。</p>
<p>手機閱讀時，表格可以左右滑動。</p><div class="table-wrap"><table><thead><tr><th scope="col">接收端觀察</th><th scope="col">丟棄與 Flow Control 處理</th></tr></thead><tbody><tr><td>無法確定應釋放哪個 buffer，或 TLP 對應未初始化／停用的 VC</td><td>必須丟棄，且不得更新接收端的 Flow Control 資訊。</td></tr><tr><td>其他 Malformed TLP</td><td>仍必須丟棄；接收端可以選擇不更新 Flow Control 資訊。</td></tr></tbody></table><dl class="st-terms" aria-label="本段名詞"><div><dt>VC</dt><dd>Virtual Channel，虛擬通道</dd></div></dl></div>
<p>第二列的「可以選擇不更新」不等於必須更新，也不等於每種裝置都選擇不更新。這些規則描述接收端追蹤資訊，不能只憑一次丟棄就推論實體 buffer 的全部狀態或傳送端已收到新的 credit。正常額度更新流程見 <a href="/DOCS/pcie-course/chapter-17.html">Chapter 17</a>。</p></div>
<p>判定格式時，也要分清 Reserved 欄位和保留的編碼。在 Non-Flit Mode，若 Extended Fmt Field Supported=1，使用 Reserved 的 Fmt／Type 編碼須按 Malformed 處理；若該能力位為 0，對 Fmt[2]=1 的接收處理是 undefined（未定義）。Fmt[2]=0 且 Type 值未定義時，則須按 Malformed 處理。這與「接收端忽略 Reserved 欄位的值」是不同規則；Prefix 的位元拆解見 <a href="/DOCS/pcie-course/chapter-14.html#prefix-reading">Chapter 14</a>。</p>
<p class="source">PCI Express Base 6.0 §2.3、Figure 2-81，文件頁／PDF 頁 204–206；§7.5.3.15、Table 7-33，p.992。個別格式是否需要檢查，仍應查其對應條文。</p></section>
<section id="atomic"><h2>要更新共用計數器或比較後交換，先確認哪些能力？</h2>
<p>AtomicOp（Atomic Operation，原子操作）在一次交易中讀取目標、依操作更新目標，再回傳原值。這段讀改寫不可被其他對該位置的存取拆開觀察。先用 §6.15 確認操作語意，再沿實際路徑查看各元件。</p>
<div class="table-wrap"><table><thead><tr><th scope="col">操作</th><th scope="col">Request 提供的資料</th><th scope="col">正常完成時的動作與回傳值</th></tr></thead><tbody>
<tr><td>FetchAdd</td><td>一個加數</td><td>寫回相加結果，回傳原值</td></tr><tr><td>Swap</td><td>一個交換值</td><td>寫入交換值，回傳原值</td></tr><tr><td>CAS（Compare and Swap，比較後交換）</td><td>先放比較值，再放交換值</td><td>相等才寫入交換值；相等或不相等，都回傳原值</td></tr></tbody></table></div>
<p><strong>【模擬資料】以下資料為教學用途建立，不代表特定硬體或平台。</strong>本例由 Endpoint 03:00.0 經一個 Switch，向 Root Port 所服務的主記憶體發出 32-bit CAS。要求先進入 Switch Downstream Port 02:01.0，再從 Upstream Port 01:00.0 送往 Root Port 00:01.0。兩條 Link 都已可正常傳輸，目標為平台允許 AtomicOp 存取的位置 <code>0x80001FFC</code>。</p>
<div class="table-wrap"><table><thead><tr><th scope="col">沿本例路徑查詢</th><th scope="col">應核對的正式欄位</th><th scope="col">本例假設與用途</th></tr></thead><tbody>
<tr><td>來源 Endpoint 03:00.0</td><td>Device Control 2：AtomicOp Requester Enable，bit 6；Command：Bus Master Enable</td><td>兩者均為 1，且已由裝置介面確認具有發起能力。Requester Enable 可寫入，仍不代表具有這項能力。</td></tr>
<tr><td>Switch 路徑</td><td>Device Capabilities 2：AtomicOp Routing Supported，bit 6；實際出口的 Device Control 2：AtomicOp Egress Blocking，bit 7</td><td>路徑相關 Ports 的 Routing Supported 為 1；本次出口是 Upstream Port 01:00.0，其 Egress Blocking 為 0。</td></tr>
<tr><td>目標 Root Port 00:01.0</td><td>Device Capabilities 2：32-bit AtomicOp Completer Supported，bit 7</td><td>為 1，並已確認該主記憶體位置的存取權限與平台設定。這裡查的是完成端支援，不以 Routing Supported 代替。</td></tr></tbody></table></div>
<p>Table 7-33 的這些能力欄位為 RO；Table 7-34 的兩個 AtomicOp 控制欄位在適用元件上為 RW。所有 offset 都相對於 PCI Express Capability：Device Capabilities 2 在 +24h，Device Control 2 在 +28h。請先走訪 Capability，再加相對位移。Base 6.0 沒有定義統一的 Requester 能力探索介面；也明確允許沒有發起能力的元件將 Requester Enable 做成可寫，因此讀回 1 仍須搭配裝置資料。</p>
<p class="source">規格閱讀：§6.15 Atomic Operations (AtomicOps)，pp.772–773；§6.15.2 AtomicOp Transaction Protocol Summary，pp.774–775；§6.15.3.1 Root Ports with AtomicOp Completer Capabilities，p.775；§7.5.3.15 Device Capabilities 2 Register (Offset 24h)，Table 7-33，p.990；§7.5.3.16 Device Control 2 Register (Offset 28h)，Table 7-34，p.996。</p></section>
<section id="cas-outcome"><h2>CAS 回覆成功，目標就一定被換掉了嗎？</h2>
<p><strong>不一定。CAS（比較後交換）只在原值等於比較值時寫入交換值；比較不相等也是正常執行結果。</strong>要求者要把回傳的原值與自己送出的比較值相比，才能知道這次是否交換。Successful Completion（SC，交易正常完成）本身沒有另設「比較相等」的旗標。</p>
<div class="example"><p><strong>【模擬資料】以下資料為教學用途建立，不代表特定硬體或平台。</strong>沿用前節路徑，兩條 Link 均使用 Non-Flit Mode。本節左右案例各自從目標原值 7 開始，沒有其他處理器或裝置同時更新它；兩例不是連續交易。封包格式合法、EP=0，TH=0，不使用 Prefix，並假設存取過程沒有錯誤。</p>
<p>本次 Request 的 Requester ID 為 0300h，Tag 為 2Ah，TC=0；目標地址為 <code>0x80001FFC</code>。正常交換的案例送出比較值 7、交換值 9，Request Data 依序包含這兩個 32-bit 運算值。此處列的是解碼後的數值，不預設目標記憶體採用哪種 endian 格式。</p><dl class="st-terms" aria-label="本段名詞"><div><dt>TC</dt><dd>Traffic Class，流量類別</dd></div></dl>
<figure class="diagram"><svg style="min-width:640px" viewBox="0 0 800 520" role="img" aria-labelledby="cas-outcome-title cas-outcome-desc"><title id="cas-outcome-title">CAS 正常完成後，目標可能更新，也可能保持原值</title><desc id="cas-outcome-desc">兩個獨立案例都從原值 7 開始。比較值為 7 時寫入 9；比較值為 5 時保持 7。兩者都回覆 SC 並回傳原值 7。</desc><rect x="130" y="15" width="540" height="44" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="400.0" y="43.0" text-anchor="middle" font-size="18">支援且格式合法的 32-bit CAS</text><path d="M400 59 V84" fill="none" stroke="var(--accent)" stroke-width="2.5"/><polygon points="400,84 395,74 405,74" fill="var(--accent)"/><rect x="130" y="85" width="540" height="44" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="400.0" y="113.0" text-anchor="middle" font-size="18">原子操作中讀得原值 7</text><path d="M400 129 V154" fill="none" stroke="var(--accent)" stroke-width="2.5"/><polygon points="400,154 395,144 405,144" fill="var(--accent)"/><polygon points="400,155 550,220 400,285 250,220" fill="var(--surface-alt)" stroke="var(--accent)" stroke-width="2"/><text x="400" y="226" text-anchor="middle" font-size="18">原值等於比較值？</text><path d="M250 220 H165 V323" fill="none" stroke="var(--accent)" stroke-width="2.5"/><polygon points="165,323 160,313 170,313" fill="var(--accent)"/><path d="M550 220 H635 V323" fill="none" stroke="var(--accent)" stroke-width="2.5"/><polygon points="635,323 630,313 640,313" fill="var(--accent)"/><text x="135" y="205" text-anchor="middle" font-size="18">相等：比較值 7</text><text x="665" y="205" text-anchor="middle" font-size="18">不相等：比較值 5</text><rect x="35" y="325" width="260" height="50" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="165.0" y="356.0" text-anchor="middle" font-size="18">寫入交換值 9</text><rect x="505" y="325" width="260" height="50" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="635.0" y="356.0" text-anchor="middle" font-size="18">目標保持 7</text><path d="M165 375 V405 H310 V434" fill="none" stroke="var(--accent)" stroke-width="2.5"/><polygon points="310,434 305,424 315,424" fill="var(--accent)"/><path d="M635 375 V405 H490 V434" fill="none" stroke="var(--accent)" stroke-width="2.5"/><polygon points="490,434 485,424 495,424" fill="var(--accent)"/><rect x="130" y="435" width="540" height="44" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="400.0" y="463.0" text-anchor="middle" font-size="18">兩者都回覆 SC，並回傳原值 7</text><text x="400" y="509" text-anchor="middle" font-size="18">要求者再比對回傳原值與自己的比較值</text></svg><figcaption>作者依 §6.15 繪製的判斷流程。左右是兩個獨立案例，不是連續執行兩次 CAS。SC（Successful Completion）表示交易正常完成。</figcaption></figure>
<div class="table-wrap"><table style="min-width:640px"><thead><tr><th scope="col">同一組前提下的兩個獨立案例</th><th scope="col">比較相等並交換</th><th scope="col">比較不相等</th></tr></thead><tbody>
<tr><td>執行前的原值</td><td>7</td><td>7</td></tr><tr><td>Request Data：比較值／交換值</td><td>7／9</td><td>5／9</td></tr><tr><td>執行後目標值</td><td>9</td><td>7，保持原值</td></tr><tr><td>Completion Status</td><td>SC，000b</td><td>SC，000b</td></tr><tr><td>Completion Data</td><td>原值 7</td><td>原值 7</td></tr><tr><td>要求者如何判斷？</td><td>回傳 7 等於送出的比較值 7，這次完成交換</td><td>回傳 7 不等於送出的比較值 5，這次沒有交換</td></tr></tbody></table></div>
<h3>Request 帶 8 bytes，為什麼目標只占 4 bytes？</h3>
<p>查 Table 2-15（p.162）時，先選 CAS 這一列，再看 32 Bits 這一欄，得到 Request Length=2 DW，也就是兩個運算值共 8 bytes。目標的讀取、可能的寫回，以及回傳原值，各自仍是單一 32-bit 值。DW（Double Word）為 4 bytes。</p>
<p>接著讀 p.163 的自然對齊與 4-KB 邊界規則。本例地址可被 4 整除，目標範圍為 <code>0x80001FFC–0x80001FFF</code>，剛好占該 4-KB 頁面最後 4 bytes，沒有跨頁。若直接把 Request 的 8-byte Data 長度加到地址上，就會錯把這筆 CAS 判成跨界。CAS 的兩個運算值共同作用於同一個目標，不是寫入兩個相鄰位置。</p>
<h3>再看 Completion，哪些欄位要按 AtomicOp 解讀？</h3>
<p>用 Figure 2-73（p.196）定位回覆的 Requester ID 與 Tag，核對仍是 0300h／2Ah；配對方法已在 <a href="/DOCS/pcie-course/chapter-5.html">Chapter 5</a> 帶讀。這次成功回覆是 CplD，Length=1 DW，Byte Count=4，Data 為原值 7。Request 帶 2 DW，並不要求 Completion 也回傳 2 DW。</p>
<p>§2.2.9.1 特別規定：AtomicOp Completion 的 Byte Count 等於運算值大小，Lower Address 為 Reserved。因此即使地址低 7 bits 為 7Ch，也不拿 Lower Address 重建本次結果。Non-Flit Mode 的 AtomicOp Request 在 TH=0 時，其 First／Last DW BE 也為 Reserved；本例不套用 Memory Read 的有效 Byte 或 Split Completion 計算。</p>
<p class="source">規格串接：§6.15，pp.772–773 確認 CAS 語意；§2.2.7.1 Non-Flit Mode，Table 2-15 Length Field Values for AtomicOp Requests，pp.162–163 確認兩個運算值、對齊與目標範圍；§2.2.9.1 Completion Rules for Non-Flit Mode，Figure 2-73 Completion Header Format - Non-Flit Mode，p.196，及 Table 2-37 Completion Status Field Values，p.197，確認回覆欄位與 SC 編碼。文件頁與 PDF 頁相同。</p></div>
<p>本例使用 Non-Flit 欄位布局。Flit Mode 下仍依 §6.15 解讀比較、交換與回傳原值，但封包要改用對應的 Header Base／OHC 規則，不能照搬本例的欄位位置；兩種布局的閱讀方法見 <a href="/DOCS/pcie-course/chapter-14.html#packet-layout">Chapter 14</a>。</p><dl class="st-terms" aria-label="本段名詞"><div><dt>OHC</dt><dd>Orthogonal Header Content，Flit模式的擴充標頭內容</dd></div></dl></section>
<section id="defer"><h2>DMWr 的「重試」與 CAS 的「比較不相等」有何不同？</h2>
<p>DMWr（Deferrable Memory Write，可由完成端延後接受的非 Posted 寫入）適合共享工作佇列。它有必要的 Completion，但不是用來讀改寫一個比較值。遇到暫時條件時，完成端可回覆 Request Retry Status（RRS，要求重試狀態），並保持目標不變。</p>
<p><strong>【模擬資料】以下資料為教學用途建立，不代表特定硬體或平台。</strong>假設另一組路徑與完成端已支援並啟用 DMWr，來源的 DMWr Requester Enable 也為 1。第一次提交工作項目時，共享佇列暫時無法接受，完成端因此回覆 RRS，沒有加入這項工作。要求者稍後可依實作政策重新提交；若新要求成功，才按該佇列的介面接續追蹤工作。成功接受提交與工作內容已執行完畢，仍是不同時點。</p>
<div class="table-wrap"><table><thead><tr><th scope="col">觀察到的結果</th><th scope="col">完成端這次做了什麼？</th><th scope="col">要求者接下來的依據</th></tr></thead><tbody>
<tr><td>CAS：SC，但回傳值不等於比較值</td><td>已完成比較，沒有交換</td><td>這次交易已有確定結果；後續是否再競爭更新，由同步協定決定</td></tr>
<tr><td>DMWr：因暫時條件回覆 RRS</td><td>未接受這次更新，目標保持不變</td><td>允許重送，但不要求一定重送；何時重送、是否修改內容由實作決定</td></tr>
<tr><td>普通 Posted Memory Write</td><td>沒有一般 Completion 可用來表達暫時拒收</td><td>是否已接受或完成裝置工作，須依裝置介面或其他同步機制確認</td></tr></tbody></table></div>
<p>這裡的 RRS 是 §6.32 明確允許的暫時拒收結果，不是錯誤。完成端也不得假設要求者一定會再送一次。DMWr 的原子更新、大小、路由、Egress Blocking 與錯誤條件另有規則，不能只因為看見同一個 Status 名稱，就套用 Configuration Request 的重試流程。</p>
<p class="source">規格閱讀：§6.32 Deferrable Memory Write，pp.857–860；p.858 為暫時條件、RRS 與目標保持規則，p.860 為 Requester Enable 及是否重送的規則。Table 2-37，p.197，將 RRS 編為 010b。</p></section>
<section id="timeout"><h2>如果 CAS 逾時，能把同一筆要求再送一次嗎？</h2>
<p>先確認是哪一層的重送。Data Link Replay 由相鄰兩端保護同一次傳輸，接收端會避免重複交付；要求者重新產生一筆 CAS，則會再執行一次操作。兩者的區別見 <a href="/DOCS/pcie-course/chapter-8.html">Chapter 8</a>。</p>
<p>Completion Timeout（完成回覆逾時）是要求者等不到必要回覆時記錄的結果。即使沿用前面的 CAS，也有兩種不同時間線：Request 尚未到達目標；或目標已完成比較與交換，但 Completion 沒有被要求者收到。只有要求者的 Timeout，無法分辨這兩條時間線。</p>
<p>因此，原要求的結果尚未確認時，恢復程式不能把它直接當成「沒有執行」再送一次。應先保存原 Request、Requester ID／Tag、沿途 Trace 與錯誤資料，再依平台或裝置的同步與恢復協定決定後續動作。稍後讀到的記憶體值也可能經過其他處理器或裝置更新，不能替代遺失的 Completion。這是由回覆機制推得的分析邊界；Base 6.0 沒有提供通用的軟體重試演算法。</p>
<p>正常收到 SC 時，也要區分操作種類：CAS 回傳原值，供要求者判斷是否交換；Memory Read 若有多筆 Completion，則須收齊必要回覆才完成。§2.8 的逾時範圍用於偵測異常，不能拿來估計一般服務延遲。若後續 Request 必須等 AtomicOp 被完成端觀察到，§6.15.2 要求先等 AtomicOp Completion，再發出後續 Request。</p>
<p>本章的原子保證針對目標位置的操作。對支援 AtomicOp 的 Root Port，§6.15.3.1 另外要求：代辦主記憶體存取時，須與處理器或裝置對該範圍的存取維持原子性，並保留 CPU 原子操作的原子性。整個同步演算法、其他位置的資料發布順序，以及軟體使用的記憶體屬性，仍須搭配平台與 CPU 文件；不能只靠一次 CAS 推出全部條件都已滿足。</p>
<p class="source">規格閱讀：§2.8 Completion Timeout Mechanism，pp.259–260；§6.15.2，p.774；§6.15.3.1，p.775。Replay 與軟體重試的區別在此作跨章節應用，不重複展開其狀態機。</p>
<h3>Locked Transactions 是同一種原子機制嗎？</h3><p>Locked Transactions（鎖定交易）在 §6.5.1 有不同限制：只有 Root Complex 可發起，PCI Express Endpoint 不得支援鎖定存取，新軟體也不得使用會對 I/O 裝置產生鎖定存取的指令。它不能當成某個 AtomicOp 不支援時，任意改用的替代方案。</p></section>
<section id="sources"><h2>版本與來源</h2><p>本章以 PCI Express Base Specification Revision 6.0（6.0-1.0-PUB）為技術依據，文件印刷頁與 PDF 檢視器頁碼相同。圖與數值案例由作者依已標示的規則建立，並非規格原圖或實機量測。本輪集中帶讀 CAS 回覆與 DMWr 重試；完整 AtomicOp 格式、DMWr 能力和所有錯誤條件仍需後續深入。</p><details class="source-note"><summary>完整來源定位與用途</summary><ul>
<li>§2.3 Handling of Received TLPs，pp.204–206；Figure 2-81 Flowchart for Handling of Received TLPs，p.206：接收入口、Reserved 欄位與 Request／Completion 分流。</li>
<li>§2.3.1 Request Handling Rules，pp.208–213；Figure 2-83 Flowchart for Handling of Received Request，p.213：要求支援、可選 programming model 檢查與回覆。</li>
<li>§2.2.7.1 Non-Flit Mode，pp.162–163；Table 2-15 Length Field Values for AtomicOp Requests，p.162：運算值、Length、自然對齊及 CAS 目標範圍。</li>
<li>§2.2.9.1 Completion Rules for Non-Flit Mode，pp.196–198；Figure 2-73 Completion Header Format - Non-Flit Mode，p.196；Table 2-37 Completion Status Field Values，p.197：AtomicOp Byte Count、Reserved Lower Address、Requester ID／Tag 與狀態編碼。</li>
<li>§6.15 Atomic Operations (AtomicOps)，pp.772–773；§6.15.2 AtomicOp Transaction Protocol Summary，pp.774–775；§6.15.3.1 Root Ports with AtomicOp Completer Capabilities，p.775：操作語意、路徑、等待與主記憶體原子性。</li>
<li>§7.5.3.15 Device Capabilities 2 Register (Offset 24h)，Table 7-33，p.990；§7.5.3.16 Device Control 2 Register (Offset 28h)，Table 7-34，p.996：AtomicOp 支援、啟用與阻擋欄位的作用範圍及屬性。</li>
<li>§6.32 Deferrable Memory Write，pp.857–860：暫時 RRS、目標保持、啟用與要求者重送選擇。</li>
<li>§2.8 Completion Timeout Mechanism，pp.259–260：未收到完整回覆的範圍與服務延遲限制；§6.5.1 Introduction，p.718：Locked Transactions 的發起與支援限制。</li></ul></details></section>
</article>
<nav class="bottom-nav" aria-label="課程與語言版本"><a href="/DOCS/pcie-course/index.html">課程總覽</a><a href="/DOCS/pcie-course/chapter-15.html">繁中完整教學</a><a href="/pcie/chapter-15-en/">English</a></nav>
</div>
