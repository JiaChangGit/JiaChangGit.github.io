---
layout: post
title: "PCIe Chapter 25: PTM Roles, Exchanges, and Precision"
date: 2026-10-24 00:00:00 +0800
last_modified_at: 2026-10-29 00:00:00 +0800
permalink: /pcie/chapter-25-en/
categories: [PCIe]
tags: [PCIe, Specification]
lang: en
spec_teaching: true
spec_series: pcie
description: "如何把兩回合 PTM 交換，換成可解讀事件的共同時間？"
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
<nav class="bottom-nav" aria-label="Course and editions"><a href="/DOCS/pcie-course/index.html">Course overview</a><a href="/DOCS/pcie-course/chapter-25.html">Full Chinese tutorial</a><a href="/pcie/chapter-25-zh-tw/">繁體中文</a></nav>
<article class="lesson">
<p>PTM (Precision Time Measurement) relates local event timestamps to a shared PTM Master Time. Start with the time hierarchy and controlling Function, then follow two dialogs through historical timestamps, ResponseD fields and Equation 6-2.</p><figure class="diagram"><svg viewBox="0 0 900 270" style="min-width:640px" role="img" aria-labelledby="ch25-en-t ch25-en-d"><title id="ch25-en-t">One time hierarchy, two separate PTM Links</title><desc id="ch25-en-d">The Root Port supplies time. The Switch requests time upstream and responds downstream. Each Link has its own dialogs.</desc><g data-walk-target="root"><rect x="20" y="25" width="210" height="90" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="125" y="58" text-anchor="middle" font-size="18">Root Port</text><text x="125" y="92" text-anchor="middle" font-size="15">PTM Root + Responder</text></g><g data-walk-target="switch"><rect x="345" y="25" width="210" height="90" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="450" y="58" text-anchor="middle" font-size="18">Switch</text><text x="450" y="92" text-anchor="middle" font-size="15">Requester + Responder</text></g><g data-walk-target="ep"><rect x="670" y="25" width="210" height="90" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="775" y="58" text-anchor="middle" font-size="18">Endpoint</text><text x="775" y="92" text-anchor="middle" font-size="15">PTM Requester</text></g><g data-walk-target="link1"><path d="M230 68 H345" stroke="var(--accent)" stroke-width="2"/><text x="287.5" y="48" text-anchor="middle" font-size="16">Link 1</text></g><g data-walk-target="link2"><path d="M555 68 H670" stroke="var(--accent)" stroke-width="2"/><text x="612.5" y="48" text-anchor="middle" font-size="16">Link 2</text></g><g data-walk-target="context"><rect x="40" y="155" width="820" height="95" rx="8" fill="var(--surface-alt)" stroke="var(--line)"/><text x="450" y="191" text-anchor="middle" font-size="17">Each Link: Upstream Port requests; Downstream Port responds.</text><text x="450" y="225" text-anchor="middle" font-size="17">Switch internal time distribution is implementation specific.</text></g></svg><figcaption>Author-drawn time hierarchy. Each Link has separate dialogs; distribution of time inside a Switch is implementation specific.</figcaption></figure>
<section id="scenario"><h2>Define the clocks and participants</h2><p>The Root Port → Switch → Endpoint topology has two Links. The Switch requests time upstream and supplies it downstream; Endpoint PTM Messages do not traverse the Switch to reach the Root Port. Figure 6-23 explains this division. Port background is in <a href="/DOCS/pcie-course/chapter-1.html">Chapter 1</a>.</p><p><strong>Simulated data:</strong> the topology, values and timing were created for teaching and do not represent hardware measurements. The Root Port is the PTM Root. The Switch and single-Function Endpoint support ePTM (Enhanced Precision Time Management). Basic transport is ready; the Switch has valid master time. The two-dialog example uses Non-Flit Mode, with no Replay, duplicate, Reset or context-invalidation event.</p><p>All values are normalized to ns. For this short calculation assume equal, stable clock rates, no drift and symmetric one-way transit delays. These are example assumptions, not measured properties of arbitrary Links.</p></section>
<section id="discover"><h2>Follow capability discovery into the actual roles</h2><p>Walk the Extended Capability list to ID=001Fh, Version=1. Figure 7-310, <em>PTM Capability Structure</em>, locates Capability at P+04h and Control at P+08h relative to base P. Figure 7-312/Table 7-275 then decode the roles:</p><div class="table-wrap"><table><thead><tr><th scope="col">Object</th><th scope="col">P+04h: Capability</th><th scope="col">Roles / Local Clock Granularity</th></tr></thead><tbody><tr data-ptm-cap="root"><td>Root Port</td><td>0000040Eh</td><td>Requester=0; Responder=1; Root=1; ePTM=1; 4 ns</td></tr><tr data-ptm-cap="switch"><td>Switch</td><td>0000080Fh</td><td>Requester=1; Responder=1; Root=1; ePTM=1; 8 ns</td></tr><tr data-ptm-cap="endpoint"><td>Endpoint</td><td>00000009h</td><td>Requester=1; Responder=0; Root=0; ePTM=1; Granularity=RsvdP</td></tr></tbody></table></div><p>The Root Port supplies and responds with time. The Switch supports both Requester and Responder roles. Its Root capability does not select it as Root: this example keeps its Root Select clear and uses the upstream source. The Endpoint's Local Clock Granularity is RsvdP because Root Capable is clear; a zero read there does not mean that the Endpoint has no local clock.</p><p>One Capability controls the entire Switch. Switch Downstream Ports must not implement independent PTM Capabilities. With a multi-Function Upstream Port, the controlling Function need not be the Switch Upstream Port Function. Locate the real controlling structure before attributing its behavior to downstream Ports.</p><p class="source-note">Base 6.0 §7.9.15 <em>Precision Time Management Extended Capability (PTM Capability)</em>, pp.1260–1264; Figures 7-310–7-312, Tables 7-274/7-275.</p></section>
<section id="configure"><h2>Select the source and enable the hierarchy</h2><p>Figure 7-313/Table 7-276 separates PTM Enable [0], Root Select [1] and Effective Granularity [15:8]. Root Port Control=00000003h enables it as Root. The Switch has PTM Enable=1 and Root Select=0: it obtains upstream time and responds downstream.</p><p>Enable the associated Downstream Port's PTM control before the Upstream Port's control on each Link. Here configure the Root Port, then enable the Switch, then the Endpoint. The Switch's single Enable also controls downstream responder behavior; do not search each downstream Port for a separate Control structure.</p><p>Endpoint software must program Effective Granularity from the maximum Local Clock Granularity reported by the PTM Root and intervening Time Sources: max(4 ns, 8 ns)=8 ns. Endpoint Control=00000801h therefore means Enable=1, Root Select=0 and Effective Granularity=08h. The field conveys expected accuracy information; it does not adjust the clock or bound every source of error.</p><p>Special encodings matter. Local Clock Granularity=00h means a Time Source has no local clock and propagates upstream timing; FFh means greater than 254 ns. If an intervening Switch reports 00h, Effective Granularity=00h means unknown. Do not treat that unknown as an ordinary zero and discard it when taking a maximum.</p><p class="source-note">Base 6.0 §6.21.3, p.800; §§7.9.15.2–7.9.15.3, Tables 7-275/7-276, pp.1262–1264.</p></section>
<section id="dialog"><h2>Why does the second dialog need the first?</h2><p>Focus on Link 2: Endpoint Upstream Port as Requester, Switch Downstream Port as Responder. In Figure 6-22, t1/t4 belong to the Requester and t2/t3 to the Responder; primes identify the next dialog.</p><figure class="diagram" id="ptm-dialog-figure"><svg viewBox="0 0 900 660" style="min-width:720px" role="img" aria-labelledby="ch25-dialog-en-t ch25-dialog-en-d"><title id="ch25-dialog-en-t">Two dialogs: current receipt time, previous turnaround</title><desc id="ch25-dialog-en-d">The first Response provides history. The second ResponseD carries master time 5200 ns from the second dialog and turnaround 200 ns from the first.</desc><text x="150" y="30" text-anchor="middle" font-size="17">Endpoint / Upstream Port</text><path d="M150 65 V600" stroke="var(--line)" stroke-width="2"/><text x="750" y="30" text-anchor="middle" font-size="17">Switch / Downstream Port</text><path d="M750 65 V600" stroke="var(--line)" stroke-width="2"/><text x="150" y="55" text-anchor="middle" font-size="15">Requester: local ns</text><text x="750" y="55" text-anchor="middle" font-size="15">Responder: master ns</text><path d="M150 110 L750 150" stroke="var(--accent)" stroke-width="2" fill="none"/><polygon points="750,150 740,144 740,156" fill="var(--accent)"/><path d="M750 210 L150 250" stroke="var(--accent)" stroke-width="2" fill="none"/><polygon points="150,250 160,244 160,256" fill="var(--accent)"/><path d="M150 385 L750 425" stroke="var(--accent)" stroke-width="2" fill="none"/><polygon points="750,425 740,419 740,431" fill="var(--accent)"/><path d="M750 495 L150 535" stroke="var(--accent)" stroke-width="2" fill="none"/><polygon points="150,535 160,529 160,541" fill="var(--accent)"/><text x="150" y="96" text-anchor="middle" font-size="16">t1 = 1,000</text><text x="750" y="135" text-anchor="middle" font-size="16">t2 = 3,200</text><text x="750" y="195" text-anchor="middle" font-size="16">t3 = 3,400</text><text x="150" y="280" text-anchor="middle" font-size="16">t4 = 1,600</text><text x="150" y="370" text-anchor="middle" font-size="16">t1′ = 3,000</text><text x="750" y="410" text-anchor="middle" font-size="16">t2′ = 5,200</text><text x="750" y="480" text-anchor="middle" font-size="16">t3′ = 5,520</text><text x="150" y="565" text-anchor="middle" font-size="16">t4′ = 3,720</text><text x="450" y="105" text-anchor="middle" font-size="16">1. PTM Request</text><text x="450" y="210" text-anchor="middle" font-size="16">PTM Response</text><text x="450" y="380" text-anchor="middle" font-size="16">2. PTM Request</text><text x="450" y="460" text-anchor="middle" font-size="16">ResponseD: Master Time = 5,200 ns</text><text x="450" y="485" text-anchor="middle" font-size="16">Propagation Delay = 200 ns</text><path d="M40 315 H860" stroke="var(--line)" stroke-dasharray="6 5"/><text x="450" y="340" text-anchor="middle" font-size="16">First Response → next Request: 1,400 ns ≥ 1 μs</text><text x="450" y="630" text-anchor="middle" font-size="17">ResponseD combines t2′ with the preceding interval t3 − t2.</text></svg><figcaption>Author-created case based on Figure 6-22. Time flows downward. Line lengths are illustrative, not to scale.</figcaption></figure><div class="table-wrap"><table><thead><tr><th scope="col">Dialog</th><th scope="col">Event</th><th scope="col">Symbol</th><th scope="col">Value</th><th scope="col">Time domain</th></tr></thead><tbody><tr data-ptm-time="t1"><td>1</td><td>Endpoint TX Request</td><td>t1</td><td>1,000 ns</td><td>Local</td></tr><tr data-ptm-time="t2"><td>1</td><td>Switch RX Request</td><td>t2</td><td>3,200 ns</td><td>PTM Master Time</td></tr><tr data-ptm-time="t3"><td>1</td><td>Switch TX Response</td><td>t3</td><td>3,400 ns</td><td>PTM Master Time</td></tr><tr data-ptm-time="t4"><td>1</td><td>Endpoint RX Response</td><td>t4</td><td>1,600 ns</td><td>Local</td></tr><tr data-ptm-time="t1-next"><td>2</td><td>Endpoint TX Request</td><td>t1′</td><td>3,000 ns</td><td>Local</td></tr><tr data-ptm-time="t2-next"><td>2</td><td>Switch RX Request</td><td>t2′</td><td>5,200 ns</td><td>PTM Master Time</td></tr><tr data-ptm-time="t3-next"><td>2</td><td>Switch TX ResponseD</td><td>t3′</td><td>5,520 ns</td><td>PTM Master Time</td></tr><tr data-ptm-time="t4-next"><td>2</td><td>Endpoint RX ResponseD</td><td>t4′</td><td>3,720 ns</td><td>Local</td></tr></tbody></table></div><p>The first Request finds no valid preceding history, so the Switch returns Response, completing the dialog without timing data. Both sides still retain their local timestamps. After receiving Response, the Requester must wait at least 1 μs before another Request. This case waits 3,000−1,600=1,400 ns.</p><p>On the second Request, the Switch has the previous turnaround t3−t2=200 ns and the current receipt time t2′=5,200 ns in the master domain, so it returns ResponseD. Those fields refer to different dialogs. The current turnaround t3′−t2′=320 ns belongs to a later response; it cannot replace the 200 ns carried now.</p><p class="source-note">Base 6.0 §6.21.2, Figure 6-22, pp.797–798; §6.21.3.1, p.801; §6.21.3.2, p.803.</p></section>
<section id="message-fields"><h2>Locate the fields before interpreting Propagation Delay</h2><p>Table 2-35 identifies Request as Msg/Code52h, Response as Msg/Code53h, and ResponseD as MsgD/Code53h. Code53h alone does not distinguish a timing-data response. All use TC0 and local Routing=100b. Requester ID is the transmitting Port's ID on that segment.</p><p>Use Figure 2-61 for Non-Flit Request/Response and Figure 2-62 for Non-Flit ResponseD. ResponseD carries 64-bit PTM Master Time in Header bytes 8–15 and 32-bit Propagation Delay in a 1 DW Data Payload. In Flit Mode, perform transport processing and TLP reassembly before using Figures 2-63/2-64; the base Header format differs.</p><dl class="st-terms" aria-label="Terms in this passage"><div><dt>DW</dt><dd>Double Word, a four-byte unit</dd></div><div><dt>TLP</dt><dd>Transaction Layer Packet</dd></div></dl><p>Despite its name, Propagation Delay carries the <strong>preceding responder turnaround interval</strong>, t3−t2, under §6.21.3.2. Data bytes <code>00 00 00 C8</code> use this edition's Interpretation A: byte0 is the most significant byte, yielding 000000C8h=200 ns. The Master Time field is 0000000000001450h=5,200 ns. One-way Link transit time still needs calculation from the Requester's stored round trip.</p><p>Reversing those payload bytes yields C8000000h=3,355,443,200 ns, larger than this case's 600 ns round trip. Check byte order, field boundaries, dialog association and both Ports' configuration before accepting a negative calculated delay. Optional PTM Propagation Delay Adaptation supports compatibility with older Interpretation B; capable Switches control interpretation independently per Port. This example assumes both ends use A.</p><p class="source-note">Base 6.0 §2.2.8.10, Table 2-35 and Figures 2-61–2-64, pp.190–192; §6.21.3, pp.800–801; §6.21.3.2, p.803.</p></section>
<section id="time-case"><h2>Convert a local event into the master domain</h2><p>Subtract the previous responder turnaround from the previous local round trip. Under the symmetry assumption, half the remainder estimates one-way transit time. Equation 6-2 subtracts it from current t2′ to obtain master time at current t1′:</p><div class="table-wrap"><table><thead><tr><th scope="col">Meaning</th><th scope="col">Calculation</th><th scope="col">Result</th></tr></thead><tbody><tr data-ptm-result="rtt"><td>Previous local round trip</td><td>t4 − t1 = 1,600 − 1,000</td><td>600 ns</td></tr><tr data-ptm-result="turnaround"><td>Previous responder turnaround</td><td>t3 − t2 = 3,400 − 3,200</td><td>200 ns</td></tr><tr data-ptm-result="one-way"><td>Estimated one-way Link delay</td><td>(600 − 200) / 2</td><td>200 ns</td></tr><tr data-ptm-result="master"><td>Master time at current Request transmission</td><td>t2′ − 200 = 5,200 − 200</td><td>5,000 ns</td></tr><tr data-ptm-result="event"><td>Later stored local event</td><td>5,000 + (4,000 − 3,000)</td><td>6,000 ns</td></tr></tbody></table></div><p>The final row additionally assumes a local event at 4,000 ns, with the same valid context and clock-rate relationship. Local 3,000 ns maps to master 5,000 ns; adding the local 1,000 ns interval gives master 6,000 ns. This is an author deduction under the short, drift-free case assumptions. An implementation must track rate differences and context refresh; the 2,000 ns offset is not permanent.</p><p>Using the current 320 ns turnaround with the previous 600 ns round trip would give a false 140 ns one-way estimate and master time 5,060 ns at t1′. The 60 ns error comes from mixing dialogs. Keeping only the latest ResponseD while losing t1/t4 likewise leaves missing inputs, not zero-valued inputs.</p><p class="source-note">Base 6.0 §6.21.2, Equation 6-2, p.797; <em>PTM Theory and Operation</em> Implementation Note and Figure 6-23 <em>Precision Time Measurement Example</em>, p.799. Numeric inputs and event conversion are author-created.</p></section>
<section id="context"><h2>Why can Replay invalidate timing even when delivery is deduplicated?</h2><p>Reliable transport avoids repeated logical delivery, but PTM measures actual transmission and reception. Section 6.21.3 requires the specified t1 Request-transmit, t2 Request-receive, t3 Response/ResponseD-transmit and t4 Response-receive timestamps to update even for the stated Replay/duplicate cases. A deduplicated Transaction list alone cannot recover those wire times.</p><p>This case supports ePTM. Replaying the Endpoint's PTM Request invalidates the Requester context. Under the ePTM rule the context remains invalid until two successive dialogs complete successfully without replays. Replaying Response/ResponseD or receiving a duplicate Request also requires the Responder to invalidate the associated history under §6.21.3.2, so a later Response may be needed to rebuild it.</p><p>Figure 6-24, <em>PTM Requester Operation</em>, connects Invalid Context, Request issuance, Response/ResponseD and Valid Context. Response takes the wait-at-least-1 μs path; ResponseD supplies timing data, subject to the text's ePTM invalidation requirements. After issuing a Request, do not issue another until a corresponding response, Reset, or 100 μs without a corresponding PTM Message. This is not Memory Read Completion Timeout.</p><p>The Responder must <strong>attempt</strong> to issue Response or ResponseD within 10 μs. Missing history requires Response. With history available but master time still being retrieved elsewhere, Response is also permitted when retrieval is expected to exceed 10 μs. The rule does not guarantee a data-bearing ResponseD on every Request.</p><p class="source-note">Base 6.0 §§6.21.3–6.21.3.2, Figure 6-24, pp.800–803. Keep ePTM/MUST@FLIT qualifications separate from generic Non-Flit behavior; the example explicitly supports ePTM.</p></section>
<section id="limits"><h2>Attach the accuracy and validity conditions to the result</h2><p>Equation 6-2 estimates one-way transit as half the round trip. Actual one-way delays of 300 ns and 100 ns still total 400 ns and yield an estimate of 200 ns. Subtraction from responder receipt time then overestimates the true transmit time by 100 ns. Effective Granularity=8 ns does not bound that asymmetry error.</p><p>Figure 6-25, <em>PTM Timestamp Capture Example</em>, places capture near the Physical Layer. Non-Flit timestamps refer to the first bit of the framing STP Symbol/Token at Port pins. Flit timestamps refer to the Flit_Marker Indicator bit identifying the contained PTM Message; a Flit may contain at most one PTM Message. Internal capture requires consideration of path compensation. The specification does not bound overall capture accuracy and consistency; verify the analyzer's reference point too.</p><p>Retimers may introduce asymmetric and variable delays; consult their manufacturer documentation. A non-Root Switch using a local context must invalidate it no more than 10 ms after the last upstream dialog and refresh before further downstream ResponseD transmission. Periodic refresh is optional when implementation-specific means guarantee phase lock with master time. This is not a universal 10 ms Endpoint-context lifetime.</p><p>Master time observed through PTM must be monotonic and strictly increasing. Keep the time domain and valid interval with each converted event. Different PTM Hierarchies may have independent master times; PTM time is not automatically UTC or an OS wall clock. Software access to context, internal Switch distribution and triggers for refreshing time have implementation-specific aspects. Enable=1 permits participation; actual dialogs and context validity still need evidence.</p><p class="source-note">Base 6.0 §6.21.1, p.796; §6.21.2 and Implementation Notes, pp.798–799; §6.21.3, p.800; §6.21.3.3, p.804; Figure 6-25, p.805.</p></section>
<section id="reading"><h2>Turn an unknown Trace into a reading route</h2><p>Identify the hierarchy, controlling Function, selected Root and adjacent Ports. Confirm mode and Message type, then pair Requests with Response/ResponseD using Table 2-35. Mark dialogs as in Figure 6-22, verify turnaround byte order and retained local timestamps, and check for context invalidation between dialogs. Apply Equation 6-2 only after those inputs match; retain granularity, capture reference and asymmetry limits alongside the result.</p><p>A Control snapshot alone cannot provide a time conversion. One ResponseD still lacks the preceding local round trip. If the clock relationship has changed, the old context is unsuitable for new events. Each step points to concrete missing evidence without assigning a unique faulty component.</p></section>
<section id="sources"><h2>Edition and source map</h2><p>PCI Express Base Specification Revision 6.0 (6.0-1.0-PUB) supplies the technical rules. Printed and PDF-viewer pages match. All topology, registers, timing and arithmetic examples are author-created; no hardware programming or accuracy measurements were performed. No external website is used as technical evidence.</p><details class="source-note"><summary>Sources by reading purpose</summary><ul><li>Roles: §6.21 <em>Precision Time Measurement (PTM) Mechanism</em>, §6.21.1 <em>Introduction</em>, pp.795–796; Figure 6-21 <em>Example System Topologies using PTM</em>, p.796.</li><li>Dialogs and calculation: §6.21.2 <em>PTM Link Protocol</em>, pp.797–799; Figure 6-22 <em>Precision Time Measurement Link Protocol</em> and Equation 6-2 <em>PTM Master Time</em>, p.797; Figure 6-23 <em>Precision Time Measurement Example</em>, p.799.</li><li>Configuration and validity: §6.21.3 <em>Configuration and Operational Requirements</em>, pp.800–801; §6.21.3.1 <em>PTM Requester Role</em>, pp.801–802; Figure 6-24 <em>PTM Requester Operation</em>, p.802; §6.21.3.2 <em>PTM Responder Role</em>, p.803; §6.21.3.3 <em>PTM Time Source Role - Rules Specific to Switches</em>, pp.804–805; Figure 6-25 <em>PTM Timestamp Capture Example</em>, p.805.</li><li>Messages: §2.2.8.10 <em>Precision Time Measurement (PTM) Messages</em>, Table 2-35 <em>Precision Time Measurement Messages</em>, Figures 2-61–2-64, pp.190–192. Select the mode-specific Request/Response and ResponseD layouts.</li><li>Capability and Control: §7.9.15 <em>Precision Time Management Extended Capability (PTM Capability)</em>, pp.1260–1264; Figure 7-310 <em>PTM Capability Structure</em>, Figure 7-311/Table 7-274 <em>PTM Extended Capability Header</em>, p.1261; Figure 7-312/Table 7-275 <em>PTM Capability Register</em>, pp.1262–1263; Figure 7-313/Table 7-276 <em>PTM Control Register</em>, pp.1263–1264.</li><li>External boundaries: Retimer delay requires manufacturer data. Software context access, integration with software clocks and measured accuracy require device/platform interfaces and measurements; there is no universal Base-defined Linux or firmware readout interface.</li></ul></details></section>
</article>
<nav class="bottom-nav" aria-label="Course and editions"><a href="/DOCS/pcie-course/index.html">Course overview</a><a href="/DOCS/pcie-course/chapter-25.html">Full Chinese tutorial</a><a href="/pcie/chapter-25-zh-tw/">繁體中文</a></nav>
</div>
