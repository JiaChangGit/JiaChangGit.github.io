"""Independent FDP course: context, reasoning and worked examples."""
BASE = 'NVME-BASE-2.4'
NVM = 'NVME-NVM-CS-1.3'
REPORT_ID = 'base-flexible-data-placement'


def bi(zh, en):
    return dict(zh=zh, en=en)


UNITS = []


def unit(key, zh, en, section, pages, summary, english, example, example_en, steps, reading, source=BASE):
    UNITS.append(dict(key=key, title=bi(zh,en), section=section, pages=pages, source=source,
      summary=bi(summary,english), example=bi(example,example_en), steps=steps,
      reading=bi(reading, 'Read the referenced structures as parts of this mechanism; distinguish identifiers, counts, units, and the state being reported.')))


unit('model','先看資料為何需要一起回收','Why group data for reclamation','8.1.12.1','673-676',
 'FDP 讓主機依資料使用方式安排寫入，目標是減少媒體回收時搬移仍有效資料的成本。功能以 Endurance Group 為範圍；LBA 決定邏輯位置，Placement Identifier 則透過 namespace 的對照關係選擇目前接收資料的 Reclaim Unit。',
 'FDP lets the host organize writes around data usage to reduce valid-data movement during reclamation. It operates within an Endurance Group. LBA selects a logical address, while a Placement Identifier follows a namespace mapping to the Reclaim Unit currently receiving data.',
 '說明性案例：短期暫存 A、B 今天失效，長期資料 C 下週才失效。若三者混在需要一起回收的媒體中，今天清理 A、B 時仍可能要搬 C；把生命週期相近的資料分組，才有機會減少這種搬移。',
 'Illustrative case: temporary data A/B expires today while C remains valid for a week. Mixing them can require moving C when reclaiming space from A/B. Grouping similar lifetimes can reduce that movement.',
 [('從主機看見的更新開始','檔案系統把某個 LBA 的內容改掉，並不表示 SSD 已經原地覆寫同一塊媒體。裝置可能把新內容放到別處，原位置成為不再需要的舊資料。回收空間時，若同一批媒體仍夾著有效資料，控制器就需要保留或搬移那些資料。這是理解 FDP 的出發點。'),
  ('主機提供的是分組資訊','主機較容易知道哪些資料會一起失效，例如同一批可整體刪除的暫存檔。FDP 讓主機把這種關係反映到資料放置上，但不把 NAND 實體位址交給主機管理，也不保證任意分組都能改善寫入量；分錯生命週期，仍可能留下需要搬移的資料。'),
  ('先分清楚 4 層物件','Endurance Group 裡有一個或多個 Reclaim Group；每個 Reclaim Group 裡有多個 Reclaim Unit。Reclaim Unit Handle 在每個 Reclaim Group 各持有一個目前可寫入單位的參照。因此只說 RUH 3 還不夠，還需要知道是哪一個 Reclaim Group。'),
  ('Handle 會持續存在，所指單位會換','當目前的 Reclaim Unit 寫滿，控制器把相應參照改到同一 Reclaim Group 的另一個空單位。主機後續仍可使用相同 handle；相同 PID 並不是某塊媒體永久不變的地址。切換也不表示之前寫入的有效資料已刪除。'),
  ('把模型接回 namespace','每個 namespace 的 Placement Handle List 將 PHNDL 對應到 RUHID。主機寫入時帶 NSID、LBA 和 PID；控制器先從 PID 取 PHNDL 與 RGID，再查 namespace 的表，最後選到目前的 RU。這幾個步驟會在後文使用同一組數值逐步演算。')],
 'Base 70 看層次與參照，730 再加上 namespace 的映射。兩張圖的用途不同：前者回答資源有哪些，後者回答一筆 Write 如何抵達其中一個資源。')

unit('isolation','初次分開寫入，搬移後是否仍分開','Isolation before and after internal relocation','8.1.12.1','675-676',
 '一個 RU 同時最多由一個 RUH 參照，因此不同 RUH 的新寫入起初分開。Initially Isolated 允許控制器搬移後在同一 Reclaim Group 合併同類型 RUH 的資料；Persistently Isolated 則要求搬移目的 RU 只包含同一 RUH 寫入的資料。',
 'An RU is referenced by at most one RUH, so new writes using different handles start separately. Initially Isolated handles allow relocated data from different handles of that type to be combined within the same Reclaim Group. Persistently Isolated handles require a destination RU containing only data written through the same handle.',
 'RUH 1 和 RUH 3 都是 Initially Isolated 時，兩者舊資料搬移後可以進同一 RU；若兩者是 Persistently Isolated，不能因為今天都只剩一點資料，就把兩者有效資料合併到同一 RU。',
 'Relocated data from Initially Isolated RUH 1 and RUH 3 may share an RU. If both are Persistently Isolated, their remaining data cannot be combined merely because each has little data left.',
 [('先看共同點','兩種類型都讓不同 RUH 的新寫入起初放在不同 RU。不能把 Initially Isolated 解讀成完全沒有隔離，也不能把 Persistently Isolated 解讀成控制器不得搬移資料。真正需要比較的是控制器內部搬移之後，哪些資料可以放到同一個目的 RU。'),
  ('Initially Isolated 的允許範圍','RUHT=1h。控制器例如為了垃圾回收，把舊資料搬到同一 Reclaim Group 內的另一個 RU；目的 RU 可以混合其他 Initially Isolated RUH 所寫的資料。原本分組仍影響初次放置，但不能據此假設搬移後每一組都維持各自的 RU。'),
  ('Persistently Isolated 的限制','RUHT=2h。控制器一樣可以在同一 Reclaim Group 內搬移，但目的 RU 只能包含由同一 RUH 寫入的資料。這是資料來源的隔離條件，不是固定實體地址、跨 Reclaim Group 的複製能力，或資料永久保留的承諾。'),
  ('隔離不等於 namespace 隔離','不同 namespace 可以在符合格式等條件時共用同一 RUH。此時即使 RUHT=2h，也不能把該 RUH 的持續隔離當成這些 namespace 彼此隔離；規則的識別對象是 RUH。選用共享或獨立 RUH 前，要先確認應用程式想一起管理的是哪些資料。')],
 'Base 295 定義 RUHT；731 和 732 要比較搬移箭頭的來源與目的 RU，而不是只比較兩張圖的外框。')

unit('config','讀懂候選配置與 PID 的切割方式','Read configurations and the PID layout','5.2.13.1.29','319-322',
 'LID 20h 回傳 Endurance Group 的配置清單。先讀整份大小與每筆 DSZE，再檢查 FDPCV、NRG、NRUH、RUHT、RUNS 等內容。RGIF 決定 16-bit PID 高位有多少 bits 是 RGID，剩餘低位才是 PHNDL；配置索引不是 byte offset。',
 'LID 20h lists configurations for an Endurance Group. Use the log size and each DSZE, then inspect FDPCV, NRG, NRUH, RUHT, RUNS, and related fields. RGIF assigns the high bits of the 16-bit PID to RGID and the remaining low bits to PHNDL. A configuration index is not a byte offset.',
 'NRG=4、RGIF=2、PHNDL=1、RGID=2：PID=(2<<14)|1=8001h。PHNDL=1 的 RUHID 由 namespace 的表決定，不能把 8001h 當成 RUHID，也不能把它當成 LBA。',
 'With NRG=4, RGIF=2, PHNDL=1 and RGID=2, PID=(2<<14)|1=8001h. The namespace mapping determines the RUHID for PHNDL 1; 8001h is neither a RUHID nor an LBA.',
 [('先讀清單外框，再讀一筆配置','NUMFDPC 在 header bytes 1:0，採數量減 1 的編碼；值 1 表示 2 筆配置。SZE 是整份 log 的 byte 數，第一筆從 byte 16 開始。每筆配置可能因 RUH 數與廠商資料長度不同而有不同 DSZE，所以下一筆位置要加上本筆 DSZE，不能假設固定間距。'),
  ('位置、索引與有效性分開','第 0、1、2 筆是清單索引，Set Features 的 FDPCIDX 選這個索引。假設第 0 筆 DSZE=80，則第 1 筆起點是 byte 96；要選它仍填 FDPCIDX=1，不是 96。FDPCV=0 表示該候選目前不可用；建立其他 Endurance Group 或啟用其他配置後，可用性可能改變。'),
  ('用配置判斷數量、類型與大小','NRG、NRUH 是直接計數且非零；RUH 清單依 RUHID 遞增，每筆描述器提供 RUHT。RUNS 是每個 RU 的名目 bytes，ERUTL 是估計時間上限秒數，0 表示未回報。MAXPIDS 則是 Update 可接受的 NPID 編碼上限，不能把這幾個值都當成同一種容量。'),
  ('從一個 16-bit 值取出兩個選擇','RGIF=r 且 r>0 時，RGID=PID>>(16-r)，PHNDL=PID & ((1<<(16-r))-1)。NRG=1 且 RGIF=0 時，16 bits 全部是 PHNDL；NRG=1 但 RGIF 非零也合法，此時 RGID 欄位由控制器忽略。不要自行以 log2(NRG) 取代裝置實際回報的 RGIF。'),
  ('結構長度需要把對齊也算進去','一筆配置先有 64 bytes 固定部分，再加 NRUH×4 bytes 的 RUH 描述器、VSS bytes 的廠商內容，最後補 0 到 8-byte 邊界。例：NRUH=3、VSS=1，未補齊為 77 bytes，補 3 bytes 後 DSZE=80。VS 是廠商資料；沒有廠商定義時不替其中的值編造意義。')],
 'Base 293 看清單索引與總長；294／295 看一筆配置和 RUH 類型；296／297 是 RGIF=0 與非零的兩種 PID 格式。')

unit('enable','啟用的是整個 Endurance Group','Enable the Endurance Group configuration','8.1.12.2','677-678',
 '先查 FDPS 與有效配置，讓目標 Endurance Group 沒有 namespace，再以 FID 1Dh、SV=1 設定 FDPE 與 FDPCIDX。設定值改變後需重新取得資料格式資訊，再建立 namespace；FDP 設定成功改變也會清除該群組的 FDP 事件與統計。',
 'Check FDPS and valid configurations, ensure the target Endurance Group has no namespaces, then set FID 1Dh with SV=1, FDPE and FDPCIDX. After a value change, refresh data-format information before creating namespaces. A successful feature-value change also clears that group’s FDP events and statistics.',
 'ENDGID=2、選配置索引 1：Set Features CDW10=8000001Dh、CDW11=00000002h、CDW12=00000101h。這表示替群組 2 啟用第 1 筆配置；尚未代表某個 namespace 的 Data Placement Directive 已啟用。',
 'For ENDGID=2 and configuration index 1: Set Features CDW10=8000001Dh, CDW11=00000002h, CDW12=00000101h. This enables that group configuration; it does not yet enable a namespace’s Data Placement Directive.',
 [('FDPS 回答能力，不回答目前狀態','Identify Controller 的 CTRATT.FDPS=1 表示支援 FDP；LID 20h 再回答有哪些配置。即使兩者都符合，也還不能直接對現有 namespace 所屬群組改設定。支援、候選可用性與目前啟用狀態是不同問題，必須依次確認。'),
  ('先處理現有 namespace 的原因','FDP 改變的是群組的配置，後續 namespace 的資料格式與 handle 映射也與該配置有關。只要群組還有 namespace，而要求的 FID 1Dh 值又不同於目前值，控制器就以 Command Sequence Error 拒絕。這項規則要求刪除該群組全部 namespace 後才變更，不能把它畫成隨時可以切換的普通開關。'),
  ('把目標、配置與保存分開編碼','CDW11 低 16 bits 是 ENDGID；CDW12 bit 0 是 FDPE、bits 15:8 是 FDPCIDX；Save 在 CDW10 bit 31。此 Feature 可保存、預設 0，值的改變只允許在 SV=1 時進行。支援 SSFS 而 SV=0 的要求會回 Invalid Field in Command。'),
  ('成功後需要重新確認什麼','Feature 值改變時，控制器可以改變 Identify 所提供的資料格式相關資訊。主機應重新查支持的格式，再建立使用 NVM Command Set（CSI=00h）的 namespace。還要保留舊統計的量測終點，因為成功改值會把 FDP Statistics 清 0，並清掉 FDP Events；前後已不是同一段累計期間。'),
  ('報告操作順序不等於立即執行刪除','本文教的是配置條件與流程。完整順序是確認能力與候選、安排既有資料與 namespace 的處理、在空群組保存新設定、重新查格式、建立 namespace 及其映射，再啟用所需 Directive 與事件。這裡不把「設定成功」當成資料已遷移或已安全保存的證明。')],
 'Base 499 選群組，500 選配置與啟用。必要引用中的 Feature 通用欄位解釋 SV、SEL；不要把 Get Features 的能力回覆和目前值回覆混用。')

unit('namespace','建立 namespace 的 Placement Handle 對照表','Create the namespace handle mapping','4.1.6.3','110-113',
 'NPHNDLS 與 Placement Handle List 建立 namespace 私有的 PHNDL→RUHID 對照。主機可明確列出不同 RUH；NPHNDLS=0 則由控制器選一個 RUH 作為 PHNDL 0。共享 RUH 的 namespace 必須使用相同資料格式，且控制器選用與主機明確指定的 RUH 有分配限制。',
 'NPHNDLS and the Placement Handle List define a namespace-local PHNDL→RUHID mapping. A host may list distinct RUHs; NPHNDLS=0 asks the controller to choose one for PHNDL 0. Namespaces sharing an RUH must use the same data format, and controller-selected and explicitly selected handles have allocation restrictions.',
 'NRUH=4，namespace A 的清單為 [1,3]：PHNDL 0→RUHID 1，PHNDL 1→RUHID 3。namespace B 可以用不同 PHNDL 編號指到 RUHID 3，但必須符合共享格式條件；不能因為 A 的 PHNDL 1 有效，就假設 B 也有 PHNDL 1。',
 'With NRUH=4 and namespace A’s list [1,3], PHNDL 0 maps to RUHID 1 and PHNDL 1 to RUHID 3. Namespace B may map a different PHNDL to RUHID 3 subject to the shared-format requirement. A valid handle in A does not automatically exist in B.',
 [('PHNDL 是清單的位置，RUHID 是清單的內容','本例 NPHNDLS=2，bytes 512:513 放 1，514:515 放 3。第 0 筆的位置定義 PHNDL 0，內容 1 才是 RUHID。這是「索引」與「值」的典型差別：寫入帶 PHNDL，控制器查出 RUHID；不能把主機清單 [1,3] 解讀成這個 namespace 只有 PHNDL 1 和 PHNDL 3。'),
  ('主機提供清單時的完整檢查','非零 NPHNDLS 不能大於 NRUH 或 128；每個 RUHID 必須小於 NRUH；同一 namespace 的清單不能重複 RUHID。若列到控制器已為 NPHNDLS=0 的 namespace 選用的 RUH，也會被拒絕為 Invalid Placement Handle List。'),
  ('不提供清單並不是沒有 Placement Handle','NPHNDLS=0 要求控制器替 namespace 建立唯一的 PHNDL 0。若群組已存在這種 namespace，新 namespace 使用相同的控制器選定 RUH；否則控制器需選一個未被主機明確配置的 RUH。沒有可用候選時會回 Invalid Placement Handle List，不能任意借用一個已被明確配置的 RUH。'),
  ('共享需要一致的資料格式','兩個 namespace 明確使用同一 RUH 時，Format Index 必須相同；不一致會回 Invalid Format。只看每個 logical block 的 data bytes 相同還不夠，Format Index 代表整份資料格式選擇。FDP 群組中的 namespace 使用 NVM Command Set，且不能把 NVM Set 配置混進同一個 FDP 配置。'),
  ('建立後取得目前映射與容量','建立命令決定 PHNDL 到 RUH 的關係，但每個 RUH 在各 Reclaim Group 指向的 RU 會隨寫入變化。使用 I/O Management Receive 查目前的 PID、RUHID、剩餘可寫量與時間，才能把建立時的表接到運作中的狀態。Create 與 Attachment 是不同操作；要透過某控制器做 I/O，namespace 還需能由該控制器存取。')],
 'NVM 134 只取 ENDGID、NPHNDLS、Placement Handle List 與必要格式關係；Base 730 用圖把同一張映射表接到 Write。',source=NVM)

unit('directive','分清兩次啟用與三種 Write 情況','Two enablement steps and three Write cases','8.1.9.4','653',
 'FDP 已啟用的群組內，namespace 還需要啟用 Data Placement Directive 才能明確指定 PID。Enable 使用外層 Identify DTYPE=00h，CDW12 目標 DTYPE=02h；Data Placement 本身沒有 Send／Receive 操作。沒有使用 Directive 的寫入則使用 PHNDL 0，讓控制器選 Reclaim Group。',
 'Within an FDP-enabled group, enable the namespace’s Data Placement Directive before explicitly specifying a PID. Enable uses outer Identify DTYPE=00h and target DTYPE=02h in CDW12. Data Placement has no Send/Receive operations of its own. Writes without a directive use PHNDL 0 and a controller-selected Reclaim Group.',
 '啟用 Data Placement：Directive Send CDW11=00000001h、CDW12=00000201h。把外層 CDW11 的 DTYPE 直接填 02h 會被拒絕；02h 是這次 Enable 的目標，不是它的外層管理操作類型。',
 'To enable Data Placement, use Directive Send CDW11=00000001h and CDW12=00000201h. Putting DTYPE=02h in outer CDW11 is rejected; 02h is the enable target, not the outer management operation.',
 [('先確認兩種狀態各屬於誰','FID 1Dh 是 Endurance Group 的 FDP 設定；Data Placement Directive 則套用到指定 namespace，以及適用的主機身分與共享控制器關係。群組有能力並已啟用，不會自動證明某主機已替 namespace 啟用 Directive。'),
  ('Enable 由 Identify Directive 處理','Directive Send 外層選 DTYPE=00h、DOPER=01h，再由 CDW12 的 DTYPE=02h、ENDIR=1 指定目標。若 namespace 不在已啟用 FDP 的群組，回 FDP Disabled；若用 NSID=FFFFFFFFh 要一次啟用所有 namespace，回 Invalid Namespace or Format。應逐一對有效 namespace 設定。'),
  ('為何不能直接對 Data Placement 發管理操作','§8.1.9.4 沒有定義 Data Placement 的任何 Directive Operations。因此 Send 或 Receive 若在 CDW11 直接選 DTYPE=02h，回 Invalid Field in Command。查能力使用 Identify Directive 的 Return Parameters；查 RUH 狀態與更新參照則使用 I/O Management 命令，各入口有不同工作。'),
  ('DTYPE 被忽略、明確使用與非法類型','I/O 中若沒有任何 I/O Directive 啟用，或 DTYPE=00h，控制器忽略 DTYPE／DSPEC；FDP 群組裡這種寫入使用 PHNDL 0，RG 由控制器選。若 Directive 有效且 DTYPE=02h，才解讀 DSPEC 為 PID。若已有 I/O Directive 啟用，卻選不支援或未啟用的類型，則以 Invalid Field in Command 拒絕。'),
  ('保存的啟用狀態不代表參照不變','Data Placement 的 DPDIRCLR=1 表示其啟用狀態跨 Controller Level Reset 保留；但 RUH 目前指向哪個 RU、剩餘容量與事件仍需重新查。不要因為 Enable 不必照搬 Streams 的 reset 規則，就省略後續 FDP 狀態恢復流程。')],
 'Base 705 分 supported／enabled／reset persistence，706 看目標 DTYPE；186 看外層 DTYPE，兩個欄位不能互換。')

unit('write','把一筆 Write 走完，包含非法 PID','Follow one Write, including invalid PIDs','8.1.12.3','678',
 '明確放置的 Write 用 DTYPE=02h、DSPEC=PID；LBA 與區塊數仍決定邏輯資料。PID 的 RGID 或 PHNDL 無效時，控制器另選該 namespace 可存取的 RG／RUH 來處理放置，並在所選 RUH 已啟用該事件時記錄 Invalid Placement Identifier；不能把這個規則套到 Update。',
 'An explicit-placement Write uses DTYPE=02h and DSPEC=PID while LBA and block count define the logical data. If RGID or PHNDL is invalid, the controller chooses an accessible RG/RUH and records Invalid Placement Identifier if enabled on the selected RUH. This Write rule does not apply to Update.',
 '沿用 PHNDL 1→RUHID 3、RGIF=2：寫 LBA 128 起的 8 blocks，PID=8001h。在 CETYPE=0 且其餘選項清 0 的例子，CDW10=00000080h、CDW11=0、CDW12=00200007h、CDW13=80010000h。',
 'With PHNDL 1→RUHID 3 and RGIF=2, write eight blocks starting at LBA 128 using PID=8001h. With CETYPE=0 and other options zero, CDW10=00000080h, CDW11=0, CDW12=00200007h, and CDW13=80010000h.',
 [('固定其他條件，觀察 PID 的作用','假設 namespace A 可存取、Data Placement 已啟用，映射 [1,3]，NRG=4、RGIF=2。PID=8001h 指 RG 2 與 PHNDL 1，查表得到 RUH 3。控制器把這次資料放到 RUH 3 在 RG 2 目前參照的 RU；LBA 128 是 namespace 的邏輯位置，與 RG 2 不是同一層地址。'),
  ('把命令長度與放置選項分開','8 blocks 的 NLB 是 7，位於 CDW12 bits 15:0；DTYPE=2 位於 bits 23:20。CETYPE=0 的格式下，PID 放在 CDW13 高 16 bits。不能把 PID 填入 SLBA，不能把 8 直接填成 NLB，也不能把這個 CDW13 例子無條件套到非零 CETYPE。'),
  ('沒有明確帶 PID 時仍有 FDP 放置','若本例 Write 不使用 Directive，PHNDL 自動採 0，因而查到 RUHID 1；Reclaim Group 由控制器選。這不表示離開 FDP 群組，也不表示控制器把非零 DSPEC 自動當作 PID。是否解讀 DSPEC 先取決於 Directive 規則。'),
  ('非法 PID 的資料與事件分開判斷','假設改成 PHNDL=2，但 A 只有 PHNDL 0、1。控制器為這次 Write 選擇 A 可存取的 RG／RUH；這個放置錯誤本身不是要求 Write 必須失敗。事件是否出現還取決於實際所選 RUH 是否啟用了 Invalid Placement Identifier；想收到此事件，應在所有 RUH 啟用它。其他命令錯誤仍可能使 Write 失敗。'),
  ('寫入完成與媒體持久化分開','FDP 沒有取消 volatile write cache 的差別。有些配置帶 cache，有些 namespace 由 VWCNP=1 明確表示沒有。完成 Write 不應一律解讀成已寫入非揮發媒體；需要持久化時使用原本的 FUA／Flush 規則。FDP 的分組選擇也不額外提供原子寫入保證。')],
 'NVM 70 看 SLBA，71 看 NLB／DTYPE／CETYPE，72 看 DSPEC。Base 346 的 VWCNP 與 338 的 VWCP 解釋為何群組配置與 namespace 的 cache 要分層讀。')

unit('status','查目前可寫容量，別把回覆當成永久保證','Inspect available writes and remaining time','3.2.1.1','26',
 'I/O Management Receive 的 MO=01h 逐一回傳 namespace 每個 PHNDL、每個 RG 的狀態。NVM 描述器含 PID、RUHID、EARUTR 秒數與 RUAMW logical blocks；回覆是處理當下的狀態，未必反映其他未完成命令，且 RUNS 只是名目大小。',
 'I/O Management Receive MO=01h reports each namespace PHNDL for each RG. NVM descriptors contain PID, RUHID, EARUTR in seconds, and RUAMW in logical blocks. Each descriptor reflects processing-time state, may not reflect outstanding commands, and need not match nominal RUNS.',
 '2 個 PHNDL、4 個 RG 共 8 筆描述器，大小=16+8×32=272 bytes，NUMD=67。某筆 RUAMW=6、block data size=4096 bytes，表示當時尚可寫 24576 bytes；不是還有 6 個 RU。',
 'Two PHNDLs and four RGs produce eight descriptors: 16+8×32=272 bytes, so NUMD=67. RUAMW=6 at 4096 bytes per logical block represents 24576 bytes available at that instant, not six RUs.',
 [('查詢對象是 namespace，不是 ENDGID','I/O Management Receive 用 NSID 指定可存取的 namespace；MO=01h，這個操作沒有定義 MOS 的額外選擇。NSID=0 或 FFFFFFFFh 會回 Invalid Namespace or Format，FDP 未啟用則回 FDP Disabled。這和 LID 20h～23h 用 ENDGID 選群組不同。'),
  ('先讀 header，再按 32 bytes 前進','header 是 16 bytes，NRUHSD 位於 bytes 15:14，直接表示描述器數量。第 i 筆從 16+32×i 開始。NVM 排序先 PHNDL 遞增，再 RGID 遞增：先看 PH0/RG0、PH0/RG1…，才輪到 PH1。這有助於核對相同 PH 在不同 RG 的狀態。'),
  ('容量與時間各回答一個問題','RUAMW 是當時仍可寫入的 logical block 數；EARUTR 是目前 RU 估計還可維持被參照的秒數，0 表示沒回報時間，不表示立即到期。ERUTL 是配置層的估計上限，EARUTR 是這次狀態中的剩餘估計，不該用相同數值替代。'),
  ('實際容量可能大於或小於名目大小','RUAMW×格式化 block 大小可以小於 RUNS，例如有缺陷的可寫媒體減少；也可以大於 RUNS，例如有額外預留容量。因此即使看到未寫過的 RU，也不能直接用 RUNS 除 block size 取代裝置回覆。Reset 或 Flush 之後，RUAMW 也可能改變或不變。'),
  ('傳輸長度與快照限制','NUMD 採 Dword 數量減 1；短 buffer 只收到前段。此 Status 操作有特別規則：buffer 比完整結構長時，多出的部分填 0。不同描述器不是保證同一時刻的原子快照；若另外有 Write 或 Update 正在處理，不可把剛查到的容量當成已為下一筆 Write 保留。')],
 'Base 650～653 說明命令與清單外框，NVM 21 才定義每個 32-byte 描述器。兩份規格是外框加內容的關係。',source=NVM)

unit('update','主機要求換一個空 RU，舊資料仍有自己的生命週期','Request a fresh RU without erasing old data','7.4.1.1','596-597',
 'I/O Management Send MO=01h 接收 PID 清單，將已寫入的 RU 參照換到空 RU；若原本已空，可換也可不換。非法 PID 或超出限制會拒絕命令，但失敗前可能已有部分更新。與 Update 重疊處理的 Write 可能落在更新前或更新後的 RU。',
 'I/O Management Send MO=01h takes a PID list and moves a written RU reference to an empty RU; an already-empty RU may be retained or changed. Invalid PIDs or excess limits cause rejection, but partial updates may already have occurred. Writes processed concurrently may use the RU before or after the update.',
 '要更新 PID 8000h、8001h：NPID=1，CDW10=00010001h，資料 buffer 的 4 bytes 為 00 80 01 80。這是 2 個 little-endian PID；不需要另外用 NUMD 表示長度。',
 'To update PIDs 8000h and 8001h, NPID=1, CDW10=00010001h, and the four buffer bytes are 00 80 01 80. These are two little-endian PIDs; there is no separate NUMD for this command.',
 [('Update 改的是參照，不是 PHNDL 清單','同一 PID 經由同一 PHNDL→RUHID 映射，在指定 RG 換到新的空 RU。它不是重新建立 namespace 的 Placement Handle List，不會把 PHNDL 1 改成 PHNDL 2，也不會因為成功就把舊 RU 的有效 LBA 刪掉。'),
  ('已寫入與原本為空有不同要求','若目前 RU 已寫有 user data，控制器必須改到另一個空 RU；若目前 RU 完全沒寫過，可保留也可換另一個空 RU。主機提早切走尚未寫滿的 RU，可能犧牲可用寫入量，並在事件已啟用時留下 Not Fully Written To Capacity 紀錄。'),
  ('NPID 放在 MOS 裡，不是獨立 CDW','CDW10 的 MO 位於 bits 7:0，MOS 位於 bits 31:16；Update 把 MOS 的 16 bits 定義為 NPID。清單有 K 個 PID 時，NPID=K-1，每個 PID 2 bytes。NPID 不得超過配置 MAXPIDS；MAXPIDS 自身已是數量減 1 的上限，不能再把編碼值多減一次。'),
  ('Update 不採 Write 的非法 PID 容錯','RGID 超出 NRG 或 PHNDL 超出 namespace 的數量時，Update 回 Invalid Field in Command。命令被拒絕也不保證清單完全沒動過，因為規格允許部分 PID 已更新。完成後需要的狀態應重新查詢，不能假設整批更新具備全部成功或全部回復的語意。'),
  ('想形成清楚資料邊界，先處理重疊 I/O','如果某筆 Write 在 Update 處理期間使用同一 PID，資料可進入切換前或切換後的 RU。主機若需要讓「這一批」和「下一批」分開，應先完成並協調相關寫入，執行 Update，確認完成後才送下一批；還要依 cache 情況處理持久化。單靠先後送進不同 queue 不能證明控制器的處理順序。')],
 'Base 654／655 是 Send 入口；656 把 MOS 解讀為 NPID；657 看每個 2-byte PID。對比 Receive：Send 沒有 NUMD。')

unit('usage','Usage 查誰配置了 RUH，不查剩多少容量','Usage reports allocation, not remaining capacity','5.2.13.1.30','322-323',
 'LID 21h 按 RUHID 回報 RUHA：0 未被 namespace 使用，1 由主機明確指定，2 由控制器選用。這份清單以 Endurance Group 為範圍，最多一個 RUH 的屬性為 2；它不列每個 RG 的剩餘可寫量，後者需要 I/O Management Receive。',
 'LID 21h reports RUHA by RUHID: zero unused by namespaces, one explicitly host-selected, and two controller-selected. The Endurance Group list has at most one type-2 entry. It does not report available writes per RG; use I/O Management Receive for that.',
 '4 個 RUH 的 RUHA=[2,1,0,1]：RUH 0 供控制器自選的 namespace 使用，RUH 1／3 被明確指定，RUH 2 尚未使用。值 1 不表示只有一個 namespace 使用，也不表示已寫了 1 block。',
 'For RUHA=[2,1,0,1], RUH 0 serves controller-selected namespaces, RUHs 1/3 are explicitly selected, and RUH 2 is unused. A value of one neither counts namespaces nor means one block has been written.',
 [('先選正確群組','Get Log Page 的 LSI.ENDGID 選 Endurance Group；FDP 已啟用時，此查詢的 NSID 保留。不能把某個 NSID 放進去期待清單只剩這個 namespace 的 RUH。若該群組 FDP 未啟用，回 FDP Disabled。'),
  ('RUHID 由清單位置取得','8-byte header 的 NRUH 是直接計數，與目前配置的 NRUH 相同。第 i 個 8-byte 描述器從 8+8×i 開始，它描述 RUHID i；描述器本身 byte 0 是 RUHA，其餘保留。不要把它的 byte offset 當成 RUHID。'),
  ('三個值是分類，不是數量','RUHA=0 表示沒被 namespace 使用，1 表示主機在建立時明確指定，2 表示 namespace 請控制器選。控制器自選的 namespace 共用同一個此類 RUH，所以整份清單最多一筆為 2。RUHA=1 的 RUH 可以被符合條件的多個 namespace 共享。'),
  ('用兩種查詢回答不同問題','安排新 namespace 時，Usage 協助看 RUH 的分配來源；準備下一批 Write 時，Status 協助看某 namespace 可用的 PID 及剩餘量。Usage 不會直接告訴你哪個 RU 尚有 24 KiB，也不能由 RUHA=0 推斷某段舊媒體已被擦除。')],
 'Base 298 給清單位置；299 給分類值。與 Base 653／NVM 21 對照時，只比較各自回答的問題，不把欄位名稱相似當成相同資訊。')

unit('statistics','用相同量測期間判斷寫入放大','Measure writes over the same interval','5.2.13.1.31','323-324',
 'LID 22h 的 HBMW 計主機寫入，MBMW 同時包含主機與控制器內部寫入，MBE 計媒體擦除量，皆為含對應 metadata 的相關 byte 計數。比較相同配置期間的增量，才可用 ΔMBMW/ΔHBMW 觀察寫入放大；不能把擦除量加到分子，或跨清零直接相減。',
 'LID 22h records host writes in HBMW, host plus internal controller writes in MBMW, and erased bytes in MBE, with the relevant data/metadata accounting. Compare deltas within the same configuration interval to observe write amplification as ΔMBMW/ΔHBMW. Do not add erased bytes to the numerator or subtract across a reset of the counters.',
 '同一配置期間 HBMW 增加 100 GiB、MBMW 增加 150 GiB，觀察比值為 1.5；MBE 增加 200 GiB 另行記錄。若另一時段主機沒有新寫入但控制器仍搬資料，ΔHBMW=0，不能把除法結果說成 0。',
 'If HBMW increases by 100 GiB and MBMW by 150 GiB, the observed ratio is 1.5; an MBE increase of 200 GiB is separate. If host writes do not increase while internal relocation continues, ΔHBMW=0 and the ratio is undefined, not zero.',
 [('先知道這份累計涵蓋誰','Log 以 Endurance Group 為範圍，包含該 FDP 配置期間曾存在的全部 namespace。不能刪掉某 namespace 後，就以為它過去的寫入也會從累計移除。FDP 未啟用時，查詢回 FDP Disabled；啟用時 NSID 在這份查詢中保留。'),
  ('主機寫入與媒體寫入的差距','HBMW 不含控制器垃圾回收等內部寫入；MBMW 包含相關主機和內部寫入。NVM §4.1.4.6 指明計入 User Data Out Commands，以及 Write Zeroes、Write Uncorrectable。因此不能單純用 PCIe 傳輸的 payload bytes 替代 HBMW，尤其某些命令沒有等量主機 payload。'),
  ('用前後快照算增量','三個計數都是 128 bits，讀出後先記錄配置、群組、時間與起點，再計算同一時段差值。例如 host 從 500 增至 600 GiB，media 從 800 增至 950 GiB，差值的比是 150/100=1.5，不是只比結束時的 950/600。工作負載與背景處理也應一併考量。'),
  ('遇到清零、飽和與零分母','成功改變 FID 1Dh 值會把統計清 0，firmware update 不會清零；計數到 2^128-1 後飽和不回繞。跨清零不能直接相減，飽和後差值不再完整，host 增量為 0 時則不計這個比值。這些邊界會決定一個漂亮數字到底有沒有意義。')],
 'Base 300 的三列先分開看計數對象，再讀共同的清零與飽和條件。NVM §4.1.4.6 補足哪些命令列入，該節沒有另外一張 log 格式圖。')

unit('events','先替 RUH 選事件，再讀已發生的紀錄','Enable events on handles before reading records','5.2.30.1.22','507-509',
 'FID 1Eh 透過 NSID＋PHNDL 選 RUH，為列出的事件類型啟用或停用紀錄。Get 回支持的事件與目前啟用狀態，Set 送事件類型清單；共享 RUH 的 namespace 也共享該 RUH 的設定效果。LID 23h 才是已發生事件的紀錄。',
 'FID 1Eh selects an RUH through NSID plus PHNDL and enables or disables the listed event types. Get returns supported types and enablement; Set supplies a type list. Namespaces sharing the RUH share the effect of its settings. LID 23h contains events that actually occurred.',
 '對 PHNDL=1 啟用 00h、03h、80h：NOET=3，CDW11=00030001h、CDW12=1，Set buffer 為 00 03 80。NOET 直接計數，Get 的每個回覆項目卻是 2 bytes，不能沿用 Set 的 1-byte 項目長度。',
 'For PHNDL=1, enable types 00h, 03h and 80h using NOET=3, CDW11=00030001h, CDW12=1, and Set buffer 00 03 80. NOET is a direct count; each Get response entry is two bytes, unlike the one-byte Set entries.',
 [('先查支援，再選需要的類型','Get Features FID 1Eh 以指定 namespace 的 PHNDL 找到 RUH。一般的值查詢會在 buffer 回 supported event descriptors，CQE DW0.NOET 回項目數，按事件值遞增排列。SEL=3 則是通用能力查詢，不能用一般值回覆格式解讀。'),
  ('Set 一次控制所列的一組事件','CDW11 高位 NOET 表示 buffer 中有幾個 1-byte 事件類型，低位 PHNDL 選對象；CDW12.FDPEE 決定這些類型啟用或停用。Get 忽略輸入的 NOET 與 CDW12 開關，回覆每個類型目前狀態。若 PHNDL 無效，Get／Set 都會回 Invalid Field in Command。'),
  ('選 namespace 的路徑，改 RUH 的設定','A 的 PHNDL 1 與 B 的 PHNDL 0 若都映射到 RUH 3，透過 A 改事件設定會影響這個共享 RUH。不能以為 NSID 不同就各有一份獨立開關。FDP 停用時，此 Feature 的 Get／Set 都回 FDP Disabled；Feature 本身可保存，保存行為仍按通用 SV／SEL 規則使用。'),
  ('沒有紀錄，不一定沒有發生','事件必須在發生時已對相關 RUH 啟用才會被記錄。容量達上限後，新增紀錄會丟掉最舊的一筆；若設定值改變也可能清掉整份歷史。因此排程與效能分析應記錄設定及讀取時段，不能只憑空白的 log 宣告整段運作從未發生事件。')],
 'Base 501 是回覆數量，502／503 是請求選擇，504 是 Set 清單，505／506 是 Get 清單與每項開關。')

unit('event-record','把事件的原因、位置與資料量讀完整','Interpret event causes, locations and moved data','5.2.13.1.32','324-327',
 'LID 23h 一次選 host 或 controller events，依發生先後回傳 64-byte 紀錄。先看 ETYP，再用 PIV／NSIDV／LV 判斷哪些識別欄位有效。Media Reallocated 的 NVM 擴充還要讀 LBAV、NLBAM 和一個示例 LBA；事件時間戳不保證數值遞增。',
 'LID 23h selects either host or controller events and returns 64-byte records in occurrence order. Read ETYP, then PIV/NSIDV/LV to determine which identifiers are valid. The NVM Media Reallocated extension adds LBAV, NLBAM and one example LBA. Timestamp values are not guaranteed to increase.',
 'Invalid Placement Identifier 紀錄若 PIV=1、LV=1：PID 是主機原先送錯的值，RGID／RUHID 是控制器實際另選的目的。兩者不同是這個事件要揭露的差異，不是清單損壞。',
 'For Invalid Placement Identifier with PIV=1 and LV=1, PID is the invalid value submitted by the host, while RGID/RUHID identify the controller’s selected destination. Their difference is meaningful, not evidence of a corrupt record.',
 [('查哪一類事件先由命令決定','CDW10 bit 8 的 FDPET=1 選 host events，0 選 controller events；單次回覆不混兩類。整份 log 是 4096 bytes，64-byte header 後接 64-byte 記錄，最多容納 63 筆；實際支援上限仍依裝置。NUMFDPE 是實際筆數，最後一筆以外的 bytes 沒有可任意當作新紀錄的意義。'),
  ('Host events 說明哪些使用行為','00h 是主機 Update 時舊 RU 尚未寫滿；01h 是未在估計時間內寫滿而控制器改參照；02h 是 Controller Level Reset 改了一個或多個 RUH，此事件的 NSID 與 PID 保留；03h 是 Write 的 PHNDL 或 RGID 不合法。事件名稱描述原因，不能把全部都翻成「配置失敗」。'),
  ('Controller events 說明內部改變','80h Media Reallocated 描述 Initially Isolated 資料被搬到別的 RU；81h 描述控制器隱式改了 RUH 的參照。這和主機明確送 Update 不同。廠商事件範圍另有編碼，沒有廠商說明時只保存原值，不套用 80h 的欄位意義。'),
  ('先看有效位，再讀看似有值的欄位','PIV 決定 PID 可否使用，NSIDV 決定 NSID，LV 同時控制 RGID 與 RUHID。NSIDV=0 時 NSID 清 0 且忽略；LV=0 時兩個位置欄清 0 且忽略；PIV=0 時 PID 保留。若無法回報具體 RUH，PIV 與 LV 都清 0，不能把這些 0 解讀成真的在 RG0／RUH0。'),
  ('Media Reallocated 的 LBA 只是一個被搬移的例子','NVM 擴充中的 NLBAM=0 表示沒回報數量，FFFFh 表示至少 65535 個；LBA 在 LBAV=1 時有效，代表其中一個被搬移的 LBA，而不是連續範圍起點。因此 NLBAM=8、LBA=100 不能推論恰好搬了 100～107。PIV=1 才能把原始寫入的 handle 與此搬移關聯起來。'),
  ('順序以清單為準，時間需要讀來源與計時屬性','紀錄按發生先後排列，但 reset 或主機重新設 Timestamp 可讓後一筆時間數值較小。ETMSP 的格式含時間、初始化來源與是否可能暫停計時；分析跨 reset 的事件時保留清單順序，不能直接按 timestamp 數字重新排序。')],
 'Base 301 選事件類別，302 看清單，303 看共同事件欄位，480 看時間格式。NVM 116 只解釋 80h 的 ETSP 16 bytes，不是另一個 log。')

unit('lifetime','把資料失效、RU 切換與 reset 分開','Separate data invalidation, RU switching and reset','8.1.12','673-678',
 '降低回收成本，需要主機追蹤一整個 RU 內資料的使用週期；資料不再需要時，可用 Dataset Management AD=1 指出其 LBA 範圍。RUH Update 只改未來寫入的參照。Reset 後重新查配置、事件、namespace 的 PID 狀態與 cache，不要將保留啟用狀態誤認為所有 RU 狀態不變。',
 'Reducing reclamation cost requires tracking the useful lifetime of data written into an RU. When no longer needed, Dataset Management AD=1 can identify its LBA ranges. RUH Update changes the reference for future writes. After reset, refresh configuration, event settings, PID state and cache information; preserved enablement does not imply unchanged RU state.',
 '同一 RU 內曾寫 LBA 100 起 8 blocks、LBA 1000 起 4 blocks。兩段都失效後，DSM 可帶 2 個 ranges：NR=1，LLB 分別為 8、4；不是把兩個不連續範圍誤寫成從 100 起共 12 blocks。',
 'If an RU received eight blocks at LBA 100 and four at LBA 1000, once both expire DSM can describe two ranges: NR=1 and LLB values 8 and 4. Do not replace these disjoint ranges with twelve blocks starting at 100.',
 [('主機要追蹤實際資料，而不是只記一個 PID','同一 PID 在 RU 寫滿或 Update 後會指向新 RU。若要在舊 RU 資料一起失效時通知控制器，主機需知道那一批實際寫了哪些 LBA 範圍。單看目前 PID 並無法重新找回所有舊批次的 LBA；規格介面沒有把 PID 當成可直接刪整批資料的鍵。'),
  ('DSM 的範圍描述有自己的計數規則','AD=1 表示主機提供解除配置建議；每個 range 有 SLBA 與直接計數的 LLB，命令 NR 則是 range 數減 1。把兩個不連續範圍拆成兩列，才能正確表達哪些邏輯資料不再需要。此命令是 advisory，不能保證提交後立刻擦除媒體，也不能當成 Sanitize。'),
  ('大小限制會影響一次能處理多少範圍','先確認 NVMDSMSV 與 DSM 限制欄位所表示的命令支援，再以非零 DMRL、DMRSL、DMSL 分別判斷 range 數、單一 range blocks、整命令 blocks。NVMDSMSV=1 時限制欄位 0 表示未回報該限制；NVMDSMSV=0 時欄位 0 表示不支援命令。超出非零限制的部分可能不處理。主機需要分批並在既有資料已不再使用時發出；不能只因為清單完整，就推論一個超大命令必然處理全部內容。'),
  ('Reset 後沿資訊依存關係恢復','先 Get FID 1Dh 確認 ENDGID 的 FDPE／FDPCIDX，再查 LID 20h 取得該配置，接著查並設定所需 FDP events；對各 namespace 查 RUH Status 與 CNS08h cache 資訊。Data Placement 的 enable 狀態可保留，但 RUH 參照與 RUAMW 仍可能變動，舊快照不能直接接著使用。'),
  ('結束一批資料，與更換整份配置不同','Update 是單一或多個 PID 的參照更新；DSM 是指定不再需要的邏輯範圍；改 FID 1Dh 是 Endurance Group 配置更動，需先無 namespace，並清事件與統計。把這三種操作分開，才能說清楚誰改了什麼、哪些資料仍可讀，以及哪些累計值還能前後比較。')],
 'NVM 45～47 看 range 個數、AD 與長度；129 只取 DSM 三個處理限制。將它們接到主文資料生命週期，而不是再複製一套完整 DSM 教學。')
