"""a profile selection screen"""

from textual import events
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import ListView, ListItem, Label, Footer

from aws_stuff_doer.login.login import list_profiles
from aws_stuff_doer.uilib.widgets import CustomHeader

def get_profiles():
    return list_profiles()

PROFILES: list[str] = get_profiles()

class LabelItem(ListItem):

    def __init__(self, label: str) -> None:
        super().__init__()
        self.label = label

    def compose(self) -> ComposeResult:
        yield Label(self.label)


class ListProfileApp(Screen):

    def compose(self) -> ComposeResult:
        yield CustomHeader(id="header")
        yield ListView(*[LabelItem(profile) for profile in PROFILES], id="list")
        yield Label("Choose a profile...", id="chosen")
        yield Footer()

    def on_list_view_selected(self, event: ListView.Selected):
        self.query_one("#chosen", Label).update(event.item.label)


    def on_key(self, event: events.Key) -> None:
        """handle if we want to bail on profile selection page."""
        if event.key == "escape":
            self.app.pop_screen()