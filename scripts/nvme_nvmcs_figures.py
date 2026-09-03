"""Source-specific figure worksheets; captions and page evidence live in the register."""
try:
    from scripts.nvme_nvm_command_set import LESSONS, MODULES, REPORT_ID, b
except ModuleNotFoundError:
    from nvme_nvm_command_set import LESSONS, MODULES, REPORT_ID, b

DETAILS = {}


def f(numbers, fields, zh, en):
    for n in numbers if isinstance(numbers, list) else [numbers]:
        DETAILS[n] = dict(key_items=fields.split(','), text=b(zh,en))


f(1,'Base,PCIe Transport,NVM Command Set','依功能層分開閱讀：Base 給共同機制，PCIe 給本機 transport，NVM 給 logical-block 命令語意；這是保留範圍的家族關係重畫。','Read by functional layer: Base supplies shared mechanisms, PCIe the local transport, and NVM logical-block command semantics. This redraw retains only the included family relationships.')
f(2,'LBA','LBA 是 logical block 的位址，不是 byte offset；要換成資料 bytes，還需所選格式的 LBADS。','LBA addresses a logical block, not a byte offset; converting to data bytes also requires LBADS from the selected format.')
f(3,'Compare,Write,Match','先 Compare 成功才執行同 range 的 Write；兩個 CQE 分別表示比對與寫入結果，並須檢查 fused atomicity limits。','Compare must succeed before Write updates the same range. Two CQEs report comparison and write outcomes separately; fused atomicity limits still apply.')
f(4,'AWUN,AWUPF,ACWU,NAWUN,NAWUPF,NACWU,NABSN,NABSPF,NABO','先用 NSABP 選 controller 或 namespace 值，再解碼 0-based 大小及 namespace 的零值繼承規則；不可把每個 raw 0 都解釋成一個 block。','Use NSABP to select controller or namespace parameters, then decode zero-based sizes and namespace zero-value inheritance. Raw zero does not universally mean one block.')
f(5,'Overlapping writes,Read result,AWUN','本圖討論正常運作下重疊寫入的可觀測結果；將 write size 與解碼後 AWUN 比較，再看讀取是否落在相同 atomic unit。','This table concerns observable overlapping-write results during normal operation. Compare write size with decoded AWUN and locate the read within atomic units.')
f(6,'Old data,New write,AWUPF','先保存失敗前的媒體內容與此次 write 範圍，這個 initial state 是下一張 failure-result 表的前提。','Record pre-failure media contents and the new write range. This initial state supplies the assumptions for the following failure-result table.')
f(7,'Old data,Torn write,AWUPF','把 power-fail 原子大小內的舊資料保留保證，與超過大小時可能 torn write 的結果分開；未完成寫入不能當作全新資料。','Separate old-data preservation within the power-fail atomic unit from possible torn writes above it. An unfinished write cannot be assumed to contain all-new data.')
f(8,'NABO,NABSN,NABSPF','在數線標出 offset+k×boundary size；長度小於 atomic size 仍可能因起點而跨 boundary。','Place boundaries at offset+k×boundary size on the LBA line. A write shorter than the atomic size can still cross a boundary because of its starting position.')
f(9,'MAM,NAWUN,NAWUPF,NABSN,NABSPF','Multiple 模式將適用 normal／power-fail size 與兩種 boundary size 對齊成相同值；fused 比對寫入仍遵守 Single 模式。','Multiple mode aligns the applicable normal/power-fail sizes with both boundary sizes. Fused Compare-and-Write still follows Single mode.')
f(10,'Write A,Write B,Write C,Write D,Atomic subranges','Single 模式要分開的 A/B/C，在 Multiple 模式可由 D 覆蓋，但保證仍以每個切出的 subrange 為單位，不是 D 整體 transaction。','A/B/C require separate commands for the illustrated Single-mode guarantees. Multiple-mode D can cover them together, but guarantees remain per subrange, not one D-wide transaction.')
f(11,'PRACT,PRCHK,GRDCHK,ATCHK,RTCHK','PRACT 是 action，PRCHK 是三種檢查的 bit mask。PRACT=1 時先比較 MS 與 PI size，才能知道資料是否 strip／insert 或維持 metadata 大小。','PRACT selects an action and PRCHK selects three checks. With PRACT=1, compare MS with PI size to determine stripping/insertion versus preservation of metadata size.')
f(12,'STC,STS','STC 啟用 Storage Tag checking；STS=0 時沒有 Storage Tag，controller 忽略 STC。','STC enables Storage Tag checking. When STS=0 there is no Storage Tag and the controller ignores STC.')
f(13,'Get LBA Status,I/O controller,Administrative controller','Get LBA Status 86h 對 I/O controller 是 optional、對 Administrative controller 禁止；本工作表只保留這兩欄。','Get LBA Status 86h is optional for an I/O controller and prohibited for an Administrative controller; this worksheet retains those two columns.')
f(14,'Read,Write,Optional commands','Read／Write 是 mandatory；Compare、Verify、Copy、Write Zeroes、Write Uncorrectable 等須檢查各自能力，不能用表列存在代替支援宣告。','Read/Write are mandatory. Compare, Verify, Copy, Write Zeroes, Write Uncorrectable, and other optional commands require their own capability checks; appearing in the table does not establish support.')
f(15,'LID 0Eh,LID 28h','0Eh 為 I/O controller 的 optional log；28h 對 I/O 與 Administrative controllers 都是 optional。支援與作用域另查 log 定義。','0Eh is optional for I/O controllers; 28h is optional for I/O and Administrative controllers. Check the log definition separately for scope.')
f(16,'FID 03h,FID 05h,FID 0Ah,FID 15h,FID 1Ch,FID 28h','將各 Feature 的 support row 與 controller 類型對照；Administrative controller 的 Performance Characteristics 不允許 namespace scope。','Match each Feature support row to controller type. Performance Characteristics on an Administrative controller cannot have namespace scope.')
f(17,'Persistent Event Log,Optional,Not recommended','此表是是否將 Feature 更新寫入 Persistent Event Log 的要求；03h 的 NR 不是禁止使用該 Feature，也不是其他 Features 的支援等級。','This table governs recording Feature updates in the Persistent Event Log. NR for 03h does not prohibit the Feature and is not another Feature support classification.')
f(18,'SCT,SC,LBA Out of Range,Capacity Exceeded','Generic status 80h 是 LBA Out of Range，81h 是 Capacity Exceeded；解碼前保留 SCT，並分別核對 NSZE 與 NCAP／NUSE。','Generic status 80h is LBA Out of Range and 81h Capacity Exceeded. Retain SCT and check NSZE separately from NCAP/NUSE.')
f(19,'SCT=1,Command-specific status','用 opcode 與 SCT=1 找對應 command-specific status；例如 Copy 的格式／重疊錯誤與 Read 的 PI 錯誤有不同適用集合。','Use opcode and SCT=1 to select command-specific status. Copy format/overlap errors and Read PI errors have different applicability sets.')
f(20,'Compare Failure,Deallocated or Unwritten Logical Block','Media/Data Integrity 類型含 Compare miscompare 與 deallocated/unwritten 存取錯誤；後者要回查 DULBE，而非直接判為壞媒體。','Media/Data Integrity status includes Compare miscomparison and deallocated/unwritten access errors. Investigate DULBE for the latter rather than immediately declaring bad media.')
f(21,'PID,RUHID,EARUTR,RUAMW','以 PID 找 Placement Handle／Reclaim Group，再解讀 RUHID、剩餘時間估計及可寫 blocks；RUAMW 不是固定的 nominal RU size。','Use PID for Placement Handle/Reclaim Group, then interpret RUHID, estimated time remaining, and writable blocks. RUAMW is not a fixed nominal RU size.')
f(22,'Opcode,NSID,Transfer direction','Opcode 低兩 bits 指示資料傳輸方向；Copy 的 host-to-controller 是 descriptors。除特別註明的命令外，不能使用 broadcast NSID。','The low two opcode bits encode transfer direction; Copy transfers descriptors host-to-controller. Broadcast NSID is unavailable except for specifically noted commands.')

# Repeated command layouts receive field-specific explanations, not a generic
# paragraph inferred from the word "command" in a caption.
f([23,50,67],'MPTR','MPTR 只在所選格式使用 separate metadata 時提供 metadata 位置；先核對 PSDT／metadata 格式，不能把它當成 user-data buffer。','MPTR supplies the metadata location for a separate-metadata format. Check PSDT/metadata format first; it is not the user-data buffer.')
f([24,68],'DPTR','這裡的 DPTR 指向 host 輸入資料：Compare 的 expected data 或 Write 的新資料；PRP／SGL 由 common command format 決定。','Here DPTR addresses host input: expected Compare data or new Write data. The common command format determines PRP/SGL interpretation.')
f([32,44],'DPTR','DPTR 指向 descriptors，而不是待複製或 deallocate 的 user data；buffer 長度需由 descriptor size 與解碼後 range count 計算。','DPTR addresses descriptors rather than user data to copy or deallocate. Compute buffer length from descriptor size and decoded range count.')
f([51,135],'DPTR','DPTR 是 controller 回傳資料的 host 目的位置；Read 回 data，Get LBA Status 回 descriptor list，兩者不可共用 payload parser。','DPTR addresses the host destination: Read returns data and Get LBA Status returns a descriptor list. They cannot share one payload parser.')
f([25,52,60],'ELBTU,ELBTL,ELBST,EILBRT','CDW2／3 的 upper tags 要和 CDW14 lower tags 合併，再依 PI 格式與 STS 拆成 expected storage／reference；unused bits 依格式忽略。','Combine CDW2/3 upper tags with CDW14 lower tags, then split expected storage/reference fields by PI format and STS. Unused bits are ignored as specified by the format.')
f([33,69,81],'LBTU,LBTL,LBST,ILBRT','Upper／lower tag 欄位組成寫入端的 Storage 與初始 Reference Tag；Copy 的這組 command fields 屬於 destination，source expectations 在 descriptors。','Upper/lower tag fields encode write-side Storage and initial Reference Tags. For Copy these command fields belong to the destination; source expectations are in descriptors.')
f([26,53,61,70,77,82,136],'SLBA,CDW10,CDW11','64-bit SLBA 的低 32 bits 在 CDW10、高 32 bits 在 CDW11；先完成 range-specific 模式檢查，才把它作為位址使用。','SLBA is 64 bits: low 32 in CDW10, high 32 in CDW11. Check range-specific modes before using it as an address.')
f(34,'SDLBA','SDLBA 指第一個 destination block，後續來源按 descriptor 順序連接；它不會為每個 source range 重新歸零。','SDLBA identifies the first destination block; subsequent sources concatenate in descriptor order rather than restarting the destination for each range.')
f([27,54,62,71],'LR,FUA,PRINFO,STC,CETYPE,NLB','CDW12 合併行為 bits 與 0-based NLB；Compare／Verify 要 PRACT=0，Read／Write 才依 metadata 格式選 PRACT。FUA 不建立其他命令順序。','CDW12 combines behavior bits with zero-based NLB. Compare/Verify require PRACT=0, while Read/Write select PRACT by metadata format. FUA does not order other commands.')
f([28,56,63],'CETYPE,CEV','CETYPE 非零時 CDW13 low16 解讀為 CEV；CETYPE=0 的 layout 另有定義或 reserved，不能同時塞 DSM hints。','With nonzero CETYPE, CDW13 low16 contains CEV. CETYPE=0 has a different or reserved layout; do not simultaneously encode DSM hints.')
f([29,57,64],'ELBTL,ELBTU','CDW14 是 expected-tag 空間低 32 bits；它未必全是 Reference Tag，STS 可能占用其中高 bits。','CDW14 contains the low 32 bits of expected-tag space. It is not necessarily all Reference Tag: STS may consume some high bits.')
f([30,58,65],'ELBATM,ELBAT','CDW15 high16 是 Application Tag mask，low16 是 expected tag；mask bit=0 表示不比較該位，不是要求 tag bit=0。','CDW15 high16 is the Application Tag mask and low16 the expected tag. A zero mask bit excludes comparison rather than requiring a zero tag bit.')
f([31,59,66,76,80,89],'SCT,SC,Command-specific error','把此命令列出的 SC 與 SCT 一起比對；Invalid Protection Information 指設定／初值不適合所選格式，與實際 Guard Check Error 不同。只適用於本表列出的命令。','Compare SC together with SCT and this command’s applicable entries. Invalid Protection Information concerns settings/initial values incompatible with the format, distinct from a Guard Check Error. Apply only entries listed for the command.')
f(35,'PRINFOW,PRINFOR,STCR,STCW,DESFMT,NR','Copy 在同一 CDW12 分開讀端／寫端 PI、descriptor format 與 0-based range count。STCRS 的正確能力定義在 Figure 127；本圖指 Figure 115 的文字引用錯置。','Copy CDW12 separates read/write PI, descriptor format, and zero-based range count. STCRS is defined in Figure 127; this figure’s reference to Figure 115 is misplaced.')
f([36,73,85],'DSPEC,CEV','CDW13 high16 保存 Directive Specific，low16 依 CETYPE 保存 CEV；Directive 與 command extension 是獨立欄位。','CDW13 high16 carries Directive Specific and low16 carries CEV according to CETYPE. Directive and command extension are separate fields.')
f([37,74,86],'LBTL,LBST,ILBRT','CDW14 提供寫入 tags 的低 32 bits；依 STS 將 space 分割，不能把高位 Storage Tag 全部丟棄。','CDW14 supplies the low 32 bits of write tags. Split the space according to STS rather than discarding Storage Tag high bits.')
f([38,75,87],'LBATM,LBAT','Application Tag mask 與 tag 分別在 CDW15 high16／low16；Copy 使用於寫入目的端，來源端有獨立 expected 欄位。','Application Tag mask/tag occupy CDW15 high16/low16. Copy uses these for the destination write, with separate expected fields for sources.')
f(39,'DESFMT,SNSID,PI size','0h/2h 搭配 8-byte PI、1h/3h 搭配 16-byte PI；2h/3h 有 SNSID。4h 指向另一 command set 的 Memory Copy 定義，這份 NVM 文件沒有其完整 descriptor layout。','Formats 0h/2h pair with eight-byte PI and 1h/3h with 16-byte PI; 2h/3h contain SNSID. Format 4h refers to Memory Copy in another command set; this NVM document does not provide its complete descriptor layout.')
f(40,'SNSID,SLBA,NLB,ELBT,ELBAT,ELBATM,FCO','0h/2h 每個 source entry 32 bytes；0h 的 SNSID／FCO 位置 reserved，2h 可使用。NLB 先加一，再累加至 destination length。','Formats 0h/2h use 32-byte source entries. SNSID/FCO locations are reserved in 0h and usable in 2h. Add one to NLB before accumulating destination length.')
f(41,'SNSID,SLBA,NLB,ELBTU,ELBTL,FCO','1h/3h 每個 source entry 40 bytes，以較大的 tags 支援 16-byte PI；3h 帶 SNSID／FCO，不能用 32-byte stride 解析。','Formats 1h/3h use 40-byte source entries with larger tag fields for 16-byte PI. Format 3h carries SNSID/FCO; a 32-byte parsing stride is incorrect.')
f(42,'Source ranges,SDLBA,Destination offsets','依 source descriptor 順序把各段長度相加，產生連續 destination；圖中的加總是 block 數，不能直接累加 raw NLB 而漏掉每段的一。','Sum decoded source lengths in descriptor order to form the contiguous destination. The diagram sums block counts, not raw NLB values missing one block per range.')
f(43,'Fast Copy Not Possible,Overlapping I/O Range,Insufficient Resources','Copy 錯誤要合看 CQE DW0 的最低失敗 source index；後續 entries 可能已處理，不能假設回滾。FCO 失敗再依 DNR 判斷重試。','Read Copy errors with CQE DW0’s lowest failed source index; later entries may already be processed, so rollback is not implied. Use DNR when considering retry after FCO failure.')
f(45,'NR','CDW10 low8 的 NR 是 0-based，最大 FFh 表示 256 個 ranges；這與 DMRL 的 1-based limit 不同。','NR in CDW10 low8 is zero-based: FFh requests 256 ranges. This differs from the one-based DMRL processing limit.')
f(46,'AD,IDW,IDR','CDW11 bits2/1/0 分別是 deallocate、integral write、integral read hints；處理 AD 不代表一定釋放。','CDW11 bits2/1/0 select deallocate, integral-write, and integral-read hints. Processing AD does not guarantee deallocation.')
f(47,'CATTR,LLB,SLBA','每筆 16 bytes：CATTR、1-based LLB、64-bit SLBA；256 筆需要 4096 bytes。不要沿用 NLB 的加一解碼。','Each 16-byte entry contains CATTR, one-based LLB, and 64-bit SLBA; 256 entries require 4096 bytes. Do not apply NLB’s add-one decoding.')
f(48,'CASZE,WPREP,SWR,SRR,AL,AF','這些 context attributes 描述預期 workload；即使 host hints 不精確，controller 仍須維持資料完整性。','These context attributes describe an expected workload. The controller must preserve data integrity even when host hints are inaccurate.')
f(49,'Conflicting Attributes,Command Size Limit Exceeded','DSM 的 size-limit error 受 NVMDSMSV 影響；variant=1 不得因 processing limits 回報該錯誤。','DSM size-limit status depends on NVMDSMSV; variant=1 must not return that error because of processing limits.')
f(55,'DSM,INCPRS,SEQREQ,AL,AF','Read 在 CETYPE=0 才用 CDW13 low8 提供 DSM hints；one-time／speculative read 是 access-frequency hints，不保證 controller 一定改變 cache 策略。','Read uses CDW13 low8 DSM hints only when CETYPE=0. One-time/speculative reads are access-frequency hints, not guaranteed cache-policy changes.')
f(72,'DSPEC,DSM','Write 的 CETYPE=0 layout 包含 high16 DSPEC 與 low8 DSM；不要與 CETYPE 非零的 CEV layout 混寫。','The CETYPE=0 Write layout contains high16 DSPEC and low8 DSM. Do not mix it with the nonzero-CETYPE CEV layout.')
f(78,'DTYPE,NLB','Write Uncorrectable 的 CDW12 保留 Directive Type 與 0-based NLB；沒有 Read／Write 的 FUA／PRINFO 欄位，不能直接複用那些命令。','Write Uncorrectable CDW12 carries Directive Type and zero-based NLB. It lacks Read/Write FUA/PRINFO fields, so their encoding cannot be copied wholesale.')
f([79,84],'DSPEC,Reserved','此 CDW13 layout 只使用 high16 DSPEC，low16 reserved；保留位不是額外的 tag 或長度空間。','This CDW13 layout uses only high16 DSPEC, with low16 reserved. Reserved bits are not additional tag or length space.')
f(83,'NSZ,DEAC,PRINFO,STC,DTYPE,NLB','NSZ 在 bit23，DEAC 在 bit25，因此這裡 DTYPE 只有 bits22:20。PRCHK=000b、STC=0；整個 namespace 模式還要 NSZS 與零值讀取條件。','NSZ is bit23 and DEAC bit25, leaving DTYPE at bits22:20. PRCHK=000b and STC=0 are required; whole-namespace mode also requires NSZS and zero-valued reads.')
f(88,'LBACZ','只在 NSZ=1 且 Successful Completion 下，LBACZ=1 證明整個 namespace 已清零；0 只表示命令 range。','For NSZ=1 with Successful Completion, LBACZ=1 establishes whole-namespace zeroing; zero reports only the command range.')

f(90,'Notice 00h,Notice 05h,Notice 09h,Notice 0Ah','分別辨識 namespace attribute、LBA Status 與 Rate Limiting notices；NUSE 與 ANA capacity 特例不產生 attribute-change 通知。','Distinguish namespace-attribute, LBA Status, and Rate Limiting notices. NUSE and ANA capacity exceptions do not generate attribute-change notices.')
f(91,'PIL,PI,MSET','PI 選 protection type，MSET 選 metadata transfer；本版 PIL=0。Guard width 另由 LBAF／ELBAF 決定。','PI selects protection type and MSET metadata transfer; this revision requires PIL=0. LBAF/ELBAF separately determine Guard width.')
f(92,'FID,Scope,Persistence','讀 scope 與 buffer 需求，再看 persistence 註腳；對 saveable Feature 不使用本表 nonsaveable persistence 欄。','Read scope and buffer requirements, then the persistence footnote. The nonsaveable persistence column does not govern saveable Features.')
f(93,'Overlapping Range','只有 controller 實際檢查 LBA Range Type 且發現 overlap 時才必須回此錯誤；不可假設成功 Set 已完成全面驗證。','This error is required when the controller checks LBA Range Type and detects overlap. Successful Set does not imply comprehensive validation.')
f([94,95],'NUM','NUM low6 是 0-based：Set 時指定有效 entries，Get 時從 CQE DW0 讀實際回傳 entries；兩者都不是 byte count。','NUM low6 is zero-based: Set specifies valid entries and Get returns the count in CQE DW0. Neither is a byte count.')
f(96,'Type,ATTRB,SLBA,NLB,GUID','64-byte entry 分開描述用途、host hints 與 range；SLBA／NLB 是 logical blocks，GUID 是識別欄位，不是授權。','A 64-byte entry separates intended use, host hints, and range. SLBA/NLB describe logical blocks, while GUID identifies the range type rather than granting authorization.')
f(97,'DULBE,TLER','DULBE 是 bit16，TLER low16 以 100 ms 計；TLER=0 表示不限制 retry timeout，須由 recovery 起點計時。','DULBE is bit16 and TLER low16 uses 100 ms units. TLER=0 disables the retry timeout; timing begins when recovery starts.')
f(98,'DN','DN=1 只解除 normal atomicity 保證，power-fail atomicity 仍須遵守；這是 controller-scoped Feature。','DN=1 releases only normal-atomicity obligations; power-fail atomicity remains. This Feature has controller scope.')
f(99,'LBASIN,RLCCN','bits13／22 分別控制 LBA Status 與 Rate Limiting notices；取得 log 和清除事件還須依各 log 的 RAE 流程。','Bits13/22 control LBA Status and Rate Limiting notices respectively. Log retrieval and event clearing still follow each log’s RAE procedure.')
f(100,'LSIPI,LSIRI','high16 LSIPI 是不可改的 poll interval，low16 LSIRI 是 report interval；兩者均為 100 ms 單位，Set 回傳最接近可支援值。','High16 LSIPI is the unchangeable poll interval, low16 LSIRI the report interval. Both use 100 ms units; Set returns the nearest supported value.')
f(101,'LBAFEE','Host Behavior Support byte2 的 LBAFEE 允許 host 宣告延伸 LBA formats；只允許 0／1，並需對照 controller ELBAS。','LBAFEE at Host Behavior Support byte2 declares host extended-LBA-format support. Only zero/one are valid; also check controller ELBAS.')
f(102,'RVSPA,ATTRI','ATTRI low8 選擇標準、list 或 vendor attribute；bit8 RVSPA 刪除 saved vendor value，並非刪除整個 Feature。','ATTRI low8 selects standard, list, or vendor attributes. RVSPA bit8 deletes a saved vendor value, not the entire Feature.')
f(103,'R4KARL','R4KARL 是 latency bucket 而非直接時間；0Eh 是 50–100 μs 的半開區間，00h 為未回報。','R4KARL is a latency bucket rather than a direct time value. 0Eh is the half-open 50–100 μs interval, and 00h means unreported.')
f(104,'ATTRTYP,MSVSPA,USVSPA,PAID','ATTRTYP 應與 Get SEL 相符；用 MSVSPA／USVSPA 看 saved slots，再以每個 128-bit PAID 辨識 payload，不假設 slots 連續。','Match ATTRTYP to Get SEL. Use MSVSPA/USVSPA for saved slots and each 128-bit PAID to identify payloads; slots need not be contiguous.')
f(105,'PAID,ATTRL,VS','PAID 指出 vendor payload 的定義，ATTRL 限制有效 VS bytes，最大 FE0h；未知 PAID 不應由標準表格猜測。','PAID identifies the vendor payload definition and ATTRL bounds valid VS bytes, at most FE0h. Do not invent a standard decoding for an unknown PAID.')
f(106,'TGT,TID','先辨識 TGT 再解讀 TID；TGT=0 使用 controller ID，不能指定 Admin controller、無效 ID 或 FFFDh..FFFFh。','Interpret TID after TGT. TGT=0 uses a controller ID and excludes Admin controllers, invalid IDs, and FFFDh..FFFFh.')
f(107,'RLE,RLM,BWSF,TBWV,WBWV,TIOPS,WIOPS,WRIOPSR,WRBWR','1024-byte 設定分出 enable/mode、兩種 bandwidth、兩種 IOPS 與兩個 write/read ratios；加權 total consumption 與 write-only consumption 分開計。','The 1024-byte configuration separates enable/mode, two bandwidth limits, two IOPS limits, and two write/read ratios. Calculate weighted total and write-only consumption separately.')
f(108,'BWSF,MBSF,ABWSF','共同 scale 表供設定、maximum 與 available bandwidth 使用；0..2 是 MiB/s 階梯，3..5 是 GiB/s 階梯。','The shared scale table applies to configured, maximum, and available bandwidth. Values 0..2 are MiB/s scales and 3..5 GiB/s scales.')
f(109,'LID,CSI,Scope,Restore behavior','log 表列出 NVM 補充及 scope／CSI；28h 使用 CSI，restore-to-default 欄也不能當成一般 reset persistence。','The log index lists NVM extensions, scope, and CSI applicability. 28h uses CSI; restore-to-default behavior is not ordinary reset persistence.')
f(110,'LBA','Error Information bytes23:16 是適用時最低錯誤 LBA；需與原命令與 namespace 相連，不當成全 subsystem 的 byte address。','Error Information bytes23:16 contain the lowest erroneous LBA when applicable. Associate it with the original command and namespace, not a subsystem-wide byte address.')
f(111,'FLBA,FLBA Valid','FLBA 只有 valid bit=1 時可用；多個失敗 blocks 時只需回一個，與 Error Information 的最低 LBA 定義不同。','Use FLBA only when its valid bit is one. One failing block may represent several failures, unlike Error Information’s lowest-LBA rule.')
f(112,'FLBAS,DPS','create 取 host-specified values，single delete 取被刪 namespace 的 Identify 值；delete all 時兩欄 reserved。','Create records host-specified values, single-delete records the deleted namespace’s Identify values, and delete-all reserves both fields.')
f(113,'LSLPLEN,NLSLNE,ESTULB,LSGC','先讀 bytes 長度與 namespace-element 數；NLSLNE=0 且 ESTULB 非零仍有需調查範圍，LSGC 是 16-bit 可回繞 counter。','Read byte length and namespace-element count first. NLSLNE=0 with nonzero ESTULB still warrants investigation; LSGC is a wrapping 16-bit counter.')
f(114,'NEID,NLRD,RATYPE','NEID 定位 namespace，RATYPE 建議後續 Get LBA Status 的 ATYPE；NLRD=FFFFFFFFh 表示無 range list 且宜檢查全 namespace。','NEID identifies the namespace and RATYPE recommends the later Get LBA Status ATYPE. NLRD=FFFFFFFFh means no range list is available and the whole namespace should be examined.')
f(115,'RSLBA,RNLB','每筆 16-byte range 用 RSLBA 與 0-based RNLB；它是 log 提供的粗範圍，還不是 Get LBA Status 的最終 status descriptor。','Each 16-byte range uses RSLBA and zero-based RNLB. It is a coarse log range, not the final status descriptor from Get LBA Status.')
f(116,'LBAV,NLBAM,LBA','先驗 LBAV 再使用 LBA；NLBAM=0 未回報數量、FFFFh 表示至少該數量，不是一定恰好搬移 65535 blocks。','Validate LBAV before using LBA. NLBAM=0 means unreported and FFFFh means at least that many, not exactly 65535 moved blocks.')
f(117,'NP,LPL,GC,NST,Port offsets','NP／NST 是 0-based，LPL 是 dwords，port 指標也以 log 起點的 dwords 表示；讀完整 log 後重驗 GC。','NP/NST are zero-based, LPL is dwords, and port pointers are dword offsets from the log start. Recheck GC after collecting the log.')
f(118,'PORTID,NC,RLMA,ARBWV,AWBWV,ARIOPS,AWIOPS','port descriptor 的 available 指尚未分配額度，與 RLMA 的 maximum 不同；controller-list offset 仍相對整份 log。','Available fields in a port descriptor report unassigned capacity, distinct from RLMA maximums. Controller-list offsets remain relative to the whole log.')
f(119,'CNTLID,NNSMAD,RLMA,Access offsets','controller descriptor 以實際 NNSMAD 指出 access descriptors 數；這個 count 不採 NP／NC 的加一規則。','A controller descriptor gives the actual access-descriptor count in NNSMAD. It does not use NP/NC add-one decoding.')
f(120,'SC,SI,NNSMAD,RLMA','先以 SC 選 scope 再解讀 SI 與巢狀 access list；本表 SI 說明仍提 NSET 且 byte 例子錯置，應以 SC 與表列 bytes7:4 定位。','Select scope with SC before interpreting SI and nested access lists. The SI prose still mentions NSET and misplaced example bytes; SC and the tabulated bytes7:4 provide the field location.')
f(121,'MBSF,MRBWV,MWBWV,MRIOPS,MWIOPS','以 MBSF 轉 bandwidth；四個 maximum 需配合 workload size 與 queue depth，不能當成任意 workload 的最低保證。','Scale bandwidth using MBSF. The four maximums depend on workload size and queue depth and are not minimum guarantees for arbitrary workloads.')
f(122,'CNS,NSID,CSI,CNTID','以 CNS 選資料結構，再看 NSID／CSI 是否使用；00h、05h、08h 的 namespace 資訊互補，09h／0Ah 用 FIDX。','Select the structure with CNS, then check NSID/CSI applicability. Namespace information from 00h, 05h, and 08h is complementary; 09h/0Ah use FIDX.')
f(123,'NSZE,NCAP,NUSE,NSFEAT,NLBAF,FLBAS,MC,DPC,DPS,DLFEAT,Atomicity,Performance hints,Copy limits,Identifiers','把這張跨頁資料結構分成容量、格式能力／目前格式、deallocation、atomicity、performance、Copy limits 與識別資料七組；每組先看 capability gate 再使用數值。','Partition this multipage structure into capacity, format capability/current format, deallocation, atomicity, performance, Copy limits, and identifiers. Apply each capability gate before using its values.')
f(124,'OPTPERF,NPWG,NPWA,NPDG,NPDGL,NPDAL,NOWS','OPTPERF 是 2-bit selector：不同值啟用不同 small／large deallocate 欄位組；不是一個通用的 performance enabled bit。','OPTPERF is a two-bit selector enabling different small/large deallocate-field sets, not a universal performance-enable bit.')
f(125,'LBADS,MS,RP','LBADS 為 exponent，MS 為實際 metadata bytes，RP 為相對效能級別；LBADS=0 是目前不可用，不能解成一個 byte 或 512 bytes。','LBADS is an exponent, MS an actual metadata-byte count, and RP a relative performance class. LBADS=0 means currently unavailable, not one byte or 512 bytes.')
f(126,'AWUN,AWUPF,ACWU','controller atomicity 值供適用 namespaces 使用；namespace capability 可覆寫，AWUPF 不大於 AWUN，ACWU 專供 fused Compare-and-Write。','Controller atomicity values apply unless qualified namespace values override them. AWUPF does not exceed AWUN; ACWU specifically governs fused Compare-and-Write.')
f(127,'LBSTM,PIC,PIFA,ELBAF,NPDGL,NPRG,NPRA,NORS,NPDAL,LBAPSS,TLBAAG','延伸 namespace 結構把 PI／mask 能力、每-format ELBAF 與性能／allocation hints 分開；NPRG／NPRA／NORS 受 OPTRPERF 限制。','The extended namespace structure separates PI/mask capabilities, per-format ELBAF, and performance/allocation hints. OPTRPERF gates NPRG/NPRA/NORS.')
f(128,'QPIF,PIF,STS','PIF=11b 且支援 QPIFS 才使用 QPIF；STS 是 bits count，切分固定寬度的 Storage/Reference Space，沒有增大 PI。','QPIF applies when PIF=11b and QPIFS is supported. STS counts bits dividing a fixed-width Storage/Reference Space; it does not enlarge PI.')
f(129,'VSL,WZSL,WUSL,DMRL,DMRSL,DMSL,KPIOCAP,WZDSL,AOCS,VER,LBAMQF,RLA,SLMC','本表實際延伸到文件頁106，不能只讀有 caption 的103頁。Size limits 要結合 ONCS variants；SLMC 是 0-based，VER 為 command-set 版本。','This table continues through printed page106, not just captioned page103. Size limits require ONCS variants; SLMC is zero-based and VER identifies the command-set version.')
f(130,'MJR,MNR,TER','1.3 對應 MJR=1、MNR=3、TER=0；此為 NVM command-set version，與 Base version 另記。','Revision 1.3 maps to MJR=1, MNR=3, TER=0. Record this command-set version separately from the Base version.')
f(131,'FIDX','CNS09h／0Ah 的 CDW11 low16 是 Format Index，不能同時當成某個 namespace ID；CSI 另選 command set。','For CNS09h/0Ah, CDW11 low16 is Format Index rather than a namespace ID; CSI separately selects the command set.')
f(132,'GDM,ND,NGD','GDM=0 時 descriptor0 套全部格式，ND=0；GDM=1 以相同 index 對應 format。ND 是 0-based，支援數量受 LBAFEE 影響。','GDM=0 applies descriptor0 to all formats and uses ND=0. GDM=1 maps matching indices to formats. ND is zero-based and LBAFEE affects the supported count.')
f(133,'NSG,NCG','NSG／NCG 以 bytes 表示 preferred allocation granularity；0 表示未回報，不能拿來做除法或要求 namespace 大小為零。','NSG/NCG report preferred allocation granularity in bytes. Zero means unreported, not a divisor or a requirement for zero namespace size.')
f(134,'NSZE,NCAP,FLBAS,DPS,NMIC,ANAGRPID,NVMSETID,ENDGID,LBSTM,NPHNDLS,RUH list','Create payload 只有指定欄位可由 host 填寫；LBSTM／placement list 不在基本 Identify 相同區段，不能直接 memcpy 整份 Identify 結構。','Only designated create-payload fields are host-specified. LBSTM/placement-list locations differ from the basic Identify area, so copying an entire Identify structure is incorrect.')
f(137,'MNDW','MNDW 是 0-based 最大 dword 數；buffer bytes=(MNDW+1)×4，實際回量再看 NLSD。','MNDW is the zero-based maximum dword count: buffer bytes=(MNDW+1)×4. NLSD determines the actual returned descriptor count.')
f(138,'ATYPE,RL','ATYPE=02h／10h／11h 選 allocated／scan／tracked 行為；RL=0 是從 SLBA 到 namespace 最後 LBA，不是零長度。','ATYPE=02h/10h/11h selects allocated/scan/tracked behavior. RL=0 runs from SLBA through the final namespace LBA rather than requesting zero length.')
f(139,'NLSD,CMPC','8-byte header 後跟 16-byte descriptors；NLSD 是實際數量。CMPC=1 表示資訊尚未完整，即使 CQE 已成功。','An eight-byte header precedes 16-byte descriptors; NLSD is an actual count. CMPC=1 means information is incomplete even if the CQE succeeded.')
f(140,'DSLBA,NLB,LBARS','NLB 是 0-based；LBARS=010b 適用 ATYPE02h，表示至少一個 block 已配置，不表示每個 block 都獨立配置。','NLB is zero-based. LBARS=010b applies to ATYPE02h and means at least one block is allocated, not that every block is individually allocated.')
f(141,'ANA state,FID 05h,NUSE,NVMCAP','按 command 與 ANA state 交叉查：FID05h 的 Get／Set 限制列並不完全相同，Identify 的容量回零只描述報告值。','Cross-reference command and ANA state. FID05h Get/Set restrictions differ; Identify capacity zeroing describes reported values only.')
f(142,'NEID,NLRD,RATYPE,RSLBA,RNLB','示例 namespace element 指出兩段候選 ranges 與 RATYPE=11h；這是後續查詢輸入，不是每個候選 block 的最終診斷。','The example namespace element supplies two candidate ranges and RATYPE=11h as input to later queries, not a final diagnosis for every candidate block.')
f([143,144],'NLSD,DSLBA,NLB,CMPC','同一 log range 可由後續 Get LBA Status 產生不同數量的精細 descriptors；以實際 NLSD、NLB 與 CMPC 判斷是否需要續查。','A log range can yield different numbers of detailed Get LBA Status descriptors. Use actual NLSD, NLB, and CMPC to determine whether follow-up is needed.')

f(145,'NOIOB,Conformant range,Crossing range','最佳 I/O boundary 的示意獨立於 atomic boundary；跨線命令可分割以符合建議，但分割本身會增加命令數。','The optimal-I/O boundary illustration is independent of atomic boundaries. Splitting crossings can meet recommendations while increasing command count.')
f(146,'NABO,NABSN','在 namespace 起點之外另標 atomic offset；不能把所有 boundaries 都預設從 LBA0 開始。','Mark the atomic offset separately from the namespace origin; not all boundaries necessarily start at LBA0.')
f(147,'NPWA,NPWG','NPWA 指起點，NPWG 指長度 granularity；示意的 8 blocks 是解碼後大小，並非 raw field=8。','NPWA governs the start and NPWG the length granularity. The illustrated eight blocks are a decoded size, not raw field value eight.')
f(148,'NPRA,NPRG','讀取 alignment 與 granularity 分開，示例為 4-block alignment 與 8-block granularity；較短且錯位的讀取可能影響效能。','Read alignment and granularity differ: the example uses four-block alignment and eight-block granularity. Short misaligned reads may affect performance.')
f(149,'Old prefix,New data,Old suffix','只更新 8-block unit 中的 3 blocks，示例需讀回前後共 5 blocks 舊資料再合成；這是可能的 read-modify-write 成本。','Updating only three blocks of the illustrated eight-block unit requires reading five old prefix/suffix blocks before combining them: a possible read-modify-write cost.')
f(150,'Aligned start,Full granularity','示意同時滿足 NPWA 與 NPWG 的範圍，可避免範例中的頭尾補讀；不是對所有硬體保證沒有任何內部讀取。','The illustrated range satisfies NPWA and NPWG and avoids the example’s edge reads. It does not guarantee that all hardware performs no internal reads.')
f(151,'Misaligned start,Full length','長度剛好一個 NPWG，起點仍可能錯位而觸及兩個 units；只檢查 length modulo NPWG 不足。','A length of exactly one NPWG can still touch two units when misaligned. Checking length modulo NPWG alone is insufficient.')
f(152,'SGS,SWS,Stream granularity','以 SGS 個 SWS units 組成 stream granularity；寫入依 SWS、stream deallocate 依較大 granularity 協調。','A stream granularity contains SGS units of SWS. Coordinate writes with SWS and stream deallocation with the larger granularity.')
f(153,'Data,Metadata,DPTR','extended LBA 依序排列每個 block 的 data 後接 metadata；不可把全部 data 排完才接全部 metadata。','Extended LBAs place metadata immediately after each block’s data, not all data first followed by all metadata.')
f(154,'Data buffer,Metadata buffer,MPTR','separate 模式保留 data 與 metadata 兩個 buffer 並保持 block 對應；不是把 metadata 任意重排成無序清單。','Separate mode uses distinct data/metadata buffers with block correspondence, not an arbitrarily reordered metadata list.')
f(155,'Guard16,Application16,Reference32','STS=0 的 8-byte PI 由 16-bit Guard、16-bit Application 與 32-bit Reference 組成，各欄位依圖採高位在前。','With STS=0, eight-byte PI contains a 16-bit Guard, 16-bit Application, and 32-bit Reference field, with most-significant bytes first as shown.')
f(156,'Guard16,Application16,StorageReference32','加入 Storage Tag 後仍維持 8 bytes；只把原先的 32-bit Reference space 切開，不在末端追加新 bytes。','Adding Storage Tag keeps PI at eight bytes by dividing the 32-bit Reference space rather than appending new bytes.')
f(157,'Guard32,Application16,StorageReference80','32b Guard 的 16-byte PI 留 80 bits 給 Storage／Reference；STS 至少 16，Reference 至少保留 16 bits。','16-byte PI with 32b Guard leaves 80 bits for Storage/Reference. STS is at least 16, leaving at least 16 Reference bits.')
f(158,'Zero vector,FF vector,Incrementing bytes,CRC32C','用四組 4 KiB vectors 驗證 CRC32C，而非只驗證全零；incrementing／decrementing patterns 更容易找出順序錯誤。','Validate CRC32C with all four 4 KiB vectors, not zeros alone. Incrementing/decrementing patterns help expose ordering errors.')
f(159,'Guard64,Application16,StorageReference48','64b Guard 的 PI 雖與 32b Guard 同為 16 bytes，Storage／Reference 只剩 48 bits；不能複用 80-bit 切分。','64b Guard PI is also 16 bytes, but only 48 bits remain for Storage/Reference. Do not reuse the 80-bit split from 32b Guard.')
f(160,'F(x),G(x),R(x),CRC checking','以 GF(2) 的 polynomial remainder 解釋 CRC；實際 NVM CRC64 仍需套用後續 Figure161 的 init、reflection 與 XOR 參數。','Polynomial remainders over GF(2) explain CRC, while actual NVM CRC64 also requires the initialization, reflection, and XOR parameters in Figure161.')
f(161,'Width64,Poly,Init,RefIn,RefOut,XorOut,Check','完整參數組才辨識 NVM CRC64：Poly=AD93D23594C93659h、Init／XorOut 全一、RefIn／RefOut=true。此圖 Check=11199E506128D175h 是常見 LSB-first register 結果 AE8B14860A799888h 的 64-bit 反轉；以 Figure 163 向量交叉驗證表示方式。','The full set identifies NVM CRC64: Poly=AD93D23594C93659h, all-ones Init/XorOut, RefIn/RefOut=true. Its Check=11199E506128D175h is the 64-bit reversal of the conventional LSB-first register result AE8B14860A799888h. Cross-check representation using Figure 163 vectors.')
f(162,'Byte order,Reflected bits,Message body','逐 byte 的 bits 0..7 對應 reflected input；不要把圖中顯示順序誤當 host integer 的原生 endian。','Bits0..7 of each byte illustrate reflected input. Do not confuse diagram order with a host integer’s native endianness.')
f(163,'Zero vector,FF vector,Incrementing bytes,CRC64','核對四組 CRC64 vectors 與 command-set 指定參數；十六進位分組樣式不改變數值，但不可自行補或刪除 hex digits。','Check all four CRC64 vectors against the command-set parameters. Hex grouping does not change the number, but adding or removing digits does.')
f(164,'STS,Storage Tag,Reference Tag','高 STS bits 是 Storage Tag，低剩餘 bits 是 Reference Tag；某一側可依合法 STS 不存在。','High STS bits form Storage Tag and remaining low bits Reference Tag; either can be absent for an allowed STS.')
f(165,'PI format,STS,Tag width','以各格式總 space 減 STS 得 Reference width：32b Guard 是 80−STS，並不是 32−STS。','Subtract STS from each format’s total space to obtain Reference width: 32b Guard uses 80−STS, not 32−STS.')
f(166,'CDW2,CDW3,CDW14,StorageReferenceSpace','用最多 80-bit 的抽象 space 連接三個 Dwords；依 PI format 先去掉 unused bits，再切 storage／reference。','Map the abstract space of up to 80 bits across three Dwords. Remove format-specific unused bits before splitting storage/reference.')
f(167,'PI format,Used bits,Ignored bits','此表列出每個 Guard 格式實際使用的命令 bits；unused 不等於可自行定義的新欄位。','This table lists command bits actually used by each Guard format. Unused bits are not new implementation-defined fields.')
f([168,169],'STS=0,CDW14,Reference32','16b Guard 且 STS=0 時只有 CDW14 的 32-bit initial／expected reference；範例 LBADS 應依 Figure125 的 exponent 定義判讀。','With 16b Guard and STS=0, CDW14 alone carries the 32-bit initial/expected reference. Interpret the example’s LBADS through Figure125’s exponent definition.')
f([170,171],'Storage32,Reference48,CDW2,CDW3,CDW14','STS=32 的 80-bit space 先放 Storage32 再放 Reference48；CDW3 high16 屬 Storage、low16 屬 Reference。Figure171 的重疊 range 需交叉查 Figure166／170。','The 80-bit space with STS=32 contains Storage32 followed by Reference48. CDW3 high16 belongs to Storage and low16 to Reference; cross-check Figure171’s overlapping range against Figures166/170.')
f([172,173],'Storage18,Reference30,CDW3,CDW14','48-bit space 且 STS=18 時，Storage 低2 bits 進 CDW14 high2，其餘 Reference30 佔 CDW14 low30。','With a 48-bit space and STS=18, the low two Storage bits occupy CDW14 high2 and Reference30 occupies CDW14 low30.')
f(174,'Write,PRACT,MS,PI','Write PRACT=0 保留 host PI；PRACT=1 在 MS=PI 時插入、MS>PI 時取代。生成 PI 的分支忽略 checking bits。','Write PRACT=0 preserves host PI. PRACT=1 inserts when MS=PI and replaces when MS>PI; the PI-generation branch ignores checking bits.')
f(175,'Read,PRACT,MS,PI','Read 先依要求檢查；PRACT=1 且 MS=PI 才 strip，MS>PI 則仍把 PI 隨 metadata 回傳。','Read performs requested checks first. PRACT=1 strips PI only when MS=PI; with MS>PI, PI is still returned within metadata.')
f(176,'Host input,Media input,PI checks,Compare','Compare 的 host 與 media 輸入各有 PI checking；一般比較涵蓋 data 與非 PI metadata，不能只比對 PI 就宣告內容相同。','Compare performs PI checks on both host and media inputs. Ordinary comparison covers data and non-PI metadata; comparing PI alone does not establish equal contents.')
f([177,178],'PRINFOR.PRACT=0,PRINFOW.PRACT=0,Pass-through','這兩圖是 matching PI formats 的 pass-through：讀／寫 PRACT 都為0；metadata 大小不同的兩個例子仍須保留各自 layout。','These are pass-through examples for matching PI formats with both PRACT bits zero. The two metadata-size examples retain their distinct layouts.')
f([179,180],'PRINFOR.PRACT=1,PRINFOW.PRACT=1,Replace','這兩圖是 matching PI formats 的 replace：讀／寫 PRACT 都為1；來源 PI 檢查與目的 PI 產生有不同角色。','These are replace examples for matching PI formats with both PRACT bits one. Source PI checking and destination PI generation have distinct roles.')
f(181,'Source no PI,Destination PI,Insert','只有 corresponding PI formats 且 destination metadata 全為 PI 時使用 insert 特例，write PRACT 必須1。','Use the insert exception only with corresponding PI formats and PI-only destination metadata; write PRACT must be one.')
f(182,'Source PI,Destination no PI,Strip','只有 corresponding PI formats 且 source metadata 全為 PI 時使用 strip 特例，read PRACT 必須1。','Use the strip exception only with corresponding PI formats and PI-only source metadata; read PRACT must be one.')
f(192,'NLBAF,NULBAF,Format Index','先把 raw NLBAF 加1成共同格式數，再加 NULBAF；unique attributes 區緊接在共同區之後。','Decode raw NLBAF by adding one, then add NULBAF. Unique-attribute formats immediately follow the common-format region.')
f(193,'CNS00h,CNS05h,CNS08h,CNS09h,CNS0Ah','共同能力查詢與 per-format 查詢覆蓋的格式集合不同；09h／0Ah 可查 NULBAF 定義的 unique-attribute entries。','Common-capability and per-format queries cover different format sets. 09h/0Ah can query unique-attribute entries defined by NULBAF.')
f(194,'NSID,NLB,SLBA,LBACIR,DLBA,ESA,CDQP','32-byte entry 最後一 byte 含範圍有效性、deallocation、sequence 與 phase；先看 LBACIR 再用 SLBA／NLB，NLB 是0-based。','The final byte of a 32-byte entry carries range applicability, deallocation, sequence, and phase. Check LBACIR before using SLBA/NLB; NLB is zero-based.')
f(195,'Port,Controller0,Controller1,EnduranceGroup1,EnduranceGroup2','這是共享節點的 graph，不是單一樹；同一 EG 可被兩個 controllers 引用，且不能因此重算共享媒體能力。','This is a graph with shared nodes, not a tree. Two controllers may reference one EG without doubling its shared media capability.')
f(196,'Dword offsets,Byte ranges,LPL,Shared descriptors','以 Figure195 重畫關係；來源示例把 dword offset299 寫成 byte1916，但299×4=1196，且其他範圍也不一致，必須做 bounds 檢查。','Redraw the relationships from Figure195. The source labels dword offset299 as byte1916, although 299×4=1196, and other ranges also conflict. Bounds checks are essential.')
f(197,'PCIe Port0,PCIe Port1,Shared Endurance Group','雙 port 的 transport 能力不會複製 shared EG 的媒體能力；由同一 storage bottleneck 解釋競爭。','Two ports do not duplicate the media capability of their shared EG; analyze contention at the shared storage bottleneck.')
f(198,'Port descriptors,Controller descriptors,Shared access,LPL','保留双 port 共用一個 storage node 的關係；原範例 LPL=570 dwords 但列出超出2280 bytes的結構，因此不可當成有效輸入樣本。','Preserve the two-port/shared-storage relationship. The example gives LPL=570 dwords while listing structures beyond 2280 bytes, so it is not a valid input fixture.')
f(199,'Reservation type,Holder,Registrant,Command','逐列區分 read-like／write-like 命令，再按 holder／registration 與 reservation type 判斷；不可把所有非 holder 視為相同。','Classify read-like/write-like commands, then apply holder/registration state and reservation type. Nonholders do not all have identical permissions.')
f(200,'Get Log Page,Error Information,LBA','NVM 這張 Figure200 補充 sanitize 期間 Error Information 的 LBA 回0；它不是 Base 同號的 Feature 表，也不能取代 Base 的允許命令清單。','NVM Figure200 adds zero-valued Error Information LBA during sanitize. It is not the Base Feature table with the same number and does not replace the Base permitted-command list.')
f(201,'Block Erase,Crypto Erase,Overwrite','保留已配置 media 的成功 sanitize 回值依方法不同；若已 deallocate，改採 deallocated-read 規則，不將任何方法一概寫成全零。','Successful sanitize values on allocated media depend on the method. Deallocated blocks follow deallocated-read rules; no universal all-zero result is implied.')
f(202,'Token supply,Queued commands,Admission,Internal resource','Token 不足讓命令等候；可處理部分但整筆完成才發布 CQE。此圖為 informative implementation example，不是唯一排程演算法。','Insufficient tokens make commands wait. Partial processing is possible, but CQE publication follows complete processing. This is an informative implementation example, not the only scheduler.')

f(80,'Attempted Write to Read Only Range','Write Uncorrectable 的本表只列 Attempted Write to Read Only Range；不能把其他命令的 PI 狀態集合套進來。','This Write Uncorrectable table lists Attempted Write to Read Only Range only; do not import other commands’ PI status sets.')
f(183,'RECCS,RENSCS','先分固定 364-byte controller configuration 與 48-byte namespace configuration；總長 412 bytes，僅能單筆設定一次。','Separate the fixed 364-byte controller configuration from the 48-byte namespace configuration: 412 bytes total, set once in one command.')
f(184,'CSS,TO,CQR,MQES','未列出的 CAP bits 清零；CSS 表示僅 NVM，TO=FFh 表示 127.5 秒，queues 要 physically contiguous，MQES 受 underlying 限制。圖中 CQE 名稱對應 contiguous-queue 欄位。','Unlisted CAP bits are zero. CSS indicates NVM only, TO=FFh means 127.5 seconds, queues must be physically contiguous, and MQES is bounded by the underlying controller. The figure labels the contiguous-queue field CQE.')
f(185,'MJR,MNR,TER','範本的 VS 固定 020300h，即 2.3.0；不要因手上的 Base 版本為 2.4 就改成 2.4。','The template fixes VS=020300h, meaning 2.3.0; do not change it to 2.4 because that is the supplied Base revision.')
f(186,'AFI,FRS1','Active firmware slot 固定為 1；其餘 firmware log 值依零值規則及 configuration state 的 FR exception。','The active firmware slot is fixed to 1. Other firmware-log values follow the zeroing rule and the configuration-state FR exception.')
f(187,'TMPSEL,THSEL,TMPTH,IV,CD,NCQS,NSQS','Composite over／under 預設 FFFFh／0；IV=0 的 CD=1，其他 IV 的 CD=0。Number of Queues 取決於請求與配置結果，不是固定零。','Composite over/under thresholds default to FFFFh/0. IV=0 has CD=1, other vectors CD=0. Number of Queues depends on requested and allocated counts, not a fixed zero.')
f(188,'NSZE,NCAP,NSFEAT,VER,SQES,CQES,NGUID,UUID','Identify 只開放列出的 exceptions：NCAP=NSZE、SQES=66h 為 64-byte SQE、CQES=44h 為 16-byte CQE；CNS06h 的 NVM VER 固定 1.2.0。','Identify permits the listed exceptions: NCAP=NSZE, SQES=66h for 64-byte SQEs, CQES=44h for 16-byte CQEs, and NVM VER=1.2.0 in CNS06h.')
f(189,'ECNTLID,MDTS,RAB,NCQS,NSQS,MQES,ONCS,AWUN,AWUPF','本機欄位 slice：ECNTLID=0，限制值不得超過 underlying；NCQS／NSQS 先解 0-based。WZS／DSMS 需對應底層能力與所報 Commands Supported and Effects。','Local-field slice: ECNTLID=0 and limits must not exceed underlying support. Decode zero-based NCQS/NSQS. WZS/DSMS must correspond to underlying support and reported Commands Supported and Effects.')
f(190,'ENSID,LBAF0,NAWUN,NAWUPF,NGUID,NUUID','caption 雖寫 Controller，內容是 namespace：ENSID=1、MS=0、RP=0；LBADS 必須與 underlying 相同。NGUID=0 時 NUUID 必須有效。','Despite Controller in the caption, this is namespace configuration: ENSID=1, MS=0, RP=0, with LBADS matching the underlying namespace. A zero NGUID requires a valid NUUID.')
f(191,'Feature values,CSATTR.CP,NVMECSS,NVMECS','固定 header 為 64 bytes，後接 NVMECSS×4 bytes 的 NVMECS；零長度時欄位不存在。CP=1 只證明整段 Receive 期間 suspended，內層 VER 須為 1h。','A 64-byte header precedes NVMECSS×4 bytes of NVMECS, absent at zero length. CP=1 establishes suspension throughout Receive processing; nested VER must be 1h.')

BASE_DETAILS = {
 93: ('READ-WRITE','OPC,NSID,MPTR,DPTR,CDW10-15', b('Common SQE 將 namespace、data pointers 與 command-specific Dwords 分開；NVM 章節只補充相應 command fields。','The common SQE separates namespace, data pointers, and command-specific Dwords; NVM sections supply the corresponding command fields.')),
 97: ('SUPPORT-STATUS','DW0,DW1,SQHD,SQID,CID,Status', b('CQE 的 command-specific result 與共同 queue／status 資訊各有位置；Copy DW0 與 Write Zeroes DW0 使用不同意義。','CQE command-specific results have separate locations from common queue/status information. Copy DW0 and Write Zeroes DW0 have different meanings.')),
 98: ('SUPPORT-STATUS','SQHD,SQID', b('DW2 的 SQHD／SQID 回報對應 submission queue 資訊，不能當作此次命令已傳輸的 byte count。','DW2 SQHD/SQID report submission-queue information, not the byte count transferred by this command.')),
 99: ('SUPPORT-STATUS','CID,Status', b('DW3 以 CID 配回命令、Status 判定結果；command-specific DW0 不取代 status。','DW3 associates completion through CID and reports its result through Status; command-specific DW0 does not replace Status.')),
 101: ('SUPPORT-STATUS','SCT,SC,DNR,P', b('Status 要一併解讀 SCT／SC，DNR 用於重試判斷，phase 用於辨識新 completion；它們回答不同問題。','Interpret SCT/SC together, DNR for retry guidance, and phase for a new completion; these fields answer different questions.')),
 110: ('READ-WRITE','PRP,Page base,Offset', b('PRP layout 包含頁基址與首筆 offset；NVM payload 可能是 data 或 descriptor list，不能由 pointer 類型推定內容。','PRP layout contains a page base and first-entry offset. NVM payload can be data or a descriptor list; pointer type does not determine content.')),
 111: ('READ-WRITE','Page size,PRP offset', b('頁大小決定 base／offset 切分。計算第一頁剩餘空間後才決定後續 PRP pages。','Page size determines the base/offset split. Calculate the first page’s remaining space before mapping subsequent PRP pages.')),
 116: ('READ-WRITE','SGL descriptor,Address,Length,Type', b('本機 SGL descriptor 用 address、length 與 type 描述 buffer；保留 generic layout，不展開其他 transport 的 descriptor types。','A local SGL descriptor describes a buffer with address, length, and type. This slice retains the generic layout without expanding other transport descriptor types.')),
 338: ('IDENTIFY','ONCS,CTRATT,MDTS,SANICAP', b('NVM 需要 Base Identify 的 ONCS variants、CTRATT.ELBAS／MEM、MDTS 與 SANICAP 等能力；本 slice 不展開其餘跨頁欄位。','NVM uses Base Identify capabilities including ONCS variants, CTRATT.ELBAS/MEM, MDTS, and SANICAP. This slice does not expand the remaining multipage fields.')),
 346: ('IDENTIFY','NSID,NSATTR,NMIC,RESCAP,ANAGRPID', b('CNS08h 提供 command-set-independent namespace 屬性，與 NVM CNS00h／05h 組合；不應只依其中一份結構推論全部能力。','CNS08h provides command-set-independent namespace attributes and combines with NVM CNS00h/05h. No single structure establishes every capability.')),
 491: ('COPY','CFD2E,CFD3E', b('Host Behavior Support 的 CFD2E／CFD3E 宣告 host 接受 Copy formats2h／3h；controller CDF support 與 host enablement 是兩項門檻。','Host Behavior Support CFD2E/CFD3E declare host acceptance of Copy formats2h/3h. Controller CDF support and host enablement are separate gates.')),
 312: ('SANITIZE','SPROG,SSTAT,SCDW10,SANS', b('Sanitize Status 提供 operation 的進度、結果、起始命令及 state；成功的啟動 CQE 無法取代這份 log。','Sanitize Status supplies operation progress, outcome, initiating command, and state. A successful initiating CQE cannot replace this log.')),
 451: ('SANITIZE','SANACT,AUSE,NDAS,EMVS,PREQ', b('Subsystem Sanitize 的 CDW10 分開方法及修飾 bits；本教學只把 NVM §4.1.7 的 Base 命令相依補齊。','Subsystem Sanitize CDW10 separates method from modifiers. This worksheet supplies the Base command dependency of NVM §4.1.7.')),
 452: ('SANITIZE','OVRPAT', b('CDW11 的 OVRPAT 是 Overwrite pattern；不是所有 SANACT 都使用此值，也不能套用於 Crypto Erase 的讀值預期。','CDW11 OVRPAT is the Overwrite pattern. Not every SANACT uses it, and it does not define Crypto Erase read values.')),
 561: ('MIGRATION-QUEUE','MOS,MO', b('Track Send CDW10 先選 management operation，MOS 再依 operation 解讀；NVM 的本範圍使用 Log User Data Changes。','Track Send CDW10 selects a management operation before MOS is interpreted. This NVM scope uses Log User Data Changes.')),
 562: ('MIGRATION-QUEUE','LACT', b('LACT 控制開始／停止 user-data changes logging；必須配合 CDQID 指定已建立的 LBA Migration Queue。','LACT controls starting/stopping user-data change logging and must be combined with CDQID for a created LBA Migration Queue.')),
 563: ('MIGRATION-QUEUE','CDQID', b('CDQID 是 controller data queue identifier；不是 NSID 或 SQID，識別此次變更記錄送往哪個 queue。','CDQID identifies the controller data queue, not NSID or SQID, selecting the destination for change records.')),
 712: ('STREAMS','SWS,SGS', b('只讀 Streams Return Parameters 的 SWS／SGS 相依 slice；NVM §5.13 將 SWS 的 command-set 單位定義為 logical blocks。','Read only the SWS/SGS slice of Streams Return Parameters. NVM §5.13 defines the command-set unit of SWS as logical blocks.')),
}


def detail(figure):
    n=int(figure['number'])
    if figure['source_id']=='NVME-NVM-CS-1.3':
        return DETAILS[n]
    key, fields, text=BASE_DETAILS[n]
    return dict(key_items=fields.split(','), text=text, key=key)


def guide_for(figure, language):
    return detail(figure)['text'][language]


def lesson_for(figure):
    if figure['source_id']=='NVME-BASE-2.4':
        key=BASE_DETAILS[int(figure['number'])][0]
        return next(m for m in MODULES if m['sources']==['NVMCS13-'+key])
    return next(m for m in MODULES if int(figure['number']) in m['figures'])


def expanded_guide(figure, language):
    data=detail(figure); m=lesson_for(figure); en=language=='en'
    terms=[(field, definition(field, language)) for field in data['key_items'] if field in TERMS]
    other=[field for field in data['key_items'] if field not in TERMS]
    if other:
        terms.append(('Related fields' if en else '相關欄位', ', '.join(other)+' — '+data['text'][language]))
    return dict(kind='layout', context=data['text'][language],
        kind_text=('Field relationships and a worked interpretation, redrawn for this source and revision.' if en else '依本來源與版本重整欄位關係，配合解碼案例閱讀。'),
        terms=terms,
        steps=[('Locate the cited page range and identify raw versus decoded units.' if en else '定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。'),
               data['text'][language], m['lead'][language],
               ('Apply the scenario below and retain the original command, target, and result.' if en else '套用下方情境，保存原命令、target 與結果。')],
        answers=[['Interpretation' if en else '判讀', data['text'][language]], ['Boundary' if en else '邊界',m['pitfall'][language]]],
        example=m['example'][language], debug=[['Debug',m['pitfall'][language]]], misconception=m['pitfall'][language],
        check=[('Which field changes the result in this example?' if en else '哪個欄位改變會使本例結果不同？'),
               ('Is this a requirement, a capability, or an informative example?' if en else '此處是規範要求、支援能力，還是 informative example？')])


TERMS = {
 'LBA':b('Logical Block Address；以所選格式的 block 為單位。','Logical Block Address, measured in blocks of the selected format.'),
 'STC':b('Storage Tag Check；獨立於三位元 PRCHK，STS=0 時忽略。','Storage Tag Check, separate from three-bit PRCHK and ignored when STS=0.'),
 'PRACT':b('Protection Information Action；依命令與 MS 選擇 PI 處理。','Protection Information Action; PI handling depends on command and MS.'),
 'PRCHK':b('Protection Information Check；Guard、Application、Reference 的檢查 bits。','Protection Information Check bits for Guard, Application, and Reference.'),
 'STS':b('Storage Tag Size；固定 Storage/Reference Space 中的高位 bit 數。','Storage Tag Size, the high-bit count within fixed Storage/Reference Space.'),
 'NLB':b('Number of Logical Blocks；本報告命令／status descriptors 的該欄為 0-based。DSM 的 LLB 另為1-based。','Number of Logical Blocks; this field in the report’s commands/status descriptors is zero-based. DSM LLB is separately one-based.'),
 'NLBAF':b('共同屬性 LBA formats 數的 0-based 欄位。','Zero-based count of LBA formats with common attributes.'),
 'NULBAF':b('Unique Attribute LBA Formats 的實際數量；可以為0。','Actual count of Unique Attribute LBA Formats; zero is allowed.'),
 'LBADS':b('LBA Data Size 的 exponent；資料 bytes=2^LBADS，0表示目前不可用。','LBA Data Size exponent; data bytes=2^LBADS, while zero means currently unavailable.'),
 'LBAFEE':b('Host 的 LBA Format Extension Enable 宣告。','Host LBA Format Extension Enable declaration.'),
 'DULBE':b('Deallocated or Unwritten Logical Block Error Enable，需 namespace DAE 支援。','Deallocated or Unwritten Logical Block Error Enable, requiring namespace DAE support.'),
 'DMRL':b('Dataset Management Ranges Limit，實際 range 數上限。','Dataset Management Ranges Limit, an actual range-count limit.'),
 'FCO':b('Fast Copy Only；要求適用來源以 fast copy 方法執行。','Fast Copy Only; requests a fast-copy method for the applicable source.'),
 'NSZ':b('Namespace Zeroes；要求全 namespace 清零，需額外 capability 與 DEAC 條件。','Namespace Zeroes; requests whole-namespace zeroing with additional capability and DEAC conditions.'),
 'LBACZ':b('LBAs Cleared to Zero；成功 NSZ 命令的範圍確認 bit。','LBAs Cleared to Zero; scope-confirmation bit for successful NSZ commands.'),
 'ATYPE':b('Get LBA Status Action Type；02h allocated，10h scan，11h tracked。','Get LBA Status Action Type: 02h allocated, 10h scan, 11h tracked.'),
 'CMPC':b('Completion Condition；描述 Get LBA Status 是否已完成所要求的範圍。','Completion Condition; describes whether Get LBA Status finished the requested range.'),
 'BWSF':b('Bandwidth Scale Factor；需乘 bandwidth value，單位為 MiB/s 或 GiB/s。','Bandwidth Scale Factor; multiply by the bandwidth value in MiB/s or GiB/s.'),
 'GC':b('Rate Limiting log 的 32-bit Generation Count，用於分段讀取一致性。','32-bit Generation Count in the Rate Limiting log, used for chunk consistency.'),
 'ESA':b('Entry Sequence Attribute；LBA Migration Queue 的 start／stop／suspend／full 標記。','Entry Sequence Attribute, marking start/stop/suspend/full in the LBA Migration Queue.'),
 'KPIODAAG':b('Key Per I/O Data Access Alignment and Granularity；0-based blocks。','Key Per I/O Data Access Alignment and Granularity, in zero-based blocks.'),
 'SWS':b('Stream Write Size；NVM command-set 單位為 logical blocks。','Stream Write Size; the NVM command-set unit is logical blocks.'),
 'NSZE':b('Namespace Size；可定址 logical blocks 總數。','Namespace Size, the total number of addressable logical blocks.'),
 'NCAP':b('Namespace Capacity；同時可配置 logical blocks 最大數量。','Namespace Capacity, the maximum number of simultaneously allocated logical blocks.'),
 'NUSE':b('Namespace Utilization；目前配置 logical blocks 數量。','Namespace Utilization, the number of currently allocated logical blocks.'),
 'AWUN':b('Atomic Write Unit Normal；controller 正常原子寫入大小的 0-based 欄位。','Atomic Write Unit Normal, the controller’s zero-based normal atomic-write size.'),
 'AWUPF':b('Atomic Write Unit Power Fail；失敗條件原子大小的0-based欄位。','Atomic Write Unit Power Fail, the zero-based atomic size for failure conditions.'),
}


for names,zh,en in [
 ('NSID,SNSID,ENSID','Namespace 識別碼；SNSID 選 Copy 來源，ENSID 選匯出 namespace，合法值受個別命令約束。','Namespace identifier; SNSID selects a Copy source and ENSID an exported namespace. Valid values are command-specific.'),
 ('SLBA,SDLBA,DSLBA','範圍起始 LBA；SDLBA 選 Copy 目的，DSLBA 是 Get LBA Status descriptor 的起點。','Starting LBA; SDLBA selects the Copy destination and DSLBA starts a Get LBA Status descriptor.'),
 ('DPTR','命令 data pointer；Read 是目的、Write 是來源、Copy／DSM 指向 descriptors。','Command data pointer: destination for Read, source for Write, descriptors for Copy/DSM.'),
 ('MPTR','Separate metadata 的指標；metadata placement 由 namespace format 與命令欄位決定。','Separate-metadata pointer; namespace format and command fields determine metadata placement.'),
 ('MS','每個 logical block 的 metadata bytes；與 PI size 比較以判斷 PRACT 的傳輸效果。','Metadata bytes per logical block; compare with PI size to determine PRACT transfer effects.'),
 ('PIF,QPIF','Protection Information Format selector；PIF 選一般格式，QPIF 提供 Qualified PI 的格式能力。','Protection Information Format selector; PIF selects the normal format and QPIF supplies Qualified PI format capability.'),
 ('PIL','Protection Information Location；用來判斷 PI 在 metadata 前端或後端，需遵守所選 Guard 格式限制。','Protection Information Location; selects PI placement within metadata subject to Guard-format restrictions.'),
 ('PRINFO,PRINFOR,PRINFOW','PRACT 與 PRCHK 的組合欄位；Copy 的 R／W 版本分別控制讀端／寫端。','Combined PRACT/PRCHK field; Copy R/W versions control the read and write sides separately.'),
 ('STCR,STCW','Copy 讀端／寫端的 Storage Tag Check；依兩側 STS 與 PI 處理分支判斷有效性。','Copy read/write Storage Tag Check; validity depends on each side’s STS and PI processing branch.'),
 ('GRDCHK,ATCHK,RTCHK','PRCHK 的 Guard／Application／Reference 檢查選擇；另須套用 PI 特殊停用值規則。','PRCHK Guard/Application/Reference check selection, also subject to PI disable-sentinel rules.'),
 ('LBST,ELBST','Logical Block Storage Tag／Expected Logical Block Storage Tag；寬度由 STS 決定。','Logical Block Storage Tag/Expected Logical Block Storage Tag; width is determined by STS.'),
 ('ILBRT,EILBRT','Initial Logical Block Reference Tag／expected 初值；Type 1／2 依 block 遞增並在欄位寬度處回捲。','Initial Logical Block Reference Tag/expected initial value; Type 1/2 increment per block and wrap at the field width.'),
 ('LBAT,ELBAT','Logical Block Application Tag／expected tag；16-bit，checking 與 mask 及停用值規則共同決定。','Logical Block Application Tag/expected tag; 16 bits, with checking governed by masks and disable sentinels.'),
 ('LBATM,ELBATM,LBSTM','Tag comparison mask；bit=0 排除比較，Storage mask 額外受支援與對齊限制。','Tag comparison mask; zero bits exclude comparison, with extra support/alignment rules for Storage masking.'),
 ('LBTU,LBTL,ELBTU,ELBTL,ELBT','Logical Block Tags／expected tags 的上／下部分；依 Guard 格式、STS 與 Dword 位置組合。','Upper/lower Logical Block Tags or expected tags; combine according to Guard format, STS, and Dword position.'),
 ('CETYPE,CEV','Command Extension Type／Value；Type 先決定 Value 的用途，不能固定當作 DSM hints。','Command Extension Type/Value; Type selects the meaning of Value, which is not always DSM hints.'),
 ('DTYPE,DSPEC','Directive Type／Specific 欄位；Directive 類型決定 Specific 的內容與 placement 效果。','Directive Type/Specific fields; the directive type determines Specific contents and placement effects.'),
 ('FUA','Force Unit Access；要求 nonvolatile-media 語意，不自動建立其他命令的順序。','Force Unit Access; requires nonvolatile-media semantics without automatically ordering other commands.'),
 ('LR','Limited Retry；指定受 Error Recovery policy 約束的重試行為。','Limited Retry; selects retry behavior governed by Error Recovery policy.'),
 ('NR','Range count 的 0-based 欄位；實際 descriptors 數為 NR+1。','Zero-based range-count field; actual descriptor count is NR+1.'),
 ('LLB','DSM 的 Length in Logical Blocks；1-based，與 Read／Write 的 NLB 編碼不同。','DSM Length in Logical Blocks; one-based, unlike Read/Write NLB encoding.'),
 ('DMRSL,DMSL','DSM 單一 range／全命令 blocks 的 processing limit；與 DMRL 的 range 數限制分開。','DSM per-range/whole-command block processing limits, separate from DMRL range-count limits.'),
 ('DESFMT','Copy Source Range Entry 格式 selector；同時影響 descriptor 大小、來源 NSID 與 PI tag layout。','Copy Source Range Entry format selector; affects descriptor size, source NSID, and PI tag layout.'),
 ('DEAC','Write Zeroes 的 deallocate 選擇；與 namespace 支援、NSZ、回讀規則一起判讀。','Write Zeroes deallocation selection; interpret with namespace support, NSZ, and read behavior.'),
 ('VSL,WZSL,WUSL','Verify／Write Zeroes／Write Uncorrectable 大小限制；非零值使用 exponent 與 minimum page size。','Verify/Write Zeroes/Write Uncorrectable size limits; nonzero values use an exponent and minimum page size.'),
 ('WZDSL','Write Zeroes with Deallocate 的專用大小限制；不可直接沿用 WZSL。','Specific Write Zeroes with Deallocate size limit; do not substitute WZSL.'),
 ('NAWUN,NAWUPF,NACWU,ACWU','Namespace normal／power-fail／compare-and-write 或 controller compare-and-write 原子大小；0-based。','Namespace normal/power-fail/compare-and-write or controller compare-and-write atomic size; zero-based.'),
 ('NABO','Namespace Atomic Boundary Offset；決定第一個 boundary 的位置。','Namespace Atomic Boundary Offset; determines the first boundary location.'),
 ('NABSN,NABSPF','Normal／power-fail atomic boundary size；0 值與 NSABP 支援要依欄位定義判讀。','Normal/power-fail atomic boundary size; interpret zero values and NSABP support using field definitions.'),
 ('MAM','Multiple Atomicity Mode；跨 boundary 的命令分成各自原子的 subranges。','Multiple Atomicity Mode; a crossing command is divided into independently atomic subranges.'),
 ('DN','Write Atomicity Normal 的 Disable Normal；不免除 power-fail atomicity。','Disable Normal in Write Atomicity Normal; does not remove power-fail atomicity.'),
 ('NVMCAP','NVM Capacity；以 bytes 計，不能與 NSZE／NCAP 的 logical-block 數直接比較。','NVM Capacity, measured in bytes; not directly comparable to NSZE/NCAP logical-block counts.'),
 ('ONCS','Optional NVM Commands Supported；包含能力及 variant，需結合 NVM Identify 的 limits。','Optional NVM Commands Supported; includes capability/variant information to combine with NVM Identify limits.'),
 ('MDTS','Maximum Data Transfer Size；以 minimum page size 為基準的 exponent；零有特定無限制語意。','Maximum Data Transfer Size; an exponent based on minimum page size, with a defined no-limit meaning for zero.'),
 ('FID,LID,CSI,CNS','分別選 Feature、log page、I/O command set 與 Identify 回傳資料結構；數值不能跨識別空間混用。','Select Feature, log page, I/O command set, and Identify response structure respectively; values are not interchangeable across spaces.'),
 ('SCT,SC','Status Code Type 與 Status Code；兩欄共同識別錯誤，單看 SC 可能誤判。','Status Code Type and Status Code jointly identify errors; SC alone can be ambiguous.'),
 ('NP,NC','Rate Limiting log 的 port／controller 數，皆採 0-based。','Port/controller counts in the Rate Limiting log; both are zero-based.'),
 ('NNSMAD','Non-Volatile Storage Medium Access Descriptors 數；實際數量，零表示此節點沒有下游 descriptors。','Actual number of Non-Volatile Storage Medium Access Descriptors; zero means no downstream descriptors.'),
 ('LPL','Rate Limiting Log Page Length；單位是 dwords，讀取 bytes 前乘 4 並檢查邊界。','Rate Limiting Log Page Length in dwords; multiply by four and validate bounds before reading bytes.'),
 ('RLMA','Rate Limiting Maximum Access；所述 port、controller 或 storage access 的最大能力，不是目前流量。','Rate Limiting Maximum Access; maximum capability for the described port/controller/storage access, not current traffic.'),
 ('TBWV,WBWV,TIOPS,WIOPS','Total／Write Bandwidth Value 與 Total／Write IOPS limits；bandwidth 另乘 BWSF。','Total/Write Bandwidth Values and Total/Write IOPS limits; bandwidth additionally uses BWSF.'),
 ('WRBWR,WRIOPSR','Write-to-Read Bandwidth／IOPS Ratio；計算寫入對 total budget 的權重。','Write-to-Read Bandwidth/IOPS Ratio; weights writes against the total budget.'),
 ('TGT,TID','Rate Limiting Target／Target Identifier；先選作用域，再解讀 target ID。','Rate Limiting Target/Target Identifier; select the scope before interpreting the target ID.'),
 ('MNDW','Maximum Number of Dwords；限制 Get LBA Status 回傳資料長度。','Maximum Number of Dwords; bounds Get LBA Status response length.'),
 ('RNLB','LBA Status log 的 Range Number of Logical Blocks；0-based。','Range Number of Logical Blocks in the LBA Status log; zero-based.'),
 ('NLSD','Number of LBA Status Descriptors；實際 descriptor 數量。','Number of LBA Status Descriptors; an actual descriptor count.'),
 ('LBAV,LBARS','LBA Valid 與 LBA Range Status；先驗資料是否有效，再依 Action Type 解讀狀態。','LBA Valid and LBA Range Status; check validity before interpreting status for the Action Type.'),
 ('LBACIR','LBA Change Indication Range；指定 range、整個 namespace 或無 range 的 entry 解讀。','LBA Change Indication Range; selects explicit range, whole namespace, or no-range entry interpretation.'),
 ('CDQP,DLBA','Controller Data Queue Phase 與 Deallocated LBA 標記；分別判別新 entry 與 deallocation 提示。','Controller Data Queue Phase and Deallocated LBA flag; distinguish new entries and deallocation indications.'),
 ('RECCS,RENSCS','Reference Exported Controller／Namespace Configuration State；分別是 364／48 bytes。','Reference Exported Controller/Namespace Configuration State, 364/48 bytes respectively.'),
 ('NVMECSS','NVMe Controller State Size；單位 dwords，0 時可變 state 欄位不存在。','NVMe Controller State Size in dwords; zero omits the variable state field.'),
 ('CSATTR.CP','Controller Suspended；1 表示整段 Migration Receive 處理期間皆 suspended。','Controller Suspended; one means suspended throughout Migration Receive processing.'),
 ('NCQS,NSQS,MQES','支援的 completion／submission queue 數與 queue entries；先解 0-based，再核對 underlying 上限。','Supported completion/submission queue counts and queue entries; decode zero-based values and check underlying limits.'),
 ('TO','CAP Timeout；每單位 500 ms，FFh 為 127.5 秒。','CAP Timeout in 500 ms units; FFh means 127.5 seconds.'),
 ('SQES,CQES','Submission／Completion Queue Entry Size；nibbles 以 2 的次方表示最小／最大 bytes。','Submission/Completion Queue Entry Size; nibbles encode minimum/maximum bytes as powers of two.'),
]:
    for term in names.split(','):
        TERMS[term]=b(zh,en)


def definition(term, language):
    if term in TERMS:
        return TERMS[term][language]
    # Each worksheet immediately above supplies the particular field relationship;
    # this label avoids imposing a global meaning on overloaded abbreviations.
    return (f'{term}: interpret within this Figure’s field relationship, units, and applicability stated above.' if language=='en'
            else f'{term}：依本 Figure 上方已解釋的欄位關係、單位與適用條件判讀。')
