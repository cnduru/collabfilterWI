import math
import pickle
from movie import Movie
from user import User

movies = {}
users = {}
movie_mean = 0
user_mean = 0

def load_movies():
    global movies

    try:
        with open('training.pickle', 'rb') as handle:
            movies = pickle.load(handle)
    except:
        print('Load the movies first, dumbass!')

def load_users():
    global movies, users

    for movie in movies:
        for user in movies[movie].user_ratings:
            if user not in users:
                users[user] = User(user)

            users[user].add_rating(movies[movie].m_id, movies[movie].user_ratings[user])

def movie_user_mean():
    global movies
    N = 0
    rating = 0

    for key in movies:
        N += len(movies[key].user_ratings)
        for user in movies[key].user_ratings:
            rating += movies[key].user_ratings[user]

    return 1/N*rating

def user_mean():
    global users

    sum = 0
    for user in users:
        sum += users[user].avg_ratings()
    user_mean = sum / float(len(users))
    return user_mean

def movie_mean():
    global movies

    sum = 0
    for movie in movies:
        sum += movies[movie].get_rating()
    movie_mean = sum / float(len(movies))
    return movie_mean

def zero_test():
    pass


#def preprocess():
