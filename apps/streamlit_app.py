import datetime as dt
import streamlit as st
import requests
import pandas as pd


st.title("KickPredict")

# Boolean variable to control the display of "Prediction from project information" tab
show_info_prediction_tab = False  # Set to True to reactivate this tab

# Options for the sidebar menu
#sidebar_options = [
    #"Select a project",
    #"Enter a URL"
#]

# mode = st.sidebar.radio(
    #"Choose an option",
    #tuple(sidebar_options)
#)

#if mode == "Select a project":
    #st.header("Project Selection")

# Sample projects dictionary
sample_projects = {
    "1": {
        "id": "1153426630",
        "name": "GUITAR-JO 2.0 - Make Your Electric Guitar",
        "url": "https://www.kickstarter.com/projects/sample/tech-project-1"
    },
    "2": {
        "id": "1053513419",
        "name": "Charggee: A New Way to Charge",
        "url": "https://www.kickstarter.com/projects/1740700612/charggee-a-new-way-to-charge-protect-your-mobile-d"
    },
    "3": {
        "id": "100411349",
        "name": "E Coin Mining and Rig-Building Workshop",
        "url": "https://www.kickstarter.com/projects/1079598152/e-coin-mining-and-rig-building-workshop/posts"
    },
    "4": {
        "id": "1073099678",
        "name": "Pill Swallowing Device",
        "url": "https://www.kickstarter.com/projects/1301067747/pill-swallowing-device/comments"
    },
}

st.markdown("Predict your likely Kickstarter project success or failure based on comments posted by backers.")

# Sélection du projet par son alias
choix = st.selectbox(
    "choose a project",
    options=list(sample_projects.keys()),
    format_func=lambda x: sample_projects[x]["name"]  # affiche le “name” dans la liste
)

st.info(sample_projects[choix]["url"])

if st.button("Lancer la requête"):

    # Récupération de l’ID correspondant
    id_projet = sample_projects[choix]["id"]

    params = {
                "id_projet": id_projet
            }

    response = requests.get("https://kickstarter-api-195095770000.europe-west1.run.app/predict_par_id", params=params)
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
                st.success(message)
                st.info(f"Probability of success: **{probability*100:.1f} %**")

                #st.info(f"based on the following posted comments: {comments}")
                st.markdown("### Commentaires")
                for c in comments:
                    st.markdown(f"- {c}")

            else:
                #st.error(project_name)
                st.snow()
                st.error(message)
                st.info(f"Probability of failure: **{probability*100:.1f} %**")
                st.info(sample_projects[choix]["url"])
                #st.info(f"based on the following posted comments: {comments}")
                st.markdown("### Commentaires")
                for c in comments:
                    st.markdown(f"- {c}")

        else:
            st.error("We are unable to retrieve a prediction for this project")


# Sample projects dictionary


#     # Project selection
# selected_project = st.selectbox(
# "Select a project",
# options=list(sample_projects.keys())
# )

# if selected_project:
# # Display project info
# project_data = sample_projects[selected_project]

# # Project name
# st.subheader("Project Name")
# st.write(project_data['name'])

# # Project URL
# st.subheader("Project URL")
# st.write(project_data['url'])

# # Comments list
# st.subheader("Comments")
# with st.expander("View comments", expanded=True):
#     # Simulate multiple comments
#     comments = [
#         {"text": "I love this project! The campaign is well structured.", "sentiment": "positive"},
#         {"text": "I'm disappointed by the lack of details about delivery times.", "sentiment": "negative"},
#         {"text": "Do you ship internationally?", "sentiment": "neutral"},
#         {"text": "Great innovation, I can't wait to receive my copy.", "sentiment": "positive"},
#         {"text": "I don't really understand how this product works.", "sentiment": "neutral"}
#     ]

#     for i, comment in enumerate(comments):
#         if comment["sentiment"] == "positive":
#             st.success(comment["text"])
#         elif comment["sentiment"] == "negative":
#             st.error(comment["text"])
#         else:
#             st.info(comment["text"])

# # Predicted state and probability
# st.subheader("Prediction")
# col1, col2 = st.columns(2)

# # Simulate a predicted state based on the actual project state for demonstration
# predicted_state = "Success" if project_data["state"] == "success" else "Failure"
# probability = 0.87 if project_data["state"] == "success" else 0.73

# with col1:
#     st.metric("Predicted State", predicted_state)
# with col2:
#     st.metric("Probability", f"{probability*100:.1f}%")

# # Informative message
# st.info("Note: Predictions are simulated. Real predictions will be available when the API is integrated.")

# elif mode == "Enter a URL":
# st.header("Analysis from URL")

# # URL input field
# url = st.text_input("Kickstarter project URL")

# if st.button("Analyze this project"):
# if not url:
#     st.warning("Please enter a URL")
# else:
#     # Simulate loading
#     with st.spinner("Analysis in progress..."):
#         # Simulated project name
#         project_name = "Demo project via URL"

#         # Display project info
#         # Project name
#         st.subheader("Project Name")
#         st.write(project_name)

#         # Project URL
#         st.subheader("Project URL")
#         st.write(url)

#         # Comments list
#         st.subheader("Comments")
#         with st.expander("View comments", expanded=True):
#             # Simulate multiple comments
#             comments = [
#                 {"text": "This project looks promising!", "sentiment": "positive"},
#                 {"text": "I'm concerned about the team's experience.", "sentiment": "negative"},
#                 {"text": "When is the delivery date?", "sentiment": "neutral"}
#             ]

#             for i, comment in enumerate(comments):
#                 if comment["sentiment"] == "positive":
#                     st.success(comment["text"])
#                 elif comment["sentiment"] == "negative":
#                     st.error(comment["text"])
#                 else:
#                     st.info(comment["text"])

#         # Predicted state and probability
#         st.subheader("Prediction")
#         col1, col2 = st.columns(2)

#         # Simulate the predicted state for demonstration
#         import random
#         predicted_state = random.choice(["Success", "Failure"])
#         probability = random.uniform(0.6, 0.9)

#         with col1:
#             st.metric("Predicted State", predicted_state)
#         with col2:
#             st.metric("Probability", f"{probability*100:.1f}%")

#         # Informative message
#         st.info("Note: Predictions are simulated. Real predictions will be available when the API is integrated.")
