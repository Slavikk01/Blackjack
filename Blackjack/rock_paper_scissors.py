import random

from game_interface import GameInterface


class RockPaperScissorsGame(GameInterface):
    _moves = {
        "1": "камінь",
        "2": "ножиці",
        "3": "папір",
    }
    _winning_moves = {
        "камінь": "ножиці",
        "ножиці": "папір",
        "папір": "камінь",
    }

    def __init__(self, player_name):
        computer_name = "Комп'ютер"
        if player_name == computer_name:
            computer_name = "Комп'ютер-суперник"

        self._players = [player_name, computer_name]
        self._scores = {player: 0 for player in self._players}

    @property
    def players(self):
        return self._players

    @property
    def scores(self):
        return self._scores

    def make_move(self, player: str) -> str:
        if player not in self._players:
            raise ValueError(f"Невідомий гравець: {player}")

        if player == self._players[1]:
            return random.choice(list(self._winning_moves))

        while True:
            print("1 - Камінь")
            print("2 - Ножиці")
            print("3 - Папір")
            choice = input(f"{player}, ваш вибір: ")

            if choice in self._moves:
                return self._moves[choice]

            print("Невірний вибір. Введіть 1, 2 або 3.")

    def play_round(self):
        player_move = self.make_move(self._players[0])
        computer_move = self.make_move(self._players[1])

        print(f"{self._players[0]}: {player_move}")
        print(f"{self._players[1]}: {computer_move}")

        if player_move == computer_move:
            print("Нічия!")
        elif self._winning_moves[player_move] == computer_move:
            self._scores[self._players[0]] += 1
            print(f"Переміг гравець {self._players[0]}!")
        else:
            self._scores[self._players[1]] += 1
            print(f"Переміг {self._players[1]}!")

        print(
            f"Рахунок: {self._players[0]} "
            f"{self._scores[self._players[0]]} : "
            f"{self._scores[self._players[1]]} {self._players[1]}"
        )

    def run(self):
        print("\nКАМІНЬ, НОЖИЦІ, ПАПІР")

        while True:
            self.play_round()

            if input("Зіграти ще раз? (так/ні): ").strip().lower() not in {
                "так", "т", "yes", "y"
            }:
                break
