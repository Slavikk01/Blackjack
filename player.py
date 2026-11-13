
from participant import Participant
from logger import get_logger


logger = get_logger(__name__)


class Player(Participant):
    def __init__(self, name, money=1000):
        super().__init__()
        self._name = name
        self._money = money
        self._bet = 0

        logger.info(
            "Player created: %s, initial balance: %s",
            self._name,
            self._money
        )

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
            logger.warning(
                "Invalid bet from %s: %s",
                self._name,
                amount
            )
            print("Ставка повинна бути більшою за 0.")
            return False

        if amount > self._money:
            logger.warning(
                "Insufficient balance for %s. Bet: %s, balance: %s",
                self._name,
                amount,
                self._money
            )
            print("Недостатньо грошей для такої ставки.")
            return False

        self._bet = amount
        self._money -= amount

        logger.info(
            "Player %s placed bet: %s. Remaining balance: %s",
            self._name,
            amount,
            self._money
        )

        return True

    def win(self, multiplier=2):
        winnings = int(self._bet * multiplier)
        self._money += winnings

        logger.info(
            "Player %s won. Payout: %s, balance: %s",
            self._name,
            winnings,
            self._money
        )

        self._bet = 0

    def lose(self):
        logger.info(
            "Player %s lost bet: %s. Balance: %s",
            self._name,
            self._bet,
            self._money
        )

        self._bet = 0

    def push(self):
        self._money += self._bet

        logger.info(
            "Player %s received bet back: %s. Balance: %s",
            self._name,
            self._bet,
            self._money
        )

        self._bet = 0

    def choose_action(self):
        while True:
            choice = input("Ваш вибір: ")

            if choice == "1":
                return "hit"

            if choice == "2":
                return "stand"

            print("Невірний вибір.")
