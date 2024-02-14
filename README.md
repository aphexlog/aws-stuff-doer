# aws-stuff-doer: an inteactive CLI to help manage your AWS projects and sso sessions.

[![PyPI version](https://badge.fury.io/py/aws-stuff-doer.svg)](https://badge.fury.io/py/aws-stuff-doer)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

ASD is a simple and effective tool for managing AWS Single Sign-On (SSO). Tailored for both developers and administrators, ASD offers an easy way to streamline your AWS SSO process, including running custom shell commands with specific profiles and exporting temporary AWS credentials.

## Features

- **Easy Integration**: Seamlessly integrate with existing AWS infrastructure.
- **Secure Authentication**: Enhance security with robust SSO capabilities.
- **Customizable**: Extend and adapt ASD to suit your specific needs.
- **Run Custom Commands**: Execute shell commands with AWS profiles and export temporary credentials in memory.
- **Temporary AWS Credentials**: Access temporary AWS credentials specific to a profile, securely available in memory.

## Installation

You can install ASD via pip:

```bash
pip install aws-stuff-doer
```
```

## Usage

Getting started with ASD is easy:

To generate temporary AWS credentials for a specific profile:
```bash
asd -p <profile_name>
```
This will generate temporary AWS credentials for the specified profile and store them in the ~/.aws/credentials file.

To open your AWS console in a browser session:
```bash
asd <your_command_here> --profile <profile_name> --console
```

To get help:
```bash
asd --help
```
or
```bash
go see a therapist.
```

The project is available on [pypip](https://pypi.org/project/aws-stuff-doer/).

## Contributing

Contributions are welcome! Check out the [issues](https://github.com/aphexlog/aws-stuff-doer/issues) or submit a pull request.

## License

aws-stuff-doer is released under the [MIT License](https://github.com/aphexlog/aws-stuff-doer/blob/main/LICENSE).

---

Feel free to reach out with questions, suggestions, or just to say hello. Happy coding!

## Contact Information
- **Author**: Aaron West
- **Email**: aphexlog@gmail.com

---

Thank you for your interest in aws-stuff-doer! Follow the project on [GitHub](https://github.com/aphexlog/aws-stuff-doer) for the latest updates...
