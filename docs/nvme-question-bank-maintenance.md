# Independent NVMe question bank — Q1–Q68

Approved 2026-10-01. Purpose: learn the specification and judge firmware behavior.
This delivery is six volumes plus an index, each in standalone Traditional Chinese
HTML and equivalent Traditional Chinese/English Pages. The Chinese HTML adds
independent teaching steps and an APST state example. It does not require following
a presentation route through the PDF.

## Scope and editorial decisions

Use the three registered ratified PDFs. Exclude Fabrics and PCIe link/packet details;
retain PCIe configuration, interrupts, registers, queues and doorbells needed for
NVMe SSD behavior. Shared PDF pages can include excluded material; citing a page
does not authorize teaching all of that page.

The user supplied Q69–Q320 for later work and explicitly limited this delivery to
Q1–Q68. Future ranges are preserved in `.ai/nvme-question-bank/scope.json`, including
all chapters VII–XXVI. The user subsequently allowed additional non-overlapping
questions and correction of unreasonable question premises. Keep the original IDs;
correct premises without silently changing the subject. This delivery adds no extra
questions because the supplied 320-question plan already covers the adjacent topics.
Q12 and Q17 now ask about required creation/deletion dependencies rather than
implying that the order is merely usual. Future Q290 must not describe FID09h.CD as
interrupt masking: it disables coalescing, while masks are separate PCIe mechanisms.

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

Content: `scripts/nvme_qa_{init,queues,doorbells,commands,identify,features}.py`.
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
timestamp (this batch uses 00:00 +0800), build without `--future`, and require all
14 post URLs to exist in the output. Do not enable `future` globally to hide this.

Keep the repository's existing Ruby/Bundler pair (Ruby 3.3.8, Bundler 2.6.7) and pinned
actions. The historical Ruby 3.0.7/Bundler compatibility failure must not recur.
After push, both validation and Pages workflows must succeed for the same commit;
check deployed question IDs, all 17 items and the new stylesheet, not only HTTP 200.
