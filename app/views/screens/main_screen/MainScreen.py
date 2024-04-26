from textual.app import ComposeResult
from textual.containers import ScrollableContainer, Container
from textual.screen import Screen
from textual.widgets import Footer, Placeholder

from app.views.widgets import CustomHeader, ListProfiles


class MainScreen(Screen): # type: ignore
    """A simple home screen."""


    def compose(self) -> ComposeResult:
        yield CustomHeader()
        # yield Placeholder("Main Screen")
        yield Container(ListProfiles(), classes="main-screen-container")
        yield Footer()
