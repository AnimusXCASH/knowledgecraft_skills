from __future__ import annotations
import argparse, hashlib, json, shutil, subprocess, sys
from pathlib import Path
from datetime import datetime, timezone
VALID={"new","extracted","grounded","ideas_created","series_planned","drafted","qa_approved","scheduled","published","failed","ignored"}
def now(): return datetime.now(timezone.utc).isoformat()
def sha256(path):
 h=hashlib.sha256()
 with Path(path).open('rb') as f:
  for chunk in iter(lambda:f.read(1024*1024),b''): h.update(chunk)
 return h.hexdigest()
def load(path):
 path=Path(path); return json.loads(path.read_text(encoding='utf-8')) if path.exists() else {"version":1,"updated_at":now(),"sources":{}}
def save(path,data):
 path=Path(path); path.parent.mkdir(parents=True,exist_ok=True); data['updated_at']=now(); tmp=path.with_suffix(path.suffix+'.tmp'); tmp.write_text(json.dumps(data,indent=2,ensure_ascii=False),encoding='utf-8'); tmp.replace(path)
def sid(d): return 'SRC-'+d[:12]
def pdf(path):
 try:
  import fitz; doc=fitz.open(path); return '\n\n'.join(p.get_text('text') for p in doc)
 except Exception: pass
 try:
  from pypdf import PdfReader; r=PdfReader(str(path)); return '\n\n'.join((p.extract_text() or '') for p in r.pages)
 except Exception: pass
 exe=shutil.which('pdftotext')
 if exe:
  p=subprocess.run([exe,'-layout',str(path),'-'],capture_output=True)
  if p.returncode==0: return p.stdout.decode('utf-8',errors='replace')
 raise RuntimeError('No PDF extractor available. Install pymupdf or pypdf, or pdftotext.')
def docx(path):
 try: from docx import Document
 except Exception as e: raise RuntimeError('DOCX extraction requires python-docx.') from e
 return '\n\n'.join(p.text for p in Document(str(path)).paragraphs if p.text.strip())
def extract_text(path):
 path=Path(path); e=path.suffix.lower()
 if e=='.pdf': return pdf(path)
 if e=='.docx': return docx(path)
 if e in {'.md','.txt','.html','.htm'}: return path.read_text(encoding='utf-8',errors='replace')
 raise RuntimeError('Unsupported file type: '+e)
def prior_same_path(reg,path,digest):
 c=[(r.get('discovered_at',''),k) for k,r in reg['sources'].items() if r.get('primary_path')==str(Path(path).resolve()) and r.get('sha256')!=digest]
 return sorted(c,reverse=True)[0][1] if c else None
def scan(a):
 rp=Path(a.registry).resolve(); reg=load(rp); byhash={r['sha256']:k for k,r in reg['sources'].items()}; exts={x.lower() for x in a.extensions.split(',')}; added=seen=0
 for rs in a.roots:
  root=Path(rs).expanduser().resolve()
  if not root.exists(): print('WARNING missing root:',root,file=sys.stderr); continue
  for p in root.rglob('*'):
   if not p.is_file() or p.suffix.lower() not in exts: continue
   seen+=1; d=sha256(p)
   if d in byhash:
    r=reg['sources'][byhash[d]]; paths=set(r.get('paths',[r.get('primary_path')])); paths.add(str(p.resolve())); r['paths']=sorted(x for x in paths if x); r['last_seen_at']=now(); continue
   k=sid(d); st=p.stat(); rev=prior_same_path(reg,p,d)
   reg['sources'][k]={"source_id":k,"sha256":d,"filename":p.name,"primary_path":str(p.resolve()),"paths":[str(p.resolve())],"extension":p.suffix.lower(),"size_bytes":st.st_size,"discovered_at":now(),"last_seen_at":now(),"status":"new","revision_of":rev,"extracted_path":None,"artifacts":{},"history":[{"at":now(),"event":"discovered"}],"error":None}; byhash[d]=k; added+=1
 save(rp,reg); print(f'Files seen: {seen}; new content: {added}')
def ext(a):
 rp=Path(a.registry).resolve(); reg=load(rp); out=Path(a.out).resolve(); targets=[k for k,r in reg['sources'].items() if r.get('status') in {'new','failed'}] if a.pending else [a.source_id]
 for k in targets:
  if k not in reg['sources']: print('Unknown source:',k,file=sys.stderr); continue
  r=reg['sources'][k]
  try:
   text=extract_text(r['primary_path'])
   if not text.strip(): raise RuntimeError('Extraction returned empty text.')
   out.mkdir(parents=True,exist_ok=True); fp=out/f'{k}.md'; fp.write_text(f"# Extracted source: {r['filename']}\n\n- source_id: `{k}`\n- sha256: `{r['sha256']}`\n- original_path: `{r['primary_path']}`\n\n---\n\n"+text,encoding='utf-8'); r['status']='extracted'; r['extracted_path']=str(fp); r['error']=None; r['history'].append({'at':now(),'event':'status','value':'extracted'}); print('Extracted',k)
  except Exception as e: r['status']='failed'; r['error']=str(e); r['history'].append({'at':now(),'event':'failed','value':str(e)}); print('FAILED',k,e,file=sys.stderr)
 save(rp,reg)
def status(a):
 reg=load(Path(a.registry).resolve()); counts={}
 for r in reg['sources'].values(): counts[r.get('status','unknown')]=counts.get(r.get('status','unknown'),0)+1
 print('Total:',len(reg['sources']))
 for s in sorted(counts): print(f'{s:16} {counts[s]}')
 for k,r in sorted(reg['sources'].items()): print(f"{k}  {r.get('status','?'):16}  {r.get('filename','')}")
def mark(a):
 if a.status not in VALID: raise SystemExit('Invalid status: '+a.status)
 rp=Path(a.registry).resolve(); reg=load(rp)
 if a.source_id not in reg['sources']: raise SystemExit('Unknown source: '+a.source_id)
 r=reg['sources'][a.source_id]
 if a.artifact:
  p=Path(a.artifact).resolve()
  if not p.exists(): raise SystemExit('Artifact does not exist: '+str(p))
  r.setdefault('artifacts',{})[a.status]=str(p)
 r['status']=a.status; r['history'].append({'at':now(),'event':'status','value':a.status}); save(rp,reg); print(a.source_id,'->',a.status)
def main():
 p=argparse.ArgumentParser(); p.add_argument('--registry',default='.knowledgecraft/research/registry.json'); s=p.add_subparsers(dest='cmd',required=True)
 x=s.add_parser('scan'); x.add_argument('roots',nargs='+'); x.add_argument('--extensions',default='.pdf,.docx,.md,.txt,.html,.htm'); x.set_defaults(fn=scan)
 x=s.add_parser('extract'); x.add_argument('source_id',nargs='?'); x.add_argument('--pending',action='store_true'); x.add_argument('--out',default='.knowledgecraft/research/extracted'); x.set_defaults(fn=ext)
 x=s.add_parser('status'); x.set_defaults(fn=status)
 x=s.add_parser('mark'); x.add_argument('source_id'); x.add_argument('status'); x.add_argument('--artifact'); x.set_defaults(fn=mark)
 a=p.parse_args(); a.fn(a)
if __name__=='__main__': main()
