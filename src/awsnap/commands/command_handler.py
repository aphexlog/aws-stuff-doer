# commands/command_handler.py
from .create_command import create_pipeline
import logging

logging.basicConfig(level=logging.INFO)


def handle_command(arg):
    """Handle command."""
    args = arg.split()
    subcommand = args[0]

    logging.info(f"Received command: {subcommand}")

    if subcommand == "create":
        # Ensure you are passing the correct number of arguments to create_pipeline
        # For now, let's assume the repo_string is always "elevator-robot/awsnap" and the branch is "main"
        repo_string = "elevator-robot/awsnap"
        branch = "main"  # Default branch
        build_commands = [
            "npm install",
            "npm run build",
            "cdk synth",
        ]  # Default build commands
        logging.info(
            f"Creating pipeline with args: repo_string={repo_string}, branch={branch}, build_commands={build_commands}"
        )
        create_pipeline(repo_string, branch, build_commands)
    else:
        logging.error(f"Unknown command: {subcommand}")
        raise ValueError(f"Unknown command: {subcommand}")
