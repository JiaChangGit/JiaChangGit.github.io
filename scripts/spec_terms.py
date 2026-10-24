"""Visible reminders at the first two uses, with separate series/language state.

Insertions preserve authored HTML. Ambiguous abbreviations such as SC are
deliberately omitted; these require a context-specific authored explanation.
"""
from html import escape
from html.parser import HTMLParser
import re

COMMON={
 'DMA':('Direct Memory Access，裝置直接存取記憶體','Direct Memory Access, device access to memory'),
 'MMIO':('Memory-Mapped I/O，記憶體映射輸入輸出','Memory-Mapped I/O, mapped device-register access'),
 'BAR':('Base Address Register，基底位址暫存器','Base Address Register'),
 'MSI':('Message Signaled Interrupt，訊息中斷','Message Signaled Interrupt'),
 'MSI-X':('Message Signaled Interrupts Extension，表格式訊息中斷','Message Signaled Interrupts Extension'),
 'PF':('Physical Function，實體功能','Physical Function'),
 'VF':('Virtual Function，虛擬功能','Virtual Function'),
 'SR-IOV':('Single Root I/O Virtualization，單根I/O虛擬化','Single Root I/O Virtualization'),
 'BDF':('Bus／Device／Function，匯流排、裝置與功能識別','Bus/Device/Function'),
 'FLR':('Function Level Reset，以功能為範圍的重設','Function Level Reset'),
}
NVME={**COMMON,
 'SQ':('Submission Queue，提交佇列','Submission Queue'),
 'CQ':('Completion Queue，完成佇列','Completion Queue'),
 'SQE':('Submission Queue Entry，佇列中的命令項目','Submission Queue Entry'),
 'CQE':('Completion Queue Entry，佇列中的完成項目','Completion Queue Entry'),
 'SQID':('Submission Queue Identifier，提交佇列識別碼','Submission Queue Identifier'),
 'CQID':('Completion Queue Identifier，完成佇列識別碼','Completion Queue Identifier'),
 'CID':('Command Identifier，同一提交佇列內的命令識別碼','Command Identifier, unique among outstanding commands in one SQ'),
 'NSID':('Namespace Identifier，邏輯儲存空間識別碼','Namespace Identifier'),
 'LBA':('Logical Block Address，邏輯區塊位址','Logical Block Address'),
 'SLBA':('Starting LBA，起始邏輯區塊位址','Starting Logical Block Address'),
 'PRP':('Physical Region Page，描述資料頁位置的指標','Physical Region Page, a data-page pointer'),
 'SGL':('Scatter Gather List，描述分散資料區段的清單','Scatter Gather List'),
 'PI':('Protection Information，資料保護資訊','Protection Information'),
 'FID':('Feature Identifier，功能識別碼','Feature Identifier'),
 'LID':('Log Page Identifier，紀錄頁識別碼','Log Page Identifier'),
 'CNS':('Controller or Namespace Structure，選擇Identify回傳結構','Controller or Namespace Structure, selecting Identify data'),
 'CSI':('Command Set Identifier，命令集識別碼','Command Set Identifier'),
 'SCT':('Status Code Type，完成狀態代碼類型','Status Code Type'),
 'DNR':('Do Not Retry，命令重試的狀態提示','Do Not Retry, a completion retry indication'),
 'HMB':('Host Memory Buffer，主機記憶體緩衝','Host Memory Buffer'),
 'CMB':('Controller Memory Buffer，控制器記憶體緩衝','Controller Memory Buffer'),
 'PMR':('Persistent Memory Region，持久性記憶體區域','Persistent Memory Region'),
 'APST':('Autonomous Power State Transition，自主電源狀態轉換','Autonomous Power State Transition'),
 'FDP':('Flexible Data Placement，彈性資料放置','Flexible Data Placement'),
}
PCIE={**COMMON,
 'TLP':('Transaction Layer Packet，交易層封包','Transaction Layer Packet'),
 'DLLP':('Data Link Layer Packet，資料鏈結層封包','Data Link Layer Packet'),
 'LTSSM':('Link Training and Status State Machine，鏈結訓練與狀態機','Link Training and Status State Machine'),
 'FC':('Flow Control，流量控制','Flow Control'),
 'LCRC':('Link Cyclic Redundancy Check，鏈結循環冗餘檢查','Link Cyclic Redundancy Check'),
 'ECRC':('End-to-End CRC，端到端循環冗餘檢查','End-to-End Cyclic Redundancy Check'),
 'FEC':('Forward Error Correction，前向錯誤更正','Forward Error Correction'),
 'OHC':('Orthogonal Header Content，Flit模式的擴充標頭內容','Orthogonal Header Content'),
 'TC':('Traffic Class，流量類別','Traffic Class'),
 'VC':('Virtual Channel，虛擬通道','Virtual Channel'),
 'ARI':('Alternative Routing-ID Interpretation，替代路由識別碼解讀','Alternative Routing-ID Interpretation'),
 'ACS':('Access Control Services，存取控制服務','Access Control Services'),
 'ATS':('Address Translation Services，位址轉譯服務','Address Translation Services'),
 'PASID':('Process Address Space ID，程序位址空間識別碼','Process Address Space ID'),
 'PRI':('Page Request Interface，頁面要求介面','Page Request Interface'),
 'AER':('Advanced Error Reporting，進階錯誤回報','Advanced Error Reporting'),
 'DPC':('Downstream Port Containment，下游連接埠錯誤隔離','Downstream Port Containment'),
 'PME':('Power Management Event，電源管理事件','Power Management Event'),
 'RID':('Routing ID，封包使用的路由識別碼','Routing ID, the packet routing identity'),
 'DW':('Double Word，4 bytes的資料單位','Double Word, a four-byte unit'),
 'PAM4':('Pulse Amplitude Modulation with 4 levels，四階脈衝振幅調變','Pulse Amplitude Modulation with 4 levels'),
 'NRZ':('Non-Return-to-Zero，不歸零編碼','Non-Return-to-Zero'),
 'EQ':('Equalization，等化程序','Equalization'),
 'TPH':('TLP Processing Hints，封包處理提示','TLP Processing Hints'),
 'LTR':('Latency Tolerance Reporting，延遲容忍度回報','Latency Tolerance Reporting'),
 'OBFF':('Optimized Buffer Flush/Fill，緩衝區排空與填入的活動提示','Optimized Buffer Flush/Fill'),
 'PTM':('Precision Time Measurement，精確時間量測','Precision Time Measurement'),
 'DPA':('Dynamic Power Allocation，動態功率配置','Dynamic Power Allocation'),
 'DOE':('Data Object Exchange，資料物件交換','Data Object Exchange'),
 'CMA':('Component Measurement and Authentication，元件量測與驗證','Component Measurement and Authentication'),
 'SPDM':('Security Protocol and Data Model，安全協定與資料模型','Security Protocol and Data Model'),
 'IDE':('Integrity and Data Encryption，完整性與資料加密','Integrity and Data Encryption'),
 'TEE':('Trusted Execution Environment，可信賴執行環境','Trusted Execution Environment'),
 'DRS':('Device Readiness Status，裝置就緒狀態','Device Readiness Status'),
 'FRS':('Function Readiness Status，功能就緒狀態','Function Readiness Status'),
 'RTR':('Readiness Time Reporting，就緒時間回報','Readiness Time Reporting'),
 'NPEM':('Native PCIe Enclosure Management，原生PCIe機箱管理','Native PCIe Enclosure Management'),
 'VPD':('Vital Product Data，產品識別與描述資料','Vital Product Data'),
 'VSEC':('Vendor-Specific Extended Capability，廠商專屬擴充能力','Vendor-Specific Extended Capability'),
 'DVSEC':('Designated Vendor-Specific Extended Capability，指定廠商專屬擴充能力','Designated Vendor-Specific Extended Capability'),
 'EA':('Enhanced Allocation，增強資源配置','Enhanced Allocation'),
 'FPB':('Flattening Portal Bridge，扁平化入口橋接器','Flattening Portal Bridge'),
 'ROM':('Read-Only Memory，唯讀記憶體','Read-Only Memory'),
 'UEFI':('Unified Extensible Firmware Interface，統一可延伸韌體介面','Unified Extensible Firmware Interface'),
}

class Reminders(HTMLParser):
    def __init__(self,text,definitions,lang):
        super().__init__(convert_charrefs=True)
        self.text=text;self.definitions=definitions;self.lang=lang
        self.starts=[0]+[m.end() for m in re.finditer('\n',text)]
        self.stack=[];self.block=None;self.counts={};self.insertions=[]
        self.pattern=re.compile(r'(?<![A-Za-z0-9_-])(?:'+'|'.join(re.escape(t) for t in sorted(definitions,key=len,reverse=True))+r')(?![A-Za-z0-9_-])')
        self.feed(text)
    def ignored(self):
        return any(tag in {'nav','style','script','title','desc','code','pre'} or
                   tag=='details' and 'open' not in attrs or
                   set((attrs.get('class') or '').split()) & {'st-terms','term-note','qa-citations','qa-glossary','source-note','qr-sources','qa-references','st-specs'} or
                   attrs.get('id') in {'source-index','sources','question-index','figure-index'} for tag,attrs in self.stack)
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs)
        if tag not in {'br','hr','input','meta','link','wbr','img','source','area','base'}:self.stack.append((tag,attrs))
        if not self.block and tag in {'p','figure','table','h1','h2','h3','h4'} and not self.ignored():self.block=(tag,len(self.stack),[],[])
    def handle_data(self,data):
        if self.block and not self.ignored():
            self.block[2].append(data)
            self.block[3].extend(m.group() for m in self.pattern.finditer(data))
    def handle_endtag(self,tag):
        if self.block and tag==self.block[0] and len(self.stack)==self.block[1]:
            raw=' '.join(self.block[2]);terms=[]
            for term in self.block[3]:
                if self.counts.get(term,0)<2:
                    self.counts[term]=self.counts.get(term,0)+1
                    definition=self.definitions[term][self.lang=='en']
                    fullname=definition.split('，')[0].split(',')[0]
                    if fullname not in raw and term not in terms:terms.append(term)
            if terms:
                line,col=self.getpos();offset=self.starts[line-1]+col+len('</'+tag+'>')
                note='<dl class="st-terms" aria-label="'+('本段名詞' if self.lang=='zh' else 'Terms in this passage')+'">'
                note+=''.join('<div><dt>'+escape(t)+'</dt><dd>'+escape(self.definitions[t][self.lang=='en'])+'</dd></div>' for t in terms)+'</dl>'
                self.insertions.append((offset,note))
            self.block=None
        for i in range(len(self.stack)-1,-1,-1):
            if self.stack[i][0]==tag:
                del self.stack[i:];break

def explain_terms(text,series,lang):
    parser=Reminders(text,PCIE if series=='pcie' else NVME,lang)
    for offset,note in reversed(parser.insertions):text=text[:offset]+note+text[offset:]
    return text
