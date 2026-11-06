"""Resolve DOIs, via API pública do Crossref, dos selecionados para leitura que não têm DOI nem arXiv
(registros vindos só do Scopus colado da tela). Aceita apenas correspondência exata de título normalizado.
Saída: triagem_v2/doi_resolvidos.csv (lido por triagem_v2.py).
"""
import csv, json, sys, time, urllib.parse, urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from triagem_ieee import norm_title  # noqa: E402

V2 = Path(__file__).resolve().parent.parent / "triagem_v2"


def main():
    rows = [r for r in csv.DictReader(open(V2 / "triagem_final.csv", encoding="utf-8-sig"))
            if r["ler_texto_completo"] == "S" and not r["doi"] and not r["arxiv"]]
    out = []
    for r in rows:
        url = "https://api.crossref.org/works?" + urllib.parse.urlencode(
            {"query.bibliographic": r["titulo"], "rows": 3, "select": "DOI,title"})
        req = urllib.request.Request(url, headers={"User-Agent": "SLR-triagem/1.0 (script de revisão sistemática)"})
        doi = ""
        try:
            items = json.load(urllib.request.urlopen(req, timeout=60))["message"]["items"]
            for it in items:
                if it.get("title") and norm_title(it["title"][0]) == norm_title(r["titulo"]):
                    doi = it["DOI"]; break
        except Exception as e:  # noqa: BLE001
            print("erro", r["id"], e)
        out.append({"id": r["id"], "titulo": r["titulo"], "doi": doi})
        print(r["id"], doi or "—", r["titulo"][:70])
        time.sleep(1)
    with open(V2 / "doi_resolvidos.csv", "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=["id", "titulo", "doi"]); w.writeheader(); w.writerows(out)
    print(f"resolvidos: {sum(bool(o['doi']) for o in out)} de {len(out)}")


if __name__ == "__main__":
    main()
