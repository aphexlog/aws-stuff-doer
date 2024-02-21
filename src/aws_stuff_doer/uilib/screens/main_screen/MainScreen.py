from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, Placeholder


class MainScreen(Screen): # type: ignore
    """A simple home screen."""
    def compose(self) -> ComposeResult:
        yield Header()
        yield Placeholder("Main Screen")
        yield Footer()

