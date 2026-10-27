---
layout: post
title: "PCIe Chapter 4: BARs, Address Spaces, and Resource Allocation"
date: 2026-10-20 00:00:00 +0800
last_modified_at: 2026-10-28 00:00:00 +0800
permalink: /pcie/chapter-4-en/
categories: [PCIe]
tags: [PCIe, Specification]
lang: en
spec_teaching: true
spec_series: pcie
description: "從 BAR 格式、大小與對齊配置資源，串連 Bridge Window 和解碼控制，追查設定空間可讀但 Memory Read 失敗的情境。"
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
<nav class="bottom-nav" aria-label="Course and editions"><a href="/DOCS/pcie-course/index.html">Course overview</a><a href="/DOCS/pcie-course/chapter-4.html">Full Chinese tutorial</a><a href="/pcie/chapter-4-zh-tw/">繁體中文</a></nav>
<article class="lesson">
<p><strong>Simulated data:</strong> Addresses, settings and device Registers are created for teaching and do not represent a particular device or platform.</p>
<section id="chapter-overview"><h2>Connect a device resource to the CPU access path</h2><figure class="diagram"><svg viewBox="0 0 900 450" role="img" aria-labelledby="ch4-guide-title ch4-guide-desc"><title id="ch4-guide-title">Nested boxes show address coverage, not multiple copies of device memory. Platform translation determines the relationship between CPU addresses and the address encoded in a BAR.</title><desc id="ch4-guide-desc">Nested boxes show address coverage, not multiple copies of device memory. Platform translation determines the relationship between CPU addresses and the address encoded in a BAR.</desc><g data-walk-target="cpu"><rect x="300" y="10" width="300" height="60" rx="9" fill="var(--surface-alt)" stroke="var(--line)" /><text x="450.0" y="35" text-anchor="middle" font-size="16">CPU access to a device resource</text></g><g data-walk-target="request"><path d="M450 70 L450 115" fill="none" stroke="var(--accent)" stroke-width="2" /><polygon points="450.0,115.0 455.0,105.0 445.0,105.0" fill="var(--accent)" /><text x="450.0" y="83.5" text-anchor="middle" font-size="16">Apply platform address translation</text></g><g data-walk-target="root-window"><rect x="40" y="115" width="820" height="305" rx="9" fill="var(--surface-alt)" stroke="var(--line)" /><text x="450.0" y="140" text-anchor="middle" font-size="16">Root Port window: covers downstream allocations</text></g><g data-walk-target="switch-window"><rect x="135" y="190" width="630" height="205" rx="9" fill="var(--surface-alt)" stroke="var(--line)" /><text x="450.0" y="215" text-anchor="middle" font-size="16">Each switch-path window covers the same target</text></g><g data-walk-target="bar"><rect x="250" y="270" width="400" height="95" rx="9" fill="var(--surface-alt)" stroke="var(--line)" /><text x="450.0" y="295" text-anchor="middle" font-size="16">Endpoint Memory BAR</text><text x="450.0" y="318" text-anchor="middle" font-size="16">Configured base, size and alignment</text></g></svg><figcaption>Nested boxes show address coverage, not multiple copies of device memory. Platform translation determines the relationship between CPU addresses and the address encoded in a BAR.</figcaption></figure><dl class="st-terms" aria-label="Terms in this passage"><div><dt>BAR</dt><dd>Base Address Register</dd></div></dl><p class="lead">A BAR (Base Address Register) describes a device resource and its allocation interface. Determine type and size, allocate an aligned base, cover the range with every bridge window, then enable the applicable decoding.</p><p><strong>Specification route:</strong> Figures 7-10–7-12 and Table 7-9 → bridge-window rules and Figure 7-14 → Command controls in Figure 7-5 and Table 7-4.</p></section>
<p class="lead">Discovering a Function is followed by resource allocation and forwarding setup. BARs describe the Endpoint's own resources, Bridge Windows determine which address ranges reach downstream, and Command bits control permitted accesses. All three must be consistent.</p>
<p><a href="/DOCS/pcie-course/chapter-4.html">Full Chinese tutorial</a> · <a href="/DOCS/pcie-course/index.html">Course roadmap</a> · <a href="/pcie/chapter-4-zh-tw/">繁體中文</a></p>
<aside class="note"><strong>Versions and assumptions</strong><p>Fields follow Base 6.0; address views and handoff follow PCI Firmware 3.3, which is not its matching edition. The example is an ordinary Type 0 PCI Express Endpoint, not a VF, without Enhanced Allocation or Resizable BAR. Values are author-created, with no hardware operation. During sizing the driver is not using the device, no transactions are outstanding, and MSE/BME are clear. Software saves original BARs and confirms configuration write completion. Printed and PDF page numbers coincide.</p><dl class="st-terms" aria-label="Terms in this passage"><div><dt>VF</dt><dd>Virtual Function</dd></div></dl></aside>
<section id="format"><h2>Identify the format before calculating size</h2>
<p>A BAR resides in Configuration Space; it is not a workload buffer. A Type 0 Header has six DWORD locations, and a 64-bit BAR consumes two consecutive locations. A Bridge's Type 1 Header has only two BAR locations, distinct from its downstream Memory Windows.</p>
<p>A Memory BAR has bit 0 clear; bits 2:1 encode 32-bit as 00b and 64-bit as 10b, with Prefetchable in bit 3. An I/O BAR has bit 0 set and address bits beginning at bit 2, so the Memory BAR's four-bit mask does not apply. This example uses no I/O BAR: an ordinary PCIe Endpoint must not depend on OS allocation of I/O resources and must not generate I/O Requests.</p>
<p>Prefetchable expresses permitted behavior such as reads without side effects and tolerance of write merging, not current CPU cache state. A Prefetchable BAR on this ordinary Endpoint must support 64-bit addressing; a non-Prefetchable BAR may be 32-bit.</p>
<details class="source-note"><summary>Reading order</summary><p>Locate the BAR through Figure 7-10 (p.928) or Figure 7-14 (p.936). Decode its format through Figures 7-11/7-12 and Table 7-9 (p.929), then read capacity, pairing, and alignment rules in §7.5.1.2.1 (p.930). Ordinary Endpoint restrictions: §1.3.2.2, p.105.</p></details></section>
<section id="size"><h2>Size probes require the correct 32-bit or 64-bit width</h2>
<p>The specified method disables the corresponding decoding, saves the original BAR, writes all ones, reads it back, and masks the encoding bits. Invert and add one within the intended width. Restore the original value, or establish a consistent new allocation before re-enabling decoding. Clearing BME does not remove earlier outstanding transactions; their absence is a separate assumption here.</p>
<div class="table-wrap"><table><caption>Teaching probe and allocation results</caption><thead><tr><th scope="col">Resource</th><th scope="col">Readback after all-one writes</th><th scope="col">Size and allocation</th></tr></thead><tbody><tr><td>BAR0, 0x10</td><td>0xFFFFC000</td><td>32-bit non-Prefetchable; 16 KiB at 0x80004000–0x80007FFF.</td></tr><tr><td>BAR2/BAR3, 0x18/0x1C</td><td>0xFFE0000C/0xFFFFFFFF</td><td>64-bit Prefetchable; 2 MiB at 0x120000000–0x1201FFFFF.</td></tr></tbody></table></div>
<pre><code>BAR0 mask = 0xFFFFC000 &amp; 0xFFFFFFF0
size = ((~mask) &amp; 0xFFFFFFFF) + 1 = 0x4000

BAR2/3 mask = (0xFFFFFFFF &lt;&lt; 32) | (0xFFE0000C &amp; 0xFFFFFFF0)
size = ((~mask) &amp; 0xFFFFFFFFFFFFFFFF) + 1 = 0x200000</code></pre>
<p>BAR3 is BAR2's upper DWORD, not a separate I/O BAR despite reading all ones. The assigned values are 0x80004000 for BAR0 and 0x2000000C/0x00000001 for BAR2/3. An initial zero BAR does not prove absence; use the valid unimplemented result from the correct probe, and do not misinterpret an all-zero mask as a 4 GiB request.</p>
<p>Assume BAR0+0x120 is a valid device Register, yielding PCI address 0x80004120. The example separately assumes identical CPU/PCI mapping, so the CPU uses that same number. This is not a platform-wide guarantee. The Register and the available resource addresses are also teaching assumptions.</p>
<details class="source-note"><summary>Sources and limits</summary><p>Base 6.0 §7.5.1.2.1, pp.928–930, including the 32/64-bit sizing explanation on p.930. Firmware 3.3 §3.1.1 (p.32) permits non-identity MMIO mapping. Every allocation also needs platform resources, alignment, non-overlap, and address-width checks.</p></details></section>
<section id="window"><h2>Every Bridge Window on the path must contain the target</h2>
<p>The path to 03:00.0 passes through Root Port 00:01.0, Switch Upstream Port 01:00.0, and Downstream A 02:01.0. All three support and use the following windows in the example. The platform reserves the ranges, with no competing sibling allocation.</p>
<div class="table-wrap"><table><caption>Shared teaching configuration for the three Bridges</caption><thead><tr><th scope="col">Fields</th><th scope="col">Values</th><th scope="col">Decoded inclusive range</th></tr></thead><tbody><tr><td>Memory Base/Limit at 0x20/0x22, 16 bits each</td><td>0x8000/0x8000</td><td>0x80000000–0x800FFFFF</td></tr><tr><td>Prefetchable Base/Limit at 0x24/0x26, 16 bits each; Upper at 0x28/0x2C, 32 bits each</td><td>0x2001/0x2011; both Upper values are 1</td><td>0x120000000–0x1201FFFFF</td></tr></tbody></table></div>
<p>The Base's omitted lower 20 address bits become zero, while the Limit's become one, creating inclusive ranges with 1 MiB granularity. A low nibble of one in the Prefetchable fields indicates 64-bit support, with Upper fields supplying address bits 63:32. A window may exceed a BAR's size, but its gaps need not contain valid Registers. Bus Number ranges do not replace Memory Windows.</p>
<details class="source-note"><summary>Sources</summary><p>Figure 7-14, p.936; §7.5.1.3.8–§7.5.1.3.10, pp.940–941. The full tutorial derives the masks, shifts, and range containment.</p></details></section>
<section id="control"><h2>MSE and BME control different behavior</h2>
<p>Command is a 16-bit Register at 0x04. Bit 0 controls I/O Space, bit 1 MSE controls received Memory accesses, and bit 2 BME controls Function-originated Memory/I/O Requests. A Type 1 Port's BME also controls forwarding those Requests upstream, without blocking Completions.</p>
<p>With resources, windows, platform mapping, and the device interface ready, Command=0x0002 on the Endpoint and all three Bridges permits the example's CPU MMIO read while prohibiting Endpoint-originated DMA Memory Requests. BME does not block the read's Completion. BME=0 also prohibits MSI/MSI-X because they use in-band Memory Writes.</p><dl class="st-terms" aria-label="Terms in this passage"><div><dt>MMIO</dt><dd>Memory-Mapped I/O, mapped device-register access</dd></div><div><dt>DMA</dt><dd>Direct Memory Access, device access to memory</dd></div><div><dt>MSI</dt><dd>Message Signaled Interrupt</dd></div><div><dt>MSI-X</dt><dd>Message Signaled Interrupts Extension</dd></div></dl>
<p>Changing the Endpoint to 0x0006 adds permission to originate the relevant Requests, but does not prepare buffers, device work, platform translation, or upstream Port BME. Do not update Command by blindly writing back a DWORD that includes Status at 0x06, since Status contains RW1C bits.</p>
<details class="source-note"><summary>Control sources</summary><p>Base 6.0 §7.5.1.1.3, Figure 7-5/Table 7-4, pp.917–920; BME, Completion, and MSI behavior on p.919. Command/Status layout: Figure 7-4, p.916; Status RW1C: Table 7-5, pp.922–923.</p></details></section>
<section id="read-path"><h2>Why can Configuration Space be readable while a Memory Read fails?</h2>
<p>Configuration access selects a Function and Register using BDF and an offset; a Memory Read selects its target by memory address. In the existing example, place <code>0x80004120</code> inside BAR0 and each Bridge Window, then inspect Memory Space Enable (MSE) along the receiving direction.</p><dl class="st-terms" aria-label="Terms in this passage"><div><dt>BDF</dt><dd>Bus/Device/Function</dd></div></dl>
<aside class="example"><strong>Simulated data: decoding is disabled at an intermediate Port</strong><p>Assume Configuration Space of 03:00.0 is readable and BAR0 and all three Bridge Windows retain their earlier settings. MSE is 1 at the Root Port, Switch Upstream Port, and Endpoint, but 0 at Downstream A. Using the example’s identity mapping, the CPU issues a 4-byte Memory Read to the valid BAR0 + 0x120 Register. Assume the Request is legal and has reached Downstream A’s Primary Side, the bridge side facing upstream.</p>
<p>Scroll the table horizontally to see all columns when needed.</p><div class="table-wrap"><table style="min-width: 640px"><caption>Two accesses to the same target</caption><thead><tr><th scope="col">Observation</th><th scope="col">Meaning at this step</th><th scope="col">Next step</th></tr></thead><tbody><tr><td>Configuration Read of 03:00.0 succeeds</td><td>Configuration data was obtained from this Function through the configuration path.</td><td>Locate BAR0 in the Type 0 Header, then the Windows and Command in the Type 1 Headers.</td></tr><tr><td>PCI Memory Read address is 0x80004120</td><td>It lies inside BAR0, 0x80004000–0x80007FFF, and each assumed Memory Window.</td><td>After checking the ranges, inspect MSE at the receiving Function and Bridges.</td></tr><tr><td>Downstream A has MSE=0</td><td>The example’s Memory Read has reached its Primary Side. Table 7-4 requires it to be handled as Unsupported Request (UR).</td><td>This Port handles the read as UR rather than forwarding it to the Endpoint. Request Handling requires a UR Completion; the return path must still deliver it.</td></tr></tbody></table></div>
<p>If the other conditions remain unchanged and Downstream A’s MSE is set, the Port is enabled to decode and further process the address. Check whether the Request reaches the Endpoint, whether a Completion returns, and whether the device interface is ready before assessing the transaction. The platform determines how the CPU observes an error; PCIe Completion Status and the CPU’s read result are distinct observations.</p></aside>
<p>Locate the BAR and Bridge fields in Figure 7-10 and Figure 7-14; decode Memory Base/Limit with §7.5.1.3.8; then read MSE in Figure 7-5/Table 7-4, including the Primary Side condition for a Type 1 Header. Finally use §2.3.1 to determine how UR is returned for a Request requiring Completion. (Base 6.0, printed/PDF pp.208, 916–918, 928, 936, 940.)</p>
<h3>Is every byte inside a BAR readable?</h3>
<p>The BAR defines an address range, while the device interface defines which Registers can be used. The example assumes only that <code>+0x120</code> is a readable Register; it does not define <code>+0x3000</code>, although that offset is also inside BAR0. Base 6.0 §7.5.1.2.1 (p.930) permits a Function to return UR for unused locations its programming model never accesses. The device interface and transaction evidence are needed to assess an actual access.</p></section>

<section id="checks"><h2>Keep allocation and handoff conclusions separate</h2>
<p>Firmware 3.3 §3.5 (pp.34–35) uses I/O/Memory Enable and ROM Enable to determine corresponding resource configuration, not BME to establish BAR validity. Enabled resources must be correctly configured by firmware, but drivers still prepare device-specific work.</p><dl class="st-terms" aria-label="Terms in this passage"><div><dt>ROM</dt><dd>Read-Only Memory</dd></div></dl>
<details class="question"><summary>Can the 16 KiB BAR move to 0x80005000?</summary><p>No. Its lower 14 bits are not all zero, violating natural alignment. The example's 0x80004000 base meets the requirement. (§7.5.1.2.1, p.930.)</p></details>
<details class="question"><summary>Do correct windows permit a successful MMIO read when Endpoint MSE is clear?</summary><p>Success cannot be expected. With MSE clear, the Endpoint handles received Memory Space accesses as UR. A forwarding path does not replace target enablement. (Table 7-4, p.918.)</p></details></section>
<p><a href="/DOCS/pcie-course/chapter-5.html">Chapter 5</a> follows Requests and Completions; Chapters 6–7 cover DMA and interrupts.</p><dl class="st-terms" aria-label="Terms in this passage"><div><dt>DMA</dt><dd>Direct Memory Access, device access to memory</dd></div></dl>
</article>
<nav class="bottom-nav" aria-label="Course and editions"><a href="/DOCS/pcie-course/index.html">Course overview</a><a href="/DOCS/pcie-course/chapter-4.html">Full Chinese tutorial</a><a href="/pcie/chapter-4-zh-tw/">繁體中文</a></nav>
</div>
