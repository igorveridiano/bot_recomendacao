# -*- coding: utf-8 -*-
"""Cluster para o bot.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1wo-dkD_hgpOrezK4PTgWxCtTSkuBrAwq
"""
from imdb import IMDb
import pandas as pd
import nltk
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from nltk.stem.snowball import SnowballStemmer
from sklearn.externals import joblib
import pickle

nltk.download('stopwords')
nltk.download('punkt')

imdb = IMDb()

top250 = imdb.get_top250_movies()

all_movies = {}
count = 0
for movie in top250:
    imdb.update(movie, info=['plot'])
    all_movies[count] = movie
    count += 1

movie_database = []
count = 0
for m in all_movies:
    movie_instance = {}
    movie = all_movies[m]
    movie_instance['id'] = m
    movie_instance['movie'] = movie['title']
    movie_instance['year'] = movie['year']

    text_ = ""

    if 'synopsis' in movie.keys():
        for synopsi in movie['synopsis']:
            text_ += synopsi + " "

    if 'plot' in movie.keys():
        for plot in movie['plot']:
            text_ += plot + " "

    movie_instance['text'] = text_

    movie_database.append(movie_instance)

ids = []
titles = []
synopsis = []
for movie in movie_database:
    ids.append(movie['id'])
    titles.append(movie['movie'])
    synopsis.append(movie['text'])

stopwords = nltk.corpus.stopwords.words('english')

stemmer = SnowballStemmer("english")


# here I define a tokenizer and stemmer which returns the set of stems in the text that it is passed

def tokenize_and_stem(text):
    # first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
    tokens = [word for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    filtered_tokens = []
    # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
    for token in tokens:
        if re.search('[a-zA-Z]', token):
            filtered_tokens.append(token)
    stems = [stemmer.stem(t) for t in filtered_tokens]
    return stems


def tokenize_only(text):
    # first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
    tokens = [word.lower() for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    filtered_tokens = []
    # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
    for token in tokens:
        if re.search('[a-zA-Z]', token):
            filtered_tokens.append(token)
    return filtered_tokens


totalvocab_stemmed = []
totalvocab_tokenized = []

for text in synopsis:
    allwords_stemmed = tokenize_and_stem(text)
    totalvocab_stemmed.extend(allwords_stemmed)

    allwords_tokenized = tokenize_only(text)
    totalvocab_tokenized.extend(allwords_tokenized)

vocab_frame = pd.DataFrame({'words': totalvocab_tokenized}, index=totalvocab_stemmed)

# define vectorizer parameters
tfidf_vectorizer = TfidfVectorizer(max_df=0.8, max_features=200000,
                                   min_df=0.2, stop_words='english',
                                   use_idf=True, tokenizer=tokenize_and_stem, ngram_range=(1, 3))

tfidf_matrix = tfidf_vectorizer.fit_transform(synopsis)

num_clusters = 5

km = KMeans(n_clusters=num_clusters)

km.fit(tfidf_matrix)

clusters = km.labels_.tolist()

films = {'title': titles, 'synopsis': synopsis, 'cluster': clusters, 'id': ids}

frame = pd.DataFrame(films, index=[clusters], columns=['title', 'cluster', 'id'])

model_persist = {
    'model': km,
    'vector': tfidf_vectorizer,
    'movie_database': movie_database,
    'all_movies': all_movies,
    'frame': frame,
}

joblib.dump(model_persist, 'model.pkl')

pickle.dumps(tokenize_and_stem)