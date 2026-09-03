# NVMe 規格報告領域規則

本文件固定本次報告的來源、規範性用語、來源優先序與公開邊界。適用對象是撰寫、
翻譯、審查或驗證本報告的人員；不取代 NVM Express 原始規格，也不涵蓋尚未提供的
PCI Express Base Specification 或 controller vendor 行為。

查證日期：2026-09-03。

## 採用來源

| 來源 ID | 正式文件 | Revision | Ratified | PDF 頁數 |
|---|---|---:|---:|---:|
| `NVME-BASE-2.4` | NVM Express Base Specification | 2.4 | 2026-07-31 | 870 |
| `NVME-NVM-CS-1.3` | NVM Express NVM Command Set Specification | 1.3 | 2026-07-31 | 177 |
| `NVME-PCIE-TRANSPORT-1.4` | NVM Express NVMe over PCIe Transport Specification | 1.4 | 2026-07-31 | 48 |

目前沒有其他適用的 Errata、Engineering Change Notice (ECN)、Technical Proposal 或
controller vendor 文件。若之後新增，必須先更新來源登記、範圍與所有受影響 claim，
再更新九份報告中受影響的輸出（共 36 個交付檔）。

## 規範性用語

權威定義位於 `NVME-BASE-2.4` §1.4.1，文件印刷頁 2-3、PDF 頁 28-29。
`NVME-NVM-CS-1.3` §1.3（文件／PDF 頁 9）沿用 Base 的 conventions、keywords 與
byte／word／dword relationships。`NVME-PCIE-TRANSPORT-1.4` §1.3（文件／PDF 頁
6-7）沿用 Base conventions，但另定義 PCI／PCIe register 或 property 表格中的 Reset 欄。

| 規格 keyword | 台灣繁體中文 | 使用規則 |
|---|---|---|
| `mandatory` | 強制 | 依規格定義實作的項目 |
| `may` | 可、得 | 有選擇彈性，規格不暗示偏好；不得翻成機率上的「可能」 |
| `obsolete` | 已廢止 | 舊版曾定義、目前版本已移除的功能 |
| `optional` | 選用 | 規格不要求支援；一旦實作，仍須依規格定義實作 |
| `R` / `reserved` | 保留 | 依欄位語境處理，不等同一般未使用值 |
| `shall` | 必須 | 強制要求；詳細中文版保留「必須（shall）」 |
| `should` | 宜、建議 | 有強烈偏好的建議，但仍保留選擇彈性 |

若原文沒有使用上述 keyword，不得只因句意強烈就自行提升為 `shall`。`must`、
`shall not`、`need not` 等字樣若出現在後續範圍，應逐句依原文語法與上下文登記，
不得先建立規格沒有定義的全域對照規則。

## 規格間衝突的優先序

`NVME-NVM-CS-1.3` §1.2 與 `NVME-PCIE-TRANSPORT-1.4` §1.2 都定義下列優先序；
號碼較小者優先：

1. 非 NVMe 規格（Non-NVMe specifications）
2. NVM Express Base Specification
3. NVM Express Transport specifications
4. NVM Express I/O Command Set specifications
5. NVM Express Management Interface Specification
6. NVM Express Boot Specification

本次只提供第 2、3、4 類文件。PCIe Transport 1.4 §1.5 參照 PCI Express Base
Specification Revision 6.2，但該文件未納入本次來源。涉及 PCIe 原生語意時，只能描述
Transport 1.4 明載的 NVMe-specific requirement；不得補寫 PCIe 6.2 條文。

## 引用格式

每個結論至少包含：

```text
來源：<SOURCE-ID>, Rev. <revision>, §<section>,
Figure <n>／Table <n>（若適用）, 文件頁 <p>, PDF 頁 <p>
```

Base 2.4 的正文第 1 頁位於 PDF 第 27 頁；正文範圍可用 `PDF 頁 = 文件頁 + 26`
核對。NVM Command Set 1.3 與 PCIe Transport 1.4 的可見頁碼目前與 PDF 頁碼一致。
跨頁 Figure／Table 應列完整頁碼範圍。

正文引用到範圍外 Figure 時，若理解主題需要該 Figure，應以相依教學項目登記並只介紹
被引用的欄位與關係；這不會把 Figure 所在章節整段納入範圍。Fabrics／Discovery 專用
Figure 的排除優先於相依引用規則。

## 公開與重繪邊界

- 三份來源 PDF 留在儲存庫外，不提交 Git、PR、CI artifact 或 GitHub Pages。
- 公開內容使用自行撰寫摘要、短必要術語、精確定位與自行重繪圖。
- 不複製完整規格表格或原圖；重繪圖應只保留理解所需的關係，並列來源 claim。
- 無法確定散布權或規格沒有定義的內容，標成待確認，不自行補完。
