"""Independent course introductions, interpretation tables and worked lessons."""
from scripts.nvme_qa_model import pair

def extend(volumes,intros,aids,lessons):
    def chapter(slug,a,b,title,intro,heading,takeaway,headers,rows,example,refs,course):
        zh,en=pair(title);volumes.append((slug,a,b,zh,en));intros[slug]=pair(intro)
        aids[slug]=dict(title=pair(heading),takeaway=pair(takeaway),headers=[pair(s) for s in headers],rows=[[pair(s) for s in row] for row in rows],example=pair(example),refs=refs)
        lessons[slug]=course
    chapter('logs',69,81,'Get Log Page 與資料一致性 || Get Log Page and data consistency',
      'Log 回答狀態、歷史或支援能力，但不是每份 Log 都保存歷史，也不是讀取後一定不變。本冊先選對資料與範圍，再處理長度、分段、事件確認與一致性。 || Logs expose state, history or capability, with different lifetimes and read effects. Choose the view and scope before length, pagination, acknowledgment and consistency.',
      '同樣是讀 Log，四個問題要分開 || Four separate questions when reading logs',
      '先決定要證明什麼，再選 Log；讀成功只代表查詢成功，不代表被查的管理操作已完成。 || Choose the evidence first; a successful read does not complete the operation being observed.',
      ['需要的證據 || Evidence needed','查詢對象 || View','判讀限制 || Limitation'],[
       ['支援哪些 Log || Supported logs','LID00h || LID00h','支援不等於目前有事件 || Support does not imply a current event'],
       ['目前健康 || Current health','SMART LID02h || SMART LID02h','警告可恢復；累計值則有生命週期 || Current warnings and lifetime counters differ'],
       ['這次命令的錯誤細節 || Command error details','Error LID01h || Error LID01h','需對回命令，且舊 entries 可能消失 || Correlate identity; old entries can disappear'],
       ['持續事件歷史 || Persistent event history','PEL LID0Dh || PEL LID0Dh','容量與事件支援限制仍存在 || Capacity and supported-event limits remain']],
      '假設一次讀4096 bytes，NUMD=1023。下一段若採 byte offset，LPO=4096；若 Log 使用 index offset，則要依該 Log 的索引規則前進，不能照抄4096。 || A 4096-byte read encodes NUMD1023. The next byte offset is 4096, but index-offset logs require their own entry progression.',
      ['getlog','smart','error','pelcontext'],[
       ('先知道 Log 是快照還是歷史','想知道目前溫度時，SMART 的現在值比一筆很早的事件有用；想知道剛才是否發生短暫異常時，現在值又不一定足夠。先寫出要回答的問題，再選目前狀態、累計計數或歷史事件。這樣即使讀到的資料不同，也能分辨是觀察時間不同，還是真的互相矛盾。'),
       ('分段的難處在於內容也可能改變','一份 Log 分兩次讀取，不保證兩段來自同一時點。第一段讀完後，如果資料長度或 entries 順序改變，第二段可能接到不同版本。對有 generation 或 context 的 Log，先建立一致的觀察範圍，再分段讀取；沒有這類保證時，必須說明資料可能在讀取期間變動，不能自行宣稱原子快照。'),
       ('RAE 是確認事件，不是取消資料讀取','RAE=1 仍然會讀取資料，只是保留相應事件；RAE=0 的成功讀取可能確認事件。假設兩個程式先後讀同一 Log，第一個已確認，第二個看到的通知狀態就可能不同。因此做事件驗證時，要同時保存讀取順序、RAE 與結果，不能只比較最後一份 buffer。')])
    chapter('asynchronous-events',82,92,'Asynchronous Event Request || Asynchronous Event Request',
      'AER 讓 Host 先留下等待通知的請求，controller 有事件時才完成它。先理解請求、事件、Log 與確認的關係，再處理多事件、遮蔽與重新掛入。 || AER preposts requests that complete on events. Connect requests, events, logs and acknowledgment before concurrency and rearming.',
      '通知完成後，工作還沒結束 || Notification completion is not the end',
      'AER 回報事件線索；詳細內容與目前狀態仍要讀相應 Log。 || An AER supplies event identity; logs provide detail and current state.',
      ['階段 || Stage','Host 或 Controller 動作 || Action','需要保存的資訊 || Evidence'],[
       ['事前 || Before event','Host 提交 AER || Host submits AER','請求 CID 與上限 AERL+1 || Request identity and AERL+1 limit'],
       ['事件發生 || Event occurs','Controller 完成適用請求 || Controller completes a request','Type、Information、LID || Type, information, LID'],
       ['查證 || Inspect','Host 讀對應 Log || Host reads matching log','selector、RAE 與原始內容 || Selectors, RAE and raw data'],
       ['繼續接收 || Continue','Host 重新掛 AER || Host posts another AER','新的 outstanding 請求 || New outstanding request']],
      '假設 AERL=3，允許上限是4筆。完成一筆後，Host 可補回一筆；不能把已完成但未補掛的請求仍算成可接收下一事件的空間。 || AERL3 allows four requests. Replace a completed request; a completed unrearmed request cannot receive another event.',
      ['aerfull','getlog','aec'],[
       ('等待不是故障','一般命令長期不完成可能需要調查，但 AER 的目的就是等待事件。沒有事件時保持 outstanding 可以完全正常。驗證前先確認這是 AER，而不是誤用一般 I/O timeout。AER 也會占用自己的命令追蹤資料，所以 Host 必須正確處理完成與重新提交。'),
       ('通知與確認各自解決一個問題','通知讓 Host 知道有事需要查看；確認則告訴 controller 該事件已被處理。若只補掛 AER 卻沒按事件規則確認，同類事件可能仍受遮蔽；若只讀 Log 卻沒補掛，下一事件可能暫時沒有請求可回報。兩個步驟都需要，但具體清除方式仍要依事件類型判斷。'),
       ('一次狀態改變不必對應一筆新通知','多次同類事件可能合併，某些警告在讀取前也可能恢復。不要用取樣次數要求同樣數量的 AER。應先固定事件類型、enable、尚未確認狀態與掛入請求數，再檢查規範要求的通知行為；這比單純比較事件與 CQE 的總數可靠。')])
    chapter('errors',93,106,'錯誤 Status 與 Error Information || Error status and Error Information',
      '本冊從一筆失敗命令出發，先判斷錯誤類型，再找補充記錄與恢復依據。重點是把原命令、完成狀態及歷史資料對回同一件事。 || Start with one failed command, classify it and correlate completion with supplemental records and recovery evidence.',
      '把三種證據分開讀 || Three different kinds of evidence',
      '先確認命令身分，再比較錯誤；名稱相似的紀錄不一定描述相同事件。 || Establish command identity before comparing records.',
      ['證據 || Evidence','能回答什麼 || What it establishes','不能直接推論什麼 || What it does not prove'],[
       ['CQE || CQE','該命令的完成結果 || Command completion result','所有媒體效果已撤銷 || All media effects were undone'],
       ['Error Information || Error Information','錯誤補充欄位及參數位置 || Additional failure detail','每個失敗都必有一筆 || One entry for every failed command'],
       ['PEL || PEL','支援的持續事件 || Supported persistent events','完整命令執行歷史 || A complete command trace']],
      '一筆命令同時有非法 NSID 與壞的 PRP，可能先檢出任一條件。若要驗證 Invalid Namespace，就應先修正指標，只保留一個錯誤原因。 || A request with both bad NSID and PRP may expose either fault first. Isolate NSID to test its required status.',
      ['status','error','pelcontext'],[
       ('Status 是分類，不是完整根因','Invalid Field 告訴你要求中有不合法欄位，但不一定直接指出是哪一個。保存原始 SQE 後，再使用 Error Information 的 Parameter Error Location 等欄位縮小範圍。若該位置無效或沒有額外資訊，就應承認還無法定位，不要只靠 Status 名稱猜一個欄位。'),
       ('重試前要先修正前提','DNR=0 表示重試可能成功，不保證立刻原樣重送一定有效。如果原因是 namespace 還沒 ready，就需等狀態改變；如果是參數不合法，則需先修正參數。先問「哪個條件已經不同」，再決定重試，才能避免無意義的重複命令。'),
       ('記錄容量會改變看得到的歷史','錯誤紀錄的有效 entries 與累計 Error Count 不同。舊 entry 可能因容量或 reset 消失，但計數仍可保留。看到計數大於目前可讀筆數是合理情況；查不到原 entry 只能說證據不完整，不能反推那次錯誤沒發生。')])
    chapter('recovery',107,117,'Abort、Timeout 與錯誤恢復 || Abort, timeout and recovery',
      'Timeout 是 Host 的觀察，未必能說明命令停在哪裡。本冊沿提交、取得、執行、完成與處理的路徑找證據，再決定 Abort 或較大範圍 reset。 || A timeout is an observation, not a location. Follow submission through consumption before choosing abort or reset.',
      '先確認命令走到哪一步 || Find the command stage first',
      '未看到完成，不代表命令沒有執行，也不代表媒體沒有變動。 || Missing completion proves neither nonexecution nor unchanged media.',
      ['可觀察階段 || Stage','主要證據 || Evidence','下一個疑點 || Next question'],[
       ['已提交 || Submitted','SQE、Tail Doorbell || SQE and tail','Controller 是否取得 || Was it consumed?'],
       ['已取得 || Consumed','適用的 SQHD 與追蹤資料 || SQHD and tracking','是否正在長操作 || Is it a long operation?'],
       ['已完成 || Completed','CQE 與 Phase || CQE and phase','Host 是否漏處理 || Did the host miss it?'],
       ['恢復中 || Recovering','Abort CQE／reset 狀態 || Abort/reset state','原操作結果是否仍不確定 || Are prior effects uncertain?']],
      'Abort 指向 SQ5/CID9，Abort 本身是另一筆 Admin command。兩者各回一筆 CQE 可以正常；只有同一目標命令真的完成兩次，才是重複完成問題。 || Abort targeting SQ5/CID9 has its own Admin completion. One CQE for each is normal; duplicate target completion is different.',
      ['abort','commrecovery','reset','cqe'],[
       ('先分清三種時間','Ready Timeout 用於 controller 狀態切換，Host 的 Command Timeout 用於軟體等待，而長時間管理操作另有其進度與限制。把這三者套同一秒數，可能將正常 Sanitize 或 AER 判成故障。每次量測都要寫下起點、等待的條件及規範是否真的給了上限。'),
       ('Abort 不是撤銷交易','命令在被中止前可能已產生部分效果。即使 Abort 有立即效果，也不能保證把已寫資料回復成舊內容。Host 應先保留目標命令與結果的不確定性，再決定是否能安全重試；對有副作用的管理操作，重新查目前狀態尤其重要。'),
       ('恢復範圍要跟問題相稱','一筆命令卡住不一定需要整個 subsystem reset，但通道已無法使用時，繼續送 Abort 也可能沒有幫助。先判斷 CQ 是否滿、命令是否已完成但 Host 漏看，以及 Admin 通道是否可用。選擇較大範圍 reset 後，必須一起重建該範圍內的 queues 與命令追蹤，不能只重送原命令。')])
    chapter('format-sanitize',118,135,'Format 與 Sanitize || Format and sanitize',
      'Format 改變 namespace 格式；Sanitize 處理資料清除。兩者的範圍、完成點與 reset 行為不同，本冊以一次操作的前、中、後狀態逐步區分。 || Format changes namespace format; sanitize removes data. Compare scope, completion and reset behavior across the operation lifecycle.',
      '三條操作路徑不能互換 || Three distinct operation paths',
      '支援 subsystem Overwrite，不代表支援 namespace Overwrite。 || Subsystem overwrite support does not enable namespace overwrite.',
      ['操作 || Operation','主要選擇 || Main selectors','完成證據 || Completion evidence'],[
       ['Format NVM || Format NVM','LBAF、metadata、PI、SES || Format, metadata, PI and SES','Format CQE 與新格式 || Format CQE and resulting format'],
       ['Subsystem Sanitize || Subsystem sanitize','SANACT、範圍與選項 || Action and options','啟動 CQE 後還看 LID81h || Initiation CQE followed by status'],
       ['Namespace Sanitize || Namespace sanitize','NSID、Crypto Erase || NSID and crypto erase','查目標 namespace 的狀態 || Target namespace status']],
      'SANICAP.OWS=1 只能證明相應的 subsystem Overwrite 能力。若要求清除單一 namespace，Base2.4 的 Sanitize Namespace 只允許 Crypto Erase，不能將 SANACT=3 照搬過去。 || OWS1 advertises subsystem overwrite. Base2.4 namespace sanitize permits crypto erase, not copied SANACT3 overwrite.',
      ['format','nvmformat','sanitizecmd','sanitizelog','sanitizestate'],[
       ('先問要改格式，還是要清資料','將4KiB格式改成512-byte格式，是 Format 的問題；想讓原資料無法恢復，則要明確選擇清除方法及影響範圍。Format 的 Secure Erase 選項與 Sanitize 也不能只因都提到清除就視為等價。先確認需求，才能查對支援欄位與命令。'),
       ('Sanitize 有兩個完成點','命令啟動成功後，controller 可以在背景繼續清除。這時 Log 顯示進行中並不矛盾。Host 需要繼續觀察 SOS、SPROG 與可能的 verification state；最終成功、失敗或進入特定 failure mode，才是媒體操作的結果。不要只保留最初 Success CQE。'),
       ('Reset 不會把進行中的操作一律取消','Sanitize 有跨 reset 與失電恢復後持續的規則；Format 的中斷結果則需重新探索。恢復後先查原操作範圍、目前格式或 Sanitize Status，再決定下一步。未收到 CQE 不代表操作完全沒做，重送前必須先確定裝置目前狀態。')])
    chapter('firmware-boot',136,148,'Firmware Update 與 Boot Partition || Firmware update and boot partitions',
      '先分清下載、提交與啟用，再把 Boot Partition 的讀取和切換放在旁邊比較。資料已傳入 controller，不代表新韌體或新開機映像已開始使用。 || Separate download, commit and activation, then compare boot-image access and selection.',
      '從映像資料到真正啟用 || From image bytes to activation',
      'Slot、pending activation 與目前 running revision 各描述一個階段。 || Slot contents, pending activation and running revision describe different stages.',
      ['階段 || Stage','查哪些欄位 || Evidence','此時能說什麼 || Conclusion'],[
       ['Download || Download','OFST、NUMD、完整映像 || Offset, length, coverage','資料已傳送，不等於啟用 || Transferred, not activated'],
       ['Commit || Commit','FS、CA、CQE || Slot, action, status','依 Action 存入或安排啟用 || Stored or activation scheduled'],
       ['Activation || Activation','所需 reset、FR、CAFS || Required reset, revision, active slot','確認目前實際版本 || Establish running version'],
       ['Boot Partition || Boot partition','ABPID、BRS、FID85h || Active partition, read state, protection','判斷映像讀取及保護 || Interpret boot access/protection']],
      'CA=2 是安排既有 slot 在指定啟用時機生效；若還沒做該步驟，Identify.FR 不必提前改變。Boot 的 CA=7 則是選 Active Partition，不能直接等同一般 Firmware Activation。 || Pending slot activation need not change FR early; boot CA7 selects a partition and is not ordinary firmware activation.',
      ['firmware','fwlog','boot','bootreg','bootprotect'],[
       ('分段傳送先弄清楚單位與順序','Firmware Download 的 Offset 與 Length 以 Dword 表示，Length 還有 zero-based 編碼。一般 firmware 段落可以按允許方式安排，但 Boot Partition image 要遵守其順序要求。兩個流程即使用到相同命令，也不能共用所有檢查條件。'),
       ('成功 Commit 要連同 Action 解讀','同樣是 Commit 成功，可能只是存入映像，也可能安排下次 reset 啟用。若回覆要求特定 reset，就要做那一種；CC.EN 切換不能取代所有 Conventional Reset 要求。完成後以 active slot 與 running revision 核對，而不是只看 Download 有沒有成功。'),
       ('Boot 讀取有自己的狀態回報','Register 路徑使用 BPMBL 提供 buffer、BPRSEL 指定讀取範圍、BPINFO.BRS 表示進行與結果。這不是一筆 queue 命令，所以不會出現可供解碼的 NVMe CQE。讀取中也不能任意重設；先等狀態結束，才能把 buffer 當成可用映像。')])
    chapter('self-test',149,156,'Device Self-test || Device self-test',
      'Self-test 將裝置內部診斷結果回報給 Host。先確認能啟動哪種測試，再分清進度、最終結果與失敗欄位有效性。 || Establish supported tests, then distinguish progress, final results and valid failure details.',
      '啟動、執行、結果是三種資訊 || Start, progress and result are distinct',
      '啟動 CQE 成功，不表示測試通過。 || Successful initiation does not mean a passed test.',
      ['觀察 || Observation','欄位／介面 || Interface','用途 || Use'],[
       ['可否執行 || Capability','OACS、DSTO || OACS, DSTO','確認支援與並行條件 || Support and concurrency'],
       ['目前執行 || Progress','Current Operation、Completion Percentage || Current operation and percentage','了解還在做什麼 || Track current work'],
       ['本次結果 || Result','最新 Result 的 DSTC、DSTR || Newest test/result codes','辨識通過、失敗或中止 || Pass, failure or abort'],
       ['失敗細節 || Failure detail','VDINFO、SEGN、FLBA || Validity, segment and LBA','只有有效欄位才可推論 || Use only valid fields']],
      'Short 在 CLR 下需要中止；Extended 有跨 CLR 持續與失電恢復的規則。不能只看測試名稱都有 Self-test，就要求相同 reset 結果。 || Short and extended tests have different reset/power continuity rules.',
      ['selftest','dstlog','nvmselftest'],[
       ('測試範圍先於結果解釋','NSID=0、指定 namespace 與廣播選擇有不同範圍。先保存啟動參數，才知道失敗結果對應哪個對象。若測試只涵蓋某個 namespace，不能將成功結果擴大成所有 namespace 都已測過。'),
       ('有效位元是資料可否使用的前提','Result 結構中有很多欄位，但不代表每次都有效。FLBA 只有有效條件成立時，才是可用的失敗位置；它也不是全部壞 LBA 清單。先讀 DSTR 與 VDINFO，再看細節，才不會將保留或無效 bytes 當成真實故障位置。'),
       ('比較新舊結果比只看目前 idle 更可靠','測試開始前先保存最新結果；結束後再比較最前面的新紀錄。Current Operation 回到 idle 只表示現在沒有測試進行，可能是通過、失敗或中止。再搭配時間、測試種類與結果代碼，才能說清楚這次發生了什麼。')])
    chapter('namespace-management',157,173,'Namespace Management、Attachment 與保護 || Namespace management, attachment and protection',
      '建立 namespace、讓 controller 能存取它，以及限制寫入，是三組獨立狀態。本冊用同一物件從建立到刪除的流程，把三者接起來。 || Creation, attachment and write protection are separate states connected through a namespace lifecycle.',
      '存在、可見、可寫分別確認 || Check existence, access and writability separately',
      'Create 成功不會自動完成 Attachment。 || Creation does not automatically attach a namespace.',
      ['問題 || Question','主要證據 || Evidence','下一步 || Next step'],[
       ['是否存在 || Does it exist?','Allocated List、Create CQE.NSID || Allocated inventory and returned NSID','確認格式與容量 || Check format/capacity'],
       ['此路徑能否存取 || Is it attached here?','Active List、Controller List || Active and attachment lists','確認 Ready 與路徑狀態 || Check readiness/path'],
       ['是否能改資料 || Is writing allowed?','NWPC、WPC、FID84h.WPS || Capability, control and state','依狀態檢查命令限制 || Apply command restrictions']],
      'Allocated={1,2}、ControllerA.Active={1} 只表示2尚未在A的 active清單。它可能仍存在，甚至已附加B；不能直接判定 namespace2被刪除。 || Namespace2 absent from A’s active list may still exist and be attached to B.',
      ['nsattach','nvmcreate','idlist','nwp'],[
       ('容量要先換成所選格式的 blocks','NSZE 與 NCAP 不是 bytes。若每個 logical block 有4096 bytes，NSZE=1000 對應4000KiB的邏輯位址空間。NCAP 描述可配置容量，而且不得大於 NSZE。先選 LBA Format，再計算欄位，不能把4KiB格式的數字原封套到512-byte格式。'),
       ('Attach 改路徑，不複製資料','Shared namespace 經兩台 controller 存取時，兩條路徑通往同一份資料。Detach 其中一台，只移除那台的附加關係；另一台仍附加就可能繼續使用。驗證時要記下命令從哪台送入，再比較該台 Active List，不能只看 subsystem 中任一份清單。'),
       ('保護能力、進入許可、目前狀態要分開','NWPC 回答支援哪些保護，WPC 控制是否允許進入特定狀態，WPS 才是目前保護。清除控制位不等於解除已進入的保護。永久保護與直到Power Cycle的保護又有不同退出條件，所以不能只看到不可保存就要求 reset 後回到無保護。')])
    chapter('reset-shutdown',174,187,'Reset 與 Shutdown || Reset and shutdown',
      'Reset 結束操作環境，Shutdown 準備安全停止；兩者的目的和完成證據不同。先看影響範圍，再分辨哪些狀態需要重建，哪些操作仍持續。 || Reset rebuilds an operating context while shutdown prepares stopping; compare scope, completion and retained operations.',
      '停止的要求與停止的完成 || Requested stop versus completed stop',
      'Host 寫入要求不等於 controller 已完成；等待條件必須看回報狀態。 || A host request is not device completion; inspect reported state.',
      ['動作 || Action','要求 || Request','完成後的主要處理 || Follow-up'],[
       ['Controller Reset || Controller reset','CC.EN→0 || CC.EN→0','等RDY=0，重建queues || Wait RDY0 and rebuild queues'],
       ['Subsystem Reset || Subsystem reset','適用的reset介面 || Applicable reset interface','確認全部受影響controller || Recover affected controllers'],
       ['Normal Shutdown || Normal shutdown','CC.SHN=01b || CC.SHN=01b','等SHST=10b，核對斷電範圍 || Wait SHST10b and power-off scope'],
       ['Abrupt Shutdown || Abrupt shutdown','CC.SHN=10b || CC.SHN=10b','仍觀察完成狀態 || Still observe completion']],
      'Normal要求送出後若SHST還未完成就掉電，仍可能增加UPL；Abrupt已完成後才掉電則不必然增加。關鍵是掉電當時狀態。 || Incomplete normal shutdown can qualify for UPL; completed abrupt shutdown need not. State at power loss matters.',
      ['reset','shutdownfull','pciereset','smart'],[
       ('重設保留位址，不表示保留queue','某些 reset 會保留 AQA、ASQ、ACQ，但 Admin 指標已重設，I/O queues 也已刪除。舊記憶體中即使還留著 CQE，Host 仍必須初始化 Phase 與追蹤資料。位址是配置資訊，queue 的有效使用期間則已經結束。'),
       ('Shutdown 先準備，後等待','正常流程要先停止送入新工作並處理相關依賴，再要求 Shutdown。接著觀察 SHST，不是睡固定時間就假定完成。實際可移除電源的範圍還要看 CAP.CPS 與其他 controllers；只看到一台完成，不保證整個多 controller 裝置都已準備好。'),
       ('未完成操作不能一律重送','Reset 可能讓 Host 失去 CQE，但媒體操作未必回復到開始前。恢復後應先查管理操作狀態與持續性紀錄，再判斷能否重試。例如 Sanitize 可能持續，namespace 也可能已建立；直接重送可能造成另一個動作或不同錯誤。')])
    chapter('health',188,204,'Power、Thermal 與 Health Monitoring || Power, thermal and health monitoring',
      '功耗狀態、溫度控制與健康計數互相關聯，但各自回答不同問題。本冊先建立狀態與時間概念，再學習如何讀取警告與工作量。 || Power states, thermal control and health counters are related but answer different questions. Learn state and timing before warnings and workload.',
      '控制值、目前值、累計值分開看 || Separate controls, current state and lifetime counts',
      '設定門檻不等於發生警告；警告恢復也不會把累計工作量清除。 || A configured threshold is not a warning, and warning recovery does not clear lifetime workload.',
      ['種類 || Kind','例子 || Examples','比較方式 || Comparison'],[
       ['控制 || Control','APST.ITPT、HCTM.TMT1／2 || APST/HCTM settings','先確認單位與支援 || Check units/support'],
       ['目前狀態 || Current state','溫度、Critical Warning || Temperature and warning','與同時點條件比對 || Compare contemporaneous conditions'],
       ['累計 || Cumulative','Data Units、Busy Time、UPL || Data, busy time and power loss','前後差值與取整 || Differences and quantization']],
      'APST閒置2000ms與PSD.EXLAT=100µs發生在不同階段：前者是開始進入低功耗前的等待，後者是離開時延遲。不能把它們當成每筆命令固定延遲。 || A 2000 ms idle threshold and 100 µs exit latency describe different phases, not a fixed per-command delay.',
      ['powerdetail','psd','power','thermal','smart'],[
       ('用狀態轉移理解省電','先找目前工作狀態，再看 APST 會在閒置多久後轉去哪個非工作狀態。需要處理I/O時，controller 要回到工作狀態，這時才會受到退出與進入延遲影響。只背 Power State 編號無法推論延遲，必須一起看 NOPS、ENLAT、EXLAT 及實際轉移路徑。'),
       ('溫度門檻與降速不是同一個設定','SMART 溫度警告描述健康條件；HCTM 讓 Host 提供熱管理門檻，controller 在指定條件下調整行為。兩者可能同時發生，也可能只有其中之一。比較時保留當時溫度、TMT1／TMT2與警告門檻，避免把效能降低一律解釋為SMART錯誤。'),
       ('相同名稱的計數也要核對單位','SMART Data Units以1000×512bytes為單位並向上取整，而Endurance Group的相關資料量欄位以10^9bytes計。短測試中，小量新增資料可能還看不到預期差值，或受取整邊界影響。先換算單位，再說明取樣區間與量化誤差，才有可比較的結果。')])
    chapter('persistent-events',205,216,'Persistent Event Log 與 Timestamp || Persistent Event Log and Timestamp',
      'PEL 保存重要事件，Timestamp 協助解釋事件時間。本冊先教一致地取回完整Log，再說明可變長度、事件類型與時鐘變更。 || Retrieve a consistent PEL before interpreting variable lengths, event types and changing time bases.',
      '讀取的context與事件的持久性分開 || Reporting context differs from persistent history',
      '事件仍保留，不代表舊context在reset後仍可沿用。 || Persistent events do not guarantee a reusable context after reset.',
      ['讀取步驟 || Retrieval step','需要欄位 || Fields','注意事項 || Constraint'],[
       ['建立觀察範圍 || Establish view','ACT、RCE || Action and context status','ACT3的RCE=0可表示剛建立成功 || ACT3 RCE0 can mean newly established'],
       ['走訪Log || Traverse','LHL、TLL、TNEV || Header length, total length, event count','不能把每筆事件固定為同樣大小 || Events have variable lengths'],
       ['解析事件 || Parse event','EHL、EL、VSIL || Header, event and vendor lengths','整筆=EHL+3+EL || Total=EHL+3+EL'],
       ['解釋時間 || Interpret time','Origin、SYNC、Timestamp Change || Clock attributes and change event','不能一律要求timestamp單調增加 || Timestamps need not be monotonic']],
      'EHL=21、EL=20、VSIL=4時，整筆事件44bytes，其中Event Data為16bytes。VSIL已包含在EL，若再加一次就會走錯下一筆。 || With EHL21/EL20/VSIL4, total length is 44 bytes and event data16 bytes; adding VSIL again misaligns the next event.',
      ['pelcontext','nvmpel','timestamp'],[
       ('Context固定的是這次讀取視角','controller 可以在背景繼續記錄新事件，但既有 reporting context 不會因此任意插入新內容。這讓 Host 能分段取回一份一致的報告。讀完要依流程釋放；下次要看新事件，再建立新 context，而不是假設同一份快照永遠更新。'),
       ('長度從欄位定義一步一步算','先用LHL取得Log Header結尾，再以EHL+3找出每筆Event Header長度，最後加EL前進。EL裡已包含vendor-specific部分，所以標準Event Data要扣掉VSIL。每次前進都檢查TLL界限，不能因Get Log要求傳輸對齊，就替每筆事件自行加padding。'),
       ('事件時間需要共同基準','Host重新設定Timestamp後，後續事件時間可能突然變大或變小。Timestamp Change提供變更前後資訊，Origin與SYNC則說明這個值如何建立與累計。先解釋時鐘基準，再比較事件先後，才能避免把合法校時誤判為PEL排序錯誤。')])
    chapter('keep-alive',217,222,'Keep Alive || Keep Alive',
      'Keep Alive用來偵測Host是否仍維持連線活動，在PCIe上屬選配。本冊分開命令模式與流量模式，說明何時開始計時及到期後的結果。 || Optional PCIe Keep Alive detects host liveness through command-based or traffic-based timing.',
      '兩種模式，兩種重新計時依據 || Two modes with different renewal evidence',
      '一筆命令長期outstanding，不等於每個流量區間都有新活動。 || One long-outstanding command does not establish activity in every interval.',
      ['條件 || Condition','查詢或動作 || Evidence/action','判讀 || Interpretation'],[
       ['支援與粒度 || Support/granularity','KAS、TBKAS || KAS, TBKAS','KAS單位100 ms；模式另確認 || KAS uses 100 ms units; mode is separate'],
       ['逾時設定 || Timeout','FID0Fh.KATO || FID0Fh.KATO','要求值可能向上調整 || Value may be rounded up'],
       ['命令模式 || Command mode','成功Keep Alive／KATO Set || Successful Keep Alive/KATO Set','依成功操作重新計時 || Restart on qualifying success'],
       ['流量模式 || Traffic mode','區間內取得命令 || Command fetches in interval','不能只看仍有outstanding || Outstanding alone is insufficient']],
      'KAS=2表示200ms粒度；KATO要求250ms時需向上配合粒度。Host應讀回實際值，用它安排後續活動，而不是堅持回值必須等於250。 || KAS2 means 200 ms granularity; a 250 ms request is rounded upward. Schedule using actual readback.',
      ['keepalive','idctrl','feature'],[
       ('支援不代表已經啟動','先看KAS判斷能力，再看KATO是否非零，以及controller是否處於EN=1、RDY=1且沒有shutdown的適用狀態。少了這些前提，就不能只因過了某個時間要求出現Keep Alive Timeout。這是能力、設定與運作狀態共同決定的計時器。'),
       ('流量模式觀察的是每個區間','假設一筆長命令在第一個區間被取得，之後一直執行。這只能證明第一個區間有活動，不能替所有後續區間提供新活動證據。Host需依模式的活動觀察與Keep Alive策略維持需求，不能把一筆尚未完成的命令當作永久保活。'),
       ('到期是controller狀態變化','PCIe Keep Alive到期會有指定錯誤記錄、停止處理及CFS等要求。這不是一般命令多等一下即可的延遲；Host應保存時序與狀態，再按恢復流程重建通道。也不要套用本題範圍以外的傳輸資源清理規則。')])
    chapter('memory',223,236,'HMB、CMB 與 PMR || HMB, CMB and PMR',
      '先看記憶體位於哪裡、由誰提供與何時可回收，再看持久性。HMB、CMB、PMR不能因都含Memory就套同一組reset規則。 || Compare location, ownership, lifetime and persistence rather than treating all memory facilities alike.',
      '位置、使用者與持久性 || Location, ownership and persistence',
      '位址設定保留，不代表原內容保留；CQE成功也不必然證明PMR資料已持久化。 || Retained addressing is not retained content; CQE success alone does not establish PMR persistence.',
      ['機制 || Facility','記憶體與用途 || Location/use','結束或確認條件 || Lifetime/evidence'],[
       ['HMB || HMB','Host提供controller專用buffer || Host-provided controller buffer','成功停用後才能回收 || Reclaim after successful disable'],
       ['CMB || CMB','Controller提供可選用途記憶體 || Controller memory with advertised uses','依reset／CMSE規則重建內容 || Reinitialize under reset/CMSE rules'],
       ['PMR || PMR','PCIe function提供持久記憶體 || Function-provided persistent region','檢查Ready、健康及PMRWBM || Check readiness, health and write barriers']],
      'HMB停用成功前，Host不能重用其buffer。CMB在某些reset後即使CBA還在，CQ內容仍須重新初始化；PMR則另有持久性與健康要求。 || HMB cannot be reused before disable; retained CMB addressing can still require content reinitialization; PMR has distinct persistence/health rules.',
      ['hmb','cmb','cmbreg','pmr','pmrreg'],[
       ('HMB是借出去的Host記憶體','Host仍擁有實體記憶體，但在HMB啟用期間，controller具有規範允許的專用使用權。Host不能因某筆普通命令完成就回收它，也不能改寫descriptor list。先成功停用HMB，確認存取生命週期結束，再釋放或重用，才能避免controller寫到新用途資料。'),
       ('CMB要先查用途再放東西','支援CMB不代表能放所有queue、資料或清單。SQS、CQS、LISTS、RDS、WDS各管不同用途，其他限制還管是否能混用Host與CMB範圍。先把某筆命令需要的queue、data、metadata、list逐一標位置，再檢查每種用途，不能只確認地址落在CMB就算合法。'),
       ('PMR有可存取與可信資料兩層','EN設定後仍需等NRDY清除，再看ERR及HSTS。先前寫入是否已持久化，還要按PMRWBM使用支援的確認方法。即使讀取可以完成，Restore Error或Read Only也會改變能做的推論；不能只憑讀回一個值就宣稱整份資料歷經斷電仍可靠。')])
    chapter('security',237,245,'Security 與 Lockdown || Security and Lockdown',
      'Security Send／Receive承載協定資料；Lockdown限制命令或Feature。先分清資料交換結果與禁止範圍，再討論reset及斷電持續性。 || Security commands transport protocol data; Lockdown prohibits selected operations. Separate protocol results, prohibition scope and persistence.',
      '傳輸成功、協定成功與允許執行 || Transport, protocol and permission are distinct',
      'NVMe Success不自動等於認證成功；被鎖定Feature的Get也不自動被禁止。 || NVMe success is not authentication success, and prohibiting Set does not automatically prohibit Get.',
      ['問題 || Question','需要的資訊 || Evidence','結果所在位置 || Where the answer resides'],[
       ['資料有沒有交換 || Was data exchanged?','Security CQE || Security CQE','NVMe命令結果 || NVMe completion'],
       ['安全操作是否成功 || Did authentication succeed?','SECP、SPSP、payload || Protocol selectors/payload','所選協定定義 || Selected protocol'],
       ['命令是否被禁止 || Is it prohibited?','IFC、CSEL、SCP、清單 || Interface/scope/list','Lockdown及目標CQE || Prohibition and target completion'],
       ['斷電後是否保留 || Does it survive power loss?','CSEL與LDPE || CSEL and LDPE','範圍專屬規則 || Scope-specific persistence']],
      'CSEL=0、LDPE=1的禁止可跨Power Cycle保留；CSEL=1／2不能只因LDPE=1就取得同樣持續性。 || CSEL0 with LDPE1 persists, while CSEL1/2 do not gain that persistence from LDPE.',
      ['security','lockdown','locklog','lockpersist'],[
       ('先指定安全協定，才談鎖定狀態','NVMe定義如何送收安全資料，但不替所有外部協定定義相同的session、金鑰與解鎖規則。若問題沒有指定協定，就不能可靠回答Power Cycle後一定解鎖或一定保留認證。教材會明確區分NVMe能證明的傳輸結果，以及仍需所選協定才能解讀的狀態。'),
       ('Lockdown的目標是多個selector交集','想禁止某操作，必須同時選對介面、controller範圍、opcode或FID與UUID。若只禁止Admin介面，另一個未被涵蓋的介面可能仍允許；若鎖的是Set Features的FID，Get仍可能正常。驗證前先寫出完整選擇條件，才知道哪個成功案例是真正漏鎖。'),
       ('彙整清單要看全部與部分的差別','一般全體視角與增強FFFFh視角的集合意義不同。增強清單裡ACNTL=0表示不是所有controller都受該項限制，並不表示完全沒有禁止。先確認查詢格式，再看是哪幾台受影響，避免將部分限制看成空清單。')])
    chapter('virtualization',246,255,'Multi-Controller 與 Virtualization || Multi-controller and virtualization',
      '多路徑、shared namespace與虛擬化是不同關係。本冊先畫controller拓樸，再加入attachment、ANA及可分配queue／interrupt資源。 || Separate multipath, shared storage and virtualization before combining topology, attachment, ANA and resources.',
      '同一張拓樸上有三種狀態 || Three state dimensions on one topology',
      'Online、Enabled與namespace可存取不是同一件事。 || Online, enabled and namespace-accessible are different.',
      ['狀態 || State','查詢 || Discovery','用途 || Interpretation'],[
       ['管理角色 || Role','Primary Capabilities、Secondary List || Primary/secondary structures','誰可管理誰的資源 || Resource-management authority'],
       ['可啟用性 || Online status','Secondary state、VQ／VI || State and resource counts','是否具備Online前提 || Online prerequisites'],
       ['命令介面 || Interface','CC、CSTS || CC/CSTS','controller是否已啟用 || Enabled/readiness'],
       ['namespace路徑 || Namespace path','Active List、ANA || Active inventory and ANA','目前可否經此路徑存取 || Current path availability']],
      'Secondary Online之後仍需Host初始化並Enable；把Online直接當RDY=1，會跳過必要步驟。 || Online does not set RDY1; host initialization and enable remain necessary.',
      ['multipath','virtual','virtualcmd','virtualid','ana','analog'],[
       ('Shared資料不是每台各有一份','兩台controller附加同一shared namespace，是兩個入口通往同一份資料。某台reset不必然讓另一台失去存取，但Host仍需協調同時寫入。判斷路徑差異時，先看attachment與ANA，不要把另一台讀到不同時間的資料直接解釋為有兩份獨立副本。'),
       ('Flexible資源有明確的配置階段','VQ描述一組SQ／CQ資源，VI描述interrupt vector。資源不能同時屬於兩台controller；secondary在Offline時才能進行相關配置。常見順序是Offline、分配資源、適當CLR、Online，再由Host啟用。每一步完成後讀回狀態，才能定位是資源不足還是順序不合法。'),
       ('CFS不一定是媒體壞掉','Secondary進入Offline也會設定CFS，所以先查角色與管理狀態。若primary被disable、reset或shutdown，相關secondary也會受影響。只看CFS就立即判硬體故障，會忽略這種由合法管理流程造成的狀態。')])
    chapter('capacity',256,267,'NVM Set、Endurance Group 與容量 || NVM sets, endurance groups and capacity',
      '容量欄位分布於不同管理層級，健康計數也有自己的範圍。本冊先理解歸屬，再計算Create／Delete實際改變哪一層的容量。 || Establish ownership before interpreting layer-specific capacity and group-scoped health.',
      '容量不是只有一個剩餘數字 || Capacity has multiple accounting layers',
      'namespace的blocks、Group的bytes與實體容量調整不能混算。 || Namespace blocks, group bytes and adjusted physical consumption differ.',
      ['層級 || Layer','觀察 || Observation','常見誤解 || Common mistake'],[
       ['Namespace || Namespace','NSZE、NCAP、LBA Format || Logical size/capacity and format','把blocks直接當bytes || Treating blocks as bytes'],
       ['Set／Group || Set/group','總容量與未配置容量 || Total/unallocated capacity','把不同資源池加總兩次 || Double-counting resource pools'],
       ['實體配置 || Physical allocation','CAF、配置粒度 || Adjustment and granularity','假設邏輯容量等於消耗量 || Equating logical size and physical cost'],
       ['健康 || Health','LID09h、EGCW || Group log/warnings','用SMART單位解Group計數 || Using SMART counter units']],
      'CAF=200時，要求5GiB的Group可消耗10GiB的上層容量，還需考慮配置粒度。這不表示namespace的每個LBA大小也加倍。 || CAF200 can make5 GiB consume10 GiB before granularity effects; it does not double LBA size.',
      ['capacitymodel','capacitycmd','capacityop','eghealth','egevents'],[
       ('先畫容量往哪裡分配','支援Sets時，namespace屬於Set，Set屬於Group，Group屬於Domain。未支援Sets的裝置不需要虛構一層Set0。每個Create都應查它直接使用的資源池，不能拿subsystem總剩餘容量代替所選Group的可用容量。'),
       ('一層變動不代表每層都同樣變動','建立或刪除Set會影響Group內的未配置容量，但不應直接要求UNVMCAP跟著同樣增減。因為該Group已經從更上層取得容量，內部分配只是改變使用方式。驗證時把各層欄位放在同一表，先說明預期影響，再比較差值。'),
       ('容量不足的補充資訊要保留原文差異','Capacity Management的容量不足規則要求Error Information提供補充值，但所附版本正文與Figure165對該數值的措辭有差異。教材會保留兩處定位，不自行把它們改成相同意思。遇到規範自身矛盾時，能確定的Status與不能唯一決定的補充值要分開說。')])
    chapter('media',268,275,'Domain、Reclaim Group 與 Media Unit || Domains, reclaim groups and media units',
      '管理歸屬與FDP放置關係要用不同視角閱讀。本冊先辨認各種ID的範圍，再追蹤一筆Write如何選到RU，最後解讀媒體資訊的限制。 || Distinguish ownership from FDP placement, then follow identifiers to an RU and interpret media-report limits.',
      '從Write的PID走到目前RU || Follow a write PID to the current RU',
      'PID裡的PH不是RUH ID；必須先經過namespace的對照表。 || A PID placement handle is not the RUH identifier; apply namespace mapping.',
      ['步驟 || Step','假設值 || Hypothetical value','選到什麼 || Selection'],[
       ['解PID || Decode PID','RGID=1、PH=0 || RGID1, PH0','指定RG1及namespace的PH0 || RG1 and namespace PH0'],
       ['查對照 || Map handle','NS1.PH0→RUH2 || NS1 PH0 maps to RUH2','選RUH2 || RUH2'],
       ['查目前參照 || Current reference','RUH2在RG1參照RU乙 || RUH2 references RU B in RG1','這次Write使用的RU || Current placement RU'],
       ['RU用滿後 || After filling','controller更換目前RU || Controller replaces active RU','PH可不變，實際RU改變 || Stable PH, different RU']],
      '若另一namespace的PH0對RUH3，即使兩筆Write的PID數字相同，也可能使用不同RUH。比較前必須保留NSID與配置。 || Equal PID values in two namespaces can map to different RUHs; preserve NSID and configuration.',
      ['fdpmodel','fdpcontrol','fdpnvm','mediaunit'],[
       ('歸屬圖與放置圖各有用途','歸屬圖回答namespace用哪個Group的容量；放置圖回答這筆資料要透過哪個handle與RG放進目前RU。兩者互相關聯，但不能把所有名詞塞成一條包含鏈。畫圖時標清楚箭頭代表歸屬還是參照，才不會把可變的RU參照誤當永久物件位置。'),
       ('Write容錯不等於所有FDP命令容錯','Write帶非法PID時有特定fallback與事件規則，目的在讓資料仍能被放到可用位置。但RUH Update是明確的管理要求，非法參數不能自動套用同一種補救。閱讀錯誤規則時先確認是哪個命令，不能只因都使用RUH就共用答案。'),
       ('耗損資訊不能直接變成Ready判斷','Media Unit的PUSED及AVSP提供耗損與spare資訊，沒有一個通用位元能直接推論namespace已不可用。PUSED超過100也不代表所有I/O必須失敗。要判斷存取問題，還需看attachment、controller狀態、ANA及實際CQE，媒體欄位只是補充證據。')])
    chapter('pointers',276,285,'PRP 與 SGL || PRP and SGL',
      '資料指標描述的是記憶體配置。本冊先算PRP跨頁，再讀SGL的descriptor關係，最後把格式錯誤與傳輸失敗分開。 || Learn memory layout through PRP boundary calculations, SGL descriptor relationships and distinct error classes.',
      '4KiB頁面，PRP1從offset1024開始 || A 4 KiB page with first offset 1024',
      'PRP2類型由跨頁數決定；不能只用資料總長是否大於一頁判斷。 || Boundary crossings, including the first offset, determine PRP2.',
      ['資料長度 || Transfer length','第一頁之後剩餘 || Remaining after first page','PRP2用途 || PRP2 role'],[
       ['2048bytes || 2048 bytes','0 || 0','保留不用 || Reserved'],
       ['4096bytes || 4096 bytes','1024 bytes || 1024 bytes','直接指第二頁 || Direct second-page pointer'],
       ['8192bytes || 8192 bytes','5120 bytes || 5120 bytes','指PRP List || PRP-list pointer']],
      'SGL Last Segment.LEN=32描述2筆16-byte descriptors；實際payload多長，要讀這兩筆Data Block.LEN。不要把descriptor清單大小當成資料大小。 || A 32-byte last segment contains two descriptors; their data lengths determine payload size.',
      ['pointers','sgls','retirement'],[
       ('先算第一頁還剩多少','頁面大小P=4096、起點offset=1024，代表第一頁只能放3072bytes。長度4096雖然剛好是一頁大小，仍需要第二頁。這就是為什麼PRP判斷一定要包含offset。把資料畫成第一段3072加剩餘段，比死背某個長度門檻更不容易出錯。'),
       ('清單本身也占記憶體','PRP List每筆8bytes，4KiB清單頁從頁首開始可放512筆。如果還要下一頁清單，最後一筆是鏈結，就只剩511筆描述資料。SGL則每筆16bytes，而且Segment.LEN描述下一段清單，不是payload。把清單空間與資料空間分色或分欄，能避免兩種長度混用。'),
       ('格式錯誤與存取失敗需要不同證據','PRP offset不合法可從欄位直接看出；位址格式合法但記憶體已被Host回收，則是另一種存取問題。保存原SQE、清單與buffer生命週期，才能定位。SGL也可能先傳合法部分，之後才檢出另一筆錯誤，所以失敗CQE不證明整個buffer完全未變。')])
    chapter('interrupts',286,296,'Interrupt 設定與完成通知 || Interrupt configuration and completion delivery',
      '先確認CQE真的存在，再查通知如何送到Host。本冊把CQ關聯、合併、mask與Host處理分開，避免把沒有中斷當成沒有完成。 || Establish CQE posting before diagnosing routing, aggregation, masks and host consumption.',
      '四個控制，四個不同問題 || Four controls answer different questions',
      'FID09h.CD停用的是coalescing，不是interrupt。 || FID09h.CD disables coalescing, not interrupts.',
      ['控制 || Control','欄位／介面 || Interface','決定什麼 || Meaning'],[
       ['CQ通知路徑 || CQ routing','Create CQ.IV／IEN || IV/IEN','用哪個vector、是否通知 || Vector and notification enable'],
       ['合併 || Aggregation','FID08h.TIME／THR || TIME/THR','建議合併時間與數量 || Recommended delay/count'],
       ['單vector例外 || Per-vector override','FID09h.CD || CD','是否停用該vector合併 || Disable aggregation for this vector'],
       ['遮蔽 || Masking','INTMS／INTMC或MSI-X masks || Mode-specific masks','是否允許送出中斷 || Allow delivery']],
      '兩條CQ共用IV3，mask=1時仍可能寫入CQE。解除mask後，一次通知可讓Host處理多筆完成，不要求每筆補送一次中斷。 || Shared masked CQs can accumulate entries; one later interrupt can cover many completions.',
      ['interruptfeature','interruptmask','interruptfull','create'],[
       ('先從CQ找答案','中斷只是提醒Host查看CQ，命令真正結果仍在CQE。若沒有通知，先看正確CQ位置及Phase；有新完成就往IEN、IV、mask與coalescing查，沒有新完成才繼續往提交與執行追。這個順序能把兩種完全不同的問題分開。'),
       ('Mask與合併不能用同一個bit思考','CD=1表示不套用合併，反而可能更快通知；mask=1則阻止通知送出。Pin／MSI用INTMS寫1設定、INTMC寫1清除，MSI-X則用自己的mask。不能在MSI-X模式存取INTMS／INTMC，也不能用Get FID09h的值證明真正mask已解除。'),
       ('量測合併時保留建議的強度','TIME與THR是Host給controller的建議，PCIe允許實作選擇如何使用，甚至不做合併。測試可以描述觀察到的延遲與中斷量，但不能僅因沒有精準等到門檻就判違規。Host持續更新CQ Head也可能讓聚合計時重新開始，必須把處理中的活動一起記錄。')])
    chapter('integration',297,320,'整合驗證與證據交叉比對 || Integrated validation and evidence correlation',
      '本冊把前面機制放進具體矛盾情境：先確認比較的是同一對象與同一時點，再判斷證據是否足夠。相關機制使用固定連結，不重複整段教學。 || Apply prior mechanisms to apparent contradictions, matching identity and time before judging evidence.',
      '一條可重走的驗證路徑 || A reproducible evidence path',
      '先寫出要驗證的規範要求，再選資料；資料多不等於證據完整。 || State the requirement before collecting evidence; volume is not completeness.',
      ['階段 || Stage','保存什麼 || Preserve','避免什麼誤判 || Avoid'],[
       ['前提 || Preconditions','能力、scope、設定、狀態 || Support, scope, configuration, state','把支援當成所有參數皆合法 || Support means all requests are legal'],
       ['操作 || Operation','原命令、selector、時間 || Request, selectors, time','用事後重建內容代替原件 || Reconstructed rather than original evidence'],
       ['結果 || Results','CQE、狀態Log、事件 || Completion, logs, events','把接受當成背景操作結束 || Acceptance equals operation completion'],
       ['持續性 || Persistence','reset來源及前後狀態 || Reset type and state changes','把全部reset當成同一件事 || All resets have identical effects']],
      '「Sanitize CQE成功、Log仍進行中」可正常；「同一操作確定已結束、相同scope的Log仍永久進行中」才需要進一步找新操作、快取或狀態更新問題。 || Successful initiation with progress is normal; confirmed final completion with persistent same-scope in-progress data needs investigation.',
      ['status','commandseffects','feature','getlog','aerfull','pelcontext'],[
       ('先排除假矛盾','比較的controller、NSID、CSI、UUID、SEL或時間不同，結果就可能合理不同。遇到不一致時先列出這些條件，再看是不是同一個物件的同一種資料。例如Active List不同不代表資料損壞，Current與Saved不同也不代表Set失敗。'),
       ('每次只改一個能解釋結果的條件','建立合法基準後，只改一個參數或順序，才能知道錯誤是誰造成的。如果NSID、PRP與命令狀態同時不合法，回報任何一個先檢出的錯誤都可能合理。測試設計的工作是讓證據能回答問題，而不是先選一個期待的Status再找理由。'),
       ('結論也要保留證據界線','能證明違反shall時就明確指出；只偏離should時保留建議強度；規範未定義或原文互相矛盾時，說明哪一部分無法唯一判定。這不是省略答案，而是讓符合性結論可被另一位讀者重新檢查，不把猜測寫成規範要求。')])
