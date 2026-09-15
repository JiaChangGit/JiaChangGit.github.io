"""Only diagrams that explain a relationship beyond the prose."""
from html import escape
from scripts.nvme_reader_visuals import diagram, box, arrow, steps
from scripts.nvme_directives_content import bi


def table(title, headers, rows, caption):
    return '<figure><figcaption><strong>'+escape(title)+'</strong></figcaption><div class="table-wrap"><table><thead><tr>'+''.join('<th scope="col">'+escape(t)+'</th>' for t in headers)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+escape(t)+'</td>' for t in row)+'</tr>' for row in rows)+'</tbody></table></div><figcaption>'+escape(caption)+'</figcaption></figure>'


def illustration(key, lang='zh'):
    if key == 'streams-model':
        return steps(bi('從準備到資料使用','From preparation to data use')[lang], bi(
          ['查 Directives／Streams 支援；先登記適用的非零 Host Identifier。',
           '透過 Identify Directive 啟用 Streams；確認狀態與參數。',
           '選擇專用或 subsystem 資源；需要專用容量時請求配置並讀實際授予數。',
           'Write 帶 Stream Identifier；第一筆使用未開啟編號的寫入會開啟串流。',
           'Get Status 看開啟編號；用 Release Identifier 結束分組，用 Release Resources 歸還專用配置。'],
          ['Check Directives/Streams support and register an appropriate nonzero Host Identifier.',
           'Enable Streams through the Identify Directive and inspect state and parameters.',
           'Use exclusive or subsystem resources; request and inspect a grant if exclusive capacity is needed.',
           'Issue Writes with Stream Identifiers; first use of an unopened identifier opens a stream.',
           'Observe open identifiers with Get Status; release an identifier to end its grouping or release resources to return the exclusive allocation.'])[lang],
          bi('Allocate Resources 是選擇專用容量的操作，不是每個使用 Streams 的主機都必須先配置。來源：Base §8.1.9.2–§8.1.9.3。',
             'Allocate Resources selects exclusive capacity; prior exclusive allocation is not required for every Streams user. Source: Base §§8.1.9.2–8.1.9.3.')[lang])
    if key == 'streams-enable':
        return diagram(bi('Enable 的外層操作與內層目標','Enable: outer operation and inner target')[lang],
          bi('外層 DTYPE=0 選 Identify；內層 DTYPE=1 才指要啟用的 Streams。圖塊寬度為閱讀調整，以標示的 bits 為準。來源：Base Figures 186、706。',
             'Outer DTYPE=0 selects Identify; inner DTYPE=1 targets Streams. Box widths aid reading; the bit labels define actual widths. Source: Base Figures 186/706.')[lang],[
          box(20,25,210,70,['CDW11', '00000001h']),
          box(250,25,230,70,['DTYPE[15:8] = 0','Identify'],'command'),
          box(500,25,240,70,['DOPER[7:0] = 1','Enable Directive'],'command'),
          box(20,150,210,70,['CDW12','00000101h']),
          box(250,150,230,70,['DTYPE[15:8] = 1','Streams'],'success'),
          box(500,150,240,70,['ENDIR[0] = 1',bi('啟用','Enable')[lang]],'success'),
          arrow(365,95,365,150)],250)
    if key == 'streams-resources':
        return diagram(bi('8 個資源：專用配置與共用池分開計算','Eight resources: exclusive capacity and the shared pool')[lang],
          bi('說明性快照：無其他專用配置。MSL=8，專用配置 NSA=3、其中 NSO=1；非專用池 NSSA=5、其中 NSSO=2。開啟數與池的總容量不是同一個計數。來源：Base Figure 712。',
             'Illustrative snapshot with no other exclusive allocation: MSL=8, NSA=3 with NSO=1, and NSSA=5 with NSSO=2. Open counts differ from pool capacities. Source: Base Figure 712.')[lang],[
          box(20,20,720,65,['MSL = 8']),
          box(20,130,280,80,['NSA = 3',bi('本例 namespace 專用','Namespace-exclusive')[lang]],'command'),
          box(320,130,420,80,['NSSA = 5',bi('未專用配置的 subsystem 池','Nonexclusive subsystem pool')[lang]]),
          arrow(160,85,160,130),arrow(530,85,530,130),
          box(20,250,280,65,['NSO = 1',bi('專用部分開啟 1 條','One stream open')[lang]],'success'),
          box(320,250,420,65,['NSSO = 2',bi('池中開啟 2 條','Two open in the pool')[lang]],'success')],345)
    if key == 'streams-sharing':
        return table(bi('固定同一 namespace、同一編號 7','Same namespace, same identifier 7')[lang],
          bi(['控制器路徑','非零 Host Identifier','SSID=0 的串流分組','SSID=1 的串流分組'],
             ['Controller path','Nonzero Host Identifier','Stream group: SSID=0','Stream group: SSID=1'])[lang],
          [['C1','A','A / 7','7'],['C2','A','A / 7','7'],['C3','B','B / 7','7'],['C4','C','C / 7','7']],
          bi('分組欄的 A / 7 是本表的身分對照寫法，不是命令編碼。SSID=0 有 3 組；SSID=1 有 1 組。此表的所有 Host Identifier 都非零。來源：Base Figure 710 的關係，改用編號 7 說明。',
             'A / 7 is a table label for identity and identifier, not a command encoding. SSID=0 gives three groups; SSID=1 gives one. All identities here are nonzero. Adapted relationship from Base Figure 710, illustrated with identifier 7.')[lang])
    if key == 'streams-sizes':
        items=[box(20,15,720,55,[bi('每個 logical block = 4096 bytes','Each logical block = 4096 bytes')[lang]])]
        for i in range(4):
            items.append(box(20+i*180,110,174,80,['SWS = 8 blocks','32 KiB'],'command'))
        items += [box(20,235,720,70,['SGS = 4 SWS = 32 blocks = 128 KiB'],'success'),
                  arrow(380,190,380,235)]
        return diagram(bi('SGS 乘上 SWS，再乘 block 大小','Multiply SGS by SWS, then by block size')[lang],
          bi('4 個 32 KiB 的 SWS 組成 128 KiB 的 granularity 單位；圖是大小組成，不是 4 筆命令的執行順序。來源：Base Figure 708／712、NVM §5.13。',
             'Four 32 KiB SWS units form one 128 KiB granularity unit. This is size composition, not the execution order of four commands. Source: Base Figures 708/712 and NVM §5.13.')[lang],items,335)
    if key == 'streams-lifetime':
        return table(bi('哪些操作結束編號，哪些操作歸還資源','Ending identifiers versus returning resources')[lang],
          bi(['事件或操作','編號／開啟狀態','專用配置','資料本身'],
             ['Event or operation','Identifier/open state','Exclusive allocation','User data'])[lang],
          bi([
           ['Release Identifier','結束指定編號的本次串流','保留給 namespace 重用','此操作不刪除資料'],
           ['Release Resources','不可只用 NSA=0 推論全部編號狀態','歸還，NSA 清 0','此操作不刪除資料'],
           ['停用 Streams','釋放受影響主機的所有編號','釋放其資源','停用不是安全清除'],
           ['Format NVM','釋放受影響 namespace 的開啟編號','不能從這條規則推論全部歸還','資料效果依 Format 操作'],
           ['刪除／變成寫入保護','釋放 namespace 的全部編號','釋放全部串流資源','不能把追蹤清除等同媒體清除']],
          [['Release Identifier','Ends this use of one identifier','Retained for namespace reuse','Does not delete data'],
           ['Release Resources','NSA=0 alone is not a complete identifier-state report','Returned; NSA becomes zero','Does not delete data'],
           ['Disable Streams','Releases affected host identifiers','Releases affected resources','Not secure erasure'],
           ['Format NVM','Releases affected open identifiers','Do not infer release of all capacity from this rule','Data effects follow Format'],
           ['Delete / become write-protected','Releases namespace stream identifiers','Releases all stream resources','Tracking release is not media erasure']])[lang],
          bi('Reset 另依「是否仍有同一主機的已啟用控制器」判斷，不能與停用操作合併。來源：Base §8.1.9.2.2.1、§8.1.9.3、§8.1.9.3.2。',
             'Reset additionally depends on enabled controllers associated with the same host; it is not interchangeable with explicit disablement. Source: Base §§8.1.9.2.2.1, 8.1.9.3, and 8.1.9.3.2.')[lang])
    return ''
