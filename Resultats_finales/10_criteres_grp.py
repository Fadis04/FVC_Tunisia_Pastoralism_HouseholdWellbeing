import pandas as pd
import os

# ------------------------------
# 1️⃣ Charger le fichier Excel
file_path = "TAPE_Survey_Tunisia_Scores_19-09-2025.xlsx"
sheet_name = "Household"  # adapte si nécessaire
df = pd.read_excel(file_path, sheet_name=sheet_name)

# ------------------------------
# 2️⃣ Nettoyage des colonnes
# Remplacer .5 par 0.5 et les valeurs manquantes par 0
df = df.fillna(0)
for col in df.columns:
    df[col] = df[col].replace({'.5': 0.5})

# ------------------------------
# 3️⃣ Créer les 10 critères pour chaque ménage
df['Diversity'] = (
    df.get('score_dm_man_crop', 0) +
    df.get('score_dm_man_animals', 0) +
    df.get('score_dm_man_animal_products', 0) +
    df.get('score_dm_woman_crop', 0) +
    df.get('score_dm_woman_animals', 0) +
    df.get('score_dm_woman_animal_products', 0)
)

df['Synergies'] = (
    df.get('score_bio_dung_beetles', 0) +
    df.get('score_bio_nasty_flies', 0) +
    df.get('score_bio_ivermectin_use', 0) +
    df.get('score_bio_amphibians', 0) +
    df.get('score_bio_carnivores', 0) +
    df.get('score_bio_birds', 0) +
    df.get('score_bio_poison_use', 0) +
    df.get('score_bio_hunt', 0) +
    df.get('score_bio_invasive', 0)
)

df['Efficiency'] = (
    df.get('score_water_sources', 0) +
    df.get('score_water_quality', 0) +
    df.get('score_dm_man_crop', 0) +
    df.get('score_dm_man_animals', 0) +
    df.get('score_dm_woman_crop', 0) +
    df.get('score_dm_woman_animals', 0)
)

df['Recycling'] = (
    df.get('score_bio_dung_beetles', 0) +
    df.get('score_bio_ivermectin_use', 0)
)

df['Resilience'] = (
    df.get('score_amphibian_richness', 0) +
    df.get('score_carnivore_richness', 0) +
    df.get('score_bird_richness', 0) +
    df.get('score_income_compare', 0) +
    df.get('score_production_future', 0)
)

df['HumanValues'] = (
    df.get('score_own_credit', 0) +
    df.get('org_participation_score', 0)
)

df['CultureTraditions'] = df.get('farmer_policy_score', 0)
df['CircularEconomy'] = df.get('org_participation_score', 0)
df['CoCreation'] = df.get('org_participation_score', 0)

df['Governance'] = (
    df.get('market_access_score', 0) +
    df.get('control_seeds_score', 0) +
    df.get('control_livestock_score', 0)
)

# ------------------------------
# 4️⃣ Agrégation par région, district et municipalité
group_cols = ['region', 'district', 'municipality']
criteria_cols = [
    'Diversity','Synergies','Efficiency','Recycling','Resilience',
    'HumanValues','CultureTraditions','CircularEconomy','CoCreation','Governance'
]

# Moyenne par regroupement
df_grouped = df.groupby(group_cols).agg({col: 'mean' for col in criteria_cols})

# Ajouter le nombre de ménages par groupe
df_grouped['nb_menages'] = df.groupby(group_cols).size()

# ------------------------------
# 5️⃣ Sauvegarder le résultat
output_folder = "Resultats_10_criteres_FAO_TAPE"
os.makedirs(output_folder, exist_ok=True)
output_file = os.path.join(output_folder, "TAPE_10_criteres_grouped.xlsx")
df_grouped.to_excel(output_file)

print(f"✅ Fichier enregistré : {output_file}")
print(df_grouped.head())
