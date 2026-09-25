from game import BlackjackGame


if __name__ == "__main__":
    name = input("Введіть ваше ім'я: ")

    game = BlackjackGame(name)
    game.run()
