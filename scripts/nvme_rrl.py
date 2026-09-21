"""Register the Read Recovery Level report and its post-only Spec route."""
from pathlib import Path
import json
import re
from scripts.nvme_rrl_content import BASE, REPORT_ID, UNITS, bi
from scripts.nvme_rrl_terms import TERMS
ROOT = Path(__file__).resolve().parents[1]
PREFIX = 'RRL'


def install(reports, titles, modules, glossaries, images):
    from scripts.nvme_lessons import LESSONS
    from scripts.nvme_course_walkthroughs import COURSES
    from scripts.nvme_reader_context import REPORT_CONTEXT
    from scripts.nvme_overviews import OVERVIEWS
    from scripts.nvme_review_bank import BANK
    figures = [f for f in json.loads((ROOT/'.ai/nvme-report/figure-table-register.json').read_text())['entries'] if f['report_id'] == REPORT_ID]
    report = dict(prefix=PREFIX, source_id=BASE, scope_entry='RRL-BASE-INCLUDE', date='2026-09-21',
        title_zh='NVMe Read Recovery Level：讀取復原、作用範圍與設定',
        title_en='NVMe Read Recovery Level: Recovery Effort, Scope, and Configuration',
        range='Base §8.1.23、§5.2.30.1.12（FID 12h）',
        range_en='Base §§8.1.23 and 5.2.30.1.12 (FID 12h)', course_claim_first=True, claims=[])
    modules[REPORT_ID] = []
    for u in UNITS:
        cid=PREFIX+'-'+u['key'].upper(); mid='rrl-'+u['key']
        report['claims'].append(dict(key=u['key'].upper(), source_id=BASE, section=u['section'],
            printed_pages=re.sub(r'\d+', lambda m: str(int(m[0])-26), u['pages']), pdf_pages=u['pages'],
            normative_keyword='none', scope_entry_id='RRL-BASE-PREREQUISITES' if u['prerequisite'] else 'RRL-BASE-INCLUDE',
            zh_tw=u['summary']['zh'], en=u['summary']['en']))
        titles[cid]=(u['title']['zh'],u['title']['en'])
        modules[REPORT_ID].append(dict(id=mid, title=u['title'], lead=u['summary'], sources=[cid],
            figures=[int(f['number']) for f in figures if f['teaching_module']==mid], rows=bi([],[]),
            example=u['example'], pitfall=bi('','')))
        LESSONS[mid]=dict(headers=bi(['問題','判斷','例子'],['Question','Interpretation','Example']),
            teaching=[s[1] for s in u['steps']], reading=bi(u['reading'], {
                'levels':'Read mandatory versus optional levels first, then follow the direction of decreasing recovery in Figure 755.',
                'scope':'Use Figure 67 for containment and Figure 484 for the corresponding command target.',
                'discover':'Read only CTRATT.RRLVLS/NSETS, RRLS and ONCS.SSFS in the long Figure 338.',
                'set':'Figures 484/485 separate the target from the value; the command-envelope references explain placement and SV.',
                'get':'Figure 198 selects the question; Figures 201 and 485 provide alternative DW0 formats.',
                'activation':'The time sequence explains the successful-completion boundary; section 4.4 supplies shared-access context.',
                'lifetime':'Read Figures 126/127 by capability row and feature-scope column, and pair Figure 466 with footnote 2.'
            }[u['key']]))
        COURSES[mid]=dict(title=u['title']['zh'],steps=u['steps'],outcome=u['example']['zh'])
    extras=[
        ('INHERITANCE','scope','8.1.23','715',False,
         '在 NVM Set 內建立的 namespace 繼承該 Set 的 RRL；不支援 NVM Sets 時，所有 namespace 使用同一 RRL。',
         'A namespace created in an NVM Set inherits that set’s RRL; without NVM Sets, all namespaces use one RRL.'),
        ('TARGET-RULES','set','4.4','195',True,
         'NVM Set 與 subsystem 範圍的 Feature，NSID 應為 0；非零值使 Get／Set Features 被中止，不能用來縮小成單一 namespace。',
         'For an NVM Set or subsystem-scoped feature, NSID should be zero; nonzero values cause Get/Set Features to be aborted rather than narrowing the scope to a namespace.'),
        ('SET-ENVELOPE','set','5.2.30','482-485',True,
         'FID 12h 不使用資料 buffer；Set 的 CDW10 帶 FID 與 SV。未使用的命令專用欄位保留，不可保存時要求 SV=1 會以 Feature Identifier Not Saveable 中止。',
         'FID 12h uses no data buffer. Set CDW10 carries FID and SV; unused command-specific fields are reserved, and SV=1 for a non-saveable feature causes Feature Identifier Not Saveable.'),
        ('QUERY-SELECTION','get','5.2.12','235-238',True,
         'SEL 的 0、1、2、3 分別選目前、預設、已保存與能力。沒有可用的 saved 值時，saved 查詢回 default；能力格式只表示 CHANG、NSSPEC 與 SVBL。',
         'SEL 0/1/2/3 selects current/default/saved/capabilities. A saved query returns default when no saved value is available; the capability format reports CHANG, NSSPEC and SVBL.'),
        ('SHARED-ACCESS','activation','4.4','194',True,
         '多個主機同時存取非 controller scope 的共享 Feature 值，需要主機間協調；Base 沒有指定協調程序。',
         'Concurrent access by multiple hosts to shared features outside controller scope requires host coordination, whose procedure is not specified by Base.'),
        ('PERSISTENCE-FOOTNOTE','lifetime','5.2.30','484-485',True,
         'FID 12h 的 Current Setting Persists 欄為 Yes，註腳 2 限定該欄僅供不可保存的 Feature 使用。',
         'FID 12h has Yes in Current Setting Persists, and footnote 2 restricts that column to non-saveable features.'),
        ('SET-IDENTIFIER','scope','3.2.2','106-108',True,
         'NVMSETID 是 subsystem 內的 16-bit Set 識別值；支援 NVM Sets 時 0 為保留，不支援時主機將此欄清為 0。',
         'NVMSETID is a 16-bit set identifier within the subsystem. Zero is reserved when NVM Sets are supported; otherwise the host clears the field to zero.'),
    ]
    for key,mid,section,pages,prerequisite,zh,en in extras:
        report['claims'].append(dict(key=key,source_id=BASE,section=section,pdf_pages=pages,
            printed_pages=re.sub(r'\d+',lambda m:str(int(m[0])-26),pages),normative_keyword='none',
            scope_entry_id='RRL-BASE-PREREQUISITES' if prerequisite else 'RRL-BASE-INCLUDE',zh_tw=zh,en=en))
        titles[PREFIX+'-'+key]=(zh,en)
        next(m for m in modules[REPORT_ID] if m['id']=='rrl-'+mid)['sources'].append(PREFIX+'-'+key)
    reports[REPORT_ID]=report
    glossaries[REPORT_ID]=[(term,'') for term in TERMS]
    images[REPORT_ID]=dict(zh='posts/2026/dogMC_title.jpg',en='posts/2026/cat_title.jpg')
    REPORT_CONTEXT[REPORT_ID]=dict(
        intro=bi('讀取遇到難以復原的資料時，控制器應該再多試一些，還是少做一些復原、讓主機早點取得結果？Read Recovery Level 提供這項取捨。本文從等級與影響範圍開始，再把支援位元、設定命令、讀回格式和重設後的行為接起來，讓每個欄位都對應到一個具體問題。',
         'When data is difficult to recover, should a controller spend more effort or use less recovery before returning a result to the host? Read Recovery Level provides this tradeoff. Start with levels and affected scope, then connect capability bits, configuration, readback and reset behavior so each field answers a concrete question.'),
        axes=bi([
            ['先理解取捨','等級調整的是讀取錯誤復原的程度。比較最多、預設與最少復原，並分清策略、實際延遲與成功結果。'],
            ['找到共用設定的對象','先看是否有儲存集合，再找哪些 namespace 在同一集合內。這決定一次設定影響誰，以及哪些空間無法各自選不同等級。'],
            ['把能力、要求與結果接起來','先查哪些等級受支援，再指定目標與新值，最後以正確的查詢格式讀回。支援清單、目前值與保存能力分別回答不同問題。'],
            ['沿著時間追蹤設定','以設定成功區分先前與後續命令；再判斷重設覆蓋範圍、目前值與已保存值。這樣才能解釋何時用新值、何時可能回到另一個值。']],
            [['Understand the tradeoff','Levels adjust read-error recovery effort. Compare maximum, default and minimum recovery, separating policy from measured latency and successful recovery.'],
             ['Find who shares the setting','Determine whether sets exist and which namespaces share a set. This identifies the affected spaces and those that cannot independently choose different levels.'],
             ['Connect capability, request and result','Discover supported levels, choose the target and value, then read back using the correct format. Level support, current value and saveability answer different questions.'],
             ['Follow the setting over time','Use successful completion to distinguish earlier and later commands. Then consider reset scope, current and saved values to explain when a new or restored value applies.']]),
        background=bi(['讀者已學過 OS、Computer Organization，並了解 SSD 的基本概念。本文的 Set 7／9、namespace A／B／C 與位元數值均為說明性範例；使用前須以實際裝置回報的集合與能力為準。',
                       '先用一個 Set 的設定情境串起觀念，再比較容易混淆的值與範圍；讀完應能解釋哪些空間共用設定，以及每次查詢究竟回答什麼。'],
                      ['Assumes operating systems, computer organization and basic SSD knowledge. Sets 7/9, namespaces A/B/C and encoded values are illustrative and depend on actual device capabilities.',
                       'Follow one set’s configuration, then compare easily confused values and scopes. The goal is to explain which spaces share a setting and what each query actually answers.']))
    OVERVIEWS[REPORT_ID]=bi([
        '可以用同一個問題貫穿全文：想讓 Set 7 內的讀取採用最少復原，需要查哪些能力、送出什麼參數，又要怎樣知道目前真的在用這個設定？先理解這條流程，再看每個欄位的位置。',
        '後半部會刻意比較相同數值在不同格式下的意思，以及相同設定在不同重設範圍下的結果。這些對比能避免只背等級名稱，卻把查詢或持續性判斷用錯。'],
        ['Follow one question: to use minimum recovery for reads in set 7, what must be discovered, which parameters are needed, and how can the current setting be confirmed?',
         'The comparisons distinguish identical numbers in different result formats and identical settings under different reset scopes.'])
    questions=[
        ('bitmap','RRLS=8011h，能選 Level 8 嗎？Level 15 應填 8000h 嗎？',
         'With RRLS=8011h, is level 8 available, and should level 15 be encoded as 8000h?',
         '不能選 8，因為 bit 8 是 0。要選 15，先用 RRLS bit 15 確認支援，再在 4-bit RRL 欄填 Fh；8000h 是支援位元的遮罩，不是等級代碼。',
         'No: bit 8 is zero. For level 15, check RRLS bit 15, then encode Fh in the four-bit RRL field. The value 8000h is a support-bit mask, not the level code.', ['DISCOVER','SET']),
        ('scope','A、B 在同一 Set，能靠填 A 的 NSID 只讓 A 用 Level 15 嗎？',
         'Can A’s NSID select level 15 only for A when A and B share one set?',
         '不能。RRL 依 Set 共用，命令的 NVMSETID 選該集合；這種 scope 的 NSID 應為 0，非零不會縮小作用範圍，而會使命令被中止。',
         'No. RRL is shared at set scope and NVMSETID selects the set. NSID should be zero for this scope; nonzero does not narrow the effect and causes the command to be aborted.', ['SCOPE','TARGET-RULES']),
        ('result','成功 Get 的 DW0=4，為什麼還不能立即說目前是 Level 4？',
         'Why is successful Get DW0=4 not enough to conclude that the current level is 4?',
         '還要看 SEL。SEL=0 才回 current；SEL=3 的 4 是 CHANG=1、NSSPEC=0、SVBL=0 的能力組合。若 SEL=1，4 說的是預設值。',
         'Check SEL: zero returns current, while three makes 4 the CHANG=1/NSSPEC=0/SVBL=0 capability combination. With SEL=1, it is the default value.', ['GET','QUERY-SELECTION']),
        ('timing','Set Level 15 成功後，仍在途的 Read A 與之後才提交的 Read B 都保證用 15 嗎？',
         'After Set level 15 succeeds, must both an outstanding read A and a subsequently submitted read B use 15?',
         'B 必須使用新設定；A 已先提交，可能套用或不套用新值。Level 15 本身也沒有固定毫秒上限。需要清楚區分兩批時，宜先完成 A，再修改設定。',
         'B must use the new setting; already-submitted A may or may not use it. Level 15 also has no fixed millisecond bound here. Complete A before changing settings when a clear batch boundary is needed.', ['ACTIVATION','LEVELS']),
        ('reset','SV=0 成功設成 15，是否一重設就回到 4？',
         'Does successfully setting 15 with SV=0 mean every reset restores 4?',
         '不一定。不可保存的 FID 12h 本身具持續性；可保存者還要看重設範圍。Figure 126 的全體情況回 saved 或 default，Figure 127 的局部情況對 Set／subsystem scope 維持 current。',
         'Not necessarily. Non-saveable FID 12h is persistent. A saveable instance depends on reset scope: Figure 126 restores saved or default, while Figure 127 retains current for set/subsystem scope.', ['LIFETIME','PERSISTENCE-FOOTNOTE']),
    ]
    BANK[REPORT_ID]=[dict(id='rrl-'+key,question=bi(qz,qe),answer=bi(az,ae),sources=[PREFIX+'-'+s for s in src]) for key,qz,qe,az,ae,src in questions]


ROUTE = [
    (499,499,'5.2.30.1.12','5.2.30.1.13',bi('從 Read Recovery Level Config 標題起，先解釋 Set／subsystem 範圍，再用 Set 7、Level 15 連看 Figures 484／485，最後指出 Get 回覆位置與 SEL=3 例外。',
        'Start at Read Recovery Level Config. Explain set/subsystem scope, connect Figures 484/485 with set 7 and level 15, then show Get’s return location and the SEL=3 exception.')),
    (715,716,'8.1.23','8.1.24',bi('從 Read Recovery Level 標題起，把設定連回復原取捨、namespace 繼承與 LR 限制；Figure 755 收束方向、必備與選用等級。',
        'Start at Read Recovery Level. Connect configuration to the recovery tradeoff, namespace inheritance and the LR limitation. Use Figure 755 to conclude with level direction and mandatory versus optional support.')),
]


def render_route(reader):
    lang=reader.lang;reader.figure_label='R';reader.figure_paragraph_no=0
    out=['<section id="spec-route"><h2>'+bi('開著 Spec 的順向報告路徑','A forward route through the specification')[lang]+'</h2>']
    out.append(reader.paragraph(bi('先用本文建立全貌，再開 Base PDF：499 → 715～716，只往後翻一次。以下採 PDF 檢視器頁碼；共用頁從指定標題開始，在下一節標題前停止。必要引用的欄位已在中文教學整理，不必為每一個引用反覆跳頁。',
        'Establish the overview first, then open the Base PDF: 499 → 715–716, with one forward jump. These are PDF viewer page numbers. On shared pages, start at the named heading and stop before the next section. The Chinese tutorial explains the necessary references without repeated detours.')[lang]))
    rows=[[f'R{i} · Base PDF ' + (str(a) if a==b else f'{a}–{b}'),f'§{section}',why[lang]+' '+bi(f'在 §{stop} 前停下。',f'Stop before §{stop}.')[lang]] for i,(a,b,section,stop,why) in enumerate(ROUTE,1)]
    out.append(reader.table(bi(['翻頁順序','主範圍','講解重點與停止位置'],['Page sequence','Primary scope','Focus and stop heading'])[lang],rows))
    out.append('</section>');reader.figure_label=None
    return '\n'.join(out)
