import os
import shutil
import json

from typing import Optional
from casino.accounts import Account

from .cards import Card

#default fallback so theme is always defined
theme = {"color": "", "reset": ""}

def clear_screen() -> None:
    """Clear the screen."""
    if os.name == "nt":  # Windows
        os.system("cls")
    else:  # Unix
        # clear screen + clear scrollback buffer
        os.system('clear && printf "\\033[3J"')


def cprint(*args, sep: str = " ", end: str = "\n") -> None:
    """Print text in the center of the screen."""
    terminal_width = shutil.get_terminal_size().columns
    text = sep.join(map(str, args))

    # split lines and print each one centered
    lines = text.splitlines()
    for i, line in enumerate(lines):
        # center text then print colored
        line_center = line.center(terminal_width)
        colored_line = f"{theme['color']}{line_center}{theme['reset']}"
        if i < len(lines) - 1:
            print(colored_line)
        else:
            print(colored_line, end=end)


def cinput(prompt: str = "") -> str:
    """Get input from the user in the center of the screen."""
    terminal_width = shutil.get_terminal_size().columns
    # center text then print colored
    prompt_center = prompt.center(terminal_width)
    colored_prompt = f"{theme['color']}{prompt_center}{theme['reset']}"
    print(colored_prompt)

    # move cursor to the center for input
    cursor_padding = (terminal_width // 2) + 1
    print(" " * cursor_padding, end="")
    return input().strip()


def display_topbar(
    account: Optional[Account],
    header: str,
    margin: int = 1,
) -> None:
    """Display the top bar of the game."""
    cprint(header)
    if account:
        header_lines = header.splitlines()
        header_width = max(len(line) for line in header_lines if line.strip())

        left_text = f"👤 {account.name}"
        right_text = f"💰 {account.balance}"

        # Space available for padding
        inner_width = header_width
        cprint(f"{left_text}{right_text.rjust(inner_width - len(left_text))}")
    # Add margin after
    print("\n" * margin, end="")

def print_cards(hand: list[Card]) -> None:
    """Print ASCII card faces side by side."""

    # Get front or back of card depending on if it is hidden or not
    card_str = [card.back if card.hidden else card.front for card in hand]

    # Split each card into lines
    card_lines = [card.strip().splitlines() for card in card_str]

    # Find the tallest card
    max_height = max(len(lines) for lines in card_lines)

    # Normalize all cards to the same height
    for lines in card_lines:
        width = len(lines[0])
        lines.extend([" " * width] * (max_height - len(lines)))

    # Build each horizontal row across all cards
    rows = [
        "  ".join(lines[i] for lines in card_lines)
        for i in range(max_height)
    ]

    # Print as a single block
    cprint("\n".join(rows))
