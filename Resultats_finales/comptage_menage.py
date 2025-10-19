import pandas as pd

# Charger le fichier Excel
file_path = "TAPE_Survey_Tunisia_Scores_19-09-2025.xlsx"
sheet_name = "Household"
df = pd.read_excel(file_path, sheet_name=sheet_name)

# Vérifier les colonnes pour le regroupement
print(df[['region', 'district', 'municipality']].head())

# Compter le nombre de ménages par regroupement
household_counts = df.groupby(['region', 'district', 'municipality']).size().reset_index(name='nb_menages')

# Afficher le résultat
print(household_counts)
