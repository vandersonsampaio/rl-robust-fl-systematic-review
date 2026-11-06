"""Higieniza Scopus.txt (texto copiado da lista de resultados do Scopus) em CSV.

Estrutura de cada registro no texto colado:
    \t<Tipo>[  •  Open access]\t
    <n>\t<Título>\t<Autor1>\n,\n<Autor2>...\t<Fonte>\n, <vol(nº), págs>\t<Ano>\t<Citações>
    \tHide abstract
    <resumo ...>
    Opens in a new tab. / View at Publisher / Related documents
O arquivo contém duas colagens (1–2000 e 1–1400); `lote` distingue as duas.

Saída: scopus_limpo.csv (UTF-8 com BOM) e scopus_higienizacao.md (relatório).
"""
import csv, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC, OUT, REP = ROOT / "Scopus.txt", ROOT / "scopus_limpo.csv", ROOT / "scopus_higienizacao.md"

NUM = re.compile(r"^(\d+)\t")
END_ABS = ("Opens in a new tab.", "View at Publisher", "Related documents", "View PDF",
           "Full text options", "Show abstract", "Hide abstract")


def clean(s):
    return re.sub(r"\s+", " ", s).strip()


def parse(src=None):
    lines = Path(src or SRC).read_text(encoding="utf-8").splitlines()
    starts = [i for i, l in enumerate(lines) if NUM.match(l)]
    recs, problems, lote, prev_n = [], [], 1, 0
    for k, i in enumerate(starts):
        n = int(NUM.match(lines[i]).group(1))
        if n <= prev_n:
            lote += 1
        prev_n = n
        # tipo de documento: última linha não vazia antes do número
        j = i - 1
        while j >= 0 and not lines[j].strip():
            j -= 1
        tipo_raw = clean(lines[j]) if j >= 0 else ""
        tipo, _, acesso = tipo_raw.partition("•")
        # cabeçalho: do número até '\tHide abstract'
        stop = starts[k + 1] if k + 1 < len(starts) else len(lines)
        h = i
        while h < stop and lines[h].strip() != "Hide abstract":
            h += 1
        header = "\n".join(lines[i:h])
        parts = header.split("\t")
        rec = {"lote": lote, "n_lote": n, "tipo": clean(tipo), "open_access": "S" if "Open access" in acesso else "N"}
        if len(parts) >= 6:
            autores = [clean(a) for a in re.split(r"\n,\s*\n?|,\.\.\.\s*\n?", parts[2]) if clean(a).strip(",. ")]
            fonte_bruta = "\t".join(parts[3:-2])
            fonte, _, detalhes = fonte_bruta.partition("\n")
            rec.update(titulo=clean(parts[1]), autores="; ".join(a.strip(", ") for a in autores),
                       autores_truncados="S" if ",..." in parts[2] else "N",
                       fonte=clean(fonte), volume_paginas=clean(detalhes).lstrip(", "),
                       ano=clean(parts[-2]), citacoes=clean(parts[-1]))
        else:
            problems.append((lote, n, "cabeçalho com %d campos" % len(parts), clean(header)[:120]))
            rec.update(titulo=clean(parts[1]) if len(parts) > 1 else clean(header), autores="",
                       autores_truncados="", fonte="", volume_paginas="", ano="", citacoes="")
        # resumo
        a = h + 1
        buf = []
        while a < stop and lines[a].strip() not in END_ABS and not lines[a].startswith("\t"):
            buf.append(lines[a])
            a += 1
        rec["resumo"] = clean(" ".join(buf))
        if h >= stop:
            problems.append((lote, n, "sem 'Hide abstract'", rec["titulo"][:120]))
        elif not rec["resumo"]:
            problems.append((lote, n, "resumo vazio", rec["titulo"][:120]))
        if not re.fullmatch(r"(19|20)\d\d", rec["ano"] or ""):
            problems.append((lote, n, f"ano inválido: {rec['ano']!r}", rec["titulo"][:120]))
        recs.append(rec)
    return recs, problems


def norm_title(t):
    return re.sub(r"[^a-z0-9]+", " ", t.lower()).strip()


def main():
    recs, problems = parse()
    # Os lotes são a mesma busca ordenada do mais novo (lote 1) e do mais antigo (lote 2);
    # sobrepõem-se em 2024. Mesmo título + mesmo resumo = registro colado duas vezes (removido).
    # Mesmo título com resumo diferente = homônimo (mantido, apenas sinalizado).
    seen_tr, seen_t, kept, dups = {}, {}, [], []
    for idx, r in enumerate(recs, 1):
        r["id"] = f"SCO-{idx:04d}"
        nt, key = norm_title(r["titulo"]), (norm_title(r["titulo"]), r["resumo"])
        if key in seen_tr:
            dups.append({"id": r["id"], "lote": r["lote"], "n_lote": r["n_lote"], "titulo": r["titulo"],
                         "duplicata_de": seen_tr[key], "criterio": "titulo+resumo identicos (sobreposicao dos lotes)"})
            continue
        seen_tr[key] = r["id"]
        r["homonimo_de"] = seen_t.get(nt, "")
        seen_t.setdefault(nt, r["id"])
        r["fora_periodo"] = "S" if r["ano"].isdigit() and int(r["ano"]) < 2017 else "N"
        kept.append(r)
    cols = ["id", "lote", "n_lote", "titulo", "autores", "autores_truncados", "ano", "fora_periodo", "fonte",
            "volume_paginas", "tipo", "open_access", "citacoes", "homonimo_de", "resumo"]
    with open(OUT, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader(); w.writerows(kept)
    with open(ROOT / "scopus_dedup.csv", "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=list(dups[0]) if dups else ["id"])
        w.writeheader(); w.writerows(dups)
    all_recs, recs = recs, kept

    from collections import Counter
    lotes = Counter(r["lote"] for r in all_recs)
    lens = sorted(len(r["resumo"]) for r in recs)
    rep = [
        "# Higienização do Scopus.txt", "",
        f"- Registros extraídos do texto colado: **{len(all_recs)}** ("
        + ", ".join(f"lote {k}: {v}" for k, v in sorted(lotes.items())) + ")",
        "- Lote 1 = resultados do mais novo ao mais antigo; lote 2 = do mais antigo ao mais novo; "
        "sobrepõem-se no ano de 2024.",
        f"- Duplicatas da sobreposição removidas (título + resumo idênticos): **{len(dups)}** (ver scopus_dedup.csv)",
        f"- **Registros únicos em scopus_limpo.csv: {len(recs)}**",
        f"- Homônimos mantidos (mesmo título, resumo diferente): {sum(bool(r['homonimo_de']) for r in recs)}",
        f"- Fora do período do protocolo (ano < 2017): {sum(r['fora_periodo'] == 'S' for r in recs)}",
        f"- Com resumo: {sum(bool(r['resumo']) for r in recs)}",
        f"- Tamanho do resumo (caracteres): mín {lens[0]}, mediana {lens[len(lens)//2]}, máx {lens[-1]}",
        f"- Registros com lista de autores truncada pelo Scopus (',...'): {sum(r['autores_truncados'] == 'S' for r in recs)}",
        f"- Tipos de documento: " + ", ".join(f"{k} {v}" for k, v in Counter(r['tipo'] for r in recs).most_common()),
        f"- Anos: " + ", ".join(f"{k}: {v}" for k, v in sorted(Counter(r['ano'] for r in recs).items())),
        "", "**Limitação:** o texto colado não traz DOI, palavras-chave nem afiliações; a deduplicação entre bases "
        "será feita por título normalizado.", "",
        f"## Problemas de parse ({len(problems)})", "",
        *[f"- lote {l}, nº {n}: {p} — {t}" for l, n, p, t in problems],
    ]
    REP.write_text("\n".join(rep) + "\n", encoding="utf-8")
    print("\n".join(rep[:12]), f"\nproblemas: {len(problems)}")
    for p in problems[:15]:
        print(p)


if __name__ == "__main__":
    main()
