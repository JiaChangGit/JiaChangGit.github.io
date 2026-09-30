"""Bring-up and PCIe lookup entries; source locations live in the registry."""
from scripts.nvme_quickref_data import card

card('B34','Doorbell 在記憶體映射中的位置','MMIO|doorbell|OFST',[
'查 controller properties 後面的空間怎麼排列時，用這張表找傳輸專用區的起點。PCIe 的 doorbell 區從 offset 1000h 開始；這是相對暫存器基底的位置，不是主機實體位址 1000h。',
'表的 OFST 是位元組偏移，Size 是佔用大小，T 表示由傳輸規格定義。Variable 表示大小隨配置而變，不能假設整區只佔 4 KiB；個別 SQ／CQ doorbell 位址還要用 CAP.DSTRD 計算。',
'例如 BAR 映射基底為 80000000h，doorbell 區起點就是 80001000h。要找 queue 2 的 doorbell，繼續查 PCIe Figures 5、6，不能直接在這個起點寫入 queue ID。'],[
'Use this table to locate the transport-specific area after controller properties. PCIe doorbells begin at offset 1000h relative to the register base, not host physical address 1000h.',
'OFST is a byte offset, Size gives occupied space, and T means transport-defined. Variable does not imply a fixed 4 KiB region. Individual SQ/CQ doorbells also depend on CAP.DSTRD.',
'For an illustrative BAR base of 80000000h, the doorbell region begins at 80001000h. Locate queue 2 using PCIe Figures 5 and 6; writing its queue ID at the region start is not equivalent.'],'P5 P6 P20')

card('B36','CAP：設定前先查硬體能力','CAP|MQES|MPSMIN|MPSMAX|DSTRD|TO|CRMS|CSS',[
'建立佇列、選記憶體頁大小或判斷 ready timeout 前，先查 CAP。它是能力回報，不是目前 CC 的設定值；讀到某能力不代表主機已啟用它。',
'常查的群組是 MQES bits15:0（最大 queue entries 減 1）、CQR bit16（I/O queue 連續記憶體要求）、DSTRD bits35:32（doorbell 間距 2^(2+DSTRD) bytes）、MPSMIN／MPSMAX bits51:48／55:52（頁大小指數）。CSS bits44:37、NSSRS bit36、CRMS bits60:59分別查命令集、subsystem reset 與 ready 模式；TO bits31:24以 500 ms 計。',
'例如 MQES=03FFh 是最多 1024 entries，DSTRD=1 是間距 8 bytes；兩個值都不能直接當 bytes 使用。選頁大小時還要核對 CC.MPS，等待 ready 則搭配 CC.CRIME、CRTO 與啟用流程。'],[
'Read CAP before choosing queue sizes, memory pages or readiness timeouts. It reports capabilities, not the current CC configuration; advertised support does not mean a function is enabled.',
'Frequently used groups are MQES bits 15:0 (maximum entries minus one), CQR bit 16 (contiguous I/O queue requirement), DSTRD bits 35:32 (2^(2+DSTRD) byte stride), and MPSMIN/MPSMAX bits 51:48/55:52 (page-size exponents). CSS bits 44:37, NSSRS bit 36 and CRMS bits 60:59 describe command sets, subsystem reset and ready modes. TO bits 31:24 uses 500 ms units.',
'For example, MQES=03FFh allows 1024 entries while DSTRD=1 means an 8-byte stride. Neither raw value is a byte count. Check CC.MPS for the selected page size and combine CC.CRIME, CRTO and initialization rules for readiness.'],'B41 B57 P5')

card('B41','CC：主機實際選了什麼','CC|EN|MPS|IOSQES|IOCQES|SHN|CRIME',[
'當能力看來足夠，controller 卻無法正常啟用，查 CC 可核對主機真正寫入的設定。它同時包含啟用、命令集、頁大小、佇列項目大小和 shutdown 通知。',
'EN bit0 控制啟用；CSS bits6:4 選命令集；MPS bits10:7 指定 2^(12+MPS) bytes；AMS bits13:11 選排程；SHN bits15:14 發 shutdown 通知。IOSQES bits19:16／IOCQES bits23:20 是每項 bytes 的 2 次方指數，CRIME bit24 決定啟用時的 ready 模式。',
'IOSQES=6、IOCQES=4 分別是 64-byte SQE、16-byte CQE，不是 queue 深度。EN 由 1 清為 0 會引發 Controller Reset；MPS、CSS 等設定有停用時才能修改的條件，不能把這個暫存器當任意時點都能重寫的設定表。'],[
'When advertised capabilities look adequate but initialization fails, inspect what the host actually programmed in CC. It combines enablement, command-set selection, page size, entry sizes and shutdown notification.',
'EN bit 0 enables the controller; CSS bits 6:4 selects command sets; MPS bits 10:7 specifies 2^(12+MPS) bytes; AMS bits 13:11 selects arbitration; SHN bits 15:14 requests shutdown. IOSQES bits 19:16 and IOCQES bits 23:20 are entry-size exponents. CRIME bit 24 selects the ready mode at enablement.',
'IOSQES=6 and IOCQES=4 mean 64-byte SQEs and 16-byte CQEs, not queue depths. Clearing EN from one to zero initiates Controller Reset. Fields such as MPS and CSS have disabled-state update requirements; this is not an unrestricted live configuration register.'],'B36 B42 B44')

card('B42','CSTS：啟用與關機進度回報','CSTS|RDY|CFS|SHST|ST',[
'CC 表示主機要求什麼，CSTS 表示控制器回報什麼。啟用卡住、命令無完成結果或 shutdown 尚未結束時，先把這兩邊對起來。',
'RDY bit0 表示已準備處理 submission entries；CFS bit1 表示無法由適當 CQ 回報的致命錯誤；SHST bits3:2 區分未開始、進行中與完成；ST bit6 區分 controller 與 subsystem shutdown。NSSRO bit4、PP bit5 另提供 reset 發生與處理暫停資訊。',
'SHST=10b 表示 shutdown 完成，不是一般 I/O 成功。RDY=1 的可用範圍還受 ready 模式影響；在 media-independent 模式下，不能據此假設所有 namespace 的媒體都已就緒。'],[
'CC describes the host request; CSTS describes the controller response. Compare them when enablement stalls, completions disappear or shutdown remains incomplete.',
'RDY bit 0 indicates readiness to process submission entries. CFS bit 1 reports a fatal error that could not be communicated through an appropriate CQ. SHST bits 3:2 encodes shutdown progress; ST bit 6 distinguishes controller and subsystem shutdown. NSSRO bit 4 and PP bit 5 report reset occurrence and processing pause.',
'SHST=10b means shutdown completed, not that an ordinary I/O succeeded. The usable scope of RDY=1 depends on the ready mode: media-independent readiness does not establish readiness of every namespace medium.'],'B41 B57')

card('B43','NSSR：辨識 subsystem reset 要求','NSSR|NSSRC|NSSRS|4E564D65h',[
'分析重設紀錄時，這張表用來辨識是否要求了整個 NVM subsystem reset。支援由 CAP.NSSRS 回報，與只清除單一 controller 的 CC.EN 不同。',
'offset20h 的 NSSRC bits31:0 只有寫入 4E564D65h 才啟動此 reset；其他值沒有這個功能效果。讀回固定為 0，不能靠讀值找回主機最後寫入的要求。',
'若 trace 顯示曾寫入 4E564D65h，之後讀 NSSR 得 0 是規格定義行為，不能據此認為寫入沒發生。確認重設完成與影響範圍，仍要搭配狀態與 §3.7.1 的流程。'],[
'Use this table to recognize a request for NVM Subsystem Reset in a trace. CAP.NSSRS advertises support. Its scope differs from clearing one controller’s CC.EN.',
'At offset 20h, NSSRC bits 31:0 initiates the reset only when written with 4E564D65h. Other values have no such functional effect. Reads return zero, not the last requested value.',
'A trace containing a write of 4E564D65h followed by a zero readback is consistent with the definition; it does not show that the write was lost. Determine completion and reset scope using status and §3.7.1.'],'B36 B41 B42')

card('B44','AQA：Admin 佇列深度','AQA|ASQS|ACQS|queue depth',[
'Admin commands 一開始就無法提交或回收時，用 AQA 核對兩個 Admin queues 的大小。這裡記的是 entry 數量，不是記憶體容量。',
'ASQS bits11:0 與 ACQS bits27:16 分別是 submission／completion 深度減 1；中間與高位保留。每個 queue 至少 2、最多 4096 entries，啟用時把其中一個欄位留為 0 會產生未定義結果。',
'要配置兩個各 64 entries 的 Admin queues，ASQS=63、ACQS=63，AQA=003F003Fh。SQ 與 CQ 的 entry 大小不同，所以相同深度不代表相同 buffer bytes。'],[
'Inspect AQA when Admin commands cannot be submitted or completions reclaimed. It holds queue entry counts, not buffer byte capacities.',
'ASQS bits 11:0 and ACQS bits 27:16 encode submission and completion depths minus one. The intervening and upper bits are reserved. Each queue has 2 to 4096 entries; enabling with either size field zero produces undefined results.',
'Two Admin queues of 64 entries use ASQS=63 and ACQS=63, giving AQA=003F003Fh. Equal depths do not imply equal buffer sizes because SQ and CQ entries have different sizes.'],'B45 B46')

card('B45','ASQ：Admin 命令佇列基底','ASQ|ASQB|Admin SQ|alignment',[
'這張表回答 controller 要從哪裡取 Admin 命令。ASQ 是 Admin Submission Queue 的基底，不是目前待執行命令的地址，也不是 SQ tail。',
'ASQB bits63:12 保存實體位址的高 52 bits；bits11:0 保留為 0。完整地址還必須依 CC.MPS 的頁大小對齊，因此最低 12 bits 為 0 只是最低要求。',
'例如 CC.MPS=1 代表 8 KiB pages；地址 00101000h 雖然 4 KiB 對齊，仍不符合這個設定。先核對 AQA 的深度和實際配置範圍，再比較 SQ doorbell 更新。'],[
'This table tells where the controller fetches Admin commands. ASQ is the Admin Submission Queue base, not the next command address or SQ tail.',
'ASQB bits 63:12 stores the upper 52 bits of the physical address; bits 11:0 are reserved zero. The complete address must also align to the page size selected by CC.MPS, so clearing 12 low bits is only the minimum requirement.',
'With CC.MPS=1, pages are 8 KiB. Address 00101000h is 4 KiB-aligned but does not meet that configuration. Check AQA and the allocated memory extent before correlating SQ doorbell writes.'],'B41 B44 P5')

card('B46','ACQ：Admin 完成佇列基底','ACQ|ACQB|Admin CQ|interrupt vector 0',[
'Admin 命令已被取走，但主機在錯誤位置等完成結果時，查 ACQ。所有經 Admin SQ 提交的命令，其完成項目都送到這個 Admin CQ。',
'ACQB bits63:12 是地址高位，低12 bits保留；地址按 CC.MPS 對齊。Admin CQ 固定關聯 interrupt vector0，不能把任意 I/O CQ 的向量設定套用過來。',
'ACQ 基底正確仍不保證每個 entry 都是新結果；讀取端還要看 CQE 的 phase tag，再更新 CQ head doorbell。ACQ 不會隨每筆完成而加16。'],[
'Check ACQ when an Admin command was fetched but the host is waiting at the wrong completion address. Commands submitted through Admin SQ complete in this Admin CQ.',
'ACQB bits 63:12 contains the upper address bits; the low 12 bits are reserved. Alignment follows CC.MPS. Admin CQ is associated with interrupt vector 0, not an arbitrary I/O CQ vector.',
'A correct ACQ base does not make every entry new. The consumer must check the CQE phase tag and update the CQ head doorbell. ACQ itself does not advance by 16 after each completion.'],'B99 P6')

card('B57','CRTO：控制器與媒體就緒的等待時間','CRTO|CRIMT|CRWMT|ready timeout',[
'這張表用來區分「先能處理不依賴媒體的命令」與「全部必要媒體就緒」兩種等待目標。排查初始化慢，先確定自己正在等待哪一件事。',
'CRIMT bits31:16 與 CRWMT bits15:0 均以500 ms計。前者在支援並啟用 media-independent ready 模式時使用；CRWMT 描述 controller 及必要媒體全部就緒的最長等待時間，且不得小於 CRIMT。',
'若 CRIMT=4、CRWMT=20，分別是2秒與10秒。2秒後某些 Admin 命令已可執行，不代表讀 namespace 應立即成功；仍要看 CC.CRIME 與該命令是否需要媒體。'],[
'Use CRTO to separate readiness for commands independent of media from readiness of all required media. First identify which condition an initialization timeout is testing.',
'CRIMT bits 31:16 and CRWMT bits 15:0 both use 500 ms units. CRIMT applies to supported and enabled media-independent readiness. CRWMT covers the controller and required media becoming ready and must not be smaller than CRIMT.',
'CRIMT=4 and CRWMT=20 mean 2 seconds and 10 seconds. Availability of some Admin commands after 2 seconds does not imply that namespace reads should already succeed. Check CC.CRIME and the command’s media dependency.'],'B36 B41 B42')

card('P5','SQ doorbell：告知新的提交位置','SQyTDBL|SQT|DSTRD|tail|wrap',[
'主機把命令放入 SQ 後，用此 doorbell 告知新的 tail。表內的 y 是 queue ID；offset 從 controller register base 起算，不是 SQ buffer 起算。',
'地址公式為1000h+(2y)×(4<<CAP.DSTRD)，SQT 在bits15:0，bits31:16保留。寫入的是環形佇列的新索引，新增命令數要由前後 tail 差值並考慮回繞計算。',
'DSTRD=1、y=2 時，offset=1020h。深度64的 SQ 若 tail 從62走到1，新增的是3項；寫 1不代表只新增1項。'],[
'After placing commands in an SQ, the host writes its new tail through this doorbell. Here y is the queue ID and the offset is relative to the register base, not the SQ buffer.',
'The address is 1000h+(2y)×(4<<CAP.DSTRD). SQT occupies bits 15:0; bits 31:16 are reserved. The value is the new ring index; derive the number of added commands from the change while accounting for wraparound.',
'With DSTRD=1 and y=2, the offset is 1020h. For a 64-entry SQ, advancing tail from 62 to 1 adds 3 entries. Writing 1 does not mean one new command.'],'P6 B36')

card('P6','CQ doorbell：歸還已讀取的位置','CQyHDBL|CQH|head|wrap',[
'主機讀完 CQE 後，更新 CQ head doorbell，告知哪些位置可供 controller 重用。這個動作不是提交新命令，也不是讀取目前 CQ head。',
'offset=1000h+(2y+1)×(4<<CAP.DSTRD)，CQH位於bits15:0，高位保留。寫入新head，前後差值需考慮環形回繞；doorbell讀回值由廠商定義，不適合作為狀態查詢。',
'DSTRD=1、queue2的 CQ doorbell 在1028h，與 SQ 的1020h相隔8 bytes。若只處理完成項目卻沒適時歸還空間，controller可能沒有可重用的CQ位置。'],[
'After consuming CQEs, the host updates the CQ head doorbell to release positions for controller reuse. This does not submit commands or read the current head.',
'Its offset is 1000h+(2y+1)×(4<<CAP.DSTRD). CQH occupies bits 15:0, with reserved upper bits. Calculate released entries from the new head with wraparound. Doorbell readback is vendor-specific and unsuitable as a status query.',
'For DSTRD=1, queue 2 uses CQ offset 1028h, eight bytes after SQ offset 1020h. Consuming completions without returning space can leave the controller without reusable CQ positions.'],'P5 B99')

card('P12','PCI CMD：MMIO 與 Bus Master 的入口','PCI CMD|BME|MSE|IOSE|MMIO|DMA',[
'PCIe 裝置可被枚舉，卻不能正常存取暫存器或搬移主機資料時，這張 PCI configuration 表是起點。這裡的 CMD 不是 NVMe command，也不是 NVMe CC。',
'常查 BME bit2（Bus Master Enable，允許裝置主動發起存取）、MSE bit1（Memory Space Enable，記憶體空間存取啟用）及IOSE bit0。bit10為Interrupt Disable，其餘欄位依PCI用途分開判讀。',
'看見BAR地址已配置，不能因此認定BME／MSE也已啟用。先核對PCI設定，再查NVMe佇列地址；把PCI CMD與NVMe CC的offset混用會讀到完全不同資料。'],[
'Start with this PCI configuration table when a device enumerates but register access or host-data transfers fail. PCI CMD is neither an NVMe command nor NVMe CC.',
'Common checks are BME bit 2 (Bus Master Enable), MSE bit 1 (Memory Space Enable) and IOSE bit 0. Bit 10 is Interrupt Disable. Interpret the remaining fields according to their PCI roles.',
'An assigned BAR does not establish that BME and MSE are enabled. Check PCI configuration before queue addresses. Confusing PCI CMD offsets with NVMe CC accesses a different register space.'],'P20 B41')

card('P20','BAR0：暫存器基底的低位與屬性','BAR0|MLBAR|BA|TP|PF|RTE',[
'從PCI configuration找到NVMe暫存器映射時，先讀BAR0的位址與類型，再判斷是否需要BAR1高位。此表也說明位址低位不是全部都能當地址使用。',
'BA bits31:14保存低32-bit地址中的可設定部分；bits13:4保留。PF bit3說明不允許prefetch，TP bits2:1表示映射類型，RTE bit0表示memory space。更大的映射空間可以使更多地址位唯讀。',
'組合地址前要去掉屬性位，並確認TP所指類型。64-bit映射時只取BAR0會截斷4 GiB以上地址；反過來也不能不看類型便把任意下一個BAR當高32bits。'],[
'Use BAR0 to find the NVMe register mapping and determine whether BAR1 supplies upper address bits. Low bits also contain attributes rather than address data.',
'BA bits 31:14 holds the programmable portion of the lower 32 address bits; bits 13:4 are reserved. PF bit 3 indicates non-prefetchable space, TP bits 2:1 gives the mapping type and RTE bit 0 selects memory space. Larger apertures may make additional address bits read-only.',
'Remove attributes and check TP before assembling the address. Using only BAR0 truncates a 64-bit mapping above 4 GiB; treating every following BAR as an upper half without checking type is also incorrect.'],'P21 B34')

card('P21','BAR1：64-bit 暫存器地址的高位','BAR1|MUBAR|BA|64-bit address',[
'確認使用64-bit暫存器映射後，這張表提供地址高32bits。它和BAR0是一組地址，不是另一個NVMe暫存器區。',
'BA bits31:0直接對應完整地址bits63:32。地址的低位與屬性仍來自BAR0；主機可用的地址範圍還受到平台與橋接器資源配置限制。',
'例如有效高位為1、低位地址部分為80000000h，組合為0000000180000000h。忽略高位會誤存取80000000h，兩者相差4 GiB。'],[
'Once a 64-bit register mapping is established, BAR1 supplies its upper 32 bits. Together with BAR0 it forms one address, not a second NVMe register area.',
'BA bits 31:0 corresponds directly to full-address bits 63:32. BAR0 still supplies the low address and attributes. Platform and bridge resource allocation also constrains usable addresses.',
'An upper value 1 and lower address portion 80000000h form 0000000180000000h. Dropping the upper half accesses 80000000h instead, a 4 GiB difference.'],'P20')

card('P44','MSI-X：總開關、遮罩與向量數','MSI-X|MXE|FM|TS|interrupt',[
'CQ已產生完成項目但未收到中斷時，這張表可確認MSI-X是否啟用、是否被整體遮罩，以及硬體提供多少向量。',
'MXE bit15為MSI-X enable，FM bit14遮罩全部向量，TS bits10:0為table entries減1。使用MSI-X還要求MSI enable清0；FM清0後，個別vector mask仍各自有效。',
'TS=3表示4個向量，不是向量3已被啟用。FM由1改0也不會自動清除每個向量自己的mask，還要配合CQ指定的interrupt vector查表。'],[
'When a CQ contains completions but interrupts are absent, check MSI-X enablement, the function-wide mask and available vector count.',
'MXE bit 15 enables MSI-X, FM bit 14 masks all vectors and TS bits 10:0 encodes table entries minus one. MSI enable must be clear for MSI-X use. Clearing FM leaves each vector’s own mask effective.',
'TS=3 means four vectors, not that vector 3 is enabled. Changing FM from one to zero does not clear individual vector masks. Correlate the table with the CQ’s interrupt-vector assignment.'],'P45 P46')

card('P45','MSI-X Table：先找 BAR，再加 offset','MTAB|TBIR|TO|MSI-X',[
'要定位MSI-X table以核對向量配置，先由這張表找BAR，再加table offset。BAR index和位址偏移是兩個欄位。',
'TBIR bits2:0選BAR；TO bits31:3保存8-byte對齊的偏移。形成offset時清除低3bits，不能把整個32-bit值直接加到BAR基底。64-bit BAR以低Dword的BAR識別。',
'若MTAB=00002004h，TBIR=4、offset=2000h，表示BAR4所映射基底加2000h，而不是BAR0加2004h。可用BIR編碼須依本表判斷。'],[
'To inspect MSI-X vector configuration, locate the table by selecting its BAR and adding its offset. The BAR index and byte displacement are separate fields.',
'TBIR bits 2:0 selects the BAR; TO bits 31:3 holds an 8-byte-aligned offset. Clear the low three bits before adding the offset to the BAR base. A64-bit BAR is identified by its lower Dword BAR.',
'MTAB=00002004h means TBIR=4 and offset 2000h: BAR4’s mapped base plus 2000h, not BAR0 plus 2004h. Use the table’s permitted BIR encodings.'],'P44 P46')

card('P46','MSI-X PBA：待處理中斷的資料位置','MPBA|PBA|PBIR|PBAO|pending',[
'這張表定位Pending Bit Array，讓你檢查向量是否有待處理的中斷狀態。PBA與MSI-X table是不同結構，不能因為都屬MSI-X就使用同一個offset。',
'PBIR bits2:0選BAR，PBAO bits31:3給8-byte對齊的偏移；算法類似MTAB，但欄位內容可以不同。這裡描述的是PBA位置，並不是各vector的pending bits本身。',
'MPBA=00003000h表示由BAR0映射基底加3000h取得PBA。是否已出現CQE仍要讀CQ；一個pending bit不能代替CQ裡每筆命令的status。'],[
'This register locates the Pending Bit Array used to inspect pending interrupt state. PBA and the MSI-X table are different structures and need not share an offset.',
'PBIR bits 2:0 selects a BAR; PBAO bits 31:3 supplies an 8-byte-aligned offset. The calculation resembles MTAB but the values may differ. These are location fields, not the per-vector pending bits themselves.',
'MPBA=00003000h locates PBA at BAR0’s mapped base plus 3000h. Inspect CQ memory to determine completed commands; a pending bit does not replace their individual completion statuses.'],'P45 B99')

card('P55','PCIe Link：目前談成的速度與寬度','PXLS|NLW|CLS|SCC|link speed|link width',[
'頻寬低於預期時，查這張表確認目前協商出的link speed和width。裝置宣告的最大能力不能代替目前結果。',
'NLW bits9:4是Negotiated Link Width，CLS bits3:0是Current Link Speed編碼；link未up時兩者未定義。SCC bit12描述是否使用平台提供的共同參考時鐘，不是link速度。',
'若NLW=2，表示目前是x2，不能因產品標示x4就假設四條lane都在用。CLS需用對應PCIe版本的速度編碼解讀；本表沒有完整定義外部PCIe速度表，不把編碼值直接當GT/s。'],[
'When bandwidth is below expectation, inspect negotiated link speed and width here. Maximum advertised capability is not the current negotiated result.',
'NLW bits 9:4 is Negotiated Link Width; CLS bits 3:0 is the Current Link Speed encoding. Both are undefined while the link is down. SCC bit 12 describes use of the platform’s common reference clock, not link speed.',
'NLW=2 means the active link is x 2 even if the product supports x 4. Decode CLS using the applicable PCIe speed encoding; this table does not fully define that external encoding, so the raw code is not a GT/s value.'],'P60 P63')

card('P60','PCIe AER：不可更正錯誤狀態','AERUCES|CTS|URES|MTS|UCS|DLPES|PCIe AER',[
'查PCIe交易或連結異常時，這張表列出不可更正錯誤狀態。這裡AER是Advanced Error Reporting，不是NVMe的Asynchronous Event Request。',
'常用欄位包含 CTS bit14（Completion Timeout）、UCS bit16（Unexpected Completion）、MTS bit18（Malformed TLP）、URES bit20（Unsupported Request）及 DLPES bit4（Data Link Protocol Error）。TLP是交易層封包；多個狀態可同時置位。另有mask與severity暫存器決定回報和嚴重程度。',
'CTS=1只能證明記錄了PCIe completion timeout，不能直接判定是哪筆NVMe CID失敗。保存狀態與header log後再對時間、佇列及CQE；應先保存原始狀態，再進行錯誤復原，避免丟失用來對照的資訊。'],[
'Use this register for uncorrectable PCIe transaction or link errors. Here AER means Advanced Error Reporting, not NVMe Asynchronous Event Request.',
'Common bits are CTS bit 14 (Completion Timeout), UCS bit 16 (Unexpected Completion), MTS bit 18 (Malformed TLP), URES bit 20 (Unsupported Request) and DLPES bit 4 (Data Link Protocol Error). TLP means transaction-layer packet. Multiple bits can be set; separate mask and severity registers control reporting and severity.',
'CTS=1 records a PCIe completion timeout but does not identify the failed NVMe CID. Preserve status and header logs before correlating time, queues and CQEs. Save the original status before error recovery so it remains available for correlation.'],'P63 B101 B212')

card('P63','PCIe AER：已更正錯誤與重傳線索','AERCES|RES|BTS|BDS|RTS|RRS|correctable',[
'鏈路仍能運作但效能或穩定性下降時，可查已更正錯誤狀態。已更正表示該類錯誤有修復機制，不表示出現頻率不值得觀察。',
'RES bit0為Receiver Error，BTS6／BDS7為Bad TLP／Bad DLLP，RRS8為replay編號回捲，RTS12為Replay Timer Timeout。這些是狀態位，不是發生次數；遮罩另由AERCEM控制。',
'兩次快照都看到RTS=1，若中間沒清除，不能推論又新增一次timeout。要分析發生頻率，需記錄取樣時間、清除行為與重現條件，再與當時的link狀態對照。'],[
'Inspect correctable errors when the link operates but performance or stability degrades. Correctable describes recovery of that error class, not whether its frequency matters.',
'RES bit 0 is Receiver Error; BTS bit 6 / BDS bit 7 are Bad TLP/Bad DLLP; RRS bit 8 is replay-number rollover; RTS bit 12 is Replay Timer Timeout. These are status bits, not occurrence counters. AERCEM controls their masks separately.',
'Seeing RTS=1 in two snapshots without an intervening clear does not establish two timeouts. Frequency analysis needs sampling times, clear operations and reproduction conditions, correlated with link status.'],'P55 P60')
