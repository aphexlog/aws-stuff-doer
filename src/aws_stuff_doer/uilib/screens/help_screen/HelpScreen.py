from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, Static

HELP_TEXT =  """
                           Help Menu
    ASD: An AWS Utility to help manage your projects and sso sessions.

    Keybindings:

        d: Toggle dark mode
        q: Quit
        h: Show help

    Press escape to exit.
    """

class HelpScreen(Screen): # type: ignore
    """A simple help screen."""

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static(HELP_TEXT)
        yield Footer()

