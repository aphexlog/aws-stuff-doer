"""A Textual app to handle s3 bucket operations"""
import boto3
import logging
from typing import Optional
from mypy_boto3_s3 import S3Client
from mypy_boto3_s3.type_defs import ListObjectsV2OutputTypeDef

from textual.app import App, ComposeResult, Logger
from textual.widgets import Header, Footer, ListItem, ListView, Label

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

    # def __init__(self, bucket_name: str):
        # self.bucket_name = bucket_name

    def list_buckets(self):
        try:
            response = client.list_buckets()
            return response
        except client.exceptions.ClientError as err:
            logging.error(f"Error listing buckets: {err}")
        return None

class S3App(App): # type: ignore
    """Textual App to handle S3 Bucket Operations"""

    BINDINGS = [
        ("Q", "quit", "Quit"),
    ]

    def compose(self) -> ComposeResult:
        """Create children widgets for the app"""
        yield Header(show_clock=True, time_format="%H:%M:%S")
        yield ListView()
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
            logging.error("Failed to retrieve buckets")
            list_item = ListItem(Label("Failed to retrieve buckets"))
            list_view.append(list_item)


if __name__ == "__main__":
    S3App().run()
