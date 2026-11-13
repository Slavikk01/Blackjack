from game import BlackjackGame
from contextlib import redirect_stdout
from pathlib import Path
import sys


if __name__ == "__main__":
    # Файли знаходяться в тій самій папці, що й main.py.
    folder = Path(__file__).resolve().parent
    input_path = folder / "input.txt"
    output_path = folder / "output.txt"

    try:
        # Зчитуємо відповіді гравця з input.txt,
        # а всі повідомлення програми записуємо в output.txt.
        with input_path.open("r", encoding="utf-8") as input_file, \
             output_path.open("w", encoding="utf-8") as output_file:
            old_stdin = sys.stdin
            try:
                sys.stdin = input_file
                with redirect_stdout(output_file):
                    name = input("Введіть ваше ім'я: ")
                    game = BlackjackGame(name)
                    game.run()
            finally:
                sys.stdin = old_stdin

    except FileNotFoundError:
        print(f"Помилка: файл введення не знайдено: {input_path}")
        print("Створіть input.txt у папці з main.py та запишіть відповіді по одній на рядок.")
