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
'initialization':'先把 controller 的狀態轉移看懂，再處理命令。讀到能力不代表已啟用；設下 EN 不代表已 Ready；RDY=1 也不一定代表所有媒體存取都已就緒。這一冊用時間、狀態與可執行的動作來核對初始化。 || Understand controller state transitions before commands. Discovering capabilities is not enabling; setting EN is not readiness; RDY=1 need not establish readiness of every media operation. This volume connects timing, state and permitted actions.',
'queues':'Queue 的記憶體、controller 分配的數量，以及已成功建立的 queue，是三件事。先理解 SQ 與 CQ 的依賴，再看大小、識別碼、刪除與重設，才能判斷何時可以安全回收記憶體。 || Queue memory, allocated queue counts and successfully created queues are distinct. Learn SQ/CQ dependencies before size, identifiers, deletion and reset so memory can be reclaimed at the right time.',
'doorbells':'Doorbell 告訴另一端指標移到哪裡；Phase 告訴 Host，這個 CQ 位置是不是新一輪的完成。兩者一起使用，才不會把繞回誤判成倒退，或把舊完成誤判成新完成。 || Doorbells communicate pointer positions; phase tells the host whether a CQ slot belongs to the next completion generation. Together they distinguish wrap-around from an invalid movement and new completions from stale ones.',
'commands':'沿著提交、取得、處理、完成、Host 回收的流程，辨認每個欄位能證明什麼。命令順序、仲裁、公平性與中斷是不同問題；不能用一張完成順序清單推論全部行為。 || Follow submission, consumption, processing, completion and host reclamation to learn what each field proves. Ordering, arbitration, fairness and interrupts answer different questions; completion order alone cannot establish them all.',
'identify':'把 Identify 當成多個不同的查詢入口。先問「查誰、查哪一種資料」，再選 CNS、CSI、NSID 及其他 selector。能力、目前配置與清單變更分開核對，才能找出真正矛盾。 || Treat Identify as several distinct query interfaces. Choose the object and structure before CNS, CSI, NSID and other selectors. Separate capability, current configuration and changing lists to find real contradictions.',
'features':'先確認設定作用在哪裡、能不能改及保存，再執行 Set。成功完成、Current 回讀、實際行為與重設後恢復，都要各自確認；一次成功 CQE 無法替代這四個觀察。 || Establish scope, changeability and saveability before Set. Completion, Current readback, actual behavior and restoration after reset are separate observations; a successful CQE does not replace them.',
}.items()}

# Each table has a single teaching purpose, named columns and a worked result.
AIDS = {
'initialization':dict(
 title=pair('從未啟用到能送命令 || From disabled to command submission'),
 takeaway=pair('先等前一輪停完，再設定下一輪；兩次等待都要看 RDY，不能只看自己寫入的 EN。 || Wait for the previous lifetime to end before configuring the next; both waits require RDY, not merely the EN value written by the host.'),
 headers=[pair(x) for x in ['階段 || Stage','觀察／動作 || Observation or action','下一步的條件 || Condition for advancing']],
 rows=[[pair(c) for c in r] for r in [
 ['停用完成 || Disable complete','CC.EN=0；CSTS.RDY=0 || CC.EN=0; CSTS.RDY=0','設定 AQA、ASQ、ACQ 與 CC || Configure AQA, ASQ, ACQ and CC'],
 ['啟用中 || Enabling','EN 0→1，開始計時 || EN 0→1 starts the timer','等 RDY=1；檢查 CFS 與適用 timeout || Wait for RDY=1; check CFS and applicable timeout'],
 ['介面就緒 || Interface ready','RDY=1；依 Ready Mode 判斷媒體限制 || RDY=1; apply media restrictions for the ready mode','先送合法 Admin 命令，再建立 I/O queue || Submit permitted Admin commands, then create I/O queues'],
 ['再次停用 || Disabling again','EN 1→0；不再新增提交 || EN 1→0; stop new submissions','等 RDY=0，才開始下一輪 || Wait for RDY=0 before another lifetime'],
 ]],
 example=pair('假設 CAP.TO=4，停用等待上限的單位換算是 4×500 ms=2 s。這不是每筆 I/O 命令的 timeout。啟用則還須依 CAP.CRMS 與所選模式檢查 CRTO，不能把這個 2 s 套到所有情況。 || With hypothetical CAP.TO=4, the disable timeout is 4×500 ms=2 s. This is not an I/O command timeout. Enable additionally requires CAP.CRMS and the selected CRTO rules; 2 s is not universal.'),
 refs=['cc','cap','adminreg','crto','init','ready']),
'queues':dict(
 title=pair('一個 CQ、兩個 SQ：建立與回收是相反方向 || One CQ and two SQs: creation and reclamation run in opposite directions'),
 takeaway=pair('CQ 是 SQ 回報完成的目的地；仍有 SQ 依賴它時，不能先刪掉它。 || The CQ is the completion destination for its SQs; it cannot be deleted while an SQ still depends on it.'),
 headers=[pair(x) for x in ['觀察層次 || Observation','教學假設 || Hypothetical value','可以推論什麼 || What it establishes']],
 rows=[[pair(c) for c in r] for r in [
 ['數量配額 || Count allocation','FID07h 回 NSQA=3、NCQA=1 || FID07h returns NSQA=3, NCQA=1','分配 4 個 I/O SQ、2 個 I/O CQ；尚未建立 || 4 I/O SQs and 2 I/O CQs allocated, not created'],
 ['單一 queue 深度 || Queue depth','Create CQ：QID=1、QSIZE=7 || Create CQ: QID=1, QSIZE=7','8 個 entries；ring 要保留一格辨認 Full || 8 entries; the ring reserves one slot to distinguish full'],
 ['依賴關係 || Dependencies','SQ1.CQID=1；SQ2.CQID=1 || SQ1.CQID=1; SQ2.CQID=1','先建 CQ1，再建 SQ1、SQ2 || Create CQ1 before SQ1 and SQ2'],
 ['回收順序 || Reclamation','刪 SQ1、SQ2，各自等成功完成 || Delete SQ1/SQ2 and wait for their successful completions','再刪 CQ1；相關生命週期結束後才回收記憶體 || Delete CQ1 next; reclaim memory after the relevant lifetime ends'],
 ]],
 example=pair('假設 SQ1 已刪除，但 SQ2 仍存在。此時刪 CQ1 仍是非法順序，因為 SQ2 還要向 CQ1 回報。SQ1 的刪除完成，也不代表 SQ2 的資料 buffer 可以回收。 || If SQ1 is deleted but SQ2 remains, deleting CQ1 is still an invalid sequence: SQ2 still uses it. SQ1 deletion also does not authorize reclaiming SQ2 data buffers.'),
 refs=['number','create','delete','queue']),
'doorbells':dict(
 title=pair('8 格 CQ：把繞回與 Phase 放在同一張表 || An eight-entry CQ: wrap-around and phase together'),
 takeaway=pair('位置回到 0 不代表舊資料重新有效；Host 還要比對這一輪預期的 Phase。 || Returning to slot 0 does not make old data valid again; the host must also compare the expected phase.'),
 headers=[pair(x) for x in ['時點 || Point in time','Host 下一格／預期 Phase || Host next slot / expected phase','讀取結果與動作 || Read result and action']],
 rows=[[pair(c) for c in r] for r in [
 ['初始化 || Initialization','位置 0，預期 P=1；記憶體 P 初始化為 0 || Slot 0, expect P=1; initialize memory P to 0','目前沒有新完成 || No new completion yet'],
 ['第一輪末端 || End of first traversal','位置 7，預期 P=1 || Slot 7, expect P=1','讀到 P=1：處理 CQE，下一格回 0，預期改 0 || P=1: consume CQE, wrap to 0, change expectation to 0'],
 ['第二輪起點 || Start of second traversal','位置 0，預期 P=0 || Slot 0, expect P=0','若仍是舊 P=1，不處理；讀到新 P=0 才處理 || Ignore stale P=1; consume only new P=0'],
 ['通知已消費 || Report consumption','CQ Head 從 7 更新成 2 || CQ Head advances from 7 to 2','表示消費位置 7、0、1，共 3 格；不是倒退 5 格 || Consumed slots 7, 0, 1: 3 entries, not a retreat by 5'],
 ]],
 example=pair('算指標距離時使用 (2−7+8) mod 8=3。Doorbell 值是位置 2，並不是「新增釋放 2 格」。CQE 的 Phase 是有效性判斷；CQ Head Doorbell 則把已消費位置告知 controller，兩者不可互相代替。 || Modular distance is (2−7+8) mod 8=3. The doorbell reports position 2, not “free two more slots.” Phase establishes CQE validity; the head doorbell reports consumption to the controller.'),
 refs=['queue','cqe','pcie']),
'commands':dict(
 title=pair('同一筆命令，五個不同的觀察時點 || Five observations during one command lifetime'),
 takeaway=pair('看見進度不等於看見成功；先指出你觀察到哪一個階段。 || Evidence of progress is not evidence of success; identify the stage you actually observed.'),
 headers=[pair(x) for x in ['時點 || Stage','能確認的事情 || What is established','尚不能確認的事情 || What is not yet established']],
 rows=[[pair(c) for c in r] for r in [
 ['寫好 SQE || SQE prepared','Host 已填 Opcode、CID、NSID、資料指標 || Host filled opcode, CID, NSID and data pointers','controller 是否已看見 || Controller visibility'],
 ['更新 SQ Tail || SQ tail updated','命令已提交；記憶體可見性另須保證 || Submission, with separately ensured memory visibility','命令是否已取得或完成 || Consumption or completion'],
 ['CQE 回報 SQHD 前進 || A CQE reports an advanced SQHD','controller 已消費至回報的位置 || Consumption reached the reported position','那幾格的所有命令都已完成 || Completion of all commands from those slots'],
 ['目標 CQE Phase 有效 || Target CQE has valid phase','可用 SQID＋CID 對回這筆完成，讀 SCT／SC || Correlate SQID+CID and inspect SCT/SC','一定已產生中斷，或資料一定持久 || Interrupt delivery or unconditional persistence'],
 ['Host 更新 CQ Head || Host advances CQ head','Host 已消費完成、歸還 CQ 空間 || Host consumed completions and released CQ space','其他 SQ 或其他 CID 同時完成 || Completion of other SQs or CIDs'],
 ]],
 example=pair('SQ1 的 CID=7 與 SQ2 的 CID=7 可以同時存在。若共用 CQ，看到 CID=7 還不夠，要先看 CQE.SQID。若目標是確認 Write 的持久性，還須核對 WCE、FUA 或 Flush 的完成條件，不能只看成功 Status。 || SQ1/CID7 and SQ2/CID7 can coexist. In a shared CQ, CID7 alone is insufficient: read SQID. Write persistence additionally requires WCE, FUA or Flush completion conditions, not only success status.'),
 refs=['sqe','cqe','order','vwc','nvmatomic']),
'identify':dict(
 title=pair('先選問題，再選 Identify 結構 || Choose the question before the Identify structure'),
 takeaway=pair('不同 CNS 回答不同問題；「已配置」不能直接推論成「這個 controller 現在可存取」。 || Different CNS values answer different questions; allocated does not automatically mean accessible through this controller.'),
 headers=[pair(x) for x in ['想知道什麼 || Question','查詢入口 || Query','回覆如何使用 || How to use the response']],
 rows=[[pair(c) for c in r] for r in [
 ['controller 宣告的能力 || Advertised controller capability','CNS=01h || CNS=01h','讀 OACS、ONCS、MDTS 等，再配合該欄位條件 || Read OACS, ONCS, MDTS and their field conditions'],
 ['目前可存取的 namespaces || Currently active namespaces','CNS=02h || CNS=02h','取得 active list；不是所有已配置容量 || Active list, not all allocated capacity'],
 ['已配置的 namespaces || Allocated namespaces','支援 Namespace Management 時用 CNS=10h || CNS=10h with Namespace Management support','清單可包含未 attach 到此 controller 的 namespace || May include namespaces not attached to this controller'],
 ['單一 NVM namespace 的格式 || Format of one NVM namespace','CNS=00h；需要時加 CNS=05h、CSI=00h || CNS=00h; additionally CNS=05h, CSI=00h when applicable','NSZE／NCAP、FLBAS、LBAF 與 PI 格式共同解讀 || Interpret NSZE/NCAP, FLBAS, LBAF and PI together'],
 ['不依賴命令集的 namespace 屬性 || Command-set-independent namespace properties','CNS=08h || CNS=08h','與 NVM 特定的 LBA 格式結構分開 || Keep separate from the NVM-specific LBA format structure'],
 ]],
 example=pair('假設 Allocated List={1,2}，目前 controller 的 Active List={1}。這只能證明 namespace 2 未出現在此 controller 的 active list；不能直接判定它被刪除。下一步查 attachment 與適用的狀態，並留下 controller 身分及查詢時間。 || If Allocated={1,2} and this controller’s Active={1}, namespace2 is absent from this active list; that does not establish deletion. Check attachment and relevant state, preserving controller identity and query time.'),
 refs=['idcmd','idctrl','idlist','idns','nsmanage']),
'features':dict(
 title=pair('Current 與 Saved：兩條不同的設定路徑 || Current and Saved follow different update paths'),
 takeaway=pair('SV=0 改現在；SV=1 才要求保存。重設恢復仍要配合 scope、saveable 與個別 Feature 例外。 || SV=0 changes the present value; SV=1 requests saving. Restoration additionally depends on scope, saveability and feature exceptions.'),
 headers=[pair(x) for x in ['動作 || Action','Current || Current','Saved／下一次恢復 || Saved / subsequent restoration']],
 rows=[[pair(c) for c in r] for r in [
 ['教學起點：可保存的 Feature || Start with a saveable feature','A || A','Saved=A || Saved=A'],
 ['Set B，SV=0，成功 || Successful Set B, SV=0','B || B','仍是 A || Remains A'],
 ['發生會恢復 Saved 的重設 || A reset restoring Saved','回到 A || Returns to A','A || A'],
 ['Set C，SV=1，成功 || Successful Set C, SV=1','C || C','更新成 C || Updates to C'],
 ['再次發生相同重設 || Same reset again','回到 C || Returns to C','C || C'],
 ]],
 example=pair('這張表刻意假設 Feature 可保存，且該重設適用 Saved 恢復；不能套到所有 Feature。例如 FID84h 不可保存且沒有 Default，但 WPS=1 的基本保護仍跨斷電持續，WPS=2 則在 Power Cycle 解除。 || This table assumes a saveable feature and a reset that restores Saved. It is not universal: FID84h is unsaveable with no Default, yet basic WPS1 survives power cycling and WPS2 clears on a power cycle.'),
 refs=['feature','getfeat','setfeat','nwp']),
}

# Extra course material is exclusive to the independent Chinese HTML.
LESSONS = {
'initialization':[
('先分清誰寫、誰回報','CC.EN 由 Host 寫入，表示要求；CSTS.RDY 由 controller 回報，表示狀態。就像按下電源開關與系統完成開機是兩個時點，驗證時必須留下兩者的時間。單看 EN=1，只能證明 Host 要求啟用，不能證明裝置已準備好。'),
('Independent mode 為什麼需要兩個期限','管理介面可以先準備好，媒體稍後才能服務。CRIMT 約束先就緒的介面，CRWMT 約束媒體；兩個時間都從 EN 0→1 起算。假設介面在 300 ms Ready，而媒體期限為 2 s，媒體的剩餘時間是 1.7 s，不是重新獲得 2 s。實際 deadline 的選取還須配合 CAP.TO 與 CRTO 的比較規則。'),
('重設後的位元仍在，不代表物件仍在','CC.EN 觸發的 Controller Reset 可保留 AQA／ASQ／ACQ，因而省去重新提供基底位址；但 queue 指標已重設，I/O queues 被刪除。Host 若繼續拿舊 CID 對照新 CQE，會把前一輪資料誤認成新完成。建立新的追蹤狀態，是恢復流程的一部分。')],
'queues':[
('把配額、深度與記憶體容量分開算','FID07h 回覆決定能建立多少個 I/O queues；Create Queue.QSIZE 決定其中一個 queue 有幾格；每格大小再決定記憶體需求。假設 NVM I/O SQ 有 64 格，每格 64 bytes，整個 SQ 需要 4096 bytes。這不代表分配到 64 個 SQ，也不代表能同時塞滿 64 個尚未消費的 entry。'),
('CQ 共用帶來什麼取捨','共用 CQ 可以集中處理通知，但 CQ 若被一個繁忙 SQ 的完成佔滿，其他共用者也可能暫停。分開 CQ 則能隔離這種空間壓力。它們是完成緩衝區配置的差別，不是資料是否共享的差別；namespace 是否共享是另一層問題。'),
('刪除的完成點比刪除的提交點重要','送出 Delete SQ 之後，原 SQ 仍可能有已取得的命令需要收尾。Host 不能一送出刪除就立刻釋放原記憶體。等 Delete SQ 成功，才有規範定義的完成邊界；即使有命令沒有獨立 CQE，也可能是規範允許的隱含中止，不能無限等它們。')],
'doorbells':[
('指標是位置，差值才是數量','Doorbell 裡的 2 指位置 2，不是這次送 2 筆。8 格 ring 從 7 前進到 2，要走過 7、0、1，共 3 格。使用一般大小比較看到 2<7 就報錯，會把正常繞回誤判成非法行為。'),
('Phase 不是成功位元','Phase 只告訴 Host 這格是否屬於現在期待的一輪。有效 CQE 裡仍可能是失敗 Status。反過來，舊 CQE 即使留著 Success，Phase 不符就不能再處理一次。先驗有效性、再解碼 SCT／SC，順序不能相反。'),
('為何 Host 處理完還要寫 CQ Head','Host 在自己的程式裡把完成標為已處理，controller 並不知道。CQ Head Doorbell 才是通知 controller 可以重用哪些位置的介面。若漏寫，Host 明明已處理完，controller 仍可能因 CQ Full 而停住；這不是 media latency 變長。')],
'commands':[
('從欄位反推它真正能證明的事','SQHD 是 controller 對 SQ 消費位置的回報；CID 才是此次完成的命令識別。假設同一 CQE 回報 SQHD=4、CID=9，不能據此宣稱 SQ 的前 4 個命令都已完成。裝置可以先取得多筆，再以不同順序完成。'),
('錯誤碼先做單一原因實驗','假設命令同時有非法 NSID 與非法資料指標，兩種錯誤都可能被較早發現。把它當成只測 NSID 的測例，會誤判實作。先建立合法基準，再只改一個參數，並記錄目前狀態、scope 及支援能力，才能讓 Status 的比較有意義。'),
('正常寫入與 fused operation 的順序不同','兩個普通命令放在相鄰 SQE，不會自動變成不可分割的操作。支援的 fused pair 要有對應 FUSE 設定、同一 SQ 的相鄰位置與同一次提交，且仍各自有完成。Host 也不能把整體吞吐量與仲裁權重直接畫等號；不同命令消耗的時間不同。')],
'identify':[
('從裝置、容量到可見性，分三次問','Identify Controller 描述這個 controller；Identify Namespace 描述指定 namespace 的格式與容量；Active List 描述目前能透過這個 controller 使用的 namespace 集合。這三份回覆互補，不能靠 Controller.NN 就認定從 NSID=1 到 NN 全都存在並可存取。'),
('欄位是位元遮罩還是索引，會改變算式','CNS 選資料結構；CSI 選命令集；某些欄位是能力 bitmap，某些是陣列 index。以 LBAF 為例，先從 FLBAS 解出正確索引，再去讀那一筆格式描述，不能把 FLBAS 原始值直接當 bytes 數。對比型別通常比死背十六進位值更有用。'),
('查詢結果也有時間','Create 成功後才查 Allocated List，Attach 成功後才查該 controller 的 Active List。若另一個管理者同時改配置，前後清單可能屬於不同時間。先釐清順序與觀察對象，再判斷是不是韌體沒有更新回覆。')],
'features':[
('先問能不能，再問目前是多少','Get Features.SEL=3 回的是能力，例如是否可修改、是否可保存，不是工作中的值。假設 DW0=5，是 bits2 與0為1；它不能拿來與 Current=5 直接比較。比較前，先確認兩次 Get 的 SEL 相同。'),
('APST 的狀態轉移該怎麼讀','教學假設：目前 PS0，APSTE=1，PS0 entry 的 ITPT=2000 ms、ITPS=3，而且 PS3 是支援的 non-operational state。PS0 持續 idle 超過 2000 ms → 進入 PS3；有工作需要離開時 → 考慮 PS3.EXLAT 才能恢復處理。ITPT 是進入前的 idle 門檻，EXLAT 是退出延遲，兩者不能相加後宣稱每筆命令固定要等這麼久。'),
('持久性與原子性要各做一個判斷','持久性問「已完成的資料在斷電後還在嗎」；原子性問「更新是否可能一部分新、一部分舊」。WCE、FUA、Flush 與原子單位、邊界處理的是不同保證。即使資料持久，超出原子範圍的多 block 操作仍不能憑空獲得整筆不可分割的保證。')],
}
