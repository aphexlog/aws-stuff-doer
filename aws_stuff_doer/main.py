import logging

import typer
from botocore.exceptions import ProfileNotFound
import pkg_resources

from .cmd.config import AWSConfigManager
from .cmd.aws_auth import AWSAuthenticator
from .cmd.s3stuff import s3stuff


def get_version():
    package_name = "aws-stuff-doer"

    try:
        return pkg_resources.get_distribution(package_name).version
    except pkg_resources.DistributionNotFound:
        return "unknown"


app = typer.Typer(
    help="ASD: An AWS Utility to help manage AWS SSO and AWS CLI profiles",
    invoke_without_command=True,
    no_args_is_help=True,
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
def configure(
    sso: bool = typer.Option(False, help="Configure AWS SSO profile"),
    session: bool = typer.Option(False, help="Initialize AWS SSO session"),
    fmt: bool = typer.Option(False, help="Reformat AWS CLI configuration file"),
):
    """Manage AWS SSO and AWS CLI profiles"""
    configurator = AWSConfigManager()

    if sso:
        configurator.configure_sso()
    elif session:
        configurator.configure_session()
    elif fmt:
        configurator.fmt()
    else:
        typer.echo("Please provide a valid option")
        typer.echo("Run 'asd config --help' for more information")
        raise typer.Exit(1)


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


@app.callback(invoke_without_command=True)
def main(
    version: bool = typer.Option(
        False, "-v", "--version", help="Show version and exit", is_eager=True
    ),
    ctx: typer.Context = typer.Option(None),
):
    """Main callback to handle logging setup"""
    if version:
        typer.echo(f"aws-stuff-doer {get_version()}")
        raise typer.Exit()
    setup_logging()
