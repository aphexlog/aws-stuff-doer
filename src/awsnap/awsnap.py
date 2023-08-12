import boto3
import webbrowser
import argparse
import os
import botocore.exceptions
import configparser
import cmd
import logging


class AWSnapShell(cmd.Cmd):
    prompt = "(awsnap) "

    def do_open(self, profile):
        """Open AWS Console with a specific profile"""
        sso_url = get_sso_url_from_profile(profile)
        open_aws_console(profile, sso_url)

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
    config_path = os.path.expanduser("~/.aws/config")
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
    session = boto3.Session(profile_name=profile)

    # Check if SSO credentials are needed
    if not sso_credentials_exist(session):
        authenticate_sso(profile)
        if not sso_credentials_exist(session):
            raise Exception("SSO authentication failed")

    # Open the URL with the obtained credentials
    webbrowser.open(sso_url)


def sso_credentials_exist(session):
    try:
        # This call will raise an exception if the credentials are not available
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
            "sso", region_name="region-name", profile_name=profile
        )

        # Assuming you have obtained the SSO Start URL
        sso_start_url = get_sso_url_from_profile(profile)

        # Ensure the SSO Start URL is valid
        if not sso_start_url:
            logging.error(
                "Failed to obtain SSO Start URL for profile %s", profile
            )
            return False

        client.start_sso_login(ssoStartUrl=sso_start_url)
        return True

    except Exception as e:
        logging.error(
            "An error occurred during SSO authentication for profile %s: %s",
            profile,
            str(e),
        )
        return False


def get_sso_url_from_profile(profile):
    config = configparser.ConfigParser()
    config.read(f"{os.path.expanduser('~')}/.aws/config")

    sso_session = config.get(f"profile {profile}", "sso_session")
    sso_start_url = config.get(f"sso-session {sso_session}", "sso_start_url")

    return sso_start_url


def export_temporary_aws_credentials(profile):
    session = boto3.Session(profile_name=profile)

    # Fetch temporary credentials
    credentials = session.get_credentials()
    access_key = credentials.access_key
    secret_key = credentials.secret_key
    session_token = credentials.token

    # Export them as environment variables
    os.environ["AWS_ACCESS_KEY_ID"] = access_key
    os.environ["AWS_SECRET_ACCESS_KEY"] = secret_key
    os.environ["AWS_SESSION_TOKEN"] = session_token


def run_shell_command(profile, command):
    # Export temporary AWS credentials for the profile
    export_temporary_aws_credentials(profile)

    # Run the command
    print(f"Running command for profile {profile}: {command}")
    os.system(command)


def main():
    parser = argparse.ArgumentParser(
        description="AWSnap: Open AWS Console with Profile or Enter Interactive Mode or Run a Custom Shell Command"
    )
    parser.add_argument(
        "-p", "--profile", help="AWS profile name", required=True
    )
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
