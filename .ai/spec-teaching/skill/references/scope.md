# 本次範圍與版本

2026-10-23 使用者確認全部七項選擇，並補充 PCIe 要涵蓋 Base 6.0 尚未成篇的主題；另確認兩篇 NVMe 專篇也完整納入。使用者確認工具包後，已授權開始修訂，並要求注意公開 GitHub Pages 的資安。

## 納入

1. PCIe：現有 Chapter 0–13 與索引，並查證、編排、補足 PCI Express Base Specification Revision 6.0 全文尚未涵蓋的主題。附錄也須核對，不預先排除。新增課程依理解順序安排，不必照 Spec 順序。
2. NVMe 自問自答：27 冊、Q1–Q328 與總索引。
3. NVMe 圖表判讀與情境練習：7 冊、45 個情境、117 張既有圖表與總索引。
4. NVMe over PCIe Transport 1.4：同名專篇，report_id=`pcie-transport-1.4`。
5. NVM Command Set 1.3：同名專篇，report_id=`nvm-command-set-1.3`。

各項均包含繁中教學 HTML、中英文文章；有索引的系列同時整理索引。兩篇 NVMe 專篇也是綠色系列。其他 NVMe 專篇與整站外觀不在範圍內。

## 版本邊界

| 來源 | 本次依據 | 注意 |
|---|---|---|
| PCI Express Base | 6.0，2021-12-16 | PCIe 主課程依據；全文含附錄需建立涵蓋表 |
| PCI Firmware | 3.3，2021-01-20 | 既有韌體背景；不視為與 Base 6.0 同版配套 |
| NVM Express Base | 2.4，2026-07-31 ratified | 依 repository 登記及使用者提供的 PDF |
| NVM Command Set | 1.3，2026-07-31 ratified | 保留命令集特定條件 |
| NVMe over PCIe Transport | 1.4，2026-07-31 ratified | 文中引用的 PCIe Base 版本須逐項查明，不直接換成 6.0 |

來源登記以兩個系列既有的 `source-register.json` 為準；來源 PDF 不進公開 repository、工具下載包或 CI artifact。本文列的是目前登記版本，未宣稱是網路最新版本。

NVMe 原有 Fabrics 排除與各篇範圍維持；本次沒有擴寫整套 NVMe 規格的授權。理解所需的跨篇背景可以簡短補上，並保留精確來源。
