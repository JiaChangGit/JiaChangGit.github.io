"""Original teaching diagrams; no source PDF image is embedded in the site."""
from html import escape


def diagram(figure, language):
    if figure['report_id'] != 'nvm-command-set-1.3' or figure['source_id'] != 'NVME-NVM-CS-1.3':
        return None
    n = int(figure['number'])
    if n not in {8,10,42,153,154,164,166,167,168,169,170,171,172,173,183,191,195,197,202}:
        return None
    en = language == 'en'
    parts = []
    aid = 'nvmcs-diagram-' + str(n)
    def label(x,y,text,size=19):
        parts.append(f'<text x="{x}" y="{y}" text-anchor="middle" font-size="{size}">{escape(text)}</text>')
    def box(x,y,w,h,text,role='object'):
        parts.append(f'<rect class="v-{role}" x="{x}" y="{y}" width="{w}" height="{h}" rx="8"/>')
        for i,line in enumerate(text.split('|')):
            label(x+w/2,y+h/2+(i-(len(text.split('|'))-1)/2)*25+6,line)
    def edge(x1,y1,x2,y2):
        parts.append(f'<path class="v-line" d="M{x1},{y1} L{x2},{y2}" marker-end="url(#{aid})"/>')
    if n in {8,10}:
        title = 'MAM: independent atomic subranges' if en else 'MAM：各段原子，不是整筆 transaction'
        label(410,35,'Decoded boundary size = 8; offset = 0')
        for i in range(16):
            x=26+i*48
            box(x,75,44,55,str(i),'success' if i>=4 else 'object')
        parts.append('<path class="v-line" d="M408,55 V225"/>')
        box(218,153,182,65,'LBA 4..7|Atomic A','command')
        box(418,153,374,65,'LBA 8..15|Atomic B','decision')
        label(410,262,'Write SLBA=4, decoded count=12; A and B may have different outcomes',17)
    elif n==42:
        title = 'Copy preserves descriptor order at the destination' if en else 'Copy：依來源描述順序接成連續目的範圍'
        box(30,45,240,65,'Source range 0|LBA 10..11','command')
        box(30,185,240,65,'Source range 1|LBA 80..82','command')
        box(480,45,290,65,'Destination 100..101','success')
        box(480,185,290,65,'Destination 102..104','success')
        edge(270,77,480,77);edge(270,217,480,217)
        label(410,153,'SDLBA=100; decoded counts 2 + 3 = 5 blocks')
    elif n in {153,154}:
        title = 'Metadata placement' if en else 'Metadata 的兩種傳輸位置'
        label(410,30,'Extended LBA: one buffer')
        for x,t,w,r in [(30,'Data 0',240,'object'),(270,'MD 0',130,'decision'),(410,'Data 1',240,'object'),(650,'MD 1',130,'decision')]: box(x,50,w,60,t,r)
        label(410,155,'Separate metadata: matching data and metadata buffers')
        box(30,175,365,65,'DPTR: Data 0 | Data 1','command')
        box(425,175,365,65,'MPTR: MD 0 | MD 1','decision')
        label(410,282,'One command uses one placement mechanism; align the same block indices',17)
    elif n in {164,166,167,168,169,170,171,172,173}:
        title = 'Storage/Reference partition before Dword packing' if en else '先切 Storage／Reference，再封裝 Dwords'
        label(410,32,'Example: 64b Guard, STS=18, reference width=30')
        box(30,58,285,68,'Storage: 18 bits|high-order space','decision')
        box(315,58,475,68,'Reference: 30 bits|low-order space','object')
        box(30,166,285,68,'CDW3[15:0]|Storage[17:2]','command')
        box(338,166,185,68,'CDW14[31:30]|Storage[1:0]','decision')
        box(544,166,246,68,'CDW14[29:0]|Reference[29:0]','success')
        label(410,281,'Storage=0x12345, Reference=0x2A → CDW3=0x48D1, CDW14=0x4000002A',16)
    elif n in {183,191}:
        title = 'Configuration and runtime state have different lengths' if en else 'Configuration 與 runtime state 長度不同'
        label(410,31,'Figure 183: 412 bytes, configured once')
        box(30,55,580,65,'RECCS: bytes 0..363 (364 bytes)','command')
        box(620,55,170,65,'RENSCS|48 bytes','object')
        label(410,164,'Figure 191: 64 + 4 × NVMECSS bytes')
        box(30,187,230,65,'Fixed header|64 bytes','decision')
        box(280,187,510,65,'Variable NVMECS|NVMECSS dwords; nested VER=1','success')
        label(410,293,'NVMECSS=0: variable field absent; CP describes suspension evidence',17)
    elif n in {195,197}:
        title = 'Rate Limiting capability graph' if en else 'Rate Limiting 能力圖：共享節點'
        if n==195:
            # One port, two controllers, each accessing both Endurance Groups.
            edge(215,150,320,70);edge(215,150,320,230)
            edge(490,70,600,70);edge(490,70,600,230)
            edge(490,230,600,70);edge(490,230,600,230)
            box(35,113,180,75,'Port 0','command')
            box(320,35,170,70,'Controller 0');box(320,195,170,70,'Controller 1')
            box(600,35,185,70,'EG 1','success');box(600,195,185,70,'EG 2','success')
        else:
            edge(215,70,320,70);edge(215,230,320,230)
            edge(490,70,600,150);edge(490,230,600,150)
            box(35,35,180,70,'Port 0','command');box(35,195,180,70,'Port 1','command')
            box(320,35,170,70,'Controller 0');box(320,195,170,70,'Controller 1')
            box(600,113,185,75,'Shared EG 1','success')
        label(410,303,'Equal access capabilities: share descriptor; different capabilities: separate descriptors',16)
    else:
        title = 'Token bucket admission and completion' if en else 'Token bucket：准入與完成分開判斷'
        box(25,100,180,75,'Queued command','command')
        box(300,15,220,60,'Periodic token refill','object')
        box(300,105,220,75,'Enough tokens?','decision')
        box(605,105,190,75,'Process portion','success')
        box(300,220,220,65,'Wait; retain command','failure')
        edge(205,137,300,137);edge(410,75,410,105);edge(520,137,605,137);edge(410,180,410,220)
        label(568,125,'Yes',17);label(435,206,'No',17)
        label(410,324,'All required buckets admit work; CQE only after the entire command is processed',16)
    desc = 'Original teaching example. Exact field conditions and source citations appear in the adjacent worksheet.' if en else '自行重畫的教學示意；確切欄位條件與來源定位見相鄰工作紙。'
    return f'<svg viewBox="0 0 820 350" role="img" data-visual-kind="mechanism" aria-label="{escape(title)}"><title>{escape(title)}</title><desc>{escape(desc)}</desc><defs><marker id="{aid}" markerWidth="9" markerHeight="7" refX="8" refY="3.5" orient="auto"><path d="M0,0 L0,7 L8,3.5 z" class="v-arrow"/></marker></defs>'+''.join(parts)+'</svg>'
