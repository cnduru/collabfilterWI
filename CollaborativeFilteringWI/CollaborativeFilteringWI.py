import math
import pickle
import numpy as np
import random
from movie import Movie
from user import User
from progressTrack import Progress

movies = {}
users = {}
probe_movies = {}
movie_mean = 0
user_mean = 0


def load_movies():
    global movies

    try:
        with open('training.pickle', 'rb') as handle:
            movies = pickle.load(handle)
    except:
        print('Load the movies first, dumbass!')

def load_probes():
    global probe_movies

    try:
        with open('probe.pickle', 'rb') as handle:
            probe_movies = pickle.load(handle)
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

    return 1 / N * rating


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

def train(K=10, i=1000):
    global movies, users
    # initilize
    random.seed()
    A = np.array([0.1] * len(users) * K).reshape((len(users), K))
    B = np.array([0.1] * len(movies) * K).reshape(K, (len(movies)))
    eta = 0.001
    mum = movie_user_mean()


    p = Progress(i*K, "training")
    for k in range(K):
        for count in range(i):#until convergence
            mov = movies[random.randint(1, len(movies) - 1)]
            usr = users[random.choice(list(mov.user_ratings.keys()))]
            Rmu = mov.user_ratings[usr.u_id] - mov.get_rating() - usr.avg_ratings() + mum
            #calc
            A[mov.m_id, k] += eta * (Rmu - A[mov.m_id, :].dot(B[:, usr.num])) * B[k, usr.num]
            B[k, usr.num] += eta * A[mov.m_id, k] * (Rmu - A[mov.m_id, :].dot(B[:, usr.num]))
            p.percent(count*k)
    return A, B


def predict(A, B, m_id, u_id, mum):
    global movies, users
    if u_id in users:
        Rmu = A[m_id, :].dot(B[:, users[u_id].num]) + movies[m_id].get_rating() + users[u_id].avg_ratings() - mum
    else:
        Rmu = 0
        #print('User has no previous ratings.')

    return Rmu


def RMSE(A, B):
    global probe_movies
    mum = movie_user_mean()
    sum = 0
    n = 0
    p = Progress(len(probe_movies))

    for mov in probe_movies:
        for u_id, rating in probe_movies[mov].user_ratings.items():
            pred_rating = predict(A, B, probe_movies[mov].m_id, u_id, mum)
            if pred_rating == 0:
                n -= 1
            else:
                sum += (pred_rating - rating)**2
        p.percent(mov)

    for key in probe_movies:
        n += len(probe_movies[key].user_ratings)

    return math.sqrt(sum/n)


def zero_test(mum):
    global movies, users
    pp_all_ratings = []
    for mov in movies.values():
        for u_id, rating in mov.user_ratings.items():
            pp_all_ratings.append(rating - mov.get_rating() - users[u_id].avg_ratings() + mum)
    return sum(pp_all_ratings)


load_movies()
load_probes()
load_users()
print("Loading... done")
#a3 = user_means()
#a4 = movie_means()
#a5, n = movie_user_mean()
#print(predict(A, B, 1, 30878))
#a6 = zero_test(a5)
#a = 1
ks = [10, 20, 30, 40, 50]
its = [1000, 10000, 50000]
for k in ks:
    for i in its:
        A, B = train(k, i)
        print("k=", k, "iters=", i, "RMSE=", RMSE(A, B))

