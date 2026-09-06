"""Local definitions for concepts and overloaded abbreviations used by readers."""


def b(zh, en):
    return {'zh': zh, 'en': en}


COMMON = {
 'Host': b('主機；執行作業系統並送出 NVMe 命令的一端。','The system running the operating system and issuing NVMe commands.'),
 'logical block': b('邏輯區塊；namespace 可定址的基本單位，其資料大小由使用中的格式決定。','An addressable unit in a namespace; its data size is determined by the active format.'),
 'metadata': b('隨 logical block 儲存的附加資料，可包含資料保護資訊，也可有其他用途。','Additional information stored with a logical block; it can contain protection information or serve other purposes.'),
 'PI': b('Protection Information；用 Guard 與 tags 檢查資料及其關聯資訊的保護欄位。','Protection Information: Guard and tag fields used to check data and its associated information.'),
 'Protection Information': b('資料保護資訊，縮寫 PI；包含 Guard 與 tags，用來檢查資料及其關聯資訊。','PI: protection fields containing a Guard and tags for checking data and its associated information.'),
 'CRC': b('Cyclic Redundancy Check，循環冗餘檢查；由資料位元計算檢查值，以偵測資料變化。','Cyclic Redundancy Check: a check value computed from data bits to detect changes.'),
 'Guard': b('PI 的檢查值欄位；所選格式決定檢查值的寬度與計算方法。','The PI check-value field; the selected format determines its width and calculation.'),
 'LBAF': b('LBA Format；描述一種 logical block 格式，包括資料及 metadata 大小。','LBA Format: a description of a logical-block format, including data and metadata sizes.'),
 'ELBAF': b('Extended LBA Format；與相同 index 的 LBAF 配對，補充 PI 格式與 Storage Tag 大小。','Extended LBA Format: pairs with LBAF at the same index and adds PI format and Storage Tag size.'),
 'Format Index': b('格式索引；用來選取一組 LBAF／ELBAF 格式資訊的編號。','The number selecting a corresponding LBAF/ELBAF format description.'),
 'FID': b('Feature Identifier；指定要讀取或設定哪一項 Feature 的編號。','Feature Identifier: selects the Feature to read or configure.'),
 'LID': b('Log Page Identifier；指定要讀取哪一種 log page 的編號。','Log Page Identifier: selects the type of log page to read.'),
 'CSI': b('I/O Command Set Identifier；選擇 I/O 命令集，NVM Command Set 使用 00h。','I/O Command Set Identifier: selects an I/O command set; NVM uses 00h.'),
 'CNS': b('Controller or Namespace Structure；Identify 命令用來選擇回傳資料結構的欄位。','Controller or Namespace Structure: the Identify selector for a response data structure.'),
 'SCT': b('Status Code Type；指定完成狀態碼所屬類別，需與 SC 一起解讀。','Status Code Type: selects the completion-status category and is interpreted with SC.'),
 'SC': b('Status Code；指定所選 SCT 類別中的完成結果。','Status Code: identifies the completion result within the selected SCT category.'),
 'IOPS': b('Input/Output Operations Per Second；每秒 I/O 操作數，與每秒傳輸 bytes 的頻寬不同。','Input/Output Operations Per Second; an operation rate, distinct from byte throughput.'),
 'APST': b('Autonomous Power State Transition；依設定的閒置條件自動轉換電源狀態。','Autonomous Power State Transition: automatic power-state changes under configured idle conditions.'),
 'HCTM': b('Host Controlled Thermal Management；由 host 設定溫度門檻的熱管理機制。','Host Controlled Thermal Management: thermal management using thresholds configured by the host.'),
 'ANA': b('Asymmetric Namespace Access；描述同一 namespace 經不同 controllers 存取時的路徑狀態。','Asymmetric Namespace Access: the state of access to a namespace through different controllers.'),
 'NUMCIDS': b('Number of Controller Identifiers；Controller List 中有效 controller IDs 的數量。','Number of Controller Identifiers: the count of valid controller IDs in a Controller List.'),
 'Dword': b('Double word；32 bits，也就是 4 bytes。','Double word: 32 bits, or 4 bytes.'),
 'CDW': b('Command Dword；命令中的 32-bit 欄位單位，後面的數字是其索引。','Command Dword: a 32-bit unit in a command, followed by its index.'),
 'NSABP': b('Namespace Atomic Boundary Parameters；表示 namespace 的原子寫入參數是否適用。','Namespace Atomic Boundary Parameters: indicates applicability of namespace atomic-write parameters.'),
 'DRB': b('Deallocated Read Behavior；指定 deallocated logical block 的資料回傳規則。','Deallocated Read Behavior: selects the data-return behavior for deallocated logical blocks.'),
 'DSM': b('Dataset Management；由 host 提供資料範圍的使用與配置提示。','Dataset Management: host hints about use and allocation of data ranges.'),
 'token bucket': b('權杖桶；以累積的額度限制操作速率，執行操作時扣除所需額度。','A rate-control model that accumulates credits and consumes them when admitting work.'),
}

NVM = {}
for term, full, zh, en in [
 ('NSID','Namespace Identifier','識別命令作用的 namespace。','Identifies the namespace addressed by a command.'),
 ('SNSID','Source Namespace Identifier','指定 Copy 的來源 namespace。','Selects a Copy source namespace.'),
 ('ENSID','Exported Namespace Identifier','指定匯出的 namespace。','Identifies an exported namespace.'),
 ('SLBA','Starting LBA','指定命令範圍的起點。','Starts the command range.'),
 ('SDLBA','Starting Destination LBA','指定 Copy 連續目的範圍的起點。','Starts the contiguous Copy destination range.'),
 ('DSLBA','Descriptor Starting LBA','指定 LBA Status descriptor 的範圍起點。','Starts an LBA Status descriptor range.'),
 ('MS','Metadata Size','每個 logical block 的 metadata bytes 數。','Metadata bytes per logical block.'),
 ('PIF','Protection Information Format','選擇 PI 格式；qualified 格式再使用 QPIF。','Selects a PI format; a qualified format additionally uses QPIF.'),
 ('QPIF','Qualified Protection Information Format','指定 qualified PI 的格式。','Selects a qualified PI format.'),
 ('PRINFO','Protection Information','命令內的 PRACT 與 PRCHK 組合欄位。','The command field combining PRACT and PRCHK.'),
 ('PRINFOR','Protection Information Read','Copy 讀取端的 PI 處理與檢查欄位。','Copy read-side PI handling and checking.'),
 ('PRINFOW','Protection Information Write','Copy 寫入端的 PI 處理與檢查欄位。','Copy write-side PI handling and checking.'),
 ('STCR','Storage Tag Check Read','要求 Copy 讀取端的 Storage Tag 檢查。','Requests Copy read-side Storage Tag checking.'),
 ('STCW','Storage Tag Check Write','要求 Copy 寫入端的 Storage Tag 檢查。','Requests Copy write-side Storage Tag checking.'),
 ('GRDCHK','Guard Check','要求 Guard 檢查。','Requests Guard checking.'),
 ('ATCHK','Application Tag Check','要求 Application Tag 檢查。','Requests Application Tag checking.'),
 ('RTCHK','Reference Tag Check','要求 Reference Tag 檢查。','Requests Reference Tag checking.'),
 ('CETYPE','Command Extension Type','選擇命令延伸欄位 CEV 的用途。','Selects the interpretation of the command extension value CEV.'),
 ('CEV','Command Extension Value','內容依 CETYPE 的選擇解讀。','Its contents are interpreted according to CETYPE.'),
 ('DTYPE','Directive Type','指定命令使用哪一類 Directive。','Selects the Directive type for the command.'),
 ('DSPEC','Directive Specific','內容由 Directive 類型決定。','Its contents depend on the Directive type.'),
 ('DMRSL','Dataset Management Range Size Limit','單一 range 的 logical block 處理數量限制。','The logical-block processing limit for one range.'),
 ('DMSL','Dataset Management Size Limit','整筆命令的 logical block 處理數量限制。','The logical-block processing limit for the command.'),
 ('VSL','Verify Size Limit','Verify 的大小限制，需結合 variant 能力判讀。','A Verify size limit, interpreted with its variant capability.'),
 ('WZSL','Write Zeroes Size Limit','Write Zeroes 的大小限制，需結合 variant 能力判讀。','A Write Zeroes size limit, interpreted with its variant capability.'),
 ('WUSL','Write Uncorrectable Size Limit','Write Uncorrectable 的大小限制，需結合 variant 能力判讀。','A Write Uncorrectable size limit, interpreted with its variant capability.'),
 ('NAWUN','Namespace Atomic Write Unit Normal','namespace 正常情況原子寫入大小；依適用與零值規則判讀。','Namespace normal atomic-write size, subject to applicability and zero-value rules.'),
 ('NAWUPF','Namespace Atomic Write Unit Power Fail','namespace 失敗條件的原子寫入大小；依適用與零值規則判讀。','Namespace failure-condition atomic-write size, subject to applicability and zero-value rules.'),
 ('NACWU','Namespace Atomic Compare and Write Unit','namespace 的 fused compare-and-write 大小限制。','The namespace fused compare-and-write size limit.'),
 ('ACWU','Atomic Compare and Write Unit','controller 的 fused compare-and-write 大小限制。','The controller fused compare-and-write size limit.'),
 ('NABSN','Namespace Atomic Boundary Size Normal','正常情況的原子邊界大小。','The normal-operation atomic boundary size.'),
 ('NABSPF','Namespace Atomic Boundary Size Power Fail','失敗條件的原子邊界大小。','The failure-condition atomic boundary size.'),
 ('NP','Number of Ports','Rate Limiting log 的 port 數，採 0-based 編碼。','The 0-based port count in the Rate Limiting log.'),
 ('NC','Number of Controllers','Rate Limiting log 的 controller 數，採 0-based 編碼。','The 0-based controller count in the Rate Limiting log.'),
 ('TBWV','Total Bandwidth Value','總頻寬設定值，需乘上 BWSF 指定的單位。','Total bandwidth value, scaled by BWSF.'),
 ('WBWV','Write Bandwidth Value','寫入頻寬設定值，需乘上 BWSF 指定的單位。','Write bandwidth value, scaled by BWSF.'),
 ('TIOPS','Total IOPS','總 I/O 操作速率設定值。','The total I/O operation-rate value.'),
 ('WIOPS','Write IOPS','寫入操作速率設定值。','The write operation-rate value.'),
 ('WRBWR','Write-to-Read Bandwidth Ratio','寫入相對於讀取的頻寬權重。','The write-to-read bandwidth weight.'),
 ('WRIOPSR','Write-to-Read IOPS Ratio','寫入相對於讀取的操作數權重。','The write-to-read operation-count weight.'),
 ('TGT','Target','選擇 Rate Limiting 設定的目標類型。','Selects the rate-limit target type.'),
 ('TID','Target Identifier','指定所選目標類型中的實體。','Identifies an entity of the selected target type.'),
 ('LBAV','LBA Valid','指出回報的 LBA 是否有效。','Indicates whether the reported LBA is valid.'),
 ('LBARS','LBA Range Status','描述 LBA range 的狀態。','Describes the state of an LBA range.'),
 ('CDQP','Controller Data Queue Phase','讓 host 判別 queue 位置的新 entry。','Lets the host identify a new entry at a queue location.'),
 ('DLBA','Deallocated LBA','entry 中的 deallocation 標記。','An entry flag indicating deallocation.'),
 ('NCQS','Number of I/O Completion Queues Supported','支援的 I/O CQ 數，採 0-based 編碼。','The supported I/O CQ count, using 0-based encoding.'),
 ('NSQS','Number of I/O Submission Queues Supported','支援的 I/O SQ 數，採 0-based 編碼。','The supported I/O SQ count, using 0-based encoding.'),
 ('MQES','Maximum Queue Entries Supported','queue entry 數上限，採 0-based 編碼。','The maximum queue-entry count, using 0-based encoding.'),
 ('SQES','Submission Queue Entry Size','以 2 的次方表示 SQE 的最小與最大 bytes。','Encodes minimum and maximum SQE bytes as powers of 2.'),
 ('CQES','Completion Queue Entry Size','以 2 的次方表示 CQE 的最小與最大 bytes。','Encodes minimum and maximum CQE bytes as powers of 2.'),
]:
    NVM[term] = b(full+'；'+zh, full+'; '+en)


def definitions(report_id, language):
    selected = dict(COMMON)
    if report_id == 'nvm-command-set-1.3':
        selected.update(NVM)
    return {term: value[language] for term, value in selected.items()}
