"""Specific teaching slices, not source-table reproductions."""

def f(keys, zh, en, claim):
    return dict(key_items=keys.split(","), zh=zh, en=en, claim=claim)


BASE_FIGURES = {
    36: f("CAP.BPS", "先查 BPS 再使用 Boot properties；支援 Boot 不代表已啟用 controller。", "Check BPS before using Boot properties; Boot support does not imply an enabled controller.", "BOOT-MODEL"),
    49: f("ABPID,BPSZ,BRS", "ABPID 指 active partition，BPSZ 使用 128 KiB，BRS 依 00b/01b/10b/11b 區分未請求、傳輸中、成功與錯誤。", "ABPID identifies the active partition, BPSZ uses 128 KiB units, and BRS distinguishes no request/in progress/success/error with 00b/01b/10b/11b.", "BOOT-READ"),
    50: f("BPID,BPRSZ,BPROF", "BPRSEL bit 31 是 BPID、bit 30 保留，[29:10] 是以 4 KiB 計的 BPROF，[9:0] 是以 4 KiB 計的 BPRSZ；寫入會觸發讀取。", "BPRSEL bit 31 is BPID, bit 30 is reserved, [29:10] is BPROF in 4 KiB units, and [9:0] is BPRSZ in 4 KiB units; writing initiates a read.", "BOOT-READ"),
    51: f("BMBBA", "BPMBL[63:12] 提供 Boot Memory Buffer 基底位址，低 12 bits 保留；先確認 host buffer 的連續性與對齊。", "BPMBL[63:12] provides the Boot Memory Buffer base address; the low 12 bits are reserved. Establish a contiguous, aligned host buffer first.", "BOOT-READ"),
    144: f("Get Log Page,Boot Partition,Sanitize Status", "比較 Sanitize 欄的命令白名單及各命令限制；Boot log 可讀，Telemetry 07h/08h 未被列入。只使用通用與 memory-based 命令列。", "Read the Sanitize column's command allowlist and per-command restrictions. Boot is readable; Telemetry 07h/08h is not listed. Only common and memory-based command rows are used.", "SAN-RESTRICT"),
    145: f("Set Features,Namespace Management,Firmware Commit", "這張表約束所有 controllers：例如拒絕刪除正被 sanitize 的 namespace，並限制 firmware update；先套用 target 關係再判斷 status。", "This table applies to all controllers: for example, deletion of a namespace being sanitized and firmware updates are restricted. Establish the target relationship before choosing a status.", "SAN-RESTRICT"),
    146: f("Attached Namespace,Admin command restrictions", "這張表補充有 attached sanitizing namespace 的 controllers；不能把所有 controller 與只有 attached controller 的限制混為一談。", "This table adds restrictions for controllers with an attached namespace being sanitized. Do not conflate all-controller restrictions with attached-controller restrictions.", "SAN-RESTRICT"),
    151: f("LID,AEI,AET", "CQE DW0[23:16] 是 LID、[15:8] 是 AEI、[2:0] 是 AET；Sanitize 用 LID 81h/AET 110b，Telemetry 使用 Notice 類型。", "CQE DW0[23:16] is LID, [15:8] AEI, and [2:0] AET. Sanitize uses LID 81h/AET 110b; Telemetry uses the Notice type.", "SAN-EVENT"),
    152: f("EVNTSP", "AER DW1 是 event-specific parameter；Sanitize 以 0h 指 subsystem，以 NSID 指 namespace，不能把它讀成進度。", "AER DW1 is the event-specific parameter. Sanitize uses zero for a subsystem and NSID for a namespace; it is not progress.", "SAN-EVENT"),
    155: f("Telemetry Log Changed", "只取 Telemetry Log Changed Notice：用事件定位 08h，再讀 log；事件不包含診斷 payload。", "Use the Telemetry Log Changed Notice slice: locate 08h from the event and read the log; the event does not contain the diagnostic payload.", "TEL-EVENT"),
    156: f("Sanitize Operation Completed,Unexpected Deallocation,Entered Media Verification", "01h/02h/03h 三種 Sanitize AEI 必須與 SOS/SANS 一起看；Entered Media Verification 不是 operation 全部完成。", "Read Sanitize AEI 01h/02h/03h with SOS/SANS. Entered Media Verification is not completion of the entire operation.", "SAN-EVENT"),
    187: f("BPID,CA", "Boot 更新只取 BPID 與 CA=110b/111b：前者替換 partition 內容，後者更新 active ID；兩個動作分開。", "For Boot, use BPID and CA=110b/111b: the former replaces partition contents and the latter changes the active ID. They are separate actions.", "BOOT-UPDATE"),
    188: f("MUD", "MUD 是重疊更新偵測的 completion 證據；仍需遵守單一 image sequence 的 controller/endpoint 邊界。", "MUD supplies completion evidence for overlapping updates; the single-controller/endpoint image-sequence boundary still applies.", "BOOT-SEQUENCE"),
    189: f("Boot Partition Write Prohibited,Invalid Firmware Image", "Boot Partition Write Prohibited 指向保護狀態；Invalid Firmware Image 指向 image/sequence 驗證。分辨 status 後才選重試步驟。", "Boot Partition Write Prohibited points to protection state; Invalid Firmware Image points to image/sequence validation. Classify status before choosing a retry step.", "BOOT-UPDATE"),
    190: f("DPTR", "Download 的 DPTR 指向此次 image portion 的 host buffer；資料指標不代表目標 Boot Partition 位址。", "Download DPTR identifies the host buffer for this image portion, not the destination Boot Partition address.", "BOOT-UPDATE"),
    191: f("NUMD", "NUMD 是此次 portion 的 zero-based dword count：512 bytes 編為 127，並須另外符合 Download 的 alignment/granularity 規則。", "NUMD is the portion's zero-based dword count: 512 bytes encodes as 127, with Download alignment/granularity requirements checked separately.", "BOOT-UPDATE"),
    192: f("OFST", "OFST 用 dword 表示 image offset；Boot image 需從開頭依序傳送，不能借用一般 firmware portion 的其他排序假設。", "OFST is an image offset in dwords. Boot images are sent in order from the beginning; do not borrow other ordering assumptions for ordinary firmware portions.", "BOOT-SEQUENCE"),
    193: f("Overlapping Range", "Overlapping Range 是 download portion 重疊的 status；保留每段 offset 與 length 才能重建錯誤區間。", "Overlapping Range reports overlapping download portions; preserve each offset and length to reconstruct the offending range.", "BOOT-SEQUENCE"),
    198: f("FID,SEL", "Get Features 以 FID 指定 feature，SEL 指定 current/default/saved/capabilities；FID 85h、17h 的值與 capability 不可混讀。", "Get Features uses FID for the feature and SEL for current/default/saved/capabilities. Do not confuse values for FID 85h/17h with their capabilities.", "BOOT-FID"),
    199: f("UUID Index", "CDW14 的 UUID Index 是共用 feature 介面的一部分；本報告的標準 FID 不需自創 vendor UUID 對應。", "The CDW14 UUID Index belongs to the common Feature interface; these standard FIDs do not call for invented vendor-UUID mappings.", "BOOT-FID"),
    201: f("CHANG,NSSPEC,SVBL", "SEL=011b 回傳的 bits 2/1/0 分別是 changeable/namespace-specific/saveable；不是 BP0WPS 或 NODRM 的當前值。", "For SEL=011b, bits 2/1/0 report changeable/namespace-specific/saveable, not current BP0WPS or NODRM values.", "BOOT-FID"),
    203: f("DPTR", "Get Log Page 的 data pointer 指向接收 buffer；buffer 必須容納 encoded NUMD 所要求的資料。", "Get Log Page's data pointer identifies a receive buffer large enough for the encoded NUMD request.", "TEL-ALIGN"),
    204: f("LID,LSP,RAE,NUMDL", "CDW10[7:0]=LID，[14:8]=LSP，[15]=RAE，[31:16]=NUMDL；LID 決定 LSP 是 Boot BPID 或 Telemetry capture controls。", "CDW10[7:0]=LID, [14:8]=LSP, [15]=RAE, and [31:16]=NUMDL. LID determines whether LSP means Boot BPID or Telemetry capture controls.", "TEL-CREATE"),
    205: f("NUMDU,LSI", "NUMDU 與 NUMDL 組成 zero-based dword count；LSI 是另一個 log-specific selector，不是 LSP。", "NUMDU and NUMDL form the zero-based dword count; LSI is a separate log-specific selector, not LSP.", "TEL-ALIGN"),
    206: f("LPOL", "LPO 低 32 bits 位於 CDW12；Telemetry byte offset 必須以 512-byte blocks 對齊。", "The low 32 bits of LPO occupy CDW12; Telemetry byte offsets must align to 512-byte blocks.", "TEL-ALIGN"),
    207: f("LPOU", "LPO 高 32 bits 位於 CDW13；不可先截斷為 32-bit 再計算大型 log 的 offset。", "The high 32 bits of LPO occupy CDW13; do not truncate a large-log offset to 32 bits before computing it.", "TEL-ALIGN"),
    208: f("CSI,OT,UUID Index", "CDW14 的 CSI/OT/UUID Index 是共用解碼上下文；先遵守該 LID 的 offset 語義，不能把 byte offset 誤作 index。", "CSI/OT/UUID Index in CDW14 provide common decoding context. Apply the LID's offset semantics rather than mistaking a byte offset for an index.", "TEL-ALIGN"),
    209: f("LID 07h,LID 08h,LID 15h,LID 81h", "僅取 07h、08h、15h、81h 四列；每列把 log ID 與其章節相連，不延伸其他 log 的教學。", "Use only the 07h, 08h, 15h, and 81h rows, connecting each ID to its section without extending into other logs.", "TEL-MODEL"),
    210: f("Supported Log Pages,LID Support and Effects", "Supported Log Pages 依 LID 提供 descriptor；07h descriptor 是 MCDAS 的查詢入口。", "Supported Log Pages provides a descriptor per LID; the 07h descriptor is the lookup point for MCDAS.", "TEL-CREATE"),
    211: f("LSUPP,LID Specific Parameter", "先查 LSUPP 再解該 LID 的 specific parameter；MCDAS 的 bit 0 是此 parameter 的內容，不是 CTHID。", "Check LSUPP before decoding that LID's specific parameter. MCDAS bit 0 belongs to this parameter, not to CTHID.", "TEL-CREATE"),
    220: f("CTHID,MCDA", "CTHID 位於 CDW10 bit 8，MCDA 位於 bits 11:9。MCDAS=1 且 CTHID=1 才套用 MCDA；後續讀同一 snapshot 用 CTHID=0。", "CTHID occupies CDW10 bit 8 and MCDA bits 11:9. Apply MCDA only with MCDAS=1 and CTHID=1; subsequent reads of that snapshot use CTHID=0.", "TEL-CREATE"),
    221: f("THDA1LB,THDA2LB,THDA3LB,THDA4LB,THS,THDGN,TCDA,TCDGN,RID", "07h 的 Last Blocks 在 bytes 8–19，THS 在 380、THDGN 在 381、TCDA/TCDGN 在 382/383；RID 在 384–511。先讀 header，再按累積 area 大小讀 payload。", "For 07h, Last Blocks occupy bytes 8–19, THS 380, THDGN 381, TCDA/TCDGN 382/383, and RID 384–511. Read the header before fetching cumulative-area payloads.", "TEL-MODEL"),
    222: f("MCDAS", "LID Specific Parameter bit 0 是 MCDAS；它宣告是否支援 MCDA，不表示已建立到哪一個 area。", "LID Specific Parameter bit 0 is MCDAS. It advertises MCDA support, not which area has already been created.", "TEL-CREATE"),
    223: f("TCDA1LB,TCDA2LB,TCDA3LB,TCDA4LB,TCS,TCDA,TCDGN,RID", "08h 的 TCS 在 byte 381；TCDA/TCDGN 位於 382/383。TCDGN 在資料更新最後才增加，讀完重讀 header 比對；TCDA=0 採 2.4 的 acknowledgement 後未更新語義。", "For 08h, TCS is byte 381 and TCDA/TCDGN are 382/383. TCDGN increments as the final update step; reread the header after collection. Interpret TCDA=0 using 2.4's no-update-since-acknowledgement meaning.", "TEL-TCDA"),
    279: f("BPID", "LID 15h 使用 CDW10 bit 8 選 BPID，其他 LSP bits 保留；同一 bit 在 07h 卻是 CTHID。", "LID 15h uses CDW10 bit 8 as BPID and reserves other LSP bits; that same bit means CTHID for 07h.", "BOOT-LOG"),
    280: f("LID,BPINFO,ABPID,BPSZ,BPD", "Header bytes 0–15；BPINFO 在 bytes 4–7，ABPID 是 bit 31，BPSZ 是 bits 14:0。BPD 從 byte 16 起，長度為 BPSZ×128 KiB。", "Header bytes are 0–15; BPINFO occupies 4–7 with ABPID at bit 31 and BPSZ at bits 14:0. BPD begins at byte 16 and is BPSZ×128 KiB long.", "BOOT-LOG"),
    311: f("Reservation Notification,Log Page Count,Notification Type", "這是 Reservation Notification 的通知資料結構，回報通知計數與類型等；不含 SPROG。8.1.27.4.2 的引用疑似錯置，進度應對照 Figure 312。", "This Reservation Notification structure reports notification counts/types and does not contain SPROG. The reference in 8.1.27.4.2 appears misplaced; use Figure 312 for progress.", "SOURCE-XREF"),
    312: f("SPROG,SSTAT,SCDW10,ETO,ETPVDS,SSI,MNSOIP,STNSID", "512-byte log：SPROG[1:0]、SSTAT[3:2]、SCDW10[7:4]、時間估計[35:8]、SSI[36]、MNSOIP[43:40]、STNSID[47:44]。先用 NSID 決定 target，再一起讀 SOS/SANS/FAILS 與進度。", "The 512-byte log has SPROG[1:0], SSTAT[3:2], SCDW10[7:4], estimates[35:8], SSI[36], MNSOIP[43:40], and STNSID[47:44]. Select the target with NSID, then interpret SOS/SANS/FAILS and progress together.", "SAN-STATUS"),
    338: f("BPCAP,LPA,SANICAP,CTRATT", "只解本題欄位：BPCAP byte 102，LPA byte 261，SANICAP bytes 328–331，以及 CTRATT 的 MDS；SANICAP 分開檢查方法、VERS/NVERS、SPRRS、NDI 與 NODMMAS。", "Decode only this report's fields: BPCAP byte 102, LPA byte 261, SANICAP bytes 328–331, and MDS in CTRATT. Check methods, VERS/NVERS, SPRRS, NDI, and NODMMAS separately.", "SAN-NDAS"),
    451: f("SANACT,AUSE,OWPASS,OIPBP,NDAS,EMVS,PREQ", "由 SANACT 決定操作，再依方法解讀其餘 bits；OWPASS=0 是 16，EMVS 不能搭配 Overwrite/NDAS=1。PREQ bit 11 與 namespace 命令不同。", "Select the action with SANACT before decoding method-dependent bits. OWPASS=0 means 16, and EMVS cannot combine with Overwrite/NDAS=1. PREQ bit 11 differs from the namespace command.", "SAN-COMMAND"),
    452: f("OVRPAT", "CDW11 的 32-bit OVRPAT 僅在 Overwrite 適用；搭配 OIPBP 與 pass 奇偶才可推導每一輪寫入 pattern。", "The 32-bit OVRPAT in CDW11 applies only to Overwrite. Combine it with OIPBP and pass parity to derive each pass's pattern.", "SAN-OVERWRITE"),
    453: f("Firmware Activation Requires Reset,PMR Enabled,Controller Suspended", "這些是啟動命令的 command-specific failure；與稍後背景作業的 Sanitize Failed/SOS 分開記錄。", "These are command-specific failures of the initiating command. Record them separately from later background-operation Sanitize Failed/SOS results.", "SAN-PREFLIGHT"),
    454: f("SANACT,AUSE,PREQ,EMVS", "Namespace CDW10 只有 Exit Failure/Crypto Erase/Exit Verification；PREQ 在 bit 4，EMVS 在 bit 10，無 NDAS 或 Overwrite 參數。", "Namespace CDW10 offers Exit Failure/Crypto Erase/Exit Verification, with PREQ at bit 4 and EMVS at bit 10, and no NDAS or Overwrite parameters.", "SAN-NAMESPACE"),
    464: f("FID,SV", "Set Features 的 FID 決定 CDW11 解法；SV 是保存要求，不能因設定成功就推論 power cycle 後仍保留。", "Set Features FID selects the CDW11 interpretation. SV requests saving; successful setting alone does not prove persistence through power cycles.", "BOOT-FID"),
    465: f("UUID Index", "Set 的 UUID Index 使用條件與 feature identity 一起判斷；本題標準 FIDs 不擴成 vendor feature protocol。", "Interpret the Set UUID Index with feature identity; these standard FIDs do not expand into a vendor-feature protocol.", "BOOT-FID"),
    466: f("FID 85h,FID 17h,FID 0Bh,FID 16h", "只看 Boot protection、Sanitize Config、AEC、Host Behavior Support 的 feature rows 與 scope；FID 17h 是 subsystem policy。", "Use only rows/scopes for Boot protection, Sanitize Config, AEC, and Host Behavior Support. FID 17h is subsystem policy.", "SAN-NDAS"),
    474: f("TLN", "只取 bit 10 TLN：TCDA 從 0h 變 1h 且 TLN enabled 時發送 Telemetry Log Changed；此表在 5.2.30.1.6。", "Use TLN bit 10: when TCDA changes from 0h to 1h with TLN enabled, Telemetry Log Changed is reported. This table belongs to 5.2.30.1.6.", "TEL-EVENT"),
    491: f("ETDAS", "Host Behavior Support byte 1 的 ETDAS=1 表示 host 支援 Area 4；仍需 controller 的 DA4S。", "ETDAS=1 at Host Behavior Support byte 1 declares host Area 4 support; controller DA4S is still required.", "TEL-DA4"),
    492: f("NODRM", "FID 17h CDW11 bit 0 是 NODRM；只有 NDI=1 且命令 NDAS=1 才影響 error/warning response。不是每次 sanitize 都必須設定的開關。", "FID 17h CDW11 bit 0 is NODRM. It selects error/warning response when NDI=1 and command NDAS=1; it is not a switch required for every sanitize.", "SAN-NDAS"),
    542: f("BP0WPS,BP1WPS", "兩個 3-bit state 欄位獨立設定；000b 只表示 Set 不改變，Get 需回實際狀態，100b 只回報 RPMB 控制。", "The two three-bit state fields are set independently. 000b only requests no change in Set; Get returns actual state and uses 100b only to report RPMB ownership.", "BOOT-FID"),
    679: f("Boot Partition 0,Boot Partition 1,Host Memory Buffer", "把兩個等大的 Boot Partitions 與此次 host 讀取 buffer 分開；active ID 選擇啟動映像，不限制 host 只能讀 active partition。", "Separate the two equal Boot Partitions from this read's host buffer. Active ID selects the boot image, not a restriction to reading only the active partition.", "BOOT-MODEL"),
    680: f("Write Unlocked,Write Locked,Write Locked Until Power Cycle", "Set Features 在 unlocked/locked 間切換，兩者可進入 locked-until-power-cycle；power cycle 回 locked。Locked-until-power-cycle 沒有一般 Set 解鎖箭頭。", "Set Features switches unlocked/locked and can move either to locked-until-power-cycle; a power cycle returns to locked. There is no ordinary Set-unlock edge from locked-until-power-cycle.", "BOOT-RESET"),
    681: f("Power Cycles,Controller Level Resets", "逐列比較三個 state：controller reset 保留它們；power cycle 後 unlocked 與 until-power-cycle 都變 locked。", "Compare all three states: controller reset preserves them, while power cycle changes unlocked and until-power-cycle to locked.", "BOOT-RESET"),
    682: f("RPMB Disabled,RPMB Enabled,Write Locked,Write Unlocked", "RPMB enable 之前與之後是不同區域；啟用後以 authenticated configuration write 解鎖/上鎖，reset 會回 locked。", "Before and after RPMB enablement are different regions; once enabled, authenticated configuration writes unlock/lock and resets return to locked.", "BOOT-RESET"),
    683: f("RPMB Protection Enabled,Persistence", "RPMB-only 且保護尚未啟用時 unlocked 可保留；保護啟用後 unlocked 不跨 reset/power cycle。雙機制支援時還要套用 Figure 684 的預設與控制權。", "For RPMB-only protection before enablement, unlocked can persist; once enabled, unlocked does not survive reset/power cycle. Dual-mechanism support also requires Figure 684's defaults and ownership rules.", "BOOT-RESET"),
    684: f("Set Features Owner,RPMB Owner,Enable Gate", "先沿 Set Features 區追蹤狀態，再經 enable gate 轉移到 RPMB；不能從 until-power-cycle bypass 到 RPMB。", "Track states in the Set Features region, then transfer through the enable gate to RPMB; until-power-cycle cannot be bypassed through RPMB enablement.", "BOOT-REJECT"),
    756: f("Boot Partition Write Protection Enable,Boot Partition Write Protection", "Device Configuration Block 分開保存啟用保護與每個 partition 的鎖定控制；啟用後拒絕關閉 RPMB Boot 保護的寫入。", "The Device Configuration Block separates protection enablement from each partition's lock control; once enabled, writes attempting to disable RPMB Boot protection are rejected.", "BOOT-CAP"),
    757: f("Authenticated Device Configuration Block Read,Authenticated Device Configuration Block Write", "只追蹤 Boot 所需的 authenticated configuration read/write message types；message type 必須與預期 response 配對。", "Track authenticated configuration read/write message types needed for Boot and pair each request with its expected response.", "BOOT-CAP"),
    758: f("Result,Authentication Failure,Counter Failure", "Operation Result 區分成功、認證與 counter 等失敗；傳輸命令完成不等於 RPMB 寫入已成功。", "Operation Result distinguishes success, authentication, counter, and other failures; transport-command completion does not itself prove successful RPMB writing.", "BOOT-CAP"),
    760: f("Message Type,Result,Write Counter,Nonce,Authentication", "Frame 的 message type、counter、nonce、result 與 authentication 是驗證回應的不同證據；不能只看資料 payload。", "Message type, counter, nonce, result, and authentication provide different response-validation evidence in the frame; payload alone is insufficient.", "BOOT-CAP"),
    761: f("Authentication Key,Program Result", "Authentication key 的設定是 authenticated configuration 流程的前置背景；需核對 programming result，不把送出 key 當成成功。", "Authentication-key programming is prerequisite context for authenticated configuration; verify its result rather than equating key submission with success.", "BOOT-CAP"),
    762: f("Write Counter,Nonce,Authenticated Response", "先取得並驗證 write counter，配合 nonce/authentication 確認回應，再構造受保護的 configuration write。", "Obtain and validate the write counter, use nonce/authentication to verify the response, then construct the protected configuration write.", "BOOT-CAP"),
    765: f("Configuration Write,Counter,Result Read", "Authenticated configuration write 後需核對 result；此流程變更 Boot 保護狀態，不是 Firmware Commit 寫入 image 的流程。", "Verify the result after an authenticated configuration write. This changes Boot protection state, not image contents as Firmware Commit does.", "BOOT-CAP"),
    766: f("Configuration Read,Nonce,Authentication", "Authenticated configuration read 取得可驗證的保護設定，用以確認哪一套機制目前控制 partition。", "Authenticated configuration read retrieves verifiable protection settings used to establish which mechanism currently controls the partition.", "BOOT-CAP"),
    770: f("Subsystem Target,Namespace Target,User Data,Boot Partition,CMB,PMR", "每一資料類別分別看兩種 target：Boot/RPMB 不動，user-data locations 要處理，CMB/PMR/PDA 的差異不可被『全部 namespaces』概括。", "Evaluate both targets for each data class: Boot/RPMB stay unchanged, user-data locations are processed, and CMB/PMR/PDA differences cannot be summarized as all namespaces.", "SAN-SCOPE"),
    771: f("OIPBP,OWPASS,OVRPAT,PI", "用 total pass 奇偶決定第一輪是否反相，再逐輪反相；PI bytes 也有 FFh/00h 規則。不能只看最後的 OVRPAT。", "Use total-pass parity to determine whether the first pass is inverted, then invert between passes; PI bytes follow FFh/00h rules too. OVRPAT alone is insufficient.", "SAN-OVERWRITE"),
    772: f("Idle,Restricted Processing,Restricted Failure,Unrestricted Processing,Unrestricted Failure,Media Verification,Post-Verification Deallocation", "七個 state 以 AUSE 分出兩條 processing/failure 路徑，EMVS 接到 verification，再經 deallocation 返回；逐條配合 Figures 773–779 判讀。", "Seven states split into processing/failure paths through AUSE, use EMVS to reach verification, then return through deallocation. Interpret each edge with Figures 773–779.", "SAN-STATE"),
    773: f("A1,AUSE=0,B1,AUSE=1", "Idle 的 A1/B1 分別進 Restricted/Unrestricted Processing；進入時清 SPROG 與 MVCNCLD，不代表 operation 已完成。", "A1/B1 leave Idle for Restricted/Unrestricted Processing respectively. Entry clears SPROG and MVCNCLD; it does not mean the operation is complete.", "SAN-STATE"),
    774: f("C1,D1,F1,EMVS,MVCNCLD", "Restricted Processing 成功可 C1 回 Idle 或 F1 進 Verification，取決於 EMVS/MVCNCLD；D1 表示 processing 失敗。", "Restricted Processing succeeds through C1 to Idle or F1 to Verification depending on EMVS/MVCNCLD; D1 reports processing failure.", "SAN-STATE"),
    775: f("A2,Restricted Retry", "Restricted Failure 只有 A2 重進 Restricted Processing 的恢復路徑；Exit Failure Mode 與 AUSE=1 不能取代成功的 restricted retry。", "Restricted Failure recovers through A2 into Restricted Processing; Exit Failure Mode and AUSE=1 cannot substitute for a successful restricted retry.", "SAN-STATE"),
    776: f("C2,D2,F2,EMVS,MVCNCLD", "Unrestricted Processing 的 C2/D2/F2 對應成功回 Idle、失敗、進入 Verification；不是允許一般 I/O 不受限制。", "C2/D2/F2 from Unrestricted Processing mean successful Idle return, failure, or entry into Verification; unrestricted does not mean ordinary I/O is unrestricted.", "SAN-STATE"),
    777: f("A3,B2,E,Exit Failure Mode", "Unrestricted Failure 可 A3 restricted retry、B2 unrestricted retry，或 E Exit Failure Mode 到 Idle；E 不能當成 sanitize 成功證據。", "Unrestricted Failure permits A3 restricted retry, B2 unrestricted retry, or E Exit Failure Mode to Idle; E is not proof of successful sanitization.", "SAN-STATE"),
    778: f("G,Exit Media Verification,Reset,MVCNCLD", "G 進 Post-Verification Deallocation：由退出動作、指定 reset 或阻止 verification 的 composition change 觸發；取消驗證須對照 MVCNCLD。", "G enters Post-Verification Deallocation on the exit action, specified resets, or a composition change preventing verification; check MVCNCLD for canceled verification.", "SAN-VERIFY-STATE"),
    779: f("H,I1,I2,FAILS", "Deallocation 成功走 H 到 Idle；失敗依原 AUSE 走 I1/I2 到 Failure，FAILS 記 6h，與 processing 失敗的來源區分。", "Successful deallocation takes H to Idle; failure follows original AUSE through I1/I2 to Failure, with FAILS=6h distinguishing it from processing failure.", "SAN-VERIFY-STATE"),
    780: f("Last Block 65,Last Block 1000,Last Block 30000", "65/1000/30000 的三個 areas 共享前綴；Area 3 包含 Area 1 與 2，不把長度相加。", "Areas ending at 65/1000/30000 share prefixes; Area 3 includes Areas 1 and 2, so do not sum their lengths.", "TEL-MODEL"),
    781: f("Last Block 0,Last Block 1000,Equal Endpoints", "0/1000/1000 表示 Area 1 空、Area 2 有資料、Area 3 無新增資料；Area 3 的視圖仍涵蓋與 Area 2 相同的 blocks。", "Endpoints 0/1000/1000 mean empty Area 1, populated Area 2, and no additional Area 3 data; the Area 3 view still covers the same blocks as Area 2.", "TEL-MODEL"),
}

NVM_FIGURES = {
    11: f("PRACT,PRCHK,GRDCHK,ATCHK,RTCHK", "PRACT 處理 PI 傳遞，PRCHK 的三個 bits 分別要求 Guard/Application/Reference Tag checking；Media Verification 明確要求 PRCHK=000b。", "PRACT governs PI handling; the three PRCHK bits request Guard/Application/Reference Tag checking. Media Verification explicitly requires PRCHK=000b.", "NVM-VERIFY"),
    12: f("STC,Storage Tag", "此處 STC 是 Storage Tag Check，不是另一報告的 Self-test Code；驗證 Read 要求 STC=0。", "Here STC is Storage Tag Check, not Self-test Code from another report; verification Reads require STC=0.", "NVM-VERIFY"),
    200: f("Get Log Page,Error Information,LBA", "NVM Command Set 補充 sanitize 期間的 Error Information 行為，LBA 回 0；同號的 Base Figure 200 是另一張表，不可混用。", "The NVM Command Set adds Error Information behavior during sanitize: return zero in LBA. Base Figure 200 is a different table and cannot be substituted.", "NVM-BRIDGE"),
    201: f("Block Erase,Crypto Erase,Overwrite", "三種方法的 audit data values 分別是 vendor-specific、indeterminate、依 Overwrite 機制；若已 deallocate 則讀取依另一套規則。", "Audit values are vendor-specific, indeterminate, or governed by Overwrite for the three methods; deallocated-block reads follow separate rules.", "NVM-VALUES"),
}


def guide_for(figure, language):
    source = NVM_FIGURES if figure["source_id"] == "NVME-NVM-CS-1.3" else BASE_FIGURES
    return source[int(figure["number"])][language]


def expanded_guide(figure, language, fallback):
    try:
        from scripts.nvme_boot_telemetry_sanitize import MODULES
        from scripts.nvme_bts_terms import definition
    except ModuleNotFoundError:
        from nvme_boot_telemetry_sanitize import MODULES
        from nvme_bts_terms import definition
    source = NVM_FIGURES if figure["source_id"] == "NVME-NVM-CS-1.3" else BASE_FIGURES
    data = source[int(figure["number"])]
    claim_id = 'BASEBTS-' + data['claim']
    module = next(m for m in MODULES if claim_id in m['sources'])
    english = language == 'en'
    # The figure's field slice, supporting mechanism, and worked scenario are
    # separate; field names alone cannot choose a generic state-machine lesson.
    kind = 'state' if int(figure['number']) in range(680, 685) or int(figure['number']) in range(772, 780) else 'layout'
    context = data[language]
    return dict(
        kind=kind, context=context,
        kind_text=("The indexed fields below belong to this source document and this Figure. The worked example connects them to the full operation." if english else "下列欄位限定於此來源文件與此 Figure；範例將欄位連回完整操作。"),
        terms=[(term, definition(term, figure['report_id'], language, fallback)) for term in data['key_items']],
        steps=[
            (f"Confirm {figure['source_id']}, §{figure['section']}, Figure {figure['number']}; equal Figure numbers in different documents are different sources." if english else f"確認 {figure['source_id']}、§{figure['section']}、Figure {figure['number']}；不同文件的同號 Figure 是不同來源。"),
            ("Apply the field/state rule above to the captured raw input." if english else "將上方欄位／狀態規則套用到保存的原始輸入。"),
            module['lead'][language],
            ("Compare the observation with the worked scenario and retain the cited source and target identity." if english else "用具體情境比對觀測結果，保留引用位置與 target 身分。"),
        ],
        answers=[
            ['Rule' if english else '規則', context],
            ['Boundary' if english else '邊界', module['pitfall'][language]],
        ],
        example=module['example'][language],
        debug=[['Symptom / correction' if english else '症狀／修正', module['pitfall'][language]]],
        misconception=module['pitfall'][language],
        check=[
            ("Which source-specific fields establish the decision?" if english else "哪些本文件的欄位支持這個判斷？"),
            ("Which capability, target, or state would change the worked result?" if english else "哪個 capability、target 或 state 會改變範例結果？"),
        ],
    )
