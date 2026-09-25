"""Diagrams for lifecycle and byte relationships; tables only where comparison helps."""
from scripts.nvme_report_extension import bi
from scripts.nvme_reader_visuals import diagram,box,arrow
from scripts.nvme_directives_visuals import table

def illustration(key,lang='zh'):
    def txt(zh,en):return bi(zh,en)[lang]
    if key=='pel-context':
        return diagram(txt('一次分段讀取：固定集合、核對後釋放','One multipart retrieval: fix, verify, release'),
          txt('箭頭表示主機讀取順序。context仍可能因reset或保留期限失去；GNUM變化表示這次內容可能不一致，應重新取得。ACT3沿用舊context時不自動納入新事件。來源：Base §5.2.13.1.14、Figure232。',
              'Arrows show host retrieval order. Reset or retention expiry can lose a context; changed GNUM calls for rereading. ACT3 reuse does not incorporate later events. Source: Base §5.2.13.1.14, Figure232.'),[
          box(30,20,700,75,[txt('確認支援，協調 context 的使用','Check support and coordinate context use')],'command'),arrow(380,95,380,130),
          box(30,130,700,90,[txt('ACT1 建立，或 ACT3 建立／沿用','ACT1 establish, or ACT3 establish/reuse'),txt('讀 header：TLL、GNUM、RCE','Read header: TLL, GNUM, RCE')],'command'),arrow(380,220,380,255),
          box(30,255,700,90,[txt('ACT0：按 offset 分段讀同一份集合','ACT0: read chunks from the fixed event set'),txt('新事件另行保存，不加入目前集合','New events are logged outside this context')]),arrow(380,345,380,380),
          box(30,380,700,90,[txt('ACT0 重讀 header，比較 GNUM','ACT0 reread header and compare GNUM'),txt('變了：重新取得；沒變：完成一致性核對','Changed: reread; unchanged: finish checking')],'decision'),arrow(380,470,380,505),
          box(30,505,700,75,[txt('ACT2 釋放；不刪除持久事件歷史','ACT2 release; persistent history remains')],'success')],600)
    if key=='pel-layout':
        return diagram(txt('一筆事件：不要把 VSI 重複加進總長','One event: count VSI only once'),
          txt('說明性算例：起點512、EHL21、VSIL4、EL20。圖示寬度為排版用，不按byte數比例。上排是結構，下排是相對log起點的實際位置。來源：Base Figure234。',
              'Illustration: start512, EHL21, VSIL4, EL20. Widths are schematic, not proportional to byte counts. Positions are relative to the log origin. Source: Base Figure234.'),[
          box(15,20,255,100,['Header = EHL + 3','24 bytes'],'command'),
          box(285,20,190,100,['VSI = VSIL','4 bytes']),
          box(490,20,255,100,['ED = EL − VSIL','16 bytes'],'success'),
          box(15,155,255,75,['512 … 535']),box(285,155,190,75,['536 … 539']),box(490,155,255,75,['540 … 555']),
          box(30,280,700,75,[txt('下一筆 = 512 + 24 + 20 = 556','Next record = 512 + 24 + 20 = 556')],'decision')],385)
    if key=='pel-health':
        return table(txt('三種事件，回答三個問題','Three events answer different questions'),
          txt(['事件','保存什麼','可以回答什麼'],['Event','Preserved data','Question answered']),
          bi([['01h SMART','512-byte健康快照','當時的健康與累計量'],['0Ch Telemetry','診斷資料的前512-byte header','當時捕捉了哪一份資料，邊界為何'],['0Dh Thermal','門檻代碼與相對溫差','跨過哪種門檻或改變哪種熱管理狀態']],
             [['01h SMART','512-byte health snapshot','Historical health and counters'],['0Ch Telemetry','First512-byte diagnostic header','Which capture and which boundaries'],['0Dh Thermal','Threshold code and relative difference','Which crossing or thermal-control change']])[lang],
          txt('Telemetry事件未保存資料blocks；Thermal事件也不是另一份完整SMART。來源：Base Figures237、254、255。',
              'Telemetry blocks are absent, and a thermal event is not another full SMART snapshot. Sources: Base Figures237,254,255.'))
    if key=='pel-namespace':
        return diagram(txt('同一個值，來源與事件位置不同','The same value moves to a different offset'),
          txt('Create取主機輸入、單一Delete取NVM Identify，兩者的FLBAS／DPS來源位置相同。Delete All則保留，不能做這種有效值解讀。來源：Base247；NVM112、123、134。',
              'Create uses host input and single Delete uses NVM Identify; both share these source offsets. Delete All reserves the fields. Sources: Base247; NVM112,123,134.'),[
          box(20,30,310,100,['Source byte26','FLBAS = 12h'],'command'),arrow(330,80,430,80),box(430,30,310,100,['Event byte32','FLBAS = 12h'],'success'),
          box(20,165,310,100,['Source byte29','DPS = 01h'],'command'),arrow(330,215,430,215),box(430,165,310,100,['Event byte33','DPS = 01h'],'success'),
          box(25,310,710,95,[txt('format index2 · 延伸metadata · PI Type1','Format index2 · extended metadata · PI Type1'),txt('數值12h不是LBA大小18 bytes','12h does not mean an 18-byte LBA')],'decision')],430)
    if key=='pel-sanitize':
        return table(txt('清除事件的名稱，與它真正證明的進度','Sanitize event names and what they establish'),
          txt(['看到的紀錄','可確認的事','還不能說的事'],['Record','Established fact','Not yet established']),
          bi([['09h Start','進入清除處理；保存參數與NSID','清除已完成'],['0Eh Media Verification','已進入媒體驗證；沒有ED','已成功完成；ED內有NSID'],['0Ah Completion + SOS3','操作已進入失敗狀態','SPROGFFFFh就等於成功'],['0Ah Completion + SOS1','此次操作成功完成','之後永遠沒有新資料寫入']],
             [['09h Start','Entered processing; parameters and NSID saved','Operation completed'],['0Eh Media Verification','Entered verification; no ED','Successful completion or NSID in ED'],['0Ah Completion + SOS3','Entered failure state','FFFFh proves success'],['0Ah Completion + SOS1','This operation succeeded','No data can ever be written afterward']])[lang],
          txt('這是結論對比，不是保證每份PEL都包含完整事件配對。來源：Base §§5.2.13.1.14.2.9、.10、.14。',
              'This compares justified conclusions; it does not guarantee complete event pairs. Sources: Base §§5.2.13.1.14.2.9,.10,.14.'))
    if key=='pel-features':
        return diagram(txt('Set Feature ED：用三個參數算出位置','Set Feature ED: locate data using three parameters'),
          txt('純格式算例DWC3、MBC8、LCCDW01，沒有假定某FID一定使用這些欄位。來源：Base Figure253。',
              'Layout-only example: DWC3, MBC8, LCCDW01. No particular FID is assumed to use these fields. Source: Base Figure253.'),[
          box(20,20,340,100,['SFEL · bytes0–3','0008000Bh'],'command'),box(400,20,340,100,['CDW10–12 · bytes4–15','3 × 4 = 12 bytes']),
          box(20,150,340,100,['MBUF · bytes16–23','8 bytes']),box(400,150,340,100,['CCDW0 · bytes24–27','4 bytes'],'success'),
          box(30,295,700,70,['ED = 4 + 12 + 8 + 4 = 28 bytes'],'decision')],390)
    return ''
