import string
import re
import langid
import pandas as pd

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

stop_words = set(stopwords.words('english')) ## define stopw
lemmatizer = WordNetLemmatizer()

def basic_cleaning(sentence:str)->str:
    '''
    Supprime les espaces en trop et met tout en minuscules
    '''
    sentence = sentence.strip() ## remove whitespaces
    sentence = sentence.lower() ## lowercasesentence = ''.join(char for char in sentence if not char.isdigit()) ## remove numbers
    return sentence

## cleaning options :
def removing_ponctuation(sentence:str)->str:
    '''
    Supprime les chiffres et la ponctuation
    '''
    for punctuation in string.punctuation:
        sentence = sentence.replace(punctuation, '') ## remove punctuation
    # Sépare en mots
    words = sentence.split()
    # Garde seulement les mots alphanumériques (lettres et chiffres)
    cleaned_words = [w for w in words if re.fullmatch(r'[a-zA-Z0-9]+', w)] # re.fullmatch(r'[a-zA-ZÀ-ÿ0-9]+', w) si on veut garder accents etc...
    return ' '.join(cleaned_words)

def removing_stop_words(tokenized_sentence:list)->list:
    '''
    Supprime les stopwords et les mots qui ne sont pas composés uniquement de lettres et chiffres.
    '''
    return [
        w for w in tokenized_sentence if (w not in stop_words)
    ]

def lemmatizing(tokenized_sentence_cleaned:list)->list:
    '''
    Lemmatisation des mots d'abord comme verbes, puis comme noms
    '''
    # Étape 1 : lemmatisation comme verbes
    verb_lemmatized = [
        lemmatizer.lemmatize(word, pos="v")
        for word in tokenized_sentence_cleaned
    ]
    # Étape 2 : lemmatisation comme noms
    noun_lemmatized = [
        lemmatizer.lemmatize(word, pos="n")
        for word in verb_lemmatized
    ]
    return noun_lemmatized

def cleaning_sentence(
    comment: str,
    remove_ponctuation:bool=True,
    remove_stop_words:bool=True,
    lemmatize:bool=True,
    keep_only_english = True
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

def remove_not_English(df:pd.DataFrame)->pd.DataFrame:
    # Filtre par langue English
    print(f"🔄 Début du nettoyage des {len(df)} commentaires uniques...")
    print(f"...cela peut prendre quelque minutes...")
    _before = len(df)
    df = df[df['commentaires'].apply(lambda c: langid.classify(c)[0] == 'en')]
    print(f"❌ {_before - len(df)} commentaires supprimés car not English")
    return df

def preprocess(df:pd.DataFrame, remove_not_english=True)->pd.DataFrame :
    # enlève des commentaires pas anglais
    if remove_not_english :
        df = remove_not_English(df)
    # nettoie les features (possible d'optimiser par params)
    df.loc[:, 'X'] = df['commentaires'].apply(cleaning_sentence)

    _before = len(df)
    df = df.dropna(subset=['X'])
    print(f"❌ {_before - len(df)} commentaires vides supprimés")
    return df

def preprocess_projet(projet:pd.DataFrame)->pd.DataFrame :
# explode pour faire le preprocess par ligne
    commentaires = projet.explode('commentaires').reset_index(drop=True)
    # preprocess
    preproc = preprocess(commentaires)
    # regroup les commentaires par projet
    preproc_projet = (
        preproc
        .groupby(['id'])['X']
        .agg(' '.join)
        .reset_index()
    )
    return projet.merge(preproc_projet)
