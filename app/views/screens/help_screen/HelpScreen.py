from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Footer, Static

from app.views.widgets import CustomHeader

HELP_TEXT = """
                           Help Menu
    ASD: An AWS Utility to help manage your projects and sso sessions.

    Key Bindings:

        q: Quit
        d: Toggle dark mode
        ?: Toggle help screen

    """


class HelpScreen(Screen):  # type: ignore
    """A simple help screen."""

    def compose(self) -> ComposeResult:
        yield CustomHeader()
        yield Static(HELP_TEXT)
        yield Footer()
