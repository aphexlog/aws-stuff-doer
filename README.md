# aws-stuff-doer: An Interactive CLI to Manage Your AWS Projects and SSO Sessions

[![PyPI version](https://badge.fury.io/py/aws-stuff-doer.svg)](https://badge.fury.io/py/aws-stuff-doer)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**AWS Stuff Doer (ASD)** is your go-to tool for managing AWS Single Sign-On (SSO). Designed for both developers and administrators, ASD simplifies your AWS SSO workflow, allowing you to run custom shell commands with specific profiles and export temporary AWS credentials seamlessly.

## Features

- **Easy Integration**: Effortlessly integrate with your existing AWS infrastructure.
- **Secure Authentication**: Improve security with robust SSO capabilities.
- **Customizable**: Tailor ASD to meet your unique requirements.
- **Run Custom Commands**: Execute shell commands using AWS profiles and export temporary credentials securely in memory.
- **Temporary AWS Credentials**: Access temporary AWS credentials specific to a profile, securely available in memory.

## Installation

Install ASD using pip:

```bash
pip install aws-stuff-doer
```

## Usage

Invoke ASD with the following command syntax:

```bash
asd [OPTIONS] COMMAND [ARGS]...
```

**ASD**: The AWS Utility to manage AWS SSO and AWS CLI profiles conveniently.

<!-- here is what prints when you run the help command, use it as context: -->
<!-- ❯ asd --help -->
                                                                                                                                                                                                                                           
<!--  Usage: asd [OPTIONS] COMMAND [ARGS]... -->                                                                                                                                                                                                    
                                                                                                                                                                                                                                           
<!--  ASD: An AWS Utility to help manage AWS SSO and AWS CLI profiles -->                                                                                                                                                                           
                                                                                                                                                                                                                                           
<!-- ╭─ Options ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮ -->
<!-- │ --version             -v        Show version and exit                                                                                                                                                                                   │ -->
<!-- │ --install-completion            Install completion for the current shell.                                                                                                                                                               │ -->
<!-- │ --show-completion               Show completion for the current shell, to copy it or customize the installation.                                                                                                                        │ -->
<!-- │ --help                          Show this message and exit.                                                                                                                                                                             │ -->
<!-- ╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯ -->
<!-- ╭─ Commands ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮ -->
<!-- │ list     List available AWS profiles                                                                                                                                                                                                    │ -->
<!-- │ config   Manage AWS SSO and AWS CLI profiles                                                                                                                                                                                            │ -->
<!-- │ auth     Authenticate with AWS SSO or open consoles                                                                                                                                                                                     │ -->
<!-- │ s3       Perform S3 bucket operations                                                                                                                                                                                                   │ -->
<!-- ╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯ -->


### Positional Arguments:
- **COMMAND**: The command to execute
- **ARGS**: Additional arguments for the command
- **OPTIONS**: Additional options for the command

### Commands:
- **list**: List available AWS profiles
- **config**: Manage AWS SSO and AWS CLI profiles
- **auth**: Authenticate with AWS SSO or open consoles
- **s3**: Perform S3 bucket operations

### Options:
- **--version, -v**: Show version and exit
- **--install-completion**: Install completion for the current shell
- **--show-completion**: Show completion for the current shell, to copy it or customize the installation
- **--help**: Show this message and exit

## Examples
- **List available AWS profiles**:
```bash
asd list
```

- **Manage AWS SSO and AWS CLI profiles**:
```bash
asd config
```

- **Authenticate with AWS SSO or open consoles**:
```bash
asd auth
```

- **Perform S3 bucket operations**:
```bash
asd s3
```

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
