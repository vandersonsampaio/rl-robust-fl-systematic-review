"""Etapa 1 (título/resumo) da base Scopus.

Entrada:  scopus_limpo.csv (gerado por higienizar_scopus.py; 2978 registros únicos)
          scopus_dedup.csv (422 duplicatas da sobreposição das colagens)
          triagem/scopus_decisoes_manuais.tsv (lidos título + resumo)
          triagem/acm_triagem.csv, triagem/ieee_triagem.csv (decisões herdadas)
Saída:    triagem/scopus_triagem.csv, triagem/scopus_prisma.md

Ordem de decisão por registro:
  1. ano < 2017                      -> E-PER (fora do período do protocolo, §5)
  2. mesmo título já triado em ACM/IEEE -> decisão herdada (metodo = herdado:<id>)
  3. decisão manual (FL + adversário, com ou sem RL; e casos conferidos)
  4. regra por termos, idêntica à do IEEE (ver triagem_ieee.rule)
"""
import csv, sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from triagem_ieee import norm_title, rule  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "triagem"


def main():
    rows_in = list(csv.DictReader(open(ROOT / "scopus_limpo.csv", encoding="utf-8-sig")))
    n_dup_colagem = sum(1 for _ in csv.DictReader(open(ROOT / "scopus_dedup.csv", encoding="utf-8-sig")))
    prev = {}
    for f in ("acm_triagem.csv", "ieee_triagem.csv"):
        for r in csv.DictReader(open(OUT / f, encoding="utf-8-sig")):
            prev.setdefault(norm_title(r["titulo"]), r)
    manual = {}
    for line in open(OUT / "scopus_decisoes_manuais.tsv", encoding="utf-8"):
        if line.strip():
            i, dec, mot, conf = line.rstrip("\n").split("\t")
            manual[i] = (dec, mot, conf)

    rows = []
    for x in rows_in:
        nt = norm_title(x["titulo"])
        other = prev.get(nt)
        if x["fora_periodo"] == "S":
            dec, mot, conf, metodo = "E-PER", "Publicado antes de 2017 (fora do período, §5)", "alta", "regra"
        elif other:
            dec, mot, conf = other["etapa1_decisao_r1"], other["etapa1_motivo_r1"], other["confianca_r1"]
            metodo = f"herdado:{other['id']}"
        elif x["id"] in manual:
            (dec, mot, conf), metodo = manual[x["id"]], "leitura_manual"
        else:
            (dec, mot), conf, metodo = rule(x["titulo"] + " " + x["resumo"], x["titulo"]), "alta", "regra"
        baixar = "S" if dec in ("I", "D") else ("§9.2" if dec == "E-EC2" else "N")
        rows.append({
            "id": x["id"], "fonte": "Scopus", "titulo": x["titulo"], "ano": x["ano"], "doi_arxiv": "",
            "etapa1_decisao_r1": dec, "etapa1_motivo_r1": mot,
            "etapa1_decisao_r2": "", "etapa1_consenso": "",
            "etapa2_decisao": "", "etapa2_motivo": "", "conferido_r2": "",
            "via_snowballing": "N", "origem_snowballing": "",
            "confianca_r1": conf, "metodo": metodo, "tem_resumo": "S" if x["resumo"] else "N",
            "baixar_pdf": baixar, "dup_outra_base": other["id"] if other else "",
            "venue": x["fonte"], "tipo": x["tipo"], "autores": x["autores"], "resumo": x["resumo"],
        })

    with open(OUT / "scopus_triagem.csv", "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader(); w.writerows(rows)

    c = Counter(r["etapa1_decisao_r1"] for r in rows)
    kind = lambda r: r["metodo"].split(":")[0]
    cm = Counter((r["etapa1_decisao_r1"], kind(r)) for r in rows)
    excl = sorted((k, v) for k, v in c.items() if k.startswith("E-"))
    novos = [r for r in rows if r["etapa1_decisao_r1"] in ("I", "D") and not r["dup_outra_base"]]
    lines = [
        "# PRISMA 2020 — Scopus (etapa 1)", "",
        "| etapa | n |", "|---|---|",
        f"| identificados (texto colado, 2 lotes) | {len(rows_in) + n_dup_colagem} |",
        f"| duplicatas removidas (sobreposição dos lotes) | {n_dup_colagem} |",
        f"| **triados na etapa 1** | **{len(rows)}** |",
        *[f"| &nbsp;&nbsp;{m} | {sum(kind(r) == m for r in rows)} |" for m in ("leitura_manual", "herdado", "regra")],
        f"| excluídos na etapa 1 | {sum(v for _, v in excl)} |",
        *[f"| &nbsp;&nbsp;{k} (manual {cm[(k, 'leitura_manual')]} · herdado {cm[(k, 'herdado')]} · "
          f"regra {cm[(k, 'regra')]}) | {v} |" for k, v in excl],
        f"| seguem para texto completo (I) | {c['I']} |",
        f"| seguem para texto completo (D) | {c['D']} |",
        f"| **seguem para a etapa 2 (I + D)** | **{c['I'] + c['D']}** |",
        f"| &nbsp;&nbsp;dos quais novos (não estão na ACM/IEEE) | {len(novos)} |", "",
        f"Registros também presentes na ACM ou no IEEE (mesmo título): {sum(bool(r['dup_outra_base']) for r in rows)}.",
        "E-PER: fora do período do protocolo (ano < 2017).",
    ]
    (OUT / "scopus_prisma.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
