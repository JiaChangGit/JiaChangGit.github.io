# 2026-09-13 中文課程與引用教學修訂

使用者授權完成全部修改、驗證後 commit 與 push。13 篇均保留中文課程 HTML
及內容對等的中英文全局報告，共 39 個交付物。五篇精確主範圍登記於
`.ai/nvme-report/scope.json` 的 `primary_scope`，不納入 Fabrics。

## 編排

中文課程使用獨立情境，逐步呈現中間判斷與計算，再連回規格條件。
問答前的逐圖重點與案例保留；相關欄位另有一次完整解說及來源，逐圖連回。
必要解釋預設可見，不再以欄名清單或重複的折疊段落代替教學。
Power State／APST 使用有條件的轉移圖與延遲時間線；Boot 使用來源與目的
座標圖及保護狀態圖；Self-test 區分命令完成與背景作業完成。

## 來源複核及修正

- Boot 的多 domain 共享限制針對 Write Locked Until Power Cycle 狀態，
  不代表分割區不可用。Set Features 與 RPMB 的 reset 保留行為分開比較。
  來源：Base PDF 539–540、615–620。
- MNSOIP 是並行 namespace sanitize 作業數上限；不是目前作業數。
  SANS、FAILS、SOS、MVCNCLD、GDE、NDE、PRGD 分別按有效條件使用。
  來源：Base PDF 340–345、747–755。
- Sanitize 的 AUSE、EMVS、NDAS、NODRM、PREQ 依方法、能力及狀態配對。
  來源：Base PDF 476–479、503–504。Overwrite 的反相首遍需按總 pass 數奇偶決定，並分開計算 PI；以 Base PDF 743 複核。
- Namespace Create 的 PI／LBAFEE／LBSTM 及 FDP handle 清單限制加入完整例子。
  粒度的 ND 使用數量減 1；NSG／NCG 使用 bytes，不能與 block 數直接相除。
  來源：NVM PDF 108、110–113。
- Device Self-test 的 STC／目前作業組合、DSTP 有效性、Format 交互作用及
  FLBA 限制分別介紹。來源：Base PDF 225–226、256–258、641–642；NVM PDF 76。
- APST 要求連續閒置時間超過 ITPT；返回最近 operational state 處理 I/O。
  轉移時間採來源 EXLAT 加目標 ENLAT。來源：Base PDF 495、693–695。
- 各篇 Identify Controller 與通知圖只教該篇使用的分支。移除 Self-test 的
  CAP.DSTRD 誤引及 Sanitize 的 Figure 474 誤引；該表沒有 Sanitize 專屬通知位元。
  HMB 篇的 Identify 欄位索引移除舊合輯留下的 Self-test 欄位。

## 防止回歸

公開語句不得用無條件全字串替換消除 decode／locate：這曾把「解碼器」變成
「依欄位換算器」，也破壞英文語法。禁止無對象圖標的規則由結構驗證處理。
保留技術語句的上下文，應在來源文字中完整改寫。

驗證涵蓋五篇精確主範圍、每張圖的重點與案例、欄位解說的實際內容和連結、
全部 HTML 的獨立推理教學、雙語對等、數值、術語次數、來源及排除範圍。
產物再生比較逐檔回報，避免單一失敗產生數百萬字的字典差異。
本機 Jekyll 使用 Ruby 3.3 與 lockfile 的 Bundler；發布後仍須核對同一 commit
的報告驗證、Pages 部署與線上內容。先前 Ruby 3.0 問題見
`docs/ci-pages-maintenance.md`。

本文件是維護紀錄，由 Jekyll 排除，不呈現在教材。
