"""Help command for the AWS Stuff Doer CLI."""

from textual import events  # type: ignore
from textual.app import ComposeResult  # type: ignore
from textual.screen import Screen  # type: ignore
from textual.widgets import ListView, ListItem, Label, Footer  # type: ignore

from app.login import list_profiles  # type: ignore
from app.views.widgets import CustomHeade  # type: ignore
