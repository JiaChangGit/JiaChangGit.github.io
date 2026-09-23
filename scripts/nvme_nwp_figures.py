"""Unique source-figure lessons and shared, narrowly scoped field guides."""
EXAMPLES={}
GUIDES={}
MEMBERS={}

def example(number,takeaway,worked,en):
    EXAMPLES[number]=dict(takeaway=takeaway,example=worked,en=en)

def group(key,title,relation,numbers,*rows):
    ident='nwp-'+key
    GUIDES[ident]=dict(id=ident,title=title,relation=relation,rows=list(rows),
        headers=['欄位或圖上標示','讀值與條件','帶入例子後的結論'])
    for n in numbers:MEMBERS[n]=ident

def lesson(figure):return EXAMPLES[int(figure['number'])]
def guide(figure):return GUIDES[MEMBERS[int(figure['number'])]]

example(735,'M／O 表示支援要求；兩個 persistence 欄表示事件發生後是否仍保持原狀態。',
 'WPS=2 這列在 Power Cycles 是 No、Controller Level Resets 是 Yes。配合正文可知：真正 power cycle 後回到 0；沒有 power cycle 的控制器重設仍是 2。不是看見任一 Reset 就讀 No。',
 'M/O describes support requirements; the two persistence columns describe retention across different events.')
group('state-definitions','把狀態、支援要求與持續性分開讀',
 'Figure 735 不是能力 bitmap，也不是命令格式；每一列是一種狀態。以下代碼用 Figure 541 補上，讓名稱、數值與事件結果接得起來。',[735],
 ('M／O 與註腳','M：有實作本功能時必備；O：有實作本功能時仍可選擇是否支援。','NWPC bit0=1、bits2:1=0 的裝置可以只有狀態 0、1。'),
 ('No Write Protect／Write Protect','0 為未設保護，1 為一般保護；兩者都跨 power cycle 與 Controller Level Reset 保留。','斷電不會自動把 1 解除成 0。'),
 ('Write Protect Until Power Cycle','2 在沒有 power cycle 的 Controller Level Reset 後保留；power cycle 才使其回到 0。','僅重設控制器後，仍不能送 Set WPS=0 來解除 2。'),
 ('Permanent Write Protect','3 是永久保護；兩種事件後都保持。','power cycle 不提供 3 → 0 的路徑。'),
 ('Persistent Across 欄的讀法','先選目前狀態，再選實際事件；No 表示不保留原狀態，轉到哪裡要結合正文。','狀態 2 的 No 不是功能消失，而是狀態轉為 0。'))

example(736,'圖上的普通箭頭由 Set Features 觸發，唯一標 Power Cycle 的箭頭是 2 回到 0。',
 '原圖有 1 → 2 與 1 → 3，但沒有 2 → 3。即使永久保護受支援且 PWPC=1，已在 2 時要求改成 3 仍會被拒絕；必須尊重目前狀態，而不只檢查目的地能力。',
 'Ordinary arrows are Set Features transitions; the explicitly labeled power-cycle arrow returns state 2 to 0.')
group('state-arrows','用起點、方向和觸發事件讀狀態機',
 '這張圖沒有 bit 欄位，節點與箭頭就是需要解讀的資訊。Figure 736 只畫轉換關係；可用能力、WPC 與 MDS 的附加條件見控制欄位組。',[736],
 ('Initial state → No Write Protect','新建 namespace 從 0 開始。','這是建立時的起點，不代表每次控制器重設都回到 0。'),
 ('0 → 1 與 1 → 0','成功 Set Features 進入一般保護或解除一般保護。','先在 1，要求 0，是有箭頭的操作。'),
 ('0／1 → 2','兩個來源都可以要求進入 Until Power Cycle，另須支援、WPUPCC=1、MDS=0。','來源 1 也能進入 2，不必先解除成 0。'),
 ('0／1 → 3','兩個來源都可以要求進入 Permanent，另須支援且 PWPC=1。','來源 2 不在這組箭頭內。'),
 ('2 → 0：Power Cycle','這個返回箭頭的事件不是 Set Features。','沒有 power cycle 的重設保留 2。'),
 ('3 沒有離開箭頭；2 沒有 Set 離開箭頭','要區分「改變到另一狀態」與同值請求；本節的 Feature Not Changeable 條文針對改變狀態的嘗試。','不替原圖補上 3 → 1，也不把條文擴寫成所有同值請求必須失敗。'))

example(338,'NWPC 說明裝置能力，MDS 限制狀態 2，SSFS 決定是否能使用非零查詢選項。',
 'NWPC=05h 表示支援 0／1 與 3，不支援 2；不是目前 WPS=5。若 NWPC=07h 但 MDS=1，也仍不能使用狀態 2。這些結論要讀各自的 bit，不能比較整個 CTRATT 是否只等於 400h。',
 'NWPC advertises state support, MDS restricts state 2, and SSFS controls nonzero Feature selectors.')
group('identify','先辨認位元組位置，再辨認每個 bit 的問題',
 'Figure 338 很長；本篇只取 NWPC、CTRATT.MDS 與 ONCS.SSFS。其他未在此列出的能力 bit 有各自用途，不是全都保留。位置從 Identify Controller 結構起點起算。',[338],
 ('NWPC byte 531：bit0 NWPWPS','1 支援 No Write Protect／Write Protect；0 不支援本功能，bits1、2 也須為 0。','NWPC=01h 已表示支援本功能的基本兩種狀態。'),
 ('NWPC bit1 WPUPCS','1 支援 Until Power Cycle，且必須支援 WPC 控制欄位。','(NWPC >> 1) & 1 = 0 時，不選 WPS=2。'),
 ('NWPC bit2 PWPS；bits7:3 保留','1 支援 Permanent，且必須支援 WPC。bit2 本身不是 PWPC 進入許可。','05h 的 bit2=1；仍要另外確認 WPC.PWPC。'),
 ('CTRATT bytes 99:96：bit10 MDS','1 支援多 domain；0 表示單 domain 且不支援多 domain 回報。','使用 (CTRATT >> 10) & 1；MDS=1 阻止進入 2。'),
 ('ONCS bytes 521:520：bit4 SSFS','1 支援非零 SEL／SV；0 時不使用非零選項。特定 Feature 的限制仍優先適用。','SSFS=1 不會讓不可保存的 FID84h 變成可以 SV=1。'))

example(756,'WPC 的兩個 bit 只控制進入請求，不儲存 namespace 目前的 WPS。',
 'Device Configuration Block byte2=02h：PWPC=1、WPUPCC=0，所以只開放進入永久狀態的這項控制條件。重設後 byte2 的這兩個 bit 清零，先前已成功設為 3 的 namespace 仍是 3。',
 'The WPC bits control entry requests; they do not store the current namespace state.')
group('rpmb-control','WPC 的位置、兩個許可與重設後結果',
 '本篇引用 Figure 756 的 byte2。它是 RPMB target0 的 512-byte Device Configuration Block 的一部分；相鄰 bytes0、1 屬 Boot Partition 保護，不能拿來解讀 namespace 的 WPS。',[756],
 ('byte2：WPC；Type=RW','可讀寫的控制欄位，透過 RPMB 的存取機制操作；不在 FID84h 的命令參數內。','WPC=01h 不等於某個 namespace 已是 WPS=1。'),
 ('WPC bit0：WPUPCC','0 拒絕要求進入 2 的 Set；1 允許處理該要求，但仍須符合能力與狀態條件。','NWPC 支援且 WPC=01h，也不能忽略 MDS=1 的禁止。'),
 ('WPC bit1：PWPC','0 拒絕要求進入 3 的 Set；1 允許處理，並不直接執行狀態轉換。','把 PWPC 設為 1 本身不會把所有 namespace 變永久保護。'),
 ('power cycle／Controller Level Reset','支援本功能時，WPUPCC、PWPC 均清為 0。','重設後要進入 3 的新請求與既有 WPS=3 的保留，是不同問題。'),
 ('保留區與不支援時','WPC bits7:2 保留；不支援 Namespace Write Protection 時 WPC 必須為 0。結構 bytes511:3 保留。','例子只使用 00h～03h，不把保留 bit 當成更多保護狀態。'))

example(541,'WPS 是低 3 bits 的狀態代碼；成功的非能力查詢把同一格式放在 CQE DW0。',
 'CDW11=00000003h 表示 Permanent，雖然二進位是 011b，仍只選一個狀態。Get SEL=0 成功回 DW0=00000002h 才表示目前 Until Power Cycle；它不是 NWPC bit1 的能力回報。',
 'WPS is a three-bit state code; a successful non-capability Get returns that layout in completion DW0.')
group('wps','把名稱、bit 編碼與回覆位置連起來',
 'Set 的參數與 Get 的回覆共用 WPS 格式，但所在的位置不同。只有命令成功時，才按該次 SEL 的回覆格式解讀結果。',[541],
 ('bits2:0：WPS=000b／001b','0：No Write Protect；1：Write Protect。','Set CDW11=00000001h 要求進入一般保護。'),
 ('WPS=010b／011b','2：Until Power Cycle；3：Permanent。','3 是狀態代碼，不是兩個可獨立開關的保護 flags。'),
 ('WPS=100b～111b；bits31:3','4～7 是保留代碼，高 29 bits 也是保留。','能力查詢 DW0=6 不用此表；用此表硬解會讀到保留代碼。'),
 ('Get 成功且 SEL≠3：CQE DW0','以 Figure541 格式回覆；本功能沒有 default，實務查目前值使用 SEL=0。','Get 命令不以 CDW11 的舊內容作為回覆，主機讀的是 completion DW0。'))

example(93,'NSID 選對象，CDW10 選 Feature，CDW11 放 WPS；序號與欄位值不可混淆。',
 'namespace7 的 NSID 位於 bytes7:4；WPS=1 位於 CDW11 bits2:0，CDW11 的 byte offset 是 11×4=44。offset44 是欄位的位置，不是 namespace ID 或狀態。',
 'NSID selects the namespace, CDW10 selects the feature, and CDW11 carries WPS; locations are not values.')
example(463,'Set 是否使用 DPTR 取決於 Feature 是否需要資料結構；FID84h 不需要。',
 '設定 WPS=1 的 1 直接放 CDW11，不配置一個含 1 的資料 buffer 再把地址放 DPTR。Figure466 的 FID84h 列標示 Uses Data Buffer=No。',
 'Set needs DPTR only for a feature attribute structure; FID84h uses no such structure.')
example(464,'SV 是保存請求，FID 是功能識別值；不使用 SV 不代表保護會在斷電後消失。',
 'SV=0、FID84h 得 CDW10=00000084h；把 bit31 設為 1 得 80000084h，卻會對此不可保存的功能提出無效的保存要求。WPS=1 的跨斷電持續性仍由狀態規則決定。',
 'SV requests saving and FID selects the feature; clearing SV does not imply loss of protection on power cycling.')
example(466,'FID84h 的 No 帶註腳8，必須回到此 Feature 的狀態規則判斷持續性。',
 '只看 Current Setting Persists 的 No，會錯把 WPS=1 讀成斷電即解除。註腳8 指定由該 Feature 定義，而 Figure735 規定 WPS=1 保留；本列同時指出 namespace 作用範圍、無屬性 buffer。',
 'The FID84h persistence cell carries footnote 8, which delegates retention to the feature-specific state rules.')
group('command-envelope','把目標、外框與功能參數放到正確位置',
 '只取 Figure93 的 NSID、CDW 位置，Figure463 的資料指標用途、Figure464 的 SV／FID，以及 Figure466 的 FID84h 列與註腳2、8。',[93,463,464,466],
 ('NSID bytes7:4：active、inactive、invalid','active 已附接本控制器；inactive 已配置但未附接；invalid 是無效識別值。通用格式對 inactive 回 Invalid Field in Command，對 invalid 回 Invalid Namespace or Format，除非另有特例。','不存在的 ID 和存在但未附接的 ID 不要寫成同一種「不可用」。'),
 ('NSID=FFFFFFFFh','Set：MDS=0 通常設定本控制器附接的所有 namespace，MDS=1 拒絕。Get：本功能沒有全體查詢特例，回 Invalid Namespace or Format。','不從一次 broadcast Set 推論每個目標都可轉換，也不假設更新原子性。'),
 ('CDW10 bytes43:40','SV bit31；FID bits7:0；bits30:8 保留。FID84h 不可保存，使用 SV=0。','(0 << 31) | 84h = 00000084h。'),
 ('CDW11 bytes47:44；DPTR bytes39:24','CDW11 帶 WPS；Figure463 定義的 DPTR 不用來放本 Feature 屬性。','byte offset44 = 11×4；不是把 WPS 左移44位。'),
 ('Figure466：84h 列 Scope／Uses Data Buffer','Scope=Namespace；Uses Data Buffer=No。','不是只對收到命令的控制器生效。'),
 ('Figure466：註腳2與8','持續性欄只供不可保存 Feature 使用；84h 正是不可保存，但註腳8仍要求使用專屬狀態規則。','WPS1保留、WPS2在power cycle清除，不能一起讀成No。'))

example(197,'Get 不需要資料 buffer，也可以在完成項目裡回報 WPS。',
 '讀 namespace7 的 WPS 時，成功 CQE DW0=1 就是結果；預先配置的 buffer 未被寫入不代表控制器沒有回答。Figure197 規定無資料結構時忽略 DPTR。',
 'Get may return WPS in completion DW0 without transferring an attribute buffer.')
example(198,'SEL 選的是要問的問題，本功能不提供每一種選項的有效值。',
 'FID84h 的 CDW10=00000084h 問 current；00000184h 問 default，卻因沒有 default 被拒絕。SEL=2 也不代表查前一次 WPS，因為它問的是通用 saved 值。',
 'SEL selects the question; this feature does not provide a value for every selector.')
example(201,'CHANG 可以為 1，即使 namespace 目前已在不可改變的永久狀態。',
 'SEL3 成功回 DW0=6：bit2 CHANG=1、bit1 NSSPEC=1、bit0 SVBL=0。表示功能有可變更值、屬 namespace 作用範圍、不可保存；不是允許把目前 WPS3 解除，也不是第6種保護狀態。',
 'CHANG can remain set even when the current namespace state is permanent and unchangeable.')
group('query','先看 SEL，再決定如何解讀 DW0',
 '以下非零 SEL 的討論以控制器支援 SSFS 為前提。成功 Get 的回覆格式不能只根據 DW0 數字猜測。',[197,198,201],
 ('CDW10 FID bits7:0、SEL bits10:8','FID84h；SEL0問current，1問default，2問saved，3問capabilities；4～7保留，bits31:11保留。','SEL3需左移8位：00000384h。'),
 ('SEL0／1／2 與 DPTR','0成功回WPS；1因沒有default回Invalid Field in Command。2因不可保存轉問default，所以也不能取得WPS。沒有屬性結構，忽略DPTR。','需要目前保護狀態就用SEL0，不使用default或saved猜測。'),
 ('SEL3 DW0 bit2：CHANG','只要此Feature任一屬性有可變更值，就回1，即使目前值不可改。','不能因CHANG1就畫出Permanent的解除箭頭。'),
 ('SEL3 DW0 bit1：NSSPEC','1表示namespace 作用範圍。','WPS針對所選namespace，其他控制器也須遵守。'),
 ('SEL3 DW0 bit0：SVBL；bits31:3保留','FID84h不可保存，SVBL0。','6 = 4 + 2；能力三位元與WPS三位元剛好同寬，但語意不同。'))

example(737,'先找命令名稱，再看上標註腳，最後判斷這次動作會不會修改受保護媒體。',
 'Dataset Management 在右欄卻帶註腳1；若該次動作嘗試修改受保護 namespace 的非揮發媒體，必須失敗。Flush 的註腳2則明確規定成功且不產生作用，兩者不能用同一句「允許」概括。',
 'Find the command, read its footnote, and then consider whether this particular action modifies protected media.')
group('allowed-commands','把兩個命令集合與三項註腳讀完整',
 'Figure737 不是 bit 表。左右兩欄分別屬 Admin 與 NVM Command Set；上下相鄰的命令沒有一一配對或執行先後關係。以下按共同限制重新編排，保留全部列出的命令。',[737],
 ('Admin：無特別上標的列','Device Self-test、Get Features、Get Log Page、Identify、Namespace Attachment，依各命令規則正常處理。','正常處理仍可能因其他原因失敗，不保證每筆成功。'),
 ('Admin：註腳1','Directive Send、Security Receive、Security Send、Set Features、Vendor Specific；若指定動作嘗試修改該 namespace 非揮發媒體，必須失敗。','Set Features列在表內不代表可以略過WPS轉換限制。'),
 ('Admin：Directive Receive／註腳3','嘗試配置Streams資源時，以Namespace is Write Protected中止。','同一命令的其他操作仍需按自己的定義處理。'),
 ('NVM：無特別上標的列','Compare、Read、Reservation Register、Reservation Report、Reservation Acquire、Reservation Release、Verify，正常處理。','保護媒體不等於完全禁止查詢或存取協調。'),
 ('NVM：註腳1','Dataset Management、Vendor Specific；嘗試修改該namespace非揮發媒體的動作必須失敗。','不能僅看到Dataset Management在表中就說所有動作都允許。'),
 ('NVM：Flush／註腳2','必須成功且無作用；該namespace所有volatile write cache資料與metadata已在進入保護時提交到非揮發媒體。','不是讓Flush在已保護的媒體上繼續寫回舊資料。'),
 ('表後三種拒絕條件','未列出的命令：指定受保護NSID，或指定未受保護NSID但會改到受保護namespace，或未指定NSID卻會改到受保護namespace。','依次可用Write、跨namespace的Format NVM、會影響受保護namespace的Sanitize理解。'))

example(213,'AMRO 是健康警告，不是「有人把 namespace 設成 Write Protect」的通知。',
 'namespace7 的 WPS=1 且 SMART Critical Warning bit3=0 並不矛盾。即使所有namespace都用本功能保護，也不能只因此把AMRO設為1。',
 'AMRO is a health warning, not a notification that Namespace Write Protection was configured.')
group('health','只讀 SMART 的相關位元，不借用它代表設定',
 'Figure213 只取 byte0 Critical Warning 的 bit3。此處不把其他健康欄位納入教學範圍。',[213],
 ('byte0 bit3：All Media Read-Only (AMRO)','1回報全部媒體處於唯讀狀況，但不可僅因Namespace Write Protection狀態改變造成唯讀就設1。','AMRO0不能證明namespace7的WPS是0。'),
 ('健康欄位與Feature的界線','用Get FID84h查WPS；不要把AMRO當另一份WPS或狀態機的事件旗標。','WPS0也只表示本機制未設保護，不保證媒體健康且所有Write成功。'))

example(103,'Namespace is Write Protected 表示命令被保護限制，不是進入保護的要求被拒絕。',
 '受保護namespace的Write回SCT=0、SC=20h；要求把WPS2改成0則用Figure554的Feature Not Changeable。先辨認原命令在做什麼，再比較完成狀態。',
 'Namespace is Write Protected identifies an operation blocked by protection, not a rejected request to enter protection.')
example(554,'Feature Not Saveable 與 Not Changeable 分別拒絕保存要求與當下不可執行的值變更。',
 'WPS0時錯送SV1：不可保存；WPS2時要求改成0：不可改變。兩者都不是用重送相同參數就能證明已設好狀態。',
 'Not Saveable rejects a save request; Not Changeable rejects a currently disallowed value change.')
group('status','以狀態類型與代碼區分三種失敗',
 '本篇只取Figure103的20h與Figure554的0Dh、0Eh。SCT是狀態碼類型，SC是該類型內的代碼；以下不是整個CQE Status欄的16-bit編碼。',[103,554],
 ('SCT0／SC20h：Namespace is Write Protected','命令受到本狀態機的寫入保護禁止。','Write指定已受保護的namespace，不能只用另一控制器重送來繞過。'),
 ('SCT1／SC0Dh：Feature Identifier Not Saveable','所選Feature不支援保存值。','FID84h搭SV1，不能解讀成「永久保護能力不支援」。'),
 ('SCT1／SC0Eh：Feature Not Changeable','Feature值不支援變更，或此時該值不能改。','原WPS2／3的改變請求、WPC不允許的進入要求、MDS1下進入2，都屬本篇相關情境。'))

SOURCES={
 735:('8.1.18','690','model','Namespace Write Protection State Definitions'),
 736:('8.1.18','690','transitions','Namespace Write Protection State Machine Model'),
 737:('8.1.18.2','691-692','commands','Commands Allowed when Specifying a Write Protected NSID'),
 541:('5.2.30.1.38','538','configure','Write Protection – Command Dword 11'),
 338:('5.2.14.2.1','372,397-398,401','controls','Identify – Identify Controller Data Structure, I/O Command Set Independent'),
 756:('8.1.24','717-718','controls','RPMB Device Configuration Block Data Structure'),
 93:('4.1.1','166-168','configure','Common Command Format'),
 463:('5.2.30','482','configure','Set Features – Data Pointer'),
 464:('5.2.30','483','configure','Set Features – Command Dword 10'),
 466:('5.2.30','485','transitions','Set Features – Feature Identifiers'),
 197:('5.2.12','235','configure','Get Features – Data Pointer'),
 198:('5.2.12','235-236','configure','Get Features – Command Dword 10'),
 201:('5.2.12.2','238','configure','Completion Queue Entry Dword 0 when Select is set to 11b'),
 213:('5.2.13.1.3','247','observe','SMART / Health Information Log'),
 103:('4.2.1','175','observe','Status Code – Generic Command Status Values'),
 554:('5.2.30.4','545','observe','Set Features – Command Specific Status Values'),
}
