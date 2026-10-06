"""Q223–236: memory ownership, supported placement and persistence."""
from scripts.nvme_qa_extension import question
from scripts.nvme_qa_model import COMMON, REFS, pair
REFS['cmb']='B|8.2.1 (memory placement and lifetime)|768-770|'
REFS['cmbreg']='B|3.1.4 (CMBLOC, CMBSZ, CMBMSC, CMBSTS)|93-95,96-98|47–48, 52–55'
REFS['pmr']='B|8.2.5 (memory behavior; exclude PCIe packet detail)|771-772|'
REFS['pmrreg']='B|3.1.4 (PMR properties)|99-103|58–64'
COMMON['hmb_op']={**COMMON['command'],
 9:pair("""啟用或停用 HMB 沒有獨立的成功 AER；若另外發生已定義的硬體錯誤，才依其事件條件回報。 || HMB enable/disable has no separate success AER; independently defined hardware faults follow their own event rules."""),
 10:pair("""Get Features 回報 EHM、HMNARE、HMNAR 與配置資料；它不是 HMB 內容的備份。成功操作不要求 Error entry，失敗則依實際 CQE 與記錄條件判斷。 || Get reports HMB state and allocation, not a backup of buffer contents. Successful operations require no error entry; failures use CQE/logging rules."""),
 11:pair("""若支援該 FID 的 PEL Set Feature Event，依允許記錄與成功變更條件處理；一般 HMB 讀寫不是逐次 Persistent Event。 || Supported, permitted Set Feature logging follows successful-change rules; ordinary HMB accesses are not individual persistent events."""),
 12:pair("""HMB 資源配置不跨 CLR 保留。重設後應重新提供先前配置的記憶體；只有大小、descriptor 位址與內容、buffer 內容都符合原狀時，才能用 MR=1 表示原記憶體返回。 || HMB allocation does not persist across CLR. Reprovide it after reset; MR=1 requires unchanged size, descriptor address/content and buffer content."""),
 13:pair("""Subsystem Reset 使受影響 controller 的 HMB 配置失效，Host 恢復通道後重新配置。舊 Host RAM 的 bytes 還在，不代表 controller 仍有使用權或已知其地址。 || Subsystem reset invalidates affected HMB allocations. Reconfigure after recovery; residual RAM bytes do not establish an active allocation."""),
 14:pair("""HMB 不是持久儲存。若供電變化使內容遺失，重新配置應使用 MR=0，不能謊稱原內容仍在。規範要求 controller 在使用 HMB 時，面對 surprise removal 仍確保不因 HMB 造成資料遺失或損壞。 || HMB is not persistent storage. Use MR=0 if content was lost; the controller must prevent data loss/corruption from surprise removal while using HMB."""),
 15:pair("""HMB 是 Host 分配給此 controller 專用的記憶體；啟用期間 Host 不得改寫 descriptor list 或 buffer，也不能把同一區域交給其他用途。這與 namespace 的共享能力無關。 || HMB is host memory exclusively allocated to this controller; the host shall not modify its list/buffers while enabled or repurpose them.""")}
COMMON['cmb_op']={**COMMON['register'],**COMMON['queue'],
 8:pair("""CMB Register 與記憶體存取沒有 NVMe CQE；若使用 CMB 的 Admin／I/O 命令回 CQE，才對該命令解讀 DNR、More。不能替 MMIO 寫入編造 Status。 || CMB register/memory accesses have no CQE. Decode DNR/More only for an Admin/I/O command using CMB, not for MMIO itself."""),
 12:pair("""CC.EN 觸發的 CLR 與 FLR 保留 CMBMSC，但 CMB 內容變成 undefined。Host 必須重新初始化要使用的內容，特別是 CQ Phase；位址設定保留不等於 queue 或資料有效。 || CC.EN reset and FLR retain CMBMSC but make CMB contents undefined. Reinitialize memory, especially CQ phases; retained addressing does not preserve valid queues/data."""),
 13:pair("""Subsystem Reset 後重新確認 CMB Register 與 mapping，重建使用它的 queues。不能把 CC.EN／FLR 的特定 CMBMSC 保留規則擴大成所有重設都保留。 || Rediscover mappings and rebuild queues after subsystem reset; do not extend specific CC.EN/FLR retention to every reset source."""),
 14:pair("""CMB 不提供 PMR 的跨斷電持久性保證。Power Cycle 後重新配置、初始化，再使用支援的用途。 || CMB has no PMR-style power-cycle persistence guarantee; reconfigure and initialize it."""),
 15:pair("""CMB 位於 controller，但 Host 與 controller 使用的地址範圍可以不同。需正確轉換相同 offset，並避免與其他 DMA 及 PMR 範圍衝突。 || Host and controller CMB address ranges may differ; map equal offsets correctly and avoid DMA/PMR conflicts.""")}
COMMON['pmr_op']={**COMMON['register'],
 8:pair("""直接存取 PMR 或其 Register 沒有 NVMe CQE。使用 PMR buffer 的命令若有 CQE，才解讀其 Status、DNR 與 More；成功 CQE仍不能取代 PMR 健康與持久性檢查。 || Direct PMR/register access has no CQE. Commands using a PMR buffer do, but successful CQE does not replace health/persistence verification."""),
 9:pair("""PMR 變成唯讀或不可靠時，SMART.CW.PMRRO 回報警告，並可能依 SMART AER 設定通知。通知可能晚於狀態變化，因此從上次確認 HSTS 正常以來的操作都應納入檢查。 || Read-only/unreliable PMR sets the SMART warning and may trigger configured AER. Delivery may lag, so assess operations since the last normal HSTS observation."""),
 10:pair("""PMRSTS 的 NRDY、HSTS、ERR 是主要證據，SMART 提供 PMR 警告。Register 存取不要求每次新增 Error Log；使用 PMR 的命令失敗才另依其 CQE 與記錄條件分析。 || NRDY/HSTS/ERR are primary evidence, with SMART PMR warnings. Register accesses are not individually error-logged; command failures follow CQE rules."""),
 11:pair("""若 PMR 警告符合支援的 PEL Critical Warning hardware event，依事件規則記錄；每次 PMR 讀寫或 EN 切換不是獨立 PEL 事件。 || A PMR warning may qualify for a supported PEL critical-warning event; each read/write or EN change is not independently logged."""),
 12:pair("""Ready 且已確認持久的內容跨 CLR 保留。CC.EN 觸發的 CLR 另保留 PMR 控制／狀態 Register；但仍應確認健康，不能因 Register 保留就忽略 Restore Error。 || Ready-state persistent data survives CLR. CC.EN reset also retains PMR control/status registers; inspect health and Restore Error nonetheless."""),
 13:pair("""Subsystem Reset 後重新確認啟用與 Ready 狀態，再檢查 HSTS。PMR 的資料持久性與 Register 是否須重建是不同問題；Restore Error 表示原內容可能未正確恢復。 || Recheck enable/readiness and HSTS after subsystem reset. Data persistence differs from register restoration; Restore Error questions restored contents."""),
 14:pair("""Ready 時已完成且確認持久的寫入應跨 Power Cycle 保留；恢復後仍須確認 HSTS 與 ERR。Sanitize 可清除 PMR，不能把同時發生的 Sanitize 當成一般斷電遺失。 || Confirmed persistent writes survive power cycles, subject to restored health checks. Sanitize can purge PMR and is distinct from ordinary power-loss behavior."""),
 15:pair("""PMR 屬於提供它的 PCIe function，其他存取端也必須核對該 PMR 的健康。命令所有 data 與 metadata 必須全部位於 PMR 或全部在其外，不能任意混放。 || PMR belongs to its PCIe function; consumers must check that PMR’s health. A command’s data and metadata must be entirely inside or outside PMR.""")}
COMMON['memory_compare']={**COMMON['hmb_op'],
 8:pair("""HMB 透過 Set Features，具有 CQE；CMB／PMR 的直接 Register 存取沒有 CQE。若是命令使用其中的 buffer，DNR／More 屬於那筆命令，不能替不同存取方式共用一組固定值。 || HMB Set Features has a CQE; direct CMB/PMR register accesses do not. Commands using buffers carry their own DNR/More, not one fixed memory-type value."""),
 12:pair("""CLR 後 HMB 配置失效；CMB 特定 mapping 可保留，但內容 undefined；PMR 已持久內容保留。三者都需依各自狀態重新確認是否可用。 || CLR invalidates HMB allocation; CMB mappings may persist while contents become undefined; persistent PMR data remains. Recheck readiness separately."""),
 13:pair("""Subsystem Reset 後重建受影響控制環境，再分別處理 HMB 配置、CMB 初始化與 PMR 健康檢查；不能把所有記憶體當成同一種保存介面。 || After subsystem reset, separately restore HMB allocation, initialize CMB and check PMR health."""),
 14:pair("""HMB 與 CMB 不提供 PMR 的持久性承諾；PMR 也要先用支援的 write barrier 與健康狀態確認先前寫入。Host RAM 是否另有持久硬體不是這三種 NVMe 介面替它保證。 || HMB/CMB lack PMR persistence guarantees; PMR still requires supported barriers and health checks. External host-memory persistence is a separate property."""),
 15:pair("""先確認記憶體位於 Host 或 controller，再確認使用權與地址空間。相同數字的地址可能經過不同 mapping，不能只比地址值就判定同一個 buffer。 || Identify physical location, ownership and address space; identical numeric addresses do not prove identical buffers across mappings.""")}

def q(n,t,b,o=None):
 profile='memory_compare' if n in (223,236) else 'hmb_op' if n<228 else 'cmb_op' if n<232 else 'pmr_op'
 question(n,t,profile,['hmb','cmb','cmbreg','pmr','pmrreg','idctrl'],b,o)

q(223,"HMB、CMB 與 PMR 分別解決什麼問題？ || What problems do HMB, CMB and PMR solve?", '''
它們都與記憶體有關，但借用方向、使用者與保存承諾不同；先辨認這三件事，才不會錯配 buffer。 || Their memory location, user and persistence guarantees differ; identify those before placement.
HMB 位於 Host，專供 controller 使用；CMB 位於 controller，供宣告支援的 queue 或 buffer；PMR 是可直接讀寫的持久記憶體區域。 || HMB is host memory dedicated to the controller; CMB is controller memory for supported uses; PMR is directly accessible persistent memory.
HMB 查 HMPRE；CMB 查 CAP.CMBS、CMBSZ；PMR 查 CAP.PMRS、PMRCAP。 || Discover HMB through HMPRE, CMB through CAP/CMBSZ and PMR through CAP/PMRCAP.
HMB 用 FID0Dh 配置 descriptor；CMB 用 CMBMSC／CMBLOC 建立地址關係；PMR 用 PMRCTL 與 PMRSTS 確認啟用和健康。 || HMB uses FID0Dh descriptors; CMB uses address/control registers; PMR uses enable/readiness/health registers.
依需求選擇：借 Host RAM 給韌體使用選 HMB；將 SQ 放到裝置記憶體須查 CMB.SQS；要直接存放持久資料則研究 PMR 的 barrier 與健康。 || Match the need: firmware host RAM, supported CMB SQ placement or persistent PMR data with barriers and health checks.
正確結果是功能可用且符合各自使用限制，不是所有記憶體都能放所有資料結構。 || Success means supported use within its constraints, not universal placement freedom.
PMR 的 queue、PRP／SGL list 支援不在規範範圍，controller 可回 Invalid Field；不能因 PMR 可讀寫就把它當成另一個 CMB。 || Queue/list use in PMR is outside scope and may return Invalid Field; writable PMR is not interchangeable with CMB.
用能力、配置、存取方式與恢復後內容交叉比對，而不是只看一個地址能不能讀到 bytes。 || Compare support, configuration, access method and restored contents, not only readable bytes.
先檢查選錯記憶體種類，或把「位於裝置」誤解成「必定持久」。 || First check memory type and the mistaken assumption that device-local means persistent.
''')
q(224,"HMB 大小與 Descriptor List 如何配置？ || How are HMB size and descriptor lists configured?", '''
Host 以多段實體連續記憶體提供 HMB，不必一次取得整塊連續 RAM，但 descriptor list 本身必須實體連續。 || Multiple contiguous ranges form HMB; the descriptor list itself must be physically contiguous.
配置給一個 controller 專用，Host 啟用後不能當一般工作 buffer 改寫。 || The allocation is exclusive to one controller and unavailable for ordinary host writes while enabled.
查 HMPRE、HMMIN、HMMINDS、HMMAXD；前兩者及 HMMINDS 用 4 KiB 單位。 || Read preferred/minimum size, minimum descriptor size and maximum descriptors; size capability fields use 4 KiB units.
HSIZE 與每筆 BSIZE 卻用 CC.MPS page 單位；HMDLEC 是實際筆數，list address 16-byte 對齊，BADD 按 CC.MPS 對齊。 || HSIZE/BSIZE use CC.MPS pages; HMDLEC is a literal count, list address is 16-byte aligned and BADD page-aligned.
先配置並固定 RAM，填 16-byte descriptors，核對各段大小與 HSIZE，再以 EHM=1 啟用，等 CQE 成功才交給 controller 使用。 || Pin memory, construct descriptors, reconcile sizes and enable with EHM=1, awaiting success.
Get 回 EHM 與 attributes 可核對實際配置。假設 CC.MPS 選 8 KiB，HSIZE=256 表示 2 MiB，不是 1 MiB。 || Get verifies allocation; with hypothetical 8 KiB pages, HSIZE256 means 2 MiB.
HMDLEC=0 須 Invalid Field；超過建議可用 descriptor 限制可能只使部分記憶體未利用，不能一律預期拒絕整個配置。 || Zero HMDLEC requires Invalid Field; exceeding usable descriptor limits may reduce utilization rather than force rejection.
同時比對能力單位、命令單位與 Get attributes，不能直接將 HMPRE 數字抄進 HSIZE。 || Convert capability units before encoding HSIZE and verify readback.
先檢查 4 KiB 與 CC.MPS 的差別，以及 HMDLEC 是否錯用 zero-based。 || First check page units and literal descriptor count.
''')
q(225,"HMB 位址、大小或 Descriptor 數量不合法時如何判斷？ || How are malformed HMB allocations handled?", '''
不同欄位的錯誤規則不同；驗證時要指定單一錯誤，才知道應預期哪一種反應。 || Different fields have different rules; isolate one malformed condition at a time.
包含 descriptor list 本身、每筆記憶體範圍，以及目前 HMB 是否已啟用。 || Check list structure, ranges and current enable state.
查 HMMINDS／HMMAXD、HMBR 與 Get.EHM，再核對 Set 的欄位。 || Check limits, HMBR, current EHM and submitted fields.
HMDLEC=0 是 Invalid Field；BSIZE=0 的 descriptor 必須忽略。HMDLLA 低 4 bits 要清零，但 controller 必須如同其為零運作，且不必檢查。 || Zero entry count is Invalid Field; zero-size descriptors are ignored. The list address low four bits are treated as zero without a required check.
先測可判定的格式錯誤，再將地址無法存取造成的傳輸失敗分開；不要把 Host 錯誤 mapping 當作同一種參數錯誤。 || Separate specified format errors from inaccessible-memory transfer failures.
合法配置成功；超出可用 descriptor 限制時，可出現未完全利用 HMB 的結果。 || Valid allocation succeeds; out-of-limit allocation may be only partly used.
已啟用又要求 EHM=1 必須 Command Sequence Error；不支援 HMBR 卻設 HMNARE=1 必須 Invalid Field。不能要求每個低位對齊錯誤都回相同 Status。 || Re-enabling active HMB requires Command Sequence Error; unsupported HMNARE requires Invalid Field. Do not demand one status for every alignment defect.
將具體欄位條件對到指定反應，保留「忽略」與「必須拒絕」之間的差別。 || Match each condition to its rule, preserving ignore versus reject semantics.
先確認測試是否同時放入多種錯誤，造成 Status 無法唯一預測。 || First check whether multiple faults prevent a unique expected status.
''')
q(226,"HMB 如何啟用、停用並在 Reset 後重新提供？ || How is HMB enabled, disabled and returned after reset?", '''
HMB 的使用權要明確交接，Host 才知道何時能回收記憶體。 || Explicit ownership transitions establish when memory may be reclaimed.
EHM 控制 controller 是否可使用 HMB，MR 描述返回的內容是否仍符合原狀。 || EHM controls use; MR describes whether returned contents are unchanged.
先 Get.EHM 與配置，Reset 後也重新確認，而不沿用 Host 記錄的啟用狀態。 || Read EHM/allocation rather than assuming pre-reset enablement persists.
EHM=0 時 CDW12～15 忽略；MR=1 要求原大小、list 位址、list 內容及 buffer 內容完全相同。 || EHM0 ignores CDW12–15; MR1 requires identical size, list address/content and buffer contents.
啟用後交給 controller；需要回收時送 EHM=0 並等成功 CQE，之後才能改寫。Reset 後再提供保留的配置或新的配置。 || Enable, then disable and await success before host modification; reprovide retained or new allocation after reset.
停用成功後 controller 不得再存取 HMB，直到重新啟用；原本未啟用時再停用也成功且不做其他動作。 || After successful disable no HMB access is allowed until re-enabled; disabling an already disabled HMB succeeds without action.
已啟用再次啟用是 Command Sequence Error；內容已被改動卻宣告 MR=1 是 Host 違反前提，不能期待原快取仍安全可用。 || Re-enable while enabled is a sequence error; claiming MR1 after modification violates the return premise.
用停用 CQE 當作可修改的交接點；僅送出停用命令並不表示交接完成。 || Use successful disable completion, not submission, as the ownership handoff.
先檢查 Host 回收記憶體的時點是否早於停用完成。 || First compare reclamation timing with disable completion.
''')
q(227,"Host 提前回收仍在使用的 HMB 會有什麼後果？ || What happens if the host prematurely reclaims HMB?", '''
這會破壞 controller 專用記憶體的前提，可能讓裝置讀到其他用途的資料，或改寫已被重新分配的 RAM。 || It violates exclusive ownership and can expose or corrupt memory reassigned to another use.
受影響可能超過 NVMe buffer 本身，因為 Host 已把同一實體頁交给別的程式。 || Damage may reach unrelated host data in reassigned physical pages.
查 EHM 與最後一次停用 CQE，並保存記憶體配置和 mapping 的生命週期。 || Check EHM, disable completion and allocation/mapping lifetime.
HMB descriptor 與描述的 ranges 都受保護；只保留 list 卻回收資料頁，仍違反規則。 || Both descriptors and described ranges must remain intact; retaining only the list is insufficient.
先請求停用，等成功完成，再解除 mapping 與回收；若故障無法停用，需完成足以終止舊存取的恢復流程後才回收。 || Disable and await success before unmapping; failure recovery must end old accesses before reclamation.
正確交接後，controller 不再使用舊區域，Host 才可安全重用。 || After a valid handoff the old allocation is no longer accessed.
這種 Host 違規沒有保證會被 controller 偵測或以固定 Status 拒絕；可能出現資料損壞，不能靠期待 Error Log 防護。 || Host misuse has no guaranteed detection or fixed status and may corrupt data; error logging is not protection.
區分 Host 提前回收與 controller 在成功停用後仍存取：前者是 Host 問題，後者才違反明定停止存取要求。 || Distinguish premature host reclamation from controller accesses after successful disable.
先比對合法存取結束的時點與記憶體開始重用的時間。 || First align ownership end and memory reuse timing.
''')
q(228,"Host 如何找出 CMB 的位置、大小與可用用途？ || How are CMB location, size and uses discovered?", '''
需要同時知道 Host 如何存取 CMB，以及命令中的地址如何讓 controller 指向同一區域。 || Discover both host access and controller interpretation of command addresses.
CMB 有 PCIe address range 與 controller address range，兩者基底可不同，相同 offset 對應相同內容。 || Its PCIe and controller address ranges may have different bases but matching offsets.
查 CAP.CMBS，設 CMBMSC.CRE 後讀 CMBLOC 與 CMBSZ；CRE=0 時這兩個屬性可為零。 || Check CAP.CMBS, enable CRE and read location/size; zero values with CRE0 do not prove absence.
CMBLOC.BIR 選 BAR、OFST 配合大小單位求偏移；CMBSZ.SZ×SZU 求大小，再受 BAR 可用範圍限制。SQS、CQS、LISTS、RDS、WDS 各自宣告用途。 || BIR selects BAR, OFST locates the region and SZ×SZU determines size within BAR limits; support bits distinguish uses.
配置不衝突的 CBA，設 CMSE，檢查 CMBSTS.CBAI，再初始化要放入的 queue 或 buffer。 || Configure a nonconflicting CBA, enable CMSE, check CBAI and initialize contents.
Host 與命令使用各自正確的地址，同一 offset 對到同一份 CMB 內容。 || Both address views reach the same contents at matching offsets.
無效 CBA 會使 CBAI=1 且未成功啟用 controller memory space；這是 Register 狀態，不是回一筆 Admin CQE。 || Invalid CBA sets CBAI and prevents memory-space enablement; it is register state, not an Admin CQE.
比對 BAR 範圍、OFST、SZU、CBA 與支援 flags，不能只看 CAP.CMBS。 || Cross-check address bounds, units and use flags, not just capability presence.
先檢查是否把 BAR 地址直接拿去當已重新配置的 controller 地址。 || First check confusion between BAR and configured controller addresses.
''')
q(229,"哪些 Queue、Data、Metadata 與指標清單可放 CMB？ || Which queues, buffers and lists may reside in CMB?", '''
CMB 用途由多個能力位元分別控制，支援 SQ 不表示同時支援 CQ 或資料。 || Independent capability bits govern placement; SQ support does not imply CQ/data support.
限制可能以整條 queue、單筆命令的 list，或該命令的所有 data／metadata 為單位。 || Restrictions apply to an entire queue, a command’s list or its data/metadata set.
查 CMBSZ.SQS、CQS、LISTS、RDS、WDS，以及 CMBLOC.CQMMS、CQPDS、CDPMLS、CDPCILS、CDMMMS。 || Inspect use flags and mixed-memory/discontiguous-list capabilities.
CQMMS=0 要求單一 queue 全在 CMB 或全在外；CQPDS=0 要求 CMB queue 實體連續。LISTS 控制 PRP／SGL list，其他 bits 再決定混放與 SQ 位置限制。 || CQMMS0 prohibits mixed queue placement; CQPDS0 requires contiguous queues. LISTS and related bits govern pointer-list placement and dependencies.
先按物件選用途 flag，再檢查它和 SQ、data、metadata 的組合條件，最後才配置地址。 || Select the object capability, then validate its combined placement constraints before allocating.
假設 SQS=1、CQS=0，可把支援的 SQ 放 CMB，CQ 仍放 Host memory；不是兩者一定一起搬。 || With hypothetical SQS1/CQS0, an SQ may use CMB while its CQ remains in host memory.
違反使用要求一般須 Invalid Use of Controller Memory Buffer；但 LISTS=0 仍放 list 的條文明定 undefined，不能強行替它指定固定 Status。 || General misuse requires Invalid Use of CMB; placing lists with LISTS0 is explicitly undefined, not a fixed-status case.
RDS／WDS 要按命令資料方向解讀，例如 Read 的結果是 controller 傳向 Host 的資料。 || Interpret RDS/WDS by command transfer direction.
先檢查只確認了功能存在，卻漏查所選物件的用途 flag。 || First check the specific use flag rather than mere CMB presence.
''')
q(230,"CMB 超出範圍或用於不支援用途時如何處理？ || How are out-of-range or unsupported CMB uses handled?", '''
要分清無效 mapping、合法 mapping 中的用途違規，以及根本不被解讀成 CMB 的地址。 || Distinguish invalid mapping, misuse within a mapped CMB and addresses interpreted elsewhere.
CBA 與大小決定 controller address range；CMSE=0 時 Host 提供的地址不被視為 CMB。 || CBA/size define the controller range; disabled CMSE routes addresses elsewhere.
保存 CMBMSC、CMBSTS、CMBLOC、CMBSZ 與命令完整資料範圍。 || Preserve mapping/status/capabilities and the full command range.
CBA 不得使範圍溢出 64-bit 地址，也不得與已啟用的 PMR controller range 重疊。 || CBA must not overflow the 64-bit address space or overlap enabled PMR space.
先算起點與末端，再判斷每個地址落在哪個空間；最後檢查用途旗標與混放條件。 || Calculate both range endpoints, resolve address spaces and check use/mixing rules.
合法範圍且符合用途限制時，命令按正常資料存取執行。 || Valid ranges and uses follow ordinary command processing.
無效 mapping 看 CBAI；用途違規依 Invalid Use of CMB；範圍外地址可能被當成其他記憶體，不能一律預期「CMB 越界」專用 Status。 || Mapping failure uses CBAI; misuse uses its specified status. Out-of-range addresses may resolve elsewhere and have no universal CMB-overrun status.
命令錯誤與 Register 狀態是兩份證據；沒有 CQE 不表示 Register 啟用成功。 || Command outcomes and register status are separate evidence.
先檢查範圍計算是否溢位，以及計算用的是 Host 還是 controller 地址。 || First check arithmetic overflow and which address space was used.
''')
q(231,"Reset 後 CMB 設定與內容會保留嗎？ || Do CMB configuration and contents survive reset?", '''
位址保留與內容保留是兩件事，這是 CMB 恢復時最容易混淆的地方。 || Mapping retention and data retention are distinct.
CC.EN 觸發的 CLR 與 FLR 有明確 CMBMSC 保留例外，其他來源須看對應 Register 規則。 || CC.EN reset and FLR explicitly retain CMBMSC; other sources use their own register rules.
保存 Reset 來源、CMBMSC 與 CMBSTS，恢復後再讀取確認。 || Snapshot source and registers, then reread after recovery.
CMSE 由 0 轉 1、Controller Reset 或 FLR，都使 CMB 內容 undefined。 || CMSE0→1, Controller Reset and FLR make CMB contents undefined.
恢復 mapping 後重新初始化會用到的記憶體，再建立 queue；CQ 尤其要初始化 Phase，避免誤讀殘留完成。 || Restore mapping, initialize memory and rebuild queues, especially CQ phase bits.
新的使用期間從已初始化的內容開始，不能沿用舊 queue 指標或假定資料保存。 || A new lifetime uses initialized contents, not old queue state.
讀到與 Reset 前相同 bytes 也不代表規範保證保留；undefined 可以碰巧相同。 || Identical residual bytes do not turn undefined retention into a guarantee.
用 Register 保留規則驗 mapping，用 queue 與內容初始化規則驗使用權，兩項分開判定。 || Validate mappings and content/queue initialization separately.
先檢查是否因 CMBMSC 沒變，就省略了 CQ 與 buffer 初始化。 || First check whether unchanged CMBMSC incorrectly caused initialization to be skipped.
''')
q(232,"PMR 如何確認支援、啟用並等待 Ready？ || How is PMR discovered, enabled and made ready?", '''
PMR 可獨立於 NVMe 命令處理環境啟用，Host 必須等其自己的 Ready 狀態。 || PMR enablement is independent of the command controller and has its own readiness state.
PMR 占用 PMRCAP.BIR 指定 BAR 的整個區域；controller 地址可另由 PMRMSC 設定。 || PMR occupies the selected BAR region, with separately configurable controller addressing.
查 CAP.PMRS、PMRCAP 的 BIR、CMSS、RDS、WDS、PMRWBM、PMRTO、PMRTU。 || Check support, location, command access, barrier mechanisms and timeout units.
PMRCTL.EN 啟用；PMRSTS.NRDY=0 配合 EN=1 才代表 Ready，還要看 HSTS 與 ERR。 || EN1 plus NRDY0 establishes readiness, with health/error checks still required.
配置需要的地址空間，設 EN=1，等待 NRDY=0；Host 應至少等待 PMRTO×PMRTU 指定時間再判斷沒有完成轉換。 || Configure addressing, set EN and wait for NRDY0, allowing at least the declared timeout interval.
Ready 且健康正常後才能依支援用途讀寫；不需要先設 CC.EN=1 才能啟用 PMR。 || Use supported accesses when ready and healthy; CC.EN need not be enabled first.
PMRTO 是 Host 應給的等待時間，不可直接寫成 controller 每筆命令的 timeout。CBA 無效另看 CBAI。 || PMRTO is a transition wait allowance, not a per-command timeout; invalid addressing is reported by CBAI.
能力、EN、NRDY、HSTS 與 mapping 一起成立，才是可使用的配置。 || Combine capability, enablement, readiness, health and mapping evidence.
先檢查是否把 NRDY=1 誤看成 Ready，或漏算 PMRTU 的分鐘／500 ms 單位。 || First check inverted readiness and timeout units.
''')
q(233,"PMR 未 Ready、發生錯誤或過早存取時會怎樣？ || What happens for not-ready or unhealthy PMR accesses?", '''
存取在傳輸層完成，不表示記憶體內容有效；PMR 必須同時檢查自身狀態。 || Completion of an access does not establish valid contents without PMR status.
直接 PMR 讀寫與 NVMe 命令使用 PMR buffer，兩者的錯誤觀察方式不同。 || Direct accesses and commands using PMR buffers expose errors differently.
檢查 EN、NRDY、HSTS、ERR；HSTS 在 not-ready 時清零，因此零 HSTS 不能單獨證明健康可用。 || Inspect EN/NRDY/HSTS/ERR; HSTS clears when not ready, so zero alone does not prove usable health.
Not-ready 直接讀可成功卻回 undefined；直接寫可成功卻不更新內容。HSTS 可表示 Restore Error、Read Only 或 Unreliable。 || Not-ready reads can succeed with undefined data and writes can succeed without updating memory; health distinguishes restore failure, read-only and unreliable states.
先確認 Ready，再存取；完成後用支援的 barrier 與狀態檢查，遇到健康改變則回查上次正常觀察後的操作。 || Establish readiness, access, then verify barriers/status and reconsider accesses since the last normal health observation.
NVMe 命令成功把資料寫向 PMR，也不單憑 CQE 保證 PMR 實際寫入成功。 || A successful NVMe command targeting PMR does not alone prove the PMR write succeeded.
若關聯 controller 偵測命令寫 PMR 未成功，應以 Data Transfer Error 中止；直接 MMIO 存取沒有可要求的 NVMe CQE。 || Detected failure writing an associated PMR should produce Data Transfer Error for the command; direct accesses have no NVMe CQE.
將 CQE 成功與 PMRSTS 正常分別核對，不可用其中一項替代另一項。 || Validate command success and PMR health separately.
先檢查存取當時 EN／NRDY，而不只看較晚恢復後的狀態。 || First inspect readiness at access time, not merely after later recovery.
''')
q(234,"Host 如何安全停用 PMR？ || How is PMR safely disabled?", '''
停用前要先確認先前寫入已完成且持久，避免把仍在路上的寫入誤當成保存完成。 || Establish completion and persistence before disabling rather than assuming in-flight writes are safe.
包含直接 PMR 存取與仍以 PMR 為 buffer 的命令，所有使用者都要協調停止。 || Coordinate direct users and commands still using PMR buffers.
查 PMRWBM 支援的 barrier、PMRSTS 健康與 PMRTO／PMRTU。 || Check supported barriers, health and transition wait units.
依能力可用 PMR memory read 或 PMRSTS read 建立先前寫入已持久的保證；不能假設任意 Register read 都是 barrier。 || Use the advertised PMR-read or PMRSTS-read barrier, not an arbitrary register read.
停止新存取，等相關工作結束，執行支援的 barrier 並確認健康，再清 PMRCTL.EN，等待 NRDY=1。 || Stop accesses, drain users, perform the supported barrier/health check, clear EN and wait for NRDY1.
NRDY=1 表示停用完成到可再次啟用的狀態；先前合法持久內容不因停用就變成 CMB 那樣的 undefined。 || NRDY1 indicates disabled readiness for re-enable; valid persistent content is not made undefined as CMB would be.
ERR 非零或 HSTS 不正常時，不能把停用成功當成先前資料已正確保存；應保留錯誤證據。 || Successful disable cannot prove earlier data valid when error/health state says otherwise.
用 barrier、健康與 EN／NRDY 的順序驗證，不只看最後 EN=0。 || Verify barrier/health and enable-state ordering, not only final EN0.
先檢查所有 PMR 使用者是否已停止，以及 barrier 是否真的受支援。 || First verify quiesced users and the actual supported barrier.
''')
q(235,"Reset 與 Power Cycle 如何影響 PMR 狀態及持久資料？ || How do resets and power cycles affect PMR state and data?", '''
持久資料與目前可存取狀態不同；即使內容應保留，恢復期間仍可能尚未 Ready。 || Persistence and current accessibility differ; restoration can leave retained data temporarily unavailable.
資料保留適用已完成且持久的 PMR 寫入，不擴張到 Host 尚未確認的寫入。 || Retention applies to completed persistent writes, not unverified in-flight writes.
重設前保存 barrier 結果，恢復後讀 EN、NRDY、HSTS、ERR 與 mapping。 || Preserve barrier evidence and inspect enable/readiness/health/mapping after recovery.
HSTS=Restore Error 表示 PMR 現在運作且持久，但前次內容可能未正確恢復；與目前 Unreliable 意義不同。 || Restore Error means current normal persistent operation with possibly incorrect restored content, unlike ongoing Unreliable status.
先恢復 Ready，再驗健康，最後按測試保存的內容核對；若同時做 Sanitize，另依清除規則判斷。 || Restore readiness, inspect health and verify content, accounting separately for Sanitize.
符合前提的持久資料應跨 CLR、停用與 Power Cycle 保留；Register 保留則依 Reset 來源分別檢查。 || Qualified persistent data survives CLR, disable and power cycle; register retention remains source-specific.
PMRSTS.ERR 非零會維持到 PCI Function reset；清 CC.EN 不保證把錯誤清零。 || Nonzero ERR persists until PCI Function reset; clearing CC.EN does not necessarily clear it.
內容、Register 與錯誤狀態分三項驗證，不能只因其中一項符合就宣稱全部通過。 || Verify data, registers and errors as separate requirements.
先確認失去的是已持久內容，還是尚未完成的寫入或尚未恢復的讀取。 || First distinguish persistent-data loss from incomplete writes or premature reads.
''')
q(236,"Host Memory、HMB、CMB 與 PMR 的存取與生命週期如何比較？ || How do host memory, HMB, CMB and PMR lifetimes compare?", '''
同樣是資料地址，背後可能有不同擁有者、初始化責任與可回收條件。 || Equal-looking data addresses can have different owners, initialization duties and reclamation conditions.
普通 Host buffer 由 Host 管理，命令期間供 controller 存取；HMB 專供 controller；CMB 位於裝置；PMR 額外提供持久性機制。 || Ordinary host buffers are command-scoped; HMB is controller-exclusive; CMB is device-local; PMR adds persistence mechanisms.
以 HMPRE、CMB/PMR flags 與每筆命令資料指標，確認實際使用哪一種空間。 || Use capabilities and command pointers to identify the actual space.
普通 buffer 按命令與 queue 生命週期回收；HMB 等停用完成；CMB 重設後需初始化；PMR 保存前需支援的 barrier 與健康確認。 || Reclaim ordinary buffers by command/queue lifetime, HMB after disable, initialize CMB after reset and verify PMR barriers/health.
先畫出 Host 地址、controller 地址與實際記憶體的對應，再標註從何時開始可存取、何時才能回收。 || Map host/controller addresses to physical memory and mark access/reclamation boundaries.
例如一個成功 Write CQE 可結束其來源 Host buffer 使用，但不代表整塊 HMB 同時釋放，也不代表 PMR barrier 已執行。 || A Write completion can end source-buffer use without releasing HMB or performing a PMR barrier.
錯誤回應依違反哪個介面規則決定，不存在統一「記憶體錯誤」Status 可套用全部情況。 || Error outcomes depend on the violated interface, not one universal memory-error status.
核對 ownership、mapping、命令完成與持久性各自的證據，避免用「還能讀到資料」代替全部驗證。 || Verify ownership, mapping, completion and persistence rather than merely readable contents.
先確認正在比較的是哪個生命週期：命令、HMB 配置、CMB mapping，還是 PMR 的持久資料。 || First identify whether the lifetime is a command, HMB allocation, CMB mapping or persistent PMR data.
''')
