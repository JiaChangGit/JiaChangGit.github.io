---
layout: post
title: "PCIe Chapter 22：連線診斷、Lane Margining 與 Flit 紀錄"
date: 2026-10-24 00:00:00 +0800
last_modified_at: 2026-10-29 00:00:00 +0800
permalink: /pcie/chapter-22-zh-tw/
categories: [PCIe]
tags: [PCIe, Specification]
lang: zh-TW
spec_teaching: true
spec_series: pcie
description: "要檢查某條 Lane，設定空間應該怎麼查？"
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
<nav class="bottom-nav" aria-label="課程與語言版本"><a href="/DOCS/pcie-course/index.html">課程總覽</a><a href="/DOCS/pcie-course/chapter-22.html">繁中完整教學</a><a href="/pcie/chapter-22-en/">English</a></nav>
<article class="lesson">
<p>Lane Margining（接收端裕量量測）讓軟體在 Link 維持 L0 時，觀察接收端偏離正常取樣位置後的表現。本章以 16.0 GT/s Endpoint 的一條 Lane 為例，從 Extended Capability（延伸能力結構）找到控制位置，查詢接收端能力，再讀懂命令回報與復原流程。</p><figure class="diagram"><svg viewBox="0 0 900 250" role="img" aria-labelledby="ch22-zh-t ch22-zh-d"><title id="ch22-zh-t">Lane Margining 的規格閱讀路線</title><desc id="ch22-zh-d">診斷前先確認能力與就緒，再操作指定範圍。</desc><g data-walk-target="n0"><rect x="30" y="40" width="350" height="44" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="205.0" y="69" text-anchor="middle" font-size="16">找到對應 Port 的能力</text></g><g data-walk-target="n1"><rect x="515" y="40" width="350" height="44" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="690.0" y="69" text-anchor="middle" font-size="16">確認用途、模式與就緒</text></g><g data-walk-target="n2"><rect x="515" y="175" width="350" height="44" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="690.0" y="204" text-anchor="middle" font-size="16">依 Lane／接收端選擇控制</text></g><g data-walk-target="n3"><rect x="30" y="175" width="350" height="44" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="205.0" y="204" text-anchor="middle" font-size="16">讀取回報並恢復正常設定</text></g><g data-walk-target="a"><path d="M380 74 L515 74" stroke="var(--accent)" stroke-width="2" fill="none"/><polygon points="515,74 505.0,79.0 505.0,69.0" fill="var(--accent)"/><text x="447.5" y="64.0" text-anchor="middle" font-size="16"></text></g><g data-walk-target="b"><path d="M690 84 L690 175" stroke="var(--accent)" stroke-width="2" fill="none"/><polygon points="690,175 685.0,165.0 695.0,165.0" fill="var(--accent)"/><text x="690.0" y="129.5" text-anchor="middle" font-size="16"></text></g><g data-walk-target="c"><path d="M515 209 L380 209" stroke="var(--accent)" stroke-width="2" fill="none"/><polygon points="380,209 390.0,204.0 390.0,214.0" fill="var(--accent)"/><text x="447.5" y="199.0" text-anchor="middle" font-size="16"></text></g></svg><figcaption><p>作者繪製的規格閱讀路線；命令之間的等待與交握，見下方完整案例。</p></figcaption></figure><section id="walk"><h2>從 Endpoint 的 Lane 3 開始，要依序查哪幾張圖？</h2>
<p><strong>【模擬資料】以下資料為教學用途建立，不代表特定硬體或平台。</strong>拓撲為 Root Port 直接連接 Endpoint，沒有 Retimer（訊號重整器），也沒有 Lane Reversal（Lane 順序反轉）。目前 Link 在 L0，以 16.0 GT/s x4 運作；兩端最大寬度均為 x8。這次觀察 Endpoint 接收 Root Port 資料的方向，指定啟用中的預設 Lane 3。</p>
<p>先回顧一個方向關係：Root Port 是 Downstream Port，Endpoint 的 Port 是 Upstream Port。這次要調整的是 Endpoint 的 Receiver（接收端），所以從 Endpoint 的設定空間下命令。多功能 Endpoint 只在 Function 0 放這組 Lane Margining（接收端裕量量測）能力。</p>
<div class="table-wrap"><table><thead><tr><th scope="col">閱讀順序</th><th scope="col">這次讀哪裡？</th><th scope="col">帶著什麼結果往下查？</th></tr></thead><tbody>
<tr><td>1. 定位結構</td><td>Figure 7-126／Table 7-111，p.1080</td><td>沿 Extended Capability（延伸能力結構）鏈找到 ID 0027h、Version 1h，將起點記為 C</td></tr>
<tr><td>2. 找 Lane 項目</td><td>Figure 7-125，pp.1079–1080</td><td>Lane 0 Control 從 C+08h 起，每 Lane 佔 4 bytes；Lane 3 Control=C+14h，Status=C+16h</td></tr>
<tr><td>3. 確認可下命令</td><td>Figures 7-127／7-128、Tables 7-112／7-113，pp.1080–1081</td><td>本例 Margining uses Driver Software=0、Margining Ready=1；Margining Software Ready 此時無定義，不拿它當額外門檻</td></tr>
<tr><td>4. 選接收端</td><td>Figure 4-60，p.553；Receiver Number 編碼，p.552</td><td>Endpoint 的 Upstream Port Receiver 是 Rx(F)，Receiver Number=110b；不是 Root Port 自己的 Rx(A)=001b</td></tr>
<tr><td>5. 組命令、讀回報</td><td>Figures 7-129／7-130、Tables 7-114／7-115，pp.1082–1083；Table 4-63，pp.554–556</td><td>欄位位置在 Chapter 7，命令與回覆語意在 Chapter 4；兩邊要合併閱讀</td></tr>
</tbody></table></div>
<p>這裡的 Lane 項目依<strong>預設 Lane 編號</strong>排列，不隨協商寬度或 Lane Reversal 重新編號。Maximum Link Width 決定有效項目的範圍；超出最大寬度的項目值未定義。本例另外確認 Lane 3 位於目前 x4 的啟用範圍，才對它進行測試。</p>
<p class="source-note">來源：§7.7.10–§7.7.10.5，文件／PDF pp.1077–1083；§4.2.18.1、Figure 4-60，pp.552–553。</p></section>

<section id="margin-session"><h2>知道暫存器位置後，如何完成一次命令？</h2>
<p>先完成 §4.2.18.3 的操作準備：目前速率須至少為 16.0 GT/s，待測 Lane 必須在目前 Link Width 內；Upstream Port 的 Function 電源設定須阻止 Port 進入 L1，兩端 ASPM Control（自主 Link 省電控制）須設為 00b。保存 Hardware Autonomous Speed Disable 與 Hardware Autonomous Width Disable 原值；兩端的對應欄位若可寫，均設為 1，測完再恢復。</p>
<p>本例以上準備都已完成，且每次只測一條 Lane。Figure 7-129 的 16-bit Control 與 Figure 7-130 的 Status 使用相對應的欄位位置；bit 7 是 RsvdP（保留原值），本例原值為 0。下表數值都是完整 16-bit 讀值，不是記憶體中的 byte 排列。</p>
<figure class="diagram"><svg viewBox="0 0 900 235" style="min-width:640px" role="img" aria-labelledby="margin-fields-title margin-fields-desc"><title id="margin-fields-title">同一組欄位，命令與回報的 Payload 不同</title><desc id="margin-fields-desc">Control 051E 選 Rx F、timing type 011，向右五步。Status 821E 的 Payload 82 表示執行中且錯誤計數二，不是向右一百三十步。</desc>
<text x="30" y="30" font-size="17">Control：051Eh → timing，向右 5 steps</text>
<rect x="30" y="48" width="390" height="58" fill="var(--surface-alt)" stroke="var(--line)"/><rect x="420" y="48" width="65" height="58" fill="var(--surface-alt)" stroke="var(--line)"/><rect x="485" y="48" width="75" height="58" fill="var(--surface-alt)" stroke="var(--line)"/><rect x="560" y="48" width="160" height="58" fill="var(--surface-alt)" stroke="var(--line)"/><rect x="720" y="48" width="150" height="58" fill="var(--surface-alt)" stroke="var(--line)"/>
<g text-anchor="middle" font-size="16"><text x="225" y="72">[15:8] Payload=05h</text><text x="225" y="94">方向與步數</text><text x="452" y="72">[7]</text><text x="452" y="94">RsvdP</text><text x="522" y="72">[6]</text><text x="522" y="94">0b</text><text x="640" y="72">[5:3] Type</text><text x="640" y="94">011b</text><text x="795" y="72">[2:0] Receiver</text><text x="795" y="94">110b：Rx(F)</text></g>
<text x="30" y="147" font-size="17">Status：821Eh → 執行中，MErrorCount=2</text><path d="M30 163 H870" stroke="var(--accent)" stroke-width="2"/><text x="30" y="192" font-size="16">Payload=82h：bits [7:6]=10b；bits [5:0]=000010b</text><text x="30" y="220" font-size="16">Usage Model [6]=0b：本次使用 Lane Margining</text></svg><figcaption>作者依 Figures 7-129／7-130 與 Table 4-63 繪製。回報的低位欄位用來辨認對象與命令，Payload 要按回報定義解碼。</figcaption></figure>
<p><strong>每次換命令前，先送 No Command 並等待其回覆。</strong>Table 4-63 將它定義為 Receiver=000b、Type=111b、Payload=9Ch、Usage Model=0b；本例 Control 為 9C38h。新命令須以一次不可分割的寫入更新 Control，再以一次不可分割的讀取取得 Status。核對回報的 Receiver、Type、Usage Model，以及該命令預期的 Payload；檢查 No Command 回覆時，核對 Receiver Number Status=000b、Margin Type Status=111b、Usage Model Status=0b；依 Table 7-115，Margin Payload Status 此時不作有效結果比較。</p>
<p>若 Link 仍在 L0 且速率至少為 16.0 GT/s，目標接收端須在收到有效命令後 1 ms 內套用並回覆；Step Margin 的回覆仍可能是準備中。§4.2.18.3 建議兩次 Status 讀取至少間隔 10 μs。新命令發出 10 ms 後仍未取得預期回覆，軟體可以宣告該接收端的 margining 失敗；這和 Configuration Write 已取得 Completion 是不同的檢查。這裡說的命令回覆，也不等同於 Data Link Layer 的 Ack。</p>
<p class="source-note">來源：§4.2.18.2–§4.2.18.3，文件／PDF pp.557–561；Figures 7-129／7-130、Tables 7-114／7-115，pp.1082–1083。</p></section>

<section id="margin-example"><h2>查完能力，再向右移 5 steps，回報怎麼讀？</h2>
<p>延續前面的模擬配置，Rx(F) 的能力回覆假設如下。<strong>下表每一列新命令之前，都已完成 No Command 交握</strong>，包括只改 Payload 的情況。Table 4-63 左半部是命令，右半部是回覆；Report 類命令的回覆 Payload 會換成所查的值。</p>
<div class="table-wrap"><table><thead><tr><th scope="col">命令／觀察時點</th><th scope="col">寫入 Control</th><th scope="col">讀到 Status</th><th scope="col">如何解讀？</th></tr></thead><tbody>
<tr data-margin-case="cap"><td>Report Margin Control Capabilities</td><td>880Eh</td><td>150Eh</td><td>Payload=15h：獨立錯誤取樣器、以 sample count 回報、支援左右分開的 timing，也支援 voltage；不支援上下分開的 voltage</td></tr>
<tr data-margin-case="steps"><td>Report MNumTimingSteps</td><td>8A0Eh</td><td>200Eh</td><td>回報 32 steps；這是接收端宣告的步數上限</td></tr>
<tr data-margin-case="offset"><td>Report MMaxTimingOffset</td><td>8B0Eh</td><td>190Eh</td><td>回報最大時間位移為 nominal UI（標稱單位間隔）的 25%</td></tr>
<tr data-margin-case="limit"><td>Set Error Count Limit</td><td>C516h</td><td>C516h</td><td>Payload 高兩位為 11b、低六位為 5；接收端回報已登記的錯誤上限 5</td></tr>
<tr data-margin-case="setup"><td>Step Margin：向右 5 steps，剛開始</td><td>051Eh</td><td>401Eh</td><td>Payload 高兩位 01b：仍在準備，尚未開始執行步進量測；錯誤計數為 0</td></tr>
<tr data-margin-case="running"><td>同一命令，稍後讀取</td><td>051Eh</td><td>801Eh</td><td>10b：量測執行中；錯誤計數為 0</td></tr>
<tr data-margin-case="errors"><td>同一命令，再次讀取</td><td>051Eh</td><td>821Eh</td><td>10b：仍在執行；MErrorCount=2，未超過本例上限 5</td></tr>
</tbody></table></div>
<p>例如 880Eh 可拆成 <code>(88h &lt;&lt; 8) | (001b &lt;&lt; 3) | 110b</code>。Report Margin Control Capabilities 的 Payload=15h，其 bit 4 是 MIndErrorSampler、bit 3 是 MSampleReportingMethod、bit 2 是 MIndLeftRightTiming、bit 1 是 MIndUpDownVoltage、bit 0 是 MVoltageSupported。bit 3=0 表示使用 sample count；bit 1=0 只表示不能分開選上下方向，並不否定 bit 0 宣告的 voltage 支援。</p>
<p>Step Margin 的 Payload=05h，則依 §4.2.18.1.2 解讀：本例 MIndLeftRightTiming=1，bit 6=0 選右邊、bits [5:0]=5 選步數。Table 8-12 要求位移隨步數單調增加，沒有保證每一步都是等距；因此知道 32 steps 對應最大 25% UI，仍不能把第 5 step 直接按比例換成固定時間。</p>
<p>回到 Status=821Eh，Payload=82h 的高兩位是執行狀態，低六位才是 MErrorCount（本次裕量測試的錯誤計數）。因為本例使用獨立錯誤取樣器，這個 2 是該取樣器偵測到的 bit errors，Link 的正常資料流可能仍然沒有錯誤。若 MIndErrorSampler=0，計數改依 §4.2.18.2 的邏輯錯誤條件解讀，例如 Port 進入 Recovery；兩種計數不能混在一起比較。</p>
<p>量測仍在執行時，軟體須依回報方式取得實際取樣量；本例可在完成必要交握後使用 Report MSampleCount。規格<strong>建議</strong>每個位置至少量到 10<sup>8</sup> bits 再換下一步，錯誤上限已超過時例外；準備期間尚未量測，不能算進取樣量。本例尚未提供取樣量，因此這幾個 Status 只示範命令與執行狀態的讀法，還不足以完成該位置的裕量評估。單次讀到 0 errors，只描述已觀察到的樣本。</p>
<p>另外兩個 Step Margin 回報是：11b 表示 NAK（不支援這筆裕量命令），MErrorCount=0；00b 表示錯誤過多，接收端已自動回到正常取樣位置。使用獨立取樣器時，超過上限是否自動結束是可選行為，所以仍須讀執行狀態。硬體的 01b 準備狀態不得持續超過收到新有效命令後的 100 ms；軟體若從發命令起已等 200 ms 仍看到 01b，可以判定該接收端 margining 失敗。這裡的 NAK 是裕量命令的執行回報，與 Data Link Layer 要求重送的 Nak 不同。</p>
<p class="source-note">來源：§4.2.18.1–§4.2.18.3、Table 4-63 <em>Margin Commands and Corresponding Responses</em>，文件／PDF pp.553–561；§8.4.4、Table 8-12 <em>Lane Margining</em>，pp.1395–1398。</p></section>

<section id="restore"><h2>讀到結果後，怎麼結束這個方向的測試？</h2>
<p>No Command 用來分隔命令，<strong>不會自動把持續中的 Step Margin 移回正常位置</strong>。一個測試方向結束時，先完成更換命令前所需的 No Command 交握。接著依 §4.2.18.3，於 Downstream 與 Upstream Ports 依序 broadcast 下列命令，而且每一步都先確認接收端回覆，再送下一步。本例無 Retimer，回覆的接收端分別是 Root Port 的 Rx(A) 與 Endpoint 的 Rx(F)。</p>
<ol><li>Go to Normal Settings：本例 Control=0F10h，恢復正常取樣位置。</li><li>No Command：本例 Control=9C38h，等待交握完成。</li><li>Clear Error Log：本例 Control=5510h，清除裕量量測累積的錯誤計數。</li><li>No Command：本例 Control=9C38h，再確認回覆。</li></ol>
<p>上述 Control 的 Receiver=000b 表示 broadcast；有效回覆除 No Command 外，會帶回實際回覆者的 Receiver Number。因此 Endpoint 的 Go to Normal Settings 回覆本例是 0F16h，Root Port 的回覆則是 0F11h。命令與 Status 不必逐 bit 相同。Clear Error Log 清的是 margining 錯誤紀錄，不是清除 AER（進階錯誤回報）的全部 Status。</p><dl class="st-terms" aria-label="本段名詞"><div><dt>AER</dt><dd>Advanced Error Reporting，進階錯誤回報</dd></div></dl>
<p>整個測試程序完成後，恢復先前保存的自主變速／變寬 Disable 值。若量測期間速率改變，結果不準確，軟體必須退出程序並把 Control 設為 No Command，避免日後回到 16.0 GT/s 以上時意外重新啟動。若 Link 進入 Recovery，還須按獨立或共用取樣器的規則處理暫停、回到預設位置與恢復測試；僅看到再次進入 L0，無法把前後資料視為同一段連續量測。</p>
<p class="source-note">來源：§4.2.18，文件／PDF p.550；§4.2.18.1–§4.2.18.3，pp.553–561。</p></section>
<section id="logs"><h2>Margining 與 Flit 紀錄，各自回答什麼問題？</h2><p>前面的 Margining 會改變測試條件，並回報指定取樣位置的表現。若只想看傳輸期間記錄的錯誤，則按用途選下面的結構；Flit Mode（固定長度傳輸單位模式）的格式與重送原理見 <a href="/DOCS/pcie-course/chapter-18.html">Chapter 18</a>。</p><div class="table-wrap"><table><thead><tr><th scope="col">想觀察的內容</th><th scope="col">規格入口</th><th scope="col">適用條件與用途</th></tr></thead><tbody><tr><td>64.0 GT/s 實體層狀態</td><td>§7.7.7／Figure 7-97，pp.1055–1056</td><td>讀 Equalization 與相關速率狀態；未支援 64.0 GT/s 時，標頭以外暫存器的行為未定義</td></tr><tr><td>Flit 錯誤紀錄、錯誤計數與 FBER 量測</td><td>§7.7.8／Figure 7-103，pp.1060–1061</td><td>只在 Flit Mode 生效；紀錄、Counter Control／Status 與 FBER（First Bit Error Rate，第一位元錯誤率）量測各有自己的欄位與條件</td></tr><tr><td>初始寬度、Segment 等資訊</td><td>§7.7.9／Figure 7-120、Table 7-110，pp.1072、1077</td><td>Device Status 3 的 Initial Link Width 是初次訓練結果；目前寬度另讀 Negotiated Link Width</td></tr><tr><td>主動注入測試錯誤</td><td>§7.8.13／Figure 7-211，pp.1171–1172</td><td>Flit Error Injection（Flit 錯誤注入）是可選能力，只在 Flit Mode 生效；找到結構後，仍須另外選擇是否啟動測試</td></tr></tbody></table></div><p>Retimer 的裕量命令則由 Downstream Port 代送，透過 Control SKP Ordered Set（帶 Link 控制資訊的 SKP 序列）向下傳遞，回報向上返回。這仍是同一條 Link 內的接收端定位；本章案例的 Endpoint Rx(F) 使用自己的 Control／Status，不套用 Retimer 的代送路徑。</p></section>
<section id="result"><h2>怎樣保存一份可以再分析的結果？</h2><p>保存 Port／Function、預設 Lane、Receiver Number、速率與模式、能力回報、測試方向、步數、開始／結束時間、執行狀態、錯誤計數及取樣量。另記錄重訓練、速率改變與復原命令。這樣才能知道兩筆數據是否量到同一個位置、同一種錯誤，以及相近的樣本數。</p><p>§7.7.7 另提醒：64.0 GT/s 的 parity 錯誤記在名稱為 16.0 GT/s 的 Local／First Retimer／Second Retimer Data Parity Mismatch Status Registers。若要追蹤特定速率的錯誤，軟體<strong>應</strong>在速率改變時清除這些紀錄；先保存舊紀錄，再開始下一段觀察。</p><p>本例完成的是接收端能力查詢、單一 timing 位置的判讀與復原。完整裕量輪廓還需要逐一測其他位置、方向並取得足夠樣本。各速率參數可以不同；16.0 GT/s 的 voltage margining 是可選，32.0／64.0 GT/s 則要求支援。64.0 GT/s 的 Step Margin 同時作用於 PAM4（四階訊號）的三個眼，仍須按該速率參數解讀。這些接收端內部觀察不等同於 <a href="/DOCS/pcie-course/chapter-21.html">Chapter 21 的外部 stressed-eye 與 BER 測試</a>，也不足以單獨宣告完整電氣符合性。</p><dl class="st-terms" aria-label="本段名詞"><div><dt>PAM4</dt><dd>Pulse Amplitude Modulation with 4 levels，四階脈衝振幅調變</dd></div></dl></section><section id="sources"><h2>版本與來源</h2><p>本章依 PCI Express Base Specification Revision 6.0（6.0-1.0-PUB）；以下文件印刷頁與 PDF 檢視器頁碼相同。命令讀值為教學假設，未執行實機測試。</p><details class="source-note"><summary>完整來源定位</summary><ul><li>§4.2.18 <em>Lane Margining at Receiver</em>, pp.550–561; §4.2.18.1 <em>Receiver Number, Margin Type, Usage Model, and Margin Payload Fields</em>, pp.551–557; Figure 4-60 <em>Receiver Number Assignment</em>, p.553; Table 4-63 <em>Margin Commands and Corresponding Responses</em>, pp.554–556.</li><li>§4.2.18.2 <em>Margin Command and Response Flow</em>, pp.557–560; §4.2.18.3 <em>Receiver Margin Testing Requirements</em>, pp.560–561.</li><li>§7.7.10 <em>Lane Margining at the Receiver Extended Capability</em>, pp.1077–1083; Figure 7-125 (layout), pp.1079–1080; Figure 7-126 / Table 7-111 (header), p.1080; Figure 7-127 / Table 7-112 (port capabilities), pp.1080–1081; Figure 7-128 / Table 7-113 (port status), p.1081; Figure 7-129 / Table 7-114 <em>Lane N: Margining Control Register Entry</em>, p.1082; Figure 7-130 / Table 7-115 <em>Lane N: Margining Lane Status Register Entry</em>, p.1083.</li><li>§8.4.4 <em>Lane Margining at the Receiver - Electrical Requirements</em>, pp.1395–1398; Table 8-12 <em>Lane Margining</em>, pp.1396–1398.</li><li>§4.2.3.1.1 <em>PAM4 Signaling</em>, p.343 (FBER); §7.7.7 <em>Physical Layer 64.0 GT/s Extended Capability</em>, pp.1055–1056, Figure 7-97; §7.7.8 <em>Flit Logging Extended Capability</em>, pp.1060–1061, Figure 7-103 <em>Flit Logging Extended Capability Structure</em>; §7.7.9 <em>Device 3 Extended Capability Structure</em>, p.1072, Figure 7-120; §7.7.9.4 / Table 7-110 <em>Device Status 3 Register</em>, p.1077; §7.8.13 <em>Flit Error Injection Extended Capability</em>, pp.1171–1172, Figure 7-211 <em>Flit Error Injection Extended Capability Structure</em>.</li></ul></details></section>
</article>
<nav class="bottom-nav" aria-label="課程與語言版本"><a href="/DOCS/pcie-course/index.html">課程總覽</a><a href="/DOCS/pcie-course/chapter-22.html">繁中完整教學</a><a href="/pcie/chapter-22-en/">English</a></nav>
</div>
