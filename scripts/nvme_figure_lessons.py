"""Fail closed when a published source figure has no authored teaching."""
from scripts.nvme_figure_examples_base import LESSONS as BASE
from scripts.nvme_figure_examples_nvm import LESSONS as NVM
from scripts.nvme_figure_examples_pcie import LESSONS as PCIE

CATALOG = {'NVME-BASE-2.4':BASE,'NVME-NVM-CS-1.3':NVM,'NVME-PCIE-TRANSPORT-1.4':PCIE}

def lesson(figure):
    # Deliberately no caption-based fallback: missing examples stop publication.
    return CATALOG[figure['source_id']][int(figure['number'])]

def detail(figure):
    source,number=figure['source_id'],int(figure['number'])
    if source=='NVME-NVM-CS-1.3':
        from scripts.nvme_nvmcs_figures import DETAILS
        return DETAILS[number]['text']['zh']
    if source=='NVME-BASE-2.4' and figure['report_id'] in {'base-boot-partitions','base-telemetry','base-sanitize'}:
        from scripts.nvme_bts_figures import guide_for
        return guide_for(dict(figure,report_id='base-boot-telemetry-sanitize'),'zh')
    from scripts.nvme_figure_notes import note
    return note(figure,'zh') or ''
