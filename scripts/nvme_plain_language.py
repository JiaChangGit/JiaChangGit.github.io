"""Normalize prose, not HTML, identifiers, or English translations."""
import re

PHRASES = {
 '不能混成同一種 gate': '必須分開判斷必要要求與配置建議',
 'preferred hint，不是單獨 abort gate': '建議配置粒度；未符合這項建議，不能單獨成為拒絕命令的理由',
 'otherwise-valid create': '符合其他所有要求的建立命令',
 'otherwise valid create': '符合其他所有要求的建立命令',
 'portion alignment／granularity gate': '每段映像的起點對齊與長度粒度要求',
 'capability gate': '功能支援條件', 'format gate': '格式選用條件',
 'validity gates': '有效性判斷', 'validity gate': '有效性判斷',
 'interpret the fields bytes': '換算後的 byte 數',
 'controller-local active state': '對指定控制器的可存取狀態',
 'exclusive ownership lifecycle': '記憶體交付、使用與收回的期間',
 'operation lifecycle': '背景作業的各個階段',
 'record fence timestamp': '停用完成後才可修改或回收',
 'validate alignment/count': '先核對位址對齊和描述子數量',
 'controller exclusive use': '控制器專用；主機不得修改',
 'host owns and initializes descriptors': '主機配置記憶體並初始化描述子',
 'controller may still retrieve data': '控制器仍可取回必要資料',
 'host still waits': '主機仍須等停用完成',
 'host may modify/reclaim': '主機可修改或收回記憶體',
 'Before enable': '啟用之前', 'After enable CQE': '啟用命令完成後',
 'Disable in flight': '停用命令尚未完成', 'After disable CQE': '停用命令完成後',
 'current value': '目前值', 'default value': '預設值', 'saved value': '保存值',
 'configured policy': '設定的使用政策', 'current restriction state': '目前生效的限制狀態',
 'new undefined contents': '新提供的記憶體，內容尚未初始化',
 'return identical old HMB': '交回符合相同條件的原有 HMB',
 '建立 rollback baseline': '了解預設設定',
 '確認此刻 controller policy': '確認控制器目前採用的設定',
 'byte-unit hints': '以 bytes 為單位的配置粒度建議',
 'granularity hints': '配置粒度建議', 'granularity violation': '未符合粒度建議',
 'capacity consumption': '實際消耗容量', 'allocation capacity': '配置容量',
 'allocation unit': '內部配置單位', 'fully provisioned': '完整配置',
 'physical address': '實體位址', 'physically contiguous': '實體位址連續',
 'active NSID': '目前可存取的 NSID', 'controller only': '只測試控制器',
 'support marker': '支援標示', 'command identity': '命令身分',
 'namespace scope': '指定的 namespace 範圍',
 'command-specific payload': '命令專用參數',
 'data-pointer selector': '資料指標選擇欄位',
 'address + byte length': '起始位址與資料長度（bytes）',
 'address + descriptor-list length': '清單位址與清單長度（bytes）',
 'page-based addresses': '以記憶體頁描述位址',
 'sustained maximum power': '持續最大功率',
 'idle typical／active average': '閒置典型功率／工作中平均功率',
 'relative throughput／latency': '相對吞吐量／相對延遲',
 'body_section': 'body_section',
}

WORDS = {
 'gate':'必要條件', 'hints':'建議', 'hint':'建議', 'abort':'中止命令',
 'aborted':'被中止', 'allocation':'配置', 'rounding':'向上取整',
 'divisibility':'是否為整數倍', 'granularity':'粒度',
 'buffer':'緩衝區', 'buffers':'緩衝區', 'controller':'控制器',
 'controllers':'控制器', 'host':'主機', 'hosts':'主機',
 'command':'命令', 'commands':'命令', 'completion':'完成回報',
 'capability':'支援能力', 'capabilities':'支援能力',
 'target':'操作對象', 'state':'狀態', 'scope':'作用範圍',
 'status':'狀態', 'reset':'重設', 'enable':'啟用', 'disable':'停用',
 'ownership':'使用權限', 'bytes':'bytes', 'raw':'原始',
 'offset':'位移', 'index':'索引', 'entry':'項目', 'entries':'項目',
 'count':'數量', 'length':'長度', 'address':'位址',
 'unit':'單位', 'units':'單位', 'boundary':'邊界',
 'payload':'資料內容', 'layout':'欄位配置', 'header':'標頭',
 'reserved':'保留', 'read-only':'唯讀', 'shared':'共享',
 'active':'目前可存取', 'inactive':'目前不可存取',
 'attached':'已附加', 'unallocated':'尚未配置', 'allocated':'已配置',
 'otherwise':'其他情況', 'may':'可以', 'shall':'必須', 'should':'建議',
}


def chinese(value):
    for old, new in sorted(PHRASES.items(), key=lambda item: -len(item[0])):
        # Phrase boundaries also apply to the first/last English word. In
        # particular, active NSID must never match inside inactive NSID.
        pattern = (r'(?<![A-Za-z])' if old[0].isascii() and old[0].isalpha() else '') + re.escape(old) + (r'(?![A-Za-z])' if old[-1].isascii() and old[-1].isalpha() else '')
        value = re.sub(pattern, lambda _: new, value)
    # Keep technical English terms in the sentence when the surrounding
    # paragraph defines them below. Replacing every isolated word (for
    # example, controller or host) created artificial spaces and duplicated
    # normative wording such as “必須（必須）”.
    # Correct isolated simplified characters introduced in older teaching copy.
    for old, new in {'单凭':'單憑','單凭':'單憑','单独':'單獨','單独':'單獨','后续':'後續','後续':'後續',
                     '关系':'關係','比較':'比較','比较':'比較','整体':'整體','减少':'減少','结果':'結果',
                     '圖':'圖','图':'圖','该':'該','一条':'一條','一张':'一張','传输':'傳輸','傳输':'傳輸',
                     '两級':'兩級'}.items():
        value = value.replace(old, new)
    return value


def tree(value, lang=None):
    if isinstance(value, dict):
        return {k:tree(v, k if k in ('zh','en','zh_tw') else lang) for k,v in value.items()}
    if isinstance(value, list):
        return [tree(v, lang) for v in value]
    return chinese(value) if isinstance(value,str) and lang in ('zh','zh_tw') else value


def apply(modules):
    for rid, values in modules.items():
        modules[rid] = tree(values)
    def update(rid, key, **fields):
        next(m for m in modules[rid] if m['id']==key).update(fields)
    update('base-self-test-namespace-management','capacity-granularity-math',
      lead={'zh':'先分清各種容量數值的單位，再比較必要的容量關係與建議配置粒度。前者決定是否符合規格要求，後者用來減少配置空間的浪費。',
            'en':'Establish capacity units before comparing required capacity relationships with recommended allocation granularities. The former govern validity; the latter reduce wasted allocation.'},
      example={'zh':'每個區塊 4 KiB、NSG=1 MiB、NCG=2 MiB。NSZE=NCAP=1024 時，1024×4 KiB=4 MiB，是兩種粒度的整數倍。改成 1000 時，1000×4 KiB=4000 KiB=3.90625 MiB，不是 1 MiB 或 2 MiB 的整數倍；可能浪費部分配置容量。但只要其他要求符合，不能只因未符合粒度建議而中止建立命令。',
               'en':'With 4 KiB blocks, NSG=1 MiB and NCG=2 MiB, NSZE=NCAP=1024 gives 4 MiB, a multiple of both granularities. A count of 1000 gives 4000 KiB=3.90625 MiB, not a multiple of 1 MiB or 2 MiB. Some allocated capacity may be wasted, but an otherwise valid creation command shall not be aborted solely for failing the granularity hints.'})
    update('base-power-features','apst-state-machine', example={
      'zh':'閒置 2000 ms 後進 PS3：ITPT=2000=07D0h，放入 bits31:8 得 0007D000h；ITPS=3，放入 bits7:3 得 18h。相加得到低 Dword=0007D018h，其餘保留位與高 Dword 為 0。32 個 8-byte 項目合計 256 bytes。',
      'en':'For PS3 after 2000 ms idle: ITPT=2000=07D0h in bits31:8 gives 0007D000h; ITPS=3 in bits7:3 gives 18h. Their sum is low Dword 0007D018h. Reserved bits and the high Dword are zero. Thirty-two 8-byte entries total 256 bytes.'})
    update('base-ch4','identity-text', rows={
      'zh':[['VID／SSVID','廠商與 subsystem 廠商識別值','按各自欄位辨認對象'],['SN／MN','產品序號與型號字串','依固定欄位長度與填補規則閱讀'],['EUI64／NGUID／UUID','不同格式的物件識別值','長度及身分範圍不能互換'],['Controller List','NUMCIDS 加上 16-bit IDs','有明確數量欄位'],['Namespace List','直接排列 32-bit NSIDs','沒有 Controller List 的數量標頭']],
      'en':[['VID/SSVID','Vendor and subsystem vendor identifiers','Interpret each field for its own object'],['SN/MN','Product serial and model strings','Read fixed lengths and padding rules'],['EUI64/NGUID/UUID','Different object identifier formats','Widths and identity scopes are not interchangeable'],['Controller List','NUMCIDS followed by 16-bit IDs','Has an explicit count header'],['Namespace List','Direct sequence of 32-bit NSIDs','Does not have the Controller List count header']]})
    update('base-self-test-hmb-emulation','hmb-ownership-lifecycle', example={
      'zh':'把啟用及停用放在時間線上：啟用完成後，控制器可使用主機提供的區域；送出 EHM=0 只是要求停止使用。在停用完成回報到達之前，這些區域仍保持有效。停用完成後，主機才可以修改或回收。',
      'en':'On the HMB timeline, enable completion permits controller use of the provided regions. Submitting EHM=0 requests disablement; the regions remain valid until disable completion. The host may modify or reclaim them afterward.'})

    # A section about format units should not jump to an unrelated Rate Limiting identifier.
    update('nvm-command-set-1.3','nvmcs-foundation', example={
      'zh':'LBADS=0Ch 表示資料大小 2^12=4096 bytes；MS=16 表示每個區塊另有 16 bytes metadata，所以完整邏輯區塊為 4112 bytes。Format Index=3 只是選第 4 個格式，不能拿 3 當作大小或位移。',
      'en':'LBADS=0Ch gives 2^12=4096 data bytes; MS=16 adds 16 metadata bytes per block, for a complete logical block of 4112 bytes. Format Index=3 selects the fourth format; three is neither its size nor an offset.'})
