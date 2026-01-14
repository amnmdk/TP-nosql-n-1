from config import collection

for arbre in collection.find().limit(20):
    print(
        f"- {arbre['nom']} ({arbre['latin']}) | "
    )
