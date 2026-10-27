---
layout: post
title: "PCIe Chapter 16: Traffic Classes, Virtual Channels, and Arbitration"
date: 2026-10-24 00:00:00 +0800
last_modified_at: 2026-10-28 00:00:00 +0800
permalink: /pcie/chapter-16-en/
categories: [PCIe]
tags: [PCIe, Specification]
lang: en
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
<div class="pcie-article spec-teaching" data-spec-series="pcie" lang="en">
<nav class="bottom-nav" aria-label="Course and editions"><a href="/DOCS/pcie-course/index.html">Course overview</a><a href="/DOCS/pcie-course/chapter-16.html">Full Chinese tutorial</a><a href="/pcie/chapter-16-zh-tw/">繁體中文</a></nav>
<article class="lesson">
<p>TC (Traffic Class) labels a packet. VC (Virtual Channel) associates traffic with queues, buffers, and flow-control resources. Follow one Link's map through configuration, dual-end enablement, and initialization before considering arbitration and end-to-end service.</p><figure class="diagram"><svg viewBox="0 0 900 420" role="img" aria-labelledby="ch16-en-t ch16-en-d"><title id="ch16-en-t">Traffic classes, maps, and shared Link resources</title><desc id="ch16-en-d">Map traffic classes into virtual channels and follow their separate resources.</desc><g data-walk-target="tc"><rect x="20" y="30" width="320" height="44" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="180.0" y="59" text-anchor="middle" font-size="16">TC: packet traffic class</text></g><g data-walk-target="map"><rect x="485" y="30" width="390" height="44" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="680.0" y="59" text-anchor="middle" font-size="16">Configure matching link-end maps</text></g><g data-walk-target="vc0"><rect x="40" y="190" width="340" height="68" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="210.0" y="219" text-anchor="middle" font-size="16">VC0: fixed mapping for TC0</text><text x="210.0" y="243" text-anchor="middle" font-size="16">May also carry other TCs</text></g><g data-walk-target="vc1"><rect x="500" y="190" width="350" height="68" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="675.0" y="219" text-anchor="middle" font-size="16">VC1: carries TC7 in this example</text><text x="675.0" y="243" text-anchor="middle" font-size="16">Separate resources and flow control</text></g><g data-walk-target="arb"><rect x="255" y="335" width="390" height="44" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="450.0" y="364" text-anchor="middle" font-size="16">Arbitrate among eligible traffic</text></g><g data-walk-target="a"><path d="M340 52 L485 52" stroke="var(--accent)" stroke-width="2" fill="none"/><polygon points="485,52 475.0,57.0 475.0,47.0" fill="var(--accent)"/><text x="412.5" y="42.0" text-anchor="middle" font-size="16">Class</text></g><g data-walk-target="b"><path d="M600 98 L210 190" stroke="var(--accent)" stroke-width="2" fill="none"/><polygon points="210,190 218.58488245528918,182.83761260270933 220.88083939100602,192.57047352585693" fill="var(--accent)"/><text x="405.0" y="134.0" text-anchor="middle" font-size="16">TC0</text></g><g data-walk-target="c"><path d="M720 98 L670 190" stroke="var(--accent)" stroke-width="2" fill="none"/><polygon points="670,190 670.3820106563359,178.82618830217524 679.1682557520613,183.60132150637384" fill="var(--accent)"/><text x="695.0" y="134.0" text-anchor="middle" font-size="16">TC7</text></g><g data-walk-target="d"><path d="M210 258 L350 335" stroke="var(--accent)" stroke-width="2" fill="none"/><polygon points="350,335 338.8282471643727,334.5618920456617 343.6474346620943,325.7997329588952" fill="var(--accent)"/><text x="280.0" y="286.5" text-anchor="middle" font-size="16">Eligible</text></g><g data-walk-target="f"><path d="M670 258 L550 335" stroke="var(--accent)" stroke-width="2" fill="none"/><polygon points="550,335 555.7160971423175,325.39134590800614 561.1165815589857,333.8076852586577" fill="var(--accent)"/><text x="610.0" y="286.5" text-anchor="middle" font-size="16">Eligible</text></g></svg><figcaption>Author-drawn teaching diagram based on PCI Express Base 6.0. Exchanges unrelated to this lesson are omitted.</figcaption></figure><dl class="st-terms" aria-label="Terms in this passage"><div><dt>TC</dt><dd>Traffic Class</dd></div></dl><section id="mapping"><h2>Where do TC and VC take effect?</h2><dl class="st-terms" aria-label="Terms in this passage"><div><dt>VC</dt><dd>Virtual Channel</dd></div></dl>
<p>TC (Traffic Class) is an invariant TLP label. VC (Virtual Channel) selects queues, buffers, and flow-control resources through each Link's map. Section 2.5.1 explicitly notes that TLPs carry no VC ID field: a Port associates a TLP with a VC through its TC/VC Map.</p><dl class="st-terms" aria-label="Terms in this passage"><div><dt>TLP</dt><dd>Transaction Layer Packet</dd></div></dl>
<p>Start with Table 2-43 (p.233). Its VC0, VC1 row gives TC0–TC6/VC0 and TC7/VC1 as an example. TC0 is fixed to VC0; software configures other supported TCs. A TC must not map to multiple VCs within a Port or Endpoint Function.</p>
<p>Then read the upper example in Figure 2-88 (p.234). TC7 uses VC0 on the Endpoint–Switch Link and VC1 on the Switch–Root Complex Link. The TC7 label stays unchanged; its local resources change. VC IDs and maps must match across each Link, while different Switch Ports can have different configurations.</p>
<p class="source">Reading route: §2.5 Virtual Channel (VC) Mechanism, pp.229–230; §2.5.1 Virtual Channel Identification (VC ID), p.232; §2.5.2 TC to VC Mapping, Table 2-43 TC to VC Mapping Example, p.233; Figure 2-88 An Example of TC/VC Configurations, p.234. Document and PDF pages match.</p></section>
<section id="vc-enable"><h2>Both ends support VC1. How does it become usable?</h2>
<p><strong>Configure matching VC IDs and TC/VC Maps, enable both ends, then confirm that both VC Negotiation Pending bits are clear.</strong> VC Enable is a control. VC Negotiation Pending reports unfinished negotiation. Enable=1 at one end alone does not complete the process.</p>
<div class="example"><p><strong>【模擬資料】Teaching assumptions, not measurements of a particular device or platform.</strong> Consider one Link between Root Port 00:01.0 and single-Function Endpoint 01:00.0. Both Data Link Layers remain DL_Active. The Link uses Non-Flit Mode; Flit Mode is not supported. There is no MFVC and no arbitration table in use. At each end, Extended VC Count=1, Low Priority Extended VC Count=0, and All VCs Enabled remains 0.</p>
<p>The Count excludes default VC0, so each end has two VC Resource register sets. Initially, VC0 is usable with TC/VC Map FFh; the additional resource is disabled. The goal is TC0–TC6/VC0 and TC7/VC1. Stop new TC7 transactions in both directions and ensure all associated outstanding transactions have ended before changing the maps.</p>
<h3>Locate Control and Status in Figure 7-221</h3>
<p>Assume Extended Capability traversal found Virtual Channel Extended Capability ID=0002h, Version=1, at offset 180h in the Root Port and 200h in the Endpoint. Each offset belongs to that Function's Configuration Space, not a global memory address.</p>
<p>Figure 7-221 (p.1183) allocates 0Ch bytes per resource. For the second resource, index 1, the Control offset is <code>14h + 1 × 0Ch = 20h</code>. Status occupies the upper 16 bits of its 32-bit row, so the 16-bit Status offset is <code>18h + 1 × 0Ch + 2 = 26h</code>. The row start at 24h is not the Status access location.</p>
<div class="table-wrap"><table style="min-width:640px"><thead><tr><th scope="col">Read target</th><th scope="col">Root Port 00:01.0</th><th scope="col">Endpoint 01:00.0</th></tr></thead><tbody><tr><td>VC Resource Control Register (1), 32-bit</td><td>180h + 20h = <strong>1A0h</strong></td><td>200h + 20h = <strong>220h</strong></td></tr><tr><td>VC Resource Status Register (1), 16-bit</td><td>180h + 26h = <strong>1A6h</strong></td><td>200h + 26h = <strong>226h</strong></td></tr></tbody></table></div>
<h3>Assign the maps and VC ID before enabling</h3>
<p>In Table 7-207 (pp.1189–1191), each TC/VC Map[7:0] bit selects its corresponding TC. At both ends, remove TC7 from VC0, changing its map from FFh to <strong>7Fh</strong>. Assign resource 1 VC ID[26:24]=1 and Map=<strong>80h</strong>, with VC Enable[31]=0. TC7 remains quiesced while no enabled VC temporarily carries it.</p>
<p>With all other bits assumed zero, resource 1's 32-bit Control snapshot is <strong>01000080h</strong>. After both ends are prepared, set VC Enable at each end; the snapshot becomes <strong>81000080h</strong>. Software updates fields according to their attributes and preserves RsvdP bits; these values illustrate how the fields compose a readback.</p>
<figure class="diagram"><svg style="min-width:640px" viewBox="0 0 900 620" role="img" aria-labelledby="vc-enable-title vc-enable-desc"><title id="vc-enable-title">Enable at both ends, then wait for both negotiations</title><desc id="vc-enable-desc">With DL_Active and both VC Enable bits set, read both Pending bits. If either is one, wait and read again. Only when both are zero may traffic use this VC.</desc><rect x="100" y="20" width="600" height="70" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="400.0" y="45" text-anchor="middle" font-size="18">Both Ports: assign VC ID 1 and TC7 map</text><text x="400.0" y="70" text-anchor="middle" font-size="18">Configure while this VC is disabled</text><path d="M400 90 V119" fill="none" stroke="var(--accent)" stroke-width="2.5"/><polygon points="400,119 395,109 405,109" fill="var(--accent)"/><rect x="100" y="120" width="600" height="70" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="400.0" y="145" text-anchor="middle" font-size="18">Set VC Enable = 1 at both Ports</text><text x="400.0" y="170" text-anchor="middle" font-size="18">Link remains DL_Active</text><path d="M400 190 V224" fill="none" stroke="var(--accent)" stroke-width="2.5"/><polygon points="400,224 395,214 405,214" fill="var(--accent)"/><polygon points="400,225 550,300 400,375 250,300" fill="var(--surface-alt)" stroke="var(--accent)" stroke-width="2"/><text x="400" y="295" text-anchor="middle" font-size="18">Both Pending = 0?</text><text x="400" y="320" text-anchor="middle" font-size="17">VC enabled at both ends</text><path d="M550 300 H720 V414" fill="none" stroke="var(--accent)" stroke-width="2.5"/><polygon points="720,414 715,404 725,404" fill="var(--accent)"/><text x="720" y="285" text-anchor="middle" font-size="17">No: at least one is 1</text><rect x="580" y="415" width="280" height="70" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="720.0" y="440" text-anchor="middle" font-size="18">Wait; read both Ports again</text><text x="720.0" y="465" text-anchor="middle" font-size="18">Pending is read-only</text><path d="M860 450 H880 V207 H400 V224" fill="none" stroke="var(--accent)" stroke-width="2.5"/><polygon points="400,224 395,214 405,214" fill="var(--accent)"/><path d="M400 375 V524" fill="none" stroke="var(--accent)" stroke-width="2.5"/><polygon points="400,524 395,514 405,514" fill="var(--accent)"/><text x="425" y="405" font-size="17">Yes</text><rect x="100" y="525" width="600" height="70" rx="10" fill="var(--surface-alt)" stroke="var(--line)"/><text x="400.0" y="550" text-anchor="middle" font-size="18">TC7 may use the initialized VC</text><text x="400.0" y="575" text-anchor="middle" font-size="18">Credit, ordering and arbitration still apply</text></svg><figcaption>Author-drawn flow based on Tables 7-207/7-208. Both sides are configured; their write order and polling interval are not prescribed by this diagram.</figcaption></figure>
<h3>Read both Status registers; do not write Pending</h3>
<p>Table 7-208 (pp.1191–1192) defines VC Negotiation Pending as Status bit 1, RO, updated by hardware. Its value is defined only while the Link is <strong>DL_Active and that VC Enable=1</strong>. A displayed zero while the VC is disabled does not establish completed negotiation.</p>
<div class="table-wrap"><table style="min-width:640px"><thead><tr><th scope="col">Two observations after enabling</th><th scope="col">Root Port 16-bit Status</th><th scope="col">Endpoint 16-bit Status</th><th scope="col">TC7 use</th></tr></thead><tbody><tr><td>Both enables are 1; initialization is progressing</td><td>0000h: Pending=0</td><td>0002h: Pending=1</td><td>Keep waiting; both ends are not yet complete</td></tr><tr><td>Both enables remain 1; a later read</td><td>0000h: Pending=0</td><td>0000h: Pending=0</td><td>VC1 may be used, subject to normal transmission conditions</td></tr></tbody></table></div>
<p>Hardware clears Pending when negotiation finishes on exit from FC_INIT2. Check the same VC at both ends. Acting on the Root Port's zero alone misses the Endpoint's unfinished initialization. This Status is not a W1C event field; software cannot complete negotiation by writing 1.</p>
<p>After all intended VCs have been enabled, software may set All VCs Enabled (Port VC Control bit 4) to aid buffer allocation. Leaving it clear must still allow correct operation of enabled VCs. Once set, changing a VC Enable in this Capability while the Link is up has undefined behavior; it is not an ordinary live-switching mechanism.</p>
<p class="source">Connected sources: §7.9.1 Virtual Channel Extended Capability, pp.1181–1184, Figure 7-221 Virtual Channel Extended Capability Structure, p.1183; Table 7-202 Port VC Capability Register 1, p.1185; Table 7-207 VC Resource Control Register, pp.1189–1191; Figure 7-229/Table 7-208 VC Resource Status Register, pp.1191–1192; Table 7-204 Port VC Control Register, pp.1186–1187. Document and PDF pages match.</p></div></section>
<section id="example"><h2>After initialization, can VC1 progress while VC0 lacks credit?</h2>
<p><strong>【模擬資料】Continue with the initialized Non-Flit configuration; the following is an assumed transmission instant.</strong> For Endpoint-to-Root-Port traffic, a TC0 Memory Write uses VC0 and a TC7 Memory Write uses VC1. VC0 lacks Posted Data Credit. VC1 has sufficient Header and Data Credit, and the TC7 packet satisfies other ordering and transmission conditions.</p>
<div class="table-wrap"><table><thead><tr><th scope="col">Candidate</th><th scope="col">Resources</th><th scope="col">Eligible for transmission arbitration?</th></tr></thead><tbody><tr><td>TC0 Memory Write</td><td>Required VC0 Data Credit unavailable</td><td>This packet waits</td></tr><tr><td>TC7 Memory Write</td><td>Required VC1 credits available</td><td>Eligible; it still needs to win arbitration</td></tr></tbody></table></div>
<p>Non-Flit Mode has independent FC credit pools per VC, so blocking this VC0 packet does not consume VC1's credits. It also does not establish that all VC0 traffic is blocked: different FC classes within a VC must be evaluated for each candidate. This chapter isolates the VC-level distinction; continue to <a href="/DOCS/pcie-course/chapter-17.html">Chapter 17</a> for detailed credit consumption and updates.</p><dl class="st-terms" aria-label="Terms in this passage"><div><dt>FC</dt><dd>Flow Control</dd></div></dl>
<p>If Flit Mode uses Shared FC, dedicated and shared resources replace this fully independent-pool model. Apply the section 2.6 resource rules before deciding whether a VC is eligible.</p>
<p class="source">Reading route: §2.6 Ordering and Receive Buffer Flow Control, p.235; §6.3.3.1, Implementation Note: VC Control Logic at the Egress Port, p.709. Flow Control protects the adjacent receiver's buffers; it does not establish arrival at the ultimate Completer.</p></section>
<section id="arbitration"><h2>When two VCs are eligible, which uses the Link first?</h2>
<p>First identify the arbitration participants. For a Switch, read Figure 6-8 (p.708) from left to right: routing selects the Egress Port, whose map selects the VC. Traffic from different Ingress Ports competing for the same egress VC undergoes <strong>Port Arbitration</strong>. Different VCs at that egress then compete for the shared Link through <strong>VC Arbitration</strong>. The TLP's TC number alone determines neither decision.</p>
<p>Continue to Figure 6-9 (p.709): read VC ID and Relative Priority, then the priority-group boundary. The specification defines default relative priority in ascending VC ID order. With Strict Priority, the higher VC ID is serviced first. A group using RR (Round Robin) or WRR (Weighted Round Robin) instead requires its arbitration capabilities, selection, and tables; VC IDs alone do not determine every actual transmission order.</p>
<p>The simulated configuration has Low Priority Extended VC Count=0. Under section 6.3.3.2, all VCs therefore use Strict Priority. When both VCs at one transmitter have eligible traffic, VC1 has higher relative priority than VC0. This is not bandwidth reservation inherent in TC7; TC7 is simply mapped to this example's VC1.</p>
<p>Priority cannot bypass a packet's missing credit. Conversely, sustained high-priority traffic can starve lower-priority traffic. Section 6.3.3.2.1 requires regulation of high-priority traffic with Strict Priority and sufficient service for lower-priority transactions to avoid timeouts. Bandwidth and latency guarantees also need the end-to-end contract introduced next.</p>
<p class="source">Reading route: §6.3.3.1 Traffic Flow and Switch Arbitration Model, Figure 6-8 Switch Arbitration Structure, p.708; §6.3.3.2 VC Arbitration - Arbitration Between VCs, Figure 6-9 VC ID and Priority Order - An Example, pp.709–710; §6.3.3.2.1 Strict Priority Arbitration Model and §6.3.3.2.2 Round Robin Arbitration Model, p.710; Table 7-202, p.1185.</p></section>
<section id="service"><h2>What establishes service guarantees for periodic data?</h2>
<p>An Isochronous Contract connects the requester, completer, and fabric-resource responsibilities. In Figure A-1 (p.1521), first follow one complete flow: Device A exchanges upstream Read/Write Requests and returning Read Completions with the Root Complex; Device B to Device C is a separate peer-to-peer flow. Each model needs its own path and service capabilities checked.</p>
<p>Then compare the two Figure A-2 timelines (p.1522). Oversubscription leaves too little service opportunity for other traffic. A concentrated injection burst causes congestion. The contract therefore requires both resource reservation and traffic regulation. Section A.2 relates period T, transaction count N, budgeted payload Y, and latency L. Merely mapping TC7 to VC1 establishes no such contract.</p>
<p>This is a reading entry point, not a complete isochronous configuration. System software must also check aggregate requirements when flows share a VC/TC. Non-isochronous assignment policies are not a universal Base 6.0 platform configuration.</p>
<p class="source">Reading route: §A.1 Introduction, pp.1521–1522; Figure A-1 An Example Showing Endpoint-to-Root-Complex and Peer-to-Peer Communication Models, p.1521; §A.2 Isochronous Contract and Contract Parameters, pp.1522–1523; Figure A-2 Two Basic Bandwidth Resourcing Problems: Over-Subscription and Congestion, p.1522.</p></section>
<section id="sources"><h2>Edition and sources</h2><p>Authority: PCI Express Base Specification Revision 6.0 (6.0-1.0-PUB). Printed document and PDF viewer pages match. Configurations, readbacks, and the teaching flowchart are author-created, not hardware measurements. This revision teaches additional-VC enablement on one Link; MFVC, complete arbitration tables, Shared FC, and full isochronous configuration remain for deeper coverage.</p><details class="source-note"><summary>Complete source locations and purpose</summary><ul>
<li>§2.5 Virtual Channel (VC) Mechanism, pp.229–230; §2.5.1 Virtual Channel Identification (VC ID), p.232; §2.5.2 TC to VC Mapping, p.233; §2.5.3 VC and TC Rules, pp.234–235. Table 2-43 TC to VC Mapping Example, p.233; Figure 2-88 An Example of TC/VC Configurations, p.234: labels, resources, and matching maps.</li>
<li>§2.6 Ordering and Receive Buffer Flow Control, Figure 2-89 Relationship Between Requester and Ultimate Completer, p.235: per-Link flow control and mode-dependent resources.</li>
<li>§7.9.1 Virtual Channel Extended Capability, pp.1181–1184; Figure 7-221 Virtual Channel Extended Capability Structure, p.1183; Table 7-201 Virtual Channel Extended Capability Header, p.1184: applicability, ID, Version, and resource offsets.</li>
<li>§7.9.1.2 Port VC Capability Register 1 (Offset 04h), Table 7-202, p.1185: resource count and priority group; §7.9.1.4 Port VC Control Register (Offset 0Ch), Table 7-204, pp.1186–1187: All VCs Enabled.</li>
<li>§7.9.1.7 VC Resource Control Register, Figure 7-228, p.1189, Table 7-207, pp.1189–1191: Map, VC ID, Enable; §7.9.1.8 VC Resource Status Register, Figure 7-229, p.1191, Table 7-208, pp.1191–1192: Pending validity and dual-end checks.</li>
<li>§6.3.2 TC/VC Mapping and Example Usage, pp.703–704: remapping and TC Filtering; §6.3.3 VC Arbitration, p.705; §6.3.3.1 Traffic Flow and Switch Arbitration Model, pp.706–709, Figure 6-8 Switch Arbitration Structure, p.708: two arbitration stages.</li>
<li>§6.3.3.2 VC Arbitration - Arbitration Between VCs, pp.709–710, Figure 6-9 VC ID and Priority Order - An Example, p.709; §6.3.3.2.1 Strict Priority Arbitration Model and §6.3.3.2.2 Round Robin Arbitration Model, p.710: ordering, groups, regulation, and fairness conditions.</li>
<li>§A.1 Introduction, pp.1521–1522; §A.2 Isochronous Contract and Contract Parameters, pp.1522–1523; Figure A-1 An Example Showing Endpoint-to-Root-Complex and Peer-to-Peer Communication Models, p.1521; Figure A-2 Two Basic Bandwidth Resourcing Problems: Over-Subscription and Congestion, p.1522: entry into the end-to-end contract.</li></ul></details></section>
</article>
<nav class="bottom-nav" aria-label="Course and editions"><a href="/DOCS/pcie-course/index.html">Course overview</a><a href="/DOCS/pcie-course/chapter-16.html">Full Chinese tutorial</a><a href="/pcie/chapter-16-zh-tw/">繁體中文</a></nav>
</div>
