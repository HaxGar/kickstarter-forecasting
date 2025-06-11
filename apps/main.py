import kickstarter_predictor
import kickstarter_predictor.data as data
from kickstarter_predictor import train_test
import kickstarter_predictor.data
import kickstarter_predictor.registry
from kickstarter_predictor.predict import pred
from sklearn.model_selection import cross_validate
from sklearn.pipeline import make_pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import recall_score
from sklearn.model_selection import GridSearchCV
from scipy.stats import uniform, randint
import pandas as pd
import numpy as np
import langid

def preprocess_and_train(ngram = (1, 3), max_features = 10000, alpha=0.1, model_type = 'MultinomialNB_by_project') -> None:
    print('------Preprocess and train------')
    df = data.load_data(ligne_par_commentaire=False)
    X_train, y_train = train_test.load_or_create_split(file='train',df=df, balancing=True, ligne_par_commentaire=False)
    X_test, y_test = train_test.load_or_create_split(file='test',df=df, balancing=True, ligne_par_commentaire=False)

    pipeline_naive_bayes = make_pipeline(
        TfidfVectorizer(ngram_range=ngram, max_features=max_features),
        MultinomialNB(alpha=alpha)
    )

    pipeline_naive_bayes.fit(X_train, y_train)

    scores = pipeline_naive_bayes.score(X_test, y_test)

    kickstarter_predictor.registry.save_full_registry(model=pipeline_naive_bayes, model_type=model_type, params=pipeline_naive_bayes.get_params(), metrics=scores)
    return None

if __name__ == '__main__':
    try:
        preprocess_and_train()
        pred()
    except:
        import sys
        import traceback

        import ipdb
        extype, value, tb = sys.exc_info()
        traceback.print_exc()
        ipdb.post_mortem(tb)
