class Movie:
    def __init__(self, m_id, user_ratings):
        self.m_id = int(m_id)
        self.user_ratings = user_ratings

    def remove_user(self, u_id):
        self.user_ratings.pop(u_id)

    def add_user(self, u_id, rating=None):
        if u_id not in self.user_ratings:
            self.user_ratings[u_id] = rating
        else:
            raise ValueError('User already exists') #YUUUUUU