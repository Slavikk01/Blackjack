from participant import Participant


class Dealer(Participant):
    def __init__(self):
        super().__init__()

    def must_hit(self):
        # Дилер бере карту, якщо має менше 17
        if self.score < 17:
            return True

        return False
