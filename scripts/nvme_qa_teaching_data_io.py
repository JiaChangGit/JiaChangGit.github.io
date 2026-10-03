"""Data-I/O supplement: evidence goals, a time sequence and decoded boundaries."""
from scripts.nvme_qa_model import pair

def extend(volumes,intros,aids,lessons):
    slug='data-io'
    volumes.append((slug,321,328,'資料 I/O：長度、持久性與完整性','Data I/O: size, persistence and integrity'))
    intros[slug]=pair('本冊補充原題庫尚未展開的資料 I/O 判讀：命令能不能接受、完成後保證什麼、資料內容如何驗證，以及失敗後可能留下哪些結果。先把四個問題分開，再用具體欄位值推導；既有 Feature、queue 與指標規則則連回原題。 || This supplement develops data-I/O reasoning not previously covered in depth: request validity, completion guarantees, content verification and partial failure effects. Derive answers from concrete field values while linking back to existing feature, queue and pointer lessons.')
    aids[slug]={
      'title':pair('先說清楚要證明哪件事，再選命令 || Choose the claim before choosing the command'),
      'takeaway':pair('可接受的命令、正確的內容、持久性與原子性，是四個不同判斷；一個 Success 不能代替全部證據。 || Request validity, content correctness, persistence and atomicity are separate claims; one success cannot prove all four.'),
      'headers':[pair(s) for s in ['要回答的問題 || Question to establish','需要一起看的資訊 || Evidence to combine','容易漏掉的條件 || Easily missed condition']],
      'rows':[[pair(c) for c in r] for r in [
       ['這筆資料範圍合法嗎？ || Is the request range valid?','MDTS、MPSMIN、NLB、NSZE、實際傳輸格式 || MDTS, MPSMIN, NLB, NSZE, transferred format','NLB 加1；metadata 是否計入 MDTS || NLB+1 and metadata accounting'],
       ['完成的寫入能否耐斷電？ || Is completed data persistent?','WCE、FUA、Flush 範圍與時間線 || WCE, FUA, Flush scope and timing','Flush 提交前，目標 Write 是否已完成 || Whether the Write completed before Flush submission'],
       ['中斷後能否只更新一部分？ || Can interruption leave a partial update?','有效原子單位、MAM、邊界與起訖 LBA || Effective atomic units, MAM, boundaries and LBAs','正常原子性與斷電原子性不同 || Normal and power-fail atomicity differ'],
       ['讀得到，是否就等於內容正確？ || Does readable mean correct?','Read、Compare、Verify 及 PI 檢查條件 || Read, Compare, Verify and PI conditions','Verify 沒有拿應用程式預期內容做比較 || Verify does not compare application expectations'],
       ['失敗後哪些資料可能已改？ || What changed before failure?','Copy.DW0、目的讀回、原始來源快照 || Copy DW0, destination readback, source snapshot','DW0=0 不是「完全沒寫入」的證明 || DW0=0 does not prove an untouched destination'],
      ]],
      'example':pair('教學假設先讓 Write A 成功，再提交同一 namespace 的 Flush。Flush 成功後，才有這條路徑提供的持久性保證。如果把兩個命令同時送出，即使 Flush 先成功，也不能宣稱尚未完成的 A 已被涵蓋。這個差別取決於時間關係，不是 CQE 的成功數量。 || In the example, Write A succeeds before Flush is submitted for the same namespace. Successful Flush then supplies the covered persistence guarantee. Submitting both concurrently does not let an earlier Flush success cover an unfinished A; timing, not success-counting, is decisive.'),
      'refs':['flushdata','iofields','atomicdata','verifydata','copydata'],
    }
    lessons[slug]=[
     ('先換成同一種單位，才比較大小','同樣寫著「大小」的欄位，可能是 bytes、logical blocks，也可能是指數或數量減1。假設 MDTS=5、MPSMIN=0，先算出131072 bytes；NLB=31則先換成32個區塊。接著才用目前格式計算每個區塊實際傳輸的 bytes，並依 MEM 與 metadata 配置決定 MDTS 如何計算。不能拿原始欄位值5與31直接比大小，也不能把 CC.MPS 當成 MDTS 的基準。'),
     ('用一條時間線分開持久性與順序','假設應用程式要求「資料A確定耐斷電後，才寫入指向A的索引B」。Host 必須先建立A的持久性，再提交B；只把A、Flush、B按順序放進同一SQ，並不等於已建立全部依賴。先等待A成功，再等待涵蓋A的Flush成功，是一條可明確判讀的路徑。若B本身也必須持久，B仍需要自己的持久性安排，前一筆Flush不會預先涵蓋未來的寫入。'),
     ('在 LBA 軸上畫邊界，就知道為何起點重要','教學假設原子邊界的解碼後大小是16個區塊，第一個邊界在LBA0。可以先把地址分成0～15、16～31兩段，再把Write的起點和終點放進去。14～15完全在第一段；15～16則各占一段。即使兩筆都是2個區塊，在Single Atomicity Mode中，後者仍可能失去namespace宣告的整筆2-block保證。單位大小與邊界要各檢查一次，不能只看長度。'),
     ('先準備能排除別種解釋的對照','若Verify成功卻讀到不是預期的內容，先確認是否只是寫進了合法但錯誤的資料；若PI沒有報錯，先確認PRACT或特殊tag是否讓那項檢查不會發生；若Read回DULBE，則先看區塊是否被解除配置。每個案例都要有原始命令、合法基準與一次只變更一個條件的對照。這樣結果不同時，才能知道差異是由哪項條件造成，而不是靠Status名稱猜原因。'),
    ]
