
from ..accounts import Account
from ..config import Config
from ..types import GameContext
from ..utils import cprint, cinput, clear_screen, display_topbar
from .views.view import prompt_with_refresh
from .views.themes import get_theme

from .constants import (
    ACCOUNT_STARTING_BALANCE,
    ALL_GAMES,
    CASINO_HEADER_OPTIONS,
    ENTER_OR_QUIT_PROMPT,
    GAME_CHOICE_PROMPT,
    GAME_HANDLERS,
    INVALID_CHOICE_PROMPT,
    term_width,
)


class MainMenu:
    """
    Main loop: show welcome, then (if chosen) show game menu, call handler,
    then return to top-level menu. No recursion used.
    """

    BOX_WIDTH = 30

    def __init__(self, ctx: GameContext) -> None:
        self.ctx = ctx

    @classmethod
    def create(cls) -> "MainMenu":
        """Ask for the player's name and theme, then build a menu for them."""
        cls._render_header(account=None)
        name = cinput("Enter your name: ").strip()
        while not name:
            cls._render_header(account=None)
            cprint("\nInvalid input. Please enter a valid name.\n")
            name = cinput("Enter your name: ").strip()

        # theme selection
        cls._render_header(account=None)
        get_theme()

        account = Account.generate(name, ACCOUNT_STARTING_BALANCE)
        return cls(GameContext(account=account, config=Config.default()))

    def run(self) -> None:
        while True:
            if self._prompt_action() == "q":
                self._render_header(self.ctx.account)
                cprint("\nGoodbye!\n")
                break  # exit loop -> program ends

            self._play(ALL_GAMES[self._prompt_game() - 1])

    @staticmethod
    def _render_header(account) -> None:
        clear_screen()
        display_topbar(account, **CASINO_HEADER_OPTIONS)

    def _render_welcome(self) -> None:
        self._render_header(self.ctx.account)
        cprint("")  # spacing

    def _render_game_list(self) -> None:
        self._render_welcome()
        width = term_width()
        max_length = max(map(len, ALL_GAMES))

        cprint("┌" + "─" * self.BOX_WIDTH + "┐")
        cprint("│" + " " * self.BOX_WIDTH + "│")
        for i, name in enumerate(ALL_GAMES, start=1):
            left_aligned_title = f"{name.title() :<{max_length}}"
            label = f"[{i}] {left_aligned_title}".center(self.BOX_WIDTH)
            cprint(f"│{label}│".center(width))
        cprint("│" + " " * self.BOX_WIDTH + "│")
        cprint("└" + "─" * self.BOX_WIDTH + "┘")

    def _prompt_action(self) -> str:
        return prompt_with_refresh(
            render_fn = self._render_welcome,
            prompt = ENTER_OR_QUIT_PROMPT.center(term_width()),
            error_message = INVALID_CHOICE_PROMPT,
            validator = lambda x: x.lower() in {"e", "q"},
            transform = lambda s: s.strip().lower(),
        )

    def _prompt_game(self) -> int:
        choice = prompt_with_refresh(
            render_fn = self._render_game_list,
            prompt = GAME_CHOICE_PROMPT.center(term_width()),
            error_message = INVALID_CHOICE_PROMPT,
            validator = lambda x: x.isdigit() and 1 <= int(x) <= len(ALL_GAMES),
        )
        return int(choice)

    def _play(self, game: str) -> None:
        handler = GAME_HANDLERS.get(game)
        if handler:
            clear_screen()
            handler(self.ctx)  # returns to loop after game finishes
        else:
            self._render_header(self.ctx.account)
            cprint("\nNo such game!\n")


def main():
    MainMenu.create().run()
