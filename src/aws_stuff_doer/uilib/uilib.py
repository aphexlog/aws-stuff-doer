from textual.app import App
from aws_stuff_doer.uilib.screens import MainScreen, HelpScreen

class AwsStuffDoer(App): # type: ignore
    """beginnings of aws_stuff_doer terminal ui..."""

    MODES = { # type: ignore
        "default": "main",
        "help": "help",
    }

    SCREENS = {"main": MainScreen, "help": HelpScreen}
    TITLE = "ASD"
    SUB_TITLE = " An AWS Utility to help manage your projects and sso sessions."

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("d", "toggle_dark", "Toggle dark mode"),
        ("m", "switch_mode('default')", "Main"),
        ("h", "switch_mode('help')", "Help"),
    ]

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        if hasattr(self, "dark"):
            self.dark = not self.dark
            self.refresh()
        else:
            self.dark = True
            self.refresh()

    def on_mount(self) -> None:
        self.switch_mode("default")

if __name__ == "__main__":
    app = AwsStuffDoer()
    app.run()
