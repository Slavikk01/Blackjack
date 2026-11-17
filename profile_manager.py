from pathlib import Path

PROFILES_FILE = Path(__file__).parent / "profiles.txt"


def load_profiles():
    """Зчитує профілі з profiles.txt у форматі ім'я|фішки."""
    profiles = {}
    if not PROFILES_FILE.exists():
        PROFILES_FILE.write_text(
            "# Формат: ім'я|кількість_фішок\n", encoding="utf-8"
        )
        return profiles

    for line_number, raw_line in enumerate(
        PROFILES_FILE.read_text(encoding="utf-8").splitlines(), start=1
    ):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        try:
            name, chips_text = line.rsplit("|", 1)
            name = name.strip()
            chips = int(chips_text.strip())
            if not name or chips < 0:
                raise ValueError
            profiles[name] = chips
        except ValueError:
            print(
                f"Увага: пропущено некоректний рядок {line_number} у profiles.txt."
            )
    return profiles


def save_profiles(profiles):
    """Перезаписує файл актуальними балансами всіх профілів."""
    lines = [
        "# Профілі гравців для Blackjack",
        "# Формат кожного рядка: ім'я|кількість_фішок",
    ]
    lines.extend(f"{name}|{chips}" for name, chips in profiles.items())
    PROFILES_FILE.write_text("\n".join(lines) + "\n", encoding="utf-8")
