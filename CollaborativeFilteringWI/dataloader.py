import math
import pickle
from movie import Movie

def load(mov_cnt, usr_cnt):
    """
    Parses and creates new training data files depending on the desired movie count and user count
    :param mov_cnt: movie count
    :param usr_cnt: user count
    """

    users = {}
    training_movies = {}
    for i in range(mov_cnt):
        mov_id = i + 1
        file_name = "mv_" + '0'*int(6-math.floor(math.log10(mov_id))) + str(mov_id) + ".txt"

        user_ratings = {}
        with open("download/training_set/" + file_name, 'r') as f:
            for line in f.readlines()[1:]:
                u_id, rating, date = line.split(',')
                user_ratings[int(u_id)] = int(rating)
        training_movies[mov_id] = Movie(mov_id, user_ratings)

    probe_movies = {}
    with open("download/probe.txt", 'r') as f:
        mov_id = 0
        for line in f.readlines():
            if ':' in line:
                mov_id = int(line[:-2])
            elif mov_id <= mov_cnt:
                u_id = int(line)
                if mov_id not in probe_movies:
                    probe_movies[mov_id] = Movie(mov_id, {u_id: training_movies[mov_id].user_ratings[u_id]})
                else:
                    probe_movies[mov_id].add_user(u_id, training_movies[mov_id].user_ratings[u_id])
                training_movies[mov_id].remove_user(u_id)

    with open('probe.pickle', 'wb+') as handle:
        pickle.dump(probe_movies, handle)

    with open('training.pickle', 'wb+') as handle:
        pickle.dump(training_movies, handle)

if __name__ == '__main__':
    load(1000, 1000)