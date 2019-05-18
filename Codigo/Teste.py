from imdb import IMDb

imdb = IMDb()

movies = imdb.search_movie('The Godfather')
list_movies = {}
x = 1
if movies.__len__() > 0:
    for movie_aux1 in movies:
        list_movies.update({x: movie_aux1['title']})
        x += 1
if list_movies.__len__() > 0:
    message = ''
    for y in range(1, list_movies.__len__() + 1):
        message += str(y) + '-' + list_movies[y] + '\n'

    print(message)
