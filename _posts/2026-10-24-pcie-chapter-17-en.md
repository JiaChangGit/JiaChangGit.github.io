---
layout: post
title: "PCIe Chapter 17: Data Link Initialization, Flow Control, and Replay"
date: 2026-10-24 00:00:00 +0800
last_modified_at: 2026-10-28 00:00:00 +0800
permalink: /pcie/chapter-17-en/
categories: [PCIe]
tags: [PCIe, Specification]
lang: en
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
<div class="pcie-article spec-teaching" data-spec-series="pcie" lang="en">
<nav class="bottom-nav" aria-label="Course and editions"><a href="/DOCS/pcie-course/index.html">Course overview</a><a href="/DOCS/pcie-course/chapter-17.html">Full Chinese tutorial</a><a href="/pcie/chapter-17-zh-tw/">繁體中文</a></nav>
<article class="lesson">
<p>FC (Flow Control) tracks buffer space at the adjacent receiver. Link replay handles transmission integrity, while a Completion (transaction response) belongs to the request itself. We place all three along one path so their participants and guarantees stay clear.</p><figure class="diagram"><svg viewBox="0 0 900 420" role="img" aria-labelledby="ch17-en-t ch17-en-d"><title id="ch17-en-t">Link acknowledgment and receive-credit return</title><desc id="ch17-en-d">Flow-control credits and link replay track different resources and events.</desc><g data-walk-target="tx"><rect x="20" y="30" width="300" height="44" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="170.0" y="59" text-anchor="middle" font-size="16">Transmitter: pass credit gate</text></g><g data-walk-target="rx"><rect x="550" y="30" width="320" height="44" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="710.0" y="59" text-anchor="middle" font-size="16">Neighbor receiver: check and accept</text></g><g data-walk-target="buf"><rect x="550" y="335" width="320" height="44" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="710.0" y="364" text-anchor="middle" font-size="16">Receive buffers become available</text></g><g data-walk-target="retry"><rect x="20" y="335" width="300" height="44" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="170.0" y="364" text-anchor="middle" font-size="16">Transmitter: retain replay copy</text></g><g data-walk-target="data"><path d="M320 65 L550 65" stroke="var(--accent)" stroke-width="2" fill="none"/><polygon points="550,65 540.0,70.0 540.0,60.0" fill="var(--accent)"/><text x="435.0" y="55.0" text-anchor="middle" font-size="16">Send TLP</text></g><g data-walk-target="ack"><path d="M550 145 L320 145" stroke="var(--accent)" stroke-width="2" fill="none"/><polygon points="320,145 330.0,140.0 330.0,150.0" fill="var(--accent)"/><text x="435.0" y="135.0" text-anchor="middle" font-size="16">Ack/Nak: Non-Flit</text></g><g data-walk-target="keep"><path d="M170 110 L170 335" stroke="var(--accent)" stroke-width="2" fill="none"/><polygon points="170,335 165.0,325.0 175.0,325.0" fill="var(--accent)"/><text x="90" y="212.5" text-anchor="middle" font-size="16">Retain copy</text></g><g data-walk-target="free"><path d="M710 110 L710 335" stroke="var(--accent)" stroke-width="2" fill="none"/><polygon points="710,335 705.0,325.0 715.0,325.0" fill="var(--accent)"/><text x="800" y="212.5" text-anchor="middle" font-size="16">Forward progress</text></g><g data-walk-target="credit"><path d="M550 365 L320 365" stroke="var(--accent)" stroke-width="2" fill="none"/><polygon points="320,365 330.0,360.0 330.0,370.0" fill="var(--accent)"/><text x="435.0" y="355.0" text-anchor="middle" font-size="16">UpdateFC: buffer space</text></g></svg><figcaption>Author-drawn teaching diagram based on PCI Express Base 6.0. Exchanges unrelated to this lesson are omitted.</figcaption></figure><dl class="st-terms" aria-label="Terms in this passage"><div><dt>TLP</dt><dd>Transaction Layer Packet</dd></div></dl><section id="initialization"><h2>Does link-level communication mean TLP transmission can start?</h2><dl class="st-terms" aria-label="Terms in this passage"><div><dt>TLP</dt><dd>Transaction Layer Packet</dd></div></dl>
<p>The selected VC must finish Flow Control initialization. Start with Figure 3-2 (p.265): after the Physical Link becomes operational, DL_Feature exchanges features when applicable, then DL_Init initializes default VC0. <a href="/DOCS/pcie-course/chapter-16.html#vc-enable">Chapter 16</a> covers software enablement of additional VCs.</p><dl class="st-terms" aria-label="Terms in this passage"><div><dt>VC</dt><dd>Virtual Channel</dd></div></dl>
<p>Read the DL_Init rules in section 3.2.1 (p.267): FC_INIT1 reports DL_Down, while FC_INIT2 already reports DL_Up. Nevertheless, section 3.4.1 (p.273) still blocks TLP transmission on that VC throughout FC_INIT2 until initialization exits. Follow the FC state; the DL_Up output alone does not establish permission to transmit.</p><dl class="st-terms" aria-label="Terms in this passage"><div><dt>VC</dt><dd>Virtual Channel</dd></div><div><dt>FC</dt><dd>Flow Control</dd></div></dl>
<p>In Non-Flit Mode, InitFC1 and InitFC2 each exchange Posted, Non-Posted, and Completion resource information. The first phase records advertised credits; the second completes confirmation. Other VCs that have already initialized may keep operating under their own conditions. The following example starts with VC0 initialized and both sides DL_Active.</p>
<p class="source">Reading route: §3.2 Data Link Control and Management State Machine, Figure 3-2 Data Link Control and Management State Machine, pp.264–265; §3.2.1, pp.266–267; §3.4 Flow Control Initialization Protocol and §3.4.1 Flow Control Initialization State Machine Rules, pp.270–273; §2.6.1, p.241. Document and PDF pages match.</p></section>
<section id="credits"><h2>Which credit class does this packet need?</h2>
<p>Table 2-44 (p.237) separates Posted, Non-Posted, and Completion resources into Header and Data, producing six classes. PH means Posted Header Credit and PD means Posted Data Credit; Non-Posted and Completion use NPH/NPD and CplH/CplD.</p>
<p>Then use Table 2-45 on the same page to identify the packet type. Data presence alone is insufficient: I/O Write and ordinary Memory Write both carry data, but the former is Non-Posted and the latter is Posted.</p>
<div class="table-wrap"><table><thead><tr><th scope="col">Packet</th><th scope="col">Resources</th><th scope="col">Response relationship</th></tr></thead><tbody><tr><td>Memory Write Request</td><td>1 PH + n PD</td><td>No ordinary Completion</td></tr><tr><td>Memory Read Request</td><td>1 NPH</td><td>Returned data uses a separate Completion</td></tr><tr><td>Completion with Data</td><td>1 CplH + n CplD</td><td>Check these resources in the return direction</td></tr></tbody></table></div>
<p>A basic Data credit is 4 DW, or 16 bytes. Round the individual TLP's data length upward to obtain n. The following 20-byte write therefore needs 1 PH and 2 PD. These are protocol accounting units, not a required physical buffer layout.</p><dl class="st-terms" aria-label="Terms in this passage"><div><dt>DW</dt><dd>Double Word, a four-byte unit</dd></div></dl>
<p class="source">Reading route: §2.6 Ordering and Receive Buffer Flow Control, pp.235–236; §2.6.1 Flow Control (FC) Rules, Table 2-44 Flow Control Credit Types and Table 2-45 TLP Flow Control Credit Consumption, p.237. This is ordinary Non-Flit accounting; Flit Shared FC has additional granularity rules.</p></section>
<section id="credit-cycle"><h2>Why can a smaller UpdateFC value provide more available credit?</h2>
<p><strong>CREDIT_LIMIT is the cumulative limit advertised by the receiver; CREDITS_CONSUMED is the transmitter's cumulative use. Both wrap at their field widths.</strong> The latest UpdateFC value alone is not the available balance.</p>
<div class="example"><p><strong>【模擬資料】Teaching assumptions, not measurements of a particular device or platform.</strong> Root Port 00:01.0 is preparing a 20-byte Memory Write to Endpoint 01:00.0 on TC0/VC0. The Link operates at 8.0 GT/s in Non-Flit Mode. Neither side supports Scaled Flow Control. Address, BAR, Memory Space Enable, and other transmission conditions are established; the receiver's Rx_MPS_Limit is 128 bytes.</p><dl class="st-terms" aria-label="Terms in this passage"><div><dt>BAR</dt><dd>Base Address Register</dd></div></dl>
<p>During initialization, the Endpoint advertised HdrFC=08h and DataFC=008h for Posted traffic in this direction: both finite. All other required classes also initialized. Start after substantial prior traffic, with no other Posted traffic changing the following counters during this interval. These are specification conceptual counters that a complete trace can reconstruct, not mandated readable Configuration Space registers.</p>
<h3>Select the field width before decoding the update</h3>
<p>The no-Scaled-Flow-Control row of Table 2-47 (p.241) uses 8-bit Header and 12-bit Data counters, with moduli 100h and 1000h. Locate VC, HdrFC, and DataFC in Figure 3-11 (p.284). Establish that this is UpdateFC-P for this direction's VC0, not another VC or the reverse-direction account.</p>
<p>Then track section 2.6.1.1's two quantities. The consumed column is CREDITS_CONSUMED; the limit column is CREDIT_LIMIT. Their modular difference gives available credit within the specification's outstanding-unused-credit bounds.</p>
<div class="table-wrap"><table style="min-width:640px"><thead><tr><th scope="col">Observation</th><th scope="col">Consumed counter</th><th scope="col">Latest limit</th><th scope="col">Available credit</th></tr></thead><tbody><tr data-fc-stage="wait"><td>Waiting to send</td><td><code>PH=FEh; PD=FFEh</code></td><td><code>PH=FFh; PD=FFEh</code></td><td>1 PH / 0 PD</td></tr><tr data-fc-stage="ready"><td>Update A received</td><td><code>PH=FEh; PD=FFEh</code></td><td><code>PH=00h; PD=000h</code></td><td>2 PH / 2 PD</td></tr><tr data-fc-stage="sent"><td>New TLP passes the FC gate</td><td><code>PH=FFh; PD=000h</code></td><td><code>PH=00h; PD=000h</code></td><td>1 PH / 0 PD</td></tr><tr data-fc-stage="acked"><td>Valid Ack covers this TLP</td><td><code>PH=FFh; PD=000h</code></td><td><code>PH=00h; PD=000h</code></td><td>1 PH / 0 PD</td></tr><tr data-fc-stage="updated"><td>Update B received</td><td><code>PH=FFh; PD=000h</code></td><td><code>PH=01h; PD=002h</code></td><td>2 PH / 2 PD</td></tr></tbody></table></div>
<p>The first row has 1 PH and 0 PD, so the write waits. Update A gives <code>(000h − FFEh) mod 1000h = 002h</code>, or 2 PD, and <code>(00h − FEh) mod 100h = 02h</code>, or 2 PH. The smaller zero-valued fields reflect cumulative-counter wrap, not withdrawal of previously advertised space.</p>
<h3>What do Ack and UpdateFC change after normal transmission?</h3>
<p>The new TLP consumes 1 PH and 2 PD once when it passes the FC gate. Consumed PH becomes FFh; consumed PD wraps from FFEh plus 2 to 000h. The available balance becomes 1 PH / 0 PD. A later valid Ack permits release of acknowledged replay copies but does not change the FC counters.</p>
<figure class="diagram"><svg style="min-width:640px" viewBox="0 0 820 560" role="img" aria-labelledby="credit-cycle-title credit-cycle-desc"><title id="credit-cycle-title">Ack and UpdateFC update different transmitter state</title><desc id="credit-cycle-desc">Update A provides credit, one Memory Write crosses the Link, Ack acknowledges it, then Update B advertises newly available receive space. This is one illustrative ordering, not a required Ack-versus-UpdateFC sequence.</desc><rect x="55" y="15" width="280" height="65" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="195" y="42" text-anchor="middle" font-size="20">Root Port</text><text x="195" y="66" text-anchor="middle" font-size="18">00:01.0</text><path d="M195 80 V535" stroke="var(--line)" stroke-dasharray="5 5" fill="none"/><rect x="485" y="15" width="280" height="65" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="625" y="42" text-anchor="middle" font-size="20">Endpoint</text><text x="625" y="66" text-anchor="middle" font-size="18">01:00.0</text><path d="M625 80 V535" stroke="var(--line)" stroke-dasharray="5 5" fill="none"/><path d="M625 130 H195" stroke="var(--accent)" stroke-width="2.5" fill="none"/><polygon points="195,130 205,125 205,135" fill="var(--accent)"/><text x="410" y="116" text-anchor="middle" font-size="18">Update A: HdrFC=00h / DataFC=000h</text><path d="M195 220 H625" stroke="var(--accent)" stroke-width="2.5" fill="none"/><polygon points="625,220 615,215 615,225" fill="var(--accent)"/><text x="410" y="206" text-anchor="middle" font-size="18">20-byte Memory Write: 1 PH + 2 PD</text><path d="M625 305 H195" stroke="var(--accent)" stroke-width="2.5" fill="none"/><polygon points="195,305 205,300 205,310" fill="var(--accent)"/><text x="410" y="291" text-anchor="middle" font-size="18">Ack covers this TLP</text><rect x="40" y="340" width="310" height="60" rx="8" fill="var(--surface-alt)" stroke="var(--line)"/><text x="195" y="364" text-anchor="middle" font-size="17">Replay copy can be released</text><text x="195" y="387" text-anchor="middle" font-size="17">FC counters stay unchanged</text><rect x="470" y="390" width="310" height="60" rx="8" fill="var(--surface-alt)" stroke="var(--line)"/><text x="625" y="414" text-anchor="middle" font-size="17">Receive space made available</text><text x="625" y="437" text-anchor="middle" font-size="17">Advertise 1 PH + 2 PD</text><path d="M625 495 H195" stroke="var(--accent)" stroke-width="2.5" fill="none"/><polygon points="195,495 205,490 205,500" fill="var(--accent)"/><text x="410" y="481" text-anchor="middle" font-size="18">Update B: HdrFC=01h / DataFC=002h</text><text x="410" y="549" text-anchor="middle" font-size="18">Available credit: 2 PH / 2 PD</text></svg><figcaption>Author-created normal timeline. Vertical spacing has no time scale. This example places Ack before Update B; the mechanisms do not require that order. Posted Memory Write has no ordinary Completion.</figcaption></figure>
<p>When the receiver processes the data and makes the corresponding space available, it advances CREDITS_ALLOCATED and advertises Update B. Only after the transmitter receives that valid update does its limit become PH=01h, PD=002h, restoring 2 PH / 2 PD. Section 2.6.1.1 expressly forbids interpreting credit return as transaction completion or system visibility.</p>
<h3>How does a zero UpdateFC differ from Infinite Credit?</h3>
<p>The initialization advertisement 08h/008h established finite accounting here; subsequent zeros remain cumulative-counter values. Infinite Credit is a different state established by its initialization encoding. It prevents throttling for that credit type, while other transmission conditions remain. It does not imply an infinite physical receive buffer.</p>
<p class="source">Connected sources: Table 2-46 Minimum Initial Flow Control Advertisements, pp.238–239; §2.6.1, pp.240–241; §2.6.1.1 FC Information Tracked by Transmitter, pp.242–246, Equation 2-1 CREDITS_CONSUMED and Equations 2-10/2-11 for transmission gating; §2.6.1.2 FC Information Tracked by Receiver, pp.246–247; §3.5, pp.280–281, Figure 3-11 Data Link Layer Packet Format for UpdateFC, p.284. Document and PDF pages match.</p></div></section>
<section id="integrity"><h2>Does Replay consume a second set of credits?</h2>
<p>No. In an alternative to the normal example, suppose the first transmission fails LCRC and a Nak causes replay. The Retry Buffer resends the same TLP, which already passed the FC gate. Section 2.6 states that FC accounting is unaware of repeated Data Link transmissions.</p><dl class="st-terms" aria-label="Terms in this passage"><div><dt>LCRC</dt><dd>Link Cyclic Redundancy Check</dd></div></dl>
<p>Replay itself leaves CREDITS_CONSUMED at PH=FFh, PD=000h, without consuming another 1 PH and 2 PD. A valid concurrent UpdateFC can still change CREDIT_LIMIT. Section 3.6.2.1 also explains that Retry Buffer entries have already been allocated receive space by the transmitter's FC logic. A new write generated by the upper layer is a different TLP and needs a new credit check and consumption.</p>
<p>Neither Ack nor UpdateFC substitutes for Completion. The example's Posted Memory Write has no ordinary Completion. For a Memory Read, NPH covers the Request, while CplH/CplD are checked in the return direction. The requester verifies Requester ID, Tag, Status, and returned data coverage. See <a href="/DOCS/pcie-course/chapter-5.html">Chapter 5</a> for matching and completeness, and <a href="/DOCS/pcie-course/chapter-8.html">Chapter 8</a> for detailed Replay rules.</p>
<p>LCRC (Link Cyclic Redundancy Check) and sequence numbers protect an adjacent Link. ECRC (End-to-End CRC) adds integrity checking across intermediate components under its support/enable conditions. Data Poisoning marks known-unreliable data without repairing it. These mechanisms address different responsibilities from receive-buffer accounting.</p><dl class="st-terms" aria-label="Terms in this passage"><div><dt>ECRC</dt><dd>End-to-End Cyclic Redundancy Check</dd></div></dl>
<p class="source">Reading route: §2.6, p.236; §3.6.2 LCRC, Sequence Number, and Retry Management (TLP Transmitter), p.288; §3.6.2.1, pp.293–294; §3.6.2.2 Handling of Received DLLPs (Non-Flit Mode), pp.297–298; §3.6.3 LCRC and Sequence Number (TLP Receiver) (Non-Flit Mode), pp.300–301; §2.7 End-to-End Data Integrity, p.252.</p></section>
<section id="modes"><h2>What changes with Scaled FC or Flit Mode?</h2>
<p>Scaled FC (Scaled Flow Control) activation is established through Data Link Feature Exchange; initialization supplies HdrScale/DataScale. Table 2-47 changes effective counter widths with scaling. The example's fixed 8-bit/12-bit modular arithmetic cannot simply be retained.</p>
<p>Flit Mode adds Shared FC and dedicated credits, with additional rules for Completion merging, accounting granularity across contiguous TLPs, and the applicable gate. One transmitted Flit does not mean one credit.</p>
<p>Protection also moves to Flit-level CRC, FEC (Forward Error Correction), and Replay. Section 3.1 calls the Flit link CRC LCRC; section 3.6.2.3 (p.300) explicitly excludes Ack/Nak DLLPs in Flit Mode. Do not copy the example's return-packet formats into a Flit trace. Continue to <a href="/DOCS/pcie-course/chapter-18.html">Chapter 18</a> for full Flit carriage and protection.</p>
<p class="source">Reading route: §3.3 Data Link Feature Exchange, pp.268–269; Table 2-47, p.241; §2.6, pp.235–236; §2.6.1, pp.241–242; §3.1 Data Link Layer Overview, pp.263–264; §3.6.2.3, p.300.</p></section>
<section id="latency"><h2>Why can the transmitter wait after receive space is freed?</h2>
<p>Separate three events: the receiver processes TLPs and advances CREDITS_ALLOCATED; it schedules and sends UpdateFC; the transmitter receives a valid update and changes CREDIT_LIMIT. The first can finish while later events remain pending. An update whose DLLP integrity check fails does not take effect.</p><dl class="st-terms" aria-label="Terms in this passage"><div><dt>DLLP</dt><dd>Data Link Layer Packet</dd></div></dl>
<p>The section 2.6.1.2 Non-Flit Mode Flow Control Update Latency note measures from freed receive space to the first Symbol transmitted for the corresponding UpdateFC. Tables 2-48–2-50 are recommended latency guidelines, not the entire transmission-plus-processing delay. Required update-scheduling triggers and periodic-update rules must be read separately.</p>
<p>Appendix H explains the derivation and is explicitly informational. For persistently zero PD, locate the missing event along that chain. A wait caused by Replay, ordering, or arbitration belongs to its own mechanism.</p>
<p class="source">Reading route: §2.6.1.2 FC Information Tracked by Receiver, pp.246–249; Implementation Note: Non-Flit Mode Flow Control Update Latency, pp.251–252; §3.5, p.281; Appendix H Flow Control Update Latency and ACK Update Latency Calculations and §H.1 Flow Control Update Latency, pp.1581–1582.</p></section>
<section id="sources"><h2>Edition and sources</h2><p>Authority: PCI Express Base Specification Revision 6.0 (6.0-1.0-PUB). Printed document and PDF viewer pages match. Counters, configurations, and the timeline are author-created, not hardware measurements. This revision teaches finite, unscaled Non-Flit Posted credit; full Scaled/Shared FC, all Replay rules, and Appendix H formulas remain for deeper coverage.</p><details class="source-note"><summary>Complete source locations and purpose</summary><ul>
<li>§3.2 Data Link Control and Management State Machine and §3.2.1 Data Link Control and Management State Machine Rules, pp.264–267; Figure 3-2, p.265; §3.4 Flow Control Initialization Protocol and §3.4.1 Flow Control Initialization State Machine Rules, pp.270–273: DL_Up versus completed FC initialization.</li>
<li>§2.6 Ordering and Receive Buffer Flow Control, pp.235–236; Figure 2-89 Relationship Between Requester and Ultimate Completer, p.235; §2.6.1 Flow Control (FC) Rules, Tables 2-44 Flow Control Credit Types and 2-45 TLP Flow Control Credit Consumption, p.237; Table 2-46 Minimum Initial Flow Control Advertisements, pp.238–240: classes, units, initial advertisements, and Link scope.</li>
<li>§2.6.1, pp.240–241; Table 2-47 [Field Size] Values, p.241; §2.6.1.1 FC Information Tracked by Transmitter, pp.242–246; Equation 2-1 CREDITS_CONSUMED, p.242; Equation 2-10 CUMULATIVE_CREDITS_REQUIRED, p.245; Equation 2-11 Transmitter Gate, p.246: widths, wrap, finite/infinite accounting, and transmission conditions.</li>
<li>§2.6.1.2 FC Information Tracked by Receiver, pp.246–249; Equation 2-12 CREDITS_ALLOCATED, p.247: release and return; Non-Flit Mode Flow Control Update Latency note and Tables 2-48–2-50, pp.251–252: measurement endpoints and recommendations.</li>
<li>§3.5 Data Link Layer Packets (DLLPs), pp.280–281; Figure 3-11 Data Link Layer Packet Format for UpdateFC, p.284: VC, HdrFC, DataFC, and update validity.</li>
<li>§3.6.2 LCRC, Sequence Number, and Retry Management (TLP Transmitter), p.288; §3.6.2.1, pp.293–294; §3.6.2.2 Handling of Received DLLPs (Non-Flit Mode), pp.297–298; §3.6.3 LCRC and Sequence Number (TLP Receiver) (Non-Flit Mode), pp.300–301: retry storage, Ack, and no second credit consumption.</li>
<li>§2.7 End-to-End Data Integrity, p.252; §3.1 Data Link Layer Overview, pp.263–264; §3.3 Data Link Feature Exchange, pp.268–269; §3.6.2.3, p.300: integrity, features, and mode boundaries.</li>
<li>Appendix H Flow Control Update Latency and ACK Update Latency Calculations and §H.1 Flow Control Update Latency, pp.1581–1582: informational derivation.</li></ul></details></section>
</article>
<nav class="bottom-nav" aria-label="Course and editions"><a href="/DOCS/pcie-course/index.html">Course overview</a><a href="/DOCS/pcie-course/chapter-17.html">Full Chinese tutorial</a><a href="/pcie/chapter-17-zh-tw/">繁體中文</a></nav>
</div>
