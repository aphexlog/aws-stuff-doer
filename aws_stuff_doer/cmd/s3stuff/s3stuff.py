"""A Textual app to handle s3 bucket operations"""
import boto3
import logging
from mypy_boto3_s3 import S3Client
from mypy_boto3_s3.type_defs import ListObjectsV2OutputTypeDef

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Header, Footer, ListItem, ListView, Label, Input, RichLog

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logging.getLogger("botocore").setLevel(logging.ERROR)

client: S3Client = boto3.client("s3")  # type: ignore

class S3Manager:
    """Handles S3 Bucket Operations"""

    def list_buckets(self):
        try:
            response = client.list_buckets()
            return response
        except client.exceptions.ClientError as err:
            logging.error(f"Error listing buckets: {err}")
        return None

    def list_objects(self, bucket_name: str):
        try:
            response: ListObjectsV2OutputTypeDef = client.list_objects_v2(Bucket=bucket_name)
            return response
        except client.exceptions.ClientError as err:
            logging.error(f"Error listing objects in bucket {bucket_name}: {err}")
        return None

    def delete_bucket(self, bucket_name: str):
        try:
            response = client.delete_bucket(Bucket=bucket_name)
            return response
        except client.exceptions.ClientError as err:
            if err.response['Error']['Code'] == 'BucketNotEmpty':
                logging.info(f"Bucket {bucket_name} is not empty. Emptying it now...")
                self.empty_bucket(bucket_name)
                response = client.delete_bucket(Bucket=bucket_name)
                return response
            logging.error(f"Error deleting bucket {bucket_name}: {err}")
        return None

    def empty_bucket(self, bucket_name: str):
        paginator = client.get_paginator('list_object_versions')
        for page in paginator.paginate(Bucket=bucket_name):
            versions = page.get('Versions', []) + page.get('DeleteMarkers', [])
            for version in versions:
                client.delete_object(Bucket=bucket_name, Key=version['Key'], VersionId=version['VersionId'])

class S3App(App): # type: ignore
    """Textual App to handle S3 Bucket Operations"""
    CSS_PATH = "s3app.css"

    def __init__(self):
        super().__init__()
        self.confirm_delete_input = Input(placeholder="Confirm deletion (y/n)", name="confirm_delete")
        self.selected_bucket = None

    BINDINGS = [
        Binding("enter", "select_cursor", "Select", show=False),
        Binding("up", "cursor_up", "Cursor Up", show=False),
        Binding("down", "cursor_down", "Cursor Down", show=False),
        Binding("Q", "quit", "Quit"),
        Binding("D", "delete_bucket", "Delete Bucket"),
    ]

    def compose(self) -> ComposeResult:
        """Create children widgets for the app"""
        yield Header(show_clock=True, time_format="%H:%M:%S")
        yield ListView(classes="box")
        yield RichLog(classes="box", name="rich_log")
        yield Footer()

    def on_mount(self) -> None:
        """Event handler called when the app is mounted"""
        self.list_buckets()

    def list_buckets(self):
        """List all S3 buckets"""
        s3_manager = S3Manager()
        response = s3_manager.list_buckets()
        list_view = self.query_one(ListView)
        list_view.clear()  # Clear the list view first
        if response is not None:
            buckets = response.get("Buckets", [])
            for bucket in buckets:
                bucket_name = bucket.get("Name", "")
                list_item = ListItem(Label(bucket_name))
                list_view.append(list_item)
        else:
            self.log_to_rich("Failed to retrieve buckets", level="error")
            list_item = ListItem(Label("Failed to retrieve buckets"))
            list_view.append(list_item)

    def action_select_cursor(self) -> None:
        """Event handler for selecting an item"""
        list_view = self.query_one(ListView)
        selected_item = list_view.index
        if selected_item is not None:
            selected_bucket = list_view.children[selected_item].children[0].render()
            self.log_to_rich(f"Selected bucket: {selected_bucket}", level="info")
            # self.list_objects(selected_bucket)
        else:
            self.log_to_rich("No bucket selected", level="error")

    def action_delete_bucket(self) -> None:
        """Delete the selected bucket"""
        list_view = self.query_one(ListView)
        selected_item = list_view.index
        if selected_item is not None:
            self.selected_bucket = list_view.children[selected_item].children[0].render()
            self.log_to_rich(f"Attempting to delete bucket: {self.selected_bucket}", level="info")
            if not self.query("Input"):
                self.mount(self.confirm_delete_input)
            self.set_focus(self.confirm_delete_input)

    async def on_input_submitted(self, message: Input.Submitted) -> None:
        """Handle the input confirmation for deletion"""
        if message.input.name == "confirm_delete":
            confirm_input = self.query_one(Input)
            if confirm_input.value.lower() == "y":
                s3_manager = S3Manager()
                response = s3_manager.delete_bucket(str(self.selected_bucket))
                if response is not None:
                    self.log_to_rich(f"Deleted bucket: {self.selected_bucket}", level="info")
                    self.list_buckets()
                else:
                    self.log_to_rich(f"Failed to delete bucket: {self.selected_bucket}", level="error")
            else:
                self.log_to_rich("Deletion canceled", level="info")
            await confirm_input.remove()
            self.set_focus(self.query_one(ListView))

    def log_to_rich(self, message: str, level: str = "info"):
        """Log messages to the RichLog widget"""
        rich_log = self.query_one(RichLog)
        if level == "info":
            rich_log.write(f"[INFO] {message}")
        elif level == "error":
            rich_log.write(f"[ERROR] {message}")
        elif level == "warning":
            rich_log.write(f"[WARNING] {message}")
        else:
            rich_log.write(f"[LOG] {message}")
