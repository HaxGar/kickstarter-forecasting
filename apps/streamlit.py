import datetime as dt
import streamlit as st
import requests
import json

st.title("Kickstarter Predictor")

# Variable booléenne pour contrôler l'affichage de l'onglet de prévision par informations
show_info_prediction = False  # Mettre à True pour réactiver cet onglet

# Dictionnaire de projets exemples
sample_projects = {
    "Projet Tech 1": {"id":"1153426630" ,"name":"GUITAR-JO 2.0 - Make Your Electric Guitar","state":"success","url": "https://www.kickstarter.com/projects/sample/tech-project-1"},
    "Projet Jeu 2": {"id":"1053513419" ,"name":"Charggee: A New Way to Charge. Protect Your Mo","state":"success","url": "https://www.kickstarter.com/projects/1740700612/charggee-a-new-way-to-charge-protect-your-mobile-d?ref=nav_search&result=project&term=Charggee%3A%20A%20New%20Way%20to%20Charge&total_hits=1"},
    "Projet Art 3": {"id":"100411349" ,"name":"E Coin Mining and Rig-Building Workshop","state":"fail","url": "https://www.kickstarter.com/projects/1079598152/e-coin-mining-and-rig-building-workshop/posts"},
    "Projet Art 4": {"id":"1073099678" ,"name":"Pill Swallowing Device","state":"fail","url": "https://www.kickstarter.com/projects/1301067747/pill-swallowing-device/comments"},
}

# Fonction pour remplacer l'importation de predict_api
def call_predict_api(url, comment_type):
    # Cette fonction simule l'appel à l'API
    # Plus tard, vous pourrez la remplacer par un vrai appel API
    # Par exemple: requests.get(f"http://localhost:8000/predict?kickstarterurl={url}&comment_type={comment_type}")
    return {
        "status": "success",
        "score de confiance": 0.6,
        "probability": 0.6
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
                result = call_predict_api(url, comment_type)
                prob = result.get("probability", 0.5)  # Valeur par défaut de 0.5 si non disponible
                st.success(f"Probabilité de réussite : {prob * 100:.1f}%")

elif mode == "Sélection d'un projet exemple":
    st.header("Prévision à partir d'un projet exemple")

    selected_project = st.selectbox(
        "Sélectionnez un projet",
        options=list(sample_projects.keys())
    )

    if selected_project:
        project_data = sample_projects[selected_project]
        st.write(f"Nom: {project_data['name']}")
        st.write(f"URL: {project_data['url']}")
        st.write(f"État actuel: {project_data['state']}")

        if st.button("Analyser ce projet"):
            with st.spinner("Analyse en cours..."):
                # Appel à l'API avec les données du projet sélectionné
                result = call_predict_api(project_data['url'], "all")
                st.write("Résultat de l'analyse: ")
                st.write("Projet: " + selected_project)
                prob = result.get("probability", 0.5)  # Valeur par défaut de 0.5 si non disponible
                st.success(f"Probabilité de réussite : {prob * 100:.1f}%")
