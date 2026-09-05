#!/usr/bin/env python3
"""Link registered harnesses to one skill registry, preserving replaced entries in trash.

check: read-only, exits 1 on missing/drifting/duplicate registry entries.
sync: repair with a durable move/restore manifest outside skill discovery.
add NAME SKILLS_DIR: register a new verified skill-discovery path; no sync yet.
Never publishes skills, pushes git, follows skill-internal paths, or deletes files.
"""
import argparse
import datetime
import json
import os
from pathlib import Path
import re
import sys
import uuid

DEFAULT_CONFIG = Path.home()/'.config/cortana/skill-harnesses.json'
SKIP={'.git','.system','.hub','.archive','.curator_backups','.trash','references','assets','templates','scripts','__pycache__','node_modules','venv','.venv','_org'}

def safe_path(value):
    p=Path(value).expanduser().absolute()
    if 'documents' in (x.lower() for x in p.parts) or 'documents' in (x.lower() for x in p.resolve().parts):
        raise ValueError('Documents paths are prohibited')
    return p

def defaults():
    return {'version':1,'registry':str(Path(__file__).resolve().parent.parent),'harnesses':[
        {'name':'claude','skills_dir':'~/.claude/skills'},
        {'name':'codex','skills_dir':'~/.codex/skills'},
        {'name':'hermes','skills_dir':'~/.hermes/skills'}]}

def validate_config(data):
    names=[x['name'] for x in data['harnesses']]
    if len(set(names))!=len(names):raise ValueError('duplicate harness names')
    targets=[str(safe_path(x['skills_dir']).resolve()) for x in data['harnesses']]
    source=(safe_path(data['registry'])/'skills').resolve()
    for i,target in enumerate(targets):
        for other in targets[i+1:]:
            if Path(target)==source and Path(other)==source:continue
            if Path(target).is_relative_to(other) or Path(other).is_relative_to(target):
                raise ValueError('harness target directories overlap')
    return data

def read_config(path):
    return validate_config(json.loads(path.read_text()) if path.exists() else defaults())

def skill_entries(root):
    """Inspect physical skill roots; symlink targets are not traversed recursively."""
    entries=[]
    if not root.exists():return entries
    for cur,dirs,files in os.walk(root,followlinks=False):
        dirs[:]=[d for d in dirs if d not in SKIP and not d.startswith('.')]
        p=Path(cur)
        if 'SKILL.md' in files:
            entries.append(p);dirs[:]=[];continue
        for d in list(dirs):
            q=p/d
            if q.is_symlink():
                safe_path(q)
                if (q/'SKILL.md').is_file():entries.append(q)
                dirs.remove(d)
    return entries

def build_plan(data,registry_override=None):
    registry=safe_path(registry_override or data['registry']);source=registry/'skills'
    if not source.is_dir():raise ValueError(f'registry skills unavailable: {source}')
    skills={p.name:p for p in source.iterdir() if not p.name.startswith('.') and p.is_dir() and (p/'SKILL.md').is_file()}
    if not skills:raise ValueError('registry contains no skills; refusing empty-source synchronization')
    actions=[];reports=[]
    for spec in data['harnesses']:
        root=safe_path(spec['skills_dir'])
        if root.resolve()==source.resolve():
            reports.append({'name':spec['name'],'path':str(root),'registry_skills':len(skills),'direct_root':True,'changes':0});continue
        if root.resolve().is_relative_to(registry.resolve()) or registry.resolve().is_relative_to(root.resolve()):
            raise ValueError('harness path overlaps the registry')
        if root.resolve()==Path.home().resolve() or str(root)=='/':raise ValueError('unsafe harness root')
        found=skill_entries(root);by_id={}
        for p in found:by_id.setdefault(p.name,[]).append(p)
        start=len(actions);queued=set()
        def preserve(p,reason):
            if str(p) in queued:return
            # Refuse flattening native packages that carry separately discoverable subskills.
            if p.is_dir() and not p.is_symlink():
                nested=[q for q in p.rglob('SKILL.md') if q.parent!=p]
                if nested and ((p/'SKILL.md').exists() or any(q.parent.name not in skills for q in nested)):
                    raise ValueError(f'nested local-only skill package requires manual reconciliation: {p}')
            actions.append({'op':'trash','path':str(p),'root':str(root),'harness':spec['name'],'reason':reason});queued.add(str(p))
        for skill,p in sorted(skills.items()):
            target=root/skill
            # Preserve a native category whose name matches a registry skill.
            if target.is_dir() and not target.is_symlink() and not (target/'SKILL.md').is_file():
                target=root/'_cortana-registry'/skill
            for old in by_id.get(skill,[]):
                if old!=target:preserve(old,'duplicate/nested registry-owned ID')
            same=target.is_symlink() and target.resolve()==p.resolve()
            if not same:
                if target.exists() or target.is_symlink():preserve(target,'replace with canonical skill link')
                actions.append({'op':'link','path':str(target),'source':str(p),'harness':spec['name']})
        # Only retire stale symlinks owned by this exact registry, never local-only packages.
        for managed_parent in (root,root/'_cortana-registry'):
            if not managed_parent.exists():continue
            for p in managed_parent.iterdir():
                if not p.is_symlink() or p.name in skills:continue
                dest=p.resolve()
                if dest.parent==source.resolve():preserve(p,'stale registry skill link')
        reports.append({'name':spec['name'],'path':str(root),'registry_skills':len(skills),'direct_root':False,'changes':len(actions)-start,
                        'local_only_skills_preserved':len([p for p in found if p.name not in skills])})
    # A category can share a registry ID (Hermes github/). Preserve the whole
    # category once when all its skill children are registry-owned.
    moves=[a for a in actions if a['op']=='trash']
    moves=[a for a in moves if not any(Path(a['path']).is_relative_to(Path(b['path'])) and a['path']!=b['path'] for b in moves)]
    actions=moves+[a for a in actions if a['op']=='link']
    for report in reports:
        report['changes']=sum(a['harness']==report['name'] for a in actions)
    return {'registry':str(registry),'registry_skill_count':len(skills),'harnesses':reports,'actions':actions}

def save_json(path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    tmp=path.with_name(path.name+'.tmp-'+uuid.uuid4().hex[:8]);tmp.write_text(json.dumps(value,indent=2)+'\n');os.replace(tmp,path)

def apply_plan(plan,manifest_path):
    receipt={'created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'registry':plan['registry'],'actions':[],'state':'running'}
    save_json(manifest_path,receipt)
    stamp=datetime.datetime.now().strftime('%Y%m%d-%H%M%S')+'-'+uuid.uuid4().hex[:8]
    for action in plan['actions']:
        entry=dict(action);path=safe_path(action['path'])
        if action['op']=='trash':
            root=safe_path(action['root'])
            trash=root.parent/'.trash'/'cortana-skill-sync'/stamp/path.relative_to(root)
            trash.parent.mkdir(parents=True,exist_ok=True)
            entry['restore_from']=str(trash);entry['state']='pending';receipt['actions'].append(entry);save_json(manifest_path,receipt)
            if trash.exists() or trash.is_symlink():raise ValueError(f'trash collision: {trash}')
            path.rename(trash)
        else:
            path.parent.mkdir(parents=True,exist_ok=True)
            entry['state']='pending';receipt['actions'].append(entry);save_json(manifest_path,receipt)
            # No replacement: a concurrent write must fail rather than be overwritten.
            path.symlink_to(safe_path(action['source']),target_is_directory=True)
        entry['state']='done';save_json(manifest_path,receipt)
    receipt['state']='complete';save_json(manifest_path,receipt)
    return receipt

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--config',type=Path,default=DEFAULT_CONFIG)
    ap.add_argument('--registry',help='Explicit registry clone override')
    sub=ap.add_subparsers(dest='command',required=True)
    sub.add_parser('check');sub.add_parser('plan');sub.add_parser('sync')
    add=sub.add_parser('add');add.add_argument('name');add.add_argument('skills_dir')
    args=ap.parse_args();config=safe_path(args.config);data=read_config(config)
    if args.registry:data['registry']=str(safe_path(args.registry))
    # Explicit legacy path overrides remain usable for one invocation.
    for h in data['harnesses']:
        env_key=h['name'].upper().replace('-','_')+'_SKILLS'
        if env_key in os.environ:h['skills_dir']=os.environ[env_key]
    data['harnesses']=[h for h in data['harnesses'] if h['skills_dir']]
    validate_config(data)
    if args.command=='add':
        if not re.fullmatch(r'[a-z0-9][a-z0-9-]*',args.name):raise ValueError('name must be kebab-case')
        if any(h['name']==args.name for h in data['harnesses']):raise ValueError('harness name already registered')
        path=safe_path(args.skills_dir)
        if any(safe_path(h['skills_dir']).resolve()==path.resolve() for h in data['harnesses']):raise ValueError('path already registered')
        data['harnesses'].append({'name':args.name,'skills_dir':str(path)})
        validate_config(data)
        build_plan(data,args.registry)  # validate all paths before saving
        save_json(config,data);print(json.dumps({'registered':args.name,'path':str(path),'next':'review plan, then sync'}));return 0
    plan=build_plan(data,args.registry)
    if args.command=='sync':
        if not config.exists():save_json(config,data)
        if plan['actions']:
            receipt=config.parent/'receipts'/('skill-sync-'+datetime.datetime.now().strftime('%Y%m%d-%H%M%S')+'-'+uuid.uuid4().hex[:8]+'.json')
            apply_plan(plan,receipt);after=build_plan(data,args.registry)
            print(json.dumps({'receipt':str(receipt),'before':plan['harnesses'],'after':after['harnesses'],'remaining_changes':len(after['actions'])},indent=2));return int(bool(after['actions']))
        print(json.dumps({'already_synchronized':True,'harnesses':plan['harnesses']},indent=2));return 0
    print(json.dumps(plan if args.command=='plan' else {k:v for k,v in plan.items() if k!='actions'},indent=2))
    return int(bool(plan['actions'])) if args.command=='check' else 0

if __name__=='__main__':
    try:sys.exit(main())
    except (OSError,ValueError,KeyError,json.JSONDecodeError) as exc:
        print(f'skill sync failed: {exc}',file=sys.stderr);sys.exit(2)
