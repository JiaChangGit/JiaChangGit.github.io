---
layout: post
title: "PCIe Chapter 14：從 TLP 標頭到 Flit 封包布局"
date: 2026-10-24 00:00:00 +0800
last_modified_at: 2026-10-28 00:00:00 +0800
permalink: /pcie/chapter-14-zh-tw/
categories: [PCIe]
tags: [PCIe, Specification]
lang: zh-TW
spec_teaching: true
spec_series: pcie
description: "用同一筆部分寫入需求比較 Non-Flit／Flit 完整 TLP，串連格式、OHC、資料起點與有效 bytes。"
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
<nav class="bottom-nav" aria-label="課程與語言版本"><a href="/DOCS/pcie-course/index.html">課程總覽</a><a href="/DOCS/pcie-course/chapter-14.html">繁中完整教學</a><a href="/pcie/chapter-14-en/">English</a></nav>
<article class="lesson">
<p>TLP（Transaction Layer Packet，交易層封包）把要求、回覆與訊息送過 PCIe。讀取封包前，先確認 Link 使用 Non-Flit Mode（非 Flit 模式）或 Flit Mode（固定傳輸單元模式）；兩者的 TLP（承載交易的封包）標頭布局不同。本章從這個分岔開始，把格式欄位接到位址、資料長度與有效 byte。</p><figure class="diagram"><svg viewBox="0 0 900 420" role="img" aria-labelledby="ch14-zh-t ch14-zh-d"><title id="ch14-zh-t">本章角色與事件</title><desc id="ch14-zh-d">先辨識模式，再定位標頭、附加欄位與資料。</desc><g data-walk-target="mode"><rect x="30" y="30" width="250" height="44" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="155.0" y="59" text-anchor="middle" font-size="16">先確認 Link 的模式</text></g><g data-walk-target="nfm"><rect x="30" y="175" width="350" height="68" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="205.0" y="204" text-anchor="middle" font-size="16">Non-Flit：Fmt ＋ Type</text><text x="205.0" y="228" text-anchor="middle" font-size="16">決定標頭長度與資料</text></g><g data-walk-target="fm"><rect x="500" y="175" width="360" height="68" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="680.0" y="204" text-anchor="middle" font-size="16">Flit：Type ＋ OHC ＋ TS</text><text x="680.0" y="228" text-anchor="middle" font-size="16">決定基本標頭、擴充與尾部</text></g><g data-walk-target="body"><rect x="245" y="335" width="410" height="44" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="450.0" y="364" text-anchor="middle" font-size="16">按欄位定義讀取位址、身分與資料</text></g><g data-walk-target="a"><path d="M155 74 L205 175" stroke="var(--accent)" stroke-width="2" fill="none"/><polygon points="205,175 196.08241815935642,168.25635602100587 205.0443660788092,163.81974814008865" fill="var(--accent)"/><text x="180.0" y="114.5" text-anchor="middle" font-size="16">Non-Flit</text></g><g data-walk-target="b"><path d="M280 60 L660 175" stroke="var(--accent)" stroke-width="2" fill="none"/><polygon points="660,175 648.9804081905046,176.88907288162778 651.8769866090005,167.31777028138032" fill="var(--accent)"/><text x="470.0" y="107.5" text-anchor="middle" font-size="16">Flit</text></g><g data-walk-target="c"><path d="M205 243 L350 335" stroke="var(--accent)" stroke-width="2" fill="none"/><polygon points="350,335 338.877476179746,333.864454374372 344.23492220835004,325.42065356842005" fill="var(--accent)"/><text x="277.5" y="279.0" text-anchor="middle" font-size="16">依格式</text></g><g data-walk-target="d"><path d="M680 243 L550 335" stroke="var(--accent)" stroke-width="2" fill="none"/><polygon points="550,335 555.2743678294779,325.1419553663331 561.0510564046202,333.30466748338216" fill="var(--accent)"/><text x="615.0" y="279.0" text-anchor="middle" font-size="16">依格式</text></g></svg><figcaption>作者依 Base 6.0 繪製的教學示意；省略與本章無關的交換。</figcaption></figure><dl class="st-terms" aria-label="本段名詞"><div><dt>OHC</dt><dd>Orthogonal Header Content，Flit模式的擴充標頭內容</dd></div></dl><section id="format"><h2>為什麼不能只背一張標頭圖？</h2><p>在非 Flit 格式，先用 Figure 2-4 找 byte 0 的 Fmt／Type，再對 Table 2-2、Table 2-3。以 Memory Read 為例，Fmt 可表示 32-bit 或 64-bit 位址布局，要求不帶資料；Memory Write 則帶寫入資料。Type 也會影響路由，因此只看 Length 還不足以找到下一個封包。例如，另一筆 Non-Flit、32-bit 位址的 Memory Read 即使 Length=2，在沒有 Prefix 與 Digest 時，Request 本身仍只有 12 bytes Header，讀取資料由後續 Completion 返回。先確認這個 Type 是否帶資料，再使用 Length 計算封包大小。</p><p>換成 Flit 格式時，從 Figure 2-6 與 Table 2-5 重新開始。Type 不再只是舊格式的五個 bits；例如 Table 2-5 的 NOP 是 00h，而 32-bit 位址 Memory Read 是 03h。若沿用非 Flit 的解碼表，第一步就會讀錯。</p></section>
<section id="extensions"><h2>找到基本標頭後，怎麼走到資料？</h2><p>OHC（用來補充標頭資訊的擴充內容）由 Figure 2-6 的 OHC 欄位指出。接著讀 p.131 的出現順序，再用 Table 2-6 選擇適用的 A 類布局。例如有明確 Byte Enables 的 Memory Request，要沿 Table 2-6 找到 Figure 2-7 的 OHC-A1。後面的完整案例會把它接到實際的資料起點。不要固定假設所有 Flit 標頭都是相同長度。</p><dl class="st-terms" aria-label="本段名詞"><div><dt>OHC</dt><dd>Orthogonal Header Content，Flit模式的擴充標頭內容</dd></div></dl><p>TS 是 Trailer Size，用來指出尾部大小與用途；它與 Length 的資料長度分開計算。非 Flit 格式另有 Prefix（標頭前的擴充內容）與 TD（TLP Digest 存在標記）。判讀工具應先完成整個格式的大小計算，再移到後一包。</p></section>
<section id="packet-layout"><h2>用同一個寫入需求，走完兩種格式</h2>
<div class="example"><p><strong>【模擬資料】以下資料為教學用途建立，不代表特定硬體或平台。</strong>兩段獨立 Trace 都由已配置的 Endpoint 03:00.0 發出 Memory Write，目標位址為 <code>0x80001000</code>。本例假設位址與路徑可用、允許裝置發起存取，且沒有 Prefix、IDE 或 TPH；保留欄位及其他未使用欄位填 0。兩段 Trace 的 Link 模式已由外部資訊確認，並已取得完整的邏輯 TLP。</p><dl class="st-terms" aria-label="本段名詞"><div><dt>IDE</dt><dd>Integrity and Data Encryption，完整性與資料加密</dd></div><div><dt>TPH</dt><dd>TLP Processing Hints，封包處理提示</dd></div></dl>
<p>兩筆資料負載相同，都是 <code>A0 A1 A2 A3 B0 B1 B2 B3</code>，Length=2 DW（每個 DW 是 4 bytes）；但只要寫入中間四個 bytes。First DW BE=<code>1100b</code>，Last DW BE=<code>0011b</code>。Flit 案例從已重組的 TLP 開始，沒有把完整 FLIT 當作一筆 TLP。下列十六進位依圖中的 byte 0、byte 1 順序排列，每四個 bytes 換行；它不是 CPU 端的 DWORD 讀值表。</p><dl class="st-terms" aria-label="本段名詞"><div><dt>DW</dt><dd>Double Word，4 bytes的資料單位</dd></div></dl>
<h3>先讀 Non-Flit 的 20 bytes</h3>
<pre><code style="font-size: 1rem">40 00 00 02
03 00 00 3C
80 00 10 00
A0 A1 A2 A3
B0 B1 B2 B3</code></pre>
<p>先用 Figure 2-4 讀第一個 byte：<code>0x40</code> 的 Fmt=<code>010b</code>、Type=<code>00000b</code>。查 Tables 2-2／2-3 的組合，得到帶資料、使用 3 DW Header 的 Memory Write。再用 Figure 2-5 讀 Length=2、TD=0；因此本例有 12 bytes Header、8 bytes Data Payload，沒有 Digest，合計 <strong>20 bytes</strong>。</p>
<p>接著換到 Figure 2-31。byte 4–5 的 <code>03 00</code> 是 Requester ID=<code>0x0300</code>，本例對應 03:00.0；byte 8–11 提供地址，得到 <code>0x80001000</code>。最後到 Figure 2-26／Table 2-10，讀 Header byte 7=<code>0x3C</code>：高四位是 Last DW BE=<code>0011b</code>，低四位是 First DW BE=<code>1100b</code>。Header 在 byte 11 結束，資料從 <strong>byte 12</strong> 開始。</p>
<h3>再讀 Flit 格式的 24 bytes</h3>
<pre><code style="font-size: 1rem">40 01 00 02
03 00 00 00
80 00 10 00
00 00 00 3C
A0 A1 A2 A3
B0 B1 B2 B3</code></pre>
<p>這次先讀 Figure 2-6，第一個 byte 的整個 <code>0x40</code> 都是 Type。查 Table 2-5 編號 64 的項目，得到 32-bit address Memory Write、Header Base=3 DW，Data Payload 由 Length 決定。這筆 Type 恰好與前例的第一個 byte 相同，不能用它單獨辨識 Link 模式。</p>
<p>byte 1 的 OHC=<code>00001b</code> 表示有 OHC-A；byte 2 的 TS=<code>000b</code> 表示沒有 Trailer，Length 仍為 2。先用 Figure 2-40 讀完 12 bytes Header Base，再依 Table 2-6 的 Memory Request 選到 OHC-A1。Figure 2-7 顯示這個擴充占 1 DW；其內部 byte 3 才是兩組 BE。換成整筆 TLP 的位置，就是 byte 12+3=<strong>byte 15</strong>，讀到 <code>0x3C</code>。</p>
<p>所以這筆的 Data Payload 從 <strong>byte 16</strong> 開始，總長度為 12+4+8=<strong>24 bytes</strong>。本例 OHC-A1 的 PV=0，沒有有效的 PASID；其餘不使用欄位為 0。OHC-A1 在這裡用來提供部分寫入所需的 BE，沒有增加資料負載的長度。</p><dl class="st-terms" aria-label="本段名詞"><div><dt>PASID</dt><dd>Process Address Space ID，程序位址空間識別碼</dd></div></dl>
<figure class="diagram"><svg viewBox="0 0 820 370" style="min-width: 640px" role="img" aria-labelledby="packet-layout-title packet-layout-desc"><title id="packet-layout-title">相同的部分寫入需求，在兩種格式中的資料起點不同</title><desc id="packet-layout-desc">兩個案例的基本部分都是三個DW，並承載八個資料bytes。Non-Flit 的有效byte選擇放在Header內，資料從byte12開始；Flit多加一個DW的OHC-A1，因此資料從byte16開始。兩個邏輯TLP分別為20及24bytes。</desc><text x="20" y="63" font-size="18">Non-Flit</text><text x="20" y="238" font-size="18">Flit</text><rect x="130" y="35" width="330" height="72" rx="8" fill="var(--surface-alt)" stroke="var(--line)" stroke-width="1"/><text x="295.0" y="64" text-anchor="middle" font-size="18">Header</text><text x="295.0" y="90" text-anchor="middle" font-size="18">3 DW = 12 bytes</text><rect x="460" y="35" width="220" height="72" rx="8" fill="var(--blue-soft)" stroke="var(--accent)" stroke-width="2"/><text x="570.0" y="64" text-anchor="middle" font-size="18">Data Payload</text><text x="570.0" y="90" text-anchor="middle" font-size="18">2 DW = 8 bytes</text><rect x="130" y="210" width="330" height="72" rx="8" fill="var(--surface-alt)" stroke="var(--line)" stroke-width="1"/><text x="295.0" y="239" text-anchor="middle" font-size="18">Header Base</text><text x="295.0" y="265" text-anchor="middle" font-size="18">3 DW = 12 bytes</text><rect x="460" y="210" width="110" height="72" rx="8" fill="var(--blue-soft)" stroke="var(--accent)" stroke-width="2"/><text x="515.0" y="239" text-anchor="middle" font-size="18">OHC-A1</text><text x="515.0" y="265" text-anchor="middle" font-size="18">1 DW</text><rect x="570" y="210" width="220" height="72" rx="8" fill="var(--blue-soft)" stroke="var(--accent)" stroke-width="2"/><text x="680.0" y="239" text-anchor="middle" font-size="18">Data Payload</text><text x="680.0" y="265" text-anchor="middle" font-size="18">2 DW = 8 bytes</text><text x="130" y="133" text-anchor="middle" font-size="17">0</text><text x="460" y="133" text-anchor="middle" font-size="17">12</text><text x="680" y="133" text-anchor="middle" font-size="17">20</text><text x="130" y="308" text-anchor="middle" font-size="17">0</text><text x="460" y="308" text-anchor="middle" font-size="17">12</text><text x="570" y="308" text-anchor="middle" font-size="17">16</text><text x="790" y="308" text-anchor="middle" font-size="17">24</text><path d="M130 114 H680 M130 289 H790" stroke="var(--line)"/><text x="295" y="163" text-anchor="middle" font-size="17">BE 位於 Header byte 7</text><text x="460" y="344" text-anchor="middle" font-size="17">BE 位於 OHC-A1 byte 3，也就是 TLP byte 15</text></svg><figcaption>作者依兩筆模擬 TLP 繪製。數字是各自從起點算起的 byte offset，最右側數字是總長度；兩列都未計入 Data Link 與 Physical Layer 的封裝。</figcaption></figure>
</div>
<p>現在回到 §2.2.5.2 看這個擴充為何不能省：對這筆 2 DW Memory Request，若沒有 OHC-A1，接收端會把 First 與 Last DW BE 都視為 <code>1111b</code>。這會變成八個 bytes 全部啟用，已經改變原本只寫中間四個 bytes 的需求。OHC 是否存在，會直接影響接收端如何執行存取。</p>
<p>如果工具把第二段 Trace 當成 Non-Flit，就可能把 byte 7 的 <code>0x00</code> 誤讀成兩組 BE，並把 OHC 的 <code>00 00 00 3C</code> 當成資料起點，讓整段 payload 錯位四個 bytes。本例應先修正工具的解碼模式；這些假象不能直接當作線路上真的出現了錯誤封包。</p>
<details class="source-note"><summary>每一步查哪張圖表？</summary><p>PCI Express Base Specification Revision 6.0：Figure 2-4 <em>Fields Present in All TLPs</em>（PDF／印刷 p.119）→ Figure 2-5 <em>Fields Present in All Non-Flit Mode TLP Headers</em>、Table 2-2 <em>Fmt[2:0] Field Values</em>／Table 2-3 <em>Fmt[2:0] and Type[4:0] Field Encodings</em>（pp.120–121）→ Figure 2-31 <em>Request Header Format for 32-bit Addressing of Memory</em>（p.163）→ Figure 2-26／Table 2-10 <em>Byte Enables Location and Correspondence</em>（pp.150–151），完成 Non-Flit 判讀。Flit 改由 Figure 2-6 <em>First DW of Header Base</em>（p.122）→ Table 2-5 <em>Flit Mode TLP Header Type Encodings</em> 的編號 64（Type=40h）項目（p.125）→ §2.2.1.2 的 TS／OHC 規則、Table 2-6 <em>OHC-A Included Fields for OHC-A1 through OHC-A5</em>（pp.130–132）→ Figure 2-40 <em>Flit Mode Mem32 Request</em>（p.169）與 Figure 2-7 <em>OHC-A1</em>（p.132）。§2.2.5.2 <em>Byte Enable Rules for Flit Mode</em>（p.152）定義未帶 OHC-A1 時的預設 BE。上述 PDF 與印刷頁碼相同；閱讀順序是查詢路線，不代表硬體執行圖表的先後。</p></details>
</section>
<section id="bytes"><h2>八個 payload bytes，為什麼只寫入四個？</h2>
<p>沿用上面的兩筆模擬資料。§2.2.5.1 與 Table 2-10 把每個 BE bit 對應到資料 byte：First DW BE 的 bit 0 對應第一個 DW 的最低位址 byte；Last DW BE 的 bit 0 則對應最後一個 DW 的最低位址 byte。<code>1100b</code> 選到第一個 DW 的 +2、+3；<code>0011b</code> 選到最後一個 DW 的 +4、+5。</p>
<div class="table-wrap"><table><caption>兩種格式送出相同資料，也選到相同的記憶體 bytes</caption><thead><tr><th scope="col">資料內的 offset</th><th scope="col">對應位址</th><th scope="col">Payload 內容</th><th scope="col">依本例 BE 執行的寫入</th></tr></thead><tbody><tr><td>+0、+1</td><td>0x80001000–0x80001001</td><td>A0、A1</td><td>不寫入這兩個 bytes。</td></tr><tr><td>+2、+3</td><td>0x80001002–0x80001003</td><td>A2、A3</td><td>寫入 A2、A3。</td></tr><tr><td>+4、+5</td><td>0x80001004–0x80001005</td><td>B0、B1</td><td>寫入 B0、B1。</td></tr><tr><td>+6、+7</td><td>0x80001006–0x80001007</td><td>B2、B3</td><td>不寫入這兩個 bytes。</td></tr></tbody></table></div>
<p>因此被選取的位址範圍是 <code>0x80001002–0x80001005</code>，共四個 bytes，但兩筆 TLP 的 Data Payload 都仍有八個 bytes。Length 維持 2 DW，接收端不會因為部分 bytes 沒被選中，就把它們從封包裡刪掉。本例也未跨越 4-KB 邊界，BE 選取的資料連續；其他長度、對齊或非連續組合，須再依 §2.2.5.1 檢查。</p>
<p>在本例的 Non-Flit 格式中，若改成 1 DW Request，Last DW BE 必須為 <code>0000b</code>；不能把本例的 <code>0011b</code> 直接沿用。這項規則接在 Figure 2-26 後，圖中的位置與周圍文字要一起讀。</p>
</section>
<section id="digest-check"><h2>TD 為 1，能確認接收端檢查過 ECRC 嗎？</h2><dl class="st-terms" aria-label="本段名詞"><div><dt>ECRC</dt><dd>End-to-End CRC，端到端循環冗餘檢查</dd></div></dl>
<p>只能先確認非 Flit 格式的 TLP 宣告帶有 Digest（尾端檢查欄位），還要檢查接收端能力與設定，才能判斷是否執行 ECRC（End-to-End CRC，端到端循環冗餘檢查）。沿用前面的 Non-Flit Memory Write：Header 為 12 bytes、Payload 為 8 bytes；若另設 TD=1，且沒有 Prefix，末尾的 Digest 再占 4 bytes，邏輯 TLP 共 24 bytes。這是作者依格式建立的模擬情境。</p>
<p>先查 Figure 2-5 的 TD 與 Length：Length 描述 Payload 大小，Digest 不計入其中。接著讀 §2.2.3：TD 與實際 TLP 長度若不相符，屬於 Malformed TLP，錯誤與接收 Port 關聯。若接收端不支援 ECRC 檢查，規則要求忽略 Digest；轉送 Multicast TLP 且出口啟用 MC_Overlay 的中間接收端有另列例外，須查 §6.14.5。支援檢查時，繼續查 §2.7.1 的使用條件。</p>
<p>不要把 TD=1 當成「檢查成功」的紀錄，也不要把 §2.2.3 的 Non-Flit TD 格式直接套到 Flit Mode。是否啟用與錯誤記錄，還需檢查實際接收元件及其 AER 設定。</p><dl class="st-terms" aria-label="本段名詞"><div><dt>AER</dt><dd>Advanced Error Reporting，進階錯誤回報</dd></div></dl><p class="source-note">Base 6.0 §2.2.1.1、Figure 2-5（PDF／印刷 p.120）；§2.2.2–§2.2.3 <em>TLP Digest Rules - Non-Flit Mode Only</em>（pp.142、144）；§2.7.1 與 §6.14.5 提供後續條件。</p></section>
<section id="mps-limits"><h2>同一個裝置的傳送與接收上限一定相同嗎？</h2>
<p>不一定。MPS（Maximum Payload Size，TLP 資料負載大小上限）要分別從傳送 Function 與接收 Function 判斷。先查 Device Capabilities 的 <code>Max_Payload_Size Supported</code>、<code>Rx_MPS_Fixed</code>、<code>Mixed_MPS_Supported</code>，再查 Device Control 的 <code>Max_Payload_Size</code> 設定，最後回到 §2.2.2 判斷各欄位適用的條件。</p>
<p>傳送端先算 <code>Tx_MPS_Limit</code>：單 Function 裝置使用該 Function 的設定；ARI（Alternative Routing-ID Interpretation，替代的 Function 識別方式）裝置使用 Function 0 的設定。非 ARI 多 Function 裝置各 Function 設定一致時使用共同值；不一致時使用由實作選定的 Function 的值。軟體不宜在不了解實作時設定不同值。</p>
<p>若 <code>Mixed_MPS_Supported=1</code>，裝置有依目的地選擇 MPS 的實作機制，選定值可以高於或低於 Tx_MPS_Limit，但不得超過該 Function 宣告的 Supported 值；目標是 host memory 時仍使用 Tx_MPS_Limit。該機制如何為個別目的地選值，還要查實作資料。</p>
<p>接收端則先查 <code>Rx_MPS_Fixed</code>：為 1 時，<code>Rx_MPS_Limit</code> 使用該接收 Function 的 Supported 值；為 0 時，依 §2.2.2 的單 Function、ARI 或適用的非 ARI 多 Function 規則查設定。接收端必須檢查超過自身 Rx_MPS_Limit 的帶資料 TLP；若發現違規，按 Malformed TLP 處理，錯誤與接收 Port 關聯。</p>
<div class="example"><p><strong>【模擬資料】以下資料為教學用途建立，不代表特定硬體或平台。</strong>一個 ARI 多 Function 裝置有 Function 0 與 Function 1；假設 Function 0 的 MPS 設定為 128 bytes、Function 1 為 256 bytes，Function 1 的 Supported 為 512 bytes，且 Rx_MPS_Fixed=1。Function 1 傳送至 host memory 時，Tx_MPS_Limit 使用 Function 0 的 128 bytes；Function 1 接收帶資料 TLP 時，Rx_MPS_Limit 則為 512 bytes。兩個結果分別約束不同方向，實際傳送仍須符合路徑與目標條件。</p></div>
<p>MPS 限制的是 TLP 攜帶的 Data Payload；Memory Read Request 本身不帶所要求的資料，其 Length 不是以 MPS 設定限制。讀取要求大小還要另查 Maximum Read Request Size 等適用規則。對支援 Flit Mode 的實作，Table 7-20 還要求 Supported 至少為 512 bytes，且 Rx_MPS_Fixed 必須為 1；不能把這個要求誤寫成每個 Non-Flit 裝置都相同。</p>
<details class="source-note"><summary>從欄位接到傳送與接收規則</summary><p>PCI Express Base Specification Revision 6.0：§2.2.2 <em>TLPs with Data Payloads - Rules</em>（PDF／印刷 pp.141–142）；§7.5.3.3 Figure 7-24／Table 7-20 <em>Device Capabilities Register</em>（pp.955、958）；§7.5.3.4 Figure 7-25／Table 7-21 <em>Device Control Register</em>（pp.959–960）。先在 Figure 找欄位，再讀 Table 中的能力和模式條件，最後依 §2.2.2 選用對應 Function 與方向。</p></details></section>
<section id="byte-enable-rules"><h2>看到不連續的 Byte Enable，就一定是錯誤嗎？</h2><p>先沿用前面的 Memory Write，改變 Length、位址對齊與 BE，依 §2.2.5.1 比較。下表是模擬的 Non-Flit Mode Request；是否允許不連續，必須連同長度與對齊一起看。</p><p>手機閱讀時，可左右滑動表格查看完整內容。</p><div class="table-wrap"><table><thead><tr><th scope="col">條件</th><th scope="col">First／Last DW BE</th><th scope="col">規格判讀</th></tr></thead><tbody><tr><td>1 DW Request</td><td>1010b／0000b</td><td>第一個 DW 可以不連續；1 DW 的 Last 必須為 0000b。</td></tr><tr><td>2 DW Memory Request，起點為 8-byte 對齊</td><td>1010b／0101b</td><td>這種 QW 對齊的 2 DW Memory Request，兩個 BE 都允許不連續。</td></tr><tr><td>2 DW Memory Request，起點為 4-byte 但非 8-byte 對齊</td><td>1010b／0101b</td><td>不符合此長度與對齊條件下的連續性規則。</td></tr></tbody></table></div><p>Figure 2-26 只告訴我們 Non-Flit Mode 中欄位的位置；Table 2-10 把各 bit 對回資料 byte。再讀附近文字，才能判斷上述組合是否允許。Receiver 可以選擇檢查各項 BE 規則；若已實作的檢查發現違規，該 TLP 是 Malformed TLP。不能因沒有看到錯誤紀錄，就反推 BE 一定合法。</p><p>切換到 Flit Mode 時，先查 §2.2.5.2：Memory Request 若沒有 OHC-A1，First DW BE 預設視為 1111b；Length 至少 2 DW 時，Last DW BE 也視為 1111b。若需要其他 BE 值，須帶 OHC-A1。I/O 和 Configuration Request 分別有自己的 OHC 要求，不能把 Memory Request 的省略條件直接套用。</p><p class="source-note">Base 6.0 §§2.2.5.1–2.2.5.2，Figure 2-26、Table 2-10，pp.149–152；QW 表示 8 bytes。</p></section>
<section id="th-byte-enable"><h2>同一個 Header 位元組，什麼時候不再是 Byte Enable？</h2><p>接續 Figure 2-26。Non-Flit Mode 的 Memory Read 或 Deferrable Memory Write（DMWr，可延後處理的記憶體寫入）若 TH=1，原本放 First／Last DW BE 的位置改用來承載 Steering Tag 的 ST[7:0]。此時不能把那個位元組直接拆成兩個 BE。</p><p>【模擬資料】一筆符合適用條件的 Memory Read，TH=1 且 Length=1 DW：First DW BE 的隱含值是 1111b、Last DW BE 是 0000b。若 Length 大於 1 DW，兩者的隱含值都是 1111b。規格只允許在可接受把要求視為所有請求 bytes 都啟用時設定 TH；帶讀取副作用的 Non-Prefetchable 區域還要留意 §2.2.5.1 的實作說明。</p><p>這個例子只處理 Non-Flit Mode 的欄位重用。若 Trace 是 Flit Mode，應回到該模式的 Header 與 OHC 規則，不要把 Figure 2-26 的位元組位置直接套用。</p><p class="source-note">Base 6.0 §2.2.5.1、Figure 2-26，pp.149–150；TH／Steering Tag 的適用要求另讀 §2.2.7.1.1。</p></section>
<section id="zero-length-read"><h2>沒有啟用任何 Byte，為什麼 Read 還會收到資料？</h2><p>【模擬資料】一筆 Non-Flit Mode Memory Read 的 Length=1 DW、First DW BE=0000b、Last DW BE=0000b。§2.2.5.1 規定，這類 Read 對應的 Completion 必須有 1 DW 長度及 1 DW Data Payload；其內容未指定，不能把回傳值當成讀到的裝置資料。</p><p>規格的 zero-length Read（零長度讀取）實作說明還提供一種用途：Requester 可用它確認先前 Posted Write 已完成到 PCIe 目的地。要讓這個用途在各情況下有效，Read 要指向與那些 Write 相同的裝置；規格建議可使用其中一筆 Write 的相同位址，且此作用只涵蓋與 Read 同一個 Traffic Class 的流量。這不等於確認應用資料已保存到非揮發媒體。</p><p>例如先發一筆 TC0 的 Posted Write，再對同一裝置發 TC0 的零長度 Read，接著觀察其正常 Completion；這時才有依規格判讀先前 Write 到達 PCIe 目的地的依據。若 Write 是 TC1，不能只靠這筆 TC0 Read 推論它已完成。也要保留完整路徑和 Attribute 等條件，不能只因送出 Read 就當作已收到回覆。</p><p class="source-note">Base 6.0 §2.2.5.1，zero-length Write／Read 與實作說明，pp.151–152；Ordering 的詳細條件另讀 §2.4。</p></section>
<section id="next"><h2>封包有回覆時，從哪裡接著讀？</h2><p>先按 §2.2.9 確認這類要求需要 Completion（完成回覆）。Memory Read 的資料隨完成回覆返回；一般 Posted Memory Write 沒有對應的成功完成回覆。接下來到 <a href="/DOCS/pcie-course/chapter-15.html">Chapter 15</a>，沿接收端的處理流程，確認合法性、能力與回覆結果。</p></section>
<section id="sources"><h2>版本與來源</h2><p>本章以 PCI Express Base Specification Revision 6.0（6.0-1.0-PUB）為準，文件頁與 PDF 頁相同。案例的配置與讀值均為作者假設，並非實機測量。</p><details class="source-note"><summary>完整來源定位</summary><ul><li>§2.2.1.1; §2.2.1.2; pp.119,120,121,122,123; Figures 2-4, 2-5, 2-6; Tables 2-2, 2-3, 2-4, 2-5</li><li>§2.2.1.2; pp.130,131,132; Figures 2-7; Tables 2-6</li><li>§2.2.5.1; pp.149,150; Figures 2-26</li><li>§2.2.9; pp.195</li></ul></details></section>
</article>
<nav class="bottom-nav" aria-label="課程與語言版本"><a href="/DOCS/pcie-course/index.html">課程總覽</a><a href="/DOCS/pcie-course/chapter-14.html">繁中完整教學</a><a href="/pcie/chapter-14-en/">English</a></nav>
</div>
