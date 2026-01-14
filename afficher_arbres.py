from config import collection

for arbre in collection.find().limit(20):
    print(
        f"- {arbre['nom']} ({arbre['latin']}) | "
        f"{arbre['commune']} | "
        f"{arbre['hauteur']} m | "
        f"{arbre['circonference']} m | "
        f"lat={arbre['localisation']['lat']}, lon={arbre['localisation']['lon']}"
    )
