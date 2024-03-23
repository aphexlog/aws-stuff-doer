import argparse
import logging
from app.get_version import get_version

from app.ui import App

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# Set logging level for botocore to ERROR to suppress stack traces
logging.getLogger("botocore").setLevel(logging.ERROR)

def main():
    parser = argparse.ArgumentParser(
        description="ASD: An AWS Utility to help manage your projects and sso sessions.",
    )
    parser.add_argument("-p", "--profile", help="AWS profile name")
    parser.add_argument("--open", action="store_true", help="Open AWS console")  # noqa
    parser.add_argument(
        "-l",
        "--list",
        action="store_true",
        help="List available profiles",
    )
    parser.add_argument(
        "command",
        nargs="*",
        help="Command followed by its arguments to run in the shell",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {get_version()}",
    )

    args = parser.parse_args()

    if not any(vars(args).values()):
        app = App()
        app.run()
    else:
        parser.print_help()
