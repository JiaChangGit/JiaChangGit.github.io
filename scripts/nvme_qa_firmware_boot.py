"""Q136–148: download, commit, activation and boot image handling."""
from scripts.nvme_qa_extension import question

def q(n,t,r,b,o=None): question(n,t,'firmware_op',r+['firmware','fwlog','idctrl','fwpel'],b,o)

q(136,'Firmware Slot 的數量、唯讀限制與使用狀態從哪裡查？ || Where are firmware slot count, protection and usage reported?', [], '''
原題只用 Firmware Slot Information 判斷全部能力，需要修正：Log 提供 slot 內容與 Active 狀態，數量及 slot1 是否唯讀則在 Identify.FRMW。 || The original premise needs correction: the log reports contents/activation, while Identify.FRMW reports slot count and slot1 read-only capability.
Firmware slots 由同一 domain 的 controllers 共用；查詢前先確認是哪個 domain 的更新。 || Firmware slots are shared within a domain; identify the update domain first.
OACS 宣告 firmware download/commit 支援；FRMW 宣告 slot 數、slot1 唯讀與無 Reset 啟用能力。 || OACS advertises firmware commands; FRMW reports slot count, slot1 protection and reset-free activation capability.
LID03h 中 CAFS 是目前 Active slot，NAFS 是預定下一次適用 Reset 啟用的 slot；FRS1～7 是各 slot 的 revision。 || LID03h CAFS is current slot, NAFS the pending next-reset slot and FRS1–7 the slot revisions.
先讀 FRMW，再讀 LID03h，選可寫且符合更新計畫的 slot；不要透過嘗試覆寫 slot1 來探測它是否唯讀。 || Read FRMW then LID03h and choose a writable slot; do not probe protection by attempting overwrite.
能分清「存在幾個 slot」、「哪個已有映像」、「目前執行哪個」與「下次準備啟用哪個」。 || Establish count, populated slots, running slot and pending activation separately.
某 slot revision 全為 0 可表示沒有有效映像或不支援，不能只靠 Log 反推 slot 數。非法或唯讀 slot 可回 Invalid Firmware Slot。 || All-zero revision can mean empty or unsupported and cannot establish count; invalid/read-only slots use Invalid Firmware Slot.
Identify.FR 應對應真正執行中的版本，而不是直接取 NAFS 指向的 pending revision。 || Identify.FR reflects the running image, not automatically the pending slot revision.
先查 FRMW，避免把尚未使用的 slot 當成不存在。 || First read FRMW before interpreting an empty slot as nonexistent.
''')

q(137,'Firmware Image Download 如何使用 OFST 與 NUMD？ || How do OFST and NUMD describe firmware download pieces?', [], '''
分段下載讓 Host 不必一次提供完整映像，但每段的位置與長度必須能正確重組。 || Segmentation avoids transferring an entire image at once but requires correct positions and lengths.
OFST 相對於整份待更新映像，不是相對於這一段的 Host buffer。 || OFST is relative to the whole image, not the host buffer for the current piece.
檢查 FWUG 的對齊／粒度限制與 MDTS 等傳輸限制。FWUG 特殊值要依欄位解讀，不能一律當成一般倍數。 || Check FWUG alignment/granularity and applicable transfer limits such as MDTS, honoring FWUG special values.
OFST 以 Dword 為單位；NUMD 為零起算 Dword 數。位元組起點=OFST×4，長度=(NUMD+1)×4。 || OFST counts Dwords and NUMD is zero-based Dword length: byte start=OFST×4 and length=(NUMD+1)×4.
假設每段 4096 bytes，第一段 OFST=0、NUMD=1023，第二段 OFST=1024、NUMD=1023；每段 buffer 都指向該段實際資料。 || For 4096-byte pieces use OFST0/NUMD1023 then OFST1024/NUMD1023 with each pointer addressing that piece.
Download Success 只表示該段下載完成，還沒有 Commit，也沒有啟用新映像。 || Download success completes the piece, not Commit or activation.
不符合 FWUG 時 controller 可回 Invalid Field；重疊範圍可回 Overlapping Range。單位錯誤會同時造成錯誤位移與資料缺口。 || FWUG violations may return Invalid Field and overlaps Overlapping Range; unit mistakes create misplaced data and gaps.
用每段的起點、終點與長度核對完整覆蓋，並與原始映像內容比對。 || Verify complete coverage from each range and compare with the source image.
先查 NUMD 是否少減了 1，OFST 是否誤用 bytes。 || First check the zero-based length and Dword offset units.
''')

q(138,'下載重疊、缺漏、順序與無效 Image 如何處理？ || How are overlap, gaps, order and invalid images handled?', ['boot'], '''
需要區分分段傳輸錯誤與整份映像驗證失敗。每段成功，仍可能因資料缺漏或格式錯誤而不能 Commit。 || Separate segment-transfer errors from whole-image validation; successful pieces can still form an invalid incomplete image.
同一更新流程應只處理一份映像，並使用同一 controller；不要將兩份 firmware 或 Boot Partition 的下載交錯。 || Keep one image per update sequence and use the same controller; avoid interleaving firmware/boot updates.
確認 FWUG、映像需求與支援時的 Multiple Update Detected 能力。 || Check FWUG, image requirements and supported multiple-update detection.
Firmware pieces 可以亂序；Boot Partition pieces 必須由映像開頭依序提交。Overlapping Range 與 MUD 是不同資訊，前者檢查範圍，後者報告更新流程重疊。 || Firmware pieces may arrive out of order; boot pieces must be ordered from the start. Range overlap and MUD sequence-overlap reporting are distinct.
在 Host 建立段落清單，確認無缺口、無重疊且全部成功，再 Commit；一份流程結束後才開始下一份。 || Track ranges and successful transfers, verify no gaps/overlap, Commit, then begin the next image.
有效完整映像應能進入適用 Commit 流程；不能要求每一段都單獨驗證整份映像。 || A valid complete image proceeds through Commit; individual pieces need not validate the complete image.
重疊可回1/14h；Commit 驗證不合法可回1/07h。多個更新流程重疊的結果可能未定義，不能要求固定錯誤碼來補救 Host 違反建議。 || Overlap may use 1/14h and invalid Commit image1/07h. Overlapping update sequences can have undefined results, not a universal recovery status.
保留 Download 範圍與 Commit CQE，區分傳輸完成、資料完整與映像可啟用。 || Preserve ranges and Commit results to separate transfer completion, completeness and activation validity.
先檢查是否把 Boot 的必須依序規則誤套到一般 firmware，或反過來。 || First check whether firmware and boot ordering rules were interchanged.
''')

q(139,'Firmware Commit 的 FS 與 CA 如何選？ || How are Firmware Commit slot and action selected?', [], '''
Commit 可以只保存、安排下次啟用，或立即啟用；選擇取決於更新計畫與裝置能力，不是每次都用同一個 CA。 || Commit can store, schedule or activate immediately, depending on the update plan and capability.
FS 選 firmware slot；Boot 操作用 BPID，不能把 BPID 當成更多的 firmware slots。 || FS selects firmware slots while BPID selects boot partitions.
讀 FRMW、目前 slot、pending slot 與 MTFA，確認無 Reset 啟用是否適合。 || Read FRMW, active/pending slots and MTFA before choosing reset-free activation.
CA0=保存不啟用；CA1=保存並在下次 CLR 啟用；CA2=下次 CLR 啟用既有 slot；CA3=立即啟用。FS=0 讓 controller 選 slot1～7。 || CA0 stores only,1 stores/schedules CLR activation,2 schedules an existing slot and 3 activates immediately. FS0 lets the controller select a slot1–7.
先完成需要的 Download，再送選定的 Commit；如果只啟用既有映像，就不必先下載相同內容。 || Download when needed, then Commit; activating an existing stored image need not redownload it.
CA0 成功不改 running version；CA1／2 需等待適用 Reset；CA3 的 Commit 保持執行中直到啟用成功或失敗。 || CA0 leaves the running version unchanged, CA1/2 await reset and CA3 remains outstanding until activation succeeds or fails.
唯讀／非法 slot 回 Invalid Firmware Slot；非法映像回 Invalid Firmware Image；需更強 Reset 的回覆表示 Commit 已保存但啟用還缺步驟。 || Invalid/read-only slots and images have distinct errors; required-reset statuses can indicate successful storage with activation still pending.
用 CA 解釋 FR、CAFS 與 NAFS 的預期變化，不要求所有 CA 都立即更新 FR。 || Derive FR/CAFS/NAFS expectations from CA rather than demanding immediate FR change for every action.
先查實際 CA，避免把只保存的操作誤判成啟用失敗。 || First inspect CA before diagnosing a store-only operation as activation failure.
''')

q(140,'立即啟用與等待不同 Reset 啟用有何差別？ || How do immediate and reset-triggered activation differ?', ['reset'], '''
立即啟用可保留 controller 操作環境，但映像變更可能要求 Reset 才能安全切換。Host 必須尊重 Commit 指定的 Reset 類型。 || Immediate activation can preserve the operating environment, but image changes may require reset; honor the reported reset type.
啟用影響同一 domain 的 controllers；Reset 本身的範圍可能再涵蓋更多 controller。 || Activation covers the domain, while the chosen reset can have broader scope.
看 FRMW 的無 Reset 啟用能力、MTFA 與 Commit Status；能力支援不保證每一份映像都可立即啟用。 || Check reset-free capability, MTFA and Commit status; capability does not guarantee every image qualifies.
1/0Bh 要 Conventional Reset，1/10h 要 Subsystem Reset，1/11h 要 CLR；1/12h 表示立即啟用需超過 MTFA，映像已 Commit 但未啟用。 || Required resets use 1/0Bh,1/10h and 1/11h;1/12h means activation exceeds MTFA, leaving the image committed but inactive.
CA3 若成功就查新版本；若回要求 Reset，安排對應 Reset 再初始化與查版本。只做較小 Reset 不能滿足明定的較大 Reset 要求。 || After CA3 success check the new revision; otherwise perform the required reset and reinitialize. A narrower reset does not satisfy a stronger requirement.
CA1／2 回 Success 時，任一適用 CLR 方法即可啟用；若特別回要求 Conventional 或 Subsystem Reset，則等待那種類型。 || CA1/2 success allows activation by applicable CLR methods; explicit Conventional/Subsystem requirements narrow the trigger.
例如要求 Conventional Reset 後只清 CC.EN，controller 應繼續執行原映像，不能以 FR 沒變判違規。 || If Conventional Reset was required, clearing CC.EN alone leaves the old image running and unchanged FR is expected.
同時記錄 CA、Status、實際 Reset 來源與恢復後 FR，才能判斷啟用是否符合規範。 || Correlate CA, status, actual reset source and recovered FR.
先查做的是哪種 Reset，而不是只看 Host 介面都叫「reset」。 || First identify the actual reset type rather than the host operation’s generic name.
''')

q(141,'Firmware Activation Starting 何時產生？ || When is Firmware Activation Starting reported?', ['aerfull','aec','cc'], '''
這個事件讓 Host 知道 controller 將進行不經 Reset 的韌體啟用，可能暫停處理；它不是啟用已成功的通知。 || The event announces reset-free activation and possible processing pause, not successful completion.
受新映像影響的 controllers 各自依通知設定回報，並不只限於提交 Commit 的 controller。 || Affected controllers report according to their notification settings, not solely the Commit recipient.
確認 Firmware Activation Notices 已啟用、AER 已掛入，以及 FRMW／MTFA 等啟用資訊。 || Check enabled activation notices, posted AERs and activation capabilities/timing.
AER 的 Notice 類型、Firmware Activation Starting 資訊及 LID03h 引導 Host 查 slot；CSTS.PP 表示處理暫停狀態。 || The Notice event points to LID03h; CSTS.PP reports processing pause.
Commit CA3 開始啟用時處理通知，依 PP 觀察恢復，再查 Commit 結果與 FR。不要在收到 Starting 後立即把新版本列為成功。 || Handle the event at activation start, observe processing recovery, then check Commit and FR.
成功證據是適用 Commit 完成與實際 running revision；Starting 只證明已開始相應流程。 || Success requires the relevant completion and running revision; Starting establishes initiation only.
沒有啟用通知或沒有可完成的 AER 時，不能期待同樣的即時 CQE。載入失敗則另有 Firmware Image Load Error。 || Disabled notices or unavailable AERs alter notification observation; load failure has its own error event.
比較事件時間、PP 與 Commit 完成，辨別真正卡住與 Host 尚未處理通知。 || Correlate event timing, PP and completion to distinguish activation stalls from unhandled notifications.
先查 AEC 的 Firmware Activation Notices，而不是只看是否送過任意 AER。 || First check the activation-notice configuration, not merely whether an AER was submitted.
''')

q(142,'Download、Commit 或 Activation 中發生 Reset／斷電如何處理？ || How are firmware-update interruptions recovered?', ['reset'], '''
更新有暫存下載、保存到 slot、啟用三個階段，各自的持久性不同；復原時先定位中斷在哪一階段。 || Staging, committing and activation have different persistence; identify the interruption stage first.
保存與啟用的範圍是 domain；中斷也可能讓所有共享 controllers 同時失去通訊。 || Storage and activation are domain-wide and interruption can affect its shared controllers.
保存最後完成的 Download／Commit、CA、FS、FR 及 slot Log，恢復後再次讀取。 || Preserve last completed transfers/Commit, CA/FS and revision/slot snapshots, then reread after recovery.
CLR 發生在 Download 與 Commit 完成之間時，controller 必須丟棄下載部分。啟用 Commit 期間進入 D3cold，恢復可使用原映像或新映像。 || CLR between download and completed Commit discards staging; D3cold during activation Commit may resume with old or new firmware.
恢復通道後查實際版本與 slot；未完成 Commit 的映像重新下載，不從原暫存 offset 自行續傳。 || Recover, inspect running/stored revisions and redownload uncommitted staging rather than assuming resumable offsets.
已知目前執行版本、pending 狀態與可用能力後，才能決定重試、重新 Commit 或已完成。 || Decide completion/retry/recommit only after identifying running revision, pending state and capabilities.
沒有 CQE 時不能補造成功或失敗碼。新版本未啟用可能是合法保留原版本，而不是必然毀損。 || Do not invent status for a lost CQE; retaining old firmware can be a valid interrupted-activation outcome.
使用 PEL Commit 與 Reset Event 補足歷史，但 NFR 只記要求版本，仍須與 FR 比對。 || Use Commit/Reset PEL history but compare requested NFR with actual FR.
先查最後一筆真正完成的 Commit，而不是最後一段已下載的資料。 || First identify the last completed Commit rather than the last downloaded piece.
''')

q(143,'Firmware 載入失敗後如何回復？ || How does firmware-load failure recovery work?', ['aerfull'], '''
裝置需要在新映像無法載入時恢復可運作映像，但可回復到什麼內容仍取決於先前有效 slot 或 baseline 是否存在。 || Recovery depends on available previously activated or baseline images when a new image cannot load.
失敗與回復影響該映像涵蓋的 controllers；不應以單一 slot 的內容推論整個更新歷史。 || Recovery affects controllers using the image; one slot alone does not describe full history.
查 FR、CAFS／NAFS、各 slot revision、Firmware Image Load Error 與 PEL。 || Check FR, active/pending slots, revisions, load-error events and PEL.
新映像無法載入時，controller 必須回復至最近已啟用 slot 的映像，或可用的 baseline 唯讀映像，並回報 Firmware Image Load Error。 || On load failure, revert to the most recently activated slot image or available read-only baseline and report Firmware Image Load Error.
恢復後讀實際 FR，確認是否回到可用映像，再檢查失敗的 Commit／activation 狀態；不要立即反覆啟用同一失敗映像。 || Read recovered FR and failure evidence before attempting the same image again.
controller 可恢復舊版本運作，同時保留更新失敗的證據；舊版本運作不表示前次更新成功。 || Running old firmware can demonstrate recovery while the attempted update remains failed.
如果 Host 已覆寫 Active slot，舊映像可能不再存在，因此不能保證永遠回到某個特定歷史版本。 || Overwriting the active slot may remove the prior image; no guarantee exists of returning to any chosen historical revision.
核對實際 slot 內容與可用 baseline，避免測試把不存在的舊映像當成必須回復的對象。 || Compare actual slot/baseline availability rather than demanding rollback to unavailable content.
先查 Active slot 是否曾被覆寫，這會直接影響可回復映像。 || First check whether the active slot was overwritten.
''')

q(144,'Activation 後如何確認版本、Slot 與 Command Effects？ || How is completed activation verified?', ['commandseffects'], '''
啟用完成後可能改變能力與命令效果，Host 必須更新快取，不能只看版本字串就沿用所有舊設定假設。 || Activation can change capabilities/effects; refresh caches rather than relying solely on revision text.
查詢涵蓋受影響 domain 的 controller 與 namespaces，並保留相同身分以便前後比較。 || Compare the same affected controller/domain and namespace identities before and after.
讀 Identify.FR、FRMW、CAP、Firmware Slot Information，並重新取得適用 CSI 的 Commands Supported and Effects。 || Read FR/FRMW/CAP, slot information and relevant-CSI Commands Supported and Effects.
CAFS 表示現行 slot，NAFS 表示待啟用安排，FR 是 running revision；Effects 的 CSUPP／CCC／NCC／NIC 等說明支援及可能影響。 || CAFS identifies current slot, NAFS pending activation and FR running revision; Effects reports support and possible capability/inventory changes.
先確認啟用真的完成，再重新查能力，最後依新宣告重新驗證需要使用的命令與格式。 || Establish activation completion, refresh capability and validate required commands/formats.
FR、目前 slot revision 與啟用結果應能互相解釋；pending slot 尚未啟用時，不應要求 FR 提前更新。 || Running revision, active slot and activation outcome should agree; pending activation does not require early FR changes.
查詢失敗先看 Ready／media 限制與新能力，不直接判定映像損壞。 || Diagnose readiness/media restrictions and new capability before declaring image corruption.
比較有效欄位與真正變更，避免把保留欄位或不適用 CSI 的資料列當成不一致。 || Compare applicable fields and CSI rather than reserved or unrelated structures.
先排除 Host 使用舊 Identify／Effects buffer 的快取問題。 || First exclude stale Identify/effects buffers.
''')

q(145,'Activation 後哪些設定應保留，哪些需要重新探索？ || What should persist or be rediscovered after activation?', ['feature','reset','uuid','idns'], '''
不能要求整份 Identify、Feature 與所有 bytes 都不變。韌體可更新能力；但使用者資料、namespace 配置及各功能的持久性仍需遵守其規則。 || Do not require every byte to remain unchanged: capability can evolve while data/configuration obey their persistence rules.
先區分不經 Reset 的啟用與實際執行 Reset；後者會另外觸發 queue、Feature 與 Register 的重設規則。 || Separate reset-free activation from actual reset, which independently changes queues, features and registers.
比較 Feature 的 Saved／Current／持續性、namespace 身分／attachment，以及新 Identify 能力與 UUID List。 || Compare feature saved/current/persistence, namespace identity/attachment, capabilities and UUID list.
FR 預期反映 running image；Current Feature 不可僅依版本字串推論。UUID slot 的不相容變更可能要求 Reset，避免舊 UUID Index 指向另一個意思。 || FR identifies the image, not feature restoration. Incompatible UUID-slot changes can require reset to avoid reinterpreting old indices.
建立更新前基準，記錄 CA 與實際 Reset，更新後按每項功能的保留規則分類比對，再重新配置必要的 Host 狀態。 || Snapshot before update, record activation/reset path, compare each function’s persistence and restore required host state.
結果應符合所執行的更新與 Reset 路徑；正常能力變更與不應遺失的資料／配置要分開驗證。 || Validate the actual activation/reset path, distinguishing permitted capability changes from improper data/configuration loss.
不能只用「版本變了所以全部可重設」合理化遺失；也不能用「只是更新」要求 I/O queues 跨真正 Reset 有效。 || Firmware change does not justify arbitrary loss, nor does updating preserve queues across a real reset.
把差異逐項對應來源要求，記錄新能力、應保留值及必須重建值。 || Map differences to requirements: changed capability, retained values and rebuilt state.
先確認是否真的發生 CLR，再判斷 Feature 與 queue 的預期。 || First establish whether CLR occurred before setting persistence expectations.
''')

q(146,'Boot Partition 支援、狀態與 Active ID 如何確認？ || How are boot partition support, state and active ID discovered?', ['boot','bootreg','bootlog','bootprotect'], '''
Boot Partition 可讓 Host 在建立 queue 或啟用 controller 前，透過簡化介面讀取開機映像。它不是一般 namespace 的 LBA 區間。 || Boot partitions provide pre-queue/pre-enable image access through a simplified interface, not ordinary namespace LBAs.
支援時有兩個等大的 partitions，ID=0／1；多個 controllers 可能共用它們。 || Supported controllers expose two equal partitions, IDs0/1, potentially shared across controllers.
先讀 CAP.BPS，再讀 BPINFO 的 ABPID、BPSZ、BRS；保護能力看 Identify.BPC，支援時也可讀 Boot Partition Log15h。 || Read CAP.BPS and BPINFO.ABPID/BPSZ/BRS, Identify.BPC for protection and supported LID15h for log access.
BPMBL 提供 Host buffer 位址，BPRSEL 指定 BPID、讀取 offset 與大小；BPINFO.BRS 回報進行中、成功或錯誤。 || BPMBL supplies buffer address, BPRSEL selects partition/range and BRS reports transfer state.
配置實體連續 buffer，確認沒有讀取進行中，設定位址與讀取選擇，再等待 BRS 完成。讀取中不得 Reset、Shutdown 或變更相關傳輸屬性。 || Allocate contiguous memory, ensure no read is active, configure address/selection and wait for BRS; do not reset/shutdown/change transport properties during the read.
BRS=10b 表示要求內容已傳到 buffer；11b 表示傳輸錯誤。這個 Register 讀取流程沒有 NVMe CQE。 || BRS10b indicates transferred data and 11b transfer error; the register-based flow has no NVMe CQE.
不要為 BPRSEL 寫入指定 Invalid Field CQE。Log 路徑才按 Get Log Page 的參數與完成規則判讀。 || Do not invent Invalid Field CQEs for BPRSEL writes; the log path separately follows Get Log completion rules.
將 CAP、ABPID、size、BRS 與實際讀回內容一起確認，不能只靠 ABPID 就宣告映像有效。 || Verify capability, selected active ID, size, status and content; ABPID alone does not validate the image.
先確認使用 Register 還是 Log 讀取介面，避免混用 offset、完成與錯誤表示。 || First distinguish register and log interfaces before applying offset/completion semantics.
''', {8:'Register 讀取流程沒有 CQE，因此沒有 DNR／More；若使用 LID15h 則解讀該 Get Log Page 的 CQE。 || The register path has no DNR/More; LID15h uses its Get Log Page CQE.',9:'Boot Partition Register 讀取不定義成功 AER。使用 Log 也不因讀取成功就產生 Firmware Activation Starting。 || Boot register reads have no success AER; log-read success does not trigger Firmware Activation Starting.',11:'一般 Boot 讀取不是 Firmware Commit Event；只有另行完成 Commit 時才依 PEL 規則記錄。 || Ordinary boot reads are not Firmware Commit events; actual Commit completion follows PEL rules.'})

q(147,'Boot Partition 如何下載、提交與切換 Active？ || How are boot images downloaded, committed and selected?', ['boot','bootprotect','bootreg'], '''
兩個 partitions 讓 Host 可以先更新非 Active 的一份，讀回確認後才切換，減少中斷更新造成不可用開機映像的風險。 || Two partitions allow updating and verifying the inactive image before selection, reducing interrupted-update risk.
BPID 指定要寫入或標為 Active 的 partition；保護狀態必須由所有共享它的 controllers 一致執行。 || BPID selects the written/activated partition, with protection enforced by all sharing controllers.
確認 CAP.BPS、BPC、目前 ABPID 與有效保護機制；FID85h 與 RPMB 不一定同時掌控狀態。 || Check BPS/BPC, ABPID and the active protection mechanism; FID85h and RPMB do not simultaneously control protection.
先用 Firmware Image Download 依序送整份映像；Commit CA6 寫入 BPID，CA7 才標為 Active 並更新 ABPID。 || Download in order; CommitCA6 replaces the selected partition and CA7 selects it active.
完成下載，解除目標寫入鎖定，CA6 提交，讀回驗證，CA7 切換，最後恢復合適的寫入保護。 || Download, unlock target, commitCA6, verify, selectCA7 and restore protection.
CA6 成功表示寫入該 partition；不代表 ABPID 已切換。CA7 成功後再確認 ABPID。 || CA6 success writes the partition without necessarily changing ABPID; verify ABPID after CA7.
被鎖定而嘗試改寫時回 Boot Partition Write Prohibited。寫入中 Reset／斷電可能留下新舊混合內容，不能直接標為 Active。 || Locked writes use Boot Partition Write Prohibited; reset/power interruption can leave mixed contents requiring verification before activation.
分別比較下載內容、讀回內容及 ABPID，避免「切換成功」掩蓋「映像內容錯誤」。 || Compare downloaded/readback content and ABPID separately.
先查是否只做了 CA6，卻期待 ABPID 自動改變。 || First check whether onlyCA6 was performed while expecting automatic active selection.
''', {9:'Boot Partition CA6／CA7 不等同 controller firmware activation，因此不能要求 Firmware Activation Starting。若另有錯誤事件，依其本身條件處理。 || BootCA6/CA7 are not controller-firmware activation and do not require Firmware Activation Starting.',12:'CLR 會丟棄未 Commit 的下載；Boot 寫入中重設可能留下舊、新或混合內容，恢復後必須驗證再決定是否切換。 || CLR discards uncommitted staging; interrupted boot commit can leave old/new/mixed content and needs verification.',13:'Subsystem Reset 中斷 Boot Commit 也不能視為原子回復；恢復後查 Active ID、保護狀態與實際內容。 || Subsystem-reset interruption does not guarantee atomic rollback; inspect active ID, protection and content.',14:'Boot Commit 中斷電可留下混合內容。Set Features 保護機制的 Power Cycle 會回到 Write Locked；不要把解鎖狀態當成跨斷電不變。 || Power loss during boot commit can leave mixed content; the Set Features protection mechanism returns to Write Locked on a power cycle.',15:'Boot partitions 可由多個 controllers 共用；更新與保護需要在所有共享者之間協調，不能只鎖住一條 Host 路徑。 || Shared boot partitions require coordinated update/protection across all sharing controllers.'})

q(148,'Boot Partition 更新與 Controller Firmware 更新有何不同？ || How do boot and controller-firmware updates differ?', ['boot','bootprotect'], '''
Boot Partition 保存供 Host 開機使用的映像；controller firmware 是 SSD controller 執行的程式。共用下載命令，不代表用途、順序與啟用方式相同。 || Boot images are for host booting; controller firmware runs the SSD. Shared download commands do not imply shared semantics.
Boot 用 BPID0／1；firmware 用 slots1～7 與 domain 範圍。兩者不是同一份儲存清單。 || Boot uses IDs0/1; firmware uses slots1–7 within a domain.
Boot 看 CAP.BPS／BPC／BPINFO；firmware 看 OACS／FRMW／MTFA 與 LID03h。 || Boot discovery uses BPS/BPC/BPINFO; firmware uses OACS/FRMW/MTFA and LID03h.
Firmware Download 可亂序，CA0～3 管理保存與啟用；Boot Download 必須依序，CA6／7 管理替換與 Active ID。 || Firmware download may be out of order withCA0–3; boot download is ordered withCA6/7.
先決定更新對象，再選對能力、下載順序、Commit Action 與驗證方法。不要交錯兩種更新流程。 || Identify the target before selecting capabilities, order, action and verification; do not interleave update sequences.
Firmware 成功以 running FR／slot 驗證；Boot 成功以內容及 ABPID 驗證。更新 Boot 不要求 Identify.FR 改變。 || Verify firmware via running revision/slot and boot via content/ABPID; boot update does not require FR to change.
Boot Commit 斷電可能混合新舊內容；Firmware load failure 有回復映像的規則。不能將其中一套保證套到另一套。 || Interrupted boot commits can mix contents; firmware load failure has image fallback rules. Do not transfer guarantees between them.
測試報告按對象記錄狀態與持久性，避免把 CA7 的 Active 與 firmware CAFS 混為一談。 || Record target-specific state/persistence rather than conflating boot Active selection with firmware CAFS.
先問「這份映像由 Host 開機使用，還是由 SSD controller 執行」，再查正確介面。 || First determine whether the host boots from the image or the SSD controller executes it.
''')
