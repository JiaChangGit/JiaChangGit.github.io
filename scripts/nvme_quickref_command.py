"""Command, completion and host-memory descriptor lookup."""
from scripts.nvme_quickref_data import card

card('B92','CDW0：先辨認命令與資料指標格式','CDW0|OPC|CID|PSDT|FUSE',[
'解讀一筆SQE時，先看CDW0，確定命令識別、opcode及後續資料指標的格式。CID要連同SQID才能唯一識別尚未完成的命令。',
'CID在bits31:16，PSDT在15:14，FUSE在9:8，OPC在7:0。PSDT=00b使用PRP；01b／10b使用SGL但metadata指標解讀不同。PCIe Admin命令使用PRP。FUSE區分一般操作與融合操作中的第一／第二筆。',
'同樣的DPTR bytes，PSDT不同就可能代表兩個PRP指標或一個SGL描述子。因此看到一個似乎合理的地址，不足以證明解析正確；先核對PSDT和命令所允許的格式。'],[
'Start a submission-entry decode with CDW0: command identity, opcode and pointer format. CID identifies an outstanding command uniquely only together with its SQID.',
'CID occupies bits 31:16, PSDT bits 15:14, FUSE bits 9:8 and OPC bits 7:0. PSDT=00b uses PRPs; 01b/10b use SGLs with different metadata-pointer interpretations. PCIe Admin commands use PRPs. FUSE identifies ordinary operations or the first/second fused command.',
'The same DPTR bytes may represent two PRP pointers or one SGL descriptor depending on PSDT. A plausible address alone does not validate the decode; check PSDT and the command’s permitted format first.'],'B93 B98')

card('B93','64-byte 命令的共同位置','SQE|NSID|MPTR|DPTR|CDW10|PRP2',[
'這張表是把原始命令bytes對回欄位的總地圖。它告訴你哪些位置共通，哪些位置必須接到個別命令定義。',
'CDW0在bytes3:0，NSID在7:4，CDW2／3在15:8，MPTR在23:16，DPTR在39:24，CDW10～15在63:40。PRP模式下，DPTR分為PRP1與PRP2；PRP2可能保留、指第二頁或指PRP List，取決於傳輸跨越多少頁邊界。',
'例如4 KiB頁、PRP1頁內offset=512、傳輸8192 bytes，需要3個資料頁；PRP2因此指向清單，而不是第二資料頁。NSID=FFFFFFFFh也不是所有命令都接受的通用廣播值。'],[
'This is the byte map for the common 64-byte command. It separates common fields from positions whose definitions belong to individual commands.',
'CDW0 is bytes 3:0, NSID bytes 7:4, CDW2/3 15:8, MPTR bytes 23:16, DPTR bytes 39:24 and CDW10–15 63:40. In PRP mode DPTR contains PRP1/PRP2; PRP2 is reserved, a second-page pointer or a list pointer according to page-boundary crossings.',
'With 4 KiB pages, initial offset 512 and 8192 transferred bytes, three data pages are needed. PRP2 therefore points to a list rather than the second data page. Also, NSID=FFFFFFFFh is not a universally accepted broadcast value.'],'B92 B111 B113')

card('B97','CQE：完成結果的外框','CQE|DW0|DW1|DW2|DW3',[
'拿到completion原始資料時，先用此配置圖分出回傳值、queue位置、命令識別與status。共同格式至少16 bytes，圖中只描述前16 bytes。',
'DW0與DW1依命令定義，不能一律當0或一般status；DW2含SQID與SQHD，DW3含STATUS、P與CID。P是phase tag，用來辨認環形CQ中的新項目。',
'Get Features的DW0可能是Feature值，Namespace Management的DW0可能是新NSID。兩者都應先查命令定義；是否成功則由DW3的status判斷。'],[
'Use this layout to separate command-specific results, queue information, command identity and status. The common format is at least 16 bytes; this figure describes its first 16.',
'DW0/DW1 are command-specific, not universally zero or status fields. DW2 contains SQID/SQHD; DW3 contains STATUS, P and CID. P is the phase tag identifying new entries in the circular CQ.',
'Get Features may return a feature value in DW0; Namespace Management may return a new NSID there. Decode those through their command definitions and determine completion status from DW3.'],'B98 B99 B101')

card('B98','CQE DW2：對回 SQ 與已消耗的位置','SQID|SQHD|CQE DW2',[
'多個SQ共用同一個CQ時，SQID協助把完成結果對回來源。SQHD則讓主機知道提交佇列哪些位置已被controller消耗。',
'SQID在bits31:16，SQHD在15:0。SQID加上DW3的CID識別命令；SQHD是建立這筆CQE時的SQ head快照，不是完成的命令在SQ中的index。',
'SQHD=12不代表CID12完成，也不保證主機讀取時controller仍停在12。命令可以不同順序完成，應分開追蹤buffer可重用位置與命令完成狀態。'],[
'When several SQs share a CQ, SQID identifies the source queue. SQHD tells the host which submission positions the controller has consumed.',
'SQID occupies bits 31:16 and SQHD bits 15:0. SQID plus DW3.CID identifies the command. SQHD snapshots the SQ head when the CQE was created; it is not the completed command’s SQ index.',
'SQHD=12 does not mean CID=12 completed or that the current controller head remains 12. Track reusable submission slots separately from command completion because completion order can differ.'],'B99 P5')

card('B99','CQE DW3：新舊判別、CID 與狀態','CID|P|Phase Tag|STATUS|CQE DW3',[
'主機掃描CQ時，這張表把「是否新完成項目」與「哪筆命令、什麼結果」分開。P不是成功旗標。',
'CID在bits15:0，P在bit16，STATUS在bits31:17。主機按目前CQ循環所期待的phase判斷新項目；若CQE分多次寫入，phase bit必須在最後一次寫入更新。',
'P符合目前期待值後，再用SQID／CID對命令並解析status。P=1本身不代表新項目，因為期待值會隨CQ回繞改變。'],[
'During CQ scanning, this table separates freshness from command identity and outcome. P is not a success flag.',
'CID occupies bits 15:0, P bit 16 and STATUS bits 31:17. Compare P with the phase expected for the current CQ cycle. If a CQE is written through multiple writes, its phase bit must be updated in the final write.',
'After confirming the expected phase, match SQID/CID and decode status. P=1 alone does not establish freshness because the expected value changes on CQ wraparound.'],'B98 B101')

card('B101','Status：類別、錯誤碼與重試提示','SCT|SC|DNR|M|CRD|ACRE',[
'命令有完成結果但不成功時，從這張表拆出狀態欄位，再選正確的錯誤碼表。原圖bit位置是相對整個CQE DW3，不是已移位的15-bit STATUS。',
'DNR bit31表示相同命令重送是否預期仍失敗；M bit30表示Error Information有額外資訊；CRD bits29:28選重試等待時間；SCT bits27:25為類別，SC bits24:17為代碼。CRD只有DNR=0且Host Behavior Support的ACRE=1才適用。',
'DW3=8005002Ah可拆出DNR=1、SCT=0、SC=02h、P=1、CID=002Ah。這表示通用Invalid Field in Command，不能只取02h就忽略類別；DNR=0的情況也不保證重試成功。'],[
'For unsuccessful completions, split status here before choosing a code table. Figure bit positions are relative to the complete CQE DW3, not an already shifted 15-bit STATUS value.',
'DNR bit 31 predicts failure of resubmitting the same command; M bit 30 indicates extra Error Information. CRD bits 29:28 selects retry delay, SCT bits 27:25 gives the category and SC bits 24:17 the code. CRD applies only with DNR=0 and ACRE=1 in Host Behavior Support.',
'DW3=8005002Ah decodes to DNR=1, SCT=0, SC=02h, P=1 and CID=002Ah: generic Invalid Field in Command. Do not interpret 02h without its category. Conversely, DNR=0 does not guarantee a successful retry.'],'B102 B103 B212')

card('B102','SCT：決定去哪張錯誤碼表','SCT|Generic|Command Specific|Media|Path Related',[
'這張表是status查詢的分流入口。同一個SC數值，在不同SCT下可能完全不同。',
'SCT=0是通用命令狀態，1是命令專屬狀態，2是媒體與資料完整性，3是路徑相關，7是廠商專屬，4～6保留。表的Reference欄帶你到對應Base小節；I/O命令還可能有command set補充。',
'SC=80h、SCT=0在NVM代表LBA Out of Range；SC=80h、SCT=1則是Conflicting Attributes。工具若只印80h，資訊不足以判讀。'],[
'This table routes a status lookup. Identical SC values can mean entirely different things under different SCT values.',
'SCT=0 is generic, 1 command-specific, 2 media/data integrity, 3 path-related and 7 vendor-specific; 4–6 are reserved. The Reference column leads to the corresponding Base section, with additional command-set definitions where applicable.',
'For NVM commands, SC=80h with SCT=0 means LBA Out of Range; SC=80h with SCT=1 means Conflicting Attributes. A tool displaying only 80h has not provided enough information.'],'N18 N19 B107')

card('B103','通用錯誤碼：先區分哪類參數問題','generic status|Invalid Field|Invalid Namespace|SC',[
'SCT=0時，這張表可查opcode、欄位、namespace、資料傳輸與命令順序等通用結果。它不是所有I/O特有錯誤的完整清單。',
'Value欄是SC，Definition描述觸發情況。常查00h成功、01h非法opcode、02h非法欄位、0Bh非法namespace或格式。錯誤名稱相近不代表相同條件；inactive NSID與invalid NSID也不能混為一談。',
'收到02h時先看命令的欄位及有效條件，再用M和Error Information中的Parameter Error Location縮小位置。不能把每個02h都直接歸因為NSID錯誤。'],[
'For SCT=0, look up generic opcode, field, namespace, transfer and sequencing outcomes here. This is not the complete list of I/O-specific errors.',
'Value is SC; Definition describes the condition. Common entries include 00h success, 01h invalid opcode, 02h invalid field and 0Bh invalid namespace or format. Similar names do not imply identical conditions; inactive and invalid NSIDs are distinct.',
'For 02h, inspect command fields and their validity conditions, then use M and Parameter Error Location in Error Information to narrow the location. Not every 02h is an NSID error.'],'B212 N18')

card('B104','Admin 命令專屬狀態','command specific|queue error|firmware status|SCT 1',[
'SCT=1且涉及Admin操作時，先在這張表找原因，再回到發出命令的章節。部分狀態表示需要後續動作，不宜只分成成功／硬體故障。',
'表以SC對應描述，包含queue ID或大小錯誤、韌體slot／image問題，以及需要reset的啟用結果。對照時保留原opcode，因為命令專屬碼必須放回命令情境。',
'韌體要求reset的完成結果，和下載image無效是兩種處理方向：前者應確認啟用時點與所需reset層級，後者應檢查image及提交參數。不要看到非0狀態就反覆重送相同更新。'],[
'For SCT=1 on Admin operations, start here and then return to the issued command’s definition. Some statuses request further action rather than fitting a simple success/hardware-failure split.',
'The table maps SC to descriptions including invalid queue identifiers or sizes, firmware slot/image problems and activation results requiring reset. Keep the original opcode because command-specific status requires command context.',
'A firmware result requiring reset differs from an invalid image. The former calls for checking activation timing and reset scope; the latter calls for inspecting the image and commit parameters. Repeatedly submitting the same update is not a universal response.'],'B187 N19')

card('B107','媒體與保護檢查錯誤','SCT 2|Guard|Application Tag|Reference Tag|Media Error',[
'SCT=2時，用這張表區分媒體讀寫錯誤與資料保護檢查失敗。保護資訊不符不必然等於NAND物理損壞。',
'SC及描述涵蓋Write Fault、Unrecovered Read，以及Guard、Application Tag、Reference Tag檢查錯誤。先保留失敗種類，再查namespace格式、命令的檢查旗標與預期tag。',
'Reference Tag失敗時，LBA起點、PI類型或tag設定不一致都值得核對；若只記成「讀取錯誤」，會失去定位線索。NVM另補Compare Failure及Deallocated／Unwritten相關碼。'],[
'For SCT=2, separate media read/write failures from protection-check failures. A protection mismatch does not by itself establish physical NAND damage.',
'The codes include Write Fault, Unrecovered Read and Guard, Application Tag or Reference Tag checks. Preserve the specific failure category and correlate namespace format, command check controls and expected tags.',
'For a Reference Tag failure, inspect the starting LBA, PI type and tag configuration. Reducing it to “read error” discards useful evidence. NVM adds Compare Failure and deallocated/unwritten-block codes.'],'N20 N155 N174 N175')

card('B110','PRP 地址如何分成頁基底與 offset','PRP|Page Base Address|offset|CC.MPS',[
'這張位元圖用來確認PRP的地址切割。頁內offset是從該頁起點算起的bytes，不是第幾個PRP entry。',
'高位是Page Base Address，低n+1位是頁內offset；分界由CC.MPS決定。4 KiB頁使用低12bits，8 KiB頁使用低13bits，不能在所有配置硬套同一個FFFh遮罩。',
'地址12345000h在4 KiB頁下offset為0；在8 KiB頁下offset為1000h。相同地址的PRP是否合法，還要看它在命令或清單中的角色。'],[
'This bit diagram explains the split within a PRP address. An offset counts bytes from the page start, not PRP entries.',
'Upper bits hold the page base; the lower n+1 bits hold the page offset. CC.MPS determines the split:12 low bits for 4 KiB pages and 13 for 8 KiB. A fixed FFFh mask is not valid for every configuration.',
'Address 12345000h has offset zero with 4 KiB pages but 1000h with 8 KiB pages. Its validity also depends on the PRP’s role in the command or list.'],'B111 B41')

card('B111','PRP：哪些位置允許頁內 offset','PBAO|PRP1|PRP2|alignment',[
'看懂位址分界後，查這張表與其後段落判斷對齊要求。第一個資料指標、PRP List指標和清單內資料頁指標，規則不同。',
'PBAO佔64bits。一般PRP offset至少Dword對齊；資料起始PRP可依命令允許非0 offset，清單內資料頁指標則頁對齊。初始PRP List指標另須8-byte對齊，後續list page須頁對齊。',
'4 KiB頁下，作為第一個資料PRP的200004h可能合法，作為清單內資料頁指標卻不合頁對齊要求。不能只檢查最低2bits就放行所有PRP位置。'],[
'Use this definition and its following text to distinguish alignment rules for the initial data pointer, a PRP-list pointer and data-page pointers inside a list.',
'PBAO spans 64 bits. A PRP offset is at least Dword-aligned. The initial data PRP may permit a nonzero offset, while list data-page entries are page-aligned. The initial list pointer must be 8-byte-aligned; subsequent list pages are page-aligned.',
'With 4 KiB pages, 200004h may be valid as an initial data PRP but is not page-aligned for an entry inside the list. Checking only the bottom two bits is insufficient.'],'B110 B113 B93')

card('B113','PRP List：不連續實體頁的排列','PRP List|page chain|non-contiguous',[
'主機資料buffer跨多個不連續實體頁時，這張圖展示PRP List如何保存每頁地址。資料邏輯上連續，不代表實體地址必須連續。',
'每個清單項目8bytes，資料頁地址的offset為0；項目緊密排列，從entry0開始。若清單需要下一頁，當頁最後一項改為下一個list page的指標，因此不是每一項都代表資料頁。',
'4 KiB清單頁可容納512個8-byte項目；需要串接時，最後一項用於串接，這一頁最多剩511個資料頁地址。不能把清單page地址也算入資料傳輸。'],[
'This diagram shows a PRP list describing physically noncontiguous pages. Logical data continuity does not require consecutive physical addresses.',
'Each entry is 8 bytes; data-page addresses have zero page offset. Entries are packed from entry 0. If another list page is needed, the final entry points to that page rather than to data.',
'A4 KiB list page holds 512 eight-byte entries. With chaining, the last entry is a link, leaving at most 511 data-page addresses on that page. Do not count the list-page address as transferred data.'],'B93 B111')

card('B114','SGL 結構錯誤如何對應 status','SGL validation|Invalid Number of SGL Descriptors|Invalid SGL Segment Descriptor',[
'SGL地址看來正確卻被拒絕時，查這張條件對照表。它針對描述子排列與類型的錯誤，不只檢查buffer是否夠長。',
'Segment／Last Segment描述子出現在segment中非最後位置，對應Invalid Number of SGL Descriptors；最後一個segment又含串接描述子，對應Invalid SGL Segment Descriptor；不支援的type或type/subtype組合則是SGL Descriptor Type Invalid。',
'若3個描述子中第2個是Segment，第3個還是Data Block，錯在串接描述子的位置；把第3個資料buffer加大不會解決這個結構錯誤。'],[
'Consult this condition-to-status table when apparently valid SGL addresses are rejected. It checks descriptor arrangement and types, not just buffer length.',
'A Segment/Last Segment descriptor before a segment’s final position yields Invalid Number of SGL Descriptors. A link descriptor inside the final segment yields Invalid SGL Segment Descriptor. Unsupported types or type/subtype combinations yield SGL Descriptor Type Invalid.',
'If descriptor 2 of 3 is a Segment descriptor followed by a Data Block, the link is in the wrong position. Enlarging the third descriptor’s data buffer does not repair that structural error.'],'B116 B121 B122')

card('B116','SGL 描述子的 type 與 subtype','SGLID|SGLDT|SGLDST|descriptor',[
'每個SGL描述子長16bytes，先看最後一個byte，才能決定前15bytes如何解讀。不能看見前8bytes就一律當使用者資料地址。',
'byte15為SGLID，上半byte bits7:4是type，下半byte bits3:0是subtype；bytes14:0依類型定義。常見Data Block、Segment、Last Segment的type分別為0、2、3。',
'SGLID=30h表示type3、subtype0，地址指向最後一段描述子清單，而不是直接指資料。支援哪些類型仍要查Identify及PCIe適用條件。'],[
'An SGL descriptor is 16 bytes. Inspect its last byte before interpreting the first 15; the first eight bytes are not always a user-data address.',
'Byte 15 is SGLID: bits 7:4 selects type and bits 3:0 subtype. Bytes 14:0 are type-specific. Common Data Block, Segment and Last Segment types are 0, 2 and 3.',
'SGLID=30h means type 3/subtype 0: its address points to the final descriptor segment rather than directly to data. Supported types still depend on Identify and PCIe applicability.'],'B119 B121 B122 B338')

card('B119','SGL Data Block：直接描述資料 buffer','SGL Data Block|ADDR|LEN|SGLS',[
'這張表用來解讀真正的資料範圍。以本系列的PCIe memory address用法，ADDR是buffer起點，LEN是資料長度。',
'ADDR在bytes7:0，LEN在11:8，12～14保留，byte15的type為0。LEN直接以bytes計，0表示不傳資料，仍是有效描述子；對齊與粒度須配合Identify的SGLS。',
'LEN=4096是4096 bytes，不能套用NLB的加1規則。若controller要求4-byte粒度，ADDR及LEN都要符合，不能只把地址對齊而保留4097-byte長度。'],[
'Decode actual data-buffer extents here. For the PCIe memory-address use covered by this series, ADDR is the buffer start and LEN its length.',
'ADDR is bytes 7:0, LEN bytes 11:8, bytes 12–14 reserved, and byte 15 has type 0. LEN counts bytes directly; zero describes a valid zero-length transfer. Alignment and granularity depend on Identify.SGLS.',
'LEN=4096 means 4096 bytes, without the NLB plus-one rule. If four-byte granularity is required, both ADDR and LEN must comply; aligning the address does not make a 4097-byte length valid.'],'B116 B338')

card('B121','SGL Segment：指向下一段描述子','SGL Segment|type 2|LEN|ADDR',[
'當單一描述子不能描述所有資料時，Segment描述子把讀取者帶到下一段SGL。它的長度是描述子清單大小，不是資料buffer大小。',
'ADDR bytes7:0指向下一段，LEN bytes11:8必須非0且是16的倍數，byte15的type為2。這種串接描述子必須位於所屬segment的最後。',
'LEN=48表示下一段有3個16-byte描述子，不能推論只傳48bytes使用者資料；實際資料量要由Data Block等資料描述子計算。'],[
'A Segment descriptor links to another SGL segment when one descriptor cannot describe the transfer. Its length measures descriptor storage, not the data buffer.',
'ADDR bytes 7:0 points to the next segment; LEN bytes 11:8 must be nonzero and a multiple of 16; byte 15 has type 2. The link descriptor must be last in its containing segment.',
'LEN=48 means three 16-byte descriptors in the next segment, not a 48-byte data transfer. Obtain the actual transfer extent from data descriptors.'],'B114 B119 B122')

card('B122','SGL Last Segment：最後一段仍是一份清單','SGL Last Segment|type 3|last segment',[
'這張表標示接下來指向的segment已是最後一段。Last不表示這個描述子直接指向最後一塊使用者資料。',
'ADDR bytes7:0及LEN bytes11:8描述下一段，也是最後一段的描述子陣列；LEN非0且是16的倍數。type=3；被指向的最後segment不能再放Segment或Last Segment串接描述子。',
'LEN=32的Last Segment可指向兩個Data Block描述子。若第二個又是Segment，就違反最後segment的結構限制，應回查Figure114。'],[
'This descriptor marks the next segment as the final one. “Last” does not mean it directly identifies the last user-data block.',
'ADDR bytes 7:0 and LEN bytes 11:8 describe the next and final descriptor array. LEN is nonzero and a multiple of 16; type is 3. That final segment cannot contain another Segment or Last Segment link.',
'A Last Segment with LEN=32 can point to two Data Block descriptors. If the second is another Segment link, the final-segment constraint is violated; use Figure 114 to identify the error.'],'B114 B121')

card('N18','NVM 通用狀態補充：地址、容量與原子性','SCT 0|LBA Out of Range|Capacity Exceeded|Atomic Write Unit Exceeded',[
'Base通用表找不到NVM特有原因時，接著查這張補充表，SCT仍然是0。這不是新的status編碼格式。',
'SC14h為超過atomic write unit，1Eh為SGL地址或長度粒度錯誤，25h為Invalid Key Tag，80h為LBA超出namespace大小，81h為配置使用量超過namespace容量。',
'80h查SLBA、NLB與NSZE；81h查NUSE、NCAP及配置情境。兩者都與容量相關，但「位址越界」和「使用量超過可配置容量」不應使用同一個判斷式。'],[
'Use this extension when the Base generic table does not cover the NVM-specific condition. SCT remains 0; the status format is unchanged.',
'SC=14h exceeds an atomic write unit, 1Eh indicates invalid SGL alignment/granularity, 25h an invalid key tag, 80h an LBA beyond namespace size, and 81h utilization exceeding namespace capacity.',
'For 80h, inspect SLBA/NLB and NSZE. For 81h, inspect NUSE/NCAP and allocation context. Address range and allocated-capacity exhaustion require different checks.'],'N123 N4')

card('N19','NVM 命令專屬錯誤與命令清單','SCT 1|Conflicting Attributes|Invalid Protection Information|Copy errors',[
'收到NVM命令的SCT=1時，這張表除了錯誤名稱，也直接列出哪些命令可能回它。適合檢查工具是否套錯command set。',
'80h為Conflicting Attributes，81h為Invalid Protection Information，82h為Attempted Write to Read Only Range；Copy還有83h大小限制、85h格式不相容、86h無法fast copy、87h重疊範圍與89h資源不足。',
'SC81h在這裡是PI設定無效，不等於SCT2的Guard Check Error；前者先檢查要求的保護參數是否成立，後者則檢查資料與保護值是否吻合。'],[
'For SCT=1 on NVM commands, this table lists both meanings and affected commands. It helps detect use of the wrong command-set decoder.',
'80h is Conflicting Attributes, 81h Invalid Protection Information and 82h Attempted Write to Read Only Range. Copy adds size-limit 83h, incompatible-format 85h, fast-copy 86h, overlapping-range 87h and insufficient-resource 89h outcomes.',
'SC=81h here indicates invalid PI parameters, not the SCT=2 Guard Check Error. Check whether the requested protection configuration is valid before treating it as a mismatch between data and protection values.'],'B107 N39')

card('N20','NVM 媒體狀態補充：Compare 與未寫入區塊','SCT 2|Compare Failure|Deallocated or Unwritten Logical Block|DULBE',[
'此表補上NVM命令對資料內容或已釋放區塊的失敗原因。它能避免把Compare不一致一律記成媒體不可讀。',
'SC85h表示Compare Failure；87h表示Copy、Read或Verify嘗試使用deallocated或unwritten的LBA範圍而失敗。解讀87h時，還應核對namespace行為與Deallocated or Unwritten Logical Block Error相關設定。',
'Compare回85h表示比較不相符，不是該命令一定遇到CRC失敗。Read回87h也不能直接推論實體媒體損壞，先確認這段LBA是否被deallocate或尚未寫入。'],[
'This table adds NVM content-comparison and deallocated/unwritten-block failures. It prevents misclassifying every Compare mismatch as unreadable media.',
'SC=85h means Compare Failure.87h reports a failed Copy, Read or Verify involving deallocated or unwritten LBAs. Interpret 87h together with namespace behavior and the Deallocated or Unwritten Logical Block Error configuration.',
'Compare 85h establishes a miscompare, not necessarily a CRC failure. Read 87h likewise does not by itself establish physical damage; first check whether the range was deallocated or never written.'],'B107 N47')
