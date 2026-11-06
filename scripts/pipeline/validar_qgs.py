"""Validação da string S1 (§6.4): testa os blocos A, B e C da S1 no título + resumo do arXiv."""
import re, sys, xml.etree.ElementTree as ET
NS = {'a': 'http://www.w3.org/2005/Atom'}
A = r'federated learning|federated optimization|federated averaging'
B = (r'reinforcement learning|q-learning|deep q|\bdqn\b|policy gradient|actor-critic|\bddpg\b|\btd3\b|\bppo\b|'
     r'soft actor-critic|multi-armed bandit|contextual bandit|linucb|markov decision process')
C = r'byzantine|poisoning|backdoor|malicious|adversar|robust aggregation|attack'


def entries(path):
    for e in ET.parse(path).getroot().findall('a:entry', NS):
        yield (e.find('a:id', NS).text.split('/')[-1],
               ' '.join(e.find('a:title', NS).text.split()),
               ' '.join(e.find('a:summary', NS).text.split()),
               [c.get('term') for c in e.findall('a:category', NS)])


def blocks(text):
    return {k: sorted({m.lower() for m in re.findall(p, text, re.I)}) for k, p in (('A', A), ('B', B), ('C', C))}


if __name__ == '__main__':
    for i, t, s, cats in entries(sys.argv[1]):
        m = blocks(t + ' ' + s)
        print(f"{i} | {t[:95]}\n   A={m['A']} B={m['B']} C={m['C']} => {'CASA' if all(m.values()) else 'NAO CASA'}\n   cats={cats}")
