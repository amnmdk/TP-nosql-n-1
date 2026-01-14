from config import collection

print("=== 10 premiers arbres du Bois de Vincennes ===\n")

for arbre in collection.find(
    {"commune": "Bois de Vincennes"}
).limit(10):
    print(
        f"{arbre['nom']} ({arbre['latin']}) | "
        f"{arbre['hauteur']} m | "
        f"{arbre['commune']}"
    )

print("\n=== Arbres de plus de 20 mètres ===\n")

for arbre in collection.find(
    {"hauteur": {"$gt": 20}}
):
    print(
        f"{arbre['nom']} ({arbre['latin']}) | "
        f"{arbre['hauteur']} m | "
        f"{arbre['commune']}"
    )
