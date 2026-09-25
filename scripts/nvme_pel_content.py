"""Persistent Event Log: independent beginner course and paired overview claims."""
from scripts.nvme_report_extension import bi

REPORT_ID='base-persistent-event-log'

def claim(zh,en,section,pages,background=False,nvm=False):
    return dict(text=bi(zh,en),section=section,pages=pages,background=background,
        source_id='NVME-NVM-CS-1.3' if nvm else 'NVME-BASE-2.4',
        scope_entry_id='PEL-'+('NVM' if nvm else 'BASE')+('-PREREQUISITES' if background else '-INCLUDE'))

UNITS=[
dict(key='purpose',title=bi('先分清事件歷史、目前狀態與完整性','Distinguish history, current state and completeness'),claims=[
 claim('Persistent Event Log（PEL，LID 0Dh）保存 NVM subsystem 的重要事件，跨 power cycle 與 reset 保留。它不是每筆 I/O 的流水帳，也不是永遠不會遺失的完整歷史：容量、同類事件數量、頻率抑制與淘汰策略由廠商決定，Sanitize 也可能移除或修改紀錄。',
 'Persistent Event Log (PEL, LID 0Dh) retains significant NVM subsystem events across power cycles and resets. It is not a trace of every I/O or a guaranteed complete history: vendors define capacity, per-type limits, frequency suppression and eviction, and Sanitize may remove or modify records.','5.2.13.1.14','270-271'),
 claim('先用 Identify Controller 的 LPA.PES 確認支援，PELS 以 64 KiB 為單位回報最大空間；本次實際回報長度則是 PEL header 的 TLL。SEB 宣告事件種類支援，TNEV 計算這次回報有多少筆，兩者不能互相代替。',
 'LPA.PES advertises PEL support and PELS reports maximum space in 64 KiB units. TLL is the actual reported length. SEB advertises supported event types, whereas TNEV counts records in this report.','5.2.14.2.1; 5.2.13.1.14','273-275,381,390',True),
],steps=[
 ('先想一個實際要回答的問題','裝置重設後恢復服務，你想知道之前是否更新過韌體、是否發生電源中斷、是否重新建立過 namespace。現在的設定只能告訴你「目前怎樣」，PEL 則留下事件當時的資訊。這種差異就像目前的銀行餘額與交易紀錄：兩者可以互相說明，卻不是同一份資料。這個比喻只幫助理解用途，不表示 PEL 具有帳本的完整性保證。'),
 ('先看支援，再看這份紀錄實際有什麼','可以把讀取分成三個問題：裝置能不能提供 PEL；它支援記錄哪些事件；這次實際回傳哪些事件。PES、SEB、TNEV 分別回答它們。例如裝置支援 Thermal Excursion，這次卻沒有溫度事件，可能只是沒有觸發，不能推論裝置不支援。反過來，紀錄裡沒有某件事，也不能直接斷言它從未發生。'),
 ('持久不代表無限，也不代表每次斷電都零遺失','規格要求跨重設與電源循環保留，但對突發斷電造成的事件遺失，使用的是「設計應盡量降低」的要求。容量或同類事件上限滿了，刪除哪些紀錄由廠商決定，不能自動假設一定刪最舊。事件太密集時也可以按廠商門檻抑制重複事件；因此計算 log 裡某類事件筆數，不等於可靠的終生發生次數。'),
 ('如何安排閱讀順序','先學會取得同一份資料，再學外框與長度。接著依問題讀事件：健康與溫度、時間與重設、namespace 與格式、清除作業、硬體、設定及擴充。範圍內每張規格表都在後面的圖表教學區有重點、案例與欄位說明；需要細節時可以直接從本單元連過去，不必把所有欄位一次背完。'),
],example=bi('說明性範例：PELS=4 表示最大 256 KiB；本次 TLL=4096、TNEV=9，則只回報 4 KiB、9 筆事件。不能拿最大空間當本次長度，也不能拿 9 當事件種類數。',
 'Illustration: PELS=4 means a maximum of 256 KiB. TLL=4096 and TNEV=9 describe a 4 KiB report containing nine records, not nine event types.'),reading=bi('Figure 233 看實際回報；Figure 236 看事件分類；Figure 338 只取相關能力。','Use Figures 233/236 for report contents and types, and the relevant capabilities in Figure 338.')),

dict(key='context',title=bi('用 reporting context 取得同一份紀錄','Use a reporting context to retrieve one consistent report'),claims=[
 claim('Reporting context 固定本次回報的事件集合；之後新增的事件仍須記錄，但不加入既有 context。ACT=1 建立並讀取，已有 context 時失敗；ACT=0 讀取既有 context，沒有時失敗；ACT=2 釋放，沒有也不是錯誤。受支援的 ACT=3 建立或沿用 context，一律回傳 offset 0 的 512-byte header。',
 'A reporting context fixes the event set for this report; later events are still logged but excluded from that context. ACT=1 establishes and reads, failing if a context exists; ACT=0 reads an existing context, failing if absent; ACT=2 releases and tolerates absence. Supported ACT=3 establishes or reuses a context and always returns the 512-byte header at offset zero.','5.2.13.1.14','271-272,277'),
 claim('ACT=3 回覆的 RCE 表示處理命令前是否已有 context；RCE=0 不表示建立失敗。分段讀取應先記下 GNUM，完成後重讀比較；不同表示資料可能來自不同 context，應重新取得。GNUM 只有建立新 context 且內容與上次不同才遞增，16-bit 值會回捲。',
 'For ACT=3, RCE reports whether a context already existed when the command was processed; zero is not creation failure. For multipart reads, record GNUM first and compare it after retrieval; a mismatch indicates potentially invalid data and calls for rereading. GNUM increments when a newly established context differs from the previous contents and wraps as a 16-bit value.','5.2.13.1.14','271-274'),
 claim('Get Log Page 的 NUMD 是從 0 計數的 Dword 長度；512 bytes 對應 NUMD=127。PEL 是 subsystem 範圍，NSID 使用 0 或 FFFFFFFFh。一般以 OT=0 使用 byte offset；ACT=2 忽略長度與 offset，ACT=3 也忽略它們而固定回 512 bytes，因此 buffer 至少配置 512 bytes。',
 'Get Log Page NUMD is a zero-based Dword count, so 512 bytes corresponds to 127. PEL has subsystem scope and uses NSID zero or FFFFFFFFh. Normal OT=0 requests use byte offsets; ACT=2 ignores length/offset and ACT=3 overrides them with a fixed 512-byte transfer, requiring a buffer of at least that size.','5.2.13; 5.2.13.1.14','239-243,272',True),
],steps=[
 ('為什麼不能讀一塊就重新建立一次','一份 PEL 可能比單次傳輸大。假設先讀到 A、B，裝置此時新增 C；如果下一次又從另一份事件集合取資料，接起來就可能漏掉或重複某筆。Context 用來固定這一次要報告的集合與資料位置。它不停止裝置記錄新事件，只讓讀取者能分批完成同一份報告。'),
 ('選擇建立動作後，再用讀取動作接續','一般先確認沒有其他讀取者佔用或管理這份 context，再使用 ACT=1 建立，或使用支援的 ACT=3。後續分段用 ACT=0，加上各段的 offset 與長度。ACT=3 若回 RCE=1，是沿用既有 context，不能當成剛取得含最新事件的新快照；若要更新，應在讀取者之間協調後釋放，再建立。不要任意釋放別人正在使用的 context。'),
 ('讀取期間仍可能失去 context','規格建議保留 context，直到主機釋放、subsystem reset、controller level reset，或廠商規定足夠完成讀取的一段時間。不能因 ACT=1 成功就假設永遠存在。先讀 header 記下 GNUM 與 TLL，收齊資料後再讀 header，比對 GNUM；若變了，這次拼接的結果不應當作一致資料。'),
 ('讀完再釋放，而不是每一段釋放','ACT=2 只處理釋放，不回傳 log data，也不依 NUMD 或 offset 讀資料。主機完成一份報告後應釋放 context，讓下一次建立能包含新事件。釋放 context 與清除持久事件歷史是兩件事；前者結束這次讀取，不是一個刪除所有 PEL 事件的命令。'),
],example=bi('512-byte 建立讀取：ACT=1、LID=0Dh、NUMDL=127、RAE=0，CDW10=007F010Dh；ACT=3 對應 007F030Dh。假設先讀 GNUM=41，中途新增事件但 context 保留，最後仍為 41；下一次建立是否變成 42，取決於回報內容是否改變。',
 'For a 512-byte establish/read, ACT=1, LID=0Dh, NUMDL=127 and RAE=0 produce CDW10=007F010Dh; ACT=3 gives 007F030Dh. If the initial GNUM is 41 and the context survives, a later event does not alter that report’s GNUM. The next establishment increments to 42 only if its reported contents changed.'),reading=bi('Figures 232／235 分開教命令動作與支援宣告；233 的 RCI／GNUM 說明 context 狀態。','Figures 232/235 separate action and support; Figure 233 provides RCI/GNUM.')),

dict(key='layout',title=bi('從 header 走到每筆事件的邊界','Walk from the header to each event boundary'),claims=[
 claim('LHL 的計數不含前 20 bytes，因此 log header 大小是 LHL+20；EHL 不含事件前 3 bytes，因此事件 header 大小是 EHL+3。EL 已包含 VSIL 指出的廠商資料，事件總大小為 EHL+3+EL，真正 ED 大小為 EL−VSIL。LREV 描述外層格式，ET 與 ETR 決定事件內容的格式。',
 'The log header occupies LHL+20 bytes and an event header occupies EHL+3 bytes. EL already includes the VSIL vendor-information bytes: total record size is EHL+3+EL and ED size is EL−VSIL. LREV describes the outer format; ET and ETR select the payload format.','5.2.13.1.14','273-277'),
],steps=[
 ('先分清位置、長度和第幾筆','Offset 是離起點多少 bytes；index 是第幾筆。現在的 log header 佔 512 bytes，所以第一筆事件從 offset 512 開始，它的 index 是 0。第二筆從哪裡開始，必須把第一筆的實際總長度加上去。事件不是每筆固定 512 bytes，也不能用 index 乘固定常數當 offset。'),
 ('先看外框，再看內容','每筆事件先有共同 header：ET 告訴你是什麼事件，ETR 告訴你用哪一版內容，CNTLID 與 ETSTP 說明記錄者與時間。接著可能有 VSI，最後才是 ED。沒有 VSI 時 VSIL=0；沒有 ED 時也可能仍有一個有效事件，例如進入 Media Verification 的 ET=0Eh。不要把「沒有內容」當成「沒有事件」。'),
 ('用算例走一次，不背表格中的長算式','假設事件從 offset 512 開始，EHL=21、VSIL=4、EL=20。共同 header 為 24 bytes，VSI 在 536～539，ED 在 540～555，長 16 bytes；下一筆從 556 開始。EL 的 20 已是 4+16，再多加 VSIL 會錯跳到 560，把下一筆開頭跳掉。這就是原表把長度分開的理由。'),
 ('先確認邊界，再按版本解讀','整份事件區不得超出 TLL，每筆的 VSIL 不應大於 EL，前進後的 offset 也不得超過回報邊界。事件本身長度未保證是 4 的倍數；傳輸請求的 Dword 對齊是另一層限制，可以讀取包含部分事件的資料塊後再組合。遇到尚未支援的 ET 或 ETR，先保留原始 bytes、依外框長度走到下一筆，不拿相似事件格式硬解。'),
],example=bi('EHL=21、VSIL=4、EL=20、起點512：header=24、ED=16、總長44、下一筆556。另一筆若 EL=22、VSIL=0，總長46；不能為了 Dword 對齊把它擅自改成48。',
 'With EHL=21, VSIL=4, EL=20 and start 512: header=24, ED=16, total=44, next=556. A record with EL=22 and VSIL=0 totals 46 bytes; do not round it up to 48 merely for Dword alignment.'),reading=bi('Figures 233／234 的 bytes 欄是相對位置；Figure 236 的 ET 是代碼，兩者不是同一種數字。','Figures 233/234 show relative positions; Figure 236 lists type codes.')),

dict(key='health',title=bi('健康、Telemetry 與溫度各留下什麼證據','Interpret health snapshots, telemetry references and temperature events'),claims=[
 claim('ET=01h 保存 512-byte SMART 快照，記錄間隔不得超過 24 power-on hours；ET=0Ch 可保存新建 Telemetry 的前 512 bytes，並不包含完整診斷資料。ET=0Dh 記錄溫度門檻事件，其 OTMP 是相對門檻的 Kelvin 差值，不是絕對溫度。這些都是事件當時的資料。',
 'ET=01h stores a 512-byte SMART snapshot at intervals no greater than 24 power-on hours. ET=0Ch may record the first 512 bytes of newly created telemetry, not its complete diagnostic data. ET=0Dh records thermal-threshold events; OTMP is a Kelvin difference from a threshold, not an absolute temperature. These are historical observations.','5.2.13.1.14.2.1; 5.2.13.1.14.2.12; 5.2.13.1.14.2.13','278,290-292'),
 claim('SMART 的 Data Units Read／Written 使用 1000×512-byte 單位、向上取整；Composite Temperature 使用 Kelvin。Telemetry 的 Last Block 是由 block 1 開始之資料區的最後編號，各資料區是由同一起點擴大的集合，不是要相加的四段。',
 'SMART Data Units Read/Written use rounded-up units of 1000×512 bytes; Composite Temperature uses Kelvin. Telemetry Last Block is the final block number of an area beginning at block 1. The areas expand from the same start rather than forming four disjoint segments to add together.','5.2.13.1.3; 5.2.13.1.8; 5.2.13.1.9','247-251,260-263',True),
],steps=[
 ('快照先問拍攝時間','一份 PEL 裡的 SMART 是當時拍下的 512-byte 健康資料。今天讀到去年快照的 POH、Data Units 或警告，不能把它當成今天的數值。沒有虛擬化時各控制器都要按規定間隔記錄；有虛擬化時是各 primary controller。24 hours 指 power-on hours，裝置關機幾天不會因此把它變成每個日曆日一筆。'),
 ('單位決定比較是否有意義','SMART 累計量要連同單位閱讀：忙碌時間用分鐘、電源時間用小時、熱管理累積時間用秒，溫度用 Kelvin。Data Units=3 不是 3 bytes，也不是精確 3000 個 512-byte 單位，而是向上取整後的結果；原計數落在 2001～3000 個單位。零值有些表示未回報，不能把所有零都解成從未發生。'),
 ('Telemetry 事件是一張索引卡','ET=0Ch 留下 Telemetry header：可辨認廠商、原因、作用範圍、generation number 和各資料區邊界。若 header 說 Data Area 3 結束於 block 9，意思是原始診斷資料區曾涵蓋 blocks 1～9；這 9 個 blocks 並沒有跟著收入此 PEL 事件。歷史 header 也不保證現在裝置還留著同一份原始資料。'),
 ('溫度差值要搭配觸發門檻','若 THRESH=1、已知 WCTEMP=343 K、OTMP=5，這是往上跨過警告門檻的事件，可理解為約 348 K 的當時溫度。THRESH=88h 是回到正常區間，89h 是停止某種熱管理動作，兩者又是不同事件。遇到廠商門檻或不知門檻值時，只靠 OTMP 不能還原絕對溫度；Kelvin 差 5 與 Celsius 差 5 相同，但絕對值需要減 273.15。'),
],example=bi('PEL 內有 ET01 的 CTEMP=300 K，稍後又有 ET0D：THRESH=1、OTMP=5，並已知 WCTEMP=343 K。前者是較早快照的約26.85°C；後者是跨門檻事件的約74.85°C。兩筆不同時間的觀察不矛盾。',
 'An ET01 snapshot has CTEMP=300 K; a later ET0D record has THRESH=1 and OTMP=5 with known WCTEMP=343 K. The earlier snapshot is about 26.85°C and the threshold event about 74.85°C. Observations at different times need not match.'),reading=bi('Figures 237／254／255 分別對應完整健康快照、Telemetry header 與溫差事件。','Figures 237/254/255 distinguish a health snapshot, telemetry header and threshold event.')),

dict(key='time',title=bi('韌體、時間戳與重設要連著讀','Connect firmware, timestamps and reset records'),claims=[
 claim('Firmware Commit 完成時記錄 ET02，不代表新韌體已啟用；ET04 在 power-on 或 reset 完成後，提供成為有效版本的 FREV 與各控制器資訊。ET03 保存時間戳變更前的 PTSTP，而共同 header 的 ETSTP 是變更後的時間。時間戳可能由重設起算、由主機設定，也可能有停止計時區間。',
 'ET02 is logged when Firmware Commit completes and does not by itself prove activation. ET04 records completed power-on/reset with the effective FREV and per-controller information. ET03 stores the previous timestamp in PTSTP and the new timestamp in the event header ETSTP. Timestamps may originate at reset, be host-set, or include periods when counting stopped.','5.2.13.1.14.2.2; 5.2.13.1.14.2.3; 5.2.13.1.14.2.4; 5.2.30.1.8','278-280,496-497',True),
],steps=[
 ('有紀錄不等於操作成功，更不等於已啟用','ET02 包含舊版本 OFR、要求的新版本 NFR、Commit Action、slot，以及 Firmware Commit 的 SCT／SC。它是在命令完成時記錄，完成可能帶有錯誤，或表示還需要某種 reset 才能啟用。先讀命令結果，再看後續 ET04 的 FREV 與 FA，才能把「提出更新」與「重設後真正生效」接起來。'),
 ('一筆重設事件可能涵蓋多個控制器','ET04 先有 8-byte FREV，後面不是固定一份資訊，而是多個 36-byte 描述子。每份有 CNTLID、FA、當時是否進行 Format、控制器電源循環次數、累積通電毫秒與事件時間。外層 CNTLID 指這筆事件的記錄者，內層各 CNTLID 才指出每份描述子對應誰；不能以為整筆只談外層那個控制器。'),
 ('時間軸為什麼可能向後跳','Timestamp 是 48-bit 毫秒數加上屬性。Origin=0 是從控制器重設後的起點計時；Origin=1 表示主機設過時間，仍不能直接保證它是真實世界的 UTC。主機可能調整時鐘，新的數字比舊的更小；ET03 的 PTSTP 與 MSR 正是讓你辨認這種變更。SYNC=1 還表示計時可能曾暫停。'),
 ('事件順序也要尊重來源邊界','規格建議較新的事件放在較小 offset，但具體排序方式由廠商決定。不同控制器可能有不同時間基準，時間也可能被改過；因此不要只用 ETSTP 大小重新排序後，就宣稱得到全 subsystem 嚴格一致的因果順序。先保留原始順序，再用 reset、時間變更與事件內容說明能建立的關係。'),
],example=bi('ET02 的 NFR=版本B，只能說曾要求提交B；後續 ET04 的 FREV=版本A、FA=2 表示該次啟用失敗，重設後有效版本仍是A。不能只在全文搜尋到B就報告「更新成功」。',
 'An ET02 NFR of version B records an attempted commit. A later ET04 with FREV=A and FA=2 reports failed activation and A still effective after reset; the mere occurrence of B in the log is not success.'),reading=bi('Figures 238～241 與 Timestamp Figure480 共用時間基準教學。','Read Figures 238–241 together with Timestamp Figure 480.')),

dict(key='namespace',title=bi('把 namespace 變更接到 NVM 格式欄位','Connect namespace changes to NVM format fields'),claims=[
 claim('ET06 記錄成功的 Namespace Management 命令。Base Figure247 定義整體內容與欄位來源；NVM Figure112 補定 byte32 的 FLBAS 與 byte33 的 DPS：建立時取主機指定值，刪除單一 namespace 時取該 namespace 的 Identify 值，刪除全部時這兩個欄位保留。',
 'ET06 records successful Namespace Management commands. Base Figure247 defines the payload and field origins; NVM Figure112 specializes byte32 FLBAS and byte33 DPS: host-specified values for creation, Identify values for single-namespace deletion, and reserved fields for deletion of all namespaces.','4.1.4.4','76-77',False,True),
 claim('ET07 在 Format 參數驗證後、修改媒體前記錄；ET08 在已修改媒體的 Format 完成時記錄，完成可以失敗。FNVMS 的 INCPLTF=1 表示已修改部分或全部資料卻未成功，也要求 FNVME=1。SFPI 是曾回報的最小剩餘百分比；全體 namespace 的 Format 則為0，不能單憑0判成功。',
 'ET07 is recorded after Format parameter validation and before media modification; ET08 records completion of a Format that modified media, which may fail. INCPLTF=1 means some or all data was modified without successful completion and requires FNVME=1. SFPI is the smallest reported remaining percentage; an all-namespace Format reports zero, so zero alone is not success.','5.2.13.1.14.2.6; 5.2.13.1.14.2.7; 5.2.13.1.14.2.8','284-287'),
 claim('FLBAS 的 format index 由 bits6:5 與 bits3:0 組合，bit4 選 metadata 傳輸方式；DPS bits2:0 選保護資訊類型。NVM 1.3 的 DPS.PIP 必須為0，把啟用的保護資訊放在 metadata 尾端。Format index 只是格式表的編號，本身不是 byte 大小。',
 'FLBAS combines bits6:5 and bits3:0 into a format index, with bit4 selecting metadata transfer. DPS bits2:0 select the protection-information type. NVM 1.3 requires DPS.PIP=0, placing enabled protection information at the end of metadata. A format index names a format-table entry, not a byte size.','4.1.5.1; 4.1.6','85-87,112-113',True,True),
],steps=[
 ('先看做了什麼，再決定其餘欄位能不能讀','ET06 的 NMCDW10 保留 Namespace Management 的命令參數，其中 SEL 區分 Create、Delete、Restore。建立成功時 NSID 是分配到的新識別值；刪除一份時是被刪除的識別值；刪除全部是 FFFFFFFFh。當事件表示刪除全部，NSZE、NCAP、FLBAS、DPS 等單一 namespace 欄位不具有可用內容，不能把裡面的0說成「刪除了一個大小0的namespace」。'),
 ('Base 負責外框，NVM 補上兩個洞','Base 表先告訴你 byte32、33 是由 command set 定義的欄位。NVM Figure112 才告訴你怎麼取得 FLBAS 與 DPS。這兩個 bytes 在事件裡的位置固定，但資料原本在 NVM Identify 或 Create 資料結構的 byte26、29。複製進事件後位置改了；如果仍到事件的 byte26 找 FLBAS，讀到的是 NCAP 的一部分。'),
 ('用數值分清容量與格式','NSZE 與 NCAP 用 logical blocks 計算，不是 bytes。假設 NSZE=1000、NCAP=800，已知所選格式為4096 bytes資料加8 bytes metadata：可定址範圍是LBA0～999，可配置上限是800 blocks。若 FLBAS bit4=1，單一延伸區塊傳輸資料加metadata共4104 bytes；bit4=0時metadata另放buffer。範例的格式內容是另行給定，不是從format index的數字猜來。'),
 ('建立、格式化與格式化結果分開','Namespace Management 是儲存物件的建立或刪除；Format 則是媒體格式操作。ET07 留下開始時的 NSID、FNA、CDW10；ET08 留下結果與進度。若 FNA 表示一次影響所有 namespace，命令指定其中一個 NSID 也不能把它理解成只改一份。看到開始事件，還不足以證明完成；看到完成事件，也還要檢查 FNVMS。'),
],example=bi('NVM 事件 byte32=12h、byte33=01h：format index=2、metadata隨延伸LBA傳輸、PI Type1位於metadata尾端；前提是這是Create或單一Delete。若同一數值出現在Delete All保留欄位，不能做這些推論。',
 'For an NVM event, byte32=12h and byte33=01h mean format index 2, extended-LBA metadata and Type1 protection at the metadata end, provided the operation is Create or single Delete. Identical bytes in reserved Delete All fields establish none of those facts.'),reading=bi('Base247 和 NVM112 應放一起讀；248／249 則是一個格式化操作的起點與結果。','Pair Base247 with NVM112; Figures248/249 show a Format operation’s start and outcome.')),

dict(key='sanitize',title=bi('把清除開始、完成與媒體驗證分開','Separate sanitize start, completion and media verification'),claims=[
 claim('ET09 記錄 sanitize 進入處理狀態，ET0A 記錄進入 Idle 或失敗狀態；成功的命令完成不等於長時間清除已完成。ET0E 記錄進入 Media Verification，ETR=1、EL=0，沒有 ED。Start／Completion 的 NSID 指定清除對象，FFFFFFFFh 表示整個 subsystem。',
 'ET09 records entry into sanitize processing; ET0A records entry into Idle or a failure state. Successful command completion is not completion of the long-running operation. ET0E marks entry into Media Verification with ETR=1 and EL=0, carrying no ED. Start/completion NSID identifies the target; FFFFFFFFh means the subsystem.','5.2.13.1.14.2.9; 5.2.13.1.14.2.10; 5.2.13.1.14.2.14','287-288,292'),
 claim('SPROG 的進度刻度是65536；FFFFh也可能出現在 Media Verification 或非處理狀態，所以要同時讀SSTAT.SOS。SOS=3表示失敗，1表示成功完成，4表示成功但發生了未要求的deallocation，2涵蓋處理中、驗證與驗證後deallocation。',
 'SPROG uses a scale of 65536. FFFFh also appears during Media Verification or outside processing, so interpret SSTAT.SOS alongside it: 3 is failure, 1 successful completion, 4 success with unexpected deallocation, and 2 covers processing, verification and post-verification deallocation.','5.2.13.1.38','340-342',True),
],steps=[
 ('清除操作比命令生命週期長','主機送出 Sanitize，控制器可以先成功完成這個啟動命令，再花較長時間處理媒體。PEL 的開始與完成事件是記錄清除操作走到哪個狀態，不是把同一個 CQE 重複保存兩次。開始事件保存當時的 SANICAP 與啟動參數，幫你辨認使用的是 block erase、overwrite 或 crypto erase。'),
 ('相同事件類型仍要比對清除對象','新格式的 ET09、ET0A 都有 NSID。若一筆指向namespace7，另一筆指向FFFFFFFFh，不能只因時間相近就宣稱是一對。兩種事件沒有提供通用的作業流水號；必須結合對象、時間與記錄上下文判讀。歷史可能有淘汰或抑制，更不能要求每個start一定都能在手上這份資料找到completion。'),
 ('完成事件的名字不是成功保證','ET0A 包含 SPROG、SSTAT、CINFO 和 NSID。SSTAT 裡的 SOS 才告訴你是成功、失敗還是其他狀態。CINFO 是廠商補充原因，沒有通用碼表；它不能取代 SOS。尤其 SPROG=FFFFh 在多種情況都可能出現，不能直接換算成「已安全清完100%」。'),
 ('進入驗證是一個節點，不是另一份進度表','ET0E 的事件總長仍包含共同 header，但沒有 ED，因此也沒有自己的 NSID、SPROG 或 SSTAT 可讀。這個事件只證明進入了 Media Verification。若後續驗證被取消或清除失敗，仍需依其他事件與狀態辨認，不能替空的 ED 補想像中的欄位。'),
],example=bi('ET0A 回報 SPROG=FFFFh、SSTAT.SOS=3：結果是失敗，不是成功100%。若只看到 ET0E，能說已進入驗證，但不能說清除已完成，也不能從不存在的ED讀出NSID。',
 'An ET0A with SPROG=FFFFh and SSTAT.SOS=3 reports failure, not 100% success. ET0E alone establishes entry into verification, not sanitize completion or an NSID from its nonexistent ED.'),reading=bi('Figures250／251連到Sanitize參數與狀態；ET0E本身沒有另畫內容表。','Figures250/251 link to sanitize parameters/status; ET0E has no payload table.')),

dict(key='hardware',title=bi('先選硬體錯誤代碼，再選附加資料格式','Select the hardware-error code before its additional format'),claims=[
 claim('ET05 的 NSHEEC 選擇硬體錯誤種類，AHEI 的格式與長度跟著種類改變。01h～03h 是 PCIe 錯誤資訊，08h 是非預期斷電資訊，0Bh 是控制器就緒逾時資訊；某些種類沒有 AHEI。硬體事件子類的支援由廠商決定，不能把固定的一張表套到所有 ET05。',
 'In ET05, NSHEEC selects the hardware-error kind and thereby the AHEI layout and length. Codes01h–03h carry PCIe error information, 08h unexpected-power-loss information, and 0Bh controller-ready timeout information; some kinds have no AHEI. Vendors select supported subtypes, so one fixed layout cannot decode every ET05.','5.2.13.1.14.2.5','280-284'),
],steps=[
 ('把兩層種類分開','外層 ET=05h 只表示是 hardware error。進入 ED 後還要讀 NSHEEC，才能決定後面 AHEI 是哪一種資料。這類結構像一封信的信封標「設備事件」，內頁再標「電源」或「連線」；後面的欄位要按內頁種類讀，不能因共同開頭相同就當成每封都裝同一種表。'),
 ('警告、鏈路事件與命令錯誤有不同證據','Critical Warning 類型保留警告位元；Endurance Group 警告還帶 Group ID；media/data integrity 類型則帶完整 CQE。PCIe link status change 的附加資料是 Link Status 暫存器值，並不是PCIe錯誤類型那份80-byte AER結構。Link not active 和CSTS.CFS的類型沒有額外資料，沒有AHEI本身不是紀錄損壞。'),
 ('電源事件不能只看「不正常」三個字','Unexpected Power Loss 附加資訊有累計UPL與一個UPLOA位元。UPLOA描述一個很特定的情境：已在shutdown處理或完成狀態，卻因允許忽略shutdown的帶外管理操作讓媒體仍需運作，此時主電源掉落。UPLOA=0只表示不符合這個特殊標記，不表示這次掉電其實是正常關機。'),
 ('就緒逾時要連同當時模式','控制器啟用後的等待限制跟 ready mode 有關。事件內的 CRIME 保存當時模式，CNR、ACMNR、NNR 分別指出控制器、Admin命令所需媒體、或附接namespace未及時就緒。這些位元可同時提供線索，不是四選一的錯誤等級；有一位為0也不表示其他範圍已正常。'),
],example=bi('同是ET05：NSHEEC=08h時AHEI開頭是16-byte UPL計數；NSHEEC=0Bh時AHEI開頭則是狀態位元。若不先看NSHEEC，就會把計數的低byte錯讀成CRIME/CNR。',
 'Within ET05, NSHEEC=08h begins AHEI with a 16-byte UPL counter, whereas 0Bh begins with status bits. Skipping NSHEEC could misread a counter byte as CRIME/CNR.'),reading=bi('Figure242是共同外框，243選子類，244～246是三種不同的附加資料。','Figure242 is the envelope, 243 selects the subtype, and 244–246 define different additional data.')),

dict(key='features',title=bi('設定事件如何保留命令與資料','How feature events preserve commands and data'),claims=[
 claim('ET0B 在成功 Set Features、值確實改變且支援記錄時必須記錄；成功但同值時可記錄。Figure252 的 O／P／NR 是各 Feature 在指定控制器類型上的記錄要求，不是該 Feature 的支援能力。SFEL 決定連續 CDW、可選資料 buffer 與可選 CQE DW0 的位置。',
 'ET0B must be logged for successful value-changing Set Features when logging is supported; successful same-value requests may be logged. Figure252 O/P/NR describes logging requirements for a feature/controller type, not feature support. SFEL locates consecutive command Dwords, an optional data buffer and optional completion DW0.','5.2.13.1.14.2.11','288-290'),
 claim('ET0F 是 Configurable Device Personality 的專屬事件，描述設定變更、freeze／unfreeze或安全條件造成的freeze。CDPRFS記錄要求的freeze狀態，CDPCE表示變更錯誤；不能因requested bit=1就宣稱已成功freeze。Manufacturing Default請求只記一筆，不逐personality拆成多筆。',
 'ET0F is the dedicated Configurable Device Personality event for changes, freeze/unfreeze and security-triggered freezing. CDPRFS records the requested freeze state and CDPCE a change error; a requested bit alone does not prove successful freezing. A Manufacturing Default request produces one event rather than one per personality.','5.2.13.1.14.2.15','292-293'),
],steps=[
 ('先辨認記錄政策，不把O當成功','O是可選記錄，P是禁止記錄，NR是不建議記錄。選對I/O或Admin控制器欄位後再看Feature列。Timestamp在這張Set Feature表是P，因為有自己的ET03；因此「沒有ET0B的Timestamp紀錄」不能說主機從未改過時鐘。某Feature為O也不代表控制器一定會替它留下事件。'),
 ('命令Dword數與buffer bytes分開算','SFEL的DWC直接計算幾個Dwords，1～6有效，沒有NUMD那種加1。從CDW10開始连續保存，直到最高的非保留命令Dword，中間即使某個Dword是保留也包含在內。MBC則以bytes計算後面的資料buffer；LCCDW0只有0或1，決定最後是否再有4-byte完成值。三種單位不能混算。'),
 ('完成DW0不是整份完成項目','這個可選欄位只保存Set Features的CQE DW0，不是16-byte CQE，也不是其中的Status欄。先用SFEL找到它，再按那個Feature的回覆意義讀；若LCCDW0=0，這個位置根本沒有欄位，不能把下一笔事件的頭當成完成值。'),
 ('Personality事件不是Set事件的改名','ET0F把請求狀態PS、PERID與personality專屬資料PED分開。PED從byte12開始，內容由PERID指定的personality定義；共同格式本身沒有提供一套適用所有personality的欄位。讀者至少能確定請求freeze與否、有沒有change error、針對哪個personality，以及保留的原始專屬資料長度。'),
],example=bi('格式計算例，未指定某個FID：DWC=3、MBC=8、LCCDW0=1得到SFEL=0008000Bh；ED長度=4+3×4+8+4=28 bytes。CDW10～12在bytes4～15，buffer在16～23，CQE DW0在24～27。',
 'Layout-only example, not a specific FID: DWC=3, MBC=8 and LCCDW0=1 give SFEL=0008000Bh and an ED length of 4+3×4+8+4=28 bytes. CDW10–12 occupy bytes4–15, buffer16–23, and completion DW0 24–27.'),reading=bi('Figure252先判斷是否記錄，253再解資料位置；256是另一種專屬事件格式。','Figure252 defines logging policy, 253 the variable layout, and 256 a separate dedicated event.')),

dict(key='extensions',title=bi('識別值映射與廠商擴充如何讀到正確邊界','Read identifier mappings and vendor extensions within their boundaries'),claims=[
 claim('ET10 記錄 Exported NVM Subsystem 的建立、刪除或實體變更；OTYP 決定 EEID／UEID 代表namespace、controller、port或其他對象。ETDE 的 ED 是一串廠商資料描述子，每筆長度為6+VSEDL，依VSEDT選資料型別；廠商事件與任何事件皆可能有的VSI並不是同一層。ETDF的內容格式由TCG保留定義。',
 'ET10 records creation, deletion or entity changes of an Exported NVM Subsystem; OTYP determines whether EEID/UEID identify a namespace, controller, port or another object. ETDE ED contains vendor descriptors, each 6+VSEDL bytes and interpreted by VSEDT. A vendor event differs from the optional VSI attached to any event. ETDF payload formatting is reserved for TCG definition.','5.2.13.1.14.2.16; 5.2.13.1.14.2.17; 5.2.13.1.14.2.18','293-296'),
],steps=[
 ('同一個實體可以有兩套編號','Exported NVM Subsystem是在底層資源之上呈現的儲存子系統；PEL記錄其中實體對應關係的改變。假設Exported namespace5對應Underlying namespace42，EEID=5、UEID=42描述的是同一映射的兩端，不是兩個互相競爭的namespace ID。OTYP=2表示新增namespace，4則改成新增controller，解讀欄位前先確認種類。這裡只教事件內的映射，不展開傳輸或建立流程。'),
 ('廠商事件有自己的內部串列','共同事件header後可能先有VSI，再有ETDE的ED。ED內又是一筆筆小描述子，每筆有VSEC、VSEDT、UIDX、VSEDL與VSED。前面的VSI大小由VSIL管；內部資料大小由各自VSEDL管。不要看到兩個都寫vendor就合在一起，也不要把外層EL當作每一筆內部描述子的長度。'),
 ('先讀型別，再決定怎樣顯示','VSEDT=1是以零字元結尾的事件名稱，若存在必須第一筆；2是其他ASCII字串；3是二進位，byte order由廠商定義；4是64-bit有號整數，使用二補數。原始bytes全是FF，在型別4可代表−1，在型別3卻不應自動當−1。VSEC由廠商定義，同類事件必須使用一致的碼；UIDX記錄事件當時的UUID索引。'),
 ('能確認外框，不代表能憑空解出廠商意義','沒有廠商資料定義，仍能確認每筆描述子的範圍、資料型別、原始值及名稱，但不能編造某個VSEC表示哪種故障。同樣地，ETDF只在本份Base規格中保留給TCG定義事件版本與內容；可以按共同外框辨認並保留這笔事件，不能拿ETDE的描述子規則套上去。'),
],example=bi('廠商ED先放名稱「TEMP」：含結尾零共5 bytes，第一描述子總長11；再放型別4的8-byte整數，第二描述子總長14。ED合計25；若VSIL=0、EHL=21，外層事件總長49 bytes。',
 'A vendor ED contains the name “TEMP” plus its zero terminator: five data bytes and an eleven-byte descriptor. A second descriptor holds an eight-byte type4 integer and totals fourteen bytes. ED totals25; with VSIL=0 and EHL=21, the outer event totals49 bytes.'),reading=bi('Figure257按OTYP選識別值；258～260由清單走到描述子，再選型別。','Figure257 selects identifier semantics by OTYP; 258–260 move from list to descriptor to data type.')),
]

# Tutorial conclusions apply the rule to a new case instead of repeating the
# overview example that already appears in the detailed walkthrough.
TUTORIAL_OUTCOMES={
 'purpose':'讀一份只剩最新20筆的PEL時，可以解釋這20筆各自保存的事實；但沒有廠商的保存與抑制策略，就不能用它計算整段使用期間的完整事件發生率。',
 'context':'若ACT3回RCE1，而且你要取得context建立之後才發生的事件，只重新讀header不會更新集合。應先與其他讀取者協調，結束舊context，再建立新的一份。',
 'layout':'接續算例：從556開始的下一筆若header24、EL22，會在602結束。第三筆就從602開始；實際傳輸仍可用對齊的區塊包含這個位置，不能把第三筆擅自移到604。',
 'health':'比較兩份SMART快照時，先確認相同controller，再看事件時間與欄位是否有回報。即使累計DUR增加，也不能只憑兩個向上取整的值宣稱精確新增了多少bytes。',
 'time':'讀到Timestamp Change後，應把它當作時鐘基準曾調整的明確紀錄。保留事件原始排列與各控制器資訊，才能說明時間數字變小的原因，而不把它誤當成紀錄倒序。',
 'namespace':'在PEL中找到一次成功Create，能知道分配出的NSID與當時輸入格式；仍不能推論它今天存在、已附接本控制器，或後來沒有再被Format。每個結論需要相應的時間與事件證據。',
 'sanitize':'對namespace清除，原始SCDW10的bit4是PREQ；對subsystem overwrite，同一bit屬於OWPASS。保存同樣的32-bit數值，不代表套用同一個欄位格式。',
 'hardware':'若一筆硬體事件只有ED前綴而沒有AHEI，先看NSHEEC：05h或09h本來就沒有附加內容，不能一律判成被截斷。若種類要求特定內容，才需要確認實際長度是否足夠。',
 'features':'把例子改為DWC2、MBC0、LCCDW00：SFEL=2，ED只有12 bytes，最後是CDW11。此時沒有buffer，也沒有CQE DW0，不要繼續多讀4 bytes。',
 'extensions':'OTYP2的EEID可以使用32bits；例如說明用的namespace ID70000不能截成16bits。若OTYP4改為controller，卻必須依該列只讀低16bits，不以namespace的寬度類推。',
}
for unit in UNITS:unit['tutorial_outcome']=TUTORIAL_OUTCOMES[unit['key']]
