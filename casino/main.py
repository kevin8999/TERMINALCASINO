from .menu.constants import CASINO_HEADER_OPTIONS
from .menu.main_menu import main
from .utils import cprint, clear_screen, display_topbar


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        clear_screen()
        display_topbar(account=None, **CASINO_HEADER_OPTIONS)
        cprint("\nGoodbye! (Interrupted)\n")
