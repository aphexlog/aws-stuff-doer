import logging

import typer
from botocore.exceptions import ProfileNotFound

from .cmd.config import AWSConfigManager
from .cmd.get_version import get_version
from .cmd.login import AWSAuthenticator
from .cmd.s3stuff import s3stuff

app = typer.Typer(
    help="ASD: An AWS Utility to help manage AWS SSO and AWS CLI profiles"
)


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    logging.getLogger("botocore").setLevel(logging.ERROR)


@app.command(name="list")
def list_profiles():
    """List available AWS profiles"""
    profiles = AWSAuthenticator.list_profiles()
    print("Available AWS profiles:")
    for profile in profiles:
        print(profile)


@app.command(name="config")
def configure():
    """Manage AWS SSO and AWS CLI profiles"""
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


@app.command(name="auth")
def authenticate(
    profile: str = typer.Option(..., "-p", "--profile", help="AWS profile name"),
    open_sso: bool = typer.Option(
        False, "--open-sso", help="Open AWS SSO user console"
    ),
    open_console: bool = typer.Option(False, "--open", help="Open AWS account console"),
):
    """Authenticate with AWS SSO or open consoles"""
    try:
        authenticator = AWSAuthenticator(profile)

        if open_console:
            authenticator.open_aws_account_console()
        elif open_sso:
            authenticator.open_aws_sso_console()
        else:
            authenticator.authenticate_sso()

    except ProfileNotFound as err:
        logging.error(f"Profile not found: {err}")
        raise typer.Exit(1)
    except Exception as err:
        logging.error(f"Failed to authenticate: {err}")
        raise typer.Exit(1)


@app.command(name="s3")
def s3_operations():
    """Perform S3 bucket operations"""
    ui = s3stuff.S3App()
    ui.run()


@app.callback()
def main(
    version: bool = typer.Option(False, "--version", help="Show version and exit"),
):
    """Main callback to handle version and logging setup"""
    if version:
        typer.echo(f"aws-stuff-doer {get_version()}")
        # raise typer.Exit()
    setup_logging()


if __name__ == "__main__":
    app()
