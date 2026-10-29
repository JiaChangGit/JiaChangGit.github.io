---
layout: post
title: "PCIe Chapter 17：資料連結初始化、流量控制與重送細節"
date: 2026-10-24 00:00:00 +0800
last_modified_at: 2026-10-28 00:00:00 +0800
permalink: /pcie/chapter-17-zh-tw/
categories: [PCIe]
tags: [PCIe, Specification]
lang: zh-TW
spec_teaching: true
spec_series: pcie
description: "從VC初始化接到有限Non-Flit credit計數，以20byte寫入帶讀回繞、Ack、UpdateFC與Replay，分清接收緩衝、重送副本及交易結果。"
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
<nav class="bottom-nav" aria-label="課程與語言版本"><a href="/DOCS/pcie-course/index.html">課程總覽</a><a href="/DOCS/pcie-course/chapter-17.html">繁中完整教學</a><a href="/pcie/chapter-17-en/">English</a></nav>
<article class="lesson">
<p>FC（Flow Control，流量控制）確認相鄰接收端有空間；重送機制處理 Link 上的資料傳輸錯誤；Completion（完成回覆）則回到交易本身。這一章把三者放在同一條路徑，從發送前的空間檢查，走到接收、回報與後續處理。</p><figure class="diagram"><svg viewBox="0 0 900 420" role="img" aria-labelledby="ch17-zh-t ch17-zh-d"><title id="ch17-zh-t">傳送確認與接收額度分別回報</title><desc id="ch17-zh-d">接收空間回報與錯誤重送是兩個獨立機制；成功Ack不代表交易完成。</desc><g data-walk-target="tx"><rect x="20" y="30" width="300" height="44" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="170.0" y="59" text-anchor="middle" font-size="16">傳送端：先確認接收資源</text></g><g data-walk-target="rx"><rect x="550" y="30" width="320" height="44" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="710.0" y="59" text-anchor="middle" font-size="16">相鄰接收端：檢查與接收</text></g><g data-walk-target="buf"><rect x="550" y="335" width="320" height="44" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="710.0" y="364" text-anchor="middle" font-size="16">接收緩衝釋放空間</text></g><g data-walk-target="retry"><rect x="20" y="335" width="300" height="44" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="170.0" y="364" text-anchor="middle" font-size="16">傳送端：保留重送資料</text></g><g data-walk-target="data"><path d="M320 65 L550 65" stroke="var(--accent)" stroke-width="2" fill="none"/><polygon points="550,65 540.0,70.0 540.0,60.0" fill="var(--accent)"/><text x="435.0" y="55.0" text-anchor="middle" font-size="16">送出 TLP</text></g><g data-walk-target="ack"><path d="M550 145 L320 145" stroke="var(--accent)" stroke-width="2" fill="none"/><polygon points="320,145 330.0,140.0 330.0,150.0" fill="var(--accent)"/><text x="435.0" y="135.0" text-anchor="middle" font-size="16">Ack／Nak：非 Flit</text></g><g data-walk-target="keep"><path d="M170 110 L170 335" stroke="var(--accent)" stroke-width="2" fill="none"/><polygon points="170,335 165.0,325.0 175.0,325.0" fill="var(--accent)"/><text x="90" y="212.5" text-anchor="middle" font-size="16">留存副本</text></g><g data-walk-target="free"><path d="M710 110 L710 335" stroke="var(--accent)" stroke-width="2" fill="none"/><polygon points="710,335 705.0,325.0 715.0,325.0" fill="var(--accent)"/><text x="800" y="212.5" text-anchor="middle" font-size="16">資料往前處理</text></g><g data-walk-target="credit"><path d="M550 365 L320 365" stroke="var(--accent)" stroke-width="2" fill="none"/><polygon points="320,365 330.0,360.0 330.0,370.0" fill="var(--accent)"/><text x="435.0" y="355.0" text-anchor="middle" font-size="16">UpdateFC：空間回報</text></g></svg><figcaption>作者依 Base 6.0 繪製的教學示意；省略與本章無關的交換。</figcaption></figure><dl class="st-terms" aria-label="本段名詞"><div><dt>TLP</dt><dd>Transaction Layer Packet，交易層封包</dd></div></dl><section id="initialization"><h2>Link 已能交換資訊，就能開始送 TLP 嗎？</h2><dl class="st-terms" aria-label="本段名詞"><div><dt>TLP</dt><dd>Transaction Layer Packet，交易層封包</dd></div></dl>
<p>還要確認該 VC 的 Flow Control 初始化已完成。沿 Figure 3-2（p.265）先辨認 Data Link 狀態：實體 Link 可用後，若條件適用，先經 DL_Feature 交換功能資訊，再進入 DL_Init，初始化基本通道 VC0。額外 VC 的軟體啟用方式已在 <a href="/DOCS/pcie-course/chapter-16.html#vc-enable">Chapter 16</a> 帶讀。</p><dl class="st-terms" aria-label="本段名詞"><div><dt>VC</dt><dd>Virtual Channel，虛擬通道</dd></div></dl>
<p>接著讀 §3.2.1 的 DL_Init 規則（p.267），這裡有一個容易漏掉的差別：在 FC_INIT1 時回報 DL_Down；進入 FC_INIT2 後已回報 DL_Up，但仍未完成初始化。§3.4.1（p.273）明確要求，FC_INIT2 期間仍須阻止該 VC 的 TLP 傳送，直到離開這個狀態。因此，判斷傳送時機要接著查 FC 狀態，不能停在 DL_Up 這個輸出。</p><dl class="st-terms" aria-label="本段名詞"><div><dt>FC</dt><dd>Flow Control，流量控制</dd></div></dl>
<p>Non-Flit Mode 的 InitFC1／InitFC2 各交換 Posted、Non-Posted、Completion 三組資源資訊。先取得對方宣告的額度，再完成第二階段確認；已經初始化完成的其他 VCs，仍可依自身條件傳輸。後面的案例從 VC0 已完成初始化、雙端皆處於 DL_Active 的時點開始。</p>
<p class="source">規格閱讀：§3.2 Data Link Control and Management State Machine，Figure 3-2 Data Link Control and Management State Machine，pp.264–265；§3.2.1，pp.266–267；§3.4 Flow Control Initialization Protocol、§3.4.1 Flow Control Initialization State Machine Rules，pp.270–273；§2.6.1，p.241。文件頁與 PDF 頁相同。</p></section>
<section id="credits"><h2>先分清楚：這筆封包要用哪一類 credit？</h2>
<p>先用 Table 2-44（p.237）把資源分成 Posted、Non-Posted、Completion，每一類再分 Header 與 Data，形成六種 credit。PH 是 Posted Header Credit，PD 是 Posted Data Credit；Non-Posted 與 Completion 則分別使用 NPH／NPD、CplH／CplD。</p>
<p>再用同頁的 Table 2-45 找封包種類，不要只看它有沒有 Data。例如 I/O Write 與一般 Memory Write 都帶資料，前者是 Non-Posted，後者是 Posted，需要的 credit 類別不同。</p>
<div class="table-wrap"><table><thead><tr><th scope="col">本次要傳的封包</th><th scope="col">所需資源</th><th scope="col">與回覆的關係</th></tr></thead><tbody><tr><td>Memory Write Request</td><td>1 PH + n PD</td><td>沒有一般 Completion</td></tr><tr><td>Memory Read Request</td><td>1 NPH</td><td>返回的資料另由 Completion 承載</td></tr><tr><td>Completion with Data</td><td>1 CplH + n CplD</td><td>在反方向檢查這個封包所需的額度</td></tr></tbody></table></div>
<p>Data credit 的基本單位是 4 DW，也就是 16 bytes；n 按本筆 TLP 的資料長度向上取整。後面的 20-byte 寫入因此需要 1 PH 與 2 PD。這些單位是協定帳目，不等同於硬體內部必定以相同大小切割緩衝。</p><dl class="st-terms" aria-label="本段名詞"><div><dt>DW</dt><dd>Double Word，4 bytes的資料單位</dd></div></dl>
<p class="source">規格閱讀：§2.6 Ordering and Receive Buffer Flow Control，pp.235–236；§2.6.1 Flow Control (FC) Rules，Table 2-44 Flow Control Credit Types、Table 2-45 TLP Flow Control Credit Consumption，p.237。這裡使用一般 Non-Flit Mode 計算；Flit Shared FC 另有計帳粒度。</p></section>
<section id="credit-cycle"><h2>UpdateFC 的數字變小，為什麼可用額度反而增加？</h2>
<p><strong>CREDIT_LIMIT 是接收端累積宣告的額度上限，CREDITS_CONSUMED 是傳送端累積使用的額度；兩者都會按欄位寬度回繞。</strong>單看最新一個 UpdateFC 的數字，還不知道目前能傳多少。</p>
<div class="example"><p><strong>【模擬資料】以下資料為教學用途建立，不代表特定硬體或平台。</strong>Root Port 00:01.0 正要向 Endpoint 01:00.0 傳送一筆 20-byte Memory Write，使用 TC0／VC0。Link 為 8.0 GT/s、Non-Flit Mode；雙端不支援 Scaled Flow Control。地址、BAR、Memory Space Enable 與其他傳送條件均已確認，接收端的 Rx_MPS_Limit 為 128 bytes。</p><dl class="st-terms" aria-label="本段名詞"><div><dt>BAR</dt><dd>Base Address Register，基底位址暫存器</dd></div></dl>
<p>初始化時，Endpoint 對此方向的 Posted 類別宣告 HdrFC=08h、DataFC=008h，兩者都是有限額度。其他必要類別也已完成初始化。下面從 Link 已經傳輸許多封包後開始，假設這段期間沒有其他 Posted 封包干擾計數。這些是規格用來說明行為的概念計數，可由完整 Trace 重建；它們不是 Configuration Space 中規定可讀取的寄存器。</p>
<h3>先選欄位寬度，再讀更新值</h3>
<p>Table 2-47（p.241）在「不支援 Scaled Flow Control」這一列，指定 Header 計數為 8 bits、Data 為 12 bits，分別以 100h 與 1000h 為模數。再到 Figure 3-11（p.284）找到 UpdateFC 的 VC、HdrFC 與 DataFC，確認這是回報本次 VC0、Posted 資源的 UpdateFC-P，而非另一個 VC 或反方向的帳目。</p>
<p>接著依 §2.6.1.1 追蹤兩組數值。下表的「已消耗計數」為 CREDITS_CONSUMED；「最新宣告上限」為 CREDIT_LIMIT。可用額度是兩者之差按相同欄位寬度取模，並須遵守規格對未使用額度的範圍限制。</p>
<div class="table-wrap"><table style="min-width:640px"><thead><tr><th scope="col">觀察時點</th><th scope="col">已消耗計數</th><th scope="col">最新宣告上限</th><th scope="col">目前可用 credit</th></tr></thead><tbody><tr data-fc-stage="wait"><td>準備傳送，先等待</td><td><code>PH=FEh; PD=FFEh</code></td><td><code>PH=FFh; PD=FFEh</code></td><td>1 PH / 0 PD</td></tr><tr data-fc-stage="ready"><td>收到 Update A</td><td><code>PH=FEh; PD=FFEh</code></td><td><code>PH=00h; PD=000h</code></td><td>2 PH / 2 PD</td></tr><tr data-fc-stage="sent"><td>新 TLP 通過 FC 檢查</td><td><code>PH=FFh; PD=000h</code></td><td><code>PH=00h; PD=000h</code></td><td>1 PH / 0 PD</td></tr><tr data-fc-stage="acked"><td>收到涵蓋本 TLP 的有效 Ack</td><td><code>PH=FFh; PD=000h</code></td><td><code>PH=00h; PD=000h</code></td><td>1 PH / 0 PD</td></tr><tr data-fc-stage="updated"><td>收到 Update B</td><td><code>PH=FFh; PD=000h</code></td><td><code>PH=01h; PD=002h</code></td><td>2 PH / 2 PD</td></tr></tbody></table></div>
<p>第一列只有 1 PH、0 PD，這筆寫入還不能送。收到 Update A 後，PD 的差值變成 <code>(000h − FFEh) mod 1000h = 002h</code>，所以有 2 PD；PH 則由 <code>(00h − FEh) mod 100h = 02h</code> 得到 2 PH。更新欄位由較大的值變成零，是累積計數回繞，沒有撤回先前宣告的空間。</p>
<h3>正常傳送後，Ack 與 UpdateFC 各改變什麼？</h3>
<p>這筆新 TLP 通過 FC 檢查時，只消耗一次 1 PH、2 PD。PH 的已消耗計數成為 FFh，PD 從 FFEh 加 2 後回繞成 000h，可用額度剩 1 PH、0 PD。稍後收到有效 Ack，傳送端可釋放被確認的重送副本，但 FC 計數不會因此改變。</p>
<figure class="diagram"><svg style="min-width:640px" viewBox="0 0 820 560" role="img" aria-labelledby="credit-cycle-title credit-cycle-desc"><title id="credit-cycle-title">Ack 與 UpdateFC 各自更新不同的傳送端狀態</title><desc id="credit-cycle-desc">Update A 提供額度後送出一筆 Memory Write；Ack 確認該筆傳輸，Update B 再回報新接收空間。這是示範順序，不規定 Ack 和 UpdateFC 的普遍先後。</desc><rect x="55" y="15" width="280" height="65" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="195" y="42" text-anchor="middle" font-size="20">Root Port</text><text x="195" y="66" text-anchor="middle" font-size="18">00:01.0</text><path d="M195 80 V535" stroke="var(--line)" stroke-dasharray="5 5" fill="none"/><rect x="485" y="15" width="280" height="65" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="625" y="42" text-anchor="middle" font-size="20">Endpoint</text><text x="625" y="66" text-anchor="middle" font-size="18">01:00.0</text><path d="M625 80 V535" stroke="var(--line)" stroke-dasharray="5 5" fill="none"/><path d="M625 130 H195" stroke="var(--accent)" stroke-width="2.5" fill="none"/><polygon points="195,130 205,125 205,135" fill="var(--accent)"/><text x="410" y="116" text-anchor="middle" font-size="18">Update A: HdrFC=00h / DataFC=000h</text><path d="M195 220 H625" stroke="var(--accent)" stroke-width="2.5" fill="none"/><polygon points="625,220 615,215 615,225" fill="var(--accent)"/><text x="410" y="206" text-anchor="middle" font-size="18">20-byte Memory Write: 1 PH + 2 PD</text><path d="M625 305 H195" stroke="var(--accent)" stroke-width="2.5" fill="none"/><polygon points="195,305 205,300 205,310" fill="var(--accent)"/><text x="410" y="291" text-anchor="middle" font-size="18">涵蓋這筆 TLP 的有效 Ack</text><rect x="40" y="340" width="310" height="60" rx="8" fill="var(--surface-alt)" stroke="var(--line)"/><text x="195" y="364" text-anchor="middle" font-size="17">可釋放這筆重送副本</text><text x="195" y="387" text-anchor="middle" font-size="17">FC 計數保持不變</text><rect x="470" y="390" width="310" height="60" rx="8" fill="var(--surface-alt)" stroke="var(--line)"/><text x="625" y="414" text-anchor="middle" font-size="17">接收端釋放對應空間</text><text x="625" y="437" text-anchor="middle" font-size="17">回報新增 1 PH + 2 PD</text><path d="M625 495 H195" stroke="var(--accent)" stroke-width="2.5" fill="none"/><polygon points="195,495 205,490 205,500" fill="var(--accent)"/><text x="410" y="481" text-anchor="middle" font-size="18">Update B: HdrFC=01h / DataFC=002h</text><text x="410" y="549" text-anchor="middle" font-size="18">傳送端可用額度恢復為 2 PH / 2 PD</text></svg><figcaption>作者建立的正常傳輸時序，縱向距離不代表時間長度。本例選擇先收到 Ack、後收到 Update B；兩種回報機制沒有這項固定先後要求。Posted Memory Write 沒有一般 Completion。</figcaption></figure>
<p>接收端處理資料並釋放對應空間後，先增加自己的 CREDITS_ALLOCATED，再以 Update B 回報。傳送端收到有效更新，才把最新上限換成 PH=01h、PD=002h，重新得到 2 PH、2 PD。這仍只證明接收緩衝的額度已回報；§2.6.1.1 明確禁止把 credit 返回解讀為交易已完成或已達到系統可見。</p>
<h3>UpdateFC 為零，和 Infinite Credit 如何區分？</h3>
<p>本例的有限額度，已由初始化時的 08h／008h 確立；後來的零值按累積計數解讀。Infinite Credit 則是在初始化時用特定編碼宣告的另一種狀態。傳送端對已宣告為 Infinite 的那一類資源，不再因該類 credit 不足而阻擋；它仍須遵守其他傳送條件，也不代表接收端真的有無限實體緩衝。</p>
<p class="source">規格串接：Table 2-46 Minimum Initial Flow Control Advertisements，pp.238–239；§2.6.1，pp.240–241；§2.6.1.1 FC Information Tracked by Transmitter，pp.242–246，Equation 2-1 CREDITS_CONSUMED、Equations 2-10／2-11 的傳送檢查；§2.6.1.2 FC Information Tracked by Receiver，pp.246–247；§3.5，pp.280–281，Figure 3-11 Data Link Layer Packet Format for UpdateFC，p.284。文件頁與 PDF 頁相同。</p></div></section>
<section id="integrity"><h2>如果中間發生 Replay，要再扣一次 credit 嗎？</h2>
<p>不需要。若把前面的正常流程改成「第一次傳送未通過 LCRC 檢查，收到 Nak 後重送」，重送的是 Retry Buffer 中同一筆 TLP。它已經通過一次 FC 檢查；§2.6 說明，流量控制計帳不會因 Data Link Layer 重複傳送而再記一次。</p><dl class="st-terms" aria-label="本段名詞"><div><dt>LCRC</dt><dd>Link Cyclic Redundancy Check，鏈結循環冗餘檢查</dd></div></dl>
<p>因此，在這個額外情境中，重送本身不會改變 CREDITS_CONSUMED，仍為 PH=FFh、PD=000h；如果同時收到有效 UpdateFC，CREDIT_LIMIT 仍依回報更新。不會因為重送而多扣第二份 1 PH、2 PD。§3.6.2.1 也說明，Retry Buffer 的內容都已由傳送端的 FC 邏輯配置接收空間，不需要再次同步額度。若上層重新產生一筆新的寫入，那才是另一筆 TLP，須重新檢查並消耗額度。</p>
<p>Ack 與 UpdateFC 同樣不能代替 Completion。前例是 Posted Memory Write，原本就沒有一般 Completion；若改追蹤 Memory Read，要求使用 NPH，回程 Completion 則在反方向檢查 CplH／CplD，並由 Requester 依 Requester ID、Tag、Status 與資料範圍確認交易結果。配對與完整回覆的帶讀見 <a href="/DOCS/pcie-course/chapter-5.html">Chapter 5</a>；Replay 的詳細規則見 <a href="/DOCS/pcie-course/chapter-8.html">Chapter 8</a>。</p>
<p>LCRC（Link Cyclic Redundancy Check，鏈結循環冗餘檢查）與序號保護相鄰 Link。ECRC（End-to-End CRC，端到端循環冗餘檢查）則補上經過中間元件時的完整性檢查；其產生與檢查仍有支援、啟用條件。Data Poisoning 是標示資料已知不可靠的資訊，並不修復資料。這些機制與接收端緩衝額度各有責任，不能互相代替。</p>
<p class="source">規格閱讀：§2.6，p.236；§3.6.2 LCRC, Sequence Number, and Retry Management (TLP Transmitter)，p.288；§3.6.2.1，pp.293–294；§3.6.2.2 Handling of Received DLLPs (Non-Flit Mode)，pp.297–298；§3.6.3 LCRC and Sequence Number (TLP Receiver) (Non-Flit Mode)，pp.300–301；§2.7 End-to-End Data Integrity，p.252。</p></section>
<section id="modes"><h2>換成 Scaled FC 或 Flit Mode，要重新選哪些規則？</h2>
<p>Scaled FC（Scaled Flow Control，以比例擴充額度表示的流量控制）先經 Data Link Feature Exchange 判斷是否啟用，再用初始化取得的 HdrScale／DataScale 解讀。Table 2-47 會隨比例改變有效計數寬度，不能繼續固定使用本例的 8-bit／12-bit 取模。</p>
<p>Flit Mode 還加入 Shared FC 與專用 credit，Shared Credit 是否與 Completion 合併、連續 TLP 的計帳粒度，以及使用哪組傳送檢查，都有額外規則。傳送一個 Flit，不等同於固定消耗一個 credit。</p>
<p>傳輸保護也要換成 Flit 層的 CRC、FEC（Forward Error Correction，前向錯誤更正）與 Replay。§3.1 將 Flit 的鏈結 CRC 稱為 LCRC；§3.6.2.3（p.300）明確說明 Flit Mode 不使用 Ack／Nak DLLP。因此本例兩條回報箭頭的封包格式，不能原樣搬進 Flit Trace。完整 Flit 承載與保護方式接到 <a href="/DOCS/pcie-course/chapter-18.html">Chapter 18</a>。</p><dl class="st-terms" aria-label="本段名詞"><div><dt>DLLP</dt><dd>Data Link Layer Packet，資料鏈結層封包</dd></div></dl>
<p class="source">規格閱讀：§3.3 Data Link Feature Exchange，pp.268–269；Table 2-47，p.241；§2.6，pp.235–236；§2.6.1，pp.241–242；§3.1 Data Link Layer Overview，pp.263–264；§3.6.2.3，p.300。</p></section>
<section id="flit-prefix-credit"><h2>Flit Mode 怎麼指出這筆 TLP 使用哪一類 credit？</h2>
<p>先確認 Link 正以 Flit Mode 運作，再看 §2.2.10.3 的 Figure 2-77。Flit Mode Local TLP Prefix 是附在 TLP 前面的 4-byte 欄位；它的 byte 0 是 <code>8Dh</code>，byte 1 的 bit 7 是 TLP Uses Dedicated Credits（此 TLP 使用專用額度）。這個 Prefix 只允許用在 Flit Mode。</p>
<div class="example"><p><strong>【模擬資料】以下資料為教學用途建立，不代表特定硬體或平台。</strong>假設這條 Link 已啟用 Shared FC（共享流量控制），下列是三筆獨立 TLP 的不同狀況；每筆仍要依自身類型、長度與當時可用額度通過 Flow Control 檢查。</p>
<p>手機閱讀時，表格可以左右滑動。</p><div class="table-wrap"><table><thead><tr><th scope="col">Local Prefix</th><th scope="col">bit 7</th><th scope="col">此 TLP 使用的額度</th></tr></thead><tbody><tr><td><code>8D 80 00 00</code></td><td>1</td><td>專用 credit</td></tr><tr><td><code>8D 00 00 00</code></td><td>0</td><td>共享 credit</td></tr><tr><td>沒有這個 Prefix</td><td>無</td><td>共享 credit</td></tr></tbody></table></div>
<p>這兩個 Prefix 範例中的其他位元均為 0，並非指定所有 TLP 都要附上 Prefix。規格容許在 Flit Mode 的 TLP 使用它，但強烈建議只附在明確需要它的 TLP 上。§2.6.1 另外容許傳送端即使有足夠共享 credit，仍選擇使用專用 credit；選用時應以 Prefix 的 bit 7 表示。</p></div>
<p>若這個 Prefix 被加到 Non-Flit TLP，便是錯誤。對支援 Flit Mode 的元件，規格要求視為 Malformed TLP；對不支援 Flit Mode 的元件，這項處理是強烈建議。這裡的條件是元件<strong>是否支援</strong> Flit Mode，與觀察當下 Link 是否處於該模式是兩個不同問題。</p>
<p class="source">規格閱讀：Base 6.0 §2.2.10.3、Figure 2-77，文件頁／PDF 頁 200–201；§2.6.1，p.236；MUST@FLIT 的定義見 Terms and Acronyms，p.88。Non-Flit Prefix 的判讀另見 <a href="/DOCS/pcie-course/chapter-14.html#prefix-reading">Chapter 14</a>。</p></section>
<section id="latency"><h2>接收端空間已釋放，發送端為什麼仍在等待？</h2>
<p>先把時間線拆成三段：接收端處理 TLP 並增加 CREDITS_ALLOCATED、安排並送出 UpdateFC、傳送端收到有效更新並改變 CREDIT_LIMIT。第一段已完成時，後兩段可能還在進行；如果 DLLP 的完整性檢查失敗，這次更新也不會生效。</p><dl class="st-terms" aria-label="本段名詞"><div><dt>DLLP</dt><dd>Data Link Layer Packet，資料鏈結層封包</dd></div></dl>
<p>讀 §2.6.1.2 的 Non-Flit Mode Flow Control Update Latency 說明時，留意量測起訖：從接收端釋放緩衝，到對應 UpdateFC 的第一個 Symbol 送出。Tables 2-48–2-50 給的是建議延遲，不包含之後跨 Link 傳輸及對端處理的全部時間。另有必須安排更新的條件與週期性更新規則，要分開查閱。</p>
<p>Appendix H 解釋這些延遲值的推導，但明確標為資訊性。若本例的 PD 長時間維持零，先沿這三段確認更新停在哪裡；如果其實是 Replay、排序或仲裁在等待，就回到相應機制，不把所有停頓都歸給 credit。</p>
<p class="source">規格閱讀：§2.6.1.2 FC Information Tracked by Receiver，pp.246–249；Non-Flit Mode Flow Control Update Latency 的 Implementation Note，pp.251–252；§3.5，p.281；Appendix H Flow Control Update Latency and ACK Update Latency Calculations、§H.1 Flow Control Update Latency，pp.1581–1582。</p></section>
<section id="sources"><h2>版本與來源</h2><p>本章依 PCI Express Base Specification Revision 6.0（6.0-1.0-PUB）撰寫，文件印刷頁與 PDF 檢視器頁碼相同。計數、配置與時序圖由作者依規則建立，不是實機量測。本輪集中帶讀有限、未縮放的 Non-Flit Posted credit；完整 Scaled／Shared FC、全部 Replay 規則及 Appendix H 公式仍須深入。</p><details class="source-note"><summary>完整來源定位與用途</summary><ul>
<li>§3.2 Data Link Control and Management State Machine、§3.2.1 Data Link Control and Management State Machine Rules，pp.264–267；Figure 3-2，p.265；§3.4 Flow Control Initialization Protocol、§3.4.1 Flow Control Initialization State Machine Rules，pp.270–273：DL_Up 與 FC 初始化完成的差別。</li>
<li>§2.6 Ordering and Receive Buffer Flow Control，pp.235–236；Figure 2-89 Relationship Between Requester and Ultimate Completer，p.235；§2.6.1 Flow Control (FC) Rules，Tables 2-44 Flow Control Credit Types／2-45 TLP Flow Control Credit Consumption，p.237；Table 2-46 Minimum Initial Flow Control Advertisements，pp.238–240：分類、單位、最小初始額度與逐 Link 範圍。</li>
<li>§2.6.1，pp.240–241；Table 2-47 [Field Size] Values，p.241；§2.6.1.1 FC Information Tracked by Transmitter，pp.242–246；Equation 2-1 CREDITS_CONSUMED，p.242；Equation 2-10 CUMULATIVE_CREDITS_REQUIRED，p.245；Equation 2-11 Transmitter Gate，p.246：計數寬度、回繞、有限與 Infinite 額度、傳送條件。</li>
<li>§2.6.1.2 FC Information Tracked by Receiver，pp.246–249；Equation 2-12 CREDITS_ALLOCATED，p.247：釋放與回報；Non-Flit Mode Flow Control Update Latency 的 Implementation Note 及 Tables 2-48–2-50，pp.251–252：更新延遲的起訖與建議值。</li>
<li>§3.5 Data Link Layer Packets (DLLPs)，pp.280–281；Figure 3-11 Data Link Layer Packet Format for UpdateFC，p.284：VC、HdrFC、DataFC 與更新有效性。</li>
<li>§3.6.2 LCRC, Sequence Number, and Retry Management (TLP Transmitter)，p.288；§3.6.2.1，pp.293–294；§3.6.2.2 Handling of Received DLLPs (Non-Flit Mode)，pp.297–298；§3.6.3 LCRC and Sequence Number (TLP Receiver) (Non-Flit Mode)，pp.300–301：重送緩衝、Ack 與不重複消耗 credit。</li>
<li>§2.7 End-to-End Data Integrity，p.252；§3.1 Data Link Layer Overview，pp.263–264；§3.3 Data Link Feature Exchange，pp.268–269；§3.6.2.3，p.300：完整性、功能與模式邊界。</li>
<li>Appendix H Flow Control Update Latency and ACK Update Latency Calculations、§H.1 Flow Control Update Latency，pp.1581–1582：資訊性推導的範圍。</li></ul></details></section>
</article>
<nav class="bottom-nav" aria-label="課程與語言版本"><a href="/DOCS/pcie-course/index.html">課程總覽</a><a href="/DOCS/pcie-course/chapter-17.html">繁中完整教學</a><a href="/pcie/chapter-17-en/">English</a></nav>
</div>
