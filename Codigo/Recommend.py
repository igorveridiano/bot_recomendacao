from imdb import IMDb

from Codigo.FunctionRecommend import recommend
from Codigo.Bot import new_model

imdb = IMDb()


def recommend(movie_title):
    imdb.update(movie_title, info=['plot'])
    text_ = ""

    if 'synopsis' in movie.keys():
        for synopsi in movie['synopsis']:
            text_ += synopsi + " "

    if 'plot' in movie.keys():
        for plot in movie['plot']:
            text_ += plot + " "

    synopse = text_

    matrix_test = new_model['vector'].transform(synopse)
    print(matrix_test)

    cluster = new_model['model'].predict(matrix_test)
    print("O filme pertence ao cluster %i" % cluster[0])

    frames = new_model['frame']

    movies = new_model['all_movies']

    ids_selected = list(frames[frames['cluster'] == cluster[0]]['id'])

    recommend_list_aux = []

    for id_ in ids_selected:
        simillarity = recommend(movies[id_], synopse)
        list = (movies[id_]['title'], simillarity)
        recommend_list_aux.insert(list)

    recommend_list_aux.sort(key=lambda x: x[1], reverse=True)
    recommend_list = []
    for x in range(0, 10):
        recommend_list.insert(recommend_list_aux[x][0])

    return recommend_list
