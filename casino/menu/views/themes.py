from pathlib import Path
from ...utils import cprint, cinput

BASE_DIR = Path(__file__).resolve().parents[2]  # casino/
THEME_DIR = BASE_DIR / "themes"

# loads theme from json file
def load_theme(folder: str, name: str) -> dict[str, str]:
    """Load a theme by name from a specific folder"""
    theme_path = THEME_DIR / folder / f"{name}.json"
    with open(theme_path, "r", encoding="utf-8") as f:
        return json.load(f)

def get_theme():
    # cprint/cinput read utils.theme, so the chosen theme must be stored there
    # choose from original 16 terminal colors or custom colors
    cprint(f"Please choose a theme folder below, or press enter to use default")
    folder = cinput(f"1.Original Terminal   2.Custom Colors")

    # original 16
    if folder == '1':
        ansi_dir = THEME_DIR / "ansi"
        themes = [f.stem for f in ansi_dir.glob("*.json")]

        if not themes:
            cprint("No ANSI themes found.")
            return

        cprint("Please choose an ANSI theme:")
        for i, t_name in enumerate(themes, start=1):
            cprint(f"{i}. {t_name}")

        try:
            choice = int(cinput("Enter number: "))
            if 1 <= choice <= len(themes):
                utils.theme = load_theme("ansi", themes[choice - 1])
                cprint(f"Loaded theme: {themes[choice - 1]}")
            else:
                cprint("Invalid choice. Default theme chosen.")
        except ValueError:
            cprint("Invalid input. Default theme chosen.")
    # custom user added colors
    elif folder == '2':
        custom_dir = THEME_DIR / "custom"
        themes = [f.stem for f in custom_dir.glob("*.json")]

        if not themes:
            cprint("No custom themes found.")
            return

        cprint("Please choose a custom theme:")
        for i, t_name in enumerate(themes, start=1):
            cprint(f"{i}. {t_name}")

        try:
            choice = int(cinput("Enter number: "))
            if 1 <= choice <= len(themes):
                utils.theme = load_theme("custom", themes[choice - 1])
                cprint(f"Loaded theme: {themes[choice - 1]}")
            else:
                cprint("Invalid choice. Default theme chosen.")
        except ValueError:
            cprint("Invalid input. Default theme chosen.")
    # neither chosen, default used
    else:
        cprint("Invalid choice. Default theme chosen.")
