---
layout: post
title: "PCIe Chapter 19：LTSSM、Equalization 與 Retimer"
date: 2026-10-24 00:00:00 +0800
last_modified_at: 2026-10-29 00:00:00 +0800
permalink: /pcie/chapter-19-zh-tw/
categories: [PCIe]
tags: [PCIe, Specification]
lang: zh-TW
spec_teaching: true
spec_series: pcie
description: "Link 還沒到正常傳送狀態，應該追哪個階段？"
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
<nav class="bottom-nav" aria-label="課程與語言版本"><a href="/DOCS/pcie-course/index.html">課程總覽</a><a href="/DOCS/pcie-course/chapter-19.html">繁中完整教學</a><a href="/pcie/chapter-19-en/">English</a></nav>
<article class="lesson">
<p>LTSSM（Link Training and Status State Machine，鏈結訓練與狀態機）描述 Link 的偵測、訓練與運作。本章先讀正常路徑，再用 Polling 案例把狀態箭頭接上收發紀錄、計數及 Timeout；Retimer 與升速則按各自的適用條件接著看。</p><figure class="diagram"><svg viewBox="0 0 900 430" style="min-width:640px" role="img" aria-labelledby="ch19-zh-t ch19-zh-d"><title id="ch19-zh-t">LTSSM 初次訓練與返回 L0</title><desc id="ch19-zh-d">初次訓練的部分路徑，以及L0經Recovery返回L0的分支；省略其他分支。</desc><g data-walk-target="detect"><rect x="20" y="35" width="190" height="74" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="115.0" y="64" text-anchor="middle" font-size="16">Detect</text><text x="115.0" y="88" text-anchor="middle" font-size="16">偵測遠端終端</text></g><g data-walk-target="poll"><rect x="300" y="35" width="250" height="74" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="425.0" y="64" text-anchor="middle" font-size="16">Polling</text><text x="425.0" y="88" text-anchor="middle" font-size="16">交換訓練序列</text></g><g data-walk-target="config"><rect x="630" y="35" width="250" height="74" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="755.0" y="64" text-anchor="middle" font-size="16">Configuration</text><text x="755.0" y="88" text-anchor="middle" font-size="16">協商 Lane 與寬度</text></g><g data-walk-target="recovery"><rect x="220" y="290" width="310" height="74" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="375.0" y="319" text-anchor="middle" font-size="16">Recovery</text><text x="375.0" y="343" text-anchor="middle" font-size="16">重建鎖定、對齊或變速</text></g><g data-walk-target="l0"><rect x="630" y="290" width="250" height="74" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="755.0" y="319" text-anchor="middle" font-size="16">L0：正常操作</text><text x="755.0" y="343" text-anchor="middle" font-size="16"></text></g><g data-walk-target="a"><path d="M210 72 H300" fill="none" stroke="var(--accent)" stroke-width="2"/><polygon points="300,72 290,67 290,77" fill="var(--accent)"/><text x="255" y="60" text-anchor="middle" font-size="16"></text></g><g data-walk-target="b"><path d="M550 72 H630" fill="none" stroke="var(--accent)" stroke-width="2"/><polygon points="630,72 620,67 620,77" fill="var(--accent)"/><text x="590" y="60" text-anchor="middle" font-size="16"></text></g><g data-walk-target="c"><path d="M755 109 V290" fill="none" stroke="var(--accent)" stroke-width="2"/><polygon points="755,290 750,280 760,280" fill="var(--accent)"/><text x="805" y="205" text-anchor="middle" font-size="16">完成訓練</text></g><g data-walk-target="d"><path d="M630 315 H530" fill="none" stroke="var(--accent)" stroke-width="2"/><polygon points="530,315 540,310 540,320" fill="var(--accent)"/><text x="580" y="300" text-anchor="middle" font-size="16">觸發</text></g><g data-walk-target="e"><path d="M530 347 H630" fill="none" stroke="var(--accent)" stroke-width="2"/><polygon points="630,347 620,342 620,352" fill="var(--accent)"/><text x="580" y="378" text-anchor="middle" font-size="16">恢復</text></g></svg><figcaption><p>主狀態用來定位進度，箭頭沒有代替子狀態的接收、計數與 Timeout 規則。L0 之後仍要分開確認 Data Link 與 Transaction 結果。</p></figcaption></figure>
<section id="route"><h2>先找到狀態，再找轉換條件</h2>
<p>讀 LTSSM（Link Training and Status State Machine，鏈結訓練與狀態機）紀錄時，先確認是哪一端的 Port、哪條 Link，以及資料記錄的方向與時間。Figure 4-48 用來定位主狀態；§4.2.6 解釋各狀態要完成的工作；§4.2.7 才定義子狀態的動作、接收條件與 Timeout。三者要接著讀。</p>
<p>本章選初次建立 Link 的 Polling 作完整示範。先查 Figure 4-49，確認 Receiver Detection（接收端終端偵測）之後如何進入 Polling；再放大 Figure 4-50，沿正常路徑讀 Polling.Active 與 Polling.Configuration。後節再接到速度提升、Equalization 與 Retimer，說明分析範圍如何隨情境改變。</p>
<p class="source-note">Base 6.0 §4.2.6 <em>Link Training and Status State Machine (LTSSM) Descriptions</em>（pp.444–452）；§4.2.7 <em>Link Training and Status State Rules</em>、Figure 4-48 <em>Main State Diagram for Link Training and Status State Machine</em>（pp.452–454）；Figure 4-49 <em>Detect Substate Machine</em>（p.456）、Figure 4-50 <em>Polling Substate Machine</em>（p.464）。</p></section>

<section id="polling-gates"><h2>看到 TS1 或 TS2，還差哪些條件才能前進？</h2>
<p><strong>一次收到正確序列，只代表那次接收有效；轉換條件還包含連續接收、傳送數量與 Lane 範圍。</strong>TS1、TS2 是 Training Sequence Ordered Sets（訓練用的有序符號組），兩端各自送出，也各自檢查收到的內容。</p>
<div class="example"><p><strong>【模擬資料】以下資料為教學用途建立，不代表特定硬體或平台。</strong>Root Port 00:01.0 與 Endpoint 01:00.0 直接相連，沒有 Retimer。本次觀察 Root Port 的 LTSSM 與收發紀錄，初次訓練使用 2.5 GT/s、8b/10b；Detect 已在兩條候選 Lane 上偵測到 Receiver。以下暫稱 Lane A、Lane B，它們是工具已配對的接線通道，尚不是 Configuration 分配完成的 Logical Lane Number。</p>
<p>假設 Enter Compliance=0，沒有 Loopback 或 Compliance 測試要求。接收的 TS1 均以 PAD 填入 Link Number 與 Lane Number，Compliance Receive=0；本例也不涉及極性反轉。PAD 是尚未指派編號時使用的填充值，不是 Lane 0。所有下列觀察都在所屬子狀態的 Timeout 到期之前。</p>
<h3>第一步：Polling.Active 同時看本端傳送量與每條 Lane 的接收</h3>
<p>Root Port 在 Polling.Active 持續送出 TS1。依 p.457 的正常轉換路徑，至少要送出 1024 組 TS1，而且 Detect 曾偵測到 Receiver 的所有 Lane，都須連續收到八組符合條件的訓練序列。這裡的 1024 是本端傳送量，八組則是各 Lane 的接收條件，不能把兩個方向的數量相加。</p>
<div class="table-wrap"><table><thead><tr><th scope="col">同一次 Polling.Active 的時點</th><th scope="col">本端已送 TS1</th><th scope="col">Lane A 連續合格接收</th><th scope="col">Lane B 連續合格接收</th><th scope="col">依本例正常路徑的依本例條件的下一狀態</th></tr></thead><tbody>
<tr data-polling-stage="active-early"><td>A0</td><td>1000</td><td>8</td><td>7</td><td>Polling.Active</td></tr><tr data-polling-stage="active-tx"><td>A1</td><td>1023</td><td>31</td><td>30</td><td>Polling.Active</td></tr><tr data-polling-stage="active-ready"><td>A2</td><td>1024</td><td>32</td><td>31</td><td>Polling.Configuration</td></tr>
</tbody></table></div><p>A0 的兩項條件都還不完整。到了 A1，兩條 Lane 的連續接收都已足夠，但本端仍少送一組 TS1；A2 才同時滿足。數字是工具依完整紀錄整理出的接收次數，不是規格要求公開的 Configuration Register。</p>
<h3>第二步：Polling.Configuration 的傳送計數有新的起點</h3>
<p>Root Port 進入 Polling.Configuration 後改送 TS2，Link Number 與 Lane Number 仍為 PAD。接著查 §4.2.7.2.3：在 Detect 曾偵測到 Receiver 的 Lane 上，收到八組連續 TS2，並且<strong>從收到第一組 TS2 之後，再送出 16 組 TS2</strong>，才能前進到 Configuration。本例 Lane A、Lane B 都已連續收到八組，接收條件成立；接著核對首次接收後的傳送數量。</p>
<div class="table-wrap"><table><thead><tr><th scope="col">同一次 Polling.Configuration 的時點</th><th scope="col">首次收到 TS2 前已送</th><th scope="col">首次收到 TS2 後已送</th><th scope="col">本端 TS2 合計</th><th scope="col">Lane A／B 連續收到 TS2</th><th scope="col">依本例條件的下一狀態</th></tr></thead><tbody>
<tr data-polling-stage="config-wait"><td>B0</td><td>6</td><td>15</td><td>21</td><td>8 / 8</td><td>Polling.Configuration</td></tr><tr data-polling-stage="config-ready"><td>B1</td><td>6</td><td>16</td><td>22</td><td>9 / 9</td><td>Configuration</td></tr>
</tbody></table></div><p>B0 雖然總共送過 21 組 TS2，但符合本次起算條件的只有 15 組；要等到 B1 才足夠。分析工具若只顯示「TS2 共 21 組」，還得找出首次收到 TS2 的位置，才能判斷這一條規則。</p>
<figure class="diagram"><svg viewBox="0 0 900 690" style="min-width:640px" role="img" aria-labelledby="polling-gates-title polling-gates-desc"><title id="polling-gates-title">Polling 正常路徑的轉換條件</title><desc id="polling-gates-desc">等待迴圈僅適用尚未Timeout時；Timeout分支見後方表格。</desc><rect x="260" y="35" width="380" height="60" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="450" y="73" text-anchor="middle" font-size="20">Polling.Active</text><rect x="260" y="300" width="380" height="60" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="450" y="338" text-anchor="middle" font-size="20">Polling.Configuration</text><rect x="260" y="610" width="380" height="60" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="450" y="648" text-anchor="middle" font-size="20">Configuration</text><polygon points="450,120 635,190 450,260 265,190" fill="var(--surface-alt)" stroke="var(--line)"/><text x="450" y="182" text-anchor="middle" font-size="16">已送滿 1024 TS1，且各 Lane</text><text x="450" y="208" text-anchor="middle" font-size="16">連續接收條件都成立？</text><path d="M635 190 H790 V65 H640" fill="none" stroke="var(--accent)" stroke-width="2"/><polygon points="640,65 650,60 650,70" fill="var(--accent)"/><text x="710" y="230" text-anchor="middle" font-size="16">否：持續送 TS1</text><polygon points="450,420 635,490 450,560 265,490" fill="var(--surface-alt)" stroke="var(--line)"/><text x="450" y="482" text-anchor="middle" font-size="16">連續收到 8 TS2，且自首次</text><text x="450" y="508" text-anchor="middle" font-size="16">收到 TS2 後已送滿 16 TS2？</text><path d="M635 490 H790 V330 H640" fill="none" stroke="var(--accent)" stroke-width="2"/><polygon points="640,330 650,325 650,335" fill="var(--accent)"/><text x="710" y="530" text-anchor="middle" font-size="16">否：持續送 TS2</text><path d="M450 95 V120" fill="none" stroke="var(--accent)" stroke-width="2"/><polygon points="450,120 445,110 455,110" fill="var(--accent)"/><path d="M450 260 V300" fill="none" stroke="var(--accent)" stroke-width="2"/><polygon points="450,300 445,290 455,290" fill="var(--accent)"/><path d="M450 360 V420" fill="none" stroke="var(--accent)" stroke-width="2"/><polygon points="450,420 445,410 455,410" fill="var(--accent)"/><path d="M450 560 V610" fill="none" stroke="var(--accent)" stroke-width="2"/><polygon points="450,610 445,600 455,600" fill="var(--accent)"/><text x="475" y="286" font-size="16">是</text><text x="475" y="593" font-size="16">是</text></svg><figcaption>作者依正常路徑繪製的條件圖；等待迴圈僅適用尚未 Timeout 的情況。Active 的接收條件依前文案例選用，完整可接受序列及 Timeout 分支仍須查 §4.2.7.2.1；此圖不是完整 LTSSM。</figcaption></figure>
<h3>到了 Configuration，哪些工作仍未完成？</h3>
<p>B1 只把本端推進 Configuration。後續還要依 Figure 4-51（p.482）的 Linkwidth 與 Lanenum 子狀態建立 Link Number、Logical Lane Number 與寬度，並完成後續訓練，才會到 L0。兩條候選 Lane 都通過 Polling，也還沒有直接決定最後必為 x2。先前的 <a href="/DOCS/pcie-course/chapter-8.html">Chapter 8</a> 說明了 Link 能力與目前結果如何分開；L0 之後的 Data Link 與 Flow Control 初始化則接到 <a href="/DOCS/pcie-course/chapter-17.html#initialization">Chapter 17</a>。</p></div>
<p class="source-note">Base 6.0 §4.2.7.1.2 <em>Detect.Active</em>（p.456）；§4.2.7.2.1 <em>Polling.Active</em>（pp.457–458）；§4.2.7.2.3 <em>Polling.Configuration</em>、§4.2.7.2.4 <em>Polling.Speed</em>（p.463）；Figure 4-50（p.464）；§4.2.7.3 <em>Configuration</em>（p.464 起）。</p></section>

<section id="timeouts"><h2>等待超時後，並非一律返回 Detect</h2>
<p>先前的案例只走正常轉換。若遲遲無法前進，就要分開查每個子狀態的 Timeout 規則，不能沿用一個共同的「失敗」箭頭。</p>
<div class="table-wrap"><table><thead><tr><th scope="col">目前位置</th><th scope="col">規格的 Timeout 或條件</th><th scope="col">接著查什麼</th></tr></thead><tbody>
<tr><td>Detect.Active，只有部分 Lane 偵測到 Receiver</td><td>等待 12 ms，再次執行 Receiver Detection</td><td>兩次是否恰好相同 Lane 成功；相同才可走向 Polling，不同則回 Detect.Quiet</td></tr>
<tr><td>Polling.Active</td><td>24 ms Timeout，另有部分 Lane 可前進的條件</td><td>至少一條 Lane 連續收到八組合格序列、首次收到 TS1／TS2 後已再送出至少 1024 組 TS1，以及預先指定 Lane 集合是否曾退出 Electrical Idle；符合規則可到 Polling.Configuration，其他條件可能到 Polling.Compliance 或 Detect</td></tr>
<tr><td>Polling.Configuration</td><td>48 ms Timeout 前仍未滿足轉換條件</td><td>到期後回 Detect；原本缺的是連續接收，還是首次接收後的傳送量，須由紀錄分開確認</td></tr>
</tbody></table></div>
<p>§4.2.6 的通則給 LTSSM Timeout「不得提早、最多延後 50%」的容許範圍，除非該處另有明文。因此，24 ms 與 48 ms 是規格標稱值，對應上限分別為 36 ms 與 72 ms；不能要求所有實作都恰好在第 24.000 ms 或 48.000 ms 轉移。分析前仍要確認 Timer 的起點、觀察時間及資料是否連續。</p>
<p>Polling.Active 的 Timeout 分支使用「至少一條」及 implementation-specific 的預定 Lane 集合，和正常路徑的「所有偵測成功 Lane」不同。這是規格容許進一步訓練的分支，不足以指出哪條 Lane 已損壞。Polling.Compliance 則還可能由 Enter Compliance 或指定的訓練控制條件觸發；實際進入原因要回查控制與序列內容。</p>
<p class="source-note">Base 6.0 §4.2.6（p.444，Timeout 容許範圍）；§4.2.7.1.2（p.456）；§4.2.7.2.1（pp.457–458）；§4.2.7.2.3（p.463）。</p></section>

<section id="status-map"><h2>為什麼正在 Polling，Link Training 卻是零？</h2>
<p>Link Status Register 的 Link Training bit 只描述特定狀態，並不是完整 LTSSM 的縮寫。本例讀 Root Port 的這個 bit；Endpoint、Switch Upstream Port 與 PCI Express to PCI/PCI-X Bridge 的此欄位不適用，必須固定為零。</p>
<div class="table-wrap"><table><thead><tr><th scope="col">本例 Root Port 的進度</th><th scope="col">Link Training</th><th scope="col">解讀方式</th></tr></thead><tbody><tr><td>Polling</td><td>0</td><td>仍在交換訓練序列；零值不表示已進入 L0</td></tr><tr><td>初次 Configuration</td><td>1</td><td>已離開 Polling，正在處理寬度、Lane 與後續訓練</td></tr><tr><td>L0</td><td>0</td><td>須結合其他狀態與歷史，才知道這次零值是在訓練前還是訓練後</td></tr></tbody></table></div>
<p>先用 Table 4-48 把狀態對應到 bit，再回 Table 7-26 看欄位適用性。Table 4-48 的 LinkUp 是 Physical Layer 給 Data Link Layer 的狀態，和 Link Status 的 Data Link Layer Link Active 不同；後者還須確認回報能力與 DL_Active。相關跨層狀態在 <a href="/DOCS/pcie-course/chapter-8.html">Chapter 8</a> 與 <a href="/DOCS/pcie-course/chapter-17.html#initialization">Chapter 17</a> 已完整說明。</p>
<p class="source-note">Base 6.0 Table 4-48 <em>Link Status Mapped to the LTSSM</em>（p.453）；§7.5.3.8、Figure 7-29、Table 7-26 <em>Link Status Register</em>（pp.978–979）。</p></section>

<section id="equalization"><h2>升速時，再沿 Recovery 追到 Equalization</h2>
<p>初次 Link 先以 2.5 GT/s 到 L0，即使兩端都支援更高速率也是如此；之後可從 L0 進 Recovery 改變速度。Polling 中宣告的高速度能力，不代表當時已用該速度傳輸。§4.2.7.2.4 也明確指出 Polling.Speed 不可達，不要把它補進初次升速路徑。</p>
<p>Equalization（等化，調整每條 Lane 的發送與接收設定以補償通道影響）有速率相關的流程。§4.2.4 要求第一次切換到各個 8.0 GT/s 以上速率時執行適用程序，但另定義了所有元件共同支援與宣告後可採用的略過機制。這裡先分清一般程序、略過到最高 NRZ 速率，以及 No Equalization Needed；不可因某端宣告一個 bit，就替整條路徑省略訓練。</p><dl class="st-terms" aria-label="本段名詞"><div><dt>NRZ</dt><dd>Non-Return-to-Zero，不歸零編碼</dd></div></dl>
<p>升速紀錄需要接起「哪一端提出變更、進了哪些 Recovery 子狀態、適用的等化流程、最後速度與寬度」。<a href="/DOCS/pcie-course/chapter-8.html">Chapter 8</a> 的雙端 Register 與狀態帶讀可作查詢入口。經過 Recovery 也不等於重新列舉或清掉所有 Data Link 狀態，須按實際的 LinkUp 與 Reset 歷史判斷。</p>
<p class="source-note">Base 6.0 §4.2.6.4（p.445）；§4.2.7.2.4 與 p.464 的 <em>Support for Higher Data Rates Than 2.5 GT/s</em> 說明；§4.2.4 <em>Link Equalization Procedure for 8.0 GT/s and Higher Data Rates</em>（pp.392–393）。</p></section>

<section id="retimer"><h2>有 Retimer 時，一條 Link 與電氣區段怎麼分？</h2>
<p>Retimer（重定時器）理解 Physical Layer 協定，並重新建立訊號時序。Figure 4-61 先畫出整條 Link，再把 Retimer 兩側標為 Link Segments。每個 Retimer 有兩個 Pseudo Ports（偽連接埠），朝向會在 Configuration 期間動態確定。</p>
<div class="table-wrap"><table><thead><tr><th scope="col">示意路徑：Root Port → 一個 Retimer → Endpoint</th><th scope="col">角色</th><th scope="col">分析位置</th></tr></thead><tbody><tr><td>Root Port 到 Retimer</td><td>Root Port 的 Downstream Port 對向 Retimer 的 Upstream Pseudo Port</td><td>第一段電氣通道</td></tr><tr><td>Retimer 到 Endpoint</td><td>Retimer 的 Downstream Pseudo Port 對向 Endpoint 的 Upstream Port</td><td>第二段電氣通道</td></tr><tr><td>Root Port 到 Endpoint 整體</td><td>仍是一條 PCIe Link</td><td>Data Link 與 Transaction 不因 Retimer 多出一層 Switch</td></tr></tbody></table></div>
<p>接著查 §4.3.2 的模式：Forwarding mode 轉送適用的符號及 Electrical Idle；Execution mode 則在 Polling.Compliance、等化 Phase 2／3 等指定情境參與協定。追查某一段的等化結果時，要標明 Pseudo Port 與方向，不能用 Root Port 的整體狀態替每一段補出相同結果。</p>
<p>Base 6.0 允許同一條 Link 最多兩個 Retimers，外形規格仍可能加上限制。這些元件對 Data Link 與 Transaction Layer 透明；不能替它們各配置一組 Bridge Bus Number，也不能把分段等化當成多組獨立的 TLP Ack／Replay。電氣品質是否合格，還需要 Chapter 8 的適用要求與實際量測。</p><dl class="st-terms" aria-label="本段名詞"><div><dt>TLP</dt><dd>Transaction Layer Packet，交易層封包</dd></div></dl>
<p class="source-note">Base 6.0 §4.3 <em>Retimers</em>（pp.564–565）；§4.3.2 <em>Supported Retimer Topologies</em>、Figure 4-61 同名圖（pp.566–567）。本節表格是作者整理的拓撲示意。</p></section>

<section id="power"><h2>低功耗與測試分支，另外確認目的與條件</h2>
<p>L0p（L0 內部分 Lane 省電的機制）只用於 Flit Mode，保持對稱的目標寬度，且每方向至少有一條活動 Lane。它不是讓整條 Link 先離開 L0 再重建；轉換期間兩側也可能短暫處於不同寬度。相對地，L0s 是另一種快速省電狀態，在 Flit Mode、有 Retimer，或使用獨立 SSC（Spread Spectrum Clocking，展頻時鐘）的分離參考時鐘時，不得支援與宣告。</p>
<p>Polling.Compliance 用於測試；Loopback 的 Lead 發起測試，Follower 負責回送資料；Hot Reset 用 in-band 訊號重設配置好的 Link 與相關下游裝置。它們在 Figure 4-48 都有各自的分支。分析工具若只留下「沒有 TLP」，仍要補上具體狀態與進入條件，才能分清訓練、低功耗或測試。L1、Function 電源狀態與平台政策則接到 <a href="/DOCS/pcie-course/chapter-9.html">Chapter 9</a>。</p><dl class="st-terms" aria-label="本段名詞"><div><dt>TLP</dt><dd>Transaction Layer Packet，交易層封包</dd></div></dl>
<p class="source-note">Base 6.0 §4.2.6.2（p.444）、§4.2.6.6–4.2.6.7（pp.445–447）、Figure 4-47 的轉換說明（p.450）、§4.2.6.8–4.2.6.12（pp.451–452）。</p></section>

<section id="sources"><h2>版本與來源</h2><p>本章以 PCI Express Base Specification Revision 6.0（6.0-1.0-PUB）為準；上述文件印刷頁碼與 PDF 檢視器頁碼相同。案例的拓撲與計數均由作者建立；工具通道名稱不等同於規格分配的 Lane Number。</p><details class="source-note"><summary>本章閱讀位置與用途</summary><ul><li>§4.2.6（pp.444–452）：各主狀態目的與 Timeout 通則；Table 4-48（p.453）、Figure 4-48（p.454）：狀態與狀態欄位的對照。</li><li>§4.2.7.1.1 <em>Detect.Quiet</em>（p.455）、§4.2.7.1.2 <em>Detect.Active</em>、Figure 4-49（p.456）：偵測與重試分支。</li><li>§4.2.7.2.1 <em>Polling.Active</em>（pp.457–458）、§4.2.7.2.3 <em>Polling.Configuration</em> 與 §4.2.7.2.4 <em>Polling.Speed</em>（p.463）、Figure 4-50（p.464）：本章傳送與連續接收算例。</li><li>§4.2.7.3 <em>Configuration</em>（p.464 起）、Figure 4-51 <em>Configuration Substate Machine</em>（p.482）、§4.2.7.3.1.1 <em>Downstream Lanes</em>（pp.464–465）：Polling 後還須完成寬度與 Lane 配置。</li><li>§7.5.3.8 <em>Link Status Register</em>、Figure 7-29、Table 7-26（pp.978–979）：Link Training 的作用與適用範圍。</li><li>§4.2.4（pp.392–393）：首次等化及略過機制；§4.3、§4.3.2、Figure 4-61（pp.564–567）：Retimer 角色、模式與電氣區段。</li></ul></details></section>
</article>
<nav class="bottom-nav" aria-label="課程與語言版本"><a href="/DOCS/pcie-course/index.html">課程總覽</a><a href="/DOCS/pcie-course/chapter-19.html">繁中完整教學</a><a href="/pcie/chapter-19-en/">English</a></nav>
</div>
