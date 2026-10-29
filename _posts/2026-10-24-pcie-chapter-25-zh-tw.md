---
layout: post
title: "PCIe Chapter 25：PTM 與時間同步的角色、交換與精度"
date: 2026-10-24 00:00:00 +0800
last_modified_at: 2026-10-29 00:00:00 +0800
permalink: /pcie/chapter-25-zh-tw/
categories: [PCIe]
tags: [PCIe, Specification]
lang: zh-TW
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
<div class="pcie-article spec-teaching" data-spec-series="pcie" lang="zh-Hant-TW">
<nav class="bottom-nav" aria-label="課程與語言版本"><a href="/DOCS/pcie-course/index.html">課程總覽</a><a href="/DOCS/pcie-course/chapter-25.html">繁中完整教學</a><a href="/pcie/chapter-25-en/">English</a></nav>
<article class="lesson">
<p>PTM 讓元件以共同時間解讀本地事件。本章先確認時間來源與控制範圍，再用兩回合完整案例串起歷史時間、ResponseD 欄位、時間公式與有效條件。</p><dl class="st-terms" aria-label="本段名詞"><div><dt>PTM</dt><dd>Precision Time Measurement，精確時間量測</dd></div></dl><figure class="diagram"><svg viewBox="0 0 900 270" style="min-width:640px" role="img" aria-labelledby="ch25-zh-t ch25-zh-d"><title id="ch25-zh-t">同一個時間階層中的兩條獨立 PTM Link</title><desc id="ch25-zh-d">Root Port 提供時間。Switch 在上游取得時間，再從下游回覆 Endpoint；每條 Link 有各自的交換回合。</desc><g data-walk-target="root"><rect x="20" y="25" width="210" height="90" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="125" y="58" text-anchor="middle" font-size="18">Root Port</text><text x="125" y="92" text-anchor="middle" font-size="15">時間來源／回覆方</text></g><g data-walk-target="switch"><rect x="345" y="25" width="210" height="90" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="450" y="58" text-anchor="middle" font-size="18">Switch</text><text x="450" y="92" text-anchor="middle" font-size="15">上游要求／下游回覆</text></g><g data-walk-target="ep"><rect x="670" y="25" width="210" height="90" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="775" y="58" text-anchor="middle" font-size="18">Endpoint</text><text x="775" y="92" text-anchor="middle" font-size="15">Requester：要求方</text></g><g data-walk-target="link1"><path d="M230 68 H345" stroke="var(--accent)" stroke-width="2"/><text x="287.5" y="48" text-anchor="middle" font-size="16">Link 1</text></g><g data-walk-target="link2"><path d="M555 68 H670" stroke="var(--accent)" stroke-width="2"/><text x="612.5" y="48" text-anchor="middle" font-size="16">Link 2</text></g><g data-walk-target="context"><rect x="40" y="155" width="820" height="95" rx="8" fill="var(--surface-alt)" stroke="var(--line)"/><text x="450" y="191" text-anchor="middle" font-size="17">每條 Link：Upstream Port 要求，Downstream Port 回覆。</text><text x="450" y="225" text-anchor="middle" font-size="17">Switch 內部如何傳遞共同時間，由實作決定。</text></g></svg><figcaption>作者繪製的時間階層示意。PTM（Precision Time Measurement，精確時間量測）在每條 Link 分別交換；Switch 內部傳遞時間的方式由實作決定。</figcaption></figure><section id="scenario"><h2>本地時鐘不同，先建立什麼關係？</h2><p>沿用 <a href="/DOCS/pcie-course/chapter-1.html">Chapter 1 的 Port 與相鄰 Link</a> 概念：Root Port → Switch → Endpoint 是兩條 Link。Switch 從上游取得共同時間，再透過內部機制提供給下游 Port；Endpoint 的 PTM 訊息不會穿過 Switch，一路直接找 Root Port。這正是 Figure 6-23 要說明的分工。</p><p><strong>【模擬資料】以下資料為教學用途建立，不代表特定硬體或平台。</strong>本章選 Root Port 為 PTM Root。Switch 與 Endpoint 的基本傳輸已就緒，均支援 ePTM（Enhanced Precision Time Management，增強式精確時間管理）；分析的 Endpoint 只有 Function 0。數值案例在 Non-Flit Mode 下進行，兩回合間沒有 Replay、Duplicate、Reset 或 Context 失效事件。Switch 已取得有效共同時間。</p><p>為了先看懂 Equation 6-2，案例把所有時間都換成 ns，假設兩邊時鐘速率在這段短時間內相同、沒有漂移，往返的單向傳輸延遲也相同。這些是算例假設；後面再說明不對稱與 Replay 如何影響結果。</p></section>
<section id="discover"><h2>想查 Endpoint 能否參與，從哪個結構開始？</h2><p>先沿 Extended Capability 鏈找 ID=001Fh、Version=1。Figure 7-310 <em>PTM Capability Structure</em> 給出布局：若結構起點為 P，Capability 在 P+04h，Control 在 P+08h。接著用 Figure 7-312／Table 7-275 解碼角色，先不要把結構存在當成已經啟用。</p><div class="table-wrap"><table><thead><tr><th scope="col">對象</th><th scope="col">P+04h: Capability</th><th scope="col">角色／Local Clock Granularity</th></tr></thead><tbody><tr data-ptm-cap="root"><td>Root Port</td><td>0000040Eh</td><td>Requester=0; Responder=1; Root=1; ePTM=1; 4 ns</td></tr><tr data-ptm-cap="switch"><td>Switch</td><td>0000080Fh</td><td>Requester=1; Responder=1; Root=1; ePTM=1; 8 ns</td></tr><tr data-ptm-cap="endpoint"><td>Endpoint</td><td>00000009h</td><td>Requester=1; Responder=0; Root=0; ePTM=1; Granularity=RsvdP</td></tr></tbody></table></div><p>Root Port 提供時間並回覆；Switch 同時要求與回覆。雖然 Switch 的 PTM Root Capable=1，本章仍將 Root Select 清為零，使用上游 Root Port 的時間。Endpoint 只有 Requester 角色；它的 Local Clock Granularity 欄位因 Root Capable=0 而為 RsvdP，不能將其中的零解釋成「Endpoint 沒有本地時鐘」。</p><p>對 Switch，§7.9.15 規定一份 Capability 控制整顆 Switch。Switch Downstream Port 不得各自實作這個 Capability；上游是多 Function 時，控制 Function 也不一定就是 Switch Upstream Port Function。應先找出真正的控制結構，再將它的設定對到下游行為。</p><p class="source-note">Base 6.0 §7.9.15 <em>Precision Time Management Extended Capability (PTM Capability)</em>，pp.1260–1264；Figures 7-310–7-312、Tables 7-274／7-275。</p></section>
<section id="configure"><h2>找到能力後，怎麼選時間來源與啟用？</h2><p>開 Figure 7-313／Table 7-276，分開看 PTM Enable [0]、Root Select [1] 與 Effective Granularity [15:8]。本章 Root Port 的 Control=00000003h，表示已啟用且選為 Root；Switch 的 PTM Enable=1、Root Select=0，向上取得共同時間並在下游回覆。</p><p>同一條 Link 必須先啟用 Downstream Port 所屬的 PTM 控制，才能啟用 Upstream Port 所屬的控制。因此案例先設定 Root Port，再啟用 Switch，最後啟用 Endpoint。Switch 的一次 Enable 同時控制其 PTM 下游回覆行為，不能在每個下游 Port 尋找不存在的獨立 PTM Control。</p><p>Endpoint 的 Effective Granularity 必須採 PTM Root 與所有中間 Time Sources 回報的最大 Local Clock Granularity。本章為 max(4 ns, 8 ns)=8 ns，因此 Endpoint 的 Control=00000801h：Enable=1、Root Select=0、Effective Granularity=08h。這是預期精度資訊，欄位本身不調整時鐘，也不是讀到 8 ns 就代表所有誤差都小於 8 ns。</p><p>還要辨認特殊編碼：Local Clock Granularity=00h 表示 Time Source 不實作本地時鐘、只轉傳上游時間；FFh 表示大於 254 ns。若路徑中有 Switch 回報 00h，Effective Granularity 的 00h 表示未知，不能把它當成普通數值零，略過後再取最大值。</p><p class="source-note">Base 6.0 §6.21.3，p.800；§7.9.15.2／§7.9.15.3，Tables 7-275／7-276，pp.1262–1264。</p></section>
<section id="dialog"><h2>為什麼第二回合需要保存第一回合的時間？</h2><p>現在只觀察 Link 2：左邊是 Endpoint 的 Upstream Port，右邊是 Switch 的 Downstream Port。先看 Figure 6-22 <em>Precision Time Measurement Link Protocol</em>，把 t1／t4 放在要求方，t2／t3 放在回覆方；再用單引號辨認第二回合。下圖將規格中的關係換成完整算例：</p><figure class="diagram" id="ptm-dialog-figure"><svg viewBox="0 0 900 660" style="min-width:720px" role="img" aria-labelledby="ch25-dialog-zh-t ch25-dialog-zh-d"><title id="ch25-dialog-zh-t">兩回合交換：本回合接收時間與上一回合處理時間</title><desc id="ch25-dialog-zh-d">第一回合建立歷史資料；第二回合 ResponseD 帶回當次接收的共同時間5200ns，以及前次回覆處理時間200ns。</desc><text x="150" y="30" text-anchor="middle" font-size="17">Endpoint / Upstream Port</text><path d="M150 65 V600" stroke="var(--line)" stroke-width="2"/><text x="750" y="30" text-anchor="middle" font-size="17">Switch / Downstream Port</text><path d="M750 65 V600" stroke="var(--line)" stroke-width="2"/><text x="150" y="55" text-anchor="middle" font-size="15">Requester: local ns</text><text x="750" y="55" text-anchor="middle" font-size="15">Responder: master ns</text><path d="M150 110 L750 150" stroke="var(--accent)" stroke-width="2" fill="none"/><polygon points="750,150 740,144 740,156" fill="var(--accent)"/><path d="M750 210 L150 250" stroke="var(--accent)" stroke-width="2" fill="none"/><polygon points="150,250 160,244 160,256" fill="var(--accent)"/><path d="M150 385 L750 425" stroke="var(--accent)" stroke-width="2" fill="none"/><polygon points="750,425 740,419 740,431" fill="var(--accent)"/><path d="M750 495 L150 535" stroke="var(--accent)" stroke-width="2" fill="none"/><polygon points="150,535 160,529 160,541" fill="var(--accent)"/><text x="150" y="96" text-anchor="middle" font-size="16">t1 = 1,000</text><text x="750" y="135" text-anchor="middle" font-size="16">t2 = 3,200</text><text x="750" y="195" text-anchor="middle" font-size="16">t3 = 3,400</text><text x="150" y="280" text-anchor="middle" font-size="16">t4 = 1,600</text><text x="150" y="370" text-anchor="middle" font-size="16">t1′ = 3,000</text><text x="750" y="410" text-anchor="middle" font-size="16">t2′ = 5,200</text><text x="750" y="480" text-anchor="middle" font-size="16">t3′ = 5,520</text><text x="150" y="565" text-anchor="middle" font-size="16">t4′ = 3,720</text><text x="450" y="105" text-anchor="middle" font-size="16">1. PTM Request</text><text x="450" y="210" text-anchor="middle" font-size="16">PTM Response</text><text x="450" y="380" text-anchor="middle" font-size="16">2. PTM Request</text><text x="450" y="460" text-anchor="middle" font-size="16">ResponseD: Master Time = 5,200 ns</text><text x="450" y="485" text-anchor="middle" font-size="16">Propagation Delay = 200 ns</text><path d="M40 315 H860" stroke="var(--line)" stroke-dasharray="6 5"/><text x="450" y="340" text-anchor="middle" font-size="16">首次 Response 後到下次 Request：1,400 ns ≥ 1 μs</text><text x="450" y="630" text-anchor="middle" font-size="17">ResponseD 把本回合 t2′ 與上一回合 t3 − t2 放在一起。</text></svg><figcaption>作者依 Figure 6-22 建立的模擬案例。時間由上往下；線長僅供定位，不按數值比例繪製。</figcaption></figure><div class="table-wrap"><table><thead><tr><th scope="col">回合</th><th scope="col">事件</th><th scope="col">時間點</th><th scope="col">模擬時間</th><th scope="col">所屬時間</th></tr></thead><tbody><tr data-ptm-time="t1"><td>1</td><td>Endpoint TX Request</td><td>t1</td><td>1,000 ns</td><td>Local</td></tr><tr data-ptm-time="t2"><td>1</td><td>Switch RX Request</td><td>t2</td><td>3,200 ns</td><td>PTM Master Time</td></tr><tr data-ptm-time="t3"><td>1</td><td>Switch TX Response</td><td>t3</td><td>3,400 ns</td><td>PTM Master Time</td></tr><tr data-ptm-time="t4"><td>1</td><td>Endpoint RX Response</td><td>t4</td><td>1,600 ns</td><td>Local</td></tr><tr data-ptm-time="t1-next"><td>2</td><td>Endpoint TX Request</td><td>t1′</td><td>3,000 ns</td><td>Local</td></tr><tr data-ptm-time="t2-next"><td>2</td><td>Switch RX Request</td><td>t2′</td><td>5,200 ns</td><td>PTM Master Time</td></tr><tr data-ptm-time="t3-next"><td>2</td><td>Switch TX ResponseD</td><td>t3′</td><td>5,520 ns</td><td>PTM Master Time</td></tr><tr data-ptm-time="t4-next"><td>2</td><td>Endpoint RX ResponseD</td><td>t4′</td><td>3,720 ns</td><td>Local</td></tr></tbody></table></div><p>第一回合開始時，Switch 沒有前次歷史資料，所以回覆 PTM Response。它結束這次 dialog，但不帶時間資料。兩端仍會各自保存本地時間；Endpoint 收到 Response 後，至少等待 1 μs 才能送下一筆 Request。案例實際等待 3,000−1,600=1,400 ns，符合這項條件。</p><p>第二回合收到 Request 時，Switch 同時具備前次 t3−t2=200 ns，以及本次接收 Request 的 PTM Master Time t2′=5,200 ns，因此回覆 ResponseD。這兩個欄位分屬不同回合。本次處理時間 t3′−t2′=320 ns，應留給後續回合使用，不能拿來取代這次 ResponseD 的 200 ns。</p><p class="source-note">Base 6.0 §6.21.2，Figure 6-22，pp.797–798；§6.21.3.1，p.801；§6.21.3.2，p.803。</p></section>
<section id="message-fields"><h2>ResponseD 的資料放在哪裡？Propagation Delay 又代表什麼？</h2><p>先查 Table 2-35 <em>Precision Time Measurement Messages</em>。Request 使用 Msg、Code=52h；Response 使用 Msg、Code=53h；ResponseD 則是 MsgD、Code=53h。因此不能只看 Code=53h 就認定一定帶有時間資料。三者使用 TC0、Routing=100b，在相鄰接收端終止；Requester ID 是本段 Transmitting Port 的 ID。</p><p>Non-Flit Mode 的 Request／Response 看 Figure 2-61，ResponseD 看 Figure 2-62。ResponseD 的 64-bit PTM Master Time 放在 Header bytes 8–15，32-bit Propagation Delay 放在 1 DW Data Payload。換成 Flit Mode 時，先完成承載與 TLP 重組，再使用 Figures 2-63／2-64，不能沿用 Non-Flit Mode 的基本 Header 格式。</p><dl class="st-terms" aria-label="本段名詞"><div><dt>DW</dt><dd>Double Word，4 bytes的資料單位</dd></div><div><dt>TLP</dt><dd>Transaction Layer Packet，交易層封包</dd></div></dl><p>欄位名雖然叫 Propagation Delay，§6.21.3.2 規定填的是<strong>前一回合從收到 Request 到送出 Response 的間隔</strong>，即 t3−t2。本章 Data Byte 0–3 為 <code>00 00 00 C8</code>，依本版 Interpretation A，Byte 0 是最高位元組，所以是 000000C8h＝200 ns。PTM Master Time 欄位則為 0000000000001450h＝5,200 ns。真正的單向 Link 延遲仍要用要求方保存的往返時間推算。</p><p>若工具將這四個 Payload bytes 反過來解成 C8000000h，就得到 3,355,443,200 ns，已經大於本例 600 ns 的本地往返時間。此時先檢查 Byte Order、欄位起點、回合配對及雙端設定；不要把負的推算結果當成真實傳輸延遲。本版也定義可選的 PTM Propagation Delay Adaptation Capability，供兩端與舊 Interpretation B 相容；Switch 具備此能力時，各 Port 的 Interpretation B 控制獨立。本例假設雙端均使用 A，未啟用 B。</p><p class="source-note">Base 6.0 §2.2.8.10，Table 2-35、Figures 2-61–2-64，pp.190–192；§6.21.3，pp.800–801；§6.21.3.2，p.803。</p></section>
<section id="time-case"><h2>拿到 ResponseD 後，如何換算事件時間？</h2><p>先用第一回合的本地時間求往返間隔，再扣掉同一回合的回覆處理時間，剩下的才是兩個方向合計的傳輸時間。依 Equation 6-2 <em>PTM Master Time</em>，在對稱延遲假設下除以二，從本回合 t2′ 扣回去，就得到本回合 Request 送出的 t1′ 所對應的共同時間。</p><div class="table-wrap"><table><thead><tr><th scope="col">要找的量</th><th scope="col">推算方式</th><th scope="col">結果</th></tr></thead><tbody><tr data-ptm-result="rtt"><td>前一回合的本地往返時間</td><td>t4 − t1 = 1,600 − 1,000</td><td>600 ns</td></tr><tr data-ptm-result="turnaround"><td>前一回合的回覆處理時間</td><td>t3 − t2 = 3,400 − 3,200</td><td>200 ns</td></tr><tr data-ptm-result="one-way"><td>估計單向 Link 延遲</td><td>(600 − 200) / 2</td><td>200 ns</td></tr><tr data-ptm-result="master"><td>本回合 Request 送出時的共同時間</td><td>t2′ − 200 = 5,200 − 200</td><td>5,000 ns</td></tr><tr data-ptm-result="event"><td>稍後記錄的本地事件</td><td>5,000 + (4,000 − 3,000)</td><td>6,000 ns</td></tr></tbody></table></div><p>最後一列另假設 Endpoint 在本地 4,000 ns 記錄了一個事件，且 Context 與時鐘速率關係仍有效。前面已建立本地 3,000 ns 對應共同時間 5,000 ns，因此再加上本地經過的 1,000 ns，得到事件的共同時間 6,000 ns。這是在本章短時間、無漂移假設下的作者推演；實作仍須追蹤時鐘速率差與 Context 更新，不能永久套用固定 2,000 ns 位移。</p><p>如果誤拿第二回合的 320 ns 去扣第一回合的 600 ns，單向估計會變成 140 ns，t1′ 的共同時間也會錯算為 5,060 ns。這個 60 ns 的差異來自回合配錯，與四則運算本身無關。只保存最後一筆 ResponseD 而遺失 t1／t4，也會缺少公式所需的資料，不能用零補上。</p><p class="source-note">Base 6.0 §6.21.2，Equation 6-2，p.797；<em>PTM Theory and Operation</em> Implementation Note 與 Figure 6-23 <em>Precision Time Measurement Example</em>，p.799。表中讀值與事件換算均為作者建立。</p></section>
<section id="context"><h2>Replay 已經避免重複交付，PTM 為何還要重建？</h2><p>一般可靠傳輸避免把同一個邏輯 TLP 重複交付，但 PTM 量的是線上實際傳送與接收的時間。§6.21.3 要求送出 Request 的 t1、收到 Request 的 t2、送出 Response／ResponseD 的 t3，以及收到 Response 的 t4，遇到規定的 Replay／Duplicate 情況仍要更新。不能只從去重後的 Transaction 清單推回這些時間點。</p><dl class="st-terms" aria-label="本段名詞"><div><dt>TLP</dt><dd>Transaction Layer Packet，交易層封包</dd></div></dl><p>本章已假設 ePTM 支援。若 Endpoint 的 PTM Request 被 Replay，Requester 必須使內部 PTM Context 失效；依 ePTM 規則，在完成兩次連續成功、沒有 Replay 的 dialog 前，不能繼續使用該 Context。若 Responder 重送 Response／ResponseD 或收到重複 Request，也須依 §6.21.3.2 清除相應歷史時間，後續可能先回 Response 來重新建立資料。</p><p>Figure 6-24 <em>PTM Requester Operation</em> 把這件事分成 Invalid Context、發起 Request、接收 Response／ResponseD 與 Valid Context。收到 Response 會走至少 1 μs 的等待路徑；收到 ResponseD 才有帶資料的路徑，還須搭配本版文字中的 ePTM 失效條件。無回覆時，Requester 在收到對應訊息、Reset，或滿 100 μs 之前，不得再發新的 Request；這項規則不是一般 Memory Read 的 Completion Timeout。</p><p>Responder 收到 Request 後必須<strong>嘗試</strong>在 10 μs 內送 Response 或 ResponseD。歷史資料不足時必須回 Response；若已有歷史間隔但仍須從別處取得共同時間，且預期取得時間超過 10 μs，也允許先回 Response。不能把 10 μs 改寫成每次必定收到 ResponseD 的保證。</p><p class="source-note">Base 6.0 §§6.21.3–6.21.3.2，Figure 6-24，pp.800–803。Non-Flit Mode 與 ePTM／MUST@FLIT 的規範條件須分開閱讀；本案例明確採已支援 ePTM 的情況。</p></section>
<section id="limits"><h2>算出共同時間後，精度還受哪些條件限制？</h2><p>Equation 6-2 用往返傳輸時間的一半估計單向延遲。若兩方向其實分別為 300 ns 與 100 ns，往返合計仍為 400 ns，公式仍估 200 ns；從回覆方接收時間扣回去時，就會比真正的送出時間多算 100 ns。這說明 Effective Granularity=8 ns 並未涵蓋 Link 不對稱造成的全部誤差。</p><p>Figure 6-25 <em>PTM Timestamp Capture Example</em> 提醒擷取點要接近 Physical Layer。Non-Flit Mode 以 Port pins 處 STP Symbol／Token 的第一個 bit 為基準；Flit Mode 以標示內含 PTM Message 的 Flit_Marker Indicator bit 為基準，一個 Flit 最多一個 PTM Message。若實際在內部量測，須考量路徑補償；規格沒有對量測準確性與一致性給出完整界限。Analyzer 的顯示時間也必須先確認其擷取基準。</p><p>Retimer（重定時器）可能引入方向不對稱與變動，須查廠商資料。不是 Root、且使用本地 Context 回覆的 Switch，最晚須在上一次上游 dialog 後 10 ms 內使 Context 失效，之後必須先刷新才能再回 ResponseD；若實作保證本地時鐘與共同時間 phase locked，週期刷新要求可省略。這項 10 ms 條件不是所有 Endpoint Context 通用的固定有效期限。</p><p>透過 PTM 觀察到的共同時間必須單調且嚴格遞增。分析事件時仍須保留時間域與有效期間：同一 PTM Hierarchy 共用一個來源，不同 Hierarchy 的 Master Time 可能獨立；它也不自動等於 UTC 或作業系統的牆上時間。PTM context 如何讓軟體讀取、Switch 內部如何傳時間，以及觸發下一次量測的方法，都有實作決定的部分。讀到 Enable=1，只能先確認允許依角色參與，還需要交換紀錄與 Context 有效性的資料。</p><p class="source-note">Base 6.0 §6.21.1，p.796；§6.21.2 與 Implementation Notes，pp.798–799；§6.21.3，p.800；§6.21.3.3，p.804；Figure 6-25，p.805。</p></section>
<section id="reading"><h2>下次拿到一份 PTM Trace，怎麼接回規格？</h2><p>先畫出時間階層，定位真正的控制 Function、選定 Root 與相鄰 Port。再確認目前模式和訊息種類，依 Table 2-35 配對 Request 與 Response／ResponseD。接著按 Figure 6-22 標記每個回合，核對歷史處理間隔的 byte order、保留的本地時間，以及兩回合之間有沒有 Context 失效事件。資料配齊後才代 Equation 6-2，最後把粒度、擷取點與不對稱誤差附在結果旁。</p><p>如果只有一張 Control 快照，還無法做時間換算；如果只有一筆 ResponseD，還缺前次本地往返時間；如果時鐘關係已改變，舊 Context 就不適合拿來換算新的事件。每一步都對應一份具體資料，無須先猜是哪個元件故障。</p></section>
<section id="sources"><h2>版本與來源</h2><p>本章以 PCI Express Base Specification Revision 6.0（6.0-1.0-PUB）為準，文件印刷頁與 PDF 檢視器頁碼相同。拓撲、讀值、時序與計算均為作者建立；未執行實機設定或時間精度量測。本章沒有以外部網站作技術依據。</p><details class="source-note"><summary>依閱讀目的查完整來源</summary><ul><li>角色與時間階層：§6.21 <em>Precision Time Measurement (PTM) Mechanism</em>、§6.21.1 <em>Introduction</em>，pp.795–796；Figure 6-21 <em>Example System Topologies using PTM</em>，p.796。PTM Root 與各 PCIe 元件的架構角色不同。</li><li>交換與公式：§6.21.2 <em>PTM Link Protocol</em>，pp.797–799；Figure 6-22 <em>Precision Time Measurement Link Protocol</em>、Equation 6-2 <em>PTM Master Time</em>，p.797；Figure 6-23 <em>Precision Time Measurement Example</em>，p.799。先標時間與回合，再推算。</li><li>設定、有效性與擷取：§6.21.3 <em>Configuration and Operational Requirements</em>，pp.800–801；§6.21.3.1 <em>PTM Requester Role</em>，pp.801–802；Figure 6-24 <em>PTM Requester Operation</em>，p.802；§6.21.3.2 <em>PTM Responder Role</em>，p.803；§6.21.3.3 <em>PTM Time Source Role - Rules Specific to Switches</em>，pp.804–805；Figure 6-25 <em>PTM Timestamp Capture Example</em>，p.805。</li><li>訊息格式：§2.2.8.10 <em>Precision Time Measurement (PTM) Messages</em>，Table 2-35 <em>Precision Time Measurement Messages</em>、Figures 2-61–2-64，pp.190–192。分別定位兩種模式的 Request／Response 與 ResponseD，不把 MsgD 的資料負載當成整個時間回覆。</li><li>能力與控制：§7.9.15 <em>Precision Time Management Extended Capability (PTM Capability)</em>，pp.1260–1264；Figure 7-310 <em>PTM Capability Structure</em>、Figure 7-311／Table 7-274 <em>PTM Extended Capability Header</em>，p.1261；Figure 7-312／Table 7-275 <em>PTM Capability Register</em>，pp.1262–1263；Figure 7-313／Table 7-276 <em>PTM Control Register</em>，pp.1263–1264。</li><li>外部邊界：Retimer 方向延遲需查廠商文件；取得 PTM Context、對接軟體時鐘與評估實際誤差，需裝置／平台介面資料與量測。Base 的可選介面不能寫成所有 Linux 或韌體平台通用的讀取方法。</li></ul></details></section>
</article>
<nav class="bottom-nav" aria-label="課程與語言版本"><a href="/DOCS/pcie-course/index.html">課程總覽</a><a href="/DOCS/pcie-course/chapter-25.html">繁中完整教學</a><a href="/pcie/chapter-25-en/">English</a></nav>
</div>
