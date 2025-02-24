import logging
from typing import Optional

import typer
import boto3
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
    editor: str = typer.Option("vim", help="Editor to open the config file"),
):
    """Manage AWS SSO and AWS CLI profiles"""
    configurator = AWSConfigManager()

    if sso:
        configurator.configure_sso()
    elif session:
        configurator.configure_session()
    elif fmt:
        configurator.fmt()
    if not any([sso, session, fmt]):
        # open config witch vim by default if none provided or any other editor
        configurator.open_config_file(editor)
    else:
        typer.echo("Please provide a valid option")
        typer.echo("Run 'asd config --help' for more information")
        raise typer.Exit(1)


@app.command(name="auth")
def authenticate(
    profile: str = typer.Option(..., "-p", "--profile", help="AWS profile name"),
):
    """Authenticate with AWS SSO"""
    try:
        authenticator = AWSAuthenticator(profile)
        authenticator.authenticate_sso()
    except ProfileNotFound as err:
        logging.error(f"Profile not found: {err}")
        raise typer.Exit(1)
    except Exception as err:
        logging.error(f"Failed to authenticate: {err}")
        raise typer.Exit(1)

open_app = typer.Typer(help="Open AWS Console interfaces")
app.add_typer(open_app, name="open")

@open_app.command(name="sso")
def open_sso():
    """Open AWS SSO user console"""
    try:
        # Use default profile if exists, or ask user to specify
        profiles = AWSAuthenticator.list_profiles()
        profile = profiles[0] if profiles else typer.prompt("Enter AWS profile name")
        authenticator = AWSAuthenticator(profile)
        authenticator.open_aws_sso_console()
    except Exception as err:
        logging.error(f"Failed to open SSO console: {err}")
        raise typer.Exit(1)

@open_app.command(name="console")
def open_console(
    service: Optional[str] = typer.Argument(None, help="Service to open in console"),
    profile: Optional[str] = typer.Option(None, "-p", "--profile", help="AWS profile name"),
):
    """Open AWS Console or specific service console"""
    try:
        # Use default profile if exists, or ask user to specify
        if not profile:
            profiles = AWSAuthenticator.list_profiles()
            profile = profiles[0] if profiles else typer.prompt("Enter AWS profile name")
        
        authenticator = AWSAuthenticator(profile)
        if service:
            authenticator.open_aws_service_console(service)
        else:
            authenticator.open_aws_account_console()
    except Exception as err:
        logging.error(f"Failed to open console: {err}")
        raise typer.Exit(1)


@app.command(name="s3")
def s3_operations():
    """Perform S3 bucket operations"""
    ui = s3stuff.S3App()
    ui.run()


@app.command(name="services")
def list_services(
    all: bool = typer.Option(False, "-a", "--all", help="Show all available AWS services")
):
    """List AWS services. By default shows only configured services."""
    # Get our mappings
    console_paths = AWSAuthenticator.CONSOLE_PATHS
    
    print("Available AWS services:")
    print("\nConfigured Services (with console paths):")
    for service in sorted(console_paths.keys()):
        path = console_paths[service]
        # Only show services with simple paths (no # or complex routing)
        if '#' not in path and '/' not in path:
            print(f"  {service} -> {path}")
    
    if all:
        # Get list of valid services from boto3
        valid_services = boto3.Session().get_available_services()
        print("\nAll Available Services:")
        for service in sorted(valid_services):
            if service not in console_paths:
                print(f"  {service} (console path not configured)")


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
