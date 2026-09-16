# Flexible Data Placement maintenance record

The user requested this independent report on 2026-09-15. Three artifacts are
dated 2026-09-16: an independently written Traditional Chinese beginner-to-advanced
HTML course and equivalent Chinese/English overview posts with a forward PDF route.
Publication and push are authorized by the continuing project instructions.

Primary Base 2.4 scope: 8.1.12, 3.2.4, 8.1.9.4, 7.3, 7.4,
5.2.30.1.21–22 (FID 1Dh/1Eh), 5.2.13.1.29–32 (LID 20h–23h).
Primary NVM 1.3 scope: 3.2, 4.1.4.6–7. Earlier reports' exclusions are unchanged.
Fabrics, Discovery and NQN remain excluded.

There are 33 primary figures: Base 70, 293–303, 499–506, 650–657, 730–732;
NVM 21 and 116. The register separately lists 26 necessary reference slices.
Every selected figure has a distinct takeaway and example; related field rules
are explained together once. Four diagrams and five comparisons/flows are placed
along the course where they answer a concrete question.

The tutorial does not require live specification navigation. The posts use actual
viewer pages: Base 110–111, 319–327, 506–509, 594–597, 653, 673–678;
then a single switch to NVM 26 and 79. Shared-page stopping headings are explicit.

Source-reading pitfalls retained for future maintenance:

- NUMFDPC and NPID use count-minus-one encoding; NPHNDLS, NRUH, NRUHSD and NOET
  are direct counts. The last-row labels in some source tables are inconsistent
  with their stated count encoding; follow the field definitions and verify offsets.
- Base's prose near the namespace mapping cites Figure 729; the actual FDP mapping
  diagram is Figure 730. Figure 729 belongs to the preceding excluded topic.
- NVM 4.1.4.7.1.1 has an inconsistent “Event Type 0h” heading. The outer Media
  Reallocated event code is 80h in Base Figure 303; NVM Figure 116 defines its ETSP,
  not a new outer event encoding. Do not silently teach Media Reallocated as 00h.
- Figure 129 continues on pages 104–105 without repeating its caption. The selected
  DSM fields are there, not on caption page 103. Figure 346 is Base 5.2.14.2.8.
- Invalid Write PIDs cause placement fallback with conditional event logging;
  invalid Update PIDs cause rejection, potentially after partial updates.
- Data Placement enablement persists across Controller Level Reset. This does not
  promise that RUH references, remaining capacity, event enablement or snapshots
  are unchanged. Do not copy Streams' persistence behavior into FDP.
- RUAMW is logical blocks, RUNS bytes, ERUTL/EARUTR seconds. PID is not RUHID.
- A Media Reallocated LBA is one moved LBA, not the start of a contiguous range.
- The current NVM revision interprets zero DSM limit fields with NVMDSMSV: when
  the support bit is one, zero reports no recommended limit; when zero, the fields
  participate in command support. Never reduce this to “zero always means unlimited.”
- FID 1Dh requires SV=1 for changing values and no existing namespace in the group.
  A successful value change clears FDP statistics and events. Firmware update does
  not clear the statistics.

Private PDFs, full extracted text and rendered source pages remain untracked.
Public outputs contain self-authored explanations, examples, diagrams and precise
locations, not copies of the source tables.
