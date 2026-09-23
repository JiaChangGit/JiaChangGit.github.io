"""Independently authored Namespace Write Protection lessons."""
from scripts.nvme_report_extension import bi

REPORT_ID='base-namespace-write-protection'

def claim(zh,en,section,pages,background=False):
    return dict(text=bi(zh,en),section=section,pages=pages,background=background)

UNITS=[
dict(key='model',title=bi('先看保護誰，再看四種狀態','Start with the protected object and four states'),claims=[
 claim('Namespace Write Protection 讓主機控制單一 namespace 的寫入保護狀態。支援這項能力時，No Write Protect 與 Write Protect 必備；Until Power Cycle 與 Permanent 兩種狀態選用。namespace 建立時從 No Write Protect 開始；同一 namespace 的狀態須由所有附接它的控制器共同遵守。',
 'Namespace Write Protection lets the host control a namespace’s write-protection state. No Write Protect and Write Protect are mandatory when the capability is supported; Until Power Cycle and Permanent are optional. A newly created namespace starts in No Write Protect, and every controller to which it is attached must enforce its state.','8.1.18','690-692'),
 claim('FID 84h 的作用範圍是 namespace，不使用額外屬性資料 buffer。WPS 的 0、1、2、3 是互斥的狀態代碼，不是可自由組合的位元遮罩。',
 'FID 84h has namespace scope and no attribute data buffer. WPS values 0, 1, 2 and 3 are mutually exclusive state codes, not independently combinable flags.','5.2.30.1.38','538-539'),
],steps=[
 ('從保存一份資料的情境開始','假設 namespace 7 放著一份已完成驗證的資料集，接下來只希望讀取，不希望後續命令改寫它。這時主機可以要求控制器把 namespace 7 切到 Write Protect。保護的是這份儲存空間，不是某個程式的檔案權限，也不是把整顆裝置拔掉；查詢狀態、讀取資料等操作仍各有允許規則。本文的 7 是說明用的有效識別值。'),
 ('四個代碼先按用途理解','WPS=0 表示本機制未設寫入保護；1 表示已保護，但可用合法的 Set Features 要求解除；2 表示維持保護直到 power cycle；3 表示永久保護。這些代碼不代表程度從弱到強的連續量。尤其 3 不是把 1 與 2 兩種功能疊加，而是另外定義的一個狀態。'),
 ('支援整個功能，不等於支援每一種狀態','裝置可以只提供 0 與 1，仍符合這項選用功能的最低要求。想用 2 或 3，必須先確認控制器宣告支援。原表的 M 是「有實作 Namespace Write Protection 時必備」，不能讀成每一台 NVMe 裝置都一定有這項功能。'),
 ('從另一個控制器存取也受到限制','若控制器 A、B 都附接 namespace 7，由 A 設好的保護不能透過 B 繞過。規格要求附接該 namespace 的任何控制器都遵守它的保護狀態。反過來，namespace 8 是另一個設定對象；保護 7 不等於自動把 8 的 WPS 也改成 1。之後會再討論影響多個 namespace 的命令。'),
],example=bi('說明性範例：namespace 7 由 A、B 共同存取。經 A 成功設為 WPS=1 後，B 也必須遵守保護；不能把設定命令的傳送入口當作保護的邊界。',
 'Illustration: controllers A and B access namespace 7. After A successfully sets WPS=1, B must enforce the protection too. The controller receiving the configuration command is not the boundary of enforcement.'),reading=bi('先用 Figure 735 比較狀態與支援要求；WPS 的實際編碼在 Figure 541。','Use Figure 735 for state definitions and support requirements, and Figure 541 for the WPS encoding.')),

dict(key='transitions',title=bi('沿著狀態圖理解解除與重設','Follow transitions, release and reset behavior'),claims=[
 claim('Set Features 可在 0 與 1 之間切換，也可從 0 或 1 進入受支援且獲准的 2 或 3。處於 2 或 3 時，用 Set Features 要求改變狀態會得到 Feature Not Changeable。一般狀態機中，2 經 power cycle 回到 0；沒有 power cycle 的 Controller Level Reset 不解除它。',
 'Set Features can switch between 0 and 1 and enter supported, permitted state 2 or 3 from either. Attempts to change state 2 or 3 with Set Features fail with Feature Not Changeable. In the normal state machine, a power cycle returns state 2 to 0; a Controller Level Reset without power cycling does not release it.','8.1.18; 5.2.30.1.38','538-539,690-691'),
 claim('除了狀態 2，四種狀態都跨 power cycle 與 Controller Level Reset 保留。FID 84h 不可保存且沒有 default 值，但這不會取消各狀態本身的持續性。Revert to Subsystem Manufacturing Settings Personality 生效時，非永久狀態回到 0，永久狀態維持。',
 'All states except 2 persist across power cycles and Controller Level Resets. FID 84h is non-saveable and has no default, which does not cancel state-specific persistence. When Revert to Subsystem Manufacturing Settings Personality takes effect, non-permanent states return to 0; Permanent remains.','5.2.30.1.38; 8.1.18','538-539,690'),
],steps=[
 ('先追蹤可逆的那條路','建立 namespace 後是 0。成功 Set WPS=1 會進入一般寫入保護，之後成功 Set WPS=0 可以解除。這兩個方向都是命令造成的轉換。不要看到狀態名稱有「Write Protect」就以為一律不可解除；是否能解除，要看完整的狀態名稱與目前代碼。'),
 ('Until Power Cycle 不是 Until Reset','從 0 或 1 可進入 2，但沒有用 Set Features 從 2 回到 0、1 或前進到 3 的箭頭。要求改變會被拒絕。2 回到 0 的特殊箭頭是 power cycle；若只是控制器層級重設而沒有 power cycle，仍然是 2。日常說的「重開」太含糊，必須辨認實際發生的是哪種事件。'),
 ('Permanent 的圖上沒有解除箭頭','從 0 或 1 進入 3 後，Set Features 不能再改變此狀態，斷電與控制器重設也不解除它。這是理解狀態機的重要界線：不能因為 3 的數字比 2 大，就假設可以先進入 2 再往上調到 3。圖上的箭頭才定義了允許路徑，支援與控制條件還要同時成立。'),
 ('把不可保存和跨重設保留分開','Set Features 的 Save 是一種儲存 feature 屬性值的通用機制；本功能不提供這種保存選項。WPS 的持續性則直接由本節規定。因此 WPS=1 即使是用 SV=0 設定，斷電後仍是 1；WPS=2 同樣用 SV=0，斷電後卻回到 0。不能用 SV 的值替代狀態規則。'),
 ('出廠設定復原是另外一種事件','指定的 Revert to Subsystem Manufacturing Settings Personality 真正生效後，1、2 等非永久狀態回到 0；3 保留。它不是一般 Controller Level Reset 的別名，也不是本篇 state machine 裡的 Set WPS 解除命令。這裡只說它對 WPS 的結果，不把這項管理操作當作一般解除流程。'),
],example=bi('同樣先成功設為 WPS=2：沒有斷電的控制器重設後仍為 2；power cycle 後為 0。若原本是 WPS=1，兩種事件之後都仍為 1。',
 'Starting at WPS=2: a controller reset without power cycling retains 2; a power cycle changes it to 0. Starting at WPS=1, both events retain 1.'),reading=bi('Figure 736 看箭頭與事件，Figure 735 看事件後是否保留；兩張圖回答不同問題。','Figure 736 defines transitions and triggers; Figure 735 compares persistence across events.')),

dict(key='controls',title=bi('能力、進入許可與目前狀態是三件事','Separate capability, entry permission and current state'),claims=[
 claim('NWPC 宣告控制器支援哪些狀態；RPMB 的 WPC 控制是否允許命令進入狀態 2 或 3；FID 84h 的 WPS 才是 namespace 目前的狀態。WPUPCC=0 或 PWPC=0 會阻止對應的進入要求。MDS=1 的多 domain subsystem 禁止使用狀態 2，即使相關能力與控制位已設為 1。',
 'NWPC advertises supported states; RPMB WPC permits commands to enter state 2 or 3; FID 84h WPS is the namespace’s actual state. WPUPCC=0 or PWPC=0 blocks the corresponding entry request. MDS=1 prohibits state 2 even when its capability and control bits are set.','8.1.18; 5.2.30.1.38','538-539,690-691'),
 claim('Identify Controller 的 NWPC 位於 byte 531，bit 0 支援 0／1，bit 1 支援 2，bit 2 支援 3。CTRATT bit 10 的 MDS 表示多 domain；ONCS bit 4 的 SSFS 控制非零 SEL／SV 的支援。',
 'Identify Controller byte 531 contains NWPC: bit 0 supports states 0/1, bit 1 supports 2, and bit 2 supports 3. CTRATT bit 10 is MDS, and ONCS bit 4 is SSFS for nonzero SEL/SV support.','5.2.14.2.1','372,397-398,401',True),
 claim('RPMB target 0 的 Device Configuration Block byte 2 是 WPC：bit 0 WPUPCC、bit 1 PWPC。支援 Namespace Write Protection 時，這兩個控制位在 power cycle 或 Controller Level Reset 後清為 0；它們清零不代表既有 WPS 也清零。',
 'WPC is byte 2 of the RPMB target 0 Device Configuration Block: WPUPCC is bit 0 and PWPC is bit 1. With Namespace Write Protection support, both clear after a power cycle or Controller Level Reset. Clearing these controls does not clear an existing WPS.','8.1.24','717-718',True),
],steps=[
 ('先問裝置會不會，再問目前允不允許','NWPC=07h 表示 0～3 都受支援，並不是目前 WPS=7。即使硬體具備永久保護能力，PWPC=0 仍會拒絕要求進入 3 的 Set Features。這就像一項操作確實存在，但另有控制位決定現在是否接受；兩者都不能用目前 namespace 是不是唯讀來替代。'),
 ('WPC 位於另一份經認證存取的設定結構','WPC 不在 FID 84h 的 CDW11，也不屬於 namespace 的 WPS。它在 RPMB target 0 的 Device Configuration Block 內；RPMB 透過認證與防重播機制存取，不能把一般 namespace 的 Write 命令當作修改 WPC 的方法。本篇只需要理解這個控制欄位與 FID 84h 的關係，不需要先學完整訊息交換才能理解狀態機。'),
 ('控制位重設後，已保護的資料仍然受到保護','假設 PWPC 曾為 1，namespace 7 已成功進入永久保護。控制器重設後 PWPC 清為 0，意思是後續嘗試讓其他 namespace 進入永久保護時，必須重新滿足控制條件；namespace 7 本來的永久保護仍在。WPS=2 經沒有斷電的控制器重設也保留，雖然 WPUPCC 此時已清零。'),
 ('多 domain 限制要看整個 subsystem','狀態 2 的解除需要 namespace 與它所附接的所有控制器同時經歷 power cycle。多 domain 配置不能以單一局部電源事件保證這件事，因此規格禁止在 MDS=1 時使用狀態 2；要求進入時回 Feature Not Changeable。這個條件針對狀態 2，不應自行擴大成多 domain 配置禁止所有寫入保護。'),
],example=bi('NWPC=07h、WPC=01h、目前 WPS=0：單 domain 可在其餘條件滿足時要求 WPS=2；WPS=3 因 PWPC=0 被拒絕。若改成 MDS=1，WPS=2 的要求也會被拒絕。',
 'With NWPC=07h, WPC=01h and current WPS=0, a single-domain subsystem can enter 2 when other conditions are met; entering 3 is blocked by PWPC=0. Changing MDS to 1 also blocks entry into 2.'),reading=bi('Figure 338 的支援位、Figure 756 的控制位與 Figure 541 的狀態碼要分開解碼。','Decode support bits in Figure 338, control bits in Figure 756 and state codes in Figure 541 separately.')),

dict(key='configure',title=bi('把查詢、設定與成功完成接起來','Connect querying, configuration and successful completion'),claims=[
 claim('以有效且 active 的 NSID 選 namespace；Get FID 84h、SEL=0 讀目前 WPS，Set 在 CDW11 bits 2:0 放新 WPS。設定不可使用 SV=1；SEL=1 沒有 default 可讀，回 Invalid Field in Command。成功進入寫入保護時，控制器必須把該 namespace 的所有揮發性寫入快取資料及 metadata 寫入非揮發媒體。',
 'Select an active namespace with NSID. Get FID 84h with SEL=0 reads current WPS; Set places the requested WPS in CDW11 bits 2:0. SV=1 is not available. SEL=1 has no default to return and fails with Invalid Field in Command. A successful transition to a protected state commits all associated volatile write-cache data and metadata to non-volatile media.','5.2.30.1.38','538-539'),
 claim('Get 的 SEL=3 回 CHANG、NSSPEC、SVBL 能力格式；CHANG=1 只表示功能有可改變的值，不保證目前的永久狀態可解除。FID 84h 不可保存，SEL=2 的 saved 請求依通用規則轉成 default，仍遇到本功能沒有 default 的限制。',
 'Get SEL=3 returns CHANG, NSSPEC and SVBL, not WPS. CHANG=1 means that some feature value is changeable, not that a currently permanent state can be released. FID 84h is non-saveable, so the generic saved-query fallback to default still encounters this feature’s lack of a default.','5.2.12; 5.2.12.2; 5.2.30.1.38','235-238,538',True),
 claim('namespace scope 的 FFFFFFFFh：Set 在 MDS=0 時通常選處理命令之控制器附接的所有 namespace；MDS=1 時回 Invalid Field in Command。Get 沒有本功能特例可套用，回 Invalid Namespace or Format。共享設定需要主機間協調。',
 'For namespace scope, Set with FFFFFFFFh normally selects all namespaces attached to the processing controller when MDS=0; MDS=1 returns Invalid Field in Command. Get has no exception for this feature and returns Invalid Namespace or Format. Shared settings require host coordination.','4.4','194-195',True),
 claim('成功 Set Features 完成後才提交的命令必須使用新設定；更早已提交的命令可能使用或不使用新設定。要劃清前後兩批，主機宜先讓處理中的命令完成，再修改設定。成功完成不能早於 Feature 屬性設定完成。',
 'Commands submitted after successful Set Features completion must use the new setting; previously submitted commands may or may not do so. The host should complete outstanding commands before changing the setting for a clear boundary. Successful completion cannot precede completion of the feature update.','5.2.30.1; 5.2.30.4','485,545',True),
],steps=[
 ('先讀目前值，才能選合法路徑','範例選已附接的 namespace 7，送 Get Features，FID=84h、SEL=0，CDW10=00000084h。成功完成後，CQE DW0 的低 3 bits 才是 WPS。若讀到 0，可以計畫進入 1；若讀到 2，就不能以相同流程要求改成 1。Get 不會把 namespace 改成查到的值，它只回報狀態。'),
 ('同一個 DW0，要先看當初問的是什麼','SSFS 支援非零 SEL 時，SEL=3 的 CDW10 是 00000384h，回覆改成能力格式。假設 DW0=6，表示 CHANG=1、NSSPEC=1、SVBL=0，不是 WPS=6。尤其即使已永久保護，CHANG 仍可表示這個 Feature 曾有可變更的值；它不是解除永久保護的許可。SEL=2 也不能拿來尋找「上次保護前的值」：不可保存時會轉問 default，而本功能沒有 default。'),
 ('送出要求，不把參數當結果','在 WPS=0 的範例中，Set 的 NSID=7、CDW10=00000084h、CDW11=00000001h，表示要求一般 Write Protect；WPS 不放在資料 buffer 裡。SV=0 是正確用法。若錯用 SV=1，會遇到 Feature Identifier Not Saveable，不能因為送過命令就宣稱已經保護成功。'),
 ('成功完成之前，控制器還要處理快取','進入保護不只是把一個狀態 bit 改掉。該 namespace 在揮發性寫入快取中的資料和 metadata 必須在轉換時寫到非揮發媒體。這樣成功切入保護後，受影響的既有快取內容不會留待後續寫回。規格沒有給這個步驟固定毫秒數；資料量與裝置行為會影響完成時間。'),
 ('用清楚的命令邊界理解前後行為','教學流程先等待先前的寫入完成，再送 Set，等待成功 CQE，最後讀回 WPS。這符合通用的設定切換建議，也避免把已在處理中的命令硬套成一定使用新值。若多個主機共享同一 namespace，還要協調對這份設定的存取；本規格不定義主機之間的協調協定。'),
 ('不要把特殊 NSID 當成方便的查詢捷徑','本文使用單一 active NSID，是為了明確選到目標。FFFFFFFFh 的 Set 和 Get 行為不對稱；Set 在單 domain 可涵蓋該控制器附接的全部 namespace，但每個目標仍受自己的狀態限制，不能據此推論多目標更新的原子性。Get 不用這個值回一張全體 WPS 清單。active 表示已附接於本控制器；inactive 與 invalid 的錯誤也不同，欄位教學會把兩者分開。'),
],example=bi('namespace 7 原為 0：Set 的 CDW10=00000084h、CDW11=00000001h；等待成功完成後，Get SEL=0 回 DW0=1 才能確認目前為 Write Protect。能力查詢 DW0=6 回答的是另一個問題。',
 'Starting with namespace 7 at 0: Set CDW10=00000084h and CDW11=00000001h. After successful completion, Get SEL=0 returning DW0=1 confirms Write Protect. A capability response DW0=6 answers a different question.'),reading=bi('Figure 93 定位 NSID 與 CDW；Figures 198／201 分開查詢選擇與回覆，Figures 464／541 接上設定參數。','Figure 93 locates NSID and command dwords; Figures 198/201 separate query selection from results, and Figures 464/541 supply configuration parameters.')),

dict(key='commands',title=bi('保護後，哪些命令仍能做什麼','What commands may do after protection'),claims=[
 claim('Figure 737 列出對受保護 NSID 正常處理的命令，但註腳仍限制會修改非揮發媒體的動作。Flush 成功且不產生作用；Directive Receive 若要求配置 Streams 資源則回 Namespace is Write Protected。未列出的命令只要符合本節列出的受保護目標或跨 namespace 修改條件，就會被拒絕。',
 'Figure 737 lists commands normally processed for a protected NSID, with footnotes restricting actions that modify non-volatile media. Flush succeeds with no effect; Directive Receive allocating Streams resources fails with Namespace is Write Protected. Unlisted commands are rejected when the section’s protected-target or cross-namespace modification conditions apply.','8.1.18.2','691-692'),
],steps=[
 ('正常處理不等於保證成功','Read、Compare、Verify 仍可以處理，是指寫入保護本身不阻擋它們；若讀到媒體錯誤，仍可能因自己的命令規則失敗。Get Features、Identify 等查詢也是如此。這張表不是「只要在表內就永遠成功」的保證表，而是說明寫入保護如何與命令處理共存。'),
 ('有些列必須連註腳一起讀','例如 Dataset Management 列在允許表中，但其指定動作若試圖修改受保護 namespace 的非揮發媒體，控制器必須使命令失敗。Directive Send、Security Send／Receive、Set Features 與兩類 Vendor Specific 命令也有這個註腳。因此僅用命令名稱判斷不夠，必須再看該次請求的具體動作。'),
 ('Flush 的特例來自前面的轉換保證','受保護 NSID 的 Flush 必須成功且不產生作用。原因是進入保護時，該 namespace 的所有揮發性快取資料與 metadata 已被寫入非揮發媒體。這裡沒有授權 Flush 在保護後偷偷修改資料，也沒有說所有情況下的 Flush 都不需要做事；這是針對已受保護 namespace 的規則。'),
 ('Directive Receive 要辨認是不是配置資源','這個命令名稱看起來像只接收資料，但其配置 Streams 資源的操作另有規則：對受保護 namespace 執行時，必須以 Namespace is Write Protected 中止。這個例子提醒讀者：資料傳送方向不能單獨代表操作是否改變狀態。'),
 ('真正影響的 namespace 比命令上寫哪個 NSID 更重要','未列在 Figure 737 的命令，若直接指定受保護 namespace，會受到拒絕規則約束。另一種情況是命令指定未受保護的 namespace 8，實際操作卻會修改受保護的 7；規格以 Format NVM 為例，仍須拒絕。再例如 Sanitize 沒有指定某個 NSID，只要執行會修改受保護 namespace，仍須拒絕。不能靠改填目標或省略 NSID 繞過保護。'),
],example=bi('namespace 7 已受保護、8 未受保護。如果某次 Format NVM 雖指定 8，其格式化範圍卻包含 7，該命令仍須以 Namespace is Write Protected 中止。範圍只含 8 的另一個操作不能直接套用這個案例。',
 'Namespace 7 is protected and 8 is not. If a Format NVM command names 8 but its formatting scope includes 7, it must fail with Namespace is Write Protected. An operation confined to 8 does not inherit that conclusion.'),reading=bi('Figure 737 的兩個命令集合與三項註腳一起讀；Figure 103 再確認保護錯誤的含義。','Read both command sets and all three footnotes in Figure 737, then use Figure 103 for the protection-status meaning.')),

dict(key='observe',title=bi('用正確的狀態與錯誤解釋結果','Interpret results using the right state and status'),claims=[
 claim('主機應以 Get FID 84h 查 namespace 寫入保護狀態。控制器不得只因本狀態機造成的唯讀條件，就把 SMART Critical Warning 的 All Media Read-Only 設為 1；AMRO=0 也不能證明 namespace 沒有設保護。外部寫入保護系統與本機制組合的結果不在此規格定義內。',
 'Use Get FID 84h to determine namespace write-protection state. The controller must not assert SMART All Media Read-Only solely because this state machine creates a read-only condition; AMRO=0 does not prove that a namespace is unprotected. Combined behavior with external write-protection systems is outside this specification’s definition.','8.1.18.1','691'),
 claim('Namespace is Write Protected 表示命令被既有保護禁止；Feature Not Changeable 表示要求改變的值當下不可改；Feature Identifier Not Saveable 表示不支援保存要求。它們分別出現在命令執行、狀態轉換與保存設定的問題上。',
 'Namespace is Write Protected identifies a command prohibited by protection; Feature Not Changeable identifies a currently disallowed value change; Feature Identifier Not Saveable identifies an unsupported save request. They answer different execution, transition and saving questions.','4.2.1; 5.2.30.4','175,545',True),
],steps=[
 ('查詢設定與查看健康警告，目的不同','WPS=1 是主機要求的 namespace 保護狀態；SMART 的 AMRO 是全體媒體唯讀警告。若所有 namespace 都因 FID 84h 設成保護，也不能僅因此把 AMRO 設為 1。想知道 namespace 7 的設定，直接查它的 WPS，不要從整體健康 bit 猜測。'),
 ('WPS=0 只排除這個機制的保護','解除本功能不代表下一筆 Write 在任何條件下都會成功。其他錯誤、媒體狀況或外部保護仍可能影響操作；本節沒有把它們都收編成 WPS 的狀態。若外部寫入保護機制也存在，本規格不定義兩者組合的所有結果，不能自行編造優先順序。'),
 ('從主機原本想做的動作解讀失敗','如果主機本來想寫受保護的 namespace，Namespace is Write Protected 說的是資料命令受到限制。若主機想把 WPS=2 改成 0，Feature Not Changeable 說的是此狀態不允許 Set 解除。若主機錯把 SV=1 加到 FID 84h，Feature Identifier Not Saveable 說的是保存要求不成立；這三種情境不能都寫成模糊的「功能不支援」。'),
 ('完成一個可以向別人說清楚的判斷','最後應能把 namespace、能力、控制位、目前狀態、所要求的動作與完成結果串成一句有因果的描述。例如：namespace 7 已是 2，所以 Set WPS=0 被拒絕；控制器重設未造成 power cycle，因此目前仍是 2。這比只記一個錯誤名稱更能解釋裝置行為。'),
],example=bi('WPS=1 且 AMRO=0 完全可能同時成立：namespace 受到設定保護，但不能因此回報全體媒體唯讀警告。Read 仍按自身條件處理，Write 則受保護限制。',
 'WPS=1 and AMRO=0 can coexist: the namespace is protected by configuration, which alone cannot assert the all-media read-only warning. Reads follow their own rules, while writes are constrained by protection.'),reading=bi('Figure 213 只取 AMRO；Figures 103／554 比較錯誤原因，不把健康 bit 當成 WPS。','Read only AMRO in Figure 213 and distinguish status meanings in Figures 103/554; a health bit is not WPS.')),
]
