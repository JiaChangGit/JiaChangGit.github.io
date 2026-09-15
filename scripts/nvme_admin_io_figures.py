"""Report-local examples and field relationships; never alter older courses."""
EXAMPLES={}
GUIDES={}
NVM_EXAMPLES={
 90:dict(takeaway='NVM 的 Notice 表補充命令集特定事件，仍使用 Base AER 的 AET／AEI 格式。',example='事件值只指出需要關注哪種 NVM 狀態，不是一般 Read 的完成結果；相關但未納入的 Log 不在本次展開。'),
 110:dict(takeaway='Error Information 的 NVM User Data 欄位在適用時指出發生錯誤的最低編號 LBA。',example='若本次可回報錯誤範圍包含 LBA 100 與 108，這個欄位依定義取最低的 100；不把其他 Log 的位置保證套到這裡。'),
 132:dict(takeaway='Namespace Granularity List 用 GDM 決定格式到粒度描述子的對應，ND 表示零起算的描述子數量。',example='ND=1 表示兩筆描述子；要知道 Format Index 1 用哪一筆，還需先讀 GDM 的對應規則。'),
 133:dict(takeaway='每筆粒度描述子的 NSG 與 NCG 分別給 namespace 大小和容量的建議 byte 粒度。',example='250 個 4096-byte blocks 是 1000 KiB；若建議粒度為 1 MiB，必須先統一 bytes 才能比較，不能把 250 直接和 1048576 比。'),
}
NVM_GUIDES={}
NVM_EXAMPLES.update({
 192:dict(takeaway='NLBAF 用零起算表示共用能力的格式數，NULBAF 直接表示另外的非共用格式數；先換算個數再讀分組。',example='NLBAF=2、NULBAF=2 表示 3+2=5 個格式，索引 0–2 屬共用能力群，3–4 屬非共用群；原始值 2+2 會少算 1 個。'),
 193:dict(takeaway='CNS 00h／05h／08h 只讀 NLBAF 群；CNS 09h／0Ah 可依 Format Index 查兩群的能力。',example='若 index 3 屬 NULBAF 群，先用 CNS 09h 查其 NVM Namespace 格式資料，再用 0Ah 查命令集專屬資料，不以共用的 broadcast 查詢結果代替。'),
})


def example(n, takeaway, worked):
    EXAMPLES[n]=dict(takeaway=takeaway, example=worked)


example(143,'Opcode 必須連同 Admin 命令集、傳輸方向與 NSID 用法判讀；本篇只讀保留命令的列。','Admin 02h 讀 Log，I/O 02h 讀資料；兩者數值相同，但所屬命令集不同。')
example(144,'本篇使用 Format 欄判斷進行格式化時仍可處理哪些管理要求及其限制。','Format 進行期間，Error Information 的 LBA 欄依表要求回 0h，不能把這個值當成 LBA 0 發生媒體錯誤。')
example(147,'Abort 的 CDW10 同時指定原命令的 SQID 和 CID。','SQID=3、CID=7 形成 CDW10=00070003h；SQ 4 上的 CID 7 不在這筆要求的目標內。')
example(148,'IANP 只回答是否執行了立即中止，不能單獨證明原命令的最終結果。','IANP=1 時，原命令可能稍後才以 Command Abort Requested 完成，也可能早已正常完成；必須再讀原 CQE。')
example(149,'Abort Command Limit Exceeded 指尚未完成的 Abort 太多，不是原 SQ 的命令數超限。','若目前已達 ACL 所允許的並行數，再送一筆 Abort 可能回 03h；增加原 SQ 的記憶體深度不能解除這個限制。')
example(150,'AER 的命令專屬 status 05h 表示同時尚未完成的事件要求超過上限。','AERL 的編碼換算成允許的要求數後再安排 AER；不要把長時間等待事件誤當作要求已失效而一直補送。')
example(151,'AER 的 DW0 用 AET 選事件表，再以 AEI 與 LID 指出事件內容及相應紀錄。','AET=001b、AEI=01h 是溫度門檻事件；AEI=01h 若出現在其他 AET 下，必須換到那張表解讀。')
example(152,'EVNTSP 的含義由特定事件決定，沒有定義時就是該事件的保留欄位。','收到電壓事件才用電壓事件的感測器與量測格式；不能把另一事件的 DW1 也解成相同 bit 欄位。')
example(153,'Error Status 的事件資訊區分不存在的 doorbell、無效寫入值及控制器內部錯誤。','寫一個未建立的 queue doorbell 是 00h；已存在的 queue 卻寫出非法 pointer 值是 01h，兩者不是同一條件。')
example(154,'SMART／Health 事件分成可靠度、溫度門檻與 spare 低於門檻三類。','AEI=01h 要再確認是哪個感測器與上下限條件；它不等於所有感測器都過熱。')
example(155,'Notice 的 AEI 指定狀態變動的類別；本篇以 namespace 清單變動與 firmware 啟用通知連到保留的 Log。','收到 namespace 變動通知後讀 LID 04h，再重新 Identify 受影響對象；通知不是一份完整的 namespace 清單。')
example(156,'I/O Command Specific Status 的 AEI 必須在其專屬 AET 分支解讀；這張表不提供一般 Read／Write 的 CQE status 對照。','AER 是事件通知；某一筆 Read 的成功或失敗仍從那筆 Read 的 CQE 判斷。本表的專題事件流程不在本篇重講。')
example(157,'Immediate 事件有自己的處理方式，包括正常 subsystem shutdown 與溫度遲滯恢復。','Temperature Threshold Hysteresis Recovery 表示遲滯事件結束；它不是重新發出同一個過溫事件。')
example(158,'One Shot 的 AEI 指出單次通知種類，再由相應 EVNTSP 格式補充目標或量測。','One Shot 的 03h 先選到電壓事件，再讀 Figure 159；不能只拿 03h 到 Error Status 表找定義。')
example(159,'電壓事件用 VSENT 選感測器、VTHT 分超壓或欠壓、IVM 配合 VOLSS 換算電壓。','相同 IVM 數字若配到不同 VOLSS，代表的伏特數不同；先確認 VSENT 指到哪一筆 Identify 感測器資料。')
example(160,'功率事件把 PMT 的量測類別與 IPV／IPS 的數值及倍率分開儲存。','收到一個功率數值時，先以 IPS 換算成 Watts，再和同一 PMT 的情境比較；本篇不進入功率 Feature 的配置。')
example(161,'這個事件的 EVNTSP 回報 CDQID，而不是把 tail pointer 的位移直接放進 DW1。','DW1 低 16 bits=3 表示事件屬於資料佇列 3；不能把它當作 tail 已前進 3 bytes 或 3 entries。')
example(187,'本篇讀 firmware 的 CA 與 FS：先選保存或啟用動作，再指定 slot，Boot 專用 CA 不展開。','映像存入 slot 2 後，是否會立即執行取決於 CA 與支援能力；FS=2 本身不保證立即切換。')
example(194,'Format 的範圍先由 SES 決定使用 FNS 或 SENS，再由 scope bit 與 NSID 選出影響對象。','SES=000b、FNS=1 時，即使 NSID=3，也不能只按 namespace 3 解讀影響範圍。')
example(195,'Format CDW10 把 Format Index、secure erase 與命令集專屬格式設定放在不同欄位。','Format Index=18（12h）需要 LBAFU=1、LBAFL=2，並滿足延伸格式的前提；SES 與這個索引是獨立選擇。')
example(196,'Invalid Format 不只表示格式編號不存在，也可能表示 metadata 空間或目前配置不允許所選格式。','所選 PI 需要的 metadata 大於格式提供的空間時，不能只檢查 Format Index 有在清單中就認為要求有效。')
example(200,'Get Features 的 FID 表是共同入口；本篇只讀保留 FID 的列，再到各功能定義解讀回覆。','FID=07h 回覆的是佇列數量相關資訊，不用 FID=02h 的 Power State 欄位解讀同一個 DW0。')
example(209,'LID 表指出 Log 的名稱、scope 與是否使用 CSI；本篇保留八種 Log，不把整張清單當成報告範圍。','LID 03h 與 LID 02h 的作用範圍及欄位不同；即使都由 Get Log Page 讀取，也不是同一種紀錄。')
example(212,'Error Entry 先用 ECNT 判定紀錄，再用 SQID／CID、STS、PEL、NSID 及有效的專屬資訊描述錯誤。','PEL 的 BYTLOC=40、BITLOC=0 指 SQE 的第 40 byte 中 bit 0，不是 LBA 40，也不是第 40 個 Dword。')
example(214,'每個 Temperature Sensor 項目以 Kelvin 儲存溫度；0h 表示沒有實作該感測器。','TST=300 表示約 26.85 °C；TST=0 不能翻成裝置溫度為 −273.15 °C。')
example(216,'Commands Supported and Effects 依 Admin 與 I/O 分成兩張固定位置的 opcode 索引表。','Admin Opcode 02h 的項目在 byte 8；I/O Opcode 02h 的項目在 byte 1032。相同 opcode 要先選對清單。')
example(217,'每個命令項目分別回報支援、資料或能力變動、執行限制與作用範圍。','CSUPP=1 只回答支援；若 NCC 表示可能改變 namespace 能力，完成後還應重新 Identify，而非直接沿用舊格式資料。')
example(270,'Feature Identifiers Effects Log 以 FID 為索引，每筆項目描述 Set Features 對該功能的影響。','FID 07h 的項目從 byte 7×4=28 開始；這是 Log 內的 byte offset，不是 Get Features 的回覆值。')
example(271,'FID 項目分別回報支援、scope、UUID 選擇支援及可能造成的內容或能力變動；保存與變更能力另由 Get Features 查詢。','FSP=0 表示未回報 scope，不是「完全不影響任何對象」；非零 FSP 按規格只設一個 scope bit。')
example(304,'MDCSV 選資料結構版本，MDCS 的三個旗標分別描述不同層次的預設配置狀態。','DNCS=0 可能是目前不同於預設，也可能是控制器不支援對應能力；先看相應 support bit，不能直接宣稱配置已被改過。')
example(331,'Get Log Page 的 status 分清 LID、controller identifier 與命令集不受支援三類問題。','9h 的 Invalid Log Page 不等於 1Fh 的 Invalid Controller Identifier；後者應對照 LSI 中選到的 controller。')
example(332,'Identify 的 DPTR 指向固定大小的結果 buffer；使用 PRP 時本節不允許以 PRP List 取代該指標。','4096-byte 結構最多跨一個 page boundary；不能因為其他命令支援 PRP List，就把同一種配置直接套用到 Identify。')
example(333,'CNS 決定回傳結構種類，CNTID 只在指定的 Identify 操作中用來選 controller。','查不使用 CNTID 的 CNS 時，主機依規格將 CNTID 清為 0，而不是把 namespace 的 NSID 填到那裡。')
example(334,'CSI 選命令集，CNSSID 的意義則由 CNS 決定；兩個欄位不能互換。','查 CNS=04h 時，低 16 bits 用作 NVM Set 清單的起始識別碼；不能把那個值解成 CSI。')
example(335,'UIDX 是 Identify 的 UUID 選擇欄位，不是回傳結構中的 namespace ID。','一般標準結構的查詢不應隨意填入一個 UUID Index；本篇不展開已排除的 UUID List。')
example(336,'CNS 表同時說明回傳哪一種結構及哪些目標欄位參與查詢；只使用本篇保留的入口。','CNS=05h 要配合命令集選擇；CNS=02h 回傳目前可存取的 NSID 清單，不能把前者的結構套在後者。')
example(338,'這張長表以裝置身分、命令限制、功能能力與電源描述子建立控制器全貌；各能力只對其對應操作成立。','ACL、AERL、MDTS 分別限制 Abort 數量、AER 數量及資料傳輸量；把三者都當成 queue depth 會做出錯誤配置。')
example(339,'Voltage Sensor 結構同時描述採樣間隔、量測倍率與感測器對應的供電輸入。','IVMSR 用 VSRV 與 VSRS 算時間；IVM 另用 VOLSS 算 Volts，不能拿時間倍率去換算電壓。')
example(341,'Time Scale 表把編碼對應到時間單位，必須與使用它的數值欄位一起換算。','原始數值 10 若配不同 scale，實際時間不同；先選這張表的時間單位，再乘以該欄位數值。')
example(342,'Namespace Identification Descriptor 以 NIDT 選資料型別，NIDL 給 payload 長度，再讀 NID。','一筆 16-byte 識別資料不代表整筆描述子只有 16 bytes；前面還有 descriptor header，下一筆要從完整長度之後開始。')
example(343,'CNS=04h 的 CNSSID 用 NVMSETID 決定 NVM Set 清單起點。','要繼續列舉時，應依這一節的起點條件選下一個識別碼；不要把它當成資料 buffer 的 byte offset。')
example(344,'NVM Set List 先給 NUMENT，再列出各組 NVM Set Attributes Entry。','NUMENT=2 時先讀兩筆有效 entry；4096-byte 回覆中剩下的空間不能都當成另一些 NVM Sets。')
example(345,'每筆 NVM Set 項目把 set 與 endurance group 識別、效能提示及總量／未配置容量連在一起。','OWS 用 bytes；TNVMSC 與 UNVMSC 也用規定的容量單位。不能把 OWS 當成這個 NVM Set 裡的 namespace 數量。')
example(349,'CNS=18h 用 DID 指定 Domain List 的起始 domain。','DID 是資源識別碼，不是第幾個 4 KiB 區塊；分段列舉需按本節對起始值的規則前進。')
example(350,'Domain List 用 NUMENT 界定後續有效的 Domain Attributes Entry 數量。','NUMENT=1 表示只解一筆 domain 資料，不能把回覆尾端零值視為第二個 domain。')
example(351,'Domain 項目以 DID 配對總容量、未配置容量與單一 Endurance Group 可用上限。','TDC 與 UDC 是同一 domain 的總量和剩餘量；MEGDC 則是另一個配置上限，不能拿它取代 UDC。')
example(352,'CNS=19h 的 ENGGID 選 Endurance Group 清單起點。','ENGGID 是 Endurance Group ID；雖然同樣放在 CDW11 低位元，也不是 CNS=18h 的 Domain ID。')
example(353,'Endurance Group List 用 NEGIDS 說明後面有多少個有效的 group identifiers。','清單回報三個 ID，意思是三個可列舉的 Endurance Groups，不是總容量 3 blocks。')
example(354,'Identify I/O Command Set 結構列出可選的命令集組合，每個 IOCSC 是一個 vector。','IOCSCI=2 選第 3 個組合；組合裡可以有多個命令集位元，不能把組合索引當成 CSI。')
example(355,'I/O Command Set Vector 的各 bit 表示某命令集是否在組合中選用。','NVMCS=1 表示該組合包含 NVM Command Set；它不保證每個選用 NVM 命令都受到支援。')
example(356,'Underlying Namespace List 的 GENCTR 辨識清單版本，NUMENT 界定有效的對應項目數。','分段查詢前後 GENCTR 改變，不能直接把兩段當成同一版對應關係；本篇只讀結構，不教 export 流程。')
example(357,'每筆 Underlying Namespace 項目把底層 namespace 的 NSID 與 controller 對應連起來。','兩個不同底層儲存對象都可能使用 NSID=1；必須保留其所屬對象及 controller context，不能只用數字 1 合併紀錄。')
example(358,'Supported Controller State Formats 分開列出 NVMe state format 版本與廠商格式 UUID。','NV 與 NUUID 是兩組項目的個數，不能把 NV=2 當成「目前控制器正在使用版本 2」。')
example(456,'Security Receive 的 DPTR 指向主機接收協定回覆的 buffer。','主機預留的接收空間要配合 AL；DPTR 只給位置，不表示已經收到一份成功的安全協定結果。')
example(457,'Security Receive 的 SECP、SPSP 與適用的 NSSF 共同選出所要讀取的協定回覆。','SPSP1=12h、SPSP0=34h 合成 1234h；低 8 bits 的 NSSF 不是 SPSP 的第三個 byte。')
example(458,'AL 使用 Security Protocol In 的配置長度規則，不是零起算的 Dword 數。','512-byte 接收長度不套用 NUMD=127 的 Get Log Page 編碼；先按安全協定長度定義提供 AL。')
example(459,'在 SECP=EAh 下，SPSP 再選協定用途，NSSF 的含義也跟著該用途改變。','SPSP=0001h 與 0002h 是不同用途；只能依選中的那一列解讀 NSSF，不能跨列混合。')
example(460,'Security Send 的 DPTR 指向待送出的安全協定資料。','主機 buffer 存的是協定訊息；它不是 namespace 的一般 Write user-data buffer。')
example(461,'Security Send 的選擇欄位格式與 Receive 配合，但這筆操作負責把資料送入控制器。','相同 SECP／SPSP 可出現在請求與回覆階段，仍須依協定配對，不能只靠欄位值相同就視為同一次交易。')
example(462,'TL 表示 Security Protocol Out 的傳輸長度，與 Receive 的 AL 分別描述傳出資料和接收配置。','傳出 256 bytes、預留接收 512 bytes 是合理的不同數量；不必為了讓 TL 等於 AL 而補送無關資料。')
example(466,'Set Features 的 FID 表是設定入口；本篇只讀保留項目與其 scope、保存和變更規則。','FID=06h 設定 write cache，FID=07h 協商 queue 數量；同樣使用 CDW11 不代表兩者有同樣位元含義。')
example(467,'仲裁設定用 HPW／MPW／LPW 控制權重，AB 控制一次仲裁的 burst 上限。','某個 weight 欄位填 3 表示對應的 4 個命令單位；AB 則依 2 的次方或特殊值解讀，不能全部加 1。')
example(469,'Power Management 的 Get 回覆同時給目前 PS、WH 和 IIELL。','IIELL=20 以 100 μs 為單位是 2 ms；PS=3 是狀態編號，不是 3 ms。')
example(471,'WCE 控制 volatile write cache 是否啟用，不能單獨代替資料已持久保存的證據。','WCE=1 時，普通 Write 成功不自動等同已提交至非揮發性媒體；還要看 FUA 或後續 Flush。')
example(472,'Number of Queues 的 NCQR／NSQR 分開表達主機要求的 CQ 與 SQ 數量。','各要求 4 條時都填 3；需要 4 條 SQ 並不代表一定需要 4 條 CQ，因多條 SQ 可共用 CQ。')
example(473,'NCQA／NSQA 回報實際配置數量，主機必須依回覆決定後續能建立多少佇列。','請求值是 3，但回覆 NCQA=1，代表分配 2 條 CQ，不能照請求自行建立 4 條。')
example(479,'Set Timestamp 的 TSTMP 是自 UTC epoch 起算的毫秒值。','1000 表示 epoch 後 1 秒，不是 1000 秒；結構中未定義的 bytes 按 reserved 規則處理。')
example(480,'Get Timestamp 除了時間值，還回報時間來源及計時是否可能停止的屬性。','如果 SYNC 表示計數可能曾停止，就不能把與主機時鐘的差值全部解釋成傳輸延遲。')
example(494,'IOCSCI 選擇 Identify I/O Command Set 清單中的組合索引。','IOCSCI=1 選第 2 個支援組合，不是直接設定 CSI=1，也不會替 namespace 變更資料格式。')
example(495,'Get I/O Command Set Profile 回傳目前選定的組合索引。','回覆 IOCSCI=2 後，要讀先前取得的第 3 個 vector 才知道含有哪些命令集。')
example(536,'PBSLC 是主機提供的 pre-boot software load count，並非控制器自行估算的工作完成百分比。','PBSLC=3 不能呈現為「已完成 3%」；它是在這個 Feature 定義下的載入計數。')
example(543,'TIME 與 THR 是中斷聚合的時間及完成項目門檻，兩者的編碼方式不同。','TIME=10 對應 1 ms；THR=7 對應 8 個完成項目的門檻。0 值另有停用規則，不能一律解成正常的最小門檻。')
example(544,'CD 對指定 IV 停用中斷聚合，而不是停用這條 CQ 的所有中斷。','IV=2、CD=1 讓 vector 2 不採用 aggregation；CQ 是否啟用中斷仍由建立 CQ 時的 IEN 決定。')
example(554,'Set Features 的命令專屬錯誤分辨不可保存、不可變更、作用對象及支援條件。','Feature Not Saveable 和 Feature Not Changeable 是不同結果；把 SV 清零不能自動解決不可變更的值。')
example(571,'Create CQ 的 PRP1 要配合 PC 解讀為連續記憶體基址或所需的 PRP 配置。','PC=1 時，PRP1 是新 CQ 的對齊基址；不能填入另一條 SQ 的位址或一般資料 buffer。')
example(572,'CQ 的 QID 與 QSIZE 分別選新佇列識別碼和零起算深度，Admin Queue ID 不可當成新 I/O CQ ID。','建立 QID=2、深度 64 的 CQ，QSIZE=63；QSIZE=0 被本節禁止，不代表可以建立單一 entry 的 I/O CQ。')
example(573,'CQ 的 IV、IEN 與 PC 分別指定中斷路徑、是否啟用中斷及記憶體是否實體連續。','IEN=0 時主機可用輪詢讀 CQE；這不表示 CQ 不會收到完成項目。')
example(574,'Create CQ 的 status 將佇列 ID、深度與中斷 vector 的錯誤分開回報。','Invalid Interrupt Vector 應檢查 IV 的可用範圍，不應把 QSIZE 改大來嘗試解決。')
example(575,'Create SQ 的 PRP1 配合 PC 指向 Submission Queue 的記憶體配置。','即使 SQ 和 CQ 深度相同，兩者是不同的 buffer；SQ 的 PRP1 不應直接沿用 CQ 的基址。')
example(576,'SQ 的 QID 與 QSIZE 定義提交端的識別與深度，並受控制器最大 queue entries 限制。','深度 128 的 SQ 以 QSIZE=127 編碼；SQ ID 可以與另一個 CQ ID 數值相同，因兩種 ID 有不同名稱空間。')
example(577,'CQID 建立 SQ 到 CQ 的引用，QPRIO 選仲裁優先類別，PC 描述 SQ 的記憶體配置。','SQ 3、SQ 4 都可填 CQID=2；CQID 不是中斷 vector，也不是下一筆 command 的 CID。')
example(578,'NVMSETID 指定 SQ 關聯的 NVM Set，與 SQ 的 QID 及資料命令的 NSID 不同。','QID=3、NVMSETID=5 表示「SQ 3 關聯 set 5」，不能改寫成 namespace 5 或 CQ 5。')
example(579,'Create SQ 的 status 除 ID 和深度外，也檢查要引用的 CQ 是否有效。','在 CQ 2 尚未建立時建立 SQ 指向 CQ 2，應看 Invalid Completion Queue，而非以為 SQ 的 PRP 記憶體太小。')
example(580,'Delete CQ 以 QID 指定要移除的完成佇列，且須滿足沒有 SQ 仍引用它的條件。','若 SQ 3 還指向 CQ 2，先刪除 SQ 3 再刪 CQ 2；不能因 CQ 暫時沒有新完成項目就直接移除。')
example(581,'Delete CQ 區分 ID 無效與目前不允許刪除的完成佇列。','QID 根本不存在與仍被 SQ 引用是不同情境；前者查 ID，後者查引用關係。')
example(582,'Delete SQ 用 QID 指定要移除的提交佇列，不是用 CID 中止其中某一筆命令。','QID=3 刪除整條 SQ 3；若只想指定 SQ 3 裡 CID 7 的要求，那是前面 Abort 的目標格式。')
example(583,'Delete SQ 的命令專屬錯誤指出提交佇列識別碼無效。','已刪除 SQ 3 後又用同一 QID 要求刪除，不應把失敗回覆當成原先資料命令的執行結果。')
example(645,'本篇從 I/O Opcode 表只取 Flush 列，與後面的 NVM 命令 opcode 一起辨識命令集。','Flush 是 I/O 命令，不因為作用是持久保存，就放到 Admin Submission Queue。')


def fields(numbers,key,title,relation,*rows):
    guide=dict(id='adminio-'+key,title=title,relation=relation,rows=list(rows))
    for n in numbers:GUIDES[n]=guide


fields([143,144,645],'command-map','命令集、方向與狀態是三次判斷',
 '先選 Admin 或 I/O，再看本篇保留的 opcode 列；支援與目前狀態允許的操作分開檢查。',
 ('Opcode function／Data Transfer／NSID Used','Opcode 低位元描述傳輸型態，但仍需看完整 opcode 和所屬命令集；NSID 的使用由該命令定義。','Admin 02h 與 I/O 02h 同值不同義；Flush 沒有一般 user-data payload。'),
 ('Format 進行中的允許命令列','讀 Figure 144 的 Format 欄及本篇保留命令的額外限制；正文保留 may／should 的要求強度。','Format 與其他 namespace 操作衝突時，要按是否已在執行及回覆條件分別解釋。'))
fields([147,148,149],'abort','目標命令、立即中止與最終完成',
 'Abort 自己的 CQE 和原命令的 CQE 分別提供不同證據；立即中止還有不得再造成後續效果的界線。',
 ('SQID／CID','CDW10 低 16 bits 是 SQID，高 16 bits 是原命令 CID；一起辨識目標。','SQID=3、CID=7 → 00070003h。'),
 ('IANP／原命令 status','IANP=0 表示立即中止已執行；=1 只表示未立即中止，最後結果看原 CQE。','Abort status 成功、IANP=1，不足以證明原資料 transfer 已停止。'),
 ('ACL／Abort Command Limit Exceeded','ACL 是從 0 起算的並行 Abort 限制；不要與 SQ depth 混用。','ACL=3 表示最多 4 筆 outstanding Abort；超過可能回 03h。'))
fields(list(range(187,194)),'firmware','把映像的傳送位置接到保存與啟用時機',
 '先看 Commit 的選擇，再看 Download 的欄位；實際更新仍先傳送完整映像，接著執行適用的保存及啟用動作。',
 ('CA／FS','只讀一般 firmware 動作：CA=0 保存已下載映像但不啟用；1 保存並安排下次 Controller Level Reset 啟用；2 對既有 slot 安排下次 Controller Level Reset 啟用；3 保存新映像後立即啟用，若沒有新下載則啟用 slot 的既有映像。各項仍須符合其支援條件。','CA=0 成功只證明映像已保存；之後仍要選所需的啟用動作。'),
 ('FRMW／FS／CA=3','slot 數、slot 1 唯讀及不經 reset 啟用的支援各自確認；FS=0 依規格由控制器選擇適用 slot。','裝置支援多個 slot，不代表每個 slot 都能覆寫，也不代表能立即啟用。'),
 ('MUD／MEFWO／ASQFWO','偵測多個更新序列的情況，與單筆 Download 片段重疊是不同層次。','先確認是否支援該回覆，再判斷更新序列是否受其他更新影響。'),
 ('DPTR／NUMD／OFST／FWUG','DPTR 給映像片段位置；NUMD 是 Dword 數減 1，OFST 是 Dword 位移；FWUG 約束粒度與對齊。','第二個 4096-byte 片段：NUMD=1023、OFST=1024，不把 OFST 也減 1。'),
 ('completion status／AFI.CAFS／NAFS／FRS','status 可能指出啟用所需 reset；LID 03h 分開檢查目前 slot、下次 slot 與版本字串。','NAFS=2 而 CAFS=1，表示目前仍執行 slot 1；不能用 slot 2 已有版本字串證明已切換。'))
fields([203,204,205,206,207,208,210,211],'get-log','一次 Log 讀取的目標、位置、長度與事件處理',
 '先依所選 LID 解讀 LSP／LSI，再設定要傳回主機的區段；所有欄位都有效，才構成可解讀的一次讀取。',
 ('LID／CSI／LSP／LSI','LID 選紀錄，CSI 在適用時選命令集；LSP／LSI 的定義由該 Log 指定。','同樣填 LSI=1，必須先知道該 Log 是否把它用作 controller identifier；不能任意當成 entry 1。'),
 ('NUMDU／NUMDL','合成 NUMD=(NUMDU<<16)|NUMDL，再以 (NUMD+1)×4 計算 bytes；只對合成值加 1。','512 bytes 使用 NUMDU=0、NUMDL=127。'),
 ('LPOU／LPOL／OT／IOS','合成 64-bit LPO；OT=0 使用 byte offset，OT=1 使用該 Log 的索引規則，後者先確認 IOS 支援。','位移 512 bytes 填 LPO=512；entry index 7 表示項目位置，不能未讀布局就換成 7 bytes。'),
 ('DPTR／RAE','DPTR 指接收記憶體；RAE=1 保留相應事件，RAE=0 在成功讀取時依事件規則清除。','讀取失敗不清除事件；事件處理與 NUMD 指定的 buffer 大小是兩個獨立條件。'),
 ('LSUPP／IOS／LID Specific Parameter','LID 00h 先確認 Log 與其進階選項的支援；每個 LID 的專屬參數仍依該紀錄解讀。','控制器支援 Get Log Page，不表示所有 LID 或 index 模式都可用。'))
fields(list(range(150,162)),'events','先解事件型別，再決定 DW1 和後續讀取',
 'AER 的格式是共同入口，後續事件表才定義 AEI 和 EVNTSP。這裡解釋收到的事件，不加入已排除功能的設定流程。',
 ('AET bits 2:0／AEI bits 15:8／LID bits 23:16','AET 選 Error、SMART、Notice、Immediate、One Shot 或命令集分支；AEI 再在分支內解碼。','AET=1、AEI=1 連到溫度門檻，不能直接把 AEI=1 當成所有事件共通定義。'),
 ('EVNTSP DW1','事件定義決定這 32 bits 的格式；未定義時為 reserved。','讀不屬該事件的位元表會把 ID 誤算成量測數值。'),
 ('AERL／status 05h','AERL 為零起算的 outstanding AER 上限，超限可能回 05h。','AERL=3 表示允許 4 筆，而不是 3 筆。'),
 ('一般事件／RAE','一般事件回報後遮蔽同類事件，依該事件規則成功讀取相應 Log 並清除才解除；RAE=1 保留。','正在分次讀取事件紀錄時先保留事件，讀取失敗也不應視為已清除。'),
 ('Immediate／One Shot','Immediate 只在事件當下已有 outstanding AER 時回報，沒有則不補報；One Shot 只回報一次，回報時由控制器清除，pending 事件的清除按各事件定義。','不要為了清除 Immediate 事件而任意讀一個無關 Log。'),
 ('Error／SMART／Notice 各表的 AEI','Error 指介面或內部錯誤；SMART 指健康條件；Notice 指狀態變化。','不存在的 doorbell 與 spare 低於門檻要進不同事件分支。'),
 ('VSENT／VTHT／IVM／VOLSS','VSENT 指向感測器，VTHT 分超壓或欠壓，IVM 乘該感測器的 VOLSS 換算 Volts。','先在 Identify 選同一感測器的倍率，再換算量測，不能只由原始 IVM 比較不同感測器。'),
 ('PMT／IPS／IPV','PMT 指量測類別，IPS 的倍率乘 IPV 得到 Watts；IPM 是含倍率和數值的欄位組合。','報告功率值時同時帶出類別、單位與這是 interval measurement 的背景。'),
 ('CDQID bits 15:0','Controller Data Queue 事件的 DW1 指出資料佇列 ID，本表沒有把 tail pointer 位置直接放入此欄。','CDQID=3 不等於 tail offset=3。'))
fields([194,195,196],'format','範圍與格式是互相獨立的兩組選擇',
 '先選影響哪些 namespaces，再選它們的新格式和 erase 設定；兩組條件都滿足才是一筆有效的 Format。',
 ('SES／FNS／SENS／NSID','SES=0 看 FNS，secure erase 看 SENS；所選 scope bit 與 NSID 一起決定範圍。','NSID=3、SES=0、FNS=1 仍影響規格定義的所有 namespaces。'),
 ('FNVMBS','這個 bit=1 時不支援 NSID=FFFFFFFFh 的 Format broadcast 用法，會回 Invalid Field in Command。','不能只看欄位名稱裡有 Support 就把 1 理解為支援。'),
 ('LBAFU bits 13:12／LBAFL bits 3:0','符合延伸格式前提時，Format Index=(LBAFU<<4)|LBAFL；格式須在可用清單中。','LBAFU=1、LBAFL=2 → Format Index 18，而非 12 bytes。'),
 ('SES bits 11:9','0 不要求 secure erase；1 User Data Erase，2 Cryptographic Erase；其餘值保留。','User Data Erase 完成後內容不指定為全零，不能拿零值讀回當成唯一成功條件。'),
 ('PIL／PI／MSET','這三個共同位置的 NVM 意義由 NVM Figure 91 補充，需與 metadata 空間和能力配合。','不能在沒有足夠 metadata 的格式上僅靠 PI 非零啟用保護。'),
 ('CQE／Invalid Format','Format CQE 在格式化完成時回報；Invalid Format 包含不支援格式或設定不相容等情況。','成功後重新 Identify 取得新格式，再計算後續 Read／Write buffer。'))
fields([212,213,214,215,216,217,270,271,304,331],'log-records','八種 Log 的內容，分別能證明什麼',
 '共同傳輸格式不重講；這一組直接把每個保留 Log 的欄位連到有效範圍、單位和後續判斷。',
 ('ECNT／SQID／CID／STS／PEL','ECNT=0 是無效 entry；非命令專屬錯誤的 SQID／CID 可為 FFFFh。PEL 分 byte 和 bit，STS 按 status 格式解讀。','BYTLOC=40、BITLOC=0 指向 SQE 第 40 byte 的 bit 0；不是 LBA。'),
 ('NSID／LBA／VSIA／CSI／opcode／命令專屬資訊','先確認欄位在該錯誤下有效，再回到對應 namespace、命令集和來源命令；VSIA=0 表示沒有額外廠商 Log。','錯誤紀錄中的值不足以定位特定命令時，不能憑 FFFFh 猜測最後一筆命令。'),
 ('Critical Warning／Available Spare／Percentage Used','分別表示警示位元、可用 spare 百分比與耐久度估計使用量，不能當成相同的剩餘容量。','Percentage Used 不是檔案系統已使用的磁碟空間比例。'),
 ('Composite Temperature／TST／Sensor entries','溫度用 Kelvin，感測器 entry 的 0 表示未實作；實際量測位置由實作決定。','300 K 約為 26.85 °C；未實作的 0 值不轉換成攝氏。'),
 ('Data Units／Host Commands／Media Errors／Error Entries','流量、命令次數、資料錯誤數與錯誤紀錄數是不同統計；NVM 計數補充集中在後面的 §4.1.4.1–.2。','同一筆大 Write 與小 Write 都可增加一筆命令，但流量不同。'),
 ('Power Cycles／Power On Hours／Unsafe Shutdowns／Busy Time／Thermal counters','各計數有自己的單位與累計條件，時間欄位不能全部當秒數。','Controller Busy Time 以分鐘、Power On Hours 以小時呈現，直接比較原始數字沒有意義。'),
 ('AFI.CAFS／NAFS／FRS1–FRS7','分清目前啟用 slot、下次啟用 slot 與各 slot 的 revision；revision 是 ASCII 字串。','slot 2 已保存新版且 NAFS=2，不等於 CAFS 已經變成 2。'),
 ('Changed Attached Namespace List','回報變動的 NSID；特殊全 FFFFFFFFh 值表示須依規則重新取得完整資訊。','不能把 changed 清單當成所有 active namespaces 的完整清單。'),
 ('ACS／IOCS／CSUPP／LBCC／NCC／NIC／CCC','先選 Admin 或 I/O 表，再看支援及可能改變的內容／能力；每項有獨立含義。','Admin opcode 2 在 byte 8；I/O opcode 2 在 byte 1032。NCC 提醒之後重新確認 namespace 能力。'),
 ('CSE／CSER／CSP','CSER 有有效且主機支援的值時按其優先規則判讀，CSE 描述相應提交與執行限制；CSP=0 是未回報範圍。','支援某命令不代表可與任何其他 namespace 命令並行。'),
 ('FIS／FSUPP／UDCC／NCC／NIC／CCC／FSP','LID 12h 每筆以 FID 索引；FSUPP 表支援，其餘 bits 區分 user data、namespace 能力、inventory 與 controller 能力變動。FSP 非零時只選一個範圍，0 是未回報。','FID 07h 在 byte 28；不把 scope=0 解成沒有影響。'),
 ('MDCSV／MDCS.DCCS、DNCS、DSCS','版本為 0；三個 default status bits 各須配對相應支援能力。不支援時值為 0 且主機應忽略。','DNCS=0 不能單獨證明 namespace 配置曾被修改。'),
 ('Log command status','Invalid Log Page、Invalid Controller Identifier 與 I/O Command Set Not Supported 分別定位不同選擇錯誤。','LID 對但 LSI 指到無效 controller，不能簡化為該 Log 不存在。'))
fields([332,333,334,335,336,337],'identify-request','Identify 的結構選擇與目標選擇',
 '把主機的一句查詢拆成 CNS、CSI、NSID／CNTID／CNSSID，再確認 4096-byte 回覆用哪張表解讀。',
 ('DPTR／4096-byte buffer','Identify 結構大小固定；使用 PRP 時本節不允許把 DPTR 當 PRP List。','能放 4096 bytes 不等於地址與跨 page 配置一定符合要求。'),
 ('CNS／CNTID','CNS 決定結構；只有相應操作使用 CNTID，不使用時 host 清為 0。','CNS=02h 讀 active NSID list，不把 NSID 填成 CNTID。'),
 ('CSI／CNSSID','CSI 選命令集，CNSSID 是 CNS 專用識別碼。未使用欄位按該處規則處理。','NVM Command Set 的 CSI=00h；NVM Set ID 與 CSI 不同。'),
 ('UIDX','指定 UUID 選擇機制的索引，並非 namespace ID。本篇不展開排除的 UUID List。','標準格式的查詢不任意選一個非零 UIDX。'),
 ('CNS applicability／scope','依保留 CNS 列確認哪些選擇欄位有效；未使用回覆空間按規格清零。','4096 bytes 的尾端零值不自動構成更多有效 entries。'))
fields([338,339,340,341],'controller','把 Identify Controller 的長表分成能力群組',
 '同一個 4096-byte 結構包含多種獨立能力，依這份報告使用的命令分組閱讀；不展開專題與傳輸排除欄位。',
 ('VID／SSVID／SN／MN／FR／VER','裝置身分、型號、firmware revision 與規格版本是不同識別資料；FR 是 ASCII revision。','兩台同型號裝置仍有不同 SN；VER 也不是 firmware slot 編號。'),
 ('OACS／ONCS／LPA／OAES','分別查 Admin 能力、NVM 選用命令、Log 能力及事件能力；只看使用的位元。','支援 Compare 不保證也支援 Copy，LPA 的 offset 支援不保證所有 Log 都支援 index offset。'),
 ('ACL／AERL／ELPE','Abort、AER 與 Error Log entry 上限各自使用零起算編碼。','原值 3 分別代表該類資源 4 筆，不代表三種資源可互相共用。'),
 ('MDTS／memory page 基準／SQES／CQES','MDTS 非零時以最小 memory page 大小乘 2^MDTS 限制傳輸；SQES／CQES 以指數描述 entry 大小。','最小 page 4096 bytes、MDTS=5 → 128 KiB；這不是 128 個 LBA。'),
 ('NN／MNAN／CNTLID／NSETIDMAX／ENDGIDMAX','數量、identifier 上限與目前控制器識別不同；配合各清單確認實際存在的對象。','NN 非零不代表每個 1 到 NN 的 NSID 都 active。'),
 ('FRMW.NOFS／FFSRO／FAWR／SMUD／FWUG／MTFA／MPTFAWR','分別回答 slot 數、唯讀、無 reset 啟用、重疊偵測、片段粒度及時間限制。','FWUG 處理片段大小與對齊，不是 slot 容量；MTFA 與 MPTFAWR 的觀察時間不同。'),
 ('FNA.FNS／SENS／CES／FNVMBS','範圍、erase 能力與 broadcast 限制分別用在 Format 判斷。','FNVMBS=1 禁止 Format 使用 FFFFFFFFh；CES 則回答 crypto erase 支援。'),
 ('HMPRE／HMMIN／HMMINDS／HMMAXD／HMB capabilities','偏好量、最小量、描述子大小與數量限制是不同條件，單位按欄位定義換算。','主機提供足夠總 bytes，仍可能因單筆描述子太小而不符合要求。'),
 ('NPSS／PSD.MP、MPS／ENLAT／EXLAT／NOPS','NPSS 是零起算的電源狀態數；MP 配 MPS 得到功率，進入／退出延遲與能否處理 I/O 分開。','5 個狀態的 NPSS=4；狀態 4 不代表 4 W。'),
 ('RRT／RRL／RWT／RWL／IDLP、IPS／ACTP、APW、APS','relative 指標只能比較相對表現；idle／active power 配自己的倍率與工作負載條件。','RRL 的相對排名不能直接轉成 μs 延遲，APW 也不是 watts 數值。'),
 ('MTFA 等 time values／Time Scale','先確認數值欄位使用的單位或 scale，再換算時間。','不能把一個使用 100 ms 的欄位與另一個使用 μs 的原值直接比較。'),
 ('HCTMA／MNTMT／MXTMT／WCTEMP／CCTEMP／temperature sensors','熱管理能力、允許的管理範圍、警告／臨界條件及感測器資料各自使用。','TMT1／TMT2 不能超過對應允許範圍，也不能把 warning temperature 當成 PS 編號。'),
 ('IVMSR.VSRV、VSRS／VOLSS／PIT／PISL／PISV','感測器採樣間隔、量測倍率和供電輸入身分分開讀；僅用來解本篇保留的事件參數。','VSRS 算時間，VOLSS 算電壓；PISL 辨別供電輸入，不是量測數值。'))
fields([342,343,344,345,346,349,350,351,352,353,354,355,356,357,358],'identify-lists','識別描述子、資源清單與格式清單有不同形狀',
 '清單先找個數與起始 ID，描述子先找型別與長度；各入口回報不同對象，不能共用同一個 parser 假設。',
 ('NIDT／NIDL／NID','4-byte 描述子 header 後接 NIDL bytes 的 NID；NIDT 決定其型別，CSI 型別也有自己的長度。','16-byte NID 加 4-byte header，共占 20 bytes，下一筆從其後開始。'),
 ('NVMSETID／NUMENT／NSETID／ENDGID','CNS=04h 用起點選清單，NUMENT 指 entry 數；entry 把 NVM Set 連到 Endurance Group。','ID 是識別碼，不是配置容量；相鄰數值不代表相鄰媒體。'),
 ('R4KRT／OWS／TNVMSC／UNVMSC','典型讀取時間、最佳寫入 bytes、總容量與未配置容量各有自己的單位和含義。','效能提示不保證每次都達到該延遲，也不改變命令最大傳輸限制。'),
 ('CNS=08h 的 NSFEAT.VWCNP／NMIC／FPI／NSATTR／NSTAT／NVMSETID／ENDGID','VWCNP 表示該 namespace 沒有 volatile cache；NMIC 表共享能力；FPI 先確認支援再讀剩餘 Format 百分比；NSATTR 表目前保護狀態；NSTAT 分 I/O 影響與 ready。資源 ID 補歸屬，資料大小在 NVM 結構補充。','看到共通特性位元不能直接推出每個 LBA 有 4096 bytes。'),
 ('DID／NUMENT／TDC／UDC／MEGDC','Domain 清單起點、項目數、總量、未配置量及單一 group 配置上限分開讀。','MEGDC 不等於目前 UDC；兩者同是容量也不能互換。'),
 ('ENGGID／NEGIDS／Endurance Group IDs','CNS=19h 的起點與回覆數量界定有效 group identifiers。','NEGIDS=2 是兩個 group IDs，不是兩個 namespaces。'),
 ('IOCSC0…511／I/O Command Set Vector／IOCSCI','清單列命令集組合，vector 的位元表示包含哪些命令集，Feature 用索引選組合。','IOCSCI=2 指第 3 個 vector，NVMCS=1 才表示該 vector 包含 NVM。'),
 ('GENCTR／NUMENT／底層 NSID 與 CNTLID／IDX','底層對應清單先確認版本，再解 entry 的所在儲存對象、namespace 與 controller；IDX 是清單索引。','IDX=7 指第 8 個可回報項目；不是 byte offset 7。本篇不展開遠端傳輸識別格式。'),
 ('NV／NUUID／兩類 state format entries','支援的 NVMe 版本項目與廠商格式項目分別計數，不等於目前運行狀態。','NV=2 表示有兩個版本 entries；不在此進行 controller migration。'))
fields(list(range(456,463)),'security','協定選擇、資料方向與兩種長度',
 'Security 命令提供傳輸外層；回覆內容是否成功，還需要依所選安全協定判斷。',
 ('SECP／SPSP1／SPSP0','SECP 選 protocol，SPSP=(SPSP1<<8)|SPSP0；各協定定義相應子選項。','12h 與 34h 組成 1234h，而非兩個不同 protocols。'),
 ('NSSF','在 SECP=EAh 時按所選用途解讀；其他協定為 reserved。','不能在未知協定上沿用 RPMB target 的解讀方式。'),
 ('DPTR／AL／TL','Receive 的 AL 是接收配置長度，Send 的 TL 是輸出傳輸長度；採指定的安全協定長度規則。','256-byte 請求配 512-byte 回覆空間，不必讓 TL=AL。'),
 ('SECP=00h／EAh／結果資料','00h Receive 可獨立查支援協定；EAh 再按 SPSP 分用途，其他交易的配對由協定定義。','Receive 不一定對應緊接在前的某一筆 Send；需要讀協定結果狀態。'))
fields([463,464,465,466,467,468,469,470,471,472,473,474,475,476,477,478,479,480,482,483,494,495,536,554],'features','保留的共同 Feature：控制哪一個行為',
 '先看共同 FID／SV，再按功能分支讀欄位；同一個 CDW11 在不同 FID 下不是同一種值。',
 ('FID／SV／DPTR／UIDX','FID 選功能，SV 要求保存；資料結構與 UUID 選擇依該功能定義，不能推論全部支援。','SV=1 不可用於不支援保存的功能；與值能否變更是兩個問題。'),
 ('HPW／MPW／LPW／AB','權重採零起算數量，AB 以 2^AB 或特殊值表示一次仲裁最多服務的命令數。','weight=3 → 4；AB=3 → 8。適用於所選仲裁機制，並非每命令 priority。'),
 ('PS／WH／IIELL','狀態、工作負載提示與 Idle I/O Exit Latency Limit 分開；IIELL 單位為 100 μs。','IIELL=20 → 2 ms；PS=3 只是狀態索引。'),
 ('TMPSEL／THSEL／TMPTH／TMPTHH','選感測器、上／下門檻、Kelvin 門檻值與遲滯；恢復事件需要按照遲滯規則判斷。','溫度剛越過上限後小幅下降，不必然立刻發出恢復事件。'),
 ('WCE／FUA／Flush','WCE 控制 volatile cache；FUA 和 Flush 另建立資料提交條件。','完成通知的時間不等於一般 Write 已持久保存。'),
 ('NCQR／NSQR／NCQA／NSQA','請求與回覆皆是零起算數量；實際配置不得由請求值代替。','requested=3、allocated=1 → 要求 4，實得 2。'),
 ('Asynchronous Event Configuration','各位元選擇所支援事件是否可回報，不是事件歷史；只配置本篇保留的功能分支。','開啟溫度事件回報，不表示現在已經過溫。'),
 ('APSTE／ITPT／ITPS','啟用 APST 後，以目前狀態對應的 entry 選 idle 超過 ITPT 時要進入的非 operational state。','ITPT=2000 ms、ITPS=3 → entry 低 Dword 0007D018h；有 I/O 時按規則回到先前 operational 狀態。'),
 ('APSTE／NOPPME／互動表','APST 控制自動狀態轉移，NOPPME 控制非 operational 狀態中的背景活動電力行為。','兩個 bit 的四種組合不是四個 Power State IDs。'),
 ('TSTMP／TSTMPO／SYNC','TSTMP 用毫秒；Get 的來源及同步屬性説明計數來源與是否可能停止。','1000 是 1 秒；某些 SYNC 狀態下不能把時間差全當 drift。'),
 ('TMT1／TMT2／HCTMA／MNTMT／MXTMT','熱管理界線需符合支援能力及規格允許範圍，TMT1／TMT2 彼此也有關係。','給出一個很高的值不代表能要求控制器越過安全或支援範圍工作。'),
 ('IOCSCI／Get 回覆','Set 選支援的命令集組合；Get 回目前組合索引。','IOCSCI=1 不是 CSI=1，也不是 namespace 1。'),
 ('PBSLC','Software Progress Marker 的 pre-boot software load count 由主機設定，依規格回報。','不能把 PBSLC=3 畫成 3% 進度條。'),
 ('Feature Not Saveable／Not Changeable／Not Namespace Specific','錯誤分別表示保存、變更與指定 namespace 的使用方式有問題。','清 SV 只處理保存要求，不能改變功能的 scope 或不可變更條件。'))
fields([543,544],'interrupts','中斷聚合和單一 vector 的例外',
 'CQE 的寫入與中斷送達可以不同時；聚合設定影響通知次數及延遲，不改變完成項目的內容。',
 ('TIME／THR','TIME 用 100 μs 為單位，THR 是零起算 entry 門檻；任一欄為 0 時依本節停用聚合。','TIME=10、THR=7 分別是 1 ms 與 8 entries；THR=0 另有特殊意義。'),
 ('IV／CD／CQ.IEN','CD 停用指定 vector 的 coalescing，IEN 則在建立 CQ 時決定是否啟用中斷。','CD=1 不等於 IEN=0；主機仍可能收到不聚合的中斷。'))
fields(list(range(571,584)),'queues','佇列欄位與引用關係決定建立及刪除順序',
 'CQ 先存在，SQ 才能透過 CQID 引用；刪除時先拆 SQ 的引用。對數量、深度及記憶體各做一次檢查。',
 ('Number of Queues／QID／QSIZE','Feature 協商可建立數量，QID 指一條 I/O 佇列，QSIZE 指該條深度。QSIZE=0 被禁止。','4 條深度 64 的 SQ：數量編碼 3，各 QSIZE=63；不是 QSIZE=3。'),
 ('PRP1／PC／CAP.CQR','PC=1 用連續配置；PC=0 按清單配置規則，還需確認 controller 是否要求實體連續。','支援一般資料 PRP List 不自動表示可建立不連續 queue。'),
 ('CQ.IV／IEN','IV 選中斷 vector，IEN 決定這條 CQ 是否啟用中斷。','IEN=0 可輪詢 CQ；它不是停用 CQE 寫入。'),
 ('SQ.CQID／QPRIO／NVMSETID','SQ 引用已建立 CQ；priority 依仲裁模式使用，NVMSETID 補上資源關聯。','SQ 3 和 SQ 4 共用 CQ 2，兩者仍可有各自的 priority。'),
 ('Delete SQ QID／Delete CQ QID','先移除所有引用該 CQ 的 SQ，再刪 CQ；原命令完成與 memory lifetime 依相應條件確認。','CQ 暫時為空並不能取代「已無 SQ 引用」的條件。'),
 ('Invalid Queue Identifier／Queue Size／Completion Queue／Interrupt Vector','分開指出 ID、深度、引用或中斷選擇的問題。','目標 CQ 不存在時，不要以改小 SQ depth 代替建立該 CQ。'))


def lesson(figure):
    from scripts.nvme_figure_lessons import CATALOG
    n=int(figure['number'])
    if figure['source_id']=='NVME-BASE-2.4' and n in EXAMPLES:return EXAMPLES[n]
    if figure['source_id']=='NVME-NVM-CS-1.3' and n in NVM_EXAMPLES:return NVM_EXAMPLES[n]
    return CATALOG[figure['source_id']][n]


def guide(figure):
    n=int(figure['number'])
    return GUIDES.get(n) if figure['source_id']=='NVME-BASE-2.4' else NVM_GUIDES.get(n)


def nvm_fields(numbers,key,title,relation,*rows):
    g=dict(id='adminio-nvm-'+key,title=title,relation=relation,rows=list(rows))
    for n in numbers:NVM_GUIDES[n]=g


nvm_fields([31,43,49,59,66,76,80,89],'results','把完成 status 放回該命令的問題',
 '同一個狀態數字必須配合 SCT 與命令種類解讀；每張表說明該操作的特定失敗條件。',
 ('SCT／SC／命令 Opcode','先選命令與 status 類別，再到該表找原因，不能用一張表通解所有命令。','Compare Failure 指內容不同；Read 無法取回資料是不同問題。'),
 ('範圍／格式／能力／命令選項','命令可能因範圍無效、格式不相容或所要求的選項不可用而失敗；回到對應欄位檢查。','Fast Copy Not Possible 不等於所有 Copy 都不受支援。'),
 ('部分處理／回覆的命令專屬資訊','是否已處理部分範圍及其單位由該命令規定，不用一般的全有或全無假設取代。','Copy 的來源範圍與 Write Zeroes 的已處理資訊不能共用同一個解碼公式。'))
nvm_fields([90,110],'log-additions','事件分支與錯誤位置的 NVM 定義',
 '這兩張圖分別補 Base AER 與 Error Information，並沒有新增一種共同 Log 格式。',
 ('AER.AET／AEI／Notice','NVM Notice 值放在既有事件型別下解讀；其對應狀態流程若不在範圍內，僅辨識通知意義。','不能把事件的 AEI 數字當成某筆 Read 的 status。'),
 ('Error Entry bytes 23:16／LBA','在適用的錯誤情境下，回報發生錯誤的最低編號 LBA。','錯誤涉及 LBA 100 與 108 時，這個欄位取 100；不代表已列出所有錯誤位置。'),
 ('Data Units Read／Written 的 NVM 補充','當 logical block 大小不是 512 bytes，先把資料量轉成 512-byte units，再依 Base 的統計格式回報。','4096-byte data 對應 8 個 512-byte units；還需套用 Base 的千單位計數和進位規則。'))
nvm_fields([91],'format','PIL、PI 與 MSET 補上 NVM 的格式選擇',
 'Base 決定範圍與 Format Index，本表把其中的命令集專屬 bits 對回 metadata 與 PI 的配置。',
 ('PIL／PI','PI 選保護資訊類型或停用，PIL 指定 PI 在 metadata 的位置；須具備對應能力與空間。','metadata 不夠時，不能只填 PI 非零就使該格式合法。'),
 ('MSET／metadata 傳輸','MSET 分開選 metadata 以延伸 LBA 或單獨 buffer 傳輸，需和格式的支援能力相符。','每 block 4096+8 bytes 的 metadata 若分離，8 blocks 的 data 與 metadata 分別是 32768、64 bytes。'))
nvm_fields([94,95,96],'range-type','LBA Range Type 的個數、用途與範圍',
 '一筆 entry 描述一段既有 LBA 空間的用途；它不建立新的 namespace 或檔案系統。',
 ('Set CDW11.NUM／Get CQE.NUM','兩者都是描述子數減 1；Get 不使用請求中的 NUM，回覆 NUM 才表示有效筆數。','NUM=1 對應兩筆 entries；不能只提供第一筆的 buffer。'),
 ('Type／Attributes／SLBA／NLB／GUID','Type 表用途，Attributes 補覆寫與可見性，SLBA 指起點，NLB 為 block 數減 1，GUID 辨識用途實體。','Type 與 GUID 並不改變 LBADS，範圍大小仍要按目前 LBA 格式換算。'))
nvm_fields([98],'normal-atomicity','DN 控制正常條件的要求，不代替持久保存',
 'Write Atomicity Normal 與掉電原子性、FUA／Flush 分別回答不同問題。',
 ('DN／AWUN／NAWUN','依 DN 的定義決定正常操作下的原子性要求；單位選擇仍要依 namespace 能力。','正常原子單位有 8 blocks，不表示任意長度或跨邊界 Write 都保證整筆原子。'),
 ('AWUPF／NAWUPF／FUA／Flush','前兩者對應掉電條件，後兩者對應資料持久保存，不能用 DN 統一替代。','FUA 不會放大 atomic write unit，Flush 不會把已跨原子邊界的 Write 改成整筆原子。'))
nvm_fields([122,123,125,126,127,128,129,130,131],'identify','從指定 namespace 或格式取得一組一致的能力',
 '先用 CNS／CSI 與目標選擇回覆，再用同一個 Format Index 配對容量、LBA Format、延伸資料與命令限制。',
 ('CNS／CSI／NSID／FIDX／CNTID','各 CNS 定義哪個目標欄位有效；Format Index 查詢與已存在 namespace 的查詢不同。','FIDX=2 不是 NSID=2；需依該 CNS 的入口選擇。'),
 ('NSZE／NCAP／NUSE','分清可定址大小、可配置容量及已使用量，再按目前 data block 大小換算。','NSZE=1000、LBADS=12 → 可定址 data 容量 4000 KiB，不是 1000 KiB。'),
 ('NLBAF／FLBAS／LBAF／NULBAF','清單個數與當前格式索引各有編碼；沿同一索引讀基礎及適用的延伸項目。','FLBAS 選 index 2，不把其 data 大小與 index 3 的 PI 格式混用。'),
 ('LBADS／MS／RP','LBADS 是以 2 為底的資料 byte 大小指數，MS 是 metadata bytes，RP 是相對效能。','LBADS=0Ch、MS=8 → 4096+8 bytes；RP 不直接換成 IOPS。'),
 ('MC／DPC／DPS／PIC／PIF／QPIF／STS','metadata 傳輸能力、PI 能力、目前設定與延伸格式分開確認；STS 分配 tag bits。','有 PI 能力不代表目前已啟用；要按同一格式檢查 tag 寬度與位置。'),
 ('NSFEAT／DLFEAT／NUSE','特性與解除配置後行為需要一起讀；使用量不能定位哪些連續 LBA 已配置。','NUSE=600 不代表只有 LBA 0–599 有資料。'),
 ('AWUN／AWUPF／ACWU／namespace 對應欄位','正常、掉電與融合操作有各自上限；namespace 欄位是否取代 controller 值依能力判讀。','正常 8-block 保證不能直接推論掉電也有 8 blocks。'),
 ('NABSN／NABSPF／NABO','原子邊界大小與起點偏移需與整段 Write 一起判斷。','長度小於單位但跨到下一個邊界，仍可能沒有整筆原子保證。'),
 ('ONCS／VWC／NWPC 等命令集能力','逐一查使用命令的能力；volatile cache presence 與其 Flush 行為不是同一個 bit。','Copy 不能只因 Compare 受支援就直接使用。'),
 ('MSSRL／MCL／MSRC／Copy format capabilities','單一來源長度、總複製長度、來源描述子數和格式能力各自限制 Copy。','兩段都未超 MSSRL，總和仍可能超 MCL。'),
 ('VSL／WZSL／WUSL／WZDSL／DMRL／DMRSL／DMSL','各命令的限制依其欄位單位與 0 值規則解讀；DSM 三項分別限制範圍數、單段與總量。','DMRL=2 只處理 range numbers 小於 2 的相關屬性；不表示每段只能有 2 blocks。'),
 ('IOCS specific version／PIC／Extended LBA Format','命令集版本與能力支援需一起確認，再讀該格式中的保護資訊。','PIC.QPIFS=0 時，不能把不受支援的 QPIF 當成有效格式選項。'))
nvm_fields([132,133],'granularity','只讀粒度資料，分清對應關係與單位',
 '這裡保留的是 Identify 的 Namespace Granularity List；不加入 Namespace Management 的建立或附加流程。',
 ('NGA.GDM／ND／NGD','GDM 決定 Format Index 如何對應描述子，ND 是描述子數減 1，NGD 是各筆描述子。','ND=1 表示兩筆，但格式 1 使用哪一筆仍需先看 GDM。'),
 ('NSG／NCG','兩者以 bytes 表示大小和容量建議粒度；與 LBA 數比較前先按相應格式換算。','250×4096 bytes=1000 KiB，與 1 MiB 粒度不同；不要把效率提示提高為所有命令的硬性拒絕條件。'))
nvm_fields([192,193],'format-list','格式清單的分組、個數與查詢入口',
 '兩張圖一起回答：有多少格式、需要的格式屬哪一群、用哪個 CNS 取得它自己的能力。',
 ('NLBAF／NULBAF／Format Index','實際共用格式數為 NLBAF+1，非共用格式數為 NULBAF；索引須小於兩群實際個數總和。','NLBAF=2、NULBAF=2 → 共 5 個；最大有效 index=4。'),
 ('CNS 00h／05h／08h 與 09h／0Ah','前三者只涉及共用能力群；後兩者可查兩群，以指定 Format Index 取得需要的結構。','index 3 屬非共用群時，選 09h／0Ah；不要以 NSID=FFFFFFFFh 的共用資料代替。'),
 ('LBADS／格式目前可用性','支援但目前不可用的格式以 LBADS=0h 表示；先確認有效，才以 2 的次方計算大小。','LBADS=0Ch 可表示 4096 bytes；不可把此處 LBADS=0h 解成可用的 1 byte。'),
 ('LBAFEE／最大格式數','主機未啟用格式延伸時至多 16 個，啟用時至多 64 個；本篇只交代引用前提。','索引在 0–63 之內仍不充分，還必須小於該裝置實際格式總數。'))

from scripts.nvme_admin_io_figure_revision import apply
apply(EXAMPLES, GUIDES, NVM_EXAMPLES, NVM_GUIDES)
