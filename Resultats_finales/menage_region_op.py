import pandas as pd
import plotly.graph_objects as go
import os

# ------------------------------
# Charger les données
file_path = "TAPE_Survey_Tunisia_Scores_19-09-2025.xlsx"
sheet_name = "Household"
df = pd.read_excel(file_path, sheet_name=sheet_name).fillna(0)

# ------------------------------
# Calcul du nombre de ménages par région/district/municipalité
group_cols = ['region', 'district', 'municipality']
df_counts = df.groupby(group_cols).size().reset_index(name='nb_menages')

# ------------------------------
# Créer dossier pour sauvegarder graphes
graph_folder = "Graphs_Barplots_Interactive_Optimized"
os.makedirs(graph_folder, exist_ok=True)

# ------------------------------
# Palette harmonieuse par district
district_palette = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2']

# ------------------------------
# Générer graphes interactifs
for region_name, region_group in df_counts.groupby('region'):

    fig = go.Figure()

    districts = region_group['district'].unique()
    for i, district_name in enumerate(districts):
        district_group = region_group[region_group['district']==district_name]
        color = district_palette[i % len(district_palette)]

        fig.add_trace(go.Bar(
            x=district_group['municipality'],
            y=district_group['nb_menages'],
            name=district_name,
            marker=dict(
                color=color,
                line=dict(color='black', width=2)  # Cadre noir pour toutes les barres
            ),
            text=district_group['nb_menages'],
            textposition='inside',
            hovertemplate=(
                "<b>Région:</b> %{customdata[0]}<br>"
                "<b>District:</b> %{customdata[1]}<br>"
                "<b>Municipalité:</b> %{customdata[2]}<br>"
                "<b>Ménages:</b> %{y}"
            ),
            customdata=district_group[['region','district','municipality']]
        ))

    # ------------------------------
    # Layout optimisé
    fig.update_layout(
        barmode='group',
        title=f"Répartition des ménages par districts et municipalités ({region_name})",
        yaxis_title="Nombre de ménages",
        xaxis_title="Municipalités",
        xaxis_tickangle=-45,  # incliner les noms des municipalités
        xaxis_tickfont=dict(size=10),
        plot_bgcolor='white',
        title_font_size=22,
        yaxis=dict(gridcolor='lightgray'),
        legend_title="Districts",
        margin=dict(l=50, r=50, t=100, b=150),
        uniformtext_minsize=10,
        uniformtext_mode='hide'
    )

    # ------------------------------
    # Affichage et sauvegarde
    fig.show()
    safe_name = region_name.replace(" ", "_").replace(" ","_")
    fig.write_html(os.path.join(graph_folder, f"menages_{safe_name}_values_inside.html"))
