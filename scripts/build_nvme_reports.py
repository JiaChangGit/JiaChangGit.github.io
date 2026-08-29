#!/usr/bin/env python3
"""Build four NVMe reports from the local, gitignored source inventory."""

from __future__ import annotations

import argparse
import html
import json
import re
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
        "title_en": "NVMe Base 2.4 Chapters 1-2: Specification Language, PCIe Queues, and Storage Model",
        "source_id": "NVME-BASE-2.4",
        "scope_entry": "BASE12-INCLUDE",
        "range": "§1-§2；文件頁 1-37；PDF 頁 27-63",
        "range_en": "§1-§2; printed pages 1-37; PDF pages 27-63",
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
        "range": "§3；文件頁 38-138；PDF 頁 64-164",
        "range_en": "§3; printed pages 38-138; PDF pages 64-164",
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
        "range": "§4；文件頁 139-175；PDF 頁 165-201",
        "range_en": "§4; printed pages 139-175; PDF pages 165-201",
        "diagram": ["64-byte SQE", "PRP or SGL", "Command execution", "16-byte+ CQE"],
        "diagram_note_zh": "SQE 以 CID 與 SQID 識別 command，data pointer 描述 buffer；CQE 回報 SQ head、SQID、CID、phase 與 status。",
        "diagram_note_en": "The SQE identifies a command with CID plus SQID and describes buffers through data pointers; the CQE reports SQ head, SQID, CID, phase, and status.",
        "claims": [
            c("SQE", "4.1.1", "139-143", "Admin 與 I/O common SQE 固定為 64 bytes。CDW0、NSID、data pointer 與 CDW10-15 的通用位置先固定，再由各 command 定義命令專屬內容。", "The common Admin and I/O SQE is 64 bytes. CDW0, NSID, data pointers, and CDW10-15 establish the common layout before each command defines command-specific content."),
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
        "range": "§1-§3 與 Annex A；文件頁／PDF 頁 1-48",
        "range_en": "§1-§3 and Annex A; printed/PDF pages 1-48",
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

POST_IMAGES = {
    "base-ch1-2": {
        "zh": "posts/2026/dogMC_title.jpg",
        "en": "posts/2026/cat_title.jpg",
    },
    "base-ch3": {
        "zh": "posts/2026/dogMC_title.jpg",
        "en": "posts/2026/cat_title.jpg",
    },
    "base-ch4": {
        "zh": "posts/2026/dogMC_title.jpg",
        "en": "posts/2026/cat_title.jpg",
    },
    "pcie-transport-1.4": {
        "zh": "posts/2026/lion_title.jpg",
        "en": "posts/2026/catFlower_title.jpg",
    },
}

CORE_TITLES = {
    "BASE12-FAMILY": ("NVMe 規格家族的分工", "Roles in the NVMe specification family"),
    "BASE12-KEYWORDS": ("規範性用語的強度", "Normative keyword strength"),
    "BASE12-NUMBERS": ("進位與容量單位", "Radix and capacity units"),
    "BASE12-DWORD": ("byte、word 與 dword", "Byte, word, and dword relationships"),
    "BASE12-QUEUE": ("PCIe queue pair 模型", "PCIe queue-pair model"),
    "BASE12-STORAGE": ("NVM 儲存階層", "NVM storage hierarchy"),
    "BASE12-COMMANDSET": ("Admin 與 I/O Command Set", "Admin and I/O Command Sets"),
    "BASE12-SUBSYSTEM": ("subsystem 物件與 NSID", "Subsystem objects and NSIDs"),
    "BASE12-MULTIPATH": ("multi-path 與 namespace sharing", "Multi-path and namespace sharing"),
    "BASE12-ASYMMETRY": ("非對稱路徑特性", "Asymmetric path characteristics"),
    "BASE3-STATIC": ("static controller model", "Static controller model"),
    "BASE3-TYPES": ("I/O 與 Administrative controller", "I/O and Administrative controllers"),
    "BASE3-ORDER": ("命令與完成順序", "Command and completion ordering"),
    "BASE3-PROPERTY": ("property 存取寬度", "Property access width"),
    "BASE3-NAMESPACE": ("NSID 狀態與特殊值", "NSID states and special values"),
    "BASE3-MEDIA": ("媒體與回收階層", "Media and reclamation hierarchy"),
    "BASE3-DOMAIN": ("domain 邊界與識別碼", "Domain boundaries and identifiers"),
    "BASE3-QUEUE": ("PCIe queue 建立與 pointer", "PCIe queue creation and pointers"),
    "BASE3-PROCESS": ("命令處理與 arbitration", "Command processing and arbitration"),
    "BASE3-INIT": ("controller 初始化", "Controller initialization"),
    "BASE3-SHUTDOWN": ("shutdown 狀態流程", "Shutdown state flow"),
    "BASE3-RESET": ("reset 層級與影響範圍", "Reset levels and scope"),
    "BASE3-CAPACITY": ("capacity model", "Capacity model"),
    "BASE3-KEEPALIVE": ("Keep Alive timer", "Keep Alive timers"),
    "BASE3-FIRMWARE": ("firmware update 與 privileged action", "Firmware updates and privileged actions"),
    "BASE4-SQE": ("common SQE 配置", "Common SQE layout"),
    "BASE4-CID": ("CID 唯一性", "CID uniqueness"),
    "BASE4-PSDT": ("PRP／SGL 選擇", "PRP/SGL selection"),
    "BASE4-CQE": ("common CQE 與 Phase Tag", "Common CQE and Phase Tag"),
    "BASE4-STATUS": ("SCT、SC 與 DNR", "SCT, SC, and DNR"),
    "BASE4-PHASE": ("Completion Queue phase", "Completion Queue phase"),
    "BASE4-PRP": ("PRP alignment 與 page", "PRP alignment and pages"),
    "BASE4-SGL": ("SGL descriptor 與 length", "SGL descriptors and length"),
    "BASE4-FEATURE": ("Feature value 與 persistence", "Feature values and persistence"),
    "BASE4-IDENTIFIER": ("全域識別碼的範圍", "Scope of global identifiers"),
    "BASE4-LISTS": ("Controller／Namespace List", "Controller and Namespace Lists"),
    "BASE4-UTF8": ("UTF-8 輸入驗證", "UTF-8 input validation"),
    "PCIE14-SCOPE": ("Transport 與 Base 的優先序", "Transport and Base precedence"),
    "PCIE14-CONVENTION": ("PCIe Reset 欄定義", "PCIe Reset-column convention"),
    "PCIE14-KEYWORDS": ("Transport 規範性用語", "Transport normative language"),
    "PCIE14-OVERVIEW": ("PCIe transport 概觀", "PCIe transport overview"),
    "PCIE14-MMIO": ("BAR 與 register 存取", "BAR and register access"),
    "PCIE14-DOORBELL": ("SQ／CQ doorbell offset", "SQ/CQ doorbell offsets"),
    "PCIE14-QUEUE": ("queue 與 interrupt vector", "Queues and interrupt vectors"),
    "PCIE14-RESET": ("PCIe reset recovery", "PCIe reset recovery"),
    "PCIE14-COMMAND": ("PCIe command flow", "PCIe command flow"),
    "PCIE14-INTERRUPT": ("interrupt 模式與延遲", "Interrupt modes and delay"),
    "PCIE14-POWER": ("slot power limit", "Slot power limit"),
    "PCIE14-ERROR": ("NVMe 與 PCIe error 分層", "NVMe and PCIe error layers"),
    "PCIE14-CONFIG": ("PCI configuration requirements", "PCI configuration requirements"),
    "PCIE14-SECURITY": ("平台安全與隔離依賴", "Platform security and isolation dependencies"),
    "PCIE14-EOM": ("receiver eye measurement", "Receiver-eye measurement"),
    "PCIE14-HOST": ("host implementation checklist", "Host implementation checklist"),
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


def figure_explanation(figure: dict, language: str) -> dict[str, str]:
    """Return a source-specific, non-verbatim guide for one Figure."""

    title = figure["title"]
    lower_title = title.lower()
    number = figure["number"]
    items = list(figure.get("key_items", []))
    item_text = ", ".join(items)
    first = items[0] if items else title
    keywords = list(figure.get("source_keywords", []))
    keyword_text = ", ".join(f"`{item}`" for item in keywords) or "none"

    offset = re.match(
        r"^Offset\s+([^:]+):\s*([A-Z0-9-]+)\s+-\s+(.+)$", title
    )
    dword = re.match(r"^(.+?)\s+-\s+Command Dword\s+([0-9-]+)$", title)
    second = (
        items[1]
        if len(items) > 1
        else ("the cited condition" if language == "en" else "引用條件")
    )

    if language == "en":
        if offset:
            location, symbol, name = offset.groups()
            purpose = (
                f"Defines {symbol} ({name}) at offset {location} and identifies "
                "the fields that software must decode at that location."
            )
            reading = (
                f"Start at {symbol}, then map bit ranges to access type, reset value, "
                f"and field meaning. Evidence index: {item_text}."
            )
            example = (
                f"Read {symbol} with the required width, then verify {first} and "
                f"{second} separately before using either value."
            )
        elif dword:
            command, index = dword.groups()
            purpose = (
                f"Defines command-specific fields in CDW{index} for {command}."
            )
            reading = (
                f"Locate CDW{index}, then decode the named fields without borrowing "
                f"semantics from another command. Evidence index: {item_text}."
            )
            example = (
                f"Build one {command} entry, set {first}, and independently validate "
                f"{second} before ringing the Submission Queue doorbell."
            )
        elif "family of specifications" in lower_title or "types of nvme command sets" in lower_title:
            purpose = f"Places {title} in the NVMe document and command-set hierarchy."
            reading = (
                "Read from the common Base requirements toward the transport and command-set layer; "
                f"keep these source-derived labels distinct: {item_text}."
            )
            example = (
                f"Start with {first}, then follow the branch containing {second}; cite the document "
                "that owns the requirement instead of assuming every layer defines it."
            )
        elif "decimal and binary units" in lower_title or "byte, word, and dword" in lower_title:
            purpose = f"Defines the numeric-unit or byte-width convention illustrated by {title}."
            reading = (
                f"Separate decimal units from binary units and preserve byte/word/Dword boundaries. Evidence index: {item_text}."
            )
            example = (
                f"Normalize one value using {first}, then verify its storage width against {second} before comparing it."
            )
        elif "support requirements" in lower_title:
            purpose = f"Summarizes the support levels assigned by {title}."
            reading = (
                f"Resolve the row and controller/command-set context before interpreting its support marker. Evidence index: {item_text}."
            )
            example = (
                f"Look up {first} in the applicable row, then confirm the context identified by {second} before labeling it required or optional."
            )
        elif "status code" in lower_title or "error" in lower_title:
            purpose = f"Defines the status/error classification represented by {title}."
            reading = (
                "Resolve the category before the individual code or flag; keep "
                f"reserved values uninterpreted. Evidence index: {item_text}."
            )
            example = (
                f"For one reported condition, identify {first} first and then check "
                f"{second} instead of decoding an isolated numeric value."
            )
        elif any(word in lower_title for word in ("layout", "format", "definition", "descriptor", "field", "register", "values", "structure", "capabilit", "configuration space", "command dword")):
            purpose = f"Defines the concrete layout or value relationships for {title}."
            reading = (
                "Follow byte/bit order, length, access type, and reserved areas; "
                f"the source-derived evidence index is {item_text}."
            )
            example = (
                f"Use {first} as the first parser checkpoint and {second} as a second, "
                "independent boundary check."
            )
        elif any(word in lower_title for word in ("identifier", "controller ids", "nsid types", "serial number", "model number", "oui", "eui64", "nguid", "uuid", "wwn")):
            purpose = f"Defines the identifier composition or namespace of values shown by {title}."
            reading = (
                f"Keep the value width, issuing authority, uniqueness scope, and reserved values separate. Evidence index: {item_text}."
            )
            example = (
                f"Parse {first} at its defined width, then validate the scope associated with {second} before using it as an identity key."
            )
        elif "virtualization" in lower_title or "sr-iov" in lower_title:
            purpose = f"Shows the Physical Function and Virtual Function relationships in {title}."
            reading = (
                f"Separate PCIe Function identity, controller ownership, and shared device resources. Evidence index: {item_text}."
            )
            example = (
                f"Start at the function represented by {first}, then trace its relationship to {second} without treating shared resources as private."
            )
        elif "queue" in lower_title or "command processing" in lower_title or "phase tag" in lower_title:
            purpose = f"Shows the queue or command relationship expressed by {title}."
            reading = (
                "Trace ownership and direction from host to SQ, controller, and CQ; "
                f"keep the indexed elements distinct: {item_text}."
            )
            example = (
                f"Trace one command through Figure {number}, using {first} and "
                f"{second} as checkpoints for ownership or pointer movement."
            )
        elif any(word in lower_title for word in ("namespace", "subsystem", "domain", "nvm set", "endurance", "capacity", "controller types", "storage hierarchy", "logical view of non-volatile storage")):
            purpose = f"Shows the object or capacity relationships in {title}."
            reading = (
                "Separate logical identifiers from controllers, namespaces, ports, "
                f"and capacity containers. Evidence index: {item_text}."
            )
            example = (
                f"Choose one object labeled by {first} and trace its relationship to "
                f"{second} without treating an identifier as the object itself."
            )
        elif "arbitration" in lower_title:
            purpose = f"Shows how {title} selects work from competing Submission Queues."
            reading = (
                f"Track priority class, service order, and the point at which the arbiter selects the next command. Evidence index: {item_text}."
            )
            example = (
                f"Compare queues represented by {first} and {second}, then advance only the queue chosen by the stated arbitration rule."
            )
        elif any(word in lower_title for word in ("shutdown", "timeout", "after reset", "power state", "reset sequence", "initialization sequence")):
            purpose = f"Shows the state or timing progression represented by {title}."
            reading = (
                f"Follow the states or time bounds in arrow order and identify which actor observes each transition. Evidence index: {item_text}."
            )
            example = (
                f"Begin at {first}, record the transition that reaches {second}, and evaluate timeout or reset behavior only at the stated boundary."
            )
        elif "privileged action" in lower_title:
            purpose = f"Identifies the privileged-operation boundary illustrated by {title}."
            reading = (
                f"Separate the requesting command from the privilege or controller state that authorizes it. Evidence index: {item_text}."
            )
            example = (
                f"Check {first} first, then verify the authorization condition associated with {second} before issuing the operation."
            )
        elif any(word in lower_title for word in ("prp entry", "prp list", "sgl segment", "sgl data block", "sgl bit bucket", "sgl read example")):
            purpose = f"Shows how {title} maps a transfer onto host-memory locations."
            reading = (
                f"Follow address, length, page/segment boundaries, and the link to the next entry in order. Evidence index: {item_text}."
            )
            example = (
                f"Map a transfer beginning at {first}, then verify the boundary or next element identified by {second} before continuing."
            )
        elif any(word in lower_title for word in ("interrupt", "msi", "msi-x", "pin based")):
            purpose = f"Shows the interrupt delivery or masking relationship represented by {title}."
            reading = (
                f"Trace the vector/message source, mask state, and delivery destination separately. Evidence index: {item_text}."
            )
            example = (
                f"Select the source represented by {first}, then confirm the mask or vector condition represented by {second} before expecting delivery."
            )
        elif "transport protocol layers" in lower_title:
            purpose = f"Separates the responsibilities of the protocol layers in {title}."
            reading = (
                f"Read vertically by layer and horizontally by peer interaction; do not assign a transport rule to the Base layer. Evidence index: {item_text}."
            )
            example = (
                f"Start with {first}, follow the operation to {second}, and cite the layer that defines the observed behavior."
            )
        elif "utf-8" in lower_title:
            purpose = f"Shows the input-validation sequence required by {title}."
            reading = (
                f"Follow decoding, prohibited-code-point, and truncation checks in order. Evidence index: {item_text}."
            )
            example = (
                f"Validate {first} first and reject the input if the check associated with {second} fails before accepting the string."
            )
        elif "eye" in lower_title or "eve diagram" in lower_title or "eom" in lower_title or "lane" in lower_title:
            purpose = f"Shows the receiver-eye measurement information in {title}."
            reading = (
                "Confirm support and returned length before interpreting lane, "
                f"parameter, header, or descriptor data. Evidence index: {item_text}."
            )
            example = (
                f"Check that {first} is present, then parse {second} only when the "
                "returned structure is long enough."
            )
        else:
            purpose = f"Explains the specific relationship or example named {title}."
            reading = (
                f"Use the source-derived elements {item_text} as checkpoints and "
                "apply only the conditions in the cited section."
            )
            example = (
                f"Create a review row for Figure {number}, verify {first}, then verify "
                f"{second} against the cited section."
            )
        caveat = (
            f"Source keyword index: {keyword_text}. The index locates normative "
            "language but does not replace the condition attached to each field."
            if keywords
            else "The Figure is explanatory or structural; this guide does not turn its visual relationship into a new requirement."
        )
    else:
        if offset:
            location, symbol, name = offset.groups()
            purpose = (
                f"定義 offset {location} 的 {symbol}（{name}），並指出軟體在該位置"
                "必須分別解碼的欄位。"
            )
            reading = (
                f"先定位 {symbol}，再把 bit range 對到 access type、reset value 與欄位"
                f"語意；來源欄位索引：{item_text}。"
            )
            example = (
                f"依規定寬度讀取 {symbol}，先獨立驗證 {first}，再驗證 {second}，"
                "確認後才使用欄位值。"
            )
        elif dword:
            command, index = dword.groups()
            purpose = f"定義 {command} 在 CDW{index} 的 command-specific 欄位。"
            reading = (
                f"先定位 CDW{index}，再依本命令定義解碼，不借用其他 command 的語意；"
                f"來源欄位索引：{item_text}。"
            )
            example = (
                f"建立一筆 {command}，設定 {first} 後再獨立驗證 {second}，確認完成才"
                "更新 Submission Queue doorbell。"
            )
        elif "family of specifications" in lower_title or "types of nvme command sets" in lower_title:
            purpose = f"定位〈{title}〉在 NVMe 文件與 command set 階層中的位置。"
            reading = (
                f"由共通 Base 要求往 transport 與 command set 分支閱讀，並分開核對：{item_text}。"
            )
            example = (
                f"先從 {first} 出發，再沿包含 {second} 的分支找定義來源，不假設每一層都重複定義同一要求。"
            )
        elif "decimal and binary units" in lower_title or "byte, word, and dword" in lower_title:
            purpose = f"定義〈{title}〉使用的數值單位或 byte 寬度慣例。"
            reading = (
                f"分開十進位與二進位單位，並保留 byte／word／Dword 邊界；來源索引：{item_text}。"
            )
            example = (
                f"先依 {first} 正規化一個數值，再用 {second} 核對儲存寬度後才進行比較。"
            )
        elif "support requirements" in lower_title:
            purpose = f"統整〈{title}〉指定的支援等級。"
            reading = (
                f"先確認 row 與 controller／command-set 上下文，再解讀 support marker；來源索引：{item_text}。"
            )
            example = (
                f"先在適用 row 查找 {first}，再核對 {second} 所代表的上下文，最後才判斷必須或選用。"
            )
        elif "status code" in lower_title or "error" in lower_title:
            purpose = f"定義〈{title}〉所表示的 status／error 分類。"
            reading = (
                f"先判斷類別，再解個別 code 或 flag；保留值不自行賦義。來源欄位索引：{item_text}。"
            )
            example = (
                f"收到一筆狀態時先辨認 {first}，再檢查 {second}，不可脫離類別單看數值。"
            )
        elif any(word in lower_title for word in ("layout", "format", "definition", "descriptor", "field", "register", "values", "structure", "capabilit", "configuration space", "command dword")):
            purpose = f"定義〈{title}〉的實際配置或數值關係。"
            reading = (
                f"依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：{item_text}。"
            )
            example = (
                f"以 {first} 作為 parser 的第一個檢查點，再用 {second} 獨立檢查另一個邊界。"
            )
        elif any(word in lower_title for word in ("identifier", "controller ids", "nsid types", "serial number", "model number", "oui", "eui64", "nguid", "uuid", "wwn")):
            purpose = f"定義〈{title}〉的識別碼組成或數值空間。"
            reading = (
                f"分開數值寬度、核發來源、唯一性範圍與保留值；來源索引：{item_text}。"
            )
            example = (
                f"依定義寬度解析 {first}，再核對 {second} 的唯一性範圍後才把它當成 identity key。"
            )
        elif "virtualization" in lower_title or "sr-iov" in lower_title:
            purpose = f"呈現〈{title}〉中 Physical Function 與 Virtual Function 的關係。"
            reading = (
                f"分開 PCIe Function identity、controller ownership 與 shared device resource；來源索引：{item_text}。"
            )
            example = (
                f"從 {first} 所代表的 Function 出發，再追到 {second}，不要把 shared resource 誤當成 private resource。"
            )
        elif "queue" in lower_title or "command processing" in lower_title or "phase tag" in lower_title:
            purpose = f"呈現〈{title}〉中的 queue 或 command 關係。"
            reading = (
                f"沿 host、SQ、controller、CQ 的擁有者與方向閱讀，並分開追蹤：{item_text}。"
            )
            example = (
                f"沿 Figure {number} 追蹤一筆 command，以 {first} 與 {second} 作為擁有者或 pointer 變動檢查點。"
            )
        elif any(word in lower_title for word in ("namespace", "subsystem", "domain", "nvm set", "endurance", "capacity", "controller types", "storage hierarchy", "logical view of non-volatile storage")):
            purpose = f"呈現〈{title}〉中的物件或容量關係。"
            reading = (
                f"將邏輯 identifier、controller、namespace、port 與容量容器分開；來源索引：{item_text}。"
            )
            example = (
                f"選擇 {first} 標示的一個物件，再追到 {second}，過程中不把 identifier 當成物件本身。"
            )
        elif "arbitration" in lower_title:
            purpose = f"呈現〈{title}〉如何在多個 Submission Queue 間選擇工作。"
            reading = (
                f"分別追蹤 priority class、服務順序與 arbiter 選出下一筆 command 的時點；來源索引：{item_text}。"
            )
            example = (
                f"比較 {first} 與 {second} 所代表的 queue，再只推進由規定 arbitration rule 選中的 queue。"
            )
        elif any(word in lower_title for word in ("shutdown", "timeout", "after reset", "power state", "reset sequence", "initialization sequence")):
            purpose = f"呈現〈{title}〉的狀態或時間推進關係。"
            reading = (
                f"依箭頭順序追蹤 state 或 time bound，並標出每個 transition 的觀察者；來源索引：{item_text}。"
            )
            example = (
                f"從 {first} 開始，記錄到達 {second} 的 transition，只在規定邊界判斷 timeout 或 reset 行為。"
            )
        elif "privileged action" in lower_title:
            purpose = f"界定〈{title}〉所示的 privileged operation 邊界。"
            reading = (
                f"分開發出 command 的主體，以及授權該操作的 privilege／controller state；來源索引：{item_text}。"
            )
            example = (
                f"先核對 {first}，再確認 {second} 對應的授權條件成立後才發出操作。"
            )
        elif any(word in lower_title for word in ("prp entry", "prp list", "sgl segment", "sgl data block", "sgl bit bucket", "sgl read example")):
            purpose = f"呈現〈{title}〉如何把 transfer 對映到 host memory。"
            reading = (
                f"依序追蹤 address、length、page／segment boundary 與下一個 entry 的連結；來源索引：{item_text}。"
            )
            example = (
                f"從 {first} 所示位置開始對映 transfer，再核對 {second} 的邊界或下一個元素後才繼續。"
            )
        elif any(word in lower_title for word in ("interrupt", "msi", "msi-x", "pin based")):
            purpose = f"呈現〈{title}〉中的 interrupt 傳遞或 masking 關係。"
            reading = (
                f"分開追蹤 vector／message 來源、mask 狀態與傳遞目的端；來源索引：{item_text}。"
            )
            example = (
                f"選定 {first} 所代表的來源，再確認 {second} 對應的 mask 或 vector 條件後才預期 interrupt 送達。"
            )
        elif "transport protocol layers" in lower_title:
            purpose = f"分開〈{title}〉中各 protocol layer 的責任。"
            reading = (
                f"垂直按 layer、水平按 peer interaction 閱讀，不把 transport rule 歸到 Base layer；來源索引：{item_text}。"
            )
            example = (
                f"先從 {first} 出發，再沿操作追到 {second}，最後引用真正定義該行為的 layer。"
            )
        elif "utf-8" in lower_title:
            purpose = f"呈現〈{title}〉要求的輸入驗證順序。"
            reading = (
                f"依序執行 decoding、禁止 code point 與 truncation 檢查；來源索引：{item_text}。"
            )
            example = (
                f"先驗證 {first}；若 {second} 對應的檢查失敗，就在接受字串前拒絕輸入。"
            )
        elif "eye" in lower_title or "eve diagram" in lower_title or "eom" in lower_title or "lane" in lower_title:
            purpose = f"呈現〈{title}〉中的 receiver-eye measurement 資訊。"
            reading = (
                f"先確認支援與回傳長度，再解 lane、parameter、header 或 descriptor；來源索引：{item_text}。"
            )
            example = (
                f"先確認 {first} 已存在，只有在回傳結構長度足夠時才繼續解析 {second}。"
            )
        else:
            purpose = f"解釋〈{title}〉所指的特定關係或範例。"
            reading = (
                f"以 PDF 擷取出的 {item_text} 作為核對點，只套用引用 section 明載的條件。"
            )
            example = (
                f"為 Figure {number} 建立檢查列，先核對 {first}，再依引用 section 核對 {second}。"
            )
        caveat = (
            f"來源 keyword 索引：{keyword_text}。索引用來定位規範性語句，不取代各欄位所附的完整條件。"
            if keywords
            else "這張 Figure 主要提供結構或說明；本導讀不把圖示關係提升為新的規格要求。"
        )

    if figure.get("mode") == "scope-reduced":
        caveat += (
            " Only the PCIe/memory-based portion is in scope."
            if language == "en"
            else " 本報告只解釋 PCIe／memory-based 部分。"
        )
    if "Eve Diagram" in title:
        caveat += (
            ' The source caption spells "Eve"; the section context identifies a receiver eye. The caption is preserved for traceability.'
            if language == "en"
            else " 原始 Figure caption 使用「Eve」；section 上下文說明的是 receiver eye。此處保留原 caption 以利追溯。"
        )
    return {
        "purpose": purpose,
        "reading": reading,
        "example": example,
        "caveat": caveat,
        "keyword_text": keyword_text,
        "item_text": item_text,
    }


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
        "heading_zh_tw": CORE_TITLES[claim_id][0],
        "heading_en": CORE_TITLES[claim_id][1],
    }
    result["citation_zh_tw"] = cite(result, "zh")
    result["citation_en"] = cite(result, "en")
    return result


def make_figure_claim(report_id: str, report: dict, figure: dict) -> dict:
    figure_id = f"{report['prefix']}-FIG-{int(figure['number']):03d}"
    zh_parts = figure_explanation(figure, "zh")
    en_parts = figure_explanation(figure, "en")
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
            f"{zh_parts['purpose']} {zh_parts['reading']}"
        ),
        "en": (
            f"Figure {figure['number']}, \"{figure['title']}\": "
            f"{en_parts['purpose']} {en_parts['reading']}"
        ),
        "scope_entry_id": report["scope_entry"],
        "source_keywords": list(figure.get("source_keywords", [])),
        "key_items": list(figure.get("key_items", [])),
        "evidence_digest": figure.get("evidence_digest", ""),
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


def section_group(section: str) -> str:
    if section.lower().startswith("annex"):
        return section
    pieces = section.split(".")
    return ".".join(pieces[:2]) if len(pieces) > 1 else pieces[0]


def anchor(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


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
    figure_groups: list[str] = []
    for figure in figures:
        group = section_group(str(figure["section"]))
        if group not in figure_groups:
            figure_groups.append(group)

    parts = [
        "<!doctype html>",
        '<html lang="zh-Hant-TW">',
        "<head>",
        '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        f"<title>{html.escape(report['title_zh'])}｜{label}</title>",
        "</head>",
        "<body>",
        '<nav id="top" aria-label="章節導覽"><a href="#scope">範圍</a> ｜ '
        '<a href="#map">流程圖</a> ｜ <a href="#claims">規格重點</a> ｜ '
        '<a href="#figure-index">Figure 索引</a> ｜ '
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
        f"<p><strong>完整度：</strong>本檔介紹 {len(figures)} 張納入範圍的 Figure。"
        "100 分鐘口頭報告應以規格重點與必講 Figure 為主；其餘 Figure 作為附錄查閱，"
        "但仍完整保留於本檔。</p>",
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
        heading = item["heading_zh_tw"]
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
    parts.extend(
        [
            '</section><section id="figure-index"><h2>Figure 索引</h2>',
            "<p>依 section 跳轉；每張 Figure 可個別展開，減少 iPad 長頁面捲動。</p>",
            "<ul>",
            *[
                f'<li><a href="#section-{anchor(group)}">§{html.escape(group)}</a></li>'
                for group in figure_groups
            ],
            "</ul></section>",
            '<section id="figures"><h2>Figure 逐圖導讀</h2>',
        ]
    )
    figure_claims = {
        int(item["figure"]): item for item in claims if item["figure"] is not None
    }
    active_group = ""
    for figure in figures:
        item = figure_claims[int(figure["number"])]
        details = figure_explanation(figure, "zh")
        group = section_group(str(figure["section"]))
        if group != active_group:
            if active_group:
                parts.append("</section>")
            active_group = group
            parts.append(
                f'<section id="section-{anchor(group)}"><h3>§{html.escape(group)}</h3>'
            )
        figure_anchor = f"figure-{figure['number']}"
        parts.extend(
            [
                f'<details id="{figure_anchor}" data-figure-table-id="{figure["id"]}">',
                f'<summary><strong>Figure {figure["number"]}: '
                f'{html.escape(figure["title"])}</strong></summary>',
                f'<p><span data-claim-id="{item["id"]}">'
                f'{html.escape(item["zh_tw"])}</span></p>',
                "<ul>",
                f"<li><strong>解決的問題：</strong>{html.escape(details['purpose'])}</li>",
                f"<li><strong>閱讀順序：</strong>{html.escape(details['reading'])}</li>",
                f"<li><strong>條件與限制：</strong>{html.escape(details['caveat'])}</li>",
                "<li><strong>說明性範例（informative example）：</strong>"
                f"{html.escape(details['example'])} 此例不新增規格要求。</li>",
            ]
        )
        if not tutorial:
            parts.extend(
                [
                    "<li><strong>來源欄位索引：</strong>"
                    + html.escape(details["item_text"])
                    + "。</li>",
                    "<li><strong>來源 keyword 索引：</strong>"
                    + html.escape(details["keyword_text"])
                    + "；Figure 導讀本身的 normative keyword 為 none。</li>",
                    "<li><strong>追溯鍵：</strong>" + html.escape(item["id"]) + "。</li>",
                ]
            )
        parts.extend(
            [
                "</ul>",
                f"<p><small>{html.escape(item['citation_zh_tw'])}</small></p>",
                '<p><a href="#figure-index">回到 Figure 索引</a> ｜ '
                '<a href="#top">回到頂端</a></p>',
                "</details>",
            ]
        )
    if active_group:
        parts.append("</section>")
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


def frontmatter(
    report_id: str, title: str, description: str, language: str
) -> str:
    lang = "en" if language == "en" else "zh-Hant-TW"
    image = POST_IMAGES[report_id][language]
    return f"""---
layout: post
read_time: true
show_date: true
title: "{title}"
date: 2026-08-28
description: "{description}"
lang: {lang}
img: {image}
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
        frontmatter(report_id, title, description, language),
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
        heading = item["heading_en"] if english else item["heading_zh_tw"]
        out.extend(
            [
                f"### {index}. {heading}",
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
            "## " + ("Figure index" if english else "Figure 索引"),
            "",
            (
                f"This report introduces all {len(figures)} in-scope Figures. Use the "
                "section links below for the 100-minute presentation path; every Figure "
                "remains available as an appendix item."
                if english
                else f"本報告介紹全部 {len(figures)} 張納入範圍的 Figure。100 分鐘簡報"
                "以 section 主線與必講 Figure 為主，其餘 Figure 仍完整保留作為附錄。"
            ),
            "",
        ]
    )
    figure_groups: list[str] = []
    for figure in figures:
        group = section_group(str(figure["section"]))
        if group not in figure_groups:
            figure_groups.append(group)
    for group in figure_groups:
        out.extend([f"- [§{group}](#section-{anchor(group)})", ""])
    out.extend(
        [
            "## " + ("Figure-by-Figure Guide" if english else "Figure 逐圖導讀"),
            "",
            (
                "The source uses Figure numbers for diagrams and field-layout tables. "
                "No source artwork is reproduced; compact field and keyword indexes "
                "come from the locally verified PDFs."
                if english
                else "本範圍的規格以 Figure 編號同時涵蓋示意圖與欄位表；本文不重製原圖。"
                "欄位與 keyword 索引來自本機核對過的 PDF。"
            ),
            "",
        ]
    )
    figure_claims = {
        int(item["figure"]): item for item in claims if item["figure"] is not None
    }
    active_group = ""
    for figure in figures:
        item = figure_claims[int(figure["number"])]
        details = figure_explanation(figure, language)
        statement = item["en"] if english else item["zh_tw"]
        citation = item["citation_en"] if english else item["citation_zh_tw"]
        group = section_group(str(figure["section"]))
        if group != active_group:
            active_group = group
            out.extend(
                [
                    f'<a id="section-{anchor(group)}"></a>',
                    "",
                    f"### §{group}",
                    "",
                ]
            )
        out.extend(
            [
                '<details markdown="1">',
                f"<summary><strong>Figure {figure['number']}: "
                f"{html.escape(figure['title'])}</strong></summary>",
                "",
                f"<!-- claim:{item['id']} figure-table:{figure['id']} -->",
                "",
                statement,
                "",
                "- Purpose: " + details["purpose"]
                if english
                else "- 解決的問題：" + details["purpose"],
                "",
                "- How to read: " + details["reading"]
                if english
                else "- 閱讀順序：" + details["reading"],
                "",
                (
                    "- Conditions and limits: " + details["caveat"]
                    if english
                    else "- 條件與限制：" + details["caveat"]
                ),
                "",
                (
                    "- Informative example: "
                    + details["example"]
                    + " This example adds no requirement."
                    if english
                    else "- 說明性範例（informative example）："
                    + details["example"]
                    + " 此例不新增規格要求。"
                ),
                "",
                (
                    "- Source field index: " + details["item_text"]
                    if english
                    else "- 來源欄位索引：" + details["item_text"]
                ),
                "",
                (
                    "- Source keyword index: " + details["keyword_text"]
                    if english
                    else "- 來源 keyword 索引：" + details["keyword_text"]
                ),
                "",
            ]
        )
        out.extend([f"> {citation}", "", "</details>", ""])
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
    argparse.ArgumentParser(description=__doc__).parse_args()
    contract = json.loads(
        (CONTROL / "output-contract.json").read_text(encoding="utf-8")
    )
    register_doc = json.loads(
        (CONTROL / "figure-table-register.json").read_text(encoding="utf-8")
    )
    register_entries = register_doc["entries"]
    artifacts = {item["id"]: item for item in contract["artifacts"]}
    all_claims = []

    for report_id, report in REPORTS.items():
        figures = sorted(
            [
                item
                for item in register_entries
                if item["report_id"] == report_id
                and item["scope_status"] == "INCLUDE"
            ],
            key=lambda item: int(item["number"]),
        )
        for figure in figures:
            if not figure.get("key_items") or not figure.get("evidence_digest"):
                raise ValueError(
                    f"{figure['id']} lacks tracked compact PDF evidence"
                )
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
        "schema_version": 3,
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
    (CONTROL / "claims.json").write_text(
        json.dumps(claims_doc, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        f"Built 16 artifacts, {len(all_claims)} claims, "
        f"using {len(register_entries)} tracked Figure records"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
