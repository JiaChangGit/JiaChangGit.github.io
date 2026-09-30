"""Editorial source for the independently scoped NVMe figure quick reference."""
CARDS = {}

def card(key, title, tags, zh, en, related=''):
    assert key not in CARDS, key
    assert len(zh) == len(en) and len(zh) >= 3, key
    CARDS[key] = dict(key=key, title=title, tags=tags.split('|'),
                      paragraphs={'zh':zh, 'en':en}, related=related.split())

TOPICS = [
    ('init','初始化、佇列與 PCIe','Initialization, Queues, and PCIe',
     '先確認位址與能力，再看啟用狀態、佇列位置與中斷。PCIe link 和錯誤暫存器用來區分傳輸問題與命令回覆。',
     'Start with addresses and capabilities, then readiness, queue locations and interrupts. Link and PCIe error registers distinguish transport observations from command completions.'),
    ('command','命令格式、資料指標與完成狀態','Commands, Data Pointers, and Completion Status',
     '先用 SQID／CID 對回命令，再解 SCT／SC。資料搬移異常時，分清 PRP 的頁面指標與 SGL 的位址、長度和描述子類型。',
     'Match the command using SQID/CID before decoding SCT/SC. For data-transfer problems, distinguish PRP pages from SGL addresses, lengths and descriptor types.'),
    ('identify','Identify、Namespace 與資料格式','Identify, Namespaces, and Data Formats',
     'CNS 決定回傳哪一種 Identify 結構；controller 能力、namespace 格式和選定格式的大小要分開查，再組合成可用設定。',
     'CNS selects the Identify structure. Look up controller capabilities, namespace configuration and selected-format sizes separately, then combine them into a valid configuration.'),
    ('io','I/O 命令與資料完整性','I/O Commands and Data Integrity',
     '由命令的位址與數量走到 metadata、保護資訊和原子性。相同欄位寬度不代表相同計數方式，命令成功也不等於所有持久性與原子性保證都成立。',
     'Follow command addresses and counts into metadata, protection information and atomicity. Equal field widths do not imply equal counting rules; command success alone does not establish every persistence or atomicity guarantee.'),
    ('features','Features、電源、效能與資源','Features, Power, Performance, and Resources',
     '先分辨支援能力、目前值、預設值與保存值，再查各 Feature。電源延遲、排程權重、佇列數與回收資源各有單位，不能互相替代。',
     'Separate support, current, default and saved values before interpreting individual features. Power latency, scheduling weights, queue counts and reclamation resources use different units.'),
    ('logs','健康、事件與診斷紀錄','Health, Events, and Diagnostic Logs',
     '先確認讀取參數與支援，再分清目前狀態、累計數與歷史快照。Telemetry 和持久事件的版本、長度與讀取生命週期，會決定資料能否正確串接。',
     'Validate retrieval parameters and support, then distinguish current state, cumulative counters and historical snapshots. Telemetry and persistent-event versions, lengths and retrieval lifecycles determine whether records can be combined.'),
    ('maintenance','維護與管理操作','Maintenance and Management',
     '把要求的動作、命令完成與背景操作結果分開看。韌體提交、namespace 建立和 Sanitize 接受命令，各自都還有不同的後續狀態需要核對。',
     'Separate the requested action, command completion and background result. Firmware commitment, namespace creation and acceptance of a Sanitize command each require different follow-up observations.'),
]

# Keep the editorial sequence explicit; imports register each source figure once.
def load():
    from scripts import nvme_quickref_init, nvme_quickref_command, nvme_quickref_identify
    from scripts import nvme_quickref_io, nvme_quickref_features, nvme_quickref_logs, nvme_quickref_maintenance
    return CARDS
