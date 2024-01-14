import pandas as pd

# Chemin vers les fichiers CSV
path_ratings = 'C:\\Users\\FiercePC\\Desktop\\IA\\Projet_IMDb\\bdd_csv\\title_ratings.csv'
path_basics = 'C:\\Users\\FiercePC\\Desktop\\IA\\Projet_IMDb\\bdd_csv\\title_basics.csv'

# Taille de chaque chunk
chunk_size = 10000

# Initialiser un DataFrame vide pour stocker les notes des films
df_movies_ratings = pd.DataFrame()

# Lecture de title_basics.csv pour obtenir les identifiants des films
df_basics = pd.read_csv(path_basics)
movie_ids = set(df_basics[df_basics['titleType'] == 'movie']['tconst'])

# Lecture de title_ratings.csv par chunks
for chunk in pd.read_csv(path_ratings, chunksize=chunk_size):
    # Filtrer pour obtenir seulement les notes des films
    movies_chunk = chunk[chunk['tconst'].isin(movie_ids)]
    # Concaténer avec le DataFrame global
    df_movies_ratings = pd.concat([df_movies_ratings, movies_chunk], ignore_index=True)

# Trier les films en fonction de leur note moyenne
top_rated_movies = df_movies_ratings.sort_values(by='averageRating', ascending=False)

# Afficher les films les mieux notés
print(top_rated_movies.head(10))
