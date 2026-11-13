
from dealer import Dealer
from deck import Deck
from game_interface import GameInterface
from participant import Participant
from player import Player
from rules import Rules
from logger import get_logger


logger = get_logger(__name__)


class BlackjackGame(GameInterface):
    def __init__(self, player_name):
        self._deck = Deck()
        self._player = Player(player_name)
        self._dealer = Dealer()
        self._participants: list[Participant] = [
            self._player,
            self._dealer
        ]
        self._rules = Rules()
        self._round_number = 0
        self._game_over = False

        logger.info("Blackjack game initialized for player: %s", player_name)

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
    def participants(self):
        return self._participants

    @property
    def players(self):
        return self._participants

    @property
    def rules(self):
        return self._rules

    @property
    def round_number(self):
        return self._round_number

    @property
    def game_over(self):
        return self._game_over

    def choose_participant_actions(self):
        actions = []

        for participant in self._participants:
            action = participant.choose_action()
            actions.append(action)

        return actions

    def make_move(self, player: Participant) -> str:
        action = player.choose_action()

        participant_name = (
            "player" if player is self._player else "dealer"
        )

        logger.info("%s chose action: %s", participant_name, action)

        if action == "hit":
            card = self._deck.draw_card()
            player.hand.add_card(card)

            logger.info(
                "%s drew a card. Current score: %s",
                participant_name,
                player.hand.score
            )

        return action

    # ------------------------------------------------------
    # Нова гра
    # ------------------------------------------------------
    def start_round(self):
        self._round_number += 1

        logger.info("Round %s started", self._round_number)

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
                    logger.info(
                        "Player placed a bet: %s. Balance: %s",
                        bet,
                        self._player.money
                    )
                    break
                else:
                    logger.warning("Invalid bet amount: %s", bet)

            except ValueError:
                logger.warning("Player entered an invalid bet value")
                print("Введіть ціле число.")

        # Роздача карт
        self.deal_initial_cards()

        # Перевірка Blackjack
        if self._player.hand.is_blackjack:
            logger.info("Player has Blackjack")

            print("\nУ вас BLACKJACK!")

            if self._dealer.hand.is_blackjack:
                logger.info("Both player and dealer have Blackjack")

                print("У дилера також BLACKJACK!")
                self._player.push()
            else:
                print("Ви перемогли!")
                self._player.win(self._rules.blackjack_payout)

            return

        # Якщо дилер має Blackjack
        if self._dealer.hand.is_blackjack:
            logger.info("Dealer has Blackjack")

            print("\nУ дилера BLACKJACK!")
            self._player.lose()
            return

        self.player_turn()

        # Якщо гравець перебрав
        if self._player.hand.is_bust:
            logger.info(
                "Player went bust with score: %s",
                self._player.hand.score
            )

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

        logger.info(
            "Initial cards dealt. Player score: %s, dealer score: %s",
            self._player.hand.score,
            self._dealer.hand.score
        )

        print("\nВаші карти:")
        print(self._player.hand.show_cards())
        print(f"Ваш рахунок: {self._player.hand.score}")

        print("\nКарти дилера:")
        print(self._dealer.hand.show_cards(hide_first=True))

    # ------------------------------------------------------
    # Хід гравця
    # ------------------------------------------------------
    def player_turn(self):
        participant: Participant = self._player

        logger.info("Player turn started")

        while True:
            print("\n" + "-" * 40)
            print("Ваш хід")
            print(f"Карти: {participant.hand.show_cards()}")
            print(f"Рахунок: {participant.hand.score}")

            if participant.hand.score == 21:
                logger.info("Player reached 21")

                print("У вас 21!")
                break

            print("\n1 - Hit (взяти карту)")
            print("2 - Stand (зупинитися)")

            action = self.make_move(participant)

            if action == "hit":
                new_card = participant.hand.cards[-1]
                print(f"\nВи отримали: {new_card}")
                print(f"Новий рахунок: {participant.hand.score}")

                if participant.hand.is_bust:
                    break
            else:
                logger.info("Player decided to stand")
                print("Ви зупинилися.")
                break

        logger.info(
            "Player turn finished. Final score: %s",
            participant.hand.score
        )

    # ------------------------------------------------------
    # Хід дилера
    # ------------------------------------------------------
    def dealer_turn(self):
        participant: Participant = self._dealer

        logger.info("Dealer turn started")

        print("\n" + "-" * 40)
        print("Хід дилера")
        print(f"Карти дилера: {participant.hand.show_cards()}")
        print(f"Рахунок дилера: {participant.score}")

        while self.make_move(participant) == "hit":
            new_card = participant.hand.cards[-1]
            print(f"Дилер бере карту: {new_card}")
            print(f"Новий рахунок дилера: {participant.score}")

        if participant.hand.is_bust:
            logger.info(
                "Dealer went bust with score: %s",
                participant.hand.score
            )
            print("Дилер перебрав 21!")
        else:
            logger.info(
                "Dealer stopped with score: %s",
                participant.score
            )
            print(f"Дилер зупинився на {participant.score}.")

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

        logger.info("Round result: %s", winner)

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

        logger.info(
            "Round %s finished. Player balance: %s",
            self._round_number,
            self._player.money
        )

        print(f"Ваш баланс: ${self._player.money}")

    # ------------------------------------------------------
    # Запуск гри
    # ------------------------------------------------------
    def run(self):
        logger.info("Blackjack game started")

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
                logger.info("Player ran out of money")

                print("\nУ вас закінчилися гроші.")
                break

            print("\nХочете зіграти ще раз?")
            print("1 - Так")
            print("2 - Ні")

            choice = input("Ваш вибір: ")

            if choice != "1":
                logger.info("Player decided to end the game")
                break

        self._game_over = True

        logger.info(
            "Blackjack game finished. Final balance: %s",
            self._player.money
        )

        print("\n" + "=" * 50)
        print("ДЯКУЄМО ЗА ГРУ!")
        print(f"Кінцевий баланс: ${self._player.money}")
        print("=" * 50)
