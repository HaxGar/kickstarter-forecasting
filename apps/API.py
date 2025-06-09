from fastapi import FastAPI
from kickstarter_predictor.registry import load_model
from kickstarter_predictor.data import cleaning_sentence, load_merged_raw_data, load_live_projects_comments

app = FastAPI()
# model = load_model() # à ajouter lorsque que le modèle sera live

@app.get("/predict")
def predict_api(kickstarterurl : str, comment_type : str):

    # 1/ Charger les données + cleaning
        # à partir d'une url kickstarter > besoin de scrapper / pending Adrien

        # à partir des datasets dispo > remonter les campagnes avec label = live + cleaning data
    df = load_live_projects_comments(ligne_par_commentaire=True)
    X_test = df['X']

    # 2/ Predict success or failure
    # result = model.predict(clean_test)

    return {"Hello": kickstarterurl, "result": {
        "status" : "success",
        "score de confiance" : 0.6
    }}
