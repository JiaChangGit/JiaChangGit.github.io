"""Small escaped components shared by explicitly selected teaching series."""
from html import escape

SERIES_REPORTS = frozenset({'pcie-transport-1.4','nvm-command-set-1.3'})

def specification_badges(series='nvme'):
    labels = (['PCI Express Base 6.0'] if series=='pcie' else
              ['NVM Express Base 2.4','NVM Command Set 1.3','NVMe over PCIe Transport 1.4'])
    return '<div class="st-specs" aria-label="Specification editions">'+''.join('<span>'+escape(label)+'</span>' for label in labels)+'</div>'

def reading_route(identifier, title, steps, language='zh'):
    """A reading route, explicitly distinct from hardware execution order.

    Each step is (heading, explanation, [(label, local_fragment_or_path)]).
    Strings are text, never interpolated as executable HTML.
    """
    out=['<section class="st-route" id="'+escape(identifier,quote=True)+'"><h4>'+escape(title)+'</h4>',
         '<p class="st-route-help">'+('下面是閱讀規格的順序；實際操作的先後與等待條件，會在情境解說中另外交代。' if language=='zh' else 'This is a specification reading route. The scenario separately explains action order and wait conditions.')+'</p>',
         '<ol class="st-reading-route">']
    for heading,explanation,links in steps:
        out.append('<li><strong>'+escape(heading)+'</strong><p>'+escape(explanation)+'</p>')
        for label,url in links:
            if url.startswith('//') or '\\' in url or ':' in url or '..' in url.split('/'):
                raise ValueError('Reading links must use local fragments or repository paths')
            out.append('<a href="'+escape(url,quote=True)+'">'+escape(label)+'</a>')
        out.append('</li>')
    return '\n'.join(out+['</ol></section>'])
