---
layout: post
title: "PCIe Chapter 11：熱插拔與拓樸變動"
date: 2026-10-21 00:00:00 +0800
permalink: /pcie/chapter-11-zh-tw/
categories: [PCIe]
tags: [PCIe, Specification]
lang: zh-TW
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

html:not([data-theme="dark"]) .pcie-article { color-scheme: light; }
html[data-theme="dark"] .pcie-article { color-scheme: dark; }

.pcie-article { background: transparent; margin: 1.5rem 0; }
.pcie-article .lesson { padding: 0; border: 0; background: transparent; }
</style>
<div class="pcie-article" lang="zh-Hant-TW">
<nav class="bottom-nav" aria-label="課程與語言版本"><a href="/DOCS/pcie-course/index.html">課程總覽</a><a href="/DOCS/pcie-course/chapter-11.html">繁中完整教學</a><a href="/pcie/chapter-11-en/">English</a></nav>
<article class="lesson">
<p class="lead">PCIe Hot-Plug 要把實體插槽的變化轉成一致的軟體狀態。能力、通知、供電、Link 就緒與資源配置各有不同的證據；其中任何一步成立，都不能代替其餘步驟。本篇用一個插入案例說明查詢路線，最後比較有秩序移除與非同步移除。</p>
<aside class="note"><strong>依據與假設</strong><p>依 PCIe Base 6.0 與 PCI Firmware 3.3，保留兩者的版本邊界。所有數值、時間與容量是作者案例，另設 Hot-Plug 插槽於 Switch Downstream Port 02:01.0，下游為 03:00.0。假設 OS 已取得 native Hot-Plug 控制權、沒有 SFI 介入，不使用提早就緒通知。</p></aside>
<section id="capability"><h2>能力查詢從管理插槽的 Port 開始</h2><p>在 02:01.0 找到 PCI Express Capability base=0x70 後，先讀 Figure 7-23 的 Port Type 與 Slot Implemented，再看 Figure 7-30 的 Slot Capabilities。不能到 Endpoint 尋找所屬插槽的控制器。實體元件的配置仍取決於 form factor，Base 不要求每種插槽都有相同的按鈕、扣具與指示燈。</p>
<div class="table-wrap"><table><caption>插槽起始快照</caption><thead><tr><th scope="col">Register</th><th scope="col">位置／寬度</th><th scope="col">值</th></tr></thead><tbody><tr><td>PCI Express Capabilities</td><td>0x72／16 bits</td><td>0x0162</td></tr><tr><td>Slot Capabilities</td><td>0x84／32 bits</td><td>0x002825DF</td></tr><tr><td>Slot Control</td><td>0x88／16 bits</td><td>0x17F8</td></tr><tr><td>Slot Status</td><td>0x8A／16 bits</td><td>0x0048</td></tr></tbody></table></div>
<p>0x0162 表示 Version=2、Type=6、Slot Implemented=1。Slot Capabilities bits 0–4 全為 1，具備按鈕、電源控制器、MRL 扣具感測器與兩種指示燈；bit 6=1 支援 Hot-Plug，bit 18=0 支援 Command Completed。bits 31:19 為實體插槽 5，不是 Device Number；Power Limit Value=75、Scale=0，得到 75 W 上限，不是目前耗電量。</p><p>HPS bit 5=0，因此本例只示範有秩序流程。不能把這個 bit 當成所有非同步移除方案的唯一判定；Base 6.0 已不建議以舊 HPS 機制支援 async hot-plug，而建議 DPC。SFI 也可能抑制 HPS 讀值。</p><details class="source-note"><summary>查詢位置</summary><p>§6.7／Table 6-7（pp.727–728）；Figure 7-23／Table 7-19（pp.953–954）→ Figures 7-30–7-32／Tables 7-27–7-29（pp.980–986）。HPS 與 DPC 見 §6.7.6（pp.741–742）。</p></details></section>
<section id="events"><h2>狀態、事件與通知分開解讀</h2><p>Slot Status=0x0048 同時表示 Presence Detect State bit 6=1，以及 Presence Detect Changed bit 3=1。前者是目前偵測結果，後者是待處理事件。相同 Slot Event 尚未清除時，後續同類事件會被忽略，所以一個 bit 不能表示變化次數或完整順序。</p><p>本例主電源關閉時仍由 out-of-band 機制偵測插入。一般在 In-Band PD Disable=0 時，Presence 是 in-band 與適用 out-of-band 的 OR；in-band 需要供電。Presence=1 仍不證明 Link Active。</p><p>0x17F8 已開啟 Presence Changed、Command Completed、DLL State Changed 的通知及 Hot-Plug Interrupt Enable，但事件紀錄與實際收到中斷不同。後者還需符合 INTx 或 MSI／MSI-X 的啟用、向量與路由條件。</p>
<div class="table-wrap"><table><caption>不同時間的事件確認</caption><thead><tr><th scope="col">Slot Status 快照</th><th scope="col">寫入 0x8A 的 RW1C 值</th><th scope="col">無新事件時讀回</th></tr></thead><tbody><tr><td>0x0048：Presence Changed</td><td>0x0008</td><td>0x0040</td></tr><tr><td>0x0050：Command Completed</td><td>0x0010</td><td>0x0040</td></tr><tr><td>0x0140：DLL State Changed</td><td>0x0100</td><td>0x0040</td></tr></tbody></table></div><p>先保存並處理事件，再對指定 RW1C bit 寫 1；Presence 是唯讀狀態。實際處理須重新核對並行變化，不對相鄰 Control／Status 做不加區分的 32-bit 讀改寫。</p><details class="source-note"><summary>事件與中斷</summary><p>§6.7.3.1、§6.7.3.4（pp.735–737）；Tables 7-28／7-29（pp.983–986）。中斷傳送回顧 <a href="/pcie/chapter-7-zh-tw/">Chapter 7</a>。</p></details></section>
<section id="timing"><h2>命令完成不等於可以立刻枚舉</h2><p>確認扣具關閉、功率預算足夠且沒有前一筆未完成命令後，本例寫 Slot Control=0x12F8：Power On、Power Indicator Blink、Attention Indicator Off，保留原通知設定。任何 Slot Control 寫入都是 Hot-Plug 命令；本例支援 Command Completed，須等前一筆完成才發下一筆。一秒未完成時，規格允許重送或發下一筆，不能據此假定供電成功。</p>
<div class="table-wrap"><table><caption>作者設定的插入時間線</caption><thead><tr><th scope="col">時間</th><th scope="col">證據或動作</th><th scope="col">意義</th></tr></thead><tbody><tr><td>0 ms</td><td>寫入 Power On</td><td>啟動插入供電流程。</td></tr><tr><td>20 ms</td><td>Command Completed</td><td>控制器可接受下一個命令；不保證實際動作完成。</td></tr><tr><td>40 ms</td><td>Link Status=0x2043</td><td>讀到 Data Link Layer Link Active=1。</td></tr><tr><td>140 ms</td><td>開始 Configuration Request</td><td>從讀到 Active 起已等 100 ms；本例無提早就緒機制。</td></tr></tbody></table></div>
<p>Power Controller Control 的讀回值也不是電源量測；故障可能阻止供電。DLL State Changed 後，必須讀 Link Active，不能只憑 Changed bit 發設定存取。Hot-Add 的 DLL 變化一秒期限從本例的 Power On 寫入起算；判定已 Active 卻無 Successful Configuration Completion 的裝置損壞，則須從 Active 起允許至少一秒。兩個期限不同。</p><details class="source-note"><summary>完成與等待條件</summary><p>§6.7.3.2–§6.7.3.3（pp.735–736）；Tables 7-28／7-29（pp.984–986）。Reset 與 Readiness 例外見 §6.6.1（pp.721–723）及 <a href="/pcie/chapter-9-zh-tw/">Chapter 9</a>。</p></details></section>
<section id="resources"><h2>可存取設定空間之後，仍要有可用資源</h2><p>假設目前路徑只剩 0x80080000–0x800FFFFF，共 0x80000 bytes（512 KiB），新 BAR 需要 0x100000 bytes（1 MiB）且依大小對齊。即使 Configuration Request 成功，這段空間仍放不下。BAR 寫到視窗外不會讓 Bridge 自動轉送。</p><p>事先預留 Bus Numbers 與位址範圍可降低配置困難；不足時能否搬移其他配置，取決於 Host Bridge 資源、沿途視窗及軟體協調。這是作者的系統推演，不是規格保證每張熱插入卡都有空間。詳細枚舉與 BAR 計算連回 Chapters 3–4。</p><details class="source-note"><summary>配置邊界</summary><p>PCI Firmware 3.3 §3.5（pp.34–37）、§4.3.2（p.47）；<a href="/pcie/chapter-4-zh-tw/">Chapter 4</a>。</p></details></section>
<section id="removal"><h2>移除模式決定軟體是否來得及協調</h2><p>Orderly removal 有機會先停止新工作，依裝置協定處理在途工作，再完成供電、指示燈與移除流程。清 BME 不等於舊交易或應用工作都完成。Async removal 則可能在軟體協調前已失去裝置，必須處理失效狀態與未完成工作，不能再向消失的裝置要求完成證據。</p><p>這是作者整理的系統流程；各類裝置的停止、取消與保存方法不由 PCIe 統一定義。DPC 限制下游錯誤擴散，並不判定應用工作成功；其狀態與恢復條件見 <a href="/pcie/chapter-12-zh-tw/">Chapter 12</a>。管理權則見 <a href="/pcie/chapter-13-zh-tw/">Chapter 13</a>。依據：Base §6.7、§6.7.6（pp.727、741–742）、§6.2.11（pp.694–697）；Firmware §4.5。</p></section>
<section id="questions"><h2>用兩個問題檢查判讀</h2><details class="question"><summary>Presence Changed=1、Presence=0，是否代表從未插入？</summary><p>不能。Changed 是待處理事件，Presence 是目前結果，兩者不能還原完整歷史。依據：§6.7.3.1、Table 7-29。</p></details><details class="question"><summary>Command Completed 與 Power Fault 同時存在，是否互相矛盾？</summary><p>不矛盾。命令介面可以接收下一筆，不保證供電成功；仍須處理電源故障。依據：Tables 7-28／7-29。</p></details></section>
</article>
<nav class="bottom-nav" aria-label="課程與語言版本"><a href="/DOCS/pcie-course/index.html">課程總覽</a><a href="/DOCS/pcie-course/chapter-11.html">繁中完整教學</a><a href="/pcie/chapter-11-en/">English</a></nav>
</div>
