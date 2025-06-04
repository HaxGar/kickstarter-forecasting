import pandas as pd
import ast

from pathlib import Path

from kickstarter_predictor.params import *

#cleaning
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

## private properties
stop_words = set(stopwords.words('english')) ## define stopw
lemmatizer = WordNetLemmatizer()

## row data, private funcions :
def load_raw_projects(filterLive=True)->pd.DataFrame:
    '''
    read the raw csv of projects
    without state=='live' if filterLive=True,
    prepare for the merge ('ID' renamed to 'id')
    '''
    path = Path(LOCAL_DATA_PATH).joinpath('raw', "ks-projects-201801.csv")
    df_projects = pd.read_csv(path)
    df_projects.rename(columns={'ID':'id'}, inplace=True)
    if filterLive :
        df_projects = df_projects[df_projects['state']!='live']
        df_projects['state'] = df_projects['state'].apply(lambda x: 1 if x == 'successful' else 0)

    return df_projects

def load_raw_commentaires()->pd.DataFrame:
    '''
    read the raw csv of comments
    by filtering out the empty coments
    '''
    path = Path(LOCAL_DATA_PATH).joinpath('raw', "comments_clean.csv")
    df_comments = pd.read_csv(path)
    df_comments = df_comments[df_comments['comments']!='[]']
    # cast string as py list
    df_comments['commentaires'] = df_comments['comments'].apply(ast.literal_eval)
    df_comments.drop(columns=['comments'], inplace=True)

    return df_comments

def load_merged_raw_data(ligne_par_ligne:bool)->pd.DataFrame:
    '''
    merge the two df : comments and projects
    ligne par ligne si ligne_par_ligne==True,
    sinon par projet
    '''
    df_comments = load_raw_commentaires()
    df_projects = load_raw_projects()

    df_merged = (
        df_comments.merge(
            df_projects[['id', 'state']]
        )
    )

    if ligne_par_ligne :
        df_merged = df_merged.explode('commentaires').reset_index(drop=True)
    else :
        df_merged['commentaires'] = df_merged['commentaires'].apply(
            lambda x: '; '.join(x)
        )

    return df_merged.rename(columns={"commentaires": "X", 'state':'y'})

def basic_cleaning(sentence:str)->str:
    '''
    Nettoie une phrase :
    - supprime les espaces en trop
    - met en minuscules
    - supprime les chiffres et la ponctuation
    '''
    sentence = sentence.strip() ## remove whitespaces
    sentence = sentence.lower() ## lowercase
    sentence = ''.join(char for char in sentence if not char.isdigit()) ## remove numbers
    return sentence

## cleaning options :
def removing_ponctuation(sentence:str)->str:
    for punctuation in string.punctuation:
        sentence = sentence.replace(punctuation, '') ## remove punctuation
    return sentence

def removing_stop_words(tokenized_sentence:list)->list:
    return [w for w in tokenized_sentence if not w in stop_words]

def lemmatizing(tokenized_sentence_cleaned:list)->list:
    return [lemmatizer.lemmatize(word, pos="v") for word in tokenized_sentence_cleaned]

def cleaning_sentence(
    comment: str,
    remove_ponctuation:bool=True,
    remove_stop_words:bool=True,
    lemmatize:bool=True
)->str:
    '''
    Applique les étapes NLP à une phrase :
    - nettoyage : supprime les espaces et les chiffres, met en minuscules
    - suppression des ponctuation (optionnelle)
    - suppression des stopwords (optionnelle)
    - lemmatisation (optionnelle) (ex: "running" devient "run")
    Retourne la phrase nettoyée sous forme de string.
    '''
    clean_word = basic_cleaning(comment)

    if remove_ponctuation:
        clean_word=removing_ponctuation(clean_word)

    clean_word = word_tokenize(clean_word)
    if remove_stop_words:
        clean_word=removing_stop_words(clean_word)

    if lemmatize:
        clean_word=lemmatizing(clean_word)

    if isinstance(clean_word, list):
        return ' '.join(word for word in clean_word)
    else:
        return clean_word
    return clean_word

## callable functions
def load_data(
    ligne_par_ligne: bool = True,
    remove_ponctuation: bool = True,
    remove_stop_words: bool = True,
    lemmatize: bool = True
)->pd.DataFrame:
    '''
    load merged data from cache ou de raw selon 2 scénarios possible :
        - une ligne par chaque commentaire si ligne_par_ligne==True
        - une ligne par projet avec les commentaires regroupés si ligne_par_ligne==False,
    le nettoie selon 2 paramètres :
        - avec ou sans ponctuation (remove_ponctuation: True || False)
        - avec ou sans stop words (remove_stop_words: True || False)
        - avec ou sans lemmatization (lemmatize: True || False)
    '''
    #1) load merged data from cache ou de raw
    if ligne_par_ligne : scenario = 'par_projet'
    else : scenario = 'par_commentaire'

    filename = 'merged_data'

    # ponctuation
    if remove_ponctuation : filename += '_sans_ponctuation'

    # stop words
    if remove_stop_words : filename += '_sans_stop_words'

    # lemmatized
    if remove_stop_words : filename += "_lemmatized"

    filename += ".csv"
    cache_path = Path(LOCAL_DATA_PATH).joinpath('processed', scenario, filename)

    if cache_path.is_file():
        df = pd.read_csv(cache_path)
    else :
        df = load_merged_raw_data(ligne_par_ligne)
        # cleaning :
        df['X'] = df['X'].apply(
            cleaning_sentence,
            remove_ponctuation=remove_ponctuation,
            remove_stop_words=remove_stop_words,
            lemmatize=lemmatize
        )

        df.to_csv(cache_path)

    return df
