"""Chinese learning sequence and explanations, independent of the live PDF route."""
ORDER = ['command-map','identify','nvm-identify','format-list','queues','read','write','flush',
         'compare','verify','copy','dataset','zeroes','namespace','format','nvm-admin',
         'get-features','features','nvm-features','pcie-features','abort','aer','logs','nvm-logs',
         'selftest','firmware','boot','telemetry','sanitize','security']

INTRO = '作業系統要使用一顆 NVMe SSD，得先知道它有哪些儲存空間、每個區塊的格式、可以接受哪些命令，以及命令完成後究竟保證了什麼。這篇從一筆讀寫的需要開始，把查詢能力、準備佇列、傳輸資料和裝置維護接起來。先用具體情境建立全貌，再拆開欄位、時間順序與例外條件。'
BACKGROUND = ['以下的主機是發命令及提供記憶體的一方；controller 接收命令並管理裝置，namespace 是主機可定址的一份儲存空間。LBA 指出空間內的位置；一個 LBA 有多少 bytes，要由該 namespace 目前的格式決定。例子若使用 4096-byte LBA，會明確標示，不能把它當成所有 SSD 的固定值。',
              '閱讀時先看每節情境和算例，再用圖中的箭頭確認誰提供資料、誰改變狀態。要查精確欄位時，可以沿每節末尾的連結前往本文的圖表教學；相關欄位集中解釋，後面的圖只補自己的重點和案例。基本機制與必要條件都在本文說明，來源標示供核對使用。']
CONNECTIONS = ['用一筆「將 32 KiB 寫到指定位置」串起主軸：Identify 確認 4096-byte LBA 與長度上限；佇列承接 Write；SLBA 選位置，NLB=7 表示 8 blocks；DPTR 指向 32768 bytes。命令完成後，是否已能承受掉電，還要看 cache、FUA 與 Flush 的條件。這些欄位是同一件工作的不同部分。',
               '維護功能有自己的時間尺度。Create 產生 namespace，Attach 開通存取關係；Self-test、Telemetry 與 Sanitize 可能在命令回覆之後繼續工作。先分清「要求已處理」「背景作業進行中」「最終結果已產生」，才不會把所有成功 CQE 都解成工作已全部完成。']

# Replacements remove report narration and make omitted conditions explicit.
REPLACE = {
 'command-map': {2: ('能力與當前狀態是兩次判斷','Identify 回報支援某命令，只回答裝置有沒有實作它。Format 或 Sanitize 進行中，部分命令會受限制。Figure 144 的讀法是先選目前的作業狀態，再找要發出的命令列，最後讀該交叉位置的規則及註記。例如同樣要讀狀態，Get Log Page 與開始另一個媒體修改操作不是同一類要求；不能把「支援」當成任何時刻都允許執行。')},
 'firmware': {0: ('先下載，再選保存與啟用方式','Firmware Image Download 把映像分段送入控制器，Firmware Commit 才指定後續動作。一般 firmware 的 CA=0 替換 slot 但不安排啟用；CA=1 替換並安排在下次 Controller Level Reset 啟用；CA=2 以已存在的 slot 安排下次啟用；CA=3 要求支援的立即啟用。Boot Partition 另外用 CA=6 寫入、CA=7 選 active partition。先分清 firmware slot 和 Boot Partition，才知道 FS 與 BPID 哪一個欄位適用。'),
              1: ('保存成功、待啟用、正在執行是三個時點','FS 選擇 firmware slot；FS=0 讓控制器選 slot，非零值須是受支援的 slot。FRMW 回報 slot 數、slot 1 是否唯讀、是否支援不經 reset 啟用。即使映像已保存，若回覆要求 reset，當前執行版本仍不能只由保存結果推斷。LID 03h 的 CAFS 指目前 slot，NAFS 指下次啟用的 slot，FRS1–FRS7 則存各 slot 的 revision。')},
 'format': {0: ('格式化與建立空間是不同操作','namespace 已存在後，可以用 Format 改變它的資料格式和相關設定；Create 才是產生 namespace 的操作。Format 完成後不能再回傳受影響 namespace 原先的 user data，因此它會影響內容，不是替空間換個名稱。接下來先確認影響範圍，再選資料格式，這個順序可以避免只看 NSID 就低估影響。'),
            2: ('格式索引、metadata 和 PI 要互相相容','LBAFU 與 LBAFL 組成 Format Index=(LBAFU<<4)|LBAFL；延伸索引的可用性受 LBAFEE 的支援及主機宣告條件約束。MSET=0 選分離 metadata，MSET=1 選延伸 LBA；PI=0 停用保護資訊，1／2／3 選對應 PI 類型，PIL 選 metadata 內 PI 的位置。先由 Identify 的 MC、DPC、LBAF 確認傳輸方式、PI 類型和 metadata 大小都支援，再要求該組合。設定值不會替一個 MS=0 的格式憑空增加 metadata。Format 成功 CQE 表示格式化已完成，之後重新取得目前格式才能正確計算 I/O buffer。')},
 'logs': {2: ('把 SMART 的計數換成有意義的單位','Composite Temperature 以 Kelvin 編碼，300 K 約為 26.85 °C。Data Units Read／Written 採每單位 1000 個 512-byte units 的累計表示，數值向上取整；讀到 2 不是只傳了 2 個 LBA，也不是保證剛好 1,024,000 bytes。Host Read／Write Commands 是命令計數。相同的命令次數可以對應很不同的資料量；這些欄位也不是 NAND 實際寫入次數。'),
          3: ('清單變動與命令影響要轉成不同動作','LID 04h 列出自上次讀取後有變動的 attached namespace 資訊；它不是 active namespace 的完整清單。LID 05h 把 CSUPP 的支援能力與 LBCC、NCC、NIC、CCC 的內容或能力變化分開；知道執行某命令可能改變 namespace 能力，就要在成功後重新取得相關 Identify 資料。Self-test、Boot、Telemetry 和 Sanitize 的 Log 使用相同傳輸機制，但各自的有效狀態、長度與時間背景不同。')},
 'identify': {1: ('把 4096-byte 長表看成幾組可以回答的問題','Figure 338 可分為裝置身分、命令能力、資源限制、資料操作能力及電源狀態。VID／SN／MN／FR 辨識裝置；OACS／ONCS 告訴主機可用命令；MDTS 限制傳輸量；ACL／AERL 限制不同未完成要求的數量。FRMW／FWUG 用於 firmware，DSTO／EDSTT 用於 Self-test，SANICAP 用於 Sanitize，LPA 則協助判斷 Log 能力。這些欄位不是一串都要填入每筆命令的參數，而是執行相應工作前要取得的條件。'),
             3: ('Underlying Namespace List：索引選一段清單，NSID 識別其中的空間','CNS=1Dh 可查詢底層 namespace 對應。CNSSID 在這裡是起始 index，不是 NSID；每次最多回 12 筆。header 的 GENCTR 是清單版本，NUMENT 是有效項目數；每筆 320 bytes，包含底層 NSID 和 IDX。以 PCIe memory-based controller 的格式看，項目內的 CNTLID 欄位須為 0，主機忽略它，不能用它建立 controller 對應。假設有 15 筆，第一次 CNSSID=0 取得 indexes 0–11，第二次 CNSSID=12 取得 12–14；核對 GENCTR 未變，才把兩段當成同一版清單。'),
             4: ('Controller State Formats：數的是格式項目，不是目前版本','CNS=20h 回報可支援的控制器狀態資料格式，供保存或還原狀態時確認格式相容性。NV 是版本 entry 數，NUUID 是廠商 UUID entry 數；版本 entry 每筆 2 bytes，UUID entry 每筆 16 bytes。例如 NV=2、兩筆版本值為 1 和 3，意思是支援這 2 種格式，不是目前運行在「版本 2」。此清單的版本及 UUID 選擇索引從 1 起算；不要直接套用從 0 起算的 LBA Format Index。')},
 'security': {0: ('外層傳送完成，內層還有自己的結果','Security Send／Receive 是 NVMe 傳送安全協定訊息的外層。先用 CQE 判斷這筆 NVMe 傳输命令是否完成，再解讀所選協定的回覆。以驗證身分為例，成功取得一份回覆，內容仍可能表示驗證未通過；「收到回覆」與「驗證通過」是不同結果，不能只看外層成功。'),
             1: ('把選擇值和 buffer 容量分開','SECP 選安全協定，SPSP=(SPSP1<<8)|SPSP0 是 16-bit 協定專屬值。NSSF 只在 SECP=EAh 時使用：SPSP=0001h 選 RPMB 用途，0002h 選 CDP authentication 用途；其他 SECP 下 NSSF 保留。Send 的 TL 是送出的 byte 長度；Receive 的 AL 是接收端配置的 byte 長度，採 INC_512=0 的編碼。256-byte 請求與 512-byte 回覆空間可分別填 TL=256、AL=512，不使用 NUMD 的減 1 編碼。'),
             2: ('查詢支援協定，不需要先送一筆請求','SECP=00h 的 Receive 是列出支援安全協定的查詢，沒有對應的先前 Send。其他安全交換可能由一筆或多筆 Send 形成回覆，配對方式由所選協定定義；不能把全系統最後送出的 Send 一律當成這份回覆的來源。'),
             3: ('重設之後，先前待取的回覆可能已不存在','Security Receive 的待取資料可能不會跨 communication loss 或 Controller Level Reset 保留。例如 Send 已完成，主機尚未取回結果時發生 controller reset；恢復後不能保證 Receive 還能拿到先前那份資料。主機要依所選協定重新建立交換狀態，而不是沿用 reset 前的回覆假設。這是資料可能失效的具體時點。')},
 'queues': {2: ('Delete SQ 成功是舊命令的完成界線','Delete SQ 的成功 CQE 出現前，原 SQ 裡的命令可以各自回報成功或 Command Aborted due to SQ Deletion。Delete SQ 成功之後，控制器不得再為那條已刪除 SQ 的舊命令送出完成狀態；尚未有 CQE 的舊命令，都隱含以 Command Aborted due to SQ Deletion 結束。因此主機不能永遠等待那些命令各自再回一筆 CQE。'),
            3: ('用 3 筆命令追蹤明確完成與隱含完成','假設 SQ 3 有 CID 10、11、12，CID 10 已有成功 CQE；接著 Delete SQ 3 成功，而 11、12 沒有各自的 CQE。此時 10 保留原結果，11、12 視為因 SQ 刪除而中止。Delete SQ 完成後，主機才可釋放描述該 SQ 的 PRP List。若 SQ 4 仍引用 CQ 2，就還不能刪 CQ 2；CQ 暫時是空的，也不能取代「沒有任何 SQ 引用」的條件。')},
 'flush': {2: ('cache 狀態和 namespace 範圍都會改變判讀','指定 NSID 選一份 namespace；FFFFFFFFh 則須看 VWC.FB：11b 對該控制器 attached 的所有 namespaces 生效，10b 回 Invalid Namespace or Format，00b 的舊值行為未定義。若 volatile write cache 不存在或未啟用，Flush 沒有資料提交作用；沒有 Sanitize 進行時必須成功，Sanitize 進行時則允許成功，不能一律宣稱必定成功。這是完成狀態的條件，與 Flush 是否傳送 data buffer 無關。')},
 'dataset': {0: ('檔案刪除後，主機提供的是空間使用資訊','檔案系統知道某段舊資料不再需要，可以用 Dataset Management 的 AD 告知控制器可解除那些 LBA 的配置。控制器可以選擇對部分或全部範圍不採取解除配置動作；未解除部分的原資料不因此改變。這不是立即抹除 NAND 的保證。Sanitize 才另外定義清除舊 user data 的作業與完成狀態。'),
             1: ('一份清單有幾段，每段有多長，是兩個數','命令 NR 表示範圍描述子數減 1；每筆描述子長 16 bytes。描述子內 SLBA 是起點，LLB 是直接的 block count。2 筆描述子分別有 4 和 6 blocks，命令 NR=1、buffer 長 32 bytes，各 LLB 填 4、6。Read 的 NLB 則用 blocks−1；不能因兩者都在描述範圍，就抄同一個原始數字。'),
             2: ('AD、IDR、IDW 選擇用途，不改變範圍長度','CDW11 bit 2 的 AD 表示可解除配置；bit 1 的 IDW 表示主機預期範圍內部分資料被寫入時，其餘部分也會一起被寫；bit 0 的 IDR 表示主機預期部分資料被讀取時，其餘部分也會一起被讀。這是在描述未來存取的關係，不會因 IDR=1 就立即執行 Read。沿用前述 4+6 blocks 的例子，CDW11=1 提供整段讀取提示，=2 提供整段寫入提示，=4 要求解除配置；NR 和 LLB 都不變。'),
             3: ('Context Attributes 讓提示更具體','每筆描述子另有 Context Attributes。CASZE 指預期每次 Read／Write 的 block 數，0 表示未提供；WPREP 表示近期預期寫入，SWR／SRR 表示順序寫入／讀取。AL 描述延遲需求，AF 描述存取頻率。例如一段大型影音資料可帶順序讀取資訊，幫助控制器理解使用方式；這些提示仍不保證固定 NAND 位置或指定延遲。'),
             4: ('限制值和 NVMDSMSV 決定超量要求如何處理','DMRL 限每筆命令的範圍數，DMRSL 限單段處理量，DMSL 限總處理量；這 3 個值必須同為 0 或同為非零。NVMDSMSV=0 時，全零表示不支援 DSM；非零時，超過限制會以 Command Size Limit Exceeded 中止。NVMDSMSV=1 時，全零表示沒有回報這些上限；非零時規格建議處理界線內的屬性而不處理界線外部分，且不因此回 Command Size Limit Exceeded。接受屬性與實際依提示改變媒體配置仍是兩件事。'),
             5: ('解除配置後，讀回結果要看哪兩項設定','DULBE 啟用時，讀到 deallocated／unwritten block 可回 Deallocated or Unwritten Logical Block 錯誤。未啟用時再看 DLFEAT.DRB：001b 回零，010b 回 FFh，000b 可回零或 FFh，並在重新寫入前保持規格要求的一致行為。需要可靠取得零值時，不能只假設所有裝置的 DSM 都會留下相同內容。')},
 'nvm-admin': {0: ('同一筆 Format，先選資料排列','MSET 決定 data 與 metadata 是否放在一起傳輸。若每 LBA 為 4096-byte data、8-byte metadata，MSET=1 使用每筆 4104 bytes 的延伸 LBA；MSET=0 則讓 data 與 metadata 分開傳輸。8 blocks 的延伸 buffer 是 32832 bytes，分離時則是 32768-byte data 加 64-byte metadata。能力與格式允許哪種排列，須由 MC 與目前 LBAF 確認。')},
 'nvm-logs': {0: ('錯誤位置要同時有有效旗標和數值','Base 的 Error Information 結構先用 SQID、CID、status、NSID 區分命令和錯誤；NVM 的 User Data 補充讓部分錯誤指向 logical block。相關資訊有效時，Error Information 的 LBA 指失敗的最低 LBA；不能把無效欄位的零值當成 LBA 0 損壞。這個最低位置規則與 Self-test 的 Failing LBA 不同，後者是測試發現的失敗位置，未要求是最低位址。'),
              2: ('用兩次快照計算工作負載，不把累計當瞬間值','假設兩次 SMART 相隔 10 秒，Host Write Commands 相差 100，Data Units Written 相差 10。可以說這段時間新增約 100 筆命令和以 512,000 bytes 為單位的流量計數，但單位的向上取整會影響短區間精度。不要用單次累計值當作當下 IOPS，也不要把 Data Units Written 當成實體 NAND 寫入量。')},
 'nvm-identify': {3: ('把目前空間與支援格式分成不同查詢','CNS=09h／0Ah 的 Format Index 查詢，是問某個支援格式的能力，不是在查 NSID 9 或 10。已配置 namespace、active namespace、支援格式和容量粒度也有不同入口。Create 選用的是可支援格式與資源條件；Read／Write 使用的則是目標 namespace 現在真正啟用的格式。先問「正在用哪個」還是「能選哪些」，再選 CNS。')},
 'format-list': {0: ('同一個格式編號，要一路用到底','Format Index 指向支援格式中的一筆。從這筆資料取得 data 大小、metadata 大小和能力，才能把 Read、Write、Compare、Verify、Copy 的 buffer 與 PI 條件算在同一基礎上。若取 data 大小時用 index 2、取保護能力時卻用 index 3，即使兩個數值各自有效，組合也不一定是任何可用格式。')},
}

REPLACE.setdefault('aer',{})[3]=('把事件參數當成有型別的資料','電壓事件用 VSENT 選感測器，IVM 要配該感測器的 VOLSS 倍率才是 Volts；電力事件用 PMT 選量測類別，IPS 與 IPV 一起換成 Watts。Controller Data Queue 事件的 CDQID 則是佇列 ID，不是量測值。先從 AET／AEI 選到正確格式，再解 DW1；同一個 32-bit 數字不能跨事件直接比較。')
REPLACE.setdefault('get-features',{})[2]=('資料回在 CQE 還是主機 buffer，要看 Feature','Power Management 等小型屬性可放在 CQE DW0；APST 則有資料結構，需要 DPTR 指向 buffer。CDW14 的 UUID Index 另負責選擇相應的功能定義，不是 namespace ID。一般標準功能使用其規定的選擇值；不能看見 DPTR 有位址，就假設每個 Feature 都會回一整個 buffer。')
REPLACE.setdefault('pcie-features',{})[2]=('MR 說明這份記憶體是不是原來那一份','EHM 決定是否啟用 HMB；MR=1 表示回傳先前提供的主機記憶體及保留內容。控制器可利用仍有效的內容恢復使用，前提是主機確實保留原配置和內容。重新分配一塊同樣大小的空白記憶體，不符合「歸還原記憶體」的意思。')
REPLACE.setdefault('features',{})[0]=('按控制對象整理 Feature','命令資源類包括 Arbitration、Number of Queues 與 PCIe 中斷設定；電源與溫度類包括 Power Management、APST、Temperature Threshold、HCTM 與 Non-Operational Power State Config；其餘設定則控制 cache、事件、時間和命令集組合。Boot 保護與 Sanitize Config 各跟自己的作業一起學。這樣分類是為了找對要改的行為，不表示同一類 Feature 可以互相代替。')
REPLACE.setdefault('copy',{})[2]=('描述子格式決定來源是否可以在另一個 namespace','DESFMT=0／1 不含 SNSID，來源與目的使用命令同一個 NSID；=2／3 包含 SNSID，可選不同來源 namespace，但除了裝置支援，還需要主機啟用該格式。0／2 對應 16-bit Guard PI，1／3 對應 32-bit 或 64-bit Guard PI。格式相容性不是只比每 LBA 的 data bytes：PI 與 metadata 配置也要相容。來源無 PI、目的有 PI 時，PRINFOW.PRACT 必須要求產生所需 PI，不能直接當作兩端布局完全相同。')
REPLACE.setdefault('copy',{})[3]=('失敗回覆的 DW0 不是已完成 block 數','Copy 失敗時，CQE DW0 回傳最小編號的未成功來源範圍。假設 ranges 0、1、2、5 成功，3、4 未成功，DW0=3；不能因此推論 range 5 沒有執行。控制器也可能已處理部分未成功範圍。若完全沒有寫入目的 LBA，DW0 為 0；反過來只看到 DW0=0，仍不能排除第一段已部分寫入。')
REPLACE.setdefault('read',{})[2]=('先選欄位格式，再設定檢查選項','CDW10–11 合成 64-bit SLBA；CDW12 的 NLB 使用 blocks−1，PRINFO 選 PI 的 action 與檢查。CDW13 在 CETYPE=0 時不使用 Command Extension Value；CETYPE 非零時，低 16 bits 才按指定 extension 定義解讀。一般不使用 extension 的讀取將 CETYPE 設 0，保留欄位填 0；不能因低 16 bits 有空間就自行放入應用程式標籤。')
REPLACE['zeroes']={
 0:('Write Uncorrectable 是錯誤標記','Write Uncorrectable 以 SLBA／NLB 選範圍，標記後，後續讀取會遇到不可校正的資料錯誤。它不需要主機提供一份「錯誤資料」buffer；成功 Write 相應位置可清除這種標記。它與 Compare 發現內容不一致也不同：前者是主動標記，後者是檢查兩份內容。'),
 1:('Write Zeroes 可以要求範圍，也可以要求整個 namespace','一般 Write Zeroes 用 SLBA／NLB 選範圍，DEAC=1 另要求解除配置；NSZ=1 要求整個 namespace，必須同時 DEAC=1 且該 namespace 支援解除配置後 data 與非 PI metadata 回零。裝置另以 ONCS.NSZS 表示整體零值功能支援。支援且使用 NSZ 時，SLBA／NLB 被忽略；不支援時可能只處理原本範圍，所以主機還要讀完成資訊。'),
 2:('LBACZ 是一個結果旗標，不是長度','NSZ=1 且命令成功時，CQE DW0 bit 0 的 LBACZ=1 表示整個 namespace 已清為零，=0 只保證命令範圍。NSZ=0 成功則表示指定範圍已清為零。失敗時可能已有部分或全部清零，不能由失敗反推所有舊內容都保留。這裡沒有「LBACZ+1 個 blocks」的公式。'),
 3:('限制值要配合 NVMWZSV 和 DEAC','WZSL 與非零 WZDSL 分別對應一般和 DEAC=1 的大小限制；WZDSL=0 時使用 WZSL。NVMWZSV=0 的非零限制是硬性上限，超量回 Invalid Field in Command；NVMWZSV=1 時則是建議上限，超量可能延遲。NSZ=1 的整體零值要求不受這兩個範圍大小欄位限制。')}
REPLACE.setdefault('nvm-features',{})[0]=('NVM 的 IIELL 以特定 Read 工作量作為基準','Power Management 的 Idle I/O Exit Latency Limit 是閒置控制器恢復處理 I/O 的額外延遲限制。若延遲依命令種類或長度而變，NVM 用讀取 NPWG 所指 block 數的 Read 當基準。更大的 Read 或 Copy 可能超過這個限制；因此它不是所有 I/O 的總延遲保證，也不是工作負載 hint 的另一種寫法。')
REPLACE.setdefault('nvm-features',{})[2]=('DN=1 放棄正常原子單位，仍保留掉電原子單位','DN=0 時，控制器須遵守適用的 AWUN／NAWUN 和 AWUPF／NAWUPF；DN=1 時，主機表示不要求正常操作的 AWUN／NAWUN，只要求掉電的 AWUPF／NAWUPF。若有效正常單位為 8 blocks、掉電單位為 1 block，DN=1 就不能再用正常的 8-block 單位主張保證。FUA 或 Flush 不會恢復這個被放棄的要求。')

ADDITIONS = {
 'abort': [('用時間線決定 buffer 何時還在使用','在主機送出 Abort 與收到其 CQE 之間，原命令可能剛好正常完成，兩筆完成回覆也可能前後交錯。先以 SQID／CID 對回原命令，再看 IANP 與原命令結果。沒有 immediate abort 保證且原命令尚未結束時，不能將原 data buffer 交給新用途，否則新資料可能與舊命令的存取重疊。')],
 'aer': [('用一個狀態變化接上查詢流程','假設 namespace 的能力改變，控制器用 Notice 完成一筆 AER。主機由 DW0 找到事件種類與相應 Log，讀到變動的對象後，再重新 Identify 那些 namespaces。AER 負責告訴主機有變化，Log 協助找對象，Identify 提供更新後的能力；三份資料不是重複的同一份狀態。')],
 'get-features': [('把 SEL=0 和 SEL=3 放在同一個例子','以 Power Management 為例，SEL=0 回目前設定，PS 欄位才是電源狀態編號；SEL=3 回支援能力，DW0 bit 2 的 CHANG、bit 1 的 NSSPEC、bit 0 的 SVBL 要按能力解讀。即使兩次 DW0 都剛好為 1，前者與後者仍可能在回答完全不同的問題。')],
 'features': [('用一個 APST 轉移算出代價','假設目前在可處理 I/O 的 PS0，對應 APST entry 設 ITPT=2000 ms、ITPS=3，且 PS3 是支援的 non-operational state。閒置達到轉移條件時，裝置進入 PS3；新 I/O 到來時須先退出低功耗狀態，才能回到 operational state 處理工作。ENLAT／EXLAT 以 μs 表示進入和退出延遲，不能拿 ITPT 的 ms 原值直接相加。ITPT 控制何時開始轉移，EXLAT 則影響重新服務的等待。')],
 'pcie-features': [('停用 HMB 的 CQE 是回收記憶體前的界線','主機用 Set Features FID 0Dh、EHM=0 要求停用 HMB，不能在命令仍未完成時就覆寫或回收原記憶體。成功完成停用後，控制器不再存取先前提供的 HMB，主機才可重新利用。MR=1 表示提供先前那份記憶體及保留內容以便重用；新分配或已更動的內容不能冒充未變的舊 HMB。')],
 'read': [('把 SLBA、長度與 namespace 終點放在同一條軸上','若 NSZE=1000，有效 LBA 是 0–999。SLBA=996、NLB=3 讀 4 blocks，最後位置為 999；NLB=4 則需要到 1000，超出可定址範圍。這項檢查與 buffer 足不足是獨立條件：主機即使配置更多記憶體，也不能讓 namespace 多出一個 LBA。')],
 'write': [('持久保存和原子性可用兩個問題分開','FUA 的問題是「這筆 Write 完成時，資料是否已符合非揮發性提交要求」；原子性的問題是「失敗或掉電時，受保護範圍會不會只更新一部分」。例如只等到 Write 的一般完成，可能尚未取得持久保存保證；即使用 FUA，超過 atomic write 大小或跨越不允許的 boundary，也不會因而獲得更大的原子範圍。')],
 'compare': [('不要把一次比對當成之後內容不會改','假設 Compare 在 LBA 100 成功，另一條 SQ 的 Write 隨後更新 LBA 100。這兩筆結果可以同時成立：比對當時內容相同，之後內容被合法修改。Compare 沒有替範圍上鎖；若需要比對結果和後續更新不可被插入，還需要明確支援並使用對應的命令配對機制。')],
 'verify': [('一個實際的選擇題：要拿回資料，還是只需要檢查結果','備份程式要把檔案內容傳到另一台機器，必須用 Read 取得 bytes，Verify 成功不會給它檔案。若只是檢查一段範圍的儲存層可讀性與適用 PI，Verify 可省掉一般 data 傳回。若手上有一份應一致的內容，要查是否吻合，才是 Compare 的用途。')],
 'copy': [('目的位址隨前面來源的長度向後推進','第 1 段來源有 4 blocks，放到 SDLBA=1000 後會使用 1000–1003；第 2 段有 6 blocks，從 1004 接續放到 1009。命令 NR=1 代表 2 個來源描述子，不是 2 blocks；目的總長是每段實際 block 數的總和。主機 buffer 放的是這些描述子，不是 10 blocks 的 user data。')],
 'zeroes': [('錯誤標記的恢復與零值寫入是不同觀察','Write Uncorrectable 對範圍標記不可校正，後續讀取會遇到相應錯誤；之後成功 Write 該位置可移除這種狀態。Write Zeroes 的用途則是讓資料具有零值語意，且不要求主機提供整段零值 buffer。要比較兩者，應問後續讀取看到錯誤還是零值結果，而不是比較「是否有主機 payload」這一項共同特徵。')],
 'nvm-features': [('原子寫入單位也採數量編碼','AWUN／AWUPF 與 namespace 對應值用 block 數減 1 表示單位；例如有效 atomic unit 原值為 7，就是 8 blocks。先判斷使用 controller 還是 namespace 的能力，再檢查 boundary 與 DN 的設定。掉電使用的單位與正常操作單位可能不同；不能把 AWUN 的 8 blocks 直接當成 AWUPF 的保證。')],
}

def apply(courses):
    for key, updates in REPLACE.items():
        steps=list(courses['adminio-'+key]['steps'])
        for index, value in sorted(updates.items()):
            if index < len(steps): steps[index]=value
            else: steps.append(value)
        courses['adminio-'+key]['steps']=steps
    for key, steps in ADDITIONS.items():
        courses['adminio-'+key]['steps']=list(courses['adminio-'+key]['steps'])+steps
