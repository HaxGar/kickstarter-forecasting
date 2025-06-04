import numpy as np
import kickstarter_predictor.data as data
import kickstarter_predictor.preprocess.nlp_preprocessing as nlp_preprocessing
from sklearn.model_selection import cross_validate
from sklearn.pipeline import make_pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import recall_score

cleaned_comments = data.load_merged_data(ligne_par_ligne=True)#.iloc[:10000]
X = cleaned_comments['X']
y = cleaned_comments['y']

preproc_X =  nlp_preprocessing.preprocessing(X,
                                             tokenized = True,
                                             removed_word = True,
                                             lemmatized=True)
# print(preproc_X)
pipeline_naive_bayes = make_pipeline(
    TfidfVectorizer(),
    MultinomialNB()
)

cv_results = cross_validate(pipeline_naive_bayes, preproc_X, y, cv = 5, scoring = ["recall"])
average_recall = cv_results["test_recall"].mean()
results = average_recall
print(results)
