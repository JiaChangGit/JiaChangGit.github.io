---
layout: post
title: "PCIe Chapter 1：拓撲、交易角色與逐 Link 判讀"
date: 2026-10-20 00:00:00 +0800
last_modified_at: 2026-10-24 00:00:00 +0800
permalink: /pcie/chapter-1-zh-tw/
categories: [PCIe]
tags: [PCIe, Specification]
lang: zh-TW
spec_teaching: true
spec_series: pcie
description: "以同一個 Switch 拓撲帶讀元件、Function、Port 與 Link，追蹤 Read 往返角色，再比較連線能力、目前結果與欄位適用性。"
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
<nav class="bottom-nav" aria-label="課程與語言版本"><a href="/DOCS/pcie-course/index.html">課程總覽</a><a href="/DOCS/pcie-course/chapter-1.html">繁中完整教學</a><a href="/pcie/chapter-1-en/">English</a></nav>
<article class="lesson">
<p class="lead">先把拓撲上的元件、Port 與 Link 分清楚，再沿一筆 Memory Read 的往返，辨認固定的拓撲方向與當次傳輸角色。接著把設定欄位放回同一條 Link，讀懂能力、目前結果與軟體識別。</p>
<aside class="example"><strong>【模擬資料】以下資料為教學用途建立，不代表特定硬體或平台。</strong><p>卡片配置、編號與讀值是作者假設；Link 已建立，Function 已確認存在，查詢期間拓撲保持不變。</p></aside>
<figure class="diagram"><svg viewBox="0 0 840 585" class="course-diagram" role="img" aria-labelledby="ch1-topology-svg-title ch1-topology-svg-desc"><title id="ch1-topology-svg-title">沿拓樸找到 03:00.1</title><desc id="ch1-topology-svg-desc">所有BDF皆在Segment 0000；實線是外部Link，虛線是內部邏輯連接；Endpoint A的兩個Function共用一條Link。</desc><g><rect x="285" y="20" width="270" height="80" rx="10" fill="var(--blue-soft)" stroke="var(--line)" stroke-width="2"/><text x="420" y="47" text-anchor="middle" fill="var(--ink)" font-size="18">Root Port</text><text x="420" y="72" text-anchor="middle" fill="var(--ink)" font-size="16">00:01.0 · 01–04</text></g><g><rect x="285" y="155" width="270" height="80" rx="10" fill="var(--blue-soft)" stroke="var(--line)" stroke-width="2"/><text x="420" y="182" text-anchor="middle" fill="var(--ink)" font-size="18">Switch Upstream Port</text><text x="420" y="207" text-anchor="middle" fill="var(--ink)" font-size="16">01:00.0 · 02–04</text></g><g><rect x="35" y="330" width="300" height="80" rx="10" fill="var(--blue-soft)" stroke="var(--line)" stroke-width="2"/><text x="185" y="357" text-anchor="middle" fill="var(--ink)" font-size="18">Downstream Port A</text><text x="185" y="382" text-anchor="middle" fill="var(--ink)" font-size="16">02:01.0 · 03–03</text></g><g><rect x="505" y="330" width="300" height="80" rx="10" fill="var(--blue-soft)" stroke="var(--line)" stroke-width="2"/><text x="655" y="357" text-anchor="middle" fill="var(--ink)" font-size="18">Downstream Port B</text><text x="655" y="382" text-anchor="middle" fill="var(--ink)" font-size="16">02:02.0 · 04–04</text></g><g><rect x="35" y="475" width="300" height="80" rx="10" fill="var(--blue-soft)" stroke="var(--line)" stroke-width="2"/><text x="185" y="502" text-anchor="middle" fill="var(--ink)" font-size="18">Endpoint A</text><text x="185" y="527" text-anchor="middle" fill="var(--ink)" font-size="16">03:00.0 / 03:00.1</text></g><g><rect x="505" y="475" width="300" height="80" rx="10" fill="var(--blue-soft)" stroke="var(--line)" stroke-width="2"/><text x="655" y="502" text-anchor="middle" fill="var(--ink)" font-size="18">Endpoint B</text><text x="655" y="527" text-anchor="middle" fill="var(--ink)" font-size="16">04:00.0</text></g><g><path d="M420 100 V155" fill="none" stroke="var(--accent)" stroke-width="2.5"/><text x="465" y="132" text-anchor="middle" fill="var(--ink)" font-size="15">LR</text></g><g><path d="M420 235 V280 H185 V330 M420 280 H655 V330" fill="none" stroke="var(--accent)" stroke-width="2.5" stroke-dasharray="6 5"/><text x="420" y="270" text-anchor="middle" fill="var(--ink)" font-size="15">內部 Bus 02（邏輯連接）</text></g><g><path d="M185 410 V475" fill="none" stroke="var(--accent)" stroke-width="2.5"/><text x="225" y="450" text-anchor="middle" fill="var(--ink)" font-size="15">LA</text></g><g><path d="M655 410 V475" fill="none" stroke="var(--accent)" stroke-width="2.5"/><text x="695" y="450" text-anchor="middle" fill="var(--ink)" font-size="15">LB</text></g></svg><figcaption>作者的 Segment 0000 配置快照。實線為外部 Link，虛線為 Switch 內部邏輯連接；Endpoint A 的兩個 Function 共用一條 Link。Base 6.0 Figures 1-3／7-2，文件頁／PDF 頁 107、904。</figcaption></figure>

<p><a href="/DOCS/pcie-course/chapter-1.html">完整中文教學與拓樸圖</a> · <a href="/DOCS/pcie-course/index.html">課程路線</a> · <a href="/pcie/chapter-1-en/">English</a></p>
<aside class="note"><strong>版本與範圍</strong><p>架構與欄位依 PCI Express Base Specification Revision 6.0；後半部 Segment 的補充另列 PCI Firmware 3.3。文件頁與 PDF 檢視器頁相同。本例使用一般多功能裝置的編址，沒有套用進階 Function 編號機制。</p></aside>

<section id="objects"><h2>一張卡、Function 與 Link，要分別記錄什麼？</h2>
<p>component 是單一實體封裝；Device 是同一階層中具有共同 Bus Number 與 Device Number 的 Function 集合。Function 是可在設定空間個別定址的功能，Port 則是元件連接 Link 的介面。</p>
<p>Link 包含相鄰兩端 Port 與其間的 Lane。每條 Lane 有一組傳送差動對及一組接收差動對；x4 表示四條 Lane 組成一條 Link。本例 A 的兩個 Function 共用一個 Port 與 LA，所以兩份設定資料不會增加外部連線數量。</p>
<p>圖上以 Endpoint A 簡稱提供端點功能的元件；規格的 Endpoint 是 Function 類型。實體卡片、封裝、設定對象與外部連線各有用途，分析時先寫出當前所指的對象。</p>
<p class="source-ref">Base 6.0 Terms and Acronyms：component、Device、Function、Lane、Link、Port，文件頁／PDF 頁 83–85、87、89；§1.2，pp.100–102。</p></section>

<section id="roles"><h2>Read 往返時，哪些角色保持不變？</h2>
<p>Switch 的 Upstream Port 朝向 Root Complex，Downstream Port 朝向下游；這些名稱由拓撲決定。Requester 是發起交易的 Function，Completer 負責處理原 Request 並產生所需回覆。Transmitter 與 Receiver 則依某一次 Link 傳輸指定。</p>
<!-- pcie-walk: walks/chapter1-roles.json -->
<div class="guided-walk" id="ch1-roles" role="group" aria-labelledby="ch1-roles-title" data-walk-version="1">
<h3 id="ch1-roles-title">同一筆 Read，逐段看誰在傳、誰在收</h3>
<p class="walk-help" id="ch1-roles-help">選擇步驟後，圖中對應的元件與下方解說會加上重點標示。完整圖與所有解說會持續顯示；也可用方向鍵切換步驟。</p>
<div class="walk-order"><p>先沿 Request 從 A 走到主機，再沿 Completion 返回；每條實線都重新指定傳送端與接收端。LA、LR 是本章用來追蹤連線的代號。</p></div>
<input class="walk-choice" type="radio" name="ch1-roles-step" id="ch1-roles-choice-1" value="1" data-walk-step="1" aria-describedby="ch1-roles-help" aria-controls="ch1-roles-view ch1-roles-step-1" checked="checked">
<label class="walk-label" for="ch1-roles-choice-1">1. A 發出 Request：先通過 LA</label>
<input class="walk-choice" type="radio" name="ch1-roles-step" id="ch1-roles-choice-2" value="2" data-walk-step="2" aria-describedby="ch1-roles-help" aria-controls="ch1-roles-view ch1-roles-step-2">
<label class="walk-label" for="ch1-roles-choice-2">2. Switch 轉送 Request：再通過 LR</label>
<input class="walk-choice" type="radio" name="ch1-roles-step" id="ch1-roles-choice-3" value="3" data-walk-step="3" aria-describedby="ch1-roles-help" aria-controls="ch1-roles-view ch1-roles-step-3">
<label class="walk-label" for="ch1-roles-choice-3">3. 主機一端回傳 Completion：通過 LR</label>
<input class="walk-choice" type="radio" name="ch1-roles-step" id="ch1-roles-choice-4" value="4" data-walk-step="4" aria-describedby="ch1-roles-help" aria-controls="ch1-roles-view ch1-roles-step-4">
<label class="walk-label" for="ch1-roles-choice-4">4. Switch 轉送 Completion：經 LA 回到 A</label>
<div class="walk-view" id="ch1-roles-view">
<figure class="diagram walk-diagram">
<svg viewBox="0 0 760 470" role="img" aria-labelledby="ch1-roles-svg-title ch1-roles-svg-desc"><title id="ch1-roles-svg-title">同一筆 Memory Read 的角色與傳輸方向</title><desc id="ch1-roles-svg-desc">由上往下追蹤 Endpoint A Function 1 的 Request，再追蹤 Root Complex 返回的 Completion。Link LA 連接 Endpoint Port 與 Switch Downstream Port A；Link LR 連接 Switch Upstream Port 與 Root Port。Switch 內部轉送以虛線表示。</desc><g fill="none" stroke="var(--line)" stroke-width="2" stroke-dasharray="5 5"><path d="M90 88 V440" /><path d="M285 88 V440" /><path d="M475 88 V440" /><path d="M670 88 V440" /></g><g data-walk-target="ep" class="walk-node" data-walk-steps="1 4"><rect x="12" y="14" width="156" height="72" rx="8" fill="var(--blue-soft)" stroke="var(--line)" /><text x="90" y="42" text-anchor="middle" fill="var(--ink)" font-size="18">Endpoint A Port</text><text x="90" y="68" text-anchor="middle" fill="var(--ink)" font-size="17">Function 1</text></g><g data-walk-target="dp" class="walk-node" data-walk-steps="1 4"><rect x="205" y="14" width="160" height="72" rx="8" fill="var(--blue-soft)" stroke="var(--line)" /><text x="285" y="42" text-anchor="middle" fill="var(--ink)" font-size="18">Switch DP A</text><text x="285" y="68" text-anchor="middle" fill="var(--ink)" font-size="16">Downstream Port</text></g><g data-walk-target="up" class="walk-node" data-walk-steps="2 3"><rect x="395" y="14" width="160" height="72" rx="8" fill="var(--blue-soft)" stroke="var(--line)" /><text x="475" y="42" text-anchor="middle" fill="var(--ink)" font-size="18">Switch UP</text><text x="475" y="68" text-anchor="middle" fill="var(--ink)" font-size="16">Upstream Port</text></g><g data-walk-target="rp" class="walk-node" data-walk-steps="2 3"><rect x="592" y="14" width="156" height="72" rx="8" fill="var(--blue-soft)" stroke="var(--line)" /><text x="670" y="42" text-anchor="middle" fill="var(--ink)" font-size="18">Root Port</text><text x="670" y="68" text-anchor="middle" fill="var(--ink)" font-size="17">Root Complex</text></g><g data-walk-target="req-a" class="walk-node" data-walk-steps="1"><path d="M90 140 H277" stroke="var(--accent)" stroke-width="3" /><path d="M277 135 L285 140 L277 145 Z" fill="var(--accent)" /><text x="187" y="126" text-anchor="middle" fill="var(--ink)" font-size="18">LA: Memory Read</text></g><g data-walk-target="inside-up" class="walk-node" data-walk-steps="2"><path d="M285 185 H467" stroke="var(--accent)" stroke-width="2.5" stroke-dasharray="6 5" /><path d="M467 180 L475 185 L467 190 Z" fill="var(--accent)" /><text x="380" y="172" text-anchor="middle" fill="var(--muted)" font-size="16">Switch forwarding</text></g><g data-walk-target="req-root" class="walk-node" data-walk-steps="2"><path d="M475 230 H662" stroke="var(--accent)" stroke-width="3" /><path d="M662 225 L670 230 L662 235 Z" fill="var(--accent)" /><text x="572" y="216" text-anchor="middle" fill="var(--ink)" font-size="18">LR: Memory Read</text></g><g data-walk-target="cpl-root" class="walk-node" data-walk-steps="3"><path d="M670 320 H483" stroke="var(--accent)" stroke-width="3" /><path d="M483 315 L475 320 L483 325 Z" fill="var(--accent)" /><text x="572" y="306" text-anchor="middle" fill="var(--ink)" font-size="18">LR: Completion</text></g><g data-walk-target="inside-down" class="walk-node" data-walk-steps="4"><path d="M475 365 H293" stroke="var(--accent)" stroke-width="2.5" stroke-dasharray="6 5" /><path d="M293 360 L285 365 L293 370 Z" fill="var(--accent)" /><text x="380" y="352" text-anchor="middle" fill="var(--muted)" font-size="16">Switch forwarding</text></g><g data-walk-target="cpl-a" class="walk-node" data-walk-steps="4"><path d="M285 410 H98" stroke="var(--accent)" stroke-width="3" /><path d="M98 405 L90 410 L98 415 Z" fill="var(--accent)" /><text x="187" y="396" text-anchor="middle" fill="var(--ink)" font-size="18">LA: Completion</text></g><text x="380" y="460" text-anchor="middle" fill="var(--muted)" font-size="16">Request: Upstream → Root Complex · Completion: Downstream → Endpoint</text></svg>
<figcaption>作者依規格建立的角色時序圖。由上往下讀事件，不表示實際延遲；實線是 LA／LR 上的傳送，虛線是 Switch 內部轉送。圖中 DP／UP 分別表示 Downstream Port／Upstream Port。</figcaption></figure>
<div class="walk-summary"><p class="lead">Upstream／Downstream Port 的名稱由拓撲決定。Transmitter／Receiver 隨當次傳送改變；同一筆 Read 的 Requester 不會因開始接收 Completion 而改名。</p></div>
<ol class="walk-steps">
<li class="walk-step" id="ch1-roles-step-1" data-walk-step="1" data-walk-targets="ep dp req-a"><h4>A 發出 Request：先通過 LA</h4><div class="walk-condition"><p>本例由 Function 1 讀取主機記憶體；只追蹤一筆可用一個 Completion 回覆的 Read，省略仲裁、重送與其他流量。</p></div><div class="walk-explanation"><p>Endpoint A 的 Function 1 是 Requester（發起這筆交易的功能）。在 LA 上，A 的 Port 是 Transmitter（傳送端），Switch Downstream Port A 是 Receiver（接收端）。Request 朝 Root Complex 前進，所以方向是 Upstream。</p></div><div class="walk-source" data-source-claims="PCIE-CH1-ROLES-001 PCIE-CH1-EXAMPLE-001"><p>Base 6.0 Terms and Acronyms：Requester、Receiver、Transmitter、Upstream，文件頁／PDF 頁 90、93–94；Figure 1-3，p.107。</p></div></li>
<li class="walk-step" id="ch1-roles-step-2" data-walk-step="2" data-walk-targets="up rp req-root inside-up"><h4>Switch 轉送 Request：再通過 LR</h4><div class="walk-condition"><p>觀察點已從 LA 改到 LR；Switch 轉送同一筆 Request，不在此例另行發起交易。</p></div><div class="walk-explanation"><p>Switch 將 Request 轉到自己的 Upstream Port，再送給 Root Port。這一段由 Switch 的 Upstream Port 傳送、Root Port 接收。原始 Requester 仍是 A 的 Function 1；Switch 內部的虛線只表示轉送，不是另一條外部 Link。</p></div><div class="walk-source" data-source-claims="PCIE-CH1-ROLES-001 PCIE-CH1-BDF-001"><p>Base 6.0 §1.3.3／Figure 1-3，p.107；§2.2.6.2，p.157：Switch 轉送時保留 Transaction ID。</p></div></li>
<li class="walk-step" id="ch1-roles-step-3" data-walk-step="3" data-walk-targets="rp up cpl-root"><h4>主機一端回傳 Completion：通過 LR</h4><div class="walk-condition"><p>假設 Read 已被正確處理，Completer 正在回覆資料。本圖不由單一 Link 的傳送推定所有交易成功。</p></div><div class="walk-explanation"><p>Root Complex 一端的 Completer（處理原 Request 並產生回覆的功能）返回 Completion。LR 上改成 Root Port 傳送、Switch Upstream Port 接收。資料方向變成 Downstream；Upstream Port 的名稱保持不變。</p></div><div class="walk-source" data-source-claims="PCIE-CH1-ROLES-001"><p>Base 6.0 Terms and Acronyms：Completer、Completion、Downstream、Receiving/Transmitting Port，文件頁／PDF 頁 82–84、90、93。</p></div></li>
<li class="walk-step" id="ch1-roles-step-4" data-walk-step="4" data-walk-targets="dp ep cpl-a inside-down"><h4>Switch 轉送 Completion：經 LA 回到 A</h4><div class="walk-condition"><p>這是同一筆 Read 的返回路徑；Completion 欄位與完整性檢查會在交易章繼續帶讀。</p></div><div class="walk-explanation"><p>Switch 從 Downstream Port A 將 Completion 送回 A。LA 上改成 Downstream Port A 傳送、A 的 Port 接收。A 的 Function 1 仍是原始 Requester，現在是在接收回覆；Requester 不是「此刻正在傳送的那一端」。</p></div><div class="walk-source" data-source-claims="PCIE-CH1-ROLES-001"><p>Base 6.0 Terms and Acronyms：Requester、Completer、Completion；§1.3.3／Figure 1-3，文件頁／PDF 頁 82–83、90、107。</p></div></li>
</ol></div>
</div>
<!-- /pcie-walk -->
<p>本例只沿同一個 Root Port 的下游路徑往返，沒有套用 Root Complex 跨 Root Port 轉送時的特殊規則。普通 Switch 的轉送與原始 Requester 身分須分開記錄。</p>
<p class="source-ref">Base 6.0 Terms and Acronyms，文件頁／PDF 頁 82–84、90、93–94；§1.3.1，pp.103–104；§1.3.3／Figure 1-3，p.107；§2.2.6.2，p.157。</p></section>
<section id="links"><h2>同一個 Switch，為什麼需要三組 Link 資料？</h2>
<div class="table-wrap"><table><caption>沿外部實線配對 Link Partner</caption><thead><tr><th scope="col">Link</th><th scope="col">兩端 Port</th><th scope="col">本例的觀察範圍</th></tr></thead><tbody>
<tr><td>LR</td><td>Root Port ↔ Switch Upstream Port</td><td>主機與 Switch。</td></tr>
<tr><td>LA</td><td>Switch Downstream Port A ↔ Endpoint A Port</td><td>Switch 與卡 A；A 的兩個 Function 共用。</td></tr>
<tr><td>LB</td><td>Switch Downstream Port B ↔ Endpoint B Port</td><td>Switch 與卡 B。</td></tr>
</tbody></table></div>
<p>Switch 內部的虛線是邏輯連接，沒有多出第四條外部 Link。調查 A 時，先取得 LA 的兩端；Switch Upstream Port 的 Link Status 描述 LR。若再串接第二層 Switch，則為新增的每條 Link 重新配對相鄰 Port。</p>
<p class="source-ref">Base 6.0 §1.2–§1.3，Figure 1-2 Example PCI Express Topology、Figure 1-3 Logical Block Diagram of a Switch，文件頁／PDF 頁 100–107。</p></section>
<section id="path-capabilities">
<h2>卡 A 支援 64.0 GT/s，主機到卡 A 的路徑也一樣嗎？</h2>
<p>先逐條 Link 比較兩端支援能力，再另外記錄目前速率與寬度。下面沿用同一拓撲；數值是假設兩端同步取得、且 Link 已建立的解碼結果，尚未提供 Target、訓練歷史或板上 Lane 接線資料。</p>
<div class="table-wrap"><table><caption>教學快照：能力、共同上限與目前結果</caption><thead><tr><th scope="col">Link</th><th scope="col">兩端各自的最高速率／最大寬度</th><th scope="col">共同支援的最高速率與寬度上限</th><th scope="col">兩端一致回報的目前結果</th></tr></thead><tbody>
<tr><td>LR</td><td>Root Port：32.0 GT/s、x8<br>Switch Upstream Port：32.0 GT/s、x8</td><td>32.0 GT/s、x8</td><td>32.0 GT/s、x8</td></tr>
<tr><td>LA</td><td>Downstream Port A：64.0 GT/s、x8<br>Endpoint A Port：64.0 GT/s、x8</td><td>64.0 GT/s、x8</td><td>16.0 GT/s、x4</td></tr>
<tr><td>LB</td><td>Downstream Port B：16.0 GT/s、x4<br>Endpoint B Port：16.0 GT/s、x4</td><td>16.0 GT/s、x4</td><td>8.0 GT/s、x4</td></tr>
</tbody></table></div>
<p><strong>先讀 LA：</strong>A 的 Port 與 Downstream Port A 都支援 64.0 GT/s，但目前共同運作於 16.0 GT/s、x4。這是能力與目前結果的比較；要解釋為什麼採用這個結果，還需要有效的控制設定、實際接線與訓練紀錄。</p>
<p><strong>再沿路讀 LR：</strong>卡 A 與主機之間還經過 LR，其兩端最高支援 32.0 GT/s。資料經 Switch 在不同 Link 之間轉送，各條 Link 分別訓練與運作；整條路徑不會共同協商成一個速率。因此，Endpoint 的 64.0 GT/s 能力描述的是自己的 Port，不能代替上游 Link 的資料。</p>
<p>這張表也不能直接推算應用效能。資料量、其他分支流量、封包與傳輸開銷都會影響實際進度。這裡只先建立逐 Link 比較的方法。</p>
<ol class="route"><li><strong>先定位能力欄位</strong><br>Figure 7-27／Table 7-23：讀 Max Link Speed 與 Maximum Link Width；Figure 7-38／Table 7-35：讀 Supported Link Speeds Vector。</li><li><strong>再定位目前結果</strong><br>Figure 7-29／Table 7-26：讀 Current Link Speed 與 Negotiated Link Width；Link 未建立時，這兩個值的定義有條件。</li><li><strong>把讀值放回同一條 Link</strong><br>先比相鄰兩端，再沿拓撲換到下一條 Link；設定、目前狀態與事件紀錄分欄保留。</li></ol>
<p>以上是規格查閱順序，不是 Link Training 的執行時序。欄位位移與速率編碼的完整讀法可接回 <a href="/DOCS/pcie-course/chapter-0.html#case">Chapter 0 的查詢案例</a>；本節將重點放在讀值描述哪一個 Port 與哪一條 Link。</p>
<details class="source-note"><summary>能力與狀態欄位的正式位置</summary><p>Base 6.0 §7.5.3.6 Link Capabilities Register (Offset 0Ch)，Figure 7-27／Table 7-23，文件頁／PDF 頁 966–969；Maximum Link Width 可大於實際接線寬度的規則在 p.967。§7.5.3.18 Link Capabilities 2 Register (Offset 2Ch)，Figure 7-38／Table 7-35，p.998，定義 Supported Link Speeds Vector；本例各 Port 支援從 2.5 GT/s 到其最高速率之間的全部速率。§7.5.3.8 Link Status Register (Offset 12h)，Figure 7-29／Table 7-26，pp.977–979，定義 Current Link Speed、Negotiated Link Width 及欄位適用性。逐 Link 初始化見 §1.2，p.102。</p></details>
</section>

<section id="root-peer-path"><h2>兩個 Endpoint 在不同 Root Port 下，一定能互相存取嗎？</h2><p>【模擬資料】假設 Endpoint A、B 分別位於同一個 Root Complex（RC）的不同 Root Port 下。先沿 Figure 1-2 找出兩個 hierarchy domain：若 A 要存取 B，路徑需要經過 RC。Base 6.0 §1.3.1 把跨 domain 的 peer-to-peer 路由列為可選且取決於實作；兩個 Endpoint 都能被列舉，仍不足以證明 RC 提供這條路徑。</p><p>RC 支援這種路由時，可以採不同設計：例如接手 Request、重新形成必要的封包並處理返回的 Completion，也可以在內部採用實體或虛擬 Switch。§1.3.1 一般允許 RC 在跨 domain 轉送時拆分封包；相對地，§1.3.3 不允許 Switch 把一個封包拆成更小的封包。兩者都須遵守各自適用的封包規則，不能把某一種實作當成所有平台的路徑。</p><p>拆分也有例外：RC 轉送 Deferrable Memory Write Request 時不得拆分；Vendor-Defined Message 若要拆分，受 128-byte 邊界條件限制。實際分析還須確認平台路由、各 Bridge Window、目標 BAR 與存取政策；本題只由拓撲確認需要經過 RC，無法保證 Request 會到達 B。</p><dl class="st-terms" aria-label="本段名詞"><div><dt>BAR</dt><dd>Base Address Register，基底位址暫存器</dd></div></dl><p class="source-note">Base 6.0 §1.3、Figure 1-2，pp.102–103；§§1.3.1、1.3.3，pp.103–104、106–107；Deferrable Memory Write 的細節見 §6.32。</p></section>
<section id="integrated-endpoint"><h2>找到 Endpoint，為什麼有時沒有可配對的 Link？</h2><p>前面案例的插卡是接在 Port 外部的 Endpoint。Figure 1-2 還有另一種位置：Root Complex Integrated Endpoint（RCiEP，整合在 Root Complex 內的 Endpoint）。它仍是一個 Function，支援 Configuration Request，但它位於 Root Complex 內部，不出現在 Root Port 對外的 hierarchy domain 或 Switch 中。</p><p>【模擬資料】假設某個可讀取設定空間的 Function，Device/Port Type 識別為 RCiEP。此時應查 RCiEP 適用的欄位；規格要求它不實作 Link Capabilities、Link Control、Link Status 及其 2 版 Register。不能只因讀不到這些 Register，就判斷有一條 Link 斷線。若 Function 是另一種 Device/Port Type，仍須依該類型查它的適用規則。</p><p>RCiEP 也可能與可選的 Root Complex Event Collector（RCEC，Root Complex 事件收集器）關聯。RCEC 處理相關 RCiEP 的錯誤與 PME（Power Management Event，電源管理事件）訊息；要確認關聯，查 RCEC 的 Endpoint Association Extended Capability。RCEC 是可選的，不能假設每個 RCiEP 都有一個。若某個 RCiEP 已關聯 RCEC，規格要求其 PME 和錯誤經由該 RCEC，且它最多只關聯一個 RCEC。</p><p>三種 Endpoint 都使用 Type 0 Configuration Header，但限制並不相同。讀 §1.3.2.1–§1.3.2.3 時，可先比對下表，再按實際欄位回到對應規則。</p><div class="table-wrap"><table><thead><tr><th scope="col">Function 類型</th><th scope="col">與 I/O Request 有關的規則</th><th scope="col">Memory Requester 位址能力</th></tr></thead><tbody><tr><td>Legacy Endpoint</td><td>可選擇產生 I/O Request，也可選擇作為 I/O Request 的 Completer</td><td>不要求能產生 4 GB 以上的位址</td></tr><tr><td>PCI Express Endpoint</td><td>不得產生 I/O Request，也不得依賴作業系統配置 BAR 所宣告的 I/O 資源</td><td>須能產生大於 4 GB 的位址</td></tr><tr><td>RCiEP</td><td>不得產生 I/O Request，也不得要求 BAR 所宣告的 I/O 資源</td><td>須能產生 Host 作為 Completer 可處理的位址範圍</td></tr></tbody></table><dl class="st-terms" aria-label="本段名詞"><div><dt>BAR</dt><dd>Base Address Register，基底位址暫存器</dd></div></dl></div><p>這些條件各自針對 Function 的角色與能力；不能把「某次 Request 使用的位址」當成該 Function 的完整位址能力，也不能把三種 Endpoint 的限制混成同一條。</p><p class="source-note">Base 6.0 §1.3、Figure 1-2，pp.102–103；§§1.3.2.1–1.3.2.3、1.3.4，pp.104–106、108；Device/Port Type 的欄位見 §7.5.3.2。</p></section>
<section id="types">
<h2>想知道某個 Function 扮演什麼角色，應先讀哪兩種欄位？</h2>
<p>選定 Function 後，先讀設定空間 <code>0x0E</code> 的 8-bit Header Type。低 7 bits 選出標頭布局，bit 7 指示可能有多個功能。再沿清單找到 PCI Express Capability（描述或控制能力的結構），讀起點加 <code>0x02</code> 的 16-bit Register，以 bits 7:4 的 Device/Port Type 確認角色。先選布局，再判斷角色。</p>
<aside class="example"><strong>教學假設</strong><p>以下位址與讀值由作者設計，不是實機量測。枚舉已完成，拓樸在讀取期間維持穩定，設定讀取均成功。各 Function 的 PCI Express Capability 都已沿清單找到，起點恰好是 <code>0x70</code>；因此本例的角色欄位位於 <code>0x72</code>。表中 Device/Port Type 是擷取後的欄位值，並非完整 Register 讀值。如何尋找 Capability，請回看 <a href="/DOCS/pcie-course/chapter-0.html#case">Chapter 0 的查詢案例</a>。</p></aside>
<div class="table-wrap"><table><caption>Header 格式與 PCIe 角色要分開判讀</caption><thead><tr><th scope="col">查詢對象</th><th scope="col">Header Type 讀值</th><th scope="col">Device/Port Type 欄位值</th><th scope="col">結論</th></tr></thead><tbody>
<tr><td>Endpoint A 的 Function 0</td><td><code>0x80</code></td><td><code>0x0</code></td><td>Type 0 標頭；可能有多個 Function；PCI Express Endpoint。</td></tr>
<tr><td>Root Port</td><td><code>0x01</code></td><td><code>0x4</code></td><td>Type 1 標頭；Root Port。</td></tr>
<tr><td>Switch Upstream Port</td><td><code>0x01</code></td><td><code>0x5</code></td><td>Type 1 標頭；Switch Upstream Port。</td></tr>
<tr><td>Switch Downstream Port</td><td><code>0x01</code></td><td><code>0x6</code></td><td>Type 1 標頭；Switch Downstream Port。</td></tr>
</tbody></table></div>
<pre><code>Header 格式：0x80 &amp; 0x7F = 0
Multi-Function Device：(0x80 &amp; 0x80) &gt;&gt; 7 = 1
Device/Port Type：(PCIe_Capabilities &amp; 0x00F0) &gt;&gt; 4</code></pre>
<p><code>0x80</code> 不能解成「Type 128」，也不能解成「已有 8 個 Function」。Multi-Function Device bit 為 1 表示裝置可能有多個 Function；實際有哪些 Function，仍須以發現結果為準。本例的 Endpoint A 指提供端點功能的元件；另假設其 Function 0 與 Function 1 都已被找到。</p>
<details class="source-note"><summary>這一步應如何翻閱規格？</summary><p>先看 Base 6.0 §7.5.1.1.9 的 Figure 7-8／Table 7-7（pp.924–925），分清 Header 格式與 bit 7。接著用 Figure 7-21（p.952）定位 Capability（描述或控制能力的結構） 內的 Register，再以 Figure 7-23／Table 7-19（pp.953–954）查 Device/Port Type。Type 1 標頭只能先告訴我們要用橋接格式，不能單獨區分 Root Port 與 Switch Port。</p></details>
<p>Device/Port Type 描述 Function 類型：RCiEP 使用 Type 0 Header，卻不得實作列出的 Link Capabilities／Control／Status 及其 2 Registers。讀 Data Link Layer Link Active 時也要先確認 Reporting Capable；固定讀零可能是未提供回報，不能直接當成連線失效。（Base 6.0 §1.3.2.3，pp.105–106；Table 7-19，pp.953–954；Tables 7-23、7-26，pp.969、979。）</p>
</section>

<section id="path">
<h2>目標是 0000:03:00.1，怎麼確認它位於哪條下游路徑？</h2>
<p>本例在 Segment（匯流排的邏輯分組） <code>0000</code> 中放置一個 Root Port 和一個有兩個 Downstream Port 的 Switch。Endpoint A 的兩個 Function 位於 Bus <code>03</code>，Endpoint B 位於 Bus <code>04</code>。下表是已完成配置的快照；本章先讀懂結果，Bus Number 的配置程序留到枚舉章節。</p>
<div class="table-wrap"><table><caption>教學快照：Bridge 的 BDF 與下游 Bus 範圍（數字皆為十六進位）</caption><thead><tr><th scope="col">Bridge 角色</th><th scope="col">BDF（Segment 0000）</th><th scope="col">Secondary</th><th scope="col">Subordinate</th><th scope="col">本例下游</th></tr></thead><tbody>
<tr><td>Root Port</td><td><code>00:01.0</code></td><td><code>01</code></td><td><code>04</code></td><td>Switch 及其兩條分支。</td></tr>
<tr><td>Switch Upstream Port</td><td><code>01:00.0</code></td><td><code>02</code></td><td><code>04</code></td><td>內部 Bus 02 上的兩個 Downstream Port。</td></tr>
<tr><td>Switch Downstream Port A</td><td><code>02:01.0</code></td><td><code>03</code></td><td><code>03</code></td><td>Endpoint A：<code>03:00.0</code>、<code>03:00.1</code>。</td></tr>
<tr><td>Switch Downstream Port B</td><td><code>02:02.0</code></td><td><code>04</code></td><td><code>04</code></td><td>Endpoint B：<code>04:00.0</code>。</td></tr>
</tbody></table><dl class="st-terms" aria-label="本段名詞"><div><dt>BDF</dt><dd>Bus／Device／Function，匯流排、裝置與功能識別</dd></div></dl></div>
<p>Secondary Bus Number 表示緊接在 Bridge 下游的 Bus，Subordinate Bus Number 則界定其下游 Bus Number 範圍的上限。目標 Bus <code>03</code> 落在 Root Port 的 <code>01–04</code>、Upstream Port 的 <code>02–04</code> 及 Downstream Port A 的 <code>03–03</code> 範圍內；Downstream Port B 的範圍只有 <code>04–04</code>，因此不在本例通往目標的路徑上。</p>
<p>這裡用範圍核對已知拓樸，不代表範圍內每個號碼都必須有裝置。Bridge 自己的 BDF（Bus、Device、Function 識別號） 與它通往哪個 Bus 也要分開：<code>02:01.0</code> 本身位於 Bus <code>02</code>，其 Secondary 為 <code>03</code>。本章不以 Primary Bus Number 推導 Bridge 自己的 BDF；Base 6.0 將該欄位保留作舊式相容用途，PCIe 通常不使用它。</p>
<details class="source-note"><summary>下游 Bus Number 應讀哪裡？</summary><p>Base 6.0 §7.5.1.3 的 Figure 7-14（p.936）列出 Type 1 Header。Secondary 與 Subordinate 分別在 byte offset <code>0x19</code>、<code>0x1A</code>，各讀 8 bits；含義見 §7.5.1.3.3–§7.5.1.3.4（p.937）。相鄰的 Primary 位於 <code>0x18</code>，其 PCIe 相容性說明見 §7.5.1.3.2（同頁）。</p></details>
</section>

<section id="identity">
<h2>BDF、Segment 與 Requester ID，各自保留了哪些資訊？</h2>
<p>在本章的傳統編址下，BDF 包含 8-bit Bus Number、5-bit Device Number 與 3-bit Function Number。<code>0000:03:00.1</code> 的前四位是 Segment；同一個 Segment 內，後面的 <code>03:00.1</code> 才是 BDF。這些數字表示邏輯識別位置，不是實體插槽的編號。</p>
<div class="table-wrap"><table><caption>相同或相近的數字，可能指向不同 Function</caption><thead><tr><th scope="col">識別號</th><th scope="col">本例代表的對象</th><th scope="col">需要保留的差異</th></tr></thead><tbody>
<tr><td><code>0000:03:00.0</code></td><td>Endpoint A 的 Function 0。</td><td>與下一列共用 Bus、Device，Function 不同。</td></tr>
<tr><td><code>0000:03:00.1</code></td><td>Endpoint A 的 Function 1。</td><td>必須使用自己的設定空間讀值。</td></tr>
<tr><td><code>0001:03:00.0</code></td><td>另一個 Segment 中的 Endpoint。</td><td>BDF 與第一列相同，但 Segment 不同。</td></tr>
</tbody></table></div>
<p>另假設 Segment <code>0001</code> 中也已發現 <code>03:00.0</code>。這是作者加入的第二個邏輯範圍，並非前一張表的下游分支；不能省略 Segment 後把兩筆紀錄合併。</p>
<p>當 <code>0000:03:00.1</code> 是要求的來源時，本例的 16-bit Requester ID（封包要求來源的識別號） 按以下方式組成：</p>
<pre><code>Requester ID = (Bus &lt;&lt; 8) | (Device &lt;&lt; 3) | Function
             = (0x03 &lt;&lt; 8) | (0x00 &lt;&lt; 3) | 0x1
             = 0x0301</code></pre>
<p><strong>案例推演：</strong><code>0x0301</code> 保留 BDF，沒有把 Segment <code>0000</code> 編進這 16 bits。這項結論僅限 Requester ID（封包要求來源的識別號） 欄位，不能擴大成「所有 PCIe 封包都沒有 Segment 資訊」；Base 6.0 的部分 Flit Mode 封包另有相關欄位。本章也不把 BDF 當作永久硬體身分：若不同時間的紀錄使用了不同配置，僅憑 BDF 相同或不同，仍不足以判斷是不是同一個實體裝置。</p>
<details class="source-note"><summary>識別範圍與位元配置的規格位置</summary><p>傳統 BDF：Base 6.0 §7.3.1（p.911），§2.2.4.2／Table 2-8（p.147），Figures 2-20、2-22（p.148）。Requester ID：§2.2.6.2（pp.156–157），其中 p.156 說明 16-bit 識別號及執行期間可能改變的 Bus／Device Number，p.157 另說明 Segment 欄位。Segment Group 的邏輯範圍：Firmware 3.3 §1.3（pp.8–9），§4.3.2.3（p.47）。</p></details>
</section>

<section id="self-check"><h2>下一步需要的觀察資料</h2><p>只收到速率與寬度時，先補上 Port、直接對端、時間與欄位名稱；只收到工具的「Endpoint」標籤時，回到 Header Type 與 Device/Port Type 的讀值；只看到一段 Request 時，先標出 Link 與方向。這樣才能把後續訓練、錯誤與 Completion 資料接到同一個對象。</p><p>本章的模擬快照不提供完整訓練歷史與故障證據，也沒有用 BDF 保證永久硬體身分。</p></section>
<p>讀懂這些識別資訊後，下一步才是系統性地查詢某個 Function 的設定空間與 Capability。完整拓樸圖、逐步判讀與來源整理，見 <a href="/DOCS/pcie-course/chapter-1.html">Chapter 1 中文教學</a>；接著可讀 <a href="/DOCS/pcie-course/chapter-2.html">Chapter 2：設定空間與 Capability</a>。</p>
</article>
<nav class="bottom-nav" aria-label="課程與語言版本"><a href="/DOCS/pcie-course/index.html">課程總覽</a><a href="/DOCS/pcie-course/chapter-1.html">繁中完整教學</a><a href="/pcie/chapter-1-en/">English</a></nav>
</div>
