import datetime as dt
import streamlit as st
import requests
import pandas as pd


st.title("KickPredict")

st.markdown("Predict your likely Kickstarter project success or failure based on comments posted by backers.")

tab1, tab2 = st.tabs([
    "Predict with validation projects",
    "Predict current project"
])

with tab1:
    # Sample projects dictionary
    sample_projects = {
        "1": {
            "id": "1153426630",
            "name": "GUITAR-JO 2.0 - Make Your Electric Guitar",
            "url": "https://www.kickstarter.com/projects/jlangberg/guitar-jo-20-make-your-electric-guitar-sound-like"
        },
        "2": {
            "id": "1053513419",
            "name": "Charggee: A New Way to Charge",
            "url": "https://www.kickstarter.com/projects/1740700612/charggee-a-new-way-to-charge-protect-your-mobile-d"
        },
        "3": {
            "id": "100411349",
            "name": "E Coin Mining and Rig-Building Workshop",
            "url": "https://www.kickstarter.com/projects/1079598152/e-coin-mining-and-rig-building-workshop"
        },
        "4": {
            "id": "1073099678",
            "name": "Pill Swallowing Device",
            "url": "https://www.kickstarter.com/projects/1301067747/pill-swallowing-device"
        },
    }

    # Sélection du projet par son alias
    choix = st.selectbox(
        "choose a project :",
        options=list(sample_projects.keys()),
        format_func=lambda x: sample_projects[x]["name"]  # affiche le “name” dans la liste
    )

    st.info(sample_projects[choix]["url"])

    if st.button("Predict"):

        # Récupération de l’ID correspondant
        id_projet = sample_projects[choix]["id"]

        params = {
                    "id_projet": id_projet
                }

        response = requests.get("https://kickstarter-api-195095770000.europe-west1.run.app/predict_par_id", params=params)
#        response = requests.get("http://localhost:8080/predict_par_id", params=params)
        print(response)

        if response.status_code == 200:
            message = response.json().get("message", None)
            project_name = response.json().get("project_name", None)
            comments = response.json().get("comments", None)
            df_comments = pd.DataFrame(comments, columns=["comments"])
            probability = response.json().get("probability_key", None)
            prediction = response.json().get("prediction", None)

            if message:
                if prediction == 1:
                    #st.success(project_name)
                    st.balloons()
                    col1, col2 = st.columns([2,1])
                    with col1:
                        st.success(message)
                    with col2:
                        st.info(f"Probability of success:  \n" f"**{probability*100:.1f} %**")
                    st.markdown("##### Based on the following posted comments:")
                    for c in comments:
                        st.markdown(f"- {c}")

                else:
                    #st.error(project_name)
                    st.snow()
                    col1, col2 = st.columns([2,1])
                    with col1:
                        st.error(message)
                    with col2:
                        st.info("Probability of failure:  \n" f"**{probability*100:.1f} %**")
                    st.markdown("##### Based on the following posted comments:")
                    for c in comments:
                        st.markdown(f"- {c}")

            else:
                st.error("We are unable to retrieve a prediction for this project")

with tab2:
    project_url = st.text_input("Enter the project url :", "")
    # Bouton pour déclencher la requête
    if st.button("Scrape and predict"):
        params = {
                    "url": project_url
                }

        response = requests.get("https://kickstarter-api-195095770000.europe-west1.run.app/predict_by_url", params=params)
#        response = requests.get("http://localhost:8080/predict_by_url", params=params)
        print(response)

        if response.status_code == 200:
            message = response.json().get("message", None)
            project_name = response.json().get("project_name", None)
            comments = response.json().get("comments", None)
            df_comments = pd.DataFrame(comments, columns=["comments"])
            probability = response.json().get("probability_key", None)
            prediction = response.json().get("prediction", None)

            if message:
                if prediction == 1:
                    #st.success(project_name)
                    st.balloons()
                    col1, col2 = st.columns([2,1])
                    with col1:
                        st.success(message)
                    with col2:
                        st.info(f"Probability of success:  \n" f"**{probability*100:.1f} %**")
                    st.markdown("##### Based on the following posted comments:")
                    for c in comments:
                        st.markdown(f"- {c}")

                else:
                    #st.error(project_name)
                    st.snow()
                    col1, col2 = st.columns([2,1])
                    with col1:
                        st.error(message)
                    with col2:
                        st.info("Probability of failure:  \n" f"**{probability*100:.1f} %**")
                    st.markdown("##### Based on the following posted comments:")
                    for c in comments:
                        st.markdown(f"- {c}")

            else:
                st.error("We are unable to retrieve a prediction for this project.")
        else:
            st.error("We are unable to retrieve a prediction for this project.")
