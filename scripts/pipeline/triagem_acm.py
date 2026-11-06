"""Etapa 1 (título/resumo) da base ACM DL: parse, deduplicação e triagem.

Entrada:  acm (1).bib, acm.bib
Saída:    triagem/acm_triagem.csv   (planilha §11.1 + campos de apoio)
          triagem/acm_dedup.csv     (duplicatas removidas)
          triagem/acm_prisma.md     (contagens para o fluxo PRISMA §11.4)

Decisões do revisor 1 (triagem assistida por Claude; revisão humana pendente).
Códigos: I, D, E-ECn (protocolo §7) e E-ICn (não atende ao critério de inclusão n
quando nenhum EC descreve o motivo).
"""
import csv, html, re, unicodedata
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FILES = ["acm (1).bib", "acm.bib"]
OUT = ROOT / "triagem"


def parse_bib(path):
    txt = path.read_text(encoding="utf-8")
    recs = []
    for m in re.finditer(r"@(\w+)\{([^,]*),", txt):
        i, depth = m.end(), 1
        while depth and i < len(txt):
            depth += {"{": 1, "}": -1}.get(txt[i], 0)
            i += 1
        body = txt[m.end():i - 1]
        f = {"_type": m.group(1), "_key": m.group(2), "_file": path.name}
        for fm in re.finditer(r"(\w+)\s*=\s*\{", body):
            j, d = fm.end(), 1
            while d:
                d += {"{": 1, "}": -1}.get(body[j], 0)
                j += 1
            if fm.start() and body[:fm.start()].count("{") != body[:fm.start()].count("}"):
                continue  # campo aninhado dentro de outro valor
            v = body[fm.end():j - 1].replace("&nbsp;", " ")
            f[fm.group(1).lower()] = re.sub(r"\s+", " ", html.unescape(v)).strip()
        recs.append(f)
    return recs


def norm_title(t):
    t = re.sub(r"[^\w]+", " ", t)  # travessões e símbolos viram espaço antes do ASCII
    t = unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", " ", t).strip()


# Decisões por título normalizado (independe da ordem do arquivo).
# (decisão, motivo, confiança)  confiança: alta | media (ex.: sem resumo no export)
DEC = {
 "phantom physics aware adversarial attacks against federated learning coordinated ev charging management system":
  ("E-EC1", "MARL usado pelo atacante (FDI); FL só como gêmeo digital", "alta"),
 "feddrlpd deep reinforcement learning based defense mechanism against poisoning attacks in federated learning":
  ("I", "QGS Q3; DRL (DQN) como defesa contra envenenamento", "alta"),
 "byzantine robust aggregation for federated learning with reinforcement learning":
  ("I", "RL-GM: DDPG ajusta pesos da mediana geométrica contra envenenamento", "alta"),
 "an innovative multi agent approach for robust cyber physical systems using vertical federated learning":
  ("D", "VFL + actor-critic para CPS 'robusto'; sem resumo, não dá para saber se há clientes adversários", "media"),
 "energy efficient serverless federated learning with blockchain enhanced optimized raft consensus":
  ("E-EC3", "DRL para alocação de recursos/energia; sem adversários", "media"),
 "a software defined wrapper discriminant federated learning reinforcement attention adversarial regression approach for privacy and task management in cloud edge computing":
  ("D", "DQL para privacidade e gestão de tarefas; 'adversarial' ambíguo e sem resumo", "media"),
 "a federated learning based selection and incentive system using blockchain technology":
  ("D", "Seleção de clientes com DQN + incentivo; sem resumo, pode visar clientes maliciosos", "media"),
 "federated learning based deep q network intrusion detection system":
  ("E-EC4", "FL para treinar agente DQN de IDS; RL não decide a agregação", "alta"),
 "private and provably efficient federated decision making":
  ("E-EC4", "Tese: bandits/RL federados com corrupção adversarial no treino do bandit", "alta"),
 "decentralized federated learning towards communication efficiency robustness and personalization":
  ("I", "D-CERP: seleção de vizinhos confiáveis por multi-armed bandit contra bizantinos", "alta"),
 "collaborative privacy preserving network intrusion detection a federated multi agent reinforcement learning approach":
  ("E-EC4", "MARL federado para IDS de rede; sem resumo", "media"),
 "a gan dqn enhanced ai driven framework for real time smart intrusion detection system in cooperative iot networks":
  ("E-EC4", "DQN como IDS de ameaças de rede treinado com FL; não defende a agregação", "alta"),
 "a robust federated learning framework for low quality data and its applications":
  ("D", "FL robusto a dados de baixa qualidade com RL; sem resumo, não dá para saber se há adversários", "media"),
 "federated unlearning with reinforcement learning adaptive privacy preservation for clients":
  ("D", "Unlearning federado com RL; foco em privacidade, mas unlearning pode remover clientes envenenadores; sem resumo", "media"),
 "attention based intrusion detection in mqtt iot network a federated learning and deep reinforcement learning approach":
  ("D", "DDQN é o IDS; pesos de agregação por atenção (não-RL) e 'robustez a ataques adversários' — checar se é defesa de agregação (fronteira EC2/EC4)", "media"),
 "learning to attack federated learning a model based reinforcement learning attack framework":
  ("E-EC1", "QGS B2 (controle de fronteira): RL do atacante", "alta"),
 "learning to collaborate an orchestrated decentralized framework for peer to peer llm federation":
  ("E-EC3", "LinUCB para pareamento P2P contra transferência negativa; sem adversários", "alta"),
 "empowering trustworthy client selection in edge federated learning leveraging reinforcement learning":
  ("I", "Q-learning + reputação para seleção de clientes, mitigando clientes maliciosos", "alta"),
 "f2c net a privacy preserving federated transformer rl architecture for real time control in multi domain sd iot systems":
  ("E-EC4", "RL federado para controle em SD-IoT com DP; sem clientes adversários; sem resumo", "media"),
 "ai powered cyber resilience a reinforcement learning approach for automated threat hunting in 5g networks":
  ("E-EC4", "MARL federado para caça a ameaças de rede 5G; não defende a agregação", "alta"),
 "revocable noise federated learning a quantum audited and dynamically coordinated framework for zero loss privacy":
  ("E-IC2", "Privacidade diferencial/ruído; sem defesa contra clientes adversários; sem resumo", "media"),
 "delay aware 6tisch iiot networks for energy efficient data transmission by adopting federated learning and edge computing":
  ("E-EC3", "DRL para migração/latência em IIoT", "alta"),
 "human immune system inspired security for federated learning empowered internet of things":
  ("I", "Agente DRL identifica e descarta clientes maliciosos (label flipping) na agregação", "alta"),
 "fedaa a reinforcement learning perspective on adaptive aggregation for fair and robust federated learning":
  ("I", "QGS Q2; DDPG para pesos de agregação contra clientes maliciosos", "alta"),
 "adversarial attacks on federated learned adaptive bitrate algorithms":
  ("E-EC1", "Ataque de backdoor em modelo DRL treinado com FL; sem defesa", "alta"),
 "blockchain based secure and efficient federated learning with three phase consensus and unknown device selection":
  ("D", "Defesa via Multi-Krum/consenso; bandit combinatório seleciona dispositivos (eficiência?) — checar se a seleção atua contra maliciosos", "media"),
 "a secure and fair client selection based on ddpg for federated learning":
  ("I", "DDPG pondera escores de segurança/justiça na seleção de clientes contra envenenamento", "alta"),
 "preventing harm to the rare in combating the malicious a filtering and voting framework with adaptive aggregation in federated learning":
  ("D", "Defesa contra maliciosos com agregação adaptativa; KW cita RL, mas sem resumo — fronteira IC3/EC2", "media"),
 "improving iot security through federated deep q learning with realistic traffic modelling":
  ("E-EC4", "DQN federado como IDS de IoT; não defende a agregação", "alta"),
 "adaptive robust client selection in federated learning a two stage reinforcement learning approach":
  ("I", "VEPTP-TSR: controlador DQN regula a seleção de clientes contra envenenamento", "alta"),
 "a federated advisory teacher student framework with simultaneous learning agents":
  ("E-EC4", "RL federado (teacher-student); sem defesa de agregação", "media"),
 "the evolution of cooperation in continuous dilemmas via multi agent reinforcement learning":
  ("E-IC1", "MARL em dilemas de cooperação; não é FL", "media"),
 "drl sa deep reinforcement learning based client selection and secure aggregation for federated learning":
  ("E-IC2", "Adversário é man-in-the-middle/privacidade; DRL para seleção/peso por eficiência, sem clientes maliciosos", "alta"),
 "towards quantum resilient food systems federated ai and lightweight lattice hashing for blockchain based traceability":
  ("E-IC2", "Rastreabilidade na cadeia de alimentos; DRL para detecção de anomalias, sem defesa da agregação", "alta"),
 "a survey on zeroth order optimization for machine learning":
  ("E-EC5", "Survey", "alta"),
 "reputation based model aggregation and resource optimization in wireless federated learning systems":
  ("D", "Agregação por reputação contra maliciosos; DRL para escalonamento (atraso) — checar se o DRL usa a reputação", "media"),
 "dap fl federated learning flourishes by adaptive tuning and secure aggregation":
  ("E-IC2", "DDPG ajusta hiperparâmetros locais; segurança via Paillier (privacidade), sem clientes envenenadores", "alta"),
 "cloud edge client collaborative learning in digital twin empowered mobile networks":
  ("E-EC3", "MADRL para escalonamento de recursos; ameaça é vazamento de gradiente", "alta"),
 "collaborative federated learning for 6g with a deep reinforcement learning based controlling mechanism a ddos attack detection scenario":
  ("E-EC3", "DRL para trade-off acurácia/latência; DDoS é a tarefa, não um ataque ao FL", "alta"),
 "exploring novel machine learning approaches for cheat detection in competitive gaming":
  ("E-IC2", "Ensaio exploratório sobre detecção de trapaça; sem defesa de FL nem avaliação", "alta"),
 "universal interactive verification framework for federated learning protocol":
  ("E-IC2", "Framework de verificação/análise de riscos baseado em RL; não é defesa de agregação", "media"),
 "a federated learning framework with self attention and deep reinforcement learning for iot intrusion detection":
  ("E-EC4", "DRL federado como NIDS; não defende a agregação", "alta"),
 "a federated deep reinforcement learning based trust model in underwater acoustic sensor networks":
  ("E-EC4", "DRL federado para modelo de confiança em nós de rede de sensores, não em clientes do FL", "alta"),
 "a survey on architectures and algorithms of wide area distributed intelligent systems challenges methods and prospects":
  ("E-EC5", "Survey", "alta"),
 "cooperative edge caching based on elastic federated and multi agent deep reinforcement learning in next generation networks":
  ("E-EC3", "MADRL para cache de borda", "alta"),
 "reinforcement learning based personalized differentially private federated learning":
  ("E-IC2", "RL escolhe a perturbação de DP contra inferência de pertinência; sem clientes envenenadores", "alta"),
 "fed pemc a privacy enhanced federated deep learning algorithm for consumer electronics in mobile edge computing":
  ("E-EC3", "DRL para compressão de modelo/comunicação; ameaça é inferência", "alta"),
 "provable and efficient algorithms for federated batch and reinforcement learning":
  ("E-IC3", "Tese; agregação robusta sem componente RL (RL/bandits é outro capítulo)", "alta"),
 "systemization of knowledge robust deep learning using hardware software co design in centralized and federated settings":
  ("E-EC5", "SoK/survey", "alta"),
 "risk aware reinforcement learning based federated learning for iov systems":
  ("I", "RL hierárquico seleciona participantes e tamanho de dados para resistir a ataques egoístas (free-riding)", "alta"),
 "risk aware federated reinforcement learning based secure iov communications":
  ("E-EC4", "RL federado para controle de potência contra espionagem; sem clientes adversários", "alta"),
 "federated intrusion detection on non iid data for iiot networks using generative adversarial networks and reinforcement learning":
  ("E-EC3", "RL para seleção de clientes sob não-IID; sem adversários ao FL", "alta"),
 "defending against membership inference attack for counterfactual federated recommendation with differentially private representation learning":
  ("E-IC2", "Defesa contra inferência de pertinência (privacidade); RL offline na recomendação", "alta"),
 "fault tolerant federated reinforcement learning with theoretical guarantee":
  ("E-EC4", "Robustez do treino de RL federado a agentes bizantinos", "alta"),
 "solving a class of non convex minimax optimization in federated learning":
  ("E-IC3", "Otimização minimax federada; sem RL na defesa", "alta"),
 "joint blockchain and federated learning based offloading in harsh edge computing environments":
  ("E-EC3", "DRL para offloading de tarefas", "alta"),
 "advancing security and trust in wsns a federated multi agent deep reinforcement learning approach":
  ("E-EC4", "MARL federado para IDS em WSN; confiança usada para escalonar recursos", "alta"),
 "deep learning in industry 4 0 transforming manufacturing through data driven innovation":
  ("E-IC1", "Visão geral de DL na Indústria 4.0", "alta"),
 "toward smart security enhancement of federated learning networks":
  ("I", "DRL seleciona dispositivos benignos após verificação (VBA) contra envenenamento", "alta"),
 "fed inforce fusion a federated reinforcement based fusion model for security and privacy protection of iomt networks against cyber attacks":
  ("D", "Provável IDS de IoMT com RL federado (EC4), mas sem resumo — confirmar", "media"),
 "a blockchain privacy preserving computation large language model triad for marketizing media data factors":
  ("E-IC2", "Blockchain + LLM para dados de mídia; PPO só no ajuste do LLM", "alta"),
 "resource allocation in next generation mobile networks":
  ("E-IC3", "Tese; confiança contra envenenamento em FL sem componente RL (RL em outro capítulo)", "alta"),
 "sdn enabled efficient resource utilization in a secure trustworthy and privacy preserving iov fog environment":
  ("E-IC3", "Tese; reputação no FL sem RL (RL usado para distribuição de tarefas)", "alta"),
}


def main():
    OUT.mkdir(exist_ok=True)
    recs = []
    for fn in FILES:
        recs += parse_bib(ROOT / fn)
    n_ident = len(recs)

    # Deduplicação: DOI, depois título normalizado.
    seen_doi, seen_t, kept, dups = {}, {}, [], []
    for r in recs:
        doi = r.get("doi", "").lower().strip()
        nt = norm_title(r.get("title", ""))
        hit = seen_doi.get(doi) if doi else None
        how = "doi"
        if hit is None:
            hit, how = seen_t.get(nt), "titulo"
        if hit is not None:
            dups.append({"arquivo": r["_file"], "titulo": r.get("title", ""), "doi": doi,
                         "duplicata_de": hit["id"], "criterio": how})
            continue
        r["id"] = f"ACM-{len(kept) + 1:03d}"
        kept.append(r)
        if doi:
            seen_doi[doi] = r
        seen_t[nt] = r

    rows = []
    for r in kept:
        nt = norm_title(r.get("title", ""))
        dec, mot, conf = DEC[nt]
        doi = r.get("doi", "")
        rows.append({
            "id": r["id"], "fonte": "ACM DL", "titulo": r.get("title", ""),
            "ano": r.get("year", ""), "doi_arxiv": doi,
            "etapa1_decisao_r1": dec, "etapa1_motivo_r1": mot,
            "etapa1_decisao_r2": "", "etapa1_consenso": "",
            "etapa2_decisao": "", "etapa2_motivo": "", "conferido_r2": "",
            "via_snowballing": "N", "origem_snowballing": "",
            # campos de apoio
            "confianca_r1": conf,
            "tem_resumo": "S" if r.get("abstract") else "N",
            "baixar_pdf": "S" if dec in ("I", "D") else "N",
            "tipo": r["_type"], "venue": r.get("booktitle") or r.get("journal") or r.get("school", ""),
            "numpages": r.get("numpages", ""), "autores": r.get("author", ""),
            "url": r.get("url", "") or (f"https://doi.org/{doi}" if doi else ""),
            "keywords": r.get("keywords", ""), "resumo": r.get("abstract", ""),
        })

    with open(OUT / "acm_triagem.csv", "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader(); w.writerows(rows)
    with open(OUT / "acm_dedup.csv", "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=["arquivo", "titulo", "doi", "duplicata_de", "criterio"])
        w.writeheader(); w.writerows(dups)

    per_file = Counter(r["_file"] for r in recs)
    c = Counter(r["etapa1_decisao_r1"] for r in rows)
    excl = sorted((k, v) for k, v in c.items() if k.startswith("E-"))
    lines = [
        "# PRISMA 2020 — ACM Digital Library (etapa 1)", "",
        "| etapa | n |", "|---|---|",
        *[f"| identificados: `{k}` | {v} |" for k, v in per_file.items()],
        f"| **identificados (total ACM)** | **{n_ident}** |",
        f"| duplicatas removidas (dentro da ACM) | {len(dups)} |",
        f"| **triados na etapa 1** | **{len(rows)}** |",
        f"| excluídos na etapa 1 | {sum(v for _, v in excl)} |",
        *[f"| &nbsp;&nbsp;{k} | {v} |" for k, v in excl],
        f"| seguem para texto completo (I) | {c['I']} |",
        f"| seguem para texto completo (D) | {c['D']} |",
        f"| **seguem para a etapa 2 (I + D)** | **{c['I'] + c['D']}** |", "",
        f"Registros sem resumo no export: {sum(r['tem_resumo'] == 'N' for r in rows)} "
        "(decisão por título + palavras-chave; confiança 'media').", "",
        "Pendente: deduplicação entre bases (Scopus, IEEE, arXiv, WoS), que altera "
        "'duplicatas removidas' e 'triados' no fluxo consolidado.",
    ]
    (OUT / "acm_prisma.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
