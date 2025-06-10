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


@app.get("/predict")
def predict_api(commentaires : str):

    # 1/a Load data from kickstarter url
        # besoin de scrapper / pending Adrien-Anatole

    # 1/b Load and preprocess data for live campaign
    df = load_live_projects_comments(ligne_par_commentaire=False)

    # 2/ Predict
    result = main.pred(df=df.head(1), model_name=model_name)

    # Aggregate results
    y_pred = result['y_pred']
    y_pred_proba = result['y_pred_proba']

    message = (
    "🎉 Your Kickstarter project is likely to SUCCEED!"
    if y_pred == 1
    else "⚠️ Your Kickstarter project is likely to FAIL."
    )

    return {
    "prediction": int(y_pred),
    "probability_of_success": round(float(y_pred_proba), 4),
    "message": message
    }
