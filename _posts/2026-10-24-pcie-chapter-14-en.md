---
layout: post
title: "PCIe Chapter 14: TLP Headers and Flit Packet Layouts"
date: 2026-10-24 00:00:00 +0800
last_modified_at: 2026-10-28 00:00:00 +0800
permalink: /pcie/chapter-14-en/
categories: [PCIe]
tags: [PCIe, Specification]
lang: en
spec_teaching: true
spec_series: pcie
description: "用同一筆部分寫入需求比較 Non-Flit／Flit 完整 TLP，串連格式、OHC、資料起點與有效 bytes。"
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
<nav class="bottom-nav" aria-label="Course and editions"><a href="/DOCS/pcie-course/index.html">Course overview</a><a href="/DOCS/pcie-course/chapter-14.html">Full Chinese tutorial</a><a href="/pcie/chapter-14-zh-tw/">繁體中文</a></nav>
<article class="lesson">
<p>A TLP (Transaction Layer Packet) carries a request, completion, or message. First establish whether the link uses Non-Flit Mode or Flit Mode: their TLP (transaction packet) header layouts differ. We follow that choice into address, identity, length, and byte selection.</p><figure class="diagram"><svg viewBox="0 0 900 420" role="img" aria-labelledby="ch14-en-t ch14-en-d"><title id="ch14-en-t">Roles and events in this chapter</title><desc id="ch14-en-d">Choose the TLP format, locate its header fields, then interpret the selected bytes.</desc><g data-walk-target="mode"><rect x="30" y="30" width="250" height="44" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="155.0" y="59" text-anchor="middle" font-size="16">Identify link mode</text></g><g data-walk-target="nfm"><rect x="30" y="175" width="350" height="68" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="205.0" y="204" text-anchor="middle" font-size="16">Non-Flit: Fmt + Type</text><text x="205.0" y="228" text-anchor="middle" font-size="16">Header length and data presence</text></g><g data-walk-target="fm"><rect x="500" y="175" width="360" height="68" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="680.0" y="204" text-anchor="middle" font-size="16">Flit: Type + OHC + TS</text><text x="680.0" y="228" text-anchor="middle" font-size="16">Base, extensions, and trailer</text></g><g data-walk-target="body"><rect x="245" y="335" width="410" height="44" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="450.0" y="364" text-anchor="middle" font-size="16">Decode address, identity, and data</text></g><g data-walk-target="a"><path d="M155 74 L205 175" stroke="var(--accent)" stroke-width="2" fill="none"/><polygon points="205,175 196.08241815935642,168.25635602100587 205.0443660788092,163.81974814008865" fill="var(--accent)"/><text x="180.0" y="114.5" text-anchor="middle" font-size="16">Non-Flit</text></g><g data-walk-target="b"><path d="M280 60 L660 175" stroke="var(--accent)" stroke-width="2" fill="none"/><polygon points="660,175 648.9804081905046,176.88907288162778 651.8769866090005,167.31777028138032" fill="var(--accent)"/><text x="470.0" y="107.5" text-anchor="middle" font-size="16">Flit</text></g><g data-walk-target="c"><path d="M205 243 L350 335" stroke="var(--accent)" stroke-width="2" fill="none"/><polygon points="350,335 338.877476179746,333.864454374372 344.23492220835004,325.42065356842005" fill="var(--accent)"/><text x="277.5" y="279.0" text-anchor="middle" font-size="16">Format</text></g><g data-walk-target="d"><path d="M680 243 L550 335" stroke="var(--accent)" stroke-width="2" fill="none"/><polygon points="550,335 555.2743678294779,325.1419553663331 561.0510564046202,333.30466748338216" fill="var(--accent)"/><text x="615.0" y="279.0" text-anchor="middle" font-size="16">Format</text></g></svg><figcaption>Author-drawn teaching diagram based on PCI Express Base 6.0. Exchanges unrelated to this lesson are omitted.</figcaption></figure><dl class="st-terms" aria-label="Terms in this passage"><div><dt>OHC</dt><dd>Orthogonal Header Content</dd></div></dl><section id="format"><h2>Why start with the format?</h2><p>In Non-Flit Mode, locate Fmt/Type in Figure 2-4, then consult Tables 2-2 and 2-3. Fmt distinguishes header size and data presence; Type also determines routing. A Memory Read requests data without carrying that read data in its request. For example, a separate Non-Flit 32-bit-address Memory Read with Length=2 and no Prefix or Digest has only a 12-byte Request Header; its data returns in Completion packets. The Type/format determines whether Length describes data present in this packet.</p><p>For Flit Mode, restart with Figure 2-6 and Table 2-5. The eight-bit Type is a different encoding: NOP is 00h, while a 32-bit-address Memory Read is 03h. Reusing the Non-Flit decoding table misidentifies the packet.</p></section>
<section id="extensions"><h2>How do extensions affect the data position?</h2><p>OHC (Orthogonal Header Content, optional header extensions) is indicated in Figure 2-6. Read the presence/order rules on p.131, then Table 2-6 for the applicable A format. A Memory Request with explicit Byte Enables uses OHC-A1 in Figure 2-7. OHC follows the Header Base in A-B-C-E order.</p><p>TS (Trailer Size) describes the trailer separately from Length. Non-Flit Mode instead has its own prefix and TD (TLP Digest presence) rules. Determine the entire packet size before locating the next packet.</p></section>
<section id="packet-layout"><h2>Follow the same write intent through both formats</h2>
<div class="example"><p><strong>Simulated data: this teaching scenario does not represent a particular device or platform.</strong> Two independent traces each contain a Memory Write from configured Endpoint 03:00.0 to <code>0x80001000</code>. Assume the address and path are usable, device-initiated access is permitted, and no Prefix, IDE or TPH is present. Reserved and otherwise unused fields are zero. External evidence identifies each Link mode, and the complete logical TLP has already been recovered.</p><dl class="st-terms" aria-label="Terms in this passage"><div><dt>IDE</dt><dd>Integrity and Data Encryption</dd></div><div><dt>TPH</dt><dd>TLP Processing Hints</dd></div></dl>
<p>Both payloads are <code>A0 A1 A2 A3 B0 B1 B2 B3</code>, with Length=2 DW (Double Words, four bytes each), but only the middle four bytes are selected. First DW BE=<code>1100b</code> and Last DW BE=<code>0011b</code>. The Flit example starts after TLP reassembly; it is not a complete FLIT. Hex below follows the figures' byte 0, byte 1 order, with four bytes per line, rather than CPU DWORD read values.</p>
<h3>Decode the 20-byte Non-Flit TLP</h3>
<pre><code style="font-size: 1rem">40 00 00 02
03 00 00 3C
80 00 10 00
A0 A1 A2 A3
B0 B1 B2 B3</code></pre>
<p>Figure 2-4 splits the first byte, <code>0x40</code>, into Fmt=<code>010b</code> and Type=<code>00000b</code>. Tables 2-2/2-3 identify their combination as a Memory Write with a three-DWORD Header and data. Figure 2-5 then gives Length=2 and TD=0: 12 bytes of Header, eight bytes of Data Payload and no Digest, totaling <strong>20 bytes</strong>.</p>
<p>Next, Figure 2-31 locates Requester ID <code>03 00</code> in bytes 4–5, or <code>0x0300</code>, corresponding to 03:00.0 here. Bytes 8–11 give address <code>0x80001000</code>. Figure 2-26 and Table 2-10 locate Header byte 7=<code>0x3C</code>: its high nibble is Last DW BE=<code>0011b</code>, and its low nibble is First DW BE=<code>1100b</code>. The Header ends at byte 11; data starts at <strong>byte 12</strong>.</p>
<h3>Decode the 24-byte Flit-format TLP</h3>
<pre><code style="font-size: 1rem">40 01 00 02
03 00 00 00
80 00 10 00
00 00 00 3C
A0 A1 A2 A3
B0 B1 B2 B3</code></pre>
<p>Start again with Figure 2-6: the entire first byte, <code>0x40</code>, is Type. Entry #64 in Table 2-5 identifies a 32-bit-address Memory Write, a three-DWORD Header Base, and Data Payload determined by Length. Its first byte happens to match the preceding example, so that byte alone does not identify the Link mode.</p>
<p>Byte 1 has OHC=<code>00001b</code>, indicating OHC-A. Byte 2 has TS=<code>000b</code>, indicating no Trailer; Length remains 2. Figure 2-40 locates the 12-byte Header Base. Table 2-6 selects OHC-A1 for this Memory Request, and Figure 2-7 shows its one-DWORD layout. The BE fields are in byte 3 relative to that OHC block: overall TLP byte 12+3=<strong>byte 15</strong>, containing <code>0x3C</code>.</p>
<p>Data therefore starts at <strong>byte 16</strong>, and the TLP totals 12+4+8=<strong>24 bytes</strong>. PV=0 in this OHC-A1 means no valid Process Address Space ID (PASID); the other unused fields are zero. OHC-A1 supplies partial-write byte selection without increasing the data payload length.</p>
<figure class="diagram"><svg viewBox="0 0 820 370" style="min-width: 640px" role="img" aria-labelledby="packet-layout-title packet-layout-desc"><title id="packet-layout-title">The same partial write has different payload offsets in Non-Flit and Flit formats</title><desc id="packet-layout-desc">Both cases use a three-DWORD base and an eight-byte payload. Non-Flit places byte enables in the header, so data starts at byte12. Flit adds one DWORD of OHC-A1 after its Header Base, so data starts at byte16. Total logical TLP sizes are20 and24 bytes.</desc><text x="20" y="63" font-size="18">Non-Flit</text><text x="20" y="238" font-size="18">Flit</text><rect x="130" y="35" width="330" height="72" rx="8" fill="var(--surface-alt)" stroke="var(--line)" stroke-width="1"/><text x="295.0" y="64" text-anchor="middle" font-size="18">Header</text><text x="295.0" y="90" text-anchor="middle" font-size="18">3 DW = 12 bytes</text><rect x="460" y="35" width="220" height="72" rx="8" fill="var(--blue-soft)" stroke="var(--accent)" stroke-width="2"/><text x="570.0" y="64" text-anchor="middle" font-size="18">Data Payload</text><text x="570.0" y="90" text-anchor="middle" font-size="18">2 DW = 8 bytes</text><rect x="130" y="210" width="330" height="72" rx="8" fill="var(--surface-alt)" stroke="var(--line)" stroke-width="1"/><text x="295.0" y="239" text-anchor="middle" font-size="18">Header Base</text><text x="295.0" y="265" text-anchor="middle" font-size="18">3 DW = 12 bytes</text><rect x="460" y="210" width="110" height="72" rx="8" fill="var(--blue-soft)" stroke="var(--accent)" stroke-width="2"/><text x="515.0" y="239" text-anchor="middle" font-size="18">OHC-A1</text><text x="515.0" y="265" text-anchor="middle" font-size="18">1 DW</text><rect x="570" y="210" width="220" height="72" rx="8" fill="var(--blue-soft)" stroke="var(--accent)" stroke-width="2"/><text x="680.0" y="239" text-anchor="middle" font-size="18">Data Payload</text><text x="680.0" y="265" text-anchor="middle" font-size="18">2 DW = 8 bytes</text><text x="130" y="133" text-anchor="middle" font-size="17">0</text><text x="460" y="133" text-anchor="middle" font-size="17">12</text><text x="680" y="133" text-anchor="middle" font-size="17">20</text><text x="130" y="308" text-anchor="middle" font-size="17">0</text><text x="460" y="308" text-anchor="middle" font-size="17">12</text><text x="570" y="308" text-anchor="middle" font-size="17">16</text><text x="790" y="308" text-anchor="middle" font-size="17">24</text><path d="M130 114 H680 M130 289 H790" stroke="var(--line)"/><text x="295" y="163" text-anchor="middle" font-size="17">BE in Header byte 7</text><text x="460" y="344" text-anchor="middle" font-size="17">BE in OHC-A1 byte 3 = TLP byte 15</text></svg><figcaption>Author-created layout for the two simulated logical TLPs. Numbers are byte offsets from each TLP start; the right endpoint is the total size. Neither row includes Data Link or Physical Layer framing.</figcaption></figure>
</div>
<p>Section 2.2.5.2 explains why the extension is needed for this intent: without OHC-A1, a two-DWORD Memory Request implies First and Last DW BE=<code>1111b</code>. All eight bytes would be enabled, changing the intended middle-four-byte write. OHC presence affects the access performed by the receiver.</p>
<p>A Non-Flit decoder applied to the second trace could misread byte 7=<code>0x00</code> as both BE fields and mistake OHC bytes <code>00 00 00 3C</code> for the payload start, shifting data by four bytes. Correct the analyzer mode first; these artifacts do not establish that an erroneous packet actually appeared on the Link.</p>
<details class="source-note"><summary>Connected figure and table reading</summary><p>PCI Express Base Specification Revision 6.0: Figure 2-4 <em>Fields Present in All TLPs</em> (PDF/printed p.119) → Figure 2-5 <em>Fields Present in All Non-Flit Mode TLP Headers</em>, Table 2-2 <em>Fmt[2:0] Field Values</em>/Table 2-3 <em>Fmt[2:0] and Type[4:0] Field Encodings</em> (pp.120–121) → Figure 2-31 <em>Request Header Format for 32-bit Addressing of Memory</em> (p.163) → Figure 2-26/Table 2-10 <em>Byte Enables Location and Correspondence</em> (pp.150–151). For Flit, restart with Figure 2-6 <em>First DW of Header Base</em> (p.122) → Table 2-5 <em>Flit Mode TLP Header Type Encodings</em>, entry #64, Type=40h (p.125) → TS/OHC rules in §2.2.1.2 and Table 2-6 <em>OHC-A Included Fields for OHC-A1 through OHC-A5</em> (pp.130–132) → Figure 2-40 <em>Flit Mode Mem32 Request</em> (p.169) and Figure 2-7 <em>OHC-A1</em> (p.132). Section 2.2.5.2 <em>Byte Enable Rules for Flit Mode</em> (p.152) defines implied BE values without OHC-A1. PDF and printed page numbers match here. This is a reading route, not a hardware execution sequence.</p></details>
</section>
<section id="bytes"><h2>Why do eight payload bytes update only four bytes?</h2>
<p>Continue the same simulated writes. Section 2.2.5.1 and Table 2-10 map each BE bit to a data byte: First DW BE bit 0 selects the lowest-address byte in the first DW; Last DW BE bit 0 selects the lowest-address byte in the last DW. First=<code>1100b</code> selects offsets +2 and +3; Last=<code>0011b</code> selects +4 and +5.</p>
<div class="table-wrap"><table><caption>Both formats carry the same data and select the same memory bytes</caption><thead><tr><th scope="col">Data offset</th><th scope="col">Address</th><th scope="col">Payload content</th><th scope="col">Write under these BE values</th></tr></thead><tbody><tr><td>+0, +1</td><td>0x80001000–0x80001001</td><td>A0, A1</td><td>Do not write these bytes.</td></tr><tr><td>+2, +3</td><td>0x80001002–0x80001003</td><td>A2, A3</td><td>Write A2, A3.</td></tr><tr><td>+4, +5</td><td>0x80001004–0x80001005</td><td>B0, B1</td><td>Write B0, B1.</td></tr><tr><td>+6, +7</td><td>0x80001006–0x80001007</td><td>B2, B3</td><td>Do not write these bytes.</td></tr></tbody></table></div>
<p>The selected range is <code>0x80001002–0x80001005</code>, totaling four bytes, while each TLP still carries eight payload bytes. Length remains 2 DW; disabled bytes are not removed from the packet. This example stays within a 4-KB boundary and selects contiguous bytes. Other lengths, alignments or non-contiguous patterns require the full §2.2.5.1 rules.</p>
<p>In the Non-Flit example, changing to a one-DWORD Request requires Last DW BE= <code>0000b</code>; the example's <code>0011b</code> cannot simply be retained. Read the conditions following Figure 2-26 together with the field locations.</p>
</section>
<section id="next"><h2>Continue into receiver handling</h2><p>Section 2.2.9 identifies requests requiring a Completion (transaction response). A Memory Read receives data in its completion; a normal posted Memory Write has no corresponding successful completion. Chapter 15 follows receiver checks and the resulting response.</p></section>
<section id="sources"><h2>Edition and sources</h2><p>This chapter uses PCI Express Base Specification Revision 6.0 (6.0-1.0-PUB). Document and PDF page numbers match. Example configurations and values are author assumptions, not device measurements.</p><details class="source-note"><summary>Complete source locations</summary><ul><li>§2.2.1.1; §2.2.1.2; pp.119,120,121,122,123; Figures 2-4, 2-5, 2-6; Tables 2-2, 2-3, 2-4, 2-5</li><li>§2.2.1.2; pp.130,131,132; Figures 2-7; Tables 2-6</li><li>§2.2.5.1; pp.149,150; Figures 2-26</li><li>§2.2.9; pp.195</li></ul></details></section>
</article>
<nav class="bottom-nav" aria-label="Course and editions"><a href="/DOCS/pcie-course/index.html">Course overview</a><a href="/DOCS/pcie-course/chapter-14.html">Full Chinese tutorial</a><a href="/pcie/chapter-14-zh-tw/">繁體中文</a></nav>
</div>
