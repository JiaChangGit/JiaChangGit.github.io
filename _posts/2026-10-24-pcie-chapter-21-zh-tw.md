---
layout: post
title: "PCIe Chapter 21：接收端、通道與參考時脈"
date: 2026-10-24 00:00:00 +0800
last_modified_at: 2026-10-29 00:00:00 +0800
permalink: /pcie/chapter-21-zh-tw/
categories: [PCIe]
tags: [PCIe, Specification]
lang: zh-TW
spec_teaching: true
spec_series: pcie
description: "發送端符合規格，為什麼接收端還要另做測試？"
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
<nav class="bottom-nav" aria-label="課程與語言版本"><a href="/DOCS/pcie-course/index.html">課程總覽</a><a href="/DOCS/pcie-course/chapter-21.html">繁中完整教學</a><a href="/pcie/chapter-21-en/">English</a></nav>
<article class="lesson">
<p>Rx（Receiver，接收端）看到的是訊號走過通道後的結果。接收能力要和通道損耗、等化及 Refclk（Reference Clock，參考時脈）一起檢查；單看發送端波形，還沒有走完整條訊號路徑。</p><figure class="diagram"><svg viewBox="0 0 900 420" style="min-width:640px" role="img" aria-labelledby="ch21-zh-t ch21-zh-d"><title id="ch21-zh-t">接收實測與校準模型的不同路徑</title><desc id="ch21-zh-d">先建立通道與時脈模型，再判讀接收端壓力測試。</desc><g data-walk-target="tx"><rect x="20" y="60" width="220" height="44" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="130.0" y="89" text-anchor="middle" font-size="16">發送設定／測試來源</text></g><g data-walk-target="channel"><rect x="335" y="60" width="240" height="44" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="455.0" y="89" text-anchor="middle" font-size="16">通道：損耗與串擾</text></g><g data-walk-target="rx"><rect x="650" y="60" width="230" height="44" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="765.0" y="89" text-anchor="middle" font-size="16">Rx：接收與等化</text></g><g data-walk-target="clock"><rect x="30" y="300" width="300" height="44" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="180.0" y="329" text-anchor="middle" font-size="16">Refclk 架構與抖動模型</text></g><g data-walk-target="eye"><rect x="480" y="300" width="390" height="68" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="675.0" y="329" text-anchor="middle" font-size="16">TP2 資料加上校準模型</text><text x="675.0" y="353" text-anchor="middle" font-size="16">TP2P 眼圖：套用適用的條件</text></g><g data-walk-target="a"><path d="M240 94 L335 94" stroke="var(--accent)" stroke-width="2" fill="none"/><polygon points="335,94 325.0,99.0 325.0,89.0" fill="var(--accent)"/><text x="287.5" y="84.0" text-anchor="middle" font-size="16">訊號</text></g><g data-walk-target="b"><path d="M575 94 L650 94" stroke="var(--accent)" stroke-width="2" fill="none"/><polygon points="650,94 640.0,99.0 640.0,89.0" fill="var(--accent)"/><text x="612.5" y="84.0" text-anchor="middle" font-size="16">輸入</text></g><g data-walk-target="c"><path d="M330 334 L480 334" stroke="var(--accent)" stroke-width="2" fill="none"/><polygon points="480,334 470.0,339.0 470.0,329.0" fill="var(--accent)"/><text x="405.0" y="324.0" text-anchor="middle" font-size="16">時脈條件</text></g><g data-walk-target="d"><path d="M455 104 V190 H675 V300" stroke="var(--accent)" stroke-width="2" fill="none"/><polygon points="675,300 670,290 680,290" fill="var(--accent)"/><text x="570" y="175" text-anchor="middle" font-size="16">校準時使用 Replica 路徑</text></g></svg><figcaption><p>作者繪製的關係圖。上方是實際 Rx 接收路徑，下方是另行校準的模型路徑；沒有把等化模型接到 DUT 的實測輸出後。</p></figcaption></figure>
<section id="receiver"><h2>先分清校準眼圖與接收器測試結果</h2>
<p>Rx（Receiver，接收端）測試先建立一個符合指定壓力的輸入，再用這個輸入測實際接收器。Stressed eye（加入指定損耗、抖動與干擾的眼圖）校準成功，只代表測試刺激已準備好；DUT（Device Under Test，待測元件）的接收結果要在下一階段取得。</p>
<p>§8.4.1 把 recovered eye（恢復眼圖）定義在接收判決輸入。2.5／5.0 GT/s 對應 Rx pins；8.0、16.0、32.0、64.0 GT/s 則對應套用行為接收等化後的 die pad 訊號。較高速率的這個位置無法直接探測，規格因此用量測加模型建立等效眼圖。</p>
<p>本章接著示範 16.0 GT/s。前章已說明差分電壓與量測參考點，這裡只保留接收測試需要的背景，再把校準通道、模型眼圖與 DUT 測試接起來。</p>
<p class="source-note">Base 6.0 §8.4.1 <em>Receiver Stressed Eye Specification</em>（p.1357）；§8.4.2.1 <em>Procedure for Calibrating a Stressed EH/EW Eye</em>（pp.1376–1379）；§8.4.2.2 <em>Procedure for Testing Rx DUT</em>（p.1382 起）。</p></section>

<section id="rx-calibration"><h2>16.0 GT/s Endpoint：從通道選表到 DUT 測試</h2>
<div class="example"><p><strong>【模擬資料】以下資料為教學用途建立，不代表特定硬體或平台。</strong>待測元件是一個支援 32.0 GT/s 的 Endpoint，本次測它的一條 Rx Lane，速率設為 16.0 GT/s，採 Common Refclk（共同參考時脈，以下簡稱 CC）。訊號由測試來源送入 Endpoint；通道與眼圖讀值均為作者建立。</p>
<h3>第一步：依接收元件類型選 Table 8-8 的列</h3>
<p>先到 §8.4.1.2，找 Table 8-8 的 <em>16.0 GT/s Non-Root Port</em> 列。選列依據是待測 Endpoint 的類型，不是圖樣產生器的位置。這列在 1 GHz 的校準通道損耗範圍是 4.2–5.2 dB，8 GHz 則是 24.5–25.5 dB；Root Port 在 8 GHz 的條目不同。</p>
<div class="table-wrap"><table><thead><tr><th scope="col">頻率</th><th scope="col">假設 SDD21 讀值</th><th scope="col">以正值表示的損耗</th><th scope="col">本例選列的名目範圍</th></tr></thead><tbody><tr><td>1 GHz</td><td>−4.7 dB</td><td>4.7 dB</td><td>4.2–5.2 dB</td></tr><tr><td>8 GHz</td><td>−25.0 dB</td><td>25.0 dB</td><td>24.5–25.5 dB</td></tr></tbody></table></div>
<p>SDD21 表示差分輸入到差分輸出的傳輸特性；本例以負 dB 記錄衰減，而表格以正值列損耗。兩個取樣點落在名目範圍內，但還要核對完整遮罩、回波損耗與通道條件。Figure 8-27 是 8.0 GT/s 的示例，讀它的頻率軸、損耗軸與邊界讀法即可；本例的數值要回到 16.0 GT/s 那一列。</p>
<p>§8.4.1.2 另要求 16.0／32.0／64.0 GT/s 的校準通道提供一系列損耗選項，範圍至少從高頻名目下限再少 2 dB，到高頻名目上限再多 3 dB。因此本例至少涵蓋 <code>22.5–28.5 dB</code>，相鄰選項差不得超過 <code>0.5 dB</code>。這些選項供後續調整壓力使用；單獨量到 25 dB 還沒有完成整個眼圖校準。</p>
<h3>第二步：沿 Figure 8-26 區分 TP2 與 TP2P</h3>
<p>先沿上方校準路徑，從來源經校準通道、Replica Channel（重現引出通道特性的參考通道）到 TP2。TP2 是可量測的資料；後處理再加入 behavioral Rx package（行為接收封裝模型）、Rx equalization 與 CDR（Clock and Data Recovery，時脈與資料恢復）模型，才建立 TP2P 的等效恢復眼圖。這些模型不表示 DUT 內部必須使用相同電路。</p>
<p>再看下方測試路徑：校準完成後，纜線改接到實際 DUT 的 Breakout Channel，最後讀 DUT 的 BER（Bit Error Rate，位元錯誤率）結果。上方的封裝與等化模型不是串在 DUT 後面的實體元件，也不能再重複加到實測 BER 上。</p>
<p><strong>損耗參考點要分欄記錄。</strong>§8.4.1.2 以 TP3 到 TP2 描述校準通道的 SDD21；§8.4.2.1 又特別說明，16.0 GT/s 的總通道損耗保留將 TP1–TP3 纜線計入的既有測法，32.0／64.0 GT/s 則把該纜線視為產生器的一部分。前表只帶讀通道名目條目的兩個頻點，不是後續每一步總損耗的替代值。</p>
<h3>第三步：從 Table 8-10 找目標，再讀 Note 4 與 Note 8</h3>
<p>選 16.0 GT/s 欄：<code>TRX-UI=62.5 ps</code>、目標眼寬 <code>TRX-ST=0.30 UI</code>、目標眼高 <code>VRX-ST=15 mVPP</code>。EH 是 Eye Height（眼高），EW 是 Eye Width（眼寬）；所以本例的名目眼寬為 <code>0.30 × 62.5 = 18.75 ps</code>。</p>
<p>Note 4 指定這些目標參照 TP2P，不能拿 TP2 的原始開口直接比較。Note 8 則要求校準 EH／EW 時關閉共模干擾，完成後在 stressed-eye jitter test 再開啟。本例的 <code>VRX-CM-INT</code> 是 120 MHz、150 mVPP 的單音共模干擾，且依 Note 8 在 TP2 量測、不作後處理；因此，校準紀錄與測試紀錄要各自保留共模干擾的開關狀態與幅度。</p>
<p>接著讀 §8.4.2.1 的 16.0 GT/s 步驟：先以適用的壓力設定與通道開始，依模型眼圖選 Tx preset（預先定義的等化組合），逐步增加通道損耗，再依規則重選 preset、調整 Sj（Sinusoidal Jitter，正弦抖動）、差分干擾與擺幅，取得合法的最後組合。Figure 8-42 把這些調整位置畫在來源、通道與後處理旁；閱讀時要把每個箭頭連回它實際改變的條件。</p>
<h3>第四步：多次量測的平均值，確認的是校準視窗</h3>
<p>假設其餘校準步驟與工具要求均已按本次條件完成，下面只摘出同一個最終設定的五次 TP2P 結果，均為後處理模型在 10<sup>−12</sup> BER 對應條件下的眼圖；實際 DUT 錯誤率另於第五步測試。§8.4.2.1 要求至少五次量測，實際次數還要足以得到穩定值；16.0 GT/s 的最終平均眼高容許 15 ± 1.5 mV，平均眼寬容許 18.75 ± 0.5 ps。</p>
<div class="table-wrap"><table><thead><tr><th scope="col">校準量</th><th scope="col">五次假設讀值</th><th scope="col">平均值</th><th scope="col">最終平均值視窗</th></tr></thead><tbody><tr data-rx-check="eh"><td>EH</td><td>14.5, 15.0, 15.5, 15.2, 14.8 mVPP</td><td>15 mVPP</td><td>13.5–16.5 mVPP</td></tr><tr data-rx-check="ew"><td>EW</td><td>18.5, 18.8, 18.9, 18.6, 18.95 ps</td><td>18.75 ps</td><td>18.25–19.25 ps</td></tr></tbody></table></div>
<p>兩個平均值均符合最後視窗。在通道、壓力與 preset 選擇等校準步驟也完成的前提下，這組設定可接著用於 DUT 測試。若平均值不符，就先調整測試壓力再量；這一步處理的是測試訊號，尚未取得 Endpoint 的接收結果。</p>
<figure class="diagram"><svg viewBox="0 0 900 660" style="min-width:640px" role="img" aria-labelledby="rx-calibration-title rx-calibration-desc"><title id="rx-calibration-title">先校準測試訊號，再接上 DUT 測試</title><desc id="rx-calibration-desc">TP2資料經接收封裝、等化與CDR模型得到TP2P眼圖。合法校準後才改接DUT測BER；校準不符則調整壓力條件再校準。</desc><text x="450" y="32" text-anchor="middle" font-size="21">A．先校準要施加的壓力訊號</text><rect x="210" y="55" width="480" height="75" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="450" y="84" text-anchor="middle" font-size="18">來源 → 通道＋Replica → TP2</text><text x="450" y="110" text-anchor="middle" font-size="17"></text><rect x="210" y="155" width="480" height="75" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="450" y="184" text-anchor="middle" font-size="18">Rx 封裝＋行為等化／CDR 模型</text><text x="450" y="210" text-anchor="middle" font-size="17">TP2P：校準後的 EH／EW</text><rect x="210" y="470" width="480" height="75" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="450" y="499" text-anchor="middle" font-size="18">來源 → 通道＋Breakout → Rx DUT</text><text x="450" y="525" text-anchor="middle" font-size="17">鎖定、必要干擾與 Sj 掃頻條件</text><polygon points="450,265 630,330 450,395 270,330" fill="var(--surface-alt)" stroke="var(--line)"/><text x="450" y="337" text-anchor="middle" font-size="18">校準條件成立？</text><path d="M630 330 H810 V92 H690" stroke="var(--accent)" stroke-width="2" fill="none"/><polygon points="690,92 700,87 700,97" fill="var(--accent)"/><text x="725" y="365" text-anchor="middle" font-size="16">否：調整壓力與損耗</text><text x="470" y="420" font-size="16">是：改接纜線</text><text x="450" y="455" text-anchor="middle" font-size="21">B．再測實際接收器</text><text x="450" y="610" text-anchor="middle" font-size="19">依完整測試條件取得 BER 結果</text><path d="M450 130 V155" stroke="var(--accent)" stroke-width="2" fill="none"/><polygon points="450,155 445,145 455,145" fill="var(--accent)"/><path d="M450 230 V265" stroke="var(--accent)" stroke-width="2" fill="none"/><polygon points="450,265 445,255 455,255" fill="var(--accent)"/><path d="M450 395 V435" stroke="var(--accent)" stroke-width="2" fill="none"/><polygon points="450,435 445,425 455,425" fill="var(--accent)"/><path d="M450 545 V580" stroke="var(--accent)" stroke-width="2" fill="none"/><polygon points="450,580 445,570 455,570" fill="var(--accent)"/></svg><figcaption>作者依校準與測試階段整理的流程圖。Replica 校準路徑與 Breakout／DUT 測試路徑在不同階段使用；圖中沒有把模型當成實際接收器的一段電路。</figcaption></figure>
<h3>第五步：改接 DUT 後，再確認接收結果與掃頻範圍</h3>
<p>§8.4.2.2.1 要求 BERT（Bit Error Rate Tester，位元錯誤率測試器）的 Tx 使用 Modified Compliance Pattern。校準時固定的 Tx preset，進入 DUT 測試後可依規則調整，讓實際接收器取得較好的眼圖餘裕；共模干擾等測試條件也須切換到測試階段的設定。依 §8.4.2，測 Rx 時 DUT 的其他 PCIe Lanes 須收送資料；其他 I/O 的活動則是建議，兩者的要求強度不同。</p>
<p>本例採 16.0 GT/s、CC，且元件支援 32.0 GT/s，因此沿 Figure 8-45 查 Sj mask。先看橫軸頻率與縱軸 Sj 幅度（單位是 UI），再讀 §8.4.2.2.1：CDR 初始鎖定後須按適用規則改為掃頻條件；33 kHz 必須測試，並不是在其他掃頻測點持續疊加的背景 tone。16.0 GT/s 的 210 MHz 附加 tone，幅度取校準時 100 MHz Sj 幅度減去 0.1 UI；若校準 Sj 低於 0.1 UI，則不加這個 tone。這項設定要從校準紀錄帶入，不能只留下最後 EH／EW。</p>
<p>假設 DUT 報告只留下「CDR 已鎖定」及「某個掃頻測點未觀察到錯誤」。目前仍缺測試量、錯誤計數、其他所選頻點與完整壓力條件。16.0 GT/s 的目標是適用掃頻範圍內 BER 符合 <code>10<sup>−12</sup></code>；規格不要求逐一測遍連續頻率，但應選足夠測點以涵蓋可能的共振失敗，且 33 kHz 是明確必測點。單一零錯誤摘要還不足以完成這項判定。</p></div>
<p class="source-note">Base 6.0 §§8.4.1.1–8.4.1.2、Figure 8-26 <em>Rx Test board Topology for 16.0 and 32.0 GT/s</em>、Table 8-8 <em>Calibration Channel IL Limits</em>（pp.1357–1361）；§8.4.2.1、Figure 8-42 <em>Layout for Calibrating the Stressed Jitter Eye at 16.0, 32.0, and 64.0 GT/s</em>（pp.1376–1379）；Table 8-10 <em>Stressed Jitter Eye Parameters</em>、Notes 4／8（p.1380）；§8.4.2.2.1 <em>Sj Mask</em>（pp.1382–1385）、Figure 8-45（p.1385）。</p></section>

<section id="channel"><h2>校準通道、實際平台通道與外形規格，怎麼接起來？</h2>
<p>前面的校準通道用來產生接收測試的壓力；平台通道是否合格，還要按 §8.5.1 的範圍判讀。Captive channel 指平台設計涵蓋 Tx pin 到 Rx pin 的整段通道。若設計由不同板卡或元件分擔，須接上適用的 form-factor specification；CEM 是一個例子，該分工情境由外形規格優先定義。本章沒有用未提供的外形規格補上板卡數值。</p>
<p>沿 Figure 8-56／8-57，先取得通道特性，再加入 Tx／Rx 的行為封裝模型，成為 die pad 到 die pad 的拓撲；模型還須包含受干擾路徑與足夠的串擾來源。最後套用適用的發送條件、接收等化及時脈恢復，才看接收判決位置的眼圖。</p>
<p>Figure 8-57 的正式標題只列 8.0 與 16.0 GT/s；鄰近文字才進一步列出 32.0／64.0 GT/s 的模型要求。以本例 16.0 GT/s 為例，通道模擬使用 first-order CTLE（連續時間線性等化器）與 two-tap DFE（兩個抽頭的判決回授等化器）作最低能力模型。這是規格的驗證模型，不是指定 DUT 的電路結構；也不能把前章的 Tx 測試通道直接當成本章的 Rx 校準通道。</p>
<p class="source-note">Base 6.0 §8.5.1 <em>Channel Compliance Testing</em>（pp.1400–1402）；Figure 8-56 <em>Flow Diagram for Channel Tolerancing at 2.5 and 5.0 GT/s</em>、Figure 8-57 <em>Flow Diagram for Channel Tolerancing at 8.0 and 16.0 GT/s</em>（p.1401）；§8.5.1.1 <em>Behavioral Transmitter and Receiver Package Models</em>（p.1402 起）。</p></section>

<section id="clock"><h2>共同時脈會改變哪些觀察條件？</h2>
<p>Refclk（Reference Clock，參考時脈）不只是示意圖的一條連線。§8.6.6 的 Common Refclk 架構把同一來源分配給 Tx 與 Rx，部分低頻變動會共同傳遞；最後到接收判決位置的相對時序，還受 Tx／Rx PLL（Phase-Locked Loop，鎖相迴路）、CDR 與傳輸延遲差影響。</p>
<p>讀 Figure 8-89 時，先找共同來源分到兩端的路徑，再找 Tx 資料路徑與 Rx 取樣時脈路徑的差異。§8.6.5 又把後處理分成兩類：edge filtering 減少量測取樣造成的誤差；另一類用行為模型描述 PLL、CDR 與適用的 transport delay。這些濾波組合得到判決位置的有效 Refclk jitter，不是把所有原始 jitter 直接相加。</p>
<p>§8.6.4 在此沒有為 Independent Refclk（IR，獨立參考時脈）定義相同的 Refclk 傳遞函數與對應 jitter limits；這不表示 IR 沒有其他發送或接收要求。本例若改為 IR，就要重新選 Sj profile 與適用模型，不能沿用 CC 的 Figure 8-45。前章 <a href="/DOCS/pcie-course/chapter-20.html#clock-route">Chapter 20</a> 已帶讀 Tx 的時脈取樣選表，本章不重複那套流程。</p>
<p>§8.6.1 的 Refclk 測試對象是時脈來源，本節的 DUT 測試對象則是 Rx；兩種測試的參考點與結果應分開保存。只有各自的條件齊全，才能把時脈、通道與接收結果串成同一條分析路徑。</p>
<p class="source-note">Base 6.0 §8.6.1 <em>Refclk Test Setup</em>（p.1420）；§8.6.4 <em>Refclk Architectures Supported</em>、§8.6.5 <em>Filtering Functions Applied to Raw Data</em>（p.1426）；§8.6.6 <em>Common Refclk Rx Architecture (CC)</em>、Figure 8-89 <em>Common Refclk Rx Architecture for all Data Rates Except 32.0 and 64.0 GT/s</em>（p.1428）。</p></section>

<section id="sources"><h2>版本與來源</h2><p>本章以 PCI Express Base Specification Revision 6.0（6.0-1.0-PUB）為準，所列印刷頁碼與 PDF 檢視器頁碼相同。案例讀值、假設與階段摘錄均為作者建立，不是實測報告或合規證明。</p><details class="source-note"><summary>本章閱讀位置與用途</summary><ul><li>§8.4.1（p.1357）：各速率 recovered-eye 參考點；§§8.4.1.1–8.4.1.2、Figure 8-26、Figure 8-27 <em>Example Calibration Channel IL Mask Excluding Rx Package for 8.0 GT/s</em>、Table 8-8（pp.1357–1361）：校準通道與量測位置。</li><li>§8.4.2 <em>Stressed Eye Test</em>、§8.4.2.1（pp.1376–1379）：來源、通道、preset 與壓力調整；16.0 GT/s 的最後平均值視窗見 p.1377，纜線計入方式見 p.1376。</li><li>Table 8-10（pp.1380–1381）：目標、單位與 Note 4／8 的參考點及共模切換；§8.4.2.1.1 <em>Post Processing Tool Requirements</em>（p.1381）：校準工具一致性要求。</li><li>§8.4.2.2、§8.4.2.2.1（pp.1382–1385）：DUT 的圖樣、鎖定與 Sj 測試；Figure 8-45 <em>Sj Mask for Receivers Operating in CC mode at 16.0 GT/s</em>（p.1385）。</li><li>§8.5.1、Figures 8-56／8-57（pp.1400–1402）：平台通道與最低能力模型；§8.6.1、§§8.6.4–8.6.6、Figure 8-89（pp.1420、1426–1428）：Refclk 測試、架構與濾波。</li></ul></details></section>
</article>
<nav class="bottom-nav" aria-label="課程與語言版本"><a href="/DOCS/pcie-course/index.html">課程總覽</a><a href="/DOCS/pcie-course/chapter-21.html">繁中完整教學</a><a href="/pcie/chapter-21-en/">English</a></nav>
</div>
