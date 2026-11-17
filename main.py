from game import BlackjackGame
from rock_paper_scissors import RockPaperScissorsGame
from logger import get_logger
from profile_manager import load_profiles, save_profiles

logger = get_logger(__name__)


def choose_profile(profiles):
    """Дозволяє вибрати профіль, який заздалегідь створено у файлі."""
    names = list(profiles)
    print("\nДоступні профілі:")
    for index, name in enumerate(names, start=1):
        print(f"{index} - {name} ({profiles[name]} фішок)")

    while True:
        choice = input("Оберіть номер профілю (або 0 для виходу): ").strip()
        if choice == "0":
            return None
        if choice.isdigit() and 1 <= int(choice) <= len(names):
            return names[int(choice) - 1]
        print("Невірний вибір. Спробуйте ще раз.")


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

        if choice == "1":
            profiles = load_profiles()
            if not profiles:
                print("\nНемає створених профілів. Спочатку відкрийте profiles.txt і додайте профіль.")
                print("Приклад рядка: Андрій|1000")
                break

            name = choose_profile(profiles)
            if name is None:
                break

            logger.info("Blackjack selected by player: %s", name)
            game = BlackjackGame(name, starting_money=profiles[name])
            game.run()
            profiles[name] = game.player.money
            save_profiles(profiles)
        else:
            name = input("Введіть ваше ім'я: ")
            logger.info("Rock Paper Scissors selected by player: %s", name)
            game = RockPaperScissorsGame(name)
            game.run()

    logger.info("Application finished")
