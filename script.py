import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent

SRC1 = HERE / "data-raw" / "les-arbres.json"
SRC2 = HERE / "data-raw" / "arbres-remarquables-du-territoire-des-hauts-de-seine-hors-proprietes-privees.json"
OUT = HERE / "data" / "arbres.json"
OUT.parent.mkdir(parents=True, exist_ok=True)

def load(p):
    with p.open("r", encoding="utf-8") as f:
        obj = json.load(f)
    return obj if isinstance(obj, list) else obj.get("results", [])

def get_code_insee_paris(arr):
    if not arr:
        return None
    val = str(arr).upper()
    if "BOIS DE BOULOGNE" in val:
        return "75016"
    if "BOIS DE VINCENNES" in val:
        return "75012"
    m = re.search(r'(\d+)(?:ER|E)?\s*ARRDT', val)
    if m:
        n = int(m.group(1))
        if 1 <= n <= 20:
            return f"750{n:02d}"
    return None

def normalize_commune(val):
    if not val:
        return None
    v = str(val).upper()
    if "BOIS DE BOULOGNE" in v:
        return "Bois de Boulogne"
    if "BOIS DE VINCENNES" in v:
        return "Bois de Vincennes"
    m = re.search(r'(\d+)(?:ER|E)?\s*ARRDT', v)
    if m:
        n = int(m.group(1))
        return "Paris 1er" if n == 1 else f"Paris {n}ème"
    return val.title()

def latin_name(rec):
    if rec.get("nom_latin"):
        return rec["nom_latin"]
    if rec.get("genre") and rec.get("espece"):
        return f"{rec['genre']} {rec['espece']}"
    return rec.get("genre") or rec.get("espece")

def localise(rec):
    gp = rec.get("geo_point_2d") or {}
    return {
        "lat": gp.get("lat"),
        "lon": gp.get("lon")
    }

data = []

# PARIS — arbres remarquables uniquement
for r in load(SRC1):
    if r.get("remarquable") == "OUI":
        data.append({
            "source": "paris",
            "commune": normalize_commune(r.get("arrondissement")),
            "code_insee": get_code_insee_paris(r.get("arrondissement")),
            "nom": r.get("nom_francais") or r.get("libellefrancais") or r.get("genre"),
            "latin": latin_name(r),
            "hauteur": r.get("hauteurenm") or r.get("hauteur"),
            "circonference": r.get("circonferenceencm"),
            "localisation": localise(r)
        })

# HAUTS-DE-SEINE — déjà remarquables
for r in load(SRC2):
    data.append({
        "source": "hauts-de-seine",
        "commune": normalize_commune(r.get("commune")),
        "code_insee": r.get("code_insee"),
        "nom": r.get("nom_francais"),
        "latin": r.get("nom_latin"),
        "hauteur": r.get("hauteur"),
        "circonference": r.get("circonference"),
        "localisation": localise(r)
    })

with OUT.open("w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"OK → {len(data)} arbres")
