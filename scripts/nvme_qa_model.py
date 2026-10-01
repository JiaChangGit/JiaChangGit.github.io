"""Question bank: bilingual, source-located answers for the approved Q1–Q68."""
from importlib import import_module

LABELS = [
('這個功能要解決什麼問題？','What problem does this function solve?'),
('它的影響範圍是什麼？','What is its scope?'),
('支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？','Which register, Identify field, feature or log page establishes support?'),
('涉及哪些 Command 與重要欄位？','Which commands and fields matter?'),
('正常流程及先後順序是什麼？','What is the normal sequence?'),
('成功時應回傳什麼結果？','What indicates success?'),
('不支援、非法參數或錯誤順序時的 Status？','What status applies to unsupported, invalid or out-of-order requests?'),
('DNR 與 More 應如何設定？','How are DNR and More set?'),
('是否產生 Asynchronous Event？','Is an asynchronous event generated?'),
('是否更新 Error Information Log 或其他 Log？','Are Error Information or other logs updated?'),
('是否記錄於 Persistent Event Log？','Is it recorded in the Persistent Event Log?'),
('Controller Reset 後是否保留或繼續？','What survives or continues after Controller Reset?'),
('NVM Subsystem Reset 後是否保留或繼續？','What survives or continues after NVM Subsystem Reset?'),
('Power Cycle 後是否保留或繼續？','What survives or continues after a power cycle?'),
('是否影響其他 Controller 或 Namespace？','Are other controllers or namespaces affected?'),
('Identify、Feature、Log 與 Command 行為是否一致？','Are Identify, features, logs and command behavior consistent?'),
('結果不符預期時，第一個要檢查什麼？','What should be checked first when the result differs?')]

# Locator strings are source prefix | section | PDF start-end | figure numbers.
REFS = {'conventions': 'B|1.4.1|28-29|', 'cap': 'B|3.1.4 (CAP, VS)|80-85|36–37', 'cc': 'B|3.1.4 (CC, CSTS, NSSR)|86-92|41–43', 'adminreg': 'B|3.1.4 (AQA, ASQ, ACQ, CMBLOC)|92-94|44–47', 'crto': 'B|3.1.4 (CRTO)|98-99|57', 'init': 'B|3.5.1|131-132|', 'ready': 'B|3.5.3–3.5.4|135-139|84–85', 'shutdown': 'B|3.6.1|140-141|', 'reset': 'B|3.7.1–3.7.4|146-150|', 'queue': 'B|3.3.1|114-117|73–74', 'qattr': 'B|3.3.3–3.4.1|127|', 'order': 'B|3.4.1–3.4.5|127-131|80–81', 'sqe': 'B|4.1.1|165-168|92–93', 'cqe': 'B|4.2.1, 4.2.3–4.2.4|170-183|97–105, 109', 'status': 'B|4.2.3|171-181|101–105', 'error': 'B|5.2.13.1.2|244-246|212', 'aer': 'B|5.2.2|209-216|150–156', 'pel': 'B|5.2.13.1.14 (header, reset, hardware, Set Feature events)|270-282,284,288-290|232–244, 246, 252–253', 'fatal': 'B|9.1–9.6.1|851-852|', 'create': 'B|5.3.1–5.3.2|553-557|571–579', 'delete': 'B|5.3.3–5.3.4|557-558|580–583', 'number': 'B|5.2.30.1.5|491-492|472–473', 'arbit': 'B|5.2.30.1.1|486|467', 'idcmd': 'B|5.2.14.1|362-366|332–337', 'idctrl': 'B|5.2.14.2.1|366-413|338–341', 'idlist': 'B|5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2|413-425,428-430|342–355, 360–362', 'idns': 'N|4.1.5.1–4.1.5.4|84-107|123–130', 'nsid': 'B|3.2.1|104-107|', 'identity': 'B|4.7.1|199-201|', 'uuid': 'B|8.1.31.1–8.1.31.2|763-764|782', 'virtual': 'B|8.2.7|780-785|796', 'nsmanage': 'B|5.2.24–5.2.25, 8.1.17|468-474,686-690|442–450', 'effects': 'B|5.2.13.1.5|252-256|216–218', 'feature': 'B|4.4|192-195|126–127', 'getfeat': 'B|5.2.12|235-238|197–202', 'setfeat': 'B|5.2.30.1 (common fields, scope and persistence)|482-486|463–466', 'setcomplete': 'B|5.2.30 (Command Completion)|545|554', 'vwc': 'B|5.2.30.1.4|490-491|471', 'aec': 'B|5.2.30.1.6|492-494|474', 'power': 'B|5.2.30.1.2, 5.2.30.1.7|486-488,494-495|468–469, 475–478', 'powerstates': 'B|8.1.19|692-698|738–740', 'thermal': 'B|5.2.30.1.10|497-498|482', 'timestamp': 'B|5.2.30.1.8|495-497|479–480', 'keepalive': 'B|3.9 (common and PCIe rules), 5.2.30.1.9|155-161,497|481', 'rrl': 'B|5.2.30.1.12, 8.1.23|499,715-716|484–485, 755', 'behavior': 'B|5.2.30.1.15|501-503|491', 'profile': 'B|5.2.30.1.18|504-505|494–495', 'irqfeat': 'B|5.2.30.2.1–5.2.30.2.2|540-541|543–544', 'hmb': 'B|5.2.30.2.3, 8.2.4|541-545,770|545–553', 'nwp': 'B|5.2.30.1.38, 8.1.18|538,690-692|541, 735–737', 'nvmfeat': 'N|4.1.3.1–4.1.3.7|64-69|92–101', 'nvmatomic': 'N|2.1.2–2.1.4|14-20|3–9', 'pcie': 'P|3.1–3.4|9-13|3–8', 'irq': 'P|3.5|13-16|9', 'pciconfig': 'P|3.8.1 (NVMe configuration access)|16-18|10–17'}

def pair(text):
    parts=text.strip().split(' || ')
    if len(parts)!=2 or not all(parts): raise ValueError('Expected a Chinese / English pair: '+text[:100])
    return tuple(parts)

# These are complete answers to shared mechanics, not a blanket yes/no default.
COMMON = {
'command': {
8: ('有 CQE 時，DNR=1 表示相同命令再送到此 NVM subsystem 的任一 controller 仍預期失敗；DNR=0 只表示可能成功。除非本題錯誤另有明定，不把某個 Status 固定綁成 DNR=1。More=1 表示 Error Information Log 有這筆命令的補充資訊。SCT=SC=0 時 DNR 應為 0。','For a CQE, DNR=1 means the identical command is expected to fail if resubmitted to any controller in this subsystem; DNR=0 means it may succeed. Do not assign DNR=1 solely from an error name unless that condition mandates it. More=1 identifies additional information for this command in the Error Information Log. DNR should be zero when SCT=SC=0.'),
9: ('命令完成與非同步通知是兩件事；本題操作成功本身不保證有事件。若操作引起規範列出的事件，還要核對事件支援、適用的通知設定、是否已遮蔽，以及 Host 是否掛入 Asynchronous Event Request。','Command completion and asynchronous notification are separate. Success here does not itself guarantee an event. For a defined resulting event, check support, applicable notification configuration, masking and an outstanding Asynchronous Event Request.'),
10: ('成功 CQE 不是要求新增 Error Information 的理由。錯誤有 More=1 時，查 LID 01h 並用 SQID、CID 和 Error Count 對應；不能把每個非成功 CQE 都當成必須新增一筆。操作改變的狀態則由本題列出的查詢介面重新讀取。','A successful CQE does not require a new Error Information entry. For an error with More=1, read LID 01h and correlate SQID, CID and Error Count; not every unsuccessful CQE requires a new entry. Re-read the interfaces named in this question for the state the operation changes.'),
11: ('Persistent Event Log 是選配的事件歷史，不是所有命令的執行清單。先查 LPA 的支援與 Supported Events Bitmap，再判斷本次是否符合指定事件的記錄條件；不能只因命令成功或失敗就要求新增一筆。','The optional Persistent Event Log is an event history, not a trace of every command. Check LPA support and the Supported Events Bitmap, then the logging condition for the particular event. Command success or failure alone does not require an entry.'),
},
'register': {
8: ('不適用於這次 Register 存取：它沒有 NVMe CQE，因此沒有可設定的 DNR／More。若之後的 Admin 或 I/O 命令失敗，才解讀那筆命令的 CQE。','Not applicable to this register access: it has no NVMe CQE and therefore no DNR or More to set. Decode those bits only for a subsequent Admin or I/O command that actually returns a CQE.'),
9: ('這次 Register 存取本身不定義一筆成功通知。若另發生 Internal Error 等已定義事件，使用該事件規則；Controller 還不能處理 Admin Queue 時，不能把等待事件當成初始化完成判斷。','This register access does not define a success notification. A separate defined event, such as an Internal Error, follows its own rules. When the Admin Queue is unavailable, waiting for an event cannot replace initialization-state checks.'),
10: ('不會因每次讀寫 Register 就要求建立 Error Information entry。初始化問題先保存 CAP、CC、CSTS、CRTO 與時間；若之後能讀 Log，再用事件及錯誤內容補足證據。','Every register read or write does not require an Error Information entry. Preserve CAP, CC, CSTS, CRTO and timestamps first; logs provide additional evidence if the controller subsequently permits access.'),
11: ('一般 Register 存取不是獨立的 Persistent Event。若發生重設、電源或硬體錯誤，只有在支援 PEL 且符合對應事件條件時才要求記錄；不能將每次 CC 寫入都等同 Power-on or Reset 事件。','An ordinary register access is not a separate persistent event. Reset, power or hardware conditions are recorded when PEL support and the corresponding event requirements apply; each CC write is not automatically a Power-on or Reset event.'),
},
'queue': {
12: ('清除 CC.EN 使 Controller Level Reset 執行：I/O SQ／CQ 被刪除，Admin Queue 的指標重設；AQA／ASQ／ACQ 在這種重設中保留不代表舊 CQE 仍有效。重新初始化 Admin CQ 的 Phase，Enable 後重新配置及建立 I/O Queue。','Clearing CC.EN initiates a Controller Level Reset: I/O queues are deleted and Admin Queue pointers reset. Retention of AQA/ASQ/ACQ for this reset does not validate old CQEs. Reinitialize Admin CQ phases, enable, then configure and recreate I/O queues.'),
13: ('受 NVM Subsystem Reset 影響的 controller 執行 Controller Level Reset；舊 Queue 不能沿用。Host 應重新確認傳輸與 Register 狀態，再建立 Admin／I/O 操作環境，不套用 CC.EN 重設對 AQA 等 Register 的保留例外。','Affected controllers undergo Controller Level Reset during an NVM Subsystem Reset; old queues cannot be reused. Re-establish transport and register state and the Admin/I/O environment. Do not apply the AQA retention exception of a CC.EN reset to this different reset source.'),
14: ('斷電後重新走初始化與 Queue 建立流程。主機記憶體中即使還有舊 SQE／CQE 位元，也不是新一輪 Queue 的有效命令或完成；Host 必須重建自己的指標、Phase 與 outstanding 對照。','After a power cycle, initialize and create queues again. Residual SQE/CQE bytes in host memory are not valid commands or completions for the new queue lifetime; rebuild host pointers, phases and outstanding-command tracking.'),
15: ('Queue 屬於建立它的 controller，不因相同 QID 就和別的 controller 共用。共用 CQ 的多個 SQ 則有直接關係：CQ 空間不足或刪除順序會影響它們。Queue 重設不等於刪除 namespace 或撤銷已完成的資料寫入。','Queues belong to their controller; equal QIDs on different controllers do not identify the same queue. SQs sharing a CQ are directly coupled through CQ capacity and deletion ordering. Queue reset neither deletes a namespace nor reverses completed writes.'),
},
'identify': {
12: ('Controller Reset 中止尚未完成的查詢；不要把沒有收到的回覆當成全零資料。重新建立查詢路徑後再讀取，按欄位判斷固定識別、目前配置及動態狀態；Reset 本身不代表 namespace 被刪除。','Controller Reset stops an outstanding query; a missing response is not an all-zero result. Re-read after recovery, distinguishing identity, configuration and dynamic state by field. Reset alone does not mean the namespace was deleted.'),
13: ('重設完成後重新探索受影響 controller 與 namespace。NVM Subsystem Reset 是通訊與控制狀態的重設，不能直接推論所有儲存配置回到出廠值；另有管理操作時，依那個操作確認變更。','Rediscover affected controllers and namespaces after reset. An NVM Subsystem Reset does not by itself imply that all storage configuration returns to manufacturing defaults. Verify changes caused by any separate management operation.'),
14: ('Power Cycle 後重新查詢版本、能力、目前格式及附加清單。固定識別資訊與持續配置不應被當成一般暫存 Feature；但韌體啟用或配置變更可能有不同結果，必須留下前後快照及事件時間。','After a power cycle, re-read version, capabilities, current format and attachment lists. Stable identity and persistent configuration are not ordinary volatile feature values. Firmware activation or configuration changes require before/after snapshots and event timing.'),
15: ('Identify 只讀資料，不會建立、格式化或附加 namespace。回覆的觀察範圍依 CNS 與選擇欄位決定；另一個 controller 看到的 active list 可以不同，不能因清單不同就判定資料損壞。','Identify reads data; it does not create, format or attach a namespace. CNS and selectors determine the view. Active lists may differ across controllers, so different lists do not alone establish corruption.'),
},
'feature': {
12: ('先分 scope 與 saveable。整個 subsystem 受重設影響時，可保存 Feature 的 Current 回 Saved（沒有 Saved 則 Default）；不可保存且不持續的回 Default。多 controller 只重設其中一個時，共用 scope 另依 Figure 127 保留；本題列出的個別 Feature 規則優先。','Separate scope from saveability. For a reset covering the subsystem, a saveable Current value is restored from Saved, or Default if no Saved value exists; a non-saveable, nonpersistent value returns to Default. A partial reset uses Figure 127 for shared scopes. The specific feature exceptions in this question take precedence.'),
13: ('不能只看 Reset 名稱。若重設涵蓋整個 subsystem，使用 Figure 126；若 multi-domain 的重設只涵蓋一部分，使用 Figure 127。不可保存但規定持續的值繼續保留，不能誤用「不可保存＝重設清零」。','Determine reset coverage, not only its name. Figure 126 applies to the whole subsystem; Figure 127 applies to a partial multi-domain reset. A non-saveable feature specified as persistent remains persistent; non-saveable does not mean reset to zero.'),
14: ('可保存且 SV=1 成功的設定，在斷電後依 Saved 恢復；SV=0 不會更新 Saved。不可保存的 Feature 才看 Figure 466 的持續性欄與個別例外。重新取得 Current 和行為結果，不能只看到 Saved 存在就假設硬體正在使用它。','A successfully saved SV=1 setting is restored from Saved across a power cycle; SV=0 does not update Saved. For non-saveable features use Figure 466 persistence and feature-specific exceptions. Verify Current and behavior rather than assuming an existing Saved value is already active.'),
15: ('依 Feature scope 決定。Controller scope 通常只控制目標 controller；namespace、NVM Set 或 subsystem scope 可能由其他 controller 共同觀察。跨 Host 修改共用設定需要協調，不能把 NSID=FFFFFFFFh 當成所有 Feature 通用的廣播。','Feature scope determines impact. Controller-scoped settings target that controller; namespace, NVM Set and subsystem settings may be shared across controllers. Coordinate changes across hosts and do not treat NSID=FFFFFFFFh as a universal feature broadcast.'),
}
}

QUESTIONS=[]
def add(number, title, profile, refs, body, overrides=None):
    """Author Q1–7,16–17 individually; use applicable common mechanics for Q8–15."""
    rows=[pair(line) for line in body.strip().splitlines() if line.strip()]
    if len(rows)!=9: raise ValueError((number,len(rows)))
    answers={i:value for i,value in zip([1,2,3,4,5,6,7,16,17],rows)}
    base='register' if profile=='register' else 'command'
    answers.update(COMMON[base])
    answers.update(COMMON[profile if profile in ('identify','feature') else 'queue'])
    if overrides: answers.update({k:pair(v) if isinstance(v,str) else v for k,v in overrides.items()})
    common_refs=['reset']
    if base=='command':common_refs+=['status','error','aer','pel']
    else:common_refs+=['pel','fatal']
    if profile=='feature':common_refs+=['feature','setfeat']
    QUESTIONS.append(dict(id=number,title=pair(title),profile=profile,refs=list(dict.fromkeys(refs+common_refs)),answers=answers))

def load():
    if not QUESTIONS:
        for module in ('init','queues','doorbells','commands','identify','features'):
            import_module('scripts.nvme_qa_'+module)
        refine()
    return sorted(QUESTIONS,key=lambda x:x['id'])

def refine():
    """Topic-specific event exceptions and evidence discovered during source review."""
    REFS.update({
        'featureeffects':'B|5.2.13.1.18|302-304|270–271',
        'nschange':'B|5.2.13.1.4, 5.2.13.1.14.2.6–5.2.13.1.14.2.8|251-252,284-287|215, 247–249',
    })
    feature_pel=pair('若支援 PEL 的 Set Feature Event，還要看 Figure 252 是否支援記錄此 FID：Set 成功且設定改變時必須記錄；成功但重設相同值則允許記錄。不是每個 FID 都能套用此事件；Timestamp 的 Set Feature Event 明確禁止，另用 Timestamp Change Event 判斷。 || With supported PEL Set Feature logging, Figure 252 must also permit and support this FID: successful changes shall be recorded; successfully reapplying the same value may be recorded. This is not universal across FIDs. Timestamp is prohibited from Set Feature logging and uses its separate Timestamp Change event rules.')
    COMMON['feature_events']={11:feature_pel}
    for q in QUESTIONS:
        if q['profile']=='feature':
            q['answers'][11]=feature_pel
            q['refs'].append('featureeffects')
    q=next(q for q in QUESTIONS if q['id']==6)
    q['answers'][1]=pair('CFS 通常表示嚴重 controller 狀態，與單一命令失敗不同。但若是 virtualization 的 secondary controller，進入 Offline 也會設定 CFS；先確認 controller 角色與 Online／Offline，不能直接宣判硬體故障。 || CFS normally signals a serious controller condition rather than an individual command error. A virtualized secondary controller also sets CFS when Offline, so establish its role and Online/Offline state before diagnosing a hardware failure.')
    q['refs'].append('virtual')
    q=next(q for q in QUESTIONS if q['id']==51)
    q['answers'][9]=pair('Identify 查詢本身不產生變更事件。Create、Delete、Attach、Detach 或 Format 所造成的 namespace attribute 變化，須按影響對象、支援與 AEC 設定判斷 Namespace Attribute Changed 通知；不同 controller 不一定看到相同變更。 || Identify queries do not generate change events. Namespace attribute changes from Create, Delete, Attach, Detach or Format follow the affected-controller, support and AEC conditions for Namespace Attribute Changed; controllers need not observe identical changes.')
    q['answers'][10]=pair('檢查 Changed Namespace List（LID 04h）與重新讀取的 Identify；前者通知哪些 NSID 曾變更，不取代目前配置。讀取的 RAE 設定會影響通知確認，先保存原事件與清單，再做後續查詢。 || Check Changed Namespace List (LID04h) alongside fresh Identify data. The list identifies changed NSIDs, not current configuration. RAE affects acknowledgement; preserve the event and list before subsequent queries.')
    q['answers'][11]=pair('支援 PEL 時，Create／Delete 的 Change Namespace Event 與 Format Start／Completion 是不同事件。Attach／Detach 不可直接當成 Create／Delete 記錄；Identify 本身也不要求新增這些事件。 || With PEL support, Change Namespace events for Create/Delete differ from Format Start/Completion events. Attach/Detach are not Create/Delete records; Identify itself does not require these events.')
    q['refs'].append('nschange')
    q=next(q for q in QUESTIONS if q['id']==62)
    q['refs'].append('powerstates')
    q['answers'][11]=pair('Power Management 的 Set Feature Event 為 Not Recommended；APST 與 HCTM 的 Set Feature 記錄為 Optional，支援後依成功且設定改變的條件記錄。實際跨越熱門檻另看 Thermal Excursion Event，不把一次設溫度等同一次溫度異常。 || Power Management Set Feature logging is Not Recommended; APST/HCTM logging is Optional and, when supported, follows successful-change rules. Actual temperature excursions use Thermal Excursion event conditions; setting a threshold is not a temperature excursion.')
    REFS['thermalpel']='B|5.2.13.1.14.2.13|291-292|255'
    q['refs'].append('thermalpel')
    q=next(q for q in QUESTIONS if q['id']==63)
    q['answers'][11]=pair('Timestamp 不得記成 Set Feature Event；支援 PEL 時改看 Timestamp Change Event（03h），保留變更前後值。KATO 與 HMB 的 Set Feature 記錄為 Optional，若支援，成功且設定改變時需記錄；不能要求所有 Get 都留一筆。 || Timestamp shall not be logged as a Set Feature event; with PEL, use Timestamp Change (03h) and its before/after values. KATO/HMB Set Feature logging is Optional; when supported, successful changes require recording. Gets are not universally logged.')
