import csv, re, sys
from pathlib import Path
B = Path(__file__).resolve().parent.parent / 'triagem_v2'
m = {r['id']: r for r in csv.DictReader(open(B / 'mapa_pdfs.csv', encoding='utf-8-sig'))}
for i in sys.argv[1:]:
    r = m[i]; t = (B / 'txt' / r['pasta'] / (r['arquivo'] + '.txt')).read_text(encoding='utf-8', errors='ignore')
    tt = re.sub(r'\s+', ' ', re.sub(r'-\n(?=[a-z])', '', t))
    a = re.search(r'(?i)abstract[\s:.—-]*(.{200,1500}?)(?:Index Terms|Keywords|CCS Concepts|1\s*\.?\s*Introduction|I\. I)', tt[:15000])
    c = re.search(r'(?i)(?:\d+\.?|[IVX]+\.)\s*(?:Conclusions?|Concluding Remarks|Discussion and Conclusion)\s+(.{100,1400})', tt[len(tt)//2:])
    rl = len(re.findall(r'(?i)reinforcement learning|bandit|\bDQN\b|\bPPO\b', tt))
    print(f'##### {i} [{r["pasta"]}] {r["titulo"]} | chars={len(tt)} | RL-menções={rl}')
    print('ABS:', a.group(1)[:1300] if a else tt[:1300])
    print('CONC:', c.group(1)[:1200] if c else '(n/e)')
    print()
