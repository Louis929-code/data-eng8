from pathlib import Path
import json
import csv
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")
print("Clé récupérée :", API_KEY)

# 1. pathlib : trouver le fichier
dossier_data = Path("data")
fichier_entree = dossier_data / "logs-bruts.json"
print("Je lis :", fichier_entree)

# 2. try/except : lire le .json brut sans planter
try:
    with open(fichier_entree, "r", encoding="utf-8") as f:
        donnees = json.load(f)
    print("J'ai lu", len(donnees), "lignes brutes")
except FileNotFoundError:
    print("Erreur : fichier introuvable :", fichier_entree)
    donnees = []

# 3. Compréhension de liste : filtrer seulement les ERROR
erreurs = [ligne for ligne in donnees if ligne["status"] == "ERROR"]
print("J'ai gardé", len(erreurs), "erreurs")

# 4. Écrire le résultat nettoyé en .csv
dossier_sortie = Path("output")
dossier_sortie.mkdir(exist_ok=True)
fichier_sortie = dossier_sortie / "logs_nettoyes.csv"

with open(fichier_sortie, "w", newline="", encoding="utf-8") as f:
    ecrivain = csv.DictWriter(f, fieldnames=["id", "message", "status"])
    ecrivain.writeheader()
    ecrivain.writerows(erreurs)

print("Résultat écrit dans :", fichier_sortie)
