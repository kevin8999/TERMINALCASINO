from unittest.mock import patch,ANY,call,Mock
from casino.menu.main_menu import *
from casino.games import *
import pytest

#Add more tests as needed


def test_empty_name_and_quit():
    inputs = ["","TEST","1","8","q"]
    mock_input = Mock(side_effect=inputs)
    mock_print = Mock()

    with patch("casino.menu.main_menu.cinput", mock_input), \
        patch("casino.menu.views.view.cinput", mock_input), \
        patch("casino.menu.main_menu.get_theme"), \
        patch("casino.menu.main_menu.Account.generate") as mock_generate, \
        patch("casino.menu.main_menu.cprint", mock_print), \
        patch("casino.menu.views.view.cprint", mock_print), \
        patch("casino.menu.main_menu.clear_screen"), \
        patch("casino.menu.main_menu.display_topbar"):

        main()

    mock_generate.assert_called_with('TEST',ANY)
    mock_print.assert_called_with("\nGoodbye!\n")

def test_interrupt():
    with patch("casino.menu.main_menu.cinput", side_effect=KeyboardInterrupt):
        with pytest.raises(KeyboardInterrupt):
            main()

def test_invalid_game():
    ctx = GameContext(account=Account.generate('test', 100), config=Config.default())
    inputs = ["E","Poker","Blackjack","[1]","20","1.5","Quit","-1",KeyboardInterrupt]
    mock_print = Mock()
    with patch("casino.menu.views.view.cinput",side_effect=inputs), \
         patch("casino.menu.main_menu.cprint", mock_print), \
         patch("casino.menu.views.view.cprint", mock_print):
            with pytest.raises(KeyboardInterrupt):
                MainMenu(ctx).run()
    mock_print.assert_called_with("\nInvalid input. Please try again.\n")
    assert mock_print.call_args_list.count(call("\nInvalid input. Please try again.\n"))==len(inputs)-2

@pytest.mark.parametrize("game_index, game_name", [(str(i + 1), name) for i, name in enumerate(ALL_GAMES)])
def test_game_handler_called(game_index, game_name):
    ctx = GameContext(account=Account.generate("test", 100), config=Config.default())
    handlers = {name: Mock() for name in ALL_GAMES}
    with patch("casino.menu.main_menu.prompt_with_refresh", side_effect=["e", game_index, "q"]), \
         patch("casino.menu.main_menu.GAME_HANDLERS", handlers), \
         patch("casino.menu.main_menu.ALL_GAMES", ALL_GAMES), \
         patch("casino.menu.main_menu.cprint"), \
         patch("casino.menu.main_menu.clear_screen"), \
         patch("casino.menu.main_menu.display_topbar"), \
         patch("casino.menu.main_menu.get_theme"), \
         patch("casino.menu.main_menu.cinput", return_value="q"):
          MainMenu(ctx).run()

    handlers[game_name].assert_called_once()

    for other_name, mock_func in handlers.items():
        if other_name != game_name:
            mock_func.assert_not_called()