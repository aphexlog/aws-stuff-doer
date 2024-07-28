"""A Textual app to handle s3 bucket operations"""
import boto3
import logging
from mypy_boto3_s3 import S3Client
from mypy_boto3_s3.type_defs import ListObjectsV2OutputTypeDef

# from textual import on
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Header, Footer, ListItem, ListView, Label, Input, RichLog, SelectionList, OptionList

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logging.getLogger("botocore").setLevel(logging.ERROR)

client: S3Client = boto3.client("s3")  # type: ignore

class RichLogger:
    def __init__(self, rich_log: RichLog):
        self.rich_log = rich_log

    def info(self, message: str):
        self.rich_log.write(f"[INFO] {message}")

    def error(self, message: str):
        self.rich_log.write(f"[ERROR] {message}")

    def warning(self, message: str):
        self.rich_log.write(f"[WARNING] {message}")

class S3App(App): # type: ignore
    """Textual App to handle S3 Bucket Operations"""
    CSS_PATH = "s3app.css"

    def __init__(self):
        super().__init__()
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
        self.rich_logger = RichLogger(self.query_one(RichLog))
        self.list_buckets()
        self.query_one(RichLog).visible = True  # Ensure RichLog is visible
        self.set_focus(self.query_one(ListView))  # Set initial focus to

    def list_buckets(self):
        """List all S3 buckets"""
        try:
            response = client.list_buckets()
            list_view = self.query_one(ListView)
            list_view.clear()  # Clear the list view first
            buckets = response.get("Buckets", [])
            for bucket in buckets:
                bucket_name = bucket.get("Name", "")
                bucket_date = bucket.get("CreationDate", "")
                list_item = ListItem(
                    Label(f"{bucket_name} - {bucket_date}", classes="bucket-info"),
                    classes="bucket-item",
                )
                list_view.append(list_item)
        except client.exceptions.ClientError as err:
            self.rich_logger.error(f"Error listing buckets: {err}")

    def list_objects(self, bucket_name: str):
        """List objects in a specific S3 bucket"""
        try:
            response: ListObjectsV2OutputTypeDef = client.list_objects_v2(Bucket=bucket_name)
            return response
        except client.exceptions.ClientError as err:
            self.rich_logger.error(f"Error listing objects in bucket {bucket_name}: {err}")
        return None

    def delete_bucket(self, bucket_name: str):
        """Delete a specific S3 bucket"""
        try:
            response = client.delete_bucket(Bucket=bucket_name)
            return response
        except client.exceptions.ClientError as err:
            if err.response['Error']['Code'] == 'BucketNotEmpty':
                self.rich_logger.info(f"Bucket {bucket_name} is not empty. Emptying it now...")
                self.empty_bucket(bucket_name)
                self.rich_logger.info(f"Finished emptying bucket {bucket_name}. Attempting to delete again...")
                try:
                    response = client.delete_bucket(Bucket=bucket_name)
                    return response
                except client.exceptions.ClientError as err:
                    self.rich_logger.error(f"Error deleting bucket {bucket_name}: {err}")
            else:
                self.rich_logger.error(f"Error deleting bucket {bucket_name}: {err}")
        return None

    def empty_bucket(self, bucket_name: str):
        """Empty a specific S3 bucket"""
        paginator = client.get_paginator('list_object_versions')
        for page in paginator.paginate(Bucket=bucket_name):
            versions = page.get('Versions', []) + page.get('DeleteMarkers', [])
            for version in versions:
                client.delete_object(Bucket=bucket_name, Key=version['Key'], VersionId=version['VersionId'])

    def action_select_cursor(self) -> None:
        """Event handler for selecting an item"""
        list_view = self.query_one(ListView)
        selected_item = list_view.index
        if selected_item is not None:
            selected_bucket = list_view.children[selected_item].children[0].render()
            self.rich_logger.info(f"Selected bucket: {selected_bucket}")
        else:
            self.rich_logger.error("No bucket selected")

    def action_delete_bucket(self) -> None:
        """Delete the selected bucket"""
        list_view = self.query_one(ListView)
        selected_item = list_view.index
        if selected_item is not None:
            self.selected_bucket = list_view.children[selected_item].children[0].render()
            self.rich_logger.info(f"Attempting to delete bucket: {self.selected_bucket}")
            self.mount(Input(name="confirm_delete", id="terminal", classes="box"))
            self.set_focus(self.query_one(Input))
            self.query_one(Input).value = ""
            self.query_one(Input).placeholder = "Type 'y' to confirm deletion"
        else:
            self.rich_logger.error("No bucket selected")

    async def on_input_submitted(self, message: Input.Submitted) -> None:
        """Handle the input confirmation for deletion"""
        if message.input.name == "confirm_delete":
            confirm_input = self.query_one(Input)
            if confirm_input.value.lower() == "y":
                response = self.delete_bucket(str(self.selected_bucket))
                if response is not None:
                    self.rich_logger.info(f"Deleted bucket: {self.selected_bucket}")
                    self.list_buckets()
                else:
                    self.rich_logger.error(f"Failed to delete bucket: {self.selected_bucket}")
            else:
                self.rich_logger.info("Deletion canceled")
            await confirm_input.remove()
            self.set_focus(self.query_one(ListView))

if __name__ == "__main__":
    S3App().run()
