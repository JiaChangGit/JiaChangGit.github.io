---
layout: post
title: "PCIe Chapter 26: Multifunction, ARI, SR-IOV, and Shadow Functions"
date: 2026-10-24 00:00:00 +0800
last_modified_at: 2026-10-29 00:00:00 +0800
permalink: /pcie/chapter-26-en/
categories: [PCIe]
tags: [PCIe, Specification]
lang: en
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
<div class="pcie-article spec-teaching" data-spec-series="pcie" lang="en">
<nav class="bottom-nav" aria-label="Course and editions"><a href="/DOCS/pcie-course/index.html">Course overview</a><a href="/DOCS/pcie-course/chapter-26.html">Full Chinese tutorial</a><a href="/pcie/chapter-26-zh-tw/">繁體中文</a></nav>
<article class="lesson">
<p>Several Functions may share one Link while retaining distinct Transaction identities and resources. This chapter follows one SR-IOV (Single Root I/O Virtualization) case from ARI interpretation through RID/BAR allocation, readiness, memory decoding and Reset, then distinguishes Shadow Functions.</p><dl class="st-terms" aria-label="Terms in this passage"><div><dt>ARI</dt><dd>Alternative Routing-ID Interpretation</dd></div><div><dt>RID</dt><dd>Routing ID, the packet routing identity</dd></div><div><dt>BAR</dt><dd>Base Address Register</dd></div></dl><figure class="diagram"><svg viewBox="0 0 900 300" style="min-width:680px" role="img" aria-labelledby="ch26-en-t ch26-en-d"><title id="ch26-en-t">Several Functions share one Endpoint Port</title><desc id="ch26-en-d">Root Port connects through a Switch. One Endpoint Port serves the PF and three VFs. Their Function identities do not create extra physical Links.</desc><g data-walk-target="root"><rect x="20" y="40" width="170" height="65" rx="9" fill="var(--surface-alt)" stroke="var(--line)"/><text x="105.0" y="78" text-anchor="middle" font-size="18">Root Port</text></g><g data-walk-target="dp"><rect x="270" y="40" width="210" height="65" rx="9" fill="var(--surface-alt)" stroke="var(--line)"/><text x="375.0" y="78" text-anchor="middle" font-size="18">Switch</text></g><path d="M190 72 H270 M480 72 H560" stroke="var(--accent)" stroke-width="2"/><text x="230" y="52" text-anchor="middle" font-size="15">Link 1</text><text x="520" y="52" text-anchor="middle" font-size="15">Link 2</text><rect x="560" y="20" width="320" height="245" rx="12" fill="var(--surface-alt)" stroke="var(--line)"/><text x="720" y="50" text-anchor="middle" font-size="18">Endpoint / one Port</text><g data-walk-target="pf"><rect x="580" y="70" width="280" height="48" rx="8" fill="var(--surface-alt)" stroke="var(--line)"/><text x="720" y="101" text-anchor="middle" font-size="17">PF: RID 0300h</text></g><g data-walk-target="vfs"><rect x="580" y="150" width="90" height="70" rx="8" fill="var(--surface-alt)" stroke="var(--line)"/><text x="625" y="177" text-anchor="middle" font-size="16">VF 1</text><text x="625" y="203" text-anchor="middle" font-size="16">0310h</text><rect x="675" y="150" width="90" height="70" rx="8" fill="var(--surface-alt)" stroke="var(--line)"/><text x="720" y="177" text-anchor="middle" font-size="16">VF 2</text><text x="720" y="203" text-anchor="middle" font-size="16">0312h</text><rect x="770" y="150" width="90" height="70" rx="8" fill="var(--surface-alt)" stroke="var(--line)"/><text x="815" y="177" text-anchor="middle" font-size="16">VF 3</text><text x="815" y="203" text-anchor="middle" font-size="16">0314h</text></g><text x="720" y="247" text-anchor="middle" font-size="15">Function boxes share the Port</text><g data-walk-target="scope"><text x="285" y="158" text-anchor="middle" font-size="15">Identify the Switch Downstream Port</text><text x="450" y="291" text-anchor="middle" font-size="16">ARI Forwarding: the Port immediately above this Device</text></g></svg><figcaption>Author-created topology. The PF (Physical Function) manages associated configuration; VFs (Virtual Functions) share the Endpoint Port but retain their identities and resources.</figcaption></figure><dl class="st-terms" aria-label="Terms in this passage"><div><dt>RID</dt><dd>Routing ID, the packet routing identity</dd></div><div><dt>ARI</dt><dd>Alternative Routing-ID Interpretation</dd></div></dl>
<section id="scenario"><h2>Identify the participants and assumptions</h2><p>Use the Port/Link model in <a href="/DOCS/pcie-course/chapter-1.html">Chapter 1</a> and allocation background in <a href="/DOCS/pcie-course/chapter-4.html">Chapter 4</a>. Root Port → Switch → Endpoint has two Links. The single Endpoint Port serves one PF and three VFs to be created. Configuration, Transaction identity and resources belong to individual Functions; speed, width and LTSSM belong to their shared Link.</p><dl class="st-terms" aria-label="Terms in this passage"><div><dt>LTSSM</dt><dd>Link Training and Status State Machine</dd></div></dl><p><strong>Simulated data:</strong> topology, fields and timings are author-created, not hardware measurements. PF RID=0300h is the lowest-numbered PF and is in D0. Software is ARI-aware; sufficient Bus Numbers and upstream resource Windows are available, with no conflicting Function identities. Initially VF Enable=0 and VF MSE=0. This case has no VF Resizable BAR, FRS support, or shorter reported/platform VF Enable Time.</p><dl class="st-terms" aria-label="Terms in this passage"><div><dt>BAR</dt><dd>Base Address Register</dd></div><div><dt>FRS</dt><dd>Function Readiness Status</dd></div></dl><p>Base 6.0 Chapter 9 already defines SR-IOV architecture, configuration and lifecycle. VM assignment policy, IOMMU isolation and internal device scheduling still require platform/device information.</p><dl class="st-terms" aria-label="Terms in this passage"><div><dt>SR-IOV</dt><dd>Single Root I/O Virtualization</dd></div></dl></section>
<section id="ari"><h2>Does 0314h mean Device 2, Function 4, or Function 20?</h2><p>Section 6.13 divides a conventional 16-bit RID (Routing ID) into Bus [15:8], Device [7:3] and Function [2:0]. ARI (Alternative Routing-ID Interpretation) instead interprets the low byte as an 8-bit Function Number without increasing RID width. Thus 0314h conventionally displays as Bus 03h/Device 02h/Function 04h, but means Bus 03h/Function 14h, decimal20, for this ARI Device. ARI does not itself create VFs; creation remains controlled through the associated PF's SR-IOV Control.</p><p>Figure 6-13 identifies the Switch Downstream Port immediately above the Endpoint. Check its Device Capabilities 2.ARI Forwarding Supported [5] and Device Control 2.ARI Forwarding Enable [5]; both are set here. An ARI Endpoint below the Switch does not require enabling every ancestor Port.</p><p>In the Device, find ARI Extended Capability ID=000Eh, Version=1. Table 7-157's Next Function Number links non-VF Functions from Function 0. For VFs that field is undefined: use First VF Offset/VF Stride instead. Shadow Functions do not enter this list either.</p><p>The PF's ARI Capable Hierarchy is a separate hint that the immediately upstream Downstream Port has ARI enabled. Software should match it to that Port's ARI Forwarding Enable; it is set here. It resides in the lowest-numbered PF and affects the Device. Do not change it while any PF has VF Enable set; it does not replace the Port's forwarding control.</p><p class="source-note">Base 6.0 §6.13, Figure 6-13, pp.762–765; §7.8.8, Figures 7-181–7-184, Tables 7-156–7-158, pp.1146–1148; §7.5.3.15, p.990; §7.5.3.16, p.996; §9.3.3.3.5, pp.1457–1458.</p></section>
<section id="setup"><h2>Read the fields that precede VF creation</h2><p>In the PF, locate SR-IOV Extended Capability ID=0010h, Version=1, with base S. Figure 9-10 locates fields with different access widths. Counts and RID offsets below are 16-bit; Page Sizes are 32-bit:</p><div class="table-wrap"><table><thead><tr><th scope="col">Register / field</th><th scope="col">Offset from S</th><th scope="col">Value</th><th scope="col">Meaning</th></tr></thead><tbody><tr data-sriov-field="total"><td>TotalVFs</td><td>0Eh</td><td>0008h</td><td>Maximum 8 VFs</td></tr><tr data-sriov-field="num"><td>NumVFs</td><td>10h</td><td>0003h</td><td>Create 3 VFs</td></tr><tr data-sriov-field="first"><td>First VF Offset</td><td>14h</td><td>0010h</td><td>16-bit RID offset</td></tr><tr data-sriov-field="stride"><td>VF Stride</td><td>16h</td><td>0002h</td><td>16-bit RID stride</td></tr><tr data-sriov-field="supported"><td>Supported Page Sizes</td><td>1Ch</td><td>00000553h</td><td>4/8/64/256 KiB; 1/4 MiB</td></tr><tr data-sriov-field="system"><td>System Page Size</td><td>20h</td><td>00000010h</td><td>Bit 4 → 64 KiB</td></tr></tbody></table></div><p>TotalVFs is capacity; NumVFs is the selected count. NumVFs initially has an undefined value, so software explicitly sets it. Here 3≤8. Write NumVFs only while VF Enable is clear; changing it while enabled or selecting more than TotalVFs has undefined results.</p><p>System Page Size=00000010h selects bit4, hence 2<sup>4+12</sup>=65,536 bytes=64 KiB, not 16 bytes. Select exactly one supported bit: zero, multiple bits or an unsupported bit have undefined results. The reported bitmap includes the six required page sizes. Write System Page Size only while VF Enable is clear; changing it leaves all VF BARn contents indeterminate, requiring fresh sizing/allocation.</p><p>NumVFs and ARI Capable Hierarchy can affect First VF Offset/VF Stride. Configure those inputs before reading the offsets rather than reusing a snapshot from another count.</p><p class="source-note">Base 6.0 §§9.2.1.1–9.2.1.2, pp.1445–1447; §9.3.3.1, Figures 9-10/9-11, Table 9-2, pp.1451–1452; §9.3.3.7, p.1459; §§9.3.3.12–9.3.3.14, pp.1462–1463.</p></section>
<section id="rid"><h2>Find the third VF's identity</h2><p>Table 9-1 defines VF N RID=PF RID+First VF Offset+(N−1)×VF Stride, using unsigned 16-bit arithmetic with carries dropped. With NumVFs=3, PF 0300h, Offset 0010h and Stride0002h:</p><div class="table-wrap"><table><thead><tr><th scope="col">VF</th><th scope="col">RID calculation</th><th scope="col">RID</th><th scope="col">ARI Bus / Function</th><th scope="col">Legacy Bus / Device / Function</th></tr></thead><tbody><tr data-vf-rid="1"><td>1</td><td>0300h + 0010h + 0×0002h</td><td>0310h</td><td>03h / 10h</td><td>03h / 02h / 00h</td></tr><tr data-vf-rid="2"><td>2</td><td>0300h + 0010h + 1×0002h</td><td>0312h</td><td>03h / 12h</td><td>03h / 02h / 02h</td></tr><tr data-vf-rid="3"><td>3</td><td>0300h + 0010h + 2×0002h</td><td>0314h</td><td>03h / 14h</td><td>03h / 02h / 04h</td></tr></tbody></table></div><p>VF numbering here starts at 1 as in Table 9-1; reconcile a tool's zero-based VF index first. A stride of2 increments RID, not a byte address. The legacy column is another display of the same bits, while this case uses ARI Function Numbers.</p><p>These VFs remain on Bus 03h. Other configurations may need additional Bus Numbers reserved before enabling. Every PF/VF RID must be unique; a VF must not be on a numerically lower Bus than its PF. Modulo arithmetic does not authorize a conflicting or lower-Bus assignment.</p><p class="source-note">Base 6.0 §9.2.1.2, Table 9-1, pp.1446–1447; §§9.3.3.9–9.3.3.10, p.1461.</p></section>
<section id="bar"><h2>Find VF 3's memory range independently</h2><p>Figure 9-9 separates the PF's ordinary BAR from the VF BAR in its SR-IOV Capability. A VF's own Type0 Header BARs are hardwired zero. Configure the group through the PF's VF BARs, not by programming a separate Header BAR in each VF.</p><p>After selecting the 64 KiB System Page Size, sizing the 64-bit Prefetchable VF BAR0/1 pair returns low DW=FFFF000Ch and high DW=FFFFFFFFh. Remove the low four attribute bits to obtain address mask FFFFFFFFFFFF0000h. Invert across 64 bits and add 1: each VF aperture is 10000h=64 KiB.</p><dl class="st-terms" aria-label="Terms in this passage"><div><dt>DW</dt><dd>Double Word, a four-byte unit</dd></div></dl><p>Allocate first-VF base 90000000h, represented by VF BAR0=9000000Ch and VF BAR1=00000000h. Section 9.2.1.1.1 derives later starts as base+(VF number−1)×per-VF aperture:</p><div class="table-wrap"><table><thead><tr><th scope="col">VF</th><th scope="col">Start</th><th scope="col">End, inclusive</th><th scope="col">Per-VF aperture</th></tr></thead><tbody><tr data-vf-bar="1"><td>1</td><td>90000000h</td><td>9000FFFFh</td><td>10000h / 64 KiB</td></tr><tr data-vf-bar="2"><td>2</td><td>90010000h</td><td>9001FFFFh</td><td>10000h / 64 KiB</td></tr><tr data-vf-bar="3"><td>3</td><td>90020000h</td><td>9002FFFFh</td><td>10000h / 64 KiB</td></tr></tbody></table></div><p>VF 3 starts at 90020000h and occupies 90020000h–9002FFFFh. Three VFs map 30000h=192 KiB using NumVFs=3, not maximum TotalVFs=8. Software may reserve extra space as a separate future-allocation policy. Upstream Windows must cover the mapped ranges, and each aperture's size/alignment must satisfy System Page Size.</p><p>If implemented, VF Resizable BAR ID=0024h, Version=1 resides in the PF, never in a VF. It is independent of the PF's ordinary Resizable BAR. Clear VF MSE before changing VF BAR Size, select a supported size, reprogram the now-undefined VF BAR, then enable decoding as needed. Hardware reflects the greater requirement of System Page Size and VF BAR Size. This optional mechanism is not used in the numeric case.</p><p class="source-note">Base 6.0 §9.2.1.1.1, Figure 9-9, pp.1445–1446; §9.3.3.14, pp.1462–1463; §7.5.1.2.1, Figures 7-10/7-11, Table 7-9, pp.928–930; §7.8.7, Figures 7-178–7-180, Tables 7-154/7-155, pp.1142–1145.</p></section>
<section id="enable"><h2>VF Enable does not permit immediate BAR access</h2><p>Separate initialization waiting, Configuration readiness and Memory decoding. Assume unlisted Control bits are zero and keep ARI Capable Hierarchy [4] set: 0010h is disabled, 0011h has VF Enable=1/VF MSE=0, and 0019h additionally sets VF MSE [3]. In the diagram, RRS (Request Retry Status) follows the retry path; SC (Successful Completion) proceeds to the next configuration step.</p><figure class="diagram" id="vf-enable-figure"><svg viewBox="0 0 920 460" style="min-width:720px" role="img" aria-labelledby="ch26-enable-en-t ch26-enable-en-d"><title id="ch26-enable-en-t">From disabled VFs to a ready Memory Request</title><desc id="ch26-enable-en-d">Configure with VFs disabled, allocate identities and BARs, enable VFs, wait, obtain Successful Configuration Completion, then enable memory decoding. RRS loops only the Configuration retry.</desc><rect x="20" y="30" width="260" height="90" rx="9" fill="var(--surface-alt)" stroke="var(--line)"/><text x="150" y="64" text-anchor="middle" font-size="16">VF Enable=0; VF MSE=0</text><text x="150" y="94" text-anchor="middle" font-size="16">NumVFs / Page / ARI</text><rect x="330" y="30" width="260" height="90" rx="9" fill="var(--surface-alt)" stroke="var(--line)"/><text x="460" y="64" text-anchor="middle" font-size="16">RID + VF BAR allocation</text><text x="460" y="94" text-anchor="middle" font-size="16">Bus / address ranges</text><rect x="640" y="30" width="260" height="90" rx="9" fill="var(--surface-alt)" stroke="var(--line)"/><text x="770" y="64" text-anchor="middle" font-size="16">VF Enable=1; VF MSE=0</text><text x="770" y="94" text-anchor="middle" font-size="16">Control = 0011h</text><rect x="640" y="180" width="260" height="90" rx="9" fill="var(--surface-alt)" stroke="var(--line)"/><text x="770" y="214" text-anchor="middle" font-size="16">First Configuration access</text><text x="770" y="244" text-anchor="middle" font-size="16">Wait ≥100 ms in this case</text><rect x="640" y="325" width="260" height="90" rx="9" fill="var(--surface-alt)" stroke="var(--line)"/><text x="770" y="359" text-anchor="middle" font-size="16">Configuration response?</text><text x="770" y="389" text-anchor="middle" font-size="16">RRS: retry later / SC: continue</text><rect x="330" y="325" width="260" height="90" rx="9" fill="var(--surface-alt)" stroke="var(--line)"/><text x="460" y="359" text-anchor="middle" font-size="16">VF MSE=1</text><text x="460" y="389" text-anchor="middle" font-size="16">Control = 0019h</text><rect x="20" y="325" width="260" height="90" rx="9" fill="var(--surface-alt)" stroke="var(--line)"/><text x="150" y="359" text-anchor="middle" font-size="16">Memory Request to VF 3</text><text x="150" y="389" text-anchor="middle" font-size="16">Address = 90020010h</text><path d="M280 75 L330 75" stroke="var(--accent)" stroke-width="2"/><polygon points="330,75 320,70 320,80" fill="var(--accent)"/><path d="M590 75 L640 75" stroke="var(--accent)" stroke-width="2"/><polygon points="640,75 630,70 630,80" fill="var(--accent)"/><path d="M770 120 L770 180" stroke="var(--accent)" stroke-width="2"/><polygon points="770,180 765,170 775,170" fill="var(--accent)"/><path d="M770 270 L770 325" stroke="var(--accent)" stroke-width="2"/><polygon points="770,325 765,315 775,315" fill="var(--accent)"/><path d="M640 370 L590 370" stroke="var(--accent)" stroke-width="2"/><polygon points="590,370 600,365 600,375" fill="var(--accent)"/><path d="M330 370 L280 370" stroke="var(--accent)" stroke-width="2"/><polygon points="280,370 290,365 290,375" fill="var(--accent)"/><path d="M900 370 H912 V298 H770 V325" stroke="var(--accent)" stroke-width="2" fill="none"/><polygon points="770,325 765,315 775,315" fill="var(--accent)"/><text x="615" y="357" text-anchor="middle" font-size="15">SC</text><text x="460" y="447" text-anchor="middle" font-size="16">The retry does not restart the 1 s interval from VF Enable.</text></svg><figcaption>Author-created normal path, with no FRS or shorter reported/platform readiness time. Function-specific initialization is assumed complete before the final access.</figcaption></figure><dl class="st-terms" aria-label="Terms in this passage"><div><dt>FRS</dt><dd>Function Readiness Status</dd></div></dl><div class="table-wrap"><table><thead><tr><th scope="col">Since VF Enable</th><th scope="col">SR-IOV Control</th><th scope="col">Configuration Request</th><th scope="col">Memory Request</th></tr></thead><tbody><tr data-vf-stage="create"><td>0 ms</td><td>0011h</td><td>No</td><td>No</td></tr><tr data-vf-stage="early"><td>50 ms</td><td>0011h</td><td>No</td><td>No</td></tr><tr data-vf-stage="rrs"><td>120 ms</td><td>0011h</td><td>Yes / RRS</td><td>No</td></tr><tr data-vf-stage="ready"><td>180 ms</td><td>0011h</td><td>Yes / SC</td><td>No</td></tr><tr data-vf-stage="memory"><td>181 ms</td><td>0019h</td><td>Yes</td><td>Yes, readiness established</td></tr></tbody></table></div><p>After enabling, Requests to the VFs must wait until at least 100 ms, a PF FRS (Function Readiness Status) Message with reason VF Enabled, or the applicable reported/platform VF Enable Time. The case has no early alternatives, so no Configuration Request is sent at 50 ms.</p><p>At 120 ms the VF returns Configuration RRS (Request Retry Status). Such retry status is permitted within the 1.0 s interval after VF Enable, and the RC/software must allow at least 1.0 s before declaring a VF broken for not returning Successful Completion to a valid Configuration Request. Each RRS does not restart that interval.</p><p>At 180 ms SC (Successful Completion) establishes one Memory-readiness condition. VF MSE remains clear, so Memory access is still disabled. At 181 ms Control=0019h enables decoding; with Function-specific initialization also complete, the example accesses VF 3 at 90020010h. Other specified FRS,1.0 s or applicable reported/platform VF Enable Time paths can establish Memory readiness. Simply waiting100 ms is not equivalent to those conditions.</p><p>After a VF has successfully responded to a Request, it must not return Configuration RRS without an intervening disable or other valid Reset. Clearing VF Enable destroys VFs; no field in the PF's SR-IOV Capability may then be accessed until at least 1.0 s has elapsed or a PF FRS Message with reason VF Disabled is received. Do not immediately poll Control or rewrite NumVFs.</p><p class="source-note">Base 6.0 §9.3.3.3, Figure 9-13/Table 9-4, pp.1454–1455; §9.3.3.3.1, pp.1455–1457; §9.3.3.3.4, p.1457.</p></section>
<section id="vf-config"><h2>FFFFh Vendor ID and clear MSE have VF-specific meanings</h2><p>Unlike ordinary Function probing, §§7.5.1.1.1–7.5.1.1.2 require a VF's raw Vendor ID and Device ID to return FFFFh. Virtualization software should present its PF's Vendor ID and the PF's VF Device ID field respectively. At the 180 ms read, first inspect the SC Completion, then interpret FFFFh using the VF-specific rule rather than an ordinary absence shortcut.</p><p>A VF's Command.Memory Space Enable is ROZ (Read Only Zero). The PF's VF MSE controls Memory decoding for the associated Active VFs. I/O Space Enable is also hardwired zero; VFs do not support I/O Space. A VF's own Bus Master Enable instead controls its ability to initiate Memory Requests. That direction differs from host access to VF resources; PF BME does not represent every VF.</p><p>Once their individual Bus Master Enable and device conditions are satisfied, two VFs may issue Memory Reads with Tag 05h. Match returned Completions using Requester IDs0310h and 0312h as well as Tag; equal Tags do not make one Transaction. A healthy shared Link does not establish each Function's resource, BME, Transaction or device-initialization state.</p><p>For interrupt details return to <a href="/DOCS/pcie-course/chapter-7.html">Chapter 7</a>. With allocated resources VFs may use MSI, MSI-X or both, but must not implement INTx. Internal allocation, scheduling and VM assignment remain platform/device policy.</p><dl class="st-terms" aria-label="Terms in this passage"><div><dt>MSI</dt><dd>Message Signaled Interrupt</dd></div><div><dt>MSI-X</dt><dd>Message Signaled Interrupts Extension</dd></div></dl><p class="source-note">Base 6.0 §§7.5.1.1.1–7.5.1.1.3, Table 7-4, pp.917–918; §7.5.1.2.1, p.928; §9.2.1.4, p.1449; PF/VF scope and identities, pp.1440–1447.</p></section>
<section id="reset"><h2>Distinguish VF Reset, PF Reset and recreation</h2><div class="table-wrap"><table><thead><tr><th scope="col">Action</th><th scope="col">VF existence</th><th scope="col">PF VF BAR / VF MSE and state</th></tr></thead><tbody><tr><td>FLR to one VF</td><td>Retained in Configuration and Bus address space</td><td>Resets that VF; PF VF BARs, VF MSE and VF Resizable BAR values unaffected</td></tr><tr><td>FLR to PF</td><td>Associated VFs cease to exist</td><td>Resets PF and SR-IOV Capability, including VF Enable</td></tr><tr><td>VF Enable:1 → 0 → 1</td><td>Destroyed, then a new set created</td><td>No VF state survives disable, including sticky bits; readiness rules apply again</td></tr></tbody></table><dl class="st-terms" aria-label="Terms in this passage"><div><dt>FLR</dt><dd>Function Level Reset</dd></div></dl></div><p>New VFs enter D0uninitialized when the PF is in D0; creating them while the PF is in a lower power state has undefined behavior. Conventional Reset also clears VF Enable and removes VFs. The shared Link remaining in L0 does not describe these Function lifecycle changes.</p><p class="source-note">Base 6.0 §§9.2.2–9.2.2.3, p.1449; §9.2.3, p.1450; §9.3.3.3.1, p.1456.</p></section>
<section id="shadow"><h2>Why can a Shadow identity issue Requests without independent Configuration?</h2><p>Shadow Functions borrow Requester ID/Tag resources of otherwise unimplemented Functions to extend a Requester's Outstanding Request capacity. Characteristics come from the associated Function; this does not create another assignable VF. Locate ID=002Dh, Version=1, then use Figure 7-365 and Tables 7-320–7-322.</p><p><strong>Continuing the simulated case:</strong> assume PF 0300h implements one Shadow Function and 0320h is otherwise unused. Number of Shadow Functions=0 is N−1 encoded, hence one Instance. The first entry atH+0Ch contains Shadow Function Number=0020h, a16-bit BDF offset. Add 0300h+0020h=0320h; it is not an absolute Function Number replacement.</p><dl class="st-terms" aria-label="Terms in this passage"><div><dt>BDF</dt><dd>Bus/Device/Function</dd></div></dl><p>Assume translation/access-control resources have been prepared, Phantom Functions Enabled=0, and no Outstanding Non-Posted Requests before enabling Shadow Functions. Changing its Enable while such Requests are outstanding, or enabling it together with Phantom Functions, has undefined behavior.</p><p>Requester ID 0320h may now issue Memory Read. Ordinary Posted Requests are also permitted, but MSI/MSI-X Requests must not use Shadow Transaction ID resources. Configuration access to 0320h, absent errors with other behavior, must return UR rather than independent Configuration Space. This differs from a created VF returning SC with FFFFh ID fields.</p><dl class="st-terms" aria-label="Terms in this passage"><div><dt>MSI</dt><dd>Message Signaled Interrupt</dd></div><div><dt>MSI-X</dt><dd>Message Signaled Interrupts Extension</dd></div></dl><p>A Shadow Function Number greater than 7 requires ARI; without ARI the Shadow must remain in the same Device. Software must update translation resources before Requests, otherwise behavior is undefined. Relate the identity back to its PF/Capability while still considering its separate RID throughout the path.</p><p class="source-note">Base 6.0 §7.9.25 and §§7.9.25.1–7.9.25.4, pp.1299–1303; Figures 7-365–7-369, Tables 7-319–7-322. Use the field definitions for first-entry offset and N−1 count.</p></section>
<section id="sources"><h2>Edition, source route and platform boundaries</h2><p>PCI Express Base Specification Revision 6.0 (6.0-1.0-PUB) supplies the rules; printed and PDF-viewer pages match. All topology, fields, RID/BAR values and timings are author-created. No hardware was configured. No external website supplies technical claims.</p><details class="source-note"><summary>Sources used by question</summary><ul><li>Scope: Chapter 9 examples, Figures 9-6–9-8, pp.1440–1444; §9.2.1 <em>SR-IOV Resource Discovery</em>, §9.2.1.1 <em>Configuring SR-IOV Capabilities</em>, §9.2.1.1.1 <em>Configuring the VF BAR Mechanisms</em>, §9.2.1.2 <em>VF Discovery</em>, pp.1445–1447; Figure 9-9 <em>BAR Space Example for Single BAR Device</em>, p.1446; Table 9-1 <em>VF Routing ID Algorithm</em>, p.1447.</li><li>Structure/control: §9.3.3 <em>SR-IOV Extended Capability</em>, pp.1450–1463; Figures 9-10/9-11, Table 9-2, pp.1451–1452; Figure 9-13/Table 9-4 <em>SR-IOV Control Register</em>, pp.1454–1455; §§9.3.3.3.1,9.3.3.3.4,9.3.3.3.5, pp.1455–1458; §§9.3.3.6–9.3.3.7, p.1459; §§9.3.3.9–9.3.3.14, pp.1461–1463.</li><li>ARI: §6.13 <em>Alternative Routing-ID Interpretation (ARI)</em>, pp.762–765; Figure 6-13 <em>Example System Topology with ARI Devices</em>, p.764; §7.8.8 <em>ARI Extended Capability</em>, Figures 7-181–7-184, Tables 7-156–7-158, pp.1146–1148; §7.5.3.15 <em>Device Capabilities 2 Register</em>, p.990; §7.5.3.16 <em>Device Control 2 Register</em>, p.996.</li><li>VF Configuration: §§7.5.1.1.1–7.5.1.1.3, pp.917–918; Figure 7-5/Table 7-4 <em>Command Register</em>, p.918; §7.5.1.2.1 <em>Base Address Registers (Offset 10h - 24h)</em>, pp.928–930; interrupts §9.2.1.4, p.1449.</li><li>Reset/recreation: §§9.2.2–9.2.2.3 <em>SR-IOV Reset Mechanisms</em>, p.1449; §9.2.3 <em>IOV Re-initialization and Reallocation</em>, p.1450.</li><li>Resizable VF BAR: §7.8.7 <em>VF Resizable BAR Extended Capability</em>, Figures 7-178–7-180, Tables 7-154/7-155, pp.1142–1145. This capability is absent from the numeric example.</li><li>Shadow: §7.9.25 <em>Shadow Functions Extended Capability</em> and §§7.9.25.1–7.9.25.4, pp.1299–1303; Figure 7-365 <em>Shadow Functions Extended Capability Structure</em>, Figure 7-366/Table 7-319 <em>Shadow Functions Extended Capability Header</em>, p.1301; Figure 7-367/Table 7-320 <em>Shadow Functions Capability Register</em>, Figure 7-368/Table 7-321 <em>Shadow Functions Control Register</em>, pp.1302–1303; Figure 7-369/Table 7-322 <em>Shadow Functions Instance Register Entry</em>, p.1303.</li><li>External boundaries: VM assignment, IOMMU isolation, software-presented VF Configuration, device initialization and scheduling require actual platform/device documents. VF/Shadow identity alone does not establish correctly configured isolation.</li></ul></details></section>
</article>
<nav class="bottom-nav" aria-label="Course and editions"><a href="/DOCS/pcie-course/index.html">Course overview</a><a href="/DOCS/pcie-course/chapter-26.html">Full Chinese tutorial</a><a href="/pcie/chapter-26-zh-tw/">繁體中文</a></nav>
</div>
