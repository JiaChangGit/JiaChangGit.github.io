"""SQ Associations: concepts, worked examples, and a tutorial independent of posts."""
from scripts.nvme_report_extension import bi
UNITS=[]


def unit(key, title, summary, section, pages, example, steps, reading, background=False, extras=()):
    UNITS.append(dict(key=key,title=bi(*title),claims=[dict(text=bi(*summary),section=section,pages=pages,background=background),*extras],
        example=bi(*example),steps=steps,reading=bi(*reading)))


def reference(section,pages,zh,en):
    return dict(section=section,pages=pages,text=bi(zh,en),background=True)


unit('model',('把佇列用途告訴控制器','Tell the controller which set a queue serves'),
 ('SQ Associations 讓主機在建立 I/O Submission Queue 時，提供該 SQ 對應的 NVM Set，作為控制器在 Predictable Latency Mode 下改善效能的提示。這是選用能力；Predictable Latency Mode 不依賴主機一定使用 SQ Associations。',
  'SQ Associations lets a host associate an I/O Submission Queue with an NVM Set at queue creation, providing a hint for improved performance with Predictable Latency Mode. It is optional; Predictable Latency Mode does not depend on using SQ Associations.'),
 '8.1.28','758-759',
 ('說明性範例：Set 7 內有 namespace A、B，Set 9 內有 C。主機先安排 SQ3、SQ4 服務 Set 7，SQ5 服務 Set 9，再在建立各 SQ 時送入對應的 Set 編號。控制器因此知道這些佇列預期承載哪一組儲存空間的 I/O。',
  'Illustrative example: set 7 contains namespaces A/B and set 9 contains C. The host assigns SQ3/SQ4 to set 7 and SQ5 to set 9, specifying those set identifiers when creating the queues. The controller learns which storage group each queue is intended to serve.'),
 [('先辨認三種物件','namespace 是命令要存取的邏輯儲存空間；NVM Set 是可配置出 namespace、也可保留未配置空間的儲存集合；SQ 是主機放置待執行命令的佇列。它們分別回答「存取誰、屬於哪組儲存、從哪裡提交」。不能把 SQ 的記憶體空間當作 namespace 的資料容量。'),
  ('關聯描述的是 SQ 的預定用途','主機把某個 SQ 關聯到 Set 7，意思是打算把 Set 7 內 namespace 的 I/O 送到這個 SQ。這項關聯不會建立 namespace，也不會把原本屬於 Set 9 的 namespace 搬到 Set 7。I/O 命令本身仍以 NSID 指定真正的資料對象。'),
  ('為什麼要讓控制器知道','Predictable Latency Mode 以 NVM Set 為單位提供服務品質屬性。若主機把不同 Set 的工作混在同一個 SQ，控制器比較難單靠佇列判斷工作所屬；提供關聯並遵守分流規則，讓佇列資訊能配合 Set 層級的處理。規格沒有替這項提示指定固定的加速倍數。'),
  ('提示、模式與延遲保證分別看','支援 SQ Associations、已建立 SQ 關聯、已啟用 Predictable Latency Mode，是三個不同狀態。建立 SQ 關聯不會順便把模式打開；模式也可以在不使用此選用提示的情況下運作。主機若希望取得關聯的效益，還必須持續按正確 Set 分流。')],
 ('先看 Figure 67 的儲存歸屬，再對照命令中的 NVMSETID；本節本身沒有另列編號圖表。','Start with storage membership in Figure 67, then connect it to NVMSETID in the command. The primary section contains no separately numbered figure.'))

unit('support',('支援能力、模式狀態與工作視窗','Separate support, mode state and operating windows'),
 ('支援 SQ Associations 的控制器必須在 CTRATT 同時宣告 SQA、NVM Sets 與 Predictable Latency Mode 支援。這些支援位元不表示每個 Set 目前都已啟用模式，也不表示目前處於可提供確定性延遲的視窗。',
  'A controller supporting SQ Associations must advertise SQA, NVM Sets and Predictable Latency Mode in CTRATT. These support bits do not mean that every set has the mode enabled or is currently in a deterministic window.'),
 '8.1.28','758-759',
 ('只觀察相關三個 bit：SQA bit 8、PLM bit 5、NSETS bit 2 的遮罩合計為 0124h。用 (CTRATT & 0124h)==0124h 檢查三者，不要求整個 CTRATT 恰好等於 0124h，因為控制器可能還有其他能力。',
  'The three relevant bits are SQA bit 8, PLM bit 5 and NSETS bit 2, giving mask 0124h. Test (CTRATT & 0124h)==0124h rather than requiring the entire field to equal 0124h, since other capabilities may also be present.'),
 [('先讀控制器的能力宣告','Identify Controller 的 CTRATT 位於 bytes 99:96。SQA bit 8 為 1 表示支援 SQ Associations；同時必須有 NSETS bit 2 與 PLM bit 5。這三個 bit 是不同能力，不可只看到支援 NVM Sets，就自行推論控制器也支援 SQ Associations。'),
  ('支援不等於目前已啟用','模式是以 NVM Set 為單位配置的。假設 Set 7 已啟用 Predictable Latency Mode，Set 9 沒有啟用，兩者仍可存在於宣告 PLM 支援的同一個控制器內。本篇設定 SQ 關聯的命令不會取代模式配置；範例的效益討論以相關 Set 已啟用該模式為前提。'),
  ('模式內還有兩種工作視窗','例如 Set 7 在 DTWIN 接收讀寫，之後進入 NDWIN 準備下一個視窗；這時延遲性質已改變，SQ3 關聯 Set 7 的設定卻可以保持不變。規格的服務品質描述適用於 subsystem 內部，不涵蓋 PCIe 傳輸路徑的全部延遲。因此不能僅靠 SQA=1 保證應用程式端的每次 I/O 延遲。'),
  ('保持正確路由仍不足以無限延長 DTWIN','DTWIN 還受到讀取量、最佳寫入大小的寫入量、視窗時間及廠商定義屬性限制；若超過相關典型或最大值，或發生需控制器立即處理的 Deterministic Excursion，Set 可能轉入 NDWIN。SQ 關聯幫助工作分組，但沒有取消這些模式規則。')],
 ('Figure 338 讀三個支援位元；Figure 751 讀兩種工作視窗，不把視窗的交替誤認為功能支援 bit 在切換。','Read the three capability bits in Figure 338 and the operating windows in Figure 751; window transitions are not changes to capability bits.'),
 extras=[reference('8.1.21','708-709','Predictable Latency Mode 有 DTWIN／NDWIN；DTWIN 的確定性依賴操作限制與當時狀態，SQ 提示不會取消這些條件。','Predictable Latency Mode has DTWIN/NDWIN; determinism depends on operating rules and current state, which the SQ hint does not remove.')])

unit('inventory',('先建立 namespace 到 Set 的對照','Map namespaces to sets before routing commands'),
 ('主機需要兩份資訊：NVM Set List 說明控制器可存取哪些 Set，Identify Namespace 則說明指定 namespace 屬於哪個 Set。清單位置、NVM Set Identifier 與 NSID 是不同數值，不能用同一個編號代替。',
  'The host needs two kinds of information: the NVM Set List identifies accessible sets, while Identify Namespace identifies the set containing a namespace. List position, NVM Set Identifier and NSID are different values.'),
 '5.2.14.2.4','414-415',
 ('說明性範例：NUMENT=2，Entry 0 的 NSETID=7，Entry 1 的 NSETID=9；兩筆分別從 byte 128、256 開始。另查 NSID=11、12 得到 Set 7，查 NSID=21 得到 Set 9。路由表應保存這些實際值，不是把清單索引 0、1 當 Set 編號。',
  'Illustrative example: NUMENT=2, entry 0 has NSETID=7 and entry 1 has NSETID=9, at byte offsets 128 and 256. Namespace queries map NSIDs 11/12 to set 7 and NSID 21 to set 9. Store those actual mappings, not list indices 0/1 as set identifiers.'),
 [('用 CNS 選正確的問題','Identify 的 CNS=01h 取得控制器能力，CNS=04h 取得 NVM Set List，CNS=08h 取得指定 namespace 的 I/O Command Set Independent 資料。CNS 放在 CDW10 bits 7:0；CNS=04h 用 CDW11 的 CNSSID 低 16 bits 提供清單起始 Set 編號，CNS=08h 則以命令 NSID 選 namespace。'),
  ('清單的數量與位置要各自計算','NVM Set List 前 128 bytes 是 header，NUMENT 在 byte 0，直接表示 0～31 筆。每筆 entry 為 128 bytes，所以索引 i 的起點為 128+i×128。NUMENT=0 就是空清單，不把後面的補零區解成 Set 0；最多 31 筆加 header 正好是 4096 bytes。'),
  ('起始識別值使用大於或等於','CNS=04h 回傳的 Set 識別值從指定起點開始，採大於或等於，並按識別值排序。若上一批最後一個 NSETID 是 37，而還要繼續查，可以用 38 當下一次起點，避免又取回 37。這個起點是識別值，不是第幾頁，也不是記憶體 byte offset。若到 FFFFh 就不能再加 1 回繞成 0。'),
  ('從 namespace 的回覆找歸屬','對有效且目前可透過該控制器存取的 NSID 使用 CNS=08h，回覆 bytes 11:10 的 NVMSETID 指出其 Set。若查 inactive NSID，回的是全零結構，不能把它當成「有效 namespace 屬於 Set 0」。不支援 NVM Sets 或 namespace 沒有已格式化儲存空間時，此欄也為 0，因此要連同查詢條件判斷。'),
  ('能力或配置改變後，對照表也要跟著更新','命令的 NSID 決定真正的資料對象，主機保存的對照表只是目前認識。若 namespace 被刪除或配置已變，不能繼續拿舊的 NSID→Set→SQ 關係送命令。建立 SQ 前先確認目標 Set 在可用清單中，之後也要讓路由與目前有效的 namespace 配置一致。')],
 ('Figures 333／334／336 選查詢；343～345 解釋清單；346 只取 NSID 查詢條件及 NVMSETID 歸屬欄位。','Figures 333/334/336 select the query; 343–345 explain the list; 346 supplies the namespace-to-set mapping.'), True,
 extras=[reference('5.2.14.2.8','416,419','CNS=08h 對 active NSID 回 namespace 結構；NVMSETID 位於 bytes 11:10。inactive NSID 回全零資料，不能當有效歸屬。','CNS=08h returns the namespace structure for an active NSID, with NVMSETID at bytes 11:10. An inactive NSID returns zeros rather than a valid membership mapping.')])

unit('create',('建立 SQ 時，同時指定 Set 與完成佇列','Select both the set and completion queue when creating an SQ'),
 ('Create I/O Submission Queue 的 CDW12.NVMSETID 建立 SQ 與 Set 的關聯；CDW11.CQID 則指定完成結果送往哪個 CQ。兩個欄位用途不同。NVMSETID=0 或不支援 SQA 時不建立特定 Set 關聯；SQA 支援時指定清單外的非零 Set，命令必須以 Invalid Field in Command 中止。',
  'Create I/O Submission Queue uses CDW12.NVMSETID for the set association and CDW11.CQID for the destination completion queue. NVMSETID=0 or unsupported SQA means no specific set association. With SQA supported, a nonzero identifier absent from the set list must cause Invalid Field in Command.'),
 '5.3.2','555-557',
 ('說明性範例：CQ2 已建立且裝置支援所需深度，建立 64 筆的 SQ3，關聯 Set 7，採實體連續記憶體與 round-robin 仲裁：CDW10=003F0003h、CDW11=00020001h、CDW12=00000007h。若每個 SQE 為 64 bytes，64 筆需 4096 bytes。',
  'Illustrative example: with CQ2 already created and sufficient supported depth, create a 64-entry SQ3 associated with set 7, using contiguous memory and round-robin arbitration: CDW10=003F0003h, CDW11=00020001h, CDW12=00000007h. At 64 bytes per SQE, the queue uses 4096 bytes.'),
 [('先準備完成結果的去處','CQ 保存完成項目，SQ 保存待執行命令。Create I/O SQ 的 CQID 必須指定已建立的有效 I/O CQ；不能填 Admin CQ 的 0。多個 SQ 可以把結果送往同一個 CQ，因此 CQ2 的編號與 Set 7 沒有必須相同的關係。'),
  ('CDW10 同時裝深度與 SQ 編號','bits 31:16 的 QSIZE 採數量減 1，64 筆填 63，也就是 003Fh；bits 15:0 的 QID 填 SQ3 的 3。合成 (63<<16)|3=003F0003h。QSIZE=0 不是空 SQ 的合法建立要求；QID=0 是 Admin Queue，也不能用來建立一般 I/O SQ。'),
  ('CDW11 管完成路徑、優先級與記憶體配置','CQID 放高 16 bits，本例是 2。低位 PC=1 表示實體連續 SQ 記憶體；QPRIO bits 2:1 只在 weighted round robin with urgent priority class 仲裁時使用，本例採 round robin，因此控制器忽略 QPRIO。剩餘 bits 15:3 保留。這些欄位都不會代替 CDW12 的 Set 選擇。'),
  ('CDW12 才是這篇的 Set 提示','低 16 bits 放 NVMSETID=7，高 16 bits 保留。0 在此有明確定義：不與特定 Set 關聯；它不是廣播到全部 Set。這和某些必須指定有效 Set 的其他命令對 0 的規則不同，必須依 Create I/O SQ 的定義解讀。'),
  ('PRP1 指向佇列記憶體','PC=1 時，PRP1 放實體連續 SQ 的基底位址，並依已配置的記憶體頁大小對齊。以 4 KiB 頁、每項 64 bytes、64 筆為例，SQ 恰好占一頁，可用 00100000h 等已配置且對齊的主機位址。這個位址保存命令項目，不是 Set 7 的儲存媒體位址。'),
  ('等建立成功，再使用這個 SQ','SQ 的 QID、CQID、深度與 Set 識別值都需要各自有效。建立命令成功後，主機才可按該 SQ 的配置提交 I/O。若支援 SQA 卻把不存在的 Set 99 填入 CDW12，這是建立參數錯誤；與之後把其他 Set 的 I/O 送錯佇列是不同問題。')],
 ('Figures 575～579 按記憶體、深度、完成路徑、Set 與建立錯誤分工閱讀；本篇範例採一般主機記憶體。','Read Figures 575–579 as queue memory, size, completion destination, set selection and creation errors. The example uses ordinary host memory.'), True, extras=[reference('3.3','114','PCIe 的多個 SQ 可以使用同一個 CQ；共用完成佇列不會取代各 SQ 的 Set 關聯。','Multiple PCIe SQs may share a CQ; the shared completion destination does not replace their individual set associations.')])

unit('routing',('讓每筆 I/O 的 Set 與 SQ 關聯一致','Keep each I/O’s set consistent with its SQ association'),
 ('要取得 SQ Associations 的效益，主機必須把每個 I/O SQ 關聯到某個 NVM Set，並只把命令送入與該命令 NSID 所屬 Set 相符的 SQ。不遵守操作規則可能影響 Predictable Latency；這不是一個由本節定義的強制拒絕其他 Set 命令的存取保護機制。',
  'To obtain the benefits of SQ Associations, the host must associate each I/O submission queue with an NVM Set and send commands only to queues matching the set containing the command’s NSID. Violating the operating rules may affect Predictable Latency; this section does not define mandatory access-control rejection of mismatched commands.'),
 '8.1.28','759',
 ('已知 NSID11／12→Set7、NSID21→Set9，且 SQ3／SQ4→Set7、SQ5→Set9。NSID11 可以選 SQ3 或 SQ4；NSID21 應選 SQ5。即使三個 SQ 都把完成項目送往 CQ2，也不會改變這個分流判斷。',
  'Given NSIDs 11/12→set 7, NSID 21→set 9, SQ3/SQ4→set 7 and SQ5→set 9, NSID11 can use SQ3 or SQ4 while NSID21 should use SQ5. Sharing CQ2 as the completion destination does not change this routing decision.'),
 [('以資料對象為起點','先看 I/O 命令的 NSID，再查這個 namespace 的 NVMSETID，最後從主機建立的關聯中選同一個 Set 的 SQ。不要反過來先找一個空 SQ，就假定它可以承載任何 namespace；這會讓主機提供給控制器的提示與實際工作不一致。'),
  ('一個 Set 可以使用多個 SQ','一個 Create I/O SQ 命令只能填一個 NVMSETID，但主機可以建立多個 SQ，逐一填入同一個 Set 編號。例子裡 SQ3、SQ4 都服務 Set 7。這表示關聯不是一個 Set 只能有一個 SQ，也不表示每個 namespace 必須獨占一個 SQ。'),
  ('不同的關聯錯誤有不同後果','建立時指定不存在的 Set，Figure 578 明定命令中止；建立成功後卻把 Set 9 的命令送入關聯 Set 7 的 SQ，違反的是主機操作規則。§8.1.28 說這可能影響可預測延遲，沒有在此規定每次都回某個錯誤碼，因此不能靠「沒報錯」證明路由正確。'),
  ('CQ 共用不等於 Set 混用','SQ3 與 SQ5 可以都使用 CQ2；CQ 裡的完成項目仍用命令與佇列識別資訊對應原命令。SQ→CQ 是結果回報路徑，SQ→Set 是工作分組提示。要判斷主機是否遵守 SQA 規則，應比較 Set 歸屬，不是比較 CQID。'),
  ('關聯是在建立時提出的','§8.1.28 的啟用方式是在建立 SQ 時給出關聯，不提供直接改寫既有 SQ 關聯的操作。若要換一套佇列配置，主機可先妥善完成既有工作，再依新的配置建立並使用對應 SQ；不能只修改自己記憶體裡的路由表，就宣稱控制器收到新的 Set 提示。')],
 ('用正文的路由表檢查 NSID→NVM Set→SQ，欄位依據回到 Figure 346 與 Figure 578。','Use the routing table to check NSID→NVM Set→SQ, with the fields supplied by Figures 346 and 578.'))
