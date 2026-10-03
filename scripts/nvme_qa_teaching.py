"""Volume introductions and worked teaching aids; examples are hypothetical."""
from scripts.nvme_qa_model import pair

VOLUMES = [
('initialization',1,9,'Controller 初始化與停用','Controller initialization and disable'),
('queues',10,21,'Admin Queue 與 I/O Queue','Admin and I/O queues'),
('doorbells',22,30,'Doorbell、Queue Full 與 Wrap-around','Doorbells, full queues and wrap-around'),
('commands',31,43,'Command、Completion 與處理順序','Commands, completions and processing order'),
('identify',44,53,'Identify 與能力探索','Identify and capability discovery'),
('features',54,68,'Get Features 與 Set Features','Get Features and Set Features'),
]

INTRO = {k:pair(v) for k,v in {
'initialization':'先理解 controller 如何從停用轉為就緒，再開始處理命令。讀到能力，不表示 controller 已啟用；Host 設定 EN，也還要等待 RDY。即使 RDY=1，仍可能需要依 Ready Mode 確認媒體是否可用。本冊將狀態、等待時間及允許執行的動作放在一起，說明每個階段應如何判斷。 || Understand controller state transitions before commands. Discovering capabilities is not enabling; setting EN is not readiness; RDY=1 need not establish readiness of every media operation. This volume connects timing, state and permitted actions.',
'queues':'Host 準備的 queue 記憶體、controller 分配的 queue 配額，以及已成功建立的 queue，是三種不同資訊。本冊先說明 SQ 與 CQ 的依賴關係，再討論大小、識別碼、刪除及重設，讓你能判斷何時可以使用 queue，以及何時能安全回收記憶體。 || Queue memory, allocated queue counts and successfully created queues are distinct. Learn SQ/CQ dependencies before size, identifiers, deletion and reset so memory can be reclaimed at the right time.',
'doorbells':'Doorbell 告訴 controller，Host 的指標已前進到哪個位置；Phase 則讓 Host 分辨 CQ 中的是新完成結果，還是上一圈留下的資料。本冊將位置與有效性一起說明，幫助你正確處理繞回及空間釋放，避免將正常繞回誤判成倒退，或把舊 CQE 處理兩次。 || Doorbells communicate pointer positions; phase tells the host whether a CQ slot belongs to the next completion generation. Together they distinguish wrap-around from an invalid movement and new completions from stale ones.',
'commands':'從 Host 提交命令，到 controller 取得、處理並回報完成，再到 Host 回收資源，各階段能證明的事情不同。本冊沿著這條流程解讀 Command 與 CQE，並說明順序、仲裁及中斷各自控制什麼。只有完成順序，還不足以推論 controller 內部的全部行為。 || Follow submission, consumption, processing, completion and host reclamation to learn what each field proves. Ordering, arbitration, fairness and interrupts answer different questions; completion order alone cannot establish them all.',
'identify':'Identify 提供多種查詢結構。先確定要查哪個物件、需要哪一種資訊，再選擇 CNS、CSI、NSID 及其他欄位。本冊分別說明能力、目前配置與清單變更，讓你知道不同回覆如何互相補充，以及哪些差異才可能構成矛盾。 || Treat Identify as several distinct query interfaces. Choose the object and structure before CNS, CSI, NSID and other selectors. Separate capability, current configuration and changing lists to find real contradictions.',
'features':'設定 Feature 前，先確認它影響哪個物件、是否可變更，以及是否可保存。設定後，再分別確認命令成功、Current 讀回值、實際行為與重設後的恢復結果。本冊依這些步驟說明如何驗證設定，避免只看成功 CQE 就跳到功能一定正確的結論。 || Establish scope, changeability and saveability before Set. Completion, Current readback, actual behavior and restoration after reset are separate observations; a successful CQE does not replace them.',
}.items()}

# Each table has a single teaching purpose, named columns and a worked result.
AIDS = {
'initialization':dict(
 title=pair('從未啟用到能送命令 || From disabled to command submission'),
 takeaway=pair('重新啟用前，先確認上一輪停用已完成。啟用與停用都要觀察 RDY 的實際變化，不能只看 Host 自己寫入的 EN。 || Wait for the previous lifetime to end before configuring the next; both waits require RDY, not merely the EN value written by the host.'),
 headers=[pair(x) for x in ['階段 || Stage','觀察／動作 || Observation or action','下一步的條件 || Condition for advancing']],
 rows=[[pair(c) for c in r] for r in [
 ['停用完成 || Disable complete','CC.EN=0；CSTS.RDY=0 || CC.EN=0; CSTS.RDY=0','設定 AQA、ASQ、ACQ 與 CC || Configure AQA, ASQ, ACQ and CC'],
 ['啟用中 || Enabling','Host 將 EN 從 0 設為 1，並開始計時 || EN 0→1 starts the timer','等待 RDY=1，同時檢查 CFS 及適用的 timeout || Wait for RDY=1; check CFS and applicable timeout'],
 ['介面就緒 || Interface ready','RDY=1；依 Ready Mode 判斷媒體限制 || RDY=1; apply media restrictions for the ready mode','先執行允許的 Admin 命令，再建立 I/O queue || Submit permitted Admin commands, then create I/O queues'],
 ['再次停用 || Disabling again','Host 將 EN 從 1 清為 0，並停止提交新命令 || EN 1→0; stop new submissions','等待 RDY=0，才開始下一次初始化 || Wait for RDY=0 before another lifetime'],
 ]],
 example=pair('假設 CAP.TO=4，停用等待上限為 4×500 ms=2 s。這個期限用來等待 controller 停用，不是每筆 I/O 命令的 timeout。啟用時還須根據 CAP.CRMS、所選 Ready Mode 及 CRTO 決定期限，因此不能將這個 2 s 套用到所有等待情況。 || With hypothetical CAP.TO=4, the disable timeout is 4×500 ms=2 s. This is not an I/O command timeout. Enable additionally requires CAP.CRMS and the selected CRTO rules; 2 s is not universal.'),
 refs=['cc','cap','adminreg','crto','init','ready']),
'queues':dict(
 title=pair('一條 CQ、兩條 SQ：先建立依賴對象，刪除時則反過來 || One CQ and two SQs: creation and reclamation run in opposite directions'),
 takeaway=pair('SQ 的命令要透過關聯的 CQ 回報完成。因此，只要仍有 SQ 使用某條 CQ，就不能先刪除那條 CQ。 || The CQ is the completion destination for its SQs; it cannot be deleted while an SQ still depends on it.'),
 headers=[pair(x) for x in ['觀察層次 || Observation','教學假設 || Hypothetical value','可以推論什麼 || What it establishes']],
 rows=[[pair(c) for c in r] for r in [
 ['數量配額 || Count allocation','FID07h 回 NSQA=3、NCQA=1 || FID07h returns NSQA=3, NCQA=1','可建立 4 條 I/O SQ、2 條 I/O CQ；這時還沒有建立 queue || 4 I/O SQs and 2 I/O CQs allocated, not created'],
 ['單一 queue 深度 || Queue depth','Create CQ：QID=1、QSIZE=7 || Create CQ: QID=1, QSIZE=7','共有 8 個位置；環狀 queue 須保留一格，用來區分已滿與空佇列 || 8 entries; the ring reserves one slot to distinguish full'],
 ['依賴關係 || Dependencies','SQ1.CQID=1；SQ2.CQID=1 || SQ1.CQID=1; SQ2.CQID=1','先建 CQ1，再建 SQ1、SQ2 || Create CQ1 before SQ1 and SQ2'],
 ['回收順序 || Reclamation','刪 SQ1、SQ2，各自等成功完成 || Delete SQ1/SQ2 and wait for their successful completions','最後再刪 CQ1，並在各 queue 的使用期間結束後回收對應記憶體 || Delete CQ1 next; reclaim memory after the relevant lifetime ends'],
 ]],
 example=pair('假設 SQ1 已刪除，但 SQ2 仍存在。這時不能刪除 CQ1，因為 SQ2 還要使用它回報命令結果。另外，SQ1 刪除完成只結束 SQ1 的使用期間，不表示仍由 SQ2 使用的資料 buffer 也可以回收。 || If SQ1 is deleted but SQ2 remains, deleting CQ1 is still an invalid sequence: SQ2 still uses it. SQ1 deletion also does not authorize reclaiming SQ2 data buffers.'),
 refs=['number','create','delete','queue']),
'doorbells':dict(
 title=pair('8 格 CQ：把繞回與 Phase 放在同一張表 || An eight-entry CQ: wrap-around and phase together'),
 takeaway=pair('CQ 索引回到 0，不表示位置 0 裡的舊資料重新有效。Host 還要比對這一圈期待的 Phase，才能確認是否已有新 CQE。 || Returning to slot 0 does not make old data valid again; the host must also compare the expected phase.'),
 headers=[pair(x) for x in ['時點 || Point in time','Host 下一格／預期 Phase || Host next slot / expected phase','讀取結果與動作 || Read result and action']],
 rows=[[pair(c) for c in r] for r in [
 ['初始化 || Initialization','位置 0，預期 P=1；記憶體 P 初始化為 0 || Slot 0, expect P=1; initialize memory P to 0','目前沒有新完成 || No new completion yet'],
 ['第一輪末端 || End of first traversal','位置 7，預期 P=1 || Slot 7, expect P=1','讀到 P=1：處理 CQE，下一格回 0，預期改 0 || P=1: consume CQE, wrap to 0, change expectation to 0'],
 ['第二輪起點 || Start of second traversal','位置 0，預期 P=0 || Slot 0, expect P=0','若仍是舊 P=1，不處理；讀到新 P=0 才處理 || Ignore stale P=1; consume only new P=0'],
 ['通知 controller 已處理的範圍 || Report consumption','CQ Head 從 7 更新成 2 || CQ Head advances from 7 to 2','表示位置 7、0、1 的 3 筆 CQE 已處理完畢，不是指標倒退 5 格 || Consumed slots 7, 0, 1: 3 entries, not a retreat by 5'],
 ]],
 example=pair('這次前進距離為 (2−7+8) mod 8=3，所以 Host 將 Doorbell 寫成位置 2，通知 controller 有 3 格已可重用；不是因為寫了 2，就表示釋放 2 格。Phase 用來確認 Host 讀到的是新 CQE，CQ Head Doorbell 則通知 controller 哪些 CQE 已處理完畢，兩者負責不同工作。 || Modular distance is (2−7+8) mod 8=3. The doorbell reports position 2, not “free two more slots.” Phase establishes CQE validity; the head doorbell reports consumption to the controller.'),
 refs=['queue','cqe','pcie']),
'commands':dict(
 title=pair('同一筆命令，五個不同的觀察時點 || Five observations during one command lifetime'),
 takeaway=pair('觀察到流程有進展，不表示命令已成功完成。先確認觀察的是哪個階段，才能知道這份資訊足以支持什麼結論。 || Evidence of progress is not evidence of success; identify the stage you actually observed.'),
 headers=[pair(x) for x in ['時點 || Stage','能確認的事情 || What is established','尚不能確認的事情 || What is not yet established']],
 rows=[[pair(c) for c in r] for r in [
 ['寫好 SQE || SQE prepared','Host 已填 Opcode、CID、NSID、資料指標 || Host filled opcode, CID, NSID and data pointers','controller 是否已能看見這筆 SQE || Controller visibility'],
 ['更新 SQ Tail || SQ tail updated','命令已提交；Host 仍須另行確保記憶體內容對 controller 可見 || Submission, with separately ensured memory visibility','controller 是否已取得 SQE，或命令是否已完成 || Consumption or completion'],
 ['CQE 回報 SQHD 前進 || A CQE reports an advanced SQHD','controller 已消費至回報的位置 || Consumption reached the reported position','這些位置原先放置的命令是否全部完成 || Completion of all commands from those slots'],
 ['目標 CQE Phase 有效 || Target CQE has valid phase','可用 SQID＋CID 對回這筆完成，讀 SCT／SC || Correlate SQID+CID and inspect SCT/SC','中斷是否已送達，以及資料是否已持久保存 || Interrupt delivery or unconditional persistence'],
 ['Host 更新 CQ Head || Host advances CQ head','Host 已處理 CQE，並釋放對應的 CQ 空間 || Host consumed completions and released CQ space','其他 SQ 或其他 CID 的命令是否也已完成 || Completion of other SQs or CIDs'],
 ]],
 example=pair('SQ1 的 CID=7 與 SQ2 的 CID=7 可以同時存在。若它們共用 CQ，Host 只看到 CID=7 還無法找到原命令，必須搭配 CQE.SQID 才能正確配對。若要進一步確認 Write 的資料是否已持久保存，還需核對 WCE、FUA 或 Flush 的完成條件，不能只看成功 Status。 || SQ1/CID7 and SQ2/CID7 can coexist. In a shared CQ, CID7 alone is insufficient: read SQID. Write persistence additionally requires WCE, FUA or Flush completion conditions, not only success status.'),
 refs=['sqe','cqe','order','vwc','nvmatomic']),
'identify':dict(
 title=pair('先選問題，再選 Identify 結構 || Choose the question before the Identify structure'),
 takeaway=pair('每個 CNS 回答的問題不同。namespace 已配置，只表示它存在，不能直接推論目前這個 controller 已能存取它。 || Different CNS values answer different questions; allocated does not automatically mean accessible through this controller.'),
 headers=[pair(x) for x in ['想知道什麼 || Question','查詢入口 || Query','回覆如何使用 || How to use the response']],
 rows=[[pair(c) for c in r] for r in [
 ['controller 宣告的能力 || Advertised controller capability','CNS=01h || CNS=01h','讀取 OACS、ONCS、MDTS 等欄位，並依各欄位的有效條件判讀 || Read OACS, ONCS, MDTS and their field conditions'],
 ['目前可存取的 namespaces || Currently active namespaces','CNS=02h || CNS=02h','取得此 controller 的 Active List；這不是全部已配置 namespace 的清單 || Active list, not all allocated capacity'],
 ['已配置的 namespaces || Allocated namespaces','支援 Namespace Management 時用 CNS=10h || CNS=10h with Namespace Management support','清單可包含未 attach 到此 controller 的 namespace || May include namespaces not attached to this controller'],
 ['單一 NVM namespace 的格式 || Format of one NVM namespace','CNS=00h；需要時加 CNS=05h、CSI=00h || CNS=00h; additionally CNS=05h, CSI=00h when applicable','NSZE／NCAP、FLBAS、LBAF 與 PI 格式共同解讀 || Interpret NSZE/NCAP, FLBAS, LBAF and PI together'],
 ['不依賴命令集的 namespace 屬性 || Command-set-independent namespace properties','CNS=08h || CNS=08h','使用此結構解讀共通屬性，不要套用 NVM 特定 LBA 格式結構的欄位位置 || Keep separate from the NVM-specific LBA format structure'],
 ]],
 example=pair('假設 Allocated List={1,2}，而目前 controller 的 Active List={1}。這表示 namespace 2 不在此 controller 的 Active List 中，但不能據此判定它已被刪除。下一步應確認附加關係及適用狀態，並保留 controller 身分與查詢時間，讓前後資料可以正確比較。 || If Allocated={1,2} and this controller’s Active={1}, namespace2 is absent from this active list; that does not establish deletion. Check attachment and relevant state, preserving controller identity and query time.'),
 refs=['idcmd','idctrl','idlist','idns','nsmanage']),
'features':dict(
 title=pair('Current 與 Saved：兩條不同的設定路徑 || Current and Saved follow different update paths'),
 takeaway=pair('SV=0 只變更目前值；SV=1 才同時要求保存。重設後如何恢復，還要看 Feature 的作用範圍、保存能力及個別例外。 || SV=0 changes the present value; SV=1 requests saving. Restoration additionally depends on scope, saveability and feature exceptions.'),
 headers=[pair(x) for x in ['動作 || Action','Current || Current','Saved／下一次恢復 || Saved / subsequent restoration']],
 rows=[[pair(c) for c in r] for r in [
 ['教學起點：可保存的 Feature || Start with a saveable feature','A || A','Saved=A || Saved=A'],
 ['Set B，SV=0，成功 || Successful Set B, SV=0','B || B','仍是 A || Remains A'],
 ['發生會恢復 Saved 的重設 || A reset restoring Saved','回到 A || Returns to A','A || A'],
 ['Set C，SV=1，成功 || Successful Set C, SV=1','C || C','更新成 C || Updates to C'],
 ['再次發生相同重設 || Same reset again','回到 C || Returns to C','C || C'],
 ]],
 example=pair('這張表假設 Feature 可保存，而且所執行的重設會從 Saved 恢復 Current。若前提不同，就不能直接套用。例如 FID84h 不可保存，也沒有 Default，但 WPS=1 的基本保護仍會跨越 Power Cycle 保留；WPS=2 則在 Power Cycle 後解除。它們的持續性由保護模式本身決定。 || This table assumes a saveable feature and a reset that restores Saved. It is not universal: FID84h is unsaveable with no Default, yet basic WPS1 survives power cycling and WPS2 clears on a power cycle.'),
 refs=['feature','getfeat','setfeat','nwp']),
}

# Extra course material is exclusive to the independent Chinese HTML.
LESSONS = {
'initialization':[
('先分清誰寫、誰回報','CC.EN 由 Host 寫入，表示要求啟用或停用；CSTS.RDY 由 controller 回報，表示它目前是否就緒。就像按下電源開關與系統完成開機是兩個時點，驗證時也必須記錄 EN 變化與 RDY 變化各自的時間。單看 EN=1，只能證明 Host 已要求啟用，不能證明 controller 已準備好。'),
('Independent mode 為什麼需要兩個期限','Independent mode 允許管理介面先就緒，再等待媒體能夠提供服務。CRIMT 對應介面就緒的期限，CRWMT 對應媒體就緒的期限；兩者都從 EN 由 0 變成 1 時起算。例如介面在 300 ms 就緒，而媒體期限是 2 s，媒體剩下的等待時間就是 1.7 s，不會從介面就緒時重新獲得 2 s。實際採用哪個期限，仍須依 CAP.TO 與 CRTO 的比較規則決定。'),
('重設後的位元仍在，不代表物件仍在','由清除 CC.EN 觸發的 Controller Reset 會保留 AQA、ASQ、ACQ，因此 Host 不必只因這種重設就重新提供相同的基底位址。不過，Admin Queue 指標已重設，I/O queue 也已刪除。如果 Host 繼續用舊 CID 紀錄配對新 CQE，可能把前一次 queue 留下的資料當成新結果。因此，重建命令追蹤狀態也是恢復流程的一部分。')],
'queues':[
('把配額、深度與記憶體容量分開算','FID07h 的回覆決定能建立多少條 I/O queue；Create Queue 的 QSIZE 決定一條 queue 有多少個位置；每個位置的大小，則用來計算需要多少記憶體。例如一條 NVM I/O SQ 有 64 個位置，每個位置 64 bytes，總共需要 4096 bytes。這不表示 controller 分配了 64 條 SQ；由於環狀 queue 需保留一格，也不表示能同時放入 64 筆尚未消費的 SQE。'),
('CQ 共用帶來什麼取捨','多條 SQ 共用 CQ，可以集中處理完成通知。不過，如果一條繁忙 SQ 產生大量 completion，將 CQ 空間占滿，其他共用者也可能受到阻塞。各自使用 CQ，則能隔離這種空間壓力。這項取捨關乎完成結果放在哪裡，與 namespace 的資料是否共享是不同問題。'),
('刪除的完成點比刪除的提交點重要','Host 送出 Delete SQ 後，controller 仍可能需要處理已取得的命令，因此不能在提交刪除命令的同時，就立刻釋放原記憶體。等 Delete SQ 成功完成，才到達規範定義的刪除完成點。某些命令即使沒有各自的 CQE，也可能已依規則被隱含中止；Host 應按刪除規則清理追蹤資料，而不是無限等待這些 completion。')],
'doorbells':[
('指標是位置，差值才是數量','Doorbell 中的 2 表示索引位置 2，不表示這次提交了 2 筆。對 8 個位置的環狀 queue，從 7 前進到 2，經過的是 7、0、1，共 3 個位置。如果只用一般數字大小比較，看到 2<7 就判定倒退，便會把正常繞回誤認為非法操作。'),
('Phase 不是成功位元','Phase 只用來判斷這個 CQ 位置是否包含目前這一圈的新完成結果。即使 Phase 有效，CQE 內仍可能是失敗 Status；反過來，舊 CQE 即使留有 Success，只要 Phase 不符合期待值，就不能再處理一次。因此，先確認有效性，再解讀 SCT 與 SC，才能避免誤讀殘留資料。'),
('為何 Host 處理完還要寫 CQ Head','Host 在自己的程式中將 CQE 標記為已處理，並不會自動通知 controller。必須更新 CQ Head Doorbell，controller 才能得知哪些位置已可重用。如果漏掉這一步，即使 Host 已處理完所有結果，controller 仍可能因 CQ Full 而停住。這時應檢查空間釋放流程，而不是先把停滯歸因於媒體延遲。')],
'commands':[
('從欄位反推它真正能證明的事','SQHD 回報 controller 已消費到的 SQ 位置，CID 則識別這次完成的是哪筆命令。例如同一 CQE 回報 SQHD=4、CID=9，只能分別知道 SQ 消費進度及已完成命令的識別碼，不能據此宣稱 SQ 的前 4 筆命令全部完成。controller 可以先取得多筆 SQE，再以不同順序完成命令。'),
('錯誤碼先做單一原因實驗','假設一筆命令同時含有非法 NSID 與非法資料指標，controller 可能先發現其中任一錯誤。如果把它當成只測 NSID 的案例，就可能因實際回報另一種合法錯誤而誤判。比較 Status 前，先建立參數及狀態都合法的基準，再每次只改一項，並記錄作用範圍與支援能力，才能知道結果是由哪個條件造成。'),
('正常寫入與 fused operation 的順序不同','兩筆普通命令即使放在相鄰的 SQ 位置，也不會自動成為不可分割的操作。支援的 fused pair 必須設定對應 FUSE 值，放在同一 SQ 的相鄰位置，並透過同一次 Tail 更新提交；兩筆仍各自有完成結果。判斷一般排程時也要分清楚開始處理與完成：不同命令耗時不同，因此整體吞吐比例不一定等於仲裁權重。')],
'identify':[
('從裝置、容量到可見性，分三次問','Identify Controller 描述 controller 的能力與屬性；Identify Namespace 描述指定 namespace 的格式及容量；Active List 則列出目前可經由這個 controller 使用的 namespace。這三份資料各自回答不同問題，必須互相配合。不能只讀到 Controller.NN，就認定 NSID 從 1 到 NN 全都存在，而且全部可存取。'),
('欄位是位元遮罩還是索引，會改變算式','解讀數值前，先確認欄位的資料型態：CNS 選擇資料結構，CSI 選擇命令集，bitmap 的各位元代表不同能力，index 則指出清單中的某一筆。例如讀取 LBA 格式時，先從 FLBAS 解出索引，再讀取對應的 LBAF 描述；不能把 FLBAS 的原始數字直接當成 byte 數。知道數值用來選擇什麼，比單獨背下十六進位值更容易正確運用。'),
('查詢結果也有時間','要觀察管理操作的結果，必須等操作成功後再查詢：Create 成功後查 Allocated List，Attach 成功後查目標 controller 的 Active List。如果另一個管理者同時修改配置，兩份清單可能來自不同時點。先確認查詢順序及對象，再判斷 controller 是否漏了更新，才能避免把正常的時間差當成錯誤。')],
'features':[
('先問能不能，再問目前是多少','Get Features.SEL=3 回傳的是能力，例如是否可變更及是否可保存，而不是目前正在使用的設定。假設 DW0=5，表示能力欄位的 bit2 與 bit0 為 1，不能直接拿來和 Current=5 比較。比較兩次 Get 的結果前，先確認 FID、SEL 及作用對象一致，才能知道它們是否描述同一件事。'),
('APST 的狀態轉移該怎麼讀','假設目前處於 PS0，APSTE=1，PS0 entry 的 ITPT=2000 ms、ITPS=3，而且 PS3 是受支援的非工作狀態。controller 在 PS0 持續閒置超過 2000 ms 後，會轉入 PS3；之後若有工作需要離開 PS3，恢復處理時就要考慮 PS3.EXLAT 所描述的退出延遲。ITPT 是進入前的閒置門檻，EXLAT 是離開時的延遲，兩者發生在不同階段，不能相加後宣稱每筆命令都固定等待這麼久。'),
('持久性與原子性要各做一個判斷','持久性問的是已完成資料在斷電後是否仍存在；原子性問的是一次更新是否可能留下部分新資料、部分舊資料。WCE、FUA 與 Flush 處理持久性；原子單位及邊界則限制哪些寫入具有原子性。即使資料已持久保存，超出原子保證範圍的多 block 操作，也不會因此自動取得整筆不可分割的保證。')],
}

from scripts.nvme_qa_teaching_extended import extend
extend(VOLUMES, INTRO, AIDS, LESSONS)
