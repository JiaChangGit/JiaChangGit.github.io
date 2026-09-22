"""Submission Queue Associations: registration and post-only reading route."""
from scripts.nvme_report_extension import bi, install_report, render_forward_route
from scripts.nvme_sqa_content import UNITS
from scripts.nvme_sqa_terms import TERMS

CONFIG = dict(id='base-sq-associations', prefix='SQA', date='2026-09-22',
 title=bi('NVMe SQ Associations：從儲存歸屬到 I/O 佇列分流',
          'NVMe SQ Associations: From Storage Membership to I/O Queue Routing'),
 range=bi('Base §8.1.28；以 PCIe I/O 佇列為例', 'Base §8.1.28, using PCIe I/O queues'),
 context=dict(
  intro=bi('主機知道每筆 I/O 要讀寫哪個 namespace，但控制器也需要知道：這個提交佇列預計服務哪一組儲存空間？SQ Associations 讓主機在建立佇列時提供這項提示。本文把儲存歸屬、佇列配置與命令分流接起來，說明提示何時有幫助，以及為什麼「命令完成」還不足以證明分流正確。',
   'A host knows which namespace an I/O targets, but the controller can also benefit from knowing which storage set a submission queue is intended to serve. SQ Associations supplies that hint when the queue is created. This report connects storage membership, queue setup and command routing, explaining when the hint helps and why successful I/O alone does not prove correct routing.'),
  axes=bi([
   ['看懂三種關係','namespace 屬於哪個 NVM Set，SQ 關聯哪個 Set，完成結果送往哪個 CQ：這三種關係各回答不同問題，不能因為編號接近就混在一起。'],
   ['確認提示的前提','先查控制器能力，再分清 Predictable Latency Mode 是否啟用、Set 目前處於哪種工作視窗。支援位元本身沒有提供固定的應用程式延遲上限。'],
   ['把儲存清單接到建立命令','讀出 Set 的實際識別值及 namespace 歸屬，再放進 Create I/O SQ。清單索引、byte 位置與識別值各有用途，64 筆佇列也有自己的數量編碼。'],
   ['用每筆 I/O 檢查分流','從命令 NSID 找到 Set，再選已關聯該 Set 的 SQ。比較建立參數錯誤與後續送錯佇列，理解規格對兩者規定的不同後果。']],
   [['Distinguish three relationships','A namespace belongs to a set, an SQ is associated with a set, and completions go to a CQ. Each relationship answers a different question; identifiers are not interchangeable.'],
    ['Check the hint’s prerequisites','Discover controller support, distinguish mode enablement from support, and consider the set’s current operating window. Capability bits alone provide no fixed application-latency bound.'],
    ['Connect storage queries to queue creation','Read actual set identifiers and namespace membership, then encode Create I/O SQ. List index, byte position and identifier serve different purposes, as does the count encoding for a 64-entry queue.'],
    ['Check routing for each I/O','Follow command NSID to set to an associated SQ. Compare invalid creation parameters with later queue misuse and their different specified consequences.']]),
  background=bi([
   '預備知識是 OS、Computer Organization 與基本 SSD 概念。本文的 Set 7／9、SQ3／4／5、CQ2 與 namespace 編號均為說明性範例；能力與可用編號以裝置實際回覆為準。',
   '從「這筆 I/O 應送到哪個佇列」出發，先建立全貌，再逐步追蹤查詢、欄位與結果。'],
   ['Assumes operating systems, computer organization and basic SSD knowledge. Sets 7/9, SQ3/4/5, CQ2 and namespace identifiers are illustrative; actual support and identifiers come from the device.',
    'Start with the queue selection for one I/O, establish the overview, then follow queries, fields and results.'])),
 connections=bi([
  '同一組例子貫穿本文：namespace A、B 在 Set 7，C 在 Set 9。主機讓 SQ3、SQ4 服務 Set 7，SQ5 服務 Set 9，而完成結果可以共用 CQ2。讀完應能說明每個編號從哪裡取得、填在哪裡，以及後續怎樣選對 SQ。',
  'SQ Associations 是配合 Predictable Latency Mode 的選用提示。提示是否受支援、提示是否正確、模式當下能提供什麼服務品質，需要分別確認。'],
  ['One example runs throughout: namespaces A/B belong to set 7 and C to set 9. SQ3/SQ4 serve set 7, SQ5 serves set 9, and completions can share CQ2. Follow where each identifier comes from, where it is encoded and how it selects an SQ.',
   'SQ Associations is an optional hint for Predictable Latency Mode. Support for the hint, correctness of the hint and the mode’s current quality of service are separate questions.']),
 questions=[
  dict(key='support',question=bi('CTRATT 的三個相關 bit 都是 1，能否直接保證下一筆 Read 的完成時間？',
    'Do all three capability bits being one guarantee the completion time of the next read?'),
   answer=bi('不能。它們只表示支援能力。還要確認目標 Set 的模式已啟用、目前的工作視窗與操作限制；而服務品質描述也不包括 PCIe 連線的全部延遲。',
    'No. They report support. Check mode enablement for the target set, the current window and operating limits; the quality-of-service description also excludes PCIe connection latency.'),sources=['SUPPORT','SUPPORT-2']),
  dict(key='list',question=bi('清單 Entry 1 的 NSETID=9，建立 SQ 時填 1、256，還是 9？',
    'Entry 1 contains NSETID=9. Should queue creation encode 1, 256 or 9?'),
   answer=bi('填 9。1 是索引；256 是該筆相對整份清單起點的 byte 位置；9 才是要填入 CDW12 的 Set 識別值。',
    'Encode 9. One is the index, 256 is the entry’s byte offset from the list start, and nine is the set identifier for CDW12.'),sources=['INVENTORY','CREATE']),
  dict(key='route',question=bi('NSID21 屬於 Set 9，SQ3 與 SQ5 都使用 CQ2，是否可以任選一個 SQ？',
    'NSID21 belongs to set 9, and SQ3/SQ5 share CQ2. Can either SQ be selected?'),
   answer=bi('依本例應選關聯 Set 9 的 SQ5。共用 CQ 只代表完成結果送到相同地方，不能改變 SQ3 關聯 Set 7 的事實。',
    'Use SQ5, associated with set 9 in this example. Sharing a CQ only shares the completion destination; SQ3 remains associated with set 7.'),sources=['ROUTING','CREATE-2']),
  dict(key='zero',question=bi('把 NVMSETID 設為 0，是建立通往所有 Set 的共同提示嗎？',
    'Does NVMSETID=0 create a shared hint for every set?'),
   answer=bi('不是。Create I/O SQ 把 0 定義為沒有特定 Set 關聯；它不能滿足本篇「先建立關聯，再按 Set 分流」的提示使用方式。',
    'No. Create I/O SQ defines zero as no association with a specific set. It does not provide the association required for the routing discipline described here.'),sources=['CREATE','ROUTING']),
  dict(key='errors',question=bi('Set 9 的命令送到關聯 Set 7 的 SQ，而且成功完成，是否表示主機使用正確？',
    'An I/O for set 9 succeeds on an SQ associated with set 7. Does success prove correct host use?'),
   answer=bi('不表示。送錯 SQ 違反分流規則，可能影響可預測延遲；§8.1.28 沒有要求每次都用錯誤碼拒絕。這與建立 SQ 時填入清單外非零 Set、必須回 Invalid Field in Command 的規則不同。',
    'No. Misrouting violates the operating rules and may affect predictable latency; §8.1.28 does not require rejection with an error each time. This differs from an unsupported nonzero set identifier at SQ creation, which must cause Invalid Field in Command.'),sources=['ROUTING','CREATE'])])


def install(reports, titles, modules, glossaries, images):
    install_report(CONFIG, UNITS, TERMS, reports, titles, modules, glossaries, images)


ROUTE = [
 (363,365,'5.2.14','5.2.14.1',bi('只讀 Figures 333／334 的 CNS 與 CNSSID，再用 Figure 336 的 01h／04h／08h 三列說明三種查詢；到表格註腳即停止，不展開其他 CNS。',
  'Read CNS/CNSSID in Figures 333/334, then only CNS 01h/04h/08h and their relevant footnotes in Figure 336. Skip the other CNS rows.')),
 (370,372,'5.2.14.2.1','5.2.14.2.2',bi('在 Figure 338 只找 bytes 99:96 的 CTRATT，讀 SQA bit 8、PLM bit 5、NSETS bit 2。讀完這三個 bit 就停止，不讀完整 Identify Controller 表。',
  'In Figure 338, locate CTRATT at bytes 99:96 and read only SQA bit 8, PLM bit 5 and NSETS bit 2. Stop after those bits.')),
 (414,415,'5.2.14.2.4','5.2.14.2.5',bi('從 NVM Set List 標題起，用兩筆 Set 7／9 說明起始 ID、NUMENT 與 entry；分清 128-byte 步距和實際 Set ID。',
  'Start at NVM Set List. Use entries for sets 7/9 to explain the starting ID, NUMENT and entries, separating the 128-byte stride from actual identifiers.')),
 (416,419,'5.2.14.2.8','5.2.14.2.9',bi('先確認 active NSID 的回覆條件，再直接在 Figure 346 找 bytes 11:10 的 NVMSETID 與相鄰 ENDGID；讀完歸屬欄即停止。',
  'Check the response condition for an active NSID, then locate NVMSETID at bytes 11:10 and adjacent ENDGID in Figure 346. Stop after membership fields.')),
 (555,557,'5.3.2','5.3.3',bi('以 SQ3、CQ2、Set 7 串起 Figures 575～579；重點在 CDW12 與 CDW11 不同用途，以及非法 Set 的建立結果。',
  'Connect Figures 575–579 with SQ3, CQ2 and set 7, emphasizing the different roles of CDW12/CDW11 and the result of an invalid set at creation.')),
 (708,709,'8.1.21','8.1.21.2',bi('只補模式開頭、Figure 751 與 §8.1.21.1 的操作條件；在 Figure 752 前停止。視窗名稱與模式啟用分開，不展開完整模式設定。',
  'Read the mode introduction, Figure 751 and the operating conditions in §8.1.21.1, stopping before Figure 752. Separate window state from mode enablement without expanding full configuration.')),
 (758,759,'8.1.28','8.1.29',bi('從 Submission Queue (SQ) Associations 標題開始，最後完整講主範圍：選用提示、支援前提、建立時關聯，以及兩項主機分流規則。',
  'Start at Submission Queue (SQ) Associations and conclude with the complete primary scope: optional hint, support prerequisites, association at creation and the two host routing rules.')),
]


def render_route(reader):
    return render_forward_route(reader, ROUTE)
