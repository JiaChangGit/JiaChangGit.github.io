---
layout: post
title: "PCIe Chapter 7：中斷如何把事件交給軟體"
date: 2026-10-21 00:00:00 +0800
permalink: /pcie/chapter-7-zh-tw/
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
<nav class="bottom-nav" aria-label="課程與語言版本"><a href="/DOCS/pcie-course/index.html">課程總覽</a><a href="/DOCS/pcie-course/chapter-7.html">繁中完整教學</a><a href="/pcie/chapter-7-en/">English</a></nav>
<article class="lesson">
<p class="lead">中斷讓軟體知道有事待處理；事件的內容與數量仍由裝置介面提供。本章從 MSI-X Capability 算出 Table 與 entry 位址，再追蹤遮罩、Pending 和中斷 Memory Write，避免把支援能力、啟用與實際通知混為一談。</p>
<p><a href="/DOCS/pcie-course/chapter-7.html">完整中文教學</a> · <a href="/DOCS/pcie-course/index.html">課程路線</a> · <a href="/pcie/chapter-7-en/">English</a></p>
<aside class="note"><strong>版本與案例</strong><p>依 Base 6.0，普通 Endpoint 03:00.0，MSI-X Capability=0xD0、BAR0=0x80004000，大小 16 KiB。不使用 SR-IOV、Enhanced Allocation 或 TPH；Non-Flit Mode，資料與中斷均為 TC0、IDO=0。MSE／BME、平台映射及中斷接收資源均已準備好。數值與初始化安排為作者推演。</p></aside>
<section id="mechanisms"><h2>MSI-X 的 Message 實際上是 Memory Write</h2>
<p>INTx 用 Assert_INTx／Deassert_INTx Message 模擬電位式中斷；MSI 與 MSI-X 則把系統指定的 DWORD 資料寫到指定位置，使用 MWr 而非 Msg／MsgD，也沒有普通 Completion。能產生中斷的 Function 必須支援 MSI、MSI-X 或兩者，INTx 則為可選相容機制。MSI 與 MSI-X 不得同時啟用；使用其中一者時，也不得用 INTx 要求服務。</p>
<p>獨立的 MSI 對照案例：ID=0x05，Message Control 讀回 0x0184，代表 MMC=010b、要求 4 個向量，MME=000b、MSI 尚未啟用；支援 64-bit Address 與 PVM，不支援 Extended Message Data。系統可在 MSI 關閉時配置 2 個向量，MME=001b，再完成其餘設定並啟用。MSI 最多 32 個、採 2 的冪次編碼；MSI-X 的 Table Size 則使用 N−1。</p>
<details class="source-note"><summary>機制與 MSI 入口</summary><p>§6.1–§6.1.4.4（pp.659–664）；Figures 7-44–7-47（pp.1011–1012）、Figure 7-49／Table 7-41（pp.1013–1014）。普通 PCI Express Endpoint 實作 MSI 時須支援 64-bit Message Address。上述 MSI 例子不代表主案例另有一個 MSI Capability。</p></details></section>
<section id="locate"><h2>由 Capability 找到 Memory Space 的 Table</h2>
<div class="table-wrap"><table><caption>主案例的設定讀值</caption><thead><tr><th scope="col">位移與寬度</th><th scope="col">讀值</th><th scope="col">解碼</th></tr></thead><tbody><tr><td>0xD0，16 bits</td><td>0x0011</td><td>ID=0x11、Next=0。</td></tr><tr><td>0xD2，16 bits</td><td>0x0007</td><td>8 個 entries，Enable=0、Function Mask=0。</td></tr><tr><td>0xD4，32 bits</td><td>0x00002000</td><td>Table BIR=0、位移 0x2000。</td></tr><tr><td>0xD8，32 bits</td><td>0x00003000</td><td>PBA BIR=0、位移 0x3000。</td></tr></tbody></table></div>
<p>低 3 bits 的 BIR 選 BAR，遮掉低 3 bits 後就是 byte 位移，不再左移。因此 Table base=0x80006000，8 × 16 bytes 的 Table 占 0x80006000–0x8000607F；PBA base=0x80007000，所需的 1 個 QWORD 占 0x80007000–0x80007007。兩者均在 BAR0 內且不重疊。本例把一般 Register 與 MSI-X 結構分到不同的自然對齊 4 KiB 頁面。</p>
<p>Entry 3 是第四個 entry，起點為 0x80006000 + 3 × 16 = 0x80006030。它在 +0x00、+0x04、+0x08、+0x0C 分別保存 Message Address、Upper Address、Data、Vector Control。本例依序為 0xFEE01000、0x00000000、0x00000045、初始 0x00000001。設定時保留其他 Vector Control bits，只在適當時機清 Mask bit。</p>
<p>Entry 位址與訊息目標不同：裝置最後向平台指定的 0xFEE01000 寫入 0x00000045，四個 bytes 全部有效，不修改 Data 低位元。0x45 不是 Table index，本例也不替它定義 CPU 編號或中斷控制器編碼。RO／No Snoop 必須為零。</p>
<details class="source-note"><summary>逐步閱讀路線</summary><p>Figure 7-56（p.1018）→ Figure 7-60／Table 7-49（p.1022）→ Figures 7-61／7-62、Tables 7-50／7-51（pp.1023–1024）→ Figures 7-57／7-58（p.1019）、Equations 7-1／7-2（p.1021）→ Tables 7-52–7-55（pp.1024–1026）。頁面隔離見 p.1020；訊息屬性見 p.661。64-bit BAR 的 BIR 必須指向低 DWORD。</p></details></section>
<section id="configure"><h2>先控制通知，再開放 entry</h2>
<p>作者採用的初始化安排是：裝置事件尚未活動時，系統軟體先設 Function Mask，Control 讀回 0x4007；在 entry Mask=1 時填入有效 Address／Data；啟用 MSI-X 並保持全域遮罩，讀回 0xC007；依平台 I/O 規則確認設定可見，再清 entry 3 Mask 和 Function Mask，最後讀回 0x8007。其他 entries 保持遮罩，通知路徑準備好後才啟動工作。</p>
<p>這不是唯一合法序列。MSI/MSI-X Message Control 的 RW 欄位由系統軟體管理，規格不允許裝置驅動程式直接修改。Table／PBA 存取必須為對齊的完整 DWORD 或 QWORD；不得在未遮罩 entry 上修改 Address／Data／適用的 Steering Tag。遮罩原本未遮罩的 entry 時，應先用 DWORD 更新 Vector Control，不能同時用 QWORD 更改 Data 與 Mask。</p>
<details class="source-note"><summary>條件來源</summary><p>§6.1.4.2–§6.1.4.5（pp.662–665）；存取對齊見 p.1020；控制權見 pp.1013、1022；Reserved 保存見 Table 7-55（p.1026）。Function Mask 不改變各 entry 自己的 Mask。</p></details></section>
<section id="pending"><h2>Pending 表示待送訊息，不記錄事件次數</h2>
<p>MSI-X 已啟用而 entry 3 被有效遮罩時，若發生原應通知的事件，裝置必須設 PBA bit 3，且不得送訊息。若其餘 bits 為零，本例 QWORD 讀回 0x0000000000000008；多次事件仍可能是相同值。事件仍待處理時解除遮罩，裝置必須安排傳送，送出後清 Pending；若底層事件已在遮罩期間被滿足，則須先清 Pending，避免不必要通知。</p>
<p>軟體應只讀、不寫 Pending bits；寫入結果未定義，不能當成 RW1C。PBA=0 也不表示 CPU 已服務完成。同一向量多次通知不保證逐筆各獲服務，事件計數與交握須由裝置介面處理。</p>
<p>本例同一 Function 的資料寫入與 MSI-X 同為 TC0，因此中斷寫入不得越過先前 Posted 寫入；系統須保證中斷處理常式能觀察到先於該訊息抵達的更新，不必為了沖出那些寫入再讀裝置 Register。Chapter 6 的映射與同步前提仍適用。不同 TC 要另外同步；訊息抵達順序不保證服務順序，也沒有固定延遲保證。</p>
<details class="source-note"><summary>Pending 與順序來源</summary><p>§6.1.4.5–§6.1.4.7（pp.664–667）；Table 7-56（p.1027）。跨 TC 同步見 p.661，延遲見 p.660。共用向量時讀裝置狀態辨識來源，與前述資料 flush 是不同用途。</p></details></section>
<section id="checks"><h2>確認條件是否足夠</h2><details class="question"><summary>有 8 個 Table entries，就已配置 8 個不同向量嗎？</summary><p>沒有。Table Size 是容量；系統可配置較少向量，甚至讓多個 entries 共用同一 Address／Data。</p></details><details class="question"><summary>entry Mask=0，但 Function Mask=1，可以通知嗎？</summary><p>不行。Function Mask 使所有 entries 按遮罩處理，不會替它們改寫各自的 Mask bit。</p></details></section>
<p>下一階段將說明 Link 建立與可靠傳遞。查核日期：2026-10-21；來源頁碼為 Base 6.0 文件／PDF 頁碼。</p>
</article>
<nav class="bottom-nav" aria-label="課程與語言版本"><a href="/DOCS/pcie-course/index.html">課程總覽</a><a href="/DOCS/pcie-course/chapter-7.html">繁中完整教學</a><a href="/pcie/chapter-7-en/">English</a></nav>
</div>
