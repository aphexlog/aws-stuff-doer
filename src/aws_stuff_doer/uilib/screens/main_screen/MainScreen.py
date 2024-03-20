from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Footer, Placeholder

from aws_stuff_doer.uilib.widgets import CustomHeader


class MainScreen(Screen): # type: ignore
    """A simple home screen."""
    def compose(self) -> ComposeResult:
        yield CustomHeader()
        yield Placeholder("Main Screen")
        yield Footer()

