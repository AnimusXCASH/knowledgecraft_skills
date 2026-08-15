from pathlib import Path
import re,sys
R=Path(__file__).parent/'.opencode'/'skills'; rx=re.compile(r'^[a-z0-9]+(-[a-z0-9]+)*$'); e=[]
for d in sorted(p for p in R.iterdir() if p.is_dir()):
 i=d.name
 if not rx.fullmatch(i) or len(i)>64:e.append(f'{i}: invalid portable ID')
 p=d/'SKILL.md'
 if not p.exists():e.append(f'{i}: missing SKILL.md');continue
 t=p.read_text(encoding='utf-8')
 if not t.startswith('---\n'):e.append(f'{i}: missing frontmatter');continue
 q=t.split('---',2)
 if len(q)<3:e.append(f'{i}: malformed frontmatter');continue
 fm=q[1]; n=re.search(r'(?m)^name:\s*([^\n]+)$',fm); desc=re.search(r'(?m)^description:\s*(.+)$',fm)
 if not n or n.group(1).strip().strip('"').strip("'")!=i:e.append(f'{i}: name must equal directory ID')
 if not desc or not desc.group(1).strip():e.append(f'{i}: missing description')
 if desc and len(desc.group(1).strip())>1024:e.append(f'{i}: description too long')
if e:
 print('FAILED');[print(' -',x) for x in e];sys.exit(1)
print(f'PASSED: {len([p for p in R.iterdir() if p.is_dir()])} skills')
