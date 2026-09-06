"""Small, concrete illustrations selected for their teaching purpose."""
from html import escape


def bi(language, zh, en):
    return en if language == 'en' else zh


def diagram(title, caption, elements, height=260):
    return ('<figure><div class="diagram-scroll"><svg viewBox="0 0 760 ' + str(height) + '" role="img">'
            + '<title>' + escape(title) + '</title><desc>' + escape(caption) + '</desc>'
            + ''.join(elements) + '</svg></div><figcaption>' + escape(caption) + '</figcaption></figure>')


def box(x, y, width, height, lines, role='object'):
    out = [f'<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="6" class="v-{role}"/>']
    for i, text in enumerate(lines):
        yy = y + height / 2 + (i - (len(lines)-1)/2) * 25 + 6
        out.append(f'<text x="{x+width/2}" y="{yy}" text-anchor="middle" font-size="17">{escape(text)}</text>')
    return ''.join(out)


def arrow(x1, y1, x2, y2, label=''):
    # Orthogonal connectors leave the boxes before reaching the next object.
    line = f'<path d="M{x1},{y1} L{x2},{y2}" class="v-line"/>'
    if x2 > x1:
        line += f'<path d="M{x2-7},{y2-4} L{x2},{y2} L{x2-7},{y2+4}" class="v-line"/>'
    else:
        line += f'<path d="M{x2-4},{y2-7} L{x2},{y2} L{x2+4},{y2-7}" class="v-line"/>'
    if label:
        line += f'<text x="{(x1+x2)/2}" y="{(y1+y2)/2-10}" text-anchor="middle" font-size="14">{escape(label)}</text>'
    return line


def steps(title, values, caption):
    return '<figure><figcaption><strong>' + escape(title) + '</strong></figcaption><ol class="flow-steps">' + ''.join('<li>'+escape(v)+'</li>' for v in values) + '</ol><figcaption>'+escape(caption)+'</figcaption></figure>'


def module_illustration(report_id, module, language):
    key = module['id']
    en = language == 'en'
    if key in {'nvmcs-capacity', 'capacity-granularity-math'}:
        title = bi(language, '可定址、可配置、已配置是 3 個不同的量', 'Addressable, allocatable, and allocated are distinct')
        return diagram(title, bi(language, '教學例：NSZE=1000、NCAP=800、NUSE=600。LBA 編號的範圍與目前配置量要分開理解。', 'Example: NSZE=1000, NCAP=800, NUSE=600. The LBA address range is distinct from current allocation.'), [
            box(20,20,720,70,['NSZE = 1000', 'LBA 0 … 999']),
            box(20,110,576,55,['NCAP = 800'], 'command'),
            box(20,185,432,55,['NUSE = 600'], 'success')])
    if key == 'sqe':
        title = 'CDW0 · 32 bits'
        fields = [('CID', '31:16', 300, 'object'), ('PSDT', '15:14', 90, 'command'), ('Reserved', '13:10', 130, 'decision'), ('FUSE','9:8',90,'command'), ('OPC','7:0',110,'success')]
        elements, x = [], 20
        for name, width, span, role in fields:
            elements.append(box(x,35,span,85,[name,width],role)); x += span
        return diagram(title, bi(language, 'CDW0 把命令識別、資料指標類型、融合操作與操作碼放在同一個 Dword。欄位寬度以標示的 bit 範圍為準，圖塊為閱讀需要調整。', 'CDW0 holds command identity, data-pointer type, fused-operation selection, and opcode. Labeled bit ranges determine widths; boxes are sized for readability.'), elements, 160)
    if key in {'queues', 'command'}:
        return steps(bi(language, '一筆命令如何往返', 'One command round trip'), bi(language,
            ['Host 將命令寫入 SQ（提交佇列）。', 'Host 更新 SQ Tail Doorbell，通知 Controller 有新命令。', 'Controller 取出並執行命令，將結果寫入 CQ（完成佇列）。', 'Host 讀取 CQE，再更新 CQ Head Doorbell，交還已讀取的位置。'],
            ['The host writes a command to the Submission Queue (SQ).', 'The host updates the SQ Tail Doorbell to announce new work.', 'The controller retrieves and executes the command, then writes its result to the Completion Queue (CQ).', 'The host reads the CQE and updates the CQ Head Doorbell to release consumed entries.']), bi(language, '命令與結果放在佇列；Doorbell 傳達佇列位置的更新。', 'Queues hold commands and results; doorbells announce updated queue positions.'))
    if key == 'nvmcs-metadata':
        return diagram(bi(language,'資料與 Metadata 放在哪裡','Where data and metadata travel'), bi(language,'同一批 logical blocks 的資料與 metadata 必須對應；可以交錯傳輸，也可以分開傳輸。','Data and metadata must correspond to the same logical blocks, whether transferred together or separately.'), [
            box(20,30,240,65,['Data 0']), box(260,30,120,65,['MD 0'],'decision'), box(390,30,230,65,['Data 1']),box(620,30,120,65,['MD 1'],'decision'),
            box(20,155,350,65,['DPTR: Data 0, Data 1'],'command'),box(390,155,350,65,['MPTR: MD 0, MD 1'],'decision')])
    if key == 'telemetry-layout':
        return diagram(bi(language,'Telemetry Data Areas 是累積範圍','Telemetry Data Areas are cumulative'), bi(language,'Header 位於 block 0。每個 Data Area 都從 block 1 開始，較大的 Area 包含較小 Area 的資料。','The header occupies block 0. Each Data Area starts at block 1, and larger areas include the data in smaller areas.'),[
            box(20,20,155,210,['Header','Block 0'],'command'),
            box(205,20,160,55,['Area 1']), box(205,95,325,55,['Area 2'],'decision'),box(205,170,535,55,['Area 3'],'success')])
    if key == 'telemetry-capture':
        return steps(bi(language,'讓分段讀取對應同一份資料','Keep segmented reads on one snapshot'),bi(language,
            ['讀取 header，記下 generation number。','依資料範圍分段讀取，沿用同一份快照。','再次讀取 header，比較 generation number。','兩次 generation 相符後，才把分段內容視為同一份資料。'],
            ['Read the header and save its generation number.','Read the data in segments from the same snapshot.','Read the header again and compare generation numbers.','Treat the segments as one snapshot only when the generations match.']),bi(language,'Generation number 用來辨識資料版本；建立新快照與讀取既有快照是不同動作。','The generation number identifies a data version; creating a snapshot and reading an existing snapshot are different operations.'))
    if key == 'fw-commit-state':
        return steps(bi(language,'下載、保存與啟用分別改變什麼','Downloading, storing, and activating have different effects'),bi(language,
            ['Firmware Image Download：傳送映像的各個片段。','Firmware Commit：依 CA 選擇保存至 slot 與啟用方式。','需要 reset 的啟用：在指定 reset 發生後切換執行版本。','Firmware Slot Information：分開查看目前執行 slot 與下次預定 slot。'],
            ['Firmware Image Download transfers portions of the image.','Firmware Commit uses CA to choose slot replacement and activation behavior.','Activation requiring reset changes the running image after the specified reset.','Firmware Slot Information distinguishes the current active slot from the next active slot.']),bi(language,'下載完成、映像已保存、版本正在執行，是不同狀態。','Transfer complete, image stored, and image running are different states.'))
    if key == 'namespace-lifecycle':
        return steps(bi(language,'Namespace 從建立到可存取','From namespace creation to access'),bi(language,
            ['建立 namespace，取得 NSID。','將 namespace 附加至指定 controller。','由該 controller 的 Identify 結果確認 namespace 與格式。','I/O 命令使用 NSID 指定要存取的 namespace。'],
            ['Create the namespace and obtain its NSID.','Attach the namespace to the selected controller.','Use that controller’s Identify results to establish the namespace and format.','I/O commands use NSID to select the namespace.']),bi(language,'建立儲存物件與讓 controller 可以存取它，是分開的動作。','Creating a storage object and making it accessible through a controller are separate actions.'))
    if key == 'apst-state-machine':
        return steps(bi(language,'閒置時間如何影響功耗狀態','How idle time affects power state'),bi(language,
            ['Host 設定 APST entries 的閒置時間 ITPT 與目標狀態 ITPS。','啟用 APST 後，controller 依閒置計時判斷轉移。','到達適用門檻後，進入指定 non-operational power state。','恢復處理 I/O 前，需要計入離開該狀態的延遲。'],
            ['The host configures idle time ITPT and target state ITPS in APST entries.','When APST is enabled, the controller evaluates idle timers.','At the applicable threshold, it enters the selected non-operational power state.','Resuming I/O requires accounting for the exit latency of that state.']),bi(language,'APST 以閒置時間換取節能，同時引入狀態轉移延遲。','APST uses idle time to save power while introducing transition latency.'))
    if key == 'hmb-ownership-lifecycle':
        return steps(bi(language,'Host Memory Buffer 的使用期間','The lifetime of a Host Memory Buffer'),bi(language,
            ['Host 配置記憶體，建立 descriptor list。','Host 透過 HMB Feature 將記憶體範圍提供給 controller。','啟用期間，host 維持描述的記憶體範圍有效。','停用並完成規格要求的交接後，host 才能回收記憶體。'],
            ['The host allocates memory and builds a descriptor list.','The HMB Feature makes those ranges available to the controller.','The host keeps the described memory valid while HMB is enabled.','The host reclaims memory only after disabling HMB and completing the required handoff.']),bi(language,'記憶體屬於 host，但不能在 controller 仍可使用時提前回收。','The memory belongs to the host, but cannot be reclaimed while the controller may still use it.'))
    return ''
