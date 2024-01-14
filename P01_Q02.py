import pandas as pd
import matplotlib.pyplot as plt

# Chargement des données
df = pd.read_csv('C:\\Users\\FiercePC\\Desktop\\IA\\Projet_IMDb\\bdd_csv\\title_basics.csv', low_memory=False)

# Conversion des types de données
df['startYear'] = pd.to_numeric(df['startYear'], errors='coerce')
df['runtimeMinutes'] = pd.to_numeric(df['runtimeMinutes'], errors='coerce')

# Suppression des valeurs NaN, des valeurs aberrantes et des années supérieures à 2023
df = df.dropna(subset=['runtimeMinutes', 'startYear'])
df = df[(df['runtimeMinutes'] > 0) & (df['runtimeMinutes'] < 300) & (df['startYear'] <= 2023)]

# Calcul de la moyenne de la durée par année
mean_runtime_per_year = df.groupby('startYear')['runtimeMinutes'].mean().reset_index()

# Préparation du graphique
plt.figure(figsize=(15, 7))
plt.plot(mean_runtime_per_year['startYear'], mean_runtime_per_year['runtimeMinutes'], marker='o')

# Réglage des étiquettes de l'axe des x pour afficher par décennie
plt.xticks(range(int(mean_runtime_per_year['startYear'].min()), int(mean_runtime_per_year['startYear'].max())+1, 10), rotation=45)

# Autres configurations du graphique
plt.title('Évolution de la Durée Moyenne des Films par Année', fontsize=16)
plt.xlabel('Année', fontsize=14)
plt.ylabel('Durée Moyenne (minutes)', fontsize=14)
plt.grid(True)
plt.tight_layout()  # Ajustement automatique pour s'assurer que tout tient dans le graphique

# Affichage du graphique
plt.show()
