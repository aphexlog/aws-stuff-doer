from textual import events
from textual.app import App

from app.views.screens import MainScreen, HelpScreen, WelcomeScreen
from app.views.widgets.profile_select import ListProfileApp


class App(App):  # type: ignore
    """beginnings of aws_stuff_doer terminal ui..."""

    MODES = {"welcome": "welcome", "default": "main", "help": "help"}  # type: ignore

    SCREENS = {"welcome": WelcomeScreen, "main": MainScreen, "help": HelpScreen, "profile": ListProfileApp}  # type: ignore

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("d", "toggle_dark", "Toggle dark mode"),
        ("?", "toggle_help", "Toggle Help"),
        ("l", "login", "Login to AWS SSO"),
        ("p", "select_profile", "Select a profile"),
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
        pass

    def action_select_profile(self) -> None:
        """An action to select a profile."""
        self.app.push_screen("profile")
