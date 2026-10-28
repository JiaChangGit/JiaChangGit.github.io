---
layout: post
title: "PCIe Chapter 23：功率預算、動態分配與緊急降功耗"
date: 2026-10-24 00:00:00 +0800
last_modified_at: 2026-10-29 00:00:00 +0800
permalink: /pcie/chapter-23-zh-tw/
categories: [PCIe]
tags: [PCIe, Specification]
lang: zh-TW
spec_teaching: true
spec_series: pcie
description: "裝置已進 D0，功率限制還有哪些層次？"
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
<nav class="bottom-nav" aria-label="課程與語言版本"><a href="/DOCS/pcie-course/index.html">課程總覽</a><a href="/DOCS/pcie-course/chapter-23.html">繁中完整教學</a><a href="/pcie/chapter-23-en/">English</a></nav>
<article class="lesson">
<p>D0 表示 Function 處於工作電源狀態，功率仍受系統授權與所用機制限制。Power Budgeting（功率預算資料）讓系統了解裝置在指定條件下的需求；DPA（Dynamic Power Allocation，動態功率配置）則讓軟體在 D0 內調整 Function 的功率配置。本章先讀功耗資料，再帶一次降功率與升功率的完整案例。</p><figure class="diagram"><svg viewBox="0 0 900 280" style="min-width:640px" role="img" aria-labelledby="ch23-zh-t ch23-zh-d"><title id="ch23-zh-t">不同功率機制的對象與用途</title><desc id="ch23-zh-d">三欄分別表示功耗回報、插卡授權與D0內功率配置，並非三個連續步驟。緊急降功耗另有優先關係。</desc><g data-walk-target="n0"><rect x="20" y="25" width="260" height="95" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="150" y="60" text-anchor="middle" font-size="17">回報功耗資料</text><text x="150" y="94" text-anchor="middle" font-size="16">Power Budgeting</text></g><g data-walk-target="a"><text x="150" y="157" text-anchor="middle" font-size="16">按相同條件整理需求</text></g><g data-walk-target="n1"><rect x="320" y="25" width="260" height="95" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="450" y="60" text-anchor="middle" font-size="17">整張卡的功率授權</text><text x="450" y="94" text-anchor="middle" font-size="16">Slot / Power Limit</text></g><g data-walk-target="b"><text x="450" y="157" text-anchor="middle" font-size="16">依授權機制限制功率</text></g><g data-walk-target="n2"><rect x="620" y="25" width="260" height="95" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="750" y="60" text-anchor="middle" font-size="17">Function 的功率配置</text><text x="750" y="94" text-anchor="middle" font-size="16">DPA within D0</text></g><g data-walk-target="c"><text x="750" y="157" text-anchor="middle" font-size="16">依 Control 與 Status 判讀</text></g><g data-walk-target="n3"><rect x="20" y="205" width="860" height="55" rx="10" fill="var(--surface-alt)" stroke="var(--accent)"/><text x="450" y="239" text-anchor="middle" font-size="17">Emergency Power Reduction：支援時優先處理</text></g></svg><figcaption><p>作者依 Base 6.0 §§6.8、6.9、6.16、6.24 繪製。每種能力均須先確認是否實作及其適用條件。DPA 是 Dynamic Power Allocation（動態功率配置）。</p></figcaption></figure><section id="budget"><h2>要替插卡安排功率，先確定資料代表誰</h2>
<p>先回顧一個範圍差異：Function 是軟體可識別的功能，插卡則可能包含多個 Function，甚至多個 Device。Table 6-10 <em>Power Budgeting Deployments</em>（p.743）依能力結構的分布決定資料涵蓋範圍。例如，多功能 Device 只有一個 Function 實作 Power Budgeting（功率預算資料）時，資料代表整個 Device；若多個 Function 都實作，資料才分別代表各 Function，依表中規則加總。</p>
<p>這一步要在算瓦數之前完成。多裝置插卡還要判斷資料是按整張卡回報，還是按 Device 回報；沒有這個範圍資訊，直接把所有可讀值相加會重複計算。§6.8.1 也把韌體已配置與預算管理者接手的情況分開，實際平台採用哪一種管理流程由平台決定。</p>
<p><strong>【模擬資料】以下資料為教學用途建立，不代表特定硬體或平台。</strong>本章使用一張只有單功能 Endpoint 的插卡，所有耗電均涵蓋在 Function 0 的回報中，沒有其他 Device 或外接電源。它從 12 V 與 3.3 V 兩條電源軌取電，目前為 D0。假設 System Allocated=0、Extended Power Budgeting Supported=0，且共有四筆非延伸資料；平台另已依適用外形規格與總預算完成足夠的功率授權。</p>
<p class="source-note">來源：§6.8 <em>Power Budgeting Mechanism</em>、§6.8.1 <em>System Power Budgeting Process Recommendations</em>、Table 6-10，文件／PDF pp.742–744。</p></section>

<section id="budget-entries"><h2>Data Select 怎麼選，哪些資料才可以加總？</h2>
<p>先沿 Extended Capability（延伸能力結構）鏈找到 ID 0004h、Version 1h，將起點記為 C。Figure 7-136 定位三個本次會用到的入口：Data Select 在 C+04h，為 8-bit；Data 在 C+08h，為 32-bit；Power Budgeting Capability 在 C+0Ch。先查 Capability 的 System Allocated，再依序<strong>寫入 Data Select 索引、讀取 Data</strong>。索引從 0 開始，預設值未定義，因此每次查詢都要明確選取。</p>
<p>接著打開 Figure 7-139／Table 7-122。Base Power 在 bits [7:0]；Data Scale 低兩位在 bits [9:8]，第三位另在 bit 21，並不連續。本例未使用延伸資料，第三位為 0，倍率編碼 001b 代表 0.1×。先由 PM State、PM Sub State、Type、Power Rail 辨認條件，再把 Base Power 乘上倍率：</p>
<div class="table-wrap"><table><thead><tr><th scope="col">Index</th><th scope="col">Data</th><th scope="col">PM State / Sub State</th><th scope="col">Type</th><th scope="col">Power Rail</th><th scope="col">Base Power</th><th scope="col">Data Scale</th><th scope="col">功率</th></tr></thead><tbody><tr data-budget-entry="0"><td>0</td><td>000181B4h</td><td>D0 / 0</td><td>011b</td><td>000b / 12 V</td><td>180</td><td>0.1×</td><td>18 W</td></tr><tr data-budget-entry="1"><td>1</td><td>00058132h</td><td>D0 / 0</td><td>011b</td><td>001b / 3.3 V</td><td>50</td><td>0.1×</td><td>5 W</td></tr><tr data-budget-entry="2"><td>2</td><td>000381C8h</td><td>D0 / 0</td><td>111b</td><td>000b / 12 V</td><td>200</td><td>0.1×</td><td>20 W</td></tr><tr data-budget-entry="3"><td>3</td><td>0007813Ch</td><td>D0 / 0</td><td>111b</td><td>001b / 3.3 V</td><td>60</td><td>0.1×</td><td>6 W</td></tr></tbody></table></div>
<p>以索引 0 的 000181B4h 為例，Base Power=B4h=180、Data Scale=001b，所以得到 18 W；Type=011b 是 Sustained Power（持續功率），Power Rail=000b 是 12 V。索引 1 的條件相同，只是另一條電源軌，所以兩筆一起構成 <strong>23 W</strong> 的 D0 持續功率。索引 2／3 同屬 Type=111b 的 Maximum Power（最大功率），加總為 <strong>26 W</strong>。</p>
<p>Table 7-122 對這兩種 Type 使用不同量測定義：除非外形規格另有明定，Sustained Power 是最大吞吐量下的 5 秒平均，Maximum Power 則使用 1 ms 移動視窗。23 W 與 26 W 描述不同條件，不一起加總。若另有 Thermal（熱負載）項目，要用於散熱評估，也不當成額外電源軌再加一次。</p>
<p>本例索引 4 已超出四筆資料，Data 回傳全零。若裝置支援 Extended Power Budgeting，延伸項目在 Enable=0 時也會被隱藏成全零；因此不同裝置上的零值，還要連同 Support、Enable 與索引解讀。另外，Base Power 大於 EFh 且符合 Table 7-122 所列條件時，會改用功率區間編碼；不能一律把 F0h 當成 240 W。</p>
<p>本例 System Allocated=0，所以需要由負責的預算管理者納入評估。若該 bit=1，表示這份裝置預算已包含在系統預算內，軟體做功率預算決策時必須忽略這份回報，避免再算一次；裝置本身仍然會耗電。</p>
<p class="source-note">來源：§7.8.1–§7.8.1.5，Figure 7-136（p.1090）、Figure 7-137／Table 7-120（p.1091）、Figure 7-139／Table 7-122（pp.1094–1097）、Figure 7-140／Table 7-123（p.1098）；Data Select 與全零規則見 pp.1091、1093。</p></section>

<section id="grants"><h2>讀到 26 W，系統就已經授權 26 W 了嗎？</h2>
<p>Power Budgeting 回報需求；授權要再查使用中的機制。§6.9 的 Slot Power Limit（插槽功率限制）由 Downstream Port 的 Slot Capabilities 欄位提供，透過 Set_Slot_Power_Limit Message 傳給同一條 Link 對端的 Upstream Port，再反映於 Device Capabilities 的 Captured Slot Power Limit Value／Scale。這項限制的對象是整張插卡。</p>
<p>插卡尚未獲得較高功率授權前，必須遵守適用外形規格的初始限制；Slot 機制也不是任意往下寫一個更小值。§6.8.3 另定義 Power Limit PM Sub State 與 Out of Band Power Limit 等機制，具有不同的優先關係。前者的 Power Limit Enable／Power Limit PM Sub State 只能在所有 Functions 都處於 D0uninitialized 時，以 Configuration Write 設定；任何 Function 離開該狀態後再改，行為未定義。</p>
<p>因此，下面的執行期調整使用 DPA。Power Budgeting 的 PM Sub State 最多有 8 個，DPA Substate 最多有 32 個；規格沒有把這兩組編號直接配對。Function 的 D0／D1 等電源狀態，以及 Link 的 L1.1／L1.2，也各有不同意義。</p>
<p class="source-note">來源：§6.8.3 <em>Power Limit Mechanismsm</em>（原文標題拼字）、§6.9 <em>Slot Power Limit Control</em>，文件／PDF pp.744–746。</p></section>

<section id="dpa"><h2>同在 D0，如何把配置從 26 W 降到 10 W？</h2>
<p>DPA 是可選的 Endpoint Function 功能，適用於 D0。Substate 從 0 連續編到 Substate_Max；0 代表最高配置，每往後一級的配置必須小於或等於前一級。軟體可以直接從 0 選到 2，無須先經過 1；Function 在任一子狀態中都必須回應 Configuration Space 存取。</p>
<p>延續前面的單功能插卡，假設另找到 DPA Extended Capability，起點為 D。Figure 7-281 先給整體布局；Figure 7-282／Table 7-251 確認 ID=0016h、Version=1h。接著依下列順序把能力換成可用的配置表：</p>
<ol><li>Figure 7-283／Table 7-252：D+04h 的 DPA Capability=08031002h。Substate_Max=2，表示共三個子狀態；Power Allocation Scale=01b，倍率為 1.0×；Transition Latency Unit=00b，單位為 1 ms；Value 0=3，Value 1=8。</li><li>Figure 7-284／Table 7-253：D+08h 的 DPA Latency Indicator=00000004h。bit 2=1，因此目標子狀態 2 用 Value 1；bit 0／1=0，兩者用 Value 0。</li><li>Figures 7-287／7-288、Table 7-256：Power Allocation Array 從 D+10h 開始，每個子狀態一個 byte，不是每項一個 DWORD。</li></ol>
<div class="table-wrap"><table><thead><tr><th scope="col">Substate</th><th scope="col">Array offset</th><th scope="col">Array byte</th><th scope="col">Allocation</th><th scope="col">Indicator bit</th><th scope="col">Maximum latency</th></tr></thead><tbody><tr data-dpa-profile="0"><td>0</td><td>D+10h</td><td>1Ah</td><td>26 W</td><td>0</td><td>3 ms</td></tr><tr data-dpa-profile="1"><td>1</td><td>D+11h</td><td>12h</td><td>18 W</td><td>0</td><td>3 ms</td></tr><tr data-dpa-profile="2"><td>2</td><td>D+12h</td><td>0Ah</td><td>10 W</td><td>1</td><td>8 ms</td></tr></tbody></table></div>
<p>因此，選擇子狀態 2 的最大轉換時間是 <strong>8 ms</strong>；回到子狀態 0 則是 <strong>3 ms</strong>。這些上限依<strong>目標子狀態</strong>選取，裝置可以提早完成。DPA 的倍率與前面 Power Budgeting Data Scale 的編碼不同，必須各讀自己的 Table。</p>
<p class="source-note">來源：§6.16 <em>Dynamic Power Allocation (DPA) Capability</em>，文件／PDF pp.777–778；§7.9.12、Figures 7-281–7-288、Tables 7-251–7-256，pp.1236–1241。</p></section>

<section id="dpa-transition"><h2>Control 與 Status 要怎麼一起看？</h2>
<p>先看 Figure 7-285／Table 7-254：Status 在 D+0Ch，bits [4:0] 是 Substate Status，bit 8 是 Substate Control Enabled。本例初始讀值 0100h，表示 Enabled=1、目前子狀態為 0。再看 Figure 7-286／Table 7-255：Control 在 D+0Eh，bits [4:0] 是要求的目標，其餘 RsvdP（保留原值）位元本例原值均為 0。以下假設 Function 持續在 D0、沒有 Reset、緊急降功耗或其他軟體改寫，先完成降功率，再提出升功率要求。</p>
<figure class="diagram"><svg viewBox="0 0 900 300" style="min-width:640px" role="img" aria-labelledby="dpa-transition-title dpa-transition-desc"><title id="dpa-transition-title">降功率：26 W → 10 W / 升功率：10 W → 26 W</title><desc id="dpa-transition-desc">過渡期間 Substate Status=0，配置仍為 26 W. 過渡期間 Substate Status=0，配置已為 26 W.</desc><text x="30" y="32" font-size="18">降功率：26 W → 10 W</text><path d="M100 70 H800" stroke="var(--accent)" stroke-width="2"/><polygon points="800,70 790,65 790,75" fill="var(--accent)"/><path d="M100 58 V82 M800 58 V82" stroke="var(--accent)" stroke-width="2"/><text x="100" y="106" text-anchor="middle" font-size="16">要求 2</text><text x="800" y="106" text-anchor="middle" font-size="16">完成於 2（最長 8 ms）</text><text x="450" y="60" text-anchor="middle" font-size="16">過渡期間 Substate Status=0，配置仍為 26 W</text><text x="30" y="179" font-size="18">升功率：10 W → 26 W</text><path d="M100 217 H800" stroke="var(--accent)" stroke-width="2"/><polygon points="800,217 790,212 790,222" fill="var(--accent)"/><path d="M100 205 V229 M800 205 V229" stroke="var(--accent)" stroke-width="2"/><text x="100" y="253" text-anchor="middle" font-size="16">要求 0</text><text x="800" y="253" text-anchor="middle" font-size="16">完成於 0（最長 3 ms）</text><text x="450" y="207" text-anchor="middle" font-size="16">過渡期間 Substate Status=0，配置已為 26 W</text></svg><figcaption>作者依 §6.16 繪製的兩種轉換方向；不代表每次降功率後都必須升回去。圖中的瓦數表示配置額度，並非瞬間實測功率。</figcaption></figure>
<div class="table-wrap"><table><thead><tr><th scope="col">觀察時點</th><th scope="col">Control</th><th scope="col">Status</th><th scope="col">Status 對應配置</th><th scope="col">系統如何安排功率</th></tr></thead><tbody><tr data-dpa-transition="initial"><td>降功率前</td><td>0000h</td><td>0100h</td><td>26 W</td><td>按原配置保留額度</td></tr><tr data-dpa-transition="down-pending"><td>降功率進行中</td><td>0002h</td><td>0100h</td><td>26 W</td><td>尚未完成降功率，先保留原額度</td></tr><tr data-dpa-transition="down-done"><td>降功率已完成</td><td>0002h</td><td>0102h</td><td>10 W</td><td>此時才可按較低配置重新安排額度</td></tr><tr data-dpa-transition="up-pending"><td>升功率已開始，仍在過渡中</td><td>0000h</td><td>0100h</td><td>26 W</td><td>提出升功率要求前，就須先備妥較高額度</td></tr></tbody></table></div>
<p>降功率時，Status 必須等轉換完成才顯示較低配置。本例 Substate Control=2、Substate Status 仍為 0 的期間，系統要保留 26 W，不能先把差額分給別張卡。讀到 Substate Status=2 之後，Function 必須遵守該狀態的 10 W 配置。</p>
<p>升功率時則不同：轉換期間 Substate Status 就要顯示較高配置，所以讀到目標 0 不能單獨證明已完成轉換。系統必須在提出要求前先準備好 26 W 額度，再依目標的最大轉換時間與需要的裝置資訊安排後續動作。Substate Status 表示的是裝置必須遵守的配置，不是功率感測器的即時讀值，也不保證某個應用效能。</p>
<p>§6.16 允許軟體在前一次轉換完成前再改目標；裝置可調整進行中的轉換，或在完成後比對最新目標並繼續轉換。本例為了看清兩個方向，沒有插入其他要求。分析實機紀錄時，必須保留每次 Control 寫入，不能只拿最後一筆 Status 反推完整經過。</p>
<p class="source-note">來源：§6.16，文件／PDF pp.777–778；§7.9.12.4–§7.9.12.5、Figures 7-285／7-286、Tables 7-254／7-255，pp.1239–1240。</p></section>

<section id="dpa-handoff"><h2>Enabled=0，要寫 1 把 DPA 打開嗎？</h2>
<p>這個欄位要先看屬性。Substate Control Enabled 是 RW1C（寫入 1 會清除），不在 DPA Control 裡，而在 DPA Status 的 bit 8。硬體在 Conventional Reset 或 FLR（Function Level Reset，單一功能重設）後設為 1；軟體不能直接把它設回 1。</p>
<p>例如，在子狀態 2 時讀到 Status=0102h，若向 Status 寫入 0100h，效果是清除 Enabled。之後即使修改 Control 的目標，也不會由該欄位直接啟動 DPA 轉換。這讓裝置專屬軟體可以接手功率管理；接手後的策略由相應軟體與裝置機制決定，不能由 Disabled 推論裝置會永久固定在 10 W。</p>
<p class="source-note">來源：§6.16，文件／PDF p.777；§7.9.12.4、Table 7-254，pp.1239–1240。</p></section>

<section id="emergency"><h2>緊急降功耗後，裝置會自動恢復嗎？</h2>
<p>Emergency Power Reduction State（緊急功率降低狀態）是可選的保護機制，用來避免系統損害；支援時會優先於這裡的一般功率控制。先從 Device Capabilities 2 的 Emergency Power Reduction Supported 與 Emergency Power Reduction Initialization Required，連到 Table 6-16 核對允許的觸發方式。退出後如何恢復，則繼續讀 §6.24 的文字規則。</p>
<p>例如 Supported=10b 可使用適用外形規格定義的機制；該外形規格必須確實定義這種請求方式，才能使用此編碼。廠商專屬與自主機制也依 Table 6-16 的條件判讀。這裡沒有一個對所有平台通用的「寫標準 Configuration bit 即觸發」流程。</p>
<div class="table-wrap"><table><thead><tr><th scope="col">Initialization Required</th><th scope="col">進入時</th><th scope="col">退出後</th></tr></thead><tbody><tr><td>0</td><td>Function 可以降低效能或進入裝置專屬休眠；Upstream Port 維持運作，未完成 Requests 必須正常完成</td><td>不需軟體介入即可恢復正常操作</td></tr><tr><td>1</td><td>Function 停止正常運作，Upstream Port 可以進入 DL_Down；若仍維持 DL_Up，未完成 Requests 仍須正常完成</td><td>需要軟體介入；若先前進入 DL_Down，所有 Functions 都會被重設，並需要完整重新配置</td></tr></tbody></table></div>
<p>Initialization Required=1 時也可能維持 DL_Up，因此光是 Configuration Space 可讀，仍不足以判定是否需要軟體重新初始化。裝置如何通知軟體需要重新初始化，以及外部觸發訊號的硬體細節，還要查平台、外形規格或廠商文件。Power Budgeting 回報也須包含相應的緊急狀態功耗資料，不能直接沿用前面正常 D0 的 26 W。</p>
<p class="source-note">來源：§6.24 <em>Emergency Power Reduction State</em>、Table 6-16 <em>Emergency Power Reduction Supported Values</em>，文件／PDF pp.812–813；§7.5.3.15，p.993；§7.8.1.4，p.1097。</p></section>

<section id="virtual-functions"><h2>多功能裝置與 PF／VF，哪些功率要一起算？</h2><dl class="st-terms" aria-label="本段名詞"><div><dt>PF</dt><dd>Physical Function，實體功能</dd></div><div><dt>VF</dt><dd>Virtual Function，虛擬功能</dd></div></dl>
<p>PF（Physical Function，實體功能）與 VF（Virtual Function，虛擬功能）屬於 SR-IOV（單根 I/O 虛擬化）的功能分工。Power Budgeting 可由 PF 實作，回報必須涵蓋其相關 VFs；VF 不得實作這組能力。DPA 也由相關 PF 管理 VF 的功率，VF 不得實作 DPA Capability。</p><dl class="st-terms" aria-label="本段名詞"><div><dt>SR-IOV</dt><dd>Single Root I/O Virtualization，單根I/O虛擬化</dd></div></dl>
<p>一般多功能 Device 則可以有部分或全部 Functions 實作 DPA；總配置依各份 DPA 配置加總。一個 Function 的 DPA 也可涵蓋其他未實作 DPA 的 Functions，這些關聯由實作決定。因此本章的單功能案例不能直接複製成「每個 VF 都再配置 26 W」。</p>
<p>Function 的 D-State 另依 §5.10：PF 必須有 Power Management Capability，VF 可選。VF 沒有自己的能力時，視為跟隨相關 PF 的等效電源狀態；若 VF 有自己的能力，PF 比 VF 進入更低功耗狀態會造成未定義行為，軟體應先降低 VFs 的電源狀態，再降低 PF。這與本章在 D0 內調整 DPA 配置是不同操作。</p>
<p class="source-note">來源：§5.10–§5.10.1，文件／PDF p.655；§6.16.1，p.778；§7.8.1，p.1090。</p></section><section id="sources"><h2>版本與來源</h2><p>本章依 PCI Express Base Specification Revision 6.0（6.0-1.0-PUB）。以下文件印刷頁與 PDF 檢視器頁碼相同；案例讀值與轉換觀察均為教學假設，未執行實機量測。</p><details class="source-note"><summary>完整來源定位</summary><ul><li>§6.8 <em>Power Budgeting Mechanism</em>, pp.742–745; Table 6-10 <em>Power Budgeting Deployments</em>, p.743; §6.8.1 <em>System Power Budgeting Process Recommendations</em>, pp.743–744; §6.8.3 <em>Power Limit Mechanismsm</em>, pp.744–745; §6.9 <em>Slot Power Limit Control</em>, pp.745–746.</li><li>§7.8.1 <em>Power Budgeting Extended Capability</em>, pp.1090–1098; Figure 7-136 (layout), p.1090; Figure 7-137 / Table 7-120 (header), p.1091; §7.8.1.2 <em>Power Budgeting Data Select Register</em>, p.1091; §7.8.1.3 / Figure 7-138 / Table 7-121 <em>Power Budgeting Control Register</em>, pp.1091–1093; §7.8.1.4 / Figure 7-139 / Table 7-122 <em>Power Budgeting Data Register</em>, pp.1093–1097; §7.8.1.5 / Figure 7-140 / Table 7-123 <em>Power Budgeting Capability Register</em>, p.1098.</li><li>§6.16 <em>Dynamic Power Allocation (DPA) Capability</em>, pp.777–778; §6.16.1 <em>DPA Capability with Multi-Function Devices</em>, p.778.</li><li>§7.9.12 <em>Dynamic Power Allocation Extended Capability (DPA Capability)</em>, pp.1236–1241; Figure 7-281 <em>Dynamic Power Allocation Extended Capability Structure</em>, p.1237; Figure 7-282 / Table 7-251 <em>DPA Extended Capability Header</em>, pp.1237–1238; Figure 7-283 / Table 7-252 <em>DPA Capability Register</em>, pp.1238–1239; Figure 7-284 / Table 7-253 <em>DPA Latency Indicator Register</em>, p.1239; Figure 7-285 / Table 7-254 <em>DPA Status Register</em>, pp.1239–1240; Figure 7-286 / Table 7-255 <em>DPA Control Register</em>, p.1240; Figure 7-287 <em>DPA Power Allocation Array</em>, p.1240; Figure 7-288 / Table 7-256 <em>Substate Power Allocation Register (0 to Substate_Max)</em>, p.1241.</li><li>§6.24 <em>Emergency Power Reduction State</em>, pp.812–813; Table 6-16 <em>Emergency Power Reduction Supported Values</em>, p.812; §7.5.3.15 <em>Device Capabilities 2 Register</em>, p.993 (support and initialization fields); §5.10 <em>SR-IOV Power Management</em> / §5.10.1 <em>VF Device Power Management States</em>, p.655.</li></ul></details></section>
</article>
<nav class="bottom-nav" aria-label="課程與語言版本"><a href="/DOCS/pcie-course/index.html">課程總覽</a><a href="/DOCS/pcie-course/chapter-23.html">繁中完整教學</a><a href="/pcie/chapter-23-en/">English</a></nav>
</div>
