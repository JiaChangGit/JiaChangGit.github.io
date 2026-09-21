"""Source-specific lessons, with one shared home for related field rules."""
EXAMPLES = {}
GUIDES = {}
MEMBERS = {}


def example(number, takeaway, worked, en):
    EXAMPLES[number] = dict(takeaway=takeaway, example=worked, en=en)


def group(key, title, relation, numbers, *rows):
    ident = 'rrl-' + key
    GUIDES[ident] = dict(id=ident, title=title, relation=relation, rows=list(rows))
    for number in numbers:
        MEMBERS[number] = ident


def lesson(figure):
    return EXAMPLES[int(figure['number'])]


def guide(figure):
    return GUIDES[MEMBERS[int(figure['number'])]]


example(755, '等級增加代表復原量減少，M／O 說明支援要求，不是效能評分。',
 '若 RRLS=8010h，裝置只支援 4、15；雖然表裡畫了 0～15，不能要求 Level 0。0 提供最多復原的敘述，有「若支援」的前提。',
 'Increasing levels mean decreasing recovery; M/O denotes support requirements, not performance scores.')
group('level-fields', '用支援要求與箭頭，讀懂整張等級總覽',
 '先確認功能受支援，再讀各列的 M／O，最後看復原量的方向。表裡沒有延遲單位或復原次數。', [755],
 ('Level 0～15', '16 個可能等級；數字較高，復原量較少。', '不能把 Level 8 當 8 次重試或 8 ms。'),
 ('O／M', 'O 表示選用；M 表示支援 RRL 時必備。4、15 為 M，其餘為 O。', '即使 Level 0 提供最多復原，也可能沒有實作。'),
 ('Definition：Default／Fast Fail', '4 為預設的一般復原量；15 為最少復原量。', '目前讀回 15 與預設是 4 可以同時成立。'),
 ('向下箭頭：Decreasing Amount of Recovery', '比較的是相對復原量，沒有定義等距、倍數、毫秒或成功率。', '從 4 調到 15，只能說選擇較少復原，不能承諾每次 I/O 快幾倍。'))

example(67, 'namespace 位於哪個 Set 內，決定它繼承哪一份 RRL。',
 '原圖的 A1、A2、A3 同在 Set A。若 A 的 RRL 為 15，三者共用 15；Set B 的 B1、B2 不因 A 的設定命令而一起改變。',
 'The containing NVM Set determines which RRL a namespace inherits.')
group('scope-fields', '從包含關係判斷設定影響',
 '這張圖沒有 bit 欄位；要讀的是外框、namespace 方塊與未配置空間三者的關係。', [67],
 ('NVM Set A／B／C 外框', '各代表一個與其他集合邏輯分開的 NVM 集合；圖上的 A／B／C 是示意名稱。', '實際命令使用 16-bit NVMSETID，不把字母 A 填進命令。'),
 ('NS A1～A3、B1～B2、C1', '每個具有已格式化儲存空間的 namespace 完整位於一個 Set；同 Set 繼承共同屬性。', 'A1 的讀取復原策略與 A2 共用 Set A 的 RRL。'),
 ('Unallocated 區域', '屬於該 Set、但尚未配置給 namespace 的儲存空間。', '之後從 Set A 建立新 namespace，仍繼承 A 的 RRL，不是從灰色區塊取得另一個等級。'))

example(338, '先讀支援功能的 bit，再用 RRLS 檢查候選等級，最後判斷可用的查詢方式。',
 'CTRATT 的相關 bits 為 0000000Ch 時，bit 3、2 同為 1，表示有 RRL 與 NVM Sets。RRLS=8011h 可選 0、4、15；ONCS bit 4 若為 0，仍只使用 SEL=0、SV=0。',
 'Check the feature bit, the candidate level in RRLS, and support for extended Feature selection separately.')
group('identify-fields', '同一份 Identify，回答三種不同問題',
 '只讀本篇所需的欄位切片；其他能力 bit 有自己的定義，不能把未在此介紹的 bit 全當保留。位置全部以 Identify Controller 結構起點為準。', [338],
 ('CTRATT bytes 99:96：RRLVLS bit 3', '1 支援 RRL；0 不支援。', '用 (CTRATT >> 3) & 1 判斷，不直接比較整個 CTRATT 是否等於 8。'),
 ('CTRATT：NSETS bit 2', '1 支援 NVM Sets，FID 12h 按 Set 選擇；0 則採 subsystem 範圍。', 'CTRATT=8 的相關 bits 表示有 RRL、沒有 NVM Sets。'),
 ('RRLS bytes 101:100：bits 15:0', '每一 bit 對應同編號等級；支援 RRL 時，bit 4、15 必須為 1。', '11 80 → 8011h；(8011h >> 8) & 1 = 0，Level 8 不受支援。'),
 ('ONCS bytes 521:520：SSFS bit 4', '1 支援非零 SEL／SV；0 不支援這些非零選項。', 'SSFS=1 才繼續用 SEL=3 查本 Feature 的 SVBL；SSFS 本身不等於 SVBL。'))

example(484, 'CDW11 放目標 Set，不放 namespace 編號，也不放等級。',
 'Set 7 的 CDW11=00000007h；若裝置不支援 NVM Sets，填 0 且本 Feature 忽略此欄，命令影響整個 subsystem。支援 Sets 時 0 是保留識別值，不是全部 Set。',
 'CDW11 identifies the target set, not a namespace or a recovery level.')
example(485, '4-bit RRL 是直接的等級代碼；Get 回覆使用同一格式，但位置改在 CQE DW0。',
 'Level 15 在 Set 的 CDW12 填 0000000Fh。成功 Get 且 SEL=0 時，若 CQE DW0 也是 0000000Fh，低 4 bits 表示目前等級 15；這不是 RRLS 的 bit 15 遮罩 8000h。',
 'RRL is a direct four-bit level code; Get reuses its layout in completion DW0.')
group('target-value-fields', '把目標與新值各自放到正確位置',
 '兩張圖相鄰，但代表兩個不同問題。把 NVMSETID 與 RRL 合在同一個 Dword，會失去正確的欄位語意。', [484,485],
 ('Figure 484：CDW11 bits 15:0', 'NVMSETID 選 Set；bits 31:16 保留。沒有 Set 支援時忽略此欄，主機填 0。', '7 是已存在 Set 的識別碼，不是第 7 個 namespace。'),
 ('Figure 485：Set CDW12 bits 3:0', 'RRL 直接指定 0～15 的某個受支援等級；bits 31:4 保留。', '15 填 Fh；沒有數量減 1 或再加 1 的換算。'),
 ('Figure 485：Get 成功且 SEL≠3', '相同 RRL 格式出現在 CQE DW0；Get 命令的 CDW12 不承載這份回覆。', '讀回值先取 DW0 & Fh，再依查詢的 SEL 說明是目前、預設或已保存。'),
 ('Reserved', '本範例將保留位清 0，不利用它們增加等級範圍或夾帶其他參數。', '0000001Fh 的 bit 4 已落入保留區，不能稱作 Level 31。'))

example(93, '共同格式先交代欄位位置，FID 12h 再賦予 CDW11／12 專屬含義。',
 'CDW11 的 byte offset 為 11×4=44，NVMSETID=7 存在 bytes 45:44；CDW12 從 48 開始，低 4 bits 才是等級。NSID 則在 bytes 7:4，本 Feature 填 0。',
 'The common format supplies locations; FID 12h supplies the meanings of CDW11 and CDW12.')
example(463, 'Set Features 的 DPTR 是否有用途，要看該 Feature 有沒有資料結構。',
 '本 Feature 的 Set 只要 CDW11 的 Set 編號與 CDW12 的等級，不需要把 Fh 放進一個 buffer 再提供地址。Figure 466 的 FID 12h 列明確標示不使用 data buffer。',
 'Set Features uses DPTR only when the selected feature requires an attribute data structure.')
example(464, 'FID 與 SV 分別選功能和保存要求，SV 不決定作用範圍。',
 'SV=0、FID=12h 得 00000012h；確認可保存後，SV=1 得 80000012h。兩者仍用同一個 CDW11 選 Set，不能藉 SV 改成單一 namespace 設定。',
 'FID selects the feature and SV requests saving; SV does not select the affected scope.')
group('envelope-fields', '命令外框與 FID 12h 參數的接法',
 '本篇只用共同格式中的 NSID、資料指標位置與 CDW10～12；欄位序號不是欄位內的值。', [93,463,464],
 ('NSID：bytes 7:4', '本 Feature 屬 NVM Set 或 subsystem scope，依 §4.4 應填 0；非零會被中止。', '有 A、B 兩個 namespace 共用 Set 7，也仍填 NSID=0、NVMSETID=7。'),
 ('DPTR：bytes 39:24', 'Figure 463 說明 Set 的資料指標；FID 12h 沒有屬性資料結構，因此不用此欄。', '不把等級 Fh 當成記憶體地址。'),
 ('CDW10：bytes 43:40', 'FID bits 7:0；SV bit 31；bits 30:8 保留。', '(1 << 31) | 12h = 80000012h，只在保存條件成立時使用。'),
 ('CDW11／12：bytes 47:44／51:48', '分別放 NVMSETID 與 RRL；其欄位規則見 Figures 484／485 的共同說明。', '相同數值 7 放在 CDW11 是 Set 7，放在 CDW12 則會選 Level 7。'),
 ('SV=1 的必要條件', '需 SSFS 支援及本 Feature 可保存；不可保存時要求 SV=1，回 Feature Identifier Not Saveable。', '收到失敗完成，不能把所要求的 15 當成設定成功的證據。'))

example(197, '沒有額外資料結構的 Feature，Get 會忽略 DPTR。',
 '查 RRL 後，主機應讀成功 CQE 的 DW0，不能在一份預先配置但未被使用的 buffer 裡找 Fh。DPTR 沒有資料，不表示 Get 沒有回覆。',
 'Get ignores DPTR when no feature data structure is used; the result can still be in the completion.')
example(198, 'SEL 讓同一個 FID 分別回答目前、預設、已保存或能力。',
 'SSFS=1 時，FID12h 搭配 SEL=0／1／2／3，CDW10 依序是 00000012h、00000112h、00000212h、00000312h。只改這個選擇，就會改變回覆的問題或格式。',
 'SEL chooses current, default, saved or capability information for the same FID.')
example(201, 'SEL=3 回三個能力 bit，不回等級清單，也不回目前 RRL。',
 'DW0=5 時，bit 2、0 為 1：可變更且可保存，NSSPEC=0。把 5 解讀成 Level 5 會用錯格式；讀目前值必須另送 SEL=0。',
 'SEL=3 returns three capability bits, not a level bitmap or the current RRL.')
group('readback-fields', '先用 SEL 選格式，再解讀回傳欄位',
 'Figure 198 是送出的命令；Figure 201 是 SEL=3 的回覆。SEL≠3 的成功回覆則回到 Figure 485 的 RRL 格式。', [197,198,201],
 ('Get CDW10：SEL bits 10:8、FID bits 7:0', 'SEL=0 current、1 default、2 saved、3 capabilities；4～7 保留，高位 31:11 保留。', 'SEL3 的 3 需左移 8 bits，不是把 FID 從 12h 改成 15h。'),
 ('Get CDW11／DPTR', 'CDW11 沿用 NVMSETID 指定目標；DPTR 因無資料結構而忽略。', '同一 Set 的設定與讀回，都使用相同 NVMSETID。'),
 ('能力 DW0：CHANG bit 2', '1 表示有可變更值；0 表示值不可變更。', '它不表示支援 RRL Level 2。'),
 ('能力 DW0：NSSPEC bit 1', '1 表示 namespace scope；0 不能自行推成 controller scope。', '本 Feature 的 Set／subsystem 範圍仍由 NSETS 與主範圍定義決定。'),
 ('能力 DW0：SVBL bit 0；31:3 保留', '1 可保存；0 不可保存。讀 saved 卻沒有 saved 值時，回 default。', '能力值 4 表示可變更但不可保存；current 值 4 才表示 Level 4。'))

example(466, 'FID 12h 列的 Yes 要連同註腳 2 讀，不能跳過可保存性判斷。',
 '不可保存的 FID 12h：Yes 表示目前值跨 power cycle 與 reset 保留。可保存的 FID 12h：這一欄不用，改查 current／saved 與適用重設表。',
 'The Yes in the FID 12h row is conditional on footnote 2: it applies only to a non-saveable feature.')
example(126, '全體範圍重設下，可保存的值回到 saved，沒有 saved 才回 default。',
 '可保存的 RRL 在 Set 7 目前為 15、saved 為 4。若這次重設符合 Figure 126 的整個 subsystem 條件，結果是 current=4，不是維持最後一次 SV=0 的 15。',
 'A whole-subsystem reset restores a saveable value from saved, or from default when no saved value exists.')
example(127, '局部範圍重設下，RRL 所在的 NVM Set／subsystem 欄是維持不變。',
 '可支援多控制器的 subsystem 只對其中一個控制器做 Controller Level Reset，適用本表；current=15 的共用 RRL 維持 15，不因該控制器重設而套用 controller-scope 欄的恢復規則。',
 'For a subset reset, the NVM Set/subsystem columns retain RRL rather than applying the controller-scope column.')
group('reset-fields', '先選能力與重設範圍，再讀交叉儲存格',
 '先看 FID 12h 是否可保存。不可保存的持續性由 Figure 466 與 §4.4 直接決定；可保存者再用 Figures 126／127 的對應欄。', [466,126,127],
 ('Figure 466：Feature Identifier／Uses Data Buffer／Scope', '只取 FID12h 這列：不使用 buffer，範圍為 NVM Set 或 NVM subsystem。', '不能因為 Set 命令經某個控制器送出，就改讀 controller scope。'),
 ('Figure 466：Current Setting Persists／註腳 2', 'Yes 只適用不可保存的 Feature；可保存者不用此欄。', '不可保存且目前為 15，跨 power cycle 與 reset 仍保留 15。'),
 ('Figure 126：Saveable 列', '適用全體範圍重設；所有 Feature scope 的此列都回 saved，無 saved 回 default，除非另有規定。', '目前 15、saved 4 → current 4。'),
 ('Figure 127：Saveable 列 × NVM Set／NVM subsystem 欄', '適用局部範圍重設；這兩欄維持 current，除非另有規定。', '目前 15、saved 4 → current 15；不能誤讀左側 controller 欄。'),
 ('兩張重設表的另一列', 'Non-saveable and non-persistent 同時要求不可保存與不具持續性；FID12h 的不可保存分支具持續性，不符合這一列。', '不可只看到 Non-saveable，就忽略後面 and non-persistent 而套用預設值。'),
 ('表格適用的配置與事件', 'Figure126：單控制器的 Controller Level Reset，或覆蓋整個 subsystem 的適用 NVM Subsystem Reset。Figure127：多控制器的 Controller Level Reset，或多 domain 中未覆蓋全體的 NVM Subsystem Reset。', '先寫出裝置配置與重設覆蓋範圍，再查結果；配置不是重設後的值。'))


# Source slices are deliberately narrower than the surrounding sections.
SOURCES = {
 755: ('8.1.23', '716', 'levels', 'Read Recovery Level Overview'),
 484: ('5.2.30.1.12', '499', 'set', 'Read Recovery Level Config – Command Dword 11'),
 485: ('5.2.30.1.12', '499', 'set', 'Read Recovery Level Config – Command Dword 12'),
 67: ('3.2.2', '107', 'scope', 'NVM Sets and Associated Namespaces'),
 338: ('5.2.14.2.1', '370-373,397-398', 'discover', 'Identify – Identify Controller Data Structure, I/O Command Set Independent'),
 93: ('4.1.1', '166-168', 'set', 'Common Command Format'),
 463: ('5.2.30', '482', 'set', 'Set Features – Data Pointer'),
 464: ('5.2.30', '483', 'set', 'Set Features – Command Dword 10'),
 197: ('5.2.12', '235', 'get', 'Get Features – Data Pointer'),
 198: ('5.2.12', '235-236', 'get', 'Get Features – Command Dword 10'),
 201: ('5.2.12.2', '238', 'get', 'Completion Queue Entry Dword 0 when Select is set to 11b'),
 466: ('5.2.30', '484-485', 'lifetime', 'Set Features – Feature Identifiers'),
 126: ('4.4', '193', 'lifetime', 'Current Value after Reset with Scope of Entire NVM Subsystem'),
 127: ('4.4', '193-194', 'lifetime', 'Current Value after Reset with Scope of Subset of the NVM Subsystem'),
}
