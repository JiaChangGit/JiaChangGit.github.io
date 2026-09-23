"""Register the three editions and the post-only forward Spec route."""
from scripts.nvme_report_extension import bi,install_report,render_forward_route
from scripts.nvme_nwp_content import REPORT_ID,UNITS
from scripts.nvme_nwp_terms import TERMS

CONFIG=dict(id=REPORT_ID,prefix='NWP',date='2026-09-23',
 title=bi('NVMe Namespace Write Protection：狀態、控制與命令行為',
          'NVMe Namespace Write Protection: States, Controls, and Command Behavior'),
 range=bi('Base §8.1.18、§5.2.30.1.38（FID 84h）','Base §§8.1.18 and 5.2.30.1.38 (FID 84h)'),
 context=dict(intro=bi(
 '一份已寫好的資料要繼續提供讀取，又要避免後續命令改動它，可以對所在的 namespace 設定寫入保護。Namespace Write Protection 不只是一個開關：它有可解除、直到斷電、永久等不同狀態，並把裝置支援、進入許可與實際保護分開。本篇把這些關係接到 FID 84h，最後說明保護如何改變命令處理。',
 'A completed dataset may need to remain readable while later commands are prevented from modifying its namespace. Namespace Write Protection provides reversible, until-power-cycle and permanent states, separating hardware support, entry permission and actual protection. This report connects those distinctions to FID 84h and explains their consequences for command processing.'),
 axes=bi([
 ['保護的對象與邊界','設定跟著 namespace，所有附接它的控制器都要遵守。先分清資料對象與傳送命令的控制器，再看會影響多個 namespace 的操作。'],
 ['用事件追蹤狀態','四種狀態各有允許的進入與離開路徑。Set Features、控制器重設與 power cycle 造成的結果不同，圖上的箭頭必須帶著事件讀。'],
 ['從能力走到成功設定','NWPC 回答能不能支援，WPC 決定特定進入要求是否獲准，WPS 回報目前狀態。設定成功還包含將既有寫入快取提交到媒體。'],
 ['保護後如何使用與觀察','Read、Flush、管理命令各有處理規則；跨 namespace 的操作也受影響。用目前 WPS、完成狀態與健康警告回答各自的問題。']],
 [['Object and enforcement boundary','The setting belongs to a namespace and is enforced by every attached controller. Distinguish the storage object from the command’s controller, then consider operations affecting multiple namespaces.'],
 ['Track states through events','Each state has specific entry and exit paths. Set Features, controller reset and power cycling are distinct triggers, so read every arrow together with its event.'],
 ['From capability to successful configuration','NWPC advertises support, WPC permits particular entry requests, and WPS reports current state. Successful protection also commits existing volatile write-cache contents to media.'],
 ['Use and observe protected storage','Read, Flush and management commands have different rules, including cross-namespace effects. Current WPS, completion status and health warnings answer different questions.']]),
 background=bi([
 '讀者已學過 OS 與 Computer Organization，並了解 SSD 基本概念。本文使用 namespace 7／8 與控制器 A／B 作為說明性範例；數值不代表裝置一定具備這些配置。',
 '先掌握四種狀態，再讀支援與控制位，接著完成一個設定案例；最後把狀態套回實際命令。欄位說明按相關概念分組，可從正文直接連到對應圖表。'],
 ['Assumes operating systems, computer organization and basic SSD concepts. Namespaces 7/8 and controllers A/B are illustrative rather than assumed device configurations.',
 'Start with the four states, examine support and control bits, complete a configuration example, and apply the result to commands. Related fields are grouped and linked from the main explanations.'])),
 connections=bi([
 '全文以 namespace 7 的資料集為例：先決定需要哪種保護與解除方式，再確認裝置能否接受該轉換，等待設定成功，最後解釋哪些操作還能執行。每個欄位都有一個具體要回答的問題。',
 '最容易混淆的三組關係是：支援能力與進入許可、不可保存與跨斷電保留、namespace 保護狀態與全體媒體健康警告。後面的對比會分別處理它們。'],
 ['Follow the dataset in namespace 7: choose a protection and release policy, verify that the transition is available, wait for successful configuration, and explain which operations remain possible. Each field answers a concrete question.',
 'Keep three distinctions in view: support versus entry permission, non-saveability versus persistence, and namespace protection versus an all-media health warning.']),
 questions=[])

for key,qz,qe,az,ae,src in [
 ('reset','WPS=2，沒有斷電的控制器重設後，能用 Set WPS=0 解除嗎？',
  'After a controller reset without power cycling, can Set WPS=0 release WPS=2?',
  '不能。這種重設維持狀態2，Set不能改變它；power cycle才沿著圖上的特殊箭頭回到0。WPUPCC清零只是關閉之後的進入許可，不是解除現有保護。',
  'No. That reset retains state 2, which Set cannot change. A power cycle follows the special return arrow to 0. Clearing WPUPCC closes future entry permission; it does not release existing protection.', ['TRANSITIONS','CONTROLS-3']),
 ('support','NWPC=07h、PWPC=1，是否代表任何 namespace 現在都能進入永久保護？',
  'Do NWPC=07h and PWPC=1 mean every namespace can now enter Permanent Write Protect?',
  '還要看目前狀態。0或1才有進入3的Set路徑；原本在2時，改成3仍會被拒絕。NWPC是支援，PWPC是許可，兩者都不取代狀態機。',
  'The current state still matters. States 0 and 1 have a Set path to 3; changing state 2 to 3 is rejected. Support and entry permission do not replace the state machine.', ['CONTROLS','TRANSITIONS']),
 ('capability','成功的能力查詢回 DW0=6，能否說目前 WPS=6，而且可解除永久保護？',
  'If a successful capability query returns DW0=6, is WPS=6 and can permanent protection be released?',
  '兩個結論都不對。SEL3的6解成CHANG1、NSSPEC1、SVBL0；CHANG表示此Feature有可變更的值，不保證目前值可改。查WPS要另用SEL0。',
  'Neither follows. With SEL=3, 6 means CHANG=1, NSSPEC=1 and SVBL=0. CHANG describes the existence of changeable values, not permission to change the current value. Query WPS separately with SEL=0.', ['CONFIGURE-2']),
 ('flush','保護後 Flush 為什麼成功卻不寫回資料？',
  'Why does Flush succeed without writing data after protection?',
  '轉入保護時已要求提交該namespace全部揮發性寫入快取資料與metadata。因此這裡的成功不代表還有一次額外寫入，也不能反推其他未受保護namespace的Flush同樣無作用。',
  'The transition already commits all associated volatile write-cache data and metadata. Success here does not imply another write, and the rule cannot be extended to Flush on an unprotected namespace.', ['CONFIGURE','COMMANDS']),
 ('scope','7受保護、8未受保護，把 Format NVM 的 NSID 填8就一定能執行嗎？',
  'If 7 is protected and 8 is not, does naming 8 guarantee that Format NVM can proceed?',
  '不一定。還要判斷這次format真正涵蓋哪些namespace；若也會修改7，就必須因保護而拒絕。保護依實際影響判斷，不只看命令上的目標編號。',
  'No. Examine the actual formatting scope. If it would modify 7, protection requires rejection. The effect matters in addition to the named target.', ['COMMANDS']),
]:CONFIG['questions'].append(dict(key=key,question=bi(qz,qe),answer=bi(az,ae),sources=src))

def install(reports,titles,modules,glossaries,images):
    install_report(CONFIG,UNITS,TERMS,reports,titles,modules,glossaries,images)

ROUTE=[
 (538,539,'5.2.30.1.38','5.2.30.1.39',bi('從 Namespace Write Protection Config 開始，用 Figure541 讀WPS編碼，再說不可保存、沒有default、拒絕轉換的條件，以及下一頁的快取提交。',
 'Start at Namespace Write Protection Config. Use Figure541 for WPS, then cover non-saveability, the absent default, rejected transitions and the cache-commit requirement on the next page.')),
 (690,692,'8.1.18','8.1.19',bi('從 Namespace Write Protection 標題開始。Figure735比較四種狀態，Figure736沿箭頭解釋事件，Theory of Operation接能力與共享保護，Figure737連同下一頁三項註腳說明命令。',
 'Start at Namespace Write Protection. Compare states in Figure735, follow event-labeled transitions in Figure736, connect capability and shared enforcement in Theory of Operation, and read Figure737 with all three footnotes on the next page.')),
 (718,718,'8.1.24 · Figure756 byte2','Figure757',bi('最後只補看Device Configuration Block的WPC byte2，對照PWPC、WPUPCC與重設清零。不要從此展開其餘RPMB訊息表。',
 'Finish with only WPC byte2 in the Device Configuration Block: PWPC, WPUPCC and their reset-to-zero behavior. Stop before the RPMB message-type table.')),
]

def render_route(reader):return render_forward_route(reader,ROUTE).replace("§Figure757", "Figure757")
