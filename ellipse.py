import requests
import json

# Clé API JCDecaux
api_key = "e0a1bf2c844edb9084efc764c089dd748676cc14"

# URL de base de l'API JCDecaux
base_url = "https://api.jcdecaux.com/vls/v3/"

# Liste des villes pour lesquelles on veut récupérer des données
villes = ["paris", "lyon", "marseille"]

# Dictionnaire pour stocker les données sur les vélos par ville
donnees_par_ville = {}

# Pour chaque ville, on appelle l'API JCDecaux pour récupérer les données sur les vélos
for ville in villes:
    url = base_url + "stations?contract=" + ville + "&apiKey=" + api_key
    response = requests.get(url)
    if response.status_code == 200:
        data = json.loads(response.content.decode('utf-8'))
        donnees_par_ville[ville] = data
    else:
        print("Erreur lors de l'appel à l'API pour la ville ", ville)

# Affichage des données pour chaque ville
for ville, donnees in donnees_par_ville.items():
    nb_velos_total = len(donnees)
    nb_velos_electriques = 0
    for station in donnees:
        if station["electric_bike"] == True:
            nb_velos_electriques += station["num_bikes_available"]
    nb_velos_mecaniques = nb_velos_total - nb_velos_electriques
    pct_velos_electriques = nb_velos_electriques / nb_velos_total * 100
    pct_velos_mecaniques = nb_velos_mecaniques / nb_velos_total * 100
    print(ville.capitalize())
    print("-" * 20)
    print("Nombre total de vélos :", nb_velos_total)
    print("Nombre de vélos électriques :", nb_velos_electriques, "(", round(pct_velos_electriques, 1), "%)")
    print("Nombre de vélos mécaniques :", nb_velos_mecaniques, "(", round(pct_velos_mecaniques, 1), "%)")
    print("\n")

# Classement des villes par nombre de vélos disponibles
villes_triees = sorted(donnees_par_ville.keys(), key=lambda x: len(donnees_par_ville[x]), reverse=True)
print("Classement des villes par nombre de vélos disponibles :")
print("-" * 20)
for i, ville in enumerate(villes_triees):
    nb_velos = len(donnees_par_ville[ville])
    print(str(i+1) + ". " + ville.capitalize() + " :", nb_velos, "vélos")
