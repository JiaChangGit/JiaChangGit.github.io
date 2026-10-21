---
layout: post
title: "PCIe Chapter 1：拓樸、Function 與識別方式"
date: 2026-10-20 00:00:00 +0800
permalink: /pcie/chapter-1-zh-tw/
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
<nav class="bottom-nav" aria-label="課程與語言版本"><a href="/DOCS/pcie-course/index.html">課程總覽</a><a href="/DOCS/pcie-course/chapter-1.html">繁中完整教學</a><a href="/pcie/chapter-1-en/">English</a></nav>
<article class="lesson">
<p class="lead">看到兩個 Function，不能直接說有兩張卡；看到相同的 BDF，也要先確認是否位於同一個 Segment。本章把實體連接、軟體看到的橋接結構，以及 Function 的識別號放在同一個案例中，練習從欄位讀值還原它們的關係。</p>
<p><a href="/DOCS/pcie-course/chapter-1.html">完整中文教學與拓樸圖</a> · <a href="/DOCS/pcie-course/index.html">課程路線</a> · <a href="/pcie/chapter-1-en/">English</a></p>
<aside class="note"><strong>版本與範圍</strong><p>本章欄位依 PCI Express Base Specification Revision 6.0，Segment 的背景另參考 PCI Firmware Specification Revision 3.3。頁碼對應課程採用的 PDF，文件頁與 PDF 頁序相同。案例採傳統 Bus／Device／Function（BDF）編址，不使用 Alternative Routing-ID Interpretation（ARI），也不使用 Flattening Portal Bridge（FPB）的識別方式；這些機制涉及額外的發現、編號或路由規則，尤其 ARI 會改變 Device／Function 位元的解讀。案例也不使用 SR-IOV、Phantom／Shadow Functions；後兩者可借用額外的 Function 識別號，另待進階章節討論。</p></aside>

<section id="objects">
<h2>一張卡、Function 與 Port，為什麼不能互相代換？</h2>
<p>卡是實體組裝的單位，Function 則是軟體可以個別辨識與設定的對象。一張卡可以提供多個 Function，也可能包含 Switch 和多個 Endpoint。因此，Function 數量不能直接換算成卡片數量。</p>
<p>Switch 的 Upstream Port 朝向 Root Complex，Downstream Port 則朝向下游。軟體會把各個 Switch Port 看成 PCI-to-PCI Bridge；這些橋接結構透過內部邏輯 Bus 相連。這不是說外部 PCIe Link 變成了共用的平行匯流排，也不是每個 Bridge 都對應一顆獨立晶片。</p>
<p>讀拓樸時，先保留這兩種視角：Link 告訴我們相鄰的硬體如何連接，Bridge 的設定資料則讓軟體辨識通往下游的路徑。</p>
<details class="source-note"><summary>Switch 與邏輯拓樸的規格位置</summary><p>Base 6.0 §1.3.3，pp.106–107，Figure 1-3 在 p.107；§7.1，pp.903–904，Figure 7-1／Figure 7-2 在 p.904。前者說明 Switch 的連接與橋接呈現，後者對照軟體看到的配置結構。本例的 Switch 內部 Bus 只連接 Downstream Port 的虛擬 Bridge，Endpoint 則位於對外 Link 的另一端。</p></details>
</section>

<section id="types">
<h2>想知道某個 Function 扮演什麼角色，應先讀哪兩種欄位？</h2>
<p>先讀設定空間 <code>0x0E</code> 的 8-bit Header Type。低 7 bits 決定標頭格式，bit 7 是 Multi-Function Device 指示。再找出 PCI Express Capability，讀取起點加 <code>0x02</code> 的 16-bit PCI Express Capabilities Register，以 bits 7:4 的 Device/Port Type 判斷 PCIe 角色。兩個欄位名稱都帶有 Type，回答的問題卻不同。</p>
<aside class="example"><strong>教學假設</strong><p>以下位址與讀值由作者設計，不是實機量測。枚舉已完成，拓樸在讀取期間維持穩定，設定讀取均成功。各 Function 的 PCI Express Capability 都已沿清單找到，起點恰好是 <code>0x70</code>；因此本例的角色欄位位於 <code>0x72</code>。表中 Device/Port Type 是擷取後的欄位值，並非完整 Register 讀值。如何尋找 Capability，請回看 <a href="/DOCS/pcie-course/chapter-0.html#case">Chapter 0 的查詢案例</a>。</p></aside>
<div class="table-wrap"><table><caption>Header 格式與 PCIe 角色要分開判讀</caption><thead><tr><th scope="col">查詢對象</th><th scope="col">Header Type 讀值</th><th scope="col">Device/Port Type 欄位值</th><th scope="col">結論</th></tr></thead><tbody>
<tr><td>Endpoint A 的 Function 0</td><td><code>0x80</code></td><td><code>0x0</code></td><td>Type 0 標頭；可能有多個 Function；PCI Express Endpoint。</td></tr>
<tr><td>Root Port</td><td><code>0x01</code></td><td><code>0x4</code></td><td>Type 1 標頭；Root Port。</td></tr>
<tr><td>Switch Upstream Port</td><td><code>0x01</code></td><td><code>0x5</code></td><td>Type 1 標頭；Switch Upstream Port。</td></tr>
<tr><td>Switch Downstream Port</td><td><code>0x01</code></td><td><code>0x6</code></td><td>Type 1 標頭；Switch Downstream Port。</td></tr>
</tbody></table></div>
<pre><code>Header 格式：0x80 &amp; 0x7F = 0
Multi-Function Device：(0x80 &amp; 0x80) &gt;&gt; 7 = 1
Device/Port Type：(PCIe_Capabilities &amp; 0x00F0) &gt;&gt; 4</code></pre>
<p><code>0x80</code> 不能解成「Type 128」，也不能解成「已有 8 個 Function」。Multi-Function Device bit 為 1 表示裝置可能有多個 Function；實際有哪些 Function，仍須以發現結果為準。本例的 Endpoint A 指提供端點功能的元件；另假設其 Function 0 與 Function 1 都已被找到。</p>
<details class="source-note"><summary>這一步應如何翻閱規格？</summary><p>先看 Base 6.0 §7.5.1.1.9 的 Figure 7-8／Table 7-7（pp.924–925），分清 Header 格式與 bit 7。接著用 Figure 7-21（p.952）定位 Capability 內的 Register，再以 Figure 7-23／Table 7-19（pp.953–954）查 Device/Port Type。Type 1 標頭只能先告訴我們要用橋接格式，不能單獨區分 Root Port 與 Switch Port。</p></details>
</section>

<section id="path">
<h2>目標是 0000:03:00.1，怎麼確認它位於哪條下游路徑？</h2>
<p>本例在 Segment <code>0000</code> 中放置一個 Root Port 和一個有兩個 Downstream Port 的 Switch。Endpoint A 的兩個 Function 位於 Bus <code>03</code>，Endpoint B 位於 Bus <code>04</code>。下表是已完成配置的快照；本章先讀懂結果，Bus Number 的配置程序留到枚舉章節。</p>
<div class="table-wrap"><table><caption>教學快照：Bridge 的 BDF 與下游 Bus 範圍（數字皆為十六進位）</caption><thead><tr><th scope="col">Bridge 角色</th><th scope="col">BDF（Segment 0000）</th><th scope="col">Secondary</th><th scope="col">Subordinate</th><th scope="col">本例下游</th></tr></thead><tbody>
<tr><td>Root Port</td><td><code>00:01.0</code></td><td><code>01</code></td><td><code>04</code></td><td>Switch 及其兩條分支。</td></tr>
<tr><td>Switch Upstream Port</td><td><code>01:00.0</code></td><td><code>02</code></td><td><code>04</code></td><td>內部 Bus 02 上的兩個 Downstream Port。</td></tr>
<tr><td>Switch Downstream Port A</td><td><code>02:01.0</code></td><td><code>03</code></td><td><code>03</code></td><td>Endpoint A：<code>03:00.0</code>、<code>03:00.1</code>。</td></tr>
<tr><td>Switch Downstream Port B</td><td><code>02:02.0</code></td><td><code>04</code></td><td><code>04</code></td><td>Endpoint B：<code>04:00.0</code>。</td></tr>
</tbody></table></div>
<p>Secondary Bus Number 表示緊接在 Bridge 下游的 Bus，Subordinate Bus Number 則界定其下游 Bus Number 範圍的上限。目標 Bus <code>03</code> 落在 Root Port 的 <code>01–04</code>、Upstream Port 的 <code>02–04</code> 及 Downstream Port A 的 <code>03–03</code> 範圍內；Downstream Port B 的範圍只有 <code>04–04</code>，因此不在本例通往目標的路徑上。</p>
<p>這裡用範圍核對已知拓樸，不代表範圍內每個號碼都必須有裝置。Bridge 自己的 BDF 與它通往哪個 Bus 也要分開：<code>02:01.0</code> 本身位於 Bus <code>02</code>，其 Secondary 為 <code>03</code>。本章不以 Primary Bus Number 推導 Bridge 自己的 BDF；Base 6.0 將該欄位保留作舊式相容用途，PCIe 通常不使用它。</p>
<details class="source-note"><summary>下游 Bus Number 應讀哪裡？</summary><p>Base 6.0 §7.5.1.3 的 Figure 7-14（p.936）列出 Type 1 Header。Secondary 與 Subordinate 分別在 byte offset <code>0x19</code>、<code>0x1A</code>，各讀 8 bits；含義見 §7.5.1.3.3–§7.5.1.3.4（p.937）。相鄰的 Primary 位於 <code>0x18</code>，其 PCIe 相容性說明見 §7.5.1.3.2（同頁）。</p></details>
</section>

<section id="identity">
<h2>BDF、Segment 與 Requester ID，各自保留了哪些資訊？</h2>
<p>在本章的傳統編址下，BDF 包含 8-bit Bus Number、5-bit Device Number 與 3-bit Function Number。<code>0000:03:00.1</code> 的前四位是 Segment；同一個 Segment 內，後面的 <code>03:00.1</code> 才是 BDF。這些數字表示邏輯識別位置，不是實體插槽的編號。</p>
<div class="table-wrap"><table><caption>相同或相近的數字，可能指向不同 Function</caption><thead><tr><th scope="col">識別號</th><th scope="col">本例代表的對象</th><th scope="col">需要保留的差異</th></tr></thead><tbody>
<tr><td><code>0000:03:00.0</code></td><td>Endpoint A 的 Function 0。</td><td>與下一列共用 Bus、Device，Function 不同。</td></tr>
<tr><td><code>0000:03:00.1</code></td><td>Endpoint A 的 Function 1。</td><td>必須使用自己的設定空間讀值。</td></tr>
<tr><td><code>0001:03:00.0</code></td><td>另一個 Segment 中的 Endpoint。</td><td>BDF 與第一列相同，但 Segment 不同。</td></tr>
</tbody></table></div>
<p>另假設 Segment <code>0001</code> 中也已發現 <code>03:00.0</code>。這是作者加入的第二個邏輯範圍，並非前一張表的下游分支；不能省略 Segment 後把兩筆紀錄合併。</p>
<p>當 <code>0000:03:00.1</code> 是要求的來源時，本例的 16-bit Requester ID 按以下方式組成：</p>
<pre><code>Requester ID = (Bus &lt;&lt; 8) | (Device &lt;&lt; 3) | Function
             = (0x03 &lt;&lt; 8) | (0x00 &lt;&lt; 3) | 0x1
             = 0x0301</code></pre>
<p><strong>案例推演：</strong><code>0x0301</code> 保留 BDF，沒有把 Segment <code>0000</code> 編進這 16 bits。這項結論僅限 Requester ID 欄位，不能擴大成「所有 PCIe 封包都沒有 Segment 資訊」；Base 6.0 的部分 Flit Mode 封包另有相關欄位。本章也不把 BDF 當作永久硬體身分：若不同時間的紀錄使用了不同配置，僅憑 BDF 相同或不同，仍不足以判斷是不是同一個實體裝置。</p>
<details class="source-note"><summary>識別範圍與位元配置的規格位置</summary><p>傳統 BDF：Base 6.0 §7.3.1（p.911），§2.2.4.2／Table 2-8（p.147），Figures 2-20、2-22（p.148）。Requester ID：§2.2.6.2（pp.156–157），其中 p.156 說明 16-bit 識別號及執行期間可能改變的 Bus／Device Number，p.157 另說明 Segment 欄位。Segment Group 的邏輯範圍：Firmware 3.3 §1.3（pp.8–9），§4.3.2.3（p.47）。</p></details>
</section>

<section id="self-check">
<h2>換一個觀察結果，還能沿用原來的結論嗎？</h2>
<details class="question"><summary>只讀到 Header Type 為 0x80，就能宣告 Function 1 一定存在嗎？</summary><p>不能。Table 7-7（pp.924–925）只讓我們判定 Type 0 標頭，以及裝置可能有多個 Function。必須另有 Function 1 的有效發現結果，才能宣告它存在；本例已把這項結果列為教學假設。</p></details>
<details class="question"><summary>目標改成 0000:04:00.0，仍然經過 Downstream Port A 嗎？</summary><p>不會。依本例快照，Bus <code>04</code> 落在 Downstream Port B 的 <code>04–04</code> 範圍內，卻不在 A 的 <code>03–03</code> 範圍。前段仍經過同一個 Root Port 與 Upstream Port，只有 Switch 的下游分支改變。（Base 6.0 §7.5.1.3.3–§7.5.1.3.4，p.937。）</p></details>
<details class="question"><summary>兩筆紀錄的 BDF 都是 03:00.0，是否就可以視為同一個 Function？</summary><p>還不能。至少先確認 Segment 與紀錄所屬的配置時間。本例的 <code>0000:03:00.0</code> 和 <code>0001:03:00.0</code> 是不同 Function；若是不同時間的紀錄，相同 BDF 也不能單獨證明硬體身分相同。（Firmware 3.3 §1.3，pp.8–9；Base 6.0 §2.2.6.2，p.156。）</p></details>
</section>
<p>讀懂這些識別資訊後，下一步才是系統性地查詢某個 Function 的設定空間與 Capability。完整拓樸圖、逐步判讀與來源整理，見 <a href="/DOCS/pcie-course/chapter-1.html">Chapter 1 中文教學</a>；接著可讀 <a href="/DOCS/pcie-course/chapter-2.html">Chapter 2：設定空間與 Capability</a>。</p>
</article>
<nav class="bottom-nav" aria-label="課程與語言版本"><a href="/DOCS/pcie-course/index.html">課程總覽</a><a href="/DOCS/pcie-course/chapter-1.html">繁中完整教學</a><a href="/pcie/chapter-1-en/">English</a></nav>
</div>
