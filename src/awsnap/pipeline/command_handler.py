import hashlib
from git import Repo, InvalidGitRepositoryError
from .cloudformation import create_pipeline, delete_pipeline
from boto3 import Session

import logging


def get_git_repo_info():
    try:
        repo = Repo(search_parent_directories=True)
        branch = repo.active_branch.name
        remote_url = repo.remotes.origin.url
        return remote_url, branch
    except InvalidGitRepositoryError:
        logging.error("Could not find a valid Git repository.")
        return None, None


def generate_pipeline_name(repo_path):
    # Create a unique hash based on the repository's path
    hash_digest = hashlib.sha1(repo_path.encode()).hexdigest()[:8]
    return f"pipeline-{hash_digest}"


def handle_command(arg):
    """Handle command."""
    args = arg.split()
    subcommand = args[0]

    logging.info(f"Received command: {subcommand}")

    region = Session().region_name or "us-east-1"
    logging.info(f"Using region: {region}")

    if subcommand == "create":
        repo_url, branch = get_git_repo_info()
        if not repo_url or not branch:
            return

        # Use the repository's local path to generate a unique pipeline name
        repo = Repo(search_parent_directories=True)
        pipeline_name = generate_pipeline_name(repo.working_tree_dir)

        # Extract 'owner/repo' from URL
        repo_string = repo_url.split("/")[-1].replace(".git", "")
        owner = repo_url.split("/")[-2]
        repo_string = f"{owner}/{repo_string}"

        build_commands = ["cdk synth"]

        logging.info(
            f"Creating pipeline with name: {pipeline_name}, repo_string={repo_string}, branch={branch}"  # noqa: E501
        )
        create_pipeline(
            pipeline_name,
            repo_string,
            branch,
            build_commands,
            region=region,  # noqa: E501
        )

    elif subcommand == "delete":
        logging.info("Deleting pipeline")
        # For delete, use the generated pipeline name
        repo_path = Repo(search_parent_directories=True).working_tree_dir
        pipeline_name = generate_pipeline_name(repo_path)

        logging.info(f"Deleting pipeline with name: {pipeline_name}")
        delete_pipeline(pipeline_name, region=region)

    else:
        logging.error(f"Unknown command: {subcommand}")
        raise ValueError(f"Unknown command: {subcommand}")
