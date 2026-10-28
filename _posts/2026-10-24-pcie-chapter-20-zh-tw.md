---
layout: post
title: "PCIe Chapter 20：發射端電氣條件與量測觀點"
date: 2026-10-24 00:00:00 +0800
last_modified_at: 2026-10-29 00:00:00 +0800
permalink: /pcie/chapter-20-zh-tw/
categories: [PCIe]
tags: [PCIe, Specification]
lang: zh-TW
spec_teaching: true
spec_series: pcie
description: "要判讀發送端電氣規格，為什麼不能先抄一個電壓上限？"
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
<nav class="bottom-nav" aria-label="課程與語言版本"><a href="/DOCS/pcie-course/index.html">課程總覽</a><a href="/DOCS/pcie-course/chapter-20.html">繁中完整教學</a><a href="/pcie/chapter-20-en/">English</a></nav>
<article class="lesson">
<p>Tx（Transmitter，發送端）的電氣數值，必須和量測位置、參考時脈、速率及測試圖樣一起讀。這章從 Figure 8-1 的量測路徑開始，再把電壓、等化與抖動接到適用條件。</p><figure class="diagram"><svg viewBox="0 0 900 420" role="img" aria-labelledby="ch20-zh-t ch20-zh-d"><title id="ch20-zh-t">Tx 量測路徑與參考條件</title><desc id="ch20-zh-d">電氣量測先定義觀察點及時脈，再選相應速率與圖樣。</desc><g data-walk-target="dut"><rect x="20" y="60" width="230" height="44" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="135.0" y="89" text-anchor="middle" font-size="16">Tx：待測發送端</text></g><g data-walk-target="breakout"><rect x="335" y="60" width="230" height="44" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="450.0" y="89" text-anchor="middle" font-size="16">測試板引出通道</text></g><g data-walk-target="scope"><rect x="650" y="60" width="230" height="44" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="765.0" y="89" text-anchor="middle" font-size="16">量測設備：取得波形</text></g><g data-walk-target="ref"><rect x="20" y="290" width="230" height="44" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="135.0" y="319" text-anchor="middle" font-size="16">參考時脈條件</text></g><g data-walk-target="process"><rect x="470" y="290" width="410" height="68" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="675.0" y="319" text-anchor="middle" font-size="16">依參數選擇後處理與參考點</text><text x="675.0" y="343" text-anchor="middle" font-size="16">依參數、單位與註腳判讀</text></g><g data-walk-target="a"><path d="M250 94 L335 94" stroke="var(--accent)" stroke-width="2" fill="none"/><polygon points="335,94 325.0,99.0 325.0,89.0" fill="var(--accent)"/><text x="292.5" y="84.0" text-anchor="middle" font-size="16">訊號</text></g><g data-walk-target="b"><path d="M565 94 L650 94" stroke="var(--accent)" stroke-width="2" fill="none"/><polygon points="650,94 640.0,99.0 640.0,89.0" fill="var(--accent)"/><text x="607.5" y="84.0" text-anchor="middle" font-size="16">波形</text></g><g data-walk-target="c"><path d="M135 290 L135 104" stroke="var(--accent)" stroke-width="2" fill="none"/><polygon points="135,104 140.0,114.0 130.0,114.0" fill="var(--accent)"/><text x="230" y="210" text-anchor="middle" font-size="16">依架構供應</text></g><g data-walk-target="d"><path d="M765 104 L675 290" stroke="var(--accent)" stroke-width="2" fill="none"/><polygon points="675,290 675.4856429311786,278.8302125828915 684.227215692394,283.6866418946778" fill="var(--accent)"/><text x="795" y="210" text-anchor="middle" font-size="16">後處理</text></g></svg><figcaption>作者繪製的量測關係圖；後處理依參數選擇，完整測法與例外須回到條目註記。</figcaption></figure>
<section id="setup"><h2>先把可量到的位置，接回規格的參考點</h2>
<p>Figure 8-1 先看三個位置：DUT（Device Under Test，待測元件）的 Tx pin、板上的 Breakout Channel（把訊號引到接頭的通道），以及可供量測的 TP1。TP1 取得的波形包含這段通道的影響，和元件 pin 的波形不同。</p>
<p>再看同圖的 Replica Channel（用來重現引出通道特性的參考通道），以及它兩端的 TP2、TP3。這條通道用來協助建立 TP1 與元件 pin 的對應，並非 Tx 訊號接著流過的第二條串接路徑。§8.3.1.1 要求按所選參數處理參考點；其原則是電壓參數須還原到 pin，除非該處另有規定。</p>
<p>De-embedding 是依通道特性移除量測路徑影響的後處理。它不是從電壓或 jitter（訊號邊緣或脈寬的時間變化）直接減去一個固定數字。§8.3.5.2 還說明，此處理會放大高頻雜訊，因此須遵守適用的頻率與後處理規則。</p>
<p>讀報告時，先找待測元件與 Lane、速率、full／reduced swing、測試圖樣、參考時脈、量測位置及後處理。若報告只有「TP1 量到多少」，就先補足上述條件，再選參數比較。</p>
<p class="source-note">Base 6.0 §8.3.1 <em>Measurement Setup for Characterizing Transmitters</em>、Figure 8-1 <em>Tx Test Board for Non-Embedded Refclk</em>（p.1318）；§8.3.1.1 <em>Breakout and Replica Channels</em>（pp.1319–1320）；§8.3.5.1–8.3.5.2（pp.1336–1337）。</p></section>

<section id="clock-route"><h2>時脈架構怎麼決定取樣與後處理？</h2>
<p>Refclk（Reference Clock，參考時脈）是否由元件內部產生、能否在 DUT pin 量到，以及是否測試 SRIS（使用獨立展頻參考時脈的架構），會改變量測方式。先在 Table 8-5 選欄，再選列，最後才讀交叉儲存格；不要先認定所有 Tx 測試都只取資料波形。</p>
<div class="table-wrap"><table><thead><tr><th scope="col">本次選用的條件</th><th scope="col">Table 8-5 的位置</th><th scope="col">取樣與後處理</th></tr></thead><tbody><tr><td>Non-Embedded Refclk；DUT pin 可取得 Refclk；不測 SRIS</td><td>右欄、第一列</td><td>1-port measurement，使用 CC CDR 與乾淨的外部 Refclk</td></tr><tr><td>Embedded Refclk；DUT pin 可取得 Refclk；不測 SRIS</td><td>左欄、第一列</td><td>2-port measurement，使用 CC CDR、PLL（見註 1）及 10 ns transport delay</td></tr></tbody></table></div>
<p>CDR（Clock and Data Recovery，時脈與資料恢復）在這裡是後處理使用的規格模型；CC 表示 Common Clock。第二列的 2-port measurement 同步擷取 Tx 資料與 Tx Refclk，以移除兩者共有的時脈抖動；這項選擇和 D+、D− 是兩根導線不同。PLL（Phase-Locked Loop，鎖相迴路）的特性要依該速率的 Refclk 章節查，transport delay（傳輸延遲）則連到 §8.6.6，不能自行當成零。</p>
<p>若改為 Independent Refclk（IR，獨立參考時脈）模式，§8.3.5.3 規定使用 single-port jitter measurement，並選適合該架構的 model CDR。上表只帶讀 Table 8-5 的兩個指定組合，其餘條件須回完整表核對。DUT 若支援多種 Refclk 模式，也須依規格在各支援模式下測試。</p>
<p class="source-note">Base 6.0 Figure 8-2 <em>Tx Test board for Embedded Refclk</em>（p.1319）；§8.3.5.3 <em>Independent Refclk Measurement and Post Processing</em>、§8.3.5.4 <em>Embedded and Non-Embedded Refclk Measurement and Post Processing</em>、Table 8-5 <em>Tx Measurement and Post Processing For Different Refclks</em>（p.1338）。</p></section>

<section id="voltage"><h2>先分清差分、單端與共模，再找電壓限制</h2>
<p>先讀 §8.3.2 的定義，再看 Figure 8-3。D+、D− 各自相對參考電位的電壓是單端電壓；兩者相減得到差分電壓，兩者平均則是共模電壓。</p>
<p><code>VDIFF = VD+ − VD−</code>；<code>VCM = (VD+ + VD−) / 2</code>。峰對峰值（peak-to-peak，以下單位寫作 mVPP）是同一個電壓量的最高值減最低值。Equation 8-1 的 <code>VDIFFp-p = 2 × max|VD+ − VD−|</code> 另有前提：差分擺幅必須對稱。先確認這項前提，才可用乘二的簡式。</p>
<p>Figure 8-3 的用途是把三條曲線放在一起，讓讀者看懂它們的關係。它不是「讀出任一曲線高度，就能直接和 Tx 電壓上限比較」的圖。正式測法還要接 §8.3.3.6 或 §8.3.3.7，再回 Table 8-6 選速率、參數與單位。</p>
<p class="source-note">Base 6.0 §8.3.2 <em>Voltage Level Definitions</em>、Equations 8-1 <em>VDIFFp-p</em> 與 8-2 <em>VTX-AC-CM-PP</em>（p.1320）；Figure 8-3 <em>Single-ended and Differential Levels</em>（p.1321）。</p></section>

<section id="voltage-case"><h2>單端 450 mVPP，為什麼對應差分 900 mVPP？</h2>
<div class="example"><p><strong>【模擬資料】以下資料為教學用途建立，不代表特定硬體或平台。</strong>觀察待測 Endpoint 的一條 Tx Lane，訊號由 DUT 輸出到 TP1；速率為 5.0 GT/s、full swing（完整擺幅），使用 Non-Embedded Refclk、乾淨外部時脈，且不測 SRIS。依前表採 1-port measurement 與 CC CDR。假設接上適用的 compliance test load，並已完成差分電壓所需的通道還原。</p>
<p>§8.3.3.6 在 2.5／5.0 GT/s 要使用 500 次 Compliance Pattern（符合性測試圖樣），於 0.5 UI 位置取平均 transition eye amplitude（訊號跳變時的眼高）。以下是按此前提整理的理想化代表電壓；只用來說明幅度關係，不模擬邊緣、過衝或雜訊。UI（Unit Interval）是此處的訊號時間單位，0.5 UI 是規定的取樣位置。</p>
<div class="table-wrap"><table><thead><tr><th scope="col">互補的兩個代表狀態</th><th scope="col">D+（mV）</th><th scope="col">D−（mV）</th><th scope="col">VDIFF（mV）</th><th scope="col">VCM（mV）</th></tr></thead><tbody><tr data-voltage-state="high"><td>H</td><td>825</td><td>375</td><td>+450</td><td>600</td></tr><tr data-voltage-state="low"><td>L</td><td>375</td><td>825</td><td>−450</td><td>600</td></tr></tbody></table></div>
<p>H 狀態下，差分為 <code>825 − 375 = +450 mV</code>；L 狀態則為 <code>375 − 825 = −450 mV</code>。因此差分峰對峰為 <code>+450 − (−450) = 900 mVPP</code>。D+ 自己只在 375 與 825 mV 之間變化，單端峰對峰是 <code>450 mVPP</code>；D− 也相同。兩個狀態的共模都是 <code>600 mV</code>，它是平均電位，不是差分擺幅。</p>
<figure class="diagram"><svg viewBox="0 0 900 460" style="min-width:640px" role="img" aria-labelledby="voltage-levels-title voltage-levels-desc"><title id="voltage-levels-title">作者案例中的單端電壓與差分電壓</title><desc id="voltage-levels-desc">互補的825與375mV單端電壓形成正負450mV差分電壓；差分峰對峰900mV，共模600mV。</desc><text x="450" y="30" text-anchor="middle" font-size="19">單端：D+ 實線／D− 虛線</text><text x="90" y="85" font-size="17">825 mV</text><text x="90" y="170" font-size="17">375 mV</text><path d="M185 80 H330 V165 H480 V80 H630 V165 H780" stroke="var(--accent)" stroke-width="3" fill="none"/><path d="M185 165 H330 V80 H480 V165 H630 V80 H780" stroke="var(--accent)" stroke-width="2" stroke-dasharray="7 5" fill="none"/><path d="M810 80 H830 V165 H810" stroke="var(--accent)" stroke-width="2" fill="none"/><text x="845" y="128" text-anchor="middle" font-size="15">450</text><text x="845" y="150" text-anchor="middle" font-size="15">mVPP</text><text x="450" y="232" text-anchor="middle" font-size="19">差分：D+ − D−</text><text x="90" y="286" font-size="17">+450 mV</text><text x="115" y="330" font-size="17">0 mV</text><text x="90" y="373" font-size="17">−450 mV</text><path d="M185 325 H780" stroke="var(--line)" stroke-dasharray="4 5" fill="none"/><path d="M185 280 H330 V370 H480 V280 H630 V370 H780" stroke="var(--accent)" stroke-width="3" fill="none"/><path d="M810 280 H830 V370 H810" stroke="var(--accent)" stroke-width="2" fill="none"/><text x="845" y="327" text-anchor="middle" font-size="15">900</text><text x="845" y="350" text-anchor="middle" font-size="15">mVPP</text><text x="450" y="425" text-anchor="middle" font-size="18">VCM = (D+ + D−) / 2 = 600 mV</text></svg><figcaption>作者繪製的理想化波形，不按時間比例；省略上升／下降時間與雜訊。上下圖使用各自標示的電壓尺度，不能把共模 600 mV 當成差分的零點。</figcaption></figure>
<h3>找到參數列之後，還要把 Note 3 接回測法</h3>
<p>接著翻到 Table 8-6 的 <code>VTX-DIFF-PP</code> 列，選 5.0 GT/s 欄。這列描述 full swing 的差分峰對峰 Tx voltage swing，範圍是 <code>800–1000 mVPP</code>；旁邊 Note 3 要求回到 §8.3.3.6／§8.3.3.7 核對測法。因此，本例應以 900 mVPP 比較，而非拿 D+ 的 450 mVPP 比較。</p>
<p>在已列明的量測假設下，900 mVPP 落在這一項的範圍內。這個結論只涵蓋本次差分擺幅；Tx 的 jitter、共模雜訊、等化及其他條目仍需各自量測。兩個代表狀態都算出 600 mV，也不足以證明完整波形沒有 AC 共模雜訊。</p>
<p>若量測模式改為 reduced swing（低擺幅），就要讀另一列 <code>VTX-DIFF-PP-LOW</code>。兩列在本版的最大值同為 1000 mVPP，但最小值不同，不能只抄上限而省略輸出模式。</p></div>
<p class="source-note">Base 6.0 §8.3.3.6 <em>Method for Measuring VTX-DIFF-PP at 2.5 GT/s and 5.0 GT/s</em>（p.1326）；Table 8-6 <em>Data Rate Dependent Transmitter Parameters</em> 的兩個差分擺幅條目（p.1348）、Note 3（p.1351）。</p></section>

<section id="equalization"><h2>升速之後，電壓與 Preset 要換哪一套讀法？</h2>
<p>2.5／5.0 GT/s 的 Tx equalization 只有 de-emphasis（去加重），測量要依 §8.3.3.1／§8.3.3.4 的 transition（跳變）與 non-transition（未跳變）的平均眼高比值。升到 8.0、16.0、32.0 或 64.0 GT/s 後，改用係數與 preset（預先定義的等化組合）控制，不能把前例兩個代表電壓當成完整 preset 測試。</p>
<p>§8.3.3.7 的擺幅測法要求關閉適用的前後游標等化係數，在 Compliance Pattern 的低頻區段量測：8.0／16.0／32.0 GT/s 使用 64 個零與 64 個一；64.0 GT/s 則使用 64 個 PAM4 level 0 與 64 個 level 3。再依規則選每半週期末端的量測區域，並對 500 次重複取平均。</p><dl class="st-terms" aria-label="本段名詞"><div><dt>PAM4</dt><dd>Pulse Amplitude Modulation with 4 levels，四階脈衝振幅調變</dd></div></dl>
<p>如果要確認 preset 本身，查 Figure 8-7：一條路徑擷取已等化的輸出，另一條路徑擷取未等化的輸出，再由後處理套用係數重建，找出兩者誤差最小的係數。Table 8-1 適用 8.0／16.0／32.0 GT/s，Table 8-2 適用 64.0 GT/s；它們用比值與容許範圍定義 preset，係數大小也不直接等於輸出電壓大小。</p>
<p>這樣就能接回 <a href="/DOCS/pcie-course/chapter-19.html#equalization">Chapter 19</a>：Link 上交換的是設定要求，這裡量的是該設定實際形成的輸出。設定已要求、訓練已結束與電氣條目已通過，仍須分別確認。</p>
<p class="source-note">Base 6.0 §8.3.3.1–8.3.3.3（pp.1321–1323）；Tables 8-1、8-2（pp.1324–1325）；§8.3.3.4–8.3.3.7、Figure 8-7 <em>Methodology for measuring Tx equalization coefficients and presets</em>（pp.1325–1326）。</p></section>

<section id="jitter"><h2>量 jitter 時，先用待測項目選圖樣</h2>
<p>Jitter（邊緣或脈寬的時間變化）的數值還取決於圖樣、等化與後處理。先讀 §8.3.5 的適用規則，再選 Table 8-6 的參數列；不要把各種 jitter 都縮成同一個數字。</p>
<div class="table-wrap"><table><thead><tr><th scope="col">速率與待測內容</th><th scope="col">§8.3.5 指定的圖樣</th><th scope="col">Tx 等化條件</th></tr></thead><tbody><tr><td>2.5／5.0 GT/s jitter</td><td>Compliance Pattern，依規定的 zero-crossing 處理</td><td>依該速率適用的 de-emphasis 設定</td></tr><tr><td>8.0／16.0 GT/s jitter</td><td>Compliance Pattern，依規定的 zero-crossing 處理</td><td>應選出最低 jitter 的 preset</td></tr><tr><td>32.0 GT/s jitter</td><td>Jitter Measurement Pattern</td><td>必須無 Tx equalization</td></tr><tr><td>64.0 GT/s uncorrelated total jitter 與 deterministic jitter</td><td>Jitter Measurement Pattern，涵蓋四階 PAM4 的十二種轉換</td><td>必須無 Tx equalization</td></tr><tr><td>64.0 GT/s uncorrelated total pulse width jitter 與 deterministic pulse width jitter</td><td>High Swing Toggle Pattern，量 level 0 與 level 3 的轉換</td><td>必須無 Tx equalization</td></tr></tbody></table><dl class="st-terms" aria-label="本段名詞"><div><dt>PAM4</dt><dd>Pulse Amplitude Modulation with 4 levels，四階脈衝振幅調變</dd></div></dl></div>
<p>32.0 與 64.0 GT/s 的 Tx jitter 量測，示波器最低頻寬要求為 50 GHz；64.0 GT/s 另建議使用規定的 4th-order Bessel-Thomson filter，於 33 GHz 衰減 3 dB。頻寬要求與濾波建議的規範強度不同，記錄條件時要保留這個差別。</p>
<p>§8.3.5 要求量測某一條 Tx Lane 時，其他 PCIe Lanes 送出 Compliance Pattern，以納入晶片與封裝的串擾；也要求 DUT 啟動正常系統情境會使用的盡可能多的輸出。這比 §8.3.1 的一般量測環境介紹更具體，實際程序要回到當前待測項目的要求。</p>
<p>最後再核對參考點。Table 8-6 中 <code>VTX-AC-CM-PP</code> 與 <code>VTX-AC-CM-PP-filtered</code> 明確註記共模雜訊分析不做 de-embedding，正是「除非另有規定」的例外。它們不是 jitter 參數，也不能直接沿用前例差分擺幅的後處理。報告若只寫「全部還原到 pin」，仍須逐項確認是否符合該列的規則。</p>
<p class="source-note">Base 6.0 §8.3.5 <em>Tx Jitter Parameters</em>（p.1336）、§8.3.5.1–8.3.5.2（pp.1336–1338）；Table 8-6 共模電壓兩列與註記（p.1350）。此處示範條件選擇，並非完整符合性測試程序。</p></section>

<section id="sources"><h2>版本與來源</h2><p>本章以 PCI Express Base Specification Revision 6.0（6.0-1.0-PUB）為準；所列文件印刷頁碼與 PDF 檢視器頁碼相同。案例已標明理想化電壓與量測假設，並非特定裝置的實測或合規證明。</p><details class="source-note"><summary>本章閱讀位置與用途</summary><ul><li>§8.3.1、Figures 8-1／8-2（pp.1318–1319）；§8.3.1.1（pp.1319–1320）：量測接點、Breakout／Replica Channel 及參考點。</li><li>§8.3.2 <em>Voltage Level Definitions</em>、Equations 8-1／8-2（p.1320）；Figure 8-3（p.1321）：單端、差分與共模定義。</li><li>§8.3.3 <em>Tx Voltage Parameters</em> 與 §8.3.3.1–8.3.3.7（pp.1321–1326）；Tables 8-1／8-2、Figure 8-7：各速率的擺幅、等化與 preset 測法。</li><li>§8.3.5 <em>Tx Jitter Parameters</em> 及 §8.3.5.1–8.3.5.5（pp.1336–1338）；Table 8-5（p.1338）：圖樣、量測環境、時脈取樣與後處理。PLL 與 transport delay 的完整定義依表內連到相應 Refclk 章節與 §8.6.6，本章不展開其演算法。</li><li>§8.3.6 <em>Data Rate Dependent Parameters</em>、Table 8-6（p.1347 起）：本例使用 p.1348 的差分擺幅列與 p.1351 的 Note 3；p.1350 的 AC 共模條目帶讀不做 de-embedding 的例外。</li></ul></details></section>
</article>
<nav class="bottom-nav" aria-label="課程與語言版本"><a href="/DOCS/pcie-course/index.html">課程總覽</a><a href="/DOCS/pcie-course/chapter-20.html">繁中完整教學</a><a href="/pcie/chapter-20-en/">English</a></nav>
</div>
