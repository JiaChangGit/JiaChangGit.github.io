"""Independent Read Recovery Level course and bilingual overview material."""
BASE = 'NVME-BASE-2.4'
REPORT_ID = 'base-read-recovery-level'


def bi(zh, en):
    return dict(zh=zh, en=en)


UNITS = []


def unit(key, section, pages, title, summary, example, steps, reading, prerequisite=False):
    UNITS.append(dict(key=key, section=section, pages=pages, title=bi(*title),
        summary=bi(*summary), example=bi(*example), steps=steps, reading=reading,
        prerequisite=prerequisite))


unit('levels', '8.1.23', '715-716',
 ('讀取遇到困難時，要花多少力氣復原？', 'How much recovery should a difficult read receive?'),
 ('Read Recovery Level（RRL）在讀取完成時間與錯誤復原投入之間提供取捨。支援此功能時，Level 4 是必備的預設等級，Level 15 是必備的 Fast Fail；Level 0 若有支援，提供最多復原。等級越高，復原量越少；與 I/O 命令 LR 的互動由實作決定。',
  'Read Recovery Level (RRL) balances read completion time against recovery effort. When the feature is supported, level 4 is the mandatory default and level 15 is mandatory Fast Fail. Optional level 0 provides maximum recovery. Higher levels provide less recovery; interaction with an I/O command’s LR field is implementation-specific.'),
 ('說明性情境：資料有另一份可用副本的服務，可能希望裝置少做復原，早些交由上層決定下一步；願意等待這份媒體資料的工作，可能選較多復原的受支援等級。這是選擇策略的理由，不是特定等級的延遲或成功率保證。',
  'Illustrative scenario: a service with another usable copy may prefer less device recovery before deciding its next action. A workload willing to wait for this copy may prefer a supported level with more recovery. These are policy choices, not latency or success-rate guarantees.'),
 [
  ('先把「復原」放回讀取流程', '主機送出讀取後，控制器需要從媒體取得正確資料。當資料不容易讀出時，額外的復原工作會占用時間。RRL 讓主機選擇控制器要投入多少復原，而不是直接指定要讀哪個位置、回傳多少 bytes，或把媒體內容改成另一份資料。'),
  ('數字描述的是復原量的順序', '規格定義 0～15 共 16 個可能的等級，數字往上走，復原量往下走。0 是最多復原，4 是一般程度且為預設，15 是最少復原。中間等級的差距不是固定比例：不能把 8 解讀成 4 的兩倍速度，也不能把等級當作重試次數。'),
  ('先確認有功能，再談必備等級', 'RRL 本身不是每個控制器都必須具備的功能。一旦支援，subsystem 與所有控制器就必須支援 4、15，宣告能力與等級清單，並支援 FID 12h。0、1～3、5～14 是選用等級；表上列有這些數字，不代表手上的裝置全部能選。'),
  ('Fast Fail 沒有定義一個毫秒數', 'Fast Fail 指最少的復原量。這兩節沒有替它指定 1 ms、10 ms 等上限，也沒有規定完全不做復原。它調整的是讀取困難時的處理策略；正常讀取可能根本用不到較深入的復原，因此不能承諾每筆 Read 都會變快。'),
  ('不要替 LR 發明優先順序', 'I/O 命令中的 Limited Retry（LR）也是與復原有關的控制資訊，但 §8.1.23 明確把 LR 與 RRL 的互動留給實作。即使已選 Level 15，又送出帶 LR 的命令，仍不能由本規格推導成「一定零次重試」或「LR 一定蓋過 RRL」。兩者的共同效果需要對應實作資訊。')
 ], 'Figure 755 先看 4 與 15 的 M，再看 0 的 O，最後沿箭頭確認數字增加時復原量減少。')

unit('scope', '5.2.30.1.12', '499',
 ('一個設定，會影響哪些儲存空間？', 'Which storage spaces share one setting?'),
 ('有 NVM Sets 時，FID 12h 以 NVM Set 為範圍，選中的集合共用一份 RRL。沒有 NVM Sets 時，範圍改為整個 NVM subsystem，所有 namespace 使用同一等級。改變 RRL 不會改變 namespace 中已有的資料。',
  'With NVM Sets, FID 12h has NVM Set scope with one RRL for the selected set. Without NVM Sets, the feature has NVM subsystem scope and all namespaces use one level. Changing RRL does not change their stored data.'),
 ('說明性範例：Set 7 內有 namespace A、B，Set 9 內有 C。把 Set 7 改成 15，A、B 共用這個新等級，C 仍使用 Set 9 的設定。不能把 A 改成 15、同時要求同一 Set 內的 B 保持 4。',
  'Illustrative example: set 7 contains namespaces A/B and set 9 contains C. Setting set 7 to 15 changes the shared level for A/B; C retains set 9’s setting. A cannot use 15 while B in the same set retains 4.'),
 [
  ('先分清 namespace 與 NVM Set', 'namespace 是主機存取的邏輯儲存空間；NVM Set 則是可包含一個或多個 namespace 的儲存集合。具有已格式化儲存空間的 namespace 完整位於一個 NVM Set 內，不橫跨多個 Set。RRL 是集合的屬性，所以要沿 namespace 的歸屬往上找，才知道它共用誰的設定。'),
  ('共享設定不代表共享每一個欄位', '例子裡 A、B 可以是不同大小、不同用途的 namespace，但兩者在同一個 Set，因此共用 RRL。這個關係只說明讀取復原策略的範圍，不表示 A 的資料會被複製到 B，或兩者的每一項設定都完全相同。'),
  ('新增 namespace 也沿用 Set 的等級', '假設 Set 7 已經設為 15，之後又在其中建立 namespace D，D 繼承的是 Set 7 的 RRL。不能因為 D 是新建的，就推論它一定單獨回到預設 4；預設等級與目前 Set 正在使用的等級是不同概念。'),
  ('沒有 NVM Sets 時，不能靠編號隔離影響', '若裝置不支援 NVM Sets，所有 namespace 使用 subsystem 的同一個 RRL。此時 FID 12h 不用 NVMSETID 選範圍；送入 7 並不會創造 Set 7。主機依 NVM Set 共通規則把 NVMSETID 填 0，控制器在本 Feature 忽略該欄。'),
  ('變更策略與變更資料分開理解', '從 4 改到 15 不會清除、格式化或重寫 namespace 中的資料。它可能改變後續遇到困難的讀取如何處理，不能當作修復既有資料的命令。主機也不能透過本 Feature 指定只改某一個 LBA 的策略。')
 ], 'Figure 67 說明集合與 namespace 的包含關係；Figure 484 把這個關係接到命令的 NVMSETID。')

unit('discover', '5.2.14.2.1', '370-373,397-398',
 ('讀懂支援位元，才知道哪些值能選', 'Read capability bits before choosing a level'),
 ('Identify Controller 的 CTRATT.RRLVLS 表示是否支援功能，RRLS 的 16 個 bits 分別表示各等級是否支援。CTRATT.NSETS 決定使用 Set 或 subsystem 範圍；ONCS.SSFS 則決定能否使用非零 SEL 與 SV。這些能力不能互相替代。',
  'Identify Controller reports feature support in CTRATT.RRLVLS and individual levels in the 16-bit RRLS bitmap. CTRATT.NSETS selects set versus subsystem scope. ONCS.SSFS controls support for nonzero SEL and SV. These capabilities answer different questions.'),
 ('說明性範例：RRLS=8011h，拆成 (1<<15) | (1<<4) | (1<<0)，表示只支援 0、4、15。byte 100、101 若是 11 80，依 little-endian 組合後才是 8011h；它不是目前等級，也不是「共有 8011h 個等級」。',
  'Illustrative example: RRLS=8011h equals (1<<15) | (1<<4) | (1<<0), advertising levels 0, 4 and 15. Bytes 100/101 containing 11 80 form 8011h in little-endian order. This is neither the current level nor a level count.'),
 [
  ('先確認整體支援', '在 Identify Controller 資料結構 bytes 99:96 的 CTRATT 內，bit 3 是 RRLVLS。它為 1 才表示控制器支援 RRL；bit 2 的 NSETS 則是另一件事，說明有沒有 NVM Sets。RRLVLS=1、NSETS=0 是可以理解的組合：功能存在，但設定由整個 subsystem 共用。'),
  ('bitmap 中，每一個 bit 都是一個答案', 'RRLS 位於 bytes 101:100。要判斷等級 n 是否支援，計算 (RRLS >> n) & 1；結果 1 表示支援，0 表示不支援。範例 8011h 的 bit 8 是 0，因此即使 8 在 0～15 範圍內，也不能當成可選值。這個檢查與欄位放不放得下 8 是兩回事。'),
  ('不要把 bitmap 與 RRL 欄位互換', 'RRLS 用 16 個 bits 同時列出可用集合；設定命令的 RRL 只用 4 個 bits 放一個等級。選 15 時，RRLS 中應檢查的是 bit 15，也就是遮罩 8000h；實際送進 RRL 的卻是 Fh，不能把 8000h 塞進該欄。'),
  ('再確認查詢與保存的擴充能力', 'ONCS 位於 bytes 521:520，其中 bit 4 是 SSFS。若為 0，不使用非零 SEL 或 SV，仍可以用 SEL=0 讀目前值。若為 1，可用 SEL=3 查本 Feature 是否可變更、是否可保存；這裡回的是另一組能力 bits，並不是 RRLS 支援等級清單。')
 ], 'Figure 338 很長，本篇只讀 CTRATT 的 RRLVLS／NSETS、RRLS，以及 ONCS.SSFS；逐圖區集中列出 byte 位置與算例。', True)

unit('set', '5.2.30.1.12', '499',
 ('把「哪個集合、哪個等級」組成設定命令', 'Encode the target set and requested level'),
 ('Set Features 用 FID 12h 選 Read Recovery Level Config，CDW11 的低 16 bits 放 NVMSETID，CDW12 的低 4 bits 放 RRL。這個 Feature 不使用資料 buffer；NVM Set 或 subsystem 範圍的 NSID 應為 0。',
  'Set Features selects Read Recovery Level Config with FID 12h. CDW11 bits 15:0 carry NVMSETID; CDW12 bits 3:0 carry RRL. No data buffer is used, and NSID should be zero for the NVM Set or subsystem scope.'),
 ('說明性範例：已確認 Set 7 存在且支援 Level 15，以 SV=0 設定：NSID=0、CDW10=00000012h、CDW11=00000007h、CDW12=0000000Fh。三個數值依序回答「改哪項功能、改哪個 Set、改成哪個等級」。',
  'Illustrative example: after confirming that set 7 exists and level 15 is supported, use SV=0 with NSID=0, CDW10=00000012h, CDW11=00000007h and CDW12=0000000Fh. These select the feature, set and level respectively.'),
 [
  ('先選 Feature，再解讀後面的參數', 'CDW10 bits 7:0 的 FID=12h 選本篇功能；bit 31 的 SV 控制是否提出保存要求。先用 SV=0 理解目前值的修改，得到 CDW10=00000012h。是否需要保存、是否支援保存，以及重設後如何處理，會在後面的生命週期單元分開說明。'),
  ('NVMSETID 不是 namespace 編號', 'CDW11 bits 15:0 是 16-bit NVM Set Identifier，高 16 bits 保留。已支援 NVM Sets 時要填既有 Set 的識別碼，0 是保留值，不是「全部 Set」。本篇例子用已知有效的 7；不把 namespace A 的 NSID 放到此欄。命令本身的 NSID 則依共通規則填 0，非零會被中止。'),
  ('RRL 是一個 4-bit 代碼', 'CDW12 bits 3:0 直接保存等級，bits 31:4 保留。15 的十六進位是 Fh，所以整個 CDW12 是 0000000Fh。這不是數量減 1 的欄位，選 Level 15 就填 15；填 14 會選到另一個等級。送出前先確認 RRLS 的對應 bit 為 1。'),
  ('只有參數，沒有另外一包設定資料', '本 Feature 的屬性就在 CDW11、CDW12，不需要另外準備一份 data buffer。Set 的 DPTR 在此沒有用途，Get 的 DPTR 也會被忽略。其餘沒有供本 Feature 使用的命令專用欄位屬保留區；示例將保留位清 0，不自行塞入額外控制資訊。'),
  ('看懂索引與位移，才能讀欄位圖', 'Dword 是 4 bytes；命令的 CDW11 表示從 0 起算的第 11 個 Dword，起點是 byte offset 44，CDW12 起點則是 48。NVMSETID=7 是識別值，並不是 byte offset 7。命令欄位位置、欄位中的 Set 編號、欄位中的等級，各有不同用途。')
 ], 'Figures 484／485 對照看：前者回答對象，後者回答新值。共同命令外框與 SV 放在相應引用圖表中。')

unit('get', '5.2.30.1.12', '499',
 ('讀回時先看 SEL，才知道 DW0 在回答什麼', 'Interpret returned DW0 according to SEL'),
 ('成功的 Get Features 在 SEL≠3 時，以 CQE DW0 回傳 Figure 485 格式的 RRL。SEL=3 則改回 Supported Capabilities：CHANG、NSSPEC、SVBL。相同 DW0 數值可能有完全不同的意思；RRLS 等級清單仍應從 Identify Controller 取得。',
  'Successful Get Features with SEL other than 3 returns RRL in CQE DW0 using Figure 485. SEL=3 instead returns Supported Capabilities: CHANG, NSSPEC and SVBL. The same DW0 value can have entirely different meanings; the level bitmap remains in Identify Controller.'),
 ('同樣收到 DW0=00000004h：SEL=0 時表示目前 Level 4；SEL=3 時表示 CHANG=1、NSSPEC=0、SVBL=0，也就是可變更、非 namespace scope、不可保存。後者不能讀成「目前 Level 4」。',
  'The same DW0=00000004h means current level 4 with SEL=0, but CHANG=1, NSSPEC=0 and SVBL=0 with SEL=3: changeable, not namespace-scoped and not saveable. The latter is not a current-level result.'),
 [
  ('讀目前值，沿用相同的目標 Set', 'Get Features 的 CDW10 bits 10:8 是 SEL，bits 7:0 是 FID。查目前值用 SEL=0，因此 CDW10=00000012h；查 Set 7 仍用 CDW11=00000007h、NSID=0。Set 命令放新等級的 CDW12，不是 Get 命令拿來要求回傳等級的位置；Get 的未使用命令專用欄位保留。'),
  ('成功完成之後，從回覆而非命令抽出等級', '確認 Get 命令成功，再讀完成項目的 DW0，取 bits 3:0 就得到 RRL。若 DW0=0000000Fh，讀回的是 Level 15。Figure 485 雖然以 Command Dword 12 為標題，§5.2.30.1.12 另明確指定：Get 成功且 SEL≠3 時，同一個格式放到 CQE DW0。'),
  ('有支援時，再比較目前、預設與已保存', 'SSFS=1 時，SEL=1 查 default，SEL=2 查 saved，SEL=3 查 supported capabilities；4～7 保留。預設 RRL 為 4，但目前值可以是 15。若功能不可保存，或還沒有已保存值，SEL=2 依 Get 共通規則回預設；不能只因查到 4，就說主機曾把 4 保存過。'),
  ('能力回覆要換一種欄位解讀', 'SEL=3 的 DW0 bit 2 是 CHANG，bit 1 是 NSSPEC，bit 0 是 SVBL，bits 31:3 保留。NSSPEC=1 才表示 namespace 範圍；為 0 時，這個 bit 不會告訴你其他範圍是哪一種。本篇應再看 NSETS 與 FID 12h 的定義，判定為 NVM Set 或 NVM subsystem，不能自行推成只影響一個控制器。'),
  ('用同一個例子串起三種查詢', '假設 SSFS=1，先用 CDW10=00000312h 查能力；能力允許後設定 Set 7。接著用 00000012h 查 current，預期讀回要求的 15；若改用 00000112h 查 default，回答的仍是 4。這三次是在問能力、目前值與預設值，不是控制器自相矛盾。')
 ], 'Figure 198 決定問題；Figure 201 與 Figure 485 是兩種互斥的 DW0 解讀方式，先確認 SEL 再挑格式。')

unit('activation', '5.2.30.1', '485',
 ('以成功完成為界，區分舊命令與新命令', 'Use successful completion as the settings boundary'),
 ('已提交而尚在執行的命令，可能套用或不套用剛改好的 Feature。Set Features 成功完成後才提交的命令，必須使用新設定。若希望明確區隔兩批讀取，主機宜先讓原有命令完成，再改設定。',
  'Commands already submitted may or may not use a newly changed feature value. Commands submitted after successful Set Features completion must use the new settings. To separate two read batches clearly, the host should let outstanding commands complete before changing the feature.'),
 ('說明性時間順序：Read A 先提交，接著 Set RRL=15；Set 成功後才提交 Read B。B 必須使用新設定，但不能對仍未完成的 A 作相同保證。若先等 A 完成再送 Set，就能明確分成兩批。',
  'Illustrative sequence: submit read A, then set RRL=15, then submit read B after Set completes successfully. B must use the new setting; the same guarantee does not apply to an outstanding A. Waiting for A before Set makes the batches distinct.'),
 [
  ('「送出設定」與「設定成功」中間還有處理時間', '主機把 Set Features 提交到佇列，只代表控制器可以開始處理它。不能在此刻就宣稱新的 RRL 已適用於之後所有命令；規格用成功完成作為後續提交命令的保證界線。設定失敗時，也不能把要求值當作有效的 current。'),
  ('已在途的讀取沒有統一的新舊保證', 'Read A 若在 Set 成功前就已提交，設定變更時它可能仍在執行。共通規則允許它套用或不套用新設定。教材中的時間圖因此把 A 標為不保證採新值，而不是擅自指定它一定用舊值。'),
  ('需要清楚分界時，主機可先整理提交順序', '先暫緩新的讀取，等已提交命令完成，再送 Set，等成功後才提交下一批。這樣做的目的，是讓每一批使用哪個 RRL 可被明確說明；不是說 RRL 會改寫舊資料。完成設定後，也宜重新確認與該 Feature 有關的能力及狀態。'),
  ('共用 Set 時，還要協調其他主機', 'RRL 不屬於單一控制器私有的設定。多個主機若同時管理同一 Set 或 subsystem，一個主機剛讀回 15，另一個主機仍可能隨後改成 4。Base 要求這類共享 Feature 存取有某種主機間協調，但沒有指定協調協定；不能把一次讀回當成永遠鎖住該值。')
 ], '這裡用時間順序圖說明成功界線；共用 Feature 的協調背景取自 §4.4。', True)

unit('lifetime', '4.4', '193-195',
 ('重設後保留什麼，要分可保存性與重設範圍', 'Persistence depends on saveability and reset scope'),
 ('Figure 466 把 FID 12h 的持續性列為 Yes，但該欄只適用於不可保存的 Feature。若本 Feature 可保存，應依 current／saved 與重設範圍判斷：整個 subsystem 範圍的重設按 Figure 126，局部範圍按 Figure 127。例如多控制器的 subsystem 只重設一個控制器，Set／subsystem 的共用目前值維持不變；符合全體條件的重設則回到 saved，沒有 saved 才回 default。',
  'Figure 466 lists persistence as Yes for FID 12h, but that column applies only to non-saveable features. If the feature is saveable, distinguish current from saved and use the reset scope: Figure 126 for whole-subsystem scope, Figure 127 for a subset. Resetting one controller in a multi-controller subsystem retains the shared current value. An applicable whole-subsystem reset instead restores saved, or default if no saved value exists.'),
 ('說明性範例：可保存的 FID 12h 目前是 15、saved 是 4。遇到 Figure 126 適用的全體重設後，current 回到 saved=4；若是 Figure 127 適用的局部重設，NVM Set／subsystem 範圍的 current 維持 15。',
  'Illustrative example: a saveable FID 12h has current=15 and saved=4. A whole-subsystem reset covered by Figure 126 restores current to 4. A subset reset covered by Figure 127 leaves the set/subsystem-scoped current value at 15.'),
 [
  ('先分開「目前值」與「已保存值」', 'current 是正在使用的設定，saved 是主機要求保存後留下的設定。SSFS 支援不代表每一項 Feature 都可保存，還要看該 FID 的 SVBL。只有本 Feature 可保存時，成功的 SV=1 設定才同時更新 current 與 saved；SV=0 的成功設定只更新 current。'),
  ('不可保存，不等於斷電一定遺失', 'Figure 466 的 FID 12h 列為 Yes，註腳 2 說明這個持續性欄只用在不可保存時。因此不可保存的 RRL 目前值仍必須跨 power cycle 與 reset 保留。SV=0 的意義是沒有提出保存要求，不能直接翻成「這個設定斷電就沒了」。'),
  ('可保存時，看這次重設覆蓋的範圍', 'Figure 126 適用於只有單一控制器的 subsystem 發生 Controller Level Reset，或多控制器且無多 domain 的 NVM Subsystem Reset，或確實重設全部 domain 的 NVM Subsystem Reset。可保存的 Feature 在這些情況用 saved 恢復 current；沒有 saved 時用 default，本篇為 4。'),
  ('局部重設不應重設仍被其他控制器共用的值', 'Figure 127 適用於可支援多控制器的 subsystem 發生 Controller Level Reset，以及多 domain 的 NVM Subsystem Reset 未覆蓋整個 subsystem 的情況。對 NVM Set／NVM subsystem 範圍而言，表中結果是維持不變，除非另有規定。要用這張表，先確認配置與實際重設範圍，不能只看事件名稱裡有 Reset。'),
  ('把保存要求寫成具體數值', '若已確認 SSFS=1、SVBL=1，Set 的 CDW10 加上 bit 31，得到 80000012h；NVMSETID 與 RRL 仍各放 CDW11、CDW12。若 Feature 不可保存卻送 SV=1，控制器必須以 Feature Identifier Not Saveable 中止，不能把該失敗當成已成功修改 current。'),
  ('讀能力、讀保存值、讀目前值各有用途', 'SVBL 告訴你能不能要求保存，SEL=2 告訴你保存查詢回什麼，SEL=0 才告訴你現在用什麼。判斷一次重設的結果時，把裝置能力、重設覆蓋範圍及前後值列在一起，才不會把 Figure 466 的一個 Yes 解讀成所有情境都永遠使用最後一次要求值。')
 ], 'Figures 126／127 以列選可保存性、以欄選 Feature 範圍；Figure 466 的 FID 12h 列必須和註腳 2 合讀。', True)
