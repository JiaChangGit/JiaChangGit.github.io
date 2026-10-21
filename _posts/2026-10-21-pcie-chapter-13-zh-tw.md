---
layout: post
title: "PCIe Chapter 13：韌體、ACPI 與 OS 的控制權"
date: 2026-10-21 00:00:00 +0800
permalink: /pcie/chapter-13-zh-tw/
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
<nav class="bottom-nav" aria-label="課程與語言版本"><a href="/DOCS/pcie-course/index.html">課程總覽</a><a href="/DOCS/pcie-course/chapter-13.html">繁中完整教學</a><a href="/pcie/chapter-13-en/">English</a></nav>
<article class="lesson">
<p class="lead">找到 PCIe 欄位，不代表目前的軟體有權設定它。韌體先建立開機環境，OS 再依平台描述與協商結果管理資源及功能。本篇分清 UEFI、ACPI、PCI Firmware 的角色，並以非零 Start Bus 的 ECAM 與 _OSC 協商案例說明常見誤判。</p><aside class="note"><strong>版本與來源</strong><p>主要依 PCI Firmware 3.3，硬體語意依 PCIe Base 6.0；Firmware 3.3 參考的 Base 版本是 5.0，兩者不是同版配套。UEFI 2.11／ACPI 6.6 只補充明列的官方索引摘錄，全文取得受限，不宣稱已完整核對。所有案例數值均為作者假設。</p></aside>
<section id="roles"><h2>依問題選擇規格</h2><div class="table-wrap"><table><caption>文件的分工</caption><thead><tr><th scope="col">文件</th><th scope="col">本篇使用範圍</th></tr></thead><tbody><tr><td>UEFI 2.11 §14</td><td>PCI Bus／Device Driver、Root Bridge I/O 與 PCI I/O 的軟體介面入口。</td></tr><tr><td>ACPI；PCI Firmware 3.3 §3–§4</td><td>Host Bridge 的平台描述、_CRS 與 _OSC，以及 PCI 專用使用規則。</td></tr><tr><td>PCIe Base 6.0</td><td>Capability、Register、事件與交易的硬體語意。</td></tr></tbody></table></div><p>UEFI 的 PCI Device Driver 在 boot services 環境透過 PCI I/O 使用控制器；PCI Bus Driver 建立控制器的 device handles。Root Bridge I/O 則是追查整條 bus 存取抽象的入口。這些介面不取代晶片組相依的枚舉細節，也不表示 OS native driver 就是 UEFI driver。</p><details class="source-note"><summary>UEFI 補充的核對邊界</summary><p><a href="https://uefi.org/sites/default/files/resources/UEFI_Spec_Final_2.11.pdf">UEFI 2.11</a> §14.3.7–§14.4（文件 p.623）由官方索引摘錄核對；介面章節位置見 <a href="https://uefi.org/specs/UEFI/2.11/">2.11 目錄</a>。全文回覆 403，不以未讀部分推定額外規範。</p></details></section>
<section id="handoff"><h2>交接不保證每個裝置都已配置</h2><p>Firmware §3.5 要求韌體配置所有 Host Bridges，以及通往開機／主控台裝置的 PCI-to-PCI Bridges；OS 不能假定其他路徑也都完成。UEFI drivers／applications 不得自行變更由韌體配置者持有的 BAR／Bridge 配置。OS 判讀既有 BAR，仍需對應 Enable 與平台轉譯資訊，CPU 位址未必等於 BAR。</p><p>Host Bridge 在 ACPI namespace 中提供 _HID／_CID、_CRS 等描述，並依條件提供 _SEG 等資訊。Segment 與 BDF 須一起辨識目標；namespace 路徑不是 BDF。依據：PCI Firmware 3.3 §3.5（pp.34–37）、§4.1.5（pp.45–46）；BAR 細節見 <a href="/pcie/chapter-4-zh-tw/">Chapter 4</a>。</p></section>
<section id="address"><h2>MCFG 提供設定存取位置，_CRS 限定資源範圍</h2><div class="table-wrap"><table><caption>非零 Start Bus 的作者案例</caption><thead><tr><th scope="col">項目</th><th scope="col">值</th></tr></thead><tbody><tr><td>MCFG Base Address／Segment</td><td>0xE0000000／0x0002</td></tr><tr><td>Start Bus／End Bus</td><td>0x40／0x4F</td></tr><tr><td>Bus／Device／Function／Offset</td><td>0x42／0x03／0x01／0x180</td></tr><tr><td>設定存取位址</td><td>0xE4219180</td></tr></tbody></table></div><p>先選對 Segment entry、確認目標 Bus 在範圍內，再以 Bus 0 為基準計算：<code>0xE0000000 + (0x42 &lt;&lt; 20) + (0x03 &lt;&lt; 15) + (0x01 &lt;&lt; 12) + 0x180 = 0xE4219180</code>。這個 entry 涵蓋 0xE4000000–0xE4FFFFFF，共 16 MiB；不能先減 Start Bus 而算成 0xE0219180，也不能推定 Base 到實際範圍之前的區域可用。</p><p>假設 _CRS 提供下游 Memory 範圍 0x90000000–0x90FFFFFF、無轉譯；BAR 仍須檢查大小、對齊、占用與沿途視窗。ECAM 不是可分配給 BAR 的資源池。MCFG 與 Host Bridge 熱加入時的 _CBA 也有不同用途，不要混成一般 Endpoint 熱插入。</p><details class="source-note"><summary>閱讀路徑</summary><p>Firmware Table 4-1（p.39）→ Tables 4-2、4-3（pp.41–42）→ §4.1.4（pp.44–45）。_CBA 見 §4.1.3（pp.42–44）；_CRS 見 §3.5（pp.35–37）、§4.3.2（p.47）。</p></details></section>
<section id="osc"><h2>宣告支援、要求控制與實際授權是三件事</h2><p>PCI Host Bridge 的 _OSC 涵蓋該 Host Bridge 所起始的 hierarchy。Firmware §4.5.1 定義 UUID=<code>33DB4D5B-1FF7-401C-9657-7441C03DD766</code>、Revision=1、三 DWORD Buffer。DWORD 1 放通用 Query／回傳資訊；DWORD 2 是 OS 單向宣告的 Support Field，回傳修改不作授權；DWORD 3 是 Control 請求與回覆。</p><p>送入 DWORD 1 bit 0=1 是 Query，清除才要求接管；回傳 bit 0 是 Reserved。回傳 bit 1、2、3 分別是處理失敗、UUID 不識別、Revision 不識別，bit 4 是 Capabilities Masked。發生錯誤時，不可把保留的 Control bit 當成成功授權。</p><p>授權 1 不證明每個裝置都有該能力；回傳 0 也不等於硬體沒有實作。韌體不能只因自己未支援功能就任意拒絕；應有明確的平台不相容依據。OS 仍須查每個 Slot／Function。</p><details class="source-note"><summary>介面與通用欄位</summary><p>Firmware §4.5.1（pp.48–49）、Tables 4-4–4-6（pp.49–58）。通用 bit 定義補充依 <a href="https://uefi.org/sites/default/files/resources/ACPI_Spec_6.6.pdf">ACPI 6.6 §6.2.12</a>官方索引摘錄（文件 p.401）；全文未取得，不延伸到其他 ACPI 行為。Firmware §4.5.3（pp.61–62）亦示範 0x10 遮罩回報。</p></details></section>
<section id="negotiation"><h2>用相依條件解讀一次完整協商</h2><p>本例要求 native Hot-Plug bit 0、native PME bit 2、AER bit 3、PCI Express Capability Structure bit 4 與 DPC bit 7，Control=0x9D。DPC 還要求 Support bit 7 的 Error Disconnect Recover（EDR）支援。Support=0x9F 宣告 bits 0–4 與 bit 7：Extended Config operation regions、ASPM、Clock PM、Segment Groups、MSI、EDR。未請求 LTR、Completion Timeout 或 SFI。</p><p>Hot-Plug、PME、AER 需搭配 Control bit 4；DPC 另需 Control bit 3。韌體保留 DPC 時必須保留 AER；授予 DPC 則須同時授予 AER 與 Capability。bit 4 的概括名稱不能推翻個別控制權。Support ASPM 也不等於 Control PME，更不替代 L1.2 的硬體、時序與 LTR 條件。</p><div class="table-wrap"><table><caption>假設平台保留 AER／DPC 的三次呼叫</caption><thead><tr><th scope="col">階段</th><th scope="col">輸入 DWORD 1／Control</th><th scope="col">回傳 DWORD 1／Control</th></tr></thead><tbody><tr><td>第一次 Query</td><td>0x00000001／0x0000009D</td><td>0x00000010／0x00000015</td></tr><tr><td>調整後 Query</td><td>0x00000001／0x00000015</td><td>0x00000000／0x00000015</td></tr><tr><td>正式接管</td><td>0x00000000／0x00000015</td><td>0x00000000／0x00000015</td></tr></tbody></table></div><p>Support 始終為 0x0000009F；假設平台已知 native DPC 有相容性問題，沒有其他錯誤或先前授權。<code>0x9D &amp; ~0x15 = 0x88</code> 表示 AER／DPC 被遮罩。Query 不得因呼叫改動硬體；規格強烈建議 Query 到不再 Mask。第二列仍不是接管，第三列才按有效結果轉移 Hot-Plug、PME 與相應 Capability 的控制權。</p><details class="source-note"><summary>相依與呼叫順序</summary><p>Firmware Tables 4-4–4-6（pp.49–58）、§4.5.2（pp.59–60）、§4.5.3（pp.61–62）。本例政策是作者假設，不是複製規格 ASL 平台範例。</p></details></section>
<section id="ownership"><h2>交接後的責任，以及有限的 EDR 例外</h2><p>授予 Hot-Plug 時，韌體須安排原生事件路由，之後不再更新插槽指示燈與電源狀態；PME 也有相應路由與 Register 限制。同次開機、同一 Host Bridge 的後續呼叫須保留已宣告支援與已取得的請求，韌體不能收回已授權項目；Firmware 3.3 沒有讓 OS 自行放棄已取得控制權的機制。</p><p>未獲 AER／DPC 控制權，不能任意改 Mask、Severity 或 DPC Control；但 Table 4-6 定義 EDR 協作例外。從 EDR Notify 到呼叫 _OST 前，OS 可處理觸發 Port 的指定 Device／AER／RP PIO Status，並可寫 DPC Trigger Status；處理其後 Trigger 仍為 1 的下游熱移除時，也允許處理該 Trigger。對應 _OST 返回後，到下游 Function 重新初始化完成或停用前，又有針對下游指定 DPC／Device／AER Status 的有限權限。各期間韌體須遵守對應的禁止寫入規則。</p><p>這不是交出完整 DPC Configuration，也不免除 Link inactive／適用 RP Busy 等硬體條件。完整判讀要同時確認對象、時間窗、通知與 _OST；沒有 _OSC 時，OS 不得啟用該介面定義的功能。</p><details class="source-note"><summary>責任與恢復例外</summary><p>Firmware Table 4-6（pp.53–57）、§4.5.2.2–§4.5.2.3（p.59）、§4.5.1（p.49）。連讀 <a href="/pcie/chapter-11-zh-tw/">Chapter 11</a> 的插槽能力及 <a href="/pcie/chapter-12-zh-tw/">Chapter 12</a> 的隔離條件。</p></details></section>
<section id="questions"><h2>確認三類證據沒有混用</h2><details class="question"><summary>Support bit 7=1 就代表 DPC 歸 OS 管理嗎？</summary><p>沒有；它宣告 EDR 支援，仍需合法 Control 請求、相依功能及非 Query 的有效授權。依據：Tables 4-4–4-6。</p></details><details class="question"><summary>MCFG 存取成功、_OSC 也成功，可以忽略 _CRS 不足嗎？</summary><p>不能。設定存取、控制權與資源容量是不同問題。依據：Firmware §3.5、§4.1、§4.5。</p></details></section>
</article>
<nav class="bottom-nav" aria-label="課程與語言版本"><a href="/DOCS/pcie-course/index.html">課程總覽</a><a href="/DOCS/pcie-course/chapter-13.html">繁中完整教學</a><a href="/pcie/chapter-13-en/">English</a></nav>
</div>
