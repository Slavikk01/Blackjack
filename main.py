
from game import BlackjackGame
from rock_paper_scissors import RockPaperScissorsGame
from logger import get_logger


logger = get_logger(__name__)


if __name__ == "__main__":
    logger.info("Application started")

    while True:
        print("Оберіть гру:")
        print("1 - Blackjack")
        print("2 - Камінь, ножиці, папір")
        print("0 - Вийти")
        choice = input("Ваш вибір: ").strip()

        if choice == "0":
            logger.info("User exited the application")
            break

        if choice not in {"1", "2"}:
            logger.warning("Invalid game selection: %s", choice)
            print("Невірний вибір. Введіть 1, 2 або 0.\n")
            continue

        name = input("Введіть ваше ім'я: ")

        if choice == "1":
            logger.info("Blackjack selected by player: %s", name)
            game = BlackjackGame(name)
        else:
            logger.info("Rock Paper Scissors selected by player: %s", name)
            game = RockPaperScissorsGame(name)

        game.run()
        break

    logger.info("Application finished")
