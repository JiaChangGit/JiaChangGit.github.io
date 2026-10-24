#!/usr/bin/env python3
"""Run only existing read-only project checks; never generate, commit or publish."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import subprocess
import sys

CHECKS = {
 'pcie_build':['scripts/build_pcie_course.py','--check'],
 'pcie_evidence':['scripts/validate_pcie_course.py'],
 'pcie_guides':['scripts/validate_pcie_teaching.py'],
 'pcie_examples':['scripts/validate_pcie_examples.py'],
 'nvme_questions':['scripts/build_nvme_question_bank.py','--check'],
 'nvme_question_sources':['scripts/nvme_qa_sources.py','--check'],
 'nvme_figures':['scripts/build_nvme_quickref.py','--check'],
 'nvme_reports':['scripts/validate_nvme_report.py','--phase','publish'],
 'publication_boundaries':['scripts/validate_public_teaching.py'],
}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo',type=Path,default=Path(__file__).resolve().parents[1])
    parser.add_argument('--python',default=sys.executable)
    parser.add_argument('--only',nargs='+',choices=list(CHECKS),default=list(CHECKS))
    parser.add_argument('--list',action='store_true')
    parser.add_argument('--output',type=Path)
    args = parser.parse_args()
    repo = args.repo.resolve()
    if args.output and args.output.resolve().is_relative_to(repo):
        parser.error('Write reports outside the repository')
    commands = [(name,[args.python,'-B',*CHECKS[name]]) for name in args.only]
    if args.list:
        print(json.dumps(dict(commands),indent=2,ensure_ascii=False))
        return 0
    results = []
    for name,command in commands:
        if not (repo / CHECKS[name][0]).is_file():
            result = {'name':name,'returncode':127,'output':'Missing project check'}
        else:
            try:
                run = subprocess.run(command,cwd=repo,text=True,encoding='utf-8',errors='replace',stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=300,check=False)
                result = {'name':name,'returncode':run.returncode,'output':run.stdout}
            except subprocess.TimeoutExpired:
                result = {'name':name,'returncode':124,'output':'Check exceeded 300 seconds; no mutating fallback executed'}
        results.append(result)
        print(f'{name}: '+('PASS' if result['returncode']==0 else 'FAIL'),flush=True)
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return int(any(result['returncode'] for result in results))

if __name__ == '__main__':
    raise SystemExit(main())
