from typing import Optional
import subprocess
from pathlib import Path
import boto3
import logging
import configparser
from botocore.exceptions import TokenRetrievalError

# Configure logging as before
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logging.getLogger("botocore").setLevel(logging.ERROR)


class AWSAuthenticator:
    """Handles AWS SSO Authentication and Credential Management"""

    def __init__(self, profile: str):
        self.profile = profile
        self.config_path = Path.home() / ".aws" / "config"
        self.credentials_path = Path.home() / ".aws" / "credentials"
        self.session = boto3.Session(profile_name=profile)
        self.client = self.session.client("sts") # type: ignore

    def sso_credentials_exist(self) -> bool:
        try:
            self.client.get_caller_identity()
            return True
        except (self.client.exceptions.ClientError, TokenRetrievalError):
            return False

    def authenticate_sso(self) -> bool:
        """Authenticate SSO for the given profile."""
        if self.sso_credentials_exist():
            logging.info(f"Already authenticated SSO for profile {self.profile}")
            self.export_temporary_aws_credentials()
            return True
        try:
            command = ["aws", "sso", "login", "--profile", self.profile]
            subprocess.run(command, check=True)
            logging.info(f"Successfully authenticated SSO for profile {self.profile}")
            self.export_temporary_aws_credentials()
            return True
        except subprocess.CalledProcessError as err:
            logging.error(f"An error occurred during SSO authentication for profile {self.profile}: {err}")
        except Exception as err:
            logging.error(f"An error occurred during SSO authentication for profile {self.profile}: {err}")
        return False

    def get_sso_url_from_profile(self) -> Optional[str]:
        """Get the SSO start URL from the AWS profile configuration."""
        config = configparser.ConfigParser()
        if self.config_path.exists():
            config.read(self.config_path)
            try:
                sso_session = config.get(f"profile {self.profile}", "sso_session")
                sso_start_url = config.get(f"sso-session {sso_session}", "sso_start_url")
                print(sso_start_url)
                return sso_start_url
            except configparser.NoSectionError:
                logging.error("Could not find the necessary SSO configuration.")
                return None
        return None

    def export_temporary_aws_credentials(self) -> bool:
        """Export temporary AWS credentials to the default profile in ~/.aws/credentials."""
        try:
            session = boto3.Session(profile_name=self.profile)
            credentials = session.get_credentials().get_frozen_credentials() # type: ignore

            config = configparser.ConfigParser()
            if self.credentials_path.exists():
                config.read(self.credentials_path)
            if "default" not in config.sections():
                config.add_section("default")

            config.set("default", "aws_access_key_id", credentials.access_key)
            config.set("default", "aws_secret_access_key", credentials.secret_key)
            config.set("default", "aws_session_token", credentials.token)

            with open(self.credentials_path, "w") as f:
                config.write(f)

            logging.info("Temporary AWS credentials have been written to the default profile in ~/.aws/credentials")
            return True
        except Exception as err:
            logging.error(f"Failed to export temporary AWS credentials: {err}")
            return False

    def open_aws_console(self) -> None:
        """Open the AWS Management Console in the default web browser."""
        try:
            sso_start_url = self.get_sso_url_from_profile()
            if sso_start_url:
                subprocess.run(["open", sso_start_url])
        except Exception as err:
            logging.error(f"Failed to open the AWS Management Console: {err}")

    @classmethod
    def list_profiles(cls) -> list[str]:
        """List all AWS profiles in the ~/.aws/config file."""
        config_path = Path.home() / ".aws" / "config"
        config = configparser.ConfigParser()
        config.read(config_path)

        profiles = [
            section.replace("profile ", "")
            for section in config.sections()
            if section.startswith("profile ")
        ]
        return profiles
