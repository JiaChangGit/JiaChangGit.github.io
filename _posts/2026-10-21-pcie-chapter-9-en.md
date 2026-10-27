---
layout: post
title: "PCIe Chapter 9: Reset Scope and Recovery Conditions"
date: 2026-10-21 00:00:00 +0800
last_modified_at: 2026-10-28 00:00:00 +0800
permalink: /pcie/chapter-9-en/
categories: [PCIe]
tags: [PCIe, Specification]
lang: en
spec_teaching: true
spec_series: pcie
description: "從單一 Function 的 FLR 流程與前後快照，判讀舊 Completion、就緒條件、保留欄位與錯誤紀錄。"
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
<nav class="bottom-nav" aria-label="Course and editions"><a href="/DOCS/pcie-course/index.html">Course overview</a><a href="/DOCS/pcie-course/chapter-9.html">Full Chinese tutorial</a><a href="/pcie/chapter-9-zh-tw/">繁體中文</a></nav>
<article class="lesson">
<aside class="note"><strong>[Simulated data]</strong><p>The topology, values, and times in this chapter are teaching examples, not measurements of a particular device or platform.</p></aside>
<figure class="diagram"><svg viewBox="0 0 900 640" role="img" aria-labelledby="flr-walk-title flr-walk-desc"><title id="flr-walk-title">Reset 03:00.0 while preserving its peer</title><desc id="flr-walk-desc">Time runs downward. Software discovers support, quiesces work, handles old traffic, triggers reset, waits, and restores settings. The peer and shared Link remain unaffected.</desc>
<g><rect x="15" y="20" width="260" height="64" rx="12" fill="var(--blue-soft)" stroke="var(--line)"/><text x="145" y="59" text-anchor="middle">System software</text><path d="M145 84 V610" stroke="var(--line)" stroke-dasharray="5 5"/></g>
<g><rect x="320" y="20" width="260" height="64" rx="12" fill="var(--blue-soft)" stroke="var(--line)"/><text x="450" y="59" text-anchor="middle">Target 03:00.0</text><path d="M450 84 V610" stroke="var(--line)" stroke-dasharray="5 5"/></g>
<g><rect x="625" y="20" width="260" height="64" rx="12" fill="var(--blue-soft)" stroke="var(--line)"/><text x="755" y="59" text-anchor="middle">Peer Function 03:00.1</text><path d="M755 84 V610" stroke="var(--line)" stroke-dasharray="5 5"/><text x="755" y="280" text-anchor="middle">Continues its work</text><text x="755" y="315" text-anchor="middle">Shared Link stays up</text></g>
<g><text x="298" y="123" text-anchor="middle">Discover reset support</text><path d="M145 140 H450 M440 134 L450 140 L440 146" fill="none" stroke="var(--accent)" stroke-width="2.5"/></g>
<g><text x="298" y="195" text-anchor="middle">Quiesce and handle old traffic</text><path d="M145 212 H450 M440 206 L450 212 L440 218" fill="none" stroke="var(--accent)" stroke-width="2.5"/></g>
<g><text x="298" y="269" text-anchor="middle">Write the reset control</text><path d="M145 286 H450 M440 280 L450 286 L440 292" fill="none" stroke="var(--accent)" stroke-width="2.5"/><text x="298" y="321" text-anchor="middle">Complete this config write first</text><path d="M450 338 H145 M155 332 L145 338 L155 344" fill="none" stroke="var(--accent)" stroke-width="2.5"/><rect x="345" y="359" width="210" height="48" rx="10" fill="var(--blue-soft)" stroke="var(--line)"/><text x="450" y="389" text-anchor="middle">Start Function reset</text></g>
<g><rect x="25" y="436" width="540" height="83" rx="10" fill="var(--blue-soft)" stroke="var(--line)"/><text x="295" y="470" text-anchor="middle">Check readiness and old-traffic handling</text><text x="295" y="501" text-anchor="middle">This example handles old traffic before reset</text></g>
<g><text x="298" y="566" text-anchor="middle">Restore settings, then resume work</text><path d="M145 585 H450 M440 579 L450 585 L440 591" fill="none" stroke="var(--accent)" stroke-width="2.5"/></g></svg><figcaption>Author-created sequence based on Base 6.0 §6.6.2. This normal-flow example handles outstanding traffic before reset; the ordinary peer Function and shared Link remain operational.</figcaption></figure>
<p class="lead">Function Level Reset (FLR) resets one Endpoint Function while preserving the shared Link and other ordinary Functions. Software quiesces work, handles outstanding traffic, triggers reset, waits for readiness, and restores the settings needed to resume work.</p>
<p><a href="/DOCS/pcie-course/chapter-9.html">Full Chinese tutorial</a> · <a href="/pcie/chapter-9-zh-tw/">繁體中文</a> · <a href="/DOCS/pcie-course/index.html">Course roadmap</a></p>
<aside class="note"><strong>Version and example</strong><p>Base 6.0. Ordinary Functions 03:00.0 and 03:00.1 share a Link to 02:01.0, without Single Root I/O Virtualization (SR-IOV). Read values and times are authored assumptions; PCI Express Capability is at 0x70.</p></aside>
<section id="walk"><h2>Follow the normal reset sequence</h2><p>Chapters 6–8 established memory access, interrupt notification, and Link operation. Here, keep that Link running while rebuilding the target Function. The reading route follows the software task: Figure 7-24 for support, Figure 7-26 for outstanding traffic, Figure 7-25 for the trigger, then §6.6.2 for waiting and restoration.</p><ol><li>Check Function Level Reset (FLR, the per-Function mechanism) support in Device Capabilities bit 28.</li><li>Coordinate other accessors, stop new work, and handle existing Requests. The example in the implementation note on p.727 clears Command and checks Transactions Pending, which tracks outstanding Non-Posted Requests requiring Completions.</li><li>Write Initiate FLR in Device Control. The Function completes this Configuration Write before starting reset.</li><li>In this example, wait 100 ms, then attempt Configuration access. If subsequent initialization still needs time, Request Retry Status (RRS) tells software to retry later. Satisfy any remaining old-transaction wait before initialization.</li><li>Restore fields by their access rules, rebuild the device interface and notification path, then resume work.</li></ol><p>The following sections explain the field values and exceptions along this route.</p></section><section id="scope"><h2>Preserving another Function requires the right reset scope</h2><div class="table-wrap"><table><caption>Reset mechanisms and scope</caption><thead><tr><th scope="col">Mechanism</th><th scope="col">Meaning and selection limits</th></tr></thead><tbody><tr><td>Cold/Warm Fundamental Reset</td><td>Cold follows power application; Warm does not remove and reapply power, and Base defines no universal trigger. Hardware and platform determine scope, not a single targeted Function.</td></tr><tr><td>Hot Reset</td><td>Propagates Conventional Reset in-band across a Link. Downstream Port Secondary Bus Reset initiates it; a Switch can propagate it downstream.</td></tr><tr><td>FLR</td><td>Resets the targeted ordinary Endpoint Function without affecting the Link or other ordinary Functions.</td></tr></tbody></table><dl class="st-terms" aria-label="Terms in this passage"><div><dt>FLR</dt><dd>Function Level Reset</dd></div></dl></div><p>If 03:00.1 must keep working, first discover FLR support in 03:00.0. Secondary Bus Reset on 02:01.0 affects both; operating above the Switch can broaden scope. PERST# board timing needs the relevant platform/form-factor specification. Physical Function (PF) FLR clears Virtual Function (VF) Enable, making the associated VFs cease to exist; ordinary-Function isolation must not be generalized to that relationship.</p><details class="source-note"><summary>Scope sources</summary><p>§6.6.1–§6.6.2 (pp.721–727), §4.2.5.9 (p.441); PF/VF: Table 7-21 (p.962).</p></details></section>
<section id="locate"><h2>Discover support, handle pending traffic, then trigger FLR</h2><div class="table-wrap"><table><caption>Authored FLR configuration reads</caption><thead><tr><th scope="col">Offset/width</th><th scope="col">Value</th><th scope="col">Interpretation</th></tr></thead><tbody><tr><td>0x74/32 bits</td><td>0x10008000</td><td>Device Capabilities bit 28=1: FLR supported.</td></tr><tr><td>0x7A/16 bits</td><td>0x0020</td><td>Device Status bit 5=1: outstanding Non-Posted Requests.</td></tr><tr><td>0x78/16 bits</td><td>0x2810</td><td>Existing Device Control settings.</td></tr><tr><td>0x04/16 bits</td><td>0x0006</td><td>Command Memory Space Enable (MSE, memory decoding) and Bus Master Enable (BME, request issuance) are enabled.</td></tr></tbody></table></div><p>Read Figure 7-24/Table 7-20, Figure 7-26/Table 7-22, then Figure 7-25/Table 7-21. After quiescing and required waits, a 16-bit write of <code>0x2810 | 0x8000 = 0xA810</code> triggers FLR without writing adjacent read/write-one-to-clear (RW1C) Status. Initiate FLR always reads zero. That bit means something else in a PCIe-to-PCI/PCI-X Bridge, so Function type is a prerequisite.</p><details class="source-note"><summary>Field locations</summary><p>Figures 7-24–7-26, Tables 7-20–7-22 (pp.955, 958–959, 962, 965–966).</p></details></section>
<section id="pending"><h2>Stopping new Requests does not remove old Completions</h2><p>Bus Master Enable (BME)=0 does not recall Requests already sent. Transactions Pending tracks this Function's Non-Posted Requests, which may complete or terminate through timeout. It does not cover all Posted Writes, CPU accesses, or external work, and FLR completion itself must clear it.</p><p>In the authored scenario, FLR occurs before an old Memory Read (MRd) with transaction Tag=0x13 returns. Immediate Tag reuse could misassociate a late Completion with a new transaction. Software must coordinate other accessors, stop device work and Direct Memory Access (DMA) and interrupt activity, then handle outstanding transactions. The p.727 Implementation Note offers an algorithm that clears Command and polls Pending or waits sufficiently before FLR; it does not replace device-specific quiescence.</p><details class="source-note"><summary>Pending and stale Completion sources</summary><p>Table 7-22 (p.966); §6.6.2 (pp.725–727).</p></details></section>
<section id="wait"><h2>FLR completion, readiness, and old-transaction waits are separate</h2><p>The initiating Configuration Write must receive its Completion before FLR starts. The Function must complete FLR within 100 ms, but subsequent device-specific initialization can take longer. If it still needs initialization after that limit, it must return Request Retry Status (RRS) for Configuration Requests. After returning a non-RRS Completion, it cannot return RRS again until another reset.</p><p>If Transactions Pending=1 at initiation, software must allow old Completions to arrive or reach reasonable certainty that they will not arrive before initialization. Using the pre-FLR Completion Timeout is recommended. If timeout was disabled, the delay is system dependent but at least 100 ms. Function Readiness Status (FRS) Configuration-Ready can permit earlier Configuration access without proving all prior Requests completed. Requests during FLR may be silently discarded; arbitrary memory-mapped I/O (MMIO) polling is not a standard completion indication.</p><dl class="st-terms" aria-label="Terms in this passage"><div><dt>MMIO</dt><dd>Memory-Mapped I/O, mapped device-register access</dd></div></dl><p>Conventional Reset uses different timing origins. Without Device Readiness Status (DRS) or another applicable early-readiness exception, a Downstream Port supporting above 5 GT/s requires at least 100 ms after Link training completes. Authored example: reset ends at t=0 ms, training finishes at t=40 ms, and the first Configuration Request is no earlier than t=140 ms. The corresponding branch for a Port supporting only up to 5 GT/s counts from reset exit. Without Readiness Notifications, at least 1 s after Conventional Reset exit must be allowed before declaring failure from missing Successful Completion; this is distinct from first-access timing.</p><details class="source-note"><summary>Timing sources</summary><p>FLR: §6.6.2 (pp.725–727); Conventional Reset, Immediate Readiness, DRS, and reported-time exceptions: §6.6.1 (pp.722–723).</p></details></section>
<section id="restore"><h2>Interpret retained fields before restoring operation</h2>
<p>Read the FLR rules and exceptions in §6.6.2, then interpret field attributes using Table 7-2. Some request-enabling controls are cleared, while particular settings and error records are preserved. Check each field before deciding what software needs to restore.</p>
<h3 id="retained-status">Use before-and-after snapshots to explain a retained error</h3>
<div class="example"><p><strong>[Simulated data] These teaching snapshots do not represent a particular device or platform.</strong>The ordinary Function is 03:00.0, with PCI Express Capability at 0x70. Assume Advanced Error Reporting (AER) has been located at 0x100, version 2, using Non-Flit Mode (individual-packet delivery). A Completion Timeout was previously recorded. Software clears Command and handles old traffic before taking the first snapshot; it takes the second after FLR completes and Configuration access is ready. No new errors or AER-clearing writes occur between snapshots. Only selected fields are shown.</p>
<p>On narrow screens, scroll the table horizontally to read all columns.</p>
<div class="table-wrap"><table style="min-width: 640px"><caption>Function 03:00.0 before and after FLR</caption><thead><tr><th scope="col">Field and location</th><th scope="col">Before → after</th><th scope="col">Applicable rule</th></tr></thead><tbody>
<tr><th scope="row">Bus Master Enable, Command bit 2, 0x04</th><td>0 → 0</td><td>Software already cleared it while quiescing; FLR also requires this request-enabling control to be cleared. Zero means the corresponding new Requests remain disabled, but does not itself establish FLR completion.</td></tr>
<tr><th scope="row">Max_Payload_Size, Device Control bits 7:5, 0x78</th><td>000b → 000b</td><td>Explicitly preserved across FLR; 000b configures a 128-byte size.</td></tr>
<tr><th scope="row">Completion Timeout Status, Uncorrectable Error Status bit 14, 0x104</th><td>1 → 1</td><td>Table 7-135 specifies sticky write-one-to-clear status (RW1CS). Under Table 7-2, Hot Reset and FLR neither initialize nor modify this bit.</td></tr>
</tbody></table></div></div>
<p>Follow bit 14 in Figure 7-155 into Table 7-135, then read the RW1CS definition in Table 7-2. Default=0 does not remove the preservation rule. Under the example assumptions, the post-FLR 1 is the retained old record. Incomplete event or write history would require checking whether a new error occurred.</p>
<p>After saving the error evidence, a 32-bit write of <code>0x00004000</code> to 0x104 clears only bit 14. Other defined status bits receive zero and are unaffected by that clear operation. With no new error, bit 14 subsequently reads zero; the saved evidence still records the Timeout. See <a href="/DOCS/pcie-course/chapter-12.html#preserve">Chapter 12</a> for snapshots and related AER fields.</p><dl class="st-terms" aria-label="Terms in this passage"><div><dt>AER</dt><dd>Advanced Error Reporting</dd></div></dl>
<p>§6.6.2 contains the complete preservation list, including Max_Payload_Size, Active State Power Management (ASPM) Control, Read Completion Boundary (RCB), hardware-initialized (HwInit), and sticky fields; Flit-capable implementations have additional requirements. Physical and Data Link state machines and Virtual Channel 0 (VC0) remain intact. Cold/Warm Reset and auxiliary-power preservation conditions need their own checks.</p>
<p>Handle read-only (RO), write-one-to-clear (RW1C), sticky write-one-to-clear (RW1CS), trigger controls, and writable settings according to their rules. Rebuild device interfaces, interrupts, and DMA conditions before restarting work. FLR does not clear host buffers for software or define every device's queue reconstruction.</p><dl class="st-terms" aria-label="Terms in this passage"><div><dt>DMA</dt><dd>Direct Memory Access, device access to memory</dd></div></dl>
<details class="source-note"><summary>Preservation and field sources</summary><p>Base 6.0 §6.6.2 <em>Function Level Reset (FLR)</em> (PDF/printed pp.724–726); Table 7-2 <em>Register and Register Bit-Field Types</em> (pp.914–915); Figure 7-5/Table 7-4 <em>Command Register</em> (pp.918–919); Figure 7-25/Table 7-21 <em>Device Control Register</em> (pp.959–960); Figure 7-154/Table 7-134 <em>Advanced Error Reporting Extended Capability Header</em> (p.1112); Figure 7-155/Table 7-135 <em>Uncorrectable Error Status Register</em> (p.1113). PDF viewer and printed page numbers match for these references.</p></details></section>
<section id="questions"><h2>Check the scope</h2><details class="question"><summary>Does a lack of Link retraining mean FLR failed?</summary><p>No. FLR must not affect the Link. Check the Function's reset and recovery conditions.</p></details><details class="question"><summary>Can all DMA buffers be reclaimed when Pending=0 after FLR?</summary><p>No. Old-transaction waits, quiescence, coordination with other accessors, and platform DMA lifetime rules still matter.</p></details></section>
</article>
<nav class="bottom-nav" aria-label="Course and editions"><a href="/DOCS/pcie-course/index.html">Course overview</a><a href="/DOCS/pcie-course/chapter-9.html">Full Chinese tutorial</a><a href="/pcie/chapter-9-zh-tw/">繁體中文</a></nav>
</div>
