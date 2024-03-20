"""Open the AWS console for the specified profile."""

from typing import Tuple
import configparser
from pathlib import Path
import webbrowser
import boto3
import logging
import botocore.exceptions

from app.services.login import authenticate_sso


def get_sso_url_from_profile(profile) -> Tuple[str, str]:
    config = configparser.ConfigParser()
    config_path = Path.home() / ".aws" / "config"

    sso_session = config.get(f"profile {profile}", "sso_session")
    sso_start_url = config.get(f"sso-session {sso_session}", "sso_start_url")
    region = config.get(
        f"profile {profile}", "region", fallback=None
    )  # Fetching the region

    return sso_start_url, region


def open_aws_console(profile, sso_url):
    sso_url, region = get_sso_url_from_profile(profile)
    try:
        # Create the session with the region if available
        session = (
            boto3.Session(profile_name=profile, region_name=region)
            if region
            else boto3.Session(profile_name=profile)
        )

        if not sso_credentials_exist(session):
            authenticate_sso(profile)
            if not sso_credentials_exist(session):
                raise Exception("SSO authentication failed")

        webbrowser.open(sso_url)
        logging.info(f"Opened AWS console for profile {profile}")

    except Exception as err:
        logging.error(
            f"Failed to open AWS console for profile {profile}: {str(err)}"
        )  # noqa
        raise


def sso_credentials_exist(session):
    try:
        session.client("sts").get_caller_identity()
        return True
    except (
        botocore.exceptions.BotoCoreError,
        botocore.exceptions.ClientError,
    ):
        return False
