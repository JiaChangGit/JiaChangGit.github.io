"""Paired opening narratives and learning axes for independently readable notes."""

def b(zh, en):
    return {'zh': zh, 'en': en}


def context(intro, axes, background):
    return {'intro': intro, 'axes': b([a[0] for a in axes], [a[1] for a in axes]), 'background': background}


REPORT_CONTEXT = {
    'nvm-command-set-1.3': context(
        b('NVM Command Set 說明主機如何以 logical block 為單位讀寫與管理儲存空間。理解它的關鍵，是把資料格式、命令行為、資料完整性與資源管理連起來：同一筆命令，會因 namespace 格式、支援能力與設定不同而有不同的適用條件。',
          'The NVM Command Set defines how a host reads, writes, and manages storage in logical blocks. Its central connections are data formats, command behavior, data integrity, and resource management: a command’s applicable conditions depend on the namespace format, advertised capabilities, and settings.'),
        [(['儲存空間與格式','先理解 namespace 的容量、LBA 格式，以及資料與 metadata 的關係。'],['Storage and formats','Establish namespace capacity, LBA formats, and the relationship between data and metadata.']),
         (['命令做了什麼','比較 Read、Write、Compare、Verify、Copy 與空間管理命令的作用及完成條件。'],['Command behavior','Compare Read, Write, Compare, Verify, Copy, and space-management commands and their completion conditions.']),
         (['資料完整性與順序','理解原子性、命令相依、Protection Information，以及資料檢查的範圍。'],['Integrity and ordering','Understand atomicity, command dependencies, Protection Information, and the scope of checks.']),
         (['能力與資源管理','以 Identify、Features 和 log 理解格式選擇、效能限制及進階資源功能。'],['Capabilities and resources','Use Identify, Features, and logs to understand format selection, performance limits, and advanced resource features.'])],
        b(['主機透過提交佇列送出命令，控制器透過完成佇列回報結果。Base 規格定義這套共同機制；本篇聚焦命令如何作用於 namespace 內的 logical blocks。'],
          ['The host submits commands through a submission queue, and the controller reports results through a completion queue. The Base specification defines this shared mechanism; this note focuses on how commands act on logical blocks within a namespace.'])),
    'base-boot-telemetry-sanitize': context(
        b('Boot Partitions、Telemetry 與 Sanitize 分別處理開機映像、裝置內部狀態資料與資料清除。這篇把三者放在同一套控制方式下理解：先確認支援能力，再分清楚命令要求、背景狀態與回報資料，才能知道一次操作實際完成了什麼。',
          'Boot Partitions, Telemetry, and Sanitize handle boot images, device internal-state data, and data sanitization. This note connects them through a shared control model: establish capabilities, then distinguish the command request, background state, and reported data to understand what an operation actually accomplished.'),
        [(['Boot Partitions','讀取與更新開機映像，並理解 active partition 與寫入保護。'],['Boot Partitions','Read and update boot images, distinguishing the active partition from write protection.']),
         (['Telemetry','理解資料範圍、快照版本與分段讀取的一致性。'],['Telemetry','Understand data areas, snapshot versions, and consistency across segmented reads.']),
         (['Sanitize','區分清除目標、清除方法、背景狀態與清除後的讀取規則。'],['Sanitize','Distinguish targets, methods, background states, and post-sanitization read behavior.'])],
        b(['命令完成與背景作業完成可能是不同事件。Get Log Page 用來讀取回報資料；Get／Set Features 用來查詢及設定功能。後文會在使用處解釋相關識別碼與欄位。'],
          ['Command completion and background-operation completion can be separate events. Get Log Page retrieves reported data; Get/Set Features query and configure functions. Relevant identifiers and fields are explained where used.'])),
    'base-ch1-2': context(
        b('NVMe 是主機與儲存控制器之間的介面。本篇先建立整體關係：主機如何送出命令、控制器如何回報結果，以及 namespace、controller、NVM subsystem 各代表什麼。這些概念是閱讀後續命令與欄位的起點。',
          'NVMe is an interface between a host and a storage controller. This note establishes how the host submits commands, how the controller reports results, and what namespaces, controllers, and NVM subsystems represent. These concepts provide the foundation for later commands and fields.'),
        [(['規格如何分工','分辨 Base、Transport 與 I/O Command Set 各自定義的內容。'],['Specification responsibilities','Distinguish what Base, Transport, and I/O Command Set specifications define.']),
         (['命令如何往返','以提交佇列與完成佇列理解主機和控制器的合作。'],['Command round trips','Understand cooperation between host and controller through submission and completion queues.']),
         (['儲存物件與路徑','分清 namespace、controller 與 subsystem，並理解多條存取路徑。'],['Storage objects and paths','Distinguish namespaces, controllers, and subsystems, including multiple access paths.'])],
        b(['這裡的主機包含作業系統與驅動程式；控制器提供主機可存取的 NVMe 介面。NVMe 描述主機可見的行為，不能直接等同 SSD 內部 NAND 的實體配置。'],
          ['The host includes the operating system and driver; the controller provides the NVMe interface accessible to that host. NVMe describes host-visible behavior, which does not directly specify the SSD’s physical NAND organization.'])),
    'base-ch3': context(
        b('控制器開始處理 I/O 之前，需要先建立可用的介面、佇列與狀態。本篇沿著控制器的運作生命週期，連起能力查詢、初始化、命令處理、記憶體資源，以及關機、重設與韌體啟用。',
          'Before a controller can process I/O, its interface, queues, and operating state must be established. This note follows the controller lifecycle through capabilities, initialization, command processing, memory resources, shutdown, resets, and firmware activation.'),
        [(['啟動與能力','從識別控制器，到設定必要 properties 與確認可處理命令。'],['Startup and capabilities','Identify the controller, configure required properties, and establish readiness.']),
         (['佇列與命令處理','理解佇列位置、Doorbell 更新與仲裁分工。'],['Queues and processing','Understand queue positions, doorbell updates, and arbitration.']),
         (['資源與生命週期','區分容量、控制器記憶體與各種狀態改變的影響範圍。'],['Resources and lifecycle','Distinguish capacity, controller memory, and the scope of state changes.'])],
        b(['提交佇列保存主機送出的命令，完成佇列保存控制器回報的結果。主機要先建立這些共同機制，再使用讀寫等命令；以下從這個先後關係展開。'],
          ['Submission queues hold commands from the host, and completion queues hold results from the controller. The host establishes these shared mechanisms before using commands such as reads and writes.'])),
    'base-ch4': context(
        b('一筆 NVMe 命令必須告訴控制器要做什麼、對哪個 namespace 操作，以及資料放在哪裡；完成結果則必須讓主機認出是哪筆命令、結果如何。本篇從這兩個方向拆解 SQE、CQE 與 PRP／SGL。',
          'An NVMe command must identify the operation, target namespace, and data location. Its completion must identify the command and report the outcome. This note uses these two directions to explain SQEs, CQEs, and PRP/SGL data pointers.'),
        [(['命令內容 SQE','理解命令識別、操作碼與資料指標的分工。'],['Command contents: SQE','Understand command identifiers, opcodes, and data pointers.']),
         (['完成結果 CQE','分開理解新完成項目、命令身分與狀態碼。'],['Completion results: CQE','Distinguish new entries, command identity, and status codes.']),
         (['資料位址 PRP／SGL','把作業系統的記憶體頁面概念接到 NVMe 資料傳輸。'],['Data addresses: PRP/SGL','Connect memory-page concepts to NVMe data transfers.']),
         (['其他共用資料結構','理解功能值、識別碼、清單與文字的表示方式。'],['Other shared structures','Understand representations for Feature values, identifiers, lists, and text.'])],
        b(['命令與完成項目是佇列中的記錄，讀寫的資料通常由資料指標指定。先分清楚「命令記錄」與「命令要搬移的資料」，就能理解後面的欄位配置。'],
          ['Command and completion entries are records in queues; data pointers identify the data involved in a transfer. Distinguishing the command record from its transfer data is the starting point for the field layouts.'])),
    'pcie-transport-1.4': context(
        b('NVMe over PCIe Transport 說明 NVMe 的佇列、properties 與通知如何透過 PCIe 運作。本篇把作業系統熟悉的記憶體映射 I/O、DMA 與中斷，接到一筆 NVMe 命令的實際傳遞過程。',
          'NVMe over PCIe Transport explains how NVMe queues, properties, and notifications operate over PCIe. This note connects memory-mapped I/O, DMA, and interrupts to the transfer of an NVMe command.'),
        [(['介面位置','透過 BAR 與 configuration space 找到 NVMe 介面及能力。'],['Interface locations','Use BARs and configuration space to locate the NVMe interface and capabilities.']),
         (['命令與通知','區分佇列資料、Doorbell 與 interrupt 的作用。'],['Commands and notifications','Distinguish queue data, doorbells, and interrupts.']),
         (['平台行為','理解 reset、電源、錯誤回報與鏈路量測各自的適用範圍。'],['Platform behavior','Understand the scope of resets, power, error reporting, and link measurements.'])],
        b(['Base 規格定義 NVMe 的共同命令與佇列模型；PCIe Transport 補上本機 PCIe 的連接方式。讀取記憶體中的 queue entry，與存取裝置的 MMIO register，是不同種類的存取。'],
          ['The Base specification defines the common NVMe command and queue model; PCIe Transport supplies the local PCIe binding. Accessing a queue entry in memory and accessing a device MMIO register are different kinds of access.'])),
    'base-admin-fw-logs': context(
        b('韌體更新包含傳送映像、保存至 slot 與切換執行版本。這篇說明 Firmware Image Download、Firmware Commit 和 Firmware Slot Information 如何一起完成這件事，並分清楚每一步改變了什麼狀態。',
          'Firmware updates involve transferring an image, storing it in a slot, and changing the running version. This note explains how Firmware Image Download, Firmware Commit, and Firmware Slot Information cooperate, distinguishing the state changed by each step.'),
        [(['能力與更新單位','確認可用 slots、寫入限制及下載片段的粒度。'],['Capabilities and update units','Establish available slots, write restrictions, and download granularity.']),
         (['下載與啟用','理解映像範圍、Commit Action 與 reset 的關係。'],['Download and activation','Understand image ranges, Commit Action, and reset requirements.']),
         (['執行版本','以目前與預定 active slot 區分已保存和正在執行的版本。'],['Running version','Use current and next active slots to distinguish stored and running images.'])],
        b(['Firmware slot 是保存韌體映像的位置；有版本字串不代表該映像正在執行。控制器的能力查詢、命令完成與 slot 資訊必須分別理解。'],
          ['A firmware slot stores an image; a revision string alone does not establish that the image is running. Controller capabilities, command completion, and slot information provide distinct information.'])),
    'base-power-features': context(
        b('NVMe 的功耗與溫度管理是在耗電、回應延遲與工作能力之間做取捨。本篇先建立 power state 的意義，再說明主機設定、自動閒置轉移與溫度相關控制如何分工。',
          'NVMe power and temperature management involve tradeoffs among energy use, response latency, and operating capability. This note establishes the meaning of a power state, then explains host settings, automatic idle transitions, and temperature controls.'),
        [(['功耗狀態','比較功耗、可否處理 I/O，以及進出狀態的延遲。'],['Power states','Compare power, I/O capability, and entry/exit latency.']),
         (['設定與自動轉移','理解 Get／Set Features、APST 與背景工作的限制。'],['Settings and automatic transitions','Understand Get/Set Features, APST, and limits on background work.']),
         (['溫度控制','分開溫度事件通知與控制器的熱管理行為。'],['Temperature control','Distinguish temperature-event notification from thermal-management behavior.'])],
        b(['Features 是控制器提供給主機查詢或設定的功能。支援某個功能、目前功能值，以及設定能否跨斷電保存，是不同資訊。'],
          ['Features are controller functions the host can query or configure. Support, the current value, and persistence across power loss are distinct properties.'])),
    'base-self-test-hmb-emulation': context(
        b('本篇涵蓋裝置自我測試、Host Memory Buffer，以及與記憶體和命令格式相關的延伸功能。主線是分清楚功能由誰啟動、資料由誰提供，以及控制器何時仍可使用這些資源。',
          'This note covers device self-test, Host Memory Buffer, and extensions involving memory and command formats. It distinguishes who starts a function, who supplies its data, and when the controller may still use the resources.'),
        [(['自我測試','分清啟動命令、背景測試進度與結果記錄。'],['Self-test','Distinguish the start command, background progress, and result records.']),
         (['Host Memory Buffer','理解主機記憶體如何提供給控制器，以及可回收的時機。'],['Host Memory Buffer','Understand how host memory is made available to the controller and when it can be reclaimed.']),
         (['記憶體與命令延伸','理解 descriptor、Doorbell Emulation 與 vendor command 長度的界線。'],['Memory and command extensions','Understand descriptors, Doorbell Emulation, and vendor-command length boundaries.'])],
        b(['主機和控制器各自有記憶體；能夠提供某段記憶體的位址，不代表另一方已停止使用它。這與 OS 中記憶體生命週期的概念相通。'],
          ['The host and controller each have memory. Knowing the address of a region does not establish that the other party has stopped using it, much like memory-lifetime rules in an operating system.'])),
    'base-self-test-namespace-management': context(
        b('Device Self-test 用來理解裝置測試的結果；Namespace Management 用來建立與管理主機可存取的儲存空間。本篇把測試結果、容量與格式選擇，以及 namespace 的建立、附加、刪除和還原分開說清楚。',
          'Device Self-test reports device-test outcomes; Namespace Management creates and manages host-accessible storage. This note separates test results, capacity and format selection, and namespace creation, attachment, deletion, and restoration.'),
        [(['測試與結果','分清命令完成、測試完成與有效的結果欄位。'],['Tests and results','Distinguish command completion, test completion, and valid result fields.']),
         (['容量與格式','理解容量單位、配置粒度及 LBA 格式選擇。'],['Capacity and formats','Understand capacity units, allocation granularity, and LBA format selection.']),
         (['Namespace 生命週期','把建立、附加、刪除與還原視為不同的狀態改變。'],['Namespace lifecycle','Treat creation, attachment, deletion, and restoration as different state changes.'])],
        b(['Namespace 是控制器呈現給主機的邏輯儲存空間，以 NSID 識別。建立 namespace 與把它附加至 controller 是兩個步驟，不能由其中一步推論另一步已完成。'],
          ['A namespace is logical storage exposed to the host and identified by NSID. Creating it and attaching it to a controller are separate steps; completing one does not establish completion of the other.'])),
}
