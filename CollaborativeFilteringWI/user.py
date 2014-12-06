class User:
    count = 0

    def __init__(self, u_id):
        self.u_id = u_id
        self.ratings = {}
        self.rating = -1
        self.num = self.count
        self.count += 1

    def add_rating(self, m_id, rating):
        self.ratings[m_id] = rating

    def avg_ratings(self):
        if self.rating == -1:
            self.rating = sum(self.ratings.values()) / float(len(self.ratings))
        return self.rating
