---
layout: post
title: "PCIe Chapter 4：BAR、位址空間與資源配置"
date: 2026-10-20 00:00:00 +0800
permalink: /pcie/chapter-4-zh-tw/
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

html:not([data-theme="dark"]) .pcie-article { color-scheme: light; }
html[data-theme="dark"] .pcie-article { color-scheme: dark; }

.pcie-article { background: transparent; margin: 1.5rem 0; }
.pcie-article .lesson { padding: 0; border: 0; background: transparent; }
</style>
<div class="pcie-article" lang="zh-Hant-TW">
<nav class="bottom-nav" aria-label="課程與語言版本"><a href="/DOCS/pcie-course/index.html">課程總覽</a><a href="/DOCS/pcie-course/chapter-4.html">繁中完整教學</a><a href="/pcie/chapter-4-en/">English</a></nav>
<article class="lesson">
<p class="lead">找到 Function 後，還要建立資源位址與沿途轉送範圍。BAR 描述 Endpoint 自己需要的空間；Bridge Window 決定要求能否走到下游；Command 的控制位則決定目前允許哪些存取。這三件事必須一起成立。</p>
<p><a href="/DOCS/pcie-course/chapter-4.html">完整中文教學</a> · <a href="/DOCS/pcie-course/index.html">課程路線</a> · <a href="/pcie/chapter-4-en/">English</a></p>
<aside class="note"><strong>版本與前提</strong><p>欄位依 Base 6.0；位址視角與交接依 PCI Firmware 3.3，兩者不是同版配套。案例是一般 Type 0 PCI Express Endpoint，非 VF，不用 Enhanced Allocation 或 Resizable BAR。所有資料為作者設計，不操作實機。探測時驅動尚未使用裝置，沒有進行中的交易，MSE、BME 均為 0；軟體保存 BAR 原值並確認設定寫入完成。文件頁與 PDF 頁序相同。</p></aside>
<section id="format"><h2>先認格式，再談大小</h2>
<p>BAR 位於 Configuration Header，不是工作資料緩衝區。Type 0 Header 提供六個 DWORD 位置；64-bit BAR 佔兩個連續位置。Bridge 的 Type 1 Header 則只有兩個 BAR 位置，與下游 Memory Window 分開。</p>
<p>Memory BAR 的 bit 0 為 0，bits 2:1 的 00b／10b 分別表示 32／64-bit，bit 3 為 Prefetchable；I/O BAR 的 bit 0 為 1，位址從 bit 2 起，不能套用 Memory BAR 的低四位遮罩。本例不用 I/O BAR：一般 PCIe Endpoint 不得依賴 OS 配置 I/O 資源，也不得發 I/O Requests。</p>
<p>Prefetchable 表示資源容許規格列出的無讀取副作用與寫入合併等行為，不是 CPU 快取狀態。對本例的一般 Endpoint，Prefetchable BAR 須支援 64-bit；非 Prefetchable 可以是 32-bit。</p>
<details class="source-note"><summary>查閱順序</summary><p>先看 Figure 7-10（p.928）或 Figure 7-14（p.936）定位，再看 Figures 7-11／7-12、Table 7-9（p.929）辨識格式；容量、配對與對齊規則在 §7.5.1.2.1（p.930）。一般 Endpoint 限制見 §1.3.2.2，p.105。</p></details></section>
<section id="size"><h2>探測值必須按 32 或 64 bits 計算</h2>
<p>規格的探測方法先停用相應解碼、保存原 BAR，再寫全 1、讀回並遮掉類型 bits。取反加一時，必須限制運算寬度；最後還原原值，或在重新啟用前完成一致的新配置。BME 清零不代表先前交易自動消失，本例另以沒有進行中交易為前提。</p>
<div class="table-wrap"><table><caption>教學探測與分配結果</caption><thead><tr><th scope="col">資源</th><th scope="col">全 1 探測的讀回值</th><th scope="col">計算大小與分配</th></tr></thead><tbody><tr><td>BAR0，0x10</td><td>0xFFFFC000</td><td>32-bit 非 Prefetchable；16 KiB，配置 0x80004000–0x80007FFF。</td></tr><tr><td>BAR2／BAR3，0x18／0x1C</td><td>0xFFE0000C／0xFFFFFFFF</td><td>64-bit Prefetchable；2 MiB，配置 0x120000000–0x1201FFFFF。</td></tr></tbody></table></div>
<pre><code>BAR0 mask = 0xFFFFC000 &amp; 0xFFFFFFF0
size = ((~mask) &amp; 0xFFFFFFFF) + 1 = 0x4000

BAR2/3 mask = (0xFFFFFFFF &lt;&lt; 32) | (0xFFE0000C &amp; 0xFFFFFFF0)
size = ((~mask) &amp; 0xFFFFFFFFFFFFFFFF) + 1 = 0x200000</code></pre>
<p>BAR3 是 BAR2 的高 DWORD，不能因為回全 1 就當成另一個 I/O BAR。配置後 BAR0 為 0x80004000；BAR2／3 為 0x2000000C／0x00000001。初始 BAR 為 0 不代表未實作；只有依正確探測取得的未實作結果，才能如此判讀，也不能把全零遮罩誤算成 4 GiB 需求。</p>
<p>假設 BAR0 的 +0x120 是有效 Register，PCI 位址就是 0x80004120。本例另假設 CPU／PCI 相同映射，CPU 因而使用同一數字；這不是所有平台的保證。該 Register 功能與可用資源位址也是教學假設。</p>
<details class="source-note"><summary>來源與限制</summary><p>Base 6.0 §7.5.1.2.1，pp.928–930，包含 p.930 的 32／64-bit sizing 說明。Firmware 3.3 §3.1.1（p.32）容許 non-identity MMIO mapping。所有分配須另外符合平台資源、對齊、不重疊與位址寬度要求。</p></details></section>
<section id="window"><h2>沿途每一層 Window 都要涵蓋目標</h2>
<p>到 03:00.0 的路徑經 Root Port 00:01.0、Switch Upstream Port 01:00.0、Downstream A 02:01.0。本例三者皆支援並配置下列窗口，平台已保留相應範圍，其他分支不佔用它們。</p>
<div class="table-wrap"><table><caption>三個 Bridge 的共同教學配置</caption><thead><tr><th scope="col">欄位</th><th scope="col">設定值</th><th scope="col">解碼後的範圍</th></tr></thead><tbody><tr><td>Memory Base／Limit，0x20／0x22，各 16 bits</td><td>0x8000／0x8000</td><td>0x80000000–0x800FFFFF</td></tr><tr><td>Prefetchable Base／Limit，0x24／0x26，各 16 bits；Upper，0x28／0x2C，各 32 bits</td><td>0x2001／0x2011；Upper 均為 1</td><td>0x120000000–0x1201FFFFF</td></tr></tbody></table></div>
<p>Base 的低 20 address bits 補 0，Limit 補 1，形成 1 MiB 粒度的包含起點與終點的範圍。Prefetchable 欄位的低 nibble=1 表示支援 64-bit，Upper 接成位址高 32 bits。窗口可以比 BAR 大，但不保證空隙中有有效 Register；也不能把 Bus Number 範圍拿來代替 Memory Window。</p>
<details class="source-note"><summary>來源</summary><p>Figure 7-14，p.936；§7.5.1.3.8–§7.5.1.3.10，pp.940–941。完整教學逐步計算各個遮罩、位移與包含關係。</p></details></section>
<section id="control"><h2>MSE 與 BME 不是同一個開關</h2>
<p>Command 位於 0x04，寬度 16 bits。bit 0 控制 I/O Space，bit 1 的 MSE 控制收到的 Memory 存取，bit 2 的 BME 控制 Function 發起 Memory／I/O Requests；Type 1 Port 的 BME 還控制向上游轉送相關要求，不阻擋 Completion。</p>
<p>在資源、窗口、平台映射與裝置介面均已就緒的前提下，本例 Endpoint 與三個 Bridge 的 Command=0x0002，允許 CPU 讀取已配置的 MMIO，但 Endpoint 尚不能發起 DMA Memory Request；讀取回覆的 Completion 不被 BME 阻擋。BME=0 也禁止 MSI／MSI-X，因為它們是帶內 Memory Write。</p>
<p>把 Endpoint 改為 0x0006，只增加發起相關要求的許可，仍要準備緩衝區、裝置工作、平台轉譯與上游 Port 的 BME。修改 Command 時也不能任意連同 0x06 的 Status 一起原樣回寫，因為 Status 含 RW1C 位元。</p>
<details class="source-note"><summary>控制位來源</summary><p>Base 6.0 §7.5.1.1.3，Figure 7-5／Table 7-4，pp.917–920；BME、Completion 與 MSI 說明在 p.919。Command／Status 布局：Figure 7-4，p.916；Status RW1C：Table 7-5，pp.922–923。</p></details></section>
<section id="checks"><h2>配置與交接的結論要分清</h2>
<p>Firmware 3.3 §3.5（pp.34–35）以 I/O／Memory Enable 及 ROM Enable 判斷相應資源配置，不使用 BME 判定 BAR 是否有效。已啟用的資源必須由韌體正確配置，但驅動仍須依裝置介面準備工作。</p>
<details class="question"><summary>16 KiB BAR 改放 0x80005000，可以嗎？</summary><p>不行。低 14 bits 不是全 0，未達自然對齊；本例正確的基底 0x80004000 才符合。（§7.5.1.2.1，p.930。）</p></details>
<details class="question"><summary>窗口正確，Endpoint MSE=0，是否仍可成功讀 MMIO？</summary><p>不能期待成功。MSE=0 時，Endpoint 收到的 Memory Space 存取按 UR 處理；路徑可轉送不能代替終點啟用。（Table 7-4，p.918。）</p></details></section>
<p>Chapter 5 將延伸到 Request 與 Completion；後續章節仍在規劃中。</p>
</article>
<nav class="bottom-nav" aria-label="課程與語言版本"><a href="/DOCS/pcie-course/index.html">課程總覽</a><a href="/DOCS/pcie-course/chapter-4.html">繁中完整教學</a><a href="/pcie/chapter-4-en/">English</a></nav>
</div>
