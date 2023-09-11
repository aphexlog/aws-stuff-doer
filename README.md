# AWSnap: AWS SSO Utility

[![PyPI version](https://badge.fury.io/py/awsnap.svg)](https://badge.fury.io/py/awsnap)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

AWSnap is a simple and effective tool for managing AWS Single Sign-On (SSO). Tailored for both developers and administrators, AWSnap offers an easy way to streamline your AWS SSO process, including running custom shell commands with specific profiles and exporting temporary AWS credentials.

## Features

- **Easy Integration**: Seamlessly integrate with existing AWS infrastructure.
- **Secure Authentication**: Enhance security with robust SSO capabilities.
- **Customizable**: Extend and adapt AWSnap to suit your specific needs.
- **Run Custom Commands**: Execute shell commands with AWS profiles and export temporary credentials in memory.
- **Temporary AWS Credentials**: Access temporary AWS credentials specific to a profile, securely available in memory.

## Installation

You can install AWSnap via pip:

```bash
pip install awsnap
```

## Usage

Getting started with AWSnap is easy:

To generate temporary AWS credentials for a specific profile:
```bash
awsnap -p <profile_name>
```
This will generate temporary AWS credentials for the specified profile and store them in the ~/.aws/credentials file.

To open your AWS console in a browser session:
```bash
awsnap <your_command_here> --profile <profile_name> --console
```

To get help:
```bash
awsnap --help
```
or
```bash
go see a therapist.
```

The project is available on [pypip](https://pypi.org/project/awsnap/).

## Contributing

Contributions are welcome! Check out the [issues](https://github.com/aphexlog/AWSnap/issues) or submit a pull request.

## License

AWSnap is released under the [MIT License](https://github.com/aphexlog/AWSnap/blob/main/LICENSE).

---

Feel free to reach out with questions, suggestions, or just to say hello. Happy coding!

## Contact Information
- **Author**: Aaron West
- **Email**: aphexlog@gmail.com

---

Thank you for your interest in AWSnap! Follow the project on [GitHub](https://github.com/aphexlog/AWSnap) for the latest updates.
