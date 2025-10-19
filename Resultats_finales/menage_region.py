import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

# ------------------------------
# Charger les données
file_path = "TAPE_Survey_Tunisia_Scores_19-09-2025.xlsx"
sheet_name = "Household"
df = pd.read_excel(file_path, sheet_name=sheet_name)

# Remplacer valeurs manquantes par 0
df = df.fillna(0)

# ------------------------------
# Créer un dossier pour sauvegarder les graphes
graph_folder = "Graphs_Barplots"
os.makedirs(graph_folder, exist_ok=True)

# ------------------------------
# Calculer le nombre de ménages par région, district, municipalité
group_cols = ['region', 'district', 'municipality']
df_counts = df.groupby(group_cols).size().reset_index(name='nb_menages')

# ------------------------------
# Couleurs par région
region_colors = {
    "Bizerte": sns.color_palette("Blues", n_colors=10),
    "Sidi Bouzid": sns.color_palette("Oranges", n_colors=10)
}

# ------------------------------
# 1️⃣ Graphique : Nombre total de ménages par région
region_counts = df_counts.groupby('region')['nb_menages'].sum().reset_index()
plt.figure(figsize=(8,6))
colors = [region_colors[r][5] if r in region_colors else "grey" for r in region_counts['region']]
ax = plt.bar(region_counts['region'], region_counts['nb_menages'], color=colors)
plt.title("Nombre total de ménages par région", fontsize=14)
plt.xlabel("Région", fontsize=12)
plt.ylabel("Nombre de ménages", fontsize=12)
plt.xticks(rotation=45)

# Ajouter valeurs sur chaque barre
for i, val in enumerate(region_counts['nb_menages']):
    plt.text(i, val+1, str(val), ha='center', va='bottom', fontsize=10)

plt.tight_layout()
plt.savefig(os.path.join(graph_folder, "menages_par_region_colored.png"), dpi=200)
plt.close()
print("✅ Graphique nombre de ménages par région enregistré.")

# ------------------------------
# 2️⃣ Graphique : Répartition par district et municipalité avec couleurs par région
for region_name, region_group in df_counts.groupby('region'):
    plt.figure(figsize=(10,6))
    n_munis = region_group['municipality'].nunique()
    palette = region_colors.get(region_name, sns.color_palette("Greys", n_colors=n_munis))
    ax = sns.barplot(
        data=region_group,
        x='district',
        y='nb_menages',
        hue='municipality',
        palette=palette
    )
    plt.title(f"Répartition des ménages dans les districts et municipalités de {region_name}", fontsize=14)
    plt.xlabel("District", fontsize=12)
    plt.ylabel("Nombre de ménages", fontsize=12)
    plt.xticks(rotation=45)
    plt.legend(title="Municipalité", bbox_to_anchor=(1.05, 1), loc='upper left')

    # Ajouter valeurs sur chaque barre
    for p in ax.patches:
        height = p.get_height()
        ax.annotate(f"{int(height)}", (p.get_x() + p.get_width() / 2., height),
                    ha='center', va='bottom', fontsize=9, color='black', rotation=90)

    plt.tight_layout()
    safe_name = region_name.replace(" ", "_").replace(" ", "_")
    filename = os.path.join(graph_folder, f"repartition_menages_{safe_name}.png")
    plt.savefig(filename, dpi=200)
    plt.close()
    print(f"✅ Graphique répartition ménages pour {region_name} enregistré.")

print("✅ Tous les graphiques sont générés avec couleurs différenciées par région et valeurs affichées.")
