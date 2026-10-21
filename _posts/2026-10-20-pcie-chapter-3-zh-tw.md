---
layout: post
title: "PCIe Chapter 3：從未知拓樸到完成裝置發現"
date: 2026-10-20 00:00:00 +0800
permalink: /pcie/chapter-3-zh-tw/
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

html:not([data-theme="dark"]) .pcie-article { color-scheme: light; }
html[data-theme="dark"] .pcie-article { color-scheme: dark; }

.pcie-article { background: transparent; margin: 1.5rem 0; }
.pcie-article .lesson { padding: 0; border: 0; background: transparent; }
</style>
<div class="pcie-article" lang="zh-Hant-TW">
<nav class="bottom-nav" aria-label="課程與語言版本"><a href="/DOCS/pcie-course/index.html">課程總覽</a><a href="/DOCS/pcie-course/chapter-3.html">繁中完整教學</a><a href="/pcie/chapter-3-en/">English</a></nav>
<article class="lesson">
<p class="lead">枚舉要先建立可走的設定路徑，才能找到下游 Function。讀到某個值時，也必須分清有效身分、暫時未就緒，以及存取失敗。本章把 Bridge 的 Bus Number 配置與這些結果放在同一個流程中。</p>
<p><a href="/DOCS/pcie-course/chapter-3.html">完整中文教學</a> · <a href="/DOCS/pcie-course/index.html">課程路線</a> · <a href="/pcie/chapter-3-en/">English</a></p>
<aside class="note"><strong>版本與教學前提</strong><p>欄位與交易依 Base 6.0；平台與交接依 PCI Firmware 3.3，後者並非 Base 6.0 的同版配套。以下為作者推演，不是實機操作。採傳統 BDF，不用 ARI、SR-IOV 或 FPB。平台提供 Segment 0000、Bus 00–3F，Root Port 00:01.0 已可存取，連線與等待條件已滿足；軟體獨占這段配置，沒有其他階層競爭 Bus Number。文件頁與 PDF 頁序相同。</p></aside>
<section id="entry"><h2>平台提供起點，Function 讀值提供下一步證據</h2>
<p>系統先從平台取得 Host／Root Bridge 的 Segment、Bus 範圍與設定存取介面，不是任意掃描實體記憶體。Root Bridge 的平台介面與 Root Port 的對外 Link 角色不同。Firmware 3.3 要求韌體配置所有 Host Bridge，讓 OS 能處理其下游裝置。</p>
<p>探查 Function 時，Vendor ID 是規格建議的存在性線索，FFFFh 表示沒有 Function。但軟體可見資料不等於 Completion payload：對依賴全 1 回覆的軟體，Root Complex 會把 Configuration Request 的 UR 結果合成全 1。讀取失敗或路徑尚未建立，則不能只憑任意 buffer 值判定實體卡不存在。</p>
<details class="source-note"><summary>來源</summary><p>Firmware 3.3 §3.1.1，p.32；§3.5，pp.34–35。Base 6.0 Vendor ID：§7.5.1.1.1，p.917；未實作目標與 UR：§7.3.1，p.911；全 1 資料合成：§2.3.2，p.221。</p></details></section>
<section id="rrs"><h2>0xFFFF0001 不是一般的 Vendor／Device ID</h2>
<p>RRS（Request Retry Status）是 Base 6.0 用來表示指定情況下暫時不能處理要求的狀態。它只在適用的 Reset／Readiness 條件下合法，不能當作任何時刻通用的忙碌回覆。</p>
<aside class="example"><strong>另一個尚未就緒的情境</strong><p>假設目標剛經過允許回 RRS 的 Reset，尚未成功完成後續設定要求，也沒有 Configuration-Ready、Immediate Readiness 或其他禁止條件。Root Port 以自身控制位管理可見性，PCIe Capability 起點已查得為 0x70。這個情境獨立於下節的正常枚舉。</p></aside>
<div class="table-wrap"><table><caption>先查能力與設定，再解讀合成資料</caption><thead><tr><th scope="col">讀取</th><th scope="col">假設值</th><th scope="col">意義</th></tr></thead><tbody><tr><td>Root Capabilities：0x8E，16 bits</td><td>0x0001</td><td>bit 0 支援 Configuration RRS Software Visibility。</td></tr><tr><td>Root Control：0x8C，16 bits</td><td>0x0010</td><td>bit 4 已啟用可見性。</td></tr><tr><td>目標 offset 0x00，32 bits</td><td>0xFFFF0001</td><td>Root Complex 收到 RRS 後，合成 Vendor ID 0001h，其餘 bytes 全 1。</td></tr></tbody></table></div>
<p>讀取必須涵蓋 Vendor ID 的兩個 bytes；若只讀這個 16-bit 欄位，特殊值是 0001h。這不是已配發的 Vendor ID。未啟用可見性或讀取其他位置時，不應期待相同資料格式，適用時由 Root Complex 重新發出要求。等待期限仍須依 Reset、Readiness 與平台策略判斷，不能假設所有情況都等同一個固定時間。</p>
<details class="source-note"><summary>查詢路線</summary><p>Figure 7-21（p.952）定位 +1Eh／+1Ch；Figure 7-34／Table 7-31（p.988）查能力，Figure 7-33／Table 7-30（pp.986–988）查設定。RRS 條件：§2.3.1，pp.211、214；合成值與重試規則：§2.3.2，pp.220–221。</p></details></section>
<section id="walk"><h2>先開放可能的下游範圍，再回填實際結果</h2>
<p>本例採先走完一個分支再返回的搜尋策略，暫以平台授予的 3F 作 Subordinate 上限，完成後縮回實際範圍。這是教學策略，不是所有平台唯一的程序。</p>
<div class="table-wrap"><table><caption>Bus Number 配置的教學順序</caption><thead><tr><th scope="col">順序</th><th scope="col">動作</th></tr></thead><tbody><tr><td>1</td><td>Root Port 00:01.0 設 Secondary=01、Subordinate=3F。</td></tr><tr><td>2</td><td>找到 01:00.0 的 Switch Upstream Port，設 Secondary=02、Subordinate=3F。</td></tr><tr><td>3</td><td>找到 02:01.0 的 Downstream A，設 Secondary=03、Subordinate=3F。</td></tr><tr><td>4</td><td>確認 03:00.0 與 03:00.1；本分支完成後，A 的 Subordinate 改為 03。</td></tr><tr><td>5</td><td>回到 Bus 02，替 02:02.0 的 Downstream B 設 Secondary=04、Subordinate=3F。</td></tr><tr><td>6</td><td>確認 04:00.0；B 的 Subordinate 改為 04，最後 Upstream Port 與 Root Port 也改為 04。</td></tr></tbody></table></div>
<p>03:00.0 的 Header Type=80h 只允許探查其他 Function；Function 1 存在是另一筆有效結果。04:00.0 的 Header Type=00h，且無其他機制指示，因此不得一律掃描 Function 1–7。本例的普通 Link 對端用 Device 0，Switch 內部 Downstream Port 則可出現在其他 Device Number。</p>
<p>讀 Figure 7-14 找 Secondary／Subordinate 的 0x19／0x1A，各讀寫 8 bits，再依 p.937 的定義使用。設定寫入必須完成，才能使用新路徑；本例不以 Primary Bus Number 推導 Bridge 自身 BDF。平台若有保留需求，也不一定要把最後的上限縮到 04。</p>
<details class="source-note"><summary>來源</summary><p>Base 6.0 §7.5.1.3，Figure 7-14，p.936；§7.5.1.3.2–§7.5.1.3.4，p.937；Header Type：Table 7-7，p.925；Device Number：§7.3.1，p.911；ECAM 寫入完成保障：p.908。</p></details></section>
<section id="routing"><h2>Header 的 Type 與要求封包的 Type，必須分開</h2>
<p>Configuration Header Type 1 描述 Bridge 的標頭格式；Configuration Request Type 1 則用於向更深層路由。對目標 03:00.1，Root Port 的下一層 Bus 是 01，因此仍以 Type 1 往 Switch 送；Switch 判定 Bus 03 正是 Downstream A 的下一層，再轉為 Type 0 送到 Endpoint。對 Bridge 自身設定空間的有效 Type 0 Request，同樣可以由 Bridge 處理。</p>
<p>本例描述對外路由結果，不假設 Switch 的內部邏輯 Bus 是另一條實體 PCIe Link。若目標不在有效範圍，則依 UR 規則處理。（Base 6.0 §7.3.2–§7.3.3，pp.912–913。）</p></section>
<section id="finish"><h2>找到 BDF 後，仍未完成資源與工作設定</h2>
<p>枚舉結果提供 Function 清單、橋接路徑與身分線索，不能直接證明 MMIO 或 DMA 已可用。Firmware 3.3 §3.5（pp.34–35）要求開機／主控台路徑及所有 Host Bridge 完成指定配置，其他裝置可留給 OS；不能只因任意 Endpoint 尚未配置就宣告韌體違規。</p>
<details class="question"><summary>讀到 0xFFFF0001，就以 Device ID FFFFh 選擇驅動程式，可以嗎？</summary><p>在本例 RRS 條件下不可以。這是暫時未就緒的合成值，尚未取得真正身分；應處理重試與就緒，而非當成未知產品繼續初始化。（§2.3.2，p.220。）</p></details>
<details class="question"><summary>最後 Subordinate 比 04 大，一定是枚舉錯誤嗎？</summary><p>不一定。要核對平台授予範圍、分支一致性與保留政策；04 是本例採用的最終範圍，不是通用常數。</p></details></section>
<p>下一步是 <a href="/DOCS/pcie-course/chapter-4.html">Chapter 4 的 BAR 與資源配置</a>。</p>
</article>
<nav class="bottom-nav" aria-label="課程與語言版本"><a href="/DOCS/pcie-course/index.html">課程總覽</a><a href="/DOCS/pcie-course/chapter-3.html">繁中完整教學</a><a href="/pcie/chapter-3-en/">English</a></nav>
</div>
