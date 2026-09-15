"""Diagrams used where positions or state transitions clarify the lesson."""
from scripts.nvme_reader_visuals import diagram,box,arrow

def illustration(key):
    if key=='adminio-features':
        from scripts.nvme_course_visuals import course_illustration
        return course_illustration('apst-state-machine')
    if key=='adminio-boot':
        return diagram('Log 的起點與映像的起點相差 16 bytes',
          '說明性範例：每一行從自己的起點量位移，寬度不按 bytes 比例。映像 offset 4096 對應 Log LPO=4112；讀 4096 bytes 的 NUMD=1023。',[
          box(20,35,140,70,['Log header','bytes 0–15'],'command'),
          box(160,35,570,70,['Boot Partition Data','從 Log byte 16 開始']),
          box(160,155,285,65,['image bytes 0–4095']),
          box(445,155,285,65,['image bytes 4096–8191'],'success'),
          '<text x="160" y="260" font-size="16">image offset 0</text>',
          '<text x="445" y="260" font-size="16">image offset 4096 → LPO 4112</text>'
          ],295)
    if key=='adminio-telemetry':
        return diagram('Data Area 2 包含 Data Area 1',
          '說明性範例：Header 位於 block 0；Area 1 含 blocks 1–65，Area 2 含 blocks 1–1000。橫軸示意包含關係，不按比例。取 Area 2 時，已讀過的 1–65 不須當成另一塊相加。',[
          box(20,40,140,200,['Header','block 0'],'command'),
          box(180,40,210,75,['Area 1','blocks 1–65']),
          box(180,165,550,75,['Area 2：blocks 1–1000'],'success'),
          '<path d="M390,120 L390,165" class="v-line"/>',
          '<text x="530" y="140" text-anchor="middle" font-size="16">新增部分：66–1000</text>'
          ],275)
    if key=='adminio-namespace':
        return diagram('同一個 namespace，可有不同 controller 的附加關係',
          '說明性範例：NSID=7 已建立，A、B 原本都附加。Detach A 移除上方這一條關係，B 的關係與 namespace 物件仍在。虛線表示已移除的關係，不代表資料被刪除。',[
          box(25,30,220,75,['Controller A']),box(25,180,220,75,['Controller B']),
          box(465,95,265,95,['Namespace','NSID = 7'],'success'),
          '<path d="M245,67 L385,67 L385,115 L465,115" class="v-line" stroke-dasharray="7 6"/>',
          '<text x="350" y="35" text-anchor="middle" font-size="16">Detach A</text>',
          '<path d="M245,217 L385,217 L385,170 L465,170" class="v-line"/>',
          '<text x="350" y="255" text-anchor="middle" font-size="16">B 仍可存取</text>'
          ],290)
    if key=='adminio-queues':
        return diagram('Delete SQ 的成功 CQE 決定舊命令的最後界線',
          '說明性範例：CID 10 已有自己的 CQE；11、12 尚無 CQE。Delete SQ 成功後，11、12 隱含以 Command Aborted due to SQ Deletion 完成，控制器之後不再送出它們的完成狀態。箭頭是時間順序。',[
          box(20,55,210,100,['SQ 3：CID 10','先回成功 CQE']),
          box(275,55,210,100,['Delete SQ 3','回成功 CQE'],'command'),
          box(530,55,210,100,['CID 11、12','隱含中止'],'success'),
          arrow(230,105,275,105),arrow(485,105,530,105),
          '<text x="380" y="205" text-anchor="middle" font-size="16">成功刪除後，不再等待 11、12 各自的 CQE</text>'
          ],245)
    if key=='adminio-selftest':
        return diagram('測試啟動完成與測試結果，是兩個時點',
          '說明性範例：命令先成功，測試在背景繼續；LID 06h 的 current 欄位追蹤正在進行的作業，歷史 results 記錄已结束的作業。最前面的舊結果不會因新測試剛開始，就自動變成新測試結果。',[
          box(20,35,220,85,['送出 extended test','STC = 2'],'command'),
          box(280,35,200,85,['命令成功','背景測試開始']),
          box(520,35,220,85,['目前進度 50%','測試仍在進行']),
          arrow(240,78,280,78),arrow(480,78,520,78),
          box(280,200,460,80,['作業結束 → current = none','最新 result：成功／中止／失敗'],'success'),
          arrow(630,120,630,200)
          ],320)
    if key=='adminio-dataset':
        return diagram('範圍清單不變，旗標描述的意圖改變',
          '說明性範例：2 個 16-byte 描述子，NR=1，總 buffer=32 bytes。IDR、IDW 與 AD 是命令旗標，套用到提供的範圍；改旗標不會把 LLB 的 4、6 變成另一種長度。',[
          box(20,30,350,80,['Range 0：SLBA = 200','LLB = 4 → LBAs 200–203']),
          box(390,30,350,80,['Range 1：SLBA = 500','LLB = 6 → LBAs 500–505']),
          box(20,170,220,90,['IDR = 1','預期整段一起讀'],'command'),
          box(270,170,220,90,['IDW = 1','預期整段一起寫'],'command'),
          box(520,170,220,90,['AD = 1','可解除配置'],'decision')
          ],300)
    if key=='adminio-sanitize':
        return diagram('先接受要求，再由 Log 確認背景結果',
          '圖示清除的共同時間順序：SANACT 選支援方法，命令成功後背景作業繼續。SSTAT 的最終狀態才回答結果；EMVS 另可要求進入驗證狀態，不能把「清除處理結束」一律畫成回到 Idle。',[
          box(20,45,200,90,['Sanitize 命令','要求支援的方法'],'command'),
          box(280,45,200,90,['命令成功','背景作業進行']),
          box(540,45,200,90,['LID 81h','狀態與有效進度']),
          arrow(220,90,280,90),arrow(480,90,540,90),
          box(70,225,290,85,['正常完成／失敗','以最終狀態辨認'],'success'),
          box(400,225,290,85,['EMVS 的驗證要求','另看 SSI.SANS 狀態'],'decision'),
          '<path d="M640,135 L640,185 L215,185 L215,225" class="v-line"/>',
          '<path d="M545,185 L545,225" class="v-line"/>'
          ],350)
    return ''
