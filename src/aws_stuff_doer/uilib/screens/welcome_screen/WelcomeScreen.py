from rich.markdown import Markdown

from textual.app import ComposeResult
from textual.screen import Screen
from textual.containers import Container
from textual.widgets import Header, Footer, Static


WELCOME_MD = """\
# Welcome to ASD!

ASD is a terminal-based User Interface (UI) designed to streamline the management of your AWS projects and Single Sign-On (SSO) sessions.

**Here are some key functionalities provided by ASD:**

- **Manage AWS Projects**: Easily switch between your AWS projects and manage them directly from your terminal.
- **SSO Sessions**: Handle your SSO sessions without leaving your terminal.
- **User-Friendly Interface**: ASD provides a clean and intuitive interface that makes managing your AWS projects a breeze.

**Press any button to continue...**

For more information, please visit the [GitHub repo](https://github.com/aphexlog/aws-stuff-doer).
"""


class WelcomeScreen(Screen):  # type: ignore
    """A simple welcome screen."""

    CSS_PATH = "welcome_screen.css"

    def compose(self) -> ComposeResult:
        yield Header()
        yield Container(Static(Markdown(WELCOME_MD), id="text"), id="md")  # type: ignore
        yield Footer()
