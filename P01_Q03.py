import pandas as pd

# Chemins vers les fichiers CSV
path_principals = 'C:\\Users\\FiercePC\\Desktop\\IA\\Projet_IMDb\\bdd_csv\\title_principals.csv'
path_basics = 'C:\\Users\\FiercePC\\Desktop\\IA\\Projet_IMDb\\bdd_csv\\title_basics.csv'

# Taille de chaque chunk
chunk_size = 10000

# Initialiser des ensembles vides pour stocker les identifiants uniques
actors_in_movies = set()
actors_in_tv_series = set()

# Fonction pour traiter chaque chunk
def process_chunk(chunk, title_ids):
    # Filtrer pour obtenir seulement les acteurs et actrices
    actors_chunk = chunk[chunk['category'].isin(['actor', 'actress'])]
    # Trouver les acteurs qui sont dans les titres donnés (movies ou tv_series)
    return set(actors_chunk[actors_chunk['tconst'].isin(title_ids)]['nconst'])

# Lire title_basics.csv pour identifier les movies et tv_series
df_basics = pd.read_csv(path_basics)
movies_ids = set(df_basics[df_basics['titleType'] == 'movie']['tconst'])
tv_series_ids = set(df_basics[df_basics['titleType'] == 'tvSeries']['tconst'])

# Lecture de title_principals.csv par chunks
for chunk in pd.read_csv(path_principals, chunksize=chunk_size):
    actors_in_movies |= process_chunk(chunk, movies_ids)
    actors_in_tv_series |= process_chunk(chunk, tv_series_ids)

# Trouver les acteurs communs
common_actors = actors_in_movies.intersection(actors_in_tv_series)

# Afficher les résultats
print(common_actors)
