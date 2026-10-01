"""Spec-only exercises integrated into the existing eight figure-reference pages.

All observations are hypothetical. Pairs keep Chinese and English claims aligned.
References use an existing figure plus exact PDF pages, or a section-only source.
"""
CASES = []

def case(topic, title, question, observations, route, steps, figures, sources):
    number = sum(c['topic'] == topic for c in CASES) + 1
    assert len(steps) >= 3
    assert all(len(pair) == 2 for pair in [title, question, route] + observations + steps)
    CASES.append(dict(id=f'{topic}-{number:02d}', topic=topic, title=title,
                      question=question, observations=observations, route=route,
                      steps=steps, figures=figures.split(), sources=sources.split()))

def load():
    from scripts import nvme_scenarios_identify, nvme_scenarios_io, nvme_scenarios_features
    from scripts import nvme_scenarios_logs, nvme_scenarios_init
    from scripts import nvme_scenarios_command, nvme_scenarios_maintenance
    return CASES
