"""Tutorial diagrams show causal relationships, separate from overview posts."""
from html import escape
from scripts.nvme_reader_visuals import diagram, box, arrow


def route(points, label='', label_at=None):
    commands = 'M'+' L'.join(f'{x},{y}' for x,y in points)
    x,y = points[-1]; px,py = points[-2]
    if x > px: head = f'M{x-7},{y-5} L{x},{y} L{x-7},{y+5}'
    elif x < px: head = f'M{x+7},{y-5} L{x},{y} L{x+7},{y+5}'
    elif y > py: head = f'M{x-5},{y-7} L{x},{y} L{x+5},{y-7}'
    else: head = f'M{x-5},{y+7} L{x},{y} L{x+5},{y+7}'
    out = f'<path d="{commands}" class="v-line"/><path d="{head}" class="v-line"/>'
    if label:
        lx,ly = label_at
        out += f'<text x="{lx}" y="{ly}" text-anchor="middle" font-size="16">{escape(label)}</text>'
    return out


def course_illustration(key):
    if key.startswith('rrl-'):
        from scripts.nvme_rrl_visuals import illustration
        return illustration(key)
    if key.startswith('lockdown-'):
        from scripts.nvme_lockdown_visuals import illustration
        return illustration(key)
    if key.startswith('fdp-'):
        from scripts.nvme_fdp_visuals import illustration
        return illustration(key)
    if key.startswith('streams-'):
        from scripts.nvme_directives_visuals import illustration
        return illustration(key)
    if key.startswith('adminio-'):
        from scripts.nvme_admin_io_visuals import illustration
        return illustration(key)
    if key == 'apst-state-machine':
        return diagram('APST：閒置條件與 I/O 觸發的兩條路徑',
          '說明性情境：目前是 operational PS0，目標是已支援的 non-operational PS3；PS0 entry 設 ITPT=2000 ms、ITPS=3。APSTE 啟用且連續閒置超過門檻時轉入 PS3；有未完成 I/O 時不符合閒置定義。若進行中作業會使功率超過目標狀態宣告值，規格建議控制器不要自動轉入。新的 I/O 到達後，控制器返回最近的 operational state，本例是 PS0。箭頭代表事件與轉移，並非等比例時間。', [
          box(25,90,245,100,['PS0 · operational','可處理 I/O'],'success'),
          box(485,90,245,100,['PS3 · non-operational','先退出，才能處理 I/O']),
          route([(270,115),(380,115),(380,45),(607,45),(607,90)], 'APSTE=1；連續閒置 > 2000 ms',(380,25)),
          route([(485,165),(380,165),(380,250),(147,250),(147,190)], '新 I/O → 返回最近的 operational state',(380,283)),
          '<text x="380" y="330" text-anchor="middle" font-size="16">PS0 entry：(2000 &lt;&lt; 8) | (3 &lt;&lt; 3) = 0007D018h</text>'
          ],365)
    if key == 'power-state-mental-model':
        return diagram('功耗狀態轉移的時間如何計算',
          '說明性數值：PS0→PS3 的最大轉移時間是 EXLAT(PS0)+ENLAT(PS3)=0+100=100 μs；PS3→PS0 則是 500+0=500 μs。退出與進入取自不同狀態。圖中區塊寬度為排版用途，不代表時間比例；實際延遲以裝置的 Power State Descriptor 為準。', [
          box(20,40,150,75,['PS0','處理 I/O'],'success'),
          box(185,40,175,75,['退出 PS0','EXLAT = 0 μs'],'command'),
          box(375,40,195,75,['進入 PS3','ENLAT = 100 μs'],'decision'),
          box(585,40,155,75,['PS3','閒置']),
          route([(50,150),(710,150)],'進入省電狀態：最多 100 μs',(380,180)),
          box(20,230,150,75,['PS3','新 I/O 到達']),
          box(185,230,175,75,['退出 PS3','EXLAT = 500 μs'],'command'),
          box(375,230,195,75,['進入 PS0','ENLAT = 0 μs'],'decision'),
          box(585,230,155,75,['PS0','處理 I/O'],'success'),
          route([(50,340),(710,340)],'恢復處理：轉移最多 500 μs，另加命令處理時間',(380,373))
          ],410)
    if key == 'boot-protection':
        return diagram('Set Features 控制時的 Boot 寫入保護狀態',
          '這張圖只描述目前由 Set Features 控制、且允許使用圖中狀態的分割區。Write Unlocked 跨 Controller Level Reset 保留，但 power cycle 後回 Write Locked。Write Locked Until Power Cycle 的變更要求會被拒絕；power cycle 後回到 Write Locked，仍須明確解鎖才能更新。multi-domain 且跨控制器共享的分割區不得進入 until-power-cycle 狀態；RPMB 控制時改用另一套操作及保留規則。', [
          box(20,75,245,85,['Write Locked','禁止修改內容']),
          box(485,75,245,85,['Write Unlocked','允許依更新流程寫入'],'success'),
          route([(265,95),(485,95)],'Set：解鎖 001b',(375,75)),
          route([(485,140),(265,140)],'Set：鎖定 010b',(375,185)),
          box(240,300,290,100,['Write Locked Until','Power Cycle'],'decision'),
          route([(70,160),(70,350),(240,350)],'Set：011b',(130,280)),
          route([(530,350),(710,350),(710,230),(140,230),(140,160)],'power cycle → Write Locked',(440,252)),
          '<text x="385" y="440" text-anchor="middle" font-size="16">Until Power Cycle 中：一般 Set 變更 → Feature Not Changeable</text>'
          ],475)
    if key == 'boot-read':
        return diagram('讀取 Boot 資料時，來源與目的各有自己的座標',
          '說明性例子：BPSZ=2，每個分割區有 256 KiB；選 BP1、BPROF=1、BPRSZ=2，表示從 BP1 的 4 KiB 位置取 8 KiB。BMBBA 指向 4 KiB 對齊的主機接收位址；BRS=10b 才表示這條 Properties 路徑讀取成功。LID 15h 是另一條 Admin 路徑，含 16-byte header，不能沿用同一個 log offset 起點。', [
          box(20,55,270,120,['BP1 · 256 KiB','來源起點：1 × 4 KiB','本次長度：2 × 4 KiB']),
          box(470,55,270,120,['Host memory','目的：BMBBA << 12','接收空間至少 8 KiB'],'success'),
          arrow(290,115,470,115,'8 KiB'),
          box(140,245,480,70,['BRS：01b 讀取中 → 10b 成功','11b 錯誤：buffer 內容未定義'],'command')
          ],350)
    if key == 'selftest-command-state-machine':
        return diagram('Device Self-test 的命令與背景作業使用不同完成點',
          '命令成功回覆代表要求被接受，背景測試仍可能繼續。測試期間看 DSTOS／DSTCS；測試結束後再由結果紀錄判讀 DSTR 與有效旗標。時間軸只表示順序，不按持續時間比例繪製。', [
          box(20,35,200,75,['主機提出要求','STC + NSID'],'command'),
          box(280,35,200,75,['命令 CQE 成功','要求已接受'],'success'),
          box(540,35,200,75,['主機繼續查詢','Get Log Page']),
          arrow(220,72,280,72),arrow(480,72,540,72),
          box(280,190,230,100,['背景測試執行中','DSTOS：目前作業','DSTCS：完成百分比']),
          box(550,190,190,100,['測試已結束','RDS：歷史結果'],'decision'),
          route([(380,110),(380,190)]),arrow(510,240,550,240),
          '<text x="380" y="340" text-anchor="middle" font-size="17">命令完成 ≠ 測試通過；歷史結果 ≠ 目前進度</text>'
          ],375)
    if key == 'namespace-lifecycle':
        return diagram('Create 管物件，Attach／Detach 管連線',
          '說明性例子：Create 成功得到 NSID=7，再分別附加到控制器 3、5。只對控制器 3 Detach，移除的是左側存取關係，namespace 及控制器 5 的存取關係仍存在。Delete 才改變物件是否存在。', [
          box(45,30,230,75,['Controller 3']),box(485,30,230,75,['Controller 5']),
          box(220,240,320,100,['Namespace · NSID 7','容量、格式與儲存內容'],'success'),
          route([(160,105),(160,290),(220,290)],'Attach／Detach',(85,190)),
          route([(600,105),(600,290),(540,290)],'Attach／Detach',(675,190)),
          '<text x="380" y="390" text-anchor="middle" font-size="17">Create／Delete 改變底下的物件；Attach／Detach 改變連線</text>'
          ],425)
    return ''
