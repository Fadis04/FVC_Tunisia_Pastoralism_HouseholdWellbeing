import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# === 1. Chargement des données ===
file_path = "TAPE_Survey_Tunisia_Scores_19-09-2025.xlsx"
sheet_name = "Household"

df = pd.read_excel(file_path, sheet_name=sheet_name)

# === 2. Sélection des indices représentatifs ===
elements = {
    "Diversité": df["index_animal_biodiversity"],
    "Synergies": df["index_gs_herb_div"],
    "Efficience": df["index_man_prod_assets"],
    "Recyclage": df["index_bio_insects"],
    "Résilience": df["index_bio_mig_birds"],
    "Valeurs humaines et sociales": df["index_woman_total"],
    "Culture et traditions": df["index_earning_perception"],
    "Gouvernance": df["org_participation_score"],
    "Économie circulaire": df["score_income_compare"],
    "Co-création": df["farmer_policy_score"]
}

# === 3. Calcul des moyennes ===
scores = [v.mean() for v in elements.values()]
labels = list(elements.keys())

# Boucler pour fermer la forme du radar
scores += scores[:1]
angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
angles += angles[:1]

# === 4. Création du graphique radar ===
plt.figure(figsize=(8, 8))
plt.polar(angles, scores, 'b-', linewidth=2)
plt.fill(angles, scores, color='skyblue', alpha=0.25)

# Personnalisation
plt.xticks(angles[:-1], labels, fontsize=9)
plt.title("TAPE - Caractérisation moyenne de la transition agroécologique", 
          size=13, weight='bold', pad=20)
plt.tight_layout()

# === 5. Sauvegarde automatique du graphique ===
output_file = "graph_radar_moyenne.png"
plt.savefig(output_file, dpi=300, bbox_inches='tight')
plt.close()

print(f"✅ Graphique radar enregistré sous : {output_file}")
