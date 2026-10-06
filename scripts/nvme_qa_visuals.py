"""Explanatory flows that replace prose, rather than repeat it below a diagram."""
from scripts.nvme_qa_model import pair

VISUALS = {}

def flow(n, replaces, title, intro, steps, conclusion):
    VISUALS[n] = dict(replaces=replaces, title=pair(title), intro=pair(intro),
                      steps=[(pair(a), pair(b)) for a,b in steps], conclusion=pair(conclusion))

flow(3, [4,5,6,17], 'Enable 的兩條等待期限 || The two readiness deadlines',
     '下圖把介面就緒與媒體就緒分開。兩個計時器都從 Enable 起算，不是在 RDY=1 後才開始等媒體。 || Interface readiness and media readiness are separate. Both deadlines start at Enable; the media timer does not restart when RDY becomes 1.', [
    ('起點：CC.EN 由 0 變 1 || Start: CC.EN changes from 0 to 1', '記下時間與 CC.CRIME；讀取 RDY、CFS，持續確認初始化狀態。 || Record the time and CC.CRIME; observe RDY and CFS throughout initialization.'),
    ('分支 A：With Media || Branch A: With Media', '以 CRWMT 判斷就緒期限。CRTO 的單位是 500 ms；到 RDY=1 才提交此模式允許的命令。 || Use CRWMT for the readiness deadline, in 500 ms units. Submit commands permitted by this mode only after RDY=1.'),
    ('分支 B：Independent || Branch B: Independent', '先以 CRIMT 判斷介面就緒，再以 CRWMT 判斷媒體期限。RDY=1 不代表媒體已健康可用；仍須遵守命令的媒體就緒條件。 || Use CRIMT for interface readiness and CRWMT for the media deadline. RDY=1 does not prove media health or availability; command-specific media conditions still apply.'),
    ('回到同一條時間軸驗證 || Check a single timeline', '教學假設 CRIMT=2、CRWMT=20：介面期限在 Enable 後 1 s，媒體期限在 Enable 後 10 s。 || With hypothetical CRIMT=2 and CRWMT=20, the deadlines are 1 s and 10 s after Enable.')],
    'A、B 是不同模式，不是依序執行的兩個操作。若發生初始化失敗，須連同 CFS 與失敗條件判斷，不能只因曾看到 RDY=1 就宣告成功。 || A and B are alternative modes, not consecutive actions. Evaluate CFS and failure conditions; merely observing RDY=1 does not establish successful initialization.')

flow(12, [5,6,17], '先有 CQ，SQ 才能引用它 || Create the CQ before an SQ refers to it',
     '箭頭表示必須等前一步完成，不能只依命令提交順序推定物件已經存在。 || Each arrow requires completion of the preceding step, not merely submission order.', [
    ('準備 CQ 記憶體 || Prepare CQ memory', '依大小與對齊要求配置，並初始化每個 CQE 的 Phase。 || Allocate with the required size and alignment, and initialize CQE phase bits.'),
    ('Create I/O CQ → 等 Admin CQ 回報成功 || Create I/O CQ → await success on the Admin CQ', '這筆 Create 的完成結果出現在 Admin CQ，不在正在建立的 I/O CQ。 || This Create completes on the Admin CQ, not on the new I/O CQ.'),
    ('Create I/O SQ → 等 Admin CQ 回報成功 || Create I/O SQ → await success on the Admin CQ', 'CQID 指向已成功建立的 CQ；兩筆 Create 的成功 Status 都是 SCT=0、SC=00h。 || CQID refers to the successfully created CQ. Both successful Creates report SCT=0, SC=00h.'),
    ('開始 I/O || Start I/O', '兩步都成功後，才填入 I/O SQE 並更新 SQ Tail Doorbell。 || Only after both steps succeed, populate I/O SQEs and update the SQ Tail Doorbell.')],
    '若 Create CQ 失敗，就還沒有可供這條 SQ 使用的 CQ。先處理失敗原因；「Create CQ 已提交」不能替代「Create CQ 已成功」。 || If CQ creation fails, that CQ is not available to the SQ. Resolve the failure; submitted is not the same as successfully created.')

flow(27, [5,6,17], 'Phase 跟著整圈變，不跟著每筆 CQE 變 || Phase changes per traversal, not per CQE',
     '教學假設 CQ 有 4 個位置，Host 第一圈期待 P=1。 || Assume a four-entry CQ; the host initially expects P=1.', [
    ('檢查目前 Head 的 P || Inspect P at the current head', 'P 不符期待值：這個位置還沒有本圈的新結果，先等待；不要解讀殘留的 CID 或 Status。 || If P does not match, wait: the slot has no new result for this traversal. Do not decode its stale CID or status.'),
    ('P 符合 → 處理 CQE || P matches → process the CQE', 'Head 依序走 0、1、2、3；這一圈各位置的新 CQE 都使用 P=1。 || Head visits 0, 1, 2 and 3. New CQEs in this traversal all use P=1.'),
    ('Head 從 3 回到 0 → 反轉期待值 || Head wraps from 3 to 0 → invert expected phase', '下一圈期待 P=0。若只從 1 移到 2，尚未換圈，期待值不變。 || Expect P=0 in the next traversal. Moving from slot 1 to 2 does not change the expected phase.')],
    '重新建立 CQ 時，要重新初始化 Phase 與 Host 的期待值。此處的 4-entry 大小只是方便看懂換圈的教學假設。 || Recreating the CQ requires reinitializing phase bits and the host expectation. Four entries are used only to illustrate wrapping.')

flow(75, [5], '把每一段放回正確的 Log 位置 || Place every chunk at its correct log offset',
     '教學假設：以 OT=0 讀取 8192 bytes 的 Log，每次傳輸 4096 bytes。 || Example: read an 8192-byte log with OT=0 in 4096-byte transfers.', [
    ('第 1 段：LPO=0、NUMD=1023 || Chunk 1: LPO=0, NUMD=1023', '這一段對應 Log 的 bytes 0～4095；保存查詢目標、回覆與取樣資訊。 || This transfer covers log bytes 0–4095; preserve the target, response and sampling information.'),
    ('第 2 段：LPO=4096、NUMD=1023 || Chunk 2: LPO=4096, NUMD=1023', '這一段對應 Log 的 bytes 4096～8191，接在前一段後面，沒有缺口。 || This covers bytes 4096–8191, immediately after the first chunk with no gap.'),
    ('合併前分別檢查範圍與一致性 || Check coverage and consistency before merging', '重疊 bytes 可用來比對；若兩次讀取期間內容變更，不能任意挑一份覆蓋另一份。 || Overlapping bytes can be compared; if content changed between reads, do not arbitrarily overwrite one version with another.')],
    '完整覆蓋 8192 bytes 只證明沒有漏段。各段是否屬於同一份資料，仍要依目標 Log 的 generation 或 context 機制確認。 || Covering all 8192 bytes proves coverage only. Use the particular log’s generation or context mechanism to establish consistency.')

flow(84, [5,6,17], '事件確認與補上 AER 是兩件事 || Acknowledgment and replenishing AERs are separate',
     '這是一般需透過 Log 確認的事件路徑；Immediate 與 One-Shot 須另依各自規則處理。 || This path applies to ordinary events acknowledged through a log; Immediate and One-Shot events follow their own rules.', [
    ('收到 AER Completion → 保存通知 || Receive an AER completion → preserve it', '先記錄事件種類、資訊與 LID，再讀取所需診斷內容。 || Record the event type, information and LID before reading diagnostic content.'),
    ('依事件規則確認 || Acknowledge under the event’s rules', '通常以成功的 Get Log Page、RAE=0 確認。RAE=1 是保留；讀取失敗也不能當作已確認。 || Typically acknowledge with a successful Get Log Page using RAE=0. RAE=1 retains the event, and a failed read does not acknowledge it.'),
    ('維持等待中的 AER || Maintain outstanding AERs', '重新提供 Request，才能接收後續回報；補 Request 本身不會確認上一個事件。 || Replenish requests for later notifications; a new request does not itself acknowledge the earlier event.')],
    '若警告條件持續存在，確認後仍可能再通知。確認前應考慮門檻或通知設定，避免反覆回報；檢查時分開確認「資訊已保存、事件已確認、Request 仍在等待」。 || A persistent warning may notify again. Consider thresholds or notification settings before acknowledgment; verify preservation, acknowledgment and pending requests separately.')

flow(113, [5,17], '先定位失效範圍，再選復原方式 || Locate the failure before selecting recovery',
     '下列分支是 Host 選擇復原範圍的判斷方式，不是規格要求每次都走完的固定三步。 || These branches guide the host’s recovery choice; they are not a mandatory three-step sequence.', [
    ('先看 CQ：是否已經有有效 Completion？ || First inspect the CQ: is a valid completion already present?', '若只是 Host 漏處理或沒有收到中斷，先處理 CQE 並追查通知路徑。 || If the host missed processing or an interrupt, consume the CQE and investigate notification.'),
    ('單筆命令仍未完成，Admin 通道正常 || One command remains outstanding; Admin path works', '可考慮針對目標送 Abort，再分別追蹤 Abort 與目標命令的結果。 || Consider a targeted Abort, tracking its result separately from the target command.'),
    ('Queue 受損，但管理通道可用 || Queue failure with a usable management path', '按 Delete／Create 規則復原相關 queue，確認舊存取已停止，再交接記憶體。 || Recover the affected queues under Delete/Create rules, confirming old accesses have stopped before reusing memory.'),
    ('Admin 嚴重失效，或 Delete 沒有完成 || Severe Admin failure or a Delete that does not complete', '考慮 Controller Reset；不必先強迫送出一筆已無法完成的 Abort。 || Consider Controller Reset without forcing an Abort through an unusable path.')],
    '沒有 CQE 時，Host timeout 本身沒有 DNR 可讀。復原後仍需確認背景管理操作是否持續，不能只以新 queue 能送命令作為全部完成的證據。 || Without a CQE, a host timeout provides no DNR bit. After recovery, also check ongoing background operations; a working new queue is not the whole result.')

flow(191, [5,6,17], 'APST：先設定來源狀態，再看閒置轉換 || APST: configure the source state, then observe idle transition',
     '教學假設 PS0 為工作狀態、PS3 為受支援的非工作狀態。以下只畫這一條轉換。 || Assume operational PS0 and supported non-operational PS3. Only this transition is shown.', [
    ('設定 PS0 entry，再 Get 確認 || Set the PS0 entry and verify it', 'APSTE=1、ITPT=2000 ms、ITPS=3，低 Dword 為 0007D018h。entry 的索引是來源 PS0，不是目標 PS3。 || Set APSTE=1, ITPT=2000 ms and ITPS=3: low Dword 0007D018h. The entry index is source PS0, not destination PS3.'),
    ('PS0 → 沒有 outstanding I/O，且連續閒置超過 2000 ms || PS0 → no outstanding I/O and continuously idle for over 2000 ms', '這才符合此 entry 的觸發條件；不能只從上一筆命令提交時刻開始累計。 || These are the entry’s triggering conditions; time since the last submission alone is insufficient.'),
    ('轉入 PS3 || Transition into PS3', 'ITPT 是轉換前的閒置門檻，不是進入或離開 Power State 的延遲。 || ITPT is the idle threshold before transition, not state entry or exit latency.')],
    'Get Features 讀回設定表，不能單憑讀回成功證明已發生轉換。ITPT=0 停用該來源 entry；APSTE=0 則停用整個 APST。 || Get Features returns configuration, not proof that a transition occurred. ITPT=0 disables that source entry; APSTE=0 disables APST globally.')

flow(206, [5,6,16,17], '同一個 Context 的完整讀取流程 || Read one complete reporting context',
     '先固定回報視圖，再分段讀取；期間新增的事件留待下一次 Context 回報。 || Establish the reporting view before reading chunks; later events belong to a subsequent context.', [
    ('ACT=3 → 讀 Header || ACT=3 → read the header', 'buffer 至少 512 bytes；記錄 GNUM、TLL 與回報 Context。 || Provide at least 512 bytes of buffer and record GNUM, TLL and the reporting context.'),
    ('ACT=0 → 按 LPO 分段讀取 || ACT=0 → read chunks using LPO', '依 TLL 安排範圍，讓所有片段都來自同一個 Context。 || Cover the TLL range while keeping every chunk in the same context.'),
    ('讀完再核對 GNUM || Recheck GNUM after reading', '相同：可確認這項一致性條件。不同：已讀資料可能無效，應重新讀取，不能只補最後一段。 || If unchanged, this consistency condition holds. If changed, the data may be invalid: reread it rather than replacing only the final chunk.'),
    ('ACT=2 → 釋放 Context || ACT=2 → release the context', '完成一致的讀取後釋放，再為下一次查詢取得新的回報視圖。 || Release after a consistent read, allowing a fresh view for the next query.')],
    '每段都保存 ACT、LPO 與 GNUM。Get Log Page 各自成功，不表示不同 Context 的片段可以混在一起。 || Preserve ACT, LPO and GNUM per chunk. Successful individual reads do not permit mixing different contexts.')

flow(226, [5,6,16,17], '以停用完成作為 HMB 記憶體交接點 || HMB ownership changes at disable completion',
     'Host 已提交停用命令時，controller 仍可能在使用 HMB。要等完成結果，才能回收記憶體。 || Submitting a disable request does not yet end controller access. Wait for completion before reclaiming memory.', [
    ('啟用成功 → Controller 可使用 HMB || Enable succeeds → controller may use HMB', 'Host 維持 buffer、Descriptor List 與位址映射有效。 || Keep buffers, the descriptor list and mappings valid.'),
    ('要求 EHM=0 → 等成功 CQE || Request EHM=0 → await a successful CQE', '尚未成功完成前，不改寫或回收仍由 controller 使用的記憶體。 || Do not modify or reclaim memory still in use before successful completion.'),
    ('停用成功 → Host 可回收或重配 || Disable succeeds → host may reclaim or reconfigure', '在重新啟用前，controller 不得再存取 HMB；原本就停用時，再停用也成功且不做其他動作。 || The controller must not access HMB until re-enabled. Disabling an already-disabled HMB succeeds without other action.'),
    ('另一種情況：Reset 後重新提供配置 || Separate case: provide the configuration after reset', 'Reset 不是停用 HMB 的必做步驟。若發生 Reset，可提供保留的原配置或新配置；只有完全符合 MR 前提時才能設 MR=1。 || Reset is not required to disable HMB. After a reset, supply the retained or a new configuration; use MR=1 only when all return-memory conditions hold.')],
    '驗證時把最後一次 HMB 存取、停用 CQE 與 Host 回收時刻放在同一條時間軸上。 || Compare the last HMB access, disable completion and host reclamation on one timeline.')

flow(232, [5,6,16,17], 'PMR 使用自己的 Enable 與 Ready || PMR has its own Enable and Ready',
     '不要把 CSTS.RDY 或 CC.EN 當成 PMR 是否可用的答案。 || CSTS.RDY and CC.EN do not answer whether PMR is usable.', [
    ('先配置所需的位址空間 || Configure the required address space', '依能力建立 BAR／controller 位址映射；無效 controller base address 另查 CBAI。 || Establish supported BAR/controller mappings; check CBAI for an invalid controller base address.'),
    ('設 PMRCTL.EN=1 || Set PMRCTL.EN=1', 'PMR 可以在 CC.EN=0 時啟用，不必先建立 NVMe 命令處理環境。 || PMR can be enabled with CC.EN=0, without first enabling NVMe command processing.'),
    ('等待 PMRSTS.NRDY=0 || Wait for PMRSTS.NRDY=0', '判斷未完成轉換前，Host 應至少等待 PMRTO×PMRTU；確認 PMRTU 使用分鐘或 500 ms 單位。 || Before judging the transition incomplete, the host should wait at least PMRTO×PMRTU, using the indicated minutes or 500 ms unit.'),
    ('再確認 HSTS、ERR 與用途 || Check HSTS, ERR and permitted use', 'EN=1、NRDY=0、健康與映射條件成立後，才能依支援用途存取。 || Access only when enabled, ready, healthy and correctly mapped, and only for supported uses.')],
    'NRDY=1 的意思是「尚未就緒」。PMRTO 也不是任意一筆 I/O 命令的執行期限。 || NRDY=1 means not ready. PMRTO is not an execution deadline for an arbitrary I/O command.')

flow(277, [4,5,6,17], '由剩餘長度決定 PRP2 的意義 || Determine PRP2 from the remaining length',
     '先算第一頁可放多少資料：頁面大小 P 減去 PRP1 的頁內 offset。剩餘長度 R 就是總長度扣掉已由第一頁描述的資料。 || First-page capacity is page size P minus PRP1’s page offset. Let R be the transfer length remaining after that first-page data.', [
    ('R=0：只需要第一頁 || R=0: only the first page is needed', 'PRP2 為保留欄位，不需要另一個資料頁。 || PRP2 is reserved; no additional data page is needed.'),
    ('0<R≤P：再一頁就夠 || 0<R≤P: one more page is enough', 'PRP2 直接指向第二個資料頁。 || PRP2 points directly to the second data page.'),
    ('R>P：還需要至少兩個資料頁 || R>P: at least two more data pages are needed', 'PRP2 指向 PRP List，由清單列出後續資料頁位址。 || PRP2 points to a PRP List containing the subsequent data-page addresses.')],
    '三列是互斥分支。教學假設 P=4096、offset=1024，第一頁容量為 3072 bytes：傳輸 4096 bytes 時 R=1024，PRP2 指資料頁；傳輸 8192 bytes 時 R=5120，PRP2 指清單。PRP2 沒有獨立的類型旗標，不能只看它非零就猜用途。 || These are mutually exclusive branches. With P=4096 and offset=1024, the first page holds 3072 bytes: a 4096-byte transfer leaves R=1024 (data-page pointer); an 8192-byte transfer leaves R=5120 (list pointer). PRP2 has no independent type flag; a nonzero value alone does not identify its meaning.')

flow(299, [5,6,17], 'Set 與 Get 不同時，先對齊查詢條件 || Align query conditions before comparing Set and Get',
     '先排除讀到不同種類設定值的情況，再判斷 controller 是否沒有套用設定。 || First rule out reading a different kind of value before concluding that the controller failed to apply a setting.', [
    ('保存 Set 要求與成功結果 || Preserve the Set request and successful completion', '記錄 FID、SV、NSID、其他選擇欄位及資料內容。 || Record FID, SV, NSID, other selectors and the payload.'),
    ('同一目標，以 SEL=0 讀 Current || Read Current with SEL=0 on the same target', '讀 Default、Saved 或另一個 namespace，都不能直接驗證這次目前設定。 || Default, Saved or another namespace’s value does not directly verify this current setting.'),
    ('檢查是否允許調整，再觀察實際效果 || Check allowed adjustment, then observe behavior', '讀回合法調整後的值，且行為符合該值，仍可構成成功驗證。 || A permitted adjusted value with matching behavior can be a valid successful result.'),
    ('若要驗證保存，另查 Saved 與指定 Reset || To test saving, separately inspect Saved and the specified reset', '保存是另一個測試目標，不要把 Current 的驗證與重設恢復混成一次數字比較。 || Persistence is a separate test objective; do not collapse current-value and reset-recovery checks into one numeric comparison.')],
    '若選擇條件相同，也沒有合法調整、其他 Set 或中途 Reset，才進一步追查實作不一致。 || Investigate implementation inconsistency only after ruling out different selectors, permitted adjustment, another Set and intervening reset.')

# These are alternative paths, not a linear sequence. Render each branch with
# its explicit condition instead of drawing an arrow from one branch to another.
VISUALS[3]['branches'] = [1, 2]
VISUALS[113]['branches'] = [1, 2, 3]
VISUALS[277]['branches'] = [0, 1, 2]
VISUALS[226]['branches'] = [3]
VISUALS[299]['branches'] = [3]
