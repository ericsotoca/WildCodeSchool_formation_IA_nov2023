import pandas as pd
from io import StringIO

# Liste des fichiers CSV
csv_files = [
    "C:\\Users\\FiercePC\\Desktop\\IA\\Projet_IMDb\\bdd_csv\\title_principals.csv"
    "C:\\Users\\FiercePC\\Desktop\\IA\\Projet_IMDb\\bdd_csv\\title_akas.csv",
    "C:\\Users\\FiercePC\\Desktop\\IA\\Projet_IMDb\\bdd_csv\\title_basics.csv",
    "C:\\Users\\FiercePC\\Desktop\\IA\\Projet_IMDb\\bdd_csv\\title_crew.csv",
    "C:\\Users\\FiercePC\\Desktop\\IA\\Projet_IMDb\\bdd_csv\\title_episode.csv",
    "C:\\Users\\FiercePC\\Desktop\\IA\\Projet_IMDb\\bdd_csv\\title_ratings.csv",
    "C:\\Users\\FiercePC\\Desktop\\IA\\Projet_IMDb\\bdd_csv\\name_basics.csv",
]

for file in csv_files:
    try:
        # Lecture du fichier CSV
        df = pd.read_csv(file)

        # Création du fichier de sortie
        output_file = file.replace('.csv', '_analyse.txt')
        with open(output_file, 'w') as f:
            # Affichage et écriture du nom du fichier
            filename = file.split('\\')[-1]
            f.write(f"Analyse de : {filename}\n")

            # Aperçu des données
            f.write("Aperçu des données:\n")
            f.write(df.head().to_string() + "\n")

            # Informations sur les données
            f.write("\nInformations sur les données:\n")
            buffer = StringIO()  # Utilisation de StringIO pour capturer la sortie
            df.info(buf=buffer)
            f.write(buffer.getvalue() + "\n")

            # Statistiques descriptives
            f.write("\nStatistiques descriptives:\n")
            f.write(df.describe(include='all').to_string() + "\n")

            # Remplacement des '\N' par NaN
            df.replace('\\N', pd.NA, inplace=True)

            # Compte des valeurs manquantes après remplacement
            f.write("\nValeurs manquantes après remplacement des '\\N' :\n")
            f.write(df.isna().sum().to_string() + "\n")

            # Analyse des types de données
            f.write("\nAnalyse des types de données:\n")
            for col in df.columns:
                f.write(f"{col}: {df[col].dtype}\n")

            # Vérification des doublons
            f.write("\nDoublons:\n")
            f.write(str(df.duplicated().sum()) + "\n")

            f.write("\n" + "="*50 + "\n")
    except FileNotFoundError as e:
        print(f"Erreur : Le fichier {file} n'a pas été trouvé.")
