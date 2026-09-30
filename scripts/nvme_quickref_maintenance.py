"""Maintenance requests, payloads and observable outcomes."""
from scripts.nvme_quickref_data import card

card('B187','Firmware Commit：放進 slot 與啟用的差別','Firmware Commit|CA|FS|BPID|activate',[
'韌體已下載但版本未改變時，查Commit Action，分辨本次是否只放入slot、等待reset或立即啟用。下載與commit不是同一步。',
'FS bits2:0指定slot，0讓controller選；CA bits5:3的0為放入但不啟用、1為放入後下次Controller Level Reset啟用、2為既有slot下次reset啟用、3為立即啟用。CA6／7屬Boot Partition，搭配BPID bit31。',
'CA=1命令成功後，當下active firmware仍可是舊版；用Firmware Slot Information比較目前與下次active slot，再核對completion是否要求特定reset。'],[
'If a download did not change the running revision, inspect Commit Action to distinguish placement, activation after reset and immediate activation. Download and commit are separate steps.',
'FS bits 2:0 selects a slot, with zero letting the controller choose. CA bits 5:3 values 0/1/2/3 mean place without activation, place and activate at next Controller Level Reset, activate an existing slot at that reset, or activate immediately. CA=6/7 concern Boot Partitions with BPID bit 31.',
'After successful CA=1, the running firmware may still be old. Compare current and next-active slots and check whether completion specifies a particular reset requirement.'],'B191 B215 B104')

card('B191','Firmware Download：每個 chunk 的大小','Firmware Image Download|NUMD|FWUG|chunk',[
'重建韌體下載分段時，這張表解每一段長度。整份image的大小不能直接填到每個chunk命令。',
'CDW10的NUMD bits31:0以Dwords數減1表示本段長度，bytes=4×(NUMD+1)。還需搭配CDW11的Offset與Identify.FWUG要求，確認分段位置、粒度與完整性。',
'4096-byte chunk的NUMD=1023，而不是4096。讀trace時要分開記錄長度與目的image offset；正確長度仍可能因offset或FWUG條件不符而失敗。'],[
'Decode each firmware-download chunk length here. The whole-image size is not automatically the size of every command.',
'CDW10.NUMD bits 31:0 encodes Dword count minus one, giving 4×(NUMD+1) bytes. Combine it with CDW11.Offset and Identify.FWUG for chunk placement and granularity.',
'A4096-byte chunk uses NUMD=1023, not 4096. Record length and image offset separately; correct length alone does not satisfy offset or FWUG requirements.'],'B187 B338')

card('B215','Firmware Slot Log：目前版本與待啟用 slot','LID 03h|AFI|CAFS|NAFS|FRS',[
'更新後要確認「已存放」與「正在執行」是否相同，查這份log。某slot有版本字串，不代表它就是active slot。',
'AFI byte0的CAFS bits2:0為目前active slot，NAFS bits6:4為下次可造成啟用的reset所要啟用slot；NAFS=0表示未指示。FRS1～7每個8bytes，保存各slot的revision，從byte8開始。',
'CAFS=1、NAFS=2、slot2有新版字串，表示目前仍從slot1載入，slot2等待啟用。FRS為0可能是該slot未支援或沒有有效版本，不能單靠0區分兩者。'],[
'Use this log to distinguish stored and running firmware. A revision string in a slot does not make it active.',
'In AFI byte 0, CAFS bits 2:0 is the active slot and NAFS bits 6:4 the slot for the next reset able to activate it; NAFS=0 means unspecified. FRS1–7 are eight-byte revisions starting at byte 8.',
'CAFS=1/NAFS=2 with a new slot 2 revision means firmware was loaded from slot 1 while slot 2 awaits activation. A zero FRS can mean unsupported slot or no valid revision; it does not distinguish them.'],'B187')

card('B177','Device Self-test：選哪種測試或中止','Device Self-test|STC|short|extended|Host-Initiated Refresh',[
'測試啟動命令的動作由STC決定。命令完成與測試背景流程完成是兩回事，結果應接著看Self-test log。',
'CDW10 bits3:0的STC=1啟動short、2啟動extended、3啟動Host-Initiated Refresh、Eh為廠商專屬、Fh中止。NSID與支援能力另決定測試對象及動作是否適用。',
'STC=2成功完成提交後，若log仍顯示extended進行中，並不矛盾。不能把Admin CQE成功當成整個測試已通過。'],[
'STC chooses the requested self-test action. Command completion differs from completion of the background test; inspect the log for its outcome.',
'CDW10.STC bits 3:0 values 1/2/3 start short, extended or Host-Initiated Refresh operations; Eh is vendor-specific and Fh aborts. NSID and capabilities separately determine target and applicability.',
'After a successful STC=2 submission, an extended test may still be in progress in the log. Admin CQE success is not proof that the test passed.'],'B218 B219')

card('B218','Self-test Log：目前進度與最近 20 筆結果','LID 06h|CDSTO|CDSTC|DSTOS|RDS',[
'這張表將目前正在執行的狀態與過去結果分開。查測試進度看前2bytes；查成敗看後面的result list。',
'CDSTO byte0低4bits為目前operation，CDSTC byte1低7bits為完成百分比。DSTOS=0時進度欄應忽略。從byte4開始保存20筆28-byte結果，第一筆是最新完成或中止的操作。',
'byte1仍留25而DSTOS已為0時，不應報告「測試卡在25%」。先讀最新結果，確認是完成、命令中止、reset中止或其他原因。'],[
'This layout separates the current operation from historical outcomes. The first two bytes describe progress; the result list describes success or failure.',
'CDSTO byte 0 low 4 bits identifies the current operation; CDSTC byte 1 low 7 bits gives completion percentage. Ignore progress when DSTOS=0. Twenty 28-byte results begin at byte 4, newest completed or aborted operation first.',
'If byte 1 still contains 25 but DSTOS is zero, do not report a test stuck at 25%. Read the newest result for completion, command abort, reset abort or another cause.'],'B219 B177')

card('B219','Self-test Result：先看有效位再讀失敗位置','DSTS|DSTR|DSTC|VDINFO|FLBA|SEGN|POH',[
'這張表用來判讀一筆Self-test結果，並區分「測試失敗」與「操作被中止」。後面的診斷欄位不是每筆都有意義。',
'DSTS byte0高4bits是測試類型、低4bits是結果；SEGN byte1僅特定結果有效。VDINFO byte2分別標NSID、FLBA、SCT、SC是否有效；POH bytes11:4記完成／中止時通電小時，NSID15:12與FLBA23:16描述失敗對象。',
'VDINFO的FVLD=0時，即使FLBA bytes全0，也不能宣稱LBA0故障。DSTR=2是Controller Level Reset中止，也不等於測出媒體損壞。'],[
'Interpret an individual test result here, distinguishing detected failures from aborted operations. Diagnostic fields are not universally valid.',
'DSTS byte 0 high 4 bits gives test type and low 4 result; SEGN byte 1 is valid for a specific result. VDINFO byte 2 independently validates NSID, FLBA, SCT and SC. POH bytes 11:4 timestamps completion/abort in power-on hours; NSID bytes 15:12 and FLBA bytes 23:16 identify the failing target.',
'If FVLD is zero, all-zero FLBA bytes do not establish failure at LBA 0. DSTR=2 means a Controller Level Reset aborted the test, not a detected media failure.'],'B218 B102')

card('B443','Namespace Attachment：建立後還要附加到 controller','Namespace Attachment|SEL|Attach|Detach|Controller List',[
'namespace存在但某個controller看不到時，查attachment動作及controller list。建立儲存物件與讓某controller存取，是不同操作。',
'CDW10.SEL bits3:0的0表示Attach、1表示Detach，其他值保留。實際namespace由NSID指定，目標controllers在資料buffer清單中。此表的SEL數值不能套到Namespace Management。',
'Detach不等於Delete：它解除controller與namespace的關聯，不是直接刪除namespace。若清單處理失敗，Error Information可提供第一個失敗entry的byte offset，不能假設後續controllers都已處理。'],[
'When a namespace exists but is inaccessible through one controller, inspect attachment and the controller list. Creating storage and making it accessible through a controller are different operations.',
'CDW10.SEL bits 3:0 values 0/1 mean Attach/Detach; other values are reserved. NSID chooses the namespace and a buffer lists target controllers. These SEL meanings differ from Namespace Management.',
'Detach is not Delete: it removes an association. On list-processing failure, Error Information can locate the first failed entry by byte offset; do not assume later controllers were processed.'],'B446 B212')

card('B446','Namespace Management：Create、Delete 或 Restore','Namespace Management|SEL|Create|Delete|Restore',[
'這張表用來辨認主機要求改變namespace配置的哪一種動作。單靠opcode無法區分Create與Delete。',
'CDW10.SEL bits3:0的0／1／2分別為Create、Delete、Restore Default Namespace Configuration。其餘bits保留；資料buffer與NSID的用途依動作而變，Create還需搭配CSI選格式。',
'Create成功回傳的新NSID，只證明namespace已建立，不保證已附加給目標controller。Restore是恢復預設namespace配置，不是任意備份snapshot的還原。'],[
'This selector distinguishes namespace-management actions that share one opcode. Opcode alone cannot tell Create from Delete.',
'CDW10.SEL bits 3:0 values 0/1/2 select Create, Delete or Restore Default Namespace Configuration. Other bits are reserved. Buffer and NSID interpretation depends on the action; Create also uses CSI to select its format.',
'A successfully returned new NSID establishes creation, not attachment to the desired controller. Restore means the default namespace configuration, not restoration of an arbitrary backup snapshot.'],'N134 B443')

card('N134','Create Namespace buffer：哪些欄位由主機填','NSZE|NCAP|FLBAS|DPS|NMIC|NPHNDLS|Placement Handle',[
'建立NVM namespace時，此表列出主機可以指定的buffer位置。它只沿用部分Identify欄位，不應把完整Identify回覆不加修改地當Create輸入。',
'NSZE在bytes7:0、NCAP15:8、FLBAS26、DPS29、NMIC30，後面有ANAGRPID、NVMSETID、ENDGID。LBSTM在391:384，FDP使用NPHNDLS393:392及從512開始的Placement Handle list；保留區須按Create格式處理。',
'支援並啟用FDP時，placement handle清單建立到RUH的對應；不支援或未啟用時不能依這些bytes宣稱配置有效。NSZE與NCAP仍以所選格式的blocks為單位，不是bytes。'],[
'This table lists host-specified positions for NVM namespace creation. It reuses only part of Identify, so a complete Identify response is not an unmodified Create payload.',
'NSZE occupies bytes 7:0, NCAP bytes 15:8, FLBAS byte 26, DPS byte 29 and NMIC byte 30, followed by group identifiers. LBSTM occupies bytes 391:384. FDP uses NPHNDLS bytes 393:392 and the Placement Handle list from 512; reserved areas follow the Create definition.',
'With FDP supported and enabled, the list maps placement handles to RUHs. Otherwise those bytes cannot establish a valid mapping. NSZE/NCAP still count blocks of the chosen format, not bytes.'],'N123 N125 B294')

card('B195','Format CDW10：格式編號與清除選項','Format NVM|LBAFL|LBAFU|SES|LBAFEE|PI|MSET',[
'Format要求的是哪個資料格式、是否同時secure erase，用此表解CDW10。Base先定共同外框，PI和metadata語意要接NVM補充。',
'LBAFL bits3:0與LBAFU13:12組成format index；LBAFU須符合LBAFEE條件。SES bits11:9的0／1／2分別為不要求secure erase、User Data Erase、Cryptographic Erase。PIL8、PI7:5與MSET4依command set解讀。',
'format index是清單索引，不是bytes或LBA大小。SES=1後資料內容不保證為零；若驗證程式只接受全0，會把允許的其他擦除後內容誤判成失敗。'],[
'Decode the selected format and erase request here. Base supplies the common envelope; NVM defines PI and metadata semantics.',
'LBAFL bits 3:0 with LBAFU bits 13:12 forms the format index, with LBAFU subject to LBAFEE. SES bits 11:9 values 0/1/2 request no secure erase, User Data Erase or Cryptographic Erase. PIL bit 8, PI bits 7:5 and MSET bit 4 are command-set-specific.',
'A format index selects a list entry, not a byte size. SES=1 does not guarantee zero-filled data; a validator that accepts only zeros can reject permitted post-erase contents.'],'N91 N125')

card('N91','NVM Format 補充：PI 類型與 metadata 放置','Format NVM|PIL|PI|MSET|Type 1|Type 2|Type 3',[
'這張表補上Base Format表留給NVM的三個欄位。PI type與Guard位寬不是同一組選擇，不能因Type3就當成64-bit Guard。',
'MSET bit4選extended LBA或separate buffer；PI bits7:5的0停用、1／2／3啟用對應保護類型；PIL bit8表示PI位置。NVM Command Set 1.0及後續版本要求PIL清0，PI放metadata尾端。',
'選MSET=1、PI=1是extended LBA加Type1保護。實際metadata大小與Guard格式，仍要讀所選LBAF／ELBAF，而不是從這兩個值推算。'],[
'This table fills the three NVM-specific fields left by Base Format. PI type and Guard width are different selections; Type 3 does not mean 64-bit Guard.',
'MSET bit 4 chooses extended LBA or separate metadata. PI bits 7:5 disables protection at 0 or selects Types 1/2/3. PIL bit 8 chooses PI position; NVM Command Set 1.0 and later requires PIL=0, placing PI at the metadata tail.',
'MSET=1/PI=1 selects extended LBA with Type 1 protection. Obtain metadata size and Guard format from the selected LBAF/ELBAF instead of inferring them from these two controls.'],'B195 N125 N128')

card('B451','Subsystem Sanitize：動作與完成模式','Sanitize|SANACT|AUSE|OWPASS|NDAS|EMVS|PREQ',[
'查整個NVM subsystem的Sanitize要求時，這張表解動作、覆寫次數及後續狀態選項。命令接受與sanitize完成必須分開驗證。',
'SANACT bits2:0選1退出failure、2 Block Erase、3 Overwrite、4 Crypto Erase、5退出Media Verification；AUSE bit3選完成模式。OWPASS7:4、OIPBP8供Overwrite使用；NDAS9、EMVS10、PREQ11另控制deallocation、驗證與purge要求。',
'Overwrite的OWPASS=0表示16次，不是0次。操作成功接受後應讀LID81h追蹤SOS等結果，不能把Admin CQE success或單一SPROG值當成已成功清除。'],[
'Decode subsystem-wide sanitize action, overwrite passes and subsequent-state options here. Acceptance of the command and completion of sanitization require separate observations.',
'SANACT bits 2:0 selects 1 exit failure, 2 Block Erase, 3 Overwrite, 4 Crypto Erase or 5 exit Media Verification. AUSE bit 3 selects completion mode. OWPASS bits 7:4/OIPBP bit 8 apply to overwrite; NDAS bit 9, EMVS bit 10 and PREQ bit 11 control deallocation, verification and purge requests.',
'For overwrite, OWPASS=0 means 16 passes, not none. After acceptance, inspect LID=81h and SOS; Admin CQE success or a single SPROG value does not prove successful sanitization.'],'B312 B454')

card('B454','Namespace Sanitize：PREQ 的 bit 位置不同','Sanitize Namespace|SANACT|PREQ bit4|EMVS|NSID',[
'針對單一namespace的Sanitize命令有自己的CDW10格式。它不能直接複製subsystem Sanitize的所有控制位。',
'SANACT bits2:0、AUSE bit3、PREQ bit4、EMVS bit10有效；開始操作的動作是Crypto Erase=4，Block Erase與Overwrite編碼在此保留。bits9:5與31:11保留。',
'例如CDW10=0000041Ch包含SANACT4、AUSE1、PREQ1及EMVS1。若把PREQ放到subsystem用的bit11，這裡寫到的是保留位，不是提出purge要求。'],[
'Namespace Sanitize has its own CDW10 layout. Do not copy every control bit from subsystem Sanitize.',
'Valid controls include SANACT bits 2:0, AUSE bit 3, PREQ bit 4 and EMVS bit 10. Crypto Erase 4 starts an operation; Block Erase and Overwrite encodings are reserved here. Bits 9:5 and 31:11 are reserved.',
'CDW10=0000041Ch contains SANACT=4, AUSE=1, PREQ=1 and EMVS=1. Placing PREQ at the subsystem command’s bit 11 instead writes a reserved bit, not a purge request.'],'B451 B312')

card('B312','Sanitize Status：進度、結果與目前狀態','LID 81h|SPROG|SOS|SCDW10|SSI|GDE|NDE|STNSID',[
'這張log同時回答背景操作進行到哪裡、最近結果與當前sanitize state。查詢時先確認是subsystem還是namespace目標，再套欄位語意。',
'SPROG bytes1:0為進度分數，status內SOS區分從未操作、成功、進行中、失敗等。SCDW10保存啟動參數；估計時間欄位有各自的0／FFFFFFFFh意義。SSI補目前state及failure state，另有清除狀態與STNSID等目標資訊。',
'SPROG=FFFFh不能單獨當成功：SOS=3仍代表失敗。解析SCDW10時，也要按目標選Figure451或454，尤其PREQ的bit位置不同。'],[
'This log reports progress, the latest outcome and current sanitize state. Determine whether the queried target is a subsystem or namespace before decoding scope-dependent fields.',
'SPROG bytes 1:0 is a progress fraction; SOS distinguishes never run, success, processing and failure. SCDW10 records starting parameters. Estimated-time fields have individual zero/FFFFFFFFh meanings. SSI supplements state/failure details alongside erased-state and STNSID information.',
'SPROGFFFFh alone is not success: SOS=3 still means failure. Decode SCDW10 using Figure 451 or 454 according to target, especially the different PREQ position.'],'B451 B454 B234')

card('B541','Namespace Write Protection：目前保護狀態','FID 84h|WPS|Write Protect|Permanent Write Protect',[
'寫入命令被拒絕時，查此namespace目前WPS，再分辨是否可解除、需power cycle或永久保護。這不是Boot Partition的保護編碼。',
'CDW11 bits2:0為WPS：0未保護，1一般保護，2直到power cycle，3永久保護。支援能力與進入許可另查NWPC及Write Protection Control；WPS只描述要求或回報的狀態。',
'已進入WPS=2或3後，直接Set Features要求改回0會得到Feature Not Changeable。不能因SEL=3回CHANG=1，就判定當前永久狀態可以反轉。'],[
'When writes are rejected, inspect namespace WPS to distinguish reversible, power-cycle-bound and permanent protection. Boot Partition protection uses different encodings.',
'CDW11.WPS bits 2:0 values 0/1/2/3 mean unprotected, protected, until-power-cycle and permanent. NWPC and Write Protection Control separately govern capability and entry permission; WPS describes requested/reported state.',
'Once WPS=2 or 3 is entered, requesting 0 through Set Features returns Feature Not Changeable. SEL=3.CHANG=1 does not make a permanent current state reversible.'],'B201 B346 B542')

card('B542','Boot Partition 保護：兩個 partition 的獨立欄位','FID 85h|BP0WPS|BP1WPS|RPMB|Boot Partition',[
'Boot Partition更新被阻擋時，查兩個partition各自的保護狀態。此表的0不是「未保護」，與namespace WPS不同。',
'BP0WPS bits2:0、BP1WPS bits5:3：0僅供Set使用、表示不要求改變；1解鎖、2鎖定、3鎖至power cycle。4表示由RPMB控制，只能回報，不能作Set要求；預設兩者都是鎖定。',
'要只解鎖partition0並保留partition1原狀，兩欄分別為1與0，CDW11=1。不能把兩欄都清0當作解鎖兩個partition；若 NVM subsystem 的 CTRATT.MDS=1，且該 Boot Partition 由多個 controller 共享，將它設成3（鎖至 power cycle）的要求會以 Feature Not Changeable 中止。'],[
'Check each Boot Partition’s protection when updates are blocked. Zero does not mean unprotected as it does for namespace WPS.',
'BP0WPS bits 2:0 and BP1WPS bits 5:3 encode 0 no requested change (Set only), 1 unlocked, 2 locked and 3 locked until power cycle. Value 4 reports RPMB-controlled protection and is reserved for Set. Both default to locked.',
'To unlock partition 0 while leaving partition 1 unchanged, use 1 and 0, producing CDW11=1. Clearing both fields does not unlock both partitions. If CTRATT.MDS=1 and multiple controllers share the Boot Partition, requesting state 3 (locked until power cycle) fails with Feature Not Changeable.'],'B541 B187')
