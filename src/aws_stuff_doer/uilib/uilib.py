from textual import events
from textual.app import App

from aws_stuff_doer.uilib.screens import MainScreen, HelpScreen, WelcomeScreen
from aws_stuff_doer.login.login import authenticate_sso


class AwsStuffDoer(App):  # type: ignore
    """beginnings of aws_stuff_doer terminal ui..."""

    MODES = {  # type: ignore
        "welcome": "welcome",
        "default": "main",
        "help": "help",
    }

    SCREENS = {"welcome": WelcomeScreen, "main": MainScreen, "help": HelpScreen}

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("d", "toggle_dark", "Toggle dark mode"),
        ("?", "toggle_help", "Toggle Help"),
        ("l", "login", "Login to AWS SSO"),
    ]

    TITLE = "ASD"
    SUB_TITLE = " An AWS Utility to help manage your projects and sso sessions."

    def on_mount(self) -> None:
        """Handle mount event."""
        self.switch_mode("welcome")

    def on_key(self, event: events.Key) -> None:
        """Handle key events."""
        # If we are in the welcome screen, switch to the default screen when any key is pressed
        if self.current_mode == "welcome" and event.key != "d" and event.key != "q":
            self.app.switch_mode("default")

    def action_toggle_help(self) -> None:
        """An action to toggle the help screen."""
        current_mode = self.current_mode
        new_mode = "help" if current_mode != "help" else "default"
        self.switch_mode(new_mode)

    def action_login(self) -> None:
        """An action to login to AWS SSO."""
        profile = self.select_profile()
        authenticate_sso(profile)

    def select_profile(self) -> str:
        # Here you should implement the logic to let the user select a profile
        # For now, we'll just return a placeholder profile name
        return "elevator-robot"


if __name__ == "__main__":
    app = AwsStuffDoer()
    app.run()
