import boto3
import logging

from mypy_boto3_logs import CloudWatchLogsClient
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Header, Footer, ListView, RichLog, ListItem, Label, Input

from aws_stuff_doer.cmd.s3stuff.s3stuff import RichLogger


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logging.getLogger("botocore").setLevel(logging.ERROR)

client: CloudWatchLogsClient = boto3.client("logs")  # type: ignore


class CloudwatchApp(App): # type: ignore
    """Textual App to handle Cloudwatch Logging Operations"""
    CSS_PATH = "cloudwatchapp.css"

    def __init__(self):
        super().__init__()

    BINDINGS = [
        Binding("enter", "select_cursor", "Select", show=False),
        Binding("up", "cursor_up", "Cursor Up", show=False),
        Binding("down", "cursor_down", "Cursor Down", show=False),
        Binding("Q", "quit", "Quit"),
        Binding("D", "delete_log_group", "Delete Log Group"),
        Binding("S", "stream_log_group", "Stream Logs"),
    ]

    def compose(self) -> ComposeResult:
        """Create children widgets for the app"""
        yield Header(show_clock=True, time_format="%H:%M:%S")
        yield ListView(classes="box")
        yield RichLog(classes="box", name="rich_log")
        yield Footer()

    def on_mount(self) -> None:
        """Event handler called when the app is mounted"""
        self.rich_logger = RichLogger(self.query_one(RichLog))
        self.load_log_groups()
        self.query_one(RichLog).visible = True  # Ensure RichLog is visible
        self.set_focus(self.query_one(ListView))  # Set initial focus to

    def load_log_groups(self):
        try:
            paginator = client.get_paginator("describe_log_groups")
            list_view = self.query_one(ListView)
            list_view.clear()  # Clear the list view first
            for page in paginator.paginate():
                for log_group in page["logGroups"]:
                    log_group_name = log_group["logGroupName"]
                    list_item = ListItem(Label(f"{log_group_name}"), classes="log-group-item")
                    list_item.data = log_group_name  # Store the log group name in the data attribute
                    list_view.append(list_item)
        except Exception as e:
            self.rich_logger.error(f"Error listing log groups: {e}")

    def delete_log_group(self, log_group: str):
        """Delete a specific log group"""
        try:
            response = client.delete_log_group(logGroupName=log_group)
            return response
        except client.exceptions.ClientError as err:
            self.rich_logger.error(f"Error deleting log group {log_group}: {err}")
        return None

    def load_log_streams(self, log_group: str):
        """Stream logs from the selected log group"""
        try:
            log_stream_list = self.query_one(ListView)
            log_stream_list.clear()
            paginator = client.get_paginator("describe_log_streams")
            count = 0  # Initialize counter
            stream_limit = 50 # Limit the number of streams to 50
            for page in paginator.paginate(logGroupName=log_group, orderBy='LastEventTime'):
                for log_stream in page["logStreams"]:
                    if count >= stream_limit:
                        break
                    log_stream_name = log_stream["logStreamName"]
                    list_item = ListItem(Label(f"{log_stream_name}"), classes="log-stream-item")
                    list_item.data = log_stream_name  # Store the log stream name in the data attribute
                    log_stream_list.append(list_item)
                    count += 1
                    if count >= stream_limit:
                        break
        except Exception as e:
            self.rich_logger.error(f"Error streaming logs: {e}")

    def action_delete_log_group(self) -> None:
        """Delete the selected log group"""
        list_view = self.query_one(ListView)
        selected_item = list_view.index
        if selected_item is not None:
            selected_text = str(list_view.children[selected_item].children[0].render())
            self.rich_logger.info(f"Selected text: {selected_text}")
            self.selected_log_group: str = selected_text
            self.rich_logger.info(f"Attempting to delete log group: {self.selected_log_group}")
            self.mount(Input(name="confirm_delete", id="terminal", classes="box"))
            self.set_focus(self.query_one(Input))
            self.query_one(Input).value = ""
            self.query_one(Input).placeholder = "Type 'y' to confirm deletion"
        else:
            self.rich_logger.error("No log group selected")

    def action_stream_log_group(self) -> None:
        """Event handler for streaming the selected log group"""
        list_view = self.query_one(ListView)
        selected_item = list_view.index
        if selected_item is not None:
            if 0 <= selected_item < len(list_view.children):
                selected_group = list_view.children[selected_item]
                group_name = getattr(selected_group, 'data', 'Unknown Group')
                self.rich_logger.info(f"Streaming log group: {group_name}")
                self.load_log_streams(group_name)
            else:
                self.rich_logger.error(f"Selected item index {selected_item} is out of bounds")
        else:
            self.rich_logger.error("No log group selected")

    async def on_input_submitted(self, message: Input.Submitted) -> None:
        """Handle the input confirmation for deletion"""
        if message.input.name == "confirm_delete":
            confirm_input = self.query_one(Input)
            if confirm_input.value.lower() == "y":
                response = self.delete_log_group(str(self.selected_log_group))
                if response is not None:
                    self.rich_logger.info(f"Deleted log group: {self.selected_log_group}")
                    self.load_log_groups()
                else:
                    self.rich_logger.error(f"Failed to delete log group: {self.selected_log_group}")
            else:
                self.rich_logger.info("Deletion canceled")
            await confirm_input.remove()
            self.set_focus(self.query_one(ListView))

if __name__ == "__main__":
    CloudwatchApp().run()
