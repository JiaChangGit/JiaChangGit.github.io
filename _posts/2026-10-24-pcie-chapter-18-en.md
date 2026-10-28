---
layout: post
title: "PCIe Chapter 18: Encoding, Flits, CRC, and FEC"
date: 2026-10-24 00:00:00 +0800
last_modified_at: 2026-10-28 00:00:00 +0800
permalink: /pcie/chapter-18-en/
categories: [PCIe]
tags: [PCIe, Specification]
lang: en
spec_teaching: true
spec_series: pcie
description: "Flit、編碼與錯誤更正，怎麼放在同一張圖裡？"
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
<nav class="bottom-nav" aria-label="Course and editions"><a href="/DOCS/pcie-course/index.html">Course overview</a><a href="/DOCS/pcie-course/chapter-18.html">Full Chinese tutorial</a><a href="/pcie/chapter-18-zh-tw/">繁體中文</a></nav>
<article class="lesson">
<p>The previous chapter separated credit, Ack, and transaction completion. Here a TLP (Transaction Layer Packet) enters a Flit (fixed-size transfer unit) and crosses the Lanes to the receiver. First follow normal placement and checks, then use Selective Replay to see why TLP content and DLP are handled differently.</p><figure class="diagram"><svg viewBox="0 0 900 420" role="img" aria-labelledby="ch18-en-t ch18-en-d"><title id="ch18-en-t">Roles and events in this chapter</title><desc id="ch18-en-d">Connect encoding, Flit contents, and the scope of error protection.</desc><g data-walk-target="tlp"><rect x="40" y="25" width="820" height="44" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="450.0" y="54" text-anchor="middle" font-size="16">TLP: transaction-dependent header and data</text></g><g data-walk-target="flit"><rect x="40" y="145" width="820" height="68" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="450.0" y="174" text-anchor="middle" font-size="16">Flit: 256 bytes</text><text x="450.0" y="198" text-anchor="middle" font-size="16">236 TLP + 6 DLP + 8 CRC + 6 ECC</text></g><g data-walk-target="wire"><rect x="40" y="310" width="820" height="44" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="450.0" y="339" text-anchor="middle" font-size="16">Wire encoding depends on rate; PAM4 at 64 GT/s</text></g><g data-walk-target="a"><path d="M450 69 L450 145" stroke="var(--accent)" stroke-width="2" fill="none"/><polygon points="450,145 445.0,135.0 455.0,135.0" fill="var(--accent)"/><text x="300" y="105" text-anchor="middle" font-size="16">Pack into fixed units</text></g><g data-walk-target="b"><path d="M450 213 L450 310" stroke="var(--accent)" stroke-width="2" fill="none"/><polygon points="450,310 445.0,300.0 455.0,300.0" fill="var(--accent)"/><text x="300" y="260" text-anchor="middle" font-size="16">Distribute over lanes</text></g></svg><figcaption>Author-drawn overview based on Base 6.0. DLP means Data Link Layer Payload, CRC means Cyclic Redundancy Check, and ECC means Error Correcting Code.</figcaption></figure><dl class="st-terms" aria-label="Terms in this passage"><div><dt>PAM4</dt><dd>Pulse Amplitude Modulation with 4 levels</dd></div></dl>
<section id="mode"><h2>Choose the mode before the wire decoder</h2><p>64.0 GT/s uses PAM4 (four-level pulse-amplitude modulation) and Flit Mode. Lower rates can also use Flit Mode. Establish the Link, direction, rate, and mode at the observation time before decoding a trace.</p><dl class="st-terms" aria-label="Terms in this passage"><div><dt>PAM4</dt><dd>Pulse Amplitude Modulation with 4 levels</dd></div></dl><p>The identification note on p.309 distinguishes Flit Mode Supported in the PCI Express Capabilities Register, Flit Mode Disable in Link Control, and Flit Mode Status in Link Status 2. The last field describes operation in Flit Mode now or in the future. Training advertisements and the successfully negotiated variable <code>Flit_Mode_Enabled</code> are separate information.</p><div class="table-wrap"><table><thead><tr><th scope="col">Rate</th><th scope="col">Wire encoding</th><th scope="col">Flit Mode detail</th></tr></thead><tbody><tr><td>2.5 / 5.0 GT/s</td><td>8b/10b: 8-bit data characters become 10-bit Symbols</td><td>Traditional STP, SDP, END, and EDB packet markers are not used</td></tr><tr><td>8.0 / 16.0 / 32.0 GT/s</td><td>128b/130b: 128-bit payload plus a 2-bit Sync Header</td><td>Per-Lane Block encoding remains; Non-Flit Mode Framing Tokens are not used</td></tr><tr><td>64.0 GT/s</td><td>1b/1b and PAM4: two bits per signaling interval</td><td>Use Flit Mode and the transmit/receive processing in Figures 4-22 and 4-23</td></tr></tbody></table></div><p>Packaging and wire encoding answer different questions. The name 1b/1b does not remove Flit management, CRC, or correction overhead.</p><p class="source-note">Base 6.0 §§4.2.1, 4.2.2, 4.2.3, 4.2.3.1 (pp.309, 318, 340); Figures 4-22 and 4-23 (p.342).</p></section>

<section id="layout"><h2>Follow a Flit byte to its Lane</h2><p>Read the fixed areas in §4.2.3.3, then select the placement table for the Link width. Offsets below start at byte 0 of one Flit. The TLP area may contain several TLPs or a portion of a TLP.</p><div class="table-wrap"><table><thead><tr><th scope="col">Flit byte range</th><th scope="col">Size</th><th scope="col">Purpose</th></tr></thead><tbody><tr><td>0–235</td><td>236 bytes</td><td>TLP content: headers, data, and required NOP (no-operation) TLPs</td></tr><tr><td>236–241</td><td>6 bytes</td><td>DLP (Data Link Layer Payload), numbered DLP0–DLP5</td></tr><tr><td>242–249</td><td>8 bytes</td><td>CRC (Cyclic Redundancy Check) over the first 242 bytes, excluding ECC</td></tr><tr><td>250–255</td><td>6 bytes</td><td>ECC (Error Correcting Code); protection covers the entire Flit, including CRC</td></tr></tbody></table></div><div class="example"><p><strong>Simulated data:</strong> This author-created teaching case is not a device or platform measurement. Assume an established 64.0 GT/s x4 Link with aligned, decoded data and specification Logical Lane numbers.</p><p>Select Table 4-12 for x4. Read Lane 0 through Lane 3 across a row, then move down: bytes 0–3 occupy Lanes 0–3, and byte 4 returns to Lane 0. The selected positions below show how this continues into DLP and protection bytes.</p><div class="table-wrap"><table><thead><tr><th scope="col">Flit byte</th><th scope="col">Content</th><th scope="col">Logical Lane</th><th scope="col">Position check</th></tr></thead><tbody><tr><td>236</td><td>DLP0</td><td>0</td><td>Bytes 236–239 carry DLP0–DLP3</td></tr><tr><td>237</td><td>DLP1</td><td>1</td><td>Adjacent Lane after DLP0</td></tr><tr><td>242</td><td>CRC0</td><td>2</td><td>Bytes 240–241 still carry DLP4–DLP5</td></tr><tr><td>250</td><td>ECC1[0]</td><td>2</td><td>Bytes 248–249 carry CRC6–CRC7</td></tr><tr><td>252</td><td>ECC0[0]</td><td>0</td><td>The final group is ECC0[0], ECC1[1], ECC2[1], ECC0[1]</td></tr></tbody></table></div><p>Keep the content label and position together. The ECC area starts at byte 250, but that byte is ECC1[0], not ECC0[0]. This example follows placement without treating table rows as training or protocol wait times.</p></div><p>Next read Table 4-15 from the continuation of TLP 19 through subsequent headers, data, and NOPs. It shows why one Flit need not begin with a new TLP. When no TLP is ready, §4.2.3.4.1 requires NOP TLPs (no-operation packets) with alignment and packing rules; unused space is not arbitrary padding.</p><p><strong>Author calculation:</strong> <code>236/256=92.1875%</code> is the TLP-area fraction, before TLP headers and NOPs. It is not application throughput; see <a href="/DOCS/pcie-course/chapter-37.html#capacity">Chapter 37</a> for performance estimates.</p><p class="source-note">Base 6.0 §4.2.3.3 (pp.351–352); Table 4-12 <em>Flit interleaving in a x4 Link</em> (p.354); §4.2.3.4.1 and Table 4-15 <em>Example TLP Placement in Flit Mode on a x16 Link</em> (pp.357–359).</p></section>

<section id="protection"><h2>Follow normal correction and checking first</h2><p>PAM4 (two bits per interval using four voltage levels) increases signaling density, but smaller eye height and width increase susceptibility to errors. FEC (Forward Error Correction) attempts correction before the Flit CRC check.</p><p>Read Figures 4-22 and 4-23 together. The transmitter generates eight CRC bytes from the 236-byte TLP area and six-byte DLP, generates ECC, then distributes the Flit across Lanes. The receiver performs applicable Lane decoding and descrambling, aggregates the Flit, applies FEC decoding/correction, and checks CRC. These are conceptual processing diagrams, not a mandate for identical internal datapath widths.</p><dl class="st-terms" aria-label="Terms in this passage"><div><dt>FEC</dt><dd>Forward Error Correction</dd></div></dl><p>For the x4 case, assume one correctable byte error is corrected, no ECC group reports an uncorrectable error, CRC passes, and Flit Usage and Flit_Status use legal encodings. This meets the valid-Flit conditions in §4.2.3.4.2. Sequence, replay state, and TLP-format rules still determine which TLP content can be delivered; a passing CRC does not complete a Request.</p><p>The three colors in Table 4-12 identify ECC groups, not Lanes. Each group can correct one byte error. The distribution across groups matters, so a total count of erroneous bytes alone is insufficient. A CRC failure or an ECC-group uncorrectable indication prevents valid-Flit treatment; receive and replay rules then apply.</p><p class="source-note">Base 6.0 §4.2.3.1; Figures 4-22 <em>Transmit side at 64.0 GT/s</em> and 4-23 <em>Receive side at 64.0 GT/s</em> (pp.341–342); §4.2.3.1.1 (pp.342–343); §4.2.3.4.2 (p.359); §§4.2.3.4.3–4.2.3.4.4 (pp.384–385).</p></section>

<section id="dlp-replay"><h2>Must a replayed Flit be byte-for-byte identical?</h2><p><strong>TLP content is replayed; DLP carries current management information.</strong> Section 4.2.3.3 excludes DLP from the Link Layer Retry Buffer. Since CRC covers DLP, CRC and ECC are generated for the content being transmitted now.</p><div class="example"><p><strong>Simulated data:</strong> Author-created data for teaching, not measurements. Root Port 00:01.0 and Endpoint 01:00.0 share the 64.0 GT/s x4 Link. Both are in Normal Flit Exchange Phase with Data Link and Flow Control initialization complete. The following is an event excerpt, not a continuous full trace.</p><h3>Decode the transmitted DLP before assigning a direction to its sequence</h3><p>The Root Port transmits a Payload Flit with Explicit Sequence Number 12Ah. Its saved pre-channel DLP0–DLP5 are <code>51 2A 80 00 00 00</code>. Assume its previous transmitted Flit was NOP, making Prior Flit was Payload zero. These bytes are the transmitter's original content; a damaged receiver-side DLP is not reliable evidence after a CRC failure.</p><div class="table-wrap"><table><thead><tr><th scope="col">Field in Tables 4-17 / 4-19</th><th scope="col">Decoded value</th><th scope="col">Use in this case</th></tr></thead><tbody><tr><td>DLP0[7:6]: Flit Usage</td><td>01b</td><td>Payload Flit contains part of at least one non-NOP TLP</td></tr><tr><td>DLP0[4]: Type of DLLP Payload</td><td>1b</td><td>Inspect DLP2[7] to select Optimized_Update_FC or Flit_Marker</td></tr><tr><td>DLP0[3:2]: Replay Command</td><td>00b</td><td>The included sequence explicitly identifies the transmitted Flit</td></tr><tr><td>{DLP0[1:0], DLP1[7:0]}: Flit Sequence Number</td><td><code>(1h &lt;&lt; 8) | 2Ah = 12Ah</code></td><td>Combine high two bits and low eight bits, rather than reading DLP1 alone</td></tr><tr><td>DLP2–DLP5: Flit_Marker</td><td>80000000h</td><td>bit31=1 selects Flit_Marker; Flit_Status=00b supplies no Nullified or Poisoned indication here</td></tr></tbody></table><dl class="st-terms" aria-label="Terms in this passage"><div><dt>DLLP</dt><dd>Data Link Layer Packet</dd></div></dl></div><h3>Decode the reverse-direction Selective Nak</h3><p>CRC still fails after FEC processing at the Endpoint. Assume later received information identifies the invalid Flit as Payload, sufficient RX Retry Buffer exists, and the Endpoint chooses Selective Nak (a request to replay one specified Flit). One valid reverse-direction NOP Flit carries <code>1D 29 80 00 00 00</code>. Its preceding Flit in that direction was also NOP, so Prior Flit was Payload is zero.</p><p>Here <code>Replay Command=11b</code>. Sequence <code>129h</code> means the last valid received Flit, and the requested replay is <code>129h + 1 = 12Ah</code>. It refers to Root Port → Endpoint traffic, not a newly assigned sequence for this reverse NOP Flit. Command 10b would mean Standard Nak, requesting all unacknowledged Flits rather than this single-Flit scope.</p>
<div class="table-wrap"><table><thead><tr><th scope="col">Direction and capture point</th><th scope="col">DLP0–DLP5</th><th scope="col">Replay Command</th><th scope="col">Sequence field</th><th scope="col">Meaning in this row</th></tr></thead><tbody><tr data-dlp-case="payload"><td>Root Port → Endpoint, before transmission</td><td><code>51 2A 80 00 00 00</code></td><td>00b</td><td>12Ah</td><td>The transmitted Payload Flit</td></tr><tr data-dlp-case="selective"><td>Endpoint → Root Port, valid reception</td><td><code>1D 29 80 00 00 00</code></td><td>11b</td><td>129h</td><td>Requests replay of 12Ah</td></tr></tbody></table></div>
<figure class="diagram"><svg viewBox="0 0 900 450" style="min-width:640px" role="img" aria-labelledby="flit-replay-title flit-replay-desc"><title id="flit-replay-title">Selective Replay retains TLP content and uses current DLP</title><desc id="flit-replay-desc">An invalid Payload Flit 12Ah leads to a Selective Nak carrying 129h. The Root Port replays 12Ah with retained TLP content, current DLP, and newly generated CRC and ECC. Other traffic is omitted.</desc><rect x="45" y="20" width="300" height="56" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="195" y="44" text-anchor="middle" font-size="18">Root Port 00:01.0</text><text x="195" y="65" text-anchor="middle" font-size="16">Transmitter of this TLP</text><rect x="555" y="20" width="300" height="56" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="705" y="44" text-anchor="middle" font-size="18">Endpoint 01:00.0</text><text x="705" y="65" text-anchor="middle" font-size="16">Receiver of this TLP</text><path d="M195 76 V430 M705 76 V430" stroke="var(--line)" stroke-dasharray="5 5" fill="none"/><path d="M195 132 H705" stroke="var(--accent)" stroke-width="2"/><polygon points="705,132 695,127 695,137" fill="var(--accent)"/><text x="450" y="116" text-anchor="middle" font-size="17">Payload Flit 12Ah</text><rect x="545" y="151" width="320" height="49" rx="8" fill="var(--surface-alt)" stroke="var(--line)"/><text x="705" y="181" text-anchor="middle" font-size="16">Invalid reception: no TLP delivery</text><path d="M705 242 H195" stroke="var(--accent)" stroke-width="2"/><polygon points="195,242 205,237 205,247" fill="var(--accent)"/><text x="450" y="226" text-anchor="middle" font-size="17">Selective Nak: 129h requests 12Ah</text><rect x="35" y="263" width="320" height="66" rx="8" fill="var(--surface-alt)" stroke="var(--line)"/><text x="195" y="289" text-anchor="middle" font-size="16">Retained TLP + current DLP</text><text x="195" y="314" text-anchor="middle" font-size="16">Generate CRC and ECC again</text><path d="M195 374 H705" stroke="var(--accent)" stroke-width="2"/><polygon points="705,374 695,369 695,379" fill="var(--accent)"/><text x="450" y="358" text-anchor="middle" font-size="17">Replay: Explicit Sequence Number = 12Ah</text><text x="705" y="410" text-anchor="middle" font-size="16">Process after validity / sequence checks</text></svg><figcaption>Author-drawn excerpt with no time scale. Other Flits, waits, and repeated Naks are omitted. This case uses Selective Replay; Standard Replay has a different scope.</figcaption></figure>
<h3>Compare replay content and the receive outcome</h3><p>The Root Port schedules replay of 12Ah, retrieving TLP content from its TX Retry Buffer and using current DLP information. When it sends the replay with an Explicit Sequence Number, it uses the stored 12Ah. The Endpoint applies validity and sequence checks and processes stored/replayed content in receive order, preventing replay from becoming a newly delivered transaction.</p><p>The excerpt omits scheduling waits, other Flits, and repeated Naks. Section 4.2.3.4.2.1.3 requires at least three consecutive Nak Flits in Normal Flit Exchange Phase, subject to its exceptions. One arrow is therefore not a complete wire schedule. Read Figure 4-33 next: first follow the single invalid Payload Flit and Selective Replay, then the later consecutive invalid Flits and Standard Nak.</p><p>Successful replay establishes a recovered Link-transfer outcome for this case. The original Transaction still determines the required Completion and final result. See <a href="/DOCS/pcie-course/chapter-14.html">Chapter 14</a> for TLP formats and <a href="/DOCS/pcie-course/chapter-5.html">Chapter 5</a> for Request/Completion analysis.</p></div><p class="source-note">Base 6.0 §4.2.3.3 (p.352); Figure 4-29 <em>DLP Byte to Bit Number Assignment</em> (p.359); Figure 4-30 <em>DLP Bit usage</em>, Tables 4-16 <em>Flit Types</em>, 4-17 <em>DLP Bytes in the Flit</em> (pp.360–361), and 4-19 <em>Flit_Marker</em> (p.362); §§4.2.3.4.2.1.3–4.2.3.4.2.1.7 (pp.370–383), including Figure 4-33 <em>Flit Ack/Nak/Replay Example</em> (p.383).</p></section>

<section id="scramble"><h2>Use appendices when verifying algorithm outputs</h2><p>The layout, DLP, and receive rules are enough for the case above. Use the appendices when checking a specific encoder, decoder, or check-code output.</p><div class="table-wrap"><table><thead><tr><th scope="col">Verification task</th><th scope="col">Source</th><th scope="col">Condition to retain</th></tr></thead><tbody><tr><td>2.5 / 5.0 GT/s data-character encoding</td><td>Appendix B, Table B-1 <em>8b/10b Data Symbol Codes</em> (p.1531 onward)</td><td>Select by byte and Running Disparity, the per-Lane accumulated imbalance; this is not a 64.0 GT/s coding table</td></tr><tr><td>8b/10b scrambling output</td><td>§C.1 <em>8b/10b Data Scrambling Example</em> (p.1541)</td><td>Alternative implementations must produce the same output; this example is not a universal scrambler for every rate</td></tr><tr><td>Flit ECC encode/decode</td><td>§4.2.3.4.4; Appendix J (p.1595); §J.2 <em>84 Byte to 86 Byte Encoder</em> (p.1607)</td><td>Apply the interleaving before checking check/parity results; a different pipeline must preserve reference outputs</td></tr><tr><td>Eight-byte Flit CRC</td><td>§4.2.3.4.3; Appendix K <em>MATLAB created generator matrix for CRC code</em> (p.1619)</td><td>Input is 242 TLP/DLP bytes; preserve the specified matrix and bit ordering</td></tr></tbody></table></div></section>

<section id="sources"><h2>Edition and sources</h2><p>PCI Express Base Specification Revision 6.0 (6.0-1.0-PUB) is the technical authority. Printed and PDF-viewer page numbers match for the cited locations. Assumed values, topology, and event excerpts are marked beside the cases.</p><details class="source-note"><summary>Complete reading locations</summary><ul><li>§4.2.1 <em>8b/10b Encoding for 2.5 GT/s and 5.0 GT/s Data Rates</em> (p.309); §4.2.2 <em>128b/130b Encoding for 8.0 GT/s, 16.0 GT/s, and 32.0 GT/s Data Rates</em> (p.318); §4.2.3 <em>Flit Mode Operation</em> and §4.2.3.1 <em>1b/1b Encoding for 64.0 GT/s and higher Data Rates</em> (p.340).</li><li>Figures 4-22 / 4-23 (p.342) explain processing order; §4.2.3.1.1 <em>PAM4 Signaling</em> and Figure 4-24 (pp.342–343) supply signaling/error context.</li><li>§4.2.3.3 <em>Data Stream in Flit Mode</em> (pp.351–352); Tables 4-10–4-14 (pp.352–356) select x16 / x8 / x4 / x2 / x1 placement. This case reads Table 4-12 (p.354).</li><li>§4.2.3.4.1 <em>TLP Bytes in Flit</em>, Table 4-15 (pp.357–359); §4.2.3.4.2 <em>DLP Bytes in Flit</em>, Figures 4-29–4-30, Tables 4-16–4-17 and 4-19 (pp.359–362).</li><li>§4.2.3.4.2.1.3 <em>Normal Flit Exchange Phase</em> (pp.370–372); §4.2.3.4.2.1.4 <em>Received Ack and Nak Processing</em> (p.372); §4.2.3.4.2.1.5 <em>Ack, Nak, and Discard Rules</em> (pp.373–378); §4.2.3.4.2.1.6 <em>Flit Replay Scheduling</em> (pp.378–379); §4.2.3.4.2.1.7 <em>Flit Replay Transmit Rules</em> (pp.380–383, including the Figure 4-33 example).</li><li>§4.2.3.4.3 <em>CRC Bytes in Flit</em> (pp.384–385); §4.2.3.4.4 <em>ECC Bytes in Flit</em> (p.385 onward); Appendices B, C.1, J, J.2, and K as mapped in the preceding table.</li></ul></details></section>
</article>
<nav class="bottom-nav" aria-label="Course and editions"><a href="/DOCS/pcie-course/index.html">Course overview</a><a href="/DOCS/pcie-course/chapter-18.html">Full Chinese tutorial</a><a href="/pcie/chapter-18-zh-tw/">繁體中文</a></nav>
</div>
