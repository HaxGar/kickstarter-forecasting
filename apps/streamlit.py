import streamlit as st
import datetime as dt

# ===============================
# Configuration des onglets visibles
# ===============================
# Variables de contrôle pour activer/désactiver les onglets
show_info_prediction_tab = False  # Onglet "Prévision à partir des informations du projet"
show_link_prediction_tab = True   # Onglet "Prévision à partir d'un lien Kickstarter"
show_sample_project_tab = True    # Onglet "Sélection d'un projet exemple"

# ===============================
# Interface Streamlit
# ===============================
st.title("Kickstarter Predictor")

# Construction dynamique du menu latéral en fonction des variables de contrôle
sidebar_options = []

if show_info_prediction_tab:
    sidebar_options.append("Prévision à partir des informations du projet")
if show_link_prediction_tab:
    sidebar_options.append("Prévision à partir d'un lien Kickstarter")
if show_sample_project_tab:
    sidebar_options.append("Sélection d'un projet exemple")

# Afficher le menu uniquement s'il y a au moins une option
if sidebar_options:
    mode = st.sidebar.radio("Choisissez une option", tuple(sidebar_options))
else:
    st.warning("Aucun onglet n'est actuellement activé. Veuillez modifier les variables de configuration.")
    mode = None

# ===============================
# Contenu des onglets
# ===============================

# Onglet 1 : Prévision à partir des informations du projet
if show_info_prediction_tab and mode == "Prévision à partir des informations du projet":
    st.header("Prévision du montant cagnotté")
    st.write("Cette fonctionnalité est en cours de développement...")

    # Contenu vide pour l'instant, à compléter plus tard

# Onglet 2 : Prévision à partir d'un lien Kickstarter
elif show_link_prediction_tab and mode == "Prévision à partir d'un lien Kickstarter":
    st.header("Prévision à partir d'un lien Kickstarter")
    url = st.text_input("Lien du projet Kickstarter")
    comment_type = st.selectbox("Type de commentaires à analyser", ["all", "positifs", "négatifs"])

    if st.button("Analyser le lien"):
        if not url:
            st.warning("Veuillez fournir un lien")
        else:
            with st.spinner("Analyse en cours..."):
                # Simulation de résultat pour l'instant
                st.success(f"Probabilité de réussite : {60}%")
                st.info("Note: L'API n'est pas encore opérationnelle.")

# Onglet 3 : Sélection d'un projet exemple
elif show_sample_project_tab and mode == "Sélection d'un projet exemple":
    st.header("Prévision à partir d'un projet exemple")

    # Dictionnaire de projets exemples
    sample_projects = {
        "Projet Tech 1": {"id":"1153426630", "name":"GUITAR-JO 2.0 - Make Your Electric Guitar", "state":"success", "url": "https://www.kickstarter.com/projects/sample/tech-project-1"},
        "Projet Jeu 2": {"id":"1053513419", "name":"Charggee: A New Way to Charge", "state":"success", "url": "https://www.kickstarter.com/projects/1740700612/charggee-a-new-way-to-charge-protect-your-mobile-d"},
        "Projet Art 3": {"id":"100411349", "name":"E Coin Mining and Rig-Building Workshop", "state":"fail", "url": "https://www.kickstarter.com/projects/1079598152/e-coin-mining-and-rig-building-workshop/posts"},
        "Projet Art 4": {"id":"1073099678", "name":"Pill Swallowing Device", "state":"fail", "url": "https://www.kickstarter.com/projects/1301067747/pill-swallowing-device/comments"},
    }

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
                # Simulation de résultat pour l'instant
                st.write("Résultat de l'analyse: ")
                st.write("Projet: " + selected_project)
                st.success(f"Probabilité de réussite : {60}%")
                st.info("Note: L'API n'est pas encore opérationnelle.")
