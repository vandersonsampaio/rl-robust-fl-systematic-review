"""Etapa 1 (título/resumo) da base IEEE Xplore: parse, deduplicação e triagem.

Entrada:  export2026.09.27-20.48.04.csv (export IEEE)
          triagem/ieee_decisoes_manuais.tsv (decisões lidas título+resumo, revisor 1 assistido)
          triagem/acm_triagem.csv (para marcar sobreposição com a ACM)
Saída:    triagem/ieee_triagem.csv, triagem/ieee_dedup.csv, triagem/ieee_prisma.md

Registros sem decisão manual recebem decisão por regra, conforme os termos presentes em
título + resumo + palavras-chave do autor (coluna `metodo` = regra):
  - sem 'federated'/FL          -> E-IC1
  - FL sem termo de RL/bandit   -> E-IC3 (ou E-EC5 se survey/revisão)
  - FL + RL sem termo adversário/cliente malicioso -> E-EC4 (RL federado), E-EC3
    (eficiência/recursos) ou E-IC2 (demais), ou E-EC5 se survey/revisão
Os regex de apoio estão abaixo; todo registro com FL + RL + termo adversário, e todo
FL + termo adversário, foi lido manualmente.
"""
import csv, re, unicodedata
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "export2026.09.27-20.48.04.csv"
OUT = ROOT / "triagem"

FL = re.compile(r"federated|\bFL\b", re.I)
RL = re.compile(r"reinforcement|q-learning|q learning|deep q|\bdqn|ddqn|policy gradient|actor.critic|ddpg|td3|"
                r"\bppo\b|proximal policy|soft actor|\bsac\b|bandit|linucb|thompson|upper confidence|\bucb|"
                r"markov decision|\bmdp\b|\bdrl\b|\bmarl\b|\bfrl\b", re.I)
SURVEY = re.compile(r"survey|review|overview|tutorial|systematic|state-of-the-art and|editorial|retract", re.I)
FRL = re.compile(r"federated (deep |multi-?agent |hierarchical |inverse |offline |secure |security )?"
                 r"(reinforcement|q-learning|ddqn|dqn|ddpg|actor|temporal difference|imitation)|\bfrl\b|"
                 r"federated .{0,30}reinforcement", re.I)
EFF = re.compile(r"resource|energy|latenc|communication|client selection|offload|allocation|schedul|caching|"
                 r"bandwidth|power", re.I)


def norm_title(t):
    t = re.sub(r"[^\w]+", " ", t)
    t = unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode().lower()
    return re.sub(r"\s+", " ", t).strip()


def rule(text, title):
    if not FL.search(text):
        return "E-IC1", "FL não aparece em título/resumo/palavras-chave"
    if SURVEY.search(title):
        return "E-EC5", "Survey/revisão/editorial"
    if not RL.search(text):
        return "E-IC3", "Sem componente de RL/bandit em título/resumo"
    if FRL.search(text):
        return "E-EC4", "RL federado (FL treina agentes de RL); sem defesa de agregação contra clientes adversários"
    if EFF.search(text):
        return "E-EC3", "RL em FL para eficiência/recursos; sem clientes adversários"
    return "E-IC2", "RL e FL presentes, mas sem defesa contra clientes adversários"


def main():
    rows_in = list(csv.DictReader(open(SRC, encoding="utf-8-sig")))
    manual = {}
    for line in open(OUT / "ieee_decisoes_manuais.tsv", encoding="utf-8"):
        if line.strip():
            i, dec, mot, conf = line.rstrip("\n").split("\t")
            manual[int(i)] = (dec, mot, conf)

    acm = {}
    for r in csv.DictReader(open(OUT / "acm_triagem.csv", encoding="utf-8-sig")):
        if r["doi_arxiv"]:
            acm[r["doi_arxiv"].lower()] = r["id"]
        acm[norm_title(r["titulo"])] = r["id"]

    seen_doi, seen_t, dups, rows = {}, {}, [], []
    for n, x in enumerate(rows_in, 1):
        doi, nt = x["DOI"].strip().lower(), norm_title(x["Document Title"])
        hit = seen_doi.get(doi) if doi else None
        how = "doi"
        if hit is None:
            hit, how = seen_t.get(nt), "titulo"
        if hit is not None:
            dups.append({"linha_export": n, "titulo": x["Document Title"], "doi": doi,
                         "duplicata_de": hit, "criterio": how})
            continue
        rid = f"IEEE-{n:03d}"  # id = linha do export, para rastreabilidade
        if doi:
            seen_doi[doi] = rid
        seen_t[nt] = rid

        text = " ".join([x["Document Title"], x["Abstract"], x["Author Keywords"]])
        if n in manual:
            dec, mot, conf = manual[n]
            metodo = "leitura_manual"
        else:
            (dec, mot), conf, metodo = rule(text, x["Document Title"]), "alta", "regra"
        baixar = "S" if dec in ("I", "D") else ("§9.2" if dec == "E-EC2" else "N")
        rows.append({
            "id": rid, "fonte": "IEEE Xplore", "titulo": x["Document Title"],
            "ano": x["Publication Year"], "doi_arxiv": x["DOI"],
            "etapa1_decisao_r1": dec, "etapa1_motivo_r1": mot,
            "etapa1_decisao_r2": "", "etapa1_consenso": "",
            "etapa2_decisao": "", "etapa2_motivo": "", "conferido_r2": "",
            "via_snowballing": "N", "origem_snowballing": "",
            "confianca_r1": conf, "metodo": metodo,
            "tem_resumo": "S" if x["Abstract"].strip() else "N",
            "baixar_pdf": baixar,
            "dup_outra_base": acm.get(doi) or acm.get(nt, ""),
            "venue": x["Publication Title"], "autores": x["Authors"],
            "url": x["PDF Link"] or (f"https://doi.org/{x['DOI']}" if x["DOI"] else ""),
            "keywords": x["Author Keywords"], "resumo": x["Abstract"],
        })

    with open(OUT / "ieee_triagem.csv", "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader(); w.writerows(rows)
    with open(OUT / "ieee_dedup.csv", "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=["linha_export", "titulo", "doi", "duplicata_de", "criterio"])
        w.writeheader(); w.writerows(dups)

    c = Counter(r["etapa1_decisao_r1"] for r in rows)
    cm = Counter((r["etapa1_decisao_r1"], r["metodo"]) for r in rows)
    excl = sorted((k, v) for k, v in c.items() if k.startswith("E-"))
    over = [r for r in rows if r["dup_outra_base"]]
    lines = [
        "# PRISMA 2020 — IEEE Xplore (etapa 1)", "",
        "| etapa | n |", "|---|---|",
        f"| **identificados** | **{len(rows_in)}** |",
        f"| duplicatas removidas (dentro do IEEE) | {len(dups)} |",
        f"| **triados na etapa 1** | **{len(rows)}** |",
        f"| &nbsp;&nbsp;lidos manualmente (título + resumo) | {sum(r['metodo'] == 'leitura_manual' for r in rows)} |",
        f"| &nbsp;&nbsp;decididos por regra de termos | {sum(r['metodo'] == 'regra' for r in rows)} |",
        f"| excluídos na etapa 1 | {sum(v for _, v in excl)} |",
        *[f"| &nbsp;&nbsp;{k} (manual {cm[(k, 'leitura_manual')]} · regra {cm[(k, 'regra')]}) | {v} |"
          for k, v in excl],
        f"| seguem para texto completo (I) | {c['I']} |",
        f"| seguem para texto completo (D) | {c['D']} |",
        f"| **seguem para a etapa 2 (I + D)** | **{c['I'] + c['D']}** |", "",
        f"E-EC2 ({c['E-EC2']}) vão para a ficha reduzida de defesas adaptativas não-RL (§9.2).", "",
        f"Sobreposição com a ACM (mesmo DOI ou título): {len(over)} registros — "
        + ", ".join(f"{r['id']}={r['dup_outra_base']}" for r in over) + ".",
        "Essas sobreposições entram como duplicatas no fluxo consolidado entre bases.",
    ]
    (OUT / "ieee_prisma.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
