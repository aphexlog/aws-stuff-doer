# commands/command_handler.py
from .cloudformation import create_pipeline, delete_pipeline
import logging

logging.basicConfig(level=logging.INFO)


def handle_command(arg):
    """Handle command."""
    args = arg.split()
    subcommand = args[0]

    logging.info(f"Received command: {subcommand}")

    if subcommand == "create":
        repo_string = "elevator-robot/awsnap"
        branch = "main"  # Default branch
        build_commands = [
            "npm install",
            "npm run build",
            "cdk synth",
        ]  # Default build commands
        logging.info(
            f"Creating pipeline with args: repo_string={repo_string}, branch={branch}, build_commands={build_commands}"  # noqa: E501
        )
        create_pipeline(repo_string, branch, build_commands)
    elif subcommand == "delete":
        stack_name = "MyPipelineStack"
        logging.info(f"Deleting pipeline with args: stack_name={stack_name}")
        delete_pipeline(stack_name)
    else:
        logging.error(f"Unknown command: {subcommand}")
        raise ValueError(f"Unknown command: {subcommand}")
