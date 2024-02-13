# Rex: an inteactive CLI to help manage your AWS projects and sso sessions.

[![PyPI version](https://badge.fury.io/py/rex.svg)](https://badge.fury.io/py/rex)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

rex is a simple and effective tool for managing AWS Single Sign-On (SSO). Tailored for both developers and administrators, rex offers an easy way to streamline your AWS SSO process, including running custom shell commands with specific profiles and exporting temporary AWS credentials.

## Features

- **Easy Integration**: Seamlessly integrate with existing AWS infrastructure.
- **Secure Authentication**: Enhance security with robust SSO capabilities.
- **Customizable**: Extend and adapt rex to suit your specific needs.
- **Run Custom Commands**: Execute shell commands with AWS profiles and export temporary credentials in memory.
- **Temporary AWS Credentials**: Access temporary AWS credentials specific to a profile, securely available in memory.

## Installation

You can install rex via pip:

```bash
pip install rex
```

## Usage

Getting started with rex is easy:

To generate temporary AWS credentials for a specific profile:
```bash
rex -p <profile_name>
```
This will generate temporary AWS credentials for the specified profile and store them in the ~/.aws/credentials file.

To open your AWS console in a browser session:
```bash
rex <your_command_here> --profile <profile_name> --console
```

To get help:
```bash
rex --help
```
or
```bash
go see a therapist.
```

The project is available on [pypip](https://pypi.org/project/rex/).

## Contributing

Contributions are welcome! Check out the [issues](https://github.com/aphexlog/rex/issues) or submit a pull request.

## License

rex is released under the [MIT License](https://github.com/aphexlog/rex/blob/main/LICENSE).

---

Feel free to reach out with questions, suggestions, or just to say hello. Happy coding!

## Contact Information
- **Author**: Aaron West
- **Email**: aphexlog@gmail.com

---

Thank you for your interest in rex! Follow the project on [GitHub](https://github.com/aphexlog/rex) for the latest updates...
