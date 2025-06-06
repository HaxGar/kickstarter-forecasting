import kickstarter_predictor.data as data
from sklearn.model_selection import cross_validate
from sklearn.pipeline import make_pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import recall_score
import langid

cleaned_comments = data.load_data(
    # ligne_par_ligne=True,
    # remove_ponctuation=True,
    # remove_stop_words=True,
    # lemmatize=True
)#.iloc[:10000]
X = cleaned_comments['X']
y = cleaned_comments['y']


pipeline_naive_bayes = make_pipeline(
    TfidfVectorizer(),
    MultinomialNB()
)

cv_results = cross_validate(
    pipeline_naive_bayes, X, y, cv = 5,
    #scoring = ["recall"]
)
# average_recall = cv_results["test_recall"].mean()
# results = average_recall
print(cv_results)
