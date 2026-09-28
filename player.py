from participant import Participant


class Player(Participant):
    def __init__(self, name, money=1000):
        super().__init__()
        self._name = name
        self._money = money
        self._bet = 0

    @property
    def name(self):
        return self._name

    @property
    def money(self):
        return self._money

    @property
    def bet(self):
        return self._bet

    def place_bet(self, amount):
        if amount <= 0:
            print("Ставка повинна бути більшою за 0.")
            return False

        if amount > self._money:
            print("Недостатньо грошей для такої ставки.")
            return False

        self._bet = amount
        self._money -= amount
        return True

    def win(self, multiplier=2):
        self._money += int(self._bet * multiplier)
        self._bet = 0

    def lose(self):
        self._bet = 0

    def push(self):
        self._money += self._bet
        self._bet = 0

    def choose_action(self):
        while True:
            choice = input("Ваш вибір: ")
            if choice == "1":
                return "hit"
            if choice == "2":
                return "stand"
            print("Невірний вибір.")
