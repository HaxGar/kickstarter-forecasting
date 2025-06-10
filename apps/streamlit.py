import datetime as dt
import streamlit as st

#from API import predict_target, predict_success

st.title("Kickstarter Predictor")

mode = st.sidebar.radio(
    "Choisissez une option",
    (
        "Prévision à partir des informations du projet",
        "Prévision à partir d'un lien Kickstarter",
    ),
)

if mode == "Prévision à partir des informations du projet":
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

else:
    st.header("Prévision à partir d'un lien Kickstarter")
    url = st.text_input("Lien du projet Kickstarter")

    if st.button("Analyser le lien"):
        if not url:
            st.warning("Veuillez fournir un lien")
        else:
            result = 'test2' #predict_success(url)
            prob = 10 #result.get("probability")
            st.success(f"Probabilité de réussite : {prob * 100:.1f}%")
