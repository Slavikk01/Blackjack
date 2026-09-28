from dealer import Dealer
from deck import Deck
from player import Player
from rules import Rules


class BlackjackGame:
    def __init__(self, player_name):
        self._deck = Deck()
        self._player = Player(player_name)
        self._dealer = Dealer()
        self._rules = Rules()
        self._round_number = 0
        self._game_over = False

    @property
    def deck(self):
        return self._deck

    @property
    def player(self):
        return self._player

    @property
    def dealer(self):
        return self._dealer

    @property
    def rules(self):
        return self._rules

    @property
    def round_number(self):
        return self._round_number

    @property
    def game_over(self):
        return self._game_over

    # ------------------------------------------------------
    # Нова гра
    # ------------------------------------------------------
    def start_round(self):
        self._round_number += 1

        self._player.reset_hand()
        self._dealer.reset_hand()

        print("\n" + "=" * 50)
        print(f"РАУНД №{self._round_number}")
        print("=" * 50)

        print(f"Ваш баланс: ${self._player.money}")

        # Вибір ставки
        while True:
            try:
                bet = int(input("Введіть вашу ставку: "))

                if self._player.place_bet(bet):
                    break

            except ValueError:
                print("Введіть ціле число.")

        # Роздача карт
        self.deal_initial_cards()

        # Перевірка Blackjack
        if self._player.hand.is_blackjack:
            print("\nУ вас BLACKJACK!")

            if self._dealer.hand.is_blackjack:
                print("У дилера також BLACKJACK!")
                self._player.push()
            else:
                print("Ви перемогли!")
                self._player.win(self._rules.blackjack_payout)

            return

        # Якщо дилер має Blackjack
        if self._dealer.hand.is_blackjack:
            print("\nУ дилера BLACKJACK!")
            self._player.lose()
            return

        self.player_turn()

        # Якщо гравець перебрав
        if self._player.hand.is_bust:
            print("Ви перебрали 21.")
            self._player.lose()
            return

        self.dealer_turn()

        self.finish_round()

    # ------------------------------------------------------
    # Початкова роздача
    # ------------------------------------------------------
    def deal_initial_cards(self):
        # Гравцю 2 карти
        self._player.hand.add_card(self._deck.draw_card())
        self._player.hand.add_card(self._deck.draw_card())

        # Дилеру 2 карти
        self._dealer.hand.add_card(self._deck.draw_card())
        self._dealer.hand.add_card(self._deck.draw_card())

        print("\nВаші карти:")
        print(self._player.hand.show_cards())
        print(f"Ваш рахунок: {self._player.hand.score}")

        print("\nКарти дилера:")
        print(self._dealer.hand.show_cards(hide_first=True))

    # ------------------------------------------------------
    # Хід гравця
    # ------------------------------------------------------
    def player_turn(self):
        while True:
            print("\n" + "-" * 40)
            print("Ваш хід")
            print(f"Карти: {self._player.hand.show_cards()}")
            print(f"Рахунок: {self._player.hand.score}")

            if self._player.hand.score == 21:
                print("У вас 21!")
                break

            print("\n1 - Hit (взяти карту)")
            print("2 - Stand (зупинитися)")

            action = self._player.choose_action()

            if action == "hit":
                new_card = self._deck.draw_card()
                self._player.hand.add_card(new_card)

                print(f"\nВи отримали: {new_card}")
                print(f"Новий рахунок: {self._player.hand.score}")

                if self._player.hand.is_bust:
                    break
            else:
                print("Ви зупинилися.")
                break

    # ------------------------------------------------------
    # Хід дилера
    # ------------------------------------------------------
    def dealer_turn(self):
        print("\n" + "-" * 40)
        print("Хід дилера")
        print(f"Карти дилера: {self._dealer.hand.show_cards()}")
        print(f"Рахунок дилера: {self._dealer.score}")

        while self._dealer.choose_action() == "hit":
            new_card = self._deck.draw_card()
            self._dealer.hand.add_card(new_card)

            print(f"Дилер бере карту: {new_card}")
            print(f"Новий рахунок дилера: {self._dealer.score}")

        if self._dealer.hand.is_bust:
            print("Дилер перебрав 21!")
        else:
            print(f"Дилер зупинився на {self._dealer.score}.")

    # ------------------------------------------------------
    # Завершення раунду
    # ------------------------------------------------------
    def finish_round(self):
        print("\n" + "=" * 50)
        print("РЕЗУЛЬТАТ")
        print("=" * 50)

        print(f"Ваші карти: {self._player.hand.show_cards()}")
        print(f"Ваш рахунок: {self._player.hand.score}")

        print(f"Карти дилера: {self._dealer.hand.show_cards()}")
        print(f"Рахунок дилера: {self._dealer.score}")

        winner = self._rules.determine_winner(
            self._player,
            self._dealer
        )

        if winner == "player":
            print("\nВи перемогли!")
            self._player.win()

        elif winner == "dealer":
            print("\nДилер переміг.")
            self._player.lose()

        elif winner == "blackjack":
            print("\nBLACKJACK! Ви перемогли!")
            self._player.win(self._rules.blackjack_payout)

        elif winner == "push":
            print("\nНічия!")
            self._player.push()

        print(f"Ваш баланс: ${self._player.money}")

    # ------------------------------------------------------
    # Запуск гри
    # ------------------------------------------------------
    def run(self):
        print("=" * 50)
        print("          BLACKJACK")
        print("=" * 50)

        print("Правила:")
        print("- Мета — набрати якомога ближче до 21.")
        print("- Якщо більше 21 — ви програли.")
        print("- Картинки J, Q, K = 10.")
        print("- Туз A = 11 або 1.")
        print("- Дилер бере карти до 17.")
        print("- Blackjack = A + карта на 10.")

        while self._player.money > 0:
            self.start_round()

            if self._player.money <= 0:
                print("\nУ вас закінчилися гроші.")
                break

            print("\nХочете зіграти ще раз?")
            print("1 - Так")
            print("2 - Ні")

            choice = input("Ваш вибір: ")

            if choice != "1":
                break

        self._game_over = True

        print("\n" + "=" * 50)
        print("ДЯКУЄМО ЗА ГРУ!")
        print(f"Кінцевий баланс: ${self._player.money}")
        print("=" * 50)
