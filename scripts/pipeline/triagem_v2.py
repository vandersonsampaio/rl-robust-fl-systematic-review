"""Etapa 1 da busca definitiva (S1 revisada, S2a, S2b): decisões + PRISMA + listas de download.

Entrada:  triagem_v2/registros.csv (consolidar_v2.py), triagem_v2/dedup_log.csv
          triagem_v2/decisoes_s1_manuais.tsv, triagem_v2/decisoes_q7_manuais.tsv
          triagem/{acm,ieee,scopus}_triagem.csv (decisões da rodada anterior, herdadas por título)
Saída:    triagem_v2/triagem_final.csv, triagem_v2/prisma_v2.md, triagem_v2/download_<fonte>.csv,
          triagem_v2/download_lista.md

Decisão S1 (critérios §7), aplicada aos registros recuperados pela S1 ou lidos manualmente:
  ano < 2017 -> E-PER; título já triado na rodada anterior -> herdado; lido -> manual; demais -> regra.
Decisão QP7 (S2a/S2b; critério declarado em validacao/validacao_6.4.md e no relatório):
  Q7-I/Q7-D/Q7-E por leitura; registros S2 sem termos de auditoria/avaliação -> Q7-E por regra.
"""
import csv, sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from triagem_ieee import norm_title, rule  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
V2 = ROOT / "triagem_v2"
PREF = ("IEEE", "ACM", "Scopus", "arXiv")


def load_tsv(p):
    out = {}
    for line in open(p, encoding="utf-8"):
        if line.strip():
            i, d, m, c = line.rstrip("\n").split("\t")
            out[i] = (d, m, c)
    return out


def main():
    R = list(csv.DictReader(open(V2 / "registros.csv", encoding="utf-8-sig")))
    log = list(csv.DictReader(open(V2 / "dedup_log.csv", encoding="utf-8-sig")))
    s1m, q7m = load_tsv(V2 / "decisoes_s1_manuais.tsv"), load_tsv(V2 / "decisoes_q7_manuais.tsv")
    prev = {}
    for f in ("acm_triagem.csv", "ieee_triagem.csv", "scopus_triagem.csv"):
        for r in csv.DictReader(open(ROOT / "triagem" / f, encoding="utf-8-sig")):
            prev.setdefault(norm_title(r["titulo"]), r)

    # DOIs resolvidos pelo Crossref (resolver_doi.py) para registros só do Scopus colado
    resolved = {}
    if (V2 / "doi_resolvidos.csv").exists():
        resolved = {r["id"]: r["doi"] for r in csv.DictReader(open(V2 / "doi_resolvidos.csv", encoding="utf-8-sig"))
                    if r["doi"]}
    for x in R:
        x["doi_origem"] = "export" if x["doi"] else ""
        if not x["doi"] and x["id"] in resolved:
            x["doi"], x["doi_origem"] = resolved[x["id"]], "crossref (título exato)"

    rows = []
    for x in R:
        strings = x["strings"].split(";")
        text = " ".join([x["titulo"], x["resumo"], x["keywords"]])
        # --- S1
        s1 = s1mot = s1conf = s1met = ""
        old = prev.get(norm_title(x["titulo"]))
        if x["id"] in s1m:
            (s1, s1mot, s1conf), s1met = s1m[x["id"]], "leitura_manual"
        elif "s1" in strings:
            if x["ano"].isdigit() and int(x["ano"]) < 2017:
                s1, s1mot, s1conf, s1met = "E-PER", "Publicado antes de 2017 (fora do período, §5)", "alta", "regra"
            elif old:
                s1, s1mot, s1conf = old["etapa1_decisao_r1"], old["etapa1_motivo_r1"], old["confianca_r1"]
                s1met = f"herdado:{old['id']}"
            else:
                (s1, s1mot), s1conf, s1met = rule(text, x["titulo"]), "alta", "regra"
        # --- QP7
        q7 = q7mot = q7met = ""
        if x["id"] in q7m:
            q7, q7mot, _ = q7m[x["id"]]
            q7met = "leitura_manual"
        elif "s1" not in strings:
            q7, q7mot, q7met = "Q7-E", "Sem termos de auditoria/avaliação no título/resumo", "regra"
        ler = "S" if s1 in ("I", "D") or q7 in ("Q7-I", "Q7-D") else ("§9.2" if s1 == "E-EC2" else "N")
        fonte_dl = next(b for b in PREF if b in x["bases"].split(";"))
        rows.append({**{k: x[k] for k in ("id", "titulo", "ano", "venue", "autores", "doi", "doi_origem", "arxiv", "url",
                                            "bases", "strings")},
                     "s1_decisao": s1, "s1_motivo": s1mot, "s1_confianca": s1conf, "s1_metodo": s1met,
                     "q7_decisao": q7, "q7_motivo": q7mot, "q7_metodo": q7met,
                     "ler_texto_completo": ler, "fonte_download": fonte_dl,
                     "id_rodada_anterior": old["id"] if old else "",
                     "resumo": x["resumo"]})
    with open(V2 / "triagem_final.csv", "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)

    # ---------- PRISMA
    brutos = Counter((l["base"], l["string"]) for l in log)
    uni_base = defaultdict(set)
    for l in log:
        uni_base[l["base"]].add(l["id"])
    s1rows = [r for r in rows if r["s1_decisao"]]
    q7rows = [r for r in rows if r["q7_decisao"]]
    c1, c7 = Counter(r["s1_decisao"] for r in s1rows), Counter(r["q7_decisao"] for r in q7rows)
    met1 = Counter((r["s1_decisao"], r["s1_metodo"].split(":")[0]) for r in s1rows)
    L = ["# PRISMA 2020 — busca definitiva (S1 revisada, S2a, S2b) — etapa 1", "",
         "## Identificação", "", "| base | S1 | S2a | S2b | total bruto | únicos na base |", "|---|---|---|---|---|---|"]
    for b in PREF:
        L.append(f"| {b} | {brutos[(b,'s1')]} | {brutos[(b,'s2a')]} | {brutos[(b,'s2b')]} | "
                 f"{sum(brutos[(b,s)] for s in ('s1','s2a','s2b'))} | {len(uni_base[b])} |")
    L += ["", f"- Registros brutos: **{len(log)}**",
          f"- Duplicatas removidas (dentro e entre bases, entre strings; DOI ou título normalizado): **{len(log) - len(R)}**",
          f"- Registros únicos triados: **{len(R)}** — recuperados pela S1: "
          f"{sum('s1' in r['strings'].split(';') for r in rows)}; só pela S2a/S2b: "
          f"{sum('s1' not in r['strings'].split(';') for r in rows)} "
          f"(destes, {len(s1rows) - sum('s1' in r['strings'].split(';') for r in rows)} com FL+RL+adversário "
          "também foram triados pelos critérios da S1)",
          f"- Triados pelos critérios da S1: **{len(s1rows)}**; avaliados exclusivamente para a QP7: **{len(R) - len(s1rows)}**", "",
          "## Triagem S1 (critérios §7)", "", "| decisão | manual | herdado | regra | total |", "|---|---|---|---|---|"]
    for k in sorted(c1, key=lambda k: (k[0] != "I", k[0] != "D", k)):
        L.append(f"| {k} | {met1[(k,'leitura_manual')]} | {met1[(k,'herdado')]} | {met1[(k,'regra')]} | {c1[k]} |")
    L += ["", f"**S1 → texto completo: {c1['I'] + c1['D']}** (I {c1['I']} + D {c1['D']}); "
          f"E-EC2 → ficha §9.2: {c1['E-EC2']}", "",
          "## Triagem QP7 (S2a ∪ S2b)", "", "| decisão | n |", "|---|---|",
          *[f"| {k} | {v} |" for k, v in sorted(c7.items())], "",
          f"**QP7 → texto completo: {c7['Q7-I'] + c7['Q7-D']}**", "",
          f"## Total para leitura integral: **{sum(r['ler_texto_completo'] == 'S' for r in rows)}** trabalhos únicos", ""]
    (V2 / "prisma_v2.md").write_text("\n".join(L), encoding="utf-8")
    print("\n".join(L))

    # ---------- listas de download por fonte
    sel = [r for r in rows if r["ler_texto_completo"] == "S"]
    md = ["# Lista de download — textos completos (etapa 2)", "",
          "Cada trabalho aparece uma vez, na fonte preferida (IEEE → ACM → Scopus → arXiv). "
          "Coluna 'motivo' indica S1 (defesa com RL) ou QP7 (auditoria/avaliação).", ""]
    for b in PREF:
        part = sorted([r for r in sel if r["fonte_download"] == b], key=lambda r: r["titulo"].lower())
        with open(V2 / f"download_{b.lower()}.csv", "w", newline="", encoding="utf-8-sig") as f:
            w = csv.DictWriter(f, fieldnames=["id", "titulo", "ano", "venue", "doi", "arxiv", "link", "s1_decisao",
                                              "q7_decisao", "bases", "id_rodada_anterior"])
            w.writeheader()
            for r in part:
                link = (f"https://doi.org/{r['doi']}" if r["doi"] else
                        f"https://arxiv.org/abs/{r['arxiv']}" if r["arxiv"] else r["url"])
                w.writerow({k: r[k] for k in ("id", "titulo", "ano", "venue", "doi", "arxiv", "s1_decisao",
                                              "q7_decisao", "bases", "id_rodada_anterior")} | {"link": link})
        md += [f"## {b} ({len(part)})", "", "| id | título | ano | motivo | link |", "|---|---|---|---|---|"]
        for r in part:
            mot = "/".join(filter(None, [r["s1_decisao"] if r["s1_decisao"] in ("I", "D") else "",
                                         r["q7_decisao"] if r["q7_decisao"] in ("Q7-I", "Q7-D") else ""]))
            link = (f"https://doi.org/{r['doi']}" if r["doi"] else
                    f"https://arxiv.org/abs/{r['arxiv']}" if r["arxiv"] else "(buscar pelo título)")
            md.append(f"| {r['id']} | {r['titulo'].replace('|', '/')} | {r['ano']} | {mot} | {link} |")
        md.append("")
    (V2 / "download_lista.md").write_text("\n".join(md), encoding="utf-8")
    print("download por fonte:", Counter(r["fonte_download"] for r in sel),
          "| sem DOI/arXiv:", sum(1 for r in sel if not r["doi"] and not r["arxiv"]))


if __name__ == "__main__":
    main()
