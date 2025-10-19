import pandas as pd
import os
import numpy as np
import plotly.graph_objects as go

# ------------------------------
# Charger les résultats
output_file = "Resultats_10_criteres_FAO_TAPE/TAPE_10_criteres_grouped.xlsx"
df_grouped = pd.read_excel(output_file, index_col=0)

# ------------------------------
# Colonnes des critères
criteria_cols = [
    'Diversity','Synergies','Efficiency','Recycling','Resilience',
    'HumanValues','CultureTraditions','CircularEconomy','CoCreation','Governance'
]

# ------------------------------
# Créer dossier pour graphiques
graph_folder = "Graphs_Radar_Interactive"
os.makedirs(graph_folder, exist_ok=True)
levels = ['region','district','municipality']
for level in levels:
    os.makedirs(os.path.join(graph_folder, level), exist_ok=True)

# ------------------------------
# Fonction radar chart interactif
def radar_chart_interactive(values, labels, title, filename):
    # Normaliser entre 0 et 100
    values_norm = (values - np.min(values)) / (np.max(values) - np.min(values)) * 100

    # Fermer le radar pour un polygone complet
    values_plot = np.concatenate((values_norm, [values_norm[0]]))
    labels_plot = labels + [labels[0]]

    fig = go.Figure()

    # Trace principale
    fig.add_trace(go.Scatterpolar(
        r=values_plot.tolist(),
        theta=labels_plot,
        fill='toself',
        line=dict(color='royalblue', width=3),
        marker=dict(size=8, color='darkblue'),
        hovertemplate='%{theta}: %{r:.1f}<extra></extra>'
    ))

    # Cercle de référence à 100
    fig.add_trace(go.Scatterpolar(
        r=[100]*len(labels_plot),
        theta=labels_plot,
        mode='lines',
        line=dict(color='lightgray', dash='dash'),
        name='Max 100',
        hoverinfo='skip'
    ))

    # Layout optimisé
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickangle=45,
                tickfont=dict(size=10),
                gridcolor='lightgray'
            ),
            angularaxis=dict(
                tickfont=dict(size=11),
            ),
            bgcolor='white'
        ),
        title=dict(text=title, font=dict(size=20, color='darkblue')),
        showlegend=False,
        margin=dict(l=50, r=50, t=100, b=50)
    )

    # Sauvegarde HTML
    fig.write_html(filename)
    print(f"✅ Radar chart interactif enregistré : {filename}")

# ------------------------------
# Génération radar charts interactifs
for level in levels:
    for name, group in df_grouped.groupby(level):
        values = group[criteria_cols].mean().values
        safe_name = str(name).replace(" ", "_").replace(" ", "_")
        filename = os.path.join(graph_folder, level, f"{safe_name}.html")
        radar_chart_interactive(values, criteria_cols, f"{level.capitalize()} : {name}", filename)

print("✅ Tous les graphiques radar interactifs sont générés et enregistrés.")
