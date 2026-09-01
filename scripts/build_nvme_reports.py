#!/usr/bin/env python3
"""Build NVMe reports from tracked scope, claims, and compact PDF evidence."""

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
    "base-admin-fw-logs": {
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
        "base-admin-fw-logs": "basefwlog",
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
    is_fwlog = figure.get("report_id") == "base-admin-fw-logs"
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
        "scope_entry_id": item.get("scope_entry_id") or report["scope_entry"],
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
        "scope_entry_id": figure["scope_entry_id"],
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
    if any(key in claim_id for key in ("FW-", "COMMIT", "DOWNLOAD", "UUID")):
        return "把 image portion、firmware slot、Commit Action 與 activation 所需 reset 分成四欄逐項核對。"
    if "LOG-" in claim_id:
        return "先用 LID 決定資料 scope，再核對 transfer length、offset type、RAE 與 log-specific header。"
    return {
        "base-ch1-2": "先確認概念位於規格家族、儲存階層或路徑層級，不把不同層級合併。",
        "base-ch3": "先寫清楚動作主體是 host 或 controller，再核對當下 lifecycle state。",
        "base-ch4": "先定位資料結構的 byte／dword 邊界，再閱讀欄位條件。",
        "base-admin-fw-logs": "先判斷目前位於 download、commit、activation 或 log verification 階段。",
        "pcie-transport-1.4": "先找 Base 的通用規則，再疊加 PCIe Transport 的專屬限制。",
    }[report_id]


def section_group(section: str) -> str:
    if section.lower().startswith("annex"):
        return section
    pieces = section.split(".")
    return ".".join(pieces[:2]) if len(pieces) > 1 else pieces[0]


def figure_group(figure: dict) -> str:
    if figure.get("role") == "referenced_dependency":
        return "dependency"
    return section_group(str(figure["section"]))


def figure_group_label(group: str, language: str) -> str:
    if group == "dependency":
        return (
            "Referenced Figure dependencies (outside the main section range)"
            if language == "en"
            else "引用相依 Figure（位於主章節範圍外）"
        )
    return f"§{group}"


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
        group = figure_group(figure)
        if group not in figure_groups:
            figure_groups.append(group)
    dependency_count = sum(
        item.get("role") == "referenced_dependency" for item in figures
    )
    figure_policy = (
        "<p><strong>Figure／Table 政策：</strong>不重製規格原圖；以下逐張說明用途、"
        "讀法、條件與說明性範例。指定正文沒有引用任何編號 Table；"
        "欄位表在本規格中以 Figure 編號。</p>"
        if report_id == "base-admin-fw-logs"
        else "<p><strong>Figure 政策：</strong>不重製規格原圖；以下逐張說明用途、"
        "讀法、條件與說明性範例。欄位表雖以表格呈現，在本範圍的規格中仍以 Figure 編號。</p>"
    )

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
        figure_policy,
        f"<p><strong>完整度：</strong>本檔介紹 {len(figures)} 張納入範圍的 Figure。"
        + (
            f"其中 {dependency_count} 張位於主章節範圍外，但因正文直接引用而納入相依教學。"
            if dependency_count
            else ""
        )
        + "100 分鐘口頭報告應以規格重點與必講 Figure 為主；其餘 Figure 作為附錄查閱，"
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
                f'<li><a href="#section-{anchor(group)}">'
                f'{html.escape(figure_group_label(group, "zh"))}</a></li>'
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
        group = figure_group(figure)
        if group != active_group:
            if active_group:
                parts.append("</section>")
            active_group = group
            parts.append(
                f'<section id="section-{anchor(group)}"><h3>'
                f'{html.escape(figure_group_label(group, "zh"))}</h3>'
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
            f"<p>查證日期：{html.escape(report.get('verified_date', '2026-08-29'))}。目前未納入其他 Errata、ECN、"
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
    report_date = REPORTS[report_id].get("date", "2026-08-28")
    return f"""---
layout: post
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
    dependency_count = sum(
        item.get("role") == "referenced_dependency" for item in figures
    )
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
                f"Verification date: {report.get('verified_date', '2026-08-29')}. No additional errata, ECNs, "
                "Technical Proposals, controller-vendor documents, or source text "
                "from the external PCI Express Base Specification are included."
                if english
                else f"查證日期：{report.get('verified_date', '2026-08-29')}。目前未納入其他 Errata、ECN、"
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
                + (
                    f" {dependency_count} Figures are outside the main section range but are included because the requested text directly references them."
                    if dependency_count
                    else ""
                )
                if english
                else f"本報告介紹全部 {len(figures)} 張納入範圍的 Figure。100 分鐘簡報"
                "以 section 主線與必講 Figure 為主，其餘 Figure 仍完整保留作為附錄。"
                + (
                    f"其中 {dependency_count} 張位於主章節範圍外，但因指定正文直接引用而納入相依教學。"
                    if dependency_count
                    else ""
                )
            ),
            "",
        ]
    )
    figure_groups: list[str] = []
    for figure in figures:
        group = figure_group(figure)
        if group not in figure_groups:
            figure_groups.append(group)
    for group in figure_groups:
        out.extend(
            [
                f"- [{figure_group_label(group, language)}](#section-{anchor(group)})",
                "",
            ]
        )
    out.extend(
        [
            "## " + ("Figure-by-Figure Guide" if english else "Figure 逐圖導讀"),
            "",
            (
                ("The requested text contains no numbered Table reference. " if report_id == "base-admin-fw-logs" else "")
                + "The source uses Figure numbers for diagrams and field-layout tables. "
                "No source artwork is reproduced; compact field and keyword indexes "
                "come from the locally verified PDFs."
                if english
                else ("指定正文沒有引用任何編號 Table。" if report_id == "base-admin-fw-logs" else "")
                + "本範圍的規格以 Figure 編號同時涵蓋示意圖與欄位表；本文不重製原圖。"
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
        group = figure_group(figure)
        if group != active_group:
            active_group = group
            out.extend(
                [
                    f'<a id="section-{anchor(group)}"></a>',
                    "",
                    f"### {figure_group_label(group, language)}",
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


FIRMWARE_PARTS = [
    {
        "id": "mental-model",
        "zh": "PART 1 — 先建立 Mental Model：image、slot、domain",
        "en": "PART 1 — Mental Model: Images, Slots, and Domains",
        "intro_zh": "Firmware update 不是把檔案寫進裝置後立刻生效。Downloaded image、slot 內已保存的 image、目前執行中的 image，以及排定在下一次 reset 啟用的 image，是四個要分開追蹤的狀態。",
        "intro_en": "A firmware update is not an immediate file replacement. Track four distinct states: downloaded image data, an image stored in a slot, the currently executing image, and an image scheduled for activation at a later reset.",
        "claims": [
            "BASEFWLOG-MODEL-DOMAIN",
            "BASEFWLOG-CAP-FR",
            "BASEFWLOG-CAP-MDS-ULIST",
            "BASEFWLOG-CAP-FRMW",
            "BASEFWLOG-CAP-MTFA",
            "BASEFWLOG-CAP-FWUG",
            "BASEFWLOG-CAP-MPTFAWR",
        ],
        "inference_zh": "工程上應把 domain 當作 firmware 狀態的共享鍵。只記錄 PCI Function 或 controller ID，可能把同一組 shared slots 誤判成多套獨立 firmware。",
        "inference_en": "Use the domain as the firmware-state sharing key. Recording only a PCI Function or controller ID can incorrectly turn one shared slot set into several apparently independent firmware stores.",
    },
    {
        "id": "download",
        "zh": "PART 2 — 建立 Download Sequence：切片、對齊、失效條件",
        "en": "PART 2 — Build the Download Sequence: Portions, Alignment, Invalidation",
        "intro_zh": "Image 可以分段傳送，但 controller 看到的是 dword range，不是檔名或檔案 offset。每一段都要同時滿足 buffer、0's-based length、image-relative offset 與 FWUG。",
        "intro_en": "An image may be transferred in portions, but the controller sees dword ranges rather than a filename or byte-oriented file offset. Every portion must satisfy buffer, zero-based length, image-relative offset, and FWUG constraints together.",
        "claims": [
            "BASEFWLOG-FW-SEQUENCE",
            "BASEFWLOG-DOWNLOAD-RANGE",
            "BASEFWLOG-DOWNLOAD-FIELDS",
            "BASEFWLOG-FW-DISCARD",
        ],
        "inference_zh": "driver 應在送出 command 前用 byte interval 檢查 overlap，再轉成 NUMD／OFST；若先轉成 0's-based 欄位才檢查，最容易發生 off-by-one。",
        "inference_en": "A driver should detect overlap on byte intervals before converting to NUMD and OFST. Performing interval checks only after zero-based encoding makes off-by-one defects much more likely.",
    },
    {
        "id": "commit-activate",
        "zh": "PART 3 — Commit 與 Activation：CA 決定狀態轉移",
        "en": "PART 3 — Commit and Activation: CA Selects the State Transition",
        "intro_zh": "Firmware Commit 同時承擔驗證、slot placement 與 activation policy。最重要的判斷不是「command 成功了嗎」，而是成功後 image 位於哪個 slot、是否已 active、還欠哪一種 reset。",
        "intro_en": "Firmware Commit combines validation, slot placement, and activation policy. The key question is not merely whether the command succeeded, but which slot now holds the image, whether it is active, and which reset—if any—still remains.",
        "claims": [
            "BASEFWLOG-COMMIT-PURPOSE",
            "BASEFWLOG-COMMIT-CDW10",
            "BASEFWLOG-COMMIT-BOOT",
            "BASEFWLOG-COMMIT-MUD",
            "BASEFWLOG-COMMIT-STATUS",
            "BASEFWLOG-FW-RESET",
            "BASEFWLOG-FW-IMMEDIATE",
            "BASEFWLOG-FW-FAILURE",
            "BASEFWLOG-RESET-XREF",
            "BASEFWLOG-UUID-LIST",
            "BASEFWLOG-UUID-RESET",
            "BASEFWLOG-XREF-337",
        ],
        "inference_zh": "recovery code 應以完整 SCT／SC 分流，而不是只判斷 success／failure。回報需要 Conventional Reset 時，用 FLR 取代並不能滿足該狀態所指示的 activation 邊界。",
        "inference_en": "Recovery logic should branch on the complete SCT/SC rather than a success/failure boolean. When status requires Conventional Reset, substituting FLR does not satisfy the indicated activation boundary.",
    },
    {
        "id": "lid03",
        "zh": "PART 4 — 用 LID 03h 驗證：從 command 到 512-byte layout",
        "en": "PART 4 — Verify with LID 03h: From Command to the 512-Byte Layout",
        "intro_zh": "LID 03h 是 firmware workflow 的觀測面：AFI 回答 current／next active slot，FRS1-FRS7 回答各 slot 保存的 revision。它不替代 Firmware Commit completion，也不告訴 host 該用哪一種 reset。",
        "intro_en": "LID 03h is the observation surface for the firmware workflow. AFI reports current and next active slots, while FRS1-FRS7 report stored revisions. It does not replace Firmware Commit completion or choose the required reset for the host.",
        "claims": [
            "BASEFWLOG-LOG-COMMAND",
            "BASEFWLOG-LOG-LENGTH",
            "BASEFWLOG-LOG-RAE",
            "BASEFWLOG-LOG-OFFSET",
            "BASEFWLOG-LOG-SCOPE",
            "BASEFWLOG-LID03-DESCRIPTION",
            "BASEFWLOG-LID03-AFI",
            "BASEFWLOG-LID03-FRS",
        ],
        "inference_zh": "驗證時要同時比對 Identify.FR、LID 03h 的 CAFS 與對應 FRSx。只比 ASCII revision 可能在兩個 slots 恰好含相同字串時失去 slot 身分。",
        "inference_en": "Verification should compare Identify.FR, LID 03h CAFS, and the corresponding FRSx together. Comparing only the ASCII revision loses slot identity when two slots happen to contain the same string.",
    },
]


def firmware_mental_model_svg() -> str:
    return """<svg width="100%" height="240" viewBox="0 0 820 240" role="img" aria-labelledby="fw-model-title fw-model-desc">
<title id="fw-model-title">Firmware update mental model</title>
<desc id="fw-model-desc">Downloaded portions are committed to a shared firmware slot, selected for activation, and then observed through Identify FR and LID 03h.</desc>
<defs><marker id="fw-arrow" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="currentColor"/></marker></defs>
<rect x="20" y="70" width="150" height="70" fill="none" stroke="currentColor"/><text x="95" y="96" text-anchor="middle" fill="currentColor">Downloaded</text><text x="95" y="120" text-anchor="middle" fill="currentColor">image portions</text>
<rect x="230" y="40" width="170" height="130" fill="none" stroke="currentColor"/><text x="315" y="66" text-anchor="middle" fill="currentColor">Domain-shared slots</text><text x="315" y="95" text-anchor="middle" fill="currentColor">slot 1 · current</text><text x="315" y="120" text-anchor="middle" fill="currentColor">slot 2 · next</text><text x="315" y="145" text-anchor="middle" fill="currentColor">slot 3…7</text>
<rect x="470" y="70" width="140" height="70" fill="none" stroke="currentColor"/><text x="540" y="96" text-anchor="middle" fill="currentColor">Running</text><text x="540" y="120" text-anchor="middle" fill="currentColor">firmware</text>
<rect x="670" y="40" width="130" height="130" fill="none" stroke="currentColor"/><text x="735" y="70" text-anchor="middle" fill="currentColor">Observation</text><text x="735" y="100" text-anchor="middle" fill="currentColor">Identify.FR</text><text x="735" y="127" text-anchor="middle" fill="currentColor">LID 03h AFI</text><text x="735" y="151" text-anchor="middle" fill="currentColor">FRS1…FRS7</text>
<line x1="170" y1="105" x2="228" y2="105" stroke="currentColor" marker-end="url(#fw-arrow)"/><text x="199" y="91" text-anchor="middle" fill="currentColor">Commit</text>
<line x1="400" y1="105" x2="468" y2="105" stroke="currentColor" marker-end="url(#fw-arrow)"/><text x="434" y="91" text-anchor="middle" fill="currentColor">activate</text>
<line x1="610" y1="105" x2="668" y2="105" stroke="currentColor" marker-end="url(#fw-arrow)"/>
<path d="M315,170 C315,220 540,220 540,142" fill="none" stroke="currentColor" marker-end="url(#fw-arrow)"/><text x="425" y="218" text-anchor="middle" fill="currentColor">immediate or reset boundary</text>
</svg>"""


def firmware_afi_svg() -> str:
    return """<svg width="100%" height="170" viewBox="0 0 820 170" role="img" aria-labelledby="afi-title afi-desc">
<title id="afi-title">AFI and Firmware Slot Information layout</title>
<desc id="afi-desc">AFI byte zero contains NAFS in bits six through four and CAFS in bits two through zero, followed by reserved bytes and seven eight-byte revision fields.</desc>
<text x="20" y="28" fill="currentColor">AFI byte 0</text>
<rect x="20" y="40" width="80" height="38" fill="none" stroke="currentColor"/><rect x="100" y="40" width="240" height="38" fill="none" stroke="currentColor"/><rect x="340" y="40" width="80" height="38" fill="none" stroke="currentColor"/><rect x="420" y="40" width="240" height="38" fill="none" stroke="currentColor"/>
<text x="60" y="64" text-anchor="middle" fill="currentColor">R</text><text x="220" y="64" text-anchor="middle" fill="currentColor">NAFS [6:4]</text><text x="380" y="64" text-anchor="middle" fill="currentColor">R</text><text x="540" y="64" text-anchor="middle" fill="currentColor">CAFS [2:0]</text>
<text x="20" y="108" fill="currentColor">512-byte log page</text>
<rect x="20" y="120" width="70" height="34" fill="none" stroke="currentColor"/><rect x="90" y="120" width="90" height="34" fill="none" stroke="currentColor"/><rect x="180" y="120" width="390" height="34" fill="none" stroke="currentColor"/><rect x="570" y="120" width="230" height="34" fill="none" stroke="currentColor"/>
<text x="55" y="142" text-anchor="middle" fill="currentColor">AFI</text><text x="135" y="142" text-anchor="middle" fill="currentColor">R 1:7</text><text x="375" y="142" text-anchor="middle" fill="currentColor">FRS1…FRS7 · bytes 8:63</text><text x="685" y="142" text-anchor="middle" fill="currentColor">Reserved 64:511</text>
</svg>"""


def firmware_claim_order(claims: list[dict]) -> list[dict]:
    by_id = {item["id"]: item for item in claims if item["figure"] is None}
    return [by_id[claim_id] for part in FIRMWARE_PARTS for claim_id in part["claims"]]


def firmware_figure_appendix_html(claims: list[dict], figures: list[dict]) -> list[str]:
    figure_claims = {
        int(item["figure"]): item for item in claims if item["figure"] is not None
    }
    out = [
        '<section id="appendix"><h2>Appendix A — Supporting Figure／Field Reference</h2>',
        "<p id=\"figure-index\"><strong>[解釋]</strong> 下列 Figure 是主流程的可追溯證據，不是文章章節順序。"
        "<code>referenced_dependency</code> 只摘取理解所需欄位；Figure 209 只發布 LID 03h row。</p>",
    ]
    for figure in figures:
        item = figure_claims[int(figure["number"])]
        details = figure_explanation(figure, "zh")
        role = "最小相依切片" if figure.get("role") == "referenced_dependency" else "主範圍證據"
        out.extend(
            [
                "<details><summary><strong>Figure "
                + str(figure["number"])
                + ": "
                + html.escape(figure["title"])
                + "</strong> — "
                + role
                + "</summary>",
                f'<!-- figure-table:{figure["id"]} -->',
                f'<p><strong>[SPEC]</strong> <span data-claim-id="{item["id"]}">{html.escape(item["zh_tw"])}</span></p>',
                "<p><strong>[解釋]</strong> " + html.escape(details["purpose"] + " " + details["reading"]) + "</p>",
                "<p><strong>來源欄位索引：</strong> " + html.escape(details["item_text"]) + "</p>",
                "<p><small>" + html.escape(item["citation_zh_tw"]) + "</small></p>",
                "</details>",
            ]
        )
    out.append("</section>")
    return out


def render_firmware_html(
    report: dict, claims: list[dict], figures: list[dict], tutorial: bool
) -> str:
    label = "新手教學版" if tutorial else "詳細 Spec 版"
    claims_by_id = {item["id"]: item for item in claims if item["figure"] is None}
    toc = "".join(
        f'<li><a href="#{part["id"]}">{html.escape(part["zh"])}</a></li>'
        for part in FIRMWARE_PARTS
    )
    parts = [
        "<!doctype html>",
        '<html lang="zh-Hant-TW">',
        "<head>",
        '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        f"<title>{html.escape(report['title_zh'])}｜{label}</title>",
        "</head>",
        "<body>",
        '<header id="top">',
        f"<h1>{html.escape(report['title_zh'])}</h1>",
        f"<p><strong>{label}</strong>｜從 Firmware Image Download 到 LID 03h 驗證的工程教學</p>",
        "<p>讀者前提：已理解 NVMe Admin Queue、SQE／CQE、Controller Level Reset 與 Identify 基礎。</p>",
        "</header>",
        '<nav aria-label="目錄"><details open><summary><strong>Contents／章節導覽</strong></summary><ol>',
        '<li><a href="#scope">範圍、來源與閱讀語意</a></li>',
        toc,
        '<li><a href="#example">End-to-End Example</a></li>',
        '<li><a href="#debug">Debug Decision Flow</a></li>',
        '<li><a href="#appendix">Appendix A — Supporting Figure／Field Reference</a></li>',
        "</ol></details></nav>",
        "<main>",
        '<section id="scope"><h2>範圍、來源與閱讀語意</h2>',
        f"<p><strong>納入：</strong>{html.escape(report['range'])}。</p>",
        "<p><strong>明確不納入：</strong>其他 LID、未核准的傳輸專屬內容、NVM Command Set 1.3，以及 Boot Partition 的完整功能流程。BPID 與 CA=110b／111b 只作 §5.2.9／§5.2.10 cross-reference。</p>",
        "<table><thead><tr><th>標記</th><th>用途</th><th>能否視為 requirement</th></tr></thead><tbody>",
        "<tr><td>[SPEC]</td><td>規格明文的精確轉述，保留 shall／may／should</td><td>依原 keyword</td></tr>",
        "<tr><td>[解釋]</td><td>把多個欄位連成可理解的機制</td><td>否</td></tr>",
        "<tr><td>[推論]</td><td>依 Spec 導出的工程實作含意</td><td>否</td></tr>",
        "<tr><td>[說明性範例]</td><td>協助計算與 Debug 的具體數值</td><td>否</td></tr>",
        "</tbody></table>",
        "<p><strong>規範強度：</strong><code>shall／shall not</code> 是強制要求；<code>should／should not</code> 是有偏好的建議；<code>may</code> 表示允許選擇；<code>reserved</code> 不得自行賦予意義。</p>",
        "<p><strong>來源：</strong>NVM Express Base Specification, Revision 2.4；NVMe over PCIe Transport Specification, Revision 1.4（僅 §3.3 reset 名稱）。查證日期：2026-09-01。</p>",
        "</section>",
        '<section aria-labelledby="model-picture"><h2 id="model-picture">一張圖先看完整故事</h2>',
        firmware_mental_model_svg(),
        "<p><strong>[解釋]</strong> Download 只建立暫存 portions；Commit 才把 image 驗證並放進 slot。Activation 再把某個 slot 的 image 變成正在執行的 firmware。最後以 Identify.FR 與 LID 03h 觀察結果。</p>",
        "</section>",
    ]
    for part in FIRMWARE_PARTS:
        parts.extend(
            [
                f'<section id="{part["id"]}"><h2>{html.escape(part["zh"])}</h2>',
                "<p><strong>[解釋]</strong> " + html.escape(part["intro_zh"]) + "</p>",
            ]
        )
        if part["id"] == "mental-model":
            parts.extend(
                [
                    "<table><thead><tr><th>物件／欄位</th><th>它回答什麼</th><th>Debug 時何時讀</th></tr></thead><tbody>",
                    "<tr><td>FRMW／FWUG／MTFA／MPTFAWR</td><td>能做什麼、限制與時間</td><td>任何 download 前</td></tr>",
                    "<tr><td>Downloaded portions</td><td>尚未 commit 的 image ranges</td><td>download／overlap 錯誤</td></tr>",
                    "<tr><td>Firmware slot</td><td>已保存但不一定 active 的 image</td><td>commit 與 LID 03h</td></tr>",
                    "<tr><td>Identify.FR＋AFI／FRSx</td><td>目前執行者與 slot 狀態</td><td>activation 後驗證</td></tr>",
                    "</tbody></table>",
                ]
            )
        if part["id"] == "commit-activate":
            parts.extend(
                [
                    "<table><thead><tr><th>CA</th><th>對 slot 的動作</th><th>activation 時點</th><th>LID 03h 觀察重點</th></tr></thead><tbody>",
                    "<tr><td>000b</td><td>放置 downloaded image</td><td>不 activation</td><td>FRSx 可變，CAFS 不因此改變</td></tr>",
                    "<tr><td>001b</td><td>放置 downloaded image</td><td>下次合適 CLR</td><td>reset 前看 NAFS；後看 CAFS</td></tr>",
                    "<tr><td>010b</td><td>使用既有 slot</td><td>下次合適 CLR</td><td>reset 前看 NAFS；後看 CAFS</td></tr>",
                    "<tr><td>011b</td><td>放置或使用既有 slot</td><td>立即；command 等到結果</td><td>完成後重新讀 CAFS／FRSx</td></tr>",
                    "</tbody></table>",
                ]
            )
        if part["id"] == "lid03":
            parts.extend([firmware_afi_svg()])
        for item_id in part["claims"]:
            item = claims_by_id[item_id]
            parts.extend(
                [
                    f"<article><h3>{html.escape(item['heading_zh_tw'])}</h3>",
                    f'<p><strong>[SPEC]</strong> <span data-claim-id="{item["id"]}">{html.escape(item["zh_tw"])}</span></p>',
                    f"<p><small>{html.escape(item['citation_zh_tw'])}</small></p>",
                    "</article>",
                ]
            )
        parts.extend(
            [
                "<p><strong>[推論]</strong> " + html.escape(part["inference_zh"]) + "</p>",
                '<p><a href="#top">回到目錄</a></p></section>',
            ]
        )
    parts.extend(
        [
            '<section id="example"><h2>End-to-End Example：12 KiB image，slot 2，下次 CLR 啟用</h2>',
            "<p><strong>[說明性範例]</strong> 假設 Identify 回報 <code>NOFS=3</code>、<code>FFSRO=1</code>、<code>FWUG=1h</code>，目前 LID 03h 為 <code>CAFS=1</code>。選 slot 2 可避開 read-only slot 1；FWUG=1h 代表 4 KiB granularity／alignment。</p>",
            "<ol><li>將 12 KiB 切成三個 4 KiB portions。每段 4096 bytes=1024 dwords，所以 <code>NUMD=1024-1=1023=000003FFh</code>。</li><li>三段的 <code>OFST</code> 依序為 <code>00000000h</code>、<code>00000400h</code>、<code>00000800h</code>；byte offsets 分別是 0、4096、8192。</li><li>送出 Firmware Commit：<code>CA=001b</code>、<code>FS=010b</code>，所以 <code>CDW10=0000000Ah</code>。成功只表示已排定下次合適 CLR，不表示 slot 2 已在執行。</li><li>reset 前讀完整 LID 03h：512 bytes=128 dwords，<code>NUMD=127</code>，<code>CDW10=007F0003h</code>。若 AFI=<code>21h</code>，則 <code>NAFS=2</code>、<code>CAFS=1</code>。</li><li>執行 Firmware Commit status 所要求且能觸發 activation 的 reset，重新初始化 controller／I/O queues，再讀 Identify.FR 與 LID 03h；確認 <code>CAFS=2</code> 且 FRS2 是預期 revision。</li></ol>",
            "<p><strong>[推論]</strong> 若 reset 後 FRS2 正確但 CAFS 仍為 1，代表 image 已在 slot 2，卻沒有完成預期的 activation；優先檢查 CA、completion status 與實際 reset 類型。</p>",
            '<p><a href="#top">回到目錄</a></p></section>',
            '<section id="debug"><h2>Debug Decision Flow</h2>',
            "<table><thead><tr><th>觀察點</th><th>先檢查</th><th>常見誤解</th><th>下一步</th></tr></thead><tbody>",
            "<tr><td>Download 回 Invalid Field</td><td>(NUMD+1)×4、OFST×4、FWUG</td><td>把 NUMD 當實際 dword 數</td><td>以 byte interval 重算 alignment</td></tr>",
            "<tr><td>Commit 回 Invalid Firmware Slot</td><td>NOFS、FFSRO、FS</td><td>slot 1 永遠可寫</td><td>改用支援且可寫的 slot</td></tr>",
            "<tr><td>Commit 要求 reset</td><td>完整 SCT／SC</td><td>所有 reset 等價</td><td>依 status 與 PCIe §3.3 選 reset</td></tr>",
            "<tr><td>LID 03h 看似沒更新</td><td>MDS／DID、處理 command 的 controller、AFI</td><td>每個 controller 有獨立 slots</td><td>回到同一 domain 核對</td></tr>",
            "<tr><td>FRSx 全零</td><td>NOFS、slot 有效性、buffer offset</td><td>零值是空字串 revision</td><td>視為 unsupported／no valid revision</td></tr>",
            "<tr><td>立即 activation timeout</td><td>MTFA、MPTFAWR、completion status</td><td>CA=011b 是背景工作</td><td>等待 command 結果並照 status recovery</td></tr>",
            "</tbody></table>",
            "<p><strong>最小紀錄集合：</strong>controller／domain identity、FRMW、FWUG、MTFA、MPTFAWR、每筆 NUMD／OFST、Commit CDW10、完整 CQE status／MUD、reset 類型、activation 前後的 512-byte LID 03h。</p>",
            '<p><a href="#top">回到目錄</a></p></section>',
        ]
    )
    if not tutorial:
        parts.extend(
            [
                '<section id="field-reference"><h2>Detailed Reference — 重要欄位速查</h2>',
                "<table><thead><tr><th>結構</th><th>欄位</th><th>encoding／unit</th><th>嚴謹注意事項</th></tr></thead><tbody>",
                "<tr><td>Firmware Image Download CDW10</td><td>NUMD[31:0]</td><td>0's-based dwords</td><td>實際 bytes=(NUMD+1)×4</td></tr>",
                "<tr><td>Firmware Image Download CDW11</td><td>OFST[31:0]</td><td>dwords</td><td>image 起點 portion shall 為 0h</td></tr>",
                "<tr><td>Firmware Commit CDW10</td><td>BPID／CA／FS</td><td>bit 31／[5:3]／[2:0]</td><td>100b-101b reserved</td></tr>",
                "<tr><td>Get Log Page CDW10</td><td>NUMDL／RAE／LSP／LID</td><td>[31:16]／15／[14:8]／[7:0]</td><td>LID 03h full read=007F0003h</td></tr>",
                "<tr><td>LID 03h byte 0</td><td>NAFS／CAFS</td><td>[6:4]／[2:0]</td><td>NAFS=0 只表示未指出 next slot</td></tr>",
                "<tr><td>LID 03h bytes 8:63</td><td>FRS1-FRS7</td><td>各 8-byte ASCII</td><td>invalid／unsupported slot shall 為 0h</td></tr>",
                "</tbody></table></section>",
            ]
        )
    parts.extend(firmware_figure_appendix_html(claims, figures))
    parts.extend(
        [
            '<section id="sources"><h2>來源與限制</h2>',
            "<p>主要來源：NVM Express Base Specification, Revision 2.4。Reset 名稱的最小外部依賴：NVM Express NVMe over PCIe Transport Specification, Revision 1.4, §3.3, 文件／PDF 頁 11。</p>",
            "<p>目前未納入額外 Errata、ECN、Technical Proposal、controller vendor 文件或 PCI Express Base Specification 原文。若 revision 或核准範圍改變，應用 claim ID 重新核對。</p>",
            '<p><a href="#top">回到目錄</a></p></section>',
            "</main>",
            "</body>",
            "</html>",
            "",
        ]
    )
    return "\n".join(parts)


def firmware_figure_appendix_markdown(
    claims: list[dict], figures: list[dict], language: str
) -> list[str]:
    english = language == "en"
    figure_claims = {
        int(item["figure"]): item for item in claims if item["figure"] is not None
    }
    out = [
        "## Appendix A — Supporting Figure / Field Reference",
        "",
        (
            "Figures are traceable evidence for the workflow, not the article outline. Dependency entries expose only the required slice; Figure 209 is limited to the LID 03h row."
            if english
            else "Figure 是主流程的可追溯證據，不是文章骨架。dependency entries 只取理解所需切片；Figure 209 只保留 LID 03h row。"
        ),
        "",
    ]
    for figure in figures:
        item = figure_claims[int(figure["number"])]
        details = figure_explanation(figure, language)
        statement = item["en"] if english else item["zh_tw"]
        citation = item["citation_en"] if english else item["citation_zh_tw"]
        role = (
            "minimum dependency slice"
            if english and figure.get("role") == "referenced_dependency"
            else "最小相依切片"
            if figure.get("role") == "referenced_dependency"
            else "main-scope evidence"
            if english
            else "主範圍證據"
        )
        out.extend(
            [
                '<details markdown="1">',
                f"<summary><strong>Figure {figure['number']}: {html.escape(figure['title'])}</strong> — {role}</summary>",
                "",
                f"<!-- claim:{item['id']} figure-table:{figure['id']} -->",
                "",
                "**[SPEC]** " + statement,
                "",
                ("**[Explanation]** " if english else "**[解釋]** ")
                + details["purpose"]
                + " "
                + details["reading"],
                "",
                ("Source field index: " if english else "來源欄位索引：")
                + details["item_text"],
                "",
                "> " + citation,
                "",
                "</details>",
                "",
            ]
        )
    return out


def render_firmware_markdown(
    report: dict, claims: list[dict], figures: list[dict], language: str
) -> str:
    english = language == "en"
    title = report["title_en"] if english else report["title_zh"]
    description = (
        "A source-located engineering tutorial from firmware download through LID 03h verification."
        if english
        else "從 firmware download 到 LID 03h 驗證、可供 GitHub Pages 與 PPT 使用的工程教學。"
    )
    by_id = {item["id"]: item for item in claims if item["figure"] is None}
    out = [
        frontmatter("base-admin-fw-logs", title, description, language),
        f"# {title}",
        "",
        (
            "This tutorial builds an end-to-end engineering model: capability readout, image download, commit and activation, reset boundaries, and verification with Firmware Slot Information (LID 03h)."
            if english
            else "本教學建立完整工程模型：能力探測、image download、commit／activation、reset 邊界，以及用 Firmware Slot Information（LID 03h）驗證結果。"
        ),
        "",
        "## " + ("Scope and source semantics" if english else "範圍與來源語意"),
        "",
        ("Scope: " + report["range_en"] + "." if english else "範圍：" + report["range"] + "。"),
        "",
        SOURCES["NVME-BASE-2.4"]["marker"],
        "",
        SOURCES["NVME-PCIE-TRANSPORT-1.4"]["marker"]
        + (" — §3.3 reset terminology only" if english else " — 僅 §3.3 reset 名稱"),
        "",
        (
            "Excluded: every other LID, unapproved transport-specific material, NVM Command Set 1.3, and the full Boot Partition feature flow. BPID and CA=110b/111b remain only as cross-references."
            if english
            else "排除：其餘 LID、未核准的傳輸專屬內容、NVM Command Set 1.3、Boot Partition 完整功能流程；BPID 與 CA=110b／111b 只保留 cross-reference。"
        ),
        "",
        (
            "`shall` is mandatory, `should` is a preferred recommendation, `may` permits a choice, and `reserved` is not assigned an invented meaning. `[SPEC]` is a source-faithful paraphrase; `[Explanation]`, `[Inference]`, and `[Informative example]` add no requirement."
            if english
            else "`shall` 是強制要求，`should` 是有偏好的建議，`may` 表示允許選擇，`reserved` 不自行賦義。`[SPEC]` 是忠於來源的轉述；`[解釋]`、`[推論]`、`[說明性範例]` 不新增 requirement。"
        ),
        "",
        "## Mental Model",
        "",
        "```text",
        "Downloaded portions -> committed slot -> current / next active image -> Identify.FR + LID 03h",
        "```",
        "",
    ]
    for part in FIRMWARE_PARTS:
        out.extend(
            [
                f"## {part['en'] if english else part['zh']}",
                "",
                ("**[Explanation]** " if english else "**[解釋]** ")
                + (part["intro_en"] if english else part["intro_zh"]),
                "",
            ]
        )
        for item_id in part["claims"]:
            item = by_id[item_id]
            out.extend(
                [
                    f"### {item['heading_en'] if english else item['heading_zh_tw']}",
                    "",
                    f"<!-- claim:{item['id']} -->",
                    "",
                    "**[SPEC]** " + (item["en"] if english else item["zh_tw"]),
                    "",
                    "> " + (item["citation_en"] if english else item["citation_zh_tw"]),
                    "",
                ]
            )
        out.extend(
            [
                ("**[Inference]** " if english else "**[推論]** ")
                + (part["inference_en"] if english else part["inference_zh"]),
                "",
            ]
        )
    out.extend(
        [
            "## " + ("End-to-End Example" if english else "End-to-End Example：12 KiB image，slot 2，下次 CLR 啟用"),
            "",
            (
                "**[Informative example]** Assume NOFS=3, FFSRO=1, FWUG=1h, and CAFS=1. Use writable slot 2. Split 12 KiB into three 4 KiB portions. Each portion is 1024 dwords, so NUMD=1023=000003FFh; OFST values are 00000000h, 00000400h, and 00000800h. Commit with CA=001b and FS=010b, giving CDW10=0000000Ah. Before reset, read all 512 bytes of LID 03h with NUMD=127 and CDW10=007F0003h. AFI=21h decodes to NAFS=2 and CAFS=1. Perform the required reset, reinitialize, then verify CAFS=2 together with FRS2 and Identify.FR."
                if english
                else "**[說明性範例]** 假設 NOFS=3、FFSRO=1、FWUG=1h、CAFS=1，選可寫的 slot 2。12 KiB 切成三個 4 KiB portions；每段 1024 dwords，所以 NUMD=1023=000003FFh，OFST 依序是 00000000h、00000400h、00000800h。以 CA=001b、FS=010b commit，CDW10=0000000Ah。Reset 前完整讀 512-byte LID 03h：NUMD=127、CDW10=007F0003h；AFI=21h 解成 NAFS=2、CAFS=1。執行要求的 reset、重新初始化，再一起驗證 CAFS=2、FRS2 與 Identify.FR。"
            ),
            "",
            "## " + ("Debug Decision Flow" if english else "Debug Decision Flow"),
            "",
            (
                "| Symptom | First evidence | Likely mistake | Next action |\n|---|---|---|---|\n| Download Invalid Field | NUMD, OFST, FWUG | NUMD treated as a direct count | Recompute byte intervals |\n| Invalid Firmware Slot | NOFS, FFSRO, FS | Slot 1 assumed writable | Select a supported writable slot |\n| Reset-required status | Full SCT/SC | All resets treated as equal | Follow status and PCIe §3.3 |\n| LID 03h unchanged | MDS/DID, controller, AFI | Slots assumed per controller | Verify within the same domain |\n| FRSx is zero | NOFS, slot validity, buffer offset | Zero treated as an empty revision string | Treat as unsupported/no valid revision |"
                if english
                else "| 症狀 | 第一證據 | 常見錯誤 | 下一步 |\n|---|---|---|---|\n| Download Invalid Field | NUMD、OFST、FWUG | 把 NUMD 當直接 count | 重算 byte intervals |\n| Invalid Firmware Slot | NOFS、FFSRO、FS | 假設 slot 1 可寫 | 改用支援且可寫 slot |\n| reset-required status | 完整 SCT／SC | 把所有 reset 視為相同 | 依 status 與 PCIe §3.3 |\n| LID 03h 未更新 | MDS／DID、controller、AFI | 假設 slots 各 controller 獨立 | 在同一 domain 核對 |\n| FRSx 為零 | NOFS、slot validity、buffer offset | 當成空字串 revision | 視為 unsupported／no valid revision |"
            ),
            "",
        ]
    )
    out.extend(firmware_figure_appendix_markdown(claims, figures, language))
    out.extend(
        [
            "## " + ("Limits" if english else "限制"),
            "",
            (
                "Verification date: 2026-09-01. No additional errata, ECNs, Technical Proposals, controller-vendor documents, or PCI Express Base Specification source text are included. Re-check affected claim IDs when the approved source set changes."
                if english
                else "查證日期：2026-09-01。未納入其他 Errata、ECN、Technical Proposal、controller vendor 文件或 PCI Express Base Specification 原文。核准來源集合改變時，應依 claim ID 重查。"
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
    scope_doc = json.loads((CONTROL / "scope.json").read_text(encoding="utf-8"))
    figure_allowlists = {
        item["id"]: set(item.get("included_figure_ids", []))
        for item in scope_doc["reports"]
    }
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
            make_claim(report_id, report, item) for item in report["claims"]
        ]
        report_claims.extend(
            make_figure_claim(report_id, report, item) for item in figures
        )
        all_claims.extend(report_claims)

        ids = artifact_ids(report_id)
        if report_id == "base-admin-fw-logs":
            output_text = {
                ids[0]: render_firmware_html(report, report_claims, figures, True),
                ids[1]: render_firmware_html(report, report_claims, figures, False),
                ids[2]: render_firmware_markdown(
                    report, report_claims, figures, "zh"
                ),
                ids[3]: render_firmware_markdown(
                    report, report_claims, figures, "en"
                ),
            }
        else:
            output_text = {
                ids[0]: render_html(
                    report_id, report, report_claims, figures, True
                ),
                ids[1]: render_html(
                    report_id, report, report_claims, figures, False
                ),
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
        f"Built {len(contract['artifacts'])} artifacts, {len(all_claims)} claims, "
        f"using {len(register_entries)} tracked Figure records"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
