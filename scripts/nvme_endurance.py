"""Endurance Group Information and Event Aggregate, plus event configuration."""
from scripts.nvme_report_extension import bi, install_report, render_forward_route
from scripts.nvme_endurance_content import UNITS
from scripts.nvme_endurance_terms import TERMS

CONFIG=dict(id='base-endurance-group-events',prefix='EGE',date='2026-09-22',
 title=bi('NVMe Endurance Group：健康資訊、事件清單與通知設定','NVMe Endurance Groups: Health Information, Pending Events and Notification Settings'),
 range=bi('Base §5.2.13.1.10（LID 09h）、§5.2.13.1.15（LID 0Fh）、§5.2.30.1.17（FID 18h）',
 'Base §5.2.13.1.10 (LID 09h), §5.2.13.1.15 (LID 0Fh), §5.2.30.1.17 (FID 18h)'),
 context=dict(
  intro=bi('同一個儲存裝置裡，不同儲存群組的耐用度與健康狀態可能不同。Endurance Group Information 讓主機查一組的警告、讀寫量與容量；Event Aggregate 則把需要注意的群組列出來。本篇把 FID 18h 的逐組設定接到這兩份 log，說明主機如何從一則通知走到具體資料，又如何確認事件而不誤以為問題已經修復。',
   'Different storage groups in one device can have different endurance and health conditions. Endurance Group Information reports one group’s warnings, traffic and capacity; Event Aggregate lists groups requiring attention. This report connects per-group FID 18h settings to both logs, following a notification to the relevant data and distinguishing acknowledgement from recovery.'),
  axes=bi([
   ['觀察對象與健康狀態','先分清 Group、Set、namespace 的歸屬，再讀警告與壽命估計；避免把一組的資訊當作整台裝置的結論。'],
   ['數值的單位與限制','資料量、命令次數、容量各有自己的單位。用實際數字看懂向上取整與「0 表示未回報」，才不會算出不存在的精確值。'],
   ['設定如何變成待處理清單','逐組選擇警告，再理解清單如何排序、如何編碼長度；識別值、項目序號與 byte 位置各不相同。'],
   ['通知與確認的先後關係','從 AER 完成結果找到清單，再找到單組資料；比較清除通知、移除項目與警告解除，掌握持續警告的處理方式。']],
   [['Storage scope and health','Establish Group, Set and namespace membership, then interpret warnings and wear estimates without treating one group as the whole device.'],
    ['Units and uncertainty','Traffic, command counts and capacity use different units. Work through rounding and zero-as-not-reported before drawing numerical conclusions.'],
    ['From configuration to a pending list','Select warnings per group, then examine ordering and transfer length. Identifiers, entry numbers and byte positions are distinct.'],
    ['Notification and acknowledgement','Follow an AER completion to the aggregate list and individual data. Distinguish notice clearing, entry removal and recovery from the underlying condition.']]),
  background=bi(['預備知識：OS、Computer Organization 與基本 SSD 概念。Group 7／9、警告值與流量數字皆是說明性範例，並非任何特定裝置的量測結果。','先學會看懂資料，再走完整的通知流程；必要的 Get Log Page、Get／Set Features 與 AER 欄位會在本文就近說明。'],
   ['Assumes operating systems, computer organization and basic SSD knowledge. Group identifiers, warning values and traffic figures are illustrative, not measurements from a particular device.','Interpret the data first, then follow the notification sequence. Necessary Get Log Page, Get/Set Features and AER fields are explained locally.'])),
 connections=bi(['用同一個問題串起全篇：Group 7 的可用備用容量降到 8%，門檻為 10%，而且可靠度下降。主機要能說出：哪些 bit 描述狀態、哪些 bit 選擇通知、清單如何找到 7，以及哪次讀取才算確認這一組的事件。','健康資料提供現在的狀態與累積統計；事件機制協助主機及時查看。前者不能完整重建通知當時的狀態，後者也不會因為主機已確認事件就修復媒體。'],
 ['One scenario connects the report: group 7 has 8% available spare against a 10% threshold, plus degraded reliability. Identify the state bits, the reporting mask, how the list selects group 7 and which read acknowledges that group’s event.','Health data supplies current state and cumulative statistics; events prompt timely inspection. Current data is not a complete historical snapshot, and acknowledging an event does not repair media.']),
 questions=[
  dict(key='units',question=bi('DUW=3、MUW=5，能否精確算出主機寫了 3 GB、寫入放大率為 5/3？','Do DUW=3 and MUW=5 prove exactly 3 GB of host writes and write amplification of 5/3?'),answer=bi('不能。兩欄均以十億 bytes 向上取整，DUW=3 代表大於二十億且不超過三十億 bytes。MUW 也只有區間資訊，因此比值只能作粗略觀察。','No. Both fields round up in billions of bytes. DUW=3 means more than two and at most three billion bytes. MUW likewise represents an interval, so the ratio is only a coarse observation.'),sources=['TRAFFIC']),
  dict(key='mask',question=bi('把 Group 7 的 FID18h mask 從 05h 改成 01h，LID09h 的可靠度警告會自動消失嗎？','Does changing group 7’s FID 18h mask from 05h to 01h clear its reliability warning in LID 09h?'),answer=bi('不會。改的是可靠度警告是否觸發新增清單項目；實際狀態由控制器回報。若重新啟用時狀態仍成立，事件可再次回報。','No. The change controls whether that warning adds an entry; the controller still reports the actual condition. Re-enabling reporting while the condition remains true triggers reporting again.'),sources=['CONFIGURE','HEALTH']),
  dict(key='position',question=bi('清單 [1,2,7] 的 index 2 位於 offset 12，查 LID09h 要用哪個 ENDGID？','Index 2 in [1,2,7] starts at offset 12. Which ENDGID selects LID 09h?'),answer=bi('用 7。2 是從 0 起算的項目位置，12 是 byte 距離，7 才是讀出的識別值；此 ID 放進 Get Log Page 的 LSI。','Use 7. Two is the zero-based index and 12 the byte distance; seven is the identifier read from that entry and placed in Get Log Page LSI.'),sources=['AGGREGATE']),
  dict(key='ack',question=bi('成功讀取 LID0Fh、RAE=0 後，為何 Group 7 仍在清單？','Why can group 7 remain listed after a successful LID 0Fh read with RAE=0?'),answer=bi('這次清除的是清單變更通知。要確認 Group 7 的事件並移除它的項目，須成功讀取 LID09h、ENDGID7、RAE=0；若警告持續，也要考慮再次回報。','That read clears the aggregate-change notice. Acknowledge group 7 and remove its entry with a successful LID 09h read for ENDGID7 with RAE=0, while also considering repeated reporting for a persistent condition.'),sources=['SERVICE']),
  dict(key='state',question=bi('收到事件卻讀到 EGCW=0，或看到 PUSED=103，分別可以下什麼結論？','What follows from EGCW=0 after a notice, or from PUSED=103?'),answer=bi('EGCW=0 只說讀取當時沒有該欄位的警告，不能還原通知當時的狀態；103 表示已超過估計壽命的 100%，不直接表示媒體故障或唯讀。兩者都要按欄位本身的時間與定義解讀。','EGCW=0 describes the state at the read, not necessarily at notification time. PUSED=103 exceeds the estimated 100% life consumed but does not itself mean failure or read-only operation. Interpret each field according to its time reference and definition.'),sources=['HEALTH'])])

def install(reports,titles,modules,glossaries,images):
    install_report(CONFIG,UNITS,TERMS,reports,titles,modules,glossaries,images)

ROUTE=[
 (108,110,'3.2.3','3.2.4',bi('從 Endurance Groups 標題開始，用 Figure 69 說明分組，再講三個操作的關係；不回翻 NVM Set 細節。','Start at Endurance Groups, use Figure 69 for containment and connect the three operations without detouring into NVM Set details.')),
 (209,213,'5.2.2','5.2.3',bi('只補 AER、RAE 與 Figure 151 的三個通知欄位；Figure 155 只讀 06h 這列，到該列說明結束即停止。','Introduce AER, RAE and the three Figure 151 notice fields. Read only row 06h of Figure 155 and stop at its end.')),
 (235,241,'5.2.12','5.2.13.1',bi('只補 Get Features 的 SEL、能力回覆，再接 Get Log Page 的 LID、LSI、RAE、NUMD 與 offset；Figure 209 只讀 09h／0Fh。','Cover SEL and the capability result, then Get Log Page LID, LSI, RAE, NUMD and offsets. Read only rows 09h/0Fh in Figure 209.')),
 (263,265,'5.2.13.1.10','5.2.13.1.11',bi('從本節標題開始完整講 Figures 224／225：指定 Group、警告 bit、壽命估計、流量與容量。用 DUW=3 的區間算例。','Start at the section heading and cover Figures 224/225: group selection, warnings, wear estimates, traffic and capacity. Work through the DUW=3 interval.')),
 (296,296,'5.2.13.1.15','5.2.13.1.16',bi('只讀本節及 Figure 261；用 [1,2,7] 算 14-byte 內容與 16-byte 傳輸，再分清逐組項目的移除。','Read this section and Figure 261 only. Use [1,2,7] to derive 14 bytes of content and a 16-byte transfer, then explain removal of a group entry.')),
 (369,398,'5.2.14.2.1','5.2.14.2.2',bi('在 Figure 338 向後依序只找 PDF369 的 OAES bit14、372 的 CTRATT bit4、379 的 AERL、388 的 ENDGIDMAX、398 的 ONCS bit4；跳過其餘欄位，不逐頁朗讀。','Move forward through Figure 338: OAES bit14 on PDF369, CTRATT bit4 on 372, AERL on 379, ENDGIDMAX on 388 and ONCS bit4 on 398. Skip all other fields.')),
 (483,485,'5.2.30','5.2.30.1.1',bi('只讀 Figure 464 的 FID／SV、Figure 466 的 18h 與 0Bh 列及註腳2；保存能力與目前值不要混在一起。','Read FID/SV in Figure 464 and rows 18h/0Bh plus footnote 2 in Figure 466. Distinguish save capability from current settings.')),
 (492,493,'5.2.30.1.6','5.2.30.1.7',bi('在 Figure 474 只讀 EGEALCN bit14 與支援限制，到該 bit 的敘述結束便停止。','Read only EGEALCN bit14 and its support checks in Figure 474, stopping at the end of that bit’s description.')),
 (504,504,'5.2.30.1.17','5.2.30.1.18',bi('完整講 FID18h 與 Figure 493，以 00050007h 收束設定例子，再用已畫好的流程連回兩種確認，不向前翻頁。','Cover FID18h and Figure 493 completely, finishing with 00050007h and the two acknowledgements in the prepared sequence diagram, without paging backward.')),
]

def render_route(reader):
    return render_forward_route(reader,ROUTE)
