"""a profile selection screen"""

from textual.app import ComposeResult
from textual.widgets import Header, Footer, ListView, ListItem
from textual.containers import Container


class ProfileSelect(Container):  # type: ignore
    """A simple profile selection screen."""

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield ListView()
