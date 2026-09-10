#!/usr/bin/env python3
"""Build NVMe reports from tracked scope, claims, and compact PDF evidence."""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
from pathlib import Path

# All entry points share one module namespace (including question banks and
# topic installation); direct execution must not create a second copy.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

try:
    from scripts.nvme_nvm_command_set import install as install_nvmcs
    from scripts.nvme_nvmcs_figures import guide_for as nvmcs_figure_guide
except ModuleNotFoundError:
    from nvme_nvm_command_set import install as install_nvmcs
    from nvme_nvmcs_figures import guide_for as nvmcs_figure_guide

try:
    from scripts.nvme_boot_telemetry_sanitize import install as install_bts
    from scripts.nvme_bts_figures import guide_for as bts_figure_guide
    from scripts.nvme_report_questions import render_questions
    from scripts.nvme_bts_terms import definition as report_term_definition
except ModuleNotFoundError:
    from nvme_boot_telemetry_sanitize import install as install_bts
    from nvme_bts_figures import guide_for as bts_figure_guide
    from nvme_report_questions import render_questions
    from nvme_bts_terms import definition as report_term_definition

try:
    from scripts.nvme_teaching_content import (
        REPORT_GLOSSARIES,
        REPORT_MODULES,
        TERM_LIBRARY,
        expanded_figure_guide,
        term_definition,
    )
except ModuleNotFoundError:  # Direct execution puts scripts/ on sys.path.
    from nvme_teaching_content import (
        REPORT_GLOSSARIES,
        REPORT_MODULES,
        TERM_LIBRARY,
        expanded_figure_guide,
        term_definition,
    )


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
    "NVME-NVM-CS-1.3": {
        "revision": "1.3",
        "marker": "NVM Express NVM Command Set Specification, Revision 1.3",
    },
}


def page_shift(value: str, delta: int) -> str:
    return re.sub(r"\d+", lambda match: str(int(match.group()) + delta), value)


def c(
    key,
    section,
    pages,
    zh,
    en,
    keyword="none",
    source="NVME-BASE-2.4",
    scope_entry=None,
):
    pdf_pages = (
        pages
        if source in {"NVME-PCIE-TRANSPORT-1.4", "NVME-NVM-CS-1.3"}
        else page_shift(pages, 26)
    )
    return {
        "key": key,
        "source_id": source,
        "section": section,
        "printed_pages": pages,
        "pdf_pages": pdf_pages,
        "normative_keyword": keyword,
        "zh_tw": zh,
        "en": en,
        "scope_entry_id": scope_entry,
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
            c("KEYWORDS", "1.4.1", "2-3", "規格的 mandatory、may、optional、reserved、shall、should 各有固定語氣；引用時保留英文 keyword，不能把 may 或 should 翻成 shall。", "The specification assigns distinct force to mandatory, may, optional, reserved, shall, and should. A summary must not strengthen may or should into shall."),
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
    "base-admin-fw-logs": {
        "prefix": "BASEFWLOG",
        "title_zh": "NVMe Base 2.4：Firmware Update 與 LID 03h 驗證",
        "title_en": "NVMe Base 2.4: Firmware Update and LID 03h Verification",
        "source_id": "NVME-BASE-2.4",
        "scope_entry": "BASE-FWLOG-INCLUDE",
        "date": "2026-09-01",
        "verified_date": "2026-09-01",
        "range": "§3.11、§3.11.1、§5.2.9、§5.2.10、§5.2.13 的 LID 03h 必要共通欄位、§5.2.13.1.4；主範圍文件頁 135-138、202-206、212-216、225-226，並含最小 dependency slice",
        "range_en": "§3.11, §3.11.1, §5.2.9, §5.2.10, the minimum common §5.2.13 fields needed for LID 03h, and §5.2.13.1.4; main printed pages 135-138, 202-206, 212-216, and 225-226, plus the minimum dependency slice",
        "diagram": ["Image Download", "Firmware Commit", "Activate / Reset", "Get Log Page"],
        "diagram_note_zh": "host 以 OFST／NUMD 傳送 image portions，Firmware Commit 驗證並決定 slot／activation action；需要時完成 reset 與重新初始化，再用 LID 03h 比對目前與下一個 active slot。",
        "diagram_note_en": "The host transfers image portions with OFST and NUMD, Firmware Commit validates them and selects a slot and activation action, and LID 03h then verifies the current and next active slots after any required reset and reinitialization.",
        "claims": [
            c("MODEL-DOMAIN", "5.2.9", "202", "同一 domain 內的 controllers 共用 firmware slots，且相同 firmware image 會套用到該 domain 的所有 controllers；若不支援 multiple domains，範圍就是整個 NVM subsystem。", "Controllers in one domain share firmware slots, and the same firmware image is applied to all controllers in that domain. If multiple domains are not supported, that scope is the entire NVM subsystem."),
            c("FW-RESET", "3.11", "135-136", "需要 reset 的標準流程是：一筆以上 Firmware Image Download、Firmware Commit 驗證並放入 slot、執行能觸發該 activation 的 Controller Level Reset，然後重新初始化 controller 與 I/O queues。", "The reset-based flow is one or more Firmware Image Download commands, Firmware Commit to validate and place the image, a Controller Level Reset capable of causing activation, and reinitialization of the controller and I/O queues."),
            c("FW-IMMEDIATE", "3.11", "136", "CA=011b 要求立即 activation。Firmware Commit 不是 background operation，會保持進行中直到 activation 成功或失敗；若 Firmware Activation notice 已啟用，受影響 controller 可（may）送出 Firmware Activation Starting event。", "CA=011b requests immediate activation. Firmware Commit is not a background operation and remains in progress until activation succeeds or fails. If Firmware Activation notices are enabled, an affected controller may send Firmware Activation Starting.", "may"),
            c("FW-FAILURE", "3.11", "136-137", "若新 image 無法成功載入，controller 必須（shall）回復到最近 activation 的 slot image；若該 image 也無法載入，則載入可用的 baseline read-only image，並產生 Firmware Image Load Error event。", "If the new image cannot be loaded, the controller shall revert to the image in the most recently activated slot; if that image also cannot be loaded, it loads an available baseline read-only image and generates Firmware Image Load Error.", "shall"),
            c("FW-SEQUENCE", "3.11", "137", "host 不宜（should not）讓 firmware／Boot Partition update sequences 重疊，且同一 sequence 宜（should）只使用一個 controller 或 Management Endpoint。", "The host should not overlap firmware or Boot Partition update sequences and should use only one controller or Management Endpoint throughout a sequence.", "should"),
            c("FW-DISCARD", "3.11, 5.2.10", "137, 205-206", "Firmware Commit 完成後的第一筆新 Firmware Image Download，以及 download 後、Firmware Commit 完成前發生的 Controller Level Reset，都必須（shall）使 controller 丟棄尚存的已下載 portions。", "The first Firmware Image Download after Firmware Commit completes, and a Controller Level Reset after download but before Firmware Commit completion, shall cause the controller to discard remaining downloaded portions.", "shall"),
            c("UUID-LIST", "3.11.1", "137-138", "firmware revisions 間的 UUID List 宜（should）保持 entry 位置穩定：新增 UUID 宜接在尾端；移除時宜原位改成 NVMe Invalid UUID；不宜重用 invalid entry，也不宜縮短或移除清單。", "Across firmware revisions, UUID List entry positions should remain stable: new UUIDs should be appended, a removed UUID should be replaced in place with the NVMe Invalid UUID, an invalid entry should not be reused, and the list should not be shortened or removed.", "should"),
            c("UUID-RESET", "3.11.1", "138", "若 downloaded image 在既有 entry 中，以有效 UUID 取代 NVMe Invalid UUID 或另一個有效 UUID，controller 必須（shall）要求 reset；所有受這個 UUID List 變更影響的 controllers 都必須（shall）reset。", "If a downloaded image replaces the NVMe Invalid UUID or a different valid UUID with a valid UUID in an existing entry, the controller shall require reset, and all controllers affected by that UUID List change shall be reset.", "shall"),
            c("CAP-FR", "5.2.14.1", "340", "Identify Controller 的 FR 是目前 active firmware revision 的 8-byte ASCII string，scope 是 controller 所屬 domain；它與 LID 03h 回報的目前 revision 資訊相同。", "Identify Controller FR is the eight-byte ASCII string for the currently active firmware revision in the controller's domain. It is the same revision information available from LID 03h."),
            c("CAP-MDS-ULIST", "5.2.14.1", "346, 364", "CTRATT.MDS 判斷 LID 03h 回傳 domain scope 還是整個 NVM subsystem scope；CTRATT.ULIST 判斷 controller 是否支援 UUID List reporting。MDS=1 時 DID 必須（shall）非零；single-domain subsystem 的 DID 必須（shall）為 0h。", "CTRATT.MDS determines whether LID 03h returns domain-scoped or NVM-subsystem-scoped information, while CTRATT.ULIST indicates UUID List reporting support. With MDS=1, DID shall be nonzero; in a single-domain subsystem, DID shall be 0h.", "shall"),
            c("CAP-FRMW", "5.2.14.1", "354", "FRMW 的 SMUD、FAWR、NOFS 與 FFSRO 分別表示重疊 update 偵測、免 reset activation、domain 支援的 slot 數（1 到 7）以及 slot 1 是否 read-only。", "FRMW.SMUD, FAWR, NOFS, and FFSRO describe overlapping-update detection, activation without reset, the domain's supported slot count (1 through 7), and whether slot 1 is read-only."),
            c("CAP-MTFA", "5.2.14.1", "357", "MTFA 以 100 ms 為單位，表示 activation 時 controller 暫停處理 commands 的最長時間；支援免 reset activation 時此欄位必須（shall）有效，0h 表示最大時間未定義。", "MTFA is in 100 ms units and reports the maximum time command processing is temporarily stopped during activation. It shall be valid when activation without reset is supported; 0h means the maximum is undefined.", "shall"),
            c("CAP-FWUG", "5.2.14.1", "359", "FWUG 以 4 KiB 為單位限制 NUMD 與 OFST 的 granularity／alignment：1h=4 KiB、2h=8 KiB、0h=未提供資訊、FFh=可用任何 dword granularity 與 alignment。違反時 controller 可（may）回 Invalid Field in Command。", "FWUG constrains NUMD and OFST granularity/alignment in 4 KiB units: 1h is 4 KiB, 2h is 8 KiB, 0h reports no information, and FFh permits any dword granularity and alignment. A controller may return Invalid Field in Command for a violation.", "may"),
            c("CAP-MPTFAWR", "5.2.14.1", "364", "MPTFAWR 以 100 ms 為單位，估算 CA=011b 的 Firmware Commit 從處理到完成所需最大時間，且包含把 image commit 到 slot 的時間；不支援免 reset activation 時必須（shall）為 0h。", "MPTFAWR is a 100 ms-unit estimate of the maximum processing time to complete Firmware Commit with CA=011b, including time to commit the image to a slot. It shall be 0h when activation without reset is unsupported.", "shall"),
            c("COMMIT-PURPOSE", "5.2.9", "202-203", "Firmware Commit 驗證最後下載的 image、把它放入 firmware slot，並依 Commit Action 決定只放置、在後續 Controller Level Reset activation，或立即 activation。成功 commit 不等於當下已 active。", "Firmware Commit validates the last downloaded image, places it in a firmware slot, and uses Commit Action to choose placement only, activation at a later Controller Level Reset, or immediate activation. Successful commit does not by itself mean the image is currently active."),
            c("COMMIT-CDW10", "5.2.9", "203", "CDW10[5:3] 是 CA，CDW10[2:0] 是 FS。CA 000b 只放置；001b 放置並排定下次 CLR activation；010b 排定既有 slot；011b 立即 activation。FS=0h 時 controller 必須（shall）在 slot 1 到 7 中選一個。", "CDW10[5:3] is CA and CDW10[2:0] is FS. CA 000b places only, 001b places and schedules activation at the next CLR, 010b schedules an existing slot, and 011b activates immediately. With FS=0h, the controller shall choose a slot from 1 through 7.", "shall"),
            c("COMMIT-BOOT", "5.2.9", "203-205", "BPID 與 CA=110b／111b 屬於 Boot Partition：110b 取代指定 partition，111b 將它標成 active；Boot Partition Write Prohibited 是 Firmware Commit 的 command-specific status 之一。", "BPID and CA=110b/111b belong to Boot Partition handling: 110b replaces the selected partition, 111b marks it active, and Boot Partition Write Prohibited is one of the Firmware Commit command-specific status values."),
            c("COMMIT-MUD", "5.2.9", "204", "Firmware Commit CQE.DW0[1:0] 的 MUD 分別回報 Management Endpoint 與 Admin Submission Queue 偵測到的 overlap。若 FRMW.SMUD=0，MUD 必須（shall）為 00b；MUD 在 command 成功或 aborted 時都有效。", "Firmware Commit CQE.DW0[1:0] MUD reports overlap detected through a Management Endpoint and an Admin Submission Queue. If FRMW.SMUD is 0, MUD shall be 00b; MUD is valid whether the command succeeds or is aborted.", "shall"),
            c("COMMIT-STATUS", "5.2.9", "204-205", "Firmware Commit 的 command-specific status 區分 invalid slot／image、需要 Conventional／NVM Subsystem／Controller Level Reset、MTFA violation、activation prohibited、overlapping range、Boot Partition write prohibited 與 personality incompatibility。", "Firmware Commit command-specific status distinguishes invalid slot/image, required Conventional/NVM Subsystem/Controller Level Reset, MTFA violation, activation prohibited, overlapping range, Boot Partition write prohibition, and personality incompatibility."),
            c("DOWNLOAD-RANGE", "5.2.10", "205-206", "Firmware Image Download 可分成多個 portions，firmware image portions 可不依序送達；host 宜（should）避免 ranges 重疊並符合 FWUG。Boot Partition portions 則必須（shall）依序提交。", "Firmware Image Download may split an image into portions, and firmware-image portions may arrive out of order. The host should avoid overlapping ranges and comply with FWUG. Boot Partition portions shall be submitted in order.", "shall"),
            c("DOWNLOAD-FIELDS", "4.1.1, 5.2.10", "140-142, 205-206", "NVMe over PCIe 的 Admin command 不得使用 SGL，因此 DPTR 以 PRP 指向本次來源 buffer；NUMD 是 0's-based dword count，所以 bytes=(NUMD+1)×4；OFST 是距 image 起點的 dword offset，所以 byte offset=OFST×4。包含 image 起點的 portion 必須（shall）令 OFST=0h。", "An Admin command over NVMe over PCIe shall not use SGL, so DPTR uses PRPs to identify the source buffer. NUMD is a zero-based dword count, so bytes=(NUMD+1)×4; OFST is a dword offset from the image start, so byte offset=OFST×4. The portion containing the image start shall use OFST=0h.", "shall"),
            c("LOG-COMMAND", "4.1.1, 5.2.13", "140-142, 212-215", "讀 LID 03h 時，未使用 namespace，因此 NSID 必須（shall）為 0h；DPTR 以 PRP 指向 512-byte destination buffer。必要的 CDW10-CDW14 slice 為 LID=03h、LSP=0、RAE=0、NUMDL/NUMDU 表示 512 bytes、LSI=0、LPOL/LPOU=0、OT=0、UIDX=0；CSI 對 LID 03h 不使用，controller 依 Figure 208 規則忽略。", "When reading LID 03h, no namespace is used, so NSID shall be 0h, and DPTR uses PRPs to identify the 512-byte destination buffer. The required CDW10-CDW14 slice is LID=03h, LSP=0, RAE=0, NUMDL/NUMDU for 512 bytes, LSI=0, LPOL/LPOU=0, OT=0, and UIDX=0. LID 03h does not use CSI, which the controller ignores under Figure 208's rule.", "shall"),
            c("LOG-LENGTH", "5.2.13", "213-215", "NUMDL 與 NUMDU 合成 0's-based dword count。LID 03h 固定 512 bytes=128 dwords，因此 NUMD=127=0000007Fh，NUMDL=007Fh、NUMDU=0000h；在 LSP=0、RAE=0 下，CDW10=007F0003h。", "NUMDL and NUMDU form a zero-based dword count. LID 03h is 512 bytes, or 128 dwords, so NUMD=127=0000007Fh, NUMDL=007Fh, and NUMDU=0000h. With LSP=0 and RAE=0, CDW10=007F0003h."),
            c("LOG-RAE", "5.2.2, 5.2.13", "186, 213", "RAE=0 會在 command 成功時清除對應 asynchronous event，RAE=1 則保留；若 command 未成功，controller 必須（shall）保留 event。Firmware Activation Starting event 要以 RAE=0 讀取 LID 03h 才會清除。", "RAE=0 clears the corresponding asynchronous event on successful completion, while RAE=1 retains it. If the command fails, the controller shall retain the event. Firmware Activation Starting is cleared by reading LID 03h with RAE=0.", "shall"),
            c("LOG-OFFSET", "5.2.13", "214-215", "本報告以完整 512-byte LID 03h、LPOL=LPOU=0、OT=0 為基準。一般 byte offset 必須 dword aligned；超過 log page 大小的 offset 必須（shall）回 Invalid Field in Command。LID 03h 不需要 index-offset 分支。", "This report uses the complete 512-byte LID 03h with LPOL=LPOU=0 and OT=0. A general byte offset is dword aligned, and an offset beyond the log page shall return Invalid Field in Command. LID 03h needs no index-offset branch.", "shall"),
            c("LOG-SCOPE", "5.2.13", "215-216", "Figure 209 的 LID 03h row 指定 CSI=N、scope=Domain／NVM subsystem、reference=§5.2.13.1.4。MDS=1 時回傳處理 command 之 controller 所屬 domain；否則回傳整個 NVM subsystem 的資訊。", "The LID 03h row in Figure 209 specifies CSI=N, scope=Domain/NVM subsystem, and reference §5.2.13.1.4. With MDS=1, the data is for the domain containing the controller that processed the command; otherwise it is for the NVM subsystem."),
            c("LID03-DESCRIPTION", "5.2.13.1.4", "225-226", "Firmware Slot Information log page 固定 512 bytes，說明每個支援 slot 內的 firmware revision，並指出 current active slot 與（若 controller 有回報）next active slot。revision 以 ASCII string 表示。", "The 512-byte Firmware Slot Information log page reports the firmware revision stored in each supported slot and identifies the current active slot plus the next active slot when reported. Revisions are ASCII strings."),
            c("LID03-AFI", "5.2.13.1.4", "226", "byte 0 的 AFI 中，NAFS=bits 6:4、CAFS=bits 2:0；bits 7 與 3 reserved。NAFS 非零表示將於下一次能觸發 activation 的 CLR 啟用該 slot，NAFS=0 表示 controller 未指出 next slot；CAFS 是目前執行 image 的來源 slot。", "In AFI byte 0, NAFS is bits 6:4 and CAFS is bits 2:0; bits 7 and 3 are reserved. Nonzero NAFS identifies the slot to activate at the next CLR capable of causing activation; NAFS=0 means no next slot is indicated. CAFS identifies the source slot of the running image."),
            c("LID03-FRS", "5.2.13.1.4", "226", "FRS1 到 FRS7 位於 bytes 8-63，每格 8 bytes；slot 沒有有效 revision 或不支援時，該 FRS 必須（shall）清為 0h。bytes 1-7 與 64-511 reserved。", "FRS1 through FRS7 occupy bytes 8-63, eight bytes per slot. If a slot has no valid revision or is unsupported, its FRS shall be cleared to 0h. Bytes 1-7 and 64-511 are reserved.", "shall"),
            c("RESET-XREF", "3.3", "11", "NVMe over PCIe Transport 將 Conventional Reset 與 Function Level Reset 分別列為額外的 transport-specific Controller Level Reset 方法；除 Controller Reset 外，Controller Level Reset 會依 PCI Express Base Specification 重設 PCI register space。", "NVMe over PCIe Transport lists Conventional Reset and Function Level Reset as distinct additional transport-specific Controller Level Reset methods. Except for Controller Reset, Controller Level Reset resets PCI register space as defined by the PCI Express Base Specification.", "none", "NVME-PCIE-TRANSPORT-1.4", "BASE-FWLOG-PCIE-RESET-PREREQUISITE"),
            c("XREF-337", "5.2.9, 5.2.14.1", "202, 340", "來源 §5.2.9 將 Firmware Revision 欄位指向 Figure 337；但 Figure 337 是 Command Set Identifiers，FR 實際列在 Figure 338。未取得另行核准的 errata，因此保留並揭露這個來源內部交叉引用差異，不靜默改寫。", "Source §5.2.9 points Firmware Revision to Figure 337, but Figure 337 contains Command Set Identifiers and FR appears in Figure 338. Without separately approved errata, this report preserves and discloses the internal source discrepancy instead of silently rewriting it."),
        ],
    },
    "base-power-features": {
        "prefix": "BASEPOWER",
        "title_zh": "NVMe Base 2.4：Power／Thermal Features 與 Power Management",
        "title_en": "NVMe Base 2.4: Power/Thermal Features and Power Management",
        "source_id": "NVME-BASE-2.4",
        "scope_entry": "BASE-POWER-INCLUDE",
        "date": "2026-09-02",
        "verified_date": "2026-09-02",
        "range": "§5.2.12、§5.2.30 共通命令、FID 02h／04h／0Ch／10h／11h，以及 §8.1.19～§8.1.19.5；含五張最小 dependency Figure，排除 Power Limit、IIELL、其他 FID 與傳輸專屬內容",
        "range_en": "§5.2.12, the common §5.2.30 command, FIDs 02h/04h/0Ch/10h/11h, and §8.1.19 through §8.1.19.5; includes five minimum dependency Figures and excludes Power Limit, IIELL, other FIDs, and transport-specific material",
        "diagram": ["Get capability / value", "Choose host policy", "Set one Feature", "Observe completion / temperature"],
        "diagram_note_zh": "先用 Get Features 區分支援能力與目前值，再依 Power State Descriptor、溫度能力與工作負載選 policy；Set Features 成功後，以 completion、SMART/Health 與實際 latency／temperature 形成驗證閉環。",
        "diagram_note_en": "First use Get Features to separate capability from current value. Choose policy from Power State Descriptors, thermal capabilities, and workload; after Set Features succeeds, close the loop with completion evidence, SMART/Health, and observed latency/temperature.",
        "claims": [
            c("READ-FIRST", "5.2.12", "209", "Get Features 是讀取 Feature 屬性的 Admin command。工程流程不應從寫入猜測開始，而要先辨認 FID、查 capability，再取得 current／default／saved value。", "Get Features is the Admin command that retrieves Feature attributes. An engineering flow starts by identifying the FID, querying capability, and retrieving current/default/saved values instead of guessing before a write."),
            c("GET-SELECT", "5.2.12", "209-210", "CDW10.SEL 選擇 current=000b、default=001b、saved=010b 或 supported capabilities=011b；CDW10.FID 選 Feature。其餘 SEL encoding reserved。", "CDW10.SEL selects current=000b, default=001b, saved=010b, or supported capabilities=011b; CDW10.FID selects the Feature. Other SEL encodings are reserved.", "reserved"),
            c("GET-SAVED", "5.2.12", "210", "若要求 saved value，但 controller 不支援 saved value 或尚無 saved value，controller 會以 default value 運作。這不是『讀取成功就代表曾經儲存』。", "If a saved value is requested but saved values are unsupported or none exists, the controller operates using the default value. A successful read therefore does not prove that a value was previously saved."),
            c("GET-UIDX", "5.2.12", "210", "CDW14.UIDX 只有在 controller 支援 UUID List 且該 Feature 需要 UUID 關聯時才有意義；未使用時保留為 0。", "CDW14.UIDX is meaningful only when the controller supports the UUID List and the Feature uses a UUID association; otherwise it remains zero."),
            c("GET-CAP", "5.2.12.1", "211-212", "SEL=011b 時，CQE.DW0 以 CHANG、NSSPEC、SVBL 回報是否可變更、是否 namespace-specific、是否可 save。這三個 capability bits 與 Feature value 是兩種不同資料，不能混解。", "With SEL=011b, CQE.DW0 reports CHANG, NSSPEC, and SVBL: changeable, namespace-specific, and saveable. These capability bits are distinct from the Feature value and must not be decoded as one."),
            c("GET-STATUS", "5.2.12.2", "212", "若 Get Features 指定不適用的 Controller Identifier，command-specific status 1Fh 是 Invalid Controller Identifier。Debug 要同時保存 SCT、SC、DNR、CDW10、CDW14 與 target controller。", "If Get Features specifies an inapplicable Controller Identifier, command-specific status 1Fh is Invalid Controller Identifier. Debug evidence retains SCT, SC, DNR, CDW10, CDW14, and the target controller."),
            c("SET-DPTR", "5.2.30", "456-457", "Set Features 的 DPTR 只在所選 Feature 定義 data structure 時使用。以 PRP 指向 buffer 時，該 data buffer 不得跨越超過一個 memory page boundary，因 PRP2 不能在此指向 PRP List。", "Set Features uses DPTR only when the selected Feature defines a data structure. With PRPs, that data buffer shall not cross more than one memory-page boundary because PRP2 cannot point to a PRP List here.", "shall not"),
            c("SET-SAVE", "5.2.30", "457", "CDW10.SV=1 要求把值保存為跨 reset／power cycle 可用的 saved value；若 Feature 不可 save，controller 會回 Feature Identifier Not Saveable。先讀 SVBL，再決定是否設 SV。", "CDW10.SV=1 requests a saved value that can persist across reset/power-cycle boundaries. If the Feature is not saveable, the controller returns Feature Identifier Not Saveable. Read SVBL before setting SV."),
            c("SET-AFTER", "5.2.30", "459", "Set Features 成功後，後續 commands 必須（shall）使用新設定。若軟體需要讓一批 commands 一致套用舊值或新值，host 宜（should）先讓既有 in-flight commands 完成，再切換。", "After Set Features succeeds, subsequent commands shall use the new setting. If software needs a batch of commands to use one consistent setting, the host should allow existing in-flight commands to complete before switching.", "shall"),
            c("FID-SCOPE", "5.2.30", "457-459", "本報告五個 FID 的 scope 都是 Controller。FID 02h、04h、0Ch、11h 不支援 save；FID 10h 支援 save。只有 FID 0Ch 需要 256-byte data structure。", "All five FIDs in this report have Controller scope. FIDs 02h, 04h, 0Ch, and 11h are not saveable; FID 10h is saveable. Only FID 0Ch uses a 256-byte data structure."),
            c("POWER-STATES", "8.1.19", "666-667", "controller 必須（shall）至少支援一個 power state，最多可（may）支援 32 個，編號從 0 連續排列。PS0 的 maximum power 最高；後續 state 的 maximum power 不得高於前一個 state。", "A controller shall support at least one power state and may support up to 32, numbered contiguously from zero. PS0 has the highest maximum power; each subsequent state's maximum power does not exceed the preceding state.", "shall"),
            c("POWER-METRICS", "8.1.19", "666-668", "Power State Descriptor（PSD）把 maximum power、operational/non-operational、entry/exit latency、idle/active power 與 relative performance 放在同一份描述。MP 是 sustained maximum；IDLP 與 ACTP 是不同測量情境，不能拿單次瞬間功耗互相比。", "A Power State Descriptor (PSD) combines maximum power, operational/non-operational type, entry/exit latency, idle/active power, and relative performance. MP is a sustained maximum; IDLP and ACTP use different measurement conditions and are not interchangeable with an instantaneous sample."),
            c("TRANSITION", "8.1.19.1", "668-669", "從舊 state 直接切到新 state 的最大 transition time，是舊 state 的 EXLAT 加上新 state 的 ENLAT。若 controller 內部經過多個 state，則每一段 transition time 相加。", "The maximum direct-transition time from an old state to a new state is the old state's EXLAT plus the new state's ENLAT. If a controller transitions through multiple states, the transition times for every segment are summed."),
            c("RELATIVE", "8.1.19.2", "668", "Relative Read／Write Throughput 與 Latency 都是『值越小越好』，但只可在相同 characteristic 內比較；throughput code 不能與 latency code 混成一個總分。", "Relative Read/Write Throughput and Latency use smaller-is-better encodings, but comparisons are valid only within the same characteristic. A throughput code and a latency code are not combined into one score."),
            c("NONOP", "8.1.19", "667-668", "non-operational power state 不處理 I/O commands，但仍可能處理 property、PMR、CMB、Admin／background 或 transport-specific access。『non-operational』不是 controller 關機。", "A non-operational power state does not process I/O commands, but may still service properties, PMR, CMB, Admin/background work, or transport-specific accesses. Non-operational does not mean the controller is powered off.", "may"),
            c("NONOP-IO", "8.1.19", "668", "host 在手動切入 non-operational state 前宜（should）先 drain I/O。若 I/O command 到達，controller 會自主回到最近使用的 operational state，再處理 I/O。", "The host should drain I/O before manually entering a non-operational state. If an I/O command arrives, the controller autonomously returns to the most recently used operational state before processing I/O.", "should"),
            c("FID02", "5.2.30.1.2", "460-461", "FID 02h 用 CDW11.PS[4:0] 選 power state、WH[7:5] 提供 workload hint。指定的 PS 必須（shall）在 Identify Controller.NPSS 宣告範圍內；不支援的 PS 應（should）以 Invalid Field in Command 中止。", "FID 02h uses CDW11.PS[4:0] to select a power state and WH[7:5] for a workload hint. PS shall be within the range advertised by Identify Controller.NPSS; an unsupported PS should be aborted with Invalid Field in Command.", "shall"),
            c("WORKLOAD", "8.1.19.3", "669", "WH=000b 表示未知 workload；001b 對應先 idle、再做 32 筆 random 1 MiB writes、再 idle 的情境；010b 對應 80,000 筆 sequential 128 KiB writes。011b～111b reserved。", "WH=000b means unknown workload; 001b represents idle, 32 random 1-MiB writes, then idle; 010b represents 80,000 sequential 128-KiB writes. Encodings 011b through 111b are reserved.", "reserved"),
            c("RTD3", "8.1.19.4", "669-670", "RTD3E 與 RTD3R 分別描述進入與恢復時間，供 PCIe D3cold 使用情境評估 idle break-even；NVMe 文字明確說這不是 D3hot 的時間。PCIe D-state 的完整原始行為不在目前提供來源內，不能據此自行補寫。", "RTD3E and RTD3R describe entry and resume time for evaluating idle break-even in a PCIe D3cold use case; the NVMe text explicitly says these are not D3hot times. Complete PCIe D-state semantics are not present in the supplied source and are not invented here."),
            c("FID04", "5.2.30.1.3", "462-463", "FID 04h 可為 Composite Temperature 與最多八個實作的 temperature sensors 設 over／under threshold。溫度以 Kelvin 編碼；到達 over threshold 或低於等於 under threshold 時，SMART/Health 的 Temperature Threshold critical warning 可能觸發 asynchronous event。", "FID 04h sets over/under thresholds for Composite Temperature and up to eight implemented temperature sensors. Temperature is encoded in Kelvin; reaching an over threshold or falling to/below an under threshold may set the SMART/Health Temperature Threshold critical warning and trigger an asynchronous event.", "may"),
            c("HYST", "5.2.30.1.3.1", "463-464", "Figure 470 的 TMPSEL 選 sensor、THSEL 選 over/under、TMPTH 是 threshold、TMPTHH 是 hysteresis。over event 在溫度降到 threshold−hysteresis 時結束；under event在溫度升到 threshold+hysteresis 時結束。", "In Figure 470, TMPSEL selects a sensor, THSEL selects over/under, TMPTH is the threshold, and TMPTHH is hysteresis. An over event ends at threshold minus hysteresis; an under event ends at threshold plus hysteresis."),
            c("FID0C", "5.2.30.1.7", "468-469", "FID 0Ch 的 APSTE=1 啟用 Autonomous Power State Transition（APST）；預設值是 0。啟用只表示 controller 可依 APST table 的 idle timer 自主切換，並不保證一定進入任何特定 state。", "FID 0Ch APSTE=1 enables Autonomous Power State Transition (APST); the default is zero. Enabling it allows controller transitions based on APST-table idle timers; it does not guarantee entry into a particular state."),
            c("APST-ENTRY", "5.2.30.1.7", "469", "APST data structure 固定 256 bytes，共 32 個 8-byte entries。每格 ITPT[31:8] 是毫秒 idle threshold，ITPS[7:3] 是目標 non-operational state；ITPT=0 會停用該 entry。", "The APST data structure is 256 bytes with 32 eight-byte entries. Each entry uses ITPT[31:8] as the idle threshold in milliseconds and ITPS[7:3] as the target non-operational state; ITPT=0 disables that entry."),
            c("APST-NOPPME", "5.2.30.1.7", "469", "APSTE 控制 timer-based entry，NOPPME 控制 controller-initiated background operation 是否可暫時超過 non-operational limit。兩者是兩個正交開關：不要把『可自主進 state』誤解成『可為背景工作提高 power』。", "APSTE controls timer-based entry, while NOPPME controls whether controller-initiated background operations may temporarily exceed a non-operational limit. These are orthogonal switches; autonomous state entry does not imply permission to raise power for background work."),
            c("FID10", "5.2.30.1.10", "471-472", "FID 10h 的 TMT1[31:16] 是較輕度 thermal management threshold，TMT2[15:0] 是較重度 threshold，單位都是 Kelvin；0h 分別停用對應 threshold。", "FID 10h uses TMT1[31:16] as the lighter thermal-management threshold and TMT2[15:0] as the heavier threshold, both in Kelvin; zero independently disables the corresponding threshold."),
            c("HCTM", "5.2.30.1.10, 8.1.19.5", "472, 670-671", "非零 TMT1 必須（shall）小於 TMT2，且兩者必須落在 MNTMT～MXTMT 內；否則回 Invalid Field in Command。達 TMT1 時 controller 採降低影響的動作，達 TMT2 時採更強動作；hysteresis 由 vendor 決定。", "A nonzero TMT1 shall be less than TMT2, and both shall lie between MNTMT and MXTMT; otherwise the command returns Invalid Field in Command. At TMT1 the controller acts to minimize impact, while TMT2 invokes stronger action; hysteresis is vendor-specific.", "shall"),
            c("FID11", "5.2.30.1.11", "472-473", "FID 11h 的 NOPPME=1 允許 controller-initiated background operation 暫時把 power 提高到不超過最後一個 operational state 的上限；NOPPME=0 時，這類工作不得超過目前 non-operational state limits。", "FID 11h NOPPME=1 allows a controller-initiated background operation to raise power temporarily, no higher than the last operational state's limit. With NOPPME=0, such work shall not exceed the current non-operational-state limits.", "shall not"),
            c("OBSERVE", "5.2.13.1.3", "220-225", "設定完成不是驗證終點。SMART/Health 應同時觀察 Composite Temperature、TTC critical warning、warning temperature time、HCTM transition counters 與已實作 sensor readings，再對照 CQE 與 host latency。", "Successful configuration is not the end of verification. Observe SMART/Health Composite Temperature, the TTC critical warning, warning-temperature time, HCTM transition counters, and implemented sensor readings together with CQE and host latency."),
        ],
    },
    "base-self-test-hmb-emulation": {
        "prefix": "BASEDIAGMEM",
        "title_zh": "NVMe Base 2.4：Device Self-test、HMB、Doorbell Emulation 與 Vendor Commands",
        "title_en": "NVMe Base 2.4: Device Self-test, HMB, Doorbell Emulation, and Vendor Commands",
        "source_id": "NVME-BASE-2.4",
        "supporting_source_ids": ["NVME-NVM-CS-1.3"],
        "scope_entry": "BASE-DIAGMEM-INCLUDE",
        "date": "2026-09-02",
        "verified_date": "2026-09-02",
        "range": "Base §5.2.6、§5.2.13.1.7、§5.2.30.2.3、§8.1.8、§8.1.29、§8.2.3、§8.2.4，以及 NVM Command Set 1.3 §4.1.4.3；另含建構命令與能力判斷所需的最小 dependency slice",
        "range_en": "Base §§5.2.6, 5.2.13.1.7, 5.2.30.2.3, 8.1.8, 8.1.29, 8.2.3, and 8.2.4, plus NVM Command Set 1.3 §4.1.4.3; includes the minimum dependency slice needed to construct commands and gate capabilities",
        "diagram": ["Discover capability", "Construct command / memory", "Controller background work", "Read completion / log evidence"],
        "diagram_note_zh": "三條工程主線共享同一個原則：先確認 capability 與 ownership boundary，再提交 command 或 MMIO notification，最後用 CQE、log page 與記憶體生命週期證明結果。",
        "diagram_note_en": "Three engineering tracks share one rule: establish capability and ownership boundaries, submit the command or MMIO notification, then prove the result with CQEs, log pages, and memory-lifecycle evidence.",
        "claims": [
            c("SELFTEST-GATE", "5.2.14.2.1, 8.1.8", "352-358, 614", "啟動 Device Self-test 前，先讀 Identify Controller：OACS.DSTS 判斷 command 是否支援；EDSTT 是 extended operation 在 power state 0 的名目分鐘數；DSTO.SDSO 決定同時只能有一個 subsystem-wide operation，或每個 controller 各一個。這三個欄位回答不同問題。", "Before starting Device Self-test, read Identify Controller. OACS.DSTS gates command support, EDSTT gives the nominal extended-operation time in minutes at power state 0, and DSTO.SDSO selects one subsystem-wide operation versus one operation per controller. These fields answer different questions.", "none", "NVME-BASE-2.4", "BASE-DIAGMEM-DEPENDENCY-INCLUDE"),
            c("SELFTEST-NSID", "5.2.6", "199", "Device Self-test 由收到 command 的 controller 執行。NSID=00000000h 只測 controller；00000001h～FFFFFFFEh 指定一個 namespace；FFFFFFFFh 包含提交當下可由該 controller 存取的所有 attached namespaces。invalid 與 inactive NSID 會得到不同 status。", "Device Self-test is performed by the controller that receives the command. NSID 00000000h tests only the controller, 00000001h through FFFFFFFEh select one namespace, and FFFFFFFFh includes every attached namespace accessible through that controller when the operation starts. Invalid and inactive NSIDs produce different status results."),
            c("SELFTEST-STC", "5.2.6", "199-200", "CDW10.STC[3:0] 選動作：1h=short、2h=extended、3h=Host-Initiated Refresh、Eh=vendor specific、Fh=abort；其餘 encoding reserved。只有 STC=Eh 時 CDW15.DSTP 才是 vendor specific，其他情況 CDW15 reserved。", "CDW10.STC[3:0] selects the action: 1h short, 2h extended, 3h Host-Initiated Refresh, Eh vendor specific, and Fh abort; other encodings are reserved. CDW15.DSTP is vendor specific only when STC is Eh and is reserved otherwise.", "reserved"),
            c("SELFTEST-INPROGRESS", "5.2.6", "200", "已有 operation 時，再送 short、extended 或 Host-Initiated Refresh 必須以 Device Self-test in Progress 中止；vendor-specific 新命令的行為仍是 vendor specific。STC=Fh 則依序中止目前 operation、建立最新 result、清除 current status，最後成功完成 command。", "When an operation is already running, a new short, extended, or Host-Initiated Refresh request is aborted with Device Self-test in Progress; a new vendor-specific request remains vendor specific. STC Fh instead aborts the current operation, creates the newest result, clears current status, and then completes successfully in that order.", "shall"),
            c("SELFTEST-COMPLETION", "5.2.6", "201", "Device Self-test command 的 Admin CQE 只證明『啟動／中止動作已被處理』，不是背景測試已完成。command-specific status 1Dh 表示已有 operation in progress；software 必須把 CQE 與後續 LID 06h 分開記錄。", "The Admin CQE for Device Self-test proves that the start or abort action was processed, not that the background test finished. Command-specific status 1Dh means an operation is already in progress; software records the CQE separately from later LID 06h evidence."),
            c("SELFTEST-BACKGROUND", "8.1.8", "614", "Device Self-test 是由 vendor-specific segments 組成的背景工作。若另一個 command 必須暫停測試才能處理，controller 必須（shall）依序 suspend self-test、處理並完成該 command、再 resume self-test；同時可處理哪些 command 則由 vendor 決定。", "Device Self-test is background work composed of vendor-specific segments. If another command requires suspension, the controller shall suspend the self-test, process and complete that command, and then resume the self-test in order. Which commands may run concurrently remains vendor specific.", "shall"),
            c("SELFTEST-TIMING", "8.1.8.1-8.1.8.2", "615-616", "short operation 應（should）在兩分鐘內完成，且 Controller Level Reset 會中止；extended operation 應在 EDSTT 內完成，必須跨 Controller Level Reset 與 power restoration 持續並於之後 resume。兩者不能共用同一套 reset 預期。", "A short operation should finish within two minutes and is aborted by a Controller Level Reset. An extended operation should finish within EDSTT, shall persist across Controller Level Reset and power restoration, and resumes afterward. The two operations cannot share one reset expectation.", "should"),
            c("SELFTEST-ABORTS", "8.1.8.1-8.1.8.2", "615-616", "short 與 extended 都會被適用的 Format NVM、sanitize start 或 STC=Fh 中止，namespace 從 inventory 移除時則可能（may）中止。Figure 701 顯示 Format 的 NSID 與 secure-erase 選項會改變是否必須中止，不能只看 opcode。", "Both short and extended operations are aborted by an applicable Format NVM command, sanitize start, or STC Fh, and may be aborted when the namespace is removed from inventory. Figure 701 shows that Format NSID and secure-erase selections affect whether abort is required; the opcode alone is insufficient.", "may"),
            c("SELFTEST-LOG-COMMAND", "5.2.13", "213-216", "讀取 LID 06h 所需的最小 Get Log Page slice 是：LID=06h、LSP=0、RAE 依事件策略選擇、NUMD 表示 564 bytes、LPOL/LPOU=0、OT=0、CSI=0、UIDX=0。564 bytes=141 dwords，因此 0's-based NUMD=140=008Ch；RAE=0 時 CDW10=008C0006h。", "The minimum Get Log Page slice for LID 06h uses LID 06h, LSP 0, RAE selected by event policy, NUMD for 564 bytes, LPOL/LPOU 0, OT 0, CSI 0, and UIDX 0. 564 bytes are 141 dwords, so zero-based NUMD is 140 or 008Ch; with RAE 0, CDW10 is 008C0006h.", "none", "NVME-BASE-2.4", "BASE-DIAGMEM-DEPENDENCY-INCLUDE"),
            c("SELFTEST-CURRENT", "5.2.13.1.7", "229-230", "LID 06h 的 byte 0 以 DSTOS 表示目前 operation，byte 1 的 DSTCS[6:0] 是完成百分比；DSTOS=0 時 host 應忽略 DSTCS。controller 在 operation 完成或被中止時，必須先建立 result entry，之後才能把 in-progress status 清為 0。", "In LID 06h, byte 0 DSTOS identifies the current operation and byte 1 DSTCS[6:0] is the completion percentage; the host should ignore DSTCS when DSTOS is zero. When an operation completes or is aborted, the controller creates a result entry before clearing in-progress status to zero."),
            c("SELFTEST-HISTORY", "5.2.13.1.7", "229-230", "LID 06h 保留 20 筆、每筆 28 bytes 的結果，RDS1 永遠是最新完成或中止的 operation。未使用 entry 必須讓 DSTR=Fh 且 DSTC=0h，其他欄位由 host 忽略；不能把全零以外的殘值當成歷史結果。", "LID 06h retains 20 results of 28 bytes each, with RDS1 always the most recently completed or aborted operation. An unused entry uses DSTR Fh and DSTC 0h, while the host ignores its other fields; residual nonzero bytes are not history records.", "shall"),
            c("SELFTEST-RESULT", "5.2.13.1.7", "231", "每筆 DSTS 的高 nibble DSTC 表示原始 self-test code，低 nibble DSTR 表示完成／中止原因。只有 DSTR=7h 時 SEGN 才指出第一個失敗 segment；其他 DSTR 下 SEGN 應忽略。", "In each result DSTS, the high-nibble DSTC records the original self-test code and low-nibble DSTR records the completion or abort reason. SEGN identifies the first failed segment only when DSTR is 7h and is ignored for other DSTR values."),
            c("SELFTEST-VALIDITY", "5.2.13.1.7", "231-232", "VDINFO 的 NSIDVLD、FVLD、SCTVLD、SCVLD 是四個獨立 validity gates。NSID、FLBA、STCT、STC 只有在對應 bit=1 時才可解讀；先驗證 validity，再讀數值，不能用非零值猜測有效。", "VDINFO NSIDVLD, FVLD, SCTVLD, and SCVLD are independent validity gates. NSID, FLBA, STCT, and STC are interpreted only when their corresponding bit is one; validate the bit before the value instead of inferring validity from nonzero data."),
            c("SELFTEST-NVM-FLBA", "4.1.4.3", "76", "Base 將 Figure 219 的 FLBA 留給 I/O Command Set 定義。NVM Command Set 1.3 規定 bytes 23:16 是造成失敗的 logical block address；若有多個失敗 logical blocks，只回其中一個，且僅 FVLD=1 時有效。", "Base leaves Figure 219 FLBA to the applicable I/O Command Set. NVM Command Set 1.3 defines bytes 23:16 as the logical block address that caused the failure; when multiple logical blocks fail, only one is reported, and it is valid only when FVLD is one.", "none", "NVME-NVM-CS-1.3", "NVMCS-DIAGMEM-INCLUDE"),
            c("SELFTEST-DEBUG", "5.2.13.1.7, 8.1.8", "229-232, 614-616", "Debug 時把 command、current state 與歷史 result 分成三個時間點：保存 STC／NSID／CQE；輪詢 DSTOS／DSTCS；完成後保存 DSTS、SEGN、VDINFO、POH、NSID、FLBA、STCT、STC 與 vendor bytes。這樣才能分辨 command rejection、operation abort 與 media failure。", "Debugging separates command, current state, and historical result into three timestamps: retain STC/NSID/CQE, poll DSTOS/DSTCS, and after completion retain DSTS, SEGN, VDINFO, POH, NSID, FLBA, STCT, STC, and vendor bytes. This distinguishes command rejection, operation abort, and media failure."),
            c("HMB-CAPABILITY", "5.2.14.2.1, 8.2.4", "357, 362, 744", "HMPRE=0 表示 HMB 不支援；非零時以 4 KiB units 表示 preferred size，HMMIN 表示 minimum request。HMMINDS 與 HMMAXD 是 descriptor 限制。即使 host 無法提供 HMB，controller 仍必須（shall）正常運作。", "HMPRE zero means HMB is unsupported; a nonzero value is the preferred size in 4-KiB units, while HMMIN gives the minimum request. HMMINDS and HMMAXD constrain descriptors. The controller shall still function correctly when the host cannot provide HMB.", "shall", "NVME-BASE-2.4", "BASE-DIAGMEM-DEPENDENCY-INCLUDE"),
            c("HMB-OWNERSHIP", "5.2.30.2.3, 8.2.4", "515-516, 744", "HMB 是 host 配置、controller 專用的記憶體租約。Set Features enable 成功後，host 必須（shall）停止寫入 descriptor list 與所有描述的 memory ranges，直到 disable command 完成；這是 ownership transfer，不只是 performance hint。", "HMB is host-allocated memory leased exclusively to the controller. After successful Set Features enable, the host shall stop writing both the descriptor list and every described memory range until disable completes. This is an ownership transfer, not merely a performance hint.", "shall"),
            c("HMB-SET-COMMAND", "5.2.30, 5.2.30.2.3", "456-459, 516-518", "Set Features 使用 FID=0Dh；CDW11 放 EHM、MR、HMNARE，CDW12 放 HSIZE，CDW13／14 組成 64-bit HMDL address，CDW15 是 HMDLEC。HMDL address 必須 16-byte aligned；HMDLEC=0 必須回 Invalid Field in Command。", "Set Features uses FID 0Dh. CDW11 holds EHM, MR, and HMNARE; CDW12 holds HSIZE; CDW13/14 form the 64-bit HMDL address; and CDW15 is HMDLEC. The HMDL address is 16-byte aligned, and HMDLEC zero returns Invalid Field in Command.", "shall", "NVME-BASE-2.4", "BASE-DIAGMEM-DEPENDENCY-INCLUDE"),
            c("HMB-DESCRIPTORS", "5.2.30.2.3", "517-518", "HMDL 是連續的 16-byte descriptor array；每個 entry 的 BADD 必須依 CC.MPS memory page size 對齊，BSIZE 以相同 page units 表示連續長度。BSIZE=0 的 entry 由 controller 忽略；HSIZE 應與可用 descriptors 的 page 數相符。", "HMDL is a contiguous array of 16-byte descriptors. Each entry BADD is aligned to the CC.MPS memory-page size, and BSIZE gives a contiguous length in the same page units. The controller ignores an entry whose BSIZE is zero, and HSIZE is reconciled with the usable descriptor-page total."),
            c("HMB-NUMERIC", "5.2.30.2.3", "516-518", "說明性範例：CC.MPS=0 代表 4 KiB page；HSIZE=64 代表 256 KiB。若 HMDL=00000012_34567000h、HMDLEC=2，CDW13=34567000h、CDW14=00000012h、CDW15=00000002h。兩個 descriptor 各 BSIZE=32 pages 時，合計正好 64 pages。", "Informative example: CC.MPS zero means a 4-KiB page, so HSIZE 64 means 256 KiB. For HMDL 00000012_34567000h and HMDLEC 2, CDW13 is 34567000h, CDW14 is 00000012h, and CDW15 is 00000002h. Two descriptors of BSIZE 32 pages each total exactly 64 pages."),
            c("HMB-SEQUENCE", "5.2.30.2.3", "515-516", "HMB 已 enable 時再次送 EHM=1 必須以 Command Sequence Error 中止；尚未 enable 時送 EHM=0 則成功但不做事。disable completion 前 controller 應取回所需資料；CQE 被 posted 後才表示 host 可安全修改或回收 buffer。", "Reissuing EHM one while HMB is already enabled is aborted with Command Sequence Error; issuing EHM zero while disabled succeeds without action. Before disable completion, the controller should retrieve needed data; only the posted CQE means the host may safely modify or reclaim the buffer.", "should"),
            c("HMB-GET", "5.2.12, 5.2.30.2.3", "209-212, 518-519", "Get Features 使用 FID=0Dh；SEL≠supported-capabilities 成功時，CQE.DW0 回 EHM、HMNARE、HMNAR，data buffer 回 4 KiB Attributes data structure，包括 HSIZE、HMDL address 與 HMDLEC。『已啟用』與『目前正在限制 access』是不同狀態。", "Get Features uses FID 0Dh. On successful SEL other than supported capabilities, CQE.DW0 returns EHM, HMNARE, and HMNAR, while the data buffer returns a 4-KiB Attributes structure containing HSIZE, HMDL address, and HMDLEC. Enabled and currently access-restricted are different states.", "none", "NVME-BASE-2.4", "BASE-DIAGMEM-DEPENDENCY-INCLUDE"),
            c("HMB-NONOP", "5.2.30.2.3", "516-519", "HMNARE 只有 Identify.CTRATT.HMBR=1 時可啟用。HMNARE 是 policy，HMNAR 是 controller 此刻是否真的因 non-operational state 而被限制；Admin commands 與其啟動的 background operations 有明文例外。NOPPME 不改變這項 HMB restriction。", "HMNARE may be enabled only when Identify.CTRATT.HMBR is one. HMNARE is policy, while HMNAR reports whether a non-operational state currently restricts the controller; Admin commands and background operations initiated by them are explicit exceptions. NOPPME does not alter this HMB restriction."),
            c("HMB-RESET-RTD3", "8.2.4", "744", "HMB 不會跨 Controller Level Reset 保存在 controller。reset 後 host 應重新提供資源；若 MR=1 表示歸還先前內容，size、descriptor-list address、descriptor-list contents 與 HMB contents 必須完全相同。RTD3 前宜先 disable，恢復後再依是否保留內容選 MR。", "HMB is not persistent in the controller across Controller Level Reset. The host should provide resources again afterward. MR one returns prior contents and requires the exact same size, descriptor-list address, descriptor-list contents, and HMB contents. Disable before RTD3, then select MR according to content preservation on resume."),
            c("HMB-SURPRISE", "8.2.4", "744", "使用 HMB 時發生 surprise removal，controller 必須（shall）確保不造成 data loss 或 data corruption。這不代表 HMB 內容本身具有持久性，而是裝置不得把內部正確性依賴在 host 一定能先走正常 release 流程。", "During surprise removal while HMB is in use, the controller shall ensure no data loss or data corruption. This does not make HMB contents persistent; it means internal correctness cannot depend on the host always completing the normal release flow.", "shall"),
            c("DOORBELL-STRIDE", "3.1.4.1, 8.2.3", "56, 744", "CAP.DSTRD 的實際間距是 2^(2+DSTRD) bytes。DSTRD=0／2／4 分別得到 4／16／64 bytes；software emulation 可用 64-byte stride 把 doorbells 分散到 cacheline，硬體 NVMe interface 的 expected value 是 0h。", "CAP.DSTRD produces a spacing of 2^(2+DSTRD) bytes. DSTRD values 0, 2, and 4 yield 4, 16, and 64 bytes; software emulation can use 64-byte spacing to separate doorbells by cacheline, while the expected hardware-interface value is 0h."),
            c("DOORBELL-DEBUG", "8.2.3", "744", "emulator Debug 不只看 doorbell value，也要保存 CAP.DSTRD、計算後 byte stride、queue identifier、被監看的 cacheline 與 write timestamp。把 encoded DSTRD 直接當 bytes 會讓 queue notification 落到錯誤位址。", "Emulator debugging retains not only the doorbell value but CAP.DSTRD, computed byte stride, queue identifier, monitored cacheline, and write timestamp. Treating encoded DSTRD directly as bytes places queue notifications at the wrong address."),
            c("VENDOR-GATE", "5.2.14.2.1, 8.1.29", "356, 374, 733", "standard Vendor Specific command format 是 optional。AVSCC.VSCF 控制 vendor-specific Admin commands；ICSVSCC.SNVSCF 控制 vendor-specific I/O commands。兩個 capability 必須分開讀，不能因其中一個為 1 就假設另一類命令也使用 Figure 94。", "The standard Vendor Specific command format is optional. AVSCC.VSCF controls vendor-specific Admin commands, while ICSVSCC.SNVSCF controls vendor-specific I/O commands. Read the capabilities independently; one being set does not prove that the other command class uses Figure 94."),
            c("VENDOR-FORMAT", "4.1.1, 8.1.29", "143, 733", "Figure 94 保留 common CDW0、NSID、metadata/data pointers 與 CDW12-CDW15，並把 CDW10／11 定義成 NDT／NDM。若 command 不使用 NSID，必須清為 0；invalid NSID 在使用時必須回 Invalid Namespace or Format，inactive NSID 行為仍是 vendor specific。", "Figure 94 retains common CDW0, NSID, metadata/data pointers, and CDW12-CDW15, while defining CDW10/11 as NDT/NDM. An unused NSID is cleared to zero; an invalid NSID used by the command returns Invalid Namespace or Format, while inactive-NSID behavior remains vendor specific.", "shall"),
            c("VENDOR-LENGTH", "4.1.1, 8.1.29", "143, 733", "NDT 與 NDM 是實際 dword 數，不是 0's-based。NDT=00000100h 代表 256 dwords=1024 bytes；driver 可用 NDT／NDM 驗證 application buffer，避免 data 或 metadata transfer overflow。是否支援 standard format 仍先由 VSCF／SNVSCF gate。", "NDT and NDM are actual dword counts, not zero based. NDT 00000100h means 256 dwords or 1024 bytes; a driver can validate application buffers with NDT/NDM to prevent data or metadata-transfer overflow. VSCF or SNVSCF still gates use of the standard format."),
            c("BOUNDARY-DEBUG", "5.2.6, 5.2.30.2.3, 8.1.29, 8.2.3", "199-201, 515-519, 733, 744", "三條流程的共同 Debug 原則是找第一個 broken boundary：self-test 比對 command→current status→result；HMB 比對 capability→descriptor math→ownership→disable CQE；emulation／vendor command 比對 capability encoding→byte count／stride→實際 memory access。", "All three tracks debug from the first broken boundary: self-test compares command, current status, and result; HMB compares capability, descriptor math, ownership, and disable CQE; emulation/vendor commands compare capability encoding, byte count or stride, and actual memory access."),
        ],
    },
    "base-self-test-namespace-management": {
        "prefix": "BASENSMGMT",
        "title_zh": "NVMe Base 2.4：Device Self-test 與 Namespace Management",
        "title_en": "NVMe Base 2.4: Device Self-test and Namespace Management",
        "source_id": "NVME-BASE-2.4",
        "supporting_source_ids": ["NVME-NVM-CS-1.3"],
        "scope_entry": "BASE-NSMGMT-INCLUDE",
        "date": "2026-09-02",
        "verified_date": "2026-09-02",
        "range": "Base §5.2.6、§5.2.13.1.7（僅 LID 06h）、§5.2.24、§5.2.25、§8.1.8、§8.1.17（排除 §8.1.17.3），以及 NVM Command Set 1.3 §2.1.1、§4.1.4.3、§4.1.6、§5.8；另含理解與實作所需的最小 dependency slice",
        "range_en": "Base §§5.2.6, 5.2.13.1.7 (LID 06h only), 5.2.24, 5.2.25, 8.1.8, and 8.1.17 (excluding §8.1.17.3), plus NVM Command Set 1.3 §§2.1.1, 4.1.4.3, 4.1.6, and 5.8; includes the minimum dependency slice needed for understanding and implementation",
        "diagram": ["Discover capability and capacity", "Run self-test / construct namespace", "Observe LID 06h / receive NSID", "Attach, verify, detach, or delete"],
        "diagram_note_zh": "本報告把診斷與配置分成兩條生命週期：Self-test 用 LID 06h 證明背景 operation 的結果；Namespace Management 先建立未附掛 namespace，再用 Controller List 建立可存取關係，最後以 event、Identify 與 CQE 關閉驗證迴路。",
        "diagram_note_en": "The report separates diagnostic and provisioning lifecycles. LID 06h proves the result of a background self-test, while Namespace Management first creates an unattached namespace, then uses a Controller List to establish access and closes verification through events, Identify data, and CQEs.",
        "claims": [
            c("SELFTEST-GATE", "5.2.14.2.1, 8.1.8", "353-358, 614", "啟動 Device Self-test 前先讀 Identify Controller：OACS.DSTS 判斷 command 是否支援；EDSTT 是 extended operation 在 power state 0 的名目分鐘數；DSTO.SDSO 決定同時只有一個 subsystem-wide operation，或每個 controller 各一個。三者分別是支援、時間與 concurrency scope。", "Before starting Device Self-test, read Identify Controller. OACS.DSTS gates command support, EDSTT gives the nominal extended-operation duration in minutes at power state 0, and DSTO.SDSO selects one subsystem-wide operation versus one operation per controller. They describe support, time, and concurrency scope respectively.", "none", "NVME-BASE-2.4", "BASE-NSMGMT-DEPENDENCY-INCLUDE"),
            c("SELFTEST-NSID", "5.2.6", "199", "Device Self-test 由收到 command 的 controller 執行。NSID=00000000h 只測 controller；00000001h～FFFFFFFEh 指定一個 active namespace；FFFFFFFFh 包含提交當下該 controller 可存取的所有 attached namespaces。invalid 與 inactive NSID 是不同錯誤。", "Device Self-test is performed by the controller receiving the command. NSID 00000000h tests only that controller; 00000001h through FFFFFFFEh select one active namespace; and FFFFFFFFh includes all attached namespaces accessible through that controller when the operation starts. Invalid and inactive NSIDs are distinct errors."),
            c("SELFTEST-STC", "5.2.6", "199-200", "CDW10.STC[3:0] 選動作：1h=short、2h=extended、3h=Host-Initiated Refresh、Eh=vendor specific、Fh=abort；其餘 encoding reserved。只有 STC=Eh 時 CDW15.DSTP 才是 vendor specific，其他 STC 下 CDW15 reserved。", "CDW10.STC[3:0] selects 1h short, 2h extended, 3h Host-Initiated Refresh, Eh vendor specific, or Fh abort; the other encodings are reserved. CDW15.DSTP is vendor specific only when STC is Eh and is reserved for other STC values.", "reserved"),
            c("SELFTEST-INPROGRESS", "5.2.6", "200", "已有 operation 時，再送 short、extended 或 Host-Initiated Refresh 必須以 Device Self-test in Progress 中止；STC=Fh 則依序中止目前 operation、建立最新 result、清除 current status，再成功完成 abort command。", "While an operation is active, a new short, extended, or Host-Initiated Refresh request shall be aborted with Device Self-test in Progress. STC Fh instead aborts the current operation, creates the newest result, clears current status, and successfully completes the abort command in that order.", "shall"),
            c("SELFTEST-COMPLETION", "5.2.6", "201", "Device Self-test 的 Admin CQE 只證明啟動或中止動作已被處理，不代表背景測試完成。software 必須把 command CQE、LID 06h current state 與最後 result entry 當成三個不同時間點。", "The Device Self-test Admin CQE proves only that the start or abort action was processed; it does not mean that the background test has finished. Software treats the command CQE, current LID 06h state, and final result entry as three distinct timestamps."),
            c("SELFTEST-BACKGROUND", "8.1.8", "614", "Device Self-test 是由 vendor-specific segments 組成的背景工作。若處理另一個 command 必須暫停測試，controller 必須（shall）依序 suspend self-test、處理並完成該 command、再 resume self-test；可同時處理哪些 command 仍由 vendor 決定。", "Device Self-test is background work composed of vendor-specific segments. If processing another command requires suspension, the controller shall suspend the self-test, process and complete that command, and resume the self-test in order. Which commands may run concurrently remains vendor specific.", "shall"),
            c("SELFTEST-TIMING", "8.1.8.1-8.1.8.2", "615-616", "short operation 應（should）在兩分鐘內完成，Controller Level Reset 會中止；extended operation 應在 EDSTT 內完成，必須跨 Controller Level Reset 與 power restoration 持續並於之後 resume。兩種測試不能共用同一套 reset 預期。", "A short operation should finish within two minutes and is aborted by Controller Level Reset. An extended operation should finish within EDSTT, shall persist across Controller Level Reset and power restoration, and resumes afterward. The two test types do not share one reset expectation.", "should"),
            c("SELFTEST-ABORTS", "8.1.8.1-8.1.8.2", "615-616", "short 與 extended 都會被適用的 Format NVM、sanitize start 或 STC=Fh 中止，namespace 從 inventory 移除時則可能（may）中止。Figure 701 顯示必須同時看 Format NSID、secure-erase 選項與 Self-test NSID。", "Both short and extended operations are aborted by an applicable Format NVM command, sanitize start, or STC Fh, and may be aborted when the namespace is removed from inventory. Figure 701 requires the Format NSID, secure-erase selection, and Self-test NSID to be evaluated together.", "may"),
            c("SELFTEST-LOG-COMMAND", "5.2.13", "213-216", "完整讀取 LID 06h 使用 564 bytes=141 dwords，因此 0's-based NUMD=140=008Ch；LID=06h、LSP=0、LPOL/LPOU=0、OT=0、CSI=0、UIDX=0。RAE=0 時 CDW10=008C0006h。", "A complete LID 06h read transfers 564 bytes or 141 dwords, so zero-based NUMD is 140 or 008Ch. Use LID 06h, LSP zero, LPOL/LPOU zero, OT zero, CSI zero, and UIDX zero. With RAE zero, CDW10 is 008C0006h.", "none", "NVME-BASE-2.4", "BASE-NSMGMT-DEPENDENCY-INCLUDE"),
            c("SELFTEST-CURRENT", "5.2.13.1.7", "229-230", "LID 06h byte 0 的 DSTOS 表示目前 operation，byte 1 的 DSTCS[6:0] 是完成百分比；DSTOS=0 時 host 應忽略 DSTCS。operation 完成或中止時，controller 必須先建立 result entry，再把 in-progress status 清為 0。", "In LID 06h, byte 0 DSTOS identifies the current operation and byte 1 DSTCS[6:0] gives completion percentage; the host should ignore DSTCS when DSTOS is zero. When an operation completes or is aborted, the controller creates a result entry before clearing in-progress status to zero.", "shall"),
            c("SELFTEST-HISTORY", "5.2.13.1.7", "229-232", "LID 06h 保留 20 筆、每筆 28 bytes 的結果，RDS1 是最新一筆。DSTS 高 nibble DSTC 記原始 self-test code，低 nibble DSTR 記完成或中止原因；只有 DSTR=7h 時 SEGN 才可解讀。", "LID 06h retains twenty 28-byte results with RDS1 newest. The high DSTS nibble DSTC records the original self-test code and the low nibble DSTR records completion or abort reason. SEGN is interpreted only when DSTR is 7h."),
            c("SELFTEST-VALIDITY", "5.2.13.1.7", "231-232", "VDINFO 的 NSIDVLD、FVLD、SCTVLD、SCVLD 是四個獨立 validity gates。NSID、FLBA、STCT、STC 只有在對應 bit=1 時才可讀；parser 不得以欄位非零猜測有效。", "VDINFO NSIDVLD, FVLD, SCTVLD, and SCVLD are four independent validity gates. NSID, FLBA, STCT, and STC are interpreted only when the corresponding bit is one; a parser does not infer validity from a nonzero field."),
            c("SELFTEST-NVM-FLBA", "4.1.4.3", "76", "NVM Command Set 1.3 將 result bytes 23:16 定義為造成失敗的 logical block address。若多個 logical blocks 失敗，只回其中一個，而且僅在 FVLD=1 時有效。", "NVM Command Set 1.3 defines result bytes 23:16 as the logical block address that caused the failure. If multiple logical blocks fail, only one is reported, and it is valid only when FVLD is one.", "none", "NVME-NVM-CS-1.3", "NVMCS-NSMGMT-INCLUDE"),
            c("CAPACITY-MODEL", "2.1.1", "13-14", "Namespace Size（NSZE）是 LBA 0 到 n−1 的總 logical blocks；Namespace Capacity（NCAP）是任一時點最多可配置的 blocks；Namespace Utilization（NUSE）是目前已配置 blocks。永遠遵守 NSZE ≥ NCAP ≥ NUSE。", "Namespace Size (NSZE) is the total logical-block range from LBA zero through n minus one; Namespace Capacity (NCAP) is the maximum allocatable blocks at any time; and Namespace Utilization (NUSE) is the number currently allocated. NSZE is always at least NCAP, which is at least NUSE.", "none", "NVME-NVM-CS-1.3", "NVMCS-NSMGMT-INCLUDE"),
            c("THIN-PROVISIONING", "2.1.1", "13", "NSFEAT.THINP=1 時，controller 可（may）回報 NCAP<NSZE，並必須（shall）追蹤 NUSE。THINP=0 時，controller 必須回報 NCAP=NSZE，且可讓 NUSE 永遠等於 NCAP。", "With NSFEAT.THINP one, a controller may report NCAP below NSZE and shall track NUSE. With THINP zero, the controller shall report NCAP equal to NSZE and may report NUSE as always equal to NCAP.", "shall", "NVME-NVM-CS-1.3", "NVMCS-NSMGMT-INCLUDE"),
            c("NSMGMT-CAPABILITY", "8.1.17", "660", "完整 Namespace Management capability 由 Namespace Management command 與 Namespace Attachment command 組成。支援時 controller 必須支援兩者、設 OACS.NMS=1、支援 Attached Namespace Attribute Changed event；Allocated event 為 should，Namespace Granularity 與 Restore Default 為 may。", "The complete Namespace Management capability consists of Namespace Management and Namespace Attachment. A supporting controller shall implement both, set OACS.NMS to one, and support the Attached Namespace Attribute Changed event; the Allocated event is a should, while Namespace Granularity and Restore Default are may capabilities.", "shall"),
            c("NSID-LIFECYCLE", "8.1.17", "660", "create 成功後 namespace 已 allocated 但尚未 attached，因此對 controller 尚非 active。detach 使該 controller 上的 NSID 變 inactive；delete 使 subsystem 中的 NSID 變 unallocated。受影響的 outstanding 或後續 commands 依 inactive NSID 處理。", "After create succeeds, the namespace is allocated but not attached and therefore is not active on a controller. Detach makes its NSID inactive on that controller; delete makes the NSID unallocated in the subsystem. Affected outstanding and later commands are handled as though issued to an inactive NSID."),
            c("CREATE-PREFLIGHT", "8.1.17.1", "661-662", "create 前先以 NSID=FFFFFFFFh、CNS=00h 讀 common namespace capabilities；若支援，再用 CNS=16h 讀 Namespace Granularity，並確認可用 capacity。這三步完成後才建立 4096-byte create buffer。", "Before create, read common namespace capabilities with NSID FFFFFFFFh and CNS 00h; if supported, read Namespace Granularity with CNS 16h and determine available capacity. Only then construct the 4096-byte create buffer."),
            c("CREATE-BASE-COMMAND", "5.2.25", "446-448", "Create 使用 NSID=0、SEL=0h 與 CSI=00h（NVM Command Set）。DPTR 指向 4096-byte data structure：bytes 0:511 是 I/O Command Set specific、512:1023 reserved、1024:4095 vendor specific。reserved bytes 由 host 清為 0。", "Create uses NSID zero, SEL 0h, and CSI 00h for the NVM Command Set. DPTR identifies a 4096-byte structure: bytes 0:511 are I/O-Command-Set-specific, 512:1023 are reserved, and 1024:4095 are vendor specific. The host clears reserved bytes to zero.", "reserved"),
            c("CREATE-NVM-PAYLOAD", "4.1.6.4", "111-113", "NVM create payload 的主要 host-specified fields 是 NSZE、NCAP、FLBAS、DPS、NMIC、ANAGRPID、NVMSETID、ENDGID、LBSTM、NPHNDLS 與 Placement Handle List。成功 create 後，namespace 依這些屬性格式化；未使用的 reserved fields 應清為 0。", "The primary host-specified NVM create fields are NSZE, NCAP, FLBAS, DPS, NMIC, ANAGRPID, NVMSETID, ENDGID, LBSTM, NPHNDLS, and the Placement Handle List. After successful create, the namespace is formatted with these attributes, and unused reserved fields should be zero.", "should", "NVME-NVM-CS-1.3", "NVMCS-NSMGMT-INCLUDE"),
            c("PROTECTION-VALIDATION", "4.1.6.2", "110", "End-to-end Data Protection 設定在 create 時套用。LBAFEE 未啟用時，特定 16-bit STS 非零、32-bit 或 64-bit Guard Protection Information 組合必須以 Invalid Namespace or Format 中止；LBSTM 不符合 Figure 127 capability 時則回 Invalid Field in Command。", "End-to-end Data Protection settings are applied during create. Without LBAFEE, specified combinations using nonzero STS with 16-bit, or 32-bit or 64-bit Guard Protection Information, are aborted with Invalid Namespace or Format. An LBSTM that violates Figure 127 capability returns Invalid Field in Command.", "shall", "NVME-NVM-CS-1.3", "NVMCS-NSMGMT-INCLUDE"),
            c("FDP-VALIDATION", "4.1.6.3", "110-111", "只有指定 Endurance Group 已啟用 Flexible Data Placement（FDP）且 SEL=Create 時，NPHNDLS 與 Placement Handle List 才參與驗證。NPHNDLS 不得大於支援的 Reclaim Unit Handles 或 128；重複、越界、格式不相容或無可用 handle 會導向 Invalid Placement Handle List 或 Invalid Format。", "NPHNDLS and the Placement Handle List participate in validation only when Flexible Data Placement (FDP) is enabled in the selected Endurance Group and SEL is Create. NPHNDLS may not exceed the supported Reclaim Unit Handles or 128; duplicates, out-of-range handles, incompatible formats, or no available handle lead to Invalid Placement Handle List or Invalid Format.", "shall", "NVME-NVM-CS-1.3", "NVMCS-NSMGMT-INCLUDE"),
            c("GROUP-SELECTION", "8.1.17", "661", "NVMSETID／ENDGID 的決策矩陣為：兩者 0 由 controller 選兩者；NVMSETID=0、ENDGID≠0 時由指定 Endurance Group 內選 NVM Set；NVMSETID≠0、ENDGID=0 必須 Invalid Field；兩者非 0 時只有該 NVM Set 確實屬於指定 Endurance Group 才可配置。", "The NVMSETID/ENDGID matrix is: both zero lets the controller choose both; NVMSETID zero with nonzero ENDGID selects an NVM Set inside the specified Endurance Group; nonzero NVMSETID with zero ENDGID is Invalid Field; and both nonzero are valid only when that NVM Set belongs to the specified Endurance Group.", "shall"),
            c("ALLOCATION-ROUNDING", "8.1.17", "661", "controller 可（may）按內部 allocation unit 把實際消耗容量向上取整。Spec 範例中，32 blocks×4 KiB=128 KiB 的 namespace，在 1 MiB allocation unit 下可消耗 1 MiB；因此 capacity consumption 不一定等於 logical block size×block count。", "A controller may round actual capacity consumption up to an internal allocation unit. In the specification example, 32 blocks times 4 KiB equals a 128-KiB namespace but may consume 1 MiB with a 1-MiB allocation unit; capacity consumption therefore need not equal logical-block size times block count.", "may"),
            c("GRANULARITY-HINTS", "5.8", "165", "Namespace Granularity 的 NSG 與 NCG 都是 byte-unit hints。若 NSZE×LBA size 可整除 NSG、NCAP×LBA size 可整除 NCG 且 NSZE=NCAP，配置為 fully provisioned 且全部容量可由 LBA 定址；不符合 hint 可能浪費容量，但 otherwise-valid create 不得只因違反 hint 被中止。", "Namespace Granularity NSG and NCG are byte-unit hints. If NSZE times LBA size is divisible by NSG, NCAP times LBA size is divisible by NCG, and NSZE equals NCAP, the namespace is fully provisioned and all allocated capacity is LBA-addressable. Violating a hint may waste capacity, but an otherwise valid create shall not be aborted solely for that reason.", "shall not", "NVME-NVM-CS-1.3", "NVMCS-NSMGMT-INCLUDE"),
            c("ATTACH-COMMAND", "5.2.24", "444-445", "Namespace Attachment 的 DPTR 指向 4096-byte Controller List；SEL=0h attach、SEL=1h detach。以 PRP 指向此 buffer 時不得使用 PRP List，因 buffer 不可跨越超過一個 memory-page boundary。attach／detach 狀態跨所有 reset events 保留。", "Namespace Attachment DPTR points to a 4096-byte Controller List; SEL 0h attaches and SEL 1h detaches. With PRPs, the buffer cannot use a PRP List because it may not cross more than one memory-page boundary. Attach/detach state persists across all reset events.", "shall not"),
            c("ATTACH-LIMITS", "5.2.24", "444-445", "attach 前分別核對 Domain aggregate MAXDNA 與每個 I/O controller 的 MAXCNA；非零 limit 被超過時回 Namespace Attachment Limit Exceeded。還要核對 I/O Command Set support／enable state，不能把所有 attach failure 都歸成同一種 status。", "Before attach, check Domain-aggregate MAXDNA and per-I/O-controller MAXCNA separately. Exceeding a nonzero limit returns Namespace Attachment Limit Exceeded. I/O Command Set support and enablement are additional independent gates, so attach failures do not collapse to one status."),
            c("CREATE-COMPLETION", "5.2.25, 8.1.17.1", "446-448, 662", "Create 成功時 controller 選擇可用 NSID，CQE.DW0 回傳該 NSID；此刻 namespace 尚未 attached。software 必須先保存 returned NSID，再以 Namespace Attachment 建立 controller access，不能在 create CQE 後直接送 I/O。", "On successful create, the controller selects an available NSID and returns it in CQE DW0; the namespace is still unattached. Software preserves the returned NSID and then establishes controller access through Namespace Attachment instead of issuing I/O immediately after the create CQE."),
            c("DELETE", "5.2.25, 8.1.17.1", "446, 448, 662", "Delete 的 NSID 指定已建立 namespace；FFFFFFFFh 表示 delete all，即使目前零個 namespaces 也成功。delete 會使 namespace 從 subsystem 消失並具有 detach side effect；host 應先 detach 所有 controllers，讓 event 與 outstanding-I/O 行為更可控。", "Delete NSID selects a created namespace, while FFFFFFFFh means delete all and succeeds even when no namespace exists. Delete removes the namespace and has a detach side effect; the host should detach it from every controller first so events and outstanding-I/O behavior remain controlled.", "should"),
            c("RESTORE-DEFAULT", "5.2.25.1", "447-448", "Restore Default 使用 SEL=2h，NSID 應為 0 且 controller 會忽略它。先讀 RDNCS，刪除 subsystem 中所有 namespaces，再送 restore；若仍有 namespace，回 Command Sequence Error。成功前 controller 必須套用 current active firmware image 的 default configuration 並設 DNCS=1。", "Restore Default uses SEL 2h; NSID should be zero and is ignored by the controller. Check RDNCS, delete every namespace in the subsystem, and then issue restore; any remaining namespace causes Command Sequence Error. Before success, the controller applies the current active firmware image's default configuration and sets DNCS to one.", "shall"),
            c("COMMAND-STATUS", "5.2.24-5.2.25", "445, 448", "Debug 要保留 command-specific status：Attachment 可回 already attached 18h、private 19h、not attached 1Ah、Controller List invalid 1Ch、ANA attach failed 25h、limit 27h、I/O Command Set 29h／2Ah；Management 可回 Invalid Format 0Ah、insufficient capacity 15h、NSID unavailable 16h、thin provisioning unsupported 1Bh、ANA group invalid 24h。", "Debug evidence retains command-specific status. Attachment may return already attached 18h, private 19h, not attached 1Ah, Controller List invalid 1Ch, ANA attach failed 25h, limit 27h, or I/O Command Set 29h/2Ah. Management may return Invalid Format 0Ah, insufficient capacity 15h, NSID unavailable 16h, thin provisioning unsupported 1Bh, or ANA group invalid 24h."),
            c("NAMESPACE-EVENTS", "8.1.17.1-8.1.17.2", "662-663", "create 改變 Allocated Namespace ID list；attach／detach 改變 Active Namespace ID list；delete 可能同時改變兩者。啟用對應 notice 時，host 收到 asynchronous event 後應重新 Identify，而不是只用 event code 猜新 inventory。§8.1.17.2 對處理 delete 的 controller 與其他 controllers 規定不同 event reporting。", "Create changes the Allocated Namespace ID list, attach/detach changes the Active Namespace ID list, and delete may change both. When the corresponding notice is enabled, the host reissues Identify after the asynchronous event rather than inferring inventory from the event code alone. Section 8.1.17.2 distinguishes the controller processing delete from the other controllers."),
            c("GRANULARITY-EXAMPLE", "5.8", "165", "說明性範例：LBA=4 KiB、NSG=1 MiB（256 LBAs）、NCG=2 MiB（512 LBAs）。NSZE=NCAP=1024 同時滿足兩種 granularity；NSZE=1000、NCAP=1000 不滿足 NSG／NCG 整除，但若其他欄位都合法，controller 不得只因這個 hint violation 中止 create。", "Informative example: with 4-KiB LBAs, NSG 1 MiB equals 256 LBAs and NCG 2 MiB equals 512 LBAs. NSZE and NCAP of 1024 satisfy both granularities. Values of 1000 violate NSG/NCG divisibility, but an otherwise valid create is not aborted solely for that hint violation.", "shall not", "NVME-NVM-CS-1.3", "NVMCS-NSMGMT-INCLUDE"),
            c("END-TO-END-DEBUG", "5.2.24-5.2.25, 8.1.17.1", "444-448, 661-663", "完整 trace 至少保存：OACS.NMS／limits、common Identify 與 granularity snapshot、4096-byte create buffer、raw SQE、CQE.DW0 NSID、Controller List、attach CQE、AER、重新 Identify 結果，以及 detach／delete 後的 inactive／unallocated 狀態。第一個不一致的 boundary 才是 Debug 起點。", "A complete trace retains OACS.NMS and limits, common Identify and granularity snapshots, the 4096-byte create buffer, raw SQE, CQE DW0 NSID, Controller List, attach CQE, AER, refreshed Identify result, and inactive/unallocated state after detach/delete. The first inconsistent boundary is the debugging start point."),
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
    "nvm-command-set-1.3": {"zh": "posts/2026/dogMC_title.jpg", "en": "posts/2026/cat_title.jpg"},
    "base-boot-telemetry-sanitize": {
        "zh": "posts/2026/dogMC_title.jpg",
        "en": "posts/2026/cat_title.jpg",
    },
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
    "base-admin-fw-logs": {
        "zh": "posts/2026/dogMC_title.jpg",
        "en": "posts/2026/cat_title.jpg",
    },
    "base-power-features": {
        "zh": "posts/2026/dogMC_title.jpg",
        "en": "posts/2026/cat_title.jpg",
    },
    "base-self-test-hmb-emulation": {
        "zh": "posts/2026/dogMC_title.jpg",
        "en": "posts/2026/cat_title.jpg",
    },
    "base-self-test-namespace-management": {
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
    "BASEFWLOG-MODEL-DOMAIN": ("先找出 firmware 的共享邊界", "Start with the firmware-sharing boundary"),
    "BASEFWLOG-FW-RESET": ("需要 reset 的完整流程", "Complete reset-based flow"),
    "BASEFWLOG-FW-IMMEDIATE": ("立即 activation 不是背景工作", "Immediate activation is not background work"),
    "BASEFWLOG-FW-FAILURE": ("載入失敗與 fallback", "Load failure and fallback"),
            "BASEFWLOG-FW-SEQUENCE": ("update sequence 應以串行方式規劃", "Plan update sequences as serialized work"),
    "BASEFWLOG-FW-DISCARD": ("downloaded portions 何時失效", "When downloaded portions are discarded"),
    "BASEFWLOG-UUID-LIST": ("UUID List 的位置穩定性", "UUID List positional stability"),
    "BASEFWLOG-UUID-RESET": ("UUID 變更造成的 reset 邊界", "Reset boundary caused by UUID changes"),
    "BASEFWLOG-CAP-FR": ("FR：目前 active revision", "FR: currently active revision"),
    "BASEFWLOG-CAP-MDS-ULIST": ("MDS、DID 與 ULIST", "MDS, DID, and ULIST"),
    "BASEFWLOG-CAP-FRMW": ("FRMW：slot 與 activation 能力", "FRMW: slot and activation capabilities"),
    "BASEFWLOG-CAP-MTFA": ("MTFA：暫停 command processing 的時間", "MTFA: command-processing pause"),
    "BASEFWLOG-CAP-FWUG": ("FWUG：download granularity 與 alignment", "FWUG: download granularity and alignment"),
    "BASEFWLOG-CAP-MPTFAWR": ("MPTFAWR：立即 activation 的完成時間", "MPTFAWR: immediate-activation completion time"),
    "BASEFWLOG-COMMIT-PURPOSE": ("Firmware Commit 的真正作用", "What Firmware Commit actually does"),
    "BASEFWLOG-COMMIT-CDW10": ("CA 與 FS 的決策矩陣", "CA and FS decision matrix"),
    "BASEFWLOG-COMMIT-BOOT": ("Boot Partition cross-reference 邊界", "Boot Partition cross-reference boundary"),
    "BASEFWLOG-COMMIT-MUD": ("MUD：重疊 sequence 的證據", "MUD: evidence of overlapping sequences"),
    "BASEFWLOG-COMMIT-STATUS": ("status 決定下一個 recovery 動作", "Status selects the next recovery action"),
    "BASEFWLOG-DOWNLOAD-RANGE": ("portion 順序、overlap 與 FWUG", "Portion ordering, overlap, and FWUG"),
    "BASEFWLOG-DOWNLOAD-FIELDS": ("DPTR、NUMD、OFST 與實際 bytes", "DPTR, NUMD, OFST, and actual bytes"),
    "BASEFWLOG-LOG-COMMAND": ("LID 03h 的最小 command slice", "Minimum command slice for LID 03h"),
    "BASEFWLOG-LOG-LENGTH": ("512 bytes 的實際 command 計算", "Concrete command calculation for 512 bytes"),
    "BASEFWLOG-LOG-RAE": ("RAE 的事件副作用", "RAE event side effect"),
    "BASEFWLOG-LOG-OFFSET": ("完整讀取與 offset 邊界", "Full-read and offset boundary"),
    "BASEFWLOG-LOG-SCOPE": ("LID 03h 的 domain／subsystem scope", "Domain/subsystem scope of LID 03h"),
    "BASEFWLOG-LID03-DESCRIPTION": ("LID 03h 回答的問題", "What LID 03h answers"),
    "BASEFWLOG-LID03-AFI": ("AFI：current 與 next active slot", "AFI: current and next active slots"),
    "BASEFWLOG-LID03-FRS": ("FRS1-FRS7 與 reserved 區", "FRS1-FRS7 and reserved regions"),
    "BASEFWLOG-RESET-XREF": ("PCIe reset 名稱不能混用", "Do not conflate PCIe reset names"),
    "BASEFWLOG-XREF-337": ("Figure 337／338 交叉引用差異", "Figure 337/338 cross-reference discrepancy"),
    "BASEPOWER-READ-FIRST": ("先讀後寫：Feature 能力盤點", "Read before write: Feature capability inventory"),
    "BASEPOWER-GET-SELECT": ("SEL 與 FID", "SEL and FID"),
    "BASEPOWER-GET-SAVED": ("saved value fallback", "Saved-value fallback"),
    "BASEPOWER-GET-UIDX": ("UIDX 使用條件", "UIDX applicability"),
    "BASEPOWER-GET-CAP": ("CHANG／NSSPEC／SVBL", "CHANG/NSSPEC/SVBL"),
    "BASEPOWER-GET-STATUS": ("Get Features failure evidence", "Get Features failure evidence"),
    "BASEPOWER-SET-DPTR": ("Set Features data buffer", "Set Features data buffer"),
    "BASEPOWER-SET-SAVE": ("SV 與 saveability", "SV and saveability"),
    "BASEPOWER-SET-AFTER": ("成功後的切換邊界", "Post-success transition boundary"),
    "BASEPOWER-FID-SCOPE": ("五個 FID 的 scope／persistence", "Scope and persistence of the five FIDs"),
    "BASEPOWER-POWER-STATES": ("power state 編號與上限", "Power-state numbering and limits"),
    "BASEPOWER-POWER-METRICS": ("Power State Descriptor mental model", "Power State Descriptor mental model"),
    "BASEPOWER-TRANSITION": ("entry／exit latency 計算", "Entry/exit latency calculation"),
    "BASEPOWER-RELATIVE": ("relative performance 解讀", "Relative-performance interpretation"),
    "BASEPOWER-NONOP": ("non-operational 不等於關機", "Non-operational is not powered off"),
    "BASEPOWER-NONOP-IO": ("I/O 觸發 operational return", "I/O-triggered operational return"),
    "BASEPOWER-FID02": ("FID 02h：手動 power state", "FID 02h: manual power state"),
    "BASEPOWER-WORKLOAD": ("Workload Hint", "Workload Hint"),
    "BASEPOWER-RTD3": ("RTD3E／RTD3R 邊界", "RTD3E/RTD3R boundary"),
    "BASEPOWER-FID04": ("FID 04h：temperature threshold", "FID 04h: temperature threshold"),
    "BASEPOWER-HYST": ("temperature hysteresis", "Temperature hysteresis"),
    "BASEPOWER-FID0C": ("FID 0Ch：APST enable", "FID 0Ch: APST enable"),
    "BASEPOWER-APST-ENTRY": ("APST 256-byte table", "APST 256-byte table"),
    "BASEPOWER-APST-NOPPME": ("APSTE × NOPPME", "APSTE × NOPPME"),
    "BASEPOWER-FID10": ("FID 10h：TMT1／TMT2", "FID 10h: TMT1/TMT2"),
    "BASEPOWER-HCTM": ("HCTM control loop", "HCTM control loop"),
    "BASEPOWER-FID11": ("FID 11h：background power permission", "FID 11h: background-power permission"),
    "BASEPOWER-OBSERVE": ("SMART／Health 驗證閉環", "SMART/Health verification loop"),
    "BASEDIAGMEM-SELFTEST-GATE": ("先確認 self-test capability 與 concurrency scope", "Gate self-test capability and concurrency scope"),
    "BASEDIAGMEM-SELFTEST-NSID": ("NSID 決定測試涵蓋範圍", "NSID selects the test scope"),
    "BASEDIAGMEM-SELFTEST-STC": ("STC 與 CDW15 的命令編碼", "STC and CDW15 command encoding"),
    "BASEDIAGMEM-SELFTEST-INPROGRESS": ("已有 operation 時的狀態矩陣", "State matrix while an operation is active"),
    "BASEDIAGMEM-SELFTEST-COMPLETION": ("CQE 不等於測試完成", "A CQE is not test completion"),
    "BASEDIAGMEM-SELFTEST-BACKGROUND": ("背景測試的 suspend／resume 契約", "Background-test suspend/resume contract"),
    "BASEDIAGMEM-SELFTEST-TIMING": ("short 與 extended 的 reset 差異", "Reset differences between short and extended tests"),
    "BASEDIAGMEM-SELFTEST-ABORTS": ("Format、sanitize 與 abort 條件", "Format, sanitize, and abort conditions"),
    "BASEDIAGMEM-SELFTEST-LOG-COMMAND": ("564-byte LID 06h command 計算", "Constructing the 564-byte LID 06h command"),
    "BASEDIAGMEM-SELFTEST-CURRENT": ("current operation 與完成百分比", "Current operation and completion percentage"),
    "BASEDIAGMEM-SELFTEST-HISTORY": ("20 筆 newest-first result ring", "Twenty newest-first results"),
    "BASEDIAGMEM-SELFTEST-RESULT": ("DSTS 與 SEGN 的條件式解碼", "Conditional DSTS and SEGN decoding"),
    "BASEDIAGMEM-SELFTEST-VALIDITY": ("VDINFO 是四個獨立 validity gates", "VDINFO contains four independent validity gates"),
    "BASEDIAGMEM-SELFTEST-NVM-FLBA": ("NVM Command Set 補完 FLBA 語意", "NVM Command Set completes FLBA semantics"),
    "BASEDIAGMEM-SELFTEST-DEBUG": ("以三個時間點重建 self-test", "Reconstruct self-test across three timestamps"),
    "BASEDIAGMEM-HMB-CAPABILITY": ("HMB capability 與 descriptor limits", "HMB capability and descriptor limits"),
    "BASEDIAGMEM-HMB-OWNERSHIP": ("HMB 是 ownership transfer", "HMB is an ownership transfer"),
    "BASEDIAGMEM-HMB-SET-COMMAND": ("FID 0Dh 的 Set Features layout", "Set Features layout for FID 0Dh"),
    "BASEDIAGMEM-HMB-DESCRIPTORS": ("HMDL 與 descriptor page math", "HMDL and descriptor page math"),
    "BASEDIAGMEM-HMB-NUMERIC": ("256 KiB HMB 完整計算", "Complete 256-KiB HMB calculation"),
    "BASEDIAGMEM-HMB-SEQUENCE": ("enable／disable 的 completion fence", "Enable/disable completion fence"),
    "BASEDIAGMEM-HMB-GET": ("Get Features 分開讀 policy 與 state", "Get Features separates policy from state"),
    "BASEDIAGMEM-HMB-NONOP": ("HMNARE 與 HMNAR 不相同", "HMNARE and HMNAR are different"),
    "BASEDIAGMEM-HMB-RESET-RTD3": ("reset／RTD3 後的 Memory Return", "Memory Return after reset or RTD3"),
    "BASEDIAGMEM-HMB-SURPRISE": ("surprise removal 的資料正確性", "Data correctness during surprise removal"),
    "BASEDIAGMEM-DOORBELL-STRIDE": ("DSTRD encoding 到 cacheline stride", "DSTRD encoding to cacheline stride"),
    "BASEDIAGMEM-DOORBELL-DEBUG": ("emulator 的 doorbell 證據鏈", "Doorbell evidence chain for emulators"),
    "BASEDIAGMEM-VENDOR-GATE": ("Admin 與 I/O vendor format 分開 gate", "Gate Admin and I/O vendor formats independently"),
    "BASEDIAGMEM-VENDOR-FORMAT": ("Figure 94 的 boundary-safe layout", "Boundary-safe Figure 94 layout"),
    "BASEDIAGMEM-VENDOR-LENGTH": ("NDT／NDM 是實際 dword count", "NDT/NDM are actual dword counts"),
    "BASEDIAGMEM-BOUNDARY-DEBUG": ("從第一個 broken boundary 開始 Debug", "Debug from the first broken boundary"),
    "BASENSMGMT-SELFTEST-GATE": ("先確認 Self-test capability 與 concurrency scope", "Gate Self-test capability and concurrency scope"),
    "BASENSMGMT-SELFTEST-NSID": ("NSID 決定 Self-test 涵蓋範圍", "NSID selects Self-test scope"),
    "BASENSMGMT-SELFTEST-STC": ("STC 與 CDW15 的命令編碼", "STC and CDW15 command encoding"),
    "BASENSMGMT-SELFTEST-INPROGRESS": ("operation in progress 的命令矩陣", "Command matrix while an operation is active"),
    "BASENSMGMT-SELFTEST-COMPLETION": ("CQE 不等於背景測試完成", "A CQE is not background-test completion"),
    "BASENSMGMT-SELFTEST-BACKGROUND": ("背景測試的 suspend／resume 契約", "Background-test suspend/resume contract"),
    "BASENSMGMT-SELFTEST-TIMING": ("short 與 extended 的 reset 差異", "Reset differences between short and extended tests"),
    "BASENSMGMT-SELFTEST-ABORTS": ("Format、sanitize 與 abort 條件", "Format, sanitize, and abort conditions"),
    "BASENSMGMT-SELFTEST-LOG-COMMAND": ("564-byte LID 06h command 計算", "Constructing the 564-byte LID 06h command"),
    "BASENSMGMT-SELFTEST-CURRENT": ("current operation 與完成百分比", "Current operation and completion percentage"),
    "BASENSMGMT-SELFTEST-HISTORY": ("20 筆 newest-first result history", "Twenty newest-first result entries"),
    "BASENSMGMT-SELFTEST-VALIDITY": ("先驗證 validity bit 再讀欄位", "Validate the validity bit before the field"),
    "BASENSMGMT-SELFTEST-NVM-FLBA": ("NVM Command Set 補完 FLBA 語意", "NVM Command Set completes FLBA semantics"),
    "BASENSMGMT-CAPACITY-MODEL": ("NSZE、NCAP、NUSE 的容量不等式", "The NSZE, NCAP, NUSE capacity inequality"),
    "BASENSMGMT-THIN-PROVISIONING": ("THINP 決定 NCAP／NUSE 回報責任", "THINP governs NCAP/NUSE reporting"),
    "BASENSMGMT-NSMGMT-CAPABILITY": ("完整 capability 是 Manage 加 Attach", "The complete capability combines Manage and Attach"),
    "BASENSMGMT-NSID-LIFECYCLE": ("allocated、active、inactive、unallocated", "Allocated, active, inactive, and unallocated"),
    "BASENSMGMT-CREATE-PREFLIGHT": ("create 前的 capability／capacity 盤點", "Capability and capacity preflight before create"),
    "BASENSMGMT-CREATE-BASE-COMMAND": ("Base 4096-byte create envelope", "The Base 4096-byte create envelope"),
    "BASENSMGMT-CREATE-NVM-PAYLOAD": ("NVM host-specified create fields", "NVM host-specified create fields"),
    "BASENSMGMT-PROTECTION-VALIDATION": ("Protection Information 與 LBSTM gates", "Protection Information and LBSTM gates"),
    "BASENSMGMT-FDP-VALIDATION": ("FDP Placement Handle validation", "FDP Placement Handle validation"),
    "BASENSMGMT-GROUP-SELECTION": ("NVMSETID／ENDGID 決策矩陣", "NVMSETID/ENDGID decision matrix"),
    "BASENSMGMT-ALLOCATION-ROUNDING": ("requested size 不等於 capacity consumption", "Requested size need not equal capacity consumption"),
    "BASENSMGMT-GRANULARITY-HINTS": ("NSG／NCG 是配置提示而非合法性門檻", "NSG/NCG are allocation hints, not validity gates"),
    "BASENSMGMT-ATTACH-COMMAND": ("Controller List 建立 access relationship", "Controller List establishes access relationships"),
    "BASENSMGMT-ATTACH-LIMITS": ("MAXDNA 與 MAXCNA 是兩層 limits", "MAXDNA and MAXCNA are two levels of limits"),
    "BASENSMGMT-CREATE-COMPLETION": ("CQE.DW0 回 NSID，但尚未 attached", "CQE DW0 returns an NSID that is not yet attached"),
    "BASENSMGMT-DELETE": ("detach 後再 delete 的可控流程", "A controlled detach-then-delete flow"),
    "BASENSMGMT-RESTORE-DEFAULT": ("RDNCS、delete-all 與 DNCS", "RDNCS, delete-all, and DNCS"),
    "BASENSMGMT-COMMAND-STATUS": ("用 command-specific status 定位 failure gate", "Use command-specific status to locate the failed gate"),
    "BASENSMGMT-NAMESPACE-EVENTS": ("AER 後重新 Identify inventory", "Refresh Identify inventory after AER"),
    "BASENSMGMT-GRANULARITY-EXAMPLE": ("4 KiB LBA 的 NSG／NCG 計算", "NSG/NCG calculation with 4-KiB LBAs"),
    "BASENSMGMT-END-TO-END-DEBUG": ("從第一個生命週期邊界開始 Debug", "Debug from the first lifecycle boundary"),
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

install_bts(REPORTS, CORE_TITLES, REPORT_MODULES, REPORT_GLOSSARIES)
install_nvmcs(REPORTS, CORE_TITLES, REPORT_MODULES, REPORT_GLOSSARIES)
try:
    from scripts.nvme_reader_edits import apply as apply_reader_edits
except ModuleNotFoundError:
    from nvme_reader_edits import apply as apply_reader_edits
apply_reader_edits(REPORTS, REPORT_MODULES, CORE_TITLES)
try:
    from scripts.nvme_plain_language import apply as apply_plain_language, chinese
except ModuleNotFoundError:
    from nvme_plain_language import apply as apply_plain_language, chinese
apply_plain_language(REPORT_MODULES)
sys.path.insert(0, str(ROOT))
from scripts.nvme_report_split import install as install_split, SPLITS
install_split(REPORTS, CORE_TITLES, REPORT_MODULES, REPORT_GLOSSARIES)
for new_id, (old_id, *_) in SPLITS.items():
    POST_IMAGES[new_id] = POST_IMAGES[old_id]
    REPORTS[new_id]['date'] = '2026-09-11'
try:
    from scripts.nvme_figure_notes import note as authored_figure_note
except ModuleNotFoundError:
    from nvme_figure_notes import note as authored_figure_note


def artifact_ids(report_id: str) -> list[str]:
    if report_id in SPLITS:
        key = REPORTS[report_id]['prefix'].lower()
        return [key+'-tutorial-html', key+'-zh-md', key+'-en-md']
    key = {
        "base-ch1-2": "base12",
        "base-ch3": "base3",
        "base-ch4": "base4",
        "base-admin-fw-logs": "basefwlog",
        "base-power-features": "basepower",
        "base-self-test-hmb-emulation": "basediagmem",
        "base-self-test-namespace-management": "basensmgmt",
        "base-boot-telemetry-sanitize": "basebts",
        "nvm-command-set-1.3": "nvmcs13",
        "pcie-transport-1.4": "pcie14",
    }[report_id]
    return [
        f"{key}-tutorial-html",
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

    if language == 'zh':
        from scripts.nvme_figure_lessons import lesson
        teaching = lesson(figure)
        return dict(purpose=teaching['takeaway'], example=teaching['example'])

    if figure.get('report_id') in SPLITS:
        figure = dict(figure, report_id=SPLITS[figure['report_id']][0])

    if figure.get("report_id") in {"base-boot-telemetry-sanitize", "nvm-command-set-1.3"}:
        return {
            "purpose": (nvmcs_figure_guide if figure['report_id'] == 'nvm-command-set-1.3' else bts_figure_guide)(figure, language),
            "reading": "Decode the source-specific fields below." if language == "en" else "依下列來源欄位逐項解碼。",
            "example": "Apply the worked example in the linked teaching module." if language == "en" else "套用相應教學單元的具體案例。",
            "caveat": "Preserve target, state, and applicability; the original cross-reference is retained when suspected to be misplaced." if language == "en" else "保留 target、state 與適用條件；疑似錯置的原引用仍保留供核對。",
            "item_text": ", ".join(figure["key_items"]),
            "keyword_text": ", ".join(figure["source_keywords"]) or "none",
        }

    title = figure["title"]
    lower_title = title.lower()
    number = figure["number"]
    is_fwlog = figure.get("report_id") == "base-admin-fw-logs"
    is_power = figure.get("report_id") == "base-power-features"
    is_diagmem = figure.get("report_id") == "base-self-test-hmb-emulation"
    is_nsmgmt = figure.get("report_id") == "base-self-test-namespace-management"
    items = list(figure.get("key_items", []))
    item_text = ", ".join(items)
    first = items[0] if items else title
    keywords = list(figure.get("source_keywords", []))
    keyword_text = ", ".join(f"`{item}`" for item in keywords) or "none"
    authored_purpose = authored_figure_note(figure, language)

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
        elif is_fwlog and "data pointer" in lower_title:
            purpose = f"Defines how {title} identifies the destination or source buffer for this command."
            reading = (
                f"Resolve pointer type and address before checking transfer length and alignment. Evidence index: {item_text}."
            )
            example = (
                f"Validate the pointer form represented by {first}, then confirm the boundary associated with {second} before starting the transfer."
            )
        elif is_fwlog and "log page" in lower_title:
            purpose = f"Defines the returned log-page layout and selection context for {title}."
            reading = (
                f"Start with the fixed header and scope, validate counts or lengths, then walk entries or data areas in order. Evidence index: {item_text}."
            )
            example = (
                f"Read {first} first, use {second} as an independent size or identity check, and stop before any unreturned byte."
            )
        elif is_fwlog and ("event" in lower_title or "logging requirements" in lower_title):
            purpose = f"Defines the event record, event taxonomy, or logging condition represented by {title}."
            reading = (
                f"Resolve event type and record length before decoding event-specific data. Evidence index: {item_text}."
            )
            example = (
                f"Identify {first}, validate the record boundary using {second}, and decode only the data defined for that event type."
            )
        elif is_fwlog and ("operation" in lower_title or "state machine" in lower_title):
            purpose = f"Defines the operation or state progression represented by {title}."
            reading = (
                f"Follow request, state, transition condition, and completion in order. Evidence index: {item_text}."
            )
            example = (
                f"Begin with {first}, move to the state associated with {second} only when the cited transition condition is satisfied."
            )
        elif is_fwlog and any(word in lower_title for word in (" types", " codes", " scale", " sensors")):
            purpose = f"Defines the enumerated values, measurement scale, or sensor selection represented by {title}."
            reading = (
                f"Resolve the selector or code first, then apply its unit, scale, or reserved-value rule. Evidence index: {item_text}."
            )
            example = (
                f"Decode {first}, then apply the interpretation selected by {second}; do not assign meaning to a reserved value."
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
        elif is_power:
            purpose = f"Maps the power/thermal control relationship represented by {title}."
            reading = (
                f"Trace selector, state or threshold, transition condition, and observation evidence in order. "
                f"Source-derived checkpoints: {item_text}."
            )
            example = (
                f"Record {first} as raw input, validate {second} against the cited capability or state, "
                "then correlate completion time with temperature and I/O-latency evidence."
            )
        elif is_diagmem:
            purpose = f"Connects {title} to a self-test, host-memory, doorbell, or vendor-command engineering boundary."
            reading = (
                f"Resolve capability and owner first, decode {item_text}, then verify the completion, log, or memory-lifecycle evidence."
            )
            example = (
                f"Capture {first} as raw evidence, validate {second} against the cited section, and reject any state or byte range that crosses the declared boundary."
            )
        elif is_nsmgmt:
            purpose = f"Connects {title} to the Self-test evidence path or namespace lifecycle."
            reading = (
                f"Identify the object and lifecycle state, decode {item_text}, then verify the next transition with a CQE, log, event, or Identify snapshot."
            )
            example = (
                f"Capture {first} as raw input, validate {second} against the cited capability and state, then record the resulting lifecycle transition."
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
        elif is_fwlog and "data pointer" in lower_title:
            purpose = f"定義〈{title}〉如何指出本命令的來源或目的 buffer。"
            reading = (
                f"先判斷 pointer type 與 address，再核對 transfer length 和 alignment；來源欄位索引：{item_text}。"
            )
            example = (
                f"先驗證 {first} 所代表的 pointer 形式，再核對 {second} 對應的邊界，通過後才開始 transfer。"
            )
        elif is_fwlog and "log page" in lower_title:
            purpose = f"定義〈{title}〉的回傳配置與 selector／scope 上下文。"
            reading = (
                f"先讀固定 header 與 scope，驗證 count／length 後，再依序走訪 entry 或 data area；來源欄位索引：{item_text}。"
            )
            example = (
                f"先讀 {first}，再以 {second} 作為獨立的大小或 identity 檢查點，且不得解析超過實際回傳的 byte。"
            )
        elif is_fwlog and ("event" in lower_title or "logging requirements" in lower_title):
            purpose = f"定義〈{title}〉所表示的 event record、event 分類或記錄條件。"
            reading = (
                f"先判斷 Event Type 與 record length，再解 event-specific data；來源欄位索引：{item_text}。"
            )
            example = (
                f"先辨認 {first}，以 {second} 驗證 record 邊界，再只解析該 Event Type 定義的資料。"
            )
        elif is_fwlog and ("operation" in lower_title or "state machine" in lower_title):
            purpose = f"定義〈{title}〉所表示的 operation 或 state progression。"
            reading = (
                f"依序追蹤 request、state、transition condition 與 completion；來源欄位索引：{item_text}。"
            )
            example = (
                f"從 {first} 開始，只有在引用條文的 transition condition 成立時，才移到 {second} 所對應的 state。"
            )
        elif is_fwlog and any(word in lower_title for word in (" types", " codes", " scale", " sensors")):
            purpose = f"定義〈{title}〉中的列舉值、measurement scale 或 sensor selector。"
            reading = (
                f"先解 selector／code，再套用對應 unit、scale 或 reserved-value rule；來源欄位索引：{item_text}。"
            )
            example = (
                f"先解碼 {first}，再套用 {second} 選定的解讀方式；保留值不得自行賦義。"
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
        elif is_power:
            purpose = f"呈現〈{title}〉所描述的 power／thermal 控制關係。"
            reading = (
                f"依序追蹤 selector、state 或 threshold、transition condition 與觀測證據；"
                f"來源欄位索引：{item_text}。"
            )
            example = (
                f"保存 {first} 的 raw input，先用引用 capability／state 驗證 {second}，再把 completion time "
                "與 temperature、I/O latency 證據放在同一條 timeline。"
            )
        elif is_diagmem:
            purpose = f"把〈{title}〉連到 self-test、host memory、doorbell 或 vendor command 的工程邊界。"
            reading = (
                f"先辨認 capability 與 owner，再解碼 {item_text}，最後以 completion、log 或 memory lifecycle 證據核對。"
            )
            example = (
                f"保存 {first} 的 raw evidence，依引用 section 驗證 {second}，若 state 或 byte range 超出宣告邊界就拒絕繼續。"
            )
        elif is_nsmgmt:
            purpose = f"把〈{title}〉連到 Self-test 證據路徑或 namespace lifecycle。"
            reading = (
                f"先確認物件與 lifecycle state，再解碼 {item_text}，最後以 CQE、log、event 或 Identify snapshot 驗證下一個 transition。"
            )
            example = (
                f"保存 {first} 的 raw input，依 capability 與目前 state 驗證 {second}，再記錄實際發生的 lifecycle transition。"
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

    if authored_purpose:
        purpose = authored_purpose

    if figure.get("mode") == "scope-reduced" or figure.get("scope_reduced"):
        caveat += (
            " Only the PCIe/memory-based portion is in scope."
            if language == "en"
            else " 本報告只解釋 PCIe／memory-based 部分。"
        )
    focus = figure.get("dependency_focus")
    if figure.get("role") == "referenced_dependency":
        references = ", ".join(f"§{item}" for item in figure.get("referenced_from", []))
        if language == "en":
            caveat += (
                f" This Figure is a dependency referenced from {references}; only the "
                "elements needed by the requested sections are taught here."
            )
            if focus:
                caveat += " " + focus["en"]
        else:
            caveat += (
                f" 這是 {references} 直接引用的範圍外相依 Figure；此處只教學指定章節需要的元素。"
            )
            if focus:
                caveat += " " + focus["zh_tw"]
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
        "scope_entry_id": item.get("scope_entry_id") or report["scope_entry"],
        "heading_zh_tw": CORE_TITLES[claim_id][0],
        "heading_en": CORE_TITLES[claim_id][1],
    }
    result["citation_zh_tw"] = cite(result, "zh")
    result["citation_en"] = cite(result, "en")
    return result


def make_figure_claim(report_id: str, report: dict, figure: dict) -> dict:
    figure_id = figure["id"]
    zh_parts = figure_explanation(figure, "zh")
    en_parts = figure_explanation(figure, "en")
    result = {
        "id": f"{figure_id}-CLAIM",
        "report_id": report_id,
        "source_id": figure["source_id"],
        "revision": SOURCES[figure["source_id"]]["revision"],
        "section": figure["section"],
        "figure": str(figure["number"]),
        "table": None,
        "printed_pages": figure["printed_pages"],
        "pdf_pages": figure["pdf_pages"],
        "normative_keyword": "none",
        "zh_tw": zh_parts['purpose'],
        "en": (
            f"Figure {figure['number']}, \"{figure['title']}\": "
            f"{en_parts['purpose']}"
        ),
        "scope_entry_id": figure["scope_entry_id"],
        "source_keywords": list(figure.get("source_keywords", [])),
        "key_items": list(figure.get("key_items", [])),
        "evidence_digest": figure.get("evidence_digest", ""),
    }
    result["citation_zh_tw"] = cite(result, "zh", int(figure["number"]))
    result["citation_en"] = cite(result, "en", int(figure["number"]))
    return result


def frontmatter(
    report_id: str, title: str, description: str, language: str
) -> str:
    lang = "en" if language == "en" else "zh-Hant-TW"
    image = POST_IMAGES[report_id][language]
    report_date = REPORTS[report_id].get("date", "2026-08-28")
    slugs = {'base-boot-telemetry-sanitize': 'boot-telemetry-sanitize', 'nvm-command-set-1.3': 'nvm-command-set-1-3'}
    slugs.update({rid:rid.removeprefix('base-') for rid in SPLITS})
    permalink = f"permalink: /nvme/{slugs[report_id]}-{'en' if language == 'en' else 'zh-tw'}/\n" if report_id in slugs else ""
    return f"""---
{permalink}layout: post
read_time: true
show_date: true
title: "{title}"
date: {report_date}
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


def clean_public_language(content: str) -> str:
    """Keep public editions concrete and free of authoring shorthand.

    The source records may retain internal review labels, but the rendered
    editions should describe the reader's action directly.  This final pass
    also covers legacy figure explanations that are shared by the paired
    posts.
    """
    replacements = (
        (r"\bDebug first broken boundary\b", "Review the first broken boundary"),
        (r"\bDebug from the first\b", "Review from the first"),
        ("Debug 時", "證據檢視時"),
        ("Debug 圖", "證據圖"),
        ("Debug 還要", "證據檢視還要"),
        (r"\bdebugging\b", "evidence review"),
        (r"\bDebugging\b", "Evidence review"),
        (r"\bdebug\b", "diagnostic review"),
        (r"\bDebug\b", "Evidence review"),
        (r"\bdecoded\b", "interpreted values"),
        (r"\bDecoded\b", "Interpreted values"),
        (r"\bdecoding\b", "reading the fields"),
        (r"\bDecoding\b", "Reading the fields"),
        (r"\bdecode\b", "read the fields"),
        (r"\bDecode\b", "Read the fields"),
        (r"\blocated\b", "found"),
        (r"\bLocated\b", "Found"),
        (r"\blocating\b", "finding"),
        (r"\bLocating\b", "Finding"),
        (r"\blocate\b", "find"),
        (r"\bLocate\b", "Find"),
        ("解碼", "依欄位換算"),
    )
    for old, new in replacements:
        if old.startswith(r"\b"):
            content = re.sub(old, new, content)
        else:
            content = content.replace(old, new)
    return content


def clean_claim_language(claim: dict) -> dict:
    """Apply the public wording pass to the claim text used for rendering."""
    cleaned = dict(claim)
    for field in ("zh_tw", "en"):
        if cleaned.get(field):
            cleaned[field] = clean_public_language(cleaned[field])
    cleaned['zh_tw'] = chinese(cleaned['zh_tw'])
    return cleaned


FW_GLOSSARY = [
    ("Domain", "Firmware slots 的共享與 activation 範圍；不一定等於單一 controller。", "The sharing and activation scope for firmware slots; not necessarily one controller."),
    ("Firmware image", "可下載、驗證、保存並啟用的 firmware 內容。", "Firmware content that can be downloaded, validated, stored, and activated."),
    ("Firmware slot", "保存一個 firmware revision 的邏輯位置；不等於目前正在執行。", "A logical location holding one firmware revision; not necessarily the executing revision."),
    ("Activation", "讓某個 slot 的 image 成為 controller 正在執行的 firmware。", "Making the image in a slot become the firmware executed by the controller."),
    ("FR", "Firmware Revision；目前正在執行的 8-byte ASCII revision。", "Firmware Revision; the eight-byte ASCII revision currently executing."),
    ("FRMW", "Firmware Updates capability byte；集合 SMUD、FAWR、NOFS、FFSRO。", "Firmware Updates capability byte containing SMUD, FAWR, NOFS, and FFSRO."),
    ("SMUD", "Support Multiple Update Detection；能否偵測重疊 update sequence。", "Support Multiple Update Detection; whether overlapping update sequences can be detected."),
    ("FAWR", "Firmware Activation Without Reset；是否支援不經 reset 的 activation。", "Firmware Activation Without Reset support."),
    ("NOFS", "Number Of Firmware Slots；domain 支援 1 到 7 個 slots。", "Number Of Firmware Slots; one through seven slots in the domain."),
    ("FFSRO", "First Firmware Slot Read Only；slot 1 是否唯讀。", "First Firmware Slot Read Only."),
    ("MTFA", "Maximum Time for Firmware Activation；activation 暫停 command processing 的上限，100 ms units。", "Maximum Time for Firmware Activation; command-processing pause in 100 ms units."),
    ("FWUG", "Firmware Update Granularity；NUMD／OFST 的 granularity 與 alignment，4 KiB units。", "Firmware Update Granularity for NUMD/OFST alignment, in 4 KiB units."),
    ("MPTFAWR", "Maximum Processing Time for Firmware Activation Without Reset；CA=011b command 完成時間，100 ms units。", "Maximum Processing Time for Firmware Activation Without Reset, in 100 ms units."),
    ("DPTR / PRP", "Data Pointer／Physical Region Page；指向本次 transfer buffer。", "Data Pointer / Physical Region Page identifying the transfer buffer."),
    ("NUMD / OFST", "0's-based dword count／image-relative dword offset。", "Zero-based dword count / image-relative dword offset."),
    ("CA / FS", "Commit Action／Firmware Slot；決定 Commit 做什麼、作用在哪個 slot。", "Commit Action / Firmware Slot selecting the operation and target slot."),
    ("MUD", "Multiple Update Detected；Firmware Commit CQE 的 overlap 證據。", "Multiple Update Detected; overlap evidence in the Firmware Commit CQE."),
    ("LID / RAE", "Log Page Identifier／Retain Asynchronous Event。", "Log Page Identifier / Retain Asynchronous Event."),
    ("AFI", "Active Firmware Info；LID 03h byte 0。", "Active Firmware Info in byte 0 of LID 03h."),
    ("NAFS / CAFS", "Next／Current Active Firmware Slot。", "Next / Current Active Firmware Slot."),
    ("FRS1…FRS7", "Firmware Revision for Slot 1…7；每格 8-byte ASCII。", "Firmware Revision for Slots 1 through 7; eight ASCII bytes each."),
]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--reports', nargs='+', choices=list(REPORTS), help='Rebuild selected reports, newest first by default.')
    args = parser.parse_args()
    sys.path.insert(0, str(ROOT))
    from scripts.nvme_reader import render
    contract = json.loads(
        (CONTROL / "output-contract.json").read_text(encoding="utf-8")
    )
    register_doc = json.loads(
        (CONTROL / "figure-table-register.json").read_text(encoding="utf-8")
    )
    scope_doc = json.loads((CONTROL / "scope.json").read_text(encoding="utf-8"))
    figure_allowlists = {
        item["id"]: set(item.get("included_figure_ids", []))
        for item in scope_doc["reports"]
    }
    register_entries = register_doc["entries"]
    artifacts = {item["id"]: item for item in contract["artifacts"]}
    all_claims = []

    priority = ['nvm-command-set-1.3', 'base-boot-partitions', 'base-telemetry', 'base-sanitize']
    order = priority + [key for key in reversed(REPORTS) if key not in priority]
    for report_id in order:
        report = REPORTS[report_id]
        figures = sorted(
            [
                item
                for item in register_entries
                if item["report_id"] == report_id
                and item["scope_status"] == "INCLUDE"
                and (
                    not figure_allowlists.get(report_id)
                    or item["id"] in figure_allowlists[report_id]
                )
            ],
            key=lambda item: (
                item.get("role") == "referenced_dependency",
                int(item["number"]),
            ),
        )
        for figure in figures:
            if not figure.get("key_items") or not figure.get("evidence_digest"):
                raise ValueError(
                    f"{figure['id']} lacks tracked compact PDF evidence"
                )
        report_claims = [
            clean_claim_language(make_claim(report_id, report, item))
            for item in report["claims"]
        ]
        report_claims.extend(
            clean_claim_language(make_figure_claim(report_id, report, item))
            for item in figures
        )
        all_claims.extend(report_claims)

        if args.reports and report_id not in args.reports:
            continue
        ids = artifact_ids(report_id)
        for artifact_id in ids:
            artifact = artifacts[artifact_id]
            language = 'en' if artifact['language'] == 'en' else 'zh'
            content = render(report_id, report, report_claims, figures,
                             REPORT_MODULES[report_id], language, artifact['format'] == 'html', sys.modules[__name__])
            content = clean_public_language(content)
            # Base Chapter 3 and the firmware/log report explicitly exclude
            # transport discovery. Keep the teaching wording within each
            # report's registered scope instead of exposing that term in a
            # figure title or inherited prerequisite sentence.
            if report_id in {"base-ch3", "base-admin-fw-logs"} and language == "en":
                content = re.sub(
                    r"\brediscovery\b|\bdiscovery\b|\bdiscovered\b|\bdiscovering\b",
                    "out-of-scope transport material",
                    content,
                    flags=re.IGNORECASE,
                )
            if artifact["format"] != "html":
                sibling = artifacts[ids[1] if artifact["language"] == "en" else ids[2]]
                sibling_post = Path(sibling["path"]).stem
                label = "繁體中文" if artifact["language"] == "en" else "English"
                switch = f"\n[{label}]({{% post_url {sibling_post} %}})\n"
                end = content.index("---", 4) + 3
                content = content[:end] + switch + content[end:]
            path = ROOT / artifacts[artifact_id]["path"]
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
        print(f'Built {report_id}: 3 editions', flush=True)

    claims_doc = {
        "schema_version": 3,
        "allowed_normative_keywords": [
            "mandatory",
            "may",
            "obsolete",
            "optional",
            "reserved",
            "shall",
            "shall not",
            "should",
            "should not",
            "none",
        ],
        "claims": all_claims,
    }
    (CONTROL / "claims.json").write_text(
        json.dumps(claims_doc, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    # Topic landing page lists only current editions. Retired URLs are ordinary
    # pages with links, so neither pagination nor feeds repeat the old articles.
    from scripts.nvme_reader_context import REPORT_CONTEXT
    hub=['---\nlayout: menu-page\ntitle: NVMe 教學與報告\npermalink: /nvme-notes/\nnvme_notes: true\n---\n<div class="nvme-note">',
         '<h1>NVMe 教學與報告</h1><p>先用中英文報告理解主軸、流程與案例，再打開 Spec 閱讀精確定義。中文教學 HTML 提供由淺入深的解釋，以及每張範圍內圖表的重點、案例與細節。</p>']
    for rid in order:
        editions=[a for a in contract['artifacts'] if a['report_id']==rid]
        hub.append('<section><h2>'+html.escape(REPORTS[rid]['title_zh'])+'</h2><p>'+html.escape(REPORT_CONTEXT[rid]['intro']['zh'])+'</p><ul>')
        for a in editions:
            if a['format']=='html':
                link='/'+a['path']; label='完整中文教學 HTML（iPad／電腦）'
            else:
                link='{% post_url '+Path(a['path']).stem+' %}'; label='English overview' if a['language']=='en' else '中文全局報告'
            hub.append('<li><a href="'+link+'">'+label+'</a></li>')
        hub.append('</ul></section>')
    hub.append('</div>')
    (ROOT/'_pages/nvme-notes.html').write_text('\n'.join(hub)+'\n',encoding='utf-8')
    print(
        f"Tracked {len(contract['artifacts'])} artifacts, {len(all_claims)} claims, "
        f"using {len(register_entries)} tracked Figure records"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
