import pandas as pd

# Chemins des fichiers
path_principals = 'C:\\Users\\FiercePC\\Desktop\\IA\\Projet_IMDb\\bdd_csv\\title_principals.csv'
path_names = 'C:\\Users\\FiercePC\\Desktop\\IA\\Projet_IMDb\\bdd_csv\\name_basics.csv'
path_basics = 'C:\\Users\\FiercePC\\Desktop\\IA\\Projet_IMDb\\bdd_csv\\title_basics.csv'

# Taille de chaque chunk
chunk_size = 10000

# Lecture des données des acteurs
df_principals = pd.concat([chunk[chunk['category'].isin(['actor', 'actress'])]
                           for chunk in pd.read_csv(path_principals, chunksize=chunk_size)])

# Lecture des données de base des titres pour les informations temporelles
df_basics = pd.concat([chunk[['tconst', 'startYear']]
                       for chunk in pd.read_csv(path_basics, chunksize=chunk_size, usecols=['tconst', 'startYear'])])

# Jointure pour associer les années aux acteurs
df_principals = df_principals.merge(df_basics, on='tconst', how='left')

# Comptage du nombre d'apparitions de chaque acteur par année
actor_counts_by_year = df_principals.groupby(['nconst', 'startYear']).size().reset_index(name='count')

# Lecture des informations des acteurs
df_names = pd.concat([chunk for chunk in pd.read_csv(path_names, chunksize=chunk_size)])

# Fusion des données des acteurs avec leur nombre d'apparitions
actor_info = df_names.merge(actor_counts_by_year, on='nconst')

# Tri des acteurs par leur nombre total d'apparitions et par année
actor_info_sorted = actor_info.sort_values(by=['count', 'startYear'], ascending=[False, True])

# Affichage des acteurs les plus présents et des périodes les plus actives pour ces acteurs
print(actor_info_sorted[['primaryName', 'startYear', 'count']].head(10))