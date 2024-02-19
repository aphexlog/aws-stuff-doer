from textual.app import App, ComposeResult
from textual.events import Show
from textual.widgets import Header, Footer


class TerminalUi(App):
    """A Textual app to manage stopwatches."""

    TITLE = "ASD"
    SUB_TITLE = " An AWS Utility to help manage your projects and sso sessions."
    BINDINGS = [
        ("q", "quit", "Quit"),
        ("d", "toggle_dark", "Toggle dark mode"),
        ("?", "show_help", "Show help"),
    ]
    help = """
    ASD: An AWS Utility to help manage your projects and sso sessions.

    Keybindings:

        d: Toggle dark mode
        q: Quit
        ?: Show help

    """

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield Footer()

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        if hasattr(self, "dark"):
            self.dark = not self.dark
            self.refresh()
        else:
            self.dark = True
            self.refresh()


if __name__ == "__main__":
    app = TerminalUi()
    app.run()
