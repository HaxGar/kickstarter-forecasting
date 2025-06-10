# N'importez que streamlit, rien d'autre
import streamlit as st

# Titre principal
st.title("Kickstarter Predictor")

# Création des onglets - utilisation de st.tabs au lieu de radio buttons pour éviter les problèmes
tab1, tab2, tab3 = st.tabs([
    "Prévision à partir des informations du projet",
    "Prévision à partir d'un lien Kickstarter",
    "Sélection d'un projet exemple"
])

# Contenu de l'onglet 1
with tab1:
    st.header("Prévision à partir des informations du projet")
    st.info("Cette fonctionnalité est en cours de développement...")

# Contenu de l'onglet 2
with tab2:
    st.header("Prévision à partir d'un lien Kickstarter")
    url = st.text_input("Lien du projet Kickstarter")
    comment_type = st.selectbox("Type de commentaires à analyser", ["all", "positifs", "négatifs"])

    if st.button("Analyser le lien"):
        if not url:
            st.warning("Veuillez fournir un lien")
        else:
            st.success("Simulation: Probabilité de réussite: 60%")
            st.info("Note: Cette fonctionnalité est en développement")

# Contenu de l'onglet 3
with tab3:
    st.header("Prévision à partir d'un projet exemple")

    # Version simplifiée des projets
    projects = ["Projet Tech 1", "Projet Jeu 2", "Projet Art 3", "Projet Art 4"]
    selected = st.selectbox("Sélectionnez un projet", projects)

    if selected:
        st.write(f"Projet sélectionné: {selected}")

        if st.button("Analyser ce projet"):
            st.success(f"Simulation: Probabilité de réussite: 60%")
            st.info("Note: Cette fonctionnalité est en développement")
