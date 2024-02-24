"""The login functionality for the aws_stuff_doer"""

# this package should enable users to login to AWS SSO and take the profile as an argument to the funtion
import subprocess
from pathlib import Path
import boto3
import logging
import botocore.exceptions
import configparser


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# Set logging level for botocore to ERROR to suppress stack traces
logging.getLogger("botocore").setLevel(logging.ERROR)


def sso_credentials_exist(session):
    try:
        session.client("sts").get_caller_identity()
        return True
    except (
        botocore.exceptions.BotoCoreError,
        botocore.exceptions.ClientError,
    ):
        return False


def authenticate_sso(profile):
    try:
        command = [
            "aws",
            "sso",
            "login",
            "--profile",
            profile,
        ]
        subprocess.run(command, check=True)

        logging.info(f"Successfully authenticated SSO for profile {profile}")
        return True
    except subprocess.CalledProcessError as err:
        logging.error(
            f"An error occurred during SSO authentication for profile {profile}: {err}"  # noqa
        )
        return False
    except Exception as err:
        logging.error(
            f"An error occurred during SSO authentication for profile {profile}: {err}"  # noqa
        )
        return False


def get_sso_url_from_profile(profile):
    config = configparser.ConfigParser()
    config_path = Path.home() / ".aws" / "config"

    sso_session = config.get(f"profile {profile}", "sso_session")
    sso_start_url = config.get(f"sso-session {sso_session}", "sso_start_url")
    region = config.get(
        f"profile {profile}", "region", fallback=None
    )  # Fetching the region

    return sso_start_url, region


def export_temporary_aws_credentials(profile):
    try:
        session = boto3.Session(profile_name=profile)
        credentials = session.get_credentials()
        access_key = credentials.access_key
        secret_key = credentials.secret_key
        session_token = credentials.token

        credentials_path = Path.home() / ".aws" / "credentials"
        config = configparser.ConfigParser()

        # Read existing credentials if they exist
        if credentials_path.exists():
            config.read(credentials_path)

        if "default" not in config.sections():
            config.add_section("default")

        config.set("default", "aws_access_key_id", access_key)
        config.set("default", "aws_secret_access_key", secret_key)
        config.set("default", "aws_session_token", session_token)

        with open(credentials_path, "w") as f:
            config.write(f)

        logging.info(
            "Temporary AWS credentials have been written to the default profile in ~/.aws/credentials"  # noqa
        )
        return True  # Ensure to return True after successful execution
    except Exception as err:
        logging.error(f"Failed to export temporary AWS credentials: {err}")
        return False


def list_profiles():
    config_path = Path.home() / ".aws" / "config"
    config = configparser.ConfigParser()
    config.read(config_path)

    profiles = [
        section.replace("profile ", "")
        for section in config.sections()
        if section.startswith("profile ")
    ]

    print("Available Profiles:")
    for profile in profiles:
        print(f"  - {profile}")
