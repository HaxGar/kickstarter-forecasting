# !pip install -r requirements.txt
import pandas as pd

import string

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

from sklearn.feature_extraction.text import CountVectorizer

# debug :
import data

def cleaning(sentence):
    # Basic cleaning
    sentence = sentence.strip() ## remove whitespaces
    sentence = sentence.lower() ## lowercase
    sentence = ''.join(char for char in sentence if not char.isdigit()) ## remove numbers

    # Advanced cleaning
    for punctuation in string.punctuation:
        sentence = sentence.replace(punctuation, '') ## remove punctuation
    return sentence

def tokenize(sentence):
    tokenized_sentence = word_tokenize(sentence) ## tokenize
    return tokenized_sentence

def removing_words(tokenized_sentence):
    stop_words = set(stopwords.words('english')) ## define stopwords

    tokenized_sentence_cleaned = [ ## remove stopwords
        w for w in tokenized_sentence if not w in stop_words
    ]
    return tokenized_sentence_cleaned


def lemmatizing(tokenized_sentence_cleaned):
    lemmatized = [
        WordNetLemmatizer().lemmatize(word, pos = "v")
        for word in tokenized_sentence_cleaned
    ]
    return lemmatized

def preprocessing_sentence(comment: str)->str:

    sentence=cleaning(comment)
    tokenized_sentence=tokenize(sentence)
    tokenized_sentence_cleaned=removing_words(tokenized_sentence)
    lemmatized=lemmatizing(tokenized_sentence_cleaned)
    cleaned_sentence = ' '.join(word for word in lemmatized)

    return cleaned_sentence

def preprocessing(X: pd.DataFrame, ngram_range=(1,1)) -> pd.DataFrame :
    return X.apply(preprocessing_sentence)

def preprocessing_with_vectorization(X: pd.DataFrame, ngram_range=(1,1)) : #renvoi : scipy.sparse._csr.csr_matrix
    X_preproc =X.apply(preprocessing_sentence)
    # vectorization :
    count_vectorizer = CountVectorizer(ngram_range=ngram_range)
    X_preproc = count_vectorizer.fit_transform(X_preproc)
    #print(type(X_preproc))
    return X_preproc

# df=data.load_merged_data().iloc[:500]
# print(preprocessing_with_vectorization(df['X']))
