import os
import shutil
import platform
from typing import Optional
import subprocess
from pathlib import Path
import boto3
import logging
import configparser
from botocore.exceptions import TokenRetrievalError

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname=s - %(message)s",
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
        self.client = self.session.client("sts")  # type: ignore

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
            logging.error(f"SSO authentication error for profile {self.profile}: {err}")
        except Exception as err:
            if err.__class__.__name__ == "FileNotFoundError":
                logging.error("AWS CLI v2 is required for SSO authentication.")
                self.install_aws_cli_v2()
                logging.info("AWS CLI v2 has been installed.")
                return False
            logging.error(f"SSO authentication error for profile {self.profile}: {err}")
        return False

    def install_aws_cli_v2(self) -> None:
        """Install AWS CLI v2 using the official installer."""
        os_name = platform.system()

        try:
            # Create a temp dir to install this.
            os.mkdir("./tmp_aws_cli")

            if os_name == "Darwin":
                # Download the AWS CLI package into the temporary directory
                subprocess.run(["curl", "https://awscli.amazonaws.com/AWSCLIV2.pkg", "-o", "./tmp_aws_cli/AWSCLIV2.pkg"])

                # Install AWS CLI
                subprocess.run(["sudo", "installer", "-pkg", "./tmp_aws_cli/AWSCLIV2.pkg", "-target", "/"])
            elif os_name == "Linux":
                # Download the AWS CLI package into the temporary directory
                subprocess.run(["curl", "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip", "-o", "./tmp_aws_cli/awscliv2.zip"])

                # Install AWS CLI
                subprocess.run(["unzip", "./tmp_aws_cli/awscliv2.zip", "-d", "./tmp_aws_cli"])
                subprocess.run(["sudo", "./tmp_aws_cli/aws/install"])
            elif os_name == "Windows":
                # Download the AWS CLI package into the temporary directory
                subprocess.run(["curl", "https://awscli.amazonaws.com/AWSCLIV2.msi", "-o", "./tmp_aws_cli/AWSCLIV2.msi"])

                # Install AWS CLI
                subprocess.run(["msiexec", "/i", "./tmp_aws_cli/AWSCLIV2.msi", "/quiet"])
            else:
                logging.error(f"Unsupported OS: {os_name}")

                shutil.rmtree("./tmp_aws_cli")
        except Exception as err:
            logging.error(f"Failed to install AWS CLI v2: {err}")

    def get_sso_url_from_profile(self) -> Optional[str]:
        """Get the SSO start URL from the AWS profile configuration."""
        config = configparser.ConfigParser()
        if self.config_path.exists():
            config.read(self.config_path)
            try:
                sso_session = config.get(f"profile {self.profile}", "sso_session")
                sso_start_url = config.get(f"sso-session {sso_session}", "sso_start_url")
                return sso_start_url
            except configparser.NoSectionError:
                logging.error("Could not find the necessary SSO configuration.")
                return None
        return None

    def get_account_url_from_profile(self) -> Optional[str]:
        """Get the account URL from the AWS profile configuration."""
        config = configparser.ConfigParser()
        if self.config_path.exists():
            config.read(self.config_path)
            try:
                profile_section = f"profile {self.profile}"
                account_id = config.get(profile_section, "sso_account_id")
                role_name = config.get(profile_section, "sso_role_name")
                sso_start_url = self.get_sso_url_from_profile()
                account_url = f"{sso_start_url}/#/console?account_id={account_id}&role_name={role_name}"
                return account_url
            except configparser.NoSectionError:
                logging.error("Could not find the necessary account configuration.")
                return None
        return None

    def export_temporary_aws_credentials(self) -> bool:
        """Export temporary AWS credentials to the default profile in ~/.aws/credentials."""
        try:
            session = boto3.Session(profile_name=self.profile)
            credentials = session.get_credentials().get_frozen_credentials()  # type: ignore

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

            logging.info("Temporary AWS credentials written to the default profile in ~/.aws/credentials")
            return True
        except Exception as err:
            logging.error(f"Failed to export temporary AWS credentials: {err}")
            return False

    def open_aws_sso_console(self) -> None:
        """Open the AWS Management Console in the default web browser."""
        try:
            sso_start_url = self.get_sso_url_from_profile()
            if sso_start_url:
                subprocess.run(["open", sso_start_url])
        except Exception as err:
            logging.error(f"Failed to open the AWS Management Console: {err}")

    def open_aws_account_console(self) -> None:
        """Open the AWS Management Console in the default web browser."""
        try:
            account_url = self.get_account_url_from_profile()
            if account_url:
                subprocess.run(["open", account_url])
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
