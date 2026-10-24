"""Deliberate reading routes for one canonical opening scenario per volume."""
from scripts.spec_teaching import reading_route

LEAD_CASES = {'init':'init-01','command':'command-01','identify':'identify-01','io':'io-01',
              'features':'features-01','logs':'logs-01','maintenance':'maintenance-03'}

# A route follows the reader's questions, not a claimed hardware state machine.
ROUTES = {
 'init':[
  (('先確認 PCIe 存取條件','Establish PCIe access'),('從 Command 暫存器讀取 MSE、BME，再由 BAR 找到 NVMe 暫存器空間。先確認這些欄位，後面才有正確的存取位置與條件。','Read MSE and BME in the Command register and locate the NVMe register space through the BAR before checking controller operation.'),['P12','P20']),
  (('再讀 NVMe 能力與配置','Read NVMe capability and configuration'),('先讀 CAP 的能力與限制，再對照 CC 的工作配置；兩張圖分別說明裝置提供什麼，以及軟體選了什麼。','Read CAP for capabilities and limits, then CC for the configuration selected by software.'),['B36','B41']),
  (('最後確認初始化狀態','Check initialization state'),('由 CSTS 確認 controller 狀態，再接到 Admin Queue 與 Identify。這裡先建立觀察順序，完整佇列初始化回到相關教學。','Use CSTS for controller state before proceeding to the Admin Queue and Identify. The related lesson explains full queue initialization.'),['B42'])],
 'command':[
  (('先看這筆完成項目是否有效','Check whether the completion is new'),('先從 CQE 的 DW3 找到 Phase Tag，依這一輪預期值判讀。只有本輪的新完成項目才接著配對命令。','Locate the phase tag in CQE DW3 and compare it with the host’s expected phase before matching a completion.'),['B97','B99']),
  (('用 SQID 與 CID 找回命令','Match SQID and CID'),('由 DW2 取得提交佇列識別值，再由 DW3 取得命令識別值。兩者一起定位同一佇列內尚未完成的命令。','Read the submission-queue identifier from DW2 and command identifier from DW3 to locate an outstanding command in that SQ.'),['B98','B99']),
  (('回到原命令及生命週期','Return to the command and its lifecycle'),('對照原 SQE 的 CID 與當時的佇列配置，再讀完成狀態；保留佇列重建與 CID 重用的時間資訊。','Correlate the original SQE and queue configuration, then interpret status with queue-recreation and CID-reuse timing retained.'),['B92','B97'])],
 'identify':[
  (('先選對 Identify 結構','Select the Identify structure'),('由 CNS 總表選擇 controller、已配置清單與活動清單。先確定回覆的對象，再比較數量。','Use the CNS table to select controller information, the allocated list and the active list before comparing counts.'),['B336']),
  (('分別讀數量與附接限制','Read count and attachment limits'),('在 Identify Controller 找 NN、MNAN 與 MAXCNA 的定義及有效條件，再搭配兩份清單的筆數。','Find NN, MNAN and MAXCNA with their validity conditions, then combine them with the two list counts.'),['B338']),
  (('接著確認建立所需資源','Check creation resources'),('Namespace Management 的操作與主機指定欄位說明建立時還要提供什麼。數量名額只是其中一項前提。','The Namespace Management operation and host-specified fields identify additional creation requirements beyond the count limit.'),['B446','N134'])],
 'io':[
  (('先找原子性參數的關係','Locate atomicity parameters'),('先由 Single Atomicity Mode 的參數表分清正常與斷電情況，再看本例採用 controller 還是 namespace 的值。','Distinguish normal and power-failure parameters in the Single Atomicity Mode table and determine which scope supplies the values.'),['N4','N123']),
  (('確認本筆 Write 的區塊數','Determine the Write block count'),('讀取 Write 的 NLB；本例 NLB=7 表示 8 個區塊，再和已確認的原子單位比較。','Read Write NLB. Here NLB=7 requests eight blocks, which are compared with the established atomic units.'),['N71']),
  (('保留不同事件的保證條件','Retain event-specific conditions'),('回到原子性參數表，分別解釋正常與斷電時整筆寫入的保證。成功完成、持久性與原子性各依相關規則判讀。','Return to the atomicity parameters to explain whole-write guarantees separately for normal operation and power failure.'),['N4'])],
 'features':[
  (('先看請求中的選擇欄位','Read the request selectors'),('Get Features 的 FID 選功能，SEL 選回覆種類。先保留這兩個值，才能選對 DW0 的格式。','FID selects the feature and SEL selects the response kind; retain both to select the correct DW0 format.'),['B198']),
  (('SEL=3 時讀能力格式','Decode the SEL=3 capability response'),('這張圖專門解釋 SEL=3 的 DW0：CHANG、NSSPEC 與 SVBL。先按此格式解讀 00000005h。','This figure defines CHANG, NSSPEC and SVBL in DW0 for SEL=3; decode 00000005h using that format.'),['B201']),
  (('再接到功能自身的工作值','Proceed to the feature value'),('從 Feature 清單找到該 FID 的定義，再以 SEL=0 讀目前值。能力 bitmap 與工作值使用不同回覆格式。','Find the FID’s own definition in the feature list, then retrieve its current value using SEL=0.'),['B466','B198'])],
 'logs':[
  (('先辨識每個量的用途','Identify each reported quantity'),('在 SMART／Health 圖表分別找到 Percentage Used、Available Spare 與門檻，先讀各自的定義及單位。','Locate Percentage Used, Available Spare and its threshold in SMART/Health and read their individual definitions and units.'),['B213']),
  (('把警告和對應數值配起來','Correlate warnings with values'),('回到同一張表的 Critical Warning，對照備援空間的警告位元，再讀 Available Spare 與門檻。','Correlate the spare critical-warning bit with Available Spare and its threshold in the same table.'),['B213']),
  (('分項說明觀察結果','Explain the observations separately'),('溫度、壽命估計與備援警告各自列出；需要判斷目前 I/O 行為時，再補實際操作資訊。','Report temperature, endurance estimate and spare warnings separately, adding observed I/O behavior when that is the question.'),['B213'])],
 'maintenance':[
  (('先查目前版本與啟用能力','Read the running revision and activation capability'),('Identify Controller 的 FR 說明目前執行的版本，FRMW 則提供韌體槽位與啟用能力。','Identify Controller FR reports the running revision; FRMW supplies slot and activation capabilities.'),['B338']),
  (('再查目前與下次啟用槽位','Read current and next-active slots'),('由 Firmware Slot Information 的 AFI 讀 CAFS、NAFS，再對照各槽位版本字串。','Read CAFS and NAFS from Firmware Slot Information AFI and compare the slot revision strings.'),['B215']),
  (('接回 Commit 的動作與完成條件','Connect the Commit action and completion conditions'),('查看 Firmware Commit 的 action 與完成規則，確認版本何時生效；適用的啟用步驟完成後再重新讀取版本。','Use the Firmware Commit action and completion rules to determine when activation occurs, then reread the revision afterward.'),['B187'])],
}

def lesson_route(case,language,register,standalone=False):
    if LEAD_CASES[case['topic']] != case['id']:
        return ''
    index=0 if language=='zh' else 1
    steps=[]
    for titles,explanations,keys in ROUTES[case['topic']]:
        links=[]
        for key in keys:
            row=register[key]
            prefix={'B':'Base 2.4','N':'NVM Command Set 1.3','P':'NVMe over PCIe Transport 1.4'}[key[0]]
            target='#figure-'+key.lower()
            if row['group'] != case['topic']:
                target=(row['group']+'.html' if standalone else '/nvme/figure-reference/'+row['group']+'/'+('zh-tw' if language=='zh' else 'en')+'/')+target
            links.append((prefix+' · Figure '+str(row['number']),target))
        steps.append((titles[index],explanations[index],links))
    return reading_route('route-'+case['id'],'這個情境要連起哪些規格圖表？' if language=='zh' else 'Which figures connect this scenario?',steps,language)
