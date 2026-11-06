from game import BlackjackGame
from rock_paper_scissors import RockPaperScissorsGame


if __name__ == "__main__":
    while True:
        print("Оберіть гру:")
        print("1 - Blackjack")
        print("2 - Камінь, ножиці, папір")
        print("0 - Вийти")
        choice = input("Ваш вибір: ").strip()

        if choice == "0":
            break
        if choice not in {"1", "2"}:
            print("Невірний вибір. Введіть 1, 2 або 0.\n")
            continue

        name = input("Введіть ваше ім'я: ")
        if choice == "1":
            game = BlackjackGame(name)
        else:
            game = RockPaperScissorsGame(name)

        game.run()
        break
