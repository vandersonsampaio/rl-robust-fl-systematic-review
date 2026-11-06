"""Consolida as buscas definitivas (S1 revisada, S2a, S2b) de ACM, IEEE, Scopus e arXiv.

Entradas (raiz do projeto):
  acm-<s1|s2a|s2b>-<t|a>.bib   (t = campo Title, a = campo Abstract; o ACM só aceitou um campo por vez)
  ieee-<s1|s2a|s2b>.csv
  scopus-<s1|s2a|s2b>.txt      (texto colado da tela; várias consultas com sobreposição)
  validacao/arxiv_revisada_all.csv (S1), arxiv_s2_revisada.csv (S2a), arxiv_s2b.csv (S2b)
Saída: triagem_v2/registros.csv (um registro único por trabalho) e triagem_v2/dedup_log.csv.
"""
import csv, re, sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from triagem_acm import parse_bib          # noqa: E402
from triagem_ieee import norm_title         # noqa: E402
from higienizar_scopus import parse as parse_scopus  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "triagem_v2"
STRINGS = ("s1", "s2a", "s2b")
ARXIV = {"s1": "arxiv_revisada_all.csv", "s2a": "arxiv_s2_revisada.csv", "s2b": "arxiv_s2b.csv"}
BASE_ORDER = {"IEEE": 0, "ACM": 1, "Scopus": 2, "arXiv": 3}  # base preferida como registro principal


def raw_records():
    for s in STRINGS:
        for f in sorted(ROOT.glob(f"acm-{s}-*.bib")):
            for r in parse_bib(f):
                yield dict(base="ACM", string=s, arquivo=f.name, titulo=r.get("title", ""),
                           resumo=r.get("abstract", ""), keywords=r.get("keywords", ""),
                           doi=r.get("doi", ""), ano=r.get("year", ""),
                           venue=r.get("booktitle") or r.get("journal") or r.get("school", ""),
                           autores=r.get("author", ""), tipo=r["_type"],
                           url=r.get("url", "") or (f"https://doi.org/{r['doi']}" if r.get("doi") else ""))
        f = ROOT / f"ieee-{s}.csv"
        if f.exists():
            for r in csv.DictReader(open(f, encoding="utf-8-sig")):
                yield dict(base="IEEE", string=s, arquivo=f.name, titulo=r["Document Title"], resumo=r["Abstract"],
                           keywords=r["Author Keywords"], doi=r["DOI"], ano=r["Publication Year"],
                           venue=r["Publication Title"], autores=r["Authors"], tipo=r["Document Identifier"],
                           url=(f"https://doi.org/{r['DOI']}" if r["DOI"] else r["PDF Link"]))
        f = ROOT / f"scopus-{s}.txt"
        if f.exists():
            recs, problems = parse_scopus(f)
            for p in problems:
                print("scopus parse:", f.name, p)
            for r in recs:
                yield dict(base="Scopus", string=s, arquivo=f.name, titulo=r["titulo"], resumo=r["resumo"],
                           keywords="", doi="", ano=r["ano"], venue=r["fonte"], autores=r["autores"],
                           tipo=r["tipo"], url="")
        f = ROOT / "validacao" / ARXIV[s]
        for r in csv.DictReader(open(f, encoding="utf-8-sig")):
            aid = re.sub(r"v\d+$", "", r["arxiv_id"])
            yield dict(base="arXiv", string=s, arquivo=ARXIV[s], titulo=r["titulo"], resumo=r["resumo"],
                       keywords=r["categorias"], doi=f"arXiv:{aid}", ano=r["publicado"][:4], venue="arXiv",
                       autores="", tipo="preprint", url=f"https://arxiv.org/abs/{aid}")


def main():
    OUT.mkdir(exist_ok=True)
    raw = list(raw_records())
    ident = Counter((r["base"], r["string"]) for r in raw)
    # mesmo DOI ou mesmo título normalizado = mesmo trabalho
    groups, key_of_doi = {}, {}
    for r in raw:
        nt = norm_title(r["titulo"])
        doi = r["doi"].lower().strip()
        key = (key_of_doi.get(doi) if doi else None) or nt
        groups.setdefault(key, []).append(r)
        if doi:
            key_of_doi[doi] = key
    rows, log = [], []
    ordered = sorted(groups.values(),
                     key=lambda g: (min(BASE_ORDER[r["base"]] for r in g), norm_title(g[0]["titulo"])))
    for n, g in enumerate(ordered, 1):
        g.sort(key=lambda r: (BASE_ORDER[r["base"]], -len(r["resumo"])))
        m = g[0]
        rid = f"V2-{n:04d}"
        rows.append(dict(
            id=rid, titulo=m["titulo"], ano=m["ano"], venue=m["venue"], autores=m["autores"], tipo=m["tipo"],
            doi=next((r["doi"] for r in g if r["doi"] and not r["doi"].startswith("arXiv")), ""),
            arxiv=next((r["doi"][6:] for r in g if r["doi"].startswith("arXiv:")), ""),
            url=next((r["url"] for r in g if r["url"]), ""),
            bases=";".join(sorted({r["base"] for r in g}, key=BASE_ORDER.get)),
            strings=";".join(sorted({r["string"] for r in g})),
            n_ocorrencias=len(g),
            keywords=max((r["keywords"] for r in g), key=len),
            resumo=max((r["resumo"] for r in g), key=len)))
        for r in g:
            log.append(dict(id=rid, base=r["base"], string=r["string"], arquivo=r["arquivo"], titulo=r["titulo"]))
    with open(OUT / "registros.csv", "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    with open(OUT / "dedup_log.csv", "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=list(log[0])); w.writeheader(); w.writerows(log)

    per = defaultdict(set)
    for l in log:
        per[(l["base"], l["string"])].add(l["id"])
    print("base    str   brutos  únicos_na_base")
    for k in sorted(ident):
        print(f"{k[0]:7s} {k[1]:4s} {ident[k]:6d} {len(per[k]):6d}")
    print("únicos na união:", len(rows))
    print("por string:", Counter(s for r in rows for s in r["strings"].split(";")))


if __name__ == "__main__":
    main()
