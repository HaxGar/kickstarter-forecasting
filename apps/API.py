from fastapi import FastAPI
from kickstarter_predictor.registry import load_model
from sklearn.model_selection import train_test_split
from kickstarter_predictor.train_test import load_or_create_split
from kickstarter_predictor.data import cleaning_sentence

app = FastAPI()
# model = load_model() # à ajouter lorsque que le modèle sera live

@app.get("/predict")
def predict_api(kickstarterurl : str, comment_type : str):

    # charger les données à partir d'une url kickstarter
    X_test, y_test = load_or_create_split(file='test')

    # preprocesser la donnée
    clean_test = cleaning_sentence(X_test.head(1))


    # predict success or failure
    # result = model.predict(clean_test)

    return {"Hello": kickstarterurl, "result": {
        "status" : "success",
        "score de confiance" : 0.6
    }}
