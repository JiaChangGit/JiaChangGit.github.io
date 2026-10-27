---
name: spec-teaching
description: Create and revise the PCIe Base 6.0 course and the selected NVMe self-study, figures/scenarios, Transport 1.4, and NVM Command Set 1.3 articles in JiaChangGit.github.io, using connected specification reading, guided diagrams, natural Taiwan Chinese, and blue/green series styles.
---

# PCIe 與 NVMe 規格教學

本 skill 保存本次已對齊的教學方式。適用範圍與工作狀態見 [scope.md](references/scope.md)；寫作與視覺決策見 [teaching.md](references/teaching.md)；編輯入口及檢查見 [workflow.md](references/workflow.md)。執行任務時先讀使用者當次要求與 repository 的 `AGENTS.md`，再讀相關參考文件。使用者的新指示優先於舊版 skill 與歷史專案限制。

2026-10-24 使用者明確說明：提供的題目、分類、題數與回答格式都只是參考。撰寫 PCIe 自學教材時另讀 [authoring.md](references/authoring.md)：按學習目的選題與組織內容，不要求逐題沿用原代碼或填滿固定小節。來源準確、模式與適用條件、自然中文及必要推理仍須保留。

## 核心決策

- 讀者具備基本程式、CPU／記憶體與位元運算概念，尚未熟悉 PCIe 或 NVMe。先建立系統觀，再深入規格、欄位與流程。
- 依每章的核心問題重排段落、改寫語句與重整圖表。既有 Chapter 7–9 可作導圖與教學銜接的參考，但每篇仍依學習目的安排，不套固定章節、圖數或回答項目。
- 開頭先用合適的總覽圖或關係表定位主題，接著講重點，只回顧本篇必要前情。先完整帶讀正常流程，再解釋相關條件與例外。
- 自問自答用來教人。問題接著解說，交代角色、動作、原因及下一步；不要求讀者先作答。正常流程、必要條件與推導直接顯示，補充背景及完整引用可收合。
- 圖與正文共同完成教學。角色關係、跨元件交換、狀態轉換、等待分支及欄位比較，依問題選擇拓樸、時序、狀態、流程或表格。完整圖文持續可見，逐步功能只高亮重點。
- 沿情境串起規格：現在為何查這張 Figure／Table、讀哪個欄位、讀到什麼，以及如何進到下一步。閱讀路線不冒充硬體執行順序。
- 作者自行推演案例與假設讀值可以使用，須就近標明；規格規定、教學假設與推演結論要分得清楚。保留規範強度、有效條件、禁止及未定義行為。
- 每篇、每個語言版本各自計算術語。英文 Spec 關鍵字與縮寫前兩次都就近簡短解釋，圖中也適用。後文優先使用穩定自然的中文；詞彙表和滑鼠提示不能取代可見說明。
- 中文使用自然的台灣語句，寫清楚誰對誰做什麼，再接結果、原因與條件。按上下文選連接詞，不用抽象評論或密集英文速記代替解說。
- 繁中 HTML 提供完整教學；中英文文章保留相同主線、核心圖、代表案例及適用條件。跨篇只短述必要背景，完整原理連回主要文章。
- 共用閱讀樣式，PCIe 用藍色、NVMe 用綠色。實際來源仍寫明規格名稱與版本，尤其分清 PCI Express Base 6.0 與 NVMe over PCIe Transport 1.4。

## 範圍與完成依據

PCIe 包含現有全部文章，並補齊 Base 6.0 尚未涵蓋的主題。NVMe 僅含自問自答、圖表判讀與情境練習、NVMe over PCIe Transport 1.4、NVM Command Set 1.3，均含繁中教學 HTML 與中英文文章。保留既有 URL、題號、有效錨點與圖表固定位置。

全規格涵蓋表區分「待核對」「僅提及」「已帶讀」；標題、索引或短介紹不算完成。新增主題有完整教學、來源及三版本並經校閱，才列為已帶讀。

先改 authored 來源及產生器，再產生頁面；來源與算例可用腳本檢查，中文、教學順序及圖文語意必須實際校閱。明暗、桌機、平板、手機、鍵盤、離線及列印都需可讀。腳本通過、AI 作答或按完步驟都不能當作真人已學會的證據。

本版已由使用者確認並授權開始修訂。執行及發布範圍仍依當次要求；之後若要求只讀或先確認，該要求優先。來源 PDF、本機路徑、私密資料與檢查紀錄不得進入公開網站。
