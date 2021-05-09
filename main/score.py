class Score:
    __score = 0

    def increment_score(self, amount):
        self.__score += amount

    def decrement_score(self, amount):
        self.__score -= amount

    def reset_score(self):
        self.__score = 0

    def get_score(self):
        return round(self.__score, 2)
