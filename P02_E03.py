import pandas as pd
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler
from sklearn.compose import ColumnTransformer

# Charger les données
data = pd.read_csv('C:\\Users\\FiercePC\\Desktop\\IA\\Projet_IMDb\\approche_8\\filtered_imdb_data.csv')

# Prétraitement des données (comme dans votre script d'entraînement)
preprocessor = ColumnTransformer(
    transformers=[
        ('genres', OneHotEncoder(), ['genres']),
        ('num', MinMaxScaler(), ['averageRating', 'numVotes'])
    ])
X = preprocessor.fit_transform(data[['genres', 'averageRating', 'numVotes']])

# Construire le modèle kNN (comme dans votre script d'entraînement)
k = 5
model = NearestNeighbors(n_neighbors=k, algorithm='brute')
model.fit(X)

# Sélectionner un film pour tester
test_index = 100  # Choisissez un index de film dans votre jeu de données
test_film = X[test_index]
test_film_reshaped = test_film.reshape(1, -1)

# Trouver les k films les plus proches
distances, indices = model.kneighbors(test_film_reshaped)

# Afficher les films recommandés
print("Film sélectionné pour la recommandation :")
print(data.iloc[test_index])
print("\nFilms recommandés :")
for i in indices[0]:
    print(data.iloc[i])
