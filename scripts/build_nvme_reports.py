#!/usr/bin/env python3
"""Build four NVMe reports from the local, gitignored source inventory."""

from __future__ import annotations

import argparse
import html
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTROL = ROOT / ".ai" / "nvme-report"
SOURCES = {
    "NVME-BASE-2.4": {
        "revision": "2.4",
        "marker": "NVM Express Base Specification, Revision 2.4",
    },
    "NVME-PCIE-TRANSPORT-1.4": {
        "revision": "1.4",
        "marker": "NVM Express NVMe over PCIe Transport Specification, Revision 1.4",
    },
}


def page_shift(value: str, delta: int) -> str:
    values = [int(item) + delta for item in value.split("-")]
    return str(values[0]) if len(values) == 1 else f"{values[0]}-{values[-1]}"


def c(key, section, pages, zh, en, keyword="none", source="NVME-BASE-2.4"):
    pdf_pages = pages if source == "NVME-PCIE-TRANSPORT-1.4" else page_shift(pages, 26)
    return {
        "key": key,
        "source_id": source,
        "section": section,
        "printed_pages": pages,
        "pdf_pages": pdf_pages,
        "normative_keyword": keyword,
        "zh_tw": zh,
        "en": en,
    }


REPORTS = {
    "base-ch1-2": {
        "prefix": "BASE12",
        "title_zh": "NVMe Base 2.4 第 1、2 章：規格語言、PCIe 佇列與儲存模型",
        "title_en": "NVMe Base 2.4 Chapters 1–2: Specification Language, PCIe Queues, and Storage Model",
        "source_id": "NVME-BASE-2.4",
        "scope_entry": "BASE12-INCLUDE",
        "range": "§1–§2；文件頁 1–37；PDF 頁 27–63",
        "range_en": "§1–§2; printed pages 1–37; PDF pages 27–63",
        "diagram": ["Host / CPU core", "Submission Queue", "NVMe controller", "Completion Queue"],
        "diagram_note_zh": "命令由 host 放入 Submission Queue；controller 取走並執行，再把完成結果寫入 Completion Queue。",
        "diagram_note_en": "The host places commands in a Submission Queue; the controller fetches and executes them, then posts completions to a Completion Queue.",
        "claims": [
            c("FAMILY", "1.1.1", "1", "Base Specification 定義通用 NVMe 協定；Transport Specification 綁定特定傳輸，I/O Command Set Specification 擴充命令與資料結構。這是適用關係，不是協定堆疊。", "The Base Specification defines the common NVMe protocol; a Transport Specification binds it to a transport, and an I/O Command Set Specification extends commands and data structures. This is an applicability relationship, not a protocol stack."),
            c("KEYWORDS", "1.4.1", "2-3", "規格的 mandatory、may、optional、reserved、shall、should 各有固定語氣；詳細版保留英文 keyword，不能把 may 或 should 翻成 shall。", "The specification assigns distinct force to mandatory, may, optional, reserved, shall, and should. A summary must not strengthen may or should into shall."),
            c("NUMBERS", "1.4.2", "3-5", "數值的解讀同時包含進位與單位；十六進位使用 h 後綴，二進位使用 b 後綴，十進位可省略 d。十進位與二進位容量前綴代表不同倍率。", "A value is interpreted together with its radix and units. Hexadecimal uses the h suffix, binary uses b, and decimal may omit d. Decimal and binary capacity prefixes represent different multipliers."),
            c("DWORD", "1.4.3", "5", "NVMe 以 byte、word、dword 表示欄位位置；一個 word 為 2 bytes，一個 dword 為 4 bytes。解欄位時先確認 byte 與 bit 編號。", "NVMe expresses field locations in bytes, words, and dwords. A word is two bytes and a dword is four bytes; field decoding starts by confirming byte and bit numbering."),
            c("QUEUE", "2.1", "21-23", "PCIe memory-based model 把 Submission Queue 與 Completion Queue 配置在記憶體。多個 I/O Submission Queues 可共用一個 I/O Completion Queue；Admin queue pair 維持一對一。", "In the PCIe memory-based model, Submission and Completion Queues reside in memory. Multiple I/O Submission Queues may share an I/O Completion Queue, while the Admin queue pair remains one-to-one."),
            c("STORAGE", "2.3.1", "26-33", "儲存模型用 NVM subsystem、domain、Endurance Group、NVM Set／Reclaim Group、Reclaim Unit 與 namespace 表達包含關係。namespace 是 host 實際透過 controller 存取的格式化容量。", "The storage model expresses containment through the NVM subsystem, domain, Endurance Group, NVM Set or Reclaim Group, Reclaim Unit, and namespace. A namespace is the formatted capacity a host accesses through a controller."),
            c("COMMANDSET", "2.3.2", "33", "Admin Command Set 管理 controller 與 queue；I/O Command Set 定義對 namespace 的資料操作。Base 說明通用機制，個別 I/O Command Set Specification 說明命令語意。", "The Admin Command Set manages controllers and queues; an I/O Command Set defines data operations on namespaces. Base describes common mechanisms, while each I/O Command Set Specification describes command semantics."),
            c("SUBSYSTEM", "2.3.3", "33-35", "controller、port、namespace 與 PCI Function 是不同物件；NSID 是 controller 用來指向 namespace 的 handle，不是 namespace 本身。", "Controllers, ports, namespaces, and PCI Functions are distinct objects. An NSID is a controller-visible handle for a namespace, not the namespace itself."),
            c("MULTIPATH", "2.4.1", "35-37", "multi-path I/O 是同一 host 到同一 namespace 的兩條以上獨立路徑；namespace sharing 是兩個以上 host 經不同 controller 存取同一 shared namespace。兩者都需要至少兩個 controller。", "Multi-path I/O provides two or more independent paths from one host to one namespace; namespace sharing lets two or more hosts access one shared namespace through different controllers. Both require at least two controllers."),
            c("ASYMMETRY", "2.4.2", "37", "支援多路徑或共享時，各 controller 對同一 namespace 的存取特性不一定相同；host 可依 controller 所回報的狀態選擇路徑。", "With multi-path or sharing, controllers need not provide identical access characteristics to the same namespace; the host may select paths using the state reported by each controller.", "may"),
        ],
    },
    "base-ch3": {
        "prefix": "BASE3",
        "title_zh": "NVMe Base 2.4 第 3 章：Controller、Queue、初始化與重設",
        "title_en": "NVMe Base 2.4 Chapter 3: Controllers, Queues, Initialization, and Resets",
        "source_id": "NVME-BASE-2.4",
        "scope_entry": "BASE3-INCLUDE",
        "range": "§3；文件頁 38–138；PDF 頁 64–164",
        "range_en": "§3; printed pages 38–138; PDF pages 64–164",
        "diagram": ["Properties / CAP", "CC.EN = 1", "CSTS.RDY = 1", "Queues active"],
        "diagram_note_zh": "host 先讀能力與設定 Admin queues，再啟用 controller；只有 CSTS.RDY 回報 ready 後才進入正常 queue processing。",
        "diagram_note_en": "The host reads capabilities and configures Admin queues before enabling the controller; normal queue processing starts only after CSTS.RDY reports ready.",
        "claims": [
            c("STATIC", "3.1.1", "38", "memory-based controller 必須（shall）只支援 static controller model。", "A memory-based controller shall support only the static controller model.", "shall"),
            c("TYPES", "3.1.3-3.1.3.2", "39-43", "本輪只使用 I/O controller 與 Administrative controller：前者可執行使用者資料的 I/O，後者以管理為目的且不支援資料 I/O command。兩者都具有一組 Admin Submission／Completion Queue。", "This report uses the I/O and Administrative controller roles. The former performs user-data I/O; the latter is management-oriented and does not support data I/O commands. Both have one Admin Submission/Completion Queue pair."),
            c("ORDER", "3.1.3", "40", "除 fused operation 外，controller 取走的命令與完成沒有一般性的先後保證；若有順序需求，強制該順序是 host 的責任。", "Except for fused operations, fetched commands and completions have no general ordering guarantee. Enforcing any required order is the host's responsibility."),
            c("PROPERTY", "3.1.4", "52-54", "host 必須（shall）以 property 指定的寬度，從 property 起始 offset 存取；memory-based controller 的實際存取規則由 PCIe Transport 補充。", "The host shall access a property at its starting offset using the specified width; the PCIe Transport adds the access rules for a memory-based controller.", "shall"),
            c("NAMESPACE", "3.2.1", "78-80", "NSID 0h 無效，FFFFFFFFh 是 broadcast 值；其餘 NSID 還要區分 allocated／unallocated 與 active／inactive，不能只看數字是否落在範圍內。", "NSID 0h is invalid and FFFFFFFFh is the broadcast value. Other NSIDs still need allocated/unallocated and active/inactive classification; numeric range alone is insufficient."),
            c("MEDIA", "3.2.2-3.2.4", "80-85", "NVM Set、Endurance Group、Reclaim Group 與 Reclaim Unit 分別描述容量集合、耐久度管理與回收粒度。是否支援及其 identifier 由 Identify／log page 能力判定。", "NVM Sets, Endurance Groups, Reclaim Groups, and Reclaim Units describe capacity grouping, endurance management, and reclamation granularity. Support and identifiers are determined from Identify data and log-page capabilities."),
            c("DOMAIN", "3.2.5", "85-88", "domain 是 NVM subsystem 內的故障／通訊邊界。多 domain subsystem 的 identifier 必須（shall）在該 subsystem 內唯一。", "A domain is a failure or communication boundary inside an NVM subsystem. In a multi-domain subsystem, each domain identifier shall be unique within that subsystem.", "shall"),
            c("QUEUE", "3.3.1", "88-91", "PCIe queue 由 host-addressable memory 中的環形 buffer、head 與 tail pointer 構成。host 建立 I/O Completion Queue 後再建立對應 Submission Queue，並以 doorbell 推進 pointer。", "A PCIe queue is a circular buffer in host-addressable memory with head and tail pointers. The host creates an I/O Completion Queue before its Submission Queue and advances pointers through doorbells."),
            c("PROCESS", "3.4.1-3.4.5", "101-105", "command processing 要分開看 ordering、fused／atomic semantics、arbitration 與 outstanding command 上限；priority 屬於 Submission Queue，不是每一筆 command 的獨立欄位。", "Command processing separates ordering, fused and atomic semantics, arbitration, and outstanding-command limits. Priority belongs to a Submission Queue, not to each command as an independent attribute."),
            c("INIT", "3.5.1, 3.5.3-3.5.4", "105-113", "PCIe 初始化以 CAP 判斷能力與 timeout，設定 AQA／ASQ／ACQ 與 CC，接著等待 CSTS.RDY。ready mode 與 CRTO 會影響 host 等待與錯誤處理。", "PCIe initialization reads CAP, configures AQA/ASQ/ACQ and CC, then waits for CSTS.RDY. Ready mode and CRTO affect host wait and error handling."),
            c("SHUTDOWN", "3.6.1, 3.6.3", "113-120", "正常 shutdown 由 host 設定 CC.SHN，controller 透過 CSTS.SHST 回報進度；NVM subsystem shutdown 是更大範圍的處理，不能與單一 controller shutdown 混為一談。", "Normal shutdown begins when the host sets CC.SHN and the controller reports progress in CSTS.SHST. NVM subsystem shutdown has a wider scope and is not the same as one controller shutdown."),
            c("RESET", "3.7", "120-125", "NVM Subsystem Reset、Controller Level Reset 與 Queue Level Reset 的影響範圍不同；設計 recovery flow 前先確認哪一層狀態會被清除、queue 是否仍存在。", "NVM Subsystem, Controller Level, and Queue Level resets have different scopes. A recovery flow first determines which state is cleared and whether queues still exist."),
            c("CAPACITY", "3.8", "125-129", "capacity model 分開追蹤 NVM subsystem、Endurance Group、NVM Set 與 namespace 的可用或配置容量；同一數值不可跨層級直接比較。", "The capacity model tracks available or configured capacity separately at subsystem, Endurance Group, NVM Set, and namespace levels. Values from different levels are not directly interchangeable."),
            c("KEEPALIVE", "3.9", "129-135", "Keep Alive 以 KATO／KATT 建立 host 與 controller 的存活監測；本報告只保留 controller 共通與 PCIe 可用的 timer、command 與 timeout 行為。", "Keep Alive uses KATO and KATT for host/controller liveness monitoring. This report retains only controller-common and PCIe-applicable timer, command, and timeout behavior."),
            c("FIRMWARE", "3.10-3.11", "135-138", "privileged action 會影響其他 host 或 controller；firmware update 分成 image download、commit／activate 與可能的 reset，host 依回報的 activation action 安排流程。", "A privileged action may affect other hosts or controllers. Firmware update separates image download, commit/activation, and any required reset; the host sequences the flow using the reported activation action."),
        ],
    },
    "base-ch4": {
        "prefix": "BASE4",
        "title_zh": "NVMe Base 2.4 第 4 章：SQE、CQE、Status、PRP 與 SGL",
        "title_en": "NVMe Base 2.4 Chapter 4: SQE, CQE, Status, PRP, and SGL",
        "source_id": "NVME-BASE-2.4",
        "scope_entry": "BASE4-INCLUDE",
        "range": "§4；文件頁 139–175；PDF 頁 165–201",
        "range_en": "§4; printed pages 139–175; PDF pages 165–201",
        "diagram": ["64-byte SQE", "PRP or SGL", "Command execution", "16-byte+ CQE"],
        "diagram_note_zh": "SQE 以 CID 與 SQID 識別 command，data pointer 描述 buffer；CQE 回報 SQ head、SQID、CID、phase 與 status。",
        "diagram_note_en": "The SQE identifies a command with CID plus SQID and describes buffers through data pointers; the CQE reports SQ head, SQID, CID, phase, and status.",
        "claims": [
            c("SQE", "4.1.1", "139-143", "Admin 與 I/O common SQE 固定為 64 bytes。CDW0、NSID、data pointer 與 CDW10–15 的通用位置先固定，再由各 command 定義命令專屬內容。", "The common Admin and I/O SQE is 64 bytes. CDW0, NSID, data pointers, and CDW10–15 establish the common layout before each command defines command-specific content."),
            c("CID", "4.1.1", "140", "CID 與 Submission Queue identifier 的組合用來唯一識別 command；FFFFh 宜（should）避免使用，因 Error Information log 以該值表示錯誤未對應特定 command。", "CID in combination with the Submission Queue identifier uniquely identifies a command. FFFFh should be avoided because the Error Information log uses it when an error is not associated with a particular command.", "should"),
            c("PSDT", "4.1.1", "140-142", "CDW0.PSDT 決定 DPTR 解讀為 PRP 或 SGL。NVMe over PCIe 的 Admin command 原則上必須（shall）使用 PRP，除非 command 定義另有規定。", "CDW0.PSDT selects PRP or SGL interpretation for DPTR. An Admin command over PCIe shall use PRPs unless its command definition specifies otherwise.", "shall"),
            c("CQE", "4.2.1", "144-145", "common CQE 至少 16 bytes；若以多次寫入建立 CQE，Phase Tag 必須（shall）在最後一次寫入更新，避免 host 看到半成品。", "The common CQE is at least 16 bytes. If multiple writes construct it, the Phase Tag shall be updated in the last write so the host does not consume a partial entry.", "shall"),
            c("STATUS", "4.2.3", "145-155", "status 要先解 Status Code Type（SCT），再解 Status Code（SC），同時檢查 Do Not Retry（DNR）等控制 bit；數值不能脫離 SCT 單獨解讀。", "Status decoding starts with Status Code Type (SCT), then Status Code (SC), together with control bits such as Do Not Retry (DNR). An SC value is not interpreted without its SCT."),
            c("PHASE", "4.2.4", "155-158", "Phase Tag 讓 host 判斷環形 Completion Queue slot 是否為新完成項目；host 消費 CQE 後推進 CQ head doorbell，wrap 時預期 phase 翻轉。", "The Phase Tag lets the host distinguish a new entry in a circular Completion Queue. After consuming CQEs, the host advances the CQ head doorbell and expects phase inversion on wrap."),
            c("PRP", "4.3.1", "158-159", "PRP 以固定大小 entry 指向 physical memory page。第一個 entry 可含 page offset；後續 PRP 必須（shall）符合 page alignment，資料長度決定需要幾個 entry。", "A fixed-size PRP entry points to a physical memory page. The first entry may contain a page offset; subsequent PRPs shall obey page alignment, and transfer length determines the required entry count.", "shall"),
            c("SGL", "4.3.2", "159-166", "SGL 由一個以上 descriptor／segment 描述資料 buffer。SGL length 必須（shall）大於等於 requested transfer length；本報告只介紹 PCIe 可用的通用 descriptor。", "An SGL describes a data buffer through one or more descriptors and segments. SGL length shall equal or exceed the requested transfer length; this report covers only generic descriptors applicable to PCIe.", "shall"),
            c("FEATURE", "4.4", "166-169", "Feature 可能具有 default、saved、current value；saved value 支援與跨 reset／power cycle 的 persistence 由 SSFS 與各 Feature capability 判定。", "A Feature may have default, saved, and current values. Saved-value support and persistence across resets or power cycles are determined from SSFS and each Feature capability."),
            c("IDENTIFIER", "4.5", "169-172", "VID／SSVID、SN／MN、IEEE OUI、EUI64、NGUID 與 UUID 的來源、長度與唯一性範圍不同；不能只因外觀相似就互換。此節為 informative。", "VID/SSVID, SN/MN, IEEE OUI, EUI64, NGUID, and UUID differ in origin, length, and uniqueness scope and are not interchangeable. This section is informative."),
            c("LISTS", "4.6", "172-173", "Controller List 與 Namespace List 都先給出數量，再排列 identifier；實作 parser 時，先依格式定義的上限與保留區驗證輸入。", "Controller and Namespace Lists provide a count followed by identifiers. A parser first validates the count, defined limit, and reserved area before consuming entries."),
            c("UTF8", "4.8", "175", "處理 UTF-8 輸入時要依規格流程驗證編碼、禁止的 code point 與截斷情況；不可把任意 byte sequence 當成有效字串。", "UTF-8 input processing validates encoding, prohibited code points, and truncation using the specified flow; an arbitrary byte sequence is not automatically a valid string."),
        ],
    },
    "pcie-transport-1.4": {
        "prefix": "PCIE14",
        "title_zh": "NVMe over PCIe Transport 1.4：完整傳輸綁定",
        "title_en": "NVMe over PCIe Transport 1.4: Complete Transport Binding",
        "source_id": "NVME-PCIE-TRANSPORT-1.4",
        "scope_entry": "PCIE14-INCLUDE",
        "range": "§1–§3 與 Annex A；文件頁／PDF 頁 1–48",
        "range_en": "§1–§3 and Annex A; printed/PDF pages 1–48",
        "diagram": ["Write SQE", "Ring SQ tail doorbell", "Controller executes", "Read CQE / ring CQ head"],
        "diagram_note_zh": "PCIe transport 以 host memory 的 queue 配合 MMIO doorbell；資料可由 PRP／SGL 指到 host-addressable memory。",
        "diagram_note_en": "The PCIe transport combines queues in host memory with MMIO doorbells; PRPs or SGLs identify data in host-addressable memory.",
        "claims": [
            c("SCOPE", "1.2", "6", "PCIe Transport 補充 Base Specification，定義 PCIe 專屬資料結構、延伸、要求與行為；通用 NVMe 行為仍由 Base 定義。規格衝突時 Base 的優先序高於 Transport。", "The PCIe Transport supplements the Base Specification with PCIe-specific structures, extensions, requirements, and behavior; common NVMe behavior remains in Base. In a conflict, Base has higher precedence than a Transport Specification.", "shall", "NVME-PCIE-TRANSPORT-1.4"),
            c("CONVENTION", "1.3", "6-7", "本文件沿用 Base 的 conventions；register／property 表格中的 Reset 欄改表示依 PCI 或 PCIe 規格定義之 reset 後欄位值。", "This document inherits Base conventions. In register or property tables, the Reset column instead denotes the post-reset field value defined by the applicable PCI or PCIe specification.", "none", "NVME-PCIE-TRANSPORT-1.4"),
            c("KEYWORDS", "1.4.1", "2-3", "shall、may 與 should 的語氣仍由 Base 2.4 定義；Transport 摘要不得自行提高或降低規範強度。", "The force of shall, may, and should remains defined by Base 2.4; a Transport summary must not strengthen or weaken the normative language.", "none", "NVME-BASE-2.4"),
            c("OVERVIEW", "2", "8", "PCIe transport 使用 memory-mapped I/O 進行資料與 register 存取，並使用 PCIe configuration space 與 message-signaled interrupt。", "The PCIe transport uses memory-mapped I/O for data and register access, along with PCIe configuration space and message-signaled interrupts.", "none", "NVME-PCIE-TRANSPORT-1.4"),
            c("MMIO", "3.1", "9-10", "NVMe controller registers 位於 BAR0／BAR1 所指定的 memory space。host 必須（shall）使用 native width 或 aligned 32-bit access，不得發出 locked access；違反時行為未定義。", "NVMe controller registers reside in memory space identified by BAR0/BAR1. The host shall use native-width or aligned 32-bit accesses and shall not issue locked accesses; violation produces undefined behavior.", "shall", "NVME-PCIE-TRANSPORT-1.4"),
            c("DOORBELL", "3.1.2.1-3.1.2.2", "10-11", "SQ tail 與 CQ head doorbell 從 offset 1000h 起，實際 stride 由 CAP.DSTRD 決定；queue identifier y 參與 offset 計算。", "SQ-tail and CQ-head doorbells begin at offset 1000h, with stride determined by CAP.DSTRD; queue identifier y participates in the offset calculation.", "none", "NVME-PCIE-TRANSPORT-1.4"),
            c("QUEUE", "3.2", "11", "PCIe 支援多個 Submission Queues 共用一個 Completion Queue。建立 CQ 時若啟用 interrupt，Interrupt Vector 必須（shall）初始化成對應 MSI-X 或 multiple-message MSI vector。", "PCIe permits multiple Submission Queues to share a Completion Queue. If interrupts are enabled when creating the CQ, Interrupt Vector shall be initialized to the corresponding MSI-X or multiple-message MSI vector.", "shall", "NVME-PCIE-TRANSPORT-1.4"),
            c("RESET", "3.3", "11-12", "PCIe reset 來源包含 Base 定義的 controller/reset 流程與 PCIe 層級 reset。Recovery 設計要以 reset 類型判斷 controller property、queue 與 PCI configuration state。", "PCIe reset sources include Base controller/reset flows and PCIe-level resets. Recovery logic uses the reset type to determine controller-property, queue, and PCI-configuration state.", "none", "NVME-PCIE-TRANSPORT-1.4"),
            c("COMMAND", "3.4", "12-13", "command flow 是：寫 SQE、更新 SQ tail doorbell、controller 取走與執行、寫 CQE、發出 interrupt（若啟用）、host 處理 CQE、更新 CQ head doorbell。doorbell 只通告 pointer，不攜帶 command 本體。", "The command flow writes an SQE, updates the SQ-tail doorbell, lets the controller fetch and execute, posts a CQE, optionally interrupts, processes the CQE, and updates the CQ-head doorbell. A doorbell conveys a pointer, not the command body.", "none", "NVME-PCIE-TRANSPORT-1.4"),
            c("INTERRUPT", "3.5", "13-16", "可用模式為 pin-based、single-message MSI、multiple-message MSI 與 MSI-X。規格建議 MSI-X；coalescing 可降低 interrupt rate，但通常增加 latency。Admin CQ 的 interrupt 不宜（should not）延遲。", "Modes are pin-based, single-message MSI, multiple-message MSI, and MSI-X. The specification recommends MSI-X. Coalescing can reduce interrupt rate at the cost of latency, and Admin-CQ interrupts should not be delayed.", "should", "NVME-PCIE-TRANSPORT-1.4"),
            c("POWER", "3.6", "16", "host 絕不可（shall never）選擇功耗高於 PCIe slot power limit 的 NVMe power state；違反時 power behavior 未定義。", "The host shall never select an NVMe power state whose consumption exceeds the PCIe slot power limit; violation results in undefined power behavior.", "shall", "NVME-PCIE-TRANSPORT-1.4"),
            c("ERROR", "3.7", "16", "NVMe command error 由 CQE status 回報；PCIe transport／link error 則依 PCIe 機制與本文件的 NVMe-specific 要求處理，兩者的 recovery 層級不同。", "NVMe command errors are reported in CQE status, while PCIe transport or link errors use PCIe mechanisms plus this document’s NVMe-specific requirements. Their recovery scopes differ.", "none", "NVME-PCIE-TRANSPORT-1.4"),
            c("CONFIG", "3.8.1-3.8.7", "16-35", "§3.8 逐欄定義 NVMe controller 的 PCI header、Power Management、MSI／MSI-X、PCIe capability 與 AER 額外要求。PCI／PCIe 原始欄位語意仍以 PCI-SIG 規格為準。", "Section 3.8 defines additional NVMe-controller requirements for the PCI header, Power Management, MSI/MSI-X, PCIe capability, and AER. Original PCI/PCIe field semantics remain governed by PCI-SIG specifications.", "none", "NVME-PCIE-TRANSPORT-1.4"),
            c("SECURITY", "3.8.8-3.8.10", "35-39", "power-loss signaling、confidential computing 與 TDISP 把平台事件或隔離狀態映射到 NVMe controller 行為；實作仍需要本次未提供的外部 PCIe／TDISP 規格。", "Power-loss signaling, confidential computing, and TDISP map platform events or isolation state to NVMe-controller behavior. Implementation still requires external PCIe/TDISP specifications not supplied for this report.", "none", "NVME-PCIE-TRANSPORT-1.4"),
            c("EOM", "3.9", "39-46", "Physical Interface Receiver Eye Opening Measurement log page 以 header、lane descriptor 與 EOM data 回報量測；host 先查支援與大小，再依 lane／parameter 解析。", "The Physical Interface Receiver Eye Opening Measurement log page reports measurements through a header, lane descriptors, and EOM data. The host checks support and size before parsing lanes and parameters.", "none", "NVME-PCIE-TRANSPORT-1.4"),
            c("HOST", "Annex A", "47-48", "Annex A 是 informative host checklist：提交時先寫 SQE 再 doorbell；完成時以 phase 判斷新 CQE，完成讀取後再推進 CQ head；interrupt handler 要處理同 vector 的所有相關 CQ。", "Annex A is an informative host checklist: write the SQE before its doorbell, use phase to identify a new CQE, advance CQ head after consumption, and service every relevant CQ associated with an interrupt vector.", "none", "NVME-PCIE-TRANSPORT-1.4"),
        ],
    },
}

EXCLUDED = {
    "base-ch1-2": {4, 8, 9, 10},
    "base-ch3": {29, 35, 72, 75, 76, 77, 78, 79, 82, 83},
    "base-ch4": {95, 96, 100, 106, 123, 124, 141},
    "pcie-transport-1.4": set(),
}
SCOPE_REDUCED = {
    "base-ch1-2": {1, 5},
    "base-ch3": {23, 28, 30, 31, 32, 33, 84, 85, 90, 91},
    "base-ch4": {117, 118},
    "pcie-transport-1.4": {1},
}


def artifact_ids(report_id: str) -> list[str]:
    key = {
        "base-ch1-2": "base12",
        "base-ch3": "base3",
        "base-ch4": "base4",
        "pcie-transport-1.4": "pcie14",
    }[report_id]
    return [
        f"{key}-tutorial-html",
        f"{key}-detailed-html",
        f"{key}-zh-md",
        f"{key}-en-md",
    ]


def cite(item: dict, language: str, figure: int | None = None) -> str:
    source = item["source_id"]
    rev = SOURCES[source]["revision"]
    fig = f", Figure {figure}" if figure is not None else ""
    if language == "en":
        return (
            f"Source: {source}, Rev. {rev}, §{item['section']}{fig}, "
            f"printed pages {item['printed_pages']}, PDF pages {item['pdf_pages']}"
        )
    return (
        f"來源：{source}, Rev. {rev}, §{item['section']}{fig}, "
        f"文件頁 {item['printed_pages']}, PDF 頁 {item['pdf_pages']}"
    )


def figure_explanation(caption: str, language: str) -> tuple[str, str, str]:
    low = caption.lower()
    if any(word in low for word in ("queue", "command processing", "phase tag")):
        kind = "queue"
    elif any(word in low for word in ("prp", "sgl", "data block", "descriptor")):
        kind = "pointer"
    elif any(word in low for word in ("status", "error", "warning")):
        kind = "status"
    elif any(
        word in low
        for word in (
            "offset",
            "register",
            "capabilit",
            "command dword",
            "format",
            "layout",
            "field",
        )
    ):
        kind = "field"
    elif any(
        word in low
        for word in (
            "namespace",
            "subsystem",
            "domain",
            "nvm set",
            "endurance",
            "capacity",
        )
    ):
        kind = "architecture"
    elif any(
        word in low
        for word in (
            "identifier",
            "vendor id",
            "serial number",
            "eui",
            "nguid",
            "uuid",
            "list",
        )
    ):
        kind = "identifier"
    elif any(word in low for word in ("interrupt", "msi", "msi-x")):
        kind = "interrupt"
    elif any(word in low for word in ("eye", "eom", "lane")):
        kind = "measurement"
    else:
        kind = "general"

    zh = {
        "queue": (
            "整理 queue／command 的關係或處理順序。",
            "依 host、SQ、controller、CQ 與 pointer／phase 的方向閱讀。",
            "先選一個 queue identifier，沿箭頭追蹤一筆 command 與 completion。",
        ),
        "pointer": (
            "說明資料 buffer 如何由 PRP／SGL 結構描述。",
            "逐一核對 address、offset、length、alignment 與下一層 pointer。",
            "用跨兩個 memory page 的 buffer 檢查第一個 offset 與後續 alignment。",
        ),
        "status": (
            "整理狀態、錯誤或其分類欄位。",
            "先讀類型與控制 bit，再在正確類型下解讀 code；保留值不自行賦義。",
            "以一筆失敗 CQE 為例，先解 SCT，再解 SC 與 DNR。",
        ),
        "field": (
            "整理欄位、位元或 register 配置。",
            "由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。",
            "讀取前先確認 capability，再以欄位寬度與遮罩解碼。",
        ),
        "architecture": (
            "說明 subsystem 物件的包含、連接或容量關係。",
            "分開辨認 controller、port、namespace、identifier 與容量階層。",
            "替單一 namespace 標出其 NSID、controller 與所屬容量階層。",
        ),
        "identifier": (
            "整理 identifier 或 list 的 byte layout 與範圍。",
            "先確認長度、byte order、數量欄位、唯一性範圍與保留區。",
            "parser 先驗證 count 與長度，再逐筆讀取 identifier。",
        ),
        "interrupt": (
            "說明 interrupt capability、vector 或通知行為。",
            "分開 capability 是否存在、enable 狀態、vector mapping 與 pending／mask。",
            "為兩個 Completion Queues 配置 vector，檢查是否共用及如何服務。",
        ),
        "measurement": (
            "整理 receiver eye measurement 的輸入、輸出或資料格式。",
            "先讀支援與大小，再依 lane、parameter、header 與 descriptor 解碼。",
            "先查回報長度，再只解析完整存在的 lane descriptor。",
        ),
        "general": (
            "提供本節概念、支援條件或範例的結構化索引。",
            "先看標題所指物件，再對照相鄰文字的條件、圖例與例外。",
            "選一個具體 controller 設定，逐項對照圖中的關係。",
        ),
    }
    en = {
        "queue": (
            "Organizes a queue or command relationship or processing sequence.",
            "Follow host, SQ, controller, CQ, and pointer or phase direction.",
            "Choose one queue identifier and trace one command and its completion.",
        ),
        "pointer": (
            "Shows how PRP or SGL structures describe a data buffer.",
            "Check address, offset, length, alignment, and next-level pointers in order.",
            "Use a buffer crossing two memory pages to check the first offset and later alignment.",
        ),
        "status": (
            "Organizes status or error fields and their classification.",
            "Read the type and control bits before decoding a code within that type; do not assign meaning to reserved values.",
            "For a failed CQE, decode SCT first, then SC and DNR.",
        ),
        "field": (
            "Organizes a field, bit, or register layout.",
            "Map offsets, bytes, or bits to names, access type, reset value, and conditions.",
            "Check capability support first, then decode using the specified width and mask.",
        ),
        "architecture": (
            "Shows containment, connection, or capacity relationships among subsystem objects.",
            "Keep controllers, ports, namespaces, identifiers, and capacity levels distinct.",
            "For one namespace, mark its NSID, controller, and capacity hierarchy.",
        ),
        "identifier": (
            "Organizes identifier or list byte layout and scope.",
            "Check length, byte order, count, uniqueness scope, and reserved area.",
            "A parser validates count and length before reading identifiers.",
        ),
        "interrupt": (
            "Shows interrupt capability, vector, or notification behavior.",
            "Separate capability presence, enable state, vector mapping, and pending or mask state.",
            "Assign vectors to two Completion Queues and check sharing and service behavior.",
        ),
        "measurement": (
            "Organizes receiver-eye measurement inputs, outputs, or data format.",
            "Check support and size before decoding lanes, parameters, headers, and descriptors.",
            "Read the returned length first and parse only complete lane descriptors.",
        ),
        "general": (
            "Provides a structured index to a concept, support condition, or example.",
            "Identify the named object, then read adjacent conditions, legend, and exceptions.",
            "Choose a concrete controller configuration and map it to the relationships shown.",
        ),
    }
    return (en if language == "en" else zh)[kind]


def flow_svg(report: dict) -> str:
    boxes = []
    arrows = []
    for index, label in enumerate(report["diagram"]):
        x = 10 + index * 180
        boxes.append(
            f'<rect x="{x}" y="35" width="150" height="70" rx="8" '
            f'fill="#f4f4f4" stroke="#333"/>'
            f'<text x="{x + 75}" y="75" text-anchor="middle" '
            f'font-size="14">{html.escape(label)}</text>'
        )
        if index < 3:
            arrows.append(
                f'<line x1="{x + 150}" y1="70" x2="{x + 178}" y2="70" '
                'stroke="#333" marker-end="url(#arrow)"/>'
            )
    return (
        '<svg width="100%" height="140" viewBox="0 0 720 140" role="img" '
        'aria-labelledby="flow-title flow-desc">'
        '<title id="flow-title">NVMe report flow</title>'
        f'<desc id="flow-desc">{html.escape(report["diagram_note_zh"])}</desc>'
        '<defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="6" '
        'refY="3" orient="auto"><path d="M0,0 L0,6 L7,3 z" fill="#333"/>'
        '</marker></defs>'
        + "".join(boxes + arrows)
        + "</svg>"
    )


def make_claim(report_id: str, report: dict, item: dict) -> dict:
    claim_id = f"{report['prefix']}-{item['key']}"
    result = {
        "id": claim_id,
        "report_id": report_id,
        "source_id": item["source_id"],
        "revision": SOURCES[item["source_id"]]["revision"],
        "section": item["section"],
        "figure": None,
        "table": None,
        "printed_pages": item["printed_pages"],
        "pdf_pages": item["pdf_pages"],
        "normative_keyword": item["normative_keyword"],
        "zh_tw": item["zh_tw"],
        "en": item["en"],
        "scope_entry_id": report["scope_entry"],
    }
    result["citation_zh_tw"] = cite(result, "zh")
    result["citation_en"] = cite(result, "en")
    return result


def make_figure_claim(report_id: str, report: dict, figure: dict) -> dict:
    figure_id = f"{report['prefix']}-FIG-{int(figure['number']):03d}"
    zh_parts = figure_explanation(figure["title"], "zh")
    en_parts = figure_explanation(figure["title"], "en")
    scope_zh = (
        " 本報告只解釋圖中的 PCIe／memory-based 部分。"
        if figure["mode"] == "scope-reduced"
        else ""
    )
    scope_en = (
        " This report explains only the PCIe/memory-based portion."
        if figure["mode"] == "scope-reduced"
        else ""
    )
    result = {
        "id": f"{figure_id}-CLAIM",
        "report_id": report_id,
        "source_id": report["source_id"],
        "revision": SOURCES[report["source_id"]]["revision"],
        "section": figure["section"],
        "figure": str(figure["number"]),
        "table": None,
        "printed_pages": figure["printed_pages"],
        "pdf_pages": figure["pdf_pages"],
        "normative_keyword": "none",
        "zh_tw": (
            f"Figure {figure['number']}〈{figure['title']}〉："
            f"{zh_parts[0]} {zh_parts[1]}{scope_zh}"
        ),
        "en": (
            f"Figure {figure['number']}, “{figure['title']}”: "
            f"{en_parts[0]} {en_parts[1]}{scope_en}"
        ),
        "scope_entry_id": report["scope_entry"],
    }
    result["citation_zh_tw"] = cite(result, "zh", int(figure["number"]))
    result["citation_en"] = cite(result, "en", int(figure["number"]))
    return result


def tutorial_check(report_id: str, claim_id: str) -> str:
    if any(key in claim_id for key in ("KEYWORD", "NUMBER", "DWORD")):
        return "先圈出 keyword、進位、單位與 bit／byte 編號，再開始解讀句子或欄位。"
    if any(key in claim_id for key in ("QUEUE", "COMMAND", "ORDER", "PROCESS")):
        return "畫出 host → SQ → controller → CQ，並在每一步標上由誰更新 pointer。"
    if any(key in claim_id for key in ("STORAGE", "SUBSYSTEM", "NAMESPACE", "MEDIA", "DOMAIN", "CAPACITY")):
        return "把 identifier 與實體／邏輯物件分開，再由 namespace 往上追到所屬容量階層。"
    if any(key in claim_id for key in ("INIT", "SHUTDOWN", "RESET", "STATIC")):
        return "先寫出目前 controller state，再核對哪個 register／property 觸發狀態轉換。"
    if any(key in claim_id for key in ("SQE", "CQE", "STATUS", "PHASE", "CID", "PSDT")):
        return "先定位 dword 與 bit 範圍，再決定這個欄位用於識別、資料指標或完成狀態。"
    if any(key in claim_id for key in ("PRP", "SGL", "LIST", "IDENTIFIER", "UTF8")):
        return "先驗證長度、alignment、type 與保留值，再沿 pointer 或 entry 順序解析。"
    if any(key in claim_id for key in ("MMIO", "DOORBELL", "CONFIG", "INTERRUPT", "POWER", "EOM")):
        return "先分辨欄位位於 PCI configuration space、MMIO register、host memory 或 log page。"
    return {
        "base-ch1-2": "先確認概念位於規格家族、儲存階層或路徑層級，不把不同層級合併。",
        "base-ch3": "先寫清楚動作主體是 host 或 controller，再核對當下 lifecycle state。",
        "base-ch4": "先定位資料結構的 byte／dword 邊界，再閱讀欄位條件。",
        "pcie-transport-1.4": "先找 Base 的通用規則，再疊加 PCIe Transport 的專屬限制。",
    }[report_id]


def render_html(
    report_id: str,
    report: dict,
    claims: list[dict],
    figures: list[dict],
    tutorial: bool,
) -> str:
    source_markers = [SOURCES[report["source_id"]]["marker"]]
    if report_id == "pcie-transport-1.4":
        source_markers.append(SOURCES["NVME-BASE-2.4"]["marker"])
    label = "新手教學版" if tutorial else "詳細 Spec 版"
    parts = [
        "<!doctype html>",
        '<html lang="zh-Hant-TW">',
        "<head>",
        '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        f"<title>{html.escape(report['title_zh'])}｜{label}</title>",
        "</head>",
        "<body>",
        '<nav aria-label="章節導覽"><a href="#scope">範圍</a> ｜ '
        '<a href="#map">流程圖</a> ｜ <a href="#claims">重點</a> ｜ '
        '<a href="#figures">Figure 逐圖導讀</a> ｜ '
        '<a href="#sources">來源</a></nav>',
        "<main>",
        f"<h1>{html.escape(report['title_zh'])}｜{label}</h1>",
        "<p>用途：供具備 PCIe 與 NVMe 基礎的工程人員在 iPad 離線閱讀，"
        "並作為 100 分鐘簡報的內容來源。</p>",
        '<section id="scope"><h2>範圍與閱讀方式</h2>',
        f"<p><strong>納入：</strong>{html.escape(report['range'])}。"
        "正文只保留 PCIe／memory-based 與通用 NVMe 內容；"
        "未納入主題不會出現在報告或 PPT。</p>",
        "<p><strong>Figure 政策：</strong>不重製規格原圖；以下逐張說明用途、"
        "讀法、條件與說明性範例。欄位表雖以表格呈現，"
        "在本範圍的規格中仍以 Figure 編號。</p>",
        "<table><thead><tr><th>keyword</th><th>台灣繁體中文</th>"
        "<th>強度</th></tr></thead><tbody>"
        "<tr><td>shall</td><td>必須</td><td>強制要求</td></tr>"
        "<tr><td>may</td><td>可、得</td><td>允許選擇</td></tr>"
        "<tr><td>should</td><td>宜、建議</td><td>有偏好的建議</td></tr>"
        "<tr><td>optional</td><td>選用</td>"
        "<td>不要求支援；實作後仍依定義</td></tr></tbody></table></section>",
        '<section id="map"><h2>整體流程圖</h2>',
        flow_svg(report),
        f"<p>{html.escape(report['diagram_note_zh'])}</p></section>",
        '<section id="claims"><h2>規格重點</h2>',
    ]
    core_claims = [item for item in claims if item["figure"] is None]
    for index, item in enumerate(core_claims, 1):
        heading = "先看懂" if tutorial else "規格結論"
        parts.extend(
            [
                f"<article><h3>{index}. {heading}</h3>",
                f'<p><span data-claim-id="{item["id"]}">'
                f'{html.escape(item["zh_tw"])}</span></p>',
                f"<p><small>{html.escape(item['citation_zh_tw'])}</small></p>"
                "</article>",
            ]
        )
        if tutorial:
            parts.insert(
                len(parts) - 1,
                "<p><strong>新手檢查點：</strong>"
                + html.escape(tutorial_check(report_id, item["id"]))
                + "</p>",
            )
        else:
            parts.insert(
                len(parts) - 1,
                "<dl><dt>Claim ID</dt><dd>"
                + html.escape(item["id"])
                + "</dd><dt>規範性 keyword</dt><dd>"
                + html.escape(item["normative_keyword"])
                + "</dd></dl>",
            )
    parts.append('</section><section id="figures"><h2>Figure 逐圖導讀</h2>')
    figure_claims = {
        int(item["figure"]): item for item in claims if item["figure"] is not None
    }
    for figure in figures:
        item = figure_claims[int(figure["number"])]
        purpose, reading, example = figure_explanation(figure["title"], "zh")
        parts.extend(
            [
                f'<article data-figure-table-id="{figure["id"]}">'
                f'<h3>Figure {figure["number"]}: '
                f'{html.escape(figure["title"])}</h3>',
                f'<p><span data-claim-id="{item["id"]}">'
                f'{html.escape(item["zh_tw"])}</span></p>',
                "<ul>",
                f"<li><strong>解決的問題：</strong>{html.escape(purpose)}</li>",
                f"<li><strong>閱讀順序：</strong>{html.escape(reading)}</li>",
                "<li><strong>規範語氣：</strong>本導讀不新增 shall／may／should；"
                "實際強度以同節文字與欄位描述為準。</li>",
                "<li><strong>說明性範例（informative example）：</strong>"
                f"{html.escape(example)}此例不新增規格要求。</li>",
            ]
        )
        if figure["mode"] == "scope-reduced":
            parts.append(
                "<li><strong>範圍：</strong>只介紹 PCIe／memory-based 部分。</li>"
            )
        if not tutorial:
            parts.append(
                "<li><strong>追溯鍵：</strong>"
                + html.escape(item["id"])
                + "；normative keyword：none（Figure 導讀本身不新增要求）。</li>"
            )
        parts.extend(
            [
                "</ul>",
                f"<p><small>{html.escape(item['citation_zh_tw'])}</small></p>"
                "</article>",
            ]
        )
    parts.extend(
        [
            "</section>",
            '<section id="sources"><h2>來源與限制</h2>',
            *[f"<p>{html.escape(marker)}</p>" for marker in source_markers],
            "<p>查證日期：2026-08-29。目前未納入其他 Errata、ECN、"
            "Technical Proposal、controller vendor 文件或未提供的 "
            "PCI Express Base Specification 原文；PCIe 原生語意只轉述"
            "本次來源明載的 NVMe-specific requirement。</p>",
            "</section>",
            "</main>",
            "</body>",
            "</html>",
            "",
        ]
    )
    return "\n".join(parts)


def frontmatter(title: str, description: str) -> str:
    return f"""---
layout: post
read_time: true
show_date: true
title: "{title}"
date: 2026-08-28
description: "{description}"
tags: [NVMe, PCIe, Specification]
category: NVMe
author: Jia-Chang
github: JiaChangGit/JiaChangGit.github.io/tree/main/DOCS/nvme-spec-report
toc: yes
---
"""


def render_markdown(
    report_id: str,
    report: dict,
    claims: list[dict],
    figures: list[dict],
    language: str,
) -> str:
    english = language == "en"
    title = report["title_en"] if english else report["title_zh"]
    description = (
        "Source-located PCIe/NVMe report for PPT authoring."
        if english
        else "供 GitHub Pages 與 PPT 使用的 NVMe 規格導讀。"
    )
    fence = chr(96) * 3
    out = [
        frontmatter(title, description),
        f"# {title}",
        "",
        (
            "Purpose: a source-located engineering report for GitHub Pages "
            "and a 100-minute presentation."
            if english
            else "用途：供 GitHub Pages 閱讀與 100 分鐘簡報製作；"
            "讀者已具備 PCIe 與 NVMe 基礎。"
        ),
        "",
        (
            "Scope: "
            + report["range_en"]
            + ". Only PCIe/memory-based and common NVMe content appears below."
            if english
            else "範圍：" + report["range"] + "。正文只保留 PCIe／memory-based "
            "與通用 NVMe 內容。"
        ),
        "",
        "## " + ("Source versions" if english else "來源版本"),
        "",
        SOURCES[report["source_id"]]["marker"],
    ]
    if report_id == "pcie-transport-1.4":
        out.append(SOURCES["NVME-BASE-2.4"]["marker"])
    out.extend(
        [
            "",
            (
                "Verification date: 2026-08-29. No additional errata, ECNs, "
                "Technical Proposals, controller-vendor documents, or source text "
                "from the external PCI Express Base Specification are included."
                if english
                else "查證日期：2026-08-29。目前未納入其他 Errata、ECN、"
                "Technical Proposal、controller vendor 文件或未提供的 "
                "PCI Express Base Specification 原文。"
            ),
            "",
            "## " + ("Reading map" if english else "閱讀地圖"),
            "",
            fence + "text",
            " -> ".join(report["diagram"]),
            fence,
            "",
            report["diagram_note_en"] if english else report["diagram_note_zh"],
            "",
            "## " + ("Normative language" if english else "規範性用語"),
            "",
            (
                "shall is mandatory, may permits a choice, should expresses a "
                "preferred recommendation, and optional means support is not "
                "required. The report preserves these terms and never promotes "
                "one into another."
                if english
                else "shall 譯為「必須」，may 譯為「可／得」，should 譯為"
                "「宜／建議」，optional 譯為「選用」。本文不提高或降低原文語氣。"
            ),
            "",
            "## " + ("Specification findings" if english else "規格重點"),
            "",
        ]
    )
    core_claims = [item for item in claims if item["figure"] is None]
    for index, item in enumerate(core_claims, 1):
        text = item["en"] if english else item["zh_tw"]
        citation = item["citation_en"] if english else item["citation_zh_tw"]
        out.extend(
            [
                f"### {index}. {item['id']}",
                "",
                f"<!-- claim:{item['id']} -->",
                "",
                text,
                "",
                f"> {citation}",
                "",
            ]
        )
    out.extend(
        [
            "## " + ("Figure-by-Figure Guide" if english else "Figure 逐圖導讀"),
            "",
            (
                "The source uses Figure numbers for both diagrams and field-layout "
                "tables. No source artwork is reproduced."
                if english
                else "本範圍的規格以 Figure 編號同時涵蓋示意圖與欄位表；"
                "本文不重製原圖。"
            ),
            "",
        ]
    )
    figure_claims = {
        int(item["figure"]): item for item in claims if item["figure"] is not None
    }
    for figure in figures:
        item = figure_claims[int(figure["number"])]
        purpose, reading, example = figure_explanation(figure["title"], language)
        statement = item["en"] if english else item["zh_tw"]
        citation = item["citation_en"] if english else item["citation_zh_tw"]
        out.extend(
            [
                f"### Figure {figure['number']}: {figure['title']}",
                "",
                f"<!-- claim:{item['id']} figure-table:{figure['id']} -->",
                "",
                statement,
                "",
                "- Purpose: " + purpose
                if english
                else "- 解決的問題：" + purpose,
                "",
                "- How to read: " + reading
                if english
                else "- 閱讀順序：" + reading,
                "",
                (
                    "- Normative force: this guide adds no shall, may, or should; "
                    "use the adjacent source text and field descriptions."
                    if english
                    else "- 規範語氣：本導讀不新增 shall／may／should；"
                    "實際強度以同節文字與欄位描述為準。"
                ),
                "",
                (
                    "- Informative example: "
                    + example
                    + " This example adds no requirement."
                    if english
                    else "- 說明性範例（informative example）："
                    + example
                    + "此例不新增規格要求。"
                ),
                "",
            ]
        )
        if figure["mode"] == "scope-reduced":
            out.extend(
                [
                    (
                        "- Scope: only the PCIe/memory-based portion is introduced."
                        if english
                        else "- 範圍：只介紹 PCIe／memory-based 部分。"
                    ),
                    "",
                ]
            )
        out.extend([f"> {citation}", ""])
    out.extend(
        [
            "## " + ("Use and limitations" if english else "使用與限制"),
            "",
            (
                "Use the claim IDs as stable PPT traceability keys. Re-check "
                "affected claims if the source revision, errata set, or approved "
                "scope changes."
                if english
                else "製作 PPT 時以 claim ID 作為追溯鍵。來源 revision、Errata "
                "集合或核准範圍改變時，必須重新核對受影響 claim。"
            ),
            "",
        ]
    )
    return "\n".join(out)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--inventory",
        type=Path,
        default=ROOT / "tmp" / "pdfs" / "nvme-report" / "inventory.json",
    )
    args = parser.parse_args()
    inventory = json.loads(args.inventory.read_text(encoding="utf-8"))["reports"]
    contract = json.loads(
        (CONTROL / "output-contract.json").read_text(encoding="utf-8")
    )
    artifacts = {item["id"]: item for item in contract["artifacts"]}
    all_claims = []
    register_entries = []

    for report_id, report in REPORTS.items():
        figures = []
        for raw in inventory[report_id]["figures"]:
            number = int(raw["number"])
            excluded = number in EXCLUDED[report_id]
            mode = (
                "excluded"
                if excluded
                else (
                    "scope-reduced"
                    if number in SCOPE_REDUCED[report_id]
                    else "full"
                )
            )
            figure_id = f"{report['prefix']}-FIG-{number:03d}"
            if excluded:
                exclusion_scope = report["scope_entry"].replace(
                    "-INCLUDE", "-FABRIC-EXCLUDE"
                )
            else:
                exclusion_scope = report["scope_entry"]
            entry = {
                "id": figure_id,
                "report_id": report_id,
                "source_id": report["source_id"],
                "type": "Figure",
                "number": str(number),
                "title": raw["caption"],
                "section": raw["section"],
                "printed_pages": raw["printed_pages"],
                "pdf_pages": raw["pdf_pages"],
                "scope_entry_id": exclusion_scope,
                "scope_status": "EXCLUDE" if excluded else "INCLUDE",
                "mode": mode,
                "required_artifact_ids": []
                if excluded
                else artifact_ids(report_id),
                "introduced_in": [] if excluded else artifact_ids(report_id),
            }
            register_entries.append(entry)
            if not excluded:
                figures.append(entry)
        report_claims = [
            make_claim(report_id, report, item) for item in report["claims"]
        ]
        report_claims.extend(
            make_figure_claim(report_id, report, item) for item in figures
        )
        all_claims.extend(report_claims)

        ids = artifact_ids(report_id)
        output_text = {
            ids[0]: render_html(report_id, report, report_claims, figures, True),
            ids[1]: render_html(report_id, report, report_claims, figures, False),
            ids[2]: render_markdown(
                report_id, report, report_claims, figures, "zh"
            ),
            ids[3]: render_markdown(
                report_id, report, report_claims, figures, "en"
            ),
        }
        for artifact_id, content in output_text.items():
            path = ROOT / artifacts[artifact_id]["path"]
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")

    claims_doc = {
        "schema_version": 2,
        "allowed_normative_keywords": [
            "mandatory",
            "may",
            "obsolete",
            "optional",
            "reserved",
            "shall",
            "should",
            "none",
        ],
        "claims": all_claims,
    }
    figures_doc = {"schema_version": 2, "entries": register_entries}
    (CONTROL / "claims.json").write_text(
        json.dumps(claims_doc, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (CONTROL / "figure-table-register.json").write_text(
        json.dumps(figures_doc, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        f"Built 16 artifacts, {len(all_claims)} claims, "
        f"and {len(register_entries)} Figure records"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
