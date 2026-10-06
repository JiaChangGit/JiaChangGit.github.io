# Independent NVMe question bank — Q1–Q328

Expanded with explicit authorization on 2026-10-02. Purpose: learn the specification and judge firmware behavior.
The current delivery is 27 volumes plus an index, each in standalone Traditional Chinese
HTML and equivalent Traditional Chinese/English Pages. The Chinese HTML adds
independent teaching steps and an APST state example. It does not require following
a presentation route through the PDF.

## Scope and editorial decisions

Use the three registered ratified PDFs. Exclude Fabrics and PCIe link/packet details;
retain PCIe configuration, interrupts, registers, queues and doorbells needed for
NVMe SSD behavior. Shared PDF pages can include excluded material; citing a page
does not authorize teaching all of that page.

The user explicitly authorized completing Q69–Q320, superseding the earlier
Q1–Q68-only delivery. All 320 original IDs were completed in 26 topic volumes. The 2026-10-03 supplement
adds Q321–Q328 as a separate data-I/O volume under the user’s express permission
to fill genuine gaps. Original IDs and URLs remain unchanged. Earlier scope
statements below are historical records.
Unreasonable premises are corrected without losing their subject: Q273 does not
invent a media-unit availability bit; Q290 distinguishes coalescing from masking;
Q312 distinguishes the Abort completion from the target completion.


## Source review findings

- Base Figure 104 (SCT=1) assigns I/O Command Set Combination Rejected to 2Bh,
  while the supplied Figure 554 lists 15h for the same name. Q58 preserves both
  source locations and flags the conflict; do not resolve it by inventing a value.
  No additional errata were supplied.
- Reserved bits/fields and reserved encodings in defined fields have different
  recipient obligations. A nonzero reserved bit is not automatically a mandatory
  Invalid Field completion.
- CQ-before-SQ and deleting every dependent SQ before a CQ are dependencies, not
  performance recommendations. Queue allocation, entry count and instantiated
  queues are separate quantities.
- Create CQ's CQR/PC error uses shall; Create SQ uses should. Keep the difference.
- SQHD reports consumption, not completion of every preceding command. CID is
  unique among outstanding commands in one SQ, not globally across all queues.
- Initial phase, modular pointer movement and one-unused-slot full detection must
  be explained together. A successful CQE still needs a valid phase and identity.
- DNR=0 permits a possible successful retry, not guaranteed immediate identical
  retry. MMIO does not have a CQE. Do not prescribe command statuses for undefined
  register/doorbell use.
- PEL Set Feature recording requires the supported FID and event, successful Set
  and a changed setting; repeating the same value may be logged. Timestamp uses
  its separate event and is prohibited from Set Feature logging. Power Management
  Set Feature logging is Not Recommended, not Mandatory.
- A secondary controller can set CFS while Offline; CFS alone is not sufficient to
  diagnose a physical hardware fault in that configuration.
- FID07h allocations can be less or more than requested. After the first successful
  Set in a CLR lifetime they remain fixed until the next CLR.
- FID84h is unsaveable with no Default, but state retention is explicit. Do not
  equate unsaveable with volatile. Timestamp may restore an older Saved value;
  observe Origin as well as the timestamp when comparing reset behavior.

## Implementation and checks

Content: topic modules `scripts/nvme_qa_*.py`; the load list in `nvme_qa_model.py` orders dependencies.
`nvme_qa_teaching_extended.py` adds 20 independent courses; `nvme_qa_review.py` records explicit cross-topic corrections.
The model retains all 17 bilingual items. Shared mechanisms are rendered in full
once per volume, with a concise applicable answer and local link in each question.
Question anchors (`q-001`) and answer anchors (`q-001-a-01`) are independent of
volume and paragraph counters. Index navigation preserves practice-first disclosure;
a deep answer anchor reveals the containing answer. Native details remain usable
without JavaScript; search, mass disclosure and explicit theme switching are optional
enhancements. Before printing, all answers open and restore their state afterward.

Source evidence records each locator, figure-heading pages, selected-page digest
and all three file hashes. No PDF or extracted prose is committed. The source audit
uses actual body positions, not the occasionally inconsistent cross-references.

```sh
python3 -B scripts/build_nvme_question_bank.py
python3 -B scripts/build_nvme_question_bank.py --check
python3 -B scripts/nvme_qa_sources.py --check
python3 -B scripts/nvme_qa_sources.py --source-dir /path/to/original/pdfs
python3 -B scripts/build_nvme_quickref.py --check
python3 -B scripts/validate_nvme_report.py --phase publish
python3 -B -m unittest discover -s tests -v
```

Source changes require `nvme_qa_sources.py --source-dir ... --refresh` after reading
the changed pages. CI checks registered evidence without requiring private PDFs.
`build_nvme_reports.py` owns the NVMe landing page; update its generated link block.
Standalone outputs embed both stylesheets; Pages load the scoped extra stylesheet
through `nvme_qa: true`. Theme colors follow explicit site choice even when OS color
preference is opposite.

Validation performed: all three PDF hashes and 58 locator groups; 117 unit tests;
old 66-artifact publication contract and 24-artifact quick-reference drift check;
Jekyll production build; 252 browser states covering 21 outputs × three sizes ×
light/dark × collapsed/expanded, with no missing anchors, duplicate IDs, whole-page
overflow or text contrast failures. Keyboard disclosure, search, expand/collapse,
deep answer links, explicit theme toggle and offline standalone navigation tested.
Representative source page 541 and both-language rendered screenshots inspected.
The final wording updates are followed by a targeted browser check and rebuild.

## 2026-10-01 Chinese editorial review

The user reaffirmed that Q69–Q320 remain future scope. This revision reviews
Q1–Q68, their Chinese introductions, teaching examples, tables and shared rules.
The persistent writing requirements are recorded at the top of `AGENTS.md`:
use natural Taiwan Traditional Chinese, check connective words against the actual
logical relationship, make pronoun references and changes of actor explicit, and
prefer complete explanations over compressed fragments. Longer text is acceptable
when it supplies a missing condition, action or consequence; repetition is not.

The review revised 561 authored answer passages and 103 shared/teaching strings,
plus reader instructions. For example, “通知已消費完成” now identifies the Host,
the CQ Head Doorbell and the completion positions being released. State changes
and reset rules now name which value or object changes before explaining the result.
Numerical formulas and compact field mappings remain where they aid lookup.
Question IDs, the 17-item structure, source locators, status-code exceptions and
all seven generated English files are unchanged. No new topic or technical
requirement was added by this language revision.

Editorial validation: 117 tests passed, 58 source locator groups verified, old report
and quick-reference contracts unchanged, and production Jekyll build passed.
All 14 Chinese outputs passed 168 browser states (three viewport sizes, both themes,
collapsed/expanded), with no overflow, missing anchors, duplicate IDs or contrast
failures. Search, keyboard disclosure, deep links and offline navigation also passed.
Representative light/dark screenshots were inspected. After the final queue-example and
APST wording cleanup, the 11 question-bank tests and 48 targeted browser states
passed again, and the production site was rebuilt.

## Publication pitfalls

Do not set a post's timestamp later than the actual publication time. A noon time
on today's date was initially excluded by a morning Jekyll build. Use an elapsed
timestamp (question-bank posts use 00:00 +0800), build without `--future`, and
require every declared post URL to exist in the output (54 in the expanded bank). Do not enable `future` globally to hide this.

Keep the repository's existing Ruby/Bundler pair (Ruby 3.3.8, Bundler 2.6.7) and pinned
actions. The historical Ruby 3.0.7/Bundler compatibility failure must not recur.
After push, both validation and Pages workflows must succeed for the same commit;
check deployed question IDs, all 17 items and the new stylesheet, not only HTTP 200.


## 2026-10-02 expansion source decisions

- All 320 questions retain 17 bilingual perspectives; 26 volumes and an index
  produce 81 artifacts. Original URLs and Q/answer anchors are retained. The
  integration volume links to mechanism questions rather than duplicating them.
- Namespace Sanitize permits Crypto Erase only; subsystem OWS does not authorize
  namespace Overwrite. Initiation completion is separate from operation completion.
- Base Figure 104 gives MNSOIP-limit error 3Ch, while Figure 455 gives 12h.
  Q135 preserves the conflict, without silently choosing one encoding.
- Base Capacity Management insufficient-capacity prose (PDF220) describes the
  largest creatable capacity, while Figure165 (PDF221) describes required capacity.
  Q265 preserves this conflict for command-specific error information.
- PEL Supported Events bitmap Figure233 reserves bit16 while Figure236 defines
  Event Type10h; Q205 flags the discrepancy. No supplied errata resolves it.
- Short self-test aborts on CLR; extended testing persists/resumes after CLR and
  power restoration. Neither defines a generic self-test-completed AER.
- PEL has no universal PEL-changed AER. Timestamp uses Event03h, not generic Set
  Feature logging; reporting-context lifetime must not replace clock retention rules.
- UPL (formerly Unsafe Shutdowns) follows actual main-power loss and shutdown state,
  not a blanket Normal/Abrupt label. Preserve the applicable Ignore Shutdown exception.
- PCIe Admin commands cannot use SGLs; SDT is a recommendation, not a universal
  rejection limit. Do not import capsule-only descriptor-count limits into PCIe.
- FID09h.CD is coalescing disable. INTMC uses write-one-to-clear. MSI-X masking
  uses its own table/function masks; INTMS/INTMC access is undefined in that mode.
- Media Unit wear fields do not define namespace readiness. FDP PH is namespace
  specific and maps to RUH; write-PID fallback does not apply to invalid RUH Update.
- Firmware source cross-references, Boot register/log locations, FDP figures and
  Changed Namespace/Effects aliases use actual body headings in the provided PDFs.
- Existing Ruby3.3.8/Bundler2.6.7 workflow is retained. Do not revert to Ruby3.0.7
  with an incompatible unpinned Bundler. Verify both workflows at the pushed SHA.

Editorial review keeps Taiwan Traditional Chinese complete subjects and logical
connectives; simplified-character repairs do not substitute for sentence review.
Shared event/reset descriptions are selected by the actual operation, including
Timestamp, Boot reads, namespace queries and group-health queries.


## 2026-10-03 expansion validation

- Generated 81 artifacts: 26 topic volumes and one index, each in three editions.
  Every original question ID 1–320 has all 17 perspectives; no overlapping extra
  questions were added. New posts retain their 2026-10-02 authoring date.
- All 122 tests passed after the final question/common-rule wording changes.
  Production Jekyll build, generated-artifact checks, publish contract and the
  existing 117-figure quick-reference check passed.
- Source evidence checks cover 320 questions, 123 locator groups and the identities
  of all three supplied PDFs. Their full text and rendered source images stay in
  ignored local files and are not published.
- Checked 22,221 internal links, including cross-volume question links and source
  anchors, against the production site; none were missing.
- Browser checks cover 81 pages at 834, 1194 and 1440 pixels, both explicit themes
  against the opposite system theme, and collapsed/expanded answers: 972 states.
  They check overflow, contrast, missing anchors and duplicate IDs. Keyboard
  disclosure, search, deep answer links, theme selection and offline navigation
  are also exercised. Representative light/dark screenshots are reviewed.
- The final index spacing and health-flow arrow styling are followed by a targeted
  72-state browser recheck. These changes do not alter question answers or sources.
  Q213 then expands the existing header-field definitions and length example, with
  a further 36-state check of its three editions; its source locations are unchanged.
- Keep command-reset behavior distinct from log-query lifetime; keep PRP/SGL buffer
  retirement distinct from queue-register retention. Shared prose is selected for
  the actual operation rather than copied solely because an answer asks about reset.


## 2026-10-03 data-I/O supplement

Q321–Q328 add eight distinct reasoning tasks: MDTS/metadata/range validity;
Write/Flush/FUA persistence; atomic units and boundary crossings; Read/Compare/
Verify evidence; Write Zeroes versus deallocation and DULBE; a constrained PI
example; Copy partial-completion evidence; and intentional Write Uncorrectable
marks versus physical-media diagnoses. The original questions cover the related
features and error mechanisms, which remain canonical and are linked rather than
copied. All eight have 17 bilingual answer perspectives; the standalone Chinese
volume adds four lessons and a boundary comparison using stated hypothetical
values. There are now 84 artifacts: 27 volumes plus an index in three editions.

Source review adds ten locator groups (133 total) and preserves all three original
PDF identities. Important boundaries include MEM metadata accounting, zero-value
exceptions in atomicity fields, VSL/WUSL advisory variants, PI escape tags and
Copy descriptor-format-specific overlap rules. Do not treat Copy DW0 as a safe
resume cursor, Verify as an application-content comparison, or a successful
Write Zeroes followed by DULBE as proof that zeroing failed.

Validation for the supplement: all 125 tests passed, including independently
calculated MDTS/metadata, atomic-boundary and Copy-range examples. The production
Jekyll build, report publication contract, source-evidence check and existing
quick-reference check passed. All 22,941 local links across the 84 artifacts resolve.
The new volume and index were exercised in all three editions at three viewport
widths, in both explicit themes and with answers closed/open (72 states), with no
overflow, contrast or anchor errors. Representative light/dark screenshots were
reviewed, including the boundary comparison and English answers. Search, keyboard
disclosure, deep links and standalone offline navigation also passed. Original
Q1–Q320 content is unchanged; the full earlier browser pass remains recorded above.


## 2026-10-04 capability lookup routes

Kept 328 questions and 27 volumes. The user's Sanitize Namespace example is
implemented inside Q118 instead of adding a near-duplicate question. Q81 explains
the general Admin/I/O entry distinction; Q69 provides a log-support lookup; Q54
separates FID support, saveability and current state. Each worked table retains
original figure and printed/PDF page positions, query parameters, hypothetical
responses, byte/bit decoding and limits on the resulting claim. All three editions
include these worked answers, folded inside the existing 17-part answer.

Q118 now describes a read-only capability query throughout its event/log/reset
answers rather than inheriting Format/Sanitize operation effects. Q134/Q135 link
back to that canonical support route. Corrected Q50/Q81 to Figure338 LPA.CSES
and Q69/Q75 to LPEDS. Figure211's cross-reference calls the latter SPEDS; retain
the actual Identify field-table name and position (LPA bit2), not a new bit.

SANICAP.CES and NVERS do not replace Admin8Ch CSUPP. Figure28's Optional is a
specification requirement classification, not an observation of the device.
Figure216 locates the entry at4×8Ch=230h; Figure217 bit0 interprets it. A failed
LID05h read is missing evidence, not CSUPP0. Lookup examples never initiate erase
or alter feature values. Source PDFs and rendered source pages stay private.

Validation: 128 tests and the publication contract passed, with 23,070 internal
links resolved across all 84 artifacts. Original PDFs verify 134 locator groups.
The five changed page groups (including index and the field-name correction)
passed 180 browser states across three editions, three widths, two explicit themes
and both answer disclosure states. Chinese and English lookup tables were visually
reviewed. Final field/value spacing receives a focused follow-up on the three
worked-route volumes. Offline navigation, search and keyboard disclosure passed.


## 2026-10-05 — Answers follow the question, not the 17-part prompt

The user explicitly changed the output contract: the original 17 perspectives
are optional prompts for the author. They are no longer required answer sections.
This supersedes the historical 17-item requirements above and in older AGENTS
entries. Q1–Q328, the 27 volumes, all three editions and existing URLs remain.

Every question now has an explicit reading plan in `nvme_qa_presentation.py`.
The plans distinguish field interpretation, comparisons, capability lookup,
procedures, concepts, errors, diagnosis, lifetime and events. Simple questions
have bespoke shorter explanations; operation-specific error and retention rules
remain where they actually answer the question. General MMIO/command event and
reset boilerplate is not emitted into hidden or visible answer HTML.

The legacy `answers` keys remain editorial material and compatibility anchors,
not a requirement for future authors. Old `q-NNN-a-NN` fragments still open the
revised answer; there are no hidden copies of the removed paragraphs. Necessary
shared rules are explained once and linked locally. Relevant detail moved out of
introductory comparisons links to its existing canonical question.

Twelve bilingual, offline flows replace the paragraphs they explain: Q3, Q12,
Q27, Q75, Q84, Q113, Q191, Q206, Q226, Q232, Q277 and Q299. The diagrams distinguish
submission from completion, alternative branches from sequential operations,
and successful information retrieval from successful background operations.
Q3 retains CRTO timing origins and PEL/DNR failure conditions. Q113 does not turn
host recovery policy into a mandatory Abort→Queue Reset→Controller Reset chain.
Q277 uses the first-page offset before choosing the meaning of PRP2.

The underlying source locations and three PDF identities are unchanged. The
restructured renderer preserves the source index, worked capability queries,
standalone teaching lessons and counterpart Chinese/English content. No new
question was needed: this change improves existing learning objectives without
creating similar questions.

Completion validation on 2026-10-06: 132 tests passed; the final question-bank
subset passed all 26 tests after the last editorial adjustments. All three source
PDF hashes and 134 locator groups were checked. The 84 generated artifacts match
the builder, the publication contract passes, and 15,561 local links resolve.
Browser verification covered 1,008 states across all 84 editions (three viewport
sizes, two explicit themes and folded/expanded answers), plus 144 focused states
after final edits. All passed contrast, overflow, fragment and duplicate-ID checks.
All 12 explanatory flows, a concise answer and a retention comparison were
visually reviewed. Offline navigation, keyboard disclosure, search, theme changes
and legacy deep links passed. Q172 specifically excludes the old unrelated
Attachment retention text; Q195 links the established feature-specific comparison
instead of repeating a generic reset table.
