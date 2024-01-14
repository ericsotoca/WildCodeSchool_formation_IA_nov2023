import pandas as pd

# Liste des fichiers TSV
tsv_files = [
    "C:\\Users\\FiercePC\\Desktop\\IA\\Projet_IMDb\\bdd_csv\\name_basics.tsv",
    "C:\\Users\\FiercePC\\Desktop\\IA\\Projet_IMDb\\bdd_csv\\title_akas.tsv",
    "C:\\Users\\FiercePC\\Desktop\\IA\\Projet_IMDb\\bdd_csv\\title_basics.tsv",
    "C:\\Users\\FiercePC\\Desktop\\IA\\Projet_IMDb\\bdd_csv\\title_crew.tsv",
    "C:\\Users\\FiercePC\\Desktop\\IA\\Projet_IMDb\\bdd_csv\\title_episode.tsv",
    "C:\\Users\\FiercePC\\Desktop\\IA\\Projet_IMDb\\bdd_csv\\title_ratings.tsv",
    "C:\\Users\\FiercePC\\Desktop\\IA\\Projet_IMDb\\bdd_csv\\title_principals.tsv"
]

chunk_size = 10000  # Taille de chaque chunk, ajuste selon la capacité de ton ordinateur

for file in tsv_files:
    # Initialisation du DataFrame final
    df_final = pd.DataFrame()

    # Lecture du fichier TSV par chunks
    for chunk in pd.read_csv(file, sep='\t', chunksize=chunk_size, low_memory=False):
        # Traitement des valeurs manquantes
        chunk.fillna("Inconnu", inplace=True)

        # Ajout du chunk au DataFrame final
        df_final = pd.concat([df_final, chunk], ignore_index=True)

    # Conversion des types de données pour optimisation (si nécessaire)
    # Exemple : df_final['colonne'] = df_final['colonne'].astype('type')

    # Sauvegarde en format CSV
    csv_file = file.replace('.tsv', '.csv')
    df_final.to_csv(csv_file, index=False)

    print(f"Le fichier {file} a été converti en {csv_file}.")
