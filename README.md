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
asd [-h] [-p PROFILE] [--open-sso] [--open] [-l] [--version] [command ...]
```

**ASD**: The AWS Utility to manage AWS SSO and AWS CLI profiles conveniently.

### Positional Arguments:
- **command**: Command followed by its arguments to run in the shell

### Options:
- **-h, --help**: Show this help message and exit
- **-p PROFILE, --profile PROFILE**: Specify AWS profile name
- **--open-sso**: Open AWS SSO user console
- **--open**: Open AWS account console
- **-l, --list**: List available profiles
- **--version**: Show program's version number and exit
