from rich.text import Text

from textual.widget import Widget
from textual.events import Mount

class HeaderProfile(Widget):
    """Display the logged in AWS profile on the right of the header."""
    DEFAULT_CSS = """
    HeaderProfile {
        color: $text;
        text-opacity: 85%;
        content-align: right middle;
        dock: right;
        width: 25;
        padding: 0 1;
    }
    """
    profile: str | None = None

    def __init__(self):
        super().__init__()

    def update_profile(self, profile: str):
        """Set the profile to display."""
        HeaderProfile.profile = profile
        self.refresh()

    def render(self):
        """Update the header aws profile."""
        if HeaderProfile.profile is not None:
            text = f"Profile: {HeaderProfile.profile}"
        else:
            text = "Not logged in..."

        return Text(text, no_wrap=True, overflow="ellipsis")

class HeaderTitle(Widget):
    """Display the title / subtitle in the header."""

    DEFAULT_CSS = """
    HeaderTitle {
        content-align: center middle;
        width: 100%;
    }
    """

    text: str = ""
    """The main title text."""

    sub_text = ""
    """The sub-title text."""

    def render(self):
        """Render the title and sub-title.

        Returns:
            The value to render.
        """
        text = Text(self.text, no_wrap=True, overflow="ellipsis")
        if self.sub_text:
            text.append(" — ")
            text.append(self.sub_text, "dim")
        return text

class CustomHeader(Widget):
    DEFAULT_CSS = """
    CustomHeader {
        dock: top;
        width: 100%;
        background: $foreground 5%;
        color: $text;
        height: 1;
    }
    """

    def __init__(self,
                *,
                 name: str | None = None,
                 id: str | None = None,
                 classes: str | None = None,
                ):
        super().__init__(name=name, id=id, classes=classes)
        self.header_profile = HeaderProfile()

    def update_profile(self, profile: str):
        """Update the profile in the HeaderProfile widget."""
        self.header_profile.update_profile(profile)

    def compose(self):
        yield HeaderTitle()
        yield self.header_profile

    @property
    def screen_title(self) -> str:
        """The title that this header will display.

        This depends on [`Screen.title`][textual.screen.Screen.title] and [`App.title`][textual.app.App.title].
        """
        screen_title = self.screen.title
        title = screen_title if screen_title is not None else self.app.title
        return title

    @property
    def screen_sub_title(self) -> str:
        """The sub-title that this header will display.

        This depends on [`Screen.sub_title`][textual.screen.Screen.sub_title] and [`App.sub_title`][textual.app.App.sub_title].
        """
        screen_sub_title = self.screen.sub_title
        sub_title = (
            screen_sub_title if screen_sub_title is not None else self.app.sub_title
        )
        return sub_title

    def on_mount(self, _: Mount) -> None:
        """Handle the mount event."""
        def set_title() -> None:
            self.query_one(HeaderTitle).text = self.screen_title

        def set_sub_title(sub_title: str) -> None:
            self.query_one(HeaderTitle).sub_text = self.screen_sub_title

        self.watch(self.app, "title", set_title)
        self.watch(self.app, "sub_title", set_sub_title)
        self.watch(self.screen, "title", set_title)
        self.watch(self.screen, "sub_title", set_sub_title)