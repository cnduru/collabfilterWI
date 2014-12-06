import math
import pickle
import numpy as np
import random
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

    return 1 / N * rating, N


def user_means():
    global users

    r_sum = 0
    for user in users:
        r_sum += users[user].avg_ratings()
    res = r_sum / float(len(users))
    return res


def movie_means():
    global movies

    r_sum = 0
    for movie in movies:
        r_sum += movies[movie].get_rating()
    res = r_sum / float(len(movies))
    return res


def train(K=10):
    global movies, users
    # initilize
    random.seed()
    A = np.array([0.1] * len(users) * K).reshape((len(users), K))
    B = np.array([0.1] * len(movies) * K).reshape(K, (len(movies)))
    eta = 0.001

    for k in range(K):
        for _ in range(1000):#until convergiance
            mov = movies[random.randint(1, len(movies) - 1)]
            usr = users[random.choice(list(mov.user_ratings.keys()))]
            Rmu = mov.user_ratings[usr.u_id]
            #calc
            A[mov.m_id, k] += eta * (Rmu - A[mov.m_id, :].dot(B[:, usr.num])) * B[k, usr.num]
            B[k, usr.num] += eta * A[mov.m_id, k] * (Rmu - A[mov.m_id, :].dot(B[:, usr.num]))
    g = 0




def pre_pro(m, u, mum):
    return 0 - m - u + mum


def zero_test(mum):
    global movies, users
    pp_all_ratings = []
    for mov in movies.values():
        for u_id, rating in mov.user_ratings.items():
            pp_all_ratings.append(rating - mov.get_rating() - users[u_id].avg_ratings() + mum)
    return sum(pp_all_ratings)


load_movies()
load_users()
a3 = user_means()
a4 = movie_means()
a5, n = movie_user_mean()
#train()
a6 = zero_test(a5)
a = 1