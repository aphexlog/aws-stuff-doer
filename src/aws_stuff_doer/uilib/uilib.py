from textual.app import App
from aws_stuff_doer.uilib.screens import MainScreen, HelpScreen


class AwsStuffDoer(App):
    """beginnings of aws_stuff_doer terminal ui..."""

    MODES = {  # type: ignore
        "default": "main",
        "help": "help",
    }

    SCREENS = {"main": MainScreen, "help": HelpScreen}
    TITLE = "ASD"
    SUB_TITLE = " An AWS Utility to help manage your projects and sso sessions."

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("d", "toggle_dark", "Toggle dark mode"),
        ("?", "toggle_help", "Toggle Help"),
    ]

    def action_toggle_help(self) -> None:
        """An action to toggle the help screen."""
        current_mode = self.current_mode
        new_mode = "help" if current_mode != "help" else "default"
        self.switch_mode(new_mode)

    def on_mount(self) -> None:
        self.switch_mode("default")


if __name__ == "__main__":
    app = AwsStuffDoer()
    app.run()
