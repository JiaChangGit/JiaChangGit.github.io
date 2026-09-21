# Read Recovery Level 維護紀錄

本文件供維護與來源查核，不納入讀者教材。

2026-09-21 使用者要求 Base §8.1.23 + §5.2.30.1.12（FID 12h）合為一篇。
沿用三版：獨立中文教學 HTML、內容對等的中英文全局報告。
前篇 Admin／I/O 的 FID 12h 排除項不變；本次明確納入不會反向擴大舊篇。

主範圍完整包含 Figures 755、484、485。11 張必要引用為
67、93、126、127、197、198、201、338、463、464、466。
各圖有獨立重點、例子與共用欄位解釋的實際連結；必要背景只取相關欄位。
Figure 338 僅取 CTRATT.RRLVLS／NSETS、RRLS、ONCS.SSFS；
Figure 466 只取 FID 12h 列、表頭與註腳 2。不擴充為其他 FID 的教學。

## 不可省略的來源條件

- RRL 支援是前提。支援時 4 與 15 必備，0 是選用；15 提供最少復原，
  沒有固定毫秒上限、零次重試或保證更快的規定。與 LR 的互動由實作決定。
- CTRATT 位於 bytes 99:96，RRLVLS bit 3、NSETS bit 2；RRLS bytes 101:100。
  ONCS bytes 521:520，SSFS bit 4。bit 位置均相對各自欄位。
- RRLS 是 bitmap，不是目前 RRL；8011h 由 little-endian bytes 11 80 組成，
  只支援 0、4、15。Level 15 在 RRL 欄填 Fh，支援遮罩則是 8000h。
- NVM Sets 支援時，0 是保留的 NVMSETID，不是廣播；不支援時，
  主機依 §3.2.2 清 NVMSETID=0，本 Feature 忽略此欄並作用於 subsystem。
- NVM Set／subsystem scope 的 NSID 應清 0，非零使 Get／Set 中止；
  不可誤套一般 controller-scope Get 允許有效 NSID 的規則。
- Set CDW11 放目標 Set，CDW12 放 RRL。Get 保留相同 CDW11 目標，
  成功且 SEL≠3 的結果用 Figure 485 格式放在 CQE DW0，不在 Get CDW12。
- SEL=3 是 CHANG／NSSPEC／SVBL 能力格式，不是 RRLS 或 current。
  NSSPEC=0 不表示一定是 controller scope；SSFS=0 不使用非零 SEL／SV。
- FID12h 不使用 data buffer；DPTR 的 Set 不使用與 Get 忽略由各自定義說明。
- 設定成功後才提交的命令必須採新值；在途命令可能採用也可能不採用。
  共享 Feature 的多主機存取需要協調，Base 不指定協調程序。
- Figure 466 的 Yes 只適用不可保存 Feature（註腳 2）。不可保存的 FID12h
  仍須跨 power cycle 與 reset 保留 current；SV=0 不等於無持續性。
- 可保存者：Figure126 的全體範圍重設回 saved／default；Figure127 的局部範圍
  重設在 NVM Set／subsystem 欄維持 current。先確認配置與重設覆蓋範圍，
  不能只用重設名稱選表。Non-saveable and non-persistent 列不適用本篇的
  不可保存但具持續性分支。

## 報告路徑與驗證

中文 HTML 按七個單元教學，沒有 Spec 翻頁路徑。
中英文 post 使用 Base PDF 檢視器 499 → 715～716，只向後跳一次。
499 從 §5.2.30.1.12 開始，在 §5.2.30.1.13 前停止；715 從 §8.1.23
開始，716 在 §8.1.24 前停止。實際 PDF 已視覺核對，不沿用目錄頁碼猜測。

驗證涵蓋範圍／來源登記、完整逐圖解釋、bitmap 與命令編碼運算、雙語順序、
三版明暗模式與 iPad／桌面排版。完成時核對同一 commit 的全部 CI 與線上內容。
Ruby／Bundler 不需變更，仍遵守 `ci-pages-maintenance.md`。
