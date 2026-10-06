"""Question-specific reading plans. The old 17 aspects are editorial inputs only.

Choose a form by the actual learning task, not by the chapter or command profile.
Unselected legacy text remains in the authoring history, never in folded HTML.
"""

# Every question is assigned explicitly. New questions require an editorial choice.
KINDS = {
    'fields': '1 11 16 24 30 31 34 35 49 76 83 100 126 127 128 137 152 155 158 168 188 190 196 197 198 199 200 201 213 215 224 244 260 272 276 278 279 288 321 323 326 327',
    'compare': '8 13 41 44 45 46 54 60 62 64 70 71 72 73 93 94 95 96 101 116 119 140 148 150 170 171 174 175 184 189 222 223 236 246 256 268 270 281 284 287 324 325',
    'lookup': '14 47 50 57 69 74 81 118 136 146 149 157 203 205 217 228 237 248 252 257 262 269 283',
    'process': '2 3 4 10 12 17 20 21 22 26 27 29 51 58 59 61 63 65 66 75 84 88 90 107 112 120 124 134 139 144 147 160 161 162 177 178 180 182 183 191 193 206 214 218 219 226 232 234 242 247 251 253 254 258 264 266 271 286 289 290 292 293 295 322',
    'concept': '5 7 19 25 28 36 38 39 40 42 78 82 86 87 99 102 103 104 110 111 122 129 132 156 164 173 185 186 194 210 227 229 240 249 250 263 273 275 277 291 328',
    'error': '15 18 23 32 33 48 56 85 97 108 109 121 135 138 151 159 163 165 166 207 225 230 233 238 239 243 259 265 280 282',
    'diagnose': '6 37 43 53 68 77 80 92 98 105 106 113 114 117 125 131 143 181 187 192 204 285 296 297 298 299 300 301 302 304 305 306 307 308 309 310 311 312 313 314 315 316 317 319 320',
    'lifecycle': '9 52 55 67 79 91 115 123 130 142 145 153 169 172 176 179 195 212 216 220 221 231 235 241 245 255 267 294 303 318',
    'events': '89 133 141 154 167 202 208 209 211 261 274',
}

# A section has a bilingual heading and relevant source paragraphs, not a fixed
# number of required answers. Paragraph 1 opens the answer without a heading.
FORMS = {
    'fields': [
        ('先確認資料的來源與範圍', 'Establish the source and scope', [2, 3]),
        ('欄位、單位與判讀例子', 'Fields, units and worked interpretation', [4, 5, 6]),
        ('判讀時要保留的條件', 'Conditions that change the interpretation', [7, 16]),
    ],
    'compare': [
        ('差別在哪裡', 'What differs', [2, 4]),
        ('如何選擇與確認', 'How to choose and verify', [3, 5, 6]),
        ('哪些結論不能互相套用', 'Where the comparison stops', [7, 16]),
    ],
    'lookup': [
        ('要查哪個對象、哪份資料', 'Select the target and information', [2, 3, 4]),
        ('查詢順序與回覆判讀', 'Query sequence and interpretation', [5, 6]),
        ('證據不足或不一致時怎麼判斷', 'Handle missing or inconsistent evidence', [7, 16, 17]),
    ],
    'process': [
        ('操作前先準備什麼', 'Prepare the operation', [2, 3, 4]),
        ('先後順序與完成條件', 'Sequence and completion conditions', [5, 6]),
        ('未符合條件時如何處理', 'Handle unmet conditions', [7, 16]),
    ],
    'concept': [
        ('機制與適用範圍', 'Mechanism and scope', [2, 4]),
        ('用操作與結果理解', 'Understand it through actions and results', [3, 5, 6]),
        ('容易誤判的地方', 'Avoid a misleading conclusion', [7, 16]),
    ],
    'error': [
        ('先區分是哪一種失敗', 'Distinguish the failure conditions', [2, 4, 7]),
        ('用哪些資料確認原因', 'Establish the cause from evidence', [3, 5]),
        ('結果與後續驗證', 'Outcome and follow-up checks', [6, 16, 17]),
    ],
    'diagnose': [
        ('先保留哪些證據', 'Preserve the evidence first', [2, 3, 4]),
        ('依什麼順序排除原因', 'Work through the possible causes', [17, 5]),
        ('什麼結果足以支持結論', 'Decide what the evidence supports', [6, 7, 16]),
    ],
    'lifecycle': [
        ('先界定觸發方式與影響對象', 'Identify the trigger and affected objects', [2, 3]),
        ('哪些狀態改變，恢復後怎麼處理', 'State changes and recovery', [4, 5, 6]),
        ('如何驗證保留或恢復結果', 'Verify retention and recovery', [7, 16, 17]),
    ],
    'events': [
        ('事件何時成立、由誰觀察', 'When the event exists and who observes it', [2, 3, 4]),
        ('通知、讀取與確認的關係', 'Notification, reading and acknowledgment', [5, 6]),
        ('沒有通知或紀錄時怎麼判斷', 'Evaluate missing notifications or records', [7, 16, 17]),
    ],
}

# Short, single-mechanism questions need fewer paragraphs. Remove repetition,
# not the qualifying condition or the actual result. These choices are explicit.
OMIT = {54: [17]}


# Include event/error/retention detail only where it answers this question.
# These are not appended automatically because the chapter uses a command.
EXTRA = {
    3: [8, 11], 16: [12], 23: [9, 10], 51: [10], 61: [9],
    62: [12, 14], 64: [12, 14], 65: [12, 13, 14],
    79: [12, 13, 14], 89: [9], 91: [12], 96: [9],
    99: [10], 103: [10], 105: [8], 123: [12, 13, 14],
    125: [10, 11], 130: [12, 13, 14], 133: [9, 11],
    141: [9], 142: [12, 13, 14], 146: [8, 10, 12, 15],
    147: [10, 15], 148: [9, 10, 12, 14, 15], 153: [12, 13, 14],
    167: [9, 10, 11], 169: [12, 13, 14],
    174: [8], 202: [9],
    208: [11], 209: [11], 212: [12, 13, 14],
    216: [9, 11, 12, 13, 14], 231: [12, 13, 14],
    235: [12, 13, 14], 241: [12, 13, 14], 245: [12, 13, 14],
    250: [8], 255: [12, 13, 14], 260: [14, 15], 261: [9, 10, 15],
    265: [10], 267: [12, 13, 14], 274: [9, 10, 11],
    285: [8, 10], 290: [8], 301: [10], 324: [10],
}

# A short conceptual answer need not inherit even the three-section pattern.
# Each omission below is a restatement of an included paragraph, not a lost
# status condition, unit, example or source reference.
CUSTOM_SECTIONS = {
    5: [('何時可以提交命令', 'When commands may be submitted', [2,3,5]),
        ('Doorbell 不能取代就緒條件', 'Doorbells do not replace readiness', [4,7,16])],
    25: [('先確認 Queue 的有效期間', 'Establish the queue lifetime', [2,3,4,5]),
         ('不存在的 Queue 沒有固定錯誤回報', 'No fixed response for a nonexistent queue', [7,16])],
    38: [('哪些階段有順序，哪些沒有', 'Which stages are ordered', [2,3,4]),
         ('有相依關係時，Host 要怎麼做', 'How the host handles dependencies', [5,6,7,16])],
    110: [('IANP 決定的是中止後的保證', 'IANP defines the guarantee after abort', [3,4,6,7]),
          ('已經發生的效果仍要另外確認', 'Earlier effects still need checking', [5,16])],
    111: [('先分開判讀 Abort 與目標的 CQE', 'Read the Abort and target CQEs separately', [3,4,6]),
          ('IANP=1 後仍要追蹤目標', 'Continue tracking the target after IANP=1', [5,7])],
    154: [('正常測試完成，要看哪裡', 'Where normal test completion is reported', [2,5,6]),
          ('Diagnostic Failure 是另一種通知', 'Diagnostic Failure is a distinct notification', [3,4,16])],
    211: [('紀錄與通知各自有哪些條件', 'Conditions for recording and notification', [2,3,4]),
          ('如何建立正確的驗證預期', 'Build the right verification expectations', [5,6,16])],
    273: [('耗損數值不是 Ready 狀態', 'Wear values are not readiness state', [2,4,6]),
          ('存取失敗時，應依什麼證據判斷', 'Evidence to examine after access fails', [3,5,7,16])],
    291: [('遮蔽的是通知，CQ 仍會前進', 'Masking suppresses notification, not CQ progress', [2,4,6]),
          ('如何觀察完成並避免 CQ 滿', 'Observe completions and avoid a full CQ', [3,5,7])],
}

CUSTOM_LEADS = {
    136: ('要同時讀 Identify 與 Firmware Slot Information Log：Identify.FRMW 提供 slot 數量及 slot 1 是否唯讀，Log 則提供各 slot 的內容與啟用狀態。',
          'Read both Identify and the Firmware Slot Information Log: Identify.FRMW supplies the slot count and slot 1 read-only capability; the log supplies slot contents and activation state.'),
    154: ('正常 Self-test 完成要從 Device Self-test Log 判斷；規範沒有定義通用的 Self-test Completed 通知，因此不能把等到 AER 當成完成條件。',
          'Determine normal self-test completion from the Device Self-test Log. There is no generic Self-test Completed notice, so receiving an AER is not a completion requirement.'),
    211: ('PEL 新增紀錄，不代表一定會發出 AER。持久事件紀錄與非同步通知有各自的觸發條件，要分開判斷。',
          'A new PEL record does not necessarily produce an AER. Persistent recording and asynchronous notification have separate triggering conditions.'),
    207: ('這套介面不是讓 Host 建立多個不同 ID 的 Context。判斷命令順序是否正確，要看 ACT 要求的動作，以及目前是否已有 reporting context。',
          'This interface does not let the host create a list of contexts with distinct IDs. Command ordering depends on the requested ACT operation and whether a reporting context already exists.'),
    273: ('不能直接判斷。Media Unit Status Log（LID10h）沒有一個能直接換算成 Namespace Ready 的通用狀態；必須再查看 namespace 與存取路徑的證據。',
          'Not directly. Media Unit Status Log (LID10h) has no generic state that translates into Namespace Ready; inspect namespace and access-path evidence separately.'),
    290: ('FID09h 的 Interrupt Vector Configuration 不負責遮蔽中斷。它的 CD 位元控制該 vector 是否使用 Interrupt Coalescing；真正的 mask 必須從使用中的中斷機制確認。',
          'Interrupt Vector Configuration (FID09h) does not mask interrupts. Its CD bit controls whether that vector uses interrupt coalescing; inspect the active interrupt mechanism for the actual mask.'),
}

RELATED = {7:[3], 51:[167], 63:[216,221,226], 119:[123,130,133],
           147:[148], 154:[133], 172:[65], 195:[55,62],
           223:[226,231,235], 261:[260]}

def extra_title(fields):
    if fields == [8]:return ('CQE、DNR 與 More 在這裡是否適用', 'Whether CQE, DNR and More apply here')
    if fields == [10]:return ('用 Log 補充哪些證據', 'Evidence supplied by the log')
    if fields == [11]:return ('Persistent Event 的記錄條件', 'Persistent Event recording conditions')
    if fields == [9]:return ('Asynchronous Event 的通知條件', 'Asynchronous Event notification conditions')
    if 15 in fields:return ('回報方式與共享對象', 'Reporting and shared objects')
    if 8 in fields:return ('錯誤完成與紀錄要如何對照', 'Correlate error completions and records')
    return ('分開核對事件通知與 Log 紀錄', 'Check notifications and log records separately')

PROMPTS = {
    'fields': ('先試著說明欄位的單位與編碼，再用一組數值推導結果。', 'Explain the units and encoding, then work through one set of values.'),
    'compare': ('先說出比較對象最重要的差別，並舉一個不能互相代用的例子。', 'Identify the key difference and one case where the alternatives are not interchangeable.'),
    'lookup': ('先選查詢介面與目標，再說明哪個回傳欄位能支持你的結論。', 'Choose the interface and target, then identify the returned field that supports your conclusion.'),
    'process': ('先排出操作順序，指出哪一步必須等待完成，才能進行下一步。', 'Order the actions and identify which completion must precede the next action.'),
    'concept': ('先用自己的話解釋機制，再舉一個常見誤解。', 'Explain the mechanism in your own words and identify a common misconception.'),
    'error': ('先區分失敗條件，再判斷是否有規範明定的回報結果。', 'Distinguish failure conditions before deciding whether a particular response is required.'),
    'diagnose': ('先列出已知證據與仍缺少的資訊，再決定能不能判定韌體違規。', 'Separate available evidence from missing information before judging conformance.'),
    'lifecycle': ('先指明重設或中斷的方式，再分別判斷設定、進行中的操作與資料。', 'Name the reset or interruption, then assess settings, ongoing operations and data separately.'),
    'events': ('先說明事件成立的條件，再區分通知、事件確認與紀錄。', 'Establish the event condition, then distinguish notification, acknowledgment and recording.'),
}

def reading_plan(q):
    n = q['id']
    kinds = [kind for kind, ids in KINDS.items() if n in map(int, ids.split())]
    if len(kinds) != 1:
        raise ValueError(f'Q{n} needs exactly one deliberate reading plan: {kinds}')
    kind = kinds[0]
    sections = [dict(title=(zh, en), fields=[i for i in fields if i not in OMIT.get(n, [])])
                for zh, en, fields in CUSTOM_SECTIONS.get(n, FORMS[kind])]
    extras = EXTRA.get(n, [])
    # Retention belongs in a comparison only for questions about retention.
    retention = [i for i in extras if i in (12, 13, 14)]
    if retention:
        title=('重設或斷電時，要確認什麼', 'Checks across reset or power loss')
        sections.insert(2, dict(title=title, fields=retention, table=True))
    special = [i for i in extras if i not in retention]
    if special:
        sections.append(dict(title=extra_title(special), fields=special))
    return dict(kind=kind, prompt=PROMPTS[kind], lead=CUSTOM_LEADS.get(n,q['answers'][1]),
                related=list(dict.fromkeys(q.get('related',[])+RELATED.get(n,[]))),
                sections=[s for s in sections if s['fields']])
