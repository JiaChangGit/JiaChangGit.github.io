"""Visuals for scope, bitmap interpretation, typed readback and time boundaries."""
from scripts.nvme_reader_visuals import diagram, box, arrow
from scripts.nvme_directives_visuals import table
from scripts.nvme_rrl_content import bi


def illustration(key, lang='zh'):
    if key == 'rrl-scope':
        return diagram(bi('同一 Set 內共用等級','Namespaces in one set share a level')[lang],
            bi('說明性範例：設定目標是 Set 7，A、B 一起使用 15；C 沿用 Set 9 的 4。若無 NVM Sets，則所有 namespace 共用 subsystem 的一份 RRL。來源：Base §8.1.23、§5.2.30.1.12、Figure 67。',
               'Illustrative example: targeting set 7 gives A/B level 15; C retains set 9’s level 4. Without NVM Sets, all namespaces share one subsystem RRL. Sources: Base §§8.1.23, 5.2.30.1.12 and Figure 67.')[lang], [
            box(20,20,720,70,['NVM subsystem']),
            arrow(190,90,190,140),arrow(565,90,565,140),
            box(20,140,345,95,['NVM Set 7','RRL: 4 → 15'],'command'),
            box(395,140,345,95,['NVM Set 9','RRL: 4'],'object'),
            arrow(190,235,190,285),arrow(565,235,565,285),
            box(20,285,345,100,['namespace A + B','RRL = 15'],'success'),
            box(395,285,345,100,['namespace C','RRL = 4'])],410)
    if key == 'rrl-discover':
        return table(bi('從支援清單走到一個設定值','From a support bitmap to one selected value')[lang],
            bi(['想選的等級','檢查 RRLS=8011h 的哪個 bit','送進 RRL 的值'],
               ['Candidate level','Test in RRLS=8011h','Value encoded in RRL'])[lang],bi([
                ['0','bit 0 = 1，支援','0h'],['4','bit 4 = 1，支援','4h'],
                ['8','bit 8 = 0，不支援','不選此值'],['15','bit 15 = 1，支援','Fh']],
                [['0','Bit 0 = 1: supported','0h'],['4','Bit 4 = 1: supported','4h'],
                 ['8','Bit 8 = 0: unsupported','Do not select'],['15','Bit 15 = 1: supported','Fh']])[lang],
            bi('RRLS 的 bit 位置選一個是／否答案；RRL 則直接保存等級代碼。兩者不能互換。來源：Base Figures 338、485。',
               'The bit position in RRLS selects a yes/no answer; RRL directly encodes the chosen level. They are not interchangeable. Sources: Base Figures 338/485.')[lang])
    if key == 'rrl-get':
        return diagram(bi('同一個 DW0=4，先確認查詢問題','DW0=4: first identify the query')[lang],
            bi('假設 SSFS=1，兩次都成功。SEL=0 的回覆採 RRL 格式；SEL=3 的回覆採能力格式。能力查詢不會改變目前等級。來源：Base Figures 198、201、485。',
               'Assume SSFS=1 and successful completions. SEL=0 uses the RRL layout; SEL=3 uses capability bits. A capability query does not change the current level. Sources: Base Figures 198/201/485.')[lang], [
            box(20,20,720,70,['Get Features · FID 12h · CQE DW0 = 00000004h']),
            arrow(190,90,190,160),arrow(565,90,565,160),
            box(20,160,345,105,['SEL = 0',bi('問目前值','Current value')[lang]],'command'),
            box(395,160,345,105,['SEL = 3',bi('問能力','Supported capabilities')[lang]],'command'),
            arrow(190,265,190,325),arrow(565,265,565,325),
            box(20,325,345,105,['DW0[3:0] = 4','RRL = 4'],'success'),
            box(395,325,345,105,['CHANG = 1','NSSPEC = 0 · SVBL = 0'],'success')],455)
    if key == 'rrl-activation':
        return diagram(bi('設定成功是後續提交的保證界線','Successful Set completion defines the boundary')[lang],
            bi('時間由上往下。A 在界線前提交，不能保證採用新設定；B 在成功後才提交，必須採用新設定。這張圖沒有替 RRL 指定固定完成時間。來源：Base §5.2.30.1。',
               'Time runs downward. A was submitted before the boundary and is not guaranteed to use the new value. B is submitted after success and must use it. No fixed completion time is implied. Source: Base §5.2.30.1.')[lang], [
            box(20,20,720,80,[bi('提交 Read A；A 仍可能在執行','Submit read A; A may remain outstanding')[lang],bi('新設定是否套用到 A：不保證','New setting for A: not guaranteed')[lang]]),
            arrow(380,100,380,145),
            box(20,145,720,70,[bi('提交 Set Features：RRL = 15','Submit Set Features: RRL = 15')[lang]],'command'),
            arrow(380,215,380,260),
            box(20,260,720,70,[bi('Set 成功完成','Set completes successfully')[lang]],'decision'),
            arrow(380,330,380,375),
            box(20,375,720,80,[bi('此後才提交 Read B','Submit read B after this completion')[lang],bi('B 必須使用新設定','B must use the new setting')[lang]],'success')],480)
    if key == 'rrl-lifetime':
        return table(bi('相同 current=15，重設後為何不同？','Why can current=15 have different reset outcomes?')[lang],
            bi(['Feature 能力與原值','這次事件的判斷條件','之後的 current'],
               ['Capability and prior values','Applicable event condition','Resulting current'])[lang],bi([
                ['不可保存；current=15','Power cycle 或 reset：FID12h 具持續性','15'],
                ['可保存；current=15、saved=4','Figure126 的全體範圍重設','4：取 saved'],
                ['可保存；current=15、沒有 saved','Figure126 的全體範圍重設','4：取 default'],
                ['可保存；current=15、saved=4','Figure127 的局部範圍重設；Set／subsystem scope','15：維持目前值']],
                [['Non-saveable; current=15','Power cycle or reset: FID12h is persistent','15'],
                 ['Saveable; current=15, saved=4','Whole-subsystem reset under Figure126','4: from saved'],
                 ['Saveable; current=15, no saved value','Whole-subsystem reset under Figure126','4: from default'],
                 ['Saveable; current=15, saved=4','Subset reset under Figure127; set/subsystem scope','15: unchanged']])[lang],
            bi('先查可保存性，再確認配置與重設範圍。表內都是說明性原值；兩種重設表的完整適用條件在相鄰段落說明。來源：Base §4.4、Figures 126／127／466。',
               'Check saveability, then the configuration and reset scope. Prior values are illustrative; adjacent text states the applicability of both reset tables. Sources: Base §4.4 and Figures 126/127/466.')[lang])
    return ''
