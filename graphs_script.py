import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

# ------------------------
# Configurations générales
# ------------------------
file_path = "TAPE_Survey_Tunisia_Scores_19-09-2025.xlsx"
sheet_name = "Household"
output_dir = "graphs_by_region_municipality"
os.makedirs(output_dir, exist_ok=True)

# ------------------------
# Charger les données
# ------------------------
df = pd.read_excel(file_path, sheet_name=sheet_name)

# ------------------------
# Fonction pour créer radar charts
# ------------------------
def plot_radar(df_row, indicators, title, save_path):
    import matplotlib.pyplot as plt
    import numpy as np
    
    values = df_row[indicators].values.flatten().tolist()
    labels = indicators
    
    # Fermeture du radar
    values += values[:1]
    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    angles += angles[:1]

    plt.figure(figsize=(6,6))
    ax = plt.subplot(111, polar=True)
    ax.plot(angles, values, 'o-', linewidth=2)
    ax.fill(angles, values, alpha=0.25)
    ax.set_thetagrids(np.degrees(angles[:-1]), labels)
    plt.title(title, size=14)
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()

# ------------------------
# Fonction principale pour générer les graphiques
# ------------------------
def create_graphs(data, group_cols, output_dir):
    grouped = data.groupby(group_cols)
    
    for group_name, group_df in grouped:
        # Nom du groupe
        if isinstance(group_name, tuple):
            name_str = "_".join([str(n) for n in group_name])
        else:
            name_str = str(group_name)
        
        folder_path = os.path.join(output_dir, name_str)
        os.makedirs(folder_path, exist_ok=True)
        
        # ------------------------
        # 1. Histogrammes simples
        # ------------------------
        numeric_cols = ['agr_total', 'hh_total', 'area_common_pasture', 'area_private_pasture', 
                        'area_common_crop', 'area_private_crop']
        for col in numeric_cols:
            if col in group_df.columns:
                plt.figure(figsize=(8,5))
                sns.histplot(group_df[col].dropna(), kde=True, bins=10)
                plt.title(f"{col} - {name_str}")
                plt.xlabel(col)
                plt.ylabel("Nombre de ménages")
                plt.savefig(os.path.join(folder_path, f"{col}_histogram.png"))
                plt.close()
        
        # ------------------------
        # 2. Barres empilées Hommes/Femmes
        # ------------------------
        man_cols = ['agr_men_25plus', 'agr_young_male_15_24']
        woman_cols = ['agr_women_25plus', 'agr_young_female_15_24']
        if all(col in group_df.columns for col in man_cols+woman_cols):
            bar_df = pd.DataFrame({
                'Hommes': group_df[man_cols].sum(axis=1),
                'Femmes': group_df[woman_cols].sum(axis=1)
            })
            bar_df_sum = bar_df.sum()
            bar_df_sum.plot(kind='bar', stacked=True, figsize=(6,5), color=['blue','pink'])
            plt.title(f"Répartition hommes/femmes - {name_str}")
            plt.ylabel("Nombre d'agriculteurs")
            plt.savefig(os.path.join(folder_path, "gender_distribution.png"))
            plt.close()
        
        # ------------------------
        # 3. Heatmap corrélations biologiques
        # ------------------------
        bio_columns = [col for col in group_df.columns if col.startswith('index_bio_')]
        if bio_columns:
            plt.figure(figsize=(10,6))
            sns.heatmap(group_df[bio_columns].corr(), annot=True, cmap="coolwarm")
            plt.title(f"Corrélation indicateurs biologiques - {name_str}")
            plt.savefig(os.path.join(folder_path, "bio_indices_correlation.png"))
            plt.close()
        
        # ------------------------
        # 4. Radar chart pour biodiversité
        # ------------------------
        radar_cols = [col for col in group_df.columns if col.startswith('index_gs_')]
        if radar_cols:
            # Prendre la moyenne pour le radar chart
            mean_row = group_df[radar_cols].mean().to_frame().T
            plot_radar(mean_row, radar_cols, f"Radar biodiversité - {name_str}", 
                       os.path.join(folder_path, "biodiversity_radar.png"))

# ------------------------
# Générer graphiques par gouvernorat
# ------------------------
create_graphs(df, group_cols=['region'], output_dir=output_dir)

# ------------------------
# Générer graphiques par municipalité
# ------------------------
create_graphs(df, group_cols=['region','district','municipality'], output_dir=output_dir)

print("✅ Tous les graphiques ont été générés dans le dossier :", output_dir)
