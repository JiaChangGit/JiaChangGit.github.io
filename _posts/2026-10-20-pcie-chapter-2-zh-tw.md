---
layout: post
title: "PCIe Chapter 2：讀取設定空間與尋找 Capability"
date: 2026-10-20 00:00:00 +0800
permalink: /pcie/chapter-2-zh-tw/
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
<nav class="bottom-nav" aria-label="課程與語言版本"><a href="/DOCS/pcie-course/index.html">課程總覽</a><a href="/DOCS/pcie-course/chapter-2.html">繁中完整教學</a><a href="/pcie/chapter-2-en/">English</a></nav>
<article class="lesson">
<p class="lead">查詢 PCIe 功能時，先找對清單，再解碼欄位。Capability 的位置不是固定常數，清單中的 ID、Next 與結構內的相對位移也有不同作用。本章以 Device Serial Number（DSN）說明如何從功能名稱走到可驗證的讀取結果。</p>
<p><a href="/DOCS/pcie-course/chapter-2.html">完整中文教學</a> · <a href="/DOCS/pcie-course/index.html">課程路線</a> · <a href="/pcie/chapter-2-en/">English</a></p>
<aside class="note"><strong>版本與前提</strong><p>依 PCI Express Base Specification Revision 6.0。以下位置與讀值為作者設計，不是量測；目標是已找到的一般 Type 0 PCI Express Endpoint，非 RCiEP／VF，不用 ARI、SR-IOV 或 RCRB 清單。設定讀取成功、快照穩定，平台可存取完整設定空間。本例不支援 Flit Mode，因此 AER Header 可採 Version 2。頁碼為所採 PDF 的文件頁／PDF 頁，兩者相同。</p></aside>
<section id="space"><h2>先區分查詢對象、設定 offset 與 CPU 位址</h2>
<p>Segment 與 BDF 選定 Function，Configuration Space 內的 byte offset 再選 Register。每個 Function 有 4096 bytes；前 256 bytes 是 PCI 相容區，0x100–0xFFF 是延伸區。ECAM 可以將 CPU 的記憶體映射存取轉成 Configuration Request；這不是裝置 Memory BAR 的工作區，也不能把設定 offset 直接當作 CPU 實體位址。</p>
<p>傳統 Capability 清單由 Header 的 Capabilities Pointer 進入，本章 Type 0／1 的指標在 0x34。Extended 清單則直接從 0x100 開始。PCI Express Capability 本身在傳統清單，DSN 才在 Extended 清單；不能靠名稱是否含 PCIe 來分類。</p>
<details class="source-note"><summary>閱讀位置</summary><p>Base 6.0 §7.2–§7.2.2.2，Figure 7-3／Table 7-1，pp.905–909；Figure 7-4，p.916；Capabilities Pointer：§7.5.1.1.11，p.926；Extended 清單：§7.6–§7.6.3，Figures 7-42／7-43、Table 7-39，pp.1008–1010。</p></details></section>
<section id="lists"><h2>ID 為 0 與 Next 為 0，不能混為一談</h2>
<p>傳統清單一般以 16-bit 開頭的低 byte 表示 ID、高 byte 表示 Next。教學資料中的路徑是 <code>0x40 → 0x50 → 0x70 → 0xD0 → 0</code>，依序為 PM、Null、PCIe、MSI-X。</p>
<div class="table-wrap"><table><caption>代表性讀值：位置均為 Function 內的 byte offset</caption><thead><tr><th scope="col">位置與寬度</th><th scope="col">讀值</th><th scope="col">判讀</th></tr></thead><tbody><tr><td>0x50，16 bits</td><td>0x7000</td><td>傳統 ID=00h 是 Null；Next=0x70，繼續走訪。</td></tr><tr><td>0x100，32 bits</td><td>0x18020001</td><td>Extended ID=0001h，AER Version 2；Next=0x180。</td></tr><tr><td>0x180，32 bits</td><td>0x00010003</td><td>Extended ID=0003h，DSN Version 1；Next=0，清單結束。</td></tr></tbody></table></div>
<pre><code>Extended ID = header &amp; 0xFFFF
Version     = (header &gt;&gt; 16) &amp; 0xF
Next        = (header &gt;&gt; 20) &amp; 0xFFC</code></pre>
<p>Next 是從整份設定空間起點計算的 byte offset，已經包含所需的位移；不能再加目前結構位置，也不必乘 4。遇到未知 ID，仍可依有效的 Header 走到下一項。解析器應檢查範圍、對齊與是否重訪同一個 offset；這些是教材採用的可靠性檢查，不是新增的硬體功能。位置不必遞增。</p>
<details class="source-note"><summary>ID 與清單格式的來源</summary><p>PM：Figure 7-18／Table 7-14，p.945；PCIe：Figure 7-22／Table 7-18，p.953；MSI-X：Figure 7-59／Table 7-48，pp.1021–1022；Null：§7.9.27、Figure 7-384／Table 7-336，p.1315。Extended Header：Table 7-39，p.1010；AER：Figure 7-154／Table 7-134，p.1112。Flit Mode 支援者的 AER Header 須為 Version 3，本例已排除。</p></details></section>
<section id="dsn"><h2>找到 DSN 後，還要分清資料位置與表示順序</h2>
<p>先以 Figure 7-242／Table 7-221 確認 ID 0003h，再以 Figure 7-241 找 Lower DW 與 Upper DW：它們位於結構起點 +0x04、+0x08。本例從 0x184 讀 32 bits 得 0x33221100，從 0x188 讀 32 bits 得 0x77665544。</p>
<pre><code>Register 整數 = (0x77665544 &lt;&lt; 32) | 0x33221100
              = 0x7766554433221100</code></pre>
<p>Table 7-222 另外規定 Register byte 與 EUI-64 byte 的對映；依 EUI 高 byte 到低 byte 書寫，本例為 <code>00-11-22-33-44-55-66-77</code>。數字只示範重組，不宣稱是已配發或可使用的產品序號；實際值須符合 IEEE 公司識別碼與製造商延伸識別碼規則，也不能單憑此值當成身分認證。</p>
<p>DSN 是可選能力。一般多功能 Device 若實作 DSN，Function 0 必須實作；其他有實作的 Function 必須回報相同值。因此 DSN 不能代替 BDF 中的 Function Number。</p>
<details class="source-note"><summary>DSN 的精確位置</summary><p>Base 6.0 §7.9.3–§7.9.3.2，Figures 7-241–7-243、Tables 7-221／7-222，pp.1205–1207。RCiEP 與 PF／VF 有不同條件，本例不適用。</p></details></section>
<section id="meaning"><h2>讀到資料，不代表可以原樣回寫</h2>
<p>Attributes 欄必須與位元定義一起讀。RO 不表示硬體狀態永遠不變；RW1C 則在寫 1 時清除狀態，寫 0 不作用。若假設一個 4-bit 欄位全部為 RW1C，讀到 1001b，只想清 bit 0，應寫 0001b；沒有新事件時剩下 1000b。這是語義示例，不是某個真實 Register。</p>
<p>RsvdP 要保存讀值，RsvdZ 要寫 0，不能把所有 Reserved 都當成同一種欄位。存取失敗不能當成「不支援」的有效回覆；成功讀到 0 也不保證該處實作了有意義的 Register。只有在正確入口與有效結果成立後，才依格式解讀。</p>
<details class="source-note"><summary>屬性與結果邊界</summary><p>Base 6.0 §7.4、Table 7-2，pp.913–915。未實作 Register 在無其他錯誤時，設定讀取成功回 0：§7.3.3，p.913。0x100 的全零 Extended Header 表示沒有 Extended Capabilities：§7.6.1，p.1009。此規則不等同傳統 Null Capability 的 ID=0。</p></details></section>
<section id="questions"><h2>換個讀值，如何檢查理解？</h2>
<details class="question"><summary>在 0x180 讀到 0x24010003，DSN 的 Lower DW 改到 0x244 了嗎？</summary><p>沒有。0x240 是下一項的位置；目前 DSN 仍在 0x180，Lower DW 仍位於 0x184。（Figure 7-241，p.1205；Table 7-39，p.1010。）</p></details>
<details class="question"><summary>在傳統清單找不到 DSN，就能宣告不支援嗎？</summary><p>不能。DSN 在 Extended 清單，必須透過能存取該區域的介面查詢；查錯清單或無法存取，都不是有效的不存在證據。（§7.6.1，p.1009；§7.9.3，p.1205。）</p></details></section>
<p>接著讀 <a href="/DOCS/pcie-course/chapter-3.html">Chapter 3</a>，了解系統在尚不知道 BDF 時，如何建立搜尋路徑。</p>
</article>
<nav class="bottom-nav" aria-label="課程與語言版本"><a href="/DOCS/pcie-course/index.html">課程總覽</a><a href="/DOCS/pcie-course/chapter-2.html">繁中完整教學</a><a href="/pcie/chapter-2-en/">English</a></nav>
</div>
