---
layout: post
title: "PCIe Chapter 12：錯誤證據、回報與隔離"
date: 2026-10-21 00:00:00 +0800
permalink: /pcie/chapter-12-zh-tw/
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
<nav class="bottom-nav" aria-label="課程與語言版本"><a href="/DOCS/pcie-course/index.html">課程總覽</a><a href="/DOCS/pcie-course/chapter-12.html">繁中完整教學</a><a href="/pcie/chapter-12-en/">English</a></nav>
<article class="lesson">
<p class="lead">PCIe 錯誤判讀需要串起偵測、回報、接收與隔離的證據。Status 記錄錯誤，不保證訊息送達；Source ID 識別回報者，不直接指出根本原因。本篇以 AER 與 DPC 的兩個獨立案例說明這些界線。</p><aside class="note"><strong>版本與假設</strong><p>依 PCIe Base 6.0，所有值與事件順序均為作者設計，使用普通非 SR-IOV Function。AER 案例不支援 Flit Mode／End-End TLP Prefix，且未啟用 DPC；後面的 DPC 是另一事件。假設管理者有相應權限，讀取期間沒有未說明的新事件。</p></aside>
<section id="model"><h2>先建立從 Function 到 Root 的證據關係</h2><p>Correctable Error 可由協定恢復，但可能影響效能。Uncorrectable Error 影響功能，並依嚴重程度分為 Non-Fatal／Fatal；Non-Fatal 不能解成工作已成功，Fatal 也不是某顆晶片損壞的直接診斷。AER 提供比基本錯誤回報更細的狀態、遮罩、嚴重程度與 Log；沒有 AER 不等於完全沒有錯誤回報。</p><p>依序查看來源 Function 的 Status、偵測當時的 Mask／Severity／Device Control、有效 Header Log，再到 Root Error Status／Source ID 比對。若可能有隔離，另查 DPC Status。不同時間的設定不能自動套回事發時刻。依據：§6.2.1–§6.2.4（pp.669–679）、Figure 6-1（p.670）。</p></section>
<section id="aer"><h2>兩個 Status bit，只有一個未被遮罩</h2><p>在 03:00.0 走訪 Extended Capability 清單，依 Figure 7-154 找到 AER ID=0x0001。本例 base=0x100，Version=2、Next=0；不能把 Base 6.0 的所有 Flit 欄位都當成這個 Function 的能力。假設先前紀錄已清、設定自事件前未變，沿途轉送條件已啟用。</p><div class="table-wrap"><table><caption>來源 Function 的讀值</caption><thead><tr><th scope="col">Register／位置</th><th scope="col">值</th><th scope="col">判讀</th></tr></thead><tbody><tr><td>Header／0x100</td><td>0x00020001</td><td>AER，Version 2。</td></tr><tr><td>Uncorrectable Status／0x104</td><td>0x00044000</td><td>Completion Timeout bit 14、Malformed TLP bit 18。</td></tr><tr><td>Mask／0x108</td><td>0x00040000</td><td>只遮罩上述 Malformed TLP。</td></tr><tr><td>Severity／0x10C</td><td>0x00040000</td><td>Timeout 為 Non-Fatal；Malformed 為 Fatal。</td></tr><tr><td>AER Capabilities and Control／0x118</td><td>0x0000100E</td><td>FEP=14、Timeout Header Log Capable=1。</td></tr><tr><td>Device Control／0x78，16 bits</td><td>0x2816</td><td>Non-Fatal／Fatal Reporting Enable 均為 1。</td></tr></tbody></table></div>
<p><code>0x00044000 &amp; ~0x00040000 = 0x00004000</code>，本例只有 Timeout 未遮罩。Masked error 仍能設定 Status，但不為該次錯誤送出 Error Message，也不寫入 Header Log、TLP Prefix Log 或 FEP。Fatal Severity 不會越過 Mask。本例 Timeout 依 Severity 與 Device Control 產生 ERR_NONFATAL；這些值是設定後快照，不是預設值。</p><p>完整回報還有沿途 Bridge、Root primary interface 與中斷條件。依 Figure 6-3 查整條路徑；Unsupported Request／Advisory Non-Fatal 另有規則，不能普遍套用本例運算。</p><details class="source-note"><summary>欄位與回報來源</summary><p>Figures 7-154–7-157／Tables 7-134–7-137（pp.1112–1117）；Figure 7-25／Table 7-21（pp.958–962）；§6.2.3.2.2（p.673）、§6.2.6／Figure 6-3（pp.683–685）、§6.2.8.1（p.692）。</p></details></section>
<section id="log"><h2>先確認 Log 有效，再解碼交易</h2><p>FEP=14 且 Status bit 14=1，因此 FEP 有效。Completion Timeout Header Log Capable bit 12=1 才支持本例記下超時 Request；Multiple Header Recording bits 9、10=0，沒有 Flit／Prefix。本例用四 DWORD Log 容量，並只解讀三 DWORD Header。</p><div class="table-wrap"><table><caption>Timeout 所對應的 Request Header</caption><thead><tr><th scope="col">位置</th><th scope="col">DWORD 值</th><th scope="col">內容</th></tr></thead><tbody><tr><td>0x11C</td><td>0x00000040</td><td>3 DW Memory Read，Length=64 DW。</td></tr><tr><td>0x120</td><td>0x030013FF</td><td>Requester=0x0300、Tag=0x13、兩個 Byte Enable 均為 0xF。</td></tr><tr><td>0x124</td><td>0x40001000</td><td>起始位址。</td></tr><tr><td>0x128</td><td>不解讀</td><td>12-byte Header 的第四個 DWORD 未定義。</td></tr></tbody></table></div><p>Request 範圍為 0x40001000–0x400010FF，共 256 bytes；記錄的是未如期完成的 Request，不是超時的 Completion。Figure 7-161 的 DWORD 排列把 Header byte 0 放在 bits 31:24，不能再把上表反轉一次。Flit Log 須改查 Logged TLP was Flit Mode、Header Log Size、Logged TLP Size 與 Type／OHC。</p><p>Log 只能定位交易與等待結果，不能單獨指定 Endpoint、Completer、Link 或平台誰造成問題。它也不能分配給已 Mask、沒有本次 Log 的 Malformed TLP。</p><details class="source-note"><summary>有效性與格式</summary><p>§6.2.4.2（pp.679–680）；Figures 7-160、7-161／Tables 7-140、7-141（pp.1121–1123）；Memory Request 格式見 <a href="/pcie/chapter-5-zh-tw/">Chapter 5</a>。</p></details></section>
<section id="root"><h2>Root 的 Source ID 是第一個回報者</h2><div class="table-wrap"><table><caption>同一 AER 案例的 Root Port 快照</caption><thead><tr><th scope="col">Root AER base=0x100</th><th scope="col">值</th><th scope="col">意義</th></tr></thead><tbody><tr><td>Root Error Command／0x12C</td><td>0x00000002</td><td>Non-Fatal 中斷回報啟用。</td></tr><tr><td>Root Error Status／0x130</td><td>0x00000024</td><td>Uncorrectable Received 與 Non-Fatal Received。</td></tr><tr><td>Error Source ID／0x134</td><td>0x03000000</td><td>高 16 bits 為 0x0300，即 03:00.0。</td></tr></tbody></table></div><p>本例 Root 中斷向量編號為 0，且 primary interface 傳送條件已滿足。Source ID 表示回報 Timeout 的 Endpoint，不等於物理故障根因。第二個同類訊息會設 Multiple bit，但不取代第一個 Source ID。</p><p>Root Status 更新不受 Root Error Command／Root Control 控制，仍需要適用的 primary interface 傳送允許。要證明 CPU 收到中斷，還需向量與路由證據。依據：Figures 7-162–7-164／Tables 7-142–7-144（pp.1123–1127）。</p></section>
<section id="preserve"><h2>清除前，先保存能互相比對的紀錄</h2><p>作者建議先保存狀態、設定、FEP、有效 Log 與 Root／DPC 證據，並確認並行變化；多個 Register 的讀取不是自動原子快照。清除 FEP 指向的 Status 後，硬體可能換入下一筆 Log，所以先清再讀會破壞關聯。</p><p>啟用 Multiple Header Recording 且 FEP 有效時，規格建議依 FEP 逐筆處理，不清其他 Status；確定沒有 Header 的 masked error 有列明例外。PCI Status 與 AER Status 也不會互相連帶清除。依據：§6.2.4.2（pp.679–681，註腳 108）、§6.2.7.1（p.691）。</p></section>
<section id="dpc"><h2>DPC 可能在 Root 收到原訊息之前隔離</h2><p>換成另一事件：Switch Downstream Port 02:01.0 有 DPC base=0x300，不使用 RP Extensions。</p><div class="table-wrap"><table><caption>獨立 DPC 案例</caption><thead><tr><th scope="col">欄位／位置</th><th scope="col">值</th><th scope="col">意義</th></tr></thead><tbody><tr><td>Header／0x300</td><td>0x0001001D</td><td>ID=0x001D、Version=1。</td></tr><tr><td>Control／0x306，16 bits</td><td>0x000A</td><td>Trigger Enable=10b，Interrupt Enable=1。</td></tr><tr><td>Status／0x308，16 bits</td><td>0x000B</td><td>Triggered、Reason=01b、Interrupt Status=1。</td></tr><tr><td>Error Source ID／0x30A，16 bits</td><td>0x0300</td><td>觸發的 ERR_NONFATAL 來自 03:00.0。</td></tr></tbody></table></div>
<p>Enable=10b 可因本地未遮罩 Uncorrectable Error 或收到 ERR_NONFATAL／ERR_FATAL 觸發。此例 Reason=01b，Source ID 因而有效；若 Reason=00b，不能用 Source ID 判來源。觸發訊息在 Port 被丟棄，不再向 Root 轉送。本例只開 DPC 中斷、未開 DPC ERR_COR，所以不能要求 Root 出現前例的 0x24。</p><p>DPC 使下游 Link 進 Disabled。釋放前必須讀到 Link Active=0；若是有 RP Extensions 的 Root Port，還須等 RP Busy=0。Switch Port 的 RP Busy 是 Reserved。清 Interrupt Status 只是確認通知；清 Trigger Status 才釋放 DPC，讓 Link 回 Detect。之後設定存取仍須遵守 Conventional Reset 時序，並由軟體完成恢復，不能把 Trigger 清除視為應用工作成功。</p><details class="source-note"><summary>隔離與釋放</summary><p>§6.2.11–§6.2.11.2（pp.694–697）；Figures 7-297–7-301／Tables 7-261–7-265（pp.1248–1254）。所有權接 <a href="/pcie/chapter-13-zh-tw/">Chapter 13</a>。</p></details></section>
<section id="questions"><h2>確認證據的限制</h2><details class="question"><summary>FEP=14，但 Status bit 14=0，還能用 Log 指認最新 Timeout 嗎？</summary><p>不能，FEP 已無效。非零 Log 不能取代有效條件。依據：§6.2.4.2。</p></details><details class="question"><summary>Status=0 能否證明從未發生錯誤？</summary><p>不能；狀態可能已清除或重設，也須考慮偵測與實作條件。依據：§6.2.4.2、Table 7-135。</p></details></section>
</article>
<nav class="bottom-nav" aria-label="課程與語言版本"><a href="/DOCS/pcie-course/index.html">課程總覽</a><a href="/DOCS/pcie-course/chapter-12.html">繁中完整教學</a><a href="/pcie/chapter-12-en/">English</a></nav>
</div>
