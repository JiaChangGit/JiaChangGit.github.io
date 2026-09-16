"""Independent Lockdown course; source page numbers are actual PDF viewer pages."""
BASE = 'NVME-BASE-2.4'
REPORT_ID = 'base-command-feature-lockdown'


def bi(zh, en):
    return dict(zh=zh, en=en)


UNITS = []


def unit(key, zh, en, section, pages, summary, english, example, example_en, steps, reading):
    UNITS.append(dict(key=key, title=bi(zh,en), section=section, pages=pages,
      summary=bi(summary,english), example=bi(example,example_en), steps=steps,
      reading=bi(reading, 'Use the field relationships and worked example to interpret this operation.')))


unit('model','先理解：限制的是哪個操作從哪裡進來','Start with the operation and its incoming interface','8.1.5','623-625',
 'Command and Feature Lockdown 讓主機限制特定管理命令，或 Set Features 對某個 FID 的設定操作。限制同時有操作種類、接收介面與控制器範圍；LID 14h 用來查可禁止項目與目前禁止狀態，Lockdown 命令用來改變它們。',
 'Command and Feature Lockdown restricts selected management commands or Set Features operations targeting a particular FID. Each restriction has an operation class, incoming interface and controller scope. LID 14h reports what can be prohibited and what is currently prohibited; Lockdown changes that state.',
 '假設 FID 06h 可被禁止：只限制「Set Features / FID 06h」與限制整個 Set Features opcode，影響不同。前者不會只因這條規則而禁止其他 FID 的設定，也不等同禁止 Get Features 讀取。',
 'Assume FID 06h is prohibitable. Restricting Set Features for FID 06h differs from restricting the entire Set Features opcode: the former does not by itself prohibit setting other FIDs or reading with Get Features.',
 [('從管理需求開始','假設一台機器已完成儲存裝置設定，接下來希望限制某些管理操作。Lockdown 讓控制器在收到指定操作時拒絕執行；它不修改 namespace 的資料格式，也沒有替每個 LBA 建立讀寫權限表。先辨認要限制的是哪種命令，才能選對入口。'),
  ('命令代碼與 Feature 編號分屬不同空間','Admin 命令用 opcode 選動作；Set Features 的命令內又用 FID 選設定項目。Lockdown 的 SCP=0 表示 OFI 是 Admin opcode，SCP=2 表示 OFI 是 Set Features 的 FID。相同的 06h 放在不同 SCP 底下，代表的操作可以完全不同。'),
  ('設定命令與被限制命令是兩次動作','先送 Lockdown，控制器成功完成後，對選定範圍建立限制。之後再有符合條件的命令進來，才會因限制而被拒絕。要分清「成功設定禁止」和「後來某個命令被禁止」的完成結果；前者成功，後者失敗，並不矛盾。'),
  ('讀回時必須問對問題','可禁止清單是裝置提供的能力，不是目前的黑名單；目前禁止清單才表示限制狀態。兩者都在 LID 14h，透過不同 CNTTS 選擇。沒有先保留查詢的種類與介面，就算拿到一串 opcode，也無法判斷它代表能禁止還是已禁止。'),
  ('知道功能的邊界','哪些命令或 FID 可被禁止由廠商決定，甚至可包含 Lockdown 自己。因此不能看到功能支援位元就假設每個管理操作都能限制，也不能先把解除限制的入口禁止，再假設一定能從同一條路徑解除。')],
 '先把查詢 LID 14h 與修改 Lockdown 分成兩條箭頭，再接到被限制的管理命令；Figure 365 的 SCP／IFC／CSEL 各回答不同問題。')

unit('capability','先查支援層級，再查可禁止項目','Check capability level before choosing an item','8.1.5','625',
 'Identify Controller 的 OACS.CFLS 表示基本 Lockdown 能力，CCFLS 表示可選控制器的擴充能力。CFLS=1 保證 CSEL=0 與 LID 14h；CCFLS=1 還要求 CSEL=1、2 與增強版 Log。每個 OFI 能否被禁止仍需查清單。',
 'OACS.CFLS advertises basic Lockdown support, while CCFLS advertises controller-scoped support. CFLS requires CSEL=0 and LID 14h; CCFLS additionally requires CSEL=1/2 and the enhanced log. The list still determines whether an individual OFI is prohibitable.',
 '只觀察 OACS 的 bits 13、10：2400h 同時設了 CCFLS 與 CFLS；0400h 只表示基本能力。不能把 0400h 的裝置當成一定支援 CSEL=1 或 ELPF=1。',
 'Considering only OACS bits 13 and 10, 2400h sets both CCFLS and CFLS, while 0400h advertises only basic support. The latter does not guarantee CSEL=1 or ELPF=1.',
 [('從 Identify 的能力位元往下讀','OACS 在 Identify Controller bytes 257:256，bit 10 是 CFLS、bit 13 是 CCFLS。這是 16-bit 欄位；從原始 bytes 讀到 00 24 時，以 little-endian 合成 2400h，再看各 bit，不能把第一個 byte 當成全部能力。'),
  ('基本能力已經包含哪些必要入口','CFLS=1 的控制器必須支援整個 NVM subsystem 範圍的 Lockdown，以及 Command and Feature Lockdown Log。它沒有直接承諾可以逐一挑控制器；因此第一層問題是功能存在，第二層才是控制器選擇。'),
  ('擴充能力如何接到查詢格式','CCFLS=1 必須同時支援基本能力，以及 CSEL=1 的單一控制器、CSEL=2 的某 primary controller 所屬 secondary controllers。對應的 ELPF=1 Log 能查指定控制器或彙整多個控制器。CCFLS=1、CFLS=0 不是合法的能力組合。'),
  ('功能支援不等於操作全部開放','通過能力檢查後，以 CNTTS=0 查目標種類的可禁止清單。如果要限制 FID，查 SCP=2；要限制 Admin opcode，查 SCP=0。某個命令本來就受控制器支援，也不表示它允許被 Lockdown 禁止，兩個問題不能互相代替。')],
 'Figure 338 很大，本篇只讀 OACS 的 CFLS、CCFLS；先核對 byte 位置，再把位元接到 Figure 274 的 ELPF 和 Figure 365 的 CSEL。')

unit('targets','介面與控制器是兩個獨立選擇','Select interfaces and controllers independently','5.2.16','432-433',
 'IFC 選命令接收介面：00b 為 Admin Submission Queue，01b 為該 Queue 加 Management Endpoint，10b 為 Management Endpoint。CSEL 選全部控制器、單一控制器或某 primary 的 secondary controllers，CSS 再提供所需控制器編號。',
 'IFC selects the incoming interface: 00b is the Admin Submission Queue, 01b adds the Management Endpoint, and 10b is the Management Endpoint only. CSEL selects all controllers, one controller, or a primary controller’s secondaries; CSS supplies the required controller identifier.',
 '要限制控制器 7 的 Admin Queue：CSEL=1、CSS=7、IFC=00b。送 Lockdown 的控制器與受影響的控制器不能混為一談；IFC 也不是在描述這次 Lockdown 是從哪裡送進去。',
 'To restrict controller 7 through its Admin Queue, choose CSEL=1, CSS=7 and IFC=00b. The controller processing Lockdown need not be confused with the selected target, and IFC describes where the restricted command is received.',
 [('同一操作走不同入口，結果可以不同','主機通常經由 Admin Submission Queue 送管理命令；Management Endpoint 則是帶外管理入口。規格容許同一操作在 Queue 被禁止、在帶外入口仍允許，但必須有相應支援。這裡只使用 Base 定義的入口與回覆規則，不推導未提供的 NVMe-MI 封包格式。'),
  ('先決定介面，再決定控制器集合','IFC 與 CSEL 一起決定適用範圍。CSEL=0 選 subsystem 全部控制器；1 選 CSS 指定的控制器；2 選 CSS 所指 primary controller 的全部 secondary controllers。最後一種不是把 primary 自己也列入目標。CSEL=Fh 是廠商定義，3h～Eh 保留。'),
  ('CSS 依 CSEL 改變意義','CSS 在 CDW14 高 16 bits。CSEL=0 時 CSS 保留；1 時是目標 Controller Identifier；2 時是 primary 的 Identifier。若 CSEL=2 的 CSS 不對應 primary，回 Invalid Controller Identifier。不能把 namespace 編號填進 CSS，也不能把 CSEL=2 理解成「控制器 2」。'),
  ('介面不存在或組合不合理時會拒絕','裝置沒有 Management Endpoint 卻選 IFC=01b 或 10b，Lockdown 回 Invalid Field in Command。SCP=4 是 NVMe-MI 的 PCIe Command Set opcode 類別，只能走 Management Endpoint；它若配 IFC=00b 或 01b 也會被拒絕。這個 PCIe Command Set 不是 NVMe 的 NVM I/O 命令集。'),
  ('控制器選擇也有能力條件','若 CCFLS=0，非零 CSEL 的 Lockdown 會以 Invalid Field in Command 拒絕。即使 CSS 看起來是有效的控制器編號，也不能跳過這項能力條件；編號有效與功能支援是不同層次。')],
 'Figure 365 選集合與介面；Figure 366 用 CSS 完成指名。對照時先寫下 CSEL，再讀 CSS，避免把一個欄位當成固定意義。')

unit('query','把 LID 14h 的查詢問題寫完整','Ask a precise question with LID 14h','5.2.13.1.20','305-306',
 'LID 14h 的 SCP 選項目種類，CNTTS=00b 查可禁止、01b 查 Admin Queue 目前禁止、10b 查 Management Endpoint 目前禁止。ELPF=0 使用一般格式；ELPF=1 使用增強格式，並以 LSI.CNTLID 選控制器，FFFFh 查所有控制器。',
 'For LID 14h, SCP selects the item class; CNTTS=00b requests prohibitable items, 01b current Admin Queue prohibitions, and 10b current Management Endpoint prohibitions. ELPF selects the basic or enhanced format. Enhanced requests use LSI.CNTLID, with FFFFh selecting all controllers.',
 '讀 512 bytes 的一般格式、查 Admin Queue 已禁止 FID：LID=14h、SCP=2、CNTTS=1、ELPF=0，NUMD=127，得到 CDW10=007F1214h。這是查詢，不會新增任何禁止項目。',
 'A 512-byte basic request for currently prohibited Admin Queue FIDs uses LID=14h, SCP=2, CNTTS=1, ELPF=0 and NUMD=127, giving CDW10=007F1214h. Reading the log does not add prohibitions.',
 [('用三個條件描述回覆內容','先選 SCP：0 是 Admin opcode，2 是 Set Features FID，3 是 Management Interface Command Set opcode，4 是其 PCIe Command Set opcode；1 與 5～F 保留。接著選 CNTTS，再選格式。若只記錄 LID 14h，會遺失足以改變清單意義的條件。'),
  ('可禁止與目前禁止用不同 CNTTS','CNTTS=0 回裝置允許禁止的項目；1、2 分別回兩種接收介面的目前禁止項目，3 保留。若 subsystem 沒有 Management Endpoint，卻查 CNTTS=2，命令會回 Invalid Field in Command；空清單和查詢本身失敗不能混為一談。'),
  ('只有增強格式使用這個控制器選擇','ELPF 是 CDW10 bit 14；設 1 時需要 CCFLS 支援。CNTLID 放在 CDW11 的 LSI，也就是高 16 bits；FFFFh 代表所有控制器。ELPF=0 時這個 LSI.CNTLID 保留，填入 7 也不會把一般格式變成控制器 7 的專屬回覆。'),
  ('把 byte 長度換成命令需要的 Dword 數','1 Dword 是 4 bytes，NUMD=(回傳 bytes/4)-1。512 bytes 是 128 Dwords，所以 NUMD=127，而不是 512。低 16 bits 放 NUMDL，高 16 bits 放 NUMDU。資料由 DPTR 指定的主機 buffer 接收，沒有放進完成佇列的 DW0。'),
  ('位移和清單索引不能互換','本篇範例 OT=0，以 byte offset 指向 Log 內的起點，LPOL／LPOU 合成 64-bit 值且需 4-byte 對齊。ELPF 是 Log 格式選擇，不是 offset 單位。若要用 OT=1 的 index-offset，必須有對應支援與項目定義，不能看到清單就自行把第 2 筆索引填成 byte offset 2。')],
 'Figure 274 解釋 CDW10 中間的 bits 14:8；275 解釋 CDW11 高 16 bits。Figure 204～208 則提供包住它們的長度與位移欄位。')

unit('basic','一般格式：一串代碼代表全體共同的項目','Basic format: a compact list with subsystem-wide meaning','5.2.13.1.20','307',
 '一般 Log 固定 512 bytes，CFILA 回報查詢種類，LNGTH 直接表示後方代碼清單的 byte 數，清單從 byte 4 開始並由小到大排列。對全體控制器的可禁止項目與 Admin Queue 目前禁止項目，不能把一般清單當成任何一台控制器的聯集。',
 'The basic log is 512 bytes. CFILA identifies the query meaning, LNGTH directly counts bytes in the ascending code list starting at byte 4. Its all-controller prohibitable and Admin Queue prohibited lists must not be mistaken for a union of items reported by any controller.',
 '回覆開頭 12 00 00 02 06 07：CFILA=12h 表示 Admin Queue 已禁止 FID；LNGTH=2，後面兩個 FID 是 06h、07h。02h 是長度，不是第三個 FID。',
 'Header and list bytes 12 00 00 02 06 07 mean CFILA=12h: currently prohibited Admin Queue FIDs. LNGTH=2 selects FIDs 06h and 07h. The byte 02h is the length, not a third FID.',
 [('先解釋 header，再讀值','byte 0 的 CFILA[5:4] 是 CS、[3:0] 是 SS，分別回映查詢 CNTTS 與 SCP；[7:6] 保留。bytes 2:1 保留，byte 3 才是 LNGTH。這個清單沒有逐項附上「這是 opcode 還是 FID」，必須先由 header 判斷。'),
  ('長度直接計數，0 代表空清單','LNGTH=n 時，有 n 個各 1-byte 的代碼，位置是 bytes 4 到 n+3。LNGTH=0 沒有有效代碼；不是 1 個值為 0 的項目。LNGTH 與 Get Log 的 NUMD 不同，不能對 LNGTH 再加 1。'),
  ('排序用來掃描，不是清單位置就是代碼','範例清單 [06h,07h] 在 byte 4、5。第一筆的索引是 0、byte offset 是 4、內容才是 FID 06h；三者各自回答第幾筆、存在哪、代表什麼。清單後方到 byte 511 的保留區不參與排序，也不當成其他命令。'),
  ('全體條件會隱藏只有部分控制器具備的項目','假設控制器 A 已禁止 FID 06h，但 B 未禁止。一般格式的 Admin Queue 目前禁止清單不能因為 A 禁止就當作「全體已禁止 06h」。需要知道部分控制器的差異時，改用增強格式的 FFFFh 彙整，再以特定 CNTLID 追查。')],
 'Figure 276 由 CFILA → LNGTH → CFIL 讀，先確認查詢種類，再決定到底有幾個代碼可解讀。')

unit('enhanced','增強格式：分清至少一台與全部控制器','Enhanced format: distinguish some controllers from all','5.2.13.1.20','308-309',
 '增強 Log 用 16-byte header 說明版本、查詢種類、CNTLID、SZE、NCFID 與 CFIDS，描述器按 CFI 遞增排列。CNTLID=FFFFh 時清單含至少一台控制器回報的項目；每筆 ACNTL=1 才表示所有控制器都回報這項。',
 'The enhanced log has a 16-byte header with version, query attributes, CNTLID, SZE, NCFID and CFIDS. Descriptors are sorted by CFI. With CNTLID=FFFFh, entries are reported by at least one controller; ACNTL=1 means every controller reports that item.',
 'A 禁止 06h、07h，B 只禁止 07h：查全體 Admin Queue 已禁止 FID，增強清單可回 (06h,ACNTL=0)、(07h,ACNTL=1)。06h 的 0 不是「沒禁止」，而是「不是全部都有」。',
 'If A prohibits FIDs 06h/07h and B prohibits only 07h, the enhanced all-controller Admin Queue list can return (06h,ACNTL=0) and (07h,ACNTL=1). Zero for 06h means not all controllers, not that none prohibit it.',
 [('先讀長度，再決定要拿多少資料','VER=0，header 的 SZE 是整份 Log byte 數。NCFID 是描述器數，CFIDS 是每筆描述器 byte 數，兩者直接計數。先讀足 16-byte header，確認完整大小，再依控制器傳輸能力讀取需要的內容；不能永久假設增強 Log 也只有 512 bytes。'),
  ('依 CFIDS 算位置，不把 byte offset 當控制器編號','第 i 筆從 16+i×CFIDS 開始。若 NCFID=2、CFIDS=2，兩筆起點是 16、18，清單結束於 byte 19，SZE=20 的範例完全裝得下。若未來描述器尺寸不同，應依回報步距前進，不能把 2 bytes 寫死成所有版本通用規則。'),
  ('Header 與描述器都有 CFIA，但不是同一個欄位','header byte 1 的 CFIA 包含 CS／SS，說明整份清單的種類；描述器 byte 1 的 CFIA 只有 bit 0 的 ACNTL 是本篇定義的有效屬性。把 header 的 12h 用來解讀 ACNTL，或把描述器的 01h 當 SCP，都會讀錯。'),
  ('全體彙整保留部分控制器的資訊','CNTLID=FFFFh 時，只要至少一台控制器回報某 CFI，就可在清單看到它。ACNTL=1 表示所有控制器都回報，0 表示至少一台但非全部。它不列出是哪幾台，因此需要進一步以各 CNTLID 查詢，才能建立精確的控制器對照表。'),
  ('描述器中的 0 與空清單也不同','NCFID=0 才是沒有描述器；ACNTL=0 是一筆已存在項目的屬性。以 A／B 的例子，06h 留在全體增強清單內，但不應出現在一般格式的全體共同禁止清單中。比較兩種格式時，先確認同一 SCP、CNTTS 和查詢期間。')],
 'Figure 277 給外框與步距，278 給每筆 CFI／ACNTL。拿 A／B 範例對照 276，才能看出增強格式增加的是什麼資訊。')

unit('command','完整編碼一次禁止與解除操作','Encode one prohibition and its removal','5.2.16','431-433',
 'Lockdown 使用 CDW10 的 CSEL、OFI、IFC、PRHBT、SCP，以及 CDW14 的 CSS／UIDX。PRHBT=1 禁止、0 允許；其他欄位保留原本要作用的種類、介面與控制器集合。重複禁止已禁止項目或允許已允許項目，本身不是錯誤。',
 'Lockdown uses CSEL, OFI, IFC, PRHBT and SCP in CDW10, plus CSS/UIDX in CDW14. PRHBT=1 prohibits and zero allows; the other selectors define the operation, interface and controller set. Repeating an existing prohibition or allowance is not itself an error.',
 '假設能力與清單均允許：禁止控制器 7 的 Admin Queue 設定 FID 06h，CDW10=00010612h、CDW14=00070000h。解除同一項限制只改 PRHBT=0，CDW10=00010602h；兩次都使用 Lockdown opcode 24h。',
 'Assuming support and eligibility, prohibit Set Features FID 06h on controller 7’s Admin Queue with CDW10=00010612h and CDW14=00070000h. Allow the same item with PRHBT=0, giving CDW10=00010602h. Both commands use Lockdown opcode 24h.',
 [('列出意圖再填 bits','本例限制的是 FID，因此 SCP=2；FID 是 06h，因此 OFI=6；只針對 Admin Queue，因此 IFC=0；要禁止，因此 PRHBT=1；只針對控制器 7，因此 CSEL=1、CSS=7。每個值都來自一句具體需求，而不是從另一個命令整段複製。'),
  ('演算 CDW10','CSEL 位於 bits 19:16，OFI 在 15:8，IFC 在 6:5，PRHBT 在 bit 4，SCP 在 3:0。因此 (1<<16)|(6<<8)|(0<<5)|(1<<4)|2 = 00010612h。bits 31:20 和 bit 7 保留。把 FID 06h 直接填 CDW10=6，會選錯 SCP，並未完成這項設定。'),
  ('CDW14 提供目標，不傳資料清單','CSS 在 bits 31:16，填 7 得 00070000h；本例 UIDX=0，不選廠商 UUID。Lockdown 沒有用資料 buffer 傳一串 OFI，一次只有這一個 OFI；除 CDW10、CDW14 外，其他命令專用欄位保留。'),
  ('等完成，再讀同一範圍的狀態','成功完成後，用 ELPF=1、CNTLID=7、SCP=2、CNTTS=1 查回。若範例只有 FID 06h 一筆，header 加 2-byte 描述器共 18 bytes；Get Log 傳輸以 Dword 計，需容納至少 20 bytes，但 SZE 外的傳輸尾端不能當有效 Log 內容。'),
  ('解除時保持其餘選擇一致','解除例子保留同一個 FID、介面與控制器，只清 PRHBT。先確認執行解除的 Lockdown 入口仍允許；如果先前也禁止了 Lockdown 自身，不能把 PRHBT=0 當成可繞過限制的特殊命令。重複送出原本已成立的禁止或允許，本身不算錯。')],
 'Figure 365 與 366 是同一筆命令的兩個 Dword。把完整算式對回各個 bits，再用 LID 14h 確認目標，而不是只看送出命令就假設已生效。')

unit('result','把設定失敗與命令被禁止分開判斷','Separate a rejected configuration from a prohibited command','5.2.16','433-434',
 'Lockdown 設定本身可因項目不可禁止、介面不支援或控制器選擇無效而失敗。28h 是 Prohibition of Command Execution Not Supported；1Fh 是 Invalid Controller Identifier。已受限制的 Admin 命令則回通用狀態 Command Prohibited by Command and Feature Lockdown。',
 'The Lockdown request can fail because the item is not prohibitable, an interface does not support it, or a controller selection is invalid. Command-specific 28h means Prohibition of Command Execution Not Supported and 1Fh means Invalid Controller Identifier. A subsequently prohibited Admin command instead returns the generic Command Prohibited by Command and Feature Lockdown status.',
 '第一次 Lockdown 成功；第二次送出的 Set Features 被禁止，回 SCT=0、SC=23h。若第一次 Lockdown 就因 OFI 不可禁止而回 SCT=1、SC=28h，代表沒有得到成功設定的證據，不能把這兩種失敗當成一件事。',
 'Lockdown may succeed and the later Set Features fail with SCT=0, SC=23h. If Lockdown itself returns SCT=1, SC=28h because the OFI is not prohibitable, there is no successful configuration result. These failures describe different operations.',
 [('先看是哪個命令完成','CQE 的 Command Identifier 對回原本命令，Status 再解出 SCT 與 SC。只看到 23h 或 28h 這個數字還不夠；SCT 決定狀態碼類別，也要知道完成的是 Lockdown 還是被限制的後續命令。'),
  ('項目不可禁止與入口不支援有不同要求強度','若 OFI 沒被標示為可禁止，Lockdown 必須回 Prohibition of Command Execution Not Supported。若它可禁止，但不支援 IFC 選到的其中一個介面，規格建議回同一狀態，也允許回 Invalid Field in Command；不能把建議誤寫成唯一合法結果。'),
  ('欄位組合錯誤不是成功建立限制','缺 Management Endpoint 卻選它、SCP=4 卻包含 Admin Queue、CCFLS=0 卻用非零 CSEL，都會回 Invalid Field in Command。CSEL=2 指到非 primary 的控制器編號則回 Invalid Controller Identifier。應把錯誤放回它所檢查的選擇，而不是統稱為「裝置不支援」。'),
  ('被限制的命令依接收入口得到回覆','已禁止的操作從 Admin Queue 進來，以 Command Prohibited by Command and Feature Lockdown 中止；Management Endpoint 則回 Access Denied Error Response。這是兩個入口的回覆形式，不能要求帶外回覆一定長得像 Admin CQE。'),
  ('多個問題同時存在時，不推論唯一檢查順序','通用規則允許在多個失敗原因同時成立時由廠商選擇回報狀態，除非有另外規定。學習例子一次固定一個錯誤原因，才看得出哪個條件導向哪個結果；這不代表控制器內部必須依教材排列的順序檢查。')],
 'Figure 367 是 Lockdown 本身的特定狀態；Figure 103 的 SC=23h 是後續命令被限制。用 Figure 99／101 把命令身分、狀態種類與代碼接起來。')

unit('persistence','限制何時消失，要看 CSEL 與持續性設定','Follow restrictions across allowance and power cycles','8.1.5','624-625',
 'CSEL=0 的全體限制在 Lockdown Persistence 啟用時跨 power cycle 保留；停用時持續到 subsystem power cycle 或後續解除。CSEL=1、2 的限制持續到 power cycle 或後續解除，不因 LDPE=1 自動取得全體限制的跨斷電保留規則。',
 'A CSEL=0 prohibition persists across power cycles when Lockdown Persistence is enabled; otherwise it lasts until a subsystem power cycle or subsequent allowance. CSEL=1/2 prohibitions last until a power cycle or allowance and do not inherit subsystem-wide power-cycle persistence from LDPE=1.',
 '同時有「CSEL=0 禁止 FID 06h」與「CSEL=1 禁止 FID 07h」，且 Lockdown Persistence 已啟用。subsystem power cycle 後，前者按全體持續性規則保留，後者不因這個設定而跨斷電保留。',
 'With Lockdown Persistence enabled, suppose CSEL=0 prohibits FID 06h and CSEL=1 prohibits FID 07h. After a subsystem power cycle, the first persists under the all-controller rule; the second does not gain power-cycle persistence from that setting.',
 [('先問限制是用哪個 CSEL 建立','持續性取決於當初 Lockdown 的 CSEL。CSEL=0 搭配 LDPE=1，禁止會跨 power cycle 持續，直到後續 Lockdown 解除；LDPE=0 則可由 subsystem power cycle 結束。CSEL=1、2 依自己的規則，在 power cycle 或後續解除時結束。一般 Controller Reset 不等於整個 subsystem power cycle。'),
  ('LDPE 和 LDPS 分別是設定與讀回','Lockdown Persistence 屬於 Configurable Device Personality 的 PERID=02h；FID=22h 是 Feature 編號，不能把 02h 當成同一層編號。設定的 CDW11 bit 0 是 LDPE；Get 回覆 CQE DW1 bit 0 是 LDPS。DW0 則回報該 personality 的屬性，兩個 Dword 要分開讀。'),
  ('設定持續性與凍結設定是不同動作','Personality 是裝置的一組配置，frozen 表示不允許再任意改變該配置。CDW13 的 CHPS 控制是否改設定，PERFS 控制凍結請求，PERID 選配置。設定接受後是否還待特定 reset，需看 MRSTT 與 PPSC；教材不能把送出 LDPE=1 直接當成所有情況都已生效。'),
  ('避免把必要的解凍入口一起封死','當 Lockdown Persistence 已啟用，而此 personality 未凍結或不支援認證解凍，要求禁止整個 Set Features 或 FID 22h 的 Lockdown 必須回 Prohibition of Command Execution Not Supported。這是特定條件下的規則，不表示任何 FID 永遠都能被禁止。'),
  ('認證命令有明確限定的例外','若持續性已啟用，且任一 personality 支援認證解凍，控制器與 Management Endpoint 必須允許指定 CDP Authentication、SPSP=0002h 的 Security Send／Receive，即使先前限制了這兩個 opcode。例外只涵蓋這種認證用途，不能擴張成所有 Security 命令都無條件允許。'),
  ('解凍與目前禁止清單仍應分開觀察','成功的 Security Send 認證解凍若解凍的是 Lockdown Persistence Personality，持續性會停用。這不等於該命令本身直接移除每個目前禁止項目；後續狀態與是否跨 power cycle 保留應分別查證。本篇教到影響 Lockdown 的條件，不展開金鑰、驗證訊息與其他 personality 的操作。')],
 'Figure 518／519 對照輸入 LDPE 和輸出 LDPS；512～514 與 292 僅補足 PERID、凍結、待生效狀態與認證支援，避免把持續性當成單一無條件開關。')

unit('uuid','同一廠商 FID 有不同定義時，用 UUID 選版本','Select the intended vendor definition with a UUID','5.2.16','432-433',
 '廠商定義 FID 的 Lockdown 在 SCP=2 且相關命令與項目支援 UUID 選擇時，使用 CDW14.UIDX 選 UUID List 項目。LID 14h 對 SCP=2 的廠商 FID 查詢也可使用 UIDX；SCP≠2 時忽略 UIDX。UIDX 是清單索引，不是 FID 或 byte offset。',
 'For a vendor-specific FID, Lockdown uses CDW14.UIDX when SCP=2 and UUID selection is supported for the commands and item involved. LID 14h can likewise use UIDX for vendor FIDs with SCP=2; other scopes ignore it. UIDX is a UUID List index, not a FID or byte offset.',
 '假設兩份廠商定義都使用 FID C0h，UUID List 的第 2 項對應所需定義。使用 UIDX=2；不是把 C0h 填 UIDX，也不是填第 2 項的 byte offset 64。',
 'If two vendor definitions both use FID C0h and UUID List entry 2 identifies the intended definition, use UIDX=2. Neither FID C0h nor that entry’s byte offset 64 belongs in UIDX.',
 [('先確認什麼情況需要 UUID','標準定義的主要流程通常不用選廠商 UUID。只有涉及同一個廠商 FID 的不同定義，且相關能力支援時，才需用 UUID 區分內容。SCP=2 是必要條件；對 Admin opcode 等其他 SCP，UIDX 會被忽略，不會改變操作種類。'),
  ('Lockdown 與查詢應對到同一份定義','Lockdown 需要本命令及 Set Features 對該廠商 FID 支援 UUID 選擇，才以 CDW14 提供 UIDX。LID 14h 查詢 SCP=2 且指定 UUID 時，控制器應依該 UUID 回報廠商 FID 的限制資訊。沒有把這層定義對齊，清單上的 C0h 可能不是原本要限制的設定。'),
  ('索引、項目位置與 UUID 本體有三種長度','UIDX 是 7 bits；UUID List 每項 32 bytes，項目中的 UUID 本體是 16 bytes。清單前 32 bytes 保留，第一項索引 1 位於 byte 32，第二項位於 byte 64；第 2 項的 UUID 本體從 byte 80 開始。命令填的是 2，不是 64 或 80。'),
  ('0 不表示第一個 UUID','UIDX=0 表示不指定 UUID；有效非零索引必須對應受支援且有效的 UUID。指到全 0、NVMe Invalid UUID，或不支援於該資訊的 UUID，依通用 UUID 規則回 Invalid Field in Command。NVMe Invalid UUID 是 FFFFFFFF_FFFFFFFF_7FFFFFFF_FFFFFFFFh，用來保留已失效項目的索引位置；它和全 0 的清單終止值不同。清單末尾第 127 項必須為 0，不能把最大 7-bit 數當成一定可用的索引。')],
 'Figure 782 說明命令只帶索引；347／348 說明索引對到哪一項與哪 16 bytes。再回到 Figure 366 和 208，確認 UIDX 放在哪個命令。')
