
# !pip install nltk

# 1 - DATA MANIPULATION
import pandas as pd

# 2 - DATA VISUALISATION
import matplotlib.pyplot as plt

import string

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

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

def preprocessing(sentence):
    sentence=cleaning(sentence)
    tokenized_sentence=tokenize(sentence)
    tokenized_sentence_cleaned=removing_words(tokenized_sentence)
    lemmatized=lemmatizing(tokenized_sentence_cleaned)
    cleaned_sentence = ' '.join(word for word in lemmatized)

    return cleaned_sentence

# df['cleaned_comment'] = df['comments'].apply(preprocessing)
# df[['comments', 'cleaned_comment']].head()
