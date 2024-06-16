import configparser
from pathlib import Path
import boto3
from mypy_boto3_sts import STSClient
import logging

client: STSClient = boto3.client("sts")  # type: ignore

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logging.getLogger("botocore").setLevel(logging.ERROR)


class AWSConfigManager:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config_path = Path.home() / ".aws" / "config"

    def configure_sso(self):
        sso_profile = input("Enter SSO profile name: ")
        sso_session = input("Enter SSO session name: ")
        sso_account_id = input("Enter SSO account ID: ")
        sso_role_name = input("Enter SSO role name: ")
        region = input("Enter region: ")
        output = input("Enter output format: ")

        self.config[f"profile {sso_profile}"] = {
            "sso_session": sso_session,
            "sso_account_id": sso_account_id,
            "sso_role_name": sso_role_name,
            "region": region,
            "output": output,
        }

        with open(self.config_path, "a") as configfile:
            self.config.write(configfile)

        logging.info("AWS SSO profile configured successfully")

    def configure_session(self):
        sso_session = input("Enter SSO session name: ")
        sso_start_url = input("Enter SSO start URL: ")
        sso_region = input("Enter SSO region: ")
        sso_registration_scopes = input("Enter SSO registration scopes (default: sso:account:access): ") or "sso:account:access"

        self.config[f"sso-session {sso_session}"] = {
            "sso_start_url": sso_start_url,
            "sso_region": sso_region,
            "sso_registration_scopes": sso_registration_scopes,
        }

        with open(self.config_path, "a") as configfile:
            self.config.write(configfile)

        logging.info("AWS SSO session configured successfully")

    def fmt(self):
        """Reformat the config file"""
        self.config.read(self.config_path)
        for section in self.config.sections():
            if section.startswith("profile "):
                if "sso_start_url" in self.config[section]:
                    self.config.remove_option(section, "sso_start_url")
                if "sso_region" in self.config[section]:
                    self.config.remove_option(section, "sso_region")
                if "sso_registration_scopes" in self.config[section]:
                    self.config.remove_option(section, "sso_registration_scopes")
            if section.startswith("sso-session "):
                if "sso_account_id" in self.config[section]:
                    self.config.remove_option(section, "sso_account_id")
                if "sso_role_name" in self.config[section]:
                    self.config.remove_option(section, "sso_role_name")
                if "region" in self.config[section]:
                    self.config.remove_option(section, "region")
                if "output" in self.config[section]:
                    self.config.remove_option(section, "output")
        with open(self.config_path, "w") as configfile:
            self.config.write(configfile)
        logging.info("Config file formatted successfully")
