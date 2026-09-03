"""Context-specific definitions for the Boot/Telemetry/Sanitize report."""

def b(zh, en):
    return {"zh": zh, "en": en}


TERMS = {
    "BPID": b("Boot Partition Identifier；選取 0 或 1，與目前 active partition 分開。", "Boot Partition Identifier; selects 0 or 1 independently of the active partition."),
    "ABPID": b("Active Boot Partition ID；指出目前選為啟動映像的 partition。", "Active Boot Partition ID; identifies the partition selected as the boot image."),
    "BPSZ": b("Boot Partition Size；每單位 128 KiB。", "Boot Partition Size; each unit is 128 KiB."),
    "BRS": b("Boot Read Status；00b 未請求、01b 進行中、10b 成功、11b 錯誤。", "Boot Read Status: 00b no request, 01b in progress, 10b success, 11b error."),
    "BPCAP": b("Boot Partition Capabilities；辨識 Set Features 與 RPMB 保護機制的支援組合。", "Boot Partition Capabilities; identifies the supported combination of Set Features and RPMB protection."),
    "BP0WPS": b("Boot Partition 0 Write Protection State；FID 85h 的 bits 2:0。", "Boot Partition 0 Write Protection State; bits 2:0 of FID 85h."),
    "BP1WPS": b("Boot Partition 1 Write Protection State；FID 85h 的 bits 5:3。", "Boot Partition 1 Write Protection State; bits 5:3 of FID 85h."),
    "BPRSZ": b("Boot Partition Read Size；以 4 KiB 為單位，不能套用 BPSZ 的單位。", "Boot Partition Read Size; uses 4 KiB units, not BPSZ units."),
    "BPROF": b("Boot Partition Read Offset；BPRSEL bits 29:10，以 4 KiB 為單位；bit 30 保留。", "Boot Partition Read Offset; BPRSEL bits 29:10 in 4 KiB units; bit 30 is reserved."),
    "BMBBA": b("Boot Memory Buffer Base Address；BPMBL bits 63:12，低 12 bits 保留。", "Boot Memory Buffer Base Address; BPMBL bits 63:12, with the low 12 bits reserved."),
    "CTHID": b("Create Telemetry Host-Initiated Data；07h 的 capture 要求，後續分段讀同一快照要清為 0。", "Create Telemetry Host-Initiated Data; the 07h capture request, cleared for subsequent reads of that snapshot."),
    "MCDA": b("Maximum Created Data Area；支援且要求 capture 時選擇建立的最大 area。", "Maximum Created Data Area; selects the largest area to create when supported and capture is requested."),
    "MCDAS": b("Maximum Created Data Area Supported；07h 的 LID Specific Parameter bit 0，宣告 MCDA 支援。", "Maximum Created Data Area Supported; bit 0 of the 07h LID Specific Parameter, advertising MCDA support."),
    "ETDAS": b("Extended Telemetry Data Area 4 Supported；Host Behavior Support 中由 host 宣告 Area 4 支援。", "Extended Telemetry Data Area 4 Supported; the host's Area 4 declaration in Host Behavior Support."),
    "TCDA": b("Telemetry Controller-Initiated Data Available；2.4 中表示自上次 RAE=0 acknowledgement 後是否有更新。", "Telemetry Controller-Initiated Data Available; in 2.4, indicates an update since the last RAE=0 acknowledgement."),
    "TCDGN": b("Telemetry Controller-Initiated Data Generation Number；8-bit generation，完成更新最後才遞增。", "Telemetry Controller-Initiated Data Generation Number; an eight-bit generation incremented at the end of an update."),
    "THDGN": b("Telemetry Host-Initiated Data Generation Number；用來比對分段讀取是否仍屬同一快照。", "Telemetry Host-Initiated Data Generation Number; checks whether chunks still belong to one snapshot."),
    "RAE": b("Retain Asynchronous Event；Telemetry 收集中用 1 保留通知狀態，完成後用 0 acknowledgement。", "Retain Asynchronous Event; use one during Telemetry collection and zero to acknowledge completion."),
    "SANACT": b("Sanitize Action；決定實際方法、退出 Failure 或退出 Media Verification。", "Sanitize Action; selects the method, Exit Failure Mode, or Exit Media Verification."),
    "AUSE": b("Allow Unrestricted Sanitize Exit；選擇失敗時是否允許不經成功重試就退出 Failure。", "Allow Unrestricted Sanitize Exit; selects whether failure can be exited without a successful retry."),
    "NDAS": b("No-Deallocate After Sanitize；命令要求，需與 SANICAP.NDI 及 NODRM 一起解讀。", "No-Deallocate After Sanitize; a command request interpreted with SANICAP.NDI and NODRM."),
    "NDI": b("No-Deallocate Inhibited；宣告 controller 是否抑制 NDAS 的要求。", "No-Deallocate Inhibited; advertises whether the controller inhibits NDAS."),
    "NODRM": b("No-Deallocate Response Mode；FID 17h bit 0，選擇受抑制 NDAS 的 error 或 warning 回應。", "No-Deallocate Response Mode; FID 17h bit zero selects error or warning for inhibited NDAS."),
    "EMVS": b("Enter Media Verification State；成功 processing 後要求進入驗證，受方法與 capability 限制。", "Enter Media Verification State; requests verification after successful processing, subject to method and capability restrictions."),
    "PREQ": b("Purge Request；與 SPRRS 一起判定 purge 要求與回報；兩種 Sanitize 命令的 bit 位置不同。", "Purge Request; interpreted with SPRRS for purge request/reporting; its bit position differs between the Sanitize commands."),
    "SPROG": b("Sanitize Progress；raw/65536，僅表示目前量測階段的進度。", "Sanitize Progress; raw/65536, indicating progress only for the currently measured phase."),
    "SOS": b("Sanitize Operation Status；SSTAT bits 2:0，與目前 SANS state 分開判讀。", "Sanitize Operation Status; SSTAT bits 2:0, interpreted separately from the current SANS state."),
    "MVCNCLD": b("Media Verification Canceled；記錄要求的驗證被取消，會影響 processing 後的轉移。", "Media Verification Canceled; records canceled verification and affects the transition after processing."),
    "PRCHK": b("Protection Information Check；三個 bits 分別要求 guard、application tag、reference tag 檢查；驗證讀取設 000b。", "Protection Information Check; three bits request guard, application-tag, and reference-tag checking; verification reads use 000b."),
    "STC": b("Storage Tag Check；本報告指 NVM Read 的 storage tag 檢查，驗證讀取設 0。", "Storage Tag Check; here it selects storage-tag checking for NVM Reads and is zero for verification reads."),
}


def definition(term, report_id, language, fallback):
    if report_id == "base-boot-telemetry-sanitize" and term in TERMS:
        return TERMS[term][language]
    if report_id == "base-self-test-namespace-management" and term == "SEL":
        return b("Select；Namespace Management 的 create/delete/restore selector，與 Get Features 的 SEL 不同。", "Select; the Namespace Management create/delete/restore selector, distinct from Get Features SEL.")[language]
    return fallback(term, language)
