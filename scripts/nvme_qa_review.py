"""Explicit cross-topic corrections after loading the authored chapters."""
from scripts.nvme_qa_model import COMMON, QUESTIONS, pair

def review():
    byid={q['id']:q for q in QUESTIONS}
    def set_values(ids,values):
        for n in ids:byid[n]['answers'].update({k:pair(v) if isinstance(v,str) else v for k,v in values.items()})
    # Timestamp is a clock feature, not a persistent-log reporting context.
    COMMON['timestamp_op']={**COMMON['command'],**{k:byid[214]['answers'][k] for k in range(9,16)}}
    for n in (214,215,216):
        byid[n]['answers'].update(COMMON['timestamp_op']);byid[n]['profile']='timestamp_op'
        byid[n]['refs']+=['timestamp','feature','setfeat']
    set_values([174],{8:'Queue Level Reset 若透過 Delete／Create 命令處理，要解讀各命令的 CQE；CC.EN 與 NSSR 等 Register 操作沒有 NVMe CQE，因此沒有 DNR／More。不能將這幾種機制的回報方式混用。 || Queue-reset Delete/Create commands have CQEs; CC.EN/NSSR register accesses do not. DNR/More therefore apply only to the command completions.'})
    set_values([146],{
        10:'Register 路徑以 BPINFO.BRS 回報讀取狀態，不會產生 Firmware Slot Log 更新。Get Log Page 路徑則回傳選定 Boot Partition 的資料；讀取失敗依其 CQE 與錯誤記錄條件判斷。 || Register reads report through BRS, without updating firmware-slot history; the log path returns selected boot data and uses its own CQE/error rules.',
        12:'Boot Partition 內容不是隨 CLR 清除的 queue 資料；但 Host 不得在 Register 讀取進行中執行 Reset。重設後重新檢查屬性與 BRS，不能沿用未完成讀取的成功假設。 || Boot contents are not cleared like queue state, but the host must not reset during an active register read. Recheck properties/state afterward.',
        13:'Subsystem Reset 後重新探索共享 Boot Partitions 與讀取狀態；這不是刪除 Boot 映像的操作。若先前讀取未完成，不得將舊 buffer 當作已成功取得完整資料。 || Rediscover partitions and read state after subsystem reset; reset is not boot-image erasure and does not validate an incomplete buffer.',
        14:'Boot 映像保存在非揮發儲存中，Power Cycle 後重新讀取。FID85h 的預設保護為 Write Locked；保護狀態與映像內容是兩項不同資訊。 || Boot images persist in nonvolatile storage and can be reread after power cycling; FID85h defaults to Write Locked independently of image contents.',
        15:'多個 controllers 可共用 Boot Partitions。查詢時確認目前 controller 的 CAP、BPINFO 與共享關係，不以某台 controller 的讀取完成推論其他台的獨立 buffer 也已完成。 || Controllers may share partitions, but one controller’s completed transfer does not complete another’s buffer.'})
    set_values([147],{10:'以 Commit CQE、BPINFO.ABPID、Boot Partition 讀回資料及 FID85h 核對更新。一般 Firmware Slot Information 描述 firmware slots，不是 Boot Partition 映像清單。 || Verify commit, ABPID, boot-data readback and protection; firmware-slot information is not a boot-image inventory.'})
    set_values([148],{
        9:'不經 Reset 的 controller firmware 啟用，依啟用設定回報 Firmware Activation Starting；Boot CA6／CA7 不屬於這種啟用，不要求相同通知。 || Reset-free controller-firmware activation follows the enabled Starting notice; Boot CA6/CA7 do not require that notice.',
        10:'Firmware 更新讀 LID03h 與 Identify.FR；Boot 更新讀 ABPID、內容與保護狀態。失敗時各自保留 Commit CQE 及可關聯的 Error Information。 || Firmware uses slot information and running revision; boot uses ABPID, content and protection. Preserve target-specific commit/error evidence.',
        12:'CLR 會丟棄尚未 Commit 的暫存下載。已 Commit 的 firmware 按 CA 與所需 reset 啟用；Boot 寫入中斷則可能留下混合內容，需重新讀回確認。 || CLR discards uncommitted staging; committed firmware follows activation rules, while interrupted boot writes can leave mixed contents.',
        13:'Subsystem Reset 可能滿足 firmware 要求的啟用方式，但不能保證被中斷的 Boot 寫入已成功。恢復後依更新對象查 slot／FR 或 Boot 內容／ABPID。 || Subsystem reset can satisfy firmware activation requirements but does not validate an interrupted boot write; inspect the appropriate result.',
        14:'Firmware 啟用中失電後需查實際執行映像及可能的回復結果；Boot Commit 失電可留下新舊混合內容。兩者都不能只因重新上電就宣告更新成功。 || After power loss verify actual firmware/fallback or potentially mixed boot contents; power restoration alone proves neither update successful.',
        15:'Firmware 以共享 slot 的 Domain 為主要範圍；Boot 以共享該 partition 的 controllers 為範圍。更新時先找出所有共用者，不能只協調提交命令的那條路徑。 || Coordinate the firmware domain or all controllers sharing a boot partition, not only the submitting path.'})
    for n in (118,119):
        set_values([n],{i:'本題比較兩種操作：'+COMMON['format_op'][i][0]+' Sanitize 則不同：'+COMMON['sanitize_op'][i][0]+' || This comparison distinguishes Format: '+COMMON['format_op'][i][1]+' Sanitize: '+COMMON['sanitize_op'][i][1] for i in range(9,16)})
    set_values([223,236],{
        9:'配置 HMB、CMB 或 PMR 本身沒有通用成功 AER。PMR 若進入唯讀等符合 SMART 警告的狀態，才依該警告與通知設定回報，不能將 HMB 的正常啟用當成同一種事件。 || No generic success AER accompanies memory configuration; qualifying PMR health warnings use their specific SMART/event rules.',
        10:'HMB 用 Feature 及實際存取生命週期驗證，CMB 用位置與用途能力驗證，PMR 另需檢查 Ready、ERR、HSTS。這些觀察不是逐次寫入 Error Information 的要求。 || Verify HMB lifetime, CMB placement/use and PMR readiness/error/health; these observations are not per-access error-log mandates.',
        11:'一般記憶體存取不是 PEL 事件。支援的 HMB Set Feature 記錄與 PMR 健康／硬體事件需各自符合條件，不能要求每次存取都有事件。 || Ordinary memory access is not a PEL event; supported HMB feature changes and PMR health/hardware events follow separate conditions.'})
    # Read-only topology queries and namespace operations should not inherit
    # secondary-resource allocation semantics as if they were the same action.
    for n in (247,249,251):
        for i in range(9,16):byid[n]['answers'][i]=COMMON['namespace_op'][i]
    for n in (248,252):
        for i in range(12,16):byid[n]['answers'][i]=COMMON['identify'][i]
    set_values([260,261],{
        12:'Group 的累計健康資訊不因查詢 controller 的 CLR 就重新開始；目前警告則需在恢復後依實際狀態判讀。未完成的 Log 查詢要重新送出。 || Group lifetime health is not restarted by a querying controller reset; reassess current warnings and reissue interrupted reads.',
        13:'Subsystem Reset 不等於刪除 Endurance Group。恢復後讀同一 ENDGID，分開比較累計值、目前狀態及已確認的事件。 || Subsystem reset does not delete the group; compare cumulative values, current state and acknowledgment state separately.',
        14:'未被刪除的 Group 保留其生命週期資訊；Power Cycle 後重新讀取。FID18h 與 AEC 的設定恢復另依 Feature 規則，不由 Log 保留性推論。 || A retained group’s lifetime information persists; feature/event configuration restoration remains a separate rule.',
        15:'健康資料以 Group 為範圍；多個 controllers 可能查看同一資料。RAE 確認也會影響後續事件觀察，需保存讀取者與時間。 || Group health can be shared across readers; record acknowledgments and reader timing.'})
    # Feature questions in the integration chapter retain the FID-specific PEL rule.
    set_values([299,303],{11:COMMON['feature_events'][11]})
    for q in QUESTIONS:q['refs']=list(dict.fromkeys(q['refs']))
