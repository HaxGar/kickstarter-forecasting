from fastapi import FastAPI

from kickstarter_predictor.predict import pred
#import numpy as np

from kickstarter_predictor.registry import *
from kickstarter_predictor.preprocess_ML import *
from kickstarter_predictor.data import *
from kickstarter_predictor.scraper import scrape_kickstarter_url

app = FastAPI()

# Load model when launching the API
model_name = '20250610-101116_MultinomialNB_by_project.pkl'
model_info = load_model(model_name=model_name)
model = model_info['model']


@app.get("/predict_par_titre")
def predict_par_titre(titre_du_projet : str = 'The REEL THING - Fishing Gun / Grab Your Gun and GO!!!') -> dict :
    # p. e. : 'The REEL THING - Fishing Gun / Grab Your Gun and GO!!!'
    # on pourrait le faire avec index du projet aussi

    # 1/a Load data from kickstarter url
        # besoin de scrapper / pending Adrien-Anatole

    # 1/b Load and preprocess data for live campaign
    df = load_data_by_project_title(titre_du_projet)

    # 2/ Predict
    result = pred(df, model_name=model_name)
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
        "Name of your project" : df['name'][0],
        "Our prediction": message,
        "Based on the following posted comments" : [c for c in df['commentaires'][0]],
        "Prediction": int(y_pred),
        probability_key: probability
    }


@app.get("/predict_par_id")
def predict_par_id(id_projet : str = '1376423') -> dict :
    #p.e.: id_projet = 1376423
    id_projet = int(id_projet)
    # 1/a Load data from kickstarter url
        # besoin de scrapper / pending Adrien-Anatole

    # 1/b Load and preprocess data for live campaign
    df = load_data_by_project_id(id_projet)

    # 2/ Predict
    result = pred(df, model_name=model_name)
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
        "project_name" : df['name'][0],
        "message": message,
        "comments" : [c for c in df['commentaires'][0]],
        "prediction": int(y_pred),
        "probability_key": probability
    }

@app.get("/predict_by_url")
def predict_by_url(url: str) -> dict:
    dataframe_comments, user_comments = scrape_kickstarter_url(
        url
        # "https://www.kickstarter.com/projects/zafirro/zafirro-sapphire-blade-razor"                                                                           # FAIL
        # "https://www.kickstarter.com/projects/hozodesign/neoblade?ref=discovery_category&total_hits=54753&category_id=334"                                    # SUCCESS
        # "https://www.kickstarter.com/projects/ohdoki/the-handy-2-the-1-male-sex-toy-now-even-better?ref=discovery_category&total_hits=54753&category_id=52"   # SUCCESS
    )

    prepreocessed_project = preprocess(dataframe_comments)

    result = pred(prepreocessed_project, "20250610-101116_MultinomialNB_by_project.pkl")

      # Aggregate results
    y_pred = result['y_pred']
    y_pred_proba = result['y_pred_proba']

    if y_pred == 1:
        message = "🎉 Your Kickstarter project is likely to SUCCEED!"
        probability = round(float(y_pred_proba), 4)
    else:
        message = "⚠️ Unfortunaltely, your Kickstarter project is likely to FAIL."
        probability = round(float(y_pred_proba), 4)

    return {
        "project_name" : "Named is not scraped yet",
        "message": message,
        "comments" : user_comments,
        "prediction": int(y_pred),
        "probability_key": probability
    }