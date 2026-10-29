---
layout: post
title: "PCIe Chapter 26：多功能、ARI、SR-IOV 與 Shadow Functions"
date: 2026-10-24 00:00:00 +0800
last_modified_at: 2026-10-29 00:00:00 +0800
permalink: /pcie/chapter-26-zh-tw/
categories: [PCIe]
tags: [PCIe, Specification]
lang: zh-TW
spec_teaching: true
spec_series: pcie
description: "同一組 VF 的 ARI 身分、BAR 範圍與可用時機，如何一起確認？"
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
<nav class="bottom-nav" aria-label="課程與語言版本"><a href="/DOCS/pcie-course/index.html">課程總覽</a><a href="/DOCS/pcie-course/chapter-26.html">繁中完整教學</a><a href="/pcie/chapter-26-en/">English</a></nav>
<article class="lesson">
<p>多個 Function 可以共用一條 Link，但仍有各自的交易身分與資源。本章以一組 PF／VF 案例，串起 ARI 解讀、RID 與 BAR 計算、初始化等待、VF 解碼與 Reset，再比較 Shadow Functions。</p><dl class="st-terms" aria-label="本段名詞"><div><dt>PF</dt><dd>Physical Function，實體功能</dd></div><div><dt>VF</dt><dd>Virtual Function，虛擬功能</dd></div><div><dt>ARI</dt><dd>Alternative Routing-ID Interpretation，替代路由識別碼解讀</dd></div><div><dt>RID</dt><dd>Routing ID，封包使用的路由識別碼</dd></div><div><dt>BAR</dt><dd>Base Address Register，基底位址暫存器</dd></div></dl><figure class="diagram"><svg viewBox="0 0 900 300" style="min-width:680px" role="img" aria-labelledby="ch26-zh-t ch26-zh-d"><title id="ch26-zh-t">多個 Function 共用一個 Endpoint Port</title><desc id="ch26-zh-d">Root Port 經 Switch 連到同一個 Endpoint Port；PF 與三個 VF 共用該 Port，Function 身分不會增加實體 Link。</desc><g data-walk-target="root"><rect x="20" y="40" width="170" height="65" rx="9" fill="var(--surface-alt)" stroke="var(--line)"/><text x="105.0" y="78" text-anchor="middle" font-size="18">Root Port</text></g><g data-walk-target="dp"><rect x="270" y="40" width="210" height="65" rx="9" fill="var(--surface-alt)" stroke="var(--line)"/><text x="375.0" y="78" text-anchor="middle" font-size="18">Switch</text></g><path d="M190 72 H270 M480 72 H560" stroke="var(--accent)" stroke-width="2"/><text x="230" y="52" text-anchor="middle" font-size="15">Link 1</text><text x="520" y="52" text-anchor="middle" font-size="15">Link 2</text><rect x="560" y="20" width="320" height="245" rx="12" fill="var(--surface-alt)" stroke="var(--line)"/><text x="720" y="50" text-anchor="middle" font-size="18">Endpoint / one Port</text><g data-walk-target="pf"><rect x="580" y="70" width="280" height="48" rx="8" fill="var(--surface-alt)" stroke="var(--line)"/><text x="720" y="101" text-anchor="middle" font-size="17">PF: RID 0300h</text></g><g data-walk-target="vfs"><rect x="580" y="150" width="90" height="70" rx="8" fill="var(--surface-alt)" stroke="var(--line)"/><text x="625" y="177" text-anchor="middle" font-size="16">VF 1</text><text x="625" y="203" text-anchor="middle" font-size="16">0310h</text><rect x="675" y="150" width="90" height="70" rx="8" fill="var(--surface-alt)" stroke="var(--line)"/><text x="720" y="177" text-anchor="middle" font-size="16">VF 2</text><text x="720" y="203" text-anchor="middle" font-size="16">0312h</text><rect x="770" y="150" width="90" height="70" rx="8" fill="var(--surface-alt)" stroke="var(--line)"/><text x="815" y="177" text-anchor="middle" font-size="16">VF 3</text><text x="815" y="203" text-anchor="middle" font-size="16">0314h</text></g><text x="720" y="247" text-anchor="middle" font-size="15">Function 方塊共用同一個 Port</text><g data-walk-target="scope"><text x="285" y="158" text-anchor="middle" font-size="15">先定位 Switch Downstream Port</text><text x="450" y="291" text-anchor="middle" font-size="16">ARI Forwarding：查緊鄰裝置上方的 Downstream Port</text></g></svg><figcaption>作者建立的拓撲。PF（Physical Function，實體功能）管理相關配置；VF（Virtual Function，虛擬功能）各有資源與身分，仍共用同一個 Endpoint Port。</figcaption></figure><dl class="st-terms" aria-label="本段名詞"><div><dt>RID</dt><dd>Routing ID，封包使用的路由識別碼</dd></div><div><dt>ARI</dt><dd>Alternative Routing-ID Interpretation，替代路由識別碼解讀</dd></div></dl><section id="scenario"><h2>這章先建立哪一組對象？</h2><p>沿用 <a href="/DOCS/pcie-course/chapter-1.html">Chapter 1 的 Port／Link</a> 與 <a href="/DOCS/pcie-course/chapter-4.html">Chapter 4 的資源配置</a>：Root Port 經 Switch 連到 Endpoint。Endpoint 只有一個 Port，內含一個 PF 與三個將要建立的 VF；每個 Function 的 Configuration、交易身分與資源要分別看，Link Speed、Width 與 LTSSM 則仍屬共用的 Link。</p><dl class="st-terms" aria-label="本段名詞"><div><dt>LTSSM</dt><dd>Link Training and Status State Machine，鏈結訓練與狀態機</dd></div></dl><p><strong>【模擬資料】以下資料為教學用途建立，不代表特定硬體或平台。</strong>假設 PF 處於 D0，RID=0300h，且是本裝置最低編號的 PF。軟體具備 ARI 支援，所需 Bus Number 與上層資源 Window 均可配置，沒有其他 PF／VF 占用本例身分。初始 VF Enable=0、VF MSE=0；本例不實作 VF Resizable BAR、不支援 FRS，也沒有採用較短的回報或平台 VF Enable Time。</p><dl class="st-terms" aria-label="本段名詞"><div><dt>BAR</dt><dd>Base Address Register，基底位址暫存器</dd></div><div><dt>FRS</dt><dd>Function Readiness Status，功能就緒狀態</dd></div></dl><p>這份 Base 6.0 的 Chapter 9 已定義 SR-IOV 架構、配置與生命週期；主要答案直接依本版查閱。虛擬機分配政策、IOMMU 隔離與裝置內部排程仍須平台或裝置資料，不能由 PF／VF 數量推論。</p><dl class="st-terms" aria-label="本段名詞"><div><dt>SR-IOV</dt><dd>Single Root I/O Virtualization，單根I/O虛擬化</dd></div></dl></section>
<section id="ari"><h2>0314h 是 Device 2、Function 4，還是 Function 20？</h2><p>先讀 §6.13：傳統 16-bit RID（Routing ID，路由識別碼）分成 Bus [15:8]、Device [7:3]、Function [2:0]；ARI 把低 8 bits 合併成 Function Number，RID 的總長度不變。因此同一個 0314h，可被傳統顯示方式拆成 Bus=03h、Device=02h、Function=04h，在 ARI 裝置中則表示 Bus=03h、Function=14h，也就是十進位 20。顯示成哪種格式，不會創造另一個實體 Device。ARI 本身也不建立 VF；建立 VF 仍須由所屬 PF 的 SR-IOV Control 處理。</p><dl class="st-terms" aria-label="本段名詞"><div><dt>SR-IOV</dt><dd>Single Root I/O Virtualization，單根I/O虛擬化</dd></div></dl><p>接著用 Figure 6-13 <em>Example System Topology with ARI Devices</em> 找到緊鄰 Endpoint 上方的 Switch Downstream Port。查該 Port 的 Device Capabilities 2.ARI Forwarding Supported [5]，再查 Device Control 2.ARI Forwarding Enable [5]。本例這兩個 bit 都為一；Root Port 上方那條通往 Switch 的 Link，不因最下游是 ARI 裝置就必須同樣啟用。</p><p>裝置端另沿 ARI Extended Capability（ID=000Eh、Version=1）讀取能力。Table 7-157 的 Next Function Number 由 Function 0 開始串非 VF Functions；<strong>VF 的這個欄位為 undefined</strong>，須改走 First VF Offset／VF Stride，Shadow Functions 也不加入這條鏈。因此不能把 ARI 鏈列出的 Function 數直接當成 VF 數。</p><p>PF 的 ARI Capable Hierarchy 又是另一個 bit：它提示裝置，緊鄰上方 Port 已啟用 ARI。軟體應讓它與該 Port 的 ARI Forwarding Enable 一致；本例設為一。它在最低編號 PF 控制整個裝置，不能在任一 PF 的 VF Enable 已為一時改變。這個設定不會取代上方 Port 的轉送控制。</p><p class="source-note">Base 6.0 §6.13，pp.762–765；Figure 6-13，p.764；§7.8.8，Figures 7-181–7-184、Tables 7-156–7-158，pp.1146–1148；§7.5.3.15，p.990；§7.5.3.16，p.996；§9.3.3.3.5，pp.1457–1458。</p></section>
<section id="ari-capture"><h2>ARI Function 如何取得發送要求時的 Bus Number？</h2>
<p>前一節已將 <code>0314h</code> 拆成 ARI 的 Bus <code>03h</code> 與 Function Number <code>14h</code>。現在接到 §2.2.6.2：ARI Device 的 Functions 只要求擷取 Type 0 Configuration Write 中的 Bus Number；ARI Requester ID 的低 8 bits 是 Function Number，沒有另外的 Device Number 欄位。</p>
<div class="example"><p><strong>【模擬資料】以下資料為教學用途建立，不代表特定硬體或平台。</strong>假設 ARI Function <code>14h</code> 完成發給自己的 Type 0 Configuration Write，該設定要求帶有 Bus <code>03h</code>；本例也假設該寫入成功，且這筆由 Function 自身發起的要求沒有使用 Shadow Function。它以擷取的 Bus 與自己的 Function Number 組合，得到 Requester ID <code>0314h</code>。</p>
<p>ARI Device 可以選擇每個 Function 各自保存 Bus Number，也可以由整個 Device 共用一份。若採共用方式，所有 Functions 都須更新並使用共同的 Bus Number；不能假設每個 Function 有彼此獨立的 Bus 快照。</p>
<p>假設平台已依 §6.4 協調停止新交易並處理未完成工作，之後重新配置為 Bus <code>04h</code>，Function <code>14h</code> 又完成新的 Type 0 Configuration Write。按適用的擷取方式更新後，本例後續自行發起要求的 Requester ID 會是 <code>0414h</code>。若採逐 Function 保存，其他 Function 的擷取紀錄須各自確認；若採 Device 共用保存，則依共同值處理。</p></div>
<p>此案例使用 Non-Flit Mode，沒有展開 Flit Mode 的 Segment 欄位。初次設定與一般非 ARI Function 的對照見 <a href="/DOCS/pcie-course/chapter-3.html#requester-capture">Chapter 3</a>；Bus／Function 身分更新與 VF 啟用仍是不同步驟。</p>
<p class="source">PCI Express Base 6.0 §2.2.6.2，文件頁／PDF 頁 156–157，尤其是 ARI 相關註腳；§6.13 Alternative Routing-ID Interpretation，pp.760–762；§6.4 Device Synchronization，pp.717–718。</p></section>
<section id="setup"><h2>建立三個 VF 前，要先讀哪些欄位？</h2><p>在 PF 中沿 Extended Capability 鏈找 ID=0010h、Version=1，將起點記為 S。Figure 9-10 <em>SR-IOV Extended Capability</em> 把 Control、數量、RID 與資源欄位放在同一個結構，但讀取寬度不同。以下數量與 offset／stride 為 16-bit，Page Sizes 為 32-bit：</p><div class="table-wrap"><table><thead><tr><th scope="col">Register / field</th><th scope="col">Offset from S</th><th scope="col">模擬值</th><th scope="col">解讀</th></tr></thead><tbody><tr data-sriov-field="total"><td>TotalVFs</td><td>0Eh</td><td>0008h</td><td>此 PF 最多 8 個 VF</td></tr><tr data-sriov-field="num"><td>NumVFs</td><td>10h</td><td>0003h</td><td>這次選擇 3 個 VF</td></tr><tr data-sriov-field="first"><td>First VF Offset</td><td>14h</td><td>0010h</td><td>16-bit RID offset</td></tr><tr data-sriov-field="stride"><td>VF Stride</td><td>16h</td><td>0002h</td><td>16-bit RID stride</td></tr><tr data-sriov-field="supported"><td>Supported Page Sizes</td><td>1Ch</td><td>00000553h</td><td>4/8/64/256 KiB; 1/4 MiB</td></tr><tr data-sriov-field="system"><td>System Page Size</td><td>20h</td><td>00000010h</td><td>Bit 4 → 64 KiB</td></tr></tbody></table></div><p>TotalVFs 是最大數量，NumVFs 才是本次要建立的數量。NumVFs 的初始值為 undefined，軟體須主動設定；本例 3≤8。只有 VF Enable=0 時才能寫 NumVFs，寫入超過 TotalVFs 或在啟用中改數量，結果皆為 undefined。</p><p>System Page Size=00000010h 是選取 bit4，表示 2<sup>4+12</sup>=65,536 bytes＝64 KiB，並不是 16 bytes。它必須只設一個受支援的 bit；零、多個 bit 或未宣告的 bit 都會導致 undefined。本例的 Supported Page Sizes 包含規格要求的六種大小。Page Size 也須在 VF Enable=0 時寫入；改變後所有 VF BARn 內容為 indeterminate，須重新探測與配置。</p><p>NumVFs 與 ARI Capable Hierarchy 都可能影響 First VF Offset／VF Stride，所以先完成這些設定，再讀下面的 RID 資料；不能沿用另一組 NumVFs 時保存的 offset。</p><p class="source-note">Base 6.0 §§9.2.1.1–9.2.1.2，pp.1445–1447；§9.3.3.1，Figures 9-10／9-11、Table 9-2，pp.1451–1452；§9.3.3.7，p.1459；§§9.3.3.12–9.3.3.14，pp.1462–1463。</p></section>
<section id="rid"><h2>第 3 個 VF 的身分怎麼找？</h2><p>現在才用 Table 9-1 <em>VF Routing ID Algorithm</em>：第 N 個 VF 的 RID＝PF RID＋First VF Offset＋(N−1)×VF Stride，採 16-bit 無號運算，捨棄進位。接續已配置的 NumVFs=3、PF RID=0300h、Offset=0010h、Stride=0002h，得到：</p><div class="table-wrap"><table><thead><tr><th scope="col">VF</th><th scope="col">RID 算式</th><th scope="col">RID</th><th scope="col">ARI Bus / Function</th><th scope="col">Legacy Bus / Device / Function</th></tr></thead><tbody><tr data-vf-rid="1"><td>1</td><td>0300h + 0010h + 0×0002h</td><td>0310h</td><td>03h / 10h</td><td>03h / 02h / 00h</td></tr><tr data-vf-rid="2"><td>2</td><td>0300h + 0010h + 1×0002h</td><td>0312h</td><td>03h / 12h</td><td>03h / 02h / 02h</td></tr><tr data-vf-rid="3"><td>3</td><td>0300h + 0010h + 2×0002h</td><td>0314h</td><td>03h / 14h</td><td>03h / 02h / 04h</td></tr></tbody></table></div><p>這裡從 VF 1 開始編號，對應 Table 9-1；若工具用從零開始的 VF index，須先對照編號。Stride=2 表示 RID 每次加二，不表示 BAR 每次加兩個 bytes。表中的傳統拆法只是同一個位元樣式的顯示，本例以 ARI 的 8-bit Function Number 解讀。</p><p>三個 VF 都留在 Bus 03h；其他配置可能跨 Bus，須在啟用前保留足夠 Bus Numbers。所有 PF／VF 的 RID 必須互異，VF 也不得落在比所屬 PF 更小的 Bus Number。公式的 16-bit 回繞規則不代表軟體可以配置到更小的 Bus 或已被其他 Function 占用的身分。</p><p class="source-note">Base 6.0 §9.2.1.2，Table 9-1，pp.1446–1447；§9.3.3.9 <em>First VF Offset (Offset 14h)</em>、§9.3.3.10 <em>VF Stride (Offset 16h)</em>，p.1461。</p></section>
<section id="bar"><h2>已知 RID 後，VF 3 的記憶體位址又怎麼找？</h2><p>改看 Figure 9-9 <em>BAR Space Example for Single BAR Device</em>，將 PF 自己的普通 BAR 與 PF 內 SR-IOV 結構的 VF BAR 分開。VF 自己的 Type 0 Header BAR 全部固定讀零；要替這組 VF 配置資源，須操作 PF 的 VF BAR，不能把位址分別寫進每個 VF 的 Header BAR。</p><p>本例在選好 64 KiB System Page Size 後，對 VF BAR0／VF BAR1 這一組 64-bit、Prefetchable BAR 進行 sizing，讀回低 DW=FFFF000Ch、高 DW=FFFFFFFFh。低 4 bits 描述 BAR 類型，去除後得到 64-bit address mask=FFFFFFFFFFFF0000h；取 64-bit 反相再加一，得到每個 VF 的 aperture（位址視窗大小）=10000h＝64 KiB。</p><dl class="st-terms" aria-label="本段名詞"><div><dt>DW</dt><dd>Double Word，4 bytes的資料單位</dd></div></dl><p>再將第一個 VF 的基址配置為 90000000h，對應 VF BAR0=9000000Ch、VF BAR1=00000000h。後續起點依 §9.2.1.1.1 的公式：VF BAR base＋(VF編號−1)×per-VF aperture。這與前節的 RID 公式使用不同單位：</p><div class="table-wrap"><table><thead><tr><th scope="col">VF</th><th scope="col">起點</th><th scope="col">終點（包含）</th><th scope="col">Per-VF aperture</th></tr></thead><tbody><tr data-vf-bar="1"><td>1</td><td>90000000h</td><td>9000FFFFh</td><td>10000h / 64 KiB</td></tr><tr data-vf-bar="2"><td>2</td><td>90010000h</td><td>9001FFFFh</td><td>10000h / 64 KiB</td></tr><tr data-vf-bar="3"><td>3</td><td>90020000h</td><td>9002FFFFh</td><td>10000h / 64 KiB</td></tr></tbody></table></div><p>因此第 3 個 VF 的起點為 90020000h，完整資源範圍為 90020000h–9002FFFFh。三個 VF 合計 30000h＝192 KiB；這次映射數量採 NumVFs=3，不是直接乘最大 TotalVFs=8。軟體可另外預留更多空間供未來配置，但那是額外的資源政策。上游 Window 須涵蓋這次映射範圍，每個 VF 的大小與對齊也須符合選定的 System Page Size。</p><p>若裝置另有 VF Resizable BAR（ID=0024h、Version=1），它位於 PF，不能出現在 VF；普通 Resizable BAR 與 VF Resizable BAR 可同時存在、各管不同資源。改 VF BAR Size 前須先清 VF MSE，選受支援的大小，改後重新配置已變為 undefined 的 VF BAR，再按需求開啟 VF MSE。VF aperture 會反映 System Page Size 與 VF BAR Size 兩者要求的較大值，不能只改尺寸欄位就沿用舊基址。本例沒有使用這項可選能力。</p><p class="source-note">Base 6.0 §9.2.1.1.1，Figure 9-9，pp.1445–1446；§9.3.3.14，pp.1462–1463；§7.5.1.2.1，Figures 7-10／7-11、Table 7-9，pp.928–930；§7.8.7，Figures 7-178–7-180、Tables 7-154／7-155，pp.1142–1145。</p></section>
<section id="enable"><h2>VF Enable 設為一，就能立刻讀 BAR 嗎？</h2><p>還要分開確認初始化等待、Configuration 就緒與 Memory 解碼。本例在 PF 的 SR-IOV Control [4] 保留 ARI Capable Hierarchy=1，其他未列欄位假設為零：0010h 表示尚未啟用，0011h 表示 VF Enable=1、VF MSE=0，0019h 才同時開啟 VF MSE [3]。圖中的 RRS（Request Retry Status，要求稍後重試）走重試分支；SC（Successful Completion，成功完成狀態）才接到後續設定。</p><figure class="diagram" id="vf-enable-figure"><svg viewBox="0 0 920 460" style="min-width:720px" role="img" aria-labelledby="ch26-enable-zh-t ch26-enable-zh-d"><title id="ch26-enable-zh-t">從 VF 停用到可開始 Memory Request 的案例流程</title><desc id="ch26-enable-zh-d">停用時配置身分與BAR，啟用後等待並確認Configuration成功，才開啟記憶體解碼。RRS只回到稍後重試Configuration的分支。</desc><rect x="20" y="30" width="260" height="90" rx="9" fill="var(--surface-alt)" stroke="var(--line)"/><text x="150" y="64" text-anchor="middle" font-size="16">VF Enable=0; VF MSE=0</text><text x="150" y="94" text-anchor="middle" font-size="16">NumVFs / Page / ARI</text><rect x="330" y="30" width="260" height="90" rx="9" fill="var(--surface-alt)" stroke="var(--line)"/><text x="460" y="64" text-anchor="middle" font-size="16">推算 RID 與 VF BAR 範圍</text><text x="460" y="94" text-anchor="middle" font-size="16">配置 Bus Number 與位址</text><rect x="640" y="30" width="260" height="90" rx="9" fill="var(--surface-alt)" stroke="var(--line)"/><text x="770" y="64" text-anchor="middle" font-size="16">VF Enable=1; VF MSE=0</text><text x="770" y="94" text-anchor="middle" font-size="16">Control = 0011h</text><rect x="640" y="180" width="260" height="90" rx="9" fill="var(--surface-alt)" stroke="var(--line)"/><text x="770" y="214" text-anchor="middle" font-size="16">首次允許查 Configuration</text><text x="770" y="244" text-anchor="middle" font-size="16">本例等待至少 100 ms</text><rect x="640" y="325" width="260" height="90" rx="9" fill="var(--surface-alt)" stroke="var(--line)"/><text x="770" y="359" text-anchor="middle" font-size="16">Configuration 回覆？</text><text x="770" y="389" text-anchor="middle" font-size="16">稍後重試（RRS）／成功（SC）</text><rect x="330" y="325" width="260" height="90" rx="9" fill="var(--surface-alt)" stroke="var(--line)"/><text x="460" y="359" text-anchor="middle" font-size="16">VF MSE=1</text><text x="460" y="389" text-anchor="middle" font-size="16">Control = 0019h</text><rect x="20" y="325" width="260" height="90" rx="9" fill="var(--surface-alt)" stroke="var(--line)"/><text x="150" y="359" text-anchor="middle" font-size="16">Memory Request to VF 3</text><text x="150" y="389" text-anchor="middle" font-size="16">Address = 90020010h</text><path d="M280 75 L330 75" stroke="var(--accent)" stroke-width="2"/><polygon points="330,75 320,70 320,80" fill="var(--accent)"/><path d="M590 75 L640 75" stroke="var(--accent)" stroke-width="2"/><polygon points="640,75 630,70 630,80" fill="var(--accent)"/><path d="M770 120 L770 180" stroke="var(--accent)" stroke-width="2"/><polygon points="770,180 765,170 775,170" fill="var(--accent)"/><path d="M770 270 L770 325" stroke="var(--accent)" stroke-width="2"/><polygon points="770,325 765,315 775,315" fill="var(--accent)"/><path d="M640 370 L590 370" stroke="var(--accent)" stroke-width="2"/><polygon points="590,370 600,365 600,375" fill="var(--accent)"/><path d="M330 370 L280 370" stroke="var(--accent)" stroke-width="2"/><polygon points="280,370 290,365 290,375" fill="var(--accent)"/><path d="M900 370 H912 V298 H770 V325" stroke="var(--accent)" stroke-width="2" fill="none"/><polygon points="770,325 765,315 775,315" fill="var(--accent)"/><text x="615" y="357" text-anchor="middle" font-size="15">SC</text><text x="460" y="447" text-anchor="middle" font-size="16">RRS 重試不會重設從 VF Enable 起算的 1 s 期間。</text></svg><figcaption>作者建立的正常案例；未使用 FRS 或較短的回報／平台等待時間。最後存取前，另假設 Function 專用初始化已完成。</figcaption></figure><dl class="st-terms" aria-label="本段名詞"><div><dt>FRS</dt><dd>Function Readiness Status，功能就緒狀態</dd></div></dl><div class="table-wrap"><table><thead><tr><th scope="col">從 VF Enable 起算</th><th scope="col">SR-IOV Control</th><th scope="col">Configuration Request</th><th scope="col">Memory Request</th></tr></thead><tbody><tr data-vf-stage="create"><td>0 ms</td><td>0011h</td><td>否</td><td>否</td></tr><tr data-vf-stage="early"><td>50 ms</td><td>0011h</td><td>否</td><td>否</td></tr><tr data-vf-stage="rrs"><td>120 ms</td><td>0011h</td><td>可／本次 RRS</td><td>否</td></tr><tr data-vf-stage="ready"><td>180 ms</td><td>0011h</td><td>可／本次 SC</td><td>否</td></tr><tr data-vf-stage="memory"><td>181 ms</td><td>0019h</td><td>可</td><td>可，已確認就緒</td></tr></tbody></table></div><p>VF Enable 從零變一後，系統須先等至少 100 ms，或收到 PF 的 FRS（Function Readiness Status，功能就緒狀態）Message、Reason=VF Enabled，或已達規格允許的 VF Enable Time，才可對 VF 發 Request。本例沒有後兩種提早條件，因此 50 ms 時仍不送 Configuration Request。</p><p>120 ms 的 Configuration Request 回覆 RRS（Request Retry Status，要求稍後重試的狀態）。VF 允許在啟用後的 1.0 s 期限內，以 Configuration RRS 表示尚未準備；Root Complex／軟體也必須至少等 1.0 s，才能將無法對有效 Configuration Request 回 Successful Completion 的 VF 判為故障。這不是每次收到 RRS 就重設一秒計時。</p><p>180 ms 收到 SC（Successful Completion，成功完成狀態）後，本例已符合其中一項 Memory 就緒條件；但 VF MSE 仍為零，所以還不能存取 Memory Space。181 ms 設成 0019h，且 Function 專用初始化已完成，才進行對 VF 3 的 90020010h 存取。規格也允許由相應 FRS、等待 1.0 s 或適用的回報／平台 VF Enable Time 滿足其他 Memory 就緒路徑；<strong>單純等過 100 ms 並不等同這些條件。</strong></p><p>一個 VF 曾成功回覆 Request 後，若沒有再停用或其他合法 Reset 條件，就不能再以 Configuration RRS 回覆 Configuration Request。若清除 VF Enable，則是銷毀 VF；在至少 1.0 s 過去，或收到 PF 的 FRS Reason=VF Disabled 之前，連 PF 內這個 SR-IOV Capability 的任何欄位都不能再存取。不能清除後立刻輪詢 Control 或改 NumVFs。</p><p class="source-note">Base 6.0 §9.3.3.3，Figure 9-13、Table 9-4，pp.1454–1455；§9.3.3.3.1 <em>VF Enable</em>，pp.1455–1457；§9.3.3.3.4 <em>VF MSE (Memory Space Enable)</em>，p.1457。</p></section>
<section id="vf-config"><h2>VF 的 Vendor ID=FFFFh、MSE=0，是否代表沒有裝置？</h2><p>對一般 Function，FFFFh Vendor ID 常用於判斷不存在；對 VF，§7.5.1.1.1／§7.5.1.1.2 卻要求原始 Configuration Vendor ID 與 Device ID 固定回 FFFFh。虛擬化軟體應分別採所屬 PF 的 Vendor ID 與 SR-IOV 結構的 VF Device ID 提供 VF 的身分。本例若在 180 ms 讀 Vendor ID，重點先看這筆 Completion 是否為 SC，再依 VF 欄位規則解讀 FFFFh，不能套用一般裝置的探測捷徑。</p><p>同樣地，VF 的 Command.Memory Space Enable 為 ROZ（Read Only Zero，固定讀零），Memory 解碼由 PF 的 VF MSE 控制整組 Active VFs；VF 的 I/O Space Enable 也固定零，VF 不支援 I/O Space。VF 自己的 Bus Master Enable 則管它能否發起 Memory Request，與讓主機讀取 VF BAR 的方向不同，不能用 PF 的 Bus Master Enable 代表所有 VF。</p><p>各自的 Bus Master Enable 與裝置條件都滿足後，兩個 VF 可以用同一個 Tag=05h 發出 Memory Read。回來的 Completion 須分別以 Requester ID=0310h／0312h 配對，不能因 Tag 一樣就視為同一筆。PF／VF 共用 Link 的速度正常，也無法代替個別 Function 的資源、BME、交易與裝置初始化檢查。</p><p>若需要中斷，再接回 <a href="/DOCS/pcie-course/chapter-7.html">Chapter 7 的 MSI／MSI-X</a>。VF 可在有配置資源時使用 MSI、MSI-X 或兩者，但不得實作 INTx；內部資源分配、排程與虛擬機指派政策另由平台及裝置處理。</p><dl class="st-terms" aria-label="本段名詞"><div><dt>MSI</dt><dd>Message Signaled Interrupt，訊息中斷</dd></div><div><dt>MSI-X</dt><dd>Message Signaled Interrupts Extension，表格式訊息中斷</dd></div></dl><p class="source-note">Base 6.0 §§7.5.1.1.1–7.5.1.1.3，Table 7-4，pp.917–918；§7.5.1.2.1，p.928；§9.2.1.4 <em>Interrupt Resource Allocation</em>，p.1449；PF／VF 路由身分與資源，pp.1440–1447。</p></section>
<section id="reset"><h2>重設 VF、重設 PF 與重新建立 VF，有什麼不同？</h2><div class="table-wrap"><table><thead><tr><th scope="col">動作</th><th scope="col">VF 是否仍存在</th><th scope="col">PF 內 VF BAR／VF MSE 與 VF 狀態</th></tr></thead><tbody><tr><td>對單一 VF 發 FLR</td><td>仍存在於 Configuration 與 Bus 位址空間</td><td>重設該 VF 狀態；PF 內 VF BAR、VF MSE、VF Resizable BAR 值不受這次 VF FLR 影響</td></tr><tr><td>對 PF 發 FLR</td><td>所屬 VFs 不再存在</td><td>PF 與 SR-IOV 結構重設，包含 VF Enable</td></tr><tr><td>VF Enable：1 → 0 → 1</td><td>先銷毀，再建立新的一組</td><td>舊 VF 不得保留任何狀態，包含 Sticky bits；重新建立後依就緒規則處理</td></tr></tbody></table><dl class="st-terms" aria-label="本段名詞"><div><dt>FLR</dt><dd>Function Level Reset，以功能為範圍的重設</dd></div></dl></div><p>PF 處於 D0 時，新建立的 VFs 進入 D0uninitialized；PF 在較低電源狀態時，建立行為為 undefined。Conventional Reset 也會清除 VF Enable，使 VF 不再存在。這些行為與共用 Link 是否一直維持 L0 是不同層次，不能只看 Link Status 判斷 VF 的生命週期。</p><p class="source-note">Base 6.0 §9.2.2 <em>SR-IOV Reset Mechanisms</em>、§§9.2.2.1–9.2.2.3，p.1449；§9.2.3 <em>IOV Re-initialization and Reallocation</em>，p.1450；§9.3.3.3.1，p.1456。</p></section>
<section id="shadow"><h2>Shadow Function 為何會發 Request，卻查不到獨立 Configuration？</h2><p>Shadow Functions（影子功能）借用尚未實作 Function 的 Requester ID 與 Tag 資源，讓原本的 Requester 容納更多 Outstanding Requests。它使用關聯 Function 的特性與設定，並不建立可獨立指派的 VF。先找 ID=002Dh、Version=1，再用 Figure 7-365 定位結構，讀 Tables 7-320–7-322。</p><p><strong>接續模擬案例：</strong>假設 PF 0300h 額外實作一個 Shadow Function，且 0320h 尚未由任何 PF／VF／其他 Function 占用。Number of Shadow Functions 欄位讀零，採 N−1 編碼，表示一筆 Instance；第一筆在 H+0Ch，Shadow Function Number=0020h 是 16-bit BDF offset。用 0300h＋0020h＝0320h 算出新 Requester ID，這個欄位提供相對 offset，不能當成絕對 Function Number。</p><dl class="st-terms" aria-label="本段名詞"><div><dt>BDF</dt><dd>Bus／Device／Function，匯流排、裝置與功能識別</dd></div></dl><p>軟體已處理此身分的位址轉譯與存取控制，且主 Function 的 Phantom Functions Enabled=0、沒有 Outstanding Non-Posted Requests，才在本例開啟 Shadow Functions Enable。該 Control bit 在仍有 Outstanding Non-Posted Requests 時變更，或與 Phantom Functions Enabled 同時開啟，都會導致 undefined。</p><p>開啟後，可看到 Requester ID=0320h 的 Memory Read；一般 Posted Request 也可使用這份身分，但 <strong>MSI／MSI-X Request 不得使用 Shadow Function 的 Transaction ID 資源</strong>。對 0320h 的 Configuration 存取，在沒有其他優先錯誤時必須回 UR，而不是提供另一份獨立 Configuration Space。這與已建立 VF 的 SC／FFFFh 欄位情況不同。</p><p>Shadow Function 的 Number 大於 7 需要 ARI；非 ARI 時必須留在相同 Device。軟體也須預先更新地址轉譯資源，否則在 Request 發出時的行為為 undefined。故障分析時要把 0320h 對回關聯 PF 與這份 Capability，同時保留該 RID 在完整路徑上的檢查，不能只因它沒有可列舉的 Configuration 就忽略其 Request。</p><p class="source-note">Base 6.0 §7.9.25 <em>Shadow Functions Extended Capability</em>，pp.1299–1303；Figures 7-365–7-369、Tables 7-319–7-322。首筆 offset 與 N−1 編碼以 §7.9.25.2／§7.9.25.4 的欄位規則為準。</p></section>
<section id="sources"><h2>版本、閱讀路線與文件邊界</h2><p>本章依 PCI Express Base Specification Revision 6.0（6.0-1.0-PUB），文件印刷頁與 PDF 檢視器頁碼相同。拓撲、讀值、RID、BAR 與時間線均為作者建立，未操作實機。本章沒有以外部網站作技術依據。</p><details class="source-note"><summary>依問題查實際使用的依據</summary><ul><li>角色與資源範圍：Chapter 9 的裝置範例，Figures 9-6–9-8，pp.1440–1444；§9.2.1 <em>SR-IOV Resource Discovery</em>、§9.2.1.1 <em>Configuring SR-IOV Capabilities</em>、§9.2.1.1.1 <em>Configuring the VF BAR Mechanisms</em>、§9.2.1.2 <em>VF Discovery</em>，pp.1445–1447；Figure 9-9 <em>BAR Space Example for Single BAR Device</em>，p.1446；Table 9-1 <em>VF Routing ID Algorithm</em>，p.1447。</li><li>SR-IOV 結構與控制：§9.3.3 <em>SR-IOV Extended Capability</em>，pp.1450–1463；Figures 9-10／9-11、Table 9-2，pp.1451–1452；Figure 9-13／Table 9-4 <em>SR-IOV Control Register</em>，pp.1454–1455；§§9.3.3.3.1、9.3.3.3.4、9.3.3.3.5，pp.1455–1458；§§9.3.3.6–9.3.3.7，p.1459；§§9.3.3.9–9.3.3.14，pp.1461–1463。注意數量、身分、就緒與解碼是不同條件。</li><li>ARI：§6.13 <em>Alternative Routing-ID Interpretation (ARI)</em>，pp.762–765；Figure 6-13 <em>Example System Topology with ARI Devices</em>，p.764；§7.8.8 <em>ARI Extended Capability</em>，Figures 7-181–7-184、Tables 7-156–7-158，pp.1146–1148；§7.5.3.15 <em>Device Capabilities 2 Register</em>，p.990；§7.5.3.16 <em>Device Control 2 Register</em>，p.996。</li><li>VF Configuration：§§7.5.1.1.1–7.5.1.1.3，pp.917–918；Figure 7-5／Table 7-4 <em>Command Register</em>，p.918；§7.5.1.2.1 <em>Base Address Registers (Offset 10h - 24h)</em>，pp.928–930。中斷另查 §9.2.1.4，p.1449。</li><li>Reset 與重建：§9.2.2 <em>SR-IOV Reset Mechanisms</em>、§§9.2.2.1–9.2.2.3，p.1449；§9.2.3 <em>IOV Re-initialization and Reallocation</em>，p.1450。</li><li>可調 VF BAR：§7.8.7 <em>VF Resizable BAR Extended Capability</em>，Figures 7-178–7-180、Tables 7-154／7-155，pp.1142–1145。案例未啟用此能力，僅交代另有尺寸控制時的相依條件。</li><li>Shadow：§7.9.25 <em>Shadow Functions Extended Capability</em>、§§7.9.25.1–7.9.25.4，pp.1299–1303；Figure 7-365 <em>Shadow Functions Extended Capability Structure</em>、Figure 7-366／Table 7-319 <em>Shadow Functions Extended Capability Header</em>，p.1301；Figure 7-367／Table 7-320 <em>Shadow Functions Capability Register</em>、Figure 7-368／Table 7-321 <em>Shadow Functions Control Register</em>，pp.1302–1303；Figure 7-369／Table 7-322 <em>Shadow Functions Instance Register Entry</em>，p.1303。</li><li>平台邊界：虛擬機指派、IOMMU 隔離、軟體呈現的 VF Configuration、裝置專用初始化與排程，還須實際平台或裝置文件。Base 的 VF／Shadow 身分本身不代表隔離政策已正確配置。</li></ul></details></section>
</article>
<nav class="bottom-nav" aria-label="課程與語言版本"><a href="/DOCS/pcie-course/index.html">課程總覽</a><a href="/DOCS/pcie-course/chapter-26.html">繁中完整教學</a><a href="/pcie/chapter-26-en/">English</a></nav>
</div>
