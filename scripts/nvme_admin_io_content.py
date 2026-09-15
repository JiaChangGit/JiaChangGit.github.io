"""Authored course for the scoped Base Admin and NVM I/O report.

PDF page ranges below were checked against actual page destinations, not the
stale page numbers in the Base document's printed table of contents.
"""
from scripts.nvme_admin_io_scope import BASE, NVM


def bi(zh, en):
    return {'zh':zh, 'en':en}


UNITS=[]


def unit(key, source, sections, pages, title, summary, steps, example, reading):
    UNITS.append(dict(key=key, source=source, sections=sections, pages=pages,
                      title=bi(*title), summary=bi(*summary), steps=steps,
                      example=bi(*example), reading=bi(*reading)))


unit('command-map',BASE,'5, 5.1.1','202-204',
 ('先分清管理命令與資料命令','Separate management from data commands'),
 ('Admin 命令建立及調整控制器的工作環境；I/O 命令處理 namespace 的資料。Opcode 要連同命令集解讀，命令支援與目前是否允許執行也要分開確認。',
  'Admin commands establish and configure the operating environment; I/O commands act on namespace data. Interpret an opcode within its command set, and distinguish support from permission to execute in the current state.'),
 [('用一台剛開始工作的 SSD 想像全貌','作業系統需要知道 SSD 能做什麼、有哪些可存取的 namespace，以及如何建立資料傳輸的佇列。這些是管理面的問題。等環境準備好，讀取某一段 LBA、寫入資料或要求持久保存，才是資料面的工作。兩種命令最後都有完成回覆，但回覆能證明什麼，要看那一種命令的定義。'),
  ('讀 Opcode 表時，把三欄一起看','Figure 143 把功能、資料傳輸方向、NSID 使用方式放在同一列。傳輸方向是相對主機而言；它不是「這個命令有沒有改動 SSD」的判斷。例如 Firmware Image Download 把映像送入控制器；Firmware Commit 則用少數參數要求保存或啟用映像，兩者的資料傳輸型態不同。'),
  ('能力與當前狀態是兩次判斷','Identify 回報某命令受支援，仍不能保證每個時間點都能執行。§5.1.1 說明 Format 進行時的管理命令限制；讀 Figure 144 時先選 Format 欄，再看本篇保留的命令列和附帶條件。Sanitize 欄也須按當時作業狀態解讀。')],
 ('Admin Opcode 02h 是 Get Log Page；NVM I/O Opcode 02h 是 Read。只抄下 02h 而不記命令集，就無法知道這筆要求在做什麼。',
  'Admin opcode 02h means Get Log Page; NVM I/O opcode 02h means Read. The byte alone does not identify the operation.'),
 ('Figure 143 只讀本篇保留的命令列；Figure 144 讀 Format 與 Sanitize 狀態欄及本篇保留的列。先辨識命令集，再辨識狀態限制。',
  'Read only retained command rows in Figure 143 and the Format and Sanitize state columns for retained commands in Figure 144. Establish the command set before state-dependent restrictions.'))

unit('abort',BASE,'5.2.1','207-208',
 ('Abort：要求中止與確認中止是兩件事','Abort: requesting and confirming termination'),
 ('Abort 用 SQID 與 CID 指定原命令。Abort 的成功 CQE 不保證原命令已立即中止；IANP 和原命令的 CQE 必須分別判讀。',
  'Abort identifies the original command by SQID and CID. A successful Abort CQE does not guarantee immediate termination; interpret IANP and the original command’s CQE separately.'),
 [('先找對命令','CID 只在一條 Submission Queue 內辨識命令，所以 Abort 必須同時給出原命令的 SQID。若 SQ 3 和 SQ 8 都有 CID 7，兩者是不同要求。Abort 本身也是一筆新 Admin 命令，有自己的 CID，不能把它和要中止的 CID 混用。'),
  ('立即中止有明確的完成界線','控制器若執行 immediate abort，發出 Abort 的 CQE 之後，原命令除了發出自己的 CQE 外，不得再存取主機記憶體或造成規格列出的狀態與媒體變動。若無法保證這條界線，就不能回報已立即中止。這比「已收到停止要求」更強。'),
  ('IANP=1 之後要看什麼','IANP=1 表示沒有執行立即中止，可能是找不到命令、命令已完成，或尚無法停止；控制器仍可能稍後執行 deferred abort。最後要讀原命令 CQE 的 status，才能判斷它是否以 Command Abort Requested 結束。ACL 則限制同時尚未完成的 Abort 數量，與原命令所在 SQ 的深度不同。')],
 ('要中止 SQID=3、CID=7，可把 CDW10 編成 (7<<16)|3 = 00070003h。即使 Abort 的 status 成功，IANP=1 時仍須追蹤原命令的完成結果。',
  'For SQID=3 and CID=7, CDW10 is (7<<16)|3 = 00070003h. Even with successful Abort status, IANP=1 requires following the original command’s completion.'),
 ('依 Figure 147 的目標、Figure 148 的 IANP、Figure 149 的 Abort 並行數限制順序讀；不要把兩筆 CQE 合成一筆結果。',
  'Read the target in Figure 147, IANP in Figure 148, and the outstanding Abort limit in Figure 149. Keep the two CQEs separate.'))

unit('aer',BASE,'5.2.2','209-217',
 ('AER：讓事件找到接收它的主機','AER: delivering events to the host'),
 ('主機先提交 Asynchronous Event Request，控制器再以完成這筆命令的方式回報事件。事件類型、事件資訊、相關 LID 與 Event Specific Parameter 共同決定後續該讀什麼。',
  'The host first submits an Asynchronous Event Request; the controller later completes it to report an event. Event type, event information, associated LID, and Event Specific Parameter determine the next observation.'),
 [('這是一張先留下來的接收單','AER 不像 Read 那樣提交後立刻等資料。主機先提供尚未完成的 AER，事件發生時控制器才完成其中一筆。沒有事件時長時間不完成是正常行為，因此規格說主機不應替它設定一般命令逾時。AERL 是可同時保留的數量限制。'),
  ('先解事件類型，再解事件值','同一個 Event Information 數值，在不同 Asynchronous Event Type 下代表不同事情。Figure 151 的 DW0 決定事件類型、資訊與 Log Page Identifier；Figure 152 的 DW1 則是該事件定義的額外參數。後面的 Error、SMART、Notice、Immediate、One Shot 表都是沿這個分支讀，不能把所有 00h 當成同一事件。'),
  ('通知與取得完整紀錄分兩步','一般事件回報後，同類事件會被遮蔽，直到主機依規則讀取相應 Log Page 清除事件。Get Log Page 的 RAE=1 保留事件，RAE=0 在成功讀取時依規則清除；讀取失敗不清除。Immediate 與 One Shot 有不同處理規則，不能把一般事件的流程直接套上去。控制器重設還會終止未完成 AER，而不替那些要求回 CQE。'),
  ('把事件資料看成帶有型別的欄位','本章也列出電力、電壓及資料佇列的事件參數。這裡只教收到的參數如何表示感測器、方向或佇列位置，不加入已排除 Feature 的設定流程。遇到本篇未納入的 LID，只記下那是事件指出的另一份紀錄，不在本次報告打開它。')],
 ('Firmware Activation Starting 通知只表示即將啟用。主機應按事件規則確認通知，再用後續 Firmware Slot Information 核對版本；收到事件本身不是「新版本已在執行」的證據。',
  'A Firmware Activation Starting notice announces activation. Acknowledge it according to its rules, then use Firmware Slot Information to check the revision; the notice alone does not prove the new firmware is running.'),
 ('先讀 Figure 150–152 的完成格式，再按事件類型閱讀 Figure 153–161。共同格式只教一次，每張後續表指出其值所屬的事件類型。',
  'Start with Figures 150–152, then read Figures 153–161 by event type. Teach the common completion format once and keep each later value within its event type.'))

unit('firmware',BASE,'5.2.9, 5.2.10','228-232',
 ('Firmware：先看啟用選擇，再看映像怎麼送入','Firmware: activation choices and image transfer'),
 ('Firmware Image Download 傳送映像片段；Firmware Commit 依 CA 與 FS 決定保存及啟用。實際執行是先 Download 再 Commit，Spec 的編排則先介紹 Commit。',
  'Firmware Image Download transfers image pieces; Firmware Commit uses CA and FS to select storage and activation. Execution normally downloads before committing, while the specification presents Commit first.'),
 [('報告順序與執行順序可以分開','為了順著 PDF 翻頁，先在 §5.2.9 說明最終有哪些保存和啟用選擇，再往後讀 §5.2.10 的資料傳輸。口頭先交代「實際更新會先下載」，就不必為了展示流程來回翻兩節。CA=6／7 的 Boot Partition 動作由本篇 Boot 單元補足。'),
  ('把 slot、待啟用與正在執行分開','FS 選擇 slot，CA 決定這次是替換映像、安排啟用或要求可支援的立即啟用方式。命令可能回報需要哪一種 reset；不能看到映像已保存，就宣布控制器已換版本。支援的 slot 數、slot 1 是否唯讀及不經 reset 啟用能力，可在後面的 Identify Controller 頁一次對回。'),
  ('每一段下載都需要長度和位置','NUMD 是從 0 起算的 Dword 數量，OFST 是從整份映像開頭起算的 Dword 位移。長度加 1，位移不加 1。片段要符合 FWUG 的粒度與對齊要求；片段重疊可能回 Overlapping Range。MUD 另外描述多個更新序列重疊的偵測，與一筆命令的傳輸長度不同。')],
 ('傳送映像中的第 2 個 4096-byte 片段：NUMD=1023，OFST=1024。完成後仍須執行所需的 Commit／reset，最後以 LID 03h 的 CAFS、NAFS 與 slot revision 核對。',
  'For the second 4096-byte image piece, NUMD=1023 and OFST=1024. Follow with the required Commit/reset and verify CAFS, NAFS, and slot revisions in LID 03h.'),
 ('Figure 187–189 解釋 CA／FS、MUD 與啟用結果；Figure 190–193 解釋資料位址、數量、位移及重疊。CA=6／7 的 BPID 及保護條件接到本篇 Boot 單元。',
  'Figures 187–189 explain CA/FS, MUD, and activation results; Figures 190–193 explain the buffer, count, offset, and overlap. Connect CA=6/7, BPID, and protection conditions to the Boot unit.'))

unit('format',BASE,'5.2.11','232-235',
 ('Format：先決定影響誰，再決定新格式','Format: scope before format selection'),
 ('Format NVM 可變更媒體格式，也可依 SES 要求 secure erase。SES 決定要用 FNS 還是 SENS 判讀範圍；NSID 與 FNVMBS 再決定指定 namespace 或 broadcast 的行為。',
  'Format NVM changes the media format and can request secure erase through SES. SES selects FNS or SENS for scope interpretation; NSID and FNVMBS determine namespace and broadcast behavior.'),
 [('格式化不是建立 namespace','本篇假設 namespace 已存在。Format 改變的是該儲存空間使用的資料格式和相關設定，不重新教 Create／Attach。成功後，控制器不得再回傳受影響 namespace 原先的 user data；不能把格式化當成只更新一個不影響內容的標籤。'),
  ('先沿範圍表選一條路','SES=000b 表示沒有要求 secure erase，此時看 FNS；SES 為受支援的 secure erase 值時改看 SENS。所選的 scope bit=0 且 NSID 為指定值時，影響指定 namespace；scope bit=1 時則可能影響整個 subsystem 中的 namespaces。FFFFFFFFh 也要檢查 FNVMBS：其值為 1 表示不支援該 broadcast 用法，名稱不能取代位元定義。'),
  ('再讀格式索引與完成條件','LBAFU 和 LBAFL 組成 Format Index；PIL、PI、MSET 的 NVM 定義稍後在 NVM §4.1.2 補齊。需要特定主機格式宣告的選項，只在其前提成立時可用；這裡交代前提，不展開已排除的 Feature 設定。與進行中的 I/O、write protection 或不支援的格式衝突，可能導致命令失敗。Format 的完成 CQE 表示格式化已完成，與 AER 等待通知的完成含義不同。')],
 ('NSID=3 不一定只影響 namespace 3。若 SES=000b 且 FNS=1，必須按整體範圍判讀；若 FNS=0，才落在指定 namespace 的分支。',
  'NSID=3 does not necessarily restrict Format to namespace 3. With SES=000b and FNS=1, use the subsystem-wide branch; FNS=0 selects the specified-namespace branch.'),
 ('Figure 194 依 SES→scope bit→NSID 判讀；Figure 195 再解格式與 erase 選項，Figure 196 說明 Invalid Format。',
  'Read Figure 194 as SES → scope bit → NSID, then Figure 195 for format/erase choices and Figure 196 for Invalid Format.'))

unit('get-features',BASE,'5.2.12','235-238',
 ('Get Features：查目前值、預設值或支援能力','Get Features: values versus capabilities'),
 ('Get Features 的 SEL 選擇 current、default、saved 或 supported capabilities。SEL=011b 時，CQE DW0 的 CHANG、NSSPEC、SVBL 是能力回覆，不是該 Feature 的目前設定值。',
  'Get Features SEL selects current, default, saved, or supported capabilities. With SEL=011b, CHANG, NSSPEC, and SVBL in CQE DW0 describe capabilities, not the feature’s current value.'),
 [('同一個 FID 可以回答不同問題','想知道目前電源狀態設定，要查 current；想知道 reset 後的預設、先前保存的設定，或是否允許改變與保存，則是不同 SEL。先說明自己要問哪一個問題，再看回來的 DW0，才不會把能力旗標當成電源狀態編號。'),
  ('三個能力位元分別解釋','CHANG 表示該功能有可變更的值，不保證目前任何值都可改；SVBL 表示是否能保存。NSSPEC=1 表示 namespace scope；NSSPEC=0 不等於一律 controller scope，仍需看功能的作用範圍定義或 LID 12h。'),
  ('資料放在哪裡由功能決定','有些 Feature 只在 CQE 回傳少量資訊，有些還使用 DPTR 指向的資料結構；沒有資料結構時不能把 DPTR 當成必定有輸出的 buffer。CDW14 的 UUID Index 是選擇機制的一部分，本篇只交代共同欄位，不展開已排除的 UUID List CNS。')],
 ('SEL=3 的回覆若 CHANG=1、SVBL=0，意思是允許某些變更但不能保存；它不是「目前值是 3」，也不是保證每次 Set 都成功。',
  'A SEL=3 response with CHANG=1 and SVBL=0 permits some changes but not saving. It is neither a current value of 3 nor a guarantee that every Set succeeds.'),
 ('Figure 197–200 定位請求的資料指標與選擇值；Figure 201 專門解 SEL=011b，Figure 202 是命令錯誤。排除 FID 的表格列略過。',
  'Figures 197–200 locate request pointers and selectors; Figure 201 applies specifically to SEL=011b, and Figure 202 lists command errors. Skip excluded FID rows.'))

unit('logs',BASE,'5.2.13, 5.2.13.1.1–5.2.13.1.6, 5.2.13.1.18, 5.2.13.1.33, 5.2.13.2, 5.2.13.4','238-255,302-304,327-328,345,362',
 ('Log：先定位紀錄，再解讀紀錄裡的證據','Logs: select a record, then interpret its evidence'),
 ('本單元整理 LID 00h、01h、02h、03h、04h、05h、12h、24h；06h、07h、08h、15h、81h 配合相應作業另行教學。Get Log Page 的長度、位移與事件保留是共同機制；各 Log 的範圍、單位與有效條件由其資料結構決定。',
  'This unit groups LIDs 00h, 01h, 02h, 03h, 04h, 05h, 12h, and 24h; LIDs 06h, 07h, 08h, 15h, and 81h are explained with their corresponding operations. Transfer length, offset, and event retention are common mechanisms; each log defines its scope, units, and validity conditions.'),
 [('先分清四種紀錄用途','LID 00h 告訴主機有哪些 Log 可讀；01h 與 02h 分別提供個別錯誤紀錄與健康統計；03h、04h 用來更新 firmware 與 attached namespace 的認識；05h 和 12h 說明命令及 Feature 的支援與影響；24h 回報製造商預設配置狀態。不要把能力清單、歷史錯誤與目前設定混成同一份資料。'),
  ('長度、位移和表格索引不能互換','NUMDU:NUMDL 是從 0 起算的 Dword 數量，資料長度為 (NUMD+1)×4 bytes。OT=0 時 LPO 是 byte offset；OT=1 時是該 Log 定義的 index，必須先確認 IOS。譬如 entry 7 是第 8 個項目，位移 7 bytes 則是離開開頭 7 bytes，兩者毫無必然對應。'),
  ('健康統計必須帶單位與時間背景','SMART 的溫度以 Kelvin 編碼，Data Units Read／Written 是統計單位，不是當前 namespace 的 LBA 數。Error Information 要用 Error Count 辨識紀錄，搭配 SQID、CID、status 與欄位位置判讀；LBA 是否有意義還要看錯誤情境。NVM 對相關計數與 user-data 欄位的補充，留到最後一次切換文件後一起講。'),
  ('清單變動與命令影響要轉成後續動作','LID 04h 是自上次讀取後 changed attached namespace 的資訊，不是所有 active namespaces 的完整盤點。Commands Supported and Effects 的能力位元與內容變動、執行限制各回答不同問題；讀到可能改變 namespace 能力的命令，應安排後續重新 Identify。LID 24h 是狀態查詢，本篇不因此加入已排除的配置修改功能。')],
 ('讀取 512 bytes 的 Log：NUMD=127。若以 byte offset 從第二個 512-byte 區段開始，LPO=512，並不是 128；RAE 再獨立決定成功讀取是否保留對應事件。',
  'A 512-byte log read uses NUMD=127. With byte offsets, the second 512-byte segment uses LPO=512, not 128. RAE independently controls retention of an associated event on successful reading.'),
 ('先讀 Figure 203–211 的共同機制，再沿保留的 Log 順序讀 212–217、270–271、304。Figure 331 是共同完成狀態，不必為它重讀中間已排除的 Log。',
  'Read common mechanics in Figures 203–211, then retained logs in 212–217, 270–271, and 304. Figure 331 supplies completion status without reopening excluded intervening logs.'))

unit('identify',BASE,'5.2.14.1, 5.2.14.2, 5.2.14.5','362-431',
 ('Identify：建立控制器、namespace 與能力的地圖','Identify: map controllers, namespaces, and capabilities'),
 ('Identify 通常回傳 4096-byte 結構；CNS 選結構，CSI 選命令集，NSID、CNTID 或 CNS-specific identifier 決定查詢對象。這幾個選擇值不能互相代替。',
  'Identify returns a 4096-byte structure. CNS selects its kind, CSI the command set, and NSID, CNTID, or a CNS-specific identifier the target. These selectors are not interchangeable.'),
 [('先選「問誰、問哪一種資料」','CNS=01h 讀控制器共通資料；CNS=02h 讀 active namespace ID 清單；CNS=03h 讀 namespace 的識別描述子。CNS=05h／06h 還要由 CSI 決定命令集版本的 namespace／controller 結構。先把要求寫成一句完整的問題，會比背一長串 CNS 數值容易。'),
  ('控制器結構要分組看，不要逐 byte 唸完','Figure 338 很長，先看裝置識別與版本，再看可支援命令、最大傳輸與同時要求數，接著看功能能力與 Power State Descriptors。本篇在這一站一次對回 ACL、AERL、FRMW、FWUG、FNA、LPA、HMB 與電源相關欄位，避免每遇到一個命令都倒翻回來。表內只屬已排除專題或傳輸的欄位不展開。'),
  ('清單、描述子與能力結構有不同閱讀方式','清單通常以 count 或固定項目數界定有效內容，分段列舉還要看起始 identifier 的條件；描述子則由 type 和 length 決定下一筆從哪裡開始。NVM Set、Domain、Endurance Group 清單補足資源歸屬；I/O Command Set Vector 是命令集組合的位元圖，不是 namespace 清單。'),
  ('只讀資料結構，不把排除的管理流程帶回來','CNS=1Dh 的 Underlying Namespace List 描述背後的 namespace 對應，CNS=20h 回報支援的 controller state formats；清單計數、索引及版本欄位在獨立課程中配合實際布局解釋。UUID List、Primary／Secondary Controller 與使用者列出的其他 CNS 不讀。NVM 特定 LBA 大小和格式表會在 NVM §4.1.5 集中補上。')],
 ('CNS=01h 告訴你控制器支援什麼；CNS=02h 告訴你目前有哪些 active NSID。即使兩個回覆都是 4096 bytes，也不能用同一張欄位表解讀。',
  'CNS=01h describes controller capabilities; CNS=02h lists active NSIDs. Both responses are 4096 bytes, but they require different field layouts.'),
 ('Figure 332–337 先教查詢的選擇值；338–358 按保留的 CNS 讀其結構。長表分組講，清單先找 count／起始 ID，描述子先找 type／length。',
  'Figures 332–337 establish query selectors. Read 338–358 only for retained CNS values: group the long capability table, find counts/start IDs in lists, and type/length in descriptors.'))

unit('security',BASE,'5.2.28, 5.2.29','480-482',
 ('Security Send／Receive：協定資料的傳遞介面','Security Send/Receive: carrying protocol data'),
 ('Security Send 把安全協定資料送入控制器；Security Receive 取得相應結果。SECP 選協定，SPSP 與 NSSF 的意義由該協定決定，NVMe 命令成功不等於協定內每一步都已成功。',
  'Security Send supplies protocol data and Security Receive retrieves results. SECP selects the protocol; SPSP and NSSF are protocol-dependent. NVMe command success does not by itself prove success of every protocol operation.'),
 [('先理解外層與內層','NVMe 在這裡提供兩個資料傳輸命令。傳入的 buffer 裡還有安全協定自己的訊息與狀態，因此要先確認外層 NVMe 命令是否完成，再按內層協定解讀結果。這份報告不把外部安全規格的全部流程加入主範圍。'),
  ('傳出長度與可接收長度不同','Security Send 的 TL 描述傳出的資料長度；Security Receive 的 AL 描述接收配置長度，按 SPC-5 指定且 INC_512=0 的規則解讀，不套用 Get Log Page 的 (NUMD+1)×4。SECP、SPSP1／SPSP0 與 NSSF 合起來指定這一筆資料屬哪種交換。'),
  ('不是每一筆 Receive 前都有 Send','SECP=00h 的 Receive 用來查詢支援的安全協定，規格明確說它不對應先前的 Send。其他協定的請求與回覆如何配對、重設後資料是否仍在，要區分協定的交易識別與 NVMe 重設造成的回覆失效；不能只用「上一筆 Send」推論。')],
 ('想知道裝置支援哪些安全協定，可以先用 SECP=00h 的 Security Receive。這是在詢問能力，不是要求控制器執行某種資料清除。',
  'A Security Receive with SECP=00h queries supported security protocols. It asks about capabilities rather than requesting a data-erasure operation.'),
 ('Figure 456–462 分開讀資料指標、協定選擇與長度。Figure 459 只解 EAh 下的選擇值；不因此進入 Boot 或其他專題。',
  'Figures 456–462 separate pointers, protocol selection, and lengths. Figure 459 identifies EAh selections without expanding into Boot or other specialist workflows.'))

unit('features',BASE,'5.2.30.1, 5.2.30.4','482-540,545',
 ('Set Features：把設定連到佇列、事件與電源行為','Set Features: connect settings to operating behavior'),
 ('Set Features 的 FID 選功能，SV 要求保存，命令專屬欄位或 buffer 承載設定。每個功能有各自的作用範圍、可變更條件與重設行為，不能只照同一種設定值模型解讀。',
  'Set Features uses FID to select a feature, SV to request saving, and feature-specific fields or buffers for values. Scope, changeability, and reset behavior are defined separately for each feature.'),
 [('用三類問題整理 15 個 Base 功能','第一類是命令如何取得資源：Arbitration、Number of Queues 與後面的 PCIe 中斷設定。第二類是電源與溫度：Power Management、APST、Temperature Threshold、HCTM、Non-Operational Power State Config。第三類是系統狀態：Volatile Write Cache、Asynchronous Event Configuration、Timestamp、I/O Command Set Profile、Software Progress Marker，以及 PCIe 的 HMB。名稱相近的功能仍可能控制不同事情。'),
  ('先懂數量編碼，再看控制條件','Number of Queues 的請求與回覆都以從 0 起算的數量編碼，但「要求幾條」與「實際分配幾條」是不同值。Arbitration 的權重控制某仲裁模式下的服務分配，不是每一筆命令附帶的 priority。Volatile Write Cache 控制快取使用行為；要保證資料持久保存，仍須結合之後的 Flush 與 Write 語意。'),
  ('用狀態與時間分清電源功能','Power Management 選狀態；APST 依 idle 時間從目前狀態選一個非 operational 目標。低功耗狀態不代表可以不付延遲成本，退出與進入延遲要分開看。HCTM 的 TMT1／TMT2 是 host 給的熱管理界線；Temperature Threshold 是通知門檻；Non-Operational Power State Config 控制背景活動可否暫時超過低功耗限制，它不是另一個電源狀態編號。'),
  ('其餘功能也要說清楚各自的結果','Timestamp 使用毫秒時間值，Get 還回報其來源與是否可能停止計時；它不能無條件當成精準主機時鐘。I/O Command Set Profile 選擇支援的命令集向量組合，不直接格式化 namespace。Software Progress Marker 的 PBSLC 是主機提供的 pre-boot software load count，不是控制器自行計算的百分比。SV 也不代表所有功能都能保存，先查該功能能力。')],
 ('想取得 4 條 I/O SQ 與 4 條 I/O CQ，Number of Queues 請求欄位各填 3。若回覆 CQ 欄位是 1，表示分配 2 條，後續不能當成已取得原先要求的 4 條。',
  'To request four I/O SQs and four I/O CQs, encode 3 in each Number of Queues request field. A returned CQ value of 1 allocates two queues, not the four requested.'),
 ('先讀 Figure 463–466 的共同格式，再沿保留 FID 閱讀各表。請求與回覆分開，電源欄位對回狀態和延遲；跳過排除的 FID，不由表格連結擴張範圍。',
  'Start with the common format in Figures 463–466, then retained FIDs. Separate requests from responses and connect power fields to states and latency; skip excluded feature definitions.'))

unit('pcie-features',BASE,'5.2.30.2','540-545',
 ('PCIe 功能：中斷通知與借出的主機記憶體','PCIe features: interrupt delivery and borrowed memory'),
 ('Interrupt Coalescing 與 Interrupt Vector Configuration 調整完成通知；HMB 讓控制器使用主機提供的記憶體。中斷設定不改寫 CQE 的完成語意，HMB 也不等於主機把記憶體所有權永久交出去。',
  'Interrupt Coalescing and Interrupt Vector Configuration control completion notification; HMB lends host memory to the controller. Interrupt settings do not redefine CQE completion, and HMB does not permanently transfer memory ownership.'),
 [('完成寫入和主機收到中斷有時間差','控制器可以先把 CQE 寫入 Completion Queue，再依中斷聚合規則發通知。TIME 和 THR 一起控制聚合條件；某 vector 的 CD 可以關閉該 vector 的 aggregation。因此，看到較少中斷不能推論較少命令完成。'),
  ('HMB 要同時提供總量與配置清單','HMDL 指出每塊主機記憶體的位置和大小。HSIZE 使用 controller memory page 為單位，HMDLEC 是描述子數量；HMDL 位址和每個 BADD 都要符合對齊要求。總頁數、描述子數與 byte 位址是三種不同數量，不能混著填。'),
  ('把啟用、停用與重用分成生命週期','EHM 控制控制器能否使用這些區塊；MR 配合規格的 memory return 條件表達是否為先前提供的記憶體。只改一個主機端變數不會自動通知控制器停止存取。要收回記憶體，必須先完成本節規定的停用流程，再交給其他用途。')],
 ('每個 controller memory page 為 4096 bytes，HMDL 有兩筆各 256 pages 的描述子，合計 HSIZE=512 pages，也就是 2 MiB；HMDLEC 則是 2。',
  'With 4096-byte controller memory pages and two descriptors of 256 pages each, HSIZE=512 pages (2 MiB), while HMDLEC=2.'),
 ('Figure 543–544 先分清全域聚合設定與單一 vector 設定；545–553 再按 enable→總量→清單位址→每筆區塊→回覆讀 HMB。',
  'Figures 543–544 separate common coalescing settings from per-vector settings. Read HMB in 545–553 as enable, total size, list address, blocks, and returned attributes.'))

unit('queues',BASE,'5.3.1–5.3.4','553-558',
 ('I/O 佇列：先建立完成端，再接上提交端','I/O queues: create the completion side first'),
 ('Create I/O SQ 以 CQID 指向已存在的 I/O CQ，因此通常先建立 CQ 再建立 SQ。刪除時先移除引用該 CQ 的 SQ；數量配置、佇列建立與正常送命令是不同步驟。',
  'Create I/O SQ uses CQID to reference an existing I/O CQ, so create the CQ first. Delete referencing SQs before deleting their CQ. Queue allocation, creation, and command submission are distinct steps.'),
 [('先畫引用關係，就知道先後順序','一條 Completion Queue 可以服務多條 Submission Queues。建立 SQ 時要填入目標 CQID，所以不能先建立一條指向不存在 CQ 的 SQ。Number of Queues Feature 只完成可用數量的協商，不會替主機建立這些記憶體佇列。'),
  ('ID、深度、位址各自檢查','QID 選新佇列，QSIZE 是從 0 起算的深度，PRP1 指定佇列記憶體或清單；PC 表示實體連續的配置方式，還受 CAP.CQR 等條件約束。CQ 的 IEN／IV 處理中斷；SQ 的 QPRIO 連到仲裁模式，CQID 連到完成端；CDW12 的 NVMSETID 另外指定適用的資源歸屬。'),
  ('刪除時不要把記憶體太早拿走','先處理 SQ 的刪除與原先命令的結果，再刪除已沒有 SQ 引用的 CQ。Delete SQ 的完成結果與其中每一筆舊命令如何結束，由 Delete SQ 的成功完成界線判斷；未有自己 CQE 的舊命令隱含以 SQ Deletion 中止。Invalid Queue Identifier、Invalid Queue Size、Invalid Completion Queue 等錯誤各指出不同配置問題，不能都當成「資源不夠」。')],
 ('準備 SQ 3、SQ 4 共用 CQ 2：建立 CQ 2→建立 SQ 3 指向 CQ 2→建立 SQ 4 指向 CQ 2。移除時先刪 SQ 3 與 SQ 4，再刪 CQ 2。深度 64 的 QSIZE=63。',
  'For SQs 3 and 4 sharing CQ 2: create CQ 2, then each SQ referencing it. Remove both SQs before CQ 2. A depth of 64 encodes QSIZE=63.'),
 ('Figures 571–574 是 CQ，575–579 是 SQ，580–583 是刪除。比較相同位置的 QID／QSIZE，再辨認 CQ 的 IV 與 SQ 的 CQID。',
  'Figures 571–574 cover CQs, 575–579 SQs, and 580–583 deletion. Compare QID/QSIZE first, then distinguish a CQ’s IV from an SQ’s CQID.'))

unit('flush',BASE,'7, 7.2','590,593',
 ('Flush：用完成界線說明持久保存','Flush: a completion boundary for persistence'),
 ('Flush 要求指定 namespace 的資料及 metadata 提交至 non-volatile media。它至少涵蓋在 Flush 提交前已完成的命令；同時仍在執行的 Write 不可自動視為被納入。',
  'Flush commits data and metadata for the specified namespace to non-volatile media. It covers at least commands completed before Flush submission; concurrently outstanding Writes are not automatically covered.'),
 [('把一般完成與持久保存畫成兩條界線','若裝置使用 volatile write cache，Write 的正常完成不一定等於資料已進入非揮發性媒體。Flush 是主機要求建立持久保存界線的方法之一。它不把資料再從主機傳一次，而是要求控制器處理已持有的資料與 metadata。'),
  ('先確定 Write 已完成，再提交 Flush','假設 Write A 已完成，Write B 還在另一條 SQ 上執行，此時提交 Flush。規格保證至少包括 Flush 提交前已完成的命令；不能因此宣稱 B 也一定持久保存。若應用程式需要 A 與 B 都受這次 Flush 保護，主機先建立兩者都已完成的順序。'),
  ('NSID 決定作用範圍','指定 NSID 與 FFFFFFFFh 的範圍不同；後者需要檢查 VWC.FB：FB=11b 時對該控制器 attached 的所有 namespaces 生效；FB=10b 時回 Invalid Namespace or Format，舊版的 FB=00b 行為未定義。若 cache 不存在或未啟用，Flush 沒有資料提交作用，完成行為仍按本節的狀態條件判讀。讀 §7.2 時把範圍、已完成命令集合與 Flush 完成三件事連起來。第 7 章其他命令全部依本次清單略過，Figure 645 也只用來辨識 Flush 所屬的 I/O 命令集。')],
 ('Write A 完成→提交 Flush→Flush 成功，是 A 的持久保存證據；Write A 與 Flush 同時送出，再只等 Flush 完成，不能得到同樣保證。',
  'Write A completes → submit Flush → successful Flush establishes persistence for A. Submitting A and Flush concurrently and waiting only for Flush does not establish the same guarantee.'),
 ('Figure 645 只讀 Flush 列。§7.2 的重點在正文的時間先後與範圍，因此使用時間軸比另畫一張欄位表更有幫助。',
  'Read only the Flush row of Figure 645. Section 7.2 is chiefly about ordering and scope, so a timeline is more useful than another field table.'))

unit('compare',NVM,'3.3.1','27-29',
 ('Compare：把主機提供的內容拿來比對','Compare: check against host-provided content'),
 ('Compare 將指定 LBA 範圍的資料與主機提供的內容比對，並依設定處理 metadata／PI。成功表示符合比較條件；Compare Failure 是內容不相符，與無法讀取媒體不同。',
  'Compare checks a specified LBA range against host-provided content and handles metadata/PI according to its settings. Compare Failure denotes a mismatch, distinct from an unreadable medium.'),
 [('先問比較的兩邊是什麼','一邊是 namespace 裡選定 LBA 的資料，另一邊是主機 buffer 中的預期內容。因此 Compare 的主機資料傳輸方向與 Read 不同。若只有「想檢查媒體能不能讀」，沒有預期資料，後面 Verify 才是另一個要比較的命令。'),
  ('範圍、資料配置與檢查選項要一致','SLBA 指定起點，NLB 指定從 0 起算的區塊數量；DPTR／MPTR 的配置需配合目前格式及 metadata 是否分離。PRINFO 與 tag 欄位不是另一份待比較的 user data，而是保護資訊檢查的一部分。延伸欄位則先由命令格式選擇值判定是否適用。'),
  ('結果只對這次命令的範圍成立','比對成功能說明這次選定內容符合命令要求，不能推論其他 LBA 正確，也不會自動阻止其他命令稍後修改相同位置。需要更強的命令配對或原子操作保證，必須另外具備其定義的條件，不能只由 Compare 名稱推導。')],
 ('已知 LBA 100–107 應為某個 32 KiB buffer（每 LBA 4096 bytes），送 SLBA=100、NLB=7。若內容不同，Compare Failure 與媒體讀取錯誤是兩種不同結果。',
  'For LBAs 100–107 and a known 32 KiB buffer at 4096 bytes per LBA, use SLBA=100 and NLB=7. A mismatch and a media read error are different results.'),
 ('Figure 23–30 按 buffer→範圍→檢查選項讀，31 對回比較失敗與其他錯誤；比較資料與 PI tag 各有用途。',
  'Read Figures 23–30 as buffers, range, and checks; Figure 31 distinguishes mismatch and other failures. Comparison data and PI tags serve different purposes.'))

unit('copy',NVM,'3.3.2','30-43',
 ('Copy：主機傳描述子，控制器搬資料','Copy: descriptors cross the host interface'),
 ('Copy 的 DPTR 指向來源範圍描述子，目的位置由命令指定。描述子格式、來源與目的格式的對應、MSRC／MSSRL／MCL 及完成回覆共同限制一次操作。',
  'Copy DPTR points to source-range descriptors, while the command identifies the destination. Descriptor format, source/destination format compatibility, MSRC/MSSRL/MCL, and completion reporting constrain the operation.'),
 [('不要把 Copy 的 buffer 當成 user data','Read／Write 的 DPTR 通常搬 user data，Copy 的 DPTR 則傳一份來源範圍清單。控制器依清單在媒體上取得來源資料，再放到目的 LBA。主機省下搬移整批 user data 的工作，但仍需提供正確描述子。'),
  ('先固定描述子格式，再算每個來源範圍','DESFMT 決定每筆描述子的欄位與大小，NR 是從 0 起算的描述子數量。每個來源範圍有 SLBA 和 NLB，目的從 SDLBA 起連續放置。最大來源範圍數、單一來源長度與總長度分別受 MSRC、MSSRL、MCL 約束，不能只檢查一個上限。'),
  ('跨 namespace 時多了格式關係','格式必須依 matching／corresponding 規則相容；某些描述子也攜帶來源 NSID，不能把目的 NSID 當成所有來源的 NSID。PI 可能要依來源與目的地址調整，所需前提在命令條件中逐一確認；不在本篇重新加入 namespace 建立功能。'),
  ('別把成功範圍和原子保證混在一起','Fast copy 與一般 copy 有不同條件；是否原子、失敗時有多少來源範圍已處理，需讀本節專門規則與 CQE 回覆。不能因為只有一筆 Copy 命令，就假設所有來源與目的在任何失敗時都完全不變。')],
 ('兩個來源範圍分別有 4 與 6 blocks，NR=1，各 NLB=3、5。SDLBA=1000 時，目的依序使用 1000–1003 與 1004–1009；不是兩段都從 1000 開始。',
  'For source ranges of four and six blocks, NR=1 and their NLBs are 3 and 5. SDLBA=1000 maps them to 1000–1003 and 1004–1009, not two ranges both starting at 1000.'),
 ('Figure 32–38 是命令，39–41 是描述子，42 用來源與目的對照驗算，43 解釋失敗結果。每種格式先選定，再讀其欄位。',
  'Figures 32–38 define the command, 39–41 the descriptors, 42 maps source to destination, and 43 explains errors. Select the format before interpreting its fields.'))

unit('dataset',NVM,'3.3.3','44-48',
 ('Dataset Management：描述資料用途與解除配置','Dataset Management: usage hints and deallocation'),
 ('Dataset Management 以範圍清單提供存取屬性與 deallocate 要求。解除配置不保證媒體立即抹除，也不保證之後一定讀到零；範圍描述子的 LLB 是直接的 block count，不沿用 Read NLB 的加 1 編碼。',
  'Dataset Management supplies range attributes and deallocation requests. Deallocation guarantees neither immediate media erasure nor universally zero-filled reads, and its range-descriptor LLB is a direct block count, unlike Read’s NLB encoding.'),
 [('用「不再需要這段資料」來理解解除配置','檔案系統刪掉檔案後，可以告知控制器某些 LBA 的舊內容不再需要。這是空間使用資訊，不是這篇已排除的完整資料清除功能。後續讀回內容由 namespace 能力與 deallocated／unwritten 的規則決定。'),
  ('命令數量與每段長度要分別解碼','NR 是範圍描述子的個數，採從 0 起算；每筆描述子的 LLB 是直接的 block count。SLBA 是該範圍起點，Context Attributes 描述存取模式。AD、IDR、IDW 表達要提供哪一類要求或提示，這些是獨立旗標，不改變描述子的範圍長度。'),
  ('將處理上限與提示分開','控制器可回報每命令的範圍與總 block 處理限制，超過限制時要按規格的處理規則判讀。Context Attributes 是主機提供的使用資訊，不代表控制器必須以主機想像的實體位置安排資料。範圍相互重疊時也不能只把數字相加就當成不同容量。')],
 ('一筆描述子要表示從 LBA 200 開始共 8 blocks：SLBA=200、LLB=8；只有一筆描述子時，命令 NR=0。這和 Read 的 NLB=7 明確不同。',
  'One descriptor for eight blocks starting at LBA 200 uses SLBA=200 and LLB=8; the command uses NR=0 for one descriptor. Read would encode NLB=7 for eight blocks.'),
 ('Figure 44–47 先區分命令的 NR 與描述子的 LLB，48 解 Context Attributes，49 對回操作結果。',
  'Figures 44–47 distinguish command NR from descriptor LLB; Figure 48 defines Context Attributes and 49 reports errors.'))

unit('read',NVM,'3.3.4','48-51',
 ('Read：把範圍、格式與主機 buffer 接起來','Read: connect ranges, formats, and host buffers'),
 ('Read 用 SLBA 和 NLB 選 namespace 內的範圍，再依資料格式、metadata 配置及檢查設定把內容送入主機 buffer。命令欄位中的 block 數與 byte 數需要透過目前格式換算。',
  'Read selects a namespace range using SLBA and NLB, then transfers it to host buffers according to data format, metadata layout, and checking settings. Converting blocks to bytes requires the current format.'),
 [('先把 LBA 當成格子的編號','假設每個 LBA 有 4096 bytes 的資料，從 LBA 100 讀 8 blocks，範圍是 100–107，主機 data buffer 需要 32768 bytes。100 是位置，不是 byte offset；8 是實際 block 數，命令 NLB 則填 7。'),
  ('有 metadata 時不要只算 user data','若每個 block 另有 metadata，傳輸會依 namespace 格式採延伸 LBA 或分離的 metadata buffer。DPTR 與 MPTR 各自描述位置，PRINFO 再決定 PI 的轉移與檢查方式。不能因主機有足夠 data buffer，就省略 metadata 所需的空間及對應。'),
  ('共同位置不代表所有值都適用','CDW10–11 是 LBA 起點，CDW12 放數量與多個控制選項，CDW13 的意義還受 CETYPE 影響。每個欄位要先確認能力與啟用前提；不使用的可選機制依本節保留值規則處理，不展開本篇未納入的配置流程。')],
 ('4096-byte LBA、SLBA=100、NLB=7，data 長度是 (7+1)×4096=32768 bytes。若改用 512-byte LBA，同樣的命令範圍只對應 4096 bytes。',
  'With 4096-byte LBAs, SLBA=100 and NLB=7 transfer (7+1)×4096=32768 data bytes. With 512-byte LBAs, the same block range transfers 4096 bytes.'),
 ('Figure 50–58 按資料位置、LBA 範圍、控制與 PI 分組；Figure 59 是 Read 的完成錯誤，不與 Compare Failure 混用。',
  'Group Figures 50–58 by buffers, LBA range, control, and PI. Figure 59 contains Read completion errors, not Compare Failure.'))

unit('verify',NVM,'3.3.5','51-53',
 ('Verify：檢查可讀性，沒有主機比對資料','Verify: validate without a host comparison buffer'),
 ('Verify 對指定 LBA 範圍執行規格定義的驗證，不把正常 Read 的資料傳回主機，也不需要 Compare 的預期資料 buffer。它不能證明內容符合應用程式想要的值。',
  'Verify checks a specified LBA range without returning the normal Read payload or requiring Compare’s expected-data buffer. It does not prove that content matches an application’s intended value.'),
 [('拿三個問題對照三種命令','想把內容拿回來，用 Read；已經知道正確內容，想比對是否相同，用 Compare；想讓控制器檢查指定範圍的資料與適用保護條件，用 Verify。這三種要求可能都讀到媒體，但主機提供的資料與最後得到的證據不同。'),
  ('沒有 data buffer，仍有範圍與 tag','Verify 仍要指定 SLBA、NLB，並按支援能力與 PRINFO 解讀保護檢查、預期 tag 及命令延伸欄位。不能把 Read 的整個 SQE 複製過來，只把 opcode 換掉，就假設 DPTR／MPTR 仍有相同意義。'),
  ('成功的範圍不要擴張','Verify 成功只表示這次驗證的條件成立。資料若在應用程式寫入之前就算錯，媒體與 PI 仍可能自洽；Verify 無法知道業務邏輯所期待的值。需要與已知內容比較時，要回到 Compare 的問題。')],
 ('資料原本就被主機算成錯誤的帳款，但以完整有效格式寫入，Verify 仍可能成功。它檢查儲存層的條件，沒有另一份正確帳款可供比對。',
  'If the host originally computed an incorrect balance but stored it in a valid format, Verify may succeed. It has no separate correct balance against which to compare.'),
 ('Figure 60–65 只讀 Verify 實際使用的範圍、控制與 tag，66 解完成結果；以缺少主機資料傳輸對比 Read／Compare。',
  'Figures 60–65 define Verify’s range, controls, and tags; 66 gives results. Contrast its lack of host payload transfer with Read and Compare.'))

unit('write',NVM,'3.3.6','53-56',
 ('Write：寫入內容、持久性與原子性分開看','Write: content, persistence, and atomicity'),
 ('Write 把主機提供的資料寫入指定 LBA 範圍。FUA、volatile write cache、原子寫入限制及 PI 檢查回答不同問題；單筆命令成功不能自動推論所有可能的持久性與原子性保證。',
  'Write stores host-provided data in a specified LBA range. FUA, volatile write cache, atomic-write limits, and PI checks address distinct questions; successful completion does not imply every persistence or atomicity guarantee.'),
 [('先建立資料流','主機把資料放入 DPTR 所描述的 buffer，再用 SLBA／NLB 指定目的範圍。metadata 是否分離、需要傳多少 bytes，要與 Read 一樣依目前 namespace 格式計算。Write 不會因為命令名字相同，就接受任意大小的主機 buffer。'),
  ('FUA 與 Flush 的使用時機不同','FUA 把特定 Write 的完成連到該命令要求的非揮發性媒體提交條件；Flush 則對已完成的命令建立較後面的持久保存界線。兩者都不是「原子性開關」。是否有 volatile write cache、目前是否啟用以及指定控制選項，必須一起看。'),
  ('原子性還要檢查大小與邊界','Identify 的 atomic write 單位及 boundary 欄位限制哪些範圍有規格保證。後面的 Write Atomicity Normal Feature 也會影響正常操作下的要求；掉電條件與正常條件不能互換。先把一筆 Write 畫到 LBA 軸上，看是否超過單位或跨越相關邊界，再討論保證。')],
 ('一筆 Write 要求 FUA，可以要求該筆資料在完成時符合持久保存條件；若它跨越原子寫入邊界，FUA 並不因此讓整筆寫入具備更大的原子保證。',
  'FUA can require persistence for a particular Write at completion. If that Write crosses an atomic-write boundary, FUA does not enlarge the atomicity guarantee.'),
 ('Figure 67–75 按來源 buffer→目的 LBA→控制→PI 讀；76 的 status 再對回失敗原因。FUA 與 atomicity 不用同一個圖示代替。',
  'Read Figures 67–75 as source buffers, destination LBAs, controls, and PI; map status in 76 back to the failure. Keep persistence and atomicity distinct.'))

unit('zeroes',NVM,'3.3.7, 3.3.8','56-61',
 ('Write Uncorrectable 與 Write Zeroes：兩種不同結果','Write Uncorrectable and Write Zeroes: different outcomes'),
 ('Write Uncorrectable 使指定範圍之後的存取呈現不可更正錯誤條件；Write Zeroes 要求規格定義的零值寫入結果。兩者都不需要主機傳送整批一般 user data，但效果完全不同。',
  'Write Uncorrectable establishes an uncorrectable-error condition for the specified range; Write Zeroes requests the defined zeroing result. Neither requires a normal full host data payload, but their effects differ fundamentally.'),
 [('先看讀者最後會觀察到什麼','Write Uncorrectable 用來標記指定 logical blocks 的錯誤狀態，不是「寫入某個看起來錯誤的數值」。Write Zeroes 則讓讀取依命令及 namespace 規則得到零值相關結果，不能把它當成錯誤標記。'),
  ('零值操作仍有條件和可選行為','Write Zeroes 的 SLBA／NLB 決定範圍，DEAC、FUA、PI 及其他欄位要配合支援能力判讀。零值結果、解除配置與是否實際逐 block 寫入媒體是不同層次；控制器如何達到結果，不能只由命令名字推測。'),
  ('失敗時不能跳過完成欄位','Write Zeroes 有自己的 CQE DW0 與 status 定義。若完成回覆提供已處理範圍的資訊，要按該值的單位及適用條件使用，不能套用 Copy 的來源描述子數，或用一般 Read 的數量加 1 規則。')],
 ('想讓上層讀到零，與想讓上層收到不可更正錯誤是相反的要求。應先選需要的觀察結果，再選 Write Zeroes 或 Write Uncorrectable。',
  'Returning zeroes and returning an uncorrectable error are opposite goals. Choose the required observable result before selecting Write Zeroes or Write Uncorrectable.'),
 ('Figure 77–80 讀錯誤標記命令；81–89 讀零值命令、回覆與 status。對照相同 LBA 範圍在兩種命令後的可觀察結果。',
  'Figures 77–80 cover marking errors; 81–89 cover zeroing, completion data, and status. Compare the observable outcomes for the same LBA range.'))

unit('nvm-admin',NVM,'4.1.1, 4.1.2','62-63',
 ('NVM 補充：同一個 Admin 命令的資料語意','NVM additions to common Admin commands'),
 ('Base 定義 AER 與 Format 的共同介面；NVM §4.1.1 補充事件資訊，§4.1.2 定義 Format 的 PIL、PI 與 MSET。此處在同一份 NVM PDF 連續補完，無須再回 Base。',
  'Base defines common AER and Format interfaces. NVM §4.1.1 adds event information and §4.1.2 defines Format PIL, PI, and MSET. Complete these additions in the NVM PDF without returning to Base.'),
 [('用已看過的共同位置接上 NVM 定義','前面 Format CDW10 的一些欄位標為 I/O Command Set specific。現在這些空格才有 NVM 的具體含義：metadata 是否以延伸 LBA 或分離形式傳輸、PI 類型與其位置。這不是另一筆 Format 命令，而是同一筆命令需要兩份規格共同定義。'),
  ('先確認目前格式能容納設定','PIL 指定保護資訊的位置，PI 選擇保護類型或停用，MSET 選擇 metadata 傳輸方式。必須具備足夠 metadata 空間與對應能力；填入一組編碼不會自動創造原本不存在的 metadata。'),
  ('事件表也有命令集專屬分支','NVM 的 Notice 補充要在 Base 已解出的 Event Type 下使用。LBA 狀態等通知值若指向本次未納入的 Log 或 Feature，只辨識其事件意義，不打開另一段完整管理流程。')],
 ('如果目標 LBA 格式沒有足夠 metadata，不能只把 PI 欄位設成非零就啟用保護資訊；Format 的設定必須與 Identify 回報的格式相容。',
  'If the selected LBA format lacks sufficient metadata, setting PI nonzero does not create protection-information capacity. Format settings must match the advertised format.'),
 ('Figure 90 放回 AER 的 Notice 分支；91 放回 Format CDW10 的既有位置，不重講共同命令。',
  'Place Figure 90 in the AER Notice branch and Figure 91 in the existing Format CDW10 layout, without repeating the common command.'))

unit('nvm-features',NVM,'4.1.3.1, 4.1.3.2, 4.1.3.4','64-67',
 ('NVM 功能補充：閒置退出延遲、LBA 用途與原子性','NVM features: idle exit latency, LBA usage, and atomicity'),
 ('本篇只補充 FID 02h、03h、0Ah：Power Management 的 NVM 行為、LBA Range Type 及 Write Atomicity Normal。LBA 用途描述不會自行建立分割區，DN 不會放大掉電原子性保證。',
  'This report adds only FIDs 02h, 03h, and 0Ah: NVM Power Management behavior, LBA Range Type, and Write Atomicity Normal. LBA usage descriptions do not create partitions, and DN does not enlarge power-failure atomicity guarantees.'),
 [('Power Management 補的是工作負載語意','Base 已定義 PS 與 workload hint 的位置，NVM 在本節說明與其工作負載相關的行為。這個提示描述使用情境，不是主機可以用來要求任意效能的數字，也不改變 PS 的編號方式。'),
  ('LBA Range Type 是一份有長度的資料結構','Set 的 CDW11.NUM 是描述子數減 1；Get 忽略請求中的 NUM，改由 CQE.NUM 回報有效描述子數減 1。每筆 64-byte 描述子包含 Type、Attributes、SLBA、NLB 與 GUID；這裡 NLB 也是 block 數減 1，與 DSM 的直接計數 LLB 不同。Type 描述用途，Attributes 補充覆寫或可見性資訊，GUID 辨識用途實體。它不會替主機建立檔案系統。'),
  ('DN 要配合正常與掉電兩種保證讀','Write Atomicity Normal 的 DN 控制正常操作條件下的原子寫入要求；掉電原子性另由適用的能力與條件界定。後面 Identify 的 AWUN／AWUPF 及 namespace 對應值會讓主機知道單位。不要把 DN 設定與 FUA／Flush 的持久保存問題合成一個開關。')],
 ('把某段 LBA 的 Type 標示為特定用途，只是描述這段既有地址空間；不會因此多出另一個 NSID，也不會自動改變它的 LBA 大小。',
  'Assigning a Type to an LBA range describes existing address space. It neither creates another NSID nor changes the LBA data size.'),
 ('Figure 94–96 分開看請求數量、回覆數量與每筆描述子；98 讀 DN 的正常操作條件。未指定的 NVM Feature 小節直接略過。',
  'Figures 94–96 separate requested count, returned count, and descriptors; Figure 98 explains DN under normal-operation conditions. Skip unselected NVM feature sections.'))

unit('nvm-logs',NVM,'4.1.4.1, 4.1.4.2','76',
 ('NVM Log 補充：把數值換回資料範圍與計數','NVM log additions: interpret ranges and counters'),
 ('NVM §4.1.4.1 補充 Error Information 的 User Data，§4.1.4.2 補充 SMART／Health 的 NVM 計數語意。這些是既有 LID 01h、02h 的補充，不是兩個新的 Log。',
  'NVM §4.1.4.1 adds Error Information User Data and §4.1.4.2 adds NVM SMART/Health counter semantics. These extend LIDs 01h and 02h rather than defining new logs.'),
 [('回到同一份 Log 的專屬欄位','Base 決定 Error Entry 中 SQID、CID、status 等共同位置；NVM 的 User Data 補充讓部分錯誤能指向處理的 logical block 範圍。先確認該錯誤與欄位有效，再解讀內容；沒有有效資訊不能把零值強行當成 LBA 0 出錯。'),
  ('健康計數不是目前檔案大小','Data Units Read／Written 累計的是規格定義的傳輸量；Host Read／Write Commands 累計的是特定命令類別。兩種計數不同，不能把一次命令當成一個固定長度的 data unit，也不能用它直接推論實體 NAND 的寫入放大量。'),
  ('在這一頁停對位置','本篇只讀這兩個小節。下一個 Device Self-test 與後續 Log 都依本次範圍略過，不因為同在 PDF 第 76 頁就繼續講。這也是報告路徑同時列頁碼與停止標題的原因。')],
 ('同樣增加 1 筆 Host Write Commands，可能是 4 KiB，也可能是更大的 Write。要談流量，應讀相應的 Data Units 計數與單位，而不是只看命令筆數。',
  'One additional Host Write Command may transfer 4 KiB or much more. To discuss traffic volume, use the corresponding Data Units counter and its units, not command count alone.'),
 ('Figure 110 只補 Error Entry 的 User Data；SMART 的 NVM 計數定義在正文，直接對照前面已講過的 LID 02h 欄位。',
  'Figure 110 adds Error Entry User Data. Read the SMART counter additions in the text and connect them to the already explained LID 02h fields.'))

unit('nvm-identify',NVM,'4.1.5','83-110',
 ('NVM Identify：用格式與上限驗算一筆 I/O','NVM Identify: validate an I/O against formats and limits'),
 ('NVM Identify 補上 namespace 容量、LBA 格式、metadata／PI、原子性和命令限制。CNS、CSI、NSID 與 Format Index 的組合決定查目前 namespace，或查某個支援格式。',
  'NVM Identify adds capacity, LBA formats, metadata/PI, atomicity, and command limits. CNS, CSI, NSID, and Format Index determine whether a query describes a current namespace or a supported format.'),
 [('先用容量和格式算出可定址空間','NSZE、NCAP、NUSE 分別描述 namespace 大小、可配置容量與使用量，不能互當同義詞。FLBAS 指向目前格式，LBAF 的 LBADS 用 2 的次方表示每個 block 的資料大小，MS 則是 metadata bytes。對讀寫命令算 buffer 大小時，用目前格式，不是任選清單中的一個較熟悉格式。'),
  ('再把所有限制放到同一筆要求上','MDTS 限制資料傳輸量，Copy 的 MSRC／MSSRL／MCL 分別限制來源數、單段和總長度，DSM 還有自己的範圍處理限制。AWUN／AWUPF、namespace 的 NAWUN／NAWUPF 與 boundary 欄位回答原子性，DLFEAT 等欄位回答解除配置後的觀察結果。上限、對齊與提示要用正確單位後再比較。'),
  ('把格式能力與目前設定分開','MC、DPC、DPS、PIC 等欄位分別描述 metadata 方式、PI 能力與目前設定；Extended LBA Format 進一步指出 tag 及保護格式。支援某種 PI 不代表每個 namespace 已啟用它，也不表示所有命令的檢查選項都相同。'),
  ('已配置、格式查詢與清單是不同入口','CNS=09h／0Ah 的 Format Index 查詢不是查「編號 9 或 10 的 namespace」。CNS=11h／1Bh、16h 與其他指定入口各有已配置資料或粒度資訊的用途。這些 Identify 資料結構用來認識可查詢的對象與能力；建立及附加 namespace 的操作由另一篇專題說明。')],
 ('目前 FLBAS 選到 LBADS=0Ch、MS=8 的格式：每 block 有 4096 bytes data 與 8 bytes metadata。8 blocks 的 data 為 32768 bytes；metadata 是否另用 64-byte buffer，還要看傳輸配置。',
  'If current FLBAS selects LBADS=0Ch and MS=8, each block has 4096 data bytes and eight metadata bytes. Eight blocks carry 32768 data bytes; a separate 64-byte metadata buffer depends on the transfer layout.'),
 ('Figure 122 選入口；123–130 分容量、格式、保護與命令能力；131–133 再看格式查詢和粒度。查詢對象先確定，數值才有可比較的單位。',
  'Figure 122 selects the query; 123–130 cover capacity, format, protection, and command capabilities; 131–133 cover format selection and granularity. Establish the target and units before comparing values.'))

unit('format-list',NVM,'5.6','160-162',
 ('LBA Format List：選定同一筆格式才能配對能力','LBA Format List: match capabilities to one format'),
 ('LBA Format List 分成共用能力的格式與具有不同能力的格式。NLBAF、NULBAF 決定數量，CNS 決定能查到哪一群；Format Index 則選定這次要解讀的格式。',
  'The LBA Format List separates formats with common capabilities from formats with distinct capabilities. NLBAF and NULBAF determine counts, CNS determines which groups are accessible, and Format Index selects the format to interpret.'),
 [('把最後一頁當成前面 I/O 的檢查表','Read、Write、Compare、Verify 和 Copy 都需要知道資料格式。§5.6 集中解釋 Format Index 對應的格式清單，讓前面的 buffer、metadata 與 PI 討論落到同一份具體資料，而不是再引入一個新的資料操作。'),
  ('先把兩個計數換成實際格式數','NLBAF 採零起算，值 2 代表 3 個共用能力的格式；NULBAF 直接表示非共用格式數，值 2 代表另外 2 個。兩者合計 5 個，有效索引為 0–4。圖中的分組要以換算後的個數理解，不可直接把兩個原始欄位相加，少算一個格式。'),
  ('用 CNS 選對查詢入口','Figure 193 的 CNS 00h、05h、08h 只涵蓋 NLBAF 所描述的群組；09h、0Ah 能查兩群。對某個非共用格式，要以 Format Index 取得它自己的能力，不能沿用 NSID=FFFFFFFFh 的共用能力結果。CNS 09h 查 NVM Identify Namespace 的格式資料，0Ah 查 NVM 命令集專屬結構的格式資料。'),
  ('最後確認格式目前可用','支援的格式若目前不可用，其 LBADS 回報 0h，不能照一般指數公式把它解成可用的 1-byte LBA。可支援的最大格式數還受 LBAFEE 前提限制：0 時至多 16 個，1 時至多 64 個；本篇只說明這個引用條件，不展開其 Feature 設定。')],
 ('NLBAF=2、NULBAF=2 時，index 3 屬非共用能力的格式。用 CNS 09h／0Ah 查 index 3 的資料，再一起確認 data 大小、metadata 與 PI；不可拿 index 2 的能力代替。',
  'With NLBAF=2 and NULBAF=2, index 3 belongs to the non-common group. Query index 3 using CNS 09h/0Ah and check its data size, metadata, and PI together; capabilities from index 2 are not a substitute.'),
 ('Figure 192 先分群並換算個數；Figure 193 再決定哪些 CNS 能讀到該群。以 NLBAF=2、NULBAF=2 的 5 個格式驗算兩張圖。',
  'Use Figure 192 to separate groups and decode counts, then Figure 193 to select a CNS that reaches the required group. Check both with the five-format example NLBAF=2, NULBAF=2.'))

from scripts.nvme_admin_io_added_topics import add
add(unit, BASE)
