import boto3
import webbrowser
import argparse
import os
import botocore.exceptions
import configparser
import cmd


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
    os.system(f"aws sso login --profile {profile}")


def get_sso_url_from_profile(profile):
    config = configparser.ConfigParser()
    config.read(f"{os.path.expanduser('~')}/.aws/config")

    sso_session = config.get(f"profile {profile}", "sso_session")
    sso_start_url = config.get(f"sso-session {sso_session}", "sso_start_url")

    return sso_start_url


def main():
    parser = argparse.ArgumentParser(
        description="AWSnap: Open AWS Console with Profile or Enter Interactive Mode"
    )
    parser.add_argument("-p", "--profile", help="AWS profile name")
    parser.add_argument(
        "-i",
        "--interactive",
        action="store_true",
        help="Enter interactive mode",
    )

    args = parser.parse_args()

    if args.interactive:
        AWSnapShell().cmdloop()
    elif args.profile:
        sso_url = get_sso_url_from_profile(args.profile)
        open_aws_console(args.profile, sso_url)
    else:
        print(
            "Usage: Provide a profile (-p/--profile) or enter interactive mode (-i/--interactive)."
        )


if __name__ == "__main__":
    main()
