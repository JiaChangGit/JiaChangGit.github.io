"""Authored Directives/Streams course and equivalent overview summaries."""

BASE = 'NVME-BASE-2.4'
NVM = 'NVME-NVM-CS-1.3'
REPORT_ID = 'base-directives-streams'


def bi(zh, en):
    return {'zh': zh, 'en': en}


UNITS = []


def unit(key, title, section, pages, summary, example, steps, reading, source=BASE):
    UNITS.append(dict(key=key, title=bi(*title), section=section, pages=pages,
                      summary=bi(*summary), example=bi(*example), steps=steps,
                      reading=bi(*reading), source=source))


unit('model', ('先理解 Streams 要解決什麼問題', 'What Streams communicates'),
 '8.1.9, 8.1.9.1, 8.1.9.3', '642-649',
 ('Directives 讓主機與控制器交換額外資訊。Streams 用主機指定的 Stream Identifier，指出哪些寫入資料屬於同一組；控制器可利用分組改善資料配置或效能，但這個編號不直接指定 NAND 的實體位置。',
  'Directives exchange additional information between the host and controller. Streams uses a host-selected Stream Identifier to associate writes with a group. The controller may use that grouping for placement or performance improvements; the identifier does not select a physical NAND address.'),
 ('說明性情境：應用程式把短期暫存資料標成 stream 7，把長期保留資料標成 stream 40。兩組仍寫入各自指定的 LBA；stream 只補充分組資訊，不取代 LBA。',
  'Illustrative scenario: an application labels temporary data with stream 7 and long-lived data with stream 40. Each write still targets its specified LBAs; the stream adds grouping information instead of replacing the address.'),
 [('先看主機知道、SSD 未必知道的資訊', '作業系統送出 Write 時，控制器能看到要寫的 LBA 範圍與資料，卻不一定知道這些資料屬於哪個應用用途。例如兩筆相隔很遠的 LBA，都可能是同一批短期暫存資料。Streams 讓主機額外標出這個關係。控制器可以依此安排相關資料，但規格沒有承諾某個編號會對應固定的 NAND block，也沒有保證每種工作負載都會加速。'),
  ('分清管理操作與實際寫入', 'Directive Send／Receive 是 Admin 命令，用來查能力、啟用功能、取得狀態或管理資源。真正把使用者資料寫入 namespace 的仍是 Write；Write 內的 DTYPE 與 DSPEC 才把本次資料連到某個串流。主機不需要每寫一筆資料就先送一次 Directive Send。'),
  ('同一個 00h，要看它出現在哪裡', '在 Directive Send／Receive 的 DTYPE 中，00h 選擇 Identify Directive，這是一套查詢與啟用 Directives 的操作。在 I/O 命令的 DTYPE 中，00h 表示本次不使用 Directive。Identify Directive 也不是一般的 Identify Admin 命令：前者查 Directives，後者可查控制器與 namespace 的整體能力。'),
  ('把本篇的邊界放在流程旁邊', '本篇完整說明 Identify Directive、Streams、Directive Send／Receive、Host Identifier FID 81h 的共同與 PCIe 規則，以及 NVM Command Set 對 Streams 的大小單位。Data Placement 的 §8.1.9.4 不展開；只有 Streams 本身明定的互斥啟用限制會在相關段落說明。廠商專屬 Directive 的編碼僅供辨認，不能替廠商推定其行為。')],
 ('Figure 702 先分 Directive 類型，Figure 703 再問 I/O 的 DSPEC 在所選類型下代表什麼。先辨認管理命令和 I/O 的語境，才解讀 00h。',
  'Read Figure 702 for type selection and Figure 703 for the meaning of DSPEC in an I/O command. Establish the command context before interpreting 00h.'))

unit('host', ('先讓控制器知道哪些路徑屬於同一主機', 'Identify the host across controller paths'),
 '5.2.30.1.35, 5.2.30.1.35.1', '534-536',
 ('FID 81h 登記 Host Identifier，讓同一 NVM subsystem 內的控制器辨認共同主機。相同非零值可建立共同身分；0h 則表示不與其他控制器建立這種關聯。PCIe 的預設值為 0h，此 Feature 不可保存。',
  'FID 81h registers a Host Identifier so controllers in an NVM subsystem can recognize a common host. Equal nonzero values establish that identity; 0h does not associate a controller with other controllers. The PCIe default is 0h and this Feature is not saveable.'),
 ('控制器 C1、C2 都服務主機 A 時，在使用 Streams 前登記相同的非零 Host Identifier。若兩者都保留 0h，即使數值相同，也不能據此當作同一主機。',
  'If C1 and C2 serve host A, register the same nonzero Host Identifier before using Streams. Leaving both at 0h does not establish a shared host merely because the numeric values match.'),
 [('為什麼不能只看控制器編號', '同一台主機可能經兩個控制器存取同一個 namespace。Streams 需要知道這兩條路徑是不是同一主機，否則無法正確判斷是否共享啟用狀態、串流編號或專用資源。Host Identifier 的用途就是建立這種關聯；它不是 NSID，也不是 Stream Identifier。選值與確保唯一性的方式由主機環境決定，規格沒有指定產生演算法。'),
  ('選 64-bit 或 128-bit 時，要連同能力一起讀', 'FID 81h 的 CDW11.EXHID=0 選 64-bit，EXHID=1 選 128-bit；Identify Controller 的 CTRATT.HIDS 表示是否支援 128-bit。PCIe 可以支援其中一種或兩種，不能看到 PCIe 就假設兩種都可用。若所選長度不支援，回 Invalid Field in Command；若 subsystem 同時支援兩種長度，卻偵測到另一控制器已用不同長度的非零識別值，回 Host Identifier Inconsistent Format。'),
  ('資料 buffer 和控制位元各司其職', 'Set Features 用 FID=81h、SV=0，CDW11 選長度，DPTR 指向 HOSTID 資料。Get Features 的 SEL=0 查目前值，回覆也要看資料 buffer；SEL=3 查的是 Feature 支援能力，不能把它的 CQE DW0 當成 Host Identifier。64-bit 格式用 HOSTID 的 bytes 7:0，bytes 15:8 是保留區；128-bit 格式則使用 bytes 15:0。'),
  ('0h 改成非零值，並不是把舊串流一起搬過去', '目前 Host Identifier 為 0h 時，可以登記 HOSTID；目前已是非零值時，再要求設定會回 Command Sequence Error。若先以 0h 開始使用 Streams，之後才改成非零值，原有串流資訊與配置資源仍屬於舊的 0h 身分，不會自動轉給新身分。因此規格建議先登記非零值，再使用 Streams；若 SRNZID=1，這更是啟用 Streams 的必要條件。'),
  ('不要把非零身分當成可保存的設定', 'PCIe 的 Host Identifier 預設是 0h，沒有 saved value。主機在重新建立控制器的使用狀態時，需要確認目前身分與其他路徑的關係。0h 也可能用於部分裝置的 reservation，但它不代表跨控制器的同一主機，相關 registration／reservation 不跨 Controller Level Reset 保留；CTRATT.RHII=1 表示使用 reservations 前要求非零身分，0 表示未回報；Streams 的對應要求則看 SRNZID。本篇只用這個限制理解身分，不展開 reservation 操作。')],
 ('Figure 537 選長度，Figure 538 給實際識別值；必要引用的 Get／Set Features 表用來分清 FID、SEL、SV、DPTR 與 HOSTID。',
  'Figure 537 selects the width; Figure 538 carries the identity. The referenced Get/Set Features fields distinguish FID, SEL, SV, DPTR, and HOSTID.'))

unit('enable', ('查支援、登記身分，再啟用 Streams', 'Check support and enable Streams'),
 '8.1.9, 8.1.9.2, 8.1.9.3', '642-650',
 ('先由 OACS.DIRS 確認 Directives，再用 Identify Directive 查 Streams 是否支援與啟用。Enable Directive 的 CDW11 選 Identify 操作，CDW12 才選要啟用的 Streams；namespace 與 Host Identifier 一起決定共享的啟用狀態。',
  'First check OACS.DIRS, then query Streams support and enablement through the Identify Directive. For Enable Directive, CDW11 selects the Identify operation and CDW12 selects Streams as the target. Namespace and Host Identifier determine the shared enable state.'),
 ('對 NSID=1 啟用 Streams：Directive Send 的 CDW11=00000001h，CDW12=00000101h。前者是 DTYPE=00h、DOPER=01h；後者是目標 DTYPE=01h、ENDIR=1。',
  'To enable Streams for NSID=1, Directive Send uses CDW11=00000001h and CDW12=00000101h. The former selects DTYPE=00h/DOPER=01h; the latter selects target DTYPE=01h and ENDIR=1.'),
 [('第一層查詢：控制器是否提供 Directives', 'OACS.DIRS=1 表示控制器支援 Directives；此時必須支援 Directive Send、Directive Receive 以及 Identify Directive。它沒有直接保證 Streams 一定支援。下一步要用 Directive Receive、DTYPE=00h、DOPER=01h 取得 Identify Directive 的 Return Parameters；對這個查詢使用 NSID=FFFFFFFFh 會回 Invalid Field in Command。'),
  ('第二層查詢：分開看支援、啟用與重設保留', '4096-byte 回覆的前 3 組 32-byte 位元向量，分別位於 bytes 31:0、63:32、95:64。第一組的 SDIRS 說控制器是否支援 Streams，第二組的 SDIRE 說指定 namespace 是否已啟用，第三組的 SDIRCLR 說狀態能否跨 Controller Level Reset 保留。Streams 的 SDIRCLR 固定是 0；後文會說明多控制器仍有活動路徑時的例外，不能只憑這個 bit 推論所有路徑一起失去狀態。'),
  ('啟用要求裡有兩個 DTYPE，但用途不同', '外層 CDW11.DTYPE=00h 選 Identify Directive，DOPER=01h 選 Enable Directive。內層 CDW12.DTYPE=01h 才指向 Streams；ENDIR=1 啟用、0 停用。DSPEC 在這個操作不使用，也沒有資料傳輸。把 CDW11.DTYPE 直接填成 01h，會變成 Streams 的操作空間，並不是正確選到 Identify 的 Enable。Identify Directive 永遠啟用，不能用這個操作改變它，目標 DTYPE=00h 會被拒絕。'),
  ('作用對象不是單一開關而已', '一般以 NSID 選 namespace；同一非零 Host Identifier 下，已啟用控制器所附加的共同 namespace 必須維持相同 Directive 啟用狀態。對 Streams 使用 NSID=FFFFFFFFh 啟用／停用，作用於整個 NVM subsystem 的 namespaces 與 controllers。因此同樣的 FFFFFFFFh，在 Identify Return Parameters 是非法值，在 Enable Streams 卻有整體範圍，必須依操作判斷。'),
  ('哪些情況不能啟用', 'SRNZID=1 而 Host Identifier 仍為 0h 時，啟用會回 Host Identifier Not Initialized。要求啟用不支援的類型會回 Invalid Field in Command；資源不足則可能回 Stream Resource Allocation Failed。另一個明確限制是：namespace 所屬 Endurance Group 若已啟用 Flexible Data Placement，就不能啟用 Streams。這裡只說明兩者不能同時用在該 namespace，不展開被排除的 Data Placement 操作。')],
 ('Figure 704 選操作、705 看能力與狀態、706 組啟用要求、707 看資源不足的結果。Figure 338 只取 DIRS／HIDS／MDTS 等本篇所需能力。',
  'Read Figures 704–707 as operation selection, support/state, enable request, and resource failure. Figure 338 contributes only the capabilities needed here.'))

unit('commands', ('讀懂 Directive 命令的欄位與資料方向', 'Read the Directive command envelope'),
 '5.2.7, 5.2.8', '227-228',
 ('Directive Receive 的資料由控制器送往主機，Directive Send 則相反；實際是否有資料傳輸取決於操作。CDW11 用 DTYPE／DOPER 選操作，DSPEC 的含義由類型決定；需要 buffer 時，NUMD 是 Dword 數量減 1。',
  'Directive Receive transfers data toward the host and Directive Send toward the controller, when the selected operation transfers data. CDW11 selects DTYPE/DOPER and type-specific DSPEC. For buffer transfers, NUMD encodes the Dword count minus one.'),
 ('讀 32-byte Streams Return Parameters 時，NUMD=32÷4−1=7。Allocate Resources 雖然也是 Directive Receive，卻沒有資料傳輸；配置數量由 CQE DW0 回來。',
  'A 32-byte Streams Return Parameters transfer uses NUMD=32÷4−1=7. Allocate Resources is also a Directive Receive operation, but transfers no data; its allocation count comes back in CQE DW0.'),
 [('先定位命令，再定位操作', 'Directive Receive 的 Admin opcode 是 1Ah，Directive Send 是 19h。共同格式中的 NSID 指目標 namespace，DPTR 指主機資料 buffer；CDW11[31:16] 是 DSPEC，[15:8] 是 DTYPE，[7:0] 是 DOPER。要辨認一次操作，至少連同命令方向、DTYPE 與 DOPER 一起讀，不能只看 DOPER=01h。若某類型不支援，或雖支援但未啟用，指定該 DTYPE 的 Directive Send／Receive 都會以 Invalid Field in Command 中止；這和 I/O 命令在未啟用任何 Directive 時忽略附加欄位的規則不同。'),
  ('同一個操作值在不同命令下會變義', 'DTYPE=01h 表示 Streams：Receive 的 DOPER=01h、02h、03h 依序是 Return Parameters、Get Status、Allocate Resources；Send 的 DOPER=01h、02h 是 Release Identifier、Release Resources。因為類型與方向都參與解讀，Receive 01h 不是 Send 01h 的反向版本，它們處理的事情不同。'),
  ('不要把 NUMD 當成 byte 長度，也不要把 0 當成無資料', '若操作有資料傳輸，CDW10.NUMD 以 32-bit Dword 為單位，而且保存數量減 1。因此 bytes=(NUMD+1)×4；NUMD=0 代表 4 bytes。4096-byte Identify Directive 回覆使用 NUMD=1023，32-byte Streams 回覆使用 NUMD=7。Enable Directive、Allocate Resources 與兩個 Release 操作明定無資料傳輸，不能套這條公式替它們創造一個 4-byte payload。'),
  ('請求大小與結構大小不同時，Receive 如何回傳', '如果 NUMD 對應長度小於回覆結構，控制器只傳所要求的那一部分；如果大於結構，控制器只傳整個結構，不額外補資料。例如對 32-byte Return Parameters 要求 16 bytes，只能取得 subsystem 欄位，讀不到 byte 16 起的 SWS；要求 64 bytes，後半 buffer 也不能當作控制器回傳的參數。這個介面沒有一般化的分頁 offset 欄位，不能把 DSPEC 想成「從第幾個 byte 繼續讀」。'),
  ('命令完成和回覆資料要一起確認', '命令執行結果由 Admin CQE 回報。若操作有資料 buffer，先確認狀態成功與取得的有效長度，再讀對應結構；若是 Allocate Resources，讀 CQE DW0 的 NSA。CDW12／CDW13 是否使用由該操作定義，其他未使用的命令專屬欄位是保留欄位；PCIe 的 Admin 資料指標使用 PRP，不使用 SGL。')],
 ('Figure 181–186 分成 Receive／Send 兩組：DPTR 是位置、NUMD 是量、CDW11 是操作選擇。對照共同格式 Figure 93，注意 buffer 地址與命令欄位位置不同。',
  'Figures 181–186 form Receive/Send groups: DPTR locates memory, NUMD selects quantity, and CDW11 selects the operation. Use Figure 93 to distinguish buffer addresses from command-field positions.'))

unit('resources', ('配置多少資源，與開了幾條串流分開看', 'Separate allocated capacity from open streams'),
 '8.1.9.3, 8.1.9.3.1.1, 8.1.9.3.1.3', '647-652',
 ('Streams 可使用 namespace 的專用資源，或使用尚未專用配置的 subsystem 資源。Allocate Resources 要求的是可同時追蹤的數量，回覆 NSA 可以小於 NSR；真正開啟串流，是後續 Write 使用尚未開啟的編號時。',
  'Streams uses either namespace-exclusive resources or subsystem resources not exclusively allocated. Allocate Resources requests concurrent tracking capacity; returned NSA may be smaller than NSR. A stream is opened when a later Write uses an identifier that is not already open.'),
 ('假設 MSL=8，原本 NSSA=8，主機要求 NSR=4、實際得到 NSA=3，則 NSSA 變成 5。還沒寫入時 NSO 可以是 0；接著以編號 7、40 寫入，才會開啟兩條串流。',
  'Assume MSL=8 and NSSA=8. A request for NSR=4 that receives NSA=3 leaves NSSA=5. NSO can still be 0 before any writes; writes with identifiers 7 and 40 then open two streams.'),
 [('資源的用途是保存正在使用的串流資訊', '串流資源讓控制器追蹤某個開啟中的 Stream Identifier，例如維持資料關聯所需的狀態或 buffer。它不是分配給使用者資料的 LBA 容量。MSL 表示 subsystem 最多同時支援多少開啟的串流；NSSA 表示尚未分配成 namespace 專用的資源數。NSSA 不是「現在還沒開串流的空閒數」，因為這一池中的部分資源可能正被共用串流使用，這部分另由 NSSO 計數。'),
  ('先看兩條資源來源，再看計數', '若指定 namespace／主機關聯的 NSA 非零，這個關聯使用專用資源，可同時開啟最多 NSA 條串流；若 NSA=0，就依條件使用 subsystem 資源。NSO 是這個查詢身分可見的 namespace 開啟數。NSSO 則只計算使用非專用資源的開啟串流，不含其他 namespace 已配置專用資源中的串流。把 NSSO 當成整台 SSD 的總開啟數，會漏算專用部分。'),
  ('要求 4，不一定拿到 4', 'Allocate Resources 用 CDW12[15:0].NSR 直接表示要求數量，不是數量減 1；CQE DW0[15:0].NSA 回實際配置數量。控制器可以配置小於或等於要求的數量，主機必須按回覆安排並行串流，而不是按 NSR 假設成功數。若無法配置專用資源，可能回 Stream Resource Allocation Failed；若還有 subsystem 資源，也可以成功回 NSA=0，讓主機使用共用資源。'),
  ('想增加資源，不能把第二次 Allocate 當成加法', '若這個 namespace 已有該主機的專用資源，再送 Allocate Resources 會回 Invalid Field in Command。要從 3 改成 5，先 Release Resources，再要求完整的 5；不是再申請 2。中間會經過沒有專用資源的狀態，因此它不是一個保證立即擴容成功的原子操作。其他主機是否共享這些專用資源，還要看 SSID。'),
  ('資源用滿後，Write 不必然失敗', 'NSA 非零且新編號需要資源時，若專用資源已用滿，控制器會在該 namespace 任選一個既有編號釋放，再給新串流使用。NSA=0 且 subsystem 共用資源已忙滿時，可以從使用共用資源的任意 namespace 釋放任一串流；若所有資源都已分配為專用，則把這筆 Write 當作沒有指定串流的寫入。不要把「沒有新的追蹤資源」直接翻成「寫入資料被丟棄」。')],
 ('Figure 712 先分 subsystem、namespace、namespace 加主機三種欄位。Figure 714／715 比較要求與實際配置；Figure 711 說明無法配置時的結果。',
  'Group Figure 712 by subsystem, namespace, and namespace-plus-host scope. Figures 714/715 distinguish requested and granted counts; Figure 711 describes allocation failure.'))

unit('sharing', ('同一個 Stream Identifier，到底是不是同一條串流', 'When equal Stream Identifiers mean the same stream'),
 '8.1.9.3, 8.1.9.3.1.1, 8.1.9.3.1.2', '647-652',
 ('Stream Identifier 的意義要連同 namespace、Host Identifier 與 NSSC.SSID 判斷。SSID=0 時，不同非零主機身分的同號串流彼此獨立；SSID=1 時，同一 namespace 的同號串流可由不同非零主機身分共享。',
  'Interpret a Stream Identifier together with namespace, Host Identifier, and NSSC.SSID. With SSID=0, equal identifiers belonging to different nonzero host identities are separate streams. With SSID=1, those hosts may share the same numbered stream in the same namespace.'),
 ('C1、C2 的 Host Identifier 都是 A，C3 是 B，C4 是 C；都存取 NSID=1、stream 7。SSID=0 時是 3 條串流，SSID=1 時是 1 條。A、B、C 在例子中都代表不同的非零識別值。',
  'C1 and C2 use Host Identifier A, C3 uses B, and C4 uses C. All access NSID=1 with stream 7. There are three streams with SSID=0 and one with SSID=1. A, B, and C denote distinct nonzero identifiers.'),
 [('先用 namespace 畫出邊界', 'Stream Identifier 只是一個 16-bit 編號，主機可選 0001h–FFFFh，且可以使用稀疏集合，例如 7、40、1000，不必連續。不同 namespace 上的相同編號不能只因數字相同就視為同一串流。先固定 namespace，再用 Host Identifier 與 SSID 比較各控制器看到的資料關聯。'),
  ('SSID=0：同一主機的多條路徑共享，其他主機各自使用', '主機 A 在 C1、C2 登記同一非零值，兩條路徑對 namespace 1 的 stream 7 指向同一串流。主機 B 使用另一非零值時，它在同一 namespace 使用 stream 7，代表 B 自己的另一條串流。此時 NSA／NSO 與 Get Status 的可見內容，也按相同非零 Host Identifier 的關聯來算，不能用 A 的查詢推論 B 配置了多少。'),
  ('SSID=1：把共享範圍擴到不同非零主機身分', '所有控制器回報相同的 NSSC。當 SSID=1，對同一 namespace 而言，不同非零 Host Identifier 使用相同 Stream Identifier，指向同一串流；專用資源與 Get Status 的可見範圍也包含這些非零主機身分。這表示主機間需要協調編號的用途，不能一邊把 stream 7 當暫存資料，另一邊假設它完全是自己的獨立群組。'),
  ('0h 不加入上述非零身分共享', '即使 SSID=1，Host Identifier=0h 仍表示一個獨立主機關聯，不會因為其他控制器也填 0h 就共享串流意義。這也是為什麼先初始化 Host Identifier 很重要。Figure 710 用 A、B、C 等標籤表達身分關係；圖中的 1-a、1-b 等尾碼是區分路徑的圖示標籤，不是要求主機把字串寫入 DSPEC。')],
 ('Figure 710 固定 namespace 與編號，只改 Host Identifier 與 SSID，觀察分組數如何改變。計數結果再連到 Figure 712 的 NSA／NSO 與 Figure 713。',
  'In Figure 710, hold namespace and identifier fixed while changing Host Identifier and SSID. Connect the resulting grouping to NSA/NSO in Figure 712 and status visibility in Figure 713.'))

unit('write', ('把一筆 Write 接到串流', 'Attach a Write to a stream'),
 '8.1.9.1, 8.1.9.3', '643-649',
 ('使用 Streams 的 Write 指定 DTYPE=1、DSPEC=非零 Stream Identifier；首次使用尚未開啟的編號時，控制器開啟串流。DTYPE=0 或 Streams 的 DSPEC=0 不使用串流分組；未啟用類型的處理還要看是否已有任何 I/O Directive 啟用。',
  'A Streams Write uses DTYPE=1 and a nonzero Stream Identifier in DSPEC. First use of an unopened identifier opens a stream. DTYPE=0 or a zero Streams DSPEC omits stream grouping; handling an unenabled type also depends on whether any I/O Directive is enabled.'),
 ('CETYPE=0 的簡化例子：寫 8 blocks、stream 7，其他本例控制位元為 0，則 CDW12=(1<<20)|7=00100007h，CDW13=7<<16=00070000h。LBA 起點另在 CDW10／11。',
  'Simplified CETYPE=0 example: write eight blocks with stream 7 and other illustrated control bits zero. CDW12=(1<<20)|7=00100007h and CDW13=7<<16=00070000h. CDW10/11 separately hold the starting LBA.'),
 [('Write 才是串流開始被使用的時刻', 'Enable Streams 是讓功能可用，Allocate Resources 是取得追蹤容量，都還沒把使用者資料寫入串流。Write 第一次指定某個尚未開啟的編號，控制器才開啟它；之後再用相同編號，沿用同一開啟中的串流。主機沒有另外一個必須先送的 Open Stream 命令。'),
  ('用一個完整欄位例子對照 Admin 命令', '以 NVM Write、CETYPE=0 為例，CDW12[23:20] 的 DTYPE 是 4 bits，填 1 表示 Streams；CDW13[31:16] 的 DSPEC 填 stream 7。CDW12[15:0] 的 NLB=7 代表 8 logical blocks。Admin Directive 的 DTYPE 位於 CDW11 且寬度是 8 bits，不能把整個 Admin CDW11 複製到 Write 的 CDW12。CETYPE 決定 CDW13 的下半部格式，本例固定 0，不延伸到其他命令擴充。'),
  ('LBA、數量、串流編號是三個獨立問題', '假設起點 LBA=128、數量 8 blocks、stream=7，這筆 Write 改寫 LBA 128–135，並告訴控制器它們屬於 stream 7。把 stream 改成 40，不會把資料搬到 LBA 40；把 NLB 改成 15，才會變成寫 16 blocks。資料本身仍由 Write 的 DPTR 提供，DSPEC 不包含使用者資料。'),
  ('忽略與拒絕的條件要分開', '沒有任何 I/O Directive 啟用時，I/O 命令的 DTYPE 與 DSPEC 都會被忽略；DTYPE=0 也會讓這兩個欄位不參與 Directive 處理。若已啟用一個以上 I/O Directive，卻指定不支援或未啟用的非零類型，控制器必須回 Invalid Field in Command。Streams 已適用而 DSPEC=0 時，這筆命令仍正常處理，如同未指定 Directive，不會開啟一條名為 stream 0 的串流。'),
  ('串流標記沒有改寫一般 Write 的資料保證', 'Stream Identifier 補充資料關聯，並沒有自動提供排序、原子寫入或持久保存保證。這些仍由 Write 的其他欄位與原有規則決定。例如本例把 FUA 留 0，不能因為使用 stream 7，就宣稱 CQE 成功時一定已寫到非揮發媒體；需要這種保證時要依既有 Write／Flush 的語意安排。')],
 ('必要引用 NVM Figures 70–72 只取 SLBA、NLB、DTYPE、CETYPE 與 DSPEC 的連接。先算真正的 LBA 範圍，再把串流編號視為附加資訊。',
  'The necessary slices of NVM Figures 70–72 connect SLBA, NLB, DTYPE, CETYPE, and DSPEC. Calculate the LBA range before interpreting the additional stream information.'))

unit('sizes', ('把 SWS／SGS 換成實際的資料量', 'Convert SWS and SGS into data sizes'),
 '5.13', '175',
 ('NVM Command Set 的 SWS 以 logical blocks 為單位；SGS 則以 SWS 為單位。先用 namespace 的 logical block 大小換成 bytes，才能比較寫入對齊、傳輸長度與整組資料的解除配置範圍。',
  'For the NVM Command Set, SWS is measured in logical blocks; SGS is measured in SWS units. Convert through the namespace logical block size before comparing write alignment, transfer length, and group-sized deallocation ranges.'),
 ('假設每個 logical block 是 4096 bytes、SWS=8、SGS=4：理想寫入單位為 8×4096=32 KiB；一個 stream granularity 單位為 4×8=32 blocks，也就是 128 KiB。',
  'With 4096-byte logical blocks, SWS=8 and SGS=4, the optimal write unit is 8×4096=32 KiB. One stream-granularity unit is 4×8=32 blocks, or 128 KiB.'),
 [('先讀欄位單位，不能先比數字大小', 'SWS=8 不是 8 bytes，也不是 8 條串流；它在 NVM Command Set 表示 8 logical blocks。若 namespace 使用 4096-byte logical block，就相當於 32768 bytes。SGS=4 表示 4 個 SWS，所以先算 4×8=32 logical blocks，再乘每個 block 的 bytes。這兩個欄位提供寫入與媒體配置的粒度提示，和 MSL／NSA 的資源個數是不同維度。'),
  ('大小正確還不夠，起點也要對齊', '以上例而言，LBA 128 起寫 16 blocks，同時滿足起點是 8 的倍數、長度也是 8 的倍數。LBA 130 起寫 16 blocks，雖然長度正確，起點卻沒有對齊。規格用這些條件描述最佳化效能的寫入方式，沒有把每一筆未對齊 SWS 的有效 Write 都改成必須拒絕的命令。'),
  ('Figure 708 的上下兩層在講大小如何組成', '上層以多個 SWS 組成一個 Stream Granularity，下層以多個 Stream Granularity 組成完整串流。它不是把主機命令排成必須依序執行的流程，也不是指定 NAND 的實際地址。控制器可以用 SGS 單位準備媒體並組織資料；主機看到的是能協助安排工作負載的大小資訊。'),
  ('解除配置時，比對的是 SGS 的換算結果', '若用 Dataset Management 解除配置與某串流相關的 logical blocks，規格建議起點和長度符合 Stream Granularity 的對齊與倍數。以上例，LBA 128 起的 64 blocks 是 2 個 32-block 單位，符合這個建議；LBA 136 起的 64 blocks 雖然符合 SWS，卻沒有對齊 32-block 單位。解除配置處理 LBA 的資料配置，Release Identifier 處理串流追蹤狀態，兩者不是同一操作。'),
  ('還要檢查傳輸上限與格式變更', 'SWS 對應的資料大小建議不超過 MDTS。MDTS 的非零值以最小記憶體頁大小乘 2 的冪表示，0h 表示沒有這項最大傳輸限制。例如最小頁 4096 bytes、MDTS=5，上限是 128 KiB，本例 32 KiB 的 SWS 在此範圍內。namespace 換成不同 User Data Format 後，SWS 可能改變；不要永久沿用先前格式的 byte 換算。用 NSID=FFFFFFFFh 查 Streams 參數時，無法統一表示的 namespace 欄位可為 0，這也不能直接當成某個 namespace 的最佳寫入大小。')],
 ('Figure 708 教大小的組成；Figure 712 提供 SWS／SGS 的欄位位置。NVM §5.13 補上 SWS 的 logical-block 單位，兩份定義要一起使用。',
  'Figure 708 explains size composition and Figure 712 supplies SWS/SGS. NVM §5.13 supplies the logical-block unit; interpret the definitions together.'), source=NVM)

unit('lifetime', ('觀察串流、結束使用與處理狀態變更', 'Observe streams and end their use'),
 '8.1.9.2.2.1, 8.1.9.3, 8.1.9.3.1.2, 8.1.9.3.2', '645-653',
 ('Get Status 回報目前開啟的編號。Release Identifier 結束一個編號的本次串流關聯，專用資源仍可保留；Release Resources 歸還 namespace 的專用配置。停用、Format、刪除、寫入保護與 reset 則各有不同的狀態影響。',
  'Get Status reports open identifiers. Release Identifier ends the current association of one identifier while exclusive capacity can remain allocated; Release Resources returns the namespace-exclusive allocation. Disablement, Format, deletion, write protection, and reset have distinct effects.'),
 ('NSA=3、開啟編號為 7 與 40 時，釋放 7 之後專用配置仍是 3，40 仍可繼續使用。之後再用 7 寫入，代表新的一條串流，不能假設接回之前已結束的那一條。',
  'With NSA=3 and identifiers 7 and 40 open, releasing 7 leaves the exclusive allocation at three and 40 usable. A later write with 7 begins a new stream rather than resuming the ended association.'),
 [('讀狀態時先分清數量與編號', 'Get Status 的 bytes 1:0 是 OSC，表示開啟數量；其後每個 2-byte 欄位是一個編號，依數值遞增。若 OSC=3，後續值是 7、40、1000，表示 3 條串流，不是編號 1、2、3。主機指定的 NUMD 也會限制實際傳回多少資料；只讀到前幾個編號時，不能把未取得的欄位當成 0，或宣稱已列出全部串流。'),
  ('對整個 subsystem 查詢，不等於列出所有專用串流', 'Get Status 使用 NSID=FFFFFFFFh 時，回覆的是使用非專用 subsystem 資源的開啟串流；不是把每個 namespace 的專用串流全部加進來。同一編號若在不同 namespace 使用，只回一次。因此這份列表沒有附上逐筆 NSID，不能靠它還原每個 namespace 的完整串流清單；需要 namespace 明細時，逐一查詢對象。'),
  ('釋放一個編號，與歸還配置分開操作', 'Release Identifier 用 Directive Send、DTYPE=01h、DOPER=01h，DSPEC 填要結束的編號；沒有資料傳輸。若使用專用資源，結束的追蹤資源仍保留給這個 namespace 使用；若用共用資源，就回到 subsystem 資源池。指定未開啟的編號不宜僅因此失敗，但 NSID=FFFFFFFFh 明確非法。Release Resources 則用 DOPER=02h，成功後 NSA=0；原本沒有專用配置時不做動作，也不能只因沒有配置就失敗。主機若要有明確的單一串流結束點，應使用 Release Identifier，不把 NSA=0 當成所有資料或編號均已清除的證據。'),
  ('停用或改變 namespace 時，觀察不同的清除對象', '停用 Streams 會釋放該主機在受影響 namespace 的所有串流資源與編號；Format NVM 會釋放受影響 namespace 的所有開啟編號，不能擅自把這句擴成一定歸還所有專用配置。刪除 namespace 或把 namespace 變成寫入保護時，則必須釋放其全部串流資源與編號。這些是狀態與資源生命週期，不能拿來推論媒體上的使用者資料已安全清除。'),
  ('reset 要一起看仍啟用的其他控制器', 'Streams 不宣告跨 Controller Level Reset 保留；reset 時通常會對該控制器停用。然而，若同一 Host Identifier 還有已啟用的控制器，對這些活動控制器所附加的 namespace，Directive 不會被停用。之後設定相同非零 Host Identifier，或啟用屬於該身分的控制器時，共享 namespace 的 Directive 狀態要與既有路徑一致。這條例外依賴實際的主機關聯與附加關係，不能只看「某一個控制器 reset」就把整個 subsystem 的 Streams 狀態清空。')],
 ('Figure 713 先讀 OSC 再讀排序的編號；釋放與 reset 的規則連回正文的生命週期比較。Figure 705 的 SDIRCLR=0 需連同多控制器例外一起判斷。',
  'In Figure 713, read OSC before the sorted identifiers. Connect release and reset rules to the lifecycle comparison. Interpret Figure 705’s SDIRCLR=0 with the multi-controller exception.'))
