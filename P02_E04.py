from flask import Flask, render_template, request
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler
from sklearn.compose import ColumnTransformer

app = Flask(__name__)

# Assurez-vous que cette ligne est placée avant son utilisation dans la transformation
data = pd.read_csv('C:\\Users\\FiercePC\\Desktop\\IA\\Projet_IMDb\\approche_8\\filtered_imdb_data.csv')

# Prétraitement des données
preprocessor = ColumnTransformer(
    transformers=[
        ('genres', OneHotEncoder(), ['genres']),
        ('num', MinMaxScaler(), ['averageRating', 'numVotes'])
    ])
X = preprocessor.fit_transform(data[['genres', 'averageRating', 'numVotes']])
model = NearestNeighbors(n_neighbors=5, algorithm='brute')
model.fit(X)

@app.route('/')
def index():
    return render_template('index.html', recommandations=pd.DataFrame())

@app.route('/recommander', methods=['POST'])
def recommander():
    titre_film = request.form.get('titre_film')
    recommandations = rechercher_films_similaires(titre_film)
    return render_template('index.html', recommandations=recommandations, titre_film=titre_film)

def rechercher_films_similaires(titre):
    # Trouver l'index du film
    titre_normalise = titre.lower()
    film_index = data[data['primaryTitle'].str.lower() == titre_normalise].index

    if film_index.empty:
        return pd.DataFrame()

    test_film = X[film_index[0]]
    test_film_reshaped = test_film.reshape(1, -1)
    distances, indices = model.kneighbors(test_film_reshaped)

    # Récupérer les films recommandés
    recommandations = data.iloc[indices[0]]
    return recommandations

if __name__ == '__main__':
    app.run(debug=True)
