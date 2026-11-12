"""Точка входу в ігровий проєкт.

За замовчуванням програма читає відповіді з input.txt, а весь результат
роботи (усі print() з модулів гри) записує в output.txt.

Для звичайного введення з клавіатури запустіть:
    python main.py --console
"""
import argparse
import sys
from contextlib import redirect_stdout
from pathlib import Path

from game import BlackjackGame
from rock_paper_scissors import RockPaperScissorsGame


def run_game():
    """Запускає меню та обрану гру."""
    while True:
        print("Оберіть гру:")
        print("1 - Blackjack")
        print("2 - Камінь, ножиці, папір")
        print("0 - Вийти")
        choice = input("Ваш вибір: ").strip()

        if choice == "0":
            print("Роботу програми завершено.")
            return
        if choice not in {"1", "2"}:
            print("Невірний вибір. Введіть 1, 2 або 0.\\n")
            continue

        name = input("Введіть ваше ім'я: ").strip()
        if choice == "1":
            game = BlackjackGame(name)
        else:
            game = RockPaperScissorsGame(name)

        game.run()
        return


def run_with_files(input_path: Path, output_path: Path):
    """Читає введення з одного файлу та записує виведення в інший."""
    if not input_path.is_file():
        print(f"Помилка: файл введення не знайдено: {input_path}")
        print("Створіть input.txt і запишіть у нього відповіді по одній на рядок.")
        return

    # Обидва файли відкриваються в UTF-8. redirect_stdout перехоплює
    # всі print() не лише з main.py, а й з game.py, player.py тощо.
    with (input_path.open("r", encoding="utf-8") as input_file,
          output_path.open("w", encoding="utf-8") as output_file):
        old_stdin = sys.stdin
        try:
            sys.stdin = input_file
            with redirect_stdout(output_file):
                try:
                    run_game()
                except EOFError:
                    print("\\nПомилка: у файлі введення закінчилися дані.")
                    print("Додайте всі потрібні відповіді до input.txt та запустіть програму знову.")
        finally:
            sys.stdin = old_stdin

    print(f"Гру виконано. Результат записано у файл: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Blackjack з файловим введенням/виведенням")
    parser.add_argument("--console", action="store_true",
                        help="запустити гру зі звичайним введенням із клавіатури")
    parser.add_argument("--input", default="input.txt",
                        help="шлях до файлу введення (за замовчуванням input.txt)")
    parser.add_argument("--output", default="output.txt",
                        help="шлях до файлу результату (за замовчуванням output.txt)")
    args = parser.parse_args()

    if args.console:
        run_game()
    else:
        run_with_files(Path(args.input), Path(args.output))


if __name__ == "__main__":
    main()
