---
layout: post
title: "PCIe Chapter 16：Traffic Class、Virtual Channel 與仲裁"
date: 2026-10-24 00:00:00 +0800
last_modified_at: 2026-10-28 00:00:00 +0800
permalink: /pcie/chapter-16-zh-tw/
categories: [PCIe]
tags: [PCIe, Specification]
lang: zh-TW
spec_teaching: true
spec_series: pcie
description: "從逐Link映射走到雙端VC啟用，以欄位快照帶讀Count、Map、VC ID、Enable與Pending，再區分Port／VC仲裁、優先群組與等時性契約。"
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
<nav class="bottom-nav" aria-label="課程與語言版本"><a href="/DOCS/pcie-course/index.html">課程總覽</a><a href="/DOCS/pcie-course/chapter-16.html">繁中完整教學</a><a href="/pcie/chapter-16-en/">English</a></nav>
<article class="lesson">
<p>TC（Traffic Class，流量類別）是封包上的分類；VC（Virtual Channel，虛擬通道）將流量對應到佇列、緩衝與流量控制資源。本章先看映射，再用雙端配置案例走完啟用與初始化，最後接到傳送仲裁。</p><figure class="diagram"><svg viewBox="0 0 900 420" role="img" aria-labelledby="ch16-zh-t ch16-zh-d"><title id="ch16-zh-t">分類、映射與共同傳送資源</title><desc id="ch16-zh-d">每一條Link兩端使用一致的TC到VC映射；各Link可採不同配置。</desc><g data-walk-target="tc"><rect x="20" y="30" width="320" height="44" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="180.0" y="59" text-anchor="middle" font-size="16">TC：封包的流量分類</text></g><g data-walk-target="map"><rect x="485" y="30" width="390" height="44" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="680.0" y="59" text-anchor="middle" font-size="16">軟體配置兩端相同的映射</text></g><g data-walk-target="vc0"><rect x="40" y="190" width="340" height="68" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="210.0" y="219" text-anchor="middle" font-size="16">VC0：TC0 固定映射</text><text x="210.0" y="243" text-anchor="middle" font-size="16">也可承載其他 TC</text></g><g data-walk-target="vc1"><rect x="500" y="190" width="350" height="68" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="675.0" y="219" text-anchor="middle" font-size="16">VC1：本例承載 TC7</text><text x="675.0" y="243" text-anchor="middle" font-size="16">獨立資源與流量控制</text></g><g data-walk-target="arb"><rect x="255" y="335" width="390" height="44" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="450.0" y="364" text-anchor="middle" font-size="16">仲裁選擇下一筆傳送流量</text></g><g data-walk-target="a"><path d="M340 52 L485 52" stroke="var(--accent)" stroke-width="2" fill="none"/><polygon points="485,52 475.0,57.0 475.0,47.0" fill="var(--accent)"/><text x="412.5" y="42.0" text-anchor="middle" font-size="16">讀取分類</text></g><g data-walk-target="b"><path d="M600 98 L210 190" stroke="var(--accent)" stroke-width="2" fill="none"/><polygon points="210,190 218.58488245528918,182.83761260270933 220.88083939100602,192.57047352585693" fill="var(--accent)"/><text x="405.0" y="134.0" text-anchor="middle" font-size="16">TC0</text></g><g data-walk-target="c"><path d="M720 98 L670 190" stroke="var(--accent)" stroke-width="2" fill="none"/><polygon points="670,190 670.3820106563359,178.82618830217524 679.1682557520613,183.60132150637384" fill="var(--accent)"/><text x="695.0" y="134.0" text-anchor="middle" font-size="16">TC7</text></g><g data-walk-target="d"><path d="M210 258 L350 335" stroke="var(--accent)" stroke-width="2" fill="none"/><polygon points="350,335 338.8282471643727,334.5618920456617 343.6474346620943,325.7997329588952" fill="var(--accent)"/><text x="280.0" y="286.5" text-anchor="middle" font-size="16">可傳送</text></g><g data-walk-target="f"><path d="M670 258 L550 335" stroke="var(--accent)" stroke-width="2" fill="none"/><polygon points="550,335 555.7160971423175,325.39134590800614 561.1165815589857,333.8076852586577" fill="var(--accent)"/><text x="610.0" y="286.5" text-anchor="middle" font-size="16">可傳送</text></g></svg><figcaption>作者依 Base 6.0 繪製的教學示意；省略與本章無關的交換。</figcaption></figure><dl class="st-terms" aria-label="本段名詞"><div><dt>TC</dt><dd>Traffic Class，流量類別</dd></div></dl><section id="mapping"><h2>TC 與 VC 分別在哪裡決定？</h2><dl class="st-terms" aria-label="本段名詞"><div><dt>VC</dt><dd>Virtual Channel，虛擬通道</dd></div></dl>
<p>TC（Traffic Class，流量類別）是 TLP 上的標籤，沿途保持相同；VC（Virtual Channel，虛擬通道）則由每一條 Link 的映射決定，用來對應佇列、緩衝與流量控制資源。§2.5.1 特別提醒：TLP 沒有 VC ID 欄位，接收端要依 TC/VC Map 找到該 TLP 所屬的 VC。</p><dl class="st-terms" aria-label="本段名詞"><div><dt>TLP</dt><dd>Transaction Layer Packet，交易層封包</dd></div></dl>
<p>先查 §2.2.6.6 的 Table 2-14：TC 是 3-bit 欄位，<code>000b</code> 代表所有 PCIe 裝置都必須支援的預設 TC0；<code>001b–111b</code> 代表 TC1–TC7，用於區分服務類別。實際的 TC 標記與 TC/VC 映射由系統軟體決定；TC 數字本身不保證特定頻寬或延遲。規格在這裡討論 PCIe fabric 內的服務，如何換成其他互連的服務政策則超出本規格的範圍。（Base 6.0 §2.2.6.6、Table 2-14，文件頁／PDF 頁 161。）</p>
<p>先讀 Table 2-43（p.233）。在 VC0、VC1 這一列，右欄示範 TC0–TC6 對應 VC0、TC7 對應 VC1。這是一種配置範例；TC0 必須固定對應 VC0，其他受支援的 TC 則由軟體配置。同一個 TC 在一個 Port 或 Endpoint Function 內，只能映射到一個 VC。</p>
<p>再看 Figure 2-88（p.234）的上半部：Endpoint 到 Switch 的 Link 只有 VC0，TC7 在這一段也走 VC0；Switch 到 Root Complex 的 Link 則把 TC7 對應到 VC1。TC7 的標籤沒有改變，改變的是各段使用的資源。必須一致的是同一條 Link 兩端的 VC ID 與映射，並非整個 Switch 的所有 Ports 都採同一份配置。</p>
<p class="source">規格閱讀：§2.5 Virtual Channel (VC) Mechanism，pp.229–230；§2.5.1 Virtual Channel Identification (VC ID)，p.232；§2.5.2 TC to VC Mapping，Table 2-43 TC to VC Mapping Example，p.233；Figure 2-88 An Example of TC/VC Configurations，p.234。文件頁與 PDF 頁相同。</p></section>
<section id="vc-enable"><h2>兩端都支援 VC1，還要怎麼把它設成可用？</h2>
<p><strong>先配置兩端的 VC ID 與 TC/VC Map，再分別啟用，最後確認兩端的 VC Negotiation Pending 都已清為零。</strong>VC Enable 是控制設定；VC Negotiation Pending 表示該通道的協商是否還在進行。單看其中一端的 Enable=1，還沒有走完這段流程。</p>
<div class="example"><p><strong>【模擬資料】以下資料為教學用途建立，不代表特定硬體或平台。</strong>本例只分析 Root Port 00:01.0 與單一 Function Endpoint 01:00.0 之間的一條 Link。兩端的資料鏈結層持續處於 DL_Active，使用 Non-Flit Mode，不支援 Flit Mode；沒有 MFVC，也沒有使用仲裁表。兩端的 Extended VC Count=1，Low Priority Extended VC Count=0，All VCs Enabled 目前保持 0。</p>
<p>這個 Count 不包含基本的 VC0，所以各端共有兩組 VC Resource registers。配置前，VC0 已可用，TC/VC Map 為 FFh；額外資源尚未啟用。這次要讓 TC0–TC6 留在 VC0，將 TC7 移到 VC1。兩個方向都先停止新增 TC7 交易，並確認相關未完成交易已結束，再開始修改映射。</p>
<h3>先從 Figure 7-221 找到控制與狀態</h3>
<p>假設已沿 Extended Capability List 找到兩端的 Virtual Channel Extended Capability：ID=0002h、Version=1，Root Port 的結構起點為 180h，Endpoint 為 200h。這些起點是各 Function 的 Configuration Space offset，不是全系統共用的地址。</p>
<p>Figure 7-221（p.1183）把每組資源排成 0Ch bytes。選第二組，也就是資源索引 1：Control 的相對位移是 <code>14h + 1 × 0Ch = 20h</code>。Status 在其所在 32-bit 列的高 16 bits，所以 16-bit Status 的相對位移是 <code>18h + 1 × 0Ch + 2 = 26h</code>；不能把整列起點 24h 當成 Status 的存取位置。</p>
<div class="table-wrap"><table style="min-width:640px"><thead><tr><th scope="col">本例讀取對象</th><th scope="col">Root Port 00:01.0</th><th scope="col">Endpoint 01:00.0</th></tr></thead><tbody>
<tr><td>VC Resource Control Register (1)，32-bit</td><td>180h + 20h = <strong>1A0h</strong></td><td>200h + 20h = <strong>220h</strong></td></tr>
<tr><td>VC Resource Status Register (1)，16-bit</td><td>180h + 26h = <strong>1A6h</strong></td><td>200h + 26h = <strong>226h</strong></td></tr></tbody></table></div>
<h3>接著配置 Map 與 VC ID，再啟用</h3>
<p>讀 Table 7-207（pp.1189–1191）時，先定位 TC/VC Map[7:0]，每個 bit 對應同編號的 TC。兩端都先把 TC7 從 VC0 移除，使 VC0 的 Map 由 FFh 變成 <strong>7Fh</strong>；再把資源 1 的 VC ID[26:24] 設為 1，Map 設為 <strong>80h</strong>，此時 VC Enable[31] 先保持 0。中間暫時沒有啟用的 VC 承接 TC7，因此這段期間持續保持 TC7 流量停止。</p>
<p>在本例其他位元均為零的假設下，資源 1 的 32-bit Control 快照為 <strong>01000080h</strong>。等兩端的配置都備妥，再分別將 VC Enable 設為 1，快照成為 <strong>81000080h</strong>。軟體仍須依欄位屬性更新設定，保留 RsvdP 位元；這兩個數字用來解釋欄位如何組成讀值。</p>
<figure class="diagram"><svg style="min-width:640px" viewBox="0 0 900 620" role="img" aria-labelledby="vc-enable-title vc-enable-desc"><title id="vc-enable-title">兩端啟用後，還要等雙端協商完成</title><desc id="vc-enable-desc">在 DL_Active 且兩端 VC Enable 均為一時，讀取雙端 Pending。任一端尚為一就等待後重讀，兩端均為零才使用這個 VC。</desc><rect x="100" y="20" width="600" height="70" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="400.0" y="45" text-anchor="middle" font-size="18">兩端指定 VC ID 1，將 TC7 映射至此資源</text><text x="400.0" y="70" text-anchor="middle" font-size="18">此時先保持這個 VC 停用</text><path d="M400 90 V119" fill="none" stroke="var(--accent)" stroke-width="2.5"/><polygon points="400,119 395,109 405,109" fill="var(--accent)"/><rect x="100" y="120" width="600" height="70" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="400.0" y="145" text-anchor="middle" font-size="18">兩端分別設定 VC Enable = 1</text><text x="400.0" y="170" text-anchor="middle" font-size="18">本例 Link 持續處於 DL_Active</text><path d="M400 190 V224" fill="none" stroke="var(--accent)" stroke-width="2.5"/><polygon points="400,224 395,214 405,214" fill="var(--accent)"/><polygon points="400,225 550,300 400,375 250,300" fill="var(--surface-alt)" stroke="var(--accent)" stroke-width="2"/><text x="400" y="295" text-anchor="middle" font-size="18">兩端 Pending 都為 0？</text><text x="400" y="320" text-anchor="middle" font-size="17">兩端 VC 均已啟用</text><path d="M550 300 H720 V414" fill="none" stroke="var(--accent)" stroke-width="2.5"/><polygon points="720,414 715,404 725,404" fill="var(--accent)"/><text x="720" y="285" text-anchor="middle" font-size="17">否：至少一端為 1</text><rect x="580" y="415" width="280" height="70" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="720.0" y="440" text-anchor="middle" font-size="18">等待後，重讀兩端狀態</text><text x="720.0" y="465" text-anchor="middle" font-size="18">Pending 為唯讀欄位</text><path d="M860 450 H880 V207 H400 V224" fill="none" stroke="var(--accent)" stroke-width="2.5"/><polygon points="400,224 395,214 405,214" fill="var(--accent)"/><path d="M400 375 V524" fill="none" stroke="var(--accent)" stroke-width="2.5"/><polygon points="400,524 395,514 405,514" fill="var(--accent)"/><text x="425" y="405" font-size="17">是</text><rect x="100" y="525" width="600" height="70" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="400.0" y="550" text-anchor="middle" font-size="18">TC7 可使用完成初始化的 VC</text><text x="400.0" y="575" text-anchor="middle" font-size="18">仍須符合 credit、排序及仲裁條件</text></svg><figcaption>作者依 Tables 7-207／7-208 繪製的流程。兩端都要配置；圖中沒有規定雙端寫入的先後，也沒有指定軟體輪詢間隔。</figcaption></figure>
<h3>最後以雙端 Status 確認，不寫入 Pending</h3>
<p>Table 7-208（pp.1191–1192）的 VC Negotiation Pending 位於 Status bit 1，屬性為 RO，由硬體更新。它只有在 Link 處於 <strong>DL_Active 且該 VC Enable=1</strong> 時才有定義。若 VC 尚未啟用，即使工具把這個 bit 顯示為 0，也不能用它確認協商完成。</p>
<div class="table-wrap"><table style="min-width:640px"><thead><tr><th scope="col">啟用後的兩次觀察</th><th scope="col">Root Port 的 16-bit Status</th><th scope="col">Endpoint 的 16-bit Status</th><th scope="col">TC7 的使用時機</th></tr></thead><tbody>
<tr><td>兩端 Enable 均為 1，初始化仍在進行</td><td>0000h：Pending=0</td><td>0002h：Pending=1</td><td>繼續等待，兩端尚未都完成</td></tr>
<tr><td>兩端 Enable 仍為 1，之後再次讀取</td><td>0000h：Pending=0</td><td>0000h：Pending=0</td><td>可開始使用 VC1，仍須符合正常傳送條件</td></tr></tbody></table></div>
<p>Pending 在 VC 協商完成、離開 FC_INIT2 時由硬體清除。這裡要讀取的是兩端同一個 VC 的結果；只看到 Root Port 已清零，就讓 Endpoint 使用 TC7，會漏掉另一端尚未完成的初始化。Status 不是 W1C 事件欄位，軟體不以寫入 1 的方式「完成協商」。</p>
<p>所有預定使用的 VCs 都已啟用後，軟體可選擇設定 Port VC Control 的 All VCs Enabled（bit 4）。它幫助硬體分配緩衝資源；保持 0 時，已啟用的 VCs 仍須正確運作。若已設為 1，Link 還在運作時再改變此 Capability 內的 VC Enable，規格定義為 undefined behavior，不能把它當成一般的即時切換方式。</p>
<p class="source">規格串接：§7.9.1 Virtual Channel Extended Capability，pp.1181–1184，Figure 7-221 Virtual Channel Extended Capability Structure，p.1183；Table 7-202 Port VC Capability Register 1，p.1185；Table 7-207 VC Resource Control Register，pp.1189–1191；Figure 7-229／Table 7-208 VC Resource Status Register，pp.1191–1192；Table 7-204 Port VC Control Register，pp.1186–1187。文件頁與 PDF 頁相同。</p></div></section>
<section id="example"><h2>完成初始化後，VC0 沒有 credit，VC1 還能走嗎？</h2>
<p><strong>【模擬資料】沿用前節已完成初始化的 Non-Flit 配置，以下是假設的傳送時點。</strong>從 Endpoint 向 Root Port 傳送時，TC0 的 Memory Write 映射至 VC0；TC7 的 Memory Write 映射至 VC1。VC0 的 Posted Data Credit 不足，VC1 則有足夠的 Header 與 Data Credit，TC7 也符合其他排序與傳送條件。</p>
<div class="table-wrap"><table><thead><tr><th scope="col">候選封包</th><th scope="col">對應資源</th><th scope="col">目前是否能參與傳送仲裁？</th></tr></thead><tbody><tr><td>TC0 Memory Write</td><td>VC0 的所需 Data Credit 不足</td><td>這筆封包先等待</td></tr><tr><td>TC7 Memory Write</td><td>VC1 的所需 Credit 充足</td><td>可參與仲裁，仍須等仲裁選中</td></tr></tbody></table></div>
<p>Non-Flit Mode 各 VC 的 Flow Control credit pool 獨立，所以 VC0 這筆封包受阻，不會直接扣掉 VC1 的可用 credit。這也不是「VC0 的所有封包都停住」：同一 VC 仍分成不同的 Flow Control 類別，要依候選封包實際需要的資源判斷。這裡先看 VC 之間的隔離，credit 消耗與更新接到 <a href="/DOCS/pcie-course/chapter-17.html">Chapter 17</a> 繼續閱讀。</p>
<p>Flit Mode 若使用 Shared FC，資源分成專用與共享部分，不能把上面的完全獨立池模型原樣搬過去。§2.6 說明共享 credit 的使用條件；一個 VC 能參與仲裁，仍要依當時適用的資源模型判斷。</p><dl class="st-terms" aria-label="本段名詞"><div><dt>FC</dt><dd>Flow Control，流量控制</dd></div></dl>
<p class="source">規格閱讀：§2.6 Ordering and Receive Buffer Flow Control，p.235；§6.3.3.1 的 Implementation Note: VC Control Logic at the Egress Port，p.709。Flow Control 保護相鄰接收端的緩衝，並不代表要求已到達最終 Completer。</p></section>
<section id="arbitration"><h2>兩個 VC 都能傳送時，誰先使用 Link？</h2>
<p>先分清仲裁的對象。若流量經過 Switch，用 Figure 6-8（p.708）從左向右讀：先依地址或其他路由資訊找出 Egress Port，再依該出口的 Map 決定 VC。來自不同 Ingress Ports、但要進入同一個出口 VC 的流量，先由 <strong>Port Arbitration</strong> 決定服務順序；出口內不同 VCs 再由 <strong>VC Arbitration</strong> 競爭共同 Link。兩者都不是單看封包上的 TC 數字就能決定。</p>
<p>再接 Figure 6-9（p.709），先讀 VC ID 與 Relative Priority，再看右側的優先群組分界。規格確實定義 VC ID 由小到大的預設相對優先次序；若採 Strict Priority（嚴格優先），較大的 VC ID 先服務。若一組 VCs 採 RR（Round Robin，輪流服務）或 WRR（Weighted Round Robin，按權重輪流服務），則須讀對應的仲裁能力、選擇與表格，不能只按 ID 排出所有實際傳送次序。</p>
<p>前面的模擬配置指定 Low Priority Extended VC Count=0，依 §6.3.3.2，所有 VCs 都採 Strict Priority。因此，在同一傳送端兩個 VC 都有合格封包可送時，VC1 的相對優先權高於 VC0。這不是 TC7 自帶的頻寬保留；TC7 只是剛好映射到本例的 VC1。</p>
<p>優先權也不能讓缺少 credit 的封包直接傳送。反過來，若高優先流量持續占用 Link，較低優先流量可能一直得不到服務。§6.3.3.2.1 要求使用 Strict Priority 時調節高優先流量，並由系統軟體安排足夠的低優先服務，避免交易逾時。需要頻寬與延遲保證時，還要接到下一節的全路徑契約。</p>
<p class="source">規格閱讀：§6.3.3.1 Traffic Flow and Switch Arbitration Model，Figure 6-8 Switch Arbitration Structure，p.708；§6.3.3.2 VC Arbitration - Arbitration Between VCs，Figure 6-9 VC ID and Priority Order - An Example，pp.709–710；§6.3.3.2.1 Strict Priority Arbitration Model、§6.3.3.2.2 Round Robin Arbitration Model，p.710；Table 7-202，p.1185。</p></section>
<section id="service"><h2>週期資料需要保證，還要建立什麼？</h2>
<p>Isochronous Contract（等時性服務契約）把要求者、完成端與沿路資源的責任連在一起。讀 Figure A-1（p.1521）時，先選一條完整流向：Device A 與 Root Complex 之間，包含向上的 Read／Write Requests 與返回的 Read Completions；Device B 到 Device C 則是另一條 Peer-to-Peer 流向。兩種模型都要核對自己的路徑與服務能力。</p>
<p>接著看 Figure A-2（p.1522）的兩條時間軸。上方是過度配置，分配給等時性要求的資源使其他流量幾乎沒有服務空間；下方是短時間內注入過多要求而造成壅塞。因此契約同時需要資源保留與流量調節。§A.2 再把期間 T、交易數 N、每筆預算負載 Y 與延遲 L 接在一起；只把 TC7 映射到 VC1，還沒有建立這份契約。</p>
<p>本章先建立查閱入口，沒有宣稱已配置完整等時性服務。多個流程共用相同 VC／TC 時，系統還要核對總需求；一般非等時性服務的 TC／VC 分配政策，也不能當成 Base 6.0 對所有平台規定的固定配置。</p>
<p class="source">規格閱讀：§A.1 Introduction，pp.1521–1522；Figure A-1 An Example Showing Endpoint-to-Root-Complex and Peer-to-Peer Communication Models，p.1521；§A.2 Isochronous Contract and Contract Parameters，pp.1522–1523；Figure A-2 Two Basic Bandwidth Resourcing Problems: Over-Subscription and Congestion，p.1522。</p></section>
<section id="sources"><h2>版本與來源</h2><p>本章依 PCI Express Base Specification Revision 6.0（6.0-1.0-PUB）撰寫，文件印刷頁與 PDF 檢視器頁碼相同。配置、讀值與流程圖為作者建立的教學案例，並非實機量測。主要帶讀單一 Link 的額外 VC 啟用；MFVC、完整仲裁表、Shared FC 與完整等時性配置仍須深入。</p><details class="source-note"><summary>完整來源定位與用途</summary><ul>
<li>§2.5 Virtual Channel (VC) Mechanism，pp.229–230；§2.5.1 Virtual Channel Identification (VC ID)，p.232；§2.5.2 TC to VC Mapping，p.233；§2.5.3 VC and TC Rules，pp.234–235。Table 2-43 TC to VC Mapping Example，p.233；Figure 2-88 An Example of TC/VC Configurations，p.234：分類、資源與雙端映射。</li>
<li>§2.6 Ordering and Receive Buffer Flow Control，Figure 2-89 Relationship Between Requester and Ultimate Completer，p.235：逐 Link 流量控制與兩種模式的資源模型。</li>
<li>§7.9.1 Virtual Channel Extended Capability，pp.1181–1184；Figure 7-221 Virtual Channel Extended Capability Structure，p.1183；Table 7-201 Virtual Channel Extended Capability Header，p.1184：結構適用性、ID、Version 與資源位移。</li>
<li>§7.9.1.2 Port VC Capability Register 1 (Offset 04h)，Table 7-202，p.1185：額外資源數與低優先群組；§7.9.1.4 Port VC Control Register (Offset 0Ch)，Table 7-204，pp.1186–1187：All VCs Enabled。</li>
<li>§7.9.1.7 VC Resource Control Register，Figure 7-228，p.1189，Table 7-207，pp.1189–1191：Map、VC ID、Enable；§7.9.1.8 VC Resource Status Register，Figure 7-229，p.1191，Table 7-208，pp.1191–1192：Pending 的有效條件與雙端確認。</li>
<li>§6.3.2 TC/VC Mapping and Example Usage，pp.703–704：重新映射與 TC Filtering；§6.3.3 VC Arbitration，p.705；§6.3.3.1 Traffic Flow and Switch Arbitration Model，pp.706–709，Figure 6-8 Switch Arbitration Structure，p.708：出口的兩層仲裁。</li>
<li>§6.3.3.2 VC Arbitration - Arbitration Between VCs，pp.709–710，Figure 6-9 VC ID and Priority Order - An Example，p.709；§6.3.3.2.1 Strict Priority Arbitration Model、§6.3.3.2.2 Round Robin Arbitration Model，p.710：優先次序、群組、調節與公平性條件。</li>
<li>§A.1 Introduction，pp.1521–1522；§A.2 Isochronous Contract and Contract Parameters，pp.1522–1523；Figure A-1 An Example Showing Endpoint-to-Root-Complex and Peer-to-Peer Communication Models，p.1521；Figure A-2 Two Basic Bandwidth Resourcing Problems: Over-Subscription and Congestion，p.1522：端到端契約的查閱入口。</li></ul></details></section>
</article>
<nav class="bottom-nav" aria-label="課程與語言版本"><a href="/DOCS/pcie-course/index.html">課程總覽</a><a href="/DOCS/pcie-course/chapter-16.html">繁中完整教學</a><a href="/pcie/chapter-16-en/">English</a></nav>
</div>
