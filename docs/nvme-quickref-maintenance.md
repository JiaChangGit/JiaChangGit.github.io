# NVMe 圖表速查系列維護

2026-09-30：使用者核准三份已提供的 ratified PDF，僅排除 Fabrics；輸出繁中
HTML、中文 Pages、英文 Pages。這是新的反覆查詢／除錯／驗證系列，不沿用舊專篇
的章節、FID、LID、CNS 排除清單，也不把既有 22 篇教學合併或替換。

## 選圖與編排

依能力與初始化、命令結果與指標、Identify、I/O 與完整性、Features、logs、維護操作
分成七冊。117 張是依查詢用途挑選的原圖，並非三份 Spec 全部圖表。總索引提供問題路徑
及欄位／識別值／圖號查詢。每張原圖僅有一份獨立說明，其他入口使用錨點連結。
每圖三段分別交代用途、相關欄位及具體判讀；中英文段落、來源和順序對等。
繁中 HTML 另有跨圖查詢案例，內嵌 CSS 且不依賴 JavaScript。

原始圖表不搬入公開網站；公開的是自行撰寫的介紹、短必要術語、原圖名與完整定位。
大型 Identify 表另外提供常用欄位的 PDF 頁碼。不要把快查文字當作完整規格表的轉錄。

## 來源校正

`.ai/nvme-quickref/figures.json` 記錄原圖號、完整英文圖名、章節、文件頁、PDF 頁
及原始 PDF 頁面文字雜湊；原始 PDF 的 SHA-256 仍由既有 source-register 管理。
文字雜湊使用 `pdftotext -layout` 並正規化空白，只公開雜湊，不公開擷取全文。
來源核對需使用原始 PDF，而不能只比較舊快取。

- Base Figure 338 完整跨 PDF 366–408（文件 340–382），不能以舊索引的 390 截斷。
- NVM Figure 129 跨 PDF 103–106，續頁未重複圖名，不能只保留 103。
- Base PDF 92 視覺檢查確認 Figure 43/44/45 分屬 §3.1.4.7/.8/.9；
  部分小節標題無法由 PDF 文字抽取保留，不能直接沿用最近可抽取的標題。
- 另外核正 Figure 42、46、103、107 及 PCIe Figure 6 的章節；
  PCIe Figure 5/6 圖名分行，須保留最後的 Doorbell。
- 實際檢視 Base PDF 171/172 及 NVM PDF 19/143/145，核對 completion layout、
  atomic boundary 與 PRACT 下的 metadata 排列。尤其 metadata 大於 8 bytes 時，
  不能機械地扣掉 8 bytes 當作傳輸長度。

## 更新及驗證

編輯 `scripts/nvme_quickref_*.py` 的逐圖內容，執行：

```sh
python3 -B scripts/build_nvme_quickref.py
python3 -B scripts/build_nvme_quickref.py --check
python3 -B scripts/nvme_quickref_sources.py --source-dir <PDF_DIR>
python3 -B -m unittest discover -s tests -v
```

兩個 GitHub workflow 均檢查 24 份輸出與 manifest 是否過期。來源 PDF 核對只在
持有使用者原檔的本機執行，CI 不下載或發布 PDF。新系列獨立於舊 66 份 output contract。
新增欄位或改動例子時，同步修改中英內容、相關連結與來源頁碼。計數／位移例子要從
原始數值重算；不得只檢查一個手寫的預期字串。

版面檢查包括 834×1194、1194×834、1440×1000，明暗模式且系統偏好與網站設定
相反的情境。驗證頁面不橫向溢出、錨點不重複、連結有效、文字對比及本機 file://
跨冊導覽。表格可在自己的區域橫向捲動。發布後核對同一完整 commit SHA 的兩個
workflow，並比對線上頁面與本機建置的實際內容。

此文件是維護紀錄，不放在閱讀者正文。
