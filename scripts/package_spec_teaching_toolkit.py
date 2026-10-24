#!/usr/bin/env python3
"""Package approved teaching skills and exact project inputs outside the repo.

No source PDFs, extracted full texts, credentials, Git metadata, QA screenshots,
or command logs are included. This creates a portable authoring snapshot, not
a complete Jekyll site or an installer, and never commits or publishes.
"""
from __future__ import annotations
import argparse
import ast
from datetime import date
import hashlib
import json
from pathlib import Path
import shutil
import zipfile

ROOT=Path(__file__).resolve().parents[1]
TOOLS=['build_pcie_course.py','pcie_teaching.py','validate_pcie_course.py','validate_pcie_teaching.py',
       'validate_pcie_examples.py','check_pcie_browser.cjs','build_nvme_question_bank.py','nvme_qa_sources.py',
       'build_nvme_quickref.py','nvme_quickref_sources.py','build_nvme_reports.py','validate_nvme_report.py',
       'check_spec_teaching_browser.cjs','audit_spec_teaching.py','extract_spec_outline.py',
       'run_project_checks.py','validate_public_teaching.py','package_spec_teaching_toolkit.py','verify_teaching_bundle.py']

def dependencies(repo, seeds):
    pending=list(seeds);seen=set()
    while pending:
        relative=pending.pop()
        if relative in seen:continue
        path=repo/relative
        if not path.is_file() or path.is_symlink() or not path.resolve().is_relative_to(repo):
            raise ValueError('Missing or unsafe input: '+relative)
        seen.add(relative)
        if path.suffix!='.py':continue
        for node in ast.walk(ast.parse(path.read_text(encoding='utf-8-sig'))):
            names=[]
            if isinstance(node,ast.ImportFrom):
                module=node.module or ''
                if module in {'','scripts'}:names=[a.name for a in node.names]
                else:names=[module.removeprefix('scripts.')]
            elif isinstance(node,ast.Import):names=[a.name.removeprefix('scripts.') for a in node.names]
            for name in names:
                candidate='scripts/'+name.replace('.','/')+'.py'
                if (repo/candidate).is_file():pending.append(candidate)
    return sorted(seen)

def copy_file(source, target):
    if source.is_symlink() or source.suffix.lower() in {'.pdf','.key','.pem','.log'} or source.name.startswith('.env'):
        raise ValueError('Private/source file is not a bundle input: '+source.name)
    target.parent.mkdir(parents=True,exist_ok=True)
    shutil.copyfile(source,target)

def package(repo, destination, output):
    repo,destination,output=repo.resolve(),destination.resolve(),output.resolve()
    if destination.is_relative_to(repo) or output.is_relative_to(repo) or output.is_relative_to(destination):
        raise ValueError('Bundle and ZIP must be outside the repository; ZIP must also be outside the bundle')
    if destination.exists() or output.exists():raise ValueError('Choose a new destination and ZIP; existing files are never overwritten')
    paths=dependencies(repo,['scripts/'+name for name in TOOLS])
    for folder in ('.ai/pcie-course','.ai/spec-teaching','.ai/nvme-report','.ai/nvme-question-bank','.ai/nvme-quickref'):
        paths.extend(p.relative_to(repo).as_posix() for p in (repo/folder).rglob('*') if p.is_file() and p.suffix in {'.json','.html','.css','.md','.yaml'})
    paths.extend(p.relative_to(repo).as_posix() for p in (repo/'tests').glob('test_*.py'))
    paths.extend(['assets/css/spec-teaching.css','assets/css/nvme-reader.css','assets/css/nvme-quickref.css','assets/css/nvme-question-bank.css',
                  'AGENTS.md','docs/spec-teaching-revision.md','docs/pcie-course-plan.md','requirements-nvme-report.txt'])
    paths=sorted(set(paths))
    for relative in paths:
        source=repo/relative
        if not source.resolve().is_relative_to(repo):raise ValueError('Input leaves repository')
        copy_file(source,destination/'project-snapshot'/relative)
    for source_prefix,name in (('.ai/spec-teaching/skill','spec-teaching'),('.ai/pcie-course/skill','pcie-spec-teaching')):
        for source in (repo/source_prefix).rglob('*'):
            if source.is_file():copy_file(source,destination/'skills'/name/source.relative_to(repo/source_prefix))
    for name in ('audit_spec_teaching.py','extract_spec_outline.py','run_project_checks.py','verify_teaching_bundle.py','package_spec_teaching_toolkit.py'):
        copy_file(repo/'scripts'/name,destination/'scripts'/name)
    usage='''# PCIe／NVMe 規格教學工具包

本版保存已確認的教學規則與本輪實作：PCIe 藍、NVMe 綠；用問題帶讀角色、欄位、條件及 Figure／Table 的查閱路線。必要解說直接顯示，逐步操作只高亮圖文，不設作答或評分門檻。

## 內容與使用

- `skills/spec-teaching/` 是共同規則；`skills/pcie-spec-teaching/` 是 PCIe 相容入口。可閱讀後手動複製到自己的 Codex skills 目錄；本 ZIP 不會執行安裝。
- `scripts/` 提供只讀盤點、目錄擷取、既有檢查整合、封裝及 ZIP 完整性驗證。
- `project-snapshot/` 保存實際產生器與本機 Python 相依、authored HTML、圖解 JSON、claims、來源登記、樣式及測試。它是編輯快照；不包含整個網站與既有生成產物，不能直接當成完整 Jekyll 專案發布。

在原專案使用 Python 3.10 以上；需核對 PDF 時自行取得同版原文與 `pdftotext`。Jekyll 與瀏覽器檢查另需原專案的 Ruby、Node、Playwright／Chromium 環境。

```sh
python3 -B scripts/audit_spec_teaching.py --repo /path/to/site --scope /path/to/site/.ai/spec-teaching/scope.json --output /outside/site/review.json
python3 -B scripts/run_project_checks.py --repo /path/to/site --output /outside/site/checks.json
python3 -B scripts/verify_teaching_bundle.py --zip /path/to/toolkit.zip
```

請在原專案使用快照中的產生器與資料。先改 authored 來源，再產生頁面；兩篇 NVMe 專篇使用 `build_nvme_reports.py --reports pcie-transport-1.4 nvm-command-set-1.3`。其他 NVMe 專篇不在本輪改寫範圍。盤點腳本只列需校閱處，不會證明中文通順、條文已完整涵蓋或真人已學會。

## 版本與完成範圍

PCIe 主課程依 Base 6.0；Firmware 3.3 另保留其 Base 5.0 參考邊界。NVMe 依 Base 2.4、NVM Command Set 1.3、Transport 1.4（均為 2026-07-31 ratified 的登記文件）；Transport 1.4 自身引用 PCIe Base 6.2。來源雜湊可在登記表核對，本包沒有來源 PDF 或擷取全文。

PCIe Chapter 0–37 已有三版主題教學；規格涵蓋表另追蹤 Base Chapters 1–10、Appendices A–L 的 1,324 個目錄定位。主題章完成不等於每條細節均已帶讀，待核對子項保留原狀。指定 NVMe 系列保留 Q1–Q328、45 情境／117 圖及兩篇專篇。

`MANIFEST.json` 列出每個檔案的 SHA-256 與長度，用於傳輸完整性核對；內含 manifest 不是數位簽章。原始 PDF、私人路徑、憑證、擷取文字、測試截圖和私人執行紀錄不納入本包。
'''
    (destination/'USAGE.md').write_text(usage,encoding='utf-8')
    (destination/'SNAPSHOT-FILES.json').write_text(json.dumps({'schema_version':1,'purpose':'Approved implementation snapshot; not a full site or publication authorization','paths':paths},ensure_ascii=False,indent=2)+'\n')
    files=sorted(p for p in destination.rglob('*') if p.is_file())
    manifest={'schema_version':1,'phase':'implemented_teaching_revision','date':str(date.today()),'files':[
        {'path':p.relative_to(destination).as_posix(),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in files]}
    manifest_path=destination/'MANIFEST.json'
    manifest_path.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    output.parent.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(output,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as archive:
        for path in sorted(files+[manifest_path]):archive.write(path,destination.name+'/'+path.relative_to(destination).as_posix())
    return {'files':len(files)+1,'bytes':output.stat().st_size,'sha256':hashlib.sha256(output.read_bytes()).hexdigest()}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo',type=Path,default=ROOT)
    parser.add_argument('--destination',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    print(json.dumps(package(args.repo,args.destination,args.output),ensure_ascii=False))

if __name__=='__main__':main()
