"""Scope-specific field teaching for restored topics and formerly terse passages."""
def apply(examples, guides, nvm_examples, nvm_guides):
    from copy import deepcopy
    from scripts.nvme_field_guides_context import OVERRIDES
    from scripts.nvme_field_guides import GUIDES, MEMBERS
    def reuse(source,number,report=None):
        value=OVERRIDES.get((report,source,number)) or GUIDES[MEMBERS[(source,number)]]
        result=deepcopy(value);result['id']='adminio-'+result['id']
        return result
    def ex(n, takeaway, example):examples[n]={'takeaway':takeaway,'example':example}
    def field(numbers,key,title,relation,*rows):
        g=dict(id='adminio-'+key,title=title,relation=relation,rows=list(rows))
        for n in numbers:guides[n]=g

    ex(144,'同一命令在 Format、Sanitize 各作業狀態下，可能有不同執行限制。','先選 Format 欄或目前的 Sanitize 狀態欄，再找保留命令列及註記。支援該 opcode 只證明有這項能力，不保證目前狀態允許使用。')
    ex(176,'Self-test 的 NSID 分清控制器本身、指定 namespace 與目前可存取的全體。','NSID=0 只測 controller。一般 NSID 無效時回 Invalid Namespace or Format；NSID 處於 inactive 時則回 Invalid Field in Command。這是 ID 是否有效與目前存取狀態的差別。')
    ex(187,'CA 決定 firmware 或 Boot 映像的保存及啟用動作，FS 和 BPID 各有自己的對象。','CA=1 以 FS 指定 firmware slot 的替換及下次啟用；CA=6 以 BPID 指定要寫入的 Boot Partition。不能拿 slot 2 當成第三個 Boot Partition。')
    ex(356,'GENCTR、NUMENT 與起始 CNSSID 讓主機分批列舉同一版底層 namespace 清單。','15 筆項目可分 CNSSID=0 和 CNSSID=12 兩次取得，各回最多 12 筆；GENCTR 若改變，需重新取得一致版本，不能直接串接兩段。')
    ex(357,'每筆 320-byte entry 以 NSID 識別底層 namespace，以 IDX 標示清單索引。','在 PCIe memory-based controller 情境，CNTLID 欄位須為 0 且主機忽略。IDX=7 是清單第 8 筆，不是 NSID=7，也不是 byte offset 7。')
    ex(358,'NV 和 NUUID 分別決定 2-byte 版本項目與 16-byte UUID 項目的有效數量。','NV=2 且版本值是 1、3，代表兩種支援格式。版本資料佔 bytes 2–5，UUID 區從 (NV+1)×2=6 開始，不把 NV=2 解成目前格式版本 2。')
    ex(458,'AL 直接給 Security Receive 的 byte 配置長度，沒有 NUMD 的加 1 換算。','預留 512 bytes 時 AL=512；Get Log Page 要讀相同 bytes 才使用 NUMD=127。兩個命令的長度編碼不同。')
    ex(492,'NODRM 只在 NDI=1 且要求 NDAS=1 時，選擇拒絕或以警告模式處理。','NODRM=0 回 Invalid Field in Command；NODRM=1 處理清除，若成功則 SOS=100b，表示仍發生解除配置。NDI=0 時 NODRM 不影響行為。')
    ex(582,'Delete SQ 成功表示所有舊命令已明確或隱含完成，之後不再送出其完成狀態。','SQ 3 的 CID 10 已成功，11、12 尚無 CQE；Delete SQ 3 成功時，11、12 隱含以 Command Aborted due to SQ Deletion 結束，不要再等它們各自回 CQE。')

    # Split the overloaded Identify guide: the list and its entry share one lesson,
    # while controller-state formats have a different count/layout rule.
    guides[342]['rows']=[r for r in guides[342]['rows'] if not r[0].startswith(('GENCTR','NV／NUUID'))]
    field([356,357],'underlying','用清單版本、起始索引與固定 entry 大小分段讀取',
      '先用 CNSSID 選要從第幾筆開始，再用 GENCTR 確認版本，最後按 NUMENT 讀有效 entry；PCIe 不使用的識別欄位不能硬解成連接關係。',
      ('CNSSID／GENCTR bytes 7:0','CNSSID 是從 0 起算的開始索引；GENCTR 隨清單變動遞增，相關 subsystem reset 後清 0，也可能計數回繞。','第一批 CNSSID=0，第二批 CNSSID=12；兩次 GENCTR 不同時重新取得。'),
      ('NUMENT bytes 15:8／最多 12 entries','NUMENT 表示本次回覆有效筆數，每筆 320 bytes；第一筆在 bytes 16–335，第二筆 336–655。','NUMENT=3 只解讀 3 筆，不把 4096-byte buffer 尾端當成更多空間。'),
      ('entry 的 NSID bytes 259:256／IDX bytes 319:318','NSID 辨識底層 namespace；IDX 是其在可回報清單中的索引。','IDX=7、NSID=3 可以同時成立：第 8 個項目記錄 ID 為 3 的空間。'),
      ('entry 的 CNTLID bytes 261:260／PCIe 條件','對本篇 PCIe memory-based controller，CNTLID 必須為 0，主機忽略；entry 前 256 bytes 也不作本情境的識別依據。','不能以一個必須忽略的 0，推論底層 namespace 連到 controller 0。'),
      ('Reserved bytes 317:262','這段不是下一筆 entry，也不是可自行填入的附加索引；完整 entry 長度仍是 320 bytes。','下一筆從目前 entry 起點+320 開始，不從 NSID 欄位結束處直接接著讀。'))
    field([358],'state-formats','先算兩種項目各有幾筆，再找 UUID 區起點',
      '支援的狀態格式清單是相容性資訊。數量、格式值、選擇索引和 byte 位置各自有不同作用。',
      ('NV byte 0／NUUID byte 1','兩個直接計數分別表示版本 entry 和廠商格式 UUID entry 數；0 表示該類沒有項目。','NV=2、NUUID=1 是 2 個版本項目和 1 個 UUID，不是 3 個版本。'),
      ('Version entries／UUID entries','版本 entry 每筆 2 bytes，從 byte 2 開始；UUID 每筆 16 bytes，從 (NV+1)×2 開始。','NV=2 時，版本佔 bytes 2–5，第一個 UUID 佔 bytes 6–21。'),
      ('格式值／選擇索引','版本與 UUID 選擇索引從 1 起算；entry 保存的格式值不等於該 entry 的索引。','第 2 筆版本 entry 可保存值 3，表示索引 2 選到格式版本 3。'))

    for n in [312,451,452,453,492]:guides[n]=reuse('base',n,'base-sanitize')
    guides[451]['relation']='SANACT 先決定方法或控制動作，再判斷各選項是否適用；Sanitize Status 把要求與背景作業結果接起來。'
    # Explicitly state the conflict rather than defer to a capability table.
    guides[312]['rows'][0]=('SSTAT.SOS／SPROG','SOS=000b 尚未開始，001b 成功，010b 作業進行中，011b 失敗，100b 成功但發生非預期解除配置。作業進行中才按有效條件換算 SPROG×100/65536%。','SPROG=32768 約為 50%；SOS=010b 也可能涵蓋 Media Verification 或 Post-Verification Deallocation，須配合 SSI 確認目前階段。')
    guides[542]=reuse('base',542,'base-boot-partitions')
    # RPMB packet formats belong to a separate prerequisite; FID85 only needs the
    # control mechanism and reset policy, not an unexplained packet-field inventory.
    guides[542]['rows']=[r for r in guides[542]['rows'] if not r[0].startswith('Request/Response')]
    for n in [176,177,178,179,180,218,219,279,280,442,443,444,445,446,447,448,449,450]:
        guides[n]=reuse('base',n)
    # Namespace command structures retain a shared home, but the referenced NVM
    # payload has its own detailed table below.
    guides[442]['rows'][1]=('Create buffer／CSI／4096 bytes','Base Figure 448 是共同布局；CSI=0 的 NVM 定義更具體，以 Figure 134 指定 Host Specified Fields，並將 bytes 512–767 用作 Placement Handle List。不能把這段仍一律當成 Base 表的保留區。','NSZE／NCAP 描述 block 數，FLBAS 決定每 block 大小；整份 Create buffer 不保存那些 blocks 的 user data。')
    for n in [442,443,444,445,446,447,448,449,450]:guides[n]=guides[442]
    nvm_guides[134]=reuse('nvm',134,'base-namespace-management')
    ex(448,'Create buffer 的實際欄位由 CSI 所選的命令集補充，不能只按 Base 共同布局解讀。','NVM 的 Figure 134 以 bytes 512–767 定義 Placement Handle List；它對這段給出更具體的規則，所以不是將 Base 的 Reserved 原樣套上。')

    field([220,221,222,223],'telemetry','用建立選項、累積範圍與紀錄版本取回同一次 Telemetry',
      'Host-Initiated 和 Controller-Initiated 資料各有來源。共同的 512-byte block 編號只負責定位；generation、可用旗標和 scope 決定這些 bytes 屬於哪份紀錄。',
      ('LID 07h／08h／LPI','07h 讀主機發起資料，08h 讀控制器發起資料；header 的 Log Identifier 對應這份紀錄種類。','LID 相同只能證明種類相同，還須看 generation 才能追蹤擷取版本。'),
      ('CTHID／MCDA／MCDAS','CTHID=1 要求建立；MCDAS 回報支援 Maximum Created Data Area 選擇，MCDA 在受支援時選建立到哪個 Area。','第一筆建立用 CTHID=1，後續讀同一份資料用 0；不能每段都重新建立。'),
      ('THDA1LB–THDA4LB／TCDA1LB–TCDA4LB','Last Block 是含終點的 block 編號；各 Area 都從 block 1 開始，較大 Area 包含前面的範圍。','Area 1 Last Block=65 有 33280 bytes data；加 header 為 33792 bytes，Area 2 的新增部分才從 block 66 起。'),
      ('THDGN／TCDGN／TCDA','前兩者辨認主機／控制器資料的擷取版本；TCDA 表示控制器資料可用，清除後不可假設先前紀錄仍待取。','分段前後 generation 由 7 變 8 時，不拼接現有片段；RAE=1 可在讀取期間保留相關事件。'),
      ('THS／TCS／RID／IEEE OUI','scope 描述此份資料涵蓋的範圍；Reason Identifier 與廠商識別資料協助解讀來源和原因，payload 可採廠商格式。','知道 Last Block=65 能算資料量，但無法從這個數字推導廠商診斷內容。'),
      ('LPA／ETDAS／Area 4','LPA 的 Telemetry Data Area 4 支援能力與主機 Host Behavior Support 的 ETDAS 宣告須一起成立，才可使用延伸 Area 4。','固定 header 中存在 DA4 Last Block 欄位，不代表每台裝置或每次主機配置都能取 Area 4。'),
      ('LPO／NUMD／512-byte blocks','採 byte offset 時，block n 起點是 n×512；傳 n 個 blocks 的 Get Log Page 長度為 NUMD=n×128−1。','從 block 66 讀 2 blocks：LPO=33792、NUMD=255；不是 LPO=66。'))

    # Extend existing tables at their single teaching home.
    guides[338]['relation']='同一個 4096-byte 結構包含多種能力，按要完成的工作分組看；能力和當前設定分開，保留欄位不當成支援證據。'
    guides[338]['rows'] += [
      ('OACS.Device Self-test／DSTO.SDSO／EDSTT','OACS 表支援；SDSO=0 是每 controller 同時 1 個作業，=1 是整個 subsystem 同時 1 個；EDSTT 是 extended test 估計分鐘數。','同一 subsystem 的兩個 controllers 能否各測一次，要看 SDSO，不是只看有兩條 Admin SQ。'),
      ('SANICAP／NDI／NODMMAS／SPRRS','SANICAP 分別回報各清除方法、禁止 no-deallocate 的條件、媒體是否可能受修改，以及 Purge 要求支援。','支援 Crypto Erase 不表示也支援 Overwrite；NDI=1、NDAS=1 還需配 NODRM 決定拒絕或警告。')]
    guides[571]['rows'][4]=('Delete SQ 完成／Delete CQ 前提','Delete SQ 成功時，尚無各自 CQE 的舊命令隱含以 Command Aborted due to SQ Deletion 結束；之後不再送出那些命令的完成狀態。所有引用 SQ 移除後才可刪 CQ。','SQ 3 中 CID 10 已成功、11 未回，Delete SQ 成功保留 10 的結果並使 11 隱含中止；不等待 11 再回一筆。')
    guides[456]['rows'] += [('Receive 回覆的保留時間','先前 Send 所產生的資料可能無法跨 communication loss 或 Controller Level Reset 保留。','Send 後、Receive 前發生 reset，不能假設先前回覆仍存在；重新依選定協定建立交換狀態。')]
    nvm_guides[132]['relation']='Namespace Granularity List 提供建立 namespace 時的大小與容量建議粒度；格式索引、byte 粒度與實際 block 數需要一起換算。'

    def nf(numbers,key,title,relation,*rows):
        g=dict(id='adminio-nvm-'+key,title=title,relation=relation,rows=list(rows))
        for n in numbers:nvm_guides[n]=g
    nf([44,45,46,47,48],'dsm','先算清單與範圍，再解讀每個提示位元',
      '命令 flags 套用到提供的範圍，Context Attributes 描述每段的使用方式。數量、位置和提示分開解讀，才能理解控制器實際收到了什麼。',
      ('DPTR／NR bits 7:0','DPTR 指向範圍描述子；NR 是描述子數減 1，每筆 16 bytes。','2 筆描述子：NR=1，payload=32 bytes；與每段 LLB 無關。'),
      ('AD bit 2／IDW bit 1／IDR bit 0','AD 要求可解除配置；IDW 預期範圍內部分被寫時其餘也會一起被寫；IDR 對讀取有相同整段關係。','CDW11=1 是整段讀提示，=2 是整段寫提示，=4 是解除配置要求；不是傳 1、2、4 blocks。'),
      ('CATTR bytes 3:0／LLB bytes 7:4／SLBA bytes 15:8','這些位置相對每筆描述子起點；LLB 是直接 block 數，SLBA 是起點。','第二筆的 LLB 在 payload bytes 20–23；SLBA=200、LLB=8 表示 200–207。'),
      ('CASZE bits 31:24／WPREP bit 10','CASZE 是預期每筆 Read／Write 的 block 數，0 表示未提供；WPREP 表示近期預期會寫入。','CASZE=8 不會替實際 LLB=100 的描述子改成只有 8 blocks。'),
      ('SWR bit 9／SRR bit 8','分別提示順序寫與順序讀，描述使用模式，不是命令完成旗標。','SRR=1 不會把範圍內容立即送到主機。'),
      ('AL bits 5:4','0 無資訊，1 允許較長的 idle latency，2 一般延遲，3 低延遲需求。','AL=3 是需求描述，不能解成 3 μs 保證。'),
      ('AF bits 3:0','0 無資訊，1 典型，2 少讀少寫，3 常讀少寫，4 少讀常寫，5 常讀常寫；6–F 保留。','唯讀查詢居多的資料可用 3 表達頻率；它不會把範圍設為唯讀。'),
      ('DMRL／DMRSL／DMSL／NVMDSMSV','分別限定 range number、範圍內 block offset 與累計 block offset；NVMDSMSV 區分硬性限制和可分段處理的支援行為。','NVMDSMSV=0 且非零限制被超過，回 Command Size Limit Exceeded；=1 不因該限制回這個錯誤。'))
    nf([81,82,83,84,85,86,87,88],'zeroes','把範圍零值、整體零值與回覆旗標配在一起',
      'Write Zeroes 不傳一般的 data payload；範圍、PI 生成和是否解除配置由命令選項決定。回覆的 LBACZ 是判斷整體效果的旗標。',
      ('SLBA／NLB／NSZ／NSZS','一般使用 SLBA 和 NLB+1；支援 NSZS 且 NSZ=1 時改為整個 namespace，控制器忽略原範圍欄位。','未支援 NSZS 時可能只處理原 SLBA／NLB 範圍，不能只因送出 NSZ=1 就宣稱整體清零。'),
      ('DEAC bit 25／NSZ bit 23／DLFEAT','NSZ=1 須同時 DEAC=1，且支援 deallocated data 與非 PI metadata 回零；否則回 Invalid Field in Command。','NSZ=1、DEAC=0 是無效要求；一般範圍清零不一定要求 DEAC。'),
      ('LR／FUA／PRINFO／STC','LR 控制重試努力程度；FUA 要求非揮發性提交後完成。Write Zeroes 的 PRCHK 必須為 000b，STC 必須清 0。','不把一般 Read 的 PRCHK 檢查位元整組複製到 Write Zeroes。'),
      ('CETYPE／CEV／DTYPE／DSPEC','CETYPE 選 command extension；DTYPE 選 directive，DSPEC 的含義由該 directive 決定。CETYPE=0 時 CDW13 低 16 bits 為保留。','未使用延伸功能時不能把低 16 bits 當成自訂工作編號。'),
      ('LBTU／LBTL／LBAT／LBATM','tag 欄位配合所選 PI 格式；未格式化使用 PI 時控制器忽略這些 tag。','LBTU 與 LBTL 合成 tag bits，不是額外的目的 LBA 起點。'),
      ('LBACZ／Successful Completion','NSZ=1 且成功時，LBACZ=1 表示整個 namespace，=0 表示命令範圍；失敗則可能已有部分或全部處理。','LBACZ=1 是布林結果，不表示只清 1 個 block。'),
      ('WZSL／WZDSL／NVMWZSV','依 DEAC 選非零 WZDSL 或 WZSL；NVMWZSV=0 的上限是硬性限制，=1 則是建議。NSZ=1 不適用這兩個範圍上限。','相同大小在兩種 variant 下可分別是必須拒絕或可能延遲，不能只比較長度。'))
    nvm_examples[88]={'takeaway':'NSZ=1 的成功回覆以 LBACZ 區分整個 namespace 與原本指定範圍。','example':'LBACZ=1 表示全部 logical blocks 已清為零；LBACZ=0 只保證命令範圍。這是旗標，沒有加 1 換成 block 數的規則。'}
    nvm_guides[98]['rows'][0]=('DN／AWUN／NAWUN','DN=0 須遵守適用的正常與掉電原子單位；DN=1 不要求 AWUN／NAWUN，仍須遵守 AWUPF／NAWUPF。','正常單位 8 blocks、掉電單位 1 block 時，DN=1 不能再主張正常 8-block 保證。')
    nvm_examples[90]={'takeaway':'NVM Notice 補充 namespace 屬性變化、LBA 狀態及 rate limit 變動；一般使用量變動不一定觸發通知。','example':'NUSE 頻繁增加時，控制器不得只因這項改變就送 Attached 或 Allocated Namespace Attribute Changed Notice；不能每次看到寫入就預期一筆 AER。'}
    nf([90],'nvm-notices','先選 Notice，再讀命令集所定義的事件資訊',
      '這些值屬 Base AER 的 Notice 分支；事件資訊不是一般 I/O 的 status，也不等於查詢所得的完整狀態。',
      ('AEI=00h／09h','分別是 Attached／Allocated Namespace Attribute Changed；NUSE 改變，以及 ANA 狀態變化造成的 NUSE／NVMCAP 改變，不得據此送這兩種事件。','資料寫入導致使用量增加，不表示一定有 namespace 屬性變更通知。'),
      ('AEI=05h','LBA Status Information Alert 表示已符合潛在不可恢復 LBA 的通知條件；相關紀錄提供後續定位資訊。','事件值 05h 不是第 5 個 LBA 壞掉；取得相應 Log 且 RAE=0 才按該事件規則清除。'),
      ('AEI=0Ah','Rate Limiting Configuration Change 表示配置變更影響回報的 rate limits；讀事件指定的 Log 且 RAE=0 以確認。','收到通知時要重新取得限制資訊，不能把 0Ah 當成新的速度值。'))

    nf(list(range(32,43)),'copy','用來源描述子、目的連續範圍與保護條件讀懂 Copy',
      '命令給目的位置，每筆描述子給來源；資料不經主機 buffer 往返，但來源、目的和 PI 格式仍須相容。Fast Copy 和原子性另有各自條件。',
      ('DESFMT／NR／DPTR','NR 是來源描述子數減 1；DESFMT=0／2 用 32-byte entry，1／3 用 40-byte entry。DPTR 指這份清單。','2 個 Format 0 entries：NR=1、payload=64 bytes；不是 2 blocks 的 user data。'),
      ('DESFMT／SNSID／PI 格式','0／1 不含 SNSID、來源與目的同 namespace；2／3 含 SNSID，另須主機啟用。0／2 對應 16-bit Guard，1／3 對應 32-bit 或 64-bit Guard。','裝置支援 Format 2，但主機未啟用時，選 DESFMT=2 仍會回 Invalid Field in Command。'),
      ('SLBA／NLB／SDLBA','每段 NLB+1 是實際 block 數；目的從 SDLBA 起依來源清單順序連續安排。','4 和 6 blocks、SDLBA=1000：目的先 1000–1003，再 1004–1009。'),
      ('MSSRL／MCL／MSRC','MSSRL 限單段來源的直接 block 數；MCL 限總 block 數；MSRC 是來源範圍數減 1 的上限。','每段都小於 MSSRL，總和仍可能超過 MCL；NR 也須不超 MSRC。'),
      ('FCO／NVMAFC／DNR','FCO=1 要求該來源使用 fast copy；無法使用時回 Fast Copy Not Possible。DNR=0 允許重試，=1 表示主機不應重試同一要求。NVMAFC 表示 subsystem 內所有 Copy 都屬 fast copy。','Fast copy 指預期不比主機 Read+Write 慢的方法；即使採用該方法，並行負載或錯誤仍可能使某次實際耗時較長。'),
      ('PRINFOR／PRINFOW／PRACT','讀、寫部分分別設定 PI。Format 0／1 且有 PI 時，兩邊 PRACT 必須相同；無 PI 時控制器忽略這兩個 PRINFO 欄位。','同 namespace、PRACT 一邊 0 一邊 1，回 Invalid Field in Command，不能把它當成任意 PI 轉換。'),
      ('跨 namespace 的 data／metadata／PI 相容性','data block 大小必須相同；metadata 大小一般也相同，只有全部 metadata 都是 PI 且進行 PI 插入或移除時才有對應例外。','4096-byte data 的來源不能直接 Copy 到 512-byte data 的目的；不是只把 block 數乘 8 就變成有效格式。'),
      ('STCR／STCW／LBST／ILBRT／EILBRT／LBAT／LBATM','來源檢查與目的產生的 tag 分開；STCR 受 STCRS 支援限制，LBTU／LBTL 組合可變寬度 tag。','移到新的 SDLBA 時，不能把來源 reference tag 原值一律當成目的 reference tag；先依 PI 型別和 PRACT 決定處理。'),
      ('LR／FUA／CETYPE／CEV／DTYPE／DSPEC','LR 與 FUA 用於寫入部分；FUA 要求目的 data 及 metadata 提交非揮發性媒體後完成。其餘選擇值分別指定 command extension 或 directive。','FUA=1 仍不替另一條 SQ 的命令建立先後次序；未用的保留欄位不填自訂資訊。'),
      ('NVMCSA／原子單位和邊界','NVMCSA=1 把 Copy 的寫入部分當成單一 Write 套用原子規則；不是保證任何長度整筆不可分割。FFFFh 原子單位仍只表示 65536 blocks。','總目的長度 12 blocks、有效原子大小 8 blocks 且從邊界開始時，可能分成 8 和 4 的原子操作；來源描述子的分段不是原子邊界。'),
      ('失敗 CQE DW0／部分完成','DW0 是最小編號的未成功來源範圍；其後的來源可能已部分或全部複製。','ranges 0、1、2、5 成功而 3、4 未成功，DW0=3；不能推論 range 5 沒有寫入。'))
