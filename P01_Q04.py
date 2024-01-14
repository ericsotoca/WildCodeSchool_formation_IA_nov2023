import pandas as pd
from datetime import datetime

# Chemin vers le fichier CSV
path_names = 'C:\\Users\\FiercePC\\Desktop\\IA\\Projet_IMDb\\bdd_csv\\name_basics.csv'

# Taille de chaque chunk
chunk_size = 10000

# Initialiser une liste pour stocker les âges
ages = []

# Fonction pour calculer l'âge
def calculate_age(birth_year, death_year):
    current_year = datetime.now().year
    if pd.isna(death_year):
        return current_year - birth_year
    else:
        return death_year - birth_year

# Lecture de name_basics.csv par chunks
for chunk in pd.read_csv(path_names, chunksize=chunk_size):
    # Filtrer pour obtenir seulement les acteurs et actrices
    actors_chunk = chunk[chunk['primaryProfession'].str.contains('actor|actress', na=False)]
    # Calculer l'âge pour chaque acteur/actrice et l'ajouter à la liste
    for index, row in actors_chunk.iterrows():
        if not pd.isna(row['birthYear']):
            age = calculate_age(row['birthYear'], row['deathYear'])
            ages.append(age)

# Calculer l'âge moyen
average_age = sum(ages) / len(ages)

# Afficher l'âge moyen
print(f"L'âge moyen des acteurs est de {average_age:.2f} ans.")
