"""Exact, report-local scope for the user's Admin/I/O specification walkthrough."""
REPORT_ID = 'admin-io-spec-walkthrough'
BASE = 'NVME-BASE-2.4'
NVM = 'NVME-NVM-CS-1.3'

SPECIAL_TOPICS = {
    BASE: ['8.1.8', '5.2.6', '5.2.13.1.7', '8.1.17', '5.2.24', '5.2.25',
           '8.1.3', '5.2.13.1.21', '5.2.30.1.39', '8.1.30', '5.2.13.1.8',
           '5.2.13.1.9', '8.1.27', '5.2.13.1.38', '5.2.26', '5.2.30.1.16'],
    NVM: ['4.1.4.3', '2.1.1', '4.1.6', '5.8', '4.1.7', '5.12'],
}
EXCLUDED_BASE_SECTIONS = [
    '8.1.17.3', '8.1.27.6', '5.1.2', '5.2.3', '5.2.4', '5.2.5', '5.2.7',
    '5.2.8', '5.2.13.3', '5.2.14.4', *['5.2.'+str(n) for n in range(15,24)],
    '5.2.27', '5.2.30.3', '5.2.31', '5.2.32', '5.3.5', '5.3.6', '5.4',
    '7.1', *['7.'+str(n) for n in range(3,9)],
]
EXCLUDED_FIDS = {0x0F,0x12,0x13,0x14,0x16,0x18,0x1A,0x1B,0x1D,0x1E,0x1F,
                 *range(0x21,0x28),0x78,0x79,0x7D,0x7E,0x7F,*range(0x81,0x85)}
EXCLUDED_LIDS = {0x09,0x0A,0x0B,0x0C,0x0D,0x0F,0x10,0x11,0x13,0x14,0x16,
                 0x17,0x18,0x1A,0x1B,0x1C,0x1D,*range(0x20,0x24),0x25,0x27,0x7F,0x80}
EXCLUDED_CNS = {0x17,0x14,0x15,0x21,0x22}
NVM_INCLUDED = [*['3.3.'+str(n) for n in range(1,9)], '4.1.1', '4.1.2',
                '4.1.3.1', '4.1.3.2', '4.1.3.4', '4.1.4.1', '4.1.4.2', '4.1.5', '5.6']


def within(section, root):
    return section == root or section.startswith(root+'.')


def included(source, section, *, fid=None, lid=None, cns=None):
    if any(within(section, s) for s in SPECIAL_TOPICS.get(source, [])):
        return False
    if fid in EXCLUDED_FIDS or lid in EXCLUDED_LIDS or cns in EXCLUDED_CNS:
        return False
    if source == BASE:
        return (within(section, '5') or within(section, '7')) and not any(
            within(section, s) for s in EXCLUDED_BASE_SECTIONS)
    if source == NVM:
        return any(within(section, s) for s in NVM_INCLUDED)
    return False


def validate_manifest(manifest, figures, outputs):
    """Check source boundaries and the actual route rendered in every edition."""
    import re
    errors = []
    expected = {'base_roots':['5','7'], 'nvm_roots':NVM_INCLUDED,
                'special_topic_sections':SPECIAL_TOPICS,
                'excluded_base_sections':EXCLUDED_BASE_SECTIONS,
                'excluded_fids':[f'{n:02X}h' for n in sorted(EXCLUDED_FIDS)],
                'excluded_lids':[f'{n:02X}h' for n in sorted(EXCLUDED_LIDS)],
                'excluded_cns':[f'{n:02X}h' for n in sorted(EXCLUDED_CNS)]}
    if manifest.get('selection') != expected:
        errors.append('Admin/I/O selection differs from the approved exclusions')
    routes = manifest.get('routes', [])
    sources = [r['source_id'] for r in routes]
    if not sources or sources[0] != BASE or sources[-1] != NVM or sum(a!=b for a,b in zip(sources,sources[1:])) != 1:
        errors.append('Admin/I/O route must switch once from Base to NVM')
    previous = {}; headings = {}; selectors = {k:set() for k in ('fid','lid','cns')}
    for r in routes:
        src=r['source_id'];start=r['start_pdf_page'];end=r['end_pdf_page']
        if start > end or start < previous.get(src,0):
            errors.append(f'{r["id"]}: PDF route moves backwards')
        previous[src]=end
        if not r.get('stop_before_section') or not r.get('sections') or r['start_section']!=r['sections'][0]['section']:
            errors.append(f'{r["id"]}: missing or inconsistent section boundary')
        for h in r['sections']:
            args={k:h[k] for k in selectors if k in h}
            if not included(src,h['section'],**args):
                errors.append(f'{r["id"]}: excluded section/selector {h["section"]}')
            if not start<=h['pdf_page']<=end:
                errors.append(f'{r["id"]}: heading outside the PDF interval')
            headings[src,h['section']]=h
            for k,v in args.items():selectors[k].add(f'{v:02X}h')
    for key, values in selectors.items():
        if set(manifest['included_selectors'][key]) != values:
            errors.append(f'Admin/I/O retained {key} list differs from selected headings')
    manifest_figures={f['id']:f for f in manifest['included_figures']}
    registered={f['id']:f for f in figures if f['report_id']==REPORT_ID}
    if set(manifest_figures)!=set(registered):
        errors.append('Admin/I/O figure inventory differs from the route manifest')
    for f in registered.values():
        if (f['source_id'],f['section']) not in headings:
            errors.append(f'{f["id"]}: figure outside selected headings')
        m=manifest_figures.get(f['id'],{})
        if any(m.get(k)!=f.get(k) for k in ('source_id','section','number','pdf_pages')):
            errors.append(f'{f["id"]}: inconsistent figure source location')
        pages=[int(n) for n in re.findall(r'\d+',f['pdf_pages'])]
        offset=26 if f['source_id']==BASE else 0
        if [int(n) for n in re.findall(r'\d+',f['printed_pages'])] != [n-offset for n in pages]:
            errors.append(f'{f["id"]}: printed and viewer page numbers disagree')
    expected_rows=[(r['id'],r['source_id'],str(r['start_pdf_page'])) for r in routes]
    for artifact,text in outputs.items():
        rows=re.findall(r'<tr id="route-([^"]+)" data-route-source="([^"]+)" data-pdf-page="(\d+)"',text)
        if rows!=expected_rows:
            errors.append(f'{artifact}: published PDF route missing or out of order')
    return errors
