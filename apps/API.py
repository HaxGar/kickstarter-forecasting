from fastapi import FastAPI
from kickstarter_predictor.registry import load_model
from kickstarter_predictor.data import load_live_projects_comments
from apps import main
import numpy as np

app = FastAPI()

# Load model when launching the API
model_name = '20250610-101116_MultinomialNB_by_project.pkl'
model_info = load_model(model_name=model_name)
model = model_info['model']


<<<<<<< HEAD
@app.get("/predict")
def predict_api(commentaires : str):
=======
@app.get("/predict_par_titre")
def predict_par_titre(titre_du_projet : str = 'The REEL THING - Fishing Gun / Grab Your Gun and GO!!!') -> dict :
    # p. e. : 'The REEL THING - Fishing Gun / Grab Your Gun and GO!!!'
    # on pourrait le faire avec index du projet aussi
>>>>>>> ea8aa85 (valeurs par défault pour titre et id)

    # 1/a Load data from kickstarter url
        # besoin de scrapper / pending Adrien-Anatole

    # 1/b Load and preprocess data for live campaign
    df = load_live_projects_comments(ligne_par_commentaire=False)

    # 2/ Predict
    result = main.pred(df=df.head(1), model_name=model_name)

    # Aggregate results
  # Aggregate results
    y_pred = result['y_pred']
    y_pred_proba = result['y_pred_proba']

    if y_pred == 1:
        message = "🎉 Your Kickstarter project is likely to SUCCEED!"
        probability = round(float(y_pred_proba), 4)
        probability_key = "probability_of_success"
    else:
        message = "⚠️ Unfortunaltely, your Kickstarter project is likely to FAIL."
        probability = round(float(y_pred_proba), 4)
        probability_key = "probability_of_failure"

    return {
        "Name of your project" : df['name'].head(1),
        "Our prediction": message,
        "based on the following posted comments" : "\n".join(df['X'].head(1).tolist()),
        "prediction": int(y_pred),
        probability_key: probability
    }
<<<<<<< HEAD
=======
    print(dd)

    return dd


@app.get("/predict_par_id")
def predict_par_id(id_projet : str = '1376423') -> dict :
    #p.e.: id_projet = 1376423
    id_projet = int(id_projet)
    # 1/a Load data from kickstarter url
        # besoin de scrapper / pending Adrien-Anatole

    # 1/b Load and preprocess data for live campaign
    df = load_data_by_project_id(id_projet)

    # 2/ Predict
    result = main.pred(df, model_name=model_name)
  # Aggregate results
    y_pred = result['y_pred']
    y_pred_proba = result['y_pred_proba']

    if y_pred == 1:
        message = "🎉 Your Kickstarter project is likely to SUCCEED!"
        probability = round(float(y_pred_proba), 4)
        probability_key = "probability_of_success"
    else:
        message = "⚠️ Unfortunaltely, your Kickstarter project is likely to FAIL."
        probability = round(float(y_pred_proba), 4)
        probability_key = "probability_of_failure"

    dd = {
        "Name of your project" : df['name'],
        "Our prediction": message,
        "based on the following posted comments" : "\n".join(df['X'].tolist()),
        "prediction": int(y_pred),
        probability_key: probability
    }
    print(dd)

    return dd
>>>>>>> ea8aa85 (valeurs par défault pour titre et id)
