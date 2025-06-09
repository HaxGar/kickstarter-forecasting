from fastapi import FastAPI
from kickstarter_predictor.registry import load_model
from kickstarter_predictor.data import cleaning_sentence, load_merged_raw_data, load_live_projects_comments

app = FastAPI()
model_info = load_model()
model = model_info['model']

@app.get("/predict")
def predict_api(commentaires : str):

    # 1/ Charger les données + cleaning
        # à partir d'une url kickstarter > besoin de scrapper / pending Adrien/Anatole

        # à partir des datasets dispo > remonter les campagnes avec label = live + cleaning data
    df = load_live_projects_comments(ligne_par_commentaire=True)
    X_test = df['X']

    # 2/ Predict success or failure
    result = model.predict(X_test)
    result_proba = model.predict_proba(X_test)

    return {"Commentaires": commentaires, "result": result,
        "result_proba": result_proba
    }
