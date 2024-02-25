"""a profile selection screen"""

from textual.app import App, ComposeResult
from textual.screen import Screen
from textual.widgets import ListView, ListItem, Label, Footer, Header
from aws_stuff_doer.login.login import list_profiles


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
        yield Header()
        yield ListView(*[LabelItem(profile) for profile in PROFILES], id="list")
        yield Label("Choose a profile...", id="chosen")
        yield Footer()

    def on_list_view_selected(self, event: ListView.Selected):
        self.query_one("#chosen", Label).update(event.item.label)


if __name__ == "__main__":
    app = ListProfileApp()
    app.run()
