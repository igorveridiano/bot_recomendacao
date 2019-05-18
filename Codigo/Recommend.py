import pickle

from imdb import IMDb

from Codigo.FunctionRecommend import recommender
from sklearn.externals import joblib

imdb = IMDb()

new_model = joblib.load('model.pkl')


def recommend(movie_title):
    imdb.update(movie_title, info=['plot'])
    text_ = ""

    if 'synopsis' in movie_title.keys():
        for synopsi in movie_title['synopsis']:
            text_ += synopsi + " "

    if 'plot' in movie_title.keys():
        for plot in movie_title['plot']:
            text_ += plot + " "

    synopse = text_

    synopsis = []

    synopsis.append(synopse)

    matrix_test = new_model['vector'].transform(synopsis)

    cluster = new_model['model'].predict(matrix_test)

    frames = new_model['frame']

    movies = new_model['movie_database']

    ids_selected = frames[frames['cluster'] == cluster[0]]['id']

    recommend_list_aux = []

    for id_ in ids_selected:
        for movie in movies:
            if movie['id'] == id_:
                if movie['movie'] != movie_title:
                    simillarity = recommender(movie, synopse)
                    list = (movie['movie'], simillarity)
                    recommend_list_aux.append(list)

    recommend_list_aux.sort(key=lambda x: x[1], reverse=True)
    recommend_list = []
    for x in range(0, 10):
        if x < recommend_list_aux.__len__():
            recommend_list.append(recommend_list_aux[x][0])

    return recommend_list
