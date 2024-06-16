import argparse
import logging
from .cmd.get_version import get_version
from .cmd.login import AWSAuthenticator
from .cmd.config import AWSConfigManager

def get_profiles():
    return AWSAuthenticator.list_profiles()

PROFILES: list[str] = get_profiles()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logging.getLogger("botocore").setLevel(logging.ERROR)

def main():
    parser = argparse.ArgumentParser(
        description="ASD: An AWS Utility to help manage AWS SSO and AWS CLI profiles"
    )
    parser.add_argument(
        "-p", "--profile",
        help="AWS profile name"
    )
    parser.add_argument(
        "--open-sso",
        action="store_true",
        help="Open AWS SSO user console"
    )
    parser.add_argument(
        "--open",
        action="store_true",
        help="Open AWS account console"
    )
    parser.add_argument(
        "-l", "--list",
        action="store_true",
        help="List available profiles"
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {get_version()}"
    )
    parser.add_argument(
        "--config",
        action="store_true",
        help="Manage AWS SSO and AWS CLI profiles"
    )

    args = parser.parse_args()

    if not any(vars(args).values()):
        parser.print_help()
        return

    if args.list:
        print("Available AWS profiles:")
        for profile in PROFILES:
            print(profile)
        return

    if args.config:
        configurator = AWSConfigManager()
        print("AWS SSO and CLI Profile Configuration")
        print("1. Set up AWS SSO Profile")
        print("2. Initialize AWS SSO Session")
        print("3. Reformat AWS CLI Configuration File")

        choice = input("Enter choice: ")

        if choice == "1":
            configurator.configure_sso()
        elif choice == "2":
            configurator.configure_session()
        elif choice == "3":
            configurator.fmt()
        return

    if args.profile:
        authenticator = AWSAuthenticator(args.profile)

        if args.open:
            authenticator.open_aws_account_console()

        if args.open_sso:
            authenticator.open_aws_sso_console()

        if not args.open and not args.open_sso:
            authenticator.authenticate_sso()

if __name__ == "__main__":
    main()
