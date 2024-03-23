import argparse
import logging
from app.get_version import get_version
from app.services.login import AWSAuthenticator
# from app.services.open import open_aws_console

from app.ui import App

def get_profiles():
    return AWSAuthenticator.list_profiles()

PROFILES: list[str] = get_profiles()

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
    elif args.list:
        print("Available AWS profiles:")
        for profile in PROFILES:
            print(profile)
    elif args.profile:
        # login to AWS SSO
        authenticator = AWSAuthenticator(args.profile)
        if not authenticator.sso_credentials_exist():
            authenticator.authenticate_sso()
    else:
        parser.print_help()
