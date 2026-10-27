---
layout: post
title: "PCIe Chapter 10：裝置與連線如何省電"
date: 2026-10-21 00:00:00 +0800
last_modified_at: 2026-10-28 00:00:00 +0800
permalink: /pcie/chapter-10-zh-tw/
categories: [PCIe]
tags: [PCIe, Specification]
lang: zh-TW
spec_teaching: true
spec_series: pcie
description: "沿 PMCSR、基本 L1 協商時序與 L1.2 雙端設定，串起 Function／Link 省電、待送交易與恢復條件。"
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
<nav class="bottom-nav" aria-label="課程與語言版本"><a href="/DOCS/pcie-course/index.html">課程總覽</a><a href="/DOCS/pcie-course/chapter-10.html">繁中完整教學</a><a href="/pcie/chapter-10-en/">English</a></nav>
<article class="lesson">
<aside class="note"><strong>【模擬資料】</strong><p>本章的拓撲、讀值與事件情境為教學用途建立，不代表特定硬體或平台。</p></aside>
<section id="chapter-overview"><h2>先看本章的角色與路徑</h2><figure class="diagram"><svg viewBox="0 0 900 440" role="img" aria-labelledby="ch10-guide-title ch10-guide-desc"><title id="ch10-guide-title">上下兩列分別是 Function 與 Link 的狀態；虛線指向 L1 子狀態的額外條件。</title><desc id="ch10-guide-desc">上下兩列分別是 Function 與 Link 的狀態；虛線指向 L1 子狀態的額外條件。</desc><g data-walk-target="function-label"><rect x="30" y="15" width="230" height="55" rx="9" fill="var(--surface-alt)" stroke="var(--line)"/><text x="145.0" y="40" text-anchor="middle" font-size="15">Function 的電源狀態</text></g><g data-walk-target="d0"><rect x="325" y="15" width="200" height="65" rx="9" fill="var(--surface-alt)" stroke="var(--line)"/><text x="425.0" y="40" text-anchor="middle" font-size="15">D0</text></g><g data-walk-target="d3"><rect x="650" y="15" width="200" height="65" rx="9" fill="var(--surface-alt)" stroke="var(--line)"/><text x="750.0" y="40" text-anchor="middle" font-size="15">D3hot</text></g><g data-walk-target="d-transition"><path d="M525 45 L650 45" fill="none" stroke="var(--accent)" stroke-width="2"/><polygon points="650.0,45.0 640.0,40.0 640.0,50.0" fill="var(--accent)"/><text x="587.5" y="36.0" text-anchor="middle" font-size="13">依 PM 規則</text></g><g data-walk-target="link-label"><rect x="30" y="170" width="230" height="55" rx="9" fill="var(--surface-alt)" stroke="var(--line)"/><text x="145.0" y="195" text-anchor="middle" font-size="15">Link 的電源狀態</text></g><g data-walk-target="l0"><rect x="325" y="170" width="200" height="65" rx="9" fill="var(--surface-alt)" stroke="var(--line)"/><text x="425.0" y="195" text-anchor="middle" font-size="15">L0</text></g><g data-walk-target="l1"><rect x="650" y="170" width="200" height="65" rx="9" fill="var(--surface-alt)" stroke="var(--line)"/><text x="750.0" y="195" text-anchor="middle" font-size="15">L1</text></g><g data-walk-target="link-transition"><path d="M525 200 L650 200" fill="none" stroke="var(--accent)" stroke-width="2"/><polygon points="650.0,200.0 640.0,195.0 640.0,205.0" fill="var(--accent)"/><text x="587.5" y="191.0" text-anchor="middle" font-size="13">依 ASPM 條件</text></g><g data-walk-target="substates"><rect x="550" y="325" width="300" height="75" rx="9" fill="var(--surface-alt)" stroke="var(--line)"/><text x="700.0" y="350" text-anchor="middle" font-size="15">L1.1／L1.2</text><text x="700.0" y="373" text-anchor="middle" font-size="15">另查兩端能力、控制與時間</text></g><g data-walk-target="substate-condition"><path d="M750 235 L750 325" fill="none" stroke="var(--accent)" stroke-width="2" stroke-dasharray="6 5"/></g></svg><figcaption><p>作者的分層狀態示意，未列出全部狀態與雙向轉換；本章以適用的 L1.2 設定案例放大說明。</p></figcaption></figure><p class="lead">Function 電源狀態與 Link 電源狀態描述不同對象。D0 表示 Function 的工作電源狀態；在符合條件時，它使用的 Link 仍可透過 ASPM（Active State Power Management，主動狀態電源管理）進入省電狀態。</p><p>前情提要：Chapter 8 已建立相鄰兩端的 Link；本章再把這兩端的省電能力、控制與退出條件接起來。</p><p><strong>規格路線：</strong>Tables 5-1／5-2 → PM Capability 與 Link 欄位 → Figures 7-146–7-150 的 L1 Substates → LTR 與退出時間條件。</p><dl class="st-terms" aria-label="本段名詞"><div><dt>LTR</dt><dd>Latency Tolerance Reporting，延遲容忍度回報</dd></div></dl></section>
<p class="lead">PCIe 電源管理同時涉及 Function、Link 與平台。D-state、ASPM、L1 Substates 與喚醒各有不同的控制與證據，不能只憑一個 Enable 推論目前狀態。本章用 PMCSR 與 L1.2 算例串起查詢、設定及恢復條件。</p>
<p><a href="/DOCS/pcie-course/chapter-10.html">完整中文教學</a> · <a href="/pcie/chapter-10-en/">English</a> · <a href="/DOCS/pcie-course/index.html">課程路線</a></p>
<aside class="note"><strong>版本與假設</strong><p>PCIe 採 Base 6.0，平台補充採 ACPI 6.6。數字均為作者假設。PMCSR 使用普通 Endpoint 03:00.0；L1.2 另採已具備雙端能力、LTR、CLKREQ# 與合適時序設計的 Link，不含 SR-IOV，也不替前例追加未宣告功能。</p><dl class="st-terms" aria-label="本段名詞"><div><dt>LTR</dt><dd>Latency Tolerance Reporting，延遲容忍度回報</dd></div><div><dt>SR-IOV</dt><dd>Single Root I/O Virtualization，單根I/O虛擬化</dd></div></dl></aside>
<section id="states"><h2>Function 的 D-state 與 Link 的 L-state 分開管理</h2><p>D0 是 Function 正常工作狀態，但 ASPM 可在 D0 閒置期間降低 Link 耗電。D1、D2 是可選狀態；D3hot 保有主電源，D3cold 沒有主電源，仍可能由輔助電源支持喚醒。Reset 後的 D0uninitialized 也不等於工作介面已準備完成。</p><p>L0 可傳輸；L0s 可分方向省電，但 Flit Mode、有 Retimer、或指定的獨立 SSC 時脈條件不支援 L0s。L0p 只用於 Flit Mode，讓部分 Lane 閒置，雙向仍各至少有一條 active Lane。L1 可再細分 L1.0、L1.1、L1.2；L2／L3 則是主電源移除後，以是否有 Vaux 區分的狀態。</p><details class="source-note"><summary>狀態來源</summary><p>§5.2–§5.3.1、Tables 5-1／5-2（pp.600–609）；L0s／L0p：§4.2.6.6–§4.2.6.7（p.445）。</p></details></section>
<section id="pmcsr"><h2>讀 PM 能力，再以正確的寫值回 D0</h2><p>傳統 Capability ID=0x01 指向 PM 結構。作者假設在 0x40 讀完整 DWORD=0xC8035001：ID=0x01、Next=0x50、Version=3，D1／D2 不支援；PME_Support=<code>(value &gt;&gt; 27) &amp; 0x1F = 0x19</code>，支援從 D0、D3hot、D3cold 發出 PME。假設無可選 Data Register、Aux_Current=0 採自供電且必要供電可用。這是能力，不是完整喚醒路徑已就緒的證明。</p><dl class="st-terms" aria-label="本段名詞"><div><dt>PME</dt><dd>Power Management Event，電源管理事件</dd></div></dl><div class="table-wrap"><table><caption>PMCSR 0x44 的 16-bit 操作</caption><thead><tr><th scope="col">動作</th><th scope="col">值</th><th scope="col">意義</th></tr></thead><tbody><tr><td>讀取</td><td>0x810B</td><td>D3hot、No_Soft_Reset=1、PME_En=1、PME_Status=1。</td></tr><tr><td>寫入回 D0</td><td>0x0108</td><td>清 PowerState，對 RW1CS PME_Status 寫零以保留事件。</td></tr><tr><td>等待後讀取</td><td>0x8108</td><td>D0，PME 事件仍保留。</td></tr><tr><td>事件處理完畢後明確清除</td><td>0x8108</td><td>刻意對 PME_Status 寫 1；無新事件時讀回 0x0108。</td></tr></tbody></table><dl class="st-terms" aria-label="本段名詞"><div><dt>PME</dt><dd>Power Management Event，電源管理事件</dd></div></dl></div><p>以上假設無並行改動或新事件。No_Soft_Reset=1 保留指定 D3hot→D0 軟體轉換的內部狀態，回 D0active；它不免除恢復等待。本例 Immediate Readiness=0、無其他時間例外，所以至少等 10 ms 才再次存取，包含 Configuration。No_Soft_Reset=0 時必須完整初始化，也不保證舊狀態已清除。D3cold、Fundamental Reset 或 L2/L3 Ready 導致的 DL_Down，不沿用這項保存結論。</p><p>PowerState 沒有 D3cold 編碼。寫入不支援的 D1／D2 會正常完成，但不改變狀態；PME_Status 也不因 PME_En=0 而停止記錄符合條件的事件。進入 D3hot 前仍須妥善處理未完成交易與需保存的狀態。</p><details class="source-note"><summary>能力、寫入屬性與等待</summary><p>Figures 7-17–7-19、Tables 7-14／7-15（pp.944–949）；§5.3.1.4（pp.606–608）；Figure 5-18／Table 5-14（pp.654–655）。Figure 7-18 使用包含 Header 的完整 DWORD bit 編號，不可與 +0x02 的 16-bit 讀值混用。</p></details></section>
<section id="aspm"><h2>ASPM Enable 需要能力與延遲政策支持</h2><p>ASPM 在 D0 期間由硬體管理閒置 Link；PCI-PM 則由軟體改變 D-state。普通非 ARI 多 Function 裝置，必須所有 Functions 都離開 D0，才可代表 PCI-PM 發起進 L1。</p><dl class="st-terms" aria-label="本段名詞"><div><dt>ARI</dt><dd>Alternative Routing-ID Interpretation，替代路由識別碼解讀</dd></div></dl><p>先查兩端 Link Capabilities 的 ASPM Support，再看 Link Control 的 ASPM Control；Enable 不代表當下已在 L1。Link Capabilities 的 L1 Exit Latency 與 Endpoint Device Capabilities 的 L1 Acceptable Latency 要配合整條路徑判斷。多段退出可以重疊，不能直接把所有 Port 延遲相加：Figure 5-8 的例子最後在 T+34 μs 完成。</p><details class="source-note"><summary>ASPM 來源</summary><p>§5.3.2（pp.609–610）、§5.4.1／Figure 5-8（pp.621–640）；Tables 7-20、7-23、7-24（pp.956–957、967–972）。</p></details></section>
<section id="l1-handshake"><h2>沿時序看 L1 如何進入，再接回交易傳輸</h2>
<p>先從 Figure 7-27／Table 7-23 確認 ASPM Support，再以 Figure 7-28／Table 7-24 查看 ASPM Control。這些設定允許 L1 進入；實際交換與兩端動作接到 Figure 5-7 閱讀。</p>
<div class="example"><p><strong>【模擬資料】以下情境為教學用途建立，不代表特定硬體或平台。</strong>獨立案例為 8.0 GT/s、Non-Flit Mode Link：Switch Downstream Port 02:01.0 連到 Endpoint Upstream Port 03:00.0。兩端支援並已正確啟用 ASPM L1、延遲政策可用，Endpoint 的 D0 Functions 都允許 L1。本例不啟用 L1.1／L1.2，裝置維持 D0。協商前 Endpoint 已有各 FC 類別所需的最低 credit（接收緩衝額度），足以傳送相應的最大封包。</p><dl class="st-terms" aria-label="本段名詞"><div><dt>FC</dt><dd>Flow Control，流量控制</dd></div></dl>
<p>Endpoint 在這條 Link 的下游端，Port 類型卻是 Upstream Port。由它提出要求，Switch 的 Downstream Port 回應。螢幕較窄時，可左右滑動圖查看完整內容。</p>
<figure class="diagram"><svg viewBox="0 0 820 640" style="min-width: 640px" role="img" aria-labelledby="l1-entry-title l1-entry-desc"><title id="l1-entry-title">同一條 Link 的 ASPM L1 正常進入流程</title><desc id="l1-entry-desc">時間由上往下。Endpoint 停止新封包並等候重送副本獲得確認，才提出 L1 要求。Switch 接受前也先處理自己的未確認封包。Endpoint 先讓上行方向進入電氣閒置，Switch 再讓下行方向進入電氣閒置。</desc><rect x="45" y="15" width="280" height="75" rx="10" fill="var(--blue-soft)" stroke="var(--line)"/><rect x="495" y="15" width="280" height="75" rx="10" fill="var(--blue-soft)" stroke="var(--line)"/><text x="185" y="44" text-anchor="middle" font-size="18">Switch 02:01.0</text><text x="185" y="73" text-anchor="middle" font-size="18">Downstream Port</text><text x="635" y="44" text-anchor="middle" font-size="18">Endpoint 03:00.0</text><text x="635" y="73" text-anchor="middle" font-size="18">Upstream Port</text><path d="M185 90 V555 M635 90 V555" stroke="var(--line)" stroke-dasharray="5 5"/><rect x="495" y="115" width="280" height="65" rx="10" fill="var(--blue-soft)" stroke="var(--line)"/><text x="635" y="141" text-anchor="middle" font-size="16">停止排送新的 TLP</text><text x="635" y="166" text-anchor="middle" font-size="16">等最後一筆的 Link 層確認</text><rect x="45" y="240" width="280" height="65" rx="10" fill="var(--blue-soft)" stroke="var(--line)"/><text x="185" y="266" text-anchor="middle" font-size="16">停止排送新的 TLP</text><text x="185" y="291" text-anchor="middle" font-size="16">等先前傳送獲得確認</text><rect x="495" y="375" width="280" height="65" rx="10" fill="var(--blue-soft)" stroke="var(--line)"/><text x="635" y="401" text-anchor="middle" font-size="16">停止 TLP 與 DLLP 傳送</text><text x="635" y="426" text-anchor="middle" font-size="16">上行方向進入 Electrical Idle</text><rect x="45" y="475" width="280" height="65" rx="10" fill="var(--blue-soft)" stroke="var(--line)"/><text x="185" y="501" text-anchor="middle" font-size="16">觀察接收方向的 Electrical Idle</text><text x="185" y="526" text-anchor="middle" font-size="16">下行方向也進入 Electrical Idle</text><text x="410" y="199" text-anchor="middle" font-size="18">PM_Active_State_Request_L1 (DLLP)</text><path d="M635 215 H185 M195 209 L185 215 L195 221" fill="none" stroke="var(--accent)" stroke-width="2.5"/><text x="410" y="329" text-anchor="middle" font-size="18">PM_Request_Ack (DLLP)</text><path d="M185 345 H635 M625 339 L635 345 L625 351" fill="none" stroke="var(--accent)" stroke-width="2.5"/><rect x="245" y="575" width="330" height="45" rx="10" fill="var(--blue-soft)" stroke="var(--line)"/><text x="410" y="604" text-anchor="middle" font-size="18">兩端依規則完成 L1 進入</text></svg><figcaption>作者依 Base 6.0 Figure 5-7 與 §5.4.1.3.1 整理的教學時序圖。時間由上往下，不按比例；重複傳送的 DLLP 只畫一次。Ordered Sets、時間限制與中斷分支仍須搭配周圍文字查閱。</figcaption></figure><dl class="st-terms" aria-label="本段名詞"><div><dt>TLP</dt><dd>Transaction Layer Packet，交易層封包</dd></div><div><dt>DLLP</dt><dd>Data Link Layer Packet，資料鏈結層封包</dd></div></dl>
</div>
<p>原 Figure 5-7 的 T／D／P 是 Transaction、Data Link、Physical Layer；沿時間往下，查看哪一端先停止排送新封包，以及兩個方向如何先後進入 Electrical Idle（電氣閒置）。這些活動標示與 Figure 3-2 的 Data Link 狀態名稱分開判讀。</p>
<p>等待最後 TLP 的 Link 層確認，用來清空 Retry Buffer（保存重送副本的緩衝區）；PM_Request_Ack 則是接受 L1 要求的 DLLP（Data Link Layer Packet，資料連結層封包）。它和 TLP 的 Ack DLLP、端到端讀取的 Completion 各有用途。若先前的 Memory Read 還在等 Completion，那筆讀取仍須繼續追蹤，進入 L1 不會替它完成交易。</p>
<p>延續接受分支：若 Switch 送出 PM_Request_Ack 後才有 Memory Write（記憶體寫入）要從此 Link 傳送，必須先完成 L1 轉換，再發起退出，即使當下沒有足夠的 Flow Control credit 也要退出。回到 L0 後，再按正常額度與排程規則傳送。接著讀 Figure 4-54：L1.Entry → L1.Idle，符合退出條件後到 Recovery，再依適用流程回 L0。這是正常的 L1 退出路徑。</p>
<p>Completion Timeout 在 L1 仍計時，Flow Control Update timers 則凍結。若改走 Figure 5-6 的拒絕分支，PM_Active_State_Nak 是 Message TLP，和要求重送的 Nak DLLP 不同；原圖以 L0s 已啟用為前提。只有無 TLP 的片段時，仍需 PM 協商、Electrical Idle 與 LTSSM 紀錄來核對工具的 L1 標示。</p><dl class="st-terms" aria-label="本段名詞"><div><dt>LTSSM</dt><dd>Link Training and Status State Machine，鏈結訓練與狀態機</dd></div></dl>
<details class="source-note"><summary>能力、協商與退出來源</summary><p>Base 6.0 Figures 7-27／7-28、Tables 7-23／7-24（PDF／印刷 pp.967–968、971）；§5.4.1.3 <em>ASPM L1 State</em>、§5.4.1.3.1 <em>ASPM Entry into the L1 State</em>（pp.626–631）；Figure 5-6 <em>L1 Transition Sequence Ending with a Rejection (L0s Enabled)</em>（p.632）；Figure 5-7 <em>L1 Successful Transition Sequence</em>、§5.4.1.3.2 <em>Exit from the L1 State</em>（p.633）；§4.2.7.7 <em>L1</em>／Figure 4-54 <em>L1 Substate Machine</em>（pp.519–520）。Data Link 狀態見 §3.2.1（pp.265–268）、Table 4-48（p.453）。本段的 PDF 與印刷頁碼相同。</p></details></section>
<section id="substates"><h2>L1.2 要依兩端能力與設定順序建立</h2><div class="table-wrap"><table><caption>獨立 L1.2 案例的設定快照</caption><thead><tr><th scope="col">位置</th><th scope="col">Downstream Port</th><th scope="col">Upstream Port</th></tr></thead><tbody><tr><td>Header，0x200</td><td>0x0001001E</td><td>0x0001001E</td></tr><tr><td>Capabilities，0x204</td><td>0x00280A1F</td><td>0x0051141F</td></tr><tr><td>Control 1，0x208</td><td>0x40801404</td><td>0x40800004</td></tr><tr><td>Control 2，0x20C</td><td>0x00000051</td><td>0x00000051</td></tr></tbody></table></div><p>各自走訪 Extended 清單後，假設剛好在 0x200 找到 ID=0x001E、Version=1、Next=0；版本 1 沒有 +0x10 Status。兩端低五個 capability bits 都是 0x1F，支援四種 Substates 與總支援標記。宣告 T_POWER_ON 分別為 10／100 μs、common-mode 恢復為 10／20 μs；已設定 Control 2 的 Value=10、Scale=1，得到 100 μs。Control 1 只開 bit 2 的 ASPM L1.2。Common_Mode_Restore_Time 在 Downstream Port 設 20 μs，在 Upstream Port 是 RsvdP。</p><p>平台已確認此快照適合連接設計，不把兩端宣告值取最大值當成通用演算法。啟用前必須兩端都支援；ASPM Substate 設定期間先停用 ASPM L1，PCI-PM Substate 則在 D0 設定。先完成適用的時間與相同 LTR threshold，再依 Downstream Port、Upstream Port 順序開對應 Enable；停用順序相反。修改時間欄位須先清相應 L1.2 Enable，最後依政策恢復 ASPM L1。</p><details class="source-note"><summary>L1 Substates 查詢與設定路徑</summary><p>Figures 7-146–7-150／Tables 7-129–7-132（pp.1103–1108）；§5.5、§5.5.4–§5.5.5／Table 5-11（pp.640、650–651）。L1.1 保持 common-mode，L1.2 不要求保持，皆使用 CLKREQ#；ASPM L1.2 需要 LTR。</p></details></section>
<section id="ltr"><h2>相同 Enable，仍可能有不同的進入結果</h2><p>Control 1 的 threshold Value=128、Scale=2，為 128 × 1024 ns=131072 ns（131.072 μs）。假設已在 ASPM L1.0、CLKREQ# 已 deassert、其他條件成立，最新有效 snoop／no-snoop LTR 需求若為 204800／102400 ns，後者不足，不能進 L1.2；改為 204800／153600 ns 後，兩者皆達 threshold，在上述條件下應進入。</p><p>某一類「無需求」可走另一判斷分支，不等於 Requirement=1、Value=0；後者要求盡可能低的延遲。這些是最近的有效回報，不是 Max Latency Register 上限。LTR 也不是 Root Complex 的硬性延遲承諾。本例未開 L1.1，不能假設不足時必然退到 L1.1。啟用 Endpoint LTR 前，Root Complex 與沿途 Switch 都須支援，並由靠近 Root Port 者先啟用。</p><details class="source-note"><summary>LTR 與進入條件</summary><p>§5.5.1（p.644）；Figure 6-15、§6.18（pp.781–782）；Table 7-131（pp.1107–1108）。</p></details></section>
<section id="wake"><h2>喚醒先恢復通路，再辨識事件來源</h2><p>L2 不能傳一般 TLP。裝置依 form factor 用 WAKE# 或 Beacon 請平台恢復電源、時脈與 Link，再送含 Requester ID 的 PM_PME。因此仍需 PME_En、輔助供電與平台路徑配合。（§5.3.3.1–§5.3.3.2，pp.615–616。）</p><p>補充背景：<a href="https://uefi.org/sites/default/files/resources/ACPI_Spec_6.6.pdf#page=568">ACPI 6.6 §7.3.8–§7.3.11</a> 的 _PR0／_PR3 描述 D0／D3hot 所需電源資源，並非 PCIe Register。文件 pp.497–498 對應 PDF pp.568–569。</p></section>
<section id="questions"><h2>檢查條件是否足夠</h2><details class="question"><summary>No_Soft_Reset=1 能保證 D3cold 後保留全部狀態嗎？</summary><p>不能；它只適用指定 D3hot→D0 軟體轉換。</p></details><details class="question"><summary>只有 Endpoint 支援 L1.2，可以只開一端嗎？</summary><p>不可以。兩端對應能力、設定順序、LTR 與時序條件都要成立。</p></details></section>
</article>
<nav class="bottom-nav" aria-label="課程與語言版本"><a href="/DOCS/pcie-course/index.html">課程總覽</a><a href="/DOCS/pcie-course/chapter-10.html">繁中完整教學</a><a href="/pcie/chapter-10-en/">English</a></nav>
</div>
