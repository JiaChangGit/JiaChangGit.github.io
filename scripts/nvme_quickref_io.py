"""NVM I/O fields and the diagrams that most often disambiguate them."""
from scripts.nvme_quickref_data import card

card('N4','Single Atomicity：單位、條件與邊界的關係','AWUN|AWUPF|NAWUN|NAWUPF|ACWU|NACWU|atomicity',[
'需要驗證某次寫入是否享有整筆原子性時，用這張表整理controller基準、namespace專屬值與boundary條件。這張表明確針對Single Atomicity Mode。',
'AWUN／AWUPF分別對應正常操作與斷電情境，ACWU用於融合Compare and Write；NA前綴是namespace值。NABSN／NABSPF與NABO控制邊界。表中的不等式描述支援時必須成立的參數關係，實際值仍須按各欄編碼換算。',
'一筆寫入即使未超過NAWUN，跨namespace atomic boundary時，Single Atomicity Mode也不保證該整筆符合namespace原子性。先看模式、單位大小，再看起點與範圍，不能只比較NLB。'],[
'Use this table to organize controller baselines, namespace-specific values and boundaries when assessing whole-write atomicity. It explicitly concerns Single Atomicity Mode.',
'AWUN/AWUPF distinguish normal and power-failure conditions; ACWU applies to fused Compare and Write. The NA-prefixed fields are namespace values. NABSN/NABSPF and NABO define boundaries. Inequalities constrain supported parameters; decode each field’s representation separately.',
'Even a write within NAWUN can lose the namespace-level whole-write guarantee if it crosses an atomic boundary in Single Atomicity Mode. Check mode, unit size, starting address and extent rather than NLB alone.'],'N8 N123')

card('N8','Atomic Boundary：同樣大小，不同起點會有不同結果','NABO|NABSN|NABSPF|atomic boundary|alignment',[
'這張圖把原子性邊界畫成相鄰區間，適合快速判斷一段LBA是否跨界。圖中顏色區分區間，不代表不同namespace或不同媒體。',
'第一個界線由NABO決定，後續界線依解碼後的boundary size等距排列。寫入範圍由SLBA與blocks數決定；NABSN和NABSPF對應不同情境，原始欄位值還有0及減1編碼規則。',
'以已解碼的boundary size=8 blocks、offset=0為例，LBA4～7留在一區，LBA6～9跨越8的界線。兩者都是4 blocks，但後者不能只憑大小就宣稱享有Single Atomicity整筆保證。'],[
'The diagram divides LBA space into atomic-boundary intervals. Colors distinguish intervals, not namespaces or media.',
'NABO positions the first boundary; decoded boundary size spaces subsequent ones. SLBA and block count locate the write. NABSN/NABSPF cover different conditions, with special zero and minus-one encodings in the original fields.',
'For a decoded boundary size of 8 blocks and offset 0, LBAs 4–7 stay within one interval while 6–9 cross boundary 8. Both contain four blocks, but size alone cannot establish the Single Atomicity whole-write guarantee for the latter.'],'N4 N123')

card('N22','NVM opcode：先確認命令集再解碼','opcode|Read 02h|Write 01h|Flush 00h|Compare 05h|Copy 19h',[
'解析I/O trace時，用這張表把opcode對回NVM命令。相同opcode在Admin與I/O queue不一定代表相同操作。',
'表列出opcode、命令名稱與定義位置，包括Flush00h、Write01h、Read02h、Compare05h、Write Zeroes08h、Dataset Management09h、Verify0Ch、Copy19h。支援要求仍需搭配能力回報。',
'OPC=02h出現在NVM I/O SQ是Read；出現在Admin SQ則不能套用這張表。保留queue種類、CSI與opcode一起查，才不會把log讀取誤當成媒體讀取。'],[
'Map opcodes to NVM I/O commands here. The same opcode can have a different meaning on Admin and I/O queues.',
'Rows provide opcode, command and definition location, including Flush 00h, Write 01h, Read 02h, Compare 05h, Write Zeroes 08h, Dataset Management 09h, Verify 0Ch and Copy 19h. Check capabilities for support.',
'OPC=02h on an NVM I/O SQ means Read; on Admin SQ this table does not apply. Preserve queue type, CSI and opcode together to avoid mistaking log retrieval for media reads.'],'B92 N53 N70')

card('N53','Read 起點：64-bit SLBA','Read|SLBA|CDW10|CDW11',[
'核對Read是否讀錯位置時，先從CDW10／11合成完整SLBA。這是namespace內的logical block地址，不是host buffer地址。',
'SLBA佔64bits，低32bits在CDW10、高32bits在CDW11。實際bytes位置取決於目前LBA大小；命令長度由CDW12.NLB另外提供。',
'CDW11=1、CDW10=0表示SLBA=4294967296，不能只看低位而當成LBA0。範圍尾端是SLBA+NLB，因為NLB原始值是blocks數減1。'],[
'Combine CDW10/11 into the full SLBA when checking a Read address. It addresses logical blocks within the namespace, not host memory.',
'SLBA is 64 bits: low 32 in CDW10 and high 32 in CDW11. Its byte position depends on the current LBA size; CDW12.NLB supplies the length separately.',
'CDW11=1 and CDW10=0 means SLBA=4294967296, not LBA 0. The inclusive final LBA is SLBA+NLB because raw NLB encodes block count minus one.'],'N54 N123')

card('N54','Read CDW12：範圍、重試與保護要求','Read NLB|LR|FUA|PRINFO|STC|CETYPE',[
'讀取的長度、重試方式或保護檢查與預期不同時，查CDW12。這些控制位各自有目的，不是同一種「嚴格讀取」開關。',
'NLB bits15:0為blocks數減1；CETYPE bits19:16選命令擴充；STC bit24控制Storage Tag檢查；PRINFO bits29:26含PI動作與檢查；FUA bit30要求相關資料與metadata提交到非揮發媒體並由該媒體讀回，LR bit31要求有限重試。',
'NLB=7、每block4096bytes，資料量是32768bytes。FUA不隱含與其他命令的先後順序；LR也不等於固定時間內必定完成。'],[
'Use CDW12 when Read length, recovery or protection behavior differs from expectation. Its controls are separate mechanisms, not one “strict read” switch.',
'NLB bits 15:0 encodes blocks minus one; CETYPE bits 19:16 selects extensions; STC bit 24 checks Storage Tags; PRINFO bits 29:26 controls PI action/checks. FUA bit 30 commits relevant data/metadata to nonvolatile media and reads it from there. LR bit 31 requests limited retries.',
'NLB=7 with 4096-byte blocks transfers 32768 data bytes. FUA does not order other commands, and LR does not guarantee a fixed completion deadline.'],'N53 N175')

card('N70','Write 起點：把 LBA 與 DMA 地址分開','Write|SLBA|destination LBA',[
'寫錯區域的問題要分別查NVM目的LBA與主機來源buffer。這張表只定義Write的SLBA，不描述PRP或SGL地址。',
'CDW10／11合成64-bit SLBA，分別為低32與高32bits。SLBA以所選namespace格式的blocks為單位，不直接以512-byte sectors計。',
'同樣SLBA=8，在512-byte格式的資料起點是4096bytes，在4 KiB格式是32768bytes。先確認格式，再與應用程式的byte offset換算結果比較。'],[
'Separate the destination LBA from the host source buffer when investigating misplaced writes. This figure defines Write SLBA, not PRP or SGL addresses.',
'CDW10/11 combines low/high 32-bit halves into a 64-bit SLBA. Units are blocks of the selected namespace format, not universally 512-byte sectors.',
'SLBA=8 corresponds to byte 4096 with 512-byte blocks and byte 32768 with 4 KiB blocks. Confirm the format before comparing application byte-offset calculations.'],'N71 N125 B93')

card('N71','Write CDW12：持久性、PI 與配置提示','Write NLB|FUA|LR|PRINFO|DTYPE|CETYPE|STC',[
'驗證Write completion代表哪些保證時，查這張表的FUA與PI控制，也要保留namespace格式和cache情境。完成不等於所有其他寫入也一起持久化。',
'NLB bits15:0是blocks數減1，CETYPE19:16與DTYPE23:20分別指定命令擴充和Directive；STC24、PRINFO29:26控制保護，FUA30要求本命令資料與metadata在完成前寫入非揮發媒體，LR31控制重試努力。',
'FUA=1強化的是這筆Write的完成條件，不建立與另一筆Write的隱含順序。使用FDP或Streams時，也要依DTYPE與CETYPE解CDW13，不能把相同16bits永遠當同一種identifier。'],[
'Inspect FUA and PI controls when determining what Write completion guarantees, retaining namespace format and cache context. Completion does not automatically persist every other write.',
'NLB bits 15:0 is blocks minus one; CETYPE bits 19:16 and DTYPE bits 23:20 select extensions and directives. STC bit 24/PRINFO bits 29:26 control protection. FUA bit 30 requires this command’s data/metadata on nonvolatile media before completion; LR bit 31 controls recovery effort.',
'FUA=1 strengthens this Write’s completion condition without implicitly ordering another Write. For FDP or Streams, decode CDW13 using DTYPE and CETYPE rather than assigning a fixed meaning to the same identifier bits.'],'B471 N174 B294')

card('N39','Copy 描述子：格式決定 namespace 與 PI 配置','Copy|DF|SNSID|descriptor format',[
'解析Copy來源清單前，先查描述子格式。格式決定是否有來源NSID，以及保護資訊屬於哪種配置；選錯格式會把後續bytes全部讀錯。',
'格式0／1沒有SNSID，來源與目的namespace相同；格式2／3包含SNSID，可指定不同來源namespace。0／2對應8-byte、16-bit Guard PI；1／3對應16-byte、32或64-bit Guard PI。格式4另涉及SLM來源，其完整定義不在這三份來源規格中。',
'若DF=2，不能使用格式0的固定位置假設來源NSID不存在。是否允許跨namespace、格式是否相容與範圍限制，仍需配合Copy能力及該命令條件。'],[
'Select the Copy descriptor format before decoding its source list. It determines presence of source NSID and PI layout; a wrong format shifts the interpretation of subsequent bytes.',
'Formats 0/1 omit SNSID and use the destination namespace as source; 2/3 include SNSID and permit a different source.0/2 use 8-byte 16-bit-Guard PI; 1/3 use 16-byte 32/64-bit-Guard PI. Format 4 references SLM, whose full definition is outside the three supplied sources.',
'For DF=2, do not use a format 0 decoder that assumes SNSID is absent. Cross-namespace support, format compatibility and range limits still require Copy capability and command checks.'],'N19 N125')

card('N47','Dataset Management：每段 LBA 範圍如何排列','DSM|CATTR|LLB|SLBA|range index|offset',[
'解析Dataset Management buffer時，這張表把range編號和byte offset對在一起。range index是第幾筆，offset是距buffer起點多少bytes。',
'每筆16bytes：CATTR在相對bytes3:0，LLB在7:4，SLBA在15:8。第i筆起點為16×i。LLB直接表示blocks數，不用Read／Write NLB的加1規則；命令指定的range數另看NR。',
'第2筆（index1）從byte16開始；SLBA=100、LLB=8描述LBA100～107。LLB=8不表示9blocks。是否所有範圍都會處理，還需核對DMRL、DMRSL、DMSL及support-variant能力。'],[
'This table maps Dataset Management range indices to byte positions. An index counts entries; an offset counts bytes from the buffer start.',
'Each entry is 16 bytes: CATTR at relative 3:0, LLB bytes 7:4 and SLBA bytes 15:8. Entry i starts at 16×i. LLB directly counts blocks rather than using Read/Write’s plus-one NLB encoding. NR separately specifies the command’s range count.',
'The second entry, index 1, starts at byte 16. SLBA=100 with LLB=8 describes LBAs 100–107, not nine blocks. Processing extent also depends on DMRL/DMRSL/DMSL and support-variant capabilities.'],'N129')

card('N83','Write Zeroes：清零範圍與 deallocate 要求','Write Zeroes|DEAC|NSZ|NLB|PRCHK|STC',[
'這張表可區分一般範圍清零、要求deallocate與整個namespace清零。名字相近不代表具有Sanitize的安全清除保證。',
'NLB bits15:0為blocks數減1；NSZ bit23要求整個namespace處理，需搭配DEAC bit25及支援能力。STC bit24與PRCHK必須清0；FUA bit30描述完成前的非揮發要求。',
'NSZ=1但DEAC=0會得到Invalid Field in Command；NSZ=1時NLB由controller忽略，不能再用NLB=0推論只處理1block。操作範圍要先由NSZ及能力判斷。'],[
'Distinguish range zeroing, deallocation requests and whole-namespace zeroing here. Similar names do not confer Sanitize’s security guarantees.',
'NLB bits 15:0 encodes blocks minus one. NSZ bit 23 requests whole-namespace processing in conjunction with DEAC bit 25 and support. STC bit 24 and PRCHK must be zero. FUA bit 30 specifies the nonvolatile completion condition.',
'NSZ=1 with DEAC=0 returns Invalid Field in Command. With NSZ=1, the controller ignores NLB, so NLB=0 cannot be used to infer a one-block operation. Establish scope from NSZ and capabilities first.'],'N129 B451')

card('N153','Extended LBA：資料與 metadata 交錯','extended LBA|metadata|MS|FLBAS',[
'計算傳輸長度或尋找第2個block起點時，用此圖確認extended LBA的排列。它不是整批資料後面再附一整批metadata。',
'圖中每個LBA的資料後接該LBA的metadata，再接下一個LBA；兩者透過同一資料buffer傳輸。資料大小由LBADS決定，metadata bytes由MS決定，格式選擇由namespace設定決定。',
'若每block4096-byte資料、8-byte metadata，第二個block從4104開始，第三個從8208開始。以4096固定跨距讀取會把metadata誤當下一個block開頭。'],[
'Use this diagram to calculate transfer length and successive block positions in extended-LBA layout. It does not place one metadata batch after the entire data batch.',
'Each block’s data is followed by its metadata, then the next block. Both use the data buffer. LBADS defines data size, MS metadata bytes, and namespace configuration selects the layout.',
'With 4096 data bytes and 8 metadata bytes per block, the second starts at 4104 and the third at 8208. A4096-byte stride incorrectly treats metadata as the next block’s beginning.'],'N125 N154')

card('N154','Separate Metadata：兩個 buffer 依 LBA 配對','MPTR|separate metadata|DPTR|metadata buffer',[
'資料與metadata分開傳輸時，這張圖說明兩份buffer如何對應。它們雖不相鄰，每個LBA仍要配到自己那一份metadata。',
'DPTR指向資料buffer，MPTR描述metadata；資料與metadata分別依LBA順序排列。使用PRP形式的metadata buffer時要求實體連續；SGL用法再依PSDT和支援條件解讀。',
'2blocks、每block4096+8bytes，資料buffer需8192bytes，metadata另需16bytes；不是把MPTR指向資料buffer後第8192byte就能自動取得正確配置，必須是實際已準備好的metadata地址。'],[
'This diagram pairs two separate buffers by LBA. Physical separation does not remove the one-to-one relationship between each block and its metadata.',
'DPTR describes data and MPTR metadata, each ordered by LBA. PRP-form metadata uses physically contiguous memory; SGL metadata follows PSDT and support requirements.',
'Two blocks of 4096+8 bytes require 8192 data bytes and 16 separate metadata bytes. Merely pointing MPTR after byte 8192 of a data allocation does not create valid metadata; it must describe the prepared metadata storage.'],'B93 N153')

card('N155','16-bit Guard PI：8 bytes 的實際配置','16b Guard|Application Tag|Reference Tag|STS 0|PI endian',[
'這張圖適用16-bit Guard且STS=0的PI，常用來核對保護欄位位置和byte order。不要把所有PI都當成這個8-byte格式。',
'Guard佔bytes0～1，Application Tag佔2～3，Reference Tag佔4～7。圖上MSB在較低byte位置，表示這些多byte PI欄位採高位byte在前的排列；與一般NVMe little-endian欄位不可混用。',
'Reference Tag值00000001h在這個PI中排列為00 00 00 01，不是01 00 00 00。STS非0時要改看Storage／Reference拆分，不能沿用本圖完整32-bit Reference Tag假設。'],[
'This layout applies to 16-bit Guard PI with STS=0 and is useful for checking offsets and byte order. It is not a universal PI layout.',
'Guard occupies bytes 0–1, Application Tag 2–3 and Reference Tag 4–7. MSB at the lower byte position means these multibyte PI fields use most-significant byte first, unlike ordinary little-endian NVMe fields.',
'Reference Tag 00000001h is stored 00 00 00 01 here, not 01 00 00 00. For nonzero STS, use the Storage/Reference split instead of assuming all 32 bits remain Reference Tag.'],'N128 N174')

card('N157','32-bit Guard PI：16-byte 格式','32b Guard|PI layout|Storage and Reference Space',[
'metadata同為16bytes時，這張圖幫你區分32-bit與64-bit Guard配置。Guard寬度改變，後面的欄位位置也會移動。',
'Guard在bytes0～3，Application Tag在4～5，Storage and Reference Space在6～15，共80bits。這80bits如何分成Storage Tag與Reference Tag，另由ELBAF.STS決定。',
'STS=16時，80-bit區域高16bits為Storage Tag，餘64bits為Reference Tag。若誤套64-bit Guard格式，連Application Tag的位置都會讀錯。'],[
'Use this figure to distinguish 32-bit and 64-bit Guard layouts even though both occupy 16 PI bytes. Changing Guard width also moves later fields.',
'Guard is bytes 0–3, Application Tag 4–5 and the 80-bit Storage/Reference space 6–15. ELBAF.STS determines the split of that final space.',
'With STS=16, its high 16 bits are Storage Tag and the remaining 64 bits Reference Tag. Applying the 64-bit Guard layout would misplace even the Application Tag.'],'N128 N159')

card('N159','64-bit Guard PI：較大 Guard 與 48-bit 標籤空間','64b Guard|PI layout|Storage Tag|Reference Tag',[
'此圖用來解析64-bit Guard格式，而不是假設所有欄位都變成64bits。整份PI仍是16bytes。',
'Guard在bytes0～7，Application Tag在8～9，Storage／Reference區域在10～15，共48bits。各多byte欄位按圖中的MSB／LSB排列；tag拆分由STS決定。',
'若STS=0，48bits全給Reference Tag；STS=48則全給Storage Tag、沒有Reference Tag。位寬和檢查規則要一起核對，不能把不存在的Reference Tag當作值0。'],[
'Decode 64-bit Guard PI with this layout rather than assuming every field becomes 64 bits. The entire PI remains 16 bytes.',
'Guard occupies bytes 0–7, Application Tag 8–9 and the 48-bit Storage/Reference space 10–15. Follow the MSB/LSB byte ordering and use STS for the tag split.',
'STS=0 leaves all 48 bits for Reference Tag; STS=48 uses all of them for Storage Tag with no Reference Tag. Absence of a field is not the same as a field whose value is zero.'],'N128 N157')

card('N174','Write 的 PRACT：host 要提供多少 metadata','PRACT|Write PI|MD 8|MD 16|16b Guard',[
'這張四情境圖用來核對host buffer與媒體格式的差異，尤其適合排查PI啟用後傳輸長度不符。圖的範圍是16-bit Guard PI。',
'PRACT=0時，host傳輸包含PI的metadata。PRACT=1且metadata恰好8bytes時，host不傳這8bytes，由controller產生PI；metadata大於8bytes時，host端metadata大小維持原值，不能一律減掉8bytes。',
'4096-byte資料、8-byte metadata、PRACT=1時，host只提供資料；改為16-byte metadata時則保留16-byte metadata傳輸配置。PRCHK指定哪些檢查，不能由PRACT單獨推論所有檢查都關閉。'],[
'These four 16-bit-Guard scenarios compare host buffers with media format, particularly useful for transfer-length mismatches after enabling PI.',
'With PRACT=0 the host transfers metadata including PI. With PRACT=1 and exactly 8 metadata bytes, those bytes are not transferred by the host and the controller generates PI. When metadata exceeds 8 bytes, its host-side size remains unchanged; do not always subtract eight.',
'For 4096 data bytes, 8 metadata bytes and PRACT=1, the host supplies data only. With 16 metadata bytes, retain the 16-byte metadata transfer layout. PRCHK controls checks; PRACT alone does not disable every check.'],'N175 N71')

card('N175','Read 的 PRACT：回主機時保留或移除哪些資料','PRACT|Read PI|metadata transfer|16b Guard',[
'這張圖沿NVM→controller→host方向顯示Read的PI處理。它補足Write圖的反向資料流，適合確認讀回buffer是否少算或多算metadata。',
'PRACT=0時讀回完整metadata；PRACT=1且metadata恰好8bytes時，PI不傳回host。metadata大於8bytes時仍維持原metadata大小；不能把「controller處理PI」直接等同「host完全沒有metadata」。',
'若metadata=16bytes而buffer只按資料大小配置，即使PRACT=1仍可能配置不足。先以本圖決定傳輸形態，再用namespace的metadata放置方式決定DPTR與MPTR。'],[
'Follow NVM→controller→host in this Read diagram. It complements the Write flow and helps verify whether returned metadata was omitted from or double-counted in buffer sizing.',
'PRACT=0 returns full metadata. PRACT=1 with exactly 8 metadata bytes removes PI from the host transfer. Metadata larger than 8 bytes retains its original size; controller PI processing does not imply that the host receives no metadata.',
'For 16 metadata bytes, allocating only data capacity may be insufficient even with PRACT=1. Determine the transfer form here, then use namespace metadata placement to configure DPTR/MPTR.'],'N174 N54 N154')
