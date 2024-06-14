import requests
import matplotlib.pyplot as plt

url = "https://data.metropole-rouen-normandie.fr/api/explore/v2.1/catalog/datasets/liste-des-arrets-du-reseau-astuce-metropole-rouen-normandie/records?limit=20"
response = requests.get(url)

if response.status_code == 200:
    try:
        data = response.json()
    except requests.exceptions.JSONDecodeError as e:
        print("Erreur de décodage JSON : ", e)
        print("Contenu brut de la réponse : ", response.text)
else:
    print(f"Erreur {response.status_code}: {response.reason}")

if 'data' in locals():
    if 'results' in data:
        stops = data["results"]

        coordinates = [(stop["geo_point_2d"]["lon"], stop["geo_point_2d"]["lat"]) for stop in stops]
        stop_names = [stop["nom_arret"] for stop in stops]

        longitudes, latitudes = zip(*coordinates)

        plt.figure(figsize=(20, 12))
        plt.scatter(longitudes, latitudes, c='blue', marker='o')

        for i, name in enumerate(stop_names):
            plt.text(longitudes[i], latitudes[i], name, fontsize=9, ha='right')

        plt.title("Arrêts de bus du réseau Astuce - Métropole Rouen Normandie")
        plt.xlabel("Longitude")
        plt.ylabel("Latitude")

        plt.show()
    else:
        print("La clé 'records' n'est pas présente dans la réponse.")
