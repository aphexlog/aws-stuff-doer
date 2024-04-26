"""a profile selection screen"""

from textual import events
from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import ListView, ListItem, Label

from app.services.login import AWSAuthenticator

def get_profiles():
    return AWSAuthenticator.list_profiles()

PROFILES: list[str] = get_profiles()

class LabelItem(ListItem):

    def __init__(self, label: str) -> None:
        super().__init__()
        self.label = label

    def compose(self) -> ComposeResult:
        yield Label(self.label)

class ListProfiles(Widget):
    """A simple profile selection window."""

    DEFAULT_CSS = """
    ListView {
        color: white;
        width: 30%;
    }

    ListItem {
        padding: 1;
    }

    ListItem:hover {
        background: $panel;
    }

    Label {
        color: white;
    }
    """

    def compose(self) -> ComposeResult:
        print("TEST...")
        yield ListView(*[LabelItem(profile) for profile in PROFILES], id="list")
        yield Label("Choose a profile...", id="chosen")

    def on_list_view_selected(self, event: ListView.Selected):
        self.query_one("#chosen", Label).update(event.item.label)


    def on_key(self, event: events.Key) -> None:
        """handle if we want to bail on profile selection page."""
        if event.key == "escape":
            self.app.pop_screen()
