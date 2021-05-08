class Score:
    score = 0

    def increment_score(self, amount):
        self.score += amount

    def decrement_score(self, amount):
        self.score = max(0, self.score - amount)

    def reset_score(self):
        self.score = 0

    def get_score(self):
        return self.score