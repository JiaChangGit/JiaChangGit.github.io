"""Q118–135: formatting, sanitization targets and observable outcomes."""
from scripts.nvme_qa_extension import question

def f(n,t,r,b,o=None): question(n,t,'format_op',r+['format','nvmformat','formatpel'],b,o)
def s(n,t,r,b,o=None): question(n,t,'sanitize_op',r+['sanitizecmd','sanitizelog','sanitizestate','sanitizepel'],b,o)

f(118,'如何確認 Format 與 Sanitize 支援能力？ || How are Format and Sanitize capabilities established?', ['idctrl','commandseffects','sanitizecmd'], '''
支援 Opcode、支援某種操作，以及當前允許執行，是三個要分開確認的問題。這能避免把「支援 Sanitize」誤讀成任何清除方法都可使用。 || Opcode support, supported action and current permission are distinct; Sanitize support does not enable every erasure method.
Format 的範圍由 FNA、SES 與 NSID 決定；Sanitize 和 Sanitize Namespace 則是不同命令、不同清除目標。 || Format scope depends on FNA, SES and NSID; subsystem and namespace sanitization use distinct commands and targets.
Format 看 OACS 與 FNA；Sanitize 看 SANICAP 的 CES、BES、OWS 及 namespace 支援欄位，再用 Commands Supported and Effects 的 CSUPP 交叉確認。 || Check OACS/FNA for Format and SANICAP CES/BES/OWS plus namespace capability for sanitization; cross-check CSUPP.
Format NVM Opcode=80h，Sanitize=84h，Sanitize Namespace=8Ch。SANICAP 的 subsystem Overwrite 能力不等於 namespace Overwrite 能力。 || Opcodes are Format80h, Sanitize84h and Sanitize Namespace8Ch. Subsystem overwrite capability does not enable namespace overwrite.
先讀能力與目前 namespace 格式，再確認保護、pending activation、清除狀態等前提，最後選擇合法操作；不要用破壞性命令試探能力。 || Read capabilities and format, check protection, pending activation and sanitize state, then select a valid action rather than probing support destructively.
一致的能力宣告應能配合合法命令行為；但命令因當前狀態被拒絕，不必然表示支援宣告錯誤。 || Advertised support must agree with valid command behavior, while state-dependent rejection need not contradict support.
不支援 Opcode 與支援命令但不支援 SANACT 要分開；後者應回 Invalid Field in Command。 || Distinguish unsupported opcode from unsupported SANACT in a supported command; the latter uses Invalid Field.
把能力、Command Effects、參數與當前狀態放在一起檢查，才有足夠證據判斷符合性。 || Evaluate capability, effects, parameters and current state together for compliance.
先確認使用的是 84h 還是 8Ch，避免把兩種命令的欄位套在一起。 || First identify opcode84h versus8Ch before applying its field definitions.
''')

f(119,'Format、Secure Erase、Subsystem Sanitize 與 Namespace Sanitize 有何差別？ || How do Format, secure erase and the two sanitize targets differ?', ['sanitizecmd','sanitizestate','nvmsanitize'], '''
Format 用於改變媒體格式，也可要求 Secure Erase；Sanitize 則以清除目標中的使用者資料為主，不是一般的格式切換。 || Format changes media format and can request secure erase; Sanitize removes target user data rather than serving as an ordinary format change.
Format 依 FNA／SES／NSID 選範圍；Subsystem Sanitize 包含其規定的全部使用者資料位置；Namespace Sanitize 只清除指定 namespace 的資料範圍。 || Format scope is selected by FNA/SES/NSID; subsystem sanitize covers its defined user-data locations and namespace sanitize its selected target.
檢查 OACS、FNA、SANICAP、namespace 狀態及支援的格式。不能只看到「Crypto Erase」同名，就省略命令範圍差異。 || Check OACS, FNA, SANICAP, namespace state and formats; the shared name Crypto Erase does not imply identical command scope.
Format 的 SES=0 不要求 Secure Erase，1 為 User Data Erase，2 為 Cryptographic Erase。Sanitize 的 SANACT 另行選擇方法；Namespace Sanitize 只支援 Crypto Erase。 || Format SES0 omits secure erase,1 requests user-data erase and 2 cryptographic erase. Sanitize uses SANACT; namespace sanitization only supports Crypto Erase.
先回答要改格式、清除哪個範圍、是否需要指定清除方法，再選命令。所有 namespace 各做一次 Sanitize，也不等於 subsystem 的全部使用者資料位置都已處理。 || Choose based on format change, target and required method. Sanitizing each namespace is not equivalent to covering every subsystem user-data location.
Format CQE 在格式化完成後回傳；Sanitize 啟動成功後仍以背景方式進行，要另查 LID81h。 || Format completion follows media formatting; successful Sanitize initiation still requires LID81h monitoring.
不合法格式使用 Invalid Format；不支援 SANACT 使用 Invalid Field。各命令的拒絕條件不能互相套用。 || Invalid formats and unsupported SANACT use their separate statuses, Invalid Format and Invalid Field.
例如需要改成 4 KiB LBA，應選 Format；需要清除整個 subsystem，不能只指定一個 namespace 然後把 NDE 當 GDE。 || Use Format to select 4 KiB LBAs; erasing one namespace and observing NDE does not establish subsystem GDE.
先檢查需求中的「清乾淨」究竟指一個 namespace，還是 subsystem 的完整清除範圍。 || First clarify whether the erasure target is one namespace or the full subsystem scope.
''')

f(120,'Format 如何選 LBA Format、Metadata、PI 與 SES？ || How are Format data format, metadata, PI and SES selected?', ['idns','behavior'], '''
格式選擇決定後續 I/O 的資料長度與 metadata 位置。選錯會讓 Read／Write 的 buffer 與保護資訊不符合 namespace 的格式。 || Format selection determines I/O data and metadata layout; mismatches invalidate subsequent buffers and protection information.
設定適用於 Format 所涵蓋的 namespaces，不是只在這一筆命令中暫時使用。 || The selection configures namespaces in the format scope rather than only this command’s transfer.
讀 Identify Namespace 的 LBAF／FLBAS、MC、DPC、DPS，以及需要時的 NVM 特定格式擴充；確認 Host Behavior Support.LBAFEE。 || Read LBAF/FLBAS, MC, DPC, DPS and applicable NVM format extensions, plus LBAFEE.
CDW10 的 LBAFL 與有效時的 LBAFU 組成格式索引；MSET 選 extended LBA 或獨立 metadata buffer；PI 選 0～3；本版 NVM PIL 必須為 0。SES 另決定是否 Secure Erase。 || LBAFL plus enabled LBAFU select format; MSET selects extended or separate metadata, PI selects0–3, and current NVM PIL must be0. SES independently selects secure erase.
選定一個已宣告的格式，確認 metadata 與 PI 能力，再組合欄位。假設 LBAF2 是 4096-byte data＋16-byte metadata，MSET=1 時每個 extended LBA 傳輸長度是 4112 bytes。 || Select an advertised format and verify metadata/PI compatibility. For hypothetical LBAF2 with 4096+16 bytes, MSET=1 gives4112 bytes per extended LBA.
成功後 FLBAS／DPS 應反映設定；logical block 大小改變時，NSZE／NCAP 可能改變，應重新讀取。 || On success FLBAS/DPS reflect the selection; changed logical-block size can alter NSZE/NCAP, requiring fresh reads.
未支援格式回 Invalid Format；未啟用必要 LBAFEE 的格式回 Invalid Namespace or Format。共享 FDP RUH 還須符合共同格式限制。 || Unsupported formats use Invalid Format; formats disabled by missing LBAFEE use Invalid Namespace or Format. Shared FDP RUHs impose matching-format constraints.
用新格式重算 I/O data／metadata 長度，不要沿用 Format 前的 buffer 設定。 || Recalculate I/O data/metadata lengths rather than retaining the pre-format layout.
先查格式索引的上、下位元與 LBAFEE 是否一致，再查 MSET／PI 組合。 || First check index upper/lower bits and LBAFEE, then MSET/PI compatibility.
''')

f(121,'Format 的非法格式、參數與狀態如何回報？ || How are invalid Format parameters and states reported?', ['status','nwp','idctrl'], '''
拒絕原因可能是格式不存在、Host 未啟用格式、namespace 受保護，或與其他操作衝突。不同原因需要不同修正。 || Rejection can result from unsupported/disabled formats, protection or conflicting operations, requiring different fixes.
先計算 Format 的完整範圍，再查其中每個 namespace；只要範圍內有寫入保護，就不能只看提交時指定的 namespace 是否可寫。 || Compute full format scope before checking protection across all affected namespaces.
用 LBAF、LBAFEE、FNA、Write Protection 狀態，以及現有 I/O／Admin 操作確認前提。 || Establish preconditions through LBAF, LBAFEE, FNA, protection and concurrent operations.
Invalid Format=1/0Ah；Invalid Namespace or Format=0/0Bh；Namespace is Write Protected=0/20h；Command Sequence Error=0/0Ch；Format In Progress=0/84h。 || Relevant codes are 1/0Ah,0/0Bh,0/20h,0/0Ch and 0/84h respectively.
負向測試一次製造一項問題。例如測不支援 LBAF，先確保 NSID 合法、未受保護、沒有其他操作衝突。 || Isolate one defect per negative test, keeping NSID, protection and concurrency valid for an unsupported-LBAF test.
正確拒絕不等於格式已改變；讀回設定以確認未將失敗命令錯當成成功操作。 || Rejection does not establish a format change; re-read configuration rather than treating failure as successful execution.
Format 影響的 namespace 尚有 I/O 時，controller 可中止 Format；若因此中止，應回 Command Sequence Error。這裡的「可」不能改寫成每次都必須拒絕。 || With I/O being processed for an affected namespace, Format may be aborted, using Command Sequence Error if aborted for that reason; rejection is not universally mandatory.
測試需分清 shall、should、may，以及同時多錯誤時的 Status 選擇自由。 || Tests must distinguish shall/should/may and permitted selection among simultaneous errors.
先看是否同時觸發保護與非法格式，導致精確 Status 斷言沒有唯一答案。 || First check whether multiple defects make an exact-status assertion ambiguous.
''')

f(122,'Format 期間哪些 Admin 操作可以繼續？ || Which Admin operations can continue during Format?', ['sanitizerestrict'], '''
Host 仍需要查詢狀態、維持通知與管理 queue，所以 Format 期間不應一概封鎖全部 Admin 命令。 || Hosts still need status, notifications and queue management; Format does not universally block all Admin commands.
限制取決於操作是否影響正在 Format 的 namespace，以及 Figure144 對命令或 Log 的附加條件。 || Restrictions depend on affected namespaces and Figure144 command/log conditions.
先確認命令本身受支援，再查 Format 期間的允許清單；列在允許清單不會讓選配功能自動變成支援。 || Establish support first; the allowed-during-Format list does not enable unsupported optional commands.
常見允許項包含 Abort、AER、queue 建立／刪除、Identify、Get Features、Get Log Page 的指定 LID 及 Keep Alive。Set Features 中的 Namespace Write Protection Config 不允許。 || Examples include Abort, AER, queue management, Identify, Get Features, selected logs and Keep Alive; Namespace Write Protection Config is excluded from allowed Set Features.
以 Figure144 逐項檢查。Error Information 的 LBA 回 0；Self-test 僅 Controller DST 建議允許；不能由「Get Log Page 允許」推論所有 LID 都允許。 || Apply Figure144 per entry: error-log LBA returns zero and only Controller DST should be allowed. Get Log permission does not extend to every LID.
允許的查詢回目前狀態，不表示 Format 已完成。Format 的 CQE 或完整結果證據仍要另外確認。 || Permitted queries return state without establishing Format completion.
未列出的 Admin 若影響被 Format 的 namespace，可中止；因這項理由中止時，建議回 Format In Progress。反向的操作衝突則可能使 Format 回 Command Sequence Error。 || Unlisted Admin commands affecting the target may be aborted and should use Format In Progress for that reason; preexisting conflicting Admin work can instead cause Format sequence error.
分別驗證命令允許性、LID 限制與回傳欄位，不用一筆 Get Log 成功概括全部管理操作。 || Verify command permission, LID restrictions and returned fields separately.
先查 Figure144 的附加限制欄，尤其所查的 LID 是否真的列入。 || First inspect Figure144's additional restrictions for the specific LID.
''')

f(123,'Format 過程遇到 Reset 或斷電，如何判斷結果？ || How is interrupted Format assessed after reset or power loss?', ['reset','idns'], '''
失去 CQE 代表 Host 不知道結果，不等於操作必定沒做，也不等於已成功。恢復後應以現況與事件證據重新建立判斷。 || Lost completion means unknown outcome, not guaranteed non-execution or success; reconstruct it from current state and events.
檢查原 Format 範圍內所有 namespaces，以及其他 controller 對共享 namespace 的存取狀態。 || Inspect all originally affected namespaces and their access through other controllers.
讀 Identify Namespace 的 FLBAS、DPS、NSZE／NCAP、支援時的 FPI，及 PEL Format Completion。 || Read FLBAS, DPS, NSZE/NCAP, supported FPI and PEL Format Completion.
Format Completion Event 的 FNVMS 說明格式化結果，INFO 保存曾回報的 Status；沒有 CQE 時 INFO=0 不能當成功。 || FNVMS describes formatting outcome while INFO records a reported status; INFO=0 without a CQE is not proof of success.
先恢復 controller 與 Admin Queue，再保存事件、讀回新格式、確認可用性；若仍無法確定操作完成，就不要直接以舊格式恢復 I/O。 || Recover access, preserve events and re-read format/usability before resuming I/O; do not assume the old format when completion remains uncertain.
可以確認目前格式與完成狀態後，Host 才配置對應 buffer 與 PI。若需重新 Format，先依目前能力與範圍建立新命令。 || Configure buffers/PI after establishing current format and completion; any new Format must use current capability and scope.
Reset 不保證原資料可復原，Power Cycle 也不是撤銷 Format 的方法；未收到成功不代表舊資料安全。 || Reset/power cycle do not roll back Format or guarantee old-data survival.
把 Reset 之前最後可信的事件與恢復後第一份快照連起來，標示中間不可觀察的期間。 || Link the last trustworthy pre-reset evidence to the first recovered snapshot and mark the observation gap.
先查是否有可信的 Format 成功 CQE；若沒有，避免直接用 INFO=0 補出成功結論。 || First establish whether a trustworthy Format success CQE exists; do not infer it solely from INFO=0.
''')

f(124,'Format 成功後哪些 Identify 與 Namespace 狀態要更新？ || Which namespace data must be refreshed after Format?', ['idns','nvmformat','changedlog'], '''
Format 改變後續 I/O 的解讀方式，因此 Host 必須更新快取的 namespace 資訊，避免用舊 LBA 大小或 PI 設定讀寫。 || Format changes I/O interpretation, requiring refreshed namespace caches rather than old block/PI settings.
更新的是受影響 namespace 的格式及相關容量；Format 不等同 Create／Delete，不能預設一定產生新 NSID。 || Refresh format and capacity for affected namespaces; Format is not namespace creation/deletion and does not inherently assign a new NSID.
查 Identify Namespace 與必要的 NVM 特定結構，確認 FLBAS、DPS、LBAF、NSZE、NCAP 與 FPI。 || Query namespace and NVM-specific structures for FLBAS, DPS, LBAF, NSZE, NCAP and FPI.
FLBAS 表示使用中的格式及 metadata 傳輸方式；DPS 表示 PI 設定；NSZE／NCAP 以新的 logical block 為單位。 || FLBAS reports active format/metadata transfer, DPS protection settings and NSZE/NCAP counts in new logical blocks.
等待 Format 成功 CQE，重新 Identify，再依新格式重算 LBA 範圍與 buffer 大小；有共享存取者時同步更新它們的配置。 || Wait for Format success, refresh Identify and recalculate address/buffer layout, coordinating other accessors.
設定讀回應與命令要求一致；若 block 大小改變，NSZE／NCAP 可能不同，不能用「數字必須完全不變」驗證容量。 || Readback must reflect the request; block-size changes can change counts, so identical counts are not a valid universal capacity test.
若成功 CQE 後仍回舊格式，先排除讀錯 NSID、讀到快取或命令範圍誤判，再確認不一致。 || For old-format readback after success, exclude wrong namespace, stale caching and mistaken scope.
例如同一容量從 512-byte 改為 4096-byte LBA，應比較以 bytes 表示的容量及允許變化，而不是只比較 block 數。 || When changing512-byte to 4096-byte LBAs, compare byte capacity under allowed behavior rather than block counts alone.
先檢查 Host 是否真的重新送出 Identify，而非讀取 Format 前留下的 buffer。 || First confirm a fresh Identify was issued instead of reading a pre-format buffer.
''')

f(125,'Format 失敗時如何使用 CQE、Error Log 與 PEL？ || How are Format failures checked using CQE, Error Log and PEL?', ['error','status'], '''
先區分命令因參數被拒絕，與格式化已開始後失敗；後者可能已改變資料，不能當成完全沒有執行。 || Distinguish validation rejection from failure after formatting began, which may already have changed data.
證據需對應同一筆 Format 及同一範圍；其他 namespace 的事件不能當成這筆命令的結果。 || Evidence must match the same Format and scope, not a neighboring namespace operation.
保存 CQE 的 SCT／SC／M／DNR，及 PEL 支援與事件有效性。 || Preserve SCT/SC/M/DNR and PEL support/validity.
Error Log 用 SQID／CID／ECNT 關聯；Format Start 保存參數，Completion 的 FNVMS／INFO 記錄結果與曾回報狀態。 || Correlate Error Log by IDs/count; Format Start preserves parameters and Completion carries FNVMS/INFO.
先讀原 CQE，再依 M 取得補充資訊，最後以 PEL 與 Identify 現況補足過程。缺少某種記錄時先確認其要求，不硬湊三份一對一證據。 || Read the CQE, additional information indicated by M, then PEL/current Identify; do not force one-to-one entries across all sources.
能說明失敗原因及目前是否可用，就是有效診斷。若結果仍不確定，保留不確定性而不是假設格式化回復。 || A diagnosis establishes failure cause and current usability; retain uncertainty rather than assuming rollback.
Multiple errors 可能有不同合法 Status；INFO=0 也可能只是沒有 CQE，不可以忽略 FNVMS。 || Simultaneous faults may permit different statuses; INFO=0 can mean no CQE, requiring FNVMS interpretation.
把命令參數、結果與目前格式比對，檢查是否有「回報成功但格式不符」或「失敗卻被 Host 視為成功」的矛盾。 || Compare parameters, result and current format to detect inconsistent controller or host interpretation.
先看 Format 是否已進入執行階段，以及 PEL 是否存在相符的 Start／Completion。 || First establish whether execution began and whether corresponding Start/Completion events exist.
''')

s(126,'SANICAP 如何表示 Block Erase、Overwrite 與 Crypto Erase？ || How does SANICAP advertise sanitize methods?', ['idctrl'], '''
SANICAP 告訴 Host 哪些清除方法可用，以及 No-Deallocate、驗證等延伸能力。它不是「非零就所有方法皆可用」的布林值。 || SANICAP advertises individual methods and extensions, not a Boolean enabling every sanitize action.
CES、BES、OWS 對應 subsystem 清除方法；namespace 清除另有能力宣告，且本版只定義 Crypto Erase。 || CES/BES/OWS advertise subsystem methods; namespace sanitization has separate support and only Crypto Erase in this revision.
讀 Identify Controller.SANICAP，並交叉查 Command Effects 中的 84h／8Ch 與 LID81h 支援。 || Read SANICAP and cross-check opcodes84h/8Ch and LID81h support.
CES、BES、OWS 分別為 Crypto Erase、Block Erase、Overwrite 支援位元；NODAS／NDI 相關能力決定 NDAS 的意義，VERS／NVERS 則分別控制兩種目標的 Media Verification。 || CES/BES/OWS select method support; no-deallocate attributes govern NDAS and VERS/NVERS govern verification for the two target types.
把需求的方法對到它的能力位元，再選對 SANACT。假設只有 BES=1，就選 subsystem Block Erase，不能改用 Overwrite。 || Match the required method to its bit before SANACT selection; BES alone does not authorize Overwrite.
合法啟動回 Success，且對應 Sanitize Status 已更新；能力支援不保證每次背景清除都能成功。 || Valid initiation succeeds with status updated; supported capability does not guarantee every background operation succeeds.
支援命令但 SANACT 不受支援時，必須回 Invalid Field in Command。 || A supported command with unsupported SANACT must return Invalid Field.
若不同 controller 屬於同一 subsystem，支援的相同 Sanitize 命令類型應一致；再另外驗證各命令的目標能力。 || Controllers in the same subsystem must advertise consistent supported sanitize types for the corresponding command.
先查實際方法的能力位元，不要只檢查 SANICAP 是否非零。 || First inspect the method-specific bit rather than SANICAP being nonzero.
''')

s(127,'NDAS、Overwrite Pattern、Pass Count 與反轉 Pattern 如何使用？ || How do NDAS, overwrite pattern, passes and inversion work?', ['sanitizeconfig','nvmsanitize'], '''
Overwrite 的欄位決定覆寫內容與次數；NDAS 則控制成功後是否釋放配置。資料清除與 deallocation 是不同動作，必須分開理解。 || Overwrite fields select pattern/passes while NDAS controls allocation release; erasure and deallocation are distinct.
這些 Overwrite 與 NDAS 欄位屬 subsystem Sanitize，不能照搬到 Sanitize Namespace 的 CDW10。 || These overwrite/NDAS fields belong to subsystem Sanitize, not the namespace command layout.
確認 OWS、No-Deallocate Inhibited 與 No-Deallocate Modifies Media After Sanitize，必要時讀 FID17h.NODRM。 || Check OWS, no-deallocate inhibition/media-modification attributes and FID17h.NODRM.
SANACT=3 選 Overwrite；OVRPAT 為 32-bit pattern；OWPASS=0 表示 16 次，1～15 表示該次數；OIPBP=1 在各次之間反轉 pattern。 || SANACT3 selects Overwrite; OVRPAT is 32-bit, OWPASS0 means 16 passes and 1–15 their literal count; OIPBP1 inverts between passes.
假設 OVRPAT=AAAAAAAAh、OWPASS=2、OIPBP=1，兩次分別使用 AAAAAAAAh 與 55555555h。再獨立決定是否請求 NDAS。 || With patternAAAAAAAAh, two passes and inversion, the patterns areAAAAAAAAh then55555555h; choose NDAS separately.
成功後讀 SOS、完成 passes 與 GDE；若資料被 deallocate，Read 結果應依 deallocated LBA 規則，不保證仍讀出最後 pattern。 || After completion inspect SOS, completed passes and GDE; deallocated reads follow deallocation rules rather than guaranteeing the final pattern.
NDAS=1 但被 NDI 禁止時，NODRM=0 拒絕為 Invalid Field；警告模式可執行並回報 Unexpected Deallocate。非 Overwrite 時覆寫欄位按規定忽略。 || With inhibited NDAS, NODRM0 rejects with Invalid Field; warning mode permits processing with unexpected-deallocation reporting. Non-overwrite actions ignore overwrite fields as defined.
比較要求的 pattern／passes、Log 保存的 SCDW10 與實際完成狀態；不要把 OWPASS=0 解成沒有做任何覆寫。 || Compare request fields and logged SCDW10/outcome; OWPASS0 does not mean zero work.
先查 OWPASS 的特殊零值與 NDAS 是否有效，再分析讀回資料。 || First check zero-pass encoding and NDAS validity before interpreting readback.
''')

s(128,'SPROG、SOS、SANS 與 GDE／NDE 要怎麼一起看？ || How are progress, status, state and erased-data flags interpreted together?', ['nvmsanitize'], '''
進度比例、操作結果、狀態機位置與資料是否仍保持已清除，是四個不同問題。分開看，才能避免把 FFFFh 或 GDE=1 當成全部流程已完成。 || Progress, outcome, state and continued erased-data condition answer different questions; neitherFFFFh nor GDE1 alone proves full completion.
LID81h 依 NSID 選 subsystem 或指定 namespace；namespace 回覆中的 NDE 不能當成整個 subsystem 的 GDE。 || LID81h selects subsystem or namespace using NSID; NDE does not substitute for subsystem GDE.
確認 SANICAP 與 verification 能力，再讀同一目標的整份一致狀態快照。 || Check sanitize/verification support and read a consistent snapshot for the same target.
SPROG／65536 是適用處理階段的完成比例；SOS 表示未開始、成功、進行中、失敗等；SANS 指狀態機位置；GDE／NDE 還會受後續使用者寫入影響。 || SPROG/65536 gives applicable-phase progress, SOS outcome/progress category, SANS state, and GDE/NDE the erased condition affected by later writes.
先看 SOS 是否仍 Sanitizing，再看 SANS 在 Processing、Media Verification 或 Post-Verification Deallocation，最後才解讀 SPROG。 || Read SOS, identify the active SANS phase, then interpret SPROG.
SPROG=8000h 在適用處理階段代表約 50%；FFFFh 在未處理或 Media Verification 時也可出現，不是獨立成功證據。 || SPROG8000h indicates50% in an applicable processing phase; FFFFh also appears outside processing or during verification and is not standalone success.
Get Log 查錯目標可有 Invalid Namespace or Format；subsystem 正在清除時讀 namespace 狀態另有 Sanitize In Progress 限制。 || Invalid targets and namespace queries during subsystem sanitization have distinct Invalid Namespace/Format and Sanitize In Progress conditions.
比較 SCDW10 與原要求，避免把先前一次清除的結果當成這次結果；再查看後續是否已有寫入清除 GDE／NDE。 || Match SCDW10 to the request and consider subsequent writes clearing GDE/NDE rather than mistaking an old result for the current operation.
先查 SOS 與 SANS，接著才問 SPROG 的數值是否合理。 || First read SOS/SANS, then assess the progress value.
''')

s(129,'Subsystem Sanitize 期間哪些 Command 允許執行？ || Which commands are permitted during subsystem sanitization?', ['sanitizerestrict','nvmsanitize'], '''
清除期間必須阻止使用者資料重新流入或被讀出，但仍保留查詢、通知與必要管理能力。允許清單因此有命令、選項與 Log 層級限制。 || Sanitization restricts user-data access while preserving essential management; permissions apply to commands, options and logs.
限制適用於 subsystem 的全部 controller；換另一個 controller 不能繞過同一清除狀態。 || Restrictions apply across subsystem controllers; another controller is not a bypass.
查 Figure144、Sanitize 狀態機，以及 NVM Figure200／201 的命令集補充。 || Use Figure144, the sanitize state machine and NVM Figures200/201.
Identify、AER、Get Features、queue 管理及指定 Log 可用；Sanitize Status 可查。PEL 與 vendor-specific Log 在此清除期間禁止，Self-test 也禁止；Error Log 的 LBA 必須回 0。 || Identify, AER, Get Features, queue management and selected logs remain available. PEL/vendor logs and self-test are prohibited; Error Log LBA returns zero.
先判斷狀態，再按命令及 LID 套限制。一般 I/O 受阻；Flush 與 Media Verification Read 有特別規則，不能用「全部 I/O 一律禁止」蓋過例外。 || Apply state, command and LID restrictions; Flush and media-verification reads have explicit exceptions to ordinary I/O blocking.
允許的命令正常完成；不允許的命令被拒絕，而背景 Sanitize 繼續。清除進度查詢建議不要過度頻繁，以免干擾進度。 || Allowed commands complete while prohibited commands are rejected and sanitization continues; avoid excessively frequent polling.
進行中通常回 Sanitize In Progress；進入 failure state 後須依命令類型與失敗規則處理，不能把進行中與失敗混為一個狀態。 || In-progress rejection generally uses Sanitize In Progress; failure-state processing follows its command-specific rules.
驗證同一限制是否在所有相關 controller 生效，也檢查允許的 Get Log 沒有洩漏應清除的使用者資料欄位。 || Verify restrictions across controllers and permitted logs' sanitization of user-data fields.
先確認 LID 是否在允許清單，而非只看 Opcode=Get Log Page。 || First check the specific LID, not merely Get Log Page opcode permission.
''')

s(130,'Sanitize 遇到 Reset 或 Power Loss 會繼續嗎？ || Does sanitization continue across reset or power loss?', ['reset'], '''
Sanitize 的清除保證不能讓 Reset 或拔電變成逃脫途徑，因此背景操作會跨 Controller Level Reset 與 power cycle 繼續。 || Reset or power cycling must not provide an escape from sanitization; background processing continues across them.
持續的是所選清除目標的狀態機與操作，不是原本已消失的 Admin Queue 或 AER Request。 || What persists is the target operation/state machine, not old Admin Queues or AER requests.
重新讀 LID81h，確認 SOS、SANS、SCDW10、MVCNCLD 與目標 NSID；先恢復管理通道才能查詢。 || After recovering access, inspect target NSID, SOS, SANS, SCDW10 and MVCNCLD.
MVCNCLD 表示 Media Verification 被取消。傳輸層或 Subsystem Reset 的特定條件會設定它，不能把它解讀成 Sanitize 取消。 || MVCNCLD reports cancelled media verification under specified transport/subsystem-reset conditions, not cancelled sanitization.
重設前保存狀態；恢復後先讀同一目標的 Log，再判斷是否繼續處理、轉入 deallocation 或已完成，不直接重新開始另一筆操作。 || Preserve pre-reset state, re-read the same target and identify processing/deallocation/completion before attempting another operation.
合理結果是背景操作持續或已依狀態機完成；斷電期間沒有處理進度並不違規，但恢復後不能忘記操作。 || Continuing or completed operation can be correct; no progress while unpowered is expected, but forgetting the operation is not.
仍在處理時重送啟動要求可能被 Sanitize In Progress 拒絕。不要將這個拒絕誤判成 Reset 後功能損壞。 || A new initiation during processing can be rejected as Sanitize In Progress without implying reset damage.
檢查原參數、目標及狀態延續，再與重新建立的 AER／Log 查詢區分。 || Verify parameter/target/state continuity separately from renewed AER and query setup.
先確認查的是原目標，而不是在 namespace 清除後改查 subsystem Log。 || First ensure the post-reset query addresses the original target.
''')

s(131,'成功、失敗與 Failure Mode 在 Log 中如何區分？ || How do success, failure and failure mode differ in the log?', [], '''
操作結果與目前狀態不一定一樣。離開 Failure Mode 後，狀態可以回 Idle，但最近一次清除仍然是失敗。 || Outcome and current state differ: leaving failure mode can return to Idle while the latest sanitize outcome remains failed.
以同一 target 的 SOS 與 SANS 判斷；namespace 失敗不能直接當成整個 subsystem 的最後清除結果。 || Use SOS/SANS for one target; namespace failure is not the subsystem’s last-operation result.
讀 LID81h；支援相關 verification 資訊時另讀 FAILS 與 MVCNCLD，補足在哪一階段失敗。 || Read LID81h and applicable FAILS/MVCNCLD to establish the failure stage.
SOS=001b 為 Sanitized，010b 為 Sanitizing，011b 為 Sanitize Failed，100b 為 Sanitized Unexpected Deallocate；SANS 再指出 Idle、Processing 或 Failure 等實際狀態。 || SOS001b means sanitized,010b sanitizing,011b failed and 100b sanitized with unexpected deallocation; SANS identifies the actual state.
先查看結果，再判斷當前是否仍被失敗限制阻擋。若 SANS=Idle 但 SOS=Failed，確認是否曾執行合法 Exit Failure Mode。 || Inspect outcome and current restrictions; Idle with failed SOS can follow valid Exit Failure Mode.
成功不只看 SPROG；失敗也不是只看命令 CQE。背景失敗應由狀態與事件反映。 || Neither progress alone nor the initiation CQE establishes the final background outcome.
Restricted Failure 與 Unrestricted Failure 的允許復原動作不同。不能從兩者相同的 Failed 結果推論可使用相同恢復操作。 || Restricted and Unrestricted Failure allow different recovery actions despite both reporting failure.
將 SOS、SANS、原 AUSE 及後續復原要求放在一起，檢查是否存在不合法的狀態轉移。 || Correlate SOS, SANS, original AUSE and recovery requests to identify invalid transitions.
先看 SANS，確認讀者所說的「失敗模式」真的是目前狀態，而不是歷史結果。 || First inspect SANS to distinguish current failure mode from historical failure outcome.
''')

s(132,'Exit Failure Mode 能做什麼，不能做什麼？ || What does Exit Failure Mode accomplish?', [], '''
Exit Failure Mode 可以在允許的情況下解除失敗狀態造成的存取限制，但它不會把未清除的資料補清，也不會把失敗結果改成成功。 || Where permitted, Exit Failure Mode releases failure-state restrictions; it neither finishes erasure nor converts failure into success.
動作針對指定清除目標；subsystem 與 namespace 各有狀態機。 || The action applies to the selected subsystem or namespace target.
先讀 SANS 與原 SCDW10.AUSE。AUSE 決定操作進入 restricted 或 unrestricted 路徑。 || Read SANS and original AUSE, which selects restricted versus unrestricted processing.
SANACT=001b 表示 Exit Failure Mode。它不是新一次 Block／Crypto／Overwrite 清除。 || SANACT001b requests Exit Failure Mode, not a new erasure operation.
Unrestricted Failure 可藉此回 Idle；Restricted Failure 必須以符合限制的新清除操作復原。Idle 收到此動作不視為錯誤。 || Unrestricted Failure can transition to Idle; Restricted Failure requires a permitted new sanitize operation. The action in Idle is not an error.
合法退出後可回到允許正常存取的狀態，但 SOS 仍可報告最近操作失敗，GDE／NDE 也不能憑退出動作設成成功清除。 || Valid exit restores permitted access while SOS can retain failure; exit alone cannot establish GDE/NDE erasure.
Restricted Failure 的 Exit Failure Mode 會依目標回相應 Sanitize Failed 類型；不能用反覆重送或 Reset 繞過限制。 || Exit is rejected under restricted-failure rules; repeated requests or reset do not bypass them.
驗證成功退出後的 SANS 與失敗歷史同時合理，而不是要求 Log 全部清零。 || Verify both restored state and retained failure history rather than demanding all-zero logs.
先查原 AUSE 及現在 SANS，確認是否真的在允許退出的狀態。 || First establish AUSE and SANS to determine whether exit is permitted.
''')

s(133,'Sanitize 的 AER 與 PEL 應在何時產生？ || When are sanitize AERs and persistent events generated?', ['aerfull','aec'], '''
通知告訴 Host 狀態有重要變化，PEL 則保存歷史；兩者都不是原 Sanitize 命令的第二次完成。 || Notifications announce transitions and PEL retains history; neither is a second completion of the initiating command.
AER 由啟動操作的 controller 回報；事件參數與 PEL.NSID 協助辨別 subsystem 或 namespace 目標。 || The initiating controller reports the AER; event parameters and PEL.NSID identify the target.
確認通知支援、相關 AEC 設定、outstanding AER 與 PEL 支援。 || Establish event/configuration support, outstanding AERs and PEL support.
AER 的 AET=6、LID=81h；AEI=01h 是 Completed，02h 是 Unexpected Deallocation，03h 是 Entered Media Verification。DW1 依定義標示目標。 || AET6/LID81h use AEI01h for completion,02h unexpected deallocation and 03h verification entry; DW1 carries defined target information.
啟動後記 Start；進入驗證先通知驗證階段；操作進入 Idle 或 Failure 才形成相應完成事件。收到通知後讀同一目標的 Log。 || Record start at initiation, notify verification entry separately and record completion at Idle/failure transitions; read the same target after notification.
Completed 通知可以對應失敗完成，因此仍需讀 SOS／SANS。PEL Completion 同樣要看 SSTAT，不能只看事件名稱。 || Completed notifications and PEL completion can describe failure; inspect SOS/SANS/SSTAT.
沒有 AER Request 時不能期待立刻收到 CQE；事件是否保留與遮蔽仍遵循 AER 規則。也不要在 Sanitize 期間強迫讀取當時不允許的 PEL。 || Without an AER request no immediate CQE is expected; normal retention/masking rules apply. Do not require PEL reads while prohibited during sanitization.
對照事件的目標、原命令與 Log 狀態，區分「通知未送達」與「背景操作沒有完成」。 || Correlate event target, initiating command and log state to distinguish notification loss from unfinished processing.
先查 AEC、AER Request 及回報 controller，再判斷通知是否真的缺失。 || First check AEC, available requests and reporting controller before declaring a missing event.
''')

s(134,'Namespace Sanitize 如何指定目標並確認其他 Namespace 未被清除？ || How is namespace sanitization targeted and isolated?', ['sanitizerestrict','idctrl','nsid'], '''
Namespace Sanitize 提供單一 namespace 的 Crypto Erase，讓清除資料的範圍小於整個 subsystem。資料隔離與共享管理限制仍要分開驗證。 || Namespace Sanitize provides a narrower Crypto Erase target while shared management restrictions remain separate from data isolation.
NSID 指定一個 active namespace；其他 controller 若能存取同一 namespace，也必須遵守該目標的清除限制。 || NSID selects one active namespace, with restrictions applying across all controllers accessing it.
確認 namespace sanitize 能力、Active List、Write Protection 及 MNSOIP 並行上限。 || Check namespace sanitize support, Active List, write protection and MNSOIP concurrency limit.
Opcode8Ch、SANACT=100b；PREQ 在 CDW10 bit4，不是 subsystem Sanitize 的 bit11。用該 NSID 讀 LID81h 與 NDE。 || Use opcode8Ch/SANACT100b; PREQ is CDW10 bit 4 rather than subsystem bit 11. Query that NSID’s LID81h/NDE.
先保存目標與非目標 namespace 的資料／狀態基準，再啟動並追蹤目標。完成後驗證目標清除結果，並確認非目標資料未因這次操作被清除。 || Snapshot target and non-target baselines, initiate and monitor the target, then verify erasure and preservation of non-target data.
目標 NDE 可設為 1；其他 namespace 逐一清除也不能自行推成 GDE=1，因 subsystem 清除範圍還包含其他位置。 || Target NDE may become1; sanitizing all namespaces still does not establish GDE because subsystem scope includes other locations.
NSID=0、FFFFFFFFh、inactive 或正在刪除會被 Invalid Namespace or Format 拒絕；寫入保護另回 Namespace is Write Protected。 || Zero, broadcast, inactive or deleting namespaces use Invalid Namespace/Format; protection uses Namespace is Write Protected.
將資料內容隔離、目標 I/O 限制與全域韌體更新限制分別記錄；非目標資料不被清除，不代表所有管理命令都不受影響。 || Validate non-target data, target I/O restrictions and shared firmware restrictions separately.
先確認測試真的送 8Ch 並指定正確 NSID，而不是誤用 84h 清除 subsystem。 || First verify opcode8Ch and the intended NSID rather than subsystem opcode84h.
''')

s(135,'Namespace Sanitize 遇到不存在、Inactive 或不支援的目標如何回應？ || How are invalid or unsupported namespace sanitize requests handled?', ['status','nsid','nwp'], '''
錯誤可能來自命令不受支援、目標不合法、動作不支援或並行資源不足。這些原因不能統一寫成 Invalid Namespace。 || Unsupported command, invalid target/action and exhausted concurrency are distinct failure causes.
檢查指定 namespace 與 subsystem 目前的清除狀態；subsystem failure 也可能阻止新 namespace 操作。 || Check target and subsystem sanitize state; subsystem failure can block a new namespace operation.
使用 SANICAP、Active／Allocated Lists、Write Protection 與 LID81h.MNSOIP 建立前提。 || Establish preconditions using SANICAP, namespace lists, protection and MNSOIP.
SANACT 只有 Crypto Erase 與狀態管理動作，010b／011b 在 Namespace 命令是保留值。 || Namespace SANACT supports Crypto Erase and defined state-management actions;010b/011b are reserved.
先用合法基準驗證支援，再分別測非法 NSID、寫入保護、非法 SANACT 與並行超量；保留每次測試前的狀態。 || Establish valid support, then isolate target, protection, action and concurrency negative tests with state snapshots.
若啟動命令以非 Success 完成，不得為該命令開始清除、改寫該目標 Sanitize Status 或改變使用者資料。 || An unsuccessful initiation must not start sanitization, alter target Sanitize Status or alter user data for that command.
非法目標用 Invalid Namespace or Format；非法 SANACT 用 Invalid Field；超限用 Request Exceeds Maximum Namespace Sanitize Operations In Progress。原文 Figure104 列3Ch，Figure455 列12h，兩表有差異，不能擅自把其中一值當唯一驗收依據。 || Invalid targets use Invalid Namespace/Format, actions Invalid Field and over-limit requests their named concurrency status. Figure104 lists3Ch while Figure455 lists12h: the source conflict prevents treating either as an undisputed sole acceptance value.
除核對 Status，也驗證被拒絕的要求沒有啟動背景操作或改寫目標資料。 || Verify both status and absence of operation/data changes for rejected requests.
先確認是在驗證哪一個單獨失敗條件；並行數值爭議則保留原文兩處定位供查證。 || First isolate the failed condition; preserve both source locations for the conflicting concurrency code.
''')
