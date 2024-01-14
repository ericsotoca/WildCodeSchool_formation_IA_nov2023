import pandas as pd

# Chargement des données
title_basics = pd.read_csv('C:\\Users\\FiercePC\\Desktop\\IA\\Projet_IMDb\\bdd_csv\\title_basics.csv', low_memory=False)
title_ratings = pd.read_csv('C:\\Users\\FiercePC\\Desktop\\IA\\Projet_IMDb\\bdd_csv\\title_ratings.csv', low_memory=False)

# Remplacement des valeurs '\\N' par NaN et conversion des types de données
title_basics.replace({'\\N': None}, inplace=True)
title_basics['isAdult'] = pd.to_numeric(title_basics['isAdult'], errors='coerce')  # Convertit en NaN si non numérique
title_basics['startYear'] = pd.to_numeric(title_basics['startYear'], errors='coerce')
title_basics['endYear'] = pd.to_numeric(title_basics['endYear'], errors='coerce')
title_basics['runtimeMinutes'] = pd.to_numeric(title_basics['runtimeMinutes'], errors='coerce')

# Fusion des ensembles de données
merged_data = pd.merge(title_basics, title_ratings, on='tconst')

# Sélection des colonnes pertinentes
selected_columns = ['tconst', 'primaryTitle', 'genres', 'averageRating', 'numVotes']
filtered_data = merged_data[selected_columns]

# Sauvegarde du dataframe pour une utilisation ultérieure dans le système de recommandation
filtered_data.to_csv('c:/Users/FiercePC/Desktop/IA/Projet_IMDb/approche_8/filtered_imdb_data.csv', index=False)
