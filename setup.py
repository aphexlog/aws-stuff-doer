from setuptools import setup, find_packages

# Read the content of the README.md file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="awsnap",
    version="0.6",
    description="AWS SSO Utility",
    author="Aaron West",
    author_email="aphexlog@gmail.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    entry_points={
        "console_scripts": [
            "awsnap=awsnap.awsnap:main",
        ],
    },
    install_requires=[
        "boto3",
    ],
)
