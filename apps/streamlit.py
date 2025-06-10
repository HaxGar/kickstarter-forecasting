import datetime as dt
import streamlit as st

from API import predict_api

st.title("Kickstarter Predictor")

# Variable booléenne pour contrôler l'affichage de l'onglet de prévision par informations
show_info_prediction = False  # Mettre à True pour réactiver cet onglet

# Dictionnaire de projets exemples
sample_projects = {
    "Projet Tech 1": {"url": "https://www.kickstarter.com/projects/sample/tech-project-1", "comment_type": "all"},
    "Projet Jeu 2": {"url": "https://www.kickstarter.com/projects/sample/game-project-2", "comment_type": "all"},
    "Projet Art 3": {"url": "https://www.kickstarter.com/projects/sample/art-project-3", "comment_type": "all"},
}

# Options pour le menu latéral
sidebar_options = []
if show_info_prediction:
    sidebar_options.append("Prévision à partir des informations du projet")
sidebar_options.extend([
    "Prévision à partir d'un lien Kickstarter",
    "Sélection d'un projet exemple"
])

mode = st.sidebar.radio(
    "Choisissez une option",
    tuple(sidebar_options)
)

if show_info_prediction and mode == "Prévision à partir des informations du projet":
    st.header("Prévision du montant cagnotté")
    name = st.text_input("Nom du projet")
    deadline = st.date_input("Deadline", dt.date.today())
    duration = st.number_input("Durée de campagne (jours)", min_value=1, step=1)
    category = st.text_input("Thème ou catégorie")

    if st.button("Mettre à jour la prédiction"):
        if not name or not category:
            st.warning("Veuillez remplir tous les champs requis.")
        else:
            result = 'test'#predict_target(
                #name=name,
                #deadline=deadline.isoformat(),
                #duration=int(duration),
                #category=category,
            #)
            amount = result.get("amount")
            st.success(f"Montant recommandé : {amount} euros")

elif mode == "Prévision à partir d'un lien Kickstarter":
    st.header("Prévision à partir d'un lien Kickstarter")
    url = st.text_input("Lien du projet Kickstarter")
    comment_type = st.selectbox("Type de commentaires à analyser", ["all", "positifs", "négatifs"])

    if st.button("Analyser le lien"):
        if not url:
            st.warning("Veuillez fournir un lien")
        else:
            # Appel à l'API qui n'est pas opérationnelle pour l'instant
            with st.spinner("Analyse en cours..."):
                result = 'test2' #predict_api(url, comment_type)
                prob = 10 #result.get("probability")
                st.success(f"Probabilité de réussite : {prob * 100:.1f}%")

elif mode == "Sélection d'un projet exemple":
    st.header("Prévision à partir d'un projet exemple")

    selected_project = st.selectbox(
        "Sélectionnez un projet",
        options=list(sample_projects.keys())
    )

    if selected_project:
        project_data = sample_projects[selected_project]
        st.write(f"URL: {project_data['url']}")

        if st.button("Analyser ce projet"):
            with st.spinner("Analyse en cours..."):
                # Appel à l'API qui n'est pas opérationnelle pour l'instant
                result = 'test2' #predict_api(project_data['url'], project_data['comment_type'])
                st.write("Résultat de l'analyse: ")
                st.write("Projet: " + selected_project)
                prob = 10 #result.get("probability")
                st.success(f"Probabilité de réussite : {prob * 100:.1f}%")
