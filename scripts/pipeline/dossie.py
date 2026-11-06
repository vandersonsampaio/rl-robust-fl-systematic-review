"""Imprime um dossiê de leitura de um texto: resumo, trechos-chave por padrão e conclusão.
uso: python dossie.py <id> [--full-pattern REGEX]"""
import csv, re, sys
from pathlib import Path
B = Path(__file__).resolve().parent.parent / 'triagem_v2'
m = {r['id']: r for r in csv.DictReader(open(B / 'mapa_pdfs.csv', encoding='utf-8-sig'))}
PAT = {
 'RL': r'\b(state|action|reward|agent|policy|Q-learning|DQN|DDPG|TD3|PPO|SAC|actor|critic|bandit|UCB|Thompson|MDP|Markov|episode)s?\b',
 'BASE': r'\b(baseline|compar|FedAvg|Krum|median|trimmed|FLTrust|FLAME|random (selection|policy|strategy)|greedy|heuristic|ablation|without (the )?(RL|DRL|agent))',
 'ATK': r'\b(attack|poison|backdoor|byzantine|label[- ]flip|sign[- ]flip|malicious|adaptive attack|on-off|free-rid)',
 'EXP': r'\b(seed|runs|repeated|average (of|over)|standard deviation|std|confidence interval|t-test|wilcoxon|github|code is available|source code|learning rate|rounds|episodes|clients|non-IID|Dirichlet|dataset)',
}
def sents(t):
    t = re.sub(r'-\n(?=[a-z])', '', t); t = re.sub(r'\s+', ' ', t)
    return re.split(r'(?<=[.!?])\s+(?=[A-Z])', t)
def main():
    i = sys.argv[1]; r = m[i]
    t = (B / 'txt' / r['pasta'] / (r['arquivo'] + '.txt')).read_text(encoding='utf-8', errors='ignore')
    ref = max(t.rfind('References'), t.rfind('REFERENCES'), t.rfind('R EFERENCES'))
    body = t[:ref] if ref > len(t) * 0.5 else t
    ss = sents(body)
    print(f'##### {i} [{r["pasta"]}/{r["arquivo"]}] {r["titulo"]}')
    a = re.search(r'(?is)abstract[\s:.—-]*(.{200,1800}?)(?:\n\s*\n|Index Terms|Keywords|1\s*\.?\s*Introduction|I\. I)', t[:12000])
    print('ABS:', re.sub(r'\s+', ' ', a.group(1))[:1600] if a else re.sub(r'\s+', ' ', t[:1500]))
    lim = int(sys.argv[2]) if len(sys.argv) > 2 else 9
    for k, p in PAT.items():
        rx = re.compile(p, re.I); out = []
        for s in ss[15:]:
            n = len(rx.findall(s))
            if n >= (3 if k == 'RL' else 2) and 40 < len(s) < 600: out.append((n, s))
        out = sorted(out, key=lambda x: -x[0])[:lim]
        print(f'-- {k}:'); [print('  *', s[:450]) for _, s in out]
    c = re.search(r'(?is)\n\s*(?:[0-9IVX]+\.?\s*)?(Conclusions?|CONCLUSIONS?|Concluding Remarks)\s*\n(.{100,1500})', body)
    print('CONC:', re.sub(r'\s+', ' ', c.group(2))[:1300] if c else '(não encontrada)')
if __name__ == '__main__': main()
