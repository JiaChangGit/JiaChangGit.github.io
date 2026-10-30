---
layout: post
title: "PCIe Chapter 36：交易依賴、ID-Based Ordering 與 Message"
date: 2026-10-24 00:00:00 +0800
last_modified_at: 2026-10-29 00:00:00 +0800
permalink: /pcie/chapter-36-zh-tw/
categories: [PCIe]
tags: [PCIe, Specification]
lang: zh-TW
spec_teaching: true
spec_series: pcie
description: "先送資料、再送通知，讀者要確認哪些排序條件？"
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
<nav class="bottom-nav" aria-label="課程與語言版本"><a href="/DOCS/pcie-course/index.html">課程總覽</a><a href="/DOCS/pcie-course/chapter-36.html">繁中完整教學</a><a href="/pcie/chapter-36-en/">English</a></nav>
<article class="lesson">
<p>交易排序要先確認TC（Traffic Class，流量類別）、要求種類與屬性，再讀允許超越的規則。RO（Relaxed Ordering，放寬排序）與IDO（ID-Based Ordering，依身分放寬排序）都可能影響先後，但不能取代軟體原本需要的資料依賴。</p><figure class="diagram"><svg viewBox="0 0 900 420" role="img" aria-labelledby="ch36-zh-t ch36-zh-d"><title id="ch36-zh-t">本章角色與事件</title><desc id="ch36-zh-d">先建立資料與通知的依賴，再核對同TC內允許超越的條件。</desc><g data-walk-target="data"><rect x="30" y="45" width="320" height="44" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="190.0" y="74" text-anchor="middle" font-size="16">產生者：寫入資料</text></g><g data-walk-target="flag"><rect x="535" y="45" width="330" height="44" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="700.0" y="74" text-anchor="middle" font-size="16">產生者：送出通知</text></g><g data-walk-target="consumer"><rect x="535" y="300" width="330" height="44" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="700.0" y="329" text-anchor="middle" font-size="16">消費者：收到通知後讀資料</text></g><g data-walk-target="rules"><rect x="30" y="300" width="320" height="44" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="190.0" y="329" text-anchor="middle" font-size="16">同 TC、來源、屬性與路徑</text></g><g data-walk-target="a"><path d="M350 79 L535 79" stroke="var(--accent)" stroke-width="2" fill="none"/><polygon points="535,79 525.0,84.0 525.0,74.0" fill="var(--accent)"/><text x="442.5" y="69.0" text-anchor="middle" font-size="16">程式所需先後</text></g><g data-walk-target="b"><path d="M700 113 L700 300" stroke="var(--accent)" stroke-width="2" fill="none"/><polygon points="700,300 695.0,290.0 705.0,290.0" fill="var(--accent)"/><text x="700.0" y="196.5" text-anchor="middle" font-size="16">通知可見</text></g><g data-walk-target="c"><path d="M535 334 L350 334" stroke="var(--accent)" stroke-width="2" fill="none"/><polygon points="350,334 360.0,329.0 360.0,339.0" fill="var(--accent)"/><text x="442.5" y="324.0" text-anchor="middle" font-size="16">核對相依條件</text></g></svg><figcaption>作者依 Base 6.0 繪製的教學示意；省略與本章無關的交換。</figcaption></figure><dl class="st-terms" aria-label="本段名詞"><div><dt>TC</dt><dd>Traffic Class，流量類別</dd></div></dl><section id="table"><h2>Table 2-42 的 Yes，為什麼容易讀反？</h2><p>先固定觀察方向：Column是先發送的交易，Row是後發送的交易，表格問的是後者能否超越前者。接著到pp.223–224讀格子的條件，尤其a／b兩種情況；只看一個No或Yes會漏掉屬性例外。</p><p><strong>作者案例：</strong>同一要求者、同TC，一般Posted資料寫入之後接Posted通知寫入，沒有適用放寬條件。按A2a，後者不得超越前者。這只說明該排序關係；資料是否已持久保存，或CPU需要何種記憶體屏障，仍要按相應裝置與平台規則處理。</p></section>
<section id="ordering-walk"><h2>兩筆交易相遇時，怎麼查排序表？</h2><p><strong>教學假設：</strong>以下每列都是獨立情境；兩筆交易使用同一個 Traffic Class（TC，流量類別），並在同一個轉送位置比較。先把較早發出的交易放在 Table 2-42 的欄，再把較晚發出的交易放在列，最後讀表格下方的對應條文。</p><p>手機閱讀時，可左右滑動表格查看完整內容。</p><div class="table-wrap"><table><thead><tr><th>先發出的交易：欄</th><th>後發出的交易：列</th><th>查哪一格</th><th>這次的判讀</th></tr></thead><tbody><tr><td>Posted Memory Write</td><td>同一 Requester 的 Posted Memory Write，RO=0、IDO=0</td><td>A2a</td><td>後一筆不得超越前一筆。</td></tr><tr><td>Posted Memory Write</td><td>不同 Requester 的 Memory Read，IDO=1</td><td>B2b</td><td>符合身分條件時，後一筆<strong>可以</strong>超越；是否真的超越仍取決於實作與當時流量。</td></tr><tr><td>Non-Posted Memory Read</td><td>Posted Memory Write</td><td>A3</td><td>轉送元件必須允許後一筆超越；發生阻塞時需要能夠超越，以避免死結。</td></tr></tbody></table></div><p>表中 RO 是 Relaxed Ordering（放寬排序），IDO 是 ID-Based Ordering（依身分放寬排序）。例如第二列看的是<strong>後發 Read 的 IDO</strong>，再比較兩筆 Requester ID；FLIT Mode 還要連同 Requester Segment 一起比較。不是只要某處 Enable 為 1，就能代替檢查實際 TLP 的屬性。</p><dl class="st-terms" aria-label="本段名詞"><div><dt>TLP</dt><dd>Transaction Layer Packet，交易層封包</dd></div></dl><p>Table 2-42 適用同一 TC；Flow-Through IDE Stream 有不同排序要求，須另讀 §6.33.4。規格允許超越也不保證一定會發生；應用程式的資料可見性與同步仍需平台及裝置文件共同確認。</p><dl class="st-terms" aria-label="本段名詞"><div><dt>IDE</dt><dd>Integrity and Data Encryption，完整性與資料加密</dd></div></dl></section>
<section id="no-snoop"><h2>No Snoop 與交易排序有什麼關係？</h2>
<p>No Snoop 是交易層封包的快取一致性屬性。先讀 Base 6.0 §2.2.6.5 的 Table 2-13：值為 0 時，預期由硬體維持快取一致性；值為 1 時，則不預期硬體提供這項一致性。這個屬性本身不改變 Transaction 的排序。要判斷兩筆交易能否互相超越，仍須回到本章的 Ordering Rules Table，檢查適用的 Traffic Class、交易種類與其他屬性。</p>
<p>接著讀 Device Control Register 的 Enable No Snoop：控制位為 1，表示 Function 在符合條件時獲准將自己發起的交易設為 No Snoop=1，並不表示每筆交易都會如此設定。即使控制位為 1，Function 也只有在能保證該交易位址不在系統任何快取中時，才可設定此屬性。控制位可以固定為 0，預設值則為 1。控制位的讀值和某一筆封包的實際屬性，要分別確認。</p>
<p><strong>【模擬資料】</strong>某 Function 的 Enable No Snoop=1，觀察到一筆 Memory Write 的 No Snoop=0。這兩個值可以同時成立：控制位允許在符合條件時使用 No Snoop，但這筆封包仍選擇預設一致性處理。若改看到 No Snoop=1，還需要平台與軟體的記憶體管理資訊，才能確認該位址是否符合使用條件；不能只憑這個 bit 宣稱應用程式一定讀到最新資料。</p>
<p>Configuration Request、I/O Request、作為 Message Signaled Interrupt（訊息式中斷）的 Memory Request，以及 Message Request（規格特別允許者除外），都必須將 No Snoop 清為 0。這些類型限制要和控制位一起檢查。</p>
<p class="source-note">PCI Express Base 6.0 §2.2.6.5、Table 2-13，文件頁／PDF 頁 161；§7.5.3.4、Figure 7-25、Table 7-21，文件頁／PDF 頁 959–961。平台快取與軟體同步行為需查相應平台文件。</p></section>
<section id="ido"><h2>想開 IDO 提升效能，要先看哪種案例？</h2><p>先用Figure E-1放回拓樸，再看Appendix E的單一對象與多對象通訊。只與一個對象直接通訊，和同時透過主記憶體及P2P協作，風險不同。E.4.1示範兩個裝置都更新同一記憶體位置時，放寬後可能改變最後結果。</p><p>Appendix D則從資源依賴切入，描述收到一種交易卻必須等另一種交易送出時，如何形成等待關係。它沒有替所有平台訂完跨TC依賴規則，系統仍須在配置TC／VC時理解自身限制。</p><dl class="st-terms" aria-label="本段名詞"><div><dt>VC</dt><dd>Virtual Channel，虛擬通道</dd></div></dl></section>
<section id="ido-path"><h2>不同 Requester 的交易可以超越，就一定安全嗎？</h2><p><strong>教學情境，依 Appendix E.4.1：</strong>Device Y 先對主記憶體寫入資料，接著以 Peer-to-Peer（P2P，裝置對裝置）寫入通知 Device Z；Z 收到通知後，向同一記憶體位置寫入自己的資料。</p><p>依 Figure E-1 先找 Y、Z、Switch 與 Root Complex，再把三筆交易依觀察位置排好。假設 Y 和 Z 寫入使用同一 TC，並在 Root Complex 的共同處理位置比較。前兩筆來自 Y；Z 後來的寫入則有另一個 Requester ID。若 Z 的 Posted Write 設置 IDO，且 Table 2-42 A2b 的其他適用條件成立，Root Complex 可能讓它超越仍在等待的 Y 寫入，最後的記憶體內容便可能改變。</p><p>這個案例說明：用 Requester ID 區分交易流，無法單獨描述跨裝置的資料依賴。是否可以啟用 IDO，要先理解哪些裝置和記憶體共同參與，再依各 TLP、路徑與同步方式判斷。附錄提出同步的可能方向，具體協定仍由裝置與平台定義。</p><dl class="st-terms" aria-label="本段名詞"><div><dt>TLP</dt><dd>Transaction Layer Packet，交易層封包</dd></div></dl><p>Appendix D 處理另一種問題：不同 TC 的封包若在有限緩衝資源之間形成循環等待，可能造成死結。它討論的是資源依賴；不要把不同 TC 缺少一般排序要求，理解成系統永遠不會產生依賴。</p></section>
<section id="stop"><h2>要改 Bus Number，先清 Bus Master Enable 就夠嗎？</h2><p>§6.4把停止流程分成多項責任：阻止裝置新要求、阻止軟體新存取、確認裝置服務中的要求完成、確認已發出的Non-Posted要求完成，以及確認Posted要求已到目的地。Transactions Pending只涵蓋其中一部分。</p><p>因此，先與驅動協調停止使用，再按要求種類確認在途工作。更改身分時仍有Request／Completion在途，可能讓原有識別失效；不能把一個控制位已清零當成所有交易都已排空。</p></section>
<section id="stop-path"><h2>準備改 Bus Number 時，要確認哪些工作已停下來？</h2><p><strong>教學情境：</strong>驅動程式準備重新配置一個 Endpoint。先依 §6.4 與驅動協調，阻止裝置產生新 Request，也停止軟體送往裝置的新 Request，並確認裝置正在服務的要求已完成。</p><p>接著看 Device Status 的 Transactions Pending：它用於判斷該 Function 已發出的 Non-Posted Request 是否完成；這個欄位本身不代表先前的 Posted Write 都已到達。仍須依交易使用的 TC、排序屬性與裝置同步機制，確認 Posted Request 的目的地已收到相應工作。</p><p>§6.4 說明裝置對系統記憶體使用 TC0 的 Write，可由 Host 讀取裝置來完成相應 flush；對其他 TC 需要適用的同步機制。這是特定條件下的路徑，不能忽略 RO、IDO 或平台記憶體規則。若裝置間有 P2P 互動，即使使用 TC0，也需要參與裝置之間明確的同步協定。</p></section>
<section id="message"><h2>想查 Message Code，應先看附錄 F 還是封包圖？</h2><p>先用Table F-1以用途找到Message Code、路由與Msg／MsgD，再沿它指向的正式章節讀完整格式與規則。例如頁面要求、失效通知與LTR都能從這個入口接回前章。Table F-1也提醒其他規格可能新增Message，版本較新的定義不一定收錄在這份Base 6.0清單。</p><dl class="st-terms" aria-label="本段名詞"><div><dt>LTR</dt><dd>Latency Tolerance Reporting，延遲容忍度回報</dd></div></dl></section>
<section id="message-lookup"><h2>查到一個代碼後，怎麼找到完整格式？</h2><p><strong>教學情境：</strong>要找 Invalidate Request，先在 Appendix F 的 Table F-1 找到這一列：Message Code <code>0000 0001b</code>、Routing <code>010b</code>、類型 <code>MsgD</code>。再沿同一列的參照讀 §10.3.1，才能確認該功能的封包欄位與處理條件。</p><p>若要找 Function Readiness Status（FRS，Function 就緒狀態），改查 Table F-2 的 PCI-SIG-Defined VDM Subtype：<code>0000 1001b</code>。它是子類型，不能當成 Table F-1 的一般 Message Code。接著讀 §2.2.8.6.3，並結合 Chapter 34 的就緒事件與佇列流程。</p><p>兩張表是 Base 6.0 當時的索引；其他規格後續定義的 Message 或 Subtype 可能尚未列入。索引指出下一個閱讀位置，完整適用條件仍以對應定義為準。</p></section>
<section id="vdm"><h2>遇到 Vendor_Defined Message，先看哪個欄位？</h2><p>先從 Table 2-28 辨認 Message Code：<code>7Eh</code> 是 Vendor_Defined Type 0，<code>7Fh</code> 是 Type 1。這個 Type 表示訊息的種類，不是 TLP Header 中判斷有無 Payload 的 Type：兩者都可能使用無資料的 <code>Msg</code> 或帶資料的 <code>MsgD</code>。</p><p>接著依目前模式選 Figure 2-47（Non-Flit）或 Figure 2-48（Flit），讀 Vendor ID 與 Routing。共通格式中，Route by ID 使用 bytes 8–9 作 Destination ID；其他路由下這兩個 bytes 為 Reserved。個別訊息可以對同一位置另作定義：例如 Hierarchy ID Message 雖採 Broadcast，仍在此放入 Hierarchy ID。Vendor ID 位於 bytes 10–11；bytes 12–15 供訊息定義使用。若 Vendor ID 是 <code>0001h</code> 且 Message Code 是 <code>7Fh</code>，再到 §2.2.8.6.1 和對應模式的 Figures 2-49／2-50，依 Subtype 找 PCI-SIG Defined VDM 的具體規則。例如 <code>09h</code> 是 FRS，後續事件與對象見 <a href="/DOCS/pcie-course/chapter-34.html#frs-reason">Chapter 34</a>。</p><dl class="st-terms" aria-label="本段名詞"><div><dt>FRS</dt><dd>Function Readiness Status，功能就緒狀態</dd></div></dl><p>兩種訊息送到不支援它的 Completer 時，處理方式不同：Type 0 依規則偵測並回報 Unsupported Request；Type 1 由 Completer 靜默丟棄。這個差異描述 Completer 的處理，不能只憑中途未看到訊息就推論它已到達。Switch 對 Routing <code>000b</code>、<code>010b</code>、<code>011b</code> 的收到訊息有轉送要求；<code>100b</code> 則是本地終止。</p><p>共通格式的 Attr 並非 Reserved，但個別訊息可以訂出更嚴格的欄位規則；FRS 就將 Attr 設為 Reserved。一般 VDM 的 Requester ID 在 Non-Flit Mode 由實作決定，而 Flit Mode 須使用與 Requester 關聯的值；PCI-SIG Defined VDM 另要求該欄位使用與 Requester 關聯的值。涉及 PCIe-to-PCI/PCI-X Bridge 與 PCI-X Device ID 相容時，還須查該 Bridge 規格的額外限制。</p></section>
<section id="sources"><h2>版本與來源</h2><p>本章以 PCI Express Base Specification Revision 6.0（6.0-1.0-PUB）為準，文件頁與 PDF 頁相同。案例的配置與讀值均為作者假設，並非實機測量。</p><details class="source-note"><summary>完整來源定位</summary><ul><li>Base 6.0 §2.4.1 Transaction Ordering Rules; pp.222–225; Table 2-42 Ordering Rules Summary</li><li>Base 6.0 Appendix D Request Dependencies, Appendix E ID-Based Ordering Usage, §E.1 Introduction, §E.3 When to Use IDO, §E.4.1 When Not to Use IDO with Endpoints; pp.1549–1550,1553–1555; Figure E-1 Reference Topology for IDO Use</li><li>Base 6.0 §6.4 Device Synchronization; pp.717–718</li><li>Base 6.0 §2.2.8.6 Vendor_Defined Messages and §2.2.8.6.1 PCI-SIG Defined VDMs, pp.179–182; Table 2-28 Vendor_Defined Messages; Figures 2-47 Header for Vendor-Defined Messages - Non-Flit Mode, 2-48 Header for Vendor-Defined Messages - Flit Mode, 2-49 Header for PCI-SIG-Defined VDMs - Non-Flit Mode, 2-50 Header for PCI-SIG-Defined VDMs - Flit Mode</li><li>Base 6.0 Appendix F Message Code Usage; pp.1559–1560; Table F-1 Message Code Usage; Table F-2 PCI-SIG-Defined VDM Subtype Usage; §2.2.8.6.3 Function Readiness Status Message (FRS Message), p.183; §10.3.1 Invalidate Request, p.1497</li></ul></details></section>
</article>
<nav class="bottom-nav" aria-label="課程與語言版本"><a href="/DOCS/pcie-course/index.html">課程總覽</a><a href="/DOCS/pcie-course/chapter-36.html">繁中完整教學</a><a href="/pcie/chapter-36-en/">English</a></nav>
</div>
