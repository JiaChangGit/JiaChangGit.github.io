"""Editorial organization shared by the three reader editions.

Source locators stay in the canonical claims. Development-only records are
excluded from the teaching claim set, rather than disguised as technical prose.
"""


def b(zh, en):
    return {'zh': zh, 'en': en}


def apply(reports, modules, headings):
    def module(rid, mid, **fields):
        next(m for m in modules[rid] if m['id'] == mid).update(fields)

    def claim(rid, key, zh, en):
        next(c for c in reports[rid]['claims'] if c['key'] == key).update(zh_tw=zh, en=en)

    def remove_claims(rid, keys):
        ids = {reports[rid]['prefix'] + '-' + key for key in keys}
        reports[rid]['claims'][:] = [c for c in reports[rid]['claims'] if c['key'] not in keys]
        for m in modules[rid]:
            m['sources'] = [s for s in m['sources'] if s not in ids]

    # These were authoring / trace collection instructions, not NVMe mechanisms.
    remove_claims('base-self-test-hmb-emulation', {'SELFTEST-DEBUG', 'DOORBELL-DEBUG', 'BOUNDARY-DEBUG'})
    remove_claims('base-self-test-namespace-management', {'END-TO-END-DEBUG'})
    remove_claims('base-boot-telemetry-sanitize', {'SOURCE-XREF'})
    for rid, mid in [('base-power-features','end-to-end-debug'),
                     ('base-self-test-namespace-management','namespace-end-to-end-debug')]:
        old = next(m for m in modules[rid] if m['id'] == mid)
        retained = [m for m in modules[rid] if m is not old]
        assigned = {s for m in retained for s in m['sources']}
        retained[-1]['sources'] += [s for s in old['sources'] if s not in assigned]
        modules[rid][:] = retained

    claim('base-power-features', 'GET-STATUS',
          'Get Features 指定不適用的 Controller Identifier 時，command-specific status 1Fh 表示 Invalid Controller Identifier；狀態碼需連同 SCT 解讀。',
          'For an inapplicable Controller Identifier, Get Features reports command-specific status 1Fh, Invalid Controller Identifier; interpret the status code together with SCT.')
    claim('base-self-test-namespace-management', 'COMMAND-STATUS',
          'Namespace Attachment 與 Management 有各自的 command-specific status。Attachment 包括 already attached 18h、private 19h、not attached 1Ah、Controller List invalid 1Ch、ANA attach failed 25h、limit 27h、I/O Command Set 29h／2Ah；Management 包括 Invalid Format 0Ah、insufficient capacity 15h、NSID unavailable 16h、thin provisioning unsupported 1Bh、ANA group invalid 24h。',
          'Namespace Attachment and Management have distinct command-specific statuses. Attachment includes already attached 18h, private 19h, not attached 1Ah, Controller List invalid 1Ch, ANA attach failed 25h, limit 27h, and I/O Command Set 29h/2Ah. Management includes Invalid Format 0Ah, insufficient capacity 15h, NSID unavailable 16h, thin provisioning unsupported 1Bh, and ANA group invalid 24h.')
    claim('base-ch4', 'LISTS',
          'Controller List 先以 NUMCIDS 指定數量，再依遞增順序排列最多 2047 個 16-bit controller identifiers。Namespace List 沒有數量 header，直接依遞增順序排列 32-bit NSIDs；兩種清單未使用的 entries 都填 0。',
          'A Controller List starts with NUMCIDS and then up to 2047 ascending 16-bit controller identifiers. A Namespace List has no count header and directly lists ascending 32-bit NSIDs. Unused entries in both lists are zero filled.')
    c = next(c for c in reports['base-boot-telemetry-sanitize']['claims'] if c['key']=='SAN-NAMESPACE')
    c['zh_tw'] = c['zh_tw'].replace('被主範圍引用的 Figure 454 定義 namespace 命令：','Namespace Sanitize 的命令格式如下：')
    c['en'] = c['en'].replace('Figure 454, referenced by the main scope, defines the namespace command:', 'The Namespace Sanitize command has the following layout:')
    c = next(c for c in reports['base-boot-telemetry-sanitize']['claims'] if c['key']=='TEL-EVENT')
    c['zh_tw'] = c['zh_tw'].split('8.1.30 指向')[0].strip()
    c['en'] = c['en'].split('The .1.5 reference')[0].strip()

    r = 'nvm-command-set-1.3'
    reports[r]['title_zh'] = 'NVM Command Set 1.3：邏輯區塊、I/O 命令與資料保護'
    reports[r]['title_en'] = 'NVM Command Set 1.3: Logical blocks, I/O commands, and data protection'
    module(r,'nvmcs-foundation',title=b('Logical block、格式與單位','Logical blocks, formats, and units'),
           lead=b('Host 透過 logical block address 存取 namespace。先確定一個 block 的 data 與 metadata 大小，才能計算 buffer、理解命令範圍，並選擇適用的資料保護方式。','The host addresses namespace storage through logical block addresses. Establish data and metadata sizes before calculating buffers, interpreting command ranges, and choosing data protection.'))
    module(r,'nvmcs-crc',lead=b('同樣稱為 CRC 的計算，可能使用不同 polynomial、初值、reflection 與 final XOR。這些參數加上位元儲存順序，才共同決定 Guard 的結果。','CRC computations can use different polynomials, initial values, reflection, and final XOR. Those parameters and the stored bit order together determine the Guard result.'))
    module(r,'nvmcs-export-state',lead=b('Configuration state 描述資源配置，執行中 state 描述當下的 Feature 與 controller 狀態。後者先有固定 64-byte header，再接可變長度的內容。','Configuration state describes resource setup, while runtime state describes current Features and controller state. The latter begins with a fixed 64-byte header followed by variable-length contents.'),
           example=b('NVMECSS=16 代表 NVMECS 有 16×4=64 bytes。加上固定 64-byte header，整個結構是 128 bytes；內層 VER 再指定這段 state 的格式版本。','NVMECSS=16 gives 16×4=64 bytes of NVMECS. Adding the fixed 64-byte header yields a 128-byte structure; the nested VER identifies that state format version.'))
    order = 'foundation capacity identify format-list format namespace-create metadata support-status read-write order-fused atomic compare-verify copy copy-pi dsm dealloc zero-uncorrectable pi-formats crc tag-layout pi-checking basic-features log-events lba-status sanitize alignment performance-feature rate-config rate-modes rate-graph fdp streams ana-reservations key-per-io migration-queue export-template export-state'.split()
    indexed = {m['id']:m for m in modules[r]}
    modules[r][:] = [indexed['nvmcs-'+key] for key in order]
    assert len(modules[r]) == len(indexed)

    module(r,'nvmcs-crc',example=b('CRC-64/NVME 對 4 KiB 全 FFh 資料計算得到 C0DDBA7302ECA3ACh；全 0 資料得到 6482D367EB22B64Eh。兩個資料集長度相同，CRC 仍不同，因為檢查值取決於資料內容。','CRC-64/NVME produces C0DDBA7302ECA3ACh for 4 KiB of FFh and 6482D367EB22B64Eh for 4 KiB of zeros. Equal lengths do not imply equal CRCs because the check value depends on contents.'))
    # Concise headings describe the subject, without invented teaching labels.
    titles = {
      'base-ch1-2': [('family','Base、Command Set 與 Transport 的分工','Roles of Base, Command Set, and Transport'),('numbers','數值編碼與單位','Numeric encodings and units'),('queues','命令提交與完成的往返','Command submission and completion'),('objects','Namespace、Controller 與存取路徑','Namespaces, controllers, and access paths')],
      'base-ch3': [('identity','Controller 類型、識別碼與能力','Controller types, identifiers, and capabilities'),('properties-init','從設定到 CSTS.RDY：初始化流程','Initialization from configuration to CSTS.RDY'),('queue-arbitration','Queue 位置與命令選取','Queue positions and command selection'),('memory-capacity','Namespace、CMB、PMR 與容量','Namespaces, CMB, PMR, and capacity'),('lifecycle','Shutdown、Reset 與狀態保留','Shutdown, reset, and retained state')],
      'base-ch4': [('sqe','SQE 的共用格式與命令欄位','The common SQE format and command fields'),('cqe-status','CQE：新完成項目、命令識別與結果','CQEs: new entries, command identity, and results'),('prp','PRP 如何描述跨頁資料','How PRPs describe data across pages'),('sgl','SGL 的資料與串接描述子','SGL data and segment descriptors'),('identity-text','Feature 值、識別碼、清單與字串','Feature values, identifiers, lists, and strings')],
      'base-admin-fw-logs': [('fw-capability-plan','更新前的能力與限制','Capabilities and limits before an update'),('fw-download-geometry','Download 的長度、偏移與分段','Download lengths, offsets, and portions'),('fw-commit-state','Commit 的儲存與啟用選擇','Commit storage and activation choices'),('fw-lid03-proof','LID 03h 的目前與待啟用版本','Current and pending versions in LID 03h')],
      'base-power-features': [('feature-read-set-loop','Feature 的能力、讀取與設定','Feature capabilities, reads, and settings'),('power-state-mental-model','Power State 的功率、延遲與效能','Power-state power, latency, and performance'),('apst-state-machine','APST 的閒置條件與自動轉換','APST idle conditions and automatic transitions'),('temperature-event-loop','溫度門檻、感測器與通知','Temperature thresholds, sensors, and notifications'),('hctm-control-loop','HCTM 的兩級熱管理','Two levels of HCTM thermal management')],
      'base-self-test-hmb-emulation': [('three-boundaries','背景測試、主機記憶體與位址編碼','Background tests, host memory, and address encoding'),('selftest-command-state-machine','Device Self-test 的啟動與執行','Starting and running Device Self-test'),('selftest-observe-debug','LID 06h 的目前進度與歷史結果','Current progress and history in LID 06h'),('hmb-ownership-lifecycle','HMB 記憶體的提供、使用與收回','Providing, using, and reclaiming HMB memory'),('hmb-command-math','HMB 的描述子、大小與位址','HMB descriptors, sizes, and addresses'),('hmb-reset-power','HMB 在電源轉換與 Reset 後的狀態','HMB state across power transitions and resets'),('encoded-boundary-safety','DSTRD、NDT 與 NDM 的單位','Units of DSTRD, NDT, and NDM')],
      'base-self-test-namespace-management': [('diagnostic-and-provisioning','裝置診斷與 Namespace 配置','Device diagnostics and namespace provisioning'),('selftest-command-state-machine','Device Self-test 的執行與結果','Device Self-test execution and results'),('capacity-granularity-math','容量數值與配置粒度','Capacity values and allocation granularity'),('namespace-create-payload','建立 Namespace 所需的資料','Data required to create a namespace'),('namespace-lifecycle','建立、連接與使用 Namespace','Creating, attaching, and using a namespace'),('delete-restore-state','刪除與恢復預設配置','Deletion and restoration of default configuration'),('namespace-events','Namespace 變更通知與重新辨識','Namespace change notifications and rediscovery')],
      'pcie-transport-1.4': [('layers','NVMe 如何使用 PCIe','How NVMe uses PCIe'),('mmio-doorbell','BAR、MMIO 與 Doorbell 位址','BARs, MMIO, and doorbell addresses'),('command','Host 與 Controller 的命令交換','Command exchange between host and controller'),('interrupts','Interrupt 模式與通知行為','Interrupt modes and notification behavior'),('config-error','Configuration Space 與 PCIe 錯誤回報','Configuration space and PCIe error reporting'),('eom','接收端眼圖量測資料的結構','Receiver eye-opening measurement data layout')],
      'base-boot-telemetry-sanitize': [('telemetry-capture','建立快照、分段讀取與確認完成','Snapshot creation, chunked reads, and acknowledgement'),('sanitize-state','背景 Sanitize 的狀態與進度','Background sanitize state and progress')],
    }
    for rid, rows in titles.items():
        for mid, zh, en in rows:
            module(rid,mid,title=b(zh,en))

    # Replace implementation-failure exercises with conceptual, worked examples.
    module('base-ch4','sgl',example=b('一筆 12 KiB 的資料傳輸，可以由 2 個 Data Block descriptors 描述 8 KiB 與 4 KiB。若 descriptor 類型是 Segment，它的 length 則描述下一段 descriptor list 的大小，並非使用者資料的大小。','A 12 KiB data transfer can use two Data Block descriptors of 8 KiB and 4 KiB. A Segment descriptor instead uses length for the next descriptor list, rather than user-data length.'))
    module('base-ch4','identity-text',
           lead=b('解讀數值前要先確定它代表什麼：Feature 值具有目前與保存狀態的差別；identifier 具有識別範圍；清單與字串則各有排列及長度規則。','Establish what a value represents before interpreting it: Feature values distinguish active from saved state, identifiers have an identity scope, and lists and strings each have layout and length rules.'),
           example=b('含 3 個 controllers 的清單以 NUMCIDS=3 開始，後接 3 個 16-bit IDs。含 3 個 namespaces 的清單則直接從第 1 個 32-bit NSID 開始。UTF-8 字串的 byte 數也不等於字元數，例如「中」占 3 bytes。','A three-controller list starts with NUMCIDS=3 followed by three 16-bit IDs. A three-namespace list starts directly with the first 32-bit NSID. UTF-8 byte length also differs from character count: “中” occupies three bytes.'))
    module('pcie-transport-1.4','eom',
           lead=b('接收端眼圖量測 log 是變長結構。Header 描述整體資料，lane descriptors 描述各 lane；將結構層級與長度單位分開，才能理解每筆量測屬於哪條 lane。','The receiver eye-opening measurement log has variable length. Its header describes the whole dataset, while lane descriptors describe individual lanes. Structure levels and length units identify which lane each measurement belongs to.'),
           example=b('若需要比較 2 條 lanes，先以各自的 lane descriptor 找到量測資料，再依相同的 measurement 格式比較。Header 的 lane 數量用來描述結構，不能直接當成量測品質的指標。','To compare two lanes, locate each measurement through its lane descriptor and compare using the same measurement format. The header lane count describes structure, not measurement quality.'))

    # The introductory modules explain relationships before numeric conventions.
    for rid, order in [('base-ch1-2',['family','objects','queues','numbers']),
                       ('base-ch4',['sqe','cqe-status','prp','sgl','identity-text'])]:
        indexed={m['id']:m for m in modules[rid]}
        modules[rid][:]=[indexed[key] for key in order]
