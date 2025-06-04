# !pip install -r requirements.txt
import pandas as pd

import string

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

from sklearn.feature_extraction.text import CountVectorizer


# debug :
import kickstarter_predictor.data as data

stop_words = set(stopwords.words('english')) ## define stopw
lemmatizer = WordNetLemmatizer()

# Nettoyage de la ponctuation, chiffres et mise en minuscule
def cleaning(sentence):

    '''
    Nettoie une phrase :
    - supprime les espaces en trop
    - met en minuscules
    - supprime les chiffres et la ponctuation
    '''
    # Basic cleaning
    sentence = sentence.strip() ## remove whitespaces
    sentence = sentence.lower() ## lowercase
    sentence = ''.join(char for char in sentence if not char.isdigit()) ## remove numbers

    # Advanced cleaning
    for punctuation in string.punctuation:
        sentence = sentence.replace(punctuation, '') ## remove punctuation
    return sentence

# Tokenisation simple (via nltk)
def tokenize(sentence):

    '''
    Tokenise une phrase en liste de mots
    '''
    tokenized_sentence = word_tokenize(sentence) ## tokenize
    return tokenized_sentence

# Suppression des stopwords anglais
def removing_words(tokenized_sentence):
    '''
    Supprime les stopwords de la phrase tokenisée
    '''

    tokenized_sentence_cleaned = [ ## remove stopwords
        w for w in tokenized_sentence if not w in stop_words
    ]
    return tokenized_sentence_cleaned

# Lemmatisation des mots (forme verbale)
def lemmatizing(tokenized_sentence_cleaned):
    '''
    Lemmatisation des mots (ex: "running" devient "run")
    '''
    return [lemmatizer.lemmatize(word, pos="v") for word in tokenized_sentence_cleaned]


# Fonction complète de nettoyage d'une phrase (pipeline)
def preprocessing_sentence(comment: str ,
                           tokenized: bool=True,
                           removed_word:bool=True,
                           lemmatized:bool=True)->str:
    '''
    Applique les étapes NLP à une phrase :
    - nettoyage
    - tokenisation (optionnelle)
    - suppression des stopwords (optionnelle)
    - lemmatisation (optionnelle)
    Retourne la phrase nettoyée sous forme de string.
    '''
    clean_word=cleaning(comment)

    if tokenized:
        clean_word=tokenize(clean_word)

    if removed_word:
        clean_word=removing_words(clean_word)

    if lemmatized:
        clean_word=lemmatizing(clean_word)

    #assurer de retourner une string
    if isinstance(clean_word, list):
        return ' '.join(word for word in clean_word)
    else:
        return clean_word

# Applique preprocessing_phrase à chaque ligne d'un DataFrame
def preprocessing(X: pd.DataFrame,
                  ngram_range=(1,1),
                  tokenized: bool = True,
                  removed_word: bool = True,
                  lemmatized: bool = True
                  ) -> pd.DataFrame :
    '''
    Applique le prétraitement NLP (sans vectorisation) à chaque ligne d’un DataFrame.
    Retourne une colonne contenant les phrases nettoyées.
    '''
    return X.apply(preprocessing_sentence,tokenized=tokenized,removed_word=removed_word,lemmatized=lemmatized)

# Applique preprocessing + vectorisation avec CountVectorizer
def preprocessing_with_vectorization(X: pd.DataFrame, ngram_range=(1,1)) : #renvoi : scipy.sparse._csr.csr_matrix
    '''
    Applique le prétraitement NLP puis vectorise les phrases avec CountVectorizer.
    Retourne une matrice creuse (sparse matrix) de type csr_matrix.
    '''
    X_preproc =X.apply(preprocessing_sentence)
    # vectorization :
    count_vectorizer = CountVectorizer(ngram_range=ngram_range)
    X_preproc = count_vectorizer.fit_transform(X_preproc)
    #print(type(X_preproc))
    return X_preproc

# df=data.load_merged_data().iloc[:500]
# print(preprocessing_with_vectorization(df['X']))
