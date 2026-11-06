"""Validação da S2 (§6.3): testa os 3 blocos da S2 em título + resumo."""
import re
B1_ATUAL = r'reinforcement learning|bandit'
B1_REV = (r'reinforcement|bandit|multiarmed|\bRL\b|\bDRL\b|\bMARL\b|q[- ]learning|\bdqn\b|\bddpg\b|\btd3\b|\bppo\b|'
          r'actor[- –]critic|policy (?:gradient|learning|optimization)|upper confidence bound|\bucb\b|thompson sampling')
B2_ATUAL = r'ablation|random policy|fixed policy|heuristic baseline|simple baseline|reproducib|sanity check'
B2_REV = (B2_ATUAL + r'|random (?:selection|baseline|agent|action)|fixed (?:action|rule|weight)|static (?:policy|baseline)|'
          r'heuristic (?:policy|selection|client[- ]selection)|non-learn|without (?:the )?(?:RL|agent|learning)|'
          r'baseline(?:s)? (?:match|outperform)|replicat|re-?implement')
B3 = r'federated learning|robust aggregation|byzantine'


def s2(text, b1=B1_ATUAL, b2=B2_ATUAL):
    m = [sorted({x.lower() for x in re.findall(p, text, re.I)}) for p in (b1, b2, B3)]
    return m, all(m)
