from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
from scipy.sparse import hstack
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler

# Initialisation de l'application Flask.
app = Flask(__name__)

# Chargement du dataset de films depuis un fichier CSV dans un DataFrame pandas.
# Ce dataset est présumé avoir des colonnes pour les titres des films, les genres, les notes et le nombre de votes.
data = pd.read_csv('C:\\Users\\FiercePC\\Desktop\\IA\\Projet_IMDb\\approche_8\\filtered_imdb_data.csv')

# Définition d'une fonction pour calculer un score pondéré pour chaque film.
# Ce score prend en compte à la fois la note moyenne du film et le nombre de votes qu'il a reçus.
def weighted_rating(x, m, C):
    V = x['numVotes']
    R = x['averageRating']
    return (V/(V+m) * R) + (m/(m+V) * C)

# Calcul de la note moyenne sur l'ensemble des films et du seuil de votes à partir duquel un film est considéré comme significatif.
C = data['averageRating'].mean()
m = data['numVotes'].quantile(0.90)

# Application de la fonction de score pondéré à chaque film dans le DataFrame.
data['score'] = data.apply(weighted_rating, axis=1, m=m, C=C)

# Prétraitement des données pour la modélisation.
# Transformation OneHotEncoding des genres pour les convertir en un format numérique utilisable par le modèle.
genre_enc = OneHotEncoder()
genres_transformed = genre_enc.fit_transform(data[['genres']])

# Normalisation du score pondéré à une échelle de 0 à 1.
score_scaled = MinMaxScaler().fit_transform(data[['score']])

# Combinaison des features de genres encodés et du score pondéré en une seule matrice de features.
X = hstack([genres_transformed, score_scaled])

# Création et entraînement du modèle NearestNeighbors en utilisant la similarité cosinus comme métrique.
model = NearestNeighbors(n_neighbors=10, algorithm='brute', metric='cosine')
model.fit(X)

# Route pour l'index
@app.route('/')
def index():
    # Initialiser 'recommandations' à un DataFrame vide ou à une liste vide si vous n'avez pas de recommandations à afficher.
    recommandations = pd.DataFrame()  # ou recommandations = []
    # Assurez-vous de passer 'recommandations' dans le contexte de votre template.
    return render_template('index.html', recommandations=recommandations)

# Route pour l'auto-complétion
@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    search = request.args.get('term')  # jQuery UI envoie le terme de recherche en tant que paramètre 'term'
    matching_results = data[data['primaryTitle'].str.contains(search, case=False, na=False)]['primaryTitle'].unique()
    return jsonify(list(matching_results))  # Retourner les résultats en tant que liste pour l'auto-complétion

@app.route('/recommander', methods=['POST'])
def recommander():
    # Route pour traiter le formulaire de recherche de film.
    # Récupère le titre du film depuis le formulaire, le normalise, et appelle la fonction de recherche de films similaires.
    titre_film = request.form.get('titre_film').strip().lower()
    recherche_effectuee = True
    recommandations = rechercher_films_similaires(titre_film)
    return render_template('index.html', recommandations=recommandations, titre_film=titre_film, recherche_effectuee=recherche_effectuee)

def rechercher_films_similaires(titre):
    # Fonction pour trouver des films similaires à celui donné par le titre.
    films_trouves = data[data['primaryTitle'].str.lower() == titre.lower()]
    
    if films_trouves.empty:
        return pd.DataFrame()
    
    # Sélection du film le plus populaire en cas de multiples films avec le même titre.
    film_choisi = films_trouves.loc[films_trouves['numVotes'].idxmax()]
    film_index = film_choisi.name

    # Recherche des films voisins les plus proches en utilisant le modèle de recommandation.
    test_film = X.getrow(film_index).toarray()
    distances, indices = model.kneighbors(test_film)

    # Exclusion du film de base des résultats et récupération des 9 meilleures recommandations.
    indices = indices[0][indices[0] != film_index][:9]
    recommandations = data.iloc[indices].sort_values(by='score', ascending=False)
    
    # Ajout des scores cosinus aux recommandations
    recommandations['score_cosinus'] = 1 - distances[0][:len(recommandations)]

    return recommandations

# Point d'entrée principal pour exécuter l'application Flask.
if __name__ == '__main__':
    app.run(debug=True)
