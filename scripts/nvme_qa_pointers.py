"""Q276–285: PRP/SGL construction and evidence-aware error checks."""
from scripts.nvme_qa_extension import question
from scripts.nvme_qa_model import COMMON, REFS, pair
REFS['pointers']='B|4.2.1, 4.3.1–4.3.2 (PCIe-applicable layouts)|166-168,184-190|93, 110–122'
REFS['sgls']='B|5.2.14.2.1 (SGLS)|403-404|338'
REFS['retirement']='P|3.4 (Command Related Resource Retirement)|13|'
COMMON['pointer_op']={**COMMON['command'],**COMMON['queue'],
 12:pair("""Controller Level Reset 會中止未完成的命令；Host 應確認重設已完成、controller 已不再存取原本的記憶體，才回收資料 buffer 與 PRP／SGL 清單。清單仍留在 Host 記憶體中，不代表原命令可以繼續執行；新命令必須重新確認完整的位址、長度及記憶體生命週期。 || After Controller Level Reset, confirm reset completion and retirement of controller accesses before reclaiming buffers or PRP/SGL lists. Residual list bytes do not resume the old command; validate addresses, lengths and memory lifetime for every new submission."""),
 13:pair("""NVM Subsystem Reset 後，受影響 controllers 的原命令與 queue 已失效。若不同 controllers 曾共用同一份 buffer，Host 必須逐一確認相關存取都已結束，不能只因其中一台完成重設，就回收其他 controller 仍可能使用的記憶體。 || Subsystem reset invalidates old commands and queues on affected controllers. For shared host buffers, retire every relevant controller access before reclamation; one controller’s reset completion does not retire another’s access."""),
 14:pair("""重新上電後需重新初始化及建立 queue；舊 PRP／SGL 位元組即使仍在 Host 記憶體中，也不代表位址映射與存取權限仍然有效。重新提交前，Host 要確認這些記憶體仍屬於自己，並依新命令需要的資料長度重建或核對清單。 || Reinitialize queues after power cycling. Residual PRP/SGL bytes do not prove that address mappings or access permissions remain valid; verify ownership and reconstruct or validate the list for the new transfer."""),
 15:pair("""PRP／SGL 描述的是命令使用的 Host 記憶體，不會自行改變 namespace 的範圍。然而，若錯誤位址指向另一筆命令或另一個 controller 正在使用的 buffer，影響就可能超出原命令。Host 需分清各筆記憶體的擁有者及可回收時點，避免多個使用者互相覆寫。 || PRP/SGL layout does not change namespace scope, but an incorrect address can damage buffers used by other commands or controllers. Track buffer ownership and retirement so concurrent users cannot overwrite each other’s memory."""),
}
def q(n,t,b,o=None):question(n,t,'pointer_op',['pointers','sgls','retirement','status','error','create'],b,o)

q(276,"PRP1 如何描述第一頁的資料？ || How does PRP1 describe the first data page?",'''
PRP 將連續的命令資料分配到記憶體頁面；第一筆指標也描述資料在第一頁從哪個位置開始。 || PRPs map a command’s data stream onto memory pages, including the start within the first page.
這裡的頁面是 CC.MPS 決定的記憶體頁面，不是 SSD 的 NAND page，也不是 namespace 的 LBA。 || These are CC.MPS memory pages, not NAND pages or namespace LBAs.
先讀 CAP.MPSMIN／MPSMAX 與已設定的 CC.MPS，頁面大小是 2^(12+MPS) bytes。 || Check supported and selected MPS; page size is 2^(12+MPS) bytes.
一般資料傳輸的 PRP1 分成頁基底與頁內 offset，offset 最低兩位須為0；特殊命令可另定義 PRP1 為清單指標。 || Ordinary PRP1 contains a page base and Dword-aligned offset; special commands can instead define a list pointer.
先算第一頁剩餘容量 P−offset，再與命令資料長度比較，決定是否需要 PRP2。 || Calculate P−offset before deciding whether more pages are required.
假設 P=4096、offset=1024、資料2048 bytes，第一頁可容納3072 bytes，因此 PRP1 已足夠，PRP2 保留不用。 || With page 4096, offset 1024 and length 2048, the 3072-byte remainder suffices and PRP2 is reserved.
Create Queue 對 PRP1 有 page-aligned 要求，不能套一般資料第一頁可帶 offset 的規則。 || Create Queue requires page-aligned PRP1 and does not inherit ordinary first-data-page offset freedom.
用資料長度、offset 與頁面大小一起驗證；只看長度小於一頁仍可能跨頁。 || Verify length with offset and page size; a sub-page transfer can still cross a boundary.
先檢查 CC.MPS 與 buffer 起點，而不是先數 PRP entries。 || First check selected MPS and buffer start.
''')
q(277,"PRP2 何時是第二頁，何時是清單？ || When is PRP2 a second-page address or a list pointer?",'''
PRP2 的意義由跨越的記憶體頁面邊界數決定，沒有另外一個「這是清單」旗標。 || Boundary crossings determine PRP2 meaning without a separate list flag.
適用於採一般 PRP 資料配置的命令；命令專用定義優先。 || This applies to ordinary PRP data layouts, subject to command-specific definitions.
從 CC.MPS、PRP1 offset 與完整資料長度算需要幾頁。 || Derive the required pages from MPS, first offset and total length.
資料全部放得進第一頁時，PRP2 是保留欄位。資料跨到第二頁、但不需要第三頁時，PRP2 直接存放第二頁的位址；若還需要第三頁或更多頁，PRP2 就改為存放 PRP List 的位址。 || PRP2 is reserved for no crossing, a second-page pointer for one crossing, and a list pointer for more.
先從資料總長度扣除第一頁可容納的 bytes，再看剩餘資料是否超過一頁。這個計算決定 PRP2 指向資料頁還是清單頁，因此不能只看 PRP2 的數值猜用途。 || Subtract first-page capacity and compare the remainder with one page.
例如頁面大小 P=4096 bytes，而 PRP1 的頁內 offset=1024 bytes，第一頁還能放3072 bytes。傳輸4096 bytes 時，剩餘1024 bytes 放在第二頁，PRP2 直接指向該頁；傳輸8192 bytes 時，剩餘5120 bytes 需要兩個資料頁，因此 PRP2 必須指向列出這兩頁位址的清單。 || With 4096-byte pages and an initial offset of 1024 bytes, the first page holds 3072 bytes. A 4096-byte transfer leaves 1024 bytes for a directly addressed second page. An 8192-byte transfer leaves 5120 bytes across two further data pages, so PRP2 points to their address list.
類型選錯可能使 controller 把資料 bytes 當成位址；不能期待一定在所有錯誤傳輸前檢出。 || A wrong interpretation can turn data into addresses; detection before any transfer is not guaranteed.
檢查 PRP2 指向內容與推導的類型一致，而非只檢查它是不是非零。 || Verify the pointed content matches the derived role, not merely a nonzero address.
先重算跨頁次數，包含第一頁 offset。 || First recalculate boundary crossings including the initial offset.
''')
q(278,"PRP List 如何串接多頁？ || How are multiple PRP-list pages chained?",'''
清單頁存放資料頁位址；資料多到清單本身也放不下時，才需要串接下一個清單頁。 || List pages store data-page addresses; additional list pages are chained when necessary.
清單描述尚未由命令內 PRP 描述的資料，不得重複第一頁。 || The list covers data not already described by in-command PRPs.
以 CC.MPS 與每個 PRP entry 的8-byte大小，算清單可放幾筆。 || Use page size and eight-byte entries to calculate capacity.
若仍需下一個清單頁，目前頁的最後一筆改放下一頁清單位址；後續清單頁必須 page-aligned。 || A nonfinal list page uses its last entry as a page-aligned link to the next list page.
逐頁填滿必要 entries，只有還有資料需要描述時才使用鏈結；不能保留無意義的空洞。 || Pack only required entries and use a chain only when additional coverage is necessary.
4KiB 且從頁首開始的清單有512格；非最後頁最多511個資料頁位址加1個鏈結，最後頁才可全放512個資料頁。 || A page-aligned4 KiB list has 512 slots:511 data pointers plus a link when nonfinal, or up to 512 data pointers when final.
最後一格是不是鏈結由剩餘資料量決定；不能把每頁最後一格一律當資料，或一律當鏈結。 || Remaining transfer length determines whether the final slot is data or linkage.
Host 要保留清單直到命令完成；描述 queue 的清單則需保留到 queue 刪除成功或 controller reset。 || Retain command lists until completion, but queue lists until successful deletion or reset.
先核對資料頁總數與鏈結占用的 entry 數。 || First reconcile data-page count with slots consumed by links.
''')
q(279,"PRP 位址、Offset 與 List 有哪些對齊要求？ || What alignment rules apply to PRPs and lists?",'''
資料起點與清單起點的對齊要求不同，不能只使用一個「所有指標皆4KiB對齊」規則。 || Data and list starts have different alignment rules; not every pointer must be4 KiB aligned.
對齊依目前 CC.MPS 及指標角色判斷，不依作業系統恰好使用的頁面大小。 || Apply selected MPS and pointer role, not an assumed OS page size.
確認第一筆資料、命令內第一個清單指標、清單內資料位址或後續清單鏈結是哪一種。 || Identify first data, first list pointer, list data entry or chained-list pointer.
一般 PRP1 可帶 Dword-aligned offset；第一個 PRP List 指標需 Qword 對齊且可有頁內 offset；後續資料頁與鏈結頁需 page-aligned。 || Ordinary first data is Dword aligned; the first list pointer is Qword aligned with possible page offset; later data and list pages are page aligned.
先檢查對齊，再算第一個清單頁從起點到頁尾還容納多少 entries。 || Check alignment and remaining capacity of the first list page.
4KiB 頁內清單起點 offset=4080，可放2筆；若仍需串接，其中最後1筆必須作鏈結。 || A first list starting at 4080 within a 4 KiB page has two slots, with the last used for linkage if needed.
資料 PRP 最低兩位非零時可回 PRP Offset Invalid；若未回錯，須視為兩位清零。後續頁 offset 非零則規範建議回此錯誤，不能把 should 升成必然。 || Low-two-bit violations may produce PRP Offset Invalid or must be treated as cleared; nonzero later-page offsets should produce that error.
Host 仍必須送合法對齊；controller 可以容錯不代表 Host 的要求就消失。 || Permitted controller tolerance does not remove host alignment obligations.
先分清「Host 必須如何填」與「Controller 必須或可以如何處理錯誤」。 || First distinguish host construction requirements from controller error behavior.
''')
q(280,"PRP 為0、位址無效或鏈結錯誤時，能指定同一種錯誤嗎？ || Do zero, invalid or broken-chain PRPs have one universal error?",'''
0 是位址數值，不是 NVMe 為所有 PRP 定義的通用空指標；是否能存取還取決於實際記憶體映射。 || Zero is an address value, not a universal NVMe null pointer; accessibility depends on memory mapping.
先區分欄位格式錯誤、描述長度錯誤與實際資料搬移失敗。 || Separate format, coverage and actual transfer failures.
核對 CC.MPS、PRP 角色、需要的頁數與 Host 提供的有效記憶體範圍。 || Check MPS, pointer roles, required pages and accessible memory ranges.
非法 offset 可對應 PRP Offset Invalid；格式合法但 DMA 存取失敗可能對應 Data Transfer Error，不能只憑位址0判定。 || Invalid offsets differ from transfer failures; address zero alone does not establish either result.
建立一個合法基準，再只改一處；先查清單是否指向預期頁，再檢查整個傳輸所需範圍。 || Isolate one change from a valid baseline and inspect the complete required address coverage.
合法且可存取的配置可正常完成；保留的 PRP2 即使為0，也不構成缺少資料頁。 || A valid accessible layout can succeed, and reserved PRP2 zero is not a missing page.
規範沒有替每種循環鏈結或不可存取位址規定唯一可預測 CQE；若命令通道受破壞，也不能保證取得 CQE。 || No unique CQE is defined for every malformed chain or inaccessible address, especially if communication fails.
保存原 SQE、清單快照與位址配置，避免出錯後 Host 改寫清單，導致證據已不同。 || Preserve SQE, list contents and mapping before host changes obscure evidence.
先確認指標真的被命令使用，而非保留欄位或未走到的清單部分。 || First establish that the command actually uses the pointer.
''')
q(281,"SGL Data Block、Segment 與 Last Segment 如何配合？ || How do SGL data, segment and last-segment descriptors work?",'''
Data Block 描述資料位址與長度；Segment 類型描述下一段 descriptor 清單，而不是資料本身。 || Data blocks describe payload; segment descriptors describe another descriptor array.
SGL 用於支援它的 PCIe I/O 命令；PCIe Admin 命令不得使用 SGL。 || SGLs apply to supported PCIe I/O commands, not PCIe Admin commands.
先確認 Identify.SGLS，再看 CDW0.PSDT 的 data／metadata 配置。 || Establish SGL support and PSDT data/metadata layout.
每個 descriptor16 bytes；Data Block 類型0h，Segment2h，Last Segment3h。Segment 的 LEN 是下一段清單的 bytes。 || Descriptors are 16 bytes; types 0h/2h/3h distinguish data, segment and last segment, whose length describes descriptor bytes.
只有一個資料區塊時，可直接放在命令 SGL1；多區塊時，SGL1 指向清單，再逐筆讀 Data Block。 || One block fits directly in SGL1; multiple blocks use a pointed descriptor array.
例如 Last Segment.LEN=32，代表下一段有2個 descriptors，不代表命令只傳32 bytes；實際資料量看那兩筆 Data Block.LEN。 || Last Segment length 32 means two descriptors, not32 payload bytes; payload length comes from those entries.
鏈結 descriptor 只能在目前段最後一筆；Last Segment 指向的最後段不得再含任何鏈結 descriptor。 || Link descriptors must be last in their segment, and a last segment cannot contain another link.
分開計算 descriptor bytes 與 payload bytes，才能核對清單完整性及命令長度。 || Account descriptor and payload bytes separately.
先檢查 LEN 是屬於哪種 descriptor。 || First identify the descriptor owning each length.
''')
q(282,"SGL 位址、長度、數量與類型錯誤如何區分？ || How are SGL address, length, count and type errors distinguished?",'''
不同 SGL 錯誤指出不同的壞掉環節，不能全部簡化成 Invalid Field。 || Specific SGL errors identify different malformed structures rather than one generic invalid field.
分開 data SGL 與 metadata SGL，兩者長度錯誤有不同 Status。 || Data and metadata SGL length errors have distinct statuses.
查 SGLS 的對齊、LLDTS 及支援 descriptor 類型，再核對命令要求長度。 || Check alignment, longer-length support, descriptor types and requested transfer length.
Segment 位址需 Qword 對齊，LEN 非零且為16倍數；Data Block.LEN=0 合法，代表不傳資料。 || Segment addresses are Qword aligned with nonzero16-byte-multiple lengths; zero-length data blocks are valid.
沿鏈逐段核對邊界、最後一筆位置、type/subtype，以及全部有效資料長度。 || Traverse boundaries, link position, type/subtype and aggregate data coverage.
SGL 至少要涵蓋要求的資料量；LLDTS=1 允許較長，仍只按命令要求傳輸。 || The SGL must cover the request; LLDTS1 permits excess capacity without enlarging the transfer.
鏈結不在最後一筆須0/0Eh；最後段再鏈結須0/0Dh；不支援類型須0/11h；資料／metadata過短分別須0/0Fh、0/10h。 || Misplaced links require 0/0Eh; links inside a last segment0/0Dh; unsupported types 0/11h; short data/metadata0/0Fh or 0/10h.
LLDTS=0 的過長清單建議不要因此中止；若因此中止，建議用對應長度錯誤。對齊錯誤還須保留各欄定義的 may／should 強度。 || Excess length with LLDTS0 should not cause abort; if it does, the corresponding length status is recommended. Alignment rules retain their may/should strengths.
先找第一個能以結構證明的違規，不憑最終資料不對就猜 descriptor 類型錯誤。 || First establish a concrete structural violation rather than infer one from bad data.
''')
q(283,"Identify 的 SGL 能力如何限制合法用法？ || How do Identify SGL capabilities constrain usage?",'''
SGL 支援不是只有一個 yes/no；資料對齊、額外類型、metadata 與較長清單都有各自能力。 || SGL capability includes alignment, optional types, metadata and excess-length support.
能力還須配合傳輸與命令種類；Base 表列某個類型，不等於所有 PCIe 命令都可使用。 || Capabilities remain constrained by transport and command type.
SGLS[1:0]=00不支援、01支援且 Data Block 無對齊粒度限制、10要求 Dword 對齊與粒度。 || SGLS low bits encode unsupported, unrestricted data-block alignment, or Dword alignment/granularity.
LLDTS 控制較長清單，SBBDS 控制 Bit Bucket，MSDS 與 MBA 控制 metadata 配置；SDT 是建議 descriptor 數。 || LLDTS, SBBDS, MSDS/MBA and SDT respectively cover excess length, bit buckets, metadata and recommended count.
先選合法 PSDT，再只使用已宣告且 PCIe 允許的 type/subtype；Offset subtype 不能因看到其他傳輸定義就套用。 || Select valid PSDT and supported PCIe types/subtypes; do not import another transport’s offset format.
SGLS=10b 時，Data Block 位址與長度須是4-byte倍數；這不表示每個資料區塊都要 page-aligned。 || Dword granularity requires four-byte address/length multiples, not page alignment.
超過 SDT 可能降低效能，但 SDT 不是一律拒絕命令的硬上限；不得把 capsule 專用欄位當成 PCIe 清單上限。 || Exceeding SDT may reduce performance; it is not a universal rejection limit, and capsule-only limits do not define PCIe list limits.
支援宣告與合法描述資料必須一致；Admin 命令的 SGL 禁用規則仍優先。 || Legal behavior must match capabilities while retaining the Admin SGL prohibition.
先完整解碼 SGLS，而不是只看整個欄位非零。 || First decode individual SGLS fields instead of testing nonzero.
''')
q(284,"Data Pointer 錯誤與 Data Transfer Error 有何不同？ || How do pointer-format errors differ from Data Transfer Error?",'''
Pointer 錯誤表示描述方法不合法；Transfer Error 表示資料或 metadata 搬移失敗，兩者不能用同一個原因解釋。 || Pointer errors concern description validity; transfer errors concern moving data or metadata.
錯誤可能在清單檢查或實際存取時才被發現，時間不同。 || Detection can occur during descriptor validation or memory access.
先檢查 PRP／SGL 規則與完整範圍，再核對當時記憶體是否仍有效。 || Validate layout/coverage and memory lifetime at the time of access.
記錄 PSDT、指標、長度、SCT／SC、SQID、CID；Error Information 的 PEL 是 Parameter Error Location，不是 Persistent Event Log。 || Preserve layout and completion fields; Error Information PEL means Parameter Error Location, not Persistent Event Log.
先排除 Host 提早回收 buffer，再檢查合法位址是否能被 controller 存取。 || Exclude premature buffer reclamation before diagnosing access to a valid address.
格式合法、範圍完整且搬移成功，仍需命令本身完成才有 Success；指標合法不代表媒體操作一定成功。 || Valid pointers and successful transfer do not alone prove the requested media operation succeeded.
Data Transfer Error 為0/04h；PRP Offset 與各 SGL 結構錯誤則用各自 Status，不能把所有傳輸錯誤一律定為 Host 格式錯誤。 || Data Transfer Error is 0/04h, distinct from pointer-format statuses; not every transfer failure is a host formatting error.
SGL 可以先傳輸合法部分，之後才發現另一筆錯誤；失敗 CQE 不證明 buffer 完全未修改。 || Valid SGL portions may transfer before another descriptor fails; an error CQE does not prove an untouched buffer.
先對照原始描述資料與實際存取時點，不使用完成後才重建的清單代替原件。 || First compare original descriptors with the actual access lifetime.
''')
q(285,"PRP／SGL 錯誤如何與 CQE 及 Error Information 對回？ || How are pointer errors correlated with completion and Error Information?",'''
把錯誤對回原命令，才能知道哪個指標或資料範圍需要修正。 || Correlation identifies the original pointer or range requiring correction.
使用同一 controller、同一 queue 使用期間及相同 SQID／CID；CID 可能重用，單看數字不夠。 || Match controller, queue lifetime and SQID/CID; reusable identifiers alone are insufficient.
保存 CQE 的 SCT、SC、DNR、More，再依適用規則讀 Error Information。 || Preserve status and auxiliary bits before reading applicable error information.
Error Count、SQID、CID、Status 與 Parameter Error Location 可協助比對；無法指出欄位時，需保留其無效／未指定表示。 || Error count, command identity, status and parameter location help correlation, including invalid/unspecified location encodings.
先對命令身分與狀態，再判讀 byte／bit 位置；清單內容在 Host memory 時，不能硬把每個錯誤都映成 SQE 某一bit。 || Correlate identity/status before byte/bit locations; list-memory errors need not identify a unique SQE bit.
找到相符紀錄後，可將原始欄位、違規條件與實際 Status 放在一起驗證。 || A matched record connects original fields, violated conditions and returned status.
More=0 不證明一定沒有 Error entry；也不是每個失敗命令都要求新增 entry。DNR=0 更不代表可用同一個壞清單直接重試。 || More0 does not prohibit an entry, not every error requires one, and DNR0 does not justify reusing a malformed list.
若記錄已被覆蓋或重設後清除，說明證據不足；不能將缺少歷史紀錄當成原命令合法。 || Overwritten or reset-cleared history limits evidence rather than proving validity.
先保存原命令與清單，避免重試時覆寫唯一能定位問題的內容。 || First preserve the original command/list before retry overwrites them.
''')
