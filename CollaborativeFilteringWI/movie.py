class Movie:
    def __init__(self, m_id, user_ratings):
        self.m_id = int(m_id)
        self.user_ratings = user_ratings
        self.rating = -1

    def remove_user(self, u_id):
        self.user_ratings.pop(u_id)

    def add_user(self, u_id, rating=None):
        if u_id not in self.user_ratings:
            self.user_ratings[u_id] = rating
        else:
            raise ValueError('User already exists') #YUUUUUU

    def get_rating(self):
        if self.rating == -1:

            self.rating = sum(self.user_ratings.values()) / float(len(self.user_ratings))

        return self.rating