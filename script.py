import json

f1 = open("data-raw/les-arbres.json", "r", encoding="utf-8")
paris = json.load(f1)
f1.close()

f2 = open("data-raw/arbres-remarquables-du-territoire-des-hauts-de-seine-hors-proprietes-privees.json", "r", encoding="utf-8")
hauts = json.load(f2)
f2.close()

cles = set()

for a in paris:
    cles.update(a.keys())

for a in hauts:
    cles.update(a.keys())

resultat = []

for a in paris:
    if str(a.get("remarquable", "")).upper() == "OUI":
        arbre = {}
        for cle in cles:
            arbre[cle] = a.get(cle)
        arbre["source"] = "paris"
        resultat.append(arbre)

for a in hauts:
    arbre = {}
    for cle in cles:
        arbre[cle] = a.get(cle)
    arbre["source"] = "hauts-de-seine"
    resultat.append(arbre)

out = open("data/arbres.json", "w", encoding="utf-8")
json.dump(resultat, out, ensure_ascii=False)
out.close()
