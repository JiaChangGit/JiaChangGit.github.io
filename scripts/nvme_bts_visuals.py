"""A compact, original transition map with a searchable text equivalent."""
import html
import textwrap

TRANSITIONS = [
    ('Idle', 'A1: AUSE=0', 'Restricted Processing'),
    ('Idle', 'B1: AUSE=1', 'Unrestricted Processing'),
    ('Restricted Processing', 'C1: success; no verification', 'Idle'),
    ('Restricted Processing', 'D1: processing fails', 'Restricted Failure'),
    ('Restricted Processing', 'F1: success; EMVS=1; not canceled', 'Media Verification'),
    ('Restricted Failure', 'A2: restricted retry', 'Restricted Processing'),
    ('Unrestricted Processing', 'C2: success; no verification', 'Idle'),
    ('Unrestricted Processing', 'D2: processing fails', 'Unrestricted Failure'),
    ('Unrestricted Processing', 'F2: success; EMVS=1; not canceled', 'Media Verification'),
    ('Unrestricted Failure', 'A3: restricted retry', 'Restricted Processing'),
    ('Unrestricted Failure', 'B2: unrestricted retry', 'Unrestricted Processing'),
    ('Unrestricted Failure', 'E: Exit Failure Mode', 'Idle'),
    ('Media Verification', 'G: exit / applicable reset / cancellation', 'Post-Verification Deallocation'),
    ('Post-Verification Deallocation', 'H: deallocation succeeds', 'Idle'),
    ('Post-Verification Deallocation', 'I1: failure; original AUSE=0', 'Restricted Failure'),
    ('Post-Verification Deallocation', 'I2: failure; original AUSE=1', 'Unrestricted Failure'),
]


def state_svg():
    out = ['<svg viewBox="0 0 1000 1430" role="img" data-visual-kind="state" aria-label="Sanitize state transitions">',
           '<title>Sanitize state transitions</title><desc>Each row is one directed transition. C1/C2 require successful processing and either no requested verification, or canceled verification with successful deallocation. Sources: Base Figures 772 through 779.</desc>',
           '<text x="20" y="28" class="v-text">Object / start state</text><text x="338" y="28" class="v-text">Gate / transition condition</text><text x="710" y="28" class="v-text">Object / end state</text>']
    for i, (start, gate, end) in enumerate(TRANSITIONS):
        y=45+i*80
        fail='Failure' in end
        out.extend([f'<rect x="10" y="{y}" width="305" height="62" rx="8" class="v-node v-object"/>',
                    f'<rect x="685" y="{y}" width="305" height="62" rx="8" class="v-node {"v-failure" if fail else "v-object"}"/>',
                    f'<rect x="325" y="{y}" width="350" height="44" rx="4" class="v-decision"/>',
                    f'<path d="M318 {y+54} H681 l-8 -5 m8 5 l-8 5" class="v-line"/>',
                    f'<text x="22" y="{y+29}" class="v-text" font-size="16">{html.escape(start)}</text>',
                    f'<text x="697" y="{y+29}" class="v-text" font-size="16">{html.escape(end)}</text>'])
        for j,line in enumerate(textwrap.wrap(gate, width=38)):
            out.append(f'<text x="500" y="{y+18+j*19}" text-anchor="middle" class="v-text">{html.escape(line)}</text>')
    out.extend(['<text x="20" y="1350" class="v-text">C1/C2: EMVS=0, or MVCNCLD=1 with successful deallocation.</text>',
                '<text x="20" y="1380" class="v-text">Idle after E does not prove successful sanitization.</text>', '</svg>'])
    return '\n'.join(out)


def module_svg(module, language):
    """Reading-order diagrams avoid inventing host/buffer/controller traffic."""
    if module['id'] == 'sanitize-state':
        return state_svg()
    nodes = module['nodes'][language]
    height = 70 + len(nodes)*95
    out = [f'<svg viewBox="0 0 540 {height}" role="img" aria-label="{html.escape(module["title"][language])}">',
           '<title>Reading and operation order</title><desc>Follow the numbered interpretation steps; this is not a bus transaction trace. Conditions and alternatives are in the adjacent comparison table.</desc>']
    for i, label in enumerate(nodes):
        y = 25+i*95
        role = 'v-decision' if i == 0 else ('v-success' if i == len(nodes)-1 else 'v-object')
        out.append(f'<rect x="25" y="{y}" width="490" height="66" rx="10" class="{role}"/>')
        for j,line in enumerate(textwrap.wrap(f'{i+1}. {label}', width=42)):
            out.append(f'<text x="270" y="{y+28+j*23}" text-anchor="middle" class="v-text">{html.escape(line)}</text>')
        if i < len(nodes)-1:
            out.append(f'<path d="M270 {y+68} v23 l-5 -7 m5 7 l5 -7" class="v-line"/>')
    out.append('</svg>')
    return '\n'.join(out)


def state_text():
    return ['| Start state | Condition | End state |', '|---|---|---|'] + ['| '+' | '.join(row)+' |' for row in TRANSITIONS]


def state_table():
    return '<div class="table-wrap"><table><caption>Sanitize transition lookup / 狀態轉移索引</caption><thead><tr><th>Start state</th><th>Condition</th><th>End state</th></tr></thead><tbody>' + ''.join('<tr>' + ''.join('<td>'+html.escape(cell)+'</td>' for cell in row) + '</tr>' for row in TRANSITIONS) + '</tbody></table></div>'
