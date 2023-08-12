from pathlib import Path
import boto3
import webbrowser
import argparse
import os
import botocore.exceptions
import configparser
import cmd
import logging

# Logging configuration
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)


class AWSnapShell(cmd.Cmd):
    prompt = "(awsnap) "

    def do_open(self, profile):
        """Open AWS Console with a specific profile"""
        try:
            sso_url = get_sso_url_from_profile(profile)
            open_aws_console(profile, sso_url)
            logging.info(
                f"Successfully opened AWS console for profile {profile}"
            )
        except Exception as e:
            logging.error(
                f"Failed to open AWS console for profile {profile}: {str(e)}"
            )

    def do_login(self, profile):
        """Authenticate with AWS SSO"""
        authenticate_sso(profile)

    def do_list(self, args):
        """List available AWS profiles"""
        list_profiles()

    def do_exit(self, args):
        """Exit the interactive shell"""
        return True

    def default(self, args):
        print(f"Unknown command: {args} (type 'help' for available commands)")


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


def open_aws_console(profile, sso_url):
    try:
        session = boto3.Session(profile_name=profile)

        if not sso_credentials_exist(session):
            authenticate_sso(profile)
            if not sso_credentials_exist(session):
                raise Exception("SSO authentication failed")

        webbrowser.open(sso_url)
        logging.info(f"Opened AWS console for profile {profile}")

    except Exception as e:
        logging.error(
            f"Failed to open AWS console for profile {profile}: {str(e)}"
        )
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


def authenticate_sso(profile):
    try:
        client = boto3.client(
            "sso",
            profile_name=profile,
        )

        sso_start_url = get_sso_url_from_profile(profile)

        if not sso_start_url:
            raise ValueError(
                f"Failed to obtain SSO Start URL for profile {profile}"
            )

        client.start_sso_login(ssoStartUrl=sso_start_url)
        logging.info(f"Successfully authenticated SSO for profile {profile}")
        return True

    except Exception as e:
        logging.error(
            f"An error occurred during SSO authentication for profile {profile}: {str(e)}",
        )
        raise  # Raising exception to handle it at a higher level if needed


def get_sso_url_from_profile(profile):
    config = configparser.ConfigParser()
    config.read(f"{os.path.expanduser('~')}/.aws/config")

    sso_session = config.get(f"profile {profile}", "sso_session")
    sso_start_url = config.get(f"sso-session {sso_session}", "sso_start_url")

    return sso_start_url


def export_temporary_aws_credentials(profile):
    session = boto3.Session(profile_name=profile)
    credentials = session.get_credentials()
    access_key = credentials.access_key
    secret_key = credentials.secret_key
    session_token = credentials.token

    os.environ["AWS_ACCESS_KEY_ID"] = access_key
    os.environ["AWS_SECRET_ACCESS_KEY"] = secret_key
    os.environ["AWS_SESSION_TOKEN"] = session_token


def run_shell_command(profile, command):
    export_temporary_aws_credentials(profile)
    print(f"Running command for profile {profile}: {command}")
    os.system(command)


def main():
    parser = argparse.ArgumentParser(
        description="AWSnap: AWS SSO Utility",
    )
    parser.add_argument("-p", "--profile", help="AWS profile name")
    parser.add_argument(
        "-i",
        "--interactive",
        action="store_true",
        help="Enter interactive mode",
    )
    parser.add_argument(
        "command",
        nargs="*",
        help="Command followed by its arguments to run in the shell",
    )

    args = parser.parse_args()

    if args.interactive:
        AWSnapShell().cmdloop()
    elif args.command:
        shell_command = " ".join(args.command)
        run_shell_command(args.profile, shell_command)
    else:
        sso_url = get_sso_url_from_profile(args.profile)
        open_aws_console(args.profile, sso_url)


if __name__ == "__main__":
    main()
