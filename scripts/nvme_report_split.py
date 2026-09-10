"""Approved topic boundaries and edition purposes (2026-09-11)."""
from copy import deepcopy

SPLITS = {
 'base-device-self-test': ('base-self-test-hmb-emulation', 'BASESELFTEST', 'Device Self-test：執行、進度與結果', 'Device Self-test: execution, progress, and results', ['selftest-command-state-machine','selftest-observe-results'], 'SELFTEST-'),
 'base-hmb-emulation': ('base-self-test-hmb-emulation', 'BASEHMB', 'HMB、Doorbell Emulation 與 Vendor Commands', 'HMB, Doorbell Emulation, and Vendor Commands', ['hmb-ownership-lifecycle','hmb-command-math','hmb-reset-power','encoded-boundary-safety'], '!SELFTEST-'),
 'base-namespace-management': ('base-self-test-namespace-management', 'BASENAMESPACE', 'Namespace Management：容量、建立與附加', 'Namespace Management: capacity, creation, and attachment', ['capacity-granularity-math','namespace-create-payload','namespace-lifecycle','delete-restore-state','namespace-events'], '!SELFTEST-'),
 'base-boot-partitions': ('base-boot-telemetry-sanitize', 'BASEBOOT', 'Boot Partitions：讀取、更新與寫入保護', 'Boot Partitions: reading, updating, and write protection', ['boot-read','boot-protection'], 'BOOT-'),
 'base-telemetry': ('base-boot-telemetry-sanitize', 'BASETELEMETRY', 'Telemetry：資料收集與一致性讀取', 'Telemetry: capture and consistent retrieval', ['telemetry-layout','telemetry-capture'], 'TEL-'),
 'base-sanitize': ('base-boot-telemetry-sanitize', 'BASESANITIZE', 'Sanitize：清除範圍、方法與完成判斷', 'Sanitize: targets, methods, and completion', ['sanitize-scope','sanitize-command','sanitize-state','sanitize-read'], ('SAN-','NVM-')),
}

# Explicit source identities avoid collisions such as Base Figure 111 and NVM Figure 111.
EXTRA = {
 'base-device-self-test': [36,93,155,338],
 'base-hmb-emulation': [],
 'base-namespace-management': [346],
 'base-boot-partitions': [188,189,190,191,192,193,198,199,464,465,466,757,758,760,761,762,203,204,205,206,207,208,209,338],
 'base-telemetry': [203,205,206,207,208,209],
 'base-sanitize': [203,204,205,206,207,208,209,474],
}

def install(reports, titles, modules, glossaries):
    from scripts.nvme_reader_context import REPORT_CONTEXT, context, b
    from scripts.nvme_overviews import OVERVIEWS
    from scripts.nvme_review_bank import BANK
    originals = deepcopy(modules)
    for rid, (old, prefix, zh, en, mids, keys) in SPLITS.items():
        report = deepcopy(reports[old]); previous = report['prefix']
        report.update(prefix=prefix, title_zh='NVMe Base 2.4：'+zh, title_en='NVMe Base 2.4: '+en)
        if isinstance(keys, str) and keys.startswith('!'):
            report['claims'] = [c for c in report['claims'] if not c['key'].startswith(keys[1:])]
        else:
            report['claims'] = [c for c in report['claims'] if c['key'].startswith(keys)]
        for c in report['claims']:
            titles[prefix+'-'+c['key']] = titles[previous+'-'+c['key']]
        modules[rid] = [deepcopy(m) for m in originals[old] if m['id'] in mids]
        for m in modules[rid]:
            m['sources'] = [s.replace(previous+'-', prefix+'-', 1) for s in m['sources']]
        glossaries[rid] = deepcopy(glossaries[old])
        reports[rid] = report
        allowed = {prefix+'-'+c['key'] for c in report['claims']}
        questions = []
        for q in BANK[old]:
            q = deepcopy(q)
            q['sources'] = [s.replace(previous+'-', prefix+'-', 1) for s in q['sources']]
            if set(q['sources']) <= allowed:
                q['id'] = rid+'-'+str(len(questions)+1)
                questions.append(q)
        BANK[rid] = questions
        intro, flow = OPENINGS[rid]
        axes = [([zt,zd],[et,ed]) for zt,zd,et,ed in AXES[rid]]
        REPORT_CONTEXT[rid] = context(b(*intro), axes, b([],[]))
        OVERVIEWS[rid] = b([flow[0]], [flow[1]])
    for old in {v[0] for v in SPLITS.values()}:
        del reports[old]
    # Clarify the two tests instead of translating an English substring.
    for report in reports.values():
        for c in report['claims']:
            if c['key'] == 'SELFTEST-NSID':
                c['zh_tw'] = ('NSID 指定 Device Self-test 要納入的 namespace。0h 表示只測試控制器；FFFFFFFFh 表示納入作業開始時、已附加且可透過該控制器存取的所有 namespace。指定單一 namespace 時，識別碼超出有效範圍會回覆 Invalid Namespace or Format；有效識別碼若尚未配置，或 namespace 未附加到收到命令的控制器，則屬 inactive，回覆 Invalid Field in Command。Host-Initiated Refresh 忽略 NSID。')
                c['en'] = ('NSID selects namespaces included in Device Self-test. 0h tests the controller only; FFFFFFFFh includes all attached namespaces accessible through that controller when the operation starts. For an individual namespace, an invalid identifier returns Invalid Namespace or Format. A valid identifier that is unallocated, or whose namespace is not attached to the receiving controller, is inactive and returns Invalid Field in Command. Host-Initiated Refresh ignores NSID.')

OPENINGS = {
 'base-device-self-test': (
  ('Device Self-test 讓控制器在背景執行內部測試。讀懂這項功能，必須分清「接受測試要求」、「正在測試」與「留下測試結果」三件事；主機收到命令成功完成，並不表示裝置已通過測試。', 'Device Self-test lets a controller run internal tests in the background. Distinguish accepting a request, running a test, and recording its result: successful command completion does not mean the device has passed the test.'),
  ('先確認控制器支援哪些測試，再選擇測試種類與 namespace，送出命令後觀察目前作業及進度，最後閱讀歷史結果與有效性標記。相同的 Get Log Page 可以在不同時間回答「做到哪裡」和「最後結果如何」，但兩者使用不同欄位。', 'Check supported tests, select the test and namespaces, submit the command, observe the current operation and progress, and finally read historical results and validity indicators. Get Log Page can answer both progress and outcome questions at different times, using different fields.')),
 'base-hmb-emulation': (
  ('這篇說明主機如何把記憶體提供給控制器，以及如何理解 doorbell 位址與廠商命令長度。共同問題是：哪一方可以使用這塊記憶體、何時可以收回，以及欄位中的數值究竟用什麼單位。', 'This note explains memory lent by the host, doorbell addressing, and vendor-command lengths. The connecting questions are who may use the memory, when it may be reclaimed, and what units the encoded values represent.'),
  ('HMB 的提供、使用與收回形成一個完整流程；電源轉換與 reset 會影響這個流程。Doorbell Emulation 與 Vendor Commands 另以位址和長度算例說明，不把它們當成 HMB 的必要步驟。', 'HMB has a provision-use-reclaim lifecycle affected by power transitions and resets. Doorbell Emulation and Vendor Commands are separate address and length examples, rather than required HMB steps.')),
 'base-namespace-management': (
  ('Namespace Management 管理主機可使用的儲存空間。建立 namespace 決定容量與格式；附加 namespace 才把它連到指定控制器。因此，存在一份儲存空間，與主機能經由某個控制器使用它，是兩個不同狀態。', 'Namespace Management manages host-visible storage. Creation determines capacity and format; attachment connects the namespace to a controller. Storage existing and being usable through a particular controller are distinct states.'),
  ('先理解容量與識別碼，再準備建立資料；Create 成功後取得 NSID，接著以 Attachment 建立存取關係。需要調整配置時，分別考慮 Detach、Delete 或還原預設配置，並處理受影響控制器收到的變更通知。', 'Understand capacity and identifiers before preparing creation data. Successful Create returns an NSID; Attachment then establishes access. Configuration changes use Detach, Delete, or restoration of defaults as appropriate, with notifications to affected controllers.')),
 'base-boot-partitions': (
  ('Boot Partitions 提供存放開機映像的空間。這篇從「還沒建立一般 I/O 佇列時，主機如何取到開機資料」開始，再說明映像更新、選擇啟用的分割區與寫入保護。', 'Boot Partitions store boot images. Start with how a host retrieves boot data before normal I/O queues exist, then follow image updates, active-partition selection, and write protection.'),
  ('讀取時要選對分割區與範圍，並提供接收資料的主機記憶體；更新時則要分清傳入映像、替換內容與選擇啟用分割區。寫入保護限制的是更新行為，其狀態在不同 reset 或斷電條件下的保留方式需要另外判讀。', 'Reading selects a partition and range and supplies host destination memory. Updating separates image transfer, replacement, and active-partition selection. Write protection constrains updates; its persistence depends on the reset or power condition.')),
 'base-telemetry': (
  ('Telemetry 把裝置收集的內部狀態整理成主機可讀取的紀錄。這篇的重點是取得一份完整且一致的資料：誰建立紀錄、各資料區有多大，以及分段讀取期間紀錄是否已經換成另一份。', 'Telemetry exposes collected internal state as host-readable logs. The goal is a complete, consistent capture: who creates it, how large each area is, and whether it changes during segmented retrieval.'),
  ('先分清主機發起與控制器發起的紀錄，再從 header 得知資料區範圍。讀取多個區段時，要保留同一份紀錄的識別資訊，並依該類紀錄的規則確認讀取完成；資料區位置可由標準解釋，廠商自訂內容則需要相應格式資料。', 'Distinguish host-initiated and controller-initiated logs, then use the header to establish area boundaries. Preserve capture identity across reads and acknowledge retrieval according to that log’s rules. Standardized locations do not define the contents of vendor-specific payloads.')),
 'base-sanitize': (
  ('Sanitize 處理資料清除。理解它需要依序回答：清除哪些資料、使用哪一種方法、控制器目前處於什麼狀態，以及什麼證據能證明清除已完成。命令已被接受，與清除作業已完成，必須分別確認。', 'Sanitize handles data sanitization. Establish the target, method, current controller state, and evidence of completion. Acceptance of the initiating command and completion of sanitization must be checked separately.'),
  ('先選清除目標與支援的方法，再根據方法設定命令；之後由狀態紀錄判斷進度、成功或失敗。若進入媒體驗證狀態，還要分清驗證讀取與正常資料存取，並用 NVM Command Set 的規則理解清除後讀到的內容。', 'Select the target and supported method, then encode method-specific parameters. Read status to distinguish progress, success, and failure. Media verification has separate access rules; post-sanitize data interpretation follows the NVM Command Set.')),
}


AXES = {
 'base-device-self-test': [
  ('決定測試對象', '先確認支援能力，再選擇測試種類及要納入的 namespace；控制器接受要求後，才開始背景測試。', 'Choose the test and target', 'Check support, choose the test and namespaces, and distinguish accepting the request from running the background test.'),
  ('追蹤正在進行的作業', '用目前作業與完成百分比回答「是否還在測試、做到哪裡」；新的命令、重設或中止要求可能影響進行中的作業。', 'Follow the running operation', 'Use the current operation and completion percentage to follow progress, accounting for commands, resets, and abort requests.'),
  ('判讀留下的結果', '測試停止後，再看結果紀錄。先確認哪些欄位有效，才能解釋失敗位置與相關資訊。', 'Interpret the recorded result', 'Read the result after the test stops. Check field validity before interpreting failure locations and associated information.')],
 'base-hmb-emulation': [
  ('把主機記憶體借給控制器', 'HMB 的重點是記憶體使用權：如何提供、允許使用，以及何時能收回。', 'Lend host memory to the controller', 'Follow how HMB is provided, when the controller may use it, and when the host can reclaim it.'),
  ('處理容量與生命週期', '用容量換算理解描述項，再比較電源轉換和重設對記憶體使用的影響。', 'Understand size and lifetime', 'Translate descriptor values into capacity, then compare the effects of power transitions and resets.'),
  ('讀懂另兩種編碼', 'Doorbell Emulation 與廠商命令分別用位址和長度算例說明；它們是另外的介面機制。', 'Read two separate encodings', 'Use address and length examples to explain Doorbell Emulation and vendor commands as separate interface mechanisms.')],
 'base-namespace-management': [
  ('規劃要建立的儲存空間', '先分清容量、格式與配置粒度：需要多少可定址空間、每個區塊多大，以及控制器建議如何配置。', 'Plan the storage object', 'Separate capacity, format, and allocation granularity: how much addressable space is needed, how large each block is, and what allocation the controller recommends.'),
  ('從建立走到可存取', 'Create 建立 namespace 並回傳識別碼；Attach 讓指定控制器能存取它。用這個流程理解兩種命令各自完成什麼。', 'Move from creation to access', 'Create makes a namespace and returns its identifier. Attach makes it accessible through selected controllers. Follow the distinct outcome of each command.'),
  ('分清移除連接與刪除資料空間', 'Detach 移除控制器的存取關係，Delete 刪除 namespace；還原預設配置又有不同的前提與結果。', 'Separate disconnection from deletion', 'Detach removes access through a controller; Delete removes the namespace. Restoring defaults has its own prerequisites and outcome.'),
  ('讓主機得知配置變動', '建立、附加或刪除後，其他控制器與主機看到的資訊可能改變；透過通知及重新識別更新認識。', 'Keep the host’s view current', 'Creation, attachment, and deletion can change what controllers and hosts see. Follow notifications and refresh identification data.')],
 'base-boot-partitions': [
  ('取出開機映像', '從選擇分割區、指定讀取範圍，到把資料放入主機記憶體，理解開機讀取的完整流程。', 'Retrieve a boot image', 'Follow partition selection, range selection, and transfer into host memory as one boot-read workflow.'),
  ('更新並選擇啟用映像', '傳入新映像、替換分割區內容、選擇啟用分割區，各自解決不同問題。', 'Update and activate an image', 'Separate transferring a new image, replacing partition contents, and selecting the active partition.'),
  ('保護已寫入的內容', '比較不同寫入保護狀態，以及重設或斷電後哪些限制仍然保留。', 'Protect written contents', 'Compare write-protection states and the restrictions that persist across resets or power loss.')],
 'base-telemetry': [
  ('先確認誰建立紀錄', '主機發起與控制器發起的紀錄有不同建立方式；先分清來源，才能正確選擇讀取與確認完成的做法。', 'Establish who created the capture', 'Host-initiated and controller-initiated logs have different creation and acknowledgment rules.'),
  ('從表頭找出資料範圍', '先讀表頭，再用資料區邊界決定要讀哪些區段；標準定義位置，廠商資料格式決定如何理解內容。', 'Use the header to find the data', 'Read the header and area boundaries to plan retrieval. Standardized locations and vendor-specific payload formats answer different questions.'),
  ('確保分段讀到同一份紀錄', '資料可能分多次取回；要檢查紀錄識別與變更資訊，避免把不同時間的內容拼成一份。', 'Keep segmented reads consistent', 'Check capture identity and change information so that multiple reads do not combine data from different captures.')],
 'base-sanitize': [
  ('決定清除範圍', '先確認要清除的資料類別與範圍，再看控制器支援哪些清除能力。', 'Establish the sanitization target', 'Identify the data classes and scope before checking supported sanitization capabilities.'),
  ('選擇方法與參數', '比較區塊清除、覆寫及密碼清除的做法；命令參數必須配合所選的方法。', 'Choose a method and parameters', 'Compare block erase, overwrite, and crypto erase, then select parameters that apply to the chosen method.'),
  ('區分接受、進行與完成', '命令回覆成功不代表資料已清除完畢；持續從狀態紀錄確認進度、成功或失敗。', 'Separate acceptance, progress, and completion', 'Successful command completion does not prove sanitization is finished. Use the status log to follow progress and outcome.'),
  ('理解清除後的讀取', '媒體驗證和正常讀取的用途不同；讀回資料的意義還要結合 NVM Command Set 的規則。', 'Interpret reads after sanitization', 'Media verification and ordinary reads serve different purposes. Interpret returned data using the NVM Command Set rules.')],
}
